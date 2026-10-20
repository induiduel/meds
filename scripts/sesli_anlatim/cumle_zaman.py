#!/usr/bin/env python3
"""Sesli derslerde cümle düzeyinde zamanlama: okunan cümle vurgusu sesle birebir gitsin.

Paragraf zamanlaması (kayit.json `zamanlama`) gerçek duraklamalardan ölçülüdür; paragraf İÇİNDEKİ cümle ise
istemcide karakter oranıyla tahmin ediliyordu. Sayı, kısaltma ve uzun terimler daha uzun okunduğu için
~40 sn'lik paragraflarda vurgu sesten saniyelerce kayıyordu. Bu betik her cümle sınırını, tahmini anın
çevresindeki (±pay) en uzun duraklamaya oturtur.

Paragraf ve cümle bölmesi istemciyle BİREBİR aynı olsun diye metin yerel sunucudan okunur
(GET /api/canli-ders/<key>, 3000 açık olmalı); cümle kuralı canliDersStore.ts::cumleSinirlari ile aynıdır.

Çıktı: data/sesli_anlatim/cumle_zaman/<key>.json
  { "surum": 1, "metinHash": sha1(paragraflar '\\n' ile), "varyantlar": { "<vid>": { "bayt": n, "p": { "<i>": [t1, t2, …] } } } }
  t_j = (j+1). cümlenin başladığı saniye (paragrafın ilk cümlesi paragraf başıdır, yazılmaz).
Sunucu yalnız metinHash ve bayt tutarsa gönderir; metin/ses değişince eski dosya kendiliğinden yok sayılır.

Kullanım:
  python3 scripts/sesli_anlatim/cumle_zaman.py --hepsi            # eksik/eskimiş olanlar
  python3 scripts/sesli_anlatim/cumle_zaman.py --key k1-03-hucresel-adaptasyonlar [--zorla] [--kuru]
FFMPEG ortam değişkeni ya da imageio_ffmpeg gerekir. Yalnız CPU.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

KOK = Path(__file__).resolve().parents[2] / "data" / "sesli_anlatim"
CIKTI = KOK / "cumle_zaman"
API = os.environ.get("MEDS_API", "http://127.0.0.1:3000")
SR = 16000
FR = 160  # 10 ms


def ffmpeg_yolu() -> str:
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    try:
        import imageio_ffmpeg  # type: ignore
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def coz(mp3: Path) -> np.ndarray:
    r = subprocess.run([ffmpeg_yolu(), "-v", "error", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32)


def enerji(pcm: np.ndarray) -> np.ndarray:
    n = len(pcm) // FR
    return np.sqrt((pcm[: n * FR].reshape(n, FR) ** 2).mean(axis=1))


# canliDersStore.ts::cumleSinirlari ile aynı kural
CUMLE_RE = re.compile(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)")


def cumle_sonlari(metin: str) -> list[int]:
    out: list[int] = []
    for m in CUMLE_RE.finditer(metin):
        if not m.group(0):
            continue
        e = m.end()
        sonraki = metin[e:e + 1]
        if sonraki and sonraki != sonraki.upper() and sonraki == sonraki.lower():
            continue
        if e > (out[-1] if out else 0):
            out.append(e)
        if e >= len(metin):
            break
    if not out or out[-1] < len(metin):
        out.append(len(metin))
    return out


def sessizlikler(en: np.ndarray, esik: float, min_kare: int = 8) -> list[tuple[int, int]]:
    """Eşik altı ardışık kare aralıkları [bas, son) (kare = 10 ms)."""
    alt = en < esik
    out = []
    i = 0
    n = len(alt)
    while i < n:
        if alt[i]:
            j = i
            while j < n and alt[j]:
                j += 1
            if j - i >= min_kare:
                out.append((i, j))
            i = j
        else:
            i += 1
    return out


def konusma_parcalari(sinir: list[float], sess: list[tuple[int, int]]) -> list[list[float]]:
    """Her cümlenin sesteki konuşma parçaları [a1, b1, a2, b2, …] (sn): cümle aralığından ≥80 ms duraklamalar çıkarılır.
    Kelime kelime takip bununla yapılır: sessizlik kelimelere paylaştırılmaz (cümle sonu/virgül gecikmesi olmaz)."""
    out = []
    for a, b in zip(sinir, sinir[1:]):
        parca, bas = [], a
        for x, y in sess:
            x, y = x / 100.0, y / 100.0
            if y <= a or x >= b or y - x < 0.08:
                continue
            if x > bas + 0.05:
                parca += [round(bas, 2), round(x, 2)]
            bas = max(bas, y)
        if b > bas + 0.05:
            parca += [round(bas, 2), round(b, 2)]
        out.append(parca or [round(a, 2), round(b, 2)])
    return out


def ders_isle(key: str, zorla: bool, kuru: bool) -> str:
    with urllib.request.urlopen(f"{API}/api/canli-ders/{key}", timeout=30) as r:
        d = json.load(r)
    paras = [p for b in d["bolumler"] for p in b["paragraflar"]]
    metin_hash = hashlib.sha1("\n".join(p["metin"] for p in paras).encode("utf-8")).hexdigest()
    hedef = CIKTI / f"{key}.json"
    eski = json.loads(hedef.read_text()) if hedef.exists() else None
    if eski and (eski.get("metinHash") != metin_hash or eski.get("surum") != 2):
        eski = None
    sonuc = {"surum": 2, "metinHash": metin_hash, "varyantlar": dict((eski or {}).get("varyantlar") or {})}
    rapor = []
    for v in d["varyantlar"]:
        vid, z = v["id"], v.get("zamanlama")
        mp3 = KOK / "ses" / key / f"{vid}.mp3"
        if not z or not mp3.exists():
            continue
        bayt = mp3.stat().st_size
        if not zorla and sonuc["varyantlar"].get(vid, {}).get("bayt") == bayt:
            continue
        en = enerji(coz(mp3))
        dolu = en[en > 0]
        if not len(dolu):
            continue
        # Göreli eşik: konuşma düzeyinin (p90) ~-32 dB altı; tam sessiz (Edge) ve gürültülü (yerel) seste çalışır
        esik = max(float(np.percentile(dolu, 90)) * 0.025, float(np.percentile(dolu, 5)) * 1.5, 1.0)
        sess = sessizlikler(en, esik)
        orta = np.array([(a + b) / 2 for a, b in sess]) / 100.0
        uzun = np.array([(b - a) for a, b in sess]) / 100.0
        p_out: dict[str, list[float]] = {}
        k_out: dict[str, list[list[float]]] = {}
        oturan = toplam = 0
        for p in paras:
            i = p["i"]
            if i >= len(z) or not z[i]:
                continue
            bas, son = float(z[i][0]), float(z[i][1])
            sonlar = cumle_sonlari(p["metin"])
            if len(sonlar) < 2 or son - bas < 1:
                continue
            L = max(1, len(p["metin"]))
            sure = son - bas
            tlar: list[float] = []
            onceki = bas + 0.3
            for j, e in enumerate(sonlar[:-1]):
                tahmin = bas + sure * e / L
                kalan_cumle = len(sonlar) - 1 - j
                ust = son - 0.3 * kalan_cumle
                pay = max(1.5, min(5.0, sure * 0.12))
                lo, hi = max(onceki + 0.2, tahmin - pay), min(ust, tahmin + pay)
                toplam += 1
                sec = None
                if len(orta) and hi > lo:
                    m = (orta >= lo) & (orta <= hi)
                    if m.any():
                        idx = np.nonzero(m)[0]
                        # en uzun duraklama; eşitlikte tahmine yakın olan
                        puan = uzun[idx] - np.abs(orta[idx] - tahmin) * 0.02
                        k = idx[int(np.argmax(puan))]
                        if uzun[k] >= 0.12:
                            sec = float(orta[k])
                if sec is None:
                    sec = min(max(tahmin, onceki + 0.2), max(onceki + 0.2, ust))
                else:
                    oturan += 1
                tlar.append(round(sec, 2))
                onceki = sec
            p_out[str(i)] = tlar
            k_out[str(i)] = konusma_parcalari([bas, *tlar, son], sess)
        sonuc["varyantlar"][vid] = {"bayt": bayt, "p": p_out, "k": k_out}
        rapor.append(f"{vid}: {oturan}/{toplam} sınır duraklamaya oturdu")
    if not rapor:
        return f"{key}: güncel"
    if not kuru:
        CIKTI.mkdir(parents=True, exist_ok=True)
        tmp = hedef.with_suffix(".tmp")
        tmp.write_text(json.dumps(sonuc, ensure_ascii=False, separators=(",", ":")))
        tmp.replace(hedef)
    return f"{key}: " + "; ".join(rapor)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key")
    ap.add_argument("--hepsi", action="store_true")
    ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    if a.key:
        keys = [a.key]
    elif a.hepsi:
        with urllib.request.urlopen(f"{API}/api/canli-ders", timeout=30) as r:
            keys = [x["key"] for x in json.load(r)["dersler"]]
    else:
        ap.error("--key ya da --hepsi")
    hata = 0
    for k in keys:
        try:
            print(ders_isle(k, a.zorla, a.kuru), flush=True)
        except Exception as e:  # tek ders hatası diğerlerini durdurmaz
            hata += 1
            print(f"{k}: HATA {e}", file=sys.stderr, flush=True)
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
