#!/usr/bin/env python3
"""Ses metni — EMA'ya giden OKUNUŞ metninin TEK girişi (2026-11-16).

Önceden okunuş 9 ayrı yerde, her betiğin kendi sırasıyla kuruluyordu; yol (Kurul 1 bitişik / Kurul 2 uzun kısaltma / modül
yazımı) elle anahtar listesinden (`modul_okunus.MODUL_ANAHTARLAR`) seçildiği için her yeni partide unutuluyordu (H469, H538)
ve çözücü/asistan/ek modül yolları terim okunuşunu (Wernicke → Vernike, H128) hiç almıyordu.

Tek sıra (`hazirla`):
  uzun yol (Kurul 2+, çözücü/asistan, modül yazımı):
     1. terim okunuşu      terim_okunus.donustur        (yabancı terim; kısaltmalara dokunmaz)
     2. yazımla kısaltma   modul_okunus.donustur        (NMDA, BRCA1, IL-6 → "en mee dee aa", "bercea bir"…)
     3. fonetik + sayı     okunus.FONETIK_TTS           (özel adlar, Latince adlar, SAYI_TTS rakam okunuşu)
     4. okunuşla kısaltma  kisaltma_ses.uzat            ("de ne a" → "dee nee aa", H3)
  bitişik yol (Kurul 1 — toplu yeniden üretim yok, H3):
     1. terim okunuşu → 2. okunus.duzelt (fonetik + sayı + bitişik hece dizisi)
Yol VERİDEN seçilir: ders anahtarı → ders kayıt defteri (src/data/dersler/k*.json) → kurul; veri klasörü (k2patoloji_cozucu)
→ kurul öneki, öneksiz klasör → branş sözlüğünde (branslar.json) ise Kurul 1; ek modül → ek_moduller/index.json `kurul`.
`MODUL_ANAHTARLAR` yalnız geriye uyum: Kurul 1'de yazımla yazılmış dersler (k1-70 TBG kampı, k1-59 V2) uzun yola alınır.
Kurul bulunamazsa sessizce eski yola düşülmez: uzun yol + `scripts/gunluk.py` uyarısı.

Sözlükler KOPYALANMAZ: okunus.py, terim_okunus.json, modul_okunus.py, kisaltma_ses.py veri olarak içe aktarılır.
`SOZLUK_SURUM`: bu sözlük/kural dosyalarının içerik karması — yeni klip kaydına `okunus_surum` olarak yazılır (klip karmasına
ve dosya adına KATILMAZ; mevcut klipler yeniden üretilmez).

Kullanım:  ses_metin.py "metin" [--ders k2-09] [--modul k2patoloji_cozucu] [--kurul 2]
           from ses_metin import hazirla, SOZLUK_SURUM
"""
from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import functools  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import sys  # noqa: E402

MEDS = _kok.MEDS
_SA = _kok.SCRIPTS / "uretim" / "sesli_anlatim"
_PC = _kok.SCRIPTS / "uretim" / "patoloji_cozucu"
for _y in (_SA, _PC, _kok.SCRIPTS):
    if str(_y) not in sys.path:
        sys.path.append(str(_y))

import gunluk  # noqa: E402
import kisaltma_ses  # noqa: E402
import modul_okunus  # noqa: E402
import okunus  # noqa: E402
import terim_okunus  # noqa: E402

DERS_DEFTERI = MEDS / "src/data/dersler"
EK_MODUL_DIZIN = MEDS / "src/data/ek_moduller/index.json"

# Okunuşu belirleyen dosyalar (veri + kural kodu): içerik karması → SOZLUK_SURUM
SOZLUK_DOSYALARI = [
    okunus.SOZLUK,                      # data/sesli_anlatim/okunus/kisaltmalar.json (hece dizisi kümesi)
    terim_okunus.SOZLUK,                # data/sesli_anlatim/okunus/terim_okunus.json
    _SA / "okunus.py",                  # FONETIK_TTS, SAYI_TTS, HARF
    _SA / "terim_okunus.py",            # Latince kuralı
    _SA / "modul_okunus.py",            # KELIME, UZUN
    _PC / "kisaltma_ses.py",            # uzat
    _Path(__file__).resolve(),          # bu dosyanın sırası
]


def _sozluk_surumu() -> str:
    h = hashlib.sha1()
    for f in SOZLUK_DOSYALARI:
        h.update(f.name.encode())
        h.update(f.read_bytes() if f.exists() else b"<yok>")
    return h.hexdigest()[:12]


SOZLUK_SURUM = _sozluk_surumu()


# ---------------------------------------------------------------- yol seçimi (veriden)

@functools.lru_cache(maxsize=1)
def _ders_kurullari() -> dict[str, int]:
    """Ders kimliği (k2-09) → kurul, ders kayıt defterinden."""
    out: dict[str, int] = {}
    for f in sorted(DERS_DEFTERI.glob("k*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # bozuk defter: uyar, devam
            gunluk.olay("ses_metin", "uyari", "ders defteri okunamadı", dosya=f.name, hata=str(e))
            continue
        for ders in d.get("dersler") or []:
            if ders.get("id"):
                out[ders["id"]] = int(ders.get("kurul") or d.get("kurul"))
    return out


@functools.lru_cache(maxsize=1)
def _brans_sluglari() -> set[str]:
    try:
        d = json.loads((DERS_DEFTERI / "branslar.json").read_text(encoding="utf-8"))
        return {b["slug"] for b in d.get("branslar") or [] if b.get("slug")}
    except Exception:
        return set()


@functools.lru_cache(maxsize=1)
def _ek_modul_kurullari() -> dict[str, int]:
    try:
        return {m["id"]: int(m["kurul"]) for m in json.loads(EK_MODUL_DIZIN.read_text(encoding="utf-8"))["moduller"] if m.get("kurul")}
    except Exception:
        return {}


_DERS_ID = re.compile(r"k\d+-\d+")
_KAMP = re.compile(r"^k(\d+)-kamp$")


def ders_kurulu(ders: str) -> int | None:
    """Ders/deste anahtarı → kurul. 'k1p-k1-11-…', 'k2-09-sss-ilaclari', 'k2-07-ag-xyz' hepsi defterdeki kimlikten."""
    defter = _ders_kurullari()
    for m in _DERS_ID.finditer(ders or ""):
        if m.group(0) in defter:
            return defter[m.group(0)]
    if (m := _KAMP.match(ders or "")):
        return int(m.group(1))
    return None


def modul_kurulu(modul: str) -> int | None:
    """Veri klasörü/modül adı → kurul: 'k2patoloji_cozucu' → 2; 'patoloji_asistan' (öneksiz branş) → 1; ek modül → index."""
    ad = (modul or "").strip("/").split("/")[-1]
    if ad in _ek_modul_kurullari():
        return _ek_modul_kurullari()[ad]
    kok = re.sub(r"_(cozucu(_alt)?|asistan)$", "", ad)
    if (m := re.match(r"^k(\d)(?=[a-z])", kok)):
        return int(m.group(1))
    if kok in _brans_sluglari():
        return 1  # branslar.json: Kurul 2+ klasörü k<kurul><slug>; öneksiz slug Kurul 1 klasörüdür
    return None


_UYARILDI: set[tuple] = set()


def yol_sec(*, kurul: int | None = None, ders: str | None = None, modul: str | None = None) -> str:
    """'uzun' ya da 'bitisik'. Bilinmeyende uzun yol + günlük uyarısı (sessiz düşüş YOK)."""
    if ders and modul_okunus.modul_mu(ders):  # geriye uyum eşlemesi (Kurul 1 yazımlı dersler, Son Prova, dış ajan)
        return "uzun"
    k = kurul
    if k is None and ders:
        k = ders_kurulu(ders)
    if k is None and modul:
        k = modul_kurulu(modul)
    if k is None:
        anahtar = (ders, modul)
        if anahtar not in _UYARILDI:
            _UYARILDI.add(anahtar)
            gunluk.olay("ses_metin", "uyari", "kurul bulunamadı; uzun kısaltma yolu kullanıldı", ders=ders, modul=modul)
        return "uzun"
    return "uzun" if k >= 2 else "bitisik"


# ---------------------------------------------------------------- dönüşüm

# modul_okunus tek büyük harfi harf adıyla okur (X, Y kromozomu, vitamin B). Türkçe zamir "O" ve şık etiketi ("A, …") bundan korunur.
_KORU = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])(?:O(?=\s+[a-zçğıöşü])|[A-E](?=,\s))")


def _yazim_kisaltma(metin: str) -> str:
    korunan: list[str] = []

    def sakla(m):
        korunan.append(m.group(0))
        return f"\x00{len(korunan) - 1}\x00"
    metin = modul_okunus.donustur(_KORU.sub(sakla, metin))
    return re.sub(r"\x00(\d+)\x00", lambda m: korunan[int(m.group(1))], metin)


def _terim(metin: str) -> str:
    # küçük harfli Türkçe sözcüğe eponim okunuşu verilmez ("engel" → "Engıl" değil; terim_okunus.json "engel": "Engıl")
    return terim_okunus.donustur(metin, kucuk_ozel_ad=False)


def uzun_yol(metin: str, ek_kisaltma: set[str] | None = None) -> str:
    metin = _terim(metin)
    metin = _yazim_kisaltma(metin)
    for pat, fon in okunus.FONETIK_TTS:
        metin = pat.sub(fon, metin)
    return kisaltma_ses.uzat(metin, ek_kisaltma)


def bitisik_yol(metin: str) -> str:
    return okunus.duzelt(_terim(metin))


def hazirla(metin: str, *, kurul: int | None = None, ders: str | None = None, modul: str | None = None,
            yol: str | None = None, ek_kisaltma: set[str] | None = None) -> str:
    """Ekran/konuşma metni → EMA'ya giden okunuş metni. `yol` verilirse ('uzun'/'bitisik') seçim atlanır
    (ör. çözücü klipleri tasarım gereği daima uzun: SURUM ema-2)."""
    y = yol or yol_sec(kurul=kurul, ders=ders, modul=modul)
    return uzun_yol(metin, ek_kisaltma) if y == "uzun" else bitisik_yol(metin)


def okuyucu(**kw):
    """hazirla'nın kısmi uygulanmışı: ses_klip.seslendir(okunus=…) için."""
    y = kw.pop("yol", None) or yol_sec(**{k: kw.get(k) for k in ("kurul", "ders", "modul")})
    return lambda m: hazirla(m, yol=y)


# ---------------------------------------------------------------- eski yollar (eşdeğerlik ve fark raporu için; üretimde kullanılmaz)

def eski_ders_okunus(metin: str, anahtar: str) -> str:
    """ema_isci.tts_metni'nin 2026-11-16 öncesi davranışı (anahtar listesi + k[2-6] düzenli ifadesi)."""
    modul = modul_okunus.modul_mu(str(anahtar or ""))
    uzun = bool(re.match(r"k[2-6](p-k[2-6])?-", str(anahtar or "")))
    if modul or uzun:
        metin = terim_okunus.donustur(metin)
    if modul:
        return modul_okunus.donustur(metin)
    if uzun:
        for pat, fon in okunus.FONETIK_TTS:
            metin = pat.sub(fon, metin)
        return kisaltma_ses.uzat(metin)
    return okunus.duzelt(metin)


if __name__ == "__main__":
    a = sys.argv[1:]
    kw = {}
    for ad in ("ders", "modul", "kurul", "yol"):
        if f"--{ad}" in a:
            i = a.index(f"--{ad}")
            kw[ad] = int(a[i + 1]) if ad == "kurul" else a[i + 1]
            del a[i:i + 2]
    print(f"[sözlük {SOZLUK_SURUM} · yol {kw.get('yol') or yol_sec(**{k: v for k, v in kw.items() if k != 'yol'})}]")
    print(hazirla(" ".join(a), **kw))
