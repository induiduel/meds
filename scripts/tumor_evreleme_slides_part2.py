# -*- coding: utf-8 -*-
"""
Part 2 of the Tumor Staging and Laboratory Diagnosis Deck (Slides 13 to 24)
"""

SLIDES_PART2 = [
    {
        "slideNumber": 13,
        "title": "İntraoperatif Konsültasyon (Frozen Section)",
        "subtitle": "Hızlı Dondurulmuş Kesit Tekniği, Cerrahi Sınır Değerlendirmesi ve Kısıtlılıklar",
        "synthesisNarrative": "Frozen section ameliyat sırasında taze dokudan 10-15 dakikada cerrahi sınırları ve hızlı maligniteyi denetler; ancak tiroid foliküler lezyonlarında ve lenfoma sınıflamasında endike değildir.",
        "content": """İntraoperatif konsültasyon (hızlı dondurulmuş kesit / frozen section); hasta ameliyathanede anestezi altındayken ve cerrahi işlem devam ederken, cerrahın operasyonun seyrini anında değiştirecek kritik bir karara varmak amacıyla patoloğa taze doku göndererek acil histopatolojik görüş talep etmesidir.

Frozen Section Tekniği:
Ameliyathaneden patolojiye hiçbir fiksatif konulmadan TAZE olarak ulaştırılan doku örneği makroskobik olarak incelenir. Doku, kriyostat adı verilen (-20°C ila -30°C) dondurucu kabinde dondurma jeli içine gömülerek dondurulur. Kriyostat mikrotomu ile 4-6 mikronluk ince kesitler alınır, alkolle fikse edilip modifiye hematoksilen-eozin (H&E) ile boyanır. Patolog mikroskop altında inceleyerek 10-15 dakika içerisinde cerraha sözlü rapor verir.

Frozen Section'ın 4 Temel Endikasyonu:
1) Bilinmeyen Lezyonun Benign-Malign Ayrımı: Ameliyatın genişliğini belirler. Örneğin over kistektomisinde kitlenin benign kistadenom mu yoksa karsinom mu olduğunu belirleyerek radikal cerrahiye geçilip geçilmeyeceğine karar verilir.
2) Cerrahi Rezeksiyon Sınırlarının (Marjin) Kontrolü: Geride tümör kalıp kalmadığını belirler. Örneğin meme koruyucu cerrahide cerrahi sınırda tümör izlenirse sınır genişletilerek R0 rezeksiyon sağlanır.
3) Beklenmedik Şüpheli Odakların Değerlendirilmesi: Küratif cerrahi planlanan olguda peritonda veya karaciğerde saptanan milimetrik nodüllerin metastaz olup olmadığının teyidi.
4) Dokunun Tanı İçin Yeterliliğinin Kontrolü: Derin organ biyopsilerinde örneğin nekrotik alan değil canlı tümör içerip içermediğini teyit etmek.

Frozen Section'ın Kısıtlılıkları ve Kontrendikasyonları:
Dondurma artefaktı nükleer detayı bozabilir. Kemik ve kalsifiye lezyonlar dondurularak kesilemez.
- Tiroid Foliküler Neoplazmları: Foliküler adenom ile karsinom ayrımı tümör kapsülünün ve damarlarının boydan boya incelenmesini (kapsüler/vasküler invazyon) gerektirir; intraoperatif 1-2 dondurulmuş kesitle asla dışlanamaz, frozen KESİNLİKLE ENDİKE DEĞİLDİR!
- Primer Lenfoma Tiplendirmesi: Parafin İHK ve akış sitometrisi gerektirir; frozen artefaktı morfolojiyi bozar. Kesin tanı kalıcı parafin kesitlerle konur.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Frozen section cerrahi sınır kontrolü ve hızlı malignite tespiti için hayati bir intraoperatif yöntemdir; ancak kapsül invazyonunun taranması gereken Tiroid Foliküler Neoplazmlarında (adenom-karsinom ayrımı) ve Lenfoma tiplendirmesinde KESİNLİKLE ENDİKE DEĞİLDİR.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Ameliyat sırasında cerrahın cerrahi rezeksiyon marjininin temizliğini teyit etmek ve operasyonun seyrini belirlemek amacıyla taze dokudan 10-15 dakikada sonuç aldığı yöntem nedir? (İntraoperatif konsültasyon / Frozen section).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Frozen section taze dokunun kriyostatta dondurulup H&E boyanmasıyla 10-15 dakikada sonuç verir.",
            "Cerrahi sınır temizliğinin kontrolü ve lezyonun benign-malign ayrımı temel endikasyonlarıdır.",
            "Tiroid foliküler lezyonlarında kapsül invazyonu değerlendirilemeyeceğinden frozen yapılmaz."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-013",
            "question": "İntraoperatif konsültasyon (frozen section) yöntemi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Taze doku örneği kriyostatta -20°C ila -30°C'de dondurularak 10-15 dakika içinde cerraha mikroskobik tanı verilir.",
                "B) Cerrahi rezeksiyon sınırlarının tümörden temiz olup olmadığının kontrolü en temel endikasyonlarından biridir.",
                "C) Tiroid foliküler neoplazmlarında kapsüler veya vasküler invazyonu hızla ekarte ederek foliküler adenom-karsinom ayrımı yapmak için idealdir.",
                "D) Dondurma artefaktı hücresel detayları bozabileceğinden kesin tanı mutlaka daha sonra rutin parafin kesitlerle teyit edilir.",
                "E) Kemik ve kalsifiye lezyonlar kriyostat mikrotomunda dondurularak kesilemediği için frozen incelemeye uygun değildir."
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği yanlıştır çünkü tiroid foliküler lezyonlarında foliküler adenom ile karsinom ayrımı tümör kapsülünün ve kapsüler kan damarlarının boydan boya taranmasını (kapsüler/vasküler invazyon) gerektirir. Bu inceleme ameliyat sırasında 1-2 dondurulmuş kesitle ASLA yapılamaz; frozen section bu lezyonlarda KESİNLİKLE ENDİKE DEĞİLDİR ve yanıltıcıdır. Kesin tanı kalıcı parafin kesitlerle konulur. A, B, D ve E seçenekleri doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-013",
                "question": "İntraoperatif konsültasyon (frozen section) yöntemi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Taze doku örneği kriyostatta -20°C ila -30°C'de dondurularak 10-15 dakika içinde cerraha mikroskobik tanı verilir.",
                    "B) Cerrahi rezeksiyon sınırlarının tümörden temiz olup olmadığının kontrolü en temel endikasyonlarından biridir.",
                    "C) Tiroid foliküler neoplazmlarında kapsüler veya vasküler invazyonu hızla ekarte ederek foliküler adenom-karsinom ayrımı yapmak için idealdir.",
                    "D) Dondurma artefaktı hücresel detayları bozabileceğinden kesin tanı mutlaka daha sonra rutin parafin kesitlerle teyit edilir.",
                    "E) Kemik ve kalsifiye lezyonlar kriyostat mikrotomunda dondurularak kesilemediği için frozen incelemeye uygun değildir."
                ],
                "correctAnswer": 2,
                "explanation": "C seçeneği yanlıştır çünkü tiroid foliküler lezyonlarında foliküler adenom ile karsinom ayrımı tümör kapsülünün ve kapsüler kan damarlarının boydan boya taranmasını (kapsüler/vasküler invazyon) gerektirir. Bu inceleme ameliyat sırasında 1-2 dondurulmuş kesitle ASLA yapılamaz; frozen section bu lezyonlarda KESİNLİKLE ENDİKE DEĞİLDİR ve yanıltıcıdır. Kesin tanı kalıcı parafin kesitlerle konulur. A, B, D ve E seçenekleri doğrudur."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Sitolojik Tanı Yöntemleri: Eksfoliyatif Sitoloji ve İnce İğne Aspirasyonu (İİAB)",
        "subtitle": "Hücre Morfolojisi, Kohezivite Kaybı, Pap Smear ve Vücut Sıvıları",
        "synthesisNarrative": "Sitolojik tanı malign hücrelerin kohezivite kaybına dayanır; İİAB hücresel atipiyi minimal invaziv biçimde gösterirken doku mimarisini gösteremediği için invazyonu değerlendiremez.",
        "content": """Sitolojik tanı yöntemleri; tek tek dökülen veya iğneyle aspire edilen hücrelerin mikroskobik incelenmesine dayanan, hızlı, ucuz ve minimal invaziv yaklaşımlardır. Sitolojinin biyolojik temeli: Malign neoplazmlarda E-kaderin ve hücreler arası bağlantıların kaybı sonucu hücresel kohezivitenin (yapışkanlığın) bozulmasıdır. Bu sayede tümör hücreleri çevre boşluklara ve sıvılara kolayca dökülürler.

1) Eksfoliyatif Sitoloji:
Yüzeylerden dökülen veya mekanik olarak sıyrılan serbest hücrelerin incelenmesidir.
- Servikovajinal Smear (Pap Testi): Servikal transformasyon zonundan toplanan hücrelerin Papanicolaou boyasıyla incelenmesidir. Servikal intraepitelyal lezyonların (LSIL / HSIL) karsinoma dönüşmeden hücresel atipi aşamasında yakalanmasını sağlayarak serviks kanseri mortalitesini %70'ten fazla azaltmıştır.
- Vücut Boşluk Sıvıları: Plevra, periton (asit) ve perikard sıvılarının santrifüj çökeltisi incelenir. Malign hücrelerin (karsinomatoz peritonit/plörit) tespiti hastayı doğrudan Evre IV evresine sokar. Beyin omurilik sıvısı (BOS) sitolojisi leptomeningeal karsinomatoziste kritiktir.
- İdrar ve Balgam Sitolojisi: Mesanenin yüksek dereceli ürotelyal karsinomlarının nüks takibinde idrar sitolojisi son derece duyarlıdır.

2) İnce İğne Aspirasyon Biyopsisi (İİAB / FNAB):
Solid lezyonlardan 22-25 gauge ince iğne ve enjektörle negatif basınç altında hücre aspire edilmesidir. Yaymalar Giemsa veya Papanicolaou ile boyanır.
- Uygulama Alanları: Tiroid nodülleri (Bethesda sınıflaması), meme kitleleri, büyümüş lenfadenopatiler ve tükürük bezi tümörleri. Radyoloji eşliğinde karaciğer, pankreas ve retroperitoneal kitlelere uygulanır.
- Avantajları: Anestezi gerektirmez, poliklinik şartlarında 5 dakikada uygulanır, komplikasyonu son derece düşüktür ve ucuzdur.
- En Büyük Kısıtlılığı: Yalnızca aspire edilen hücreleri gösterir; doku mimarisini (tümör-stroma ilişkisini) göstermez. Bu nedenle tümörün bazal membranı aşıp aşmadığını (örneğin duktal karsinoma in situ ile invaziv duktal karsinom ayrımını) belirleyemez.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Sitolojik incelemenin biyolojik temeli malign hücrelerdeki E-kaderin azalması ve kohezivite (yapışkanlık) kaybıdır. İİAB hücre morfolojisini mükemmel yansıtır ancak doku mimarisini gösteremediği için in situ-invaziv karsinom ayrımı yapamaz.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Tiroid nodüllerinin preoperatif değerlendirilmesinde poliklinik şartlarında anestezi gerektirmeden uygulanan, malignite riskini belirlemede ilk basamakta tercih edilen sitolojik yöntem hangisidir? (İnce İğne Aspirasyon Biyopsisi / İİAB).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Malign hücrelerin kohezivite kaybı sayesinde dökülmesi eksfoliyatif sitolojinin temelidir.",
            "Pap smear serviks kanseri öncülü lezyonları saptayarak mortaliteyi dramatik şekilde azaltmıştır.",
            "İİAB minimal invazivdir fakat doku mimarisini göstermediğinden invazyon derinliğini değerlendiremez."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-014",
            "question": "Sitolojik tanı yöntemleri (eksfoliyatif sitoloji ve İİAB) ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Malign hücrelerin yüzeylerden ve sıvılara kolayca dökülebilmesinin temel nedeni hücreler arası adezyon ve E-kaderin kaybıdır.",
                "B) Servikovajinal Pap testi (Pap smear) servikal displazilerin erken teşhisini sağlayarak serviks kanseri mortalitesini dramatik azaltmıştır.",
                "C) İnce iğne aspirasyon biyopsisi (İİAB) tiroid nodülleri ve tükürük bezi kitlelerinde ilk basamakta tercih edilen ucuz ve minimal invaziv bir yöntemdir.",
                "D) İİAB doku mimarisini ve stromal ilişkiyi mükemmel gösterdiği için tümörün invazyon derinliğini ve evresini kesin olarak belirler.",
                "E) Plevra veya periton sıvısında malign hücrelerin sitolojik olarak saptanması hastayı doğrudan Evre IV metastatik evreye sokar."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü İİAB yalnızca aspire edilen izole hücreleri veya küçük hücre kümelerini gösterir; doku mimarisini (stroma-tümör ilişkisini) ve bazal membran bütünlüğünü GÖSTEREMEZ. Bu nedenle tümörün invaziv olup olmadığını (in situ - invaziv ayrımını) ve invazyon derinliğini belirleyemez. A, B, C ve E seçenekleri sitolojinin temel prensipleridir."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-014",
                "question": "Sitolojik tanı yöntemleri (eksfoliyatif sitoloji ve İİAB) ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Malign hücrelerin yüzeylerden ve sıvılara kolayca dökülebilmesinin temel nedeni hücreler arası adezyon ve E-kaderin kaybıdır.",
                    "B) Servikovajinal Pap testi (Pap smear) servikal displazilerin erken teşhisini sağlayarak serviks kanseri mortalitesini dramatik azaltmıştır.",
                    "C) İnce iğne aspirasyon biyopsisi (İİAB) tiroid nodülleri ve tükürük bezi kitlelerinde ilk basamakta tercih edilen ucuz ve minimal invaziv bir yöntemdir.",
                    "D) İİAB doku mimarisini ve stromal ilişkiyi mükemmel gösterdiği için tümörün invazyon derinliğini ve evresini kesin olarak belirler.",
                    "E) Plevra veya periton sıvısında malign hücrelerin sitolojik olarak saptanması hastayı doğrudan Evre IV metastatik evreye sokar."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü İİAB yalnızca aspire edilen izole hücreleri veya küçük hücre kümelerini gösterir; doku mimarisini (stroma-tümör ilişkisini) ve bazal membran bütünlüğünü GÖSTEREMEZ. Bu nedenle tümörün invaziv olup olmadığını (in situ - invaziv ayrımını) ve invazyon derinliğini belirleyemez. A, B, C ve E seçenekleri sitolojinin temel prensipleridir."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "İmmünohistokimya (İHK): Prensipler ve Tanısal Strateji",
        "subtitle": "Parafin Kesitlerde Antijen-Antikor Kenetlenmesi, Kromojenik Paternler ve Rolü",
        "synthesisNarrative": "İmmünohistokimya, parafin dokularda monoklonal antikorlar ve kromojen reaksiyonuyla hedef proteinleri gösterir; transkripsiyon faktörleri nükleer, yapısal proteinler sitoplazmik boyanır.",
        "content": """İmmünohistokimya (İHK); doku kesitlerinde (rutin parafin bloklarda) spesifik hücresel antijenlerin, bunlara karşı özel olarak geliştirilmiş monoklonal veya poliklonal antikorlar aracılığıyla mikroskop altında yerlerinin ve ekspresyon yoğunluklarının gösterilmesini sağlayan moleküler morfolojik bir tanı yöntemidir. Günümüz modern patolojisinde immünohistokimya, sadece morfolojiye dayalı sübjektif yorumu ortadan kaldıran objektif bir köprü görevi görür.

İHK Boyama Mekanizması ve Aşamaları:
1) Antijen Geri Kazanımı (Antigen Retrieval): Formalin fiksasyonu proteinler arasında çapraz bağlar kurarak antijenik epitopları maskeler. Parafin kesitler mikrodalga fırında veya basınçlı kaplarda özel tamponlar (sitrat veya EDTA) içinde ısıtılarak epitoplar antikorların bağlanabileceği açık konfigürasyona getirilir.
2) Primer Antikor Bağlanması: Hedef proteine (örneğin Sitokeratin veya ER) yüksek afiniteli monoklonal antikor uygulanır.
3) Sekonder Antikor ve Enzim Kompleksi: Primer antikoru tanıyan ve üzerinde horseradish peroksidaz (HRP) veya alkalen fosfataz enzimi taşıyan polimerik sekonder antikorlar eklenir.
4) Kromojenik Reaksiyon: Enzimin substratı olan kromojen (en sık 3,3'-diaminobenzidin - DAB) damlatılır. Enzim substratı yıkarak antijenin bulunduğu tam mikroskobik noktada suda çözünmeyen, kalıcı, yoğun kahverengi bir çökelti meydana getirir.
5) Zıt Boyama: Arka plandaki negatif hücre çekirdeklerini maviye boyamak için hematoksilen uygulanır.

Tanısal Boyanma Paternleri ve Subselüler Dağılım:
Bir antijenin doğru pozitif kabul edilmesi için biyolojik olarak bulunması gereken hücresel kompartmanda boyanması zorunludur:
- Nükleer Boyanma: Transkripsiyon faktörleri ve hormon reseptörleri hücre çekirdeğinde boyanmalıdır. Örnek: Östrojen Reseptörü (ER), Progesteron Reseptörü (PR), Ki-67, TTF-1, p53, CDX2, SOX10. Sitoplazmada görülen boyanma yalancı pozitiflik (artefakt) kabul edilir.
- Sitoplazmik Boyanma: İntraselüler filamentler, granüller ve enzimler sitoplazmada boyanır. Örnek: Sitokeratinler, Vimentin, Desmin, Sinaptofizin, Kromogranin A.
- Membranöz Boyanma: Yüzey reseptörleri ve adezyon molekülleri hücre zarında tam veya yarım çember şeklinde boyanır. Örnek: HER2/neu, CD20, CD3, E-kaderin, EGFR.

İHK'nın Tanısal Onkolojideki 3 Temel Misyonu:
1) Köken (Lineage) Belirleme: Işık mikroskobunda ayırt edilemeyen anaplastik tümörlerin karsinom, sarkom, lenfoma veya melanom olup olmadığını kesinleştirmek.
2) Primer Odak Tayini: Bilinmeyen odaktan metastaz yapmış karsinomun asıl çıktığı organı saptamak.
3) Prediktif ve Prognostik Değerlendirme: Tümörün hormonoterapiden, immünoterapiden veya hedefe yönelik akıllı ilaçlardan fayda görüp görmeyeceğini belirlemek.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "İHK'da proteinin hücre içindeki doğru kompartmanda boyanması tanı için şarttır; ER, PR, TTF-1, CDX2 ve Ki-67 mutlak nükleer boyanma verirken; Sitokeratin sitoplazmik, HER2 ve CD20 ise membranöz boyanmalıdır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Parafin doku kesitlerinde antijen-antikor spesifisitesinden yararlanılarak hedef hücresel proteinlerin kromojenik enzim reaksiyonu ile ışık mikroskobunda gösterildiği yöntem hangisidir? (İmmünohistokimya / İHK).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "İHK formalinle fikse parafinde gömülü dokularda monoklonal antikorlarla hedef proteinleri saptar.",
            "Nükleer (ER, Ki-67), sitoplazmik (CK, desmin) ve membranöz (HER2, CD20) boyanma paternleri vardır.",
            "Köken tayini, primer odak tespiti ve hedefe yönelik tedavi seçiminde temel role sahiptir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-015",
            "question": "İmmünohistokimya (İHK) yöntemi, prensipleri ve boyanma paternleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Parafin kesitlerde formalin fiksasyonunun maskelediği antijenik epitoplar mikrodalga veya ısı ile antijen geri kazanımı (retrieval) yapılarak açığa çıkarılır.",
                "B) Kromojenik reaksiyonda en sık kullanılan substrat DAB (diaminobenzidin) olup antijen bölgesinde kalıcı kahverengi çökelti oluşturur.",
                "C) Östrojen reseptörü (ER), Progesteron reseptörü (PR) ve Ki-67 gibi proteinler tanısal olarak membranöz boyanma vermek zorundadır.",
                "D) Sitokeratin ve Vimentin sitoplazmik; HER2/neu ve CD20 ise membranöz boyanma paternine sahiptir.",
                "E) İHK; anaplastik tümörlerde köken tayini, primer odak tespiti ve hedefe yönelik tedavi seçiminde temel rol oynar."
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği yanlıştır çünkü Östrojen Reseptörü (ER), Progesteron Reseptörü (PR), Ki-67 ve TTF-1 gibi moleküller transkripsiyon faktörü ve nükleer reseptör oldukları için MUTLAK NÜKLEER boyanma vermek zorundadır; sitoplazmik veya membranöz boyanmaları artefakt kabul edilir. Membranöz boyanma HER2, CD20 gibi yüzey reseptörlerine özgüdür. A, B, D ve E seçenekleri doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-015",
                "question": "İmmünohistokimya (İHK) yöntemi, prensipleri ve boyanma paternleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Parafin kesitlerde formalin fiksasyonunun maskelediği antijenik epitoplar mikrodalga veya ısı ile antijen geri kazanımı (retrieval) yapılarak açığa çıkarılır.",
                    "B) Kromojenik reaksiyonda en sık kullanılan substrat DAB (diaminobenzidin) olup antijen bölgesinde kalıcı kahverengi çökelti oluşturur.",
                    "C) Östrojen reseptörü (ER), Progesteron reseptörü (PR) ve Ki-67 gibi proteinler tanısal olarak membranöz boyanma vermek zorundadır.",
                    "D) Sitokeratin ve Vimentin sitoplazmik; HER2/neu ve CD20 ise membranöz boyanma paternine sahiptir.",
                    "E) İHK; anaplastik tümörlerde köken tayini, primer odak tespiti ve hedefe yönelik tedavi seçiminde temel rol oynar."
                ],
                "correctAnswer": 2,
                "explanation": "C seçeneği yanlıştır çünkü Östrojen Reseptörü (ER), Progesteron Reseptörü (PR), Ki-67 ve TTF-1 gibi moleküller transkripsiyon faktörü ve nükleer reseptör oldukları için MUTLAK NÜKLEER boyanma vermek zorundadır; sitoplazmik veya membranöz boyanmaları artefakt kabul edilir. Membranöz boyanma HER2, CD20 gibi yüzey reseptörlerine özgüdür. A, B, D ve E seçenekleri doğrudur."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Anaplastik ve Kötü Diferansiye Tümörlerde İHK Köken Paneli",
        "subtitle": "Sitokeratin, Vimentin, CD45 (LCA), S100/SOX10 ve Kas Belirteçleri",
        "synthesisNarrative": "İndiferansiye büyük hücreli tümörlerde köken tayininde Sitokeratin karsinomu, CD45 lenfomayı, S100/SOX10 malign melanomu, Vimentin ve Desmin ise mezenkimal/kas tümörlerini tanımlar.",
        "content": """Rutin patoloji pratiğinde en zorlu senaryolardan biri; ışık mikroskobu altında hiçbir glandüler yapı, keratinizasyon, lenfoid folikül veya hücreler arası köprü göstermeyen; aşırı atipik, iri nükleuslu büyük hücreli indiferansiye/anaplastik malign neoplazm tablosudur. Bu aşamada H&E boyası kökeni belirlemekte yetersiz kalır. Patolog, hastanın tedavisini (kemoterapi mi, radikal cerrahi mi, radyoterapi mi) tamamen değiştirecek olan histogenetik kökeni aydınlatmak için dörtlü temel İHK tarama panelini devreye sokar.

Dörtlü Temel İHK Tarama Paneli:
1) Karsinomlar (Epitel Dokusu Kökenli):
- Belirteç: Sitokeratin (CK / Cytokeratin). Epitel hücrelerinin temel sitoskeletal intermediyer filamentidir.
- Rutinde Pan-sitokeratin kokteylleri (AE1/AE3, CK8/18) kullanılır. Güçlü sitoplazmik boyanma tümörün karsinom (veya mezotelyoma) olduğunu kesinleştirir.
2) Sarkomlar (Mezenkimal Doku Kökenli):
- Belirteç: Vimentin. Mezenkimal hücrelerin (bağ dokusu, endotel, fibroblast, düz kas) intermediyer filamentidir.
- Tanısal Kural: Vimentin tek başına spesifik bir sarkom kanıtı değildir; çünkü bazı karsinomlar ve lenfomalar da vimentin eksprese edebilir. Ancak Sitokeratin, CD45 ve S100 tamamen negatifken tek başına güçlü vimentin pozitifliği mezenkimal kökeni (sarkom) kuvvetle destekler.
3) Lenfomalar (Hematolenfoid Doku Kökenli):
- Belirteç: CD45 (LCA - Leukocyte Common Antigen / Lökosit Ortak Antijeni). Hematopoetik kökenli tüm lökositlerin yüzeyinde bulunur.
- Anaplastik büyük hücreli bir lezyonda CD45 pozitifliği saptanması karsinom ve sarkom olasılıklarını dışlayarak tanıyı Malign Lenfoma'ya yönlendirir. Ardından B hücreli lenfoma için CD20, T hücreli lenfoma için CD3 uygulanır.
4) Malign Melanom (Nöral Krest Kökenli):
- Belirteçler: S100, SOX10, HMB-45 ve Melan-A (MART-1).
- Klinik ve Patolojik Tuzak: Malign melanom onkoloji patolojisinin büyük taklitçisidir (the great mimicker); mikroskop altında karsinom gibi epitelyoid, sarkom gibi iğsi veya lenfoma gibi yuvarlak küçük hücreli morfoloji gösterebilir. S100 son derece duyarlı bir tarama belirtecidir; SOX10 ise hem duyarlılığı hem özgüllüğü en yüksek nükleer belirteçtir. HMB-45 ve Melan-A melanozomlara özgül sitoplazmik belirteçlerdir. Melanomda Sitokeratin ve CD45 negatiftir.

Kas Diferansiasyonu Gösteren Tümörler:
Eğer tümör sarkom şüphesindeyse miyositer belirteçler eklenir:
- Desmin: Hem düz kas hem de çizgili kas hücrelerinde bulunan evrensel miyositer intermediyer filamenttir.
- Düz Kas Aktini (SMA): Düz kas tümörlerinde (leiomyom/leiomyosarkom) pozitiftir.
- Miyogenin ve MyoD1: İskelet kası diferansiasyonunun en özgül nükleer belirteçleridir; Rabdomyosarkom tanısında altın standarttır.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Anaplastik indiferansiye bir tümörde Sitokeratin (+) ise Karsinom, CD45 (LCA) (+) ise Lenfoma, S100 ve SOX10 (+) ise Malign Melanom, Desmin (+) ise Kas Kökenli Tümör (çizgili kasta Miyogenin/MyoD1) düşünülür.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "İndiferansiye malign tümör morfolojisi gösteren bir kitleden yapılan biyopside lenfoid neoplazm şüphesini doğrulamak amacıyla kullanılan lökosit ortak antijeni hangisidir? (CD45 / LCA).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Sitokeratin karsinomların, Vimentin mezenkimal doku/sarkomların temel belirtecidir.",
            "CD45 (LCA) pozitifliği tümörün hematolenfoid (lenfoma) kökenli olduğunu kanıtlar.",
            "Malign melanomda S100 ve SOX10 pozitifken, karsinom belirteci sitokeratin negatiftir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-016",
            "question": "Işık mikroskobunda hiçbir diferansiasyon göstermeyen 'büyük hücreli indiferansiye/anaplastik malign tümör' olgusunda uygulanan İHK köken paneli ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Sitokeratin pozitifliği tümörün mezenkimal kökenli bir sarkom olduğunu kanıtlar.",
                "B) CD45 (LCA - Lökosit Ortak Antijeni) pozitifliği lezyonun hematolenfoid kökenli bir malign lenfoma olduğunu gösterir.",
                "C) Vimentin pozitifliği yalnızca karsinomlarda görülür, sarkomlarda kesinlikle negatiftir.",
                "D) S100 ve SOX10 pozitifliği karsinom tanısını doğrulamada en özgül belirteç ikilisidir.",
                "E) Çizgili kas diferansiasyonunu (rabdomyosarkom) doğrulamada nükleer Miyogenin negatif olmalıdır."
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. İndiferansiye bir neoplazmda CD45 (LCA - Leukocyte Common Antigen) pozitifliği tümörün lenfoma olduğunu kanıtlar. A yanlıştır (Sitokeratin epitelyal karsinom belirtecidir). C yanlıştır (Vimentin mezenkimal doku/sarkom belirtecidir). D yanlıştır (S100 ve SOX10 malign melanom belirteçleridir). E yanlıştır (Miyogenin çizgili kas diferansiasyonu için kuvvetli pozitif olmalıdır)."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-016",
                "question": "Işık mikroskobunda hiçbir diferansiasyon göstermeyen 'büyük hücreli indiferansiye/anaplastik malign tümör' olgusunda uygulanan İHK köken paneli ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "options": [
                    "A) Sitokeratin pozitifliği tümörün mezenkimal kökenli bir sarkom olduğunu kanıtlar.",
                    "B) CD45 (LCA - Lökosit Ortak Antijeni) pozitifliği lezyonun hematolenfoid kökenli bir malign lenfoma olduğunu gösterir.",
                    "C) Vimentin pozitifliği yalnızca karsinomlarda görülür, sarkomlarda kesinlikle negatiftir.",
                    "D) S100 ve SOX10 pozitifliği karsinom tanısını doğrulamada en özgül belirteç ikilisidir.",
                    "E) Çizgili kas diferansiasyonunu (rabdomyosarkom) doğrulamada nükleer Miyogenin negatif olmalıdır."
                ],
                "correctAnswer": 1,
                "explanation": "B seçeneği doğrudur. İndiferansiye bir neoplazmda CD45 (LCA - Leukocyte Common Antigen) pozitifliği tümörün lenfoma olduğunu kanıtlar. A yanlıştır (Sitokeratin epitelyal karsinom belirtecidir). C yanlıştır (Vimentin mezenkimal doku/sarkom belirtecidir). D yanlıştır (S100 ve SOX10 malign melanom belirteçleridir). E yanlıştır (Miyogenin çizgili kas diferansiasyonu için kuvvetli pozitif olmalıdır)."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Nöroendokrin ve Vasküler Tümörlerin İmmünohistokimyasal Belirteçleri",
        "subtitle": "Kromogranin A, Sinaptofizin, CD56, CD31, CD34 ve Faktör VIII",
        "synthesisNarrative": "Nöroendokrin tümörlerin tanısında Kromogranin A en özgül, Sinaptofizin ise en duyarlı belirteçtir; vasküler endotelyal tümörlerde ise CD31 (PECAM-1) altın standarttır.",
        "content": """Özel doku diferansiasyonu gösteren neoplazmların tanısında organ ve fonksiyon spesifik immünohistokimyasal belirteç panelleri devreye girer. Bu gruplar arasında klinik pratikte en sık karşılaşılan iki kritik kategori nöroendokrin neoplazmlar ve vasküler endotelyal tümörlerdir.

1) Nöroendokrin Tümörler ve Karsinomlar:
Nöroendokrin hücreler; nörosekretuar granüllerinde biyolojik aminler ve polipeptit hormonlar depolayan, organoid mimari ve tuz-biber kromatin paterni sergileyen neoplazmlardır (akciğer karsinoidleri, küçük hücreli akciğer karsinomu - SCLC, gastrointestinal NET, feokromositoma ve medüller tiroid karsinomu).
- Sinaptofizin (Synaptophysin): Presinaptik küçük veziküllerin transmembran glikoproteinidir. Nöroendokrin diferansiasyonda son derece duyarlı (sensitif) bir sitoplazmik belirteçtir; hemen tüm nöroendokrin tümörlerde diffüz ve kuvvetli pozitifleşir.
- Kromogranin A (Chromogranin A): Nörosekretuar yoğun merkezli granüllerin matriksinde yer alan proteindir. Nöroendokrin diferansiasyon için ÖZGÜLLÜĞÜ (spesifisitesi) EN YÜKSEK İHK belirtecidir. Karsinoid tümörlerde çok güçlü boyanırken; granül sayısı azalan agresif tümörlerde (SCLC) boyanma fokal olabilir.
- CD56 (NCAM): Nöroendokrin tümörlerde oldukça hassastır ancak miyelom ve bazı sarkomlarda da boyanabildiğinden panelle birlikte yorumlanır.

2) Vasküler ve Endotelyal Tümörler:
Kan veya lenf damarlarının endotel hücrelerinden köken alan neoplazmlardır (Hemanjiyom, Kaposi Sarkomu ve Anjiyosarkom).
- CD31 (PECAM-1): Vasküler endotel hücreleri için EN DUYARLI VE EN ÖZGÜL İHK belirtecidir. Hücre membranında yoğun boyanma verir; anaplastik vasküler neoplazmların tanısında altın standarttır.
- CD34: Endotel hücreleri, vasküler neoplazmlar ve hematopoetik kök hücrelerde pozitiftir. Damarsal tümörlerin yanı sıra Soliter Fibröz Tümör (SFT) ve Gastrointestinal Stromal Tümörlerde (GIST) de kuvvetli pozitiftir.
- Faktör VIII İlişkili Antijen (vWF): Endotel hücrelerinin Weibel-Palade cisimciklerindeki glikoproteindir; diferansiye vasküler lezyonlarda çok özgül olmakla birlikte anaplastik anjiyosarkomlarda kaybolabilir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Nöroendokrin tümörlerin tanısında özgüllüğü en yüksek belirteç Kromogranin A'dır; presinaptik vezikül proteini olan Sinaptofizin ise en duyarlı belirteçtir. Vasküler endotelyal tümörlerde en duyarlı ve özgül belirteç CD31'dir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Küçük hücreli akciğer karsinoması veya gastrointestinal karsinoid tümör şüphesi olan bir olguda nörosekretuar granül matriks proteini olan ve nöroendokrin diferansiasyon için özgüllüğü en yüksek kabul edilen belirteç hangisidir? (Kromogranin A).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Kromogranin A nörosekretuar granül proteini olup nöroendokrin ayrımda en yüksek özgüllüğe sahiptir.",
            "Sinaptofizin presinaptik veziküllerde bulunur ve nöroendokrin lezyonlarda yüksek duyarlılık gösterir.",
            "CD31 (PECAM-1) endotel kökenli vasküler neoplazmların en duyarlı ve özgül belirtecidir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-017",
            "question": "Nöroendokrin ve vasküler tümörlerin immünohistokimyasal belirteçleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Kromogranin A, nörosekretuar granül proteini olup nöroendokrin diferansiasyon için özgüllüğü (spesifisitesi) en yüksek İHK belirtecidir.",
                "B) Sinaptofizin presinaptik küçük vezikül proteini olup nöroendokrin tümörlerin tanısında son derece duyarlı bir sitoplazmik belirteçtir.",
                "C) CD31 (PECAM-1), vasküler endotel hücreleri ve damarsal tümörler (anjiyosarkom) için en duyarlı ve özgül belirteçtir.",
                "D) CD34 sadece vasküler endotelde boyanır; stromal tümörlerde (GIST) veya soliter fibröz tümörde asla pozitifleşmez.",
                "E) Küçük hücreli akciğer karsinoması (SCLC) ve karsinoid tümörler Sinaptofizin ve Kromogranin A pozitifliği gösterir."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü CD34 vasküler endotelin yanı sıra hematopoetik kök hücrelerde, Soliter Fibröz Tümörde (SFT), Dermatofibrosarkoma Protuberans'ta (DFSP) ve Gastrointestinal Stromal Tümörlerde (GIST) de güçlü ve diffüz biçimde pozitiftir. A, B, C ve E seçenekleri doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-017",
                "question": "Nöroendokrin ve vasküler tümörlerin immünohistokimyasal belirteçleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Kromogranin A, nörosekretuar granül proteini olup nöroendokrin diferansiasyon için özgüllüğü (spesifisitesi) en yüksek İHK belirtecidir.",
                    "B) Sinaptofizin presinaptik küçük vezikül proteini olup nöroendokrin tümörlerin tanısında son derece duyarlı bir sitoplazmik belirteçtir.",
                    "C) CD31 (PECAM-1), vasküler endotel hücreleri ve damarsal tümörler (anjiyosarkom) için en duyarlı ve özgül belirteçtir.",
                    "D) CD34 sadece vasküler endotelde boyanır; stromal tümörlerde (GIST) veya soliter fibröz tümörde asla pozitifleşmez.",
                    "E) Küçük hücreli akciğer karsinoması (SCLC) ve karsinoid tümörler Sinaptofizin ve Kromogranin A pozitifliği gösterir."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü CD34 vasküler endotelin yanı sıra hematopoetik kök hücrelerde, Soliter Fibröz Tümörde (SFT), Dermatofibrosarkoma Protuberans'ta (DFSP) ve Gastrointestinal Stromal Tümörlerde (GIST) de güçlü ve diffüz biçimde pozitiftir. A, B, C ve E seçenekleri doğrudur."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Metastatik Karsinomlarda Primer Odak Tayini İçin İHK Belirteçleri",
        "subtitle": "TTF-1, PSA/NKX3.1, CDX2, GATA3 ve WT1 ile Organ Spesifik Haritalama",
        "synthesisNarrative": "Metastatik adenokarsinomlarda primer odağın belirlenmesinde nükleer transkripsiyon faktörleri esastır: Akciğerde TTF-1/Napsin A, kolonda CDX2, prostatta NKX3.1/PSA, memede GATA3, overde WT1 kullanılır.",
        "content": """Onkolojik cerrahi ve patolojide en sık karşılaşılan klinik tablolardan biri 'Bilinmeyen Primer Odaklı Metastatik Karsinom' (CUP - Carcinoma of Unknown Primary) antitesidir. Karaciğerde, vertebral kemiklerde, beyinde veya supraklaviküler lenf nodunda tespit edilen bir adenokarsinom metastazının asıl çıktığı ana organı bulmak; hastaya verilecek kemoterapi rejimini ve hedefe yönelik akıllı ilaç protokolünü belirleyen tek anahtardır. Patolog bu ayrımı yapabilmek için organ spesifik transkripsiyon faktörleri ve özgül protein panellerini kullanır.

Organ Spesifik İHK Belirteç Haritası:
1) Akciğer Adenokarsinomu:
- TTF-1 (Tiroid Transkripsiyon Faktörü-1): Akciğer epitelinde (özellikle tip II pnömositler ve Clara hücreleri) ve tiroid folliküler hücrelerinde nükleer ekspresyon gösterir. Akciğer adenokarsinomlarının %75-80'inde güçlü nükleer pozitiflik verir.
- Napsin A: Akciğer adenokarsinomuna özgül sitoplazmik aspartik proteinazdır. TTF-1 (+) / Napsin A (+) profili primer akciğer adenokarsinomunun kesin kanıtıdır.
2) Tiroid Karsinomları:
- TTF-1 (+) nükleer boyanma verir; ancak akciğerden farkı Tiroglobulin ve PAX8'in pozitif, Napsin A'nın negatif olmasıdır. Medüller tiroid karsinomunda ise kalsitonin pozitiftir.
3) Prostat Adenokarsinomu:
- PSA (Prostat Spesifik Antijen): Prostat asiner epiteli tarafından salgılanır, sitoplazmik pozitiftir.
- NKX3.1: Prostat epitelinin gelişimini yöneten androjen bağımlı nükleer transkripsiyon faktörüdür; kötü diferansiye karsinomlarda dahi pozitif kalarak prostat kökenini doğrular. Yaşlı bir erkekte kemikte osteoblastik metastaz görüldüğünde ilk taranacak ikilidir.
4) Kolorektal ve Gastrointestinal Karsinomlar:
- CDX2: İntestinal epitelin morfogenezini kontrol eden nükleer homeobox transkripsiyon faktörüdür. Kolorektal adenokarsinomların neredeyse tamamında diffüz nükleer pozitiftir.
- Sitokeratin Profili: CK20 (+) / CK7 (-) profili kolorektal adenokarsinom için son derece tipiktir.
5) Meme Karsinomu:
- GATA3: Meme glandüler epitelinde bulunan nükleer transkripsiyon faktörüdür.
- Mammaglobin ve GCDFP-15 (Gross Kistik Hastalık Sıvı Proteini): Meme kökeni için özgül sitoplazmik belirteçlerdir.
6) Ürotelyal (Mesane) Karsinom:
- GATA3 (+), p63 (+) ve Üroplakin (+) ekspresyonu sergiler.
7) Over Yüksek Dereceli Seröz Karsinomu:
- WT1 (Wilms Tümörü 1): Nükleer pozitiflik verir; over seröz tümörlerini diğer over karsinomlarından ve gastrointestinal metastazlardan ayıran temel belirteçtir. PAX8 ve CA-125 pozitifliği eşlik eder.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Karaciğerde metastatik adenokarsinomda nükleer CDX2 pozitifliği kolorektal kökeni kanıtlar. Kemik metastazı olan erkekte NKX3.1/PSA prostatı; akciğer kitlelerinde TTF-1 ve Napsin A akciğer adenokarsinomunu; over seröz karsinomunda WT1 primer odağı gösterir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Karaciğer biyopsisinde metastatik adenokarsinom saptanan bir hastada tümör hücrelerinde nükleer CDX2 ve sitoplazmik CK20 pozitifliği, CK7 negatifliği saptanması durumunda primer tümör odağı nerededir? (Kolon ve rektum / Gastrointestinal sistem).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "TTF-1 ve Napsin A akciğer adenokarsinomu için yüksek özgüllüğe sahiptir.",
            "CDX2 nükleer boyanması kolorektal adenokarsinomun en temel primer belirtecidir.",
            "Kemik metastazında PSA ve nükleer NKX3.1 prostat karsinomu tanısını koydurur."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-018",
            "question": "Bilinmeyen primer odaklı metastatik karsinomlarda primer organ odağını belirlemek için kullanılan İHK belirteçleri ile ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Nükleer CDX2 pozitifliği — Gastrointestinal sistem / Kolorektal adenokarsinom",
                "B) Nükleer TTF-1 ve sitoplazmik Napsin A pozitifliği — Akciğer adenokarsinomu",
                "C) PSA ve nükleer NKX3.1 pozitifliği — Prostat adenokarsinomu",
                "D) Nükleer GATA3 pozitifliği — Meme ve ürotelyal (mesane) karsinomları",
                "E) Nükleer WT1 pozitifliği — Mide taşlı yüzük hücreli karsinomu"
            ],
            "correctAnswer": 4,
            "explanation": "E seçeneği yanlıştır çünkü WT1 (Wilms Tümörü 1) nükleer pozitifliği Over Yüksek Dereceli Seröz Karsinomu ve malign mezotelyomada pozitiftir; mide taşlı yüzük hücreli karsinomunda WT1 negatiftir. A, B, C ve D seçeneklerindeki primer odak-İHK belirteç eşleştirmeleri tamamen doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-018",
                "question": "Bilinmeyen primer odaklı metastatik karsinomlarda primer organ odağını belirlemek için kullanılan İHK belirteçleri ile ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Nükleer CDX2 pozitifliği — Gastrointestinal sistem / Kolorektal adenokarsinom",
                    "B) Nükleer TTF-1 ve sitoplazmik Napsin A pozitifliği — Akciğer adenokarsinomu",
                    "C) PSA ve nükleer NKX3.1 pozitifliği — Prostat adenokarsinomu",
                    "D) Nükleer GATA3 pozitifliği — Meme ve ürotelyal (mesane) karsinomları",
                    "E) Nükleer WT1 pozitifliği — Mide taşlı yüzük hücreli karsinomu"
                ],
                "correctAnswer": 4,
                "explanation": "E seçeneği yanlıştır çünkü WT1 (Wilms Tümörü 1) nükleer pozitifliği Over Yüksek Dereceli Seröz Karsinomu ve malign mezotelyomada pozitiftir; mide taşlı yüzük hücreli karsinomunda WT1 negatiftir. A, B, C ve D seçeneklerindeki primer odak-İHK belirteç eşleştirmeleri tamamen doğrudur."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Terapötik ve Prognostik İmmünohistokimyasal Belirteçler",
        "subtitle": "Meme Karsinomunda ER, PR, HER2/neu Değerlendirmesi ve Ki-67 Proliferasyon İndeksi",
        "synthesisNarrative": "Meme kanserinde ER ve PR nükleer boyanarak hormonal tedaviye yanıtı; HER2 membranöz boyanarak trastuzumab hedefini predikte eder; Ki-67 proliferasyon indeksi ise agresifliği yansıtır.",
        "content": """Modern patolojide immünohistokimya, yalnızca 'Bu tümör nedir ve nereden çıkmıştır?' sorusuna yanıt vermekle yetinmez; 'Bu tümör hangi ilaca yanıt verir ve hastanın klinik seyri nasıl olacaktır?' sorularının cevabını sağlar. Bu bağlamda iki temel kavram ayrışır:
- Prognostik Belirteç: Hastaya hiçbir tedavi verilmese dahi hastalığın doğal biyolojik saldırganlığını, nüks etme olasılığını ve genel sağkalımı tahmin eden parametredir (örneğin Ki-67 proliferasyon indeksi).
- Prediktif (Terapötik) Belirteç: Hastanın spesifik bir hedefe yönelik ilaçtan, hormonoterapiden veya biyolojik ajandan fayda görüp görmeyeceğini öngören parametredir.

Meme Karsinomunda Standart Dörtlü İHK Paneli:
1) Östrojen Reseptörü (ER) ve Progesteron Reseptörü (PR):
- Nükleer transkripsiyon faktörleridir; boyanmanın mutlaka nükleusta olması gerekir (Allred skoru ile pozitif hücre yüzdesi ve boyanma şiddeti değerlendirilir).
- Prediktif Önemi: ER ve/veya PR pozitifliği (>%1 nükleer boyanma), tümörün endokrin tedavilere (Tamoksifen, Aromataz inhibitörleri: Anastrozol, Letrozol) yanıt vereceğinin kesin prediktif kanıtıdır. Aynı zamanda hormon pozitif tümörler daha iyi diferansiye olup daha iyi prognoza sahiptir.
2) HER2/neu (ERBB2 - İnsan Epidermal Büyüme Faktörü Reseptörü 2):
- Hücre membranında tirozin kinaz aktivitesine sahip büyüme faktörü reseptörüdür.
- İHK Skorlama Sistemi (Membranöz Boyanma):
  - Skor 0: Hiç membranöz boyanma yok veya <%10 hücrede zayıf boyanma (Negatif).
  - Skor 1+: Hücrelerin >%10'unda silik/kesintili membranöz boyanma (Negatif).
  - Skor 2+: Hücrelerin >%10'unda zayıf-orta şiddette çembersel membranöz boyanma (ŞÜPHELİ / EQUIVOCAL). Bu olgularda Trastuzumab verilip verilemeyeceğini belirlemek için mutlaka FISH (veya SISH/CISH) yöntemiyle gen amplifikasyonu aranmalıdır!
  - Skor 3+: İnvaziv tümör hücrelerinin >%10'unda kesintisiz, kuvvetli, tam çembersel membranöz boyanma (POZİTİF).
- Terapötik Önemi: HER2 pozitifliği (İHK 3+ veya FISH amplifiye) tümörün agresifliğini gösterir; ancak anti-HER2 monoklonal antikor tedavisine (Trastuzumab / Herceptin, Pertuzumab) doğrudan aday olduğunu gösterir.
3) Ki-67 Proliferasyon İndeksi:
- Hücre siklusunun aktif fazlarında (G1, S, G2 ve mitoz) eksprese edilen, ancak istirahat fazında (G0) bulunmayan bir nükleer protein antijenidir.
- Nükleer pozitiflik gösteren hücrelerin yüzdesi hesaplanır. Yüksek Ki-67 indeksi (>%20), tümörün hızlı bölündüğünü, agresif seyredeceğini ve klasik sitotoksik kemoterapiye daha duyarlı olduğunu gösterir. Meme kanserinde düşük riskli Lüminal A ile agresif Lüminal B alt tiplerinin ayırımında temel kriterdir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Meme karsinomunda HER2/neu İHK skoru 2+ (şüpheli) çıktığında trastuzumab tedavisi kararı verilmeden önce mutlaka FISH testi ile gen amplifikasyonu teyit edilmelidir. ER/PR nükleer, HER2 ise membranöz boyanmalıdır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Meme karsinomu tanısı alan bir hastanın patoloji raporunda HER2/neu protein ekspresyonunun immünohistokimya ile 3+ pozitif bulunması, hastada aşağıdaki tedavilerden hangisinin endike olduğunu gösterir? (Trastuzumab / Anti-HER2 monoklonal antikor).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "ER ve PR nükleer boyanarak tamoksifen ve aromataz inhibitörü yanıtını predikte eder.",
            "HER2 membranöz boyanır; 2+ şüpheli skorda FISH ile gen amplifikasyonu zorunludur.",
            "Ki-67 nükleer proliferasyon belirteci olup Lüminal A ve B alt tiplerini ayırır."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-019",
            "question": "Meme karsinomunda terapötik ve prognostik İHK belirteçlerinin değerlendirilmesi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Östrojen (ER) ve Progesteron (PR) reseptörleri nükleer boyanır ve hormonoterapiden (tamoksifen) fayda göreceğini predikte eder.",
                "B) HER2/neu immünohistokimyasal olarak membranöz boyanma paternine göre 0'dan 3+'a kadar skorlanır.",
                "C) HER2 İHK skoru 2+ (şüpheli/equivocal) bulunan olgularda anti-HER2 tedavi kararı öncesinde mutlaka FISH ile gen amplifikasyonu aranmalıdır.",
                "D) Ki-67 proliferasyon indeksinin yüksek olması tümörün agresifliğini gösterirken sitotoksik kemoterapiye duyarlılığı artırır.",
                "E) HER2 İHK skoru 1+ olan olgular doğrudan trastuzumab tedavisi için kesin pozitif kabul edilir."
            ],
            "correctAnswer": 4,
            "explanation": "E seçeneği yanlıştır çünkü HER2 İHK skoru 0 ve 1+ olan olgular kesinlikle NEGATİF kabul edilir ve trastuzumab verilmez. Yalnızca İHK skoru 3+ olanlar veya İHK 2+ olup FISH ile gen amplifikasyonu kanıtlanan olgular anti-HER2 tedaviden fayda görür. A, B, C ve D seçenekleri doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-019",
                "question": "Meme karsinomunda terapötik ve prognostik İHK belirteçlerinin değerlendirilmesi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Östrojen (ER) ve Progesteron (PR) reseptörleri nükleer boyanır ve hormonoterapiden (tamoksifen) fayda göreceğini predikte eder.",
                    "B) HER2/neu immünohistokimyasal olarak membranöz boyanma paternine göre 0'dan 3+'a kadar skorlanır.",
                    "C) HER2 İHK skoru 2+ (şüpheli/equivocal) bulunan olgularda anti-HER2 tedavi kararı öncesinde mutlaka FISH ile gen amplifikasyonu aranmalıdır.",
                    "D) Ki-67 proliferasyon indeksinin yüksek olması tümörün agresifliğini gösterirken sitotoksik kemoterapiye duyarlılığı artırır.",
                    "E) HER2 İHK skoru 1+ olan olgular doğrudan trastuzumab tedavisi için kesin pozitif kabul edilir."
                ],
                "correctAnswer": 4,
                "explanation": "E seçeneği yanlıştır çünkü HER2 İHK skoru 0 ve 1+ olan olgular kesinlikle NEGATİF kabul edilir ve trastuzumab verilmez. Yalnızca İHK skoru 3+ olanlar veya İHK 2+ olup FISH ile gen amplifikasyonu kanıtlanan olgular anti-HER2 tedaviden fayda görür. A, B, C ve D seçenekleri doğrudur."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Serum Tümör Belirteçleri: Genel İlkeler, Sınırlamalar ve Doğru Klinik Kullanım",
        "subtitle": "Biyobelirteç Spektrumu, Tarama Tuzakları, Yalancı Pozitiflikler ve Nüks Takibi",
        "synthesisNarrative": "Serum tümör belirteçleri tek başına kesin tanı koyduramaz ve genel popülasyonda tarama için uygun değildir; temel kullanım alanları tedavi yanıtının izlenmesi ve nüksün erken yakalanmasıdır.",
        "content": """Serum tümör belirteçleri (tümör biyobelirteçleri); neoplastik hücrelerin kendisi tarafından üretilerek doğrudan dolaşıma salınan veya tümörün varlığına yanıt olarak konak dokuları tarafından sentezlenen; kanda, serumda veya diğer vücut sıvılarında biyokimyasal ve immünolojik yöntemlerle kantitatif olarak ölçülebilen moleküllerdir (enzimler, onkofetal antijenler, glikoproteinler, hormonlar).

Onkolojik Laboratuvarın En Temel Klinik Aksiyomu:
Serum tümör belirteçleri tek başına KESİNLİKLE kanser tanısı koyduramaz! Kanser tanısının tartışmasız altın standardı histopatolojik incelemedir. İstisnai bazı klinik tablolar (örneğin sirotik bir hastada karaciğerde tipik lezyonla birlikte AFP'nin >400 ng/mL olması veya genç erkekte retroperitoneal kitleyle birlikte aşırı hCG/AFP yüksekliği) dışında hiçbir tümör belirteci doku biyopsisinin yerini alamaz.

Tümör Belirteçlerinin Sınırlılıkları ve Tarama Tuzakları:
Genel asemptomatik popülasyonda kanser tarama testi olarak kullanılamamalarının arkasında iki temel biyolojik sınırlılık yatar:
1) Düşük Duyarlılık (Sensitivity): Tümör belirteçlerinin kan düzeyleri tümörün kitlesel hacmi ile doğrudan ilişkilidir. Kanserlerin erken evrelerinde (Evre I-II) tümör yükü henüz çok küçük olduğundan, kandaki belirteç seviyesi sıklıkla normal referans aralıklarında kalır. Yani kanser mevcut olduğu halde test negatiftir (yalancı negatiflik).
2) Düşük Özgüllük (Specificity): Tümör belirteçlerinin neredeyse hiçbiri sadece kanser hücrelerine özgü değildir. Benign enflamatuar durumlarda, infeksiyonlarda veya organ yetmezliklerinde belirteç düzeyleri belirgin biçimde yükselebilir (yalancı pozitiflik). Örneğin PSA benign prostat hiperplazisinde (BPH) ve prostatitte; CEA sigara içenlerde ve sirozda; CA-125 endometrioziste ve pelvik enflamasyonda yükselebilir.

Serum Tümör Belirteçlerinin Gerçek ve Kanıtlanmış Klinik Kullanım Alanları:
1) Tedaviye Verilen Yanıtın İzlenmesi: Cerrahi rezeksiyon veya kemoterapi öncesinde kanda yüksek bulunan belirtecin, ameliyat sonrasında biyolojik yarı ömrüne uygun şekilde hızla taban değere inmesi veya sıfırlanması cerrahinin küratif başarısını ve tümörün tamamen temizlendiğini gösterir.
2) Nüksün (Relaps) ve Metastazın Erken Saptanması: Tedavi sonrası remisyona giren ve belirteç düzeyi normale inen bir hastanın rutin poliklinik takibinde; belirteç düzeyinin aylar sonra yeniden istikrarlı biçimde yükselmeye başlaması, klinik semptomlar veya BT/MR bulguları ortaya çıkmadan aylar önce mikroskobik nüksün geliştiğini haber verir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Serum tümör belirteçleri düşük duyarlılık ve düşük özgüllük nedeniyle asemptomatik popülasyonda kanser taraması ve kesin tanı için uygun değildir! En temel ve değerli kullanım alanları tedaviye yanıtın monitorizasyonu ve relaps/nükslerin erken saptanmasıdır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Kanser hastalarında serum tümör belirteçlerinin ölçülmesinin onkoloji pratiğindeki en güvenilir ve temel endikasyonu aşağıdakilerden hangisidir? (Tedaviye yanıtın izlenmesi ve relaps/nüksün erken saptanması).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Serum tümör belirteçleri tek başına histopatolojik biyopsi olmaksızın kesin tanı koyduramaz.",
            "Benign durumlarda yükselebilmeleri (düşük özgüllük) tarama testi olarak kullanımlarını kısıtlar.",
            "Başarılı cerrahi sonrası sıfırlanması ve takipte tekrar yükselmesi nüksün en erken bulgusudur."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-020",
            "question": "Serum tümör belirteçlerinin genel özellikleri, biyolojik sınırlamaları ve klinik kullanım alanları ile ilgili aşağıdaki ifadelerden hangisi KESİNLİKLE DOĞRUDUR?",
            "options": [
                "A) Serum tümör belirteçleri yüksek duyarlılık ve özgüllükleri nedeniyle asemptomatik genel popülasyonda kanser tarama testi olarak rutin uygulanmalıdır.",
                "B) Kanda bir tümör belirtecinin yüksek saptanması doku biyopsisi yapılmaksızın tek başına kesin kanser tanısı koydurur.",
                "C) Tümör belirteçlerinin en değerli klinik kullanım alanı, cerrahi/kemoterapiye yanıtın izlenmesi ve relaps/nüksün erken saptanmasıdır.",
                "D) Benign enflamatuar durumlarda tümör belirteçleri kesinlikle yükselmez, sadece malignitelerde artar.",
                "E) Erken evre (Evre I) tümörlerde kitle boyutu küçük olsa dahi serum tümör belirteçleri daima referans aralığının çok üzerindedir."
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği kesinlikle doğrudur. Serum tümör belirteçlerinin onkolojideki en temel ve kanıtlanmış kullanım alanı; cerrahi rezeksiyon sonrası düzeyin tabana inmesiyle tedavi yanıtının takibi ve remisyondaki hastada tekrar yükselmesiyle nüksün klinik/radyolojik bulgulardan aylar önce erken saptanmasıdır. A, B, D ve E seçenekleri yanlıştır (düşük özgüllük ve duyarlılık nedeniyle genel tarama ve tek başına kesin tanı testi olarak kullanılamazlar; benign durumlarda da yükselebilirler; erken evrede normal kalabilirler)."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-020",
                "question": "Serum tümör belirteçlerinin genel özellikleri, biyolojik sınırlamaları ve klinik kullanım alanları ile ilgili aşağıdaki ifadelerden hangisi KESİNLİKLE DOĞRUDUR?",
                "options": [
                    "A) Serum tümör belirteçleri yüksek duyarlılık ve özgüllükleri nedeniyle asemptomatik genel popülasyonda kanser tarama testi olarak rutin uygulanmalıdır.",
                    "B) Kanda bir tümör belirtecinin yüksek saptanması doku biyopsisi yapılmaksızın tek başına kesin kanser tanısı koydurur.",
                    "C) Tümör belirteçlerinin en değerli klinik kullanım alanı, cerrahi/kemoterapiye yanıtın izlenmesi ve relaps/nüksün erken saptanmasıdır.",
                    "D) Benign enflamatuar durumlarda tümör belirteçleri kesinlikle yükselmez, sadece malignitelerde artar.",
                    "E) Erken evre (Evre I) tümörlerde kitle boyutu küçük olsa dahi serum tümör belirteçleri daima referans aralığının çok üzerindedir."
                ],
                "correctAnswer": 2,
                "explanation": "C seçeneği kesinlikle doğrudur. Serum tümör belirteçlerinin onkolojideki en temel ve kanıtlanmış kullanım alanı; cerrahi rezeksiyon sonrası düzeyin tabana inmesiyle tedavi yanıtının takibi ve remisyondaki hastada tekrar yükselmesiyle nüksün klinik/radyolojik bulgulardan aylar önce erken saptanmasıdır. A, B, D ve E seçenekleri yanlıştır (düşük özgüllük ve duyarlılık nedeniyle genel tarama ve tek başına kesin tanı testi olarak kullanılamazlar; benign durumlarda da yükselebilirler; erken evrede normal kalabilirler)."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Majör Serum Tümör Belirteçleri ve Klinik İlişkileri",
        "subtitle": "PSA, CEA, AFP, CA-125, CA 19-9, beta-hCG ve Kalsitonin Paneli",
        "synthesisNarrative": "PSA prostat, CEA kolorektal, AFP hepatosellüler karsinom ve testis yolk sac tümöründe yükselirken; seminomda AFP yükselmez; kalsitonin ise tiroid medüller karsinomunun özgül belirtecidir.",
        "content": """Klinik onkolojide spesifik organ sistemleri ve tümör tipleriyle özdeşleşmiş majör serum tümör belirteçleri şunlardır:

1) Prostat Spesifik Antijen (PSA):
Prostat duktus epitelinden salgılanan bir serin proteazdır; spermin likefaksiyonunu sağlar. Prostat adenokarsinomunda kanda belirgin yükselir. Ancak benign prostat hiperplazisi (BPH), prostatit, akut üriner retansiyon ve rektal tuşe/prostat biyopsisi sonrasında da yükselebilir. Radikal prostatektomi sonrası serum PSA düzeyinin <0,1 ng/mL düzeyine düşmesi beklenir; takiplerde PSA'nın yeniden yükselmesi 'biyokimyasal nüks'ün kesin kanıtıdır.

2) Karsinoembriyonik Antijen (CEA):
Fetal gastrointestinal dokuda sentezlenen karmaşık bir onkofetal glikoproteindir. Kolorektal adenokarsinom başta olmak üzere pankreas, mide, meme ve akciğer karsinomlarında kanda yükselir. Sigara içenlerde, sirozda, ülseratif kolitte ve kronik böbrek yetmezliğinde de yükselebilir. Kolorektal karsinom cerrahisi sonrası rekürrens ve karaciğer metastazı takibinde altın standarttır.

3) Alfa-Fetoprotein (AFP):
Fetal dönemde karaciğer ve vitellüs kesesi (yolk sac) tarafından üretilen majör plazma proteinidir (fetal albümin analoğu).
- Temel Kullanım: Hepatosellüler Karsinom (HCC) ve Testisin Non-Seminomatöz Germ Hücreli Tümörleri (özellikle Yolk Sac tümörü / vitellüs kesesi komponenti).
- Kritik Klinik Ayrım: Testisin saf Seminomalarında AFP KESİNLİKLE YÜKSELMEZ! Bir testis tümöründe AFP yüksekliği saptanırsa lezyon kesinlikle non-seminomatöz kabul edilir. Ayrıca sirotik hastalarda USG ile birlikte HCC taramasında kullanılır.

4) CA-125 (Kanser Antijeni 125):
Müllerian kanal türevlerinden köken alan epitelyal glikoproteindir. Over Epitelyal (özellikle Yüksek Dereceli Seröz) Karsinomlarının temel belirtecidir. Endometriozis, adenomyozis, pelvik enflamatuar hastalık (PID), peritonit ve gebelikte de yükselebilir. Over karsinomu cerrahisi sonrası nüks takibinde esastır.

5) CA 19-9:
Sialillenmiş Lewis kan grubu antijenidir. Pankreas Adenokarsinomu ve Safra Yolu (Kolanjiyokarsinom) karsinomlarının belirtecidir. Kolestaz, safra taşı ve akut pankreatitte de yalancı pozitiflik verebilir.

6) Beta-hCG (İnsan Koryonik Gonadotropini):
Sinsityotrofoblast hücreleri tarafından üretilen hormondur. Gestasyonel Trofoblastik Hastalıklar (Mol hidatiform, Koryokarsinom) ve Testis Germ Hücreli Tümörlerinde (koryokarsinom komponenti ve seminomaların yaklaşık %10'unda) yükselir.

7) Kalsitonin:
Tiroid bezinin parafolliküler C hücreleri tarafından sentezlenen kalsiyum düzenleyici hormondur. Tiroid Medüller Karsinomunun özgül belirtecidir. MEN 2A ve 2B sendromlu ailelerde genetik taşıyıcıların taranmasında ve tiroidektomi sonrası nüks takibinde kullanılır.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Testis germ hücreli tümörlerinde AFP yüksekliği mutlak bir non-seminomatöz (özellikle Yolk Sac) komponent göstergesidir; saf seminomalarda AFP ASLA yükselmez! Tiroid medüller karsinomunun spesifik serum belirteci ise Kalsitonin'dir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Hepatosellüler karsinom (HCC) ve testis yolk sac (vitellüs kesesi) tümörlerinin tanı ve izleminde kanda takip edilen temel onkofetal tümör belirteci hangisidir? (Alfa-fetoprotein / AFP).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "PSA prostat karsinomu, CEA ise kolorektal karsinom nüks takibinde altın standarttır.",
            "AFP hepatosellüler karsinom ve testis yolk sac tümöründe yükselir, seminomda negatiftir.",
            "Kalsitonin tiroid medüller karsinomunun, CA-125 over seröz karsinomunun belirtecidir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-021",
            "question": "Majör serum tümör belirteçleri ve ilişkili oldukları malign neoplazmlar ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) CEA (karsinoembriyonik antijen), özellikle kolorektal karsinom cerrahisi sonrası nüks takibinde altın standarttır.",
                "B) AFP (alfa-fetoprotein), hepatosellüler karsinom ve testis yolk sac (vitellüs kesesi) tümörlerinin belirtecidir.",
                "C) Testisin saf Seminomalarında kanda AFP düzeyi belirgin olarak yükselir ve tanı koydurur.",
                "D) CA-125 overin seröz karsinomlarında, CA 19-9 ise pankreas ve safra yolu adenokarsinomlarında izlem belirtecidir.",
                "E) Kalsitonin, tiroid bezinin parafolliküler C hücrelerinden kaynaklanan tiroid medüller karsinomunun özgül belirtecidir."
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği yanlıştır çünkü testis tümörlerinde saf Seminomada AFP ASLA YÜKSELMEZ! Kanda AFP yüksekliği mutlak bir non-seminomatöz germ hücreli tümör (özellikle Yolk Sac tümörü komponenti) kanıtıdır. A, B, D ve E seçenekleri doğru tümör belirteci ilişkileridir."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-021",
                "question": "Majör serum tümör belirteçleri ve ilişkili oldukları malign neoplazmlar ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) CEA (karsinoembriyonik antijen), özellikle kolorektal karsinom cerrahisi sonrası nüks takibinde altın standarttır.",
                    "B) AFP (alfa-fetoprotein), hepatosellüler karsinom ve testis yolk sac (vitellüs kesesi) tümörlerinin belirtecidir.",
                    "C) Testisin saf Seminomalarında kanda AFP düzeyi belirgin olarak yükselir ve tanı koydurur.",
                    "D) CA-125 overin seröz karsinomlarında, CA 19-9 ise pankreas ve safra yolu adenokarsinomlarında izlem belirtecidir.",
                    "E) Kalsitonin, tiroid bezinin parafolliküler C hücrelerinden kaynaklanan tiroid medüller karsinomunun özgül belirtecidir."
                ],
                "correctAnswer": 2,
                "explanation": "C seçeneği yanlıştır çünkü testis tümörlerinde saf Seminomada AFP ASLA YÜKSELMEZ! Kanda AFP yüksekliği mutlak bir non-seminomatöz germ hücreli tümör (özellikle Yolk Sac tümörü komponenti) kanıtıdır. A, B, D ve E seçenekleri doğru tümör belirteci ilişkileridir."
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Moleküler Onkoloji ve Genomik Tanı Yöntemleri",
        "subtitle": "PCR ile Klonalite Analizi, Füzyon Genleri, FISH ve Yeni Nesil Dizileme (NGS)",
        "synthesisNarrative": "Moleküler patoloji; PCR ile lenfoid klonaliteyi, FISH ile HER2 ve MYCN (double minutes/HSR) amplifikasyonlarını, NGS ile de yüzlerce kanser genini aynı anda analiz eder.",
        "content": """Modern patolojide kanserin tanısı, ışık mikroskobundaki morfolojik sınırları aşarak hücre çekirdeğindeki DNA, RNA ve kromozomal anomalilerin incelendiği moleküler onkoloji çağına evrilmiştir. Moleküler patoloji teknikleri; malignitelerin kesin tanısında, reaktif süreçlerden ayrımında, prognoz tahmininde ve hedefe yönelik akıllı ilaçların seçiminde vazgeçilmez bir rol oynar.

1) PCR ve Klonalite Analizi:
Neoplastik proliferasyonlar tek bir transforme kök hücreden köken alarak monoklonal çoğalırken; enflamasyona bağlı reaktif hiperplaziler çok sayıda hücre klonunun uyarılmasıyla poliklonal gelişir.
- Lenfoma Ayırımı: Reaktif lenfoid hiperplazi ile malign lenfoma ayrımında PCR ile immünoglobulin ağır zincir (IgH) veya T hücre reseptörü (TCR) gen yeniden düzenlenmeleri taranır. Reaktif lezyonda poliklonal smear izlenirken; lenfomada tek ve keskin bir monoklonal bant saptanır.

2) Kromozomal Translokasyonların Tespiti (RT-PCR ve FISH):
- Kronik Miyeloid Lösemi (KML): t(9;22)(q34;q11) translokasyonu sonucu BCR-ABL füzyon onkoproteini oluşur; imatinib (tirozin kinaz inhibitörü) tedavisinin hedefidir.
- Ewing Sarkomu: t(11;22)(q24;q12) translokasyonu ve EWS-FLI1 füzyon transkripti.
- Foliküler Lenfoma: t(14;18) translokasyonu ile BCL2 onkogen aktivasyonu.

3) Floresan In Situ Hibridizasyon (FISH) ile Gen Amplifikasyonları:
- Nöroblastomda MYCN Amplifikasyonu: 2p24'teki MYCN geni amplifiye olarak hücre çekirdeğinde ya kromozom dışı çift dakikalar (double minutes) ya da kromozoma entegre homojen boyanan bölgeler (HSR) olarak izlenir; çocukluk çağı nöroblastomunda evreden bağımsız en kötü prognostik göstergedir.
- Meme Kanserinde HER2 (ERBB2) Amplifikasyonu: İHK 2+ şüpheli olgularda HER2 amplifikasyonunu doğrulamada FISH altın standarttır.

4) Yeni Nesil Dizileme (NGS):
Tek bir testte yüzlerce kanser geninin (tümör panelleri) paralel dizilenmesidir; nokta mutasyonları (BRAF V600E, EGFR, KRAS, TP53), delesyonlar ve kopya sayısı değişiklikleri tek seferde taranır.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Nöroblastomda MYCN gen amplifikasyonu (double minutes veya homojen boyanan bölgeler - HSR) en güçlü kötü prognoz göstergesidir. KML'de t(9;22) BCR-ABL füzyonu, Ewing sarkomunda ise t(11;22) EWS-FLI1 füzyonu tanısal moleküler anomalidir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Çocukluk çağı nöroblastomunda prognozun son derece kötü olduğunu gösteren ve sitogenetik olarak double minutes veya homojen boyanan bölgeler (HSR) şeklinde saptanan moleküler genetik anormallik hangisidir? (MYCN onkogen amplifikasyonu).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "PCR ile IgH ve TCR gen düzenlenmelerinin monoklonal bulunması lenfoma tanısını koydurur.",
            "MYCN amplifikasyonu nöroblastomda kötü prognozun en önemli göstergesidir.",
            "Meme kanserinde İHK 2+ şüpheli olgularda HER2 gen amplifikasyonu FISH ile teyit edilir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-022",
            "question": "Kanser tanısında kullanılan moleküler onkoloji ve genomik yöntemlerle ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Reaktif lenfoid hiperplazi ile lenfoma ayrımı — PCR ile IgH veya TCR gen yeniden düzenlenmelerinin monoklonalitesinin saptanması",
                "B) Kronik miyeloid lösemi (KML) — t(9;22) BCR-ABL füzyon geni",
                "C) Ewing sarkomu — t(11;22) EWS-FLI1 füzyon transkripti",
                "D) Çocukluk çağı nöroblastomunda kötü prognoz — MYCN gen amplifikasyonu (double minutes / HSR)",
                "E) Meme kanserinde HER2 gen amplifikasyonunun doğrulanması — PCR ile JAK2 V617F mutasyon analizi"
            ],
            "correctAnswer": 4,
            "explanation": "E seçeneği yanlıştır çünkü meme kanserinde HER2 gen amplifikasyonu JAK2 mutasyonu ile değil, Floresan In Situ Hibridizasyon (FISH) yöntemi ile doğrulanır. JAK2 V617F mutasyonu ise miyeloproliferatif neoplazmların (özellikle Polisitemia Vera) belirtecidir. A, B, C ve D seçeneklerindeki moleküler anomaliler ve hastalık ilişkileri tamamen doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-022",
                "question": "Kanser tanısında kullanılan moleküler onkoloji ve genomik yöntemlerle ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Reaktif lenfoid hiperplazi ile lenfoma ayrımı — PCR ile IgH veya TCR gen yeniden düzenlenmelerinin monoklonalitesinin saptanması",
                    "B) Kronik miyeloid lösemi (KML) — t(9;22) BCR-ABL füzyon geni",
                    "C) Ewing sarkomu — t(11;22) EWS-FLI1 füzyon transkripti",
                    "D) Çocukluk çağı nöroblastomunda kötü prognoz — MYCN gen amplifikasyonu (double minutes / HSR)",
                    "E) Meme kanserinde HER2 gen amplifikasyonunun doğrulanması — PCR ile JAK2 V617F mutasyon analizi"
                ],
                "correctAnswer": 4,
                "explanation": "E seçeneği yanlıştır çünkü meme kanserinde HER2 gen amplifikasyonu JAK2 mutasyonu ile değil, Floresan In Situ Hibridizasyon (FISH) yöntemi ile doğrulanır. JAK2 V617F mutasyonu ise miyeloproliferatif neoplazmların (özellikle Polisitemia Vera) belirtecidir. A, B, C ve D seçeneklerindeki moleküler anomaliler ve hastalık ilişkileri tamamen doğrudur."
            }
        ]
    },
    {
        "slideNumber": 23,
        "title": "Terapötik Karar Vermede Moleküler Hedefler, Minimal Kalıntı Hastalık ve Sıvı Biyopsi",
        "subtitle": "Sürücü Mutasyonlar, Direnç Mekanizmaları, ctDNA ve Dinamik İzlem",
        "synthesisNarrative": "Akciğerde EGFR, kolonda KRAS yabani tip varlığı ve melanomda BRAF V600E hedefe yönelik tedaviyi belirlerken; plazma ctDNA sıvı biyopsisi direnç ve nüksün takibinde devrim yaratmıştır.",
        "content": """Moleküler patolojinin en dinamik alanı, kanser tedavisini tek tip kemoterapiden çıkarıp her hastanın tümöründeki spesifik sürücü (driver) mutasyonlara yönelik hedefe yönelik akıllı tedavilere (targeted therapy) dönüştürmesidir.

Hedefe Yönelik Tedavide Moleküler Testler:
1) Akciğer Adenokarsinomu:
- EGFR Mutasyonları: Ekzon 19 delesyonu ve ekzon 21 L858R mutasyonu; EGFR tirozin kinaz inhibitörlerine (TKI: erlotinib, osimertinib) dramatik yanıt verir. Tedavi sürecinde ikincil direnç mutasyonu olan EGFR T790M gelişebilir.
- ALK Füzyonları: EML4-ALK translokasyonu saptanan olgularda ALK inhibitörleri (krizotinib, alektinib) birinci basamak hedeftir.
2) Kolorektal Karsinomda RAS Mutasyonları ve Anti-EGFR Tedavi:
- KRAS ve NRAS Mutasyon Analizi: Kolorektal kanserde anti-EGFR monoklonal antikorlar (Setuksimab, Panitumumab) reseptörü bloke eder. Ancak EGFR'nin altında yer alan KRAS veya NRAS geninde aktive edici bir mutasyon (ekzon 2 kodon 12/13) varsa sinyal iletimi otonom devam eder.
- Klinik Kural: Kolorektal kanserde anti-EGFR tedavi verilebilmesi için KRAS ve NRAS genlerinin mutasyonsuz (yabani tip / wild-type) olması ŞARTTIR! Mutant KRAS varlığı bu ilaçlara primer direnç göstergesidir.
3) Malign Melanom:
- BRAF V600E Mutasyonu: Melanomların yaklaşık %50'sinde bulunur; BRAF ve MEK inhibitörleri ile hedefe yönelik kombinasyon uygulanır.

Minimal Kalıntı Hastalık (MRD - Minimal Residual Disease):
Morfolojik tam remisyon sağlansa dahi vücutta kalan mikroskobik düzeydeki (milyonda bir) neoplastik hücrenin kantitatif PCR (qRT-PCR) veya akış sitometrisi ile ölçülmesidir (ör. KML'de BCR-ABL transkriptleri).

Sıvı Biyopsi (Liquid Biopsy):
Periferik kandan plazmada serbest dolaşan tümör DNA'sının (ctDNA) veya dolaşımdaki tümör hücrelerinin (CTC) analizidir. Tümör içi heterojeniteyi tek bir biyopsiden daha iyi yansıtır; invaziv işlem yapmadan kanda direnç mutasyonlarını (EGFR T790M) ve nüksü radyolojiden aylar önce yakalama imkanı sağlar.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Kolorektal kanserde anti-EGFR monoklonal antikor (setuksimab) tedavisinin etkili olabilmesi için KRAS ve NRAS genlerinin yabani tip (wild-type) olması şarttır; KRAS mutasyonu ilaca primer direnç kanıtıdır. Sıvı biyopside plazmadaki ctDNA analiziyle nüks ve direnç erken saptanır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Metastatik kolorektal karsinomlu bir olguda anti-EGFR monoklonal antikor (setuksimab / panitumumab) tedavisinin başlanabilmesi için aşağıdaki genlerden hangisinin mutasyonsuz (yabani tip / wild-type) olduğunun gösterilmesi zorunludur? (KRAS / NRAS genleri).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Akciğer adenokarsinomunda EGFR ekzon 19/21 mutasyonları TKI (osimertinib) duyarlılığını belirler.",
            "Kolon kanserinde KRAS mutasyonu anti-EGFR tedavisine primer direnç oluşturur.",
            "Sıvı biyopsi plazmada ctDNA analizi yaparak doku biyopsisiz mutasyon ve direnç takibi sağlar."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-023",
            "question": "Hedefe yönelik tedaviler, minimal kalıntı hastalık ve sıvı biyopsi kavramları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Kolorektal kanserde anti-EGFR monoklonal antikor (setuksimab) tedavisinin etkili olabilmesi için KRAS geninin mutant olması gerekir.",
                "B) Akciğer adenokarsinomunda EGFR ekzon 19 delesyonu olan hastalarda tirozin kinaz inhibitörleri (osimertinib vb.) etkilidir.",
                "C) Minimal kalıntı hastalık (MRD) tespiti yalnızca klasik ışık mikroskobunda H&E boyasıyla yapılan bir incelemedir.",
                "D) Sıvı biyopsi yalnızca primer kitle çıkarıldıktan sonra tümör dokusundan alınan sıvı örneklerinin incelenmesidir.",
                "E) Malign melanomda BRAF V600E mutasyonu saptandığında anti-HER2 tedavisi ilk tercihtir."
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Akciğer adenokarsinomunda EGFR tirozin kinaz alanındaki aktivasyon mutasyonları (ekzon 19 delesyonu ve L858R) EGFR tirozin kinaz inhibitörlerine (TKI) yüksek duyarlılık sağlar. A yanlıştır (KRAS mutant olursa anti-EGFR tedaviye dirençlidir; yabani tip [wild-type] olmalıdır). C yanlıştır (MRD qRT-PCR veya akış sitometrisi ile moleküler düzeyde ölçülür). D yanlıştır (sıvı biyopsi periferik kandan plazma ctDNA analizidir). E yanlıştır (BRAF V600E mutasyonunda BRAF/MEK inhibitörleri verilir)."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-023",
                "question": "Hedefe yönelik tedaviler, minimal kalıntı hastalık ve sıvı biyopsi kavramları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "options": [
                    "A) Kolorektal kanserde anti-EGFR monoklonal antikor (setuksimab) tedavisinin etkili olabilmesi için KRAS geninin mutant olması gerekir.",
                    "B) Akciğer adenokarsinomunda EGFR ekzon 19 delesyonu olan hastalarda tirozin kinaz inhibitörleri (osimertinib vb.) etkilidir.",
                    "C) Minimal kalıntı hastalık (MRD) tespiti yalnızca klasik ışık mikroskobunda H&E boyasıyla yapılan bir incelemedir.",
                    "D) Sıvı biyopsi yalnızca primer kitle çıkarıldıktan sonra tümör dokusundan alınan sıvı örneklerinin incelenmesidir.",
                    "E) Malign melanomda BRAF V600E mutasyonu saptandığında anti-HER2 tedavisi ilk tercihtir."
                ],
                "correctAnswer": 1,
                "explanation": "B seçeneği doğrudur. Akciğer adenokarsinomunda EGFR tirozin kinaz alanındaki aktivasyon mutasyonları (ekzon 19 delesyonu ve L858R) EGFR tirozin kinaz inhibitörlerine (TKI) yüksek duyarlılık sağlar. A yanlıştır (KRAS mutant olursa anti-EGFR tedaviye dirençlidir; yabani tip [wild-type] olmalıdır). C yanlıştır (MRD qRT-PCR veya akış sitometrisi ile moleküler düzeyde ölçülür). D yanlıştır (sıvı biyopsi periferik kandan plazma ctDNA analizidir). E yanlıştır (BRAF V600E mutasyonunda BRAF/MEK inhibitörleri verilir)."
            }
        ]
    },
    {
        "slideNumber": 24,
        "title": "Modern Patolojide Entegre Tanı, İmmünoterapi Biyobelirteçleri ve Dijital Patoloji",
        "subtitle": "MSI/MMR Durumu, Tümör Mutasyon Yükü (TMB), PD-L1 ve Yapay Zeka Devrimi",
        "synthesisNarrative": "MSI-H/dMMR tümörler yüksek mutasyon yükü ve bol neoantijen sayesinde anti-PD-1 immünoterapisine organ bağımsız dramatik yanıt verirken; dijital patoloji ve yapay zeka objektif tanı çağını açmıştır.",
        "content": """21. yüzyıl patolojisi, mikroskop camındaki morfolojiyi; immünofenotipik belirteçler, genomik mutasyon analizleri ve dijital görüntüleme algoritmalarıyla birleştiren Entegre (Multimodal) Tanı modeline geçmiştir. Patoloji raporu lezyonun adını koymakla kalmaz; hastanın immünoterapiye uygunluğunu ve tümörün moleküler haritasını tek bir raporda sentezler.

İmmün Kontrol Noktası Blokajı ve İmmünoterapi Biyobelirteçleri:
Malign tümörlerin temel bağışıklıktan kaçış mekanizması, T lenfositlerin yüzeyindeki immün kontrol noktası reseptörlerini (PD-1, CTLA-4) ligandları (PD-L1) aracılığıyla bağlayarak sitotoksik yanıtı baskılamalarıdır. İmmün kontrol noktası inhibitörleri (anti-PD-1: Pembrolizumab, Nivolumab; anti-PD-L1: Atezolizumab) bu freni kaldırarak bağışıklık sistemini tümöre karşı yeniden aktive eder. Başarıyı öngören majör biyobelirteçler şunlardır:

1) Mikrosatellit İnstabilitesi (MSI-H) ve DNA Uyumsuzluk Onarım Eksikliği (dMMR):
- Mekanizma: DNA replikasyon hatalarını düzelten Uyumsuzluk Onarım (MMR) genlerinde (MLH1, MSH2, MSH6, PMS2) mutasyon veya promoter hipermetilasyonu sonucu protein kaybı gelişir.
- Sonuç: Mikrosatellit bölgelerinde kaymalar ve tümör genomunda binlerce somatik mutasyon birikir (hipermutasyon fenotipi). Tümör çok sayıda immünojenik neoantijen sentezler ve yoğun intratümöral CD8+ T lenfosit infiltrasyonu çeker.
- Devrimsel Klinik Önemi: MSI-H / dMMR taşıyan tümörler, köken aldıkları organdan tamamen bağımsız olarak anti-PD-1 (Pembrolizumab) tedavisine dramatik yanıt verirler; doku ve organ tipinden bağımsız (tumor-agnostic) onay alan ilk biyobelirteçtir.

2) Tümör Mutasyon Yükü (TMB) ve PD-L1:
TMB-High (>=10 mutasyon/Mb) neoantijen zenginliğiyle immünoterapi yanıtını öngörür. Tümörde İHK ile PD-L1 pozitifliği ise akciğer karsinomunda pembrolizumab monoterapisi endikasyonunu belirler.

Dijital Patoloji ve Yapay Zeka Devrimi:
Cam lamların tam slayt tarayıcılar (WSI) ile dijitalleştirilmesi patolojide yeni bir dönem başlatmıştır. Yapay zeka ve derin öğrenme algoritmaları; mitotik indeks ve Ki-67 skorlamasında patologlar arası sübjektif değişkenliği sıfırlamakta, hassas onkoloji için çok katmanlı verileri entegre etmektedir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Mikrosatellit instabilitesi yüksek (MSI-H / dMMR) tümörler yüksek somatik mutasyon yükü ve bol neoantijen üretimi nedeniyle immün kontrol noktası inhibitörlerine (anti-PD-1) mükemmel yanıt verir; doku ve organ tipinden bağımsız (tumor-agnostic) onay alan ilk biyobelirteçtir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Kanser hastalarında tümörün çıktığı doku ve organ lokalizasyonuna bakılmaksızın, immün kontrol noktası inhibitörü (anti-PD-1 / pembrolizumab) tedavisine olağanüstü yanıtı öngören ve FDA tarafından dokudan bağımsız onaylanan moleküler biyobelirteç nedir? (Mikrosatellit İnstabilitesi / DNA Uyumsuzluk Onarım Eksikliği - MSI-H / dMMR).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "MSI-H/dMMR yüksek mutasyon yükü ve zengin neoantijen üretimiyle anti-PD-1 tedavisine duyarlıdır.",
            "PD-L1 ekspresyonu immün kontrol noktası blokajında standart İHK prediktif belirtecidir.",
            "Dijital patoloji ve yapay zeka Ki-67 ve mitoz değerlendirmesinde nesnel kantitasyon sağlar."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-024",
            "question": "Modern patolojide immünoterapi biyobelirteçleri ve dijital patoloji devrimi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) DNA uyumsuzluk onarım eksikliği (dMMR / MSI-H) olan tümörler çok sayıda neoantijen ürettikleri için anti-PD-1 immünoterapisine dramatik yanıt verirler.",
                "B) Mikrosatellit instabilitesi (MSI-H), FDA tarafından tümörün çıktığı doku ve organdan bağımsız (tumor-agnostic) onay alan ilk biyobelirteçtir.",
                "C) Tümör Mutasyon Yükü (TMB), tümörün megabazı başına düşen mutasyon sayısını ifade eder ve yüksekliği immünoterapi duyarlılığı ile ilişkilidir.",
                "D) PD-1 / PD-L1 yolağı tümör hücrelerinin sitotoksik T hücrelerini aktive ederek otoimmünite geliştirmesini sağlar.",
                "E) Dijital patoloji ve yapay zeka algoritmaları, mitotik indeks ve Ki-67 skorlamasında patologlar arasındaki değişkenliği azaltarak standardizasyon sağlar."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü PD-1 / PD-L1 yolağı T hücrelerini aktive etmez; tam aksine tümör hücreleri yüzeylerindeki PD-L1 ile T hücresindeki PD-1 reseptörüne bağlanarak sitotoksik T lenfosit yanıtını frenler ve immün kaçış sağlar. İmmünoterapi ilaçları (anti-PD-1 / anti-PD-L1) bu freni kaldırarak T hücrelerinin tümörü yok etmesini sağlar. A, B, C ve E seçenekleri immünoterapi ve dijital patolojinin temel ilkeleridir."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-024",
                "question": "Modern patolojide immünoterapi biyobelirteçleri ve dijital patoloji devrimi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) DNA uyumsuzluk onarım eksikliği (dMMR / MSI-H) olan tümörler çok sayıda neoantijen ürettikleri için anti-PD-1 immünoterapisine dramatik yanıt verirler.",
                    "B) Mikrosatellit instabilitesi (MSI-H), FDA tarafından tümörün çıktığı doku ve organdan bağımsız (tumor-agnostic) onay alan ilk biyobelirteçtir.",
                    "C) Tümör Mutasyon Yükü (TMB), tümörün megabazı başına düşen mutasyon sayısını ifade eder ve yüksekliği immünoterapi duyarlılığı ile ilişkilidir.",
                    "D) PD-1 / PD-L1 yolağı tümör hücrelerinin sitotoksik T hücrelerini aktive ederek otoimmünite geliştirmesini sağlar.",
                    "E) Dijital patoloji ve yapay zeka algoritmaları, mitotik indeks ve Ki-67 skorlamasında patologlar arasındaki değişkenliği azaltarak standardizasyon sağlar."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü PD-1 / PD-L1 yolağı T hücrelerini aktive etmez; tam aksine tümör hücreleri yüzeylerindeki PD-L1 ile T hücresindeki PD-1 reseptörüne bağlanarak sitotoksik T lenfosit yanıtını frenler ve immün kaçış sağlar. İmmünoterapi ilaçları (anti-PD-1 / anti-PD-L1) bu freni kaldırarak T hücrelerinin tümörü yok etmesini sağlar. A, B, C ve E seçenekleri immünoterapi ve dijital patolojinin temel ilkeleridir."
            }
        ]
    }
]
