"""NLP yardımcıları — Türkçe/İngilizce, deterministik, ücretsiz, GPU yok.

İçerir: normalizasyon, tokenizasyon, stop-word temizleme, hafif Türkçe kök bulma (ek soyma),
n-gram, BoW, TF-IDF, cümle bölme ve (varsa spaCy ile, yoksa kural tabanlı) öbek/bağımlılık analizi.
"""
from __future__ import annotations

import re
import unicodedata

try:
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401
except Exception:  # noqa: BLE001
    TfidfVectorizer = None

_SPACY = None


def _spacy():
    global _SPACY
    if _SPACY is not None:
        return _SPACY
    try:
        import spacy

        for name in ("tr_core_news_md", "tr_core_news_sm"):
            try:
                _SPACY = spacy.load(name)
                return _SPACY
            except Exception:  # noqa: BLE001
                continue
        _SPACY = spacy.blank("tr")  # model yok → boş boru hattı
    except Exception:  # noqa: BLE001
        _SPACY = False
    return _SPACY


_TR_MAP = str.maketrans({"ı": "i", "İ": "i", "I": "i", "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g",
                         "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u"})

STOPWORDS = set("""ve veya ile için ise ancak ama fakat bir bu şu o da de mi ki ne çok en gibi olarak olan
göre daha her hangi hangisi hangisidir hangileri aşağıdakilerden aşağıdaki aşağıda verilen seçeneklerden
değildir yanlıştır doğru yanlış hangisine hangisinde hangisini olduğuna üzere ise den dan ten tan nin nın nur
the and or of to in a an is are which what how why when where who those these this that not following
""".split())


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def fold(text: str) -> str:
    return nfc(text).translate(_TR_MAP).casefold()


def normalize(text: str) -> str:
    t = nfc(text)
    t = re.sub(r"[\u200b-\u200f\ufeff]", "", t)
    t = re.sub(r"[ \t\u00a0]+", " ", t)
    t = re.sub(r"\n{2,}", "\n", t)
    return t.strip()


_WORD = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşü0-9%]+", re.UNICODE)


def tokens(text: str, *, keep_stop: bool = False) -> list[str]:
    toks = [fold(w) for w in _WORD.findall(normalize(text))]
    if keep_stop:
        return toks
    return [t for t in toks if t not in STOPWORDS and len(t) > 1]


# Hafif Türkçe kök bulma: yaygın ekleri soyar (tam Porter değil; NLTK yok).
_TR_SUFFIXES = ("lar", "ler", "dan", "den", "tan", "ten", "nin", "nın", "dir", "dır", "dur", "dür",
                "da", "de", "ta", "te", "si", "sı", "su", "sü", "in", "ın", "un", "ün", "im", "ım",
                "la", "le", "ca", "ce", "i", "ı", "u", "ü")


def stem_tr(word: str) -> str:
    w = fold(word)
    for suf in _TR_SUFFIXES:
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def stems(text: str) -> list[str]:
    return [stem_tr(t) for t in tokens(text)]


def ngrams(text: str, n: int = 2) -> list[str]:
    toks = tokens(text)
    return [" ".join(toks[i:i + n]) for i in range(max(0, len(toks) - n + 1))]


def bow(text: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for t in tokens(text):
        out[t] = out.get(t, 0) + 1
    return out


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", normalize(text))
    return [p.strip() for p in parts if p.strip()]


def parse(text: str) -> list[dict]:
    """Öbek/bağımlılık analizi: spaCy varsa gerçek, yoksa kural tabanlı (isim öbeği) çıkarımı."""
    nlp = _spacy()
    if nlp and nlp is not False and nlp.pipe_names:
        doc = nlp(normalize(text)[:2000])
        return [{"text": t.text, "pos": t.pos_, "dep": t.dep_, "head": t.head.text} for t in doc]
    # Kural tabanlı: ardışık isim benzeri kelimeleri öbek say
    phrases = []
    for sent in sentences(text):
        words = _WORD.findall(sent)
        phrases.append({"cümle": sent, "sözcük_sayısı": len(words),
                        "öbek": " ".join(words[:6]) if words else ""})
    return phrases


def tfidf_matrix(docs: list[str]):
    if TfidfVectorizer is None:
        return None, None
    vec = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    mat = vec.fit_transform(docs)
    return vec, mat
