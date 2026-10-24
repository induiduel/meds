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


def _satir_bul(nokta, metin, satirlar):
    """Önce verilen kelime (slaytta geçen), yoksa noktayı içeren / en yakın (≤0,05) satır. → satır ({kutu, metin}) ya da None."""
    from cizim_dogrula import _kok
    if metin:
        kk = _kok(metin)
        adaylar = [s_ for s_ in satirlar if kk and kk <= _kok(s_["metin"])] or \
                  [s_ for s_ in satirlar if kk and len(kk & _kok(s_["metin"])) >= max(1, len(kk) - 1)]
        if adaylar:
            return min(adaylar, key=lambda s_: _uzak(nokta, s_["kutu"]) if nokta else 0)
    if not nokta:
        return None
    en = min(satirlar, key=lambda s_: _uzak(nokta, s_["kutu"]), default=None)
    return en if en and _uzak(nokta, en["kutu"]) <= 0.05 else None


def _kutu_bul(nokta, metin, satirlar):
    sa = _satir_bul(nokta, metin, satirlar)
    return sa["kutu"] if sa else None


MASKE = re.compile(r"maskel|gizle|altta|görünse|örter|sakla", re.I)


def _dugum_metni(t: str) -> str:
    t = re.sub(r"[\ue000-\uf8ff]", "", t)                       # PDF simge yazı tipi madde imleri ()
    yalin = re.sub(r"\([^)]*\)|^[^(]*\)", "", t).strip()            # parantezli ara söz düğüme girmez
    if len(yalin) >= 3:
        t = yalin
    t = re.sub(r"^[\s\-–•■▪●◦*()]+|[\s?!.:;,()]+$", "", t).strip()
    if len(t) > 42:
        t = t[:42].rsplit(" ", 1)[0] + "…"
    return t


def panel_tipi(k: dict) -> str:
    """Şema panelinin türü ilişki yapısından (kullanıcı 2026-10-24: "birden çok senaryo için birden çok panel türü"):
    karsit (iki kutup yan yana) · maske (görünen neden altta yatanı örter; perde kalkar) · grup (çok → bir, "}") ·
    dal (bir → çok, karar dalları) · zincir (A → B → C)."""
    kn = k.get("kenar") or []
    if any(e.get("tur") == "karsit" for e in kn):
        return "karsit"
    if any(e.get("tur") == "maske" for e in kn):
        return "maske"
    gir, cik = {}, {}
    for e in kn:
        gir[e.get("b")] = gir.get(e.get("b"), 0) + 1
        cik[e.get("a")] = cik.get(e.get("a"), 0) + 1
    if max(gir.values(), default=0) >= 2:
        return "grup"
    if max(cik.values(), default=0) >= 2:
        return "dal"
    return "zincir"


EM = 0.022           # panel yazı boyu = sayfa genişliğinin %2,2si (pdfDoc.css .pdv-cz-sema 2.2cqw)


def _bilesenler(k: dict) -> list[tuple[list, list]]:
    """Bağlı bileşenler (CizimLayer.Sema ile aynı): [(düğümler, kenarlar)]."""
    dg, kn = k.get("dugum") or [], k.get("kenar") or []
    kok = {d.get("id"): d.get("id") for d in dg}

    def bul(x):
        while kok.get(x, x) != x:
            x = kok[x]
        return x
    for e in kn:
        if e.get("a") in kok and e.get("b") in kok:
            kok[bul(e["a"])] = bul(e["b"])
    out: dict = {}
    for d in dg:
        out.setdefault(bul(d.get("id")), ([], []))[0].append(d)
    for e in kn:
        if e.get("a") in kok:
            out[bul(e["a"])][1].append(e)
    return list(out.values())


def yazi_kesisir(kutu, satirlar, pay: float = 0.01) -> bool:
    """Panel kutusu PDF yazı satırının kutusuna (ascent/descent dahil) pay kadar yaklaşıyor mu? Mürekkep eşiği harf
    gövdesini görür ama satır kutusunu görmez; panel satırın hemen altına yapışıp yazıya değiyor gibi duruyordu."""
    x0, y0, x1, y1 = kutu
    for s_ in satirlar or []:
        a = s_["kutu"]
        if not (x1 + pay <= a[0] or a[2] + pay <= x0 or y1 + pay <= a[1] or a[3] + pay <= y0):
            return True
    return False


def panel_boyu(k: dict, g: float, oran: float) -> float:
    """Panelin sayfa yüksekliği oranı cinsinden yüksekliği; istemcideki dizilimin em ile kopyası (oran = genişlik/yükseklik).
    Ölçüm: tarayıcıda 567 ve 1100 px sayfada gerçek yükseklikle karşılaştırıldı."""
    W = g / EM                                   # panel iç genişliği (em)
    dar = g < 0.32
    gw = lambda t: len(t) * 0.58 + 1.4          # düğüm genişliği (em)
    DH = 1.85                                    # düğüm yüksekliği + satır payı (em)
    toplam = 1.6                                 # panel iç boşluğu
    parcalar = _bilesenler(k)
    for j, (dg, kn) in enumerate(parcalar):
        tip = panel_tipi({"kenar": kn})
        if j:
            toplam += 1.0                        # ayraç + parça boşluğu
        if tip in ("grup", "dal"):
            anahtar = "b" if tip == "grup" else "a"
            say: dict = {}
            for e in kn:
                say[e.get(anahtar)] = say.get(e.get(anahtar), 0) + 1
            merkez_id = max(say, key=say.get) if say else None
            merkez = next((d for d in dg if d.get("id") == merkez_id), None)
            uclar = [d for d in dg if d is not merkez]
            mw = min(gw(merkez["metin"]) if merkez else 0, W * 0.4)
            kosul = max([len(e.get("etiket") or "") * 0.45 for e in kn] + [0]) if tip == "dal" else 0
            sutun = max(4.0, W - 1.8 - mw - (3.8 if tip == "grup" else 1.4) - kosul)     # uçların sütun genişliği
            for d in uclar:
                satir = max(1, -(-gw(d["metin"]) // sutun))
                toplam += satir * 1.3 + 0.65 + (0.5 if tip == "dal" else 0.3)
            if merkez and gw(merkez["metin"]) > W * 0.4:
                toplam = max(toplam, 1.6 + (-(-gw(merkez["metin"]) // (W * 0.4))) * 1.3 + 0.65)
        elif tip == "maske":
            toplam += 2 * 1.2 + 2 * DH + 0.6 + (2.2 if dar else 0)
        elif tip == "karsit":
            toplam += DH if not dar else 3 * DH
        else:                                     # zincir
            if dar:
                toplam += len(dg) * DH + max(0, len(dg) - 1) * 1.6 + sum(1.3 for e in kn if e.get("etiket"))
            else:
                satir, x = 1, 0.0
                for i, d in enumerate(dg):
                    gelen = next((e for e in kn if e.get("b") == d.get("id")), None)
                    bag = max(2.6, len((gelen or {}).get("etiket") or "") * 0.46 + 1.0)   # etiket okun üstünde, ok onun eni kadar
                    w = gw(d["metin"]) + (0 if i == 0 else bag)
                    if x and x + w > W:
                        satir += 1; x = 0.0
                    x += w
                toplam += satir * DH + (satir * 1.2 if any(e.get("etiket") for e in kn) else 0) + (satir - 1) * 0.4
    return toplam * EM * oran * 1.25            # %25 pay: 366–1100 px sayfada ölçülen en büyük sapma %11


def oku_panele(k: dict, satirlar: list) -> dict | None:
    """Yazı slaytında iki satır arasındaki ok okunmuyor ve amacı anlaşılmıyor (H40, kullanıcı 2026-10-24 s.18): iki ucu da
    yazı satırına düşen ok, sayfanın boşluğunda ilişkiyi kendi içinde canlandıran panele çevrilir. Ok yalnız resim/şema
    üstünde kalır. Düğümler etiketteki "A → B"den, yoksa slayttaki iki satırdan; etiket kenarın açıklaması olur."""
    sa = _satir_bul(k.get("a"), k.get("kaynak_metin"), satirlar)
    sb = _satir_bul(k.get("b"), k.get("hedef_metin"), satirlar)
    if not sa or not sb:
        return None
    et = str(k.get("etiket") or "").strip()
    parca = [x.strip() for x in re.split(r"\s*(?:→|->|⇒)\s*", et) if x.strip()]
    if len(parca) >= 2 and len(parca) <= 4:
        dugum = [{"id": f"d{i}", "metin": _dugum_metni(x)} for i, x in enumerate(parca)]
        kenar = [{"a": f"d{i}", "b": f"d{i + 1}", "tur": k.get("iliski") or "aktive"} for i in range(len(parca) - 1)]
    else:
        ma, mb = _dugum_metni(sa["metin"]), _dugum_metni(sb["metin"])
        # akış şeması kutularındaki tek-iki kelimelik parçalar ("hasta", "evet") düğüm olmaz: ok şemada kalır
        if not ma or not mb or ma == mb or min(len(ma.split()), len(mb.split())) < 3:
            return None
        dugum = [{"id": "d0", "metin": ma}, {"id": "d1", "metin": mb}]
        kenar = [{"a": "d0", "b": "d1", "tur": "maske" if MASKE.search(et) else (k.get("iliski") or "aktive"),
                  **({"etiket": et} if et else {})}]
    return {"tur": "sema", "s": k["s"], "k": k["k"], "dugum": dugum, "kenar": kenar, "kaynak": "ok"}


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
    # resimdeki mevcut oku kopyalayan kısa ok (yol şeklin kendi çizgileri üstünde): yeni ok çizilmez, şekildeki ok
    # çerçevelenip etiketlenir (kullanıcı 2026-10-24 s.14: ok amacı anlaşılmıyordu)
    if not hedef_yazi and (pa and pb) and ((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2) ** 0.5 < 0.14 \
            and r.kenar_orani([pa, [(pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2], pb]) >= 0.6:
        x0, x1 = sorted((pa[0], pb[0])); y0, y1 = sorted((pa[1], pb[1]))
        k["odak"] = [round(max(0, x0 - 0.02), 4), round(max(0, y0 - 0.02), 4), round(min(1, x1 + 0.02), 4), round(min(1, y1 + 0.02), 4)]
        return k
    k.update(yol=[[round(q[0], 4), round(q[1], 4)] for q in en[2]], rota=en[1], a=en[2][0], b=en[2][-1])
    if A[2] - A[0] > 0.01:
        k["kaynak_kutu"] = [round(A[0] - 0.004, 4), round(A[1] - 0.004, 4), round(A[2] + 0.004, 4), round(A[3] + 0.004, 4)]
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
        k = oku_panele(k, satirlar or []) or ok_yerlesimi(k, r, satirlar or [])
    if k["tur"] == "sema":
        k = {**k, "tip": panel_tipi(k)}
    if k.get("etiket"):
        # etiket yazısı sayfa genişliğinin %2,3ü (pdfDoc.css .pdv-cz-etiket 2.3cqw); karakter ≈0,58 em, satır 1,3 em + pay
        oran_e = r.w / r.h
        gerek = 0.023 * (0.58 * len(k["etiket"]) + 1.2)
        satir = max(1, -(-gerek // 0.42))                   # uzun etiket kırpılmaz, satıra iner (H48)
        g, h = min(0.42, gerek), 0.023 * (1.3 * satir + 0.45) * oran_e
        o = k.get("nokta", [k.get("c") or k.get("a") or [0.5, 0.5]])[0] if k["tur"] != "sema" else [0.5, 0.5]
        if k.get("odak"):
            o = [k["odak"][2], k["odak"][1]]
        elif k["tur"] == "kontur" and k.get("nokta"):
            o = [max(n[0] for n in k["nokta"]) + 0.01, min(n[1] for n in k["nokta"])]   # bölgenin sağ üstü
        aday = [(o[0] + ox, o[1] + oy) for ox in (0.0, -0.02, 0.04, -0.1, -0.2, 0.1, -0.3) for oy in (-0.04, 0.0, -0.06, 0.03, -0.12, 0.09)]
        iyi = [(r.kutu_doluluk(x - 0.012, y - 0.012, x + g + 0.012, y + h + 0.012), x, y) for x, y in aday
               if 0 <= x and x + g <= 1 and 0 <= y and y + h <= 1]
        uygun = lambda z: z[0] < 0.02 and not any(_kesisir((z[1], z[2], z[1] + g, z[2] + h), o) for o in (dolu or [])) \
            and not yazi_kesisir((z[1], z[2], z[1] + g, z[2] + h), satirlar, 0.004)
        iyi = [z for z in iyi if uygun(z)]
        if not iyi:
            # yakında boş yer yoksa: yine yakında, yazı satırına değmeyen ama resmin küçük bir kısmını (≤%25) örtebilen yer
            # (etiket anlattığı okun yanında kalsın; koyu hap resmin üstünde okunur)
            iyi = [z for z in [(r.kutu_doluluk(x - 0.006, y - 0.006, x + g + 0.006, y + h + 0.006), x, y) for x, y in aday
                               if 0 <= x and x + g <= 1 and 0 <= y and y + h <= 1]
                   if z[0] < 0.25 and not any(_kesisir((z[1], z[2], z[1] + g, z[2] + h), o) for o in (dolu or []))
                   and not yazi_kesisir((z[1], z[2], z[1] + g, z[2] + h), satirlar, 0.004)]
        if not iyi:
            # o da yoksa bütün sayfada (%2 adım) boş yer; en yakını seçilir — yazının üstüne konmaz (H48)
            tum = [(r.kutu_doluluk(xi / 50 - 0.012, yi / 50 - 0.012, xi / 50 + g + 0.012, yi / 50 + h + 0.012), xi / 50, yi / 50)
                   for xi in range(0, int((1 - g) * 50) + 1) for yi in range(0, int((1 - h) * 50) + 1)]
            iyi = [z for z in tum if uygun(z) and ((z[1] - o[0]) ** 2 + (z[2] - o[1]) ** 2) ** 0.5 < 0.35]
        if iyi:
            # boş adaylardan bölgeye en yakını (etiket anlattığı yerin yanında dursun)
            _, x, y = min(iyi, key=lambda z: (z[1] - o[0]) ** 2 + (z[2] - o[1]) ** 2)
            k = {**k, "etiket_konum": [round(x, 4), round(y, 4)], "etiket_genislik": round(g, 3)}
            if dolu is not None:
                dolu.append((x, y, x + g, y + h))
        elif k["tur"] == "akis" and k.get("odak"):
            x, yy = min(max(0.0, k["odak"][0]), 1 - g), max(0.0, k["odak"][1] - h - 0.006)
            k = {**k, "etiket_konum": [round(x, 4), round(yy, 4)], "etiket_genislik": round(g, 3)}
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
        # yükseklik bağlı bileşenlerden (istemci her bileşeni ayrı satırda çizer): bileşen başına satır = en büyük
        # dallanma/toplanma (en az 1), artı satır payı
        kok = {d.get("id"): d.get("id") for d in k.get("dugum") or []}

        def bul(x):
            while kok.get(x, x) != x:
                x = kok[x]
            return x
        for e in k.get("kenar") or []:
            if e.get("a") in kok and e.get("b") in kok:
                kok[bul(e["a"])] = bul(e["b"])
        bilesen: dict = {}
        for d in kok:
            bilesen.setdefault(bul(d), []).append(d)
        satir = 0
        for ids in bilesen.values():
            gir, cik = {}, {}
            for e in k.get("kenar") or []:
                if e.get("a") in ids:
                    gir[e["b"]] = gir.get(e["b"], 0) + 1; cik[e["a"]] = cik.get(e["a"], 0) + 1
            satir += max([1] + list(gir.values()) + list(cik.values())) + (1 if len(ids) > 3 and max([0] + list(gir.values()) + list(cik.values())) < 2 else 0)
        grup = satir
        if k["tip"] in ("maske", "karsit"):
            grup = max(grup, 3)
        oran = r.w / r.h
        boy = [(g, panel_boyu(k, g, oran)) for g in (0.5, 0.42, 0.6, 0.34, 0.3)]
        # yazının ağırlık merkezi: panel içeriğe yakın, kenara yapışmadan (≥%3 pay) ve boş yerde durur
        ys, xs = np.nonzero(r.ince[::4, ::4])
        mx, my = (xs.mean() * 4 / r.w, ys.mean() * 4 / r.h) if len(xs) else (0.5, 0.5)
        # panel anlattığı satırların yanına: düğüm terimlerinin geçtiği satırların merkezi (yoksa yazının ağırlık merkezi)
        from cizim_dogrula import _kok
        kk = _kok(" ".join(d.get("metin", "") for d in k.get("dugum") or []))
        ilgili = [s_["kutu"] for s_ in (satirlar or []) if kk & _kok(s_["metin"])]
        if ilgili:
            mx = sum((b[0] + b[2]) / 2 for b in ilgili) / len(ilgili)
            my = sum((b[1] + b[3]) / 2 for b in ilgili) / len(ilgili)
        en = None
        for g, h in boy:
            for xi in range(1, int((0.99 - g) * 100) + 1):     # %1 adım, kenardan %1 pay
                for yi in range(1, int((0.99 - h) * 100) + 1):
                    x, y = xi / 100, yi / 100
                    if any(_kesisir((x, y, x + g, y + h), o) for o in (dolu or [])):
                        continue
                    dl = r.kutu_doluluk(x - 0.012, y - 0.012, x + g + 0.012, y + h + 0.012)
                    if dl >= 0.01:            # yazının kenarına bile binmesin (H46)
                        continue
                    if yazi_kesisir((x, y, x + g, y + h), satirlar):   # PDF yazı satırı kutusuna da değmesin (H48)
                        continue
                    puan = dl * 8 + ((x + g / 2 - mx) ** 2 + (y + h / 2 - my) ** 2) ** 0.5
                    if en is None or puan < en[0]:
                        en = (puan, x, y, g, h, dl)
            if en:
                break
        if en:
            k = {**k, "konum": [round(en[1], 4), round(en[2], 4)], "genislik": round(en[3], 3), "doluluk": round(en[5], 3),
                 "kutu_h": round(en[4], 3)}
            if dolu is not None:
                dolu.append((en[1], en[2], en[1] + en[3], en[2] + en[4]))
        else:
            # boş yer yok (genel kural 14, kullanıcı 2026-10-24): panel sayfanın ALTINA eklenen alana konur; görüntüleyici
            # o sayfayı ek_alt kadar uzatır, alanı sayfanın alt kenar rengiyle boyar (slaytın kendisi gibi görünür).
            # Koordinatlar sayfa oranı olarak kalır (y > 1), işaret/vurgu/imleç katmanları etkilenmez.
            # Ek alan yalnız gerektiği kadar (kullanıcı 2026-10-24): panel önce slaytın alttaki boşluğuna oturur, yalnız
            # sığmayan kısmı için sayfa uzatılır. Aday: genişlik × x × başlangıç y; slayt içindeki parçada mürekkep < %1.
            # Seçim: en az ek alan, sonra anlatılan satırlara yakınlık.
            en2 = None
            for g in (0.9, 0.7, 0.5):
                h = panel_boyu(k, g, oran)
                for x in sorted({0.05, round(min(max(0.03, mx - g / 2), 0.97 - g), 2)}):
                    for yi in range(30, 101):
                        y = yi / 100
                        if y < 1.0:
                            ic_alt = min(1.0, y + h)
                            if r.kutu_doluluk(x - 0.012, y - 0.012, x + g + 0.012, min(1.0, ic_alt + 0.012)) >= 0.01:
                                continue
                            if yazi_kesisir((x, y, x + g, ic_alt), satirlar):
                                continue
                        ek = max(0.0, y + h + 0.02 - 1.0)
                        puan = ek * 10 + abs(y - my) * 0.5
                        if en2 is None or puan < en2[0]:
                            en2 = (puan, x, y, g, h, ek)
            _, x, y, g, h, ek = en2
            y = max(y, 1.015) if ek and y > 0.985 else y
            k = {**k, "konum": [round(x, 4), round(y, 4)], "genislik": round(g, 3), "doluluk": 0.0, "kutu_h": round(h, 3)}
            if ek > 0:
                k.update(ek_alt=round(max(ek, y + h + 0.02 - 1.0), 4), ek_renk=r.alt_renk)
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
        # dallı ok (kullanıcı 2026-10-24: resimde bir kaynaktan birden çok yere dallanan ilişki): "dallar" listesi her dal
        # için ayrı akış komutuna açılır, aynı "dal" grubuyla; istemci kaynağı bir kez çerçeveler, dalları sırayla çizer
        acik = []
        for k in komutlar:
            if k.get("tur") == "akis" and isinstance(k.get("dallar"), list) and k["dallar"]:
                n = min(4, len(k["dallar"])); g = f"{k.get('cumle')}-{len(acik)}"
                for i, dl in enumerate(k["dallar"][:4]):
                    acik.append({**{x: v for x, v in k.items() if x != "dallar"}, **dl, "dal": {"g": g, "i": i, "n": n}})
            else:
                acik.append(k)
        for k in acik:
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
            if not neden and len({(m.get("dal") or {}).get("g") or id(m) for m in mevcut}
                                 - ({(k.get("dal") or {}).get("g")} if k.get("dal") else set())) >= 2:
                neden = "cümlede 2'den çok çizim"
            if not neden and sayfa_say.get(s, 0) >= 8:
                neden = "sayfada 8'den çok çizim"
            if neden:
                kisa = re.sub(r"\d+", "N", neden)[:60]
                say["ret"][kisa] = say["ret"].get(kisa, 0) + 1
                continue
            # eş zamanlılık (genel kural 9): çizim, etiketteki / hedefteki terim konuşulurken başlar. Aralık o terimin
            # cümledeki ilk geçtiği kelimeye kaydırılır; terim cümlede hiç geçmiyorsa yazarın aralığı kalır.
            terim = " ".join(str(k.get(x) or "") for x in ("hedef_metin", "etiket", "kaynak_metin"))
            if k.get("tur") == "sema":
                terim = " ".join(d.get("metin", "") for d in k.get("dugum") or [])
            kk = CD._kok(terim)
            kel = C[cid].split()
            ilk = next((i for i, w in enumerate(kel) if CD._kok(w) & kk), None)
            if ilk is not None and not (k["bas"] <= ilk <= k["son"]):
                uz = max(2, min(8, k["son"] - k["bas"]))
                k = {**k, "bas": ilk, "son": min(len(kel) - 1, ilk + uz)}
                say["kaydirildi"] = say.get("kaydirildi", 0) + 1
            ka = kelime_araliklari(C[cid])
            komut = {x: k[x] for x in ("tur", "nokta", "a", "b", "iliski", "fazlar", "dugum", "kenar", "etiket",
                                       "kaynak_metin", "hedef_metin", "dal") if x in k}
            komut.update(s=s, k=[ka[k["bas"]][0], ka[k["son"]][1]])
            if s not in satir_onbellek and belge is not None and 1 <= s <= belge.page_count:
                satir_onbellek[s] = sayfa_satirlari(belge[s - 1])
            mevcut.append(yerlesim(komut, raster.get(s), sayfa_dolu.setdefault(s, []), satir_onbellek.get(s)))
            sayfa_say[s] = sayfa_say.get(s, 0) + 1
            say["gecti"] += 1
    # aynı cümlede aynı kaynak kutusundan çıkan oklar dallı ok olur (kaynak bir kez, dallar sırayla)
    for cs in out.values():
        for c, v in cs.items():
            gruplar: dict = {}
            for m in v:
                if m["tur"] == "akis" and m.get("kaynak_kutu") and not m.get("dal"):
                    gruplar.setdefault(tuple(m["kaynak_kutu"]), []).append(m)
            for j, ms in enumerate(x for x in gruplar.values() if len(x) >= 2):
                for i, m in enumerate(ms):
                    m["dal"] = {"g": f"{c}-o{j}", "i": i, "n": len(ms)}
        # dallı ok sayfada ortak gövdeden çıkar: bütün dallar ilk dalın çıkış noktasından başlar (genel kural 10)
        for c, v in cs.items():
            ilk_cikis: dict = {}
            for m in v:
                if m.get("dal") and m.get("yol"):
                    g = m["dal"]["g"]
                    if g not in ilk_cikis:
                        ilk_cikis[g] = m["yol"][0]
                    elif m["yol"][0] != ilk_cikis[g]:
                        m["yol"] = [ilk_cikis[g]] + m["yol"]; m["rota"] = "kavis"; m["a"] = ilk_cikis[g]
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
