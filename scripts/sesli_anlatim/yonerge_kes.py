#!/usr/bin/env python3
"""Gemini varyantında her parçanın başında sesli okunmuş üslup yönergesini keser (yeniden ücret ödemeden onarım).

Kullanım: yonerge_kes.py <key> <vid> [--kuru]
- Parça sınırları: metin → Gemini parçaları (sunucudaki metniParcala ile aynı kural, sınır 3000) + varyantın zamanlaması.
- Kesim: parçanın konuşma başından itibaren beklenen yönerge süresine en yakın sessizlik; ücretsiz anahtarla
  kesim sonrası ilk ~10 sn yazıya dökülür ve parçanın gerçek ilk cümlesiyle karşılaştırılır (doğrulanmazsa sıradaki aday).
- Çıktı: aynı vid dosyası yerine yazılır (eskisi .yedek.mp3), kayit.json'da sureSn/bayt/zamanlama güncellenir.
"""
import base64, io, json, os, re, subprocess, sys, unicodedata, urllib.request, wave
from pathlib import Path
import struct

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / 'data' / 'sesli_anlatim'
FF = os.environ.get('FFMPEG') or '/tmp/claude-1000/-home-indu-medsor/5af3e86e-9219-4c43-b962-ca6e1550adee/scratchpad/ttsenv/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
SR = 24000
YONERGE = ('Aşağıdaki Türkçe tıp dersi anlatımını, deneyimli bir kadın patoloji hocası gibi sıcak, net ve öğretici bir tonda, '
           'normalden yüzde on kadar hızlı ve akıcı bir tempoda, tıbbi terimleri özenle ve doğru telaffuz ederek oku. '
           'Metni değiştirme, hiçbir şey ekleme ya da atlama, bu yönergeyi okuma:')
SINIR = 3000


def env():
    e = {}
    for line in open(MEDS / '.env', encoding='utf-8'):
        if '=' in line and not line.startswith('#'):
            k, v = line.rstrip('\n').split('=', 1)
            e[k] = v
    return e


def paragraflar(md):
    out, bolum, tampon = [], True, []
    def bitir():
        nonlocal bolum, tampon
        t = re.sub(r'\s+', ' ', ' '.join(tampon)).strip()
        if t:
            out.append((t, bolum)); bolum = False
        tampon = []
    for s in md.splitlines():
        if s.startswith('# '): continue
        if s.startswith('@@'):
            bitir(); bolum = True; continue
        if not s.strip(): bitir()
        else: tampon.append(s.strip())
    bitir()
    return out


def parcalar(pars):
    ch, cur = [], None
    for idx, (t, b) in enumerate(pars):
        uzun = len('\n'.join(x for x, _ in cur['p'])) + len(t) if cur else 0
        if not cur or b or uzun > SINIR:
            if cur: ch.append(cur)
            cur = {'p': [(t, b)], 'idx': [idx], 'bolum': b}
        else:
            cur['p'].append((t, b)); cur['idx'].append(idx)
    if cur: ch.append(cur)
    return ch


BIR = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
ON = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
def sayi(n):
    if n == 0: return 'sıfır'
    uc = lambda x: ((BIR[x // 100] if x >= 200 else '') + 'yüz' if x >= 100 else '') + ON[(x % 100) // 10] + BIR[x % 10]
    m, b, k = n // 10**6, (n % 10**6) // 1000, n % 1000
    return (uc(m) + 'milyon' if m else '') + ((uc(b) if b > 1 else '') + 'bin' if b else '') + uc(k)


def harf(t):
    t = re.sub(r'%\s*(\d+)', r' yüzde \1 ', t)
    t = re.sub(r'(\d+)[.,](\d+)', lambda m: f' {m.group(1)} virgül {m.group(2)} ', t)
    t = re.sub(r'\d+', lambda m: ' ' + (sayi(int(m.group())) if len(m.group()) <= 9 else m.group()) + ' ', t)
    t = unicodedata.normalize('NFD', t.lower().replace('I', 'ı'))
    t = re.sub(r'[̀-ͯ]', '', t).replace('ı', 'i')
    return re.sub(r'[^a-z]', '', t)


def lcs_oran(a, b):
    if not a: return 1.0
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b, 1):
            cur[j] = prev[j - 1] + 1 if ca == cb else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1] / len(a)


def coz(mp3):
    r = subprocess.run([FF, '-v', 'error', '-i', str(mp3), '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True)
    n = len(r.stdout) // 2
    return list(struct.unpack('<%dh' % n, r.stdout[:n * 2]))


def wav_b64(pcm):
    b = io.BytesIO(); w = wave.open(b, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(struct.pack('<%dh' % len(pcm), *pcm)); w.close()
    return base64.b64encode(b.getvalue()).decode()


ANAHTARLAR = []
def dokum(pcm):
    body = json.dumps({'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': wav_b64(pcm)}},
                                               {'text': 'Bu Türkçe ses kaydını kelimesi kelimesine yazıya dök. Yalnız dökümü yaz.'}]}],
                       'generationConfig': {'temperature': 0, 'maxOutputTokens': 1000}}).encode()
    for model in ('gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-2.5-flash-lite'):
        for ad, k in ANAHTARLAR:
            req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                                         data=body, headers={'Content-Type': 'application/json', 'x-goog-api-key': k})
            try:
                d = json.load(urllib.request.urlopen(req, timeout=120))
                t = ' '.join(p.get('text', '') for p in d['candidates'][0]['content']['parts'])
                if t.strip(): return t
            except Exception:
                continue
    return None


def sessizlikler(pcm, bas, son, esik=350, min_sn=0.16):
    """[bas, son) örnek aralığında sessiz bölgeler: (başlangıç, bitiş) örnek."""
    pen = 480; out = []; i = bas; run = None
    while i < son:
        w = pcm[i:i + pen]
        m = max((abs(x) for x in w), default=0)
        if m < esik:
            run = run if run is not None else i
        else:
            if run is not None and i - run >= min_sn * SR: out.append((run, i))
            run = None
        i += pen
    if run is not None and son - run >= min_sn * SR: out.append((run, son))
    return out


def main():
    key, vid = sys.argv[1], sys.argv[2]
    kuru = '--kuru' in sys.argv
    e = env()
    ANAHTARLAR.extend([(k, v) for k, v in e.items() if re.match(r'^(TTS_FREE_GEMINI_KEY_\d+|GEMINI_API_KEY|GEMINI_FREE_KEY_\d+)$', k) and v])
    kayit = json.load(open(KOK / 'kayit.json'))
    v = next(x for x in kayit[key] if x['id'] == vid)
    zam = v['zamanlama']
    md = open(KOK / 'metin' / f'{key}.md', encoding='utf-8').read()
    pars = paragraflar(md); ch = parcalar(pars)
    assert len(pars) == len(zam), (len(pars), len(zam))
    mp3 = KOK / 'ses' / key / f'{vid}.mp3'
    pcm = coz(mp3)
    print(f'{len(ch)} parça, {len(pars)} paragraf, {len(pcm) / SR:.1f} sn')
    yeni, yeni_zam, sorun = [], [None] * len(pars), []
    onceki_son = 0
    for ci, c in enumerate(ch):
        s0 = onceki_son
        s1 = int(round(zam[c['idx'][-1]][1] * SR)) if ci < len(ch) - 1 else len(pcm)
        onceki_son = s1
        seg = pcm[s0:s1]
        # konuşma başlangıcı (öndeki sessizlikten sonra)
        k0 = next((i for i in range(0, len(seg), 240) if max((abs(x) for x in seg[i:i + 240]), default=0) > 600), 0)
        metin = '\n'.join(t for t, _ in c['p'])
        konusma = len(seg) - k0 - int(0.6 * SR)
        td = konusma * len(harf(YONERGE)) / (len(harf(YONERGE)) + len(harf(metin)))
        adaylar = [g for g in sessizlikler(seg, k0 + int(td * 0.55), k0 + int(td * 1.6))]
        adaylar.sort(key=lambda g: (abs((g[0] - k0) - td) / SR - min(0.6, (g[1] - g[0]) / SR)))
        hedef = harf(metin)[:110]
        secilen = None
        # Gemini bazı parçalarda yönergeyi okumamış olabilir: parça zaten metnin ilk cümlesiyle başlıyorsa kesme
        t0 = dokum(seg[k0:k0 + 10 * SR])
        if t0:
            h0 = harf(t0)
            if lcs_oran(hedef[:min(len(hedef), len(h0))], h0[:len(hedef) + 20]) >= 0.8 and not any(
                    w in t0.lower() for w in ('yönerge', 'tıp dersi anlatım', 'telaffuz ederek', 'hiçbir şey ekleme')):
                secilen = (k0, 1.0, 'yok')
        for g in ([] if secilen else adaylar[:4]):
            kes = max(g[0], g[1] - int(0.12 * SR))
            t = dokum(seg[kes:kes + 10 * SR])
            if t is None:
                sorun.append(f'parça {ci + 1}: döküm alınamadı'); break
            ht = harf(t)
            oran = lcs_oran(hedef[:min(len(hedef), len(ht))], ht[:len(hedef) + 20]) if ht else 0
            yonerge_iz = any(w in t.lower() for w in ('yönerge', 'tıp dersi anlatım', 'telaffuz ederek', 'hiçbir şey ekleme'))
            if oran >= 0.8 and not yonerge_iz:
                secilen = (kes, oran); break
        if not secilen:
            sorun.append(f'parça {ci + 1}: kesim doğrulanamadı (aday {len(adaylar)})')
            secilen = None
        lead = k0 if k0 < 1.0 * SR else int(0.3 * SR)
        if secilen:
            govde = seg[secilen[0]:]
            parca = [0] * min(lead, int(0.6 * SR)) + govde
            print(f'  parça {ci + 1:2d}: ' + ('yönerge okunmamış, olduğu gibi' if len(secilen) > 2 else f'yönerge {(secilen[0] - k0) / SR:5.1f} sn kesildi (doğrulama %{secilen[1] * 100:.0f})'))
        else:
            parca = seg
            print(f'  parça {ci + 1:2d}: DOKUNULMADI')
        bas = len(yeni) / SR
        yeni.extend(parca)
        son = len(yeni) / SR
        # paragraf zamanı: parça konuşmasına karakter oranıyla (öndeki boşluk ve 0,6 sn kuyruk hariç)
        kb = bas + min(lead, int(0.6 * SR)) / SR if secilen else bas + k0 / SR
        ks = max(kb + 0.5, son - 0.6)
        uz = [len(harf(t)) or 1 for t, _ in c['p']]; top = sum(uz); t0 = kb
        for j, idx in enumerate(c['idx']):
            t1 = ks if j == len(uz) - 1 else t0 + (ks - kb) * uz[j] / top
            yeni_zam[idx] = [round(t0 if j else bas, 2), round(t1 if j < len(uz) - 1 else son, 2)]
            t0 = t1
    # paragraflar uç uca
    for i in range(1, len(yeni_zam)):
        yeni_zam[i][0] = yeni_zam[i - 1][1]
    print(f'yeni süre {len(yeni) / SR:.1f} sn (eski {len(pcm) / SR:.1f}); sorun: {len(sorun)}')
    for s in sorun: print('  ', s)
    if kuru or sorun:
        print('yazılmadı' + (' (sorun var)' if sorun else ' (kuru)'))
        return 1 if sorun else 0
    raw = struct.pack('<%dh' % len(yeni), *yeni)
    yedek = mp3.with_suffix('.yedek.mp3')
    if not yedek.exists(): os.rename(mp3, yedek)
    subprocess.run([FF, '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', '-b:a', '64k', str(mp3)], input=raw, check=True)
    kayit = json.load(open(KOK / 'kayit.json'))
    v = next(x for x in kayit[key] if x['id'] == vid)
    v['sureSn'] = round(len(yeni) / SR); v['bayt'] = mp3.stat().st_size; v['zamanlama'] = yeni_zam
    v['zamanlamaKaynak'] = 'onarim-tahmini'; v['onarim'] = 'yönerge sesi kesildi'
    tmp = KOK / 'kayit.json.tmp'; json.dump(kayit, open(tmp, 'w'), ensure_ascii=False, indent=1); os.replace(tmp, KOK / 'kayit.json')
    print('yazıldı:', mp3)
    return 0


if __name__ == '__main__':
    sys.exit(main())
