#!/usr/bin/env python3
"""
Hastalık → ders programı (Kurul → Ders → Konu) eşlemesi.

Çıktı: src/data/disease_lessons.json — Hastalıklar sayfasındaki "Ders programı" süzgecinin verisi.
Yeniden üretim (yalnız CPU, ~10-20 sn):  python3 scripts/diseases/hastalik_ders_eslesmesi.py [--rapor]

Kaynaklar (tahmin yok; yalnız metinde geçen ad):
  - Ders programı: src/data/mufredat_paketi.json (resmî 2026-27 programı; kazanım konularıyla birebir aynı)
  - Konu başlığı (ad başlıkta geçiyorsa en güçlü kanıt)
  - Kazanım metinleri + slayt alıntıları + kazanım özetleri: src/data/kazanimlar/k*.json
  - O konunun etiketiyle gelen çıkmış sorular (soru kökü + doğru şık; konu etiketi sınavın kendi etiketi)
  - Amfi ders özeti (lectureSummariesCatalog.json): konuya kesin bağlıysa (kazanım slaytındaki deste kimliği) ya da
    başlık benzerliği yüksekse (aynı ders, ≥0,6). Belirsiz özetler kullanılmaz.

Eşleşme: Türkçe katlanmış metinde sözcük sınırıyla ad / eş ad / Latince ad aranır; son sözcüğün iyelik/hâl eki
düşürülüp (tümörü → tümör, hastalığı → hastalı-) en çok 7 harflik ek kabul edilir. ≤3 harfli kısaltmalar (AML, MN…)
hiç kullanılmaz; 4-6 harfli büyük harf kısaltmalar (ADPKD, FSGS) büyük/küçük harf duyarlı aranır.
Kabul: başlıkta geçer YA DA kazanım/çıkmış metninde ≥1 kez YA DA ders özetinde ≥2 kez geçer.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'src' / 'data'
OUT = DATA / 'disease_lessons.json'

FOLD = str.maketrans({'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 'â': 'a', 'î': 'i', 'û': 'u', 'é': 'e', 'ë': 'e'})


def fold(s: str) -> str:
    s = str(s or '').replace('İ', 'i').replace('I', 'ı')
    return s.lower().translate(FOLD)


def norm_text(s: str) -> str:
    """Arama metni: katlanmış, harf/rakam dışı her şey tek boşluk (sözcük sınırı korunur)."""
    return ' ' + re.sub(r'[^a-z0-9]+', ' ', fold(s)) + ' '


# ------------------------------------------------------------------ ad varyantları
# Tek başına ad sayılmayan sözcük kökleri (varyantın TÜM sözcükleri bunlardansa varyant atılır)
GENERIC_STEMS = (
    'hastal', 'sendrom', 'enfeksiyon', 'tumor', 'kanser', 'karsinom', 'nekroz', 'protein', 'reaksiyon', 'bozukl', 'sinif',
    'tip', 'akut', 'kronik', 'primer', 'sekonder', 'benign', 'malign', 'disease', 'syndrom', 'infection', 'tumour',
    'tanim', 'definition', 'kucuk', 'buyuk', 'hucre', 'cell', 'kriter', 'tedavi', 'yolu', 'derecelendir', 'who', 'dso',
    'the', 'of', 'and', 've', 'ile', 'iliskili', 'tipleri', 'lezyon', 'hiperplazi', 'hipertrofi', 'atrofi', 'metaplazi',
    'displazi', 'adenom', 'polip', 'kist', 'enflamasyon', 'inflammation', 'yetmezlik', 'zehirlenme', 'toksisite',
)
ORGAN = {
    'bobrek', 'mesane', 'karaciger', 'akciger', 'prostat', 'meme', 'over', 'serviks', 'uterus', 'testis', 'tiroid',
    'mide', 'kolon', 'pankreas', 'beyin', 'kalp', 'deri', 'kemik', 'renal', 'adrenal', 'hipofiz', 'safra', 'ozofagus', 'bagirsak',
    'endometrium', 'vulva', 'vajina', 'penis', 'ureter', 'uretra', 'dalak', 'timus', 'paratiroid', 'kidney', 'bladder', 'thyroid',
    'lung', 'liver', 'breast',
}


def fwords(s: str) -> list[str]:
    return re.sub(r'[^a-z0-9]+', ' ', fold(s)).split()


def organ_of(word: str) -> str | None:
    """"akcigerin", "tiroidin", "bobrek" → organ kökü"""
    for o in ORGAN:
        if word == o or (word.startswith(o) and len(word) - len(o) <= 3):
            return o
    return None


def is_generic(words: list[str]) -> bool:
    return all(w.startswith(GENERIC_STEMS) or organ_of(w) for w in words)


def split_variants(raw: str) -> list[tuple[str, str | None]]:
    """Ad → [(varyant, gereken organ)]. 'Wilms tümörü (nefroblastom)' → Wilms tümörü, nefroblastom.
    Organ gereksinimi: baştaki organ sözcüğü düşülmüş biçim ("Böbrek Onkositoması" → "onkositoması") yalnız o konunun
    metninde organ adı da geçiyorsa sayılır."""
    raw = str(raw or '').strip()
    if not raw:
        return []
    base = re.sub(r'\s*\([^)]*\)', '', raw).strip()
    out: list[str] = [raw, base]
    for inner in re.findall(r'\(([^)]*)\)', raw):
        if re.search(r'\s(ve|and)\s', inner):
            continue  # "(Küçük Hücreli ve Skuamöz)" gibi niteleyici listeler
        out.extend(p.strip() for p in re.split(r'[,/;]| veya | or ', inner))
    # "Ateroskleroz ve Aterom Plağı" → ayrı adlar (ikinci parça yalnız ≥2 sözcükse)
    parts = [p.strip() for p in re.split(r'\s+ve\s+', base) if p.strip()]
    if len(parts) == 2:
        out.append(parts[0])
        if len(parts[1].split()) >= 2:
            out.append(parts[1])
    # Latince adlarda "X; Y" ve "X / Y"
    out.extend(p.strip() for p in re.split(r';|\s/\s', base))
    res: list[tuple[str, str | None]] = []
    for v in out:
        v = v.strip(' .-')
        if not v:
            continue
        w = fwords(v)
        # Profilin kendi adı ("Metaplazi", "Atrofi") her zaman ad sayılır; yalnız türetilmiş parçalar süzülür
        if not w or (is_generic(w) and v not in (raw, base)):
            continue
        res.append((v, None))
        o = organ_of(w[0])
        if o and len(w) >= 2 and not is_generic(w[1:]) and len(' '.join(w[1:])) >= 8:
            res.append((' '.join(v.split()[1:]), o))
    return res


def stem_last(words: list[str]) -> tuple[list[str], bool]:
    """Son sözcükten iyelik/hâl ekini düşürür; açık uç (ek kabul) mümkünse True."""
    last = words[-1]
    if len(last) >= 6:
        if re.search(r's[iu]$', last) and len(last) >= 7:
            last = last[:-2]
        elif last[-1] in 'aeiou':
            last = last[:-1]
            if last[-1] in 'g':  # hastalığı → hastalig → hastali (hastalık/hastalığı ikisi de tutar)
                last = last[:-1]
    ok = len(last) >= 5
    return words[:-1] + [last], ok


class Pattern:
    def __init__(self, label: str, rx: re.Pattern, case: bool, lit: str, organ: str | None = None):
        # lit: düz alt dizgi ön süzgeci (regex yalnız bu geçiyorsa çalışır); organ: metinde ayrıca geçmesi gereken organ
        self.label, self.rx, self.case, self.lit, self.organ = label, rx, case, lit, organ


def build_patterns(d: dict) -> list[Pattern]:
    raws: list[tuple[str, str | None]] = []
    for src in [d.get('name'), *(d.get('altNames') or [])]:
        raws.extend(split_variants(src))
    raws.extend(split_variants(d.get('latinName') or ''))
    seen: set[str] = set()
    pats: list[Pattern] = []
    for v, organ in raws:
        letters = re.sub(r'[^A-Za-zÇĞİÖŞÜçğıöşü0-9]', '', v)
        if not letters:
            continue
        # Kısaltma: tümü büyük harf (rakam olabilir)
        if v == v.upper() and re.fullmatch(r'[A-ZÇĞİÖŞÜ0-9\-]+', v):
            if len(letters) < 4 or len(letters) > 7 or not re.search(r'[A-ZÇĞİÖŞÜ]{2}', v):
                continue
            key = 'C:' + v
            if key in seen:
                continue
            seen.add(key)
            pats.append(Pattern(v, re.compile(r'(?<![A-Za-z0-9ÇĞİÖŞÜçğıöşü])' + re.escape(v) + r"(?:'[a-zçğıöşü]+)?(?![A-Za-z0-9ÇĞİÖŞÜçğıöşü])"), True, v))
            continue
        words = re.sub(r'[^a-z0-9]+', ' ', fold(v)).split()
        if not words:
            continue
        joined = ' '.join(words)
        if len(joined) < 5:
            continue
        if re.fullmatch(r'[0-9 ]+', joined):
            continue
        stemmed, open_tail = stem_last(words)
        body = r'\s+'.join(re.escape(w) for w in stemmed)
        tail = r'[a-z]{0,8}' if open_tail else r'(?:[a-z]{0,3})?' if len(words[-1]) >= 5 else ''
        key = 'F:' + body + tail + (organ or '')
        if key in seen:
            continue
        seen.add(key)
        pats.append(Pattern(joined, re.compile(r'(?<=\s)' + body + tail + r'(?=\s)'), False, ' ' + stemmed[0], organ))
    return pats


def count(pats: list[Pattern], folded: str, raw: str) -> int:
    """Örtüşen varyantları bir kez saymak için en uzun eşleşmeyi esas alır (konum kümesi)."""
    spans: set[int] = set()
    for p in pats:
        target = raw if p.case else folded
        if p.lit not in target or (p.organ and ' ' + p.organ not in folded):
            continue
        for m in p.rx.finditer(target):
            spans.add(m.start() if not p.case else -1 - m.start())
    return len(spans)


# ------------------------------------------------------------------ özet → konu bağlama
STOP = set('ve ile de da md kisim ders hastaliklari hastaliklarda hastaligi hastaliklar giris genel bir icin donem sinif yeni kopya notu sunum pptx pdf'.split())


def toks(s: str) -> list[str]:
    s = fold(s)
    s = re.sub(r'\b\d{6}\b', ' ', s)
    s = re.sub(r'\bd\d+\b', ' ', s)
    return [t for t in re.findall(r'[a-z]+', s) if len(t) >= 3 and t not in STOP]


# Başlıkta biri varsa diğerinde de olmalı (ör. "Kemik Tümörleri" ≠ "Kemiğin konjenital hastalıkları", "Hastalıklar" ≠ "İlaçları")
TITLE_GUARDS = (('tumor', 'neopl', 'kanser', 'karsin'), ('konjen', 'anomal'))


def title_sim(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    for g in TITLE_GUARDS:
        if any(t.startswith(g) for t in a) != any(t.startswith(g) for t in b):
            return 0.0
    # "X Hastalıkları" (özet) ≠ "X İlaçları" (konu); "Antidepresanlar" → "Antidepresan İlaçlar" ise geçerli
    if any(t.startswith('hastal') for t in a) and any(t.startswith('ilac') for t in b):
        return 0.0

    def m(x: str, y: str) -> bool:
        return x[:5] == y[:5] if min(len(x), len(y)) >= 5 else x == y

    h1 = sum(1 for x in a if any(m(x, y) for y in b))
    h2 = sum(1 for y in b if any(m(x, y) for x in a))
    if h1 < 2 and not (len(a) == 1 and len(b) <= 2):
        return 0.0  # tek ortak sözcük ("Kemik", "Gis") bağlamaya yetmez
    return (h1 / len(a) + h2 / len(b)) / 2


def main() -> None:
    rapor = '--rapor' in sys.argv
    muf = json.loads((DATA / 'mufredat_paketi.json').read_text('utf-8'))
    summaries = json.loads((DATA / 'lectureSummariesCatalog.json').read_text('utf-8'))
    diseases = json.loads((DATA / 'diseases.json').read_text('utf-8'))
    sum_by_id = {s['id']: s for s in summaries}

    # Ders programı konuları (programdaki sıra korunur); "X" başlığı "X Y"nin önekiyse (yarım kalmış kopya) atlanır
    konular: list[dict] = []
    for k in muf['kurullar']:
        for d in k['dersler']:
            titles = d['konular']
            for t in titles:
                if any(o != t and o.startswith(t) for o in titles):
                    continue
                konular.append({'k': int(k['kurul']), 'd': d['ders'], 't': t})
    kidx = {(x['k'], x['d'], x['t']): i for i, x in enumerate(konular)}

    # Konu metinleri: kazanım (metin + alıntı + özet), çıkmış (kök + doğru şık, yalnız konu etiketi eşleşenler)
    kz_text: dict[int, list[str]] = defaultdict(list)
    ck_text: dict[int, list[str]] = defaultdict(list)
    deck_of: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for kurul in range(1, 7):
        j = json.loads((DATA / 'kazanimlar' / f'k{kurul}.json').read_text('utf-8'))
        for d in j['dersler']:
            for ko in d['konular']:
                i = kidx.get((kurul, d['ders'], ko['konu']))
                if i is None:
                    # yarım kopya başlık: uzun olanına yaz
                    cand = [x for x in kidx if x[0] == kurul and x[1] == d['ders'] and x[2].startswith(ko['konu'])]
                    if not cand:
                        continue
                    i = kidx[cand[0]]
                seen_q: set[str] = set()
                for kz in ko['kazanimlar']:
                    # k2-6 kazanımları şablon cümle ("… konusunun temel kavramlarını … açıklar"): ad yalnız başlıktan gelir,
                    # başlık ayrıca sayılır; metin yine de eklenir (şablon başlığı tekrarlar, ad yoksa eşleşme olmaz)
                    kz_text[i].append(kz.get('metin', ''))
                    kz_text[i].extend(s.get('alinti') or '' for s in kz.get('slaytlar') or [])
                    kz_text[i].extend(kz.get('ozetler') or [])
                    for s in kz.get('slaytlar') or []:
                        if s.get('deckId'):
                            deck_of[i][s['deckId']] += 1
                    for q in kz.get('cikmisSorular') or []:
                        if q['id'] in seen_q or fold(q.get('topic', '')).strip() != fold(ko['konu']).strip():
                            continue
                        seen_q.add(q['id'])
                        right = next((o['text'] for o in q.get('options') or [] if o.get('key') == q.get('correctAnswer')), '')
                        ck_text[i].append(f"{q.get('stem', '')} {right}")

    # Özet → konu: kesin (kazanım slaytındaki deste kimliği) ya da başlık benzerliği (aynı ders ≥0,6)
    sum_of: dict[int, list[str]] = defaultdict(list)
    used: set[str] = set()
    for i, decks in deck_of.items():
        for sid in decks:
            if sid in sum_by_id:
                sum_of[i].append(sid)
                used.add(sid)
    fuzzy = 0
    for s in summaries:
        if s['id'] in used:
            continue
        kur = int(s['kurul'])
        st = toks(s['title'])
        best, bi = 0.0, None
        for i, x in enumerate(konular):
            if x['k'] != kur or x['d'] != s.get('discipline'):
                continue
            v = title_sim(st, toks(x['t']))
            if v > best:
                best, bi = v, i
        if bi is not None and best >= 0.6:
            sum_of[bi].append(s['id'])
            used.add(s['id'])
            fuzzy += 1
            if '--rapor' in sys.argv:
                print(f"  özet≈konu {best:.2f}  {s['title'][:50]!r} → {konular[bi]['t'][:60]!r}")

    # Metinleri bir kez hazırla
    def prep(texts: list[str]) -> tuple[str, str]:
        raw = ' ' + ' \n '.join(texts) + ' '
        return norm_text(raw), raw

    T_title = {i: prep([x['t']]) for i, x in enumerate(konular)}
    T_kz = {i: prep(v) for i, v in kz_text.items()}
    T_ck = {i: prep(v) for i, v in ck_text.items()}
    T_sum = {i: prep([sum_by_id[s]['content'] for s in v]) for i, v in sum_of.items()}

    FLAG = {'baslik': 1, 'ozet': 2, 'kazanim': 4, 'cikmis': 8}
    out_map: dict[str, list[list[int]]] = {}
    lessons_used: set[int] = set()
    no_pattern = 0
    for d in diseases:
        pats = build_patterns(d)
        if not pats:
            no_pattern += 1
            continue
        rows = []
        for i in range(len(konular)):
            n_t = count(pats, *T_title[i])
            n_k = count(pats, *T_kz[i]) if i in T_kz else 0
            n_c = count(pats, *T_ck[i]) if i in T_ck else 0
            n_s = count(pats, *T_sum[i]) if i in T_sum else 0
            if not (n_t or n_k or n_c or n_s >= 2):
                continue
            flags = (FLAG['baslik'] if n_t else 0) | (FLAG['ozet'] if n_s else 0) | (FLAG['kazanim'] if n_k else 0) | (FLAG['cikmis'] if n_c else 0)
            rows.append([i, n_k + n_c + n_s + n_t, flags])
        if rows:
            rows.sort(key=lambda r: -r[1])
            out_map[d['id']] = rows
            lessons_used.update(r[0] for r in rows)

    # Yalnız hastalık içeren konular yazılır; dizinler yeniden numaralanır (programdaki sıra korunur)
    keep = sorted(lessons_used)
    remap = {old: new for new, old in enumerate(keep)}
    out_konular = []
    for old in keep:
        x = konular[old]
        decks = sorted(deck_of.get(old, {}).items(), key=lambda kv: -kv[1])
        deck = next((dk for dk, _ in decks if not dk.startswith('sum-')), None)
        out_konular.append({'k': x['k'], 'd': x['d'], 't': x['t'], **({'deck': deck} if deck else {}), 'ozet': len(sum_of.get(old, []))})
    out_map = {did: [[remap[r[0]], r[1], r[2]] for r in rows] for did, rows in out_map.items()}

    total = len(diseases)
    matched = len(out_map)
    payload = {
        'v': 1,
        'uretim': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'yontem': 'Ad/eş ad/Latince ad sözcük sınırıyla; kaynak: konu başlığı, kazanım metni, konu etiketli çıkmış soru, '
                  'konuya bağlı amfi ders özeti (≥2 geçiş). Bayrak: 1 başlık · 2 ders özeti · 4 kazanım · 8 çıkmış.',
        'kapsam': {
            'profil': total, 'eslesen': matched, 'konu': len(konular), 'konuHastalikli': len(keep),
            'ozetKonuya': len(used), 'ozetToplam': len(summaries), 'ozetBenzerlikle': fuzzy, 'adsiz': no_pattern,
        },
        'kurullar': [{'k': int(k['kurul']), 'ad': k.get('ad', '')} for k in muf['kurullar']],
        'konular': out_konular,
        'hastaliklar': out_map,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), 'utf-8')
    print(f"{OUT.relative_to(ROOT)}: {matched}/{total} profil ({matched / total:.0%}) · {len(keep)}/{len(konular)} konu · "
          f"özet {len(used)}/{len(summaries)} konuya bağlı ({fuzzy} başlık benzerliğiyle) · {OUT.stat().st_size // 1024} KB")
    if rapor:
        by_k = defaultdict(int)
        for rows in out_map.values():
            for k in {out_konular[r[0]]['k'] for r in rows}:
                by_k[k] += 1
        print('Kurul başına profil:', dict(sorted(by_k.items())))
        miss = [d['name'] for d in diseases if d['id'] not in out_map]
        print(f'Eşleşmeyen {len(miss)} profil (ilk 40):', '; '.join(miss[:40]))
        sizes = sorted(((len(rows), did) for did, rows in out_map.items()), reverse=True)[:12]
        print('En çok konuda geçenler:', ', '.join(f'{did} {n}' for n, did in sizes))


if __name__ == '__main__':
    main()
