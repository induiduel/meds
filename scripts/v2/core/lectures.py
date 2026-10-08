"""Ders notu korpusu + hızlı kanıt araması (CPU, AI yok).

`notes/*.jsonl` içindeki **yalnız ders materyali** (source.doc_type == lecture_slide) parçalarını
yükler; sınav dökümleri (past_question) kanıt sayılmaz. Türkçe katlama + 5 harflik kök ile ters
indeks kurar; terim geçişi ve metin desteği (support) bu indeks üzerinden ölçülür.

`core/evidence.support_ratio` tam kelime eşler; Türkçe ekler ("trombüsün" ↔ "trombüs") yüzünden
düşük çıkar. Buradaki `support` kök eşlemesi kullanır.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

from .. import config
from . import ids

__all__ = ["stems", "LectureCorpus"]

_WORD = re.compile(r"[^\W_]+", re.UNICODE)
_STOP = {
    "ve", "ile", "icin", "bir", "bu", "su", "da", "de", "mi", "ki", "ne", "cok", "en", "gibi",
    "olarak", "olan", "veya", "ya", "ancak", "ama", "fakat", "ise", "her", "daha", "hangisi",
    "hangisidir", "degildir", "asagidakilerden", "asagida", "olur", "olup", "eden", "edilen",
    "yapan", "ile", "kadar", "sonra", "once", "gore", "dir", "dur", "tir", "tur", "bunlar",
    "icinde", "uzerinde", "tarafindan", "sik", "siklikla", "genellikle", "neden", "nedir",
    "the", "and", "of", "in", "to", "is", "for", "with",
}
_STEM = 5


def stems(text: str) -> list[str]:
    """Katlanmış metnin içerik köklerini (en çok 5 harf) sırasıyla döndürür."""
    out = []
    for w in _WORD.findall(ids.fold_tr(text or "")):
        if len(w) < 2 or w in _STOP or w.isdigit():
            continue
        out.append(w[:_STEM])
    return out


def _head(word: str) -> str:
    """Ek almış biçimleri yakalamak için kelime gövdesi: sertleşen son ünsüz (p/ç/t/k) düşer
    ("böbrek" → "böbre" + "ği"); gerisi tam kalır ki "trombüs" "trombosit"e eşlenmesin."""
    return word[:-1] if len(word) > 4 and word[-1] in "pctk" else word


class LectureCorpus:
    def __init__(self, notes_dir: Path | None = None, sources_dir: Path | None = None):
        notes_dir = notes_dir or config.NOTES_DIR
        # Not parçaları eski depodaki kaynak kimliklerini taşır (s10 oradan alır); CORE kaynakları da eklenir.
        dirs = [sources_dir] if sources_dir else [config.DATABASE_DIR / "sources", config.SOURCES_DIR]
        self.sources: dict[str, dict] = {}
        for f in (p for d in dirs for p in d.glob("*.json")):
            try:
                s = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            self.sources.setdefault(s.get("source_id") or f.stem, s)
        self.chunks: list[dict] = []
        for f in sorted(notes_dir.glob("*.jsonl")):
            src = self.sources.get(f.stem)
            if not src or src.get("doc_type") != "lecture_slide":
                continue
            with open(f, encoding="utf-8") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    text = (rec.get("metin") or "").strip()
                    if len(text) < 30:
                        continue
                    self.chunks.append({
                        "chunk_id": rec.get("chunk_id"), "source_id": rec.get("source_id"),
                        "sayfa": rec.get("sayfa"), "text": text,
                    })
        self._toks: list[list[str]] = []
        self._sets: list[set[str]] = []
        self._post: dict[str, list[int]] = {}
        for i, ch in enumerate(self.chunks):
            toks = stems(ch["text"])
            self._toks.append(toks)
            st = set(toks)
            self._sets.append(st)
            for t in st:
                self._post.setdefault(t, []).append(i)
        self._n = len(self.chunks)
        self._avg = (sum(len(t) for t in self._toks) / self._n) if self._n else 1.0
        self._folded: dict[int, str] = {}

    # -- yardımcılar ---------------------------------------------------------------------------
    def folded(self, i: int) -> str:
        f = self._folded.get(i)
        if f is None:
            f = " " + " ".join(_WORD.findall(ids.fold_tr(self.chunks[i]["text"]))) + " "
            self._folded[i] = f
        return f

    def ref(self, i: int, quote: str | None = None) -> dict:
        ch = self.chunks[i]
        src = self.sources.get(ch["source_id"]) or {}
        out = {
            "chunk_id": ch["chunk_id"], "kaynak": src.get("name"), "ders": src.get("ders"),
            "kurul": src.get("kurul"), "sayfa": ch["sayfa"],
        }
        if quote:
            out["alinti"] = quote
        return out

    def idf(self, tok: str) -> float:
        df = len(self._post.get(tok, ()))
        return math.log(1 + (self._n - df + 0.5) / (df + 0.5))

    # -- arama ---------------------------------------------------------------------------------
    def search(self, query: str, k: int = 5, within: list[int] | None = None) -> list[tuple[int, float]]:
        """BM25 (ters indeks). `within` verilirse yalnız o parçalar arasında sıralar."""
        q = set(stems(query))
        if not q:
            return []
        scores: dict[int, float] = {}
        allowed = set(within) if within is not None else None
        k1, b = 1.5, 0.75
        for t in q:
            post = self._post.get(t)
            if not post:
                continue
            idf = self.idf(t)
            for i in post:
                if allowed is not None and i not in allowed:
                    continue
                tf = self._toks[i].count(t)
                ln = len(self._toks[i]) or 1
                scores[i] = scores.get(i, 0.0) + idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * ln / self._avg))
        return sorted(scores.items(), key=lambda x: -x[1])[:k]

    def phrase_hits(self, phrase: str, limit: int = 400) -> list[int]:
        """Terimin (katlanmış, kelime sınırlı) geçtiği parçalar. Son kelimeye ek serbest
        ("trombüs" → "trombüsün" de sayılır); kısa (<=3) kısaltmalarda tam kelime aranır."""
        words = _WORD.findall(ids.fold_tr(phrase or ""))
        if not words:
            return []
        cand = None
        for w in words:
            if len(w) < 2:
                continue
            post = set(self._post.get(w[:_STEM], ()))
            cand = post if cand is None else cand & post
            if not cand:
                return []
        if not cand:
            return []
        if len(words) == 1 and len(words[0]) <= 3:
            pat = re.compile(r" " + re.escape(words[0]) + r" ")
        else:
            pat = re.compile(r" " + r" ".join(re.escape(_head(w)) + r"\w*" for w in words))
        out = [i for i in sorted(cand) if pat.search(self.folded(i))]
        return out[:limit]

    def snippet(self, i: int, phrase: str, width: int = 420) -> str:
        """Parçada terimin geçtiği yerin çevresinden okunur bir pencere."""
        text = self.chunks[i]["text"]
        ft = ids.fold_tr(text)
        words = _WORD.findall(ids.fold_tr(phrase or ""))
        m = re.search(r"\b" + r"\W+".join(re.escape(_head(w)) + r"\w*" for w in words), ft) if words else None
        pos = m.start() if m else -1
        if pos < 0:
            return re.sub(r"\s+", " ", text[:width]).strip()
        start = max(0, pos - width // 3)
        return re.sub(r"\s+", " ", text[start:start + width]).strip()

    def support(self, text: str, chunk_ids: list[int]) -> float:
        """`text` içerik köklerinin verilen parçalarda geçme oranı (idf ağırlıklı, 0..1)."""
        toks = set(stems(text))
        if not toks:
            return 1.0
        ev: set[str] = set()
        for i in chunk_ids:
            ev |= self._sets[i]
        if not ev:
            return 0.0
        tot = sum(self.idf(t) for t in toks)
        hit = sum(self.idf(t) for t in toks if t in ev)
        return round(hit / tot, 3) if tot else 0.0
