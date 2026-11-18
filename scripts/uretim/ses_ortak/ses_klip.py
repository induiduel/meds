#!/usr/bin/env python3
"""Ses klibi — çözücü/asistan/Öğren klip üretiminin ORTAK çekirdeği (2026-11-16).

Önceden `seslendir` 4 betikte (patoloji_cozucu/cozucu_ses, spot_cozucu/ses, ogren_ses/ogren_ses_uret, patoloji_onem/asistan_ses),
`klasor` 2 betikte, `cumlele`/`nokta` 4–5 betikte kopyaydı; betikler ortak durumu eziyordu (`E.KBPS = 48`,
`E.okunus.duzelt = lambda …`) ve aynı süreçte başka bir yol bu ezmeyi devralıyordu. Burada:
  - bit hızı (`kbps`) ve okunuş işlevi (`okunus`) PARAMETREDİR; ema_isci'nin genel değişkenleri değiştirilmez.
  - klip karması formülü BİREBİR korunur: sha1(surum + "|" + "\\n".join(cumleler) + okunus.sayi_imi(cumleler))[:12]
    (mevcut ~90 bin klibin dosya adı/kaydı değişmez; okunuş değişikliği kendiliğinden yeniden üretim TETİKLEMEZ).
  - yeni üretilen klibin kayıt satırına `okunus_surum` (ses_metin.SOZLUK_SURUM) yazılır (karmaya katılmaz).
  - kayit.json ve mp3 atomik yazılır (yarım dosya kalmaz).
Duraklar: cümle sonu 0,45 sn; " | " 0,3 sn, " || " 0,7 sn; baş 0,12 sn.
Bozuk klip (H587 güncellemesi): motorun süre/karakter oranı ÜÇ tohumda da eşik dışıysa `seslendir` BozukKlip fırlatır;
`klasor` o klibi YAZMAZ (eski klip/kayıt korunur), `BOZUK` listesine ve meds_temp/ses_ortak/uretim_bozuk.jsonl'e yazar,
süreç sonunda çıkış kodu 3 olur. >400 karakterlik parça motora ses_metin.parcala ile bölünerek gider (karma değişmez).
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

import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import sys  # noqa: E402
import atexit  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Callable  # noqa: E402

for _y in (_kok.SCRIPTS / "uretim" / "sesli_anlatim", Path(__file__).resolve().parent):
    if str(_y) not in sys.path:
        sys.path.append(str(_y))
import okunus as _okunus  # noqa: E402  (yalnız sayi_imi: karma formülünün parçası)
import ses_metin  # noqa: E402

class BozukKlip(Exception):
    """Üç tohumda da süre/karakter oranı tutmadı: klip yazılmaz."""


BOZUK: list[dict] = []
BOZUK_DOSYA = _kok.MEDS.parent / "meds_temp/ses_ortak/uretim_bozuk.jsonl"


def bozuk_mu(not_) -> bool:
    """ema_isci.paragraf_seslendir notu: 'süre oranı X (3 denemede düzelmedi)'."""
    return bool(not_) and "denemede düzelmedi" in str(not_)


def bozuk_kaydet(**kw) -> None:
    kw["zaman"] = time.strftime("%Y-%m-%d %H:%M:%S")
    BOZUK.append(kw)
    try:
        BOZUK_DOSYA.parent.mkdir(parents=True, exist_ok=True)
        with BOZUK_DOSYA.open("a", encoding="utf-8") as f:
            f.write(json.dumps(kw, ensure_ascii=False) + "\n")
    except OSError:
        pass


@atexit.register
def _cikis() -> None:
    """Bozuk klip olduysa iş başarılı sayılmaz: çıkış kodu 3 (diğer atexit işleri bundan önce çalışır — ilk kaydedilen)."""
    if BOZUK:
        print(f"HATA  {len(BOZUK)} klip üç tohumda da süre/karakter eşiği dışında — YAZILMADI ({BOZUK_DOSYA})",
              file=sys.stderr, flush=True)
        sys.stdout.flush()
        os._exit(3)


CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12
HARF_AD = {"A": "A", "B": "Be", "C": "Ce", "D": "De", "E": "E"}


def cumlele(s: str) -> list[str]:
    """Ses metnini cümlelere böl (ekranda cümle vurgusu + doğal durak)."""
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", s.strip()) if c.strip()]


def nokta(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in ".!?" else s + "."


def klip_karmasi(surum: str, cumleler: list[str]) -> str:
    """DOKUNMA: mevcut kliplerin adı/kaydı bu formüle bağlı. `surum` eski betiklerdeki önekle aynı verilir
    (ör. "ema-2|1.0" — eski "ema-2" + "|1.0|" ile aynı dizge)."""
    return hashlib.sha1((surum + "|" + "\n".join(cumleler) + _okunus.sayi_imi(cumleler)).encode()).hexdigest()[:12]


def atomik_yaz(yol: Path, veri: bytes | str) -> None:
    tmp = yol.with_name(f".{yol.name}.{os.getpid()}.tmp")
    if isinstance(veri, str):
        tmp.write_text(veri, encoding="utf-8")
    else:
        tmp.write_bytes(veri)
    tmp.replace(yol)


def seslendir(tts, cumleler: list[str], *, okunus: Callable[[str], str], kbps: int, E=None,
              paragraf: Callable | None = None):
    """Cümleler → (mp3, cümle zamanları, süre, notlar). `okunus` motor metnini üretir (ses_metin.hazirla ailesi);
    `paragraf` verilirse (ör. spot Saglayici) model çağrısı odur, yoksa ema_isci.paragraf_seslendir."""
    import numpy as np

    if E is None:
        import ema_isci as E
    sr = E.SR
    sessiz = lambda sn: np.zeros(int(round(sn * sr)), dtype=np.float32)  # noqa: E731
    parca, zaman, t, notlar = [sessiz(ON_SN)], [], ON_SN, []
    for c in cumleler:
        bas = t
        for par, ayrac in re.findall(r"(.+?)(\|\||\||$)", c.strip()):
            par = par.strip()
            if not par:
                continue
            okunan = okunus(par)
            if not re.search(r"\w", okunan):  # yalnız çizim/noktalama kalan parça (H587: "│ └──┘." → "." → 0 sn, bozuk) okunmaz
                continue
            for oku in ses_metin.parcala(okunan):
                wav, n = paragraf(oku) if paragraf else E.paragraf_seslendir(tts, oku, hazir=True)
                # çok kısa parçada ("2." → "iki.", beklenen 1,0 sn / gerçek 0,5 sn) oran ölçüsü anlamsız: bozuk sayılmaz,
                # yalnız not düşülür (2026-11-17; aksi hâlde numaralı listeli her klip yazılamıyordu)
                if bozuk_mu(n) and len(oku.strip()) >= 12:
                    raise BozukKlip(f"{n}: {par[:80]}")
                if n:
                    notlar.append(f"{n}: {par[:50]}")
                parca.append(wav)
                t += len(wav) / sr
            if ayrac:
                d = UZUN_SN if ayrac == "||" else KISA_SN
                parca.append(sessiz(d))
                t += d
        zaman.append([bas, t])
        parca.append(sessiz(CUMLE_SN))
        t += CUMLE_SN
    x = np.concatenate(parca)
    mp3 = E.mp3_kodla((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes(), kbps=kbps)
    gercek = len(mp3) * 8 / (kbps * 1000)
    k = gercek / (len(x) / sr)
    return mp3, [[round(a * k, 3), round(b * k, 3)] for a, b in zaman], round(gercek, 3), notlar


def kayit_oku(kp: Path) -> dict:
    try:
        return json.loads(kp.read_text(encoding="utf-8")) if kp.exists() else {}
    except json.JSONDecodeError:
        return {}


def klasor(d: Path, K: dict[str, list[str]], *, surum: str, uret: Callable[[list[str]], tuple],
           silinsin: bool = True, koru: Callable[[str], bool] | None = None, ara_yaz: int = 10,
           log: Callable[[str], None] | None = None) -> int:
    """Klip klasörü: değişmeyen klip atlanır, yenisi üretilir, kayit.json güncellenir. Döner: yeni klip sayısı.
    uret(cumleler) → (mp3, zaman, sure, notlar); koru(klip) True ise içerikte olmasa da silinmez."""
    d.mkdir(parents=True, exist_ok=True)
    kp = d / "kayit.json"
    kayit = kayit_oku(kp)
    yeni = 0
    toplam_sn = 0.0
    t0 = time.time()
    for klip, cumleler in K.items():
        h = klip_karmasi(surum, cumleler)
        if kayit.get(klip, {}).get("h") == h and (d / f"{klip}.mp3").exists():
            continue
        try:
            mp3, zaman, sure, notlar = uret(cumleler)
        except BozukKlip as e:
            bozuk_kaydet(klasor=str(d), klip=klip, hata=str(e), karakter=sum(map(len, cumleler)))
            (log or print)(f"  HATA {d.name}/{klip}: {e} — klip yazılmadı")
            continue
        atomik_yaz(d / f"{klip}.mp3", mp3)
        kayit[klip] = {"h": h, "sure": sure, "zaman": zaman, **({"not": notlar} if notlar else {}),
                       "okunus_surum": ses_metin.SOZLUK_SURUM}
        yeni += 1
        toplam_sn += sure
        if ara_yaz and yeni % ara_yaz == 0:
            atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False))
    if silinsin:
        for klip in [a for a in kayit if a not in K and not (koru and koru(a))]:
            kayit.pop(klip)
            (d / f"{klip}.mp3").unlink(missing_ok=True)
    atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False))
    (log or (lambda s: print(f"{time.strftime('%H:%M:%S')} {s}", flush=True)))(
        f"{d.name}: {len(K)} klip, {yeni} yeni ({toplam_sn:.0f} sn ses, {time.time() - t0:.0f} sn'de)")
    return yeni


# ── --yeniden: liste tabanlı ZORLA yeniden üretim (2026-11-17, kullanıcı onayı "Okunuş doğru") ─────────────────────────────
# Klip adı/karması okunan metni içermediği için betikler "dosya var" diye atlar; burada okunus_farki.jsonl satırları
# (modül/klasör/klip + cumleler + parça → YENİ okunuş) doğrudan seslendirilir. Her klip: geçici ad → ölçüm kapısı
# (ses_kapisi.olc: çözülebilir, biçim eskisiyle aynı, sessiz değil, düzey kaba bandı, süre/karakter kaba bandı) → eski klip
# meds_temp/ses_ortak/eski_klipler/<data'ya göreli yol> altına yedek → os.replace. Kayıtta `h` (karma) KORUNUR; sure/zaman/
# okunus_surum güncellenir. Kaldığı yerden devam: yeniden/yapilan.jsonl. GPU yalnız cozucu_ses_gpu.sh ile çağrılır.
# Kullanım: cozucu_ses_gpu.sh meds/scripts/uretim/ses_ortak/ses_klip.py --yeniden <liste.jsonl> --modul a,b [--sinir N]
YENIDEN = _kok.MEDS.parent / "meds_temp/ses_ortak/yeniden"
YEDEK = _kok.MEDS.parent / "meds_temp/ses_ortak/eski_klipler"
DATA = _kok.MEDS / "data"


def _hedef(r: dict) -> tuple[Path, Path, str]:
    """→ (mp3 yolu, kayıt dosyası, kayıt anahtarı)."""
    m, k, klip = r["modul"], r["klasor"], r["klip"]
    if m == "ogren_ses":
        d = DATA / "ogren_ses" / k
        return d / f"{klip}.mp3", d / "kayit.json", klip
    if m == "terim_ses":
        return DATA / "terim_ses" / klip[:2] / f"{klip}.mp3", DATA / "terim_ses/kayit.json", klip
    if m.startswith("ek_modul:"):
        mod = m.split(":", 1)[1]
        return (DATA / "ek_moduller/ses" / mod / f"{klip}.mp3",
                _kok.MEDS / "src/data/ek_moduller" / mod / "klip.json", klip)
    d = DATA / m / "ses" / k
    return d / f"{klip}.mp3", d / "kayit.json", klip


def _yeniden(argv: list[str]) -> int:
    import shutil
    import ses_kapisi as KP
    sys.path.insert(0, str(_kok.SCRIPTS))
    import gunluk
    liste = Path(argv[argv.index("--yeniden") + 1])
    moduller = set(argv[argv.index("--modul") + 1].split(",")) if "--modul" in argv else None
    sinir = int(argv[argv.index("--sinir") + 1]) if "--sinir" in argv else None
    YENIDEN.mkdir(parents=True, exist_ok=True)
    yp = YENIDEN / "yapilan.jsonl"
    yapildi = set()
    if yp.exists():
        for s in yp.read_text(encoding="utf-8").splitlines():
            try:
                o = json.loads(s)
                yapildi.add((o["modul"], o["klasor"], o["klip"]))
            except (json.JSONDecodeError, KeyError):
                pass
    satirlar = []
    with liste.open(encoding="utf-8") as f:
        for s in f:
            r = json.loads(s)
            if (moduller is None or r["modul"] in moduller) and not r["modul"].startswith("sesli_ders") \
                    and (r["modul"], r["klasor"], r["klip"]) not in yapildi:
                satirlar.append(r)
    if sinir:
        satirlar = satirlar[:sinir]
    import ema_isci as E
    log = lambda m: print(f"{time.strftime('%H:%M:%S')} {m}", flush=True)  # noqa: E731
    log(f"yeniden: {len(satirlar)} klip ({', '.join(sorted(moduller or ['hepsi']))}); cihaz {os.environ.get('EMA_CIHAZ')}")
    if not satirlar:
        return 0
    tts = E.model_yukle()
    ek_K: dict[str, dict] = {}
    kayitlar: dict[Path, dict] = {}
    ilerleme = {"moduller": sorted(moduller or []), "toplam": len(satirlar), "yapilan": 0, "hata": 0, "atlanan": 0,
                "basla": time.strftime("%Y-%m-%d %H:%M:%S"), "hatalar": []}
    ip = YENIDEN / "ilerleme.json"
    t0 = time.time()
    ses_sn = 0.0

    def hata(r, neden):
        ilerleme["hata"] += 1
        ilerleme["hatalar"].append({"modul": r["modul"], "klasor": r["klasor"], "klip": r["klip"], "neden": neden[:300]})
        log(f"  HATA {r['modul']}/{r['klasor']}/{r['klip']}: {neden[:200]}")
        gunluk.olay("ses_yeniden", "hata", "klip üretilemedi", modul=r["modul"], klasor=r["klasor"], klip=r["klip"], neden=neden[:300])

    for i, r in enumerate(satirlar, 1):
        mp3_yol, kp, anahtar = _hedef(r)
        if kp not in kayitlar:
            kayitlar[kp] = kayit_oku(kp)
        kayit = kayitlar[kp]
        if anahtar not in kayit or not mp3_yol.exists():
            ilerleme["atlanan"] += 1
            log(f"  ATLA {mp3_yol}: kayıtta/diskte yok")
            continue
        try:
            if r["modul"].startswith("ek_modul:"):
                mod = r["modul"].split(":", 1)[1]
                if mod not in ek_K:
                    import importlib.util
                    sp = importlib.util.spec_from_file_location("ek_ses", _kok.SCRIPTS / "uretim/ek_modul/ses.py")
                    em = importlib.util.module_from_spec(sp)
                    sp.loader.exec_module(em)
                    ek_K[mod] = em.klipler(mod)
                par = ek_K[mod].get(anahtar)
                if par is None or hashlib.sha1("\n".join(par).encode()).hexdigest()[:12] != kayit[anahtar].get("v"):
                    raise ValueError("ek modül klip metni kayıttaki özetle (v) eşleşmiyor")
                ok_ = ses_metin.okuyucu(modul=mod)
                mp3, _z, sure, notlar = E.parca_uret(tts, {"paragraflar": par, "bolumBasi": False}, True, okunus=ok_)
                if any(bozuk_mu(n) for n in notlar or []):
                    raise BozukKlip(str(notlar)[:200])
                motor = sum(len(ok_(p)) for p in par)
                zaman = None
            elif r["modul"] == "terim_ses":
                ok_ = ses_metin.okuyucu(yol="uzun", modul="terim_ses")
                metin = ok_(r["cumleler"][0])
                x, n1 = E.paragraf_seslendir(tts, metin, hazir=True)
                if bozuk_mu(n1):
                    raise BozukKlip(str(n1))
                import numpy as np
                mp3 = E.mp3_kodla((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes(), kbps=48)
                sure, zaman, notlar, motor = round(len(mp3) * 8 / 48000, 2), None, [n1] if n1 else [], len(metin)
            else:
                harita = r["okunus"]
                mp3, zaman, sure, notlar = seslendir(tts, r["cumleler"], okunus=lambda p: harita[p], kbps=48, E=E)
                motor = sum(len(v) for v in harita.values())
        except BozukKlip as e:
            bozuk_kaydet(klasor=str(mp3_yol.parent), klip=anahtar, hata=str(e), karakter=sum(map(len, r["cumleler"] or [])))
            hata(r, f"bozuk: {e}")
            continue
        except Exception as e:  # noqa: BLE001
            if "CUDA" in str(e) or "out of memory" in str(e).lower():
                log(f"CUDA hatası — durduruluyor (yeniden çalıştırınca kalan devam eder): {e}")
                gunluk.olay("ses_yeniden", "hata", "CUDA hatası, durdu", hata=str(e)[:300])
                return 75
            hata(r, f"{type(e).__name__}: {e}")
            continue
        gecici = mp3_yol.with_name(f".{mp3_yol.stem}.yeniden.{os.getpid()}.mp3")
        gecici.write_bytes(mp3)
        yeni_o, eski_o = KP.olc(gecici), KP.olc(mp3_yol)
        neden = None
        if not yeni_o.get("ok") or yeni_o.get("cozme_hatasi"):
            neden = f"çözülemedi: {yeni_o.get('hata') or yeni_o.get('cozme_hatasi')}"
        elif eski_o.get("ok") and (yeni_o["sr"], yeni_o["kanal"]) != (eski_o["sr"], eski_o["kanal"]):
            neden = f"biçim farklı {yeni_o['sr']}/{yeni_o['kanal']} ≠ {eski_o['sr']}/{eski_o['kanal']}"
        elif (yeni_o.get("sure") or 0) <= 0 or yeni_o.get("max") is None or yeni_o["max"] < KP.SESSIZ_TEPE:
            neden = "sessiz/boş"
        elif yeni_o.get("mean") is not None and not (KP.DUZEY_HATA[0] <= yeni_o["mean"] <= KP.DUZEY_HATA[1]):
            neden = f"düzey {yeni_o['mean']}"
        elif motor >= 20 and not (KP.ORAN_HATA[0] <= yeni_o["sure"] / (motor / KP.KARAKTER_SN) <= KP.ORAN_HATA[1]):
            neden = f"süre/karakter {yeni_o['sure'] / (motor / KP.KARAKTER_SN):.2f}"
        if neden:
            gecici.unlink(missing_ok=True)
            hata(r, f"kapı: {neden}")
            continue
        yedek = YEDEK / mp3_yol.relative_to(DATA)
        if not yedek.exists():
            yedek.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mp3_yol, yedek)
        os.replace(gecici, mp3_yol)
        g = kayit[anahtar]
        g["sure"] = sure
        if zaman is not None:
            g["zaman"] = zaman
        if r["modul"] == "ogren_ses":
            g["guncellendi"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if notlar:
            g["not"] = notlar
        else:
            g.pop("not", None)
        g["okunus_surum"] = ses_metin.SOZLUK_SURUM
        if kp.name != "kayit.json" or r["modul"] != "terim_ses" or i % 20 == 0 or i == len(satirlar):
            atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False, indent=(2 if r["modul"] == "ogren_ses" else 0 if r["modul"].startswith("ek_modul:") else None)))
        with yp.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"modul": r["modul"], "klasor": r["klasor"], "klip": r["klip"], "dosya": str(mp3_yol.relative_to(_kok.MEDS)),
                                "kayit": str(kp.relative_to(_kok.MEDS)), "sure": sure}, ensure_ascii=False) + "\n")
        ilerleme["yapilan"] += 1
        ses_sn += sure
        if i == 200 or i % 50 == 0 or i == len(satirlar):
            gecen = time.time() - t0
            kalan = gecen / i * (len(satirlar) - i)
            ilerleme.update(gecen_sn=round(gecen), tahmini_kalan_sn=round(kalan), ses_sn=round(ses_sn))
            atomik_yaz(ip, json.dumps(ilerleme, ensure_ascii=False, indent=1))
            log(f"[{i}/{len(satirlar)}] {gecen:.0f} sn, kalan ≈ {kalan / 60:.0f} dk, hata {ilerleme['hata']}")
            if i == 200:
                gunluk.olay("ses_yeniden", "bilgi", "ilk 200 klip süre tahmini", gecen_sn=round(gecen),
                            klip_basina_sn=round(gecen / i, 2), kalan_dk=round(kalan / 60), toplam=len(satirlar))
    for kp, kayit in kayitlar.items():
        if kp.name == "kayit.json" and kp.parent.name == "terim_ses":
            atomik_yaz(kp, json.dumps(kayit, ensure_ascii=False))
    ilerleme["bitis"] = time.strftime("%Y-%m-%d %H:%M:%S")
    atomik_yaz(ip, json.dumps(ilerleme, ensure_ascii=False, indent=1))
    gunluk.olay("ses_yeniden", "hata" if ilerleme["hata"] else "bilgi", "yeniden üretim turu bitti",
                **{k: ilerleme[k] for k in ("toplam", "yapilan", "hata", "atlanan")}, moduller=",".join(sorted(moduller or [])))
    log(f"bitti: {ilerleme['yapilan']} üretildi, {ilerleme['hata']} hata, {ilerleme['atlanan']} atlandı ({time.time() - t0:.0f} sn)")
    return 1 if ilerleme["hata"] else 0


if __name__ == "__main__" and "--yeniden" in sys.argv:
    sys.exit(_yeniden(sys.argv[1:]))
