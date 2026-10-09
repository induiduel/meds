"""
Akut Enflamasyon (Ders 9) - Bölüm 1: Enflamasyonun Tanımı, Amacı ve Biyolojik Doğası
Slayt 1 - 10 (Checkpoint 1: Slayt 9)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "slideNumber": 1,
        "title": "Enflamasyonun Temel Tanımı: Vaskülarize Dokunun Koruyucu Kalkanı",
        "subtitle": "Zararlı etkenleri yok etmek ve doku onarımını başlatmak için damarlı dokunun verdiği dinamik yanıt",
        "badge": "Giriş ve Tanım",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Enflamasyon, vaskülarize (damarlı) canlı dokuların enfeksiyöz patojenlere, fiziksel/kimyasal hasara veya "
            "nekrotik hücre kalıntılarına karşı geliştirdiği en temel koruyucu konak savunma yanıtıdır. Enflamasyonun ana "
            "gayesi; hasar yapıcı etkeni sınırlandırmak, seyreltmek, nötralize etmek ve ortadan kaldırmaktır.\n\n"
            "> [KLİNİK İPUCU] Enflamasyon damarsız dokularda (örneğin normal avasküler kornea veya hyalin eklem kıkırdağı) "
            "doğrudan başlayamaz; yanıt mutlaka komşu vaskülarize dokulardan (limbus damarları veya sinovya) göç eden hücre "
            "ve plazma proteinleriyle yürütülür.\n\n"
            "Savunma araçları olan lökositler, antikorlar ve kompleman proteinleri normalde kan dolaşımında sessizce bekler. "
            "Doku hasarı oluştuğunda bu bileşenler damar dışına, interstisyel alana mobilize edilir."
        ),
        "medicalTerms": [
            {"term": "Enflamasyon", "explanation": "Damarlı dokuların enfeksiyon ve hücre hasarına karşı lökosit ve plazma proteinlerini dokuya göndererek verdiği konak savunma yanıtıdır."},
            {"term": "Vaskülarize Doku", "explanation": "İçerisinde kan ve lenf damar ağları barındıran canlı dokulardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enflamasyon yalnızca ve sadece damarlı dokularda gelişen bir yanıttır.",
            "📌 [SINAV SPOTU] Enflamatuvar yanıtın nihai amacı hem zararlı etkeni yok etmek hem de doku onarımını başlatmaktır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Savunma Yanıtı", "desc": "Zararlı ajanı sınırlama ve yok etme refleksidir.", "isKey": True},
                {"title": "Damar Bağımlılığı", "desc": "Plazma proteinleri ve lökositlerin damar yatağından dokuya transferi şarttır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Enflamasyon yalnızca damarlı dokularda gelişebilen dinamik ve koruyucu bir savunma reaksiyonudur.",
                "damarlı",
                "Yanıtın gelişebilmesi için kandan dokuya lökosit ve protein transferi sağlayan endotel ağını düşününüz"
            ),
            make_active_recall(
                "Avasküler bir doku olan korneanın santralinde gelişen bir hasarda enflamatuvar hücreler bölgeye nasıl ulaşır?",
                "Kornea avasküler olduğu için enflamasyon doğrudan merkezde başlayamaz; periferdeki limbus damarlarından ekstravaze olan nötrofiller kornea stroması boyunca hasar alanına göç eder."
            )
        ]
    })

    # Slide 2
    slides.append({
        "slideNumber": 2,
        "title": "Konak Savunmasında Enflamasyonun Yaşamsal Önemi",
        "subtitle": "Enflamasyon olmasaydı enfeksiyonlar hızla dissemine olur ve yaralar asla iyileşemezdi",
        "badge": "Fizyopatolojik Rol",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Enflamasyon olmasaydı insan vücudu basit bir bakteriyel çizik veya yüzeyel enfeksiyon karşısında bile "
            "savunmasız kalır; mikroorganizmalar kontrolsüzce çoğalarak dakikalar içinde letal sepsise yol açardı.\n\n"
            "> [TEMEL İLKE] Enflamatuvar süreç yalnızca mikropları temizlemekle kalmaz; nekrotik debrisin temizlenmesi, "
            "büyüme faktörlerinin salınması, anjiyogenez ve fibroblast proliferasyonu için gerekli moleküler mikroçevreyi hazırlar.\n\n"
            "Kalıtsal lökosit adhezyon eksikliği veya nötropenisi olan bireylerde kontrolsüz nekrotizan enfeksiyonların "
            "gelişmesi, enflamatuvar yanıtın mutlak gerekliliğinin en somut klinik kanıtıdır."
        ),
        "medicalTerms": [
            {"term": "Nötralizasyon", "explanation": "Patojenlerin toksinlerinin veya yüzey antijenlerinin antikor ve plazma proteinlerince etkisizleştirilmesidir."},
            {"term": "Debridman", "explanation": "Nekrotik doku artıklarının fagositoz yoluyla temizlenerek rejenerasyona zemin hazırlanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enflamasyon olmadan yara iyileşmesi ve skar dokusu oluşumu başlayamaz.",
            "📌 [SINAV SPOTU] Lökosit fonksiyon bozukluklarında tekrarlayan ve ölümcül pyojenik enfeksiyonlar gözlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enfeksiyon Bariyeri", "desc": "Mikropların kana ve uzak organlara yayılmasını engeller.", "isKey": True},
                {"title": "Onarımın Ön Koşulu", "desc": "Ölü doku temizlenmeden yeni doku mimarisi kurulamaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Enflamasyon Yeteneği Olan vs Olmayan Konak",
                "Normal Enflamatuvar Yanıt",
                "Bakteriler lokalize edilir, nötrofiller mikropları fagositozla öldürür, doku debride edilir ve tam iyileşme sağlanır.",
                "Enflamasyon Yeteneği Olmayan Konak",
                "Bakteriler engelsiz çoğalır, sistemik dolaşıma karışarak fulminan sepsise ve septik şoka neden olur."
            ),
            make_micro_quiz(
                "Enflamasyon yanıtı tamamen ortadan kaldırılmış bir deneysel modelde aşağıdakilerden hangisinin gerçekleşmesi beklenir?",
                {
                    "A": "Doku iyileşmesinin hızlanması",
                    "B": "Enfeksiyonların lokalize kalarak kendiliğinden sönmesi",
                    "C": "Basit bakteriyel kolonizasyonların bile yaygın dissemine doku nekrozuna ve ölüme yol açması",
                    "D": "Fibroblastların kontrolsüzce aşırı kollajen üretmesi",
                    "E": "Anjiyogenezin spontan olarak tetiklenmesi"
                },
                "C",
                {
                    "A": "Enflamasyon olmadan nekrotik doku temizlenemez, iyileşme başlayamaz.",
                    "B": "Lökositler ve kompleman olmadan mikroorganizmalar lokalize edilemez.",
                    "C": "Doğru cevap C'dir: Savunma hücreleri ve plazma proteinleri hasar alanına gelemediği için mikroplar dokuyu istila eder.",
                    "D": "Fibroblast proliferasyonu makrofaj kaynaklı büyüme faktörlerine muhtaçtır.",
                    "E": "Anjiyogenez enflamatuvar sitokinler ve VEGF ile uyarılır."
                }
            )
        ]
    })

    # Slide 3
    slides.append({
        "slideNumber": 3,
        "title": "İki Ucu Keskin Kılıç: Enflamasyonun Dokuya Verdiği Zararlar",
        "subtitle": "Savunma silahlarının (ROS, lizozomal enzimler) masum çevre parankimini tahrip etmesi",
        "badge": "Patolojik Potansiyel",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Enflamasyon hayat kurtarıcı bir mekanizma olmakla birlikte 'iki ucu keskin bir kılıçtır'. Lökositler "
            "mikropları yok etmek için ortama güçlü Reaktif Oksijen Türleri (ROS), proteolitik enzimler (elastaz, kollajenaz) "
            "ve kemokinler salgılarlar.\n\n"
            "> [KRİTİK UYARI] Bu mikrobisidal silahlar patojen ile konak hücresi arasında ayrım yapamaz; mikroçevredeki "
            "sağlıklı doku elemanları ve ekstrasellüler matriks de parçalanır.\n\n"
            "Bazı hastalıklarda (örneğin bakteriyel menenjit, ARDS veya tüberküloz) asıl ölümcül doku hasarı mikrobun "
            "kendisine değil, konağın verdiği aşırı ve kontrolsüz enflamatuvar yanıta bağlıdır."
        ),
        "medicalTerms": [
            {"term": "Kollateral Hasar", "explanation": "Savunma hücrelerinin çevreleyen sağlıklı dokuyu ikincil olarak yıkıma uğratmasıdır."},
            {"term": "Nötrofil Elastazı", "explanation": "Nötrofil granüllerinden salınan ve elastin ile matriks proteinlerini parçalayan güçlü serin proteazdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tüberküloz kavitesi ve ARDS tablosundaki akciğer harabiyeti lökosit kaynaklı immünopatolojik hasardır.",
            "📌 [SINAV SPOTU] Enflamatuvar mediyatörler sonlanma fazında frenlenemezse kronik doku yıkımı gelişir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Ayrım Gözetmeyen Silahlar", "desc": "ROS ve proteazlar endotel ve epitel hücrelerini de lize eder.", "isKey": True},
                {"title": "İmmünopatoloji", "desc": "Klinik semptomların büyük kısmı konağın kendi enflamatuvar tepkisinden kaynaklanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Enflamasyona Bağlı Doku Hasarı Mekanizması",
                [
                    "1. Nötrofiller hasar bölgesine aşırı miktarda göç eder ve aktive olur",
                    "2. Fagozom lizozomla kaynaşırken fago-lizozomal içerik hücre dışına sızar (regürjitasyon)",
                    "3. Doku interstisyumuna yüksek konsantrasyonda reaktif oksijen radikalleri ve nötrofil elastazı boşalır",
                    "4. Çevreleyen sağlıklı endotel ve parankim hücreleri nekroza uğrayarak kollateral doku hasarı meydana gelir"
                ]
            ),
            make_active_recall(
                "Akut bakteriyel menenjitte nörolojik sekellerin ve mortalitenin birincil sebebi mikroorganizmanın doğrudan etkisi midir?",
                "Hayır; subaraknoid mesafeye dolan masif nötrofil infiltratının salgıladığı sitokinler, proteazlar ve oluşan serebral ödemin yarattığı intrakraniyal basınç artışıdır."
            )
        ]
    })

    # Slide 4
    slides.append({
        "slideNumber": 4,
        "title": "Aşırı ve Uygunsuz Enflamatuvar Hastalıklar Spektrumu",
        "subtitle": "Otoimmünite, alerjik reaksiyonlar ve kronik dejeneratif süreçlerde enflamasyonun rolü",
        "badge": "Klinik Korelasyon",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Enflamasyonun patolojik boyut kazandığı üç temel klinik senaryo mevcuttur:\n\n"
            "1. **Otoimmün Hastalıklar:** İmmün sistemin kendi antijenlerine toleransı bozulur; romatoid artrit ve "
            "lupus gibi tablolarda vücut kendi eklemlerine ve damarlarına karşı sürekli bir enflamasyon yürütür.\n"
            "2. **Alerjiler ve Aşırı Duyarlılık:** Polen veya besin gibi zararsız çevresel antijenlere karşı hayatı tehdit eden "
            "astım veya anafilaktik enflamatuvar yanıtlar verilir.\n"
            "3. **Metabolik/Dejeneratif Hastalıklar:** Ateroskleroz, tip 2 diyabet ve Alzheimer gibi hastalıklarda düşük dereceli "
            "kalıcı enflamasyon organ disfonksiyonunu körükler."
        ),
        "medicalTerms": [
            {"term": "Otoantijen", "explanation": "Normal konak hücresinde bulunan ancak immün sistemce yabancı algılanarak hedeflenen yapıdır."},
            {"term": "Aşırı Duyarlılık", "explanation": "Zararsız antijenlere karşı kontrolsüz ve doku hasarı yaratan immün yanıt verilmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ateroskleroz steril bir lipid birikimi değil, damar duvarının kronik enflamatuvar hastalığıdır.",
            "📌 [SINAV SPOTU] Alerjilerde eozinofiller ve mast hücreleri başroldedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Otoimmün Saldırı", "desc": "Kendi dokusunu yabancı sayıp tahrip eden kronik yanıt.", "isKey": True},
                {"title": "Alerjik İnflamasyon", "desc": "Zararsız uyarana karşı abartılı ve yıkıcı reaksiyon.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hastalık Grubu", "Enflamatuvar Hedef / Tetikleyici", "Klinik Doku Hasarı"],
                [
                    [("Romatoid Artrit", False, ""), ("Eklem sinovyası ve kıkırdak otoantijenleri", False, ""), ("Sinovyal hipertrofi, pannus ve kıkırdak erozyonu", True, "Eklemlerde ankiloz ve fonksiyon kaybı yaratan lezyon")],
                    [("Bronşiyal Astım", False, ""), ("Zararsız çevresel alerjenler ve polenler", False, ""), ("Bronşial duvarda eozinofilik yangı ve bronkospazm", True, "Hava yolu obstrüksiyonu ve mukus tıkacı")],
                    [("Ateroskleroz", False, ""), ("Okside LDL kolesterol birikimi", False, ""), ("Damar intimasında makrofaj köpük hücreleri ve plak", True, "Lümen daralması ve trombotik oklüzyon riski")]
                ]
            ),
            make_cloze(
                "Romatoid artritte eklem harabiyetine yol açan temel patolojik süreç otoimmün enflamasyon zemininde gelişir.",
                "otoimmün",
                "Kendi antijenlerine karşı toleransın kırıldığı immünopatolojik mekanizmayı anımsayınız"
            )
        ]
    })

    # Slide 5
    slides.append({
        "slideNumber": 5,
        "title": "Akut ve Kronik Enflamasyonun Karşılaştırmalı Dinamiği",
        "subtitle": "Başlangıç hızı, hücresel kompozisyon, doku hasarı şiddeti ve lokal/sistemik belirtiler",
        "badge": "Temel Sınıflandırma",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Enflamatuvar yanıt zamansal seyrine ve patofizyolojik doğasına göre **akut** ve **kronik** olarak ikiye ayrılır.\n\n"
            "- **Akut Enflamasyon:** Dakikalar-saatler içinde hızla başlar, kısa sürer (birkaç gün). Temel hücresel aktörü "
            "==polimorfonükleer lökositlerdir (özellikle nötrofiller)==. Belirgin sıvı ve plazma proteini eksüdasyonu (ödem) görülür. "
            "Doku hasarı genellikle kendini sınırlar.\n\n"
            "- **Kronik Enflamasyon:** Günler-haftalar sonra yavaşça başlar veya akut yanıtın sonlanamamasıyla sürer. "
            "Temel hücreleri **mononükleer lökositlerdir (makrofajlar, lenfositler, plazma hücreleri)**. Eşzamanlı doku yıkımı "
            "ve anjiyogenez/fibrozis (skarlaşma) ile karakterizedir."
        ),
        "medicalTerms": [
            {"term": "Nötrofil", "explanation": "Akut enflamasyonun ilk 6-24 saatinde dokuya ilk ulaşan çok parçalı çekirdekli lökosittir."},
            {"term": "Mononükleer İnfiltrat", "explanation": "Kronik enflamasyonda görülen makrofaj, lenfosit ve plazma hücreleri topluluğudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun temel hücresi nötrofil, kronik enflamasyonun ise makrofaj ve lenfositlerdir.",
            "📌 [SINAV SPOTU] Fibrozis ve doku onarımı girişimleri kronik enflamasyonun ayırt edici özelliğidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Akut Form", "desc": "Hızlı başlangıç, nötrofil hakimiyeti, belirgin ödem.", "isKey": True},
                {"title": "Kronik Form", "desc": "Sinsi başlangıç, makrofaj/lenfosit hakimiyeti, fibrozis.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Akut Enflamasyon vs Kronik Enflamasyon",
                "Akut Enflamasyon",
                "Dakikalar içinde başlar; hakim hücre nötrofildir; belirgin sıvı ve fibrin eksüdasyonu vardır; hasar sınırlıdır.",
                "Kronik Enflamasyon",
                "Günler-haftalar sürer; hakim hücre makrofaj ve lenfosittir; belirgin anjiyogenez ve skar fibrozisi eşlik eder."
            ),
            make_active_recall(
                "Histopatolojik kesitte bol miktarda nötrofil ve ödem sıvısı görülmesi öncelikle hangi enflamasyon tipini işaret eder?",
                "Akut enflamasyonu işaret eder; çünkü nötrofiller akut fazın primer göstergesidir."
            )
        ]
    })

    # Slide 6
    slides.append({
        "slideNumber": 6,
        "title": "Akut Enflamasyonun Üç Majör Bileşeni",
        "subtitle": "Damar çapı değişimi, mikrovasküler sızıntı ve lökositlerin dokuya çıkışı",
        "badge": "Üç Ayaklı Mekanizma",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Akut enflamasyonun karmaşık tablosu incelendiğinde sürecin **üç temel vasküler ve hücresel bileşen** "
            "üzerinde yükseldiği görülür:\n\n"
            "1. **Damar Kalibresi Değişiklikleri (Vazodilatasyon):** Arteriyollerde genişleme meydana gelir; bu sayede "
            "hasarlı dokuya gelen kan akımı (hiperemi) katbekat artar.\n"
            "2. **Mikrovasküler Yapısal Değişiklikler (Geçirgenlik Artışı):** Endotel hücreleri kasılarak aralarında boşluklar "
            "açar; protein açısından zengin plazma sıvısı (eksüda) interstisyel alana sızar.\n"
            "3. **Lökosit Emigrasyonu ve Aktivasyonu:** Lökositler (başta nötrofiller) mikrodolaşımdan çıkarak hasar odağında "
            "birikir ve fagositoz için aktive olurlar."
        ),
        "medicalTerms": [
            {"term": "Kalibre Değişimi", "explanation": "Damar lümen çapının vazomotor yanıtlarla daralması veya genişlemesidir."},
            {"term": "Emigrasyon", "explanation": "Lökositlerin damar duvarını delip ekstravasküler interstisyuma göç etmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun 3 ana olayı: Vazodilatasyon, artmış vasküler geçirgenlik ve lökosit birikimidir.",
            "📌 [SINAV SPOTU] Bu üç olay dokuda kızarıklık, sıcaklık artışı ve şişlik bulgularını meydana getirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. Vazodilatasyon", "desc": "Kan akımını artırarak savunma elemanlarını hızla taşır.", "isKey": True},
                {"title": "2. Geçirgenlik", "desc": "Protein ve antikorların doku aralığına çıkışını sağlar.", "isKey": True},
                {"title": "3. Lökosit Göçü", "desc": "Patojeni yutacak ve parçalayacak hücreleri hedefe yığar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Akut Enflamasyonun Üçlü Kaskadı",
                [
                    "1. Hasar odağındaki mast hücreleri histamin salgılayarak prekapiller arteriyolleri genişletir",
                    "2. Kapiller yatakta hidrostatik basınç ve kan akımı şiddetle artarak lokal hiperemi gelişir",
                    "3. Postkapiller venüllerde endotel kasılmasıyla protein ve fibrinojen zengin eksüda dokuya sızar",
                    "4. Yavaşlayan kan akımıyla marginasyona uğrayan nötrofiller damar dışına çıkarak bakterileri kuşatır"
                ]
            ),
            make_cloze(
                "Akut enflamasyonda plazma proteinlerinin doku aralığına sızmasına neden olan temel vasküler değişiklik artmış vasküler geçirgenlik durumudur.",
                "vasküler geçirgenlik",
                "Damar duvarının sıvı ve makromoleküllere karşı geçirgen hale gelmesini ifade eden patolojik terim"
            )
        ]
    })

    # Slide 7
    slides.append({
        "slideNumber": 7,
        "title": "Enflamasyona Katılan Hücresel ve Sıvısal Elemanlar",
        "subtitle": "Dolaşımdaki lökositler, doku yerleşik bekçileri ve plazma protein sistemleri",
        "badge": "Savunma Ordusu",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Enflamasyon sahnesinde görev alan aktörler üç farklı anatomik kompartımandan mobilize edilir:\n\n"
            "- **Dolaşımdaki Hücreler:** Nötrofiller, eozinofiller, bazofiller, lenfositler, monositler ve trombositler.\n"
            "- **Doku Yerleşik Bekçi Hücreleri (Sentinels):** Hasarı ilk algılayan mast hücreleri, doku makrofajları "
            "(histiositler) ve dendritik hücrelerdir. Bu hücreler tehlikeyi algılayıp alarm sitokinleri (TNF, IL-1, histamin) salgılar.\n"
            "- **Plazma Protein Sistemleri:** Karaciğerde sentezlenen kompleman kaskadı proteinleri, pıhtılaşma/fibrinolitik "
            "faktörler ve kinin sistemi (bradikinin).\n"
            "- **Ekstrasellüler Matriks:** Kollajen lifleri, proteoglikanlar ve bazal membran lökositlerin tutunup yürüdüğü iskelettir."
        ),
        "medicalTerms": [
            {"term": "Sentinel Hücre", "explanation": "Dokularda nöbet tutarak patojen ve hasar paternlerini ilk algılayan nöbetçi hücrelerdir (makrofaj, mast, dendritik)."},
            {"term": "Kinin Sistemi", "explanation": "Kallikrein aracılığıyla bradikinin üreterek vazodilatasyon ve ağrı oluşturan plazma protein kaskadıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dokuda hasarı ilk sezen ve alarmı başlatan hücreler doku makrofajları ve mast hücreleridir.",
            "📌 [SINAV SPOTU] Kompleman sistemi hem doğrudan mikrop deler (MAC) hem de opsonizasyon ve kemotaksi sağlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dolaşım Ekibi", "desc": "Nötrofil ve monositler damardan çağrılır.", "isKey": True},
                {"title": "Nöbetçi Ekip", "desc": "Mast hücresi ve makrofajlar dokuda bekler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Savunma Kompartımanı", "Başlıca Temsilcileri", "Enflamasyondaki Anahtar Görevi"],
                [
                    [("Dolaşım Hücreleri", False, ""), ("Nötrofil, Monosit, Eozinofil", False, ""), ("Hedef dokuya göç ederek patojeni fagositozla öldürmek", True, "Hücresel yıkım ve sindirim sağlayan savunma işlevi")],
                    [("Doku Sentinelleri", False, ""), ("Mast hücresi, Makrofaj, Dendritik hücre", False, ""), ("PAMP ve DAMP algılayıp histamin ve sitokin salmak", True, "Alarm vererek damarları uyaran başlatıcı rol")],
                    [("Plazma Proteinleri", False, ""), ("Kompleman (C3a, C5a), Bradikinin, Fibrin", False, ""), ("Opsonizasyon, kemotaksi, vazodilatasyon ve pıhtılaşma", True, "Sıvısal aracıların yürüttüğü enzimatik kaskad")]
                ]
            ),
            make_active_recall(
                "Akut doku hasarında damarların dakikalar içinde genişlemesini sağlayan histamin öncelikle hangi hücreden salınır?",
                "Dokuda yerleşik bulunan ve granüllerinde hazır histamin depolayan mast hücrelerinden (ve dolaşımdaki bazofillerden) salınır."
            )
        ]
    })

    # Slide 8
    slides.append({
        "slideNumber": 8,
        "title": "Lokal Enflamasyondan Sistemik Yanıta: Akut Faz Tepkisi",
        "subtitle": "TNF-alfa, IL-1 ve IL-6 sitokinlerinin kemik iliği, hipotalamus ve karaciğer üzerindeki etkileri",
        "badge": "Sistemik Boyut",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "Enflamasyon şiddetli veya yaygın olduğunda lokal doku sınırlarını aşarak kana sitokin pompalar. "
            "Makrofaj kaynaklı **TNF-α, IL-1 ve IL-6** üçlüsü dolaşımla uzak organlara ulaşarak **Akut Faz Yanıtını** tetikler:\n\n"
            "- **Hipotalamus:** Prostaglandin E2 (PGE2) sentezi artar; termostat ayar noktası yükseltilerek **ateş (pireksi)** gelişir.\n"
            "- **Kemik İliği:** Hematopoez uyarılır; lökositoz (nötrofili) ortaya çıkar ve sola kayma (genç çomak nötrofiller) görülür.\n"
            "- **Karaciğer:** Akut faz reaktanları olan C-Reaktif Protein (CRP), Serum Amiloid A (SAA) ve fibrinojen sentezi tavan yapar; sedimantasyon (ESR) hızlanır.\n\n"
            "> Aşırı sitokin deşarjı (sitokin fırtınası) vazodilatasyon ve kapiller kaçakla septik şoka götürür."
        ),
        "medicalTerms": [
            {"term": "Akut Faz Yanıtı", "explanation": "İnflamatuvar sitokinlerin etkisiyle karaciğer, kemik iliği ve hipotalamusta oluşan sistemik reaksiyonlar bütünüdür."},
            {"term": "Sola Kayma", "explanation": "Kemik iliğinden kana immatür (çomak/bant) nötrofil salınımının artmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hipotalamusta ateş oluşturan temel mediyatör PGE2, onu uyaran sitokinler ise IL-1 ve TNF'dir.",
            "📌 [SINAV SPOTU] Karaciğerden CRP ve fibrinojen sentezini en güçlü uyaran sitokin IL-6'dır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Ateş Mekanizması", "desc": "Hipotalamik PGE2 senteziyle vücut ısısının artırılması.", "isKey": True},
                {"title": "Karaciğer Yanıtı", "desc": "CRP, SAA ve fibrinojen salınımında patlama.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Ateş, lökositoz (18.000/mm3, %15 çomak) ve CRP yüksekliği saptanan bir hastada bu sistemik bulguların patogenezini sorguluyorsunuz. Hangi moleküler eksen bu tabloyu doğrudan yönetmektedir?",
                [
                    {"text": "Hasar bölgesindeki makrofajlardan salınan TNF-alfa, IL-1 ve IL-6 sitokinlerinin hipotalamus, kemik iliği ve hepatositleri uyarması", "isCorrect": True, "feedback": "Kusursuz tıp bilgisi! Akut faz yanıtının orkestra şefleri bu üç pro-enflamatuvar sitokindir."},
                    {"text": "Bakterilerin endotel hücrelerini doğrudan fagosite ederek kana eritrosit salması", "isCorrect": False, "feedback": "Bakteriler endoteli fagosite etmez; eritrosit değil lökosit artar."},
                    {"text": "Kemik iliğinde eritropoetin salgısının artmasıyla kanda pıhtılaşma faktörlerinin tükenmesi", "isCorrect": False, "feedback": "Eritropoetin eritrosit yapar, lökositoz ve akut faz sitokinlerle tetiklenir."}
                ]
            ),
            make_micro_quiz(
                "Enflamasyonda karaciğerden C-Reaktif Protein (CRP) ve fibrinojen üretimini doğrudan ve en güçlü şekilde uyaran sitokin hangisidir?",
                {
                    "A": "İnterlökin-6 (IL-6)",
                    "B": "İnterlökin-4 (IL-4)",
                    "C": "Transforme edici büyüme faktörü-beta (TGF-β)",
                    "D": "İnterlökin-10 (IL-10)",
                    "E": "İnterferon-gama (IFN-γ)"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Hepatositlerde akut faz reaktanı genlerinin transkripsiyonunu indükleyen primer sitokin IL-6'dır.",
                    "B": "IL-4 Th2 yanıtı ve IgE sınıf değişiminde rol oynar.",
                    "C": "TGF-β anti-enflamatuvar ve fibrogenik bir sitokindir.",
                    "D": "IL-10 enflamasyonu baskılayan inhibitör sitokindir.",
                    "E": "IFN-γ makrofajları aktive eden granülomatöz sitokindir."
                }
            )
        ]
    })

    # Slide 9 (CHECKPOINT 1)
    slides.append({
        "slideNumber": 9,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Enflamasyonun Tanımı, Amacı ve Genel Prensipleri",
        "subtitle": "Bölüm 1 Temel Kavramlar, Fayda-Zarar Dengesi, Akut vs Kronik ve Sistemik Yanıt",
        "badge": "Checkpoint 1",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "İlk kontrol noktasında enflamasyonun temel felsefesini ve mimarisini özetliyoruz:\n\n"
            "1. **Enflamasyon Tanımı:** Vaskülarize dokuların hasar ve enfeksiyonu sınırlamak ve onarımı başlatmak "
            "için verdiği dinamik konak yanıtıdır. Damarsız dokularda primer olarak başlayamaz.\n"
            "2. **Çift Yönlü Bıçak:** Mikropları öldüren ROS ve nötrofil elastazı masum çevre dokuyu da lize ederek "
            "kollateral doku hasarı (menenjit, ARDS, apse) oluşturabilir.\n"
            "3. **Akut vs Kronik:** Akut form saatler içinde başlar, nötrofil hakimiyetindedir ve zengin eksüdasyon içerir. "
            "Kronik form günler-haftalar sürer, makrofaj/lenfosit hakimdir ve fibrozis ile doku yıkımı bir aradadır.\n"
            "4. **Üç Ana Ayak:** Arteriyoler vazodilatasyon, artmış vasküler geçirgenlik ve lökosit göçü/aktivasyonu.\n"
            "5. **Sistemik Akut Faz:** Makrofaj kaynaklı TNF-α, IL-1 ve IL-6; ateşi (hipotalamik PGE2), lökositozu (kemik iliği) "
            "ve akut faz proteinlerini (karaciğer CRP, fibrinojen) yönetir."
        ),
        "medicalTerms": [
            {"term": "Akut Faz Proteini", "explanation": "İnflamasyon sırasında karaciğerde sentezi katlanarak artan CRP, SAA ve fibrinojen gibi plazma molekülleridir."},
            {"term": "Kollateral Yıkım", "explanation": "Savunma hücrelerinin hedef patojeni imha ederken çevreleyen konak mimarisine verdiği ikincil hasardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun primer hücresi nötrofil, kronik enflamasyonun ise makrofajdır.",
            "📌 [SINAV SPOTU] Sistemik akut faz reaksiyonunda ateşin mediyatörü PGE2, karaciğer CRP sentezinin uyaranı IL-6'dır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Damar Şartı", "desc": "Avasküler dokularda lokal vasküler reaksiyon başlayamaz.", "isKey": True},
                {"title": "Sitokin Triadı", "desc": "TNF, IL-1 ve IL-6 lokal yangıyı sistemik cevaba dönüştürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Akut enflamasyonun lokal odağından salınan TNF ve IL-1'in hipotalamustaki termoregülatuar merkezi uyararak ateş oluşturma mekanizması nedir?",
                "Hipotalamik vasküler ve perivasküler hücrelerde Siklooksijenaz (COX) enzimini uyararak Prostaglandin E2 (PGE2) sentezini artırırlar; PGE2 hipotalamik termostatı daha yüksek bir ısı derecesine ayarlar."
            ),
            make_cloze(
                "Akut enflamasyonun hücresel karakteristiğini belirleyen ve ilk saatlerde dokuya göç eden hakim hücre nötrofil hücresidir.",
                "nötrofil",
                "Polimorfonükleer lökosit ailesinin en kalabalık ilk savunma neferi"
            ),
            make_before_after(
                "Lokal Enflamatuvar Odak vs Sistemik Akut Faz Yanıtı",
                "Lokal Enflamatuvar Odak",
                "Hasar bölgesinde sınırlı kızarıklık, şişlik, sıcaklık, ağrı ve fonksiyon kaybı gözlenir.",
                "Sistemik Akut Faz Yanıtı",
                "Ateş, halsizlik, lökositoz, sola kayma, taşikardi, CRP ve sedimantasyon yüksekliği tüm vücudu sarar."
            )
        ]
    })

    # Slide 10
    slides.append({
        "slideNumber": 10,
        "title": "Bölüm 1 Entegrasyonu: Patoloji Laboratuvarından Kliniğe",
        "subtitle": "Kandaki biyobelirteçler ile dokudaki enflamatuvar sürecin birebir eşleşmesi",
        "badge": "Laboratuvar ve Klinik",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Bir klinisyen enflamatuvar süreci takip ederken hem lokal muayene bulgularını hem de laboratuvar testlerini "
            "bütünleştirmelidir. Akut apandisitte McBurney noktasındaki hassasiyet lokal peritonit ve enflamatuvar sinir "
            "uyarısını gösterirken, kandaki 16.000 lökosit ve yüksek CRP sistemik sitokin yayılımını belgeler.\n\n"
            "> [KLİNİK İPUCU] Fibrinojen artışı eritrositlerin birbirine yapışarak kümelenmesini (rulo formasyonu) "
            "kolaylaştırır; bu durum laboratuvarda **Eritrosit Sedimantasyon Hızının (ESR)** yükselmesi olarak ölçülür.\n\n"
            "Enflamasyon çözüldüğünde anti-enflamatuvar sitokinler (IL-10, TGF-β) devreye girer, nötrofiller apoptoza gider "
            "ve laboratuvar parametreleri normale döner."
        ),
        "medicalTerms": [
            {"term": "Rulo Formasyonu", "explanation": "Fibrinojenin eritrositlerin negatif yüzey yükünü nötralize ederek madeni para gibi üst üste dizilmelerini sağlamasıdır."},
            {"term": "Rezolüsyon", "explanation": "Enflamasyon etkeninin temizlenip dokunun tamamen eski sağlıklı anatomik yapısına dönmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Eritrosit sedimantasyon hızındaki (ESR) artışın temel moleküler sebebi plazma fibrinojen konsantrasyonunun yükselmesidir.",
            "📌 [SINAV SPOTU] Enflamasyonun fizyolojik olarak sönümlenmesinde IL-10 ve TGF-beta kilit rol oynar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "ESR Mantığı", "desc": "Fibrinojen eritrositleri ağırlaştırarak çökmeyi hızlandırır.", "isKey": True},
                {"title": "Sönümlenme", "desc": "Spontan apoptoz ve inhibitör sitokinlerle yangı durdurulur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Eritrosit sedimantasyon hızının enflamasyonda belirgin şekilde yükselmesinin temel nedeni plazmada artan fibrinojen proteinidir.",
                "fibrinojen",
                "Karaciğerden salınan ve eritrositlerin rulo oluşturmasını kolaylaştıran pıhtılaşma faktörü"
            ),
            make_active_recall(
                "Akut faz yanıtında lökositoza neden olan nötrofillerin kemik iliği rezervinden hızla kana dökülmesini sağlayan temel büyüme faktörleri ve sitokinler hangileridir?",
                "Koloni uyarıcı faktörler (G-CSF ve GM-CSF) ile TNF ve IL-1 sitokinleridir; kemik iliğindeki post-mitotik nötrofil havuzunu hızla periferik kana boşaltırlar."
            )
        ]
    })

    return slides
