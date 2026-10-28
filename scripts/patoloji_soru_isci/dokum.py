#!/usr/bin/env python3
"""Ders PDF'ini biçim işaretli düz metne döker (analiz ve yazar ajanları için).
  meds/.venv-ocr/bin/python -I scripts/patoloji_soru_isci/dokum.py <ders.pdf> <cikti.txt>
İşaretler: ⟦kırmızı⟧  ‹kalın›  satır başı  Y| = sarı dolgulu satır, # = başlık boyutu (≥24 pt), (gN) = sayfadaki görsel sayısı."""
import sys, pymupdf
from pathlib import Path
doc = pymupdf.open(sys.argv[1]); out = []
for p in doc:
    hl = [d["rect"] for d in p.get_drawings() if d.get("fill") and d["fill"][0] > .95 and d["fill"][1] > .95 and d["fill"][2] < .2 and d["rect"].height < 45]
    out.append(f"=== SAYFA {p.number+1} (g{len(p.get_images())}) ===")
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            sp = [s for s in l["spans"] if s["text"].strip() or s["text"]]
            if not "".join(s["text"] for s in sp).strip(): continue
            r = pymupdf.Rect(l["bbox"]); y = any(not (r & h).is_empty for h in hl)
            seg = ""
            for s in sp:
                t = s["text"]
                if s["color"] == 0xFF0000 and t.strip(): t = f"⟦{t}⟧"
                if (s["flags"] & 16 or "Bold" in s["font"]) and t.strip(): t = f"‹{t}›"
                seg += t
            seg = seg.replace("⟧⟦", "").replace("›‹", "")
            big = max(s["size"] for s in sp) >= 24
            out.append(("Y|" if y else "") + ("# " if big else "") + seg)
Path(sys.argv[2]).write_text("\n".join(out))
