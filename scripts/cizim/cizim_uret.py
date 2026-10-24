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

import numpy as np

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


def adaylar(sayfa) -> tuple[list[dict], list[dict]]:
    """Kroki (R1) adayları: vektör okları (kroki/ok.py, PDF çiziminden kesin) ve resim kutularındaki eğriler
    (kroki/egri.py egri_cikar + kapı). Koordinatlar sayfa oranı (0–1)."""
    sys.path.insert(0, str(MEDS / "scripts" / "kroki"))
    oklar_, egriler = [], []
    W, H = sayfa.rect.width, sayfa.rect.height
    try:
        import ok as OK
        for i, o in enumerate(OK.oklar(sayfa)[:12], 1):
            oklar_.append({"id": f"A{i}", "a": [round(o["kuyruk"][0] / W, 4), round(o["kuyruk"][1] / H, 4)],
                           "b": [round(o["uc"][0] / W, 4), round(o["uc"][1] / H, 4)], "iliski": o["tur"]})
    except Exception as e:  # noqa: BLE001
        print(f"  ok adayı çıkarılamadı (s. {sayfa.number + 1}): {e}")
    try:
        import cv2
        import numpy as np
        import pymupdf
        import egri as EG
        for j, im in enumerate(sayfa.get_image_info()[:4], 1):
            x0, y0, x1, y1 = im["bbox"]
            if (x1 - x0) * (y1 - y0) < 0.03 * W * H:
                continue
            pm = sayfa.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(x0, y0, x1, y1), alpha=False)
            rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3]
            e = EG.egri_cikar(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            if not EG.kapidan_gecer(e):
                continue
            sx, sy = (x1 - x0) / e["w"], (y1 - y0) / e["h"]
            n = [[round((x0 + x * sx) / W, 4), round((y0 + y * sy) / H, 4)] for x, y in zip(e["xs"], e["ys"])]
            adim = max(1, len(n) // 24)
            n = n[::adim]
            xs = [q[0] for q in n]
            fz = []
            for f in e["fazlar"]:
                a = min(range(len(xs)), key=lambda k: abs(xs[k] - (x0 + f["bas"] * sx) / W))
                b = min(range(len(xs)), key=lambda k: abs(xs[k] - (x0 + f["son"] * sx) / W))
                if a < b:
                    fz.append({"aralik": [a, b], "faz": f["faz"] if f["faz"] in ("yukselis", "inis", "plato") else "plato"})
            egriler.append({"id": f"E{len(egriler) + 1}", "nokta": n, "fazlar": fz})
    except Exception as e:  # noqa: BLE001
        print(f"  eğri adayı çıkarılamadı (s. {sayfa.number + 1}): {e}")
    return oklar_, egriler


def _bez(a, c, b, t):
    return [(1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]]


def _kesisir(a, b, pay=0.008) -> bool:
    return not (a[2] + pay <= b[0] or b[2] + pay <= a[0] or a[3] + pay <= b[1] or b[3] + pay <= a[1])


def sayfa_satirlari(sayfa) -> list[dict]:
    """Sayfadaki yazı satırları: [{"kutu": [x0,y0,x1,y1] (0–1), "metin"}] — okun uçları bunlara oturur."""
    W, H = sayfa.rect.width, sayfa.rect.height
    out = []
    for bl in sayfa.get_text("dict").get("blocks", []):
        for ln in bl.get("lines", []):
            t = "".join(sp.get("text", "") for sp in ln.get("spans", [])).strip()
            if t:
                x0, y0, x1, y1 = ln["bbox"]
                out.append({"kutu": [x0 / W, y0 / H, x1 / W, y1 / H], "metin": t})
    return out


def _kutu_bul(nokta, metin, satirlar):
    """Önce verilen kelime (slaytta geçen), yoksa noktayı içeren / en yakın (≤0,05) satır. → kutu ya da None."""
    from cizim_dogrula import _kok
    if metin:
        kk = _kok(metin)
        adaylar = [s_ for s_ in satirlar if kk and kk <= _kok(s_["metin"])] or \
                  [s_ for s_ in satirlar if kk and len(kk & _kok(s_["metin"])) >= max(1, len(kk) - 1)]
        if adaylar:
            return min(adaylar, key=lambda s_: _uzak(nokta, s_["kutu"]) if nokta else 0)["kutu"]
    if not nokta:
        return None
    en = min(satirlar, key=lambda s_: _uzak(nokta, s_["kutu"]), default=None)
    return en["kutu"] if en and _uzak(nokta, en["kutu"]) <= 0.05 else None


def _resim_kutusu(nokta, r):
    """Resim sayfasında (yazı satırı yok) noktayı içeren en küçük çizili kutu (akış şeması kutusu): ince kenar
    haritasındaki dış hatlardan, noktayı içeren, sayfanın %0,08–%15'i kadar ve dikdörtgene yakın (dolgu ≥%80) olan en
    küçüğü. → kutu ya da None."""
    if not nokta or r is None:
        return None
    import cv2
    if not hasattr(r, "_kutular"):
        kenar = cv2.Canny(r.gri, 50, 150) if hasattr(r, "gri") else (r.kenar.astype("uint8") * 255)
        kn, _ = cv2.findContours(kenar, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        r._kutular = []
        for c in kn:
            x, y, w, h = cv2.boundingRect(c)
            oran = w * h / (r.w * r.h)
            if 0.0008 <= oran <= 0.15 and cv2.contourArea(c) >= 0.8 * w * h:
                r._kutular.append((w * h, [x / r.w, y / r.h, (x + w) / r.w, (y + h) / r.h]))
        r._kutular.sort()
    for _, K in r._kutular:
        if K[0] <= nokta[0] <= K[2] and K[1] <= nokta[1] <= K[3]:
            return K
    return None


def _uzak(p, k) -> float:
    dx = max(k[0] - p[0], 0, p[0] - k[2])
    dy = max(k[1] - p[1], 0, p[1] - k[3])
    return (dx * dx + dy * dy) ** 0.5


def ok_yerlesimi(k: dict, r, satirlar: list) -> dict:
    """Akış okunun uçları gerçek yazı kutularına oturur; rota içeriğin önünü en az kapatan seçenekten: düz (yatay/dikey),
    dirsek (dikey→yatay ya da yatay→dikey, köşe yuvarlak) ya da kavis (kullanıcı 2026-10-24: "her zaman kavis gerekmez;
    okun ucu nereyi gösteriyor belli olmalı"). Hedef, halka yerine yazının kendi kutusuyla belirtilir."""
    pa, pb = k.get("a"), k.get("b")
    A = _kutu_bul(pa, k.get("kaynak_metin"), satirlar) or _resim_kutusu(pa, r) or ([pa[0], pa[1], pa[0], pa[1]] if pa else None)
    B = _kutu_bul(pb, k.get("hedef_metin"), satirlar) or _resim_kutusu(pb, r)
    hedef_yazi = B is not None
    B = B or ([pb[0], pb[1], pb[0], pb[1]] if pb else None)
    if not A or not B:
        return k
    pay = 0.006

    def yanlar(K):
        xm, ym = (K[0] + K[2]) / 2, (K[1] + K[3]) / 2
        return {"sol": [K[0] - pay, ym], "sag": [K[2] + pay, ym], "ust": [xm, K[1] - pay], "alt": [xm, K[3] + pay]}
    YA, YB = yanlar(A), yanlar(B)
    adaylar = []
    # düz: kutular x'te ya da y'de örtüşüyorsa ortak hizadan dikey/yatay tek çizgi
    ox0, ox1 = max(A[0], B[0]), min(A[2], B[2])
    if ox1 - ox0 > 0.005:
        x = (ox0 + ox1) / 2
        adaylar.append(("duz", [[x, A[3] + pay], [x, B[1] - pay]] if B[1] > A[3] else [[x, A[1] - pay], [x, B[3] + pay]]))
    oy0, oy1 = max(A[1], B[1]), min(A[3], B[3])
    if oy1 - oy0 > 0.003:
        y = (oy0 + oy1) / 2
        adaylar.append(("duz", [[A[2] + pay, y], [B[0] - pay, y]] if B[0] > A[2] else [[A[0] - pay, y], [B[2] + pay, y]]))
    # dirsek: dikey→yatay (A üst/alt → B sol/sağ) ve yatay→dikey (A sol/sağ → B üst/alt)
    for ay in ("ust", "alt"):
        for by in ("sol", "sag"):
            p0, p2 = YA[ay], YB[by]
            if (ay == "alt") == (p2[1] > p0[1]) and (by == "sol") == (p2[0] > p0[0]):
                adaylar.append(("dirsek", [p0, [p0[0], p2[1]], p2]))
    for ay in ("sol", "sag"):
        for by in ("ust", "alt"):
            p0, p2 = YA[ay], YB[by]
            if (ay == "sag") == (p2[0] > p0[0]) and (by == "ust") == (p2[1] > p0[1]):
                adaylar.append(("dirsek", [p0, [p2[0], p0[1]], p2]))
    # kavis: en yakın yanlar arasında
    p0 = min(YA.values(), key=lambda q: _uzak(q, B)); p2 = min(YB.values(), key=lambda q: _uzak(q, A))
    dx, dy = p2[0] - p0[0], p2[1] - p0[1]
    L = (dx * dx + dy * dy) ** 0.5 or 1
    for d in (0.15, -0.15, 0.3, -0.3):
        c = [p0[0] + dx / 2 - dy / L * d * L, p0[1] + dy / 2 + dx / L * d * L]
        adaylar.append(("kavis", [_bez(p0, c, p2, t / 16) for t in range(17)]))
    adaylar.append(("kavis", [p0, p2]))

    def ornek(yol):
        out = []
        for u, v in zip(yol, yol[1:]):
            n = max(2, int(((v[0] - u[0]) ** 2 + (v[1] - u[1]) ** 2) ** 0.5 / 0.004))
            out += [[u[0] + (v[0] - u[0]) * i / n, u[1] + (v[1] - u[1]) * i / n] for i in range(n)]
        return out

    def ic(q, K):
        return K[0] - 0.008 <= q[0] <= K[2] + 0.008 and K[1] - 0.008 <= q[1] <= K[3] + 0.008

    ceza = {"duz": 0.0, "dirsek": 0.015, "kavis": 0.04}
    en = None
    for tur, yol in adaylar:
        if any(not (0 <= q[0] <= 1 and 0 <= q[1] <= 1) for q in yol):
            continue
        o = [q for q in ornek(yol) if not ic(q, A) and not ic(q, B)]
        uzunluk = sum(((v[0] - u[0]) ** 2 + (v[1] - u[1]) ** 2) ** 0.5 for u, v in zip(yol, yol[1:]))
        maliyet = (r.yol_doluluk(o) if o else 0) + 0.12 * uzunluk + ceza[tur]
        if en is None or maliyet < en[0]:
            en = (maliyet, tur, yol)
    if not en:
        return k
    k = {kk: vv for kk, vv in k.items() if kk not in ("c", "hedef")}
    k.update(yol=[[round(q[0], 4), round(q[1], 4)] for q in en[2]], rota=en[1], a=en[2][0], b=en[2][-1])
    if hedef_yazi:
        k["hedef_kutu"] = [round(B[0] - 0.004, 4), round(B[1] - 0.004, 4), round(B[2] + 0.004, 4), round(B[3] + 0.004, 4)]
    return k


def yerlesim(k: dict, r, dolu: list | None = None, satirlar: list | None = None) -> dict:
    """İçeriğin önünü kapatmayan yerleşim (kullanıcı geri bildirimi 2026-10-24): akış oku düz değil, kavislerden en az
    yazı/resim üstünden geçeni; ok hedefin hemen önünde biter, hedef ince halkayla belirtilir; etiket boş bir yere
    (yoksa hiç); şema paneli sayfanın en boş köşesine. r = SayfaRaster (yoksa yerleşim yapılmaz)."""
    if r is None:
        return k
    if k["tur"] == "akis":
        k = ok_yerlesimi(k, r, satirlar or [])
    if k.get("etiket"):
        g, h = min(0.3, 0.012 * len(k["etiket"]) + 0.04), 0.034
        o = k.get("nokta", [k.get("c") or k.get("a") or [0.5, 0.5]])[0] if k["tur"] != "sema" else [0.5, 0.5]
        aday = [(o[0] + ox, o[1] + oy) for ox in (-0.02, 0.04, -0.2, 0.1, -0.3) for oy in (-0.06, 0.03, -0.12, 0.09)]
        iyi = [(r.kutu_doluluk(x - 0.012, y - 0.012, x + g + 0.012, y + h + 0.012), x, y) for x, y in aday
               if 0 <= x and x + g <= 1 and 0 <= y and y + h <= 1]
        iyi = [z for z in iyi if z[0] < 0.02 and not any(_kesisir((z[1], z[2], z[1] + g, z[2] + h), o) for o in (dolu or []))]
        if iyi:
            _, x, y = min(iyi)
            k = {**k, "etiket_konum": [round(x, 4), round(y, 4)], "etiket_genislik": round(g, 3)}
            if dolu is not None:
                dolu.append((x, y, x + g, y + h))
        elif k["tur"] == "akis" and k.get("yol"):
            # ok etiketsiz kalmasın (H40): boş yer yoksa yolun ortasına, okunur koyu hap olarak
            y = k["yol"]; m = y[len(y) // 2]
            x, yy = min(max(0.0, m[0] - g / 2), 1 - g), min(max(0.0, m[1] - h - 0.008), 1 - h)
            k = {**k, "etiket_konum": [round(x, 4), round(yy, 4)], "etiket_genislik": round(g, 3)}
            if dolu is not None:
                dolu.append((x, yy, x + g, yy + h))
        else:
            k = {**k}; k.pop("etiket", None)                               # boş yer yok: etiket gösterilmez
    if k["tur"] == "sema":
        n = len(k.get("dugum") or [])
        # gruplu şema (≥2 düğüm aynı hedefe: "}" ile toplanır, CizimLayer.Sema) dikey sütun; değilse yatay zincir
        hedefe = {}
        for e in k.get("kenar") or []:
            hedefe.setdefault(e.get("b"), set()).add(e.get("a"))
        grup = max((len(v) for v in hedefe.values()), default=0)
        boy = ([(0.42, 0.05 * grup + 0.04), (0.36, 0.05 * grup + 0.06)] if grup >= 2 else
               [(min(0.6, 0.12 * n + 0.08), 0.08), (min(0.45, 0.09 * n + 0.06), 0.12), (min(0.32, 0.07 * n + 0.05), 0.16)])
        # yazının ağırlık merkezi: panel içeriğe yakın, kenara yapışmadan (≥%3 pay) ve boş yerde durur
        ys, xs = np.nonzero(r.ince[::4, ::4])
        mx, my = (xs.mean() * 4 / r.w, ys.mean() * 4 / r.h) if len(xs) else (0.5, 0.5)
        en = None
        for g, h in boy:
            for xi in range(2, int((0.97 - g) * 50) + 1):
                for yi in range(2, int((0.97 - h) * 50) + 1):
                    x, y = xi / 50, yi / 50
                    if any(_kesisir((x, y, x + g, y + h), o) for o in (dolu or [])):
                        continue
                    dl = r.kutu_doluluk(x - 0.015, y - 0.015, x + g + 0.015, y + h + 0.015)
                    if dl >= 0.03:
                        continue
                    puan = dl * 8 + ((x + g / 2 - mx) ** 2 + (y + h / 2 - my) ** 2) ** 0.5
                    if en is None or puan < en[0]:
                        en = (puan, x, y, g, h, dl)
            if en:
                break
        if en:
            k = {**k, "konum": [round(en[1], 4), round(en[2], 4)], "genislik": round(en[3], 3), "doluluk": round(en[5], 3)}
            if dolu is not None:
                dolu.append((en[1], en[2], en[1] + en[3], en[2] + en[4]))
        else:
            k = {**k, "konum": None, "doluluk": None}   # boş yer yok: sayfa üstünde gösterilmez
    return k


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

    ADAY: dict[int, dict] = {}
    ADAY_LISTE: dict[int, tuple] = {}
    for s_ in sayfalar:                    # partilerden önce (önbellekteki parti de adayla çözülsün)
        if belge is not None and 1 <= s_ <= belge.page_count:
            ADAY_LISTE[s_] = adaylar(belge[s_ - 1])
            ADAY[s_] = {x["id"]: x for x in ADAY_LISTE[s_][0] + ADAY_LISTE[s_][1]}

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
            if s in ADAY_LISTE:
                ao, ae = ADAY_LISTE[s]
                for x in ao:
                    satir.append(f"Aday ok {x['id']} (PDF çiziminden, kesin): kuyruk {x['a']} → uç {x['b']} ({x['iliski']})")
                for x in ae:
                    satir.append(f"Aday eğri {x['id']} (görüntüden çıkarıldı, kesin): {len(x['nokta'])} nokta, fazlar "
                                 + ", ".join(f"{f['faz']} {f['aralik']}" for f in x["fazlar"]))
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
    sayfa_dolu: dict[int, list] = {}
    satir_onbellek: dict[int, list] = {}          # sayfada yerleşmiş etiket/şema kutuları (üst üste binmesin)
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
            ad = (ADAY.get(s) or {}).get(str(k.get("aday") or ""))
            if ad:                       # aday seçildi: koordinat betikle adaydan (tahmin değil, PDF/görüntü çizimi)
                k = {**k, **{x: ad[x] for x in ("a", "b", "nokta", "fazlar") if x in ad}}
                if "iliski" in ad and k.get("tur") == "akis":
                    k["iliski"] = k.get("iliski") or ad["iliski"]
            if s and s not in raster and belge is not None and 1 <= s <= belge.page_count:
                raster[s] = CD.SayfaRaster(belge[s - 1])
            onceki = " ".join(C[x] for x in sira[:sira.index(cid) + 1])
            neden = CD.denetle(k, len(C[cid].split()), kutular(dok / f"s{s:02d}.txt"), raster.get(s), onceki)
            p, c = cid[1:].split(".C")
            mevcut = out.setdefault(p, {}).setdefault(c, [])
            if not neden and k.get("tur") == "akis" and not str(k.get("etiket") or "").strip():
                neden = "etiketsiz ok (amacı anlaşılmıyor, H40)"
            if not neden and len(mevcut) >= 2:
                neden = "cümlede 2'den çok çizim"
            if not neden and sayfa_say.get(s, 0) >= 8:
                neden = "sayfada 8'den çok çizim"
            if neden:
                kisa = re.sub(r"\d+", "N", neden)[:60]
                say["ret"][kisa] = say["ret"].get(kisa, 0) + 1
                continue
            ka = kelime_araliklari(C[cid])
            komut = {x: k[x] for x in ("tur", "nokta", "a", "b", "iliski", "fazlar", "dugum", "kenar", "etiket",
                                       "kaynak_metin", "hedef_metin") if x in k}
            komut.update(s=s, k=[ka[k["bas"]][0], ka[k["son"]][1]])
            if s not in satir_onbellek and belge is not None and 1 <= s <= belge.page_count:
                satir_onbellek[s] = sayfa_satirlari(belge[s - 1])
            mevcut.append(yerlesim(komut, raster.get(s), sayfa_dolu.setdefault(s, []), satir_onbellek.get(s)))
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
