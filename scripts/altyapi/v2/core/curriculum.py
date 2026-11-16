"""Müfredat / kazanım eşleme.

Her soruyu **Ders → Konu → Kazanım** zincirine bağlar ve ilgili tıbbi terimleri çıkarır.
Kaynaklar salt okunurdur: `taxonomy/donem3_ders_programi.json` (kurul→ders→konu) ve
`curriculum/kbu_tip_donem3_curriculum.json` (komite çekirdek konuları = kazanım).
"""
from __future__ import annotations

from functools import lru_cache

from .. import config
from . import ids, match, store

MIN_TERM_LEN = 4
MAX_TERMS = 12
# Konu/kazanım atamak için asgari BM25 skoru (düşükse boş bırakılır → yanlış eşleme yerine None).
MIN_KONU_SKOR = 5.0
MIN_KONU_SKOR_DERS = 2.5  # ders uyumluysa daha düşük eşik
MIN_KAZANIM_SKOR = 4.0

# Ders adı normalizasyonu (yol/farklı yazımlar → resmi ders adı)
_DERS_ALIAS = {
    "patoloji": "Tıbbi Patoloji",
    "tıbbi patoloji": "Tıbbi Patoloji",
    "enfeksiyon": "Enfeksiyon Hastalıkları",
    "enfeksiyon hastalıkları": "Enfeksiyon Hastalıkları",
    "farmakoloji": "Tıbbi Farmakoloji",
    "tıbbi farmakoloji": "Tıbbi Farmakoloji",
    "dahiliye": "İç Hastalıkları",
    "iç hastalıkları": "İç Hastalıkları",
    "çocuk hastalıkları": "Çocuk Sağlığı ve Hastalıkları",
    "çocuk sağlığı": "Çocuk Sağlığı ve Hastalıkları",
    "kadın doğum": "Kadın Hastalıkları ve Doğum",
    "kadın hastalıkları": "Kadın Hastalıkları ve Doğum",
    "genetik": "Tıbbi Genetik",
    "tıbbi genetik": "Tıbbi Genetik",
    "kvc": "Kalp ve Damar Cerrahisi",
    "beyin cerrahisi": "Beyin ve Sinir Cerrahisi",
    "ftr": "Fiziksel Tıp ve Rehabilitasyon",
}


def normalize_ders(ders: str | None) -> str | None:
    key = ids.fold_tr((ders or "").strip())
    return _DERS_ALIAS.get(key, ders)


class Curriculum:
    def __init__(self, taxonomy: dict, curriculum: dict):
        self.konu: dict[int, list[dict]] = {}
        self.kazanim: dict[int, list[dict]] = {}
        self.dersler: dict[int, list[str]] = {}
        self.lexicon: set[str] = set()

        for kurul in taxonomy.get("kurullar", []):
            k = kurul.get("kurul")
            if not isinstance(k, int):
                continue
            seen = set()
            konular = []
            for kn in kurul.get("konular", []):
                ders = (kn.get("ders") or "").strip()
                konu = (kn.get("konu") or "").strip()
                if not konu:
                    continue
                key = (ders, konu)
                if key in seen:
                    continue
                seen.add(key)
                konular.append({"ders": ders, "konu": konu, "text": f"{ders} {konu}".strip()})
            self.konu[k] = konular
            self.dersler[k] = sorted({kn.get("ders") for kn in kurul.get("konular", []) if kn.get("ders")})

        for code, c in (curriculum.get("committees") or {}).items():
            k = c.get("kurul")
            if not isinstance(k, int):
                continue
            topics = [t for t in (c.get("core_topics") or []) if t]
            self.kazanim[k] = [{"kazanim": t, "text": t} for t in topics]
            self.lexicon.update(t for t in ids.norm_key(" ".join(topics)).split() if len(t) >= MIN_TERM_LEN)

        for konular in self.konu.values():
            for kn in konular:
                self.lexicon.update(
                    t for t in ids.norm_key(kn["text"]).split() if len(t) >= MIN_TERM_LEN
                )
        for dersler in self.dersler.values():
            for d in dersler:
                self.lexicon.update(t for t in ids.norm_key(d).split() if len(t) >= MIN_TERM_LEN)

        self._konu_idx = {k: match.Bm25Index(v) for k, v in self.konu.items() if v}
        self._kazanim_idx = {k: match.Bm25Index(v) for k, v in self.kazanim.items() if v}

    def _terms(self, text: str) -> list[str]:
        out: list[str] = []
        for tok in ids.norm_key(text).split():
            if len(tok) >= MIN_TERM_LEN and tok in self.lexicon and tok not in out:
                out.append(tok)
        return out[:MAX_TERMS]

    @staticmethod
    def _tier(skor: float) -> str:
        if skor >= 6:
            return "yuksek"
        if skor >= 2.5:
            return "orta"
        return "dusuk"

    def map(self, rec: dict) -> dict:
        options = rec.get("options") or {}
        query = " ".join([rec.get("stem") or "", *(str(v) for v in options.values())]) \
            if isinstance(options, dict) else (rec.get("stem") or "")
        if not query.strip():
            return {}

        qkurul = rec.get("kurul")
        qders = (rec.get("ders") or "").strip()
        qfold = ids.fold_tr(qders) if qders else None

        # Bilinen ders varsa, yalnız o dersi veren kurulları aday al (isabeti belirgin artırır).
        kuruls: list[int] = []
        if qfold:
            for k, dersler in self.dersler.items():
                if any(qfold in ids.fold_tr(d) or ids.fold_tr(d) in qfold for d in dersler):
                    kuruls.append(k)
        if not kuruls:
            kuruls = [qkurul] if isinstance(qkurul, int) and qkurul in self.konu else list(self.konu)

        best = None
        for k in kuruls:
            idx = self._konu_idx.get(k)
            if not idx:
                continue
            for hit in idx.search(query, k=5):
                doc = hit["doc"]
                skor = hit["skor"]
                if qfold:
                    dfold = ids.fold_tr(doc.get("ders") or "")
                    skor *= 1.15 if (qfold in dfold or dfold in qfold) else 0.6
                if best is None or skor > best["skor"]:
                    best = {"kurul": k, "ders": doc["ders"], "konu": doc["konu"], "skor": skor}

        if not best:
            return {"terimler": self._terms(query)}

        kazanim = None
        kskor = 0.0
        kidx = self._kazanim_idx.get(best["kurul"])
        if kidx:
            kh = kidx.search(query, k=1)
            if kh:
                kazanim = kh[0]["doc"]["kazanim"]
                kskor = kh[0]["skor"]

        ders = normalize_ders(best["ders"])
        dfold = ids.fold_tr(ders or "")
        ders_uyum = bool(qfold) and (qfold in dfold or dfold in qfold)
        # Düşük güvende konu/kazanım ATAMA (yanlış eşleme yerine boş bırak).
        konu = best["konu"] if (best["skor"] >= MIN_KONU_SKOR or
                                 (ders_uyum and best["skor"] >= MIN_KONU_SKOR_DERS)) else None
        kaz = kazanim if kskor >= MIN_KAZANIM_SKOR else None

        return {
            "kurul": best["kurul"],
            "ders": ders or None,
            "konu": konu,
            "kazanim": kaz,
            "skor": round(best["skor"], 3),
            "kazanim_skor": round(kskor, 3),
            "guven": self._tier(best["skor"]),
            "terimler": self._terms(query),
        }


@lru_cache(maxsize=1)
def load() -> Curriculum | None:
    taxonomy = store.read_json(config.TAXONOMY_PATH, None)
    curriculum = store.read_json(config.CURRICULUM_PATH, None)
    if not taxonomy or not curriculum:
        return None
    return Curriculum(taxonomy, curriculum)


def map_question(rec: dict) -> dict:
    cur = load()
    return cur.map(rec) if cur else {}
