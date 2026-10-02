#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_medical_glossary.py
Comprehensive medical glossary database generator for Dönem 3 Kurul 1:
Contains 85+ Latin medical terms, bacteria, viruses, drugs, genetics, urology, and pathology terms.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

GLOSSARY_PATH = os.path.join('src', 'data', 'medical_glossary.json')

GLOSSARY_TERMS = [
    # ==================== BAKTERİYOLOJİ ====================
    {
        "term": "Staphylococcus aureus",
        "aliases": ["staphylococcus aureus", "s. aureus", "stafilokok aureus", "altın sarısı stafilokok"],
        "category": "Bakteriyoloji",
        "pronunciation": "[staf-i-lo-kok-kus au-re-us]",
        "definition": "Gram pozitif, katalaz ve koagülaz pozitif küme oluşturan kok. Deri ve yumuşak doku enfeksiyonları, apseler, osteomiyelit ve nozokomiyal bakteriyeminin baş etkenidir.",
        "clinicalPearls": "Sağlıklı toplumda burun mukozasında %20-30 oranında asemptomatik kolonize olur.",
        "badgeColor": "amber"
    },
    {
        "term": "MRSA (Metisiline Dirençli S. aureus)",
        "aliases": ["mrsa", "metisiline dirençli staphylococcus aureus", "metisilin dirençli"],
        "category": "Bakteriyoloji",
        "pronunciation": "[m-r-s-a]",
        "definition": "mecA geni aracılığıyla PBP2a sentezleyerek tüm standart beta-laktam antibiyotiklere direnç kazanmış S. aureus suşları.",
        "clinicalPearls": "Hastanede mutlaka TEMAS İZOLASYONU (Kırmızı Yıldız) gerektirir; tedavide vankomisin veya daptomisin seçilir.",
        "badgeColor": "red"
    },
    {
        "term": "Clostridioides difficile",
        "aliases": ["clostridioides difficile", "c. difficile", "clostridium difficile"],
        "category": "Bakteriyoloji",
        "pronunciation": "[klos-tri-di-oy-des dif-fi-si-le]",
        "definition": "Gram pozitif, anaerop, sporlu çomak. Geniş spektrumlu antibiyotik sonrası normal floranın bozulmasıyla psödomembranöz kolit tablosu oluşturur.",
        "clinicalPearls": "Sporları alkol bazlı jellerle ölmez! Temas sonrası eller MUTLAKA su ve sabunla yıkanmalıdır.",
        "badgeColor": "red"
    },
    {
        "term": "Mycobacterium tuberculosis",
        "aliases": ["mycobacterium tuberculosis", "m. tuberculosis", "tüberküloz basili", "koch basili"],
        "category": "Bakteriyoloji",
        "pronunciation": "[mi-ko-bak-te-ri-yum tü-ber-kü-lo-zis]",
        "definition": "Aside dirençli (ARB / Ehrlich-Ziehl-Neelsen pozitif), hücre duvarında yüksek oranda mikolik asit içeren zorunlu aerop basil. Akciğer tüberkülozunun etkenidir.",
        "clinicalPearls": "Solunum yoluyla (<5 µm aerosol) bulaşır; hastanede NEGATİF BASINÇLI ODA ve N95 MASKE (Sarı Yaprak) şarttır.",
        "badgeColor": "purple"
    },
    {
        "term": "Neisseria meningitidis",
        "aliases": ["neisseria meningitidis", "n. meningitidis", "meningokok"],
        "category": "Bakteriyoloji",
        "pronunciation": "[nay-se-ri-ya me-nin-ji-ti-dis]",
        "definition": "Gram negatif kahve çekirdeği şeklinde diplokok. Farenksten kan dolaşımına geçerek fulminan meningokoksemi ve pürülan menenjit yapar.",
        "clinicalPearls": "DAMLACIK İZOLASYONU (Mavi Çiçek) gerektirir; 1 metreden yakın mesafede cerrahi maske takılır; yakın temaslılara rifampisin kemoprofilaksisi verilir.",
        "badgeColor": "blue"
    },
    {
        "term": "Pseudomonas aeruginosa",
        "aliases": ["pseudomonas aeruginosa", "p. aeruginosa", "psödomonas"],
        "category": "Bakteriyoloji",
        "pronunciation": "[psö-do-mo-nas e-ru-ji-no-za]",
        "definition": "Gram negatif, oksidaz pozitif, yeşil-mavi piyosiyanin pigmenti üreten firsatçı basil. Nemli ortamları sever.",
        "clinicalPearls": "Ventilatör ilişkili pnömoni ve yanık yarası enfeksiyonlarının ölümcül nozokomiyal etkenidir.",
        "badgeColor": "teal"
    },
    {
        "term": "Acinetobacter baumannii",
        "aliases": ["acinetobacter baumannii", "a. baumannii", "asinetobakter"],
        "category": "Bakteriyoloji",
        "pronunciation": "[a-si-ne-to-bak-ter bau-man-ni]",
        "definition": "Gram negatif kokobasil; cansız hastane yüzeylerinde ve tıbbi cihazlarda aylarca canlı kalabilen, çoğul ilaç dirençli (MDR) fırsatçı hastane patojeni.",
        "clinicalPearls": "Yoğun bakımlarda salgın yapar; Temas İzolasyonu (Kırmızı Yıldız) zorunludur.",
        "badgeColor": "red"
    },
    {
        "term": "VRE (Vankomisine Dirençli Enterokok)",
        "aliases": ["vre", "vankomisine dirençli enterokok", "vancomycin-resistant enterococcus"],
        "category": "Bakteriyoloji",
        "pronunciation": "[v-r-e]",
        "definition": "vanA veya vanB genleri aracılığıyla hücre duvarı hedef peptidi D-Ala-D-Ala yerine D-Ala-D-Laktat sentezleyerek glikopeptidlere direnç kazanan Enterococcus faecium suşları.",
        "clinicalPearls": "Hastanelerde Temas İzolasyonu ile sınırlandırılır; tedavide linezolid tercih edilir.",
        "badgeColor": "red"
    },
    {
        "term": "Mycoplasma pneumoniae",
        "aliases": ["mycoplasma pneumoniae", "m. pneumoniae", "mikoplazma"],
        "category": "Bakteriyoloji",
        "pronunciation": "[mi-ko-plaz-ma pnö-mo-ni-ye]",
        "definition": "Hücre duvarı kesinlikle bulunmayan en küçük bağımsız çoğalan bakteri. Membranında kolesterol içerir.",
        "clinicalPearls": "Hücre duvarı olmadığından beta-laktam antibiyotiklere (penisilin/sefalosporin) DOĞAL DİRENÇLİDİR; atipik pnömoni yapar.",
        "badgeColor": "indigo"
    },
    {
        "term": "Chlamydia trachomatis",
        "aliases": ["chlamydia trachomatis", "c. trachomatis", "klamidya"],
        "category": "Bakteriyoloji",
        "pronunciation": "[kla-mi-di-ya tra-ko-ma-tis]",
        "definition": "ATP sentezleyemeyen ve konağın enerjisine muhtaç olan (enerji paraziti) zorunlu hücre içi bakteri.",
        "clinicalPearls": "Cinsel yolla bulaşan non-gonokoksik üretrit, PID ve trahomun etkenidir.",
        "badgeColor": "purple"
    },
    {
        "term": "Escherichia coli",
        "aliases": ["escherichia coli", "e. coli"],
        "category": "Bakteriyoloji",
        "pronunciation": "[e-şe-ri-şi-ya ko-li]",
        "definition": "Gram negatif, laktoz pozitif fakültatif anaerop basil. Bağırsak mikrobiyotasının normal üyesidir.",
        "clinicalPearls": "Pili (fimbria) aracılığıyla üroepitele tutunarak toplum kaynaklı üriner sistem enfeksiyonlarının %80'inden fazlasından sorumludur.",
        "badgeColor": "blue"
    },
    {
        "term": "Proteus mirabilis",
        "aliases": ["proteus mirabilis", "proteus"],
        "category": "Bakteriyoloji",
        "pronunciation": "[pro-te-us mi-ra-bi-lis]",
        "definition": "Besiyerinde dalgalanma (swarming) hareketi yapan ve güçlü ÜREAZ enzimi üreten Gram negatif basil.",
        "clinicalPearls": "Üreyi amonyak ve CO2'ye yıkarak idrar pH'sını alkali yapar; Magnezyum Amonyum Fosfat (Strüvit / Staghorn / Geyik boynuzu) taşlarının birincil etkenidir.",
        "badgeColor": "amber"
    },

    # ==================== VİROLOJİ ====================
    {
        "term": "SARS-CoV-2",
        "aliases": ["sars-cov-2", "covid-19", "koronavirüs", "coronavirus"],
        "category": "Viroloji",
        "pronunciation": "[sars-kov-iki]",
        "definition": "Zarflı, pozitif polariteli tek zincirli RNA virüsü. ACE2 reseptörüne bağlanarak alt solunum yollarına invaze olur.",
        "clinicalPearls": "Damlacıkla bulaşır; entübasyon gibi aerosol oluşturan işlemlerde N95 maske ve solunum izolasyonu gerekir.",
        "badgeColor": "rose"
    },
    {
        "term": "Varicella Zoster Virüsü (VZV)",
        "aliases": ["varicella zoster", "vzv", "suçiçeği virüsü"],
        "category": "Viroloji",
        "pronunciation": "[va-ri-sel-la zos-ter]",
        "definition": "Zarflı çift zincirli DNA virüsü (Herpesviridae). Primer enfeksiyonu suçiçeği, duyusal gangliyonlarda reaktivasyonu ise zonadır.",
        "clinicalPearls": "Hem damlacık hem solunum yoluyla (<5 µm aerosol) bulaşır; hastanede SOLUNUM İZOLASYONU (Sarı Yaprak) uygulanır.",
        "badgeColor": "amber"
    },
    {
        "term": "Kızamık Virüsü (Rubeola)",
        "aliases": ["kızamık virüsü", "rubeola", "measles virus"],
        "category": "Viroloji",
        "pronunciation": "[ru-be-o-la]",
        "definition": "Zarflı, tek zincirli negatif RNA virüsü (Paramiksovirüs). Koplik lekeleri ve makülopapüler döküntü ile seyreder.",
        "clinicalPearls": "R0 değeri 12-18 olan en bulaşıcı virüstür; mikroskobik aerosollerle bulaşır, SOLUNUM İZOLASYONU şarttır.",
        "badgeColor": "rose"
    },
    {
        "term": "İnfluenza Virüsü",
        "aliases": ["influenza", "influenza virüsü", "grip virüsü"],
        "category": "Viroloji",
        "pronunciation": "[in-flu-en-za]",
        "definition": "Segmenter tek zincirli RNA genomuna sahip Orthomyxoviridae üyesi virüs. Hemaglütinin (HA) ve Nöraminidaz (NA) glikoproteinleri içerir.",
        "clinicalPearls": "Antijenik shift (pandemi) ve antijenik drift (mevsimsel epidemi) gösterir; DAMLACIK İZOLASYONU (Mavi Çiçek) gerektirir.",
        "badgeColor": "cyan"
    },
    {
        "term": "Prionlar",
        "aliases": ["prion", "prionlar", "prpsc", "prpc"],
        "category": "Viroloji / Ajan",
        "pronunciation": "[pri-yon]",
        "definition": "Nükleik asit (DNA veya RNA) içermeyen, anormal katlanmış enfeksiyöz protein partikülleri. Normal PrPC proteinlerini PrPSc formuna çevirirler.",
        "clinicalPearls": "Standart otoklav ve kimyasal dezenfektanlara olağanüstü dirençlidir; Creutzfeldt-Jakob ve Kuru hastalıklarına yol açar.",
        "badgeColor": "purple"
    },

    # ==================== LATİN TIBBİ VE ANATOMİK TERİMLER ====================
    {
        "term": "Pes equinovarus",
        "aliases": ["pes equinovarus", "pes ekinovarus", "çomak ayak", "clubfoot"],
        "category": "Latin / Anatomi",
        "pronunciation": "[pes e-kwi-no-va-rus]",
        "definition": "Ayak bileğinin plantar fleksiyon (ekinus), topuğun içe dönmesi (varus) ve ön ayağın adduksiyonu ile karakterize konjenital ayak deformitesi.",
        "clinicalPearls": "Oligohidramniozda mekanik sıkışmaya bağlı DEFORMASYON örneğidir; Edwards sendromunda da sık görülür.",
        "badgeColor": "indigo"
    },
    {
        "term": "Pterygium colli (Yele Boyun)",
        "aliases": ["pterygium colli", "yele boyun", "webbed neck"],
        "category": "Latin / Anatomi",
        "pronunciation": "[pte-ri-ji-yum kol-li]",
        "definition": "Mastoid çıkıntıdan akromiyona kadar uzanan bilateral boyun derisi kıvrımı (kanat şeklinde cilt katlantısı).",
        "clinicalPearls": "Fetal dönemdeki masif kistik higromanın (lenfödem) rezolüsyon kalıntısıdır; Turner Sendromu (45,X) için patognomoniktir.",
        "badgeColor": "rose"
    },
    {
        "term": "Cubitus valgus",
        "aliases": ["cubitus valgus", "kubitus valgus"],
        "category": "Latin / Anatomi",
        "pronunciation": "[ku-bi-tus val-gus]",
        "definition": "Kollar anatomik pozisyondayken ön kolun gövdeden dışarıya doğru artmış bir açıyla (taşıma açısı >15°) sapması deformitesi.",
        "clinicalPearls": "Turner Sendromunda (45,X) klasik bir iskelet sistemi muayene bulgusudur.",
        "badgeColor": "indigo"
    },
    {
        "term": "Cutis aplasia (Cutis Congenita)",
        "aliases": ["cutis aplasia", "cutis aplazia", "cutis congenita", "aplasia cutis"],
        "category": "Latin / Anatomi",
        "pronunciation": "[ku-tis ap-la-zi-ya]",
        "definition": "Genellikle verteks saçlı deride doğuştan cildin, derialtı dokusunun ve nadiren kafatası kemiğinin lokalize yokluğu defekti.",
        "clinicalPearls": "Patau Sendromu (Trizomi 13) için son derece karakteristik bir kraniyofasyal anomalidir.",
        "badgeColor": "purple"
    },
    {
        "term": "Clenched Hand (Kenetlenmiş El)",
        "aliases": ["clenched hand", "kenetlenmiş el", "yumruk kenetlenmesi"],
        "category": "Latin / Anatomi",
        "pronunciation": "[klençt hend]",
        "definition": "2. ve 5. parmakların 3. ve 4. parmaklar üzerine bindiği karakteristik parmak fleksiyon kontraktürü manzarası.",
        "clinicalPearls": "Edwards Sendromunun (Trizomi 18) en patognomonik fizik muayene bulgusudur.",
        "badgeColor": "rose"
    },
    {
        "term": "Rocker-Bottom Ayak (Beşik Taban)",
        "aliases": ["rocker-bottom", "rocker bottom", "fırlak topuk", "beşik taban"],
        "category": "Latin / Anatomi",
        "pronunciation": "[ra-kır ba-tım]",
        "definition": "Belirgin kalkaneus çıkıntısı ve düzleşmiş/kavisli taban yapısı ile beşik ayaklığına benzeyen konjenital taban deformitesi.",
        "clinicalPearls": "Trizomi 18 (Edwards Sendromu) ve miksoploidide karakteristik klinik tablodur.",
        "badgeColor": "amber"
    },
    {
        "term": "Simian Çizgisi (Tek Palmar Çizgi)",
        "aliases": ["simian çizgisi", "simian crease", "tek palmar çizgi", "dört parmak çizgisi"],
        "category": "Latin / Anatomi",
        "pronunciation": "[si-mi-yan]",
        "definition": "Avuç içindeki normal iki transvers fleksür çizgisinin birleşerek el ayasını baştan başa geçen tek bir yatay çizgi oluşturması.",
        "clinicalPearls": "Down Sendromunda (Trizomi 21) %50'den fazla görülür; toplumda sağlıklı bireylerde de %1-2 bulunabilir.",
        "badgeColor": "amber"
    },
    {
        "term": "Holoprosencephaly (Holoprozensefali)",
        "aliases": ["holoprosencephaly", "holoprozensefali"],
        "category": "Latin / Anatomi",
        "pronunciation": "[ho-lo-pro-zen-se-fa-li]",
        "definition": "Embriyonik ön beynin (prosensefalon) sağ ve sol iki serebral hemisfere bölünememesi sonucu oluşan ağır nörogelişimsel malformasyon.",
        "clinicalPearls": "Patau Sendromu (Trizomi 13) kliniğinin temel nöropatolojik komponentidir; siklopi veya yarık dudak-damağa eşlik eder.",
        "badgeColor": "purple"
    },
    {
        "term": "Streak Gonad (Çizgi Gonad)",
        "aliases": ["streak gonad", "çizgi gonad", "gonadal disgenezis"],
        "category": "Latin / Anatomi",
        "pronunciation": "[striyk go-nad]",
        "definition": "Over dokusundaki foliküllerin erken fetal atreziye uğraması sonucu geriye kalan fibröz, çizgi biçimindeki non-fonksiyonel bağ dokusu bandı.",
        "clinicalPearls": "Turner Sendromunda (45,X) primer amenore ve hipergonadotropik hipogonadizmin doğrudan nedenidir.",
        "badgeColor": "rose"
    },
    {
        "term": "Glabella",
        "aliases": ["glabella", "glabella bölgesi"],
        "category": "Latin / Anatomi",
        "pronunciation": "[gla-bel-la]",
        "definition": "Alında, iki kaş arasında ve burun kökünün hemen üzerinde yer alan düz kemiksel alan.",
        "clinicalPearls": "Wolf-Hirschhorn sendromunda (4p16.3) glabella aşırı belirginleşerek Grek savaş miğferi görünümü oluşturur.",
        "badgeColor": "indigo"
    },
    {
        "term": "Telekantus",
        "aliases": ["telekantus", "telecanthus"],
        "category": "Latin / Anatomi",
        "pronunciation": "[te-le-kan-tus]",
        "definition": "Göz bebekleri arasındaki mesafe (interpupiller mesafe) normal iken iç göz kapak köşeleri (iç kantuslar) arasındaki mesafenin artmış olması.",
        "clinicalPearls": "Kemiksel orbitanın birbirinden uzaklaştığı Hipertelorizmden farklıdır; yumuşak doku anomalisi olup Waardenburg sendromunda sıktır.",
        "badgeColor": "indigo"
    },
    {
        "term": "Hipertelorizm",
        "aliases": ["hipertelorizm", "hypertelorism"],
        "category": "Latin / Anatomi",
        "pronunciation": "[hi-per-te-lo-rizm]",
        "definition": "İki göz çukuru (orbita) arasındaki kemiksel mesafenin ve interpupiller mesafenin +2 standart sapmanın üzerinde genişlemiş olması.",
        "clinicalPearls": "Cri-du-chat (5p-) ve Wolf-Hirschhorn (4p-) sendromlarında tipik yüz bulgusudur.",
        "badgeColor": "indigo"
    },
    {
        "term": "Klinodaktili",
        "aliases": ["klinodaktili", "clinodactyly"],
        "category": "Latin / Anatomi",
        "pronunciation": "[kli-no-dak-ti-li]",
        "definition": "Genellikle 5. parmağın (küçük parmak) orta falanks hipoplazisi nedeniyle 4. parmağa doğru medial eğrilik göstermesi.",
        "clinicalPearls": "Down sendromunda en sık rastlanan minör ekstremite anomalilerindendir.",
        "badgeColor": "amber"
    },

    # ==================== GENETİK VE DİSMORFOLOJİ TERİMLERİ ====================
    {
        "term": "Malformasyon",
        "aliases": ["malformasyon", "malformation"],
        "category": "Genetik & Dismorfoloji",
        "pronunciation": "[mal-for-mas-yon]",
        "definition": "Embriyonik organogenez evresinde dokunun primer oluşum hatası sonucu ortaya çıkan yapısal organ defekti (intrinsik gelişim kusuru).",
        "clinicalPearls": "Yarık dudak-damak, VSD ve spina bifida klasik malformasyon örnekleridir.",
        "badgeColor": "purple"
    },
    {
        "term": "Deformasyon",
        "aliases": ["deformasyon", "deformation"],
        "category": "Genetik & Dismorfoloji",
        "pronunciation": "[de-for-mas-yon]",
        "definition": "Normal gelişmekte olan bir dokunun fötal hayatta dış mekanik bası güçleri (örneğin oligohidramniyoz) etkisiyle şekil ve biçim değiştirmesi.",
        "clinicalPearls": "Pes ekinovarus ve Potter yüzü klasik deformasyonlardır; prognozu malformasyona göre çok daha iyidir.",
        "badgeColor": "teal"
    },
    {
        "term": "Disrupsiyon",
        "aliases": ["disrupsiyon", "disruption"],
        "category": "Genetik & Dismorfoloji",
        "pronunciation": "[dis-rup-si-yon]",
        "definition": "Normal gelişim sürecindeki bir organ veya vücut parçasının dışsal mekanik bantlar (amniyotik bant) veya vasküler iskemiyle parçalanıp yıkıma uğraması.",
        "clinicalPearls": "Kalıtsal değildir, rekürrens riski düşüktür; amniyotik bant amputasyonu en bilinen örneğidir.",
        "badgeColor": "rose"
    },
    {
        "term": "Displazi",
        "aliases": ["displazi", "dysplasia"],
        "category": "Genetik & Dismorfoloji",
        "pronunciation": "[dis-pla-zi]",
        "definition": "Genetik mutasyon nedeniyle bir dokudaki hücrelerin yapısal organizasyon ve diferansiyasyonunun bozulması.",
        "clinicalPearls": "Akondroplazi (FGFR3) ve osteogenezis imperfekta doku displazileridir; bulgular yaşla ilerler.",
        "badgeColor": "indigo"
    },
    {
        "term": "Non-Disjunction (Kromozom Ayrılamaması)",
        "aliases": ["non-disjunction", "nondisjunction", "ayrılamama", "mayotik ayrılmama"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[non-dis-cank-şın]",
        "definition": "Hücre bölünmesinde (Mayoz veya Mitoz) homolog kromozomların veya kardeş kromatitlerin zıt kutuplara ayrılamayarak aynı hücreye gitmesi kusuru.",
        "clinicalPearls": "Anöploidilerin (Trizomi 21, 18, 13, Klinefelter) bir numaralı nedenidir; Mayoz I'de olursa heterolog, Mayoz II'de olursa özdeş kromatitler aktarılır.",
        "badgeColor": "teal"
    },
    {
        "term": "Anaphase Lagging (Anafaz Gecikmesi)",
        "aliases": ["anaphase lagging", "anafazda geri kalma", "anafaz gecikmesi"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[e-na-feyz leg-ging]",
        "definition": "Anafazda bir kromatitin iğ ipliği yetersizliği nedeniyle kutba hareket etmekte gecikmesi ve nükleus zarı dışında kalarak sitoplazmada kaybolması.",
        "clinicalPearls": "Monozomi ve mozaik karyotiplerin (özellikle mozaik Turner ve Down) temel hücresel mekanizmasıdır.",
        "badgeColor": "teal"
    },
    {
        "term": "Robertsonyan Translokasyon",
        "aliases": ["robertsonyan translokasyon", "robertsonian translokasyon", "sentrik füzyon"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[ra-bırt-sin-yın]",
        "definition": "Yalnızca akrosentrik kromozomların (13, 14, 15, 21, 22) sentromer yakınından kırılarak uzun kollarının birleşmesi ve kısa kollarının kaybolması.",
        "clinicalPearls": "Taşıyıcı 45 kromozomludur ve sağlıklıdır; rob(14;21) taşıyıcısı annede Down sendromlu çocuk riski %10-15, rob(21;21)'de %100'dür.",
        "badgeColor": "teal"
    },
    {
        "term": "İzokromozom",
        "aliases": ["izokromozom", "isochromosome", "i(xq)"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[i-zo-kro-mo-zom]",
        "definition": "Sentromerin uzunlamasına değil enlemesine hatalı bölünmesiyle bir kolun silinip diğer kolun ayna simetrisi şeklinde çift kopyaya çıkması.",
        "clinicalPearls": "En sık örnek i(Xq)'dur; Turner Sendromu olgularının %15'ini oluşturur.",
        "badgeColor": "indigo"
    },
    {
        "term": "Genomik İmprinting",
        "aliases": ["genomik imprinting", "genomic imprinting", "epigenetik susturma"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[ce-no-mik im-prin-ting]",
        "definition": "Gametogenez sırasında belirli genlerin DNA metilasyonu ile maternal ya da paternal kökene bağımlı olarak susturulması (inaktivasyonu).",
        "clinicalPearls": "15q11-q13 lokusunda babadan aktif genlerin kaybı Prader-Willi; anneden aktif UBE3A geninin kaybı Angelman Sendromu yapar.",
        "badgeColor": "purple"
    },
    {
        "term": "Uniparental Dizomi (UPD)",
        "aliases": ["uniparental dizomi", "upd", "maternal upd", "paternal upd"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[u-ni-pa-ren-tal di-zo-mi]",
        "definition": "Diploid bir bireyde homolog kromozom çiftinin her iki üyesinin de tek bir ebeveynden kalıtılması durumu.",
        "clinicalPearls": "Maternal UPD 15 -> Prader-Willi sendromuna; Paternal UPD 15 -> Angelman sendromuna yol açar.",
        "badgeColor": "purple"
    },
    {
        "term": "İzodizomi vs Heterodizomi",
        "aliases": ["izodizomi", "heterodizomi", "isodisomy", "heterodisomy"],
        "category": "Genetik & Patoloji",
        "pronunciation": "[i-zo-di-zo-mi]",
        "definition": "İzodizomi tek bir ebeveyn kromozomunun duplikasyonu (otozomal resesif hastalık riski taşır); Heterodizomi ise ebeveynin iki farklı homologunun birden aktarılmasıdır.",
        "clinicalPearls": "Mayoz I ayrılmama kalıntısı heterodizomi, Mayoz II ayrılmama kalıntısı izodizomi yaratır.",
        "badgeColor": "purple"
    },

    # ==================== PATOLOJİ TERİMLERİ ====================
    {
        "term": "Apoptoz (Programlı Hücre Ölümü)",
        "aliases": ["apoptoz", "apoptozis", "apoptosis", "programlı hücre ölümü"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[a-pop-toz]",
        "definition": "Hücre zarı bütünlüğünü koruyarak kaspaz enzimleri aracılığıyla hücrenin büzüşmesi, nükleer kromatin yoğunlaşması ve enflamasyonsuz fagositozla yok edilmesi.",
        "clinicalPearls": "Nekrozdan farkı çevre dokuda enflamatuar reaksiyon YARATMAMASIDIR; embriyogenezde parmak aralarının açılmasını sağlar.",
        "badgeColor": "emerald"
    },
    {
        "term": "Koagülasyon Nekrozu",
        "aliases": ["koagülasyon nekrozu", "coagulative necrosis"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[ko-a-gü-las-yon nek-ro-zu]",
        "definition": "Hücre proteinlerinin ve enzimlerinin asidozla denatüre olması sonucu hücre temel mimarisinin (hayalet hücre manzarası) günlerce korunduğu iskemi nekrozu.",
        "clinicalPearls": "BEYİN HARİÇ tüm solid organ enfarktüslerinin (miyokard, böbrek, dalak) temel nekroz tipidir.",
        "badgeColor": "rose"
    },
    {
        "term": "Likefaksiyon (Sıvılaşma) Nekrozu",
        "aliases": ["likefaksiyon nekrozu", "sıvılaşma nekrozu", "liquefactive necrosis"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[li-ke-fak-si-yon]",
        "definition": "Güçlü litik enzimlerin dokuyu tamamen sindirerek amorf vizköz bir sıvı kütlesine (cerahat/apse) dönüştürdüğü nekroz tipi.",
        "clinicalPearls": "Bakteriyel piyojenik apselerde ve SANTRAL SİNİR SİSTEMİ (beyin) iskemik enfarktüslerinde karakteristiktir.",
        "badgeColor": "rose"
    },
    {
        "term": "Kazeifikasyon Nekrozu",
        "aliases": ["kazeifikasyon", "kazeöz nekroz", "caseous necrosis", "peynirleşme nekrozu"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[ka-ze-i-fi-kas-yon]",
        "definition": "Hücre mimarisinin tamamen silindiği, amorf, granüler, yapısız ve eozinofilik peynirimsi doku harabiyeti manzarası.",
        "clinicalPearls": "Mycobacterium tuberculosis (Tüberküloz) granülomlarının merkezinde patognomoniktir.",
        "badgeColor": "rose"
    },
    {
        "term": "Fibrinoid Nekroz",
        "aliases": ["fibrinoid nekroz", "fibrinoid necrosis"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[fib-ri-noyd nek-roz]",
        "definition": "Damar duvarında antijen-antikor kompleksleri ile plazma proteinlerinin birikmesiyle parlak pembe, amorf birikim oluşması.",
        "clinicalPearls": "Malign hipertansiyon ve immün kompleks vaskülitlerinde (PAN, SLE) görülür.",
        "badgeColor": "rose"
    },
    {
        "term": "Steatoz (Yağlanma)",
        "aliases": ["steatoz", "hepatosteatoz", "yağlanma", "fatty change"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[ste-a-toz]",
        "definition": "Parankim hücreleri (özellikle hepatositler) sitoplazmasında anormal trigliserit vakuollerinin birikmesi.",
        "clinicalPearls": "Alkol kullanımı, obezite, diyabet ve protein malnütrisyonunda (Kwashiorkor) en sık karaciğerde geri dönüşümlü hücre hasarı bulgusudur.",
        "badgeColor": "amber"
    },
    {
        "term": "Distrofik Kalsifikasyon",
        "aliases": ["distrofik kalsifikasyon", "dystrophic calcification"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[dis-tro-fik kal-si-fi-kas-yon]",
        "definition": "Serum kalsiyum düzeyi NORMAL iken, nekrotik veya hasarlı dokularda (aterom plağı, tüberküloz kazeöz odağı, yaşlı kalp kapakları) kalsiyum tuzlarının çökmesi.",
        "clinicalPearls": "Metastatik kalsifikasyondan farkı kalsiyum-fosfor metabolizmasının normal olması ve sadece hasarlı dokuda gerçekleşmesidir.",
        "badgeColor": "purple"
    },
    {
        "term": "Metastatik Kalsifikasyon",
        "aliases": ["metastatik kalsifikasyon", "metastatic calcification"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[me-tas-ta-tik kal-si-fi-kas-yon]",
        "definition": "Serumda HİPERKALSEMİ bulunması nedeniyle normal sağlıklı dokularda (mide mukozası, akciğer alveolleri, böbrek tübülleri) kalsiyum tuzlarının birikmesi.",
        "clinicalPearls": "Hiperparatiroidizm, kemik metastazları ve D vitamini intoksikasyonunda görülür; asit salgılayan dokuları sever.",
        "badgeColor": "purple"
    },
    {
        "term": "Virchow Triadı",
        "aliases": ["virchow triadı", "virchow üçlüsü", "virchow triad"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[vir-şov tri-ya-dı]",
        "definition": "İntravasküler tromboz oluşumunu başlatan 3 temel patolojik faktör: 1) Endotel Hasarı, 2) Kan Akımında Bozulma (Staz veya Türbülans), 3) Hiperkoagülabilite.",
        "clinicalPearls": "Derin ven trombozu ve pulmoner emboli gelişiminin evrensel patogenez modelidir.",
        "badgeColor": "red"
    },
    {
        "term": "Metaplazi",
        "aliases": ["metaplazi", "metaplasia"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[me-tap-la-zi]",
        "definition": "Kronik strese maruz kalan diferansiye bir erişkin hücre tipinin yerini strese daha dirençli başka bir hücre tipine bırakması.",
        "clinicalPearls": "Sigarada bronşiyal yassı epitel metaplazisi; reflüde Barrett özofagusu (intestinal glandüler metaplazi).",
        "badgeColor": "indigo"
    },
    {
        "term": "Granülom",
        "aliases": ["granülom", "granülomatöz enflamasyon", "granuloma"],
        "category": "Tıbbi Patoloji",
        "pronunciation": "[gra-nü-lom]",
        "definition": "Eritilemeyen partiküllere karşı epiteloid histiyositlerin, multinükleer dev hücrelerin (Langhans) ve çevreleyen lenfosit yakasının oluşturduğu kronik nodüler odak.",
        "clinicalPearls": "Tüberküloz (kazeöz), Sarkoidoz (non-kazeöz), Yabancı cisim ve Sifilizde görülür.",
        "badgeColor": "emerald"
    },

    # ==================== ÜROLOJİ VE NEFROLOJİ ====================
    {
        "term": "Hidronefroz",
        "aliases": ["hidronefroz", "hydronephrosis"],
        "category": "Üroloji / Nefroloji",
        "pronunciation": "[hid-ro-nef-roz]",
        "definition": "İdrar akımındaki obstrüksiyon nedeniyle renal pelvis ve kalikslerin aşırı genişlemesi ve böbrek parankiminin bası atrofisine uğraması.",
        "clinicalPearls": "En sık üreter taşı, BPH, pelviüreteral darlık ve retroperitoneal fibroziste gelişir; bası atrofisi böbrek yetmezliği doğurabilir.",
        "badgeColor": "blue"
    },
    {
        "term": "Strüvit Taşı (Magnezyum Amonyum Fosfat)",
        "aliases": ["strüvit", "struvite", "enfeksiyon taşı", "staghorn taş", "geyik boynuzu taş"],
        "category": "Üroloji / Nefroloji",
        "pronunciation": "[st-rü-vit]",
        "definition": "Üreaz üreten bakterilerin (Proteus, Klebsiella) idrarı alkalileştirmesiyle renal toplayıcı sistemi tamamen dolduran geyik boynuzu (staghorn) taşlar.",
        "clinicalPearls": "Tipik tabut kapağı kristali içerir; taş cerrahiyle çıkarılmadıkça idrar yolu enfeksiyonu tam tedavi edilemez.",
        "badgeColor": "amber"
    },
    {
        "term": "Kalsiyum Oksalat Taşı",
        "aliases": ["kalsiyum oksalat", "calcium oxalate"],
        "category": "Üroloji / Nefroloji",
        "pronunciation": "[kal-si-yum ok-sa-lat]",
        "definition": "Tüm üriner sistem taşlarının yaklaşık %70-80'ini oluşturan en yaygın böbrek taşı türü.",
        "clinicalPearls": "Radyoopaktır (direk grafide beyaz görünür); zarf şeklinde monohidrat/dihidrat kristalleri gösterir.",
        "badgeColor": "blue"
    },
    {
        "term": "Vezikoüreteral Reflü (VÜR)",
        "aliases": ["vür", "vezikoüreteral reflü", "vur"],
        "category": "Üroloji / Nefroloji",
        "pronunciation": "[ve-zi-ko-ü-re-te-ral ref-lü]",
        "definition": "Mesane ile üreter arasındaki valv mekanizmasının yetersizliği nedeniyle miksiyon esnasında idrarın mesaneden böbreğe geri kaçması.",
        "clinicalPearls": "Çocukluk çağında tekrarlayan febril üriner enfeksiyonların ve kronik piyelonefritik renal skarlaşmanın bir numaralı nedenidir.",
        "badgeColor": "cyan"
    },

    # ==================== FARMAKOLOJİ VE İLAÇLAR ====================
    {
        "term": "Vankomisin",
        "aliases": ["vankomisin", "vancomycin"],
        "category": "Farmakoloji",
        "pronunciation": "[van-ko-mi-sin]",
        "definition": "D-Ala-D-Ala ucuna bağlanarak hücre duvarı peptidoglikan sentezini engelleyen glikopeptid antibiyotik.",
        "clinicalPearls": "MRSA bakteriyemisinde intravenöz; C. difficile kolitinde oral yolla kullanılır.",
        "badgeColor": "cyan"
    },
    {
        "term": "Karbapenemler",
        "aliases": ["karbapenem", "meropenem", "imipenem", "ertapenem"],
        "category": "Farmakoloji",
        "pronunciation": "[kar-ba-pe-nem]",
        "definition": "Çoğu beta-laktamaz enzimine dirençli, gram negatif basillere karşı en geniş spektrumlu son çare beta-laktam antibiyotik ailesi.",
        "clinicalPearls": "Direnç geliştiğinde (Karbapenem Dirençli Enterobacteriaceae - CRE) hastanede Temas İzolasyonu zorunludur.",
        "badgeColor": "cyan"
    },
    {
        "term": "Kolistin (Polimiksin E)",
        "aliases": ["kolistin", "colistin", "polimiksin"],
        "category": "Farmakoloji",
        "pronunciation": "[ko-lis-tin]",
        "definition": "Gram negatif bakterilerin dış membranındaki LPS yapısını bozarak deterjan benzeri etkiyle hücreyi patlatan polipeptid antibiyotik.",
        "clinicalPearls": "Nefrotoksik ve nörotoksiktir; pan-rezistan Acinetobacter ve Klebsiella suşlarında son çaredir.",
        "badgeColor": "red"
    },
    {
        "term": "Rifampisin",
        "aliases": ["rifampisin", "rifampin"],
        "category": "Farmakoloji",
        "pronunciation": "[ri-fam-pi-sin]",
        "definition": "Bakteriyel DNA bağımlı RNA polimerazı inhibe ederek transkripsiyonu durduran güçlü antibiyotik.",
        "clinicalPearls": "Tüberküloz tedavisinin ana ilacıdır; ayrıca Meningokok menenjiti temaslılarına profilakside verilir; idrarı ve teri kırmızı-turuncuya boyar.",
        "badgeColor": "amber"
    },

    # ==================== EPİDEMİYOLOJİ VE İZOLASYON ====================
    {
        "term": "İnfodemi",
        "aliases": ["infodemi", "infodemic"],
        "category": "Epidemiyoloji",
        "pronunciation": "[in-fo-de-mi]",
        "definition": "Salgın sırasında doğru bilgilerle birlikte aşırı miktarda yanlış, asılsız ve kitlelerde panik yaratan dedikodu/bilgi seli yayılması.",
        "clinicalPearls": "DSÖ çözüm formülü: Konuşma, Dinleme ve Dedikoduları Engelleme.",
        "badgeColor": "rose"
    },
    {
        "term": "Eradikasyon",
        "aliases": ["eradikasyon", "eradication"],
        "category": "Epidemiyoloji",
        "pronunciation": "[e-ra-di-kas-yon]",
        "definition": "Bir patojenin dünya çapında görülme sıklığının kalıcı olarak sıfırlanması; tüm dünyadan rezervuarlarıyla silinmesi.",
        "clinicalPearls": "Dünya genelinde aşı ve müdahale sonlandırılır; insanda tek örnek Çiçek Hastalığıdır (1980).",
        "badgeColor": "emerald"
    },
    {
        "term": "Eliminasyon",
        "aliases": ["eliminasyon", "elimination"],
        "category": "Epidemiyoloji",
        "pronunciation": "[e-li-mi-nas-yon]",
        "definition": "Hastalığın etkeni dünyada bulunmaya devam ederken, belirli bir coğrafi bölgede (ülkede) yerli (otokton) vakanın artık görülmemesi.",
        "clinicalPearls": "Eradikasyondan farkı: Sürveyans, aşı ve kontrol önlemleri KESİNTİSİZ DEVAM ETMEK ZORUNDADIR!",
        "badgeColor": "blue"
    },
    {
        "term": "Negatif Basınçlı Oda",
        "aliases": ["negatif basınçlı oda", "negatif basınç", "negative pressure room"],
        "category": "İzolasyon",
        "pronunciation": "[ne-ga-tif ba-sınç]",
        "definition": "Oda içi hava basıncının koridora göre daha düşük tutulduğu, böylece kapı açıldığında havanın koridora kaçmayıp koridordan odaya girdiği özel oda mimarisi.",
        "clinicalPearls": "Solunum izolasyonunda (Tüberküloz, Kızamık, Suçiçeği) zorunludur; hava saatte 6-12 kez değiştirilir ve HEPA filtreden geçirilir.",
        "badgeColor": "amber"
    },
    {
        "term": "Pozitif Basınçlı Oda (Koruyucu Ortam)",
        "aliases": ["pozitif basınçlı oda", "pozitif basınç", "koruyucu ortam", "ters izolasyon"],
        "category": "İzolasyon",
        "pronunciation": "[po-zi-tif ba-sınç]",
        "definition": "Oda içi hava basıncının koridora göre daha yüksek tutularak koridordaki patojenlerin içeri sızmasının engellendiği özel ortam.",
        "clinicalPearls": "Kemik iliği nakli alıcıları ve derin nötropenik (nötrofil <500) hastalar için kullanılır; HEPA filtre şarttır.",
        "badgeColor": "cyan"
    }
]

def main():
    print(f"Generating Medical Glossary Database with {len(GLOSSARY_TERMS)} rich clinical terms...")
    with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
        json.dump(GLOSSARY_TERMS, f, ensure_ascii=False, indent=2)
    print(f"Saved medical glossary to {GLOSSARY_PATH} successfully.")

if __name__ == '__main__':
    main()
