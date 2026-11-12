#!/usr/bin/env python3
"""PDF basım kapısı (H556, 2026-11-13).

Belirti: soru çıktısı / soru dışa aktarımı / ek modül föyü "PDF indir"de
"Veri göndermek veya değiştirmek için X-API-Password başlığı gereklidir." hatası veriyordu.
Kök neden: `/api/pdf/render` yalnız gönderilen HTML'i PDF'e basan bir belge ucudur (veri yazmaz), ama
`server.ts`teki yazma parolası ara katmanının öğrenci beyaz listesinde (`STUDENT_WRITE_ROUTES`) yoktu;
öğrenciye parola verilmediği için her istek 401 dönüyordu. Canlı imajda başsız tarayıcı da yoktu
(`pdf/status` → available:false), yani parola geçse bile basım çalışmazdı.

Kapı (sunucu ayakta iken):
  1. `/api/pdf/status` → available true (sunucuda başsız tarayıcı var),
  2. dış istemci gibi (`cf-connecting-ip` başlıklı) `/api/pdf/render` → parolasız 200 ve `%PDF` imzası.

Kullanım: python3 scripts/kapilar/pdf_basim_kapisi.py [--sunucu http://localhost:3000]
"""
import argparse
import json
import sys
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument('--sunucu', default='http://localhost:3000')
a = ap.parse_args()

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1'
YEREL = 'localhost' in a.sunucu or '127.0.0.1' in a.sunucu
# Yerelde dış istemci benzetimi: yönetici loopback'i sayılmasın diye `cf-connecting-ip` basılır (yoksa kapı,
# öğrencinin yolunu sınamaz). Canlıda bu başlık GÖNDERİLMEZ: Cloudflare istemcinin yazdığı `cf-connecting-ip`i
# sahte sayıp 403 (error 1000) veriyor; zaten canlıda Cloudflare gerçek başlığı kendisi ekliyor, sunucu isteği
# loopback saymıyor. User-Agent da bot korumasına takılmamak için tarayıcı gibi.
BASLIKLAR = {'Content-Type': 'application/json', 'User-Agent': UA}
if YEREL:
    BASLIKLAR['cf-connecting-ip'] = '203.0.113.9'
GOVDE = json.dumps({
    'html': '<html><head><style>@page{size:A4}</style></head><body><h1>Kapı sınaması</h1></body></html>',
    'title': 'kapı sınaması',
    'fileName': 'kapi.pdf',
}).encode()

hata = 0


def hata_yaz(mesaj: str) -> None:
    global hata
    hata += 1
    print(f'HATA {mesaj}')


try:
    durum = json.load(urllib.request.urlopen(
        urllib.request.Request(f'{a.sunucu}/api/pdf/status', headers={'User-Agent': UA}),
        timeout=30))
except Exception as e:  # noqa: BLE001
    hata_yaz(f'pdf/status okunamadı: {e}')
    durum = {}

if not durum.get('available'):
    hata_yaz('sunucuda başsız tarayıcı (Chrome/Chromium) yok: PDF basılamaz '
             '(meds-web: CHROME_PATH/chromium kurulu olmalı; Oracle imajı Dockerfile.oracle)')

istek = urllib.request.Request(f'{a.sunucu}/api/pdf/render', data=GOVDE, headers=BASLIKLAR, method='POST')
try:
    with urllib.request.urlopen(istek, timeout=120) as r:
        kod = r.status
        govde = r.read(2048)
        tur = r.headers.get('content-type', '')
except urllib.error.HTTPError as e:
    kod, govde, tur = e.code, e.read()[:400], e.headers.get('content-type', '')
    if kod == 401:
        hata_yaz('/api/pdf/render öğrenciye kapalı (401 X-API-Password): uç STUDENT_WRITE_ROUTES beyaz listesine eklenmeli')
    else:
        hata_yaz(f'/api/pdf/render HTTP {kod}: {govde.decode("utf-8", "ignore")[:200]}')
except Exception as e:  # noqa: BLE001
    kod, govde, tur = 0, b'', ''
    hata_yaz(f'/api/pdf/render isteği başarısız: {e}')

if kod == 200:
    if not tur.startswith('application/pdf') or not govde.startswith(b'%PDF'):
        hata_yaz(f'yanıt PDF değil (content-type={tur!r}, imza={govde[:8]!r})')

if hata:
    print(f'{hata} HATA')
    sys.exit(1)
print('0 HATA — PDF basımı parolasız ve tarayıcı hazır')
