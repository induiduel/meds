# -*- coding: utf-8 -*-
"""
Clinical Medicine Master Concepts Database
(Cardiology, Pulmonology, GI, Nephrology, Endocrine, Heme, Rheum, Neuro, Peds, OB/GYN, Surgery)
"""

CLINICAL_CONCEPTS = [
    # 1. Kardiyoloji ve Damar Hastalıkları
    ("Akut Koroner Sendrom & Troponin Kinetiği", ["Kardiyoloji", "Acil Tıp", "Tıbbi Patoloji"], [
        "akut koroner sendrom", "aks", "stemi", "nstemi", "kararsiz angina unstabil",
        "kardiyak troponin i ve t", "ck mb reinfarktus tanisi", "st elevasyonu ve t dalgasi inversiyonu",
        "morfin oksijen nitrat aspirin mona", "primer perkutan koroner girisim pci kapi balon zamani 90 dk"
    ]),
    ("Fallot Tetralojisi (TOF) & Siyanotik Nöbetler", ["Kardiyoloji", "Pediatri", "Kalp ve Damar Cerrahisi"], [
        "fallot tetralojisi", "tof", "en sik siyanotik konjenital kalp hastaligi", "dortlu bilesen",
        "vsd ventrikuler septal defekt", "pulmoner infundibuler stenoz darlik", "ata binen aort dekstropozisyon", "sag ventrikul hipertrofisi",
        "telede tahta pabuc gorunumu coeur en sabot", "tet nobeti hipoksik nobet comelme pozisyonu sivr"
    ]),
    ("Ventriküler Septal Defekt (VSD)", ["Kardiyoloji", "Pediatri"], [
        "vsd", "ventrikuler septal defekt", "en sik konjenital kalp anomalisi", "sol alt sternal kenarda pansistolik ufurum holosistolik",
        "membranoz vsd musküler vsd", "eisenmenger sendromu sag sol santi pulmoner hipertansiyon siyanotik donusum"
    ]),
    ("Patent Duktus Arteriyozus (PDA) & İndometazin", ["Kardiyoloji", "Pediatri"], [
        "pda", "patent duktus arteriyozus", "sol subklavyan altinda devamli makine ufurumu gibson ufurumu",
        "prematurite konjenital rubella kizamikcik", "prostaglandin e2 kanali acik tutar", "kapatmak icin indometazin ibuprofen", "acik tutmak icin alprostadil pge1"
    ]),
    ("Aort Koarktasyonu & Diferansiyel Tansiyon", ["Kardiyoloji", "Pediatri", "Kalp ve Damar Cerrahisi"], [
        "aort koarktasyonu", "turner sendromu birlikteligi", "bikuspid aort kapagi", "ust ekstremitede hipertansiyon alt ekstremitede hipotansiyon zayif nabiz",
        "radyolojide 3 belirtisi", "kaburga altinda centiklenme rib notching interkostal arter genislemesi", "femoral nabiz gecikmesi pulsus parvus et tardus bacakta"
    ]),
    ("Aort Stenozu (Darlığı) & Senkop/Angina/Nefes Darlığı Triadı", ["Kardiyoloji", "Kalp ve Damar Cerrahisi"], [
        "aort stanozu", "aort darligi", "yasli dejeneratif kalsifik bikuspid aort zemininde", "klasik triad sad senkop angina dispne",
        "sag 2 interkostal aralikta kreşendo dekreşendo sistolik ejeksiyon ufurumu boyna yayilim", "pulsus parvus et tardus zayif ve gec vuran karotis nabzi", "s2 sertlesmesi paradoksal ciftlesme"
    ]),
    ("Aort Yetersizliği & Geniş Nabız Basıncı Belirtileri", ["Kardiyoloji", "Kalp ve Damar Cerrahisi"], [
        "aort yetersizligi", "aort regurjitasyonu", "sol 3 interkostal erken diyastolik ufurum decrescendo", "austin flint middiyastolik rulman",
        "genis nabiz basinci artmis sistolik dusuk diyastolik", "corrigan nabzi sicrayici su cekici nabiz", "de musset bas sallama nabizla", "muller uvula pulsasyonu", "quincke tirnak yatagi pulsasyonu"
    ]),
    ("Mitral Darlık & Romatizmal Kalp Hastalığı", ["Kardiyoloji"], [
        "mitral stenoz", "mitral darligi", "en sik neden akut romatizmal kardit ara", "apeksde acilma sesi opening snap ve middiyastolik rulman",
        "sol atriyum dilatasyonu basisi ses kisikligi ortner sendromu sol laringeal rekurren sinir", "disfaji ozofagus basisi", "atriyal fibrilasyon ve sistemik emboli riski mitral fasies"
    ]),
    ("Mitral Yetmezlik & Papiller Kas Rüptürü", ["Kardiyoloji"], [
        "mitral yetersizligi", "mitral regurjitasyonu", "apekste koltuga yayilan holosistolik pansistolik ufurum", "akut mi sonrasi papiller kas disfonksiyonu ve rüptürü inferior mi rca",
        "akut pulmoner odem ve kardiyojenik sok"
    ]),
    ("Mitral Kapak Prolapsusu (MVP / Barlow Sendromu)", ["Kardiyoloji"], [
        "mitral kapak prolapsusu", "mvp", "barlow sendromu", "miksomatoz dejenerasyon dermatan sulfat birikimi marfan ehlers danlos",
        "mezosistolik klik ve gec sistolik ufurum", "valsalva ve ayaga kalkma ile ufurum erkene kayar ve artar", "comelme ile ufurum gecikir ve azalir"
    ]),
    ("Kardiyak Tamponad & Beck Triadı", ["Kardiyoloji", "Acil Tıp"], [
        "kardiyak tamponad", "beck triadi", "hipotansiyon dusuk tansiyon", "juguler venoz dolgunluk", "derinden gelen boguk kalp sesleri",
        "pulsus paradoksus inspiryumda sistolik kan basincinin 10 mmhg den fazla dusmesi", "ekg de elektriksel alternans ve dusuk voltaj", "acil perikardiyosentez"
    ]),
    ("Konstriktif Perikardit & Kussmaul Belirtisi", ["Kardiyoloji"], [
        "konstriktif perikardit", "perikardiyal kalsifikasyon zirh kalp", "diyastolik dolus kisitlanmasi", "kussmaul belirtisi inspiryumda juguler dolgunluk paradoksal artis",
        "perikardiyal vuru pericardial knock erken diyastolik ses", "tüberküloz veya cerrahi sonrasi"
    ]),
    ("Hipertrofik Obstrüktif Kardiyomiyopati (HOCM / IHSS)", ["Kardiyoloji", "Tıbbi Genetik"], [
        "hocm", "hipertrofik kardiyomiyopati", "asimetrik septal hipertrofi ash", "sam sistolik anterior hareket mitral on yaprak",
        "genc sporcuda ani kardiyak olum", "sarkomerik mutasyonlar beta miyozin agir zincir myh7 miyosin baglayici protein c mybpc3",
        "valsalva ile ufurum artar comelme ile azalir beta bloker ilk tercih digoksin kontrendike"
    ]),
    ("Wolff-Parkinson-White (WPW Sendromu)", ["Kardiyoloji"], [
        "wpw", "wolff parkinson white", "aksesuar iletim yolu kent demeti", "kisa pr mesafesi 120 ms alti",
        "delta dalgasi genis qrs", "paroksismal supraventrikuler tasikardi svt psrvt", "atriyal fibrilasyonda ablasyon tedavisi", "av dugum blokerleri digoksin verapamil kontrendike af durumunda vf tetikler"
    ]),
    ("Aort Diseksiyonu (Stanford Tip A ve B)", ["Kalp ve Damar Cerrahisi", "Kardiyoloji", "Acil Tıp"], [
        "aort diseksiyonu", "yirtici bica saplanir tarzda gogus ve sirt agrisi kurek kemikleri arasi", "asimetrik kol tansiyon farki nabiz kaybi",
        "aort kok tutulumu aort yetersizligi tamponad ve koroner enfarktus", "stanford tip a cikan aort cerrahi acil", "stanford tip b inen aort medikal tansiyon kontrolu beta bloker esmolol labetalol"
    ]),

    # 2. Göğüs Hastalıkları
    ("Kronik Obstrüktif Akciğer Hastalığı (KOAH) & Amfizem", ["Göğüs Hastalıkları", "Tıbbi Patoloji"], [
        "koah", "kronik obstruktif akciger hastaligi", "fev1 fvc orani 0 70 alti geri donussuz obstrüksiyon", "sigara temel neden",
        "sentriasiner amfizem ust loblar sigara", "panasiner amfizem alt loblar alfa 1 antitripsin eksikligi a1at",
        "mavi pofurdayan blue bloater kronik bronsit kor pulmonale", "pembe pufleyen pink puffer amfizem kilo kaybi ficigogus", "reid indeksi 0 40 ustu bronsit"
    ]),
    ("Bronşiyal Astım & Patolojisi", ["Göğüs Hastalıkları", "Tıbbi Patoloji", "Farmakoloji"], [
        "astim", "bronkodilator ile reversibl hava akimi kisitlanmasi fev1 yuzde 12 ve 200 ml artis", "tip 1 asiri duyarlilik ige mast hucresi th2 il4 il5 il13 eozinofil",
        "curschmann spiralleri mukus tikaclari", "charcot leyden kristalleri eozinofil lizofosfolipaz", "bronkospazm gece oksuruk hisilti wheezing nefes darligi", "inhaler kortikosteroid saba laba"
    ]),
    ("Sarkoidoz & Non-Kazeifiye Granülom", ["Göğüs Hastalıkları", "Tıbbi Patoloji", "Romatoloji"], [
        "sarkoidoz", "non kazeifiye granulom peynirlesme yok", "bilateral hiler lenfadenopati bhla", "akciger parankim tutulumu interstisiyel",
        "serum ace anjiyotensin donusturucu enzim yuksekligi", "1 alfa hidroksilaz aktivasyonu hiperkalsemi ve hiperkalsiuri",
        "lofgren sendromu eritema nodozum bilateral hiler lap artralji ates iyi huylu", "heerfordt sendromu uveoparotid ates fasial felc uveit parotit"
    ]),
    ("İdiyopatik Pulmoner Fibrozis (İPF / UIP)", ["Göğüs Hastalıkları", "Tıbbi Patoloji"], [
        "ipf", "idiyopatik pulmoner fibrozis", "uip mutad interstisiyel pnomoni", "bal petegi gorunumu honeycomb akciger bt de",
        "fibroblastik odaklar zamansal ve mekansal heterojenite", "subplevral ve bazal baskin fibrozis", "inspiratuar krepitan velkro raller comak parmak", "pirfenidon nintedanib antifibrotik"
    ]),
    ("Pulmoner Tromboemboli & Wells Kriterleri", ["Göğüs Hastalıkları", "Kardiyoloji", "Acil Tıp"], [
        "pulmoner tromboemboli", "pte", "derin ven trombozu dvt kokenli pelvik bacak venleri", "ani baslayan batar tarzda yan agrisi nefes darligi dispne tasikardi hemoptizi",
        "wells skoru d dimer negatif ise disla", "bt pulmoner anjiyografi altin standart", "ekg s1q3t3 paterni sag ventrikul yuklenmesi", "radyoloji hampton horgucu westermark oligemi", "heparin trombolitik tpa"
    ]),
    ("Pnömokonyozlar (Silikozis, Asbestozis, Kömür İşçisi)", ["Göğüs Hastalıkları", "Tıbbi Patoloji"], [
        "silikozis", "kum puskurtme madencilik tas ocagi", "ust loblarda silikotik noduller", "yumurta kabugu kalsifikasyonu lenf bezlerinde", "tuberkuloz riskini katlar",
        "asbestozis", "gemi sokum yalitim fren balatasi", "alt lob fibrozisi plevral plaklar", "ferruginoz cisimcikler halter lifler", "malign mezotelyoma ve akciger ca riski",
        "komur iscisi pnomokonyozu", "komur makulleri progresif masif fibrozis antrakoz"
    ]),

    # 3. Gastroenteroloji ve Hepatoloji
    ("Gastroözofageal Reflü (GÖRH) & Barrett Özofagusu", ["Gastroenteroloji", "Tıbbi Patoloji"], [
        "gorh", "gastroozofageal reflu", "retrosternal yanma pirozis regurjitasyon", "alt ozofagus sfinkter gevsekligi hiatal herni",
        "barrett ozofagus", "cok katli yassi epitelin goblet hucreli kolumnar intestinal metaplaziye donusumu", "ozofagus adenokarsinomu prekursoru displazi taramasi"
    ]),
    ("Akalazya & Kuş Gagası Görünümü", ["Gastroenteroloji", "Genel Cerrahi"], [
        "akalazya", "auerbach miyenterik pleksus ganglion hucre kaybi no vip azalmasi", "alt ozofagus sfinkterinin relakse olamamasi aperistaltizm",
        "hem sivilara hem katilara karsi disfaji", "baryumlu grafide kus gagasi manzarasi bird beak", "yüksek cozunurluklu manometri altin standart", "chagas tripanosoma benzer tablo"
    ]),
    ("Çölyak Hastalığı (Gluten Enteropatisi)", ["Gastroenteroloji", "Pediatri", "Tıbbi Patoloji"], [
        "colyak", "gluten enteropatisi", "bugday arpa cavdar gliadin proteini", "hla dq2 hla dq8 doku grubu",
        "anti ttg iga doku transglutaminaz", "anti endomizyum ema iga", "duodenum biyopsisinde villus atrofisi kript hiperplazisi intraepitelyal lenfositoz iel marsh evreleme",
        "kronik malabsorbsiyon demir eksikligi anemisi steatore kalsiyum eksikligi osteoporoz", "dermatitis herpetiformis büllöz kasiyici dokuntu dirsek diz"
    ]),
    ("İnflamatuar Bağırsak: Crohn vs Ülseratif Kolit", ["Gastroenteroloji", "Tıbbi Patoloji", "Genel Cerrahi"], [
        "crohn hastaligi", "agizdan anuse tum gis transmural tutulum derin lineer ulserler kaldirim tasi manzarasi",
        "atlamali lezyonlar skip lesions non kazeifiye granulomlar fistul ve striktur darlik", "terminal ileum en sik b12 emilim bozuklugu", "asca pozitif",
        "ulseratif kolit", "yalnizca kolon tutulumu rektumdan baslar proksimale kesintisiz ilerler", "mukozal submukozal tutulum kript abseleri kriptit psodopolipler toksik megakolon",
        "p anca pozitif psc primer sklerozan kolanjit birlikteligi kolon ca riski yuksek"
    ]),
    ("Primer Biliyer Kolanjit (PBC) & AMA", ["Gastroenteroloji", "Tıbbi Patoloji"], [
        "primer biliyer kolanjit", "pbc", "orta yasli kadinlarda kronik kasinti ve yorgunluk kolestatik sarilik",
        "anti mitokondriyal antikor ama pozitifligi yuzde 95", "alkalen fosfataz alp ve ggt belirgin yuksekligi igm artisi",
        "karaciger biyopsisinde florid dukt lezyonu interlobuler safra kanali granülomatoz harabiyeti", "ursodeoksikolik asit udca tedavisi"
    ]),
    ("Primer Sklerozan Kolanjit (PSC) & p-ANCA", ["Gastroenteroloji", "Tıbbi Patoloji"], [
        "primer sklerozan kolanjit", "psc", "ulseratif kolitli genc erkeklerde", "ercp mrcp de tesbih tanesi boncuklanma safra kanallarinda striktur ve dilatasyon",
        "karaciger biyopsisinde konsantrik sogan zari periduktal fibrozis", "kolanjiokarsinom gelisme riski yuksek", "p anca pozitifligi"
    ]),
    ("Wilson Hastalığı (Hepatolentiküler Dejenerasyon)", ["Gastroenteroloji", "Nöroloji", "Tıbbi Genetik"], [
        "wilson hastaligi", "hepatolentikuler dejenerasyon", "atp7b gen mutasyonu otozomal resesif bakir atilim defekti",
        "seruloplazmin duzeyinde belirgin dusukluk 24 saatlik idrar bakirinda yukseklik", "korneada kayser fleischer kf halkasi yarık lamba muayenesi descemet zari",
        "karacigerde siroz akut hepatit bazal ganglionlarda birikim tremor distoni kore rijidite parkinsonizm psikiyatrik bozukluklar", "d penisilamin trientin cinko"
    ]),
    ("Herediter Hemokromatozis (Bronz Diyabet)", ["Gastroenteroloji", "Hematoloji", "Endokrinoloji"], [
        "herediter hemokromatozis", "hfe geni c282y ve h63d mutasyonlari otozomal resesif", "hepsidin sentez yetersizligi kontrolsuz demir emilimi",
        "ferritin ve transferrin saturasyonu belirgin yuksek yuzde 45 50 ustu", "klasik triad karaciger sirozu mikronoduler hiperpigmentasyon bronz deri bronz diyabet pankreas hasari",
        "kardiyomiyopati psodogut artropati kondrokalsinozis hipogonadizm", "flebotomi kan alma ve deferoksamin"
    ]),

    # 4. Nefroloji
    ("Minimal Lezyon Hastalığı (Lipoid Nefroz)", ["Nefroloji", "Pediatri", "Tıbbi Patoloji"], [
        "minimal lezyon hastaligi", "lipoid nefroz", "cocuklarda en sik nefrotik sendrom nedeni", "masif proteinuri hipoalbuminemi anazarka odem",
        "isik mikroskopisi ve immunfloresan tamamen normaldir", "elektron mikroskopisinde podosit ayaksi cikintilarinda silinme effacement",
        "selektif proteinuri sadece albumin kacar", "steroide yanit mukemmeldir prednisone tam kur"
    ]),
    ("Fokal Segmental Glomerüloskleroz (FSGS)", ["Nefroloji", "Tıbbi Patoloji"], [
        "fsgs", "fokal segmental glomeruloskleroz", "eriskinde en sik nefrotik sendrom nedeni siyahi irkta sik",
        "hiv iliskili nefropati eroin orak hucre obezite tek bobrek hiperfiltrasyon", "segmental skleroz ve hyalinozis",
        "non selektif proteinuri steroide yanitsizdir bobrek yetmezligine ilerler transplant sonrasi nuks yuksek"
    ]),
    ("Membranöz Nefropati & PLA2R", ["Nefroloji", "Tıbbi Patoloji"], [
        "membranoz nefropati", "anti pla2r fosfolipaz a2 reseptor antikoru primer form",
        "sekonder form malignite solid tumorler nsaid sle hepatit b", "glomerul bazal membraninda diffuz kalinlasma",
        "gumus boyada civi kubbe spike and dome gorunumu", "subepitelyal igg ve c3 granuler birikimi", "renal ven trombozu riski en yuksek nefrotik tablodur"
    ]),
    ("Akut Poststreptokoksik Glomerülonefrit (APSGN)", ["Nefroloji", "Pediatri", "Tıbbi Patoloji"], [
        "apsgn", "akut poststreptokoksik glomerulonefrit", "agbhs farenjit veya impetigo deri enfeksiyonu sonrasi 1 4 hafta latent donem",
        "nefritik sendrom hematuri kola rengi cay rengi idrar oliguri odem hipertansiyon", "serum c3 kompleman belirgin duser 6 8 haftada duzelir aso titresinde artis",
        "elektron mikroskopisinde subepitelyal horguc subepithelial humps birikintileri", "yildizli gokyuzu starry sky granuler immunfloresan"
    ]),
    ("IgA Nefropatisi (Berger Hastalığı)", ["Nefroloji", "Tıbbi Patoloji"], [
        "iga nefropatisi", "berger hastaligi", "dunyada en sik gorulen primer glomerulonefrit", "ust solunum yolu veya gis enfeksiyonu ile es zamanli epizodik makroskopik hematuri synpharyngitic",
        "serum c3 normaldir", "mezanjiyal iga ve c3 granuler birikimi mezanjiyal proliferasyon", "henoch schonlein purpurasi vaskulitinin bobrekle sinirli formu"
    ]),
    ("Goodpasture Sendromu (Anti-GBM Hastalığı)", ["Nefroloji", "Göğüs Hastalıkları", "Tıbbi Patoloji"], [
        "goodpasture sendromu", "anti gbm hastaligi", "tip 4 kollajen alfa 3 zincirine karsi otoantikor",
        "pulmoner renal sendrom alveolar hemoraji hemoptizi ve hizli ilerleyen glomerulonefrit rpgn nefritik",
        "immunfloresanda duzgun cizgisel lineer igg birikimi glomerul bazal membran boyunca", "kresentik glomerulonefrit bowman araliginda hilaller", "acil plazmaferez ve steroid siklofosfamid"
    ])
]
