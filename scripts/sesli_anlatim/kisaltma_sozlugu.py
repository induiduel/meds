#!/usr/bin/env python3
"""Sesli ders PDF yardımcısı — slayt başına KISALTMA sözlüğü (kullanıcı isteği 2026-10-26).

Terim yardımcısından ayrı bir katman: slaytta geçen kısaltmaların (DD, ÜSYE, VUR, GSBL …) açılımı yazılır.
Kısaltma çoğu zaman yalnız o derse/slayta özgüdür (kurum içi kullanım), bu yüzden açılım **o dersin kendi
metninden** çıkarılır: "Üst solunum yolu enfeksiyonu (ÜSYE)", "ÜSYE: Üst solunum yolu enfeksiyonu",
"ÜSYE (Üst solunum yolu enfeksiyonu)". Metinde açılımı yazmayan kısaltmalar yalnız elle/bilinen eşlemesi varsa
yazılır — yanlış açılım hiç yazılmaz.

Akış:
  1. adaylar  KEY             → sayfa sayfa kısaltma adayları + metinden bulunan açılımlar (denetim listesi)
  2. otomatik KEY [--yaz]     → açılımı metinde bulunanları (ve bilinen/elle eşlemeyi) yazar
  3. dogrula  KEY DOSYA [--yaz] → kapı 0 HATA; --yaz: data/sesli_anlatim/kisaltma/<key>.json
  4. sozluk_disa              → src/data/kisaltma_sozluk.json (Terimler sayfasında ayrı bölüm)

Yazar biçimi:
  { "key": "...", "s": { "<dosya>:<sayfa>": [ { "t": "ÜSYE", "acilim": "Üst solunum yolu enfeksiyonu",
                                                "a": "Üst solunum yolu enfeksiyonu. Burun, farenks ve …", "k": "kisaltma" } ] } }
Çıktı (sunucu → ön yüz, canliDers.ts `kisaltma`):
  { surum, key, uretici: "deepseek", d: { "<dosya>": { "<sayfa>": { bos, t: [ { t, acilim, a, k, b: [[x0,y0,x1,y1], …] } ] } } } }
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import terim_sozlugu as T  # noqa: E402

MEDS = T.MEDS
KOK_KIS = T.KOK / "kisaltma"
ARSIV_KIS = T.ARSIV_KOK / "kisaltma"
ELLE_KOK = T.KOK / "kisaltma_elle"
BILINEN = T.KOK / "kisaltma_bilinen.json"
SURUM = 1
EN_COK = 8          # sayfa başına kısaltma
A_ENAZ, A_ENCOK = 12, 240
AC_ENCOK = 90       # açılımın kendisi

# Tümü büyük harf (2–6) ya da en az iki büyük harf + rakam içeren kısa diziler (SpO2, HbA1c, T3)
KIS_BUYUK = re.compile(r"^[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ0-9]{1,5}$")
KIS_KARMA = re.compile(r"^(?=(?:.*[A-ZÇĞİÖŞÜ]){2})[A-ZÇĞİÖŞÜ][A-Za-zÇĞİÖŞÜçğıöşü0-9]{1,7}$")
# Başlık, unvan, romen rakamı, gündelik sözcük: kısaltma değil
STOP = {
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    "DR", "PROF", "DOC", "ARS", "GOR", "UZM", "OPR", "AM", "VE", "BU", "NE", "BIR", "ILE", "ICIN", "VEYA",
    "TIP", "FAK", "UNV", "SAY", "SIRA", "TABLO", "SEKIL", "KAYNAK", "SLYAT", "SLAY", "TR", "EN", "VK",
}


def kok_kis(key: str) -> Path:
    return ARSIV_KIS if T.ARSIV.match(key) else KOK_KIS


# ── Türkçe sözlük (hunspell): "BİLİNÇ", "KOMA", "NÖBET" gibi büyük harfli sözcükler kısaltma değildir ───────────
_TR: set[str] | None = None
_EKLER = sorted("""leri ları ler lar leri lari nin nun nın nün nda nde ndan nden yla yle yız yiz dir dur tır tür
    dan den tan ten da de ta te ye ya yi yı yu yü in un ın ün i u ı ü e a n m k si sı su sü y""".split(), key=len, reverse=True)


def tr_kokler() -> set[str]:
    global _TR
    if _TR is None:
        _TR = set()
        try:
            with Path("/usr/share/hunspell/tr_TR.dic").open(encoding="utf-8") as f:
                next(f, None)
                for satir in f:
                    s = satir.split("/")[0].strip()
                    if s and not s.startswith("#"):
                        _TR.add(T.fold(s))
        except OSError:
            pass
    return _TR


def turkce_sozcuk(w: str) -> bool:
    """Büyük harfle yazılmış olsa da Türkçe sözlükte bulunan sözcük (ekleriyle) kısaltma sayılmaz."""
    kokler = tr_kokler()
    f = T.fold(w)
    if f in kokler:
        return True
    for ek in _EKLER:
        if f.endswith(ek) and len(f) > len(ek) + 2 and f[: -len(ek)] in kokler:
            return True
    return False



# ── aday bulma ────────────────────────────────────────────────────────────────────────────────────────────────────
_BILINEN_CACHE: dict[str, str] | None = None


def kisaltma_mi(w: str) -> bool:
    w = w.strip(".,;:!?()[]'\"’“”")
    if not w or w.upper() in STOP:
        return False
    if "\u0307" in w:  # "İ" ayrışık gelmişse
        return False
    global _BILINEN_CACHE
    if _BILINEN_CACHE is None:
        _BILINEN_CACHE = bilinen()
    if w in _BILINEN_CACHE:  # elle/bilinen sözlükte olan kısaltma Türkçe sözcüğe benzese de kabul (SAK, KS)
        return True
    if turkce_sozcuk(w):  # BİLİNÇ, KOMA, NÖBET gibi büyük harfli Türkçe sözcükler
        return False
    if KIS_BUYUK.match(w):
        return True
    return bool(KIS_KARMA.match(w)) and any(c.isdigit() for c in w)


def adaylar(s: T.Sayfa) -> list[str]:
    """Sayfadaki kısaltma adayları (geçiş sırasıyla, tekrarsız)."""
    out: list[str] = []
    for w in s.metin_satir:
        for ham in re.split(r"[\s,;:()\[\]\"\uf000-\uf8ff•▪■□◆✓✔]+", w):  # H89: yapışık madde imi glifi (U+F06E…) ayırıcıdır
            for parca in re.split(r"[/\-–+]", ham):  # "HT+DM" bitişik yazımı (2026-10-27)
                parca = parca.strip(".,;:!?'\"’“”")
                if kisaltma_mi(parca) and parca not in out:
                    out.append(parca)
    return out


def metin(s: T.Sayfa) -> str:
    return " ".join(s.metin_satir)


def acilim_bul(s: T.Sayfa, kis: str) -> str:
    """Slaytın kendi metninden açılımı çıkarır: "Açılım (KIS)", "KIS (Açılım)", "KIS: Açılım", "KIS = Açılım"."""
    m = metin(s)
    k = re.escape(kis)
    # 1) "Açılım (KIS)" — cümle/ölçü sınırından sonrası, en çok 5 sözcük, yüklem içermez
    for esles in re.finditer(r"([^•·|;:()\n]{5,90}?)\s*\(\s*" + k + r"\s*\)", m):
        ad = temiz(esles.group(1))
        if ad:
            return ad
    # 2) "KIS (Açılım)"
    for esles in re.finditer(r"(?<![\wçğıöşü])" + k + r"\s*\(\s*([^)]{5,90})\)", m):
        ad = temiz(esles.group(1))
        if ad:
            return ad
    # 3) "KIS: Açılım" / "KIS = Açılım"
    for esles in re.finditer(r"(?<![\wçğıöşü])" + k + r"\s*[:=]\s*([^.;:()\n]{5,90})", m):
        ad = temiz(esles.group(1))
        if ad:
            return ad
    return ""


YUKLEM = re.compile(
    r"\b(verilir|olur|olur|yapılır|gelişir|görülür|kullanılır|artar|azalır|sağlar|neden|olduğu|gerekir|başlar|"
    r"sürer|gelir|gider|bulunur|gösterir|oluşur|beklenir|yerleşir|azaltır|artırır|etkiler|uyarır|baskılar)\b",
    re.I,
)


def temiz(ad: str) -> str:
    """Açılımı toparlar: madde imini, cümle başını ve yüklemli parçaları atar."""
    ad = re.sub(r"^[^A-ZÇĞİÖŞÜ]+", "", ad.strip())
    ad = re.sub(r"\s+", " ", ad).strip(" ,;:-–")
    # son cümle parçasını al ("… verilir. Genetik olarak riyanodin reseptörü" → "Genetik olarak riyanodin reseptörü")
    ad = re.split(r"[.!?]\s+", ad)[-1].strip(" ,;:-–")
    kel = ad.split()
    if len(kel) > 5:  # açılım kısa bir ad tamlamasıdır, cümle değil
        return ""
    ad = " ".join(kel)
    if not ad or len(ad) > AC_ENCOK or ad[0].islower():
        return ""
    if YUKLEM.search(ad):
        return ""
    # en az iki sözcük ve bir tanesi 4+ harf olmalı (tek kelimelik gürültüyü at)
    if len(kel) < 2 or not any(len(x) >= 4 for x in kel):
        return ""
    return ad


# ── sözlükler ────────────────────────────────────────────────────────────────────────────────────────────────────
def bilinen() -> dict[str, str]:
    if BILINEN.is_file():
        return {str(k): str(v) for k, v in json.loads(BILINEN.read_text(encoding="utf-8")).items()}
    return {}


def elle(key: str) -> dict[str, str]:
    p = ELLE_KOK / f"{key}.json"
    if p.is_file():
        return {str(k): str(v) for k, v in json.loads(p.read_text(encoding="utf-8")).items()}
    return {}


def kutular(s: T.Sayfa, t: str) -> list[list[float]]:
    """Kısaltmanın slayttaki kutuları. "DSM-5", "MAO-A", "5-HTTLPR", "o5-HTT" gibi bitişik yazımlarda kısaltma
    kısmı işaretlenir (terim kapısındaki kutu kuralı yalnız tam kelimeyi bulur)."""
    b = s.bul(t)
    if b:
        return b
    p = T.fold(t)
    out: list[list[float]] = []
    for w, bx, _ in s.kel:
        if p not in w:
            continue
        m = re.search(re.escape(p), w)
        if not m:
            continue
        on, son = w[:m.start()], w[m.end():]
        if not re.fullmatch(r"(?:o?[\wçğıöşü]{0,8}[-–])?", on) or not re.fullmatch(r"(?:[-–/][\wçğıöşü]{1,12}){0,2}", son):
            continue
        n = max(1, len(w))
        out.append([
            round(bx[0] + (bx[2] - bx[0]) * m.start() / n, 4), round(bx[1], 4),
            round(bx[0] + (bx[2] - bx[0]) * m.end() / n, 4), round(bx[3], 4),
        ])
        if len(out) >= 3:
            break
    return out


# ── kapı ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def denetle(key: str, yazar: dict, sy: dict[str, T.Sayfa]) -> tuple[list[str], dict]:
    try:
        from turkce_uslup import denetle as uslup
    except Exception:  # noqa: BLE001
        uslup = lambda m, y: []  # noqa: E731
    hata: list[str] = []
    cikti: dict = {}
    for yer, liste in (yazar.get("s") or {}).items():
        if yer not in sy:
            hata.append(f"{yer}: slayt yok"); continue
        if len(liste) > EN_COK:
            hata.append(f"{yer}: sayfa başına en çok {EN_COK} kısaltma ({len(liste)})")
        gorulen: set[str] = set()
        for x in liste:
            t = str(x.get("t") or "").strip()
            a = str(x.get("a") or "").strip()
            ac = str(x.get("acilim") or "").strip()
            k = str(x.get("k") or "kisaltma")
            if not kisaltma_mi(t):
                hata.append(f"{yer}: '{t}' kısaltma biçiminde değil (büyük harf, 2–8 karakter)")
            if t in gorulen:
                hata.append(f"{yer}: '{t}' aynı slaytta iki kez")
            gorulen.add(t)
            if t and t not in metin(sy[yer]):
                hata.append(f"{yer}: '{t}' bu slaytın metninde geçmiyor")
            if k != "kisaltma":
                hata.append(f"{yer}: tür 'kisaltma' olmalı")
            if not ac:
                hata.append(f"{yer}: açılım (acilim) zorunlu")
            elif len(ac) < 3 or len(ac) > AC_ENCOK:
                hata.append(f"{yer}: açılım {len(ac)} karakter (3–{AC_ENCOK})")
            # a: açıklama isteğe bağlı; yoksa açılımın kendisi yazılır (ön yüz tekrarı gizler)
            if a and a != ac:
                if not (A_ENAZ <= len(a) <= A_ENCOK):
                    hata.append(f"{yer}: açıklama {len(a)} karakter ({A_ENAZ}–{A_ENCOK})")
                if "…" in a or "..." in a or not a.endswith((".", "!", "?")):
                    hata.append(f"{yer}: açıklama tam cümleyle bitmeli (kesme yok)")
                if len(re.findall(r"[.!?](?=\s+[A-ZÇĞİÖŞÜ]|\s*$)", a)) > 2:
                    hata.append(f"{yer}: açıklama en çok 2 cümle")
                hata.extend(uslup(a, yer))
            b = kutular(sy[yer], t) if t else []
            if t and not b:
                hata.append(f"{yer}: '{t}' için kutular bulunamadı"); continue
            d, s = yer.split(":")
            sayfa = cikti.setdefault(d, {}).setdefault(s, {"bos": sy[yer].bos, "t": []})
            sayfa["t"].append({"t": t, "acilim": ac, "a": a, "k": "kisaltma", "b": b})
    return hata, {"surum": SURUM, "key": key, "uretici": "deepseek", "d": cikti}


def yaz(key: str, cikti: dict) -> Path:
    hedef = kok_kis(key) / f"{key}.json"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    tmp = hedef.with_suffix(".tmp")
    tmp.write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, hedef)
    return hedef


# ── komutlar ─────────────────────────────────────────────────────────────────────────────────────────────────────
def k_adaylar(key: str) -> int:
    sy = T.sayfalar(T.ders(key))
    if not sy:
        print(f"{key}: PDF yok"); return 2
    hepsi: dict[str, list[str]] = {}
    for yer in sorted(sy, key=lambda x: [int(v) for v in x.split(":")]):
        ad = adaylar(sy[yer])
        if not ad:
            continue
        print(f"\n## {yer}")
        for k in ad:
            ac = acilim_bul(sy[yer], k)
            hepsi.setdefault(k, []).append(yer)
            print(f"- {k}{(' → ' + ac) if ac else ''}")
    print(f"\n{key}: {len(hepsi)} ayrı kısaltma adayı · {len(sy)} sayfa")
    print("  " + ", ".join(sorted(hepsi)))
    return 0


def k_otomatik(key: str, yazilsin: bool, metinden: bool = False) -> int:
    sy = T.sayfalar(T.ders(key))
    if not sy:
        print(f"{key}: PDF yok"); return 2
    bl, el = bilinen(), elle(key)
    yazar: dict = {"s": {}}
    for yer in sy:
        for k in adaylar(sy[yer]):
            ac = el.get(k) or bl.get(k) or (acilim_bul(sy[yer], k) if metinden else "")
            if not ac:
                continue
            yazar["s"].setdefault(yer, []).append({"t": k, "acilim": ac, "a": ac, "k": "kisaltma"})
    hata, cikti = denetle(key, yazar, sy)
    for h in hata:
        print("HATA", h)
    print(f"{key}: {sum(len(v) for v in cikti['d'].values() for v in v.values()) if cikti['d'] else 0} kısaltma · {len(hata)} HATA")
    if yazilsin and not hata:
        print("yazıldı:", yaz(key, cikti))
    return 0 if not hata else 1


def k_dogrula(key: str, dosya: Path, yazilsin: bool) -> int:
    dosya = Path(dosya)
    yazar = json.loads(dosya.read_text(encoding="utf-8"))
    hata, cikti = denetle(key, yazar, T.sayfalar(T.ders(key)))
    for h in hata:
        print("HATA", h)
    toplam = sum(len(v["t"]) for d in cikti["d"].values() for v in d.values())
    print(f"{key}: {toplam} kısaltma · {len(hata)} HATA")
    if yazilsin and not hata:
        print("yazıldı:", yaz(key, cikti))
    return 0 if not hata else 1


def k_sozluk_disa() -> int:
    """Bütün kısaltma dosyalarını Terimler sayfası sözlüğüne aktarır (ayrı 'kisaltma' kategorisi)."""
    kayit: dict[str, dict] = {}
    for kok in (KOK_KIS, ARSIV_KIS):
        for p in sorted(kok.glob("*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            for say in (d.get("d") or {}).values():
                for v in say.values():
                    for x in v.get("t") or []:
                        t, a = x["t"], x["a"]
                        k = kayit.setdefault(t, {"term": t, "definition": a, "category": "kisaltma", "decks": []})
                        if d.get("key") and d["key"] not in k["decks"]:
                            k["decks"].append(d["key"])
                        if a != k["definition"]:
                            k.setdefault("baska", [])
                            if a not in k["baska"]:
                                k["baska"].append(a)
    for k in kayit.values():
        k["decks"] = sorted(k["decks"])
        if k.get("baska"):
            k["definition"] = k["definition"]  # ilk yazım esas; farklı derslerdeki anlamlar `baska`da saklanır
    hedef = MEDS / "src" / "data" / "kisaltma_sozluk.json"
    hedef.write_text(json.dumps(kayit, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(kayit)} kısaltma → {hedef}")
    return 0


def k_tarama(desen: str, yazilsin: bool) -> int:
    """Bütün dersleri tarar: açılımı bulunan (yazılabilir) ve bulunmayan kısaltmaları listeler."""
    from collections import Counter
    bl, hepsi = bilinen(), {"yazilabilir": 0, "acilimsiz": 0, "ders": 0, "kisaltma": 0}
    anahtarlar = []
    for kok in (T.KOK, T.ARSIV_KOK):
        for p in sorted((kok / "terim").glob("*.json")):
            k = json.loads(p.read_text(encoding="utf-8")).get("key") or p.stem
            if desen == "hepsi" or k.startswith(desen) or f"-{desen}" in k:
                anahtarlar.append(k)
    for key in anahtarlar:
        try:
            sy = T.sayfalar(T.ders(key))
        except Exception as e:  # noqa: BLE001
            print(f"## {key}: ders alınamadı ({e})"); continue
        if not sy:
            print(f"## {key}: PDF yok"); continue
        el = elle(key)
        sayim: Counter = Counter()
        for s in sy.values():
            for k in adaylar(s):
                sayim[k] += 1
        bulunan: dict[str, str] = {}
        yok: dict[str, set] = {}
        for yer in sy:
            for k in adaylar(sy[yer]):
                if k in bulunan or any(k in v for v in yok.values()):
                    continue
                ac = el.get(k) or bl.get(k) or (acilim_bul(sy[yer], k) if metinden else "")
                if ac:
                    bulunan[k] = ac
                elif sayim[k] >= 2:  # tek geçen aday gürültüdür
                    yok.setdefault(yer, set()).add(k)
        hepsi["ders"] += 1
        hepsi["kisaltma"] += len(bulunan) + sum(len(v) for v in yok.values())
        hepsi["yazilabilir"] += len(bulunan)
        hepsi["acilimsiz"] += sum(len(v) for v in yok.values())
        print(f"\n## {key} — {len(sy)} sayfa")
        if bulunan:
            print("  YAZILABILIR " + " | ".join(f"{k} → {v}" for k, v in bulunan.items()))
        if yok:
            print("  AÇILIM YOK  " + " | ".join(f"{y}:{','.join(sorted(v))}" for y, v in sorted(yok.items())))
    print(f"\nTOPLAM {hepsi['ders']} ders · {hepsi['kisaltma']} kısaltma · yazılabilir {hepsi['yazilabilir']} · açılımsız {hepsi['acilimsiz']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Slayt kısaltma sözlüğü")
    alt = ap.add_subparsers(dest="komut", required=True)
    a1 = alt.add_parser("adaylar"); a1.add_argument("key")
    a2 = alt.add_parser("otomatik"); a2.add_argument("key"); a2.add_argument("--yaz", action="store_true")
    a2.add_argument("--metinden", action="store_true", help="slaytın kendi metninden çıkarılan açılımı da kullan (denetlenmeli)")
    a3 = alt.add_parser("dogrula"); a3.add_argument("key"); a3.add_argument("dosya", type=Path); a3.add_argument("--yaz", action="store_true")
    a4 = alt.add_parser("tarama"); a4.add_argument("desen", nargs="?", default="hepsi"); a4.add_argument("--yaz", action="store_true")
    alt.add_parser("sozluk_disa")
    a = ap.parse_args()
    if a.komut == "adaylar":
        return k_adaylar(a.key)
    if a.komut == "otomatik":
        return k_otomatik(a.key, a.yaz, a.metinden)
    if a.komut == "dogrula":
        return k_dogrula(a.key, a.dosya, a.yaz)
    if a.komut == "tarama":
        return k_tarama(a.desen, a.yaz)
    return k_sozluk_disa()


if __name__ == "__main__":
    sys.exit(main())
