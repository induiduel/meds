"""İçerik-adresli, deterministik kimlikler.

Aynı içerik → aynı id. Bu sayede tekilleştirme bedava gelir: bir soru/kaynak bir kez girer.
Kimlikler yalnızca içerikten türetilir; sıra/sayaç durumuna bağlı değildir.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Iterable, Mapping

__all__ = ["fold_tr", "norm_key", "source_id", "chunk_id", "question_id", "content_hash"]

# Türkçe katlama: büyük/küçük ve aksan farklarını eşitler (arama ve id için, saklama için değil).
_TR_MAP = str.maketrans({
    "ı": "i", "İ": "i", "I": "i", "i": "i",
    "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g",
    "ö": "o", "Ö": "o", "ş": "s", "Ş": "s",
    "ü": "u", "Ü": "u",
})

_PUNCT = re.compile(r"[^\w\s]+", re.UNICODE)
_WS = re.compile(r"\s+", re.UNICODE)


def fold_tr(text: str) -> str:
    """Türkçe harfleri ASCII karşılıklarına indirir ve küçük harfe çevirir (boşluk/noktalama korunur)."""
    return (text or "").translate(_TR_MAP).casefold()


def norm_key(text: str) -> str:
    """Kimlik/karşılaştırma için agresif normalleştirme: NFC + TR katlama + noktalama sil + boşluk daralt."""
    s = unicodedata.normalize("NFC", text or "")
    s = fold_tr(s)
    s = _PUNCT.sub(" ", s)
    return _WS.sub(" ", s).strip()


def _sha1_hex(payload: str, n: int) -> str:
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:n]


def source_id(drive_id: str) -> str:
    """Kaynak kimliği: sha1(drive_id)[:12] (source.schema.json ile uyumlu)."""
    return _sha1_hex(str(drive_id).strip(), 12)


def chunk_id(source: str, page: int, index: int) -> str:
    """Parça kimliği: '<source_id>:p<page>:c<index>' (chunk.schema.json ile uyumlu)."""
    return f"{source}:p{int(page)}:c{int(index)}"


def question_id(stem: str, options: Mapping[str, str] | Iterable[str] | None = None) -> str:
    """Soru kimliği: normalize edilmiş kök + sıralı şıklar. Cevap/açıklama DAHİL EDİLMEZ
    (cevap sonradan doldurulabilir; id soru içeriğini temsil eder)."""
    parts = [norm_key(stem)]
    if isinstance(options, Mapping):
        for key in sorted(options):
            parts.append(f"{key}:{norm_key(str(options[key]))}")
    elif options:
        for opt in sorted(norm_key(str(o)) for o in options):
            parts.append(opt)
    return _sha1_hex("|".join(parts), 12)


def content_hash(text: str, n: int = 16) -> str:
    """Normalize metnin kısa hash'i (chunk.schema.json 'hash' alanı)."""
    return _sha1_hex(norm_key(text), n)
