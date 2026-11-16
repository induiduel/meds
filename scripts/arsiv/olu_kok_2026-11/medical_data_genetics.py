# -*- coding: utf-8 -*-
"""
Genetics, Chromosomal Anomalies, Dysmorphology & Metabolic Inborn Errors Data
"""

GENETICS_CONCEPTS = [
    # 1. Kromozom Sayı ve Yapı Anomalileri
    ("Down Sendromu (Trizomi 21)", ["Tıbbi Genetik", "Pediatri", "Kadın Hastalıkları ve Doğum"], [
        "down", "trizomi 21", "21 kromozom", "ense saydamligi", "nt", "av kanal defekti", "endokardiyal yastik",
        "cift kabarcik", "double bubble", "simian cizgisi", "brushfield lekeleri", "hipotoni", "makroglossi",
        "burun kemigi hipoplazisi", "duodenal atrezi", "karyotip 47", "robertsonian translokasyon", "anne yasi"
    ]),
    ("Edwards Sendromu (Trizomi 18)", ["Tıbbi Genetik", "Pediatri"], [
        "edwards", "trizomi 18", "18 kromozom", "rocker bottom ayagi", "mikrognati", "ust uste binen parmaklar",
        "clenched hand", "oksiput belirginligi", "dusuk kulak", "vsd", "omfalosel"
    ]),
    ("Patau Sendromu (Trizomi 13)", ["Tıbbi Genetik", "Pediatri"], [
        "patau", "trizomi 13", "13 kromozom", "holoprozensefali", "yarik dudak damak", "mikroftalmi",
        "polidaktili", "kutis aplezi", "skalp defekti", "polikistik bobrek"
    ]),
    ("Turner Sendromu (45,X0)", ["Tıbbi Genetik", "Pediatri", "Kadın Hastalıkları ve Doğum", "Dahiliye"], [
        "turner", "45 x0", "45 x", "yele boyun", "kistik higroma", "primer amenore", "aort koarktasyonu",
        "bikuspid aort", "streak over", "cizgi gonad", "kisa boy", "cubitus valgus", "genis gogus kalkan gogus"
    ]),
    ("Klinefelter Sendromu (47,XXY)", ["Tıbbi Genetik", "Dahiliye", "Üroloji"], [
        "klinefelter", "47 xxy", "jinekomasti", "azospermi", "kucuk sert testisler", "uzun boy", "infertilite",
        "barr cisimcigi", "fsh yuksekligi", "hipogonadotropik hipogonadizm", "leydig disfonksiyonu"
    ]),
    ("Triple X Sendromu (47,XXX)", ["Tıbbi Genetik"], [
        "triple x", "47 xxx", "super disi", "iki barr cisimcigi", "uzun boy", "ogrenme guclugu"
    ]),
    ("XYY Sendromu (47,XYY - Jacob Sendromu)", ["Tıbbi Genetik"], [
        "xyy", "47 xyy", "jacob", "super erkek", "siddetli akne", "uzun boy", "davranis problemleri"
    ]),
    ("Cri-du-Chat Sendromu (5p Delesyonu)", ["Tıbbi Genetik", "Pediatri"], [
        "cri du chat", "kedi miyavlamasi", "5p delesyonu", "5p delesyon", "mikrosefali", "hipertelorizm",
        "epikanik katlanti", "mental retardasyon", "laringeal disgenezi"
    ]),
    ("Wolf-Hirschhorn Sendromu (4p Delesyonu)", ["Tıbbi Genetik", "Pediatri"], [
        "wolf hirschhorn", "4p delesyonu", "yunan savasci migferi", "greek warrior helmet", "kolobom", "yarik damak"
    ]),
    ("DiGeorge Sendromu (22q11.2 Delesyonu)", ["Tıbbi Genetik", "Pediatri", "Tıbbi İmmünoloji"], [
        "digeorge", "22q11 2", "velokardiyofasiyal", "catch 22", "timus aplazisi", "t hucre eksikligi",
        "paratiroid aplazisi", "hipokalsemi", "tetani", "trunkus arteriyozus", "fallot tetralojisi", "yarik damak"
    ]),
    ("Williams Sendromu (7q11.23 Delesyonu)", ["Tıbbi Genetik", "Pediatri", "Kardiyoloji"], [
        "williams", "7q11 23", "supravalvuler aort stenozu", "peri elfin yuzu", "asiri sosyal kisilik",
        "kokteyl partisi kisiligi", "hiperkalsemi", "elastin gen delesyonu", "yildizsi iris"
    ]),
    ("Prader-Willi Sendromu (15q11-q13 Paternal Delesyon)", ["Tıbbi Genetik", "Pediatri", "Endokrinoloji"], [
        "prader willi", "15q11 q13", "paternal delesyon", "genomik imprinting", "hiperfaji", "obezite",
        "hipotoni", "hipogonadizm", "kucuk el ayak", "badem goz", "uniparental maternal dizomi"
    ]),
    ("Angelman Sendromu (15q11-q13 Maternal Delesyon)", ["Tıbbi Genetik", "Pediatri", "Nöroloji"], [
        "angelman", "15q11 q13", "maternal delesyon", "ube3a", "mutlu kukla", "happy puppet",
        "uygunsuz kahkahalar", "ataksik yuruyus", "agir zeka geriligi", "uniparental paternal dizomi"
    ]),
    ("Smith-Magenis Sendromu (17p11.2 Delesyonu)", ["Tıbbi Genetik", "Pediatri"], [
        "smith magenis", "17p11 2", "rai1 geni", "kendine zarar verme", "tirnak sokme", "uyku bozuklugu ters sirkadiyen"
    ]),
    ("Miller-Dieker Sendromu (17p13.3 Delesyonu - Lissensefali)", ["Tıbbi Genetik", "Nöroloji"], [
        "miller dieker", "17p13 3", "lis1", "pafah1b1", "lissensefali", "duz beyin", "girussuz beyin", "agir epilepsi"
    ]),

    # 2. Triplet Tekrar Artış Hastalıkları
    ("Huntington Hastalığı (CAG Tekrarı)", ["Tıbbi Genetik", "Nöroloji"], [
        "huntington", "cag tekrari", "kaudat nukleus atrofisi", "kore", "otozomal dominant", "antisipasyon",
        "avolüsyon", "gaba azalmasi", "asetilkolin azalmasi", "erken demans"
    ]),
    ("Fragil X Sendromu (CGG Tekrarı - FMR1)", ["Tıbbi Genetik", "Pediatri", "Psikiyatri"], [
        "fragil x", "cgg tekrari", "fmr1", "makroorsidizm", "buyuk kulaklar", "uzun yuz", "mental retardasyon",
        "otizm spektrum", "mitral kapak prolapsusu", "hipermobilite"
    ]),
    ("Miyotonik Distrofi Tip 1 (CTG Tekrarı - DMPK)", ["Tıbbi Genetik", "Nöroloji"], [
        "miyotonik distrofi", "ctg tekrari", "dmpk", "miyotoni", "katarakt", "frontal kellik", "gonadal atrofi",
        "kardiyak ileti bozukluklari", "kas erimesi"
    ]),
    ("Friedreich Ataksisi (GAA Tekrarı - Frataksin)", ["Tıbbi Genetik", "Nöroloji", "Kardiyoloji"], [
        "friedreich ataksisi", "gaa tekrari", "frataksin", "demir birikimi mitokondri", "hipertrofik kardiyomiyopati",
        "pes kavus", "kifoskolyoz", "derin duyu kaybi", "babinski pozitifligi", "diyabet"
    ]),
    ("Spinobulbar Muskuler Atrofi (Kennedy Hastalığı - CAG Tekrarı)", ["Tıbbi Genetik", "Nöroloji"], [
        "kennedy hastaligi", "spinobulbar muskuler atrofi", "sbma", "cag tekrari", "androjen reseptor mutasyonu",
        "fasikulasyon", "jinekomasti", "bulbar paralizi"
    ]),

    # 3. Bağ Dokusu ve İskelet Displazileri
    ("Marfan Sendromu (FBN1 Fibrillin-1)", ["Tıbbi Genetik", "Kardiyoloji", "Göz Hastalıkları"], [
        "marfan", "fbn1", "fibrillin 1", "araknodaktili", "orumcek parmak", "aort kok dilatasyonu", "aort diseksiyonu",
        "lens subluksasyonu yukari disa", "pektus ekskavatum", "uzun ekstremiteler", "hipermobilite"
    ]),
    ("Ehlers-Danlos Sendromu (Kollajen Sentez Bozukluğu)", ["Tıbbi Genetik", "Romatoloji"], [
        "ehlers danlos", "kollajen sentez", "hiperelastik cilt", "eklem hipermobilitesi", "kolay morarma",
        "col5a1", "col3a1", "vaskuler tip", "arter rupture", "organ perforasyonu"
    ]),
    ("Osteogenezis İmperfekta (Kırılgan Kemik Hastalığı - COL1A1/COL1A2)", ["Tıbbi Genetik", "Ortopedi ve Travmatoloji"], [
        "osteogenezis imperfekta", "kirilgan kemik", "mavi sklera", "col1a1", "col1a2", "tip 1 kollajen",
        "iletim tipi isitme kaybi", "tekrarlayan kemik kiriklari", "dentinogenezis imperfekta"
    ]),
    ("Akondroplazi (FGFR3 Mutasyonu)", ["Tıbbi Genetik", "Ortopedi ve Travmatoloji"], [
        "akondroplazi", "fgfr3", "orantisiz cucelik", "rizomelik kisalik", "makrosefali", "trident el",
        "uc uclu el", "foramen magnum darligi", "lomber lordoz", "endokondral kemiklesme defekti"
    ]),
    ("Tanatoforik Displazi (FGFR3 Ağır Displazi)", ["Tıbbi Genetik", "Pediatri"], [
        "tanatoforik displazi", "fgfr3", "telefon ahizesi femur", "yonca yapragi kafatasi", "olumcul cucelik", "akciger hipoplazisi"
    ]),

    # 4. Lizozomal Depo Hastalıkları
    ("Gaucher Hastalığı (Glukoserebrozidaz Eksikliği)", ["Tıbbi Genetik", "Hematoloji", "Pediatri"], [
        "gaucher", "glukoserebrozidaz", "glukoserebrozit", "burusuk kagit sitoplazma", "erlenmeyer sisesi kemik deformitesi",
        "hepatosplenomegali", "pansitopeni", "kemik krizleri", "aseptik nekroz", "enzim replasman tedavisi"
    ]),
    ("Tay-Sachs Hastalığı (Heksozaminidaz A Eksikliği)", ["Tıbbi Genetik", "Pediatri", "Nöroloji"], [
        "tay sachs", "heksozaminidaz a", "gm2 gangliozid", "kiraz kirmizisi makula", "cherry red spot",
        "asiri irkilme refleksi", "hepatosplenomegali yoktur", "noromator regresyon", "askenazi yahudileri"
    ]),
    ("Niemann-Pick Hastalığı (Sfingomiyelinaz Eksikliği)", ["Tıbbi Genetik", "Pediatri"], [
        "niemann pick", "sfingomiyelinaz", "sfingomiyelin", "kopuksu histiyositler", "foam cells",
        "kiraz kirmizisi makula", "cherry red spot", "hepatosplenomegali vardir", "norodegenerasyon"
    ]),
    ("Fabry Hastalığı (Alfa-Galaktozidaz A Eksikliği)", ["Tıbbi Genetik", "Nefroloji", "Dermatoloji"], [
        "fabry", "alfa galaktozidaz a", "seramid trihekzozid", "globotriaozilseramid", "anjiyokeratom",
        "akroparestezi yanma agri", "hipohidrozis", "kornea vertisillata", "erken bobrek yetmezligi", "x e bagli"
    ]),
    ("Krabbe Hastalığı (Galaktoserebrozidaz Eksikliği)", ["Tıbbi Genetik", "Nöroloji"], [
        "krabbe", "galaktoserebrozidaz", "psikosentez", "globoid hucreler", "optik atrofi", "periferik noropati", "demiyelinizasyon"
    ]),
    ("Metakromatik Lökodistrofi (Arilsülfataz A Eksikliği)", ["Tıbbi Genetik", "Nöroloji"], [
        "metakromatik lokodistrofi", "arilsulfataz a", "sulfatid birikimi", "santral demiyelinizasyon", "krezil moru metakromazi"
    ]),
    ("Hurler Sendromu (MPS Tip 1 - Alfa-L-İduronidaz)", ["Tıbbi Genetik", "Pediatri"], [
        "hurler", "mps tip 1", "alfa l iduronidaz", "dermatan sulfat", "heparan sulfat", "kornea bulanikligi",
        "kaba yuz gargoylizm", "hepatosplenomegali", "disostozis multipleks", "erken kalp yetmezligi"
    ]),
    ("Hunter Sendromu (MPS Tip 2 - İduronat Sülfataz)", ["Tıbbi Genetik", "Pediatri"], [
        "hunter", "mps tip 2", "iduronat sulfataz", "x e bagli", "kornea bulanikligi yoktur", "agresif davranis", "kaba yuz"
    ]),

    # 5. Glikojen Depo Hastalıkları
    ("von Gierke Hastalığı (Glikojen Depo Tip 1 - G6Paz)", ["Tıbbi Genetik", "Pediatri", "Tıbbi Biyokimya"], [
        "von gierke", "glikojen depo tip 1", "glukoz 6 fosfataz", "agir hipoglisemi aclik", "laktik asidoz",
        "hiperurisemi gut", "hiperlipidemi", "oyuncak bebek yuzu", "hepatomegali", "karaciger adenomu"
    ]),
    ("Pompe Hastalığı (Glikojen Depo Tip 2 - Asit Maltaz)", ["Tıbbi Genetik", "Kardiyoloji", "Pediatri"], [
        "pompe", "glikojen depo tip 2", "asit alfa glukozidaz", "asit maltaz", "lizozomal depo",
        "agir kardiyomegali", "kalp yetmezligi", "hipotoni floppy infant", "pas pozitif glikojen"
    ]),
    ("Cori / Forbes Hastalığı (Glikojen Depo Tip 3 - Debranching Enzim)", ["Tıbbi Genetik", "Tıbbi Biyokimya"], [
        "cori", "forbes", "glikojen depo tip 3", "dallanma yikici enzim", "debranching enzim", "limit dekstrinoz", "hafif hipoglisemi"
    ]),
    ("Andersen Hastalığı (Glikojen Depo Tip 4 - Branching Enzim)", ["Tıbbi Genetik", "Gastroenteroloji"], [
        "andersen", "glikojen depo tip 4", "dallanma enzimi", "branching enzim", "amilopektinoz", "erken siroz", "olumcul hepatopati"
    ]),
    ("McArdle Hastalığı (Glikojen Depo Tip 5 - Kas Glikojen Fosforilaz)", ["Tıbbi Genetik", "Nöroloji"], [
        "mcardle", "glikojen depo tip 5", "kas glikojen fosforilaz", "myofosforilaz", "egzersiz krampi",
        "ikinci ruzgar fenomeni", "second wind", "miyoglobinuri", "laktat artisi olmaz"
    ]),

    # 6. Amino Asit ve Üre Döngüsü Bozuklukları
    ("Fenilketonüri (PKU - Fenilalanin Hidroksilaz Eksikliği)", ["Tıbbi Genetik", "Pediatri", "Tıbbi Biyokimya"], [
        "fenilketonuri", "pku", "fenilalanin hidroksilaz", "pah", "tirozin eksikligi", "fare idrari kokusu",
        "kuf kokulu idrar", "acik ten sari sac mavi goz", "agir zeka geriligi", "guthrie testi", "bh4 tetrahidrobiyopterin"
    ]),
    ("Alkaptonüri (Homogentisat Oksidaz Eksikliği)", ["Tıbbi Genetik", "Tıbbi Biyokimya", "Romatoloji"], [
        "alkaptonuri", "homogentisat oksidaz", "homogentisik asit", "bekleyen idrarda kararma",
        "okronozis", "kulak kikirdaginda koyulasma", "buyuk eklem artriti", "spondiloartropati", "intervertebral disk kalsifikasyonu"
    ]),
    ("Akçaağaç Şurubu İdrar Hastalığı (MSUD - BCKDH Eksikliği)", ["Tıbbi Genetik", "Pediatri"], [
        "msud", "akcaagac surubu idrar", "maple syrup", "dalli zincirli amino asit", "bckdh", "losin izolosin valin",
        "yanik seker kokusu", "erken ensefalopati", "ketoasidoz"
    ]),
    ("Homosistinüri (Sistationin Beta-Sentaz Eksikliği)", ["Tıbbi Genetik", "Tıbbi Biyokimya", "Kardiyoloji"], [
        "homosistinuri", "sistationin beta sentaz", "homosistein yuksekligi", "metiyonin yuksekligi",
        "marfanoid habitus", "lens asagi ice lukse", "erken tromboz emboli", "b6 vitamini piridoksin"
    ]),
    ("Sistinüri (COLA Taşıyıcı Defekti)", ["Tıbbi Genetik", "Nefroloji", "Üroloji"], [
        "sistinuri", "cola tasiyici", "sistin ornitin lizin arjinin", "heksagonal kristaller", "idrarda sistin tasi", "sodyum siyanur nitroprussid testi"
    ]),
    ("Ornitin Transkarbamilaz Eksikliği (OTC - Üre Döngüsü Defekti)", ["Tıbbi Genetik", "Pediatri", "Tıbbi Biyokimya"], [
        "otc eksikligi", "ornitin transkarbamilaz", "ure dongusu", "x e bagli resesif", "hiperamonyemi",
        "orotik asiduri", "solunum alkalozu", "kan amonyak yuksekligi"
    ]),

    # 7. Fakomatozlar ve Tümör Baskılayıcı Sendromlar
    ("Nörofibromatozis Tip 1 (von Recklinghausen - NF1)", ["Tıbbi Genetik", "Dermatoloji", "Nöroloji"], [
        "norofibromatozis tip 1", "nf1", "norofibromin", "cafe au lait lekeleri", "sutlu kahve lekeleri",
        "lisch nodulleri iris hamartomu", "pleksiform norofibrom", "aksiller cillenme crowd belirtisi", "optik gliom", "feokromositoma"
    ]),
    ("Nörofibromatozis Tip 2 (Merlin - Bilateral Vestibüler Schwannom)", ["Tıbbi Genetik", "Nöroloji", "KBB"], [
        "norofibromatozis tip 2", "nf2", "merlin geni", "schwannomin", "bilateral vestibular schwannom",
        "akustik norinom", "menenjiom", "juvenil katarakt"
    ]),
    ("Tuberoskleroz (TSC1 Hamartin / TSC2 Tüberin)", ["Tıbbi Genetik", "Nöroloji", "Dermatoloji"], [
        "tuberoskleroz", "tsc1", "tsc2", "hamartin", "tuberin", "kortikal tuberler", "subependimal noduller",
        "sega subependimal dev hucreli astrositom", "ash leaf lekesi kul yapragi", "angiyofibrom adenoma sebaseum",
        "shagreen yamasi", "renal anjiyomiyolipom", "kardiyak rabdomyom"
    ]),
    ("von Hippel-Lindau Sendromu (VHL)", ["Tıbbi Genetik", "Onkoloji", "Nefroloji"], [
        "von hippel lindau", "vhl", "retinal hemanjiyoblastom", "serebellar hemanjiyoblastom",
        "berrak hucreli renal hucreli karsinom", "feokromositoma", "pankreatik kistler"
    ]),
    ("Li-Fraumeni Sendromu (TP53 Mutasyonu)", ["Tıbbi Genetik", "Tıbbi Onkoloji"], [
        "li fraumeni", "tp53", "p53 mutasyonu", "sarkom", "meme kanseri", "beyin tumoru", "adrenokortikal karsinom", "coklu primer kanserler"
    ]),
    ("Cowden Sendromu (PTEN Hamartoma Sendromu)", ["Tıbbi Genetik", "Dermatoloji", "Onkoloji"], [
        "cowden", "pten mutasyonu", "trikilemmom", "oral papillom", "tiroid folikuler ca", "meme ca", "endometrium ca"
    ]),
    ("Lynch Sendromu (HNPCC - Mismatch Repair Genleri)", ["Tıbbi Genetik", "Gastroenteroloji", "Genel Cerrahi"], [
        "lynch sendromu", "hnpcc", "mismatch repair", "mlh1", "msh2", "msh6", "pms2", "mikrosatellit instabilitesi",
        "sag kolon kanseri polipsiz", "endometrium kanseri", "over kanseri"
    ]),
    ("Peutz-Jeghers Sendromu (STK11 / LKB1 Mutasyonu)", ["Tıbbi Genetik", "Gastroenteroloji"], [
        "peutz jeghers", "stk11", "lkb1", "mukokutanoz hiperpigmentasyon", "dudakta melanin lekeleri",
        "hamartomatoz polipozis", "ince barsak polipleri", "intussusepsiyon", "meme over pankreas kanseri riski"
    ]),
    ("Ailesel Adenomatöz Polipozis (FAP - APC Geni)", ["Tıbbi Genetik", "Gastroenteroloji", "Genel Cerrahi"], [
        "fap", "ailesel adenomatoz polipozis", "apc geni", "yuzlerce binlerce kolon polipi",
        "yuzde yuz kolon kanseri riski", "profilaktik kolektomi", "gardner sendromu osteom", "turcot sendromu beyin tumoru"
    ]),
    ("Ataksi-Telenjiektazi (ATM Geni)", ["Tıbbi Genetik", "Nöroloji", "Tıbbi İmmünoloji"], [
        "ataksi telenjiektazi", "atm geni", "dna cift zincir kirik tamir defekti", "serebellar ataksi",
        "okulokutanoz telenjiektazi", "iga eksikligi", "alfa fetoprotein afp yuksekligi", "radyasyon duyarliligi", "lenfoma riski"
    ]),
    ("Kseroderma Pigmentozum (Nükleotid Eksizyon Tamir Defekti)", ["Tıbbi Genetik", "Dermatoloji"], [
        "kseroderma pigmentozum", "xp", "nukleotid eksizyon tamir", "uv duyarliligi", "pirimidin timin dimerleri",
        "asiri cillenme", "erken deri kanserleri melanom bcc scc"
    ]),
    ("Fanconi Anemisi (DNA Çapraz Bağ Tamir Defekti)", ["Tıbbi Genetik", "Hematoloji", "Pediatri"], [
        "fanconi anemisi", "dna capraz bag tamir", "diepoksibutan testi", "aplastik anemi pansitopeni",
        "basparmak hipoplazisi agenezisi", "kisa boy", "cafe au lait lekeleri", "aml riski"
    ]),
    ("Bloom Sendromu (BLM Geni - DNA Helikaz Defekti)", ["Tıbbi Genetik", "Pediatri"], [
        "bloom sendromu", "blm geni", "recq helikaz", "kardes kromatid degisimi artisi", "kelebek yuz eritemi", "kisa boy", "agir immunkompromize"
    ]),

    # 8. Diğer Önemli Dismorfoloji ve Genetik Sendromlar
    ("Noonan Sendromu (PTPN11 / RASopati)", ["Tıbbi Genetik", "Pediatri", "Kardiyoloji"], [
        "noonan", "ptpn11", "rasopati", "erkek turner", "pulmoner kapak darligi", "yele boyun", "hipertelorizm", "pektus karinatum"
    ]),
    ("Holt-Oram Sendromu (TBX5 - Kalp-El Sendromu)", ["Tıbbi Genetik", "Kardiyoloji", "Ortopedi ve Travmatoloji"], [
        "holt oram", "tbx5", "kalp el sendromu", "asd atriyal septal defekt", "basparmak anomalileri triphalangeal"
    ]),
    ("Treacher Collins Sendromu (TCOF1 - Mandibulofasiyal Disostoz)", ["Tıbbi Genetik", "KBB", "Plastik ve Rekonstrüktif Cerrahi"], [
        "treacher collins", "tcof1", "mandibulofasiyal disostoz", "elmacik kemigi hipoplazisi", "alt goz kapagi kolobomu", "mikrotia iletim tipi sagirlik"
    ]),
    ("Pierre Robin Sekansı (Mikrognati & Glossopitozis)", ["Tıbbi Genetik", "Pediatri", "KBB"], [
        "pierre robin", "mikrognati", "glossopitozis", "u tipi yarik damak", "hava yolu obstruksiyonu solunum sikintisi"
    ]),
    ("Alport Sendromu (COL4A5 - Tip 4 Kollajen)", ["Tıbbi Genetik", "Nefroloji", "Göz Hastalıkları"], [
        "alport sendromu", "col4a5", "tip 4 kollajen", "x e bagli", "glomerul bazal membran sepet orgusu basket weave",
        "hematuri bobrek yetmezligi", "sensorinorol isitme kaybi", "anterior lentikonus"
    ]),
    ("Kallmann Sendromu (KAL1 - Anosmi & Hipogonadizm)", ["Tıbbi Genetik", "Endokrinoloji"], [
        "kallmann", "kal1", "gnrh noron goc defekti", "koku alma kaybi anosmi", "hipogonadotropik hipogonadizm", "gecikmis ergenlik"
    ]),
    ("Kartagener Sendromu (Primer Siliyer Diskinezi - Dinein Kolu Defekti)", ["Tıbbi Genetik", "Göğüs Hastalıkları"], [
        "kartagener", "primer siliyer diskinezi", "dinein kolu defekti", "situs inversus totalis", "kronik sinuzit", "bronsektazi", "infertilite"
    ]),
    ("Wiskott-Aldrich Sendromu (WASp - Triad)", ["Tıbbi Genetik", "Pediatri", "Tıbbi İmmünoloji"], [
        "wiskott aldrich", "wasp geni", "x e bagli", "trombositopeni mikrotrombositler", "egzama atopik dermatit", "tekrarlayan kapsullu pirojen enfeksiyonlar"
    ]),
    ("Ataksi Telenjiektazi Sendromu", ["Tıbbi Genetik", "Nöroloji"], [
        "ataksi telenjiektazi", "atm geni", "serebellar ataksi", "telenjiektazi", "iga eksikligi", "afp yuksekligi"
    ]),
    ("Chédiak-Higashi Sendromu (LYST Geni)", ["Tıbbi Genetik", "Hematoloji", "Pediatri"], [
        "chediak higashi", "lyst geni", "mikrotubul lizozomal fuzon defekti", "dev notrofil nozon granulleri", "parsiyel albinizm", "periferik noropati"
    ]),
    ("Kronik Granülomatöz Hastalık (CGD - NADPH Oksidaz)", ["Tıbbi Genetik", "Tıbbi Mikrobiyoloji", "Pediatri"], [
        "kronik granulomatoz hastalik", "cgd", "nadph oksidaz eksikligi", "superoksit uretememe", "katalaz pozitif mikroorganizmalar", "sfa nbt negatifligi"
    ]),
    ("Lökosit Adezyon Defekti Tip 1 (LAD-1 - CD18 / Beta-2 İntegrin)", ["Tıbbi Genetik", "Pediatri", "Tıbbi İmmünoloji"], [
        "lokosit adezyon defekti", "lad 1", "cd18 eksikligi", "beta 2 integrin", "gobek baginin gec dusmesi", "cerahat irin olusmamasi", "lokositoz"
    ]),
    ("Ağır Kombine İmmün Yetmezlik (SCID - ADA / IL2RG)", ["Tıbbi Genetik", "Tıbbi İmmünoloji", "Pediatri"], [
        "scid", "agir kombine immun yetmezlik", "adenozin deaminaz ada eksikligi", "il2rg x e bagli", "t ve b hucre yoklugu", "pamukcuk kronik diyare"
    ]),
    ("Bruton Agamaglobulinemisi (XLA - BTK Tirozin Kinaz)", ["Tıbbi Genetik", "Tıbbi İmmünoloji", "Pediatri"], [
        "bruton", "xla", "btk tirozin kinaz", "pre b den matür b hucresine gecememe", "tum immunoglobulinler yok", "lenf nodu ve tonsil yoklugu"
    ])
]
