"""Revize v2 — motor: RAG zeminleme + AI revizyonu + kural doğrulama + değişiklik kaydı.

Her soru için: kanıt getir (semantic RAG) → kazanım eşle (taxonomy) → NER → AI revizyonu → doğrula
→ kayıt. Kaldığı yerden devam eder (checkpoint). Ücretsiz bulut AI + CPU; GPU yok.
"""
from __future__ import annotations

from ..core import evidence as evmod
from ..core import llm, store
from . import config, model, prompt, validate

_SEM = None


def _sem():
    global _SEM
    if _SEM is None:
        try:
            from semantic import pipeline as sem

            _SEM = sem.Engine()
        except Exception:  # noqa: BLE001
            _SEM = False
    return _SEM


def _evidence(text: str, k: int = 5) -> list[dict]:
    sem = _sem()
    if not sem:
        return []
    hits = sem.retrieve(text, k=k)
    out = []
    for h in hits:
        out.append({"chunk_id": h.get("chunk_id"), "source_id": h.get("source_id"),
                    "sayfa": h.get("page"), "text": h.get("text") or ""})
    return out


def _tax(text: str) -> dict:
    sem = _sem()
    return sem.tax.match(text) if sem else {}


def _ner_terms(text: str) -> list[str]:
    sem = _sem()
    if not sem:
        return []
    try:
        return [e.get("terim") for e in sem.ner.extract(text, sem.lexicon)][:12]
    except Exception:  # noqa: BLE001
        return []


def _categorize(revised: dict) -> str:
    oncul = revised.get("oncul") or []
    opts = revised.get("secenekler") or {}
    if isinstance(oncul, list) and len(oncul) >= 2:
        return "oncul"
    if isinstance(opts, dict) and len(opts) >= 4:
        return "kapali"
    return "acik"


def _assemble(qid: str, revised: dict, source: dict, val: dict, tax: dict, evidence: list[dict]) -> dict:
    opts = validate._opt_map(revised.get("secenekler"))
    return {
        "id": qid,
        "revize": config.REVIZE_TAG,
        "durum": "revize" if not val["karantina"] else "karantina",
        "kategori": _categorize(revised),
        "ders_adi": revised.get("ders_adi") or tax.get("ders") or source.get("ders_adi"),
        # kurul: kaynağın kendi gösterimi korunur (TIP310 vb.); yoksa taksonomi sayısı.
        "kurul_adi": source.get("kurul_adi") or (tax.get("kurul") if tax.get("kurul") is not None
                                                 else revised.get("kurul_adi")),
        "konu_adi": revised.get("konu_adi") or tax.get("konu") or source.get("konu_adi"),
        "kazanim": revised.get("kazanim") or tax.get("kazanim"),
        "soru_koku": revised.get("soru_koku"),
        "oncul": revised.get("oncul") or [],
        "secenekler": opts,
        "dogru_secenek": (revised.get("dogru_secenek") or "").upper()[:1] or None,
        "belirsiz": bool(revised.get("belirsiz")),
        "aciklama": revised.get("aciklama"),
        "aciklama_maddeleri": revised.get("aciklama_maddeleri") or [],
        "terimler": _ner_terms((revised.get("soru_koku") or "") + " " + " ".join(opts.values())),
        "kaynak_baglari": [{"chunk_id": e.get("chunk_id"), "source_id": e.get("source_id"),
                            "sayfa": e.get("sayfa"), "alinti": (e.get("text") or "")[:240]} for e in evidence],
        "support_ratio": round(evmod.support_ratio(
            f"{revised.get('soru_koku') or ''} {revised.get('aciklama') or ''}",
            [e.get("text") or "" for e in evidence]), 4),
        "dogrulama": {"issues": val["issues"], "karantina": val["karantina"]},
        "degisiklikler": val["degisiklikler"],
        "faz14_durum": source.get("_faz14_status"),
        "model": llm.last_model.get("ad"),
        "zaman": store.now_iso(),
    }


API_DURAK_LIMIT = 10   # art arda LLM başarısızlığı → API çalışmıyor


def run(limit: int = 20, *, log=print) -> dict:
    config.ensure_dirs()
    state = store.State("revize_v2", state_dir=config.STATE)
    inputs = model.load_inputs()
    counts = {"aday": len(inputs), "islenen": 0, "revize": 0, "karantina": 0, "atlanan": 0, "bos_yanit": 0}
    api_basarisiz = 0
    for item in inputs:
        qid = item["id"]
        if state.is_done(qid):
            counts["atlanan"] += 1
            continue
        if counts["islenen"] >= limit:
            break
        text = " ".join([item.get("soru_koku") or "", *item.get("secenekler", {}).values()])
        ev = _evidence(text)
        tax = _tax(text)
        pr = prompt.build(item, tax, ev)
        data = llm.chat_json(pr, max_tokens=2600)
        counts["islenen"] += 1
        if not isinstance(data, dict):
            counts["bos_yanit"] += 1
            api_basarisiz += 1
            if api_basarisiz >= API_DURAK_LIMIT:
                log(f"revize v2: {api_basarisiz} soru art arda başarısız — API yanıt vermiyor, durduruluyor")
                counts["api_basarisiz"] = True
                break
            continue  # denenmedi say; sonraki turda yeniden
        api_basarisiz = 0
        # Açıklamadan kaynak/atıf/meta ifadelerini temizle (yoksa yeniden üretmek yerine temizle).
        clean_acik, acik_degisti = validate.sanitize_aciklama(data.get("aciklama") or "")
        if acik_degisti:
            data["aciklama"] = clean_acik
        val = validate.validate(data, item, support_ratio=evmod.support_ratio(
            f"{data.get('soru_koku') or ''} {data.get('aciklama') or ''}",
            [e.get("text") or "" for e in ev]))
        rec = _assemble(qid, data, item, val, tax, ev)
        store.append_jsonl(config.QUESTIONS_OUT, rec)
        if val["degisiklikler"]:
            store.append_jsonl(config.CHANGES_OUT, {"id": qid, "zaman": rec["zaman"],
                                                    "model": rec["model"], "degisiklikler": val["degisiklikler"]})
        if val["karantina"]:
            store.append_jsonl(config.QUARANTINE_OUT, {"id": qid, "neden": val["issues"],
                                                       "issues": val["issues"], "zaman": rec["zaman"]})
            counts["karantina"] += 1
        else:
            counts["revize"] += 1
        state.mark_done(qid)
        log(f"  {qid}: {'revize' if not val['karantina'] else 'karantina'} {val['issues'] or ''}")
    log(f"revize v2: {counts}")
    return counts
