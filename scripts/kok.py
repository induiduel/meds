"""Konum-bağımsız proje kökü bulucu (2026-11-16 yeniden yapılandırma).

Betikler `Path(__file__).resolve().parents[N]` gibi SABİT kademe derinliği yerine
bunu kullanır; böylece dosya hangi alt klasöre taşınırsa taşınsın kök doğru bulunur.
Marker dosyaları worktree-güvenlidir (walk-up yalnız üst dizinlere bakar):

- SCRIPTS = meds/scripts   (marker: kok.py — bu dosya)
- MEDS    = meds/          (marker: server.ts)
- PROJE   = MEDS.parent (marker YOK — Oracle/Docker'da kök belgeleri bulunmaz, H579)

Kullanım (taşınan betiğin başına):
    import sys; from pathlib import Path as _P
    _s = _P(__file__).resolve()
    while not (_s / 'kok.py').exists() and _s != _s.parent:
        _s = _s.parent
    sys.path.insert(0, str(_s))
    from kok import MEDS, PROJE, SCRIPTS
"""
from pathlib import Path


def _up(marker: str, start: str = __file__) -> Path:
    p = Path(start).resolve()
    for q in (p, *p.parents):
        if (q / marker).exists():
            return q
    raise RuntimeError(f"kök markerı '{marker}' bulunamadı (başlangıç: {start})")


SCRIPTS = _up("kok.py")
try:
    MEDS = _up("server.ts")
except RuntimeError:  # server.ts olmayan dağıtım/kopya: scripts/ her zaman meds/ altındadır
    MEDS = SCRIPTS.parent
# PROJE marker'a BAĞLANMAZ (H579): PROJE_TANITIMI.md yalnız geliştirme makinesindeki repo-dışı kökte var; Oracle
# (/home/ubuntu/medsor) ve Docker (/app) onu taşımaz → import anında çöküyordu. Eski kodun parents[3]'ü ile birebir aynı anlam.
PROJE = MEDS.parent

# Çıkmış soru arşivinin TEK fiziksel kopyası (2026-11-16). Eskiden server.ts her kayıtta src/data/pastQuestions.json'a
# aynalıyordu; okuyucular buna bağlanır, src/data kopyası okunmaz/yazılmaz.
CIKMIS = MEDS / "data" / "pastQuestions.json"


def cikmis_yolu() -> Path:
    return CIKMIS


# Ders özeti kataloğunun TEK asıl kaynağı (2026-11-16). data/lectureSummariesCatalog.json eski kopyadır, okunmaz/yazılmaz.
# Canlı katman farkı (data/content/lectureSummariesCatalog.json.fark.json) Oracle'dan dağıtım [0b] ile buraya geri çekilir.
OZET_KATALOG = MEDS / "src" / "data" / "lectureSummariesCatalog.json"


def scripts_koku(start: str = __file__) -> Path:
    return _up("kok.py", start)


def meds_koku(start: str = __file__) -> Path:
    return _up("server.ts", start)


def proje_koku(start: str = __file__) -> Path:
    return meds_koku(start).parent


if __name__ == "__main__":
    print(f"SCRIPTS = {SCRIPTS}")
    print(f"MEDS    = {MEDS}")
    print(f"PROJE   = {PROJE}")
    print(f"CIKMIS  = {CIKMIS}")
    print(f"OZET_KATALOG = {OZET_KATALOG}")


# ── pymupdf yoksa .venv-ocr ile yeniden başlat (H623, 2026-11-18) ─────────────────────────────────────────────────────
# Kök neden: pymupdf yalnız meds/.venv-ocr'da; runbook/kapı komutları düz `python3` ile çağrıldığında değerlendirme,
# terim/kısaltma, çıkmış konum vb. betikler ModuleNotFoundError ile düşüyordu. Bu kanca sys.meta_path'in SONUNDA durur:
# yalnız pymupdf/fitz başka hiçbir yerde bulunamazsa devreye girer ve süreci aynı argümanlarla venv Python'unda exec eder.
# Döngü koruması MEDS_OCR_YENIDEN (venv python'u /usr/bin/python3'e sembolik bağ: yürütülebilir değil sys.prefix karşılaştırılır); venv yoksa ya da zaten venv'deysek hiçbir şey yapmaz (asıl ImportError görünür).
import os as _os
import sys as _sys


class _OcrVenvKancasi:
    ADLAR = {"pymupdf", "fitz"}

    def find_spec(self, ad, yol=None, hedef=None):
        if ad not in self.ADLAR or _os.environ.get("MEDS_OCR_YENIDEN"):
            return None
        py = MEDS / ".venv-ocr" / "bin" / "python"
        if not py.exists() or Path(_sys.prefix).resolve() == (MEDS / ".venv-ocr").resolve() or not _sys.argv or not _sys.argv[0]:
            return None
        if _sys.argv[0] in ("-c", "-m"):
            return None
        _os.environ["MEDS_OCR_YENIDEN"] = "1"
        _sys.stdout.flush(); _sys.stderr.flush()
        _os.execv(str(py), [str(py), *_sys.argv])


if not any(isinstance(k, _OcrVenvKancasi) for k in _sys.meta_path):
    _sys.meta_path.append(_OcrVenvKancasi())
