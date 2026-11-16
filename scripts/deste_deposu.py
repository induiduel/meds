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
"""
from __future__ import annotations

import contextlib
import fcntl
import json
import os
import tempfile
from pathlib import Path

_MEDS = Path(__file__).resolve().parent.parent
YOL = Path(os.environ.get("DESTE_DOSYASI") or _MEDS / "src" / "data" / "interactive_learning_decks.json")


def _kilit_yolu() -> Path:
    return YOL.with_name(YOL.name + ".lock")


def hepsi(yol: Path | None = None) -> list:
    p = Path(yol) if yol else YOL
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as f:
        veri = json.load(f)
    return veri if isinstance(veri, list) else veri.get("decks", [])


def oku(kimlik: str, yol: Path | None = None) -> dict | None:
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
        yaz_hepsi(desteler, yol, girinti)


def guncelle(deste: dict, yol: Path | None = None) -> bool:
    """Aynı id varsa yerinde değiştirir (sıra korunur, True); yoksa sona ekler (False)."""
    with duzenle(yol) as desteler:
        for i, d in enumerate(desteler):
            if d.get("id") == deste.get("id"):
                desteler[i] = deste
                return True
        desteler.append(deste)
        return False


def sil(kimlik: str, yol: Path | None = None) -> bool:
    with duzenle(yol) as desteler:
        n = len(desteler)
        desteler[:] = [d for d in desteler if d.get("id") != kimlik]
        return len(desteler) != n
