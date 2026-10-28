#!/usr/bin/env python3
"""Sesli anlatım metni denetleyicisi: biçim, uzunluk, telaffuz tuzakları.

Kullanım: metin_denetle.py [--yazim] <metin.md> [...]
--yazim: metin kısaltmaları yazımla tutar (CD2, IL-2); rakam/kısaltma/Yunan denetimi EMA'ya giden okunuşa
(modul_okunus.donustur) uygulanır (KURUL2_YAPILMAYACAK_HATALAR H23).   → HATA sayısı 0 ise çıkış kodu 0.
"""
import re, sys
from pathlib import Path

MIN_W, MAX_W = 1150, 6000
WPM = 112
# Kurul 2+ dolgu ve asılsız vurgu kalıpları (kullanıcı kuralı 2026-10-22, H22)
DOLGU = (
    r'hoca(mız)?\s+(bunu\s+|burayı\s+|bu\s+noktayı\s+)?(özellikle\s+|ayrıca\s+|bilhassa\s+)?(vurgula|altını\s+çiz|işaretle|üzerinde\s+dur)',
    r'hocanın\s+(özellikle\s+)?(vurgu|altını\s+çiz|işaret)',
    r'tekrar\s+etmekte\s+fayda', r'bir\s+kez\s+daha\s+hatırlatalım', r'şimdi\s+gelelim',
    r'daha\s+önce\s+de\s+söylediğimiz\s+gibi', r'özetlemek\s+gerekirse', r'sözü\s+uzatmadan',
)

# Kaçamak meta cümle (H127, 2026-10-28): şekil/kavram anlatılmadan "ders yorumuna girmez" diye geçmek
KACAMAK = (
    r'\bders(?:te|in)?\b[^.]{0,60}\b(girmez|vermez|anlatmaz|değinmez|açıklamaz|ayrıntılandırmaz|belirtmez)\b',
    r'\byalnız(?:ca)?\s+ad(?:ı|ını|larını)\s+(?:verir|sayar|geçer)',
    r'\b(?:slayt|şekil|çizim|resim|fotoğraf|görsel)(?:ta|te|da|de)?\b[^.]{0,40}\b(?:ayrıntı|yorum)[^.]{0,20}\b(?:yok|verilmez|yer\s+almaz)',
)
SEKIL_RE = r'\b(çizim|şekil|resim|fotoğraf|görsel|panel)'
BETIM_RE = r'(gösterilir|görülür|yer alır|gösterir)[.!?]?$'

YAZIM = False


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
    # Alt sınır hedef değil: kısa ama eksiksiz metin geçer; dolguyla uzatmak yasak (KURUL2_YAPILMAYACAK_HATALAR H22).
    if words < MIN_W: uyarilar.append(f'kelime {words} < {MIN_W} — eksik konu yoksa sorun değil, dolguyla uzatma')
    if words > MAX_W: hatalar.append(f'kelime {words} > {MAX_W}')
    for i, l in enumerate(lines, 1):
        if l.startswith(('# ', '@@ ')) or not l.strip():
            continue
        if YAZIM:
            import modul_okunus
            l = modul_okunus.donustur(l)
        if re.search(r'[*#|>\[\]{}=_`~]', l): hatalar.append(f'{i}: markdown/simge: {l[:70]}')
        if re.match(r'\s*[-•–]\s', l): hatalar.append(f'{i}: madde imi: {l[:70]}')
        if re.search(r'\d', l):
            ornek = re.findall(r".{0,15}\d+.{0,10}", l)[0]
            hatalar.append(f'{i}: rakam (yazıyla yaz): {ornek}')
        if re.search(r'[%↑↓→←±≈≥≤×/+<⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉]', l): hatalar.append(f'{i}: simge (yazıyla yaz): {l[:70]}')
        if re.search(r'[αβγδκλμθπσΔ]', l): hatalar.append(f'{i}: Yunan harfi (alfa, beta…): {l[:70]}')
        if re.search(r'[()]', l): uyarilar.append(f'{i}: parantez')
        m = re.findall(r'\b[A-ZÇĞİÖŞÜ]{2,}[a-z]*\b', l)
        if m: hatalar.append(f'{i}: kısaltma/Roma rakamı okunuşuyla yazılmalı: {", ".join(sorted(set(m)))}')
        if re.search(r'https?:|www\.', l): hatalar.append(f'{i}: URL')
    for kalip in ('merhaba', 'teşekkür ederim', 'dinlediğiniz için', 'bu derste şunları', 'kaynakça'):
        if kalip in text.lower(): uyarilar.append(f'giriş/kapanış kalıbı: "{kalip}"')
    # H22: asılsız "hoca vurguladı" meta cümleleri ve süre/kelime dolgusu yasak.
    low = text.lower()
    for kalip in DOLGU:
        for m in re.finditer(kalip, low):
            hatalar.append(f'dolgu/asılsız vurgu: "{low[max(0, m.start() - 25):m.end() + 25].strip()}"')
    onemli_n = len(re.findall(r'burası önemli|sınavda sık|çok önemli', low))
    if onemli_n > max(3, len(bolum) // 2):
        hatalar.append(f'önem vurgusu {onemli_n} kez — yalnız çıkmış/öğrenci notu dayanaklı kritik noktalarda kullan')
    paras = [x for x in re.split(r'\n\s*\n', text) if x.strip()]
    # H127: kaçamak meta cümle (HATA) ve yalnız betimlenmiş kısa şekil paragrafı (UYARI)
    for kalip in KACAMAK:
        for m in re.finditer(kalip, low):
            hatalar.append(f'kaçamak meta cümle (H127 — şekli/kavramı anlat): "{low[max(0, m.start() - 20):m.end() + 20].strip()}"')
    for x in paras:
        n = len(x.split())
        if n > 200: uyarilar.append(f'uzun paragraf ({n} kelime): {x[:50]}…')
        cs = [c for c in re.split(r'(?<=[.!?])\s+', x.strip()) if c.strip()]
        if n < 45 and re.search(SEKIL_RE, x, re.I) and cs and all(re.search(BETIM_RE, c.strip()) for c in cs):
            uyarilar.append(f'şekil yalnız betimlenmiş (H127 — ne sınar, sonuçlar, paneller): {x[:70]}…')
    onemli = len(re.findall(r'[Bb]urası önemli', text))
    print(f'{p.name}: {words} kelime ≈ {words / WPM:.0f} dk, {len(bolum)} bölüm, {len(paras)} paragraf, "Burası önemli" {onemli}')
    for h in hatalar[:60]: print('  HATA', h)
    if len(hatalar) > 60: print(f'  … {len(hatalar) - 60} hata daha')
    for u in uyarilar[:20]: print('  uyarı', u)
    print(f'  {len(hatalar)} HATA, {len(uyarilar)} uyarı')
    return len(hatalar)

if __name__ == '__main__':
    YAZIM = '--yazim' in sys.argv
    toplam = sum(denetle(Path(a)) for a in sys.argv[1:] if a != '--yazim')
    sys.exit(1 if toplam else 0)
