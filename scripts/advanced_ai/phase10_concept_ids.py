#!/usr/bin/env python3
"""
Faz 10 — Kavram kimliklendirme (Wikidata → UMLS CUI / MeSH / ICD-10 / Disease Ontology) + kimlik destekli müfredat ağacı

Amaç: metindeki farklı yazımları resmî bir kimliğe bağlamak ("glikojenoliz" ve "glycogenolysis" → aynı Wikidata öğesi,
UMLS C0017942). Bundan sonra eşleştirme kelimelerle değil kimliklerle de yapılır.

Adımlar
 1. Terim havuzu (yalnızca ders materyalinde — sınav dökümü hariç — geçenler):
    Faz 5 terimleri ve tıbbi varlık listeleri, kanıtlı sözlük, Faz 6.5 sözlüğü, doğrulanmış Faz 6 ayırıcı tanıları.
    (Bu kaynakların bir kısmı yapay zekâ üretimi; burada yalnızca ARAMA ANAHTARI olarak kullanılır — kabul ölçütü,
    Wikidata'da tıbbi kimlikli bir öğeyle birebir ad eşleşmesi ve materyalde geçmesidir.)
 2. Stanza (Türkçe) ile son kelimenin kökü: "hipertansiyonun" → "hipertansiyon" ek arama varyantı.
 3. Wikidata SPARQL: Türkçe / İngilizce ad ya da takma ad BİREBİR eşleşmesi; öğe UMLS CUI (P2892), MeSH (P486),
    ICD-10 (P494) ya da Disease Ontology (P699) kimliklerinden en az birini taşımalı. Sonuçlar önbelleğe yazılır
    (artımlı; sonraki çalıştırmalar yalnızca yeni terimleri sorar).
 4. Kavram: Wikidata öğesi. Üyeler: eşleşen terimlerimiz + öğenin Türkçe/İngilizce adı ve takma adları
    (yalnızca materyalde geçenler — eşleştirmeye katkı verebilenler).
 5. bge-m3 (Ollama, vektör benzerliği): kimliksiz kalan terimler için en yakın kavram yalnızca ADAY olarak yazılır
    (kosinüs ≥ 0,90) → hakem kuyruğu; eşleştirmede kullanılmaz.
 6. Faz 9 motoru bu kavramlarla çalıştırılır → meds_temp/phase10 (Faz 8 yüksek güven öncelikli; aynı karar kuralları).

Çıktı: meds_database_v2/concept_ids/ (kavramlar.json, terim_kimlik.jsonl, adaylar.jsonl, wikidata_onbellek.json, rapor.json)
       meds_temp/phase10/ (müfredat ağacı). Ana veritabanına yazmaz.
"""
from __future__ import annotations

import ast
import collections
import glob
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

PROJECT = P8.PROJECT
V2 = PROJECT / "meds_database_v2"
OUT = V2 / "concept_ids"
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
CACHE = OUT / "wikidata_onbellek.json"
UA = "MedSor/1.0 (egitim amacli tip terimleri eslestirme)"
SPARQL = "https://query.wikidata.org/sparql"
OLLAMA = os.environ.get("OLLAMA_URL") or "http://127.0.0.1:11434"
MED_PROPS = {"P2892": "umls_cui", "P486": "mesh", "P494": "icd10", "P699": "disease_ontology"}
BATCH = 120
GENERIC_EN = set("""cause milk teen teens disease disorder syndrome pain infection cancer tumor tumour drug therapy
treatment patient patients cell cells blood fever diabetes anemia anaemia hormone protein gene acid balls""".split())


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] [faz10] {m}", flush=True)


def norm(t: str) -> str:
    t = str(t or "").replace("i̇", "i").replace("̇", "")
    t = re.sub(r"\s*\([^)]*\)\s*", " ", t)          # parantez içi açıklamaları at
    return " ".join(t.split()).strip(" .,;:-–")


def parse(v):
    if isinstance(v, str) and v[:1] in "{[":
        try:
            return json.loads(v)
        except Exception:
            try:
                return ast.literal_eval(v)
            except Exception:
                return None
    return v


# --------------------------------------------------------------------------- 1) terim havuzu
def collect_terms() -> collections.Counter:
    terms = collections.Counter()

    def add(t, w=1):
        t = norm(t)
        if 3 <= len(t) <= 60 and len(t.split()) <= 5 and not re.search(r"\d{3,}", t):
            terms[t] += w

    for p in glob.glob(str(V2 / "questions" / "*.jsonl")):
        for q in P8.read_jsonl(Path(p)):
            tax = parse(q.get("taxonomy_metadata")) or {}
            for t in tax.get("terimler") or []:
                add(t, 2)
            ents = parse(q.get("tibbi_varliklar")) or {}
            if isinstance(ents, dict):
                for v in ents.values():
                    for t in v if isinstance(v, list) else []:
                        add(t)
    ev = V2 / "evidence_thesaurus" / "kanitli_sozluk.json"
    if ev.exists():
        for k, e in json.load(open(ev, encoding="utf-8")).items():
            add(e.get("turkce") or k, 2)
            for s in e.get("esanlamlilar") or []:
                if (e.get("guven") or {}).get(s) in ("yuksek", "orta"):
                    add(s)
    th = V2 / "medical_thesaurus" / "medical_thesaurus.json"
    if th.exists():
        for k, e in json.load(open(th, encoding="utf-8")).items():
            add(e.get("turkce") or k)
            add(e.get("latin") or "")
    vp = V2 / "deep_metadata_validated" / "dogrulama.jsonl"
    if vp.exists():
        for r in P8.read_jsonl(vp):
            for x in r.get("ayirici_tani") or []:
                add(x.get("hastalik") or "")
    return terms


def material_corpus():
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    dumps = {s for s, src in sources.items() if P8.is_exam_dump(src, chunks_by_src)}
    texts = [c.get("text") or "" for sid, cs in chunks_by_src.items() if sid not in dumps for c in cs]
    return " " + " \n ".join(P8.fold(t) for t in texts) + " "


# --------------------------------------------------------------------------- 2) Stanza kök varyantı
def stanza_variants(terms: list[str]) -> dict[str, str]:
    """Son kelimesi çekimli terimler için kök varyantı (ör. 'hipertansiyonun' → 'hipertansiyon')."""
    try:
        import stanza  # noqa: F401
        nlp = stanza.Pipeline("tr", processors="tokenize,mwt,pos,lemma", use_gpu=False, verbose=False,
                              tokenize_pretokenized=True)
    except Exception as e:  # noqa: BLE001
        log(f"Stanza kullanılamadı ({e}); kök varyantı atlanıyor")
        return {}
    out = {}
    cand = [t for t in terms if re.search(r"(ın|in|un|ün|nın|nin|ları|leri|lar|ler|da|de|ı|i|u|ü)$", t.split()[-1].lower())]
    for i in range(0, len(cand), 500):
        part = cand[i:i + 500]
        doc = nlp([[t.split()[-1]] for t in part])
        for t, s in zip(part, doc.sentences):
            lem = s.words[-1].lemma if s.words else None
            last = t.split()[-1]
            # yalnızca kök, kelimenin başı ise ve en az 4 harfse (tıbbi terimlerde Stanza bazen fazla kırpıyor)
            if lem and len(lem) >= 4 and last.lower().startswith(lem.lower()) and lem.lower() != last.lower():
                out[t] = " ".join(t.split()[:-1] + [lem])
    return out


# --------------------------------------------------------------------------- 3) Wikidata
def sparql(q: str, tries: int = 4):
    for k in range(tries):
        try:
            # POST: uzun VALUES listeleri GET'te "414 URI Too Long" veriyor
            req = urllib.request.Request(SPARQL, data=urllib.parse.urlencode({"query": q}).encode(),
                                         headers={"User-Agent": UA, "Accept": "application/sparql-results+json",
                                                  "Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read())["results"]["bindings"]
        except Exception as e:  # noqa: BLE001
            log(f"SPARQL hata ({e}); {5 * (k + 1)} sn sonra tekrar")
            time.sleep(5 * (k + 1))
    return None


def lit(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def lookup_labels(labels: list[str]) -> dict[str, list[str]]:
    """label → [QID] (yalnızca tıbbi kimlikli öğeler). Türkçe ve İngilizce, büyük/küçük harf varyantları."""
    vals = []
    for l in labels:
        for v in {l, l.lower(), l[:1].upper() + l[1:].lower()}:
            vals.append(f"{lit(v)}@tr")
            vals.append(f"{lit(v)}@en")
    q = ("SELECT DISTINCT ?l ?i WHERE { VALUES ?l { " + " ".join(vals) + " } "
         "{ ?i rdfs:label ?l } UNION { ?i skos:altLabel ?l } "
         "FILTER EXISTS { { ?i wdt:P2892 [] } UNION { ?i wdt:P486 [] } UNION { ?i wdt:P494 [] } UNION { ?i wdt:P699 [] } } }")
    rows = sparql(q)
    if rows is None:
        return None
    out = collections.defaultdict(list)
    for r in rows:
        out[P8.fold(r["l"]["value"])].append(r["i"]["value"].rsplit("/", 1)[-1])
    return out


def fetch_items(qids: list[str]) -> dict:
    q = ("SELECT ?i ?p ?v ?tr ?en ?alt WHERE { VALUES ?i { " + " ".join("wd:" + x for x in qids) + " } "
         "{ VALUES ?p { wdt:P2892 wdt:P486 wdt:P494 wdt:P699 } ?i ?p ?v } UNION "
         "{ ?i rdfs:label ?tr FILTER(LANG(?tr)='tr') } UNION { ?i rdfs:label ?en FILTER(LANG(?en)='en') } UNION "
         "{ ?i skos:altLabel ?alt FILTER(LANG(?alt)='tr' || LANG(?alt)='en') } }")
    rows = sparql(q)
    if rows is None:
        return None
    items = {x: {"qid": x, "tr": None, "en": None, "takma": [], "kimlik": {}} for x in qids}
    for r in rows:
        it = items[r["i"]["value"].rsplit("/", 1)[-1]]
        if "p" in r:
            key = MED_PROPS.get(r["p"]["value"].rsplit("/", 1)[-1])
            if key:
                it["kimlik"].setdefault(key, [])
                if r["v"]["value"] not in it["kimlik"][key]:
                    it["kimlik"][key].append(r["v"]["value"])
        if "tr" in r:
            it["tr"] = r["tr"]["value"]
        if "en" in r:
            it["en"] = r["en"]["value"]
        if "alt" in r and r["alt"]["value"] not in it["takma"]:
            it["takma"].append(r["alt"]["value"])
    return items


# --------------------------------------------------------------------------- 5) bge-m3 adayları
def embed(texts: list[str]):
    out = []
    for i in range(0, len(texts), 64):
        body = {"model": "bge-m3", "input": texts[i:i + 64]}
        try:
            req = urllib.request.Request(f"{OLLAMA}/api/embed", data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                out.extend(json.loads(r.read())["embeddings"])
        except Exception as e:  # noqa: BLE001
            log(f"bge-m3 kullanılamadı ({e}); adaylar atlanıyor")
            return None
    return out


def cos(a, b):
    s = sum(x * y for x, y in zip(a, b))
    return s / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)


# --------------------------------------------------------------------------- ana akış
def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}
    terms = collect_terms()
    log(f"terim havuzu: {len(terms)}")
    corpus = material_corpus()
    n_chunks = corpus.count("\n") + 1
    attested = [t for t in terms if f" {P8.fold(t)} " in corpus]
    rep["terim_havuzu"], rep["materyalde_gecen"] = len(terms), len(attested)
    log(f"materyalde geçen: {len(attested)}")

    variants = stanza_variants(attested)
    rep["stanza_kok_varyanti"] = len(variants)

    cache = json.load(open(CACHE, encoding="utf-8")) if CACHE.exists() else {"etiket": {}, "oge": {}}
    queries = sorted({t for t in attested} | set(variants.values()))
    todo = [t for t in queries if P8.fold(t) not in cache["etiket"]]
    log(f"Wikidata: {len(todo)} yeni etiket sorgulanacak (önbellekte {len(cache['etiket'])})")
    for i in range(0, len(todo), BATCH):
        part = todo[i:i + BATCH]
        res = lookup_labels(part)
        if res is None:
            log("Wikidata yanıt vermedi; bu tur kalan etiketler sonraki çalıştırmaya bırakıldı")
            break
        for t in part:
            cache["etiket"][P8.fold(t)] = res.get(P8.fold(t), [])
        if (i // BATCH) % 10 == 0:
            json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
            log(f"  {i + len(part)}/{len(todo)}")
        time.sleep(1.0)
    qids = sorted({q for v in cache["etiket"].values() for q in v} - set(cache["oge"]))
    for i in range(0, len(qids), 80):
        items = fetch_items(qids[i:i + 80])
        if items is None:
            break
        cache["oge"].update(items)
        time.sleep(1.0)
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

    # ---- 4) kavramlar
    term_rows, by_qid = [], collections.defaultdict(set)
    for t in attested:
        keys = [P8.fold(t)] + ([P8.fold(variants[t])] if t in variants else [])
        hits = []
        for k in keys:
            hits += cache["etiket"].get(k, [])
        hits = list(dict.fromkeys(hits))
        if len(hits) == 1:                    # birden çok öğe = belirsiz ad (ör. "MS") → kullanılmaz
            by_qid[hits[0]].add(P8.fold(t))
            it = cache["oge"].get(hits[0], {})
            term_rows.append({"terim": t, "qid": hits[0], "tr": it.get("tr"), "en": it.get("en"),
                              "kimlik": it.get("kimlik", {}), "yontem": "stanza_kok" if t in variants and
                              not cache["etiket"].get(P8.fold(t)) else "birebir_ad"})
        elif len(hits) > 1:
            term_rows.append({"terim": t, "qid": None, "belirsiz": hits[:6]})
    concepts = {}
    for qid, mem in by_qid.items():
        it = cache["oge"].get(qid, {})
        extra = {P8.fold(norm(x)) for x in [it.get("tr"), it.get("en")] + (it.get("takma") or []) if x}
        extra = {x for x in extra if len(x) >= 4 and f" {x} " in corpus}   # yalnızca materyalde geçenler
        # Wikidata takma adları bazen geniş ("diabetes", "milk", "cause") ya da başka ilaç ("omeprazole" ⊂ esomeprazol)
        base = mem | ({P8.fold(it["tr"])} if it.get("tr") else set())
        clean = set()
        for x in extra - mem:
            xs = set(x.split())
            if x in GENERIC_EN or len(x) < 5:
                continue
            if any(xs < set(b.split()) for b in base | extra):            # kelime alt kümesi = daha geniş kavram
                continue
            if any(b != x and (b.endswith(x) or x.endswith(b)) and abs(len(b) - len(x)) >= 2 for b in base):
                continue                                                  # es-omeprazol / omeprazol gibi ön ek farkı
            clean.add(x)
        members = mem | clean
        # Kendi terimlerimiz için de: etiketin ön ek farklı hâli başka bir ilaç/kavramdır (esomeprazol ≠ omeprazol)
        labels = {P8.fold(norm(x)) for x in (it.get("tr"), it.get("en")) if x}
        members = {m for m in members if m in labels or not any(
            l != m and (l.endswith(m) or m.endswith(l)) and abs(len(l) - len(m)) >= 2 and not m.startswith(l[:4])
            for l in labels)}
        # Çok genel tek kelimeler (materyal chunk'larının > %3'ünde geçen: hasta, hücre, neden…) ayırt edici değil
        members = {m for m in members if " " in m or corpus.count(f" {m} ") <= 0.03 * n_chunks}
        if len(members) < 2:
            continue
        members = sorted(members)
        concepts["§w" + qid] = {"terim": P8.fold(it.get("tr") or next(iter(mem))), "uyeler": members, "qid": qid,
                                "tr": it.get("tr"), "en": it.get("en"), "kimlik": it.get("kimlik", {})}
    rep["kimlikli_terim"] = sum(1 for r in term_rows if r.get("qid"))
    rep["belirsiz_terim"] = sum(1 for r in term_rows if r.get("belirsiz"))
    rep["kavram"] = len(concepts)
    rep["coklu_uyeli_kavram"] = sum(1 for c in concepts.values() if len(c["uyeler"]) >= 2)
    rep["umls_cui_li_kavram"] = sum(1 for c in concepts.values() if c["kimlik"].get("umls_cui"))

    # ---- 5) bge-m3 adayları (hakem kuyruğu)
    matched = {P8.fold(r["terim"]) for r in term_rows if r.get("qid") or r.get("belirsiz")}
    unmatched = sorted((t for t in attested if P8.fold(t) not in matched), key=lambda t: -terms[t])[:1500]
    labels = [(cid, c["tr"] or c["en"]) for cid, c in concepts.items() if c.get("tr") or c.get("en")]
    cands = []
    if unmatched and labels:
        eu, el = embed(unmatched), embed([l for _, l in labels])
        if eu and el:
            for t, v in zip(unmatched, eu):
                best = max(range(len(el)), key=lambda j: cos(v, el[j]))
                sc = cos(v, el[best])
                if sc >= 0.90:
                    cid = labels[best][0]
                    cands.append({"terim": t, "aday_kavram": cid, "aday_ad": labels[best][1], "qid": concepts[cid]["qid"],
                                  "kosinus": round(sc, 3), "durum": "hakem_bekliyor"})
    rep["vektor_adayi"] = len(cands)

    with open(OUT / "terim_kimlik.jsonl", "w", encoding="utf-8") as f:
        for r in term_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / "adaylar.jsonl", "w", encoding="utf-8") as f:
        for r in cands:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if concepts:
        tmp = OUT / "kavramlar.json.tmp"
        json.dump(concepts, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, OUT / "kavramlar.json")

    # ---- 6) kimlik destekli müfredat ağacı (Faz 9 motoru, Faz 8 öncelikli)
    py = sys.executable
    rc = subprocess.run([py, str(Path(__file__).resolve().parent / "phase9_thesaurus_graph.py"), "--sample", "0",
                         "--extra-concepts", str(OUT / "kavramlar.json"), "--out", str(TEMP / "phase10"), "--label", "Faz 10"],
                        capture_output=True, text=True)
    tail = rc.stdout[rc.stdout.find('{\n "sayilar"'):]
    try:
        r9 = json.loads(tail[: tail.rindex("}") + 1])
        rep["agac"] = {"faz8_karsilastirma": r9.get("faz8_karsilastirma"), "ek_kavramlar": r9.get("ek_kavramlar"),
                       "guven": {k: v for k, v in (r9.get("sorular") or {}).items() if k.startswith("guven")}}
    except Exception:
        rep["agac"] = {"rc": rc.returncode, "hata": (rc.stderr or "")[-600:]}
    rep["sure_sn"] = round(time.time() - t0, 1)
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0 if rc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
