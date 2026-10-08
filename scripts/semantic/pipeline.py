"""Uçtan uca motor: soru → normalize → NER → niyet → embedding → vektör arama → yeniden sıralama →
hiyerarşik sınıflandırma (Ders/Konu/Kazanım). Deterministik + CPU e5; GPU yok.
"""
from __future__ import annotations

import json
import os

from . import config, embeddings, intent, medical, ner, nlp, taxonomy, vectorstore


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _support(text: str, support_text: str) -> float:
    q = set(nlp.tokens(support_text))
    if not q:
        return 1.0
    ev = set(nlp.tokens(text))
    return len(q & ev) / len(q)


def _char_ngrams(s: str, n: int = 4) -> set:
    s = nlp.fold(s).replace(" ", "")
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def _cjac(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class Engine:
    def __init__(self):
        self.store = vectorstore.Store()
        self.tax = taxonomy.load()
        try:
            self.lexicon = json.loads(config.LEXICON_PATH.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            self.lexicon = medical.build_lexicon()
        from . import lexindex

        self.lexindex = lexindex
        self.reranker = None
        if os.environ.get("MEDS_SEM_CE", "0").lower() in {"1", "true", "yes", "on"}:
            try:
                from sentence_transformers import CrossEncoder

                self.reranker = CrossEncoder(config.RERANK_MODEL, device="cpu", max_length=384)
            except Exception:  # noqa: BLE001
                self.reranker = None

    def retrieve(self, question: str, k: int = config.TOP_K, kurul: int | None = None) -> list[dict]:
        """Yoğun (FAISS) + sözlüksel (TF-IDF) füzyon, ardından iki aşamalı yeniden sıralama. CPU."""
        m = self.tax.match(question, kurul=kurul)
        ents = ner.extract(question, self.lexicon)
        ent_terms = " ".join(e.get("terim", "") for e in ents[:8])
        qexp = " ".join([question, m.get("konu", "") or "", m.get("kazanim", "") or "", ent_terms]).strip()
        qv = embeddings.embed_query(qexp)
        dense = self.store.search(qv, k=150)
        qtoks = set(nlp.tokens(question))
        qstems = set(nlp.stems(question))
        qgrams = _char_ngrams(question)
        q_ders, q_konu = m.get("ders"), m.get("konu")

        cand: dict[int, dict] = {}
        for h in dense:
            i = self.store.idx_of.get(h.get("chunk_id"))
            if i is None:
                continue
            cand[i] = {"meta": h, "dense": h.get("skor", 0.0), "tfidf": 0.0}
        for i, s in self.lexindex.search(qexp, k=150):
            row = cand.get(i) or {"meta": dict(self.store.metas[i]), "dense": 0.0, "tfidf": 0.0}
            row["tfidf"] = s
            cand[i] = row

        for _i, f in cand.items():
            text = f["meta"].get("text") or ""
            ctoks = set(nlp.tokens(text))
            cov = (len(qtoks & ctoks) / len(qtoks)) if qtoks else 0.0
            scov = (len(qstems & set(nlp.stems(text))) / len(qstems)) if qstems else 0.0
            f["cov"], f["scov"] = cov, scov
            f["stage1"] = 0.45 * f["dense"] + 0.45 * f["tfidf"] + 0.20 * cov

        top = sorted(cand.values(), key=lambda f: -f["stage1"])[:30]
        for f in top:
            text = f["meta"].get("text") or ""
            gram = _cjac(qgrams, _char_ngrams(text))
            boost = 0.0
            if q_konu and f["meta"].get("konu") == q_konu:
                boost = 1.0
            elif q_ders and f["meta"].get("ders") == q_ders:
                boost = 0.5
            f["hibrit"] = round(
                0.30 * f["dense"] + 0.28 * f["tfidf"] + 0.22 * f["cov"]
                + 0.06 * f["scov"] + 0.09 * gram + 0.05 * boost, 4)
            f["meta"]["hibrit"] = f["hibrit"]
            f["meta"]["kapsam"] = round(f["cov"], 3)

        # Cross-encoder yeniden sıralama (CPU, varsa)
        if self.reranker is not None and top:
            import math

            smax = max((f["stage1"] for f in top), default=1.0) or 1.0
            rk = top[:15]
            pairs = [(question, (f["meta"].get("text") or "")[:400]) for f in rk]
            scores = self.reranker.predict(pairs, batch_size=32, show_progress_bar=False)
            for f, sc in zip(rk, scores):
                ce = 1.0 / (1.0 + math.exp(-float(sc)))
                f["meta"]["ce"] = round(ce, 4)
                f["hibrit"] = round(0.6 * ce + 0.4 * (f["stage1"] / smax), 4)
                f["meta"]["hibrit"] = f["hibrit"]

        top.sort(key=lambda f: -f["hibrit"])
        hits = [f["meta"] for f in top]
        if kurul is not None:
            hits.sort(key=lambda h: (0 if h.get("kurul") == kurul else 1, -h.get("hibrit", 0)))
        return hits[:k]

    def classify(self, question: str, kurul: int | None = None) -> dict:
        text = nlp.normalize(question)
        ents = ner.extract(text, self.lexicon)
        ent_sum = ner.summarize(ents)
        intt = intent.classify(text)
        hits = self.retrieve(text, kurul=kurul)
        top = hits[0] if hits else {}
        m = self.tax.match(text, kurul=kurul)
        # Sınıflandırma KANITA dayandırılır: en iyi parçanın metadata'sı öncelikli, taksonomi yedek.
        ders = top.get("ders") or m.get("ders")
        konu = top.get("konu") or m.get("konu")
        kazanim = m.get("kazanim") or top.get("kazanim")
        return {
            "soru": text,
            "niyet": intt,
            "varliklar": ent_sum,
            "ders": ders,
            "konu": konu,
            "kazanim": kazanim,
            "taksonomi": {k: m.get(k) for k in ("ders", "konu", "kazanim", "konu_skor") if m.get(k)},
            "guven": round(float((top.get("hibrit") or top.get("skor") or 0.0)), 4),
            "kanit": {
                "chunk_id": top.get("chunk_id"),
                "source_id": top.get("source_id"),
                "sayfa": top.get("page"),
                "ders": top.get("ders"),
                "konu": top.get("konu"),
            },
            "adaylar": [{"chunk_id": h.get("chunk_id"), "source_id": h.get("source_id"),
                         "page": h.get("page"), "skor": h.get("hibrit", h.get("skor"))}
                        for h in hits[: config.RERANK_K]],
        }
