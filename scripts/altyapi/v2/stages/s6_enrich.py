"""s6 — Zenginleştirme: kanıt kapılı, ücretsiz bulut LLM (GPU yok).

Her türetilmiş alan, KARARIN VERİLDİĞİ AYNI kanıt metniyle ölçülür (`support_ratio`). Destek
eşiğin altındaysa alan `needs_review` olarak işaretlenir; uydurma sessizce kabul edilmez.
LLM yanıt vermezse hiçbir şey yazılmaz (boş sonuç üretilmez).
"""
from __future__ import annotations

from ..core import evidence as evmod
from ..core import llm

DEFAULT_MIN_SUPPORT = 0.5
MAX_PER_RUN = 40


def _evidence_text(rec: dict, by_chunk: dict[str, str]) -> str:
    return "\n".join(by_chunk.get(cid, "") for cid in (rec.get("evidence") or []))


def enrich_records(records: list[dict], *, by_chunk: dict[str, str] | None = None,
                   min_support: float = DEFAULT_MIN_SUPPORT, limit: int = MAX_PER_RUN,
                   log=print) -> dict:
    """Kanıtı olan soruları LLM ile zenginleştirir. Donanım/ücretsiz bulut; istek yoksa atlar."""
    by_chunk = by_chunk or {}
    counts = {"denendi": 0, "zengin": 0, "destek_yetersiz": 0, "yanit_yok": 0}
    for rec in records:
        if not rec.get("evidence"):
            continue
        if counts["denendi"] >= limit:
            break
        kanit = _evidence_text(rec, by_chunk)
        if not kanit.strip():
            continue
        counts["denendi"] += 1
        prompt = (
            "Aşağıdaki ders notu parçasına DAYANARAK soruyu çözümle. Yalnızca parçada geçen bilgiyi kullan. "
            'JSON döndür: {"answer": "<A-E|null>", "options_analysis": {"A": "...", ...}, '
            '"ne_sormus": "...", "alt_konu": "...", "terimler": ["..."]}. '
            "Parçada karşılığı olmayan bilgiyi yazma.\n\n"
            f"KANIT:\n{kanit[:4000]}\n\nSORU:\n{rec.get('stem','')}\n"
            + "\n".join(f"{k}) {v}" for k, v in (rec.get("options") or {}).items())
        )
        data = llm.chat_json(prompt, max_tokens=1500)
        if not isinstance(data, dict):
            counts["yanit_yok"] += 1
            continue
        generated = " ".join([
            str(data.get("ne_sormus") or ""),
            str(data.get("alt_konu") or ""),
            " ".join(str(t) for t in (data.get("terimler") or [])),
            " ".join(str(v) for v in (data.get("options_analysis") or {}).values()),
        ])
        support = evmod.support_ratio(generated, [kanit])
        rec["enrichment"] = {
            "answer": data.get("answer"),
            "options_analysis": data.get("options_analysis") or {},
            "taxonomy_metadata": {
                "ne_sormus": data.get("ne_sormus"),
                "alt_konu": data.get("alt_konu"),
                "terimler": data.get("terimler") or [],
            },
            "support_ratio": support,
            "kaynak": "llm_free",
        }
        if support < min_support:
            rec["enrichment"]["uyari"] = "destek_yetersiz"
            rec.setdefault("issues", []).append("enrichment_unsupported")
            counts["destek_yetersiz"] += 1
        else:
            counts["zengin"] += 1
        if log:
            log(f"  zenginleştirildi {rec.get('question_id')} support={support}")
    return counts
