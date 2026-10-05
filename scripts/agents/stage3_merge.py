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

import os

# 20 çekirdeğin tamamını vektörel BLAS ve matris işlemlerine tahsis et (numpy importundan önce)
os.environ["OMP_NUM_THREADS"] = "20"
os.environ["MKL_NUM_THREADS"] = "20"
os.environ["OPENBLAS_NUM_THREADS"] = "20"
os.environ["VECLIB_MAXIMUM_THREADS"] = "20"
os.environ["NUMEXPR_NUM_THREADS"] = "20"

import argparse
import concurrent.futures
import hashlib
import json
import math
import pickle
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

try:
    import orjson
except ImportError:
    orjson = None

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
NUM_GPU_WORKERS = int(os.environ.get("MEDS_GPU_WORKERS", "3"))  # RTX 4060 8GB VRAM eşzamanlı LLM sorgu limiti

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


def embed_cached(texts: list[str], batch_size: int = 64) -> np.ndarray:
    if not texts:
        return np.zeros((0, 1024), dtype="float32")

    keys = [hashlib.sha1((lib.MODEL_EMBED + t).encode()).hexdigest() for t in texts]
    miss = [i for i, k in enumerate(keys) if k not in _disk_cache]

    if miss:
        # RTX 4060 8GB VRAM için 64'lük mini-batch'ler halinde işle
        for b_start in range(0, len(miss), batch_size):
            batch_idx = miss[b_start : b_start + batch_size]
            sub_texts = [texts[i][:2000] for i in batch_idx]
            vecs = lib.embed(sub_texts)
            with _disk_cache.transact():
                for idx, v in zip(batch_idx, vecs):
                    _disk_cache[keys[idx]] = v

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


def layout_aware_chunk(text: str, target: int = 1000, overlap: int = 120) -> list[str]:
    """
    Layout-Aware & Slayt Tabanlı Akıllı Parçalama:
    1. Slayt metni 1100 karakterin altındaysa bölmeden tek parça olarak korur.
    2. Markdown tablolarını (| col | col |) ve madde işaretli klinik listeleri asla ortadan koparmaz.
    3. Cümle sonlarını kontrol ederken tıbbi kısaltmaları korur.
    """
    text = text.strip()
    if not text:
        return []
    
    # Slayt zaten doğal bir semantik birimdir. 1100 karakterin altındaysa tek parça sakla
    if len(text) <= 1100:
        return [text]

    lines = text.split("\n")
    chunks, buf = [], ""
    
    for line in lines:
        line_str = line.strip()
        is_table_row = "|" in line_str
        is_list_item = bool(re.match(r"^\s*([•\-\u2022▪●*]|\d+[\.\)])", line_str))
        
        # Eğer henüz hedef boyuta ulaşmadıysak veya tablo/liste içindeysek satırı ekle
        if len(buf) + len(line) + 1 <= target:
            buf += line + "\n"
        else:
            # Hedef boyut aşıldı: Eğer tablo veya liste bloğundaysak bütünlüğü bozmamak için esne
            if (is_table_row or is_list_item) and len(buf) < target * 1.5:
                buf += line + "\n"
            else:
                if buf.strip():
                    chunks.append(buf.strip())
                # Overlap: Son satırlardan veya karakterlerden örtüşme al
                buf = (buf[-overlap:] if overlap and len(buf) > overlap else "") + line + "\n"

    if buf.strip():
        chunks.append(buf.strip())

    return [c for c in chunks if len(c) >= 30]


# Geriye dönük uyumluluk takma adı
split_passages = layout_aware_chunk


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
        # chunk'lar (Öksüz Veri Çözümü: Context Metadata Injection)
        chunks = []
        kurul_str = f"Komite {meta['kurul']}" if meta.get("kurul") else "Genel Komite"
        ders_str = src["ders"] or "Genel Tıp"
        konu_str = src["konu"] or title
        
        for p in d["pages"]:
            head = (p["text"].split("\n", 1)[0] or "").strip()[:120]
            context_prefix = f"[{kurul_str} | {ders_str} | Başlık: {head or konu_str}]\n"
            slide_full_text = f"{context_prefix}{p['text']}"
            for ci, ps in enumerate(split_passages(p["text"])):
                # Metnin başına statik bağlam bilgisini ekle (Child chunk)
                enriched_text = f"{context_prefix}{ps}"
                chunks.append({"chunk_id": f"{sid}:p{p['n']}:c{ci}", "source_id": sid, "page": p["n"],
                               "heading_path": [src["ders"] or "", head] if head else [src["ders"] or ""],
                               "text": enriched_text, "raw_text": ps, 
                               "parent_text": slide_full_text, # Parent-Child Mimarisi: Sayfanın tam bağlamı
                               "doc_type": "lecture_slide", "donem": meta["donem"], "kurul": meta["kurul"],
                               "ders": src["ders"], "konu": src["konu"], "quality_score": p["quality"],
                               "hash": hashlib.sha1(enriched_text.encode()).hexdigest()[:16]})
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
    # anlamsal yakın tekrarlar (soru köküne göre) — Hızlı vektör matris çarpımıyla tekilleştir
    if len(uniq) > 1 and lib.ollama_up():
        try:
            E = embed_cached([u["stem"] for u in uniq])
            # E normalize edilmiş olduğu için dot product kosinüs benzerliğidir
            # E (N, 1024) @ E.T (1024, N) yerine blok blok veya üst üçgen tarama
            merged = set()
            keep = []
            
            # Blok boyutlarıyla hızlı kosinüs benzerliği
            chunk_size = 500
            for start_i in range(0, len(uniq), chunk_size):
                end_i = min(len(uniq), start_i + chunk_size)
                # (chunk_size, 1024) @ (1024, N) -> (chunk_size, N)
                sim_block = E[start_i:end_i] @ E.T
                
                for local_i, global_i in enumerate(range(start_i, end_i)):
                    if global_i in merged:
                        continue
                    # Sadece kendisinden sonraki sorulara bak
                    high_sims = np.where(sim_block[local_i, global_i + 1:] >= 0.95)[0]
                    for off in high_sims:
                        j = global_i + 1 + off
                        if j in merged:
                            continue
                        a = set(lib.tokens(" ".join(uniq[global_i]["options"].values())))
                        b = set(lib.tokens(" ".join(uniq[j]["options"].values())))
                        if a and b and len(a & b) / len(a | b) >= 0.7:
                            uniq[global_i]["seen_in"] += uniq[j]["seen_in"]
                            uniq[global_i]["dedupe_near"] = uniq[global_i].get("dedupe_near", 0) + 1
                            if not uniq[global_i].get("answer") and uniq[j].get("answer"):
                                uniq[global_i]["answer"] = uniq[j]["answer"]
                            merged.add(j)
                    keep.append(uniq[global_i])
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
        k = min(40, len(cos))
        if len(cos) > k:
            part = np.argpartition(-cos, k)[:k]
            top = part[np.argsort(-cos[part])]
        else:
            top = np.argsort(-cos)
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
    "Sen uzman bir tıp fakültesi öğretim üyesi ve sınav komisyonu başkanısın.\n"
    "DERS NOTUNDA OLMAYAN DIŞ BİLGİ EKLEME; SADECE SANA VERİLEN <SLAYT_KANITLARI> İÇERİĞİNDEKİ BİLGİLERİ KULLAN.\n\n"
    "ZORUNLU KURALLAR:\n"
    "1. ÇELDİRİCİ & NEGATİF KANIT ANALİZİ: Yalnızca doğru cevabı açıklamakla yetinme. Her şıkkı incele;\n"
    "   - Doğru şık için: [Destekleniyor / Slayt Gerekçesi]\n"
    "   - Çeldirici şıklar için: [Eleniyor / Neden yanlış olduğu ve Slayt Çelişkisi]\n"
    "2. CITATION GROUNDING: Açıklamadaki her akademik cümlenin sonuna kanıt etiketini ekle: [Kaynak: {chunk_id}].\n"
    "3. Soru kökünü eksik/hatırda kalan kısımları slayta dayandırarak akademik dille genişlet.\n\n"
    "JSON formatında döndür:\n"
    "{\n"
    '  "analiz": "Adım adım klinik ve patolojik akıl yürütme",\n'
    '  "stem_detayli": "Genişletilmiş ve tamamlanmış akademik soru kökü",\n'
    '  "aciklama": "Slayttan kanıtlı doğru cevap gerekçesi [Kaynak: {chunk_id}]",\n'
    '  "siklar_analizi": {\n'
    '     "A": "[Destekleniyor / Eleniyor] Gerekçe...",\n'
    '     "B": "[Destekleniyor / Eleniyor] Gerekçe..."\n'
    '  },\n'
    '  "eksik_siklar": {"D": "çeldirici 1", "E": "çeldirici 2"},\n'
    '  "ne_sormus": "Sorunun ölçtüğü temel klinik patoloji",\n'
    '  "alt_konu": "İlgili slayt alt başlığı",\n'
    '  "terimler": ["Hastalık1", "Belirti1", "Gen/İlaç1"]\n'
    "}"
)


def enrich(q: dict, chunk_text: str, chunk_id: str) -> dict | None:
    import json as _j

    system_prompt = ENRICH_SYSTEM.replace("{chunk_id}", chunk_id)
    structured_user_prompt = (
        "Aşağıdaki <SLAYT_KANITLARI> içeriğine dayanarak <SORU>yu incele, her şıkkı gerekçelendir ve zenginleştir:\n\n"
        f"<SLAYT_KANITLARI>\n{chunk_text[:2200]}\n</SLAYT_KANITLARI>\n\n"
        f"<SORU>\n"
        f"Kök: {q['stem']}\n"
        f"Şıklar: {_j.dumps(q.get('options', {}), ensure_ascii=False)}\n"
        f"Doğru Cevap: {q.get('answer') or 'Bilinmiyor'}\n"
        f"</SORU>\n\n"
        "Yukarıdaki negatif kanıt ve citation grounding kurallarına uyarak sonucu geçerli bir JSON olarak döndür."
    )

    try:
        # 900 token ve 45 saniye zaman aşımı: Modelin gereksiz asılı kalmasını önler
        r = lib.chat(lib.MODEL_TEXT, structured_user_prompt, system=system_prompt, as_json=True, num_predict=900, timeout=45)
    except Exception as e:  # noqa: BLE001
        log.warning("zenginleştirme hatası: %s", e)
        return None
    src_t = set(lib.tokens(chunk_text)) | set(lib.tokens(qtext(q)))
    out = {}

    def sup(s):
        tk = lib.tokens(s)
        return sum(t in src_t for t in tk) / len(tk) if tk else 1.0

    ac = r.get("aciklama")
    if isinstance(ac, str) and ac.strip() and q.get("answer") and sup(ac) >= 0.70:
        out["explanation"] = ac.strip()
    sd = r.get("stem_detayli")
    if isinstance(sd, str) and sd.strip():
        if len(sd.strip()) > len(q["stem"]) and sup(sd) >= 0.70:
            out["stem_detailed"] = sd.strip()
    
    # Negatif Kanıt / Çeldirici Analizi
    sa = r.get("siklar_analizi")
    if isinstance(sa, dict) and sa:
        out["options_analysis"] = sa

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
    # ---------------- Checkpoint & Kaldığı Yerden Devam Etme (Zero-Data-Loss) ----------------
    checkpoint_q_path = lib.TEMP3 / "questions.jsonl"
    checkpoint_r_path = lib.TEMP3 / "review_queue.jsonl"
    prev = {}
    
    # Halihazırda işlenmiş soruları hızlıca hafızaya al
    processed_qids = set()
    if checkpoint_q_path.exists():
        try:
            for item in lib.read_jsonl(checkpoint_q_path):
                if item.get("question_id"):
                    qid = item["question_id"]
                    out.append(item)
                    processed_qids.add(qid)
                    prev[qid] = item
        except Exception as e:
            log.warning("Önceki questions.jsonl okunurken hata: %s", e)

    if checkpoint_r_path.exists():
        try:
            for item in lib.read_jsonl(checkpoint_r_path):
                if item.get("question_id"):
                    qid = item["question_id"]
                    review.append(item)
                    processed_qids.add(qid)
        except Exception as e:
            log.warning("Önceki review_queue.jsonl okunurken hata: %s", e)

    if processed_qids:
        log.info("Checkpoint bulundu: %d soru zaten işlenmiş, doğrudan kaldığı yerden devam ediliyor ✓", len(processed_qids))

    q_file_append = open(checkpoint_q_path, "a", encoding="utf-8")
    r_file_append = open(checkpoint_r_path, "a", encoding="utf-8")

    write_counter = 0
    def write_record(record: dict, force_flush: bool = False):
        nonlocal out, review, write_counter
        row_str = (orjson.dumps(record).decode("utf-8") if orjson else json.dumps(record, ensure_ascii=False)) + "\n"
        if record["status"] in ("verified", "fixed"):
            out.append(record)
            q_file_append.write(row_str)
        else:
            review.append(record)
            r_file_append.write(row_str)
        
        write_counter += 1
        if force_flush or write_counter % 10 == 0:
            q_file_append.flush()
            r_file_append.flush()
        processed_qids.add(record["question_id"])

    def enrich_worker(task):
        u_obj, base_obj, dec_obj = task
        try:
            matched_c = ch_by_id[dec_obj["kanit_chunk"]]
            context_for_llm = matched_c.get("parent_text") or matched_c["text"]
            e = enrich(u_obj, context_for_llm, dec_obj["kanit_chunk"])
            return task, e
        except Exception as ex:  # noqa: BLE001
            log.warning("enrich_worker hata: %s", ex)
            return task, None

    def process_enrichment_batch(batch_tasks):
        if not batch_tasks:
            return
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_GPU_WORKERS) as pool:
            futures = [pool.submit(enrich_worker, t) for t in batch_tasks]
            for fut in concurrent.futures.as_completed(futures):
                (u_obj, base_obj, dec_obj), e = fut.result()
                base_obj["enrichment_done"] = True
                if e:
                    base_obj["enrichment"] = e
                    if "explanation" in e:
                        base_obj["explanation"] = e["explanation"]
                    if "stem_detailed" in e:
                        base_obj["stem_detailed"] = e["stem_detailed"]
                    if "options_added" in e:
                        base_obj["options_added"] = e["options_added"]
                    if "options_analysis" in e:
                        base_obj["options_analysis"] = e["options_analysis"]
                    if "taxonomy_metadata" in e:
                        base_obj["taxonomy_metadata"] = e["taxonomy_metadata"]
                    if base_obj["status"] == "verified":
                        base_obj["status"] = "fixed"
                    orig_sample = f"{u_obj['stem'][:150]} (Şıklar: {len(u_obj['options'])})"
                    expl_str = base_obj.get("explanation") or ""
                    new_sample = f"{base_obj.get('stem_detailed') or u_obj['stem'][:150]} (Açıklama: {expl_str[:100]}...)"
                    state.add_transformation(
                        f"Kurul {base_obj['kurul']} / Soru {u_obj.get('no', '')}",
                        "Aşama 3 Soru Zenginleştirme",
                        orig_sample,
                        new_sample
                    )
                write_record(base_obj)

    enrich_batch = []
    ENRICH_BATCH_SIZE = NUM_GPU_WORKERS * 2

    try:
        for i, u in enumerate(uniq):
            qid = hashlib.sha1(qkey(u).encode()).hexdigest()[:12]
            
            # Soru zaten işlenmişse LLM/GPU çağırmadan anında atla
            if qid in processed_qids:
                continue

            if (i + 1) % 5 == 0 or i == 0:
                state.set_progress("Sorular", i + 1, total_u, f"Soru Eşleştirme & Zenginleştirme ({i+1}/{total_u})")
            base = {"question_id": qid, "donem": u["donem"], "kurul": u["kurul_hint"], "stem": u["stem"], "options": u["options"],
                    "answer": u.get("answer"), "explanation": None, "issues": list(u.get("issues", [])),
                    "seen_in": u["seen_in"][:12], "extraction": u.get("extraction"), "evidence": [], "ders": None,
                    "konu": None, "source_id": None, "status": "raw",
                    "pipeline_generation": "v2_local_pipeline_2026",
                    "tags": ["new_pipeline", "v2_verified", "local_ai_extracted"]}
            if len(u["options"]) < 2 or len(u["stem"]) < 12:
                base.update(status="rejected", issues=base["issues"] + ["yapı yetersiz"])
                write_record(base)
                continue
            if QV is None:
                base["status"] = "needs_fix"
                base["issues"].append("anlamsal eşleştirme yapılamadı (Ollama/embedding yok)")
                write_record(base)
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
                    write_record(base)
                elif do_enrich and use_llm and base["status"] in ("verified", "referee_queue"):
                    enrich_batch.append((u, base, dec))
                    if len(enrich_batch) >= ENRICH_BATCH_SIZE:
                        process_enrichment_batch(enrich_batch)
                        enrich_batch.clear()
                else:
                    write_record(base)
            else:
                base["status"] = "needs_fix"
                base["issues"].append("kaynak kesinleşmedi: " + dec["neden"])
                base["source_id"] = dec.get("kaynak")
                write_record(base)

        # Kalan son zenginleştirme havuzunu temizle
        if enrich_batch:
            process_enrichment_batch(enrich_batch)
            enrich_batch.clear()
    finally:
        q_file_append.close()
        r_file_append.close()

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
