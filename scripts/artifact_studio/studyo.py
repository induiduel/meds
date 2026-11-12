#!/usr/bin/env python3
"""Artifact stüdyosu (2026-11-13) — tek dosyalık, çevrimdışı HTML artifact üretici.

Claude masaüstünün "artifact" özelliği 3P geçit kipinde çalışmadığı için eşdeğeri yerelde:
JSON reçete → kendi kendine yeten HTML sayfa (satır içi CSS/JS, dış istek yok, yazı tipi sistemden)
→ tarayıcı önizleme bölmesinde açılır. İçerik uydurmaz: yalnız verilen metni/veriyi düzenler.

Kullanım:
  python3 meds/scripts/artifact_studio/studyo.py reçete.json [-o çıktı.html] [--tema koyu] [--ac "#2f6f4f"]
  python3 meds/scripts/artifact_studio/studyo.py --ornek            # örnek reçeteyi üret
  python3 meds/scripts/artifact_studio/studyo.py --sema             # reçete şemasını yaz

Reçete kutuları: metrik · metin · maddeler · grafik (çizgi|sütun) · tablo · not (uyarı|bilgi|başarı) ·
alıntı · kod · ayraç. Her kutuya `genislik` verilebilir: "tam" | "yarim" | "dar" (bento ızgara).
Bu betik ağa çıkmaz (AGENTS kural 20 ile uyumlu).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from html import escape
from pathlib import Path

SURUM = "1"
VARSAYILAN_CIKTI = Path(__file__).resolve().parent / "cikti"
TEMA_RENK = {
    "acik": {"zemin": "#f7f7f5", "kart": "#ffffff", "cizgi": "#e6e4df", "metin": "#1b1b19",
             "soluk": "#6b6a64", "izgara": "#eeece7"},
    "koyu": {"zemin": "#131413", "kart": "#1c1d1b", "cizgi": "#2e302d", "metin": "#f2f1ed",
             "soluk": "#a3a29a", "izgara": "#262724"},
}
PALET = ["#2f6f4f", "#c2703d", "#3a6ea5", "#9a5ea8", "#b5872b", "#3f8f8a"]
TR_HARF = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iissgguuoocc")


# ── yardımcılar ────────────────────────────────────────────────────────────────────────────────────────────────
def e(v) -> str:
    return escape("" if v is None else str(v), quote=True)


def sayi(v) -> str:
    """Türkçe okunur sayı: 1234.5 → 1.234,5 (zaten metinse dokunulmaz)."""
    if isinstance(v, (int, float)):
        s = f"{v:,.2f}".rstrip("0").rstrip(".")
        return s.replace(",", "§").replace(".", ",").replace("§", ".")
    return str(v)


def _seri_renk(seri: dict, i: int) -> str:
    return seri.get("renk") or PALET[i % len(PALET)]


# ── grafikler (satır içi SVG) ──────────────────────────────────────────────────────────────────────────────────
def _olcek(degerler: list[float], sifir: bool = False) -> tuple[float, float, float]:
    """Eksen aralığı ve adımı: okunur yuvarlak sayılar (1 · 2 · 2,5 · 5 · 10 × 10ⁿ).

    `sifir` verilirse sütun grafiğinde taban 0 olur (veri negatifse 0 yine aralıkta kalır)."""
    d = list(degerler) or [0.0]
    lo, hi = min(d), max(d)
    if sifir:
        lo, hi = min(lo, 0.0), max(hi, 0.0)
    if hi == lo:
        hi = lo + 1
    ham = (hi - lo) / 4
    us = 10 ** math.floor(math.log10(ham))
    adim = next(m * us for m in (1, 2, 2.5, 5, 10) if ham <= m * us)
    return math.floor(lo / adim) * adim, math.ceil(hi / adim) * adim, adim


def _eksenler(seriler: list[dict], sifir: bool) -> tuple[tuple[float, float, float], tuple[float, float, float] | None]:
    """Sol eksen 'sol' serilerini, sağ eksen `"eksen": "sag"` işaretli serileri kapsar.

    Farklı büyüklükteki seriler (ör. 0–5 ders sayısı ile 40–96 soru sayısı) tek eksende ezilmesin diye
    ikinci eksen; sağda seri yoksa aralık None döner."""
    sol = [float(v) for s in seriler if (s.get("eksen") or "sol") != "sag" for v in (s.get("degerler") or [])]
    sag = [float(v) for s in seriler if (s.get("eksen") or "sol") == "sag" for v in (s.get("degerler") or [])]
    if not sol:  # hepsi sağ işaretliyse sağ eksen sol eksene döner
        sol, sag = sag, []
    return _olcek(sol, sifir), (_olcek(sag, sifir) if sag else None)


def _yk(v: float, aralik: tuple[float, float, float], Y: int, ust: int, alt: int) -> float:
    lo, hi = aralik[0], aralik[1]
    return ust + (Y - ust - alt) * (1 - (v - lo) / (hi - lo))


def _izgara(parca: list[str], aralik: tuple[float, float, float],
            aralik2: tuple[float, float, float] | None,
            G: int, Y: int, sol: float, sag: float, ust: int, alt: int) -> None:
    lo, hi, adim = aralik
    k = 0
    v = hi
    while v >= lo - adim / 2 and k < 12:
        gy = _yk(v, aralik, Y, ust, alt)
        parca.append(f'<line x1="{sol}" y1="{gy:.1f}" x2="{G - sag}" y2="{gy:.1f}" stroke="var(--izgara)"/>')
        parca.append(f'<text x="{sol - 8}" y="{gy + 4:.1f}" text-anchor="end" class="eksen">{e(sayi(round(v, 4)))}</text>')
        v -= adim
        k += 1
    if aralik2:  # sağ eksen etiketleri kendi ölçeğinde (ızgaraya bağlı değil)
        lo2, hi2, adim2 = aralik2
        k = 0
        v2 = hi2
        while v2 >= lo2 - adim2 / 2 and k < 12:
            gy = _yk(v2, aralik2, Y, ust, alt)
            parca.append(f'<text x="{G - sag + 8}" y="{gy + 4:.1f}" text-anchor="start" class="eksen">'
                         f'{e(sayi(round(v2, 4)))}</text>')
            v2 -= adim2
            k += 1


def grafik_cizgi(kutu: dict) -> str:
    etiketler = [str(x) for x in kutu.get("etiketler") or []]
    seriler = kutu.get("seriler") or []
    if not seriler:
        return '<p class="bos">Grafik için seri yok.</p>'
    G, Y = 680, 240
    sol, sag, ust, alt = 44, 44, 18, 34
    aralik, aralik2 = _eksenler(seriler, False)
    n = max(1, len(seriler[0].get("degerler") or []) - 1)

    def x(i: int) -> float:
        return sol + (G - sol - sag) * (i / n if n else 0)

    parca = [f'<svg class="grafik" viewBox="0 0 {G} {Y}" role="img" aria-label="{e(kutu.get("baslik") or "grafik")}">']
    _izgara(parca, aralik, aralik2, G, Y, sol, sag, ust, alt)
    if etiketler:
        adim = max(1, len(etiketler) // 7)
        for i, lb in enumerate(etiketler):
            if i % adim == 0 or i == len(etiketler) - 1:
                parca.append(f'<text x="{x(i):.1f}" y="{Y - 12}" text-anchor="middle" class="eksen">{e(lb)}</text>')
    for si, s in enumerate(seriler):
        vs = [float(v) for v in (s.get("degerler") or [])]
        if not vs:
            continue
        ar = aralik2 if ((s.get("eksen") or "sol") == "sag" and aralik2) else aralik
        renk = _seri_renk(s, si)
        noktalar = " ".join(f"{x(i):.1f},{_yk(v, ar, Y, ust, alt):.1f}" for i, v in enumerate(vs))
        parca.append(f'<polyline points="{noktalar}" fill="none" stroke="{e(renk)}" stroke-width="2.4" '
                     f'stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(vs):
            parca.append(f'<circle cx="{x(i):.1f}" cy="{_yk(v, ar, Y, ust, alt):.1f}" r="3.2" fill="{e(renk)}"/>')
    parca.append("</svg>")
    return "".join(parca)


def grafik_sutun(kutu: dict) -> str:
    etiketler = [str(x) for x in kutu.get("etiketler") or []]
    seriler = kutu.get("seriler") or []
    if not seriler:
        return '<p class="bos">Grafik için seri yok.</p>'
    G, Y = 680, 240
    sol, sag, ust, alt = 44, 44, 18, 34
    aralik, aralik2 = _eksenler(seriler, True)  # sütun grafiğinde sıfır tabanı
    kes = len(seriler[0].get("degerler") or []) or 1
    bant = (G - sol - sag) / kes
    bw = max(6.0, min(34.0, bant * 0.66 / len(seriler)))

    parca = [f'<svg class="grafik" viewBox="0 0 {G} {Y}" role="img" aria-label="{e(kutu.get("baslik") or "grafik")}">']
    _izgara(parca, aralik, aralik2, G, Y, sol, sag, ust, alt)
    for si, s in enumerate(seriler):
        ar = aralik2 if ((s.get("eksen") or "sol") == "sag" and aralik2) else aralik
        sifir = _yk(max(ar[0], min(ar[1], 0.0)), ar, Y, ust, alt)
        for i, v in enumerate(s.get("degerler") or []):
            v = float(v)
            cx = sol + bant * i + bant / 2 - (len(seriler) * bw) / 2 + si * bw
            yv = _yk(v, ar, Y, ust, alt)
            y0, y1 = (yv, sifir) if v >= 0 else (sifir, yv)
            parca.append(f'<rect x="{cx:.1f}" y="{y0:.1f}" width="{bw - 2:.1f}" height="{max(1.0, y1 - y0):.1f}" '
                         f'rx="3" fill="{e(_seri_renk(s, si))}"/>')
    if etiketler:
        adim = max(1, len(etiketler) // 8)
        for i, lb in enumerate(etiketler):
            if i % adim == 0:
                cx = sol + bant * i + bant / 2
                parca.append(f'<text x="{cx:.1f}" y="{Y - 12}" text-anchor="middle" class="eksen">{e(lb)}</text>')
    parca.append("</svg>")
    return "".join(parca)


# ── kutu türleri ──────────────────────────────────────────────────────────────────────────────────────────────
def kutu_metrik(k: dict) -> str:
    yon = k.get("yon") or ""
    ok = {"artis": "↑", "azalis": "↓", "notr": "→"}.get(yon, "")
    if str(k.get("degisim") or "").strip().lstrip("+-").replace(",", ".") in ("0", "0.0"):
        ok = ""  # sıfır değişimde ok anlamsız
    sinif = {"artis": "iyi", "azalis": "kotu", "notr": "notr"}.get(yon, "notr")
    degisim = ""
    if k.get("degisim") not in (None, ""):
        degisim = f'<span class="degisim {sinif}">{e(ok)} {e(k["degisim"])}</span>'
    return (f'<div class="metrik"><div class="etiket">{e(k.get("etiket"))}</div>'
            f'<div class="deger">{e(sayi(k.get("deger")))}<span class="birim">{e(k.get("birim"))}</span></div>'
            f'{degisim}<div class="alt">{e(k.get("alt"))}</div></div>')


def kutu_metin(k: dict) -> str:
    madde = "".join(f"<li>{e(m)}</li>" for m in (k.get("maddeler") or []))
    return (f'{bas(k)}<p>{e(k.get("govde"))}</p>'
            + (f'<ul class="maddeler">{madde}</ul>' if madde else ""))


def bas(k: dict) -> str:
    return f'<h2>{e(k.get("baslik"))}</h2>' if k.get("baslik") else ""


def kutu_grafik(k: dict) -> str:
    ciz = grafik_cizgi(k) if (k.get("tip") or "cizgi") == "cizgi" else grafik_sutun(k)
    efsane = "".join(
        f'<span class="efsane"><i style="background:{e(_seri_renk(s, i))}"></i>{e(s.get("ad"))}</span>'
        for i, s in enumerate(k.get("seriler") or []))
    alt = f'<p class="kaynak">{e(k.get("kaynak"))}</p>' if k.get("kaynak") else ""
    return f'{bas(k)}{ciz}<div class="efsane-satiri">{efsane}</div>{alt}'


def kutu_tablo(k: dict) -> str:
    basliklar = "".join(f"<th>{e(b)}</th>" for b in (k.get("basliklar") or []))
    satirlar = "".join(
        "<tr>" + "".join(f"<td>{e(sayi(h))}</td>" for h in satir) + "</tr>"
        for satir in (k.get("satirlar") or []))
    alt = f'<p class="kaynak">{e(k.get("kaynak"))}</p>' if k.get("kaynak") else ""
    return f'{bas(k)}<div class="tablo-kap"><table><thead><tr>{basliklar}</tr></thead><tbody>{satirlar}</tbody></table></div>{alt}'


def kutu_not(k: dict) -> str:
    tur = k.get("tur2") or "bilgi"
    ikon = {"uyari": "!", "bilgi": "i", "basari": "✓"}.get(tur, "i")
    return (f'<div class="not {e(tur)}"><div class="ikon">{e(ikon)}</div><div>'
            f'<strong>{e(k.get("baslik"))}</strong><p>{e(k.get("govde"))}</p></div></div>')


def kutu_alinti(k: dict) -> str:
    return (f'<blockquote><p>{e(k.get("govde"))}</p>'
            f'<footer>{e(k.get("baslik"))}</footer></blockquote>')


def kutu_kod(k: dict) -> str:
    return f'{bas(k)}<pre><code>{e(k.get("kod"))}</code></pre>'


def kutu(k: dict) -> str:
    tur = (k.get("tur") or "metin").lower()
    gen = {"tam": "g12", "yarim": "g6", "dar": "g4", "ucde": "g4", "ceyrek": "g3"}.get(k.get("genislik") or "", "")
    if tur == "metrik":
        ic = kutu_metrik(k)
        gen = gen or "g3"
    elif tur == "grafik":
        ic = kutu_grafik(k)
        gen = gen or "g12"
    elif tur == "tablo":
        ic = kutu_tablo(k)
        gen = gen or "g12"
    elif tur == "not":
        return f'<div class="{gen or "g12"}">{kutu_not(k)}</div>'
    elif tur == "alinti":
        ic = kutu_alinti(k)
        gen = gen or "g6"
    elif tur == "kod":
        ic = kutu_kod(k)
        gen = gen or "g12"
    elif tur == "maddeler":
        ic = kutu_metin(k)
        gen = gen or "g6"
    elif tur == "ayrac":
        return '<div class="ayrac g12"></div>'
    else:
        ic = kutu_metin(k)
        gen = gen or "g6"
    return f'<section class="kart {gen}">{ic}</section>'


# ── sayfa ─────────────────────────────────────────────────────────────────────────────────────────────────────
CSS = """
*{box-sizing:border-box}
:root{--zemin:%(zemin)s;--kart:%(kart)s;--cizgi:%(cizgi)s;--metin:%(metin)s;--soluk:%(soluk)s;--izgara:%(izgara)s;--ac:%(ac)s}
html[data-tema="koyu"]{--zemin:%(koyu_zemin)s;--kart:%(koyu_kart)s;--cizgi:%(koyu_cizgi)s;--metin:%(koyu_metin)s;--soluk:%(koyu_soluk)s;--izgara:%(koyu_izgara)s}
html,body{margin:0;padding:0;background:var(--zemin);color:var(--metin)}
body{font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
     -webkit-font-smoothing:antialiased;padding:28px clamp(16px,4vw,44px) 56px}
.kabuk{max-width:1160px;margin:0 auto}
header{display:flex;align-items:flex-start;gap:20px;margin:0 0 26px}
header .basliklar{flex:1;min-width:0}
h1{font-size:clamp(24px,3vw,34px);line-height:1.15;letter-spacing:-.02em;margin:0 0 6px}
.altbaslik{color:var(--soluk);font-size:16px;margin:0}
.ust-cizgi{height:3px;width:56px;background:var(--ac);border-radius:2px;margin:14px 0 0}
.araclar{display:flex;gap:8px;flex:none}
button{font:inherit;font-size:13px;color:var(--metin);background:var(--kart);border:1px solid var(--cizgi);
       border-radius:999px;padding:7px 14px;cursor:pointer}
button:hover{border-color:var(--ac)}
.izgara{display:grid;grid-template-columns:repeat(12,1fr);gap:14px}
.g12{grid-column:span 12}.g6{grid-column:span 6}.g4{grid-column:span 4}.g3{grid-column:span 3}
@media(max-width:900px){.g6,.g4,.g3{grid-column:span 12}}
.kart{background:var(--kart);border:1px solid var(--cizgi);border-radius:16px;padding:18px 18px 16px;min-width:0}
.kart h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--soluk);margin:0 0 12px;font-weight:600}
.kart p{margin:0 0 10px}.kart p:last-child{margin-bottom:0}
.metrik .etiket{font-size:13px;color:var(--soluk)}
.metrik .deger{font-size:clamp(28px,3.4vw,40px);font-weight:650;letter-spacing:-.03em;line-height:1.1;margin:6px 0 2px}
.metrik .birim{font-size:16px;font-weight:500;color:var(--soluk);margin-left:4px}
.metrik .alt{font-size:12.5px;color:var(--soluk);margin-top:4px}
.degisim{font-size:13px;font-weight:600;border-radius:999px;padding:2px 8px;display:inline-block}
.degisim.iyi{color:#1f6b45;background:rgba(47,111,79,.12)}
.degisim.kotu{color:#a13a2a;background:rgba(178,63,45,.12)}
.degisim.notr{color:var(--soluk);background:var(--izgara)}
ul.maddeler{margin:6px 0 0;padding-left:20px}ul.maddeler li{margin:5px 0}
.grafik{width:100%%;height:auto;display:block;margin:2px 0 6px}
.eksen{fill:var(--soluk);font-size:11px}
.efsane-satiri{display:flex;flex-wrap:wrap;gap:14px;margin-top:4px}
.efsane{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:var(--soluk)}
.efsane i{width:10px;height:10px;border-radius:3px;display:inline-block}
.tablo-kap{overflow-x:auto}
table{border-collapse:collapse;width:100%%;font-size:13.5px}
th{ text-align:left;font-weight:600;color:var(--soluk);font-size:12px;letter-spacing:.04em;text-transform:uppercase;
    border-bottom:1px solid var(--cizgi);padding:8px 10px}
td{padding:8px 10px;border-bottom:1px solid var(--izgara)}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--izgara)}
.kaynak{font-size:12px;color:var(--soluk);margin-top:8px}
.not{display:flex;gap:12px;background:var(--kart);border:1px solid var(--cizgi);border-left:3px solid var(--ac);
     border-radius:14px;padding:14px 16px}
.not .ikon{flex:none;width:22px;height:22px;border-radius:50%%;display:grid;place-items:center;font-size:12px;
           font-weight:700;color:#fff;background:var(--ac)}
.not.uyari{border-left-color:#b23f2d}.not.uyari .ikon{background:#b23f2d}
.not.basari{border-left-color:#2f6f4f}.not.basari .ikon{background:#2f6f4f}
.not strong{display:block;margin-bottom:2px}
.not p{margin:0;color:var(--soluk)}
blockquote{margin:0;padding:2px 0 2px 16px;border-left:3px solid var(--ac)}
blockquote p{font-size:17px;line-height:1.45}
blockquote footer{color:var(--soluk);font-size:13px;margin-top:8px}
pre{background:var(--izgara);border-radius:12px;padding:14px 16px;overflow:auto;margin:0;font-size:13px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.ayrac{height:1px;background:var(--cizgi);margin:8px 0}
.bos{color:var(--soluk)}
footer.sayfa{margin-top:32px;color:var(--soluk);font-size:12.5px;display:flex;gap:12px;flex-wrap:wrap}
@media print{body{padding:0;background:#fff}.araclar{display:none}.kart{break-inside:avoid;border-color:#ddd}}
""" % {
    **TEMA_RENK["acik"],
    "ac": "#2f6f4f",
    "koyu_zemin": TEMA_RENK["koyu"]["zemin"], "koyu_kart": TEMA_RENK["koyu"]["kart"],
    "koyu_cizgi": TEMA_RENK["koyu"]["cizgi"], "koyu_metin": TEMA_RENK["koyu"]["metin"],
    "koyu_soluk": TEMA_RENK["koyu"]["soluk"], "koyu_izgara": TEMA_RENK["koyu"]["izgara"],
}

JS = """
(function(){
  var h=document.documentElement, b=document.getElementById('tema');
  b.addEventListener('click',function(){
    var yeni=h.getAttribute('data-tema')==='koyu'?'acik':'koyu';
    h.setAttribute('data-tema',yeni); b.textContent=yeni==='koyu'?'Açık tema':'Koyu tema';
  });
  var y=document.getElementById('yazdir');
  if(y) y.addEventListener('click',function(){window.print();});
})();
"""


def sayfa(recete: dict, tema: str, ac: str) -> str:
    tema = (tema or recete.get("tema") or "acik").lower()
    ac = ac or recete.get("vurgu") or "#2f6f4f"
    css = CSS.replace("--ac:%s" % "#2f6f4f", "--ac:" + ac, 1)
    if tema == "koyu":
        css = css.replace('<html[data-tema="koyu"]', '<html[data-tema="acik"]', 1)
    kutular = "".join(kutu(k) for k in (recete.get("kutular") or []))
    alt = f'<p class="altbaslik">{e(recete.get("altbaslik"))}</p>' if recete.get("altbaslik") else ""
    etiket = recete.get("etiket") or ""
    ust = (f'<footer class="sayfa"><span>{e(etiket)}</span>'
           f'<span>MeDSor · Artifact stüdyosu</span></footer>')
    return f"""<!DOCTYPE html>
<html lang="tr" data-tema="{e(tema)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(recete.get("baslik") or "Artifact")}</title>
<style>{css}</style>
</head>
<body>
<div class="kabuk">
  <header>
    <div class="basliklar">
      <h1>{e(recete.get("baslik") or "Artifact")}</h1>
      {alt}
      <div class="ust-cizgi"></div>
    </div>
    <div class="araclar">
      <button id="tema" type="button">{'Açık tema' if tema == 'koyu' else 'Koyu tema'}</button>
      <button id="yazdir" type="button">Yazdır</button>
    </div>
  </header>
  <main class="izgara">
    {kutular}
  </main>
  {ust}
</div>
<script>{JS}</script>
</body>
</html>
"""


ORNEK = {
    "baslik": "Kurul 2 · İçerik hattı durumu",
    "altbaslik": "Ders işçisi son 7 gün — katman katman tamamlanma",
    "etiket": "Örnek reçete · artifact stüdyosu",
    "tema": "acik",
    "vurgu": "#2f6f4f",
    "kutular": [
        {"tur": "metrik", "etiket": "Tamamlanan ders", "deger": 18, "degisim": "+3", "yon": "artis", "alt": "hedef 24"},
        {"tur": "metrik", "etiket": "Kapı hatası", "deger": 0, "degisim": "0", "yon": "notr", "alt": "son çalıştırma"},
        {"tur": "metrik", "etiket": "Ortalama süre", "deger": 41, "birim": "dk", "alt": "ders başına"},
        {"tur": "metrik", "etiket": "Ses klibi", "deger": 1240, "alt": "EMA · GPU"},
        {"tur": "grafik", "baslik": "Günlük üretim", "tip": "sutun", "etiketler": ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"],
         "seriler": [{"ad": "Ders", "degerler": [2, 3, 3, 4, 5, 4, 3]},
                     {"ad": "Örnek soru", "eksen": "sag", "degerler": [40, 62, 58, 80, 96, 74, 51]}],
         "kaynak": "otomasyon/hat.json → durum.json"},
        {"tur": "metin", "baslik": "Bu hafta", "genislik": "yarim",
         "govde": "Kurul 2 dersleri tam otomatik hattan geçti; tüm kapılar sıfır hatayla kapandı.",
         "maddeler": ["Sesli ders + örnek soru çözücü", "Hoca soruları ve ara soru katmanı", "Çıkmış eşlemesi doğrulandı"]},
        {"tur": "not", "tur2": "uyari", "baslik": "Elle komut kilidi", "govde": "LLM aşamaları yalnız kullanıcı komutuyla başlar (kural 20).", "genislik": "yarim"},
        {"tur": "tablo", "baslik": "Katman durumu", "basliklar": ["Katman", "Durum", "Not"],
         "satirlar": [["Anlatım", "Tamam", "metin_denetle 0 HATA"], ["Ses", "Tamam", "EMA · GPU"], ["Çizim", "Tamam", "çapa + çizim kapısı"], ["Öğren destesi", "Atlandı", "kullanıcı kararı"]],
         "kaynak": "DEGISIKLIK_KAYDI.md"},
        {"tur": "alinti", "govde": "Yalnız kaynağa dayanan içerik öğrenciye güven verir.", "baslik": "İçerik ilkesi", "genislik": "yarim"},
        {"tur": "kod", "baslik": "Tek komut", "kod": "python3 meds/scripts/artifact_studio/studyo.py recete.json"},
    ],
}

SEMA = {
    "baslik": "sayfa başlığı", "altbaslik": "alt başlık", "etiket": "üst bilgi", "tema": "acik|koyu", "vurgu": "#2f6f4f",
    "kutular": [
        {"tur": "metrik", "etiket": "ad", "deger": 42, "birim": "%", "degisim": "+2,1", "yon": "artis|azalis|notr", "alt": "alt yazı", "genislik": "dar"},
        {"tur": "metin", "baslik": "başlık", "govde": "paragraf", "maddeler": ["madde"], "genislik": "yarim"},
        {"tur": "grafik", "baslik": "başlık", "tip": "cizgi|sutun", "etiketler": ["Ocak"],
         "seriler": [{"ad": "seri", "renk": "#2f6f4f", "eksen": "sol|sag", "degerler": [1, 2]}], "kaynak": "kaynak"},
        {"tur": "tablo", "baslik": "başlık", "basliklar": ["A"], "satirlar": [["1"]], "kaynak": "kaynak"},
        {"tur": "not", "tur2": "uyari|bilgi|basari", "baslik": "başlık", "govde": "metin"},
        {"tur": "alinti", "govde": "alıntı", "baslik": "kaynak kişi"},
        {"tur": "kod", "baslik": "başlık", "kod": "kod"},
        {"tur": "ayrac"},
    ],
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Artifact stüdyosu — JSON reçeteden tek dosyalık HTML üretir")
    ap.add_argument("recete", nargs="?", help="reçete JSON yolu (- = stdin)")
    ap.add_argument("-o", "--cikti", help="çıktı .html yolu (varsayılan artifact_studio/cikti/<slug>.html)")
    ap.add_argument("--tema", choices=["acik", "koyu"], help="tema (reçetedekini ezer)")
    ap.add_argument("--ac", help="vurgu rengi (#rrggbb)")
    ap.add_argument("--ornek", action="store_true", help="örnek reçeteyi üret ve sayfayı yaz")
    ap.add_argument("--ornek-recete", nargs="?", const="", help="örnek reçeteyi JSON olarak yaz (varsayılan ornek.json)")
    ap.add_argument("--sema", action="store_true", help="reçete şemasını JSON olarak yaz")
    ap.add_argument("--surum", action="store_true", help="sürümü yaz")
    a = ap.parse_args(argv)

    if a.surum:
        print(SURUM)
        return 0
    if a.sema:
        print(json.dumps(SEMA, ensure_ascii=False, indent=2))
        return 0

    if a.ornek_recete is not None:
        yol = Path(a.ornek_recete) if a.ornek_recete else Path(__file__).resolve().parent / "ornek.json"
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(json.dumps(ORNEK, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(yol.resolve())
        return 0

    if a.ornek:
        recete = ORNEK
    elif not a.recete:
        ap.error("reçete yolu ya da --ornek gerekir")
    elif a.recete == "-":
        try:
            recete = json.load(sys.stdin)
        except json.JSONDecodeError as ex:
            print(f"HATA: stdin geçerli JSON değil: {ex}", file=sys.stderr)
            return 1
    else:
        p = Path(a.recete)
        if not p.exists():
            print(f"HATA: reçete bulunamadı: {p}", file=sys.stderr)
            return 1
        try:
            recete = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as ex:
            print(f"HATA: {p} geçerli JSON değil: {ex}", file=sys.stderr)
            return 1
    if not isinstance(recete, dict) or not isinstance(recete.get("kutular"), list):
        print("HATA: reçete bir nesne ve 'kutular' dizisi olmalı (--sema)", file=sys.stderr)
        return 1

    ad = str(recete.get("dosya") or recete.get("baslik") or "artifact").translate(TR_HARF).lower()
    ad = re.sub(r"-{2,}", "-", "".join(c if c.isalnum() or c in "-_" else "-" for c in ad)).strip("-")[:60] or "artifact"
    cikti = (Path(a.cikti) if a.cikti else VARSAYILAN_CIKTI / (ad + ".html")).with_suffix(".html")
    try:
        cikti.parent.mkdir(parents=True, exist_ok=True)
        cikti.write_text(sayfa(recete, a.tema or "", a.ac or ""), encoding="utf-8")
    except OSError as ex:
        print(f"HATA: çıktı yazılamadı ({cikti}): {ex}", file=sys.stderr)
        return 1
    print(cikti.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
