#!/usr/bin/env python3
"""Sesli derslerde kelime düzeyinde zamanlama: okunan kelime metinde ve slaytta sesle birebir ilerlesin.
Ses faster-whisper (medium, int8, YALNIZ CPU) ile kelime zaman damgalı çözülür; tanınan metin ders metniyle harf
düzeyinde hizalanır (SequenceMatcher). Her metin kelimesinin (istemcideki /\\S+/g bölmesiyle BİREBİR aynı) başlangıcı,
eşleşen ilk harfinin zamanıdır; eşleşmeyen kelimeler (ör. "%10" → "yüzde on") komşu eşleşmelerden doğrusal doldurulur.
Paragraf penceresi varyantın ölçülü `zamanlama`sıdır; kelime zamanı o pencereye kenetlenir ve hep artan olur.

Çıktı: data/sesli_anlatim/kelime_zaman/<key>.json → {surum, metinHash, varyantlar: {vid: {bayt, p: {i: [t, ...]}}}}
Sunucu yalnız metinHash ve bayt tutarsa gönderir (src/services/canliDers.ts).

Kullanım:
  kelime_zaman.py --key <ders> [--vid <varyant>] [--zorla] [--kuru]
  kelime_zaman.py --hepsi [--saglayici ema-yerel]     (yalnız verilen sağlayıcı; Kurul 2+ yalnız EMA)
  kelime_zaman.py --hepsi --oracle [--gpu]            (Kurul 2 hattı: meds-kelime-zaman.timer)
--oracle: metin/ses listesi canlı API'den (MEDS_ORACLE_API_URL), ses dosyası boyutu Oracle'dakiyle aynı değilse
  ssh ile birebir alınır; sonuçlar yerelde yazılır ve rsync ile Oracle'a gönderilir (Oracle zayıf ARM, GPU yok).
--gpu (kullanıcı izni 2026-10-20, AGENTS.md §10 dördüncü istisna): YALNIZ meds-gpuguard etkinken; görev döngüsü
  ≈%60 (her parçadan sonra hesap süresinin 2/3'ü kadar bekleme), 72 °C üstü yavaş, 78 °C'de soğuyana (≤64) dek durur,
  CUDA hatasında o oturum CPU'ya döner. Koruyucu ayrıca dondurabilir.
Ortam: MEDS_API (varsayılan http://127.0.0.1:3000), KZ_MODEL (medium), KZ_THREADS (8).
"""
from __future__ import annotations

import os

import sys as _sys

GPU = "--gpu" in _sys.argv
if not GPU:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""  # GPU yasak (AGENTS.md kural 10); --gpu yalnız koruyucuyla

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import unicodedata
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[2] / "data" / "sesli_anlatim"
CIKTI = KOK / "kelime_zaman"
API = os.environ.get("MEDS_API", "http://127.0.0.1:3000")
ORACLE_SSH = os.environ.get("KZ_ORACLE_SSH", "medsor-oracle")
ORACLE_KOK = os.environ.get("KZ_ORACLE_KOK", "medsor/meds/data/sesli_anlatim")  # ev dizinine göre
SES_ONBELLEK = Path(os.environ.get("KZ_SES_ONBELLEK", Path.home() / ".cache" / "meds-kelime-zaman"))
SR = 16000
KELIME_RE = re.compile(r"\S+")

_model = None
_cihaz = "cpu"


def gpu_uygun() -> bool:
    if not GPU or os.environ.get("KZ_GPU_KAPALI"):
        return False
    if subprocess.run(["systemctl", "--user", "is-active", "--quiet", "meds-gpuguard"]).returncode != 0:
        print("meds-gpuguard etkin değil: GPU kullanılmaz, CPU (AGENTS.md §10)", file=sys.stderr, flush=True)
        return False
    return True


def gpu_sicaklik() -> int:
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=5)
        return int(r.stdout.strip().splitlines()[0])
    except Exception:
        return 99  # okunamıyorsa güvenli taraf: kart görünmüyor → bekle/dur


def model():
    global _model, _cihaz
    if _model is None:
        from faster_whisper import WhisperModel
        ad = os.environ.get("KZ_MODEL", "medium")
        if gpu_uygun():
            while gpu_sicaklik() > 62:  # kart ancak ≤62 °C iken açılır
                time.sleep(10)
            try:
                _model = WhisperModel(ad, device="cuda", compute_type="int8_float16")
                _cihaz = "cuda"
                return _model
            except Exception as e:
                print(f"CUDA açılamadı ({e}); CPU", file=sys.stderr, flush=True)
        _model = WhisperModel(ad, device="cpu", compute_type="int8", cpu_threads=int(os.environ.get("KZ_THREADS", "8")))
        _cihaz = "cpu"
    return _model


def cpuya_don():
    global _model
    _model = None
    os.environ["KZ_GPU_KAPALI"] = "1"


def gpu_nefes(hesap_sn: float):
    """%60 görev döngüsü + ısı protokolü (yalnız cuda)."""
    if _cihaz != "cuda":
        return
    time.sleep(hesap_sn * 2 / 3)
    t = gpu_sicaklik()
    if t >= 78:
        while gpu_sicaklik() > 64:
            time.sleep(5)
    elif t > 72:
        time.sleep(hesap_sn * 1.5)


def ffmpeg_yolu() -> str:
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    import imageio_ffmpeg  # type: ignore
    return imageio_ffmpeg.get_ffmpeg_exe()


def coz(mp3: Path) -> np.ndarray:
    r = subprocess.run([ffmpeg_yolu(), "-v", "error", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0


def sade(s: str) -> str:
    """Hizalama için yalnız harf/rakam, küçük, aksansız (ı→i)."""
    s = s.replace("I", "ı").replace("İ", "i").lower().replace("ı", "i")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if c.isalnum() and not unicodedata.combining(c))


def tani(pcm: np.ndarray) -> tuple[str, list[float]]:
    """Tanınan sade harf dizisi + her harfin zamanı (kelime süresine yayılmış)."""
    try:
        return _tani(pcm)
    except RuntimeError as e:
        if _cihaz != "cuda":
            raise
        print(f"CUDA hatası ({e}); bu oturum CPU", file=sys.stderr, flush=True)
        cpuya_don()
        return _tani(pcm)


def _tani(pcm: np.ndarray) -> tuple[str, list[float]]:
    segs, _ = model().transcribe(pcm, language="tr", word_timestamps=True, beam_size=1,
                                 condition_on_previous_text=False, vad_filter=False)
    harf: list[str] = []
    zaman: list[float] = []
    t0 = time.time()
    for s in segs:  # üreteç: her 30 sn'lik parça burada hesaplanır
        gpu_nefes(time.time() - t0)
        t0 = time.time()
        for w in s.words or []:
            h = sade(w.word)
            if not h:
                continue
            a, b = float(w.start), max(float(w.end), float(w.start))
            for k, c in enumerate(h):
                harf.append(c)
                zaman.append(a + (b - a) * k / len(h))
    return "".join(harf), zaman


def paragraf_hizala(metin: str, bas: float, son: float, th: str, tz: list[float], ti0: int, ti1: int) -> list[float]:
    """Paragrafın kelime başlangıçları; th[ti0:ti1] bu paragrafın tanınan harfleri."""
    kel = [m.group(0) for m in KELIME_RE.finditer(metin)]
    if not kel:
        return []
    # metin harfleri ve her harfin ait olduğu kelime
    mh: list[str] = []
    sahip: list[int] = []
    for j, w in enumerate(kel):
        for c in sade(w):
            mh.append(c)
            sahip.append(j)
    zam: list[float | None] = [None] * len(kel)
    if mh and ti1 > ti0:
        sm = SequenceMatcher(None, "".join(mh), th[ti0:ti1], autojunk=False)
        for blk in sm.get_matching_blocks():
            if blk.size < 2:
                continue
            for k in range(blk.size):
                j = sahip[blk.a + k]
                t = tz[ti0 + blk.b + k]
                if zam[j] is None:  # bloklar metin sırasıyla gelir: kelimenin ilk eşleşen harfi
                    zam[j] = t
    # eşleşmeyen kelimeler: karakter oranıyla komşulardan doldur
    uz = [max(1, len(w)) for w in kel]
    birikim = np.cumsum([0] + uz[:-1]).astype(float)
    toplam = float(sum(uz))
    bilinen = [(j, z) for j, z in enumerate(zam) if z is not None]
    sol = [(-1, bas)] + bilinen + [(len(kel), son)]
    out: list[float] = []
    for j in range(len(kel)):
        if zam[j] is not None:
            out.append(zam[j])
            continue
        a = max((x for x in sol if x[0] < j), key=lambda x: x[0])
        b = min((x for x in sol if x[0] > j), key=lambda x: x[0])
        ca = birikim[a[0]] if a[0] >= 0 else -1.0
        cb = birikim[b[0]] if b[0] < len(kel) else toplam
        oran = (birikim[j] - ca) / max(1e-6, cb - ca)
        out.append(a[1] + (b[1] - a[1]) * oran)
    # pencereye kenetle, hep artan (en az 40 ms arayla)
    out[0] = bas if abs(out[0] - bas) > 1.5 else out[0]
    sonuc: list[float] = []
    onceki = bas - 0.05
    for t in out:
        t = min(max(t, onceki + 0.04, bas), son - 0.05)
        sonuc.append(round(t, 2))
        onceki = t
    return sonuc


def varyant_isle(paras: list[dict], z: list, mp3: Path) -> tuple[dict[str, list[float]], str]:
    t0 = time.time()
    pcm = coz(mp3)
    th, tz = tani(pcm)
    tza = np.array(tz)
    p_out: dict[str, list[float]] = {}
    eslesen = toplam = 0
    for p in paras:
        i = p["i"]
        if i >= len(z) or not z[i]:
            continue
        bas, son = float(z[i][0]), float(z[i][1])
        ti0 = int(np.searchsorted(tza, bas - 0.4))
        ti1 = int(np.searchsorted(tza, son + 0.4))
        ts = paragraf_hizala(p["metin"], bas, son, th, tz, ti0, ti1)
        p_out[str(i)] = ts
        toplam += len(ts)
        # ölçüm: tanınan pencerede kaç kelime harfi eşleşti (kaba kalite göstergesi)
        mh = "".join(sade(w) for w in KELIME_RE.findall(p["metin"]))
        if mh and ti1 > ti0:
            eslesen += int(SequenceMatcher(None, mh, th[ti0:ti1], autojunk=False).ratio() * len(ts))
    sure = len(pcm) / SR
    return p_out, f"%{round(100 * eslesen / max(1, toplam))} eşleşme, {round(sure / max(1e-6, time.time() - t0), 1)}× hız"


def api_json(yol: str):
    req = urllib.request.Request(f"{API}{yol}", headers={"User-Agent": "Mozilla/5.0 (meds-kelime-zaman)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def oracle_sesi(key: str, vid: str, bayt: int) -> Path | None:
    """Oracle'daki ses dosyasının birebir aynısı: yerel kopya aynı boyuttaysa o, değilse ssh ile alınır."""
    yerel = KOK / "ses" / key / f"{vid}.mp3"
    if yerel.exists() and yerel.stat().st_size == bayt:
        return yerel
    hedef = SES_ONBELLEK / key / f"{vid}.mp3"
    if hedef.exists() and hedef.stat().st_size == bayt:
        return hedef
    hedef.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["scp", "-q", f"{ORACLE_SSH}:{ORACLE_KOK}/ses/{key}/{vid}.mp3", str(hedef)], capture_output=True)
    return hedef if r.returncode == 0 and hedef.exists() and hedef.stat().st_size == bayt else None


def oracle_gonder() -> str:
    r = subprocess.run(["rsync", "-rlz", "--checksum", "--omit-dir-times", "--no-perms", "--rsync-path=sudo -n rsync", f"{CIKTI}/", f"{ORACLE_SSH}:{ORACLE_KOK}/kelime_zaman/"],
                       capture_output=True, text=True)
    return "Oracle'a gönderildi" if r.returncode == 0 else f"Oracle'a gönderilemedi: {r.stderr.strip()[:200]}"


def ders_isle(key: str, vid_sec: str | None, zorla: bool, kuru: bool, saglayici: str | None = None,
              oracle: bool = False) -> str:
    d = api_json(f"/api/canli-ders/{key}")
    paras = [p for b in d["bolumler"] for p in b["paragraflar"]]
    metin_hash = hashlib.sha1("\n".join(p["metin"] for p in paras).encode("utf-8")).hexdigest()
    hedef = CIKTI / f"{key}.json"
    eski = json.loads(hedef.read_text()) if hedef.exists() else None
    if eski and eski.get("metinHash") != metin_hash:
        eski = None
    sonuc = {"surum": 1, "metinHash": metin_hash, "varyantlar": dict((eski or {}).get("varyantlar") or {})}
    rapor = []
    for v in d["varyantlar"]:
        vid, z = v["id"], v.get("zamanlama")
        if vid_sec and vid != vid_sec:
            continue
        if saglayici and v.get("saglayici") != saglayici:
            continue
        if not z:
            continue
        if oracle:
            bayt = int(v.get("bayt") or 0)
            if not bayt or (not zorla and sonuc["varyantlar"].get(vid, {}).get("bayt") == bayt):
                continue
            mp3 = oracle_sesi(key, vid, bayt)
            if mp3 is None:
                rapor.append(f"{vid}: ses Oracle'dan alınamadı")
                continue
        else:
            mp3 = KOK / "ses" / key / f"{vid}.mp3"
            if not mp3.exists():
                continue
            bayt = mp3.stat().st_size
            if not zorla and sonuc["varyantlar"].get(vid, {}).get("bayt") == bayt:
                continue
        p_out, not_ = varyant_isle(paras, z, mp3)
        sonuc["varyantlar"][vid] = {"bayt": bayt, "p": p_out}
        rapor.append(f"{vid}: {not_}")
        if not kuru:  # her varyanttan sonra yaz: uzun işte kesinti olursa yapılan kaybolmasın
            CIKTI.mkdir(parents=True, exist_ok=True)
            tmp = hedef.with_suffix(".tmp")
            tmp.write_text(json.dumps(sonuc, ensure_ascii=False, separators=(",", ":")))
            tmp.replace(hedef)
    return f"{key}: " + ("; ".join(rapor) if rapor else "güncel")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key")
    ap.add_argument("--vid")
    ap.add_argument("--hepsi", action="store_true")
    ap.add_argument("--saglayici", help="--hepsi ile: yalnız bu sağlayıcının sesleri (ör. ema-yerel)")
    ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--oracle", action="store_true", help="canlı API + Oracle ses dosyaları; sonuç Oracle'a gönderilir")
    ap.add_argument("--gpu", action="store_true", help="yalnız meds-gpuguard etkinken (AGENTS.md §10)")
    a = ap.parse_args()
    global API
    if a.oracle:
        API = os.environ.get("MEDS_ORACLE_API_URL", "https://api.nofrostlife.com.tr").rstrip("/")
    if a.key:
        isler = [(a.key, None)]
    elif a.hepsi:
        keys = [x["key"] for x in api_json("/api/canli-ders")["dersler"]]
        # --saglayici verilirse YALNIZ o sağlayıcı (Kurul 2+: yalnız EMA, kullanıcı kararı 2026-10-20)
        isler = [(k, a.saglayici) for k in keys] if a.saglayici else [(k, None) for k in keys]
    else:
        ap.error("--key ya da --hepsi")
    hata = 0
    for k, sag in isler:
        try:
            sonuc = ders_isle(k, a.vid, a.zorla, a.kuru, sag, a.oracle)
            if not sonuc.endswith(": güncel"):
                print(sonuc, flush=True)
                if a.oracle and not a.kuru:  # her dersten sonra gönder: yapılan iş hemen canlıda
                    print("  " + oracle_gonder(), flush=True)
        except Exception as e:  # tek ders hatası diğerlerini durdurmaz
            hata += 1
            print(f"{k}: HATA {e}", file=sys.stderr, flush=True)
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
