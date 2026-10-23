#!/usr/bin/env python3
"""Şema okları → "A → B" (aktive) / "A ⊣ B" (inhibe) bağları, L0 metin satırlarına bağlı (ICERIK_MOTORU_V3.md §12.1).

Ders PDF'lerinde oklar çoğunlukla VEKTÖR çizimdir (PPTX dışa aktarımı); piksel tahmini yerine PyMuPDF `get_drawings()`
kayıtları okunur — koordinatlar birebirdir:
  - çizgi + baş: çizilmiş (stroke) düz çizgi parçasının ucunun uzantısında küçük (≤ %2 sayfa) dolu üçgen ya da
    çentikli dart (4 köşe); yön çizgiden: kuyruk = başa uzak uç (süs üçgenleri boyutla elenir);
  - blok ok: 7 köşeli dolu çokgen; uç = merkeze en uzak köşe, kuyruk = merkezin uca göre simetriği;
  - inhibisyon: çizgi ucunda kısa dik çizgi (⊣).
Uçlar okun DOĞRULTUSUNDA (±~30° koni, sayfa genişliğinin ≤ %15'i) en yakın L0 metin BLOĞUNA bağlanır (çok satırlı
şema etiketi tek düğüm); iki uç aynı bloğa düşerse ya da biri boşsa bağ yazılmaz. `a`/`b` = blok satır listeleri.
Resim içine gömülü (raster) oklar bu betiğin kapsamı dışındadır (gerekirse Hough yedeği ayrı adım).
Çıktı: L0 sayfasına `ok: [{a, b, a_metin, b_metin, tur: aktive|inhibe, bas:[x,y], son:[x,y], bicim, guven}]` (sayfa oranı).
Güven: çizgi oku `yuksek` (k1-12 s20 Robbins araşidonik asit şeması: 11 bağın 10'u doğru); blok ok `dusuk` (resim içi
süs okları da 7 köşelidir) — çizim motoru düşük güvenli bağı yalnız anlatımda iki uç terimi aynı cümlede geçince kullanır.

Kullanım (.venv-ocr): ok.py --ders k1-38 [--yaz]   |   ok.py --kurul 1 [--yaz]   (özet sayılar)
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf  # noqa: E402

import l0kayit  # noqa: E402
from ortak import dersler, pdf_bul  # noqa: E402


def _uz(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _cokgen(dr) -> list[tuple] | None:
    """Yalnız düz çizgilerden oluşan kapalı yolun köşeleri."""
    it = dr["items"]
    if not it or any(i[0] != "l" for i in it):
        return None
    k = [(i[1].x, i[1].y) for i in it]
    son = (it[-1][2].x, it[-1][2].y)
    if _uz(son, k[0]) > 1.0:
        k.append(son)
    return k


def parcalar(sayfa) -> tuple[list, list, list]:
    W = sayfa.rect.width
    sayfa_kutu = sayfa.rect + (-2, -2, 2, 2)
    cizgi, bas, blok = [], [], []
    for dr in sayfa.get_drawings():
        tip = dr.get("type") or ""
        if not sayfa_kutu.contains(dr["rect"]):
            continue                                  # sayfa dışı çerçeve/şablon kalıntısı
        if "s" in tip:
            for i in dr["items"]:
                if i[0] == "l":
                    a, b = (i[1].x, i[1].y), (i[2].x, i[2].y)
                    if _uz(a, b) >= 0.015 * W:
                        cizgi.append((a, b))
                    elif _uz(a, b) >= 3:
                        cizgi.append((a, b))          # kısa çizgi: inhibisyon çubuğu adayı
        if "f" in tip:
            k = _cokgen(dr)
            if not k:
                continue
            r = dr["rect"]
            alan = r.width * r.height / max(W * sayfa.rect.height, 1)
            if len(k) in (3, 4) and max(r.width, r.height) <= 0.02 * W:
                # ok başı: küçük dolu üçgen ya da çentikli "dart" (4 köşe); uç yönü çizgiden belirlenir (oklar())
                mx, my = sum(p[0] for p in k) / len(k), sum(p[1] for p in k) / len(k)
                uc = max(k, key=lambda p: _uz(p, (mx, my)))
                bas.append({"uc": uc, "merkez": (mx, my), "boy": max(r.width, r.height)})
            elif len(k) == 7 and alan < 0.05:
                mx, my = sum(p[0] for p in k) / 7, sum(p[1] for p in k) / 7
                uz = sorted(_uz(p, (mx, my)) for p in k)
                uc = max(k, key=lambda p: _uz(p, (mx, my)))
                if uz[-1] >= 1.3 * uz[len(uz) // 2]:           # belirgin tek uç: blok ok biçimi
                    blok.append({"uc": uc, "kuyruk": (2 * mx - uc[0], 2 * my - uc[1])})
    return cizgi, bas, blok


def oklar(sayfa) -> list[dict]:
    W = sayfa.rect.width
    cizgi, bas, blok = parcalar(sayfa)
    uzun = [c for c in cizgi if _uz(*c) >= 0.015 * W]
    kisa = [c for c in cizgi if _uz(*c) < 0.015 * W]
    out = []
    for a, b in uzun:
        for kuyruk, uc in ((a, b), (b, a)):
            dx, dy = uc[0] - kuyruk[0], uc[1] - kuyruk[1]
            L = math.hypot(dx, dy) or 1
            # baş: merkezi çizgi ucuna yakın ve yönü çizgiyle aynı
            ux, uy = dx / L, dy / L
            def uzantida(h):
                # baş merkezi çizgi doğrultusunda, ucun hemen ötesinde/üstünde; yan sapma baş boyunu geçmez
                mx, my = h["merkez"][0] - kuyruk[0], h["merkez"][1] - kuyruk[1]
                boy = mx * ux + my * uy
                yan = abs(-mx * uy + my * ux)
                return L * 0.9 <= boy <= L + 1.5 * h["boy"] + 3 and yan <= max(3, h["boy"])
            h = next((h for h in bas if uzantida(h)), None)
            if h:
                ucn = max(h["uc"], h["merkez"], key=lambda q: _uz(q, kuyruk))
                out.append({"kuyruk": kuyruk, "uc": ucn, "tur": "aktive", "bicim": "cizgi"})
                break
            # inhibisyon: uca dik kısa çizgi
            for p, q in kisa:
                orta = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
                # çubuk tek başına olmalı: uçları başka bir çizgiye değmiyor (dikdörtgen köşesi ⊣ sanılmasın)
                serbest = not any(min(_uz(p, x), _uz(p, y), _uz(q, x), _uz(q, y)) <= 2
                                  for x, y in cizgi if (x, y) not in ((p, q), (a, b)))
                if serbest and 4 <= _uz(p, q) <= 25 and _uz(orta, uc) <= 3:
                    ex, ey = q[0] - p[0], q[1] - p[1]
                    cos = abs(ex * dx + ey * dy) / (math.hypot(ex, ey) * L or 1)
                    if cos < 0.35:
                        out.append({"kuyruk": kuyruk, "uc": uc, "tur": "inhibe", "bicim": "cizgi"})
                        break
            else:
                continue
            break
    for bk in blok:
        out.append({"kuyruk": bk["kuyruk"], "uc": bk["uc"], "tur": "aktive", "bicim": "blok"})
    return out


def _satira_uzaklik(p, kutu) -> float:
    x0, y0, x1, y1 = kutu
    dx = max(x0 - p[0], 0, p[0] - x1)
    dy = max(y0 - p[1], 0, p[1] - y1)
    return math.hypot(dx, dy)


def bloklar(l0_sayfa: dict, W: float, H: float) -> list[tuple]:
    """L0 satırlarını PDF bloğu düzeyinde birleştirir: (anahtar, kutu_pt, metin, satır listesi)."""
    g: dict = {}
    for i, st in enumerate(l0_sayfa["satirlar"]):
        if len(st["metin"].strip("•–-·▪➢ ")) < 2:
            continue
        k = st.get("blok", i)
        x0, y0, x1, y1 = st["bbox"][0] * W, st["bbox"][1] * H, st["bbox"][2] * W, st["bbox"][3] * H
        if k in g:
            b = g[k]
            b[1] = [min(b[1][0], x0), min(b[1][1], y0), max(b[1][2], x1), max(b[1][3], y1)]
            b[2] += " " + st["metin"]
            b[3].append(i)
        else:
            g[k] = [k, [x0, y0, x1, y1], st["metin"], [i]]
    return [tuple(v) for v in g.values()]


def _koni(p, u, bloklar_, W) -> tuple | None:
    """p noktasından u doğrultusunda (±~30°) en yakın blok; okun gösterdiği yazı."""
    en = None
    for b in bloklar_:
        x0, y0, x1, y1 = b[1]
        cx, cy = min(max(p[0], x0), x1), min(max(p[1], y0), y1)       # kutunun p'ye en yakın noktası
        dx, dy = cx - p[0], cy - p[1]
        d = math.hypot(dx, dy)
        boy = dx * u[0] + dy * u[1]
        yan = abs(-dx * u[1] + dy * u[0])
        if d > 0.15 * W or boy < -0.01 * W or yan > max(0.6 * max(boy, 0), 0.025 * W):
            continue
        puan = d + 0.5 * yan
        if en is None or puan < en[0]:
            en = (puan, b)
    return en[1] if en else None


def bagla(sayfa, l0_sayfa: dict) -> list[dict]:
    W, H = sayfa.rect.width, sayfa.rect.height
    bl = bloklar(l0_sayfa, W, H)
    out, gorulen = [], set()
    for o in oklar(sayfa):
        dx, dy = o["uc"][0] - o["kuyruk"][0], o["uc"][1] - o["kuyruk"][1]
        L = math.hypot(dx, dy) or 1
        u = (dx / L, dy / L)
        a = _koni(o["kuyruk"], (-u[0], -u[1]), bl, W)
        b = _koni(o["uc"], u, bl, W)
        if not a or not b or a[0] == b[0] or (a[0], b[0], o["tur"]) in gorulen:
            continue
        gorulen.add((a[0], b[0], o["tur"]))
        out.append({"a": a[3], "b": b[3], "a_metin": a[2][:80], "b_metin": b[2][:80], "tur": o["tur"], "bicim": o["bicim"],
                    "guven": "yuksek" if o["bicim"] == "cizgi" else "dusuk",
                    "bas": [round(o["kuyruk"][0] / W, 4), round(o["kuyruk"][1] / H, 4)],
                    "son": [round(o["uc"][0] / W, 4), round(o["uc"][1] / H, 4)]})
    return out


def ders_oklari(ders: str) -> dict[int, list]:
    l0 = l0kayit.yukle(ders)
    b = pymupdf.open(pdf_bul(ders))
    return {s["sayfa"]: v for s in l0["sayfalar"] if (v := bagla(b[s["sayfa"] - 1], s))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ders"); ap.add_argument("--kurul", type=int); ap.add_argument("--yaz", action="store_true")
    a = ap.parse_args()
    liste = [a.ders] if a.ders else dersler(a.kurul)
    toplam = 0
    for d in liste:
        try:
            ok = ders_oklari(d)
        except SystemExit as e:
            print(f"{d}: {e}"); continue
        n = sum(len(v) for v in ok.values())
        toplam += n
        if a.ders or n:
            print(f"{d}: {n} bağ, {len(ok)} sayfa")
        if a.ders:
            for s, v in ok.items():
                for o in v:
                    print(f"  s{s}: {o['a_metin'][:40]!r} {'→' if o['tur'] == 'aktive' else '⊣'} {o['b_metin'][:40]!r} ({o['bicim']})")
        if a.yaz:
            l0kayit.yaz_toplu(d, {s: {"ok": v} for s, v in ok.items()})
    print(f"toplam {toplam} bağ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
