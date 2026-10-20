#!/usr/bin/env python3
"""
Sesli ders → MP4 video (yerel GPU, yalnız yönetici isteğiyle). Öğrencilerin tarayıcıda ürettiği videonun (src/components/
canliDers/cdVideo.ts) aynısı: o an okunan PDF slaytı (pdf_isaret kutuları: okunan satır + kelime), altta kelime kelime
vurgulu cümle, ilerleme çubuğu; PDF'in HER sayfası zaman çizelgesinde (anlatılmayanlar önceki slaytın sonuna kısa süre).

GPU kuralları (AGENTS.md §10 beşinci istisna, kullanıcı izni 2026-10-20):
  * yalnız meds-gpuguard etkin ve bu açılışta saat kilidi sorunu işaretlenmemişken (meds_temp/state/gpu_kilit_yok);
  * kodlama ffmpeg h264_nvenc; çizim CPU'da (PIL + PyMuPDF). Koruyucu `video_uret.py uret` sürecini SIGSTOP ile dondurur →
    boru durur → NVENC boşa düşer (ısı/%60 görev döngüsü protokolü aynen geçerli);
  * GPU hazır değilse iş alınmaz (CPU'ya düşülmez: 4K CPU kodlaması makineyi kilitler).

Kullanım:
  video_uret.py bekle                       # işçi döngüsü (systemd: meds-ders-video.service)
  video_uret.py uret --key K --vid V --coz 1080p --cikti out.mp4 [--sn 60]   # tek video (deneme: --sn)
Ortam: MEDS_ORACLE_API_URL (kuyruk), MEDS_PANEL_SECRET (.env), MEDS_YEREL_API (http://127.0.0.1:3000; ders verisi + PDF),
       DERS_VIDEO_ORACLE_SSH (medsor-oracle), DERS_VIDEO_FFMPEG (ffmpeg)
"""
from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
TEMP = MEDS.parent / "meds_temp"
ENV: dict[str, str] = {}
try:
    for l in (MEDS / ".env").read_text().splitlines():
        m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*\"?(.*?)\"?\s*$", l)
        if m:
            ENV[m.group(1)] = m.group(2)
except Exception:
    pass
YEREL = os.environ.get("MEDS_YEREL_API", "http://127.0.0.1:3000").rstrip("/")
ORACLE = (os.environ.get("MEDS_ORACLE_API_URL") or ENV.get("MEDS_ORACLE_API_URL") or "https://api.nofrostlife.com.tr").rstrip("/")
SIR = os.environ.get("MEDS_PANEL_SECRET") or ENV.get("MEDS_PANEL_SECRET", "")
API_SIFRE = os.environ.get("MEDSORU_API_PASSWORD") or ENV.get("MEDSORU_API_PASSWORD", "")  # canlıda yazma isteği kapısı
SSH = os.environ.get("DERS_VIDEO_ORACLE_SSH", "medsor-oracle")
UZAK_CIKTI = "/home/ubuntu/medsor/meds/data/ders_video/cikti"
FFMPEG = os.environ.get("DERS_VIDEO_FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
GIRIS_FPS = 20  # çizim örnekleme (kelime vurgusu 50 ms çözünürlük); çıkış 60 fps (ffmpeg fps süzgeci kareyi çoğaltır)
BOYUT = {"720p": (1280, 720, "4M"), "1080p": (1920, 1080, "8M"), "2k": (2560, 1440, "14M"), "4k": (3840, 2160, "28M")}
LOG = TEMP / "logs" / "ders_video.log"


def log(m: str):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ——— GPU hazır mı (AGENTS.md §10) ———
def gpu_hazir() -> tuple[bool, str]:
    if subprocess.run(["systemctl", "--user", "is-active", "--quiet", "meds-gpuguard"]).returncode != 0:
        return False, "meds-gpuguard etkin değil"
    try:
        boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        k = TEMP / "state" / "gpu_kilit_yok"
        if k.exists() and k.read_text().strip() == boot:
            return False, "saat kilidi yok (sudo nvidia-smi -lgc 300,1500)"
    except Exception:
        pass
    try:
        enc = subprocess.run([FFMPEG, "-hide_banner", "-encoders"], capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return False, "ffmpeg yok (sudo apt install ffmpeg)"
    if "h264_nvenc" not in enc:
        return False, "ffmpeg NVENC desteksiz (sudo apt install ffmpeg)"
    return True, "nvenc"


# ——— veri ———
def getir(url: str, hedef: Path | None = None, baslik: dict | None = None):
    req = urllib.request.Request(url, headers={"User-Agent": "meds-ders-video", **(baslik or {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        if hedef:
            with open(hedef, "wb") as f:
                shutil.copyfileobj(r, f, 1 << 20)
            return hedef
        return json.loads(r.read().decode("utf-8"))


CUMLE_RE = re.compile(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)")


def cumle_sinirlari(metin: str) -> list[int]:
    """canliDersStore.cumleSinirlari ile aynı kural (pdf_isaret cümle dizinleri buna göre)"""
    out: list[int] = []
    for m in CUMLE_RE.finditer(metin):
        if not m.group(0):
            continue
        e = m.end()
        s = metin[e:e + 1]
        if s and s != s.upper() and s == s.lower():
            continue
        if e > (out[-1] if out else 0):
            out.append(e)
    if not out or out[-1] < len(metin):
        out.append(len(metin))
    return out


def cizelge(detay: dict, v: dict) -> list[dict]:
    z = v.get("zamanlama") or []
    if not z:
        raise SystemExit("Bu sesin paragraf zamanlaması yok.")
    kzs = v.get("kelimeZaman") or {}
    out = []
    for b in detay["bolumler"]:
        for p in b["paragraflar"]:
            i = p["i"]
            if i >= len(z) or not z[i]:
                continue
            bas, son = z[i]
            kel = [[m.start(), m.end(), 0.0] for m in re.finditer(r"\S+", p["metin"])]
            kz = kzs.get(str(i))
            if kz and len(kz) == len(kel):
                for w, t in zip(kel, kz):
                    w[2] = t
            else:
                L = max(1, len(p["metin"]))
                for w in kel:
                    w[2] = bas + (w[0] / L) * (son - bas)
            out.append({"i": i, "metin": p["metin"], "bas": bas, "son": son, "kel": kel, "cumle": cumle_sinirlari(p["metin"]), "bolum": b["baslik"]})
    out.sort(key=lambda x: x["bas"])
    return out


def sayfa_cizelgesi(paras: list[dict], detay: dict, sure: float, sayilar: list[int]) -> list[tuple[float, int, int]]:
    """cdVideo.ts sayfaCizelgesi'nin aynısı: anlatımın gösterdiği sayfalar + hiç gösterilmeyenler önceki slaytın sonuna"""
    pdf = detay.get("pdf") or {}
    isaret = detay.get("isaret") or {}
    cap: list[list] = []
    for p in paras:
        e = (pdf.get("paragraflar") or [None] * (p["i"] + 1))[p["i"]] if p["i"] < len(pdf.get("paragraflar") or []) else None
        if not e:
            continue
        for c in range(len(p["cumle"])):
            cb = p["cumle"][c - 1] if c else 0
            w = next((k for k in p["kel"] if k[0] >= cb), None)
            t = p["bas"] if c == 0 else (w[2] if w else p["bas"])
            isr = (isaret.get(str(p["i"])) or [None] * (c + 1))
            isr = isr[c] if c < len(isr) else None
            if isr and isr.get("s"):
                sf = (isr["d"], isr["s"])
            elif e.get("sayfalar") and c < len(e["sayfalar"]) and e["sayfalar"][c]:
                sf = ((e.get("dosyalar") or [])[c] if c < len(e.get("dosyalar") or []) else e["dosya"], e["sayfalar"][c])
            else:
                sf = (e["dosya"], e["sayfa"])
            if not cap or cap[-1][1] != sf[0] or cap[-1][2] != sf[1]:
                cap.append([max(t, cap[-1][0] if cap else 0), sf[0], sf[1]])
    dil = [x for x in cap if 0 <= x[1] < len(sayilar) and 1 <= x[2] <= sayilar[x[1]]]
    ofs, top = [], 0
    for n in sayilar:
        ofs.append(top)
        top += n
    g = lambda d, s: ofs[d] + s - 1  # noqa: E731
    if not top:
        return [tuple(x) for x in dil]
    if not dil:
        pay = sure / top
        return [(g(d, s) * pay, d, s) for d, n in enumerate(sayilar) for s in range(1, n + 1)]
    dil[0][0] = 0
    gorulen = {g(x[1], x[2]) for x in dil}
    son_dilim = {g(x[1], x[2]): i for i, x in enumerate(dil)}
    ek: dict[int, list] = {}
    for d, n in enumerate(sayilar):
        for s in range(1, n + 1):
            k = g(d, s)
            if k in gorulen:
                continue
            sahip = next((son_dilim[j] for j in range(k - 1, -1, -1) if j in son_dilim), -1)
            ek.setdefault(sahip, []).append((d, s))
    bitis = lambda i: dil[i + 1][0] if i + 1 < len(dil) else sure  # noqa: E731
    pay = lambda uzun, n: max(1.2, min(4.0, uzun * 0.6 / n))  # noqa: E731
    out = []
    for i, x in enumerate(dil):
        t0 = x[0]
        if i == 0 and ek.get(-1):
            p = pay(bitis(0) - x[0], len(ek[-1]))
            for j, (d, s) in enumerate(ek[-1]):
                out.append((x[0] + j * p, d, s))
            t0 = x[0] + len(ek[-1]) * p
        out.append((t0, x[1], x[2]))
        if ek.get(i):
            son = bitis(i)
            p = pay(son - t0, len(ek[i]))
            ilk = max(t0 + 0.5, son - len(ek[i]) * p)
            adim = (son - ilk) / len(ek[i])
            for j, (d, s) in enumerate(ek[i]):
                out.append((ilk + j * adim, d, s))
    out.sort(key=lambda x: x[0])
    return out


# ——— çizim ———
def uret(key: str, vid: str, coz: str, cikti: Path, en_cok_sn: float | None = None, kodlayici: str = "h264_nvenc"):
    import fitz  # PyMuPDF
    from PIL import Image, ImageDraw, ImageFont

    W, H, bit = BOYUT[coz]
    k = H / 720
    detay = getir(f"{YEREL}/api/canli-ders/{key}")
    v = next((x for x in detay["varyantlar"] if x["id"] == vid), None)
    if not v:
        raise SystemExit("ses bulunamadı")
    paras = cizelge(detay, v)
    is_dir = Path(tempfile.mkdtemp(prefix="ders_video_"))
    try:
        ses = MEDS / "data" / "sesli_anlatim" / "ses" / key / f"{vid}.mp3"
        if not ses.exists():
            ses = getir(f"{YEREL}/api/canli-ders/ses/{key}/{vid}.mp3", is_dir / "ses.mp3")
        belgeler = []
        pdf = detay.get("pdf") or {}
        if pdf.get("deckId"):
            bilgi = getir(f"{YEREL}/api/lecture-pdf/deck/{pdf['deckId']}")
            for i, f in enumerate(bilgi.get("files") or []):
                if not f.get("available"):
                    belgeler.append(None)
                    continue
                belgeler.append(fitz.open(getir(f"{YEREL}/api/lecture-pdf/deck/{pdf['deckId']}/{i}", is_dir / f"{i}.pdf")))
        sayilar = [b.page_count if b else 0 for b in belgeler]
        sure = max(float(v.get("sureSn") or 0), paras[-1]["son"] if paras else 0)
        if en_cok_sn:
            sure = min(sure, en_cok_sn)
        sc = sayfa_cizelgesi(paras, detay, sure, sayilar)
        sc_t = [x[0] for x in sc]
        log(f"{key}/{vid} {coz}: {sum(sayilar)} sayfadan {len({(d, s) for _, d, s in sc})} sayfa çizelgede, {sure:.0f} sn")

        F = lambda ad, px: ImageFont.truetype(f"/usr/share/fonts/truetype/noto/NotoSans-{ad}.ttf", int(px))  # noqa: E731
        f_ust, f_bol, f_cum = F("Bold", 17 * k), F("Regular", 15 * k), F("Regular", 30 * k)
        Z, KART, YAZI, SOLUK, OKUNAN = (15, 20, 25), (26, 33, 41), (232, 237, 242), (125, 138, 151), (255, 210, 92)
        metin_y = int(H - 196 * k)
        ax, ay, aw, ah = int(28 * k), int(58 * k), int(W - 56 * k), int(metin_y - 58 * k - 14 * k)
        onb: dict[tuple, Image.Image] = {}

        def sayfa_resmi(d: int, s: int):
            kk = (d, s)
            if kk in onb:
                return onb[kk]
            b = belgeler[d] if d < len(belgeler) else None
            if not b or not 1 <= s <= b.page_count:
                return None
            pg = b[s - 1]
            r = pg.rect
            olc = min(aw / r.width, ah / r.height)
            pm = pg.get_pixmap(matrix=fitz.Matrix(olc, olc), alpha=False)
            im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
            if len(onb) > 6:
                onb.pop(next(iter(onb)))
            onb[kk] = im
            return im

        isaret = detay.get("isaret") or {}
        pbas = [p["bas"] for p in paras]
        pkt = [[x[2] for x in p["kel"]] for p in paras]

        def ciz(t: float) -> bytes:
            j = bisect.bisect_right(sc_t, t) - 1
            sd = sc[max(0, j)] if sc else None
            pi = bisect.bisect_right(pbas, t) - 1
            p = paras[pi] if pi >= 0 else None
            w = c = -1
            if p:
                w = max(0, bisect.bisect_right(pkt[pi], t) - 1)
                kb = p["kel"][w][0] if p["kel"] else 0
                c = next((ci for ci, e in enumerate(p["cumle"]) if kb < e), len(p["cumle"]) - 1)
            im = Image.new("RGB", (W, H), Z)
            dr = ImageDraw.Draw(im, "RGBA")
            etiket = f"{detay.get('brans')} {detay.get('no')} · " if detay.get("brans") else ""
            dr.text((28 * k, 30 * k), f"{etiket}{detay.get('baslik', '')}"[:110], font=f_ust, fill=YAZI, anchor="lm")
            if p:
                dr.text((W - 28 * k, 30 * k), p["bolum"][:60], font=f_bol, fill=SOLUK, anchor="rm")
            sr = sayfa_resmi(sd[1], sd[2]) if sd else None
            if sr:
                x0, y0 = ax + (aw - sr.width) // 2, ay + (ah - sr.height) // 2
                im.paste(sr, (x0, y0))
                isr = None
                if p and c >= 0:
                    L = isaret.get(str(p["i"])) or []
                    isr = L[c] if c < len(L) else None
                if isr and isr.get("d") == sd[1] and isr.get("s") == sd[2]:
                    for a, b2, c2, d2 in isr.get("l") or []:
                        dr.rectangle([x0 + a * sr.width, y0 + b2 * sr.height, x0 + c2 * sr.width, y0 + d2 * sr.height], fill=(255, 196, 0, 70))
                    cb = p["cumle"][c - 1] if c else 0
                    kc = p["kel"][w][0] - cb
                    wk = next((q for q in isr.get("w") or [] if q[0] <= kc < q[1]), None)
                    if wk:
                        dr.rectangle([x0 + wk[2] * sr.width - 2 * k, y0 + wk[3] * sr.height - 2 * k, x0 + wk[4] * sr.width + 2 * k, y0 + wk[5] * sr.height + 2 * k], outline=(255, 179, 0), width=max(2, int(2.5 * k)))
            else:
                dr.rectangle([ax, ay, ax + aw, ay + ah], fill=KART)
                dr.text((ax + aw / 2, ay + ah / 2), (p["bolum"] if p else detay.get("baslik", ""))[:60], font=F("Bold", 34 * k), fill=YAZI, anchor="mm")
            dr.rectangle([0, metin_y, W, H], fill=KART)
            if p:
                cb = p["cumle"][c - 1] if c else 0
                ce = p["cumle"][c]
                ks = [(j2, p["metin"][a:b3]) for j2, (a, b3, _) in enumerate(p["kel"]) if cb <= a < ce]
                bos = dr.textlength(" ", font=f_cum)
                satir, x = [[]], 0.0
                gen = W - 120 * k
                for j2, s in ks:
                    g2 = dr.textlength(s, font=f_cum)
                    if x > 0 and x + g2 > gen:
                        satir.append([]); x = 0.0
                    satir[-1].append((j2, s, x)); x += g2 + bos
                oku = max(0, next((si for si, sat in enumerate(satir) if any(q[0] == w for q in sat)), 0))
                bas = min(max(0, oku - 1), max(0, len(satir) - 3))
                gor = satir[bas:bas + 3]
                lh = 30 * k * 1.45
                y = metin_y + (H - metin_y - 6 * k) / 2 - (len(gor) - 1) * lh / 2
                for sat in gor:
                    for j2, s, xx in sat:
                        X = 60 * k + xx
                        if j2 == w:
                            g2 = dr.textlength(s, font=f_cum)
                            dr.rounded_rectangle([X - 6 * k, y - 30 * k * 0.68, X + g2 + 6 * k, y + 30 * k * 0.68], radius=8 * k, fill=(255, 210, 92, 46))
                            renk = OKUNAN
                        else:
                            renk = YAZI if j2 < w else SOLUK
                        dr.text((X, y), s, font=f_cum, fill=renk, anchor="lm")
                    y += lh
            dr.rectangle([0, H - 6 * k, W, H], fill=(255, 255, 255, 20))
            dr.rectangle([0, H - 6 * k, W * min(1, t / max(1, sure)), H], fill=OKUNAN)
            return im.tobytes()

        kod = ["-c:v", kodlayici]
        if kodlayici == "h264_nvenc":
            kod += ["-preset", "p5", "-rc", "vbr", "-cq", "23", "-b:v", bit, "-maxrate", bit, "-bufsize", bit]
        else:
            kod += ["-preset", "veryfast", "-crf", "23"]
        cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(GIRIS_FPS), "-i", "-",
               "-i", str(ses), "-t", f"{sure:.3f}", "-map", "0:v", "-map", "1:a",
               "-vf", "fps=60,format=yuv420p", *kod, "-g", "120", "-c:a", "copy", "-movflags", "+faststart", str(cikti)]
        # kart yalnız ffmpeg'e (NVENC) açılır; çizim süreci ve birim CUDA_VISIBLE_DEVICES="" ile kartı görmez
        ff_env = {**os.environ, "CUDA_VISIBLE_DEVICES": "0"} if kodlayici == "h264_nvenc" else {**os.environ, "CUDA_VISIBLE_DEVICES": ""}
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE, env=ff_env)
        kare = int(sure * GIRIS_FPS) + 1
        son_anahtar, son_bayt, son_bildirim = None, b"", 0.0
        for f in range(kare):
            t = f / GIRIS_FPS
            # anahtar: okunan kelime + sayfa + ilerleme çubuğu pikseli; değişmezse önceki kare yeniden yazılır
            j = bisect.bisect_right(sc_t, t) - 1
            pi = bisect.bisect_right(pbas, t) - 1
            w = bisect.bisect_right(pkt[pi], t) if pi >= 0 else -1
            anahtar = (j, pi, w, int(t / max(1, sure) * W))
            if anahtar != son_anahtar:
                son_bayt = ciz(t)
                son_anahtar = anahtar
            ff.stdin.write(son_bayt)
            if time.time() - son_bildirim > 3:
                son_bildirim = time.time()
                print(f"ORAN {f / kare:.4f}", flush=True)
        ff.stdin.close()
        if ff.wait() != 0:
            raise SystemExit("ffmpeg hata verdi")
        print("ORAN 1", flush=True)
        log(f"{key}/{vid} {coz} bitti: {cikti.stat().st_size / 1048576:.1f} MB")
    finally:
        shutil.rmtree(is_dir, ignore_errors=True)


# ——— işçi döngüsü ———
def api(yol: str, govde: dict | None = None):
    req = urllib.request.Request(f"{ORACLE}{yol}", data=json.dumps(govde or {}).encode(), method="POST",
                                 headers={"x-panel-secret": SIR, "Content-Type": "application/json", "User-Agent": "meds-ders-video",
                                          **({"X-API-Password": API_SIFRE} if API_SIFRE else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def bekle():
    if len(SIR) < 24:
        raise SystemExit("MEDS_PANEL_SECRET yok (.env)")
    durdur = {"v": False}
    signal.signal(signal.SIGTERM, lambda *_: durdur.__setitem__("v", True))
    log("işçi başladı")
    while not durdur["v"]:
        hazir, neden = gpu_hazir()
        try:
            r = api("/api/canli-ders/video-is/al", {"hazir": hazir, "gpu": "hazır" if hazir else neden})
        except Exception as e:  # noqa: BLE001
            log(f"kuyruk okunamadı: {e}")
            time.sleep(60)
            continue
        is_ = r.get("is")
        if not is_:
            time.sleep(30 if hazir else 120)
            continue
        iid = is_["id"]
        log(f"iş {iid}: {is_['key']} {is_['vid']} {is_['cozunurluk']}")
        out = Path(tempfile.gettempdir()) / f"{iid}.mp4"
        p = subprocess.Popen([sys.executable, __file__, "uret", "--key", is_["key"], "--vid", is_["vid"], "--coz", is_["cozunurluk"], "--cikti", str(out)],
                             stdout=subprocess.PIPE, text=True, env={**os.environ, "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES", "")})
        iptal = False
        son = 0.0
        for satir in p.stdout:  # type: ignore[union-attr]
            if satir.startswith("ORAN ") and time.time() - son > 5:
                son = time.time()
                try:
                    if api(f"/api/canli-ders/video-is/{iid}/durum", {"durum": "calisiyor", "oran": float(satir.split()[1]) * 0.97, "kodlayici": "h264_nvenc"}).get("iptal"):
                        iptal = True
                        p.terminate()
                        break
                except Exception:
                    pass
        kod = p.wait()
        try:
            if iptal:
                log(f"iş {iid} iptal edildi")
            elif kod != 0 or not out.exists():
                api(f"/api/canli-ders/video-is/{iid}/durum", {"durum": "hata", "mesaj": f"üretim başarısız (kod {kod})"})
            else:
                subprocess.run(["ssh", SSH, f"mkdir -p {UZAK_CIKTI}"], check=True, timeout=60)
                subprocess.run(["rsync", "-a", "--partial", str(out), f"{SSH}:{UZAK_CIKTI}/{iid}.mp4"], check=True, timeout=7200)
                api(f"/api/canli-ders/video-is/{iid}/durum", {"durum": "bitti", "oran": 1})
                log(f"iş {iid} gönderildi")
        except Exception as e:  # noqa: BLE001
            log(f"iş {iid} sonuç bildirilemedi: {e}")
            try:
                api(f"/api/canli-ders/video-is/{iid}/durum", {"durum": "hata", "mesaj": "video sunucuya gönderilemedi"})
            except Exception:
                pass
        finally:
            out.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="kip", required=True)
    sp.add_parser("bekle")
    u = sp.add_parser("uret")
    u.add_argument("--key", required=True)
    u.add_argument("--vid", required=True)
    u.add_argument("--coz", choices=list(BOYUT), default="1080p")
    u.add_argument("--cikti", required=True)
    u.add_argument("--sn", type=float, default=None, help="deneme: yalnız ilk n saniye")
    u.add_argument("--cpu", action="store_true", help="deneme: libx264 (GPU kullanmaz)")
    a = ap.parse_args()
    if a.kip == "bekle":
        bekle()
        return
    if a.cpu:
        uret(a.key, a.vid, a.coz, Path(a.cikti), a.sn, "libx264")
        return
    hazir, neden = gpu_hazir()
    if not hazir:
        raise SystemExit(f"GPU hazır değil: {neden}")
    uret(a.key, a.vid, a.coz, Path(a.cikti), a.sn)


if __name__ == "__main__":
    main()
