"""RAG parça deposu okuyucusu (Python eşi: src/services/ragParcaDeposu.ts).

Kural: data/local_rag_chunks.jsonl VARSA esas odur (satır satır okunur, bozuk satır atlanıp sayılır);
yoksa eski data/local_rag_chunks.json (tek JSON dizisi) okunur. mtime'a bakılmaz.
`nul_temizle=True` → satırdaki "\\u0000" kaçışları ayrıştırmadan önce atılır (Postgres NUL kabul etmez).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

JSONL_ADI = "local_rag_chunks.jsonl"
JSON_ESKI_ADI = "local_rag_chunks.json"


def okunacak_dosya(data_dir: Path) -> Path | None:
    data_dir = Path(data_dir)
    for ad in (JSONL_ADI, JSON_ESKI_ADI):
        p = data_dir / ad
        if p.exists():
            return p
    return None


def parcalari_oku(data_dir: Path, nul_temizle: bool = False) -> list[dict]:
    p = okunacak_dosya(data_dir)
    if p is None:
        return []
    if p.name == JSON_ESKI_ADI:
        metin = p.read_text(encoding="utf-8")
        if nul_temizle:
            metin = metin.replace("\\u0000", "")
        d = json.loads(metin)
        return d if isinstance(d, list) else d.get("chunks", [])
    out: list[dict] = []
    bozuk = 0
    with open(p, encoding="utf-8") as f:
        for satir in f:
            if not satir.strip():
                continue
            if nul_temizle:
                satir = satir.replace("\\u0000", "")
            try:
                c = json.loads(satir)
            except ValueError:
                bozuk += 1
                continue
            if isinstance(c, dict) and c.get("id"):
                out.append(c)
            else:
                bozuk += 1
    if bozuk:
        print(f"[rag_parca_deposu] UYARI: {p} içinde {bozuk} bozuk satır atlandı", file=sys.stderr)
    return out
