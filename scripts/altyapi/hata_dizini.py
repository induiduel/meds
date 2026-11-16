#!/usr/bin/env python3
"""hata_dizini.py — hata defterini madde düzeyinde dizinler (stdlib, LLM yok).

  python3 scripts/altyapi/hata_dizini.py            # docs/hatalar/_dizin.json üretir
  python3 scripts/altyapi/hata_dizini.py --denetle  # bayatsa çıkış 1

Her madde (docs/hatalar/*.md içindeki ##/### başlığı): {id, baslik, dosya, satir_bas, satir_son, kelime, anahtarlar}.
Anahtarlar: başlık + dizin özeti + "Kök neden"/"Önleme"/"Kural"/"Çözüm" satırlarından katlanmış anlamlı kelimeler
ve maddenin andığı yol/dosya adları. Okuma: Read offset=satir_bas limit=satir_son-satir_bas+1.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.insert(0, str(_d))
import kok as _kok  # noqa: E402

MEDS = _kok.MEDS
HATALAR = MEDS / "docs" / "hatalar"
DIZIN_MD = MEDS / "docs" / "KURUL2_YAPILMAYACAK_HATALAR.md"
CIKTI = HATALAR / "_dizin.json"
TR = str.maketrans("ıİşŞğĞüÜöÖçÇâÂîÎûÛ", "iissgguuoocCaaiiuu")
DURAK = set("""ve veya ile bir bu su o da de ki mi icin gibi daha en cok az her hic ya yani ama fakat ancak cunku
olan olarak oldu olur olmaz yok var degil ise eger kadar sonra once ayni yalniz sadece tum butun hep artik
icinde ustune uzerine gore dogru yeni eski iki tek ilk son bazen hala kendi neden nasil ne hangi diye
the and for with from into not are was this that yap yapilir yapilmaz edilir eder edildi kullanici""".split())
ALAN = re.compile(r"^\s*[-*]?\s*\*\*(K[oö]k( neden)?|[ÖO]nleme( kural[ıi])?|Kural|[ÇC][öo]z[üu]m[^*]*|Kal[ıi]c[ıi] [çc][öo]z[üu]m)[^*]*\*\*", re.I)
YOL = re.compile(r"[\w.\-]*[/][\w./\-]+|[\w\-]+\.(?:py|ts|tsx|mjs|js|json|md|sh|css|service|timer)\b")
BASLIK = re.compile(r"^(#{2,3})\s+(.*)$")


def katla(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.translate(TR).lower()).strip()


def kelimeler(s: str) -> list[str]:
    return [k for k in katla(s).split() if len(k) >= 3 and k not in DURAK and not k.isdigit()]


def ozetler() -> dict[str, str]:
    o: dict[str, str] = {}
    for m in re.finditer(r"^- \*\*(H\d+)\*\* · (.*?)(?: → hatalar/\S+)?$", DIZIN_MD.read_text(encoding="utf-8"), re.M):
        o.setdefault(m.group(1), m.group(2))
    return o


def uret() -> dict:
    oz = ozetler()
    maddeler = []
    for f in sorted(HATALAR.glob("*.md")):
        satirlar = f.read_text(encoding="utf-8").split("\n")
        bas = [(i, m) for i, s in enumerate(satirlar) if (m := BASLIK.match(s))]
        for j, (i, m) in enumerate(bas):
            son = (bas[j + 1][0] if j + 1 < len(bas) else len(satirlar))
            while son > i + 1 and not satirlar[son - 1].strip():
                son -= 1
            govde = satirlar[i + 1:son]
            baslik = m.group(2).strip()
            hm = re.match(r"\[?(H\d+)\b", baslik)
            hid = hm.group(1) if hm else None
            anah: dict[str, None] = {k: None for k in kelimeler(f.stem.replace("_", " "))}  # konu dosyası adı
            for k in kelimeler(re.sub(r"^H\d+\s*[—-]\s*", "", baslik)) + kelimeler(oz.get(hid, "") if hid else ""):
                anah[k] = None
            for s in govde:
                if ALAN.match(s):
                    for k in kelimeler(ALAN.sub("", s)):
                        anah[k] = None
            yollar = {y.strip("./`") for s in [baslik, *govde] for y in YOL.findall(s) if len(y) > 3}
            for y in sorted(yollar):
                anah[y.lower()] = None
                anah[Path(y).name.lower()] = None
            maddeler.append({
                "id": hid, "baslik": (baslik if len(baslik) > 8 or not hid else f"{hid} · {oz.get(hid, '')}")[:200], "dosya": f"docs/hatalar/{f.name}",
                "satir_bas": i + 1, "satir_son": son,
                "kelime": sum(len(s.split()) for s in govde) + len(baslik.split()),
                "anahtarlar": list(anah)[:120],
            })
    return {"surum": 1, "kaynak": "scripts/altyapi/hata_dizini.py", "madde_sayisi": len(maddeler), "maddeler": maddeler}


def yaz_metin(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace('},{"id"', '},\n{"id"') + "\n"


def main(argv: list[str]) -> int:
    metin = yaz_metin(uret())
    if "--denetle" in argv:
        if not CIKTI.exists() or CIKTI.read_text(encoding="utf-8") != metin:
            print("HATA docs/hatalar/_dizin.json bayat — yeniden üret: python3 scripts/altyapi/hata_dizini.py")
            return 1
        print("hata dizini güncel")
        return 0
    CIKTI.write_text(metin, encoding="utf-8")
    print(f"{CIKTI.relative_to(MEDS)}: {metin.count(chr(10))} madde")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
