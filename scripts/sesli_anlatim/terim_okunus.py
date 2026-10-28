#!/usr/bin/env python3
"""İngilizce/Latince tıbbi terim okunuşu — YALNIZ EMA'ya giden metne uygulanır (kullanıcı, 2026-10-28).

Ders metninde kalan yabancı yazımlar (Wernicke, Staphylococcus, amaurosis fugax, locked-in, Xanax) EMA'da Türkçe harf
kurallarıyla yanlış okunuyordu ("ştafilokokus", "vernikke"). Okunuş Türkiye tıp fakültelerindeki yaygın söyleyiştir:
  1. sözlük  data/sesli_anlatim/okunus/terim_okunus.json (eponim, Latince, İngilizce, ticari ad; çok sözcüklü önce)
  2. kural   sözlükte olmayan yabancı görünümlü sözcükler için Latince okunuş (ph→f, th→t, ch→k, sch→ş, ae/oe→e,
             y→i, c+e/i→s, c→k, x→ks, w→v, qu→kv, çift ünsüz tekleşir). Yalnız büyük harfle başlayan (eponim/cins adı)
             ya da güçlü yabancı iz taşıyan (w, x, q, ph, th, ch, ck, ae, oe) sözcüklere; Türkçe harfli sözcüklere dokunmaz.
Ek (Wernicke'de) korunur: "Vernikede". Paragraf/cümle sayısı değişmez (nokta eklenmez/silinmez).

Kullanım:
  terim_okunus.py "metin"               # dönüştürülmüş metni yazar
  terim_okunus.py --denetle <md|anahtar> # yabancı sözcükler → okunuş; sözlükte olmayanları "KURAL" diye işaretler
  terim_okunus.py --tara                 # tüm metinlerde sözlükte olmayan yabancı sözcük sıklığı (sözlük büyütmek için)
"""
from __future__ import annotations

import collections
import functools
import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
SOZLUK = MEDS / "data/sesli_anlatim/okunus/terim_okunus.json"
METIN = MEDS / "data/sesli_anlatim/metin"
TR_HARF = set("çğıöşüÇĞİÖŞÜâîû")
GUCLU_IZ = re.compile(r"[wxq]|ph|th|ch|ck|sch|ae$|oe$", re.IGNORECASE)  # ae/oe yalnız sonda: aerob, tromboemboli Türkçe
SOZ = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüâîûéèàáíóúÉ]+(?:-[A-Za-zÇĞİÖŞÜçğıöşüéè]+)*(?:['’][a-zçğıöşü]+)?")
# büyük harf zorunlu kısaltmalar (DNA, CD4) okunus.py / kisaltma_ses.py'nin işi — burada dokunulmaz
KISALTMA = re.compile(r"^[A-ZÇĞİÖŞÜ0-9]{2,}$|^[a-z]*[A-Z].*[A-Z]")  # DNA, vWF, PTHrP: kısaltma katmanının işi


@functools.lru_cache(maxsize=1)
def sozluk() -> dict[str, str]:
    d = json.loads(SOZLUK.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update({a.lower(): b for a, b in v.items()})
    return out


@functools.lru_cache(maxsize=1)
def _cok_sozcuklu() -> re.Pattern | None:
    anahtar = sorted((k for k in sozluk() if " " in k or "-" in k or "'" in k), key=len, reverse=True)
    if not anahtar:
        return None
    alt = "|".join(re.escape(k).replace(r"\ ", r"[\s-]+") for k in anahtar)
    return re.compile(rf"(?<![\wçğıöşü])({alt})((?:['’][a-zçğıöşü]+)?)(?![\wçğıöşü])", re.IGNORECASE)


def latince(w: str) -> str:
    """Kural motoru: Latince/Batı yazımı → Türkçe okunuş (küçük harf)."""
    s = w.lower()
    for a, b in (("sch", "ş"), ("tsch", "ç"), ("tch", "ç"), ("ph", "f"), ("th", "t"), ("rh", "r"), ("ch", "k"), ("ck", "k"), ("qu", "kv"),
                 ("x", "ks"), ("w", "v"), ("q", "k")):
        s = s.replace(a, b)
    s = re.sub(r"(?:ae|oe)$", "e", s)
    s = re.sub(r"^ae", "e", s)
    s = re.sub(r"cc(?=[eiy])", "ks", s)
    s = re.sub(r"c(?=[eiy])", "s", s)
    s = s.replace("c", "k")
    s = re.sub(r"(?<=[^aeiouöüı])y|^y(?=[^aeiou])", "i", s)
    s = re.sub(r"y(?=[^aeiouöüı]|$)", "i", s)
    s = re.sub(r"([bdfgklmnprstvz])\1", r"\1", s)
    s = re.sub(r"ii$", "i", s)
    s = s.replace("é", "e").replace("è", "e").replace("à", "a").replace("á", "a").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return s


def yabanci_mi(w: str, cumle_basi: bool) -> bool:
    if any(c in TR_HARF for c in w) or KISALTMA.match(w) or len(w) < 3:
        return False
    if w[:1].islower() and not GUCLU_IZ.search(re.sub(r"th", "", w)):
        return False  # küçük harfli Türkçe birleşikler: ameliyathane (th) dokunulmaz
    if GUCLU_IZ.search(w):
        return True
    return False  # büyük harf tek başına yetmez (Türkçe özel adlar, cümle başı) — sözlük yoksa dokunma


def _kucuk(s: str) -> str:
    return s.replace("İ", "i").replace("I", "ı").lower() if any(c in TR_HARF for c in s) else s.replace("İ", "i").lower()


def _buyuk(orj: str, yeni: str) -> str:
    return yeni[:1].upper() + yeni[1:] if orj[:1].isupper() else yeni


def _cevir(w: str, cumle_basi: bool) -> tuple[str, str] | None:
    """(yeni, kaynak) — kaynak: sozluk | kural."""
    gov, ek = re.match(r"(.+?)((?:['’][a-zçğıöşü]+)?)$", w).groups()
    ek = ek.lstrip("'’")
    D = sozluk()
    parca = gov.split("-")
    if gov.lower() in D:
        return _buyuk(gov, D[gov.lower()]) + ek, "sozluk"
    if len(parca) > 1:
        out = []
        for p in parca:
            r = _cevir(p, False)
            out.append(r[0] if r else p)
        return " ".join(out) + ek, "sozluk"
    if yabanci_mi(gov, cumle_basi):
        return _buyuk(gov, latince(gov)) + ek, "kural"
    return None


def donustur(metin: str, kayit: list | None = None) -> str:
    rx = _cok_sozcuklu()
    if rx:
        def cok(m):
            yeni = sozluk()[re.sub(r"[\s-]+", " ", _kucuk(m.group(1)))]
            if kayit is not None:
                kayit.append((m.group(0), yeni, "sozluk"))
            return _buyuk(m.group(1), yeni) + m.group(2).lstrip("'’")
        metin = rx.sub(cok, metin)
    out, son = [], 0
    for m in SOZ.finditer(metin):
        w = m.group(0)
        bas = m.start() == 0 or metin[:m.start()].rstrip()[-1:] in ".!?:\n"
        r = _cevir(w, bas)
        if r and r[0] != w:
            out.append(metin[son:m.start()] + r[0])
            son = m.end()
            if kayit is not None:
                kayit.append((w, r[0], r[1]))
    out.append(metin[son:])
    return "".join(out)


def _dosya(arg: str) -> Path:
    p = Path(arg)
    return p if p.exists() else METIN / f"{arg}.md"


def main(argv: list[str]) -> int:
    if argv[:1] == ["--denetle"]:
        kayit: list = []
        donustur(_dosya(argv[1]).read_text(encoding="utf-8"), kayit)
        say = collections.Counter(kayit)
        for (a, b, k), n in sorted(say.items(), key=lambda x: (x[0][2] != "kural", -x[1])):
            print(f"{'KURAL ' if k == 'kural' else '      '}{n:3d}  {a} → {b}")
        kural = sum(1 for (_, _, k) in say if k == "kural")
        print(f"\n{len(say)} farklı yabancı yazım; {kural} tanesi sözlükte yok (kural motoru). Yanlış okunanı {SOZLUK.name}'a ekle.")
        return 0
    if argv[:1] == ["--tara"]:
        say = collections.Counter()
        for f in sorted(METIN.glob("*.md")):
            kayit: list = []
            donustur(f.read_text(encoding="utf-8"), kayit)
            say.update((a, b) for a, b, k in kayit if k == "kural")
        for (a, b), n in say.most_common(int(argv[1]) if len(argv) > 1 else 150):
            print(f"{n:4d}  {a} → {b}")
        return 0
    if argv:
        print(donustur(" ".join(argv)))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
