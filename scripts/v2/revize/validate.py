"""Revize v2 — kural doğrulama ve değişiklik kaydı.

INSTRUCTIONS.md §1 kurallarını uygular. Sonuç: {ok, karantina, issues[], degisiklikler[]}.
"""
from __future__ import annotations

import re

from ..core import quality, textnorm
from . import config

_NEG = re.compile(r"(?i)(yanlıştır|değildir|hariç|olmayan|hangisi\s+yanlış|yanlıştır\?)")
_ROMAN = re.compile(r"(?m)^\s*(I{1,3}|IV|V|VI{1,3}|IX|X)\s*[\.\)\-]")
# Kanıta/kaynağa atıf veya dolaylı-anlatıcı üslup (kök ve açıklamada YASAK).
_META = re.compile(
    r"(?i)(kaynakta|kaynak\s*:|\[kaynak|slaytta|slayt\s|ders\s*notu|ders\s*notunda|"
    r"kanıtta|kanıt[ıi]nda|kanıtlar|metinde|alıntı|"
    r"belirtilmektedir\s+ki|ifade\s+edilmektedir|iddia\s+etmektedir|"
    r"yanlış\s+ifade|doğru\s+ifade\s+olarak|soru\s+\.\.\.\s+demektedir)"
)


def sanitize_aciklama(text: str) -> tuple[str, bool]:
    """Açıklamadan [Kaynak: ...] alıntılarını ve atıf/meta içeren cümleleri temizler."""
    if not text:
        return text, False
    raw = text
    t = re.sub(r"\[kaynak[^\]]*\]", "", text, flags=re.I)
    t = re.sub(r"(?i)kaynak\s*:\s*[^\s,;]+", "", t)
    parts = re.split(r"(?<=[.!?])\s+", t)
    kept = [p.strip() for p in parts if p.strip() and not _META.search(p)]
    cleaned = " ".join(kept).strip()
    return cleaned, (cleaned != raw.strip())


def _negatif(text: str) -> bool:
    return bool(_NEG.search(text or ""))


def _opt_map(raw) -> dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    out = {}
    for k, v in raw.items():
        k = str(k).strip().upper()[:1]
        if k and isinstance(v, str) and v.strip():
            out[k] = textnorm.clean_text(v)
    return out


def diff_changes(source: dict, revised: dict) -> list[dict]:
    """Kaynaktan revizeye alan farkları (model beyanıyla birleştirilir)."""
    changes = []
    # kurul_adi farkı KAYDEDİLMEZ (TIP310 ↔ 1 ↔ Kurul 1 aynı anlamdadır).
    for field in ("soru_koku", "aciklama", "dogru_secenek", "ders_adi", "konu_adi", "kazanim"):
        old = source.get(field)
        new = revised.get(field)
        if (old or "") != (new or ""):
            changes.append({"alan": field, "eski": old, "yeni": new, "neden": "kural-temelli düzeltme"})
    old_opts, new_opts = source.get("secenekler") or {}, revised.get("secenekler") or {}
    if old_opts != new_opts:
        changes.append({"alan": "secenekler", "eski": old_opts, "yeni": new_opts, "neden": "şık düzeltme/tamamlama"})
    return changes


def validate(revised: dict, source: dict, *, support_ratio: float) -> dict:
    issues: list[str] = []
    karantina = False

    if revised.get("soru_degil"):
        return {"ok": False, "karantina": True, "issues": ["soru_degil"], "degisiklikler": []}
    if revised.get("karantina"):
        return {"ok": False, "karantina": True, "issues": [revised.get("neden") or "model_karantina"], "degisiklikler": []}

    stem = (revised.get("soru_koku") or "").strip()
    if not stem:
        issues.append("soru_koku_yok")
    elif len(stem) < config.MIN_STEM_LEN:
        issues.append("soru_koku_kisa")
    elif not quality.is_question_stem(stem):
        issues.append("soru_koku_gecersiz")
    elif _META.search(stem):
        issues.append("soru_meta")  # kök, kaynağa atıf/anlatı içeriyor → format bozuk

    if _META.search(revised.get("aciklama") or ""):
        issues.append("aciklama_meta")

    opts = _opt_map(revised.get("secenekler"))
    if len(opts) not in (4, 5):
        issues.append(f"sik_sayisi_{len(opts)}")
    if len(opts) < 2:
        karantina = True
    texts = list(opts.values())
    if len(set(t.lower() for t in texts)) < len(texts):
        issues.append("tekrarlanan_sik")
    for k, v in opts.items():
        if len(v) > config.MAX_OPTION_LEN:
            issues.append(f"uzun_sik:{k}")
        if len(v) < 2:
            issues.append(f"bos_sik:{k}")

    answer = (revised.get("dogru_secenek") or "").upper()[:1]
    belirsiz = bool(revised.get("belirsiz"))
    if not belirsiz and answer:
        if answer not in opts:
            issues.append("cevap_sikta_yok")
    elif not belirsiz and not answer:
        issues.append("cevap_belirsiz")

    # yön korunmalı
    if _negatif(source.get("soru_koku") or "") != _negatif(stem):
        issues.append("yon_degisti")

    # öncül tutarlılığı
    oncul = revised.get("oncul") or []
    if isinstance(oncul, list) and len(oncul) >= 2:
        if any(re.match(r"(?i)^(yalnız|hepsi|hiçbiri|tümü)", t or "") for t in opts.values()):
            pass  # öncül temsili şıklar beklenir
    elif _ROMAN.search(source.get("soru_koku") or "") and not oncul:
        issues.append("oncul_eksik")

    if support_ratio < config.SUPPORT_MIN:
        issues.append("kanit_zayif")

    blocking = {"soru_koku_yok", "soru_koku_gecersiz", "soru_meta", "cevap_sikta_yok", "yon_degisti"}
    karantina = karantina or any(i in blocking for i in issues)

    changes = diff_changes(source, revised)
    # modelin beyan ettiği değişiklikleri ekle (alan bazında, mükerrer değilse)
    for ch in (revised.get("degisiklikler") or []):
        if isinstance(ch, dict) and ch.get("alan") and not any(c["alan"] == ch.get("alan") for c in changes):
            changes.append(ch)

    return {"ok": not karantina and not issues, "karantina": karantina, "issues": issues, "degisiklikler": changes}
