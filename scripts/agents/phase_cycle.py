#!/usr/bin/env python3
"""
Faz zinciri orkestratörü (meds-phases servisi olarak sürekli çalışır).

Bir tur: Faz 5 → Faz 6 → Faz 6.5 → Faz 7.5 → Faz 8 → kanıtlı sözlük → Faz 9 → Faz 10 → Faz 11 → Faz 14 → site yayını → Aşama 1 yenileme → (bekle) → yeni tur
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
# Elle başlatma kuyruğu: panel (localhost:8085) adım anahtarlarını buraya ekler; zincir sıradaki adımdan önce bunları çalıştırır
QUEUE = TEMP / "state" / "phase_queue.json"
QUEUE_LOCK = TEMP / "state" / "phase_queue.lock"
PY = str(ROOT / ".venv-ocr" / "bin" / "python") if (ROOT / ".venv-ocr" / "bin" / "python").exists() else sys.executable
AI = ROOT / "scripts" / "advanced_ai"
AGENTS = ROOT / "scripts" / "agents"

MAX_TEMP = int(os.environ.get("MEDS_PHASE_MAX_TEMP", "89"))
PAUSE_BETWEEN_CYCLES = int(os.environ.get("MEDS_PHASE_PAUSE_SEC", str(20 * 60)))

# (anahtar, ad, komut, zaman aşımı sn)
STEPS = [
    ("faz5", "Faz 5 · Çoklu AI konsensüs", [PY, str(AI / "multi_ai_consensus_phase5.py")], 3 * 3600),
    ("faz6", "Faz 6 · Derin metadata (en çok 40 parti, kaldığı yerden)", [PY, str(AI / "deep_metadata_generator_phase6.py"), "--cycles", "40", "--max-seconds", "6000"], 2 * 3600),
    ("faz6_dogrulama", "Faz 6 doğrulama (CPU, modelsiz)", [PY, str(AI / "validate_phase6_metadata.py")], 900),
    ("faz6_5", "Faz 6.5 · Terim sözlüğü ve soru–slayt çapaları", [PY, str(AI / "thesaurus_anchor_phase6_5.py")], 3600),
    # Faz 7 (mikro-ajan hikâye) DEVRE DIŞI — 2026-10-05 denetimi: "hangisi yanlıştır" sorularında yanlış ifadeyi
    # doğru diye gerekçelendiriyor, hatalı cevap anahtarlarını pekiştiriyor, şık açıklamalarında uydurma bilgi var.
    # Ayrıntı: yedek/faz7_hikaye_silindi_20261007/phase7_stories/KARANTINA.md (Faz 7 hikâye üretimi 2026-10-07 silindi). Düzeltilmeden zincire geri eklenmemeli.
    ("faz7_5", "Faz 7.5 · Müfredat slayt düzenleme", [PY, str(AI / "reconstruct_slides_phase7_5.py")], 3600),
    ("faz8", "Faz 8 · Soru–kazanım–konu–ders–kurul ağacı", [PY, str(AI / "phase8_curriculum_graph.py")], 3600),
    ("sozluk", "Kanıtlı sözlük (ders materyalinden kısaltma/yazım varyantı)", [PY, str(AI / "build_evidence_thesaurus.py")], 1800),
    ("faz9", "Faz 9 · Sözlük destekli müfredat ağacı", [PY, str(AI / "phase9_thesaurus_graph.py")], 3600),
    ("faz10", "Faz 10 · Kavram kimlikleri (Wikidata/UMLS) + kimlikli ağaç", [PY, str(AI / "phase10_concept_ids.py")], 3 * 3600),
    ("faz11", "Faz 11 · Soru–slayt eşleşmesi (BM25+kavram+e5+cross-encoder)", [PY, str(AI / "phase11_question_slide.py")], 4 * 3600),
    ("ogren", "Öğren bağlantıları (soru → Öğren slaytı, eşikli)", [PY, str(AI / "learn_links.py")], 3 * 3600),
    ("yeniden_bolme", "Sınav çıktısını kuralla yeniden bölme", [PY, str(AI / "resplit_exam_printout.py")], 600),
    ("karantina", "Soru karantinası + onarım", [PY, str(AI / "quarantine_questions.py")], 600),
    ("veritabani", "Veritabanına güvenli yükleme (derived/curriculum_links)", [PY, str(AI / "publish_to_database.py")], 900),
    ("yayin", "Site · Faz 5/6/6.5/8 analizlerini yayınla", [PY, str(AI / "export_phase_insights.py")], 900),
    ("asama1", "Aşama 1 · İndirme ve hatalı OCR yenileme", [PY, str(AGENTS / "stage1_refresh.py")], 6 * 3600),
    ("faz12", "Faz 12 · Ders notu temizleme (glif/OCR çöpü/üst-alt bilgi)", [PY, str(AI / "phase12_clean_notes.py")], 1800),
    ("faz13", "Faz 13 · Tıbbi varlıklar (GLiNER + terminoloji)", [PY, str(AI / "phase13_entities.py")], 4 * 3600),
    ("faz14", "Faz 14 · Çıkmış soru redaksiyon önerileri (yerel model, inceleme kuyruğu)", [PY, str(AI / "phase14_past_question_editor.py"), "--limit", "10"], 2 * 3600),
    ("ortak", "Ortak veri deposu + RAG parçaları", [PY, str(AI / "build_unified_store.py")], 1800),
    ("hakem", "Hakem kuyruğu (alıntı doğrulamalı konu/slayt denetimi)", [PY, str(AI / "referee_queue.py"), "--max", "200"], 2 * 3600),
    ("yeni_veri", "Yeni veri hattı (yalnız yeni/değişen veri, gerekli adımlar)", [PY, str(AGENTS / "new_data_pipeline.py"), "--yeni"], 12 * 3600),
    ("bekleyen", "Bekleyen verileri bitir (Aşama 1–4 + değişen adımlar)", [PY, str(AGENTS / "new_data_pipeline.py"), "--bekleyen"], 12 * 3600),
    ("rag_yenile", "RAG + veritabanı yenileme (ortak depo, analizler, site arama dizini)", [PY, str(AGENTS / "rag_refresh.py")], 3600),
    ("ornek_soru", "Örnek çalışma soruları (müfredat, drive_root notları, günlük sınırlı, yalnız ücretsiz model)", [PY, str(AI / "practice_question_generator.py")], 3600),
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


def pop_queue() -> str | None:
    """Kuyruğun başındaki geçerli adımı al (kilitli okuma-yazma; panel aynı kilidi kullanır)."""
    if not QUEUE.exists():
        return None
    with open(QUEUE_LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            q = json.load(open(QUEUE, encoding="utf-8"))
        except Exception:
            q = []
        key = None
        while q and key is None:
            k = q.pop(0)
            key = k if any(k == s[0] for s in STEPS) else None
        tmp = QUEUE.with_suffix(".tmp")
        json.dump(q, open(tmp, "w", encoding="utf-8"))
        tmp.replace(QUEUE)
    return key


def run_queued(state: dict):
    """Elle istenen adımlar: tur sırasını bozmaz, tamamlanan listesine eklenmez."""
    wait_if_paused()
    while (key := pop_queue()):
        _, name, cmd, timeout = next(s for s in STEPS if s[0] == key)
        log(f"elle istendi: {name}")
        state["aktif"] = key
        save_state(state)
        c, t = effective(key, cmd, timeout)
        res = run_step(key, name, c, t)
        res["elle"] = True
        record(state, key, res)
        state["aktif"] = None
        save_state(state)


# Panelden (localhost:8085) düzenlenen adım ayarları: {anahtar: {"kapali": bool, "zaman_asimi_dk": int, "ek_arg": "…"}}
SETTINGS = TEMP / "state" / "phase_settings.json"


def step_settings(key: str) -> dict:
    try:
        return (json.load(open(SETTINGS, encoding="utf-8")) or {}).get(key) or {}
    except Exception:
        return {}


def effective(key: str, cmd: list[str], timeout: int) -> tuple[list[str], int]:
    """Panel ayarlarını uygula: ek argümanlar komutun sonuna, zaman aşımı dakika cinsinden."""
    import shlex
    st = step_settings(key)
    extra = shlex.split(st.get("ek_arg") or "") if st.get("ek_arg") else []
    to = int(st["zaman_asimi_dk"]) * 60 if str(st.get("zaman_asimi_dk") or "").isdigit() and int(st["zaman_asimi_dk"]) > 0 else timeout
    return cmd + extra, to


# Panelden "Tümünü durdur": bu dosya varken zincir yeni adım başlatmaz (çalışan adımı panel sonlandırır)
PAUSE = TEMP / "state" / "phase_pause.json"


def wait_if_paused():
    noted = False
    while PAUSE.exists():
        if not noted:
            log("⏸ tüm fazlar panelden durduruldu; devam komutu bekleniyor")
            noted = True
        time.sleep(15)
    if noted:
        log("▶ devam ettiriliyor")


AUTOMATION = TEMP / "state" / "otomasyon.json"


def automation() -> dict:
    """Panel anahtarları: otomatik_gecis (yeni dosya → yeni veri hattı), tam_tur (tüm fazlar sırayla, eski davranış)."""
    try:
        return json.loads(AUTOMATION.read_text(encoding="utf-8"))
    except Exception:
        return {}


def record(state: dict, key: str, res: dict):
    """Son sonucu ve son 10 çalışmanın geçmişini durum dosyasına yaz."""
    state.setdefault("adimlar", {})[key] = res
    hist = state.setdefault("gecmis", {}).setdefault(key, [])
    hist.append(res)
    del hist[:-10]


def save_state(state: dict):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# GPU'yu tek başına kullanabilecek adımlar: başlamadan önce Ollama modeli GPU belleğinden boşaltılır (aynı anda iki CUDA
# işi 2026-10-06'da "GPU fallen off the bus" hatasına yol açtı). GPU koruyucu (meds-gpuguard) bu adımları da izler.
# 2026-10-06 16:5x: Ollama boşaltılmış, GPU'da TEK BAŞINA çalışan PyTorch işi (learn_links, e5/cross-encoder) yine
# "GPU fallen off the bus" (Xid 79) verdi → sorun eşzamanlılık değil, bu kartta PyTorch CUDA işi. PyTorch adımları CPU'da.
GPU_STEPS: set = set()
OLLAMA = os.environ.get("OLLAMA_URL") or "http://127.0.0.1:11434"


def unload_ollama() -> bool:
    import urllib.request
    try:
        ps = json.loads(urllib.request.urlopen(f"{OLLAMA}/api/ps", timeout=10).read()).get("models") or []
        for m in ps:
            body = json.dumps({"model": m.get("name"), "keep_alive": 0}).encode()
            urllib.request.urlopen(urllib.request.Request(f"{OLLAMA}/api/generate", data=body,
                                                          headers={"Content-Type": "application/json"}), timeout=60).read()
        time.sleep(3)
        apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader"], capture_output=True, text=True, timeout=10)
        return apps.returncode == 0 and not apps.stdout.strip()
    except Exception:
        return False


def run_step(key: str, name: str, cmd: list[str], timeout: int) -> dict:
    wait_cool()
    gpu_free = False
    if key in GPU_STEPS and gpu_temp() is not None:
        gpu_free = unload_ollama()
        log(f"  GPU {'boş — adım GPU kullanacak' if gpu_free else 'boşaltılamadı — adım CPU kullanacak'}")
    log(f"▶ {name}")
    t0 = time.time()
    out_path = TEMP / "logs" / f"phase_cycle_{key}.log"
    with open(out_path, "w", encoding="utf-8") as out:
        try:
            env = {**os.environ, "PYTHONUNBUFFERED": "1"}
            if key in GPU_STEPS:
                env.update({"MEDS_FAZ11_DEVICE": "auto" if gpu_free else "cpu", "MEDS_GPU_OK": "1" if gpu_free else "0"})
                if not gpu_free:
                    env["CUDA_VISIBLE_DEVICES"] = ""
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
    # Elle kip (varsayılan): bir faz bitince sıradaki KENDİLİĞİNDEN başlamaz; yalnız panelden kuyruğa eklenen
    # ("Başlat") adımlar çalışır. Eski otomatik tur davranışı: .env MEDS_PHASE_AUTO=1.
    if not automation().get("tam_tur") and os.environ.get("MEDS_PHASE_AUTO") != "1":
        state["aktif"] = None
        state["kip"] = "elle"
        save_state(state)
        log("elle kip: fazlar yalnız panelden başlatılınca çalışır (otomatik geçiş kapalı)")
        while True:
            if Path(__file__).stat().st_mtime > _START_MTIME:
                log("phase_cycle.py değişti → yeni kodla yeniden yükleniyor")
                lock.close()
                os.execv(sys.executable, [sys.executable] + sys.argv)
            run_queued(state)
            if once:
                return 0
            time.sleep(10)
    state["kip"] = "otomatik"
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
            if key == "faz14":
                continue                                       # Faz 14 asla otomatik başlamaz; yalnız panelden elle
            # Betik değiştiyse (yeni adım/ayar) adım aralarında kendini yeniden yükle; durum dosyası korunur
            if Path(__file__).stat().st_mtime > _START_MTIME:
                log("phase_cycle.py değişti → yeni kodla yeniden yükleniyor (kaldığı adımdan sürer)")
                lock.close()
                os.execv(sys.executable, [sys.executable] + sys.argv)
            run_queued(state)
            wait_if_paused()
            if not Path(cmd[1]).exists():
                log(f"atlandı (betik yok): {cmd[1]}")
                continue
            if step_settings(key).get("kapali"):
                log(f"atlandı (panelden kapatıldı): {name}")
                state.setdefault("tur_tamamlanan", []).append(key)
                save_state(state)
                continue
            state["aktif"] = key
            save_state(state)
            c, t = effective(key, cmd, timeout)
            record(state, key, run_step(key, name, c, t))
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
        end = time.time() + PAUSE_BETWEEN_CYCLES
        while time.time() < end:          # tur arasında da elle istenen adımlar beklemeden çalışır
            run_queued(state)
            time.sleep(30)


if __name__ == "__main__":
    sys.exit(main())
