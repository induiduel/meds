#!/usr/bin/env python3
"""Canlı çizim üretimi (R6, ICERIK_MOTORU_V3.md §4): sesli dersin cümlelerine PDF üstünde kontur / akış oku / eğri fazı /
şema komutları.

Girdi: anlamsal çapa dökümü (capa_dok.py: sNN.png numaralı kutularla, sNN.txt, cumleler.md) + çapa (capa.json: cümle →
sayfa) + işaret (isaret/<key>.json: metinHash). Sayfalar 6'lık partilere bölünür, her parti ayrı Claude oturumunda
(TALIMAT_CIZIM.md, görüntüleri Read ile görür) aynı anda yazılır; her komut cizim_dogrula.py kapısından geçer (geçmeyen
atılır). Kelime aralığı cümle içi karakter aralığına çevrilir (ön yüz imleci karakterle ilerler).

Çıktı: data/sesli_anlatim/cizim/<key>.json = {"surum": 1, "metinHash": <isaret ile aynı>, "p": {"<P>": {"<C>": [komut]}},
          "rapor": {...}}; sunucu (canliDers.ts) metinHash tutarsa işaret kaydına `z` olarak ekler.

Kullanım: .venv-ocr/bin/python scripts/cizim/cizim_uret.py <key> --dok <capa_dok dizini> --capa <capa.json>
            --isaret <isaret.json> [--paralel 4] [--parti 6] [--kuru]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDS = HERE.parents[1]
sys.path.insert(0, str(HERE))
import cizim_dogrula as CD  # noqa: E402

TALIMAT = HERE / "TALIMAT_CIZIM.md"
KOK = MEDS / "data" / "sesli_anlatim"


def cumleler(md: Path) -> dict[str, str]:
    out = {}
    for satir in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(P\d+\.C\d+):\s*(.*)$", satir)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def kelime_araliklari(metin: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", metin)]


def kutular(txt: Path) -> list[list[float]]:
    out = []
    if txt.exists():
        for s in txt.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^R\d+:.*?\[([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\]", s)
            if m:
                out.append([float(x) for x in m.groups()])
    return out


def claude(cwd: Path, istem: str, sure: int = 1800) -> str:
    b = json.loads((MEDS / "otomasyon" / "llm" / "butce.json").read_text())
    kom = ["claude", "-p", istem, "--permission-mode", "bypassPermissions", "--model", b["claude"].get("model", "claude-opus-5-5"),
           "--add-dir", str(cwd)]
    try:
        r = subprocess.run(kom, cwd=cwd, capture_output=True, text=True, timeout=sure,
                           env={**os.environ, "CUDA_VISIBLE_DEVICES": ""})
        return (r.stdout or "")[-300:] + (r.stderr or "")[-300:]
    except subprocess.TimeoutExpired:
        return "zaman aşımı"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("--dok", required=True); ap.add_argument("--capa", required=True)
    ap.add_argument("--isaret", required=True); ap.add_argument("--paralel", type=int, default=4)
    ap.add_argument("--parti", type=int, default=6); ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--is-dizini", default=None)
    a = ap.parse_args()
    dok = Path(a.dok)
    C = cumleler(dok / "cumleler.md")
    capa = json.loads(Path(a.capa).read_text())["p"]
    isr = json.loads(Path(a.isaret).read_text())
    hz = json.loads((KOK / "hizalama" / f"{a.key}.json").read_text())
    pdfler = sorted((KOK / ".pdf_onbellek").glob(f"{hz['deckId']}_0_*.pdf"))
    import pymupdf
    belge = pymupdf.open(pdfler[-1]) if pdfler else None

    sayfa_cumle: dict[int, list[str]] = {}
    for pi, par in enumerate(capa):
        for ci, x in enumerate(par or []):
            if x and x.get("sayfa") and f"P{pi}.C{ci}" in C:
                sayfa_cumle.setdefault(int(x["sayfa"]), []).append(f"P{pi}.C{ci}")
    sayfalar = sorted(sayfa_cumle)
    partiler = [sayfalar[i:i + a.parti] for i in range(0, len(sayfalar), a.parti)]
    W = Path(a.is_dizini or (MEDS.parent / "meds_temp" / "cizim" / a.key))
    W.mkdir(parents=True, exist_ok=True)
    print(f"{a.key}: {len(sayfalar)} anlatılan sayfa, {len(partiler)} parti, {a.paralel} eşzamanlı")

    def parti_isle(i_sp):
        i, sp = i_sp
        d = W / f"parti{i:02d}"
        d.mkdir(exist_ok=True)
        if (d / "cizim.json").exists():
            return i, "önceki"
        satir = ["# Bu partinin sayfaları", ""]
        for s in sp:
            png = dok / f"s{s:02d}.png"
            satir.append(f"## Sayfa {s} — görüntü: {png}")
            satir += [x for x in (dok / f"s{s:02d}.txt").read_text(encoding="utf-8").splitlines() if x.startswith(("R", "M"))][:30] \
                if (dok / f"s{s:02d}.txt").exists() else []
            for cid in sayfa_cumle[s]:
                ks = C[cid].split()
                satir.append(f"{cid}: " + " ".join(f"[{j}]{w}" for j, w in enumerate(ks)))
            satir.append("")
        (d / "sayfalar.md").write_text("\n".join(satir), encoding="utf-8")
        if a.kuru:
            return i, "kuru"
        t = time.time()
        r = claude(d, f"{TALIMAT} talimatını uygula. Çalışma dizinindeki sayfalar.md'yi oku; listelenen her sayfa görüntüsünü "
                      "Read ile aç ve bak; çizimleri cizim.json'a yaz.")
        return i, f"{round((time.time() - t) / 60, 1)} dk {r.strip()[-80:]}"

    with ThreadPoolExecutor(max_workers=a.paralel) as ex:
        for i, durum in ex.map(parti_isle, enumerate(partiler)):
            print(f"  parti {i}: {durum}", flush=True)
    if a.kuru:
        return 0

    # kapı
    raster: dict[int, CD.SayfaRaster] = {}
    sira = list(C)
    out: dict[str, dict[str, list]] = {}
    say = {"aday": 0, "gecti": 0, "ret": {}}
    sayfa_say: dict[int, int] = {}
    for f in sorted(W.glob("parti*/cizim.json")):
        try:
            komutlar = json.loads(f.read_text()).get("komutlar") or []
        except Exception as e:  # noqa: BLE001
            print(f"  {f.parent.name}: cizim.json okunamadı ({e})"); continue
        for k in komutlar:
            say["aday"] += 1
            cid = str(k.get("cumle") or "")
            if cid not in C:
                say["ret"]["bilinmeyen cümle"] = say["ret"].get("bilinmeyen cümle", 0) + 1; continue
            s = int(k.get("sayfa") or 0)
            if s and s not in raster and belge is not None and 1 <= s <= belge.page_count:
                raster[s] = CD.SayfaRaster(belge[s - 1])
            onceki = " ".join(C[x] for x in sira[:sira.index(cid) + 1])
            neden = CD.denetle(k, len(C[cid].split()), kutular(dok / f"s{s:02d}.txt"), raster.get(s), onceki)
            p, c = cid[1:].split(".C")
            mevcut = out.setdefault(p, {}).setdefault(c, [])
            if not neden and len(mevcut) >= 2:
                neden = "cümlede 2'den çok çizim"
            if not neden and sayfa_say.get(s, 0) >= 8:
                neden = "sayfada 8'den çok çizim"
            if neden:
                kisa = re.sub(r"\d+", "N", neden)[:60]
                say["ret"][kisa] = say["ret"].get(kisa, 0) + 1
                continue
            ka = kelime_araliklari(C[cid])
            komut = {x: k[x] for x in ("tur", "nokta", "a", "b", "iliski", "fazlar", "dugum", "kenar", "etiket") if x in k}
            komut.update(s=s, k=[ka[k["bas"]][0], ka[k["son"]][1]])
            mevcut.append(komut)
            sayfa_say[s] = sayfa_say.get(s, 0) + 1
            say["gecti"] += 1
    out = {p: {c: v for c, v in cs.items() if v} for p, cs in out.items()}
    out = {p: cs for p, cs in out.items() if cs}
    turler: dict[str, int] = {}
    for cs in out.values():
        for v in cs.values():
            for k in v:
                turler[k["tur"]] = turler.get(k["tur"], 0) + 1
    say["tur"] = turler
    hedef = KOK / "cizim" / f"{a.key}.json"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(json.dumps({"surum": 1, "metinHash": isr.get("metinHash"), "p": out, "rapor": say}, ensure_ascii=False),
                     encoding="utf-8")
    print(f"{a.key}: {say['aday']} aday → {say['gecti']} çizim {turler} · ret {say['ret']}")
    return 0 if say["gecti"] else 1


if __name__ == "__main__":
    sys.exit(main())
