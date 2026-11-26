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


@functools.lru_cache(maxsize=1)
def _deste_kurullari() -> dict[str, int]:
    """Öğren deste kimliği (learn-…, deck-…) → kurul; deste kaydının `committee` alanından ("Kurul 1 - Ürogenital…").
    Desteler yalnız scripts/deste_deposu.py API'siyle okunur; süreç başına bir kez kurulur (H586 güncellemesi)."""
    try:
        import deste_deposu
        out = {}
        for d in deste_deposu.hepsi():
            m = re.search(r"Kurul\s*(\d+)", str(d.get("committee") or d.get("category") or ""))
            if m:
                for k in {d.get("id"), d.get("deckId")} - {None}:
                    out[k] = int(m.group(1))
        return out
    except Exception as e:  # deste deposu okunamadı: uyar, kural tablosuyla devam
        gunluk.olay("ses_metin", "uyari", "deste deposu okunamadı", hata=str(e))
        return {}


_DERS_ID = re.compile(r"k\d+-\d+")
_KAMP = re.compile(r"^k(\d+)-kamp$")
# Kural tablosu (defterde olmayan anahtar): ders kimliği biçimi kurulu kendisi taşır.
#   k1-67-gebelik…  (defter k1-66'da bitiyor; kamp/ek dersler)   → 1
#   k2p-k2-01-…, k1p-k1-11-… (sanal desteler)                     → önekteki kurul
#   y25-k2-09-… (2025-26 arşiv anahtarları)                        → 2
_KURUL_BICIMI = re.compile(r"(?:^|[-_])k(\d)p?-(?:k\d-)?\d")


def ders_kurulu(ders: str) -> int | None:
    """Ders/deste anahtarı → kurul. Sıra: ders kayıt defteri (kimlik) → Öğren deste kaydı (committee) → kimlik biçimi."""
    ders = ders or ""
    defter = _ders_kurullari()
    for m in _DERS_ID.finditer(ders):
        if m.group(0) in defter:
            return defter[m.group(0)]
    if (m := _KAMP.match(ders)):
        return int(m.group(1))
    if ders in _deste_kurullari():
        return _deste_kurullari()[ders]
    if (m := _KURUL_BICIMI.search(ders)):
        return int(m.group(1))
    return None


# Branş sözlüğünde olmayan öneksiz Kurul 1 klasörleri (kmb: Dönem 3 beceri, Kurul 1 döneminde yazıldı; ortak: çözücü ortak klipleri)
_KURUL1_KLASOR = {"kmb"}


def modul_kurulu(modul: str) -> int | None:
    """Veri klasörü/modül adı → kurul: 'k2patoloji_cozucu' → 2; 'patoloji_asistan' (öneksiz branş) → 1; ek modül → index."""
    ad = (modul or "").strip("/").split("/")[-1]
    if ad in _ek_modul_kurullari():
        return _ek_modul_kurullari()[ad]
    kok = re.sub(r"_(cozucu(_alt)?|asistan)$", "", ad)
    if (m := re.match(r"^k(\d)(?=[a-z])", kok)):
        return int(m.group(1))
    if kok in _brans_sluglari() or kok in _KURUL1_KLASOR:
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

# modul_okunus tek büyük harfi harf adıyla okur (X, Y kromozomu, vitamin B). Türkçe zamir "O" ve şık etiketi ("A, …",
# "B) …", satır başı "C. …" / "D: …") bundan korunur.
_KORU = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])(?:O(?=\s+[a-zçğıöşü])|[A-E](?=,\s|\)\s)|(?<![^\s(\[])[A-E](?=[.:]\s+[A-ZÇĞİÖŞÜ]))")
# Türkçe ek kısaltmaya kesme ile bağlıysa (LGV'de, HIV'in) ek kısaltma okunuşundan ve kisaltma_ses.uzat'tan korunur:
# yoksa "lee gee vee de de görülür" → uzat "de de"yi DD sanıp "dee dee" okur (H586 güncellemesi).
_KESME_EK = re.compile(r"(?<=[A-ZÇĞİÖŞÜ0-9])['’]([a-zçğıöşü]+)")
# Yan yana yalnız bağlaç/ek hecelerinden oluşan dizi ("de de", "da ne") kısaltma hecesi sayılmaz; arkasından 1–2 harfli
# hece geliyorsa ("de ne a") gerçek hece dizisidir, korunmaz.
_BAGLAC_DIZI = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])(?:(?:de|da|te|ta|ne|ve)\s+)+(?:de|da|te|ta|ne|ve)(?![\wÇĞİÖŞÜçğıöşü])(?!\s+[a-zçğıöşü]{1,2}(?![\wçğıöşü]))")
# Tek başına "I", metinde başka Roma rakamı varsa Roma biridir ("I ve III" → "bir ve üç"; harf adı "ıı" değil).
_ROMA_VAR = re.compile(r"(?<![\wÇĞİÖŞÜ])(?:II|III|IV|VI|VII|VIII|IX)(?![\wÇĞİÖŞÜçğıöşü])")
_TEK_I = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü'’-])I(?![\wÇĞİÖŞÜçğıöşü'’-])")
_BUYUK_SOZ = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])[A-ZÇĞİÖŞÜ]{2,}(?![\wÇĞİÖŞÜçğıöşü])")
_TR_OZEL = set("ÇĞİÖŞÜ")


@functools.lru_cache(maxsize=1)
def _bilinen_kisaltma() -> frozenset[str]:
    """Harf harf ya da sözlükteki okunuşuyla okunacak büyük harfli kısaltmalar: modul_okunus.KELIME + okunus kümesi
    (Türkçeye özgü harf içermeyenler)."""
    # okunus kümesi derlemden toplanmış büyük harfli dizileri de içerir (TÜMÖR, BEBEK, ETKILERI): yalnız ≤4 harfli ve
    # Türkçeye özgü harfsiz olanlar kısaltma sayılır (HIV, DNA, NMDA); uzun kısaltmalar KELIME'de tutulur.
    k = {w.upper() for w in modul_okunus.KELIME} | {w.upper() for w in okunus.kume()
                                                    if len(w) <= 4 and not (_TR_OZEL & set(w.upper()))}
    return frozenset(k)


def _tr_kucuk(s: str) -> str:
    return s.replace("I", "ı").replace("İ", "i").lower()


# (b) ek: Türkçe çekim/ek-fiil sonu taşıyan ≥6 harfli tek büyük sözcük ("SIFIRDIR", "YAPMAZLAR") kısaltma değildir (2026-11-17)
_TR_EK_SON = re.compile(r"^[A-ZÇĞİÖŞÜ]{3,}(?:D[IİUÜ]R|T[IİUÜ]R|LAR|LER|MAZ|MEZ|D[IİUÜ]K)$")


def _baslik_kucult(metin: str) -> str:
    """TAMAMI BÜYÜK Türkçe başlık/etiket ("[SINAV SPOTU]", "TOPUK KANI İLE YAPILAN TESTLER") harf harf okunmaz.
    Kural: (a) ≥2 ardışık büyük harfli sözcükten en az biri ≥4 harf ve bilinen kısaltma değilse, dizideki bilinmeyen
    sözcükler küçültülür; (b) tek sözcük ≥4 harf, Türkçeye özgü harf (ÇĞİÖŞÜ) içeriyor ve bilinmiyorsa küçültülür.
    Bilinen kısaltma (modul_okunus.KELIME, okunus kümesi: HIV, DNA, ELISA…) olduğu gibi kalır."""
    B = _bilinen_kisaltma()
    es = list(_BUYUK_SOZ.finditer(metin))
    kucult: set[int] = set()
    i = 0
    while i < len(es):
        j = i
        while j + 1 < len(es) and re.fullmatch(r"[\s\-/&,]*", metin[es[j].end():es[j + 1].start()]) is not None \
                and metin[es[j].end():es[j + 1].start()].strip(" ") in ("", "-", "/", "&"):
            j += 1
        dizi = es[i:j + 1]
        if len(dizi) >= 2 and any(len(m.group(0)) >= 4 and m.group(0) not in B for m in dizi):
            kucult |= {k for k in range(i, j + 1) if es[k].group(0) not in B}
        elif len(dizi) == 1:
            w = dizi[0].group(0)
            if len(w) >= 4 and w not in B and (_TR_OZEL & set(w) or _TR_EK_SON.search(w)):
                kucult.add(i)
        i = j + 1
    if not kucult:
        return metin
    out, son = [], 0
    for k in sorted(kucult):
        out.append(metin[son:es[k].start()] + _tr_kucuk(es[k].group(0)))
        son = es[k].end()
    out.append(metin[son:])
    return "".join(out)


def _sakla(metin: str, rx: re.Pattern, korunan: list[str], grup: int = 0, on: str = "") -> str:
    def f(m):
        korunan.append(m.group(grup))
        return on + _yer(len(korunan) - 1)
    return rx.sub(f, metin)


# Yer tutucu: Özel Kullanım Alanı karakteri (U+E000+n). Rakam/harf içermez → sayı okunuşu (FONETIK_TTS), modul_okunus ve
# kisaltma_ses.uzat ona dokunmaz; \w de değildir (sözcük sınırını bozmaz).
_YER0 = 0xE000


def _yer(n: int) -> str:
    return chr(_YER0 + n)


def _geri(metin: str, korunan: list[str]) -> str:
    for _ in range(3):
        yeni = re.sub("[\uE000-\uF8FF]", lambda m: korunan[i] if (i := ord(m.group(0)) - _YER0) < len(korunan) else m.group(0), metin)
        if yeni == metin:
            break
        metin = yeni
    return metin


def _yazim_kisaltma(metin: str, korunan: list[str]) -> str:
    """Yer tutucular (_yer) uzun_yol sonunda geri konur: kisaltma_ses.uzat da korunan parçaya dokunmaz."""
    if _ROMA_VAR.search(metin):
        metin = _TEK_I.sub("bir", metin)
    metin = _sakla(metin, _KORU, korunan)
    metin = _sakla(metin, _KESME_EK, korunan, grup=1, on=" ")
    return modul_okunus.donustur(metin)


# Terim sözlüğü/kural motorunun ses_metin katmanında düzeltilen okunuşları (sözlük dosyası eski yolları da beslediği için
# orada değiştirilmez: eski yolun çıktısı = sesli ders klip özeti; değişirse 1.000+ paragraf yeniden üretilirdi).
#   - küçük harfli sıradan Türkçe sözcük: sözlükte yabancı okunuşu olsa da dokunulmaz (sperm → "spörm" değil)
#   - kural motorunun yanlış çevirdiği yabancı sözcük: doğru okunuş (checkpoint → "kekpoint" değil)
TR_SIRADAN = {"sperm", "engel", "dede", "dedem", "dedemiz", "dedesi", "gram", "test", "film", "bant", "form", "plan", "program"}
EK_OKUNUS = {"checkpoint": "çekpoint", "down": "davn", "walker": "volkır"}
# küçük harfli sözcük; tırnak içi ('sperm seleksiyonu') dahil, kesmeli ek (HIV'in) hariç
_KUCUK_SOZ = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü-])(?<![\wÇĞİÖŞÜçğıöşü]['’])([a-zçğıöşü]+)(?![\wÇĞİÖŞÜçğıöşü-])")
_EK_OKUNUS_RX = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])(" + "|".join(map(re.escape, EK_OKUNUS)) + r")(?=[a-zçğıöşü'’]*(?![\w]))",
                           re.IGNORECASE)
_IN = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])In(?=\s+(?:vivo|vitro|situ|utero)\b)")
# kutu çizim (┌─│), blok (▀█), oklar (→↓) ve geometrik şekiller (▼◄►■): tablo/akış çizimi motoru şaşırtır (H587; 2026-11-17:
# yalnız U+2500–259F temizleniyordu, ▼◄► motor metninde kalıp tumor-biyolojisi 18. adımı üç tohumda da bozdu)
_KUTU = re.compile(r"[\u2190-\u21FF\u2500-\u257F\u2580-\u259F\u25A0-\u25FF\u27F5-\u27FF]+")


def _sakla_bir(okunus_: str, orj: str, korunan: list[str]) -> str:
    korunan.append(okunus_[:1].upper() + okunus_[1:] if orj[:1].isupper() else okunus_)
    return _yer(len(korunan) - 1)


def _terim(metin: str) -> str:
    # küçük harfli Türkçe sözcüğe eponim okunuşu verilmez ("engel" → "Engıl" değil; terim_okunus.json "engel": "Engıl")
    korunan: list[str] = []

    def f(m):
        w = m.group(1)
        if w in TR_SIRADAN:
            korunan.append(w)
            return _yer(len(korunan) - 1)
        return w
    metin = _EK_OKUNUS_RX.sub(lambda m: _sakla_bir(EK_OKUNUS[m.group(1).lower().replace("ı", "i").replace("i̇", "i")], m.group(1), korunan), metin)
    metin = _KUCUK_SOZ.sub(f, metin)
    metin = terim_okunus.donustur(metin, kucuk_ozel_ad=False)
    return _IN.sub("İn", _geri(metin, korunan))  # sözlük "in vivo" → büyük harfte Türkçe İ korunur


def _kutu_temizle(metin: str) -> str:
    if not _KUTU.search(metin):
        return metin
    m = re.sub(r"\s+", " ", re.sub(r"(?:\s*" + _KUTU.pattern + r"\s*)+", ", ", metin))
    m = re.sub(r"(?:\s*,\s*){2,}", ", ", m)            # ardışık çizim parçalarından kalan ", , ,"
    m = re.sub(r"\(\s*,\s*", "(", re.sub(r"\s*,\s*([.!?;:)])", r"\1", m))
    return m.strip(" ,")


# Satır yapılı kutu tablo/çizim → okunur düz metin (2026-11-17, tumor-biyolojisi 18/24/32). _kutu_temizle tek satıra
# yassılmış metinde çalışır: o noktada tablo hücreleri satır satır iç içe geçmiştir ("Derinin Bazal │ Derinin en sık…│
# Hücreli Karsinomu│ eritir…") ve yalnız çerçeveden oluşan satır ayrı "cümle" olarak motora gider (okunuş ".", süre 0).
# Bu işlev SATIRLAR DURURKEN çağrılır (Öğren: temizle_markdown'dan önce): yatay çizgi satırları grupları ayırır, her
# grupta tüm satırlarda boş/çerçeve olan dikey koridorlar sütunları verir; sütun parçaları yukarıdan aşağı birleşir,
# hücreler ", " ile, gruplar ". " ile ayrılır; yalnız çerçeveden oluşan satır parça üretmez. İçerik atılmaz.
_KUTU_KAR = re.compile(r"[←-⇿─-╿▀-▟■-◿⟵-⟿]")
_ICERIK = re.compile(r"[0-9A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû%]")


def _grup_duz(satirlar: list[str]) -> str:
    gen = max(len(s) for s in satirlar)
    satirlar = [s.ljust(gen) for s in satirlar]
    bos = [all(s[x] == " " or _KUTU_KAR.match(s[x]) for s in satirlar) for x in range(gen)]
    cizgi = [any(_KUTU_KAR.match(s[x]) for s in satirlar) for x in range(gen)]
    # koridor: çerçeve karakteri taşıyan boş sütun ya da ≥3 boşluk genişliği
    kor = [False] * gen
    x = 0
    while x < gen:
        if not bos[x]:
            x += 1
            continue
        y = x
        while y < gen and bos[y]:
            y += 1
        if y - x >= 3 or any(cizgi[x:y]):
            for k in range(x, y):
                kor[k] = True
        x = y
    sutunlar, x = [], 0
    while x < gen:
        if kor[x]:
            x += 1
            continue
        y = x
        while y < gen and not kor[y]:
            y += 1
        sutunlar.append((x, y))
        x = y
    hucreler = []
    for a, b in sutunlar:
        parca = [_KUTU_KAR.sub(" ", s[a:b]).strip() for s in satirlar]
        h = re.sub(r"\s+", " ", " ".join(p for p in parca if p)).strip()
        if _ICERIK.search(h):
            hucreler.append(h.rstrip(" .,;"))
    return ", ".join(hucreler)


def kutu_tablo_duz(metin: str) -> str:
    """Çok satırlı metindeki kutu çizimli tablo/akış bloklarını okunur satırlara çevirir (bkz. yukarı). Kutu karakteri
    olmayan metin aynen döner. Blok: kutu karakterli satırlar + aralarındaki/ardındaki düz satırlar (``` çiti içi dahil)."""
    if not _KUTU_KAR.search(metin):
        return metin
    satirlar = metin.split("\n")
    out: list[str] = []
    i = 0
    while i < len(satirlar):
        if not _KUTU_KAR.search(satirlar[i]):
            out.append(satirlar[i])
            i += 1
            continue
        j = i  # blok sonu: kutu karakterli son satır + (çit içindeyse) çit kapanışına kadar
        cit = any(s.strip().startswith("```") for s in out[-2:]) if out else False
        son = i
        while j < len(satirlar) and not satirlar[j].strip().startswith("```"):
            if _KUTU_KAR.search(satirlar[j]):
                son = j
            elif not cit and not satirlar[j].strip():
                break
            j += 1
        blok = satirlar[i:(j if cit else son + 1)]
        gruplar, cur = [], []
        for s in blok:
            if not _ICERIK.search(s):  # yalnız çerçeve/ok satırı: grup sınırı (yatay çizgi) ya da hiç
                if "─" in s or "═" in s:
                    if cur:
                        gruplar.append(cur)
                    cur = []
                continue
            cur.append(s)
        if cur:
            gruplar.append(cur)
        cumle = [g for g in (_grup_duz(c) for c in gruplar) if g]
        if cumle:
            out.append(". ".join(cumle) + ".")
        i = j if cit else son + 1
    return "\n".join(out)


# Karşılaştırmalı yüzde (H587, 2026-11-17): "<%0.1'dir" motorda "< yüzde sıfır.1 dir" okunuyordu (simge okunmaz, noktalı
# ondalık sayı okuyucusunda yok). → "%0,1'den küçüktür" (sayı okuyucusu "yüzde sıfır virgül bir'den küçüktür" yapar).
_ABL = {"0": "dan", "1": "den", "2": "den", "3": "ten", "4": "ten", "5": "ten", "6": "dan", "7": "den", "8": "den", "9": "dan"}
_ABL_ONLUK = {"1": "dan", "2": "den", "3": "dan", "4": "tan", "5": "den", "6": "tan", "7": "ten", "8": "den", "9": "dan"}
_KARS = re.compile(r"([<>≤≥])\s*%\s*(\d+(?:[.,]\d+)?)(?:['’]([a-zçğıöşü]+))?")
# yüzdesiz karşılaştırma (2026-11-17): birim okunuşunun son ünlüsüne göre ayrılma eki; önü harf/ok olan "<" (p<0.05, <-) dokunulmaz
_BIRIM_ABL = {"mm": "den", "cm": "den", "µm": "den", "μm": "den", "ml": "den", "mL": "den", "mg": "dan", "kg": "dan", "g": "dan",
              "mmHg": "dan", "yaş": "tan", "yıl": "dan", "gün": "den", "hafta": "dan", "ay": "dan", "saat": "ten", "dk": "dan"}
_KARS_SAYI = re.compile(r"(?<![\w<>=\-])([<>≤≥])\s*(\d+(?:[.,]\d+)?)(?:\s*(" + "|".join(sorted(map(re.escape, _BIRIM_ABL), key=len, reverse=True))
                        + r")(?![\wçğıöşü]))?(?![\d%.,])(?:['’]([a-zçğıöşü]+))?")
_YUZDE_NOKTA = re.compile(r"%\s*(\d+)\.(\d+)")


def _ablatif(sayi: str) -> str:
    son = re.split(r"[.,]", sayi)[-1].lstrip("0") or "0"
    if son[-1] != "0" or son == "0":
        return _ABL[son[-1]]
    if len(son) >= 2 and son[-2] != "0" and (len(son) == 2 or son[-3:] != "000"):
        return _ABL_ONLUK[son[-2]]
    return "den"  # yüz, bin, milyon


def _karsilastirma(metin: str) -> str:
    def f(m):
        sayi = m.group(2).replace(".", ",")
        sifat = "küçük" if m.group(1) in "<≤" else "büyük"
        if m.group(1) in "≤≥":
            sifat += " ya da eşit"
        ek = "tür" if (m.group(3) or "").startswith(("d", "t")) and len(m.group(3)) <= 3 else ""
        return f"%{sayi}'{_ablatif(sayi)} {sifat}{ek}"
    def g(m):  # yüzdesiz: "< 5 mm" → "5 mm'den küçük", "≥ 0.5" → "0,5'ten büyük ya da eşit"
        sayi, birim, ek_ = m.group(2).replace(".", ","), m.group(3), m.group(4) or ""
        sifat = ("küçük" if m.group(1) in "<≤" else "büyük") + (" ya da eşit" if m.group(1) in "≤≥" else "")
        ek = "tür" if ek_.startswith(("d", "t")) and len(ek_) <= 3 else ""
        return f"{sayi} {birim}'{_BIRIM_ABL[birim]} {sifat}{ek}" if birim else f"{sayi}'{_ablatif(sayi)} {sifat}{ek}"
    return _YUZDE_NOKTA.sub(r"%\1,\2", _KARS_SAYI.sub(g, _KARS.sub(f, metin)))


# Yazılı kalıntılar (H699, 2026-11-26): başlıkta/metinde kalan Yunan harfi, bitişik harf+sayı kodu ve eğik çizgi motora
# ham gidiyordu ("α1A", "beta2", "7q", "3P", "Gq", "Ödem / Herniasyon"). Harf adına çevrilebilir biçime ayrılır.
_YUNAN = {"α": "alfa", "β": "beta", "γ": "gama", "δ": "delta", "ε": "epsilon", "κ": "kappa", "λ": "lambda", "µ": "mü", "μ": "mü"}
_YUNAN_RX = re.compile("[" + "".join(_YUNAN) + "]")
_YUNAN_SAYI = re.compile(r"(?<![\wçğıöşü])(alfa|beta|gama|delta|epsilon|kappa|lambda)(\d+)([A-Z]?)(?![\wÇĞİÖŞÜçğıöşü])")
_SAYI_HARF = re.compile(r"(?<![\w.,])(\d{1,2})([A-Za-z])(?=\d|(?![\wÇĞİÖŞÜçğıöşü]))")
_G_PROT = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])G([sqio])(?![\wÇĞİÖŞÜçğıöşü])")
_ESIK = re.compile(r"\s+/\s+|(?<=[A-Z0-9])/(?=[A-Z])|(?<=[a-zçğıöşü]{2})/(?=[a-zçğıöşü]{2})")


def _kalinti(metin: str) -> str:
    metin = re.sub(r"(?<=[αβγδε])\+(?=[αβγδε])", " ve ", metin)
    metin = _YUNAN_RX.sub(lambda m: " " + _YUNAN[m.group(0)] if m.start() and metin[m.start() - 1].isalnum() else _YUNAN[m.group(0)], metin)
    metin = _YUNAN_SAYI.sub(lambda m: f"{m.group(1)} {m.group(2)}" + (f" {m.group(3)}" if m.group(3) else ""), metin)
    metin = re.sub(r"(?<=[\dXY][pq])(\d+)\.(\d+)", r"\1 nokta \2", metin)  # kromozom bandı 15q13.3
    metin = re.sub(r"(?<=[A-Za-z0-9])\+(?=[\s,.;:)]|$)", " pozitif", metin)  # CD4+ hücre
    metin = _SAYI_HARF.sub(lambda m: f"{m.group(1)} {m.group(2).upper()} ", metin)
    metin = re.sub(r"(?<=[A-Z]) (?=[\s,.;:)'’])", "", metin)
    metin = _G_PROT.sub(lambda m: "gee " + {"s": "see", "q": "kuu", "i": "ıı", "o": "oo"}[m.group(1)], metin)
    metin = re.sub(r"(?<=[XY])(?=[pq](?![a-zçğıöşü]))", " ", metin)  # Xq27.3 → X q
    metin = re.sub(r"(?<![\wÇĞİÖŞÜçğıöşü'’-])[pq](?![\wÇĞİÖŞÜçğıöşü'’-])(?!\s*[<>=≤≥])", lambda m: "pee" if m.group(0) == "p" else "kuu", metin)  # "on beş q on üç"
    return _ESIK.sub(", ", metin)


def uzun_yol(metin: str, ek_kisaltma: set[str] | None = None) -> str:
    korunan: list[str] = []
    metin = _baslik_kucult(_kutu_temizle(metin))
    metin = _kalinti(_terim(metin))
    metin = _yazim_kisaltma(metin, korunan)
    for pat, fon in okunus.FONETIK_TTS:
        metin = pat.sub(fon, metin)
    metin = _sakla(metin, _BAGLAC_DIZI, korunan)
    return _geri(kisaltma_ses.uzat(metin, ek_kisaltma), korunan)


def bitisik_yol(metin: str) -> str:
    return okunus.duzelt(_terim(_kutu_temizle(metin)))


# Tablo/ liste metni tek "cümle" olarak motora gidince motor durmayıp konuşmaya devam edebiliyor (H587: 811 sn'lik tek cümle).
PARCA_SINIR = 400


def parcala(metin: str, sinir: int = PARCA_SINIR) -> list[str]:
    """Çok uzun (> sinir karakter) tek parçayı motor için ardışık parçalara böler: önce ; : sonra , sonra boşlukta.
    Kısa metin olduğu gibi tek öğe döner. Klip karmasına/ekran metnine dokunmaz (yalnız motora gidiş)."""
    metin = metin.strip()
    if len(metin) <= sinir:
        return [metin] if metin else []
    for ayrac in (r"(?<=[;:])\s+", r"(?<=,)\s+", r"\s+"):
        bolum = [b for b in re.split(ayrac, metin) if b.strip()]
        if len(bolum) < 2:
            continue
        out, cur = [], ""
        for b in bolum:
            if cur and len(cur) + 1 + len(b) > sinir:
                out.append(cur)
                cur = b
            else:
                cur = f"{cur} {b}" if cur else b
        if cur:
            out.append(cur)
        return [y for x in out for y in (parcala(x, sinir) if len(x) > sinir else [x])]
    return [metin[i:i + sinir] for i in range(0, len(metin), sinir)]  # boşluksuz dev dizgi (pratikte yok)


def hazirla(metin: str, *, kurul: int | None = None, ders: str | None = None, modul: str | None = None,
            yol: str | None = None, ek_kisaltma: set[str] | None = None) -> str:
    """Ekran/konuşma metni → EMA'ya giden okunuş metni. `yol` verilirse ('uzun'/'bitisik') seçim atlanır
    (ör. çözücü klipleri tasarım gereği daima uzun: SURUM ema-2)."""
    y = yol or yol_sec(kurul=kurul, ders=ders, modul=modul)
    metin = re.sub("[\uE000-\uF8FF]", "", metin)  # girdideki simge yazı tipi karakterleri (okunmaz; yer tutucuyla çakışır)
    metin = _karsilastirma(metin)
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
