#!/usr/bin/env python3
"""Veri bakım aracı — data/ ve src/data/ büyük dosya, kopya ve yedek kalıntısı raporu + güvenli arşivleme.

Yalnız stdlib (+ varsa `zstd`; yoksa Python lzma/xz). LLM/ağ/GPU yok. Varsayılan KURU çalışır.

  python3 scripts/altyapi/veri_bakim.py rapor
  python3 scripts/altyapi/veri_bakim.py arsivle [--uygula]
  python3 scripts/altyapi/veri_bakim.py geri <özgün göreli yol>
  python3 scripts/altyapi/veri_bakim.py denetle        (çıkış ≠ 0: sınır aşıldı)

Arşiv: <PROJE>/_arsiv_veri/<YYYYMMDD>/<özgün göreli yol>.zst (+ MANIFEST.jsonl). Aynı adın çok sürümlü .bak'ları
tek tar + zstd --long ile sıkıştırılır. Her arşiv açılıp sha256 doğrulanmadan özgün silinmez.
Dokunulmaz: data/_yedek/site_ayar (canlı geri alma), kodda adı geçen dosyalar, son 48 saatte değişenler,
data/backups/catalog'da her ad için en yeni 2 .bak.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import io
import json
import lzma
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

_s = Path(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
if str(_s) not in sys.path:
    sys.path.append(str(_s))
import kok as _kok  # noqa: E402
import gunluk  # noqa: E402

MEDS: Path = _kok.MEDS
ARSIV_KOK: Path = _kok.PROJE / "_arsiv_veri"
MANIFEST = ARSIV_KOK / "MANIFEST.jsonl"
KAYNAK = "veri_bakim"
KOKLER = ("data", "src/data")
ATLA = {"node_modules", ".git", "__pycache__"}
MB = 1024 * 1024

YEDEK_DIZIN = ("data/backups/", "data/_yedek/")
YEDEK_ISTISNA = ("data/_yedek/site_ayar/", "data/_yedek/site_ayar")
DESENLER = ("*.bak", "*.yedek*", "*legacy_backup*", "*_supabase.json", "*.yedek.mp3", "*.kapanis-oncesi.mp3")
KATALOG = "data/backups/catalog/"
KATALOG_SAKLA = 2
TAZE_SN = 48 * 3600

# Ses artıkları (2026-11-16, H587 güncellemesi; kaynak: ses_ortak/ses_kapisi.py artik): yaşı > SES_ARTIK_GUN olanlar aday.
#   - data/sesli_anlatim/**/.parca/** : ses birleştirme parçaları (birleşik MP3 yazıldıktan sonra artık)
#   - kayıtsız sesli ders MP3'ü: data/sesli_anlatim/ses/<anahtar>/<id>.mp3, kayit.json[<anahtar>] içinde id yok
SES_ARTIK_GUN = 14
SES_PARCA_DESEN = "data/sesli_anlatim/**/.parca/**"
SESLI_KAYIT = "data/sesli_anlatim/kayit.json"
DENETLE_YEDEK_TAVAN = 300 * MB
DENETLE_CIFT_ESIK = 5 * MB
# src/data ↔ data aynı adlı, bayt bayt aynı >5 MB çiftler (2026-11-16). YALNIZ AZALIR: çift giderilince sil.
CIFT_IZINLI = {"notebooklm_contributions.json"}  # yalnız azalır; pastQuestions + lectureSummariesCatalog kopyaları 2026-11-16 arşivlendi

ZSTD = shutil.which("zstd")
UZANTI = ".zst" if ZSTD else ".xz"
SIKISTIRICI = "zstd -19 --long=27 -T0" if ZSTD else "Python lzma (xz, preset 9) — zstd bulunamadı"


# ------------------------------------------------------------------ yardımcılar
def gezin(kok: str):
    taban = MEDS / kok
    if not taban.is_dir():
        return
    for d, dizinler, dosyalar in os.walk(taban):
        dizinler[:] = [x for x in dizinler if x not in ATLA]
        for f in dosyalar:
            p = Path(d) / f
            if p.is_file() and not p.is_symlink():
                yield p


def goreli(p: Path) -> str:
    return p.relative_to(MEDS).as_posix()


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for parca in iter(lambda: f.read(MB), b""):
            h.update(parca)
    return h.hexdigest()


def insan(n: float) -> str:
    for b in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024 or b == "GB":
            return f"{n:.1f} {b}" if b != "B" else f"{int(n)} B"
        n /= 1024
    return str(n)


def yedek_aday_mi(g: str) -> bool:
    if g.startswith(YEDEK_ISTISNA):
        return False
    if g.startswith(YEDEK_DIZIN):
        return True
    ad = g.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(ad, d) for d in DESENLER)


def arama_anahtari(g: str) -> str:
    """Kodda aranacak ad. Yedek dizinindeki genel adlı kopyalar (ör. _yedek/<klasör>/question_cards.json) için
    özgün adı aramak her zaman 'referanslı' çıkar; o yüzden yedek alt klasörünün adı aranır."""
    for d in YEDEK_DIZIN:
        if g.startswith(d):
            parca = g[len(d):].split("/")
            if len(parca) > 1 and parca[0] != "catalog":
                return parca[0]
    return g.rsplit("/", 1)[-1]


def referanslar(anahtarlar: set[str]) -> set[str]:
    """Anahtarlardan kodda (ts/tsx/py/sh/mjs/mts) geçenler — tek rg çağrısı."""
    if not anahtarlar:
        return set()
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as t:
        t.write("\n".join(sorted(anahtarlar)))
    try:
        if shutil.which("rg"):
            cmd = ["rg", "-uu", "-o", "-N", "--no-filename", "-F", "-f", t.name,
                   "-g", "*.{ts,tsx,py,sh,mjs,mts}", "-g", "!node_modules", "-g", "!dist*",
                   "-g", "!scripts/arsiv", "-g", "!scripts/altyapi/veri_bakim.py", "."]
            r = subprocess.run(cmd, cwd=MEDS, capture_output=True, text=True, timeout=300)
            return {l.strip() for l in r.stdout.splitlines() if l.strip()} & anahtarlar
        bulunan: set[str] = set()  # rg yoksa yavaş Python araması
        for d, dz, fs in os.walk(MEDS):
            rel = Path(d).relative_to(MEDS).as_posix()
            dz[:] = [x for x in dz if x not in ATLA and not x.startswith("dist")
                     and not (rel == "scripts" and x == "arsiv")]
            for f in fs:
                if f.rsplit(".", 1)[-1] in {"ts", "tsx", "py", "sh", "mjs", "mts"} and f != "veri_bakim.py":
                    try:
                        metin = (Path(d) / f).read_text(encoding="utf-8", errors="ignore")
                    except OSError:
                        continue
                    bulunan |= {a for a in anahtarlar - bulunan if a in metin}
        return bulunan
    finally:
        os.unlink(t.name)


@__import__("functools").lru_cache(maxsize=1)
def _sesli_kayitli() -> dict[str, set[str]]:
    try:
        k = json.loads((MEDS / SESLI_KAYIT).read_text(encoding="utf-8"))
        return {a: {str(v.get("id")) for v in vs} for a, vs in k.items()}
    except (OSError, json.JSONDecodeError, AttributeError):
        return {}  # kayıt okunamazsa kayıtsız tespiti YAPILMAZ (hepsi kayıtsız sanılmasın)


def ses_artik_mi(g: str, mtime: float, simdi: float) -> bool:
    """.parca/ artığı ya da kayıtsız sesli ders MP3'ü ve SES_ARTIK_GUN'den eski."""
    if simdi - mtime < SES_ARTIK_GUN * 86400:
        return False
    if fnmatch.fnmatch(g, SES_PARCA_DESEN) and "/.parca/" in g:
        return True
    m = re.match(r"data/sesli_anlatim/ses/([^/]+)/([^/]+)\.mp3$", g)
    kayit = _sesli_kayitli()
    # anahtar kayıtta hiç yoksa klasördeki MP3'lerin hepsi kayıtsızdır (ses_kapisi.py _sesli ile aynı ölçüt)
    return bool(m and kayit and m.group(2) not in kayit.get(m.group(1), set()))


def adaylar() -> list[dict]:
    simdi = time.time()
    liste = []
    for k in KOKLER:
        for p in gezin(k):
            g = goreli(p)
            if yedek_aday_mi(g) or ses_artik_mi(g, p.stat().st_mtime, simdi):
                st = p.stat()
                liste.append({"yol": g, "boyut": st.st_size, "taze": simdi - st.st_mtime < TAZE_SN,
                              "anahtar": arama_anahtari(g), "mtime": st.st_mtime})
    ref = referanslar({a["anahtar"] for a in liste})
    for a in liste:
        a["ref"] = a["anahtar"] in ref
    # katalog: her ad için en yeni 2 .bak yerinde kalır
    gruplar = defaultdict(list)
    for a in liste:
        if a["yol"].startswith(KATALOG) and a["yol"].endswith(".bak"):
            gruplar[katalog_adi(a["yol"])].append(a)
    for ad, g in gruplar.items():
        for i, a in enumerate(sorted(g, key=lambda x: x["mtime"], reverse=True)):
            a["sakla"] = i < KATALOG_SAKLA
            a["grup"] = ad
    return sorted(liste, key=lambda a: -a["boyut"])


def katalog_adi(g: str) -> str:
    ad = g.rsplit("/", 1)[-1]
    m = re.match(r"(.+?)\.\d{4}-\d{2}-\d{2}T[\d-]+Z\.bak$", ad)
    return m.group(1) if m else re.sub(r"\.bak$", "", ad)


def neden_dokunma(a: dict) -> str:
    if a["ref"]:
        return "kodda referans"
    if a["taze"]:
        return "<48 saat"
    if a.get("sakla"):
        return "katalog en yeni 2"
    return ""


# ------------------------------------------------------------------ rapor
def rapor(_a) -> int:
    with gunluk.sure(KAYNAK, "rapor"):
        tum = [p for k in KOKLER for p in gezin(k)]
        boy = {p: p.stat().st_size for p in tum}
        print("== (a) En büyük 25 JSON ==")
        for p in sorted((p for p in tum if p.suffix == ".json"), key=lambda p: -boy[p])[:25]:
            print(f"  {insan(boy[p]):>10}  {goreli(p)}")

        print("\n== (b) Bayt bayt aynı kopyalar (>1 MB) ==")
        bs = defaultdict(list)
        for p in tum:
            if boy[p] > MB:
                bs[boy[p]].append(p)
        kopya_kazanc = 0
        for n, ps in sorted(bs.items(), reverse=True):
            if len(ps) < 2:
                continue
            hs = defaultdict(list)
            for p in ps:
                hs[sha(p)].append(p)
            for h, grup in hs.items():
                if len(grup) > 1:
                    kopya_kazanc += n * (len(grup) - 1)
                    print(f"  {insan(n):>10} ×{len(grup)}  " + "  ==  ".join(goreli(p) for p in grup))
        print(f"  toplam yinelenen bayt: {insan(kopya_kazanc)}")

        print("\n== (c) Yedek/kalıntı adayları ==")
        liste = adaylar()
        kazanc = 0
        for a in liste:
            nd = neden_dokunma(a)
            if not nd:
                kazanc += a["boyut"]
            print(f"  {insan(a['boyut']):>10}  {'REF' if a['ref'] else '   '}  {nd or 'ARŞİVLENİR':18} {a['yol']}")
        print(f"\n  aday {len(liste)} dosya / {insan(sum(a['boyut'] for a in liste))}; "
              f"arşivlenebilir {insan(kazanc)} (sıkıştırıcı: {SIKISTIRICI})")
    gunluk.olay(KAYNAK, "bilgi", "rapor", aday=len(liste), arsivlenebilir=kazanc, kopya=kopya_kazanc)
    return 0


# ------------------------------------------------------------------ arşivle
def sikistir(kaynak: Path, hedef: Path) -> None:
    hedef.parent.mkdir(parents=True, exist_ok=True)
    gecici = hedef.with_name(hedef.name + ".yaziliyor")
    if ZSTD:
        subprocess.run([ZSTD, "-19", "--long=27", "-T0", "-q", "-f", str(kaynak), "-o", str(gecici)], check=True)
    else:
        with open(kaynak, "rb") as fi, lzma.open(gecici, "wb", preset=9) as fo:
            shutil.copyfileobj(fi, fo, MB)
    os.replace(gecici, hedef)


def ac_akis(arsiv: Path):
    """Arşivin açılmış içeriğini akış olarak verir (bayt üreteci)."""
    if arsiv.suffix == ".zst":
        pr = subprocess.Popen([ZSTD or "zstd", "-dc", "--long=27", str(arsiv)], stdout=subprocess.PIPE)
        assert pr.stdout
        yield from iter(lambda: pr.stdout.read(MB), b"")
        if pr.wait():
            raise RuntimeError(f"zstd açma başarısız: {arsiv}")
    else:
        with lzma.open(arsiv, "rb") as f:
            yield from iter(lambda: f.read(MB), b"")


def ac_dosyaya(arsiv: Path, hedef: Path) -> None:
    with open(hedef, "wb") as f:
        for p in ac_akis(arsiv):
            f.write(p)


def tar_uyeleri(arsiv: Path) -> dict[str, str]:
    """Tar arşivinin üyelerini açıp üye adı → sha256 döndürür (geçici dosyaya açarak)."""
    with tempfile.TemporaryDirectory(dir=arsiv.parent) as td:
        tar = Path(td) / "a.tar"
        ac_dosyaya(arsiv, tar)
        out = {}
        with tarfile.open(tar) as t:
            for m in t.getmembers():
                if m.isfile():
                    h = hashlib.sha256()
                    f = t.extractfile(m)
                    for parca in iter(lambda: f.read(MB), b""):
                        h.update(parca)
                    out[m.name] = h.hexdigest()
        return out


def manifest_yaz(kayit: dict) -> None:
    ARSIV_KOK.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")


def plan_kur(liste: list[dict]) -> list[dict]:
    """İş birimleri: {'tur': 'tek'|'tar', 'dosyalar': [...], 'arsiv': Path}."""
    gun = datetime.now().strftime("%Y%m%d")
    taban = ARSIV_KOK / gun
    isler, gruplar = [], defaultdict(list)
    for a in liste:
        if neden_dokunma(a):
            continue
        if a.get("grup"):
            gruplar[a["grup"]].append(a)
        else:
            isler.append({"tur": "tek", "dosyalar": [a], "arsiv": taban / (a["yol"] + UZANTI)})
    for ad, g in gruplar.items():
        if len(g) == 1:
            isler.append({"tur": "tek", "dosyalar": g, "arsiv": taban / (g[0]["yol"] + UZANTI)})
        else:
            isler.append({"tur": "tar", "dosyalar": g, "arsiv": taban / KATALOG / f"{ad}.bak-grubu.tar{UZANTI}"})
    return isler


def arsivle(a) -> int:
    liste = adaylar()
    isler = plan_kur(liste)
    toplam = sum(d["boyut"] for i in isler for d in i["dosyalar"])
    print(f"Sıkıştırıcı: {SIKISTIRICI}\nHedef: {ARSIV_KOK}\n")
    for i in isler:
        n = sum(d["boyut"] for d in i["dosyalar"])
        print(f"  [{i['tur']}] {insan(n):>10}  {len(i['dosyalar'])} dosya → {i['arsiv'].relative_to(ARSIV_KOK)}")
        if i["tur"] == "tar":
            for d in i["dosyalar"]:
                print(f"           - {d['yol']}")
    dokunma = [x for x in liste if neden_dokunma(x)]
    print(f"\nDokunulmayan {len(dokunma)}: " + ", ".join(f"{x['yol']} ({neden_dokunma(x)})" for x in dokunma[:40]))
    print(f"\nToplam {len(isler)} iş / {sum(len(i['dosyalar']) for i in isler)} dosya / {insan(toplam)} "
          f"(JSON/SQL için zstd -19 --long tipik oran ~%5–15 → tahmini arşiv {insan(toplam * 0.05)}–{insan(toplam * 0.15)})")
    if not a.uygula:
        print("\nKURU ÇALIŞMA — hiçbir dosya değişmedi. Uygulamak için: --uygula")
        gunluk.olay(KAYNAK, "bilgi", "arsivle kuru", is_sayisi=len(isler), bayt=toplam)
        return 0
    if not isler:
        return 0
    ARSIV_KOK.mkdir(parents=True, exist_ok=True)
    en_buyuk = max(d["boyut"] for i in isler for d in i["dosyalar"])
    bos = shutil.disk_usage(ARSIV_KOK).free
    if bos < 2 * en_buyuk:
        gunluk.olay(KAYNAK, "hata", "boş alan yetersiz", bos=bos, en_buyuk=en_buyuk)
        return 2
    hata = 0
    for i in isler:
        try:
            hata += 0 if isle(i) else 1
        except Exception as e:  # bir iş başarısızsa özgünler yerinde kalır, sıradakine geçilir
            hata += 1
            gunluk.olay(KAYNAK, "hata", f"iş başarısız: {e}", arsiv=str(i["arsiv"]))
    print(f"\nBitti: {len(isler) - hata} iş tamam, {hata} hata. Manifest: {MANIFEST}")
    return 1 if hata else 0


def isle(i: dict) -> bool:
    arsiv: Path = i["arsiv"]
    if arsiv.exists():
        gunluk.olay(KAYNAK, "uyari", "arşiv zaten var, atlandı", arsiv=str(arsiv))
        return False
    ozgun = {d["yol"]: sha(MEDS / d["yol"]) for d in i["dosyalar"]}
    if i["tur"] == "tek":
        sikistir(MEDS / i["dosyalar"][0]["yol"], arsiv)
        h = hashlib.sha256()
        for p in ac_akis(arsiv):
            h.update(p)
        dogru = {i["dosyalar"][0]["yol"]: h.hexdigest()}
    else:
        arsiv.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=arsiv.parent) as td:
            tar = Path(td) / "g.tar"
            with tarfile.open(tar, "w") as t:
                for d in i["dosyalar"]:
                    t.add(MEDS / d["yol"], arcname=d["yol"])
            sikistir(tar, arsiv)
        dogru = tar_uyeleri(arsiv)
    if any(dogru.get(y) != h for y, h in ozgun.items()):
        gunluk.olay(KAYNAK, "hata", "doğrulama tutmadı — özgünler silinmedi", arsiv=str(arsiv))
        return False
    zaman = datetime.now().isoformat(timespec="seconds")
    for d in i["dosyalar"]:
        manifest_yaz({"yol": d["yol"], "boyut": d["boyut"], "sha256": ozgun[d["yol"]],
                      "arsiv": str(arsiv), "tur": i["tur"], "uye": d["yol"] if i["tur"] == "tar" else None,
                      "zaman": zaman})
        (MEDS / d["yol"]).unlink()
        gunluk.olay(KAYNAK, "bilgi", "arşivlendi + özgün silindi", yol=d["yol"], arsiv=str(arsiv), boyut=d["boyut"])
    print(f"  ✓ {arsiv.relative_to(ARSIV_KOK)} ({insan(arsiv.stat().st_size)})")
    return True


# ------------------------------------------------------------------ geri
def geri(a) -> int:
    hedef_yol = a.yol.strip().lstrip("./")
    kayit = None
    if MANIFEST.exists():
        for satir in MANIFEST.read_text(encoding="utf-8").splitlines():
            try:
                k = json.loads(satir)
            except ValueError:
                continue
            if k.get("yol") == hedef_yol:
                kayit = k
    if not kayit:
        print(f"MANIFEST'te yok: {hedef_yol}")
        return 1
    hedef = MEDS / hedef_yol
    if hedef.exists():
        print(f"Hedef zaten var, üzerine yazılmaz: {hedef}")
        return 1
    hedef.parent.mkdir(parents=True, exist_ok=True)
    arsiv = Path(kayit["arsiv"])
    gecici = hedef.with_name(hedef.name + ".geri-aciliyor")
    if kayit.get("tur") == "tar":
        with tempfile.TemporaryDirectory(dir=arsiv.parent) as td:
            tar = Path(td) / "a.tar"
            ac_dosyaya(arsiv, tar)
            with tarfile.open(tar) as t, open(gecici, "wb") as fo:
                shutil.copyfileobj(t.extractfile(kayit["uye"]), fo, MB)
    else:
        ac_dosyaya(arsiv, gecici)
    if sha(gecici) != kayit["sha256"]:
        gecici.unlink()
        gunluk.olay(KAYNAK, "hata", "geri açma sha256 tutmadı", yol=hedef_yol)
        return 1
    os.replace(gecici, hedef)
    gunluk.olay(KAYNAK, "bilgi", "geri açıldı", yol=hedef_yol, arsiv=str(arsiv))
    print(f"Geri açıldı: {hedef_yol}")
    return 0


# ------------------------------------------------------------------ denetle
def denetle_bulgular() -> list[str]:
    """Sınır ihlalleri (boşsa temiz). yapi_koruma D10 da bunu çağırır."""
    out = []
    yedek = sum(p.stat().st_size for d in ("data/backups", "data/_yedek") for p in gezin(d))
    if yedek > DENETLE_YEDEK_TAVAN:
        out.append(f"data/backups + data/_yedek = {insan(yedek)} > {insan(DENETLE_YEDEK_TAVAN)} "
                   f"— python3 scripts/altyapi/veri_bakim.py arsivle")
    buyuk = defaultdict(dict)
    for k in KOKLER:
        for p in gezin(k):
            g = goreli(p)
            if g.startswith(YEDEK_DIZIN):
                continue
            n = p.stat().st_size
            if n > DENETLE_CIFT_ESIK:
                buyuk[k].setdefault(p.name, []).append((p, n))
    for ad, src in buyuk["src/data"].items():
        if ad in CIFT_IZINLI:
            continue
        for ps, ns in src:
            for pd, nd in buyuk["data"].get(ad, []):
                if ns == nd and sha(ps) == sha(pd):
                    out.append(f"aynı >5 MB kopya: {goreli(ps)} == {goreli(pd)} ({insan(ns)}) — biri tek kaynak olmalı")
    return out


def denetle(_a) -> int:
    b = denetle_bulgular()
    for x in b:
        print(f"HATA {x}")
    print(f"veri_bakim denetle: {len(b)} bulgu (izinli çiftler: {sorted(CIFT_IZINLI)})")
    if b:
        gunluk.olay(KAYNAK, "uyari", "denetle sınır aşıldı", bulgu=len(b))
    return 1 if b else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="data/ ve src/data/ bakım aracı (varsayılan kuru)")
    alt = ap.add_subparsers(dest="komut", required=True)
    alt.add_parser("rapor")
    s = alt.add_parser("arsivle")
    s.add_argument("--uygula", action="store_true", help="gerçekten arşivle ve özgünü sil (doğrulamadan sonra)")
    g = alt.add_parser("geri")
    g.add_argument("yol")
    alt.add_parser("denetle")
    a = ap.parse_args(argv)
    return {"rapor": rapor, "arsivle": arsivle, "geri": geri, "denetle": denetle}[a.komut](a)


if __name__ == "__main__":
    sys.exit(main())
