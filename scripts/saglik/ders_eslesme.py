#!/usr/bin/env python3
"""
Sağlık Bakanlığı sekmesi: ders slaytlarında geçen sayıların dizini → src/data/saglik/ders_eslesme.json

Halk sağlığı destelerinin (baglantilar.json'daki desteler + "Halk Sağlığı" disiplinli desteler) slayt anlatımı
cümlelere bölünür; her cümledeki anlamlı sayı (ondalıklı, yüzde, binde ya da ≥ 10 tam sayı; yıllar hariç) kanonik
biçimiyle ("7.8", "249614") dizine girer. Ön yüz (saglikDers.ts) sayfadaki bir değeri bu dizinde arar; aynı sayı +
cümlede ortak anahtar kelime (+ yıl uyumu) varsa değerin sağ üstüne "!" koyar ve sayıyı vurgular.

Çalıştırma: python3 scripts/saglik/ders_eslesme.py  (baglantilari_kur.py'den sonra)
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
DESTELER = KOK / "src/data/interactive_learning_decks.json"
BAG = KOK / "src/data/saglik/baglantilar.json"
CIKTI = KOK / "src/data/saglik/ders_eslesme.json"

SAYI = re.compile(r"(?<![\w.,/])(%\s?)?(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(?![\w])(\s?%|\s?‰)?")
YIL = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")


def kanonik(ham: str) -> str | None:
    """'249.614' → '249614', '7,8' → '7.8', '1.42' → '1.42' (tek nokta + ≠3 hane ondalık sayılır)"""
    s = ham.strip()
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        f = float(s)
    except ValueError:
        return None
    return (f"{f:.6f}".rstrip("0").rstrip(".")) or "0"


def anlamli(ham: str, kan: str, yuzde: bool) -> bool:
    if yuzde or "," in ham or ("." in kan):
        return True
    n = float(kan)
    if 1950 <= n <= 2049 and re.fullmatch(r"\d{4}", ham):
        return False  # yıl
    return n >= 10


def temizle(t: str) -> str:
    t = re.sub(r"\*\*|==|__|`|#+\s*", "", t or "")
    t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\(times|cdot)", lambda m: "×" if m.group(1) == "times" else "·", t).replace("$", "")
    t = re.sub(r"^\s*>\s*\[![A-Z]+\]\s*", "", t, flags=re.M)
    return t


def cumleler(t: str) -> list[str]:
    parcalar: list[str] = []
    for satir in re.split(r"\n+", t):
        satir = re.sub(r"^\s*[-*•]\s*", "", satir).strip()
        if not satir:
            continue
        # Sayılardaki noktayı bölme ("7.8", "249.614"): nokta + boşluk + büyük harf / satır sonu
        for c in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9(])", satir):
            c = c.strip()
            if c:
                parcalar.append(c)
    return parcalar


def kisalt(c: str, bas: int, son: int, uzun: int = 240) -> tuple[str, int, int]:
    """Cümle çok uzunsa sayının çevresinden kes; sayının yeni konumunu da döndür"""
    if len(c) <= uzun:
        return c, bas, son
    sol = max(0, bas - uzun // 2)
    sag = min(len(c), sol + uzun)
    sol = max(0, sag - uzun)
    on = "… " if sol > 0 else ""
    arka = " …" if sag < len(c) else ""
    return on + c[sol:sag] + arka, bas - sol + len(on), son - sol + len(on)


def main() -> None:
    desteler = json.loads(DESTELER.read_text(encoding="utf-8"))
    bag = json.loads(BAG.read_text(encoding="utf-8"))
    kisa: dict[str, str] = {}
    for b in bag.get("bolumler", {}).values():
        for d in b.get("desteler", []):
            kisa[d["id"]] = d.get("kisa") or d.get("baslik") or d["id"]
    secili = [d for d in desteler if d.get("id") in kisa or "Halk Sağlığı" in (d.get("discipline") or "")]
    # Aynı cümle birden çok destede varsa ilk deste yazılır: sitenin bağladığı (en yeni sürüm) desteler önce, eski "learn-*" sonra
    secili.sort(key=lambda d: (d.get("id") not in kisa, str(d.get("id", "")).startswith("learn-"), not str(d.get("id", "")).endswith("-v2")))

    # Cümleler bir kez saklanır; dizin sayı → [[cümle no, başlangıç, bitiş], …]
    cumle_l: list[dict] = []
    cumle_no: dict[tuple[str, int, str], int] = {}
    deste_ad: dict[str, str] = {}
    dizin: dict[str, list[list[int]]] = {}
    for d in secili:
        did = d["id"]
        deste_ad[did] = kisa.get(did) or d.get("shortTitle") or d.get("title") or did
        for i, s in enumerate(d.get("slides") or []):
            metin = temizle(s.get("synthesisNarrative") or s.get("content") or "")
            for c in cumleler(metin):
                bulunan = []
                for m in SAYI.finditer(c):
                    ham = m.group(2)
                    kan = kanonik(ham)
                    if kan and anlamli(ham, kan, bool(m.group(1) or m.group(3))):
                        bulunan.append((kan, m.start(2), m.end(2)))
                if not bulunan:
                    continue
                if len(c) > 260:  # uzun cümle: ilk sayının çevresi
                    t, _, _ = kisalt(c, bulunan[0][1], bulunan[0][2], 260)
                    kay = t.index(c[bulunan[0][1]:bulunan[0][2]]) - bulunan[0][1] if c[bulunan[0][1]:bulunan[0][2]] in t else 0
                    bulunan = [(k, a + kay, b + kay) for k, a, b in bulunan if 0 <= a + kay and b + kay <= len(t) and t[a + kay:b + kay] == c[a:b]]
                    c = t
                ozet = re.sub(r"\W+", "", c.lower())[:200]
                # Aynı cümle desteyin eski/yeni sürümünde tekrar ediyorsa bir kez (ilk deste) yazılır
                if any(k[2] == ozet for k in cumle_no):
                    continue
                no = len(cumle_l)
                cumle_no[(did, i, ozet)] = no
                cumle_l.append({"d": did, "s": i + 1, "b": (s.get("title") or "").strip()[:110], "t": c, "y": sorted(set(YIL.findall(c)) | set(YIL.findall(s.get("title") or "")))})
                for kan, a, b in bulunan:
                    dizin.setdefault(kan, []).append([no, a, b])
    cikti = {"surum": 2, "uretim": date.today().isoformat(), "desteler": deste_ad, "cumleler": cumle_l, "dizin": dizin}
    CIKTI.write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(secili)} deste · {len(dizin)} farklı sayı · {len(cumle_l)} cümle → {CIKTI.relative_to(KOK)} ({CIKTI.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
