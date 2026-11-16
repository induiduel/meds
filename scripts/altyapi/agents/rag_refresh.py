#!/usr/bin/env python3
"""
RAG ve veritabanı yenileme (tek adım): ortak depo + RAG parçaları → site analizleri → site arama dizini.
Faz 14 tüm soruları işleyince kendiliğinden kuyruğa girer; panelden elle de çalıştırılabilir.
Site arama dizini (localRagEngine) sunucu açılışında kurulduğu için meds-web yeniden başlatılır.
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = _kok.MEDS
PY = str(ROOT / ".venv-ocr" / "bin" / "python")


def step(title: str, cmd: list[str]) -> int:
    print(f"[{time.strftime('%H:%M:%S')}] ▶ {title}", flush=True)
    rc = subprocess.run(cmd, cwd=str(ROOT)).returncode
    print(f"[{time.strftime('%H:%M:%S')}] {'✓' if rc == 0 else '✗'} {title} (rc={rc})", flush=True)
    return rc


def main() -> int:
    rcs = [
        step("Faz 12 ders notu temizliği (yeni notlar)", [PY, "scripts/altyapi/advanced_ai/phase12_clean_notes.py"]),
        step("Ortak depo + RAG parçaları", [PY, "scripts/altyapi/advanced_ai/build_unified_store.py"]),
        step("Müfredat paketi", [PY, "scripts/altyapi/advanced_ai/curriculum_package.py"]),
        step("Site analizleri", [PY, "scripts/altyapi/advanced_ai/export_phase_insights.py"]),
        step("Site arama dizini (meds-web yeniden başlatma)", ["systemctl", "--user", "restart", "meds-web"]),
    ]
    print(json.dumps({"rag_yenile": "tamam" if not any(rcs) else "hatalı adım var", "rc": rcs}, ensure_ascii=False))
    return 0 if not any(rcs) else 1


if __name__ == "__main__":
    sys.exit(main())
