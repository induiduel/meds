#!/usr/bin/env python3
"""
Faz 9 — Sözlük destekli soru–kazanım–konu–ders–kurul–müfredat ağacı

Faz 8'in altyapısını (resmi ders programı → kurul/ders/konu, kaynaktan çıkarılmış kazanımlar, iki aşamalı BM25)
aynen kullanır; üzerine şunları ekler:

1. SÖZLÜK KAVRAMLARI (Faz 6.5 medical_thesaurus.json)
   Her terim grubu (Türkçe ad + Latince ad + eş anlamlılar) tek bir kavram belirtecine (§k<id>) dönüşür ve hem soru
   hem kazanım/konu belgelerine eklenir: soruda "hiperkortizolizm", slaytta "Cushing sendromu" yazsa da eşleşir.
   Sözlük yapay zekâ üretimidir ve hatalı "eş anlamlılar" içerir (ör. megaloblastik anemi = pernisiyöz anemi,
   osteosarkom = kemik kanseri). Bu yüzden bir eş anlamlı YALNIZCA ders materyalinde (sınav dökümü hariç) terimle
   materyalde geçiyorsa ve şunlardan biri doğruysa kabul edilir:
     a) yazım varyantı (Latince/İngilizce yazım, "H. pylori" gibi kısaltılmış ilk kelime) — harf benzerliği ≥ 0,8
     b) materyalde eşdeğerlik kalıbıyla yan yana: "X (Y)", "X = Y", "X / Y", "X veya Y", "diğer adıyla",
        "olarak da bilinir", "eski adıyla"
     c) materyalde Y'nin geçtiği slaytların en az yarısında (ve en az 2 slaytta) X de geçiyor
   Geniş kavramlar (koagülopati, adrenal yetmezlik, karbapenem antibiyotik…) ve kısa kısaltmalar (hp, uk) reddedilir.
   Kendi kendinin tekrarı / "X ve Y" → "X Y" gibi sahte eş anlamlılar atılır.

2. GÜVENİLİR METADATA
   * Faz 5: doğrulanmış ders, pedagojik amaç, tıbbi varlıklar, ders slaytı eşleşmeleri (Faz 8'deki gibi; sınav
     dökümü eşleşmeleri atılır).
   * Faz 6.5: soru–slayt çapa terimleri — yalnızca soru metninde geçenler (ders başlıkları elenir).
   * Faz 8 yüksek güven: karşılaştırma ölçütü. Faz 9 aynı konuyu bulursa "dogrulandi", farklı bulursa
     "faz8_celiski" olarak inceleme listesine düşer.
   * Faz 6 (ICD-10, ayırıcı tanı) KULLANILMAZ: elle denetimde uydurma hastalık adları ve yanlış kodlar çıktı.
   * Faz 7 (eski) karantinada, KULLANILMAZ.

Çıktı: meds_temp/phase9/ (Faz 8 ile aynı dosya düzeni + sozluk_kavramlari.json + faz8_karsilastirma.json).
Ana veritabanına yazmaz. Önceki üretim phase9.prev olarak saklanır.

Kullanım:
  python3 scripts/advanced_ai/phase9_thesaurus_graph.py [--sample 40] [--dry-run] [--no-thesaurus]
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

PROJECT = P8.PROJECT
TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp")
OUT9 = TEMP / "phase9"
THESAURUS = PROJECT / "meds_database_v2" / "medical_thesaurus" / "medical_thesaurus.json"
EVIDENCE_THESAURUS = PROJECT / "meds_database_v2" / "evidence_thesaurus" / "kanitli_sozluk.json"
ANCHORS = PROJECT / "meds_database_v2" / "medical_thesaurus" / "phase6_5_question_slide_anchors.jsonl"
PHASE8_MATCH = TEMP / "phase8" / "soru_kazanim.jsonl"

# Eşdeğerlik bildiren bağlaçlar (iki ifade arasındaki boşlukta aranır, katlanmış metinde)
EQUIV_GAP = re.compile(r"^\s*(\(|=|/|veya|ya da|diger adi(yla)?|diger ismi(yle)?|eski adi(yla)?|onceki adi(yla)?|"
                       r"olarak da bilinir|olarak da adlandirilir|nam[iı] diger|yani|ve/veya)\s*$")
_base_stems = P8.stems


def norm(t: str) -> str:
    return " ".join(str(t or "").replace("i̇", "i").replace("̇", "").split())


def fold_keep(s: str) -> str:
    """Parantez, '=' ve '/' korunarak katlama (eşdeğerlik kalıbını görebilmek için)."""
    s = norm(s).translate(P8.TR).lower()
    s = re.sub(r"[^a-z0-9()=/]+", " ", s)
    s = re.sub(r"\s*([()=/])\s*", r" \1 ", s)
    return " ".join(s.split())


# --------------------------------------------------------------------------- 1) Sözlük → doğrulanmış kavramlar
def build_concepts(material_texts: list[str], report: dict) -> dict:
    raw = json.load(open(THESAURUS, encoding="utf-8")) if THESAURUS.exists() else {}
    corpus = "\n".join(fold_keep(t) for t in material_texts)
    stats = collections.Counter()
    concepts = {}
    rejected_examples = []
    chunk_f = [f" {P8.fold(t)} " for t in material_texts]
    _hits: dict[str, set] = {}

    def hits(phrase: str) -> set:
        if phrase not in _hits:
            needle = f" {phrase} "
            _hits[phrase] = {i for i, t in enumerate(chunk_f) if needle in t}
        return _hits[phrase]

    def equiv_pattern(x: str, y: str) -> bool:
        for a_, b_ in ((x, y), (y, x)):
            for m in re.finditer(re.escape(a_), corpus):
                tail = corpus[m.end(): m.end() + len(b_) + 40]
                j = tail.find(b_)
                if 0 <= j <= 40 and EQUIV_GAP.match(tail[:j]):
                    return True
        return False

    from difflib import SequenceMatcher

    def spelling_variant(v: str, sf: str) -> bool:
        """Aynı terimin farklı yazımı: helicobacter pylori ~ helikobakter pilori, myasthenia ~ miyastenia,
        h pylori ~ helikobakter pilori (baş harf + benzer son kelime). Kısa kısaltmalar (hp, uk) kabul edilmez."""
        if len(sf) < 5:
            return False
        if SequenceMatcher(None, v, sf).ratio() >= 0.8:
            return True
        vw, sw = v.split(), sf.split()
        if len(vw) == len(sw) >= 2 and all(a_[0] == b_[0] for a_, b_ in zip(vw, sw)):
            return (SequenceMatcher(None, vw[-1], sw[-1]).ratio() >= 0.75
                    and all(len(b_) == 1 or SequenceMatcher(None, a_, b_).ratio() >= 0.75 for a_, b_ in zip(vw[:-1], sw[:-1])))
        return False

    for key, e in raw.items():
        variants = {v for v in (P8.fold(norm(key)), P8.fold(norm(e.get("turkce") or ""))) if len(v) >= 4}
        if not variants:
            continue
        base = max(variants, key=lambda v: len(hits(v)))  # materyalde en çok geçen yazım
        term_chunks = set().union(*(hits(v) for v in variants))
        if not term_chunks:
            # terim materyalde yok: yalnızca yazım varyantı/kalıp ile eşdeğerliği kanıtlanan üyeler işe yarar
            stats["terim_materyalde_yok"] += 1
        members, evidence = set(), {}
        lat = P8.fold(norm(e.get("latin") or ""))
        cands = [(lat, "latince")] if lat and len(lat) >= 5 else []
        cands += [(P8.fold(norm(x)), "es_anlamli") for x in (e.get("esanlamlilar") or []) if isinstance(x, str)]
        for sf, kind in cands:
            if (not sf or sf in variants or sf in members
                    or any(set(sf.split()) <= set(v.split()) or set(v.split()) <= set(sf.split()) for v in variants)):
                stats["sahte_es_anlamli"] += 1
                continue
            syn_chunks = hits(sf)
            if not syn_chunks:
                stats["es_anlamli_materyalde_yok"] += 1
                continue
            co = len(syn_chunks & term_chunks)
            ratio = co / len(syn_chunks) if term_chunks else 0.0
            if any(spelling_variant(v, sf) for v in variants):
                why = "yazim_varyanti"
            elif any(equiv_pattern(v, sf) for v in variants):
                why = "esdeger_kalip"
            elif co >= 2 and ratio >= 0.5:
                why = f"birlikte_gecme_{co}/{len(syn_chunks)}"
            else:
                stats["es_anlamli_red"] += 1
                if len(rejected_examples) < 25:
                    rejected_examples.append(f"{base} ≠ {sf} (birlikte {co}/{len(syn_chunks)})")
                continue
            members.add(sf)
            evidence[sf] = why
            stats[f"kabul_{kind}"] += 1
        if members:
            cid = "§k" + P8.sid(base)[:6]
            concepts[cid] = {"terim": base, "uyeler": sorted(members | variants), "kanit": evidence,
                             "kurul": e.get("kurul"), "brans": e.get("brans")}
    report["sozluk"] = {"terim": len(raw), "kavram": len(concepts), **dict(stats),
                        "reddedilen_ornek": rejected_examples}
    return concepts


def load_evidence_concepts(report: dict) -> dict:
    """Kanıtlı sözlük (build_evidence_thesaurus.py): kısaltma + yazım varyantı çiftleri, güven yüksek/orta.
    Parantez eşdeğerleri ("inceleme") kullanılmaz. 3 harften kısa kısaltmalar (ra, ms…) eşleştirmede belirsiz → atılır.
    Çiftler birleşim-bul ile kavram gruplarına dönüştürülür (terim ~ kısaltma ~ yazım varyantları)."""
    if not EVIDENCE_THESAURUS.exists():
        report["kanitli_sozluk"] = {"yok": True}
        return {}
    raw = json.load(open(EVIDENCE_THESAURUS, encoding="utf-8"))
    parent: dict[str, str] = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = collections.Counter()
    for key, e in raw.items():
        a = P8.fold(norm(e.get("turkce") or key))
        for syn in e.get("esanlamlilar") or []:
            g = (e.get("guven") or {}).get(syn)
            tur = ((e.get("kanit") or {}).get(syn) or {}).get("tur")
            if g not in ("yuksek", "orta") or tur not in ("kisaltma", "yazim_varyanti"):
                used["atlanan"] += 1
                continue
            b = P8.fold(norm(syn))
            if not a or not b or a == b or len(b.replace(" ", "")) < 3 or len(a.replace(" ", "")) < 3:
                used["kisa"] += 1
                continue
            parent[find(a)] = find(b)
            used[tur] += 1
    groups = collections.defaultdict(set)
    for x in list(parent):
        groups[find(x)].add(x)
    concepts = {}
    for members in groups.values():
        if len(members) < 2 or len(members) > 12:   # aşırı büyüyen grup = zincirleme hata; kullanılmaz
            used["grup_cok_buyuk" if len(members) > 12 else "tekil"] += 1
            continue
        head = max(members, key=len)
        concepts["§e" + P8.sid(head)[:6]] = {"terim": head, "uyeler": sorted(members), "kaynak": "kanitli_sozluk"}
    report["kanitli_sozluk"] = {"kavram": len(concepts), **dict(used)}
    return concepts


def install_concept_stems(concepts: dict):
    """P8.stems'i kavram belirteci ekleyen sürümle değiştirir (Faz 8 fonksiyonları bunu kullanır)."""
    phrase_to_cid = {}
    for cid, c in concepts.items():
        for m in c["uyeler"]:
            phrase_to_cid[m] = cid
    if not phrase_to_cid:
        return
    pat = re.compile(r"(?<![a-z0-9])(" + "|".join(re.escape(p) for p in sorted(phrase_to_cid, key=len, reverse=True))
                     + r")(?![a-z0-9])")

    def stems_with_concepts(s: str) -> list[str]:
        out = _base_stems(s)
        for m in pat.finditer(P8.fold(s)):
            out.append(phrase_to_cid[m.group(1)])
        return out

    P8.stems = stems_with_concepts


# --------------------------------------------------------------------------- 2) Güvenilir metadata
def add_anchor_terms(phase5: dict, report: dict):
    """Faz 6.5 çapa terimleri: yalnızca soru metninde geçenler Faz 5 'varlık' metnine eklenir."""
    qtext = {}
    for p in sorted((P8.DB / "questions").glob("*.jsonl")):
        for q in P8.read_jsonl(p):
            opts = q.get("options") or {}
            qtext[q["question_id"]] = P8.fold(" ".join([q.get("stem") or ""] + (list(opts.values()) if isinstance(opts, dict) else [])))
    used = 0
    if ANCHORS.exists():
        for r in P8.read_jsonl(ANCHORS):
            qid = r.get("question_id")
            qt = f" {qtext.get(qid, '')} "
            terms = [norm(t) for t in r.get("common_medical_terms") or [] if isinstance(t, str)]
            terms = [t for t in terms if len(t.split()) <= 4 and f" {P8.fold(t)} " in qt]
            if terms:
                phase5.setdefault(qid, {"ders": None, "konu": None, "amac": "", "varlik": "", "slayt_src": set(), "slayt_chunk": set()})
                phase5[qid]["varlik"] = (phase5[qid].get("varlik") or "") + " " + " ".join(terms)
                used += 1
    report["faz6_5_capa"] = {"kullanilan_soru": used}


def compare_with_phase8(matches: list, report: dict) -> dict:
    """Faz 8 yüksek güven (elle denetlendi: 20/20 doğru/kısmen doğru) ÖNCELİKLİDİR.
    * aynı konu  → karar "faz8_faz9_ayni", güven yüksek
    * çelişki    → Faz 8 kazanımı korunur (karar "faz8_onceligi"), Faz 9 önerisi `faz9_aday` olarak saklanır
    * Faz 8'de yüksek değil → Faz 9 sonucu kullanılır (karar "faz9")"""
    p8 = {}
    if PHASE8_MATCH.exists():
        for r in P8.read_jsonl(PHASE8_MATCH):
            if r.get("guven") == "yuksek" and r.get("kazanimlar"):
                p8[r["soru_id"]] = r
    c = collections.Counter()
    conflicts = []
    for r in matches:
        a = p8.get(r["soru_id"])
        if not a or not r.get("kazanimlar"):
            r["karar"] = "faz9"
            c["karar_faz9_" + str(r.get("guven"))] += 1
            continue
        ka, kb = a["kazanimlar"][0], r["kazanimlar"][0]
        if ka["konu_id"] == kb["konu_id"]:
            c["ayni_konu"] += 1
            r["karar"] = "faz8_faz9_ayni"
            r["guven"] = "yuksek"
            continue
        c["ayni_ders_farkli_konu" if P8.ders_key(ka["ders"]) == P8.ders_key(kb["ders"]) else "farkli_ders"] += 1
        conflicts.append({"soru_id": r["soru_id"], "faz8": f"{ka['ders']} / {ka['konu']}", "faz9": f"{kb['ders']} / {kb['konu']}"})
        r["faz9_aday"] = {"guven": r.get("guven"), "kazanimlar": r["kazanimlar"]}
        r["kazanimlar"] = a["kazanimlar"]
        r["guven"] = "yuksek"
        r["fark"] = a.get("fark")
        r["karar"] = "faz8_onceligi"
    n = c["ayni_konu"] + c["ayni_ders_farkli_konu"] + c["farkli_ders"]
    report["faz8_karsilastirma"] = {"faz8_yuksek": len(p8), "karsilastirilan": n, **dict(c),
                                    "ayni_konu_%": round(100 * c["ayni_konu"] / n, 1) if n else None}
    return {"ozet": report["faz8_karsilastirma"], "celiskiler": conflicts}


# --------------------------------------------------------------------------- ana akış
def main():
    ap = argparse.ArgumentParser(description="Faz 9 — sözlük destekli müfredat ağacı")
    ap.add_argument("--sample", type=int, default=40)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-thesaurus", action="store_true", help="sözlüğü kapat (etkisini ölçmek için)")
    ap.add_argument("--extra-concepts", help="ek kavram dosyası {id: {terim, uyeler}} (Faz 10: Wikidata/UMLS kimlikleri)")
    ap.add_argument("--out", help="çıktı klasörü (varsayılan meds_temp/phase9)")
    ap.add_argument("--label", default="Faz 9")
    a = ap.parse_args()
    global OUT9
    if a.out:
        OUT9 = Path(a.out)
    t0 = time.time()
    report = {"uretim": {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "betik": "phase9_thesaurus_graph.py", "etiket": a.label,
                         "yontem": "Faz 8 + doğrulanmış sözlük kavramları + Faz 5/6.5 güvenilir metadata",
                         "kullanilmayan": ["faz6 (doğrulanmamış AI: uydurma ayırıcı tanı/ICD)", "faz7 (karantina)"],
                         "veritabani_degistirildi": False}}

    kurullar, dersler, konular = P8.build_program()
    P8.attach_curriculum(kurullar, konular, report)
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    # Kaynak bağlama sözlüksüz yapılır (konu–kaynak bağı Faz 8 ile aynı kalsın); sınav dökümleri belirlenir
    source_rows = P8.link_sources(konular, dersler, sources, chunks_by_src, report)
    dump_ids = {r["kaynak_id"] for r in source_rows if r["tip"] == "sinav_dokumu"}

    if not a.no_thesaurus:
        material = [c.get("text") or "" for sid_, cs in chunks_by_src.items() if sid_ not in dump_ids for c in cs]
        concepts = build_concepts(material, report)            # eski sözlük (doğrulanmış kısım)
        concepts.update(load_evidence_concepts(report))          # kanıtlı sözlük
        if a.extra_concepts and Path(a.extra_concepts).exists():
            extra = json.load(open(a.extra_concepts, encoding="utf-8"))
            concepts.update({cid: c for cid, c in extra.items() if len(c.get("uyeler") or []) >= 2})
            report["ek_kavramlar"] = {"dosya": a.extra_concepts, "kavram": len(extra)}
        install_concept_stems(concepts)
    else:
        concepts = {}
        report["sozluk"] = {"kapali": True}

    kazanimlar = P8.build_kazanimlar(konular, dersler, chunks_by_src, source_rows)
    phase5 = P8.load_phase5(dump_ids)
    add_anchor_terms(phase5, report)
    matches, review = P8.match_questions(kazanimlar, konular, chunks_by_src, report, a.sample, phase5, use_hints=True)
    cmp = compare_with_phase8(matches, report)
    review_ids = {r["soru_id"] for r in review}
    for r in matches:
        if r.get("karar") == "faz8_onceligi" and r["soru_id"] not in review_ids:
            review.append({**r, "neden": "Faz 9 farklı konu öneriyor (Faz 8 korundu)"})
    P8.validate(kurullar, dersler, konular, kazanimlar, matches, report)
    report["uretim"]["sure_sn"] = round(time.time() - t0, 1)

    if not a.dry_run:
        P8.OUT = OUT9  # Faz 8 yazıcısı aynı düzeni phase9/ altına atomik yazar (önceki: phase9.prev)
        P8.write_outputs(kurullar, dersler, konular, kazanimlar, source_rows, matches, review, report)
        json.dump({cid: c for cid, c in concepts.items()}, open(OUT9 / "sozluk_kavramlari.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        json.dump(cmp, open(OUT9 / "faz8_karsilastirma.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    keys = ("sayilar", "kural_dogrulama", "sozluk", "kanitli_sozluk", "ek_kavramlar", "faz6_5_capa", "faz8_karsilastirma", "sorular")
    print(json.dumps({k: report.get(k) for k in keys}, ensure_ascii=False, indent=1))
    print(f"\nÇıktı: {OUT9}" if not a.dry_run else "\n(dry-run: dosya yazılmadı)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
