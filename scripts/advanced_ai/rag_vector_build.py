#!/usr/bin/env python3
"""Geriye uyum: eski giriş noktası (new_data_pipeline, dashboard, belgeler). Asıl iş rag_vektor_hatti.py'dedir —
e5 + bge-m3 tek turda, CPU servisleriyle, doğrudan meds-pg'ye; eski seçenekler (--hedef, --sadece-vektor) yok sayılır.
Eski sürüm: scripts/archive/rag_vector_build_eski.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rag_vektor_hatti  # noqa: E402

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    keep, skip = [], False
    for a in args:  # --hedef X / --hedef=X / --sadece-vektor eski seçenekleri
        if skip:
            skip = False
            continue
        if a == "--hedef":
            skip = True
            continue
        if a.startswith("--hedef=") or a == "--sadece-vektor":
            continue
        keep.append(a)
    sys.argv = [sys.argv[0]] + keep
    sys.exit(rag_vektor_hatti.main())
