#!/usr/bin/env python3
"""
Yeni veri hattı — Drive'dan gelen YENİ çıkmış soru / ders notu için yalnız GEREKLİ adımları, yalnız girdisi değiştiyse çalıştırır.

Adım sırası (yeni veri için gerekli olanlar): oku → ayrıştır → birleştir → veritabanına aktar → ders notu temizliği (Faz 12)
→ ortak depo/RAG → Faz 8 → kanıtlı sözlük → Faz 9 → Faz 10 → Faz 11 → Öğren → yeniden bölme → karantina → müfredat
çözümleme → veritabanı yayını → site analizleri → Faz 13 → site arama dizini.
Hat dışı (yeni veri için elzem değil / ağır / bulut): Faz 5, 6, 6.5, 7.5, 14, hakem, örnek soru (panelden ayrıca çalışır).

Tekrar yok:
  * Aşama 1–3 dosya özetine (sha) göre değişmeyeni zaten atlar; Faz 13 işlenmiş soruyu atlar.
  * Her adımın GİRDİ parmak izi (dosya sayısı + toplam boyut + en son değişiklik) saklanır; değişmediyse adım çalışmaz.
  * Aşama 2–4 ortak kilitle korunur (pipeline_runner ile aynı anda çalışmaz).
Kip: --yeni (varsayılan; yalnız değişen girdiler) · --bekleyen (işlenmemiş indirme/temp1/temp2 kalmayana kadar Aşama 1–4,
     sonra değişen adımlar) · --hepsi (parmak izine bakmadan; yalnız gerektiğinde) · --durum (çalıştırmadan rapor)
Yalnız ücretsiz bulut / yerel: Aşama 1–2 yerel; LLM gerektiren adımlar lib.chat (ücretsiz zincir) kullanır.
Durum: meds_temp/state/yeni_veri_hatti.json · Günlük: meds_temp/logs/yeni_veri_hatti.log
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or PROJECT / "meds_database")
DL = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or PROJECT / "meds_downloads")
STATE = TEMP / "state" / "yeni_veri_hatti.json"
LOG = TEMP / "logs" / "yeni_veri_hatti.log"
STAGE_LOCK = TEMP / "state" / "asama_kilidi.lock"
PY = str(ROOT / ".venv-ocr" / "bin" / "python")
AG = ROOT / "scripts" / "agents"
AI = ROOT / "scripts" / "advanced_ai"
V2 = PROJECT / "meds_database_v2"
PAST = ROOT / "data" / "pastQuestions.json"

# (anahtar, ad, komut, girdi yolları, zaman aşımı sn, aşama kilidi gerekir mi)
STEPS = [
    ("oku", "Aşama 1 · Belge okuma (yeni dosyalar)", [PY, str(AG / "read_document.py"), str(DL)], [DL], 6 * 3600, True),
    ("ayristir", "Aşama 2 · Onarım + soru ayrıştırma", [PY, str(AG / "stage2_clean.py")], [TEMP / "temp1"], 3 * 3600, True),
    ("birlestir", "Aşama 3 · Birleştirme + RAG", [PY, str(AG / "stage3_merge.py"), "--skip-enrich"], [TEMP / "temp2"], 3 * 3600, True),
    ("aktar", "Aşama 4 · Veritabanına aktarım", [PY, str(AG / "stage4_database.py")], [TEMP / "temp3"], 3600, True),
    ("faz12", "Faz 12 · Ders notu temizliği", [PY, str(AI / "phase12_clean_notes.py")], [DB / "chunks"], 1800, False),
    ("ortak", "Ortak depo + RAG parçaları", [PY, str(AI / "build_unified_store.py")], [DB / "chunks", DB / "derived" / "clean_notes", DB / "questions"], 1800, False),
    ("faz8", "Faz 8 · Müfredat ağacı", [PY, str(AI / "phase8_curriculum_graph.py")], [DB / "chunks", DB / "questions", DB / "taxonomy"], 3600, False),
    ("sozluk", "Kanıtlı sözlük", [PY, str(AI / "build_evidence_thesaurus.py")], [DB / "chunks"], 1800, False),
    ("faz9", "Faz 9 · Sözlük destekli ağaç", [PY, str(AI / "phase9_thesaurus_graph.py")], [DB / "derived" / "phase8", V2 / "evidence_thesaurus"], 3600, False),
    ("faz10", "Faz 10 · Kavram kimlikleri", [PY, str(AI / "phase10_concept_ids.py")], [TEMP / "phase9", V2 / "evidence_thesaurus"], 3 * 3600, False),
    ("faz11", "Faz 11 · Soru–slayt eşleşmesi", [PY, str(AI / "phase11_question_slide.py")], [DB / "chunks", DB / "questions", TEMP / "phase10"], 4 * 3600, False),
    ("ogren", "Öğren bağlantıları", [PY, str(AI / "learn_links.py")], [PAST, ROOT / "src" / "data"], 3 * 3600, False),
    ("yeniden_bolme", "Sınav çıktısı yeniden bölme", [PY, str(AI / "resplit_exam_printout.py")], [DB / "questions"], 600, False),
    ("karantina", "Karantina + onarım", [PY, str(AI / "quarantine_questions.py")], [PAST, DB / "derived" / "resplit"], 600, False),
    ("mufredat", "Müfredat çözümleme (sınav başlığı)", [PY, str(AI / "curriculum_resolve.py")], [PAST, DB / "derived" / "phase8"], 900, False),
    ("veritabani", "Veritabanına yayın", [PY, str(AI / "publish_to_database.py")], [TEMP / "phase10", TEMP / "phase11", TEMP / "hakem"], 900, False),
    ("yayin", "Site analizleri", [PY, str(AI / "export_phase_insights.py")], [DB / "derived" / "curriculum_links", TEMP / "phase11"], 900, False),
    ("faz13", "Faz 13 · Tıbbi varlıklar (yalnız yeni sorular)", [PY, str(AI / "phase13_entities.py")], [PAST], 4 * 3600, False),
]
# Bir adım çalıştıysa site arama dizini en sonda bir kez yenilenir
SITE_REFRESH = ["systemctl", "--user", "restart", "meds-web"]


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [yeni_veri] {m}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fingerprint(paths: list[Path]) -> str:
    """Girdi parmak izi: dosya sayısı + toplam boyut + en son değişiklik (içerik okunmaz; hızlı)."""
    n = size = 0
    newest = 0.0
    for p in paths:
        if p.is_file():
            st = p.stat()
            n, size, newest = n + 1, size + st.st_size, max(newest, st.st_mtime)
        elif p.is_dir():
            for f in p.rglob("*"):
                # durum/manifest dosyaları (_manifest.json, _downloads.json, *.tmp…) veri değildir
                if f.is_file() and not f.name.startswith("_") and not f.name.endswith((".tmp", ".lock", ".pid")):
                    st = f.stat()
                    n, size, newest = n + 1, size + st.st_size, max(newest, st.st_mtime)
    return hashlib.sha1(f"{n}|{size}|{int(newest)}".encode()).hexdigest()[:16]


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"adimlar": {}}


def save_state(st: dict):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(STATE)


def pending_counts() -> dict:
    """İşlenmemiş veri: indirilip okunmamış, okunup ayrıştırılmamış (temp1→temp2)."""
    sys.path.insert(0, str(AG))
    out = {}
    try:
        import read_document as RD
        dl = [f for f in DL.rglob("*") if f.is_file() and f.suffix.lower() in RD.SUPPORTED and not f.name.startswith(("~$", "."))]
        unread = 0
        for f in dl:
            j = RD.out_base(f.resolve(), TEMP / "temp1", DL.resolve()).with_suffix(".json")
            if not j.exists():
                unread += 1
        out["okunmamis_indirme"] = unread
    except Exception as e:  # noqa: BLE001
        out["okunmamis_indirme"] = f"hesaplanamadı: {e}"
    t1 = {p.relative_to(TEMP / "temp1").with_suffix("") for p in (TEMP / "temp1").rglob("*.json")} if (TEMP / "temp1").exists() else set()
    t2 = {p.relative_to(TEMP / "temp2").with_suffix("") for p in (TEMP / "temp2").rglob("*.json")} if (TEMP / "temp2").exists() else set()
    # Aşama 2 kendi durum kaydına göre (bilerek atlanan "ders programı" gibi dosyalar bekleyen sayılmaz)
    try:
        s2 = json.loads((TEMP / "state" / "pipeline_state.json").read_text(encoding="utf-8")).get("stage2") or {}
    except Exception:
        s2 = {}
    done2 = {k for k, v in s2.items() if isinstance(v, dict) and v.get("ok")}
    out["ayristirilmamis"] = len({str(r) for r in t1} - {str(r) for r in t2} - done2)
    st = load_state()
    out["degisen_adim"] = [k for k, _n, _c, ins, _t, _l in STEPS if (st["adimlar"].get(k) or {}).get("girdi") != fingerprint(ins)]
    return out


def paused() -> bool:
    """Panelde "Tümünü durdur" basılıysa (phase_pause.json) yeni adım başlatılmaz."""
    return (TEMP / "state" / "phase_pause.json").exists()


def run_step(key: str, name: str, cmd: list[str], timeout: int, need_lock: bool) -> int:
    out = TEMP / "logs" / f"yeni_veri_{key}.log"
    log(f"▶ {name}")
    t0 = time.time()
    with open(out, "a", encoding="utf-8") as of:
        of.write(f"\n===== {time.strftime('%Y-%m-%d %H:%M:%S')} {name} =====\n")
        of.flush()
        lk = open(STAGE_LOCK, "w") if need_lock else None
        try:
            if lk:
                fcntl.flock(lk, fcntl.LOCK_EX)          # Aşama 2–4: pipeline_runner ile aynı anda değil
            if paused():                                # kilit beklenirken durdurulduysa başlatma
                log(f"⏸ {name} başlatılmadı: tüm fazlar durduruldu")
                return 130
            p = subprocess.Popen(cmd, cwd=str(ROOT), stdout=of, stderr=subprocess.STDOUT, start_new_session=True,
                                 env={**os.environ, "PYTHONUNBUFFERED": "1"})
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, 15)
            rc = 124
        finally:
            if lk:
                lk.close()
    log(f"{'✓' if rc == 0 else '✗'} {name} — rc={rc}, {round(time.time() - t0)} sn (kayıt: {out.name})")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--yeni", action="store_true", help="yalnız girdisi değişen adımlar (varsayılan)")
    g.add_argument("--bekleyen", action="store_true", help="işlenmemiş verileri bitir, sonra değişen adımlar")
    g.add_argument("--hepsi", action="store_true", help="parmak izine bakmadan tüm gerekli adımlar")
    g.add_argument("--durum", action="store_true", help="çalıştırmadan durum raporu")
    g.add_argument("--isaretle", action="store_true", help="mevcut veriyi 'işlendi' olarak işaretle (ilk kurulum; eski veri yeniden işlenmez)")
    ap.add_argument("--sadece", default="", help="virgülle adım anahtarları (test/elle): ör. oku,ayristir")
    a = ap.parse_args()
    only = {x.strip() for x in a.sadece.split(",") if x.strip()}

    if a.durum:
        print(json.dumps({"bekleyen": pending_counts(), "durum": load_state()}, ensure_ascii=False, indent=1))
        return 0
    if a.isaretle:
        st = load_state()
        for key, _n, _c, inputs, _t, _l in STEPS:
            st["adimlar"][key] = {"girdi": fingerprint(inputs), "rc": 0, "bitis": "işaretlendi " + time.strftime("%Y-%m-%dT%H:%M:%S")}
        save_state(st)
        log("mevcut veri işlendi olarak işaretlendi; bundan sonra yalnız yeni veri işlenir")
        return 0
    lock = open(TEMP / "state" / "yeni_veri_hatti.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log("hat zaten çalışıyor; çıkılıyor")
        return 0
    st = load_state()
    if a.bekleyen:
        pc = pending_counts()
        log(f"bekleyen: {pc}")
    ran = []
    for key, name, cmd, inputs, timeout, need_lock in STEPS:
        if only and key not in only:
            continue
        if not Path(cmd[1]).exists():
            log(f"atlandı (betik yok): {cmd[1]}")
            continue
        fp = fingerprint(inputs)
        prev = (st["adimlar"].get(key) or {}).get("girdi")
        if not a.hepsi and prev == fp and not (a.bekleyen and key in ("oku", "ayristir", "birlestir", "aktar")):
            continue                                         # girdi değişmedi → tekrar işleme yok
        if paused():
            log("⏸ tüm fazlar durduruldu; hat burada bırakıldı (devam edilince kaldığı yerden sürer)")
            break
        rc = run_step(key, name, cmd, timeout, need_lock)
        if rc == 130 and paused():
            break
        # çıktısı bir sonraki adımın girdisi olduğundan parmak izi adım SONRASI alınır
        st["adimlar"][key] = {"girdi": fingerprint(inputs), "rc": rc, "bitis": time.strftime("%Y-%m-%dT%H:%M:%S")}
        save_state(st)
        ran.append(key)
        if rc != 0 and key in ("oku", "ayristir", "birlestir", "aktar"):
            log(f"{name} hatalı bitti; sonraki aşamalara geçilmedi (bir sonraki çalıştırmada yeniden denenir)")
            st["adimlar"][key]["girdi"] = None
            save_state(st)
            break
    if ran and not only:
        t_restart = time.time()
        subprocess.run(SITE_REFRESH, capture_output=True)
        log(f"site arama dizini yenilendi · çalışan adımlar: {', '.join(ran)}")
        # Site açılışta data/local_rag_chunks.json'u yeniden üretir; üretilince yalnız yeni/değişen parçalar vektörlenip
        # yerel Supabase'e yazılır (bulut yalnız MEDS_RAG_TARGETS ile) (rag_vector_build artımlıdır)
        chunk_file = ROOT / "data" / "local_rag_chunks.json"
        for _ in range(90):
            if chunk_file.exists() and chunk_file.stat().st_mtime > t_restart:
                break
            time.sleep(10)
        rc = run_step("rag_vektor", "RAG vektörleri (yalnız yeni/değişen parçalar) → Supabase", [PY, str(AI / "rag_vector_build.py")], 6 * 3600, False)
        ran.append("rag_vektor" if rc == 0 else "rag_vektor(hata)")
    else:
        log("yeni veri yok; hiçbir adım çalışmadı")
    st["son"] = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "calisan": ran}
    save_state(st)
    return 0


if __name__ == "__main__":
    sys.exit(main())
