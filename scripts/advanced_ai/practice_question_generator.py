#!/usr/bin/env python3
"""
Örnek çalışma sorusu üretici — müfredata dayalı, kaynaklı.

Kapsam: Drive "drive_root" klasöründeki (https://drive.google.com/drive/folders/1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W) ders
notları; yerelde okunup (Aşama 1–2, Faz 12 temizlik) veritabanına girmiş hâlleri (ortak/rag/ders_materyali.jsonl).
Sıra: müfredat paketi (Faz 8 ağacı) — Kurul 1'den başlayarak kurul → ders → konu. Her konu için hedef 10 soru.
Günlük sınır: en fazla PRACTICE_DAILY_MAX (varsayılan 10) soru.

Model: YALNIZ ÜCRETSİZ bulut (scripts/agents/cloud_llm.py: Groq / Gemini ücretsiz anahtarlar). Yanıt yoksa yerel
Ollama (lib.chat_local). Faz 14'ün ücretli anahtarı ASLA kullanılmaz.

Doğrulama (her soru):
  * 5 farklı şık, A–E cevap, en az 3 açıklama maddesi
  * kaynak alıntısı ilgili ders notu parçasında birebir (boşluk/harf katlamalı) geçmeli → yoksa reddedilir
  * çıkmış sorulardan biriyle ya da daha önce üretilmiş bir soruyla kök benzerliği ≥ 0.55 ise reddedilir (birebir kopya yok)
Çıktı: $MEDS_DATABASE_DIR/derived/ornek_sorular/sorular.jsonl (+ durum.json, rapor.json). Durum: "ai_uretimi_dogrulanmadi".

Kullanım: practice_question_generator.py [--kurul 1] [--gunluk 10] [--konu-hedef 10] [--dry]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts" / "agents"))
import curriculum_package as CP  # noqa: E402
import cloud_llm  # noqa: E402

DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
OUT = DB / "derived" / "ornek_sorular"
QFILE = OUT / "sorular.jsonl"
STATE = OUT / "durum.json"
REPORT = OUT / "rapor.json"
RAG = DB / "ortak" / "rag" / "ders_materyali.jsonl"
SOURCES = DB / "sources"
PAST = ROOT / "data" / "pastQuestions.json"
LOG = ROOT.parent / "meds_temp" / "logs" / "ornek_soru.log"
SOURCE_ROOT = "drive_root/"          # yalnız bu Drive klasöründen gelen ders notları
SIM_MAX = 0.55


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [ornek_soru] {m}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


FOLD = str.maketrans("ÇĞİIÖŞÜÂÎÛçğıöşüâîû", "cgiiosuaiucgiosuaiu")


def fold(s: str) -> str:
    return re.sub(r"\s+", " ", str(s or "").translate(FOLD).lower()).strip()


def stems(s: str) -> set[str]:
    return {w[:5] for w in re.findall(r"[a-z0-9]{3,}", fold(s))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


# ---------------------------------------------------------------- veri
def load_sources() -> dict[str, dict]:
    out = {}
    for f in SOURCES.glob("*.json"):
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(s.get("path", "")).startswith(SOURCE_ROOT) and s.get("doc_type") in (None, "lecture_slide", "summary"):
            out[s["source_id"]] = s
    return out


def load_chunks(src_ids: set[str]) -> list[dict]:
    rows = []
    with open(RAG, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("kaynak_id") in src_ids and len(r.get("metin") or "") > 80:
                rows.append(r)
    return rows


def load_past() -> list[dict]:
    try:
        d = json.loads(PAST.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else d.get("questions", [])
    except Exception:
        return []


def load_state() -> dict:
    today = time.strftime("%Y-%m-%d")
    try:
        st = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        st = {}
    st.setdefault("konu_sayac", {})
    st.setdefault("kaynak_yok", [])
    if st.get("gun") != today:
        st["gun"], st["bugun"] = today, 0
    return st


def save_state(st: dict):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(STATE)


def existing_generated() -> list[dict]:
    if not QFILE.exists():
        return []
    return [json.loads(l) for l in QFILE.read_text(encoding="utf-8").splitlines() if l.strip()]


# ---------------------------------------------------------------- kaynak seçimi
def pick_chunks(chunks: list[dict], sources: dict, kurul: int, ders: str, konu: str, k: int = 6) -> list[dict]:
    want = stems(konu)
    dk = fold(ders)
    cand = []
    for c in chunks:
        s = sources.get(c["kaynak_id"]) or {}
        if s.get("kurul") not in (kurul, str(kurul)):
            continue
        if fold(s.get("ders")) != dk and dk not in fold(s.get("path")):
            continue
        title = fold(s.get("name") or s.get("path"))
        score = 2 * len(want & stems(title)) + len(want & stems(c.get("metin", "")[:1500]))
        if score > 0:
            cand.append((score, c))
    cand.sort(key=lambda x: -x[0])
    return [c for _, c in cand[:k]]


def past_examples(past: list[dict], ders: str, konu: str, n: int = 4) -> list[str]:
    want = stems(konu) | stems(ders)
    scored = []
    for q in past:
        stem = q.get("stem") or (q.get("reconstruction") or {}).get("stem") or ""
        if len(stem) < 25:
            continue
        sc = len(want & stems(stem + " " + str(q.get("topic") or "") + " " + str(q.get("discipline") or "")))
        if sc:
            scored.append((sc, stem))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:n]]


# ---------------------------------------------------------------- üretim
SYSTEM = """Sen tıp fakültesi Dönem 3 kurul sınavı soru yazarısın. Yalnız verilen DERS NOTU PARÇALARINA dayanarak, verilen
müfredat konusunu ölçen çoktan seçmeli (A–E) özgün sorular yazarsın.
KURALLAR:
- Her soru yalnız ders notlarında açıkça geçen bilgiye dayanmalı; notta olmayan bilgiyi soru ya da doğru cevap yapma.
- Her soru için ders notundan KELİMESİ KELİMESİNE bir alıntı ("alinti", 8–40 kelime) ve parça kimliğini ("parca_id") ver.
- Çıkmış soru örnekleri yalnız biçim/zorluk içindir: onları KOPYALAMA, aynı kökü ya da aynı şık setini kullanma.
- 5 şık birbirinden farklı, tek doğru cevap; çeldiriciler aynı konudan ve makul olsun.
- Açıklamayı 3–5 madde hâlinde yaz (doğru cevabın gerekçesi + önemli çeldiricilerin neden yanlış olduğu).
- Türkçe yaz; Latince/İngilizce terimleri notta geçtiği gibi kullan. Yalnız istenen JSON."""


def build_prompt(kurul: int, ders: str, konu: str, chunks: list[dict], examples: list[str], n: int, avoid: list[str]) -> str:
    parts = "\n\n".join(f"[parca_id: {c['id']}]\n{(c.get('metin') or '')[:1800]}" for c in chunks)
    ex = "\n".join(f"- {e[:220]}" for e in examples) or "(yok)"
    av = "\n".join(f"- {a[:160]}" for a in avoid[-10:]) or "(yok)"
    return f"""KURUL {kurul} · DERS: {ders} · MÜFREDAT KONUSU: {konu}

DERS NOTU PARÇALARI (tek kaynak):
{parts}

ÇIKMIŞ SORU ÖRNEKLERİ (yalnız biçim için; kopyalama):
{ex}

DAHA ÖNCE ÜRETİLMİŞ KÖKLER (tekrar etme):
{av}

Bu konu için {n} adet soru üret. JSON şeması:
{{"sorular": [{{"soru_koku": "...", "secenekler": {{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}},
  "dogru_secenek": "A", "aciklama_maddeleri": ["...", "...", "..."], "parca_id": "...", "alinti": "notdan birebir alıntı",
  "zorluk": "kolay|orta|zor"}}]}}"""


def llm(prompt: str) -> tuple[dict | None, str]:
    """Yalnız ücretsiz bulut; olmazsa yerel Ollama. Ücretli anahtar hiç denenmez."""
    res = cloud_llm.chat(prompt, system=SYSTEM, as_json=True, max_tokens=6000, temperature=0.4, log=log)
    if isinstance(res, dict):
        return res, f"{cloud_llm.last_model.get('ad')} (ücretsiz)"
    try:
        import lib
        if lib.ollama_up():
            r = lib.chat_local(lib.MODEL_TEXT, SYSTEM + "\n\n" + prompt, as_json=True, num_predict=4000, timeout=600)
            if isinstance(r, dict):
                return r, f"yerel:{lib.MODEL_TEXT}"
    except Exception as e:  # noqa: BLE001
        log(f"yerel model kullanılamadı: {e}")
    return None, "yok"


def quote_in(chunk_text: str, quote: str) -> bool:
    q = fold(quote)
    if len(q) < 25:
        return False
    t = fold(chunk_text)
    if q in t:
        return True
    # OCR/temizlik farkları: 8 kelimelik pencerelerin çoğu geçmeli
    w = q.split()
    if len(w) < 8:
        return False
    wins = [" ".join(w[i:i + 8]) for i in range(0, len(w) - 7, 4)]
    return sum(1 for x in wins if x in t) >= max(1, int(len(wins) * 0.6))


def validate(q: dict, chunks_by_id: dict, past_stems: list[set], made_stems: list[set]) -> str | None:
    opts = q.get("secenekler") or {}
    if sorted(k.upper() for k in opts) != list("ABCDE"):
        return "şık sayısı 5 değil"
    if len({fold(v) for v in opts.values()}) < 5:
        return "aynı şık tekrar"
    if str(q.get("dogru_secenek", "")).upper() not in "ABCDE" or not q.get("dogru_secenek"):
        return "cevap geçersiz"
    if len(q.get("aciklama_maddeleri") or []) < 3:
        return "açıklama maddesi < 3"
    ch = chunks_by_id.get(q.get("parca_id"))
    if not ch:
        return "parça kimliği yok"
    if not quote_in(ch.get("metin") or "", q.get("alinti") or ""):
        return "alıntı ders notunda bulunamadı"
    st = stems(q.get("soru_koku", ""))
    if len(st) < 4:
        return "kök çok kısa"
    for ps in past_stems:
        if jaccard(st, ps) >= SIM_MAX:
            return "çıkmış soruya çok benziyor"
    for ms in made_stems:
        if jaccard(st, ms) >= SIM_MAX:
            return "daha önce üretilmiş soruya çok benziyor"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int, default=1, help="başlangıç kurulu (varsayılan 1)")
    ap.add_argument("--gunluk", type=int, default=int(os.environ.get("PRACTICE_DAILY_MAX", "10")))
    ap.add_argument("--konu-hedef", type=int, default=10)
    ap.add_argument("--parti", type=int, default=5, help="tek istekte üretilecek soru")
    ap.add_argument("--dry", action="store_true", help="kaydetmeden üret ve göster")
    a = ap.parse_args()

    st = load_state()
    kalan_gun = a.gunluk - st["bugun"]
    if kalan_gun <= 0:
        log(f"günlük sınır doldu ({st['bugun']}/{a.gunluk}); yarın devam")
        return 0
    pkg = CP.load()
    sources = load_sources()
    if not sources:
        log("drive_root kaynaklı ders notu yok (Aşama 1–2 ve veritabanı yüklemesini kontrol edin)")
        return 1
    chunks = load_chunks(set(sources))
    by_id = {c["id"]: c for c in chunks}
    past = load_past()
    past_stems = [stems(q.get("stem") or (q.get("reconstruction") or {}).get("stem") or "") for q in past]
    made = existing_generated()
    made_stems = [stems(q["soru_koku"]) for q in made]
    log(f"kaynak: {len(sources)} ders notu, {len(chunks)} parça · çıkmış: {len(past)} · üretilmiş: {len(made)} · bugün kalan: {kalan_gun}")

    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "uretilen": 0, "reddedilen": {}, "konular": []}
    for k in sorted(pkg["kurullar"], key=lambda x: x["kurul"]):
        if k["kurul"] < a.kurul:
            continue
        for d in k["dersler"]:
            for konu in d["konular"]:
                if kalan_gun <= 0:
                    break
                key = f"{k['kurul']}|{d['ders']}|{konu}"
                have = st["konu_sayac"].get(key, 0)
                if have >= a.konu_hedef or key in st["kaynak_yok"]:
                    continue
                sel = pick_chunks(chunks, sources, k["kurul"], d["ders"], konu)
                if not sel:
                    log(f"kaynak yok, atlandı: {key}")
                    st["kaynak_yok"].append(key)
                    save_state(st)
                    continue
                n = min(a.parti, a.konu_hedef - have, kalan_gun)
                avoid = [q["soru_koku"] for q in made if q.get("konu") == konu]
                res, model = llm(build_prompt(k["kurul"], d["ders"], konu, sel, past_examples(past, d["ders"], konu), n, avoid))
                if not res:
                    log("model yanıt vermedi (ücretsiz kotalar dolmuş ve yerel model kapalı olabilir); sonraki çalıştırmaya kaldı")
                    save_state(st)
                    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
                    return 0
                ok = 0
                for q in (res.get("sorular") or [])[:n]:
                    why = validate(q, by_id, past_stems, made_stems)
                    if why:
                        rep["reddedilen"][why] = rep["reddedilen"].get(why, 0) + 1
                        log(f"  reddedildi ({why}): {str(q.get('soru_koku'))[:80]}")
                        continue
                    ch = by_id[q["parca_id"]]
                    src = sources.get(ch["kaynak_id"]) or {}
                    rec = {
                        "id": "ornek-" + uuid.uuid4().hex[:12], "kurul": k["kurul"], "committeeId": f"donem3-kurul{k['kurul']}",
                        "ders": d["ders"], "konu": konu, "soru_koku": q["soru_koku"].strip(),
                        "secenekler": {kk.upper(): str(v).strip() for kk, v in q["secenekler"].items()},
                        "dogru_secenek": q["dogru_secenek"].upper(), "aciklama_maddeleri": q["aciklama_maddeleri"],
                        "zorluk": q.get("zorluk"),
                        "kaynak": {"parca_id": ch["id"], "kaynak_id": ch["kaynak_id"], "sayfa": ch.get("sayfa"),
                                   "ders_notu": src.get("name"), "alinti": q["alinti"]},
                        "model": model, "durum": "ai_uretimi_dogrulanmadi", "olusturma": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                    if a.dry:
                        print(json.dumps(rec, ensure_ascii=False, indent=1))
                    else:
                        OUT.mkdir(parents=True, exist_ok=True)
                        with open(QFILE, "a", encoding="utf-8") as f:
                            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    made.append(rec)
                    made_stems.append(stems(rec["soru_koku"]))
                    ok += 1
                if not a.dry:
                    st["konu_sayac"][key] = have + ok
                    st["bugun"] += ok
                    save_state(st)
                kalan_gun -= max(ok, 1)        # başarısız istek de günlük hakkı tüketmesin diye en az 1 sayılır
                rep["uretilen"] += ok
                rep["konular"].append({"konu": key, "uretilen": ok, "model": model})
                log(f"{key}: {ok}/{n} soru kabul ({model})")
            if kalan_gun <= 0:
                break
        if kalan_gun <= 0:
            break
    if not a.dry:
        REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"bitti: {rep['uretilen']} soru · reddedilen {rep['reddedilen']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
