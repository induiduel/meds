#!/usr/bin/env python3
"""Sesli anlatım metni denetleyicisi: biçim, uzunluk, telaffuz tuzakları.

Kullanım: metin_denetle.py <metin.md> [...]   → HATA sayısı 0 ise çıkış kodu 0.
"""
import re, sys
from pathlib import Path

MIN_W, MAX_W = 1150, 6000
WPM = 112

def denetle(p: Path):
    hatalar, uyarilar = [], []
    t = p.read_text(encoding='utf-8')
    lines = t.splitlines()
    if not lines or not lines[0].startswith('# '):
        hatalar.append('ilk satır "# Başlık" olmalı')
    bolum = [l for l in lines if l.startswith('@@ ')]
    if not (6 <= len(bolum) <= 30):
        uyarilar.append(f'bölüm sayısı {len(bolum)} (önerilen 8–25)')
    body = [l for l in lines[1:] if not l.startswith('@@ ')]
    text = '\n'.join(body)
    words = len(text.split())
    if words < MIN_W: hatalar.append(f'kelime {words} < {MIN_W}')
    if words > MAX_W: hatalar.append(f'kelime {words} > {MAX_W}')
    for i, l in enumerate(lines, 1):
        if l.startswith(('# ', '@@ ')) or not l.strip():
            continue
        if re.search(r'[*#|>\[\]{}=_`~]', l): hatalar.append(f'{i}: markdown/simge: {l[:70]}')
        if re.match(r'\s*[-•–]\s', l): hatalar.append(f'{i}: madde imi: {l[:70]}')
        if re.search(r'\d', l): hatalar.append(f'{i}: rakam (yazıyla yaz): {re.findall(r".{0,15}\d+.{0,10}", l)[0]}')
        if re.search(r'[%↑↓→←±≈≥≤×/+<⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉]', l): hatalar.append(f'{i}: simge (yazıyla yaz): {l[:70]}')
        if re.search(r'[αβγδκλμθπσΔ]', l): hatalar.append(f'{i}: Yunan harfi (alfa, beta…): {l[:70]}')
        if re.search(r'[()]', l): uyarilar.append(f'{i}: parantez')
        m = re.findall(r'\b[A-ZÇĞİÖŞÜ]{2,}[a-z]*\b', l)
        if m: hatalar.append(f'{i}: kısaltma/Roma rakamı okunuşuyla yazılmalı: {", ".join(sorted(set(m)))}')
        if re.search(r'https?:|www\.', l): hatalar.append(f'{i}: URL')
    for kalip in ('merhaba', 'teşekkür ederim', 'dinlediğiniz için', 'bu derste şunları', 'kaynakça'):
        if kalip in text.lower(): uyarilar.append(f'giriş/kapanış kalıbı: "{kalip}"')
    paras = [x for x in re.split(r'\n\s*\n', text) if x.strip()]
    for x in paras:
        n = len(x.split())
        if n > 200: uyarilar.append(f'uzun paragraf ({n} kelime): {x[:50]}…')
    onemli = len(re.findall(r'[Bb]urası önemli', text))
    print(f'{p.name}: {words} kelime ≈ {words / WPM:.0f} dk, {len(bolum)} bölüm, {len(paras)} paragraf, "Burası önemli" {onemli}')
    for h in hatalar[:60]: print('  HATA', h)
    if len(hatalar) > 60: print(f'  … {len(hatalar) - 60} hata daha')
    for u in uyarilar[:20]: print('  uyarı', u)
    print(f'  {len(hatalar)} HATA, {len(uyarilar)} uyarı')
    return len(hatalar)

if __name__ == '__main__':
    toplam = sum(denetle(Path(a)) for a in sys.argv[1:])
    sys.exit(1 if toplam else 0)
