#!/usr/bin/env python3
"""Tek sağlık raporu (2026-11-16) — bugün kurulan ölçüm parçalarını tek ekranda toplar. LLM/GPU yok; yalnız stdlib.

  python3 scripts/altyapi/saglik_raporu.py [--canli] [--json] [--gun 1]
  python3 scripts/altyapi/saglik_raporu.py egilim [--n 10]

Bölümler: Sunucu (yerel :3000; --canli ile Oracle: health + telemetri + data/gunluk), İstemci (vitals p75 + canlı istemci
hataları), Veri (veri_bakim/veri.py denetimi, boyutlar), İçerik (manifest + kural_secici), Ses (ÖNBELLEKTEN; yeniden ölçmez),
Ön yüz paketi (dist), Günlük (kaynak × seviye). Her bölüm bağımsız; erişilemeyen kaynak "erişilemedi: <neden>" yazar.
Sonda tek hüküm satırı: SAĞLIK: iyi | dikkat (N) | sorun (N). Sorun varsa çıkış 1.
--json: makine çıktısı ../meds_temp/saglik/<zaman>.json'a da yazılır (son 30 kayıt tutulur).

Gizlilik: MEDS_PANEL_SECRET yalnız süreç içinde istek başlığıdır; hiçbir çıktıya/dosyaya yazılmaz. E-posta, uuid, IP maskelenir.
Oracle'a yazma yok (ssh yalnız tail/cat). Zamanlayıcı kurulmaz; elle çalıştırılır.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.insert(0, str(_d))
from kok import MEDS, PROJE, SCRIPTS  # noqa: E402

CANLI_URL = "https://nofrostlife.com.tr"
ORACLE_MEDS = "~/medsor/meds"
KAYIT_DIZINI = PROJE / "meds_temp" / "saglik"
ESIK = {"lcp": 2500, "inp": 200, "cls": 0.1}
KOVALAR = [10, 25, 50, 100, 250, 500, 1000, 2500]

satirlar: list[str] = []
dikkat: list[str] = []
sorun: list[str] = []
J: dict = {}


def yaz(s: str = "") -> None:
    satirlar.append(s)


def maskele(s: str) -> str:
    s = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<e-posta>", s)
    s = re.sub(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", "<uuid>", s, flags=re.I)
    s = re.sub(r"\b\d{1,3}(\.\d{1,3}){3}\b", "<ip>", s)
    s = re.sub(r"\b[A-Za-z0-9]{24,}\b", "<kimlik>", s)
    return s


def sir() -> str | None:
    v = os.environ.get("MEDS_PANEL_SECRET")
    if v:
        return v
    try:
        for line in (MEDS / ".env").read_text(encoding="utf-8").splitlines():
            if line.startswith("MEDS_PANEL_SECRET="):
                return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    except OSError:
        pass
    return None


def http_json(url: str, gizli: bool = False, zaman: int = 8):
    r = urllib.request.Request(url, headers={"User-Agent": "meds-saglik/1"})
    if gizli:
        s = sir()
        if not s:
            raise RuntimeError("MEDS_PANEL_SECRET yok")
        r.add_header("x-panel-secret", s)
    with urllib.request.urlopen(r, timeout=zaman) as y:
        return json.loads(y.read().decode("utf-8", "replace"))


def kos(arg: list[str], zaman: int = 120) -> tuple[int, str]:
    p = subprocess.run(arg, cwd=MEDS, capture_output=True, text=True, timeout=zaman)
    return p.returncode, (p.stdout + p.stderr)


def ssh(komut: str, zaman: int = 25) -> str:
    p = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", "medsor-oracle", komut],
                       capture_output=True, text=True, timeout=zaman)
    if p.returncode != 0 and not p.stdout:
        raise RuntimeError((p.stderr.strip().splitlines() or ["ssh başarısız"])[-1][:80])
    return p.stdout


def jsonl(metin: str):
    for s in metin.splitlines():
        try:
            k = json.loads(s)
            if isinstance(k, dict):
                yield k
        except Exception:
            continue


def zamani(k) -> datetime | None:
    try:
        z = datetime.fromisoformat(str(k.get("zaman") or k.get("at") or "").replace("Z", "+00:00"))
        return z if z.tzinfo else z.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def kova_yuzde(kov: dict, q: float) -> str:
    n = sum(kov.values())
    if not n:
        return "-"
    hedef, top = q * n, 0
    for i, v in enumerate(kov.values()):
        top += v
        if top >= hedef:
            return f"≤{KOVALAR[i]}" if i < len(KOVALAR) else f">{KOVALAR[-1]}"
    return "?"


def p75(d: list[float]):
    if not d:
        return None
    d = sorted(d)
    return d[min(len(d) - 1, int(0.75 * (len(d) - 1) + 0.5))]


def mb(n: float) -> str:
    return f"{n / 1048576:.1f} MB"


def boyut(p: Path) -> int:
    t = 0
    for kok, _, ds in os.walk(p):
        for f in ds:
            try:
                t += os.lstat(os.path.join(kok, f)).st_size
            except OSError:
                pass
    return t


def bolum(ad: str):
    def sar(f):
        def ic(a):
            yaz(f"■ {ad}")
            try:
                f(a)
            except Exception as e:  # noqa: BLE001 — her bölüm bağımsız
                yaz(f"  erişilemedi: {type(e).__name__}: {str(e)[:90]}")
                dikkat.append(f"{ad}: erişilemedi")
        return ic
    return sar


# ── Sunucu ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def sunucu_ozet(ad: str, taban: str, gizli: bool) -> None:
    try:
        h = http_json(f"{taban}/api/health")
        yaz(f"  [{ad}] health: {'ok' if h else '?'}")
    except Exception as e:
        yaz(f"  [{ad}] health erişilemedi: {str(e)[:70]}")
        sorun.append(f"{ad} /api/health yanıt vermiyor")
        return
    try:
        t = http_json(f"{taban}/api/admin/telemetri", gizli=gizli)
    except Exception as e:
        yaz(f"  [{ad}] telemetri erişilemedi: {str(e)[:70]}")
        dikkat.append(f"{ad} telemetri erişilemedi")
        return
    tablo = t.get("tablo") or []
    yavas = sum(sum(v for k, v in r["kovalar"].items() if k in ("<=2500", ">2500")) for r in tablo)
    toplam = sum(r["sayi"] for r in tablo)
    yaz(f"  [{ad}] {len(tablo)} rota, {toplam} istek, ≥1 sn: {yavas}, başlangıç {str(t.get('baslangic'))[:16]}")
    for r in sorted(tablo, key=lambda r: -r["ortMs"])[:8]:
        yaz(f"    {r['rota'][:44]:44} n={r['sayi']:<5} ort={r['ortMs']:>7} p50{kova_yuzde(r['kovalar'], .5):>6} "
            f"p95{kova_yuzde(r['kovalar'], .95):>6} 5xx={r['hata5xx']}")
    b = (t.get("bellek") or [None])[-1]
    if b:
        yaz(f"    bellek: rss {b['rss']} MB, heap {b['heapUsed']}/{b['heapTotal']} MB, döngü p99 "
            f"{b.get('olayDongusuGecikmeMs')} ms, SSE istemci {b.get('sseIstemci')}")
        if (b.get("olayDongusuGecikmeMs") or 0) > 200:
            dikkat.append(f"{ad} olay döngüsü gecikmesi {b['olayDongusuGecikmeMs']} ms")
    else:
        yaz("    bellek: örnek yok (ilk 5 dk)")
    J.setdefault("sunucu", {})[ad] = {"istek": toplam, "yavas": yavas, "rss": b and b["rss"]}
    if yavas > 20:
        dikkat.append(f"{ad} ≥1 sn istek {yavas}")


@bolum("Sunucu")
def b_sunucu(a) -> None:
    sunucu_ozet("yerel", "http://127.0.0.1:3000", gizli=False)
    if not a.canli:
        return
    sunucu_ozet("canlı", CANLI_URL, gizli=True)
    ay = datetime.now(timezone.utc).strftime("%Y-%m")
    try:
        g = list(jsonl(ssh(f"tail -n 2000 {ORACLE_MEDS}/data/gunluk/veri-{ay}.jsonl")))
    except Exception as e:
        yaz(f"  [canlı günlük] erişilemedi: {e}")
        return
    say = Counter((str(k.get("kaynak", "?")), str(k.get("seviye", "?"))) for k in g)
    yaz("  [canlı günlük, son 2000] " + ", ".join(f"{kn}/{sv}={n}" for (kn, sv), n in say.most_common(8)))
    for k in [k for k in g if k.get("seviye") == "hata"][-5:]:
        yaz(f"    {str(k.get('zaman'))[5:16]} {str(k.get('kaynak'))[:14]:14} {maskele(str(k.get('mesaj')))[:80]}")


# ── İstemci ─────────────────────────────────────────────────────────────────────────────────────────────────────────
@bolum("İstemci")
def b_istemci(a) -> None:
    ay = datetime.now(timezone.utc).strftime("%Y-%m")
    kaynak = {"yerel": lambda: (MEDS / f"data/gunluk/vitals-{ay}.jsonl").read_text(encoding="utf-8", errors="replace")}
    if a.canli:
        kaynak["canlı"] = lambda: ssh(f"tail -n 20000 {ORACLE_MEDS}/data/gunluk/vitals-{ay}.jsonl")
    for ad, f in kaynak.items():
        try:
            kay = list(jsonl(f()))
        except Exception as e:
            yaz(f"  [{ad} vitals] erişilemedi: {str(e)[:70]}")
            continue
        rota: dict = defaultdict(lambda: defaultdict(list))
        for k in kay:
            for m in ESIK:
                if isinstance(k.get(m), (int, float)):
                    rota[k.get("rota", "?")][m].append(k[m])
        hepsi = [v for r in rota.values() for v in r["lcp"]]
        yaz(f"  [{ad} vitals] {len(kay)} örnek, {len(rota)} rota, genel LCP p75 {p75(hepsi)}")
        J.setdefault("vitals", {})[ad] = {"lcp_p75": p75(hepsi), "ornek": len(kay)}
        for r, m in sorted(rota.items(), key=lambda x: -len(x[1]["lcp"]))[:6]:
            deg = {k: p75(m[k]) for k in ESIK}
            asim = [k for k, v in deg.items() if v is not None and v > ESIK[k]]
            yaz(f"    {r[:34]:34} n={len(m['lcp']):<4} LCP {deg['lcp']} INP {deg['inp']} CLS {deg['cls']}"
                + (f"  ⚠ {'/'.join(asim)}" if asim else ""))
            if asim and len(m["lcp"]) >= 5:
                dikkat.append(f"{ad} {r[:30]} {'/'.join(asim)} eşik aşımı")
    if not a.canli:
        yaz("  istemci hataları: yalnız --canli")
        return
    sinir = datetime.now(timezone.utc) - timedelta(days=a.gun)
    try:
        kay = [k for k in jsonl(ssh(f"tail -n 3000 {ORACLE_MEDS}/data/istemci_hatalari.jsonl")) if (zamani(k) or sinir) >= sinir]
    except Exception as e:
        yaz(f"  istemci hataları erişilemedi: {e}")
        return
    sy = Counter((maskele(str(k.get("mesaj")))[:60], re.sub(r"^https?://[^/]+", "", maskele(str(k.get("adres", ""))))[:28]) for k in kay)
    yaz(f"  istemci hataları (son {a.gun} gün): {len(kay)} kayıt, {len(sy)} farklı")
    for (m, s), n in sy.most_common(8):
        yaz(f"    {n:>4}× {m:60} {s}")
    J["istemci_hata"] = len(kay)
    if len(kay) > 50:
        dikkat.append(f"istemci hatası {len(kay)} / {a.gun} gün")


# ── Veri ────────────────────────────────────────────────────────────────────────────────────────────────────────────
@bolum("Veri")
def b_veri(a) -> None:
    for arg in (["scripts/altyapi/veri_bakim.py", "denetle"], ["scripts/altyapi/veri.py", "--denetle"]):
        k, o = kos([sys.executable, *arg])
        yaz(f"  {Path(arg[0]).name}: {(o.strip().splitlines() or ['(boş)'])[-1][:100]}")
        if k != 0:
            sorun.append(f"{Path(arg[0]).name} çıkış {k}")
    buyuk = []
    for d in ("data", "src/data"):
        top = 0
        for kok, dz, ds in os.walk(MEDS / d):
            dz[:] = [x for x in dz if x not in ("backups", "_yedek", "_arsiv_veri")] if d == "data" else dz
            for f in ds:
                p = os.path.join(kok, f)
                try:
                    s = os.lstat(p).st_size
                except OSError:
                    continue
                top += s
                buyuk.append((s, os.path.relpath(p, MEDS)))
        yaz(f"  {d}/: {mb(top)} (yedek/arşiv hariç)")
    yaz("  en büyük: " + ", ".join(f"{Path(p).name[:30]} {mb(s)}" for s, p in sorted(buyuk, reverse=True)[:5]))
    yedek = sum(boyut(MEDS / "data" / x) for x in ("backups", "_yedek"))
    arsiv = boyut(MEDS / "data/_arsiv_veri") if (MEDS / "data/_arsiv_veri").exists() else boyut(PROJE / "_arsiv_veri")
    yaz(f"  data/backups+_yedek: {mb(yedek)} · _arsiv_veri: {mb(arsiv)}")
    if yedek > 300 * 1048576:
        dikkat.append(f"yedek {mb(yedek)} > 300 MB")


# ── İçerik ──────────────────────────────────────────────────────────────────────────────────────────────────────────
@bolum("İçerik")
def b_icerik(a) -> None:
    k, o = kos([sys.executable, "scripts/hat/tam_hat/manifest.py", "denetle", "--kurul", "2"], 180)
    sat = o.strip().splitlines()
    katman = [re.match(r"\s+(\w+)\s+(\d+) ders", s) for s in sat]
    katman = [(m.group(1), int(m.group(2))) for m in katman if m]
    yaz(f"  manifest: {sat[-1][:90] if sat else '(boş)'}")
    yaz("  en çok eksik katman: " + ", ".join(f"{a_} {n}" for a_, n in katman[:3]))
    if k != 0:
        sorun.append("manifest denetle bozuk/bayat")
    k, o = kos([sys.executable, "scripts/hat/tam_hat/kural_secici.py", "--denetle"])
    yaz(f"  kural_secici: {(o.strip().splitlines() or ['(boş)'])[-1][:90]}")
    if k != 0:
        sorun.append("kural_secici --denetle madde kaybı")


# ── Ses ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
@bolum("Ses")
def b_ses(a) -> None:
    yol = Path.home() / ".cache/meds/ses_kapisi.sqlite"
    if not yol.exists():
        yaz("  ölçülmedi (önbellek yok; `ses_kapisi.py tara --hepsi`)")
    else:
        db = sqlite3.connect(f"file:{yol}?mode=ro", uri=True)
        n = bozuk = kirp = 0
        for (v,) in db.execute("SELECT veri FROM olcum"):
            n += 1
            try:
                d = json.loads(v)
            except Exception:
                bozuk += 1
                continue
            bozuk += (not d.get("ok")) or not d.get("sure")
            kirp += (d.get("max") or -99) >= -0.5
        yaz(f"  önbellek: {n} ölçüm, okunamaz/süresiz {bozuk}, kırpılma şüphesi {kirp} "
            f"(son yazım {datetime.fromtimestamp(yol.stat().st_mtime):%m-%d %H:%M})")
        if bozuk:
            sorun.append(f"ses önbelleğinde {bozuk} bozuk ölçüm")
    k, o = kos([sys.executable, "scripts/uretim/ses_ortak/ses_kapisi.py", "artik"], 120)
    oz = [s for s in o.splitlines() if s.startswith("==")]
    yaz("  kayıt↔disk: " + ("; ".join(s[3:] for s in oz) or "artık yok"))
    if any("kayitsiz" in s for s in oz):
        dikkat.append("kayıtsız ses dosyası var")


# ── Ön yüz paketi ───────────────────────────────────────────────────────────────────────────────────────────────────
def paket_olc() -> dict:
    dist = MEDS / "dist"
    man = json.loads((dist / ".vite/manifest.json").read_text(encoding="utf-8"))
    html = (dist / "index.html").read_text(encoding="utf-8")
    ilk = set(re.findall(r'(?:src|href)="/?(assets/[^"]+\.(?:js|css))"', html))
    giris = [k for k, v in man.items() if v.get("isEntry")]
    yigin = list(giris)
    gorulen = set()
    while yigin:
        k = yigin.pop()
        if k in gorulen or k not in man:
            continue
        gorulen.add(k)
        v = man[k]
        ilk.add(v["file"])
        ilk.update(v.get("css", []))
        yigin.extend(v.get("imports", []))

    def gz(f):
        b = (dist / f).read_bytes()
        return len(b), len(gzip.compress(b, 6))
    o = {"js": [0, 0], "css": [0, 0]}
    for f in ilk:
        if (dist / f).exists():
            r, g = gz(f)
            t = "css" if f.endswith(".css") else "js"
            o[t][0] += r
            o[t][1] += g
    tembel = sorted(((dist / v["file"]).stat().st_size, v["file"]) for v in man.values()
                    if v["file"].endswith(".js") and v["file"] not in ilk and (dist / v["file"]).exists())
    return {"ilk_dosya": len(ilk), "js": o["js"], "css": o["css"], "tembel": tembel[::-1][:5]}


@bolum("Ön yüz paketi")
def b_paket(a) -> None:
    p = paket_olc()
    yaz(f"  ilk yük: {p['ilk_dosya']} dosya · JS {mb(p['js'][0])} (gzip {mb(p['js'][1])}) · CSS {mb(p['css'][0])} "
        f"(gzip {mb(p['css'][1])})")
    yaz("  en büyük tembel: " + ", ".join(f"{Path(f).name[:34]} {mb(s)}" for s, f in p["tembel"]))
    J["paket"] = {"ilk_gzip": p["js"][1] + p["css"][1], "ilk_dosya": p["ilk_dosya"]}


# ── Günlük ──────────────────────────────────────────────────────────────────────────────────────────────────────────
@bolum("Günlük (yerel)")
def b_gunluk(a) -> None:
    k, o = kos([sys.executable, "scripts/gunluk.py", "ozet", "--gun", str(a.gun)])
    for s in o.strip().splitlines()[:9]:
        yaz("  " + s)
    # Sınama kayıtları (geçici dizine yazan denemeler, kaynak=deneme/sinama) gerçek hata sayılmaz
    import datetime as _dt
    sinir = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=a.gun)).isoformat()
    hata = 0
    for f in sorted((MEDS / "data" / "gunluk").glob("*-*.jsonl")):
        if f.name.startswith("vitals-"):
            continue
        try:
            satirlar = f.read_text(encoding="utf-8").splitlines()[-5000:]
        except OSError:
            continue
        for sat in satirlar:
            try:
                r = json.loads(sat)
            except ValueError:
                continue
            if r.get("seviye") != "hata" or str(r.get("zaman", "")) < sinir:
                continue
            ek = r.get("ek") or {}
            if r.get("kaynak") in ("deneme", "sinama") or ek.get("kaynak") == "sinama" \
                    or str(ek.get("dosya", "")).startswith("/tmp/"):
                continue
            hata += 1
    J["gunluk_hata"] = hata
    if hata:
        dikkat.append(f"yerel günlükte {hata} hata ({a.gun} gün)")


# ── Eğilim ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def egilim(n: int) -> int:
    ds = sorted(KAYIT_DIZINI.glob("*.json"))[-n:]
    if not ds:
        print(f"(kayıt yok — önce --json ile çalıştır; {KAYIT_DIZINI})")
        return 0
    print(f"{'zaman':17} {'RSS yerel':>9} {'RSS canlı':>9} {'ilk gzip':>9} {'yavaş':>6} {'LCP p75':>8} {'hüküm':>8}")
    for p in ds:
        d = json.loads(p.read_text(encoding="utf-8"))
        s = d.get("sunucu", {})
        print(f"{p.stem:17} {str((s.get('yerel') or {}).get('rss')):>9} {str((s.get('canlı') or {}).get('rss')):>9} "
              f"{mb((d.get('paket') or {}).get('ilk_gzip') or 0):>9} "
              f"{sum((v or {}).get('yavas', 0) for v in s.values()):>6} "
              f"{str(((d.get('vitals') or {}).get('canlı') or (d.get('vitals') or {}).get('yerel') or {}).get('lcp_p75')):>8} "
              f"{d.get('hukum', '?'):>8}")
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["egilim"]:
        e = argparse.ArgumentParser()
        e.add_argument("--n", type=int, default=10)
        return egilim(e.parse_args(argv[1:]).n)
    ap = argparse.ArgumentParser(description="MeDSor tek sağlık raporu")
    ap.add_argument("--canli", action="store_true", help="Oracle'ı da oku (salt okuma)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--gun", type=int, default=1)
    a = ap.parse_args(argv)
    yaz(f"MeDSor sağlık raporu · {datetime.now():%Y-%m-%d %H:%M} · {'yerel+canlı' if a.canli else 'yerel'}")
    for f in (b_sunucu, b_istemci, b_veri, b_icerik, b_ses, b_paket, b_gunluk):
        f(a)
    hukum = f"sorun ({len(sorun)})" if sorun else f"dikkat ({len(dikkat)})" if dikkat else "iyi"
    yaz(f"SAĞLIK: {hukum}" + (" — " + "; ".join(sorun + dikkat) if sorun or dikkat else ""))
    J.update(zaman=datetime.now().isoformat(timespec="seconds"), hukum=hukum.split()[0], sorun=sorun, dikkat=dikkat)
    if a.json:
        KAYIT_DIZINI.mkdir(parents=True, exist_ok=True)
        (KAYIT_DIZINI / f"{datetime.now():%Y%m%d-%H%M%S}.json").write_text(json.dumps(J, ensure_ascii=False, indent=1), encoding="utf-8")
        for eski in sorted(KAYIT_DIZINI.glob("*.json"))[:-30]:
            eski.unlink()
        print(json.dumps(J, ensure_ascii=False, indent=1))
    else:
        print("\n".join(satirlar))
    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main())
