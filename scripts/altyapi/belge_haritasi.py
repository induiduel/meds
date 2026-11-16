"""meds/docs/HARITA.md üretir: her belgenin ilk başlığı, boyutu, son değişimi ve nereden anıldığı (AGENTS/CLAUDE, betikler).

Kullanım: python3 scripts/altyapi/belge_haritasi.py            (belge eklenince/silinince yeniden çalıştır)
          python3 scripts/altyapi/belge_haritasi.py --denetle  (yazmaz; dosya bayatsa çıkış 1 — yapi_koruma D8)
--denetle "Son değişim" sütununu karşılaştırmaz: o tarih commit'le kendiliğinden değişir, her commit'ten
sonra haritayı bayat göstermesin diye (kök neden 2026-11-16). Tarihler tek `git log` geçişiyle alınır (<1 sn).
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
denetle = "--denetle" in _sys.argv[1:]
tarihler: dict = {}
_g = subprocess.run(["git", "log", "--format=@%cs", "--name-only", "--", "docs"], capture_output=True, text=True).stdout
_t = ""
for _s in _g.splitlines():
    if _s.startswith("@"):
        _t = _s[1:]
    elif _s.strip():
        tarihler.setdefault(_s.strip(), _t)
_adlar = [os.path.basename(f) for f in glob.glob("docs/*.md")]
# hangi betik hangi belgeyi anıyor: tek `git grep -o` (C hızında; Python alt dize taraması büyük dosyalarda 1+ sn sürüyordu)
_o = subprocess.run(["git", "grep", "-o", "-F"] + [x for a in _adlar for x in ("-e", a)] + ["--", "scripts", "otomasyon", "src", "server.ts"],
                    capture_output=True, text=True).stdout
anma: dict = {}
for _s in _o.splitlines():
    _f, _, _a = _s.rpartition(":")
    anma.setdefault(_a, set()).add(_f)
satir = []
for f in sorted(glob.glob("docs/*.md")):
    ad = os.path.basename(f)
    if ad == "HARITA.md":
        continue
    t = open(f, encoding="utf-8", errors="ignore").read()
    m = re.search(r"^#\s+(.+)$", t, re.M)
    baslik = (m.group(1) if m else ad).strip()[:90].replace("|", "/")
    tarih = tarihler.get(f, "izlenmiyor")
    kd = len(anma.get(ad, ()))
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
metin = "\n".join(out) + "\n"
if denetle:
    def _norm(x: str) -> str:
        return re.sub(r"\| (\d{4}-\d\d-\d\d|izlenmiyor) \|", "| - |", x)
    eski = open("docs/HARITA.md", encoding="utf-8").read() if os.path.exists("docs/HARITA.md") else ""
    if _norm(eski) != _norm(metin):
        print("docs/HARITA.md bayat — yeniden üret: python3 scripts/altyapi/belge_haritasi.py")
        _sys.exit(1)
    _sys.exit(0)
open("docs/HARITA.md", "w", encoding="utf-8").write(metin)
print(f"docs/HARITA.md: {len(anilan)} anılan, {len(yetim)} yetim")
