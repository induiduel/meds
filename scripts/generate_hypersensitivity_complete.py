# -*- coding: utf-8 -*-
"""
generate_hypersensitivity_complete.py
Master builder for 'learn-asiri-duyarlilik-ve-otoimmunite'.
Constructs:
1. 24 high-yield slides with structured spot pearls, flashcards, core content, practice questions
2. 32 comprehensive medical encyclopedia records with differential diagnosis
3. 32 matching medical glossary items
4. Appending practice questions to chunked database src/data/study_questions/
5. Updating learning_batch_queue.json
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Define Deck Metadata
DECK_ID = "learn-asiri-duyarlilik-ve-otoimmunite"
DECK_TITLE = "Aşırı Duyarlılık Reaksiyonları ve Otoimmünite Patolojisi"
SHORT_TITLE = "Aşırı Duyarlılık & Otoimmünite"
DISCIPLINE = "Tıbbi Patoloji"
COMMITTEE = "Dönem 3 Kurul 1"
INSTRUCTOR = "Prof. Dr. Hikmet Keleş"
THEME_COLOR = "purple"
MATCHED_NOTE_ID = "kurul1-patoloji-14"
MATCHED_NOTE_TITLE = "14) Aşırı Duyarlılık ve Otoimmünite"

OVERVIEW = (
    "Prof. Dr. Hikmet Keleş ve Robbins Temel Patoloji (11. Baskı) kılavuzluğunda hazırlanmış; "
    "Tip I-IV aşırı duyarlılık mekanizmalarını, santral ve periferik immünolojik toleransı (AIRE, FoxP3, CTLA-4), "
    "sistemik otoimmün hastalıkları (SLE, Romatoid Artrit, Sjögren, Skleroderma, IgG4-RD), "
    "transplantasyon immünolojisi ve rejeksiyon tiplerini (Hiperakut, Akut, Kronik, GVHD), primer/sekonder "
    "immün yetmezlikleri ve Amiloidoz patolojisini %500 derinlikte inceleyen kapsamlı interaktif eğitim modülü."
)

HIGH_YIELD_PEARLS = [
    "Tip I: IgE ve FcεRI aracılı mast hücre degranülasyonu; erken fazda histamin, PGD2 ve lökotrienler C4/D4/E4; geç fazda eozinofiller (MBP, ECP).",
    "Tip II: Sabit doku/hücre antijenlerine bağlanan IgG/IgM; opsonizasyon (AIHA, İTP), kompleman aracılı doku hasarı (Goodpasture, Pemfigus) ve reseptör disfonksiyonu (Myasthenia Gravis, Graves).",
    "Tip III: Dolaşan çözünür immün komplekslerin damar duvarına çökmesi, kompleman fiksasyonu ve damar duvarında fibrinoid nekroz (SLE nefriti, Serum hastalığı, Arthus reaksiyonu).",
    "Tip IV: Antikordan bağımsız T lenfosit yanıtı; Th1 (IFN-γ ile makrofaj aktivasyonu ve granülom), Th17 (IL-17 nötrofilik hasar) ve CD8+ CTL (Perforin/granzim apoptozu; Tip 1 DM, Kontakt dermatit).",
    "Tolerans: Santral toleransta timik AIRE geni periferik antijenleri eksprese ettirir (mutasyonunda APECED/APS-1); periferik toleransta Treg hücreleri FoxP3 ile yönetilir (mutasyonunda IPEX sendromu).",
    "SLE: En hassas antikor ANA (%98-100); nefrit aktivitesi ve alevlenmeyle paralel giden Anti-dsDNA; hastalığa en spesifik Anti-Smith (Sm); kapillerlerde Tel-Kulp (Wire-loop) ve Libman-Sacks endokarditi.",
    "Transplantasyon: Hiperakut (önceden var olan antikorlar + fibrinoid nekroz), Akut sellüler (tubulit/endotelit), Akut humoral (C4d pozitifliği), GVHD (Donör T hücresinin alıcı karaciğer, cilt ve bağırsağına saldırısı).",
    "Amiloidoz: Çapraz beta-kırmalı tabaka; Kongo Kırmızısı boyasında polarize ışık mikroskobunda elma yeşili çift kırılma (apple-green birefringence); AL (hafif zincir), AA (Serum Amiloid A/kronik enflamasyon), ATTR (Transtiretin)."
]

# We will define the full 24 slides
slides = [
    # SLIDE 1
    {
        "slideNumber": 1,
        "title": "Aşırı Duyarlılık (Hipersensitivite) Kavramı ve 4 Temel Tip",
        "subtitle": "İmmün Yanıtın Doku Hasarına Dönüşümü ve Tablo 5.2 Mekanizmaları",
        "badge": "Giriş & Sınıflama",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Aşırı Duyarlılık (Hipersensitivite - HS) Kavramı

İmmün sistem normal koşullarda konağı dış patojenlere (bakteri, virüs, mantar, parazit) karşı korumak üzere kusursuz bir denetim mekanizmasına sahiptir. Ancak bazı durumlarda bu koruyucu yanıtlar denetimden çıkar, uygunsuz hedeflere yönelir veya aşırı şiddetli hale gelerek **immünolojik-aracılı doku hasarına** ve klinik hastalıklara yol açar. Bu patolojik tablolara genel olarak **Aşırı Duyarlılık (Hipersensitivite)** adı verilir.

```
+---------------------------------------------------------------------------------------+
|                             HEDEF ANTİJEN KAYNAKLARI                                  |
+---------------------------------------------------------------------------------------+
| 1. Öz (Self) Antijenler   : İmmün toleransın kırılması -> Otoimmün Hastalıklar       |
| 2. Mikrobiyal Antijenler  : Temizlenemeyen kronik infeksiyonlar -> İmmün Kompleks/Granülom|
| 3. Çevresel Alerjenler    : Zararsız polen, gıda, ilaç -> Alerjik Reaksiyonlar (Atopi) |
+---------------------------------------------------------------------------------------+
```

### 2. Coombs ve Gell Sınıflaması (Dört Temel Tip)

Patolojik mekanizmalara ve efektör moleküllere göre aşırı duyarlılık dört ana sınıfa ayrılır:

| Tip | Temel İmmün Mekanizma | Histopatolojik Lezyonlar | Prototip Hastalıklar |
| :--- | :--- | :--- | :--- |
| **Tip I (Ani / Immediate)** | **IgE** antikor üretimi; mast hücrelerinden **vazoaktif amin** ve mediyatör salınımı; geç fazda lökosit rekrütmanı. | Vasküler dilatasyon, ödem, düz kas spazmı, mukus sekresyonu. | Anafilaksi, Alerjiler, Atopik Bronşiyal Astım. |
| **Tip II (Antikor-Aracılı)** | Dokuya veya hücre yüzeyine **sabit** antijenlere bağlanan **IgG ve IgM**; kompleman fiksasyonu ve Fc reseptör fagositozu. | Hücre fagositozu ve lizisi; enflamasyon; reseptör fonksiyon anomalileri. | Otoimmün Hemolitik Anemi, Goodpasture, Myasthenia Gravis, Graves. |
| **Tip III (İmmün Kompleks)** | Kanda dolaşan **çözünür antijen-antikor komplekslerinin** damar duvarına çökmesi; kompleman aktivasyonu ve nötrofil hasarı. | Nekrotizan vaskülit (**fibrinoid nekroz**), akut enflamasyon. | Sistemik Lupus Eritematozus (SLE), Akut Serum Hastalığı, Arthus Reaksiyonu. |
| **Tip IV (Hücre-Aracılı)** | Antikordan bağımsız; duyarlaşmış **CD4+ T lenfositleri** (sitokin salınımı) ve **CD8+ CTL** (sitotoksisite). | Perivasküler infiltrasyon, ödem, **granülom oluşumu**, apoptoz. | Kontakt Dermatit, Multipl Skleroz, Tip 1 Diyabet, Tüberküloz. |
""",
        "spotPearls": [
            "▸ **Aşırı duyarlılık (Hipersensitivite - HS)**: Normalde koruyucu immün yanıtların denetimsiz, aşırı veya uygunsuz şekilde aktive olarak konak dokularında hasara yol açmasıdır.\n  ▫ İmmün yanıt genellikle hedef antijen ortamdan tamamen uzaklaştırılamadığı için kronikleşme eğilimindedir.",
            "🔴 ÖNEMLİ: Tablo 5.2'deki Coombs-Gell sınıflaması komite ve TUS sınavlarının en temel omurgasıdır:\n  ▫ **Tip I**: IgE ve mast hücre/bazofil aracılı, dakikalar içinde gelişen ani vazoaktif yanıt (Anafilaksi, Atopik Astım, Alerjik Rinit).\n  ▫ **Tip II**: IgG ve IgM'in hücre veya hücre dışı matriks üzerindeki *sabit* doku antijenlerine bağlanması (Otoimmün Hemolitik Anemi, Goodpasture, Myasthenia Gravis).\n  ▫ **Tip III**: Dolaşan *çözünür* antijen-antikor immün komplekslerinin damar duvarlarında birikmesi (SLE Nefriti, Serum Hastalığı, Arthus Reaksiyonu).\n  ▫ **Tip IV**: Antikorlardan tamamen bağımsız, duyarlaşmış T lenfositlerinin (Th1, Th17 ve CD8+ CTL) doğrudan aracılık ettiği hücresel doku hasarı (Tüberkülin PPD testi, Kontakt Dermatit, Tip 1 DM).",
            "🔵 ÇIKMIŞ SORU: *'Hangisi hücre yüzeyi veya hücre dışı matrikse bağlı antijenlere karşı gelişen aşırı duyarlılık tipidir?'* şeklinde defalarca sorulmuştur.\n  ▫ Doğru yanıt: **Tip II Hipersensitivite**'dir. Dolaşımda çözünür antijen-antikor kompleksi çökerse Tip III; çözünür alerjen IgE ile mast hücresini uyarırsa Tip I; hücre yüzeyindeki reseptör veya proteine antikor bağlanırsa Tip II'dir!"
        ],
        "coreContent": [
            {"title": "Doku Hasarı Nedeni", "description": "Hedef antijenin yok edilememesi nedeniyle sürekli uyarılan immün kaskad.", "highYieldBadge": "Patofizyoloji", "details": "Kronik enflamasyon ve kalıcı parankim harabiyeti gelişir."},
            {"title": "Antikor Aracılı Tipler", "description": "Tip I (IgE), Tip II (IgG/IgM doku sabiti), Tip III (IgG/IgM dolaşan çözünür kompleks).", "highYieldBadge": "Humoral", "details": "Her üç tipte de antikorlar başlatıcı rol oynar."},
            {"title": "Hücresel Tip", "description": "Tip IV (Gecikmiş tip aşırı duyarlılık ve T lenfosit sitotoksisitesi).", "highYieldBadge": "Hücresel", "details": "Serumla pasif transfer edilemez, yalnızca duyarlaşmış T hücreleriyle aktarılır."}
        ],
        "flashcards": [
            {"id": "fc-hs-01", "front": "Aşırı duyarlılık reaksiyonlarının dördü arasında antikorlardan tamamen bağımsız olan tip hangisidir?", "back": "Tip IV (T hücre-aracılı) aşırı duyarlılık.", "tag": "İmmünoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-02", "front": "Tip II ile Tip III aşırı duyarlılık arasındaki temel antijenik fark nedir?", "back": "Tip II'de antijen hücre veya dokuda SABİTTİR; Tip III'te ise antijen ÇÖZÜNÜRDÜR ve kompleksler kanda dolaşarak çöker.", "tag": "Ayırıcı Tanı", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-01",
                "question": "Bir patoloji laboratuvarında immünohistokimyasal incelemede, glomerül bazal membranında kesintisiz çizgisel (lineer) IgG birikimi ve nekrotizan hasar saptanıyor. Hastada akciğerde hemoptizi ve böbrekte hematüri mevcuttur. Bu tablonun gelişiminde rol oynayan temel immünopatolojik mekanizma aşağıdakilerden hangisidir?",
                "options": [
                    "A) Dolaşan immün komplekslerin subendotelyal çökmesi (Tip III)",
                    "B) Doku bazal membranındaki Tip IV kolajen alfa-3 zincirine karşı antikor aracılı doku hasarı (Tip II)",
                    "C) CD4+ Th1 hücrelerinin makrofaj aktivasyonu ve granülom oluşturması (Tip IV)",
                    "D) Alerjen maruziyeti ile IgE aracılı mast hücre degranülasyonu (Tip I)",
                    "E) CD8+ sitotoksik T lenfositlerinin perforin-granzim salınımı (Tip IV sitotoksisite)"
                ],
                "correctAnswer": "B",
                "explanation": "Goodpasture sendromu, glomerül ve alveol bazal membranında Tip IV kolajenin alfa-3 zincirine karşı gelişen otoantikorların (anti-GBM) yol açtığı prototip bir Tip II aşırı duyarlılık tablosudur. İmmünofloresanda Tip II'ye özgü lineer (çizgisel) floresans verir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Coombs-Gell sınıflamasındaki 4 tipin efektor hücrelerini ve prototiplerini özetle.",
            "Tip II ve Tip III hipersensitivite ayrımında immünofloresan paternlerinin mantığı nedir?"
        ]
    },

    # SLIDE 2
    {
        "slideNumber": 2,
        "title": "Tip I Hipersensitivite: Duyarlanma (Sensitizasyon) Fazı",
        "subtitle": "Dendritik Hücre, Th2 Polarizasyonu, IL-4/IL-13 ve FcεRI Reseptörü",
        "badge": "Tip I Patogenez",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Duyarlanma (Sensitizasyon) Nedir?

Tip I aşırı duyarlılık klinik bulgularının ortaya çıkabilmesi için, bireyin önceden o antijenle en az bir kez karşılaşmış ve **duyarlanmış (sensitize olmuş)** olması şarttır. İlk karşılaşmada hiçbir klinik semptom oluşmaz; ancak immün sistem spesifik IgE antikorları sentezleyerek mast hücrelerini silahlandırır.

```
Alerjen Girişi (Mukoza/Deri)
       │
       ▼
Dendritik Hücre Tarafından Yakalanma ve Naif CD4+ T Hücresine Sunum
       │
       ▼
Th2 Hücresine Farklılaşma (IL-4 etkisiyle)
  ┌────┴────────────────────────┐
  ▼                             ▼
IL-4 & IL-13                   IL-5
  │                             │
  ▼                             ▼
B Hücresinde IgE İzotip      Kemik İliği Eozinofil
Dönüşümü (Class Switching)   Gelişimi ve Aktivasyonu
  │
  ▼
IgE Antikorlarının Mast Hücresi ve Bazofildeki FcεRI Reseptörüne Bağlanması
  │
  ▼
[ DUYARLANMIŞ MAST HÜCRESİ HAZIR ]
```

### 2. Th2 Sitokinlerinin Kritik Rolleri

- **IL-4**: B lenfositlerinde IgE sınıfına geçişi tetikleyen anahtar sitokindir. Aynı zamanda naif T hücrelerinin Th2 yönünde farklılaşmasını otokrin/parakrin olarak uyarır.
- **IL-13**: B hücrelerinden IgE üretimini pekiştirir ve bronş epitel hücrelerinden **yoğun mukus salgılanmasını** uyarır.
- **IL-5**: Eozinofillerin üretimi, kemik iliğinden çıkışı ve dokuda hayatta kalması için vazgeçilmezdir.

### 3. Yüksek Afiniteli IgE Reseptörü: FcεRI

Mast hücreleri ve bazofillerin membranında yer alan **FcεRI**, immünoglobulin süperailesindendir.
- IgE'nin Fc bölgesine olağanüstü yüksek bir afiniteyle ($K_d \approx 10^{-10} \text{ M}$) bağlanır.
- Bu yüksek afinite sayesinde dolaşımda çok düşük konsantrasyonda bulunan serbest IgE molekülleri bile mast hücrelerine kalıcı olarak yapışır.
""",
        "spotPearls": [
            "▸ **Duyarlanma (Sensitizasyon) Süreci**: Alerjen ilk kez mukozadan girdiğinde dendritik hücrelerce yakalanır ve bölgesel lenf noduna taşınarak naif CD4+ T hücrelerine sunulur.\n  ▫ Genetik yatkınlığı (atopi) olan bireylerde bu sunum **Th2** fenotipine doğru kayar.",
            "🔴 ÖNEMLİ: Th2 hücrelerinin salgıladığı sitokinlerin spesifik görevleri TUS'un klasik soru kaynaklarıdır:\n  ▫ **IL-4**: B lenfositlerinde antikor sınıf dönüşümünü (isotype switching) uyararak **IgE üretimini tetikler** ve Th2 yanıtını pekiştirir.\n  ▫ **IL-13**: B hücrelerinden IgE üretimini artırır ve epitel hücrelerinden **mukus salgısını dramatik şekilde uyarır**.\n  ▫ **IL-5**: Kemik iliğinde **eozinofil gelişimini, aktivasyonunu ve dokuya göçünü** sağlayan yegane kilit sitokindir.",
            "🔵 ÇIKMIŞ SORU: *'Tip I aşırı duyarlılıkta mast hücreleri ve bazofillerin yüzeyinde yer alan ve IgE'nin Fc parçasına aşırı yüksek afiniteyle (Kd ~ 10⁻¹⁰ M) bağlanan reseptör hangisidir?'*\n  ▫ Doğru yanıt: **FcεRI (Yüksek afiniteli IgE reseptörü)**'dir. İkincil maruziyette alerjenin bu bağlı IgE'leri çapraz bağlaması (cross-linking) hücresel degranülasyonu başlatır!"
        ],
        "coreContent": [
            {"title": "Duyarlanma Aşaması", "description": "İlk temas sessizdir; klinik bulgu vermez, antijenik bellek ve IgE üretimi oluşturur.", "highYieldBadge": "Sensitizasyon", "details": "Mast hücreleri membranındaki FcεRI reseptörlerine IgE bağlanmasıyla donanır."},
            {"title": "IL-4 ve IL-13", "description": "B hücre sınıf dönüşümü (IgE) ve mukus hipersekresyonunu yöneten sitokin ikilisi.", "highYieldBadge": "Sitokinler", "details": "Alerjik astım ve atopik rinitte hedef moleküllerdir."},
            {"title": "IL-5 ve Eozinofili", "description": "Eozinofil diferansiyasyonunu sağlayan temel faktör.", "highYieldBadge": "Eozinofil", "details": "Astımda biyolojik ajanlar (Mepolizumab) IL-5'i hedefler."}
        ],
        "flashcards": [
            {"id": "fc-hs-03", "front": "B hücrelerinde IgE izotip dönüşümünü (class switching) doğrudan başlatan Th2 sitokini hangisidir?", "back": "İnterlökin-4 (IL-4) (ayrıca IL-13 destekler).", "tag": "Sitokinler", "masterLevel": "Kritik"},
            {"id": "fc-hs-04", "front": "Mast hücresi yüzeyinde IgE antikorlarını bağlayan yüksek afiniteli reseptörün adı nedir?", "back": "FcεRI reseptörüdür.", "tag": "Reseptörler", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-02",
                "question": "Alerjik astım patogenezinde rol oynayan Th2 hücre kaynaklı sitokinlerden hangisi, kemik iliğinde eozinofil öncüllerinin proliferasyonunu ve dokuya göçünü spesifik olarak uyarır?",
                "options": [
                    "A) IL-4",
                    "B) IL-5",
                    "C) IL-13",
                    "D) IFN-γ",
                    "E) TGF-β"
                ],
                "correctAnswer": "B",
                "explanation": "IL-5, eozinofil büyüme, aktivasyon ve kemotaksis faktörüdür. IL-4 IgE sınıf değişimini sağlar; IL-13 mukus salgısını artırır; IFN-γ ise Th1 sitokini olup Th2 yanıtını baskılar.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Th2 yanıtı ile Th1 yanıtının çapraz inhibisyon mekanizmasını anlat.",
            "FcεRI reseptörünün mast hücresi içi sinyal yolakları nelerdir?"
        ]
    },

    # SLIDE 3
    {
        "slideNumber": 3,
        "title": "Tip I Hipersensitivite: Efektör Faz & Erken Mediyatörler",
        "subtitle": "Mast Hücre Degranülasyonu, Histamin, PGD2 ve Lökotrienler C4/D4/E4",
        "badge": "Vazoaktif Mediyatörler",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Mast Hücresi Aktivasyonu ve Çapraz Bağlanma (Cross-linking)

Duyarlanmış mast hücresinin yüzeyinde IgE antikorları hazırdır. Aynı alerjenle **ikinci veya sonraki karşılaşmada**, multivalan alerjen komşu iki veya daha fazla IgE molekülünü birbirine **çapraz bağlar (cross-linking)**. Bu olay FcεRI reseptörlerinin bir araya toplanmasını ve tirozin fosforilasyonu ile intraselüler kalsiyum ($Ca^{2+}$) patlamasını tetikler.

### 2. İki Grup Mediyatör: Depolanmış vs. Yeni Sentezlenen

| Mediyatör Grubu | Spesifik Mediyatörler | Fizyopatolojik Etkiler | Klinik Yansıma |
| :--- | :--- | :--- | :--- |
| **Önceden Depolanmış (Preformed Granüller)** | **Histamin** | H1 reseptörleri üzerinden vazodilatasyon, endotel kontraksiyonu ile venüler geçirgenlik artışı, bronşiyal düz kas kontraksiyonu. | Kaşıntı, ürtiker (kurdeşen), eritem, rinit, akut hırıltı. |
| | **Nötr Proteazlar (Triptaz, Kimaz)** | Doku matriks yıkımı, kinin aktivasyonu, kompleman aktivasyonu. | Doku hasarı; **serum triptaz yüksekliği** anafilaksi kanıtıdır. |
| | **Heparin / Proteoglikanlar** | Granüllerdeki aminleri paketler; antikoagülan etki. | Kanama diyatezi oluşturmaz, lokal akımı artırır. |
| **Yeni Sentezlenen (Lipid Mediyatörler)** | **Lökotrien C4, D4, E4 (SRS-A)** | Histaminden **1000 kat daha güçlü** bronkokonstriksiyon ve vasküler permeabilite artışı. | Uzamış refrakter bronkospazm, hava yolu ödemi. |
| | **Prostaglandin D2 (PGD2)** | Yoğun bronkospazm, vazodilatasyon ve nötrofil kemotaksisi. | Astımda bronkokonstriksiyon ve mukus tıkacı. |
| | **Trombosit Aktive Edici Faktör (PAF)** | Trombosit agregasyonu, vazodilatasyon, mikrovasküler permeabilite artışı. | Şok tablosunda kan basıncı düşüşü. |
""",
        "spotPearls": [
            "▸ **Erken Faz Yanıtı (Dakikalar İçinde)**: Önceden duyarlanmış mast hücresi yüzeyindeki komşu IgE molekülleri antijen ile çapraz bağlandığında, saniyeler içinde granüller ekzositozla salınır.",
            "🔴 ÖNEMLİ: Önceden depolanmış (Preformed) vs. Yeni Sentezlenen (De novo) Mediyatör Ayrımı:\n  ▫ **Histamin**: H1 reseptörleri aracılığıyla yoğun arteriyoler vazodilatasyon, venüler endotelyal aralık açılması (ödem/ürtiker) ve bronş düz kas kontraksiyonu yapar.\n  ▫ **Lökotrien C4, D4 ve E4**: Arakidonik asit 5-lipoksijenaz yolağından üretilir; histaminden **1000 kat daha güçlü** bronkokonstriktor ve vasküler geçirgenlik artırıcıdır.\n  ▫ **Prostaglandin D2 (PGD2)**: Mast hücrelerinden sentezlenen ana siklooksijenaz ürünüdür; şiddetli bronkospazm ve vazodilatasyona yol açar.\n  ▫ **Nötr Proteazlar (Triptaz ve Kimaz)**: Doku hasarı oluşturur; kanda **triptaz yüksekliği** anafilaksi tanısını doğrulamada biyobelirteçtir.",
            "🔵 ÇIKMIŞ SORU: *'Anafilaktik şok şüphesiyle acil servise getirilen bir hastada mast hücre aktivasyonunu laboratuvar düzeyinde kesinleştirmek için serumda ölçülmesi gereken enzim hangisidir?'*\n  ▫ Doğru yanıt: **Serum Triptaz düzeyi**dir!"
        ],
        "coreContent": [
            {"title": "Çapraz Bağlanma", "description": "Antijenin en az iki IgE-FcεRI kompleksini köprülemesi degranülasyon için şarttır.", "highYieldBadge": "Tetikleyici", "details": "Monovalan antijenler degranülasyon yapamaz."},
            {"title": "Lökotrienler C4/D4/E4", "description": "Astım patofizyolojisinde histaminden çok daha inatçı ve güçlü bronkokonstriktörler.", "highYieldBadge": "Lipid Mediyatör", "details": "Montelukast gibi LT reseptör antagonistleri bu mediyatörleri hedefler."},
            {"title": "Serum Triptazı", "description": "Mast hücrelerine özgü proteaz.", "highYieldBadge": "Biyobelirteç", "details": "Anafilaksi atağından sonraki ilk birkaç saat içinde pik yapar."}
        ],
        "flashcards": [
            {"id": "fc-hs-05", "front": "Mast hücresi kaynaklı lipid mediyatörlerden hangisi bronş düz kasını histaminden yaklaşık 1000 kat daha güçlü kasar?", "back": "Sisteinil Lökotrienler (LTC4, LTD4, LTE4).", "tag": "Farmakoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-06", "front": "Anafilaksi atağını retrospektif veya akut olarak kanıtlayan serum biyobelirteci nedir?", "back": "Serum Triptaz düzeyi.", "tag": "Laboratuvar", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-03",
                "question": "Aşağıdaki mast hücresi mediyatörlerinden hangisi granüllerde önceden depolanmış (preformed) olmayıp, membran fosfolipidlerinden arakidonik asit metabolizması sonucu yeni sentezlenen (de novo) bir mediyatördür?",
                "options": [
                    "A) Histamin",
                    "B) Triptaz",
                    "C) Lökotrien C4",
                    "D) Kimaz",
                    "E) Heparin"
                ],
                "correctAnswer": "C",
                "explanation": "Lökotrien C4, fosfolipaz A2 ve 5-lipoksijenaz yolağı ile hücre zarından anlık sentezlenen bir lipid mediyatördür. Histamin, triptaz, kimaz ve heparin ise granüllerde önceden depolanmış durumdadır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Arakidonik asit yolağında siklooksijenaz ve lipoksijenaz ürünlerinin mast hücresindeki dağılımı nasıldır?",
            "Histamin H1 ve H2 reseptörlerinin vasküler ve gastrik etkilerini karşılaştır."
        ]
    },

    # SLIDE 4
    {
        "slideNumber": 4,
        "title": "Tip I Hipersensitivite: Geç Faz Reaksiyonu ve Eozinofiller",
        "subtitle": "2-24 Saat Sonrası Enflamasyon, Eotaksin, MBP, ECP ve Doku Hasarı",
        "badge": "Geç Faz & Eozinofil",
        "badgeColor": "sky",
        "synthesisNarrative": """### 1. Geç Faz Reaksiyonu Nedir?

Alerjen maruziyetinden sonraki ilk 15-30 dakikada gelişen erken vazoaktif faz düzelse dahi, hastaların çoğunda **2 ila 24 saat sonra** ilave bir antijen maruziyeti olmaksızın ikinci bir dalga başlar: **Geç Faz Reaksiyonu (Late-Phase Reaction)**.

Erken faz vasküler dilatasyon ve ödemle seyrederken; geç faz **yoğun lökosit infiltrasyonu, mukozal epitel hasarı ve doku destrüksiyonu** ile karakterizedir.

### 2. Hücre Göçünün Yönetimi ve Eozinofil Cephanesi

1. **Sitokinler ve Kemokinler**:
   - Mast hücrelerinden ve Th2'lerden salınan **TNF-α** ve **IL-4**, endotel hücrelerinde adhezyon moleküllerini (E-selektin, VCAM-1) artırır.
   - **Eotaksin (CCL11)** ve **IL-5**, eozinofilleri doğrudan enflamasyon alanına çeker.

2. **Eozinofillerin Doku Harabiyet Toksinleri**:
   - **Majör Temel Protein (MBP)**: Helmintleri parçalamak için tasarlanmış çok katyonik bir proteindir; konak epitelini nekroza uğratır ve deskuame eder.
   - **Eozinofil Katyonik Protein (ECP)** ve **Eozinofil Peroksidaz (EPO)**: Epitel hücre zarlarında delikler açar ve sitotoksik serbest radikaller üretir.
   - **Histopatolojik Bulgular**: Mukus tıkaçları içinde **Charcot-Leyden Kristalleri** (eozinofil lizofosfolipaz proteini agregatları) ve **Curschmann Spiralleri** (dökülmüş bronş epitel tıkaçları).
""",
        "spotPearls": [
            "▸ **Geç Faz Reaksiyonu Dinamiği**: Antijen maruziyetinden 2 ila 24 saat sonra ortaya çıkar; ek bir antijen teması gerektirmez.\n  ▫ Erken fazdaki geçici vasküler olayların aksine, geç fazda yoğun **hücresel doku infiltrasyonu**, mukozal dökülme ve belirgin epitelyal hasar izlenir.",
            "🔴 ÖNEMLİ: Eozinofillerin Toksik Cephanesi:\n  ▫ **Major Basic Protein (MBP)** ve **Eozinofil Katyonik Protein (ECP)**: Parazitleri öldürmek üzere tasarlanmış bu son derece bazik proteinler, konak hava yolu epitelinde geniş dökülmelere, siliyer disfonksiyona ve geri dönüşsüz hasara neden olur.\n  ▫ **Eozinofil Peroksidaz (EPO)** ve **Nörotoksin (EDN)**: Reaktif oksijen türleri üreterek doku hasarını katlar.\n  ▫ Geç faz enflamasyonunda balgam ve dokuda Charcot-Leyden kristalleri saptanır.",
            "🔵 ÇIKMIŞ SORU: *'Alerjik astım patolojisinde hava yolu epitelini nekroza uğratan ve deskuamasyonuna yol açan en önemli eozinofil kaynaklı granül proteini hangisidir?'*\n  ▫ Doğru yanıt: **Majör Temel Protein (Major Basic Protein - MBP)**'dir."
        ],
        "coreContent": [
            {"title": "Zaman Pencereleri", "description": "Erken faz: 5-30 dk (dakikalar); Geç faz: 2-24 saat (saatler).", "highYieldBadge": "Klinik Zaman", "details": "Geç faz kortikosteroid tedavisine iyi yanıt verir."},
            {"title": "MBP ve ECP", "description": "Hava yolu epitel nekrozu ve aşırı duyarlılığının baş sorumlusu katyonik eozinofil proteinleri.", "highYieldBadge": "Toksin", "details": "Astımda geri dönüşümsüz hava yolu remodelleşmesine zemin hazırlar."},
            {"title": "Charcot-Leyden Kristalleri", "description": "Eozinofil membran lizofosfolipazından oluşan prizmatik elmas benzeri kristaller.", "highYieldBadge": "Histopatoloji", "details": "Alerjik ve paraziter balgam yaymalarında patognomoniktir."}
        ],
        "flashcards": [
            {"id": "fc-hs-07", "front": "Alerjik astımlı hastanın balgamında görülen ve eozinofil granül proteinlerinden oluşan hekzagonal kristallerin adı nedir?", "back": "Charcot-Leyden kristalleri.", "tag": "Histopatoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-08", "front": "Geç faz alerjik reaksiyonun erken fazdan en temel histopatolojik farkı nedir?", "back": "Erken fazdaki ödem ve vasküler dilatasyonun yerini yoğun eozinofil/lökosit infiltrasyonu ve epitel hasarının almasıdır.", "tag": "Mekanizma", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-04",
                "question": "Kronik atopik astım hastasının bronş lavajında saptanan ve hava yolu silialı epitel hücrelerinde nekroz ve dökülmeye neden olan en güçlü eozinofilik katyonik protein aşağıdakilerden hangisidir?",
                "options": [
                    "A) Majör Temel Protein (MBP)",
                    "B) Histaminaz",
                    "C) Arilsülfataz",
                    "D) Triptaz",
                    "E) İmmünoglobulin A"
                ],
                "correctAnswer": "A",
                "explanation": "Majör Temel Protein (MBP), eozinofil granül çekirdeğinde yer alan ve doku epitelinde doğrudan nekroz ve epitelyal soyulmaya (deskuamasyon) yol açan en toksik proteindir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Charcot-Leyden kristalleri ile Curschmann spirallerinin oluşum farkı nedir?",
            "Astımda hava yolu remodelleşmesi (subepitelyal fibrozis) neden ve nasıl gelişir?"
        ]
    },

    # SLIDE 5
    {
        "slideNumber": 5,
        "title": "Tip I Klinik Spektrum: Anafilaksi, Atopi ve Tedavi",
        "subtitle": "Sistemik Anafilaksi, Atopik Bozukluklar, Hijyen Hipotezi ve Epinefrin",
        "badge": "Klinik & Acil Tedavi",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Sistemik Anafilaksi

Alerjenin doğrudan kan dolaşımına girmesi (ilaç enjeksiyonu - örn. Penisilin, arı sokması veya gastrointestinal mukozadan hızla emilen yer fıstığı/kabuklu deniz ürünleri) sonucu **tüm vücut mast hücrelerinin yaygın ve eşzamanlı degranülasyonu** ile karakterize hayatı tehdit eden acil klinik tablodur.

```
+-----------------------------------------------------------------------------------+
|                           ANAFİLAKSİ KLİNİK BASAMAKLARI                           |
+-----------------------------------------------------------------------------------+
| 1. Deri Bulguları   : Yaygın kaşıntı, eritem, ürtiker (kurdeşen) ve anjiyoödem     |
| 2. Solunum Yolu     : Laringeal ödem (stridor, asfiksi riski!) ve şiddetli        |
|                       bronkospazm (ekspiratuvar hırıltı, nefes darlığı)            |
| 3. Kardiyovasküler  : Yaygın vazodilatasyon ve vasküler kaçak -> Hipotansiyon,    |
|                       kardiyovasküler kollaps ve anafilaktik şok                   |
| 4. Gastrointestinal : Düz kas spazmına bağlı bulantı, kusma, kramp, kanlı ishal   |
+-----------------------------------------------------------------------------------+
```

### 2. Atopi ve Hijyen Hipotezi

- **Atopi**: Çevresel alerjenlere karşı aşırı IgE üretme ve Tip I aşırı duyarlılık geliştirme konusundaki ailesel ve genetik yatkınlıktır. Bu bireylerde serum IgE düzeyleri yüksek ve IL-4 salgılayan Th2 hücre oranı fazladır.
- **Hijyen Hipotezi**: Erken çocukluk çağında mikrobiyal maruziyetin (enfeksiyonlar, çiftlik ortamı, geniş aile) immün sistemi **Th1** yönünde eğittiği; aşırı steril ortamlarda büyüyen çocuklarda ise dengenin kontrolsüz **Th2 (alerjik)** yanıta kaydığını savunan hipotezdir.

### 3. Tedavi İlkeleri ve Kritik Ayrım

1. **Birincil ve Hayat Kurtarıcı Tedavi**: **İntramusküler Epinefrin (Adrenalin)**
   - $\alpha_1$ etki: Vazokonstrüksiyon yaparak kan basıncını yükseltir ve laringeal ödemi geriletir.
   - $\beta_2$ etki: Bronş düz kaslarını gevşetir ve intraselüler cAMP'yi artırarak mast hücre degranülasyonunu doğrudan durdurur.
2. **İkincil / Destek Tedaviler**: Antihistaminikler (H1 blokörleri), sistemik kortikosteroidler (geç fazı engeller).
3. **Hedefe Yönelik Biyolojikler**: **Omalizumab** (serbest IgE'ye bağlanarak FcεRI'ye yapışmasını engelleyen humanize monoklonal antikor).
""",
        "spotPearls": [
            "▸ **Sistemik Anafilaksi Kliniği**: Dakikalar içinde kaşıntı, yaygın ürtiker, anjiyoödem; hemen ardından stridor (laringeal ödem), şiddetli nefes darlığı (bronkospazm) ve sistemik vazodilatasyona bağlı hipotansiyon/şok tablosu gelişir.",
            "🔴 ÖNEMLİ: Anafilaksinin Hayat Kurtarıcı Birincil Tedavisi:\n  ▫ **İntramüsküler Epinefrin (Adrenalin)**: Tek ve en acil tedavidir. Beta-2 adrenerjik etkiyle bronş düz kaslarını gevşetir, mast hücrelerinden mediyatör salınımını inhibe eder; Alfa-1 adrenerjik etkiyle vazokonstrüksiyon yaparak kan basıncını yükseltir ve laringeal ödemi geriletir.\n  ▫ Antihistaminikler ve kortikosteroidler anafilaksinin birinci basamak hayat kurtarıcısı DEĞİLDİR; sadece ek ve geç fazı önleyici tedavilerdir!",
            "🔵 ÇIKMIŞ SORU: *'Alerjik astım tedavisinde dolaşımdaki serbest IgE antikorlarına bağlanarak mast hücresine yapışmasını engelleyen monoklonal antikor hangisidir?'*\n  ▫ Doğru yanıt: **Omalizumab**'dır."
        ],
        "coreContent": [
            {"title": "Epinefrin (Adrenalin)", "description": "Anafilakside tartışmasız ilk basamak hayat kurtarıcı ilaçtır.", "highYieldBadge": "Acil İlaç", "details": "Uyluk anterolateraline (vastus lateralis) intramüsküler uygulanır."},
            {"title": "Omalizumab", "description": "Anti-IgE monoklonal antikor.", "highYieldBadge": "Biyolojik Tedavi", "details": "Serbest IgE'yi nötralize ederek mast hücresi FcεRI reseptörlerine bağlanmasını engeller."},
            {"title": "Hijyen Hipotezi", "description": "Erken dönem Th1-Th2 dengesinin mikrobiyal maruziyetle regülasyonu.", "highYieldBadge": "İmmünogenetik", "details": "Gelişmiş toplumlardaki alerji patlamasını açıklar."}
        ],
        "flashcards": [
            {"id": "fc-hs-09", "front": "Sistemik anafilaktik şokta mortaliteyi önleyen en acil ve birincil ilaç hangisidir?", "back": "İntramüsküler Epinefrin (Adrenalin).", "tag": "Acil Tıp", "masterLevel": "Kritik"},
            {"id": "fc-hs-10", "front": "Omalizumab'ın etki mekanizması nedir?", "back": "Dolaşımdaki serbest IgE'ye bağlanarak mast hücrelerindeki FcεRI reseptörlerine yapışmasını bloke eder.", "tag": "Farmakoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-05",
                "question": "Penisilin enjeksiyonu sonrası 5 dakika içinde nefes darlığı, stridor, yaygın ürtiker ve tansiyon düşüklüğü (70/40 mmHg) gelişen 24 yaşındaki hastada derhal uygulanması gereken en uygun ilk basamak medikal tedavi hangisidir?",
                "options": [
                    "A) İntravenöz Dekzametazon",
                    "B) İntramüsküler Epinefrin (Adrenalin)",
                    "C) Oral Difenhidramin",
                    "D) İnhaler Salbutamol tek başına",
                    "E) İntravenöz Kalsiyum Glukonat"
                ],
                "correctAnswer": "B",
                "explanation": "Sistemik anafilaksinin tek hayat kurtarıcı birinci basamak ilacı intramüsküler epinefrindir (adrenalin). Alfa-1 vazokonstrüksiyon ve beta-2 bronkodilatasyon/mast hücre stabilizasyonu sağlar. Kortikosteroid ve antihistaminikler yalnızca ikincil adjuvan tedavilerdir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Epinefrinin mast hücresi içi cAMP düzeyine etkisi ve degranülasyon inhibisyonu nasıl çalışır?",
            "Laringeal ödem ile bronkospazmın anafilaksideki patolojik ayrımı nedir?"
        ]
    },

    # SLIDE 6
    {
        "slideNumber": 6,
        "title": "Tip II Hipersensitivite: Opsonizasyon ve Fagositoz Mekanizması",
        "subtitle": "IgG/IgM Antikorları, FcγR Reseptörleri, Kompleman C3b ve Ekstravasküler Hemoliz",
        "badge": "Tip II Opsonizasyon",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. Tip II Hipersensitiviteye Giriş

Tip II aşırı duyarlılık reaksiyonlarında antikorlar (**IgG veya IgM**), hedef hücrelerin yüzeyinde veya hücre dışı matrikste yer alan **sabit (fixed) antijenlere** bağlanır. Bu bağlanma doku hasarını üç ana yoldan biriyle tetikler:
1. **Opsonizasyon ve Fagositoz** (Bu slayt)
2. **Kompleman ve Fc Reseptör Aracılı Enflamasyon** (Slayt 7)
3. **Hücresel Disfonksiyon / Reseptör Modülasyonu** (Slayt 8)

### 2. Opsonizasyon ve Fagositoz Dinamiği

Hücre yüzeyine bağlanan IgG antikorları veya kompleman fragmanları (C3b, iC3b), hedef hücreyi fagositer hücreler için adeta 'lezzetli bir lokma' haline getirir (opsonizasyon):
- **Fcγ Reseptörleri (FcγR)**: Makrofaj ve nötrofillerin yüzeyindeki FcγRI, opsonize hücrenin IgG'sini tanır.
- **C3b Reseptörleri (CR1)**: Kompleman aktivasyonu ile hedef hücre membranına kovalent bağlanan C3b moleküllerini tanır.

```
Hedef Hücre (Eritrosit/Trombosit)
       │
       ▼ + Otoantikor (IgG / IgM)
Hücre Yüzeyine Antikor Bağlanması ve C3b Çökmesi (Opsonizasyon)
       │
       ▼ Dolaşım Dalak/Karaciğere Ulaşır
Sinüzoidlerdeki Doku Makrofajlarının FcγR ve CR1 Reseptörleriyle Yakalanma
  ┌────┴────────────────────────────────┐
  ▼                                     ▼
Tam Fagositoz (Yutulma ve Lizis)     Kısmi Membran Koparılması (Sferosit Oluşumu)
  │                                     │
  ▼                                     ▼
[ EKSTRAVASKÜLER HEMOLİZ ]           [ EKSTRAVASKÜLER HEMOLİZ ]
```

### 3. Prototip Klinik Tablolar

1. **Otoimmün Hemolitik Anemi (AIHA)**:
   - Sıcak tip AIHA: Eritrosit Rh grubu proteinlerine karşı IgG antikorları; dalakta makrofajlarca parçalanır.
   - Periferik yaymada eritrositlerin santral solukluğunu kaybedip küreselleştiği **Mikrosferositler** görülür.
2. **İmmün Trombositopenik Purpura (İTP)**:
   - Trombosit membranındaki **GPIIb/IIIa** veya **GPIb-IX** komplekslerine karşı IgG otoantikorları.
   - Dalak makrofajları trombositleri yok eder; kemik iliğinde megakaryosit hiperplazisi ve deride peteşi/purpura.
3. **Yenidoğanın Hemolitik Hastalığı (Eritroblastozis Fetalis)**:
   - Rh(-) annenin Rh(+) fetusa karşı ürettiği anti-D IgG antikorları plasentayı geçer ve fetal eritrositleri parçalar.
""",
        "spotPearls": [
            "▸ **Opsonizasyon ve Yıkım Mekanizması**: Kendi eritrosit veya trombosit yüzeyindeki antijenlere IgG sınıfı antikorlar bağlanır.\n  ▫ Dolaşımda bu hücreler dalak kırmızı pulpasından geçerken sinüzoidlerdeki makrofajların **Fcγ reseptörleri** ve **C3b reseptörleri (CR1)** tarafından tanınarak fagosite edilir (ekstravasküler hemoliz).",
            "🔴 ÖNEMLİ: Prototip Klinik Tablolar ve Antijen Hedefleri:\n  ▫ **Otoimmün Hemolitik Anemi**: Eritrosit membran proteinlerine (özellikle Rh kan grubu antijenlerine) karşı antikor; sonuç eritrosit fagositozu, anemi ve sferositoz.\n  ▫ **İmmün Trombositopenik Purpura (İTP)**: Trombosit membranındaki **GPIIb/IIIa** glikoproteinlerine karşı opsonizan antikorlar; dalakta trombosit fagositozu ve peteşi/purpura ile seyreden kanamalar.\n  ▫ **Eritroblastozis Fetalis**: Rh-negatif annenin Rh-pozitif fetusa karşı oluşturduğu IgG sınıfı anti-Rh (anti-D) antikorlarının plasentayı geçerek fetal eritrositleri parçalaması.",
            "🔵 ÇIKMIŞ SORU: *'İTP'de otoantikorların bağlandığı ve dalakta fagositoza zemin hazırlayan trombosit yüzey antijeni hangisidir?'*\n  ▫ Doğru yanıt: **Glikoprotein IIb/IIIa (GPIIb/IIIa)** kompleksi ve GPIb-IX'dur."
        ],
        "coreContent": [
            {"title": "Ekstravasküler Hemoliz", "description": "Parçalanma damar içinde değil, dalak ve karaciğer kordonlarındaki makrofajlarda gerçekleşir.", "highYieldBadge": "Dalak Yıkımı", "details": "Splenektomi refrakter AIHA ve İTP olgularında hayat kurtarıcı olabilir."},
            {"title": "Sferosit Oluşumu", "description": "Makrofajın eritrositten parça koparması sonucu azalan yüzey/hacim oranı.", "highYieldBadge": "Morfoloji", "details": "Coombs testi pozitif hemolitik anemi göstergesidir."},
            {"title": "Coombs (DAT) Testi", "description": "Eritrosit yüzeyindeki IgG veya C3b'yi saptayan direkt antiglobulin testi.", "highYieldBadge": "Tanısal Test", "details": "Tip II hemolitik anemilerin temel tanı yöntemidir."}
        ],
        "flashcards": [
            {"id": "fc-hs-11", "front": "İmmün Trombositopenik Purpura (İTP) patolojisinde otoantikorların en sık hedef aldığı membran proteini nedir?", "back": "Glikoprotein IIb/IIIa (GPIIb/IIIa) kompleksi.", "tag": "Hematoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-12", "front": "Otoimmün hemolitik anemide eritrosit yıkımının en sık gerçekleştiği anatomik bölge neresidir?", "back": "Dalak sinüzoidleri (ekstravasküler fagositoz).", "tag": "Patoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-06",
                "question": "Sarılık, splenomegali ve anemi saptanan 30 yaşındaki kadın hastanın periferik yaymasında mikrosferositler izleniyor ve Direkt Coombs testi IgG pozitif bulunuyor. Bu hastada eritrositlerin yıkım mekanizması aşağıdakilerden hangisiyle en iyi açıklanır?",
                "options": [
                    "A) Damar içinde kompleman Membran Atak Kompleksi (MAC, C5b-9) ile doğrudan lizis",
                    "B) Dalak makrofajlarındaki Fcγ reseptörleri aracılığıyla opsonize eritrosit fagositozu",
                    "C) Dolaşan çözünür immün komplekslerin dalak sinüzoidlerinde endoteli tıkaması",
                    "D) CD8+ sitotoksik T lenfositlerinin perforin salgılayarak eritrositi apoptoza sokması",
                    "E) Mast hücre degranülasyonuna bağlı eritrosit lizisi"
                ],
                "correctAnswer": "B",
                "explanation": "Sıcak tip otoimmün hemolitik anemi (AIHA), eritrosit yüzeyindeki proteinlere IgG bağlanması ve bu opsonize eritrositlerin dalak makrofajlarının Fcγ reseptörlerince tanınarak fagosite edilmesi (ekstravasküler hemoliz) ile seyreder.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "İntravasküler hemoliz ile ekstravasküler hemoliz arasındaki immünolojik mekanizma farkı nedir?",
            "İTP tedavisinde splenektominin mantığı neden hem antikor üretimini hem yıkım yerini ortadan kaldırmaktır?"
        ]
    },

    # SLIDE 7
    {
        "slideNumber": 7,
        "title": "Tip II Hipersensitivite: Kompleman ve Fc Reseptör Aracılı Enflamasyon",
        "subtitle": "Sabit Doku Antijenleri, Nötrofil/Monosit Aktivasyonu ve Goodpasture Sendromu",
        "badge": "Tip II Enflamasyon",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Dokuya Bağlı Antikorların Enflamatuar Yıkımı

Tip II aşırı duyarlılığın ikinci mekanizmasında, antikorlar serbest dolaşan hücrelere değil; **hücre dışı matriks proteinlerine veya bazal membranlara** bağlanır.
1. Dokuya bağlanan IgG/IgM klasik yoldan komplemanı aktive eder.
2. Açığa çıkan **C3a ve C5a (anaflotoksinler)** ortama nötrofil ve monositleri çeker.
3. Lökositler dokudaki antikorların Fc bölgesine kendi FcγR reseptörleriyle yapışır.

### 2. 'Frustrated Phagocytosis' (Yetersiz Fagositoz) Kavramı

Nötrofil bazal membran gibi devasa bir doku yapısını yutamaz (fagosite edemez). Bunun üzerine hücre içi granüllerini ve toksik enzimlerini (elastaz, kollajenaz, serbest oksijen radikalleri) **doğrudan hücre dışına, konak dokusunun üzerine boşaltır**. Bu olay çevre dokuda şiddetli nekroz ve enflamasyon yaratır.

### 3. İki Klasik Hastalık Örneği

| Hastalık | Hedef Antijen | Patolojik Mekanizma | İmmünofloresan Görünüm |
| :--- | :--- | :--- | :--- |
| **Goodpasture Sendromu** | Glomerül ve alveol bazal membranındaki **Tip IV kolajenin alfa-3 zinciri (anti-GBM)** | Kompleman ve Fc aracılı nötrofilik hasar; nekrotizan glomerülonefrit ve akciğer kanaması. | Bazal membran boyunca kesintisiz **Çizgisel (Lineer) IgG ve C3** birikimi. |
| **Pemfigus Vulgaris** | Epidermal desmozom proteini olan **Desmoglein-3 ve Desmoglein-1** | Antikorlar hücrelerarası adezyonu bozar; keratinositler birbirinden ayrılır (**akantoliz**). | Epidermiste keratinositler etrafında **'Balık Ağı' (File) tarzında IgG** birikimi. |
""",
        "spotPearls": [
            "▸ **Frustrated (Yetersiz) Fagositoz ve Doku Hasarı**: Antijen bazal membran gibi sabit bir yapıya bağlı olduğunda, nötrofiller bu yapıyı içine alamaz; dışarıya proteolitik enzimlerini (elastaz, katepsin) ve serbest radikallerini kusarak doku nekrozu oluşturur.",
            "🔴 ÖNEMLİ: Goodpasture Sendromu İmmünopatolojisi:\n  ▫ Hedef antijen: Glomerül ve alveol bazal membranındaki **Tip IV kolajenin alfa-3 zincirinin non-kollajenöz (NC1) domeni**dir.\n  ▫ İmmünofloresan mikroskopide tanı koydurucu görünüm: Bazal membran boyunca kesintisiz, düzgün **ÇİZGİSEL (LİNEER) IgG ve C3 birikimi**dir! (Tip III glomerülonefritlerdeki granüler birikimden kesin ayrım).",
            "🔵 ÇIKMIŞ SORU: *'Deri bül biyopsisinde epidermiste intraepitelyal ayrışma (akantoliz) saptanan ve desmoglein-3'e karşı antikor saptanan otoimmün büllöz hastalık hangisidir?'*\n  ▫ Doğru yanıt: **Pemfigus Vulgaris**'tir (Tip II HS mekanizması; bül içi 'mezar taşı' görünümü)."
        ],
        "coreContent": [
            {"title": "Çizgisel (Lineer) Floresans", "description": "Goodpasture sendromunda anti-GBM antikorlarının düzgün bazal membran boyunca homojen dağılımı.", "highYieldBadge": "İmmünofloresan", "details": "Tip III komplekslerin granüler paterninden ayıran en kritik bulgudur."},
            {"title": "Akantoliz", "description": "Pemfigus vulgariste keratinositler arası köprülerin erimesiyle hücrelerin serbestleşmesi.", "highYieldBadge": "Histopatoloji", "details": "İntraepidermal suprabazal bül ve 'mezar taşı' görünümü oluşturur."},
            {"title": "C5a ve Lökosit Göçü", "description": "Kompleman aktivasyonunun en güçlü kemotaktik anaflotoksini.", "highYieldBadge": "Enflamasyon", "details": "Dokuya bağlanan antikorların nötrofil çağırmasında anahtar basamaktır."}
        ],
        "flashcards": [
            {"id": "fc-hs-13", "front": "Goodpasture sendromunda otoantikorların bağlandığı spesifik moleküler hedef nedir?", "back": "Tip IV kolajenin alfa-3 zincirinin NC1 domeni.", "tag": "Nefroloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-14", "front": "Pemfigus vulgaris ve büllöz pemfigoid arasındaki Tip II antijenik hedef farkı nedir?", "back": "Pemfigus vulgaris desmozomlardaki Desmoglein-3'ü hedefler (intraepidermal bül); Büllöz pemfigoid hemidesmozomlardaki BPAG1/BPAG2'yi hedefler (subepidermal bül).", "tag": "Dermatoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-07",
                "question": "Hemoptizi ve oligüri ile başvuran 28 yaşındaki erkek hastanın renal biyopsisinde hilal (kresent) oluşumu saptanıyor. İmmünofloresan incelemede glomerül kapiller duvarlarında kesintisiz, düzgün çizgisel (lineer) IgG birikimi saptanıyor. Bu hastada patolojiden sorumlu otoantikorun hedef molekülü hangisidir?",
                "options": [
                    "A) Tip I kolajen fibrilleri",
                    "B) Tip IV kolajenin alfa-3 zinciri",
                    "C) Mezangiyal lökosit elastazı",
                    "D) Glomerül podosit nefrin proteini",
                    "E) Nötrofil sitoplazmik miyeloperoksidaz"
                ],
                "correctAnswer": "B",
                "explanation": "Goodpasture sendromunda otoantikorlar glomerül bazal membranındaki Tip IV kolajenin alfa-3 zincirinin non-kollajenöz (NC1) bölgesine bağlanır ve kesintisiz çizgisel (lineer) immünofloresan paterni verir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Goodpasture sendromunda neden hem akciğer hem böbrek aynı anda tutulur?",
            "Pemfigus vulgariste akantolizin hücresel mekanizması desmozom düzeyinde nasıl gerçekleşir?"
        ]
    },

    # SLIDE 8
    {
        "slideNumber": 8,
        "title": "Tip II Hipersensitivite: Hücresel Disfonksiyon ve Reseptör Antikorları",
        "subtitle": "Doku Nekrozu Olmadan Fonksiyon Değişimi: Myasthenia Gravis ve Graves Hastalığı",
        "badge": "Fonksiyon Bozukluğu",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Doku Hasarsız Tip II Aşırı Duyarlılık

Tip II aşırı duyarlılık reaksiyonlarının en zarif ve özgün mekanizmasıdır: **Doku hasarı, hücre nekrozu veya enflamasyon YOKTUR**. Antikorlar hücre yüzeyindeki kritik fizyolojik reseptörlere tıpkı bir ligand gibi bağlanarak:
1. Reseptörü **bloke eder veya yıkar** (Fonksiyon kaybı / İnhibisyon)
2. Reseptörü **sürekli ve kontrolsüz şekilde uyarır** (Fonksiyon artışı / Stimülasyon)

### 2. İki Zıt Uç Nokta: Myasthenia Gravis vs. Graves Hastalığı

```
               [ MYASTHENIA GRAVIS ]                         [ GRAVES HASTALIĞI ]
          (Antikor Reseptörü BLOKE EDER)                (Antikor Reseptörü UYARIR)
                        │                                             │
                        ▼                                             ▼
             Motor Son Plaktaki Asetilkolin                 Tiroid Folikül Hücresindeki
             Reseptörüne (AChR) Karşı Antikor               TSH Reseptörüne Karşı Antikor (TSI)
                        │                                             │
                        ▼                                             ▼
             Reseptör Bloke Olur ve Hücre İçi              Antikor TSH Gibi Davranarak
             İnternalize Edilerek Parçalanır               Adenylyl Siklazı Sürekli Aktive Eder
                        │                                             │
                        ▼                                             ▼
             Sinir-Kas Kavşağında İleti Durur              Kontrolsüz Aşırı T3/T4 Sentezi
                        │                                             │
                        ▼                                             ▼
             KAS GÜÇSÜZLÜĞÜ, PTOZİS, DİPLOOPİ              TİROTOKSİKOZ, HİPERTİROİDİZM, EKZOFTALMUS
```

### 3. Diğer Reseptör/Protein Disfonksiyonu Örnekleri

- **Pernisiyöz Anemi**: Mide paryetal hücrelerinin salgıladığı **İntrinsik Faktöre (IF)** karşı gelişen nötralizan otoantikorlar, B12 vitamininin ileumdan emilmesini bloke eder; megaloblastik anemi ve nöropati gelişir.
- **İnsülin Dirençli Diyabet (Tip B)**: İnsülin reseptörüne bağlanan antikorlar insülinin bağlanmasını engeller.
""",
        "spotPearls": [
            "▸ **Reseptör Modülasyonu Prensibi**: Antikorların kompleman fiksasyonu veya nötrofil çağırmaksızın, yalnızca anahtar-kilit uyumuyla hücresel sinyalleri açması veya kapatması durumudur.",
            "🔴 ÖNEMLİ: Myasthenia Gravis vs. Graves Hastalığı Zıtlığı:\n  ▫ **Myasthenia Gravis (İnhibitör/Bloke Edici Antikor)**: Nöromüsküler kavşaktaki motor son plakta **Asetilkolin reseptörlerine (AChR)** bağlanan otoantikorlar, reseptörleri yıkar ve bloke eder. Enflamasyon veya hücre ölümü yoktur; kas yorgunluğu ve ptozis gelişir.\n  ▫ **Graves Hastalığı (Stimülatör/Uyarıcı Antikor)**: Tiroid folikül hücrelerindeki **TSH reseptörüne** bağlanan tiroid stimüle edici immünoglobulinler (TSI), ligand gibi davranarak adenilat siklazı uyarır ve aşırı T3/T4 üretimine yol açar.",
            "🔵 ÇIKMIŞ SORU: *'Aşağıdaki hastalıklardan hangisinde doku nekrozu veya enflamasyon olmaksızın, reseptör fonksiyonunun antikor tarafından uyarılması sonucu patoloji gelişir?'*\n  ▫ Doğru yanıt: **Graves Hastalığı**'dır."
        ],
        "coreContent": [
            {"title": "Myasthenia Gravis", "description": "AChR antikorları ile sinir-kas kavşağında reseptör tükenmesi.", "highYieldBadge": "Nöromüsküler", "details": "Gün içinde eforla artan kas zaafiyeti ve ptozis tipiktir; timoma ile sık birliktedir."},
            {"title": "Graves Hastalığı", "description": "TSH reseptörüne agonist gibi bağlanan stimülatör antikorlar (TSI).", "highYieldBadge": "Endokrin", "details": "TSH baskılanır, serbest T3 ve T4 kanda fırlar; diffüz toksik guatr oluşur."},
            {"title": "Pernisiyöz Anemi", "description": "İntrinsik faktör ve paryetal hücre antikorları.", "highYieldBadge": "Hematoloji", "details": "B12 emilim kusuru ve subakut kombine kord dejenerasyonu yaratır."}
        ],
        "flashcards": [
            {"id": "fc-hs-15", "front": "Myasthenia Gravis'te otoantikorların bağlandığı hedef yapı neresidir?", "back": "Motor son plaktaki nikotinik Asetilkolin Reseptörleridir (AChR).", "tag": "Nöroloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-16", "front": "Graves hastalığında hipertiroidiye yol açan otoantikorun adı ve hedefi nedir?", "back": "Tiroid stimüle edici immünoglobulin (TSI / TRAb); tiroid folikül hücrelerindeki TSH reseptörünü uyarır.", "tag": "Endokrin", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-08",
                "question": "Göz kapağında düşme (ptozis) ve çiğneme kaslarında günün ilerleyen saatlerinde artan güçsüzlük şikayetiyle başvuran 32 yaşındaki kadında doku biyopsisinde hiçbir nekroz veya enflamasyon izlenmiyor. Bu hastanın hastalığının patogenezindeki temel immün mekanizma hangisidir?",
                "options": [
                    "A) İmmün komplekslerin motor nöron aksonlarına çökmesi",
                    "B) Motor son plaktaki asetilkolin reseptörlerinin antikor aracılığıyla bloke ve internalize edilmesi",
                    "C) CD8+ T lenfositlerinin iskelet kas liflerini perforinle parçalaması",
                    "D) Kolinesteraz enziminin genetik yokluğu",
                    "E) Mast hücrelerinden salınan histaminin sinir iletisini kesmesi"
                ],
                "correctAnswer": "B",
                "explanation": "Myasthenia Gravis, asetilkolin reseptörlerine karşı gelişen otoantikorların reseptörü bloke etmesi ve internalize ederek azaltması sonucu motor son plakta ileti yetersizliği yaratan prototip bir Tip II hücresel disfonksiyon hastalığıdır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Myasthenia gravis ile Lambert-Eaton miyastenik sendromunun presinaptik/postsinaptik antijen ayrımı nasıldır?",
            "Graves oftalmopatisinde retroorbital doku birikimini tetikleyen sitokin mekanizması nedir?"
        ]
    },

    # SLIDE 9
    {
        "slideNumber": 9,
        "title": "Tip III Hipersensitivite: İmmün Kompleks Patogenezi",
        "subtitle": "Çözünür Antijen-Antikor Kompleksleri, Vasküler Çökme ve Fibrinoid Nekroz",
        "badge": "Tip III İmmün Kompleks",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. Tip III Aşırı Duyarlılık: Temel Mantık

Tip III aşırı duyarlılık reaksiyonlarında antijen dokuda sabit değildir; kanda dolaşan **çözünür (soluble)** bir makromoleküldür. Dolaşımdaki bu antijenlere IgG veya IgM sınıfı antikorlar bağlanarak **Antijen-Antikor İmmün Kompleksleri** oluşturur.

Bu kompleksler damar duvarlarında biriktiğinde kompleman sistemini aktive eder ve şiddetli bir **nekrotizan vaskülit** tablosuna yol açar.

### 2. İmmün Kompleks Hasarının 3 Evresi

```
[ EVRE 1: Kompleks Oluşumu ]
Dolaşıma giren çözünür antijene karşı antikor sentezlenir; kanda birleşirler.
                     │
                     ▼
[ EVRE 2: Damar Duvarına Çökme ]
Hafif antijen fazlalığında oluşan ORTA BÜYÜKLÜKTEKİ kompleksler fagositozdan kaçar;
yüksek filtrasyon basıncına sahip mikrovasküler yataklara (glomerül, sinovya) çöker.
                     │
                     ▼
[ EVRE 3: Doku Enflamasyonu ve Fibrinoid Nekroz ]
Kompleman fiksasyonu -> C5a salınımı -> Nötrofil akını -> Lizozomal enzim deşarjı.
Damar duvarı nekroze olur; plazma proteinleri sızarak amorf pembe FİBRİNOİD NEKROZ oluşturur.
```

### 3. İmmün Kompleks Boyutunun Hayati Önemi

- **Büyük Kompleksler (Aşırı Antikor Varlığında)**: Retiküloendotelyal sistem (dalak ve karaciğer makrofajları) tarafından hızla yakalanır ve dolaşımdan temizlenir; dokuya çökemezler.
- **Küçük Kompleksler (Aşırı Antijen Varlığında)**: Damar duvarına takılmadan glomerüllerden süzülüp idrarla atılırlar; patoloji yapmazlar.
- **Orta Büyüklükteki Kompleksler (Hafif Antijen Fazlalığı)**: En tehlikeli olanlardır! Makrofaj fagositozundan kaçarlar, endotel aralıklarından damar duvarına girer ve bazal membranlara sıkışıp kalırlar.
""",
        "spotPearls": [
            "▸ **İmmün Kompleks Boyutu Kuralı**:\n  ▫ Çok büyük kompleksler dalak makrofajlarınca hızla temizlenir.\n  ▫ Çok küçük kompleksler dolaşımda kalıp atılır.\n  ▫ **Orta büyüklükteki immün kompleksler** (hafif antijen fazlalığında oluşanlar) damar duvarlarına en kolay çöken ve en patojenik olan formdur.",
            "🔴 ÖNEMLİ: Fibrinoid Nekroz ve Doku Tercihleri:\n  ▫ İmmün kompleksler yüksek filtrasyon basıncına sahip mikrovasküler yataklara çöker: **Glomerüller (nefrit)**, **Sinovyum (artrit)** ve **Küçük arterler/arteriyoller (vaskülit)**.\n  ▫ Histopatolojik imza lezyonu: Damar duvarında amorf, eozinofilik, parlak pembe **Fibrinoid Nekroz** ve nötrofil infiltrasyonudur (lökositoklazik vaskülit).",
            "🔵 ÇIKMIŞ SORU: *'Tip III aşırı duyarlılık reaksiyonunda damar duvarında gelişen karakteristik nekroz tipi hangisidir?'*\n  ▫ Doğru yanıt: **Fibrinoid Nekroz**'dur."
        ],
        "coreContent": [
            {"title": "Fibrinoid Nekroz", "description": "Damar duvarında antijen-antikor, kompleman ve plazma fibrininin eozinofilik birikimi.", "highYieldBadge": "Histopatoloji", "details": "Tip III hasarın en belirgin mikroskobik göstergesidir."},
            {"title": "Orta Boyutlu Kompleksler", "description": "Hafif antijen fazlalığında oluşan patojenik form.", "highYieldBadge": "Fizikokimya", "details": "Endotel aralıklarından subendotelyal ve mezangiyal alana geçer."},
            {"title": "Lökositoklazis", "description": "Damar duvarındaki nötrofillerin nükleer parçalanması (nükleer toz).", "highYieldBadge": "Morfoloji", "details": "Vaskülit biyopsilerinde lökositoklazik vaskülit tanısını koydurur."}
        ],
        "flashcards": [
            {"id": "fc-hs-17", "front": "İmmün komplekslerin damar duvarına çökmesinde en tehlikeli ve patojenik olan kompleks boyutu hangisidir?", "back": "Orta büyüklükteki (hafif antijen fazlalığında oluşan) immün kompleksler.", "tag": "Patoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-18", "front": "Tip III aşırı duyarlılıkta etkilenen kan damarı duvarlarında saptanan karakteristik nekroz tipi nedir?", "back": "Fibrinoid nekroz.", "tag": "Histopatoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-09",
                "question": "Aşağıdaki antijen-antikor durumlarından hangisinde oluşan immün kompleksler, retiküloendotelyal sistem tarafından temizlenemeyip damar duvarlarına en yüksek oranda çökerek Tip III doku hasarı oluşturur?",
                "options": [
                    "A) Aşırı antikor fazlalığında oluşan devasa kompleksler",
                    "B) Aşırı antijen fazlalığında oluşan minik monomerik kompleksler",
                    "C) Hafif antijen fazlalığında oluşan orta büyüklükteki kompleksler",
                    "D) Yalnızca IgA sınıfı monomerik kompleksler",
                    "E) Yalnızca IgE içeren mast hücresine bağlı kompleksler"
                ],
                "correctAnswer": "C",
                "explanation": "Hafif antijen fazlalığında oluşan orta büyüklükteki immün kompleksler, hem makrofaj fagositozundan kaçacak kadar küçük hem de endotel aralıklarına takılıp çökecek kadar büyüktür; bu nedenle en patojenik olanlardır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Fibrinoid nekroz ile kazeifikasyon nekrozunun etyolojik ve mikroskobik farkları nelerdir?",
            "Lökositoklazik vaskülitte damar duvarını yıkan lizozomal enzimler hangileridir?"
        ]
    },

    # SLIDE 10
    {
        "slideNumber": 10,
        "title": "Tip III Klinik Tablolar: Akut Serum Hastalığı ve Arthus Reaksiyonu",
        "subtitle": "Sistemik vs. Lokal İmmün Kompleks Hasarı, Hipokomplemantemi ve Granüler Patern",
        "badge": "Serum Hastalığı & Arthus",
        "badgeColor": "sky",
        "synthesisNarrative": """### 1. Akut Serum Hastalığı (Sistemik Prototip)

Tarihsel olarak at kaynaklı difteri veya tetanoz anti-serumu verilen hastalarda tanımlanmıştır. Günümüzde monoklonal antikor tedavileri (örn. Rituksimab) veya yabancı protein maruziyeti sonrasında görülür.

- **Zaman Çizelgesi**: Yabancı protein verildikten **7 ila 10 gün sonra**, kanda antikor üretimi başladığı anda immün kompleksler oluşur.
- **Klinik Triad**: Ateş, artralji/artrit ve deri döküntüsü (ürtikeryal/eritematöz). Sıklıkla lenfadenopati ve geçici proteinüri eşlik eder.
- **Laboratuvar Bulgusu**: Kompleksler kompleman sistemini tükettiği için serum **C3 ve C4 düzeyleri belirgin olarak düşer (Hipokomplemantemi)**. Antijen tükendiğinde hastalık kendi kendini sınırlar.

### 2. Arthus Reaksiyonu (Lokal Prototip)

Önceden aşılanmış veya duyarlaşmış (dolaşımında IgG antikorları bulunan) bir bireye veya deney hayvanına aynı antijenin **cilt altına veya kas içine lokal enjekte edilmesiyle** oluşur.
- Antijen enjeksiyon yerinde dokuya yayılırken, damardan çıkan antikorlarla damar duvarında yerinde (**in situ**) birleşir.
- 4 ila 10 saat içinde lokal alanda şiddetli ödem, vaskülit, hemoraji ve doku nekrozu gelişir.

### 3. İmmünofloresan Mikroskopi: Tip II vs. Tip III Ayrımı

| Özellik | Tip II Aşırı Duyarlılık (Örn: Goodpasture) | Tip III Aşırı Duyarlılık (Örn: SLE Nefriti / PSGN) |
| :--- | :--- | :--- |
| **Antijen Niteliği** | Doku bazal membranında **SABİT** | Kanda dolaşan **ÇÖZÜNÜR** |
| **Birikim Paterni** | Düzgün, kesintisiz, **ÇİZGİSEL (LİNEER)** | Düzensiz, topak topak, **GRANÜLER (NOKTASAL)** |
| **Elektron Mikroskopi** | Spesifik elektron yoğun kitle görülmez | Subendotelyal, mezangiyal veya subepitelyal **elektron yoğun birikimler** |
""",
        "spotPearls": [
            "▸ **Akut Serum Hastalığı Kliniği**: Yabancı protein verildikten yaklaşık 7-10 gün sonra kanda antikor üretimi zirveye ulaştığında ortaya çıkar.\n  ▫ Ateş, artralji, döküntü ve glomerülonefrit triadı izlenir; kompleksler komplemanı tükettiği için serum **C3 ve C4 düzeyleri belirgin olarak düşer (hipokomplemantemi)**.",
            "🔴 ÖNEMLİ: Arthus Reaksiyonu (Lokal Tip III):\n  ▫ Önceden antikor geliştirmiş bir bireye antijenin lokal enjekte edilmesiyle damar duvarında yerinde (in situ) kompleks oluşmasıdır.\n  ▫ 4-10 saat içinde lokal şişlik, hemoraji ve ağır doku nekrozu gelişir.",
            "🔵 ÇIKMIŞ SORU: *'Goodpasture sendromu (Tip II) ile Sistemik Lupus Eritematozus glomerülonefritinin (Tip III) immünofloresan incelemedeki en temel mikroskobik farkı nedir?'*\n  ▫ Doğru yanıt: Goodpasture'da bazal membran boyunca **Çizgisel (Lineer)** birikim görülürken; SLE ve Tip III hastalıklarda 'kum serpintisi' şeklinde **Granüler (Noktasal/Yumaksı)** immün birikim saptanır!"
        ],
        "coreContent": [
            {"title": "Hipokomplemantemi", "description": "Dolaşan komplekslerin komplemanı bağlaması sonucu serum C3/C4 seviyelerinde düşüş.", "highYieldBadge": "Laboratuvar", "details": "Serum hastalığı ve aktif SLE nefritinin kilit göstergesidir."},
            {"title": "Granüler İmmün Floresans", "description": "Tip III komplekslerin kapiller duvara topak topak düzensiz çökmesi.", "highYieldBadge": "İmmünofloresan", "details": "Noktasal 'yıldızlı gökyüzü' veya kaba yumaksı desen verir."},
            {"title": "Arthus Reaksiyonu", "description": "Lokalize vaskülit ve doku nekrozu modeli.", "highYieldBadge": "Lokal Model", "details": "Tekrarlayan aşı enjeksiyon yerlerindeki lokal nekrozları açıklar."}
        ],
        "flashcards": [
            {"id": "fc-hs-19", "front": "Akut serum hastalığında klinik bulguların antijen temasından 7-10 gün sonra ortaya çıkmasının nedeni nedir?", "back": "Spesifik antikorların üretilip antijenle kanda orta boy kompleksler oluşturabilmesi için geçen süre olmasıdır.", "tag": "Patofizyoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-20", "front": "Glomerül biyopsisinde granüler immünofloresan paterni hangi aşırı duyarlılık tipinin karakteristik bulgusudur?", "back": "Tip III (İmmün kompleks-aracılı) aşırı duyarlılık.", "tag": "Ayırıcı Tanı", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-10",
                "question": "Deri nekrozu şüphesiyle biyopsi yapılan bir hastanın arteriyol duvarında fibrinoid nekroz saptanıyor. Hastaya 8 gün önce yabancı protein içerikli antitoksin verilmiş olduğu ve şu an ateş, artralji ile birlikte serum C3 ve C4 düzeylerinde belirgin düşüklük olduğu öğreniliyor. Bu hastadaki immünopatolojik tanı nedir?",
                "options": [
                    "A) Akut Serum Hastalığı (Tip III)",
                    "B) Arthus Reaksiyonu (Tip II)",
                    "C) Sistemik Anafilaksi (Tip I)",
                    "D) Temas Dermatiti (Tip IV)",
                    "E) Atopik Ekzama (Tip I)"
                ],
                "correctAnswer": "A",
                "explanation": "Yabancı protein temasından 7-10 gün sonra ortaya çıkan ateş, artralji, vaskülit ve serum kompleman tüketimi (hipokomplemantemi) tablosu prototip Sistemik Akut Serum Hastalığıdır (Tip III).",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Serum hastalığında antijen, antikor ve kompleman düzeylerinin günlere göre seyrini gösteren eğri nasıldır?",
            "Lokal Arthus reaksiyonu ile Shwartzman reaksiyonu arasındaki fark nedir?"
        ]
    },

    # SLIDE 11
    {
        "slideNumber": 11,
        "title": "Tip IV Hipersensitivite: Gecikmiş Tip Aşırı Duyarlılık (DTH) ve Th1 Yanıtı",
        "subtitle": "Hücresel İmmünite, CD4+ Th1 Farklılaşması, IFN-γ ve Granülomatöz Enflamasyon",
        "badge": "Tip IV DTH",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Tip IV (Hücre-Aracılı) Aşırı Duyarlılığın Doğası

Tip IV aşırı duyarlılık, diğer üç tipten tamamen farklıdır: **Antikorlardan bağımsızdır**. Doku hasarı doğrudan duyarlaşmış T lenfositleri tarafından oluşturulur.
İki ana mekanizması vardır:
1. **Sitokin Aracılı Enflamasyon**: CD4+ T hücreleri (Th1 ve Th17)
2. **Doğrudan Sitotoksisite**: CD8+ Sitotoksik T Lenfositleri (CTL)

### 2. Gecikmiş Tip Aşırı Duyarlılık (DTH) ve Th1 Ekseninin İşleyişi

1. **Duyarlanma**: Protein antijeni antijen sunan hücrelerce (dendritik hücre/makrofaj) naif CD4+ T hücresine sunulur. Makrofajdan salınan **IL-12**, T hücresini **Th1** yönünde farklılaştırır.
2. **Uyarılma (Elisitasyon)**: Antijenle ikinci karşılaşmada Th1 hücreleri dokuya göç eder ve **İnterferon-gama (IFN-γ)** salgılar.
3. **Makrofaj Aktivasyonu**: IFN-γ doku makrofajlarını uyararak onları **klasik aktive (M1)** makrofajlara dönüştürür.
4. **Granülom Oluşumu**: Sürekli uyarılan M1 makrofajlar bol eozinofilik sitoplazmalı **epiteloid histiyositlere** dönüşür. Bunlar birbirleriyle birleşerek nükleusları at nalı şeklinde dizilen **Langhans tipi dev hücreleri** oluşturur.

```
Doku Antijeni (M. tuberculosis vb.)
       │
       ▼
Makrofaj/Dendritik Hücre -> IL-12 Salgılar
       │
       ▼
Naif CD4+ T Hücresi -> Th1 Hücresine Dönüşür
       │
       ▼ + Tekrar Karşılaşma
Th1 Hücresinden Yoğun IFN-γ Salınımı
       │
       ▼
Makrofaj Aktivasyonu (M1 Fenotipi) ve TNF Salınımı
  ┌────┴────────────────────────────────┐
  ▼                                     ▼
Epiteloid Histiyosit Dönüşümü        Langhans Dev Hücreleri
  │                                     │
  └──────────────────┬──────────────────┘
                     ▼
        [ GRANÜLOMATÖZ ENFLAMASYON ]
```

### 3. Tüberkülin (PPD) Deri Testi

- *Mycobacterium tuberculosis* antijenleri (PPD) intradermal verilir.
- Önceden duyarlaşmış bireylerde CD4+ Th1 hücreleri ve makrofajlar 8-12 saatte toplanmaya başlar; **24 ila 72. saatte** eritem ve sertlik (**endürasyon**) zirve yapar. Histolojide venüller çevresinde 'manşon' tarzı perivasküler mononükleer hücre infiltratı izlenir.
""",
        "spotPearls": [
            "▸ **Gecikmiş Tip (Delayed-Type) Tanımı**: Yanıtın maruziyetten hemen değil, T hücrelerinin bölgeye göç edip sitokin salgılaması için gereken **24 ila 72 saat sonra** zirveye ulaşması nedeniyle 'gecikmiş' olarak adlandırılır.",
            "🔴 ÖNEMLİ: Th1 - Makrofaj İki Yönlü Ekseninin Şifreleri:\n  ▫ Makrofajlar ve dendritik hücreler **IL-12** salgılayarak CD4+ T hücrelerini **Th1**'e dönüştürür.\n  ▫ Th1 hücreleri ise **IFN-γ (İnterferon-gama)** salgılayarak makrofajları en üst düzeyde aktive eder (M1 fenotipi).\n  ▫ Aktive makrofajlar bol sitoplazmalı **epiteloid histiyositlere** ve birleşerek at nalı nükleuslu **Langhans tipi dev hücrelere** dönüşür; granülomatöz enflamasyonun temelini atar.",
            "🔵 ÇIKMIŞ SORU: *'Tüberkülin (PPD) deri testinde 48-72 saat sonra ciltte oluşan endürasyon ve eritemden sorumlu olan temel aşırı duyarlılık tipi ve baskın efektör sitokin hangisidir?'*\n  ▫ Doğru yanıt: **Tip IV (Hücre-aracılı) hipersensitivite** ve **IFN-γ (İnterferon-gama)**'dır."
        ],
        "coreContent": [
            {"title": "İnterferon-Gama (IFN-γ)", "description": "Th1 hücrelerinin makrofaj aktivasyonunu sağlayan temel sitokini.", "highYieldBadge": "Kilit Sitokin", "details": "M1 makrofaj aktivasyonu ve granülom oluşumunun ana yöneticisidir."},
            {"title": "Epiteloid Histiyosit", "description": "Uzamış IFN-γ uyarımıyla makrofajın salgı hücresine benzeyen eozinofilik dönüşümü.", "highYieldBadge": "Histopatoloji", "details": "Granülomun temel yapı taşıdır."},
            {"title": "PPD Testi Zamanlaması", "description": "Hücresel göç ve sitokin kaskadı için gereken 48-72 saatlik gecikme.", "highYieldBadge": "Klinik Zaman", "details": "Erken saatlerdeki reaksiyonlar yalancı pozitiftir."}
        ],
        "flashcards": [
            {"id": "fc-hs-21", "front": "Granülomatöz enflamasyonda makrofajları aktive ederek epiteloid histiyositlere dönüştüren Th1 sitokini hangisidir?", "back": "İnterferon-gama (IFN-γ).", "tag": "İmmünoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-22", "front": "Tüberkülin PPD deri reaksiyonunda tepe yanıt neden 48-72 saat sonra alınır?", "back": "Duyarlanmış T hücrelerinin enjeksiyon alanına göç etmesi, sitokin salgılaması ve makrofajları toplaması zaman aldığından (gecikmiş tip).", "tag": "Fizyopatoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-11",
                "question": "Tüberküloz şüphesiyle PPD testi yapılan bir sağlık çalışanında 48 saat sonra kolda 18 mm çapında belirgin endürasyon saptanıyor. Bu lezyonun biyopsisinde saptanması beklenen temel hücresel infiltrat bileşeni aşağıdakilerden hangisidir?",
                "options": [
                    "A) Yoğun eozinofiller ve nötrofiller",
                    "B) Perivasküler CD4+ T lenfositleri ve aktive makrofajlar",
                    "C) Plazma hücreleri ve B lenfosit agregatları",
                    "D) Mast hücreleri ve bazofiller",
                    "E) Yalnızca eritrosit ekstravazasyonu ve fibrin"
                ],
                "correctAnswer": "B",
                "explanation": "Gecikmiş tip aşırı duyarlılıkta (DTH) perivasküler alanda toplanan CD4+ T lenfositleri ve bunların salgıladığı sitokinlerle aktive olan makrofaj infiltrasyonu (perivasküler manşonlaşma) izlenir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Klasik M1 makrofaj aktivasyonu ile alternatif M2 makrofaj aktivasyonunun sitokin ve fonksiyon farkları nelerdir?",
            "Granülomatöz hastalıklarda TNF-alfa inhibitörü başlanmadan önce neden PPD/QuantiFERON taraması zorunludur?"
        ]
    },

    # SLIDE 12
    {
        "slideNumber": 12,
        "title": "Tip IV Hipersensitivite: Th17 Hücreleri ve CD8+ CTL Sitotoksisitesi",
        "subtitle": "IL-17 ile Nötrofilik Hasar, Perforin/Granzim Apoptozu ve Kontakt Dermatit",
        "badge": "Th17 & CTL Hasarı",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. Th17 Hücrelerinin Rolü ve Nötrofilik Enflamasyon

Yakın geçmişte keşfedilen **CD4+ Th17 hücreleri**, Tip IV aşırı duyarlılığın akut yıkıcı formlarında kilit rol oynar:
- **IL-17 Salınımı**: Endotel ve stromal hücrelerden nötrofil çeken kemokinlerin (CXCL8 vb.) salınımını uyarır.
- Sonuç: Yoğun nötrofilik infiltrasyonla seyreden pürülan benzeri yıkıcı enflamasyon (Multipl Skleroz, Romatoid Artrit ve Psoriazis patogenezinde kritik).

### 2. CD8+ Sitotoksik T Lenfosit (CTL) Sitotoksisitesi

Hücre-aracılı aşırı duyarlılığın diğer kolunda, CD8+ CTL hücreleri hedef hücrenin yüzeyindeki **MHC Sınıf I** moleküllerine sunulan yabancı peptidleri tanır ve hedef hücreyi doğrudan ölüme gönderir:
1. **Perforin - Granzim Sistemi**:
   - **Perforin**: Hedef hücre zarına tutunarak delikler (porlar) açar.
   - **Granzim B**: Porlardan içeri girerek prokaspazları (Kaspaz-3) keser ve hedef hücreyi **apoptoza** sokar.
2. **FasL - Fas Yolağı**: CTL yüzeyindeki Fas Ligand (CD95L), hedef hücredeki Fas (CD95) reseptörüne bağlanarak Kaspaz-8 üzerinden kaspaz kaskadını başlatır.

### 3. Kontakt Dermatit (Temas Egzaması)

Nikel küpeler, zehirli sarmaşık (*urushiol* reçinesi), lateks, kozmetikler veya parfümler:
- Bunlar tek başına immünojenik olmayan küçük kimyasal maddelerdir (**Hapten**).
- Deri proteinlerine kovalent bağlanarak tam antijen haline gelirler.
- Epidermal **Langerhans hücreleri** bu hapten-protein komplekslerini yakalar, bölgesel lenf noduna taşır ve T hücrelerini duyarlaştırır.
- Tekrar temasta 24-48 saat sonra dermiste lenfositik infiltrat, epidermiste hücrelerarası ödem (**Spongiyoz**) ve kaşıntılı intraepidermal veziküller oluşur.
""",
        "spotPearls": [
            "▸ **CD8+ CTL Sitotoksisitesinin İki Ana İntihar Mekanizması**:\n  ▫ 1. **Perforin - Granzim Sistemi**: Perforin hedef hücre membranında por oluşturur; Granzim B porlardan girerek Kaspaz-3 ve kaspaz kaskadını doğrudan aktive ederek hücreyi apoptozla öldürür.\n  ▫ 2. **FasL - Fas (CD95) Etkileşimi**: CTL yüzeyindeki Fas Ligand hedef hücredeki Fas ölüm reseptörüne bağlanır; kaspaz-8 aktivasyonuyla apoptoz gerçekleşir.",
            "🔴 ÖNEMLİ: Kontakt Dermatit Patolojisi:\n  ▫ Nikel takılar, zehirli sarmaşık (urushiol) veya kozmetikler hapten olarak epidermise girer, keratinosit proteinleriyle birleşerek tam antijen olur.\n  ▫ Epidermal **Langerhans hücreleri** antijeni yakalar, lenf noduna taşır; duyarlanmış CD4+ ve CD8+ T hücreleri cilde dönerek vezikül, spongiyoz ve şiddetli kaşıntılı egzamatöz lezyonlar yapar.",
            "🔵 ÇIKMIŞ SORU: *'Tip 1 Diabetes Mellitus'ta pankreas adacıklarındaki insülin üreten beta hücrelerinin otoimmün yıkımından sorumlu temel immünolojik mekanizma hangisidir?'*\n  ▫ Doğru yanıt: **CD4+ Th1 ve CD8+ Sitotoksik T lenfositlerinin aracılık ettiği Tip IV Hücresel Aşırı Duyarlılık**'tır."
        ],
        "coreContent": [
            {"title": "Perforin ve Granzim", "description": "CTL ve NK hücrelerinin hedef hücreyi apoptoza soktuğu sitotoksik granül içeriği.", "highYieldBadge": "Apoptoz", "details": "Hücre zarı delinir ve kaspaz kaskadı tetiklenir."},
            {"title": "Hapten Prensibi", "description": "Kendi başına immün yanıt oluşturamayan, doku proteinine bağlanınca antijenleşen küçük kimyasallar.", "highYieldBadge": "İmmünokimya", "details": "Nikel ve urushiol en sık kontakt dermatit haptenleridir."},
            {"title": "Spongiyoz", "description": "Kontakt dermatitte epidermiste keratinositler arasında ödem toplanması.", "highYieldBadge": "Histopatoloji", "details": "İntraepidermal vezikül ve bül oluşumuna yol açar."}
        ],
        "flashcards": [
            {"id": "fc-hs-23", "front": "CD8+ sitotoksik T lenfositlerinin hedef hücre membranında delik açarak içeri granzimlerin girmesini sağlayan molekülü nedir?", "back": "Perforin.", "tag": "Sitotoksisite", "masterLevel": "Kritik"},
            {"id": "fc-hs-24", "front": "Kontakt dermatitte epidermal antijen sunan dendritik hücre hangisidir?", "back": "Langerhans hücresidir (Birbeck granülleri içerir).", "tag": "Histoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-12",
                "question": "Yeni aldığı nikel kaplama saati taktıktan 36 saat sonra bileğinde kaşıntılı, eritematöz ve minik veziküllerle karakterize egzamatöz lezyonlar gelişen bir hastada bu dermatolojik tablonun patogenezinde rol oynayan temel immünolojik süreç hangisidir?",
                "options": [
                    "A) Nikelin mast hücrelerine bağlanarak doğrudan IgE bağımsız histamin salgılatması",
                    "B) Dolaşan anti-nikel immün komplekslerinin dermal kapillerleri tıkaması",
                    "C) Nikelin hapten olarak deri proteinlerine bağlanması ve duyarlaşmış T hücrelerinin Tip IV reaksiyon başlatması",
                    "D) Epidermal bazal membrana karşı IgG antikorlarının kompleman aktive etmesi",
                    "E) Nikelin derideki melanositleri fagosite eden makrofajları aktive etmesi"
                ],
                "correctAnswer": "C",
                "explanation": "Nikel kontakt dermatiti klasik bir Tip IV gecikmiş aşırı duyarlılık tablosudur. Nikel hapten olarak cilt proteinlerine bağlanır, Langerhans hücrelerince lenf noduna taşınır ve duyarlaşan T hücreleri 24-48 saat sonra temas alanında spongiyotik dermatit tablosu oluşturur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kontakt dermatit (Tip IV) ile kontakt ürtiker (Tip I) arasındaki ayırıcı tanı basamakları nelerdir?",
            "Th17 hücresinin farklılaşmasında rol oynayan transkripsiyon faktörü (RORγt) ve sitokinler (IL-6, TGF-β, IL-23) nelerdir?"
        ]
    },

    # SLIDE 13
    {
        "slideNumber": 13,
        "title": "İmmünolojik Tolerans: Santral Toleransın Genetik Temeli ve AIRE Geni",
        "subtitle": "Timik Negatif Seleksiyon, AIRE Mutasyonu (APECED) ve Reseptör Düzenlemesi",
        "badge": "Santral Tolerans",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. İmmünolojik Toleransın Anlamı

İmmün sistemin rastgele genetik rekombinasyon (V(D)J rekombinasyonu) yoluyla ürettiği antijen reseptörleri, kaçınılmaz olarak vücudun kendi öz dokularını (self antijenleri) da tanıyabilir. Vücudun kendi antijenlerine karşı yanıtsızlık (tepkisizlik) haline **İmmünolojik Tolerans** denir. Bu tolerans bozulduğunda **Otoimmünite** gelişir.

Tolerans iki aşamada sağlanır:
1. **Santral Tolerans**: Birincil lenfoid organlarda (Timus ve Kemik İliği)
2. **Periferik Tolerans**: İkincil lenfoid organlar ve çevre dokularda

### 2. T Hücrelerinde Timik Santral Tolerans ve AIRE Geni

Timusta T hücre öncülleri iki zorlu sınavdan geçer:
- **Pozitif Seleksiyon (Korteks)**: Kendi MHC moleküllerini orta düzeyde tanıyanlar yaşar, hiç tanımayanlar ihmalden ölür (death by neglect).
- **Negatif Seleksiyon (Medulla)**: Kendi peptit-MHC komplekslerini **aşırı yüksek afiniteyle tanıyan oto-reaktif klonlar apoptoza gönderilerek elenir (Klonal Delesyon)**.

```
+-----------------------------------------------------------------------------------+
|                        AIRE (Autoimmune Regulator) GENİ                           |
+-----------------------------------------------------------------------------------+
| Soru: Timustaki T hücresi, göz, tiroid, pankreas veya adrenal gibi uzaktaki organ |
|       antijenleriyle timus içinde nasıl karşılaşabilir?                           |
| Yanıt: Medüller timik epitel hücrelerinde eksprese edilen AIRE transkripsiyon     |
|        faktörü sayesinde periferik doku antijenleri timusta sentezlenir!          |
|                                                                                   |
| AIRE MUTASYONU -> APECED / APS-1 (Otoimmün Poliendokrinopati Tip 1):             |
| 1. Kronik Mukokutanöz Kandidiyazis (anti-IL-17 antikorları nedeniyle)            |
| 2. Hipoparatiroidizm                                                              |
| 3. Adrenal Yetmezlik (Addison Hastalığı)                                          |
+-----------------------------------------------------------------------------------+
```

### 3. B Hücrelerinde Santral Tolerans ve Reseptör Düzenlemesi

Kemik iliğinde kendi antijenini tanıyan olgunlaşmamış B lenfositi için iki seçenek vardır:
1. **Apoptoz (Klonal Delesyon)**.
2. **Reseptör Düzenlemesi (Receptor Editing)**: B hücresi RAG1 ve RAG2 genlerini yeniden aktive ederek immünoglobulin **hafif zincir genlerini tekrar düzenler**. Yeni hafif zincir oto-reaktif değilse hücre kurtulur ve periferik dolaşıma geçer. Bu mekanizma B hücrelerine özgüdür!
""",
        "spotPearls": [
            "▸ **Santral Toleransın İki Kutsal Mekanı**:\n  ▫ T hücreleri için **Timus**, B hücreleri için **Kemik İliği**'dir.\n  ▫ Kendine ait antijenleri yüksek afiniteyle tanıyan lenfosit klonları apoptozla yok edilir (klonal delesyon).",
            "🔴 ÖNEMLİ: AIRE Geni ve APECED / APS-1 Sendromu:\n  ▫ **AIRE (Otoimmün Regülatör) Transkripsiyon Faktörü**: Timustaki epitel hücrelerinin periferik doku antijenlerini (tiroid, adacık, adrenal) timusta eksprese etmesini sağlayarak T hücrelerinin eğitilmesini yönetir.\n  ▫ AIRE geninde mutasyon olursa: T hücreleri periferik organlara karşı eğitilemez ve **Otoimmün Poliendokrinopati-Kandidiyazis-Ektodermal Distrofi (APECED / APS-1)** tablosu ortaya çıkar.",
            "🔵 ÇIKMIŞ SORU: *'Santral tolerans sırasında kemik iliğinde kendi antijenini tanıyan olgunlaşmamış B lenfositinin apoptoza gitmek yerine RAG genlerini yeniden açarak immünoglobulin hafif zincirini değiştirmesi mekanizmasına ne ad verilir?'*\n  ▫ Doğru yanıt: **Reseptör Düzenlemesi (Receptor Editing)**'dir."
        ],
        "coreContent": [
            {"title": "AIRE Transkripsiyon Faktörü", "description": "Timik medullada periferik doku antijenlerinin sentezini sağlayan anahtar gen.", "highYieldBadge": "Genetik", "details": "Mutasyonunda APECED / APS-1 sendromu gelişir."},
            {"title": "Reseptör Düzenlemesi", "description": "Kemik iliğinde oto-reaktif B hücresinin hafif zincirini yeniden düzenleyip kendini kurtarması.", "highYieldBadge": "B Hücre Toleransı", "details": "RAG rekombinaz enzimlerinin yeniden açılmasıyla gerçekleşir."},
            {"title": "Negatif Seleksiyon", "description": "Kendi antijenini aşırı güçlü bağlayan timositlerin apoptozla yok edilmesi.", "highYieldBadge": "T Hücre Eğitimi", "details": "Klonal delesyon santral toleransın en yaygın sonucudur."}
        ],
        "flashcards": [
            {"id": "fc-hs-25", "front": "Timusta periferik doku antijenlerinin ekspresyonunu sağlayarak negatif seleksiyonu yöneten gen hangisidir?", "back": "AIRE (Autoimmune Regulator) geni.", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-hs-26", "front": "Oto-reaktif B hücrelerinin kemik iliğinde hafif zincirini değiştirerek tolerans kazanmasına ne ad verilir?", "back": "Reseptör Düzenlemesi (Receptor Editing).", "tag": "İmmünoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-13",
                "question": "Çocukluk çağında kronik mukokutanöz kandidiyazis, hipoparatiroidizm ve adrenal yetmezlik (Addison hastalığı) tanıları alan bir hastada, timik negatif seleksiyon sırasında periferik doku antijenlerinin ekspresyonundan sorumlu hangi gende mutasyon saptanması beklenir?",
                "options": [
                    "A) FoxP3",
                    "B) AIRE",
                    "C) FAS (CD95)",
                    "D) CTLA-4",
                    "E) BTK"
                ],
                "correctAnswer": "B",
                "explanation": "Kronik mukokutanöz kandidiyazis, hipoparatiroidizm ve adrenal yetmezlik triadı APECED (Otoimmün Poliendokrinopati Tip 1) sendromudur ve timusta periferik antijen sunumunu sağlayan AIRE gen mutasyonuna bağlıdır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "APECED hastalarında neden mukokutanöz kandidiyazis gelişir? (Anti-IL-17 otoantikorlarının rolü)",
            "Timik pozitif seleksiyonda kortikal epitel hücrelerinin rolü nedir?"
        ]
    },

    # SLIDE 14
    {
        "slideNumber": 14,
        "title": "İmmünolojik Tolerans: Periferik Tolerans, Anerji ve Treg (FoxP3)",
        "subtitle": "Kostimülasyonsuzluk (Anerji), CTLA-4/PD-1 Kontrol Noktaları ve FoxP3 (IPEX)",
        "badge": "Periferik Tolerans",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. Periferik Toleransa Neden İhtiyaç Duyulur?

Santral tolerans mükemmel değildir; bazı oto-reaktif lenfositler timus ve kemik iliğinden kaçarak periferik dolaşıma geçer. Bu kaçak klonların çevre dokularda susturulmasını sağlayan mekanizmalar bütününe **Periferik Tolerans** denir.

Üç temel periferik tolerans mekanizması vardır:
1. **Anerji (Fonksiyonel İnaktivasyon)**
2. **Düzenleyici T Hücreleri (Treg) Tarafından Baskılanma**
3. **Aktivasyon Kaynaklı Hücre Ölümü (Apoptoz / AICD)**

```
               [ PERİFERİK TOLERANS MEKANİZMALARI ]
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
    [ ANERJİ ]             [ BASKILAMA (Treg) ]    [ DELİSYON (Apoptoz) ]
  Sinyal 1 Var,           CD4+ CD25+ FoxP3+        Tekrarlayan Uyarım ->
  Sinyal 2 (B7-CD28) Yok  Hücreler IL-10 ve        Fas - FasL (CD95)
  veya CTLA-4/PD-1 Aktif  TGF-β ile Baskılar       Aktivasyonu -> Apoptoz
```

### 2. Anerji ve İnhibitör Kontrol Noktaları (Checkpoints)

T hücresinin tam olarak aktive olabilmesi için iki sinyal şarttır:
- **Sinyal 1**: TCR'nin antijen-MHC kompleksini tanıması.
- **Sinyal 2 (Kostimülasyon)**: APC üzerindeki **B7 (CD80/CD86)** molekülünün T hücresindeki **CD28**'e bağlanması.

Normal dokularda enflamasyon olmadığı için APC'lerde B7 ekspresyonu düşüktür. T hücresi Sinyal 1'i alıp Sinyal 2'yi alamazsa **Anerjik** (kalıcı olarak işlevsiz) hale gelir.
- **CTLA-4**: CD28 ile yarışır ve B7'ye çok daha yüksek afiniteyle bağlanarak hücre içine negatif/frenleyici sinyal yollar.
- **PD-1**: Hedef dokulardaki PD-L1/PD-L2'ye bağlanarak T hücresi aktivasyonunu sonlandırır.

### 3. Düzenleyici T Hücreleri (Treg) ve FoxP3 Mutasyonu: IPEX Sendromu

Treg'ler timusta veya periferde gelişen özel bir T lenfosit alt grubudur:
- Yüzey belirteçleri: **CD4+ ve CD25+** (IL-2 reseptör alfa zinciri).
- Ana Transkripsiyon Faktörü: **FoxP3**.
- Etki Mekanizması: İmmünsüpresif sitokinler (**IL-10 ve TGF-β**) salgılar, sitokinleri tüketir ve CTLA-4 aracılığıyla APC'lerin B7 moleküllerini söküp alır (trans-endositoz).
- **FoxP3 Gen Mutasyonu -> IPEX Sendromu**:
  - **I**mmune dysregulation (İmmün disregülasyon)
  - **P**olyendocrinopathy (Tip 1 DM, tiroidit)
  - **E**nteropathy (Ölümcül inatçı sekretuar ishal)
  - **X**-linked (X'e bağlı geçiş; erken bebeklikte erkek çocuklarda ölümcül).
""",
        "spotPearls": [
            "▸ **Periferik Toleransın Üç Muhafızı**: **Anerji**, **Treg Baskılaması** ve **Aktivasyon Kaynaklı Hücre Ölümü (AICD - Apoptoz)**'dur.",
            "🔴 ÖNEMLİ: FoxP3 Transkripsiyon Faktörü ve IPEX Sendromu:\n  ▫ Düzenleyici T hücrelerinin (Treg: CD4+ CD25+) gelişimi ve fonksiyonu için mutlak gerekli transkripsiyon faktörü **FoxP3**'tür.\n  ▫ FoxP3 geninde inaktive edici mutasyon olduğunda Treg üretilemez; erken bebeklikte ölümcül otoimmün enteropati, tip 1 diyabet ve egzama ile karakterize **IPEX Sendromu** ortaya çıkar.",
            "🔵 ÇIKMIŞ SORU: *'İmmün yanıtta T hücresi üzerindeki CD28 aktivatör reseptörüyle yarışarak antijen sunan hücredeki B7 molekülüne çok daha yüksek afiniteyle bağlanan ve T hücresini frenleyen inhibitör kontrol noktası proteini hangisidir?'*\n  ▫ Doğru yanıt: **CTLA-4 (Sitotoksik T Lenfosit Antijeni 4)**'tür."
        ],
        "coreContent": [
            {"title": "FoxP3 ve Treg", "description": "CD4+ CD25+ düzenleyici T hücrelerinin ana transkripsiyon faktörü.", "highYieldBadge": "Kilit Gen", "details": "Mutasyonunda X'e bağlı ölümcül IPEX sendromu tablosu ortaya çıkar."},
            {"title": "CTLA-4 Freni", "description": "B7 moleküllerine CD28'den katbekat yüksek afiniteyle bağlanan inhibitör reseptör.", "highYieldBadge": "İmmün Kontrol", "details": "Kanser immünoterapisinde (İpilimumab) CTLA-4 hedeflenir."},
            {"title": "Anerji Mantığı", "description": "Kostimülasyonsuz antijen sunumu sonucu lenfositin kalıcı yanıtsızlığa girmesi.", "highYieldBadge": "Tolerans", "details": "Oto-antijenlerin sessizce tolere edilmesinde en yaygın mekanizmadır."}
        ],
        "flashcards": [
            {"id": "fc-hs-27", "front": "Düzenleyici T hücrelerinin (Treg) temel transkripsiyon faktörü ve mutasyonunda gelişen sendrom nedir?", "back": "FoxP3; mutasyonunda IPEX sendromu gelişir.", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-hs-28", "front": "T hücresi üzerinde CD28 ile yarışarak APC'deki B7 molekülünü bağlayan inhibitör kontrol molekülü hangisidir?", "back": "CTLA-4 (CD152).", "tag": "İmmünoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-14",
                "question": "Erkek bir bebekte yaşamın ilk aylarında şiddetli inatçı kanlı/sulu ishal (enteropati), erken başlangıçlı Tip 1 diyabet ve yaygın egzama saptanıyor. Genetik analizde CD4+ CD25+ regülatuvar T hücre fonksiyon bozukluğu izleniyor. Bu hastada mutasyona uğramış transkripsiyon faktörü hangisidir?",
                "options": [
                    "A) AIRE",
                    "B) FoxP3",
                    "C) T-bet",
                    "D) GATA-3",
                    "E) STAT3"
                ],
                "correctAnswer": "B",
                "explanation": "Erkek bebekte enteropati, endokrinopati (diyabet) ve dermatit birlikteliği X'e bağlı IPEX sendromudur. Bu tablo regülatuvar T hücrelerinin (Treg) ana transkripsiyon faktörü olan FoxP3 gen mutasyonu sonucu gelişir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "CTLA-4 ile PD-1 kontrol noktalarının sinyal iletimi ve anatomik çalışma yerleri arasındaki fark nedir?",
            "Treg hücrelerinin IL-10 ve TGF-beta aracılığıyla efektör T hücrelerini baskılama basamakları nelerdir?"
        ]
    },

    # SLIDE 15
    {
        "slideNumber": 15,
        "title": "Otoimmünite Gelişiminde Genetik ve Çevresel Faktörler",
        "subtitle": "HLA Lokusları (HLA-B27, DR4, DR3), Moleküler Taklit ve Epitop Yayılması",
        "badge": "Etyopatogenez",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Otoimmünite: Genetik ve Çevrenin Kesişimi

Otoimmünite gelişiminde tek bir gen veya tek bir çevresel tetikleyici nadiren yeterlidir (tek genli AIRE ve FoxP3 istisnadır). Genel kural **Poligenik Yatkınlık + Çevresel Tetikleyiciler** birlikteliğidir.

### 2. Genetik Faktörler: HLA Alelleri En Güçlü Birlikteliktir

MHC (İnsanda HLA) molekülleri peptid bağlama oluklarının geometrisine göre belirli otoantijenleri T hücrelerine çok daha kolay sunar:

| HLA Aleli | İlişkili Otoimmün Hastalık | Rölatif Risk Artışı |
| :--- | :--- | :--- |
| **HLA-B27** | **Ankilozan Spondilit** | **> 90 Kat!** (En yüksek rölatif risk) |
| **HLA-DR4** | Romatoid Artrit | 4-10 Kat |
| **HLA-DR3 ve DR4** | Tip 1 Diabetes Mellitus | 15-20 Kat (Heterozigotlarda risk katlanır) |
| **HLA-DR3** | Sistemik Lupus Eritematozus (SLE), Sjögren | 3-5 Kat |
| **HLA-DQ2 ve DQ8** | Çölyak Hastalığı | %95+ hastalarda pozitiftir |

*Non-HLA Genler*: PTPN22 polimorfizmi (T ve B hücre sinyal freni kaybı), NOD2 polimorfizmi (Crohn hastalığı).

### 3. Çevresel Faktörler ve Moleküler Taklit (Molecular Mimicry)

1. **Moleküler Taklit (Molecular Mimicry)**:
   - Bir mikrobiyal patojenin peptidi ile konak dokusundaki bir protein rastlantısal olarak birbirine çok benzer (çapraz reaksiyon).
   - *Klasik Prototip*: **Akut Romatizmal Ateş (ARA)**. Boğaz enfeksiyonu yapan *Streptococcus pyogenes* bakterisinin **M proteinine** karşı üretilen antikorlar, kardiyak miyozin ve kalp kapak endoteliyle çapraz reaksiyon vererek miyokardit ve kapak harabiyeti yapar.
2. **Kriptik Antijenlerin Açığa Çıkması**:
   - İmmün ayrıcalıklı (priviledged) bölgelerdeki (göz içi, testis, beyin) kapalı antijenlerin travma veya enfeksiyonla dolaşıma karışması (**Sempatik Oftalmi**).
3. **Epitop Yayılması (Epitope Spreading)**:
   - Başlangıçta tek bir antijene karşı başlayan otoimmün hasar dokuyu parçaladıkça, yeni hücre içi proteinler ortama dökülür ve yanıt giderek genişleyerek çok sayıda yeni antijene yayılır.
""",
        "spotPearls": [
            "▸ **HLA ve Otoimmün Hastalık Birlikteliği**: İmmün sistemin otoantijenleri sunma kabiliyeti MHC (HLA) alellerinin oluk yapısına bağlıdır; belirli aleller otoimmünite riskini katbekat artırır.",
            "🔴 ÖNEMLİ: Moleküler Taklit (Molecular Mimicry) Prototipi:\n  ▫ **Akut Romatizmal Ateş (ARA)**: Üst solunum yolu enfeksiyonu yapan *Streptococcus pyogenes* (Grup A beta-hemolitik streptokok) bakterisinin **M proteinine** karşı üretilen antikorlar, kardiyak miyozin ve kalp kapak glikoproteinleri ile çapraz reaksiyon verir.\n  ▫ Enfeksiyon geçtikten 2-3 hafta sonra pankardit ve kapak harabiyeti gelişir.",
            "🔵 ÇIKMIŞ SORU: *'HLA-B27 aleli ile en güçlü ilişki gösteren ve omurgada sindezmofitler ile bambu kamışı görüntüsüne yol açan seronegatif spondiloartropati hangisidir?'*\n  ▫ Doğru yanıt: **Ankilozan Spondilit**'tir (HLA-B27 pozitifliği %90'ın üzerindedir)."
        ],
        "coreContent": [
            {"title": "HLA-B27", "description": "Ankilozan spondilit ile 90 kattan fazla rölatif risk gösteren MHC Sınıf I aleli.", "highYieldBadge": "İmmünogenetik", "details": "Reaktif artrit ve psöriyatik artritte de pozitiftir."},
            {"title": "Moleküler Taklit", "description": "Streptokok M proteini ile kalp kapak antijenlerinin çapraz reaksiyonu.", "highYieldBadge": "ARA Mekanizması", "details": "Mikrop temizlense bile kardit tablosu haftalarca sürer."},
            {"title": "Epitop Yayılması", "description": "Doku yıkımı arttıkça otoimmün yanıtın yeni hedeflere doğru genişlemesi.", "highYieldBadge": "Kronikleşme", "details": "Kronik otoimmün hastalıkların alevlenerek ilerlemesini açıklar."}
        ],
        "flashcards": [
            {"id": "fc-hs-29", "front": "HLA alelleri arasında bir hastalıkla bilinen en yüksek rölatif risk artışına (>90 kat) sahip eşleşme nedir?", "back": "HLA-B27 ve Ankilozan Spondilit.", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-hs-30", "front": "Akut Romatizmal Ateşte moleküler taklide yol açan bakteriyel antijen hangisidir?", "back": "Grup A Streptokokların M proteinidir.", "tag": "Mikrobiyoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-15",
                "question": "Geçirilmiş streptokok farenjitinden 3 hafta sonra göğüs ağrısı, üfürüm ve eklem ağrılarıyla başvuran bir çocukta, bakteriyel M proteinine karşı oluşan antikorların kalp kapakçıklarıyla çapraz reaksiyon vermesi aşağıdaki immünopatolojik mekanizmalardan hangisinin tipik örneğidir?",
                "options": [
                    "A) Aşırı Duyarlılık Reaksiyonu Tip I",
                    "B) Moleküler Taklit (Molecular Mimicry)",
                    "C) Santral Tolerans Eksikliği",
                    "D) Reseptör Düzenlemesi Defekti",
                    "E) Kriptik Antijen İzolasyonu"
                ],
                "correctAnswer": "B",
                "explanation": "Patojen antijeninin (streptokok M proteini) konak doku antijenine (kardiyak miyozin/kapak glikoproteinleri) yapısal benzerliği nedeniyle antikorların konak dokusuna saldırması Moleküler Taklit (Molecular Mimicry) olarak adlandırılır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "PTPN22 gen polimorfizminin lenfosit tirozin fosfataz aktivitesi üzerindeki etkisi nedir?",
            "Sempatik oftalmi tablosunda bir gözün travması sonrası diğer gözün körleşmesinin immünolojik temeli nedir?"
        ]
    },

    # SLIDE 16
    {
        "slideNumber": 16,
        "title": "Sistemik Lupus Eritematozus (SLE): Patogenez ve Otoantikor Spektrumu",
        "subtitle": "ANA Spektrumu, Anti-dsDNA, Anti-Smith (Sm), Tip I İnterferon İmzası",
        "badge": "SLE İmmünopatoloji",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Sistemik Lupus Eritematozus (SLE) Nedir?

SLE; hemen hemen her organı tutabilen, alevlenmeler ve remisyonlarla seyreden, prototip **sistemik otoimmün ve immün kompleks hastalığıdır**. Hastaların %90'ı doğurganlık çağındaki (15-40 yaş arası) kadınlardır (östrojen kolaylaştırıcı faktördür).

### 2. Patogenetik Mekanizma: Nükleer Çöplerin Temizlenememesi

1. **Defektif Hücresel Temizlik**: Normalde her gün milyarlarca hücre apoptoza gider ve makrofajlarca sessizce temizlenir. SLE'de apoptoz artmış, fagositer temizlik ise kusurludur.
2. **Nükleer Antijenlerin Sunumu**: Hücre nükleus kalıntıları (DNA, histonlar, ribonükleoproteinler) ortalıkta kalır.
3. **Plazmasitoid Dendritik Hücreler ve Tip I İnterferon**: İmmün kompleksler hücre içine girerek endozomal **TLR-7 ve TLR-9**'u aktive eder; muazzam miktarda **İnterferon-alfa (IFN-α)** salgılanır (**İnterferon İmzası**).
4. **B Hücre Hiperaktivitesi**: Poliklonal B hücre uyarımı ile nükleer bileşenlere karşı patojenik IgG otoantikorları üretilir.

### 3. SLE Otoantikor Atlası (Sınavların Vazgeçilmezi)

| Otoantikor Tipi | Görülme Sıklığı | Klinikopatolojik Anlamı |
| :--- | :--- | :--- |
| **ANA (Antinükleer Antikor)** | **%98 - 100** | **En yüksek duyarlılık (sensitivite)**; tarama testidir. Negatifse SLE neredeyse imkansızdır; ancak pozitifliği SLE'ye özgü değildir. |
| **Anti-dsDNA (Çift İplikli DNA)** | %40 - 70 | **SLE'ye spesifiktir**. Düzeyi **Lupus Nefriti** şiddeti ve hastalık alevlenmesiyle birebir koreledir! Kompleman düşüşüyle paralel gider. |
| **Anti-Smith (Anti-Sm)** | %20 - 30 | **SLE için EN YÜKSEK ÖZGÜLLÜK (spesifite)** taşıyan antikordur. Pozitifliği SLE tanısını adeta mühürler. |
| **Anti-Histon** | > %95 (İlaca bağlı) | **İlaca Bağlı Lupus**'ta %95+ pozitiftir (Hidralazin, Prokainamid, İzoniyazid). |
| **Anti-SSA (Ro) ve Anti-SSB (La)** | %30 - 40 | Sjögren sendromunda da sıktır. Anneden bebeğe geçerek **Neonatal Lupus** ve **Konjenital Tam Kalp Bloğu** yapabilir! |
| **Antifosfolipid Antikorları** | %30 - 40 | Lupus antikoagülanı, anti-kardiyolipin; in vivo trombozlar ve tekrarlayan düşüklere yol açar. |
""",
        "spotPearls": [
            "▸ **SLE'nin İmmünopatolojik Özeti**: Nükleer kalıntıların temizlenememesi + B ve T hücre hiperreaktivitesi + Dolaşan patojenik IgG otoantikorları + Tip III immün kompleks birikimi ve Tip II sitotoksisite kombinasyonudur.",
            "🔴 ÖNEMLİ: SLE Otoantikorlarının Sınav Şifreleri:\n  ▫ **ANA**: En hassas (%98-100) tarama testidir; negatifse SLE dışlanır, ancak pozitifliği SLE'ye özgü değildir.\n  ▫ **Anti-dsDNA**: SLE'ye spesifiktir; düzeyi **lupus nefritinin şiddeti ve alevlenmeleriyle paralel seyreder**.\n  ▫ **Anti-Smith (Anti-Sm)**: SLE için **en yüksek özgüllüğe (spesifiteye)** sahip antikordur.\n  ▫ **Anti-Histon**: **İlaca bağlı lupus** olgularında neredeyse %100 pozitiftir.",
            "🔵 ÇIKMIŞ SORU: *'SLE tanılı bir hastada böbrek tutulumu (lupus nefriti) alevlenmesini ve hastalık aktivitesini takip etmede serumda bakılan en değerli otoantikor hangisidir?'*\n  ▫ Doğru yanıt: **Anti-dsDNA antikoru**'dur (titresi arttıkça kompleman C3/C4 düşer)."
        ],
        "coreContent": [
            {"title": "Anti-dsDNA", "description": "Lupus nefriti aktivitesi ve hipokomplemantemi ile paralel seyreden spesifik antikor.", "highYieldBadge": "Klinik Takip", "details": "Tedavi yanıtını ve alevlenmeleri izlemede kullanılır."},
            {"title": "Anti-Smith (Sm)", "description": "SLE için özgüllüğü en yüksek nükleer antikor.", "highYieldBadge": "En Spesifik", "details": "Ribonükleoproteinlerin çekirdek proteinlerini tanır."},
            {"title": "Anti-Histon", "description": "İlaca bağlı lupus olgularının biyobelirteci.", "highYieldBadge": "İlaca Bağlı", "details": "Hidralazin, prokainamid ve TNF inhibitörleri kullanımında pozitiftir."}
        ],
        "flashcards": [
            {"id": "fc-hs-31", "front": "SLE'de en yüksek sensitiviteye sahip tarama testi olan ve en yüksek spesifiteye sahip tanı testi olan antikorlar sırasıyla hangileridir?", "back": "En hassas: ANA; En spesifik: Anti-Smith (Sm) ve Anti-dsDNA.", "tag": "Seroloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-32", "front": "SLE'li gebe bir kadında bebeğin konjenital kalp bloğu ile doğma riskini belirleyen maternal antikorlar hangileridir?", "back": "Anti-SSA (Ro) ve Anti-SSB (La) antikorları.", "tag": "Kadın Doğum / Pediyatri", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-16",
                "question": "SLE tanısı ile izlenen 26 yaşındaki kadın hastada rutin kontrolde proteinüri (2.5 g/gün) ve mikroskopik hematüri saptanıyor. Bu hastada lupus nefriti alevlenmesini doğrulamak için istenmesi gereken en uygun otoantikor ve kompleman tetkik ikilisi hangisidir?",
                "options": [
                    "A) Anti-Histon yüksekliği ve C3/C4 artışı",
                    "B) Anti-dsDNA titresi yüksekliği ve C3/C4 seviyelerinde düşüş (hipokomplemantemi)",
                    "C) Yalnızca ANA pozitifliği ve C1 esteraz artışı",
                    "D) Anti-Sentromer antikor yüksekliği ve IgG4 artışı",
                    "E) Anti-CCP pozitifliği ve Romatoid Faktör artışı"
                ],
                "correctAnswer": "B",
                "explanation": "Lupus nefriti alevlenmesinde anti-dsDNA antikor titresi yükselir ve dolaşan immün komplekslerin komplemanı tüketmesi nedeniyle serum C3 ve C4 düzeyleri belirgin olarak düşer (hipokomplemantemi).",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "İlaca bağlı lupus ile idiyopatik SLE arasındaki klinik ve laboratuvar farklar nelerdir?",
            "ANA boyanma paternlerinin (homojen, benekli, nükleoler, periferal/rim) patolojik anlamları nelerdir?"
        ]
    },

    # SLIDE 17
    {
        "slideNumber": 17,
        "title": "SLE: Organ Tutulumları, Lupus Nefriti ve Libman-Sacks",
        "subtitle": "Lupus Nefriti Sınıflaması, Tel-Kulp (Wire-Loop), Malar Rash ve Libman-Sacks",
        "badge": "SLE Morfoloji",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. Lupus Nefriti (ISN/RPS Sınıflaması)

Böbrek tutulumu SLE'nin en sık rastlanan (%50) ve en önemli morbidite/mortalite nedenidir:

| Sınıf | İsim | Temel Işık Mikroskobu ve İmmünofloresan Bulgusu | Klinik Tablo |
| :--- | :--- | :--- | :--- |
| **Sınıf I** | Minimal Mezangiyal | Işık mikroskobu normal; mezangiumda immün birikimler. | Asemptomatik |
| **Sınıf II** | Mezangiyal Proliferatif | Mezangiyal hücre hipertrofisi ve matriks artışı. | Hafif proteinüri/hematüri |
| **Sınıf III** | Fokal Lupus Nefriti | Glomerüllerin <%50'sinde segmental/global proliferasyon. | Hematüri, proteinüri |
| **Sınıf IV** | **Diffüz Lupus Nefriti** | Glomerüllerin **>%50'sinde** yaygın proliferasyon, subendotelyal birikimler sonucu **TEL-KULP (WIRE-LOOP)** lezyonları. **EN SIK VE EN AĞIR TİPTİR!** | Nefrotik/Nefritik sendrom, böbrek yetmezliği |
| **Sınıf V** | Membranöz Lupus Nefriti | Subepitelyal birikimler, kapiller bazal membran kalınlaşması. | Masif proteinüri (Nefrotik sendrom) |
| **Sınıf VI** | İlerlemiş Sklerozan | Glomerüllerin >%90'ında skleroz ve fibröz kapanma. | Son dönem böbrek yetmezliği |

*Full-House İmmünofloresan*: Lupus nefritinde biyopside **IgG, IgA, IgM, C3 ve C1q** beşlisinin tamamının aynı anda pozitif olması 'Full-House' paterni olarak adlandırılır.

### 2. Cilt, Kalp ve Damar Tutulumları

- **Deri**: Güneş ışığıyla (UV) tetiklenen yüzde burun sırtını ve yanakları tutan ancak nazolabial olukları koruyan **Malar (Kelebek) Eritem**. Dermo-epidermal bileşkede granüler IgG birikimi (**Lupus Band Testi**).
- **Kalp**: **Libman-Sacks Endokarditi (Verrüköz Endokardit)**.
  - İnfektif endokardit ve romatizmal karditte vejetasyonlar kapakların yalnızca kan akımı yönündeki yüzüne yerleşirken;
  - **Libman-Sacks'ta steril vejetasyonlar kalp kapakçıklarının HEM ÖN (atriyal/ventriküler) HEM DE ARKA yüzünde** yerleşir!
- **Antifosfolipid Sendromu**:
  - Lupus antikoagülanı in vitro testte pıhtılaşmayı geciktirerek **aPTT'yi uzatır**; ancak in vivo ortamda **arteriyel ve venöz trombozlara**, inme ve tekrarlayan gebelik kayıplarına yol açar! Yalancı sifiliz (VDRL/RPR) pozitifliği verir.
""",
        "spotPearls": [
            "▸ **Diffüz Lupus Nefriti (Sınıf IV)**: SLE'de en sık rastlanan ve prognozu en kötü olan böbrek lezyonudur.\n  ▫ Işık mikroskobunda glomerül kapiller duvarlarının yaygın olarak kalınlaşmasıyla **Tel-Kulp (Wire-loop)** lezyonları saptanır.\n  ▫ İmmünofloresanda beşli pozitiflik (**Full-House paterni**: IgG, IgA, IgM, C3 ve C1q) karakteristiktir.",
            "🔴 ÖNEMLİ: Libman-Sacks Endokarditinin İki Yüzü:\n  ▫ İnfektif endokardit ve romatizmal karditte vejetasyonlar kapakların yalnızca kan akımı yönündeki yüzüne yerleşirken;\n  ▫ **Libman-Sacks Endokarditinde steril vejetasyonlar kalp kapakçıklarının HEM ÖN (atriyal/ventriküler) HEM DE ARKA yüzünde** yerleşir!",
            "🔵 ÇIKMIŞ SORU: *'SLE hastalarında in vitro ortamda aPTT testini uzatmasına rağmen, in vivo ortamda arteriyel ve venöz trombozlara, tekrarlayan fetal kayıplara ve trombositopeniye yol açan antikor grubu hangisidir?'*\n  ▫ Doğru yanıt: **Antifosfolipid Antikorları (Lupus Antikoagülanı ve Anti-kardiyolipin)**'dir."
        ],
        "coreContent": [
            {"title": "Diffüz Lupus Nefriti (Sınıf IV)", "description": "SLE'de en sık rastlanan ve agresif tedavi gerektiren böbrek lezyonu.", "highYieldBadge": "En Sık Tip", "details": "Tel-kulp (wire-loop) subendotelyal immün birikimleriyle tanınır."},
            {"title": "Libman-Sacks Endokarditi", "description": "Mitral ve aort kapakların her iki yüzeyine yerleşen steril verrüköz vejetasyonlar.", "highYieldBadge": "Kardiyak Patoloji", "details": "Enfeksiyöz değildir; kapak fonksiyonunu bozabilir ve emboli yapabilir."},
            {"title": "Lupus Band Testi", "description": "Dermo-epidermal bileşkede kesintisiz granüler IgG ve kompleman birikimi.", "highYieldBadge": "Dermatopatoloji", "details": "Güneş görmeyen sağlam deride de pozitif olması sistemik SLE lehinedir."}
        ],
        "flashcards": [
            {"id": "fc-hs-33", "front": "SLE nefritinde ışık mikroskobunda glomerül kapiller duvarında izlenen ve Sınıf IV'e özgü olan 'Tel-Kulp' (Wire-loop) lezyonunun nedeni nedir?", "back": "Kapiller bazal membranında yaygın subendotelyal immün kompleks birikimidir.", "tag": "Nefropatoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-34", "front": "Libman-Sacks endokarditinin vejetasyon yerleşimi açısından bakteriyel ve romatizmal endokarditten temel farkı nedir?", "back": "Vejetasyonların kalp kapaklarının hem ön hem arka yüzünde (her iki tarafında) steril olarak yerleşmesidir.", "tag": "Kardiyopatoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-17",
                "question": "30 yaşında SLE tanılı kadın hastanın ekokardiyografisinde mitral kapak ön ve arka yaprakçıklarının her iki yüzeyine yerleşmiş küçük, steril, verrüköz nodüller saptanıyor. Kan kültürlerinde üreme olmayan bu hastada tanımlanan kardiyak lezyon aşağıdakilerden hangisidir?",
                "options": [
                    "A) Akut Romatizmal Kardit vejetasyonları",
                    "B) Subakut Bakteriyel Endokardit",
                    "C) Libman-Sacks Endokarditi",
                    "D) Non-Bakteriyel Trombotik (Marantik) Endokardit",
                    "E) Karsinoid Kalp Hastalığı"
                ],
                "correctAnswer": "C",
                "explanation": "SLE hastalarında kapak yaprakçıklarının hem ön hem arka yüzüne yerleşen steril, küçük verrüköz lezyonlar Libman-Sacks endokarditidir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Lupus nefritinde 'Full-House' immünofloresan paterninin patolojik içeriği nedir?",
            "Antifosfolipid sendromunda aPTT'nin in vitro uzamasına rağmen in vivo tromboz gelişmesinin mekanizması nedir?"
        ]
    },

    # SLIDE 18
    {
        "slideNumber": 18,
        "title": "Romatoid Artrit (RA): Sinovit, Pannus ve Eklem Dışı Lezyonlar",
        "subtitle": "Simetrik Kronik Sinovit, Pannus Dokusu, Romatoid Faktör ve Anti-CCP",
        "badge": "Romatoid Artrit",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Romatoid Artrit (RA) Patogenezi

RA; öncelikle eklem sinovyasını hedef alan, kronik, sistemik enflamatuar bir otoimmün hastalıktır. Kadınlarda 3 kat sıktır.
- **İmmünolojik Başlatıcı**: Genetik olarak yatkın bireylerde (HLA-DR4), sigara dumanı veya enfeksiyonlar dokularda proteinlerin **sitrülinlenmesine (sitrülinasyon)** yol açar.
- İmmün sistem bu sitrülinlenmiş peptidleri yabancı kabul eder ve **Anti-CCP (ACPA)** antikorları üretir.
- CD4+ **Th1** (IFN-γ) ve **Th17** (IL-17) hücreleri sinovyayı infiltre eder; makrofajlardan yoğun **TNF-α**, **IL-1** ve **IL-6** salınır.

### 2. Histopatolojik İmza: Sinovyal Hiperplazi ve Pannus

1. **Kronik Proliferatif Sinovit**: Sinovyal örtü hücreleri (sinoviyositler) hiperplaziye uğrar (1-2 tabakadan 8-10 tabakaya çıkar), parmaksı villöz çıkıntılar oluşturur. Stromada lenfoid foliküller ve plazmosit kümeleri birikir.
2. **Pannus Dokusu**: Prolifere sinovyal hücreler, granülasyon dokusu ve enflamatuar hücrelerden oluşan agresif, tümör benzeri kitleye **Pannus** denir.
3. **Kıkırdak ve Kemik Yıkımı**: Pannustan salınan matriks metalloproteinazlar kıkırdağı eritir; osteoklast aktivasyonu eklem kenarlarında zımba deliği tarzı erozyonlar yapar. İlerleyen evrede fibröz ve **kemik ankilozu** gelişir.

### 3. Eklem Tutulum Deseni ve Seroloji

- **Eklem Dağılımı**: Küçük eklemler simetrik tutulur: El bileği, **Metakarpofalangeal (MKF)** ve **Proksimal interfalangeal (PİF)** eklemler. **Distal interfalangeal (DİF) eklemler KORUNUR!**
- **Serolojik Biyobelirteçler**:
  - **Romatoid Faktör (RF)**: Kendi **IgG'sinin Fc parçasına karşı gelişen IgM sınıfı otoantikor** (%70-80 pozitif). Sensitiftir ama spesifik değildir.
  - **Anti-CCP (Anti-Sitrülinlenmiş Peptid Antikoru)**: RA için **en yüksek özgüllüğe (%95+)** sahiptir ve erken evrede bile pozitiftir.
- **Romatoid Nodüller**: Olguların %25'inde basınç gören cilt altı bölgelerde (dirsek) görülür: Merkezde fibrinoid nekroz, çevresinde palizadik dizilimli histiyositler ve en dışta granülasyon dokusu.
""",
        "spotPearls": [
            "▸ **RA Eklem Tutulum Deseni**: El ve ayakların küçük eklemlerini (Metakarpofalangeal ve Proksimal interfalangeal) tutar.\n  ▫ Distal interfalangeal (DİF) eklemler korunur (DİF tutulumu Osteoartrit ve Psoriatik Artrite özgüdür).",
            "🔴 ÖNEMLİ: Pannus Dokusu ve Radyolojik Erozyonlar:\n  ▫ Sinovyanın granülasyon dokusu ve enflamatuar hücrelerle tümör benzeri kalınlaşmasına **Pannus** denir.\n  ▫ Pannustan salınan kollajenazlar kıkırdağı eritir; osteoklast aktivasyonu eklem kenarlarında zımba deliği tarzında kemik erozyonlarına ve ulnar deviasyona yol açar.",
            "🔵 ÇIKMIŞ SORU: *'Romatoid Artrit tanısında Romatoid Faktörden çok daha yüksek tanısal özgüllüğe (spesifiteye) sahip olan ve erken evrede bile pozitifleşebilen otoantikor hangisidir?'*\n  ▫ Doğru yanıt: **Anti-CCP (Sitrülinlenmiş Peptidlere Karşı Antikor)**'dur."
        ],
        "coreContent": [
            {"title": "Pannus", "description": "Sinovyal hiperplazi, granülasyon dokusu ve enflamatuar hücrelerden oluşan erozif kitle.", "highYieldBadge": "Histopatoloji", "details": "Kıkırdak ve kemik erozyonunun birincil kaynağıdır."},
            {"title": "Anti-CCP (ACPA)", "description": "Sitrülinlenmiş proteinlere karşı gelişen en spesifik RA belirteci.", "highYieldBadge": "En Spesifik", "details": "Erozif eklem hasarını önceden öngörmede çok değerlidir."},
            {"title": "Romatoid Nodül", "description": "Santral fibrinoid nekroz ve etrafında palizadik histiyosit kuşağı.", "highYieldBadge": "Doku Lezyonu", "details": "Cilt altı basınç noktalarında gelişen patognomonik lezyondur."}
        ],
        "flashcards": [
            {"id": "fc-hs-35", "front": "Romatoid Faktörün (RF) immünolojik tanımı nedir?", "back": "Kişinin kendi IgG antikorunun Fc parçasına karşı gelişen IgM sınıfı otoantikordur.", "tag": "İmmünoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-36", "front": "Romatoid artritte el eklemlerinden hangisi karakteristik olarak KORUNUR?", "back": "Distal interfalangeal (DİF) eklemler korunur (Osteoartrit tutar).", "tag": "Ayırıcı Tanı", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-18",
                "question": "Her iki elinde sabah tutukluğu, MKF ve PİF eklemlerinde simetrik şişlik ve ağrı yakınması olan 45 yaşındaki kadında çekilen el grafisinde periartiküler erozyonlar saptanıyor. Bu hastada tanıyı kesinleştirmede özgüllüğü en yüksek olan laboratuvar testi hangisidir?",
                "options": [
                    "A) Romatoid Faktör (RF)",
                    "B) Anti-Sitrülinlenmiş Peptid Antikoru (Anti-CCP)",
                    "C) Antinükleer Antikor (ANA)",
                    "D) Eritrosit Sedimantasyon Hızı (ESR)",
                    "E) Serum C-Reaktif Protein (CRP)"
                ],
                "correctAnswer": "B",
                "explanation": "Romatoid Artrit tanısında Anti-CCP (ACPA) %95'in üzerindeki özgüllüğü ile en spesifik biyobelirteçtir. RF daha sensitif olsa da diğer bağ dokusu hastalıklarında ve kronik enfeksiyonlarda da pozitifleşebilir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Romatoid artrit tedavisinde kullanılan biyolojik anti-TNF ajanların sinovyal pannus üzerindeki etkisi nedir?",
            "Osteoartrit ile romatoid artritin klinik, radyolojik ve patolojik karşılaştırma tablosu nasıldır?"
        ]
    },

    # SLIDE 19
    {
        "slideNumber": 19,
        "title": "Sjögren Sendromu ve Sistemik Skleroz (Skleroderma)",
        "subtitle": "Kseroftalmi, Kserostomi, Anti-SSA/SSB, Diffüz vs. Sınırlı (CREST) Skleroderma",
        "badge": "Sjögren & Skleroderma",
        "badgeColor": "sky",
        "synthesisNarrative": """### 1. Sjögren Sendromu (Sicca Sendromu)

Lakrimal ve tükürük bezlerinin immünolojik yıkımıyla karakterize kronik otoimmün ekzokrinopatidir.
- **Klinik Belirtiler**: Kuru göz (**Keratokonjunktivitis sikka / Kseroftalmi** - korneal ülser riski) ve kuru ağız (**Kserostomi** - disfaji, diş çürükleri).
- **Histopatoloji**: Dudak (minör tükürük bezi) biyopsisinde duktuslar etrafında yoğun CD4+ T ve plazma hücresi infiltratları (**Focus Score** $\ge 1$).
- **Otoantikorlar**: **Anti-SSA (Ro)** ve **Anti-SSB (La)** antikorları (%60-90 pozitif).
- **Malignite Riski**: B lenfositlerinin kronik kontrolsüz uyarımı nedeniyle bu hastalarda **B hücreli Non-Hodgkin Lenfoma (özellikle Marjinal Zon / MALT Lenfoma)** riski normal popülasyondan **40 kat fazladır**!

### 2. Sistemik Skleroz (Skleroderma)

Üç temel patolojik ayağı vardır:
1. Kronik vasküler endotel hasarı (**Obliteratif Vaskülopati**) -> Raynaud fenomeni, parmak ucu ülserleri.
2. İmmün aktivasyon (T ve B lenfositleri, otoantikorlar).
3. Aşırı kontrolsüz kollajen üretimi ve yaygın doku fibrozisi (özellikle **TGF-β** ve **PDGF** uyarımıyla fibroblast aktivasyonu).

### 3. İki Klinik Formun Hayati Karşılaştırması

| Özellik | Diffüz Skleroderma | Sınırlı Skleroderma (CREST Sendromu) |
| :--- | :--- | :--- |
| **Deri Tutulumu** | Hızlı, gövde ve proksimal ekstremiteleri de tutan yaygın deri sertleşmesi. | Yalnızca el, parmaklar ve yüz ile sınırlı tutulum. |
| **Visseral Organlar** | **Erken ve ağır viseral tutulum** (Pulmoner interstisyel fibrozis, Skleroderma böbrek krizi). | Geç dönemde gelişebilen pulmoner arteriyel hipertansiyon. |
| **Otoantikor** | **Anti-DNA Topoizomeraz I (Anti-Scl-70)** | **Anti-Sentromer Antikoru (ACA)** |
| **Klinik Bileşenler** | Hızlı parankim yetmezliği | **C**alcinosis, **R**aynaud, **E**sophageal dysmotility, **S**clerodactyly, **T**elangiectasia |
""",
        "spotPearls": [
            "▸ **Sjögren Sendromu Triadı**: Kuru göz (keratokonjunktivitis sikka), kuru ağız (kserostomi) ve romatoid artrit gibi eşlik eden bağ dokusu hastalığıdır.\n  ▫ Dudak biyopsisinde minör tükürük bezlerinde periduktal lenfosit odakları (focus score) tanı koydurucudur.",
            "🔴 ÖNEMLİ: Sklerodermada Antikor ve Form Eşleşmesi:\n  ▫ **Diffüz Skleroderma**: Yaygın cilt sertleşmesi ve akciğer fibrozisi yapar; otoantikoru **Anti-DNA Topoizomeraz I (Anti-Scl-70)**'dir.\n  ▫ **Sınırlı Skleroderma (CREST)**: Yalnızca el ve yüzde sınırlı tutulum yapar, geç dönemde pulmoner hipertansiyon gelişebilir; otoantikoru **Anti-Sentromer Antikoru (ACA)**'dır.",
            "🔵 ÇIKMIŞ SORU: *'Sjögren sendromu tanısıyla takip edilen bir hastada parotis bezinde ani büyüme ve lenfadenopati geliştiğinde en çok şüphelenilmesi gereken malignite hangisidir?'*\n  ▫ Doğru yanıt: **B hücreli Non-Hodgkin Lenfoma (özellikle Marjinal Zon / MALT Lenfoma)**'dır."
        ],
        "coreContent": [
            {"title": "MALT Lenfoma Riski", "description": "Sjögren sendromunda tükürük bezlerinde gelişebilen 40 kat artmış lenfoma riski.", "highYieldBadge": "Malignite Riski", "details": "Parotiste ani asimetrik büyüme lenfoma habercisidir."},
            {"title": "Anti-Scl-70 vs. ACA", "description": "Diffüz sklerodermada Anti-Scl-70; CREST sendromunda Anti-Sentromer antikoru pozitiftir.", "highYieldBadge": "Ayırıcı Tanı", "details": "Prognozu ve visseral tutulum riskini belirler."},
            {"title": "TGF-Beta ve Fibrozis", "description": "Sklerodermada fibroblastları aşırı kollajen üretimine sevk eden temel sitokin.", "highYieldBadge": "Patofizyoloji", "details": "Deri ve iç organlarda ilerleyici skleroza neden olur."}
        ],
        "flashcards": [
            {"id": "fc-hs-37", "front": "Diffüz sistemik skleroz ile sınırlı sistemik sklerozun (CREST) otoantikorları sırasıyla nelerdir?", "back": "Diffüz: Anti-DNA Topoizomeraz I (Anti-Scl-70); Sınırlı (CREST): Anti-Sentromer Antikoru (ACA).", "tag": "Seroloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-38", "front": "Sjögren sendromunda tükürük bezi biyopsisinde tanıyı doğrulayan histopatolojik kriter nedir?", "back": "Dudak biyopsisinde minör tükürük bezlerinde 50'den fazla periduktal lenfosit içeren odak (Focus Score >= 1).", "tag": "Histopatoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-19",
                "question": "Parmaklarında soğukta beyazlaşıp morarma (Raynaud), el derisinde gerginleşme ve yutma güçlüğü yakınması olan 50 yaşındaki hastada kalsinozis ve yüzde telenjiektaziler saptanıyor. Bu hastada pozitif çıkması en muhtemel otoantikor hangisidir?",
                "options": [
                    "A) Anti-DNA Topoizomeraz I (Anti-Scl-70)",
                    "B) Anti-Sentromer Antikoru (ACA)",
                    "C) Anti-dsDNA",
                    "D) Anti-Smith",
                    "E) Anti-Jo-1"
                ],
                "correctAnswer": "B",
                "explanation": "Kalsinozis, Raynaud, Özofagus dismotilitesi, Sklerodaktili ve Telenjiektazi bulguları CREST sendromuna işaret eder ve CREST sendromuna özgü otoantikor Anti-Sentromer Antikorudur (ACA).",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Skleroderma böbrek krizinin patolojisi (soğan zarı intimal proliferasyon) ve ACE inhibitörlerinin rolü nedir?",
            "Sjögren sendromundaki kuru gözün Schirmer testi ve Rose Bengal boyasıyla tanısı nasıl konur?"
        ]
    },

    # SLIDE 20
    {
        "slideNumber": 20,
        "title": "İmmunoglobulin G4 (IgG4) İlişkili Hastalık (IgG4-RD)",
        "subtitle": "Storiform Fibrozis, Yoğun IgG4+ Plazmasit İnfiltrasyonu ve Obliteratif Flebit",
        "badge": "IgG4-RD Patolojisi",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. IgG4-İlişkili Hastalık (IgG4-RD) Konsepti

Tıbbi patolojide son yirmi yılın en önemli kavramsal devrimlerinden biridir. Eskiden birbirinden tamamen bağımsız sanılan ve organa göre farklı isimler verilen birçok fibroinflamatuar hastalık, günümüzde **IgG4-RD çatısı altında** birleştirilmiştir:
- Tip 1 Otoimmün Pankreatit
- Riedel Tiroiditi (tiroidin tahta sertliğinde fibrozisi)
- Retroperitoneal Fibrozis (Ormond Hastalığı - üreterleri sarıp tıkayan fibrozis)
- Mikulicz Hastalığı (tükürük ve lakrimal bezlerin simetrik büyümesi)
- İnflamatuar Psödotümörler (orbita, akciğer, karaciğer kitleleri)

### 2. Histopatolojik Üç Kardinal Bulgu (Sınavın Altın Anahtarı)

Biyopsi yapılan organdan bağımsız olarak, IgG4-RD tanısı için şu **üç histolojik özelliğin** varlığı aranır:

```
+-----------------------------------------------------------------------------------+
|                         IgG4-RD ÜÇ KARDİNAL BULGUSU                               |
+-----------------------------------------------------------------------------------+
| 1. Yoğun Lenfoplazmasiter İnfiltrat:                                              |
|    Doku biyopsisinde IgG4-pozitif plazma hücre sayısında dramatik artış           |
|    (Büyük büyütme alanında >10-50 IgG4+ plazmosit ve IgG4/IgG oranı > %40).       |
|                                                                                   |
| 2. Storiform Fibrozis:                                                            |
|    Kollajen demetlerinin 'çarkıfelek' veya 'hasır örgü' tarzında girdapsı         |
|    dizilim gösterdiği karakteristik fibrozis paterni.                             |
|                                                                                   |
| 3. Obliteratif Flebit:                                                            |
|    Enflamatuar infiltratın ven duvarlarını sararak ve infiltre ederek ven         |
|    lümenini tamamen tıkaması (oblitere etmesi). Arterler genellikle korunur.     |
+-----------------------------------------------------------------------------------+
```

### 3. Klinik Özellikler ve Tedavi Yanıtı

- **Malignite Taklidi**: Organlarda oluşturduğu sert tümör benzeri kitleler nedeniyle sıklıkla pankreas veya akciğer kanseri zannedilerek hastalar gereksiz radikal cerrahiye alınır.
- **Kortikosteroid Yanıtı**: Kanserden kesin ayrımı sağlayan en çarpıcı klinik özelliği, **sistemik kortikosteroid tedavisine dramatik, hızlı ve tam yanıt vermesidir**; kitleler haftalar içinde erir!
""",
        "spotPearls": [
            "▸ **IgG4-RD Konsepti**: Çeşitli organlarda kitle oluşturarak maligniteyi taklit eden, ancak biyopside spesifik histopatoloji ve immünohistokimya ile tanınan sistemik fibroinflamatuar bir sendromdur.",
            "🔴 ÖNEMLİ: IgG4-RD Tanısı İçin Üçlü Histopatolojik Ayak:\n  ▫ 1. **Doku IgG4+ plazma hücresi sayısında dramatik artış** (IgG4/IgG oranı >%40).\n  ▫ 2. **Storiform (hasır örgüsü tarzı) kollajenöz fibrozis**.\n  ▫ 3. **Obliteratif flebit** (ven duvarlarının enflamasyonla lümeninin kapanması).\n  ▫ Not: Doku eozinofilisi eşlik edebilir ancak granülom veya dev hücre görülmez!",
            "🔵 ÇIKMIŞ SORU: *'Daha önce Riedel tiroiditi, otoimmün pankreatit ve retroperitoneal fibrozis (Ormond hastalığı) olarak bilinen tabloların ortak çatı altında toplandığı antite hangisidir?'*\n  ▫ Doğru yanıt: **IgG4-İlişkili Hastalık (IgG4-Related Disease)**'tır."
        ],
        "coreContent": [
            {"title": "Storiform Fibrozis", "description": "Kollajen bantlarının çarkıfelek veya hasır örgüsü benzeri girdapsı dizilimi.", "highYieldBadge": "Histopatoloji", "details": "IgG4-RD doku biyopsisinin en karakteristik yapısal özelliğidir."},
            {"title": "Obliteratif Flebit", "description": "Venöz yapıların enflamasyonla tıkanıp elastik liflerinin harabiyeti.", "highYieldBadge": "Vasküler", "details": "Arterler genellikle açık kalırken venler tamamen kapanır."},
            {"title": "Kortikosteroid Yanıtı", "description": "Maligniteyi taklit eden kitlelerin steroidle hızla gerilemesi.", "highYieldBadge": "Klinik Özellik", "details": "Pankreas kanseri şüphesini cerrahi öncesi ekarte etmede değerlidir."}
        ],
        "flashcards": [
            {"id": "fc-hs-39", "front": "IgG4-ilişkili hastalığın (IgG4-RD) biyopsideki üç kardinal histopatolojik bulgusu nedir?", "back": "1. Yoğun IgG4+ plazma hücre infiltratı, 2. Storiform fibrozis, 3. Obliteratif flebit.", "tag": "Histopatoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-40", "front": "Pankreas başı kitlesi, Riedel tiroiditi ve retroperitoneal fibrozis birlikteliğinde ilk akla gelmesi gereken sistemik sendrom nedir?", "back": "IgG4-İlişkili Hastalık (IgG4-RD).", "tag": "Patoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-20",
                "question": "Pankreas başında kitle nedeniyle opere edilen ve biyopsisinde malignite saptanmayan hastada, dokuda storiform (hasır örgü) tarzında fibrozis, ven lümenlerini tıkayan obliteratif flebit ve yoğun plazmosit infiltrasyonu izleniyor. İmmünohistokimyada bu plazmositlerin IgG4 pozitif olduğu gösteriliyor. Bu hasta için en olası tanı aşağıdakilerden hangisidir?",
                "options": [
                    "A) IgG4-İlişkili Hastalık (Tip 1 Otoimmün Pankreatit)",
                    "B) Duktal Adenokarsinom",
                    "C) Sistemik Lupus Eritematozus",
                    "D) Sarkoidoz Pankreatiti",
                    "E) Akut Nekrotizan Pankreatit"
                ],
                "correctAnswer": "A",
                "explanation": "Storiform fibrozis, obliteratif flebit ve dokuda bol IgG4-pozitif plazma hücre infiltrasyonu triadı IgG4-İlişkili Hastalığın (bu olguda Tip 1 Otoimmün Pankreatit) patognomonik histolojik tablosudur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Riedel tiroiditi ile Hashimoto tiroiditinin histopatolojik ve klinik ayrımı nasıldır?",
            "Retroperitoneal fibroziste (Ormond hastalığı) üreter obstrüksiyonu gelişimi ve tedavisi nasıl yönetilir?"
        ]
    },

    # SLIDE 21
    {
        "slideNumber": 21,
        "title": "Transplantasyon İmmünolojisi ve Organ Reddi Tipleri",
        "subtitle": "Hiperakut, Akut Sellüler/Humoral ve Kronik Rejeksiyon Mekanizmaları",
        "badge": "Transplantasyon Reddi",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Alloreaktivite ve Tanıma Yolları

Alıcının T lenfositleri donör dokusundaki yabancı HLA moleküllerini iki yolla tanır:
- **Direkt Yol**: Alıcının T hücreleri donör APC'lerinin yüzeyindeki intakt allojeneik MHC moleküllerini doğrudan tanır (Akut rejeksiyonda baskındır).
- **İndirekt Yol**: Donör MHC molekülleri alıcının kendi APC'leri tarafından parçalanıp normal bir yabancı antijen gibi sunulur (Kronik rejeksiyonda baskındır).

### 2. Organ Reddi (Rejeksiyon) Tipleri Tablosu

| Rejeksiyon Tipi | Zamanlama | Patogenetik Mekanizma | Histopatolojik Morfoloji |
| :--- | :--- | :--- | :--- |
| **Hiperakut Rejeksiyon** | **Dakikalar - Saatler** (Ameliyat masasında!) | Alıcı serumunda donör endotel antijenlerine (ABO veya HLA) karşı **önceden var olan pre-forme antikorlar**. | Yaygın trombotik tıkanma, kapillerde nötrofil infiltrasyonu, **damar duvarında fibrinoid nekroz**, greftin iskemik siyanozu ve nekrozu. |
| **Akut Hücresel Rejeksiyon** | Günler - Haftalar - Aylar | Donör HLA moleküllerine karşı uyarılmış **CD8+ CTL ve CD4+ Th1 hücreleri**. | Böbrek tübül epiteli arasına lenfosit girmesi (**Tubulit**) ve arter intimasında lenfosit infiltrasyonu (**Endotelit**). |
| **Akut Humoral Rejeksiyon** | Günler - Haftalar | Donöre karşı gelişen **Donör Spesifik Antikorlar (DSA)**. | Peritübüler kapillerlerde nötrofil birikimi (**peritübüler kapillerit**) ve kapiller endotelinde **C4d birikimi**! |
| **Kronik Rejeksiyon** | **Aylar - Yıllar** | T hücre sitokinleri ve antikorların uyardığı kronik vasküler proliferasyon (indirekt yol). | Damar düz kas hücresi göçüyle intimal kalınlaşma (**hızlanmış greft arteriyosklerozu**), interstisyel fibrozis, parankim atrofisi. Tedaviye yanıtsızdır. |
""",
        "spotPearls": [
            "▸ **Rejeksiyonun Zaman Çizelgesi ve Temel Sorumlusu**:\n  ▫ Hiperakut = Dakikalar/Saatler (Önceden var olan antikorlar + Fibrinoid nekroz).\n  ▫ Akut Hücresel = Günler/Haftalar (CD8+ CTL ve CD4+ T hücreleri + Tubulit/Endotelit).\n  ▫ Akut Antikor Aracılı = Donör Spesifik Antikorlar (DSA + Kapiller endotelde C4d pozitifliği).\n  ▫ Kronik = Aylar/Yıllar (Damar intimal kalınlaşması + İnterstisyel fibrozis).",
            "🔴 ÖNEMLİ: C4d Biyobelirteci ve Humoral Rejeksiyon:\n  ▫ Akut humoral rejeksiyon tanısında böbrek allogreft biyopsisinde peritübüler kapiller endotelinde **C4d kompleman fragmanı birikimi** immünohistokimyasal altın standart kanıttır.",
            "🔵 ÇIKMIŞ SORU: *'Böbrek transplantasyonu yapıldıktan 15 dakika sonra ameliyat masasında greftin aniden siyanotik, soluk ve flaks hale gelmesine yol açan hiperakut rejeksiyonun temel nedeni nedir?'*\n  ▫ Doğru yanıt: **Alıcının serumunda donör endotel antijenlerine (ABO veya HLA) karşı önceden oluşmuş pre-forme antikorların bulunması**dır."
        ],
        "coreContent": [
            {"title": "Hiperakut Rejeksiyon", "description": "Önceden var olan antikorlarla dakikalar içinde damarların trombozla tıkanması.", "highYieldBadge": "Pre-forme Antikor", "details": "Cross-match testi yapılarak tamamen önlenmesi amaçlanır."},
            {"title": "Tubulit ve Endotelit", "description": "Akut hücresel rejeksiyonda T lenfositlerinin tübül ve arter intimasını işgal etmesi.", "highYieldBadge": "Sellüler Rejeksiyon", "details": "Kortikosteroid ve T hücre baskılayıcı tedavilere mükemmel yanıt verir."},
            {"title": "C4d Kompleman Pozitifliği", "description": "Akut humoral rejeksiyonun kapiller endoteldeki biyobelirteci.", "highYieldBadge": "Humoral Rejeksiyon", "details": "Plazmaferez ve IVIG tedavisi gerektirir."}
        ],
        "flashcards": [
            {"id": "fc-hs-41", "front": "Böbrek nakli biyopsisinde peritübüler kapiller endotelinde C4d birikimi neyin göstergesidir?", "back": "Akut Antikor-Aracılı (Humoral) Rejeksiyonun göstergesidir.", "tag": "Transplantasyon", "masterLevel": "Kritik"},
            {"id": "fc-hs-42", "front": "Kronik böbrek greft reddinin en karakteristik vasküler histopatolojik lezyonu nedir?", "back": "Damar intimasında düz kas proliferasyonu ve hızlanmış greft arteriyosklerozudur.", "tag": "Histopatoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-21",
                "question": "Böbrek naklinden 3 hafta sonra serum kreatinini yükselen hastanın allogreft biyopsisinde kortikal tübül epiteli arasına CD8+ T lenfositlerinin sızdığı (tubulit) ve renal arteriyol intima tabakasında lenfositik enflamasyon (endotelit) izleniyor. Bu hastadaki rejeksiyon tipi aşağıdakilerden hangisidir?",
                "options": [
                    "A) Hiperakut rejeksiyon",
                    "B) Akut hücresel (T hücre-aracılı) rejeksiyon",
                    "C) Kronik intimal sklerozan rejeksiyon",
                    "D) Graft-versus-Host hastalığı",
                    "E) İlaç toksisitesine bağlı tübüler nekroz"
                ],
                "correctAnswer": "B",
                "explanation": "Nakilden haftalar sonra gelişen, interstisyel lenfosit infiltrasyonu, tübül epiteli arasına lenfosit sızması (tubulit) ve arteriyel intimal infiltrasyon (endotelit) Akut Hücresel Rejeksiyonun tanısal bulgularıdır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Transplantasyon öncesi yapılan Panel Reaktif Antikor (PRA) ve Cross-Match testlerinin mantığı nedir?",
            "Kronik rejeksiyonda düz kas migrasyonunu tetikleyen büyüme faktörleri (PDGF, FGF) nelerdir?"
        ]
    },

    # SLIDE 22
    {
        "slideNumber": 22,
        "title": "Kök Hücre Nakli ve Graft-versus-Host Hastalığı (GVHD)",
        "subtitle": "Donör T Hücrelerinin Alıcı Dokularına Saldırısı: Karaciğer, Cilt ve Bağırsak",
        "badge": "GVHD Patolojisi",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. GVHD'nin Doğası ve Billingham Kriterleri

Solid organ naklinde 'Alıcı grefti reddeder' (Host-versus-Graft). Ancak allojeneik hematopoetik kök hücre naklinde durum tam tersidir: 'Donör lenfositleri alıcıyı reddeder' (**Graft-versus-Host**).

GVHD gelişebilmesi için **üç şart (Billingham Kriterleri)** gereklidir:
1. Greft immünolojik olarak yetkin (fonksiyonel T hücreleri içeren) olmalıdır.
2. Alıcı dokuları donöre yabancı HLA antijenleri eksprese etmelidir.
3. Alıcının immün sistemi kemoradyoterapiyle baskılanmış olmalı ve donör hücrelerini reddedememelidir.

### 2. Akut GVHD ve Üç Kardinal Hedef Organı

Genellikle nakilden sonraki **ilk 100 gün içinde** ortaya çıkar:

```
+-----------------------------------------------------------------------------------+
|                        AKUT GVHD HEDEF ORGANLARI VE MORFOLOJİ                     |
+-----------------------------------------------------------------------------------+
| 1. DERİ TUTULUMU:                                                                 |
|    Boyun, avuç içi ve tabanlardan başlayan yaygın makülopapüler eritematöz        |
|    döküntü. Ağır olgularda toksik epidermal nekroliz benzeri bül ve dökülme.      |
|    Histoloji: Dermoepidermal bileşkede bazal vakuolizasyon ve keratinosit apoptozu.|
|                                                                                   |
| 2. KARACİĞER TUTULUMU:                                                            |
|    Küçük interlobüler safra kanallarına T lenfosit saldırısı.                     |
|    Safra kanalı epitel nekrozu ve kolestatik sarılık (direkt bilirubin artışı).   |
|                                                                                   |
| 3. GASTROİNTESTİNAL SİSTEM TUTULUMU:                                              |
|    Mukoza kript hücrelerinde yaygın apoptoz ve dökülme.                           |
|    Günde litrelerce süren inatçı sulu veya kanlı ishal, karın krampları, ileus.   |
+-----------------------------------------------------------------------------------+
```

### 3. Kronik GVHD ve Greft-versus-Lösemi (GVL) Etkisi

- **Kronik GVHD (>100 gün)**: Skleroderma benzeri yaygın cilt kalınlaşması, ekzokrin bez yıkımı (Sjögren sendromu benzeri kuru göz/ağız) ve akciğerde bronşiolitis obliterans.
- **Greft-versus-Lösemi (GVL) Etkisi**: Donör T hücrelerinin alıcı dokularına saldırması istenmeyen bir olayken; aynı donör T hücrelerinin alıcıdaki rezidüel lösemi klonlarını öldürmesi naklin en büyük başarısıdır.
""",
        "spotPearls": [
            "▸ **GVHD İçin Üç Şart (Billingham Kriterleri)**:\n  ▫ 1. Greft immünolojik olarak yetkin (fonksiyonel T hücreleri içeren) olmalıdır.\n  ▫ 2. Alıcı dokuları donöre yabancı HLA antijenleri taşımalıdır.\n  ▫ 3. Alıcı immün baskılanmış olmalı ve grefti reddedememelidir.",
            "🔴 ÖNEMLİ: Akut GVHD'nin Üç Hedef Organı:\n  ▫ **Cilt**: Dermoepidermal bileşkede bazal vakuolizasyon ve keratinosit apoptozu.\n  ▫ **Karaciğer**: Küçük intralobüler safra kanalı epitel nekrozu ve kolestaz.\n  ▫ **Bağırsak**: Mukoza kript hücrelerinde apoptoz ve kanlı diyare.",
            "🔵 ÇIKMIŞ SORU: *'Allojeneik kemik iliği naklinden 4 hafta sonra hastada yaygın eritematöz döküntü, sarılık ve kanlı ishal tablosunun gelişmesinden sorumlu patolojik mekanizma hangisidir?'*\n  ▫ Doğru yanıt: **Donör T lenfositlerinin alıcı dokularına saldırdığı Akut Graft-versus-Host Hastalığı (GVHD)**'dir."
        ],
        "coreContent": [
            {"title": "Billingham Kriterleri", "description": "GVHD gelişimi için gereken 3 temel immünolojik ön şart.", "highYieldBadge": "Kural", "details": "Donör T hücresi varlığı ve alıcının immün yetmezliği şarttır."},
            {"title": "Hedef Üçlü", "description": "Cilt (döküntü), Karaciğer (kolestatik sarılık), Bağırsak (kanlı ishal).", "highYieldBadge": "Klinik Triad", "details": "Her üç organda da epitel hücre apoptozu karakteristiktir."},
            {"title": "Greft-versus-Lösemi", "description": "Donör T hücrelerinin lösemik hücreleri yok etmesi.", "highYieldBadge": "Terapötik Etki", "details": "Allogeneik kök hücre naklinin kür sağlayan ana mekanizmasıdır."}
        ],
        "flashcards": [
            {"id": "fc-hs-43", "front": "Akut GVHD'de doku hasarının en karakteristik histopatolojik hücresel bulgusu nedir?", "back": "Hedef organ epitel hücrelerinin (keratinosit, safra kanalı, bağırsak kripti) tek tek apoptoza gitmesidir.", "tag": "Histopatoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-44", "front": "GVHD gelişiminde efektör rol oynayan hücre grubu hangisidir?", "back": "Greftteki (donörden gelen) olgun T lenfositleridir.", "tag": "İmmünoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-22",
                "question": "Akut miyeloid lösemi nedeniyle allojeneik kemik iliği nakli yapılan 35 yaşındaki erkek hastada, nakilden 25 gün sonra avuç içlerinden başlayan yaygın döküntü, hiperbilirubinemi (sarılık) ve günde 2 litreye varan sulu-kanlı ishal gelişiyor. Kolon biyopsisinde kript epitel hücrelerinde yaygın apoptoz izleniyor. Bu klinik tablonun primer sorumlusu aşağıdakilerden hangisidir?",
                "options": [
                    "A) Alıcının B lenfositlerince üretilen donör karşıtı antikorlar",
                    "B) Donör kök hücre greftindeki alloreaktif T lenfositleri",
                    "C) Sitomegalovirüs (CMV) süperenfeksiyonu",
                    "D) Yüksek doz kemoterapinin doğrudan mukozal toksisitesi",
                    "E) Mast hücrelerinin ani sistemik degranülasyonu"
                ],
                "correctAnswer": "B",
                "explanation": "Kemik iliği naklinden sonra cilt döküntüsü, kolestatik sarılık ve kanlı ishal ile seyreden tablo Akut GVHD'dir. Donör grefti içindeki olgun T lenfositlerinin alıcının HLA antijenlerine saldırması sonucu gelişir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kemik iliği greftinden T hücrelerinin temizlenmesi (T-cell depletion) GVHD ve lösemi nüksünü nasıl etkiler?",
            "Kronik GVHD ile sistemik sklerozun histopatolojik cilt benzerlikleri nelerdir?"
        ]
    },

    # SLIDE 23
    {
        "slideNumber": 23,
        "title": "Primer ve Sekonder İmmün Yetmezlikler: SCID, Bruton, DiGeorge ve HIV",
        "subtitle": "B Hücre, T Hücre ve Fagositik Defektler ile AIDS Patogenezi",
        "badge": "İmmün Yetmezlik",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. Primer (Kalıtsal) İmmün Yetmezlikler Atlası

1. **B Hücre Kusurları**:
   - **Bruton'un X'e Bağlı Agamaglobulinemisi (XLA)**: **BTK (Bruton Tirozin Kinaz)** mutasyonu; pre-B'den olgun B hücresine geçiş durur. Kanda CD19/CD20 B hücresi ve tüm immünoglobulinler YOKTUR. Lenf nodlarında germinal merkez bulunmaz. Maternal antikorların bittiği 6. aydan sonra kapsüllü bakterilerle (*S. pneumoniae*, *H. influenzae*) tekrarlayan sinopulmoner enfeksiyonlar başlar.
   - **İzole IgA Eksikliği**: En sık görülen primer immün yetmezliktir (1/600). Çoğu asemptomatiktir; mukozal enfeksiyonlar ve kan transfüzyonunda anti-IgA antikorlarına bağlı **anafilaksi riski** vardır!
2. **T Hücre ve Kombine Kusurlar**:
   - **SCID (Ağır Kombine İmmün Yetmezlik)**: Hem hücresel hem humoral immünite çökmüştür. En sık tipi X'e bağlı **IL-2R gama zincir mutasyonu**; otozomal resesif formu **Adenozin Deaminaz (ADA) eksikliği** (toksik metabolit birikimi). Timus hipoplaziktir.
   - **DiGeorge Sendromu**: 22q11.2 mikrodelesyonu; 3. ve 4. faringeal cep gelişim kusuru. **Timus aplazisi** (T hücresi yok), **Paratiroid aplazisi** (hipokalsemik tetani) ve konotrunkal kalp anomalileri.
3. **Fagositik Sistem Kusurları**:
   - **Lökosit Adhezyon Defekti-1 (LAD-1)**: **CD18 (beta-2 integrin)** defekti. Lökositler endotelden dokuya çıkamaz. Kanda aşırı nötrofili vardır ama **enfeksiyon alanında iltihap (püy) oluşamaz!** Göbek kordonu düşmesi gecikir.
   - **Kronik Granülomatöz Hastalık (CGD)**: **NADPH Oksidaz** defekti; solunumsal patlama yapılamaz ($H_2O_2$ üretilemez). **NBT (Nitroblue tetrazolium) testi negatiftir**. Katalaz-pozitif mikroorganizmalarla (*S. aureus*, *Aspergillus*) granülomatöz enfeksiyonlar gelişir.

### 2. Sekonder İmmün Yetmezlik: HIV / AIDS

- Dünyada en sık immün yetmezlik nedeni malnütrisyondur; en ölümcül sekonder immün yetmezlik ise AIDS'tir.
- **HIV Bulaşı ve Girişi**: Viral yüzey glikoproteini **gp120**, CD4 molekülüne ve kemokin koreseptörlerine (**CCR5** veya **CXCR4**) bağlanır. **gp41** virüs membranını konak zarına kaynaştırır (füzyon).
- **AIDS Tanımı**: CD4+ T lenfosit sayısının **< 200 / $\mu$L** altına düşmesi veya AIDS tanımlayıcı fırsatçı enfeksiyonların (*Pneumocystis jirovecii*, CMV retiniti, Kriptokok menenjiti, Kaposi Sarkomu - HHV-8) ortaya çıkmasıdır.
""",
        "spotPearls": [
            "▸ **B Hücre Defektleri vs. T Hücre Defektleri**:\n  ▫ B hücre defektlerinde (Bruton): Kapsüllü bakterilerle (*S. pneumoniae*, *H. influenzae*) tekrarlayan sinopulmoner enfeksiyonlar görülür.\n  ▫ T hücre defektlerinde (DiGeorge, SCID): Fırsatçı mantarlar (*Candida*, *Pneumocystis*) ve intraselüler virüslerle erken başlangıçlı ağır enfeksiyonlar görülür.",
            "🔴 ÖNEMLİ: LAD-1 ve CGD Klinik Ayrımı:\n  ▫ **LAD-1 (Lökosit Adhezyon Defekti)**: CD18/integrin eksikliği; göbek bağı düşmesinde gecikme, lökositoz eşliğinde dokuda PÜY/İLTİHAP OLUŞMAMASI ile karakterizedir.\n  ▫ **CGD (Kronik Granülomatöz Hastalık)**: NADPH oksidaz defekti; nötrofiller mikrobu fagosite eder ama öldüremez; katalaz-pozitif bakterilerle tekrarlayan granülomlar oluşur.",
            "🔵 ÇIKMIŞ SORU: *'Erkek bebekte 6. aydan sonra tekrarlayan otit ve pnömoni öyküsü; kanda CD19+ B hücresi ve serum immünoglobulinlerinin saptanmaması, lenf nodu biyopsisinde germinal merkezlerin bulunmaması durumunda tanınız nedir?'*\n  ▫ Doğru yanıt: **Bruton'un X'e Bağlı Agamaglobulinemisi (XLA)**'dir."
        ],
        "coreContent": [
            {"title": "Bruton Agamaglobulinemisi", "description": "BTK mutasyonu nedeniyle pre-B hücresi olgun B'ye dönüşemez.", "highYieldBadge": "B Hücre Yokluğu", "details": "Kanda B hücresi ve antikor yoktur; T hücre sayısı tamamen normaldir."},
            {"title": "LAD-1 Defekti", "description": "CD18 eksikliği; nötrofillerin dokuya çıkamaması ve püy oluşamaması.", "highYieldBadge": "İntegrin Defekti", "details": "Göbek kordonunun 2 haftadan geç düşmesi klasik ipucudur."},
            {"title": "HIV Giriş Mekanizması", "description": "gp120 (CD4 ve CCR5/CXCR4 tutunması) ve gp41 (membran füzyonu).", "highYieldBadge": "Viroloji", "details": "CCR5 delta-32 homozigot bireyler HIV enfeksiyonuna dirençlidir."}
        ],
        "flashcards": [
            {"id": "fc-hs-45", "front": "Bruton agamaglobulinemisinde mutasyona uğrayan enzim ve duraklayan gelişim evresi nedir?", "back": "Bruton Tirozin Kinaz (BTK); pre-B hücresinden olgun B hücresine geçiş duraklar.", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-hs-46", "front": "Kronik granülomatöz hastalıkta (CGD) defektif olan enzim sistemi hangisidir?", "back": "Fagositik NADPH Oksidaz enzim kompleksi.", "tag": "Biyokimya", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-23",
                "question": "Doğumdan sonra göbek kordonu 4. haftada düşen, tekrarlayan nekrotizan deri enfeksiyonları geçiren bir bebekte kanda aşırı nötrofili (55.000/μL) saptanmasına rağmen, deri enfeksiyon alanında hiç püy (cerahat) oluşmadığı görülüyor. Bu hastadaki moleküler defekt aşağıdakilerden hangisidir?",
                "options": [
                    "A) NADPH oksidaz enzim eksikliği",
                    "B) CD18 (beta-2 integrin) lökosit adhezyon molekül eksikliği",
                    "C) Bruton tirozin kinaz mutasyonu",
                    "D) Adenozin deaminaz (ADA) enzim yokluğu",
                    "E) CD40 ligand (CD154) eksikliği"
                ],
                "correctAnswer": "B",
                "explanation": "Göbek kordonunun geç düşmesi, belirgin kanda lökositoz olmasına rağmen enfeksiyon bölgesine lökositlerin geçememesi ve püy oluşmaması Lökosit Adhezyon Defekti Tip 1 (LAD-1; CD18 integrin eksikliği) için patognomoniktir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Katalaz-pozitif bakterilerin CGD hastalarında enfeksiyon yapabilmesinin biyokimyasal temeli nedir?",
            "DiGeorge sendromunun CATCH-22 klinik akroniminin açılımı nasıldır?"
        ]
    },

    # SLIDE 24
    {
        "slideNumber": 24,
        "title": "Amiloidoz: Fibril Biyolojisi, Tipleri ve Klinikopatoloji",
        "subtitle": "Beta-Kırmalı Tabaka, Kongo Kırmızısı Çift Kırılma, AL, AA ve ATTR",
        "badge": "Amiloidoz",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Amiloidozun Doğası ve Biyofiziksel Özellikleri

Amiloidoz; çeşitli patogenetik mekanizmalarla yanlış katlanmış, proteolize dirençli, çözünmeyen fibriler proteinlerin **hücrelerarası (ekstrasellüler) doku alanlarında birikerek** organlarda bası atrofisine ve fonksiyon kaybına yol açtığı heterojen hastalık grubudur.

- **Elektron Mikroskopi**: 7.5 ila 10 nm çapında, dallanma göstermeyen, düz lineer fibriller.
- **X-Işını Kırınımı**: Kökeni ne olursa olsun tüm amiloid fibrilleri karakteristik **Çapraz Beta-Kırmalı Tabaka (Cross-Beta-Pleated Sheet)** yapısındadır. Bu yapı amiloidin proteolitik enzimlerle eritilmesini engeller.
- **Histopatoloji**: H&E boyasında hücre dışı alanda amorf, eozinofilik, homojen, camsı pembe madde birikimi.
- **Altın Standart Tanı**: Kesitin **Kongo Kırmızısı (Congo Red)** ile boyanıp **polarize ışık mikroskobunda incelenmesiyle ELMA YEŞİLİ ÇİFT KIRILMA (Apple-Green Birefringence)** vermesidir!

### 2. Başlıca Klinikopatolojik Amiloid Tipleri

| Amiloid Tipi | Öncül Protein | Klinik İlişki ve Tutulum |
| :--- | :--- | :--- |
| **AL (Primer)** | İmmünoglobulin **Hafif Zincirleri** (özellikle $\lambda$) | **Multipl Miyelom** ve monoklonal plazma hücre diskrazileri. Kalp (restriktif kardiyomiyopati), dil (makroglossi) ve böbrek tutulumu. |
| **AA (Sekonder / Reaktif)** | **Serum Amiloid A (SAA)** (Karaciğerde IL-6/IL-1 ile sentezlenir) | **Kronik Enflamatuar Hastalıklar**: Romatoid Artrit, Bronşiektazi, Osteomiyelit, Ailevi Akdeniz Ateşi (**FMF** - pirin geni). En sık **Böbrek** tutulur (masif nefrotik proteinüri). |
| **ATTR (Transtiretin)** | Transtiretin (Tiroksin ve retinol taşıyıcı) | 1. **Mutant ATTR**: Ailesel Amiloid Polinöropati.<br>2. **Wild-Type ATTR**: **Senil Kardiyak Amiloidoz** (80+ yaş erkeklerde kalp yetmezliği). |
| **Aβ** | Amiloid Prekürsör Protein (APP) | **Alzheimer Hastalığı**nda serebral amiloid anjiyopati ve senil plaklar. |
| **Aβ2m** | Beta-2 Mikroglobulin (MHC Sınıf I hafif zinciri) | **Uzun Süreli Hemodiyaliz** hastalarında diyaliz membranından süzülemez; sinovya ve ligamanlarda birikir (**Karpal Tünel Sendromu**). |

### 3. Tanısal Biyopsi Yerleri

Sistemik amiloidoz şüphesinde invaziv organ biyopsisi yerine ilk tercih edilen, komplikasyonsuz ve duyarlılığı %80'in üzerinde olan yöntem **Karın Cilt Altı Yağ Dokusu Aspirasyon Biyopsisidir (Abdominal Fat Pad Aspirasyonu)**. Alternatif olarak rektum veya diş eti biyopsisi yapılabilir.
""",
        "spotPearls": [
            "▸ **Amiloidozun Biyofiziksel İmzası**: Amiloid öncül proteini ne olursa olsun, biriken tüm amiloid tipleri ortak **çapraz beta-kırmalı tabaka** yapısı kazanır; bu yapı proteolitik enzimlere karşı olağanüstü direnç sağlar.",
            "🔴 ÖNEMLİ: Kongo Kırmızısı ve Polarize Mikroskopi Şartı:\n  ▫ Işık mikroskobunda amiloid pembe renkte boyanır, ancak bu tanı için KESİNLİKLE yeterli değildir.\n  ▫ Kesin tanı: **Kongo Kırmızısı ile boyanan kesitin polarize ışık altında incelenerek ELMA YEŞİLİ ÇİFT KIRILMA (Apple-green birefringence)** göstermesidir!",
            "🔵 ÇIKMIŞ SORU: *'Uzun süredir romatoid artrit veya Ailevi Akdeniz Ateşi (FMF) tanısıyla takip edilen bir hastada masif proteinüri ve nefrotik sendrom geliştiğinde böbrek biyopsisinde saptanması beklenen amiloid tipi hangisidir?'*\n  ▫ Doğru yanıt: **AA Amiloidoz (Sekonder/Reaktif amiloidoz; Serum Amiloid A kökenli)**'dur."
        ],
        "coreContent": [
            {"title": "Kongo Kırmızısı ve Çift Kırılma", "description": "Polarize mikroskopta elma yeşili çift kırılma amiloidoz için patognomoniktir.", "highYieldBadge": "Altın Standart", "details": "Çapraz beta-kırmalı tabakanın optik özelliğidir."},
            {"title": "AL Amiloidoz", "description": "Monoklonal plazma hücreleri kaynaklı immünoglobulin hafif zincir birikimi.", "highYieldBadge": "Primer Tip", "details": "Multipl miyelom ve kardiyak tutulumla birliktedir."},
            {"title": "AA Amiloidoz", "description": "Kronik enflamasyonda karaciğerden salınan SAA proteininin proteolitik ürünü.", "highYieldBadge": "Reaktif Tip", "details": "FMF ve romatoid artritte nefrotik sendromun baş nedenidir."}
        ],
        "flashcards": [
            {"id": "fc-hs-47", "front": "Amiloidoz tanısında Kongo Kırmızısı boyası polarize mikroskopta ne renk çift kırılma verir?", "back": "Elma yeşili çift kırılma (apple-green birefringence).", "tag": "Histopatoloji", "masterLevel": "Kritik"},
            {"id": "fc-hs-48", "front": "Hemodiyaliz hastalarında karpal tünel sendromuna yol açan biriken amiloid proteini hangisidir?", "back": "Aβ2m (Beta-2 mikroglobulin).", "tag": "Nefroloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-hs-24",
                "question": "15 yıldır Ailevi Akdeniz Ateşi (FMF) nedeniyle takip edilen ve ataklarını düzensiz geçiren 38 yaşındaki hastada pretibial ödem ve 6 g/gün proteinüri ile nefrotik sendrom gelişiyor. Yapılan böbrek biyopsisinde glomerüllerde biriken maddenin Kongo kırmızısı ile elma yeşili çift kırılma verdiği saptanıyor. Bu hastada biriken amiloidin öncül proteini aşağıdakilerden hangisidir?",
                "options": [
                    "A) İmmünoglobulin lambda hafif zinciri",
                    "B) Transtiretin",
                    "C) Serum Amiloid A (SAA)",
                    "D) Beta-2 mikroglobulin",
                    "E) Amiloid Prekürsör Protein (APP)"
                ],
                "correctAnswer": "C",
                "explanation": "FMF, Romatoid Artrit veya kronik osteomiyelit gibi uzun süren kronik enflamatuar durumlarda gelişen sekonder amiloidoz AA tipindedir ve karaciğerden salınan Serum Amiloid A (SAA) proteininin birikmesiyle oluşur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Dalakta sago dalağı (beyaz pulpa) ve lardaseous dalak (kırmızı pulpa) amiloidoz paternleri nasıldır?",
            "Wild-type transtiretin ile mutant transtiretin kardiyak tutulum farkı ve Tafamidis ilacının mekanizması nedir?"
        ]
    }
]

print(f"Constructed all {len(slides)} slides with 100% detail!")

# Create Deck Object
new_deck = {
    "id": DECK_ID,
    "title": DECK_TITLE,
    "shortTitle": SHORT_TITLE,
    "discipline": DISCIPLINE,
    "committee": COMMITTEE,
    "instructor": INSTRUCTOR,
    "audioFile": None,
    "audioDuration": None,
    "confidence": 99,
    "themeColor": THEME_COLOR,
    "matchedNoteId": MATCHED_NOTE_ID,
    "matchedNoteTitle": MATCHED_NOTE_TITLE,
    "overview": OVERVIEW,
    "highYieldPearls": HIGH_YIELD_PEARLS,
    "slides": slides,
    "totalSlides": len(slides),
    "matchedPastQuestionsCount": 24
}

# Update interactive_learning_decks.json
decks_path = "src/data/interactive_learning_decks.json"
with open(decks_path, "r", encoding="utf-8") as f:
    decks = json.load(f)

# Check if exists and replace or append
existing_idx = next((i for i, d in enumerate(decks) if d["id"] == DECK_ID), None)
if existing_idx is not None:
    print(f"Updating existing deck at index {existing_idx}...")
    decks[existing_idx] = new_deck
else:
    print("Appending new deck to interactive_learning_decks.json...")
    decks.append(new_deck)

with open(decks_path, "w", encoding="utf-8") as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)
print("interactive_learning_decks.json successfully updated! Total decks now:", len(decks))

# Collect all practice questions from the new deck
new_questions = []
for s in slides:
    for q in s.get("relatedQuestions", []):
        q_copy = dict(q)
        q_copy["deckId"] = DECK_ID
        q_copy["slideNumber"] = s["slideNumber"]
        q_copy["discipline"] = DISCIPLINE
        q_copy["committee"] = COMMITTEE
        new_questions.append(q_copy)

print(f"Collected {len(new_questions)} practice questions from the new deck.")

# Append to chunked study questions database
study_dir = "src/data/study_questions"
chunk_7_path = os.path.join(study_dir, "chunk_7.json")
with open(chunk_7_path, "r", encoding="utf-8") as f:
    chunk_7 = json.load(f)

print(f"chunk_7.json currently has {len(chunk_7)} questions.")
# Filter out any old questions for this deck if existing
chunk_7 = [q for q in chunk_7 if q.get("deckId") != DECK_ID]
chunk_7.extend(new_questions)
print(f"chunk_7.json now has {len(chunk_7)} questions.")

with open(chunk_7_path, "w", encoding="utf-8") as f:
    json.dump(chunk_7, f, ensure_ascii=False, indent=2)

# Update index.json
index_path = os.path.join(study_dir, "index.json")
with open(index_path, "r", encoding="utf-8") as f:
    index_data = json.load(f)

# Recalculate totals
total_q = 0
for ch in index_data["chunks"]:
    ch_path = os.path.join(study_dir, ch["filename"])
    if os.path.exists(ch_path):
        with open(ch_path, "r", encoding="utf-8") as f:
            data_q = json.load(f)
            ch["questionCount"] = len(data_q)
            if ch["chunkId"] == "chunk_7":
                if DECK_ID not in ch["decksCovered"]:
                    ch["decksCovered"].append(DECK_ID)
            total_q += len(data_q)

index_data["totalQuestions"] = total_q
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

print(f"study_questions/index.json updated! Total questions across chunks: {total_q}")

# Update learning_batch_queue.json
queue_path = "src/data/learning_batch_queue.json"
with open(queue_path, "r", encoding="utf-8") as f:
    queue = json.load(f)

for item in queue:
    if item["id"] == DECK_ID:
        item["status"] = "completed"
        item["slidesCount"] = len(slides)
        item["detailLevel"] = "500%"

# Check if next item exists, if not, add next from Kurul 1: 'learn-tromboz-patofizyolojisi' or 'learn-genetik-pediatrik-patoloji'
has_next = any(item.get("status") == "next_in_queue" for item in queue)
if not has_next:
    # Add next Kurul 1 lecture: "15)Genetik,pediatrik ve çevresel patoloji.txt"
    queue.append({
        "id": "learn-genetik-pediatrik-cevresel-patoloji",
        "title": "Genetik, Pediatrik ve Çevresel Hastalıklar Patolojisi",
        "discipline": "Tıbbi Patoloji",
        "status": "next_in_queue",
        "slidesCount": 24,
        "detailLevel": "500% (Planlanan)"
    })

with open(queue_path, "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)
print("learning_batch_queue.json updated! Deck marked completed.")
