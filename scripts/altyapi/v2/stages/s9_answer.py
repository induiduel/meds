"""s9 — Cevap doldurma / soru tamamlama (ücretsiz bulut LLM, kanıt zorunlu).

Kurallar:
  - Zaten cevabı olan sorulara DOKUNMAZ.
  - Varsayılan olarak Faz 14'ün zaten incelediği soruları ATLAR (çakışma/tekrar yok). Birincil hedef
    Faz 14'ün denetlemediği soruları tamamlamaktır.
  - Yalnızca kanıt metni (ders notu parçası) varken çalışır; modelden birebir alıntı ister.
  - Alıntı kanıtta geçmiyorsa veya destek eşiğin altındaysa sonuç KABUL EDİLMEZ (uydurma engeli).
"""
from __future__ import annotations

from ..core import evidence as evmod
from ..core import faz14, llm, match

DEFAULT_MIN_SUPPORT = 0.5
DEFAULT_LIMIT = 40


def _evidence_text(rec: dict, by_chunk: dict[str, str], index) -> str:
    texts = [by_chunk.get(cid, "") for cid in (rec.get("evidence") or [])]
    text = "\n".join(t for t in texts if t)
    if text.strip():
        return text
    if index is not None:
        hits = match.match_question(rec, index, k=3)
        return "\n".join(h["doc"].get("text") or "" for h in hits)
    return ""


def _cited(quote: str, evidence_text: str) -> bool:
    q = evmod.tokens(quote)
    if not q:
        return False
    norm_ev = " ".join(evmod.tokens(evidence_text))
    norm_q = " ".join(q)
    return norm_q in norm_ev


def fill_answers(records: list[dict], *, by_chunk: dict[str, str] | None = None, index=None,
                 limit: int = DEFAULT_LIMIT, min_support: float = DEFAULT_MIN_SUPPORT,
                 skip_faz14: bool = True, skip_ids: set[str] | None = None, log=print) -> dict:
    by_chunk = by_chunk or {}
    skip_ids = skip_ids if skip_ids is not None else set()
    counts = {"denendi": 0, "dolduruldu": 0, "faz14_atlandi": 0, "cevapli_atlandi": 0,
              "kanit_yok": 0, "yanit_yok": 0, "destek_yetersiz": 0, "denenmis_atlandi": 0,
              "_denenen_idler": []}

    for rec in records:
        rid = rec.get("question_id")
        if rec.get("answer"):
            counts["cevapli_atlandi"] += 1
            continue
        if rid in skip_ids:
            counts["denenmis_atlandi"] += 1
            continue
        if skip_faz14 and faz14.is_reviewed(rec):
            counts["faz14_atlandi"] += 1
            continue
        if counts["denendi"] >= limit:
            break
        # Sağlayıcılar tükendiyse (hiç yanıt yok) turu bitir; sorular sonraki tura kalsın.
        if counts["yanit_yok"] >= 5 and counts["dolduruldu"] == 0:
            break

        kanit = _evidence_text(rec, by_chunk, index)
        if not kanit.strip():
            counts["kanit_yok"] += 1
            counts["_denenen_idler"].append(rid)
            continue

        counts["denendi"] += 1
        secenek = "\n".join(f"{k}) {v}" for k, v in (rec.get("options") or {}).items())
        prompt = (
            "Aşağıdaki ders notu parçasına DAYANARAK soruyu çöz. YALNIZCA parçada geçen bilgiyi kullan; "
            "parçada karşılığı yoksa answer alanını null bırak. "
            'JSON döndür: {"answer": "<A-E harfi veya kısa serbest cevap ya da null>", '
            '"explanation": "<kısa gerekçe>", "alinti": "<parçadan birebir alıntı, en az 8 kelime>"}.\n\n'
            f"KANIT:\n{kanit[:1500]}\n\nSORU:\n{rec.get('stem','')}\n{secenek}"
        )
        data = llm.chat_json(prompt, max_tokens=400)
        if not isinstance(data, dict) or not data.get("answer"):
            # Sağlayıcı yanıt vermedi ya da cevap yok: DENENMİŞ sayma, sonraki turda tekrar denenir.
            counts["yanit_yok"] += 1
            continue
        counts["_denenen_idler"].append(rid)

        answer = str(data.get("answer")).strip()
        keys = set((rec.get("options") or {}).keys())
        if keys and answer.upper()[:1] in keys:
            answer = answer.upper()[:1]
        elif keys:
            # serbest cevap şıkka denk gelmiyorsa kabul etme
            counts["destek_yetersiz"] += 1
            continue

        aciklama = str(data.get("explanation") or "")
        alinti = str(data.get("alinti") or "")
        destek = evmod.support_ratio(f"{answer} {aciklama}", [kanit])
        alinti_ok = _cited(alinti, kanit)
        # Kabul: destek yeterli VEYA (orta destek + birebir alıntı). Aksi halde reddedilir (uydurma engeli).
        if not (destek >= min_support or (destek >= 0.35 and alinti_ok)):
            counts["destek_yetersiz"] += 1
            continue

        rec["answer"] = answer
        rec["explanation"] = aciklama
        rec["answer_kaynak"] = {
            "kanal": "llm_free",
            "support_ratio": destek,
            "alinti_dogrulandi": alinti_ok,
            "alinti": alinti[:300],
            "kanit_chunk": (rec.get("evidence") or [None])[0],
        }
        rec["issues"] = [i for i in (rec.get("issues") or []) if not i.startswith("answer_")]
        if rec.get("status") == "needs_fix" and not rec["issues"]:
            rec["status"] = "fixed"
        counts["dolduruldu"] += 1

    return counts
