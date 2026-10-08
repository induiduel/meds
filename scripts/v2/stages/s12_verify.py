"""s12 — Tıbbi doğruluk denetimi (kanıt desteğiyle).

Cevaplı sorular için `answer + explanation` metninin kanıt (ders notu parçası) tarafından ne kadar
desteklendiğini ölçer ve kayda yazar:
  `tibbi_dogrulama`: {destek, durum: dogrulandi|zayif|kanitsiz, kanit}
Bu, modelin/insanın verdiği cevabın kaynakla çelişip çelişmediğini hızlı taramak içindir.
Uydurma engeli: destek düşükse kayıt `durum=zayif` işaretlenir (silinmez).
"""
from __future__ import annotations

from ..core import evidence as evmod

DOGRULANDI = 0.5
ZAYIF = 0.3


def verify_records(records: list[dict], *, by_chunk: dict[str, str] | None = None) -> dict:
    by_chunk = by_chunk or {}
    counts = {"kayit": 0, "dogrulandi": 0, "zayif": 0, "kanitsiz": 0, "cevapsiz": 0}
    for rec in records:
        counts["kayit"] += 1
        if not rec.get("answer"):
            counts["cevapsiz"] += 1
            continue
        kanit = "\n".join(by_chunk.get(cid, "") for cid in (rec.get("evidence") or []))
        if not kanit.strip():
            rec["tibbi_dogrulama"] = {"durum": "kanitsiz", "destek": 0.0}
            counts["kanitsiz"] += 1
            continue
        destek = evmod.support_ratio(f"{rec.get('answer')} {rec.get('explanation') or ''}", [kanit])
        if destek >= DOGRULANDI:
            durum = "dogrulandi"
        elif destek >= ZAYIF:
            durum = "zayif"
        else:
            durum = "kanitsiz"
        rec["tibbi_dogrulama"] = {"durum": durum, "destek": destek}
        counts[durum if durum in counts else "zayif"] += 1
    return counts
