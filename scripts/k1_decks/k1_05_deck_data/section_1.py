"""
Bölüm 1: Kazeöz Nekroz, Tüberküloz Patolojisi ve Granülomatöz İnflamasyon
Adımlar: 1 - 10
Checkpoint: Adım 9 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # ADIM 1
    slides.append({
        "slideNumber": 1,
        "title": "Kazeöz Nekroz: Tüberküloz Enfeksiyonunun Karakteristik Dokusu",
        "subtitle": "Peynirleşme nekrozunun etiyolojik temeli ve makroskobik görünümü",
        "badge": "Kazeöz Nekroz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kazeöz nekroz, tıbbi literatürde peynirleşme nekrozu olarak da tanımlanan ve hemen her zaman "
            "Mycobacterium tuberculosis enfeksiyon odaklarında karşılaşılan son derece özgün bir doku ölüm kalıbıdır. "
            "Bu patolojinin 'kazeöz' (Latince caseus = peynir) olarak adlandırılmasının temel nedeni, makroskobik "
            "incelemede nekrotik odağın sarımsı-beyaz renkli, ufalanabilir, yumuşak ve tam anlamıyla taze lor "
            "peynirine benzeyen bir kalıntı yığını oluşturmasıdır.\n\n"
            "> [SINAV SPOTU] Kazeöz nekroz solid organ enfarktlarında görülen koagülatif nekrozdan farklı olarak "
            "doku çatısını tamamen siler; amorf ve ufalanabilir peynirimsi bir görünüm kazanır.\n\n"
            "Tüberküloz basilleri akciğer parankimine yerleştiğinde konak immün yanıtı ile basilin mikolik asit zengin "
            "hücre duvarı arasında amansız bir mücadele başlar. Makrofajlar basilleri sindiremeyip sitokin salgıladıkça "
            "merkezdeki hücreler kademeli olarak ölür ve karakteristik kazeöz kitle meydana gelir."
        ),
        "medicalTerms": [
            {"term": "Kazeöz Nekroz", "explanation": "Tüberküloz basiline bağlı gelişen, makroskobik olarak peynirimsi, mikroskobik olarak amorf granüler nekroz tipidir."},
            {"term": "Mycobacterium tuberculosis", "explanation": "Aside dirençli, hücre duvarı mikolik asit ve kord faktör zengini, kazeöz granülom yapan basil."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kazeöz nekroz denildiğinde ilk akla gelen etken Mycobacterium tuberculosis'tir.",
            "📌 [SINAV SPOTU] Makroskobik olarak sarı-beyaz, yumuşak, kırılgan ve peynir benzeri kalıntılar içerir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kazeöz Kavramı", "desc": "Peynir benzeri yumuşak ve ufalanan nekrotik materyal.", "isKey": True},
                {"title": "Etiyolojik Bağlam", "desc": "Primer veya reaktivasyon akciğer tüberkülozunun değişmez bulgusudur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Akciğer tüberkülozunda lezyon merkezinde yumuşak ve peynirimsi görünümüyle kazeöz nekroz odakları izlenir.",
                "kazeöz nekroz",
                "Tüberkülozun tipik peynirleşme kalıbı"
            ),
            make_active_recall(
                "Kazeöz nekroza neden 'peynirleşme' nekrozu denir ve en tipik klinik örneği nedir?",
                "Makroskobik olarak yumuşak, sarı-beyaz ve kırılgan lor peynirine benzediği için bu isim verilir; en tipik örneği akciğer tüberkülozudur."
            )
        ]
    })

    # ADIM 2
    slides.append({
        "slideNumber": 2,
        "title": "Kazeöz Nekrozun Işık Mikroskopisi: Amorf ve Granüler Çatı Kaybı",
        "subtitle": "Koagülatif nekrozdan hücresel sınırların silinmesiyle ayrılan mikroskobik mimari",
        "badge": "Mikroskopi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Işık mikroskobu altında kazeöz nekroz alanı incelendiğinde, solid organ enfarktlarındaki koagülatif "
            "nekrozdan tamamen farklı bir tablo ile karşılaşılır. Koagülatif nekrozda ölü hücrelerin anahatları ve "
            "doku mimarisi günlerce 'hayalet hücreler' şeklinde korunurken, kazeöz nekrozda doku mimarisi tümüyle silinmiştir.\n\n"
            "Nekroz sahası, yapısını tamamen yitirmiş eozinofilik (pembe), amorf ve ince granüler döküntülerden ibarettir. "
            "Hücre sınırları hiçbir şekilde seçilemez ve çekirdekler karyoreksis veya karyolizis ile tamamen eriyip gitmiştir.\n\n"
            "> [KRİTİK UYARI] Kazeöz nekroz mikroskopisinde hücre hatları ve organel sınırları seçilemez; alan "
            "yapısız, pembe, granüler ve nükleer tozlardan zengin nekrotik bir birikim gösterir.\n\n"
            "Bu amorf kalıntı, basillerin lipidik duvar bileşenleri ile lizozomal enzimlerin dokuyu yarı sindirmesi sonucu "
            "sıvılaşma ile koagülasyon arasında asılı kalmış özel bir ara durumdur."
        ),
        "medicalTerms": [
            {"term": "Amorf Granüler Nekroz", "explanation": "Hiçbir hücre sınırı seçilemeyen, pembe-eozinofilik döküntü alanı."},
            {"term": "Hayalet Hücre (Ghost Cell)", "explanation": "Koagülatif nekrozda görülen fakat kazeöz nekrozda tamamen kaybolan hücresel iskelet."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kazeöz nekrozda doku mimarisi ve hücre hatları tamamen kaybolmuştur.",
            "📌 [SINAV SPOTU] Işık mikroskobunda yapı göstermeyen amorf, granüler, pembe eozinofilik nekrotik alan izlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Doku İskeleti", "desc": "Koagülatif nekrozun aksine hücresel konturlar bütünüyle erimiştir.", "isKey": True},
                {"title": "Mikroskobik Renk", "desc": "Hematoksilen-eozinde asellüler, homojen-granüler pembe alan.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Koagülatif vs Kazeöz Nekroz Mikroskobik Mimarisi",
                "Koagülatif Nekroz",
                "Hücre sınırları ve organ mimarisi günlerce hayalet hücreler şeklinde korunur.",
                "Kazeöz Nekroz",
                "Hücre sınırları ve doku mimarisi bütünüyle silinmiş, amorf granüler pembe döküntü oluşmuştur."
            ),
            make_cloze(
                "Mikroskop altında kazeöz nekroz sahasında doku mimarisi tamamen silinmiştir ve amorf granüler pembe kalıntılar izlenir.",
                "doku mimarisi",
                "Organın histolojik çatısının durumu"
            )
        ]
    })

    # ADIM 3
    slides.append({
        "slideNumber": 3,
        "title": "Granülomatöz İnflamasyon: Kazeöz Nekrozu Kuşatan Hücresel Kalkan",
        "subtitle": "Tip IV aşırı duyarlılık ve hücresel bağışıklığın kazeöz nekroz çevresindeki organizasyonu",
        "badge": "Granülom",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kazeöz nekroz patolojide asla tek başına, çıplak bir alan olarak bulunmaz. Nekrotik odaklar daima "
            "vücudun tüberküloz basilini sınırlandırmak amacıyla kurduğu özel bir kronik yangı bariyeri olan "
            "'granülomatöz inflamasyon' (granülom) ile kuşatılmıştır.\n\n"
            "Bu süreç, T lenfositlerin (özellikle CD4+ Th1 hücreleri) basil antijenlerini tanıması ve ortama "
            "İnterferon-gama (IFN-γ) salgılamasıyla tetiklenen bir gecikmiş tip (Tip IV) aşırı duyarlılık reaksiyonudur. "
            "IFN-γ etkisiyle aktive olan monositler ve makrofajlar, epitel hücrelerine benzeyen bol eozinofilik sitoplazmalı "
            "'epitelioid histiyositlere' dönüşürler.\n\n"
            "> [SINAV SPOTU] Granülomun olmazsa olmaz temel hücresi epitelioid histiyositlerdir; kazeöz granülomda bu "
            "hücreler kazeöz nekroz merkezini sıkı bir çit gibi sarar."
        ),
        "medicalTerms": [
            {"term": "Granülom", "explanation": "Epitelioid histiyositlerin oluşturduğu, lenfosit ve dev hücrelerle çevrili özel kronik inflamasyon odağı."},
            {"term": "Epitelioid Histiyosit", "explanation": "İnterferon-gama ile aktive olup bol eozinofilik sitoplazma kazanan, fagositik gücü yüksek değişime uğramış makrofaj."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kazeöz nekroz çevresinde granülomatöz inflamasyon (kazeöz granülom) gelişir.",
            "📌 [SINAV SPOTU] Granülom oluşumundaki kritik sitokin Th1 lenfositlerden salınan İnterferon-gama'dır (IFN-γ)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücresel Yanıt", "desc": "Tip IV hücresel immünite ve IFN-gama yönlendirmesi.", "isKey": True},
                {"title": "Temel Bileşen", "desc": "Kazeöz çekirdeği çevreleyen epitelioid histiyosit tabakası.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Kazeöz Granülom Gelişim Basamakları",
                [
                    "1. Basil Fagositozu: Makrofajlar mikobakterileri fagosite eder ancak mikolik asit nedeniyle sindiremez.",
                    "2. Antijen Sunumu: Dendritik hücreler ve makrofajlar basil antijenlerini CD4+ T lenfositlere sunar.",
                    "3. IFN-γ Salınımı: Aktive olan Th1 lenfositler ortama yoğun İnterferon-gama salgılar.",
                    "4. Epitelioid Dönüşüm: IFN-γ etkisiyle makrofajlar geniş sitoplazmalı epitelioid histiyositlere dönüşür.",
                    "5. Kazeifikasyon: Merkezde biriken sitokinler ve serbest radikaller dokuyu peynirleşme nekrozuna uğratır."
                ]
            ),
            make_cloze(
                "Granülom oluşumunda makrofajları aktive ederek epitelioid histiyosit haline getiren temel sitokin interferon-gama molekülüdür.",
                "interferon-gama",
                "Th1 lenfositlerin salgıladığı ana immün aktivatör"
            )
        ]
    })

    # ADIM 4
    slides.append({
        "slideNumber": 4,
        "title": "Langhans Tipi Dev Hücreler: Çok Çekirdekli Savunma Devleri",
        "subtitle": "Kazeöz granülomun periferinde at nalı dizilimli çekirdek mimarisi",
        "badge": "Dev Hücreler",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kazeöz nekrozun dış sınırında yer alan epitelioid histiyositlerin bir kısmı, yoğun sitokin uyarısı altında "
            "hücre zarlarını birleştirerek çok çekirdekli dev hücreler oluşturur. Tüberküloz granülomlarında görülen "
            "bu dev hücrelere 'Langhans tipi dev hücre' adı verilir.\n\n"
            "Langhans dev hücrelerinin patolojik ayırt edici özelliği, onlarca çekirdeğin hücrenin periferinde "
            "hilal veya 'at nalı' şeklinde dizilmesidir. Hücrenin merkezi ise eozinofilik ve homojen bir sitoplazma içerir.\n\n"
            "> [KRİTİK UYARI] Langhans dev hücresi tüberküloz ve kazeöz granülomlara özgüyken; Langerhans hücresi "
            "deride bulunan antijen sunucu dendritik bir hücredir. İki terim asla karıştırılmamalıdır!\n\n"
            "Yabancı cisim dev hücrelerinde ise çekirdekler hücre merkezinde dağınık veya rastgele kümelenmiştir."
        ),
        "medicalTerms": [
            {"term": "Langhans Tipi Dev Hücre", "explanation": "Çekirdekleri at nalı şeklinde dizilmiş, makrofaj füzyonuyla oluşan granülom dev hücresi."},
            {"term": "Langerhans Hücresi", "explanation": "Epidermiste yerleşmiş, Birbeck granülleri içeren fizyolojik dendritik antijen sunucu hücre."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Langhans dev hücrelerinde çekirdekler hücre çeperinde at nalı (hilal) biçiminde sıralanır.",
            "📌 [SINAV SPOTU] Langhans hücresi ile derideki Langerhans hücresi farklı kavramlardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mitolojik İskelet", "desc": "Makrofaj füzyonu ile meydana gelen çok çekirdekli dev yapı.", "isKey": True},
                {"title": "Nükleer Dizilim", "desc": "Periferik yerleşimli at nalı / U-harfi morfolojisi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hücre Türü", "Çekirdek Dağılımı", "Tipik Klinik Tablo"],
                [
                    [("Langhans Dev Hücresi", False, ""), ("At nalı şeklinde periferik dizilim", True, "Nükleer yerleşim kalıbı"), ("Tüberküloz, Kazeöz Granülom", False, "")],
                    [("Yabancı Cisim Dev Hücresi", False, ""), ("Merkezde düzensiz ve rastgele kümelenme", True, "Nükleusların konumu"), ("Sütür reaksiyonu, talk pudrası", False, "")],
                    [("Touton Dev Hücresi", False, ""), ("Halka dizilimli çekirdek, köpüksü sitoplazma", True, "Sitoplazma lipid içeriği"), ("Ksantom, jüvenil ksantogranülom", False, "")]
                ]
            ),
            make_cloze(
                "Tüberküloz granülomundaki çok çekirdekli Langhans dev hücrelerinde çekirdekler at nalı şeklinde periferde dizilir.",
                "at nalı",
                "Çekirdeklerin hilal benzeri sıralanış biçimi"
            )
        ]
    })

    # ADIM 5
    slides.append({
        "slideNumber": 5,
        "title": "Ghon Kompleksi ve Kavitasyon: Tüberküloz Lezyonunun Kaderi",
        "subtitle": "Subplevral kazeöz odaktan bronşa açılan kavern oluşumuna patolojik evreler",
        "badge": "Klinik Patoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Primer akciğer tüberkülozunda, basilin yerleştiği subplevral parankimal kazeöz odak (Ghon odağı) "
            "ile drene olduğu hiler lenf düğümündeki kazeöz nekroz birlikteliğine 'Ghon kompleksi' adı verilir. "
            "Zamanla bu lezyon fibröz bir kapsülle sarılıp distrofik olarak kalsifiye olduğunda 'Ranke kompleksi' adını alır.\n\n"
            "Eğer konak bağışıklığı zayıflarsa veya reaktivasyon tüberkülozu gelişirse, kazeöz materyal lenfosit ve "
            "makrofaj kaynaklı hidrolitik enzimlerle sıvılaşabilir. Sıvılaşan nekroz yakındaki bir bronş duvarını eritip "
            "bronş ağacına boşaldığında geride hava dolu geniş bir boşluk olan 'kavitasyon' (kavern) kalır.\n\n"
            "> [SINAV SPOTU] Kavern duvarı bol oksijen içerdiğinden basiller burada hızla çoğalır ve hasta öksürükle "
            "milyonlarca basili çevreye yayarak son derece bulaşıcı hale gelir."
        ),
        "medicalTerms": [
            {"term": "Ghon Kompleksi", "explanation": "Akciğer parankimindeki kazeöz odak ile hiler lenf nodu kazeifikasyonunun birlikteliği."},
            {"term": "Kavitasyon (Kavern)", "explanation": "Sıvılaşan kazeöz kitlenin bronşa drene olmasıyla akciğerde açılan patolojik boşluk."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ghon kompleksi: Parankimal kazeöz odak + hiler kazeöz lenfadenopati.",
            "📌 [SINAV SPOTU] Kavitasyon (kavern), reaktivasyon tüberkülozunda kazeöz nekrozun bronşa drene olmasıyla oluşur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Ghon Mimarisi", "desc": "Primer tüberkülozun subplevral ve lenfatik kazeöz tutulumu.", "isKey": True},
                {"title": "Kavernleşme Riski", "desc": "Bronşiyal drenaj sonucu yüksek oksijenli süper bulaştırıcı kavite.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Akciğer tüberkülozunda parankimdeki kazeöz odak ile hiler lenf nodu tutulumunun birlikte oluşturduğu klasik lezyon hangisidir?",
                {
                    "A": "Aschoff nodülü",
                    "B": "Ghon kompleksi",
                    "C": "Mallory cisimciği",
                    "D": "Councilman cisimciği",
                    "E": "Russell cisimciği"
                },
                "B",
                {
                    "A": "Aschoff nodülleri romatizmal karditte görülür.",
                    "B": "Doğru cevap B'dir: Ghon odağı ve hiler kazeöz lenf nodu Ghon kompleksini oluşturur.",
                    "C": "Mallory cisimleri alkolik hepatitte izlenen sitokeratin birikimidir.",
                    "D": "Councilman cisimleri viral hepatitteki apoptotik hepatositlerdir.",
                    "E": "Russell cisimleri plazma hücrelerindeki immünoglobulin birikintileridir."
                }
            ),
            make_cloze(
                "Primer tüberkülozda akciğer parankimindeki kazeöz lezyon ile hiler lenf nodunun birlikteliğine Ghon kompleksi denir.",
                "Ghon kompleksi",
                "Anton Ghon tarafından tanımlanan primer tüberküloz patolojik birimi"
            )
        ]
    })

    # ADIM 6
    slides.append({
        "slideNumber": 6,
        "title": "Kazeöz Dışı Granülomlar: Ayırıcı Tanı Spektrumu",
        "subtitle": "Kazeöz olan ve kazeöz olmayan (non-kazeifiye) granülomların klinik ayrımı",
        "badge": "Ayırıcı Tanı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Patolojide her granülom kazeöz nekroz içermez. Granülomatöz hastalıklar nekroz varlığına göre "
            "kazeifiye (nekrotizan) ve non-kazeifiye (nekrotizan olmayan) olarak iki büyük sınıfa ayrılır.\n\n"
            "Tüberküloz, histoplazmoz ve koksidioidomikoz gibi mantar enfeksiyonlarında kazeöz nekroz belirginken; "
            "Sarkoidoz, Crohn hastalığı, berilyozis ve yabancı cisim reaksiyonlarında granülomların merkezinde "
            "kazeöz nekroz bulunmaz (non-kazeifiye granülom).\n\n"
            "> [KLİNİK İPUCU] Akciğer biyopsisinde merkezinde nekroz içermeyen, sıkıca paketlenmiş epitelioid histiyosit "
            "ve dev hücrelerden oluşan granülomlar saptandığında öncelikle Sarkoidoz düşünülür.\n\n"
            "Kedi tırmığı hastalığında (Bartonella henselae) ve lenfogranüloma venereumda ise kazeöz nekroz yerine "
            "içinde nötrofil kümeleri barındıran 'süpüratif granülom' (nekrotizan granülom) izlenir."
        ),
        "medicalTerms": [
            {"term": "Non-kazeifiye Granülom", "explanation": "Merkezinde nekroz barındırmayan, epitelioid histiyosit ve dev hücrelerden zengin granülom (örn. Sarkoidoz)."},
            {"term": "Süpüratif Granülom", "explanation": "Nekroz odağında lökosit/nötrofil infiltrasyonu bulunan granülom (örn. Kedi tırmığı hastalığı)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sarkoidoz ve Crohn hastalığında kazeöz nekroz İÇERMEYEN non-kazeifiye granülomlar görülür.",
            "📌 [SINAV SPOTU] Tüberküloz ve derin mikozlar tipik kazeöz nekrozlu granülom yaparlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kazeifiye Granülom", "desc": "Tüberküloz ve fungal enfeksiyonlara özgü peynirimsi merkez.", "isKey": True},
                {"title": "Non-kazeifiye Granülom", "desc": "Sarkoidoz, Crohn ve berilyoziste izlenen temiz merkezli granülom.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "35 yaşında kadın hasta nefes darlığı ve bilateral hiler lenfadenopati ile başvuruyor. Yapılan bronkoskopik transbronşiyal biyopside merkezinde nekroz barındırmayan, sıkı epitelioid histiyosit adacıkları izleniyor.",
                [
                    {
                        "text": "Bu görünüm kazeöz nekrozlu tüberkülozdur; derhal antitüberküloz tedaviye başlanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Biyopside kazeöz nekrozun kesinlikle OLMADIĞI açıkça belirtilmiştir."
                    },
                    {
                        "text": "Nekroz içermeyen bu lezyon non-kazeifiye granülomdur ve klinik tabloyla birlikte öncelikle Sarkoidozu düşündürür.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Sarkoidozun histopatolojik damgası kazeifiye olmayan (çıplak) granülomlardır."
                    },
                    {
                        "text": "Bu lezyon akut bakteriyel piyojenik apsedir ve ampirik seftriakson verilmelidir.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Granülom kronik bir yanıttır, akut apse nötrofil lökositlerden oluşur."
                    }
                ]
            ),
            make_cloze(
                "Sarkoidoz hastalığında lezyonların merkezinde kazeöz nekroz bulunmaz; non-kazeifiye granülomlar izlenir.",
                "non-kazeifiye granülomlar",
                "Merkezinde nekroz içermeyen granülomatöz yapı tipi"
            )
        ]
    })

    # ADIM 7
    slides.append({
        "slideNumber": 7,
        "title": "Ziehl-Neelsen Boyası: Kazeöz Nekrozda Aside Dirençli Basil Kanıtı",
        "subtitle": "Hematoksilen-eozinde görünmeyen mikobakterilerin mikolik asit zırhını delen histokimyasal yöntem",
        "badge": "Laboratuvar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Standart hematoksilen-eozin (H&E) kesitlerinde kazeöz nekroz alanı pembe bir çöl gibi görünür; basilin "
            "kendisi bu boyama ile asla seçilemez. Mycobacterium tuberculosis tanısını kesinleştirmek için "
            "lezyon kesitlerine özel bir histokimyasal boyama olan 'Ziehl-Neelsen (ZN)' boyası uygulanmalıdır.\n\n"
            "Mikobakterilerin hücre duvarı yüksek oranda mikolik asit ve uzun zincirli yağ asitleri içerir. Bu mumsu "
            "yapı karbolfuksin boyasını içine hapseder ve asit-alkol solüsyonu ile muamele edildiğinde dahi rengini vermez.\n\n"
            "> [SINAV SPOTU] Bu özelliğe 'Aside Dirençli Basil (ARB)' denir. Ziehl-Neelsen boyasında zemin parlak "
            "maviye boyanırken, tüberküloz basilleri kazeöz nekroz içinde ince, hafif kıvrık kırmızı-pembe çomaklar olarak parlar.\n\n"
            "Daha hassas florokrom boyası olan Auramin-Rhodamin ile floresan mikroskobunda sarı-yeşil ışıma izlenir."
        ),
        "medicalTerms": [
            {"term": "Ziehl-Neelsen Boyası", "explanation": "Aside dirençli mikobakterileri parlak kırmızı-pembe çomaklar halinde gösteren özel histokimyasal boya."},
            {"term": "Aside Dirençli Basil (ARB)", "explanation": "Hücre duvarındaki mikolik asit sayesinde asitli alkol ile rengini kaybetmeyen mikroorganizma."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tüberküloz tanısında dokuda basili göstermek için Ziehl-Neelsen (ZN) boyası kullanılır.",
            "📌 [SINAV SPOTU] ZN boyamasında mikobakteriler mavi zemin üzerinde kırmızı (Aside Dirençli Basil / ARB) çomaklar şeklinde görünür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Boyama Prensibi", "desc": "Mikolik asit tabakasının karbolfuksin tutması ve asitle solmaması.", "isKey": True},
                {"title": "Görsel Kontrast", "desc": "Mavi doku zemininde parlayan kırmızı ARB basilleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Kazeöz nekrozlu bir dokuda Mycobacterium tuberculosis basillerini göstermek için hangi özel histokimyasal boya kullanılır?",
                "Ziehl-Neelsen (Aside Dirençli Basil / ARB) boyası kullanılır; basiller kırmızı çomaklar şeklinde boyanır."
            ),
            make_cloze(
                "Tüberküloz basilleri hücre duvarlarındaki mikolik asit sayesinde aside dirençli basil özelliği gösterir ve ZN boyasında kırmızı boyanır.",
                "aside dirençli basil",
                "Asit-alkol ile rengi solmayan mikroorganizma niteliği"
            )
        ]
    })

    # ADIM 8
    slides.append({
        "slideNumber": 8,
        "title": "Kazeöz Nekrozun Distrofik Kalsifikasyonu: Kireçlenme Dönemi",
        "subtitle": "Eriyen nekrotik hücrelerden açığa çıkan kalsiyumun dokuda fosfatla çökmesi",
        "badge": "Kalsifikasyon",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kazeöz nekroz alanları başarılı bir bağışıklık yanıtı veya antitüberküloz tedavi ile iyileşme sürecine "
            "girdiğinde, lezyon etrafı yoğun bir fibröz doku kapsülü ile sarılır. Nekrotik sahadaki hücresel döküntüler "
            "ve parçalanan membran fosfolipidleri kalsiyum iyonlarını çekmeye başlar.\n\n"
            "Serum kalsiyum seviyeleri tamamen normal olmasına rağmen, hasarlı ve ölü dokuda kalsiyum tuzlarının birikmesi "
            "olayına 'distrofik kalsifikasyon' adı verilir. Kalsiyum fosfat kristalleri (hidroksiapatit) kazeöz "
            "odağı taş sertliğinde bir nodüle dönüştürür.\n\n"
            "> [SINAV SPOTU] Akciğer grafisinde yıllar önce geçirilmiş tüberkülozun kanıtı olarak görülen radyoopak "
            "kireçlenmiş kitleler, distrofik kalsifikasyona uğramış kazeöz nekroz kalıntılarıdır (Ranke kompleksi).\n\n"
            "Histopatolojik kesitlerde bu alanlar hematoksilen ile koyu mor-mavi amorf kitleler şeklinde izlenir."
        ),
        "medicalTerms": [
            {"term": "Distrofik Kalsifikasyon", "explanation": "Serum kalsiyumu normalken hasarlı, nekrotik veya dejenere dokularda kalsiyum tuzlarının çökmesi."},
            {"term": "Metastatik Kalsifikasyon", "explanation": "Hiperkalsemi durumunda normal dokularda (böbrek, akciğer, mide) kalsiyum çökmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kazeöz nekroz odaklarının iyileşirken kireçlenmesi 'distrofik kalsifikasyon' örneğidir.",
            "📌 [SINAV SPOTU] Distrofik kalsifikasyonda serum kalsiyum ve fosfat düzeyleri NORMALDİR."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kalsiyum Çöküşü", "desc": "Nekrotik fosfolipitlerin kalsiyumu bağlamasıyla oluşan hidroksiapatit kristalleri.", "isKey": True},
                {"title": "Laboratuvar Prensibi", "desc": "Serum kalsiyumu normaldir; lezyon lokal doku hasarına bağlıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Distrofik Kalsifikasyon vs Metastatik Kalsifikasyon",
                "Distrofik Kalsifikasyon",
                "Serum Ca2+ düzeyi NORMALDİR. Yalnızca ölü/hasarlı dokularda (kazeöz nekroz, aterom plağı) çökme olur.",
                "Metastatik Kalsifikasyon",
                "Serum Ca2+ düzeyi YÜKSEKTİR (hiperkalsemi). Sağlıklı dokularda (alveol, mide mukozası, böbrek tübülü) çökme olur."
            ),
            make_cloze(
                "İyileşen tüberküloz lezyonlarında serum kalsiyumu normalken nekrotik alanda kalsiyum çökmesine distrofik kalsifikasyon denir.",
                "distrofik kalsifikasyon",
                "Ölü dokularda normal kalsiyum düzeyinde kireçlenme türü"
            )
        ]
    })

    # ADIM 9 (CHECKPOINT 1)
    slides.append({
        "slideNumber": 9,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Kazeöz Nekroz ve Granülomatöz Yanıt",
        "subtitle": "Kazeöz nekrozun etiyolojisi, mikroskopisi, hücreleri ve ayırıcı tanısının konsolide sentezi",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 1,
        "synthesisNarrative": (
            "Bu kontrol noktasında, tüberkülozun doku hasar kalıbı olan kazeöz nekrozu ve onu sınırlayan "
            "granülomatöz yanıtı tüm boyutlarıyla pekiştiriyoruz.\n\n"
            "Kazeöz nekroz; Mycobacterium tuberculosis enfeksiyonunda görülen, makroskobik olarak sarı-beyaz, "
            "peynir kıvamında ve kırılgan, mikroskobik olarak ise hücresel hatları tamamen kaybolmuş amorf granüler "
            "eozinofilik bir harabiyet alanıdır.\n\n"
            "> [ÖZET REÇETE] Kazeöz merkez + Epitelioid histiyosit çiti + At nalı çekirdekli Langhans dev hücreleri "
            "+ Periferik lenfosit halkası = Tüberküloz Granülomu!\n\n"
            "Unutulmamalıdır ki kazeöz nekrozun iyileşmesi distrofik kalsifikasyon ile sonuçlanırken; "
            "bronşa açılması kavern kavitasyonuna ve yoğun basil yayılımına yol açar. "
            "Sarkoidoz ise merkezinde kazeöz nekroz İÇERMEYEN non-kazeifiye granülomlarla seyreder."
        ),
        "medicalTerms": [
            {"term": "Kazeöz Granülom", "explanation": "Merkezinde kazeöz nekroz bulunan, epitelioid histiyosit, dev hücre ve lenfositlerle çevrili nodüler kronik yangı."},
            {"term": "Langhans Hücresi", "explanation": "Granülomda at nalı dizilimli periferik çekirdekler içeren çok çekirdekli makrofaj türevi dev hücre."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Kazeöz nekroz = Tüberküloz, makroskopide peynir benzeri yumuşak kitle, mikroskopide amorf granüler silinmiş doku.",
            "📌 [CHECKPOINT ÖZETİ] Langhans dev hücreleri = At nalı dizilimli periferik çekirdekler.",
            "📌 [CHECKPOINT ÖZETİ] Sarkoidoz = Non-kazeifiye (nekrozsuz) granülom."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-01",
                "Kazeöz nekrozun en tipik etiyolojik nedeni ve mikroskobik en belirgin özelliği nedir?",
                "En tipik neden Mycobacterium tuberculosis enfeksiyonudur; mikroskopide doku mimarisi ve hücre hatları tamamen silinmiş amorf granüler pembe alan izlenir."
            ),
            make_flashcard(
                "fc-k1-05-02",
                "Langhans tipi dev hücrelerin patolojik ve nükleer özelliği nedir?",
                "Makrofajların birleşmesiyle oluşurlar ve onlarca çekirdek hücrenin periferinde at nalı / hilal şeklinde dizilir."
            ),
            make_flashcard(
                "fc-k1-05-03",
                "Kazeöz nekroz içeren granülomlar ile Sarkoidoz granülomları arasındaki temel fark nedir?",
                "Tüberkülozda kazeöz (peynirleşme) nekrozu varken, Sarkoidoz granülomlarında kazeöz nekroz bulunmaz (non-kazeifiye granülomdur)."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Kazeöz Nekroz ve Granülom Konsolide Tablosu",
                "headers": ["Patolojik Parametre", "Tüberküloz", "Sarkoidoz"],
                "rows": [
                    ["Nekroz Varlığı", "Var (Kazeöz / Peynirleşme)", "Yok (Non-kazeifiye)"],
                    ["Makroskopi", "Sarı-beyaz kırılgan peynir kırıntısı", "Sert, granüler gri nodüller"],
                    ["Dev Hücre Tipi", "Langhans (at nalı dizilimli)", "Langhans ve yabancı cisim tipi"],
                    ["Özel Boyama", "Ziehl-Neelsen (ARB (+))", "Mikroorganizma boyanmaz (Negatif)"],
                    ["Geç Dönem Sonu", "Distrofik kalsifikasyon / Kavern", "Fibröz skar / Organ disfonksiyonu"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Hastalık", "Granülom Türü", "Tipik Boyama Özelliği"],
                [
                    [("Tüberküloz", False, ""), ("Kazeifiye (Kazeöz nekrozlu)", True, "Peynirleşme nekrozu varlığı"), ("Ziehl-Neelsen pozitif kırmızı çomaklar", False, "")],
                    [("Sarkoidoz", False, ""), ("Non-kazeifiye (Nekrozsuz)", True, "Nekroz bulunmama durumu"), ("Mikroorganizma saptanmaz (negatif)", False, "")],
                    [("Kedi Tırmığı Hastalığı", False, ""), ("Süpüratif nekrotizan granülom", True, "Nötrofil içeren merkez"), ("Warthin-Starry gümüşleme boyası", False, "")]
                ]
            ),
            make_active_recall(
                "Kazeöz nekrozun iyileşme evresinde serum kalsiyumu normalken lezyonda taş sertliğinde kalsiyum birikmesine ne ad verilir?",
                "Distrofik kalsifikasyon adı verilir."
            )
        ]
    })

    # ADIM 10
    slides.append({
        "slideNumber": 10,
        "title": "Tüberküloz Dışı Kazeöz Odaklar: Mantar ve Parazit Enfeksiyonları",
        "subtitle": "Histoplazmoz ve koksidioidomikozda mikotik kazeöz nekroz patogenezi",
        "badge": "Enfeksiyon Patolojisi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Klinik pratikte kazeöz nekroz Mycobacterium tuberculosis ile özdeşleşmiş olsa da, bazı sistemik "
            "dimorfik mantar enfeksiyonları da akciğerde tüberkülozu birebir taklit eden kazeöz granülomlar yapabilir.\n\n"
            "Özellikle Histoplasma capsulatum ve Coccidioides immitis enfeksiyonlarında, mikroorganizma makrofajlar "
            "tarafından fagosite edilir ve dokuda geniş kazeöz nekroz alanları ile Langhans dev hücreleri gelişir.\n\n"
            "> [KLİNİK İPUCU] Tüberküloz kuşkusuyla incelenen ancak Ziehl-Neelsen boyasında ARB saptanamayan kazeöz "
            "lezyonlarda mutlaka GMS (Grocott Gomori Metenamin Gümüş) veya PAS boyası ile mantar aranmalıdır.\n\n"
            "GMS boyasında Histoplasma makrofajlar içinde küçük tomurcuklanan mayalar şeklinde siyah renkte görünür."
        ),
        "medicalTerms": [
            {"term": "Histoplasma capsulatum", "explanation": "Makrofajlar içinde yaşayan ve tüberküloza benzer kazeöz granülomlar oluşturan dimorfik mantar."},
            {"term": "GMS Boyası (Grocott)", "explanation": "Mantar duvarındaki polisakkaritleri siyaha boyayarak görünür kılan özel gümüşleme boyası."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Histoplazmoz ve koksidioidomikoz akciğerde kazeöz granülom oluşturan mantarlardır.",
            "📌 [SINAV SPOTU] Mikotik kazeöz lezyonlarda mantar elemanlarını göstermek için GMS veya PAS boyası kullanılır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mantar Mimikrisi", "desc": "Derin mikozların tüberküloza eşdeğer kazeöz nekroz yapabilmesi.", "isKey": True},
                {"title": "Tanısal Ayrım", "desc": "ZN negatifliğinde GMS veya PAS gümüşleme ile mantar kanıtı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Akciğerde kazeöz nekroz ve granülomatöz inflamasyon oluşturan ancak Ziehl-Neelsen boyamasında basil görülmeyen bir lezyonda mantar morfolojisini göstermek için hangi boya tercih edilir?",
                {
                    "A": "Prusya mavisi",
                    "B": "Grocott Metenamin Gümüş (GMS)",
                    "C": "Kongo kırmızısı",
                    "D": "Sudan black",
                    "E": "Alcian blue"
                },
                "B",
                {
                    "A": "Prusya mavisi demir (hemosiderin) boyasıdır.",
                    "B": "Doğru cevap B'dir: GMS (ve PAS) mantar duvarını göstermek için kullanılan standart histokimyasal boyadır.",
                    "C": "Kongo kırmızısı amiloid boyasıdır.",
                    "D": "Sudan black lipid boyasıdır.",
                    "E": "Alcian blue asidik müsin boyasıdır."
                }
            ),
            make_cloze(
                "Tüberküloza benzer şekilde akciğerde kazeöz nekroz yapan mantarları göstermek için GMS gümüşleme boyası kullanılır.",
                "GMS",
                "Mantar hücre duvarını siyaha boyayan histokimyasal yöntem kısaltması"
            )
        ]
    })

    return slides
