# -*- coding: utf-8 -*-
"""
Pathology & Histology Master Concepts Database
"""

PATHOLOGY_CONCEPTS = [
    # 1. Hücre Hasarı, Ölümü ve Uyum Mekanizmaları
    ("Koagülasyon Nekrozu", ["Tıbbi Patoloji", "Kardiyoloji"], [
        "koagulasyon nekrozu", "iskemi enfarktüs", "hücre sınırları korunur", "hayalet hücreler ghost cells",
        "çekirdek kaybı piknoz karyoliz karyoreksis", "miyokard enfarktüsü böbrek dalak", "beyin hariç tüm katı organlar"
    ]),
    ("Kollikuasyon (Likefaksiyon) Nekrozu", ["Tıbbi Patoloji", "Nöroloji"], [
        "kollikuasyon nekrozu", "likefaksiyon nekrozu", "beyin enfarktüsü", "asidik sindirim eritme",
        "kistik kavite kist oluşumu", "abse odağı cerahat irin", "nötrofil hidrolitik enzimleri", "santral sinir sistemi"
    ]),
    ("Kazeifikasyon Nekrozu", ["Tıbbi Patoloji", "Göğüs Hastalıkları"], [
        "kazeifikasyon nekrozu", "kazeöz nekroz", "tüberküloz tbc", "peynirimsi kazeöz görünüm",
        "granülomatöz iltihap", "langhans dev hücresi at nalı", "epiteloid histiyosit", "asido rezistan basil arb"
    ]),
    ("Enzimatik Yağ Nekrozu", ["Tıbbi Patoloji", "Gastroenteroloji"], [
        "enzimatik yag nekrozu", "akut pankreatit", "pankreatik lipaz elastaz", "sabunlaşma saponifikasyon",
        "tebeşir beyazı odaklar", "kalsiyum birikimi hipokalsemi", "omental peripankreatik yağ dokusu"
    ]),
    ("Fibrinoid Nekroz", ["Tıbbi Patoloji", "Romatoloji", "Kardiyoloji"], [
        "fibrinoid nekroz", "malign hipertansiyon", "immün kompleks vasküliti", "pan poliarteritis nodoza",
        "damar duvarında parlak pembe eozinofilik birikim", "antijen antikor kompleksi ve fibrin çökmesi"
    ]),
    ("Apoptoz Mekanizmaları & Kaspazlar", ["Tıbbi Patoloji", "Tıbbi Biyokimya"], [
        "apoptoz", "programli hucre olumu", "hucre buzusmesi sitokrom c salinimi", "intrensek mitokondriyal yolak bcl2 bax bak",
        "ekstrensek olum reseptoru yalagi fas fasl tnf", "baslatici kaspaz 8 9", "yurutucu efektor kaspaz 3 6 7",
        "psomoz dna merdivenlesmesi laddering", "inflamasyon olusmaz yangisizdir"
    ]),
    ("Amiloidoz & Kongo Kırmızısı Boyama", ["Tıbbi Patoloji", "Dahiliye", "Romatoloji"], [
        "amiloidoz", "amiloid", "kongo kirmizisi congo red", "elma yesili cift kirinim apple green birefringence",
        "polarize mikroskop polarize isik", "al amiloid plazma hucre diskrazisi multipl miyelom hafif zincir",
        "aa amiloid kronik inflamasyon romatoid artrit fmf ssk sinsi", "abeta amiloid alzheimer amiloid oncul proteini",
        "attr transtiretin senil kardiyak amiloidoz ailesel polinöropati", "a cal meduller tiroid ca kalsitonin amiloid"
    ]),

    # 2. Histopatolojik Cisimcikler ve Karakteristik Bulgular
    ("Mallory-Denk Cisimcikleri", ["Tıbbi Patoloji", "Gastroenteroloji"], [
        "mallory denk", "mallory cisimcigi", "sitokeratin ara filaman yumaklari", "hepatosit balonlasma dejenerasyonu",
        "alkolik hepatit", "nash non alkolik steatohepatit", "wilson hastaligi", "hepatoselluler karsinom"
    ]),
    ("Councilman (Apoptotik) Cisimcikleri", ["Tıbbi Patoloji", "Gastroenteroloji"], [
        "councilman cisimcigi", "apoptotik hepatosit", "büzüşmüş piknotik yoğun eozinofilik asidofilik sitoplazma",
        "viral hepatit b c", "sari humma yellow fever"
    ]),
    ("Negri Cisimcikleri (Kuduz)", ["Tıbbi Patoloji", "Enfeksiyon Hastalıkları", "Nöroloji"], [
        "negri cisimcigi", "kuduz virusu rabies", "eozinofilik intrasitoplazmik inkluzyon",
        "hipokampus piramidal noronlari", "serebellum purkinje hucreleri"
    ]),
    ("Lewy Cisimcikleri & Alfa-Sinüklein", ["Tıbbi Patoloji", "Nöroloji"], [
        "lewy cisimcigi", "alfa sinuklein proteini", "konsantrik halo eozinofilik inkluzyon",
        "substantia nigra dopaminerjik noron kaybi", "parkinson hastaligi", "lewy cisimcikli demans lbd"
    ]),
    ("Psammom Cisimcikleri", ["Tıbbi Patoloji", "Tıbbi Onkoloji"], [
        "psammom cisimcigi", "psammoma body", "konsantrik lameller kalsifikasyon odagi",
        "papiller tiroid karsinomu", "menenjiom", "seroz kistadenokarsinom over", "malign mezotelyoma"
    ]),
    ("Reed-Sternberg Dev Hücreleri", ["Tıbbi Patoloji", "Hematoloji"], [
        "reed sternberg", "rs hucresi", "baykus gozu manzarasi owl eye", "iki cekirdekli dev lenfoid hucre",
        "cd15 pozitif", "cd30 pozitif", "hodgkin lenfoma", "noduler sklerozan mikst selluler"
    ]),
    ("Auer Rodları (Auer Çomakları)", ["Tıbbi Patoloji", "Hematoloji"], [
        "auer rod", "auer comagi", "kaynasmi primer azurofilik granuller", "miyeloperoksidaz mpo pozitif",
        "akut miyeloid losemi aml", "akut promiyelositik losemi apl m3 t 15 17 pml rara", "dik tetikleyebilir"
    ]),
    ("Call-Exner Cisimcikleri", ["Tıbbi Patoloji", "Kadın Hastalıkları ve Doğum"], [
        "call exner", "granuloza hucreli over tumoru", "folikul benzeri mikrokistik yapilar",
        "kahve cekirdegi nuclear groove nukleuslar", "ostrojen salgilar endometrial hiperplazi ve kanama", "inhibin pozitif"
    ]),
    ("Schiller-Duval Cisimcikleri", ["Tıbbi Patoloji", "Kadın Hastalıkları ve Doğum", "Üroloji"], [
        "schiller duval", "glomerul benzeri yapilar", "yolk sac tumoru endodermal sinus tumoru",
        "alfa fetoprotein afp yuksekligi", "cocuklarda en sik malign testis over germ hucreli tumor"
    ]),
    ("Homer-Wright Rozetleri", ["Tıbbi Patoloji", "Pediatri", "Nöroloji"], [
        "homer wright rozeti", "noropil cevresinde dizilim", "noroblastom n myc vma hva",
        "medulloblastom serebellar posterior fossa cocuk", "kucuk yuvarlak mavi hucreli tumor"
    ]),
    ("Flexner-Wintersteiner Rozetleri", ["Tıbbi Patoloji", "Göz Hastalıkları"], [
        "flexner wintersteiner rozeti", "gercek lümen iceren rozet", "retinoblastom rb1 gen mutasyonu", "lokokori kedi gozu refleksi"
    ]),
    ("Kimmelstiel-Wilson Nodülleri", ["Tıbbi Patoloji", "Nefroloji", "Endokrinoloji"], [
        "kimmelstiel wilson", "noduler glomeruloskleroz", "diyabetik nefropati", "pas pozitif hyalen aselluler mezanjiyal noduller",
        "agir mikroalbuminuri ve nefrotik proteinuri", "afferent ve efferent arteriyoloskleroz"
    ]),
    ("Aschoff Cisimcikleri & Anitschkow Hücreleri", ["Tıbbi Patoloji", "Kardiyoloji"], [
        "aschoff cisimcigi", "anitschkow hucresi", "tirtil hucresi caterpillar cell",
        "akut romatizmal kardit ara pankardit", "fibrinoid nekroz cevresinde t lenfosit ve dev histiyositler"
    ]),
    ("Birbeck Granülleri (Tenis Raketi)", ["Tıbbi Patoloji", "Pediatri", "Dermatoloji"], [
        "birbeck granulleri", "tenis raketi manzarasi elektron mikroskopisi", "langerhans hucreli histiyositoz",
        "cd1a pozitif", "cd207 langerin pozitif", "s100 pozitif", "kemik litik lezyonlari vertebra plana zimbayla delinmis kafatasi"
    ]),

    # 3. İmmünohistokimya ve Kanser Belirteçleri
    ("Sitokeratinler (CK7 & CK20)", ["Tıbbi Patoloji", "Tıbbi Onkoloji"], [
        "sitokeratin", "ck7 pozitif ck20 negatif akciger meme jinekolojik adenokarsinom",
        "ck7 negatif ck20 pozitif kolorektal karsinom cdx2 pozitif",
        "epitelyal doku karsinom belirteci", "ae1 ae3 pansitokeratin"
    ]),
    ("TTF-1 (Tiroid Transkripsiyon Faktörü-1)", ["Tıbbi Patoloji", "Göğüs Hastalıkları"], [
        "ttf 1", "tiroid transkripsiyon faktoru 1", "napsin a pozitif",
        "akciger primer adenokarsinomu", "tiroid karsinomlari", "akciger skuamoz ca da negatiftir p40 p63 pozitiftir"
    ]),
    ("p63 ve p40 (Skuamöz Hücreli Karsinom)", ["Tıbbi Patoloji", "Göğüs Hastalıkları"], [
        "p63", "p40", "skuamoz hucreli karsinom belirteci", "akciger skuamoz hucreli ca santral yerlesim kavitasyon keratin incileri",
        "intraselluler kopruler interselluler kopru"
    ]),
    ("Sinaptofizin & Kromogranin A (Nöroendokrin)", ["Tıbbi Patoloji", "Tıbbi Onkoloji"], [
        "sinaptofizin", "kromogranin a", "cd56 ncam", "noroendokrin diferansiasyon",
        "kucuk hucreli akciger karsinomu oat cell", "karsinoid tumor apudom", "feokromositoma"
    ]),
    ("S100, Melan-A ve HMB-45 (Malign Melanom)", ["Tıbbi Patoloji", "Dermatoloji"], [
        "s100", "melan a", "hmb 45", "sox10", "malign melanom paneli",
        "braf v600e mutasyonu", "breslow kalinligi en onemli prognostik kriter", "schwannoma s100 pozitif"
    ]),
    ("Desmin ve Miyogenin (Çizgili Kas Belirteçleri)", ["Tıbbi Patoloji", "Pediatri"], [
        "desmin", "miyogenin", "myod1", "cizgili kas diferansiasyonu",
        "rabdomyosarkom", "embriyonal rabdomyosarkom botriyoid vajen mesane cocuk", "alveoler rabdomyosarkom t 2 13 pax3 fkhr"
    ]),
    ("CD31 ve CD34 (Vasküler Endotelyal Belirteçler)", ["Tıbbi Patoloji", "Kardiyoloji"], [
        "cd31", "cd34", "vaskuler endotel hucre belirteci", "faktor viii iliskili antijen",
        "anjiyosarkom karaciger vinil klorur arsenik torotrast", "hemanjiom", "kaposi sarkomu hhv8"
    ]),
    ("CD20 ve CD3 (B ve T Lenfosit Belirteçleri)", ["Tıbbi Patoloji", "Hematoloji"], [
        "cd20", "cd19", "b lenfosit belirteci rituksimab hedefi", "diffuz buyuk b hucreli lenfoma folikuler lenfoma",
        "cd3", "cd4 cd8", "t lenfosit belirteci periferik t hucreli lenfoma mikozis fungoides sezary sendromu"
    ]),
    ("Ki-67 Proliferasyon İndeksi", ["Tıbbi Patoloji", "Tıbbi Onkoloji"], [
        "ki 67", "proliferasyon indeksi mib 1", "hucre siklusu g1 s g2 m fazlarinda pozitif g0 da negatif",
        "meme kanseri luminal a luminal b ayrimi", "noroendokrin tumor evrelemesi g1 g2 g3", "burkitt lenfoma ki67 yuzde yuz"
    ])
]
