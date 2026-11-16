#!/usr/bin/env python3
"""Ses kalite kapısı + kayıt↔disk↔Oracle tutarlılık denetimi (2026-11-16; ses üretmez, GPU/LLM yok — yalnız ffprobe/ffmpeg CPU).

Neden: ses hattında LUFS/kırpılma/yarım klip/baş-son sessizlik denetimi yoktu; aktarım (meds-ses-aktar rsync'i) karşı tarafta
boyut doğrulamıyordu; kayıtsız sesler ve `.parca/` artıkları görünmüyordu (bkz. docs/hatalar/ses.md H11, H13, H539).

Kullanım:
  python3 scripts/uretim/ses_ortak/ses_kapisi.py <hedef> [--kok <data kökü>] [--ornek N | --hepsi] [--json]
      <hedef>: kök adı (patoloji_cozucu, k2farmakoloji_asistan, ogren_ses, terim_ses, sesli_anlatim, ek_moduller/<modül>)
               ya da alt birim (patoloji_cozucu/01, ogren_ses/<deste>) ya da sesli ders anahtarı (k2-22-…).
      Varsayılan --ornek 40 (birim başına rastgele, tohum sabit). 0 HATA → çıkış 0, aksi 1; hedef bulunamazsa 2.
  python3 … ses_kapisi.py tara --hepsi [--ornek 40] [--json]   tüm ses köklerinde modül başına sağlık tablosu
  python3 … ses_kapisi.py oracle <hedef|--hepsi>               yerel ↔ Oracle dosya listesi + BOYUT (salt okunur ssh find)
  python3 … ses_kapisi.py artik [--json]                       .parca/, kayıtsız ses, *.yedek.mp3 raporu (SİLMEZ)

Denetimler (her dosya: ffprobe + `ffmpeg -af volumedetect,silencedetect -f null -`; sonuç önbelleği
~/.cache/meds/ses_kapisi.sqlite, anahtar (yol, boyut, mtime, ÖLÇÜM_SÜRÜMÜ)):
  HATA : okunamıyor/çözme hatası, süre 0, kayıtta olup diskte yok, tümüyle sessiz, kayıttaki süreden çözülen süre belirgin
         kısa (yarım dosya), örnekleme hızı/kanal kökün baskın biçiminden farklı, ortalama düzey kaba bant dışında,
         süre/karakter oranı kaba bant dışında.
  UYARI: diskte olup kayıtta yok, tepe ≥ −0,5 dBFS (kırpılma şüphesi), baş sessizliği > 0,6 sn, son sessizliği > 1,2 sn,
         ortalama düzey hedef bandı dışında (sesli derslerde dersler arası fark yalnız UYARI — mevcut sesler yeniden
         üretilmeyecek, kullanıcı kararı), süre/karakter oranı motor eşiği dışında.
Eşikler 2026-11-16 mevcut üretimde ölçüldü (yanlış alarm oranı: başlık altındaki ESIK yorumları); gevşetmek YASAK (kapilar/CLAUDE.md).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in sys.path:
    sys.path.append(str(_d))
import kok as _kok  # noqa: E402

DATA = _kok.MEDS / "data"
UZAK_DATA = "/home/ubuntu/medsor/meds/data"  # deploy/oracle/deploy-code.sh ORACLE_DIR/data; yerel_sesleri_tasi.py UZAK
ONBELLEK = Path.home() / ".cache/meds/ses_kapisi.sqlite"
OLCUM_SURUMU = 3  # ölçüm biçimi değişince artır → önbellek geçersiz

# ── ESİKLER (2026-11-16 ölçümü; `tara --hepsi --ornek 40` ≈ 2.400 dosya + sesli ders 70 ses) ───────────────────────────
# Ortalama düzey (mean_volume, dBFS). Ölçülen: EMA klipleri −24…−28 (medyan ≈ −25,8), sesli dersler −17…−26.
#   HATA bandı kabadır (bozuk/boş/aşırı yüksek ses yakalanır, sağlam üretimin hiçbiri düşmez);
#   UYARI bandı EMA dağılımının ±~3 dB çevresi.
DUZEY_HATA = (-40.0, -12.0)
DUZEY_UYARI = {"klip": (-30.0, -21.0), "ders": (-28.0, -16.0)}
SESSIZ_TEPE = -50.0      # max_volume bunun altındaysa tümüyle sessiz → HATA
KIRPILMA_TEPE = -0.5     # max_volume ≥ bu → kırpılma şüphesi (UYARI; EMA çıktısı np.clip ile ±1'e kırpılıyor)
BAS_SESSIZ = 0.6         # sn; UYARI
SON_SESSIZ = 1.2         # sn; UYARI
SESSIZ_ESIK = "-50dB"    # silencedetect gürültü eşiği (EMA klip arası duraklar −60 dB altı)
SESSIZ_SURE = 0.3        # silencedetect en kısa sessizlik
# Süre/karakter: motor (ema_isci.paragraf_seslendir) beklenen = karakter / 18 (hız 1); kabul 0,55–1,8. Kayıttaki metin
# okunuş dönüşümünden ÖNCEKİ metin olduğu için (kısaltma açılımı uzatır) gevşek hâli kullanılır.
KARAKTER_SN = 18.0
ORAN_UYARI = (0.55, 1.8)
ORAN_HATA = (0.35, 3.0)
# Kayıttaki süre ↔ çözülen süre: yarım/kesik dosya. Klipte 0,25 sn ya da %3'ten fazla KISA olması HATA.
SURE_FARK_SN = 0.25
SURE_FARK_ORAN = 0.03
YEREL_SAGLAYICI = {"xtts-yerel", "ema-yerel"}  # sesli dersin yerelde dosyası olması beklenen sağlayıcılar


# ── veri modeli ─────────────────────────────────────────────────────────────────────────────────────────────────────
@dataclass
class Oge:
    yol: Path
    tur: str                      # "klip" | "ders"
    sure: float | None = None     # kayıttaki süre (sn)
    karakter: int | None = None   # kayıttaki okunacak metin uzunluğu


@dataclass
class Birim:
    ad: str
    tur: str
    ogeler: list[Oge] = field(default_factory=list)
    eksik: list[str] = field(default_factory=list)    # kayıtta var, diskte yok
    kayitsiz: list[Path] = field(default_factory=list)  # diskte var, kayıtta yok
    not_: list[str] = field(default_factory=list)


def _json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return e


def _klip_dizini(ad: str, d: Path, kok: Path) -> Birim:
    """kayit.json {klip: {h, sure, zaman, cumleler?}} + <klip>.mp3 düzeni (çözücü, asistan, ogren_ses)."""
    b = Birim(ad, "klip")
    k = _json(d / "kayit.json")
    if isinstance(k, Exception) or not isinstance(k, dict):
        b.eksik.append(f"{d.relative_to(kok)}/kayit.json okunamadı: {k}")
        return b
    for klip, r in k.items():
        p = d / f"{klip}.mp3"
        if not p.exists():
            b.eksik.append(str(p.relative_to(kok)))
            continue
        r = r if isinstance(r, dict) else {}
        cum = r.get("cumleler")
        b.ogeler.append(Oge(p, "klip", r.get("sure"), sum(len(c) for c in cum) if isinstance(cum, list) else None))
    for p in d.glob("*.mp3"):
        if p.stem not in k:
            b.kayitsiz.append(p)
    return b


def _birlestir(ad: str, parcalar: list[Birim]) -> Birim:
    b = Birim(ad, parcalar[0].tur if parcalar else "klip")
    for x in parcalar:
        b.ogeler += x.ogeler
        b.eksik += x.eksik
        b.kayitsiz += x.kayitsiz
        b.not_ += x.not_
    return b


def _sesli(kok: Path, anahtarlar: list[str] | None) -> Birim:
    sa = kok / "sesli_anlatim"
    kayit = _json(sa / "kayit.json")
    b = Birim("sesli_anlatim" if anahtarlar is None else anahtarlar[0], "ders")
    if not isinstance(kayit, dict):
        b.eksik.append(f"sesli_anlatim/kayit.json okunamadı: {kayit}")
        return b
    tum = anahtarlar or list(dict.fromkeys(list(kayit) + [d.name for d in sorted((sa / "ses").glob("*")) if d.is_dir()]))
    for key in tum:
        ids = set()
        for v in kayit.get(key, []):
            ids.add(v.get("id"))
            p = sa / "ses" / key / f"{v.get('id')}.mp3"
            if p.exists():
                b.ogeler.append(Oge(p, "ders", v.get("sureSn")))
            elif v.get("saglayici") in YEREL_SAGLAYICI:
                b.eksik.append(str(p.relative_to(kok)))
        d = sa / "ses" / key
        if d.is_dir():
            b.kayitsiz += [p for p in d.glob("*.mp3") if p.stem not in ids]
    nyerel = sum(1 for vs in kayit.values() for v in vs if v.get("saglayici") not in YEREL_SAGLAYICI)
    if anahtarlar is None and nyerel:
        b.not_.append(f"{nyerel} varyant yerel olmayan sağlayıcıdan (Oracle'da üretilir; yerelde dosyası beklenmez)")
    return b


def _terim(kok: Path) -> Birim:
    d = kok / "terim_ses"
    k = _json(d / "kayit.json")
    b = Birim("terim_ses", "klip")
    if not isinstance(k, dict):
        b.eksik.append(f"terim_ses/kayit.json okunamadı: {k}")
        return b
    for h, r in k.items():
        p = d / h[:2] / f"{h}.mp3"
        if p.exists():
            b.ogeler.append(Oge(p, "klip", r.get("sure"), len(r.get("m") or "") or None))
        else:
            b.eksik.append(str(p.relative_to(kok)))
    b.kayitsiz = [p for p in d.glob("*/*.mp3") if p.stem not in k]
    return b


def _ek_modul(kok: Path, modul: str) -> Birim:
    d = kok / "ek_moduller" / "ses" / modul
    b = Birim(f"ek_moduller/{modul}", "klip")
    k = _json(_kok.MEDS / "src/data/ek_moduller" / modul / "klip.json")
    if not isinstance(k, dict):
        b.eksik.append(f"src/data/ek_moduller/{modul}/klip.json okunamadı: {k}")
        return b
    for klip, r in k.items():
        p = d / f"{klip}.mp3"
        if p.exists():
            b.ogeler.append(Oge(p, "klip", (r or {}).get("sure")))
        else:
            b.eksik.append(str(p.relative_to(kok)))
    b.kayitsiz = [p for p in d.glob("*.mp3") if p.stem not in k]
    return b


def kokler(kok: Path) -> list[str]:
    """Ses taşıyan bütün kök adları (tara --hepsi)."""
    ad = sorted(p.parent.name for p in kok.glob("*/ses*/") if p.is_dir() and any(p.glob("*/kayit.json")))
    ad += [x for x in ("ogren_ses", "terim_ses", "sesli_anlatim") if (kok / x).is_dir()]
    ad += [f"ek_moduller/{p.name}" for p in sorted((kok / "ek_moduller/ses").glob("*")) if p.is_dir()]
    return list(dict.fromkeys(ad))


def yol_kok_adi(hedef: str, kok: Path) -> str | None:
    """Kök adı yerine dizin YOLU verilmişse (ör. data/k2psikiyatri_cozucu/ses) onu içeren bilinen kök adı."""
    p = Path(hedef)
    try:
        rel = (p if p.is_absolute() else Path.cwd() / p).resolve().relative_to(kok.resolve()).as_posix()
    except ValueError:
        rel = hedef.strip("/")
        for on in ("meds/data/", "data/"):
            if rel.startswith(on):
                rel = rel[len(on):]
                break
    eslesme = []
    for ad in kokler(kok):
        dz = f"ek_moduller/ses/{ad.split('/', 1)[1]}" if ad.startswith("ek_moduller/") else ad
        if rel == dz or rel.startswith(dz + "/"):
            eslesme.append((len(dz), ad))
    return max(eslesme)[1] if eslesme and max(eslesme)[1] != hedef else None


def hedef_yok_mesaji(hedef: str, kok: Path) -> str:
    oneri = yol_kok_adi(hedef, kok)
    m = f"HATA  hedef bulunamadı: {hedef} (kök: {kok}). <hedef> dizin yolu değil, kök ADIdır."
    if oneri:
        m += f"\n      Bunu mu demek istediniz: {oneri}"
    return m + "\n      Geçerli kök adları: " + ", ".join(kokler(kok))


def coz(hedef: str, kok: Path) -> Birim | None:
    b = _coz(hedef, kok)
    if b is None and (ad := yol_kok_adi(hedef, kok)):
        print(f"UYARI hedef yol olarak verildi: {hedef} → kök adı '{ad}' ile devam ediliyor", file=sys.stderr)
        b = _coz(ad, kok)
    return b


def _coz(hedef: str, kok: Path) -> Birim | None:
    hedef = hedef.strip("/")
    if hedef == "sesli_anlatim":
        return _sesli(kok, None)
    if hedef == "terim_ses":
        return _terim(kok)
    if hedef.startswith("ek_moduller/"):
        return _ek_modul(kok, hedef.split("/", 1)[1])
    if (kok / "ek_moduller/ses" / hedef).is_dir():
        return _ek_modul(kok, hedef)
    if hedef == "ogren_ses":
        return _birlestir(hedef, [_klip_dizini(f"ogren_ses/{p.parent.name}", p.parent, kok)
                                  for p in sorted((kok / "ogren_ses").glob("*/kayit.json"))])
    if (kok / "ogren_ses" / hedef / "kayit.json").exists():
        hedef = f"ogren_ses/{hedef}"
    d = kok / hedef
    if (d / "kayit.json").exists():
        return _klip_dizini(hedef, d, kok)
    if d.is_dir():
        alt = sorted(d.glob("ses*/*/kayit.json")) or sorted(d.glob("*/kayit.json"))
        if alt:
            return _birlestir(hedef, [_klip_dizini(str(p.parent.relative_to(kok)), p.parent, kok) for p in alt])
    sk = _json(kok / "sesli_anlatim/kayit.json")
    if isinstance(sk, dict) and hedef in sk:
        return _sesli(kok, [hedef])
    return None


# ── ölçüm ───────────────────────────────────────────────────────────────────────────────────────────────────────────
_RE = {
    "mean": re.compile(r"mean_volume: (-?[\d.]+|-inf) dB"),
    "max": re.compile(r"max_volume: (-?[\d.]+|-inf) dB"),
    "n": re.compile(r"n_samples: (\d+)"),
    "ss": re.compile(r"silence_start: (-?[\d.]+)"),
    "se": re.compile(r"silence_end: (-?[\d.]+)"),
}
_HATA_SATIR = re.compile(r"error|invalid|corrupt|header missing|incomplete|truncat|could not", re.I)


def olc(yol: Path) -> dict:
    """ffprobe + ffmpeg (volumedetect, silencedetect). Dönüş: ölçüm sözlüğü (asla istisna fırlatmaz)."""
    r: dict = {"ok": True}
    try:
        pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,sample_rate,channels,bit_rate:format=duration",
                             "-of", "json", str(yol)], capture_output=True, text=True, timeout=60)
        j = json.loads(pr.stdout or "{}")
        st = [s for s in j.get("streams", []) if s.get("codec_type") == "audio"]
        if pr.returncode or not st:
            return {"ok": False, "hata": (pr.stderr.strip() or "ses akışı yok")[:200]}
        r["sr"] = int(st[0].get("sample_rate") or 0)
        r["kanal"] = int(st[0].get("channels") or 0)
        r["kbps"] = round(int(st[0].get("bit_rate") or 0) / 1000)
        r["baslik_sure"] = float(j.get("format", {}).get("duration") or 0)
        ff = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-threads", "1", "-i", str(yol), "-af",
                             f"volumedetect,silencedetect=n={SESSIZ_ESIK}:d={SESSIZ_SURE}", "-f", "null", "-"],
                            capture_output=True, text=True, timeout=600)
        e = ff.stderr
        if ff.returncode:
            return {"ok": False, "hata": e.strip().splitlines()[-1][:200] if e.strip() else f"ffmpeg çıkış {ff.returncode}"}
        r["cozme_hatasi"] = [s.strip()[:160] for s in e.splitlines() if _HATA_SATIR.search(s) and "silence" not in s][:3]
        # volumedetect özeti iki kez basılabiliyor (ilki boş: n_samples 0) → SON eşleşme alınır
        def f(k):
            m = _RE[k].findall(e)
            return None if not m else (float("-inf") if m[-1] == "-inf" else float(m[-1]))
        r["mean"], r["max"] = f("mean"), f("max")
        n = _RE["n"].findall(e)
        r["sure"] = round(int(n[-1]) / max(1, r["sr"]) / max(1, r["kanal"]), 3) if n else 0.0
        ss = [float(x) for x in _RE["ss"].findall(e)]
        se = [float(x) for x in _RE["se"].findall(e)]
        r["bas_ses"] = round(se[0], 3) if ss and ss[0] <= 0.02 and se else 0.0
        r["son_ses"] = 0.0
        if ss:
            son_bitis = se[len(ss) - 1] if len(se) >= len(ss) else r["sure"]
            if son_bitis >= r["sure"] - 0.05:
                r["son_ses"] = round(r["sure"] - ss[-1], 3)
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "hata": f"{type(ex).__name__}: {ex}"[:200]}
    return r


class Onbellek:
    def __init__(self, yol: Path = ONBELLEK):
        yol.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(yol), check_same_thread=False, timeout=30)
        self.db.execute("CREATE TABLE IF NOT EXISTS olcum (yol TEXT PRIMARY KEY, boyut INT, mtime REAL, surum INT, veri TEXT)")

    def al(self, p: Path, st) -> dict | None:
        row = self.db.execute("SELECT boyut, mtime, surum, veri FROM olcum WHERE yol=?", (str(p),)).fetchone()
        if row and row[0] == st.st_size and row[1] == st.st_mtime and row[2] == OLCUM_SURUMU:
            return json.loads(row[3])
        return None

    def koy(self, kayitlar: list[tuple]) -> None:
        self.db.executemany("INSERT OR REPLACE INTO olcum VALUES (?,?,?,?,?)", kayitlar)
        self.db.commit()


def olc_hepsi(ogeler: list[Oge]) -> dict[Path, dict]:
    ob = Onbellek()
    sonuc: dict[Path, dict] = {}
    yap: list[tuple[Path, os.stat_result]] = []
    for o in ogeler:
        try:
            st = o.yol.stat()
        except OSError as e:
            sonuc[o.yol] = {"ok": False, "hata": str(e)}
            continue
        c = ob.al(o.yol, st)
        if c is not None:
            sonuc[o.yol] = c
        else:
            yap.append((o.yol, st))
    if yap:
        yeni = []
        with cf.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
            for (p, st), r in zip(yap, ex.map(lambda a: olc(a[0]), yap)):
                sonuc[p] = r
                yeni.append((str(p), st.st_size, st.st_mtime, OLCUM_SURUMU, json.dumps(r)))
        ob.koy(yeni)
    return sonuc


# ── değerlendirme ───────────────────────────────────────────────────────────────────────────────────────────────────
def degerlendir(b: Birim, olcum: dict[Path, dict], kok: Path) -> tuple[list[str], list[str]]:
    hata: list[str] = [f"kayıtta var, diskte yok: {x}" for x in b.eksik]
    uyari: list[str] = [f"diskte var, kayıtta yok: {p.relative_to(kok)}" for p in b.kayitsiz]
    bicim: dict[tuple, int] = {}
    for o in b.ogeler:
        r = olcum.get(o.yol, {})
        if r.get("ok"):
            bicim[(r["sr"], r["kanal"])] = bicim.get((r["sr"], r["kanal"]), 0) + 1
    baskin = max(bicim, key=bicim.get) if bicim else None
    bant = DUZEY_UYARI[b.tur]
    for o in b.ogeler:
        g = o.yol.relative_to(kok)
        r = olcum.get(o.yol, {})
        if not r.get("ok"):
            hata.append(f"okunamıyor: {g} — {r.get('hata')}")
            continue
        if r.get("cozme_hatasi"):
            hata.append(f"çözme hatası (bozuk/yarım): {g} — {r['cozme_hatasi'][0]}")
        s = r.get("sure") or 0.0
        if s <= 0:
            hata.append(f"süre 0: {g}")
            continue
        if baskin and (r["sr"], r["kanal"]) != baskin:
            hata.append(f"biçim tutarsız: {g} {r['sr']} Hz/{r['kanal']} kanal (kökte baskın {baskin[0]} Hz/{baskin[1]} kanal)")
        if o.sure and s < o.sure - max(SURE_FARK_SN, SURE_FARK_ORAN * o.sure):
            hata.append(f"yarım dosya: {g} çözülen {s:.2f} sn < kayıttaki {o.sure:.2f} sn")
        mx, mn = r.get("max"), r.get("mean")
        if mx is None or mx < SESSIZ_TEPE:
            hata.append(f"tümüyle sessiz: {g} (tepe {mx} dB)")
            continue
        if mn is not None and not (DUZEY_HATA[0] <= mn <= DUZEY_HATA[1]):
            hata.append(f"düzey kaba bant dışında: {g} ortalama {mn:.1f} dB (bant {DUZEY_HATA[0]:.0f}…{DUZEY_HATA[1]:.0f})")
        elif mn is not None and not (bant[0] <= mn <= bant[1]):
            uyari.append(f"düzey hedef bandı dışında: {g} ortalama {mn:.1f} dB (hedef {bant[0]:.0f}…{bant[1]:.0f})")
        if mx >= KIRPILMA_TEPE:
            uyari.append(f"kırpılma şüphesi: {g} tepe {mx:.1f} dB")
        if r.get("bas_ses", 0) > BAS_SESSIZ:
            uyari.append(f"baş sessizliği: {g} {r['bas_ses']:.2f} sn")
        if r.get("son_ses", 0) > SON_SESSIZ:
            uyari.append(f"son sessizliği: {g} {r['son_ses']:.2f} sn")
        if o.karakter and o.karakter >= 20:
            oran = s / max(1.0, o.karakter / KARAKTER_SN)
            if not (ORAN_HATA[0] <= oran <= ORAN_HATA[1]):
                hata.append(f"süre/karakter kaba bant dışında: {g} oran {oran:.2f} ({o.karakter} karakter, {s:.1f} sn)")
            elif not (ORAN_UYARI[0] <= oran <= ORAN_UYARI[1]):
                uyari.append(f"süre/karakter motor eşiği dışında: {g} oran {oran:.2f}")
    return hata, uyari


def ornekle(b: Birim, n: int | None) -> list[Oge]:
    if n is None or len(b.ogeler) <= n:
        return b.ogeler
    return random.Random(f"ses_kapisi:{b.ad}").sample(b.ogeler, n)


def denetle(hedef: str, kok: Path, n: int | None) -> dict | None:
    b = coz(hedef, kok)
    if b is None:
        return None
    t0 = time.time()
    secili = ornekle(b, n)
    olcum = olc_hepsi(secili)
    hata, uyari = degerlendir(Birim(b.ad, b.tur, secili, b.eksik, b.kayitsiz, b.not_), olcum, kok)
    ok = [olcum[o.yol] for o in secili if olcum.get(o.yol, {}).get("ok")]
    duz = sorted(r["mean"] for r in ok if r.get("mean") is not None)
    return {"ad": b.ad, "tur": b.tur, "toplam": len(b.ogeler), "olculen": len(secili), "eksik": len(b.eksik),
            "kayitsiz": len(b.kayitsiz), "hata": hata, "uyari": uyari, "not": b.not_,
            "hatali_dosya": len({h.split(": ", 1)[1].split(" ")[0] for h in hata if ": " in h}),
            "duzey": [duz[0], duz[len(duz) // 2], duz[-1]] if duz else None,
            "bicim": sorted({f"{r['sr']}Hz/{r['kanal']}k/{r['kbps']}kbps" for r in ok}),
            "sn": round(time.time() - t0, 1)}


def yaz(s: dict, ayrinti: int = 50) -> None:
    for h in s["hata"][:ayrinti]:
        print(f"HATA  {h}")
    for u in s["uyari"][:ayrinti]:
        print(f"UYARI {u}")
    if len(s["hata"]) > ayrinti or len(s["uyari"]) > ayrinti:
        print(f"… (+{max(0, len(s['hata']) - ayrinti)} HATA, +{max(0, len(s['uyari']) - ayrinti)} UYARI daha; --json ile hepsi)")
    for x in s["not"]:
        print(f"NOT   {x}")
    d = s["duzey"]
    print(f"== {s['ad']}: {s['olculen']}/{s['toplam']} ses ölçüldü · {len(s['hata'])} HATA · {len(s['uyari'])} UYARI · "
          f"eksik {s['eksik']} · kayıtsız {s['kayitsiz']} · düzey {d[0]:.1f}/{d[1]:.1f}/{d[2]:.1f} dB (en düşük/medyan/en yüksek) · "
          f"{', '.join(s['bicim'])} · {s['sn']} sn" if d else
          f"== {s['ad']}: {s['olculen']}/{s['toplam']} ses · {len(s['hata'])} HATA · {len(s['uyari'])} UYARI · eksik {s['eksik']}")


# ── alt komutlar ────────────────────────────────────────────────────────────────────────────────────────────────────
def k_tara(a) -> int:
    kok = Path(a.kok)
    satirlar = []
    for ad in kokler(kok):
        s = denetle(ad, kok, None if a.tumu else a.ornek)
        if s:
            satirlar.append(s)
    if a.json:
        print(json.dumps(satirlar, ensure_ascii=False, indent=1))
    else:
        print(f"{'modül':<30} {'toplam':>7} {'örnek':>6} {'HATA':>5} {'UYARI':>6} {'eksik':>6} {'kayıtsız':>8}  düzey min/med/max dB")
        for s in satirlar:
            d = s["duzey"]
            dz = f"{d[0]:.1f}/{d[1]:.1f}/{d[2]:.1f}" if d else "-"
            print(f"{s['ad']:<30} {s['toplam']:>7} {s['olculen']:>6} {len(s['hata']):>5} {len(s['uyari']):>6} {s['eksik']:>6} {s['kayitsiz']:>8}  {dz}")
        top = sum(s["olculen"] for s in satirlar)
        hd = sum(s["hatali_dosya"] for s in satirlar)
        print(f"== toplam {top} ses ölçüldü · {sum(len(s['hata']) for s in satirlar)} HATA ({hd} dosya/kayıt, "
              f"%{100 * hd / max(1, top):.2f}) · {sum(len(s['uyari']) for s in satirlar)} UYARI")
        for s in satirlar:
            for h in s["hata"][:5]:
                print(f"HATA  [{s['ad']}] {h}")
    return 1 if any(s["hata"] for s in satirlar) else 0


def uzak_liste(goreli_kok: str) -> dict[str, int] | None:
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "medsor-oracle",
                        f"sudo find {UZAK_DATA}/{goreli_kok} -type f -name '*.mp3' -not -path '*/.parca/*' -printf '%P\\t%s\\n' 2>/dev/null || true"],
                       capture_output=True, text=True, timeout=600)
    if r.returncode:
        print(f"HATA  ssh: {r.stderr.strip()[:300]}", file=sys.stderr)
        return None
    out = {}
    for s in r.stdout.splitlines():
        if "\t" in s:
            p, n = s.rsplit("\t", 1)
            out[p] = int(n)
    return out


def oracle_karsilastir(dosyalar: list[Path], goreli_kok: str, kok: Path) -> dict:
    """dosyalar: yerelde beklenen MP3'ler (kok/goreli_kok altında). Salt okunur; hiçbir şey göndermez/silmez."""
    uz = uzak_liste(goreli_kok)
    if uz is None:
        return {"hedef": goreli_kok, "erisim": False}
    taban = kok / goreli_kok
    eksik, fark = [], []
    for p in dosyalar:
        g = str(p.relative_to(taban))
        n = p.stat().st_size
        if g not in uz:
            eksik.append(g)
        elif uz[g] != n:
            fark.append(f"{g} yerel {n} ≠ Oracle {uz[g]}")
    return {"hedef": goreli_kok, "erisim": True, "yerel": len(dosyalar), "oracle": len(uz), "eksik": eksik, "boyut_farki": fark}


def oracle_yaz(s: dict) -> int:
    if not s.get("erisim"):
        print(f"HATA  {s['hedef']}: Oracle'a erişilemedi")
        return 1
    for x in s["eksik"][:30]:
        print(f"HATA  Oracle'da yok: {s['hedef']}/{x}")
    for x in s["boyut_farki"][:30]:
        print(f"HATA  boyut farklı: {s['hedef']}/{x}")
    print(f"== {s['hedef']}: yerel {s['yerel']} · Oracle {s['oracle']} · eksik {len(s['eksik'])} · boyut farkı {len(s['boyut_farki'])}")
    return 1 if s["eksik"] or s["boyut_farki"] else 0


def k_oracle(a) -> int:
    kok = Path(a.kok)
    hedefler = [x for x in kokler(kok) if x != "sesli_anlatim"] if a.tumu else [a.hedef]
    kod = 0
    sonuc = []
    for h in hedefler:
        if h == "sesli_anlatim" or not h:
            print("NOT   sesli ders için: yerel_sesleri_tasi.py --dogrula")
            continue
        b = coz(h, kok)
        if b is None:
            print(hedef_yok_mesaji(h, kok))
            return 2
        gk = h.split("/")[0] if not h.startswith("ek_moduller/") else f"ek_moduller/ses/{h.split('/', 1)[1]}"
        s = oracle_karsilastir([o.yol for o in b.ogeler], gk, kok)
        sonuc.append(s)
        kod |= oracle_yaz(s)
    if a.json:
        print(json.dumps(sonuc, ensure_ascii=False, indent=1))
    return kod


def k_artik(a) -> int:
    kok = Path(a.kok)
    simdi = time.time()
    kalemler = []
    for d in kok.glob("**/.parca"):
        dosya = [p for p in d.rglob("*") if p.is_file()]
        if dosya:
            kalemler.append(("parca", d, len(dosya), sum(p.stat().st_size for p in dosya), max(p.stat().st_mtime for p in dosya)))
    for p in kok.rglob("*.yedek.mp3"):
        kalemler.append(("yedek", p, 1, p.stat().st_size, p.stat().st_mtime))
    for ad in kokler(kok):
        b = coz(ad, kok)
        for p in (b.kayitsiz if b else []):
            if not p.name.endswith(".yedek.mp3"):
                kalemler.append(("kayitsiz", p, 1, p.stat().st_size, p.stat().st_mtime))
    ozet: dict[str, list] = {}
    for t, p, n, bayt, mt in kalemler:
        o = ozet.setdefault(t, [0, 0])
        o[0] += n
        o[1] += bayt
    if a.json:
        print(json.dumps([{"tur": t, "yol": str(p.relative_to(kok)), "dosya": n, "bayt": b_, "yas_gun": round((simdi - mt) / 86400, 1)}
                          for t, p, n, b_, mt in kalemler], ensure_ascii=False, indent=1))
    else:
        for t, p, n, bayt, mt in sorted(kalemler, key=lambda x: -x[3])[: a.n]:
            print(f"{t:<9} {bayt / 1e6:8.1f} MB {n:>5} dosya {(simdi - mt) / 86400:6.0f} gün  {p.relative_to(kok)}")
        for t, (n, bayt) in ozet.items():
            print(f"== {t}: {n} dosya, {bayt / 1e6:.0f} MB")
    # veri_bakim.py aday kalıpları (o dosyaya DOKUNULMAZ; yalnız öneri)
    try:
        vb = (_kok.SCRIPTS / "altyapi/veri_bakim.py").read_text(encoding="utf-8")
        if ".parca" not in vb:
            print("ÖNERİ veri_bakim.py aday listesinde `.parca/` yok — ses birleştirme artıkları (yaşı > 2 gün) arşiv adayı olmalı.")
        if "kayitsiz" not in vb and "kayıtsız" not in vb:
            print("ÖNERİ veri_bakim.py kayıtsız sesleri (kayit.json'da olmayan MP3) tanımıyor — `ses_kapisi.py artik --json` çıktısı aday kaynağı olabilir.")
    except OSError:
        pass
    print("NOT   bu komut hiçbir şey silmez/taşımaz; arşivleme scripts/altyapi/veri_bakim.py işidir.")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    alt = argv[0] if argv and argv[0] in ("tara", "oracle", "artik") else None
    ap = argparse.ArgumentParser(description="Ses kalite kapısı (ses_kapisi.py)")
    if alt:
        argv = argv[1:]
    if alt in (None, "oracle"):
        ap.add_argument("hedef", nargs="?" if alt == "oracle" else None, default="")
    ap.add_argument("--kok", default=str(DATA), help="veri kökü (varsayılan meds/data)")
    ap.add_argument("--ornek", type=int, default=40, help="birim başına örnek (varsayılan 40)")
    ap.add_argument("--hepsi", dest="tumu", action="store_true", help="tara/oracle: bütün kökler; tek hedefte: örneklemsiz tüm dosyalar")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--n", type=int, default=40, help="artik: listelenecek en büyük kalem sayısı")
    a = ap.parse_args(argv)
    try:
        os.nice(10)
    except OSError:
        pass
    if alt == "tara":
        if not a.tumu:
            a.tumu = False
        return k_tara(argparse.Namespace(kok=a.kok, ornek=a.ornek, tumu=False, json=a.json))
    if alt == "oracle":
        if not a.hedef and not a.tumu:
            ap.error("oracle: <hedef> ya da --hepsi")
        return k_oracle(a)
    if alt == "artik":
        return k_artik(a)
    s = denetle(a.hedef, Path(a.kok), None if a.tumu else a.ornek)
    if s is None:
        print(hedef_yok_mesaji(a.hedef, Path(a.kok)))
        return 2
    if a.json:
        print(json.dumps(s, ensure_ascii=False, indent=1))
    else:
        yaz(s)
    return 1 if s["hata"] else 0


if __name__ == "__main__":
    sys.exit(main())
