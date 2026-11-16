"""Metin normalizasyonu ve onarımı — CPU-only, deterministik, ücretsiz.

Amaç: OCR/indirme kaynaklı bozulmaları (mojibake, ligatür, kontrol karakteri) onarmak ve
karşılaştırma için Türkçe katlama sağlamak. Türkçe karakterler KORUNUR; yalnızca bozuk olan
düzeltilir. Tehlikeli değişiklikler (ör. rakam→harf) `aggressive=True` ile isteğe bağlıdır.
"""
from __future__ import annotations

import re
import unicodedata

try:  # ftfy varsa mojibake onarımında kullanılır (karma metinlerde daha güvenilir)
    import ftfy as _ftfy  # type: ignore
except Exception:  # noqa: BLE001
    _ftfy = None

from .ids import fold_tr as _fold_tr

__all__ = [
    "nfc", "looks_mojibake", "fix_mojibake", "fix_ligatures", "strip_control", "normalize_ws",
    "fix_hyphen_breaks", "repair_ocr", "clean_text", "fold_tr", "has_broken_turkish",
]

# Mojibake göstergeleri: UTF-8 baytlarının Latin-1/CP1252 olarak okunmasıyla oluşan diziler.
_MOJI_TOKENS = ("Ã", "Ä", "Å", "â€", "Â", "â", "ð", "þ")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")
_MULTI_WS = re.compile(r"[ \t\u00a0\u2007\u202f]+")
_MULTI_NL = re.compile(r"\n{3,}")
_HYPHEN_BREAK = re.compile(r"([^\W\d_])\s*-\s*\n\s*([^\W\d_])", re.UNICODE)
_DIGIT_IN_WORD_0 = re.compile(r"(?<=[^\W\d_])0(?=[^\W\d_])", re.UNICODE)
_DIGIT_IN_WORD_1 = re.compile(r"(?<=[^\W\d_])1(?=[^\W\d_])", re.UNICODE)
_DIGIT_IN_WORD_5 = re.compile(r"(?<=[^\W\d_])5(?=[^\W\d_])", re.UNICODE)
# Eski PowerPoint/OCR bozulması: kelime ortasındaki '!' aslında 'i'dir ("Kals!ton!n" -> "Kalsitonin").
_BANG_IN_WORD = re.compile(r"(?<=[^\W\d_])!(?=[^\W\d_])", re.UNICODE)
# Kelime SONUNDAKİ '!' de genelde 'i'dir ("Hangis!" -> "Hangisi"). Ünlem olan kısa istisnalar korunur.
_BANG_END = re.compile(r"([^\W\d_]+)!(?=\s|$|[.,;:)\]])", re.UNICODE)
_BANG_KEEP = {"dikkat", "uyarı", "uyari", "not", "önemli", "onemli", "aman", "yasak", "tamam"}

_LIGATURES = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
    "\ufb05": "ft", "\ufb06": "st", "\u2013": "-", "\u2014": "-", "\u2018": "'",
    "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2026": "...",
}


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def _moji_score(text: str) -> int:
    return sum(text.count(tok) for tok in _MOJI_TOKENS)


def looks_mojibake(text: str) -> bool:
    if not text:
        return False
    if "Ã" in text or "Ä±" in text or "ÅŸ" in text or "\ufffd" in text:
        return True
    return _moji_score(text) >= 3


def fix_mojibake(text: str) -> str:
    """UTF-8 ↔ Latin-1/CP1252 çift okuma bozulmasını onarır; emin değilse dokunmaz."""
    if not text or not looks_mojibake(text):
        return text
    if _ftfy is not None:
        try:
            fixed = _ftfy.fix_text(text)
            if _moji_score(fixed) < _moji_score(text):
                return fixed
        except Exception:  # noqa: BLE001
            pass
    for enc in ("latin-1", "cp1252"):
        try:
            cand = text.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if _moji_score(cand) < _moji_score(text):
            return cand
    return text


def fix_ligatures(text: str) -> str:
    if not text:
        return text
    for src, dst in _LIGATURES.items():
        if src in text:
            text = text.replace(src, dst)
    return text


def strip_control(text: str) -> str:
    if not text:
        return text
    text = _ZERO_WIDTH.sub("", text)
    return _CONTROL.sub("", text)


def normalize_ws(text: str) -> str:
    if not text:
        return text
    text = _MULTI_WS.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return _MULTI_NL.sub("\n\n", text).strip()


def fix_hyphen_breaks(text: str) -> str:
    """Satır sonunda tire ile bölünmüş kelimeleri birleştirir: 'Send-\\nromu' → 'Sendromu'."""
    if not text or "-" not in text:
        return text
    prev = None
    while prev != text:
        prev = text
        text = _HYPHEN_BREAK.sub(r"\1\2", text)
    return text


def repair_ocr(text: str, aggressive: bool = False) -> str:
    """Kelime içine sıkışmış rakamları/işaretleri harfe çevirir.
    Varsayılan: 0→o ve kelime ortası '!'→'i' (yüksek güven). `aggressive` ile 1→l ve 5→s."""
    if not text:
        return text
    text = _DIGIT_IN_WORD_0.sub("o", text)
    text = _BANG_IN_WORD.sub("i", text)
    text = _BANG_END.sub(lambda m: m.group(1) + ("!" if m.group(1).casefold() in _BANG_KEEP else "i"), text)
    if aggressive:
        text = _DIGIT_IN_WORD_1.sub("l", text)
        text = _DIGIT_IN_WORD_5.sub("s", text)
    return text


def clean_text(text: str, *, aggressive_ocr: bool = False) -> str:
    """Standart temizlik zinciri. Türkçe karakterleri korur; yalnız bozukluğu onarır."""
    text = nfc(text)
    text = fix_ligatures(text)
    text = fix_mojibake(text)
    text = strip_control(text)
    text = fix_hyphen_breaks(text)
    text = repair_ocr(text, aggressive=aggressive_ocr)
    return normalize_ws(text)


def fold_tr(text: str) -> str:
    """Arama/karşılaştırma için Türkçe katlama (ids ile aynı kural)."""
    return _fold_tr(text)


def has_broken_turkish(text: str) -> bool:
    """Bozuk görünen Türkçe işaretleri (mojibake veya değiştirme karakteri) var mı?"""
    return looks_mojibake(text) or "\ufffd" in (text or "")
