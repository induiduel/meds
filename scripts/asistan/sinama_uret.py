#!/usr/bin/env python3
"""Anlama sınama seti üretir → scripts/asistan/sinama/anlama.jsonl (sabit tohum; her çalıştırmada aynı).
Grup A: elle yazılmış doğal sorular (niyet kurallarından bağımsız yazıldı). Grup B: gerçek varlıklarla şablon + gürültü
(ASCII, harf yer değiştirme, büyük harf, ünlemsiz telgraf). Alan: q, niyet, ek (beklenen ikincil, isteğe bağlı), varlik, grup."""
import json, os, random, re
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
random.seed(20261029)
A = {
 'tanim': ["anamnez nedir", "Parkinson hastalığı ne demek", "multipl skleroz hakkında bilgi verir misin", "apoptoz nedir", "hipertansiyon tanımı", "granülom ne anlama geliyor", "nekroz kavramını açıkla", "wilms tümörü nedir"],
 'etiyoloji': ["pyelonefritin nedenleri neler", "böbrek taşı neden oluşur", "migrenin risk faktörleri", "hangi etkenler üriner enfeksiyona yol açar", "iskemik inmenin sebebi nedir", "kolelitiazis için risk faktörleri"],
 'patogenez': ["akut enflamasyon nasıl gelişir", "amiloidoz patogenezi", "ateroskleroz nasıl oluşur", "kronik pyelonefritin makroskopik görünümü", "tüberkülozda granülom mekanizması", "iskemik hasarın patofizyolojisi"],
 'belirti': ["migren belirtileri nelerdir", "kızamık klinik bulguları", "hangi bulgularla seyreder gonore", "nefrotik sendromun belirtileri", "Parkinson hastasında ne görülür", "menenjitin semptomları"],
 'tani': ["tüberküloz tanısı nasıl konur", "SLE tanı kriterleri", "hepatit B için hangi testler istenir", "Wilms tümöründe tanı için ne yapılır", "multipl sklerozda altın standart tanı", "biyopsi ile hangi hastalık tanınır"],
 'tedavi': ["gonore tedavisi nasıl", "migrende ilk basamak tedavi", "akut pyelonefrit nasıl tedavi edilir", "sifiliz için ne verilir", "tüberküloz tedavi şeması", "böbrek taşında cerrahi yaklaşım"],
 'komplikasyon': ["diyabetin komplikasyonları", "pyelonefritin komplikasyonları nelerdir", "inme sonrası ne gibi sorunlar çıkar", "kronik hepatit hangi komplikasyonlara yol açar"],
 'prognoz': ["Wilms tümörünün prognozu", "ALS hastalarında sağkalım", "multipl skleroz seyri nasıl", "kronik böbrek yetmezliği iyileşir mi"],
 'sayi': ["Wilms tümörü kaç yaşta görülür", "kolorektal kanser sıklığı yüzde kaç", "gebelikte asemptomatik bakteriüri oranı", "nefrotik sendromda proteinüri kaç gram", "tüberkülozda inkübasyon kaç hafta", "hastalığın insidansı nedir"],
 'ilac_mekanizma': ["nistatinin etki mekanizması", "ketokonazol nasıl etki eder", "penisilin ne yapar hücrede", "amfoterisin B mekanizması", "sefalosporinler nasıl çalışır"],
 'endikasyon': ["nistatin ne için kullanılır", "doksisiklin hangi hastalıklarda verilir", "ketokonazolün endikasyonları", "seftriakson ne zaman kullanılır"],
 'kontrendikasyon': ["gebelikte doksisiklin verilir mi", "ACE inhibitörü kimlere verilmez", "tetrasiklin kontrendikasyonları", "NSAİİ kullanılmaz hangi durumlarda"],
 'yan_etki': ["amfoterisin B yan etkileri", "aminoglikozit toksisitesi", "kortikosteroidin istenmeyen etkileri", "ketokonazol advers etkileri neler"],
 'etkilesim': ["varfarin ile hangi ilaçlar etkileşir", "ketokonazol ve simvastatin birlikte kullanılır mı", "rifampisinin ilaç etkileşimleri"],
 'doz': ["benzatin penisilin kaç mg verilir", "seftriakson dozu", "gonore için tek doz seftriakson kaç gram", "doksisiklin kullanım şekli"],
 'goruntuleme': ["böbrek taşında hangi görüntüleme", "pyelonefrit BT bulguları", "inmede MR bulguları", "akciğer tüberkülozu röntgen görüntüsü"],
 'laboratuvar': ["nefrotik sendromda kan değerleri", "hepatitte transaminaz düzeyi", "pyelonefritte laboratuvar bulguları", "kreatinin normal değeri ne"],
 'ayirici_tani': ["Parkinson ayırıcı tanısı", "migren neyle karışır", "böbrek kitlelerinde ayırıcı tanı", "bu hastalığı hangi hastalıkla ayırt ederiz ayırıcı tanıda"],
 'karsilastir': ["ciddi ve hafif pyelonefrit arasındaki fark", "Crohn ile ülseratif kolit farkı", "tip 1 ve tip 2 diyabeti karşılaştır", "bakteriyel ile viral menenjit nasıl ayırt edilir"],
 'kisaltma': ["ADH açılımı nedir", "MS kısaltması neyin kısaltması", "AIDS açılımı", "KOAH uzun hali"],
 'cikmis_soru': ["pyelonefrit çıkmış sorular", "hepatit sınavda çıktı mı", "daha önce sorulmuş mu bu konu", "2022 kurul 3 çıkmış soruları göster", "geçmiş sınavlarda amiloidoz", "Parkinson kaç kez çıkmış"],
 'ornek_soru': ["bana nöroloji sorusu ver", "örnek soru getir enfeksiyon", "beni sına", "mini sınav yapalım", "patolojiden soru sor", "5 soruluk deneme istiyorum"],
 'git': ["sesli soru çözücü nerede", "son prova sayfasına git", "çıkmış sorulara nasıl giderim", "sözlüğü aç", "kamplar bölümüne yönlendir", "en önemliler ekranı nerede"],
 'ses_cal': ["Parkinson'u sesli anlat", "bu dersi seslendir", "sesli dersi oynat", "migren anlatımını dinlemek istiyorum"],
 'goster': ["böbrek taşı resmini göster", "granülom mikroskop görüntüsü", "akut enflamasyon şeması", "bu hastalığın görselini ver"],
 'tablo': ["tüberküloz ilaçları tablosu", "ders içeriğindeki tabloyu göster", "karşılaştırma tablosu var mı", "fizyolojik değerler tablosu"],
 'site_yardim': ["bu site ne işe yarar", "hesabımı nasıl silerim", "ATP puanı nedir", "karanlık temaya nasıl geçerim", "çevrimdışı kullanabilir miyim", "hata bildirmek istiyorum"],
 'calisma_onerisi': ["bugün ne çalışayım", "zayıf konularım neler", "çalışma planı yap", "nereden başlayayım"],
 'selam': ["merhaba", "selam", "günaydın", "naber"],
 'tesekkur': ["teşekkürler", "sağ ol", "çok teşekkür ederim", "eyvallah"],
 'veda': ["görüşürüz", "hoşça kal", "iyi geceler"],
}
g = json.load(open(os.path.join(KOK, 'src/data/medical_glossary.json'), encoding='utf-8'))
def adlar(kat, n):
    out = []
    for v in g.values():
        if v.get('category') != kat: continue
        t = re.sub(r'\s*\(.*?\)', '', v.get('term', '')).strip()
        if 3 <= len(t) <= 28 and len(t.split()) <= 3: out.append(t)
    random.shuffle(out); return out[:n]
H, D = adlar('hastalik', 140), adlar('ilac', 60)
SAB = {
 'tanim': ["{h} nedir", "{h} ne demek", "{h} hakkında bilgi ver"], 'etiyoloji': ["{h} neden olur", "{h} nedenleri neler", "{h} risk faktörleri"],
 'patogenez': ["{h} patogenezi", "{h} nasıl gelişir", "{h} mikroskopik bulguları"], 'belirti': ["{h} belirtileri", "{h} bulguları nelerdir", "{h} klinik bulguları"],
 'tani': ["{h} tanısı nasıl konur", "{h} tanı kriterleri", "{h} için hangi test istenir"], 'tedavi': ["{h} tedavisi", "{h} nasıl tedavi edilir", "{h} ilk basamak tedavi"],
 'komplikasyon': ["{h} komplikasyonları", "{h} ne gibi komplikasyonlara yol açar"], 'prognoz': ["{h} prognozu", "{h} seyri nasıl"],
 'sayi': ["{h} kaç yaşta görülür", "{h} sıklığı nedir", "{h} insidansı"], 'ayirici_tani': ["{h} ayırıcı tanısı", "{h} neyle karışır"],
 'goruntuleme': ["{h} radyolojik bulguları", "{h} BT bulguları"], 'laboratuvar': ["{h} laboratuvar bulguları", "{h} kan değerleri"],
 'cikmis_soru': ["{h} çıkmış sorular", "{h} sınavda çıktı mı", "{h} daha önce sorulmuş mu"], 'ornek_soru': ["{h} örnek soru ver", "{h} hakkında soru sor", "bana {h} sorusu getir"],
 'git': ["{h} sayfasına git", "{h} nerede", "{h} dersini aç"], 'ses_cal': ["{h} sesli anlat", "{h} sesli dersini çal", "{h} anlatımını dinle"],
 'goster': ["{h} resmini göster", "{h} görseli", "{h} mikroskop görüntüsü göster"], 'tablo': ["{h} tablosu", "{h} karşılaştırma tablosu"],
 'karsilastir': ["{h} ile {h2} farkı", "{h} ve {h2} arasındaki fark"],
 'yan_etki': ["{d} yan etkileri", "{d} advers etkileri"], 'kontrendikasyon': ["{d} kontrendikasyonları", "{d} kimlere verilmez"],
 'endikasyon': ["{d} endikasyonları", "{d} ne için kullanılır"], 'ilac_mekanizma': ["{d} etki mekanizması", "{d} nasıl etki eder"],
 'doz': ["{d} dozu", "{d} kaç mg verilir"], 'etkilesim': ["{d} ilaç etkileşimleri", "{d} ile birlikte kullanılır mı"],
}
ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
def gurultu(s):
    r = random.random()
    if r < 0.30: return s.translate(ASCII).replace('İ', 'I')
    if r < 0.45:
        w = s.split(' ')
        i = random.randrange(len(w)); t = w[i]
        if len(t) > 5:
            j = random.randrange(1, len(t) - 2); w[i] = t[:j] + t[j + 1] + t[j] + t[j + 2:]
        return ' '.join(w)
    if r < 0.55: return s.upper().replace('I', 'I')
    if r < 0.65: return s.lower() + '?'
    return s
cikti = [{'q': q, 'niyet': n, 'grup': 'A'} for n, l in A.items() for q in l]
ha = 0; da = 0
hedef = 340 / sum(len(v) for v in SAB.values())
for n, sab in SAB.items():
    for t in sab:
        for _ in range(max(1, round(hedef))):
            h = H[ha % len(H)]; ha += 1; h2 = H[ha % len(H)]; ha += 1; d = D[da % len(D)]; da += 1
            q = t.format(h=h, h2=h2, d=d)
            cikti.append({'q': gurultu(q), 'niyet': n, 'varlik': (d if '{d}' in t else h), 'grup': 'B'})
random.shuffle(cikti)
os.makedirs(os.path.join(KOK, 'scripts/asistan/sinama'), exist_ok=True)
with open(os.path.join(KOK, 'scripts/asistan/sinama/anlama.jsonl'), 'w', encoding='utf-8') as f:
    for c in cikti: f.write(json.dumps(c, ensure_ascii=False) + '\n')
print(len(cikti), 'soru;', sum(1 for c in cikti if c['grup'] == 'A'), 'A,', sum(1 for c in cikti if c['grup'] == 'B'), 'B')
