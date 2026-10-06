#!/usr/bin/env python3
"""
Faz zinciri orkestratörü (meds-phases servisi olarak sürekli çalışır).

Bir tur:  Faz 5 → Faz 6 → Faz 6.5 → Faz 7.5 → Faz 8 → kanıtlı sözlük → Faz 9 → Faz 10 → Faz 11 → site yayını → Aşama 1 yenileme → (bekle) → yeni tur
  * Fazlar SIRAYLA çalışır; aynı anda yalnızca biri GPU/AI kullanır.
  * Her adımdan önce GPU soğuması beklenir (varsayılan < 90 °C).
  * Her adımın zaman aşımı vardır; hata zinciri durdurmaz, rapora yazılır ve sıradakine geçilir.
  * Aşama 1 yenileme (stage1_refresh.py): eksik dosyaları indirir, hatalı OCR'ı yeniden okur; değişen temp1
    dosyalarını sürekli çalışan pipeline_runner (meds-pipeline) aşama 2→3→4'ten geçirir.
  * Kilit dosyası ile tek örnek çalışır (watchdog ya da elle ikinci kez başlatma güvenli).

Durum/rapor: meds_temp/state/phase_cycle_state.json, kayıt: meds_temp/logs/phase_cycle.log
"""
from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
STATE = TEMP / "state" / "phase_cycle_state.json"
LOG = TEMP / "logs" / "phase_cycle.log"
LOCK = TEMP / "state" / "phase_cycle.lock"
PY = str(ROOT / ".venv-ocr" / "bin" / "python") if (ROOT / ".venv-ocr" / "bin" / "python").exists() else sys.executable
AI = ROOT / "scripts" / "advanced_ai"
AGENTS = ROOT / "scripts" / "agents"

MAX_TEMP = int(os.environ.get("MEDS_PHASE_MAX_TEMP", "89"))
PAUSE_BETWEEN_CYCLES = int(os.environ.get("MEDS_PHASE_PAUSE_SEC", str(20 * 60)))

# (anahtar, ad, komut, zaman aşımı sn)
STEPS = [
    ("faz5", "Faz 5 · Çoklu AI konsensüs", [PY, str(AI / "multi_ai_consensus_phase5.py")], 3 * 3600),
    ("faz6", "Faz 6 · Derin metadata (en çok 40 parti, kaldığı yerden)", [PY, str(AI / "deep_metadata_generator_phase6.py"), "--cycles", "40"], 2 * 3600),
    ("faz6_dogrulama", "Faz 6 doğrulama (CPU, modelsiz)", [PY, str(AI / "validate_phase6_metadata.py")], 900),
    ("faz6_5", "Faz 6.5 · Terim sözlüğü ve soru–slayt çapaları", [PY, str(AI / "thesaurus_anchor_phase6_5.py")], 3600),
    # Faz 7 (mikro-ajan hikâye) DEVRE DIŞI — 2026-10-05 denetimi: "hangisi yanlıştır" sorularında yanlış ifadeyi
    # doğru diye gerekçelendiriyor, hatalı cevap anahtarlarını pekiştiriyor, şık açıklamalarında uydurma bilgi var.
    # Ayrıntı: meds_database_v2/phase7_stories/KARANTINA.md. Düzeltilmeden zincire geri eklenmemeli.
    ("faz7_5", "Faz 7.5 · Müfredat slayt düzenleme", [PY, str(AI / "reconstruct_slides_phase7_5.py")], 3600),
    ("faz8", "Faz 8 · Soru–kazanım–konu–ders–kurul ağacı", [PY, str(AI / "phase8_curriculum_graph.py")], 3600),
    ("sozluk", "Kanıtlı sözlük (ders materyalinden kısaltma/yazım varyantı)", [PY, str(AI / "build_evidence_thesaurus.py")], 1800),
    ("faz9", "Faz 9 · Sözlük destekli müfredat ağacı", [PY, str(AI / "phase9_thesaurus_graph.py")], 3600),
    ("faz10", "Faz 10 · Kavram kimlikleri (Wikidata/UMLS) + kimlikli ağaç", [PY, str(AI / "phase10_concept_ids.py")], 3 * 3600),
    ("faz11", "Faz 11 · Soru–slayt eşleşmesi (BM25+kavram+e5+cross-encoder)", [PY, str(AI / "phase11_question_slide.py")], 3 * 3600),
    ("veritabani", "Veritabanına güvenli yükleme (derived/curriculum_links)", [PY, str(AI / "publish_to_database.py")], 900),
    ("yayin", "Site · Faz 5/6/6.5/8 analizlerini yayınla", [PY, str(AI / "export_phase_insights.py")], 900),
    ("asama1", "Aşama 1 · İndirme ve hatalı OCR yenileme", [PY, str(AGENTS / "stage1_refresh.py")], 6 * 3600),
    ("faz12", "Faz 12 · Ders notu temizleme (glif/OCR çöpü/üst-alt bilgi)", [PY, str(AI / "phase12_clean_notes.py")], 1800),
    ("hakem", "Hakem kuyruğu (alıntı doğrulamalı konu/slayt denetimi)", [PY, str(AI / "referee_queue.py"), "--max", "200"], 2 * 3600),
]


def log(msg: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [phase_cycle] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def gpu_temp() -> int | None:
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=5)
        return int(r.stdout.strip().splitlines()[0])
    except Exception:
        return None


def wait_cool():
    t = gpu_temp()
    waited = 0
    while t is not None and t >= MAX_TEMP and waited < 1800:
        if waited == 0:
            log(f"GPU {t} °C ≥ {MAX_TEMP} °C — soğuması bekleniyor")
        time.sleep(30)
        waited += 30
        t = gpu_temp()


def save_state(state: dict):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def run_step(key: str, name: str, cmd: list[str], timeout: int) -> dict:
    wait_cool()
    log(f"▶ {name}")
    t0 = time.time()
    out_path = TEMP / "logs" / f"phase_cycle_{key}.log"
    with open(out_path, "w", encoding="utf-8") as out:
        try:
            env = {**os.environ, "PYTHONUNBUFFERED": "1"}
            p = subprocess.Popen(cmd, env=env, cwd=str(ROOT), stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, 15)
            try:
                p.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, 9)
            rc = 124
        except Exception as e:  # noqa: BLE001
            log(f"  başlatılamadı: {e}")
            rc = 1
    sec = round(time.time() - t0)
    log(f"{'✓' if rc == 0 else '✗'} {name} — rc={rc}, {sec} sn (kayıt: {out_path.name})")
    return {"rc": rc, "sure_sn": sec, "bitis": time.strftime("%Y-%m-%dT%H:%M:%S")}


_START_MTIME = Path(__file__).stat().st_mtime


def main():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    lock = open(LOCK, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("phase_cycle zaten çalışıyor; çıkılıyor.")
        return 0
    once = "--once" in sys.argv
    state = json.load(open(STATE, encoding="utf-8")) if STATE.exists() else {"tur": 0, "adimlar": {}}
    while True:
        # Yarıda kalan tur varsa (servis yeniden başlatıldı / kesildi) aynı turda kalınan adımdan devam edilir.
        done = set(state.get("tur_tamamlanan") or [])
        if state.get("tur_bitis_yok"):
            log(f"===== Tur {state['tur']} kaldığı yerden sürüyor (tamamlanan: {', '.join(done) or '-'}) =====")
        else:
            state["tur"] = state.get("tur", 0) + 1
            state["tur_baslangic"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            state["tur_tamamlanan"], done = [], set()
            state["tur_bitis_yok"] = True
            save_state(state)
            log(f"===== Tur {state['tur']} başlıyor =====")
        for key, name, cmd, timeout in STEPS:
            if key in done:
                continue
            # Betik değiştiyse (yeni adım/ayar) adım aralarında kendini yeniden yükle; durum dosyası korunur
            if Path(__file__).stat().st_mtime > _START_MTIME:
                log("phase_cycle.py değişti → yeni kodla yeniden yükleniyor (kaldığı adımdan sürer)")
                lock.close()
                os.execv(sys.executable, [sys.executable] + sys.argv)
            if not Path(cmd[1]).exists():
                log(f"atlandı (betik yok): {cmd[1]}")
                continue
            state["aktif"] = key
            save_state(state)
            state.setdefault("adimlar", {})[key] = run_step(key, name, cmd, timeout)
            state.setdefault("tur_tamamlanan", []).append(key)
            save_state(state)
        state["aktif"] = None
        state["tur_bitis_yok"] = False
        state["tur_tamamlanan"] = []
        state["tur_bitis"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save_state(state)
        log(f"===== Tur {state['tur']} bitti; {PAUSE_BETWEEN_CYCLES // 60} dk sonra Faz 5'ten yeniden =====")
        if once:
            return 0
        time.sleep(PAUSE_BETWEEN_CYCLES)


if __name__ == "__main__":
    sys.exit(main())
