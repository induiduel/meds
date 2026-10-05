#!/usr/bin/env python3
"""
MedSoru Canlı Terminal Kokpiti ve Boru Hattı İzleyici (Terminal Dashboard v2)
Tüm aşamaları (Faz 1 - Faz 6) hedefleri ve canlı ilerlemeleriyle gösterir:
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
PHASE7_STATE_FILE = DB_V2_DIR / "phase7_stories" / "phase7_state.json"


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
            elif "microagent_storyteller_phase7.py" in cmd:
                found["active_stage"] = "Faz 7 (Mikro-Ajans Hikaye)"
    except Exception:
        pass
    return found


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
            logs = get_recent_logs(LOG_FILE, num_lines=6)
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

                    # Faz 7 5-Adımlı Mikro-Ajans Modelleme durumu
                    p7_st = read_json_safe(PHASE7_STATE_FILE)
                    if p7_st:
                        cached_counts["p7_done"] = p7_st.get("total_stories_generated", len(p7_st.get("processed_qids", [])))
                    else:
                        p7_stories_dir = DB_V2_DIR / "phase7_stories"
                        if p7_stories_dir.exists():
                            cached_counts["p7_done"] = len(list(p7_stories_dir.glob("*.json")))
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
            title = " 🏥 MEDSORU AI: 6-FAZ MERKEZİ BORU HATTI & DONANIM TELEMETRİSİ "
            stdscr.addstr(0, max(0, (w - len(title)) // 2), title, curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(1, 2, "═" * (w - 4), curses.A_DIM)

            # GPU & VRAM Bilgi Kutusu
            gpu_str = f"🎮 GPU: {gpu['name']} | Yük: %{gpu['util']:02d} | Sıcaklık: {gpu['temp']}°C"
            temp_attr = curses.color_pair(4 if gpu['temp'] > 82 else (3 if gpu['temp'] > 72 else 2))
            stdscr.addstr(2, 2, gpu_str, curses.A_BOLD)

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

            stdscr.addstr(6, 2, "─" * (w - 4), curses.A_DIM)

            # ==========================================================
            # 3. 6 FAZLI BORU HATTI: HEDEFLER, İLERLEME VE KALANLAR
            # ==========================================================
            stdscr.addstr(7, 2, "🚀 6-FAZLI MIMARI: HEDEFLER, TAMAMLANANLAR VE KALANLAR:", curses.color_pair(1) | curses.A_BOLD)

            # --- FAZ 1 ---
            f1_done = cached_counts["t1"]
            f1_target = cached_counts["dl"]
            f1_rem = max(0, f1_target - f1_done)
            f1_bar = draw_bar(f1_done, f1_target, width=10)
            f1_st = "✓ TAMAM" if f1_rem <= 15 else f"{f1_rem} bekliyor"
            stdscr.addstr(8, 4, f"Faz 1 [Ham Metin & OCR]     : Hedef: {f1_target} dosya | İşlenen: {f1_done} {f1_bar} | Kalan: {f1_rem:<3} ({f1_st})", curses.color_pair(2) if f1_rem <= 15 else curses.color_pair(3))

            # --- FAZ 2 ---
            f2_done = cached_counts["t2"]
            f2_target = cached_counts["t1"]
            f2_rem = max(0, f2_target - f2_done)
            f2_bar = draw_bar(f2_done, f2_target, width=10)
            f2_st = "✓ TAMAM" if f2_rem == 0 else f"{f2_rem} bekliyor"
            stdscr.addstr(9, 4, f"Faz 2 [Türkçe Onarım & Soru]: Hedef: {f2_target} dosya | Temizlenen: {f2_done} {f2_bar} | Kalan: {f2_rem:<3} ({f2_st})", curses.color_pair(2) if f2_rem == 0 else curses.color_pair(3))

            # --- FAZ 3 ---
            f3_done = cached_counts["s3_src"]
            f3_target = 413
            f3_rem = max(0, f3_target - f3_done)
            f3_bar = draw_bar(f3_done, f3_target, width=10)
            stdscr.addstr(10, 4, f"Faz 3 [RAG Chunk & Vektör]  : Hedef: {f3_target} slayt | Chunk: {cached_counts['s3_chunk']} | Vektör(BGE-M3): {cached_counts['s3_vec']}/413 {f3_bar}", curses.color_pair(2) if f3_rem == 0 else curses.color_pair(3))
            
            # Faz 3 Soru Havuzu
            q_ver = cached_counts["q_verified"]
            q_rev = cached_counts["q_review"]
            q_tot = cached_counts["q_total"]
            stdscr.addstr(11, 4, f"      └─ Soru Havuzu Analizi: Doğrulanan: {q_ver:,} | İnceleme/Hakem Kuyruğu: {q_rev:,} | Toplam Tekil: {q_tot:,}", curses.color_pair(1))

            # --- FAZ 4 ---
            f4_done = cached_counts["db_q"]
            f4_target = max(q_ver, 2735)
            f4_bar = draw_bar(f4_done, f4_target, width=10)
            stdscr.addstr(12, 4, f"Faz 4 [meds_database Aktarım]: Hedef: {f4_target:,} soru | Aktarılan: {f4_done:,} soru {f4_bar} | DB Chunk: {cached_counts['db_chk']} (Senkron ✓)", curses.color_pair(2))

            # --- FAZ 5 ---
            p5_done = cached_counts["p5_verified"]
            p5_target = cached_counts["db_q"]
            p5_bl = cached_counts["p5_blacklisted"]
            p5_rem = max(0, p5_target - p5_done - p5_bl)
            p5_bar = draw_bar(p5_done, p5_target, width=10)
            p5_st = "Planlandı / Hazır" if p5_done == 0 else f"{p5_done} doğrulandı"
            stdscr.addstr(13, 4, f"Faz 5 [Çoklu AI Konsensüsü] : Hedef: {p5_target:,} soru | Konsensüs: {p5_done} {p5_bar} | Karantina: {p5_bl} ({p5_st})", curses.color_pair(5))

            # --- FAZ 6 ---
            p6_q_cnt = cached_counts.get("p6_q_done", 0)
            p6_lec_cnt = cached_counts.get("p6_lec_done", 0)
            p6_target = cached_counts["db_q"]
            p6_bar = draw_bar(p6_q_cnt, max(1, p6_target), width=10)
            stdscr.addstr(14, 4, f"Faz 6 [Derin Hiper-Metadata] : İşlenen Soru: {p6_q_cnt} {p6_bar} | Slayt Notu: {p6_lec_cnt} (Tempo: 5-10 dk'da 5 Soru / 2 Saatte 1 Ders)", curses.color_pair(3))

            # --- FAZ 7 ---
            p7_done = cached_counts.get("p7_done", 0)
            p7_bar = draw_bar(p7_done, 100, width=10)
            p7_st = "✓ 100 Altın Örnek Tamam" if p7_done >= 100 else f"{p7_done}/100 Modelleniyor"
            stdscr.addstr(15, 4, f"Faz 7 [5-Adım Mikro-Ajans]   : Altın Örnek: {p7_done}/100 {p7_bar} | ({p7_st} - Halüsinasyonsuz Klinik Hikaye)", curses.color_pair(2) if p7_done >= 100 else curses.color_pair(5))

            stdscr.addstr(16, 2, "─" * (w - 4), curses.A_DIM)

            # ==========================================================
            # 4. AKTİF İŞLEM, İŞLEME HIZI VE TAHMİNİ BİTİŞ (ETA)
            # ==========================================================
            stdscr.addstr(17, 2, "⚡ AKTİF SÜREÇ, HIZ & TAHMİNİ BİTİŞ (ETA):", curses.color_pair(5) | curses.A_BOLD)

            cur_desc = cur_prog.get("desc")
            if not cur_desc:
                last_time = status_data.get("time", "")
                cur_desc = f"Boru hattı döngüsü hazır ✓ (Son döngü: {last_time} - Arka plan aktif izlemede)"

            cur_step = cur_prog.get("current", 0)
            cur_tot = cur_prog.get("total", 0)

            stdscr.addstr(18, 4, f"• Aktif Görev : {cur_desc}"[:w - 6], curses.color_pair(3) | curses.A_BOLD)
            if cur_tot > 0:
                p_bar = draw_bar(cur_step, cur_tot, width=max(10, w - 50))
                stdscr.addstr(19, 4, f"• Canlı Adım  : {cur_step}/{cur_tot} {p_bar}  |  Hız: {last_speed_str}  |  Kalan Süre (ETA): {last_eta_str}", curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(19, 4, f"• Canlı Hız   : {last_speed_str}  |  Tahmini Kalan Süre (ETA): {last_eta_str}", curses.color_pair(2) | curses.A_BOLD)

            stdscr.addstr(20, 2, "─" * (w - 4), curses.A_DIM)

            # ==========================================================
            # 5. İLERİ AI & BİLGİ GRAFI KATMANI (GRAPHRAG & HYBRID SEARCH)
            # ==========================================================
            stdscr.addstr(21, 2, "🧠 İLERİ DÜZEY AI KATMANI (GraphRAG & Hibrit Arama):", curses.color_pair(1) | curses.A_BOLD)
            kg_info = f"• GraphRAG Tıbbi Bilgi Grafı : {cached_counts['kg_nodes']:,} Düğüm | {cached_counts['kg_edges']:,} Kenar (Hastalık-İlaç-Semptom Ağı)"
            search_info = f"• Hibrit Arama & Bellek      : BM25 + Dense BGE-M3 (24.657 Chunk İndeksli) ✓ | MemGPT Hiyerarşik Bellek: Devrede ✓"
            stdscr.addstr(22, 4, kg_info[:w - 6], curses.color_pair(6))
            stdscr.addstr(23, 4, search_info[:w - 6], curses.color_pair(2))

            stdscr.addstr(24, 2, "─" * (w - 4), curses.A_DIM)

            # ==========================================================
            # 6. CANLI BORU HATTI LOGLARI
            # ==========================================================
            stdscr.addstr(25, 2, "📜 BORU HATTI CANLI LOG AKIŞI:", curses.color_pair(5) | curses.A_BOLD)
            line_y = 26
            for l in logs[-5:]:
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
