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

from ayarlar import (ARALIK_SN, DERS_ARASI_SN, GUNLUK_SINIR, KAYIT, KUYRUK, SAATLER, STATE, TASLAK, log, oku,
                     yaz)

DOSYALAR = {"deck.json", "ornek_sorular.json", "sozluk.json", "hastaliklar.json", "bilgi_havuzu.jsonl",
            "cikmis_baglantilari.json", "ders_notu.md", "ders_paketi.json", "rapor.md", "denetim.json"}
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
    ("yeniden", re.compile(r"^(?:düzeltme istendi|yeniden derleme istendi|yeniden gönderildi|yarım kalan iş).*$")),
    ("hata", re.compile(r"^(?:Drive taraması hatası|tur hatası|PDF eşleşmesi hatası).*$")),
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
    """izle.sira_isle() kurallarının (saat penceresi, günlük sınır, iki ders arası) bekleyen işlere uygulanmış tahmini.
    İşçi döngüsü Drive taramasıyla birlikte ARALIK_SN'de bir döner; gerçek başlama, plan saatinden sonraki ilk turdur."""
    kuyruk = oku(KUYRUK, [])
    simdi = time.time()
    a, b = (int(x) for x in SAATLER.split("-"))

    def gun_bas(t):
        return time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(t)), "%Y-%m-%d"))

    def pencereye_al(t):
        for _ in range(48):  # saat penceresi dışındaysa bir sonraki uygun saate
            h = time.localtime(t).tm_hour
            if (a <= h < b) if a < b else (h >= a or h < b):
                return t
            t = gun_bas(t) + 3600 * (h + 1)
        return t

    islenen = {}  # gün başlangıcı → o gün taslağa dönen iş sayısı
    for v in oku(KAYIT, {}).values():
        if v.get("durum") == "taslak" and v.get("zaman"):
            islenen[gun_bas(v["zaman"])] = islenen.get(gun_bas(v["zaman"]), 0) + 1
    bugun = islenen.get(gun_bas(simdi), 0)
    son = max((k.get("basladi", 0) or 0 for k in kuyruk), default=0)
    plan = []
    for j in [j for j in kuyruk if j.get("durum") == "bekliyor"]:
        t = max(simdi, j.get("sonra", 0) or 0, son + DERS_ARASI_SN if son else 0)
        for _ in range(60):
            t = pencereye_al(t)
            if islenen.get(gun_bas(t), 0) < GUNLUK_SINIR:
                break
            t = gun_bas(t) + 86400
        islenen[gun_bas(t)] = islenen.get(gun_bas(t), 0) + 1
        son = t
        plan.append({"is_id": j["is_id"], "tahmini": t, "sonra": j.get("sonra", 0) or 0})
    return {"gunluk_sinir": GUNLUK_SINIR, "ders_arasi_sn": DERS_ARASI_SN, "saatler": SAATLER, "aralik_sn": ARALIK_SN,
            "bugun_islenen": bugun,
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
        h = re.match(r"^/kuyruk/([0-9]{8}-[0-9a-f]{10}(?:-\d+)?)/simdi$", self.path.split("?")[0].rstrip("/"))
        if h:
            return self._simdi(h.group(1))
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
        k = {"karar": karar, "not": str(body.get("not") or "")[:4000], "kim": str(body.get("kim") or "")[:200],
             "zaman": time.time()}
        yaz(d / "karar.json", k)
        if karar == "reddet":
            yaz(d / "durum.json", oku(d / "durum.json", {}) | {"durum": "reddedildi", "zaman": time.time()})
        log(f"karar: {d.name} → {karar}" + (f" ({k['not'][:80]})" if k["not"] else ""))
        return self._json(200, {"ok": True, "karar": k})


    def _simdi(self, is_id: str):
        """Programlanmış dersi hemen işle (panel "Hemen işle"): saat penceresi, günlük sınır ve ders arası atlanır.
        Aynı anda tek iş: başka iş işleniyorsa 409. İş arka planda (bu süreçte) çalışır; ders arası sayacı bundan başlar."""
        with _SIMDI_KILIT:
            kuyruk = oku(KUYRUK, [])
            j = next((k for k in kuyruk if k["is_id"] == is_id), None)
            if not j:
                return self._json(404, {"hata": "kuyrukta yok"})
            if j["durum"] != "bekliyor":
                return self._json(409, {"hata": f"iş bekliyor durumunda değil ({j['durum']})"})
            calisan = next((k for k in kuyruk if k["durum"] == "isleniyor"), None)
            if calisan:
                return self._json(409, {"hata": f"şu an başka ders işleniyor: {calisan['yol'].split('/')[-1]}"})
            from izle import sira_isle  # noqa: E402
            log(f"hemen işle istendi (panel): {is_id}")
            threading.Thread(target=self._calistir, args=(sira_isle, is_id), daemon=True, name=f"simdi-{is_id}").start()
            # Durum iş parçacığında 'isleniyor'a geçer; panel yenilendiğinde görünsün diye kısa bekle
            for _ in range(20):
                time.sleep(0.1)
                if any(k["is_id"] == is_id and k["durum"] != "bekliyor" for k in oku(KUYRUK, [])):
                    break
        return self._json(200, {"ok": True})

    @staticmethod
    def _calistir(sira_isle, is_id: str):
        try:
            sira_isle(is_id)
        except Exception as e:  # noqa: BLE001
            log(f"hemen işle hatası: {is_id}: {e!r}")

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


_SIMDI_KILIT = threading.Lock()


def baslat(port: int = 8095):
    srv = ThreadingHTTPServer(("0.0.0.0", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True, name="isci-api").start()
    log(f"iç API dinliyor: :{port}")
    return srv
