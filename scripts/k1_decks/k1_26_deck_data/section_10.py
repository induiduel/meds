# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 10: Moleküler Patoloji, Hedefe Yönelik Tedavi ve Büyük Sentez (Slayt 91-100)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: Sitogenetik ve Moleküler Tanı Yöntemleri
    slides.append({
        "id": "k1-26-s91",
        "title": "Sitogenetik ve Moleküler Tanı Yöntemleri: Karyotip, FISH ve Array CGH",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 91,
        "narrative": (
            "Modern patoloji ve tıbbi genetik, hastalıklara tanı koymak için hücresel ve moleküler düzeyde üç ana yöntem hiyerarşisi kullanır: "
            "1. **Klasik Karyotipleme (G-Bantlama):** "
            "- Bölünen hücrelerin metafaz evresinde kolşisinle durdurulup Giemsa ile boyanmasıdır. "
            "- Tüm genomu kuşbakışı gösterir; anöploidiler (Down, Turner) ve büyük kromozomal translokasyonları (>4-5 megabaz) yakalar. "
            "- Çözünürlüğü düşüktür; mikrodelesyonları göremez ve canlı bölünen hücre kültürü gerektirir. "
            "2. **Floresan in situ Hibridizasyon (FISH):** "
            "- Floresan boyalarla işaretli DNA problarının lam üzerindeki hedef DNA'ya bağlanmasıdır (interfaz veya metafaz). "
            "- Submikroskopik delesyonları (DiGeorge 22q11), gen amplifikasyonlarını (**HER2/neu**) ve füzyon genlerini (**BCR-ABL**) "
            "tek bir hücre düzeyinde yüksek çözünürlükle gösterir. "
            "3. **Mikroarray Karşılaştırmalı Genomik Hibridizasyon (Array CGH):** "
            "- Hasta ve kontrol DNA'sının farklı floresanlarla boyanıp mikroyonga üzerinde yarıştırılmasıdır. "
            "- Hücre kültürü gerektirmeden tüm genom genelinde **kopya sayısı varyasyonlarını (CNV - mikrodelesyon/duplikasyon)** "
            "kilobaz düzeyinde haritalandırır (otizm ve dismorfolojide birinci basamak testtir)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sitogenetik Tanı Yöntemlerinin Karşılaştırması",
                ["Yöntem", "Gereken Materyal", "Çözünürlük Düzeyi", "Klinik Kullanım Endikasyonu"],
                [
                    ["Klasik Karyotipleme", "Canlı bölünen hücre kültürü (metafaz)", ">4-5 Megabaz (Düşük)", "Trizomi 21, Turner 45,X, büyük translokasyonlar"],
                    [
                        "FISH (Floresan in situ)",
                        "Metafaz veya interfaz hücreleri / parafin kesit",
                        {"text": "100 kilobaz - 1 megabaz (Yüksek)", "isMasked": True, "hint": "Tek bir genin veya delesyonun floresan mikroskobunda ışıma ile tespiti"},
                        "HER2 amplifikasyonu, BCR-ABL füzyonu, 22q11 delesyonu"
                    ],
                    ["Array CGH (Mikroarray)", "Ekstrakte genomik DNA (kültürsüz)", "Kilobaz düzeyi (Çok Yüksek)", "Otizm, açıklanamayan dismorfoloji, CNV haritalama"]
                ]
            ),
            make_micro_quiz(
                "Meme karsinoması tanısı alan bir hastada hedefe yönelik monoklonal antikor tedavisi (Trastuzumab) planlamadan önce tümör dokusundaki HER2 gen amplifikasyonunu kesin olarak kantite etmek için kullanılan altın standart sitogenetik yöntem hangisidir?",
                {
                    "A": "Floresan in situ Hibridizasyon (FISH)",
                    "B": "Klasik Giemsa bantlama karyotipi",
                    "C": "Wright boyalı periferik yayma",
                    "D": "Gram boyaması",
                    "E": "Serum protein elektroforezi"
                },
                "A",
                {
                    "A": "Doğrudur; FISH parafin doku kesitinde HER2 gen kopyalarını kontrol kromozom 17 ile oranlayarak amplifikasyonu kanıtlar.",
                    "B": "Yanlış; karyotip parafinde çalışmaz ve çözünürlüğü tek gene yetmez.",
                    "C": "Yanlış; hematolojik boyadır.",
                    "D": "Yanlış; mikrobiyoloji boyasıdır.",
                    "E": "Yanlış; immünoglobulin monoklonal gamopati testidir."
                }
            )
        ]
    })

    # Slayt 92: Gen Düzeyinde İnceleme: PCR ve Gerçek Zamanlı RT-PCR
    slides.append({
        "id": "k1-26-s92",
        "title": "Gen Düzeyinde İnceleme: PCR ve Gerçek Zamanlı RT-PCR",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 92,
        "narrative": (
            "Polimeraz Zincir Reaksiyonu (PCR), moleküler patolojinin ve modern tıbbın iş gücü motorudur: "
            "1. **Klasik PCR Prensibi:** "
            "- Hedef DNA bölgesini çevreleyen sentetik oligonükleotid primerler, termostabil Taq DNA polimeraz ve serbest dNTP'ler kullanılır. "
            "- Isıl döngüler (Denatürasyon 95°C -> Bağlanma/Annealing 55-60°C -> Uzama/Extension 72°C) ile hedef dizi "
            "her döngüde ikiye katlanır; **30 döngüde tek bir DNA molekülünden 1 milyar kopya** üretilir. "
            "2. **Ters Transkripsiyon PCR (RT-PCR):** "
            "- Hücredeki haberci RNA (mRNA) molekülü ters transkriptaz enzimiyle tamamlayıcı DNA'ya (cDNA) çevrilir ve PCR yapılır. "
            "- Kronik miyeloid lösemideki **BCR-ABL füzyon transkriptini** ve RNA virüslerini (HCV, HIV, SARS-CoV-2) saptamada temeldir. "
            "3. **Gerçek Zamanlı (Real-Time) Kantitatif PCR (qPCR):** "
            "- Çoğalma sırasında floresan problar kullanılır; reaksiyon tüpü açılmadan anlık ışıma ölçülür. "
            "- Kanda **viral yük (kopya sayısı)** tayini ve minimal kalıntı hastalık (MRD) takibinde altın standarttır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "PCR Isıl Döngü Basamakları",
                [
                    "1. Denatürasyon (94-95°C): Yüksek ısıyla çift iplikli hedef DNA sarmalının tek ipliklere ayrılması",
                    "2. Primer Bağlanması (55-60°C): Özgül oligonükleotid primerlerin komplementer hedef dizilere yapışması",
                    "3. Enzimatik Uzama (72°C): Termostabil Taq polimerazın serbest dNTP'leri ekleyerek yeni ipliği örmesi",
                    "4. Geometrik Çoğalma: Her döngüde DNA miktarının ikiye katlanarak milyarlarca kopyaya ulaşması"
                ]
            ),
            make_active_recall(
                "Moleküler patolojide RNA virüslerinin varlığını saptamak veya lösemilerdeki anormal füzyon transkriptlerini çoğaltmak amacıyla RNA'yı önce cDNA'ya çevirip ardından amplifiye eden PCR yöntemi nedir?",
                "Ters transkripsiyon PCR'dır (RT-PCR).",
                "Reverse transcriptase enzimiyle RNA şablonundan DNA üreten moleküler teknik"
            )
        ]
    })

    # Slayt 93: Genom Düzeyinde İnceleme: Yeni Nesil Dizileme (NGS)
    slides.append({
        "id": "k1-26-s93",
        "title": "Genom Düzeyinde İnceleme: Yeni Nesil Dizileme (NGS)",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 93,
        "narrative": (
            "Sanger sekanslamasının tek seferde tek bir geni okuyabilen hantal yapısının yerini, günümüzde "
            "**Yeni Nesil Dizileme (NGS - Next-Generation Sequencing)** almıştır: "
            "1. **Masif Paralel Dizileme:** Milyonlarca küçük DNA parçasının aynı anda, eşzamanlı olarak paralel dizilenmesidir. "
            "Tüm insan genomu birkaç gün içinde ve son derece düşük maliyetle eksiksiz haritalanabilir. "
            "2. **NGS Uygulama Düzeyleri:** "
            "- **Hedefe Yönelik Kanser Panelleri (Targeted Gene Panels):** 50 ile 500 arasında klinik öneme sahip kanser geninin "
            "(EGFR, KRAS, BRAF, ALK, TP53 vb.) eşzamanlı taranması; onkolojide biyopsi materyalinden hedefe yönelik ilaç seçimi sağlar. "
            "- **Tüm Ekzom Dizileme (WES):** Genomun protein kodlayan tüm %1.5'lik kısmının (ekzomunun) taranmasıdır; "
            "açıklanamayan nadir pediatrik kalıtsal hastalıkların teşhisinde çığır açmıştır. "
            "- **Tüm Genom Dizileme (WGS):** Kodlayan ve kodlamayan tüm 3.3 milyar bazın eksiksiz okunmasıdır. "
            "3. **Farmakogenomik:** Hastanın kişisel mutasyon haritasına göre 'doğru hastaya, doğru ilacı, doğru dozda' verme felsefesidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Sanger Sekanslama vs Yeni Nesil Dizileme (NGS)",
                "Sanger Sekanslama (Klasik)",
                "Tek seferde tek gen veya ekzon okunur; yavaş, pahalı ve yüksek miktarda kaliteli DNA gerektirir",
                "Yeni Nesil Dizileme (NGS)",
                "Milyonlarca reaksiyon paralel okunur; yüzlerce kanser geni aynı anda taranır ve kişiselleştirilmiş onkoloji sağlar"
            ),
            make_cloze(
                "Klinik onkolojide tümör biyopsisinden yüzlerce kanser genini eşzamanlı olarak tarayan yüksek verimli teknolojiye yeni nesil dizileme adı verilir.",
                "yeni nesil dizileme",
                "Masif paralel okuma ile tümör mutasyon profilini çıkaran ileri moleküler dizileme platformu"
            )
        ]
    })

    # Slayt 94: Moleküler Hedefe Yönelik Kanser Tedavileri
    slides.append({
        "id": "k1-26-s94",
        "title": "Moleküler Hedefe Yönelik Kanser Tedavileri",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 94,
        "narrative": (
            "Geleneksel kemoterapinin tüm bölünen hücreleri zehirleyen kör yaklaşımının yerini, tümörün spesifik sürücü "
            "mutasyonunu hedef alan **hassas tıp (akıllı moleküler ilaçlar)** almıştır: "
            "1. **EGFR Mutasyonları ve Tirozin Kinaz İnhibitörleri (TKI):** "
            "- Akciğer adenokarsinomlarında (özellikle sigara içmeyen kadınlarda) EGFR tirozin kinaz alanında (ekzon 19 delesyonu, L858R) aktive edici mutasyonlar saptanır. "
            "- Bu hastalara klasik kemoterapi yerine oral **Erlotinib, Gefitinib veya Osimertinib** verilir; tümör dramatik biçimde küçülür. "
            "2. **BRAF V600E Mutasyonu ve BRAF İnhibitörleri:** "
            "- Malign melanomların %50'sinde, tiroid papiller karsinomlarında ve kolorektal kanserlerde BRAF kinazın 600. kodonunda valin yerine glutamat geçer (V600E). "
            "- MAPK yolağı kontrolsüz ateşlenir. Selektif inhibitör **Vemurafenib veya Dabrafenib**, metastatik melanomda hayat kurtarıcı remisyon sağlar. "
            "3. **HER2/neu (ERBB2) Amplifikasyonu ve Trastuzumab:** "
            "- İnvaziv meme ve mide adenokarsinomlarında HER2 reseptör geninin amplifikasyonunda monoklonal antikor **Trastuzumab (Herceptin)** kullanılır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kanserlerde Moleküler Sürücü Mutasyonlar ve Hedefe Yönelik İlaçlar",
                ["Kanser Türü", "Moleküler Değişiklik", "Onkojenik Biyoloji", "Hedefe Yönelik İlaç"],
                [
                    ["Küçük Hücreli Dışı Akciğer Kanseri", "EGFR ekzon 19 delesyonu / L858R", "Reseptör tirozin kinaz sürekli açık", "Gefitinib, Erlotinib, Osimertinib"],
                    [
                        "Malign Melanom",
                        "BRAF V600E mutasyonu",
                        {"text": "MAPK/ERK sinyal yolağının kontrolsüz uyarılması", "isMasked": True, "hint": "Hücre çoğalmasını başlatan serin-treonin kinaz kaskadının aşırı aktivasyonu"},
                        "Vemurafenib, Dabrafenib"
                    ],
                    ["Meme ve Mide Karsinomu", "HER2/neu (ERBB2) amplifikasyonu", "Aşırı büyüme faktörü reseptör yoğunluğu", "Trastuzumab (Herceptin)"],
                    ["Kronik Miyeloid Lösemi (KML)", "t(9;22) BCR-ABL füzyonu", "Sitoplazmik kontrolsüz tirozin kinaz", "İmatinib (Glivec)"]
                ]
            ),
            make_micro_quiz(
                "Metastatik malign melanom tanısıyla takip edilen bir hastanın biyopsisinde BRAF geninde V600E mutasyonu doğrulanmıştır. Bu hastanın onkolojik tedavisinde doğrudan mutasyona uğramış kinaz enzimini hedef alan en uygun akıllı ilaç hangisidir?",
                {
                    "A": "Vemurafenib",
                    "B": "Trastuzumab",
                    "C": "Penisilin",
                    "D": "Metotreksat",
                    "E": "Kolşisin"
                },
                "A",
                {
                    "A": "Doğrudur; Vemurafenib mutant BRAF V600E kinazını selektif olarak bloke eden küçük moleküllü inhibitördür.",
                    "B": "Yanlış; Trastuzumab anti-HER2 monoklonal antikorudur.",
                    "C": "Yanlış; penisilin antibakteriyeldir.",
                    "D": "Yanlış; metotreksat antimetabolit kemoterapidir.",
                    "E": "Yanlış; kolşisin FMF ve gut ilacıdır."
                }
            )
        ]
    })

    # Slayt 95: Genetik, Çevresel ve Beslenmeye Bağlı Hastalıklar Karşılaştırması
    slides.append({
        "id": "k1-26-s95",
        "title": "Genetik, Çevresel ve Beslenmeye Bağlı Hastalıklar Karşılaştırması",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 95,
        "narrative": (
            "Ders 26 boyunca incelediğimiz tüm hastalık sınıflarının patogenetik mekanizma ve klinik kesişim matrisi: "
            "1. **Mendel Hastalıkları:** Yüksek penetrans, kalıtsal tek gen arızası (Marfan - FBN1 elastik lif yıkımı; Kistik Fibrozis - CFTR dehidrate mukus). "
            "2. **Sitogenetik Bozukluklar:** Mikroskobik kromozom sayısı ve yapı sapmaları (Down Sendromu trizomi 21; Turner 45,X; Klinefelter 47,XXY). "
            "3. **Çevresel Toksinler:** Ağır metaller (Kurşun nörolojik ve hematolojik; Cıva Minamata serebral hasarı; Arsenik kutanöz hiperkeratoz ve kanser; Kadmiyum İtai-İtai osteomalazisi). "
            "Hava kirleticileri (Ozon lipid peroksidasyonu; PM2.5 miyokard enfarktüsü ve alveoler harabiyet). "
            "4. **Kişisel Çevre:** Tütün (akciğer kanseri, sentriasiner KOAH, ateroskleroz); Alkol (hepatik steatoz, Wernicke-Korsakoff, siroz). "
            "5. **Beslenme Bozuklukları:** Marasmus (kalori yok, somatik yıkım); Kwashiorkor (protein yok, hipoalbüminemik ödem, steatoz); Obezite (viseral yağ, leptin direnci, kanser)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Patolojide Üçlü Çerçevenin Büyük Karşılaştırma Matrisi",
                ["Patoloji Grubu", "Temel Moleküler / Çevresel Tetikleyici", "Prototip Hastalık", "En Ağır Klinik Sonuç"],
                [
                    ["Monogenik Mendel", "Tek gen mutasyonu (FBN1 / CFTR)", "Marfan / Kistik Fibrozis", "Aort diseksiyonu / Bronşiektazi"],
                    ["Sitogenetik", "Mayoz I ayrılamaması (Trizomi)", "Down Sendromu (Trizomi 21)", "AV septal defekt, lösemi, Alzheimer"],
                    ["Ağır Metal Toksisitesi", "-SH enzim blokajı ve katyon taklidi", "Kurşun / Cıva zehirlenmesi", "Ensefalopati, anemi, Minamata"],
                    [
                        "Kişisel Toksikoloji",
                        "Tütün katranı (PAH) ve etanol (NADH)",
                        {"text": "Akciğer karsinomu, KOAH ve Karaciğer Sirozu", "isMasked": True, "hint": "Sigara ve alkolün sebep olduğu geri dönüşsüz solunum ve hepatik yıkım tabloları"},
                        "Fatal miyokard enfarktüsü ve hepatik koma"
                    ],
                    ["Beslenme Bozukluğu", "Somatik vs viseral protein yıkımı", "Marasmus / Kwashiorkor", "Sekonder immün yetmezlik ve letal sepsis"]
                ]
            ),
            make_active_recall(
                "Tüm Ders 26 boyunca işlenen genetik, çevresel ve besinsel patolojilerin ortak kesişiminde yer alan ve hastalıkların ortaya çıkışını yöneten üçlü çerçeve hangi üç saç ayağından oluşur?",
                "Genetik zemin, çevresel maruziyet ile yaşam tarzı ve beslenme dengesidir.",
                "Kalıtsal yatkınlık, dış fiziksel toksinler ve metabolik gıda alımının kesiştiği biyolojik model"
            )
        ]
    })

    # Slayt 96: Robbins Patoloji Temelli Altın Sınav Spotları
    slides.append({
        "id": "k1-26-s96",
        "title": "Robbins Patoloji Temelli Altın Sınav Spotları",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 96,
        "narrative": (
            "Patoloji kurul, komite ve TUS sınavlarında en sık soru yapılan yüksek verimli Robbins altın spotları: "
            "1. **Genom ve Epigenetik:** İnsan genomunda protein kodlayan kısım yalnızca **%1.5'tir (~19.000 gen)**. "
            "Promotör CpG adalarının hipermetilasyonu genleri susturur; histon asetilasyonu kromatini açar. "
            "2. **Marfan Sendromu:** FBN1 mutasyonu; patogenezde **aşırı TGF-β sinyali**; lens yukarı-dışa (superotemporal) kayar; "
            "en ölümcül komplikasyon kistik medial nekroza bağlı **aort diseksiyonu ve rüptürüdür**. "
            "3. **Kistik Fibrozis:** CFTR (7q31.2); en sık mutasyon **Delta-F508** (ER katlanma kusuru); ter testi >60 mEq/L; "
            "erişkin erkekte bilateral vas deferens agenezisi (CBAVD); akciğerde kronik mukoid Pseudomonas aeruginosa. "
            "4. **Ağır Metaller:** Kurşunda eritrositlerde **bazofilik beneklenme**, metafizlerde radyoopak kurşun çizgileri ve erişkinde **düşük el**; "
            "Cıvada Minamata hastalığı; Arsenikte palmar hiperkeratoz; Kadmiyumda İtai-İtai kemik kırıkları. "
            "5. **Malnütrisyon:** Marasmusta kalori eksik, somatik kas erir, albümin normal, ödem yok; Kwashiorkorda protein eksik, "
            "viseral bölme çöker, albümin <2.5, **anazarka ödem, yağlı karaciğer ve bayrak işareti saç** görülür. "
            "6. **Obezite:** Leptin kanda çok yüksek (direnç var); adiponektin paradoksal olarak düşüktür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Sınav Kazandıran Patoloji Zıtlıkları Kataloğu",
                ["Hastalık İkilisi", "Birinci Hastalığın İmzası", "İkinci Hastalığın İmzası"],
                [
                    ["Lens Subluksasyonu", "Marfan: YUKARI VE DIŞA (superotemporal)", "Homosistinüri: AŞAĞI VE İÇE (inferonazal)"],
                    ["Malnütrisyon Ödemi", "Marasmus: ÖDEM KESİNLİKLE YOKTUR", "Kwashiorkor: YAYGIN NUTRİSYONEL ÖDEM VARDIR"],
                    [
                        "Yağ Hormonları Düzeyi",
                        "Leptin: Obezitede aşırı artar (dirençli)",
                        {"text": "Adiponektin: Obezitede paradoksal olarak azalır", "isMasked": True, "hint": "Obezitede düşerek insülin direncini patlatan koruyucu hormon"}
                    ],
                    ["Amfizem Yerleşimi", "Sigara: Sentriasiner (Üst loblar)", "Alfa-1 Antitripsin Eksikliği: Panasiner (Alt loblar)"]
                ]
            ),
            make_active_recall(
                "Lens subluksasyonu saptanan uzun boylu iki hastadan Marfan sendromlu olanda lens hangi yöne, homosistinürili olanda ise hangi yöne doğru yer değiştirir?",
                "Marfanda yukarı ve dışa; homosistinüride ise aşağı ve içe doğru kayar.",
                "Biri superotemporal zonül gevşekliği, diğeri inferonazal metabolik lizis yönü"
            )
        ]
    })

    # Slayt 97: Çıkmış Kurul ve TUS Soru Tiplerinin Patolojik Analizi
    slides.append({
        "id": "k1-26-s97",
        "title": "Çıkmış Kurul ve TUS Soru Tiplerinin Patolojik Analizi",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 97,
        "narrative": (
            "Patoloji sınavlarında klinik senaryolar üzerinden sorulan tipik vaka kurguları ve çözümleri: "
            "1. **Vaka 1 (Marfan Aort Felaketi):** 22 yaşında uzun boylu, parmakları aşırı uzun genç bir basketbolcu maç sırasında ani yırtıcı göğüs ağrısı "
            "ve senkop ile yere yığılıyor. Otopsi bulgusu: Kistik medial nekroz zemininde Stanford Tip A aort diseksiyonu ve hemoperikardiyum. "
            "2. **Vaka 2 (Kistik Fibrozis CBAVD):** 28 yaşında erkek hasta çocuk sahibi olamama nedeniyle başvuruyor. Sperm analizinde azospermi, "
            "muayenede vas deferenslerin bilateral palpe edilemediği saptanıyor. Çocuklukta tekrarlayan bronşit ve sinüzit öyküsü var. "
            "En olası genetik defekt: CFTR gen mutasyonu. "
            "3. **Vaka 3 (Kurşun Zehirlenmesi):** Eski bir evde yaşayan 3 yaşında çocukta davranış bozukluğu, hırçınlık, mikrositer anemi saptanıyor. "
            "Periferik yaymada eritrositlerde bazofilik beneklenme, diz grafisinde metafizlerde beyaz çizgiler izleniyor. Tanı: Kurşun zehirlenmesi. "
            "4. **Vaka 4 (Kwashiorkor):** Annesi sütten kestikten sonra yalnızca pirinç lapasıyla beslenen 18 aylık çocukta bacaklarda gode bırakan ödem, "
            "şiş karın, karaciğerde yağlanma ve saçta açık-koyu çizgilenme görülüyor. Tanı: Kwashiorkor."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "32 yaşında bir erkek hasta primer infertilite şikayetiyle üroloji kliniğine başvuruyor. Spermiyogramda seminal sıvı hacmi düşük ve sperm hücresi hiç izlenmiyor (azospermi). Skrotal muayenede testis boyutları normal ancak vas deferensler bilateral olarak palpe edilemiyor. Hormon tetkiklerinde FSH, LH ve Testosteron düzeyleri tamamen normal bulunuyor. Akciğer grafisinde bilateral bronşiektatik kistik alanlar izleniyor.",
                "Bu hastada altta yatan primer genetik hastalık ve tanısal doğrulama için yapılması gereken ilk tetkik hangisidir?",
                [
                    {
                        "text": "Kistik Fibrozis; CFTR gen mutasyon analizi veya Ter Klorür Testi planlanmalıdır",
                        "isCorrect": True,
                        "explanation": "Doğrudur; erişkin erkekte bilateral vas deferens agenezisi (CBAVD) ve bronşiektazi kistik fibrozisin klasik klinik prezentasyonudur."
                    },
                    {
                        "text": "Klinefelter Sendromu; Karyotip analizi yapılarak 47,XXY aranmalıdır",
                        "isCorrect": False,
                        "explanation": "Hatalı; Klinefelter'de testisler küçüktür, FSH/LH çok yüksektir ve vas deferensler anatomik olarak mevcuttur."
                    },
                    {
                        "text": "Marfan Sendromu; FBN1 gen dizilemesi istenmelidir",
                        "isCorrect": False,
                        "explanation": "Hatalı; Marfan sendromu azospermi ve vas deferens agenezisi yapmaz."
                    }
                ]
            ),
            make_micro_quiz(
                "Eski kurşun bazlı boyalarla boyanmış bir evde yaşayan ve pika öyküsü olan 2 yaşındaki bir çocuğun periferik kan yaymasında mikrositer hipokromik anemiye eşlik eden hangi patognomonik eritrosit inklüzyonu kurşun zehirlenmesini kesinleştirir?",
                {
                    "A": "Eritrosit içi bazofilik beneklenme (rRNA agregatları)",
                    "B": "Howell-Jolly cisimcikleri (DNA artıkları)",
                    "C": "Heinz cisimcikleri (denatüre hemoglobin)",
                    "D": "Auer çubukları",
                    "E": "Döhle cisimcikleri"
                },
                "A",
                {
                    "A": "Doğrudur; pirimidin-5'-nükleotidaz inhibisyonuna bağlı rRNA birikimi bazofilik beneklenme yapar ve kurşun için karakteristiktir.",
                    "B": "Yanlış; Howell-Jolly splenektomide görülür.",
                    "C": "Yanlış; Heinz cisimcikleri G6PD eksikliğindedir.",
                    "D": "Yanlış; Auer rodları akut miyeloid lösemidedir.",
                    "E": "Yanlış; Döhle cisimcikleri ağır enfeksiyon nötrofillerindedir."
                }
            )
        ]
    })

    # Slayt 98: Birinci Basamak ve Klinik Pratikte Pediatrik/Çevresel Vaka Yönetimi
    slides.append({
        "id": "k1-26-s98",
        "title": "Birinci Basamak ve Klinik Pratikte Pediatrik/Çevresel Vaka Yönetimi",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 98,
        "narrative": (
            "Genel hekimlik ve sahada aile hekimliği uygulamalarında çevresel ve pediatrik patolojilere yaklaşım ilkeleri: "
            "1. **Çocukluk Çağı Anemilerinde Kurşun Şüphesi:** Tedaviye dirençli mikrositer anemisi olan veya gelişim geriliği gösteren "
            "çocuklarda mutlaka ev ortamı (eski boyalar, su tesisatı) sorgulanmalı ve venöz kan kurşun düzeyi istenmelidir. "
            "2. **Bebeklerin Güvenli Uyku Protokolü:** SIDS'i önlemek için tüm ailelere bebeklerin ilk 1 yıl **kesinlikle sırtüstü (supine)** "
            "yatırılması, yatakta pelüş oyuncak/yastık bulundurulmaması ve evde asla sigara içilmemesi anlatılmalıdır. "
            "3. **Malnütrisyon Taraması:** Sağlık ocağına gelen her çocukta boya göre ağırlık ve **orta üst kol çevresi (MUAC)** ölçülmeli; "
            "ödem varlığı ayak sırtından kontrol edilmelidir. "
            "4. **Kişiselleştirilmiş İlaç Yönetimi:** Yavaş ve hızlı metabolize edici polimorfizmler göz önüne alınmalı; "
            "özellikle dar terapötik aralıklı ilaçlarda farmakogenomik riskler unutulmamalıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Birinci Basamakta Şüpheli Çocukluk Malnütrisyonu Yönetimi",
                [
                    "1. Antropometrik Tarama: Çocuğun boy, kilo ve orta üst kol çevresinin (MUAC) ölçülmesi",
                    "2. Ödem Kontrolü: İki taraflı ayak sırtına parmak basılarak gode bırakan nutrisyonel ödem aranması",
                    "3. Sınıflandırma: Ödem varsa Kwashiorkor; şiddetli kas erimesi ve ödem yoksa Marasmus tanısı",
                    "4. Metabolik Stabilizasyon: Hipoglisemi, hipotermi ve elektrolit dengesizliğinin acil düzeltilmesi",
                    "5. Kademeli Beslenme: Yeniden besleme sendromunu (refeeding) önlemek için dikkatli kalori ve protein artışı"
                ]
            ),
            make_cloze(
                "Ani Bebek Ölümü Sendromunu engellemek amacıyla birinci basamak hekimlerinin ailelere vermesi gereken en kritik hayat kurtarıcı uyku pozisyonu önerisi bebeğin sırtüstü yatırılmasıdır.",
                "sırtüstü",
                "Bebeğin hava yolunu açık tutarak asfiksi riskini sıfırlayan güvenli yatak pozisyonu"
            )
        ]
    })

    # Slayt 99: Biyopsikososyal Tıp ve Sağlık Eşitsizliklerinin Aşılması
    slides.append({
        "id": "k1-26-s99",
        "title": "Biyopsikososyal Tıp ve Sağlık Eşitsizliklerinin Aşılması",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 99,
        "narrative": (
            "Tıp bilimi yalnızca hücresel ve moleküler lezyonları onarmakla yetinemez; insanı çevresiyle bir bütün olarak ele almalıdır: "
            "1. **Biyopsikososyal Model:** "
            "- Bir hastanın patolojisi; genetik mutasyonu (biyolojik), maruz kaldığı stres, bağımlılık ve yeme davranışı (psikolojik) "
            "ile yaşadığı mahalle, hava kirliliği ve gelir düzeyi (sosyal) arasındaki kesişimde biçimlenir. "
            "2. **Gezegensel Sağlık (Planetary Health):** "
            "- İnsan sağlığı Dünya'nın ekolojik dengesine göbekten bağlıdır. Fosil yakıtların terk edilmesi, temiz enerjiye geçiş ve "
            "hava kirliliğinin önlenmesi; kardiyovasküler ölümleri ve solunum yetmezliklerini cerrahi müdahalelerden çok daha fazla azaltır. "
            "3. **Hekimin Toplumsal Savunuculuk Rolü:** "
            "- Geleceğin hekimi sadece reçete yazan bir teknisyen değil; temiz su, temiz hava, güvenli barınma ve sağlıklı gıdaya "
            "erişimi savunan bir toplum önderi olmak zorundadır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Biyomedikal İndirgemecilik vs Biyopsikososyal Bütüncül Tıp",
                "Dar Biyomedikal Yaklaşım",
                "Hastalığı sadece bozuk bir gen veya kimyasal reaksiyon olarak görmek; hastanın yaşadığı çevreyi ve yoksulluğu göz ardı etmek",
                "Bütüncül Biyopsikososyal Yaklaşım",
                "Genetik zemini çevresel maruziyetler, beslenme adaleti ve sosyal belirleyicilerle birlikte ele alarak kökten iyileşme sağlamak"
            ),
            make_active_recall(
                "İnsan sağlığını ve patolojisini sadece genetik ve hücresel mekanizmalarla değil, psikolojik süreçler ve sosyoekonomik çevresel koşullarla birlikte bir bütün olarak ele alan modern tıbbi yaklaşım modeline ne ad verilir?",
                "Biyopsikososyal tıp modelidir.",
                "Biyolojik, psikolojik ve sosyal faktörlerin hastalık patogenezindeki dinamik etkileşimi"
            )
        ]
    })

    # Slayt 100: Checkpoint 10 / Büyük Kapanış
    slides.append({
        "id": "k1-26-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Genetik, Pediatrik ve Çevresel Patoloji Büyük Özeti",
        "section": "Moleküler Patoloji ve Büyük Sentez",
        "slideNumber": 100,
        "narrative": (
            "Ders 26'nın bu final kontrol noktasında, 100 slaytlık dev genetik, pediatrik ve çevresel patoloji maratonunu özetliyoruz: "
            "1. **Genom ve Varyasyon:** 3.3 milyar baz çifti; %1.5 protein kodlayan ekzon (~19.000 gen); SNP farmakogenomiği, CNV otizmi belirler; CpG metilasyonu gen susturur. "
            "2. **Marfan Sendromu:** FBN1 (15q21); aşırı TGF-β sinyali; araknodaktili, pektus, lensin yukarı-dışa subluksasyonu; kistik medial nekroz ve ölümcül aort diseksiyonu. "
            "3. **Kistik Fibrozis:** CFTR (7q31.2, OR); Delta-F508 ER katlanma defekti; solunumda dehidrate mukus, terde klor artışı (>60 mEq/L); mukoid Pseudomonas ve CBAVD azospermi. "
            "4. **Çevresel Toksinler:** Ozon lipid peroksidasyonu yapar; PM2.5 alveolleri geçip MI tetikler; radon sigara içmeyende akciğer kanseri yapar. "
            "5. **Ağır Metaller:** Kurşun (ALA-dehidrataz felci, bazofilik beneklenme, kurşun çizgisi, düşük el); Cıva (Minamata mikrosefali); Arsenik (hiperkeratoz, kanser); Kadmiyum (İtai-İtai). "
            "6. **Tütün ve Alkol:** Sigara (PAH ile TP53 mutasyonu, KOAH amfizemi, ateroskleroz); Alkol (NADH fırlaması, hepatik steatoz, Wernicke). "
            "7. **Malnütrisyon:** Marasmus (kalori yok, somatik kas erir, ödem yok); Kwashiorkor (protein yok, albümin çöker, ödem, yağlı karaciğer, bayrak saçı). "
            "8. **Obezite:** Viseral yağ portal FFA boşaltır; leptin yüksek (dirençli), adiponektin paradoksal olarak düşüktür; kanser riski (endometrium). "
            "9. **Diyet ve Pediatri:** Aflatoksin B1 TP53 kodon 249 mutasyonu ile HCC; C vitamini skorbüt; prematürede RDS hiyalin membran; Nöroblastomda N-MYC amplifikasyonu. "
            "10. **Moleküler Tedavi:** EGFR TKI (Gefitinib), BRAF V600E (Vemurafenib), HER2 amplifikasyonu FISH ve Trastuzumab."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s100-1",
                "Kanser hücrelerinde HER2 gen amplifikasyonunu ve aşırı protein ekspresyonunu tespit ederek hedefe yönelik monoklonal antikor tedavisi uygunluğunu belirleyen sitogenetik yöntem nedir?",
                "Floresan in situ hibridizasyondur (FISH).",
                "Işıma veren probların lam üzerindeki kromozoma kilitlendiği mikroskobik teknik",
                "Moleküler Tanı"
            ),
            make_flashcard(
                "k1-26-fc-s100-2",
                "Malign melanom ve tiroid papiller karsinomunda görülen BRAF genindeki V600E mutasyonuna karşı geliştirilen hedefe yönelik inhibitör ajan nedir?",
                "Vemurafenib ilacıdır (BRAF inhibitörü).",
                "Valin yerine glutamat geçen serin-treonin kinaz aktivitesini selektif durduran küçük molekül",
                "Hedefe Yönelik Tedavi"
            ),
            make_flashcard(
                "k1-26-fc-s100-3",
                "İnsan genomunun yaklaşık yüzde kaçı doğrudan fonksiyonel proteinleri kodlayan ekzonik dizilerden meydana gelir?",
                "Yalnızca yüzde bir buçukluk kısımdır.",
                "Nükleotid diziliminin geriye kalan düzenleyici mimarisi dışındaki minimal kodlama payı",
                "Genom Özeti"
            )
        ],
        "interactiveElements": [
            make_table(
                "Ders 26: Büyük Kapanış ve Master Sentez Matrisi",
                ["Büyük Disiplin", "Temel Patolojik / Moleküler İlke", "Altın Standart Belirteç", "Hayat Kurtarıcı Klinik Yaklaşım"],
                [
                    ["Genom Mimarisi", "3.3 milyar bç, %1.5 protein kodlar, regülatör ncRNA", "CpG hipermetilasyonu gen susturur", "Epigenetik reversibl tedavi (DNMT inh)"],
                    ["Mendel Hastalıkları", "Marfan FBN1 (aşırı TGF-beta), KF CFTR klor kanalı", "Kistik medial nekroz / Ter klorürü >60", "Aort takibi / Mukolitik ve CFTR modülatör"],
                    ["Çevre ve Toksikoloji", "Ozon ROS yapar, PM2.5 dolaşıma sızar, kurşun -SH felç eder", "Bazofilik beneklenme, kurşun çizgisi", "Kaynak eliminasyonu, DMSA şelasyonu"],
                    [
                        "Kişisel Bağımlılık",
                        "Tütün PAH TP53 yıkar, Alkolde aşırı NADH steatoz yapar",
                        {"text": "Sentriasiner amfizem ve Mallory-Denk cisimcikleri", "isMasked": True, "hint": "Sigara ve alkolün akciğer ve karaciğerdeki karakteristik histopatolojik lezyonları"},
                        "Sigara bırakma, tiamin replasmanı, siroz takibi"
                    ],
                    ["Beslenme Patolojisi", "Marasmus somatik yıkım, Kwashiorkor viseral çöküş", "Kwashiorkorda ödem ve bayrak saçı", "Kademeli besleme, enfeksiyon kontrolü"],
                    ["Hassas Tıp", "Sürücü onkojenik mutasyonların haritalanması", "EGFR, BRAF V600E, HER2 FISH", "Hedefe yönelik kinaz inhibitörleri ve monoklonal antikorlar"]
                ]
            ),
            make_micro_quiz(
                "Tüm Ders 26 boyunca incelenen patolojik mekanizmalar göz önüne alındığında, aşağıdaki eşleştirmelerden hangisi BİLİMSEL OLARAK KUSURSUZ VE DOĞRUDUR?",
                {
                    "A": "Marfan Sendromu - FBN1 mutasyonu zemininde aşırı serbest TGF-beta sinyalizasyonu ve aort kökü diseksiyonu",
                    "B": "Kwashiorkor - Somatik iskelet kası erimesi varken serum albümin düzeyinin tamamen normal kalması",
                    "C": "Kurşun Zehirlenmesi - Karaciğerde aşırı NADH birikimi sonucu oluşan makroveziküler yağlanma",
                    "D": "Obezite - Kanda leptin hormonunun sıfıra inmesi ve adiponektinin tavan yapması",
                    "E": "Down Sendromu - Fibrillin-1 genindeki delesyon sonucu lensin aşağı ve içe kayması"
                },
                "A",
                {
                    "A": "Doğrudur; Marfan sendromu FBN1 defektiyle elastik lif mimarisini ve TGF-beta sekestrasyonunu bozar, letal aort diseksiyonu yapar.",
                    "B": "Yanlış; bu marasmustur, kwashiorkorda albümin çöker.",
                    "C": "Yanlış; NADH birikimi alkol metabolizmasındadır.",
                    "D": "Yanlış; obezitede leptin yüksek dirençli, adiponektin düşüktür.",
                    "E": "Yanlış; Down trizomi 21'dir, FBN1 Marfan'dadır."
                }
            )
        ]
    })

    return slides
