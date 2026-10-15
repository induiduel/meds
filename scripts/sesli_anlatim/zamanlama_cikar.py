#!/usr/bin/env python3
"""Üretilmiş sesli anlatım varyantlarına geriye dönük paragraf zamanlaması ekler.

MP3 ffmpeg ile çözülür (24 kHz mono s16), 10 ms pencerelerde dijital sessizlik aralıkları bulunur.
Edge (Emel) üretiminde her paragrafın ardından 0,7 sn tam sessizlik (bölüm başında ek 0,5 sn) eklendiği için
paragraflar arası ≥0,65 sn sessizlik beklenir (ölçümde ≥0,95 sn; Edge'in cümle içi tam sessiz duraklamaları ≤0,65 sn).
Eşik sırası 0,85 → 0,65 → 0,30 sn: iç aralık sayısı = paragraf-1 ise doğrudan eşlenir; fazlaysa en uzun N-1 aralık
seçilir; hiçbir eşikte yetmezse süre karakter oranıyla dağıtılır.

Sonuç kayit.json'daki varyanta `zamanlama: [[bas, son], ...]` (sn, 2 ondalık, bitişik: son = sonrakinin başı)
ve `zamanlamaKaynak` olarak yazılır. Yazmadan hemen önce dosya yeniden okunur, yalnız bu iki alan eklenir, atomik yazılır.

Kullanım:
  python3 scripts/sesli_anlatim/zamanlama_cikar.py --key k1-28-tumor-biyolojisi-ve-terminolojisi
  python3 scripts/sesli_anlatim/zamanlama_cikar.py --hepsi            # zamanlaması olmayan (ya da 'tahmini') tüm varyantlar
  python3 scripts/sesli_anlatim/zamanlama_cikar.py --hepsi --zorla    # hepsini yeniden ölç
  --kuru: yazmadan yalnız ölç ve raporla
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

KOK = Path(__file__).resolve().parents[2] / "data" / "sesli_anlatim"
KAYIT = KOK / "kayit.json"
VARSAYILAN_FFMPEG = (
    "/tmp/claude-1000/-home-indu-medsor/5af3e86e-9219-4c43-b962-ca6e1550adee/scratchpad/ttsenv/lib/python3.14/"
    "site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
)
SR = 24000
PENCERE = 240  # 10 ms
ESIK = 4  # |örnek| <= ESIK → dijital sessizlik (kod çözücü yuvarlaması payı)


def ffmpeg_yolu() -> str:
    for aday in (os.environ.get("FFMPEG"), VARSAYILAN_FFMPEG, "ffmpeg"):
        if not aday:
            continue
        if aday == "ffmpeg" or Path(aday).exists():
            return aday
    raise SystemExit("ffmpeg bulunamadı (FFMPEG ortam değişkeni)")


def metin_paragraflari(md: str) -> list[dict]:
    """sesliAnlatim.ts::metinParagraflari ile birebir aynı ayrıştırma."""
    out: list[dict] = []
    bolum_basi = True
    tampon: list[str] = []

    def bitir():
        nonlocal bolum_basi, tampon
        t = re.sub(r"\s+", " ", " ".join(tampon)).strip()
        if t:
            out.append({"t": t, "bolumBasi": bolum_basi})
            bolum_basi = False
        tampon = []

    for s in re.split(r"\r?\n", md):
        if s.startswith("# "):
            continue
        if s.startswith("@@"):
            bitir()
            bolum_basi = True
            continue
        if not s.strip():
            bitir()
        else:
            tampon.append(s.strip())
    bitir()
    return out


def sessiz_pencereler(mp3: Path) -> tuple[np.ndarray, float]:
    """10 ms pencere başına 'tam sessiz mi' dizisi ve toplam süre (sn). Akışla okunur (düşük bellek)."""
    p = subprocess.Popen(
        [ffmpeg_yolu(), "-v", "error", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
        stdout=subprocess.PIPE,
    )
    parcalar: list[np.ndarray] = []
    artik = np.zeros(0, dtype=np.int16)
    toplam = 0
    blok = PENCERE * 2 * 4000
    assert p.stdout
    while True:
        b = p.stdout.read(blok)
        if not b:
            break
        s = np.frombuffer(b, dtype=np.int16)
        toplam += len(s)
        if len(artik):
            s = np.concatenate([artik, s])
        n = len(s) // PENCERE
        artik = s[n * PENCERE :].copy()
        if n:
            m = np.abs(s[: n * PENCERE].reshape(n, PENCERE).astype(np.int32)).max(axis=1)
            parcalar.append(m <= ESIK)
    if len(artik):
        parcalar.append(np.array([np.abs(artik.astype(np.int32)).max() <= ESIK]))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg hata kodu {p.returncode}")
    return (np.concatenate(parcalar) if parcalar else np.zeros(0, dtype=bool)), toplam / SR


def sessizlik_araliklari(sessiz: np.ndarray) -> list[tuple[float, float]]:
    """Ardışık sessiz pencere koşuları → [(bas_sn, son_sn)]."""
    if not len(sessiz):
        return []
    d = np.diff(np.concatenate([[0], sessiz.astype(np.int8), [0]]))
    baslar = np.where(d == 1)[0]
    sonlar = np.where(d == -1)[0]
    return [(b * PENCERE / SR, e * PENCERE / SR) for b, e in zip(baslar, sonlar)]


def karakter_orani(paragraflar: list[dict], toplam: float) -> list[float]:
    """Paragraf başlarını karakter uzunluğu oranında dağıtır (Edge sessizlik paylarıyla)."""
    agirlik = [len(p["t"]) for p in paragraflar]
    sessiz = sum(0.7 + (0.5 if p["bolumBasi"] else 0) for p in paragraflar)
    net = max(0.0, toplam - sessiz)
    tk = sum(agirlik) or 1
    t = 0.0
    out = []
    for p, a in zip(paragraflar, agirlik):
        if p["bolumBasi"]:
            t += 0.5
        out.append(t)
        t += net * a / tk + 0.7
    return out


def zamanlama_cikar(mp3: Path, paragraflar: list[dict]) -> tuple[list[list[float]], dict]:
    n = len(paragraflar)
    sessiz, toplam = sessiz_pencereler(mp3)
    araliklar = sessizlik_araliklari(sessiz)
    # dosyanın başındaki/sonundaki sessizlik paragraf arası değildir
    bas0 = 0.0
    if araliklar and araliklar[0][0] <= 0.02:
        bas0 = araliklar[0][1]
        araliklar = araliklar[1:]
    if araliklar and araliklar[-1][1] >= toplam - 0.05:
        araliklar = araliklar[:-1]
    bilgi: dict = {"toplamSn": round(toplam, 2), "beklenenAra": n - 1}
    secilen = None
    bilgi["bulunanAra"] = sum(1 for a in araliklar if a[1] - a[0] >= 0.65)
    # Ölçüm: Edge cümle içi duraklamaları da tam sessiz ama ≤0,65 sn; paragraf araları (0,7 + Edge kuyruğu) ≥0,95 sn.
    for esik in (0.85, 0.65, 0.30):
        aday = [a for a in araliklar if a[1] - a[0] >= esik]
        if len(aday) == n - 1:
            secilen, bilgi["yontem"] = aday, ("sessizlik" if esik >= 0.65 else "sessizlik-0.30")
            break
        if len(aday) > n - 1:
            secilen = sorted(sorted(aday, key=lambda a: a[1] - a[0], reverse=True)[: n - 1])
            bilgi["yontem"] = f"sessizlik-en-uzun-{esik}"
            break
    if secilen is not None:
        baslar = [bas0] + [a[1] for a in secilen]
    else:
        baslar = karakter_orani(paragraflar, toplam)
        bilgi["yontem"] = "karakter"
    zam = [[round(b, 2), round(baslar[i + 1] if i + 1 < n else toplam, 2)] for i, b in enumerate(baslar)]
    return zam, bilgi


def kayit_oku() -> dict:
    return json.loads(KAYIT.read_text(encoding="utf-8"))


def kayda_yaz(key: str, vid: str, zam: list, kaynak: str) -> bool:
    """Yazmadan hemen önce yeniden okur, yalnız zamanlama alanlarını ekler, atomik yazar."""
    k = kayit_oku()
    v = next((x for x in k.get(key, []) if x.get("id") == vid), None)
    if v is None:
        return False
    v["zamanlama"] = zam
    v["zamanlamaKaynak"] = kaynak
    tmp = KAYIT.with_name(f"kayit.json.zc-{os.getpid()}.tmp")
    tmp.write_text(json.dumps(k, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, KAYIT)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--key", action="append", help="ders anahtarı (birden çok verilebilir)")
    g.add_argument("--hepsi", action="store_true")
    ap.add_argument("--zorla", action="store_true", help="zamanlaması olanları da yeniden ölç")
    ap.add_argument("--kuru", action="store_true", help="kayit.json'a yazma")
    a = ap.parse_args()

    kayit = kayit_oku()
    anahtarlar = a.key if a.key else list(kayit.keys())
    ozet = {"islenen": 0, "tam": 0, "yaklasik": 0, "karakter": 0, "atlanan": 0}
    for key in anahtarlar:
        if not re.fullmatch(r"k1-\d+-[a-z0-9-]+", key):
            print(f"! geçersiz anahtar: {key}")
            continue
        mdp = KOK / "metin" / f"{key}.md"
        if not mdp.exists():
            print(f"! {key}: metin yok")
            continue
        paragraflar = metin_paragraflari(mdp.read_text(encoding="utf-8"))
        for v in kayit.get(key, []):
            vid = v.get("id", "")
            if not a.zorla and v.get("zamanlama") and v.get("zamanlamaKaynak") != "tahmini":
                ozet["atlanan"] += 1
                continue
            mp3 = KOK / "ses" / key / f"{vid}.mp3"
            if not mp3.exists():
                print(f"! {key}/{vid}: mp3 yok")
                continue
            zam, b = zamanlama_cikar(mp3, paragraflar)
            yontem = b["yontem"]
            ozet["islenen"] += 1
            if yontem == "sessizlik":
                ozet["tam"] += 1
            elif yontem == "karakter":
                ozet["karakter"] += 1
            else:
                ozet["yaklasik"] += 1
            print(
                f"{key} / {vid}: paragraf {len(paragraflar)}, beklenen ara {b['beklenenAra']}, "
                f"bulunan ≥0,65 sn {b.get('bulunanAra')}, yöntem {yontem}, süre {b['toplamSn']} sn"
                + ("" if abs(b["toplamSn"] - v.get("sureSn", 0)) < 3 else f" (kayıt {v.get('sureSn')} sn!)")
            )
            if not a.kuru:
                if not kayda_yaz(key, vid, zam, yontem):
                    print(f"  ! {key}/{vid} kayıttan kalkmış; yazılmadı")
    print("ÖZET:", json.dumps(ozet, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
