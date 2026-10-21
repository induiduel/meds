#!/usr/bin/env python3
"""Öncelikli dersler: sesli derslerin "az ezber, çok puan" analizi.

Her sesli ders (Son Prova partları ve modül dersleri hariç) için ders metninden ve o dersin çıkmışlarından ölçüm
çıkarır, `src/data/oncelikli_dersler/k<N>.json` yazar. Ekran (`components/oncelikli/`) bu ham ölçümleri öğrencinin
seçtiği ağırlıklarla puanlar; buradaki `puan` yalnız varsayılan ağırlıkla hesaplanmış sıradır.

Ölçümler (hepsi metinden, LLM yok — yeniden çalıştırınca aynı sonuç):
  kelime        anlatım uzunluğu (kısa = hızlı biter)
  terim         farklı yabancı/özel terim sayısı (sözlük eşleşmesi ∪ Latince/yabancı biçim, kısaltma, gen adı, özel ad)
  ilac/hastalik sözlükte "ilac" / "hastalik|patojen" kategorisindeki farklı terimler
  sayi          farklı sayı/yüzde/hafta değeri (sayı ezberi)
  terim1000     1000 kelimede terim (ezber yoğunluğu)
  mantik1000    1000 kelimede nedensellik/akıl yürütme bağlacı ("çünkü", "bu yüzden", "yol açar", "artar" …)
  cikmis        dersin çıkmış sorusu (soru çözücü + ek modül), yil = farklı sınav yılı (ne sıklıkla çıkıyor)
  cikmisIsim    çıkmışlarda doğru şıkkı tek bir isim/terim olan soru oranı (isim ezberi soran soru)
  cikmisTerim   çıkmış kök + şıklarında 100 kelimede yabancı terim (detay düzeyi)
  beklenen      sınavda bu dersten beklenen soru = branş soru sayısı × dersin branş çıkmış payı (sınav dağılımı)

Kullanım: python3 scripts/oncelikli_dersler/analiz.py [--kurul 1] [--liste liste.json]
  --liste: /api/canli-ders çıktısı (yoksa localhost:3000'den alınır) — branş ve branş içi numara oradan gelir.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
import urllib.request
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
METIN = KOK / 'data' / 'sesli_anlatim' / 'metin'
VERI = KOK / 'src' / 'data'

BRANS = {
    'Tıbbi Patoloji': 'patoloji', 'Enfeksiyon Hastalıkları': 'enfeksiyon', 'Üroloji': 'uroloji',
    'Tıbbi Genetik': 'genetik', 'Halk Sağlığı': 'halksagligi', 'Kadın Hastalıkları ve Doğum': 'kadindogum',
    'Tıbbi Farmakoloji': 'farmakoloji',
}
GIZLI = {'k1-54-uterus-duz-kas-ve-trofoblastik-tumorleri'}

# Türkçe kökenli olmayan terimlerin biçimsel izleri. Türkçe sözcük iki ünsüzle başlamaz, q/w/x içermez;
# tıp Latincesinin ekleri (-itis, -oma, -ozis …) ve ilaç ekleri (-mab, -sillin, -azol …) ayrıca yakalanır.
LATIN_EK = re.compile(
    r'(itis|it|oma|om|ozis|oz|emi|üri|uri|pati|plazi|trofi|sitoz|penia|peni|jenez|genez|fili|filus|ensis|'
    r'okok|kokus|bakter|mab|sillin|silin|misin|mycin|azol|vir|tid|prazol|olol|pril|sartan|statin|siklin|'
    r'floksasin|sefalosporin|steroid|ase|aemia|ozom|zom|sin|tin|lin|ül|ae)$')
# Türkçe çekim/fiil izleri: bu kalıpları taşıyan sözcük sözlükte yoksa terim sayılmaz ("uzaklaştırılamaz")
TURKCE_IZ = re.compile(r'(lan|len|laş|leş|tır|tir|dır|dir|abil|ebil|amaz|emez|ama|eme|mış|miş|muş|müş|'
                       r'acak|ecek|yor|ması|mesi|ıl|il|ul|ül)[a-zçğıöşü]*$|ş|ğ')
CIFT_UNSUZ = re.compile(r'^[bcçdfgğhjklmnprsştvyz]{2}')
YABANCI_HARF = re.compile(r'[qwx]')
SOZCUK = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüâîû][A-Za-zÇĞİÖŞÜçğıöşüâîû0-9\-']*")
SAYI = re.compile(r'%\s?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s?(?:%|mg|g|ml|mm|cm|hafta|gün|yıl|ay|saat|kat)?')

# Türkçe çekim/yapım eklerini at (terim kökü kalsın): "trombozun" → "tromboz"
EKLER = sorted({
    'ların', 'lerin', 'larda', 'lerde', 'lardan', 'lerden', 'lara', 'lere', 'ları', 'leri', 'lar', 'ler',
    'nın', 'nin', 'nun', 'nün', 'ın', 'in', 'un', 'ün', 'da', 'de', 'ta', 'te', 'dan', 'den', 'tan', 'ten',
    'ya', 'ye', 'yı', 'yi', 'yu', 'yü', 'yla', 'yle', 'la', 'le', 'dır', 'dir', 'dur', 'dür', 'tır', 'tir',
    'sı', 'si', 'su', 'sü', 'nda', 'nde', 'ndan', 'nden', 'na', 'ne', 'yı', 'ki', 'lı', 'li', 'lu', 'lü',
}, key=len, reverse=True)

# Akıl yürütme / nedensellik işaretleri: metin "neden-sonuç" kuruyorsa mantıkla çözülebilir.
MANTIK = [
    'çünkü', 'bu yüzden', 'bu nedenle', 'bu sebeple', 'dolayısıyla', 'sonucunda', 'sonuç olarak', 'bu da',
    'yol açar', 'yol açtığı', 'neden olur', 'neden olan', 'nedeniyle', 'yüzünden', 'sayesinde', 'böylece',
    'bu sayede', 'artar', 'azalır', 'artırır', 'azaltır', 'düşer', 'yükselir', 'engeller', 'önler', 'tetikler',
    'mekanizma', 'mantığı', 'mantık', 'eğer', 'ise', 'demek ki', 'buna karşılık', 'oysa', 'ancak', 'fakat',
    'yerine', 'amacıyla', 'için', 'kaynaklanır', 'bağlıdır', 'karşın', 'gibi düşünün', 'düşünün',
]
# Ezber işaretleri: sınıflama/liste/isim bildiren kalıplar
EZBER = ['sınıflandırılır', 'çeşitleri', 'türleri', 'tipleri', 'şunlardır', 'sayılabilir', 'adı verilir',
         'denir', 'olarak bilinir', 'etkenleri', 'ilaçları', 'en sık', 'kriterleri', 'evreleri']


def sade(s: str) -> str:
    s = unicodedata.normalize('NFC', s).replace('I', 'ı').replace('İ', 'i').lower()
    return s


# Derlemde tek başına geçen sözcükler: ek ancak kalan kök de gerçek bir sözcükse atılır ("trombüs" → "trombü"
# gibi kesik kök üretmemek için; YZ denetimi 2026-10-22 bu hatayı yakaladı). vocab_kur() ile doldurulur.
VOCAB: set[str] = set()


def vocab_kur(metinler) -> None:
    VOCAB.clear()
    for m in metinler:
        VOCAB.update(sade(w).strip("-'") for w in SOZCUK.findall(m))


def kok(w: str) -> str:
    w = sade(w).strip("-'")
    if "'" in w:
        return w.split("'")[0]
    for e in EKLER:
        if len(w) - len(e) >= 4 and w.endswith(e) and w[: -len(e)] in VOCAB:
            return kok(w[: -len(e)]) if len(w) - len(e) > 4 else w[: -len(e)]
    return w


BURADA = Path(__file__).resolve().parent


def liste_oku(ad: str) -> set[str]:
    """Satır başına bir kök; # yorum. YZ denetiminin bulduğu hatalardan kurulur (yz_birlestir.py)."""
    f = BURADA / ad
    if not f.exists():
        return set()
    return {kok(x.split('#')[0].strip()) for x in f.read_text().splitlines() if x.split('#')[0].strip()}


TURKCE = liste_oku('turkce_sozcukler.txt')   # terim sanılan Türkçe/genel sözcükler
EK_TERIM = liste_oku('ek_terimler.txt')      # kaçırılan yabancı terimler


def sozluk() -> tuple[dict[str, str], set[str]]:
    """Sözlük terimleri (tam ifade → kategori) ve tek sözcüklü terim kökleri."""
    g = json.loads((VERI / 'medical_glossary.json').read_text())
    ifade: dict[str, str] = {}
    for v in g.values():
        t = re.sub(r'\s*\(.*?\)', '', v.get('term', '')).strip()
        if len(t) >= 4:
            ifade[sade(t)] = v.get('category', 'terim')
    return ifade, {kok(t) for t in ifade if ' ' not in t}


# Genel Türkçe sözcükler: tüm sesli derslerin çoğunda geçen kökler terim sayılmaz (belge sıklığı süzgeci).
def genel_kokler(metinler: dict[str, str]) -> set[str]:
    df: Counter[str] = Counter()
    for m in metinler.values():
        df.update({kok(w) for w in SOZCUK.findall(m)})
    esik = max(8, int(len(metinler) * 0.35))
    return {k for k, n in df.items() if n >= esik}


def bilinen_kok(k: str, sozluk_kok: set[str]) -> str:
    """Ek almış biçimi bilinen terime indir: "vankomisine" → "vankomisin" (ek terim ya da sözlük kökü, ek ≤ 4 harf)."""
    if k in EK_TERIM or k in sozluk_kok:
        return k
    for n in range(1, 5):
        b = k[:-n]
        if len(b) >= 4 and (b in EK_TERIM or b in sozluk_kok):
            return b
    return k


def yabanci_mi(ham: str, k: str, genel: set[str], sozluk_kok: set[str]) -> bool:
    if re.fullmatch(r'[A-ZÇĞİÖŞÜ]{2,}[0-9]*', ham) or re.search(r'[A-Za-z]+\d', ham):
        return k not in TURKCE  # kısaltma, gen adı (KPC, ATM, BRCA1, p53) — 3 harfliler de sayılır
    if len(k) < 4 or k in TURKCE:
        return False
    if k in EK_TERIM:
        return True
    if k in genel:
        return False
    if re.fullmatch(r'[A-ZÇĞİÖŞÜ]{2,}[0-9]*', ham) or re.search(r'[A-Za-z]+\d', ham):
        return True  # kısaltma, gen adı (BRCA1, p53)
    if k in sozluk_kok:
        return True
    if TURKCE_IZ.search(k[3:]):
        return False
    if YABANCI_HARF.search(k) or CIFT_UNSUZ.match(k):
        return True
    return len(k) >= 6 and bool(LATIN_EK.search(k))


def metin_olc(m: str, genel: set[str], ifade: dict[str, str], sozluk_kok: set[str]) -> dict:
    duz = re.sub(r'^@@.*$|^#.*$', '', m, flags=re.M)
    sozcukler = SOZCUK.findall(duz)
    n = max(1, len(sozcukler))
    kucuk = sade(duz)
    terimler: set[str] = set()
    # Cümle ortasında büyük harfle başlayan sözcük özel addır (eponim: Chadwick, Kimmelstiel-Wilson, Sertoli);
    # büyük harfli cins adını izleyen küçük harfli sözcük Latince tür adıdır (Treponema pallidum, Listeria monocytogenes).
    # YZ denetimi bu iki sınıfın sistematik olarak kaçtığını gösterdi.
    for mt in re.finditer(r"(?<=[^.!?:\n•\-\s(“\"])\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:-[A-ZÇĞİÖŞÜ]?[a-zçğıöşü]+)*)(?:\s+([a-z]{4,}))?", duz):
        ad, tur = mt.group(1), mt.group(2)
        k = kok(ad)
        if len(k) >= 4 and k not in TURKCE and k not in genel and not TURKCE_IZ.search(k[3:]):
            terimler.add(k)
            if tur and re.search(r'(um|us|is|ae|ii|i|a|es|enes|ogenes|ensis|ella)$', tur) and kok(tur) not in genel:
                terimler.add(kok(tur))
    for w in sozcukler:
        k = bilinen_kok(kok(w), sozluk_kok)
        if yabanci_mi(w, k, genel, sozluk_kok):
            terimler.add(k)
    # çok sözcüklü ek terimler ("asit fosfataz", "fibrinoid nekroz") ifade olarak aranır
    for t in EK_TERIM:
        if ' ' in t and t in kucuk:
            terimler.add(t)
    kategori = Counter()
    for t, c in ifade.items():
        if len(t) >= 5 and t in kucuk and c in ('ilac', 'hastalik', 'patojen', 'genetik'):
            kategori['ilac' if c == 'ilac' else 'hastalik' if c in ('hastalik', 'patojen') else 'gen'] += 1
    sayilar = {re.sub(r'\s', '', s) for s in SAYI.findall(duz) if re.search(r'\d', s)}
    mantik = sum(kucuk.count(' ' + b) for b in MANTIK)
    ezber = sum(kucuk.count(b) for b in EZBER)
    return {
        'kelime': n,
        'terim': len(terimler),
        'ilac': kategori['ilac'],
        'hastalik': kategori['hastalik'],
        'gen': kategori['gen'],
        'sayi': len(sayilar),
        'terim1000': round(len(terimler) * 1000 / n, 1),
        'mantik1000': round(mantik * 1000 / n, 1),
        'ezberKalip1000': round(ezber * 1000 / n, 2),
        '_terimler': terimler,
    }


def _baslik_sozcuk(s: str) -> set[str]:
    katla = str.maketrans('çğıöşüâîû', 'cgiosuaiu')
    return {w for w in re.findall(r'\w{4,}', sade(s).translate(katla))}


def cikmislar(brans: str, no: int, baslik: str) -> list[dict]:
    """Dersin çıkmışları. Sesli ders numarası çözücü numarasıyla her zaman aynı değil (k1-65 Meme Kanseri sesli
    listede 34, çözücüde 35 — YZ denetimi yakaladı): dosya başlıkla doğrulanır, uymazsa aynı branşta başlığı en çok
    örtüşen dosya alınır."""
    def dosyalar(klasor: Path) -> list[dict]:
        l = [json.loads(f.read_text()) for f in sorted(klasor.glob('*.json')) if f.name != 'index.json']
        hedef = _baslik_sozcuk(baslik)
        ayni = [d for d in l if int(d.get('no', -1)) == no and _baslik_sozcuk(d.get('baslik', '')) & hedef]
        if ayni:
            return ayni
        puan = {id(d): len(_baslik_sozcuk(d.get('baslik', '')) & hedef) for d in l}
        en = max(puan.values(), default=0)
        return [d for d in l if en >= 2 and puan[id(d)] == en]
    qs: list[dict] = []
    for d in dosyalar(VERI / f'{brans}_cozucu') + dosyalar(VERI / 'cikmis_paket' / 'ek' / brans):
        qs += [q for q in d.get('sorular', []) if q.get('tur') == 'cikmis']
    # aynı kök iki modülde → tekil
    gor, tekil = set(), []
    for q in qs:
        a = sade(q.get('soru', ''))[:120]
        if a not in gor:
            gor.add(a)
            tekil.append(q)
    return tekil


def cikmis_olc(qs: list[dict], genel: set[str], sozluk_kok: set[str]) -> dict:
    if not qs:
        return {'cikmis': 0, 'yil': 0, 'cikmisIsim': None, 'cikmisTerim': None, 'cikmisNegatif': None}
    isim = negatif = 0
    terim = kelime = 0
    yillar = set()
    for q in qs:
        y = re.search(r'(20\d\d)\s*[-–]\s*(20\d\d)|20\d\d', q.get('sinav', '') or '')
        if y:
            yillar.add(y.group(0))
        dogru = (q.get('secenekler') or {}).get(q.get('dogru'), '')
        if len(SOZCUK.findall(dogru)) <= 4:
            isim += 1  # doğru şık kısa bir ad: "hangisidir → X" tipi isim/eşleme sorusu
        if re.search(r'yanlıştır|değildir|beklenmez|söylenemez', sade(q.get('soru', ''))):
            negatif += 1
        govde = q.get('soru', '') + ' ' + ' '.join((q.get('secenekler') or {}).values())
        ws = SOZCUK.findall(govde)
        kelime += len(ws)
        terim += sum(1 for w in ws if yabanci_mi(w, kok(w), genel, sozluk_kok))
    n = len(qs)
    return {
        'cikmis': n,
        'yil': len(yillar),
        'cikmisIsim': round(isim / n, 2),
        'cikmisTerim': round(terim * 100 / max(1, kelime), 1),
        'cikmisNegatif': round(negatif / n, 2),
    }


def yuzdelik(degerler: list[float], v: float) -> float:
    """0–100: v'nin dağılımdaki yeri (küçük → 0)."""
    s = sorted(degerler)
    if len(s) < 2:
        return 50.0
    alt = sum(1 for x in s if x < v)
    esit = sum(1 for x in s if x == v)
    return round(100 * (alt + (esit - 1) / 2) / (len(s) - 1), 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--kurul', type=int, default=1)
    ap.add_argument('--liste')
    ap.add_argument('--dok', help='her dersin tüm terim listesini bu klasöre yaz (YZ denetimi için)')
    a = ap.parse_args()

    if a.liste:
        liste = json.loads(Path(a.liste).read_text())['dersler']
    else:
        with urllib.request.urlopen('http://localhost:3000/api/canli-ders', timeout=30) as r:
            liste = json.loads(r.read())['dersler']
    dersler = [d for d in liste if d.get('kurul') == a.kurul and isinstance(d.get('no'), int)
               and d.get('brans') in BRANS and d['key'] not in GIZLI and (METIN / f"{d['key']}.md").exists()]
    metinler = {d['key']: (METIN / f"{d['key']}.md").read_text() for d in dersler}
    tum = {p.stem: p.read_text() for p in METIN.glob(f'k{a.kurul}-*.md')}
    vocab_kur(tum.values())
    genel = genel_kokler(tum)
    ifade, sozluk_kok = sozluk()
    dagilim = json.loads((VERI / 'sinav_dagilimi.json').read_text())['kurullar'].get(str(a.kurul), {}).get('branslar', {})

    satirlar = []
    for d in dersler:
        b = BRANS[d['brans']]
        m = metin_olc(metinler[d['key']], genel, ifade, sozluk_kok)
        cq = cikmislar(b, d['no'], d['baslik'])
        c = cikmis_olc(cq, genel, sozluk_kok)
        c['_cq'] = [{'soru': q.get('soru'), 'secenekler': q.get('secenekler'), 'dogru': q.get('dogru'), 'sinav': q.get('sinav')} for q in cq]
        ornek = sorted(m.pop('_terimler'))
        satirlar.append({'key': d['key'], 'baslik': d['baslik'], 'brans': b, 'no': d['no'],
                         'sureSn': (d.get('varsayilan') or {}).get('sureSn'), **m, **c, '_ornek': ornek})

    # beklenen soru: branşın sınav soru sayısını dersin çıkmış payına göre (çıkmışı olmayan derse +1 yumuşatma) böl
    for b in {s['brans'] for s in satirlar}:
        grup = [s for s in satirlar if s['brans'] == b]
        top = sum(s['cikmis'] + 1 for s in grup)
        for s in grup:
            s['beklenen'] = round(dagilim.get(b, 0) * (s['cikmis'] + 1) / top, 2)

    # Boyut puanları 0–100 (yüksek = öğrenci lehine): kısalık, az ezber, mantık, kolay çıkmış, sık çıkmış, getiri
    def kol(k):
        return [s[k] for s in satirlar if s[k] is not None]
    for s in satirlar:
        ezber_ham = (yuzdelik(kol('terim1000'), s['terim1000']) * 0.4 + yuzdelik(kol('terim'), s['terim']) * 0.25
                     + yuzdelik(kol('ilac'), s['ilac']) * 0.15 + yuzdelik(kol('hastalik'), s['hastalik']) * 0.1
                     + yuzdelik(kol('sayi'), s['sayi']) * 0.1)
        s['boyut'] = {
            'kisa': round(100 - yuzdelik(kol('kelime'), s['kelime'])),
            'azEzber': round(100 - ezber_ham),
            'mantik': round(yuzdelik(kol('mantik1000'), s['mantik1000']) * 0.75
                            + (100 - yuzdelik(kol('ezberKalip1000'), s['ezberKalip1000'])) * 0.25),
            'kolayCikmis': None if s['cikmisIsim'] is None else round(
                (100 - yuzdelik(kol('cikmisTerim'), s['cikmisTerim'])) * 0.6
                + (100 - yuzdelik(kol('cikmisIsim'), s['cikmisIsim'])) * 0.4),
            'sikCikmis': round(yuzdelik(kol('cikmis'), s['cikmis']) * 0.7 + yuzdelik(kol('yil'), s['yil']) * 0.3),
            'getiri': round(yuzdelik([x['beklenen'] / max(1, x['kelime']) for x in satirlar],
                                     s['beklenen'] / max(1, s['kelime']))),
        }
    # YZ yargısı (yz/k<N>.json, Claude ders metnini + çıkmışları okuyarak verdi): azEzber / mantik / kolayCikmis
    # boyutlarında YZ %60, metin ölçümü %40; tür, gerekçe, ezber çekirdeği ve konu türleri doğrudan YZ'den.
    yzf = BURADA / 'yz' / f'k{a.kurul}.json'
    yz = json.loads(yzf.read_text()) if yzf.exists() else {}
    for s in satirlar:
        y = yz.get(s['key'])
        if not y:
            continue
        for k in ('azEzber', 'mantik', 'kolayCikmis'):
            if isinstance(y.get(k), (int, float)):
                s['boyut'][k] = round(0.6 * y[k] + 0.4 * (s['boyut'][k] if s['boyut'][k] is not None else y[k]))
        s['yz'] = {k: y[k] for k in ('tur', 'gerekce', 'ezberCekirdegi', 'konular', 'cikmisNot') if k in y}
    VARSAYILAN = {'azEzber': 3, 'mantik': 2.5, 'kolayCikmis': 1.5, 'kisa': 1.5, 'getiri': 1.5, 'sikCikmis': 1}
    for s in satirlar:
        tp = ag = 0.0
        for k, w in VARSAYILAN.items():
            v = s['boyut'][k]
            if v is None:
                v = 40  # çıkmışı olmayan ders: kolaylık bilinmiyor, hafif ceza
            tp += v * w
            ag += w
        s['puan'] = round(tp / ag)
        b = s['boyut']
        s['tur'] = s.get('yz', {}).get('tur') or ('mantik' if b['mantik'] >= 60 and b['azEzber'] >= 55 else
                    'ezber' if b['azEzber'] < 40 else 'karma')
        if a.dok:
            Path(a.dok).mkdir(parents=True, exist_ok=True)
            (Path(a.dok) / f"{s['key']}.json").write_text(json.dumps(
                {'key': s['key'], 'baslik': s['baslik'], 'brans': s['brans'], 'no': s['no'], 'terimler': s['_ornek'], 'metin': str(METIN / f"{s['key']}.md"), 'cikmislar': s['_cq']},
                ensure_ascii=False, indent=0))
        s.pop('_cq', None)
        s['ornekTerim'] = sorted(s.pop('_ornek'), key=lambda t: (-len(t), t))[:8]
    satirlar.sort(key=lambda s: -s['puan'])
    for i, s in enumerate(satirlar, 1):
        s['sira'] = i

    cikti = {
        'kurul': a.kurul,
        'aciklama': 'scripts/oncelikli_dersler/analiz.py üretir; elle yazılmaz. boyut: 0–100, yüksek = öğrenci lehine.',
        'varsayilanAgirlik': VARSAYILAN,
        'dersler': satirlar,
    }
    hedef = VERI / 'oncelikli_dersler' / f'k{a.kurul}.json'
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(json.dumps(cikti, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(satirlar)} ders → {hedef.relative_to(KOK)}')
    for s in satirlar:
        b = s['boyut']
        print(f"{s['sira']:2} {s['puan']:3} {s['tur']:6} {s['brans'][:6]:6} {s['baslik'][:42]:42} "
              f"kısa{b['kisa']:4} ezb{b['azEzber']:4} man{b['mantik']:4} kol{str(b['kolayCikmis']):>5} "
              f"sık{b['sikCikmis']:4} get{b['getiri']:4} | ç{s['cikmis']:3} t/k{s['terim1000']:6} {s['ornekTerim'][:4]}")


if __name__ == '__main__':
    main()
