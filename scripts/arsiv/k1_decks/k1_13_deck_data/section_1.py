# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-13-s01",
        "title": "Kronik Enflamasyonun Tanımı ve Eş Zamanlı Süreçler",
        "content": "Kronik enflamasyon, haftalar, aylar ve hatta yıllar süren; aktif enflamasyonun, doku hasarının ve iyileşme (onarım) girişimlerinin **aynı anda bir arada sürdüğü** uzamış bir savunma yanıtıdır:\n\n- **Dinamik Dengenin Bozulması:** Akut enflamasyondan farklı olarak olay nötrofilik eksüda ile sonlanmaz. Zararlı etken vücuttan tamamen temizlenemediği için konak savunması sürekli bir muharebe alanına dönüşür.\n- **Eş Zamanlı Üçlü Olay:** Lezyon alanında bir yandan lökositler dokuyu tahrip ederken, diğer yandan anjiyogenez (yeni damar oluşumu) ve fibroblast aktivasyonu ile kollajen sentezi (fibrozis) devam eder.\n- **Sonuç:** Süreç dokunun orijinal anatomik mimarisinin kaybıyla ve fonksiyonel parankimin yerini fibröz bağ dokusunun almasıyla (skarlaşma) sonuçlanır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Akut vs Kronik Enflamasyonun Süreç Yapısı",
                "Akut Enflamasyon",
                "Dakikalar-günler sürer; ödem ve nötrofil hakimdir; etken kalkınca doku hızla orijinal haline döner.",
                "Kronik Enflamasyon",
                "Haftalar-aylar sürer; mononükleer hücreler hakimdir; doku hasarı ve fibrozis eş zamanlı ilerler."
            ),
            make_cloze(
                "Kronik enflamasyon doku yıkımı, aktif hücresel yangı ve bağ dokusu onarımının eş zamanlı olarak birlikte sürdüğü uzamış bir yanıttır.",
                "eş zamanlı",
                "Olayların aynı anda bir arada yürümesi özelliği"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-13-s02",
        "title": "Akut ve Kronik Enflamasyonun Karşılaştırmalı Patolojisi",
        "content": "Akut ve kronik enflamasyon patolojik morfoloji, zamansal kinetik ve hücresel aktörler açısından radikal farklılıklar gösterir:\n\n1. **Zaman:** Akut yangı saatler içinde patlak verir ve birkaç günde çözülür; kronik yangı ise haftalar, aylar veya yıllar boyu persistan kalır.\n2. **Hücresel Hakimiyet:** Akut reaksiyonda mikrovasküler geçirgenlik artışı sonucu gelişen sıvı eksüdası ve nötrofil infiltrasyonu başroldedir. Kronik enflamasyonda ise **mononükleer hücreler (makrofajlar, lenfositler ve plazma hücreleri)** dokuyu istila eder.\n3. **Doku Hasarı ve Skar:** Akut enflamasyon genellikle tam rezolüsyonla iyileşir. Kronik enflamasyon ise doku parankimini progresif olarak tahrip eder ve yerini yaygın fibrozise bırakır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Akut Enflamasyon", "Kronik Enflamasyon"],
                [
                    [
                        {"text": "Başlangıç ve Süre", "isMasked": False, "hint": ""},
                        {"text": "Hızlı başlangıç (dakikalar-saatler), kısa süre", "isMasked": False, "hint": ""},
                        {"text": "Sinsi veya uzamış başlangıç, haftalar-aylar", "isMasked": True, "hint": "Kronik yangının zaman boyutu"}
                    ],
                    [
                        {"text": "Baskın Hücreler", "isMasked": False, "hint": ""},
                        {"text": "Nötrofiller ve ödem sıvısı", "isMasked": True, "hint": "Akut fazın polimorfonükleer hücreleri"},
                        {"text": "Makrofajlar, lenfositler ve plazma hücreleri", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Doku Sonucu", "isMasked": False, "hint": ""},
                        {"text": "Genellikle tam rezolüsyon ve sınırlı doku hasarı", "isMasked": False, "hint": ""},
                        {"text": "Kalıcı doku yıkımı, anjiyogenez ve fibrozis", "isMasked": True, "hint": "Kronik süreçteki kalıcı skarlaşma"}
                    ]
                ]
            ),
            make_recall(
                "Akut enflamasyonun histopatolojik incelemesinde baskın hücre nötrofil iken, kronik enflamasyonda infiltratın temelini oluşturan hücre grubu nedir?",
                "Mononükleer lökositlerdir (makrofajlar, lenfositler ve plazma hücreleri).",
                "Tek çekirdekli kronik yangı hücreleri"
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-13-s03",
        "title": "Kronik Enflamasyonun Nedenleri: Kalıcı Enfeksiyonlar",
        "content": "Kronik enflamasyonun en sık tetikleyicilerinden biri, konağın bağışıklık sisteminin temizlemekte zorlandığı **persistan (kalıcı) mikroorganizma enfeksiyonlarıdır**:\n\n- **Dirençli İntraselüler Patojenler:** Mycobacterium tuberculosis (tüberküloz), Treponema pallidum (sifiliz), bazı mantarlar (Histoplasma, Coccidioides) ve parazitler (Leishmania, Schistosoma).\n- **Fagositoza Direnç:** Bu mikroorganizmalar lipid zengin hücre duvarları (mikolik asit gibi) veya fagozom-lizozom füzyonunu engelleme yetenekleri sayesinde makrofaj içinde canlı kalırlar.\n- **Gecikmiş Tip Aşırı Duyarlık:** Canlı kalan etken sürekli antijen sunumuna yol açar; T lenfositleri aralıksız uyarılır ve granülomatöz reaksiyon gibi özel kronik yangı modelleri tetiklenir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kalıcı İntraselüler Enfeksiyonun Kronikleşme Zinciri",
                [
                    "1. Patojen İnvazyonu: Dirençli mikobakteri veya mantarlar doku makrofajları tarafından fagositozla yutulur.",
                    "2. Fagozomal Direnç: Hücre duvarındaki lipidler lizozomal sindirimi bloke ederek mikrobun canlı kalmasını sağlar.",
                    "3. Sürekli Antijen Sunumu: Makrofaj temizleyemediği antijenleri aralıksız CD4+ T hücrelerine sunar.",
                    "4. Th1 ve Sitokin Döngüsü: T hücrelerinden salınan IFN-gama kronik mononükleer yangıyı ve granülomu tetikler."
                ]
            ),
            make_quiz(
                "Konak savunması tarafından hücre içi lizozomal sindirime direnç göstererek kronik granülomatöz enflamasyona yol açan en klasik mikroorganizma hangisidir?",
                [
                    {"key": "A", "text": "Mycobacterium tuberculosis", "explanation": "A seçeneği DOĞRUDUR: Tüberküloz basili hücre duvarındaki mikolik asit sayesinde fagozomda canlı kalır ve kronik granüloma yol açar."},
                    {"key": "B", "text": "Streptococcus pneumoniae", "explanation": "B seçeneği yanlıştır: Tipik akut lober pnömoni etkenidir, nötrofilik eksüda yapar."},
                    {"key": "C", "text": "Neisseria meningitidis", "explanation": "C seçeneği yanlıştır: Akut pürülan menenjit etkenidir."},
                    {"key": "D", "text": "Staphylococcus aureus", "explanation": "D seçeneği yanlıştır: Akut apse ve püy oluşturan piyojenik bakteridir."},
                    {"key": "E", "text": "Vibrio cholerae", "explanation": "E seçeneği yanlıştır: İntestinal toksinle sekretuar ishal yapar, doku enflamasyonu yapmaz."}
                ],
                "A"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-13-s04",
        "title": "Aşırı Duyarlılık Hastalıkları: Otoimmünite ve Alerji",
        "content": "İmmün sistemin kendi dokularına veya zararsız çevresel maddelere karşı aşırı ve uygunsuz yanıt vermesi kronik enflamasyonun ikinci büyük nedenidir:\n\n1. **Otoimmün Hastalıklar:** İmmün tolerans bozulur; otoantijenler ortadan kaldırılamaz çünkü vücudun kendi yapıtaşlarıdır. T-hücreleri ve otoantikorlar dokuyu sürekli uyarır. Örnekler: Romatoid artrit (eklem kıkırdak ve kemik erozyonu), Sistemik Lupus Eritematozus (SLE), Multipl Skleroz (miyelinsizleşme).\n2. **Alerjik Hastalıklar:** Zararsız çevresel antijenlere karşı tekrarlayan temas sonucu Th2/IgE aksı uyarılır. Bronşiyal astımda bronş duvarında kronik eozinofilik ve mast hücre infiltrasyonu, bazal membran kalınlaşması ve düz kas hipertrofisi (hava yolu yeniden şekillenmesi) gelişir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Otoimmünite vs Alerji Kronik Enflamasyon Modelleri",
                "Otoimmün İnflamasyon (Ör. Romatoid Artrit)",
                "Otoantijenler tükenmez; Th1 ve Th17 lenfositleri, plazma hücreleri sinovyumu tahrip edip fibrozis yapar.",
                "Alerjik İnflamasyon (Ör. Kronik Astım)",
                "Tekrarlayan antijen teması; Th2 sitokinleri (IL-4, IL-5, IL-13), eozinofiller ve bronşiyal remodeling görülür."
            ),
            make_cloze(
                "Otoimmün hastalıklarda kendi doku antijenleri ortadan kaldırılamadığı için immün yanıt tükenmez ve kalıcı kronik enflamasyon gelişir.",
                "kendi doku antijenleri",
                "İmmün tolerans kaybında hedeflenen endojen yapılar"
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-13-s05",
        "title": "Toksik Maruziyetler: Eksojen Partiküller ve Endojen Toksinler",
        "content": "Kimyasal ve fiziksel olarak sindirilemeyen partiküllerin dokularda birikmesi kronik enflamasyonun üçüncü majör neden grubunu oluşturur:\n\n- **Eksojen Toksik Maddeler (Pnömokonyozlar):**\n  - **Silika Tozu:** Kristalize silika parçacıkları inhale edildiğinde alveoler makrofajlarca yutulur. Lizozomları patlatarak inflamazomu uyarır; yaygın nodüler fibrozise yol açar (**Silikozis**).\n  - **Asbest Lifleri:** Makrofajlar lifleri fagositozla tüketemez; kronik interstisyel fibrozis (asbestozis) ve mezotelyoma gelişimine zemin hazırlar.\n- **Endojen Toksik Maddeler:**\n  - **Kolesterol ve Lipidler:** Arter intima tabakasında biriken okside LDL, endotelde ve makrofajlarda kronik sitokin salınımı tetikler. Bu tablo modern çağın en yaygın kronik enflamatuar hastalığı olan **Ateroskleroz**'dur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Taş ocağında 15 yıldır çalışan 50 yaşındaki işçi efor dispnesi ile başvuruyor. Akciğer grafisinde her iki üst zonda nodüler dansiteler ve hiler 'yumurta kabuğu' kalsifikasyonları izleniyor.",
                "Bu hastada sindirilemeyen partiküllerin makrofaj fagozomlarını yırtarak kronik enflamasyon ve fibrozisi tetiklemesinden sorumlu eksojen etken nedir?",
                [
                    {
                        "text": "Kristalize silika tozudur (Silikozis tablosu).",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Silika partikülleri makrofaj lizozomlarını delerek NLRP3 inflamazomunu uyarır ve silikotik nodüllere yol açar."
                    },
                    {
                        "text": "Solunan saf polen parçacıklarıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Polen partikülleri alerjik rinit yapar, silikotik nodül ve fibrozis yapmaz."
                    },
                    {
                        "text": "Karbon monoksit gazı maruziyetidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Gaz partikül değildir, hipoksi yapar ancak granülomatöz nodül oluşturmaz."
                    }
                ]
            ),
            make_recall(
                "Arter duvarında biriken okside kolesterol partiküllerinin makrofaj köpük hücreleri oluşturarak tetiklediği en yaygın endojen kronik enflamatuar hastalık nedir?",
                "Aterosklerozdur.",
                "Damar sertliği ve plak oluşumu hastalığı"
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-13-s06",
        "title": "Kronik Enflamasyonun Üçlü Histolojik İmzası",
        "content": "Patolog mikroskop başına geçtiğinde bir doku kesitinde kronik enflamasyon tanısını üç eş zamanlı morfolojik bulgunun varlığıyla koyar:\n\n1. **Mononükleer Hücre İnfiltrasyonu:** Doku aralıklarında yoğunlaşmış makrofajlar, küçük yuvarlak koyu çekirdekli lenfositler ve eksantrik saat kadranı kromatinli plazma hücreleri.\n2. **Doku Yıkımı (Doku Tahribi):** Hem inatçı zararlı etkenin doğrudan saldırısı hem de aktive mononükleer hücrelerin salgıladığı serbest oksijen radikalleri, proteazlar ve sitokinlerle fonksiyonel parankimin erimesi.\n3. **İyileşme Girişimleri (Fibrogenezis ve Anjiyogenez):** Hasarlı bölgeyi çevreleyen fibroblast proliferasyonu, yoğun kollajen lif birikimi (fibrozis) ve yeni kapiller damar tomurcuklanmaları (anjiyogenez).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kronik Enflamasyonun Histolojik Üçlüsü ve Dokudaki İlerlemesi",
                [
                    "1. Mononükleer Hücum: Makrofaj, lenfosit ve plazma hücreleri damardan çıkarak interstisyumu istila eder.",
                    "2. Parankim Yıkımı: Lökositlerden salınan MMP, elastaz ve ROS fonksiyonel doku hücrelerini eritir.",
                    "3. Anjiyogenez Tetiği: Doku hipoksisi ve makrofaj sitokinleri (VEGF, FGF) yeni damar tomurcuklanması yapar.",
                    "4. Fibröz Skarlaşma: TGF-beta etkisiyle fibroblastlar kollajen sentezleyerek hasarlı parankimi skar dokusuna çevirir."
                ]
            ),
            make_cloze(
                "Kronik enflamasyonun üç karakteristik histolojik bileşeni mononükleer hücre infiltrasyonu, parankim tahribi ve fibrozis ile anjiyogenezdir.",
                "mononükleer hücre infiltrasyonu",
                "Makrofaj, lenfosit ve plazma hücresi toplanması terimi"
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-13-s07",
        "title": "Primer Kronik Enflamasyon: Sinsi Başlangıçlı Tablolar",
        "content": "Kronik enflamasyon her zaman önceden geçirilmiş gürültülü bir akut yangının (apse, selülit, flegmon) devamı olmak zorunda değildir. Birçok hastalıkta süreç **başından itibaren sinsi, asemptomatik ve primer kronik** olarak başlar:\n\n- **Klinik Seyir:** Hasta başlangıçta hiçbir şey hissetmez; akut fazın kızarıklık, şişlik ve dayanılmaz ağrı gibi kardinal semptomları görülmez.\n- **Primer Kronik Örnekleri:**\n  - **Romatoid Artrit:** Eklem sinovyumunda haftalarca fark edilmeyen T hücre ve lenfoid agregat birikimi.\n  - **Ateroskleroz:** On yıllar boyunca intimanın sessizce köpük hücreleri ve sitokinlerle dolması.\n  - **Tüberküloz:** Primer basillerin akciğer apeksinde aylar boyu sessizce çoğalması.\n  - **Nörodejeneratif Hastalıklar:** Alzheimer hastalığında amiloid-beta plakları çevresinde mikrogliya hücrelerinin on yıllarca süren kronik aktivasyonu.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sekonder Kronikleşme vs Primer Kronik Başlangıç",
                "Sekonder Kronikleşme (Ör. Kronik Osteomiyelit)",
                "Akut apse veya pürülan infeksiyonun tam temizlenememesi sonucu kronik yangıya dönüşmesidir.",
                "Primer Kronik Başlangıç (Ör. Romatoid Artrit, Ateroskleroz)",
                "Hiçbir akut belirti vermeden, en baştan sinsi mononükleer infiltrat ve fibrozisle başlar."
            ),
            make_quiz(
                "Akut enflamasyon fazı yaşanmaksızın, en baştan itibaren haftalar-yıllar içinde sinsi ve ilerleyici doku tahribiyle başlayan kronik yangı paternine ne ad verilir?",
                [
                    {"key": "A", "text": "Primer kronik enflamasyon", "explanation": "A seçeneği DOĞRUDUR: Romatoid artrit ve ateroskleroz gibi süreçler akut faz olmadan primer kronik başlar."},
                    {"key": "B", "text": "Akut seröz enflamasyon", "explanation": "B seçeneği yanlıştır: Yanık bülündeki gibi ani akut sıvı toplanmasıdır."},
                    {"key": "C", "text": "Fibrinöz perikardit", "explanation": "C seçeneği yanlıştır: Akut fibrinli yüzey eksüdasyonudur."},
                    {"key": "D", "text": "Süpüratif enflamasyon", "explanation": "D seçeneği yanlıştır: Akut nötrofilik püy oluşumudur."},
                    {"key": "E", "text": "Kataral enflamasyon", "explanation": "E seçeneği yanlıştır: Yüzeyel mukus artışıyla seyreden akut mukozal yanıttır."}
                ],
                "A"
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-13-s08",
        "title": "Akut Enflamasyonun Kronikleşme Nedenleri",
        "content": "Akut enflamatuar bir odağın fizyolojik olarak iyileşmeyip inatçı bir kronik yangıya dönüşmesine yol açan temel mekanizmalar şunlardır:\n\n1. **Yetersiz Drenaj ve Nekrotik Kalıntılar:** Apse odağının cerrahi veya spontan olarak drene edilememesi; içerideki nekrotik debrisin nötrofilleri ve ardından makrofajları sürekli uyarması.\n2. **Yabancı Cisim Varlığı:** Yaraya batan cam parçası, ahşap kıymık veya cerrahi dikiş ipliği nötrofillerce eritilemez; makrofajlar yabancı cismi çevreleyerek kronik granülomatöz yangıyı sürdürür.\n3. **Sekestr Oluşumu:** Kemik enfeksiyonunda (akut osteomiyelit) dolaşımı kesilip ölen kortikal kemik parçası (sekestr) antibiyotiklerin ulaşamadığı bir bakteri yuvası haline gelir; **kronik osteomiyelite** dönüşür.\n4. **Konak İmmün Yetersizliği:** Diyabet, malnütrisyon veya steroid kullanımı fagositozu zayıflatarak etkenin temizlenmesini engeller.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kronikleşme Nedeni", "Tipik Klinik Örnek", "Doku Patolojisi"],
                [
                    [
                        {"text": "Yetersiz Drenaj", "isMasked": False, "hint": ""},
                        {"text": "Drene edilmemiş derin doku apsesi", "isMasked": False, "hint": ""},
                        {"text": "Fibröz kapsülle çevrili kronik apse boşluğu", "isMasked": True, "hint": "Kapsüllenmiş iltihap odağı"}
                    ],
                    [
                        {"text": "Sekestr Oluşumu", "isMasked": True, "hint": "Ölü avasküler kemik parçası"},
                        {"text": "Kronik piyojenik osteomiyelit", "isMasked": False, "hint": ""},
                        {"text": "Ölü kemik etrafında involukrum ve fistül traktı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Yabancı Cisim", "isMasked": False, "hint": ""},
                        {"text": "Unutulmuş cerrahi dikiş ipliği", "isMasked": True, "hint": "Ameliyat sonrası dokuda kalan materyal"},
                        {"text": "Polarize ışıkta parlayan yabancı cisim granülomu", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Akut osteomiyelitin kronikleşmesinde antibiyotiklerin ulaşamadığı, beslenmesi bozulmuş ölü kemik parçasına ne ad verilir?",
                "Sekestrdır (etrafındaki canlı kemik kılıfına ise involukrum denir).",
                "Ölü kemik dokusu terimi"
            )
        ]
    })

    # Slide 9
    slides.append({
        "id": "k1-13-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Kronik Enflamasyon Temelleri ve Karşılaştırmalı Patoloji",
        "content": "Bu ilk kontrol noktasında kronik enflamasyonun temel dinamiklerini ve akut enflamasyonla olan kritik ayrımlarını pekiştiriyoruz:\n\n- **Eş Zamanlı Süreç:** Kronik enflamasyon doku yıkımı, mononükleer yangı ve bağ dokusu onarımının (fibrozis ve anjiyogenez) haftalar-aylar boyu bir arada sürdüğü yanıttır.\n- **Hücresel Kadro:** Nötrofillerin yerini mononükleer hücreler (makrofajlar, lenfositler, plazma hücreleri) alır.\n- **Üç Majör Neden:** 1) Kalıcı intraselüler enfeksiyonlar (tüberküloz), 2) Aşırı duyarlılık ve otoimmünite (romatoid artrit), 3) Sindirilemeyen toksik partiküller (silikozis, ateroskleroz).\n- **Üçlü Histolojik İmza:** Mononükleer infiltrasyon + parankim tahribi + fibrogenezis/anjiyogenez.\n- **Başlangıç:** Primer sinsi (ateroskleroz) veya sekonder kronikleşme (drene edilmemiş apse, sekestr).",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Aşağıdakilerden hangisi kronik enflamasyonun histopatolojik incelemesinde mutlaka bir arada görülen üç temel morfolojik özellikten biri DEĞİLDİR?",
                [
                    {"key": "A", "text": "Masif nötrofilik eksüdasyon ve yaygın vasküler konjesyon", "explanation": "A seçeneği DOĞRUDUR (aranan yanlıştır): Masif nötrofilik eksüdasyon ve vazodilatasyon akut enflamasyonun tipik bulgusudur; kronikte mononükleer infiltrat, doku hasarı ve fibrozis görülür."},
                    {"key": "B", "text": "Mononükleer hücre (makrofaj, lenfosit) infiltrasyonu", "explanation": "B seçeneği kronik enflamasyonun ana histolojik imzasıdır."},
                    {"key": "C", "text": "Enflamatuar hücrelerce üretilen parankim dokusu tahribi", "explanation": "C seçeneği kronik enflamasyonun ana histolojik imzasıdır."},
                    {"key": "D", "text": "Bağ dokusu artışı ve kollajen birikimi (fibrozis)", "explanation": "D seçeneği kronik enflamasyonun ana histolojik imzasıdır."},
                    {"key": "E", "text": "Yeni kılcal damar tomurcuklanması (anjiyogenez)", "explanation": "E seçeneği iyileşme girişiminin ana histolojik imzasıdır."}
                ],
                "A"
            ),
            make_cloze(
                "Kronik enflamasyon odağında hasar gören dokunun yerine fibroblastların kollajen biriktirmesi ve yeni damarların oluşması sürecine fibrozis ve anjiyogenez adı verilir.",
                "fibrozis ve anjiyogenez",
                "Bağ doku birikimi ve damarlanma terimleri"
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-13-s10",
        "title": "Kronik Enflamasyonda Masum Çevre Doku Tahribatı",
        "content": "Kronik enflamasyonun en trajik özelliği, konak savunma hücrelerinin salgıladığı ölümcül silahların mikroorganizmadan çok **hastanın kendi sağlıklı parankim dokusunu yok etmesidir**:\n\n- **Masum İzleyici Hasarı (Bystander Damage):** Makrofaj ve T lenfositler ortamdaki antijeni temizleyemedikçe daha fazla sitokin salgılar; salınan lizozomal enzimler (elastaz, katepsinler), matriks metalloproteinazlar (MMP-1, MMP-9), nitrik oksit ve reaktif oksijen ürünleri çevre hücreleri parçalar.\n- **Örnek Klinik Durumlar:**\n  - Tüberkülozda kavitasyon gelişimi: Akciğer parankiminin erimesi.\n  - Romatoid artritte pannus: Eklem kıkırdağının ve kemik trabeküllerinin eritilerek eklemin ankiloz olması.\n  - Kronik hepatitte siroz: Hepatositlerin ölmesi ve karaciğerin nodüler fibröz kitleye dönüşmesi.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Etkene Yönelik Savunma vs Masum Çevre Doku Hasarı",
                "Fizyolojik Konak Savunması",
                "Enzimler ve fagositoz hedef mikroba yöneliktir; çevre doku hasarı sınırlıdır.",
                "Kronik Bystander Doku Hasarı",
                "Aylarca süren kontrolsüz proteaz ve ROS salınımı sonucu çevre organ parankimi geri dönüşsüz erir."
            ),
            make_recall(
                "Kronik enflamasyonda aktive makrofajların salgıladığı ve ekstraselüler matriksi, kollajeni ve proteoglikanları parçalayarak doku yıkımına yol açan çinko bağımlı enzim ailesi hangisidir?",
                "Matriks Metalloproteinazlardır (MMP).",
                "Matriksi yıkan metal bağımlı enzim ailesi"
            )
        ]
    })

    return slides
