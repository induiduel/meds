"""Soru kökü kalite kapısı — "bu gerçekten bir soru mu?" (deterministik, AI/GPU yok).

Başlıklar ("KOMPLİKASYONLAR", "## 3. ..."), şık satırları ("Bradikardi"), ders içeriği cümleleri ve
birleşmiş sınav blokları soru DEĞİLDİR. Açık uçlu sorular şık içermek zorunda değildir ama **soru
bağlamı** (soru işareti veya soru kalıbı) taşımalıdır.
"""
from __future__ import annotations

import re

from . import textnorm

__all__ = ["is_question_stem", "MIN_LEN", "MAX_LEN"]

MIN_LEN = 18
MAX_LEN = 400

# Güçlü soru kalıpları (tek başına yeter).
_STRONG = re.compile(
    r"(?i)("
    r"hangisi|hangisidir|hangileri|hangisinde|hangisine|hangisini|hangilerinde|hangileri|"
    r"aşağıdakilerden|aşağıdakilerin|"
    r"\bnedir\b|\bnelerdir\b|\bneden\b|\bnasıl\b|\bniçin\b|\bnerede\b|\bne\s+zaman\b|"
    r"\bkaç\b|\bhangi\b|\bhangi\s|"
    r"değildir|yanlıştır|doğrudur|doğru\s+olan|yanlış\s+olan|hariç|"
    r"tanısı\s+konur|tedavisi\s+ne"
    r")"
)
# Zayıf kalıplar (yalnız büyük harfle başlıyor + yeterince uzunsa ve tek satırsa kabul).
_WEAK = re.compile(
    r"(?i)(en\s+uygun|en\s+sık|en\s+olası|beklenir|beklenmez|görülmez|söylenemez|olamaz|yapılmaz|kullanılmaz)"
)
_HEADER = re.compile(r"(?i)(sınavı|sinavi|cevap\s+anahtar|bütünleme|dönem\s*\d|kurul\s*\d\s*/|üniversite|fakültesi|ders\s+kodu)")
_OPT_IN_STEM = re.compile(r"(?:^|\s)[A-E]\)")
# Birden fazla soru kalıbı → birleşmiş blok (aşağıdakilerden/değildir bu sayıma GİRMEZ)
_MULTI = re.compile(
    r"(?i)(hangisi|hangisidir|hangileri|hangisinde|hangisine|hangisini|\bnedir\b|\bnelerdir\b|\bnasıl\b|\bnasil\b)"
)


def is_question_stem(text: str, *, allow_weak: bool = True) -> bool:
    """Metin gerçek bir soru kökü gibi mi? Başlık/şık/içerik ise False."""
    if not text:
        return False
    t = textnorm.normalize_ws(text)
    if len(t) < MIN_LEN or len(t) > MAX_LEN:
        return False
    # Kök içinde iki+ şık işareti → birleşmiş blok (soru değil)
    if len(_OPT_IN_STEM.findall(t)) >= 2:
        return False
    if _HEADER.search(t):
        return False
    if t.count("?") > 2:
        return False
    # Birleşmiş blok / gürültü göstergeleri
    if "✅" in t or "❑" in t:
        return False
    if t.count("\n") >= 3:
        return False
    if len(_MULTI.findall(t)) >= 2:
        return False
    words = t.split()
    if len(words) < 2:
        return False
    if t.count("?") >= 1 or _STRONG.search(t):
        return True
    if allow_weak and _WEAK.search(t):
        # içerik cümlesi olma riskine karşı: büyük harfle başlasın ve tek satır olsun
        return t[0].isupper() and "\n" not in t
    return False
