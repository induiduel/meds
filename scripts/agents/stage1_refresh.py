#!/usr/bin/env python3
"""
Aşama 1 yenileme: indirilemeyen/yeni dosyaları indir, hatalı OCR'lı kaynakları yeni tekniklerle yeniden oku.

Faz zinciri (phase_cycle.py) Faz 8 bitince bunu çalıştırır; ardından sürekli çalışan pipeline_runner
(meds-pipeline servisi) değişen temp1 dosyalarını aşama 2→3→4'ten kendiliğinden geçirir.

1. Drive envanteri + artımlı indirme   → scripts/pipeline/01-inventory.mjs, 02-download.mjs
2. Hatalı OCR tespiti (kaynak bazında): chunk kalite puanı düşük, bozuk karakter oranı yüksek
   ("sඈnav", özel kullanım alanı glifleri) ya da harf düşmesi ("k nuşma") belirtileri
3. Yeniden okuma: read_document.py --force --docling --vision (tablo/başlık korumalı + görsel model)
   Her turda en fazla --max-reocr kaynak; aynı kaynak 7 gün içinde tekrar denenmez.

Durum: meds_temp/state/stage1_refresh_state.json   Rapor: meds_temp/state/stage1_refresh_report.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or PROJECT / "meds_database")
DOWNLOADS = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or PROJECT / "meds_downloads")
STATE_DIR = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp") / "state"
STATE = STATE_DIR / "stage1_refresh_state.json"
REPORT = STATE_DIR / "stage1_refresh_report.json"
PY = str(ROOT / ".venv-ocr" / "bin" / "python") if (ROOT / ".venv-ocr" / "bin" / "python").exists() else sys.executable
NODE = os.environ.get("NODE_BIN") or "node"
RETRY_DAYS = 7

# Türkçe + Latin + yaygın noktalama dışında kalan glifler (Sinhala, özel kullanım alanı, kutu karakterleri…)
BAD_CHARS = re.compile(r"[^\x09\x0a\x0d\x20-\x7eçğıöşüÇĞİÖŞÜâîûÂÎÛ–—’‘“”•…·°±×÷µαβγδλμπσΩ≤≥→←↑↓✓✔%½¼¾€]")
DROPPED_LETTER = re.compile(r"\b\w{1,3} \w{1,3}(ş|ğ|ı|ç)\w*\b")


def log(msg: str):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [stage1_refresh] {msg}", flush=True)


def run(cmd: list[str], timeout: int, cwd: Path = ROOT) -> tuple[int, str]:
    try:
        # docling yerleşim modelleri CPU'da: GPU'da Ollama ile aynı anda CUDA işi Xid 79'a yol açtı
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": ""}
        r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
        return r.returncode, (r.stdout + r.stderr)[-1500:]
    except subprocess.TimeoutExpired:
        return 124, "zaman aşımı"
    except Exception as e:  # noqa: BLE001
        return 1, str(e)


def faulty_sources(limit_report: int = 50) -> list[dict]:
    """Kaynak bazında OCR kalite puanı: düşük chunk kalitesi + bozuk glif oranı + harf düşmesi."""
    out = []
    for sp in glob.glob(str(DB / "sources" / "*.json")):
        try:
            s = json.load(open(sp, encoding="utf-8"))
        except Exception:
            continue
        cp = DB / "chunks" / f"{s['source_id']}.jsonl"
        if not cp.exists():
            continue
        n = low = bad = chars = dropped = 0
        with open(cp, encoding="utf-8") as f:
            for line in f:
                try:
                    c = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = c.get("text") or ""
                n += 1
                try:
                    if float(c.get("quality_score") or 1) < 0.6:
                        low += 1
                except ValueError:
                    pass
                chars += len(t)
                bad += len(BAD_CHARS.findall(t))
                dropped += len(DROPPED_LETTER.findall(t))
        if not n:
            continue
        bad_ratio = bad / max(1, chars)
        low_ratio = low / n
        drop_rate = dropped / n
        score = low_ratio * 0.5 + min(1, bad_ratio * 40) * 0.35 + min(1, drop_rate / 3) * 0.15
        if low_ratio >= 0.3 or bad_ratio >= 0.01 or (s.get("quality_score") or 1) < 0.7:
            out.append({"source_id": s["source_id"], "path": s.get("path"), "name": s.get("name"),
                        "quality_score": s.get("quality_score"), "dusuk_kalite_orani": round(low_ratio, 3),
                        "bozuk_glif_orani": round(bad_ratio, 4), "harf_dusmesi_chunk_basina": round(drop_rate, 2),
                        "oncelik": round(score, 3)})
    out.sort(key=lambda x: -x["oncelik"])
    return out


def find_download(path: str | None) -> Path | None:
    if not path:
        return None
    base = DOWNLOADS / path
    for ext in ("", ".pdf", ".pptx", ".ppt", ".docx"):
        p = Path(str(base) + ext)
        if p.is_file():
            return p
    hits = list(base.parent.glob(base.name + ".*")) if base.parent.exists() else []
    return hits[0] if hits else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-reocr", type=int, default=6, help="bir turda yeniden okunacak en fazla kaynak")
    ap.add_argument("--skip-download", action="store_true")
    ap.add_argument("--dry", action="store_true", help="indirme/OCR çalıştırmadan yalnızca tespit raporu")
    a = ap.parse_args()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state = json.load(open(STATE, encoding="utf-8")) if STATE.exists() else {"reocr": {}}
    report = {"baslangic": time.strftime("%Y-%m-%dT%H:%M:%S"), "indirme": None, "yeniden_ocr": []}

    if not a.skip_download and not a.dry:
        log("Drive envanteri güncelleniyor…")
        rc1, o1 = run([NODE, "scripts/pipeline/01-inventory.mjs"], timeout=1800)
        log(f"envanter rc={rc1}")
        log("Eksik / yeni dosyalar indiriliyor…")
        rc2, o2 = run([NODE, "scripts/pipeline/02-download.mjs"], timeout=3 * 3600)
        log(f"indirme rc={rc2}")
        report["indirme"] = {"envanter_rc": rc1, "indirme_rc": rc2, "cikti_sonu": o2[-600:]}

    faulty = faulty_sources()
    report["hatali_ocr_aday"] = len(faulty)
    report["hatali_ocr_ilk"] = faulty[:25]
    now = time.time()
    todo = []
    for f in faulty:
        last = state["reocr"].get(f["source_id"], {}).get("ts", 0)
        if now - last < RETRY_DAYS * 86400:
            continue
        p = find_download(f["path"])
        if p:
            todo.append((f, p))
        if len(todo) >= a.max_reocr:
            break
    log(f"hatalı OCR adayı: {len(faulty)}; bu tur yeniden okunacak: {len(todo)}")

    for f, p in todo:
        if a.dry:
            report["yeniden_ocr"].append({**f, "dosya": str(p), "durum": "dry"})
            continue
        log(f"yeniden OCR: {p.name} (öncelik {f['oncelik']})")
        gpu_ok = subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0
        cmd = [PY, "scripts/agents/read_document.py", str(p), "--force", "--docling"] + (["--vision"] if gpu_ok else [])
        rc, o = run(cmd, timeout=3600)
        state["reocr"][f["source_id"]] = {"ts": time.time(), "rc": rc, "yontem": "docling+vision" if gpu_ok else "docling (GPU yok)"}
        report["yeniden_ocr"].append({**f, "dosya": str(p), "rc": rc})
        json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    report["bitis"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    json.dump(report, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("tamamlandı; değişen temp1 dosyalarını pipeline_runner aşama 2→4'ten geçirecek.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
