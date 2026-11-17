#!/usr/bin/env python3
"""Kayıt kapısı (kullanıcı kararı 2026-11-17, H610) — tam içerik işçisi ve her ajan, ders üretirken / talimat güncellerken /
hata bildirirken mevcut optimizasyonu bozan ve token kabartan YAZIMLARI yapamasın. Yalnız DEĞİŞENE bakar (git farkı);
eski içerik geriye dönük bozuk sayılmaz. LLM/ağ yok, stdlib.

  python3 scripts/kapilar/kayit_kapisi.py            # çalışma ağacı (HEAD'e göre fark + izlenmeyen yeni dosyalar)
  python3 scripts/kapilar/kayit_kapisi.py --sahne    # yalnız sahnelenen (pre-commit)
  python3 scripts/kapilar/kayit_kapisi.py --json

K1 HATA  yeni hata maddesi (docs/hatalar/*.md): Belirti + Kök neden + Çözüm + Kural alanları zorunlu; >400 kelime HATA
         (>250 UYARI); H numarası başka maddede varsa HATA; hata metni dizine (KURUL2_YAPILMAYACAK_HATALAR.md) yazılmaz.
K2 HATA  DEGISIKLIK_KAYDI.md: yeni bölüm >400 kelime HATA (>250 UYARI); bölüm sayısı >25 → eskiyi kayitlar/'a taşı.
K3 HATA  talimat belgesine (AGENTS/CLAUDE.md, KURALLAR_*, standart/akış belgeleri, TALIMAT*.md) eklenen
         (üretilmiş docs/asama_kurallari/ hariç: aşamalar arası tekrar tasarımdır) ≥10 kelimelik satır başka talimat belgesinde ya da aynı belgede zaten varsa (tekrar = her aşamada iki kez okunur);
         klasör CLAUDE.md >400 kelime UYARI.
K4 HATA  veri: src/data|data altında yedek/kopya adlı yeni dosya (veri_bakim.py arsivle kullan), aynı içerikli iki yeni dosya,
         `baglam/` ya da meds_temp çalışma verisi sahnelenmesi. >1 MB girintili yeni JSON UYARI (tek satır/sıkı yaz).
Çıkış: 0 = HATA yok, 1 = HATA. Eşik gevşetmek YASAK (kapilar/CLAUDE.md); muafiyet yalnız gerekçeyle bu dosyada.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.insert(0, str(_d))
from kok import MEDS  # noqa: E402

KOK = Path(MEDS)
H_BAS = re.compile(r"^#{2,3}\s+(H\d+)\b", re.M)
ALANLAR = {
    "Belirti": re.compile(r"\*\*Belirti", re.I),
    "Kök neden": re.compile(r"\*\*K[oö]k", re.I),
    "Çözüm": re.compile(r"\*\*(Kal[ıi]c[ıi] )?[çc][öo]z[üu]m", re.I),
    "Kural": re.compile(r"\*\*([ÖO]nleme|Kural)", re.I),
}
TALIMAT = re.compile(r"(^|/)(AGENTS\.md|CLAUDE\.md|TALIMAT[^/]*\.md)$|^docs/(KURALLAR_[^/]+|"
                     r"TAM_HAT_HIZLI_AKIS|KURUL2_DERS_STANDARDI|KURUL_OTOMASYON_EL_KITABI|OGREN_ETKILESIM_REHBERI)(\.md)?$")
YEDEK_AD = re.compile(r"(yedek|backup|\.bak$|_eski\b|_kopya|\bcopy\b|\.orig$|~$)", re.I)
VERI = re.compile(r"^(src/data|data)/")
CALISMA = re.compile(r"(^|/)baglam/|^meds_temp/")
SINIR = {"hata": (250, 400), "kayit": (250, 400), "kayit_bolum": 25, "claude_md": 400, "tekrar_kelime": 10}


def git(*a: str) -> str:
    r = subprocess.run(["git", *a], cwd=KOK, capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""


def degisenler(sahne: bool) -> list[str]:
    if sahne:
        return [p for p in git("diff", "--cached", "--name-only", "--diff-filter=AMR").splitlines() if p]
    s = set(git("diff", "--name-only", "--diff-filter=AMR", "HEAD").splitlines())
    s |= set(git("ls-files", "--others", "--exclude-standard").splitlines())
    return sorted(p for p in s if p)


def eski(p: str) -> str:
    return git("show", f"HEAD:{p}")


def yeni(p: str, sahne: bool) -> str:
    if sahne:
        return git("show", f":{p}")
    f = KOK / p
    return f.read_text(encoding="utf-8", errors="replace") if f.is_file() else ""


def kelime(s: str) -> int:
    return len(s.split())


def katla(s: str) -> str:
    return re.sub(r"[\W_]+", " ", s.lower()).strip()


def maddeler(metin: str) -> dict[str, str]:
    ms = list(H_BAS.finditer(metin))
    return {m.group(1): metin[m.start(): (ms[i + 1].start() if i + 1 < len(ms) else len(metin))]
            for i, m in enumerate(ms)}


def denetle(sahne: bool) -> list[dict]:
    bul: list[dict] = []
    ekle = lambda k, d, y, m: bul.append({"kod": k, "duzey": d, "yol": y, "mesaj": m})  # noqa: E731
    dosyalar = degisenler(sahne)

    # K1 — hata maddeleri
    tum_h: dict[str, list[str]] = {}
    for f in sorted((KOK / "docs/hatalar").glob("*.md")):
        for h in maddeler(f.read_text(encoding="utf-8")):
            tum_h.setdefault(h, []).append(f.name)
    for p in dosyalar:
        if p.startswith("docs/hatalar/") and p.endswith(".md"):
            onceki = maddeler(eski(p))
            for h, govde in maddeler(yeni(p, sahne)).items():
                if h in onceki:
                    continue
                w = kelime(govde)
                if w > SINIR["hata"][1]:
                    ekle("K1", "HATA", p, f"{h} {w} kelime > {SINIR['hata'][1]} — belirti/kök/çözüm/kural öz yaz, ayrıntı koda/belgeye işaret")
                elif w > SINIR["hata"][0]:
                    ekle("K1", "UYARI", p, f"{h} {w} kelime > {SINIR['hata'][0]}")
                eksik = [a for a, r in ALANLAR.items() if not r.search(govde)]
                if eksik:
                    ekle("K1", "HATA", p, f"{h} eksik alan: {', '.join(eksik)} (AGENTS: belirti + kök neden + kalıcı çözüm + kural)")
                if len(tum_h.get(h, [])) > 1:
                    ekle("K1", "HATA", p, f"{h} numarası birden çok maddede: {tum_h[h]} — yeni numara al (hata_dizini.py)")
        if p == "docs/KURUL2_YAPILMAYACAK_HATALAR.md":
            artis = kelime(yeni(p, sahne)) - kelime(eski(p))
            if artis > 80:
                ekle("K1", "HATA", p, f"dizine +{artis} kelime — madde metni docs/hatalar/<konu>.md'ye yazılır, dizine yalnız satır")

    # K2 — değişiklik kaydı (depo kökünün bir üstünde; git dışında → yalnız mutlak ölçü)
    kayit = KOK.parent / "DEGISIKLIK_KAYDI.md"
    if kayit.exists():
        bolumler = re.split(r"\n## \[", kayit.read_text(encoding="utf-8"))[1:]
        if len(bolumler) > SINIR["kayit_bolum"]:
            ekle("K2", "HATA", "DEGISIKLIK_KAYDI.md", f"{len(bolumler)} bölüm > {SINIR['kayit_bolum']} — en eskileri kayitlar/'a taşı")
        if bolumler:  # yalnız en yeni bölüm (bu oturumun kaydı) ölçülür
            w = kelime(bolumler[0])
            if w > SINIR["kayit"][1]:
                ekle("K2", "HATA", "DEGISIKLIK_KAYDI.md", f"en yeni bölüm {w} kelime > {SINIR['kayit'][1]} — ne/neden/yol; ayrıntı H maddesinde")
            elif w > SINIR["kayit"][0]:
                ekle("K2", "UYARI", "DEGISIKLIK_KAYDI.md", f"en yeni bölüm {w} kelime > {SINIR['kayit'][0]}")

    # K3 — talimat tekrarı
    talimatlar = [p for p in dosyalar if TALIMAT.search(p)]
    if talimatlar:
        derlem: dict[str, set[str]] = {}
        adaylar = [Path("../AGENTS.md")] + [x.relative_to(KOK) for x in KOK.rglob("*.md")
                                             if TALIMAT.search(str(x.relative_to(KOK))) and "node_modules" not in x.parts]
        for x in adaylar:
            try:
                derlem[str(x)] = {katla(l) for l in (KOK / x).read_text(encoding="utf-8").splitlines()
                                  if kelime(katla(l)) >= SINIR["tekrar_kelime"]}
            except OSError:
                pass
        for p in talimatlar:
            o, n = eski(p).splitlines(), yeni(p, sahne).splitlines()
            eklenen = [l for t, l in ((l[:2], l[2:]) for l in difflib.ndiff(o, n)) if t == "+ "]
            sayac: dict[str, int] = {}
            for l in n:
                sayac[katla(l)] = sayac.get(katla(l), 0) + 1
            for l in eklenen:
                k = katla(l)
                if kelime(k) < SINIR["tekrar_kelime"]:
                    continue
                yer = [f for f, s in derlem.items() if f != p and k in s] or (["aynı belgede iki kez"] if sayac.get(k, 0) > 1 else [])
                if yer:
                    ekle("K3", "HATA", p, f"tekrar satır ({yer[0]}): «{l.strip()[:70]}…» — tek yerde yaz, öbüründe işaret ver")
            if p.endswith("CLAUDE.md") and p.count("/") and kelime("\n".join(n)) > SINIR["claude_md"]:
                ekle("K3", "UYARI", p, f"klasör CLAUDE.md {kelime(chr(10).join(n))} kelime > {SINIR['claude_md']} — kısa tut, ayrıntı belgeye")

    # K4 — veri yazımı
    ozler: dict[str, str] = {}
    for p in dosyalar:
        if CALISMA.search(p) and sahne:
            ekle("K4", "HATA", p, "çalışma verisi (baglam/, meds_temp) git'e girmez")
            continue
        if not VERI.match(p):
            continue
        f = KOK / p
        if not f.is_file():
            continue
        if YEDEK_AD.search(Path(p).name) and not eski(p):
            ekle("K4", "HATA", p, "yedek/kopya adlı yeni veri dosyası — veri_bakim.py arsivle ile _arsiv_veri/'ye al")
        if f.stat().st_size > 4096 and not p.endswith((".mp3", ".wav", ".ogg", ".png", ".jpg", ".webp", ".pdf")):
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            if h in ozler:
                ekle("K4", "HATA", p, f"içerik {ozler[h]} ile aynı — iki kopya tutulmaz, birini kaynak yap")
            ozler.setdefault(h, p)
        if p.endswith(".json") and f.stat().st_size > 1_000_000 and not eski(p):
            bas = f.open("rb").read(4096)
            if b"\n  " in bas:
                ekle("K4", "UYARI", p, f"{f.stat().st_size // 1024} KB girintili JSON — separators=(',',':') ile sıkı yaz")
    return bul


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sahne", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    b = denetle(a.sahne)
    hata = sum(1 for x in b if x["duzey"] == "HATA")
    if a.json:
        print(json.dumps({"hata": hata, "bulgular": b}, ensure_ascii=False, indent=1))
    else:
        for x in b:
            print(f"{x['kod']} {x['duzey']:<5} {x['yol']}: {x['mesaj']}")
        print(f"kayıt kapısı: {hata} HATA, {len(b) - hata} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
