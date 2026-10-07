#!/usr/bin/env python3
"""
RAG ve veritabanı yenileme (tek adım): ortak depo + RAG parçaları → site analizleri → site arama dizini.
Faz 14 tüm soruları işleyince kendiliğinden kuyruğa girer; panelden elle de çalıştırılabilir.
Site arama dizini (localRagEngine) sunucu açılışında kurulduğu için meds-web yeniden başlatılır.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = str(ROOT / ".venv-ocr" / "bin" / "python")


def step(title: str, cmd: list[str]) -> int:
    print(f"[{time.strftime('%H:%M:%S')}] ▶ {title}", flush=True)
    rc = subprocess.run(cmd, cwd=str(ROOT)).returncode
    print(f"[{time.strftime('%H:%M:%S')}] {'✓' if rc == 0 else '✗'} {title} (rc={rc})", flush=True)
    return rc


def main() -> int:
    rcs = [
        step("Faz 12 ders notu temizliği (yeni notlar)", [PY, "scripts/advanced_ai/phase12_clean_notes.py"]),
        step("Ortak depo + RAG parçaları", [PY, "scripts/advanced_ai/build_unified_store.py"]),
        step("Müfredat paketi", [PY, "scripts/advanced_ai/curriculum_package.py"]),
        step("Site analizleri", [PY, "scripts/advanced_ai/export_phase_insights.py"]),
        step("Site arama dizini (meds-web yeniden başlatma)", ["systemctl", "--user", "restart", "meds-web"]),
    ]
    print(json.dumps({"rag_yenile": "tamam" if not any(rcs) else "hatalı adım var", "rc": rcs}, ensure_ascii=False))
    return 0 if not any(rcs) else 1


if __name__ == "__main__":
    sys.exit(main())
