#!/usr/bin/env python3
"""Kısaltma / gen sembolü → ders metninde yazılacak Türkçe okunuş (ajan UYDURMAZ, bunu kullanır). LLM yok.

  python3 scripts/tam_hat/dis_ajan/okunus_oner.py HOXD13 OTX2 MSX1 PAX6 MITF
Kural kaynağı: yayınlanmış k2-08 dersi ve sitenin kendi ses denetimi (`metin_denetle.py`, --yazim OLMADAN: büyük harfli kısaltma HATA, okunuşla yazılır).
  * Harfler Türkçe harf adıyla okunur: a, be, ce, de, e, fe, ge, he, ı, je, ke, le, me, ne, o, pe, re, se, te, u, ve, ye, ze; X = iks, W = dublevе.
  * Ünlü gibi okunan gen aileleri kelime olarak okunur: HOX = hoks, PAX = paks, SOX = soks.
  * Sayılar yazıyla (6 = altı, 13 = on üç). Başlangıçta ilk harf büyük yazılabilir ("Hoks genleri").
Emin olmadığın kısaltmada okunuşu uydurma; bu aracın çıktısını kullan, çıktı sana yanlış geliyorsa kullanıcıya sor.
"""
from __future__ import annotations

import re
import sys

HARF = {"a": "a", "b": "be", "c": "ce", "ç": "çe", "d": "de", "e": "e", "f": "fe", "g": "ge", "ğ": "yumuşak ge", "h": "he", "ı": "ı",
        "i": "i", "j": "je", "k": "ke", "l": "le", "m": "me", "n": "ne", "o": "o", "ö": "ö", "p": "pe", "q": "ku", "r": "re", "s": "se",
        "ş": "şe", "t": "te", "u": "u", "ü": "ü", "v": "ve", "w": "dublev e".replace(" ", ""), "x": "iks", "y": "ye", "z": "ze"}
KELIME = {"HOX": "hoks", "PAX": "paks", "SOX": "soks"}
BIR = ["sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def harf(h: str) -> str:
    return {"I": "ı", "İ": "i"}.get(h) or HARF.get(h.lower(), h.lower())


def sayi(n: int) -> str:
    if n < 10:
        return BIR[n]
    if n < 100:
        return (ON[n // 10] + " " + (BIR[n % 10] if n % 10 else "")).strip()
    return str(n)  # 100+: elle yaz


def oner(tok: str) -> str:
    m = re.fullmatch(r"([A-ZÇĞİÖŞÜ]+)(\d*)([A-Za-z]*)(\d*)", tok)
    if not m:
        return ""
    harfler, sayi1, harf2, sayi2 = m.groups()
    out = []
    for kel, onek in KELIME.items():
        if harfler == kel or harfler.startswith(kel):
            out.append(onek)
            harfler = harfler[len(kel):]
            break
    out += [harf(h) for h in harfler]
    if sayi1:
        out.append(sayi(int(sayi1)))
    out += [harf(h) for h in harf2]
    if sayi2:
        out.append(sayi(int(sayi2)))
    return " ".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    for t in sys.argv[1:]:
        print(f"{t:10} → {oner(t)}")
