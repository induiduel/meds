"""Öğren desteleri için TEK okuma/yazma noktası (Python tarafı).

Neden: `src/data/interactive_learning_decks.json` (~90 MB) ~20 betik tarafından tam okunup tam yazılıyordu;
her biri kendi yolunu, kendi yazma biçimini kullanıyordu (atomik değil, kilitsiz). Depo yolu, atomik yazımı ve
kilidi tek yerde toplar; arka uç (tek dosya → parçalı) ileride yalnız bu dosyada değişir.

Kullanım:
    import deste_deposu as dd
    desteler = dd.hepsi()            # list[dict], dosyadaki sırayla
    d = dd.oku("k1-07")              # dict | None (id ya da deckId)
    with dd.duzenle() as desteler:   # kilit + atomik yazım; listeyi yerinde değiştir
        desteler.append(yeni)
    dd.guncelle(deste)               # aynı id varsa yerinde değiştir, yoksa sona ekle
    dd.sil("k1-07")

Ortam: DESTE_DOSYASI ile farklı dosya (sınama) verilebilir.

Parçalı arka uç (VERI_MODELI Faz 3, iskele — varsayılan KAPALI):
    MEDS_DESTE_PARCALI=1 + MEDS_DESTE_PARCA_DIZIN=<dizin> verilirse `yol` argümanı VERİLMEYEN çağrılar monolit yerine
    parça dizininde çalışır. Biçim:
      <dizin>/_sira.json      {"bicim": 1, "desteler": [{"id", "dosya", "sha1"[, "deckId"]}, ...]}  (sıra = monolit sırası)
      <dizin>/<dosya>.json    tek deste, monolitle AYNI serileştirme: json.dumps(ensure_ascii=False), girintisiz,
                              varsayılan ayraçlar (", " / ": "), sonda satır sonu YOK.
    Birleştirme: "[" + ", ".join(parça baytları) + "]" == monolit baytları (json.dumps(liste) tanımı gereği).
    Kimlik → dosya adı: kimlik `[A-Za-z0-9][A-Za-z0-9._-]*` ise kendisi, değilse "~" + UTF-8 onaltılık; "~" ve "_"
    güvenli kümede baş harf olamadığından çakışmaz ve geri çevrilir (`dosya_adi` / `kimlik_of`).
    Bayrak yokken kod yolu öncekiyle birebir aynıdır (`_parcali()` False → eski dallar).
"""
from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

_MEDS = Path(__file__).resolve().parent.parent
YOL = Path(os.environ.get("DESTE_DOSYASI") or _MEDS / "src" / "data" / "interactive_learning_decks.json")


def _kilit_yolu() -> Path:
    return YOL.with_name(YOL.name + ".lock")


# ---------------------------------------------------------------- parçalı biçim (ortak: deste_bol.py da kullanır)
BICIM = 1
SIRA = "_sira.json"
_GUVENLI = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def dosya_adi(kimlik: str) -> str:
    if _GUVENLI.fullmatch(kimlik) and len(kimlik) <= 200:
        return kimlik + ".json"
    return "~" + kimlik.encode("utf-8").hex() + ".json"


def kimlik_of(dosya: str) -> str:
    ad = dosya[:-5] if dosya.endswith(".json") else dosya
    return bytes.fromhex(ad[1:]).decode("utf-8") if ad.startswith("~") else ad


def seri(deste: dict) -> bytes:
    """Tek destenin monolit içindeki bayt biçimi."""
    return json.dumps(deste, ensure_ascii=False).encode("utf-8")


def birlestir_bayt(parcalar: list) -> bytes:
    return b"[" + b", ".join(parcalar) + b"]"


def _parcali() -> bool:
    return os.environ.get("MEDS_DESTE_PARCALI") == "1" and bool(os.environ.get("MEDS_DESTE_PARCA_DIZIN"))


def parca_dizini() -> Path:
    return Path(os.environ["MEDS_DESTE_PARCA_DIZIN"])


def _atomik_bayt(p: Path, veri: bytes) -> None:
    fd, gecici = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=p.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(veri)
        os.replace(gecici, p)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(gecici)
        raise


def sira_oku(dizin: Path) -> dict:
    p = dizin / SIRA
    if not p.exists():
        return {"bicim": BICIM, "desteler": []}
    with open(p, encoding="utf-8") as f:
        s = json.load(f)
    if s.get("bicim") != BICIM:
        raise ValueError(f"desteler/_sira.json biçimi {s.get('bicim')} ≠ {BICIM}")
    return s


def sira_kaydi(deste: dict, bayt: bytes) -> dict:
    k = deste.get("id")
    if not isinstance(k, str) or not k:
        raise ValueError("kimliksiz deste parçalanamaz")
    g = {"id": k, "dosya": dosya_adi(k), "sha1": hashlib.sha1(bayt).hexdigest()}
    if deste.get("deckId") not in (None, k):
        g["deckId"] = deste.get("deckId")
    return g


def sira_yaz(dizin: Path, girdiler: list) -> None:
    _atomik_bayt(dizin / SIRA, (json.dumps({"bicim": BICIM, "desteler": girdiler}, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


def parca_baytlari(dizin: Path) -> list:
    return [(dizin / g["dosya"]).read_bytes() for g in sira_oku(dizin)["desteler"]]


def parcali_yaz(desteler: list, dizin: Path) -> int:
    """Listeyi parçalara yazar: yalnız baytı değişen dosyalar + _sira.json (en son); listeden düşen dosyalar silinir."""
    dizin.mkdir(parents=True, exist_ok=True)
    eski = {g["dosya"]: g for g in sira_oku(dizin)["desteler"]}
    girdiler, yazilan = [], 0
    for d in desteler:
        b = seri(d)
        g = sira_kaydi(d, b)
        if any(x["dosya"] == g["dosya"] for x in girdiler):
            raise ValueError(f"yinelenen deste kimliği: {g['id']}")
        e = eski.get(g["dosya"])
        if not e or e["sha1"] != g["sha1"] or not (dizin / g["dosya"]).exists():
            _atomik_bayt(dizin / g["dosya"], b)
            yazilan += 1
        girdiler.append(g)
    sira_yaz(dizin, girdiler)
    kalan = {g["dosya"] for g in girdiler}
    for ad in eski:
        if ad not in kalan:
            with contextlib.suppress(FileNotFoundError):
                (dizin / ad).unlink()
    return yazilan


def _parca_oku(kimlik: str) -> dict | None:
    dizin = parca_dizini()
    p = dizin / dosya_adi(kimlik)
    if not p.exists():  # deckId ile arama: yalnız sıra dosyasına bakılır
        g = next((g for g in sira_oku(dizin)["desteler"] if g.get("deckId") == kimlik), None)
        if not g:
            return None
        p = dizin / g["dosya"]
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def hepsi(yol: Path | None = None) -> list:
    if yol is None and _parcali():
        return json.loads(birlestir_bayt(parca_baytlari(parca_dizini())))
    p = Path(yol) if yol else YOL
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as f:
        veri = json.load(f)
    return veri if isinstance(veri, list) else veri.get("decks", [])


def oku(kimlik: str, yol: Path | None = None) -> dict | None:
    if yol is None and _parcali():
        return _parca_oku(kimlik)
    for d in hepsi(yol):
        if d.get("id") == kimlik or d.get("deckId") == kimlik:
            return d
    return None


# Varsayılan biçim mevcut dosyayla birebir: tek satır, json varsayılan ayraçları, sonda satır sonu yok.
def yaz_hepsi(desteler: list, yol: Path | None = None, girinti: int | None = None) -> None:
    """Atomik yazım (aynı dizinde geçici dosya + os.replace). Kilit ÇAĞIRANIN sorumluluğunda değil: duzenle() kullan."""
    p = Path(yol) if yol else YOL
    fd, gecici = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(desteler, f, ensure_ascii=False, indent=girinti)
            if girinti is not None:
                f.write("\n")
        os.replace(gecici, p)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(gecici)
        raise


@contextlib.contextmanager
def kilit():
    with open(_kilit_yolu(), "w") as k:
        fcntl.flock(k, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(k, fcntl.LOCK_UN)


@contextlib.contextmanager
def duzenle(yol: Path | None = None, girinti: int | None = None):
    """Oku → çağıran listeyi değiştirir → atomik yaz; hepsi tek kilit altında."""
    with kilit():
        desteler = hepsi(yol)
        yield desteler
        if yol is None and _parcali():
            parcali_yaz(desteler, parca_dizini())  # parça biçimi sabit; girinti uygulanmaz
        else:
            yaz_hepsi(desteler, yol, girinti)


def guncelle(deste: dict, yol: Path | None = None) -> bool:
    """Aynı id varsa yerinde değiştirir (sıra korunur, True); yoksa sona ekler (False)."""
    if yol is None and _parcali():  # tek dosya + _sira.json; monolit ayrıştırılmaz
        dizin = parca_dizini()
        with kilit():
            dizin.mkdir(parents=True, exist_ok=True)
            s = sira_oku(dizin)["desteler"]
            b = seri(deste)
            g = sira_kaydi(deste, b)
            _atomik_bayt(dizin / g["dosya"], b)
            i = next((i for i, x in enumerate(s) if x["id"] == g["id"]), None)
            if i is None:
                s.append(g)
            else:
                s[i] = g
            sira_yaz(dizin, s)
            return i is not None
    with duzenle(yol) as desteler:
        for i, d in enumerate(desteler):
            if d.get("id") == deste.get("id"):
                desteler[i] = deste
                return True
        desteler.append(deste)
        return False


def sil(kimlik: str, yol: Path | None = None) -> bool:
    if yol is None and _parcali():
        dizin = parca_dizini()
        with kilit():
            s = sira_oku(dizin)["desteler"]
            kalan = [g for g in s if g["id"] != kimlik]
            if len(kalan) == len(s):
                return False
            sira_yaz(dizin, kalan)  # önce sıra: yarıda kalırsa yetim dosya zararsız
            for g in s:
                if g["id"] == kimlik:
                    with contextlib.suppress(FileNotFoundError):
                        (dizin / g["dosya"]).unlink()
            return True
    with duzenle(yol) as desteler:
        n = len(desteler)
        desteler[:] = [d for d in desteler if d.get("id") != kimlik]
        return len(desteler) != n
