#!/usr/bin/env python3
"""Betik katmanlarını tek komutta tamamla + yayın öncesi eksik katman kapısı (kullanıcı kararı 2026-11-17).

Neden: 2026-11-17 taramasında Kurul 2 derslerinin eksiklerinin çoğu LLM işi değil, ÇALIŞTIRILMAMIŞ BETİKTİ —
ders analizi 10 derste hiç koşulmamış (H612/H613), içerik paketi girdisi yazılmamış, kelime zamanı zamanlayıcı kapalı
olduğu için üretilmemiş, çözücü bağlantısı başlık uyuşmazlığından düşmüş (H608). Her biri ayrı oturumda, ayrı denetçi
turunda ve token harcanarak bulundu. Bu betik LLM'siz katmanları sırayla, kaldığı yerden (idempotent) üretir ve
her katmanın kapısını koşar; eksik kalanı tek tabloda, düzeltme komutuyla verir.

  python3 scripts/hat/tam_hat/betik_tamamla.py k2-50            # eksik betik katmanlarını üret + kapılar
  python3 scripts/hat/tam_hat/betik_tamamla.py k2-50 --denetle  # yalnız denetle (yazmaz) → yayın kapısı (çıkış 1 = eksik var)
  python3 scripts/hat/tam_hat/betik_tamamla.py --kurul 2 --denetle   # bütün kurul
  python3 scripts/hat/tam_hat/betik_tamamla.py k2-50 --gpu      # kelime zamanı eksikse GPU istisnasıyla çöz (gpuguard açık olmalı)

Katmanlar (sıra önemli; LLM yok):
  ders_analizi   scripts/uretim/ders_analizi/uret.py <k> → --dogrula
  ders_icerik    paketten_ek.py (ek yoksa) → ders_icerik_uret → ders_icerik_adim → ders_icerik_kaynak → ders_icerik_dogrula
  zengin         zengin_transkript.py <key> (metin değiştiyse) → --dogrula
  cozucu_bag     ders defteri kodu ↔ src/data/k<N>*_cozucu (sesli) eşleşmesi (H608)
  kelime_zaman   canlı API'de her paragrafta kelime zamanı (H612); --gpu ile kelime_zaman.py --oracle --gpu
  takip          takip_kapisi.py (yerel dosya yoksa canlı kelime zamanı denetimi)
  ornek_soru     örnek soru kapısı (LLM katmanı; kalırsa onarim_paketi.py komutu verilir)
  cikmis_analiz  ders_analizi/uret.py --dogrula (çıkmış analizi LLM katmanıdır; burada yalnız denetlenir)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.append(str(_d))
import kok as _kok  # noqa: E402

KOK = _kok.MEDS
PROJE = KOK.parent
METIN = KOK / "data" / "sesli_anlatim" / "metin"
OCR_PY = KOK / ".venv-ocr" / "bin" / "python"
API = os.environ.get("MEDS_ORACLE_API_URL", "https://nofrostlife.com.tr")


def kos(cmd: list[str], zaman: int = 600) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=KOK, capture_output=True, text=True, timeout=zaman, errors="replace")
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return 124, "zaman aşımı"


def tam_anahtar(kisa: str) -> str | None:
    c = sorted(f.stem for f in METIN.glob(f"{kisa}-*.md") if not re.search(r"-v\d+$|-ag-", f.stem))
    return c[0] if c else None


def son_satir(cikti: str) -> str:
    sat = [x.strip() for x in cikti.splitlines() if x.strip() and "pymupdf_layout" not in x]
    hata = [x for x in sat if x.startswith("HATA")]
    return (hata[0] if hata else sat[-1] if sat else "")[:150]


def defter_kodu(kisa: str) -> str | None:
    for f in (KOK / "src" / "data" / "dersler").glob("k*.json"):
        for x in json.loads(f.read_text(encoding="utf-8")).get("dersler", []):
            if x.get("id") == kisa:
                return x.get("kod")
    return None


def canli(key: str) -> dict | None:
    try:
        req = urllib.request.Request(f"{API}/api/canli-ders/{key}", headers={"User-Agent": "medsor-sesli-anlatim/1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception:  # noqa: BLE001
        return None


class Rapor:
    def __init__(self, kisa: str):
        self.kisa, self.satir = kisa, []

    def ekle(self, katman: str, ok: bool, ne: str, komut: str = "") -> bool:
        self.satir.append((katman, ok, ne, komut))
        return ok

    def bas(self) -> int:
        eksik = [s for s in self.satir if not s[1]]
        print(f"\n== {self.kisa}: {len(self.satir) - len(eksik)}/{len(self.satir)} katman tamam")
        for k, ok, ne, komut in self.satir:
            print(f"  {'✓' if ok else '✗'} {k:<13} {ne}" + (f"\n      → {komut}" if komut and not ok else ""))
        return len(eksik)


def ders(kisa: str, yaz: bool, gpu: bool) -> int:
    R = Rapor(kisa)
    key = tam_anahtar(kisa)
    if not key:
        R.ekle("metin", False, "sesli ders metni yok (anlatım aşaması yapılmamış)", "kosucu.py anlatim aşaması")
        return R.bas()
    py = sys.executable

    # 1) ders analizi (+ özet) — LLM yok
    k, o = kos([py, "scripts/uretim/ders_analizi/uret.py", "--dogrula", kisa])
    if k and yaz:
        kos([py, "scripts/uretim/ders_analizi/uret.py", kisa])
        k, o = kos([py, "scripts/uretim/ders_analizi/uret.py", "--dogrula", kisa])
    R.ekle("ders_analizi", k == 0, son_satir(o), f"python3 scripts/uretim/ders_analizi/uret.py {kisa}")

    # 2) ders içerik paketi
    k, o = kos([py, "scripts/ders_icerik_dogrula.py", key])
    if k and yaz:
        if not (PROJE / "meds_temp" / "ogrenci_ders" / kisa / "taslak" / "ders_icerik_ek.json").exists():
            kos([str(OCR_PY) if OCR_PY.exists() else py, "scripts/uretim/ders_icerik/paketten_ek.py", kisa])
        for s in ("scripts/ders_icerik_uret.py", "scripts/ders_icerik_adim.py", "scripts/ders_icerik_kaynak.py"):
            kos([py, s, key])
        k, o = kos([py, "scripts/ders_icerik_dogrula.py", key])
    R.ekle("ders_icerik", k == 0, son_satir(o),
           f".venv-ocr/bin/python scripts/uretim/ders_icerik/paketten_ek.py {kisa} (görüntü tablo: taslak/tablolar_gorsel.json) → ders_icerik_uret/adim/kaynak")

    # 3) zengin transkript (metin modelden yeniyse yeniden)
    zf = KOK / "src" / "data" / "zengin_transkript" / f"{key}.json"
    bayat = not zf.exists() or json.loads(zf.read_text(encoding="utf-8")).get("kaynak_mtime") != int((METIN / f"{key}.md").stat().st_mtime)
    if bayat and yaz:
        kos([py, "scripts/uretim/sesli_anlatim/zengin_transkript.py", key])
    k, o = kos([py, "scripts/uretim/sesli_anlatim/zengin_transkript.py", key, "--dogrula"])
    R.ekle("zengin", k == 0 and (not bayat or yaz), "bayat (metin değişmiş)" if bayat and not yaz else son_satir(o),
           f"python3 scripts/uretim/sesli_anlatim/zengin_transkript.py {key}")

    # 4) çözücü bağlantısı (defter kodu ↔ sesli çözücü)
    kod = defter_kodu(kisa)
    var = False
    for ix in (KOK / "src" / "data").glob("k[0-9]*_cozucu/index.json"):
        if "hoca" in ix.parent.name:
            continue
        for x in json.loads(ix.read_text(encoding="utf-8")).get("dersler", []):
            if kod and (x["kod"] == kod or x["kod"].startswith(kod + "-")) and x.get("soru") and x.get("ses", True):
                var = True
    R.ekle("cozucu_bag", var, f"defter kodu {kod or '?'} → sesli çözücü {'var' if var else 'YOK'}",
           "örnek soru + sesli çözücü aşaması (kosucu ornek_soru; çözücü kodu = defter kodu)")

    # 5) kelime zamanı (canlı)
    d = canli(key)
    if d is None:
        R.ekle("kelime_zaman", False, "canlı API okunamadı (ders yayında değil mi?)", "ders_ekle aşaması")
    else:
        np_ = sum(len([p for p in b["paragraflar"] if p["metin"].strip()]) for b in d["bolumler"])
        eksik = [v["id"] for v in d.get("varyantlar", []) if v.get("zamanlama") and len(v.get("kelimeZaman") or {}) < np_]  # zamanlamasız eski varyant çözülemez/kullanılmaz
        if eksik and gpu and yaz:
            # CUDA kütüphane yolu ve kilit, zamanlayıcı servisiyle aynı (meds-kelime-zaman-hat.service); koruyucu kapalıysa betik kendisi reddeder
            srv = Path.home() / ".config/systemd/user/meds-kelime-zaman-hat.service"
            ld = next((ln.split("LD_LIBRARY_PATH=", 1)[1].strip() for ln in (srv.read_text().splitlines() if srv.exists() else [])
                       if "LD_LIBRARY_PATH=" in ln), "")
            kilit = f"/run/user/{os.getuid()}/meds-kelime-zaman.lock"
            kos(["bash", "-lc", f"cd {KOK} && LD_LIBRARY_PATH='{ld}' KZ_THREADS=4 flock -w 1800 {kilit} "
                 f".venv-hizala/bin/python scripts/uretim/sesli_anlatim/kelime_zaman.py --key {key} --oracle --gpu"], zaman=3600)
            d = canli(key) or d
            eksik = [v["id"] for v in d.get("varyantlar", []) if v.get("zamanlama") and len(v.get("kelimeZaman") or {}) < np_]
        R.ekle("kelime_zaman", not eksik, f"{np_} paragraf · eksik varyant: {', '.join(eksik) or 'yok'}",
               f".venv-hizala/bin/python scripts/uretim/sesli_anlatim/kelime_zaman.py --key {key} --oracle --gpu  (gpuguard açık; ya da bu betik --gpu)")

    # 6) PDF takibi (yerel dosya varsa kapı; yoksa Oracle'da üretilir, kelime zamanı denetimi yeterli)
    if (KOK / "data" / "sesli_anlatim" / "cumle_zaman" / f"{key}.json").exists() and OCR_PY.exists():
        k, o = kos([str(OCR_PY), "scripts/uretim/sesli_anlatim/takip_kapisi.py", key])
        R.ekle("takip", k == 0, son_satir(o), f".venv-ocr/bin/python scripts/uretim/sesli_anlatim/takip_kapisi.py {key}")
    else:
        R.ekle("takip", True, "cümle zamanı/işaret Oracle'da üretilir (meds-cumle-zaman); yerel kapı atlandı")

    # 6b) örnek soru kapısı (LLM katmanı — yalnız denetim). k2-16 soruları kural eklendikten sonra kapısız yayına girmişti (H617).
    od = KOK / "src" / "data" / "ornek_sorular" / kisa[:2]
    # güncel ders anahtarının dosyası önce (k2-07'de eski adlı ikinci bir dosya var; glob sırası onu seçiyordu)
    of = [od / f"{key}.json"] if (od / f"{key}.json").exists() else sorted(od.glob(f"{kisa}-*.json"))
    dk = next((x for x in (PROJE / "meds_temp" / "ogrenci_ders" / kisa, KOK / "meds_temp" / "ogrenci_ders" / kisa)
               if (x / "soru_uslubu.json").exists() and (x / "sayfalar.json").exists()), None)
    if of and dk:
        arg = [f"dosya={of[0]}", f"uslup={dk / 'soru_uslubu.json'}", f"ders={kisa}", f"sayfalar={dk / 'sayfalar.json'}"]
        k, o = kos([py, "scripts/kapilar/kos.py", "ornek_soru", *arg])
        top = re.search(r"ÖRNEK SORU KAPISI:\s*(\d+) HATA", o)
        R.ekle("ornek_soru", k == 0, f"{top.group(1) if top else '?'} HATA",
               f"python3 scripts/hat/tam_hat/onarim_paketi.py ornek_soru {of[0].relative_to(KOK)} --uslup {dk}/soru_uslubu.json "
               f"--ders {kisa} --sayfalar {dk}/sayfalar.json  → yalnız hatalı şıklar yeniden yazılır")
    elif of:
        R.ekle("ornek_soru", True, "ders çalışma klasörü yok (soru_uslubu/sayfalar) — kapı atlandı")

    # 7) çıkmış analizi (LLM katmanı — yalnız denetim)
    k, o = kos([py, "scripts/uretim/ders_analizi/uret.py", "--dogrula", kisa])
    an = KOK.parent / "meds_database_v2" / "ders_bilgi" / kisa / "degerlendirme" / "cikmis_analiz.json"
    R.ekle("cikmis_analiz", an.exists() or k == 0, "cikmis_analiz.json var" if an.exists() else "cikmis_analiz.json yok (LLM aşaması)",
           "kosucu.py cikmis_analiz aşaması (baglam/is_cikmis_analiz.md)")
    return R.bas()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dersler", nargs="*")
    ap.add_argument("--kurul", type=int)
    ap.add_argument("--denetle", action="store_true", help="yazma, yalnız denetle (yayın kapısı)")
    ap.add_argument("--gpu", action="store_true", help="eksik kelime zamanını GPU istisnasıyla çöz")
    a = ap.parse_args()
    ks = [m.group(0) for x in a.dersler if (m := re.match(r"k\d-\d{2}", x))]
    if a.kurul:
        ks += sorted({m.group(0) for f in METIN.glob(f"k{a.kurul}-*.md") if (m := re.match(rf"k{a.kurul}-\d{{2}}", f.name))
                      and not re.search(r"-v\d+\.md$|-ag-", f.name)})
    if not ks:
        ap.print_help()
        return 2
    eksik = {k: ders(k, not a.denetle, a.gpu) for k in ks}
    top = sum(1 for v in eksik.values() if v)
    print(f"\nÖZET: {len(ks) - top}/{len(ks)} ders betik katmanlarında tam" + (f" · eksikli: {', '.join(k for k, v in eksik.items() if v)}" if top else ""))
    return 1 if top else 0


if __name__ == "__main__":
    sys.exit(main())
