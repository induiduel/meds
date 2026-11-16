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
