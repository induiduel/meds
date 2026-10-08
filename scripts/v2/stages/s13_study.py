"""s13 — Sözlük ve çalışma kartları: denetim, düzeltme, kanıtlı üretim.

İki adım (AI çağrısı YOK; tanımları editör yazar, betik yalnız kanıtla ölçer):

  prepare  → `meds_temp/study/` altına çalışma paketleri:
             - glossary_audit.jsonl   mevcut sözlük kayıtları + temizlik + ders notu desteği
             - glossary_new.jsonl     sözlükte olmayan, ders notlarında geçen kavram adayları + alıntılar
             - deck_cards_audit.jsonl öğrenme destesi kartları + destek + yinelenenler
             - question_cards.jsonl   cevap anahtarlı çıkmış sorulardan kart adayları + destek
  build    → editör dosyaları (`meds_temp/study/editor_*.jsonl`) ile birleştirir, desteği yeniden ölçer,
             CORE `derived/` altına yazar ve `--export` ile site verisini (yedekleyerek) günceller.

Kanıt kapısı: bir tanım/kart yalnızca ders notu (lecture_slide) alıntılarıyla `support >= ESIK`
ise "kaynakli" sayılır; altı "inceleme" kuyruğuna gider. Sınav dökümleri kanıt değildir.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from .. import config
from ..core import ids, store, textnorm
from ..core.lectures import LectureCorpus

ESIK = 0.6
STUDY_DIR = config.TEMP_DIR / "study"
SITE_DATA = config.MEDS_DIR / "src" / "data"
GLOSSARY_JSON = SITE_DATA / "medical_glossary.json"
ENCYCLOPEDIA_JSON = SITE_DATA / "medical_encyclopedia.json"
DECKS_JSON = SITE_DATA / "interactive_learning_decks.json"
QUESTION_CARDS_JSON = SITE_DATA / "question_cards.json"
CONCEPTS = config.PROJECT_ROOT / "meds_database_v2" / "concept_ids" / "kavramlar.json"
QUESTIONS = config.QUESTIONS_DIR / "archive.jsonl"

# Sözlük kategorileri: site `glossary.ts` bu anahtarları etikete çevirir.
KATEGORI = {
    "hastalik": "hastalik", "klinik hastalık": "hastalik", "ilac": "ilac", "farmakoloji": "ilac",
    "genetik": "genetik", "genetik & patoloji": "genetik", "patoloji": "patoloji", "tıbbi patoloji": "patoloji",
    "patoloji / biyokimya": "patoloji", "patojen": "patojen", "mikrobiyoloji": "patojen",
    "parazitoloji": "patojen", "bakteriyoloji": "patojen", "viroloji": "patojen",
}

# "S • ı" gibi: bir metnin ilk iki KARAKTERİ " • " ile birleştirilmiş eski üretim hatası.
_GARBAGE_PEARL = re.compile(r"^\s*\S{1,2}\s*•\s*\S{1,2}\s*$")
_ANSWER_LEAK = re.compile(
    r"\s*\n?\s*[(\-]*\s*(?:Cevap(?:\s+anahtarı)?|CEVAP|Yanıt|Doğru cevap)\s*[:：]?\s*[A-Ea-e]\b.*$", re.S)
# Şıkka yapışmış sonraki soru/dosya artıkları: "--- [dosya.txt] ...", sondaki " (" veya " -"
_OPTION_TAIL = re.compile(r"\s*---\s*\[.*$|\s+[(\-]\s*$", re.S)


def _clean(text) -> str:
    """Sözlük/kart metni için hafif temizlik (OCR onarımı YOK: '!' gibi işaretler korunur)."""
    s = textnorm.nfc(str(text or ""))
    s = textnorm.fix_mojibake(s)
    s = textnorm.strip_control(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\s*\n\s*", " ", s)
    return s.strip()


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _evidence(corpus: LectureCorpus, term: str, text: str, aliases=(), k: int = 3) -> tuple[list[int], int]:
    """Terimin geçtiği ders notu parçaları içinden `text` ile en uyumlu k parça + toplam geçiş."""
    hits: list[int] = []
    # "X ve Y", "X vs Y", "X: Y", "X (Y)" gibi bileşik başlıklarda parçalar da aranır.
    parts = [p.strip() for p in re.split(r"\s+(?:ve|vs\.?|ile)\s+|[:;/()]|\s+-\s+", term) if len(p.strip()) > 3]
    for name in [term, *aliases, *parts]:
        if name and len(hits) < 400:
            hits.extend(i for i in corpus.phrase_hits(name) if i not in hits)
    if not hits:
        return [], 0
    top = [i for i, _ in corpus.search(f"{term} {text}", k, within=hits)]
    return top, len(hits)


# ----------------------------------------------------------------------------------------------
# prepare
# ----------------------------------------------------------------------------------------------
def _glossary_items() -> list[tuple[str, dict]]:
    raw = store.read_json(GLOSSARY_JSON, {}) or {}
    out = []
    for key, val in raw.items():
        if isinstance(val, str):
            val = {"term": key, "definition": val}
        if isinstance(val, dict):
            out.append((key, val))
    return out


# Ders dosya adından üretilmiş sahte sözlük kayıtları: inci alanı bu şablon cümledir.
_TITLE_PEARL = "konusundaki temel patofizyolojik basamaklar"


def prepare_glossary(corpus: LectureCorpus) -> dict:
    enc = {ids.norm_key(e.get("term") or ""): e for e in (store.read_json(ENCYCLOPEDIA_JSON, []) or [])}
    rows, seen = [], {}
    counts = {"kayit": 0, "cop_inci": 0, "tanim_eksik": 0, "kategori": 0, "yinelenen": 0,
              "kaynakli": 0, "zayif": 0, "kaynaksiz": 0}
    for key, v in _glossary_items():
        counts["kayit"] += 1
        term = _clean(v.get("term") or key)
        definition = _clean(v.get("definition") or v.get("description") or v.get("meaning") or "")
        issues = []
        if not (v.get("definition") or "").strip():
            issues.append("tanim_alani_bos")
            counts["tanim_eksik"] += 1
        pearl = _clean(v.get("clinicalPearls") or v.get("clinicalPearl") or "")
        if pearl and (_GARBAGE_PEARL.match(pearl) or len(pearl) < 12):
            issues.append("cop_inci")
            counts["cop_inci"] += 1
            e = enc.get(ids.norm_key(term)) or {}
            sp = e.get("examSpotPearls")
            pearl = _clean(sp if isinstance(sp, str) else " • ".join(sp or [])) if sp else ""
        if _TITLE_PEARL in pearl or "pptx" in term.lower():
            issues.append("ders_basligi")
            counts["ders_basligi"] = counts.get("ders_basligi", 0) + 1
            pearl = ""
        cat_raw = str(v.get("category") or "").strip()
        cat = KATEGORI.get(cat_raw.lower(), cat_raw.lower() or "terim")
        if cat != cat_raw:
            issues.append("kategori_normal")
            counts["kategori"] += 1
        nk = ids.norm_key(term)
        if nk in seen:
            issues.append(f"yinelenen:{seen[nk]}")
            counts["yinelenen"] += 1
        seen.setdefault(nk, key)
        aliases = [a for a in (v.get("aliases") or []) if isinstance(a, str)]
        paren = re.match(r"^(.+?)\s*\((.+?)\)$", term)
        if paren:
            aliases += [paren.group(1), paren.group(2)]
        top, nhit = _evidence(corpus, term, definition, aliases)
        destek = corpus.support(definition, top) if top else 0.0
        durum = "kaynakli" if destek >= ESIK else ("zayif" if top else "kaynaksiz")
        counts[durum] += 1
        rows.append({
            "key": key, "term": term, "category": cat, "definition": definition, "pearl": pearl,
            "aliases": aliases, "discipline": v.get("discipline"), "issues": issues,
            "gecis": nhit, "destek": destek, "durum": durum,
            "kaynaklar": [corpus.ref(i, corpus.snippet(i, paren.group(1) if paren else term, 360)) for i in top],
        })
    store.write_jsonl(STUDY_DIR / "glossary_audit.jsonl", rows, guard=False)
    return counts


def prepare_new_terms(corpus: LectureCorpus, min_hits: int = 3) -> dict:
    have: set[str] = set()
    for key, v in _glossary_items():
        have.add(ids.norm_key(key))
        have.add(ids.norm_key(v.get("term") or ""))
        have.update(ids.norm_key(a) for a in (v.get("aliases") or []) if isinstance(a, str))
    for e in store.read_json(ENCYCLOPEDIA_JSON, []) or []:
        t = e.get("term") or e.get("title") or ""
        have.add(ids.norm_key(t))
        have.update(ids.norm_key(a) for a in (e.get("aliases") or []) if isinstance(a, str))
        m = re.match(r"^(.+?)\s*\((.+?)\)$", t)
        if m:
            have.update({ids.norm_key(m.group(1)), ids.norm_key(m.group(2))})
    rows = []
    for cid, k in (store.read_json(CONCEPTS, {}) or {}).items():
        tr = k.get("tr") or k.get("terim")
        names = [tr, *(k.get("uyeler") or [])]
        if any(ids.norm_key(n) in have for n in names):
            continue
        best_name, best = tr, []
        for n in names:
            h = corpus.phrase_hits(n)
            if len(h) > len(best):
                best_name, best = n, h
        if len(best) < min_hits:
            continue
        top = [i for i, _ in corpus.search(best_name, 4, within=best)]
        rows.append({
            "kavram": cid, "term": tr, "en": k.get("en"), "uyeler": k.get("uyeler"), "kimlik": k.get("kimlik"),
            "gecis": len(best), "kaynak_sayisi": len({corpus.chunks[i]["source_id"] for i in best}),
            "kaynaklar": [corpus.ref(i, corpus.snippet(i, best_name, 360)) for i in top],
        })
    rows.sort(key=lambda r: -r["gecis"])
    store.write_jsonl(STUDY_DIR / "glossary_new.jsonl", rows, guard=False)
    return {"aday": len(rows)}


def prepare_deck_cards(corpus: LectureCorpus) -> dict:
    decks = store.read_json(DECKS_JSON, []) or []
    rows, counts = [], {"kart": 0, "yinelenen": 0, "kaynakli": 0, "zayif": 0, "kaynaksiz": 0}
    for d in decks:
        seen: dict[str, str] = {}
        for s in d.get("slides") or []:
            for idx, c in enumerate(s.get("flashcards") or []):
                counts["kart"] += 1
                front = _clean(c.get("front") or c.get("question"))
                back = _clean(c.get("back") or c.get("answer"))
                fk = ids.norm_key(front) + "||" + ids.norm_key(back)
                dup = seen.get(fk)
                seen.setdefault(fk, f"{s.get('slideNumber')}:{idx}")
                if dup:
                    counts["yinelenen"] += 1
                top = [i for i, _ in corpus.search(f"{front} {back}", 3)]
                destek = corpus.support(back, top) if top else 0.0
                durum = "kaynakli" if destek >= ESIK else ("zayif" if destek >= 0.35 else "kaynaksiz")
                counts[durum] += 1
                rows.append({
                    "deck": d.get("id") or d.get("deckId"), "slide": s.get("slideNumber"), "idx": idx,
                    "id": c.get("id"), "front": front, "back": back, "yinelenen": dup, "destek": destek,
                    "durum": durum, "kaynaklar": [corpus.ref(i, corpus.snippet(i, back.split()[0] if back else "", 300))
                                                  for i in top[:3]],
                })
    store.write_jsonl(STUDY_DIR / "deck_cards_audit.jsonl", rows, guard=False)
    return counts


def _strip_leak(text: str) -> str:
    return _clean(_OPTION_TAIL.sub("", _ANSWER_LEAK.sub("", str(text or ""))))


def prepare_question_cards(corpus: LectureCorpus) -> dict:
    groups: dict[str, dict] = {}
    for q in store.iter_jsonl(QUESTIONS):
        opts = q.get("options") or {}
        ans = (q.get("answer") or "").strip().upper()
        if not ans or not isinstance(opts, dict) or ans not in opts or q.get("acik_uclu"):
            continue
        stem = _clean(q.get("stem"))
        options = {k: _strip_leak(v) for k, v in sorted(opts.items())}
        if not stem or any(not v for v in options.values()):
            continue
        key = ids.norm_key(stem) + "||" + ids.norm_key(options[ans])
        g = groups.get(key)
        prov = q.get("provenance") or {}
        yer = {"dosya": Path(prov.get("kaynak_dosya") or "").name, "sayfa": prov.get("sayfa")}
        if g:
            g["tekrar"] += 1
            if yer not in g["cikis"]:
                g["cikis"].append(yer)
            if g["answer"] != ans or g["options"] != options:
                g.setdefault("celiski", []).append({"answer": ans, "options": options})
            continue
        groups[key] = {
            "question_id": q.get("question_id"), "stem": stem, "options": options, "answer": ans,
            "answer_text": options[ans], "kurul": q.get("kurul"), "ders": q.get("ders"),
            "konu": q.get("konu"), "tekrar": 1, "cikis": [yer],
        }
    counts = {"kart": 0, "kaynakli": 0, "zayif": 0, "kaynaksiz": 0, "celiskili": 0}
    rows = []
    for g in groups.values():
        top = [i for i, _ in corpus.search(f"{g['stem']} {g['answer_text']}", 3)]
        # Cevap metni kökle birlikte ders notunda geçiyor mu?
        destek = corpus.support(f"{g['stem']} {g['answer_text']}", top) if top else 0.0
        cevap_destek = corpus.support(g["answer_text"], top) if top else 0.0
        durum = "kaynakli" if destek >= ESIK and cevap_destek >= ESIK else (
            "zayif" if destek >= 0.4 else "kaynaksiz")
        if g.get("celiski"):
            counts["celiskili"] += 1
        counts["kart"] += 1
        counts[durum] += 1
        g.update({"destek": destek, "cevap_destek": cevap_destek, "durum": durum,
                  "kaynaklar": [corpus.ref(i, corpus.snippet(i, g["answer_text"], 360)) for i in top[:2]]})
        rows.append(g)
    store.write_jsonl(STUDY_DIR / "question_cards.jsonl", rows, guard=False)
    return counts


def prepare(log=print) -> dict:
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    corpus = LectureCorpus()
    log(f"ders notu korpusu: {len(corpus.chunks)} parça")
    out = {
        "sozluk": prepare_glossary(corpus),
        "yeni_terim": prepare_new_terms(corpus),
        "deste_kartlari": prepare_deck_cards(corpus),
        "soru_kartlari": prepare_question_cards(corpus),
    }
    store.atomic_write_json(STUDY_DIR / "prepare_report.json", {"zaman": _now(), **out})
    log(json.dumps(out, ensure_ascii=False))
    return out


# ----------------------------------------------------------------------------------------------
# build
# ----------------------------------------------------------------------------------------------
def _editor(name: str) -> list[dict]:
    p = STUDY_DIR / name
    return store.read_jsonl(p) if p.exists() else []


def _backup(path: Path) -> None:
    dst = config.PROJECT_ROOT / "yedek" / "study" / datetime.now().strftime("%Y%m%d_%H%M%S")
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst / path.name)


def _refs(corpus: LectureCorpus, chunk_ids: list[str]) -> list[int]:
    pos = {c["chunk_id"]: i for i, c in enumerate(corpus.chunks)}
    return [pos[c] for c in chunk_ids if c in pos]


def build_glossary(corpus: LectureCorpus) -> tuple[dict, dict, list[dict]]:
    """Mevcut sözlüğü düzeltir (editör düzeltmeleri + temizlik) ve editörün yeni terimlerini ekler."""
    audit = {r["key"]: r for r in _editor("glossary_audit.jsonl")}
    fixes = {r["key"]: r for r in _editor("editor_glossary_fix.jsonl")}
    new = _editor("editor_glossary_new.jsonl")
    out: dict[str, dict] = {}
    review: list[dict] = []
    counts = {"duzeltilen": 0, "silinen": 0, "yeni": 0, "yeni_red": 0, "kaynakli": 0, "zayif": 0, "kaynaksiz": 0}
    for key, a in audit.items():
        if "ders_basligi" in a["issues"] and not fixes.get(key, {}).get("definition"):
            counts["silinen"] += 1
            review.append({"tur": "sozluk_ders_basligi_silindi", "key": key})
            continue
        if any(i.startswith("yinelenen") for i in a["issues"]):
            counts["silinen"] += 1
            continue
        f = fixes.get(key) or {}
        if f.get("sil"):
            counts["silinen"] += 1
            review.append({"tur": "sozluk_silindi", "key": key, "neden": f.get("neden")})
            continue
        definition = _clean(f.get("definition") or a["definition"])
        pearl = _clean(f["pearl"]) if "pearl" in f else a["pearl"]
        top = _refs(corpus, f.get("kaynak") or [r["chunk_id"] for r in a["kaynaklar"]])
        destek = corpus.support(definition, top) if top else 0.0
        durum = "kaynakli" if destek >= ESIK else ("zayif" if top else "kaynaksiz")
        if durum != "kaynakli" and f.get("onay"):  # editör ders notu alıntılarıyla teyit etti
            durum = "editor_onay"
        counts[durum] = counts.get(durum, 0) + 1
        if f or a["issues"]:
            counts["duzeltilen"] += 1
        rec = {
            "term": _clean(f.get("term") or a["term"]), "category": f.get("category") or a["category"],
            "definition": definition, "description": definition, "discipline": a.get("discipline") or "",
            "committee": "",
        }
        if pearl:
            rec["clinicalPearl"] = pearl
        aliases = [*a["aliases"], *(f.get("aliases") or [])]
        if aliases:
            rec["aliases"] = sorted({x for x in aliases if ids.norm_key(x) != ids.norm_key(rec["term"])})
        rec["dogrulama"] = {"durum": durum, "destek": destek, "uretici": "s13_study"}
        if top:
            rec["kaynaklar"] = [corpus.ref(i) for i in top[:2]]
        out[key] = rec
        if durum not in ("kaynakli", "editor_onay"):
            review.append({"tur": "sozluk_kanit", "key": key, "destek": destek, "durum": durum})
    for n in new:
        term = _clean(n["term"])
        key = term.replace("I", "ı").replace("İ", "i").lower()
        definition = _clean(n["definition"])
        top = _refs(corpus, n.get("kaynak") or [])
        destek = corpus.support(definition, top) if top else 0.0
        mevcut = key in out or ids.norm_key(term) in {ids.norm_key(r["term"]) for r in out.values()}
        if destek < ESIK or mevcut:
            counts["yeni_red"] += 1
            review.append({"tur": "yeni_terim_red", "term": term, "destek": destek, "neden": "mevcut" if mevcut else "destek"})
            continue
        rec = {"term": term, "category": n.get("category") or "terim", "definition": definition,
               "description": definition, "discipline": n.get("discipline") or "", "committee": ""}
        if n.get("pearl"):
            rec["clinicalPearl"] = _clean(n["pearl"])
        if n.get("aliases"):
            rec["aliases"] = n["aliases"]
        rec["dogrulama"] = {"durum": "kaynakli", "destek": destek, "uretici": "s13_study"}
        rec["kaynaklar"] = [corpus.ref(i) for i in top[:2]]
        out[key] = rec
        counts["yeni"] += 1
        counts["kaynakli"] += 1
    return out, counts, review


def build_decks(corpus: LectureCorpus) -> tuple[list, dict, list[dict]]:
    decks = store.read_json(DECKS_JSON, []) or []
    audit = {(r["deck"], r["slide"], r["idx"]): r for r in _editor("deck_cards_audit.jsonl")}
    fixes = {(r["deck"], r["slide"], r["idx"]): r for r in _editor("editor_deck_fix.jsonl")}
    counts = {"kart": 0, "silinen_yinelenen": 0, "silinen_hatali": 0, "duzeltilen": 0, "kaynakli": 0,
              "zayif": 0, "kaynaksiz": 0}
    review = []
    for d in decks:
        did = d.get("id") or d.get("deckId")
        for s in d.get("slides") or []:
            kept = []
            for idx, c in enumerate(s.get("flashcards") or []):
                a = audit.get((did, s.get("slideNumber"), idx)) or {}
                f = fixes.get((did, s.get("slideNumber"), idx)) or {}
                if a.get("yinelenen"):
                    counts["silinen_yinelenen"] += 1
                    continue
                if f.get("sil"):
                    counts["silinen_hatali"] += 1
                    review.append({"tur": "kart_silindi", "deck": did, "slide": s.get("slideNumber"),
                                   "front": a.get("front"), "neden": f.get("neden")})
                    continue
                front = _clean(f.get("front") or c.get("front") or c.get("question"))
                back = _clean(f.get("back") or c.get("back") or c.get("answer"))
                if f:
                    counts["duzeltilen"] += 1
                for k in ("front", "question"):
                    if k in c or k == "front":
                        c[k] = front
                for k in ("back", "answer"):
                    if k in c or k == "back":
                        c[k] = back
                top = _refs(corpus, f.get("kaynak") or [r["chunk_id"] for r in a.get("kaynaklar", [])])
                destek = corpus.support(back, top) if top else 0.0
                durum = "kaynakli" if destek >= ESIK else ("zayif" if destek >= 0.35 else "kaynaksiz")
                if f.get("onay") and durum != "kaynakli":  # editör tıbbi doğruluğu teyit etti
                    durum = "editor_onay"
                counts[durum] = counts.get(durum, 0) + 1
                counts["kart"] += 1
                c["dogrulama"] = {"durum": durum, "destek": destek}
                if durum not in ("kaynakli", "editor_onay"):
                    review.append({"tur": "kart_kanit", "deck": did, "slide": s.get("slideNumber"),
                                   "front": front, "destek": destek})
                kept.append(c)
            if "flashcards" in s:
                s["flashcards"] = kept
    return decks, counts, review


def build_question_cards(corpus: LectureCorpus) -> tuple[list[dict], dict, list[dict]]:
    rows = _editor("question_cards.jsonl")
    fixes = {r["question_id"]: r for r in _editor("editor_question_fix.jsonl")}
    counts = {"aday": len(rows), "kart": 0, "red": 0, "duzeltilen": 0}
    cards, review = [], []
    for r in rows:
        f = fixes.get(r["question_id"]) or {}
        if f.get("sil") or (r["durum"] != "kaynakli" and not f.get("onay")) or r.get("celiski") and not f.get("onay"):
            counts["red"] += 1
            review.append({"tur": "soru_karti_red", "question_id": r["question_id"], "durum": r["durum"],
                           "neden": f.get("neden") or ("celiski" if r.get("celiski") else "destek")})
            continue
        stem = _clean(f.get("stem") or r["stem"])
        options = {k: _clean(v) for k, v in (f.get("options") or r["options"]).items()}
        ans = f.get("answer") or r["answer"]
        if f:
            counts["duzeltilen"] += 1
        counts["kart"] += 1
        cards.append({
            "id": f"q:{r['question_id']}", "front": stem, "options": options, "answer": ans,
            "back": f"{ans}) {options[ans]}", "note": _clean(f.get("note") or ""),
            "group": r.get("ders") or "Diğer", "kurul": r.get("kurul"), "konu": r.get("konu"),
            "tekrar": r["tekrar"], "cikis": r["cikis"][:5],
            "kaynak": r["kaynaklar"][0] if r.get("kaynaklar") else None,
            "dogrulama": {"durum": "kaynakli", "destek": r["destek"], "editor": bool(f.get("onay"))},
        })
    cards.sort(key=lambda c: (str(c["group"]), -c["tekrar"]))
    return cards, counts, review


_ATTRIBUTION = re.compile(
    r"^(?:Prof\.\s*Dr\.\s*[^:]{2,40}?|Amfide hoca)\s+(?:amfide\s+)?(?:özellikle\s+)?(?:vurguladı|belirtti|altını çizdi)\s*:\s*")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", ids.fold_tr(text)).strip("-")[:60]


def build_encyclopedia(glossary: dict, new_keys: set) -> tuple[list, dict]:
    """Ansiklopediyi temizler ve yeni (kanıtlı) sözlük terimlerini Sözlük sayfası biçiminde ekler.

    - Ders dosya adından üretilmiş sahte kayıtlar (şablon inci cümlesi) çıkarılır.
    - Doğrulanamayan hoca atıfları ("Prof. Dr. X amfide vurguladı:") nötr "Ders notu bağlamı:" olur.
    - `new_keys` sözlük terimleri, ders notu kaynağı ve kanıt desteğiyle eklenir (aynı adlı kayıt varsa eklenmez).
    """
    enc = store.read_json(ENCYCLOPEDIA_JSON, []) or []
    kept, fixed = [], 0
    for e in enc:
        if _TITLE_PEARL in json.dumps(e, ensure_ascii=False) or e.get("uretici") == "s13_study":
            continue
        note = e.get("lectureContextNotes") or ""
        if _ATTRIBUTION.match(note):
            e["lectureContextNotes"] = _ATTRIBUTION.sub("Ders notu bağlamı: ", note)
            fixed += 1
        kept.append(e)
    have = {ids.norm_key(e.get("term") or e.get("title") or "") for e in kept}
    for e in kept:
        m = re.match(r"^(.+?)\s*\((.+?)\)$", e.get("term") or "")
        if m:
            have.add(ids.norm_key(m.group(1)))
    added = 0
    for key in sorted(new_keys):
        g = glossary[key]
        if ids.norm_key(g["term"]) in have:
            continue
        src = (g.get("kaynaklar") or [{}])[0]
        kaynak = ", ".join(f"{k.get('kaynak')} s.{k.get('sayfa')}" for k in g.get("kaynaklar") or [] if k.get("kaynak"))
        kept.append({
            "id": f"s13-{_slug(g['term'])}", "term": g["term"], "aliases": g.get("aliases") or [],
            "category": g["category"], "kurul": f"Kurul {src['kurul']}" if src.get("kurul") else "Dönem 3",
            "discipline": g.get("discipline") or (src.get("ders") or "").title(),
            "instructorAndSource": f"Ders notu: {kaynak}" if kaynak else "",
            "definition": g["definition"], "lectureContextNotes": "",
            "examSpotPearls": g.get("clinicalPearl") or "",
            "uretici": "s13_study",
            "aiAudit": {"verified": True, "verifiedAt": _now()[:10],
                        "accuracyScore": round(100 * (g.get("dogrulama") or {}).get("destek", 0)),
                        "auditSummary": "Tanım ders notu alıntılarından yazıldı ve kanıt desteği ölçüldü."},
        })
        have.add(ids.norm_key(g["term"]))
        added += 1
    return kept, {"kayit": len(enc), "kalan_eski": len(kept) - added, "atif_notrlendi": fixed, "yeni_eklenen": added}


def build(export: bool = False, log=print) -> dict:
    corpus = LectureCorpus()
    glossary, g_counts, g_rev = build_glossary(corpus)
    old_keys = {r["key"] for r in _editor("glossary_audit.jsonl")}
    encyclopedia, e_counts = build_encyclopedia(glossary, set(glossary) - old_keys)
    decks, d_counts, d_rev = build_decks(corpus)
    qcards, q_counts, q_rev = build_question_cards(corpus)
    config.ensure_core_dirs()
    store.write_core_json(config.DERIVED_DIR / "sozluk.json", glossary)
    store.write_core_jsonl(config.DERIVED_DIR / "soru_kartlari.jsonl", qcards, guard=True)
    store.write_core_jsonl(config.REPORTS_DIR / "study_review.jsonl", g_rev + d_rev + q_rev, guard=False)
    report = {"zaman": _now(), "sozluk": g_counts, "ansiklopedi": e_counts, "deste_kartlari": d_counts, "soru_kartlari": q_counts,
              "inceleme": len(g_rev) + len(d_rev) + len(q_rev), "export": export}
    store.write_core_json(config.REPORTS_DIR / "study_latest.json", report)
    if export:
        if not glossary or not decks:
            raise RuntimeError("boş sonuçla site verisi ezilmez")
        for p in (GLOSSARY_JSON, DECKS_JSON, ENCYCLOPEDIA_JSON):
            _backup(p)
        if QUESTION_CARDS_JSON.exists():
            _backup(QUESTION_CARDS_JSON)
        store.atomic_write_json(GLOSSARY_JSON, glossary, indent=2)
        store.atomic_write_json(DECKS_JSON, decks, indent=2)
        if encyclopedia:
            store.atomic_write_json(ENCYCLOPEDIA_JSON, encyclopedia, indent=2)
        store.atomic_write_json(QUESTION_CARDS_JSON, qcards, indent=1)
    log(json.dumps(report, ensure_ascii=False))
    return report
