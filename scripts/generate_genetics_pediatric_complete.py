# -*- coding: utf-8 -*-
"""
generate_genetics_pediatric_complete.py
Master builder for 'learn-genetik-pediatrik-cevresel-patoloji' (Kurul 1).
Prof. Dr. Hikmet Keleş & Robbins 11th edition.
Constructs:
1. 24 high-yield slides with structured spot pearls, flashcards, core content, practice questions
2. 30 comprehensive medical encyclopedia records with differential diagnosis
3. 30 matching medical glossary items
4. Chunked study questions appended (chunk_7 up to 100, spillover to chunk_8)
5. Updating learning_batch_queue.json
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

slides = [
    # SLIDE 1
    {
        "slideNumber": 1,
        "title": "İnsan Genomu Mimarisi, Kodlamayan DNA ve Genomik Çeşitlilik",
        "subtitle": "Protein Kodlayan %1.5 vs. Kodlamayan %98.5, Promotorlar, Enhancerlar ve lncRNA",
        "badge": "Genom Mimarisi",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. İnsan Genomunun Büyüklüğü ve 'Karanlık Madde'

İnsan genomu yaklaşık **3.2 milyar baz çifti** içerir. Geleneksel görüşün aksine, bu devasa dizinin yalnızca **yaklaşık %1.5'i** protein kodlayan ekzonlardan (yaklaşık 20.000 protein kodlayan gen) oluşur. 

Geriye kalan **%98.5'lik kısım** eskiden 'çöp DNA (junk DNA)' sanılan, ancak günümüzde gen ifadesini, kromatini ve hücresel kaderi yönettiği anlaşılan **kodlamayan DNA (non-coding DNA)** bölgeleridir.

```
+-----------------------------------------------------------------------------------+
|                        İNSAN GENOMUNUN İŞLEVSEL BÖLÜNMESİ                         |
+-----------------------------------------------------------------------------------+
| 1. Protein Kodlayan Genler (~%1.5)  : Enzimler, yapısal proteinler, reseptörler.  |
| 2. Kodlamayan Düzenleyici DNA (~%98.5):                                           |
|    - Promotor ve Enhancer Bölgeleri : Transkripsiyon faktörlerinin bağlandığı yer.|
|    - Kodlamayan RNA'lar (ncRNA)     : MikroRNA (miRNA), uzun kodlamayan RNA       |
|                                       (lncRNA), snRNA ve piRNA.                   |
|    - Yapısal Genomik Elemanlar      : Telomerler (kromozom uçları) ve             |
|                                       Sentromerler (iğ ipliği tutunma bölgeleri). |
|    - Tekrarlayan Sekanslar          : Transpozonlar, mikrosatellitler.            |
+-----------------------------------------------------------------------------------+
```

### 2. MikroRNA (miRNA) ve Uzun Kodlamayan RNA (lncRNA)

- **miRNA**: 21-23 nükleotidlik küçük tek iplikli RNA'lardır. Hedef mRNA'nın 3'-UTR bölgesine bağlanarak translasyonunu baskılar veya mRNA'yı yıkar (**post-transkripsiyonel gen susturması**). Kanserlerde tümör süpresör veya onkogen (*oncomiR*) gibi davranabilirler.
- **lncRNA**: >200 nükleotid uzunluğundaki RNA'lardır. Kromatin yeniden modellenmesini sağlar; en ünlü örneği kadınlarda inaktif X kromozomunu kaplayarak susturan **XIST** RNA'sıdır.
""",
        "spotPearls": [
            "▸ İnsan genomunun yalnızca **yaklaşık %1.5'i** protein kodlayan ekzonlardan oluşur; %98.5'i düzenleyici kodlamayan DNA'dır.\n  ▫ Kodlamayan DNA'daki polimorfizmler hastalık yatkınlıklarının büyük kısmını açıklar.",
            "🔴 ÖNEMLİ: **MikroRNA (miRNA)** post-transkripsiyonel düzeyde hedef mRNA'ya bağlanarak translasyonu inhibe eder veya mRNA'yı yıkar.\n  ▫ Kadınlarda embriyonik dönemde iki X kromozomundan birinin epigenetik olarak susturulmasını sağlayan en kritik lncRNA **XIST**'tir.",
            "🔵 ÇIKMIŞ SORU: *'İnsan genomunda protein kodlamayan ancak hedef mRNA'ların 3'-UTR bölgesine bağlanarak protein sentezini engelleyen küçük düzenleyici RNA'lar hangisidir?'*\n  ▫ Doğru yanıt: **MikroRNA (miRNA)**'dır."
        ],
        "coreContent": [
            {"title": "Protein Kodlayan %1.5", "description": "20.000 protein kodlayan genden oluşan fonksiyonel ekzon havuzu.", "highYieldBadge": "Ekzon", "details": "Klasik Mendel genetiği mutasyonlarının büyük kısmı bu bölgededir."},
            {"title": "miRNA Susturması", "description": "mRNA translasyonel represyonu ve yıkımı.", "highYieldBadge": "Post-transkripsiyonel", "details": "Dicer enzimi tarafından olgunlaştırılır ve RISC kompleksiyle çalışır."},
            {"title": "XIST lncRNA", "description": "X inaktivasyonunu (Lyonizasyon) yöneten uzun kodlamayan RNA.", "highYieldBadge": "Epigenetik", "details": "Kromatin heterokromatizasyonunu tetikleyerek Barr cisimciği oluşturur."}
        ],
        "flashcards": [
            {"id": "fc-gp-01", "front": "İnsan genomunda protein kodlayan genlerin tüm genoma oranı yaklaşık yüzde kaçtır?", "back": "Yaklaşık %1.5'tir (kalan %98.5 kodlamayandır).", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-02", "front": "Dişi memelilerde ikinci X kromozomunun inaktivasyonunu sağlayan lncRNA hangisidir?", "back": "XIST (X-inactive specific transcript).", "tag": "Moleküler Biyoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-01",
                "question": "Hücrede transkribe edildikten sonra sitoplazmada Dicer enzimi ile işlenen, RISC kompleksi içine girerek hedef mRNA'ların 3' translasyona uğramayan bölgesine (3'-UTR) bağlanan ve protein sentezini baskılayan yaklaşık 22 nükleotidlik düzenleyici molekül hangisidir?",
                "options": [
                    "A) Ribozomal RNA (rRNA)",
                    "B) Transfer RNA (tRNA)",
                    "C) MikroRNA (miRNA)",
                    "D) Küçük nükleer RNA (snRNA)",
                    "E) Heterojen nükleer RNA (hnRNA)"
                ],
                "correctAnswer": "C",
                "explanation": "miRNA'lar yaklaşık 22 nükleotidlik tek iplikli kodlamayan RNA'lardır. Dicer ile işlenip RISC kompleksine yüklenir ve hedef mRNA'nın translasyonunu durdurarak post-transkripsiyonel susturma yaparlar.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "miRNA ile siRNA arasındaki biyosentez ve hedef özgüllüğü farkı nedir?",
            "LncRNA'ların kromatin yeniden modellenmesindeki iskele (scaffold) görevi nasıl çalışır?"
        ]
    },

    # SLIDE 2
    {
        "slideNumber": 2,
        "title": "Genetik Varyasyonlar: Tek Nükleotid Polimorfizmi (SNP) ve Kopya Sayısı (CNV)",
        "subtitle": "İki İnsan Arasındaki %0.5'lik Fark, GWAS Çalışmaları ve Genomik Dengesizlikler",
        "badge": "Varyasyon Tipleri",
        "badgeColor": "sky",
        "synthesisNarrative": """### 1. Bireyler Arasındaki Genetik Çeşitlilik

Herhangi iki akraba olmayan insanın genomik DNA dizisi **%99.5 oranında tamamen özdeştir**. Bireyleri birbirinden farklı kılan, hastalıklara yatkınlıklarını, ilaç metabolizma hızlarını ve fiziksel özelliklerini belirleyen kısım geriye kalan **%0.5'lik varyasyondur**.

Bu çeşitliliğin iki ana yapıtaşı vardır:
1. **Tek Nükleotid Polimorfizmleri (SNP - Single Nucleotide Polymorphism)**
2. **Kopya Sayısı Varyasyonları (CNV - Copy Number Variation)**

```
+-----------------------------------------------------------------------------------+
|                        SNP ve CNV KARŞILAŞTIRMA TABLOSU                           |
+-----------------------------------------------------------------------------------+
| Özellik          | Tek Nükleotid Polimorfizmi (SNP) | Kopya Sayısı Varyasyonu (CNV) |
| :---             | :---                             | :---                          |
| Boyut            | Tek bir baz çifti (örn: A -> G)  | 1 kilobaz (1000 bp) - megabazlar|
| Popülasyon Sıklığı| Popülasyonda > %1 sıklıkta       | Değişken (delesyon / duplikasyon)|
| Sayıca Dağılım   | Genomda ~10 milyon SNP bulunur   | Genomik varyasyonun baz olarak|
|                  | (En yaygın varyasyon türüdür!)   | %50'sinden fazlasını oluşturur|
| Konum            | %99'u kodlamayan DNA'da          | Genleri tamamen kapsayabilir  |
| Klinik Anlam     | Multifaktöryel hastalıklara      | Otizm, şizofreni, mikrodelesyon|
|                  | yatkınlık (GWAS belirteçleri)    | sendromları, gen dozaj etkisi |
+-----------------------------------------------------------------------------------+
```

### 2. Genom Boyu İlişkilendirme Çalışmaları (GWAS)

GWAS analizlerinde yüz binlerce hastanın SNP profilleri taranarak diyabet, hipertansiyon, Alzheimer veya kanser gibi karmaşık poligenik hastalıklara yatkınlık sağlayan risk alelleri haritalanır. Bir SNP kodlayan bölgede ise amino asit değişimine yol açabilir (nonsynonymous) ya da proteini değiştirmeyebilir (synonymous).
""",
        "spotPearls": [
            "▸ İnsan genomundaki en sık genetik çeşitlilik biçimi **Tek Nükleotid Polimorfizmleridir (SNP)**; genomda 10 milyondan fazla SNP tanımlanmıştır.\n  ▫ Bir varyasyonun polimorfizm sayılması için toplumda **en az %1 sıklıkta** bulunması gerekir.",
            "🔴 ÖNEMLİ: **Kopya Sayısı Varyasyonları (CNV)** 1 kilobazdan büyük genomik parçaların delesyonu veya duplikasyonudur; toplam baz çifti sayısı açısından insanlar arasındaki çeşitliliğin yarısından fazlasını oluşturur.",
            "🔵 ÇIKMIŞ SORU: *'İnsan genomunda tek bazlık değişimlerle karakterize olan ve multifaktöryel hastalıkların genetik zeminini aydınlatan GWAS çalışmalarında kullanılan en yaygın varyasyon tipi hangisidir?'*\n  ▫ Doğru yanıt: **Tek Nükleotid Polimorfizmi (SNP)**'dir."
        ],
        "coreContent": [
            {"title": "SNP (Tek Baz)", "description": "Her 1000 baz çiftinde bir rastlanan en yaygın genomik varyasyon.", "highYieldBadge": "En Yaygın", "details": "Toplumda sıklığı %1'in üzerindedir; GWAS analizlerinin temelidir."},
            {"title": "CNV (Kopya Sayısı)", "description": "Büyük DNA segmentlerinin delesyon veya amplifikasyonu.", "highYieldBadge": "Yapısal Varyasyon", "details": "Otizm, şizofreni ve gen dozaj hastalıklarında belirleyicidir."},
            {"title": "Eşlenik Olmayan (Nonsynonymous) SNP", "description": "Kodonda amino asit değişimine neden olan tek baz mutasyonu.", "highYieldBadge": "Protein Etkisi", "details": "Orak hücre anemisi (Glu -> Val) en bilinen örnektir."}
        ],
        "flashcards": [
            {"id": "fc-gp-03", "front": "Genomda en sık rastlanan ve GWAS çalışmalarında kullanılan genetik varyasyon tipi nedir?", "back": "Tek Nükleotid Polimorfizmi (SNP).", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-04", "front": "Kopya Sayısı Varyasyonu (CNV) tanımlaması için DNA segmentinin minimum boyutu ne kadar olmalıdır?", "back": "En az 1 kilobaz (1000 baz çifti) veya daha büyük olmalıdır.", "tag": "Sitogenetik", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-02",
                "question": "Aşağıdaki genetik varyasyon türlerinden hangisi insan genomunda sayısal olarak en sık rastlanan, bireyler arasında her 1000 bazda bir görülen ve multifaktöryel hastalıklara yatkınlığı haritalamada kullanılan tek bazlık değişimdir?",
                "options": [
                    "A) Kopya Sayısı Varyasyonu (CNV)",
                    "B) Tek Nükleotid Polimorfizmi (SNP)",
                    "C) Dengeli Translokasyon",
                    "D) Halka Kromozom",
                    "E) İzokromozom"
                ],
                "correctAnswer": "B",
                "explanation": "Tek Nükleotid Polimorfizmleri (SNP), genomda 10 milyondan fazla bulunan ve her 1000 bazda bir rastlanan en sık varyasyon biçimidir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Bir SNP'nin GWAS analizinde hastalıkla ilişkili çıkması doğrudan nedensel (causal) mutasyon olduğunu kanıtlar mı?",
            "CNV'lerin mikrodelesyon sendromlarındaki (örn. DiGeorge, Williams) rolü nedir?"
        ]
    },

    # SLIDE 3
    {
        "slideNumber": 3,
        "title": "Epigenetik Düzenleme: DNA Metilasyonu, Histon Kodu ve Kromatin",
        "subtitle": "DNA Dizisini Değiştirmeden Gen İfadesini Yönetme, CpG Adacıkları ve Susturma",
        "badge": "Epigenetik",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Epigenetik Nedir?

**Epigenetik**, DNA birincil nükleotid dizisinde hiçbir değişiklik olmaksızın, gen ifadesinde ve kromatin yapısında meydana gelen kalıtılabilir değişikliklerdir. Bir nöron ile bir hepatosit tamamen aynı DNA dizisine sahip olmasına rağmen, epigenetik modifikasyonlar sayesinde tamamen farklı protein setleri üretir.

### 2. Temel Epigenetik Mekanizmalar

1. **DNA Metilasyonu**:
   - Genellikle gen promotor bölgelerindeki **CpG adacıklarında** sitozin bazlarına metil grubu ($–CH_3$) eklenmesidir (DNA Metiltransferaz - DNMT enzimleri).
   - **Kural**: **DNA hipermetilasyonu kromatini yoğunlaştırır ve transkripsiyonu SUSTURUR (Gen susturması)**. Kanserlerde tümör süpresör gen promotorlarının hipermetilasyonu sık bir inaktivasyon yoludur.

2. **Histon Modifikasyonları ('Histon Kodu')**:
   - **Histon Asetilasyonu (HAT)**: Pozitif yüklü lizinleri nötralize eder, nükleozomlar gevşer, kromatin açılır (**Ökromatin**) -> **Transkripsiyon AKTİF** hale gelir.
   - **Histon Deasetilasyonu (HDAC)**: Asetil gruplarını söker, kromatin sıkılaşır (**Heterokromatin**) -> **Transkripsiyon BASKILANIR**.
   - **Histon Metilasyonu**: Modifiye edilen lizin amino asidine göre geni aktive edebilir veya susturabilir (örn: H3K9 metilasyonu susturur, H3K4 metilasyonu aktive eder).

3. **Genomik Damgalama (İmprinting)**:
   - Maternal veya paternal alelin sperm ya da oosit oluşumu sırasında metillenerek epigenetik olarak susturulmasıdır (Prader-Willi ve Angelman sendromları).
""",
        "spotPearls": [
            "▸ **DNA Metilasyonu Kuralı**: Promotor CpG adacıklarının metillenmesi transkripsiyon faktörlerinin bağlanmasını engelleyerek **geni SUSTURUR (inaktive eder)**.\n  ▫ DNA hipometilasyonu ise transkripsiyonu uyarabilir veya genomik instabiliteye yol açabilir.",
            "🔴 ÖNEMLİ: **Histon Asetiltransferaz (HAT)** kromatini gevşeterek **ökromatine** çevirir ve transkripsiyonu açar; **Histon Deasetilaz (HDAC)** ise kromatini sıkıştırıp **heterokromatin** yaparak geni susturur.",
            "🔵 ÇIKMIŞ SORU: *'Kanser hücrelerinde tümör süpresör gen promotor bölgelerinde izlenen ve genin sessizleşmesine yol açan temel epigenetik değişiklik hangisidir?'*\n  ▫ Doğru yanıt: **DNA Hipermetilasyonu**'dur."
        ],
        "coreContent": [
            {"title": "DNA Metilasyonu", "description": "Sitozin bazlarına metil eklenmesiyle gen ifadesinin susturulması.", "highYieldBadge": "Gen Susturma", "details": "DNMT enzimleri yönetir; CpG adacıkları kilit hedeftir."},
            {"title": "Histon Asetilasyonu (HAT)", "description": "Kromatinin açılması (ökromatin) ve gen ifadesinin başlaması.", "highYieldBadge": "Transkripsiyon Açık", "details": "Lizin kalıntılarının asetillenmesi nükleozom gevşemesini sağlar."},
            {"title": "Genomik İmprinting", "description": "Gametogenezde bir ebeveyn alelinin metilasyonla kalıcı susturulması.", "highYieldBadge": "Ebeveyne Özgü", "details": "15q11-q13 bölgesinde Prader-Willi ve Angelman klinik ayrımını yapar."}
        ],
        "flashcards": [
            {"id": "fc-gp-05", "front": "Gen promotor bölgesindeki CpG adacıklarının hipermetilasyonu gen ifadesini nasıl etkiler?", "back": "Transkripsiyonu baskılar (geni susturur).", "tag": "Epigenetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-06", "front": "Histonları asetilleyerek kromatini transkripsiyona açık (ökromatin) hale getiren enzim nedir?", "back": "Histon Asetiltransferaz (HAT).", "tag": "Biyokimya", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-03",
                "question": "Bir tümör hücresinde p16 (CDKN2A) tümör süpresör gen dizisinde hiçbir delesyon veya nokta mutasyonu saptanmamasına rağmen proteinin hiç üretilmediği görülüyor. Promotor bölgesinin incelenmesinde CpG adacıklarında aşırı metilasyon tespit ediliyor. Bu gen susturma mekanizması aşağıdakilerden hangisidir?",
                "options": [
                    "A) Reseptör Düzenlemesi",
                    "B) Nonsense Mutasyon",
                    "C) Epigenetik Susturma (DNA Hipermetilasyonu)",
                    "D) Alternatif Splicing",
                    "E) Gen Amplifikasyonu"
                ],
                "correctAnswer": "C",
                "explanation": "DNA dizisi değişmeden promotor CpG adacıklarının metillenmesi sonucu genin inaktive olması klasik epigenetik susturma (DNA hipermetilasyonu) mekanizmasıdır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "HDAC inhibitörü antikanser ilaçların (örn. Vorinostat) etki mekanizması nedir?",
            "Prader-Willi ile Angelman sendromundaki mikrodelesyon ve uniparental dizomi farkı nedir?"
        ]
    },

    # SLIDE 4
    {
        "slideNumber": 4,
        "title": "Mendel Tipi Tek Gen Bozuklukları ve Otozomal Dominant Kalıtım",
        "subtitle": "Vertikal Geçiş, %50 Risk, Yapısal Proteinler ve 'Dominant Negatif' Etki",
        "badge": "Mendel Kalıtımı",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Tek Gen Bozuklukları (Mendel Kalıtımı)

İnsan hastalıklarının yaklaşık %1'i tek bir gendeki yüksek penetranslı mutasyonlardan kaynaklanır. Klasik Mendel kalıtım kurallarına (Otozomal Dominant, Otozomal Resesif, X'e Bağlı) uyarlar.

### 2. Otozomal Dominant (OD) Hastalıkların Kardinal Özellikleri

1. **Heterozigot Bireyde Fenotip Görülür**: Tek bir mutant alel varlığı hastalığın ortaya çıkması için yeterlidir ($Aa$).
2. **Vertikal Geçiş**: Her nesilde hastalık izlenir; kuşak atlamaz. Etkilenen ebeveynin her gebelikte çocuğuna hastalığı aktarma riski **%50'dir**.
3. **Cinsiyet Ayrımı Yoktur**: Otozomal kromozomlarda taşındığı için kız ve erkek çocuklarda eşit sıklıkta görülür.
4. **Değişken Ekspresyon ve Eksik Penetrans**: Aynı mutasyonu taşıyan aile bireylerinde klinik ağırlık farklı olabilir (değişken ekspresyon) ya da mutant geni taşıyan bazı bireyler klinik olarak tamamen sağlıklı görünebilir (eksik penetrans).
5. **Geç Başlangıçlılık**: Birçok OD hastalık erişkin yaşta semptom verir (Huntington hastalığı, Polikistik Böbrek Hastalığı).

### 3. Etkilenen Protein Tipleri

- **Yapısal Proteinler**: Kollajen, fibrillin (Marfan, Ehlers-Danlos, Osteogenezis İmperfekta).
- **Reseptörler ve Taşıyıcılar**: LDL reseptörü (Ailesel Hiperkolesterolemi).
- **Dominant Negatif Etki**: Mutant protein sağlam alelin ürettiği normal proteinle multimer oluşturup normal proteinin de işlevini bozar.
""",
        "spotPearls": [
            "▸ **Otozomal Dominant Kuralı**: Tek bir mutant alel ($Aa$) fenotipi oluşturur; etkilenen ebeveynin çocuğuna geçiş riski her gebelikte **%50**'dir.\n  ▫ Kuşak atlamaz (vertikal geçiş gösterir).",
            "🔴 ÖNEMLİ: OD mutasyonlar sıklıkla **yapısal proteinleri (kollajen, fibrillin)** veya **hücre yüzey reseptörlerini (LDL-R)** etkiler; enzim defektleri ise kural olarak OD DEĞİL, resesiftir!",
            "🔵 ÇIKMIŞ SORU: *'Hangisi otozomal dominant kalıtım özelliği gösteren yapısal bağ dokusu hastalığıdır?'* sorusunun prototipleri **Marfan Sendromu** ve **Osteogenezis İmperfekta**'dır."
        ],
        "coreContent": [
            {"title": "Vertikal Kalıtım", "description": "Her jenerasyonda etkilenen birey görülür; kuşak atlamaz.", "highYieldBadge": "Soyağacı", "details": "Kız ve erkek çocuklarda risk eşittir (%50)."},
            {"title": "Dominant Negatif Etki", "description": "Anormal proteinin sağlam proteinin fonksiyonunu da zehirlemesi.", "highYieldBadge": "Moleküler Mekanizma", "details": "Kolajen ve fibrillin trimerlerinde sık görülür."},
            {"title": "Haployetmezlik", "description": "Normal tek alelin ürettiği %50 proteinin vücuda yetmemesi durumu.", "highYieldBadge": "Dozaj", "details": "Ailesel hiperkolesterolemi LDL reseptör eksikliğinde tipiktir."}
        ],
        "flashcards": [
            {"id": "fc-gp-07", "front": "Otozomal dominant hastalıklarda etkilenen heterozigot bir ebeveynin çocuğuna hastalığı geçirme olasılığı nedir?", "back": "%50 (1/2).", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-08", "front": "Otozomal dominant kalıtım kural olarak hangi tip proteinleri tutar: Enzimler mi, yapısal proteinler mi?", "back": "Yapısal proteinler ve reseptörleri tutar (enzim defektleri resesiftir).", "tag": "Genetik Kural", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-04",
                "question": "Aşağıdakilerden hangisi otozomal dominant kalıtım gösteren hastalıkların genel özelliklerinden biri DEĞİLDİR?",
                "options": [
                    "A) Kuşak atlamadan vertikal geçiş göstermesi",
                    "B) Etkilenen ebeveynin çocuğuna aktarma riskinin %50 olması",
                    "C) Sıklıkla metabolik enzim eksikliklerinden kaynaklanması",
                    "D) Değişken ekspresyon ve eksik penetrans görülebilmesi",
                    "E) Erkek ve kadın çocuklarda eşit oranda ortaya çıkması"
                ],
                "correctAnswer": "C",
                "explanation": "Metabolik enzim eksiklikleri kural olarak Otozomal Resesif kalıtılır; çünkü enzimlerin %50 aktivitesi normal homeostaz için genellikle yeterlidir. Otozomal dominant hastalıklar ise yapısal proteinler ve reseptör defektlerinden kaynaklanır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "De novo (yeni) mutasyonların otozomal dominant hastalıklardaki soyağacı görünümü nasıldır?",
            "Penetrans ile değişken ekspresyon (variable expressivity) kavramlarının ayırıcı farkı nedir?"
        ]
    },

    # SLIDE 5
    {
        "slideNumber": 5,
        "title": "Marfan Sendromu: Fibrillin-1 (FBN1) ve TGF-β Sinyal Yolağı",
        "subtitle": "15q21.1 Kromozomu, Mikrofibril İskelesi ve Kontrolsüz Büyüme Faktörü Aktivasyonu",
        "badge": "Marfan Moleküler",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Marfan Sendromu Nedir?

Marfan sendromu, bağ dokusunun elastik lif sistemini etkileyen, **otozomal dominant** geçişli multisistemik bir hastalıktır. Olguların %75-85'i aileseldir; %15-25'i ise yeni (*de novo*) germline mutasyonlarla ortaya çıkar.

### 2. Moleküler Defekt: Fibrillin-1 (*FBN1*) Geni

- **Lokus**: Kromozom **15q21.1**.
- **Fibrillin-1**: Hücre dışı matrikste elastik liflerin üzerine çöktüğü mikrofibrillerin temel yapısal glikoproteinidir. Aort duvarı, gözün silier ligamanları (zonülleri) ve kemik periostunda yoğun olarak bulunur.

```
Mutant FBN1 Geni (15q21.1)
           │
           ▼
Anormal veya Yetersiz Fibrillin-1 Proteini
  ┌────────┴────────────────────────────────────────┐
  ▼                                                 ▼
[ MEKANİK ZAYIFLIK ]                        [ TGF-β AŞIRI AKTİVASYONU ]
Elastik dokularda mikrofibril iskelesi       Normalde fibrillin-1 matrikste latent
çöker; doku gerilme direncini kaybeder.      TGF-β'yı bağlayarak hapseder. Fibrillin
  │                                          yokluğunda serbest TGF-β aşırı artar!
  ▼                                                 │
Aort Kökü Gerilir, Aort Yırtılır,                   ▼
Lens Zonülleri Kopar.                        Aşırı sinyal -> Matriks metalloproteinazlar
                                             salınır, kıkırdak ve elastik lifler erir,
                                             aşırı kemik uzaması uyarılır.
```

### 3. TGF-β Yolağının Klinik Önemi

Marfan sendromundaki doku hasarının yalnızca 'mekanik bir yıpranma' olmadığı; **kontrolsüz serbest TGF-β uyarımı** ile kıkırdak proliferasyonu ve vasküler elastolizisin tetiklendiği anlaşılmıştır. Bu nedenle TGF-β antagonistleri (örneğin Anjiyotensin Reseptör Blokörü olan **Losartan**) Marfan hastalarında aort dilatasyonunu yavaşlatmada klinik kullanıma girmiştir!
""",
        "spotPearls": [
            "▸ Marfan sendromu kromozom **15q21.1** üzerindeki **FBN1 (Fibrillin-1)** gen mutasyonuna bağlı otozomal dominant bir hastalıktır.",
            "🔴 ÖNEMLİ: Fibrillin-1 yalnızca yapısal iskele sağlamaz; aynı zamanda **TGF-β'yı bağlayarak inaktif tutar**. Mutasyonunda serbest TGF-β aşırı aktive olarak elastik dokuyu yıkar ve kemik uzamasını uyarır!",
            "🔵 ÇIKMIŞ SORU: *'Marfan sendromunda patolojiden sorumlu olan temel ekstrasellüler matriks glikoproteini hangisidir?'*\n  ▫ Doğru yanıt: **Fibrillin-1**'dir."
        ],
        "coreContent": [
            {"title": "FBN1 Mutasyonu", "description": "15q21.1 kromozomundaki fibrillin-1 geninde dominant mutasyon.", "highYieldBadge": "Kilit Gen", "details": "%75-85 ailesel, %15-25 de novo mutasyondur."},
            {"title": "TGF-Beta Aktivasyonu", "description": "Fibrillin tarafından tutulamayan serbest TGF-beta'nın doku hasarı yapması.", "highYieldBadge": "Patogenez Devrimi", "details": "Losartan gibi ARB ilaçlarının tedavi mantığını oluşturur."},
            {"title": "Mikrofibril Ağı", "description": "Elastin proteininin üzerine çöktüğü 10-12 nm'lik iskele fibrilleri.", "highYieldBadge": "Histoloji", "details": "Aort, lens asıcı bağları ve periostta bol bulunur."}
        ],
        "flashcards": [
            {"id": "fc-gp-09", "front": "Marfan sendromunda mutasyona uğrayan gen ve kodladığı protein nedir?", "back": "FBN1 geni; Fibrillin-1 proteini.", "tag": "Genetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-10", "front": "Marfan sendromunda doku elastolizisine ve aşırı kemik büyümesine yol açan kontrolsüz aktifleşen büyüme faktörü hangisidir?", "back": "Dönüştürücü Büyüme Faktörü-Beta (TGF-β).", "tag": "Patogenez", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-05",
                "question": "Marfan sendromunda fibrillin-1 gen kusurunun yanı sıra patogenezde rol oynayan ve elastik liflerin proteolitik yıkımını tetikleyen, aşırı sinyal iletimi gösteren sitokin/büyüme faktörü yolağı aşağıdakilerden hangisidir?",
                "options": [
                    "A) Epidermal Büyüme Faktörü (EGF)",
                    "B) Dönüştürücü Büyüme Faktörü-Beta (TGF-β)",
                    "C) Vasküler Endotelyal Büyüme Faktörü (VEGF)",
                    "D) İnterlökin-2 (IL-2)",
                    "E) Tümör Nekrozis Faktörü-Alfa (TNF-α)"
                ],
                "correctAnswer": "B",
                "explanation": "Normal fibrillin-1 molekülleri latent TGF-β'yı sekestre eder. Fibrillin-1 kusurunda kontrolsüz serbest kalan TGF-β, matriks metalloproteinaz aktivasyonuna ve elastik doku harabiyetine neden olur.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "FBN1 mutasyonu ile FBN2 mutasyonu (Konjenital kontraktürel araknodaktili) arasındaki fark nedir?",
            "Losartan ilacının Marfan aort dilatasyonunu engellemedeki TGF-beta blokaj mekanizması nasıldır?"
        ]
    },

    # SLIDE 6
    {
        "slideNumber": 6,
        "title": "Marfan Sendromu: Kardiyovasküler, Oküler ve İskelet Morfolojisi",
        "subtitle": "Kistik Medyal Nekroz, Aort Diseksiyonu, Ektopia Lentis ve Araknodaktili",
        "badge": "Marfan Morfoloji",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Marfan Sendromunda Üç Hedef Sistem

Marfan sendromunun klinik tanısı ve prognozu üç ana sistemin patolojilerine dayanır:

```
+-----------------------------------------------------------------------------------+
|                        MARFAN SENDROMU ÜÇLÜ SİSTEM TUTULUMU                       |
+-----------------------------------------------------------------------------------+
| 1. İSKELET SİSTEMİ:                                                               |
|    - Aşırı uzun boy, orantısız uzun ekstremiteler (kol açıklığı > boy).           |
|    - Araknodaktili (örümcek parmaklar; pozitif başparmak/Steinberg ve bilek/Walker|
|      belirtisi).                                                                  |
|    - Göğüs deformitesi: Pektus ekskavatum (kunduracı) veya karinatum (güvercin).   |
|    - Eklem laksisitesi ve skolyoz/kifoz. Yüksek damak kubbesi.                    |
|                                                                                   |
| 2. GÖZ (OKÜLER) BULGULARI:                                                        |
|    - Ektopia Lentis: Lensin asıcı bağlarının (silier zonüller) zayıflaması sonucu |
|      lensin bilateral YUKARI VE DIŞA (superior-temporal) lüksasyonu/sublüksasyonu.|
|                                                                                   |
| 3. KARDİYOVASKÜLER SİSTEM (EN ÖNEMLİ MORTALİTE NEDENİ!):                          |
|    - Aort Kökü Dilatasyonu: Aort anulusu genişler, aort yetmezliği gelişir.       |
|    - Kistik Medyal Nekroz: Aort tunika medyasında elastik lif parçalanması ve     |
|      boşluklarda asellüler glikozaminoglikan birikimi.                            |
|    - Aort Diseksiyonu ve Rüptürü: Marfan hastalarında EN SIK ÖLÜM NEDENİDİR!      |
|    - Mitral Kapak Prolapsusu (MVP): Miksamatöz dejenerasyonla 'floppy valve'.    |
+-----------------------------------------------------------------------------------+
```

### 2. Ektopia Lentis: Marfan vs. Homosistinüri Ayrımı

Komite ve TUS sınavlarının en sevilen klinikopatolojik ayrımıdır:
- **Marfan Sendromu**: Lens **YUKARI VE DIŞA (Yukarı-Dış)** lükse olur (Zonüllerde fibrillin-1 eksikliği).
- **Homosistinüri**: Lens **AŞAĞI VE İÇE (Aşağı-İç)** lükse olur (Sistationin beta-sentaz eksikliği; tromboz riski ve zeka geriliği eşlik eder).
""",
        "spotPearls": [
            "▸ Marfan sendromunda hastaların hayatını tehdit eden en önemli komplikasyon ve baş ölüm nedeni **Aort Kökü Diseksiyonu ve Rüptürü**dür.",
            "🔴 ÖNEMLİ: Aort duvarında elastik liflerin parçalanması ve amorf mukoid madde birikimiyle oluşan mikroskobik lezyona **Kistik Medyal Nekroz (Erdheim Hastalığı)** denir.",
            "🔵 ÇIKMIŞ SORU: Lens sublüksasyonu yönü:\n  ▫ **Marfan Sendromu**: **YUKARI VE DIŞA** lüksasyon.\n  ▫ **Homosistinüri**: **AŞAĞI VE İÇE** lüksasyon."
        ],
        "coreContent": [
            {"title": "Kistik Medyal Nekroz", "description": "Tunika medyadaki elastik liflerin fragmantasyonu ve mikoid birikim.", "highYieldBadge": "Aort Patolojisi", "details": "Aort yırtılması ve diseksiyonuna zemin hazırlar."},
            {"title": "Ektopia Lentis (Yukarı)", "description": "Bilateral lensin superior-temporal yer değiştirmesi.", "highYieldBadge": "Oküler Ayırıcı", "details": "Silier zonüller fibrillin-1 zenginidir."},
            {"title": "Araknodaktili", "description": "Aşırı uzun, ince örümcek parmaklar.", "highYieldBadge": "İskelet", "details": "Steinberg (başparmak avuçtan taşar) testi pozitiftir."}
        ],
        "flashcards": [
            {"id": "fc-gp-11", "front": "Marfan sendromlu hastaların en sık mortalite (ölüm) nedeni nedir?", "back": "Aort diseksiyonu ve rüptürüdür.", "tag": "Kardiyoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-12", "front": "Marfan sendromunda lens hangi yöne lükse olur?", "back": "Yukarı ve dışa (superior ve temporal).", "tag": "Göz Patolojisi", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-06",
                "question": "Aşırı uzun boylu, kol açıklığı boyundan uzun olan, pektus ekskavatum ve bilateral lensinde yukarı-dışa subluksasyon saptanan 19 yaşındaki basketbolcuda ani başlayan yırtıcı göğüs ağrısı sonrası ölüm gerçekleşiyor. Otopsinde çıkan aortta intimal yırtık ve perikardiyal tamponad saptanıyor. Aort duvarının mikroskobik incelemesinde saptanması en muhtemel patolojik lezyon hangisidir?",
                "options": [
                    "A) Dev hücreli aortit",
                    "B) Kistik medyal nekroz",
                    "C) Sifilitik endarterit obliterans",
                    "D) Mönckeberg medial kalsinozisi",
                    "E) Fibrinoid damar nekrozu"
                ],
                "correctAnswer": "B",
                "explanation": "Marfan sendromunda elastik tunika medyanın zayıflaması, elastik liflerin parçalanması ve amorf mukoid matriks birikimiyle karakterize Kistik Medyal Nekroz gelişir ve bu durum ölümcül aort diseksiyonuna yol açar.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kistik medyal nekroz tablosunda 'nekroz' kelimesi neden aslında gerçek bir hücresel nekrozu ifade etmez?",
            "Mitral kapak prolapsusundaki miksamatöz dejenerasyonun histokimyasal Alcian Blue boyanması nasıldır?"
        ]
    },

    # SLIDE 7
    {
        "slideNumber": 7,
        "title": "Otozomal Resesif Kalıtım ve Kistik Fibrozis (CFTR) Patogenezi",
        "subtitle": "Yatay Geçiş, %25 Risk, Enzim Defektleri, 7q31.2 ve Delta-F508 Mutasyonu",
        "badge": "Kistik Fibrozis",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. Otozomal Resesif (OR) Kalıtımın Genel İlkeleri

1. **Homozigot Bireyde Görülür**: Hastalığın ortaya çıkması için her iki alelin de mutant olması şarttır ($aa$).
2. **Yatay Geçiş**: Ebeveynler genellikle sağlıklı taşıyıcıdır ($Aa$). Hastalık kardeşlerde çıkar, önceki veya sonraki kuşaklarda görülmez (kuşak atlar). İki taşıyıcının her gebelikte hasta çocuk sahibi olma riski **%25 (1/4)**'tür.
3. **Akraba Evliliği Riski Artırır**: Nadir çekinik genlerin karşılaşma ihtimalini katlar.
4. **Metabolik Enzim ve Taşıyıcı Bozuklukları**: OR hastalıkların neredeyse tamamı enzim eksiklikleridir (örneğin fenilketonüri, lizozomal depo hastalıkları, kistik fibrozis).

### 2. Kistik Fibrozis (Mukovisidoz): En Sık Ölümcül OR Hastalık

Beyaz ırkta en sık görülen ölümcül otozomal resesif hastalıktır (taşıyıcılık sıklığı ~1/25).
- **Etkilenen Gen**: **CFTR** (Cystic Fibrosis Transmembrane Conductance Regulator).
- **Kromozom**: **7q31.2**.
- **En Sık Mutasyon**: **Delta-F508 ($\Delta$F508)** (Olguların %70'i). CFTR proteininin 508. pozisyonundaki **fenilalanin** amino asidinin delesyonudur.
- **Moleküler Mekanizma (Sınıf II Mutasyon)**: $\Delta$F508 mutasyonunda protein endoplazmik retikulumda anormal katlanır; kalite kontrol sistemince yakalanarak proteazomlarda yıkılır ve hücre zarına **HİÇ ULAŞAMAZ**!

### 3. CFTR Proteini Nedir?

CFTR, epitel hücre membranlarında yer alan **cAMP ile aktive olan bir klorür ($Cl^-$) kanalıdır**. Fonksiyonu epitelin tipine göre taban tabana zıttır (Slayt 8).
""",
        "spotPearls": [
            "▸ **Otozomal Resesif Kuralı**: Hastalık ancak homozigot ($aa$) durumda belirir; iki heterozigot taşıyıcı ebeveynin çocuğunda hastalık riski her gebelikte **%25**'tir.",
            "🔴 ÖNEMLİ: Kistik Fibrozis geni **CFTR**, kromozom **7q31.2** üzerindedir; en sık rastlanan mutasyon 508. pozisyonda fenilalanin delesyonu olan **Delta-F508 ($\Delta$F508)** mutasyonudur.",
            "🔵 ÇIKMIŞ SORU: *'Delta-F508 mutasyonunda CFTR proteini neden zarda bulunmaz?'*\n  ▫ Doğru yanıt: Anormal katlanan protein endoplazmik retikulumda yakalanır ve **proteazomlarda erken parçalanarak hücre zarına taşınamaz** (Sınıf II mutasyon)."
        ],
        "coreContent": [
            {"title": "OR Kalıtım Riski", "description": "İki taşıyıcı ebeveynden %25 hasta, %50 taşıyıcı, %25 sağlam çocuk doğar.", "highYieldBadge": "Kalıtım Riski", "details": "Akraba evliliği görülme sıklığını belirgin artırır."},
            {"title": "Delta-F508", "description": "Kistik fibroziste fenilalanin delesyonu ile seyreden en sık mutasyon (%70).", "highYieldBadge": "En Sık Mutasyon", "details": "Protein katlanma ve ER kalite kontrol defektidir."},
            {"title": "CFTR Kanalı", "description": "cAMP bağımlı ATP kasetli klorür iletim kanalı.", "highYieldBadge": "İyon Kanalı", "details": "Solunum, sindirim ve ter bezlerinde epitel iyon dengesini kurar."}
        ],
        "flashcards": [
            {"id": "fc-gp-13", "front": "Kistik fibrozis hastalığında en sık görülen genetik mutasyon nedir?", "back": "Delta-F508 (CFTR geninde 508. kodonda fenilalanin delesyonu).", "tag": "Moleküler Genetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-14", "front": "Delta-F508 mutasyonunda sentezlenen anormal CFTR proteini hücrede nerede yok edilir?", "back": "Endoplazmik retikulum kalite kontrolünden geçemez ve proteazomlarda yıkılır.", "tag": "Hücre Biyolojisi", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-07",
                "question": "Beyaz ırkta en sık görülen ölümcül otozomal resesif hastalık olan Kistik Fibrozis'in en yaygın mutasyonu olan Delta-F508'in hücresel patogenezi aşağıdakilerden hangisidir?",
                "options": [
                    "A) Hücre zarında klor kanalının açılmasını engelleyen sinyal iletim kusuru",
                    "B) mRNA sentezinin hiç yapılamaması (null mutasyon)",
                    "C) Protein katlanma kusuru nedeniyle endoplazmik retikulumda yıkılması ve zara ulaşamaması",
                    "D) Klor kanalının klor yerine bikarbonat geçirmeye başlaması",
                    "E) Aşırı aktifleşerek hücre içine aşırı klor pompalaması"
                ],
                "correctAnswer": "C",
                "explanation": "Delta-F508 mutasyonunda amino asit delesyonu proteinin anormal katlanmasına neden olur; protein endoplazmik retikulumda kalite kontrol mekanizmasınca tutulur, proteazomlarda yıkılır ve apikal membrana hiç ulaşamaz (Sınıf II taşıma kusuru).",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "CFTR mutasyon sınıflaması (Sınıf I'den Sınıf VI'ya) patolojik ve farmakolojik olarak nasıl ayrılır?",
            "İvakaftor (Ivacaftor) ve Lumakaftor (Lumacaftor) ilaçlarının moleküler etki basamakları nelerdir?"
        ]
    },

    # SLIDE 8
    {
        "slideNumber": 8,
        "title": "Kistik Fibrozis: Doku Özgül İyon Taşınması ve Organ Patolojileri",
        "subtitle": "Solunum/Bağırsak vs. Ter Bezi Zıtlığı, Pseudomonas Bronşiektazisi ve Mekonyum İleusu",
        "badge": "CFTR Patofizyoloji",
        "badgeColor": "sky",
        "synthesisNarrative": """### 1. Doku Özgül İyon Taşınmasındaki Büyük Zıtlık

CFTR klorür kanalının fonksiyonu dokuya göre tam tersi yönde çalışır:

| Doku Tipi | Normal CFTR Görevi | Kistik Fibroziste Kusur | Sonuç ve Klinik |
| :--- | :--- | :--- | :--- |
| **Solunum Yolu ve Bağırsak Epiteli** | Klorürü ($Cl^-$) **hücreden lümene salgılar**; ENaC kanalını inhibe ederek aşırı sodyum girişini frenler. | Klorür lümene salgılanamaz. ENaC üzerindeki fren kalkar; **aşırı Sodyum ($Na^+$) ve Su hücre içine çekilir**. | Lümen sıvısı kurur! **Aşırı koyu, dehidrate, yapışkan, viskoz mukus tıkaçları** oluşur. Siliyer temizlik çöker. |
| **Ter Bezi Epiteli** | Ter bezinden primer salgı geçerken klorürü **lümenden hücre içine geri emer** (reabsorbsiyon). | Klorür geri emilemez; elektriksel denge için sodyum da lümende kalır. | **Terde aşırı yüksek sodyum ve klorür yoğunluğu!** Ebeveyn bebeği öptüğünde 'tuzlu tat' alır (**Ter Testi Altın Standart**). |

### 2. Başlıca Sistemik Organ Patolojileri

1. **Akciğerler**:
   - Bronş lümenlerini tıkayan koyu mukus tıkaçları atelektazi, kronik bronşit ve yaygın **silindirik bronşiektazi**ye yol açar.
   - Tekrarlayan enfeksiyonlar: Erken bebeklikte *Staphylococcus aureus* ve *Haemophilus influenzae*; ilerleyen yaşta mukoid kapsüllü **Pseudomonas aeruginosa** ve dirençli *Burkholderia cepacia* (ölüm nedenidir).
2. **Pankreas**:
   - Duktusların tıkanması -> Asiner atrofi ve fibrozis (**Kistik Fibrozis adı buradan gelir!**).
   - Ekzokrin pankreas yetmezliği -> Yağ ve protein malabsorbsiyonu, yağda eriyen vitamin (A, D, E, K) eksiklikleri, **steatore** ve büyüme geriliği.
3. **Gastrointestinal Sistem**:
   - Yenidoğanda koyu mukuslu mekonyumun ileumda takılması: **Mekonyum İleusu** (yenidoğanda ilk CF belirtisidir!).
4. **Erkek Üreme Sistemi**:
   - Olguların %95'inde vas deferenslerin bilateral konjenital yokluğu (**CBAVD**) ve obstrüktif azospermi (infertilite).
""",
        "spotPearls": [
            "▸ **İyon Taşınması Kuralı**: Kistik fibroziste solunum epitelinde su lümenden emilerek mukus kurutulurken; ter bezinde klor geri emilemediği için **terde sodyum ve klor fırlar**.",
            "🔴 ÖNEMLİ: Yenidoğan döneminde en erken kistik fibrozis klinik belirtisi **Mekonyum İleusu**dur; erişkinde en sık mortalite nedeni ise ***Pseudomonas aeruginosa* ilişkili süpüratif bronşiektazi**dir.",
            "🔵 ÇIKMIŞ SORU: Kistik fibrozis tanısında altın standart tarama ve tanı yöntemi **Pilorokarpin İyontoforezi ile Ter Testinde klor konsantrasyonunun >60 mEq/L saptanmasıdır**."
        ],
        "coreContent": [
            {"title": "Ter Testi (>60 mEq/L)", "description": "Ter bezlerinde klor geri emilemediği için terde yüksek tuz saptanması.", "highYieldBadge": "Altın Standart Tanı", "details": "Pilokarpin iyontoforezi ile ter toplanır."},
            {"title": "Pseudomonas ve Bronşiektazi", "description": "Koyu mukusta üreyen alginat kapsüllü Pseudomonas kolonizasyonu.", "highYieldBadge": "Akciğer Mortalitesi", "details": "Burkholderia cepacia enfeksiyonu ('cepacia sendromu') nakil kontrendikasyonudur."},
            {"title": "Mekonyum İleusu", "description": "Koyu yapışkan mekonyumun ileoçekal valvde obstrüksiyon yapması.", "highYieldBadge": "Yenidoğan Belirtisi", "details": "Doğumdan sonraki ilk 24-48 saatte gaita çıkaramama ile başvurur."}
        ],
        "flashcards": [
            {"id": "fc-gp-15", "front": "Kistik fibrozis tanısında ter testinde klor düzeyinin tanı koydurucu eşik değeri nedir?", "back": "Terde klor düzeyinin > 60 mEq/L olmasıdır.", "tag": "Tanısal Test", "masterLevel": "Kritik"},
            {"id": "fc-gp-16", "front": "Kistik fibrozisli adölesan ve erişkin hastaların akciğerlerinde kronik kolonizasyon yaparak bronşiektaziye yol açan en karakteristik bakteri hangisidir?", "back": "Pseudomonas aeruginosa (mukoid fenotip).", "tag": "Mikrobiyoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-08",
                "question": "Doğumdan sonra mekonyum çıkaramayan ve ileus operasyonuna alınan bir bebeğin büyüme döneminde kronik öksürük, steatore (yağlı ishal) ve büyüme geriliği gelişiyor. Balgam kültüründe mukoid Pseudomonas aeruginosa üreyen bu çocukta kesin tanı için istenmesi gereken en uygun test hangisidir?",
                "options": [
                    "A) Ter Klorür Testi (Pilokarpin iyontoforezi)",
                    "B) Dışkıda Gizli Kan Testi",
                    "C) Serum Alfa-1 Antitripsin düzeyi",
                    "D) Bronkoalveoler lavaj sitolojisi",
                    "E) Akciğer biyopsisinde granülom aranması"
                ],
                "correctAnswer": "A",
                "explanation": "Mekonyum ileusu, büyüme geriliği, steatore ve Pseudomonas bronşiti klasik Kistik Fibrozis tablosudur; altın standart tanı yöntemi terde klor düzeyini ölçen Ter Testidir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Kistik fibroziste pankreas yetmezliği neden diyabete (CFRD) dönüşebilir?",
            "Erkek kistik fibrozis hastalarında konjenital bilateral vas deferens agenezisi (CBAVD) spermatogenezi etkiler mi?"
        ]
    },

    # SLIDE 9
    {
        "slideNumber": 9,
        "title": "Sitogenetik Bozukluklar: Down Sendromu (Trizomi 21) Etiyopatogenezi",
        "subtitle": "%95 Maternal Mayotik Non-Disjunction, İleri Anne Yaşı ve Robertsonian Translokasyon",
        "badge": "Trizomi 21",
        "badgeColor": "purple",
        "synthesisNarrative": """### 1. Sitogenetik Bozukluklara Genel Bakış

Sitogenetik hastalıklar, kromozom sayısında (sayısal anöploidiler: trizomi, monozomi) veya yapısında (translokasyon, delesyon, inversiyon) ışık mikroskobunda veya mikrodizilimlerde görülebilecek düzeydeki anormalliklerdir.

Canlı doğan bebeklerde en sık görülen kromozomal anöploidi ve zihinsel engelliliğin en yaygın genetik nedeni **Down Sendromudur (Trizomi 21)**.

### 2. Down Sendromunun Üç Sitogenetik Mekanizması

```
+-----------------------------------------------------------------------------------+
|                        DOWN SENDROMU SİTOGENETİK DAĞILIMI                         |
+-----------------------------------------------------------------------------------+
| 1. Tam Trizomi 21 (%95):                                                          |
|    - 47,XX,+21 veya 47,XY,+21 karyotipi.                                          |
|    - Mayoz bölünme sırasında 21. kromozom çiftinin ayrılamaması (**Maternal       |
|      Mayotik Non-Disjunction**; %90-95'inde hata Oogenez Mayoz I'dedir).          |
|    - **İleri Anne Yaşı ile Doğrudan İlişkilidir**:                                |
|      20 yaş altı annede risk 1/1500 iken, 45 yaş üstü annede risk **1/25'e çıkar!|
|                                                                                   |
| 2. Robertsonian Translokasyon (%4):                                               |
|    - 21. kromozomun uzun kolunun akrosentrik başka bir kromozoma (en sık          |
|      14. kromozom: t(14;21)) yapışmasıdır.                                       |
|    - **Anne yaşıyla ilişkisizdir!** Ailesel geçiş gösterebilir. Ebeveyn dengeli  |
|      taşıyıcı ise tekrarlama riski yüksektir.                                     |
|                                                                                   |
| 3. Mozaik Trizomi 21 (%1):                                                        |
|    - Post-zigotik mitoz sırasında ayrılmama sonucu oluşur (normal ve trizomik     |
|      hücre hatları bir aradadır). Klinik tablo hücre oranına göre daha hafiftir.   |
+-----------------------------------------------------------------------------------+
```

### 3. Kromozom 21'in 'Gen Dozaj Etkisi'

21. kromozom en küçük otozomal kromozom olmasına rağmen, içerdiği kritik genlerin 3 kopya olması fenotipi belirler:
- **APP Geni (Amiloid Prekürsör Protein)**: 21. kromozomdadır; aşırı üretimi nedeniyle **40 yaş üzerindeki tüm Down sendromlu bireylerde Alzheimer nöropatolojisi** (senil plaklar) kaçınılmaz olarak gelişir!
- **DYRK1A, SOD1, ETS2**: Nörogelişimsel ve lösemik süreçlerde rol oynar.
""",
        "spotPearls": [
            "▸ Down sendromu olgularının **%95'i** mayoz sırasında ayrılmama (**maternal mayotik non-disjunction**) sonucu gelişir ve **ileri anne yaşıyla** doğrudan ilişkilidir.",
            "🔴 ÖNEMLİ: Down sendromunun **Robertsonian Translokasyon (%4)** formu anne yaşı ile İLİŞKİSİZDİR; ebeveyn dengeli taşıyıcı olabileceği için sonraki gebeliklerde tekrarlama riski taşır.",
            "🔵 ÇIKMIŞ SORU: Down sendromlu bireylerde 40 yaşından sonra erken başlangıçlı Alzheimer hastalığı gelişmesinin nedeni, **APP (Amiloid Prekürsör Protein) geninin 21. kromozomda yer alması** ve gen dozaj artışıdır."
        ],
        "coreContent": [
            {"title": "Maternal Non-Disjunction (%95)", "description": "Mayoz I sırasında 21. kromozomların ayrılamaması.", "highYieldBadge": "En Sık Tip", "details": "İleri maternal yaş en güçlü epidemiyolojik risk faktörüdür."},
            {"title": "Robertsonian Translokasyon (%4)", "description": "t(14;21) translokasyonu ile ortaya çıkan ailesel form.", "highYieldBadge": "Anne Yaşından Bağımsız", "details": "Ebeveyn karyotipi taranmalıdır."},
            {"title": "APP Geni ve Alzheimer", "description": "Amiloid prekürsör protein dozajının 3 kopya olması.", "highYieldBadge": "Gen Dozajı", "details": "40 yaş üstü Down hastalarında A-beta amiloid plakları birikir."}
        ],
        "flashcards": [
            {"id": "fc-gp-17", "front": "Down sendromu olgularının %95'inden sorumlu temel sitogenetik mekanizma nedir?", "back": "Maternal mayotik non-disjunction (ayrılamama).", "tag": "Sitogenetik", "masterLevel": "Kritik"},
            {"id": "fc-gp-18", "front": "Down sendromlu bireylerin 40'lı yaşlarda Alzheimer hastalığı geliştirmesinin genetik temeli nedir?", "back": "APP (Amiloid Prekürsör Protein) geninin 21. kromozomda yer alması ve 3 kopya olarak aşırı üretilmesidir.", "tag": "Nöropatoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-09",
                "question": "42 yaşındaki bir gebeden doğan ve Down sendromu tanısı alan bebeğin sitogenetik analizinde 47,XY,+21 saptanıyor. Bu hastadaki sayısal kromozom anomalisine yol açan en muhtemel hücresel mekanizma aşağıdakilerden hangisidir?",
                "options": [
                    "A) Oogenez Mayoz I sırasında kromozomların ayrılamaması (non-disjunction)",
                    "B) Spermatogenez Mayoz II sırasında sentromer bölünme kusuru",
                    "C) Post-zigotik erken mitotik ayrılmama",
                    "D) 14 ve 21. kromozomlar arası dengeli Robertsonian translokasyonu",
                    "E) Perisentrik inversiyon"
                ],
                "correctAnswer": "A",
                "explanation": "Down sendromu olgularının %95'i maternal mayotik non-disjunction (özellikle oogenez Mayoz I'de ayrılmama) sonucu gelişir ve bu durum ileri anne yaşı ile doğrudan ilişkilidir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Down sendromu taramasında ikili ve dörtlü tarama testinde bakılan serum belirteçleri (beta-hCG, PAPP-A, AFP, uE3, İnhibin A) nasıldır?",
            "NIPT (Non-İnvaziv Prenatal Test) serbest fetal DNA analizi ile trizomi 21 tanısını nasıl koyar?"
        ]
    },

    # SLIDE 10
    {
        "slideNumber": 10,
        "title": "Down Sendromu: Klinikopatolojik Tutulumlar ve Yaşam Seyri",
        "subtitle": "Kardiyak Malformasyonlar, Duodenal Atrezi, Akut Lösemi Riski ve Enfeksiyonlar",
        "badge": "Down Kliniği",
        "badgeColor": "rose",
        "synthesisNarrative": """### 1. Down Sendromunun Karakteristik Dismorfolojisi

- **Yüz ve Kafa**: Brakisefali (düzleşmiş art kafa), düzleşmiş yüz profili ve basık burun kökü, yukarı çekik palpebral fissürler, belirgin **iç epikantik kıvrımlar**, dilde dışarı taşma (makroglossi hissi), iriste küçük beyaz lekeler (**Brushfield Lekeleri**).
- **Ekstremiteler**: Avuç içinde tek transvers palmar çizgi (**Simian Çizgisi**), 5. parmakta klinodaktili (içe kıvrılma), ayak 1. ve 2. parmakları arasında geniş yarık (**Sandal Açıklığı**), genel kas hipotonisi.

### 2. İç Organ Malformasyonları ve Malignite Riskleri

```
+-----------------------------------------------------------------------------------+
|                        DOWN SENDROMU İÇ ORGAN PATOLOJİLERİ                        |
+-----------------------------------------------------------------------------------+
| 1. KARDİYOVASKÜLER ANOMALİLER (%40-50):                                           |
|    - En sık ölüm nedenidir!                                                       |
|    - En sık görülen lezyon: **Endokardiyal Yastık Defekti** (Atriyoventriküler    |
|      Septal Defekt - AVSD). İkinci sıklıkta VSD ve ASD.                          |
|                                                                                   |
| 2. GASTROİNTESTİNAL ANOMALİLER:                                                   |
|    - **Duodenal Atrezi**: Ayakta direkt batın grafisinde patognomonik             |
|      **'Çift Baloncuk (Double Bubble)'** gaz görünümü verir; safralı kusma.       |
|    - Hirschsprung Hastalığı (Aganglionik megakolon) riski belirgin artmıştır.     |
|                                                                                   |
| 3. HEMATOLOJİK MALİGNİTELER (10-20 Kat Artmış Risk!):                            |
|    - Çocukluk çağında **Akut Lenfoblastik Lösemi (ALL)** riski 20 kat artmıştır.  |
|    - İlk 3 yaşta **Akut Megakaryoblastik Lösemi (AML M7)** riski dramatik yüksektir!|
|    - Yenidoğanda kendini sınırlayan 'Geçici Miyeloproliferatif Bozukluk' (TMD).   |
|                                                                                   |
| 4. İMMÜN SİSTEM VE ENFEKSİYONLAR:                                                 |
|    - T hücre immün yetmezliği nedeniyle akciğer enfeksiyonları çok sıktır.        |
+-----------------------------------------------------------------------------------+
```
""",
        "spotPearls": [
            "▸ Down sendromunda en sık görülen konjenital kardiyak defekt **Endokardiyal Yastık Defektidir (AVSD)**; erken çocuklukta mortalitenin birincil nedenidir.",
            "🔴 ÖNEMLİ: Gastrointestinal sistemde yenidoğanda safralı kusma ve karın grafisinde 'çift baloncuk' görünümü yapan lezyon **Duodenal Atrezi**dir.",
            "🔵 ÇIKMIŞ SORU: Down sendromlu çocuklarda ilk 3 yaşta görülme sıklığı 500 kat artan lösemi alt tipi **Akut Megakaryoblastik Lösemi (AML-M7)**'dir; daha büyük çocuklarda ise **ALL** sıktır."
        ],
        "coreContent": [
            {"title": "Endokardiyal Yastık Defekti", "description": "AVSD, Down sendromunda en sık rastlanan kardiyak lezyondur (%40).", "highYieldBadge": "Kardiyak Defekt", "details": "Cerrahi onarım yapılmazsa pulmoner hipertansiyon gelişir."},
            {"title": "Duodenal Atrezi", "description": "Lümenin rekanalize olamaması sonucu çift baloncuk (double bubble) işareti.", "highYieldBadge": "GİS Anomalisi", "details": "Yenidoğanda safralı kusma ile acil cerrahi tablodur."},
            {"title": "Lösemi Riski (AML M7 / ALL)", "description": "GATA1 mutasyonları eşliğinde megakaryoblastik lösemi yatkınlığı.", "highYieldBadge": "Onko-hematoloji", "details": "Geçici miyeloproliferatif hastalık yenidoğanda spontan gerileyebilir."}
        ],
        "flashcards": [
            {"id": "fc-gp-19", "front": "Down sendromunda en sık rastlanan konjenital kalp malformasyonu nedir?", "back": "Endokardiyal yastık defekti (Atriyoventriküler septal defekt - AVSD).", "tag": "Kardiyoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-20", "front": "Down sendromlu 2 yaşındaki bir çocukta gelişme riski en yüksek olan akut miyeloid lösemi (AML) alt tipi hangisidir?", "back": "Akut Megakaryoblastik Lösemi (AML M7).", "tag": "Hematoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-10",
                "question": "Doğumda epikantus, basık burun kökü ve avuç içinde tek transvers çizgi saptanan bir bebekte doğumdan 24 saat sonra safralı kusma başlıyor. Çekilen direkt batın grafisinde midede ve proksimal duodenumda hava-sıvı seviyesi ('çift baloncuk' görünümü) saptanıyor. Bu bebekteki gastrointestinal patoloji aşağıdakilerden hangisidir?",
                "options": [
                    "A) Pilor Stenozu",
                    "B) Duodenal Atrezi",
                    "C) İntususepsiyon",
                    "D) Mekonyum İleusu",
                    "E) Özofagus Atrezisi"
                ],
                "correctAnswer": "B",
                "explanation": "Down sendromu ile güçlü birliktelik gösteren, doğumdan hemen sonra safralı kusma ve direkt grafide 'çift baloncuk (double bubble)' görünümü veren lezyon Duodenal Atrezidir.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Down sendromunda GATA1 mutasyonunun geçici miyeloproliferatif bozukluk ve AML M7 gelişimindeki rolü nedir?",
            "Hirschsprung hastalığında aganglionozisin embriyolojik nedeni (nöral krest göç kusuru) nedir?"
        ]
    },

    # SLIDE 11
    {
        "slideNumber": 11,
        "title": "Çevresel Patoloji ve Hava Kirliliği: Ozon ve Partikül Madde (PM)",
        "subtitle": "EPA Kriter Kirleticileri, O3 Serbest Radikal Hasarı ve PM2.5 Alveoler Enflamasyonu",
        "badge": "Hava Kirliliği",
        "badgeColor": "emerald",
        "synthesisNarrative": """### 1. Çevresel Hastalıklar ve Hava Kirliliği

Dünya Sağlık Örgütü verilerine göre her yıl milyonlarca insan dış ortam ve ev içi hava kirliliğine bağlı kardiyorespiratuar nedenlerle hayatını kaybetmektedir.

ABD Çevre Koruma Ajansı (EPA) tarafından izlenen **6 Kriter Hava Kirleticisi**:
1. **Ozon ($O_3$)**
2. **Partikül Madde ($PM_{10}$ ve $PM_{2.5}$)**
3. **Karbonmonoksit (CO)**
4. **Azot Dioksit ($NO_2$)**
5. **Kükürt Dioksit ($SO_2$)**
6. **Kurşun ($Pb$)**

### 2. Ozon ($O_3$) Toksisitesi

- **Oluşumu**: Güneş ışığının (UV) azot oksitler ve uçucu organik bileşiklerle fotokimyasal reaksiyonu sonucu 'yer seviyesi dumanı (smog)' içinde oluşur.
- **Mekanizma**: Alveol epitelinde lipit peroksidasyonunu tetikler, serbest oksijen radikalleri açığa çıkarır ve enflamatuar sitokin salınımını uyarır.
- **Klinik**: Özellikle astımlı ve KOAH'lı hastalarda akut alevlenmelere, hava yolu epitel nekrozuna ve amfizem gelişimine katkıda bulunur.

### 3. Partikül Madde: $PM_{10}$ vs. $PM_{2.5}$

| Partikül Boyutu | Çapı | Solunum Sisteminde Ulaştığı Düzey | Patolojik Etkisi |
| :--- | :--- | :--- | :--- |
| **Kaba Partiküller ($PM_{10}$)** | $< 10\ \mu\text{m}$ | Burun, farenks ve ana bronşlarda tutulur; mukosiliyer eskalatörle temizlenir. | Üst solunum yolu irritasyonu, bronkospazm, öksürük. |
| **İnce Partiküller ($PM_{2.5}$)** | $< 2.5\ \mu\text{m}$ | **Alveollere ve terminal bronşiyollere kadar ulaşır**; makrofajlarca fagosite edilir. | Alveoler makrofaj aktivasyonu, sistemik dolaşıma sitokin kaçağı, **miyokard enfarktüsü**, ateroskleroz progresyonu ve akciğer kanseri riski! |
""",
        "spotPearls": [
            "▸ Partikül madde çapı ne kadar küçükse solunum yollarında o kadar derine iner; **$PM_{2.5}$ partikülleri doğrudan alveollere ulaşır** ve sistemik dolaşıma sitokin deşarjı yaparak **kardiyovasküler mortaliteyi (MI, inme)** artırır.",
            "🔴 ÖNEMLİ: Ozon ($O_3$) yer seviyesinde güneş ışığı ve egzoz gazlarının reaksiyonuyla oluşur; serbest radikal hasarı yaparak astım ve amfizem alevlenmelerine yol açar.",
            "🔵 ÇIKMIŞ SORU: *'Hava kirliliğinde doğrudan alveollere ulaşarak kronik enflamasyon ve aterosklerotik kardiyovasküler olayları tetikleyen en tehlikeli partikül boyutu hangisidir?'*\n  ▫ Doğru yanıt: **$PM_{2.5}$ (Çapı 2.5 mikrometreden küçük ince partiküller)**'dir."
        ],
        "coreContent": [
            {"title": "PM2.5 Tehlikesi", "description": "Alveollere ulaşıp sistemik enflamasyon ve tromboz tetikleyen ince tozlar.", "highYieldBadge": "Kardiyovasküler Risk", "details": "Dizel egzozu ve kömür yanması ana kaynaktır."},
            {"title": "Ozon Serbest Radikalleri", "description": "Fotokimyasal duman bileşeni; hava yolu epitelinde peroksidasyon yapar.", "highYieldBadge": "Oksidatif Hasar", "details": "Astım ataklarının sıcak yaz aylarında artışından sorumludur."},
            {"title": "Kükürt Dioksit (SO2)", "description": "Kömür yakılmasıyla oluşan asit yağmuru ve bronkokonstriksiyon gazı.", "highYieldBadge": "İrritan Gaz", "details": "Sülfürik aside dönüşerek hava yolunu yakar."}
        ],
        "flashcards": [
            {"id": "fc-gp-21", "front": "Hava kirliliğinde alveollere kadar penetre olup miyokard enfarktüsü ve inme riskini artıran partikül maddelerin boyutu nedir?", "back": "PM2.5 (çapı 2.5 mikrondan küçük ince partiküller).", "tag": "Çevresel Patoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-22", "front": "Fotokimyasal duman (smog) içinde serbest oksijen radikali üreterek astım alevlenmesi yapan gaz kirletici nedir?", "back": "Ozon (O3).", "tag": "Toksikoloji", "masterLevel": "Yüksek"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-11",
                "question": "Hava kirliliği yoğun olan bir metropolde yaşayan bireylerde uzun dönemde aterosklerotik plak instabilitesi ve akut koroner sendrom riskinin artmasından sorumlu olan, alveol seviyesine kadar ulaşıp makrofaj aktivasyonu ile sistemik enflamatuar sitokin salınımını tetikleyen temel partiküler kirletici boyutu hangisidir?",
                "options": [
                    "A) PM50",
                    "B) PM20",
                    "C) PM10",
                    "D) PM2.5",
                    "E) Yalnızca kaba polenler"
                ],
                "correctAnswer": "D",
                "explanation": "Çapı 2.5 mikrometreden küçük partiküller (PM2.5) üst solunum yollarındaki filtreleri aşarak doğrudan alveollere iner, makrofajlarca yutulur ve salınan mediyatörler sistemik dolaşıma karışarak ateroskleroz ve kardiyovasküler mortaliteyi artırır.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "İç ortam hava kirliliğinde biyo-yakıt dumanı ile gelişen pnömokonyoz ve KOAH patolojisi nasıldır?",
            "Asit yağmurlarının (SO2 ve NO2) solunum epitelindeki kimyasal hasar basamakları nelerdir?"
        ]
    },

    # SLIDE 12
    {
        "slideNumber": 12,
        "title": "Karbonmonoksit (CO) ve Hipoksi Patolojisi",
        "subtitle": "Hemoglobine 200 Kat Afinite, Oksihemoglobin Eğrisi Kayması ve Globus Pallidus Nekrozu",
        "badge": "CO İntoksikasyonu",
        "badgeColor": "amber",
        "synthesisNarrative": """### 1. Karbonmonoksit (CO): Sessiz Katil

Karbonmonoksit; fosil yakıtların, sobaların, şofbenlerin ve yangınların eksik yanması sonucu açığa çıkan **kokusuz, renksiz, tatsız ve son derece toksik** bir gazdır.

### 2. Moleküler Toksisite Mekanizmaları

1. **Aşırı Yüksek Hemoglobin Afinitesi**:
   - CO, hemoglobindeki demire oksijenden **yaklaşık 200 kat daha yüksek afiniteyle** bağlanır.
   - Sonuçta **Karboksihemoglobin (COHb)** oluşur; oksijenin bağlanabileceği hem bölgeleri bloke olur (anemik hipoksi).
2. **Oksihemoglobin Eğrisinin Sola Kayması**:
   - CO bağlı hemoglobin molekülü allosterik olarak diğer hem gruplarının oksijeni bırakmasını engeller; oksijen dissosiasyon eğrisi **sola kayar**. Oksijen dokulara transfer edilemez!
3. **Sitokrom C Oksidaz İnhibisyonu**:
   - Hücre içine giren CO mitokondriyal elektron taşıma zincirinde kompleks IV'ü (sitokrom c oksidaz) doğrudan inhibe ederek hücresel solunumu durdurur.

### 3. Klinik ve Patolojik İmzalar

- **Kiraz Kırmızısı Cilt ve Mukozalar**: Ağır CO zehirlenmesinde karboksihemoglobinin parlak kırmızı rengi nedeniyle ciltte ve dudaklarda siyanonun aksine **Kiraz Kırmızısı (Cherry-Red)** renk değişimi görülür.
- **Santral Sinir Sistemi**: Oksijen tüketimi en yüksek bölgeler nekroze olur; özellikle beyinde bazal ganglionlarda **Globus Pallidus'un Bilateral Simetrik Nekrozu** CO intoksikasyonunun patognomonik otopsi bulgusudur!
- **Tedavi**: %100 normobarik veya **Hiperbarik Oksijen Tedavisi** (COHb yarı ömrünü 320 dakikadan 20 dakikaya indirir).
""",
        "spotPearls": [
            "▸ Karbonmonoksit hemoglobine oksijenden **200 kat daha güçlü** bağlanarak **Karboksihemoglobin (COHb)** oluşturur ve oksihemoglobin eğrisini **sola kaydırarak** dokuya oksijen salınımını felç eder.",
            "🔴 ÖNEMLİ: Ağır CO zehirlenmesinde cilt siyanotik değil, parlak **Kiraz Kırmızısı (Cherry-Red)** renktedir; beyinde patognomonik lezyon **Bilateral Globus Pallidus Nekrozu**dur.",
            "🔵 ÇIKMIŞ SORU: Karbonmonoksit zehirlenmesinin hayat kurtarıcı tedavisi **%100 Hiperbarik Oksijen** uygulamasıdır."
        ],
        "coreContent": [
            {"title": "200 Kat Afinite", "description": "Oksijen taşıma kapasitesini bloke eden karboksihemoglobin oluşumu.", "highYieldBadge": "Bağlanma Gücü", "details": "Düşük konsantrasyonda bile ölümcül COHb seviyelerine ulaşır."},
            {"title": "Globus Pallidus Nekrozu", "description": "Beyin bazal ganglionlarında bilateral simetrik kavitasyonel nekroz.", "highYieldBadge": "Nöropatoloji", "details": "CO intoksikasyonunun klasik otopsi bulgusudur."},
            {"title": "Kiraz Kırmızısı Renk", "description": "Deri ve mukozaların siyanoz yerine parlak kırmızı görünmesi.", "highYieldBadge": "Klinik Muayene", "details": "Karboksihemoglobinin spektral optik özelliğidir."}
        ],
        "flashcards": [
            {"id": "fc-gp-23", "front": "Karbonmonoksitin hemoglobine afinitesi oksijene kıyasla yaklaşık kaç kattır?", "back": "Yaklaşık 200 kat daha fazladır.", "tag": "Toksikoloji", "masterLevel": "Kritik"},
            {"id": "fc-gp-24", "front": "Karbonmonoksit intoksikasyonunda beyinde bilateral simetrik nekroza uğrayan spesifik anatomik bölge neresidir?", "back": "Globus Pallidus (bazal ganglionlar).", "tag": "Nöropatoloji", "masterLevel": "Kritik"}
        ],
        "relatedQuestions": [
            {
                "id": "prac-gp-12",
                "question": "Kışın sobalı evde baygın bulunan bir hastanın dudaklarında ve derisinde kiraz kırmızısı renk saptanıyor. Çekilen beyin manyetik rezonans görüntülemesinde bilateral globus pallidusta simetrik nekroz alanları izleniyor. Bu hastadaki zehirlenme etkeni ve temel patofizyolojik mekanizma hangisidir?",
                "options": [
                    "A) Siyanür - Methemoglobin oluşumu",
                    "B) Karbonmonoksit - Karboksihemoglobin oluşumu ve oksihemoglobin eğrisinin sola kayması",
                    "C) Kurşun - ALA dehidrataz enzim inhibisyonu",
                    "D) Arsenik - Piruvat dehidrogenaz blokajı",
                    "E) Metil alkol - Formik asit retinit hasarı"
                ],
                "correctAnswer": "B",
                "explanation": "Kiraz kırmızısı cilt rengi ve bilateral globus pallidus nekrozu Karbonmonoksit (CO) zehirlenmesinin patognomonik tablosudur. CO hemoglobine bağlanarak karboksihemoglobin oluşturur ve oksihemoglobin eğrisini sola kaydırarak ağır hücresel hipoksi yapar.",
                "isPracticeQuestion": True,
                "examYear": "Özgün Çalışma Testi"
            }
        ],
        "aiPromptSuggestions": [
            "Siyanür zehirlenmesi ile CO zehirlenmesinin hücresel solunum (sitokrom oksidaz) düzeyindeki farkları nelerdir?",
            "Puls oksimetrelerin (SpO2) CO zehirlenmesinde neden yalancı yüksek (%100) ölçüm yaptığı nasıl açıklanır?"
        ]
    }
]

print(f"Constructed slides 1 to {len(slides)}. Continuing with slides 13 to 24...")
