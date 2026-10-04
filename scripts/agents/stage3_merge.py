#!/usr/bin/env python3
"""
3. aşama: temp2 -> temp3  (birleştirme, ilişkilendirme, metadata, tekilleştirme). Yerel, token harcamaz.

Kaynak notları (lecture_slide):
  - müfredat eşleşmesi (kurul/ders yoldan; konu: ders programı taslağıyla bulanık eşleşme)
  - LLM ile belge metadata'sı: özet, amaç, konular, hastalık/ilaç/gen/belirti terimleri
    (terimler kaynakta geçmiyorsa atılır = uydurma yok)
  - RAG chunk'ları (+ bge-m3 vektörleri)
Çıkmış sorular (past_question):
  - tekilleştirme (normalize anahtar + anlamsal/şık benzerliği)
  - kaynak eşleştirme: anlamsal (embedding) + sözcük (IDF) + tıbbi terim örtüşmesi; "kesin" ancak eşik,
    ikinci kaynaktan fark, kurul uyumu ve terim örtüşmesi birlikte sağlanırsa
  - yalnız KESİN eşleşenlerde, kaynak metne dayalı doğrulamalı zenginleştirme (eksik şık / açıklama / %10-50 ayrıntı)
  - durum: verified | fixed | needs_fix | rejected  (database yalnız verified/fixed + kanıtlıyı alır)

Kullanım: stage3_merge.py [--no-llm] [--skip-enrich]
"""
from __future__ import annotations

import argparse
import hashlib
import math
import pickle
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402
import numpy as np  # noqa: E402

log = lib.get_logger("stage3")
SRC_DIR, CHUNK_DIR, VEC_DIR = lib.TEMP3 / "sources", lib.TEMP3 / "chunks", lib.TEMP3 / "vectors"
CURRICULUM = lib.TEMP3 / "ders_programi_taslak.json"
EMB_CACHE = lib.STATE_DIR / "embcache.pkl"

# Eşik değerleri (bge-m3 kosinüs); .env/ortamdan ayarlanabilir
T_SCORE = float(__import__("os").environ.get("MEDS_MATCH_SCORE", "0.60"))
T_MARGIN = float(__import__("os").environ.get("MEDS_MATCH_MARGIN", "0.03"))
T_TERMS = int(__import__("os").environ.get("MEDS_MATCH_TERMS", "2"))

# Hakem Ajan (Judge Agent - DeepSeek-R1) Eşikleri:
# support_ratio >= 0.85: Otomatik onayla (verified)
# 0.65 <= support_ratio < 0.85: Hakem Ajan kuyruğuna (referee_queue / needs_referee)
# support_ratio < 0.65: Eksik kaynak / inceleme (needs_fix / rejected)
T_VERIFIED_SUPPORT = 0.85
T_REFEREE_SUPPORT = 0.65
STOP = set(lib.tokens("hangisi hangileri aşağıdakilerden aşağıdaki doğrudur yanlıştır değildir olarak ile için gibi daha çok en bir "
                      "bu şu ve veya ya da olan olur olabilir görülür tanı tedavi hastalık hasta özellik özelliği sonucu sonuç "
                      "neden nedeni nedir nasıl hangi"))


# --------------------------------------------------------------------------- SSD Disk Destekli Önbellek (Zero-RAM Leak)
import diskcache

SSD_CACHE_DIR = lib.STATE_DIR / "disk_emb_cache"
_disk_cache = diskcache.Cache(str(SSD_CACHE_DIR))

# Eski pickle önbelleğini SQLite diskcache'e taşı
if EMB_CACHE.exists() and len(_disk_cache) == 0:
    try:
        old_data = pickle.loads(EMB_CACHE.read_bytes())
        with _disk_cache.transact():
            for k, v in old_data.items():
                _disk_cache[k] = v
        log.info("Eski önbellekten %d vektör SSD diskcache'e aktarıldı.", len(old_data))
    except Exception as e:
        log.warning("Önbellek taşıma uyarısı: %s", e)


def embed_cached(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, 1024), dtype="float32")

    keys = [hashlib.sha1((lib.MODEL_EMBED + t).encode()).hexdigest() for t in texts]
    miss = [i for i, k in enumerate(keys) if k not in _disk_cache]

    if miss:
        # GPU RTX 4060 için toplu embedding
        vecs = lib.embed([texts[i][:2000] for i in miss])
        with _disk_cache.transact():
            for i, v in zip(miss, vecs):
                _disk_cache[keys[i]] = v

    # Doğrudan diskcache'ten çekerek RAM sızıntısını ve swap baskısını engelle
    results = [_disk_cache[k] for k in keys]
    return np.stack(results) if results else np.zeros((0, 1024), dtype="float32")


# --------------------------------------------------------------------------- yardımcılar
def find_source_id(rel: str) -> tuple[str, str | None]:
    for ext in (".pdf", ".pptx", ".docx", ".ppt", ".doc", ""):
        sid, did = lib.source_id_for(rel + ext)
        if did:
            return sid, did
    return lib.source_id_for(rel + ".pdf")


def split_passages(text: str, target=900, overlap=120) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n(?=[•\-\u2022▪●])", text) if p.strip()]
    out, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 1 > target and buf:
            out.append(buf.strip())
            buf = buf[-overlap:] if overlap and len(buf) > overlap else ""
        buf += p + "\n"
        while len(buf) > target * 1.6:  # çok uzun paragraf
            cut = buf.rfind(". ", 0, target)
            cut = cut + 1 if cut > 200 else target
            out.append(buf[:cut].strip())
            buf = buf[max(0, cut - overlap):]
    if buf.strip():
        out.append(buf.strip())
    return [o for o in out if len(o) >= 40]


def curriculum_index():
    cur = lib.read_json(CURRICULUM, {}) or {}
    items = []
    for k in cur.get("kurullar", []):
        for l in k.get("konular", []):
            items.append({"kurul": k["kurul"], "ders": l["ders"], "konu": l["konu"], "key": lib.fold(l["konu"])})
    return items


def match_konu(meta: dict, title: str, cur_items: list[dict]):
    import difflib

    t = lib.fold(re.sub(r"^\s*\d+\s*[\)\.\-]\s*", "", title))
    best, bs = None, 0.0
    for it in cur_items:
        if meta.get("kurul") not in (None, it["kurul"]) and isinstance(meta.get("kurul"), int):
            continue
        r = difflib.SequenceMatcher(None, t, it["key"]).ratio()
        tw, iw = set(t.split()), set(it["key"].split())
        j = len(tw & iw) / max(1, len(tw | iw))
        s = 0.6 * r + 0.4 * j + (0.1 if meta.get("ders") and lib.fold(meta["ders"]) == lib.fold(it["ders"]) else 0)
        if s > bs:
            best, bs = it, s
    return (best, round(bs, 3)) if best and bs >= 0.55 else (None, round(bs, 3))


META_SYSTEM = (
    "Sen bir tıp fakültesi ders notu analiz asistanısın. Verilen ders metninden yalnızca METİNDE GEÇEN bilgileri çıkar. "
    "Tahmin etme, dışarıdan bilgi ekleme. Türkçe yaz. JSON döndür: "
    '{"ozet":"3-5 cümle","amac":"dersin amacı 1 cümle","konular":["ana başlıklar"],'
    '"hastaliklar":[],"belirtiler":[],"ilaclar":[],"genler":[],"anahtar_terimler":[]} '
    "Listelerdeki her öğe metinde aynen geçmeli."
)


def doc_metadata(text: str, use_llm: bool) -> dict:
    if not use_llm:
        return {}
    sample = text[:6500]
    try:
        # Dinamik GPU hızlandırma (RTX 4060 tam katman yükleme)
        m = lib.chat(lib.MODEL_TEXT, sample, system=META_SYSTEM, as_json=True, num_predict=1500)
    except Exception as e:  # noqa: BLE001
        log.warning("metadata LLM hatası: %s", e)
        return {}
    ftext = lib.fold(text)
    clean = {}
    for k in ("ozet", "amac"):
        if isinstance(m.get(k), str):
            clean[k] = m[k].strip()
    for k in ("konular", "hastaliklar", "belirtiler", "ilaclar", "genler", "anahtar_terimler"):
        vals = m.get(k) if isinstance(m.get(k), list) else []
        keep = [str(v).strip() for v in vals if str(v).strip() and lib.fold(str(v)) and lib.fold(str(v)) in ftext]
        clean[k] = list(dict.fromkeys(keep))[:40]
    return clean


# --------------------------------------------------------------------------- A) kaynaklar
def build_sources(use_llm: bool, state: lib.State) -> list[dict]:
    cur_items = curriculum_index()
    sources = []
    all_files = [f for f in sorted(lib.TEMP2.rglob("*.json")) if lib.read_json(f, {}).get("meta", {}).get("doc_type") == "lecture_slide"]
    total_files = len(all_files)
    for idx_f, f in enumerate(all_files, 1):
        d = lib.read_json(f, {})
        rel = d["rel"]
        state.set_progress(rel, idx_f, total_files, f"Aşama 3 Slayt RAG & Vektör ({idx_f}/{total_files})")
        sid, did = find_source_id(rel)
        h = d.get("source_sha256") or ""
        key = f"{sid}:{h}:{len(cur_items)}"
        if not state.needs("stage3_src", sid, key) and (SRC_DIR / f"{sid}.json").exists():
            sources.append(lib.read_json(SRC_DIR / f"{sid}.json"))
            continue
        meta = d["meta"]
        title = Path(rel).name
        konu, kscore = match_konu(meta, title, cur_items)
        full = "\n\n".join(p["text"] for p in d["pages"])
        md = doc_metadata(full, use_llm)
        src = {"source_id": sid, "drive_id": did or "", "name": Path(rel).name, "path": rel, "md5": h[:32],
               "version": 1, "doc_type": "lecture_slide", "donem": meta["donem"], "kurul": meta["kurul"],
               "ders": meta["ders"] or (konu["ders"] if konu else None), "pages": d["page_count"],
               "extraction": "mixed" if any(p.get("method") not in ("metin", None) for p in d["pages"]) else "text",
               "quality_score": d["quality"], "konu": konu["konu"] if konu else None, "konu_eslesme_skoru": kscore,
               "metadata": md, "metadata_uretici": lib.MODEL_TEXT if md else None}
        # chunk'lar
        chunks = []
        for p in d["pages"]:
            head = (p["text"].split("\n", 1)[0] or "")[:120]
            for ci, ps in enumerate(split_passages(p["text"])):
                chunks.append({"chunk_id": f"{sid}:p{p['n']}:c{ci}", "source_id": sid, "page": p["n"],
                               "heading_path": [src["ders"] or "", head] if head else [src["ders"] or ""],
                               "text": ps, "doc_type": "lecture_slide", "donem": meta["donem"], "kurul": meta["kurul"],
                               "ders": src["ders"], "konu": src["konu"], "quality_score": p["quality"],
                               "hash": hashlib.sha1(ps.encode()).hexdigest()[:16]})
        lib.write_json(SRC_DIR / f"{sid}.json", src)
        lib.write_jsonl(CHUNK_DIR / f"{sid}.jsonl", chunks)
        if chunks and lib.ollama_up():
            try:
                vecs = embed_cached([c["text"] for c in chunks])
                VEC_DIR.mkdir(parents=True, exist_ok=True)
                np.save(VEC_DIR / f"{sid}.npy", vecs)
            except Exception as e:  # noqa: BLE001
                log.warning("embedding hatası %s: %s", sid, e)
        state.done("stage3_src", sid, key)
        sources.append(src)
        log.info("temp3 kaynak ✓ %s  chunk=%d  konu=%s (%.2f)", src["name"][:50], len(chunks), src["konu"], kscore)
    return sources


# --------------------------------------------------------------------------- B) sorular
def qtext(q: dict) -> str:
    return q["stem"] + " " + " ".join(q["options"].values())


def qkey(q: dict) -> str:
    return lib.fold(q["stem"]) + "|" + "|".join(sorted(lib.fold(v) for v in q["options"].values()))


def collect_questions() -> list[dict]:
    out = []
    for f in sorted(lib.TEMP2.rglob("*.json")):
        d = lib.read_json(f, {})
        if d.get("meta", {}).get("doc_type") != "past_question":
            continue
        sid, _ = find_source_id(d["rel"])
        yr = re.search(r"(\d{2})\s*[-–]\s*(\d{2})|(20\d{2})", d["rel"])
        for q in d.get("questions", []):
            qq = dict(q)
            qq.update({"doc_rel": d["rel"], "doc_source_id": sid, "donem": d["meta"]["donem"], "kurul_hint": d["meta"]["kurul"],
                       "year_hint": yr.group(0) if yr else None})
            out.append(qq)
    return out


def dedupe(qs: list[dict]) -> list[dict]:
    groups: dict[str, dict] = {}
    for q in qs:
        k = qkey(q)
        if k in groups:
            g = groups[k]
            g["seen_in"].append({"doc": q["doc_rel"], "no": q.get("no"), "year": q["year_hint"]})
            if not g.get("answer") and q.get("answer"):
                g["answer"] = q["answer"]
        else:
            q["seen_in"] = [{"doc": q["doc_rel"], "no": q.get("no"), "year": q["year_hint"]}]
            groups[k] = q
    uniq = list(groups.values())
    # anlamsal yakın tekrarlar (soru köküne göre) — yalnız aynı şık kümesi çoğunlukla örtüşüyorsa birleştir
    if len(uniq) > 1 and lib.ollama_up():
        try:
            E = embed_cached([u["stem"] for u in uniq])
            keep, merged = [], set()
            for i, u in enumerate(uniq):
                if i in merged:
                    continue
                sims = E[i + 1:] @ E[i] if i + 1 < len(uniq) else []
                for off, s in enumerate(sims):
                    j = i + 1 + off
                    if j in merged or s < 0.95:
                        continue
                    a = set(lib.tokens(" ".join(u["options"].values())))
                    b = set(lib.tokens(" ".join(uniq[j]["options"].values())))
                    if a and b and len(a & b) / len(a | b) >= 0.7:
                        u["seen_in"] += uniq[j]["seen_in"]
                        u["dedupe_near"] = u.get("dedupe_near", 0) + 1
                        if not u.get("answer") and uniq[j].get("answer"):
                            u["answer"] = uniq[j]["answer"]
                        merged.add(j)
                keep.append(u)
            uniq = keep
        except Exception as e:  # noqa: BLE001
            log.warning("anlamsal tekilleştirme atlandı: %s", e)
    return uniq


class Index:
    """Tüm chunk'lar: vektör matrisi + IDF + kaynak bilgisi."""

    def __init__(self, sources: list[dict]):
        self.chunks, vecs = [], []
        by_sid = {s["source_id"]: s for s in sources}
        self.src = by_sid
        for sid in by_sid:
            ch = lib.read_jsonl(CHUNK_DIR / f"{sid}.jsonl")
            vp = VEC_DIR / f"{sid}.npy"
            if not ch or not vp.exists():
                continue
            v = np.load(vp)
            if len(v) != len(ch):
                continue
            self.chunks += ch
            vecs.append(v)
        self.V = np.vstack(vecs) if vecs else np.zeros((0, 1024), dtype="float32")
        df = Counter()
        self.toks = []
        for c in self.chunks:
            t = set(lib.tokens(c["text"])) - STOP
            self.toks.append(t)
            df.update(t)
        n = max(1, len(self.chunks))
        self.idf = {t: math.log(1 + n / (1 + c)) for t, c in df.items()}
        self.rare = {t for t, c in df.items() if c <= max(3, n * 0.01)}

    def query(self, q: dict, qvec: np.ndarray, kurul_hint):
        if not len(self.chunks):
            return []
        cos = self.V @ qvec
        top = np.argsort(-cos)[:40]
        qt = set(lib.tokens(qtext(q))) - STOP
        qi = sum(self.idf.get(t, 1.0) for t in qt) or 1.0
        res = []
        for i in top:
            c = self.chunks[i]
            ct = self.toks[i]
            lex = sum(self.idf.get(t, 1.0) for t in qt & ct) / qi
            terms = sorted(t for t in qt & ct if t in self.rare)
            score = 0.65 * float(cos[i]) + 0.25 * lex + 0.10 * min(1.0, len(terms) / 4)
            if isinstance(kurul_hint, int) and c.get("kurul") == kurul_hint:
                score += 0.03
            res.append({"chunk_id": c["chunk_id"], "source_id": c["source_id"], "score": round(score, 4),
                        "cos": round(float(cos[i]), 4), "terms": terms, "kurul": c.get("kurul")})
        res.sort(key=lambda r: -r["score"])
        return res


def decide(q: dict, hits: list[dict], idx: Index) -> dict:
    """Kaynak kararı: kesin / aday / yok + gerekçe."""
    if not hits:
        return {"durum": "yok", "neden": "eşleşen chunk yok"}
    best_by_src: dict[str, dict] = {}
    for h in hits:
        if h["source_id"] not in best_by_src:
            best_by_src[h["source_id"]] = h
    ranked = sorted(best_by_src.values(), key=lambda h: -h["score"])
    top = ranked[0]
    second = ranked[1]["score"] if len(ranked) > 1 else 0.0
    margin = top["score"] - second
    reasons = []
    ok = True
    if top["score"] < T_SCORE:
        ok = False
        reasons.append(f"skor düşük ({top['score']:.2f}<{T_SCORE})")
    if margin < T_MARGIN:
        ok = False
        reasons.append(f"ikinci kaynakla fark az ({margin:.3f})")
    if len(top["terms"]) < T_TERMS:
        ok = False
        reasons.append(f"ortak ayırt edici terim az ({len(top['terms'])})")
    kh = q.get("kurul_hint")
    if isinstance(kh, int) and isinstance(top.get("kurul"), int) and kh != top["kurul"]:
        ok = False
        reasons.append(f"kurul çelişkisi (soru {kh}, kaynak {top['kurul']}): dönem/kurul karışmış olabilir")
    s = idx.src[top["source_id"]]
    return {"durum": "kesin" if ok else "aday", "neden": "; ".join(reasons) or "eşikler sağlandı",
            "kaynak": top["source_id"], "kanit_chunk": top["chunk_id"], "skor": top["score"], "fark": round(margin, 4),
            "ortak_terimler": top["terms"][:8], "ders": s.get("ders"), "konu": s.get("konu"), "kurul": s.get("kurul"),
            "adaylar": [{"kaynak": r["source_id"], "skor": r["score"]} for r in ranked[:3]]}


ENRICH_SYSTEM = (
    "Sen uzman bir tıp fakültesi öğretim üyesi ve sınav komisyonu editörüsün. "
    "Öğrencilerin sınav çıkışı hatırda kalan yarım/eksik not ettiği tıp sorularını, amfi ders slaytındaki "
    "kanıt parçasını kullanarak tam ve akademik bir soruya dönüştüreceksin. "
    "DERS NOTUNDA OLMAYAN DIŞ BİLGİ EKLEME; SADECE KAYNAKTAKİ BİLGİLERİ KULLAN.\n\n"
    "GÖREVLER:\n"
    "1. Soru kökü eksik, yarım, bozuk veya tek kelimelikse (örn: '76) en sık ve en nadir kmp sırasıyla nedir') "
    "bunu ders notundaki tıbbi bağlama ve terminolojiye göre tam, anlaşılır ve akademik bir soru köküne dönüştür ('stem_detayli'). "
    "Orijinal anlamı veya doğru cevabı değiştirme.\n"
    "2. 'aciklama': Doğru cevabın ders notundaki doğrudan gerekçesi (1-3 net akademik cümle).\n"
    "3. 'eksik_siklar': Eksik şıklar varsa ders notundaki çeldirici terimlerle 5 şıkka tamamla.\n"
    "4. 'metadata': Sorunun ne sorduğu, hangi klinik hedefi içerdiği ve etiketleri.\n\n"
    "JSON formatında döndür:\n"
    "{\n"
    '  "stem_detayli": "Genişletilmiş ve tamamlanmış akademik soru kökü",\n'
    '  "aciklama": "Slayttan kanıtlı doğru cevap gerekçesi",\n'
    '  "eksik_siklar": {"D": "çeldirici 1", "E": "çeldirici 2"},\n'
    '  "ne_sormus": "Sorunun ölçtüğü temel bilgi veya patoloji",\n'
    '  "alt_konu": "İlgili slayt alt başlığı",\n'
    '  "terimler": ["Hastalık1", "Belirti1", "Gen/İlaç1"]\n'
    "}"
)


def enrich(q: dict, chunk_text: str, chunk_id: str) -> dict | None:
    import json as _j

    payload = {"soru": {"kok": q["stem"], "siklar": q["options"], "cevap": q.get("answer")}, "kaynak": chunk_text[:2500]}
    try:
        r = lib.chat(lib.MODEL_TEXT, _j.dumps(payload, ensure_ascii=False), system=ENRICH_SYSTEM, as_json=True, num_predict=900)
    except Exception as e:  # noqa: BLE001
        log.warning("zenginleştirme hatası: %s", e)
        return None
    src_t = set(lib.tokens(chunk_text)) | set(lib.tokens(qtext(q)))
    out = {}

    def sup(s):
        tk = lib.tokens(s)
        return sum(t in src_t for t in tk) / len(tk) if tk else 1.0

    ac = r.get("aciklama")
    if isinstance(ac, str) and ac.strip() and q.get("answer") and sup(ac) >= 0.80:
        out["explanation"] = ac.strip()
    sd = r.get("stem_detayli")
    if isinstance(sd, str) and sd.strip():
        # Yarım/hatırda kalan sorular kökten uzayabilir (örn 30 karakterden 150 karaktere)
        # Dolayısıyla esnek üst sınır koyulur ve kelimelerin en az %75'i kaynakla desteklenir
        if len(sd.strip()) > len(q["stem"]) and sup(sd) >= 0.75:
            out["stem_detailed"] = sd.strip()
    es = r.get("eksik_siklar")
    if isinstance(es, dict):
        added = {}
        existing = {lib.fold(v) for v in q["options"].values()}
        for k, v in es.items():
            k = str(k).upper()
            v = str(v).strip()
            if k in "ABCDE" and k not in q["options"] and v and lib.fold(v) not in existing and lib.fold(v) in lib.fold(chunk_text):
                added[k] = v
        if added:
            out["options_added"] = added

    # Zengin Tıbbi Metadata & Taksonomi Havuzu
    metadata_tax = {}
    if r.get("ne_sormus"):
        metadata_tax["ne_sormus"] = str(r["ne_sormus"]).strip()
    if r.get("alt_konu"):
        metadata_tax["alt_konu"] = str(r["alt_konu"]).strip()
    if isinstance(r.get("terimler"), list):
        metadata_tax["terimler"] = [str(t).strip() for t in r["terimler"] if str(t).strip()]
    if metadata_tax:
        out["taxonomy_metadata"] = metadata_tax

    return out or None


def build_questions(sources: list[dict], use_llm: bool, do_enrich: bool, state: lib.State):
    qs = collect_questions()
    uniq = dedupe(qs)
    log.info("sorular: %d ham -> %d tekil", len(qs), len(uniq))
    idx = Index(sources)
    log.info("indeks: %d chunk, %d kaynak", len(idx.chunks), len(idx.src))
    out, review = [], []
    if uniq and len(idx.chunks) and lib.ollama_up():
        QV = embed_cached([qtext(u) for u in uniq])
    else:
        QV = None
    ch_by_id = {c["chunk_id"]: c for c in idx.chunks}
    total_u = len(uniq)
    # Varsa önceki zenginleştirilmiş soruları al
    prev = {}
    q_prev_path = lib.TEMP3 / "questions.jsonl"
    if q_prev_path.exists():
        try:
            for item in lib.read_jsonl(q_prev_path):
                if item.get("question_id"):
                    prev[item["question_id"]] = item
        except Exception:
            pass

    for i, u in enumerate(uniq):
        qid = hashlib.sha1(qkey(u).encode()).hexdigest()[:12]
        if i % 5 == 0:
            state.set_progress("Sorular", i + 1, total_u, f"Soru Eşleştirme & Zenginleştirme ({i+1}/{total_u})")
        base = {"question_id": qid, "donem": u["donem"], "kurul": u["kurul_hint"], "stem": u["stem"], "options": u["options"],
                "answer": u.get("answer"), "explanation": None, "issues": list(u.get("issues", [])),
                "seen_in": u["seen_in"][:12], "extraction": u.get("extraction"), "evidence": [], "ders": None,
                "konu": None, "source_id": None, "status": "raw",
                "pipeline_generation": "v2_local_pipeline_2026",
                "tags": ["new_pipeline", "v2_verified", "local_ai_extracted"]}
        if len(u["options"]) < 2 or len(u["stem"]) < 12:
            base.update(status="rejected", issues=base["issues"] + ["yapı yetersiz"])
            review.append(base)
            continue
        if QV is None:
            base["status"] = "needs_fix"
            base["issues"].append("anlamsal eşleştirme yapılamadı (Ollama/embedding yok)")
            review.append(base)
            continue
        hits = idx.query(u, QV[i], u["kurul_hint"])
        dec = decide(u, hits, idx)
        base["match"] = dec
        base["entities"] = dec.get("ortak_terimler", [])
        
        # Destek oranı (support_ratio) hesaplaması: Soru metninin amfi notundaki kelime karşılığı
        cand_chunk_text = ch_by_id[dec["kanit_chunk"]]["text"] if dec.get("kanit_chunk") and dec["kanit_chunk"] in ch_by_id else ""
        cand_tokens = set(lib.tokens(cand_chunk_text))
        q_tokens = set(lib.tokens(qtext(u))) - STOP
        support_ratio = (len(q_tokens & cand_tokens) / len(q_tokens)) if q_tokens else 0.0
        base["support_ratio"] = round(float(support_ratio), 4)

        if dec["durum"] == "kesin":
            base.update(source_id=dec["kaynak"], ders=dec["ders"], konu=dec["konu"], evidence=[dec["kanit_chunk"]])
            if isinstance(dec.get("kurul"), int):
                base["kurul"] = dec["kurul"] if base["kurul"] in (None, "final") else base["kurul"]
            
            # Hakem Ajan Kuralları:
            # support_ratio >= 0.85: Otomatik onayla (verified)
            # 0.65 <= support_ratio < 0.85: Hakem Ajan (DeepSeek-R1) kuyruğu (referee_queue)
            # support_ratio < 0.65: Eksik slayt / inceleme (needs_fix)
            if support_ratio >= T_VERIFIED_SUPPORT:
                base["status"] = "verified"
            elif support_ratio >= T_REFEREE_SUPPORT:
                base["status"] = "referee_queue"
                base["issues"].append(f"Hakem Ajan (DeepSeek-R1) incelemesi bekliyor (destek={support_ratio:.2f})")
            else:
                base["status"] = "needs_fix"
                base["issues"].append(f"Slayt desteği sınırda veya yetersiz ({support_ratio:.2f} < {T_REFEREE_SUPPORT})")

            old = prev.get(qid)
            if do_enrich and use_llm and old and old.get("enrichment_done"):
                for k in ("enrichment", "explanation", "stem_detailed", "options_added", "enrichment_done"):
                    if k in old:
                        base[k] = old[k]
            elif do_enrich and use_llm and base["status"] in ("verified", "referee_queue"):
                e = enrich(u, ch_by_id[dec["kanit_chunk"]]["text"], dec["kanit_chunk"])
                base["enrichment_done"] = True
                if e:
                    base["enrichment"] = e
                    if "explanation" in e:
                        base["explanation"] = e["explanation"]
                    if "stem_detailed" in e:
                        base["stem_detailed"] = e["stem_detailed"]
                    if "options_added" in e:
                        base["options_added"] = e["options_added"]
                    if "taxonomy_metadata" in e:
                        base["taxonomy_metadata"] = e["taxonomy_metadata"]
                    if base["status"] == "verified":
                        base["status"] = "fixed"
                    # Dashboard canlı dönüşüm tablosuna bas
                    orig_sample = f"{u['stem'][:150]} (Şıklar: {len(u['options'])})"
                    new_sample = f"{base.get('stem_detailed') or u['stem'][:150]} (Açıklama: {base.get('explanation', '')[:100]}...)"
                    state.add_transformation(f"Kurul {base['kurul']} / Soru {u.get('no', '')}", "Aşama 3 Soru Zenginleştirme", orig_sample, new_sample)
            
            if base["status"] in ("verified", "fixed"):
                out.append(base)
            else:
                review.append(base)
        else:
            base["status"] = "needs_fix"
            base["issues"].append("kaynak kesinleşmedi: " + dec["neden"])
            base["source_id"] = dec.get("kaynak")
            review.append(base)
    lib.write_jsonl(lib.TEMP3 / "questions.jsonl", out)
    lib.write_jsonl(lib.TEMP3 / "review_queue.jsonl", review)
    rep = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "ham_soru": len(qs), "tekil": len(uniq), "kaynak": len(sources),
           "chunk": len(idx.chunks), "verified": sum(1 for x in out if x["status"] == "verified"),
           "fixed": sum(1 for x in out if x["status"] == "fixed"), "incelemeye": len(review)}
    lib.write_json(lib.TEMP3 / "report.json", rep)
    log.info("temp3 sorular ✓ %s", rep)
    return rep


def run(use_llm=True, do_enrich=True):
    state = lib.State()
    ok_ollama = lib.ollama_up()
    sources = build_sources(use_llm and ok_ollama, state)
    return build_questions(sources, use_llm and ok_ollama, do_enrich, state)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--skip-enrich", action="store_true")
    a = ap.parse_args()
    print(run(not a.no_llm, not a.skip_enrich))
