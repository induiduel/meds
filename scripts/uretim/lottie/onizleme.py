#!/usr/bin/env python3
"""Lottie kare şeridi önizlemesi: dist/__lottie_onizleme.html (yerel 3000'de açılır, işten sonra silinir)."""
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import json, sys
from pathlib import Path
KOK = _kok.MEDS
ad_kare = {"zirve": [40, 150, 215, 255, 290, 320, 360, 420, 470, 520, 548, 575],
           "calisma": [30, 130, 165, 250, 320, 360, 395, 420, 500], "sevgi": [30, 100, 165, 215, 245, 292, 330, 380, 440], "gunes": [60, 175, 225, 260, 310, 360, 410, 455, 500]}
sec = sys.argv[1:] or list(ad_kare)
an = {n: json.loads((KOK / f"src/assets/lottie/{n}.json").read_text()) for n in sec}
lot = (KOK / "node_modules/lottie-web/build/player/lottie_light.min.js").read_text()
html = ("<html><body style='margin:0;background:#fff;font:11px sans-serif'><script>" + lot + "</script><script>const A=" + json.dumps(an)
        + ";const F=" + json.dumps({k: ad_kare[k] for k in sec}) + """;
for(const n in A){const row=document.createElement('div');row.style.cssText='display:flex;flex-wrap:wrap';document.body.appendChild(row);
for(const f of F[n]){const w=document.createElement('div');w.style.cssText='width:260px;text-align:center';const d=document.createElement('div');d.style.cssText='width:260px;height:260px;border:1px solid #eee';w.appendChild(d);w.append(n+' '+f);row.appendChild(w);
const a=lottie.loadAnimation({container:d,renderer:'svg',loop:false,autoplay:false,animationData:JSON.parse(JSON.stringify(A[n]))});a.goToAndStop(f,true);}}
</script></body></html>""")
(KOK / "dist/__lottie_onizleme.html").write_text(html)
