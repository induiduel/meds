#!/usr/bin/env python3
"""Yerel sesli anlatım işçisi: EMA Lightning (canberkkkkkk/ema-lightning, Apache 2.0) ile bu bilgisayarda YALNIZ CPU.

Tek sabit Türkçe ses ("Ema"), 8.6M parametre / ~34 MB; CPU'da 4 iş parçacığıyla ~20-25× gerçek zaman, ~0,9 GB RAM.
GPU kullanılmaz (AGENTS.md kural 10): CUDA_VISIBLE_DEVICES="" torch yüklenmeden önce zorlanır.

Akış (sunucu: src/services/sesliAnlatim.ts, sağlayıcı `ema-yerel`; protokol XTTS işçisiyle aynı):
  1. Panelde (/manage/sesli-anlatim) bir derse "EMA Lightning · bu PC" ile Oluştur → iş Oracle kuyruğuna girer.
  2. Bu işçi (systemd --user meds-ema) dakikada bir POST /api/sesli-anlatim/yerel/al {saglayici: ema-yerel} ile iş sorar.
  3. İş gelince ayrı süreçte model yüklenir; parçalar paragraf paragraf seslendirilir, her parça MP3 (24 kHz mono
     64 kbps CBR) + ÖLÇÜLMÜŞ paragraf zamanlarıyla PUT .../parca/<i> ile yüklenir (metin–PDF–ses eşleşmesi kesin).
  4. Son parçadan sonra POST .../bitir: sunucu birleştirir, eşleşme kapısından geçirir, varyant olarak kaydeder.

Kullanım:
  ema_isci.py bekle                              # servis döngüsü
  ema_isci.py dene "metin" [--cikti a.mp3]       # tek seferlik deneme (sunucuya dokunmaz)
Ortam: MEDS_EMA_SUNUCU (varsayılan MEDS_ORACLE_API_URL ya da https://api.nofrostlife.com.tr), MEDS_PANEL_SECRET (.env),
       EMA_IS_PARCACIGI (torch iş parçacığı, 4), EMA_HIZ (konuşma hızı 0.25–4, 1.0), MEDS_EMA_AD (işçi adı).
"""
from __future__ import annotations

import os

# GPU yasak — torch'tan önce. Tek istisna (kullanıcı, 2026-10-18): EMA_CIHAZ=cuda + meds-gpuguard etkin + saat kilidi
# (sudo nvidia-smi -lgc 300,1500); VRAM payı 0,6, koruyucu %60/ısı protokolüyle dondurur.
GPU = os.environ.get("EMA_CIHAZ") == "cuda" and os.system("systemctl --user is-active --quiet meds-gpuguard") == 0
if not GPU:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

import base64
import fcntl
import json
import re
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
import okunus  # noqa: E402 — kısaltma okunuşu düzeltmesi
VERI = Path(os.environ.get("MEDS_EMA_VERI", Path.home() / ".local/share/meds-ema"))
SAGLAYICI = "ema-yerel"
SR = 24000
KBPS = 64
ARA_SN = 0.6  # paragraf sonu sessizliği (XTTS/Gemini çıktısıyla aynı)
BOLUM_ONCE_SN = 0.6  # bölüm başı (ilk parça hariç) önde sessizlik
KARAKTER_SN = 18.0  # EMA hız 1.0'da Türkçe ~ karakter/sn (ders metninde ölçüldü; süre denetimi için)


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
SUNUCU = (os.environ.get("MEDS_EMA_SUNUCU") or ENV.get("MEDS_EMA_SUNUCU") or ENV.get("MEDS_ORACLE_API_URL") or "https://api.nofrostlife.com.tr").rstrip("/")
SIR = os.environ.get("MEDS_PANEL_SECRET") or ENV.get("MEDS_PANEL_SECRET", "")
ISCI = os.environ.get("MEDS_EMA_AD") or f"{socket.gethostname()}-ema"
HIZ = min(4.0, max(0.25, float(os.environ.get("EMA_HIZ", "1.0"))))


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def istek(yol: str, govde: dict | bytes | None = None, yontem: str = "POST", basliklar: dict | None = None, zaman_asimi: int = 60):
    h = {"x-panel-secret": SIR, "x-isci": ISCI, "x-saglayici": SAGLAYICI, "User-Agent": "meds-ema-isci"}
    # sunucunun genel yazma koruması (server.ts): loopback dışından POST/PUT için X-API-Password (ders işçisiyle aynı)
    if os.environ.get("MEDSORU_API_PASSWORD") or ENV.get("MEDSORU_API_PASSWORD"):
        h["X-API-Password"] = os.environ.get("MEDSORU_API_PASSWORD") or ENV["MEDSORU_API_PASSWORD"]
    if isinstance(govde, (bytes, bytearray)):
        veri = bytes(govde)
        h["Content-Type"] = "application/octet-stream"
    else:
        veri = json.dumps({"isci": ISCI, "saglayici": SAGLAYICI, **(govde or {})}).encode()
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


def model_yukle():
    import torch

    torch.set_num_threads(int(os.environ.get("EMA_IS_PARCACIGI", "4")))
    from ema_lightning import EMA

    t = time.time()
    cihaz = "cpu"
    if GPU and torch.cuda.is_available():
        torch.cuda.set_per_process_memory_fraction(0.6)
        cihaz = "cuda"
    tts = EMA(device=cihaz)
    log(f"EMA Lightning hazır: {cihaz} ({time.time() - t:.0f} sn, {torch.get_num_threads()} iş parçacığı, hız {HIZ})")
    return tts


def sessiz_kirp(x, esik=0.012, pay=0.08):
    """Baştaki/sondaki sessizliği kırpar (pay kadar bırakır)."""
    import numpy as np

    a = np.abs(x)
    idx = np.where(a > esik)[0]
    if not len(idx):
        return x
    p = int(pay * SR)
    return x[max(0, idx[0] - p): min(len(x), idx[-1] + p)]


UZUN_KISALTMA = False  # iş başına ayarlanır: Kurul 2+ anahtarları (k2-…, k2p-…) True
MODUL_OKUNUS = False  # modül dersleri (TBG Sınav Kampı): ekrandaki standart yazım (BRCA1, PAPP-A) → modul_okunus.py


def uzun_kisaltma_ayarla(anahtar: str) -> None:
    global UZUN_KISALTMA, MODUL_OKUNUS
    import modul_okunus
    UZUN_KISALTMA = bool(re.match(r"k[2-6](p-k[2-6])?-", str(anahtar or "")))
    MODUL_OKUNUS = modul_okunus.modul_mu(str(anahtar or ""))


def _ks():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "patoloji_cozucu"))
    import kisaltma_ses
    return kisaltma_ses


def paragraf_seslendir(tts, metin: str):
    """Bir paragraf → float32 dizi (24 kHz). Süre metne göre tutarsızsa farklı tohumla 3 kez dener."""
    import numpy as np

    # Kısaltma okunuşu — yalnız modele giden metin; paragraf/zamanlama değişmez.
    # Kurul 2+ (UZUN_KISALTMA): fonetik terimler + ünlüsü uzatılmış harf adları ("dee nee aa"); birleşik "denea" EMA'da
    # kelime gibi okunuyordu ("deneye", 2026-10-17 ölçümü, KURUL2_YAPILMAYACAK_HATALAR H3). Kurul 1 eski yolda.
    if MODUL_OKUNUS:
        import modul_okunus
        metin = modul_okunus.donustur(metin)
    elif UZUN_KISALTMA:
        for pat, fon in okunus.FONETIK_TTS:
            metin = pat.sub(fon, metin)
        metin = _ks().uzat(metin)
    else:
        metin = okunus.duzelt(metin)
    beklenen = max(1.0, len(metin) / (KARAKTER_SN * HIZ))
    en_iyi = None
    for deneme in range(3):
        s = tts.say(metin, speed=HIZ, seed=deneme, sample_rate=SR)
        wav = sessiz_kirp(np.asarray(s.audio, dtype=np.float32))
        sure = len(wav) / SR
        oran = sure / beklenen
        if 0.55 <= oran <= 1.8:
            return wav, None
        log(f"  süre tutarsız (deneme {deneme + 1}): {sure:.1f} sn, beklenen ~{beklenen:.1f}")
        if en_iyi is None or abs(np.log(oran)) < abs(np.log(en_iyi[1])):
            en_iyi = (wav, oran)
    return en_iyi[0], f"süre oranı {en_iyi[1]:.2f} (3 denemede düzelmedi)"


def mp3_kodla(pcm16: bytes) -> bytes:
    import lameenc

    enc = lameenc.Encoder()
    enc.set_bit_rate(KBPS)
    enc.set_in_sample_rate(SR)
    enc.set_channels(1)
    enc.set_quality(2)
    return xing_at(bytes(enc.encode(pcm16) + enc.flush()))


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


def parca_uret(tts, parca: dict, ilk: bool):
    import numpy as np

    sessiz = lambda sn: np.zeros(int(round(sn * SR)), dtype=np.float32)  # noqa: E731
    parcalar, zaman, notlar = [], [], []
    t = 0.0
    if parca["bolumBasi"] and not ilk:
        parcalar.append(sessiz(BOLUM_ONCE_SN))
        t += BOLUM_ONCE_SN
    for j, par in enumerate(parca["paragraflar"]):
        wav, not_ = paragraf_seslendir(tts, par)
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
    parcalar = j["parcalar"]
    mevcut = set(j.get("mevcut") or [])
    # okunuş ayarı bu (alt) süreçte de yapılmalı: üst süreçteki ayar buraya taşınmaz
    uzun_kisaltma_ayarla(is_.get("key", ""))
    tts = model_yukle()
    toplam = len(parcalar)
    for i, p in enumerate(parcalar):
        if i in mevcut:
            continue
        t0 = time.time()
        mp3, zaman, sure, notlar = parca_uret(tts, p, i == 0)
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
        sn = time.time() - t0
        log(f"{is_['key']} parça {i + 1}/{toplam}: {sure:.0f} sn ses, {sn:.0f} sn'de (RTF {sn / max(sure, 1):.3f})")
    kod, cevap = istek(f"/api/sesli-anlatim/yerel/is/{is_['id']}/bitir", {}, zaman_asimi=300)
    if kod != 200:
        log(f"birleştirme reddedildi ({kod}): {cevap}")
        return 2
    log(f"{is_['key']} bitti ✔")
    return 0


# ---------------------------------------------------------------- bekleme döngüsü (hafif süreç, torch yüklemez)

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


def bekle() -> None:
    global cocuk, calisan_is
    if not SIR:
        raise SystemExit("MEDS_PANEL_SECRET yok (.env)")
    VERI.mkdir(parents=True, exist_ok=True)
    kilit = open(VERI / "isci.lock", "w")
    try:
        fcntl.flock(kilit, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit("başka bir EMA işçisi çalışıyor")
    signal.signal(signal.SIGTERM, kapat)
    signal.signal(signal.SIGINT, kapat)
    log(f"EMA işçisi: {ISCI} → {SUNUCU}")
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
        if is_.get("ses") != "Ema":  # sunucu `saglayici` alanını tanımıyor (eski sürüm) → XTTS işini geri bırak
            log(f"EMA'ya ait olmayan iş geldi ({is_.get('ses')}); sunucu güncel değil, bırakılıyor")
            istek(f"/api/sesli-anlatim/yerel/is/{is_['id']}/hata", {"birak": True})
            time.sleep(600)
            continue
        calisan_is = is_["id"]
        uzun_kisaltma_ayarla(is_['key'])
        log(f"iş alındı: {is_['key']} · {len(cevap['mevcut'])}/{len(cevap['parcalar'])} parça hazır")
        f = VERI / "is" / f"{is_['id']}.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(cevap, ensure_ascii=False), encoding="utf-8")
        cocuk = subprocess.Popen([sys.executable, __file__, "sentezle", str(f)])
        durduruldu = False
        while cocuk.poll() is None:
            time.sleep(20)
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
        if not durduruldu and rc not in (0, 3):
            istek(f"/api/sesli-anlatim/yerel/is/{calisan_is}/hata", {"hata": f"yerel sentez süreci {rc} koduyla bitti (journalctl --user -u meds-ema)"})
        if durduruldu:
            istek(f"/api/sesli-anlatim/yerel/is/{calisan_is}/hata", {"birak": True})
        calisan_is = None
        f.unlink(missing_ok=True)
        time.sleep(5)


def dene(metin: str, cikti: str) -> None:
    tts = model_yukle()
    t = time.time()
    mp3, zaman, sure, notlar = parca_uret(tts, {"paragraflar": [p for p in metin.split("\n") if p.strip()], "bolumBasi": False}, True)
    Path(cikti).write_bytes(mp3)
    log(f"{cikti}: {sure:.1f} sn ses, {time.time() - t:.1f} sn'de (RTF {(time.time() - t) / sure:.3f}) zaman={zaman} {notlar or ''}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["bekle"]:
        # Kullanıcı kararı (2026-10-22): Oracle'daki EMA işçisine (meds-ema konteyneri, MEDS_EMA_AD=oracle-ema) iş verilmez;
        # EMA işleri yalnız bu bilgisayardaki meds-ema birimiyle üretilir.
        if ISCI == "oracle-ema" or os.path.exists("/.dockerenv"):
            print("Oracle EMA işçisi kapalı (kullanıcı kararı 2026-10-22); işler yalnız yerel bilgisayarda üretilir.")
            sys.exit(0)
        bekle()
    elif a[:1] == ["sentezle"] and len(a) == 2:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(3))
        sys.exit(sentezle(a[1]))
    elif a[:1] == ["dene"] and len(a) >= 2:
        cikti = a[a.index("--cikti") + 1] if "--cikti" in a else "ema_deneme.mp3"
        dene(a[1], cikti)
    else:
        print(__doc__)
        sys.exit(1)
