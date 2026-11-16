"""v2 test paketi. `scripts` dizinini sys.path'e ekler ki `v2.*` içe aktarılabilsin."""
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[2]  # v2 paketinin kabı (scripts/altyapi): -m v2 buradan çözülür
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
