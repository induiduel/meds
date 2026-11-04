#!/usr/bin/env python3
"""Sesli ders ara resim (mekanizma resmi) kapısı — meds/docs/ARA_RESIM_KURALLARI.md.

Kullanım: python3 meds/scripts/ara_resim/dogrula.py <ders key> [--kok <meds dizini>]
Denetler: şema, id tekilliği, SVG var + XML + viewBox + metin ögesi + güvenlik (script/harici href/foreignObject yok),
paragraf ≤ bitis ve v2 paragraf sayısı içinde, kaynak sayfalar 1..PDF sayfa sayısı, aralık çakışması, Türkçe üslup.
Çıkış: "N HATA, M UYARI"; HATA varsa çıkış kodu 1.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from turkce_uslup import denetle as uslup  # noqa: E402

SVG_NS = '{http://www.w3.org/2000/svg}'
XLINK = '{http://www.w3.org/1999/xlink}href'
ID_RE = re.compile(r'^[a-z0-9][a-z0-9_-]{0,40}$')
SVG_AD_RE = re.compile(r'^[a-z0-9][a-z0-9_.-]{0,60}\.svg$')


def yerel(etiket):
    return etiket.split('}', 1)[-1].lower() if isinstance(etiket, str) else ''


def svg_denetle(yol, yer, h, u):
    try:
        kok = ET.parse(yol).getroot()
    except ET.ParseError as e:
        h.append(f'{yer}: SVG XML olarak ayrışmıyor ({e})'); return
    if yerel(kok.tag) != 'svg':
        h.append(f'{yer}: kök öge <svg> değil'); return
    vb = (kok.get('viewBox') or '').replace(',', ' ').split()
    if len(vb) != 4:
        h.append(f'{yer}: viewBox yok ya da bozuk')
    else:
        try:
            if float(vb[2]) <= 0 or float(vb[3]) <= 0: h.append(f'{yer}: viewBox genişlik/yükseklik sıfır')
        except ValueError:
            h.append(f'{yer}: viewBox sayısal değil')
    metin = []
    for el in kok.iter():
        ad = yerel(el.tag)
        if ad == 'script': h.append(f'{yer}: <script> yasak')
        if ad == 'foreignobject': h.append(f'{yer}: <foreignObject> yasak')
        for k, v in el.attrib.items():
            kk = yerel(k) if k.startswith('{') else k.lower()
            if kk.startswith('on'): h.append(f'{yer}: olay özniteliği yasak ({k})')
            if kk == 'href' or k == XLINK:
                if not v.strip().startswith('#'): h.append(f'{yer}: harici bağlantı yasak ({v[:60]})')
            if 'url(' in v and not re.search(r'url\(\s*#', v): h.append(f'{yer}: harici url() yasak')
        if ad == 'style' and el.text and re.search(r'@import|url\(\s*[\'"]?(?!#)', el.text):
            h.append(f'{yer}: <style> içinde harici kaynak yasak')
        if ad in ('text', 'tspan', 'textpath'):
            t = ''.join(el.itertext()).strip() if ad == 'text' else ''
            if t: metin.append(t)
    if not metin:
        h.append(f'{yer}: hiç metin ögesi (<text>) yok — resim Türkçe etiketlerle okunmalı')
    toplam = ' '.join(metin)
    n = len(re.findall(r'\w+', toplam))
    if n > 60: h.append(f'{yer}: SVG içi metin {n} kelime (en çok ~40; resim slayt kopyası olmamalı)')
    elif n > 40: u.append(f'{yer}: SVG içi metin {n} kelime (hedef ≤40)')
    for t in metin: h.extend(uslup(t, f'{yer} <text>'))
    # okunabilirlik: font-size < 14 (viewBox birimiyle, genişlik ≈1000 varsayımı) uyarı
    for el in kok.iter():
        fs = el.get('font-size') or (re.search(r'font-size\s*:\s*([\d.]+)', el.get('style') or '') or [None, None])[1]
        try:
            if fs and len(vb) == 4 and float(re.sub(r'px$', '', str(fs))) * 1000 / float(vb[2]) < 14:
                u.append(f'{yer}: font-size {fs} (viewBox {vb[2]} genişliğinde ≈ {float(re.sub(r"px$", "", str(fs))) * 1000 / float(vb[2]):.0f}/1000) küçük; ≥14 px eşdeğeri'); break
        except ValueError:
            pass


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('key')
    ap.add_argument('--kok', default=str(Path(__file__).resolve().parents[2]))
    a = ap.parse_args()
    kok = Path(a.kok)
    h, u = [], []
    veri_yol = kok / 'src/data/ara_resim' / f'{a.key}.json'
    if not veri_yol.exists():
        print(f'HATA: {veri_yol} yok'); print('1 HATA, 0 UYARI'); return 1
    try:
        veri = json.loads(veri_yol.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f'HATA: JSON bozuk ({e})'); print('1 HATA, 0 UYARI'); return 1
    if veri.get('key') != a.key: h.append(f'key alanı {veri.get("key")!r} ≠ {a.key!r}')
    resimler = veri.get('resimler')
    if not isinstance(resimler, list) or not resimler:
        h.append('resimler boş ya da dizi değil'); resimler = []
    if len(resimler) > 12: u.append(f'{len(resimler)} resim (tipik 4–10)')

    # paragraf sayısı ve PDF sayfa sayısı
    n_par = None
    v2 = kok / 'data/sesli_anlatim/v2' / f'{a.key}.json'
    if v2.exists():
        d = json.loads(v2.read_text(encoding='utf-8'))
        n_par = sum(len(b.get('paragraflar') or []) for b in d.get('bolumler') or [])
    else:
        h.append(f'v2 dosyası yok: {v2}')
    n_sayfa = None
    hz = kok / 'data/sesli_anlatim/hizalama' / f'{a.key}.json'
    if hz.exists():
        try: n_sayfa = int(json.loads(hz.read_text(encoding='utf-8'))['dosyalar'][0]['pages'])
        except (KeyError, IndexError, TypeError, ValueError): u.append('hizalama dosyasında dosyalar[0].pages yok; kaynak sayfa denetlenmedi')
    else:
        u.append(f'hizalama dosyası yok ({hz.name}); kaynak sayfa denetlenmedi')

    gorulen, araliklar = set(), []
    for i, r in enumerate(resimler):
        yer = f'resimler[{i}]'
        if not isinstance(r, dict): h.append(f'{yer}: nesne değil'); continue
        rid = r.get('id')
        if not isinstance(rid, str) or not ID_RE.match(rid): h.append(f'{yer}: id geçersiz ({rid!r})')
        elif rid in gorulen: h.append(f'{yer}: id tekrar ({rid})')
        gorulen.add(rid); yer = f'{rid}'
        for alan in ('baslik', 'aciklama'):
            v = r.get(alan)
            if not isinstance(v, str) or not v.strip(): h.append(f'{yer}: {alan} boş')
            else: h.extend(uslup(v, f'{yer}.{alan}'))
        if isinstance(r.get('baslik'), str) and len(r['baslik']) > 90: u.append(f'{yer}: başlık uzun ({len(r["baslik"])} karakter)')
        if isinstance(r.get('aciklama'), str) and len(re.findall(r'\w+', r['aciklama'])) > 45: u.append(f'{yer}: alt yazı 1–2 cümleyi aşıyor')
        ad = r.get('adimlar')
        if ad is not None:
            if not isinstance(ad, list) or not all(isinstance(x, str) and x.strip() for x in ad): h.append(f'{yer}: adimlar dizgi dizisi değil')
            else:
                if len(ad) > 6: h.append(f'{yer}: adimlar en çok 6 ({len(ad)})')
                for j, x in enumerate(ad): h.extend(uslup(x, f'{yer}.adimlar[{j}]'))
        p, b = r.get('paragraf'), r.get('bitis', r.get('paragraf'))
        if not isinstance(p, int) or not isinstance(b, int) or isinstance(p, bool) or isinstance(b, bool):
            h.append(f'{yer}: paragraf/bitis tamsayı değil')
        else:
            if p < 0 or b < p: h.append(f'{yer}: paragraf ({p}) ≤ bitis ({b}) değil')
            if n_par is not None and b >= n_par: h.append(f'{yer}: bitis {b} paragraf sayısının ({n_par}) dışında')
            if b - p > 8: u.append(f'{yer}: aralık {b - p + 1} paragraf — resim uzun süre slaytın önünde kalır')
            araliklar.append((p, b, yer))
        k = r.get('kaynak')
        if k is None or k == []: u.append(f'{yer}: kaynak sayfa yok (slayt kaynaklı olmalı)')
        elif not isinstance(k, list) or not all(isinstance(x, int) and not isinstance(x, bool) for x in k): h.append(f'{yer}: kaynak tamsayı dizisi değil')
        elif n_sayfa and any(x < 1 or x > n_sayfa for x in k): h.append(f'{yer}: kaynak sayfa 1..{n_sayfa} dışında ({k})')
        svg = r.get('svg')
        if not isinstance(svg, str) or not SVG_AD_RE.match(svg): h.append(f'{yer}: svg dosya adı geçersiz ({svg!r})')
        else:
            sy = kok / 'public/ara_resim' / a.key / svg
            if not sy.exists(): h.append(f'{yer}: SVG yok ({sy})')
            else:
                if sy.stat().st_size > 400_000: u.append(f'{yer}: SVG büyük ({sy.stat().st_size // 1024} KB)')
                svg_denetle(sy, f'{yer} ({svg})', h, u)
    araliklar.sort()
    for (p1, b1, y1), (p2, b2, y2) in zip(araliklar, araliklar[1:]):
        if p2 <= b1: h.append(f'{y1} [{p1}–{b1}] ile {y2} [{p2}–{b2}] aralıkları çakışıyor')

    for x in h: print('HATA:', x)
    for x in u: print('UYARI:', x)
    print(f'{len(h)} HATA, {len(u)} UYARI')
    return 1 if h else 0


if __name__ == '__main__':
    sys.exit(main())
