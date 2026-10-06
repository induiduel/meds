#!/usr/bin/env python3
"""
Faz 5 / 6 / 6.5 / 8 çıktılarını sitenin okuyacağı tek bir temiz dosyada birleştirir.

Çıktı: $MEDS_DATABASE_DIR/derived/phase_insights/insights.json   (soru_id → analiz)
  * mufredat: Faz 9 birleşik çıktısı, yalnızca Faz 8 yüksek güvenli kayıtlar (Faz 9 da aynı konuyu bulduysa
             dogrulama="iki_yontem"); Faz 9 yoksa Faz 8 — kurul/ders/konu/kazanım + slayt kanıtı
  * faz6_5 + kanıtlı sözlük: soruda geçen kısaltmaların ders materyalindeki açılımları
  * faz5   : doğrulanmış ders/konu, pedagojik amaç, ne sormuş, tıbbi varlıklar, ders slaytı eşleşmeleri
             (sınav dökümü kaynakları kanıt sayılmaz ve atılır)
  * faz6_5 : ortak terimler + soru–slayt çapası (sınav dökümü değilse) + sözlükteki eş anlamlılar
  * faz6   : yapay zekâ üretimi derin metadata (ICD-10, ayırıcı tanı, disiplinler) — DOĞRULANMAMIŞ olarak işaretli
Python repr olarak saklanmış alanlar (ör. "{'a': 1}") ast.literal_eval ile çözülür.
Boş sonuç mevcut dosyanın üzerine yazılmaz; yazım atomiktir.
Faz zinciri (phase_cycle.py) Faz 8'den sonra bunu çalıştırır.
"""
from __future__ import annotations

import ast
import glob
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or PROJECT / "meds_database")
V2 = PROJECT / "meds_database_v2"
P8 = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp") / "phase8" / "soru_kazanim.jsonl"
P9 = P8.parent.parent / "phase9" / "soru_kazanim.jsonl"
EVID = V2 / "evidence_thesaurus" / "kanitli_sozluk.json"
OUT = DB / "derived" / "phase_insights" / "insights.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))


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


def clip(s, n=320):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def norm(t: str) -> str:
    """Bozuk birleşik nokta (i̇) ve madde imlerini temizler."""
    return " ".join(str(t or "").replace("i\u0307", "i").replace("\u0307", "").lstrip("✓•-–* ").split())


def fold(t: str) -> str:
    tr = str.maketrans("ıİçÇğĞöÖşŞüÜI", "iiccggoossuui")
    return " ".join("".join(ch if ch.isalnum() else " " for ch in norm(t).translate(tr).lower()).split())


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except Exception:
                continue


def load_sources_and_dumps():
    from phase8_curriculum_graph import is_exam_dump  # aynı ölçüt
    sources, by_src = {}, {}
    for p in glob.glob(str(DB / "sources" / "*.json")):
        try:
            s = json.load(open(p, encoding="utf-8"))
            sources[s["source_id"]] = s
        except Exception:
            pass
    for p in glob.glob(str(DB / "chunks" / "*.jsonl")):
        sid = Path(p).stem
        by_src[sid] = [c for _, c in zip(range(40), jsonl(p))]
    dumps = {sid for sid, s in sources.items() if is_exam_dump(s, by_src)}
    return sources, dumps


def src_name(sources, sid):
    s = sources.get(sid) or {}
    return s.get("name") or s.get("title") or sid


def main():
    sources, dumps = load_sources_and_dumps()
    items: dict[str, dict] = {}
    qtext: dict[str, str] = {}
    qraw: dict[str, str] = {}
    anstext: dict[str, str] = {}
    cnt = {"faz5": 0, "faz6": 0, "faz6_5": 0}

    # ---- Faz 5
    for p in glob.glob(str(V2 / "questions" / "*.jsonl")):
        for q in jsonl(p):
            qid = q.get("question_id")
            if not qid:
                continue
            audit = parse(q.get("classification_audit")) or {}
            tax = parse(q.get("taxonomy_metadata")) or {}
            ents = parse(q.get("tibbi_varliklar")) or {}
            slides = []
            for m in parse(q.get("slide_matches")) or []:
                sid = m.get("source_id")
                if not sid or sid in dumps:
                    continue
                slides.append({"kaynak": src_name(sources, sid), "source_id": sid, "sayfa": m.get("page"),
                               "chunk_id": m.get("chunk_id"), "metin": clip(m.get("sample_text"), 260)})
                if len(slides) >= 3:
                    break
            ans = (parse(q.get("options")) or {}).get((q.get("answer") or "").strip().upper())
            if ans:
                anstext[qid] = fold(ans)
            qraw[qid] = " ".join([q.get("stem") or ""] + list((parse(q.get("options")) or {}).values()))
            qtext[qid] = fold(" ".join([q.get("stem") or ""] + list((parse(q.get("options")) or {}).values())))
            # "entities" alanı eşleştirme kelimesidir (aksansız kök), terim değildir; yalnızca taxonomy terimleri
            items.setdefault(qid, {})["faz5"] = {
                "ders": audit.get("verified_ders"), "kurul": audit.get("verified_kurul"),
                "konu": audit.get("verified_konu"), "pedagojik_amac": q.get("pedagogik_amac"),
                "ne_sormus": tax.get("ne_sormus"), "alt_konu": tax.get("alt_konu"),
                "terimler": [norm(t) for t in (tax.get("terimler") or []) if isinstance(t, str)],
                "tibbi_varliklar": ents if isinstance(ents, dict) else {},
                "slaytlar": slides,
            }
            cnt["faz5"] += 1

    # ---- Faz 6: yalnızca doğrulayıcıdan (validate_phase6_metadata.py) geçen öğeler — materyalde kanıtlı ayırıcı tanılar;
    # ICD kodları resmî liste olmadan kabul edilmez. Ham Faz 6 çıktısı yayınlanmaz.
    vp = V2 / "deep_metadata_validated" / "dogrulama.jsonl"
    if vp.exists():
        for r in jsonl(vp):
            qid = r.get("question_id")
            if not qid or not (r.get("ayirici_tani") or r.get("icd10")):
                continue
            items.setdefault(qid, {})["faz6"] = {
                "dogrulanmadi": False, "kaynak": "materyal_kaniti",
                "icd10": r.get("icd10") or [],
                "ayirici_tani": [{"hastalik": x.get("hastalik"), "ozellik": clip(x.get("ozellik"), 200)}
                                 for x in (r.get("ayirici_tani") or [])][:5],
            }
            cnt["faz6"] += 1

    # ---- Faz 6.5
    thes = {}
    tp = V2 / "medical_thesaurus" / "medical_thesaurus.json"
    if tp.exists():
        try:
            thes = json.load(open(tp, encoding="utf-8"))
        except Exception:
            thes = {}
    ap = V2 / "medical_thesaurus" / "phase6_5_question_slide_anchors.jsonl"
    if ap.exists():
        for r in jsonl(ap):
            qid = r.get("question_id")
            if not qid:
                continue
            qt = qtext.get(qid) or fold(r.get("stem") or "")
            terms = [norm(t) for t in (r.get("common_medical_terms") or []) if isinstance(t, str)]
            terms = [t for t in terms if len(t.split()) <= 4 and fold(t) and f" {fold(t)} " in f" {qt} "]
            syn = {}
            for t in terms:
                e = thes.get(t) if isinstance(thes, dict) else None
                if isinstance(e, dict) and e.get("esanlamlilar"):
                    uniq, seen_f = [], {fold(t)}
                    for x in e["esanlamlilar"]:
                        if (isinstance(x, str) and len(x) < 60 and fold(x) and fold(x) not in seen_f
                                and not set(fold(x).split()) <= set(fold(t).split())):  # "X ve Y" → "X Y" eş anlamlı değil
                            seen_f.add(fold(x))
                            uniq.append(norm(x))
                    if uniq:
                        syn[t] = uniq[:4]
            g = r.get("gold_slide") or {}
            slide = None
            f5src = {x.get("source_id") for x in (items.get(qid, {}).get("faz5", {}).get("slaytlar") or [])}
            gtxt = fold(g.get("text_snippet") or "")
            at = anstext.get(qid, "")
            # çapa slaytı yalnızca Faz 5 kaynağıyla aynıysa ya da doğru cevabı içeriyorsa gösterilir
            related = g.get("source_id") in f5src or (len(at) >= 4 and f" {at} " in f" {gtxt} ")
            if g.get("source_id") and g["source_id"] not in dumps and related:
                slide = {"kaynak": src_name(sources, g["source_id"]), "source_id": g["source_id"], "sayfa": g.get("page"),
                         "chunk_id": g.get("chunk_id"), "metin": clip(g.get("text_snippet"), 260)}
            if terms or slide:
                items.setdefault(qid, {})["faz6_5"] = {"terimler": terms, "esanlamlilar": syn, "slayt": slide}
                cnt["faz6_5"] += 1

    # ---- Müfredat bağlantısı: Faz 9 birleşik çıktısı (Faz 8 öncelikli), yoksa Faz 8
    # Yalnızca Faz 8 yüksek güvenli kayıtlar yayınlanır. Faz 9'un tek başına "yüksek" dediği eşleşmeler elle denetimde
    # ~%45 doğru çıktı → yayınlanmaz. Faz 9 aynı konuyu bulduysa "iki_yontem" olarak işaretlenir.
    src, use9 = (P9, True) if P9.exists() else (P8, False)
    if src.exists():
        for r in jsonl(src):
            if r.get("guven") != "yuksek":
                continue
            karar = r.get("karar") if use9 else "faz8"
            if use9 and karar not in ("faz8_faz9_ayni", "faz8_onceligi"):
                continue
            qid = r.get("soru_id")
            ks = []
            for k in (r.get("kazanimlar") or [])[:2]:
                kn = k.get("kanit") or {}
                ks.append({"kazanim": norm(k.get("kazanim")), "konu": k.get("konu"), "ders": k.get("ders"),
                           "kurul": k.get("kurul"),
                           "kanit": {"tip": kn.get("tip"), "kaynak": kn.get("kaynak_adi"), "sayfa": kn.get("sayfa"),
                                     "chunk_id": kn.get("chunk_id"), "metin": clip(kn.get("metin"), 320)} if kn else None})
            if qid and ks:
                items.setdefault(qid, {})["mufredat"] = {
                    "guven": "yuksek", "kazanimlar": ks,
                    "dogrulama": "iki_yontem" if karar == "faz8_faz9_ayni" else "faz8"}
                cnt["mufredat"] = cnt.get("mufredat", 0) + 1
                cnt["iki_yontem"] = cnt.get("iki_yontem", 0) + (karar == "faz8_faz9_ayni")

    # ---- Faz 11: soru ↔ ders slaytı (yalnızca yüksek/orta güven; elle denetim ~%78 doğru, düşükler hakem kuyruğunda)
    p11 = P8.parent.parent / "phase11" / "soru_slayt.jsonl"
    if p11.exists():
        for r in jsonl(p11):
            if r.get("guven") not in ("yuksek", "orta") or not r.get("slaytlar"):
                continue
            items.setdefault(r["soru_id"], {})["slayt"] = {
                "guven": r["guven"],
                "slaytlar": [{"kaynak": x.get("kaynak"), "sayfa": x.get("sayfa"), "chunk_id": x.get("chunk_id"),
                              "alinti": clip(x.get("alinti"), 380), "gerekce": x.get("gerekce")} for x in r["slaytlar"][:2]],
            }
            cnt["slayt"] = cnt.get("slayt", 0) + 1

    # ---- Kanıtlı sözlük: soruda geçen kısaltmaların açılımı (ders materyalinden, kaynaklı)
    if EVID.exists():
        abbr = {}  # katlanmış kısaltma → (kısaltma, açılım)
        for key, e in json.load(open(EVID, encoding="utf-8")).items():
            for syn in e.get("esanlamlilar") or []:
                kd = ((e.get("kanit") or {}).get(syn) or {})
                if kd.get("tur") == "kisaltma" and (e.get("guven") or {}).get(syn) in ("yuksek", "orta") and len(fold(syn).replace(" ", "")) >= 3:
                    abbr[fold(syn)] = (syn, e.get("turkce") or key)
        if abbr:
            import re as _re
            pat = _re.compile(r"(?<![a-z0-9])(" + "|".join(_re.escape(k) for k in sorted(abbr, key=len, reverse=True)) + r")(?![a-z0-9])")
            for qid, raw in qraw.items():
                found = {}
                for m in pat.finditer(fold(raw)):
                    ab, exp = abbr[m.group(1)]
                    found[ab] = exp
                if found:
                    f65 = items.setdefault(qid, {}).setdefault("faz6_5", {"terimler": [], "esanlamlilar": {}, "slayt": None})
                    for ab, exp in list(found.items())[:6]:
                        f65["esanlamlilar"].setdefault(ab, [exp])
                    cnt["kisaltma_acilimi"] = cnt.get("kisaltma_acilimi", 0) + 1

    if not items:
        print("Hiç kayıt yok; mevcut dosya korunuyor.")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".tmp")
    json.dump({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "counts": cnt, "items": items},
              open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, OUT)
    print(json.dumps({"soru": len(items), **cnt, "sinav_dokumu_kaynak": len(dumps), "dosya": str(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
