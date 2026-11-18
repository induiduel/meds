#!/usr/bin/env python3
"""Toplu ses yeniden üretim SÜRÜCÜSÜ (2026-11-17, H586 okunuş değişikliği sonrası; kullanıcı onayı "yeniden üret").

Ne yapar: `okunus_farki.jsonl`'de listelenen klipleri (ve istenirse `--bozuk` listesini) YALNIZ onları, kök kök, en küçükten
büyüğe yeniden seslendirir. Klip adı/karması değişmez (`h` korunur), kayıttaki sure/zaman/not/okunus_surum güncellenir.

Neden ayrı sürücü: üretici betikler var olan klibi (karma aynı) atlıyor, tek yol her şeyi baştan üreten `--force`; o da yarıda
kesilince baştan başlıyor ve yeni klibi kapıdan geçirmeden eskisinin üstüne yazıyor. Burada:
  1. ÜRETİM (GPU, yalnız `cozucu_ses_gpu.sh` ile): yeni klip HAZIRLIK dizinine yazılır, canlı dosyaya dokunulmaz.
     Motor metni satırdaki `okunus` haritasından (okunus_farki.py ses_metin.hazirla ile yazdı) — üretici betiklere dokunulmadı.
  2. KAPI (CPU, ffprobe/ffmpeg): ses_kapisi.olc ölçümü + aynı eşikler (çözülebilir, eski klibin sr/kanal/kbps'iyle aynı, sessiz
     değil, düzey kaba bandı, süre/karakter kaba bandı) YALNIZ yeni kliplerde.
  3. TAKAS: geçen klipte eski dosya meds_temp/ses_ortak/yeniden_uretim/eski/<kök>/… altına KOPYALANIR, yeni dosya os.replace ile
     yerine konur, kayıt satırı atomik yazılır. Geçmeyen klip takas EDİLMEZ (eski yerinde), deftere `reddedildi` + neden.
Durum defteri (append-only, satır başına tek write+fsync; yarım son satır okunurken yok sayılır):
  meds_temp/ses_ortak/yeniden_uretim/durum.jsonl — {anahtar, kok, durum, zaman, …}; durum ∈ bekliyor | uretildi | reddedildi |
  kapidan_gecti | geri_alindi. Yeniden çalıştırınca kapidan_gecti/reddedildi/geri_alindi atlanır (--yeniden-dene ile son ikisi
  yeniden denenir); `uretildi` olup hazır dosyası duran klip yeniden üretilmeden kapıya girer.

Desteklenmeyen: `sesli_ders(MEDS_OKUNUS_ORTAK=1)` (klip değil bütün ders MP3'ü + zaman/çapa katmanları; ayrı karar gerekir).
GPU: sürücü GPU açmaz; üretim alt süreci `scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh` ile (koruyucu/saat kilidi/tek GPU
kilidi orada). Sarmalayıcı 75 dönerse sürücü aynı kodla çıkar, CPU'ya düşmez. TTS'tir, LLM değil (llm_kilit gerekmez); kendi
kendine başlamaz, zamanlayıcı kurmaz.

Kullanım (proje kökü /home/indu/medsor):
  python3 meds/scripts/uretim/ses_ortak/yeniden_uret.py plan --hepsi [--bozuk]          # = kuru: kök → klip, tahmini süre
  python3 meds/scripts/uretim/ses_ortak/yeniden_uret.py calistir --kok k2genetik_cozucu [--kok …] [--parti 300]
  systemd-run --user --unit=meds-ses-yeniden --collect -p WorkingDirectory=/home/indu/medsor \\
      python3 meds/scripts/uretim/ses_ortak/yeniden_uret.py calistir --hepsi              # arka planda tam iş
  python3 meds/scripts/uretim/ses_ortak/yeniden_uret.py durum                          # kök başına defter özeti
  systemctl --user stop meds-ses-yeniden                                               # durdur (kaldığı yerden sürer)
  python3 meds/scripts/uretim/ses_ortak/yeniden_uret.py geri-al --kok <ad>             # takas edilenleri eskiye döndür
Günlük: meds_temp/ses_ortak/yeniden_uretim.log
"""
from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse  # noqa: E402
import fcntl  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ses_klip as SK  # noqa: E402
import ses_kapisi as KP  # noqa: E402

TEMP = _kok.MEDS.parent / "meds_temp/ses_ortak"
LISTE = TEMP / "okunus_farki.jsonl"
BOZUK_LISTE = TEMP / "bozuk_klipler.json"
IS = TEMP / "yeniden_uretim"
DURUM = IS / "durum.jsonl"
HAZIR = IS / "hazir"
ESKI = IS / "eski"
LOG = TEMP / "yeniden_uretim.log"
GPU_SARMAL = _kok.SCRIPTS / "uretim/patoloji_cozucu/cozucu_ses_gpu.sh"
DESTEKSIZ = ("sesli_ders",)
SONLU = {"kapidan_gecti", "reddedildi", "geri_alindi"}
VARSAYILAN_SN_KARAKTER = 0.02  # ölçüm yoksa tahmin (XTTS/EMA ~RTF 0,35 × 18 karakter/sn); ilk gerçek koşudan sonra ölçülür


def log(m: str) -> None:
    s = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {m}"
    print(s, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(s + "\n")
    except OSError:
        pass


def kok_dizin(kok: str) -> str:
    return kok.replace(":", "_").replace("/", "_")


def anahtar(r: dict) -> str:
    return f"{r['modul']}|{r['klasor']}|{r['klip']}"


def dosya_karma(p: Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()[:16]


# ── defter ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def defter_yaz(**kw) -> None:
    kw.setdefault("zaman", time.strftime("%Y-%m-%d %H:%M:%S"))
    IS.mkdir(parents=True, exist_ok=True)
    satir = (json.dumps(kw, ensure_ascii=False) + "\n").encode()
    fd = os.open(DURUM, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, satir)  # tek write: O_APPEND ile satır bölünmez
        os.fsync(fd)
    finally:
        os.close(fd)


def defter_oku() -> dict[str, dict]:
    """anahtar → SON kayıt (önceki kayıtların `eski_kayit`/`yeni_karma` alanları birleştirilir)."""
    son: dict[str, dict] = {}
    if not DURUM.exists():
        return son
    for s in DURUM.read_text(encoding="utf-8").splitlines():
        try:
            o = json.loads(s)
        except json.JSONDecodeError:
            continue  # yarım son satır (kesinti)
        son[o["anahtar"]] = {**son.get(o["anahtar"], {}), **o}
    return son


# ── girdi ───────────────────────────────────────────────────────────────────────────────────────────────────────────
def bozuk_satirlari() -> list[dict]:
    """bozuk_klipler.json (Öğren adımları) → okunus_farki satırı biçimi (cümleler kayıttan, okunuş ortak yoldan)."""
    import ses_metin as SM
    out = []
    for b in json.loads(BOZUK_LISTE.read_text(encoding="utf-8")):
        deste, adim = b["deste"], str(b["adim"])
        g = SK.kayit_oku(SK.DATA / "ogren_ses" / deste / "kayit.json").get(adim) or {}
        cum = g.get("cumleler")
        if not cum:
            continue
        ok = SM.okuyucu(ders=deste)
        par = [p.strip() for c in cum for p, _ in re.findall(r"(.+?)(\|\||\||$)", c.strip()) if p.strip()]  # = seslendir
        out.append({"modul": "ogren_ses", "klasor": deste, "klip": adim, "cumleler": cum,
                    "okunus": {p: ok(p) for p in par}, "kaynak": "bozuk"})
    return out


def satirlar(bozuk: bool) -> tuple[dict[str, list[dict]], dict[str, int]]:
    """kök → satırlar (anahtar tekil, son satır geçerli); ikinci değer: desteklenmeyen kök → sayı."""
    tek: dict[str, dict] = {}
    with LISTE.open(encoding="utf-8") as f:
        for s in f:
            try:
                r = json.loads(s)
            except json.JSONDecodeError:
                continue
            tek[anahtar(r)] = r
    if bozuk:
        for r in bozuk_satirlari():
            tek[anahtar(r)] = r
    kokler: dict[str, list[dict]] = {}
    desteksiz: dict[str, int] = {}
    for r in tek.values():
        m = r["modul"]
        if m.startswith(DESTEKSIZ) or not r.get("cumleler") or (not m.startswith("ek_modul:") and m != "terim_ses"
                                                                 and not r.get("okunus")):
            desteksiz[m] = desteksiz.get(m, 0) + 1
            continue
        kokler.setdefault(m, []).append(r)
    return kokler, desteksiz


def motor_karakter(r: dict) -> int:
    return sum(len(v) for v in (r.get("okunus") or {}).values()) or sum(map(len, r["cumleler"]))


def hazir_yol(r: dict) -> Path:
    mp3, _kp, _a = SK._hedef(r)
    return HAZIR / kok_dizin(r["modul"]) / mp3.relative_to(SK.DATA)


def eski_yol(r: dict) -> Path:
    mp3, _kp, _a = SK._hedef(r)
    return ESKI / kok_dizin(r["modul"]) / mp3.relative_to(SK.DATA)


def bekleyenler(rows: list[dict], defter: dict[str, dict], yeniden_dene: bool) -> list[dict]:
    sonlu = {"kapidan_gecti"} if yeniden_dene else SONLU
    return [r for r in rows if defter.get(anahtar(r), {}).get("durum") not in sonlu]


# ── üretim (GPU alt sürecinde) ──────────────────────────────────────────────────────────────────────────────────────
class Uretici:
    """Gerçek üretici: modeli bir kez yükler; dal mantığı ses_klip._yeniden ile aynı (motor metni = satırın okunuşu)."""

    def __init__(self):
        import ema_isci as E
        self.E, self.tts, self.ek = E, E.model_yukle(), {}

    def __call__(self, r: dict) -> tuple[bytes, list | None, float, list]:
        E, m = self.E, r["modul"]
        _mp3, kp, a = SK._hedef(r)
        if m.startswith("ek_modul:"):
            import ses_metin
            mod = m.split(":", 1)[1]
            if mod not in self.ek:
                import importlib.util
                sp = importlib.util.spec_from_file_location("ek_ses", _kok.SCRIPTS / "uretim/ek_modul/ses.py")
                em = importlib.util.module_from_spec(sp)
                sp.loader.exec_module(em)
                self.ek[mod] = em.klipler(mod)
            par = self.ek[mod].get(a)
            if par is None or hashlib.sha1("\n".join(par).encode()).hexdigest()[:12] != SK.kayit_oku(kp).get(a, {}).get("v"):
                raise ValueError("ek modül klip metni kayıttaki özetle (v) eşleşmiyor")
            mp3, _z, sure, notlar = E.parca_uret(self.tts, {"paragraflar": par, "bolumBasi": False}, True,
                                                 okunus=ses_metin.okuyucu(modul=mod))
            if any(SK.bozuk_mu(n) for n in notlar or []):
                raise SK.BozukKlip(str(notlar)[:200])
            return mp3, None, sure, notlar or []
        if m == "terim_ses":
            import numpy as np
            import ses_metin
            metin = r.get("okunus", {}).get(r["cumleler"][0]) or ses_metin.okuyucu(yol="uzun", modul="terim_ses")(r["cumleler"][0])
            x, n1 = E.paragraf_seslendir(self.tts, metin, hazir=True)
            if SK.bozuk_mu(n1):
                raise SK.BozukKlip(str(n1))
            mp3 = E.mp3_kodla((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes(), kbps=48)
            return mp3, None, round(len(mp3) * 8 / 48000, 2), [n1] if n1 else []
        harita = r["okunus"]
        mp3, zaman, sure, notlar = SK.seslendir(self.tts, r["cumleler"], okunus=lambda p: harita[p], kbps=48, E=E)
        return mp3, zaman, sure, notlar


def parti_uret(kok: str, rows: list[dict], uretici) -> int:
    """Bekleyen satırları hazırlık dizinine üretir; defter: uretildi | reddedildi. Döner: 0, ya da 75 (CUDA → dur)."""
    for r in rows:
        k = anahtar(r)
        hy = hazir_yol(r)
        if hy.exists():
            continue  # önceki partide üretildi, kapı bekliyor
        defter_yaz(anahtar=k, kok=kok, durum="bekliyor")
        t0 = time.time()
        try:
            mp3, zaman, sure, notlar = uretici(r)
        except SK.BozukKlip as e:
            defter_yaz(anahtar=k, kok=kok, durum="reddedildi", neden=f"bozuk: {e}"[:300])
            log(f"  RED {k}: bozuk ({e})")
            continue
        except Exception as e:  # noqa: BLE001
            if "CUDA" in str(e) or "out of memory" in str(e).lower():
                log(f"CUDA hatası — durdu (yeniden çalıştırınca kalan sürer): {e}")
                return 75
            defter_yaz(anahtar=k, kok=kok, durum="reddedildi", neden=f"{type(e).__name__}: {e}"[:300])
            log(f"  RED {k}: {type(e).__name__}: {e}")
            continue
        hy.parent.mkdir(parents=True, exist_ok=True)
        SK.atomik_yaz(hy, mp3)
        defter_yaz(anahtar=k, kok=kok, durum="uretildi", sure=sure, zaman_dizisi=zaman, notlar=notlar,
                   motor=motor_karakter(r), uretim_sn=round(time.time() - t0, 2), yeni_karma=dosya_karma(hy))
    return 0


# ── kapı + takas (CPU) ──────────────────────────────────────────────────────────────────────────────────────────────
def kapi_denetle(yeni: Path, eski: Path, motor: int) -> str | None:
    """ses_kapisi ölçümü + HATA eşikleri (gevşetilmedi). Döner: ret nedeni ya da None."""
    y, e = KP.olc(yeni), KP.olc(eski)
    if not y.get("ok") or y.get("cozme_hatasi"):
        return f"çözülemedi: {y.get('hata') or y.get('cozme_hatasi')}"
    if e.get("ok") and (y["sr"], y["kanal"], y["kbps"]) != (e["sr"], e["kanal"], e["kbps"]):
        return f"biçim farklı {y['sr']}/{y['kanal']}/{y['kbps']} ≠ {e['sr']}/{e['kanal']}/{e['kbps']}"
    if (y.get("sure") or 0) <= 0 or y.get("max") is None or y["max"] < KP.SESSIZ_TEPE:
        return "sessiz/boş"
    if y.get("mean") is not None and not (KP.DUZEY_HATA[0] <= y["mean"] <= KP.DUZEY_HATA[1]):
        return f"düzey {y['mean']}"
    if motor >= 20 and not (KP.ORAN_HATA[0] <= y["sure"] / (motor / KP.KARAKTER_SN) <= KP.ORAN_HATA[1]):
        return f"süre/karakter {y['sure'] / (motor / KP.KARAKTER_SN):.2f}"
    return None


def _kayit_yaz(kp: Path, kayit: dict) -> None:
    ham = kp.read_text(encoding="utf-8")[:4] if kp.exists() else ""
    girinti = 2 if ham.startswith("{\n  ") else 0 if ham.startswith("{\n\"") else None  # dosyanın kendi biçimi korunur
    SK.atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False, indent=girinti))


def kapi_ve_takas(kok: str, rows: list[dict], kapi=kapi_denetle) -> dict:
    defter = defter_oku()
    say = {"gecti": 0, "red": 0}
    kayitlar: dict[Path, dict] = {}
    for r in rows:
        k = anahtar(r)
        d = defter.get(k, {})
        if d.get("durum") != "uretildi":
            continue
        mp3, kp, a = SK._hedef(r)
        hy, ey = hazir_yol(r), eski_yol(r)
        if kp not in kayitlar:
            kayitlar[kp] = SK.kayit_oku(kp)
        kayit = kayitlar[kp]
        yarim = not hy.exists() and mp3.exists() and dosya_karma(mp3) == d.get("yeni_karma")  # takas sonrası kesinti
        if not yarim:
            if not hy.exists():
                defter_yaz(anahtar=k, kok=kok, durum="reddedildi", neden="hazır dosya kayıp")
                say["red"] += 1
                continue
            if a not in kayit or not mp3.exists():
                hy.unlink()
                defter_yaz(anahtar=k, kok=kok, durum="reddedildi", neden="canlı klip kayıtta/diskte yok")
                say["red"] += 1
                continue
            neden = kapi(hy, mp3, d.get("motor") or motor_karakter(r))
            if neden:
                hy.unlink()
                defter_yaz(anahtar=k, kok=kok, durum="reddedildi", neden=f"kapı: {neden}")
                log(f"  KAPI RED {k}: {neden}")
                say["red"] += 1
                continue
            if not ey.exists():
                ey.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(mp3, ey)
            eski_kayit = d.get("eski_kayit") or kayit.get(a)
            defter_yaz(anahtar=k, kok=kok, durum="uretildi", eski_kayit=eski_kayit)  # geri alma için önce kaydet
            d["eski_kayit"] = eski_kayit
            os.replace(hy, mp3) if hy.stat().st_dev == mp3.stat().st_dev else shutil.move(str(hy), str(mp3))
        g = kayit[a]
        g["sure"] = d["sure"]
        if d.get("zaman_dizisi") is not None:
            g["zaman"] = d["zaman_dizisi"]
        if r["modul"] == "ogren_ses":
            g["guncellendi"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if d.get("notlar"):
            g["not"] = d["notlar"]
        else:
            g.pop("not", None)
        import ses_metin
        g["okunus_surum"] = ses_metin.SOZLUK_SURUM
        _kayit_yaz(kp, kayit)
        defter_yaz(anahtar=k, kok=kok, durum="kapidan_gecti", yeni_karma=dosya_karma(mp3))
        say["gecti"] += 1
    return say


# ── alt komutlar ────────────────────────────────────────────────────────────────────────────────────────────────────
def secili(a, kokler: dict[str, list[dict]]) -> list[str]:
    if a.hepsi:
        ad = list(kokler)
    else:
        ad = a.kok or []
        yok = [k for k in ad if k not in kokler]
        if yok:
            sys.exit(f"bilinmeyen/desteklenmeyen kök: {', '.join(yok)} (plan --hepsi listeyi gösterir)")
    return sorted(ad, key=lambda k: (len(kokler[k]), k))  # en küçükten büyüğe


def sn_karakter(defter: dict[str, dict]) -> tuple[float, str]:
    o = [(d["uretim_sn"], d["motor"]) for d in defter.values() if d.get("uretim_sn") and d.get("motor")]
    if len(o) >= 5:
        return sum(x for x, _ in o) / max(1, sum(m for _, m in o)), f"ölçülen ({len(o)} klip)"
    return VARSAYILAN_SN_KARAKTER, "varsayım"


def k_plan(a) -> int:
    kokler, desteksiz = satirlar(a.bozuk)
    defter = defter_oku()
    hiz, kaynak = sn_karakter(defter)
    print(f"{'kök':40} {'liste':>7} {'üretilecek':>11} {'karakter':>10} {'tahmin':>9}")
    top = [0, 0, 0]
    for k in secili(a, kokler):
        b = bekleyenler(kokler[k], defter, a.yeniden_dene)
        kar = sum(motor_karakter(r) for r in b)
        top[0] += len(kokler[k]); top[1] += len(b); top[2] += kar
        print(f"{k:40} {len(kokler[k]):7} {len(b):11} {kar:10} {kar * hiz / 60:7.0f}dk")
    print(f"{'TOPLAM':40} {top[0]:7} {top[1]:11} {top[2]:10} {top[2] * hiz / 3600:7.1f} sa  ({kaynak}: {hiz:.4f} sn/karakter)")
    for m, n in sorted(desteksiz.items()):
        print(f"  DESTEKLENMİYOR {m}: {n} (sesli ders bütün MP3 / satırda cümle-okunuş yok)")
    return 0


def k_durum(a) -> int:
    defter = defter_oku()
    say: dict[str, dict[str, int]] = {}
    for d in defter.values():
        s = say.setdefault(d["kok"], {})
        s[d["durum"]] = s.get(d["durum"], 0) + 1
    if not say:
        print("defter boş:", DURUM)
    for k, s in sorted(say.items()):
        print(f"{k:40} " + "  ".join(f"{x}={n}" for x, n in sorted(s.items())))
    red = [(k, d.get("neden")) for k, d in defter.items() if d["durum"] == "reddedildi"]
    for k, n in red[: a.ayrinti]:
        print(f"  RED {k}: {n}")
    return 0


def k_geri_al(a) -> int:
    defter = defter_oku()
    n = 0
    kayitlar: dict[Path, dict] = {}
    for k, d in defter.items():
        if d["kok"] not in a.kok or d["durum"] != "kapidan_gecti":
            continue
        modul, klasor, klip = k.split("|", 2)
        r = {"modul": modul, "klasor": klasor, "klip": klip}
        mp3, kp, an = SK._hedef(r)
        ey = eski_yol(r)
        if not ey.exists():
            log(f"  GERİ ALINAMADI {k}: yedek yok ({ey})")
            continue
        tmp = mp3.with_name(f".{mp3.name}.geri.tmp")
        shutil.copy2(ey, tmp)
        os.replace(tmp, mp3)
        if kp not in kayitlar:
            kayitlar[kp] = SK.kayit_oku(kp)
        if d.get("eski_kayit") is not None:
            kayitlar[kp][an] = d["eski_kayit"]
            _kayit_yaz(kp, kayitlar[kp])
        defter_yaz(anahtar=k, kok=d["kok"], durum="geri_alindi")
        n += 1
    log(f"geri-al {','.join(a.kok)}: {n} klip eskiye döndü")
    return 0


def k_uret(a) -> int:
    """İç kip: GPU sarmalayıcısı altında çalışır (elle çağrılmaz)."""
    kokler, _ = satirlar(a.bozuk)
    rows = bekleyenler(kokler.get(a.kok[0], []), defter_oku(), a.yeniden_dene)
    rows = [r for r in rows if not hazir_yol(r).exists()][: a.parti]
    log(f"  üretim {a.kok[0]}: {len(rows)} klip (cihaz {os.environ.get('EMA_CIHAZ')})")
    if not rows:
        return 0
    return parti_uret(a.kok[0], rows, Uretici())


def k_calistir(a) -> int:
    IS.mkdir(parents=True, exist_ok=True)
    kilit = open(IS / "surucu.lock", "w")
    try:
        fcntl.flock(kilit, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log("başka bir yeniden_uret.py calistir sürüyor — çıkılıyor")
        return 75
    kokler, _ = satirlar(a.bozuk)
    sira = secili(a, kokler)
    log(f"calistir: {len(sira)} kök sırayla: {', '.join(sira)}")
    for kok in sira:
        while True:
            b = bekleyenler(kokler[kok], defter_oku(), a.yeniden_dene)
            if not b:
                break
            uretilecek = [r for r in b if not hazir_yol(r).exists() and defter_oku().get(anahtar(r), {}).get("durum") != "uretildi"]
            if uretilecek:
                arg = [str(GPU_SARMAL), str(Path(__file__).resolve()), "_uret", "--kok", kok, "--parti", str(a.parti)]
                if a.bozuk:
                    arg.append("--bozuk")
                if a.yeniden_dene:
                    arg.append("--yeniden-dene")
                log(f"{kok}: {len(b)} bekliyor → GPU partisi ({min(a.parti, len(uretilecek))})")
                rc = subprocess.run(["bash", *arg], cwd=str(_kok.MEDS.parent)).returncode
                if rc not in (0, 3):  # 3: ses_klip atexit (bozuk klip) — defterde zaten reddedildi
                    log(f"{kok}: üretim alt süreci çıkış {rc} — durduruldu (defter sağlam; yeniden çalıştırınca sürer)")
                    return rc
            s = kapi_ve_takas(kok, kokler[kok])
            log(f"{kok}: kapı → {s['gecti']} takas edildi, {s['red']} reddedildi")
            if not uretilecek and not s["gecti"] and not s["red"]:
                break  # ilerleme yok (ör. hepsi 'bekliyor' takılı) — sonsuz döngü önlemi
    log("calistir bitti")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = p.add_subparsers(dest="komut", required=True)
    for ad in ("plan", "calistir", "durum", "geri-al", "_uret"):
        s = alt.add_parser(ad)
        s.add_argument("--kok", action="append")
        s.add_argument("--hepsi", action="store_true")
        s.add_argument("--bozuk", action="store_true", help="bozuk_klipler.json'daki Öğren adımlarını da ekle")
        s.add_argument("--yeniden-dene", action="store_true", help="reddedildi/geri_alindi olanları yeniden dene")
        s.add_argument("--parti", type=int, default=300, help="GPU alt süreci başına klip (model her partide yüklenir)")
        s.add_argument("--ayrinti", type=int, default=20)
    a = p.parse_args()
    if a.komut in ("plan", "calistir") and not (a.hepsi or a.kok):
        p.error("--kok <ad> ya da --hepsi")
    if a.komut in ("geri-al", "_uret") and not a.kok:
        p.error("--kok <ad> gerekli")
    return {"plan": k_plan, "calistir": k_calistir, "durum": k_durum, "geri-al": k_geri_al, "_uret": k_uret}[a.komut](a)


if __name__ == "__main__":
    sys.exit(main())
