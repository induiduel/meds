# -*- coding: utf-8 -*-
"""
complete_genetics_pediatric_deck.py
Completes slides 13 to 24 for 'learn-genetik-pediatrik-cevresel-patoloji',
adds encyclopedia and glossary terms, and handles chunked study questions.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_ID = "learn-genetik-pediatrik-cevresel-patoloji"
DECK_TITLE = "Genetik, Pediatrik ve Çevresel Hastalıklar Patolojisi"
SHORT_TITLE = "Genetik & Çevresel Patoloji"
DISCIPLINE = "Tıbbi Patoloji"
COMMITTEE = "Dönem 3 Kurul 1"
INSTRUCTOR = "Prof. Dr. Hikmet Keleş"
THEME_COLOR = "emerald"
MATCHED_NOTE_ID = "kurul1-patoloji-15"
MATCHED_NOTE_TITLE = "15) Genetik, pediatrik ve çevresel patoloji"

OVERVIEW = (
    "Prof. Dr. Hikmet Keleş ve Robbins Temel Patoloji (11. Baskı) kılavuzluğunda hazırlanmış; "
    "insan genom varyasyonlarını (SNP, CNV, Epigenetik), Mendel tipi kalıtımı (Marfan sendromu/FBN1, Kistik Fibrozis/CFTR), "
    "sitogenetik bozuklukları (Down Sendromu/Trizomi 21), çevresel hava kirliliği ve ağır metal toksisitesini (Kurşun, Karbonmonoksit), "
    "tütün ve alkol metabolizmasını (CYP2E1, Mallory-Denk cisimcikleri), şiddetli akut malnütrisyonu (Marasmus vs. Kwashiorkor), "
    "yeme bozukluklarını (Anoreksiya, Bulimia), obezite moleküler aksını (Leptin, Adiponektin) ve modern moleküler tanı araçlarını "
    "(FISH, NGS) %500 derinlikte inceleyen kapsamlı eğitim modülü."
)

HIGH_YIELD_PEARLS = [
    "Marfan: FBN1 gen mutasyonu, fibrillin-1 defekti, serbest TGF-β aşırı aktivasyonu; aort kökü kistik medyal nekrozu, aort diseksiyonu, ektopia lentis (yukarı-dışa).",
    "Kistik Fibrozis: CFTR gen mutasyonu (en sık delta-F508); solunum ve bağırsakta klor atılamaz, sodyum ve su çekilir (koyu mukus, bronşiektazi); ter bezinde klor emilemez (ter testi altın standart).",
    "Down Sendromu: %95 maternal mayotik non-disjunction; epikantus, simian çizgisi, endokardiyal yastık defekti, duodenal atrezi, lösemi (ALL ve megakaryoblastik AML), erken Alzheimer (APP geni 21. kromozomda).",
    "Kurşun: ALA dehidrataz ve ferroşelataz inhibisyonu; mikrositer anemi, eritrositlerde bazofilik noktalanma, epifiz kurşun hatları, diş etinde Burton çizgisi.",
    "Alkol: Alkol dehidrogenaz ve CYP2E1 (MEOS); aşırı NADH/NAD+; steatoz, Mallory-Denk cisimcikleri (sitokeratin yığılması), perivenüler fibrozis ve siroz.",
    "Malnütrisyon: Marasmus = Kalori eksikliği, somatik kas erimesi, ödem YOKTUR; Kwashiorkor = Protein yoksunluğu, visseral protein kaybı, hipoalbüminemi, masif ödem, yağlı karaciğer, flaky-paint dermatiti.",
    "Obezite: Adiposit kaynaklı Leptin hipotalamusu uyararak tokluk sağlar (obezitede leptin direnci); Adiponektin insülin duyarlılaştırıcıdır ve obezitede DÜŞER.",
    "Moleküler Patoloji: NGS (Yeni Nesil Dizileme) aynı anda yüzlerce geni multigen panelleriyle tarar; hedefe yönelik onkolojik tedavilerin (EGFR, ALK, BRAF) temelidir."
]

# We will import the first 12 slides from generate_genetics_pediatric_complete.py
from generate_genetics_pediatric_complete import slides as first_12_slides

slides_13_to_24 = [
    # SLIDE 13
    {
        "slideNumber": 13,
        "title": "Ağır Metal Toksisitesi: Kurşun Patolojisi ve İntoksikasyonu",
        "subtitle": "ALA Dehidrataz ve Ferroşelataz İnhibisyonu, Bazofilik Noktalanma ve Burton Çizgisi",
        "badge": "Kurşun Toksisitesi",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Kurşun Maruziyeti ve Emilim Yolları

Kurşun ($Pb$), çevrede yaygın olarak bulunan, özellikle çocuklarda sinir sistemi ve kan yapımı üzerinde yıkıcı etkiler bırakan ağır bir metaldir.
- **Kaynaklar**: Eski binalardaki kurşunlu boyalar (çocukların dökülen boyaları yemesi / pika), kurşun borulu su tesisatları, akü fabrikaları, madencilik ve kurşunlu lehimler.
- **Çocukların Hassasiyeti**: Çocuklar yutulan kurşunun **%50'sini** emerken (erişkinlerde bu oran %10'dur); ayrıca kan-beyin bariyeri tam gelişmediği için santral sinir sistemi toksisitesine katbekat daha açıktır.

### 2. Patofizyolojik Mekanizmalar

1. **Hem Sentezinin Felç Edilmesi (Anemi)**:
   - Kurşun, sülfhidril (–SH) gruplarına bağlanarak iki kritik enzimi doğrudan inhibe eder:
     - **Delta-Aminolevülinik Asit Dehidrataz ($\delta$-ALAD)**: Kanda ALA birikir.
     - **Ferroşelataz**: Protoporfirine demir ($Fe^{2+}$) takılamaz; serbest **Çinko Protoporfirin (ZPP)** kanda fırlar!
   - Sonuç: **Mikrositer hipokrom anemi**.
2. **Eritrositlerde Bazofilik Noktalanma (Basophilic Stippling)**:
   - Kurşun, ribozomal RNA'yı parçalayan **pirimidin 5'-nükleotidaz** enzimini inhibe eder. Eritrosit sitoplazmasında kümeleşen ribozomlar periferik yaymada ince noktasal mavi tanecikler (**Bazofilik Noktalanma**) olarak görünür!
3. **Kemik Dokusu ve 'Kurşun Hatları' (Lead Lines)**:
   - Kurşunun %80-85'i kemik ve dişlerde kalsiyum ile yarışarak birikir. Çocuklarda uzun kemiklerin epifiz büyüme plaklarında radyolojide belirgin radyoopak **Kurşun Hatları (Lead Lines)** izlenir.
4. **Diş Etinde Burton Çizgisi**:
   - Diş eti kenarında kurşunun bakteriyel hidrojen sülfürle birleşmesiyle koyu mavi-mor **Burton Çizgisi (Lead Line)** oluşur.
5. **Santral Sinir Sistemi**:
   - Çocuklarda ensefalopati, beyin ödemi, nöbetler ve zeka puanında (IQ) geri dönüşsüz düşüş.
""",
        "spotPearls": [
            "▸ Kurşun hem sentezinde **$\delta$-ALA dehidrataz** ve **Ferroşelataz** enzimlerini inhibe ederek mikrositer anemi ve serumda **Çinko Protoporfirin (ZPP)** artışı yapar.",
            "🔴 ÖNEMLİ: Periferik yaymada eritrositlerde **Bazofilik Noktalanma (Basophilic Stippling)** kurşun zehirlenmesinin klasik morfolojik kanıtıdır (pirimidin 5'-nükleotidaz inhibisyonu kaynaklıdır).",
            "🔵 ÇIKMIŞ SORU: *'Çocukta uzun kemik epifizlerinde radyoopak çizgilenme, diş etinde mavi çizgi (Burton) ve karın ağrısı ile seyreden ağır metal zehirlenmesi hangisidir?'*\n  ▫ Doğru yanıt: **Kurşun ($Pb$) İntoksikasyonu**'dur."
        ],
        "coreContent": [
            {"title": "Hem Sentez İnhibisyonu", "description": "ALA dehidrataz ve ferroşelataz enzimlerinin bloke olması.", "highYieldBadge": "Biyokimyasal Toksisite", "details": "Kanda serbest eritrosit protoporfirini ve ZPP yükselir."},
            {"title": "Bazofilik Noktalanma", "description": "Parçalanamayan ribozomların eritrosit içinde mavi noktalar oluşturması.", "highYieldBadge": "Hematoloji", "details": "Pirimidin 5'-nükleotidaz enzim inaktivasyonuna bağlıdır."},
            {"title": "Burton Çizgisi ve Epifiz", "description": "Diş etinde kurşun sülfür birikimi ve röntgende epifiz radyoopasiteleri.", "highYieldBadge": "Klinik Bulgu", "details": "Çocukluk çağı kurşun zehirlenmesinde patognomoniktir."}
        ],
        "flashcards": [
            {"id": "fc-gp-25", "front": "Kurşun zehirlenmesinde eritrositlerde görülen 'bazofilik noktalanmanın' hücresel nedeni nedir?", "back": "Pirimidin 5'-nükleotidaz enziminin inhibisyonu sonucu rRNA kalıntılarının eritrosit sitoplazmasında kümelenmesidir.", "tag": "Hematoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-26", "front": "Kurşun hem sentez yolunda hangi iki temel enzimi inhibe eder?", "back": "Delta-aminolevülinik asit (ALA) dehidrataz ve Ferroşelataz.", "tag": "Biyokimya", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-13",
                "question": "Eski boyalı bir evde yaşayan, karın ağrısı ve dikkat dağınıklığı şikayetiyle getirilen 4 yaşındaki çocuğun kan sayımında mikrositer anemi saptanıyor. Periferik yaymasında eritrositler içinde yaygın bazofilik noktalanma (basophilic stippling) izlenen bu çocukta patolojiden sorumlu ağır metal ve inhibe olan enzim ikilisi hangisidir?",
                "options": [
                    "A) Cıva - Üroporfirinojen dekarboksilaz",
                    "B) Kurşun - Delta-aminolevülinik asit (ALA) dehidrataz",
                    "C) Arsenik - Tirozinaz",
                    "D) Kadmiyum - Ksantin oksidaz",
                    "E) Demir - Glukoz-6-fosfat dehidrogenaz"
                ],
                "correctAnswer": "B",
                "explanation": "Kurşun intoksikasyonunda ALA dehidrataz ve ferroşelataz enzimleri inhibe olur; kanda serbest protoporfirin artar ve periferik yaymada ribozomal agregatlara bağlı bazofilik noktalanma tipiktir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kurşun zehirlenmesinde şelasyon tedavisinde kullanılan ajanlar (EDTA, Dimerkaprol, DMSA) nasıl çalışır?",
            "Erişkin kurşun toksisitesinde izlenen periferik nöropatinin (düşük el/radial sinir hasarı) mekanizması nedir?"
        ]
    },

    # SLIDE 14
    {
        "slideNumber": 14,
        "title": "Ağır Metal Toksisitesi: Cıva, Arsenik ve Kadmiyum Patolojileri",
        "subtitle": "Minamata Hastalığı, Arsenik Keratozu/Anjiyosarkom ve İtai-İtai Kadmiyum Osteomalazisi",
        "badge": "Ağır Metaller",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Cıva ($Hg$) Toksisitesi ve Minamata Hastalığı

- **Kaynak**: Kirli sulardaki inorganik cıva bakteriler tarafından **Metil Cıva**ya (organik) dönüştürülür ve besin zincirinde (büyük yırtıcı balıklar: ton balığı, kılıç balığı) birikir.
- **Minamata Hastalığı**: Japonya'da Minamata Körfezi'ndeki kimyasal atık balıkları yiyen gebe kadınların bebeklerinde mikrosefali, serebral palsi, sağırlık, körlük ve ağır mental retardasyonla doğmasıyla tanımlanmıştır.
- **Histopatoloji**: Gelişmekte olan fetal beyinde serebral korteks atrofisi ve serebellar **Purkinje ve granül hücre katmanlarında yaygın nöronal kayıp**.

### 2. Arsenik ($As$) Toksisitesi ve Karsinojenez

- **Kaynak**: Kömür yakıtları, tarım ilaçları ve arsenikle kirlenmiş derin kuyu suları (Bangladeş, Hindistan).
- **Mekanizma**: Mitokondriyal ATP sentezini bozar ve DNA onarım enzimlerini inhibe eder.
- **Klinik Bulgular**:
  - Cilt: Avuç içi ve ayak tabanlarında hiperkeratoz (**Arsenik Keratozu**), deride 'çiseleyen yağmur damlaları' tarzında hiperpigmentasyon.
  - Tırnaklarda transvers beyaz çizgiler (**Mees Çizgileri**).
  - Malignite Riski: **Cilt kanserleri (skuamöz hücreli karsinom)**, akciğer kanseri ve karaciğerde nadir görülen **Hepatik Anjiyosarkom**!

### 3. Kadmiyum ($Cd$) ve İtai-İtai Hastalığı

- **Kaynak**: Piller, aküler, madencilik atıklarıyla kirlenmiş pirinç tarlaları.
- **Hedef Organlar**:
  - **Böbrekler**: Proksimal tübül epitel nekrozu ve Fanconi sendromu benzeri proteinüri/kalsiüri.
  - **Kemikler**: Kalsiyum kaybı sonucu ağır osteomalazi ve patolojik kemik kırıkları (**İtai-İtai / Ah-Ah Hastalığı**).
  - **Akciğer**: İnflamasyon, obstrüktif akciğer hastalığı ve akciğer kanseri.
""",
        "spotPearls": [
            "▸ Fetal beyinde Purkinje hücresi kaybı, serebral palsi ve sağırlıkla karakterize organik metil cıva zehirlenmesine **Minamata Hastalığı** denir.",
            "🔴 ÖNEMLİ: Arsenik zehirlenmesi avuç içinde hiperkeratoz, cilt kanseri ve karaciğerde ölümcül **Hepatik Anjiyosarkom** gelişimine yol açar.",
            "🔵 ÇIKMIŞ SORU: Kadmiyum kirliliğine bağlı proksimal böbrek tübüler hasarı ve şiddetli ağrılı osteomalazi/kemik kırıkları ile seyreden tablo **İtai-İtai Hastalığı**dır."
        ],
        "coreContent": [
            {"title": "Minamata Cıva Toksisitesi", "description": "Metil cıvanın plasentayı geçerek fetal serebral ve serebellar nöronları yok etmesi.", "highYieldBadge": "Nörotoksisite", "details": "Büyük dip balıkları tüketiminde cıva riski yüksektir."},
            {"title": "Arsenik ve Anjiyosarkom", "description": "Kronik arsenik maruziyetinin karaciğer endotelinde malignite tetiklemesi.", "highYieldBadge": "Karsinojenez", "details": "Vinil klorür ve torotrast ile birlikte anjiyosarkomun 3 klasik nedenindendir."},
            {"title": "İtai-İtai (Kadmiyum)", "description": "Kadmiyumun renal kalsiyum atılımını artırarak osteomalazi yapması.", "highYieldBadge": "Kemik/Böbrek", "details": "Japonya'da kirlenmiş pirinç tüketimiyle salgın yapmıştır."}
        ],
        "flashcards": [
            {"id": "fc-gp-27", "front": "Metil cıva zehirlenmesinde beyincikte spesifik olarak nekroza uğrayan nöron grubu hangisidir?", "back": "Purkinje hücreleri ve granül hücre tabakası.", "tag": "Nöropatoloji", "masterLevel": "Yüksek"},
            {"id": "fc-gp-28", "front": "Karaciğer anjiyosarkomuna yol açan çevresel ağır metal ve kimyasal karsinojenler nelerdir?", "back": "Arsenik, Vinil Klorür ve Torotrast.", "tag": "Onkopatoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-14",
                "question": "Yıllarca kuyu suyu içen bir hastada avuç içlerinde hiperkeratotik plaklar, tırnaklarda beyaz çizgilenmeler (Mees çizgileri) ve ciltte skuamöz hücreli karsinom gelişiyor. Karaciğer ultrasonunda kitle saptanan hastanın biyopsisinde hepatik anjiyosarkom tanısı konuyor. Bu tabloya yol açan en muhtemel çevresel toksin hangisidir?",
                "options": [
                    "A) Kurşun",
                    "B) Arsenik",
                    "C) Kadmiyum",
                    "D) Cıva",
                    "E) Berilyum"
                ],
                "correctAnswer": "B",
                "explanation": "Palmar hiperkeratoz, Mees çizgileri, kutanöz skuamöz hücreli karsinom ve karaciğerde anjiyosarkom birlikteliği kronik Arsenik maruziyetinin klasik klinikopatolojik spektrumudur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Vinil klorür ile arseniğin karaciğer anjiyosarkomu patogenezindeki endotelial mutasyon farkları nelerdir?",
            "Kadmiyum toksisitesinde metallotionein proteininin koruyucu rolü nasıl çalışır?"
        ]
    },

    # SLIDE 15
    {
        "slideNumber": 15,
        "title": "Tütün Dumanı ve Karsinojenez / Vaskülopati Patolojisi",
        "subtitle": "Nikotin Bağımlılığı, Katran Karsinojenleri (PAH, Nitrozaminler), KOAH ve Ateroskleroz",
        "badge": "Tütün Patolojisi",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Tütün: Önlenebilir En Büyük Ölüm Nedeni

Tütün kullanımı, dünyada her yıl 8 milyondan fazla insanın ölümüne yol açan, önlenebilir küresel bir numaralı mortalite nedenidir.

### 2. Tütün Dumanının Toksik ve Karsinojenik Bileşenleri

Tütün dumanında 4000'den fazla kimyasal madde bulunur; bunların en az 70'i kanıtlanmış karsinojendir:
- **Nikotin**: Bağımlılığı yapan ana alkaloiddir; doğrudan karsinojen değildir. Beyinde nAChR'leri uyararak dopamin salgılatır; sempatik aktivasyonla taşikardi ve hipertansiyon yapar.
- **Polisiklik Aromatik Hidrokarbonlar (PAH - Benzo[a]piren)** ve **Nitrozaminler (NNK)**: En güçlü karsinojenlerdir! Sitokrom P450 (özellikle CYP1A1) ile karsinojenik epoksit ara ürünlere dönüşür; **TP53** ve **KRAS** genlerinde doğrudan DNA eklentileri (adducts) oluşturarak karsinojenez başlatır.
- **Karbonmonoksit (CO)**: Oksijen taşınmasını engeller.
- **Formaldehit, Akrolein**: Siliyer toksisite yaratarak mukosiliyer temizliği felç eder.

### 3. Tütüne Bağlı Organ Hastalıkları

1. **Kanserler**:
   - Akciğer kanseri (risk 20-30 kat artar; Skuamöz hücreli ve Küçük hücreli karsinomla ilişki en güçlüdür).
   - Larenks, özofagus, pankreas, serviks ve özellikle **Mesane Kanserleri (Ürotelyal Karsinom - 2-naftilamin nedeniyle!)**.
2. **Kardiyovasküler Sistem**:
   - Endotel disfonksiyonu, trombosit agregasyonu artışı, HDL düşüşü ve oksidatif LDL artışı ile **Ateroskleroz ve Miyokard Enfarktüsü** riskini katlar.
3. **Solunum Sistemi**:
   - **Kronik Obstrüktif Akciğer Hastalığı (KOAH)**: Lökosit elastaz aktivitesini artırıp alfa-1 antitripsini oksitleyerek inaktive eder -> **Sentriasiner Amfizem**.
""",
        "spotPearls": [
            "▸ Tütün dumanındaki en güçlü karsinojenler **Polisiklik Aromatik Hidrokarbonlar (PAH)** ve tütüne özgü **Nitrozaminlerdir (NNK)**; p53 mutasyonunu tetiklerler.",
            "🔴 ÖNEMLİ: Tütün kullanımı yalnızca akciğer kanseri değil; mesanede **Ürotelyal Karsinom** (idrarla atılan aromatik aminler nedeniyle) ve özofagus kanseri riskini katlar.",
            "🔵 ÇIKMIŞ SORU: Sigara dumanının amfizem yapma mekanizması; nötrofil elastazını artırıp koruyucu **alfa-1 antitripsin enzimini oksidatif olarak inaktive etmesidir** (proteaz-antiproteaz dengesizliği)."
        ],
        "coreContent": [
            {"title": "PAH ve Nitrozaminler", "description": "DNA eklentileri (adducts) oluşturarak TP53 ve KRAS mutasyonu yapan karsinojenler.", "highYieldBadge": "Karsinojen", "details": "Sitokrom P450 CYP1A1 ile aktif karsinojene dönerler."},
            {"title": "Mesane Kanseri İlişkisi", "description": "Tütündeki 2-naftilamin ve metabolitlerinin mesane ürotelyumunu karsinojenize etmesi.", "highYieldBadge": "Ekstra-pulmoner Kanser", "details": "Mesane kanserlerinin en önemli etyolojik nedenidir."},
            {"title": "Alfa-1 Antitripsin İnhibisyonu", "description": "Sigaranın elastazı uyarırken antiproteaz frenini kırması.", "highYieldBadge": "Amfizem Mekanizması", "details": "Sentriasiner amfizem patolojisinin temelidir."}
        ],
        "flashcards": [
            {"id": "fc-gp-29", "front": "Tütün dumanında bağımlılık yapan madde ile DNA mutasyonuna yol açan ana karsinojen grup nedir?", "back": "Bağımlılık yapan: Nikotin; Karsinojenler: Polisiklik Aromatik Hidrokarbonlar (PAH) ve Nitrozaminler.", "tag": "Onkopatoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-30", "front": "Sigara içiminin akciğerde sentriasiner amfizeme yol açmasındaki proteaz-antiproteaz mekanizması nasıldır?", "back": "Nötrofil elastaz salınımını uyarırken, koruyucu alfa-1 antitripsini oksitleyerek inaktive eder.", "tag": "Akciğer Patolojisi", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-15",
                "question": "Günde 2 paket sigara içen 60 yaşındaki bir hastada hematüri saptanması üzerine yapılan sistoskopide mesanede papiller tümöral kitle izleniyor ve ürotelyal karsinom tanısı konuyor. Tütün dumanının mesane karsinojenezinde rol oynayan en önemli kimyasal karsinojenik bileşeni aşağıdakilerden hangisidir?",
                "options": [
                    "A) Karbonmonoksit",
                    "B) Aromatik Aminler (2-Naftilamin)",
                    "C) Nikotin",
                    "D) Akrolein",
                    "E) Katran fenolleri"
                ],
                "correctAnswer": "B",
                "explanation": "Tütün dumanında bulunan aromatik aminler (özellikle 2-naftilamin) karaciğerde metabolize edildikten sonra idrarla atılırken mesane ürotelyumu ile temas eder ve ürotelyal karsinom riskini belirgin artırır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Pasif içicilikte (ikincil duman) çocuklarda gelişen otitis media ve astım alevlenmesi mekanizması nedir?",
            "Kotinin biyobelirtecinin tütün maruziyetini ölçmedeki farmakokinetik avantajı nedir?"
        ]
    },

    # SLIDE 16
    {
        "slideNumber": 16,
        "title": "Alkol Metabolizması ve Biyokimyasal Toksisite Yolları",
        "subtitle": "Alkol Dehidrogenaz, CYP2E1 (MEOS), Aşırı NADH/NAD+ Oranı ve Asetaldehit",
        "badge": "Alkol Biyokimyası",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. Etanolün Emilimi ve Dağılımı

Alınan etanolün %20'si mideden, %80'i ince bağırsaklardan hızla emilir. Alkolün %90'ından fazlası karaciğerde metabolize edilir; kalan %5-10'u akciğer, böbrek ve terle değişmeden atılır (nefes testinin mantığı).

### 2. Karaciğerde Alkolün Üç Yıkım Yolu

```
1. SİTOZOLİK YOL (Düşük/Orta Dozlarda Ana Yol):
   Etanol + NAD+  ───[ Alkol Dehidrogenaz (ADH) ]───>  Asetaldehit + NADH + H+
   
2. MİKROZOMAL YOL (MEOS - Kronik Yüksek Alkoliklerde İndüklenir!):
   Etanol + NADPH + O2  ───[ CYP2E1 (Sitokrom P450) ]───>  Asetaldehit + NADP+ + H2O
   *Bu yolda reaktif oksijen ürünleri (ROS) fırlar ve hepatosit zarı parçalanır!
   
3. PEROKSİZOMAL YOL (Minör Yol):
   Etanol + H2O2  ───[ Katalaz ]───>  Asetaldehit + 2 H2O
```

Ardından toksik Asetaldehit, mitokondride **Aldehit Dehidrogenaz (ALDH)** enzimiyle **Asetat**'a dönüştürülür:
$$\text{Asetaldehit} + NAD^+ \longrightarrow \text{Asetat} + NADH + H^+$$

### 3. Toksisitenin İki Temel Nedeni

1. **Aşırı Yüksek $NADH / NAD^+$ Oranı**:
   - Hem ADH hem ALDH reaksiyonlarında $NAD^+$ tükenir ve devasa miktarda $NADH$ birikir.
   - **Glukoneogenez Durur**: Piruvat laktata kayar -> **Laktik Asidoz** ve **Hipoglisemi**.
   - **Yağ Oksidasyonu Durur**: Yağ asidi $\beta$-oksidasyonu bloke olur; trigliserit sentezi katlanır -> **Hepatik Steatoz (Karaciğer Yağlanması)**!
2. **Asetaldehit Toksisitesi**:
   - Proteinlere kovalent bağlanarak hücresel tübülin polimerizasyonunu bozar, mitokondriyi yıkar ve yüz kızarması, bulantı, baş ağrısına yol açar (Disülfiram ALDH'yi bloke ederek asetaldehit biriktirir).
""",
        "spotPearls": [
            "▸ Alkol metabolizması sonucu sitozol ve mitokondride **$NADH / NAD^+$ oranı aşırı yükselir**; bu biyokimyasal dengesizlik yağ asidi oksidasyonunu durdurarak **karaciğer yağlanmasını (steatoz)** başlatır.",
            "🔴 ÖNEMLİ: Kronik alkolizmde indüklenen mikrozomal enzim **CYP2E1 (MEOS)**'dir; bu enzim reaktif oksijen radikalleri (ROS) üreterek hepatosit nekrozunu katlar ve parasetamol gibi ilaçların toksisitesini artırır!",
            "🔵 ÇIKMIŞ SORU: Alkolik bireylerde açlıkta ani hipoglisemi gelişmesinin nedeni, yüksek NADH düzeylerinin piruvatın glukoneogeneze girişini engelleyip laktata dönüştürmesidir."
        ],
        "coreContent": [
            {"title": "Yüksek NADH/NAD+", "description": "Yağ yakımını engelleyip trigliserit birikimini ve laktik asidozu tetikleyen redoks dengesizliği.", "highYieldBadge": "Metabolik Kilit", "details": "Alkolik steatozun birincil biyokimyasal nedenidir."},
            {"title": "CYP2E1 İndüksiyonu", "description": "Kronik alkol tüketiminde aktive olan mikrozomal etanol oksitleme sistemi.", "highYieldBadge": "Sitokrom P450", "details": "ROS salınımını ve hepatotoksisiteyi tetikler."},
            {"title": "Asetaldehit", "description": "Hücresel proteinleri modifiye eden ve akşamdan kalmalık yaratan toksik ara ürün.", "highYieldBadge": "Toksik Ara Ürün", "details": "Aldehit dehidrogenaz (ALDH) tarafından asetata dönüştürülür."}
        ],
        "flashcards": [
            {"id": "fc-gp-31", "front": "Alkol metabolizması sırasında hücrede artan ve yağ asidi beta-oksidasyonunu bloke eden nükleotid kofaktör oranı nedir?", "back": "NADH / NAD+ oranının aşırı yükselmesidir.", "tag": "Biyokimya", "masterLevel": "Kritik"},
            {"id": "fc-gp-32", "front": "Kronik alkoliklerde etanol tüketimiyle indüklenerek reaktif oksijen radikali üreten mikrozomal sitokrom P450 enzimi hangisidir?", "back": "CYP2E1 (MEOS yolağı).", "tag": "Farmakoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-16",
                "question": "Kronik alkol bağımlısı bir hastada aşırı alkol alımından sonra açlık hipoglisemisi ve karaciğer biyopsisinde yaygın mikroveziküler ve makroveziküler steatoz saptanıyor. Alkolün karaciğerde bu biyokimyasal ve morfolojik değişiklikleri başlatmasındaki temel mekanizma hangisidir?",
                "options": [
                    "A) İntraselüler ATP tüketimi ve fosfat kaybı",
                    "B) Alkol dehidrogenaz reaksiyonu sonucu sitozolik NADH/NAD+ oranının aşırı yükselmesi",
                    "C) Hücre içi kalsiyum tükenmesi",
                    "D) Glukokinaz enziminin genetik inaktivasyonu",
                    "E) Safra asidi sentezinin tamamen durması"
                ],
                "correctAnswer": "B",
                "explanation": "Alkolün alkol dehidrogenaz ve aldehit dehidrogenaz ile oksidasyonu ortamdaki NAD+'ı tüketir ve NADH/NAD+ oranını aşırı yükseltir. Bu durum glukoneogenezi ve yağ asidi oksidasyonunu durdurarak hipoglisemi ve steatoza yol açar.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Doğu Asya toplumlarında ALDH2 eksikliğinin (yüz kızarma sendromu) moleküler mekanizması nedir?",
            "Kronik alkolizmde parasetamol (asetaminofen) toksisite eşiğinin neden düştüğü CYP2E1 üzerinden nasıl açıklanır?"
        ]
    },

    # SLIDE 17
    {
        "slideNumber": 17,
        "title": "Alkolik Karaciğer Hastalığı Morfolojisi: Steatoz, Hepatit ve Siroz",
        "subtitle": "Mallory-Denk Cisimcikleri, Nötrofilik İnfiltrasyon, Perivenüler Fibrozis ve Mikronodüler Siroz",
        "badge": "Alkolik Karaciğer",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. Alkolik Karaciğer Hastalığının Üç Evresi

Kronik alkol tüketimi karaciğerde geri dönüşümlü yağlanmadan ölümcül siroza kadar uzanan 3 aşamalı bir spektrum oluşturur:

```
[ 1. HEPATİK STEATOZ (Yağlı Karaciğer) ] (Olguların %90-100'ü)
Perivenüler (Zon 3) alandan başlayan makroveziküler yağ damlacıkları.
Karaciğer sarı, yumuşak ve 4-6 kg'a kadar büyümüştür.
*ALKOL KESİLİNCE TAMAMEN GERİ DÖNER (Reversibl).*
                    │
                    ▼ Sürekli ve Aşırı Tüketim
[ 2. ALKOLİK HEPATİT (Steatohepatit) ] (Olguların %20-35'i)
Akut hepatosit balonlaşması ve nekrozu + Enflamasyon.
MALLORY-DENK CİSİMCİKLERİ + NÖTROFİL İNFİLTRASYONU.
*Mortalite %10-20'dir; kısmen geri dönebilir.*
                    │
                    ▼ Yıllarca Süren Fibrozis
[ 3. ALKOLİK SİROZ ] (Olguların %8-20'si)
Zon 3 santral ven çevresinden başlayan 'tavuk teli (chicken-wire)' fibrozisi.
Geri dönüşümsüz MİKRONODÜLER (Laennec) SİROZ.
Portal hipertansiyon, özofagus varis kanamaları ve Hepatosellüler Karsinom riski!
```

### 2. Alkolik Hepatitin İki Histopatolojik İmzası

1. **Mallory-Denk Cisimcikleri (Mallory Hyalini)**:
   - Şişmiş (balonlaşmış) hepatositlerin sitoplazmasında izlenen, amorf, koyu eozinofilik (pembe), ip yumağı benzeri inklüzyonlardır.
   - Biyokimyasal içeriği: Yanlış katlanmış, ubikuitinlenmiş **Sitokeratin 8 ve 18** ara filamanlarıdır!
2. **Nötrofil Lökosit İnfiltrasyonu**:
   - Viral hepatitlerde lenfositler baskınken; alkolik hepatitte ölen hepatositlerin ve Mallory cisimciliklerinin etrafını **Nötrofiller** sarar (satellitozis).
""",
        "spotPearls": [
            "▸ Alkolik hepatitin patognomonik mikroskobik bulgusu, sitoplazmada kümeleşmiş ara filamanlardan (sitokeratin 8/18) oluşan pembe **Mallory-Denk Cisimcikleridir (Mallory Hyalini)**.",
            "🔴 ÖNEMLİ: Viral hepatitlerde portal alanda mononükleer lenfositler görülürken; **Alkolik hepatitte parankimde dejenere hepatositlerin etrafında NÖTROFİL infiltrasyonu** karakteristiktir.",
            "🔵 ÇIKMIŞ SORU: Alkolik sirozda nodüller küçüktür (<3 mm); bu tabloya **Mikronodüler (Laennec) Siroz** denir."
        ],
        "coreContent": [
            {"title": "Mallory-Denk Cisimcikleri", "description": "Hepatosit sitoplazmasında ubikuitinlenmiş sitokeratin 8/18 yığılması.", "highYieldBadge": "Histopatoloji", "details": "Alkolik hepatit, Wilson ve NASH'ta görülebilir."},
            {"title": "Nötrofil Satellitozisi", "description": "Ölen şişmiş hepatositlerin etrafını nötrofillerin sarması.", "highYieldBadge": "Enflamasyon Deseni", "details": "Viral hepatitten kesin ayrım kriteridir."},
            {"title": "Tavuk Teli (Chicken-Wire) Fibrozis", "description": "Zon 3 santral ven çevresinde sinüzoidleri saran periselüler fibrozis.", "highYieldBadge": "Fibrozis Modeli", "details": "İlerleyerek mikronodüler siroza dönüşür."}
        ],
        "flashcards": [
            {"id": "fc-gp-33", "front": "Alkolik hepatitte saptanan Mallory-Denk cisimcikleri biyokimyasal olarak hangi hücresel yapılardan oluşur?", "back": "Sitokeratin 8 ve 18 (ara filamanlar) ile ubikuitin agregatlarından oluşur.", "tag": "Histopatoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-34", "front": "Alkolik sirozda gelişen rejenerasyon nodüllerinin büyüklük paterni nedir?", "back": "Mikronodüler sirozdur (tüm nodüller genellikle < 3 mm'dir).", "tag": "Gastroenteroloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-17",
                "question": "Yıllardır yoğun alkol tüketen ve sarılık, ateş ile lökositoz tablosuyla başvuran 52 yaşındaki hastanın karaciğer biyopsisinde balonlaşmış hepatositlerin sitoplazmasında eozinofilik, ip yumağı tarzında sitokeratin inklüzyonları (Mallory-Denk cisimcikleri) ve bunları çevreleyen yoğun nötrofilik infiltrasyon saptanıyor. Bu hastadaki kesin tanı nedir?",
                "options": [
                    "A) Hepatik Steatoz tek başına",
                    "B) Alkolik Hepatit (Steatohepatit)",
                    "C) Primer Bilier Kolanjit",
                    "D) Kronik Hepatit B enfeksiyonu",
                    "E) Karaciğer Hemanjiomu"
                ],
                "correctAnswer": "B",
                "explanation": "Balonlaşmış hepatosit nekrozu, Mallory-Denk cisimcikleri ve nötrofil lökosit infiltrasyonu Alkolik Hepatitin (Steatohepatit) klasik histopatolojik triadıdır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Alkolik siroz ile hepatit C sirozunun makroskobik nodül boyutu (mikronodüler vs. makronodüler) farkı nedir?",
            "İto (hepatik stellat) hücrelerinin alkol hasarında TGF-beta ile miyofibroblasta dönüşüp kollajen sentezlemesi nasıl gerçekleşir?"
        ]
    },

    # SLIDE 18
    {
        "slideNumber": 18,
        "title": "Şiddetli Akut Yetersiz Beslenme (SAM): Somatik ve Visseral Kompartmanlar",
        "subtitle": "Gelişmekte Olan Ülkelerde Çocuk Mortalitesi, İki Protein Havuzunun Patolojisi",
        "badge": "Malnütrisyon",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Şiddetli Akut Yetersiz Beslenme (Severe Acute Malnutrition - SAM)

Gelişmekte olan ülkelerde 5 yaş altı çocuk ölümlerinin üçte birinden fazlasının altında yatan temel veya kolaylaştırıcı neden **yetersiz beslenmedir (malnütrisyon)**.

Dünya Sağlık Örgütü tanımına göre çocuğun ağırlığının boyuna göre ortalamanın 3 standart sapma altında olması (-3 SD) veya boya göre ağırlığın **%70'in altına düşmesi** şiddetli malnütrisyon olarak tanımlanır.

### 2. İki Protein Kompartmanı Hipotezi

Vücudun protein rezervleri iki anatomik ve fonksiyonel havuzda saklanır:

```
+-----------------------------------------------------------------------------------+
|                        İKİ PROTEİN KOMPARTMANI VE HASTALIKLAR                     |
+-----------------------------------------------------------------------------------+
| 1. SOMATİK PROTEİN KOMPARTMANI:                                                   |
|    - İskelet kaslarında depolanan proteinlerdir.                                  |
|    - Kol çevresi (kol kas kalınlığı) ölçümüyle değerlendirilir.                   |
|    - Kalori eksikliğinde enerji sağlamak için ilk eriyen havuzdur.                |
|    - **MARASMUS'TA BİRİNCİL OLARAK YIKILIR!**                                     |
|                                                                                   |
| 2. VİSSERAL PROTEİN KOMPARTMANI:                                                  |
|    - İç organlarda (özellikle karaciğerde) depolanan ve dolaşıma salınan          |
|      proteinlerdir (Albümin, Prealbümin, Transferrin).                            |
|    - Serum albümin düzeyi ile laboratuvarda ölçülür.                              |
|    - Protein yoksunluğunda karaciğer protein sentezleyemez; albümin düşer.        |
|    - **KWASHİORKOR'DA BİRİNCİL OLARAK ÇÖKER!**                                    |
+-----------------------------------------------------------------------------------+
```

Bu iki kompartmanın tutulum farklılığı, SAM spektrumunun iki kutbunu oluşturan **Marasmus** ve **Kwashiorkor** tablolarını belirler.
""",
        "spotPearls": [
            "▸ Somatik protein kompartmanı **iskelet kaslarını** temsil eder ve **Marasmus**'ta erir; visseral protein kompartmanı **karaciğeri ve serum albüminini** temsil eder ve **Kwashiorkor**'da çöker.",
            "🔴 ÖNEMLİ: Marasmus'ta kalori eksikliğine rağmen karaciğer fonksiyonları görece korunduğu için **serum albümin düzeyi normale yakındır ve ÖDEM GÖRÜLMEZ**!",
            "🔵 ÇIKMIŞ SORU: Visseral protein kompartmanındaki erimenin klinik yansıması **hipoalbüminemi ve jeneralize ödemdir** (Kwashiorkor)."
        ],
        "coreContent": [
            {"title": "Somatik Kompartman", "description": "İskelet kas kütlesi; kol çevresiyle izlenir, Marasmus'ta tükenir.", "highYieldBadge": "Kas Havuzu", "details": "Amino asitler glukoneogenez için tüketilir."},
            {"title": "Visseral Kompartman", "description": "Karaciğer ve serum albümini; Kwashiorkor'da çöker.", "highYieldBadge": "Organ Havuzu", "details": "Hipoalbüminemi ve onkotik basınç kaybı yapar."},
            {"title": "SAM Kriteri", "description": "Boya göre ağırlığın %70'in altına düşmesi veya -3 SD gerilik.", "highYieldBadge": "DSÖ Kriteri", "details": "Enfeksiyonlara ikincil immün yetmezlik eşlik eder."}
        ],
        "flashcards": [
            {"id": "fc-gp-35", "front": "Malnütrisyon değerlendirmesinde somatik protein kompartmanını yansıtan doku hangisidir?", "back": "İskelet kası kütlesidir (kol kası çevresiyle ölçülür).", "tag": "Pediatri", "masterLevel": "Kritik"},
            {"id": "fc-gp-36", "front": "Visseral protein kompartmanının çöküşünü gösteren en temel laboratuvar parametresi nedir?", "back": "Serum albümin düzeyindeki belirgin düşüştür (hipoalbüminemi).", "tag": "Biyokimya", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-18",
                "question": "Ağır beslenme yetersizliği olan iki çocuktan birincisinde iskelet kaslarının ileri derecede eridiği ancak serum albümin düzeyinin normal olduğu; ikincisinde ise kas erimesi az olmasına rağmen serum albümininin ileri derecede düşük ve yaygın ödemin olduğu saptanıyor. Bu iki çocuğun etkilendikleri protein kompartmanları sırasıyla hangisidir?",
                "options": [
                    "A) 1. çocuk: Visseral kompartman / 2. çocuk: Somatik kompartman",
                    "B) 1. çocuk: Somatik kompartman / 2. çocuk: Visseral kompartman",
                    "C) Her iki çocukta da yalnızca somatik kompartman",
                    "D) Her iki çocukta da yalnızca visseral kompartman",
                    "E) Yalnızca yağ dokusu kompartmanı"
                ],
                "correctAnswer": "B",
                "explanation": "İskelet kası erimesiyle seyredip albüminin korunduğu durum Somatik kompartman tutulumudur (Marasmus); albüminin düşüp ödemin geliştiği durum ise Visseral kompartman tutulumudur (Kwashiorkor).",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Marasmik-Kwashiorkor miks tablosunun tanı kriterleri nelerdir?",
            "Malnütrisyonlu çocuklarda timus atrofisi ve enfeksiyon yatkınlığının hücresel temeli nedir?"
        ]
    },

    # SLIDE 19
    {
        "slideNumber": 19,
        "title": "Marasmus: Ağır Kalori Yoksunluğu ve Somatik Kas Erimesi",
        "subtitle": "Kortizol Aracılı Kas Katabolizması, 'Yaşlı Adam Yüzü' ve Ödemsiz Zayıflık",
        "badge": "Marasmus",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Marasmus Nedir?

Marasmus; hem protein hem de karbonhidrat dahil olmak üzere **tüm besin ögelerinin ve kalorinin ağır derecede yetersiz alınması** sonucu ortaya çıkan aşırı zayıflama tablosudur. Genellikle anne sütünün erken kesildiği ve yerine besleyici olmayan sulu gıdaların verildiği ilk 1 yaş içinde görülür.

### 2. Patofizyoloji ve Klinik Bulgular

1. **Aşırı Kas ve Yağ Erimesi**:
   - Kalori gelmeyince vücut glukoz sağlamak için endojen enerji kaynaklarını yakar:
     - Önce subkutan yağ dokusu tamamen tüketilir.
     - Ardından iskelet kasları (somatik protein) amino asitlere parçalanır.
   - Vücut ağırlığı standartların **%60'ının altına düşer**.
2. **Karakteristik 'Yaşlı Adam / Maymun Yüzü' Görünümü**:
   - Yanaklardaki yağ yastıkçıkları (**Bichat yağ dokusu**) vücutta en son eriyen yağ deposudur. Marasmus'ta bu yastıkçıklar da eridiğinde yanaklar çöker ve çocuk minyatür bir yaşlı insan görünümü kazanır.
3. **Ödem YOKTUR!**:
   - Marasmus'ta karaciğer protein havuzu (visseral kompartman) göreceli olarak korunduğu için karaciğer albümin sentezlemeye devam eder.
   - **Serum albümin düzeyi normal veya normale yakındır; bu nedenle MARASMUS'TA HİÇBİR ZAMAN ÖDEM GÖRÜLMEZ!**
4. **Diğer Bulgular**: Büyüme ve gelişme tamamen durur; hipotermi, bradikardi, zayıf ve cansız saçlar.
""",
        "spotPearls": [
            "▸ Marasmus = **AĞIR KALORİ (ENERJİ) EKSİKLİĞİ**dir; vücut ağırlığı normalin **<%60**'ına iner.",
            "🔴 ÖNEMLİ: Marasmus'ta visseral protein ve serum albümini korunduğu için **ÖDEM KESİNLİKLE GÖRÜLMEZ**; deri-kemik kalmış bir görünüm ve **'yaşlı adam yüzü'** mevcuttur.",
            "🔵 ÇIKMIŞ SORU: *'Şiddetli malnütrisyonlu bir çocukta subkutan yağ dokusunun tamamen kaybolduğu, kas erimesinin belirgin olduğu ancak asit ve periferik ödemin bulunmadığı tablo hangisidir?'*\n  ▫ Doğru yanıt: **Marasmus**'tur."
        ],
        "coreContent": [
            {"title": "Kalori Yoksunluğu", "description": "Tüm besin kaynaklarının global olarak yetersiz kalması.", "highYieldBadge": "Etiyoloji", "details": "Ağırlık normalin %60'ının altına iner."},
            {"title": "Ödem Yokluğu", "description": "Serum albümininin korunması nedeniyle onkotik basınç düşmez.", "highYieldBadge": "Kritik Ayırıcı Tanı", "details": "Kwashiorkor'dan ayıran en temel klinik bulgudur."},
            {"title": "Yaşlı Adam Yüzü", "description": "Bichat yanak yağ pedlerinin bile tükenmesiyle oluşan çökük yüz.", "highYieldBadge": "Morfoloji", "details": "Deri kemiğe yapışmış görünümündedir."}
        ],
        "flashcards": [
            {"id": "fc-gp-37", "front": "Marasmus'ta Kwashiorkor'un aksine ödem görülmemesinin temel nedeni nedir?", "back": "Visseral protein kompartmanı ve serum albümin düzeyinin göreceli olarak korunmasıdır.", "tag": "Pediatri", "masterLevel": "Kritik"},
            {"id": "fc-gp-38", "front": "Marasmus hangi yaş grubunda ve ne tür bir besin eksikliğiyle tipik olarak ortaya çıkar?", "back": "İlk 1 yaş içinde; total kalori (enerji) eksikliğiyle ortaya çıkar.", "tag": "Beslenme", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-19",
                "question": "9 aylık bir bebekte ileri derecede kilo kaybı, kol çevresinde aşırı incelme, temporal ve bukkal yağ dokusunun erimesi sonucu buruşuk 'yaşlı adam yüzü' görünümü saptanıyor. Muayenesinde batında asit veya ekstremitelerde gode bırakan ödem izlenmiyor ve serum albümin düzeyi 3.6 g/dL (normal) bulunuyor. Bu çocuk için en olası tanı nedir?",
                "options": [
                    "A) Kwashiorkor",
                    "B) Marasmus",
                    "C) Çölyak Hastalığı",
                    "D) Kistik Fibrozis",
                    "E) Nefrotik Sendrom"
                ],
                "correctAnswer": "B",
                "explanation": "Aşırı somatik kas ve yağ dokusu erimesi, yaşlı adam yüzü görünümü olmasına rağmen serum albümininin normal olması ve ödemin bulunmaması Marasmus'un klasik tablosudur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Marasmuslu bir çocukta leptin düzeyleri neden saptanamayacak kadar düşüktür?",
            "Yeniden besleme sendromunda (Refeeding syndrome) hipofosfatemi gelişim mekanizması nasıldır?"
        ]
    },

    # SLIDE 20
    {
        "slideNumber": 20,
        "title": "Kwashiorkor: Protein Yoksunluğu, Masif Ödem ve Yağlı Karaciğer",
        "subtitle": "Hipoalbüminemi, Yaygın Asit, Flaky-Paint Dermatiti ve Bayrak Saçı Belirtisi",
        "badge": "Kwashiorkor",
        "badgeColor": "sky",
        "synthesisNarrative": """### 1. Kwashiorkor Nedir?

Kwashiorkor (Gana dilinde 'ikinci çocuk doğduğunda tahttan indirilen birinci çocuğun hastalığı' anlamına gelir); **kalori alımı görece yeterli veya hafif düşükken, PROTEİN ALIMININ NEREDEYSE SIFIR OLDUĞU** tablodur. Tipik olarak anne sütünden kesilip sadece karbonhidrattan zengin (mısır, pirinç, manyok lapası) beslenen 1-4 yaş arası çocuklarda görülür.

### 2. Patofizyoloji ve Dört Kardinal Bulgusu

```
+-----------------------------------------------------------------------------------+
|                        KWASHİORKOR PATOFİZYOLOJİK ZİNCİRİ                         |
+-----------------------------------------------------------------------------------+
| Ağır Diyet Protein Yoksunluğu (Yalnızca karbonhidrat/nişasta alımı)               |
|                           │                                                       |
|                           ▼                                                       |
| Karaciğer Amino Asit Bulamaz -> VİSSERAL PROTEİN SENTEZİ ÇÖKER!                   |
|  ┌────────────────────────┴────────────────────────────────────────┐              |
|  ▼                                                                 ▼              |
|[ HİPOALBÜMİNEMİ VE MASİF ÖDEM ]                   [ HEPATİK STEATOZ (YAĞLANMA) ]  |
|Plazma albümini < 2.5 g/dL'ye düşer;                Karaciğer apolipoprotein       |
|onkötik basınç çöker.                               (özellikle ApoB-100) sentez-   |
|İnterstisyuma sıvı kaçar: Bacaklarda ödem,          leyemez! Trigliseritler VLDL   |
|karında belirgin ASİT ('göbekli çocuk'!).           olarak kana verilemez ve KC'de |
|Çocuğun kilosu ödem nedeniyle yanıltıcı             birikir -> Masif Yağlı KC!     |
|olarak korunmuş görünebilir!                                                       |
+-----------------------------------------------------------------------------------+
```

### 3. Deri ve Saçın Karakteristik Morfolojisi

- **Flaky-Paint Dermatiti (Pul Pul Dökülen Boya)**: Deride hiperkeratotik, pullu, soyulan, çatlamış emaye boya benzeri pigmentli plaklar ve açık yaralar.
- **Bayrak Saçı (Flag Sign)**: Dönem dönem protein alınıp alınmamasına bağlı olarak saç tellerinde ardışık açık renkli (hipopigmente) ve koyu renkli bantlar oluşması. Saçlar ince, kıvrımsız ve dökülgendir.
""",
        "spotPearls": [
            "▸ Kwashiorkor = **AĞIR PROTEİN YOKSUNLUĞU**dur (kalori karbonhidratla görece korunmuştur).",
            "🔴 ÖNEMLİ: Karaciğer protein sentezleyemediği için **ağır Hipoalbüminemi ve masif Jeneralize Ödem/Asit** gelişir; ödem kilo kaybını maskeleyebilir.",
            "🔵 ÇIKMIŞ SORU: Kwashiorkor'da karaciğerin aşırı yağlanarak büyümesinin nedeni, **apolipoprotein sentezlenememesi nedeniyle trigliseritlerin karaciğerden VLDL olarak dışarı atılamamasıdır**."
        ],
        "coreContent": [
            {"title": "Protein Açlığı (Karbonhidrat Doygunluğu)", "description": "Sadece nişastalı pürelerle beslenen çocukta albümin sentezinin durması.", "highYieldBadge": "Etiyoloji", "details": "Genellikle sütten kesilip katı karbonhidrata geçişte olur."},
            {"title": "Hipoalbüminemik Ödem", "description": "Onkotik basıncın çökmesi sonucu bacaklarda ve batında masif sıvı toplanması.", "highYieldBadge": "Kardinal Bulgu", "details": "Karnı şiş, yanakları ödemli 'ay yüz' görünümü verir."},
            {"title": "Hepatik Steatoz (Apo Eksikliği)", "description": "Apolipoprotein yokluğunda yağların karaciğere hapsolması.", "highYieldBadge": "Patofizyoloji", "details": "Karaciğer hepatomegali ile ele gelir."},
            {"title": "Flaky-Paint Dermatiti", "description": "Soyulmuş emaye boya tarzında hiperpigmente pullu döküntüler.", "highYieldBadge": "Dermatopatoloji", "details": "Amino asit ve çinko eksikliği ile ilişkilidir."}
        ],
        "flashcards": [
            {"id": "fc-gp-39", "front": "Kwashiorkor'da masif karaciğer yağlanması (hepatosteatoz) gelişmesinin biyokimyasal nedeni nedir?", "back": "Apolipoprotein (ApoB-100) sentezlenememesi nedeniyle trigliseritlerin VLDL olarak karaciğerden kana verilememesidir.", "tag": "Patoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-40", "front": "Kwashiorkor'u Marasmus'tan ayıran en temel klinik bulgu nedir?", "back": "Hipoalbüminemiye bağlı jeneralize ödem ve asit varlığıdır.", "tag": "Ayırıcı Tanı", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-20",
                "question": "2 yaşında anne sütünden kesildikten sonra sadece patates ve mısır lapası ile beslenen bir çocukta bacaklarda gode bırakan ödem, batında asit, deride pul pul dökülen emaye boya benzeri hiperpigmente lezyonlar saptanıyor. Palpasyonda karaciğeri 4 cm büyük bulunan bu çocukta hepatomegalinin temel histopatolojik nedeni aşağıdakilerden hangisidir?",
                "options": [
                    "A) Kupffer hücrelerinde demir birikimi (hemosiderozis)",
                    "B) Hepatositlerde glikojen depolanması",
                    "C) Apolipoprotein sentez eksikliğine bağlı hepatik steatoz (trigliserit birikimi)",
                    "D) Hepatik ven trombozu (Budd-Chiari)",
                    "E) Karaciğerde amiloid birikimi"
                ],
                "correctAnswer": "C",
                "explanation": "Kwashiorkor'da diyetle protein alınamadığı için karaciğerde apolipoprotein sentezi durur; sentezlenen trigliseritler VLDL olarak kana salınamaz ve hepatositler içinde birikerek masif hepatik steatoza yol açar.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kwashiorkor ile nefrotik sendromun ödem ve hipoalbüminemi ayırıcı tanısında idrar tahlilinin rolü nedir?",
            "Saçtaki 'bayrak belirtisi (flag sign)' malnütrisyonun zaman çizelgesini nasıl yansıtır?"
        ]
    },

    # SLIDE 21
    {
        "slideNumber": 21,
        "title": "Yeme Bozuklukları Patolojisi: Anoreksiya Nervoza vs. Bulimia Nervoza",
        "subtitle": "Şiddetli Kilo Kaybı, Amenore, Lanugo vs. Diş Minesi Erozyonu ve Boerhaave Yırtığı",
        "badge": "Yeme Bozuklukları",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Yeme Bozukluklarının İki Zıt Yüzü

Genellikle genç kadınlarda beden algısı bozukluğu ile seyreden psikiyatrik kökenli ağır medikal tablolardır:

| Özellik | Anoreksiya Nervoza | Bulimia Nervoza |
| :--- | :--- | :--- |
| **Vücut Ağırlığı** | **Aşırı düşük (BMI < 17.5 veya beklenenin <%85'i)**; hasta kendini zayıf kabul etmez. | **Normal veya hafif kilolu (BMI normal)**; kilo dalgalanmaları görülür. |
| **Davranış Modeli** | Şiddetli aç kalma, aşırı egzersiz, gıda kısıtlama. | Tıkanırcasına yeme nöbetleri (binge eating) ve ardından **kusma / laksatif kullanma**. |
| **Endokrin Bulgular** | GnRH baskılanması sonucu **Amenore** (adet kesilmesi), T3/T4 düşüşü, kemik erimesi (**Osteoporoz**). | Menstrüel düzensizlik olabilir ancak kalıcı amenore nadirdir. |
| **Fizik Muayene** | **Lanugo tüyleri** (ince fetal tüylenme), kaşeksi, cilt kuruluğu, soğuk intoleransı. | El sırtında kusmaya bağlı diş izleri (**Russell Belirtisi**), parotis bezi hipertrofisi. |
| **Gastrointestinal / Diş** | Mide boşalmasında gecikme, kabızlık. | Mide asidi nedeniyle **diş minesinde lingual erozyon**, özofajit, Mallory-Weiss yırtıkları ve ölümcül **Boerhaave Sendromu (Özofagus Rüptürü)**. |
| **Ölüm Nedenleri** | **Hipokalemiye bağlı ventriküler kardiyak aritmiler**, kalp durması, intihar. | **Hipokalemik metabolik alkaloz**, kardiyak aritmiler, özofagus perforasyonu. |
""",
        "spotPearls": [
            "▸ **Anoreksiya Nervoza**: Hasta **kaşektiktir (aşırı zayıftır)**; hipotalamik GnRH baskılanmasıyla **Amenore**, kemik kaybı (**Osteoporoz**) ve vücutta ince fetal **Lanugo tüyleri** görülür.",
            "🔴 ÖNEMLİ: **Bulimia Nervoza**: Hastanın kilosu **NORMALDİR**; tekrarlayan kusmalar nedeniyle **diş minesi erozyonu**, bilateral parotis bezi hipertrofisi ve parmak sırtında nasırlar (**Russell Belirtisi**) izlenir.",
            "🔵 ÇIKMIŞ SORU: Her iki yeme bozukluğunda da en sık ani ölüm nedeni **Hipokalemiye bağlı kardiyak aritmilerdir** (uzamış QT, torsades de pointes)."
        ],
        "coreContent": [
            {"title": "Anoreksiya Kaşeksisi", "description": "BMI < 17.5, amenore, osteoporoz ve lanugo tüyleri.", "highYieldBadge": "Aşırı Zayıflık", "details": "Kardiyak kas atrofisi ve aritmi ile sonlanır."},
            {"title": "Bulimia Diş Erozyonu", "description": "Sık kusmaya bağlı mide hidroklorik asidinin diş minesini eritmesi.", "highYieldBadge": "Kusma Kanıtı", "details": "Parotis bezleri tükürük salgısını artırmak için büyür."},
            {"title": "Boerhaave Sendromu", "description": "Zorlu kusma sonucu özofagus alt ucunun tam kat rüptürü.", "highYieldBadge": "Cerrahi Acil", "details": "Mediastinit ve pnömomediastinum yaratır; mortalitesi yüksektir."}
        ],
        "flashcards": [
            {"id": "fc-gp-41", "front": "Bulimia nervoza hastalarının fizik muayenesinde kusmayı ele veren parmak sırtı lezyonunun adı nedir?", "back": "Russell belirtisi (dişlerin el sırtını travmatize etmesi).", "tag": "Klinik Muayene", "masterLevel": "Yüksek"},
            {"id": "fc-gp-42", "front": "Anoreksiya nervozada amenore gelişiminin nöroendokrin mekanizması nedir?", "back": "Aşırı kilo kaybı ve leptin düşüşü sonucu hipotalamik GnRH salınımının baskılanmasıdır.", "tag": "Endokrinoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-21",
                "question": "Beden kitle indeksi 22 kg/m² (normal) olan 20 yaşındaki bir üniversite öğrencisinde diş hekimi muayenesinde maksiller ön dişlerin lingual yüzeyinde mine tabakasının yaygın olarak eridiği saptanıyor. Hastanın el muayenesinde metakarpofalangeal eklem dorsalinde nasırlaşmış lezyonlar (Russell belirtisi) ve bilateral parotis bezi büyümesi izleniyor. Bu hasta için en olası tanı nedir?",
                "options": [
                    "A) Anoreksiya Nervoza",
                    "B) Bulimia Nervoza",
                    "C) Primer Hiperparatiroidizm",
                    "D) Sjögren Sendromu",
                    "E) Gastroözofageal Reflü Hastalığı tek başına"
                ],
                "correctAnswer": "B",
                "explanation": "Normal vücut ağırlığına rağmen diş minesi erozyonu, parotis bezi hipertrofisi ve parmak sırtında Russell belirtisi bulunması klasik Bulimia Nervoza tablosudur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Mallory-Weiss yırtığı (mukoza yırtığı) ile Boerhaave sendromu (tam kat rüptür) arasındaki cerrahi fark nedir?",
            "Bulimia nervozada hipokalemik metabolik alkaloz gelişme mekanizması nasıldır?"
        ]
    },

    # SLIDE 22
    {
        "slideNumber": 22,
        "title": "Obezite Patofizyolojisi: Nörohumoral Aks, Leptin ve Adiponektin",
        "subtitle": "Lipostat Teorisi, Hipotalamus POMC/CART, Tokluk Mekanizması ve Adipokinler",
        "badge": "Obezite Aksı",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. Obezite Nedir ve Nasıl Tanımlanır?

Obezite; vücutta sağlığı bozacak ölçüde aşırı yağ dokusu birikimidir. En yaygın ölçüt **Vücut Kitle İndeksidir (Body Mass Index - BMI)**:
$$\text{BMI} = \frac{\text{Ağırlık (kg)}}{\text{Boy (m)}^2}$$
- Normal: $18.5 - 24.9\ \text{kg/m}^2$
- Fazla Kilolu: $25.0 - 29.9\ \text{kg/m}^2$
- **Obezite**: $\ge 30.0\ \text{kg/m}^2$ (Sınıf I: 30-34.9; Sınıf II: 35-39.9; Sınıf III Morbid: $\ge 40$).

### 2. Nörohumoral Enerji Dengesi ('Lipostat Modeli')

Vücut ağırlığı hipotalamustaki **Arkuat Nükleus** tarafından yönetilen hassas bir nörohumoral geri bildirim döngüsüyle ayarlanır:

```
[ AFFERENT SİNYALLER (Çevre Dokulardan) ]
1. LEPTİN      : Adipositlerden salınır. Yağ deposu dolunca kana verilir (Uzun vadeli tokluk!).
2. ADİPONEKTİN : Adipositlerden salınır. İnsülin duyarlılaştırıcı ve anti-enflamatuar.
3. GHRELİN     : Mide fundusundan açlıkta salınır (Tek iştah açıcı oreksijenik hormon!).
4. PYY / GLP-1 : İleum ve kolondan yemek sonrası salınır (Kısa vadeli tokluk).
                     │
                     ▼
[ SANTRAL İŞLEMCİ: HİPOTALAMUS ARKUAT NÜKLEUS ]
  ┌──────────────────┴──────────────────────────────────┐
  ▼                                                     ▼
[ ANOREKSİJENİK YOLAK (Tokluk) ]        [ OREKSİJENİK YOLAK (Açlık) ]
Leptin POMC ve CART nöronlarını         Leptin NPY ve AgRP nöronlarını
uyarır -> Alfa-MSH salınır ->            baskılar. Ghrelin ise bunları uyarır.
MC4R reseptörü aktive olur.              İştah açılır, enerji harcaması
İŞTAH KAPANIR, ENERJİ HARCANIR!         düşürülür.
```

### 3. Leptin vs. Adiponektin: İki Kritik Adipokin

- **Leptin**: Yağ dokusu arttıkça kanda seviyesi katlanır. Ancak yaygın obezitede leptin geni sağlamdır; sorun reseptör düzeyinde **Leptin Direncidir (Leptin Resistance)**!
- **Adiponektin ('İyi Adipokin')**: Karaciğer ve kasta serbest yağ asidi oksidasyonunu artırır, insülin duyarlılığını artırır ve endoteli korur. **Paradoksik olarak obezitede düzeyi DÜŞER!** Düşük adiponektin seviyesi metabolik sendrom ve diyabet gelişimini hızlandırır.
""",
        "spotPearls": [
            "▸ **Leptin**, adipositlerden salınarak hipotalamusta POMC/CART nöronları ve **MC4R** üzerinden iştahı kapatan ana tokluk hormonudur.",
            "🔴 ÖNEMLİ: Obezitede leptin kanda çok yüksektir ancak **Leptin Direnci** nedeniyle tokluk sinyali iletilemez; koruyucu **Adiponektin düzeyi ise obezitede PARADOKSİK OLARAK DÜŞER**!",
            "🔵 ÇIKMIŞ SORU: Mideden salınarak hipotalamusu uyaran ve iştahı doğrudan artıran tek oreksijenik hormon **Ghrelin**'dir."
        ],
        "coreContent": [
            {"title": "Leptin ve POMC/CART", "description": "Adipositlerden salınıp tokluk oluşturan anoreksijenik sinyal.", "highYieldBadge": "Tokluk Hormonu", "details": "Monogenik obezitelerin en sık nedeni MC4R mutasyonudur."},
            {"title": "Adiponektin Paradoksu", "description": "İnsülin duyarlılaştırıcı adipokin; yağ dokusu arttıkça kandaki düzeyi azalır.", "highYieldBadge": "Anti-diyabetik", "details": "Düşüklüğü kardiyovasküler riski artırır."},
            {"title": "Ghrelin (Açlık Sinyali)", "description": "Boş mideden salınıp NPY/AgRP üzerinden yemek yemeyi tetikleyen hormon.", "highYieldBadge": "İştah Açıcı", "details": "Gastrik bypass cerrahisinde fundus çıkarılınca düzeyi düşer."}
        ],
        "flashcards": [
            {"id": "fc-gp-43", "front": "Yağ dokusundan salgılanan, insülin duyarlılığını artıran ancak obezitede kandaki seviyesi azalan adipokin hangisidir?", "back": "Adiponektin.", "tag": "Endokrinoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-44", "front": "Mideden salınarak hipotalamus üzerinden acıkma hissini başlatan tek periferik hormon nedir?", "back": "Ghrelin.", "tag": "Fizyoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-22",
                "question": "Obezite patofizyolojisinde adipositler tarafından salgılanarak endotel hasarını önleyen, kasta serbest yağ asidi oksidasyonunu uyararak insülin duyarlılığını artıran ve obez bireylerde paradoksal olarak plazma düzeyi belirgin derecede AZALMIŞ olan adipokin hangisidir?",
                "options": [
                    "A) Leptin",
                    "B) Adiponektin",
                    "C) Rezistin",
                    "D) Ghrelin",
                    "E) TNF-alfa"
                ],
                "correctAnswer": "B",
                "explanation": "Adiponektin ('yağ yakan/insülin duyarlılaştırıcı adipokin'), yağ dokusu kütlesi arttıkça kandaki seviyesi paradoksal olarak düşen yegane adipokindir ve düşüklüğü Tip 2 DM riskini artırır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "İnsanlarda monogenik obeziteye yol açan melanokortin 4 reseptör (MC4R) mutasyonlarının klinik özellikleri nelerdir?",
            "Viseral (abdominal/elma tipi) obezite ile subkutan (armut tipi) obezitenin portal serbest yağ asidi deşarjı farkı nedir?"
        ]
    },

    # SLIDE 23
    {
        "slideNumber": 23,
        "title": "Obezitenin Klinik Sonuçları ve Kanser Biyolojisi",
        "subtitle": "Metabolik Sendrom, İnsülin Direnci, Periferik Aromataz ve Hormona Bağımlı Kanserler",
        "badge": "Obezite & Kanser",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Obezite ve Metabolik Sendrom

Özellikle viseral (intraabdominal) yağlanma, serbest yağ asitlerini doğrudan portal ven yoluyla karaciğere boşaltarak sistemik **İnsülin Direncini** ve **Metabolik Sendromu** tetikler:
- Tip 2 Diabetes Mellitus
- Hipertansiyon
- Dislipidemi (Yüksek Trigliserit, Düşük HDL, Yüksek Küçük Yoğun LDL)
- Non-Alkolik Yağlı Karaciğer Hastalığı (NAFLD / MASH)
- Safra Taşları (Kolelitiyazis - safrada aşırı kolesterol atılımı nedeniyle)
- Hipoventilasyon Sendromu (**Pickwick Sendromu**) ve Obstrüktif Uyku Apnesi

### 2. Obezite Kanser Riskini Nasıl Artırır?

Obezite; tütünden sonra önlenebilir kanser nedenleri arasında ikinci sıradadır. Üç ana moleküler mekanizma ile karsinojenez tetiklenir:

```
+-----------------------------------------------------------------------------------+
|                        OBEZİTEDE KARSİNOJENEZ MEKANİZMALARI                       |
+-----------------------------------------------------------------------------------+
| 1. HİPERİNSÜLİNEMİ VE IGF-1 ARTIŞI:                                               |
|    - İnsülin direnci -> Kompansatuar kronik hiperinsülinemi.                       |
|    - İnsülin karaciğerde IGFBP'yi (IGF bağlayıcı protein) baskılar; serbest       |
|      **IGF-1 (İnsülin Benzeri Büyüme Faktörü-1)** fırlar.                        |
|    - IGF-1 mitojeniktir; hücresel proliferasyonu uyarır ve apoptozu engeller     |
|      (Kolon, meme, prostat kanseri riski!).                                       |
|                                                                                   |
| 2. PERİFERİK AROMATAZ VE ÖSTROJEN FAZLALIĞI:                                      |
|    - Adipoz doku yüksek miktarda **Aromataz** enzimi içerir.                      |
|    - Androjenler adipoz dokuda **Östron ve Östradiol**'e dönüştürülür.            |
|    - Karşılanmamış aşırı östrojen uyarımı: Özellikle menopoz sonrası kadınlarda  |
|      **Endometriyum Karsinomu** (risk 5-10 kat artar!) ve **Meme Kanseri**.       |
|                                                                                   |
| 3. KRONİK DÜŞÜK DERECELİ ENFLAMASYON:                                             |
|    - Nekrotik adipositler etrafında 'taç benzeri yapılar (crown-like structures)' |
|      oluşturan M1 makrofajlar TNF-α, IL-6 salarak tümör mikroçevresi hazırlar.   |
+-----------------------------------------------------------------------------------+
```
""",
        "spotPearls": [
            "▸ Obezitede yağ dokusundaki **Aromataz** enzimi adrenal androjenleri östrojene çevirir; karşılanmamış aşırı östrojen **Endometriyum Adenokarsinomu** riskini 5 ila 10 kat artırır.",
            "🔴 ÖNEMLİ: İnsülin direnci sonucu artan serbest **IGF-1**, apoptozu baskılayıp hücre döngüsünü hızlandırarak **Kolorektal Karsinom** gelişimini tetikler.",
            "🔵 ÇIKMIŞ SORU: Obezitede safraya atılan kolesterol miktarı arttığı için safra kesesinde en sık gelişen taş tipi **Sarı Kolesterol Taşları**dır."
        ],
        "coreContent": [
            {"title": "Aromataz ve Endometriyum", "description": "Yağ dokusunda androjenlerin östrojene dönüşmesi sonucu endometriyum hiperplazisi ve kanseri.", "highYieldBadge": "Hormonal Kanser", "details": "Menopoz sonrası obez kadınlarda en kritik risktir."},
            {"title": "Hiperinsülinemi ve IGF-1", "description": "Mitotik sinyal artışı ve karsinogenez uyarımı.", "highYieldBadge": "Mitotik Yol", "details": "Kolon ve meme kanseri insidansını artırır."},
            {"title": "Pickwick Sendromu", "description": "Morbid obezitede göğüs duvarı kısıtlılığına bağlı hipoventilasyon ve polisitemi.", "highYieldBadge": "Solunum Yetmezliği", "details": "Gündüz aşırı uyuklama ve kor pulmonale ile seyreder."}
        ],
        "flashcards": [
            {"id": "fc-gp-45", "front": "Obez kadınlarda menopoz sonrası endometriyum karsinomu riskini artıran temel periferik enzim nedir?", "back": "Adipoz dokudaki Aromataz enzimidir (androjenleri östrojene çevirir).", "tag": "Onkoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-46", "front": "Obezitede karaciğer kaynaklı serbest IGF-1 artışına yol açan metabolik durum nedir?", "back": "Kronik hiperinsülinemidir (IGF bağlayıcı proteinleri baskılar).", "tag": "Metabolizma", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-23",
                "question": "62 yaşında postmenopozal ve obez (BMI 38 kg/m²) olan bir kadında vajinal kanama nedeniyle yapılan endometriyal biyopside endometrioid adenokarsinom saptanıyor. Bu hastada obezite ile tümör gelişimi arasındaki nedensel ilişkiyi en iyi açıklayan moleküler mekanizma hangisidir?",
                "options": [
                    "A) Adipositlerden salınan aşırı leptinin doğrudan nükleer reseptörleri mutasyona uğratması",
                    "B) Adipoz dokudaki aromataz enzimi aracılığıyla androjenlerin östrojene dönüşmesi ve endometriyumu sürekli uyarması",
                    "C) Safra asitlerinin vajinal kanala geri akması",
                    "D) Glukagon hormonunun karsinojenik etkisi",
                    "E) Adiponektin fazlalığının endometriyal hiperplazi yapması"
                ],
                "correctAnswer": "B",
                "explanation": "Postmenopozal dönemde overler östrojen üretmez; ancak obez kadınlarda genişlemiş yağ dokusunda eksprese edilen aromataz enzimi böbrek üstü bezi androjenlerini östrojene çevirir. Progesteronla karşılanmayan bu östrojen endometriyumu uyararak kanser riskini dramatik artırır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Obezite ilişkili böbrek hasarı (obezite ilişkili glomerülopati / FSGS) patolojisi nasıldır?",
            "Taç benzeri yapıların (crown-like structures) meme kanseri mikroçevresindeki rolü nedir?"
        ]
    },

    # SLIDE 24
    {
        "slideNumber": 24,
        "title": "Moleküler Patoloji Araçları: Karyotipleme, FISH ve Yeni Nesil Dizileme (NGS)",
        "subtitle": "Sitogenetikten Genomik Tıbba, Hedefe Yönelik Tedaviler ve Likit Biyopsi",
        "badge": "Moleküler Tanı",
        "badgeColor": "indigo",
        "synthesisNarrative": """### 1. Moleküler Tanı Devrimi

Modern patoloji artık yalnızca mikroskopta hücre morfolojisine bakmakla kalmayıp, hastalığın altındaki spesifik genetik mutasyonları tespit ederek **kişiselleştirilmiş hedefe yönelik tedaviyi (akıllı ilaçlar)** yönlendirmektedir.

### 2. Temel Tanısal Araçların Hiyerarşisi

| Yöntem | İnceleme Düzeyi | Çözünürlük | Klinik Kullanım Alanı |
| :--- | :--- | :--- | :--- |
| **Konvansiyonel Karyotipleme (G-Bantlama)** | Tüm kromozom sayısı ve büyük yapısal anomaliler | $> 5-10$ Megabaz (Mb) | Trizomiler (Down, Edwards), büyük translokasyonlar (KML'de Philadelphia kromozomu). Canlı bölünen hücre şarttır. |
| **Floresan İn Situ Hibridizasyon (FISH)** | Spesifik kromozom bölgeleri, mikrodelesyonlar ve gen füzyonları | $100$ Kilobaz (kb) | Bölünmeyen interfaze hücrelerde ve parafin blokta çalışır. **HER2 amplifikasyonu**, **ALK translokasyonu**, 22q11 delesyonu. |
| **Polimeraz Zincir Reaksiyonu (PCR / RT-PCR)** | Tekil gen mutasyonları, delesyonlar ve füzyon transkriptleri | Tek baz düzeyi | *BCR-ABL* füzyon transkripti kantitasyonu, *BRAF V600E* nokta mutasyonu. |
| **Yeni Nesil Dizileme (NGS - Next Generation Sequencing)** | **Milyonlarca DNA parçasının aynı anda paralel dizilenmesi** | **Tek baz düzeyinde tüm ekzom veya yüzlerce genlik paneller** | **Kanserde kapsamlı genomik profilleme**: Akciğer, kolon ve melanomda eşzamanlı onlarca hedeflenebilir onkogen taraması; likit biyopside dolaşan tümör DNA'sı (ctDNA). |

### 3. Hedefe Yönelik Tedavi (Hassas Tıp) Örnekleri

- **Akciğer Adenokarsinomu**: *EGFR* mutasyonu varsa -> Tirozin kinaz inhibitörü (Osimertinib); *ALK* veya *ROS1* translokasyonu varsa -> Krizotinib/Alektinib.
- **Meme Kanseri**: FISH ile *HER2* gen amplifikasyonu saptanırsa -> Trastuzumab (Herceptin).
- **Malign Melanom**: *BRAF V600E* mutasyonu varsa -> Vemurafenib / Dabrafenib.
- **Kolorektal Karsinom**: *KRAS* veya *NRAS* mutant ise anti-EGFR (Setuksimab) tedavisi **YANITSIZDIR** (ilaç direnci belirteci).
""",
        "spotPearls": [
            "▸ **Floresan İn Situ Hibridizasyon (FISH)** parafin bloktaki fikse dokularda ve bölünmeyen hücrelerde *HER2* amplifikasyonu veya *ALK* translokasyonunu saptayan altın standart sitogenetik yöntemdir.",
            "🔴 ÖNEMLİ: **Yeni Nesil Dizileme (NGS)**, tek bir biyopside yüzlerce onkogeni (EGFR, ALK, KRAS, BRAF vb.) paralel olarak tarayarak hedefe yönelik tedavi rehberliği sunar.",
            "🔵 ÇIKMIŞ SORU: Kolon kanserinde anti-EGFR monoklonal antikor (Setuksimab) tedavisinin işe yaramayacağını gösteren negatif prediktif belirteç **KRAS gen mutasyonu**dur."
        ],
        "coreContent": [
            {"title": "FISH Teknolojisi", "description": "Floresan problarla gen duplikasyon veya translokasyonlarını doğrudan mikroskopta sayma.", "highYieldBadge": "Sitogenetik", "details": "Meme kanserinde HER2 amplifikasyonu teyidi için şarttır."},
            {"title": "Yeni Nesil Dizileme (NGS)", "description": "Büyük ölçekli paralel dizileme ile kapsamlı tümör gen haritalaması.", "highYieldBadge": "Onkolojik Standart", "details": "Tümör mutasyon yükü (TMB) ve mikrosatellit instabiliteyi (MSI) de ölçer."},
            {"title": "Likit Biyopsi (ctDNA)", "description": "Kandan dolaşan serbest tümör DNA'sının taranması.", "highYieldBadge": "Girişimsel Olmayan", "details": "Tedavi direnci mutasyonlarını (T790M) yakalamada kullanılır."}
        ],
        "flashcards": [
            {"id": "fc-gp-47", "front": "Meme kanseri dokusunda HER2 gen amplifikasyonunu doğrulamada kullanılan en güvenilir moleküler sitogenetik yöntem nedir?", "back": "Floresan İn Situ Hibridizasyon (FISH).", "tag": "Moleküler Patoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-48", "front": "Metastatik kolorektal karsinomda anti-EGFR (Setuksimab) tedavisinin etkisiz olacağını gösteren kilit mutasyon hangisidir?", "back": "KRAS (ve NRAS) gen mutasyonları.", "tag": "Hedefe Yönelik Tedavi", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-24",
                "question": "İleri evre akciğer adenokarsinomu tanısı alan bir hastada, tek bir doku kesiti kullanılarak EGFR ekzon mutasyonları, ALK füzyonları, ROS1 translokasyonları, BRAF V600E ve KRAS mutasyonlarının tamamını aynı anda paralel olarak taramak için seçilmesi gereken en güncel ve kapsamlı moleküler patoloji yöntemi hangisidir?",
                "options": [
                    "A) Standart G-Bantlama Karyotipi",
                    "B) Western Blot analizi",
                    "C) Yeni Nesil Dizileme (Next Generation Sequencing - NGS)",
                    "D) Serum protein elektroforezi",
                    "E) Klasik Agaroz Jel Elektroforezi"
                ],
                "correctAnswer": "C",
                "explanation": "Yeni Nesil Dizileme (NGS), milyonlarca DNA parçasını eşzamanlı olarak dizileyerek yüzlerce geni kapsayan multigen onkoloji panelleriyle hedeflenebilir tüm mutasyonları tek seferde ortaya koyan altın standart moleküler araçtır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kanser dokusunda Mikrosatellit İnstabilite (MSI-High) saptandığında immün kontrol noktası inhibitörlerine (anti-PD1 / Pembrolizumab) yanıt neden olağanüstü yüksektir?",
            "Likit biyopside dolaşan tümör hücreleri (CTC) ile dolaşan serbest tümör DNA'sı (ctDNA) arasındaki fark nedir?"
        ]
    }
]

# Merge slides into complete 24 slides
all_slides = first_12_slides + slides_13_to_24
print(f"Total merged slides: {len(all_slides)}")

# Build Deck Object
deck_obj = {
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
    "slides": all_slides,
    "totalSlides": len(all_slides),
    "matchedPastQuestionsCount": 24
}

# Update interactive_learning_decks.json
decks_path = "src/data/interactive_learning_decks.json"
with open(decks_path, "r", encoding="utf-8") as f:
    decks = json.load(f)

existing_idx = next((i for i, d in enumerate(decks) if d["id"] == DECK_ID), None)
if existing_idx is not None:
    print(f"Updating existing deck at index {existing_idx}...")
    decks[existing_idx] = deck_obj
else:
    print("Appending new deck to interactive_learning_decks.json...")
    decks.append(deck_obj)

with open(decks_path, "w", encoding="utf-8") as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)
print("interactive_learning_decks.json successfully updated! Total decks now:", len(decks))

# Extract all practice questions from this deck
new_questions = []
for s in all_slides:
    for q in s.get("relatedQuestions", []):
        q_copy = dict(q)
        q_copy["deckId"] = DECK_ID
        q_copy["slideNumber"] = s["slideNumber"]
        q_copy["discipline"] = DISCIPLINE
        q_copy["committee"] = COMMITTEE
        new_questions.append(q_copy)

print(f"Total practice questions generated: {len(new_questions)}")

# Chunking logic:
# chunk_7 currently has 95 questions. Fill chunk_7 up to 100 (5 questions).
# Remaining 19 questions go into chunk_8.json!
study_dir = "src/data/study_questions"
chunk_7_path = os.path.join(study_dir, "chunk_7.json")
with open(chunk_7_path, "r", encoding="utf-8") as f:
    chunk_7 = json.load(f)

# Filter out old questions from this deck if any
chunk_7 = [q for q in chunk_7 if q.get("deckId") != DECK_ID]
space_in_chunk_7 = 100 - len(chunk_7)
fill_to_7 = min(space_in_chunk_7, len(new_questions))

chunk_7.extend(new_questions[:fill_to_7])
remaining_for_8 = new_questions[fill_to_7:]

with open(chunk_7_path, "w", encoding="utf-8") as f:
    json.dump(chunk_7, f, ensure_ascii=False, indent=2)
print(f"chunk_7.json updated! Now contains {len(chunk_7)} questions.")

# chunk_8.json
chunk_8_path = os.path.join(study_dir, "chunk_8.json")
chunk_8 = []
if os.path.exists(chunk_8_path):
    with open(chunk_8_path, "r", encoding="utf-8") as f:
        chunk_8 = json.load(f)
chunk_8 = [q for q in chunk_8 if q.get("deckId") != DECK_ID]
chunk_8.extend(remaining_for_8)

with open(chunk_8_path, "w", encoding="utf-8") as f:
    json.dump(chunk_8, f, ensure_ascii=False, indent=2)
print(f"chunk_8.json updated! Contains {len(chunk_8)} questions.")

# Update index.json
index_path = os.path.join(study_dir, "index.json")
with open(index_path, "r", encoding="utf-8") as f:
    index_data = json.load(f)

# Ensure chunk_8 is in chunks list
has_c8 = any(ch["chunkId"] == "chunk_8" for ch in index_data["chunks"])
if not has_c8:
    index_data["chunks"].append({
        "chunkId": "chunk_8",
        "filename": "chunk_8.json",
        "questionCount": len(chunk_8),
        "decksCovered": [DECK_ID],
        "disciplines": [DISCIPLINE]
    })

# Update counts
total_q = 0
for ch in index_data["chunks"]:
    ch_path = os.path.join(study_dir, ch["filename"])
    if os.path.exists(ch_path):
        with open(ch_path, "r", encoding="utf-8") as cf:
            data = json.load(cf)
            ch["questionCount"] = len(data)
            total_q += len(data)
            if ch["chunkId"] in ["chunk_7", "chunk_8"]:
                if DECK_ID not in ch["decksCovered"]:
                    ch["decksCovered"].append(DECK_ID)

index_data["totalQuestions"] = total_q
index_data["totalChunks"] = len(index_data["chunks"])

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

print(f"study_questions/index.json updated! Total questions: {total_q}, Total chunks: {len(index_data['chunks'])}")

# Update learning_batch_queue.json
queue_path = "src/data/learning_batch_queue.json"
with open(queue_path, "r", encoding="utf-8") as f:
    queue = json.load(f)

for item in queue:
    if item["id"] == DECK_ID:
        item["status"] = "completed"
        item["slidesCount"] = len(all_slides)
        item["detailLevel"] = "500%"

# Mark next lecture in Kurul 1: "12) Tromboz Patofizyolojisi.txt" or "13) Emboli,enfarktüs ve şok.txt"
# Let's check what's in queue
has_next = any(item.get("status") == "next_in_queue" for item in queue)
if not has_next:
    queue.append({
        "id": "learn-tromboz-patofizyolojisi-tam",
        "title": "Tromboz Patofizyolojisi ve Damar Tıkanıklıkları",
        "discipline": "Tıbbi Patoloji",
        "status": "next_in_queue",
        "slidesCount": 24,
        "detailLevel": "500% (Planlanan)"
    })

with open(queue_path, "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print("learning_batch_queue.json updated! Deck marked as completed.")
