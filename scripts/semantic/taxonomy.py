"""Hedef bilgi tabanı: hiyerarşik müfredat ağacı ve konu/kazanım eşleyici.

Seviyeler: Ders → Kurul (sistem/blok) → Konu → Kazanım. Kaynaklar salt okunur.
Eşleme sklearn TF-IDF + kosinüs benzerliği ile yapılır (deterministik, CPU).
"""
from __future__ import annotations

import json

from . import config, nlp


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def build() -> dict:
    curriculum = _read_json(config.CURRICULUM) or {}
    taxonomy = _read_json(config.TAXONOMY) or {}

    kurul_ad: dict[int, str] = {}
    kazanim: dict[int, list[str]] = {}
    for code, c in (curriculum.get("committees") or {}).items():
        k = c.get("kurul")
        if isinstance(k, int):
            kurul_ad[k] = c.get("name") or code
            kazanim[k] = [t for t in (c.get("core_topics") or []) if t]

    konular: list[dict] = []
    seen = set()
    for kurul in taxonomy.get("kurullar", []):
        k = kurul.get("kurul")
        if not isinstance(k, int):
            continue
        kurul_ad.setdefault(k, kurul.get("ad") or f"Kurul {k}")
        for kn in kurul.get("konular", []):
            ders = (kn.get("ders") or "").strip()
            konu = (kn.get("konu") or "").strip()
            if not konu:
                continue
            key = (k, ders, konu)
            if key in seen:
                continue
            seen.add(key)
            konular.append({"kurul": k, "ders": ders, "konu": konu,
                            "text": f"{ders} {konu}".strip()})

    tree: dict[str, dict] = {}
    for kn in konular:
        d = tree.setdefault(kn["ders"] or "(belirsiz)", {})
        d.setdefault(kn["kurul"], []).append(kn["konu"])

    data = {"kurul_ad": {str(k): v for k, v in kurul_ad.items()},
            "kazanim": {str(k): v for k, v in kazanim.items()},
            "konular": konular,
            "agac": tree}
    config.TAX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


class Taxonomy:
    def __init__(self, data: dict):
        self.data = data
        self.konular = data.get("konular") or []
        self.kazanim = {int(k): v for k, v in (data.get("kazanim") or {}).items()}
        self.kurul_ad = {int(k): v for k, v in (data.get("kurul_ad") or {}).items()}
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer

        self._np = np
        self._konu_vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
        self._konu_mat = self._konu_vec.fit_transform([k["text"] for k in self.konular]) if self.konular else None
        self._kaz_vec = {}
        self._kaz_mat = {}
        for k, topics in self.kazanim.items():
            v = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
            self._kaz_vec[k] = v
            self._kaz_mat[k] = v.fit_transform(topics) if topics else None

    def match(self, text: str, kurul: int | None = None, min_score: float = 0.18) -> dict:
        out: dict = {}
        if self._konu_mat is None or not self.konular:
            return out
        qv = self._konu_vec.transform([text])
        sims = (self._konu_mat @ qv.T).toarray().ravel()
        if kurul is not None:
            mask = [i for i, k in enumerate(self.konular) if k["kurul"] == kurul]
            if mask:
                best = max(mask, key=lambda i: sims[i])
            else:
                best = int(sims.argmax())
        else:
            best = int(sims.argmax())
        if sims[best] >= min_score:
            kn = self.konular[best]
            out["konu"] = kn["konu"]
            out["ders"] = kn["ders"]
            out["kurul"] = kn["kurul"]
            out["konu_skor"] = round(float(sims[best]), 3)
        # kazanım (kurul bazlı)
        kk = out.get("kurul", kurul)
        if kk in self._kaz_mat and self._kaz_mat[kk] is not None:
            kv = self._kaz_vec[kk].transform([text])
            ks = (self._kaz_mat[kk] @ kv.T).toarray().ravel()
            if ks.size:
                bi = int(ks.argmax())
                if ks[bi] >= min_score:
                    out["kazanim"] = self.kazanim[kk][bi]
                    out["kazanim_skor"] = round(float(ks[bi]), 3)
        return out


    def match_many(self, texts: list[str], min_score: float = 0.18, with_kazanim: bool = False) -> list[dict]:
        """Toplu eşleme (derleme sırasında hızlı): her metin için konu + kazanım."""
        if self._konu_mat is None or not self.konular or not texts:
            return [{} for _ in texts]
        qmat = self._konu_vec.transform(texts)
        sims = (self._konu_mat @ qmat.T).toarray()  # (konu, metin)
        out: list[dict] = []
        for j in range(len(texts)):
            col = sims[:, j]
            bi = int(col.argmax())
            if col[bi] < min_score:
                out.append({})
                continue
            kn = self.konular[bi]
            rec = {"konu": kn["konu"], "ders": kn["ders"], "kurul": kn["kurul"],
                   "konu_skor": round(float(col[bi]), 3)}
            kk = kn["kurul"]
            if with_kazanim and kk in self._kaz_mat and self._kaz_mat[kk] is not None:
                kv = self._kaz_vec[kk].transform([texts[j]])
                ks = (self._kaz_mat[kk] @ kv.T).toarray().ravel()
                if ks.size and ks.max() >= min_score:
                    rec["kazanim"] = self.kazanim[kk][int(ks.argmax())]
                    rec["kazanim_skor"] = round(float(ks.max()), 3)
            out.append(rec)
        return out


def load() -> Taxonomy:
    if config.TAX_PATH.exists():
        data = _read_json(config.TAX_PATH)
    else:
        data = build()
    return Taxonomy(data or {})