#!/usr/bin/env python3
"""Ders başına kalıcı KATMAN MANİFESTİ (Faz 5, HANTALLIK_KOK_NEDENLERI §4). Stdlib; LLM/GPU/ağ yok; veri dosyasına dokunmaz.

  python3 scripts/hat/tam_hat/manifest.py uret <k2-xx> | --kurul 2 | --hepsi [--mod tam|tasarruf] [--kapi-sonucu katman=gecti|kaldi ...]
  python3 scripts/hat/tam_hat/manifest.py goster <key> [--eksik]
  python3 scripts/hat/tam_hat/manifest.py denetle [--kurul N]     # çıkış ≠0: manifest bozuk/bayat ya da dosyası diskte yok
  python3 scripts/hat/tam_hat/manifest.py fark <key>              # son manifestten bu yana değişen/eklenen/silinen dosyalar

Yazılan dosya: <PROJE>/meds_database_v2/ders_bilgi/<key>/katman_manifest.json
  Not: aynı klasördeki `manifest.json` ADI DOLU — `scripts/hat/dersler/bilgi_deposu.py` onu (bilgi deposu: kaynak/özet yolları)
  yazar; kroki, son_prova ve otomasyon/llm/gorevler okur. Ezmemek için katman manifesti ayrı dosyadadır.
Dosya taraması `scripts/altyapi/veri.py`'nin `tara()` mantığıdır (yeniden yazılmadı, içe aktarıldı); katman adları `mod.py`'den.
Kapı komutları `scripts/kapilar/matris.json`'dan yalnız YAZILIR, çalıştırılmaz; sonucu `--kapi-sonucu` ile işlenir.
"""
from __future__ import annotations

import argparse
import fnmatch
import glob
import hashlib
import json
import os
import sys
import time
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import MEDS, PROJE, SCRIPTS  # noqa: E402

sys.path.insert(0, str(SCRIPTS / "altyapi"))
sys.path.insert(0, str(SCRIPTS / "hat" / "tam_hat"))
import veri  # noqa: E402  (tara, rel, kayit_sayisi, ders kayıt defteri okuyucusu)
import mod as kip  # noqa: E402  (KATMANLAR, yapilacak, oku)

SURUM = 1
DB2 = PROJE / "meds_database_v2"
DERS_BILGI = DB2 / "ders_bilgi"
DOSYA_ADI = "katman_manifest.json"
SHA_SINIR = 50 * 1024 * 1024
DIZIN_ACMA_SINIRI = 50          # ≤50 dosyalı dizin dosya dosya yazılır; büyükse (ses klasörü) tek toplu satır
MATRIS = SCRIPTS / "kapilar" / "matris.json"
SES_KOK = MEDS / "data" / "sesli_anlatim"

# ------------------------------------------------------------------ TEK EŞLEME TABLOSU
# katman (mod.py adı) → yol kalıpları (veri.rel() biçimi, fnmatch). Sıra önemlidir: bir dosya İLK eşleşen katmana yazılır.
# {key} = k2-62, {kod} = 2n10 (kayıt defteri), {akod} = 2a62 (ara soru / ders analizi çözücü kodu).
KATMAN_KALIPLARI: list[tuple[str, list[str]]] = [
    ("degerlendirme", ["../meds_database_v2/ders_bilgi/{key}/degerlendirme/paket.json",
                       "../meds_database_v2/ders_bilgi/{key}/degerlendirme/cikmis_taslak.json",
                       "../meds_database_v2/ders_bilgi/{key}/degerlendirme/*"]),
    ("cikmis_analiz", ["../meds_database_v2/ders_bilgi/{key}-*/degerlendirme/cikmis_analiz.json",
                       "src/data/ders_analizi/*", "data/k*dersanaliz_cozucu/*"]),
    ("hazirlik", ["../meds_database_v2/ders_bilgi/*", "data/ogrenci_onem/analiz/*", "src/data/ogrenci_onem/*",
                  "src/data/hoca_vurgu/*", "../meds_database_v2/bilgi_havuzu/*", "../meds_database_v2/kurul*_ders_paketleri/*",
                  "../meds_database_v2/ders_isci/*"]),
    ("anlatim", ["data/sesli_anlatim/metin/*", "data/sesli_anlatim/v2/*"]),
    ("ema_ses", ["data/sesli_anlatim/ses/*"]),
    ("zaman_isaret", ["data/sesli_anlatim/hizalama/*", "data/sesli_anlatim/cumle_zaman/*", "data/sesli_anlatim/kelime_zaman/*",
                      "data/sesli_anlatim/klip_zaman/*", "data/sesli_anlatim/vurgu/*", "data/sesli_anlatim/isaret/*"]),
    ("cikmis_chip", ["data/sesli_anlatim/cikmis_konum/*"]),
    ("terim_kisaltma", ["data/sesli_anlatim/terim/*", "data/sesli_anlatim/kisaltma/*", "data/sesli_anlatim/kisaltma_elle/*"]),
    ("onem_listesi", ["src/data/*_onem/*"]),
    ("ara_soru", ["src/data/k*hocaara_cozucu/*", "data/k*hocaara_cozucu/*"]),
    ("hoca_sorulari", ["src/data/*patolojihoca_cozucu/*", "data/*patolojihoca_cozucu/*", "src/data/hoca_uslubu_sorular/*"]),
    ("ornek_soru", ["src/data/ornek_sorular/*", "../meds_database_v2/ornek_sorular_k*/*", "src/data/*_cozucu/*", "data/*_cozucu/*"]),
    ("ders_icerik", ["src/data/ders_icerik/*"]),
    ("capa_cizim", ["data/sesli_anlatim/capa/*", "data/sesli_anlatim/cizim/*"]),
    ("artik_capa", ["data/sesli_anlatim/capa/*"]),
    ("ara_resim", ["src/data/ara_resim/*", "public/ara_resim/*"]),
    ("ogren_deste", ["src/data/decks/*"]),
]
# Kod adlı (ders anahtarıyla başlamayan, veri.tara()'nın görmediği) dosyalar: kayıt defteri kodundan aranır.
KOD_KALIPLARI = ["src/data/*_onem/{kod}.json", "src/data/*_cozucu/{kod}.json", "src/data/*_cozucu/{akod}.json",
                 "data/*_cozucu/ses/{kod}", "data/*_cozucu/ses/{akod}"]
# Dosya izi olmayan katmanlar (manifestte "izlenmeyen" altında, durum sayımına girmez):
IZLENMEYEN = {
    "denetci": "betik kapıları + denetçi raporu ders klasöründe tutulmuyor",
    "yayin": "commit/dağıtım izi git ve guncelleme_notu.json'da",
    "atomik_envanter": "kalıcı çıktı yolu yok (baglam/ geçici)",
    "pdf_tasarim": "kalıcı çıktı yolu yok",
}
# mod.py katmanı → matris.json aşaması
KAPI_ESLEME = {"degerlendirme": "degerlendirme", "anlatim": "anlatim", "ornek_soru": "ornek_soru", "onem_listesi": "onem",
               "cikmis_analiz": "cikmis_analiz", "ders_icerik": "ders_icerik", "capa_cizim": "cizim", "ara_soru": "ara_soru"}
ATLA_DOSYA = {DOSYA_ADI, "manifest.json"}


# ------------------------------------------------------------------ yardımcılar
def kayit_defteri() -> dict:
    out = {}
    for y in sorted(glob.glob(str(MEDS / "src/data/dersler/k[0-9].json"))):
        try:
            for x in veri.json_yukle(_P(y))["dersler"]:
                out[x["id"]] = x
        except Exception as e:  # noqa: BLE001
            veri.uyari(f"{veri.rel(y)} okunamadı: {e}")
    return out


def man_yolu(key: str) -> _P:
    return DERS_BILGI / key / DOSYA_ADI


def sha1(p: str) -> str:
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def dizin_ozet(p: str) -> tuple[int, int, float]:
    n = boyut = 0
    mt = os.path.getmtime(p)
    for dp, dn, fn in os.walk(p):
        for f in fn:
            try:
                st = os.stat(os.path.join(dp, f))
            except OSError:
                continue
            n += 1
            boyut += st.st_size
            mt = max(mt, st.st_mtime)
    return n, boyut, mt


def dosya_kaydi(p: str, sha=True) -> dict:
    st = os.stat(p)
    if os.path.isdir(p):
        n, b, mt = dizin_ozet(p)
        return {"yol": veri.rel(p), "boyut": b, "mtime": round(mt, 3), "sha1": None, "kayit_sayisi": f"{n} dosya", "dizin": True}
    k = veri.kayit_sayisi(p)
    return {"yol": veri.rel(p), "boyut": st.st_size, "mtime": round(st.st_mtime, 3),
            "sha1": sha1(p) if sha and st.st_size <= SHA_SINIR else None, "kayit_sayisi": k}


def ac(p: str) -> list[str]:
    """Küçük dizini dosyalarına açar; büyük dizin (ses) tek girdi kalır."""
    if not os.path.isdir(p):
        return [p]
    dosyalar = [os.path.join(dp, f) for dp, dn, fn in os.walk(p) for f in fn]
    if len(dosyalar) > DIZIN_ACMA_SINIRI:
        return [p]
    return sorted(f for f in dosyalar if os.path.basename(f) not in ATLA_DOSYA)


def katman_of(rel: str, key: str) -> str | None:
    for katman, kaliplar in KATMAN_KALIPLARI:
        for k in kaliplar:
            if fnmatch.fnmatch(rel, k.format(key=key)):
                return katman
    return None


def ders_dosyalari(key: str, kayit: dict | None, tarama: dict) -> list[str]:
    yollar = []
    for _, dersler in tarama.items():
        yollar += dersler.get(key, [])
    if kayit and kayit.get("kod"):
        kurul, no = key[1], key[3:]
        for k in KOD_KALIPLARI:
            yollar += glob.glob(str(MEDS / k.format(kod=kayit["kod"], akod=f"{kurul}a{no}")))
    out = []
    for y in sorted(set(yollar)):
        out += ac(y)
    return sorted(set(out))


def ders_kipi(key: str) -> tuple[str, str | None]:
    adaylar = glob.glob(str(PROJE / "meds_temp" / "*" / key / "mod.json")) + glob.glob(str(PROJE / "meds_temp" / "*" / f"{key}-*" / "mod.json"))
    if not adaylar:
        return "tam", None
    en_yeni = max(adaylar, key=os.path.getmtime)
    return kip.oku(_P(en_yeni).parent), veri.rel(en_yeni)


_MATRIS = None


def kapi_komutu(katman: str, key: str, kayit: dict | None) -> str | None:
    global _MATRIS
    if _MATRIS is None:
        try:
            _MATRIS = json.loads(MATRIS.read_text(encoding="utf-8"))["asamalar"]
        except Exception as e:  # noqa: BLE001
            veri.uyari(f"matris okunamadı: {e}")
            _MATRIS = {}
    a = _MATRIS.get(KAPI_ESLEME.get(katman, ""))
    if not a:
        return None
    dolgu = {"key": key, "ders": key, "pdf": (kayit or {}).get("pdf") or "{pdf}"}
    arg = [x.format_map(_Kalan(dolgu)) for x in a["arg"]]
    return " ".join(["python3", a["kapi"], *arg])


class _Kalan(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def ses_ozeti(key: str, kayit: dict | None, dosyalar: list[dict]) -> dict:
    klip = 0
    bayt = 0
    for d in dosyalar:
        y = d["yol"]
        if "/ses/" in y or y.startswith("data/sesli_anlatim/ses/"):
            p = MEDS / y if not y.startswith("../") else PROJE / y[3:]
            if p.is_dir():
                for f in p.rglob("*"):
                    if f.suffix in (".mp3", ".pcm") and f.is_file():
                        klip += 1
                        bayt += f.stat().st_size
            elif p.suffix in (".mp3", ".pcm"):
                klip += 1
                bayt += d["boyut"] or 0
    eksik: list[str] = []
    # 1) sesli ders kaydı (kayit.json varyantları) → ses/<slug>/<vid>.mp3
    try:
        kayitlar = json.loads((SES_KOK / "kayit.json").read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        kayitlar = {}
    for slug, vs in kayitlar.items():
        if veri.ders_of(slug) == key and slug.startswith(key):
            for v in vs if isinstance(vs, list) else []:
                f = SES_KOK / "ses" / slug / f"{v.get('id')}.mp3"
                if not f.exists():
                    eksik.append(veri.rel(f))
    # 2) çözücü klipleri: src/data/<b>_cozucu/<kod>.json "klip" → data/<b>_cozucu/ses/<kod>/<klip>.mp3
    if kayit:
        kurul, no = key[1], key[3:]
        for kod in {kayit.get("kod"), f"{kurul}a{no}"} - {None}:
            for j in glob.glob(str(MEDS / f"src/data/*_cozucu/{kod}.json")):
                try:
                    kl = (json.loads(_P(j).read_text(encoding="utf-8")).get("klip") or {})
                except Exception:  # noqa: BLE001
                    continue
                b = _P(j).parent.name
                for kid in kl:
                    f = MEDS / "data" / b / "ses" / kod / f"{kid}.mp3"
                    if not f.exists():
                        eksik.append(veri.rel(f))
    return {"klip_sayisi": klip, "toplam_mb": round(bayt / 1e6, 1), "kayitta_olup_diskte_olmayan_sayi": len(eksik),
            "kayitta_olup_diskte_olmayan": eksik[:20]}


# ------------------------------------------------------------------ üretim
def kur(key: str, kayit: dict | None, tarama: dict, mod_zorla: str | None = None, sha=True) -> dict:
    mod, mod_kaynak = (mod_zorla, "--mod") if mod_zorla else ders_kipi(key)
    yap = kip.yapilacak(mod)
    katmanlar: dict = {}
    siniflanmamis = []
    for p in ders_dosyalari(key, kayit, tarama):
        r = veri.rel(p)
        k = katman_of(r, key)
        if k is None:
            siniflanmamis.append(r)
            continue
        katmanlar.setdefault(k, []).append(dosya_kaydi(p, sha))
    ders_ekle = False
    try:
        ders_ekle = any(veri.ders_of(x.get("key", "")) == key for x in json.loads((SES_KOK / "dersler.json").read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001
        pass
    out_k: dict = {}
    ozet = {"var": 0, "eksik": 0, "atlandi": 0}
    for ad, _acik, *_ in kip.KATMANLAR:
        if ad in IZLENMEYEN:
            continue
        dos = katmanlar.get(ad, [])
        if ad == "ders_ekle":
            var = ders_ekle
        else:
            var = bool(dos)
        gerekli = yap.get(ad, True) and not (ad == "hoca_sorulari" and "patoloji" not in str((kayit or {}).get("brans", "")).lower())
        durum = "var" if var else ("eksik" if gerekli else "atlandi")
        ozet[durum] += 1
        g = {"durum": durum, "dosyalar": dos, "kapi": kapi_komutu(ad, key, kayit)}
        if ad == "ders_ekle" and var:
            g["kanit"] = "data/sesli_anlatim/dersler.json kaydı"
        if durum == "atlandi":
            g["neden"] = "yalnız patoloji (kural 26)" if ad == "hoca_sorulari" and yap.get(ad, True) else "tasarruf kipi" if mod == "tasarruf" and ad not in ("ogren_deste", "quiz") else "askıda/kapalı (AGENTS 19/22)"
        out_k[ad] = g
    dosyalar = [d for v in katmanlar.values() for d in v]
    return {
        "surum": SURUM,
        "ders": {"id": key, "kod": (kayit or {}).get("kod"), "brans": (kayit or {}).get("brans"), "konu": (kayit or {}).get("konu")},
        "kip": mod, "kip_kaynagi": mod_kaynak,
        "uretildi": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "katmanlar": out_k,
        "izlenmeyen": IZLENMEYEN,
        "siniflanmamis": siniflanmamis,
        "ses": ses_ozeti(key, kayit, dosyalar),
        "ozet": ozet,
    }


def _karsilastirilabilir(m: dict) -> dict:
    m = dict(m)
    m.pop("uretildi", None)
    return m


def yaz(key: str, m: dict) -> bool:
    """Atomik yazım; içerik (uretildi hariç) aynıysa ve kapı sonuçları korunarak dokunulmaz. True = yazıldı."""
    p = man_yolu(key)
    eski = oku(key)
    if eski:  # elle/koşucudan işlenen kapı sonuçları korunur
        for ad, g in (eski.get("katmanlar") or {}).items():
            if "kapi_sonucu" in g and ad in m["katmanlar"] and "kapi_sonucu" not in m["katmanlar"][ad]:
                m["katmanlar"][ad]["kapi_sonucu"] = g["kapi_sonucu"]
        if _karsilastirilabilir(eski) == _karsilastirilabilir(m):
            return False
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    return True


def oku(key: str) -> dict | None:
    p = man_yolu(key)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"_bozuk": True}


def secim(a, defter: dict) -> list[str]:
    if getattr(a, "hepsi", False):
        return sorted(defter)
    if getattr(a, "kurul", None):
        return sorted(k for k in defter if k.startswith(f"k{a.kurul}-"))
    return [veri.ders_of(a.key)] if getattr(a, "key", None) else []


# ------------------------------------------------------------------ bayatlık / fark
def fark_hesapla(eski: dict, yeni: dict) -> dict:
    """Dosya düzeyinde fark: eklenen/silinen/değişen (boyut ya da mtime ya da sha1)."""
    def harita(m):
        return {d["yol"]: d for g in (m.get("katmanlar") or {}).values() for d in g.get("dosyalar", [])}
    e, y = harita(eski), harita(yeni)
    degisen = [p for p in sorted(set(e) & set(y))
               if (e[p]["boyut"], e[p]["mtime"]) != (y[p]["boyut"], y[p]["mtime"])
               and not (e[p].get("sha1") and e[p].get("sha1") == y[p].get("sha1"))]
    return {"eklenen": sorted(set(y) - set(e)), "silinen": sorted(set(e) - set(y)), "degisen": degisen}


def hizli_bayat(m: dict) -> tuple[list[str], list[str]]:
    """Kayıtlı dosyalar için ucuz denetim: (diskte_yok, degismis). Yeni eklenen dosyayı görmez (onu fark/denetle yapar)."""
    yok, degis = [], []
    for g in (m.get("katmanlar") or {}).values():
        for d in g.get("dosyalar", []):
            y = d["yol"]
            p = PROJE / y[3:] if y.startswith("../") else MEDS / y
            if not p.exists():
                yok.append(y)
                continue
            if d.get("dizin"):
                _, b, mt = dizin_ozet(str(p))
            else:
                st = p.stat()
                b, mt = st.st_size, st.st_mtime
            if (b, round(mt, 3)) != (d["boyut"], d["mtime"]):
                degis.append(y)
    return yok, degis


def guncel_mi(key: str) -> tuple[dict | None, bool]:
    """veri.py için: (manifest, güncel mi). Yalnız kayıtlı dosyaları denetler (hızlı)."""
    m = oku(key)
    if not m or m.get("_bozuk") or m.get("surum") != SURUM:
        return m, False
    yok, degis = hizli_bayat(m)
    return m, not (yok or degis)


# ------------------------------------------------------------------ komutlar
def k_uret(a) -> int:
    defter = kayit_defteri()
    keys = secim(a, defter)
    if not keys:
        print("ders seçilmedi (k<N>-<NN> | --kurul N | --hepsi)")
        return 2
    sonuc = {}
    for s in a.kapi_sonucu or []:
        k, _, v = s.partition("=")
        if v not in ("gecti", "kaldi"):
            print(f"--kapi-sonucu biçimi katman=gecti|kaldi: {s}")
            return 2
        sonuc[k] = v
    if sonuc and len(keys) != 1:
        print("--kapi-sonucu yalnız tek derste")
        return 2
    t0 = time.time()
    tarama = veri.tara()
    yazilan = 0
    for key in keys:
        if key not in defter:
            veri.uyari(f"{key}: ders kayıt defterinde yok — yine de üretiliyor")
        m = kur(key, defter.get(key), tarama, a.mod)
        for k, v in sonuc.items():
            if k not in m["katmanlar"]:
                print(f"bilinmeyen katman: {k}")
                return 2
        if sonuc:
            eski = oku(key) or {}
            for ad, g in (eski.get("katmanlar") or {}).items():
                if "kapi_sonucu" in g and ad in m["katmanlar"]:
                    m["katmanlar"][ad]["kapi_sonucu"] = g["kapi_sonucu"]
            for k, v in sonuc.items():
                m["katmanlar"][k]["kapi_sonucu"] = {"sonuc": v, "zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}
        w = yaz(key, m)
        yazilan += w
        if len(keys) == 1 or a.ayrinti:
            o = m["ozet"]
            print(f"{key}: var {o['var']} · eksik {o['eksik']} · atlandı {o['atlandi']} — {'yazıldı' if w else 'değişmedi'} ({veri.rel(man_yolu(key))})")
    print(f"{len(keys)} ders, {yazilan} manifest yazıldı/güncellendi, {time.time() - t0:.1f} sn")
    return 0


def k_goster(a) -> int:
    key = veri.ders_of(a.key)
    m = oku(key)
    if not m or m.get("_bozuk"):
        print(f"{key}: manifest {'BOZUK' if m else 'yok'} → manifest.py uret {key}")
        return 1
    print(goster_metin(m, a.eksik))
    return 0


def goster_metin(m: dict, yalniz_eksik=False) -> str:
    d = m["ders"]
    o = m["ozet"]
    s = m["ses"]
    sat = [f"{d['id']} {d.get('kod') or ''} | {d.get('brans') or ''} — {d.get('konu') or ''} | kip {m.get('kip')} | {m.get('uretildi')}",
           f"özet: var {o['var']} · eksik {o['eksik']} · atlandı {o['atlandi']} | ses: {s['klip_sayisi']} klip, {s['toplam_mb']} MB, "
           f"kayıtta olup diskte yok {s.get('kayitta_olup_diskte_olmayan_sayi', 0)}",
           f"{'katman':<16}{'durum':<9}{'dosya':>6}{'KB':>9}  kapı / ilk dosya"]
    for ad, g in m["katmanlar"].items():
        if yalniz_eksik and g["durum"] != "eksik":
            continue
        kb = sum(x["boyut"] or 0 for x in g["dosyalar"]) / 1024
        ks = g.get("kapi_sonucu", {}).get("sonuc")
        ek = (g["dosyalar"][0]["yol"] if g["dosyalar"] else (g.get("neden") or g.get("kapi") or "-"))
        sat.append(f"{ad:<16}{g['durum'] + ('/' + ks if ks else ''):<9}{len(g['dosyalar']):>6}{kb:>9.0f}  {ek[:70]}")
    if m.get("siniflanmamis"):
        sat.append(f"sınıflanmamış {len(m['siniflanmamis'])}: " + ", ".join(m["siniflanmamis"][:3]))
    return "\n".join(sat[:40])


def k_fark(a) -> int:
    key = veri.ders_of(a.key)
    eski = oku(key)
    if not eski or eski.get("_bozuk"):
        print(f"{key}: önceki manifest yok/bozuk")
        return 1
    defter = kayit_defteri()
    yeni = kur(key, defter.get(key), veri.tara(), eski.get("kip") if eski.get("kip_kaynagi") == "--mod" else None)
    f = fark_hesapla(eski, yeni)
    for t in ("eklenen", "silinen", "degisen"):
        for y in f[t]:
            print(f"{t[0].upper()} {y}")
    dur = [f"{ad}: {eski['katmanlar'].get(ad, {}).get('durum')}→{g['durum']}" for ad, g in yeni["katmanlar"].items()
           if eski["katmanlar"].get(ad, {}).get("durum") != g["durum"]]
    if dur:
        print("katman durumu değişti: " + "; ".join(dur))
    print(f"{key}: +{len(f['eklenen'])} -{len(f['silinen'])} ~{len(f['degisen'])} (manifest {eski.get('uretildi')})")
    return 0


def k_denetle(a) -> int:
    t0 = time.time()
    defter = kayit_defteri()
    keys = sorted(k for k in defter if not a.kurul or k.startswith(f"k{a.kurul}-"))
    tarama = veri.tara()
    hata = 0
    yok_n = 0
    eksik_tablo: dict[int, dict[str, list[str]]] = {}
    for key in keys:
        m = oku(key)
        taze = kur(key, defter[key], tarama, m.get("kip") if m and m.get("kip_kaynagi") == "--mod" else None, sha=False)
        if m is None:
            yok_n += 1
        elif m.get("_bozuk") or m.get("surum") != SURUM:
            print(f"HATA {key}: manifest bozuk/eski sürüm")
            hata += 1
        else:
            yok, _ = hizli_bayat(m)
            f = fark_hesapla(m, taze)
            if yok:
                print(f"HATA {key}: manifestteki {len(yok)} dosya diskte yok (ör. {yok[0]})")
                hata += 1
            elif f["eklenen"] or f["degisen"] or f["silinen"]:
                print(f"HATA {key}: bayat (+{len(f['eklenen'])} ~{len(f['degisen'])} -{len(f['silinen'])}) → manifest.py uret {key}")
                hata += 1
        for ad, g in taze["katmanlar"].items():
            if g["durum"] == "eksik":
                eksik_tablo.setdefault(int(key[1]), {}).setdefault(ad, []).append(key)
    if yok_n:
        print(f"UYARI {yok_n}/{len(keys)} derste manifest yok (eksik katman tablosu canlı taramadan)")
    for kurul, t in sorted(eksik_tablo.items()):
        n = sum(1 for k in keys if k.startswith(f"k{kurul}-"))
        print(f"UYARI Kurul {kurul} ({n} ders) eksik katmanlar:")
        for ad, lst in sorted(t.items(), key=lambda x: -len(x[1])):
            print(f"  {ad:<16}{len(lst):>4} ders  " + " ".join(lst[:8]) + (" …" if len(lst) > 8 else ""))
        sayac: dict[str, int] = {}
        for lst in t.values():
            for k in lst:
                sayac[k] = sayac.get(k, 0) + 1
        en = sorted(sayac.items(), key=lambda x: (-x[1], x[0]))[:5]
        print("  en eksik: " + ", ".join(f"{k} ({v})" for k, v in en))
    print(f"{len(keys)} ders, {hata} HATA (bozuk/bayat/kayıp), {time.time() - t0:.1f} sn")
    return 1 if hata else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="manifest.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    p = alt.add_parser("uret")
    p.add_argument("key", nargs="?")
    p.add_argument("--kurul", type=int)
    p.add_argument("--hepsi", action="store_true")
    p.add_argument("--mod", choices=kip.KIPLER, help="kipi zorla (yoksa meds_temp/*/<key>/mod.json, o da yoksa tam)")
    p.add_argument("--kapi-sonucu", action="append", metavar="KATMAN=gecti|kaldi")
    p.add_argument("--ayrinti", action="store_true")
    p.set_defaults(f=k_uret)
    p = alt.add_parser("goster")
    p.add_argument("key")
    p.add_argument("--eksik", action="store_true")
    p.set_defaults(f=k_goster)
    p = alt.add_parser("denetle")
    p.add_argument("--kurul", type=int)
    p.set_defaults(f=k_denetle)
    p = alt.add_parser("fark")
    p.add_argument("key")
    p.set_defaults(f=k_fark)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
