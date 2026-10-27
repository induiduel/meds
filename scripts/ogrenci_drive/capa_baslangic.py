#!/usr/bin/env python3
"""Çapa yazımı için başlangıç capa.json (TALIMAT_CAPA): cumleler.md'deki her cümleye sayfa — konusma_v2'nin slayt
bağından (cümle sayısı tutan paragrafta), yoksa hizalamanın paragraf sayfası. mdSha1 = metin dosyasının sha1'i.
  python3 scripts/ogrenci_drive/capa_baslangic.py <key> <capa_dok dizini> [--v2 konusma_v2.json]"""
import hashlib, json, re, sys
from pathlib import Path
MEDS = Path(__file__).resolve().parents[2]
k, D = sys.argv[1], Path(sys.argv[2])
v2 = json.loads(Path(sys.argv[sys.argv.index("--v2") + 1]).read_text()) if "--v2" in sys.argv else None
hz = json.loads((MEDS / "data/sesli_anlatim/hizalama" / f"{k}.json").read_text())
C = {}
for l in (D / "cumleler.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^P(\d+)\.C(\d+):\s*(.*)$", l)
    if m:
        C.setdefault(int(m[1]), {})[int(m[2])] = m[3]
vp = [p for b in v2["bolumler"] for p in b["paragraflar"]] if v2 else []
p = []
for pi in sorted(C):
    vs = vp[pi]["cumleler"] if pi < len(vp) else []
    ayni = len(vs) == len(C[pi])
    p.append([{"ses": C[pi][ci][:60], "dosya": 0,
               "sayfa": ((vs[ci].get("slayt") or {}).get("sayfa") if ayni else None) or hz["paragraflar"][pi]["sayfa"]}
              for ci in sorted(C[pi])])
sha = hashlib.sha1((MEDS / "data/sesli_anlatim/metin" / f"{k}.md").read_bytes()).hexdigest()
(D / "capa.json").write_text(json.dumps({"mdSha1": sha, "p": p}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(p), "paragraf", sum(map(len, p)), "cümle;", sum(1 for pi in sorted(C) if pi < len(vp) and len(vp[pi]["cumleler"]) == len(C[pi])), "paragrafta v2 sayfası")
