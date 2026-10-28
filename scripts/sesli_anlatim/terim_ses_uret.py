#!/usr/bin/env python3
"""Terim / kısaltma / bilgi paketi (1-2 cümle) hazır sesleri — EMA, GPU (kullanıcı isteği 2026-10-28).

Amaç: öğrenci PDF'te ya da metinde bir terimi/bilgi paketini sesli okutmak isterse klip önceden hazır olsun.
Kaynaklar (hepsi birleştirilir, aynı okunacak metin tek klip):
  data/sesli_anlatim/terim/*.json, kisaltma/*.json   (PDF terim yardımcısı: t + a)
  src/data/ders_icerik/*.json                         (terimler t+a, kisaltmalar k+acilim, bilgiler b+m)
  src/data/terim_yardimcisi_sozluk.json, kisaltma_sozluk.json   (genel sözlük: term + definition)
Çıktı: data/terim_ses/<h2>/<h>.mp3 ve data/terim_ses/kayit.json  {h: {t: başlık, m: okunan metin, sure, kaynak: [...]}}
  h = sha1(SURUM + okunan metin)[:12]  → içerikle adreslenir; ekran aynı metni hesaplayıp klibi bulur (terim_ses_anahtar()).
Okunuş: ders sesiyle aynı Kurul 2+ yolu (terim_okunus + fonetik + "dee nee aa" kısaltma). Metni değişmeyen klip yeniden üretilmez.

Başlatıcı (GPU, koruyucu zorunlu): bash scripts/patoloji_cozucu/cozucu_ses_gpu.sh scripts/sesli_anlatim/terim_ses_uret.py [--sinir N] [--sadece-liste]
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

if os.environ.get("EMA_CIHAZ") != "cuda":
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts/sesli_anlatim"))
CIKTI = MEDS / "data/terim_ses"
SURUM = "terim-1"
ARA_SN = 0.35


def temizle(s: str) -> str:
    s = re.sub(r"\*\*|__|`", "", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def nokta(s: str) -> str:
    return s if not s or s[-1] in ".!?" else s + "."


def okunacak(baslik: str, govde: str) -> tuple[str, str]:
    return nokta(temizle(baslik)), nokta(temizle(govde))


_YUNAN = {"α": "alfa", "Α": "alfa", "β": "beta", "γ": "gama", "δ": "delta", "ε": "epsilon", "κ": "kappa", "μ": "mikro", "µ": "mikro"}
_ALT = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
_UST = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def konus(s: str) -> str:
    """Ekrandaki yazımı → modele giden okunuş. Unicode simgeler ("unikod U artı 207A") ve işaretler Türkçe okunur.
    Klip anahtarı ekrandaki metne bağlı kalır (arayüz klibi buradan bulur); yalnız seslendirilen metin değişir."""
    s = re.sub(r"[µμ]L\b", "mikrolitre", s)
    s = re.sub(r"\b([Vv]e)/([Vv]eya)\b", r"\1 ya", s)
    for a, b in _YUNAN.items():
        s = s.replace(a, b + " " if a not in "µμ" else b)
    s = re.sub(r"(\d)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: f"{m[1]} üzeri {m[2].translate(_UST)}", s)          # 10⁵ → 10 üzeri 5
    s = re.sub(r"([A-Za-zÇĞİÖŞÜçğıöşü])²", r"\1 kare", s)
    s = re.sub(r"([A-Za-zÇĞİÖŞÜçğıöşü])³", r"\1 küp", s)
    s = s.replace("⁺", " artı").replace("⁻", " eksi").translate(_ALT)
    s = s.replace("≥", " büyük eşit ").replace("≤", " küçük eşit ").replace("≈", " yaklaşık ").replace("±", " artı eksi ")
    s = s.replace("×", " çarpı ").replace("→", ", ardından ").replace("°", " derece").replace("•", " ").replace("·", " ")
    s = re.sub(r"[«»“”\"]", "", s)
    s = s.replace("é", "e").replace("ä", "e")
    s = re.sub(r"[−-](?=\d)(?<![\w])", "eksi ", s) if False else re.sub(r"(?<![\w])−(?=\d)", "eksi ", s).replace("−", " eksi ")
    s = re.sub(r"(?<=\d)\s*[–-]\s*(?=\d)", " ila ", s)   # 20–24 → 20 ila 24
    s = s.replace("–", ", ")
    s = re.sub(r"%\s*(\d[\d.,]*)", r"yüzde \1", s)
    s = re.sub(r"(\d[\d.,]*)\s*%", r"yüzde \1", s)
    s = s.replace("%", " yüzde ")
    s = re.sub(r"\s*<\s*", " küçüktür ", s)
    s = re.sub(r"\s*>\s*", " büyüktür ", s)
    s = re.sub(r"\s+=\s+", " eşittir ", s)
    s = re.sub(r"\s+\+\s+", " artı ", s)
    s = s.replace("~", " yaklaşık ")
    s = re.sub(r"(?<=\w)/(?=\w)", " bölü ", s)
    s = re.sub(r"\b([A-Z]{2,5})(\d)([A-Z])(\d{1,2})\b", r"\1 \2 \3 \4", s)   # CYP2D6 → CYP 2 D 6
    s = re.sub(r"\b([A-Z]{2,5})(\d)([A-Z])\b", r"\1 \2 \3", s)                # CYP3A → CYP 3 A
    return re.sub(r"\s+", " ", s).replace(" ,", ",").replace(" .", ".").strip()


def anahtar(baslik: str, govde: str) -> str:
    b, g = okunacak(baslik, govde)
    return hashlib.sha1(f"{SURUM}|{b}|{g}".encode()).hexdigest()[:12]


def topla() -> dict[str, dict]:
    """h → {t, b, g, kaynak:set}"""
    out: dict[str, dict] = {}

    def ekle(baslik, govde, kaynak):
        b, g = okunacak(baslik, govde)
        if not b or not g or len(g) < 4:
            return
        h = anahtar(baslik, govde)
        o = out.setdefault(h, {"t": temizle(baslik), "b": b, "g": g, "kaynak": set()})
        o["kaynak"].add(kaynak)

    for f in sorted(glob.glob(str(MEDS / "data/sesli_anlatim/terim/*.json")) + glob.glob(str(MEDS / "data/sesli_anlatim/kisaltma/*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for sl in d.get("d", {}).values():
            for pg in sl.values():
                for e in pg.get("t", []):
                    ekle(e.get("t"), e.get("a") or e.get("acilim"), d.get("key", Path(f).stem))
    for f in sorted(glob.glob(str(MEDS / "src/data/ders_icerik/*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        k = Path(f).stem
        for e in d.get("terimler", []):
            ekle(e.get("t"), e.get("a"), k)
        for e in d.get("kisaltmalar", []):
            ekle(e.get("k"), e.get("acilim"), k)
        for e in d.get("bilgiler", []):
            ekle(e.get("b"), e.get("m"), k)
    for f, ad in (("terim_yardimcisi_sozluk.json", "sozluk-terim"), ("kisaltma_sozluk.json", "sozluk-kisaltma")):
        for e in json.load(open(MEDS / "src/data" / f, encoding="utf-8")).values():
            ekle(e.get("term"), e.get("definition"), ad)
    return out


def main() -> None:
    a = sys.argv[1:]
    sinir = int(a[a.index("--sinir") + 1]) if "--sinir" in a else None
    liste = topla()
    print(f"toplam benzersiz klip: {len(liste)}", flush=True)
    if "--sadece-liste" in a:
        return
    import numpy as np
    import ema_isci as E

    E.KBPS = 48
    E.UZUN_KISALTMA = True  # Kurul 2+ okunuşu
    CIKTI.mkdir(parents=True, exist_ok=True)
    kp = CIKTI / "kayit.json"
    kayit = json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
    tts = E.model_yukle()
    sessiz = np.zeros(int(ARA_SN * E.SR), dtype=np.float32)
    yeni = hata = 0
    t0 = time.time()
    def vh(o):  # okunuş sürümü: konuş() sonucu
        return hashlib.sha1(("k1|" + konus(o["b"] + " " + o["g"])).encode()).hexdigest()[:8]

    def tamam(h):
        k = kayit.get(h)
        if not (k and (CIKTI / h[:2] / f"{h}.mp3").exists()):
            return False
        o = liste[h]
        return k.get("v") == vh(o) if "v" in k else konus(o["b"] + " " + o["g"]) == o["b"] + " " + o["g"]

    bekleyen = [h for h in liste if not tamam(h)]
    if sinir:
        bekleyen = bekleyen[:sinir]
    print(f"üretilecek: {len(bekleyen)}", flush=True)
    for i, h in enumerate(bekleyen, 1):
        o = liste[h]
        try:
            x, n1 = E.paragraf_seslendir(tts, konus(o["b"] + " " + o["g"]))  # tek paragraf: kısa başlık tek başına süre denetimini bozuyordu
            n2 = None
            mp3 = E.mp3_kodla((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
            d = CIKTI / h[:2]
            d.mkdir(exist_ok=True)
            (d / f"{h}.mp3").write_bytes(mp3)
            kayit[h] = {"t": o["t"], "m": o["b"] + " " + o["g"], "sure": round(len(mp3) * 8 / 48000, 2), "v": vh(o),
                        "kaynak": sorted(o["kaynak"])[:6], **({"not": [n for n in (n1, n2) if n]} if (n1 or n2) else {})}
            yeni += 1
        except Exception as ex:  # tek klip hatası işi durdurmaz; sonda raporlanır
            hata += 1
            print(f"HATA {h} {o['t']}: {ex}", flush=True)
            if "CUDA" in str(ex) or "out of memory" in str(ex).lower():
                print("CUDA hatası — durduruluyor (yeniden çalıştırınca kalan devam eder)", flush=True)
                break
        if i % 25 == 0:
            kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
            print(f"{i}/{len(bekleyen)} ({time.time() - t0:.0f} sn)", flush=True)
    kp.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
    print(f"bitti: {yeni} yeni, {hata} hata, toplam kayıt {len(kayit)}/{len(liste)}", flush=True)
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
