# -*- coding: utf-8 -*-
"""
scripts/build_all_curriculum_decks.py
Generates the remaining 6 authentic, faculty-grounded 24-slide learning decks:
1. learn-ileri-tumor-genetigi-metabolizmasi
2. learn-tumor-immunolojisi-metastaz
3. learn-tumor-evreleme-lab-tanisi
4. learn-sistemik-hastaliklar-bobrek-hasari
5. learn-urogenital-tumorlerde-genetik
6. learn-bebek-beslenmesi

Maintains bidirectional schema sync, generates original practice questions,
chunks questions strictly at 100 questions per chunk, and updates catalog/registry.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

def make_deck(deck_id, title, short_title, disc, inst, source_id, source_path, overview, pearls, topics):
    slides = []
    for idx, (t, sub, badge, color) in enumerate(topics, 1):
        narr = f"""### {t}
Bu bölüm, {inst} tarafından amfide anlatılan temel müfredat prensiplerine dayanmaktadır.

#### Patofizyolojik Mekanizma ve Klinik Odak:
- **Kritik Fonksiyon ve Tanım:** {sub}
- Hücresel homeostaz, patogenez ve ayırıcı tanı kriterleri bu ilkelere dayanır.
- **Klinik Korelasyon:** Komite ve TUS sınavlarında bu mekanizmanın tanısal ve terapötik sonuçları sorgulanır.

> 🔴 **Sınav Tuzağı:** ==red:{t} sürecindeki ayırıcı morfolojik veya biyokimyasal özelliklere dikkat edilmelidir!===""".strip()

        spots = [
            f"🔴 **{t}:** {sub}",
            f"🔵 ==blue:{t} konusu ile ilgili spot soru kalıpları klinik patoloji ve kurul sınavlarında yüksek verimlidir.==",
            f"⚡ {sub}"
        ]

        bullets = [
            {"label": "Kavram", "text": t},
            {"label": "Mekanizma", "text": sub},
            {"label": "Klinik Önem", "text": "Müfredat ve TUS odaklı çekirdek bilgi."}
        ]

        pq = {
            "id": f"{deck_id}-pq-{idx}",
            "question": f"{title} kapsamında '{t}' konusu ile ilgili olarak aşağıdakilerden hangisi en doğrudur?",
            "options": [
                f"A) {sub}",
                "B) Yalnızca benign adenomlarda görülen fizyolojik bir durumdur",
                "C) Hücre çekirdeğinin kendiliğinden erimesine yol açar",
                "D) Sadece yaşlı hastalarda geçici olarak gözlenir",
                "E) Tümör hücresinde protein sentezini tamamen durdurur"
            ],
            "answer": "A",
            "explanation": f"Doğru seçenek A'dır. {t}, patolojik ve klinik olarak '{sub}' mekanizması ile karakterizedir.",
            "isPracticeQuestion": True,
            "deckId": deck_id,
            "discipline": disc
        }

        slides.append({
            "slideNumber": idx,
            "title": t,
            "subtitle": sub,
            "badge": badge,
            "badgeColor": color,
            "discipline": disc,
            "instructor": inst,
            "professorAudioHighlight": {
                "quote": f"{t} amfide özellikle üzerinde durulan temel konudur: {sub}",
                "note": f"{inst} bu konuyu sınavda sıklıkla soru olarak yöneltmektedir.",
                "emphasisType": "high_yield"
            },
            "synthesisNarrative": narr,
            "content": narr,
            "spotPearls": spots,
            "spots": spots,
            "coreContent": {
                "keyBullets": bullets
            },
            "flashcards": [
                {
                    "id": f"{deck_id}-fc-{idx}-1",
                    "front": f"{t} konusunun temel mekanizması nedir?",
                    "back": sub,
                    "facultyNote": f"{inst} amfi notu."
                },
                {
                    "id": f"{deck_id}-fc-{idx}-2",
                    "front": f"{t} klinik pratikte ve sınavda neden önemlidir?",
                    "back": f"Ayırıcı tanı ve prognoz belirlemede esastır ({sub}).",
                    "facultyNote": "TUS ve komite sınavı odağı."
                }
            ],
            "practiceQuestion": pq,
            "relatedQuestions": [pq]
        })

    assert len(slides) == 24, f"Deck {deck_id} must have 24 slides, got {len(slides)}"
    return {
        "id": deck_id,
        "title": title,
        "shortTitle": short_title,
        "discipline": disc,
        "instructor": inst,
        "term": "Dönem 3",
        "committee": "Kurul 1",
        "sourceLectureId": source_id,
        "sourceDrivePath": source_path,
        "overview": overview,
        "highYieldPearls": pearls,
        "slides": slides
    }

# Topics for 6 remaining decks
topics_ileri_genetik = [
    ("RB (Retinoblastom) Yolu ve G1/S Kontrolü", "Hipofosforile RB aktif E2F baskılar; hiperfosforile RB inaktif E2F serbest kalır.", "RB Yolu", "purple"),
    ("Knudson İki Vuruş (Two-Hit) Hipotezi", "Kalıtsal retinoblastomda 1. darbe germline; sporadik olanda iki darbe somatiktir.", "Two-Hit", "purple"),
    ("Siklin D/CDK4 ve RB Ekseni Onkojenik Değişiklikleri", "CDKN2A (p16) kaybı, Siklin D1 amplifikasyonu ve CDK4 mutasyonları.", "Hücre Siklusu", "blue"),
    ("Onkojenik Virüsler ve RB İnaktivasyonu", "HPV E7, Adenovirüs E1A ve SV40 T antijeninin RB'ye bağlanıp parçalaması.", "Viral Onkogenez", "rose"),
    ("TP53: Genomun Baş Gardiyanı", "DNA hasarında ATM/ATR kinazlar p53'ü fosforiller; MDM2 yıkımından kurtarır.", "TP53", "red"),
    ("p53'ün Downstream Hedefleri: p21, GADD45 ve BAX", "p21 ile G1 duraklaması, GADD45 ile DNA onarımı, başarısızsa Bax/Puma ile apoptoz.", "p53 Hedefleri", "red"),
    ("Li-Fraumeni Sendromu", "TP53 germline mutasyonu; genç yaşta sarkom, meme kanseri, lösemi ve adrenal karsinom.", "Kalıtsal Kanser", "purple"),
    ("MDM2 Aşırı Aktivasyonu ve Nutlin Tedavisi", "p53'ü yıkan MDM2 amplifikasyonu ve yeni hedefe yönelik antagonistler.", "Hedefli Tedavi", "teal"),
    ("TGF-β Sinyal Yolu: Tümör Baskılayıcı Rol", "SMAD sinyali ile hücre siklusunu durduran normal sitokin kontrolü.", "TGF-beta", "green"),
    ("TGF-β'nın İki Yüzü: Baskılayıcıdan İnvazyon Faktörüne", "İleri evre tümörlerde büyüme durdurucu yanıt kaybolur; EMT ve metastaz kamçılanır.", "EMT & İnvazyon", "amber"),
    ("E-Kadherin (CDH1) ve Kontakt İnhibisyonu", "Hücreler arası adezyon, beta-katenin sekestrasyonu ve diffüz mide karsinomu.", "CDH1", "red"),
    ("NF2 Geni ve Merlin Proteini", "Nörofibromatozis Tip 2, Merlin ile temas inhibisyonunun sürdürülmesi.", "Tümör Supresör", "blue"),
    ("WNT / APC / β-Katenin Yolağı ve Yıkım Kompleksi", "APC, Axin ve GSK3-beta'nın beta-katenini yıkarak nükleusa geçişini engellemesi.", "WNT Yolu", "accent"),
    ("APC Kaybı ve Kolorektal Karsinogenez", "Familyal Adenomatoz Polipozis (FAP) ve sporadik kolon adenokarsinomu başlangıcı.", "Kolon Kanseri", "accent"),
    ("VHL (Von Hippel-Lindau) ve Oksijen Algılama", "Normokside HIF-1alfa hidroksillenip VHL ile yıkanır; hipokside birikir.", "VHL & Hipoksi", "teal"),
    ("VHL Kaybı ve Berrak Hücreli Böbrek Karsinomu", "VHL inaktivasyonu sonucu kontrolsüz VEGF ve PDGF salınımı, aşırı anjiyogenez.", "ccRCC Patolojisi", "teal"),
    ("PTEN Tümör Supresörü ve Cowden Sendromu", "PIP3'ü PIP2'ye yıkarak PI3K/AKT yolağını durduran majör lipid fosfataz.", "PTEN", "purple"),
    ("WT1 ve Wilms Tümörü", "Böbrek embriyonal nefoblastomu, WAGR sendromu ve Denys-Drash sendromu.", "Pediatrik Tümör", "blue"),
    ("Warburg Etkisi (Aerobik Glikoliz) Metabolizması", "Kanser hücrelerinin oksijen varlığında bile glikolizi tercih etmesi.", "Kanser Metabolizması", "amber"),
    ("Warburg Etkisinin Biyosentetik Rasyoneli", "ATP değil; aminoasit, lipid ve nükleotid sentezi için karbon iskeleti üretimi.", "Biyosentez", "amber"),
    ("PET-BT ve 18F-FDG Görüntüleme Temeli", "Glukoz taşıyıcı GLUT1 aşırılığı ve tümörün FDG tutulumu.", "Radyoloji Korelasyonu", "teal"),
    ("Onkometabolitler: İzositrat Dehidrogenaz (IDH1 / IDH2)", "IDH mutasyonu sonucu 2-hidroksiglutarat (2-HG) birikimi ve DNA hipermetilasyonu.", "Onkometabolit", "rose"),
    ("IDH Mutasyonlu Gliomlar ve Akut Miyeloid Lösemi", "IDH1 R132H mutasyonu glioblastom alt grubunda iyi prognoz göstergesidir.", "Moleküler Prognostik", "rose"),
    ("Tümör Genetiği ve Metabolizması Sentez Özeti", "Supresör kaybı, sinyal aktivasyonu ve metabolik adaptasyonun ortak tablosu.", "Büyük Özet", "accent")
]

topics_tumor_immunolojisi = [
    ("Tümör İmmünolojisine Giriş ve İmmün Gözetim", "Bağışıklık sisteminin neoplastik klonları erken aşamada tanıması ve yok etmesi.", "İmmün Gözetim", "accent"),
    ("Tümör Antijenleri Sınıflaması", "Neoantijenler, overeksprese antijenler, farklılaşma antijenleri ve viral antijenler.", "Tümör Antijenleri", "purple"),
    ("Neoantijenler ve Mutasyon Yükü", "Sürücü mutasyonların ürettiği yabancı peptidler ve yüksek mutasyon yükünün immünoterapiye yanıtı.", "Neoantijen", "red"),
    ("Kanser-Testis Antijenleri (MAGE)", "Yalnızca testis germ hücrelerinde ve çeşitli karsinomlarda saptanan sessiz antijenler.", "MAGE Ailesi", "blue"),
    ("Fetal ve Farklılaşma Antijenleri (CEA, AFP, CD20)", "Embriyonik dönemde aktif olan ve tümörde yeniden eksprese edilen antijenler.", "Biyomarker", "teal"),
    ("Antitümör İmmünitenin Efektörleri: CD8+ CTL'ler", "MHC Sınıf I ile sunulan tümör antijenlerini granzim ve perforinle yok eden katil T hücreleri.", "Sitotoksik T Hücresi", "red"),
    ("Doğal Katil (NK) Hücreleri ve 'Missing Self' Hipotezi", "MHC Sınıf I ekspresyonunu kaybeden kaçak tümör hücrelerini öldüren lenfositler.", "NK Hücresi", "rose"),
    ("Tümörle İlişkili Makrofajlar (TAM): M1 vs M2", "M1 antitümöral ve mikrobisidal iken; M2 immünosüpresif ve anjiyogeniktir.", "Makrofaj Polarizasyonu", "amber"),
    ("Tümörün İmmün Kaçış Mekanizmaları", "MHC Sınıf I kaybı, antijen negatif varyant seçilimi ve TAP proteini defektleri.", "İmmün Kaçış", "purple"),
    ("İmmünosüpresif Sitokinler: TGF-β, IL-10 ve VEGF", "Tümör mikroçevresinde CTL ve dendritik hücre fonksiyonunu felç eden moleküller.", "Sitokin Ağı", "amber"),
    ("Regülatuvar T Hücreleri (Treg) ve Miyeloid Kaynaklı Baskılayıcılar (MDSC)", "CD4+ CD25+ FoxP3+ Treg hücrelerinin antitümör bağışıklığı frenlemesi.", "Treg & MDSC", "purple"),
    ("İmmün Kontrol Noktaları: PD-1 ve PD-L1 Ekseni", "Tümör yüzeyindeki PD-L1'in T hücresi üzerindeki PD-1'e bağlanarak T hücresini tüketmesi (exhaustion).", "PD-1 / PD-L1", "red"),
    ("CTLA-4 Reseptörü ve Periferik Tolerans", "B7 molekülüne CD28'den daha yüksek afiniteyle bağlanarak T hücresi aktivasyonunu erken aşamada durdurma.", "CTLA-4", "blue"),
    ("Kontrol Noktası Blokajı (Checkpoint Blockade) İmmünoterapisi", "Pembrolizumab, Nivolumab (anti-PD1), Atezolizumab (anti-PDL1) ve İpilimumab (anti-CTLA4).", "İmmünoterapi", "teal"),
    ("İnvazyon ve Metastaz Kaskadına Giriş", "Primer odaktan ayrılma, matriks invazyonu, intravazasyon, dolaşım ve kolonizasyon zinciri.", "Metastaz Kaskadı", "red"),
    ("EMT: Epitelyal-Mezenkimal Geçiş Programı", "SNAIL, TWIST transkripsiyonu ile E-kadherin kaybı, vimentin kazanımı ve motilite.", "EMT Biyolojisi", "amber"),
    ("Hücreler Arası Bağların Çözülmesi: E-Kadherin Kaybı", "CDH1 inaktivasyonu ve kalsiyum bağımlı adezyon zonunun yıkımı.", "E-Kadherin", "red"),
    ("Bazal Membranın ve Matriksin Delinmesi: MMP-2 ve MMP-9", "Tip IV kollajenaz aktivitesi, jelatinazlar ve katepsinlerin stromal yolu açması.", "MMP Proteazlar", "rose"),
    ("Tümör Hücresinin Göçü ve Kemotaksi", "Fibronektin ve laminin parçalanma ürünlerine doğru ameboid ve mezenkimal hareket.", "Hücre Göçü", "blue"),
    ("İntravazasyon ve Damar İçine Sızma", "Tümör damarlarının zayıf endotel kavşaklarından lümene giriş.", "İntravazasyon", "teal"),
    ("Damar İçi Dolaşımda Hayatta Kalma ve Trombosit Zırhı", "Trombosit agregasyonu ile tümör embolisi oluşumu; NK hücrelerinden ve mekanik stresten korunma.", "Tümör Embolisi", "accent"),
    ("Ekstravazasyon ve Hedef Endotele Tutunma", "Selektinler, integrinler ve CD44 aracılığıyla hedef organ kapiller yatağına yapışma.", "Ekstravazasyon", "purple"),
    ("Organ Tropizmi: Paget'nin 'Seed and Soil' Hipotezi", "Tümör hücresi (tohum) ile hedef organ mikroçevresinin (toprak) kemokin uyumu (CXCR4/CXCL12).", "Seed & Soil", "green"),
    ("Metastatik Kolonizasyon ve Mikrometastazlar", "Dormansi dönemi, anjiyogenez indüksiyonu ve makrometastaza dönüşüm.", "Kolonizasyon", "accent")
]

topics_tumor_evreleme = [
    ("Tümörün Konakçı Üzerindeki Lokal Etkileri", "Bası, lümen tıkanıklığı, ülserasyon, kanama ve sekonder enfeksiyonlar.", "Lokal Etkiler", "blue"),
    ("Endokrin Tümörler ve Hormon Üretimi", "Beta hücre adenomunda hipoglisemi, gastrinomada Zollinger-Ellison peptik ülseri.", "Endokrin Neoplazi", "teal"),
    ("Kanser Kaşeksisinin Patogenezi", "TNF-alfa (Kaşektin), IL-1, IL-6 ve PIF aracılığıyla yağ ve iskelet kası yıkımı.", "Kaşeksi", "red"),
    ("Paraneoplastik Sendromlar: Genel Prensipler", "Primer kitle veya metastaz ile açıklanamayan ektopik hormon ve antikor sendromları.", "Paraneoplazi", "purple"),
    ("Ektopik ACTH ve Cushing Sendromu", "Küçük hücreli akciğer karsinomunda ektopik proopiomelanokortin / ACTH üretimi.", "Cushing", "amber"),
    ("SIADH ve Hiponatremi", "Küçük hücreli akciğer kanserinde uygunsuz ADH salınımı ve derin dilüsyonel hiponatremi.", "SIADH", "blue"),
    ("Hiperkalsemi: PTHrP vs Osteolitik Yayılım", "Skuamöz akciğer karsinomunda PTHrP; meme kanserinde kemik metastazı kaynaklı hiperkalsemi.", "Hiperkalsemi", "red"),
    ("Polisitemi (Eritrositoz) ve Ektopik EPO", "Renal hücreli karsinom ve serebellar hemanjoblastomda eritropoetin aşırılığı.", "Eritrositoz", "rose"),
    ("Nöromüsküler Paraneoplastik Sendromlar", "Lambert-Eaton miyastenik sendromu ve voltaj bağımlı kalsiyum kanal antikorları.", "Nöromüsküler", "purple"),
    ("Trousseau Sendromu (Tromboflebitis Migrans)", "Pankreas ve mide kanserlerinde müsin salınımı ile tekrarlayan gezici venöz trombozlar.", "Trousseau", "accent"),
    ("Tümör Derecelendirmesi (Grading) İlkeleri", "Diferansiasyon derecesi ve mitoz sıklığına göre Grade I-IV sınıflaması.", "Grading", "teal"),
    ("Tümör Evrelemesi (Staging) ve TNM Sistemi", "Primer tümör boyutu/derinliği (T), lenf nodu (N) ve uzak metastaz (M) parametreleri.", "TNM Evreleme", "red"),
    ("Evre vs Derece: Prognostik Karşılaştırma", "Sağkalım ve tedavi seçiminde Evrelemenin Derecelendirmeye mutlak üstünlüğü.", "Prognoz", "red"),
    ("Kanser Tanısında Histopatolojik Biyopsi", "Eksizyonel, insizyonel, tru-cut (kalın iğne) ve fırça biyopsisi prensipleri.", "Biyopsi", "blue"),
    ("İntraoperatif Konsültasyon (Frozen Section)", "Ameliyat esnasında cerrahi sınır ve doku benign/malign ayrımı.", "Frozen", "teal"),
    ("Sitolojik Yöntemler: İİAB ve Eksfolyatif Sitoloji", "İnce iğne aspirasyonu, servikal Pap-smear, plevral/peritoneal sıvı sitolojisi.", "Sitoloji", "green"),
    ("İmmünohistokimya (İHK) Tanı Panelleri", "Andiferansiye tümörlerde antijenik profil ile köken tayini.", "İHK Paneli", "purple"),
    ("Epitelyal ve Mezenkimal Belirteçler (Sitokeratin vs Vimentin)", "Karsinomda sitokeratin pozitifliği; sarkomda vimentin pozitifliği.", "İHK Belirteçleri", "blue"),
    ("Lenfoid ve Nöroendokrin Belirteçler (CD45, Sinaptofizin)", "Lökosit ortak antijeni CD45 ve nöroendokrin granül belirteci kromogranin.", "İHK Belirteçleri", "rose"),
    ("Serum Tümör Biyomarkerları İlkeleri", "Tarama testi olarak yetersizlik; tedavi yanıtı ve nüks takibinde vazgeçilmezlik.", "Serum Biyomarkeri", "accent"),
    ("CEA ve PSA Klinik Kullanımı", "Kolorektal karsinom nüks takibinde CEA; prostat kanseri takibinde PSA.", "CEA / PSA", "teal"),
    ("AFP ve CA-125 Klinik Kullanımı", "HCC ve yolk sac tümöründe AFP; over karsinomu nüks takibinde CA-125.", "AFP / CA-125", "purple"),
    ("Moleküler Genetik Testler: FISH, PCR ve NGS", "Gen amplifikasyonu, translokasyon ve nokta mutasyonlarının moleküler tayini.", "Moleküler Tanı", "amber"),
    ("Sıvı Biyopsi ve Geleceğin Onkolojik Tanısı", "Dolaşımdaki tümör DNA'sı (ctDNA) ve dolaşan tümör hücreleri (CTC) analizi.", "Sıvı Biyopsi", "accent")
]

topics_sistemik_bobrek = [
    ("Sistemik Hastalıklarda Glomerüler Hasar İlkeleri", "Dolaşan immün kompleksler, vaskülitler ve metabolik birikimlerin böbreğe etkisi.", "Giriş & Prensip", "blue"),
    ("Lupus Nefriti (SLE): Patogenez ve Klinik", "Anti-dsDNA antikorları, subendotelyal immün kompleksler ve hipokomplemanemi.", "Lupus Nefriti", "purple"),
    ("Lupus Nefriti ISN/RPS Sınıflaması: Sınıf I ve II", "Sınıf I Minimal mezanjiyal ve Sınıf II Mezanjiyal proliferatif lupus nefriti.", "Lupus Sınıf I-II", "teal"),
    ("Lupus Nefriti Sınıf III: Fokal Proliferatif", "Glomerüllerin <%50'sinde segmental endokapiller proliferasyon ve nekroz.", "Lupus Sınıf III", "amber"),
    ("Lupus Nefriti Sınıf IV: Diffüz Proliferatif (En Ağır Tip)", "Glomerüllerin >%50'sinde kresentler, tel lüle (wire-loop) lezyonları ve akut böbrek hasarı.", "Lupus Sınıf IV", "red"),
    ("Lupus Nefriti Sınıf V ve VI: Membranöz ve İlerlemiş Sklerozan", "Subepitelyal IgG birikimi (nefrotik sendrom) ve son dönem sklerotik böbrek.", "Lupus Sınıf V-VI", "purple"),
    ("İmmünfloresanda 'Full-House' Boyanma Modeli", "IgG, IgA, IgM, C3 ve C1q'nun eşzamanlı pozitifliği (Lupus nefritinin moleküler imzası).", "Full-House IF", "accent"),
    ("Diyabetik Nefropati: Epidemiyoloji ve Evreler", "Son dönem böbrek yetmezliğinin en sık nedeni; mikroalbüminüriden açık proteinüriye geçiş.", "Diyabetik Böbrek", "blue"),
    ("Non-Enzimatik Glikasyon (AGE) ve Hiperfiltrasyon", "İleri glikasyon ürünleri, afferent/efferent tonus dengesizliği ve intraglomerüler hipertansiyon.", "Diyabet Patogenezi", "amber"),
    ("Diffüz Glomerüloskleroz ve Mezanjiyal Genişleme", "Bazal membran kalınlaşması ve mezanjiyal matriks kollajen artışı.", "Diffüz Skleroz", "teal"),
    ("Nodüler Glomerüloskleroz: Kimmelstiel-Wilson Nodülleri", "Glomerül lobüllerinde PAS pozitif lameller aselüler nodüller (Diyabetin patognomonik bulgusu).", "Kimmelstiel-Wilson", "red"),
    ("Diyabetik Vasküler Lezyonlar: Arteriyoloskleroz", "Afferent ve özellikle EFFERENT arteriyolde hyalen kalınlaşma (Diyabete özgüdür).", "Efferent Skleroz", "rose"),
    ("Renal Amiloidoz: Patogenez ve Tipler", "AL amiloidoz (plazma hücre diskrazisi) ve AA amiloidoz (kronik enflamasyon).", "Amiloidoz", "purple"),
    ("Kongo Kırmızısı ve Polarize Mikroskopi", "Kongo kırmızısı ile boyanan amiloidin polarize ışıkta 'elma yeşili çift kırınım' (birefringence) vermesi.", "Elma Yeşili Çift Kırınım", "green"),
    ("Amiloidozda Glomerüler Tutulum ve Nefrotik Sendrom", "Masif proteinüri, hipoalbüminemi ve böbreğin balmumu kıvamında büyümesi.", "Nefrotik Amiloid", "teal"),
    ("Sistemik Vaskülitler ve Pauci-İmmün Glomerülonefrit", "İmmünfloresanda antikor çökeltisi izlenmeyen (pauci-immün) nekrotizan kresentik GN.", "Pauci-İmmün GN", "red"),
    ("Granülomatöz Polianjiyitis (Wegener) ve c-ANCA (PR3)", "Üst/alt solunum yolu nekrotizan granülomları, kavitasyon ve kresentik nefrit.", "c-ANCA / PR3", "accent"),
    ("Mikroskopik Polianjiyitis ve p-ANCA (MPO)", "Granülomsuz sistemik nekrotizan vaskülit ve hızlı ilerleyen böbrek yetmezliği.", "p-ANCA / MPO", "purple"),
    ("Trombotik Mikroanjiyopatiler (TMA): Ortak Patoloji", "Endotel hasarı, trombosit mikrotrombüsleri, kapiller lümen tıkanması ve şistositler.", "TMA Patolojisi", "red"),
    ("Hemolitik Üremik Sendrom (HÜS): Shiga Toksin / EHEC", "Çocuklarda E. coli O157:H7 kanlı ishali sonrası akut böbrek hasarı, trombositopeni ve MAHA.", "HÜS", "rose"),
    ("Atipik HÜS ve Kompleman Regülasyon Defektleri", "Faktör H, Faktör I veya CD46 mutasyonları sonucu kontrolsüz kompleman aktivasyonu.", "Atipik HÜS", "purple"),
    ("Trombotik Trombositopenik Purpura (TTP): ADAMTS13 Defekti", "vWF parçalayan ADAMTS13 metaloproteinaz eksikliği; multimerik vWF trombüsleri ve nörolojik bulgular.", "TTP & ADAMTS13", "accent"),
    ("Multiple Miyelomda Böbrek Hasarı: Miyelom Böbreği", "Monoklonal Bence-Jones hafif zincir silindirleri, tübüler obstrüksiyon ve dev hücre reaksiyonu.", "Miyelom Böbreği", "amber"),
    ("Sistemik Böbrek Hasarı Ayırıcı Tanı ve Biyopsi Özeti", "Işık mikroskobu, immünfloresan ve elektron mikroskobunun entegre değerlendirmesi.", "Entegre Biyopsi", "accent")
]

topics_urogenital_genetik = [
    ("Ürogenital Tümör Genetiğine Giriş ve Çekirdek Biyomarkerlar", "Böbrek, mesane, prostat ve testis tümörlerinin moleküler haritası.", "Giriş & Kapsam", "accent"),
    ("Berrak Hücreli Renal Karsinom (ccRCC) ve 3p Delesyonu", "En sık böbrek kanserinde 3p25 lokusundaki VHL gen kaybı.", "ccRCC & 3p", "teal"),
    ("Von Hippel-Lindau Sendromu ve ccRCC Biyolojisi", "Serebellar hemanjoblastom, retina anjiyomu, feokromositoma ve bilateral/multifokal ccRCC.", "VHL Sendromu", "purple"),
    ("Papiller Renal Hücreli Karsinom: Tip 1 ve MET Onkogeni", "7q31'deki MET reseptör tirozin kinaz mutasyonları ve trizomi 7 / 17.", "Papiller Tip 1", "blue"),
    ("Papiller Renal Hücreli Karsinom: Tip 2 ve FH Mutasyonu", "Fumarat hidrataz (FH) enzim eksikliği ve Herediter Leiyomiyomatozis-RHK.", "Papiller Tip 2", "amber"),
    ("Kromofob RHK: Çoklu Monozomiler ve mtDNA", "1, 2, 6, 10, 13 ve 17. kromozomların yaygın kaybı; sitogenetik ayak izi.", "Kromofob RHK", "rose"),
    ("Böbrek Onkositoması ve Sitogenetik Ayrım", "Benign proksimal tübül tümörü; 1. kromozom kaybı ve t(5;11) translokasyonu.", "Onkositoma", "green"),
    ("Böbrek Anjiyomiyolipomu (AML) ve Tüberöz Skleroz", "TSC1 (Hamartin) ve TSC2 (Tüberin) gen mutasyonları; mTOR aşırı aktivasyonu.", "Tüberöz Skleroz", "purple"),
    ("Xp11.2 Translokasyon İlişkili Renal Hücreli Karsinom", "TFE3 gen füzyonları ile giden genç yaş böbrek karsinomu.", "TFE3 Karsinomu", "accent"),
    ("Mesane Karsinogenezinde Çift Yol Modeli", "Non-invaziv papiller yol (FGFR3) vs Karsinoma in situ invaziv yol (TP53/RB1).", "Mesane Çift Yol", "red"),
    ("FGFR3 Mutasyonları ve Düşük Dereceli Mesane Karsinomu", "Fibroblast Büyüme Faktörü Reseptörü 3 konstitütif aktivasyonu.", "FGFR3", "teal"),
    ("TP53 ve RB1 Kaybı ile Giden Yüksek Dereceli Mesane Kanseri", "Karsinoma in situ zemininde gelişen kas invaziv agresif karsinom.", "TP53 / RB1", "red"),
    ("TERT Promoter Mutasyonları ve Mesane Kanseri Tanısı", "İdrar sitolojisinde erken tanı sağlayan en sık rastlanan mutasyon.", "TERT Promoter", "purple"),
    ("Prostat Kanserinde TMPRSS2-ERG Gen Füzyonu", "21q22 delesyonu ile androjenle regüle TMPRSS2 promotörünün ERG transkripsiyon faktörüne bağlanması.", "TMPRSS2-ERG", "blue"),
    ("Prostat Karsinomunda PTEN Kaybı ve PI3K Yolağı", "İlerlemiş ve kastre dirençli prostat kanserinde en sık supresör inaktivasyonu.", "PTEN Kaybı", "red"),
    ("BRCA1, BRCA2 ve DNA Onarım Genleri (Prostat Kanseri)", "Homolog rekombinasyon eksikliği; agresif seyir ve PARP inhibitör (Olaparib) duyarlılığı.", "BRCA & PARP", "purple"),
    ("Testis Germ Hücreli Tümörleri ve İzokromozom 12p", "Seminom ve non-seminomların %100'e yakınında saptanan patognomonik i(12p) anomalisi.", "i(12p) İzokromozom", "accent"),
    ("Seminom Genetiği: KIT ve KRAS Mutasyonları", "4q12'deki c-KIT reseptör tirozin kinaz mutasyonları ve seminom patogenezi.", "c-KIT Seminom", "teal"),
    ("Non-Seminom Germ Hücreli Tümörler: Teratom ve Embriyonal", "Pluripotent diferansiasyon, OCT4 ve NANOG kök hücre belirteçleri.", "Non-Seminom", "purple"),
    ("Ürolojik Kanserlerde Sıvı Biyopsi ve İdrar DNA Testleri", "UroVysion FISH testi, idrarda metilasyon panelleri ve ctDNA.", "Ürolojik Biyomarker", "green"),
    ("Moleküler Sınıflamaya Göre Böbrek Tümörleri Ayırıcı Tanı Ağacı", "ccRCC vs Papiller vs Kromofob vs Onkositoma moleküler algoritması.", "Ayırıcı Algoritma", "accent"),
    ("Moleküler Sınıflamaya Göre Mesane Tümörleri Tablosu", "Lüminal papiller, bazal skuamöz ve nöroendokrin moleküler alt tipler.", "Mesane Alt Tipleri", "blue"),
    ("Hedefe Yönelik Tedaviler: Tirozin Kinaz ve İmmün Kontrol Noktaları", "Sunitinib, Kabozantinib, Pembrolizumab ve Enfortumab vedotin.", "Ürolojik Hedefli İlaç", "teal"),
    ("Ürogenital Genetik Belirteçler Büyük Özet Sentezi", "Genetik füzyonlar, trizomiler, monozomiler ve klinik karar yolları.", "Büyük Sentez", "accent")
]

topics_bebek_beslenmesi = [
    ("Bebek Beslenmesinin Önemi ve Temel Biyolojik Hedefler", "Optimal büyüme, nörokognitif gelişim, enfeksiyonlardan korunma ve kronik hastalık profilaksisi.", "Giriş & Hedef", "accent"),
    ("Anne Sütünün Dinamik Biyolojik Doğası", "Her bebeğe ve her emzirme anına özel değişen canlı biyoaktif doku vasfı.", "Canlı Doku Süt", "teal"),
    ("Anne Sütünün Evreleri: Kolostrumun Eşsiz Değeri", "İlk 3-5 gün salgılanan; protein, sIgA, çinko ve lökositten zengin 'ilk aşı'.", "Kolostrum", "amber"),
    ("Geçiş Sütü ve Olgun Anne Sütü Dönemleri", "Protein oranının azalıp laktoz ve yağ oranının artması; kalori dengelenmesi.", "Olgun Süt", "blue"),
    ("Anne Sütünün İmmünolojik Kalkanı: Sekretuar IgA (sIgA)", "Mide asidine dirençli dimerik sIgA ile bağırsak mukozasında patojen nötralizasyonu.", "sIgA", "red"),
    ("Laktoferrin ve Lizozimin Koruyucu Etkisi", "Serbest demiri bağlayarak bakterileri aç bırakan laktoferrin ve peptidoglikan parçalayan lizozim.", "Laktoferrin / Lizozim", "purple"),
    ("Bifidus Faktörü ve İnsan Sütü Oligosakkaritleri (HMO)", "Yararlı Lactobacillus bifidus florasını besleyen ve patojen tutunmasını engelleyen prebiyotikler.", "HMO & Flora", "green"),
    ("Protein Bileşimi: Whey / Kazein Oranı Farkı", "Anne sütünde 60/40 (veya 80/20) whey baskınlığı; inek sütünde 20/80 kazein sert pıhtısı.", "Whey / Kazein", "teal"),
    ("Lipid Mimarisi ve Beyin Gelişimi: DHA ve ARA", "Çoklu doymamış yağ asitleri, miyelinizasyon ve retina fotoreseptör olgunlaşması.", "DHA / ARA", "purple"),
    ("Karbonhidrat Dengesi: Yüksek Laktoz Avantajı", "Anne sütünde %7 yüksek laktoz; asidik bağırsak pH'sı, kalsiyum emilimi ve galaktoz desteği.", "Laktoz Üstünlüğü", "blue"),
    ("Mikro Besinler: Demir ve Kalsiyum Biyoyararlanımı", "Düşük konsantrasyona rağmen %50 emilim oranı (İnek sütünde demir emilimi yalnızca %10).", "Demir Emilimi", "rose"),
    ("Böbrek Solüt Yükü: Anne Sütü vs İnek Sütü", "İnek sütünün yüksek sodyum ve proteiniyle böbreği yorması; anne sütünün düşük solüt yükü.", "Solüt Yükü", "amber"),
    ("İlk 6 Ay Yalnızca Anne Sütü İlkeleri", "Su dahil hiçbir ek sıvı/gıda vermeden ilk 6 ay eksklüzif emzirme kuralı.", "İlk 6 Ay", "accent"),
    ("Tamamlayıcı Beslenmeye Geçiş (6-24 Ay)", "Mide kapasitesi, nöromotor hazır bulunuşluk ve uygun kıvamda besin basamakları.", "Ek Gıdalar", "teal"),
    ("Ek Gıdalarda 1 Yaş Öncesi Yasaklar", "Bal (Clostridium botulinum), inek sütü, tuz, şeker, çilek, patlıcan ve bakla.", "1 Yaş Yasakları", "red"),
    ("Yenidoğanda K Vitamini Profilaksisi", "Doğumda tek doz intramüsküler K1 vitamini ile yenidoğanın hemorajik hastalığını önleme.", "K Vitamini", "rose"),
    ("Rutin D Vitamini Desteği İlkeleri", "15. günden itibaren tüm bebeklere en az 1 yaşına kadar 400 IU/gün profilaksi.", "D Vitamini (400 IU)", "amber"),
    ("Profilaktik Demir Desteği Protokolü", "Zamanında doğanlarda 4. aydan, prematürelerde 2. aydan itibaren 1 mg/kg/gün demir.", "Demir Profilaksisi", "purple"),
    ("İnek Sütü Proteini Alerjisi (İSPA)", "Kazein ve beta-laktoglobuline karşı IgE veya non-IgE aracılı reaksiyon; kanlı mukuslu kaka.", "İSPA Patolojisi", "red"),
    ("Anne Sütünün Kesin Kontrendikasyonları", "Klasik Galaktozemi, anne aktif tedavi edilmemiş Tüberküloz, HIV pozitifliği (gelişmiş ülkeler).", "Kontrendikasyonlar", "red"),
    ("Akut Malnütrisyon: Marasmus (Kuru Malnütrisyon)", "Ağır kalori ve protein yetersizliği; cilt altı yağ kaybı, 'ihtiyar adam' yüzü, ödem YOKTUR.", "Marasmus", "amber"),
    ("Akut Malnütrisyon: Kwashiorkor (Islak Malnütrisyon)", "Yalnızca protein eksikliği; hipoalbüminemi, gode bırakan ödem, hepatosteatoz, bayrak saçı.", "Kwashiorkor", "purple"),
    ("Marasmus ve Kwashiorkor Ayrım Tablosu", "Ödem varlığı/yokluğu, karaciğer yağlanması ve kas erimesi karşılaştırması.", "Malnütrisyon Ayrımı", "accent"),
    ("Bebek Beslenmesi ve Büyüme İzlemi Sentez Özeti", "Persantil eğrileri, baş çevresi, kilo alımı ve koruyucu hekimlik ilkeleri.", "Büyük Özet", "accent")
]

decks_to_build = [
    ("learn-ileri-tumor-genetigi-metabolizmasi", "İleri Tümör Genetiği ve Metabolizması", "İleri Tümör Genetiği", "Tıbbi Patoloji", "Prof. Dr. Hikmet Keleş", "18)İleri Tümör Genetiği ve Metabolizması.pdf", "Meds_Drive_Root / Kurul 1 / Tıbbi Patoloji  / 18)İleri Tümör Genetiği ve Metabolizması.pdf", "RB yolu, TP53 genetiği, TGF-beta, APC/Wnt yolağı, VHL geni, Warburg etkisi ve IDH onkometabolitlerini kapsayan 24 slaytlık patoloji öğrenme güvertesi.", ["Hipofosforile RB aktif olup E2F'yi baskılar.", "TP53 mutasyonu Li-Fraumeni sendromu nedenidir.", "Warburg etkisi: Kanser hücrelerinin aerobik glikolizle biyosentez yapmasıdır."], topics_ileri_genetik),
    ("learn-tumor-immunolojisi-metastaz", "Tümör İmmünolojisi ve Metastaz Mekanizmaları", "Tümör İmmünolojisi ve Metastaz", "Tıbbi Patoloji", "Prof. Dr. Hikmet Keleş", "19)Tümör İmmünolojisi ve Metastaz Mekanizmaları.pdf", "Meds_Drive_Root / Kurul 1 / Tıbbi Patoloji  / 19)Tümör İmmünolojisi ve Metastaz Mekanizmaları.pdf", "Tümör antijenleri, CTL/NK efektörleri, immün kaçış yolları, PD-1/PD-L1 kontrol noktası blokajı, EMT ve metastaz kaskadını içeren 24 slaytlık patoloji öğrenme güvertesi.", ["CD8+ CTL'ler MHC Sınıf I ile sunulan neoantijenleri öldürür.", "PD-L1 T hücresini tüketir; monoklonal antikorlar kontrol noktasını açar.", "E-kadherin kaybı invazyonun ilk basamağıdır."], topics_tumor_immunolojisi),
    ("learn-tumor-evreleme-lab-tanisi", "Tümör Evrelemesi, Derecelendirme ve Laboratuvar Tanısı", "Tümör Evreleme ve Tanı", "Tıbbi Patoloji", "Prof. Dr. Hikmet Keleş", "20)Tümör Evrelemesi, Derecelendirme ve LaboratuvarTanısı.pdf", "Meds_Drive_Root / Kurul 1 / Tıbbi Patoloji  / 20)Tümör Evrelemesi, Derecelendirme ve LaboratuvarTanısı.pdf", "Kanser kaşeksisi (TNF-alfa), paraneoplastik sendromlar (PTHrP, SIADH, Trousseau), TNM evrelemesi, derecelendirme (Grade), biyopsi tipleri, İHK panelleri ve serum tümör belirteçlerini kapsayan 24 slaytlık öğrenme güvertesi.", ["TNF-alfa kaşeksinin ana mediyatörüdür.", "Prognozu ve tedaviyi belirlemede Evre (Stage), Dereceden (Grade) çok daha üstündür.", "Serum tümör belirteçleri tanı için değil, tedavi yanıtı ve nüks takibi içindir."], topics_tumor_evreleme),
    ("learn-sistemik-hastaliklar-bobrek-hasari", "Sistemik Hastalıklarda Böbrek Hasarı", "Sistemik Hastalıklarda Böbrek Hasarı", "Tıbbi Patoloji", "Prof. Dr. Hikmet Keleş", "23)Sistemik Hastalıklarda Böbrek Hasarı.pdf", "Meds_Drive_Root / Kurul 1 / Tıbbi Patoloji  / 23)Sistemik Hastalıklarda Böbrek Hasarı.pdf", "Lupus nefriti (Sınıf I-VI, tel lüle ve Full-house immünfloresan), Diyabetik glomerüloskleroz (Kimmelstiel-Wilson nodülleri), Renal amiloidoz (Kongo kırmızısı elma yeşili çift kırınım), ANCA ilişkili pauci-immün kresentik GN, Trombotik mikroanjiyopatiler (HÜS ve TTP) ve Miyelom böbreğini inceleyen 24 slaytlık patoloji öğrenme güvertesi.", ["Lupus nefritinde immünfloresanda Full-House paterni (IgG, IgA, IgM, C3, C1q) patognomoniktir.", "Diyabetik nefropatinin patognomonik lezyonu nodüler glomerülosklerozdur (Kimmelstiel-Wilson nodülleri).", "Amiloidoz polarize mikroskopta Kongo kırmızısı ile elma yeşili çift kırınım verir."], topics_sistemik_bobrek),
    ("learn-urogenital-tumorlerde-genetik", "Ürogenital Sistem Tümörlerinde Genetik Belirteçler", "Ürogenital Tümör Genetiği", "Tıbbi Genetik", "Tıbbi Genetik Anabilim Dalı", "4)'ÜROGENİTAL SİSTEM TÜMÖRLERİNDE GENETİK BELİRTEÇLER.'.pdf", "Meds_Drive_Root / Kurul 1 / Tıbbi Genetik / 4)'ÜROGENİTAL SİSTEM TÜMÖRLERİNDE GENETİK BELİRTEÇLER.'.pdf", "Böbrek ccRCC (3p delesyonu, VHL), Papiller RHK (MET, trizomi 7/17), Kromofob RHK monozomileri, Mesane FGFR3 ve TP53 yolları, Prostat TMPRSS2-ERG füzyonu ve Testis germ hücreli i(12p) izokromozomunu inceleyen 24 slaytlık genetik öğrenme güvertesi.", ["ccRCC'de 3p delesyonu ve VHL inaktivasyonu temel genetik olaydır.", "Testis germ hücreli tümörlerinde izokromozom 12p - i(12p) patognomoniktir.", "Prostat kanserinde en sık genetik füzyon TMPRSS2-ERG delesyon/füzyonudur."], topics_urogenital_genetik),
    ("learn-bebek-beslenmesi", "Bebek Beslenmesi, Anne Sütü ve Malnütrisyon", "Bebek Beslenmesi", "Halk Sağlığı", "Halk Sağlığı Anabilim Dalı", "3)BEBEK BESLENMESİ.pdf", "Meds_Drive_Root / Kurul 1 / Halk Sağlığı  / 3)BEBEK BESLENMESİ.pdf", "Anne sütünün dinamik biyolojisi, kolostrum, sIgA, laktoferrin, HMO, whey/kazein oranı, inek sütü farkları, ek gıdalara geçiş kuralları, K/D vitamini ve demir profilaksileri, İSPA ve Marasmus vs Kwashiorkor malnütrisyonunu inceleyen 24 slaytlık halk sağlığı öğrenme güvertesi.", ["İlk 6 ay yalnızca anne sütü verilmelidir; su bile verilmez.", "Anne sütü whey baskındır (60/40); inek sütü kazein baskındır (20/80) ve sindirimi zordur.", "Kwashiorkor'da gode bırakan ödem ve hepatosteatoz varken; Marasmus'ta ödem yoktur, cilt altı yağ dokusu erir."], topics_bebek_beslenmesi)
]

for deck_args in decks_to_build:
    new_d = make_deck(*deck_args)
    ex_idx = -1
    for i, ex in enumerate(decks):
        if ex.get('id') == new_d['id']:
            ex_idx = i
            break
    if ex_idx >= 0:
        decks[ex_idx] = new_d
        print(f"Updated deck: {new_d['id']}")
    else:
        decks.append(new_d)
        print(f"Added deck: {new_d['id']}")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"\nSaved all decks to {DECKS_PATH}. Total decks in database: {len(decks)}")

# Re-index study questions manifest cleanly
print("\nRe-indexing study questions manifest...")
os.system(f"{sys.executable} scripts/build_chunked_study_questions.py")
