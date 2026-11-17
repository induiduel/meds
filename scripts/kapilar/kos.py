#!/usr/bin/env python3
"""Tek kapı girişi — hat aşamasının kanonik kapısını matris.json'dan çözüp çalıştırır. (kullanıcı kararı 2026-11-16)

Neden: tek-kapı birleşik betikler (anlatim_kapi, ornek_soru_kapi) çağrı sayısını azalttı ama kapı DOSYALARI hâlâ dağınık.
Bu dispatcher TEK giriş verir: ajan/işçi aşama adıyla çağırır, kapı komutunu kendisi bilmek zorunda kalmaz. Alttaki
doğrulayıcılar silinmez; bu matrisin yapı taşlarıdır — tek fark, artık buradan tek adla çağrılırlar.

  python3 scripts/kapilar/kos.py --liste
  python3 scripts/kapilar/kos.py anlatim dizin=<v3 dizin> sayfalar=<sayfalar.json> key=k2-49
  python3 scripts/kapilar/kos.py ornek_soru dosya=<...> uslup=<...> ders="<ders>" sayfalar=<...>

Aşamanın `gerekli` yer tutucuları ad=değer çiftleriyle verilir; eksikse çalıştırmadan listeyle durur. Kapının çıkış
kodu aynen döndürülür (0 = 0 HATA). Ayrık kodlar: 2 = çağrı/girdi yolu hatası (kapı çalışmadı), 70 = kapı çöktü
(Traceback; içerik hatası değil).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
KOK = _kok.MEDS
MATRIS = Path(__file__).resolve().parent / "matris.json"


def _yukle() -> dict:
    return json.loads(MATRIS.read_text(encoding="utf-8"))["asamalar"]


def _izle(asama: str, deg: dict[str, str], kod: int, ciktilar: list[str]) -> None:
    """Hata izleyicisi (scripts/kapilar/hata_izleyici.py) için kalıcı kayıt: her kapı koşusu bir JSONL satırı.
    Yazılamazsa sessizce geçer (kapı sonucu asla değişmez)."""
    try:
        import datetime
        import os
        sat = [x.strip() for x in ciktilar if "HATA" in x or "UYARI" in x]
        kayit = {
            "zaman": datetime.datetime.now().isoformat(timespec="seconds"), "asama": asama, "kod": kod,
            "ders": deg.get("key") or deg.get("ders") or deg.get("hedef") or "",
            "oturum": os.environ.get("CLAUDE_SESSION_ID", ""), "satirlar": sat[:300],
        }
        yol = KOK.parent / "meds_temp" / "hata_izleyici" / "kapi_kosulari.jsonl"
        yol.parent.mkdir(parents=True, exist_ok=True)
        with yol.open("a", encoding="utf-8") as f:
            f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001
        pass


def main() -> int:
    asamalar = _yukle()
    argv = sys.argv[1:]
    if not argv or argv[0] in ("--liste", "-l", "--help", "-h"):
        print("Aşamalar (tek kapı girişi · matris.json):")
        for ad, m in asamalar.items():
            yer = ", ".join(m["gerekli"])
            print(f"  {ad:<14} {Path(m['kapi']).name:<24} gerekli: {yer}")
        return 0
    asama, ciftler = argv[0], argv[1:]
    if asama not in asamalar:
        print(f"HATA: bilinmeyen aşama '{asama}' (geçerli: {', '.join(asamalar)})", file=sys.stderr)
        return 2
    m = asamalar[asama]
    deg: dict[str, str] = {}
    for c in ciftler:
        if "=" not in c:
            print(f"HATA: ad=değer bekleniyor, '{c}' değil", file=sys.stderr)
            return 2
        ad, _, v = c.partition("=")
        deg[ad] = v
    eksik = [g for g in m["gerekli"] if g not in deg]
    if eksik:
        print(f"HATA: eksik yer tutucu(lar): {', '.join(eksik)}  (gerekli: {', '.join(m['gerekli'])})", file=sys.stderr)
        return 2
    try:
        arg = [p.format(**deg) for p in m["arg"]]
    except KeyError as e:
        print(f"HATA: matriste tanımsız yer tutucu {e}", file=sys.stderr)
        return 2
    # Girdi yolu yoksa kapıyı hiç çalıştırma (H597): kapı Traceback basıp düşüyor, ajan bunu içerik hatası sanıyordu.
    yok = []
    for ad in m.get("yol", []):
        y = Path(deg[ad])
        if not (y if y.is_absolute() else KOK / y).exists() and not y.exists():
            yok.append(f"{ad}={deg[ad]}")
    if yok:
        print(f"GİRDİ YOK: {', '.join(yok)} bulunamadı — kapı çalıştırılmadı (içerik hatası DEĞİL; yolu düzelt). "
              f"Yollar {KOK} köküne ya da çalışma dizinine göre çözülür.", file=sys.stderr)
        return 2
    cmd = [sys.executable, m["kapi"], *arg]
    print(f"== kapı: {asama} → {' '.join(cmd[1:])}", flush=True)
    # stderr canlı aktarılır + izlenir: kapı kendi çökmesiyle (Traceback) bitmişse bu "N HATA" değil araç arızasıdır.
    # stdout da izlenir (hata izleyicisi kaydı için HATA/UYARI satırları), canlı aktarım bozulmaz.
    p = subprocess.Popen(cmd, cwd=KOK, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    son: list[str] = []
    ciktilar: list[str] = []
    assert p.stderr is not None and p.stdout is not None
    import threading

    def _oku_stdout() -> None:
        for satir in p.stdout:  # type: ignore[union-attr]
            sys.stdout.write(satir)
            sys.stdout.flush()
            ciktilar.append(satir)
    t = threading.Thread(target=_oku_stdout, daemon=True)
    t.start()
    for satir in p.stderr:
        sys.stderr.write(satir)
        son.append(satir)
        ciktilar.append(satir)
        del son[:-60]
    kod = p.wait()
    t.join(5)
    _izle(asama, deg, kod, ciktilar)
    if kod != 0 and any(s.startswith("Traceback (most recent call last)") for s in son):
        neden = next((s.strip() for s in reversed(son) if s.strip()), "")
        print(f"KAPI ÇÖKTÜ (çıkış 70): '{asama}' kapısı doğrulama yapamadan düştü → {neden}\n"
              f"  Bu bir içerik hatası DEĞİL: girdiyi/yolu denetle; girdi doğruysa kapı betiğinde hata var.", file=sys.stderr)
        return 70
    return kod


if __name__ == "__main__":
    sys.exit(main())
