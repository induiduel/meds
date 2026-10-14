"""Her soru için belge kimliği (özgün dosya ailesi) + sınav birimi (yıl|sınav) + kesinlik → birim.json"""
import json, re, collections
R = {json.loads(l)['id']: json.loads(l) for l in open('sorular_ozet.jsonl')}
B = json.load(open('bolum.json'))

def fam(s):
    s = str(s or '').replace('%20', ' ')
    s = re.sub(r'(\.(pdf|txt|pptx|json|md|docx))+$', '', s, flags=re.I)
    s = re.sub(r'_(pdf_)*pdf$', '', s)
    import unicodedata
    s = s.replace('İ', 'i').replace('I', 'ı').lower().translate(str.maketrans('çğıöşüâîû', 'cgiosuaiu'))
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^0-9a-z]+', ' ', s)
    rom = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5', 'vi': '6'}
    s = ' '.join(rom.get(t, t) for t in s.split())
    s = re.sub(r'[aeiou ]+', '', s)          # iskelet: OCR/ASCII kayıplarına dayanıklı (ö→_ gibi)
    s = s.replace('2220final', '22final')
    return s
def belge(r):
    i = r['id']
    m = re.match(r'^(k1-\d{4}-\d{4}(?:-[a-d])?)-q\d+$', i)
    if m: return 'D3K1pdf:' + m.group(1)
    if i.startswith('final-2018-2019-'): return 'dosya:' + fam('19 final')
    if B[i].startswith('cp-'): return 'combinepdf:' + B[i]
    m = re.match(r'^(?:past-)?q-(.+?)-(\d+)(?:-cs\d+)?$', i)
    if m and not re.match(r'^past-\d', i):
        f = fam(m.group(1).replace('_20final', ' final'))
        return 'dosya:' + f
    return 'dosya:' + fam(r.get('kaynak'))

# Belge → sınav birimi (yıl, sınav) ve kesinlik. Kesin = belgenin kendi başlığı/etiketi tek yıl+tek sınav diyor ve
# veriyle (örtüşme) çelişmiyor. None = bilinmiyor / derleme.
CP_K = lambda s: s[4]  # cp-K1a -> '1'
BIRIM = {}
def birim_of_belge(b):
    if b.startswith('D3K1pdf:'):
        p = b.split(':')[1]
        y = re.search(r'(\d{4}-\d{4})', p).group(1)
        return (y, 'K1', 'kesin', 'D3K1 Tüm Çıkmışlar PDF bölüm başlığı' + (' (kitapçık = öğrenci çıktısı)' if p[-2] == '-' else ''))
    if b.startswith('combinepdf:'):
        s = b.split(':')[1]
        if s == 'cp-?': return (None, None, 'belirsiz', 'birleşik PDF: sayfa bilinmiyor')
        if s == 'cp-S0': return (None, 'F?', 'tek_sinav', 'birleşik PDF ilk 100 sayfa: başlıksız, 1–100 numaralı tek sınav (tüm anabilim dalları → final biçimi); yılı bilinmiyor')
        return ('2020-2021', 'K' + s[4], 'kesin', 'sinav.karabuk.edu.tr çıktısı: "Dönem 3 Kurul %s Sonucu" (Aralık 2020–Haziran 2021 baskıları)' % s[4])
    f = b.split(':', 1)[1]
    T = {
        '18': ('2018-2019', 'K1', 'kesin', '18.txt/18.pdf = D3K1 PDF 2018-2019 ile %98 örtüşme (2026-10-13 doğrulandı)'),
        '1kurulsorular': ('2021-2022', 'K1', 'kesin', 'D3K1 PDF 2021-2022 ile %94 örtüşme'),
        '19 final': ('2018-2019', 'F', 'kesin', 'resmî 2019 Final (12.06.2019) + resmî cevap anahtarı'),
        'donem3/3. Sınıf/Kurul 2/2': ('2020-2021', 'K2', 'kesin', '2.Kurul-2021.pdf: karne 901009/901070/901035/901005 = birleşik PDF 2020-21 Kurul 2 çıktıları'),
        'donem3/3. Sınıf/Kurul 2/Kurul II Sınavı': ('2018-2019', 'K2', 'kesin', 'resmî Dönem III Kurul II Sınavı, 29 Kasım 2018'),
        'Kurul II Sınavı': ('2018-2019', 'K2', 'kesin', 'resmî Dönem III Kurul II Sınavı, 29 Kasım 2018'),
        'Kurul_II_Cevap_Anahtar_': ('2018-2019', 'K2', 'kesin', 'Kurul II cevap anahtarı, 29 Kasım 2018'),
        'Kurul I Sınavı': ('2018-2019', 'K1', 'kesin', 'resmî Dönem III Kurul I Sınavı, 18 Ekim 2018'),
        'Kurul_I_Cevap_Anahtar_': ('2018-2019', 'K1', 'kesin', 'Kurul I cevap anahtarı, 18 Ekim 2018'),
        'donem3/3. Sınıf/Kurul 3/Kurul III Sınavı': ('2018-2019', 'K3', 'olasi', 'resmî sınav serisi (Kurul I/II 2018 ile aynı biçim); taranmış, tarih okunamadı'),
        'donem3/3. Sınıf/Kurul 4/3.sınıf 4': ('2019-2020', 'K4', 'kesin', 'belge tarihi 13.03.2020'),
        'D3 KURUL 2_250607_134656': ('2024-2025', 'K2', 'kesin', 'belge tarihi 06.12.2024'),
        'D3 KURUL 1_250607_133602': ('2024-2025', 'K1', 'kesin', 'belge tarihi 25.10.2024'),
        '25': ('2024-2025', 'K1', 'kesin', 'kurul 1 klasörü, belge tarihi 25.10.2024'),
        '2021final_230619_142600': ('2020-2021', 'F', 'kesin', 'final karnesi 1729456 (Haziran 2021 sonrası)'),
        '2021final11_230619_142606': ('2020-2021', 'F', 'kesin', 'final karnesi 1729455'),
        '2021final1_230619_142616': ('2020-2021', 'F', 'kesin', 'final karnesi 1729548'),
        '21 final': ('2020-2021', 'F', 'kesin', 'final karnesi 1729548'),
        '6_kurul': ('2020-2021', 'K6', 'kesin', 'Dönem 3 Kurul 6 karnesi 1671793, 22.06.2021'),
        '22 23': ('2022-2023', 'K5', 'olasi', 'kurul 5 klasörü, adı "22 23", başlık DÖNEM 3 KURUL 5'),
        '22final230619145249': ('2021-2022', 'F', 'olasi', '"22 final" (indirme 2023-06-19): tek final sınavı, yıl adından'),
        '2223d3butunleme101817': ('2022-2023', 'B', 'kesin', 'dosya adı: 22-23 D3 Bütünleme'),
        '2223büt240624124604': ('2022-2023', 'B', 'kesin', 'dosya adı: 22-23 Büt'),
        '2223but240624124604': ('2022-2023', 'B', 'kesin', 'dosya adı: 22-23 Büt'),
        '20252026dönem3finalsınavı': ('2025-2026', 'F', 'olasi', 'dosya adı: 2025-2026 Dönem 3 Final (indirilen kopyası yok; 2021-22 finaliyle %41 ortak soru)'),
        '20222023dönem3kurul4çıkmışlar250311152630': ('2022-2023', 'K4', 'kesin', 'dosya adı: 2022-2023 Dönem 3 Kurul 4'),
        '20212022dönem3kurul4çıkmışlar250311152547': ('2021-2022', 'K4', 'kesin', 'dosya adı: 2021-2022 Dönem 3 Kurul 4'),
        '2526dönem3kurul1': ('2025-2026', 'K1', 'kesin', 'dosya adı'), '2526dönem3kurul2': ('2025-2026', 'K2', 'kesin', 'dosya adı'),
        '2526dönem3kurul3': ('2025-2026', 'K3', 'kesin', 'dosya adı'), '2526dönem3kurul4': ('2025-2026', 'K4', 'kesin', 'dosya adı'),
        '2526dönem3kurul5': ('2025-2026', 'K5', 'kesin', 'dosya adı'), '2526dönem3kurul6': ('2025-2026', 'K6', 'kesin', 'dosya adı'),
        '2526dnem3kurul1': ('2025-2026', 'K1', 'kesin', 'dosya adı'), '2526dnem3kurul2': ('2025-2026', 'K2', 'kesin', 'dosya adı'),
        '2526donem3kurul4': ('2025-2026', 'K4', 'kesin', 'dosya adı'), '2526donem3kurul6': ('2025-2026', 'K6', 'kesin', 'dosya adı'),
        'd3kurul2250607134656': ('2024-2025', 'K2', 'olasi', 'D3 KURUL 2, indirme 2025-06-07'),
        'd3kurul5250607142756': ('2024-2025', 'K5', 'olasi', 'D3 KURUL 5, indirme 2025-06-07'),
        'd3kurul4250607141527': ('2024-2025', 'K4', 'olasi', 'D3 KURUL 4, indirme 2025-06-07'),
        'd3kurul1250607133602': ('2024-2025', 'K1', 'olasi', 'D3 KURUL 1, indirme 2025-06-07'),
        'kurul32023': ('2022-2023', 'K3', 'olasi', 'KURUL 3 2023'),
        '2016gkurul5sorularıvecevaplarıpdfpatolojiiçeriyor': ('2016-2017', 'D2K5', 'olasi', '2016 Dönem 2 Kurul 5 (patoloji)'),
    }
    T = {fam(k): v for k, v in T.items()}
    if f in T: return T[f]
    return (None, None, 'belirsiz', 'derleme ya da yılı/kurulu belirsiz belge')

NOTE_RE = re.compile(r'^(20\d\d)-(20\d\d) Dönem 3 Kurul (\d)\b(?!.*(?:20\d\d-20\d\d|\bve\b|;))')
out = {}
for i, r in R.items():
    b = belge(r)
    y, s, k, why = birim_of_belge(b)
    # ders bazlı derlemelerde soru notu tek yıl + tek kurul diyorsa "not" düzeyinde birim
    if y is None and re.search(r'derleme|_kurul\d_cikmis_sorular|_donem3_kurul1_cikmis', B[i].lower()):
        m = NOTE_RE.match(str(r.get('sourceNote') or ''))
        if m: y, s, k, why = (f'{m.group(1)}-{m.group(2)}', 'K' + m.group(3), 'not', 'ders derlemesindeki soru notu: ' + r['sourceNote'][:80])
    out[i] = {'belge': b, 'yil': y, 'sinav': s, 'kesinlik': k, 'gerekce': why, 'bolum': B[i]}
json.dump(out, open('birim.json', 'w'), ensure_ascii=False)
c = collections.Counter((v['kesinlik']) for v in out.values()); print(c)
c = collections.Counter((v['yil'], v['sinav'], v['kesinlik']) for v in out.values() if v['yil']); 
for k, n in sorted(c.items()): print(n, k)
print(collections.Counter(v['belge'] for v in out.values() if v['kesinlik'] == 'belirsiz').most_common(60))
