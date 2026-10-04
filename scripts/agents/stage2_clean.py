#!/usr/bin/env python3
"""
2. aşama: temp1 -> temp2  (düzeltme / anlamlandırma). Yerel, token harcamaz.

Her belge için:
  1. Biçim temizliği (boşluk, kesik satırlar, sayfa numaraları, kontrol karakterleri, tekrarlayan üst/alt bilgi)
  2. Deterministik Türkçe onarım (mojibake, '!' = bozuk i/ı, kelime içi ASCII sadeleştirme: hucre->hücre)
  3. Kalite puanı; çok bozuk sayfalara yerel LLM ile imla düzeltmesi (DOĞRULAMALI: içerik kaybı/ekleme reddedilir)
  4. Çıkmış soru belgelerinde sorular ayrıştırılır (önce kural tabanlı, olmazsa LLM; LLM çıktısı kaynakta
     bulunamıyorsa atılır = uydurma yok), şık/gövde karışmaları ayrılır, (cevap) işareti okunur
  5. Çıktı: temp2/<yol>.md + .json  (meta, kalite, sorular, uyarılar)

Kullanım: stage2_clean.py [--limit N] [--force] [--no-llm] [--only SUBSTR]
"""
from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import re
import sys
import threading
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402

log = lib.get_logger("stage2")
OPT_RE = re.compile(r"^\s*\(?([A-Ea-e])(?:[\)\.\-:]|\s{1,4})\s*(\S.*)$")
OPT_RE_STRICT = re.compile(r"^\s*\(?([A-E])[\)\.\-:]\s*(\S.*)$")
Q_RE = re.compile(r"^\s*(\d{1,3})\s*[\.\)\-]\s*(\S.*)$")
ANS_MARK = re.compile(r"\(\s*cevap\s*\)|\bcevap\s*[:\-]?\s*$", re.I)
ANS_LINE = re.compile(r"^\s*cevap\s*[:\-]?\s*([A-E])\b", re.I)


# --------------------------------------------------------------------------- sayfa temizliği
def strip_repeated_lines(pages: list[str]) -> list[str]:
    """Çoğu sayfada tekrar eden kısa satırlar (üst/alt bilgi, filigran) çıkarılır."""
    if len(pages) < 4:
        return pages
    cnt = Counter()
    for p in pages:
        for ln in set(l.strip() for l in p.split("\n") if 3 <= len(l.strip()) <= 80):
            cnt[ln] += 1
    rep = {ln for ln, n in cnt.items() if n >= max(4, int(0.5 * len(pages)))}
    if not rep:
        return pages
    return ["\n".join(l for l in p.split("\n") if l.strip() not in rep) for p in pages]


# --------------------------------------------------------------------------- LLM doğrulamalı düzeltme
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")


def llm_fix_is_safe(orig: str, fixed: str) -> bool:
    """Yalnızca imla düzeltmesi mi? Sayılar aynı, uzunluk benzer, harf düzeyinde yüksek benzerlik."""
    if not fixed or abs(len(fixed) - len(orig)) > 0.12 * max(len(orig), 1):
        return False
    if sorted(NUM_RE.findall(orig)) != sorted(NUM_RE.findall(fixed)):
        return False
    return difflib.SequenceMatcher(None, lib.fold(orig), lib.fold(fixed), autojunk=False).ratio() >= 0.9


FIX_SYSTEM = (
    "Sen bir Türkçe tıp metni düzeltmenisin. Aşağıdaki metin OCR taramasından çıkmış hatalı bir tıp fakültesi ders notudur.\n"
    "Metnin tıbbi bağlamını bozmadan, kelimelerdeki harf ve rakam hatalarını (örneğin 0 yerine O, 1 yerine I, "
    "'5taf11ococus' yerine 'Staphylococcus', 'M1yokard' yerine 'Miyokard' gibi) düzelt ve geçerli tıbbi terminolojiye uygun hale getir.\n"
    "Anlamı değiştirme, dışarıdan bilgi ekleme, çıkarma veya özetleme yapma. "
    "Sayıları, birimleri, kısaltmaları ve gen/ilaç adlarını aynen koru. "
    "Yalnızca düzeltilmiş nihai metni yaz, açıklama ekleme."
)


def llm_polish(text: str, use_llm: bool, transform_cb=None) -> tuple[str, bool]:
    if not use_llm or len(text) < 60:
        return text, False
    # Sayfa/blok açıkça bir OCR çöpüyse LLM'e sokma, doğrudan boşalt
    if lib.is_ocr_garbage(text):
        return "", False

    out_parts, changed = [], False
    # ~1800 karakterlik parçalar (satır sınırından)
    buf = ""
    chunks = []
    for ln in text.split("\n"):
        if len(buf) + len(ln) > 1800 and buf:
            chunks.append(buf)
            buf = ""
        buf += ln + "\n"
    if buf.strip():
        chunks.append(buf)
    for c in chunks:
        if lib.is_ocr_garbage(c):
            continue  # Parça çöp ise atla
        try:
            # Hızlı düzeltmeler için hafif model (qwen3:1.7b) kullanılır, aşırı hızlıdır
            fixed = lib.chat(lib.MODEL_FAST, c.strip(), system=FIX_SYSTEM, num_predict=1200)
        except Exception as e:  # noqa: BLE001
            log.warning("LLM düzeltme atlandı: %s", e)
            out_parts.append(c.strip())
            continue
        if llm_fix_is_safe(c.strip(), fixed):
            out_parts.append(fixed.strip())
            if fixed.strip() != c.strip():
                changed = True
                if transform_cb:
                    transform_cb("İmla & Karakter Onarımı", c.strip(), fixed.strip())
        else:
            out_parts.append(c.strip())  # güvensiz düzeltme reddedildi
    return "\n".join(out_parts), changed


# --------------------------------------------------------------------------- soru ayrıştırma
def parse_questions_rules(text: str, page_of_line: list[int]) -> list[dict]:
    lines = text.split("\n")
    qs, cur, last_opt = [], None, None

    def close():
        nonlocal cur, last_opt
        if cur:
            qs.append(cur)
        cur, last_opt = None, None

    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        pg = page_of_line[i] if i < len(page_of_line) else None
        mans = ANS_LINE.match(ln)
        if mans and cur is not None:
            cur["answer"] = mans.group(1).upper()
            continue
        mq = Q_RE.match(ln)
        mo = (OPT_RE_STRICT.match(ln) or OPT_RE.match(ln)) if cur is not None else None
        # Numaralı satır: yeni soru (şık harfi satırı değilse)
        if mq and not (mo and mo.group(1).upper() == "A" and False):
            close()
            cur = {"no": int(mq.group(1)), "stem": mq.group(2).strip(), "options": {}, "answer": None, "page": pg}
            continue
        if cur is None:
            continue
        if mo:
            letter = mo.group(1).upper()
            nxt = chr(ord(last_opt) + 1) if last_opt else "A"
            if letter == nxt or (letter in "ABCDE" and letter not in cur["options"] and ord(letter) > ord(last_opt or "@")):
                cur["options"][letter] = mo.group(2).strip()
                last_opt = letter
                continue
        # devam satırı
        if last_opt:
            cur["options"][last_opt] += " " + ln.strip()
        else:
            cur["stem"] += " " + ln.strip()
    close()
    for q in qs:
        for k in list(q["options"]):
            v = q["options"][k]
            if ANS_MARK.search(v):
                q["answer"] = k
                q["options"][k] = ANS_MARK.sub("", v).strip()
        if ANS_MARK.search(q["stem"]):
            q["stem"] = ANS_MARK.sub("", q["stem"]).strip()
    return qs


def q_valid(q: dict) -> bool:
    return len(q["stem"]) >= 12 and len(q["options"]) >= 4


LLM_Q_SYSTEM = (
    "Sen bir sınav sorusu ayrıştırıcısın. Verilen ham metinden çoktan seçmeli soruları çıkar. "
    "Metinde olmayan hiçbir şeyi ekleme; soru kökünü ve şıkları metindeki gibi yaz. "
    "Şıklar harfsiz alt alta yazılmış olabilir; sırayla A,B,C,D,E ver. '(cevap)' veya 'cevap' işareti doğru şıkkı gösterir, "
    "'answer' alanına o harfi yaz, bilinmiyorsa null. Eksik/yarım soruları ATLA. "
    'JSON: {"questions":[{"no":int|null,"stem":str,"options":{"A":str,...},"answer":"A"|null}]}'
)


def support_ratio(piece: str, source_fold_tokens: set[str]) -> float:
    toks = lib.tokens(piece)
    if not toks:
        return 1.0
    return sum(t in source_fold_tokens for t in toks) / len(toks)


def parse_questions_llm(text: str, use_llm: bool, progress_cb=None, transform_cb=None) -> list[dict]:
    if not use_llm:
        return []
    out = []
    windows, buf = [], ""
    for ln in text.split("\n"):
        if len(buf) > 1800:
            windows.append(buf)
            buf = buf[-250:]  # örtüşme: pencere sınırında bölünen soru kaybolmasın
        buf += ln + "\n"
    if buf.strip():
        windows.append(buf)

    total_w = len(windows)
    for w_idx, w in enumerate(windows, 1):
        if progress_cb:
            progress_cb(w_idx, total_w, f"Yapay zeka soru ayrıştırıyor (Blok {w_idx}/{total_w})")
        try:
            res = lib.chat(lib.MODEL_TEXT, w, system=LLM_Q_SYSTEM, as_json=True, num_predict=3500)
        except Exception as e:  # noqa: BLE001
            # JSON kesilmişse içindeki tamamlanmış soruları kurtarmayı dene
            try:
                import re as _re, json as _json
                # Tek tek tam soru nesnelerini regex ile ayıkla
                recovered = []
                raw_matches = _re.findall(r'\{\s*"no"\s*:.*?\}', str(e), _re.DOTALL)
                for rm in raw_matches:
                    try:
                        recovered.append(_json.loads(rm))
                    except Exception:
                        pass
                if recovered:
                    res = {"questions": recovered}
                else:
                    log.warning("LLM soru çıkarımı atlandı: %s", e)
                    continue
            except Exception:
                log.warning("LLM soru çıkarımı atlandı: %s", e)
                continue
        src = set(lib.tokens(w))
        found_in_window = []
        for q in (res.get("questions") or []) if isinstance(res, dict) else []:
            try:
                stem = str(q.get("stem", "")).strip()
                opts = {str(k).upper(): str(v).strip() for k, v in (q.get("options") or {}).items() if str(v).strip()}
                ans = q.get("answer")
                ans = str(ans).upper() if ans and str(ans).upper() in "ABCDE" else None
            except Exception:  # noqa: BLE001
                continue
            # Uydurma koruması: her parça kaynakta bulunmalı
            if not stem or support_ratio(stem, src) < 0.85 or any(support_ratio(v, src) < 0.8 for v in opts.values()):
                continue
            q_obj = {"no": q.get("no") if isinstance(q.get("no"), int) else None, "stem": stem,
                     "options": opts, "answer": ans, "page": None}
            out.append(q_obj)
            found_in_window.append(f"{stem[:60]}... ({len(opts)} şık)")

        if transform_cb and found_in_window:
            transform_cb("Ham Metinden Soru Çıkarma", w[:120].strip() + "...", " | ".join(found_in_window[:2]))
    return out


def polish_questions(qs: list[dict], use_llm: bool, progress_cb=None, transform_cb=None):
    """Şüpheli soruları paralel batch mantığı ile doğrulamalı düzelt."""
    if not use_llm:
        return
    lex = lib.lexicon()

    def sus(q):
        txt = q["stem"] + " " + " ".join(q["options"].values())
        words = [w.lower() for w in lib.WORD_RE.findall(txt) if len(w) >= 4]
        cov = sum(lex.get(w, 0) >= 2 for w in words) / len(words) if words else 1.0
        return cov < 0.8 or q["stem"][:1].islower()

    todo = [q for q in qs if sus(q)]
    if not todo:
        return

    batches = [todo[i:i + 3] for i in range(0, len(todo), 3)]
    total_b = len(batches)
    completed_b = 0
    lock = threading.Lock()

    def handle_batch(b_idx, batch):
        nonlocal completed_b
        payload = {str(j): {"stem": q["stem"], "options": q["options"]} for j, q in enumerate(batch)}
        try:
            import json as _j
            res = lib.chat(lib.MODEL_TEXT, _j.dumps(payload, ensure_ascii=False), system=FIX_SYSTEM +
                           ' Girdi JSON; aynı yapıda JSON döndür (anahtarlar, harfler aynı kalsın).', as_json=True,
                           num_predict=2500, timeout=120)
        except Exception as e:  # noqa: BLE001
            log.warning("Soru düzeltme atlandı (batch %d): %s", b_idx, e)
            res = None

        if isinstance(res, dict):
            for j, q in enumerate(batch):
                r = res.get(str(j))
                if not isinstance(r, dict):
                    continue
                try:
                    ns, nopt = str(r["stem"]).strip(), {k: str(v).strip() for k, v in r["options"].items()}
                except Exception:
                    continue
                if set(nopt) != set(q["options"]) or not llm_fix_is_safe(q["stem"], ns):
                    continue
                if all(llm_fix_is_safe(q["options"][k], nopt[k]) for k in nopt):
                    if ns != q["stem"] or nopt != q["options"]:
                        old_s = q["stem"]
                        q["stem_before_polish"] = q["stem"]
                        q["stem"], q["options"] = ns, nopt
                        q["polished"] = True
                        if transform_cb:
                            transform_cb("Soru Düzeltme (İmla & Şık)", old_s[:100], ns[:100])

        with lock:
            completed_b += 1
            if progress_cb:
                progress_cb(completed_b, total_b, f"Soru düzeltme (Batch {completed_b}/{total_b})")

    # 2 eşzamanlı worker ile GPU / Ollama yükünü optimize et
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(handle_batch, idx, b) for idx, b in enumerate(batches, 1)]
        concurrent.futures.wait(futures)


# --------------------------------------------------------------------------- belge işleme
def process(json_path: Path, use_llm: bool, progress_cb=None, transform_cb=None) -> dict:
    d = lib.read_json(json_path)
    rel = str(json_path.relative_to(lib.TEMP1).with_suffix(""))
    meta = lib.infer_meta(rel)
    if meta["doc_type"] == "schedule":
        return {"skipped": "ders programı ayrı işlenir"}
    pages_raw = [lib.clean_layout(p["text"]) for p in d["pages"]]
    pages_raw = strip_repeated_lines(pages_raw)
    pages, stats_total = [], Counter()
    total_pages = len(pages_raw)

    for i, t in enumerate(pages_raw):
        if progress_cb and i % 5 == 0:
            progress_cb(i + 1, total_pages, f"Sayfa {i+1}/{total_pages} temizleniyor")
        
        # Slayttaki görsel/grafik OCR çöpüyse sayfayı temizle
        if lib.is_ocr_garbage(t):
            t = ""

        t2, st = lib.repair_text(t)
        stats_total.update(st)
        q = lib.quality_of(t2)
        polished = False
        if q < 0.6 and len(t2) > 150 and meta["doc_type"] != "past_question":
            t2, polished = llm_polish(t2, use_llm, transform_cb=transform_cb)
            q = lib.quality_of(t2)
        pages.append({"n": d["pages"][i]["n"], "text": t2, "quality": q,
                      "method": d["pages"][i].get("method"), "llm_polished": polished})
    quality = round(sum(p["quality"] * max(1, len(p["text"])) for p in pages) /
                    max(1, sum(max(1, len(p["text"])) for p in pages)), 3)
    issues = []
    if sum(1 for p in pages if not p["text"].strip()) > 0.3 * len(pages):
        issues.append("sayfaların >%30'u boş/okunamadı (görsel model gerekebilir)")
    if quality < 0.5:
        issues.append("düşük kalite puanı")

    out = {"stage": "temp2", "rel": rel, "source_sha256": d.get("source_sha256"), "page_count": len(pages),
           "meta": meta, "quality": quality, "repair_stats": dict(stats_total), "issues": issues, "pages": pages}

    if meta["doc_type"] == "past_question":
        if progress_cb:
            progress_cb(total_pages, total_pages, "Sorular kural tabanlı taranıyor...")
        full, page_of_line = [], []
        for p in pages:
            for ln in p["text"].split("\n"):
                full.append(ln)
                page_of_line.append(p["n"])
        text = "\n".join(full)
        qs = parse_questions_rules(text, page_of_line)
        good = [q for q in qs if q_valid(q)]
        method = "kural"
        if len(good) < 5 or len(good) < 0.5 * max(1, len(qs)):
            lq = parse_questions_llm(text, use_llm, progress_cb=progress_cb, transform_cb=transform_cb)
            if len(lq) > len(good):
                good, method = lq, "llm"
        polish_questions(good, use_llm, progress_cb=progress_cb, transform_cb=transform_cb)
        for k, q in enumerate(good, 1):
            q["extraction"] = method
            q["issues"] = ([] if q["answer"] else ["cevap bilinmiyor"]) + (["şık sayısı<5"] if len(q["options"]) < 5 else [])
        out["questions"] = good
        out["question_extraction"] = {"method": method, "rule_candidates": len(qs), "accepted": len(good)}
        if not good:
            out["issues"].append("soru çıkarılamadı")
    return out


def run(limit=0, force=False, use_llm=True, only: str | None = None) -> int:
    state = lib.State()
    files = sorted(lib.TEMP1.rglob("*.json"))
    # sözlük: temiz ders notlarından (çıkmış soru dışı), yoksa mevcutlardan
    if not lib.lexicon():
        texts = []
        for f in files:
            if lib.infer_meta(str(f.relative_to(lib.TEMP1).with_suffix("")))["doc_type"] == "lecture_slide":
                dd = lib.read_json(f, {})
                texts += [p.get("text", "") for p in dd.get("pages", [])]
        if texts:
            lib.build_lexicon(texts)
            lib.reset_lexicon()
            log.info("Sözlük oluşturuldu: %d kelime", len(lib.lexicon()))
    n = 0
    for f in files:
        rel = str(f.relative_to(lib.TEMP1).with_suffix(""))
        if only and only.lower() not in rel.lower():
            continue
        h = lib.read_json(f, {}).get("source_sha256") or str(f.stat().st_mtime)
        if not force and not state.needs("stage2", rel, h):
            continue

        def make_progress_cb(target_rel):
            return lambda cur, tot, desc: state.set_progress(target_rel, cur, tot, desc)

        def make_transform_cb(target_rel):
            return lambda step_name, inp, outp: state.add_transformation(target_rel, step_name, inp, outp)

        t0 = time.time()
        try:
            state.set_progress(rel, 1, 100, "Başlatılıyor...")
            res = process(f, use_llm, progress_cb=make_progress_cb(rel), transform_cb=make_transform_cb(rel))
            if res.get("skipped"):
                state.done("stage2", rel, h, ok=True, note=res["skipped"])
                continue
            base = lib.TEMP2 / rel
            lib.write_json(base.with_suffix(".json"), res)
            md = [f"# {rel}\n", f"> kalite: {res['quality']}  |  tür: {res['meta']['doc_type']}\n"]
            for p in res["pages"]:
                md.append(f"\n## Sayfa {p['n']}\n\n{p['text']}\n")
            base.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
            state.done("stage2", rel, h, ok=True)
            n += 1
            qn = len(res.get("questions", []))
            log.info("temp2 ✓ %s  kalite=%.2f  sorular=%s  %.1fs", rel, res["quality"], qn if qn else "-", time.time() - t0)
        except Exception as e:  # noqa: BLE001
            state.done("stage2", rel, h, ok=False, err=str(e)[:300])
            log.error("temp2 ✗ %s: %s", rel, e)
        if limit and n >= limit:
            break
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    use_llm = not a.no_llm and lib.ollama_up()
    if not a.no_llm and not use_llm:
        log.warning("Ollama kapalı: LLM adımları atlanıyor (yalnız deterministik onarım)")
    print("işlenen:", run(a.limit, a.force, use_llm, a.only))
