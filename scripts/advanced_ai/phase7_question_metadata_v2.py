#!/usr/bin/env python3
"""
Faz 7 v2 — Kanıta dayalı soru metadatası (hikâyeleştirme YOK)

Eski Faz 7 karantinada (yedek/faz7_hikaye_silindi_20261007/phase7_stories/KARANTINA.md (Faz 7 hikâye üretimi 2026-10-07 silindi)). Bu sürüm yalnızca soruyu ve konuyu anlayıp
doğrulanabilir metadata çıkarır:
  * soru tipi (olumlu/olumsuz kök), ne soruyor, konu (Faz 8 yüksek güven)
  * tıbbi varlıklar (terim + tür) — her terim soru metninde ya da ders kanıtında geçmek ZORUNDA, yoksa atılır
  * slayt kanıtı: kaynak + sayfa + kanıttan BİREBİR alıntı (doğrulanmazsa alan boş kalır)
  * cevap denetimi: kanıta göre cevap ≠ kayıtlı anahtar ise `anahtar_celiskisi` (anahtar DEĞİŞTİRİLMEZ)
Modelin anladığı kadarı kaydedilir; eksik alan `eksik` listesine yazılır. Soru bir kez işlenir ve tekrar kuyruğa
girmez (yalnızca model hiç yanıt vermediyse sonraki çalıştırmada yeniden denenir).

Zincire (phase_cycle.py) EKLENMEMİŞTİR; elle çalıştırılır. Eğitim verisine yazmaz.
Çıktı: meds_database_v2/phase7_v2/soru_metadata.jsonl, rapor.json

Kullanım:
  python3 scripts/advanced_ai/phase7_question_metadata_v2.py --limit 30 --seed 7
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or PROJECT / "meds_database")
PHASE8 = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp") / "phase8" / "soru_kazanim.jsonl"
PHASE5 = PROJECT / "meds_database_v2" / "questions"
OUT = PROJECT / "meds_database_v2" / "phase7_v2"


def env_keys() -> dict:
    keys = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                keys[k.strip()] = v.strip().strip("\"'")
    return keys


ENV = env_keys()
GROQ_KEYS = [k for k in (ENV.get("GROQ_API_KEY"), ENV.get("GROQ_API_KEY_2")) if k]
GROQ_MODEL = os.environ.get("PHASE7_MODEL", "openai/gpt-oss-120b")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
import cloud_llm  # noqa: E402

NEG = re.compile(r"(yanl[ıi]şt[ıi]r|yanl[ıi]ş\s*(olan|bir)|de[ğg]ildir|de[ğg]il\b|hari[çc]|olamaz|beklenmez|g[öo]r[üu]lmez|"
                 r"yoktur|d[ıi]ş[ıi]nda|bulunmaz|kullan[ıi]lmaz|s[öo]ylenemez|ili[şs]kili de[ğg]il|en az)", re.I)


# --------------------------------------------------------------------------- yardımcılar
def fold(s: str) -> str:
    tr = str.maketrans({"ı": "i", "İ": "i", "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ö": "o", "Ö": "o", "ş": "s", "Ş": "s",
                        "ü": "u", "Ü": "u", "I": "i", "â": "a", "î": "i", "û": "u"})
    return re.sub(r"[^a-z0-9]+", " ", (s or "").translate(tr).lower()).strip()


def quote_ok(quote: str, evidence: str) -> bool:
    """Alıntı kanıtta geçiyor mu? (katlanmış metinde birebir ya da kelimelerin ≥%85'i ardışık pencerede)"""
    q, e = fold(quote), fold(evidence)
    if len(q) < 12:
        return False
    if q in e:
        return True
    qw = q.split()
    ew = e.split()
    if len(qw) < 3:
        return False
    need = max(3, int(len(qw) * 0.85))
    sq = set(qw)
    win = len(qw) + 4
    for i in range(0, max(1, len(ew) - win + 1)):
        if len(sq & set(ew[i:i + win])) >= need:
            return True
    return False


def llm_json(system: str, user: str) -> tuple[dict | None, str]:
    """Bulut zinciri (scripts/agents/cloud_llm.py; ilk model PHASE7_MODEL). Yerel model yok."""
    chain = [f"groq:{GROQ_MODEL}"] + [m for m in cloud_llm.chain() if m != f"groq:{GROQ_MODEL}"]
    res = cloud_llm.chat(user, system=system, as_json=True, max_tokens=3000, models=chain)
    return (res if isinstance(res, dict) else None), (cloud_llm.last_model.get("ad") or "bulut")


# --------------------------------------------------------------------------- kanıt
def load_chunks_index() -> dict:
    idx = {}
    for p in glob.glob(str(DB / "chunks" / "*.jsonl")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    c = json.loads(line)
                except json.JSONDecodeError:
                    continue
                idx[c["chunk_id"]] = c
    return idx


def load_sources() -> dict:
    out = {}
    for p in glob.glob(str(DB / "sources" / "*.json")):
        try:
            s = json.load(open(p, encoding="utf-8"))
            out[s["source_id"]] = s
        except Exception:
            pass
    return out


def exam_dump_ids(chunks: dict, sources: dict) -> set:
    """Sınav/soru dökümleri ders kanıtı sayılmaz (Faz 8'deki aynı ölçüt)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from phase8_curriculum_graph import is_exam_dump  # noqa: E402
    by_src: dict = {}
    for c in chunks.values():
        by_src.setdefault(c.get("source_id"), []).append(c)
    return {sid for sid, s in sources.items() if is_exam_dump(s, by_src)}


def evidence_for(qid: str, p8: dict, p5: dict, chunks: dict, dumps: set = frozenset()) -> list[dict]:
    """Faz 8 (yüksek güven) slayt kanıtı + aynı kaynaktan komşu sayfa; yoksa Faz 5 ders slaytı eşleşmesi."""
    ev = []
    r = p8.get(qid)
    if r and r.get("guven") == "yuksek":
        for k in r["kazanimlar"][:1]:
            cid = (k.get("kanit") or {}).get("chunk_id")
            if cid and cid in chunks and chunks[cid].get("source_id") not in dumps:
                ev.append(chunks[cid])
    for cid in p5.get(qid, []):
        if cid in chunks and chunks[cid].get("source_id") not in dumps and all(cid != e["chunk_id"] for e in ev):
            ev.append(chunks[cid])
        if len(ev) >= 3:
            break
    return ev[:3]


# --------------------------------------------------------------------------- metadata
SYSTEM = """Sen bir tıp fakültesi soru analistisin. Soruyu ve konusunu anlarsın; yalnızca verilen DERS KANITI ve soru
metnine dayanırsın. Açıklama, hikâye ya da yeni tıbbi bilgi YAZMAZSIN. Alıntılar kanıttan kelimesi kelimesine olur.
Emin olmadığın alanı boş bırakırsın. Kök ile şıklar birbiriyle ilgisizse ya da metin bozuksa soru_bozuk=true. Yanıtın yalnızca geçerli JSON'dur."""

VARLIK_TURLERI = "hastalik|ilac|patojen|bulgu|test|anatomi|molekul|islem|diger"


def build_prompt(q: dict, neg: bool, evidence: list[dict], konu: str | None) -> str:
    ev_txt = "\n\n".join(f"[KANIT {i + 1} | sayfa {e.get('page')}]\n" + re.sub(r"\s+", " ", e.get("text", ""))[:1800]
                          for i, e in enumerate(evidence))
    opts = "\n".join(f"{k}) {v}" for k, v in (q.get("options") or {}).items())
    tip = "OLUMSUZ kök (doğru cevap kanıta göre YANLIŞ/uymayan şıktır)" if neg else "OLUMLU kök"
    return f"""Soru tipi: {tip}. Müfredat konusu (Faz 8): {konu or "bilinmiyor"}

SORU: {q.get('stem')}
ŞIKLAR:
{opts}

DERS KANITI:
{ev_txt}

JSON:
{{"ne_soruyor": "sorunun ölçtüğü bilgi, tek kısa cümle",
  "soru_bozuk": false,
  "tibbi_varliklar": [{{"terim": "SORU/ŞIK metninde geçtiği biçimiyle", "tur": "{VARLIK_TURLERI}"}}],
  "kanita_gore_cevap": "A|B|C|D|E|BELIRSIZ",
  "kanit_alintisi": "doğru cevabı destekleyen, kanıttan birebir TAM cümle (en az 5 kelime); kanıtta yoksa boş",
  "kanit_no": 1}}"""


def extract(q: dict, evidence: list[dict], sources: dict, p8r: dict | None) -> dict:
    neg = bool(NEG.search(q.get("stem") or ""))
    key = (q.get("answer") or "").strip().upper()
    konu = None
    if p8r and p8r.get("guven") == "yuksek":
        k0 = (p8r.get("kazanimlar") or [{}])[0]
        konu = {"kurul": k0.get("kurul"), "ders": k0.get("ders"), "konu": k0.get("konu"),
                "kazanim_id": k0.get("kazanim_id"), "kazanim": k0.get("kazanim")}
    data, model = llm_json(SYSTEM, build_prompt(q, neg, evidence, (konu or {}).get("konu")))
    rec = {"question_id": q["question_id"], "soru_tipi": "olumsuz" if neg else "olumlu", "konu": konu,
           "model": model, "zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if not data:
        return {**rec, "durum": "model_yaniti_yok"}
    eksik = []
    qtext = " ".join([q.get("stem") or ""] + list((q.get("options") or {}).values()))
    ev_all = " ".join(e.get("text", "") for e in evidence)
    hay = fold(qtext)
    varliklar, atilan = [], 0
    for v in data.get("tibbi_varliklar") or []:
        if isinstance(v, str):
            v = {"terim": v}
        t = (v.get("terim") or "").strip() if isinstance(v, dict) else ""
        if 3 <= len(t) and len(t.split()) <= 5 and fold(t) and f" {fold(t)}" in f" {hay}":
            varliklar.append({"terim": t, "tur": v.get("tur") if v.get("tur") in VARLIK_TURLERI.split("|") else "diger"})
        else:
            atilan += 1
    if not varliklar:
        eksik.append("tibbi_varliklar")
    alinti = (data.get("kanit_alintisi") or "").strip()
    kanit = None
    opt_folds = {fold(o) for o in (q.get("options") or {}).values()}
    if alinti and (len(fold(alinti).split()) < 5 or fold(alinti) in opt_folds):
        alinti = ""
    if alinti and quote_ok(alinti, ev_all):
        try:
            e = evidence[max(0, int(data.get("kanit_no") or 1) - 1)]
        except (ValueError, IndexError):
            e = evidence[0]
        if not quote_ok(alinti, e.get("text", "")):
            e = next((x for x in evidence if quote_ok(alinti, x.get("text", ""))), evidence[0])
        s = sources.get(e.get("source_id"), {})
        kanit = {"kaynak": s.get("name") or e.get("source_id"), "sayfa": e.get("page"), "chunk_id": e["chunk_id"],
                 "alinti": alinti}
    else:
        eksik.append("kanit_alintisi")
    found = str(data.get("kanita_gore_cevap") or "").strip().upper()[:1]
    if found and found in "ABCDE" and kanit:
        cevap = "uyumlu" if found == key else "anahtar_celiskisi"
    else:
        cevap = "belirsiz"
    if data.get("soru_bozuk") is True:
        eksik.append("soru_bozuk")
    return {**rec, "durum": "tamam" if not eksik else "kismi", "soru_bozuk": data.get("soru_bozuk") is True, "ne_soruyor": (data.get("ne_soruyor") or "").strip(),
            "tibbi_varliklar": varliklar, "atilan_varlik": atilan, "kanit": kanit,
            "cevap_denetimi": {"kayitli": key, "kanita_gore": found or None, "sonuc": cevap}, "eksik": eksik}


# --------------------------------------------------------------------------- ana akış
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    chunks = load_chunks_index()
    sources = load_sources()
    dumps = exam_dump_ids(chunks, sources)
    print(f"sınav dökümü kaynak (kanıt dışı): {len(dumps)}", flush=True)
    p8 = {}
    if PHASE8.exists():
        for line in open(PHASE8, encoding="utf-8"):
            r = json.loads(line)
            p8[r["soru_id"]] = r
    p5 = {}
    for p in glob.glob(str(PHASE5 / "*.jsonl")):
        for line in open(p, encoding="utf-8"):
            o = json.loads(line)
            p5[o["question_id"]] = [m.get("chunk_id") for m in (o.get("slide_matches") or [])[:3]]
    pool = []
    for p in glob.glob(str(DB / "questions" / "*.jsonl")):
        for line in open(p, encoding="utf-8"):
            q = json.loads(line)
            opts = q.get("options") or {}
            if q.get("answer") and len(q.get("stem") or "") > 25 and isinstance(opts, dict) and len(opts) >= 4:
                pool.append(q)
    random.seed(a.seed)
    random.shuffle(pool)
    done_ids = set()
    out_path = OUT / "soru_metadata.jsonl"
    if out_path.exists():
        for line in open(out_path, encoding="utf-8"):
            o = json.loads(line)
            if o.get("durum") != "model_yaniti_yok":
                done_ids.add(o["question_id"])
    stats = {"denenen": 0, "kanit_yok_atlandi": 0}
    for q in pool:
        if stats["denenen"] >= a.limit:
            break
        if q["question_id"] in done_ids:
            continue
        ev = evidence_for(q["question_id"], p8, p5, chunks, dumps)
        if not ev:
            stats["kanit_yok_atlandi"] += 1
            continue
        stats["denenen"] += 1
        res = extract(q, ev, sources, p8.get(q["question_id"]))
        stats[res["durum"]] = stats.get(res["durum"], 0) + 1
        cd = (res.get("cevap_denetimi") or {}).get("sonuc")
        if cd:
            stats["cevap_" + cd] = stats.get("cevap_" + cd, 0) + 1
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
        print(f"[{stats['denenen']}/{a.limit}] {q['question_id']} → {res['durum']}", flush=True)
        time.sleep(1.5)
    json.dump({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), **stats}, open(OUT / "rapor.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
