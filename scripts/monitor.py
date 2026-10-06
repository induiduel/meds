#!/usr/bin/env python3
"""
MedSoru Canlı Terminal Kokpiti ve Boru Hattı İzleyici (Terminal Dashboard v2)
Tüm aşamaları (Faz 1 - Faz 8, Aşama 1 yenileme) hedefleri ve canlı ilerlemeleriyle gösterir:
- Faz 1 (Ham Metin & OCR)
- Faz 2 (Türkçe Onarım & Soru Ayrıştırma)
- Faz 3 (RAG Chunking, BGE-M3 Vektörleme & Zenginleştirme)
- Faz 4 (Doğrulanmış meds_database Aktarımı)
- Faz 5 (Çoklu AI Konsensüsü & Slayt İğne-Delik Tespiti - meds_database_v2)
- Faz 6 (Derin Tıbbi Hiper-Metadata Motoru - Günlük 200 İstek Kotası)
- Donanım (GPU RTX 4060, VRAM, Sıcaklık) & Canlı Çalışan/Duran Servisler Tablosu
- Canlı Boru Hattı Log Akışı

Çalıştırma:
python3 scripts/monitor.py
"""
import curses
import json
import os
import subprocess
import time
from collections import deque
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_PARENT = ROOT_DIR.parent
TEMP_DIR = PROJECT_PARENT / "meds_temp"
STATE_FILE = TEMP_DIR / "state" / "pipeline_state.json"
STATUS_FILE = TEMP_DIR / "state" / "status.json"
LOG_FILE = TEMP_DIR / "logs" / "pipeline.log"
QUESTIONS_FILE = TEMP_DIR / "temp3" / "questions.jsonl"
REVIEW_FILE = TEMP_DIR / "temp3" / "review_queue.jsonl"

DOWNLOADS_DIR = PROJECT_PARENT / "meds_downloads"
TEMP1_DIR = TEMP_DIR / "temp1"
TEMP2_DIR = TEMP_DIR / "temp2"
TEMP3_DIR = TEMP_DIR / "temp3"
DB_DIR = PROJECT_PARENT / "meds_database"
DB_V2_DIR = PROJECT_PARENT / "meds_database_v2"
GRAPH_FILE = TEMP3_DIR / "advanced_ai" / "medical_knowledge_graph.json"
PHASE5_STATE_FILE = DB_V2_DIR / "phase5_consensus_state.json"
PHASE6_STATE_FILE = DB_V2_DIR / "deep_metadata" / "phase6_metadata_state.json"
PHASE7_V2_FILE = DB_V2_DIR / "phase7_v2" / "soru_metadata.jsonl"
PHASE8_DIR = TEMP_DIR / "phase8"
CYCLE_STATE_FILE = TEMP_DIR / "state" / "phase_cycle_state.json"
CYCLE_LOG_FILE = TEMP_DIR / "logs" / "phase_cycle.log"
STAGE1_REPORT_FILE = TEMP_DIR / "state" / "stage1_refresh_report.json"
SERVICES = ["meds-web", "meds-pipeline", "meds-phases", "meds-dashboard", "meds-downloads-watcher"]
CYCLE_NAMES = {"yayin": "Site yayını", "veritabani": "Veritabanı yüklemesi", "faz5": "Faz 5", "faz6": "Faz 6", "faz6_dogrulama": "Faz 6 doğrulama", "faz6_5": "Faz 6.5", "faz7_5": "Faz 7.5", "faz8": "Faz 8", "sozluk": "Kanıtlı sözlük", "faz9": "Faz 9", "faz10": "Faz 10", "faz11": "Faz 11", "hakem": "Hakem kuyruğu",
               "asama1": "Aşama 1"}


def systemd_active(name):
    try:
        r = subprocess.run(["systemctl", "--user", "is-active", name], capture_output=True, text=True, timeout=3)
        return r.stdout.strip() == "active"
    except Exception:
        return False


def phase7_v2_stats():
    st = {"n": 0, "tamam": 0, "kismi": 0, "celiski": 0}
    if not PHASE7_V2_FILE.exists():
        return st
    for line in open(PHASE7_V2_FILE, encoding="utf-8"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        st["n"] += 1
        st[o.get("durum")] = st.get(o.get("durum"), 0) + 1
        if (o.get("cevap_denetimi") or {}).get("sonuc") == "anahtar_celiskisi":
            st["celiski"] += 1
    return st


def phase8_stats():
    st = {"n": 0, "yuksek": 0, "orta": 0, "dusuk": 0}
    f = PHASE8_DIR / "soru_kazanim.jsonl"
    if not f.exists():
        return st
    for line in open(f, encoding="utf-8"):
        try:
            g = json.loads(line).get("guven")
        except Exception:
            continue
        st["n"] += 1
        st[g] = st.get(g, 0) + 1
    return st


def get_gpu_telemetry():
    try:
        cmd = [
            "nvidia-smi",
            "--query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu",
            "--format=csv,noheader,nounits"
        ]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
        parts = [p.strip() for p in out.split(",")]
        return {
            "name": parts[0],
            "mem_used": int(parts[1]),
            "mem_total": int(parts[2]),
            "util": int(parts[3]),
            "temp": int(parts[4])
        }
    except Exception:
        return {"name": "RTX 4060 (N/A)", "mem_used": 0, "mem_total": 8188, "util": 0, "temp": 0}


def get_recent_logs(path, num_lines=6):
    if not path.exists():
        return ["Log dosyası bekleniyor..."]
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        clean_lines = [l for l in lines if l.strip()]
        return clean_lines[-num_lines:] if clean_lines else ["Henüz log kaydı yok."]
    except Exception:
        return ["Log okuma hatası."]


def read_json_safe(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def fast_count_lines(path):
    if not path.exists():
        return 0
    try:
        with open(path, "rb") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def draw_bar(val, total, width=14):
    if total <= 0:
        return "[" + "░" * width + "] 0.0%"
    pct = min(1.0, max(0.0, val / total))
    filled = int(round(pct * width))
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct * 100:.1f}%"


def format_eta(seconds):
    if seconds is None or seconds < 0 or seconds > 86400 * 30:
        return "Hesaplanıyor..."
    sec = int(seconds)
    if sec < 60:
        return f"{sec} sn"
    elif sec < 3600:
        m = sec // 60
        s = sec % 60
        return f"{m} dk {s:02d} sn"
    else:
        h = sec // 3600
        m = (sec % 3600) // 60
        return f"{h} sa {m:02d} dk"


def get_process_statuses():
    """Çalışan veya duran temel servislerin durumunu döner."""
    found = {
        "pipeline_runner": False,
        "phase_cycle": False,
        "watchdog": False,
        "dashboard_8085": False,
        "ollama_server": False,
        "active_stage": "Boşta"
    }
    try:
        import psutil
        for p in psutil.process_iter(['name', 'cmdline']):
            cmd = " ".join(p.info['cmdline'] or [])
            if "pipeline_runner.py" in cmd:
                found["pipeline_runner"] = True
            elif "phase_cycle.py" in cmd:
                found["phase_cycle"] = True
            elif "watchdog.py" in cmd:
                found["watchdog"] = True
            elif "dashboard_server.py" in cmd:
                found["dashboard_8085"] = True
            elif "ollama" in cmd or "llama-server" in cmd:
                found["ollama_server"] = True
            
            if "stage2_clean.py" in cmd:
                found["active_stage"] = "Faz 2 (Temizlik)"
            elif "stage3_merge.py" in cmd:
                found["active_stage"] = "Faz 3 (Zenginleştirme)"
            elif "stage4_database.py" in cmd:
                found["active_stage"] = "Faz 4 (Aktarım)"
            elif "multi_ai_consensus_phase5.py" in cmd:
                found["active_stage"] = "Faz 5 (Konsensüs)"
            elif "deep_metadata_generator_phase6.py" in cmd:
                found["active_stage"] = "Faz 6 (Hiper-Metadata)"
            elif "thesaurus_anchor_phase6_5.py" in cmd:
                found["active_stage"] = "Faz 6.5 (Sözlük & Çapa)"
            elif "reconstruct_slides_phase7_5.py" in cmd:
                found["active_stage"] = "Faz 7.5 (Slayt Düzenleme)"
            elif "phase8_curriculum_graph.py" in cmd:
                found["active_stage"] = "Faz 8 (Kazanım Ağacı)"
            elif "stage1_refresh.py" in cmd or "read_document.py" in cmd:
                found["active_stage"] = "Aşama 1 (İndirme / OCR)"
            elif "phase7_question_metadata_v2.py" in cmd:
                found["active_stage"] = "Faz 7 v2 (elle, metadata)"
    except Exception:
        pass
    return found


# Faz zinciri tablosu: (anahtar, ad, birim, çıktı sayacı)
def _lines(p):
    return fast_count_lines(p) if p.exists() else 0


def _json_len(p, key=None):
    d = read_json_safe(p)
    if key:
        d = d.get(key) or {}
    return len(d) if isinstance(d, (dict, list)) else 0


PHASE_ROWS = [
    ("faz5", "Faz 5  Çoklu AI konsensüs", "soru", lambda: sum(_lines(f) for f in (DB_V2_DIR / "questions").glob("*.jsonl"))),
    ("faz6", "Faz 6  Derin metadata", "soru", lambda: read_json_safe(PHASE6_STATE_FILE).get("total_questions_processed", 0)),
    ("faz6_dogrulama", "Faz 6  doğrulama (CPU)", "soru", lambda: _lines(DB_V2_DIR / "deep_metadata_validated" / "dogrulama.jsonl")),
    ("faz6_5", "Faz 6.5 Sözlük & çapa", "çapa", lambda: _lines(DB_V2_DIR / "medical_thesaurus" / "phase6_5_question_slide_anchors.jsonl")),
    ("faz7_5", "Faz 7.5 Müfredat slaytları", "ders", lambda: len(list((DB_V2_DIR / "slide_reconstructed").glob("*.json")))),
    ("faz8", "Faz 8  Kazanım ağacı", "soru", lambda: _lines(TEMP_DIR / "phase8" / "soru_kazanim.jsonl")),
    ("sozluk", "Kanıtlı sözlük", "terim", lambda: _json_len(DB_V2_DIR / "evidence_thesaurus" / "kanitli_sozluk.json")),
    ("faz9", "Faz 9  Sözlüklü ağaç", "soru", lambda: _lines(TEMP_DIR / "phase9" / "soru_kazanim.jsonl")),
    ("faz10", "Faz 10 Kavram kimlikleri", "kavram", lambda: _json_len(DB_V2_DIR / "concept_ids" / "kavramlar.json")),
    ("faz11", "Faz 11 Soru–slayt eşleşmesi", "soru", lambda: _lines(TEMP_DIR / "phase11" / "soru_slayt.jsonl")),
    ("veritabani", "Veritabanı yüklemesi", "kayıt", lambda: read_json_safe(DB_DIR / "derived" / "curriculum_links" / "manifest.json").get("sayilar", {}).get("soru_slayt", 0)),
    ("yayin", "Site yayını", "soru", lambda: _json_len(DB_DIR / "derived" / "phase_insights" / "insights.json", "items")),
    ("asama1", "Aşama 1 İndirme & OCR", "kaynak", lambda: len(read_json_safe(STAGE1_REPORT_FILE).get("yeniden_ocr") or [])),
    ("hakem", "Hakem kuyruğu", "karar", lambda: _lines(TEMP_DIR / "hakem" / "kararlar.jsonl")),
]

ERROR_PAT = None


def recent_errors(limit=8):
    """Tüm günlüklerden son hata satırları (zaman damgalı satırlar öncelikli)."""
    import re as _re
    global ERROR_PAT
    if ERROR_PAT is None:
        ERROR_PAT = _re.compile(r"(Traceback|Error\b|ERROR|Exception|\bHATA\b|\bhata\b|✗|rc=[1-9]|başlatılamadı|zaman aşımı)")
    files = [CYCLE_LOG_FILE, LOG_FILE, TEMP_DIR / "logs" / "watchdog.out"] + sorted((TEMP_DIR / "logs").glob("phase_cycle_*.log"))
    out = []
    for f in files:
        if not f.exists():
            continue
        try:
            with open(f, "rb") as fh:
                fh.seek(0, 2)
                fh.seek(max(0, fh.tell() - 60000))
                lines = fh.read().decode("utf-8", "replace").splitlines()
        except Exception:
            continue
        for l in lines[-400:]:
            if ERROR_PAT.search(l) and "hata: 0" not in l and "rc=0" not in l:
                out.append((f.stat().st_mtime, f.name, l.strip()))
    out.sort(key=lambda x: x[0])
    seen, res = set(), []
    for _, name, l in reversed(out):
        k = l[-120:]
        if k in seen:
            continue
        seen.add(k)
        res.append(f"[{name}] {l}")
        if len(res) >= limit:
            break
    return res


def fmt_dur(sec):
    if sec is None:
        return "-"
    sec = int(sec)
    return f"{sec}s" if sec < 60 else (f"{sec // 60}dk{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}sa{(sec % 3600) // 60:02d}")


def render_dashboard(stdscr):
    try:
        curses.curs_set(0)
    except Exception:
        pass
    stdscr.nodelay(True)
    stdscr.timeout(1000)

    # Renk paleti
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)     # Başlıklar
    curses.init_pair(2, curses.COLOR_GREEN, -1)    # Başarılı / Tamam
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # İlerleme / Uyarı
    curses.init_pair(4, curses.COLOR_RED, -1)      # Hata / Yüksek Isı
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)  # Vurgu / Bölümler
    curses.init_pair(6, curses.COLOR_WHITE, -1)    # Normal metin

    # Hız ölçümü için zaman serisi
    speed_window = deque(maxlen=60)
    phase_hist = {}          # anahtar → deque[(zaman, sayı)] canlı hız için
    phase_counts = {}
    last_phase_check = 0
    errors_cache = []
    last_speed_str = "Hesaplanıyor..."
    last_eta_str = "Hesaplanıyor..."

    # Aşama sayaçlarını periyodik tazelemek için cache
    last_file_check_time = 0
    cached_counts = {
        "dl": 550,
        "t1": 536,
        "t2": 535, "t2_done": 536,
        "s3_src": 413, "s3_chunk": 413, "s3_vec": 410, "s3_src_done": 413,
        "q_verified": 2196, "q_review": 6798, "q_total": 8994,
        "db_q": 2735, "db_chk": 413,
        "kg_nodes": 6370, "kg_edges": 23896,
        "p5_verified": 0, "p5_blacklisted": 0, "p5_target": 2735,
        "p6_requests_today": 0, "p6_remaining": 200, "p6_total": 0
    }

    while True:
        try:
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q'), 27):  # 'q' veya ESC
                break

            stdscr.erase()
            h, w = stdscr.getmaxyx()
            now = time.time()

            # Verileri oku
            gpu = get_gpu_telemetry()
            p_state = read_json_safe(STATE_FILE)
            cur_prog = p_state.get("current_progress") or {}
            status_data = read_json_safe(STATUS_FILE)
            logs = get_recent_logs(LOG_FILE, num_lines=3) + get_recent_logs(CYCLE_LOG_FILE, num_lines=3)
            proc_status = get_process_statuses()

            # Dosya sayaçlarını her 3 saniyede bir hafifçe güncelle
            if now - last_file_check_time > 3.0:
                last_file_check_time = now
                try:
                    if DOWNLOADS_DIR.exists():
                        cached_counts["dl"] = len(list(DOWNLOADS_DIR.rglob("*.*")))
                    if TEMP1_DIR.exists():
                        cached_counts["t1"] = len(list(TEMP1_DIR.rglob("*.json")))
                    if TEMP2_DIR.exists():
                        cached_counts["t2"] = len(list(TEMP2_DIR.rglob("*.json")))
                    cached_counts["t2_done"] = len(p_state.get("stage2", {}))
                    
                    src_dir = TEMP3_DIR / "sources"
                    chk_dir = TEMP3_DIR / "chunks"
                    vec_dir = TEMP3_DIR / "vectors"
                    if src_dir.exists():
                        cached_counts["s3_src"] = len(list(src_dir.glob("*.json")))
                    if chk_dir.exists():
                        cached_counts["s3_chunk"] = len(list(chk_dir.glob("*.jsonl")))
                    if vec_dir.exists():
                        cached_counts["s3_vec"] = len(list(vec_dir.glob("*.npy")))
                    cached_counts["s3_src_done"] = len(p_state.get("stage3_src", {}))
                    
                    cached_counts["q_verified"] = fast_count_lines(QUESTIONS_FILE)
                    cached_counts["q_review"] = fast_count_lines(REVIEW_FILE)
                    cached_counts["q_total"] = cached_counts["q_verified"] + cached_counts["q_review"]

                    db_q_dir = DB_DIR / "questions"
                    db_chk_dir = DB_DIR / "chunks"
                    if db_q_dir.exists():
                        cached_counts["db_q"] = sum(fast_count_lines(f) for f in db_q_dir.glob("*.jsonl"))
                    if db_chk_dir.exists():
                        cached_counts["db_chk"] = len(list(db_chk_dir.glob("*.jsonl")))

                    if GRAPH_FILE.exists():
                        kg_json = read_json_safe(GRAPH_FILE)
                        cached_counts["kg_nodes"] = len(kg_json.get("nodes", []))
                        cached_counts["kg_edges"] = len(kg_json.get("edges", [])) or len(kg_json.get("links", []))

                    # Faz 5 Konsensüs durumu
                    p5_q_dir = DB_V2_DIR / "questions"
                    if p5_q_dir.exists():
                        cached_counts["p5_verified"] = sum(fast_count_lines(f) for f in p5_q_dir.glob("*.jsonl"))
                    p5_st = read_json_safe(PHASE5_STATE_FILE)
                    if p5_st:
                        cached_counts["p5_blacklisted"] = p5_st.get("total_blacklisted", 0)

                    # Faz 6 Derin Hiper-Metadata durumu (Çoklu AI & Dinamik Zamanlayıcı)
                    p6_st = read_json_safe(PHASE6_STATE_FILE)
                    today_str = date.today().isoformat()
                    if p6_st:
                        p6_q_done = p6_st.get("total_questions_processed", len(p6_st.get("processed_question_ids", [])))
                        p6_lec_done = p6_st.get("total_lectures_processed", len(p6_st.get("processed_lecture_sources", [])))
                        cached_counts["p6_q_done"] = p6_q_done
                        cached_counts["p6_lec_done"] = p6_lec_done
                        cached_counts["p6_total"] = p6_q_done

                    # Faz 6.5 Tıbbi Sözlük & Co-occurrence Anchor durumu
                    p65_anchors_file = DB_V2_DIR / "medical_thesaurus" / "phase6_5_question_slide_anchors.jsonl"
                    if p65_anchors_file.exists():
                        cached_counts["p65_anchors"] = fast_count_lines(p65_anchors_file)

                    p65_state = read_json_safe(DB_V2_DIR / "medical_thesaurus" / "phase6_5_state.json")
                    cached_counts["p65_terms"] = p65_state.get("thesaurus_terms", 0) if p65_state else 0

                    # Faz 7 v2 (zincir dışı) ve Faz 8, Aşama 1
                    cached_counts["p7v2"] = phase7_v2_stats()
                    cached_counts["p8"] = phase8_stats()
                    cached_counts["s1"] = read_json_safe(STAGE1_REPORT_FILE)

                    # Faz 7.5 Müfredat Slayt Düzenleme durumu
                    p75_dir = DB_V2_DIR / "slide_reconstructed"
                    if p75_dir.exists():
                        cached_counts["p75_done"] = len(list(p75_dir.glob("*.json")))

                except Exception:
                    pass

            total_q = cached_counts["q_total"]
            # Hız ve ETA Hesaplama
            if total_q > 0:
                speed_window.append((now, total_q))
                if len(speed_window) >= 2:
                    t_diff = speed_window[-1][0] - speed_window[0][0]
                    items_diff = speed_window[-1][1] - speed_window[0][1]
                    if t_diff >= 3.0 and items_diff > 0:
                        speed_per_sec = items_diff / t_diff
                        speed_per_min = speed_per_sec * 60.0
                        rem_items = max(0, 9200 - total_q)
                        eta_seconds = (rem_items / speed_per_sec) if speed_per_sec > 0 else 0
                        last_speed_str = f"{speed_per_min:.1f} soru/dk"
                        last_eta_str = format_eta(eta_seconds)
                    elif t_diff >= 12.0 and items_diff == 0:
                        last_speed_str = "Döngü Tamamlandı / Hazır"
                        last_eta_str = "0 sn"

            # ==========================================================
            # 1. BAŞLIK & DONANIM BİLGİSİ
            # ==========================================================
            title = " 🏥 MEDSORU AI: FAZ ZİNCİRİ & DONANIM TELEMETRİSİ "
            stdscr.addstr(0, max(0, (w - len(title)) // 2), title, curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(1, 2, "═" * (w - 4), curses.A_DIM)

            # GPU & VRAM Bilgi Kutusu
            gg = read_json_safe(TEMP_DIR / "state" / "gpu_guard.json")
            gg_txt = (f" | Koruyucu: {gg.get('durum', '?')} (ort. %{gg.get('ort_kullanim_30sn', 0)}, duraklatılan {gg.get('duraklatilan', 0)})"
                      if gg else " | Koruyucu: KAPALI")
            gpu_str = f"🎮 GPU: {gpu['name']} | Yük: %{gpu['util']:02d} | Sıcaklık: {gpu['temp']}°C (sınır <89, acil 95){gg_txt}"
            temp_attr = curses.color_pair(4 if gpu["temp"] >= 90 else (3 if gpu["temp"] >= 80 else 2))
            stdscr.addstr(2, 2, gpu_str[:max(10, w - 48)], curses.A_BOLD)

            vram_bar = draw_bar(gpu["mem_used"], gpu["mem_total"], width=14)
            stdscr.addstr(2, max(2, w - 42), f"VRAM: {gpu['mem_used']}MB/{gpu['mem_total']}MB {vram_bar}", temp_attr)

            stdscr.addstr(3, 2, "─" * (w - 4), curses.A_DIM)

            # ==========================================================
            # 2. SERVİS VE ÇALIŞMA DURUMU KOKPİTİ (ÇALIŞANLAR VE DURANLAR)
            # ==========================================================
            stdscr.addstr(4, 2, "⚙️  SERVİS VE İŞLEM DURUMLARI (Çalışan / Duran):", curses.color_pair(5) | curses.A_BOLD)

            def st_label(is_active):
                return "● ÇALIŞIYOR" if is_active else "○ DURDU"

            def st_attr(is_active):
                return curses.color_pair(2) if is_active else curses.color_pair(4)

            svc = {n: systemd_active(n) for n in SERVICES}
            p_run_str = f"Runner: {st_label(proc_status['pipeline_runner'])}"
            w_dog_str = f"Watchdog: {st_label(proc_status['watchdog'])}"
            d_srv_str = f"Kokpit(8085): {st_label(proc_status['dashboard_8085'])}"
            o_srv_str = f"Ollama GPU: {st_label(proc_status['ollama_server'])}"
            cur_act_str = f"Aktif İş: {proc_status['active_stage']}"

            stdscr.addstr(5, 4, p_run_str, st_attr(proc_status['pipeline_runner']) | curses.A_BOLD)
            stdscr.addstr(5, 26, w_dog_str, st_attr(proc_status['watchdog']) | curses.A_BOLD)
            stdscr.addstr(5, 48, d_srv_str, st_attr(proc_status['dashboard_8085']) | curses.A_BOLD)
            stdscr.addstr(5, 72, o_srv_str, st_attr(proc_status['ollama_server']) | curses.A_BOLD)
            stdscr.addstr(5, 96, cur_act_str[:w - 98], curses.color_pair(3) | curses.A_BOLD)

            x = 4
            for n in SERVICES:
                lbl = f"{n.replace('meds-', '')}: {'●' if svc[n] else '○'}  "
                if x + len(lbl) < w - 2:
                    stdscr.addstr(6, x, lbl, st_attr(svc[n]))
                x += len(lbl)
            cyc = read_json_safe(CYCLE_STATE_FILE)
            if cyc:
                aktif = CYCLE_NAMES.get(cyc.get("aktif"), cyc.get("aktif") or "bekliyor")
                hatali = [CYCLE_NAMES.get(k, k) for k, v in (cyc.get("adimlar") or {}).items() if v.get("rc") not in (0, None)]
                ztxt = f"| Zincir tur {cyc.get('tur', 0)}: {aktif}" + (f" | son hata: {', '.join(hatali)}" if hatali else "")
                if x < w - 10:
                    stdscr.addstr(6, x, ztxt[:w - x - 2], curses.color_pair(4 if hatali else 3))

            # ==========================================================
            # 3. AŞAMA 1–4 (pipeline) — kısa özet
            # ==========================================================
            y = 7
            stdscr.addstr(y, 2, "🚀 PIPELINE (Aşama 1–4):", curses.color_pair(1) | curses.A_BOLD)
            f1_done, f1_target = cached_counts["t1"], cached_counts["dl"]
            pipe = (f"İndirilen {f1_target} | OCR {f1_done} | temizlenen {cached_counts['t2']} | chunk {cached_counts['s3_chunk']} | "
                    f"vektör {cached_counts['s3_vec']} | DB soru {cached_counts['db_q']:,} | hakem kuyruğu {cached_counts['q_review']:,}")
            stdscr.addstr(y, 28, pipe[:max(0, w - 30)], curses.color_pair(2))
            y += 1

            # ==========================================================
            # 4. FAZ ZİNCİRİ: durum, son süre, çıktı, hız
            # ==========================================================
            if now - last_phase_check > 5:
                last_phase_check = now
                for key, _n, _u, fn in PHASE_ROWS:
                    try:
                        c = int(fn() or 0)
                    except Exception:
                        c = 0
                    phase_counts[key] = c
                    phase_hist.setdefault(key, deque(maxlen=120)).append((now, c))
                errors_cache = recent_errors(8)
            cyc = read_json_safe(CYCLE_STATE_FILE)
            steps = cyc.get("adimlar") or {}
            aktif = cyc.get("aktif")
            done_now = set(cyc.get("tur_tamamlanan") or [])
            stdscr.addstr(y, 2, f"🔁 FAZ ZİNCİRİ  (tur {cyc.get('tur', '-')}, aktif: {CYCLE_NAMES.get(aktif, aktif or 'bekliyor')})", curses.color_pair(1) | curses.A_BOLD)
            y += 1
            hdr = f"{'Faz':<30}{'Durum':<14}{'Son süre':<10}{'Çıktı':>10}  {'Hız':<22}{'Son bitiş':<20}"
            stdscr.addstr(y, 4, hdr[:w - 6], curses.A_DIM | curses.A_BOLD)
            y += 1
            for key, name, unit, _fn in PHASE_ROWS:
                if y >= h - 12:
                    break
                st = steps.get(key) or {}
                cnt = phase_counts.get(key, 0)
                hist = phase_hist.get(key) or []
                if key == aktif:
                    durum, attr = "● çalışıyor", curses.color_pair(3) | curses.A_BOLD
                    # canlı hız: son ~10 dk içindeki artış
                    pts = [p for p in hist if now - p[0] <= 600]
                    if len(pts) >= 2 and pts[-1][0] - pts[0][0] >= 20 and pts[-1][1] > pts[0][1]:
                        rate = (pts[-1][1] - pts[0][1]) / ((pts[-1][0] - pts[0][0]) / 60)
                        hiz = f"{rate:.1f} {unit}/dk (canlı)"
                    else:
                        hiz = "ölçülüyor…"
                    sure = "sürüyor"
                elif st.get("rc") not in (None, 0):
                    durum, attr, hiz, sure = f"✗ hata rc={st.get('rc')}", curses.color_pair(4) | curses.A_BOLD, "-", fmt_dur(st.get("sure_sn"))
                elif st:
                    durum = "✓ bu turda" if key in done_now else "✓ önceki tur"
                    attr = curses.color_pair(2)
                    sure = fmt_dur(st.get("sure_sn"))
                    s_ = st.get("sure_sn") or 0
                    hiz = f"{cnt / (s_ / 60):.0f} {unit}/dk (son tur)" if s_ >= 5 and cnt else ("anında" if cnt else "-")
                else:
                    durum, attr, hiz, sure = "○ henüz yok", curses.A_DIM, "-", "-"
                row = f"{name:<30}{durum:<14}{sure:<10}{cnt:>10,}  {hiz:<22}{(st.get('bitis') or '-').replace('T', ' ')[5:16]:<20}"
                stdscr.addstr(y, 4, row[:w - 6], attr)
                y += 1
            p7 = cached_counts.get("p7v2") or {}
            stdscr.addstr(y, 4, f"Faz 7 v2 (elle, zincir dışı): işlenen {p7.get('n', 0)} | anahtar çelişkisi {p7.get('celiski', 0)}   ·   Faz 7 (eski): karantinada"[:w - 6], curses.A_DIM)
            y += 1
            stdscr.addstr(y, 2, "─" * (w - 4), curses.A_DIM)
            y += 1

            # ==========================================================
            # 5. HATA KAYITLARI
            # ==========================================================
            stdscr.addstr(y, 2, f"🛑 SON HATA KAYITLARI ({len(errors_cache)}):", curses.color_pair(4) | curses.A_BOLD)
            y += 1
            if not errors_cache:
                stdscr.addstr(y, 4, "Hata yok ✓", curses.color_pair(2))
                y += 1
            for l in errors_cache:
                if y >= h - 8:
                    break
                stdscr.addstr(y, 4, l[:w - 6], curses.color_pair(4))
                y += 1
            stdscr.addstr(y, 2, "─" * (w - 4), curses.A_DIM)
            y += 1

            # ==========================================================
            # 6. CANLI LOG AKIŞI
            # ==========================================================
            stdscr.addstr(y, 2, "📜 CANLI LOG AKIŞI:", curses.color_pair(5) | curses.A_BOLD)
            line_y = y + 1
            s1 = cached_counts.get("s1") or {}
            if s1 and line_y < h - 2:
                stdscr.addstr(line_y, 4, f"Aşama 1 yenileme: hatalı OCR adayı {s1.get('hatali_ocr_aday', 0)} | son turda yeniden okunan {len(s1.get('yeniden_ocr') or [])} | bitiş {s1.get('bitis', '-')}"[:w - 6], curses.color_pair(1))
                line_y += 1
            for l in logs[-6:]:
                if line_y >= h - 2:
                    break
                attr = curses.color_pair(4 if "ERROR" in l else (3 if "WARN" in l else 0))
                stdscr.addstr(line_y, 4, l[:w - 6], attr)
                line_y += 1

            # ==========================================================
            # 7. ALT BİLGİ VE ÇIKIŞ
            # ==========================================================
            footer = " Çıkmak için 'q' tuşuna veya Ctrl+C'ye basın | Canlı Yenileme: 1 sn "
            stdscr.addstr(h - 1, max(0, (w - len(footer)) // 2), footer, curses.A_REVERSE)

            stdscr.refresh()
        except curses.error:
            pass


def main():
    try:
        curses.wrapper(render_dashboard)
    except KeyboardInterrupt:
        pass
    print("\n👋 MedSoru İzleyici kapatıldı.")


if __name__ == "__main__":
    main()
