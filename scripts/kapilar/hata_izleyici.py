#!/usr/bin/env python3
"""Hata izleyici — tam içerik hattında en sık düşülen ve tekrar eden kapı hatalarını bulur (kullanıcı kararı 2026-11-17).

LLM/ağ/GPU yok; yalnız betik. Amaç: hangi kural/adım en çok denetçi turu ve limit tüketiyor, hangi sayısal eşik
gereğinden katı — kanıtla görmek. Eşik GEVŞETMEZ; yalnız rapor eder (kapı eşiği değişikliği kullanıcı kararıdır, H581).

Kaynaklar
  güncel : meds_temp/hata_izleyici/kapi_kosulari.jsonl — `scripts/kapilar/kos.py` her koşuyu buraya yazar
  geçmiş : docs/hatalar/_dizin.json (H maddeleri), meds_temp/gorev/gunluk.jsonl (model çağrısı/yeniden deneme),
           `tara` ile mevcut derslerin anahtarla çalışan kapıları yeniden koşturulur (sonuç yine kapi_kosulari'na düşer)

  python3 scripts/kapilar/hata_izleyici.py tara [--kurul 2] [--ders k2-07,k2-09] [--asama ders_icerik,cikmis_analiz,takip]
  python3 scripts/kapilar/hata_izleyici.py rapor [--gun 30] [--n 25]     # → meds_temp/hata_izleyici/rapor.md
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.append(str(_d))
import kok as _kok  # noqa: E402

KOK = _kok.MEDS
TEMP = KOK.parent / "meds_temp" / "hata_izleyici"
KOSU = TEMP / "kapi_kosulari.jsonl"
GOREV = KOK.parent / "meds_temp" / "gorev" / "gunluk.jsonl"
DIZIN = KOK / "docs" / "hatalar" / "_dizin.json"
METIN = KOK / "data" / "sesli_anlatim" / "metin"

# Anahtarla (ders kimliği) çalışan, ucuz betik kapıları. Kapı listesi kos.py/matris'ten; takip ayrı betik.
TARA_ASAMA = {
    # ders_icerik ve takip tam anahtar ister (k2-07-genel-…); cikmis_analiz kısa (k2-07). takip pymupdf ister → .venv-ocr
    "ders_icerik": lambda k: [sys.executable, "scripts/kapilar/kos.py", "ders_icerik", f"key={k}"],
    "cikmis_analiz": lambda k: [sys.executable, "scripts/kapilar/kos.py", "cikmis_analiz", f"key={k[:5]}"],
    "takip": lambda k: [str(KOK / ".venv-ocr/bin/python") if (KOK / ".venv-ocr/bin/python").exists() else sys.executable,
                        "scripts/uretim/sesli_anlatim/takip_kapisi.py", k],
}

SAYISAL = re.compile(r"(en az|en çok|en fazla|eşik|sınır|<=|>=|≤|≥|<\s*\d|>\s*\d|kelime|oran|%\s*\d|\d+\s*%|tavan|taban)", re.I)


def imza(satir: str) -> str:
    """Hata satırını tekrar sayımı için kalıba indirger: sayılar, tırnak içleri, yollar, ders kimlikleri silinir."""
    s = satir.strip()
    s = re.sub(r"k\d-\d{2}[\w-]*", "<ders>", s)
    s = re.sub(r"[\"'“”‘’«»][^\"'“”‘’«»]{0,120}[\"'“”‘’«»]", "<metin>", s)
    s = re.sub(r"\S+/\S+", "<yol>", s)
    s = re.sub(r"\d+([.,]\d+)?", "#", s)
    s = re.sub(r"\s+", " ", s)
    return s[:160]


def dersler(kurul: int) -> list[str]:
    ks = set()
    for f in METIN.glob(f"k{kurul}-*.md"):
        if re.search(r"-v\d+\.md$|-ag-", f.name):
            continue
        if re.match(rf"k{kurul}-\d\d-", f.name):
            ks.add(f.stem)
    return sorted(ks)


def tara(a: argparse.Namespace) -> int:
    tum = dersler(a.kurul)
    keys = [next((t for t in tum if t.startswith(d + "-") or t == d), d) for d in a.ders.split(",")] if a.ders else tum
    asamalar = a.asama.split(",") if a.asama else list(TARA_ASAMA)
    TEMP.mkdir(parents=True, exist_ok=True)
    ozet = collections.Counter()
    for k in keys:
        for asm in asamalar:
            cmd = TARA_ASAMA[asm](k)
            try:
                p = subprocess.run(cmd, cwd=KOK, capture_output=True, text=True, timeout=a.zaman, errors="replace")
                kod, cikti = p.returncode, (p.stdout + p.stderr).splitlines()
            except subprocess.TimeoutExpired:
                kod, cikti = 124, ["HATA: zaman aşımı (izleyici)"]
            if asm == "takip" and any(re.search(r"(cumle_zaman|isaret) dosyası yok", x) for x in cikti):
                # cumle_zaman/isaret Oracle'da meds-cumle-zaman.timer ile üretilir, yerelde kopyası olmayabilir:
                # yerine canlı API'de paragraf başına kelime zamanı denetlenir (yanlış alarm önlemi, 2026-11-17)
                kod, cikti = _canli_takip(k)
            if asm == "takip":  # kos.py dışından koşar: kaydı kendimiz yazarız
                _yaz({"asama": "takip", "ders": k, "kod": kod, "satirlar": [x.strip() for x in cikti if "HATA" in x or "UYARI" in x][:300]})
            ozet[(asm, "geçti" if kod == 0 else f"çıkış {kod}")] += 1
            print(f"{k:<6} {asm:<14} {'0 HATA' if kod == 0 else f'çıkış {kod}'}", flush=True)
    print("\nÖzet:", ", ".join(f"{x[0]} {x[1]}: {n}" for x, n in sorted(ozet.items())))
    return 0


def _canli_takip(key: str) -> tuple[int, list[str]]:
    import urllib.request
    api = os.environ.get("MEDS_ORACLE_API_URL", "https://nofrostlife.com.tr")
    try:
        with urllib.request.urlopen(urllib.request.Request(f"{api}/api/canli-ders/{key}", headers={"User-Agent": "medsor-sesli-anlatim/1"}), timeout=30) as r:
            d = json.load(r)
    except Exception as e:  # noqa: BLE001
        return 2, [f"HATA canlı API okunamadı: {e}"]
    np_ = sum(len([p for p in b["paragraflar"] if p["metin"].strip()]) for b in d["bolumler"])
    hata = []
    for v in d.get("varyantlar", []):
        kz = len(v.get("kelimeZaman") or {})
        if kz < np_:
            hata.append(f"HATA canlı {v['id']}: kelime zamanı {kz}/{np_} paragraf")
    return (1 if hata else 0), hata or [f"{key}: canlı kelime zamanı tam · 0 HATA"]


def _yaz(k: dict) -> None:
    k = {"zaman": dt.datetime.now().isoformat(timespec="seconds"), "tara": True, **k}
    with KOSU.open("a", encoding="utf-8") as f:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")


def _jsonl(p: Path) -> list[dict]:
    out = []
    if p.exists():
        for s in p.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                out.append(json.loads(s))
            except json.JSONDecodeError:
                pass
    return out


def rapor(a: argparse.Namespace) -> int:
    sinir = (dt.datetime.now() - dt.timedelta(days=a.gun)).isoformat()
    kosular = [k for k in _jsonl(KOSU) if k.get("zaman", "") >= sinir]
    L: list[str] = [f"# Hata izleyici raporu — {dt.date.today()} (son {a.gun} gün)", ""]

    # 1) Kapı koşuları: aynı ders+aşama kaç kez koşturulmuş (= tekrar turu), hangi imza kaç derste
    tur = collections.Counter((k.get("ders"), k.get("asama")) for k in kosular if not k.get("tara"))
    imz: dict[str, dict] = {}
    asama_kalmadi = collections.Counter()
    for k in kosular:
        if k.get("kod"):
            asama_kalmadi[k.get("asama")] += 1
        for s in k.get("satirlar", []):
            if "HATA" not in s or re.search(r"(?<!\d)0 HATA", s):  # "0 HATA" özet satırı hata değildir
                continue
            i = imza(s)
            r = imz.setdefault(i, {"n": 0, "ders": set(), "asama": collections.Counter(), "ornek": s})
            r["n"] += 1
            r["ders"].add(k.get("ders"))
            r["asama"][k.get("asama")] += 1
    L += [f"## 1. Kapı koşuları ({len(kosular)} koşu)", ""]
    if not kosular:
        L += ["Kayıt yok. `kos.py` koşuları bundan sonra kaydedilir; geçmiş için `hata_izleyici.py tara` çalıştır.", ""]
    else:
        L += ["**Aşama başına kalan (çıkış ≠ 0) koşu:** " + ", ".join(f"{x} {n}" for x, n in asama_kalmadi.most_common()), ""]
        cok = [(d, s, n) for (d, s), n in tur.most_common() if n >= 3]
        if cok:
            L += ["**En çok yeniden koşturulan kapılar (≥3 tur = denetçi/onarım döngüsü):**", ""]
            L += [f"- {d} · {s}: {n} koşu" for d, s, n in cok[: a.n]] + [""]
        L += ["**En sık HATA kalıpları** (kaç derste görüldüğüne göre; ⚖ = sayısal eşik içeriyor):", "",
              "| # | ders | toplam | aşama | kalıp | örnek |", "|---|---|---|---|---|---|"]
        sirali = sorted(imz.items(), key=lambda x: (-len(x[1]["ders"]), -x[1]["n"]))
        for j, (i, r) in enumerate(sirali[: a.n], 1):
            isr = "⚖ " if SAYISAL.search(r["ornek"]) else ""
            L.append(f"| {j} | {len(r['ders'])} | {r['n']} | {r['asama'].most_common(1)[0][0]} | {isr}`{i[:90]}` | {r['ornek'][:110].replace('|', '/')} |")
        say = sum(1 for _, r in sirali if SAYISAL.search(r["ornek"]))
        L += ["", f"Sayısal eşikli kalıp: {say}/{len(sirali)}. Çok derste tekrar eden ⚖ kalıplar eşiğin ölçülmesi gereken adaylardır "
              "(yanlış alarm oranı ölçülmeden eşik değişmez).", ""]

    # 2) H maddeleri: hangi alan, hangi anahtar sözcükler en çok hataya konu oldu
    if DIZIN.exists():
        d = json.loads(DIZIN.read_text(encoding="utf-8"))["maddeler"]
        alan = collections.Counter(Path(m["dosya"]).stem for m in d)
        soz = collections.Counter(w for m in d for w in set(m.get("anahtarlar", [])) if len(w) > 4 and "/" not in w and "." not in w)
        L += [f"## 2. Geçmiş hata kayıtları (H maddeleri: {len(d)})", "",
              "**Alan başına:** " + ", ".join(f"{x} {n}" for x, n in alan.most_common()), "",
              "**En sık anahtar sözcükler:** " + ", ".join(f"{x} ({n})" for x, n in soz.most_common(30)), ""]

    # 3) Model çağrıları: yeniden deneme, boş yanıt, yetki hatası
    g = _jsonl(GOREV)
    if g:
        olay = collections.Counter(x.get("olay") for x in g)
        yeniden = collections.Counter(x.get("is_id", "").split("--")[0] for x in g if x.get("olay") == "cagri" and (x.get("tur") or 0) > 0)
        hata = collections.Counter(imza(x.get("mesaj") or x.get("hata") or "") for x in g if x.get("olay") in ("model_uyari", "ajan_hata", "claude_hata"))
        L += [f"## 3. Model çağrı günlüğü ({len(g)} olay)", "", "**Olaylar:** " + ", ".join(f"{x} {n}" for x, n in olay.most_common()), "",
              "**Yeniden tur alan görev türleri:** " + (", ".join(f"{x} {n}" for x, n in yeniden.most_common(12)) or "yok"), "",
              "**Sık model hataları:**", ""] + [f"- {n}× `{x[:120]}`" for x, n in hata.most_common(10)] + [""]

    L += ["## Nasıl okunur", "",
          "- Bir kalıp çok derste ve çok turda görünüyorsa kural ya model talimatında açık değil ya da eşik ölçülmemiş: önce talimata/"
          "betik düzeltmesine bak (betikle düzeltilebiliyorsa LLM turu harcama).",
          "- ⚖ kalıplarda eşiği değiştirmeden önce yanlış alarm oranını örneklemle ölç ve kullanıcıya sun.", ""]
    TEMP.mkdir(parents=True, exist_ok=True)
    (TEMP / "rapor.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n→ {TEMP / 'rapor.md'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    t = alt.add_parser("tara")
    t.add_argument("--kurul", type=int, default=2)
    t.add_argument("--ders")
    t.add_argument("--asama")
    t.add_argument("--zaman", type=int, default=180)
    r = alt.add_parser("rapor")
    r.add_argument("--gun", type=int, default=60)
    r.add_argument("--n", type=int, default=25)
    a = ap.parse_args()
    return tara(a) if a.komut == "tara" else rapor(a)


if __name__ == "__main__":
    sys.exit(main())
