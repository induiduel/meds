"""
Akut Enflamasyon (Ders 9) - Bölüm 5: Vasküler Geçirgenlik Artış Mekanizmaları ve Eksüda
Slayt 41 - 50 (Checkpoint 5: Slayt 49)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "slideNumber": 41,
        "title": "Mikrovasküler Geçirgenlik Artışına Giriş: Kaçağın Biyolojisi",
        "subtitle": "Normal Starling dengesinin çöküşü ve protein zengini plazma sıvısının dokuya hücumu",
        "badge": "Geçirgenlik Temeli",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Akut enflamasyonun kardinal bulgusu olan 'Tumor' (ödem) rastgele bir sıvı birikimi değildir; "
            "damar endotel bariyerinin kontrollü veya kontrolsüz olarak delinmesinin doğrudan sonucudur.\n\n"
            "Fizyolojik şartlarda mikrovasküler endotel, plazma proteinlerinin (albümin, immünglobülinler, fibrinojen) "
            "damar dışına çıkmasına izin vermeyen yarı geçirgen dinamik bir filtredir. Starling dengesine göre kapiller "
            "hidrostatik basınç ile plazma kolloid onkotik basıncı birbirini dengeler; az miktarda sızan sıvı ise "
            "lenfatiklerce sessizce drene edilir.\n\n"
            "> **Enflamasyonda Ne Olur?**\n"
            "Enflamatuvar mediyatörler endotel bariyerini yıkar. Hücreler arasında 0.1 ila 1 mikrometre genişliğinde "
            "delikler (interendotelyal porlar) açılır. Ağır plazma proteinleri doku aralığına boşalır; su da osmozla "
            "onları takip ederek **akut enflamatuvar eksüdayı** meydana getirir."
        ),
        "medicalTerms": [
            {"term": "Vasküler Kaçak (Leakage)", "explanation": "Endotel bütünlüğünün bozularak plazma sıvı ve proteinlerinin doku interstisyumuna kontrolsüzce sızmasıdır."},
            {"term": "Starling Dengesi", "explanation": "Damar içi ve doku arası hidrostatik ve kolloid onkotik basınçların sıvı hareketini belirleyen fiziksel kurallarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonda ödemin asıl itici gücü hidrostatik basınçtan ziyade mikrovasküler GEÇİRGENLİK ARTIŞIDIR.",
            "📌 [SINAV SPOTU] Proteinlerin dokuya geçmesi interstisyel onkotik basıncı yükselterek suyu dokuda hapseder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bariyer Çöküşü", "desc": "Endotel bağlantıları açılarak proteinlere yol verir.", "isKey": True},
                {"title": "Eksüda Fışkırması", "desc": "Albümin ve fibrinojen dokuya çıkarak şişliği büyütür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Fizyolojik Endotel Bariyeri vs Enflamatuvar Vasküler Kaçak",
                "Fizyolojik Endotel Bariyeri",
                "Endotel hücreleri sıkı bağlantılarla kapalıdır, proteinler damarda kalır, interstisyuma sadece eser miktarda berrak sıvı sızar.",
                "Enflamatuvar Vasküler Kaçak",
                "Endotel hücreleri aralanır, porlar açılır, albümin ve antikorlar sel gibi dokuya akar, devasa eksüda ödemi gelişir."
            ),
            make_cloze(
                "Akut enflamasyonda plazma proteinlerinin ve suyun dokuya hücum ederek ödem oluşturmasından sorumlu anahtar mekanizma artmış mikrovasküler geçirgenlik tablosudur.",
                "geçirgenlik",
                "Endotel bariyerinin gevşeyerek moleküler geçirgenlik kazanması"
            )
        ]
    })

    # Slide 42
    slides.append({
        "slideNumber": 42,
        "title": "Mekanizma 1: Endotel Hücre Kasılması (Endothelial Cell Contraction)",
        "subtitle": "En yaygın mekanizma: Postkapiller venüllerde histamin ve bradikinin ile hızlı aralanma",
        "badge": "Anahtar Mekanizma",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Vasküler geçirgenlik artışının klinik ve deneysel olarak **en sık görülen** primer mekanizması "
            "**Endotel Hücre Kasılmasıdır (Endothelial Cell Contraction)**.\n\n"
            "- **Anatomik Sahne:** Yalnızca ve sadece **Postkapiller Venüllerde** (20-60 mikron çaplı) gerçekleşir; "
            "kapillerlerde veya arteriyollerde bu mekanizma görülmez.\n"
            "- **Mediyatörler:** Mast hücresi kaynaklı **Histamin**, kinin kaskadı kaynaklı **Bradikinin** ve "
            "lipoksijenaz kaynaklı **Lökotrienler (LTC4, LTD4, LTE4)** ile P maddesi.\n"
            "- **Moleküler Olay:** Mediyatörler G-protein kenetli reseptörlerine bağlanır; hücre içi serbest kalsiyum artar. "
            "Endotelin aktomiyozin sitoiskeleti kasılarak hücrenin büzüşmesine ve küçülmesine yol açar.\n"
            "- Komşu iki endotel arasındaki VE-kadherin bağlantıları ayrışır ve interendotelyal aralıklar açılır.\n"
            "- **Zamanlama:** Hasardan saniyeler sonra başlar, 15-30 dakikada zirve yapar ve hızla söner (**Ani Geçici Yanıt**)."
        ),
        "medicalTerms": [
            {"term": "Endotel Kasılması", "explanation": "Histamin ve bradikinin etkisiyle venül endotelinin aktin-miyozin ile büzüşüp interendotelyal porlar açmasıdır."},
            {"term": "VE-Kadherin", "explanation": "Endotel hücrelerini birbirine bağlayan ve kasılma anında ayrışan temel adhezyon molekülüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Vasküler geçirgenlik artışının EN SIK görülen mekanizması endotel hücre kasılmasıdır.",
            "📌 [SINAV SPOTU] Endotel kasılması YALNIZCA postkapiller venüllerde gerçekleşir ve 15-30 dakikada sonlanır.",
            "📌 [SINAV SPOTU] Histamin, bradikinin ve lökotrienler bu mekanizmanın klasik tetikleyicileridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "En Sık Mekanizma", "desc": "Aktomiyozin kasılmasıyla endoteller aralanır.", "isKey": True},
                {"title": "Yer ve Süre", "desc": "Sadece postkapiller venüllerde, 15-30 dakika sürer.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Histamin Aracılı Endotel Kasılması Zinciri",
                [
                    "1. Mast hücrelerinden boşalan histamin postkapiller venül endotelindeki H1 reseptörüne bağlanır",
                    "2. G-proteini aracılığıyla hücre içi serbest kalsiyum konsantrasyonu hızla yükselir",
                    "3. Miyozin hafif zincir kinazı (MLCK) aktive olarak aktomiyozin stres liflerini kasar",
                    "4. Endotel hücreleri büzüşür ve VE-kadherin bağlantıları ayrılarak interendotelyal porlar açılır",
                    "5. Plazma proteinleri bu aralıklardan dokuya sızarak ani geçici eksüdayı oluşturur"
                ]
            ),
            make_active_recall(
                "Akut enflasyonda histaminin yol açtığı vasküler geçirgenlik artışının sadece postkapiller venüllerle sınırlı kalmasının ve kapillerleri tutmamasının nedeni nedir?",
                "H1 histamin reseptörlerinin ve aktomiyozin kasılma aparatının en yoğun olarak postkapiller venül endotelinde eksprese edilmesi ve venül endotel bağlantılarının ayrılmaya en duyarlı yapıda olmasıdır."
            )
        ]
    })

    # Slide 43
    slides.append({
        "slideNumber": 43,
        "title": "Mekanizma 2: Doğrudan Endotel Hasarı ve Nekrozu (Direct Endothelial Injury)",
        "subtitle": "Şiddetli termal yanık, lütrik bakteriyel toksinler ve nekrotizan vaskülitlerin yarattığı masif yıkım",
        "badge": "Ağır Doku Hasarı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hafif uyaranlar endoteli sadece geçici olarak büzerken, şiddetli travmalar endotel hücresini doğrudan "
            "öldürür: **Doğrudan Endotel Hasarı (Direct Endothelial Injury)**.\n\n"
            "- **Etiyoloji:** Ağır termal yanıklar, kaynar su dökülmesi, dondurucu soğuk (frostbite), kostik asit/alkali "
            "maruziyeti, litik bakteriyel toksinler (örneğin gazlı kangrende Clostridium perfringens alfa-toksini) "
            "ve radyasyon hasarı.\n\n"
            "- **Anatomik Sahne:** Yalnızca venüller değil; **arteriyoller, kapillerler ve venüller dahil tüm mikrodolaşım "
            "seviyeleri** aynı anda tahrip olur.\n\n"
            "- **Patern:** Hasar anında endotel hücreleri lize olur, soyulur ve geride çıplak bazal membran kalır. "
            "Sızıntı hemen başlar ve tromboz gelişene veya endotel yeniden rejenere olana kadar saatlerce/günlerce "
            "kesintisiz sürer (**Ani Uzamış Yanıt**).\n\n"
            "> Çıplak kollojen açığa çıktığı için lümende hızla trombosit agregasyonu ve lokal mikrovasküler tromboz gelişir."
        ),
        "medicalTerms": [
            {"term": "Doğrudan Endotel Hasarı", "explanation": "Ağır fiziksel, kimyasal veya toksik ajanların endotel hücrelerini nekroza uğratarak damar duvarını soymasıdır."},
            {"term": "Soyulma (Denudasyon)", "explanation": "Nekrotik endotel hücrelerinin dökülmesiyle damar bazal membranının korumasız açığa çıkmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ağır yanıklarda ve litik toksinlerde geçirgenlik mekanizması DOĞRUDAN ENDOTEL HASARIDIR.",
            "📌 [SINAV SPOTU] Bu mekanizma tüm mikrovasküler yatakları (arteriyol, kapiller, venül) tutar ve günlerce sürer.",
            "📌 [SINAV SPOTU] Hasarlı alanda kaçak ancak mikrovasküler tromboz veya endotel tamiri ile durdurulabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücresel Nekroz", "desc": "Endotel parçalanır, damar lümeni çıplak kalır.", "isKey": True},
                {"title": "Tüm Yatak Tutulumu", "desc": "Arteriyol, kapiller ve venüllerin hepsi birden sızdırır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Endotel Kasılması vs Doğrudan Endotel Hasarı",
                "Endotel Kasılması (Histamin)",
                "Sadece venüllerde olur; hücre canlıdır ve büzüşür; 15-30 dakikada biter; hafif travmalarda görülür.",
                "Doğrudan Endotel Hasarı (Ağır Yanık)",
                "Tüm damar yatağını (arteriyol/kapiller/venül) tutar; hücreler nekroze olup dökülür; günlerce sürer."
            ),
            make_cloze(
                "Ağır termal yanık ve gazlı kangren toksinlerinde endotel hücrelerinin nekroza uğrayarak dökülmesi sonucu gelişen mekanizmaya doğrudan endotel hasarı denir.",
                "doğrudan endotel hasarı",
                "Fiziksel veya kimyasal yıkımla endotel soyulmasına yol açan mekanizma adı"
            )
        ]
    })

    # Slide 44
    slides.append({
        "slideNumber": 44,
        "title": "Mekanizma 3: Lökosit Bağımlı Endotel Hasarı (Leukocyte-Mediated Injury)",
        "subtitle": "Konağı korumaya gelen nötrofillerin reaktif oksijen radikalleri ve proteazlarla damarı delmesi",
        "badge": "İmmün Hasar",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Bazen enflamasyonda asıl hasar yapıcı mikrop değil, mikrobu yok etmek için gelen lökositin kendisidir: "
            "**Lökosit Bağımlı Endotel Hasarı (Leukocyte-Mediated Endothelial Injury)**.\n\n"
            "- **Mekanizma:** Lökositler (özellikle nötrofiller) venül endoteline sımsıkı tutunduklarında (adhezyon) "
            "veya kılcal kapiller damarlarda sıkışıp kaldıklarında aktive olurlar.\n"
            "- Fagozom dışına ve ortama kontrolsüzce **Reaktif Oksijen Türleri (ROS)** ve **lizozomal proteazlar "
            "(nötrofil elastazı, kollojenaz, katepsin G)** salgılarlar.\n"
            "- Bu toksik maddeler endotel hücre membranını lipid peroksidasyonuyla deler ve endotel nekrozuna yol açar.\n\n"
            "- **Klinik Sahne:** En belirgin olarak nötrofillerin en yoğun biriktiği **pulmoner kapiller yatakta "
            "(ARDS / Akut Solunum Sıkıntısı Sendromu)**, **glomerülonefritlerde** ve vaskülitlerde görülür."
        ),
        "medicalTerms": [
            {"term": "Lökosit Bağımlı Hasar", "explanation": "Damar duvarına tutunan nötrofillerin salgıladığı serbest radikaller ve proteazlarla endoteli tahrip etmesidir."},
            {"term": "ARDS", "explanation": "Akciğer kapillerlerinde biriken nötrofillerin endotel ve alveol epitelini parçalamasıyla gelişen ölümcül solunum yetmezliğidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] ARDS ve akut glomerülonefritteki vasküler hasarın ana mekanizması LÖKOSİT BAĞIMLI HASARDIR.",
            "📌 [SINAV SPOTU] Nötrofil elastazı ve ROS bu mekanizmanın iki temel öldürücü molekülüdür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kollateral Yıkım", "desc": "Nötrofil granülleri endoteli yakarak delikler açar.", "isKey": True},
                {"title": "Organ Tutulumu", "desc": "Akciğer (ARDS) ve böbrek glomerülleri en duyarlı sahalardır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "ARDS'de Lökosit Bağımlı Endotel Hasarı Zinciri",
                [
                    "1. Sepsis veya pankreatit kaynaklı sitokinler pulmoner kapiller yataktaki nötrofilleri aşırı aktive eder",
                    "2. Nötrofiller akciğer endoteline sımsıkı kenetlenir ve kapiller lümeninde göllenir",
                    "3. Aktive nötrofillerden hücre dışına yüksek miktarda süperoksit, hidroksil radikali ve elastaz boşalır",
                    "4. Kapiller endoteli ve alveoler tip I epitel nekroza uğrayarak soyulur",
                    "5. Alveol boşluklarına protein zengini eksüda ve hiyalen membranlar dolarak ARDS tablosu oturur"
                ]
            ),
            make_active_recall(
                "Akut Solunum Sıkıntısı Sendromunda (ARDS) alveol-kapiller bariyerin delinerek akciğerlerin sıvı ve fibrinle dolmasının primer hücresel sorumlusu hangisidir?",
                "Pulmoner kapiller yatakta birikerek kontrolsüzce reaktif oksijen radikalleri (ROS) ve nötrofil elastazı salgılayan polimorfonükleer nötrofillerdir (lökosit bağımlı hasar)."
            )
        ]
    })

    # Slide 45
    slides.append({
        "slideNumber": 45,
        "title": "Mekanizma 4 ve 5: Artmış Transsitoz ve Yeni Damar Sızıntısı",
        "subtitle": "Vezikülovakuoler organel (VVO) kanalları ve granülasyon dokusundaki pencereli anjiyogenez",
        "badge": "Özel Yollar",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Vasküler geçirgenlik sadece hücreler arasından değil, hücrenin içinden ve yeni doğan damarlardan da yürür:\n\n"
            "1. **Artmış Transsitoz (Transcitosiz):**\n"
            "- Bazı mediyatörler (özellikle **VEGF / Vasküler Endotelyal Büyüme Faktörü**) endotel hücresi içinde "
            "birbirine bağlı vezikül kanalları sistemini (**Vezikülovakuoler Organel - VVO**) aktive eder.\n"
            "- Makromoleküller lüminal zardan veziküle alınır, sitoplazmayı bir tünel gibi boydan boya geçerek "
            "abüminal (bazal) taraftan interstisyuma boşaltılır.\n\n"
            "2. **Yeni Damarlardan Sızıntı (Anjiyogenez ve Granülasyon Dokusu):**\n"
            "- Doku onarımı ve granülasyon dokusu oluşurken VEGF ve FGF etkisiyle tomurcuklanan yeni kapiller "
            "endotel hücreleri henüz olgunlaşmamıştır.\n"
            "- Hücreler arası interendotelyal bağlantılar eksik, bazal membran delik deşiktir.\n"
            "- Bu nedenle iyileşen bir yara dokusu veya tümör anjiyogenezi sürekli **ödemli ve sızıntılıdır**."
        ),
        "medicalTerms": [
            {"term": "Transsitoz", "explanation": "Makromoleküllerin endotel hücresini vezikülovakuoler kanallar yoluyla sitoplazma boyunca baştan başa geçmesidir."},
            {"term": "VVO (Vesiculovacuolar Organelle)", "explanation": "Endotel içinde yer alan ve VEGF uyarımıyla transsitoz tünelleri oluşturan vezikül kümesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] VEGF transsitozu artırarak ve yeni pencereli damarlar üreterek geçirgenliği en güçlü artıran faktördür.",
            "📌 [SINAV SPOTU] Granülasyon dokusunun ödemli olmasının nedeni olgunlaşmamış anjiyogenik damarların sızıntılı olmasıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Transsitoz Tünelleri", "desc": "VEGF uyarımıyla hücre içinden geçen veziküler yol.", "isKey": True},
                {"title": "İmmatür Damarlar", "desc": "Yeni oluşan kapillerlerin gevşek yapısı ödem yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Geçirgenlik Mekanizması", "Etkilenen Damar Segmenti", "Tetikleyici Mediyatör ve Klinik Özellik"],
                [
                    [("1. Endotel Kasılması", False, ""), ("Yalnızca Postkapiller Venüller", False, ""), ("Histamin, Bradikinin; 15-30 dk süren en sık mekanizma", True, "Hafif hasarlardaki ani geçici venüler yanıt")],
                    [("2. Doğrudan Endotel Hasarı", False, ""), ("Arteriyol, Kapiller ve Venüller", False, ""), ("Termal yanık, toksinler; günlerce süren ağır nekroz", True, "Tüm damar yatağını tutan kalıcı soyulma")],
                    [("3. Lökosit Bağımlı Hasar", False, ""), ("Venüller ve Pulmoner Kapillerler", False, ""), ("Aktive nötrofillerin ROS ve proteazları; ARDS tablosu", True, "Savunma hücrelerinin yarattığı kollateral hasar")],
                    [("4. Artmış Transsitoz", False, ""), ("Venüller ve Kapillerler", False, ""), ("VEGF; Vezikülovakuoler organel (VVO) kanallarından geçiş", True, "Hücre içi tünellerle makromolekül taşınması")],
                    [("5. Yeni Damar Sızıntısı", False, ""), ("Tomurcuklanan Yeni Kapillerler", False, ""), ("VEGF / Anjiyogenez; tam kapanmamış interendotelyal porlar", True, "İyileşen dokularda ve tümörlerde sızıntı")]
                ]
            ),
            make_cloze(
                "Doku onarımında ve tümör anjiyogenezinde hem yeni damar yapımını hem de transsitoz yoluyla aşırı vasküler geçirgenliği uyaran anahtar faktör VEGF faktörüdür.",
                "VEGF",
                "Vasküler Endotelyal Büyüme Faktörü ifadesinin evrensel kısaltması"
            )
        ]
    })

    # Slide 46
    slides.append({
        "slideNumber": 46,
        "title": "Beş Geçirgenlik Mekanizmasının Büyük Karşılaştırma Matrisi",
        "subtitle": "Zamanlama, anatomik lokalizasyon, mediyatör ve klinik prototip entegrasyonu",
        "badge": "Sentez Tablosu",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Patoloji sınavlarında ve klinik pratikte vasküler geçirgenliğin beş mekanizmasını birbirinden ayırt etmek "
            "kritik önem taşır. Her mekanizmanın özgül bir damar segmenti tercihi, zamansal paterni ve mediyatörü vardır:\n\n"
            "- Bir sivrisinek ısırığında veya ürtikerde dakikalar içinde şişen kabarcık **Endotel Kasılmasına** bağlıdır "
            "(venüller, histamin).\n"
            "- Üzerine kaynar çorba dökülen bir deride anında kabaran ve günlerce su toplayan büller **Doğrudan Endotel "
            "Hasarı** sonucudur (tüm damarlar, nekroz).\n"
            "- Güneş altında uyuyakalan birinde 6 saat sonra derinin alev alev yanması **Gecikmiş Uzamış Yanıttır** (kapiller/venül, sitokinler).\n"
            "- Pankreatit sonrası solunum yetmezliğine giren bir hastanın akciğerlerinin beyazlaşması **Lökosit Bağımlı Hasardır** (pulmoner kapillerler, nötrofil ROS)."
        ),
        "medicalTerms": [
            {"term": "Klinik Prototip", "explanation": "Belirli bir patolojik mekanizmayı en saf ve belirgin şekilde gösteren klasik hastalık tablosudur."},
            {"term": "Akut Bül", "explanation": "Doğrudan endotel ve epidermal hasar sonucu epidermis altında geniş eksüda sıvısının birikmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Histamin = Endotel kasılması = Postkapiller venüller.",
            "📌 [SINAV SPOTU] Yanık = Doğrudan endotel nekrozu = Arteriyol + Kapiller + Venül.",
            "📌 [SINAV SPOTU] ARDS = Lökosit bağımlı endotel hasarı = Pulmoner kapillerler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kasılma vs Nekroz", "desc": "Fonksiyonel geri dönüşlü venüler büzüşme vs tam doku ölümü.", "isKey": True},
                {"title": "Klinik Çeşitlilik", "desc": "Sivrisinek ısırığından ARDS ve yanığa kadar farklı mekanizmalar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Acil servise getirilen derin ikinci derece alev yanığı olan bir hastada hasar bölgesindeki masif sıvı kaybının ve vasküler geçirgenliğin altta yatan primer patolojik mekanizması nedir?",
                [
                    {"text": "Termal etkinin mikrovasküler endotel hücrelerini doğrudan nekroza uğratarak damar duvarını soyması (doğrudan endotel hasarı)", "isCorrect": True, "feedback": "Mükemmel tıp muhakemesi! Ağır termal travmada hücreler yaşayamaz; doğrudan lizisle tüm mikrosirkülasyonda masif ve günlerce süren kaçak oluşur."},
                    {"text": "Sadece postkapiller venüllerde histamin salgılanmasıyla oluşan 15 dakikalık geçici endotel kasılması", "isCorrect": False, "feedback": "Bu hafif travmalarda veya ürtikerde olur; ağır yanığı açıklayamaz."},
                    {"text": "Yalnızca yeni tomurcuklanan anjiyogenik damarların sızıntı yapması", "isCorrect": False, "feedback": "Anjiyogenez günler sonra onarım evresinde başlar, ani yanıkta henüz yoktur."}
                ]
            ),
            make_active_recall(
                "Vasküler geçirgenlik mekanizmaları içinde sadece postkapiller venüllerde gerçekleşen ve en sık görülen mekanizma hangisidir?",
                "Endotel hücre kasılmasıdır (Endothelial cell contraction); histamin ve bradikinin ile yürütülür."
            )
        ]
    })

    # Slide 47
    slides.append({
        "slideNumber": 47,
        "title": "Eksüdanın Moleküler Anatomisi: Neden Sıradan Su Değildir?",
        "subtitle": "İmmünglobülinler, kompleman, fibrinojen ve biyolojik savunma kalkanı",
        "badge": "Eksüda Biyokimyası",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Enflamasyonda damardan dışarı sızan eksüda sıvısı pasif bir su kaçağı değil; son derece organize bir "
            "**moleküler savunma kokteylidir**.\n\n"
            "Eksüdanın içerdiği hayati elemanlar:\n"
            "1. **Antikorlar (İmmünglobülinler / IgG, IgM):** Hasar bölgesindeki mikropların antijenlerine bağlanarak "
            "onları aglütine eder, toksinleri nötralize eder ve opsonize eder.\n"
            "2. **Kompleman Proteinleri:** C3b bakteriyi işaretlerken, C5a nötrofilleri çağırır; C5b-9 (MAC) kompleksleri "
            "bakteri zarını delerek eritir.\n"
            "3. **Fibrinojen ve Pıhtılaşma Faktörleri:** Doku faktörüyle temas eden fibrinojen hızla çözünmeyen "
            "**fibrin ağlarına** polimerize olur. Bu fibrin ağı enfeksiyon odağını bir kafes gibi sararak mikropların "
            "kana ve lenfe karışmasını mekanik olarak bloke eder.\n"
            "4. **Toksin Seyreltme:** Eksüdanın sıvı fazı bakteriyel ekzotoksinleri seyrelterek doku nekrozunun şiddetini düşürür."
        ),
        "medicalTerms": [
            {"term": "Fibrin Kafesi", "explanation": "Eksüdadaki fibrinojenin polimerize olmasıyla hasar odağını çevreleyen ve mikropların yayılmasını engelleyen ağ tabakasıdır."},
            {"term": "Opsonin", "explanation": "Patojen yüzeyini kaplayarak nötrofil ve makrofajların fagositozunu yüzlerce kat kolaylaştıran moleküldür (IgG, C3b)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Eksüdadaki fibrinojen dokuda fibrin ağı oluşturarak enfeksiyonun yayılmasını sınırlar.",
            "📌 [SINAV SPOTU] Eksüda antikor, kompleman ve antimikrobiyal peptitlerle dolu aktif bir savunma sıvısıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Antikor ve Kompleman", "desc": "Mikropları opsonize edip yok eden sıvısal ajanlar.", "isKey": True},
                {"title": "Fibrin Duvarı", "desc": "Mikroorganizmayı hasar odağında hapseden mekanik bariyer.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Enflamatuvar eksüda sıvısında bol bulunan ve dokuda polimerize olarak bakterilerin çevreye yayılmasını mekanik olarak engelleyen protein fibrinojen proteinidir.",
                "fibrinojen",
                "Karaciğerde üretilen ve pıhtılaşma kaskadında fibrin oluşturan plazma proteini"
            ),
            make_active_recall(
                "Akut enflasyonda doku aralığına protein ve sıvı sızmasının (eksüdasyon) konak savunması açısından sağladığı üç temel fayda nedir?",
                "1) Bakteriyel toksinleri seyrelterek lokal doku hasarını azaltmak, 2) Kandan antikor ve kompleman taşıyarak patojenleri opsonize edip öldürmek, 3) Fibrinojen getirerek mikropları hapseden fibrin bariyeri oluşturmaktır."
            )
        ]
    })

    # Slide 48
    slides.append({
        "slideNumber": 48,
        "title": "Geçirgenlik Artışının İlaçlarla Modülasyonu",
        "subtitle": "Antihistaminikler, lökotrien reseptör antagonistleri ve kortikosteroidlerin vasküler hedefleri",
        "badge": "Farmakoterapi",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "Vasküler geçirgenlik mekanizmalarının aydınlatılması, enflamatuvar ödem ve alerji tedavisinde kullanılan "
            "ilaçların etki prensiplerini oluşturur:\n\n"
            "- **Antihistaminikler (H1 Reseptör Antagonistleri / Setirizin, Difenhidramin):** Endotel H1 reseptörlerini "
            "kompetitif olarak bloke eder; histaminin endotel kasılması yapmasını ve venüler geçirgenlik artışını durdurur. "
            "Ürtiker ve alerjik rinitte kaşıntı ve şişliği anında söndürür.\n\n"
            "- **Lökotrien Reseptör Antagonistleri (Montelukast):** CysLT1 reseptörlerini bloke ederek lökotrienlerin "
            "(LTC4, LTD4) yaptığı güçlü venüler geçirgenlik artışını ve bronkospazmı önler; astım kontrolünde temel taştır.\n\n"
            "- **Kortikosteroidler (Deksametazon, Prednizolon):** Fosfolipaz A2'yi (lipokortin/anneksin-1 aracılığıyla) "
            "bloke eder; hem prostaglandin hem lökotrien sentezini kökten keser. Ayrıca endotel sıkı bağlantılarını "
            "(zonula occludens) genetik olarak güçlendirerek kapiller kaçağı durdurur."
        ),
        "medicalTerms": [
            {"term": "H1 Antagonisti", "explanation": "Histaminin venül endotelindeki H1 reseptörünü bloke ederek endotel kasılmasını ve ödemi engelleyen ilaç sınıfıdır."},
            {"term": "Lipokortin (Anneksin-1)", "explanation": "Kortikosteroidler tarafından indüklenen ve Fosfolipaz A2 enzimini inhibe ederek arakidonik asit çıkışını durduran proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Antihistaminikler endotel kasılmasını engelleyerek erken faz ürtiker ödemini durdurur.",
            "📌 [SINAV SPOTU] Kortikosteroidler Fosfolipaz A2 inhibisyonu ile hem COX hem LOX yolaklarını aynı anda kapatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "H1 Blokajı", "desc": "Histamin kaynaklı erken venüler sızıntıyı keser.", "isKey": True},
                {"title": "Steroid Gücü", "desc": "Tüm lipid mediyatör sentezini ve kapiller kaçağı durdurur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["İlaç Grubu", "Temel Moleküler Hedefi", "Vasküler Geçirgenlik Üzerindeki Etkisi"],
                [
                    [("H1 Antihistaminikler", False, ""), ("Endotel H1 reseptör blokajı", False, ""), ("Histamin aracılı erken endotel kasılmasını ve ödemi engeller", True, "Ürtikerde kaşıntı ve kabarıklığı hızla durdurur")],
                    [("Montelukast", False, ""), ("Sisteinil lökotrien CysLT1 reseptörü", False, ""), ("Lökotrien kaynaklı uzamış venüler sızıntıyı ve spazmı önler", True, "Astımda hava yolu mukozal ödemini azaltır")],
                    [("Kortikosteroidler", False, ""), ("Fosfolipaz A2 (PLA2) inhibisyonu", False, ""), ("Arakidonik asit kaskadını kökten kesip endotel bağlarını sıkılaştırır", True, "En güçlü genel anti-ödem ve anti-inflamatuvar etki")]
                ]
            ),
            make_cloze(
                "Akut ürtikerde ciltte hızla beliren kaşıntılı ödem plaklarını endotel kasılmasını bloke ederek engelleyen ilaç sınıfı H1 antihistaminikler sınıfıdır.",
                "antihistaminikler",
                "Histamin reseptörlerini kompetitif olarak kapatan klasik anti-alerjik ilaçlar"
            )
        ]
    })

    # Slide 49 (CHECKPOINT 5)
    slides.append({
        "slideNumber": 49,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Vasküler Geçirgenlik Mekanizmaları",
        "subtitle": "Bölüm 5 Endotel Kasılması, Nekroz, Lökosit Toksisitesi, Transsitoz ve Eksüda",
        "badge": "Checkpoint 5",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Beşinci kontrol noktasında mikrovasküler geçirgenlik artışının beş mekanizmasını özetliyoruz:\n\n"
            "1. **Endotel Hücre Kasılması:** En sık mekanizma. Yalnızca postkapiller venüllerde, histamin ve bradikinin ile, "
            "aktomiyozin kasılması, 15-30 dakikada biter (ani geçici yanıt).\n"
            "2. **Doğrudan Endotel Hasarı:** Termal yanıklar ve lütrik toksinler; endotel nekroza uğrayıp soyulur; "
            "arteriyol, kapiller ve venülleri tutar; günlerce sürer.\n"
            "3. **Lökosit Bağımlı Hasar:** Adhezyona uğrayan nötrofillerin ROS ve elastaz salması; ARDS ve glomerülonefrit.\n"
            "4. **Artmış Transsitoz:** VEGF uyarımıyla vezikülovakuoler organel (VVO) kanallarından hücre içi geçiş.\n"
            "5. **Yeni Damar Sızıntısı:** Anjiyogenezde pencereli, olgunlaşmamış endotel tomurcukları (granülasyon dokusu).\n"
            "6. **Eksüda Fonksiyonu:** Fibrinojenle fibrin kafesi kurar (sınırlar), antikor ve kompleman taşır (öldürür), toksinleri seyreltir."
        ),
        "medicalTerms": [
            {"term": "Geçirgenlik Spektrumu", "explanation": "Hafif histamin kasılmasından ağır yanık nekrozuna kadar damar kaçağının farklı dereceleridir."},
            {"term": "Litik Hasar", "explanation": "Toksin veya enzimlerle damar endotel hücre membranının fiziksel olarak parçalanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] En sık geçirgenlik mekanizması: Endotel kasılması (postkapiller venüller, histamin).",
            "📌 [SINAV SPOTU] Ağır yanıkta tüm mikrosirkülasyonu tutan mekanizma: Doğrudan endotel hasarıdır.",
            "📌 [SINAV SPOTU] ARDS'deki mekanizma: Lökosit bağımlı hasardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Venüler Kasılma", "desc": "Histamin ile en sık görülen erken geçici kaçak.", "isKey": True},
                {"title": "Pan-Vasküler Nekroz", "desc": "Ağır yanıkta tüm yatakların kalıcı yıkımı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Akut enflamasyonda mikrovasküler geçirgenlik artışına yol açan beş temel mekanizmayı adlarıyla sıralayınız?",
                "1) Endotel hücre kasılması (en sık), 2) Doğrudan endotel hasarı/nekrozu, 3) Lökosit bağımlı endotel hasarı, 4) Artmış transsitoz (VVO), 5) Yeni oluşan anjiyogenik damarlardan sızıntı."
            ),
            make_micro_quiz(
                "Akut pankreatit sonrası yoğun bakımda takip edilen bir hastada gelişen Akut Solunum Sıkıntısı Sendromunda (ARDS) alveolo-kapiller membranın geçirgenlik artışından sorumlu primer mekanizma hangisidir?",
                {
                    "A": "Endotel hücre kasılması",
                    "B": "Lökosit bağımlı endotel hasarı",
                    "C": "Vezikülovakuoler organellerle transsitoz",
                    "D": "Yeni kılcal damar tomurcuklanması",
                    "E": "Perisit apoptozu"
                },
                "B",
                {
                    "A": "Endotel kasılması hafif alerjik reaksiyonlarda olur.",
                    "B": "Doğru cevap B'dir: ARDS'de pulmoner kapillerlerde biriken nötrofillerin saldığı ROS ve proteazlar endoteli parçalar (lökosit bağımlı hasar).",
                    "C": "Transsitoz VEGF aracılıdır.",
                    "D": "Anjiyogenez geç dönem onarımdadır.",
                    "E": "Perisit kaybı diyabetik retinopatidedir."
                }
            ),
            make_cloze(
                "Vasküler geçirgenlik artış mekanizmaları içinde sadece postkapiller venüllerde gerçekleşen ve en sık görülen mekanizma endotel hücre kasılması mekanizmasıdır.",
                "endotel hücre kasılması",
                "Histamin etkisiyle hücre aktomiyozin iskeletinin büzüşmesi olayı"
            )
        ]
    })

    # Slide 50
    slides.append({
        "slideNumber": 50,
        "title": "Bölüm 5 Entegrasyonu: Ağır Yanık Hastasında Sıvı Resüsitasyonunun Mantığı",
        "subtitle": "Parkland formülü, evaporatif kayıp ve onkotik basınç dengesinin patolojik temeli",
        "badge": "Yoğun Bakım Entegrasyonu",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Geniş vücut yanığı (%40+) olan bir hastada gelişen vasküler patoloji doğrudan endotel hasarının devasa boyutunu gösterir:\n\n"
            "- Yanan alanlarda endotel hücreleri anında ölür; çıplak bazal membrandan litrelerce plazma doku aralığına ve dışarı boşalır.\n"
            "- Hasarlı bölgeden salınan masif sitokinler uzaktaki sağlam organ damarlarında da geçirgenliği artırır "
            "(sistemik kapiller kaçak sendromu).\n"
            "- Saatler içinde damar içi efektif kan hacmi tükenir; hasta derin **hipovolemik şoka** sürüklenir.\n\n"
            "> [KLİNİK PROTOKOL] Parkland formülü (4 mL x kg x %Yanık alanı) ile ilk 24 saatte verilen devasa izotonik "
            "sıvı miktarı (genellikle 10-15 litre kristaloid), işte bu doğrudan endotel nekrozu ve vasküler kaçağın "
            "damar yatağında açtığı dev deliği kompanse etmek için zorunludur."
        ),
        "medicalTerms": [
            {"term": "Parkland Formülü", "explanation": "Ağır yanık hastalarında vasküler kaçak ve hipovolemiyi önlemek için ilk 24 saatlik Ringer laktat ihtiyacını hesaplayan formüldür."},
            {"term": "Kapiller Kaçak Sendromu", "explanation": "Ağır travma veya sitokin fırtınasında tüm vücut mikrodolaşımının geçirgenleşerek plazmayı dokuya kaçırmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ağır yanıklarda hipovolemik şokun temel nedeni doğrudan endotel hasarıyla plazmanın dokuya kaçmasıdır.",
            "📌 [SINAV SPOTU] İlk 24 saatte kolloid değil kristaloid (Ringer laktat) tercih edilir; çünkü kolloidler de delik damardan dokuya sızıp ödemi artırabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Masif Kaçak", "desc": "Doğrudan hasarla damar içi sıvı interstisyuma dökülür.", "isKey": True},
                {"title": "Parkland Tedavisi", "desc": "Sıvı resüsitasyonu ile hipovolemik şok önlenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Ağır yanık hastalarında vasküler kaçağa bağlı gelişen hipovolemik şoku önlemek için ilk 24 saatte sıvı açığını hesaplayan standart klinik protokol Parkland formülü protokolüdür.",
                "Parkland",
                "Yanık resüsitasyonunda kullanılan ünlü formülün adı"
            ),
            make_active_recall(
                "Ağır yanık hastasında ilk 8 saatte albümin gibi kolloid sıvıların verilmesinin önerilmemesinin mikrovasküler patolojik gerekçesi nedir?",
                "Doğrudan endotel hasarı nedeniyle damar duvarında dev yarıklar bulunmasıdır; verilen albümin de damarda kalamayıp doku aralığına sızar, interstisyel onkotik basıncı artırarak doku ödemini daha da şiddetlendirir."
            )
        ]
    })

    return slides
