"""Ders işçisi iç API'si (yalnız compose iç ağı; dışarıya port açılmaz). Site (meds-app) /api/admin/ders-isci/* altında
yönetici yetkisiyle buraya vekil olur.

  GET  /saglik                         → {"ok": true}
  GET  /taslaklar                      → [{is_id, durum, ozet, ders_id, deste_id, mod, uyari, program, sayilar, karar, zaman}]
  GET  /taslak/<is_id>                 → {baglam özeti, rapor (md), denetim, karar}
  GET  /taslak/<is_id>/dosya/<ad>      → çıktı dosyası (deck.json, ornek_sorular.json, sozluk.json, hastaliklar.json,
                                          bilgi_havuzu.jsonl, cikmis_baglantilari.json, ders_notu.md, ders_paketi.json)
  POST /taslak/<is_id>/karar           ← {"karar": "onayla"|"reddet"|"duzelt", "not": "...", "kim": "..."}
  GET  /checklist                      → checklist.json (2026-27 durum raporu verisi)
  GET  /kuyruk                         → kuyruk.json özeti (sonra/basladi dahil)
  GET  /zamanlama                      → işçi zamanlaması + bekleyen işlerin tahmini başlama saatleri (plan)
Kararlar taslak/<is_id>/karar.json'a yazılır; birleştirme (yayın) ayrı adımdır.
"""
from __future__ import annotations

import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ayarlar import (AYAR_TANIM, EFORLAR, KAYIT, KUYRUK, KUYRUK_KILIT, MODELLER, STATE, TASLAK, ayar, ayar_kaydet,
                     log, oku, yaz)

DOSYALAR = {"deck.json", "ornek_sorular.json", "sozluk.json", "hastaliklar.json", "bilgi_havuzu.jsonl",
            "cikmis_baglantilari.json", "ders_notu.md", "ders_paketi.json", "rapor.md", "denetim.json", "konusma_metni.md"}
GECERLI_ID = re.compile(r"^[0-9]{8}-[0-9a-f]{10}(?:-\d+)?$")


def taslak_ozeti(d) -> dict:
    b = oku(d / "baglam.json", {})
    du = oku(d / "durum.json", {})
    den = oku(d / "denetim.json", {})
    return {"is_id": d.name, "durum": du.get("durum") or "isleniyor", "ozet": du.get("ozet", ""),
            "ders_id": b.get("ders_id"), "deste_id": b.get("deste_id"), "mod": b.get("mod"), "uyari": b.get("uyari", ""),
            "pdf": b.get("pdf_adi"), "program": {k: (b.get("program") or {}).get(k) for k in
                                                  ("kurul", "ders", "konu", "ogretim_uyesi", "tarih", "guven", "skor")},
            "sayilar": den.get("sayilar", {}), "denetim_hata": den.get("hata"), "referans": len(den.get("referansla_tamamlanan", [])),
            "karar": oku(d / "karar.json", None), "yayin": oku(d / "yayin.json", None), "zaman": du.get("zaman")}


# Panel "Drive etkinliği": günlükten iş yaşam döngüsü satırları (Drive'dan gelen PDF kuyruğa alındı → işleniyor → taslak → karar)
OLAY_TURLERI = [
    ("kuyruga", re.compile(r"^kuyruğa alındı: (.+)$")),
    ("isleniyor", re.compile(r"^işleniyor: \S+ (.+)$")),
    ("taslak", re.compile(r"^taslak hazır: \S+ → (.+)$")),
    ("karar", re.compile(r"^karar: (\S+ → \S+)$")),
    ("simdi", re.compile(r"^hemen işle istendi \(panel\): (\S+)$")),
    ("panel", re.compile(r"^((?:ayar değişti|kuyruk eylemi|Drive taraması istendi|elle kuyruğa alma istendi|sadakat eşiği yok sayıldı).*)$")),
    ("yeniden", re.compile(r"^(?:düzeltme istendi|yeniden derleme istendi|yeniden gönderildi|yarım kalan iş).*$")),
    ("hata", re.compile(r"^(?:Drive taraması hatası|tur hatası|PDF eşleşmesi hatası|hemen işle hatası).*$")),
]


def olaylar(sinir: int = 40) -> dict:
    try:
        with open(STATE / "gunluk.log", "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 200_000))
            satirlar = f.read().decode("utf-8", "replace").splitlines()
    except OSError:
        satirlar = []
    out = []
    for sat in satirlar:
        m = re.match(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (.*)$", sat)
        if not m:
            continue
        for tur, rx in OLAY_TURLERI:
            r = rx.match(m.group(2))
            if r:
                metin = r.group(1) if r.groups() else m.group(2)
                out.append({"zaman": time.mktime(time.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")), "tur": tur, "metin": metin[:300]})
                break
    return {"son_tarama": oku(STATE / "son_tarama.json", None), "olaylar": out[-sinir:][::-1]}


def zamanlama() -> dict:
    """izle._sec() kurallarının (duraklat, saat penceresi, günlük sınır, iki ders arası) bekleyen işlere uygulanmış tahmini.
    Döngü 30 sn'de bir döner; gerçek başlama plan saatinden en geç ~1 dk sonradır."""
    kuyruk = oku(KUYRUK, [])
    simdi = time.time()
    a_ = ayar()
    a, b = a_["saat_bas"], a_["saat_bit"]
    ara = a_["ders_arasi_dk"] * 60

    def gun_bas(t):
        return time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(t)), "%Y-%m-%d"))

    def uygun(h):
        return (a <= h < b) if a < b else (h >= a or h < b)

    def pencereye_al(t):
        for _ in range(48):  # saat penceresi dışındaysa bir sonraki uygun saate
            if uygun(time.localtime(t).tm_hour):
                return t
            t = gun_bas(t) + 3600 * (time.localtime(t).tm_hour + 1)
        return t

    baslanan = {}  # gün başlangıcı → o gün işlenmeye başlanan iş sayısı
    for k in kuyruk:
        if k.get("basladi"):
            baslanan[gun_bas(k["basladi"])] = baslanan.get(gun_bas(k["basladi"]), 0) + 1
    bugun = baslanan.get(gun_bas(simdi), 0)
    son = max((k.get("basladi", 0) or 0 for k in kuyruk), default=0)
    calisan = next((k for k in kuyruk if k.get("durum") == "isleniyor"), None)
    plan = []
    if not a_["duraklat"]:
        for j in [j for j in kuyruk if j.get("durum") == "bekliyor"]:
            t = max(simdi, j.get("sonra", 0) or 0, son + ara if son else 0)
            if calisan and not plan:  # çalışan ders bitmeden yenisi başlamaz (~45 dk varsayımı)
                t = max(t, (calisan.get("basladi") or simdi) + 2700)
            for _ in range(60):
                t = pencereye_al(t)
                if baslanan.get(gun_bas(t), 0) < a_["gunluk_sinir"]:
                    break
                t = gun_bas(t) + 86400
            baslanan[gun_bas(t)] = baslanan.get(gun_bas(t), 0) + 1
            son = t
            plan.append({"is_id": j["is_id"], "tahmini": t, "sonra": j.get("sonra", 0) or 0})
    return {"gunluk_sinir": a_["gunluk_sinir"], "ders_arasi_sn": ara, "saatler": f"{a:02d}-{b:02d}",
            "aralik_sn": a_["tarama_dk"] * 60, "duraklat": a_["duraklat"], "bugun_islenen": bugun,
            "plan": plan, "zaman": simdi}


class H(BaseHTTPRequestHandler):
    # HTTP/1.1 kalıcı bağlantı: varsayılan HTTP/1.0 her yanıttan sonra soketi kapatır; Node (undici) soketi havuzda canlı
    # sanıp yeniden kullanmaya çalışınca istek zaman aşımına kadar asılı kalıyordu (bekleme sonrası ilk istek 10–27 sn).
    protocol_version = "HTTP/1.1"
    timeout = 60  # boşta kalan bağlantıyı tutan iş parçacığı sonsuza dek beklemesin

    def log_message(self, *a):
        pass

    def _json(self, code: int, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _metin(self, code: int, txt: str, tur: str):
        b = txt.encode()
        self.send_response(code)
        self.send_header("Content-Type", f"{tur}; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _taslak(self, is_id: str):
        if not GECERLI_ID.match(is_id or ""):
            return None
        d = TASLAK / is_id
        return d if d.is_dir() else None

    def do_GET(self):  # noqa: N802
        yol = self.path.split("?")[0].rstrip("/")
        if yol == "/saglik":
            return self._json(200, {"ok": True})
        if yol == "/taslaklar":
            liste = [taslak_ozeti(d) for d in TASLAK.iterdir() if d.is_dir() and (d / "baglam.json").exists()]
            return self._json(200, sorted(liste, key=lambda x: x.get("zaman") or 0, reverse=True))
        if yol == "/checklist":
            return self._json(200, oku(STATE / "checklist.json", {}))
        if yol == "/kuyruk":
            return self._json(200, [{k: j.get(k) for k in ("is_id", "yol", "durum", "eklendi", "deneme", "son_mesaj",
                                                                 "sonra", "basladi", "uyari")}
                                    | {"konular": [k.get("konu") for k in j.get("konular") or []]} for j in oku(KUYRUK, [])])
        if yol == "/ayarlar":
            return self._json(200, {"ayar": ayar(), "modeller": MODELLER, "eforlar": EFORLAR,
                                    "sinirlar": {k: [v[2], v[3]] for k, v in AYAR_TANIM.items() if v[2] is not None}})
        if yol == "/olaylar":
            return self._json(200, olaylar())
        if yol == "/zamanlama":
            return self._json(200, zamanlama())
        m = re.match(r"^/taslak/([^/]+)(?:/dosya/([^/]+))?$", yol)
        if m:
            d = self._taslak(m.group(1))
            if not d:
                return self._json(404, {"hata": "taslak yok"})
            if m.group(2):
                ad = m.group(2)
                if ad not in DOSYALAR or not (d / ad).exists():
                    return self._json(404, {"hata": "dosya yok"})
                txt = (d / ad).read_text(encoding="utf-8")
                return self._metin(200, txt, "application/json" if ad.endswith(".json") else "text/plain")
            o = taslak_ozeti(d)
            o["rapor"] = (d / "rapor.md").read_text(encoding="utf-8") if (d / "rapor.md").exists() else ""
            o["denetim"] = oku(d / "denetim.json", {})
            o["dosyalar"] = sorted(x.name for x in d.iterdir() if x.name in DOSYALAR)
            return self._json(200, o)
        return self._json(404, {"hata": "yol yok"})

    def do_POST(self):  # noqa: N802
        yol = self.path.split("?")[0].rstrip("/")
        h = re.match(r"^/kuyruk/([0-9]{8}-[0-9a-f]{10}(?:-\d+)?)/(simdi|one-al|sona-at|kaldir|yeniden-dene)$", yol)
        if h:
            return self._simdi(h.group(1)) if h.group(2) == "simdi" else self._kuyruk_eylem(h.group(1), h.group(2))
        if yol in ("/ayarlar", "/tara", "/pdf/kuyruga") or re.match(r"^/taslak/[^/]+/esik-atla$", yol):
            try:
                body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 20000)) or b"{}")
            except Exception:  # noqa: BLE001
                return self._json(400, {"hata": "geçersiz JSON"})
            if yol == "/ayarlar":
                return self._json(200, {"ayar": ayar_kaydet(body.get("ayar") or {}, str(body.get("kim") or "")[:200])})
            if yol == "/tara":
                yaz(STATE / "tara_iste.json", {"zaman": time.time(), "yollar": []})
                log("Drive taraması istendi (panel)")
                return self._json(200, {"ok": True})
            if yol == "/pdf/kuyruga":
                yollar = [str(x)[:400] for x in (body.get("yollar") or []) if x][:20]
                if not yollar:
                    return self._json(400, {"hata": "yollar boş"})
                eski = oku(STATE / "tara_iste.json", None) or {}
                yaz(STATE / "tara_iste.json", {"zaman": time.time(), "yollar": sorted(set((eski.get("yollar") or []) + yollar))})
                log("elle kuyruğa alma istendi (panel): " + ", ".join(yollar))
                return self._json(200, {"ok": True})
            return self._esik_atla(yol.split("/")[2])
        y = re.match(r"^/taslak/([^/]+)/yeniden$", self.path.split("?")[0].rstrip("/"))
        if y:
            return self._yeniden(y.group(1))
        m = re.match(r"^/taslak/([^/]+)/karar$", self.path.split("?")[0].rstrip("/"))
        d = self._taslak(m.group(1)) if m else None
        if not d:
            return self._json(404, {"hata": "taslak yok"})
        try:
            body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 20000)) or b"{}")
        except Exception:  # noqa: BLE001
            return self._json(400, {"hata": "geçersiz JSON"})
        karar = body.get("karar")
        if karar not in ("onayla", "reddet", "duzelt"):
            return self._json(400, {"hata": "karar onayla|reddet|duzelt olmalı"})
        if oku(d / "durum.json", {}).get("durum") != "onay_bekliyor":
            return self._json(409, {"hata": "taslak onay beklemiyor"})
        if (oku(d / "karar.json", {}) or {}).get("karar") == "onayla" and \
                (oku(d / "yayin.json", {}) or {}).get("durum") != "denetim_hatasi":
            return self._json(409, {"hata": "taslak onaylandı; yayın sürüyor"})
        k = {"karar": karar, "not": str(body.get("not") or "")[:4000], "kim": str(body.get("kim") or "")[:200],
             "zaman": time.time()}
        yaz(d / "karar.json", k)
        if karar != "onayla":
            (d / "yayin.json").unlink(missing_ok=True)  # yayın denetimine takılmış taslakta yeni karar
        if karar == "reddet":
            yaz(d / "durum.json", oku(d / "durum.json", {}) | {"durum": "reddedildi", "zaman": time.time()})
        log(f"karar: {d.name} → {karar}" + (f" ({k['not'][:80]})" if k["not"] else ""))
        return self._json(200, {"ok": True, "karar": k})


    def _simdi(self, is_id: str):
        """Programlanmış dersi hemen işle (panel "Hemen işle"): duraklat, saat penceresi, günlük sınır ve ders arası
        atlanır. Aynı anda tek iş: başka iş işleniyorsa 409. İş, döngünün işleme iş parçacığında başlar."""
        with KUYRUK_KILIT:
            kuyruk = oku(KUYRUK, [])
            j = next((k for k in kuyruk if k["is_id"] == is_id), None)
            if not j:
                return self._json(404, {"hata": "kuyrukta yok"})
            if j["durum"] not in ("bekliyor", "hata"):
                return self._json(409, {"hata": f"iş bekliyor durumunda değil ({j['durum']})"})
            calisan = next((k for k in kuyruk if k["durum"] == "isleniyor"), None)
            if calisan:
                return self._json(409, {"hata": f"şu an başka ders işleniyor: {calisan['yol'].split('/')[-1]}"})
            if j["durum"] == "hata":
                j.update(durum="bekliyor", deneme=0, sonra=0)
                yaz(KUYRUK, kuyruk)
        import izle  # noqa: E402  (izle.main sys.modules'a kendini koyar: aynı iş parçacığı kaydı)
        log(f"hemen işle istendi (panel): {is_id}")
        if not izle.isi_baslat(is_id):
            return self._json(409, {"hata": "işleme iş parçacığı meşgul"})
        for _ in range(20):
            time.sleep(0.1)
            if any(k["is_id"] == is_id and k["durum"] != "bekliyor" for k in oku(KUYRUK, [])):
                break
        return self._json(200, {"ok": True})

    def _kuyruk_eylem(self, is_id: str, eylem: str):
        with KUYRUK_KILIT:
            kuyruk = oku(KUYRUK, [])
            j = next((k for k in kuyruk if k["is_id"] == is_id), None)
            if not j:
                return self._json(404, {"hata": "kuyrukta yok"})
            if j["durum"] == "isleniyor":
                return self._json(409, {"hata": "iş şu an işleniyor"})
            if eylem in ("one-al", "sona-at"):
                if j["durum"] != "bekliyor":
                    return self._json(409, {"hata": "yalnız bekleyen iş sıralanır"})
                kuyruk.remove(j)
                bekleyen = [i for i, k in enumerate(kuyruk) if k["durum"] == "bekliyor"]
                if eylem == "one-al":
                    kuyruk.insert(bekleyen[0] if bekleyen else len(kuyruk), j)
                    j["sonra"] = 0
                else:
                    kuyruk.insert(bekleyen[-1] + 1 if bekleyen else len(kuyruk), j)
                # öncelik sıralaması (duzeltmeleri_isle) listeyi bozmasın: sıra = liste sırası
                for n, k in enumerate(kuyruk):
                    if k["durum"] == "bekliyor":
                        k["oncelik"] = 0
            elif eylem == "yeniden-dene":
                if j["durum"] not in ("hata", "bekliyor"):
                    return self._json(409, {"hata": f"iş {j['durum']} durumunda"})
                j.update(durum="bekliyor", deneme=0, sonra=0)
                kayit = oku(KAYIT, {})
                if kayit.get(j.get("sha256"), {}).get("durum") == "hata":
                    kayit.pop(j["sha256"], None)
                    yaz(KAYIT, kayit)
            elif eylem == "kaldir":
                if j["durum"] not in ("bekliyor", "hata"):
                    return self._json(409, {"hata": f"iş {j['durum']} durumunda"})
                kuyruk.remove(j)
                kayit = oku(KAYIT, {})
                kayit[j["sha256"]] = {"durum": "atlandi", "yol": j["yol"], "is_id": is_id, "zaman": time.time()}
                yaz(KAYIT, kayit)
            yaz(KUYRUK, kuyruk)
        log(f"kuyruk eylemi (panel): {is_id} → {eylem}")
        return self._json(200, {"ok": True})

    def _esik_atla(self, is_id: str):
        """Onaylı taslak yalnız ders notu sadakat eşiğine takıldıysa: eşiği bu taslak için yok say ve yeniden gönder."""
        d = self._taslak(is_id)
        if not d:
            return self._json(404, {"hata": "taslak yok"})
        k = oku(d / "karar.json", {}) or {}
        y = oku(d / "yayin.json", {}) or {}
        if k.get("karar") != "onayla" or y.get("durum") != "denetim_hatasi":
            return self._json(409, {"hata": "yalnız yayın denetimine takılmış onaylı taslakta"})
        hatalar = y.get("hatalar") or []
        if not hatalar or any("sadakati" not in h for h in hatalar):
            return self._json(409, {"hata": "sadakat dışında hata var; düzeltme iste"})
        yaz(d / "karar.json", k | {"esik_atla": True})
        (d / "yayin.json").unlink(missing_ok=True)
        log(f"sadakat eşiği yok sayıldı, yeniden gönderildi (panel): {is_id}")
        return self._json(200, {"ok": True})

    def _yeniden(self, is_id: str):
        """Onaylanıp siteye geçmeyen taslağı yeniden gönder: yayın hatasında yayin.json silinir (yayın zamanlayıcısı
        ≤10 dk içinde yeniden dener); yayınlanıp site derlenemediyse derleme isteği bırakılır."""
        d = self._taslak(is_id)
        if not d:
            return self._json(404, {"hata": "taslak yok"})
        if (oku(d / "karar.json", {}) or {}).get("karar") != "onayla":
            return self._json(409, {"hata": "taslak onaylanmamış"})
        y = oku(d / "yayin.json", None)
        if not y:
            return self._json(409, {"hata": "taslak zaten yayın sırasında"})
        if y.get("durum") == "yayinlandi":
            if y.get("site_derlendi") is not False:
                return self._json(409, {"hata": "taslak sitede yayında"})
            yaz(d.parent / "derle_iste.json", {"is_id": d.name, "zaman": time.time()})
            log(f"yeniden derleme istendi: {d.name}")
            return self._json(200, {"ok": True, "is": "derle"})
        (d / "yayin.json").unlink(missing_ok=True)
        log(f"yeniden gönderildi: {d.name} (önceki: {y.get('durum')})")
        return self._json(200, {"ok": True, "is": "yayinla"})




def baslat(port: int = 8095):
    srv = ThreadingHTTPServer(("0.0.0.0", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True, name="isci-api").start()
    log(f"iç API dinliyor: :{port}")
    return srv
