#!/usr/bin/env python3
"""Patoloji alternatif soru çözücü — mevcut sorulardan otomatik çözümlü metin üretir.

Girdi : meds_temp/patoloji_ornek26/cozucu/cikti_tam/<kod>.json (örnek + benzer + çıkmış; her açıklama {metin, ses})
Çıktı : meds/data/patoloji_cozucu_alt/metin/<kod>.json  (soru başına metin + ses metni + süre tahmini)
        meds/data/patoloji_cozucu_alt/metin/<kod>.md    (okunur tek dosya)
        meds/data/patoloji_cozucu_alt/metin/tum_sorular.md (bütün dersler)

Kapsam: yalnız `tur` = ornek veya cikmis sorular (benzer sorular dışarıda).
Üslup: kısa, nokta atışı, sesli çözüm gibi; harf adı yalnız seçenek listesinde ve cevap satırında.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
GIRDI = MEDS.parent / "meds_temp/patoloji_ornek26/cozucu/cikti_tam"
CIKTI = MEDS / "data/patoloji_cozucu_alt/metin"
INDEX = MEDS / "src/data/patoloji_cozucu/index.json"
HARF = "ABCDE"
HARF_SES = {"A": "A", "B": "Be", "C": "Ce", "D": "De", "E": "E"}

ACILISLAR = [
    "Şimdi seçeneklere tek tek bakalım.",
    "Seçenekleri sırayla değerlendirelim.",
    "Her seçeneği tek tek ele alalım.",
    "Şıkları sırasıyla gözden geçirelim.",
]


def buyuk(s: str) -> str:
    """Türkçe büyük harf (i → İ)."""
    if not s:
        return s
    ilk = "İ" if s[0] == "i" else s[0].upper()
    return ilk + s[1:]


KALIP = re.compile(r"^(?P<konu>.+?) bu sorunun cevabı değil(dir)?[;,]?\s*", re.I)
BIRIM = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def sayi(n: int) -> str:
    if n == 0:
        return "sıfır"
    if n >= 1000:
        return (sayi(n // 1000) + " bin " + (sayi(n % 1000) if n % 1000 else "")).strip()
    s = ""
    if n >= 100:
        s += BIRIM[n // 100] + " yüz "
        n %= 100
    if n >= 10:
        s += ONLAR[n // 10] + " "
        n %= 10
    return (s + BIRIM[n]).strip()


def rakamsiz(s: str) -> str:
    """Ses metnindeki rakamları yazıyla yaz (31 → otuz bir)."""
    return re.sub(r"\d+", lambda m: sayi(int(m.group())), s)


def eslestir(metin: str, ses: str, sira: int) -> tuple[str, str]:
    """Geçiştirme kalıbını ('bu sorunun cevabı değil;') doğal bir karşılaştırma cümlesine çevir."""
    m, m2 = KALIP.match(metin), KALIP.match(ses)
    if not m and not m2:
        return metin, ses
    konu = (m or m2).group("konu").strip()
    kalan = metin[m.end():].strip() if m else ""
    kalan_ses = ses[m2.end():].strip() if m2 else ""
    kalan = re.sub(r"^[.;:,]\s*", "", kalan)
    kalan_ses = re.sub(r"^[.;:,]\s*", "", kalan_ses)
    if sira % 2 == 0:
        metin = f"{konu} ile karıştırılabilir: {buyuk(kalan)}" if kalan else f"{konu}, bu soruda aranan özelliği taşımaz."
        ses = f"{konu} ile karıştırılabilir. {buyuk(kalan_ses)}" if kalan_ses else f"{konu}, bu soruda aranan özelliği taşımaz."
    else:
        metin = f"{buyuk(kalan)} {konu} bu sorudaki ayrımı sağlamaz." if kalan else f"{konu}, bu soruda aranan özelliği taşımaz."
        ses = f"{buyuk(kalan_ses)} {konu} bu sorudaki ayrımı sağlamaz." if kalan_ses else f"{konu}, bu soruda aranan özelliği taşımaz."
    return metin, rakamsiz(ses)


def temizle(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def soru_metni(q: dict) -> tuple[str, str]:
    """(metin, ses) — başlık + şıklar + açılış + şık açıklamaları + cevap + özet."""
    n = q["no"]
    dogru = q["dogru"]
    acilis = ACILISLAR[n % len(ACILISLAR)]

    parcalar_m: list[str] = [f"**Soru.** {q['soru']}", ""]
    parcalar_m.append(" · ".join(f"**{h})** {q['secenekler'][h]}" for h in HARF))
    parcalar_m += ["", f"**Çözüm.** {acilis}", ""]

    parcalar_s: list[str] = [q["kok_ses"]]
    parcalar_s += [f"{HARF_SES[h]}, {q['secenek_ses'][h]}" for h in HARF]
    parcalar_s.append(acilis)

    aciklamalar: dict[str, str] = {}
    for i, h in enumerate(HARF):
        em, es = eslestir(temizle(q["siklar"][h]["metin"]), temizle(q["siklar"][h]["ses"]), i + n)
        aciklamalar[h] = em
        parcalar_m += [f"- **{q['secenekler'][h]}** — {em}"]
        parcalar_s.append(es)

    parcalar_m += ["", f"**Cevap: {dogru}** — {q['secenekler'][dogru]}", "",
                   f"**Özet.** {q['cozum']['metin']}"]
    parcalar_s += [f"Doğru cevap {HARF_SES[dogru]}, {q['secenek_ses'][dogru]}", q["cozum"]["ses"]]
    return "\n".join(parcalar_m), rakamsiz("\n".join(parcalar_s)), acilis, aciklamalar


def main() -> None:
    CIKTI.mkdir(parents=True, exist_ok=True)
    basliklar = {d["kod"]: d["baslik"] for d in json.loads(INDEX.read_text(encoding="utf-8"))["dersler"]}
    tum_md: list[str] = ["# Patoloji — Alternatif Sesli Soru Çözücü", ""]
    ozet = []
    for p in sorted(GIRDI.glob("*.json")):
        kod = p.stem
        d = json.loads(p.read_text(encoding="utf-8"))
        sorular = []
        for q in d["sorular"]:
            if q.get("tur") not in ("ornek", "cikmis"):
                continue
            metin, ses, acilis, aciklamalar = soru_metni(q)
            sorular.append({
                "no": q["no"], "tur": q["tur"], "soru": q["soru"],
                "secenekler": q["secenekler"], "dogru": q["dogru"],
                "giris": acilis, "aciklamalar": aciklamalar, "ozet": q["cozum"]["metin"],
                "metin": metin, "ses": ses, "kelime": len(metin.split()),
            })
        if not sorular:
            continue
        baslik = basliklar.get(kod, kod)
        cikti = {"kod": kod, "baslik": baslik, "surum": "alt-1", "sorular": sorular}
        (CIKTI / f"{kod}.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1), encoding="utf-8")

        md = [f"# {kod} · {baslik}", "", f"_{len(sorular)} soru (örnek + çıkmış)_", ""]
        for s in sorular:
            md += [f"## Soru {s['no']}", "", s["metin"], ""]
        (CIKTI / f"{kod}.md").write_text("\n".join(md), encoding="utf-8")
        tum_md += md
        ozet.append((kod, baslik, len(sorular), sum(x["kelime"] for x in sorular)))
        print(f"{kod}: {len(sorular)} soru")

    (CIKTI / "tum_sorular.md").write_text("\n".join(tum_md), encoding="utf-8")
    print(f"TOPLAM {sum(o[2] for o in ozet)} soru, {sum(o[3] for o in ozet)} kelime")


if __name__ == "__main__":
    main()
