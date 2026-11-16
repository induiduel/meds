"""Dış ajan araçlarının ortak yardımcıları (Türkçe katlama, sayı/olumsuzluk/yön ayıklama). LLM yok."""
from __future__ import annotations

import json
import re
from pathlib import Path

KATLA = str.maketrans("çğıöşüâîûÇĞIİÖŞÜ", "cgiosuaiucgiiosu")

# Olumsuzluk: yalnız açık sözcükler (yanlış alarmı düşük tutmak için sınırlı küme)
OLUMSUZ = re.compile(r"\b(degil\w*|yok\w*|gorulmez|bulunmaz|olmaz|olmayan\w*|olmayabilir|hicbir|hic|haric\w*|disinda)\b")
YUKARI = re.compile(r"(artar|artis|artmis|artan|yuksel|yuksek|fazla|cogal|buyur|buyuk|uzar|uzayan|↑)")
ASAGI = re.compile(r"(azalir|azalma|azalmis|azalan|duser|dusuk|dusme|kisalir|kisa\b|kucul|↓)")


def katla(s: str) -> str:
    """İ→i gibi Türkçe harfleri önce katla, sonra küçült (birleşik nokta üretmesin)."""
    return s.translate(KATLA).lower()


def norm(s: str) -> str:
    """Karşılaştırma için: katla, satır sonu tirelemesini birleştir, boşlukları tek boşluk yap."""
    s = re.sub(r"-\s*\n\s*", "", s)
    s = katla(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


BIRLER = {"iki": 2, "uc": 3, "dort": 4, "bes": 5, "alti_": 6, "yedi": 7, "sekiz": 8, "dokuz": 9}
ONLAR = {"yirmi": 20, "otuz": 30, "kirk": 40, "elli": 50, "altmis": 60, "yetmis": 70, "seksen": 80, "doksan": 90}
BIR = {"bir": 1, **BIRLER}


def sayilar(s: str) -> set[str]:
    """Rakamla yazılı sayılar + yazıyla yazılı sayılar (iki…doksan dokuz). 'bir', 'altı', 'yüz' belirsiz sözcük olduğundan yazıyla aranmaz."""
    out = {m.replace(",", ".") for m in re.findall(r"\d+(?:[.,]\d+)?", s)}
    w = re.findall(r"[a-z0-9]+", katla(s))
    i = 0
    while i < len(w):
        t = w[i]
        deger = None
        if t == "on" and i + 1 < len(w) and w[i + 1] in BIR:  # on üç = 13 ("on" tek başına belirsiz)
            deger, i = 10 + BIR[w[i + 1]], i + 1
        elif t in ONLAR:
            deger = ONLAR[t]
            if i + 1 < len(w) and w[i + 1] in BIR:
                deger, i = deger + BIR[w[i + 1]], i + 1
        elif t in BIRLER:
            deger = BIRLER[t]
        if deger is not None:
            out.add(str(deger))
        i += 1
    return out


def kokler(s: str) -> set[str]:
    return {w[:5] for w in re.findall(r"[a-z0-9]+", katla(s)) if len(w) >= 5}


def yukle(p: Path):
    try:
        return json.loads(p.read_text("utf8"))
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"HATA {p}: JSON okunamadı ({e}). Yapılacak: dosyayı geçerli JSON olarak yeniden yaz.")


def sayfa_metni(sayfalar: dict, s: int, pay: int = 1) -> str:
    return " ".join(sayfalar.get(str(k), "") for k in range(s - pay, s + pay + 1))


def sayfalar_yukle(p: Path) -> dict:
    """sayfalar.json: {"1": metin} ya da [metin, …] (eski taslak biçimi) → {"1": metin}."""
    d = yukle(p)
    if isinstance(d, list):
        if not all(isinstance(x, str) for x in d):
            raise SystemExit(f"HATA {p}: sayfalar.json sayfa metni sözlüğü olmalı ({{\"1\": \"metin\"}}). Yapılacak: hazirlik.py çıktısını kullan.")
        return {str(i + 1): x for i, x in enumerate(d)}
    return {str(k): v for k, v in d.items()}
