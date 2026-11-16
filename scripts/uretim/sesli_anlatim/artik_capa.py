#!/usr/bin/env python3
"""Artık çapa (H605, kullanıcı kararı 2026-11-17): PDF işaretinde yalnız "sayfa"ya düşen cümleler için en ucuz çapa.

Tam çapa (E4, TALIMAT_CAPA.md) her cümleye görüntü bakarak yer seçer — pahalı; tasarruf kipinde hiç yapılmıyordu ve
çapasız derslerde cümlelerin ≈%18'i yalnız sayfa vurgusunda kalıyordu (takip_kapisi T5 üst %5). Bu adım YALNIZ
eşleşmeyen cümleleri, görüntüsüz, o sayfanın (±1) madde metinleriyle modele verir: ders başına ~10–20 cümle, ~1–2k token.
Betik → (yalnız artık) LLM → betik kapısı sırası; LLM çağrısı bu betikte YOK (hat oturumu/ajanı `cevap.json`'u yazar, kural 20).

  hazirla <key>    : işareti kuru üretir, "sayfa" kalan cümleleri bulur → meds_temp/artik_capa/<key>/is.md + cevap.json iskeleti
  birlestir <key>  : cevap.json'u data/sesli_anlatim/capa/<key>.json'a işler (yoksa kurar; mevcut çapanın öteki cümlelerine
                     dokunmaz), sonra pdf_isaret.py --key <key> ve takip_kapisi.py ile doğrular.

cevap.json: {"P3.C1": {"sayfa": 5, "madde": [2]} | {"sayfa": 5, "resim": 0} | null, …}
  null = slaytta karşılığı yok (giriş/geçiş/özet) → yalnız sayfa kalır. Uydurma madde YASAK.
Kullanım: .venv-ocr/bin/python scripts/uretim/sesli_anlatim/artik_capa.py hazirla|birlestir <key>   (MEDS_API gerekirse)
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdf_isaret as P  # noqa: E402

CALISMA = _kok.PROJE / "meds_temp" / "artik_capa"
BURADA = Path(__file__).resolve().parent


def _veri(key: str):
    with urllib.request.urlopen(P.api_iste(f"{P.API}/api/canli-ders/{key}"), timeout=30) as r:
        d = json.load(r)
    paras = [p for b in d["bolumler"] for p in b["paragraflar"]]
    return paras


def _pdfler(hz: dict) -> list:
    out = []
    for fi, f in enumerate(hz["dosyalar"]):
        yol = P.INDIR / f["path"]
        if not yol.exists():
            yol = P.pdf_indir(hz["deckId"], f, fi)
        out.append(P.Pdf(yol) if yol and yol.exists() else None)
    return out


def _sayfa_metni(sy, s: int) -> list[str]:
    sat = [f"  M{i}: {' '.join(m['metin'])[:160]}" for i, m in enumerate(sy.maddeler) if m["kok"]]
    sat += [f"  R{i}: görsel" for i in sy.tekil_resim]
    return [f"s.{s}:"] + sat


def hazirla(key: str) -> int:
    sonuc = P.ders_isle(key, kuru=True, zorla=True)
    if not sonuc:
        print(f"{key}: hizalama/metin yok"); return 1
    hz = json.loads((P.KOK / "hizalama" / f"{key}.json").read_text(encoding="utf-8"))
    paras = _veri(key)
    pdfler = _pdfler(hz)
    isr = sonuc["c"]
    satirlar, iskelet, sayfalar = [], {}, {}
    for p in paras:
        m = p["metin"]
        sinir = P.cumle_sonlari(m)
        for ci, x in enumerate(isr.get(str(p["i"]), [])):
            if x and x.get("t") != "sayfa":
                continue
            cid = f"P{p['i']}.C{ci}"
            s = int(x["s"]) if x else None
            d = int(x.get("d", 0)) if x else 0
            cumle = m[(sinir[ci - 1] if ci else 0):sinir[ci]].strip()
            satirlar.append(f"- {cid} (s.{s}, d{d}): {cumle}")
            iskelet[cid] = None
            if s and d < len(pdfler) and pdfler[d]:
                for s2 in (s - 1, s, s + 1):
                    sy = pdfler[d].sayfa(s2)
                    if sy and (d, s2) not in sayfalar:
                        sayfalar[(d, s2)] = _sayfa_metni(sy, s2) if d == 0 else [f"d{d} "] + _sayfa_metni(sy, s2)
    kl = CALISMA / key
    kl.mkdir(parents=True, exist_ok=True)
    toplam = sum(len(v) for v in isr.values())
    is_md = [f"# Artık çapa — {key}", "",
             f"{len(iskelet)} / {toplam} cümle slaytta işaretlenemedi. Her cümle için cevap.json'da madde (M#), görsel (R#) ya da null yaz.",
             "Kurallar: yalnız cümlenin GERÇEKTEN anlattığı madde; komşu sayfa (±1) olabilir, `sayfa`yı ona göre yaz. Giriş, geçiş,",
             "özet, \"bu soruldu\" cümlesi slaytta karşılığı yoksa null (önceki cümleyle aynı maddeyi anlatıyorsa o madde). Tahmin YASAK.",
             'Biçim: {"P3.C1": {"sayfa": 5, "madde": [2]}, "P3.C2": {"sayfa": 5, "resim": 0}, "P4.C0": null}', "",
             "## Cümleler", *satirlar, "", "## Sayfa maddeleri"]
    for k in sorted(sayfalar):
        is_md += sayfalar[k]
    (kl / "is.md").write_text("\n".join(is_md) + "\n", encoding="utf-8")
    cev = kl / "cevap.json"
    if not cev.exists():
        cev.write_text(json.dumps(iskelet, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{key}: {len(iskelet)}/{toplam} artık cümle → {kl / 'is.md'} (~{len(' '.join(is_md).split())} kelime); cevap: {cev}")
    return 0


def birlestir(key: str) -> int:
    kl = CALISMA / key
    cevap = json.loads((kl / "cevap.json").read_text(encoding="utf-8"))
    paras = _veri(key)
    md = P.KOK / "metin" / f"{key}.md"
    sha = hashlib.sha1(md.read_bytes()).hexdigest()
    capa_yol = P.KOK / "capa" / f"{key}.json"
    cj = json.loads(capa_yol.read_text(encoding="utf-8")) if capa_yol.exists() else None
    if not cj or cj.get("mdSha1") != sha or len(cj.get("p") or []) != len(paras):
        if cj:
            print(f"{key}: mevcut çapa metinle uyuşmuyor (eski) — artık çapa yalnız yeni cümleleri taşıyacak")
        cj = {"mdSha1": sha, "p": [[] for _ in paras], "kaynak": "artik_capa"}
    hata, yeni = [], 0
    for pn, p in enumerate(paras):
        m = p["metin"]
        sinir = P.cumle_sonlari(m)
        eski = P.cumle_capalari(m, sinir, cj["p"][pn]) if cj["p"][pn] else [[] for _ in sinir]
        liste = []
        for ci in range(len(sinir)):
            c = cevap.get(f"P{p['i']}.C{ci}")
            if c:
                if not isinstance(c, dict) or not c.get("sayfa") or not (c.get("madde") or c.get("resim") is not None):
                    hata.append(f"P{p['i']}.C{ci}: sayfa + madde/resim gerekli"); continue
                cumle = m[(sinir[ci - 1] if ci else 0):sinir[ci]].lstrip()
                liste.append({"ses": cumle[:60], "sayfa": int(c["sayfa"]), "dosya": int(c.get("dosya", 0)),
                              **({"madde": [int(i) for i in c["madde"]]} if c.get("madde") else {"resim": int(c["resim"])}),
                              "artik": 1})
                yeni += 1
            else:
                liste += eski[ci]
        cj["p"][pn] = liste
    if hata:
        print("\n".join("HATA " + h for h in hata)); return 1
    tmp = capa_yol.with_suffix(".tmp")
    tmp.write_text(json.dumps(cj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, capa_yol)
    print(f"{key}: {yeni} artık çapa işlendi → {capa_yol}")
    py = sys.executable
    r = subprocess.run([py, str(BURADA / "pdf_isaret.py"), "--key", key], text=True, capture_output=True)
    print((r.stdout or r.stderr).strip().splitlines()[-1:])
    r = subprocess.run([py, str(BURADA / "takip_kapisi.py"), key], text=True, capture_output=True)
    print(r.stdout.strip())
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("eylem", choices=("hazirla", "birlestir"))
    ap.add_argument("key")
    a = ap.parse_args()
    return hazirla(a.key) if a.eylem == "hazirla" else birlestir(a.key)


if __name__ == "__main__":
    sys.exit(main())
