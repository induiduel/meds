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
import sys as _llm_sys, pathlib as _llm_pl; _llm_sys.path[:0] = [str(p / "otomasyon") for p in _llm_pl.Path(__file__).resolve().parents]; from llm_kilit import kilit as _llm_kilit  # noqa: E402  LLM kilidi 2026-10-27
if __name__ == "__main__":
    _llm_kilit("cizim_uret")

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
import sablon as SB  # noqa: E402  (panel şablon kütüphanesi)
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


def yakinlasma(k: dict, kutu_listesi: list, resim: bool) -> list | None:
    """Resim üstündeki çizim için yakınlaşma bölgesi (kullanıcı 2026-10-24: "çizim asıl mevzunun önünü kapatıyor; o bölgeye
    zoom yapılsın, çizilsin, geri dönülsün"). Çizimin (boyalı bölge / ok yolu / odak çerçevesi + etiket) sınır kutusu,
    %6 pay; resim sayfasında ya da bir resim kutusunun içindeyse ve bölge sayfanın %40'ından küçükse. → [x0,y0,x1,y1] | None"""
    if k.get("tur") not in ("kontur", "akis", "egri_faz"):
        return None
    pts = list(k.get("nokta") or []) + list(k.get("yol") or [])
    if k.get("odak"):
        pts += [k["odak"][:2], k["odak"][2:]]
    if k.get("hedef_kutu"):
        pts += [k["hedef_kutu"][:2], k["hedef_kutu"][2:]]
    if not pts:
        return None
    x0, y0 = min(p_[0] for p_ in pts), min(p_[1] for p_ in pts)
    x1, y1 = max(p_[0] for p_ in pts), max(p_[1] for p_ in pts)
    if k.get("etiket_konum"):
        ex, ey = k["etiket_konum"]
        x0, y0 = min(x0, ex), min(y0, ey)
        x1, y1 = max(x1, ex + (k.get("etiket_genislik") or 0.2)), max(y1, ey + (k.get("etiket_boy") or 0.04))
    icinde = any(b[0] - 0.02 <= x0 and x1 <= b[2] + 0.02 and b[1] - 0.02 <= y0 and y1 <= b[3] + 0.02 for b in kutu_listesi or [])
    if not (resim or icinde):
        return None
    x0, y0, x1, y1 = max(0, x0 - 0.06), max(0, y0 - 0.06), min(1, x1 + 0.06), min(1, y1 + 0.06)
    if (x1 - x0) * (y1 - y0) > 0.4:
        return None
    return [round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4)]


def resim_sayfasi(kutu_listesi: list, satirlar: list, r) -> bool:
    """Slaytın anlatılan içeriği bir görsel mi (şema/resim)? Öyleyse ilişki görselin ÜSTÜNDE (ok, boyama, odak) anlatılır,
    yan panel kurulmaz (kullanıcı 2026-10-24, H51: herniasyon şeması anlatılırken altta metin paneli çıkıyordu).
    Ölçüt: sayfanın ≥%35'ini kaplayan resim kutusu, ya da PDF'te ≤4 yazı satırı varken sayfanın ≥%30'u mürekkepli
    (tek parça taranmış görüntü: resim kutusu algılanamaz)."""
    if any((b[2] - b[0]) * (b[3] - b[1]) >= 0.35 for b in kutu_listesi or []):
        return True
    if r is not None and len(satirlar or []) <= 4 and r.kutu_doluluk(0.05, 0.05, 0.95, 0.95) >= 0.30:
        return True
    return False


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


EM = 0.0175          # panel yazı boyu = sayfa genişliğinin %1,75'i (pdfDoc.css .pdv-cz-sema 1.75cqw; kullanıcı: 2,2 fazla büyük)
# Panel tasarım sürümleri (kullanıcı 2026-10-24: "en uygun biçimde yer alabilmesi için farklı tasarım versiyonları"):
# öncelik sırasıyla denenir; slayta (ek alansız) sığan ilk sürüm seçilir. yon: yatay | dikey (zincir alt alta, oklar
# aşağı); olcek: 1 normal | 0,85 kompakt. Yatay zincir tek satıra sığmıyorsa o sürüm geçersizdir (kırılan zincirde
# yana bakan ok yanlış okunuyordu) → dikey.
PAY_EK = float(os.environ.get("CIZIM_PAY", "1"))   # sınama düşerse ders zinciri daha geniş payla yeniden yerleştirir
SURUMLER = (("yatay", 1.0), ("dikey", 1.0), ("yatay", 0.85), ("dikey", 0.85))


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


def panel_boyu(k: dict, g: float, oran: float, yon: str = "yatay", olcek: float = 1.0) -> float:
    olcek = 1.0       # kompakt sürüm telefonda en küçük yazı sınırı (7,5 px) yüzünden küçülemiyor: boy tam ölçekle tahmin edilir
    if k.get("duzen"):                            # şablonlu panel (sablon.py)
        return SB.boyu(k, g, oran, EM, yon, olcek) * PAY_EK
    """Panelin sayfa yüksekliği oranı cinsinden yüksekliği; istemcideki dizilimin em ile kopyası (oran = genişlik/yükseklik).
    Ölçüm: tarayıcıda 567 ve 1100 px sayfada gerçek yükseklikle karşılaştırıldı."""
    W = g / (EM * olcek)                         # panel iç genişliği (em)
    dar = g < 0.32 or yon == "dikey"
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
                if satir > 1:
                    return 9.0                    # yatay zincir kırılıyor: bu sürüm geçersiz (dikey denenecek)
                toplam += satir * DH + (satir * 1.2 if any(e.get("etiket") for e in kn) else 0) + (satir - 1) * 0.4
    return toplam * EM * olcek * oran * 1.32 * PAY_EK            # %32 pay: telefonda en küçük yazı 7,5 px (dar sayfada %1,75 cqw'den büyük)


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
    if k.get("pdf_oku"):
        return {**{x: v for x, v in k.items() if x != "pdf_oku"}, "odak": k["pdf_oku"]}
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
        k = {**k, "tip": k.get("duzen") or panel_tipi(k)}
    if k.get("etiket"):
        # etiket yazısı sayfa genişliğinin %2,3ü (pdfDoc.css .pdv-cz-etiket 2.3cqw); karakter ≈0,58 em, satır 1,3 em + pay
        oran_e = r.w / r.h
        gerek = 0.019 * (0.58 * len(k["etiket"]) + 1.2)
        satir = max(1, -(-gerek // 0.42))                   # uzun etiket kırpılmaz, satıra iner (H48)
        g, h = min(0.42, gerek * 1.15 + 0.01), 0.019 * (1.3 * satir + 0.45) * oran_e   # %15 + kenar payı: dar ekranda satıra inmesin
        o = k.get("nokta", [k.get("c") or k.get("a") or [0.5, 0.5]])[0] if k["tur"] != "sema" else [0.5, 0.5]
        if k.get("odak"):
            o = [k["odak"][2], k["odak"][1]]
        elif k["tur"] == "kontur" and k.get("nokta"):
            o = [max(n[0] for n in k["nokta"]) + 0.01, min(n[1] for n in k["nokta"])]   # bölgenin sağ üstü
        # etiketin bağlı olduğu hedef kutu: odak çerçevesi, boyanan bölgenin sınırı ya da okun ucu (H52: etiketler çizimden
        # kopuk duruyordu). Adaylar önce kutunun hemen sağı/solu/üstü/altı; seçim etiketle kutu arasındaki boşluğa göre.
        if k.get("odak"):
            T = k["odak"]
        elif k["tur"] == "kontur" and k.get("nokta"):
            T = [min(n[0] for n in k["nokta"]), min(n[1] for n in k["nokta"]), max(n[0] for n in k["nokta"]), max(n[1] for n in k["nokta"])]
        elif k["tur"] == "akis" and (k.get("hedef_kutu") or k.get("b")):
            T = k.get("hedef_kutu") or [k["b"][0] - 0.01, k["b"][1] - 0.01, k["b"][0] + 0.01, k["b"][1] + 0.01]
        else:
            T = [o[0], o[1], o[0], o[1]]
        bos = 0.012
        aday = []
        for f in (0.0, 0.5, 1.0):
            yy = T[1] + f * max(0.0, (T[3] - T[1]) - h)
            aday += [(T[2] + bos, yy), (T[0] - g - bos, yy)]
            xx = T[0] + f * max(0.0, (T[2] - T[0]) - g)
            aday += [(xx, T[1] - h - bos), (xx, T[3] + bos)]
        aday += [(o[0] + ox, o[1] + oy) for ox in (0.0, -0.02, 0.04, -0.1, -0.2, 0.1, -0.3) for oy in (-0.04, 0.0, -0.06, 0.03, -0.12, 0.09)]
        aralik = lambda x, y: (max(T[0] - (x + g), 0, x - T[2]) ** 2 + max(T[1] - (y + h), 0, y - T[3]) ** 2) ** 0.5
        iyi = [(r.kutu_doluluk(x - 0.012, y - 0.012, x + g + 0.012, y + h + 0.012), x, y) for x, y in aday
               if 0 <= x and x + g <= 1 and 0 <= y and y + h * 1.5 <= 1]
        uygun = lambda z: z[0] < 0.02 and not any(_kesisir((z[1], z[2], z[1] + g, z[2] + h), o) for o in (dolu or [])) \
            and not yazi_kesisir((z[1], z[2], z[1] + g, z[2] + h), satirlar, 0.004)
        iyi = [z for z in iyi if uygun(z)]
        if not iyi:
            # yakında boş yer yoksa: yine yakında, yazı satırına değmeyen ama resmin küçük bir kısmını (≤%25) örtebilen yer
            # (etiket anlattığı okun yanında kalsın; koyu hap resmin üstünde okunur)
            iyi = [z for z in [(r.kutu_doluluk(x - 0.006, y - 0.006, x + g + 0.006, y + h + 0.006), x, y) for x, y in aday
                               if 0 <= x and x + g <= 1 and 0 <= y and y + h * 1.5 <= 1]
                   if z[0] < 0.25 and not any(_kesisir((z[1], z[2], z[1] + g, z[2] + h), o) for o in (dolu or []))
                   and not yazi_kesisir((z[1], z[2], z[1] + g, z[2] + h), satirlar, 0.004)]
        if not iyi:
            # o da yoksa bütün sayfada (%2 adım) boş yer; en yakını seçilir — yazının üstüne konmaz (H48)
            tum = [(r.kutu_doluluk(xi / 50 - 0.012, yi / 50 - 0.012, xi / 50 + g + 0.012, yi / 50 + h + 0.012), xi / 50, yi / 50)
                   for xi in range(0, int((1 - g) * 50) + 1) for yi in range(0, int((1 - h * 1.5) * 50) + 1)]
            iyi = [z for z in tum if uygun(z) and aralik(z[1], z[2]) < 0.3]
        if iyi:
            # boş adaylardan hedef kutuya en yakını; kutuya değmiyorsa ince bağlantı çizgisi (etiket_hedef) çizilir
            _, x, y = min(iyi, key=lambda z: aralik(z[1], z[2]))
            k = {**k, "etiket_konum": [round(x, 4), round(y, 4)], "etiket_genislik": round(g, 3)}
            if aralik(x, y) > 0.02:
                cx, cy = x + g / 2, y + h / 2
                k["etiket_hedef"] = [round(min(max(cx, T[0]), T[2]), 4), round(min(max(cy, T[1]), T[3]), 4)]
                k["etiket_boy"] = round(h, 4)
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
        boy = [(g, panel_boyu(k, g, oran, yon, olcek), yon, olcek) for yon, olcek in SURUMLER
               for g in ((0.5, 0.42, 0.6, 0.34, 0.3) if yon == "yatay" else (0.34, 0.42, 0.3, 0.5))]
        boy = [b for b in boy if b[1] < 0.98]
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
        for g, h, yon, olcek in boy:
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
                        en = (puan, x, y, g, h, dl, yon, olcek)
            if en:
                break
        if en:
            k = {**k, "konum": [round(en[1], 4), round(en[2], 4)], "genislik": round(en[3], 3), "doluluk": round(en[5], 3),
                 "kutu_h": round(en[4], 3), "yon": en[6], "olcek": en[7]}
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
            for g, yon, olcek in [(g_, y_, o_) for y_, o_ in SURUMLER for g_ in (0.9, 0.7, 0.5)]:
                h = panel_boyu(k, g, oran, yon, olcek)
                if h >= 0.98:
                    continue
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
                        puan += (0 if olcek == 1.0 else 0.05) + (0 if yon == "yatay" else 0.02)
                        if en2 is None or puan < en2[0]:
                            en2 = (puan, x, y, g, h, ek, yon, olcek)
            _, x, y, g, h, ek, yon, olcek = en2
            y = max(y, 1.015) if ek and y > 0.985 else y
            k = {**k, "konum": [round(x, 4), round(y, 4)], "genislik": round(g, 3), "doluluk": 0.0, "kutu_h": round(h, 3),
                 "yon": yon, "olcek": olcek}
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


def anlam_denetimi(W: Path, key: str, C: dict, komutlar: list) -> dict:
    """Bağımsız tıbbi anlam denetimi (kullanıcı 2026-10-24: "panel gerçekten anlatılmak isteneni doğru mu anlatmış?").
    Her panel ve ok etiketi, öğrencinin okuyacağı biçimde (sablon.okunus) cümleyle yan yana bir Claude denetçisine verilir;
    denetçi tamam / duzelt (yeni alanlar) / sil kararı yazar. Sonuç önbellekte (aynı girdi yeniden sorulmaz).
    → {sıra: {"karar", "neden", "alanlar"}}"""
    import hashlib
    satir, idx = [], []
    for i, k in enumerate(komutlar):
        cid = str(k.get("cumle") or "")
        if cid not in C or not (k.get("tur") == "sema" or (k.get("tur") == "akis" and k.get("etiket"))):
            continue
        ok = SB.okunus(k) if k.get("tur") == "sema" else f"ok etiketi: {k.get('etiket')}"
        sab = f" [şablon: {k.get('sablon_ad') or k.get('sablon') or 'serbest şema'}]" if k.get("tur") == "sema" else ""
        satir.append(f"### {i}\nCümle: {C[cid]}\nPanel{sab}: {ok}\n")
        idx.append(i)
    if not idx:
        return {}
    girdi = "\n".join(satir)
    d = W / "anlam_denetimi"
    d.mkdir(exist_ok=True)
    h = hashlib.sha1(girdi.encode()).hexdigest()[:12]
    cikti = d / f"denetim_{h}.json"
    if not cikti.exists():
        (d / "girdi.md").write_text(girdi, encoding="utf-8")
        (d / "sablonlar.json").write_text(SB.YOL.read_text(encoding="utf-8"), encoding="utf-8")
        claude(d, "Sen tıp eğitimi içeriği denetçisisin. girdi.md'deki her ### numaralı bölümde bir sesli ders cümlesi ve o "
                  "cümle anlatılırken PDF üstünde gösterilecek panel/etiket var. Her biri için karar ver: panel cümlenin "
                  "anlattığını tıbben DOĞRU ve öğrencinin YANLIŞ anlamayacağı biçimde mi gösteriyor? Özellikle: ok yönü ve ok "
                  "üstündeki söz doğru ilişkiyi mi anlatıyor (ör. 'hastalık → istenir → test' yanlıştır: test hastalığa yol "
                  "açmaz; doğrusu 'Durum | Bakılacak tetkik' tablosu), bağımsız ilişkiler birbirine bağlıymış gibi mi duruyor, "
                  "şablon anlama uygun mu (sablonlar.json), terim cümlede/ders bağlamında doğru mu. Kararlar: "
                  "tamam | duzelt | sil. duzelt ise 'alanlar' içinde panelin yeni alanlarını ver (sablonlar.json'daki uygun "
                  "şablonun kimliği 'sablon' ve o düzenin alanları: tablo→satirlar, zincir/adimlar→ogeler, liste→baslik+ogeler, "
                  "grup→kaynaklar+sonuc, dal→soru+dallar, maske→gorunen+altta, karsit→kutuplar+satirlar; ok etiketi için "
                  "'etiket'). Yalnız cümlede geçen bilgiyi kullan. Çıktı: denetim.json = "
                  '{"<numara>": {"karar": "...", "neden": "kısa", "alanlar": {...}}}. Bitince tek satır: BİTTİ.', sure=1500)
        if (d / "denetim.json").exists():
            (d / "denetim.json").rename(cikti)
    try:
        return {int(x): v for x, v in json.loads(cikti.read_text(encoding="utf-8")).items()}
    except Exception:  # noqa: BLE001
        return {}


def lazer_uyumu(isr: dict | None, cid: str, k: dict, s: int) -> str | None:
    """Çizim, öğrencinin o an baktığı yerde olmalı (H59, cizim_kapisi K4/K7): komutun sayfası cümlenin lazer sayfası
    değilse ya da lazer bir resmi gösterirken panel (sema) yazılmışsa reddedilir."""
    try:
        pn, ci = cid[1:].split(".C")
        i = ((isr or {}).get("c") or {}).get(pn)[int(ci)]
    except (TypeError, ValueError, IndexError, AttributeError):
        return None
    if not i:
        return None
    if i.get("s") and int(i["s"]) != s:
        return "lazer sayfası dışında çizim (H59)"
    if k.get("tur") == "sema" and i.get("t") == "resim":
        return "resim anlatılırken panel (H59)"
    return None


def dok_uret(belge, out_dir: Path, force: bool = False):
    """PDF sayfalarını sNN.png (M# mavi madde, R# kırmızı resim, T# yeşil tablo kutuları) ve sNN.txt olarak üretir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    import pymupdf
    sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
    from pdf_isaret import Sayfa
    for i, pg in enumerate(belge, 1):
        png_yol = out_dir / f"s{i:02d}.png"
        txt_yol = out_dir / f"s{i:02d}.txt"
        if not force and png_yol.exists() and txt_yol.exists():
            continue
        sy = Sayfa(pg)
        satir = []
        for mi, m in enumerate(sy.maddeler):
            r = pymupdf.Rect(min(x[0] for x in m["satirlar"]), min(x[1] for x in m["satirlar"]),
                             max(x[2] for x in m["satirlar"]), max(x[3] for x in m["satirlar"]))
            pg.draw_rect(r, color=(0, 0, 1), width=0.8)
            pg.insert_text((r.x0 - 2, r.y0 + 6), f"M{mi}", fontsize=7, color=(0, 0, 1))
            satir.append(f"M{mi}: {' '.join(m['metin'])}")
        for ri in sy.tekil_resim:  # yinelenen (üst üste) görsel kutusu gösterilmez; numara kalıcı dizindir
            b = sy.resimler[ri]
            r = pymupdf.Rect(b)
            pg.draw_rect(r, color=(1, 0, 0), width=1.2)
            pg.insert_text((r.x0 + 2, r.y0 + 10), f"R{ri}", fontsize=10, color=(1, 0, 0))
            satir.append(f"R{ri}: resim {sy.n(b)}")
        for ti, b in enumerate(sy.tablolar):
            r = pymupdf.Rect(b)
            pg.draw_rect(r, color=(0, 0.6, 0), width=1.2)
            pg.insert_text((r.x1 - 18, r.y0 + 10), f"T{ti}", fontsize=10, color=(0, 0.6, 0))
            satir.append(f"T{ti}: tablo {sy.n(b)}")
        pg.get_pixmap(dpi=80).save(str(png_yol))
        txt_yol.write_text("\n".join(satir), encoding="utf-8")


def cizim_aday_uret(taslak_dir: Path, pdf_yol: Path | None = None, paralel: int = 4, parti_boyu: int = 6) -> dict:
    """Bir taslak klasörü (konusma_v2.json + baglam.json + PDF) için TALIMAT_CIZIM.md kurallarına tam uyumlu
    zengin çizim komutları (kontur, akış oku, eğri fazı, şema) üretir ve cizim_aday.json olarak kaydeder."""
    import hashlib
    import pymupdf

    taslak = Path(taslak_dir)
    baglam = json.loads((taslak / "baglam.json").read_text(encoding="utf-8")) if (taslak / "baglam.json").exists() else {}
    if not pdf_yol:
        if baglam.get("pdf_yolu") and (MEDS.parent / baglam["pdf_yolu"]).exists():
            pdf_yol = MEDS.parent / baglam["pdf_yolu"]
        elif (taslak / f"{taslak.name}.pdf").exists():
            pdf_yol = taslak / f"{taslak.name}.pdf"
        else:
            adaylar_pdf = list((MEDS.parent / "meds_database_25_26" / "pdf").rglob(f"*{taslak.name}*.pdf"))
            if adaylar_pdf:
                pdf_yol = adaylar_pdf[0]

    if not pdf_yol or not Path(pdf_yol).exists():
        raise FileNotFoundError(f"Ders PDF dosyası bulunamadı: {pdf_yol}")

    belge = pymupdf.open(pdf_yol)
    dok_dir = taslak / "cizim_dok"
    dok_uret(belge, dok_dir)

    v2_yol = taslak / "konusma_v2.json"
    if not v2_yol.exists():
        raise FileNotFoundError(f"konusma_v2.json bulunamadı: {v2_yol}")
    v2 = json.loads(v2_yol.read_text(encoding="utf-8"))

    C: dict[str, str] = {}
    sayfa_cumle: dict[int, list[str]] = {}
    cumle_satirlari = []
    pi = 0
    for b in v2.get("bolumler", []):
        cumle_satirlari.append(f"\n### BÖLÜM: {b.get('baslik', '')}")
        for p in b.get("paragraflar", []):
            cumle_satirlari.append(f"\n## P{pi}")
            for ci, c in enumerate(p.get("cumleler", [])):
                cid = f"P{pi}.C{ci}"
                metin = c.get("ses") or c.get("ekran") or ""
                C[cid] = metin
                s = int(c.get("slayt", {}).get("sayfa") or 1)
                sayfa_cumle.setdefault(s, []).append(cid)
                ks = metin.split()
                cumle_satirlari.append(f"{cid}: " + " ".join(f"[{j}]{w}" for j, w in enumerate(ks)))
            pi += 1
    (dok_dir / "cumleler.md").write_text("\n".join(cumle_satirlari), encoding="utf-8")

    sayfalar = sorted(sayfa_cumle)
    partiler = [sayfalar[i:i + parti_boyu] for i in range(0, len(sayfalar), parti_boyu)]
    W = taslak / "cizim_is"
    W.mkdir(parents=True, exist_ok=True)

    ADAY: dict[int, dict] = {}
    ADAY_LISTE: dict[int, tuple] = {}
    for s_ in sayfalar:
        if 1 <= s_ <= belge.page_count:
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
            png = dok_dir / f"s{s:02d}.png"
            satir.append(f"## Sayfa {s} — görüntü: {png}")
            satir += [x for x in (dok_dir / f"s{s:02d}.txt").read_text(encoding="utf-8").splitlines() if x.startswith(("R", "M"))][:30] \
                if (dok_dir / f"s{s:02d}.txt").exists() else []
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
        (d / "sablonlar.json").write_text(SB.YOL.read_text(encoding="utf-8"), encoding="utf-8")
        istem = (
            f"{TALIMAT} talimatını uygula. Çalışma dizinindeki sayfalar.md'yi oku; listelenen her sayfa görüntüsünü (sNN.png) "
            "Read aracı ile aç ve dikkatle incele.\n\n"
            "ÖNEMLİ KURALLAR:\n"
            "1. GÖRSEL/TABLO/ŞEMA SAYFALARI:\n"
            "   - Anlatılan anatomik yapılar, lezyonlar, organlar, dokular, herniasyonlar, kanama odakları, anevrizmalar, "
            "hücreler veya tablo bölgeleri için mutlaka `tur: 'kontur'` kullan. Yapının sınırını 5-20 nokta ile KENARI boyunca "
            "sırayla dolan (nokta: [[x,y],...]). Bu alanlar oynatıcıda yarı saydam fosforlu sarı marker ile boyanacak ve kırmızı kontur hattıyla çevrilecektir!\n"
            "   - Yapılar arası yön, etki, yolak veya neden-sonuç için `tur: 'akis'` ile ok rotası çiz (a: [x,y], b: [x,y], iliski: 'aktive'|'inhibe'|'donusur', etiket: '...'). "
            "Eğer PDF'te zaten çizili bir ok varsa, onu kopyalamak yerine aday oktan seç veya odak çerçevesi çiz.\n"
            "   - Bir kaynaktan birden çok yere giden dallanmalar için `dallar` kullan.\n"
            "   - Grafik ve eğriler için `tur: 'egri_faz'` kullan.\n"
            "   - Görsel üzerindeki tüm bu çizimler için konuşma anında anlatılan bölgeye oynatıcı tarafından otomatik ZOOM yapılacaktır!\n"
            "2. YAZI AĞIRLIKLI SLAYTLAR:\n"
            "   - sablonlar.json kütüphanesinden tıbbi anlama tam uyan şablonu seçerek `tur: 'sema'` paneli kur "
            "(tani_tetkik, zehir_antidot, bulgu_dusundurur, lezyon_bulgu, neden_sonuc, siniflama, karsilastirma vb.).\n"
            "Çıktıyı `cizim.json` dosyasına `{\"komutlar\": [...]}` olarak kaydet. Bitince: BİTTİ."
        )
        t = time.time()
        r = claude(d, istem)
        return i, f"{round((time.time() - t) / 60, 1)} dk {r.strip()[-80:]}"

    with ThreadPoolExecutor(max_workers=paralel) as ex:
        for i, durum in ex.map(parti_isle, enumerate(partiler)):
            print(f"  parti {i}: {durum}", flush=True)

    tum_komut = []
    for f in sorted(W.glob("parti*/cizim.json")):
        try:
            tum_komut += json.loads(f.read_text(encoding="utf-8")).get("komutlar") or []
        except Exception:
            pass

    for k in tum_komut:
        if isinstance(k.get("yeni_sablon"), dict):
            sid = SB.yeni_ekle(k["yeni_sablon"], taslak.name)
            if sid:
                k["sablon"] = sid

    cikti_aday = {"komutlar": tum_komut}
    (taslak / "cizim_aday.json").write_text(json.dumps(cikti_aday, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{taslak.name}] {len(tum_komut)} adet çizim komutu cizim_aday.json dosyasına kaydedildi.")
    return cikti_aday


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--taslak", default=None, help="Taslak klasörü yolu (verilirse otomatik aday üretir)")
    ap.add_argument("--pdf", default=None, help="Doğrudan PDF dosya yolu")
    ap.add_argument("--v2", default=None, help="konusma_v2.json dosya yolu")
    ap.add_argument("--cikti", default=None, help="Çıktı JSON dosya yolu")
    ap.add_argument("--dok", default=None)
    ap.add_argument("--capa", default=None)
    ap.add_argument("--isaret", default=None)
    ap.add_argument("--paralel", type=int, default=4)
    ap.add_argument("--parti", type=int, default=6)
    ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--is-dizini", default=None)
    a = ap.parse_args()

    if a.taslak:
        cizim_aday_uret(Path(a.taslak), pdf_yol=Path(a.pdf) if a.pdf else None, paralel=a.paralel, parti_boyu=a.parti)
        return 0

    W = Path(a.is_dizini or (MEDS.parent / "meds_temp" / "cizim" / a.key))
    W.mkdir(parents=True, exist_ok=True)
    dok = Path(a.dok) if a.dok else (W / "dok")
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
        (d / "sablonlar.json").write_text(SB.YOL.read_text(encoding="utf-8"), encoding="utf-8")
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
    tum_komut = []
    kut = SB.kutuphane()
    for f in sorted(W.glob("parti*/cizim.json")):
        try:
            tum_komut += json.loads(f.read_text()).get("komutlar") or []
        except Exception as e:  # noqa: BLE001
            print(f"  {f.parent.name}: cizim.json okunamadı ({e})")
    # yeni şablon önerileri kütüphaneye (kapıdan geçerse; sonraki dersler de kullanır)
    for k in tum_komut:
        if isinstance(k.get("yeni_sablon"), dict):
            sid = SB.yeni_ekle(k["yeni_sablon"], a.key)
            if sid:
                k["sablon"] = sid
                say.setdefault("yeni_sablon", []).append(sid)
    kut = SB.kutuphane()
    for k in tum_komut:
        if k.get("tur") == "sema" and k.get("sablon"):
            k2, _ = SB.coz(k, kut)
            k.update(k2)
    # bağımsız tıbbi anlam denetimi (tamam / düzelt / sil)
    kararlar = anlam_denetimi(W, a.key, C, tum_komut)
    silinen = 0
    for i, kr in kararlar.items():
        if not (0 <= i < len(tum_komut)):
            continue
        if kr.get("karar") == "sil":
            tum_komut[i]["_sil"] = kr.get("neden") or "anlam denetimi"; silinen += 1
        elif kr.get("karar") == "duzelt" and isinstance(kr.get("alanlar"), dict):
            k = tum_komut[i]
            for x in ("dugum", "kenar", "satirlar", "ogeler", "kaynaklar", "sonuc", "soru", "dallar", "gorunen", "altta",
                      "kutuplar", "baslik", "basliklar", "bag", "duzen", "sablon_ad"):
                k.pop(x, None) if k.get("tur") == "sema" else None
            k.update(kr["alanlar"])
            if k.get("tur") == "sema" and k.get("sablon"):
                k2, _ = SB.coz(k, kut); k.update(k2)
    say["anlam_denetimi"] = {"bakilan": len(kararlar), "duzeltilen": sum(1 for v in kararlar.values() if v.get("karar") == "duzelt"),
                             "silinen": silinen}
    for komutlar in [tum_komut]:
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
            neden_l = lazer_uyumu(isr, cid, k, s)
            if neden_l:
                say["ret"][neden_l] = say["ret"].get(neden_l, 0) + 1
                continue
            ad = (ADAY.get(s) or {}).get(str(k.get("aday") or ""))
            if ad:                       # aday seçildi: koordinat betikle adaydan (tahmin değil, PDF/görüntü çizimi)
                k = {**k, **{x: ad[x] for x in ("a", "b", "nokta", "fazlar") if x in ad}}
                if "iliski" in ad and k.get("tur") == "akis":
                    k["iliski"] = k.get("iliski") or ad["iliski"]
            # PDF'in kendi okunu kopyalayan ok (H52, s.27: slaytın kırmızı okları mavi okla yeniden çiziliyordu): uçları bir
            # aday okun uçlarına (≤0,1) denk gelen akış, o adayın kesin koordinatına oturur ve odak çerçevesine çevrilir
            if k.get("tur") == "akis" and not ad and k.get("a") and k.get("b") and s in ADAY_LISTE:
                yak = lambda p_, q_: ((p_[0] - q_[0]) ** 2 + (p_[1] - q_[1]) ** 2) ** 0.5
                for x in ADAY_LISTE[s][0]:
                    if min(max(yak(k["a"], x["a"]), yak(k["b"], x["b"])), max(yak(k["a"], x["b"]), yak(k["b"], x["a"]))) < 0.1:
                        x0, x1 = sorted((x["a"][0], x["b"][0])); y0, y1 = sorted((x["a"][1], x["b"][1]))
                        k = {**k, "a": x["a"], "b": x["b"], "pdf_oku": [round(max(0, x0 - 0.015), 4), round(max(0, y0 - 0.015), 4),
                                                                        round(min(1, x1 + 0.015), 4), round(min(1, y1 + 0.015), 4)]}
                        say["pdf_oku_odak"] = say.get("pdf_oku_odak", 0) + 1
                        break
            if s and s not in raster and belge is not None and 1 <= s <= belge.page_count:
                raster[s] = CD.SayfaRaster(belge[s - 1])
            # aday olarak algılanmayan (raster) mevcut ok: a→b düz çizgisi boyunca slaytta çizili hat varsa yeni ok çizilmez
            if k.get("tur") == "akis" and not k.get("pdf_oku") and k.get("a") and k.get("b") and raster.get(s) is not None:
                a_, b_ = k["a"], k["b"]
                orn = [[a_[0] + (b_[0] - a_[0]) * i / 20, a_[1] + (b_[1] - a_[1]) * i / 20] for i in range(3, 18)]
                if ((a_[0] - b_[0]) ** 2 + (a_[1] - b_[1]) ** 2) ** 0.5 > 0.08 and raster[s].kenar_orani(orn) >= 0.8:
                    x0, x1 = sorted((a_[0], b_[0])); y0, y1 = sorted((a_[1], b_[1]))
                    k = {**k, "pdf_oku": [round(max(0, x0 - 0.012), 4), round(max(0, y0 - 0.012), 4), round(min(1, x1 + 0.012), 4), round(min(1, y1 + 0.012), 4)]}
                    say["pdf_oku_odak"] = say.get("pdf_oku_odak", 0) + 1
            onceki = " ".join(C[x] for x in sira[:sira.index(cid) + 1])
            if k.get("_sil"):
                say["ret"]["anlam denetimi sildi"] = say["ret"].get("anlam denetimi sildi", 0) + 1
                continue
            if k.get("tur") == "sema":
                if s not in satir_onbellek and belge is not None and 1 <= s <= belge.page_count:
                    satir_onbellek[s] = sayfa_satirlari(belge[s - 1])
                if resim_sayfasi(kutular(dok / f"s{s:02d}.txt"), satir_onbellek.get(s), raster.get(s)):
                    say["ret"]["resim sayfasında panel (görsel üstünde çiz, H51)"] = say["ret"].get("resim sayfasında panel (görsel üstünde çiz, H51)", 0) + 1
                    say.setdefault("resim_sayfasi_panel", []).append(s)
                    continue
            if k.get("tur") == "sema" and k.get("sablon"):
                k, neden_s = SB.coz(k, kut)
                if neden_s:
                    say["ret"][neden_s[:60]] = say["ret"].get(neden_s[:60], 0) + 1
                    continue
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
                                       "kaynak_metin", "hedef_metin", "dal", "sablon", "sablon_ad", "duzen", "basliklar",
                                       "bag", "satirlar", "ogeler", "kaynaklar", "sonuc", "soru", "dallar", "gorunen", "altta",
                                       "kutuplar", "baslik", "numarali", "pdf_oku") if x in k}
            komut.update(s=s, k=[ka[k["bas"]][0], ka[k["son"]][1]])
            if s not in satir_onbellek and belge is not None and 1 <= s <= belge.page_count:
                satir_onbellek[s] = sayfa_satirlari(belge[s - 1])
            yer = yerlesim(komut, raster.get(s), sayfa_dolu.setdefault(s, []), satir_onbellek.get(s))
            if lazer_uyumu(isr, cid, yer, s):  # yazıya düşen ok panele dönmüş olabilir (oku_panele): resim cümlesinde panel yok
                say["ret"]["resim anlatılırken panel (H59)"] = say["ret"].get("resim anlatılırken panel (H59)", 0) + 1
                continue
            kb = kutular(dok / f"s{s:02d}.txt")
            yk = yakinlasma(yer, kb, resim_sayfasi(kb, satir_onbellek.get(s), raster.get(s)))
            if yk:
                yer["yakin"] = yk
            mevcut.append(yer)
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
