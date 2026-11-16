"""Konum-bağımsız proje kökü bulucu (2026-11-16 yeniden yapılandırma).

Betikler `Path(__file__).resolve().parents[N]` gibi SABİT kademe derinliği yerine
bunu kullanır; böylece dosya hangi alt klasöre taşınırsa taşınsın kök doğru bulunur.
Marker dosyaları worktree-güvenlidir (walk-up yalnız üst dizinlere bakar):

- SCRIPTS = meds/scripts   (marker: kok.py — bu dosya)
- MEDS    = meds/          (marker: server.ts)
- PROJE   = /home/indu/medsor (marker: PROJE_TANITIMI.md)

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
MEDS = _up("server.ts")
PROJE = _up("PROJE_TANITIMI.md")


def scripts_koku(start: str = __file__) -> Path:
    return _up("kok.py", start)


def meds_koku(start: str = __file__) -> Path:
    return _up("server.ts", start)


def proje_koku(start: str = __file__) -> Path:
    return _up("PROJE_TANITIMI.md", start)


if __name__ == "__main__":
    print(f"SCRIPTS = {SCRIPTS}")
    print(f"MEDS    = {MEDS}")
    print(f"PROJE   = {PROJE}")
