"""meds/docs/HARITA.md üretir: her belgenin ilk başlığı, boyutu, son değişimi ve nereden anıldığı (AGENTS/CLAUDE, betikler).

Kullanım: python3 scripts/altyapi/belge_haritasi.py   (belge eklenince/silinince yeniden çalıştır)
"""
import glob
import os
import re
import subprocess
import sys as _sys
from pathlib import Path as _Path

_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

os.chdir(_kok.MEDS)
agents = "".join(open(p, encoding="utf-8").read() for p in (_kok.PROJE / "AGENTS.md", _kok.MEDS / "CLAUDE.md", _kok.MEDS / "AGENTS.md") if p.exists())
kod = subprocess.run(["git", "grep", "-l", "docs/", "--", "scripts", "otomasyon", "src", "server.ts"], capture_output=True, text=True).stdout.split()
kodmetin = [open(f, encoding="utf-8", errors="ignore").read() for f in kod]
satir = []
for f in sorted(glob.glob("docs/*.md")):
    ad = os.path.basename(f)
    if ad == "HARITA.md":
        continue
    t = open(f, encoding="utf-8", errors="ignore").read()
    m = re.search(r"^#\s+(.+)$", t, re.M)
    baslik = (m.group(1) if m else ad).strip()[:90].replace("|", "/")
    tarih = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip() or "izlenmiyor"
    kd = sum(1 for x in kodmetin if ad in x)
    nerede = ", ".join(x for x in ["AGENTS/CLAUDE" if ad in agents else "", f"{kd} betik" if kd else ""] if x) or "—"
    satir.append((ad, baslik, len(t.split()), tarih, nerede))
anilan = [s for s in satir if s[4] != "—"]
yetim = [s for s in satir if s[4] == "—"]
out = ["# `meds/docs/` Haritası — hangi belge ne için (otomatik üretilir)\n",
       "> Belgeleri gezmeden önce buraya bak; yalnız işinin belgesini aç (AGENTS 'Yönlendirme').",
       "> Yeniden üret: `python3 scripts/altyapi/belge_haritasi.py`. \"Anıldığı yer\" = AGENTS.md/CLAUDE.md ya da betiklerin belgeyi adıyla anması.\n",
       f"## Bağlayıcı / kullanılan belgeler ({len(anilan)})\n", "| Belge | Konu (ilk başlık) | Kelime | Son değişim | Anıldığı yer |", "|---|---|---:|---|---|"]
out += [f"| `{a}` | {b} | {k} | {d} | {n} |" for a, b, k, d, n in anilan]
out += [f"\n## Hiçbir yerden anılmayan belgeler ({len(yetim)}) — eski olabilir; bağlayıcı sayma, gerekirse doğrula\n",
        "| Belge | Konu | Kelime | Son değişim |", "|---|---|---:|---|"]
out += [f"| `{a}` | {b} | {k} | {d} |" for a, b, k, d, _ in yetim]
open("docs/HARITA.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"docs/HARITA.md: {len(anilan)} anılan, {len(yetim)} yetim")
