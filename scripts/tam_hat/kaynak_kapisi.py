#!/usr/bin/env python3
"""Kaynak kapısı: sayfa (`s`) taşıyan her kaydın içeriği gerçekten o PDF sayfasında mı? (kullanıcı kararı 2026-10-28) LLM yok.

  python3 scripts/tam_hat/kaynak_kapisi.py <json> <sayfalar.json> [--esik 0.25]

<json>: ders içerik paketi, örnek soru, değerlendirme paketi … — içinde `s` (int sayfa) taşıyan her sözlük denetlenir.
<sayfalar.json>: hazirlik.py çıktısı ({"1": "sayfa metni", ...}).
Kaydın metin alanlarındaki (b, m, t, a, ad, soru, aciklama, metin) içerik sözcüklerinin (≥5 harf, Türkçe katlama, 5 harf
kök) en az %25'i s−1…s+1 sayfalarında geçmelidir; geçmiyorsa HATA "kaynakta bulunamadı" (uydurma ya da yanlış sayfa —
H105/H109 sınıfı). Sözlük terimlerinde (t + a) tanım sayfa dışı açıklamadır: terim adının her sözcüğü (4 harf kök, ya da `e` eşanlamı) s−2…s+2'de
geçmiyorsa HATA, tanım sayfayla az örtüşüyorsa UYARI — denetçi tanımın DERSİN bağlamına uyduğunu okur (k2-08: "Taşıyıcı"
patojen, "Frajilite" serviks anlamında genel sözlükten gelmişti). Sözcüğü 3'ten az kayıt (kısa etiket) ve `gorsel: true` (şekilden okunan, denetçi gözle doğrular) atlanır. HATA alan kayıt yalnız kendisi düzeltilir.
Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALANLAR = ("b", "m", "t", "a", "ad", "soru", "aciklama", "metin")
# Önce katla sonra küçült: "İ".lower() birleşik nokta üretir ("DİSTROFİ" → "di̇strofi̇")
KATLA = str.maketrans("çğıöşüâîûÇĞIİÖŞÜ", "cgiosuaiucgiiosu")
GENEL = {"olarak", "oldugu", "olmasi", "sonucu", "nedeniyle", "ancak", "ayrica", "ozellikle", "arasinda", "seklinde",
         "hangisi", "asagidakilerden", "dogrudur", "yanlistir", "derste", "sayfa", "sayilir", "verilir", "belirtilir"}


def kokler(metin: str) -> set[str]:
    out = set()
    for w in re.findall(r"[a-z0-9]+", metin.translate(KATLA).lower()):
        if len(w) >= 5 and w not in GENEL:
            out.add(w[:5])
    return out


def gez(x, yol=""):
    if isinstance(x, dict):
        if isinstance(x.get("s"), int):
            yield yol, x
        for k, v in x.items():
            yield from gez(v, f"{yol}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from gez(v, f"{yol}[{i}]")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", type=Path)
    ap.add_argument("sayfalar", type=Path)
    ap.add_argument("--esik", type=float, default=0.25)
    a = ap.parse_args()
    sayfa = {int(k): kokler(v) for k, v in json.loads(a.sayfalar.read_text()).items()}
    ham = {int(k): v.translate(KATLA).lower() for k, v in json.loads(a.sayfalar.read_text()).items()}
    hata, uyari, sayi = [], [], 0
    for yol, kayit in gez(json.loads(a.dosya.read_text())):
        if isinstance(kayit.get("t"), str) and isinstance(kayit.get("a"), str):  # sözlük terimi
            if kayit.get("gorsel"):
                continue
            sayi += 1
            s = kayit["s"]
            metin = " ".join(ham.get(p, "") for p in range(s - 2, s + 3))
            adlar = [kayit["t"], *[e for e in kayit.get("e") or [] if isinstance(e, str)]]
            # 4 harf kök: Türkçe/Latince yazım farkı (müsküler/musküler, Preaurikular çukur ~ preaurikularpits) tolere edilir
            k4 = {w[:4] for w in re.findall(r"[a-z0-9]+", metin)}
            if not any(all(w[:4] in k4 for w in re.findall(r"[a-z0-9]+", ad.translate(KATLA).lower()) if len(w) >= 3)
                       for ad in adlar):
                hata.append(f"{yol} (s.{s}): terim sayfada geçmiyor «{kayit['t']}»")
                continue
            w = kokler(kayit["a"])
            if len(w) >= 3 and len(w & kokler(metin)) / len(w) < a.esik:
                uyari.append(f"{yol} (s.{s}): tanım sayfayla az örtüşüyor, bağlamı denetçi okur «{kayit['t']}: {kayit['a'][:60]}»")
            continue
        metin = " ".join(str(kayit[k]) for k in ALANLAR if isinstance(kayit.get(k), str))
        w = kokler(metin)
        if len(w) < 3 or kayit.get("gorsel"):  # şekilden okunan bilgi (pdftotext görmez): denetçi gözle doğrular
            continue
        sayi += 1
        s = kayit["s"]
        hedef = set().union(*(sayfa.get(p, set()) for p in (s - 1, s, s + 1)))
        oran = len(w & hedef) / len(w)
        if oran < a.esik:
            hata.append(f"{yol} (s.{s}, örtüşme %{oran * 100:.0f}): «{metin[:70]}»")
    for h in hata:
        print("HATA kaynakta bulunamadı", h)
    for w in uyari:
        print("UYARI", w)
    print(f"{sayi} kayıt · {len(hata)} HATA · {len(uyari)} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
