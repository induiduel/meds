#!/usr/bin/env python3
"""Yerel sesli anlatım işçisi: Coqui XTTS v2 ile bu bilgisayarda (yalnız CPU) ders seslendirir.

Akış (sunucu: src/services/sesliAnlatim.ts, sağlayıcı `xtts-yerel`):
  1. Panelde (/manage/sesli-anlatim) bir derse "Coqui XTTS v2 · bu PC" ile Oluştur → iş Oracle kuyruğuna girer.
  2. Bu işçi (systemd --user meds-xtts) dakikada bir POST /api/sesli-anlatim/yerel/al ile iş sorar.
  3. İş gelince ayrı bir süreçte model yüklenir; sunucunun verdiği parçalar (paragraf listeleri) paragraf paragraf
     seslendirilir, her parça MP3 (24 kHz mono 64 kbps CBR) + paragraf zamanlarıyla PUT .../parca/<i> ile yüklenir.
     Paragraf zamanları ölçülür (tahmin değil) → canlı derste metin–PDF–ses eşleşmesi kesin.
  4. Son parçadan sonra POST .../bitir: sunucu birleştirir, eşleşme kapısından geçirir, varyant olarak kaydeder.
     Model süreci kapanır (bellek geri verilir); bekleme döngüsü torch yüklemez.

Yarıda kalan iş (PC kapandı, servis durdu) parçaları sunucuda durduğu için kaldığı parçadan sürer.
Panelden iptal edilirse ya da "Bu PC" işçisi kapatılırsa sentez süreci sonlandırılır.

Kullanım:
  xtts_isci.py bekle                         # servis döngüsü
  xtts_isci.py dene "metin" [--ses AD] [--cikti a.mp3]   # tek seferlik deneme (sunucuya dokunmaz)
Ortam: MEDS_XTTS_SUNUCU (varsayılan MEDS_ORACLE_API_URL ya da https://api.nofrostlife.com.tr),
       MEDS_PANEL_SECRET (.env'den), XTTS_IS_PARCACIGI (torch iş parçacığı, varsayılan 6), XTTS_HIZ (1.2 — Türkçe için önerilen; muhammedsaban/coqui-xtts-v2-turkish-local),
       XTTS_CIHAZ (auto | cuda | cpu), XTTS_GPU_PAY (0.6), XTTS_SICAK_UST (72), XTTS_SICAK_ALT (64), XTTS_SICAK_DUR (78).
GPU: 2026-10-16 02:06'da RTX dizüstü kartı ısı sıçramalarıyla düştü (GSP RPC hatası, yeniden başlatma gerekti) → sınırlar
sıkılaştırıldı ve dış koruyucu (scripts/agents/gpu_guard.py, meds-gpuguard) geri getirildi; aşağıdaki ilk açıklama eski.
GPU: AGENTS.md kural 10'un TEK istisnası (kullanıcı izni 2026-10-16) — en fazla %70: VRAM payı 0.7 ile sınırlı ve
her GPU sentezinden sonra GPU boşta bekletilir (çalışma/toplam ≈ pay). Isı denetimi: GPU 80 °C'yi aşınca pay %20'ye
iner, 70 °C'ye düşünce yeniden %70; 85 °C'de 70 °C'ye inene kadar tamamen durur. GPU yoksa ya da bellek yetmezse CPU'ya düşer;
model ağırlıkları RAM'den yüklenir, metin işleme ve MP3 kodlama CPU'da.
"""
from __future__ import annotations

import os

import base64
import fcntl
import json
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import okunus  # noqa: E402 — kısaltma okunuşu ("de ne a" → "denea"); yalnız modele giden metin
VERI = Path(os.environ.get("MEDS_XTTS_VERI", Path.home() / ".local/share/meds-xtts"))
SR = 24000
KBPS = 64
ARA_SN = 0.6  # paragraf sonu sessizliği (Gemini çıktısıyla aynı)
BOLUM_ONCE_SN = 0.6  # bölüm başı (ilk parça hariç) önde sessizlik
KARAKTER_SN = 14.0  # XTTS Türkçe ~ karakter/sn (süre denetimi için kaba ölçü)


def env_dosyasi() -> dict[str, str]:
    out: dict[str, str] = {}
    f = MEDS / ".env"
    if f.exists():
        for satir in f.read_text(encoding="utf-8").splitlines():
            if "=" in satir and not satir.lstrip().startswith("#"):
                k, v = satir.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out


ENV = env_dosyasi()
SUNUCU = (os.environ.get("MEDS_XTTS_SUNUCU") or ENV.get("MEDS_XTTS_SUNUCU") or ENV.get("MEDS_ORACLE_API_URL") or "https://api.nofrostlife.com.tr").rstrip("/")
SIR = os.environ.get("MEDS_PANEL_SECRET") or ENV.get("MEDS_PANEL_SECRET", "")
ISCI = os.environ.get("MEDS_XTTS_AD") or socket.gethostname()


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def istek(yol: str, govde: dict | bytes | None = None, yontem: str = "POST", basliklar: dict | None = None, zaman_asimi: int = 60):
    h = {"x-panel-secret": SIR, "x-isci": ISCI, "x-saglayici": "xtts-yerel", "User-Agent": "meds-xtts-isci"}
    # sunucunun genel yazma koruması (server.ts): loopback dışından POST/PUT için X-API-Password (ders işçisiyle aynı)
    if os.environ.get("MEDSORU_API_PASSWORD") or ENV.get("MEDSORU_API_PASSWORD"):
        h["X-API-Password"] = os.environ.get("MEDSORU_API_PASSWORD") or ENV["MEDSORU_API_PASSWORD"]
    if isinstance(govde, (bytes, bytearray)):
        veri = bytes(govde)
        h["Content-Type"] = "application/octet-stream"
    else:
        veri = json.dumps({"isci": ISCI, "saglayici": "xtts-yerel", **(govde or {})}).encode()
        h["Content-Type"] = "application/json"
    h.update(basliklar or {})
    req = urllib.request.Request(SUNUCU + yol, data=veri, method=yontem, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=zaman_asimi) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except Exception:
            return e.code, {"error": str(e)}


# ---------------------------------------------------------------- sentez (ağır süreç)

GPU_PAY = min(0.6, float(os.environ.get("XTTS_GPU_PAY", "0.6")))  # kullanıcı sınırı en fazla %60 (2026-10-16)
YAVAS_PAY = 0.25
SICAK_UST = float(os.environ.get("XTTS_SICAK_UST", "72"))  # bunun üstünde yavaşla
SICAK_ALT = float(os.environ.get("XTTS_SICAK_ALT", "64"))  # buna inince tam hız
SICAK_DUR = float(os.environ.get("XTTS_SICAK_DUR", "78"))  # bunun üstünde SICAK_ALT'a inene kadar tamamen bekle
CUDA_HATA_KODU = 5  # sentez süreci GPU düştüğünde bu kodla çıkar: iş sıraya döner, bekle() GPU'yu bekler / CPU'ya geçer
CIHAZ = {"ad": "cpu"}
ISI = {"yavas": False, "olcum": 0.0, "c": None}


def gpu_sicaklik() -> float | None:
    """nvidia-smi ile GPU sıcaklığı (°C); 2 sn önbellek. Okunamazsa None (denetim devre dışı, pay sabit)."""
    if time.time() - ISI["olcum"] < 1:
        return ISI["c"]
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=5).stdout.split()
        ISI["c"] = float(out[0]) if out else None
    except Exception:
        ISI["c"] = None
    ISI["olcum"] = time.time()
    return ISI["c"]


def etkin_pay() -> float:
    """Isı histerezisi: > SICAK_UST → yavaş (YAVAS_PAY), ≤ SICAK_ALT → tam (GPU_PAY); ≥ SICAK_DUR → soğuyana kadar bekle."""
    c = gpu_sicaklik()
    if c is None:
        return GPU_PAY
    if c >= SICAK_DUR:
        log(f"GPU {c:.0f} °C → {SICAK_ALT:.0f} °C'ye inene kadar bekleniyor")
        while (c := gpu_sicaklik()) is not None and c > SICAK_ALT:
            time.sleep(5)
        ISI["yavas"] = False
        log(f"GPU {c} °C → tam hız")
    elif c > SICAK_UST and not ISI["yavas"]:
        ISI["yavas"] = True
        log(f"GPU {c:.0f} °C > {SICAK_UST:.0f} → yavaş mod (pay %{int(YAVAS_PAY * 100)})")
    elif c <= SICAK_ALT and ISI["yavas"]:
        ISI["yavas"] = False
        log(f"GPU {c:.0f} °C ≤ {SICAK_ALT:.0f} → tam hız (pay %{int(GPU_PAY * 100)})")
    return YAVAS_PAY if ISI["yavas"] else GPU_PAY


def model_yukle():
    import torch

    torch.set_num_threads(int(os.environ.get("XTTS_IS_PARCACIGI", "6")))
    os.environ.setdefault("COQUI_TOS_AGREED", "1")  # CPML (ticari olmayan) — kullanıcı 2026-10-16'da kabul etti
    from TTS.api import TTS

    istek_cihaz = os.environ.get("XTTS_CIHAZ", "auto")
    gpu = istek_cihaz in ("auto", "cuda") and torch.cuda.is_available()
    t = time.time()
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
    if gpu:
        try:
            torch.cuda.set_per_process_memory_fraction(GPU_PAY, 0)
            tts.to("cuda")
            CIHAZ["ad"] = "cuda"
        except Exception as e:  # VRAM yetmedi / sürücü sorunu
            log("GPU'ya alınamadı, CPU ile sürüyor:", e)
            gpu_birak(tts)
    log(f"model hazır: {CIHAZ['ad']} ({time.time() - t:.0f} sn; GPU payı %{int(GPU_PAY * 100)})")
    return tts


def gpu_birak(tts):
    import torch

    tts.to("cpu")
    CIHAZ["ad"] = "cpu"
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def tts_cagir(tts, **kw):
    """GPU'da: sentezden sonra GPU'yu (1-pay)/pay katı kadar boşta bırakır → ortalama kullanım ≈ pay (ısıya göre).
    GPU belleği taşarsa model CPU'ya alınır ve iş orada sürer."""
    import torch

    if CIHAZ["ad"] == "cuda":
        pay = etkin_pay()
        t = time.time()
        try:
            wav = tts.tts(**kw)
            torch.cuda.synchronize()
        except torch.cuda.OutOfMemoryError:
            log("GPU belleği yetmedi (pay %d) → CPU'ya geçiliyor" % int(GPU_PAY * 100))
            gpu_birak(tts)
            return tts.tts(**kw)
        except Exception as e:  # "unspecified launch failure", Xid: GPU düştü — bu süreçte CUDA artık kullanılamaz
            if "CUDA" in str(e) or "cuda" in type(e).__name__.lower() or "Accelerator" in type(e).__name__:
                log(f"GPU hatası: {str(e)[:160]} → iş sıraya bırakılıyor")
                os._exit(CUDA_HATA_KODU)
            raise
        # boşta bekleme: ortalama kullanım ≈ pay; sonrasında sıcaklık yeniden ölçülür (sıçrama cümle sırasında olur)
        time.sleep((time.time() - t) * (1 - pay) / pay)
        ISI["olcum"] = 0.0
        return wav
    return tts.tts(**kw)


def sessiz_kirp(x, esik=0.012, pay=0.08):
    """Baştaki/sondaki sessizliği kırpar (pay kadar bırakır)."""
    import numpy as np

    a = np.abs(x)
    idx = np.where(a > esik)[0]
    if not len(idx):
        return x
    p = int(pay * SR)
    return x[max(0, idx[0] - p): min(len(x), idx[-1] + p)]


CUMLE_SINIRI = 200  # XTTS Türkçe sınırı 226 karakter; aşan cümle sessizce kesilebiliyor


def cumlelere_bol(metin: str) -> list[str]:
    """Paragrafı ≤ CUMLE_SINIRI karakterlik parçalara böler: önce cümle sonu, uzun cümlede ; : , ve en son boşluk."""
    import re

    out: list[str] = []

    def ekle(c: str, ayiricilar: tuple[str, ...]):
        c = c.strip()
        if not c:
            return
        if len(c) <= CUMLE_SINIRI:
            out.append(c)
            return
        for ay in ayiricilar:
            parcalar = [x for x in re.split(f"(?<={re.escape(ay)})\\s+", c) if x.strip()]
            if len(parcalar) > 1:
                tampon = ""
                for x in parcalar:
                    if tampon and len(tampon) + 1 + len(x) > CUMLE_SINIRI:
                        ekle(tampon, ayiricilar[ayiricilar.index(ay) + 1:])
                        tampon = x
                    else:
                        tampon = f"{tampon} {x}".strip()
                ekle(tampon, ayiricilar[ayiricilar.index(ay) + 1:])
                return
        kelimeler, tampon = c.split(), ""
        for k in kelimeler:
            if tampon and len(tampon) + 1 + len(k) > CUMLE_SINIRI:
                out.append(tampon)
                tampon = k
            else:
                tampon = f"{tampon} {k}".strip()
        if tampon:
            out.append(tampon)

    for cumle in re.split(r"(?<=[.!?…])\s+", metin.strip()):
        ekle(cumle, (";", ":", ","))
    return out


def cumle_seslendir(tts, metin: str, ses: str):
    """Tek cümle → float32. Süre metne göre tutarsızsa (XTTS'in bazen uzattığı/yuttuğu çıktı) 3 kez dener."""
    import numpy as np

    hiz = float(os.environ.get("XTTS_HIZ", "1.2"))  # Türkçe için önerilen hız (coqui-xtts-v2-turkish-local)
    beklenen = max(0.6, len(metin) / (KARAKTER_SN * hiz))
    en_iyi = None
    for deneme in range(1, 4):
        wav = np.asarray(tts_cagir(tts, text=metin, speaker=ses, language="tr", split_sentences=False, speed=hiz), dtype=np.float32)
        wav = sessiz_kirp(wav)
        oran = (len(wav) / SR) / beklenen
        if 0.45 <= oran <= 2.2:
            return wav, None
        if en_iyi is None or abs(np.log(oran)) < abs(np.log(en_iyi[1])):
            en_iyi = (wav, oran)
    return en_iyi[0], f"süre oranı {en_iyi[1]:.2f} (3 denemede düzelmedi): {metin[:60]}…"


def paragraf_seslendir(tts, metin: str, ses: str):
    """Paragraf → cümle cümle seslendirilip kısa duraklarla birleştirilir; notlar sorunlu cümleleri listeler."""
    import numpy as np

    durak = np.zeros(int(0.18 * SR), dtype=np.float32)
    parcalar, notlar = [], []
    metin = okunus.duzelt(metin)  # paragraf/zamanlama değişmez: paragraf yine tek parça ölçülür
    for c in cumlelere_bol(metin):
        wav, not_ = cumle_seslendir(tts, c, ses)
        if not_:
            notlar.append(not_)
        parcalar += [wav, durak]
    return np.concatenate(parcalar[:-1] or [durak]), ("; ".join(notlar) or None)


def mp3_kodla(pcm16: bytes) -> bytes:
    import lameenc

    enc = lameenc.Encoder()
    enc.set_bit_rate(KBPS)
    enc.set_in_sample_rate(SR)
    enc.set_channels(1)
    enc.set_quality(2)
    mp3 = bytes(enc.encode(pcm16) + enc.flush())
    return xing_at(mp3)


def xing_at(mp3: bytes) -> bytes:
    """İlk kare Xing/Info başlığıysa atar: parçalar art arda eklendiğinde oynatıcı süreyi ilk parçadan okumasın."""
    if len(mp3) < 4 or mp3[0] != 0xFF or (mp3[1] & 0xE0) != 0xE0:
        return mp3
    surum = (mp3[1] >> 3) & 3  # 3: MPEG1, 2: MPEG2, 0: MPEG2.5
    br_idx = (mp3[2] >> 4) & 0xF
    sr_idx = (mp3[2] >> 2) & 3
    dolgu = (mp3[2] >> 1) & 1
    br_m1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
    br_m2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]
    sr_tab = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}
    if surum == 1 or sr_idx == 3 or br_idx in (0, 15):
        return mp3
    br = (br_m1 if surum == 3 else br_m2)[br_idx] * 1000
    sr = sr_tab[surum][sr_idx]
    boy = (144 if surum == 3 else 72) * br // sr + dolgu
    if b"Xing" in mp3[:boy] or b"Info" in mp3[:boy]:
        return mp3[boy:]
    return mp3


def parca_uret(tts, parca: dict, ilk: bool, ses: str):
    import numpy as np

    sessiz = lambda sn: np.zeros(int(round(sn * SR)), dtype=np.float32)  # noqa: E731
    parcalar = []
    zaman = []
    notlar = []
    t = 0.0
    if parca["bolumBasi"] and not ilk:
        parcalar.append(sessiz(BOLUM_ONCE_SN))
        t += BOLUM_ONCE_SN
    for j, par in enumerate(parca["paragraflar"]):
        wav, not_ = paragraf_seslendir(tts, par, ses)
        if not_:
            notlar.append(f"paragraf {j + 1}: {not_}")
        bas = t
        t += len(wav) / SR
        zaman.append([bas, t])
        parcalar += [wav, sessiz(ARA_SN)]
        t += ARA_SN
    x = np.concatenate(parcalar)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    mp3 = mp3_kodla(pcm)
    gercek = len(mp3) * 8 / (KBPS * 1000)
    k = gercek / (len(x) / SR)  # kodlayıcı dolgusu: zamanları gerçek MP3 süresine ölçekle
    zaman = [[round(a * k, 3), round(b * k, 3)] for a, b in zaman]
    return mp3, zaman, gercek, notlar


def sentezle(is_dosyasi: str) -> int:
    j = json.loads(Path(is_dosyasi).read_text(encoding="utf-8"))
    is_ = j["is"]
    ses = is_["ses"]
    parcalar = j["parcalar"]
    mevcut = set(j.get("mevcut") or [])
    tts = model_yukle()
    if ses not in (getattr(tts, "speakers", None) or [ses]):
        raise SystemExit(f"XTTS konuşmacısı yok: {ses}")
    toplam = len(parcalar)
    for i, p in enumerate(parcalar):
        if i in mevcut:
            continue
        t0 = time.time()
        mp3, zaman, sure, notlar = parca_uret(tts, p, i == 0, ses)
        meta = {"sure": sure, "zaman": zaman, "metinHash": j["metinHash"], "not": "; ".join(notlar) or None}
        for deneme in range(1, 6):
            try:
                kod, cevap = istek(
                    f"/api/sesli-anlatim/yerel/is/{is_['id']}/parca/{i}", mp3, "PUT",
                    {"x-parca-meta": base64.b64encode(json.dumps(meta).encode()).decode(), "Content-Type": "audio/mpeg"}, 180,
                )
            except Exception as e:  # ağ kopması: bekle, yeniden dene
                kod, cevap = 0, {"error": str(e)}
            if kod == 200:
                break
            if kod in (400, 404, 409, 422):
                log(f"parça {i + 1} reddedildi: {cevap}")
                return 2 if kod != 409 else 3
            log(f"parça {i + 1} yüklenemedi ({kod}): {cevap}; {deneme}. deneme")
            time.sleep(15 * deneme)
        else:
            return 4
        log(f"{is_['key']} parça {i + 1}/{toplam}: {sure:.0f} sn ses, {time.time() - t0:.0f} sn'de (RTF {(time.time() - t0) / max(sure, 1):.2f})")
    kod, cevap = istek(f"/api/sesli-anlatim/yerel/is/{is_['id']}/bitir", {}, zaman_asimi=300)
    if kod != 200:
        log(f"birleştirme reddedildi ({kod}): {cevap}")
        return 2
    log(f"{is_['key']} bitti ✔")
    return 0


# ---------------------------------------------------------------- bekleme döngüsü (hafif süreç)

cocuk: subprocess.Popen | None = None
calisan_is: str | None = None


def kapat(_sig=None, _frm=None):
    if cocuk and cocuk.poll() is None:
        cocuk.terminate()
        try:
            cocuk.wait(30)
        except subprocess.TimeoutExpired:
            cocuk.kill()
    if calisan_is:
        try:
            istek(f"/api/sesli-anlatim/yerel/is/{calisan_is}/hata", {"birak": True}, zaman_asimi=15)
        except Exception:
            pass
    sys.exit(0)


GPU_BASLA_SICAK = float(os.environ.get("XTTS_GPU_BASLA", "62"))  # sentez süreci GPU'yu ancak bu sıcaklığın altında açar


def gpu_kapisi(cpu_zorla: bool) -> dict:
    """Sentez sürecinin ortamı. GPU kartı görünmüyorsa ya da bu oturumda bir kez düştüyse CPU; görünüyorsa ≤ GPU_BASLA_SICAK
    olana kadar bekler (dış koruyucu meds-gpuguard ayrıca sentez sürecini dondurur)."""
    env = dict(os.environ)
    if cpu_zorla or os.environ.get("XTTS_CIHAZ") == "cpu":
        env.update(XTTS_CIHAZ="cpu", CUDA_VISIBLE_DEVICES="")
        return env
    # GPU koruyucu bu açılışta saat kilidinin olmadığını gördüyse (meds_temp/state/gpu_kilit_yok = açılış kimliği) yalnız CPU
    try:
        bayrak = (MEDS.parent / "meds_temp/state/gpu_kilit_yok").read_text().strip()
        if bayrak and bayrak == Path("/proc/sys/kernel/random/boot_id").read_text().strip():
            log("GPU saat kilidi yok (koruyucu) → bu açılışta CPU")
            env.update(XTTS_CIHAZ="cpu", CUDA_VISIBLE_DEVICES="")
            return env
    except FileNotFoundError:
        pass
    for _ in range(120):  # en çok ~10 dk
        ISI["olcum"] = 0.0
        c = gpu_sicaklik()
        if c is None:
            log("GPU görünmüyor (nvidia-smi) → bu iş CPU'da")
            env.update(XTTS_CIHAZ="cpu", CUDA_VISIBLE_DEVICES="")
            return env
        if c <= GPU_BASLA_SICAK:
            return env
        time.sleep(5)
    log(f"GPU 10 dk'da {GPU_BASLA_SICAK:.0f} °C'ye inmedi → bu iş CPU'da")
    env.update(XTTS_CIHAZ="cpu", CUDA_VISIBLE_DEVICES="")
    return env


def bekle() -> None:
    global cocuk, calisan_is
    gpu_dustu = False  # bu oturumda GPU bir kez düştüyse (CUDA hatası) bir daha GPU açılmaz — işçi elle yeniden başlatılmalı
    if not SIR:
        raise SystemExit("MEDS_PANEL_SECRET yok (.env)")
    VERI.mkdir(parents=True, exist_ok=True)
    kilit = open(VERI / "isci.lock", "w")
    try:
        fcntl.flock(kilit, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit("başka bir xtts işçisi çalışıyor")
    signal.signal(signal.SIGTERM, kapat)
    signal.signal(signal.SIGINT, kapat)
    log(f"XTTS işçisi: {ISCI} → {SUNUCU}")
    while True:
        try:
            kod, cevap = istek("/api/sesli-anlatim/yerel/al", {}, zaman_asimi=60)
        except Exception as e:
            log("sunucuya ulaşılamadı:", e)
            time.sleep(120)
            continue
        is_ = cevap.get("is") if kod == 200 else None
        if kod != 200:
            log(f"al: {kod} {cevap}")
        if not is_:
            time.sleep(60)
            continue
        calisan_is = is_["id"]
        log(f"iş alındı: {is_['key']} · {is_['ses']} · {len(cevap['mevcut'])}/{len(cevap['parcalar'])} parça hazır")
        f = VERI / "is" / f"{is_['id']}.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(cevap, ensure_ascii=False), encoding="utf-8")
        cocuk = subprocess.Popen([sys.executable, __file__, "sentezle", str(f)], env=gpu_kapisi(gpu_dustu))
        durduruldu = False
        while cocuk.poll() is None:
            time.sleep(45)
            try:
                _, k = istek("/api/sesli-anlatim/yerel/kalp", {"isId": calisan_is}, zaman_asimi=30)
                if k.get("dur") and cocuk.poll() is None:
                    log("panelden durduruldu/iptal edildi → sentez sonlandırılıyor")
                    durduruldu = True
                    cocuk.terminate()
                    cocuk.wait(60)
            except Exception as e:
                log("kalp atışı gönderilemedi:", e)
        rc = cocuk.returncode
        cocuk = None
        if rc == CUDA_HATA_KODU:
            gpu_dustu = True
            log("GPU düştü: iş sıraya bırakıldı (parçalar korunur); bu oturumda bundan sonra yalnız CPU")
            istek(f"/api/sesli-anlatim/yerel/is/{calisan_is}/hata", {"birak": True})
        elif not durduruldu and rc not in (0, 3):
            istek(f"/api/sesli-anlatim/yerel/is/{calisan_is}/hata", {"hata": f"yerel sentez süreci {rc} koduyla bitti (journalctl --user -u meds-xtts)"})
        if durduruldu:
            istek(f"/api/sesli-anlatim/yerel/is/{calisan_is}/hata", {"birak": True})
        calisan_is = None
        f.unlink(missing_ok=True)
        time.sleep(5)


def dene(metin: str, ses: str, cikti: str) -> None:
    tts = model_yukle()
    t = time.time()
    mp3, zaman, sure, notlar = parca_uret(tts, {"paragraflar": [metin], "bolumBasi": False}, True, ses)
    Path(cikti).write_bytes(mp3)
    log(f"{cikti}: {sure:.1f} sn ses, {time.time() - t:.1f} sn'de (RTF {(time.time() - t) / sure:.2f}) {notlar or ''}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["bekle"]:
        bekle()
    elif a[:1] == ["sentezle"] and len(a) == 2:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(3))
        sys.exit(sentezle(a[1]))
    elif a[:1] == ["dene"] and len(a) >= 2:
        ses = a[a.index("--ses") + 1] if "--ses" in a else "Chandra MacFarland"
        cikti = a[a.index("--cikti") + 1] if "--cikti" in a else "xtts_deneme.mp3"
        dene(a[1], ses, cikti)
    else:
        print(__doc__)
        sys.exit(1)
