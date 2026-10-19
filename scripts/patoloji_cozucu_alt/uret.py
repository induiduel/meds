#!/usr/bin/env python3
"""Patoloji alternatif soru çözücü — mevcut sorulardan otomatik çözümlü metin üretir.

Girdi : meds_temp/patoloji_ornek26/cozucu/cikti_tam/<kod>.json (örnek + benzer + çıkmış; her açıklama {metin, ses})
        meds/data/patoloji_cozucu_alt/duzeltmeler.json         (tıbbi ve üslup düzeltmeleri)
        meds/src/data/patoloji_cozucu/<kod>.json               (zorluk, sinav, sayfa, ipucu meta verisi)
Çıktı : meds/data/patoloji_cozucu_alt/metin/<kod>.json  (soru başına metin + ses metni + meta veri)
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
STD_COZUCU = MEDS / "src/data/patoloji_cozucu"
DUZELTME_P = MEDS / "data/patoloji_cozucu_alt/duzeltmeler.json"
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
        s += ("yüz " if n // 100 == 1 else BIRIM[n // 100] + " yüz ")
        n %= 100
    if n >= 10:
        s += ONLAR[n // 10] + " "
        n %= 10
    return (s + BIRIM[n]).strip()


def rakamsiz(s: str) -> str:
    """Ses metnindeki rakamları yazıyla yaz (31 → otuz bir)."""
    return re.sub(r"\d+", lambda m: sayi(int(m.group())), s)


def eslestir(metin: str, ses: str, sira: int) -> tuple[str, str]:
    """Yedek: kalıp kalmışsa metin ve ses alanlarını kendi konularıyla dönüştür."""
    m, m2 = KALIP.match(metin), KALIP.match(ses)
    if not m and not m2:
        return metin, rakamsiz(ses)
    konu_m = (m or m2).group("konu").strip()
    konu_s = (m2 or m).group("konu").strip()
    kalan = metin[m.end():].strip() if m else ""
    kalan_ses = ses[m2.end():].strip() if m2 else ""
    kalan = re.sub(r"^[.;:,]\s*", "", kalan)
    kalan_ses = re.sub(r"^[.;:,]\s*", "", kalan_ses)
    metin = f"{konu_m}; { kucuk_bas(kalan) }" if kalan else f"{konu_m} bu soru için geçerli değildir."
    ses = f"{konu_s}. {buyuk(kalan_ses)}" if kalan_ses else f"{konu_s} bu soru için geçerli değildir."
    return metin, rakamsiz(ses)


def kucuk_bas(s: str) -> str:
    if not s:
        return s
    return s


def temizle(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def soru_metni(kod: str, q: dict, duzeltmeler: dict) -> tuple[str, str, str, dict[str, str], str]:
    """(metin, ses, acilis, aciklamalar, ozet) — başlık + şıklar + açılış + şık açıklamaları + cevap + özet."""
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
        anahtar = f"{kod}/{n}/{h}"
        if anahtar in duzeltmeler:
            em = temizle(duzeltmeler[anahtar]["metin"])
            es = rakamsiz(temizle(duzeltmeler[anahtar]["ses"]))
        else:
            em, es = eslestir(temizle(q["siklar"][h]["metin"]), temizle(q["siklar"][h]["ses"]), i + n)
        aciklamalar[h] = em
        parcalar_m += [f"- **{q['secenekler'][h]}** — {em}"]
        parcalar_s.append(es)

    ozet_anahtar = f"{kod}/{n}/ozet"
    if ozet_anahtar in duzeltmeler:
        ozet_m = temizle(duzeltmeler[ozet_anahtar]["metin"])
        ozet_s = rakamsiz(temizle(duzeltmeler[ozet_anahtar]["ses"]))
    else:
        ozet_m = temizle(q["cozum"]["metin"])
        ozet_s = rakamsiz(temizle(q["cozum"]["ses"]))

    parcalar_m += ["", f"**Cevap: {dogru}** — {q['secenekler'][dogru]}", "",
                   f"**Özet.** {ozet_m}"]
    parcalar_s += [f"Doğru cevap {HARF_SES[dogru]}, {q['secenek_ses'][dogru]}", ozet_s]
    return "\n".join(parcalar_m), rakamsiz("\n".join(parcalar_s)), acilis, aciklamalar, ozet_m


def main() -> None:
    CIKTI.mkdir(parents=True, exist_ok=True)
    index_dersler = sorted(
        json.loads(INDEX.read_text(encoding="utf-8"))["dersler"],
        key=lambda x: x.get("no", 999),
    )
    duzeltmeler = json.loads(DUZELTME_P.read_text(encoding="utf-8")) if DUZELTME_P.exists() else {}
    tum_md: list[str] = ["# Patoloji — Alternatif Sesli Soru Çözücü", ""]
    ozet = []

    for d_meta in index_dersler:
        kod = d_meta["kod"]
        baslik = d_meta["baslik"]
        ders_no = d_meta["no"]
        p = GIRDI / f"{kod}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        std_p = STD_COZUCU / f"{kod}.json"
        std_by_no = {}
        if std_p.exists():
            for sq in json.loads(std_p.read_text(encoding="utf-8")).get("sorular", []):
                std_by_no[sq["no"]] = sq

        sorular = []
        for q in d["sorular"]:
            if q.get("tur") not in ("ornek", "cikmis"):
                continue
            metin, ses, acilis, aciklamalar, ozet_m = soru_metni(kod, q, duzeltmeler)
            sq = std_by_no.get(q["no"], {})
            ipucu = (q.get("ipucu", {}).get("metin") if isinstance(q.get("ipucu"), dict) else q.get("ipucu")) or sq.get("ipucu") or ""
            sayfa = q.get("sayfa") or sq.get("sayfa") or []
            zorluk = q.get("zorluk") or sq.get("zorluk")
            sinav = q.get("sinav") or sq.get("sinav")
            kayit_q = {
                "no": q["no"],
                "tur": q["tur"],
                **({"zorluk": zorluk} if zorluk else {}),
                **({"sinav": sinav} if sinav else {}),
                "soru": q["soru"],
                "secenekler": q["secenekler"],
                "dogru": q["dogru"],
                "ipucu": temizle(ipucu),
                "giris": acilis,
                "aciklamalar": aciklamalar,
                "ozet": ozet_m,
                "sayfa": sayfa,
                "metin": metin,
                "ses": ses,
                "kelime": len(metin.split()),
            }
            sorular.append(kayit_q)
        if not sorular:
            continue
        cikti = {"kod": kod, "no": ders_no, "baslik": baslik, "surum": "alt-2", "sorular": sorular}
        (CIKTI / f"{kod}.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1), encoding="utf-8")

        md = [f"# Ders {ders_no} ({kod}) · {baslik}", "", f"_{len(sorular)} soru (örnek + çıkmış)_", ""]
        for s in sorular:
            md += [f"## Soru {s['no']}", "", s["metin"], ""]
        (CIKTI / f"{kod}.md").write_text("\n".join(md), encoding="utf-8")
        tum_md += md
        ozet.append((kod, baslik, len(sorular), sum(x["kelime"] for x in sorular)))
        print(f"{kod} (Ders {ders_no}): {len(sorular)} soru")

    (CIKTI / "tum_sorular.md").write_text("\n".join(tum_md), encoding="utf-8")
    print(f"TOPLAM {sum(o[2] for o in ozet)} soru, {sum(o[3] for o in ozet)} kelime")


if __name__ == "__main__":
    main()
