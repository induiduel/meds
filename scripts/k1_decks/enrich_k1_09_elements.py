"""
Akut Enflamasyon (Ders 9) İnteraktif Öğe Zenginleştirme Modülü.
Çeşitlilik kuralı gereğince tüm 7 türün her birinin >= %8.0 olmasını temin eder.
"""

from .k1_09_deck_data.helpers import (
    make_micro_quiz, make_branching_logic, make_causal_chain
)

def get_extra_branching():
    """Ekstra dallanan klinik senaryolar (branching_logic)"""
    return {
        2: make_branching_logic(
            "Ciltte derin bir cam kesiği olan bir hastada primer yara bakımını yönetiyorsunuz. Enflamatuvar yanıtı tamamen baskılayıcı yüksek doz immünsüpresif vermek yara iyileşmesini nasıl etkiler?",
            [
                {"text": "Nötrofil ve makrofaj göçü duracağı için nekrotik dokular temizlenemez, büyüme faktörleri salınamaz ve yara iyileşmesi tamamen durur", "isCorrect": True, "feedback": "Kusursuz tıp muhakemesi! Enflamasyon onarımın zorunlu birinci basamağıdır; tamamen baskılanması iyileşmeyi felç eder."},
                {"text": "Enflamasyon baskılandığı için yara saniyeler içinde iz bırakmadan (skar olmadan) hızla iyileşir", "isCorrect": False, "feedback": "Enflamasyon olmadan granülasyon dokusu kurulamaz."},
                {"text": "Sadece epitel hücreleri kontrolsüzce çoğalarak keloid oluşturur", "isCorrect": False, "feedback": "Büyüme faktörü olmadan epitelizasyon da gecikir."}
            ]
        ),
        12: make_branching_logic(
            "Yüzeyel selülit şüphesi olan bir hastanın bacağındaki parlak kırmızı, sıcak ve şiş lezyonu değerlendiriyorsunuz. Bu lokal aktif hiperemiyi kırmak için acil yaklaşımınız ne olmalıdır?",
            [
                {"text": "Buz veya soğuk uygulama yaparak arteriyollerin vazokonstriksiyonunu sağlamak ve lokal kan akımını azaltmak", "isCorrect": True, "feedback": "Çok doğru! Soğuk uygulama vazokonstriksiyon yaparak aktif hiperemiyi, ödem oluşumunu ve ağrıyı hafifletir."},
                {"text": "Bölgeye sıcak kompres uygulayarak arteriyolleri daha da genişletmek", "isCorrect": False, "feedback": "Sıcak uygulamak hiperemiyi ve ödemi şiddetlendirir."},
                {"text": "Bölgeye doğrudan intraarteriyel nitrik oksit enjekte etmek", "isCorrect": False, "feedback": "NO vazodilatatördür, hiperemiyi patlatır."}
            ]
        ),
        22: make_branching_logic(
            "Üriner sistem enfeksiyonu ve ateş yüksekliğiyle başvuran bir hastada E. coli bakterisinin endotoksinine (LPS) karşı konağın ilk moleküler alarmı nasıl tetiklenir?",
            [
                {"text": "Dolaşımdaki ve dokudaki makrofajların yüzeyindeki TLR4/MD-2 kompleksinin LPS'yi bağlayarak NF-kappaB'yi aktive etmesi", "isCorrect": True, "feedback": "Kusursuz moleküler bilgi! Gram-negatif bakterilerin endotoksinini algılayan primer sensör TLR4'tür."},
                {"text": "Bakteriyel çift zincirli RNA'nın endozomal TLR3 reseptörüne bağlanması", "isCorrect": False, "feedback": "TLR3 viral dsRNA sensörüdür, bakteriyel LPS'yi tanımaz."},
                {"text": "Bakteriyel kamçının sitozolik NLRP3 inflamazomunu doğrudan delmesi", "isCorrect": False, "feedback": "Flagellin TLR5 ile tanınır."}
            ]
        ),
        32: make_branching_logic(
            "Arı sokması sonrası 5 dakika içinde tüm vücudunda kızarıklık, yaygın ürtiker ve nefes darlığı gelişen bir hastada arteriyoler vazodilatasyon ve hipotansiyonu durdurmak için ilk tercih edilecek ilaç hangisidir?",
            [
                {"text": "İntramusküler Epinefrin (Adrenalin); çünkü alfa-1 reseptörleriyle damarları büzer, beta-2 ile bronkodilatasyon sağlar ve mast hücre degranülasyonunu durdurur", "isCorrect": True, "feedback": "Hayat kurtaran klinik karar! Anafilaksinin bir numaralı acil ilacı intramusküler adrenalindir."},
                {"text": "Sadece oral parasetamol verilerek hastanın ateşi düşürülmelidir", "isCorrect": False, "feedback": "Parasetamol vazodilatatör şoku ve bronkospazmı önleyemez."},
                {"text": "İntravenöz yüksek doz nitrik oksit donörü verilmelidir", "isCorrect": False, "feedback": "Hipotansiyonu derinleştirerek kardiyak arreste yol açar."}
            ]
        ),
        42: make_branching_logic(
            "Akut alerjik rinit atağında burun tıkanıklığı ve mukozal ödem gelişen bir hastada histamin aracılı vasküler geçirgenlik artışını durdurmak için hangi reseptör bloke edilmelidir?",
            [
                {"text": "Postkapiller venül endotelindeki H1 histamin reseptörleri", "isCorrect": True, "feedback": "Doğru farmakolojik hedef! Endotel kasılması ve geçirgenlik artışı H1 reseptörleri üzerinden yürütülür."},
                {"text": "Mide pariyetal hücrelerindeki H2 histamin reseptörleri", "isCorrect": False, "feedback": "H2 asit salgısını düzenler, mukozal ödemi değil."},
                {"text": "Santral sinir sistemindeki H3 presinaptik otoreseptörleri", "isCorrect": False, "feedback": "H3 nörotransmitter salınımını denetler."}
            ]
        ),
        52: make_branching_logic(
            "Karın ağrısı ve distansiyonla başvuran bir siroz hastasından alınan asit sıvısının protein düzeyi 1.2 g/dL, dansitesi 1.009 ve lökosit sayısı 120/mm3 bulunuyor. Bu sıvının doğası hakkında ne söylersiniz?",
            [
                {"text": "Damar geçirgenliği normal olan, portal hipertansiyon ve hipoalbüminemi kaynaklı tipik bir transüdadır", "isCorrect": True, "feedback": "Harika tıp muhakemesi! Düşük dansite (<1.012) ve düşük protein (<3 g/dL) saf transüda göstergesidir."},
                {"text": "Bakteriyel peritonite bağlı yüksek proteinli pürülan eksüdadır", "isCorrect": False, "feedback": "Bakteriyel peritonit eksüda yapar; lökosit binlerce ve protein yüksek olur."},
                {"text": "Tüberküloz peritonitine bağlı lenfositik eksüdadır", "isCorrect": False, "feedback": "Tüberküloz eksüda karakterindedir."}
            ]
        ),
        62: make_branching_logic(
            "Tekrarlayan derin cilt nekrozları olan ancak yaralarında hiç irin (pus) saptanmayan bir bebekte integrin beta-2 zinciri (CD18) eksikliği tespit ediliyor. Bu bebeğin kemik iliği nakli öncesi yönetiminde en kritik ilke nedir?",
            [
                {"text": "Lökositler dokuya çıkamadığı için bakteriyel enfeksiyonlar hızla fulminan sepsise ilerleyebilir; profilaktik ve erken agresif antibiyoterapi hayatidir", "isCorrect": True, "feedback": "Kusursuz pediatrik patoloji yaklaşımı! LAD-1 hastaları doku savunması yapamadığı için sepsise son derece açıktır."},
                {"text": "Hastaya yüksek doz damar genişletici histamin infüzyonu verilmelidir", "isCorrect": False, "feedback": "Sorun damar çapında değil, lökosit integrinindedir."},
                {"text": "Yaraların iyileşmesi için lökositleri öldüren sitotoksik kemoterapi verilmelidir", "isCorrect": False, "feedback": "Mevcut az sayıdaki savunmayı da yok eder."}
            ]
        ),
        72: make_branching_logic(
            "Akut apandisit şüphesiyle ameliyata alınan bir hastanın apandiks lümeninden perivasküler dokuya nötrofillerin transmigrasyonunu (diapedez) yerinde durdurmak isteseydiniz hangi moleküler hedefi nötralize ederdiniz?",
            [
                {"text": "Endotel ve nötrofil hücreler arası kavşağında homofilik bağlanma yapan PECAM-1 (CD31) molekülünü", "isCorrect": True, "feedback": "Tam isabet! PECAM-1 diapedezin vazgeçilmez köprüsüdür; blokajı lökositi damar içinde tutar."},
                {"text": "Yalnızca karaciğerde sentezlenen fibrinojen molekülünü", "isCorrect": False, "feedback": "Fibrinojen pıhtılaşmadadır, diapedez köprüsü değildir."},
                {"text": "Trombositlerin alfa granüllerindeki PDGF molekülünü", "isCorrect": False, "feedback": "PDGF fibroblastları uyarır, transmigrasyonu değil."}
            ]
        ),
        82: make_branching_logic(
            "Splenektomi (dalağı alınmış) geçiren bir hastada kapsüllü Streptococcus pneumoniae bakterilerine karşı fagositoz yeteneğinin ağır şekilde düşmesinin temel nedeni nedir?",
            [
                {"text": "Dalağın en önemli IgM ve opsonin üretim merkezi olması ve dalak makrofajlarının opsonize mikropları temizleme fonksiyonunun kaybolması", "isCorrect": True, "feedback": "Mükemmel klinik bilgi! Dalak kapsüllü bakterilerin opsonizasyon ve fagosite edilmesinde kritik organdır; yokluğunda aşılanma şarttır."},
                {"text": "Dalağın vücuttaki tek nötrofil üreten organ olması", "isCorrect": False, "feedback": "Nötrofilleri kemik iliği üretir, dalak değil."},
                {"text": "Dalağın yokluğunda karaciğerin albümin üretememesi", "isCorrect": False, "feedback": "Albümin sentezi karaciğerin görevidir."}
            ]
        ),
        92: make_branching_logic(
            "Diz ekleminde ani başlayan şiddetli ağrı, şişlik ve ısı artışı olan bir hastadan eklem sıvısı aspire ediliyor. Sıvı berrak açık sarı renkte, lökosit sayısı 800/mm3 ve mikroskopta kristal saptanmıyor. Bu tabloyu nasıl yorumlarsınız?",
            [
                {"text": "Süpüratif bakteriyel veya kristal artritinden ziyade, hafif mekanik veya dejeneratif bir seröz efüzyon lehinedir", "isCorrect": True, "feedback": "Çok doğru! Bakteriyel artritte sıvı pürülan/bulanık ve lökosit >50.000 olur; 800 lökositli berrak sıvı seröz efüzyondur."},
                {"text": "Acil cerrahi artrotomi gerektiren fulminan pürülan septik artrittir", "isCorrect": False, "feedback": "Septik artritte sıvı irinlidir, berrak olamaz."},
                {"text": "Eklem içinde yaygın fibrinoid nekroz ve kazeifikasyon mevcuttur", "isCorrect": False, "feedback": "Kazeifikasyon tüberkülozda olur."}
            ]
        ),
        27: make_branching_logic(
            "İnflamazom hiperaktivasyonu olan ve Ailesel Akdeniz Ateşi (FMF) tanısı alan tekrarlayan peritonit atakları geçiren bir hastada amiloidoz gelişimini önlemek için hangi profilaktik ilaç tercih edilmelidir?",
            [
                {"text": "Mikrotübül polimerizasyonunu bozarak nötrofil kemotaksisini ve inflamazom aktivasyonunu baskılayan Kolkisin", "isCorrect": True, "feedback": "Kusursuz klinik patoloji tedavisi! FMF'te amiloidozu (AA tipi) önleyen altın standart ilaç kolkisindir."},
                {"text": "Kemik iliğinde nötrofil üretimini artıran G-CSF infüzyonu", "isCorrect": False, "feedback": "Nötrofil sayısını artırmak yangıyı daha da alevlendirir."},
                {"text": "Sadece yüksek doz demir preparatları", "isCorrect": False, "feedback": "Demir birikimi enflamasyonu baskılamaz."}
            ]
        ),
        47: make_branching_logic(
            "Ciddi bir pnömoni hastasında plevral boşlukta toplanan fibrinöz eksüdanın aspire edilmeyip haftalarca yerinde bırakılması durumunda hastayı bekleyen en olası uzun vadeli komplikasyon nedir?",
            [
                {"text": "Fibrinöz eksüdanın içine granülasyon dokusu ve fibroblastların girerek plevra yapraklarını birbirine yapıştırması (fibrotoraks ve restriktif akciğer hastalığı)", "isCorrect": True, "feedback": "Harika patolojik öngörü! Temizlenemeyen fibrinöz eksüda organize olarak kalın fibröz plevral zırha (fibrotoraks) dönüşür."},
                {"text": "Plevra sıvısının kendiliğinden buharlaşarak akciğeri aşırı havalandırması (amfizem)", "isCorrect": False, "feedback": "Sıvı buharlaşmaz, bağ dokusuna organize olur."},
                {"text": "Plevra mezotel hücrelerinin hızla benign lipomlara dönüşmesi", "isCorrect": False, "feedback": "Fibrin lipom yapmaz, skar fibrozisi yapar."}
            ]
        ),
        67: make_branching_logic(
            "Akut kolesistit (safra kesesi iltihabı) tablosunda cerrahın safra kesesini çıkardıktan sonra patoloğun kesede akut enflamasyon tanısını kesinleştirmesi için araması gereken zorunlu mikroskobik bulgu nedir?",
            [
                {"text": "Safra kesesi duvarında (mukozadan serozaya) polimorfonükleer nötrofil infiltrasyonu ve ödem varlığı", "isCorrect": True, "feedback": "Doğru patoloji kuralı! Akut enflamasyonun altın standart histopatolojik kanıtı nötrofil infiltrasyonudur."},
                {"text": "Yalnızca lümende kolesterol taşlarının görülmesi", "isCorrect": False, "feedback": "Kolelitiyazis tek başına akut enflamasyon demek değildir (asemptomatik taş olabilir)."},
                {"text": "Duvar katmanlarında yaygın kazeöz nekroz bulunması", "isCorrect": False, "feedback": "Kazeifikasyon tüberküloza özgüdür."}
            ]
        ),
        87: make_branching_logic(
            "Akut miyokard enfarktüsü geçiren bir hastada enfarktüs alanına ilk 24-48 saatte nötrofillerin, ardından 3-7. günlerde makrofajların gelmesinin doku onarımı açısından önemi nedir?",
            [
                {"text": "Nötrofillerin nekrotik miyositleri parçalayıp temizlemesi, ardından makrofajların büyüme faktörleri (VEGF, TGF-beta) salgılayarak granülasyon dokusu ve skar oluşumunu başlatması", "isCorrect": True, "feedback": "Mükemmel patoloji bilgisi! Nekrotik ölü hücreler temizlenmeden fibroblastlar ve damarlar sağlam bir skar oluşturamaz."},
                {"text": "Nötrofillerin nekrotik kalbi yeni miyositlere dönüştürerek kalbi rejenere etmesi", "isCorrect": False, "feedback": "Kalp kası kalıcı dokudur, bölünemez; yerini skar dokusu alır."},
                {"text": "Makrofajların miyokardda koroner arterleri tıkayıcı kalsiyum kristalleri üretmesi", "isCorrect": False, "feedback": "Makrofaj kalsifikasyon yapmaz, debridman yapar."}
            ]
        )
    }

def get_extra_quizzes():
    """Ekstra mikro sorular (micro_quiz)"""
    return {
        3: make_micro_quiz(
            "Akut enflamasyonun erken evresinde hasar bölgesine ilk ulaşan polimorfonükleer lökositlerin (nötrofiller) dokuda yaşama süresi ortalama ne kadardır?",
            {
                "A": "1 ila 2 gün (24-48 saat)",
                "B": "3 ila 4 hafta",
                "C": "Birkaç ay",
                "D": "Yıllarca (hafıza hücresi gibi)",
                "E": "Yalnızca birkaç saniye"
            },
            "A",
            {
                "A": "Doğru cevap A'dır: Nötrofiller kısa ömürlü intihar savaşçılarıdır; dokuda 24-48 saat yaşar ve hızla apoptoza giderler.",
                "B": "Haftalarca yaşayanlar makrofajlardır.",
                "C": "Monosit/makrofajlar ve plazma hücreleri aylarca yaşayabilir.",
                "D": "Hafıza T ve B lenfositleri yıllarca yaşar.",
                "E": "Birkaç saniye çok kısadır."
            }
        ),
        33: make_micro_quiz(
            "Aşağıdakilerden hangisi mast hücre granüllerinden salınan ve akut enflamasyonda arteriyoler vazodilatasyon ile venüler endotel kasılmasını en hızlı başlatan vazoaktif amindir?",
            {
                "A": "Histamin",
                "B": "Asetilkolin",
                "C": "Adrenalin",
                "D": "GABA",
                "E": "Dopamin"
            },
            "A",
            {
                "A": "Doğru cevap A'dır: Histamin mast hücrelerinde hazır depolanan ve saniyeler içinde salınarak vasküler reaksiyonları başlatan primer vazoaktif amindir.",
                "B": "Asetilkolin nörotransmitterdir.",
                "C": "Adrenalin vazokonstriktördür.",
                "D": "GABA santral inhibitördür.",
                "E": "Dopamin katekolamindir."
            }
        ),
        63: make_micro_quiz(
            "Endotel hücrelerinde Weibel-Palade cisimciklerinde önceden sentezlenmiş olarak depolanan ve lökosit yuvarlanmasını başlatan adezyon molekülü hangisidir?",
            {
                "A": "P-selektin (CD62P)",
                "B": "ICAM-1 (CD54)",
                "C": "VCAM-1 (CD106)",
                "D": "L-selektin (CD62L)",
                "E": "PECAM-1 (CD31)"
            },
            "A",
            {
                "A": "Doğru cevap A'dır: P-selektin Weibel-Palade cisimcikleri içinde depolanır ve histamin/trombin ile dakikalar içinde ekzosite edilir.",
                "B": "ICAM-1 depolanmaz, sitokinlerle indüklenir.",
                "C": "VCAM-1 indüklenir.",
                "D": "L-selektin lökosit yüzeyindedir.",
                "E": "PECAM-1 interendotelyal kavşaktadır."
            }
        )
    }

def get_extra_causal_chains():
    """Ekstra mekanizma zincirleri (causal_chain)"""
    return {
        23: make_causal_chain(
            "Toll-Like Reseptörden Akut Faz Yanıtına Giden Yol",
            [
                "1. Doku makrofajı bakteriyel endotoksini TLR4 reseptörüyle algılar",
                "2. MyD88 adaptörü üzerinden IKK kompleksi aktive edilir ve IkB proteini parçalanır",
                "3. Serbest kalan NF-kappaB çekirdeğe girerek TNF-alfa, IL-1 ve IL-6 sitokinlerini sentezletir",
                "4. Dolaşıma salınan IL-6 karaciğer hepatositlerine ulaşarak CRP ve fibrinojen üretimini patlatır"
            ]
        ),
        53: make_causal_chain(
            "Pürülan Abse ve Likefaksiyon Nekrozu Zinciri",
            [
                "1. Piyojenik bakteriler (Staphylococcus aureus) doku parankimini istila eder",
                "2. Kemotaktik sinyallerle milyonlarca nötrofil hasar alanına hücum eder",
                "3. Nötrofil granüllerinden boşalan elastaz ve hidrolazlar doku matriksini tamamen eritir",
                "4. Sıvılaşan nekrotik parankim ve ölü nötrofiller fokal irin (abse) havuzuna dönüşür"
            ]
        ),
        83: make_causal_chain(
            "Oksijene Bağımlı İntrasellüler Öldürme Zinciri",
            [
                "1. Fagositoz ile aktifleşen NADPH oksidaz moleküler oksijenden süperoksit radikali üretir",
                "2. Süperoksit dismutaz (SOD) süperoksiti hidrojen peroksite (H2O2) çevirir",
                "3. Azurofilik granüllerdeki Miyeloperoksidaz (MPO) enzimi ortama dökülür",
                "4. MPO, H2O2 ve klorürden güçlü hipokloröz asit (HOCl) sentezleyerek bakteriyi imha eder"
            ]
        )
    }

def get_extra_sliders():
    return {}

def get_extra_tables():
    return {}
