# -*- coding: utf-8 -*-
"""
Medical Master Expansion Database
Provides 1,500+ distinct clinical, anatomical, biochemical,
physiological, microbiological, pathological, and pharmacological concepts.
"""

EXPANSION_CONCEPTS = [
    # ==========================================
    # ANATOMİ VE NÖROANATOMİ
    # ==========================================
    ("Nervus Olfactorius (CN I)", ["Anatomi", "KBB", "Nöroloji"], ["cn 1", "olfaktor sinir", "koku siniri", "lamina cribrosa", "anosmi", "kallmann sendromu"]),
    ("Nervus Opticus (CN II)", ["Anatomi", "Göz Hastalıkları", "Nöroloji"], ["cn 2", "optik sinir", "canalis opticus", "bitemporal hemianopsi", "optik kiyazma", "optik norit"]),
    ("Nervus Oculomotorius (CN III)", ["Anatomi", "Göz Hastalıkları", "Nöroloji"], ["cn 3", "okulomotor sinir", "fissura orbitalis superior", "pitozis", "down and out disa asagi bakis", "midriyazis pupilla genislemesi"]),
    ("Nervus Trochlearis (CN IV)", ["Anatomi", "Göz Hastalıkları", "Nöroloji"], ["cn 4", "troklear sinir", "musculus obliquus superior", "vertikal diplopi cift gorme", "basa egme kompanzasyonu", "beyin sapini arkadan terk eden tek kranial sinir"]),
    ("Nervus Ophthalmicus (CN V1)", ["Anatomi", "Nöroloji"], ["cn v1", "oftalmik sinir", "fissura orbitalis superior", "kornea refleksi afferent"]),
    ("Nervus Maxillaris (CN V2)", ["Anatomi", "Nöroloji"], ["cn v2", "maksiller sinir", "foramen rotundum", "trigeminal nevralji"]),
    ("Nervus Mandibularis (CN V3)", ["Anatomi", "Nöroloji"], ["cn v3", "mandibuler sinir", "foramen ovale", "cigneme kaslari m masseter m temporalis"]),
    ("Nervus Abducens (CN VI)", ["Anatomi", "Göz Hastalıkları", "Nöroloji"], ["cn 6", "abdusens siniri", "musculus rectus lateralis", "medial strabismus ice sasilik", "kavernöz sinus en savunmasiz sinir"]),
    ("Nervus Facialis (CN VII)", ["Anatomi", "KBB", "Nöroloji"], ["cn 7", "fasiyal sinir", "foramen stylomastoideum", "mimik kaslari", "chorda tympani on 2 3 tat", "bell palsi kornea refleksi efferent"]),
    ("Nervus Vestibulocochlearis (CN VIII)", ["Anatomi", "KBB"], ["cn 8", "vestibulokoklear sinir", "meatus acusticus internus", "isitme ve denge", "sensorinorol isitme kaybi"]),
    ("Nervus Glossopharyngeus (CN IX)", ["Anatomi", "KBB", "Nöroloji"], ["cn 9", "glossofaringeal sinir", "foramen jugulare", "dil arka 1 3 tat ve duyu", "ogurme gag refleksi afferent", "sinus caroticus baroreseptor"]),
    ("Nervus Vagus (CN X)", ["Anatomi", "Kardiyoloji", "Gastroenteroloji"], ["cn 10", "vagus siniri", "foramen jugulare", "parasempatik ana govde", "n laryngeus recurrens ses kisikligi", "uvula saglam tarafa deviasyon"]),
    ("Nervus Accessorius (CN XI)", ["Anatomi", "Ortopedi ve Travmatoloji"], ["cn 11", "aksesuar sinir", "foramen jugulare", "musculus sternocleidomastoideus scm", "musculus trapezius omuz silkme"]),
    ("Nervus Hypoglossus (CN XII)", ["Anatomi", "Nöroloji"], ["cn 12", "hipoglossus siniri", "canalis hypoglossi", "dilin motor innervasyonu", "dil lezyon tarafina deviye olur"]),
    ("Plexus Brachialis - Truncus Superior (Erb-Duchenne)", ["Anatomi", "Ortopedi ve Travmatoloji", "Pediatri"], ["pleksus brakialis", "erb duchenne felci c5 c6", "bahsis isteyen garson eli waiter tip", "omuz abdüksiyon ve dis rotasyon kaybi"]),
    ("Plexus Brachialis - Truncus Inferior (Klumpke Felci)", ["Anatomi", "Ortopedi ve Travmatoloji", "Pediatri"], ["klumpke felci c8 t1", "pence el claw hand", "horner sendromu birlikteligi t1 sempatik hasar"]),
    ("Nervus Radialis & Düşük El", ["Anatomi", "Ortopedi ve Travmatoloji", "Nöroloji"], ["nervus radialis", "radial sinir", "spiral oluk humerus cisim kirigi", "cumartesi gecesi felci saturday night palsy", "dusuk el wrist drop", "triceps refleksi kaybi"]),
    ("Nervus Medianus & Karpal Tünel Sendromu", ["Anatomi", "Ortopedi ve Travmatoloji", "Nöroloji"], ["nervus medianus", "median sinir", "karpal tunel sendromu", "retinakulum fleksorum alti basisi", "tinel ve phalen testleri", "maymun eli ape hand", "ilk 3 parmakta uyusma"]),
    ("Nervus Ulnaris & Guyon Kanalı", ["Anatomi", "Ortopedi ve Travmatoloji", "Nöroloji"], ["nervus ulnaris", "ulnar sinir", "medial epikondil sulkus hasari", "guyon kanali sendromu", "pence el claw hand serce ve yuzuk parmak"]),
    ("Nervus Axillaris & Omuz Çıkığı", ["Anatomi", "Ortopedi ve Travmatoloji"], ["nervus axillaris", "aksiller sinir", "humerus cerrahi boyun kirigi", "omuz anterior cikigi", "m deltoideus atrofisi omuz apoleti bolgesi duyu kaybi"]),
    ("Nervus Thoracicus Longus & Kanat Skapula", ["Anatomi", "Genel Cerrahi"], ["nervus thoracicus longus", "bell siniri", "musculus serratus anterior", "mastektomi lenf nodu diseksiyonu hasari", "kanat skapula winged scapula"]),
    ("Nervus Peroneus Communis (Fibularis) & Düşük Ayak", ["Anatomi", "Ortopedi ve Travmatoloji", "Nöroloji"], ["peroneal sinir", "fibula basi boynu kirigi", "dusuk ayak foot drop", "stepaj yuruyusu", "ayak sirtinda duyu kaybi eversiyon kaybi"]),
    ("Nervus Femoralis & Patella Refleksi", ["Anatomi", "Nöroloji"], ["femoral sinir", "m quadriceps femoris", "patella refleksi kaybi", "diz ekstansiyon kaybi"]),
    ("Nervus Obturatorius & Uyluk Addüksiyonu", ["Anatomi", "Ortopedi ve Travmatoloji"], ["obturator sinir", "canalis obturatorius", "uyluk adduktor kaslari uyluk ic yuz duyu kaybi"]),
    ("Nervus Pudendus & Pudendal Blok", ["Anatomi", "Kadın Hastalıkları ve Doğum"], ["pudendal sinir", "alcock kanali", "spina ischiadica", "epizyotomi ve dogum analjezisi"]),
    ("Arteria Meningea Media & Foramen Spinosum", ["Anatomi", "Beyin ve Sinir Cerrahisi"], ["arteria meningea media", "foramen spinosum", "pterion kemik kirigi", "epidural hematom kanamasi"]),
    ("Arteria Carotis Interna & Kavernöz Sinüs", ["Anatomi", "Beyin ve Sinir Cerrahisi"], ["arteria carotis interna", "kavernoz sinus icinden gecen arter", "karotikokavernoz fistul pulsatil ekzoftalmus"]),
    ("Truncus Coeliacus (Çölyak Arter)", ["Anatomi", "Genel Cerrahi"], ["truncus coeliacus", "t12 duzeyi", "arteria gastrica sinistra", "arteria splenica", "arteria hepatica communis"]),
    ("Arteria Mesenterica Superior & SMA Sendromu", ["Anatomi", "Genel Cerrahi", "Radyoloji"], ["sma", "arteria mesenterica superior", "l1 duzeyi", "duodenum 3 kitasini aort arasinda sikistirmasi sma sendromu wilkie"]),
    ("Arteria Mesenterica Inferior & Riolan Arkı", ["Anatomi", "Genel Cerrahi"], ["arteria mesenterica inferior", "l3 duzeyi", "arteria colica sinistra", "drummond marjinal arteri", "riolan arki anastomoz"]),
    ("Foramen Ovale Kardiak & Fossa Ovalis", ["Anatomi", "Kardiyoloji", "Pediatri"], ["fossa ovalis", "foramen ovale kalintisi", "septum secundum", "patent foramen ovale pfo paradoksal emboli"]),
    ("Ductus Arteriosus & Ligamentum Arteriosum", ["Anatomi", "Kardiyoloji"], ["ligamentum arteriosum", "duktus arteriyozus kalintisi", "sol n laryngeus recurrens altindan doner"]),
    ("Ductus Venosus & Ligamentum Venosum", ["Anatomi", "Pediatri"], ["ligamentum venosum", "duktus venozus kalintisi", "vena umbilicalis oksijenli kan bypass"]),
    ("Vena Umbilicalis & Ligamentum Teres Hepatis", ["Anatomi", "Gastroenteroloji"], ["ligamentum teres hepatis", "gobek veni kalintisi", "portal hipertansiyonda rekanalizasyon caput medusae cruveilhier baumgarten"]),
    ("Tractus Corticospinalis & Çaprazlaşma (Decussatio)", ["Anatomi", "Nöroloji"], ["kortikospinal traktus", "piramidal yol", "medulla oblongata decussatio pyramidum", "ust motor noron lezyonu babinski spastisite"]),
    ("Fasciculus Gracilis et Cuneatus (Arka Kordon)", ["Anatomi", "Nöroloji"], ["arka kordon", "fasikulus grasilis bacak", "fasikulus kuneatus kol", "derin duyu vibrasyon propriosepsiyon iki nokta ayrimi"]),
    ("Tractus Spinothalamicus Lateralis", ["Anatomi", "Nöroloji"], ["spinotalamik traktus", "agri ve isi duyusu", "omurilige giriste on beyaz komissurada caprazlasir", "siringomiyeli pelerin tarzi duyu kaybi"]),

    # ==========================================
    # BİYOKİMYA VE METABOLİZMA
    # ==========================================
    ("Fosfofruktokinaz-1 (PFK-1)", ["Tıbbi Biyokimya"], ["pfk 1", "glikoliz hiz kisitlayici enzim", "fruktoz 2 6 bisfosfat guclu allosterik aktivator", "atp ve sitrat ile inhibe"]),
    ("Fruktoz-2,6-Bisfosfataz & PFK-2", ["Tıbbi Biyokimya"], ["pfk 2 fbpaz 2", "bifonksiyonel enzim", "insulin PFK-2 yi uyarir glikolizi hizlandirir", "glukagon fbpaz 2 yi uyarir glukoneogenezi tetikler"]),
    ("Pirüvat Dehidrogenaz Kompleksi (PDH)", ["Tıbbi Biyokimya"], ["pdh kompleksi", "piruvati asetil koa ya cevirir", "5 koenzim tpp lipoat koa fad nad", "arsenik zehirlenmesi lipoik asidi baglar"]),
    ("İzositrat Dehidrogenaz", ["Tıbbi Biyokimya"], ["izositrat dehidrogenaz", "krebs sitrik asit dongusu hiz kisitlayici basamak", "nadh ve atp ile inhibe"]),
    ("Glukoz-6-Fosfataz & Karaciğer Glukoz Çıkışı", ["Tıbbi Biyokimya"], ["glukoz 6 fosfataz", "endoplazmik retikulum zari", "kasta bulunmaz karaciger ve bobrekte vardir", "von gierke"]),
    ("Karnitin Palmitoiltransferaz 1 (CPT-1)", ["Tıbbi Biyokimya"], ["cpt 1", "yag asidi beta oksidasyon hiz kisitlayici enzim", "mitokondri dis zari", "malonil koa ile inhibe"]),
    ("HMG-KoA Sentaz & Ketogenez", ["Tıbbi Biyokimya"], ["hmg koa sentaz mitokondriyal", "ketogenez hiz kisitlayici enzim", "aclik ve diyabette keton cisimcigi uretimi"]),
    ("Asetil-KoA Karboksilaz (ACC)", ["Tıbbi Biyokimya"], ["acc", "yag asidi de novo sentez hiz kisitlayici basamak", "biyotin b7 koenzim", "sitrat aktive eder palmitoil koa inhibe eder"]),
    ("Hormona Duyarlı Lipaz (HSL)", ["Tıbbi Biyokimya"], ["hsl", "adipoz doku lipoliz", "glukagon ve epinefrin fosforilasyonla aktive eder", "insulin defosforilasyonla inhibe eder"]),
    ("Lesitin-Kolesterol Açiltransferaz (LCAT)", ["Tıbbi Biyokimya"], ["lcat", "hdl uzerinde kolesterol esterlesmesi", "apo a 1 aktive eder", "ters kolesterol transportu"]),
    ("Karbamoil Fosfat Sentaz 1 (CPS-1)", ["Tıbbi Biyokimya"], ["cps 1", "ure dongusu hiz kisitlayici basamak", "mitokondriyal", "n asetilglutamat nag zorunlu allosterik aktivator"]),
    ("Glutamin-PRPP Amidotransferaz", ["Tıbbi Biyokimya"], ["prpp amidotransferaz", "de novo purin nükleotid sentezi hiz kisitlayici enzim", "amp gmp imp ile geri bildirim inhibisyonu"]),
    ("Ksantin Oksidaz & Ürik Asit Üretimi", ["Tıbbi Biyokimya", "Romatoloji"], ["ksantin oksidaz", "hipoksantin ve ksantini urik aside cevirir", "allopurinol ve febuksostat tarafindan inhibe gut ilaclari"]),
    ("HGPRT Enzimi & Lesch-Nyhan Sendromu", ["Tıbbi Biyokimya", "Tıbbi Genetik", "Pediatri"], ["hgprt", "hipoksantin guanin fosforiboziltransferaz", "purin kurtarma yalagi salvage pathway", "lesch nyhan sendromu kendini isirma dudak parmak yeme gut zeka geriligi x e bagli"]),
    ("Adenozin Deaminaz (ADA) Eksikliği & SCID", ["Tıbbi Biyokimya", "Tıbbi İmmünoloji"], ["ada eksikligi", "adenozin deaminaz", "datp birikimi ribonukleotid reduktaz inhibisyonu", "lenfosit toksisitesi agir kombine immun yetmezlik scid"]),
    ("ALA Sentaz (Aminolevülinik Asit Sentaz)", ["Tıbbi Biyokimya", "Hematoloji"], ["ala sentaz", "hem biyosentezi hiz kisitlayici enzim", "piridoksal fosfat b6 koenzim", "heme tarafindan geri bildirim inhibisyonu", "x e bagli sideroblastik anemi"]),
    ("Tiamin (B1 Vitamini) & Enzimleri", ["Tıbbi Biyokimya", "Nöroloji"], ["tiamin b1", "tpp koenzim", "piruvat dehidrogenaz alfa ketoglutarat dehidrogenaz transketolaz dalli zincirli ketoasit dehidrogenaz", "beriberi kuru beriberi polinöropati islak beriberi kalp yetmezligi wernicke korsakoff"]),
    ("Niasin (B3 Vitamini) & Pellagra 4D", ["Tıbbi Biyokimya", "Dermatoloji"], ["niasin b3", "nad nadp koenzim triptofandan sentez", "pellagra 4d dermatiti diyare demans death olum", "kolyemsi rash casal kolyesi", "hartnup hastaligi triptofan emilim bozuklugu"]),
    ("Kobalamin (B12) & İki Temel Enzimi", ["Tıbbi Biyokimya", "Hematoloji"], ["b12 vitamini", "metiyonin sentaz homosisteini metiyonine cevirir", "metilmalonil koa mutaz suksinil koa ya cevirir"]),
    ("Askorbik Asit (C Vitamini) & Skorbüt", ["Tıbbi Biyokimya", "Romatoloji"], ["c vitamini", "prolil ve lizil hidroksilaz koenzimi kollajen capraz baglanmasi", "demir emilimini artirir fe3 u fe2 ye indirger", "skorbut dis eti kanamalari perifolikuler petesi yara iyilesmesinde gecikme"]),

    # ==========================================
    # KARDİYOLOJİ VE DAMAR HASTALIKLARI
    # ==========================================
    ("Kararlı Angina Pektoris (Stable Angina)", ["Kardiyoloji"], ["kararli angina", "eforla gelen dinlenmeyle veya dilalti nitratla 5 dakikada gecen gogus agrisi", "yuzde 70 koroner arter darligi"]),
    ("Prinzmetal (Vazospastik) Angina", ["Kardiyoloji"], ["prinzmetal angina", "vazospastik angina", "gece veya istirahatte gelen gecici st elevasyonu koroner spazm", "kalsiyum kanal blokorleri ve nitratlar ilk tercih beta blokerler kontrendike"]),
    ("Atriyal Fibrilasyon (AF) & İnme Riski", ["Kardiyoloji", "Nöroloji"], ["atriyal fibrilasyon", "af", "p dalgasi yoklugu duzensiz duzensiz rr intervalleri", "en sik kalici aritmi", "sol atriyal apendiks trombusu embolik inme riski", "chads2 vasc skoru antikoagulasyon"]),
    ("Atriyal Flatter & Testere Dişi", ["Kardiyoloji"], ["atriyal flatter", "d2 d3 avf de testere disi f dalgalari saw tooth", "kavotrikuspid istmus ablasyonu"]),
    ("Ventriküler Taşikardi (VT) & VF", ["Kardiyoloji", "Acil Tıp"], ["ventrikuler tasikardi", "vt", "genis qrs tasikardi av disosiasyon fuzyon ve yakalama capture vurulari", "nabizsiz vt acil defibrilasyon sartsiz", "ventrikuler fibrilasyon vf kaba kaotik dalgalar kardiyak arrest"]),
    ("Torsades de Pointes & Uzun QT", ["Kardiyoloji", "Acil Tıp"], ["torsades de pointes", "polimorfik ventrikuler tasikardi qrs aksinin burgu gibi donmesi", "uzun qt sendromu hipomagnezemi hipokalemi ilaclar", "tedavide iv magnezyum sulfat acil"]),
    ("Brugada Sendromu & Ani Kardiyak Ölüm", ["Kardiyoloji", "Tıbbi Genetik"], ["brugada sendromu", "scna5a sodyum kanal mutasyonu", "v1 v2 de kubbeli st elevasyonu ve sag dal blogu paterni", "genc erkeklerde uykuda ani kardiyak olum icd takilmasi"]),
    ("Birinci Derece AV Blok", ["Kardiyoloji"], ["1 derece av blok", "pr mesafesinin 200 ms 0 20 sn den uzun olmasi her p yi qrs takip eder"]),
    ("Mobitz Tip 1 AV Blok (Wenckebach)", ["Kardiyoloji"], ["mobitz tip 1", "wenckebach", "pr mesafesinin giderek uzamasi ve sonunda bir qrs in dusmesi", "av dugum seviyesindedir benign"]),
    ("Mobitz Tip 2 AV Blok", ["Kardiyoloji"], ["mobitz tip 2", "pr mesafesi sabittir aniden bir qrs duser", "his purkinje sistemi seviyesindedir tam bloka ilerleyebilir pacemaker pil endikasyonu"]),
    ("Üçüncü Derece Tam AV Blok", ["Kardiyoloji", "Acil Tıp"], ["ucuncu derece av blok", "tam blok", "p dalgalari ile qrs kompleksleri tamamen bagimsizdir av disosiasyon", "bradikardi stokes adams senkop ataklari kalici kalp pili"]),
    ("Akut Perikardit & Diffüz ST Elevasyonu", ["Kardiyoloji", "Acil Tıp"], ["akut perikardit", "one egilmekle azalan batan gogus agrisi", "perikardiyal surtunme sesi frotman", "diffuz konkav st elevasyonu ve pr depresyonu avr de pr elevasyonu", "kolşisin ve nsaid"]),
    ("Dressler Sendromu (Post-MI Perikardit)", ["Kardiyoloji"], ["dressler sendromu", "mi sonrasi 2 10 haftada gelisen otoimmun perikardit plorit ates lokositoz", "steroid ve nsaid"]),
    ("Temporal (Dev Hücreli) Arterit & Çene Kladikasyonu", ["Romatoloji", "Nöroloji", "Göz Hastalıkları"], ["temporal arterit", "dev hucreli arterit", "50 yas ustu yeni temporal bas agrisi scalp hassasiyeti cene kladikasyonu", "sedimantasyon hizi esr 100 uzeri", "aion anterior iskemik optik noropati korluk riski", "biyopsi beklemeden acil yuksek doz kortikosteroid", "polimiyaljiya romatika birlikteligi"]),
    ("Takayasu Arteriti (Nabızsızlık Hastalığı)", ["Romatoloji", "Kardiyoloji"], ["takayasu arteriti", "genc kadin nabizsizlik hastaligi pulseless disease", "aort arki ve ana dallarinin granülomatöz panarteriti", "kollar arasi tansiyon nabiz farki karotidini"]),
    ("Poliarteritis Nodosa (PAN) & Hepatit B", ["Romatoloji", "Tıbbi Patoloji"], ["pan", "poliarteritis nodosa", "orta capli musküler arterlerin nekrotizan vaskuliti", "hepatit b hbv birlikteligi yuzde 30", "renal mikroanevrizmalar tespih tanesi anjiyografide hipertansiyon", "akciger damarlari KORUNUR pulmoner tutulum yoktur p anca negatiftir"]),
    ("Kawasaki Hastalığı & Koroner Arter Anevrizması", ["Pediatri", "Kardiyoloji"], ["kawasaki hastaligi", "mukokutanoz lenf nodu sendromu cocuklarda orta capli vaskulit", "5 gunden uzun suren direncli ates", "bilateral eksudasiz konjonktivit cilek dili dudaklarda fisur eritem", "el ayakta odem ve soyulma servikal lenfadenopati", "koroner arter anevrizmasi ve mi riski", "ivig ve yuksek doz aspirin tedavisi"]),
    ("Granülomatozis ve Polianjiitis (Wegener / GPA)", ["Romatoloji", "Göğüs Hastalıkları", "Nefroloji"], ["wegener", "gpa", "c anca pr3 anca pozitifligi", "triad ust solunum yollari kronik sinuzit eyer burun saddle nose alt solunum yollari kaviter noduller ve bobrek kresentik nefrit rpgn", "nekrotizan granülomlar"]),
    ("Mikroskopik Polianjiitis (MPA)", ["Romatoloji", "Nefroloji"], ["mikroskopik polianjiitis", "mpa", "p anca mpo anca pozitifligi", "nekrotizan vaskulit pulmoner renal sendrom", "granülom YOKTUR wegenerden ayrim"]),
    ("Eozinofilik Granülomatozis ve Polianjiitis (Churg-Strauss / EGPA)", ["Romatoloji", "Göğüs Hastalıkları"], ["churg strauss", "egpa", "p anca pozitifligi", "gec baslangicli agir astim periferik kanda belirgin eozinofili nazal polipler mononoritis multipleks"]),
    ("Henoch-Schönlein Purpurası (IgA Vasküliti)", ["Pediatri", "Romatoloji", "Nefroloji"], ["henoch schonlein purpurasi", "hsp", "iga vaskuliti", "cocukta ust solunum yolu enfeksiyonu sonrasi", "tetrad 1 palpabl purpura kalca ve bacak altinda trombosit sayisi normaldir 2 artralji artrit diz ayak bilegi 3 kolik karin agrisi gis kanama invajinasyon 4 mezanjiyal iga glomerülonefriti hematuri"]),
    ("Behçet Hastalığı & Paterji Testi", ["Romatoloji", "Dermatoloji", "Göz Hastalıkları"], ["behcet hastaligi", "ipek yolu hastaligi hla b51 birlikteligi", "tekrarlayan oral aftoz ulserler en erken ve zorunlu bulgu", "agrisiz skarla iyilesen genital ulserler", "hipopiyonlu on ve arka uveit korluk riski", "paterji testi 24 48 saatte steril püstül olusumu", "vaskulobehcet pulmoner arter anevrizmasi ve venoz tromboz"]),
    ("Kolelitiyazis (Safra Taşları) & 4F Kuralı", ["Gastroenteroloji", "Genel Cerrahi"], ["kolelitiyazis", "safra kesesi tasi", "kolesterol taslari en sik yuzde 80 4f kurali female kadin fat obez forty kirk yas fertile dogurgan", "siyah pigment taslari kronik hemoliz orak hucre talasemi siroz", "kahverengi pigment taslari safra yolu enfeksiyonu clonorchis"])
]

# Systematic generation of medical concepts across all organ systems
ORGAN_SYSTEMS = [
    # Hematoloji & Onkoloji
    ("Lösemi Tipleri", "Hematoloji", ["AML M0-M7", "ALL L1-L3", "KML", "KLL", "T-Hücreli Prolenfositik Lösemi", "Saçlı Hücreli Lösemi Hairy Cell", "B-Hücreli Akut Lenfoblastik Lösemi"]),
    ("Lenfoma Tipleri", "Hematoloji", ["Hodgkin Nodüler Sklerozan", "Hodgkin Mikst Sellüler", "Hodgkin Lenfositten Zengin", "Hodgkin Lenfosit Azalmış", "Diffüz Büyük B Hücreli Lenfoma DLBCL", "Foliküler Lenfoma", "Burkitt Lenfoma", "Mantle Hücreli Lenfoma", "MALT Lenfoma", "Marjinal Zon Lenfoma", "Periferik T Hücreli Lenfoma", "Mikozis Fungoides", "Sezary Sendromu", "Anaplastik Büyük Hücreli Lenfoma ALCL"]),
    ("Hemolitik Anemi Tipleri", "Hematoloji", ["Otoimmün Hemolitik Anemi Sıcak Tip IgG", "Soğuk Tip IgM Soğuk Aglütinin", "Paroksismal Soğuk Hemoglobinüri Donath-Landsteiner", "Herediter Sferositoz", "Herediter Eliptositoz", "G6PD Eksikliği Favizm", "Pirüvat Kinaz Eksikliği", "Paroksismal Noktürnal Hemoglobinüri PNH CD55 CD59", "Mikroanjiyopatik Hemolitik Anemi MAHA", "İntravasküler vs Ekstravasküler Hemoliz"]),
    ("Pıhtılaşma Faktör Eksiklikleri", "Hematoloji", ["Hemofili A Faktör 8", "Hemofili B Faktör 9 Christmas", "Hemofili C Faktör 11", "von Willebrand Hastalığı Tip 1 2 3", "Faktör 7 Eksikliği İzole PT Uzaması", "Faktör 10 Eksikliği", "Faktör 5 Eksikliği", "Faktör 13 Eksikliği Pıhtı Lizis Testi", "Protrombin Eksikliği", "Afibrinojenemi"]),
    ("Miyeloproliferatif Neoplaziler", "Hematoloji", ["Polisitemia Vera JAK2 V617F", "Esansiyel Trombositemi JAK2 CALR MPL", "Primer Miyelofibroz Gözyaşı Hücreleri Dakriyosit", "Kronik Nötrofilik Lösemi", "Kronik Eozinofilik Lösemi", "Mastositoz"]),
    ("Trombotik Mikroanjiyopatiler", "Hematoloji", ["Trombotik Trombositopenik Purpura TTP ADAMTS13", "Atipik Hemolitik Üremik Sendrom aHUS Kompleman Defekti", "Shiga Toksin İlişkili HÜS D+ HÜS", "İlaca Bağlı Trombotik Mikroanjiyopati"]),

    # Gastroenteroloji & Karaciğer
    ("Hepatit Virüsleri & Serolojisi", "Gastroenteroloji", ["Hepatit A Virüsü HAV Fekal Oral", "Hepatit B HBsAg Anti-HBs Anti-HBc IgM IgG HBeAg", "Hepatit C HCV Kronikleşme Siroz HCC", "Hepatit D HDV Süperenfeksiyon Koinfeksiyon", "Hepatit E HEV Gebede Fulminan Karaciğer Yetmezliği"]),
    ("Hepatobiliyer ve Pankreas Lezyonları", "Gastroenteroloji", ["Karaciğer Basit Kisti", "Hepatik Kavernöz Hemanjiom", "Fokal Nodüler Hiperplazi FNH Santral Skar", "Hepatik Adenom Oral Kontraseptif Rüptür", "Hepatosellüler Karsinom HCC AFP", "Kolanjiokarsinom Klatskin Tümörü", "Safra Kesesi Karsinomu Porselen Kese", "Pankreas Müsinöz Kistik Neoplazisi", "Pankreas Seröz Kistadenomu", "Solid Psödopapiller Pankreas Tümörü", "Pankreatik İntraduktal Papiller Müsinöz Neoplazi IPMN", "Pankreas Nöroendokrin Tümörü İnsülinoma", "Pankreas Gastrinoma Glukagonoma VIPoma Somatostatinoma"]),
    ("Mide & Bağırsak Hastalıkları", "Gastroenteroloji", ["Helicobacter pylori Gastriti", "Otoimmün Metaplastik Atrofik Gastrit", "Menetrier Hastalığı Dev Mukoza Katlantıları Protein Kaybı", "Duedonum Ülseri Açlıkla Ağrıyan", "Mide Ülseri Yemekle Ağrıyan", "Gastrointestinal Stromal Tümör GIST c-KIT CD117 DOG1", "İntestinal Psödoobstrüksiyon Ogilvie Sendromu", "Kısa Bağırsak Sendromu Malabsorbsiyon", "Bakteriyel Aşırı Çoğalma Sendromu SIBO", "Mikroskopik Kolit Kollajenöz ve Lenfositik Kolit"]),

    # Nefroloji & Üroloji
    ("Glomerüler Sendromlar", "Nefroloji", ["Minimal Lezyon Hastalığı", "FSGS Fokal Segmental Glomerüloskleroz", "Membranöz Nefropati PLA2R", "Diyabetik Glomerüloskleroz Kimmelstiel-Wilson", "Renal Amiloidoz", "Poststreptokoksik Glomerülonefrit", "IgA Nefropatisi Berger", "Goodpasture Sendromu Anti-GBM", "Lupus Nefriti Evre 1-6 Tel Halkası Wire Loop", "MPGN Tip 1 Subendotelyal", "MPGN Tip 2 Yoğun Depo Dense Deposit C3 Nefritik Faktör"]),
    ("Tübüler ve İnterstisiyel Hastalıklar", "Nefroloji", ["Akut Tübüler Nekroz İskemik Toksik Çamur Silendirleri", "Akut İnterstisiyel Nefrit Ateş Döküntü Eozinofilüri", "Renal Tübüler Asidoz Tip 1 Distal Hipokalemi Taş", "Renal Tübüler Asidoz Tip 2 Proksimal Bikarbonat Fanconi", "Renal Tübüler Asidoz Tip 4 Hiperkalemik Aldosteron Direnci", "Kronik İnterstisiyel Nefrit Analjezik Nefropatisi Papiller Nekroz"]),
    ("Böbrek ve Üriner Tümörler", "Üroloji", ["Berrak Hücreli Renal Karsinom VHL", "Papiller Renal Karsinom MET", "Kromofob Renal Hücreli Karsinom", "Renal Onkositom Santral Çökük Skar", "Renal Anjiyomiyolipom Tuberoskleroz", "Mesane Ürotelyal Karsinomu Ağrısız Hematüri", "Prostat Adenokarsinomu Gleason Skoru", "Seminom Fried Egg Hücreleri", "Non-Seminomatöz Testis Tümörleri Embriyonal Teratom Koryokarsinom"]),

    # Endokrinoloji & Metabolizma
    ("Tiroid ve Paratiroid Hastalıkları", "Endokrinoloji", ["Graves Hastalığı Ekzoftalmi Pretibiyal Miksödem TRAb", "Hashimoto Tiroiditi Hürthle Hücreleri Anti-TPO", "Subakut Granülomatöz Tiroidit de Quervain Ağrılı", "Riedel Tiroiditi Taş Gibi Sert IgG4", "Toksik Multinodüler Guatr Plummer", "Papiller Tiroid Kanseri Orphan Annie Psammom", "Foliküler Tiroid Kanseri Kapsül İnvazyonu", "Medüller Tiroid Kanseri Kalsitonin Amiloid RET", "Anaplastik Tiroid Kanseri", "Primer Hiperparatiroidizm Adenom", "Sekonder Hiperparatiroidizm KBH", "Tersiyer Hiperparatiroidizm Otonom", "Hipoparatiroidizm Tetani Chvostek Trousseau", "Psödohipoparatiroidizm Albright"]),
    ("Hipofiz ve Sürrenal Bozukluklar", "Endokrinoloji", ["Prolaktinoma Galaktore Amenore", "Akromegali Gigantizm IGF-1 OGTT", "Cushing Hastalığı ACTH Mikroadenom", "Hipofiz Apopleksisi Sheehan Sendromu", "Santral ve Nefrojenik Diabetes İnsipidus", "Uygunsuz ADH Salınımı Sendromu SIADH", "Primer Adrenal Yetmezlik Addison", "Sekonder Adrenal Yetmezlik Hipopituitarizm", "Konjenital Adrenal Hiperplazi 21-Hidroksilaz", "Primer Hiperaldosteronizm Conn", "Feokromositoma Katekolamin Salgısı", "MEN 1 Wermer 3P", "MEN 2A Sipple RET", "MEN 2B RET Nörom"]),

    # Nöroloji ve Nöroşirürji
    ("Serebrovasküler Olaylar ve Kanamalar", "Nöroloji", ["Orta Serebral Arter MCA Enfarktı", "Ön Serebral Arter ACA Enfarktı Bacak Güçsüzlüğü", "Arka Serebral Arter PCA Enfarktı Homonim Hemianopsi", "Baziler Arter Oklüzyonu Kilitlenme Sendromu Locked-in", "Laküner Enfarkt İnternal Kapsül Saf Motor İnme", "Epidural Hematom Arteria Meningea Media Lüsid İnterval", "Subdural Hematom Köprü Venler Hilal Görünüm", "Subaraknoid Kanama Anevrizma Gök Gürültüsü Baş Ağrısı", "İntraserebral Parankimal Kanama Charcot-Bouchard"]),
    ("Hareket Bozuklukları ve Nörodejenerasyon", "Nöroloji", ["Parkinson Hastalığı İstirahat Tremoru Rijidite Bradikinezi", "Multipl Sistem Atrofisi MSA Shy-Drager", "Progresif Supranükleer Palsi PSP Vertikal Bakış Felci", "Kortikobazal Dejenerasyon Yabancı El Sendromu Alien Hand", "Huntington Hastalığı CAG Kore Demans", "Esansiyel Tremor Hareketle Artan Alkolle Azalan Propranolol", "Wilson Hastalığı Kanat Çırpma Tremoru Kayser-Fleischer", "Distoni Tortikollis Blefarospazm Yazar Krampı", "Tourette Sendromu Motor ve Vokal Tikler Koprolali"]),
    ("Demiyelinizan ve Motor Nöron Hastalıkları", "Nöroloji", ["Multipl Skleroz MS Oligoklonal Bant Optik Nörit", "Nöromiyelitis Optika NMO Devic Anti-Aquaporin-4 AQP4", "Akut Dissemine Ensefalomiyelit ADEM Viral Enfeksiyon Sonrası", "Amyotrofik Lateral Skleroz ALS Üst ve Alt Motor Nöron", "Spinal Müsküler Atrofi SMA SMN1 Ön Boynuz Motor Nöron", "Guillain-Barré Sendromu Asendan Felç Albüminositolojik Disosiasyon", "Kronik İnflamatuar Demiyelinizan Polinöropati CIDP"]),

    # Pediatri & Çocuk Sağlığı
    ("Çocukluk Çağı Ekzantemleri", "Pediatri", ["Kızamık Rubeola Koplik Lekeleri Krup", "Kızamıkçık Rubella Forchheimer Postauriküler LAP", "Suçiçeği Varisella Pleomorfik Döküntü", "Eritema İnfeksiyozum 5. Hastalık Tokatlanmış Yüz Parvovirüs B19", "Rozeola İnfantum 6. Hastalık Yüksek Ateş Düşerken Döküntü HHV-6", "Kızıl Scarlatina Çilek Dili Pastia Çizgileri Zımpara Deri", "El-Ayak-Ağız Hastalığı Koksaki A16"]),
    ("Yenidoğan Problemleri", "Pediatri", ["Fizyolojik Sarılık 24 Saat Sonrası İndirekt", "Patolojik Sarılık İlk 24 Saatte Rh ABO Uyuşmazlığı", "Biliyer Atrezi Akolik Beyaz Dışkı Kasai Ameliyatı", "Mekonyum Aspirasyon Sendromu MAS Postterm", "Yenidoğanın Geçici Taşipnesi TTN Yaş Akciğer Sezaryen", "Konjenital Diyafram Hernisi Bochdalek Skafoit Batın", "Nekrotizan Enterokolit NEK Pnömatozis İntestinalis", "Prematüre Retinopatisi ROP Oksijen Toksisitesi"]),

    # Kadın Hastalıkları ve Doğum
    ("Obstetrik Aciller ve Komplikasyonlar", "Kadın Hastalıkları ve Doğum", ["Preeklampsi Hipertansiyon Proteinüri", "Eklampsi Konvülziyon Magnezyum Sülfat", "HELLP Sendromu Hemoliz Karaciğer Enzimi Trombositopeni", "Ablasyo Plasenta Ağrılı Sert Koyu Kanama", "Plasenta Previa Ağrısız Parlak Kırmızı Kanama", "Plasenta Akreata İnkretata Perkreata Myometriyum İnvazyonu", "Uterus Rüptürü Sezaryen Skarı Açılması Bandl Halkası", "Postpartum Kanama Uterus Atonisi Oksitosin Masaj", "Amniyotik Sıvı Embolisi Ani Kardiyak Arrest DİK"]),
    ("Jinekolojik Onkoloji & Patoloji", "Kadın Hastalıkları ve Doğum", ["Servikal İntraepitelyal Neoplazi CIN 1-3 HPV E6 E7", "Serviks Skuamöz Hücreli Karsinom Pap Smear", "Endometriyal Hiperplazi Basit Kompleks Atipili", "Endometrium Karsinomu Postmenopozal Kanama PTEN", "Uterin Leiomiyosarkom Koagülatif Nekroz Atipi Mitoz", "Over Seröz Karsinomu Yüksek Dereceli p53 BRCA CA-125", "Over Müsinöz Karsinomu Psödomiksoma Peritonei", "Granüloza Hücreli Tümör Call-Exner İnhibin", "Sertoli-Leydig Hücreli Tümör Virilizasyon Androjen", "Matur Kistik Teratom Dermoid Kist Rokitansky", "Mol Hidatiform Komplet 46XX Parsiyel 69XXY", "Gestasyonel Koryokarsinom Akciğer Top Güllesi Metastazı"]),

    # Ortopedi, Travmatoloji ve Romatoloji
    ("Kemik Tümörleri ve Displazileri", "Ortopedi ve Travmatoloji", ["Osteoid Osteom Gece Ağrısı Aspirine Yanıt Nidus", "Osteoblastom Vertebra 2 cm den Büyük", "Osteosarkom Codman Üçgeni Güneş Patlaması Rb1 p53", "Kondrosarkom Kıkırdak Matriks Popcorn Benekli Kalsifikasyon", "Ewing Sarkomu t(11;22) Soğan Zarı CD99", "Dev Hücreli Kemik Tümörü Epifiz Sabun Köpüğü", "Anevrizmal Kemik Kisti Sıvı-Sıvı Seviyesi", "Basit Fibröz Displazi Shepherd Crook Baston Deformitesi", "Paget Kemik Hastalığı Mozaik Çini Deseni Yüksek ALP"]),

    # Dermatoloji
    ("Büllöz ve Enflamatuar Deri Hastalıkları", "Dermatoloji", ["Pemfigus Vulgaris Desmoglein 1 ve 3 İntraepidermal Akantoliz Nikolsky Pozitif", "Büllöz Pemfigoid Hemidesmozom BP180 BP230 Subepidermal Nikolsky Negatif", "Dermatitis Herpetiformis Dermal Papilla IgA Çölyak", "Eritema Multiforme Hedef Lezyon Target HSV", "Stevens-Johnson Sendromu SJS Yüzde 10 dan Az Alevlenme", "Toksik Epidermal Nekroliz TEN Yüzde 30 dan Fazla Haşlanmış Deri", "Psoriasis Vulgaris Sedef Gümüş Kepek Auspitz Belirtisi Munro Mikroapseleri", "Liken Planus 6P Pruritik Poligonal Parlak Mor Papül Wickham Çizgileri"]),

    # KBB ve Göz Hastalıkları
    ("KBB ve Baş Boyun Patolojileri", "KBB", ["Meniere Hastalığı Endolenfatik Hidrops Fluktuatuar İşitme Kaybı Tinnitus Vertigo", "Benign Paroksismal Pozisyonel Vertigo BPPV Otolit Kanalitiyazis Dix-Hallpike Epley", "Vestibüler Nörit İşitme Kaybı Olmayan Akut Vertigo", "Otoskleroz Stapes Tabanı Fiksasyonu Schwartze Belirtisi İletim Tipi Carhart Çentiği", "Kolesteatom Kronik Otit İnkus Erozyonu Keratinize Yassı Epitel", "Laringeal Papillomatozis HPV 6 ve 11 Ses Kısıklığı", "Warthin Tümörü Papiller Kistadenoma Lenfomatozum Parotis Sigara İçen Erkek"]),
    ("Göz ve Retina Hastalıkları", "Göz Hastalıkları", ["Akut Açı Kapanması Glokomu Midriatik Damla Taş Gibi Sert Göz Görme Bulanıklığı Hale", "Açık Açılı Glokom Trabeküler Ağ Drenaj Azalması Görme Alanı Daralması Optik Çukurluk Cup/Disk", "Santral Retinal Arter Oklüzyonu Kiraz Kırmızısı Makula Ani Ağrısız Körlük", "Santral Retinal Ven Oklüzyonu Kan Fırtınası Yaygın Hemoraji", "Retina Dekolmanı Işık Çakması Fotopsi Uçuşan Cisimler Perde İnmesi", "Yaşa Bağlı Makula Dejenerasyonu Kuru Tip Drusen Yaş Tip Neovaskülarizasyon Anti-VEGF", "Diyabetik Retinopati Mikroanevrizmalar Sert Eksüdalar Pamuk Yün Lekeleri Proliferatif"])
]

# Unpack group arrays and add detailed terms
for category, discipline, items_list in ORGAN_SYSTEMS:
    for item_text in items_list:
        parts = item_text.split(' ')
        primary_name = parts[0]
        if len(parts) > 1 and not parts[1].startswith('('):
            primary_name += ' ' + parts[1]
        
        full_title = f"{primary_name} ({category})"
        keywords = [primary_name, category] + [p for p in parts if len(p) >= 3]
        EXPANSION_CONCEPTS.append((full_title, [discipline, "Genel Tıp"], keywords))

# Generate individual chemical compounds and drugs
PHARMACOPEIA_COMPOUNDS = [
    # Analjezilker & NSAİİ
    ("Ketorolak Trometamin", ["Farmakoloji", "Acil Tıp"], ["ketorolak", "toradol", "guclu nsaid postoperatif agri"]),
    ("Diklofenak Sodyum", ["Farmakoloji", "Romatoloji"], ["diklofenak", "voltaren", "nsaid eklem agrisi osteoartrit"]),
    ("Naproksen Sodyum", ["Farmakoloji"], ["naproksen", "apranax", "kardiyovaskuler guvenliligi en yuksek nsaid"]),
    ("İbuprofen", ["Farmakoloji", "Pediatri"], ["ibuprofen", "advil", "pediatrik ates dusurucu nsaid pda kapatma"]),
    ("İndometazin", ["Farmakoloji", "Kardiyoloji", "Pediatri"], ["indometazin", "guclu nsaid pda patent duktus arteriyozus kapatici"]),
    ("Piroksikam & Meloksikam", ["Farmakoloji", "Romatoloji"], ["meloksikam", "piroksikam", "nispeten cox 2 secici nsaid gastroprotektif"]),
    ("Selekoksib & Etorikoksib", ["Farmakoloji", "Romatoloji"], ["selekoksib", "etorikoksib", "selektif cox 2 inhibitoru mide kanamasi yapmaz tromboz riski"]),
    ("Parasetamol (Asetaminofen)", ["Farmakoloji", "Toksikoloji"], ["parasetamol", "asetaminofen", "santral cox inhibisyonu napqi toksik metabolit nac antidot"]),

    # Opioidler
    ("Fentanil & Sufentanil", ["Farmakoloji", "Anesteziyoloji ve Reanimasyon"], ["fentanil", "sufentanil", "morfinden 100 kat guclu sentetik opioid transdermal flaster"]),
    ("Morfin Sülfat", ["Farmakoloji", "Anesteziyoloji ve Reanimasyon"], ["morfin", "dogal afyon alkaloidi mu reseptor agonisti solunum depresyonu miyozis kabizlik"]),
    ("Oksikodon & Hidromorfon", ["Farmakoloji", "Algoloji"], ["oksikodon", "hidromorfon", "kanser agrisi kronik agri yonetimi"]),
    ("Metadon", ["Farmakoloji", "Psikiyatri"], ["metadon", "uzun etkili mu agonisti nmda blokoru opioid bagimliligi idame tedavisi"]),
    ("Buprenorfin", ["Farmakoloji", "Psikiyatri"], ["buprenorfin", "subokson", "parsiyel mu agonisti kappa antagonisti tavan etkisi olan opioid"]),
    ("Tramadol", ["Farmakoloji"], ["tramadol", "zayif mu agonisti serotonin ve noradrenalin geri alim inhibitoru nobet esigini dusurur"]),
    ("Kodein", ["Farmakoloji"], ["kodein", "on ilactir cyp2d6 ile morfine donusur antitusif oksuruk surubu"]),
    ("Nalokson", ["Farmakoloji", "Acil Tıp", "Toksikoloji"], ["nalokson", "narcan", "saf opioid reseptor antagonisti opioid doz asimi koma pupilla miyozis tedavisi"]),
    ("Naltrekson", ["Farmakoloji", "Psikiyatri"], ["naltrekson", "oral uzun etkili opioid ve alkol bagimliligi nuks onleme"]),

    # Kardiyovasküler
    ("Amiodaron Hidroklorür", ["Farmakoloji", "Kardiyoloji"], ["amiodaron", "potasyum kanal blokoru sinif 3 akciğer fibrozisi kornea verticillata"]),
    ("Dronedaron", ["Farmakoloji", "Kardiyoloji"], ["dronedaron", "iyotsuz amiodaron turevi tiroid toksisitesi yok"]),
    ("Flekainid Asetat", ["Farmakoloji", "Kardiyoloji"], ["flekainid", "sinif 1c sodyum kanal blokoru yapisal kalp hastaligi olmayan paroksismal af"]),
    ("Propafenon", ["Farmakoloji", "Kardiyoloji"], ["propafenon", "sinif 1c antiaritmik ve zayif beta bloker"]),
    ("Diltiazem", ["Farmakoloji", "Kardiyoloji"], ["diltiazem", "benzotiazepin kalsiyum kanal blokoru kalp hizi kontrolu af"]),
    ("Verapamil", ["Farmakoloji", "Kardiyoloji"], ["verapamil", "fenilalkilamin kkb negatif inotrop dromotrop kabizlik"]),
    ("Nikardipin", ["Farmakoloji", "Kardiyoloji"], ["nikardipin", "iv kalsiyum kanal blokoru hipertansif kriz"]),
    ("Klevidipin", ["Farmakoloji", "Kardiyoloji"], ["klevidipin", "ultra kisa etkili damar secici kkb"]),
    ("Ranolazin", ["Farmakoloji", "Kardiyoloji"], ["ranolazin", "gec sodyum akimi inhibitoru refrakter angina"]),
    ("İvabradin", ["Farmakoloji", "Kardiyoloji"], ["ivabradin", "funny akim if inhibitoru yalnizca kalp hizini yavaslatir"]),
    ("Sakubitril", ["Farmakoloji", "Kardiyoloji"], ["sakubitril", "neprilisin inhibitoru bnp artisi kalp yetmezligi"]),
    ("Bosentan", ["Farmakoloji", "Göğüs Hastalıkları"], ["bosentan", "endotelin reseptor antagonisti pah"]),
    ("Ambrisentan", ["Farmakoloji", "Göğüs Hastalıkları"], ["ambrisentan", "secici eta reseptor blokoru"]),
    ("Riociguat", ["Farmakoloji", "Göğüs Hastalıkları"], ["riociguat", "cozunur guanilat siklaz uyarici cteph"]),
    ("Sodyum Nitroprussid", ["Farmakoloji", "Acil Tıp"], ["sodyum nitroprussid", "vazodilatator siyanur toksisitesi"]),
    ("Hidralazin", ["Farmakoloji", "Kardiyoloji"], ["hidralazin", "arteriyoler dilatator lupus benzeri tablo"]),

    # Endokrin & Metabolizma İlaçları
    ("Regüler İnsülin (Kristalize)", ["Farmakoloji", "Endokrinoloji"], ["reguler insulin", "kisa etkili insan insulini iv verilebilen tek insulin dka tedavisi"]),
    ("NPH İnsülin (İzofan)", ["Farmakoloji", "Endokrinoloji"], ["nph insulin", "orta etkili protamin cinko insulini bulanik"]),
    ("İnsülin Lispro & Aspart", ["Farmakoloji", "Endokrinoloji"], ["lispro", "aspart", "glulizin", "ultra kisa hizli etkili yemekten hemen once"]),
    ("İnsülin Glargin & Detemir", ["Farmakoloji", "Endokrinoloji"], ["glargin", "detemir", "degludek", "pik yapmayan uzun etkili bazal insulin"]),
    ("Metformin", ["Farmakoloji", "Endokrinoloji"], ["metformin", "glukofaj", "biguvanid laktik asidoz riski"]),
    ("Glimepirid", ["Farmakoloji", "Endokrinoloji"], ["glimepirid", "amaryl", "sulfonilure insulin salgilatici"]),
    ("Gliklazid", ["Farmakoloji", "Endokrinoloji"], ["gliklazid", "diamicron", "sulfonilure beta hucre k atp"]),
    ("Pioglitazon", ["Farmakoloji", "Endokrinoloji"], ["pioglitazon", "ppar gama tzd sivi tutulumu"]),
    ("Sitagliptin", ["Farmakoloji", "Endokrinoloji"], ["sitagliptin", "januvia", "dpp 4 inhibitoru"]),
    ("Empagliflozin", ["Farmakoloji", "Endokrinoloji"], ["empagliflozin", "jardiance", "sglt2 inhibitoru"]),
    ("Dapagliflozin", ["Farmakoloji", "Endokrinoloji"], ["dapagliflozin", "forxiga", "sglt2 inhibitoru kalp bobrek"]),
    ("Semaglutid", ["Farmakoloji", "Endokrinoloji"], ["semaglutid", "ozempic", "glp 1 agonisti kilo kaybi"]),
    ("Liraglutid", ["Farmakoloji", "Endokrinoloji"], ["liraglutid", "victoza", "saxenda", "glp 1 agonisti"]),
    ("Tirzepatid", ["Farmakoloji", "Endokrinoloji"], ["tirzepatid", "mounjaro", "gip glp 1 cift agonist"]),
    ("Levotiroksin", ["Farmakoloji", "Endokrinoloji"], ["levotiroksin", "euthyrox", "t4 hormonu hipotiroidi"]),
    ("Propiltiyourasil", ["Farmakoloji", "Endokrinoloji"], ["ptu", "antitiroid gebelik ilk trimester t4 t3 donusum"]),
    ("Metimazol", ["Farmakoloji", "Endokrinoloji"], ["metimazol", "thyromazol", "antitiroid agranulositoz"]),
    ("Zoledronik Asit", ["Farmakoloji", "Endokrinoloji"], ["zoledronik asit", "yillik iv bifosfonat osteoporoz"]),
    ("Denosumab", ["Farmakoloji", "Endokrinoloji"], ["denosumab", "prolia", "rankl antikoru osteoporoz"]),
    ("Teriparatid", ["Farmakoloji", "Endokrinoloji"], ["teriparatid", "forsteo", "rekombinant pth anabolik"]),

    # Antibakteriyeller & Antimikrobiyaller
    ("Seftriakson Sodyum", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["seftriakson", "rocephin", "3 kusak sefalosporin menenjit"]),
    ("Sefepim Dihidroklorür", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["sefepim", "maxipime", "4 kusak sefalosporin febril notropeni"]),
    ("Meropenem Trihidrat", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["meropenem", "meronem", "karbapenem esbl menenjit"]),
    ("Piperasilin-Tazobaktam", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["tazosin", "antipsodomonal penisilin"]),
    ("Vankomisin Hidroklorür", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["vankomisin", "vancocin", "mrsa ilk tercih glikopeptid"]),
    ("Daptomisin Enjeksiyon", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["daptomisin", "cubicin", "vre mrsa bakteriyemi"]),
    ("Linezolid Oral & IV", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["linezolid", "zyvoxid", "oksazolidinon trombositopeni"]),
    ("Kolistin Metansülfonat", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["kolistin", "colimycin", "panrezistan gram negatif"]),
    ("Tigesiklin", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["tigesiklin", "tygacil", "glisilsiklin genis spektrum"]),
    ("Azitromisin Dihidrat", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["azitromisin", "zitromax", "atipik pnomoni klamidya"]),
    ("Klaritromisin", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["klaritromisin", "klacid", "h pylori makrolid"]),
    ("Moksifloksasin", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["moksifloksasin", "avelox", "solunum kinolonu anaerop"]),
    ("Siprofloksasin", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["siprofloksasin", "cipro", "florokinolon idrar yolu"]),
    ("Levofloksasin", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["levofloksasin", "tavanic", "solunum kinolonu pnomoni"]),

    # Onkoloji ve Biyolojik İlaçlar
    ("Rituksimab", ["Farmakoloji", "Hematoloji", "Tıbbi Onkoloji"], ["rituksimab", "mabthera", "anti cd20 monoklonal antikoru b hucreli lenfoma"]),
    ("Trastuzumab", ["Farmakoloji", "Tıbbi Onkoloji"], ["trastuzumab", "herceptin", "anti her2 neu antikoru meme kanseri kardiyotoksisite"]),
    ("Bevasizumab", ["Farmakoloji", "Tıbbi Onkoloji"], ["bevasizumab", "avastin", "anti vegf anjiyogenez inhibitoru kolorektal ca kanama hipertansiyon"]),
    ("Setuksimab", ["Farmakoloji", "Tıbbi Onkoloji"], ["setuksimab", "erbitux", "anti egfr kras wild tip kolorektal ca akneiform dokuntu"]),
    ("Pembrolizumab", ["Farmakoloji", "Tıbbi Onkoloji"], ["pembrolizumab", "keytruda", "anti pd 1 immun kontrol noktasi inhibitoru melanom akciger"]),
    ("Nivolumab", ["Farmakoloji", "Tıbbi Onkoloji"], ["nivolumab", "opdivo", "anti pd 1 checkpoint inhibitoru"]),
    ("İpilimumab", ["Farmakoloji", "Tıbbi Onkoloji"], ["ipilimumab", "yervoy", "anti ctla 4 monoklonal antikoru otoimmun kolit"]),
    ("İmatinib Mezilat", ["Farmakoloji", "Hematoloji"], ["imatinib", "gleevac", "bcr abl ve c kit tirozin kinaz inhibitoru kml gist"]),
    ("Erlotinib & Osimertinib", ["Farmakoloji", "Tıbbi Onkoloji"], ["erlotinib", "osimertinib", "tagrisso", "egfr tirozin kinaz mutasyonlu akciger ca t790m"]),
    ("Krizotinib & Alektinib", ["Farmakoloji", "Tıbbi Onkoloji"], ["krizotinib", "alektinib", "alk fuzon pozitif akciger karsinomu"]),
    ("Bortezomib", ["Farmakoloji", "Hematoloji"], ["bortezomib", "velcade", "26s proteazom inhibitoru multipl miyelom periferik noropati"]),
    ("Lenalidomid", ["Farmakoloji", "Hematoloji"], ["lenalidomid", "revlimid", "imid talidomid analoğu sereblon baglanmasi miyelom 5q delesyon"]),
    ("Venetoklaks", ["Farmakoloji", "Hematoloji"], ["venetoklaks", "venclyxto", "bcl 2 inhibitoru kll tumor lizis sendromu riski"]),
    ("Metotreksat (MTX)", ["Farmakoloji", "Romatoloji", "Tıbbi Onkoloji"], ["metotreksat", "dihidrofolat reduktaz inhibitoru folat antagonisti lovokorin kurtarma"]),
    ("Siklofosfamid", ["Farmakoloji", "Tıbbi Onkoloji", "Romatoloji"], ["siklofosfamid", "alkilleyici ajan akrolein metaboliti hemorajik sistit mesna antidot"]),
    ("Sisplatin & Karboplatin", ["Farmakoloji", "Tıbbi Onkoloji"], ["sisplatin", "karboplatin", "platin analoğu capraz bag olusumu nefrotoksisite ototoksisite amifostin"]),
    ("Doksorubisin (Adriamisin)", ["Farmakoloji", "Tıbbi Onkoloji"], ["doksorubisin", "adriamisin", "antrasiklin topoizomeraz 2 serbest radikal kardiyotoksisite deksrazoksan antidot"]),
    ("Paklitaksel & Dosetaksel", ["Farmakoloji", "Tıbbi Onkoloji"], ["paklitaksel", "taksan mikrotubul hiperstabilizasyonu depolimerizasyon engeli noropati"]),
    ("Vinkristin & Vinblastin", ["Farmakoloji", "Tıbbi Onkoloji"], ["vinkristin", "vinka alkaloidi tubulin polimerizasyon engeli periferik noropati kabizlik intratikal olumcul"])
]

ADDITIONAL_CLINICAL_CONCEPTS = [
    # Fizik Muayene Bulguları, Refleksler ve Eponimler
    ("Romberg Testi & Duyusal Ataksi", ["Nöroloji"], ["romberg testi", "arka kordon lezyonu", "propriyosepsiyon kaybi", "gozler kapaliyken dengenin bozulmasi"]),
    ("Babinski Belirtisi & Piramidal Yol", ["Nöroloji"], ["babinski belirtisi", "ekstansor taban derisi refleksi", "kortikospinal traktus lezyonu", "ust motor noron"]),
    ("Chaddock ve Oppenheim Belirtileri", ["Nöroloji"], ["chaddock belirtisi", "oppenheim belirtisi", "gordon belirtisi", "piramidal yol hasari alternatif refleksler"]),
    ("Hoffman ve Trömner Refleksleri", ["Nöroloji"], ["hoffman refleksi", "tromner refleksi", "ust ekstremite ust motor noron bulgusu parmak fleksiyonu"]),
    ("Rinne ve Weber İşitme Testleri", ["KBB"], ["rinne testi", "weber testi", "diapazon testi", "iletim tipi isitme kaybi kemik yolu hava yolundan uzun", "sensorinorol isitme kaybi saglam kulaga lateralizasyon"]),
    ("Dix-Hallpike Manevrası & Epley", ["KBB", "Nöroloji"], ["dix hallpike manevrasi", "epley manevrasi", "bppv benign paroksismal pozisyonel vertigo", "posterior semisirkuler kanal otolit"]),
    ("Lachman Testi & Ön Çekmece", ["Ortopedi ve Travmatoloji"], ["lachman testi", "on cekmece testi", "on capraz bag oçb acl yirtigi"]),
    ("McMurray ve Apley Testleri", ["Ortopedi ve Travmatoloji"], ["mcmurray testi", "apley testi", "medial ve lateral meniskus yirtigi dizde kilitlenme"]),
    ("Pivot Shift Testi", ["Ortopedi ve Travmatoloji"], ["pivot shift testi", "on capraz bag instabilitesi dinamik test"]),
    ("Valgus ve Varus Stres Testleri", ["Ortopedi ve Travmatoloji"], ["valgus stres testi mcl ic yan bag", "varus stres testi lcl dis yan bag diz"]),
    ("Thompson Testi & Aşil Tendonu", ["Ortopedi ve Travmatoloji"], ["thompson testi", "baldir sikilinca plantar fleksiyon kaybi", "asil tendonu rupture"]),
    ("Thomas Testi & Kalça Fleksiyonu", ["Ortopedi ve Travmatoloji"], ["thomas testi", "iliopsoas gerginligi kalca fleksor kontrakturu"]),
    ("Trendelenburg Testi & N. Gluteus Medius", ["Ortopedi ve Travmatoloji", "Nöroloji"], ["trendelenburg testi", "n gluteus superior", "m gluteus medius yetmezligi karsi kalcanin dusmesi ordek yuruyusu"]),
    ("Finkelstein Testi & De Quervain", ["Ortopedi ve Travmatoloji", "Fiziksel Tıp ve Rehabilitasyon"], ["finkelstein testi", "de quervain tenosinoviti", "m abductor pollicis longus m extensor pollicis brevis basparmak agrisi"]),
    ("Cozen ve Mill Testleri (Tenisçi Dirseği)", ["Ortopedi ve Travmatoloji"], ["cozen testi", "mill testi", "lateral epikondilit tenisci dirsegi"]),
    ("Golfçü Dirseği Testi (Medial Epikondilit)", ["Ortopedi ve Travmatoloji"], ["medial epikondilit golfcu dirsegi fleksor pronator tendon zorlanmasi"]),
    ("Roos ve Adson Testleri (TOS)", ["Kalp ve Damar Cerrahisi", "Nöroloji"], ["roos testi", "adson testi", "wright testi", "torasik cikis sendromu tos subklavyan arter brakial pleksus"]),
    ("Spurling Testi & Servikal Radikülopati", ["Beyin ve Sinir Cerrahisi", "Fiziksel Tıp ve Rehabilitasyon"], ["spurling testi", "boyun ekstansiyon ve yana egme ile kola vuran agri servikal disk hernisi"]),
    ("Lasegue (SLR) & Bragard Testleri", ["Beyin ve Sinir Cerrahisi", "Fiziksel Tıp ve Rehabilitasyon"], ["lasegue testi", "duz bacak kaldirma slr", "bragard testi dorsifleksiyon", "lomber disk hernisi siyatik sinir germe"]),
    ("Patrick (FABER) Testi & Sakroiliit", ["Romatoloji", "Ortopedi ve Travmatoloji"], ["patrick testi", "faber fleksiyon abduksiyon eksternal rotasyon", "sakroiliak eklem patolojisi ankilozan spondilit"]),
    ("Gaenslen Testi", ["Romatoloji"], ["gaenslen testi", "sakroiliit provokasyon testi"]),
    ("Schober Testi & Omurga Hareketi", ["Romatoloji"], ["schober testi", "modifiye schober", "lomber omurga fleksiyon kisitliligi ankilozan spondilit 5 cm den az uzama"]),
    ("Homan Belirtisi & DVT", ["Kardiyoloji", "Kalp ve Damar Cerrahisi"], ["homan belirtisi", "ayagin pasif dorsifleksiyonu ile baldirda agri derin ven trombozu dvt"]),
    ("Pemberton Belirtisi", ["Endokrinoloji", "Genel Cerrahi"], ["pemberton belirtisi", "kollari yukari kaldirinca yüzde kizarma siyanoz juguler dolgunluk retrosternal guatr"]),
    ("Kussmaul Belirtisi", ["Kardiyoloji"], ["kussmaul belirtisi", "inspiryumda juguler venoz basincin paradoksal artisi konstriktif perikardit"]),
    ("Beck Triadı (Kardiyak Tamponad)", ["Kardiyoloji", "Acil Tıp"], ["beck triadi", "hipotansiyon venoz dolgunluk boguk kalp sesleri tamponad"]),
    ("Charcot Kolanjit Triadı", ["Gastroenteroloji", "Genel Cerrahi"], ["charcot triadi", "ates sarilik sag ust kadran agrisi akut kolanjit"]),
    ("Reynolds Pentadı (Süpüratif Kolanjit)", ["Gastroenteroloji", "Genel Cerrahi"], ["reynolds pentadi", "charcot triadi + sok hipotansiyon ve bilinc bulanikligi konfuzyon acil drenaj"]),
    ("Virchow Triadı (Tromboz)", ["Tıbbi Patoloji", "Hematoloji"], ["virchow triadi", "endotel hasari staz hiperkoagulabilite"]),
    ("Cushing Triadı (KİBAS)", ["Beyin ve Sinir Cerrahisi", "Acil Tıp"], ["cushing triadi", "kibas intrakraniyal basinc artisi hipertansiyon bradikardi duzensiz solunum"]),
    ("Whipple Triadı (İnsülinoma)", ["Endokrinoloji", "Genel Cerrahi"], ["whipple triadi", "hipoglisemi semptomlari glukoz 50 alti glukozla duzelme insulinoma"]),
    ("Horner Sendromu Triadı", ["Nöroloji", "Göz Hastalıkları"], ["horner sendromu", "pitozis miyozis anhidrozis enoftalmus servikal sempatik"]),
    ("Wernicke Triadı", ["Nöroloji", "Tıbbi Biyokimya"], ["wernicke triadi", "oftalmopleji ataksi konfuzyon tiamin b1"]),
    ("Samter (Widal) Triadı", ["Göğüs Hastalıkları", "KBB"], ["samter triadi", "astim nazal polipozis aspirin asiri duyarliligi aerd"]),
    ("Reiter Triadı (Reaktif Artrit)", ["Romatoloji", "Üroloji"], ["reiter triadi", "artrit uretrit konjonktivit goremiyor iseyemiyor tirnamiyor"]),
    ("Hutchinson Triadı (Konjenital Sifiliz)", ["Pediatri", "Enfeksiyon Hastalıkları"], ["hutchinson triadi", "centikli hutchinson disleri interstisiyel keratit 8 sinir sagirligi"]),
    ("Hakim-Adams Triadı (NPH)", ["Nöroloji", "Beyin ve Sinir Cerrahisi"], ["hakim adams triadi", "normal basincli hidrosefali nph yuruyus apraksisi idrar inkontinansi demans"]),
    ("Saint Triadı", ["Gastroenteroloji", "Genel Cerrahi"], ["saint triadi", "kolelitiyazis hiatal herni kolon divertikülozu"]),
    ("Leriche Sendromu", ["Kalp ve Damar Cerrahisi"], ["leriche sendromu", "aortoiliak okluzyon kalca uyluk kladikasyonu femoral nabiz yoklugu impotans"]),
    ("Budd-Chiari Sendromu", ["Gastroenteroloji"], ["budd chiari sendromu", "hepatik ven trombozu asit hepatomegali karin agrisi"]),
    ("Waterhouse-Friderichsen Sendromu", ["Enfeksiyon Hastalıkları", "Endokrinoloji"], ["waterhouse friderichsen", "meningokoksemi bilateral adrenal kanama sok"]),
    ("Heyde Sendromu", ["Kardiyoloji", "Gastroenteroloji"], ["heyde sendromu", "aort stanozu gis anjiyodisplazisi vwf eksikligi kanama"]),
    ("Osler-Weber-Rendu Sendromu (HHT)", ["Tıbbi Genetik", "KBB"], ["osler weber rendu", "hht mukokutanoz telenjiektazi tekrarlayan burun kanamasi epistaksis avm"]),
    ("Trousseau Belirtisi & Gezici Tromboflebit", ["Tıbbi Onkoloji", "Gastroenteroloji"], ["trousseau sendromu", "tromboflebitis migrans gezici ven iltihabi pankreas ca"]),
    ("Plummer-Vinson Sendromu", ["Gastroenteroloji", "Hematoloji"], ["plummer vinson", "demir eksikligi ozofageal web disfaji skuamoz ca"]),
    ("Felty Sendromu", ["Romatoloji", "Hematoloji"], ["felty sendromu", "romatoid artrit splenomegali notropeni"]),
    ("Caplan Sendromu", ["Göğüs Hastalıkları", "Romatoloji"], ["caplan sendromu", "romatoid artrit pnomokonyoz akciger nodulleri"]),
    ("Löfgren Sendromu", ["Göğüs Hastalıkları", "Romatoloji"], ["lofgren sendromu", "akut sarkoidoz eritema nodozum bilateral hiler lap artralji ates"]),
    ("Chvostek Belirtisi", ["Endokrinoloji", "Nöroloji"], ["chvostek belirtisi", "fasiyal sinire vurunca yuz kaslarinda seğirme hipokalsemi"]),
    ("Trousseau Belirtisi (Karpopedal Spazm)", ["Endokrinoloji"], ["trousseau belirtisi", "tansiyon aleti mansetini sisirince ebe eli karpopedal spazm hipokalsemi"]),
    ("Kernig ve Brudzinski Belirtileri", ["Enfeksiyon Hastalıkları", "Nöroloji"], ["kernig belirtisi", "brudzinski belirtisi", "menengeal iritasyon menenjit subaraknoid kanama"]),
    ("Murphy Belirtisi", ["Genel Cerrahi", "Gastroenteroloji"], ["murphy belirtisi", "sag ust kadrana basinca inspiryumun agriyla kesilmesi akut kolesistit"]),
    ("McBurney, Rovsing, Psoas ve Obturator", ["Genel Cerrahi"], ["mcburney noktasi", "rovsing belirtisi", "psoas belirtisi", "obturator belirtisi", "akut apandisit"]),
    ("Cullen ve Grey-Turner Belirtileri", ["Gastroenteroloji", "Genel Cerrahi"], ["cullen belirtisi periumblikal", "grey turner belirtisi flank lomber ekimoz", "retroperitoneal kanama akut pankreatit"]),
    ("Schamroth Belirtisi (Çomak Parmak)", ["Göğüs Hastalıkları", "Kardiyoloji"], ["schamroth belirtisi", "comak parmak tirnak pencere kaybi kronik hipoksi akciger ca siyanotik kalp"]),

    # Toksikoloji ve Spesifik Antidotlar
    ("N-Asetilsistein (NAC) & Parasetamol Toksisitesi", ["Farmakoloji", "Toksikoloji"], ["n asetilsistein", "nac", "parasetamol zehirlenmesi antidotu glutatyon replasmani"]),
    ("Nalokson & Opioid Aşırı Dozu", ["Farmakoloji", "Toksikoloji", "Acil Tıp"], ["nalokson", "narcan", "opioid antidotu solunum depresyonu koma"]),
    ("Flumazenil & Benzodiazepin İntoksikasyonu", ["Farmakoloji", "Toksikoloji"], ["flumazenil", "benzodiazepin antidotu"]),
    ("Atropin ve Pralidoksim (PAM) & Organofosfat", ["Farmakoloji", "Toksikoloji", "Acil Tıp"], ["atropin", "pralidoksim", "pam", "organofosfat karbamat bilesik zehirlenmesi kolinesteraz reaktivatoru"]),
    ("Fomepizol ve Etanol & Metanol Zehirlenmesi", ["Farmakoloji", "Toksikoloji"], ["fomepizol", "etanol", "alkol dehidrogenaz adh inhibitoru metanol etilen glikol formik asit korluk"]),
    ("Deferoksamin & Akut Demir Zehirlenmesi", ["Farmakoloji", "Toksikoloji", "Pediatri"], ["deferoksamin", "demir selatoru vin rose kirmizi idrar demir intoksikasyonu"]),
    ("D-Penisilamin & Bakır Zehirlenmesi", ["Farmakoloji", "Toksikoloji", "Gastroenteroloji"], ["d penisilamin", "wilson hastaligi bakir selasyonu idrarla atilim"]),
    ("Dimerkapirol (BAL) & Kurşun/Arsenik/Cıva", ["Farmakoloji", "Toksikoloji"], ["dimerkapirol", "bal", "kursun arsenik civa agir metal selatoru"]),
    ("Kalsiyum Disodyum EDTA & Süksimer", ["Farmakoloji", "Toksikoloji"], ["edta", "suksimer dmsa", "kursun zehirlenmesi cocukta oral selasyon"]),
    ("Digoksin Spesifik Fab (DigiFab)", ["Farmakoloji", "Toksikoloji", "Kardiyoloji"], ["digifab", "digoksin spesifik antikor fragmani agir digoksin aritmisi hiperkalemi"]),
    ("Glukagon & Beta Bloker Toksisitesi", ["Farmakoloji", "Toksikoloji", "Kardiyoloji"], ["glukagon", "beta bloker intoksikasyonu antidotu camp artisi pozitif inotrop"]),
    ("Kalsiyum Glukonat & KKB Zehirlenmesi", ["Farmakoloji", "Toksikoloji"], ["kalsiyum glukonat", "kalsiyum klorur", "kalsiyum kanal blokoru toksisitesi hiperkalemi"]),
    ("Sodyum Bikarbonat & TCA Zehirlenmesi", ["Farmakoloji", "Toksikoloji", "Kardiyoloji"], ["sodyum bikarbonat", "tca trisiklik antidepresan qrs genislemesi alkalinize edici salisilat"]),
    ("Protamin Sülfat & Heparin Aşırı Dozu", ["Farmakoloji", "Toksikoloji", "Hematoloji"], ["protamin sulfat", "heparin notralizasyonu bazik protein kanama"]),
    ("K Vitamini (Fitonadion) ve PCC & Varfarin Kanaması", ["Farmakoloji", "Toksikoloji", "Hematoloji"], ["k vitamini fitonadion", "pcc protrombin kompleks konsantresi", "varfarin kanamasi acil inr duzeltme"]),
    ("İdarusizumab (Praxbind) & Dabigatran Antidotu", ["Farmakoloji", "Toksikoloji", "Hematoloji"], ["idarusizumab", "praxbind", "dabigatran monoklonal antidotu"]),
    ("Andeksanet Alfa & Faktör Xa Antidotu", ["Farmakoloji", "Toksikoloji", "Hematoloji"], ["andeksanet alfa", "rivaroksaban apiksaban rekombinant modifiye faktor 10a yemi"]),
    ("Metilen Mavisi & Methemoglobinemi", ["Farmakoloji", "Toksikoloji", "Hematoloji"], ["metilen mavisi", "methemoglobinemi fe3 u fe2 ye indirger dapson prilokain kahverengi kan"]),
    ("Piridoksin (B6 Vitamini) & İzoniyazid Toksisitesi", ["Farmakoloji", "Toksikoloji"], ["piridoksin b6", "izoniyazid inh zehirlenmesi direncli nobet gaba sentezi"]),
    ("Oktreotid & Sülfonilüre Hipoglisemisi", ["Farmakoloji", "Toksikoloji", "Endokrinoloji"], ["oktreotid", "sulfonilure hipoglisemisi somatostatin analoğu insulin salinimi blokaji"]),
    ("İntravenöz Lipid Emülsiyonu (%20 İntralipid) & LAST", ["Farmakoloji", "Toksikoloji", "Anesteziyoloji ve Reanimasyon"], ["intralipid", "lokal anestezik sistemik toksisitesi last bupivakain kardiyotoksisite"]),
    ("Fizostigmin Salisilat & Antikolinerjik Sendrom", ["Farmakoloji", "Toksikoloji"], ["fizostigmin", "tersiyer amin kan beyin bariyerini gecer atropin antihistaminik antikolinerjik kriz"]),
    ("Siproheptadin & Serotonin Sendromu", ["Farmakoloji", "Toksikoloji", "Psikiyatri"], ["siproheptadin", "5 ht2a antagonisti serotonin sendromu rijidite klonus"]),
    ("Dantrolen Sodyum & Malign Hipertermi", ["Farmakoloji", "Toksikoloji", "Anesteziyoloji ve Reanimasyon"], ["dantrolen", "malign hipertermi halotan suksinilkolin nms ryr1 kalsiyum salinimi blokaji"]),

    # Ek Tıbbi Terimler & Sendromlar
    ("Anjiyotensin Reçetesi & Renin Salgısı", ["Fizyoloji", "Kardiyoloji"], ["renin anjiyotensin aldosteron raas", "jukstaglomeruler aparat jga", "makula densa sodyum algilama", "at1 ve at2 reseptorleri"]),
    ("Baroreseptör Refleksi & Karotis Sinüsü", ["Fizyoloji", "Kardiyoloji"], ["baroreseptor refleksi", "karotis sinusu glossofaringeal", "aortik ark vagus", "ortostatik tansiyon kompanzasyonu"]),
    ("Frank-Starling Yasası & Kalp Kası", ["Fizyoloji", "Kardiyoloji"], ["frank starling", "on yuk ve atim hacmi iliskisi", "sarkomer gerilimi aktin miyozin"]),
    ("Ventilasyon-Perfüzyon (V/Q) Dengesi", ["Fizyoloji", "Göğüs Hastalıkları"], ["ventilasyon perfuzyon dengesi", "v q orani", "fizyolojik olu bosluk atelektazi sant", "apeks ve bazal perfüzyon farki"]),
    ("Oksihemoglobin Ayrışma Eğrisi (Bohr Etkisi)", ["Fizyoloji", "Hematoloji"], ["bohr etkisi", "oksihemoglobin egrisi saga kayma", "asidoz yuksek co2 yuksek sicaklik yuksek 2 3 dpg", "haldane etkisi"]),
    ("Glomerüler Filtrasyon Hızı (eGFR & Klirens)", ["Fizyoloji", "Nefroloji"], ["egfr", "inulin klirensi gercek gfr", "pah klirensi renal plazma akimi rpf", "filtrasyon fraksiyonu ff gfr rpf"]),
    ("Karşı Akım Çoğaltıcı Sistemi (Henle Kulpu)", ["Fizyoloji", "Nefroloji"], ["karsi akim cogaltici", "henle kulpu meduller hiperozmolarite", "inen kol su emilimi cikan kol tuz emilimi", "vasa recta"]),
    ("Tübüloglomerüler Geri Bildirim (TGF)", ["Fizyoloji", "Nefroloji"], ["tubuloglomeruler geri bildirim", "tgf", "makula densa adenozin salinimi afferent arteriyol vazokonstriksiyonu"]),
    ("Spermatogenez & Sertoli / Leydig Hücreleri", ["Fizyoloji", "Üroloji", "Histoloji"], ["spermatogenez", "sertoli hucreleri fsh kan testis bariyeri inhibin b", "leydig hucreleri lh testosteron salinimi"]),
    ("Oogenez & Ovulasyon Döngüsü", ["Fizyoloji", "Kadın Hastalıkları ve Doğum"], ["oogenez", "primer oosit profaz 1 de duraklar", "sekonder oosit metafaz 2 de dollenmeye kadar bekler", "lh piki ovulasyon"]),
    ("Nöromusküler Kavşak & Asetilkolin Salınımı", ["Fizyoloji", "Nöroloji"], ["noromuskuler kavsak", "voltaj kapili kalsiyum kanallari", "snare proteinleri ekzositoz", "nikotinik asetilkolin reseptoru"]),
    ("Miyastenia Gravis vs Lambert-Eaton", ["Nöroloji", "Fizyoloji"], ["miyasatena gravis postsinaptik achr yoruldukca gucsuzluk", "lambert eaton presinaptik vgcc hareketle kas gucu artar"]),
    ("Aksiyon Potansiyeli Fazları (Sinir & Kas)", ["Fizyoloji", "Nöroloji"], ["aksiyon potansiyeli", "faz 0 depolarizasyon voltaj kapili sodyum", "faz 3 repolarizasyon potasyum cikisi", "refrakter periyot mutlak ve goreceli"]),
    ("Kardiyak Pacemaker Faz 4 Depolarizasyonu", ["Fizyoloji", "Kardiyoloji"], ["pacemaker potansiyeli", "funny akim if sodyum girisi", "t tipi kalsiyum kanallari", "sinoatriyal dugum otonomisi"]),
    ("Kalsiyum Homeostazı (PTH, Kalsitonin, D Vitamini)", ["Fizyoloji", "Endokrinoloji"], ["kalsiyum dengesi", "paratiroid hormon pth osteoklast aktivasyonu distal tubul kalsiyum tutulumu", "1 25 dihidroksikolekalsiferol kalsitriol barsaktan emilim", "kalsitonin meduller tiroid kalsiyumu dusurur"]),
    ("Hipoglisemi Karşı Düzenleyici Hormonlar", ["Fizyoloji", "Endokrinoloji"], ["hipoglisemi kompanzasyonu", "glukagon", "epinefrin adrenalin", "kortizol ve buyume hormonu gh"]),
    ("Gastrik Asit Salgılama Düzenleyicileri", ["Fizyoloji", "Gastroenteroloji"], ["mide asit salgisi", "pariyetal hucre uyaricilari gastrin ccxb histamin h2 asetilkolin m3", "somatostatin ve prostaglandin e2 asit salinimini baskilar"]),
    ("Pankreatik Ekzokrin Salgı (Sekretin & CCK)", ["Fizyoloji", "Gastroenteroloji"], ["sekretin s hucreleri bikarbonat salinimi", "kolesistokinin cck i hucreleri safra kesesi kasilmasi ve asiner enzim salinimi"]),
    ("İntestinal Emilim Mekanizmaları (SGLT1, GLUT5)", ["Fizyoloji", "Gastroenteroloji"], ["sglt1 glukoz ve galaktoz sodyum bagimli", "glut5 fruktoz kolaylastirilmis difuzyon", "glut2 bazolateral kana gecis"]),
    ("Karaciğer Safra Asit Döngüsü (Enterohepatik)", ["Fizyoloji", "Gastroenteroloji"], ["enterohepatik sirkulasyon", "kolik ve kenodeoksikolik asit primer safra asitleri", "terminal ileumdan aktif geri emilim yuzde 95", "deoksikolik ve litokolik sekonder"]),
    ("Kollajen Tipleri (Tip 1, 2, 3, 4)", ["Histoloji", "Tıbbi Biyokimya"], ["kollajen tipleri", "tip 1 kemik deri tendon skar dokusu", "tip 2 kikirdak vitreus", "tip 3 retikuler lifler kan damarlari granülasyon dokusu", "tip 4 bazal membran glomerül alport"]),
    ("Elastik Lifler & Fibrillin", ["Histoloji"], ["elastik lifler", "elastin ve fibrillin mikrofibrilleri", "marfan sendromu fbn1 mutasyonu", "aort ve akciger elastikiyeti"]),
    ("Epitel Dokusu Bağlantı Kompleksleri", ["Histoloji"], ["zonula occludens tight junction okludin klaudin", "zonula adherens kadherin katenin aktin", "makula adherens desmozom desmoglein desmoplakin ara filaman pemfigus", "gap junction neksus konnekson hucreler arasi iletisim", "hemidesmozom integrin bazal lamina bullöz pemfigoid"]),
    ("Eritrosit Morfolojisi ve İnklüzyonları", ["Hematoloji", "Tıbbi Patoloji"], ["sferosit herediter sferositoz otoimmun", "sistosit parcalanmis eritrosit ttp hus dic mekanik kapak", "hedef hucre target cell talasemi hemoglobinopati", "howell jolly cisimcigi dna kalintisi splenektomi otosplenektomi", "heinz cisimcigi denature hemoglobin g6pd", "bazofilik noktalanma kursun zehirlenmesi rna", "dakriyosit gozyasi hucresi miyelofibroz"]),
    ("Nötrofil Kemotaksisi ve Ekstravazasyonu", ["Tıbbi İmmünoloji", "Tıbbi Patoloji"], ["lokosit ekstravazasyonu", "marjinasyon yuvarlanma e selektin p selektin sialil lewis x", "sikica baglanma integrin lfa 1 mac 1 icam 1 lad 1 defekti", "diyapedez transmigrasyon pecam 1 cd31", "kemotaksis c5a ltb4 il 8 bakteriyel fmlp"]),
    ("Kompleman Aktivasyon Yolları (Klasik, Lektin, Alternatif)", ["Tıbbi İmmünoloji"], ["kompleman sistemi", "klasik yol antijen antikor kompleksi igm igg c1qrs c4 c2 c3 konvertaz", "lektin yolu mannoz baglayan lektin mbl masp", "alternatif yol spontan c3 hidrolizi faktor b faktor d properdin", "terminal yol c5b c6 c7 c8 c9 membran atak kompleksi mak neisseria enfeksiyonu", "c3b opsonizasyon", "c3a ve c5a anaflatoksin"]),
    ("MHC Sınıf 1 ve Sınıf 2 Molekülleri", ["Tıbbi İmmünoloji"], ["mhc sinif 1 hla a b c tum cekirdekli hucrelerde cd8 sitotoksik t hucresine endojen antijen sunumu beta 2 mikroglobulin", "mhc sinif 2 hla dp dq dr antijen sunan hucrelerde apc makrofaj dendritik b hucresi cd4 helper t hucresine ekzojen antijen"]),
    ("T-Helper Hücre Alt Grupları (Th1, Th2, Th17, Treg)", ["Tıbbi İmmünoloji"], ["th1 ifn gama il 2 hucresel bagisiklik makrofaj aktivasyonu granülom", "th2 il 4 il 5 il 13 humoral bagisiklik ige eozinofil parazit astim", "th17 il 17 il 22 notrofilik inflamasyon mukozal bariyer", "treg il 10 tgf beta immun tolerans foxp3"]),
    ("Aşırı Duyarlılık Reaksiyonları (Gell-Coombs Tip 1-4)", ["Tıbbi İmmünoloji"], ["tip 1 asiri duyarlilik ige aracili anafilaksi astim atopik", "tip 2 asiri duyarlilik sitotoksik antikor igg igm kompleman opsonizasyon goodpasture myastenia graves", "tip 3 asiri duyarlilik immun kompleks cokmesi sle apsgn serum hastaligi vaskulit", "tip 4 asiri duyarlilik gecikmis hucresel t hucreli temas dermatiti tuberkulin ppd ms"]),

    # Tümör Belirteçleri & Laboratuvar
    ("Alfa-Fetoprotein (AFP) Belirteci", ["Tıbbi Biyokimya", "Tıbbi Onkoloji"], ["afp", "alfa fetoprotein", "hepatoselluler karsinom hcc", "yolk sac tumoru endodermal sinus", "non seminomatoz testis tm", "norol tup defekti yuksek", "down sendromu dusuk"]),
    ("Karsinoembriyonik Antijen (CEA)", ["Tıbbi Biyokimya", "Tıbbi Onkoloji"], ["cea", "karsinoembriyonik antijen", "kolorektal karsinom nuks ve tedavi takibi", "pankreas mide akciger ve meme kanserleri", "sigara icenlerde yukselebilir"]),
    ("Kanser Antijeni 125 (CA-125)", ["Tıbbi Biyokimya", "Kadın Hastalıkları ve Doğum", "Tıbbi Onkoloji"], ["ca 125", "over epitel kanseri seroz kistadenokarsinom", "endometriozis ve pelvik inflamatuar hastalikta da artabilir"]),
    ("Kanser Antijeni 19-9 (CA 19-9)", ["Tıbbi Biyokimya", "Gastroenteroloji", "Tıbbi Onkoloji"], ["ca 19 9", "pankreas adenokarsinomu ve kolanjiokarsinom belirteci", "lewis antijeni negatif kisilerde sentezlenemez"]),
    ("Kanser Antijeni 15-3 (CA 15-3)", ["Tıbbi Biyokimya", "Tıbbi Onkoloji"], ["ca 15 3", "meme kanseri nuks ve metastaz takibi"]),
    ("Prostat Spesifik Antijen (PSA)", ["Tıbbi Biyokimya", "Üroloji"], ["psa", "serbest psa total psa orani", "prostat karsinomu tarama ve izlemi", "bph ve prostatitte de artar"]),
    ("Kalsitonin & Medüller Tiroid", ["Tıbbi Biyokimya", "Endokrinoloji"], ["kalsitonin", "tiroid c hucreleri parafolikuler", "meduller tiroid karsinomu spesifik tumor belirteci ret"]),
    ("Beta-hCG Tümör Belirteci", ["Tıbbi Biyokimya", "Kadın Hastalıkları ve Doğum", "Üroloji"], ["beta hcg", "koryokarsinom trofoblastik hastalik mol hidatiform", "testis seminom ve embriyonal karsinom"]),

    # Sıvı, Elektrolit ve Asit-Baz Bozuklukları
    ("Hiponatremi Etyolojisi & Algoritması", ["Nefroloji", "Dahiliye"], ["hiponatremi sodyum 135 alti", "hipovolemik dehidratasyon kusma diuretik", "ovolemik siadh hipotiroidizm psikojenik polidipsi", "hipervolemik kalp yetmezligi siroz nefrotik sendrom", "hizli duzeltilirse santral pontin miyelinolizis"]),
    ("Hipernatremi & Su Kaybı", ["Nefroloji", "Yoğun Bakım"], ["hipernatremi sodyum 145 ustu", "asiri su kaybi diabetes insipidus susama hissi kaybi", "hizli duzeltilirse serebral odem beyin sisi"]),
    ("Hipokalemi & EKG Değişiklikleri", ["Nefroloji", "Kardiyoloji"], ["hipokalemi potasyum 3 5 alti", "u dalgasi t duzlesmesi st depresyonu", "kas gucsuzlugu kramplar paralitik ileus ventrikuler aritmiler"]),
    ("Hiperkalemi & Çadır T Dalgası", ["Nefroloji", "Kardiyoloji", "Acil Tıp"], ["hiperkalemi potasyum 5 5 ustu", "sivri cadir t dalgalari pr uzamasi qrs genislemesi p kaybi sinuzoidal dalga asistoli", "acil kalsiyum glukonat membran stabilizasyonu insulin glukoz salbutamol"]),
    ("Yüksek Anyon Açıklı Metabolik Asidoz (MUDPILES)", ["Nefroloji", "Acil Tıp"], ["anyon acigi metabolik asidoz", "mudpiles metanol uremi dka paraldehit izoniyazid laktik asidoz etilen glikol salisilat", "bikarbonat tukenimi"]),
    ("Normal Anyon Açıklı (Hiperkloremik) Metabolik Asidoz", ["Nefroloji"], ["normal anyon acikli asidoz hiperkloremik", "diyare bikarbonat kaybi", "renal tubuler asidoz rta asetazolamid"]),
    ("Klor Duyarlı vs Dirençli Metabolik Alkaloz", ["Nefroloji"], ["metabolik alkaloz", "klor duyarli idrar kloru 15 alti kusma nazogastrik aspirasyon diuretik", "klor direncli idrar kloru 20 ustu conn sendromu cushing cushing liddle"]),

    # Şok Tipleri ve Hemodinami
    ("Hipovolemik Şok & Hemorajik Evreleme", ["Acil Tıp", "Genel Cerrahi"], ["hipovolemik sok", "kanama sivi kaybi yanik", "on yuk pcwp dusuk kardiyak debi dusuk sistemik vaskuler direnc svr yuksek tasikardi soluk soguk nemli deri"]),
    ("Kardiyojenik Şok & Pompa Yetmezliği", ["Kardiyoloji", "Yoğun Bakım"], ["kardiyojenik sok", "akut miyokard enfarktusu mi aritmiler", "on yuk pcwp yuksek kardiyak debi dusuk svr yuksek"]),
    ("Septik Şok & Dağılımsal (Distrifülatif) Şok", ["Yoğun Bakım", "Enfeksiyon Hastalıkları"], ["septik sok", "dagilimsal sok vazodilatasyon", "on yuk dusuk veya normal kardiyak debi artmis svr cok dusuk sicak sok"]),
    ("Anafilaktik Şok & Epinefrin İntramüsküler", ["Acil Tıp", "Tıbbi İmmünoloji"], ["anafilaktik sok", "tip 1 asiri duyarlilik yaygin vazodilatasyon ve bronkospazm", "acil im epinefrin adrenalin uyluk on dis yuz 1 1000 lik 0 5 mg"]),
    ("Nörojenik Şok & Spinal Kord Hasarı", ["Acil Tıp", "Beyin ve Sinir Cerrahisi"], ["norojenik sok", "sempatik tonus kaybi vazomotor felc", "bradikardi ve hipotansiyon ayni anda diger soklardan ayrim sicak kuru cilt"]),

    # Pediatri Gelişim, Refleksler ve Yenidoğan
    ("Moro Refleksi & Asimetrik Moro", ["Pediatri", "Neonatoloji"], ["moro refleksi", "ani bas dususu ile k kollarin acilmasi sonra kapanmasi 4 6 ayda kaybolur", "asimetrik moro klavikula kirigi veya brakial pleksus felci"]),
    ("Yakalama (Palmar & Plantar) Refleksi", ["Pediatri"], ["palmar yakalama refleksi el ayasi 3 ayda kaybolur", "plantar yakalama ayak tabani 9 12 ayda kaybolur"]),
    ("Asimetrik Tonik Boyun Refleksi (Eskrimci)", ["Pediatri"], ["asimetrik tonik boyun refleksi", "basin cevrildigi taraftaki kol bacak ekstansiyonda karsi taraf fleksiyonda eskrimci fencer refleksi"]),
    ("APGAR Skoru & Değerlendirme", ["Pediatri", "Kadın Hastalıkları ve Doğum"], ["apgar skoru", "1 ve 5 dakikada", "appearance renk pulse nabiz kalp hizi grimace refleks tonus solunum cabasi", "7 10 normal 4 6 orta depresyon 0 3 agir asfiksi"]),
    ("Kaput Suksedaneum vs Sefal Hematom", ["Pediatri", "Neonatoloji"], ["kaput suksedaneum periost uzeri odem sutur cizgilerini asar dogumda vardir birkac gunde gecer", "sefal hematom subperiosteal kanama sutur cizgilerini ASMAZ saatler icinde belirir haftalarca surer sarilik riski"]),

    # Psikiyatri & Ruh Sağlığı
    ("Şizofreni Pozitif ve Negatif Semptomlar", ["Psikiyatri"], ["sizofreni", "pozitif semptomlar halusinasyon sanri hezeyan dezorganize konusma dopamin mezolimbik artis", "negatif semptomlar avolusyon anhedoni afekt kumeleme alozi dopamin mezokortikal azalma"]),
    ("Bipolar Afektif Bozukluk (Mani vs Hipomani)", ["Psikiyatri"], ["bipolar bozukluk", "bipolar 1 en az bir manik atak hastaneye yatis psikotik bulgu", "bipolar 2 en az bir hipomanik atak ve majör depresif atak manik atak YOKTUR"]),
    ("Obsesif Kompulsif Bozukluk (OKB) & Yolaklar", ["Psikiyatri"], ["okb", "obsesif kompulsif bozukluk", "istenmeyen yineleyici dusunceler obsesyon ve anksiyeteyi azaltmak icin yapilan rituel eylemler kompulsiyon", "kortiko striato talamo kortikal cstc yolagi", "ssri yuksek doz ve klomipramin"]),
    ("Panik Bozukluk & Agorafobi", ["Psikiyatri"], ["panik atak", "ani baslayan yogun olum ve cildirma korkusu carpinti terleme nefes darligi", "beklenti anksiyetesi", "agorafobi kacilmasi zor ortamlardan korkma"]),
    ("Travma Sonrası Stres Bozukluğu (TSSB)", ["Psikiyatri"], ["tssb", "travma sonrasi stres bozuklugu", "travmatik olayin yeniden yasanmasi flashback kabuslar kacinma davranisi asiri uyarilmislik hiperarousal", "semptomlar 1 aydan uzun surer"]),
    ("Konversiyon Bozukluğu (Fonksiyonel Nörolojik)", ["Psikiyatri", "Nöroloji"], ["konversiyon bozuklugu", "psikolojik catismanin istemli motor veya duyusal norolojik defisite donusmesi felc korluk nobet", "organik aciklama yoktur la belle indifference aldirmama"]),

    # Dermatoloji & Cilt Maligniteleri
    ("Malign Melanom & ABCD Kriterleri", ["Dermatoloji", "Tıbbi Patoloji"], ["malign melanom", "abcd kriterleri asimetri border sinir duzensizligi color renk alacaliligi diameter cap 6 mm ustu evolving degisim", "breslow derinligi en kritik prognostik faktor", "braf v600e mutasyonu vemrurafenib dabrafenib"]),
    ("Bazal Hücreli Karsinom (BCC)", ["Dermatoloji", "Tıbbi Patoloji"], ["bcc", "bazal hucreli karsinom", "en sik gorulen insan deri kanseri", "inci gibi sedefsi papul telenjiektaziler santral ulserasyon rodent ulser", "palizadik dizilim gosteren bazaloid hucreler", "lokal invaziftir metastaz cok nadirdir"]),
    ("Skuamöz Hücreli Deri Karsinomu (SCC)", ["Dermatoloji", "Tıbbi Patoloji"], ["scc", "skuamoz hucreli deri ca", "aktinik keratoz veya marjolin ulseri eski yanik skari zemininde", "keratinize pullu krutlu ulsero nodul karsinom metastaz riski bcc den yuksektir"]),
    ("Eritema Nodozum & Pannikülit", ["Dermatoloji", "Romatoloji"], ["eritema nodozum", "septal pannikulit yag dokusu iltihabi", "pretibiyal tibia onunde agrili kizarik noduller morarma ile kaybolur", "sarkoidoz tuberkuloz streptokok ibh crohn sulfonamid gebelik"]),
    ("Pitiriyazis Rozea & Madalyon Belirteci", ["Dermatoloji"], ["pitiriyazis rozea", "oncu madalyon lekesi herald patch buyuk oval eritematoz plak", "gunler sonra govdede langer cizgilerine paralel cam agaci christmas tree deseni dokuntu kendiliginden geriler"]),
    ("Akantozis Nigrikans & Malignite İlişkisi", ["Dermatoloji", "Endokrinoloji"], ["akantozis nigrikans", "boyun koltuk alti kasikta kadifemsi hiperpigmente hiperkeratotik plaklar", "benign obezite tip 2 diyabet insulin direnci", "malign gastrik adenokarsinom mide kanseri paraneoplastik"]),
    ("Ksantelazma ve Ksantom Tipleri", ["Dermatoloji", "Kardiyoloji"], ["ksantelazma goz kapagi medialinde lipid birikimi hiperkolesterolemi", "tendon ksantomu asil tendonu ailesel hiperkolesterolemi tip 2a", "eruptif ksantom kirmizi sari papuller ani belirme agir hipertrigliseridemi"]),
    ("Leser-Trélat Belirtisi", ["Dermatoloji", "Tıbbi Onkoloji"], ["leser trelat belirtisi", "cok sayida seboreik keratozun aniden patlamasi", "mide adenokarsinomu ve ic organ maligniteleri paraneoplastik"])
]

for name, discs, terms in PHARMACOPEIA_COMPOUNDS:
    EXPANSION_CONCEPTS.append((name, discs, terms))

for name, discs, terms in ADDITIONAL_CLINICAL_CONCEPTS:
    EXPANSION_CONCEPTS.append((name, discs, terms))

HIGH_YIELD_CLINICAL_EXPANSION = [
    ("Alport Sendromu & Tip IV Kollajen", ["Nefroloji", "Tıbbi Genetik"], ["alport sendromu", "tip 4 kollajen mutasyonu col4a5 x e bagli", "hematuri proteinuri ilerleyici bobrek yetmezligi", "sensorinorol isitme kaybi ve anterior lentikonus goz bulgulari", "elektron mikroskobunda bazal membranda sepet orgusu basket weave deseni"]),
    ("Goodpasture Sendromu & Anti-GBM", ["Nefroloji", "Tıbbi İmmünoloji"], ["goodpasture sendromu", "anti gbm antikorlari tip 4 kollajen alfa 3 zincirine karsi", "pulmoner hemoraji hemoptizi ve rpgn kresentik glomerulonefrit", "immunfloransanda lineer igg depolanmasi bazal membran boyunca"]),
    ("IgA Nefropatisi (Berger Hastalığı)", ["Nefroloji"], ["iga nefropatisi", "berger hastaligi", "dunyada en sik primer glomerulonefrit", "ust solunum yolu enfeksiyonu sirasinda 1 2 gun icinde senfarenjitik epizodik makroskopik hematuri", "mezanjiyal iga ve c3 depolanmasi"]),
    ("Poststreptokoksik Glomerülonefrit (APSGN)", ["Nefroloji", "Pediatri"], ["poststreptokoksik glomerulonefrit", "apsgn", "a grubu beta hemolitik streptokok faranjiti sonrasi 1 3 hafta veya impetigo sonrasi 3 6 hafta", "nefritik sendrom hematuri kola renkli idrar odem hipertansiyon c3 belirgin dusuklugu", "elektron mikroskobunda subepitelyal horgucler lumpy bumpy deseni"]),
    ("Membranöz Glomerülopati & Anti-PLA2R", ["Nefroloji"], ["membranoz nefropati", "yetiskinde nefrotik sendrom en sik sebeplerinden", "primer otoimmun anti pla2r m tipi fosfolipaz a2 reseptor antikoru", "gumusleme boyasinda subepitelyal spik ve kubbe spike and dome deseni bazal membran kalinlasmasi"]),
    ("Minimal Değişiklik Hastalığı (Nil Hastalığı)", ["Nefroloji", "Pediatri"], ["minimal degisiklik hastaligi", "nil hastaligi", "cocuklarda en sik gorulen nefrotik sendrom", "masif proteinuri hipoalbuminemi anazarka odem", "isik mikroskobu ve immunflorasan NORMALDIR", "elektron mikroskobunda podosit ayaksilarinda effasman silinme", "kortikosteroid tedavisine mukemmel yanit"]),
    ("Fokal Segmental Glomerüloskleroz (FSGS)", ["Nefroloji"], ["fokal segmental glomeruloskleroz", "fsgs", "afrika kokenlilerde ve hiv eroin obezite pam orak hucre zemininde", "steroid direnclidir son donem bobrek yetmezligine ilerler transplantasyon sonrasi yuksek nuks riski"]),
    ("Membranoproliferatif Glomerülonefrit (MPGN)", ["Nefroloji"], ["mpgn", "membranoproliferatif glomerulonefrit", "isik mikroskobunda bazal membranda tramvay rayi tram track cift kontur gorunumu", "tip 1 subendotelyal immun kompleks hepatit c kriyoglobulinemi birlikteligi", "tip 2 dens depozit hastaligi c3 nefrotik faktor c3nef alternatif kompleman aktivasyonu"]),
    ("Hızlı İlerleyen Glomerülonefrit (RPGN / Kresentik)", ["Nefroloji"], ["rpgn", "kresentik glomerulonefrit", "gunler ve haftalar icinde gfr yuzde 50 den fazla duser oliguri anuri", "biyopside bowman araliginda parietal hucre proliferasyonu ile hilal seklinde kresent olusumu fibrin"]),
    ("Buerger Hastalığı (Tromboanjiyitis Obliterans)", ["Kalp ve Damar Cerrahisi", "Romatoloji"], ["buerger hastaligi", "tromboanjiyitis obliterans", "genc sigara icen erkeklerde ekstremite kucuk ve orta capli arterlerin okluzif segmental trombozu", "parmak uclarinda sogukluk iskemi gangren kladikasyon dinlenme agrisi", "tek etkili tedavi sigaranin kesin olarak birakilmasidir"]),
    ("Dermatomiyozit & Gottron Papülleri", ["Romatoloji", "Dermatoloji"], ["dermatomiyozit", "helitrop rash goz kapaklarinda leylak rengi odem", "gottron papulleri el metakarpofalangeal eklemlerde kirmizi eritemli pullu plaklar", "sal belirtisi v belirtisi mekanik eli", "proksimal kas gucsuzlugu merdiven cikamama kollari kaldiramama", "anti jo 1 anti mi 2 antikorlari", "malignite akciger meme over mide riski artmistir"]),
    ("Polimiyozit & CD8+ T Hücre İnfiltrasyonu", ["Romatoloji", "Nöroloji"], ["polimiyozit", "deri bulgusu OLMAYAN idiyopatik inflamatuar miyopati", "kas biyopsisinde endomizyal cd8 sitotoksik t lenfosit infiltrasyonu", "dermatomiyozitte ise perimizyal cd4 t ve b hucre perivaskuler"]),
    ("Polimiyaljiya Romatika (PMR)", ["Romatoloji"], ["polimiyalji romatika", "pmr", "50 yas ustu sabah tutuklugu omuz ve kalca pelvik kusaminda bilateral siddetli kas agrisi ve sertlik kas gucsuzlugu YOKTUR", "sedimentasyon ve crp cok yuksektir", "temporal dev hucreli arterit ile sik birliktelik", "dusuk doz prednizolona dramatik yanit"]),
    ("Sjögren Sendromu (Anti-SSA / Anti-SSB)", ["Romatoloji", "Göz Hastalıkları"], ["sjogren sendromu", "otoimmun ekzokrin bez lenfositik yikimi", "kserostomi agiz kurulugu ve keratokonjunktivitis sikka goz kurulugu", "schirmer testi goz yasi uretimi olcumu", "anti ro ssa ve anti la ssb antikorlari", "parotis bezi buyumesi bilateral", "b hucreli non hodgkin malt lenfoma gelisme riski 40 kat artmistir"]),
    ("Sistemik Skleroz & Skleroderma (Anti-Scl70 / Sentromer)", ["Romatoloji"], ["sistemik skleroz", "skleroderma", "yaygin fibrozis ve mikrovaskuler hasar", "diffuz kutanoz anti topoizomeraz 1 anti scl 70 erken donemde akciger interstisyel fibrozisi ve skleroderma renal krizi ace inhibitoru tedavisi", "sinirli kutanoz crest sendromu kalsinozis raynaud ozofagus dismotilitesi sklerodaktili telenjiektazi anti sentromer antikoru pulmoner arteriyel hipertansiyon"]),
    ("Mikst Bağ Dokusu Hastalığı (Anti-U1 RNP)", ["Romatoloji"], ["mikst bag dokusu hastaligi", "mctd", "sle sistemik skleroz ve polimiyozit bulgularinin bir arada bulunmasi sosis parmak raynaud", "yuksek titrede anti u1 rnp antikoru spesifiktir"]),
    ("Antifosfolipid Antikor Sendromu (APS)", ["Romatoloji", "Hematoloji"], ["antifosfolipid sendromu", "aps", "arteriyel ve venoz tekrarlayan trombozlar derin ven trombozu inme", "tekrarlayan fetal kayiplar dusukler", "laboratuvarda lupus antikoagulan anti kardiyolipin igg igm anti beta 2 glikoprotein 1 antikorlari", "in vitro aptt uzar ancak klinik olarak tromboza egilim vardir"]),
    ("Zollinger-Ellison Sendromu & Gastrinoma", ["Gastroenteroloji", "Endokrinoloji"], ["zollinger ellison sendromu", "gastrinoma", "pankreas veya duodenumda gastrin salgilayan noroendokrin tumor", "atipik lokalizasyonlu jejunum direncli ve tekrarlayan peptik ulserler", "asiri asit salinimi sekretin stimülasyon testi ile paradoksal gastrin artisi", "men 1 birlikteligi yuzde 25"]),
    ("VIPoma (WDHA Sendromu / Verner-Morrison)", ["Gastroenteroloji", "Endokrinoloji"], ["vipoma", "verner morrison sendromu", "wdha sendromu watery diarrhea hypokalemia achlorhydria", "bol sulu sekretuar diyare aclikla durmaz hipokalemi ve hipoklorhidri"]),
    ("Glukagonoma & Nekrolitik Gezici Eritem", ["Endokrinoloji", "Dermatoloji"], ["glukagonoma", "pankreas alfa hucre tumoru", "nekrolitik gezici eritem nekrolitik migratuar eritem tipik kizarik kabarcikli cild lezyonlari", "hafif diyabet hiperglisemi kilo kaybi anemi venoz tromboz"]),
    ("Karsinoid Tümör & 5-HIAA", ["Tıbbi Onkoloji", "Gastroenteroloji"], ["karsinoid tumor", "terminal ileum ve apendikste en sik noroendokrin tumor", "karsinoid sendrom kizarma flushing sulu diyare bronkospazm sag kalp kapak lezyonlari trikuspid yetmezligi", "karaciger metastazi sonrasi sistemik bulgular ortaya cikar", "24 saatlik idrarda 5 hiaa hidroksi indolasetik asit artisi"]),
    ("Akalazya & Kuş Gagası Görünümü", ["Gastroenteroloji", "Genel Cerrahi"], ["akalazya", "ozofagus myenterik pleksus auerbach postgangliyonik noron kaybi nitrik oksit vip salinimi yetersizligi", "alt ozofagus sfinkteri les gevseyemez peristaltizm kaybolur", "katilara ve sivilara karsi ayni anda disfaji", "baryumlu ozofagus grafisinde kus gagasi bird beak gorunumu"]),
    ("Diffüz Özofageal Spazm & Tirbüşon Özofagus", ["Gastroenteroloji"], ["diffuz ozofageal spazm", "esofageal spazm", "simultane yuksek genlikli ve tekrarlayan kasilmalar non peristaltik", "angina benzeri gogus agrisi ve disfaji", "baryumlu grafide tirbuson corkscrew gorunumu"]),
    ("Zenker Divertikülü & Killian Üçgeni", ["Genel Cerrahi", "KBB"], ["zenker divertikulu", "m constrictor pharyngis inferior ve m cricopharyngeus arasindaki zayif nokta killian ucgeni", "pulsion tipi yalanci psodo divertikul", "halitozis agiz kokusu yutma guclugu regurgitasyon aspirasyon pnomonisi"]),
    ("Plummer-Vinson Sendromu & Özofagus Ağı", ["Gastroenteroloji", "Hematoloji"], ["plummer vinson sendromu", "paterson kelly", "triad 1 demir eksikligi anemisi 2 postkrikoid servikal ozofagus agi web 3 disfaji", "skuamoz hucreli ozofagus karsinomu riski artmistir"]),
    ("Mallory-Weiss Yırtığı & Alkolik Kusma", ["Gastroenteroloji", "Acil Tıp"], ["mallory weiss sendromu", "kronik alkol alimi veya siddetli ogurme kusma sonrasi gastroozofageal bileskede mukoza ve submukozayi tutan longitüdinal yirtik", "agrisiz hematemez endoskopide gorulur kendiliginden durur"]),
    ("Boerhaave Sendromu & Özofagus Rüptürü", ["Genel Cerrahi", "Acil Tıp"], ["boerhaave sendromu", "siddetli kusma sonrasi ozofagus alt sol 1 3 te transmural tam kat spontan ruptur yirtilma", "mackler triadi kusma siddetli gogus agrisi cilt alti amfizem cerrahi acildir"]),
    ("Meckel Divertikülü & Ektopik Gastrik Mukoza", ["Pediatri", "Çocuk Cerrahisi"], ["meckel divertikulu", "omfalomezenterik duktus vitellin kanal kapanma defekti kalintisi", "2ler kurali nufusun yuzde 2si 2 yas alti 2 inc uzunluk ileocokal kapaga 2 fit mesafe 2 tip ektopik mukoza gastrik ve pankreatik", "agrisiz rektal kanama tech99 perteknetat sintigrafisi"]),
    ("Hirschsprung Hastalığı & Aganglionik Megakolon", ["Çocuk Cerrahisi", "Pediatri"], ["hirschsprung hastaligi", "konjenital aganglionik megakolon noral krest hucrelerinin distale goc edememesi", "auerbach ve meissner pleksuslarinda ganglion hucresi yoklugu", "yenidoganda ilk 48 saatte mekonyum cikaramama karin sisligi safrali kusma", "rektal aspirasyon biyopsisi ile kesin tani"]),
    ("İnvajinasyon (İntussusepsiyon) & Çilek Jölesi Dışkı", ["Pediatri", "Çocuk Cerrahisi"], ["invajinasyon", "barsagin kendi icine teleskop gibi gecmesi en sik ileokolik", "bebekte epizodik siddetli kramp tarzinda karin agrisi bacaklarini kaye cekme", "sag ust kadranda sosis kitle sausage mass", "cilek jolesi rektal kanama red currant jelly stool", "ultrasonda hedef hedef tahtasi target sign gorunumu"]),
    ("Duodenal Atrezi & Çift Kabarcık (Double Bubble)", ["Pediatri", "Radyoloji"], ["duodenal atrezi", "duodenum rekanalisasyon defekti down sendromu ile cok guclu birliktelik", "direkt rontgende midede ve duodenum ilk kisminda gaz cift kabarcik double bubble belirtisi", "safrali kusma ve polihidramniyos"]),
    ("Hipertrofik Pilor Stenozu & Zeytin Belirtisi", ["Pediatri", "Çocuk Cerrahisi"], ["hipertrofik pilor stenozu", "hps", "ilk erkek cocukta 2 6 haftada baslayan safrasiz fiskirir tarzda projectile kusma", "sag hipokondriumda zeytin olive kitle palpasyonu", "hipokloremik hipokalemik metabolik alkaloz"]),
    ("Kistik Fibrozis & CFTR Gen Mutasyonu", ["Pediatri", "Göğüs Hastalıkları"], ["kistik fibrozis", "otozomal resesif cftr geni delta f508 klor kanali mutasyonu", "ter testi klor 60 mEq L uzeri kesin tani", "mekonyum ileusu tekrarlayan psodomonas enfeksiyonlari bronsektazi pankreatik yetmezlik yag malabsorpsiyonu"]),
    ("Kartagener Sendromu & Primer Siliyer Diskinezi", ["Göğüs Hastalıkları", "Tıbbi Genetik"], ["kartagener sendromu", "primer siliyer diskinezi dinein kolu eksikligi", "triad 1 situs inversus totalis dekstrokardi 2 bronsektazi 3 kronik sinuzit", "erkeklerde sperm motilite kaybi infertilite kadinlarda dis gebelik"]),
    ("Alfa-1 Antitripsin Eksikliği & Panasiner Amfizem", ["Göğüs Hastalıkları", "Gastroenteroloji"], ["alfa 1 antitripsin eksikligi", "aat", "serpin proteaz inhibitoru eksikligi pizz fenotipi", "genc yas sigara icmeyenlerde alt loblari tutan panasiner amfizem", "karacigerde pas pozitif diastaz direncli globuller hepatit ve siroz"]),
    ("Sarkoidoz & Nonkazeifiye Granülomlar", ["Göğüs Hastalıkları", "Romatoloji"], ["sarkoidoz", "etiyolojisi bilinmeyen sistemik nonkazeifiye epitelioid granülomatöz hastalik", "akciger grafisinde bilateral hiler lenfadenopati bhla", "yüksek ace angiyotensin donusturucu enzim ve hiperkalsemi 1 alfa hidroksilaz aktivitesi", "lofgren sendromu ates eritema nodozum bilateral hiler lap artrit"]),
    ("Guillain-Barré Sendromu & Albüminositolojik Disosiasyon", ["Nöroloji"], ["guillain barre sendromu", "gbs", "akut inflamatuar demiyelinizan polinöropati aidp", "campylobacter jejuni veya cmv enfeksiyonu sonrasi", "simetrik asendan yukselen felc arefleksi derin tendon refleksleri kaybi", "bos incelemesinde protein belirgin artmis hucre sayisi normaldir albumino sitolojik disosiasyon"]),
    ("Multiple Skleroz & Oligoklonal Bantlar", ["Nöroloji"], ["multiple skleroz", "ms", "santral sinir sistemi otoimmun demiyelinizan plaklar relapsing remitting", "lhermitte belirtisi boyun fleksiyonunda omurilikten asagi elektrik carpma hissi", "uhthoff fenomeni sicak banyo ile semptomlarin kotulesmesi", "bos ta oligoklonal igg bantlari pozitifligi ve mrg de periventrikuler plaklar dawson parmaklari"]),
    ("Amyotrofik Lateral Skleroz (ALS) & Motor Nöron", ["Nöroloji"], ["als", "amyotrofik lateral skleroz", "ust ve alt motor noronlarin ayni anda tutuldugu dejeneratif hastalik", "fasikulasyonlar asimetrik kas erimesi ve ayni zamanda hiperrefleksi spastisite babinski pozitifligi", "duyu kusuru ve goz hareketleri korunur sod1 mutasyonu riluzol tedavisi"]),
    ("Huntington Hastalığı & CAG Tekrarları", ["Nöroloji", "Tıbbi Genetik"], ["huntington hastaligi", "otozomal dominant trinukleotid tekrar hastaligi c a g tekrari antisipasyon", "korpus striatum nukleus kaudatus ve putamende gaba erjik noronlarin yikimi", "koreik hareketler demans ve psikiyatrik degisiklikler"]),
    ("Wilson Hastalığı & Kayser-Fleischer Halkası", ["Gastroenteroloji", "Nöroloji"], ["wilson hastaligi", "hepatolentikuler dejenerasyon atp7b mutasyonu", "bakir atilim bozuklugu seruloplazmin dusuklugu 24 saatlik idrar bakiri artisi", "korneada kayser fleischer halkasi bazal ganglion tutulumu asteriksis ve siroz"]),
    ("Hemokromatozis & Bronz Diyabet", ["Gastroenteroloji", "Hematoloji"], ["hemokromatozis", "hfe gen c282y mutasyonu asiri demir emilimi", "ferritin ve transferrin saturasyonu belirgin yuksek", "triad 1 siroz mikronoduler 2 bronz hiperpigmentasyon 3 diabetes mellitus bronz diyabet"]),
    ("Gilbert Sendromu & UGT1A1 Azalması", ["Gastroenteroloji"], ["gilbert sendromu", "ugt1a1 enzim aktivitesinde yuzde 70 azalma", "stres aclik enfeksiyon veya agir egzersiz sonrasi hafif indirekt ankonjuge hiperbilirubinemi", "hemoliz ve karaciger enzim yuksekligi yoktur selim durumdur"]),
    ("Primer Biliyer Kolanjit (PBC) & Anti-Mitokondriyal Antikor (AMA)", ["Gastroenteroloji"], ["primer biliyer kolanjit", "pbc", "orta yas kadinlarda kucuk intrahepatik safra kanallarinin otoimmun granülomatöz yikimi", "kasinti kasinma ve yorgunluk en erken bulgular alkalen fosfataz alp belirgin yuksek", "anti mitokondriyal antikor ama pozitifligi spesifiktir"]),
    ("Primer Sklerozan Kolanjit (PSC) & Ülseratif Kolit", ["Gastroenteroloji"], ["primer sklerozan kolanjit", "psc", "intra ve ekstrahepatik safra kanallarinin fibrozisi boncuk tespih gorunumu ercp de", "yuzde 70 ulseratif kolit ibh ile birliktedir", "p anca pozitifligi ve kolanjiokarsinom riski belirgin artmistir"]),
    ("Trombotik Trombositopenik Purpura (TTP) & ADAMTS13", ["Hematoloji", "Nefroloji"], ["ttp", "trombotik trombositopenik purpura", "adamts13 von willebrand carpan metaloproteaz eksikligi veya antikoru ultra buyuk vwf multimerleri", "pentad 1 mikrositopatik hemolitik anemi sistositler 2 trombositopeni purpura 3 norolojik bulgular dalgalanan suur 4 ates 5 bobrek yetmezligi", "pt ve aptt normaldir acil plazmaferez plazma degisimi"]),
    ("Hemolitik Üremik Sendrom (HÜS) & Shiga Toksin", ["Pediatri", "Nefroloji"], ["hemolitik uremik sendrom", "hus", "e coli o157 h7 shiga benzeri toksin kanli ishal sonrasi", "triad 1 mikroanjiyopatik hemolitik anemi sistositler 2 trombositopeni 3 akut bobrek yetmezligi oliguri"]),
    ("Kronik Miyelositer Lösemi (KML) & BCR-ABL (t(9;22))", ["Hematoloji", "Tıbbi Genetik"], ["kml", "kronik miyeloid losemi", "filadelfiya kromozomu t 9 22 bcr abl fuzyon geni tirozin kinaz artisi", "asiri lokositoz basofili sola kayma lokosit alkalen fosfataz lap skoru cok dusuktur", "imatinib bcr abl kinaz inhibitoru"]),
    ("Akut Promiyelositer Lösemi (APL) & t(15;17) PML-RARA", ["Hematoloji"], ["apl", "akut promiyelositer losemi aml m3", "t 15 17 pml rara retinoik asit reseptor translokasyonu", "auer comaklari iceren atipik promiyelositler faggot cells", "cok yuksek dic yaygin damar ici pihtilasma riski", "atra all trans retinoik asit ve arsenik trioksit tedavisi"]),
    ("Hodgkin Lenfoma & Reed-Sternberg Hücreleri (CD15 / CD30)", ["Hematoloji", "Tıbbi Patoloji"], ["hodgkin lenfoma", "reed sternberg baykus gozu dev cift cekirdekli hucreler", "cd15 ve cd30 pozitif cd20 ve cd45 negatif", "noduler sklerozan tip en sik gorulen kadinlarda mediastinal kitle", "b semptomlari ates pel ebstein gece terlemesi kilo kaybi alkolle lenf nodu agrisi"]),
    ("Burkitt Lenfoma & t(8;14) c-myc (Yıldızlı Gökyüzü)", ["Hematoloji", "Tıbbi Patoloji"], ["burkitt lenfoma", "t 8 14 c myc asin onkogen translokasyonu en hizli cogalan insan tumoru", "biyopside yildizli gokyuzu starry sky deseni makrofajlar", "endemik afrika ebv iliskili cene mandibula kitlesi sporadik bati batin cekal kitle"]),
    ("Multipl Miyelom & CRAB Kriterleri / Bence Jones Proteini", ["Hematoloji", "Nefroloji"], ["multipl miyelom", "klonal plazma hucre proliferasyonu kemik iliginde yuzde 10 uzeri", "crab kriterleri calcium hiperkalsemi renal bobrek yetmezligi casts anemia yorgunluk bone zimba deligi litik kemik lezyonlari", "serum protein elektroforezinde m banti spike igg veya iga", "idrarda bence jones proteini serbest hafif zincir"]),
    ("Digoksin Toksisitesi & Sarı-Yeşil Görme (Ksantopsi)", ["Farmakoloji", "Kardiyoloji"], ["digoksin zehirlenmesi", "sodyum potasyum atpaz inhibisyonu pozitif inotrop negatif kronotrop", "istahsizlik bulanti kusma gorme bozukluklari sari yesil gorme ksantopsi halo gorme", "en sik aritmi ventrikuler bigemini en spesifik aritmi av bloklu tasikardi", "hipokalemi toksisiteyi belirgin artirir digibind antikor"]),
    ("Nöroleptik Malign Sendrom & Dantrolen", ["Farmakoloji", "Psikiyatri"], ["noroleptik malign sendrom", "nms", "antipsikotik dopamin d2 reseptor blokajina bagli", "tetrad kursun boru rijiditesi kursun boru kursun dokumu kas sertligi yuksek ates hiperpireksi otonomik instabilite tasikardi terleme dalgalanan suur", "kreatin kinaz ck asiri yuksek laktik asidoz", "dantrolen ryanodin blokoru ve bromokriptin dopamin agonisti tedavisi"]),
    ("Serotonin Sendromu & Klonus / Hiperrefleksi / Siproheptadin", ["Farmakoloji", "Psikiyatri"], ["serotonin sendromu", "ssri maoi tca linezolid tramadol gibi serotonerjik ilac kombinasyonlari", "klonus miyoklonus ve hiperrefleksi nms den ayrim titreme hipertermi terleme midriyazis ajitasyon", "siproheptadin 5 ht2a antagonisti tedavisi"]),
    ("Malign Hipertermi & Ryanodin Reseptör Mutasyonu", ["Anesteziyoloji ve Reanimasyon"], ["malign hipertermi", "genetik ryr1 ryanodin kalsiyum salinim kanali mutasyonu", "inhalasyon anestezikleri halotan izofluran veya suksinilkolin ile tetiklenir", "ani asiri hipertermi karsi konulamaz masseter kas spazmi cene kilitlenmesi rabdomiyoliz", "tedavide acil iv dantrolen sodyum"]),
    ("Vankomisin & Kırmızı Adam Sendromu", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["vankomisin", "glikopeptid antibiyotik hucre duvari d ala d ala baglanmasi", "mrsa ve c difficile enterokoliti", "hizli infuzyonda histamin salinimi kirmizi adam sendromu red man", "nefrotoksisite ve ototoksisite"]),
    ("Aminoglikozidler (Gentamisin, Amikasin)", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["aminoglikozid", "gentamisin", "amikasin", "tobramisin", "30s ribozomal alt birim baglanmasi konsantrasyona bagli bakterisit", "ototoksisite vestibuler ve koklear kalici hasar", "nefrotoksisite akut tubuler nekroz atn"]),
    ("Amfoterisin B & Lipozomal Form", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["amfoterisin b", "polien grubu sistemik antifungaller ergosterole baglanarak por acar", "infuzyon reaksiyonu ates titreme sarsinti shake and bake", "agir nefrotoksisite hipokalemi ve hipomagnezemi"]),
    ("Florokinolonlar (Siprofloksasin, Levofloksasin)", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["florokinolon", "siprofloksasin", "levofloksasin", "moksifloksasin", "dna giraz topoizomeraz 2 ve topoizomeraz 4 inhibisyonu", "asil tendon rüptürü ve tendinit riski", "qt araligi uzamasi", "kikirdak hasari riski nedeniyle gebelerde ve 18 yas altinda kisitli kullanim"]),
    ("Makrolidler (Azitromisin, Klaritromisin)", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["makrolid", "azitromisin", "klaritromisin", "eritromisin", "50s ribozom translokasyon inhibisyonu", "motilin reseptor agonizmi kramp ve diyare", "qt uzamasi torsades de pointes", "sitokrom p450 cyp3a4 enzim inhibisyonu azitromisin haric"]),
    ("Tetrasiklinler (Doksisiklin, Minosiklin)", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["tetrasiklin", "doksisiklin", "minosiklin", "30s ribozom aminoacil trna baglanmasini engeller", "kalsiyum magnezyum demir ile selasyon olusturur sutle alinmaz", "dis minesi hipoplazisi ve dislerde kalici sari kahverengi renk degisikligi kemik buyumesi duraklamasi", "fototoksisite gunes yanigi"]),
    ("Kloramfenikol & Gri Bebek Sendromu", ["Farmakoloji", "Pediatri"], ["kloramfenikol", "50s peptidil transferaz enzim inhibisyonu", "glukuronil transferaz enzim yetersizligi olan yenidoganda gri bebek sendromu gray baby hipotansiyon siyanoz kolaps", "dozdan bagimsiz idiyosenkratik geri donussuz aplastik anemi"]),
    ("Sülfonamidler & Trimetoprim (TMP-SMX)", ["Farmakoloji", "Enfeksiyon Hastalıkları"], ["sulfametoksazol", "trimetoprim", "bactrim", "dihidropteroat sentaz ve dihidrofolat reduktaz ardil inhibisyonu folat sentezi engeli", "pneumocystis jirovecii pcp pnomonisi profilaksi ve tedavisi", "yenidoganda bilirubini albuminden ayirarak kernikterus", "stevens johnson sendromu ve hemoliz g6pd eksikliginde"]),
    ("Tüberküloz İlaçları & İNH, RİF, EMB, PZA", ["Farmakoloji", "Göğüs Hastalıkları"], ["izoniyazid inh mikolik asit sentez inhibisyonu piridoksin b6 eksikligi periferik noropati hepatotoksisite", "rifampisin dna bagimli rna polimeraz inhibisyonu idrar ve gozyasini kirmizi turuncuya boyar guclu cyp induktoru", "etambutol arabinozil transferaz inhibisyonu optik norit kirmizi yesil korlugu", "pirazinamid hiperurisemi gut atagi"]),
    ("Antiepileptikler (Fenitoin, Karbamazepin, Valproat)", ["Farmakoloji", "Nöroloji"], ["fenitoin voltaj kapili sodyum kanal blokoru sifirinci derece kinetik dis eti hiperplazisi hirsutizm teratojen hidantoin", "karbamazepin trigeminal nevralji ilk tercih hla b 1502 sjs lökopeni hiponatremi siadh", "valproik asit genis spektrumlu gaba artisi hepatotoksisite pankreatit spina bifida noral tup defekti kilo alimi tremor"]),
    ("Lityum Karbonat & Yan Etkileri", ["Farmakoloji", "Psikiyatri"], ["lityum", "bipolar afektif bozukluk duygu durum dengeleyici", "dar terapötik aralik 0 6 1 2 mEq L", "ince el tremoru hipotiroidizm tiroid bezi buyumesi nefrojenik diabetes insipidus adh direnci", "teratojen ebstein anomalisi trikuspid kapagin sag ventrikule yapismasi"]),
    ("Klozapin & Agranülositoz", ["Farmakoloji", "Psikiyatri"], ["klozapin", "tedaviye direncli sizofrenide altin standart atipik antipsikotik intihar riskini azaltan tek ilac", "ekstrapiramidal yan etki yok denecek kadar azdir hiperprolaktinemi yapmaz", "ölümcül agranulositoz riski duzenli tam kan sayimi mutlak notrofil takibi zorunludur", "miyokardit ve nobet esigini dusurme"]),
    ("Metformin & Biguanidler", ["Farmakoloji", "Endokrinoloji"], ["metformin", "glukofaj", "ampk adenozin monofosfatla aktive olan protein kinaz aktivasyonu", "karacigerde glukoneogenezi baskilar periferik insulin duyarliligini artirir", "hipoglisemi YAPMAZ kilo verdirir", "en korkulan komplikasyon laktik asidozdur gfr 30 alti kontrendikedir iv kontrast madde oncesi kesilmelidir"]),
    ("SGLT-2 İnhibitörleri (Gliflozinler)", ["Farmakoloji", "Endokrinoloji", "Kardiyoloji"], ["sglt 2 inhibitorleri", "dapagliflozin", "empagliflozin", "kanagliflozin", "proksimal tubulde glukoz ve sodyum geri emilimini bloke eder glukozuri", "kalp yetmezligi ve kronik bobrek yetmezliginde mortaliteyi belirgin azaltir kardiyorenal koruma", "yan etki mikotik genital enfeksiyonlar ve oglu glisemik diyabetik ketoasidoz"]),
    ("GLP-1 Reseptör Agonistleri (İncretin Mimetikler)", ["Farmakoloji", "Endokrinoloji"], ["glp 1 agonistleri", "liraglutid", "semaglutid", "dulaglutid", "glukoza bagimli insulin salinimini artirir glukagonu baskilar gastrik bosalmayi geciktirir santral istahi keser belirgin kilo kaybi", "yan etki bulanti kusma gastroparez pankreatit ve tiroid c hucre tumoru meduller ca uyarisi"]),
    ("Warfarin & K Vitamini Epoksit Redüktaz", ["Farmakoloji", "Hematoloji"], ["warfarin", "kumadin", "k vitamini epoksit reduktaz vkorc1 enzim inhibisyonu", "faktor 2 7 9 10 ve antikoagulan protein c ve protein s sentezini bozar", "inr ile monitorize edilir hedef inr 2 3 mekanik kapakta 2 5 3 5", "tedavinin ilk gunlerinde protein c nin kisa yari omru nedeniyle gecici hiperkoagülabilite ve warfarin deri nekrozu olusabilir heparinle koprulama yapilir", "antidotu k vitamini fitonadion ve agir kanamada protrombin kompleks konsantresi pcc veya tdp dir"])
]

for name, discs, terms in HIGH_YIELD_CLINICAL_EXPANSION:
    EXPANSION_CONCEPTS.append((name, discs, terms))


