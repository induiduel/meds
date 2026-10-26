#!/usr/bin/env python3
"""Terim analizi — bir dersin PDF slaytları ve konuşmacı metninde geçen, sözlükte/terim dosyasında olmayan
"yabancı ya da bilinmesi zor" sözcükleri çıkarır (kullanıcı isteği 2026-10-26).

Amaç: terim yazarının (DeepSeek) her derste eksik kalan zor terimleri görmesi. Kapı değildir; hiçbir dosya yazmaz.
Çıktı: sayfa sayfa aday sözcükler + dilim bağlamı + kapsam özeti. Türkçe kökenli sözcükler (ekleriyle) elenir.

Kullanım:
  python3 scripts/sesli_anlatim/terim_analiz.py <key> [--en-cok 60] [--json]
  python3 scripts/sesli_anlatim/terim_analiz.py --liste            # terim dosyası olan/olmayan dersler
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

os_import = __import__("os")
os_import.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import urllib.request as _ur  # noqa: E402
import terim_sozlugu as _ts  # noqa: E402
import pdf_isaret as _pi  # noqa: E402
from pdf_hizala import STOP, katla  # noqa: E402
from terim_sozlugu import MEDS, TOK, ek_mi, fold, kok_sec, sayfalar, sozluk, turkce_kokenli  # noqa: E402

_ts.API = os_import.environ.get("MEDS_API", "https://api.nofrostlife.com.tr")
_pi.API = _ts.API


def ders(key: str) -> dict:
    """Ders bilgisi yerel hizalama dosyasından (PDF listesi + deckId); sunucuya sorulmaz."""
    h = kok_sec(key) / "hizalama" / f"{key}.json"
    d = json.loads(h.read_text(encoding="utf-8"))
    return {"key": key, "deckId": d.get("deckId", ""), "pdf": {"deckId": d.get("deckId", ""), "dosyalar": d.get("dosyalar") or []}}

EN_AZ = 4          # bundan kısa sözcük aday sayılmaz (kısaltmalar ayrı)
NGRAM = 6          # sözlük ifadesi eşleştirmesinde en çok sözcük
SOZLUK_DOSYA = Path("/usr/share/hunspell/tr_TR.dic")

# Türkçe ekler (katlanmış yazım) — uzundan kısaya; bir sözcükten en çok 4 kez soyulur.
EKLER = sorted(
    """leri ları ler lar leri lari nin nun nın nün nda nde ndan nden yla yle yız yiz dir dur tır tür
    dan den tan ten da de ta te ye ya yi yı yu yü in un ın ün i u ı ü e a
    lik lık luk lük li lı lu lü siz sız suz süz sel sal ce ca ci cı cu cü ki ken mek mak
    si sı su sü y n m k""".split(),
    key=len, reverse=True,
)


def _turkce_kokler() -> set[str]:
    k: set[str] = set()
    try:
        with SOZLUK_DOSYA.open(encoding="utf-8") as f:
            next(f, None)
            for satir in f:
                s = satir.split("/")[0].strip()
                if s and not s.startswith("#"):
                    k.add(fold(s))
    except OSError:
        pass
    return k


TURKCE_KOKLER = _turkce_kokler()


def turkce_sozcuk(w: str) -> bool:
    """Sözcük Türkçe sözlük köklerinden biri + Türkçe eklerle açıklanabiliyorsa Türkçedir."""
    if turkce_kokenli(w):
        return True
    kok = fold(w)
    if kok in TURKCE_KOKLER:
        return True
    for _ in range(4):
        for ek in EKLER:
            if len(kok) - len(ek) >= 3 and kok.endswith(ek):
                kok = kok[: -len(ek)]
                if kok in TURKCE_KOKLER:
                    return True
                break
        else:
            return False
    return False


def sozluk_ifadeleri() -> set[tuple[str, ...]]:
    """Doğrulanmış sözlükteki terim + takma ad ifadeleri (katlanmış sözcük dizisi)."""
    g = json.loads((MEDS / "src/data/medical_glossary.json").read_text(encoding="utf-8"))
    out: set[tuple[str, ...]] = set()
    for v in g.values():
        if not isinstance(v, dict):
            continue
        for ad in [v.get("term", "")] + list(v.get("aliases") or []):
            par = tuple(fold(m.group()) for m in TOK.finditer(re.sub(r"\(.*?\)", " ", str(ad))))
            par = tuple(p for p in par if p)
            if par:
                out.add(par)
    return out


def terim_dosyasi(key: str) -> dict[str, list[dict]]:
    y = kok_sec(key) / "terim" / f"{key}.json"
    if not y.exists():
        return {}
    d = json.loads(y.read_text(encoding="utf-8"))
    return {f"{di}:{si}": sy.get("t", []) for di, dos in d.get("d", {}).items() for si, sy in dos.items()}


def kapsanan(seq: list[str], ifadeler: set[tuple[str, ...]], az: int = 1) -> set[int]:
    """seq içinde sözlük ifadesine düşen konumlar."""
    kap: set[int] = set()
    for n in range(min(NGRAM, len(seq)), az - 1, -1):
        for i in range(len(seq) - n + 1):
            if tuple(seq[i:i + n]) in ifadeler:
                kap.update(range(i, i + n))
    return kap


def analiz(key: str, en_cok: int) -> dict:
    sy = sayfalar(ders(key))
    ifadeler = sozluk_ifadeleri()
    td = terim_dosyasi(key)
    terimler = [fold(x["t"]) for l in td.values() for x in l]
    terim_ifade = {tuple(fold(m.group()) for m in TOK.finditer(t)) for t in terimler}
    sayfa_bilgi = []
    aday: dict[str, dict] = {}
    for yer, s in sy.items():
        seq = [w for w, _, _ in s.kel]
        if not seq:
            sayfa_bilgi.append({"yer": yer, "kelime": 0, "terim": len(td.get(yer, []))})
            continue
        kap = kapsanan(seq, ifadeler) | kapsanan(seq, terim_ifade)
        metin = " ".join(s.metin_satir)
        for i, w in enumerate(seq):
            if i in kap or len(w) < EN_AZ or w.isdigit():
                continue
            if w in STOP or turkce_sozcuk(w):
                continue
            a = aday.setdefault(w, {"w": w, "n": 0, "sayfa": [], "ornek": ""})
            a["n"] += 1
            if yer not in a["sayfa"]:
                a["sayfa"].append(yer)
            if not a["ornek"]:
                m = re.search(rf"\b{re.escape(w)}\w*", metin, re.I)
                if m:
                    b = max(0, m.start() - 60)
                    a["ornek"] = metin[b:m.end() + 60].replace("\n", " ")
        sayfa_bilgi.append({"yer": yer, "kelime": len(seq), "terim": len(td.get(yer, []))})
    liste = sorted(aday.values(), key=lambda x: (-x["n"], x["w"]))[:en_cok]
    eksik = [p["yer"] for p in sayfa_bilgi if p["kelime"] >= 8 and p["terim"] == 0]
    return {
        "key": key, "sayfa": len(sy), "terim": len(terimler), "terimsiz_sayfa": len(eksik),
        "eksik_sayfalar": eksik[:40], "aday": liste, "aday_sayi": len(aday),
    }


def ders_listesi() -> None:
    for kok in (MEDS / "data/sesli_anlatim", MEDS / "data/arsiv_25_26/sesli_anlatim"):
        hiz = {p.stem for p in (kok / "hizalama").glob("*.json")}
        ter = {p.stem for p in (kok / "terim").glob("*.json")}
        print(f"# {kok.relative_to(MEDS)}: hizalama {len(hiz)} · terim {len(ter)} · terimsiz {len(hiz - ter)}")
        for k in sorted(hiz - ter):
            print("  -", k)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("key", nargs="?")
    ap.add_argument("--en-cok", type=int, default=60)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.key or a.key == "--liste":
        ders_listesi()
        return 0
    r = analiz(a.key, a.en_cok)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    print(f"# {r['key']}: {r['sayfa']} sayfa · {r['terim']} terim · terimsiz sayfa {r['terimsiz_sayfa']}")
    if r["eksik_sayfalar"]:
        print("terimsiz sayfalar:", ", ".join(r["eksik_sayfalar"]))
    print(f"\n{len(r['aday'])} aday (en sık {r['aday_sayi']} içinden):")
    for x in r["aday"]:
        print(f"- {x['w']} ({x['n']}×, s.{','.join(x['sayfa'][:4])}) — {x['ornek'][:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
