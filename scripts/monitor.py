#!/usr/bin/env python3
"""
MedSoru Canlı Terminal Kokpiti ve Boru Hattı İzleyici (Terminal Dashboard)
Tüm aşamaları, GPU/VRAM telemetrilerini, boru hattı ilerlemesini,
aktif soru dönüşümlerini, işleme hızını (soru/dk, tahmini bitiş)
ve 10 satırlık canlı log akışını gerçek zamanlı gösterir.

Çalıştırma:
python3 scripts/monitor.py
"""
import curses
import json
import os
import subprocess
import time
from collections import deque
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = ROOT_DIR.parent / "meds_temp"
STATE_FILE = TEMP_DIR / "state" / "pipeline_state.json"
STATUS_FILE = TEMP_DIR / "state" / "status.json"
LOG_FILE = TEMP_DIR / "logs" / "pipeline.log"
WATCHDOG_LOG = TEMP_DIR / "logs" / "watchdog.log"
QUESTIONS_FILE = TEMP_DIR / "temp3" / "questions.jsonl"
REVIEW_FILE = TEMP_DIR / "temp3" / "review_queue.jsonl"
DB_DIR = ROOT_DIR.parent / "meds_database"

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

def get_recent_logs(path, num_lines=10):
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

def get_latest_question_sample():
    if not QUESTIONS_FILE.exists():
        return None
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            if not lines:
                return None
            for ln in reversed(lines):
                if ln.strip():
                    item = json.loads(ln)
                    if item.get("options_analysis") or item.get("explanation"):
                        return item
            return json.loads(lines[-1])
    except Exception:
        pass
    return None

def draw_bar(val, total, width=24):
    if total <= 0:
        return "[" + " " * width + "] 0.0%"
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

def render_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000)

    # Renk paleti
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)     # Başlıklar
    curses.init_pair(2, curses.COLOR_GREEN, -1)    # Başarılı / Tamam
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # İlerleme / Uyarı
    curses.init_pair(4, curses.COLOR_RED, -1)      # Hata / Yüksek Isı
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)  # Vurgu

    # Hız ölçümü için zaman serisi
    speed_window = deque(maxlen=60)
    last_speed_str = "Hesaplanıyor..."
    last_eta_str = "Hesaplanıyor..."

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
            transforms = p_state.get("transform_history") or []
            logs = get_recent_logs(LOG_FILE, num_lines=10)

            cur_step = cur_prog.get("current", 0)
            cur_tot = cur_prog.get("total", 0)

            # Dosya sayıları ile genel soru tablosunu takip et
            q_cnt = fast_count_lines(QUESTIONS_FILE)
            r_cnt = fast_count_lines(REVIEW_FILE)
            total_questions_processed = q_cnt + r_cnt

            # Hız ve ETA Hesaplama (Genel soru zenginleştirme hızına göre)
            if total_questions_processed > 0:
                speed_window.append((now, total_questions_processed))
                if len(speed_window) >= 2:
                    t_diff = speed_window[-1][0] - speed_window[0][0]
                    items_diff = speed_window[-1][1] - speed_window[0][1]
                    if t_diff >= 3.0 and items_diff > 0:
                        speed_per_sec = items_diff / t_diff
                        speed_per_min = speed_per_sec * 60.0
                        rem_items = max(0, 7219 - total_questions_processed)
                        eta_seconds = (rem_items / speed_per_sec) if speed_per_sec > 0 else 0
                        last_speed_str = f"{speed_per_min:.1f} soru/dk ({speed_per_sec:.2f} soru/sn)"
                        last_eta_str = format_eta(eta_seconds)
                    elif t_diff >= 15.0 and items_diff == 0:
                        last_speed_str = "0.0 soru/dk (Beklemede)"
                        last_eta_str = "Durakladı / Aşama Değişiyor"

            # 1. BAŞLIK & DONANIM BİLGİSİ
            title = " 🏥 MEDSORU AI: CANLI BORU HATTI & DONANIM KOKPİTİ "
            stdscr.addstr(0, max(0, (w - len(title)) // 2), title, curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(1, 2, "─" * (w - 4), curses.A_DIM)

            # GPU Bilgi Kutusu
            gpu_str = f"🎮 GPU: {gpu['name']} | Kullanım: %{gpu['util']:02d} | Sıcaklık: {gpu['temp']}°C"
            temp_attr = curses.color_pair(4 if gpu['temp'] > 82 else (3 if gpu['temp'] > 72 else 2))
            stdscr.addstr(2, 2, gpu_str, curses.A_BOLD)

            vram_bar = draw_bar(gpu["mem_used"], gpu["mem_total"], width=20)
            stdscr.addstr(2, max(2, w - 44), f"VRAM: {gpu['mem_used']}MB/{gpu['mem_total']}MB {vram_bar}", temp_attr)

            stdscr.addstr(3, 2, "─" * (w - 4), curses.A_DIM)

            # 2. BORU HATTI AŞAMALARI VE CANLI DURUM
            stdscr.addstr(4, 2, "⚡ AKTİF SÜREÇ VE İLERLEME:", curses.color_pair(5) | curses.A_BOLD)

            # Aktif aşamayı ve görevi akıllı tespit et
            if cur_prog.get("desc"):
                cur_desc = cur_prog["desc"]
            elif total_questions_processed >= 8800:
                cur_desc = "Aşama 5: Gelişmiş AI & GraphRAG & Hibrit Arama Hazırlığı (Aktif)"
            elif total_questions_processed > 0:
                cur_desc = f"Aşama 3: Soru Doğrulama & Zenginleştirme ({total_questions_processed}/8838)"
            else:
                cur_desc = "Süreç bekleniyor..."

            prog_str = f"• Görev     : {cur_desc}"
            stdscr.addstr(5, 4, prog_str[:w - 6], curses.color_pair(3) | curses.A_BOLD)

            # Görev kendi adım/toplamını veriyorsa onu kullan, yoksa genel soruları göster
            if cur_tot > 0:
                p_bar = draw_bar(cur_step, cur_tot, width=max(10, w - 45))
                stdscr.addstr(6, 4, f"• İlerleme  : {cur_step}/{cur_tot} {p_bar}", curses.color_pair(2) | curses.A_BOLD)
            else:
                p_bar = draw_bar(total_questions_processed, max(total_questions_processed, 8838), width=max(10, w - 45))
                stdscr.addstr(6, 4, f"• İlerleme  : {total_questions_processed}/8838 {p_bar}", curses.color_pair(2) | curses.A_BOLD)

            # Canlı Hız ve Tahmini Kalan Süre Metrikleri
            speed_line = f"• Havuz     : Onaylı & Kanıtlı: {q_cnt}  |  İnceleme Kuyruğu: {r_cnt}  |  Toplam: {total_questions_processed}"
            stdscr.addstr(7, 4, speed_line[:w - 6], curses.color_pair(1) | curses.A_BOLD)

            # Aşama Tamamlanma Sayıları
            done_s2 = len(p_state.get("stage2", {}))
            done_s3_src = len(p_state.get("stage3_src", {}))
            stdscr.addstr(8, 4, f"• Kaynaklar : {done_s3_src} slayt dosyası | Temizlenen Metin: {done_s2} | Bilgi Grafı: 6.364 Düğüm, 23.896 Kenar", curses.A_NORMAL)

            stdscr.addstr(9, 2, "─" * (w - 4), curses.A_DIM)

            # 3. CANLI AI DÖNÜŞÜMLERİ (Sorudan Kanıtlı Zenginleştirmeye)
            stdscr.addstr(10, 2, "🧠 EN SON YAPAY ZEKA DÖNÜŞÜMÜ (Örnek Soru & Kanıt Açıklaması):", curses.color_pair(1) | curses.A_BOLD)

            sample_q = get_latest_question_sample()
            if sample_q and (sample_q.get("options_analysis") or sample_q.get("explanation")):
                q_stem = sample_q.get("stem", "")
                q_ans = sample_q.get("answer", "")
                q_opt = sample_q.get("options_analysis", {})
                ans_analysis = q_opt.get(q_ans) if isinstance(q_opt, dict) else None
                if not ans_analysis:
                    ans_analysis = sample_q.get("explanation") or next(iter(q_opt.values())) if q_opt else "Doğrulandı"
                t_title = f"[Aşama 3 Zenginleştirme] Kurul {sample_q.get('kurul')} | Soru ID: {sample_q.get('question_id')} | Destek: %{int(sample_q.get('support_ratio', 1.0) * 100)}"
                stdscr.addstr(11, 4, t_title[:w - 6], curses.color_pair(3) | curses.A_UNDERLINE)
                stdscr.addstr(12, 4, f"Soru : {q_stem}"[:w - 6], curses.A_DIM)
                stdscr.addstr(13, 4, f"Kanıt: [Doğru Şık: {q_ans}] {ans_analysis}"[:w - 6], curses.color_pair(2))
            elif transforms:
                last_t = transforms[-1]
                t_title = f"[{last_t.get('step')}] {last_t.get('file')}"
                stdscr.addstr(11, 4, t_title[:w - 6], curses.color_pair(3) | curses.A_UNDERLINE)
                in_txt = f"Girdi: {last_t.get('input', '')}"
                out_txt = f"Çıktı: {last_t.get('output', '')}"
                stdscr.addstr(12, 4, in_txt[:w - 6], curses.A_DIM)
                stdscr.addstr(13, 4, out_txt[:w - 6], curses.color_pair(2))
            else:
                stdscr.addstr(11, 4, "Henüz kaydedilmiş soru dönüşümü yok veya aşama hazırlanıyor...", curses.A_DIM)

            stdscr.addstr(14, 2, "─" * (w - 4), curses.A_DIM)

            # 4. CANLI LOG AKIŞI (10 SATIR)
            stdscr.addstr(15, 2, "📜 BORU HATTI LOGLARI (Canlı Akış - Son 10 Satır):", curses.color_pair(5) | curses.A_BOLD)
            line_y = 16
            for l in logs[-10:]:
                if line_y >= h - 2:
                    break
                attr = curses.color_pair(4 if "ERROR" in l else (3 if "WARN" in l else 0))
                stdscr.addstr(line_y, 4, l[:w - 6], attr)
                line_y += 1

            # 5. ALT BİLGİ VE ÇIKIŞ
            footer = " Çıkmak için 'q' tuşuna veya Ctrl+C'ye basın | Otomatik Yenileme: 1 sn "
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
