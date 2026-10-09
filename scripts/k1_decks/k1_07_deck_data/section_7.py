"""
Bölüm 7: Eksojen ve Endojen Pigmentler: Antrakozis, Lipofusin ve Melanin
Adımlar: 61 - 70
Checkpoint: Adım 69 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # ADIM 61
    slides.append({
        "slideNumber": 61,
        "title": "Pigment Kavramı: Eksojen ve Endojen Renk Maddelerinin Sınıflaması",
        "subtitle": "Kendi doğal rengi olan maddelerin biyolojik kaynakları ve doku birikimleri",
        "badge": "Pigment Giriş",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Pigmentler, kendilerine özgü doğal renkleri olan ve dokularda anormal miktarlarda birikerek renk değişikliği "
            "yaratan maddelerdir. Histopatolojide pigmentler kökenlerine göre iki temel kategoriye ayrılır: eksojen pigmentler "
            "(vücut dışından solunum, sindirim veya cilt yoluyla girenler) ve endojen pigmentler (vücudun bizzat kendi "
            "hücreleri tarafından sentezlenen veya metabolize edilenler).\n\n"
            "> [TEMEL İLKE] Eksojen pigmentlerin en sık görüleni karbon (kömür tozu) iken; endojen pigmentlerin en önemlileri "
            "lipofusin, melanin ve hemoglobinden köken alan hemosiderin/bilirubindir.\n\n"
            "Pigmentlerin rengi, granülasyon tipi ve özel boyalarla reaksiyonları patolojik tanıda son derece kıymetli ipuçları sunar."
        ),
        "medicalTerms": [
            {"term": "Pigment", "explanation": "Kendi içsel rengi bulunan, dokularda birikerek renk değişimi yapan maddelerdir."},
            {"term": "Endojen Pigment", "explanation": "Hücre metabolizması veya hemoglobin yıkımıyla organizmanın kendi içinde üretilen renk maddeleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Eksojen pigmentlerin en yaygını karbon (antrakozis) pigmentidir.",
            "📌 [SINAV SPOTU] Endojen pigmentler lipofusin, melanin ve hemosiderini kapsar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eksojen Kaynak", "desc": "Karbon, silika, dövme boyaları, kurşun çizgisi.", "isKey": True},
                {"title": "Endojen Kaynak", "desc": "Lipofusin (aşınma), melanin (UV kalkanı), hemosiderin (demir).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Vücut dışından solunum veya cilt yoluyla alınıp dokularda biriken renk maddelerine eksojen pigmentler adı verilir.",
                "eksojen",
                "Dış kaynaklı biyolojik maddeleri tanımlayan terim"
            ),
            make_active_recall(
                "İnsan patolojisinde en sık karşılaşılan eksojen pigment ile hücre yaşlanmasını gösteren endojen pigment hangileridir?",
                "En sık eksojen pigment karbon (kömür tozu); yaşlanmayı gösteren endojen pigment ise lipofusindir."
            )
        ]
    })

    # ADIM 62
    slides.append({
        "slideNumber": 62,
        "title": "Eksojen Pigment: Karbon (Kömür Tozu) ve Antrakozis Gelişimi",
        "subtitle": "Kentsel hava kirliliği, sigara dumanı ve kömür tozu inhalasyonu",
        "badge": "Antrakozis",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Karbon (kömür tozu), insan patolojisinde en yaygın rastlanan eksojen pigmenttir. Şehirlerde yaşayan hemen "
            "her birey egzoz gazları, endüstriyel dumanlar ve fosil yakıt atıkları nedeniyle sürekli karbon partiküllerini "
            "solur. Sigara içenlerde ve kömür madencilerinde bu inhalasyon katbekat fazladır.\n\n"
            "> [SINAV SPOTU] Akciğere ulaşan karbon partiküllerinin alveol boşluklarında ve akciğer parankiminde depolanarak "
            "siyah renkli pigmentasyon oluşturmasına 'antrakozis' (anthracosis) adı verilir.\n\n"
            "Karbon partikülleri kimyasal olarak inert (etkisiz) oldukları için hafif antrakozis genellikle doku hasarına, "
            "fibrozise veya fonksiyon kaybına yol açmaz; tamamen sessizdir."
        ),
        "medicalTerms": [
            {"term": "Antrakozis", "explanation": "Akciğer parankimi ve drene eden lenf bezlerinde karbon tozu birikmesiyle oluşan siyah pigmentasyondur."},
            {"term": "İnert Partikül", "explanation": "İmmün sistemi veya kimyasal yolakları aktive etmeyen, dokuda pasif kalan maddedir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Antrakozis kömür tozu ve karbonun akciğerde zararsız birikimidir.",
            "📌 [SINAV SPOTU] Şehirde yaşayan bireylerin ve sigara içenlerin akciğerlerinde kural olarak bulunur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Giriş Yolu", "desc": "Solunum yoluyla inhalasyon ve alveollere çökme.", "isKey": True},
                {"title": "Biyolojik Etki", "desc": "Saf karbon kimyasal olarak inerttir; fibrozis yapmaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Akciğer parankimi ve hiler lenf düğümlerinde karbon partiküllerinin birikmesiyle oluşan siyah pigmentasyona antrakozis denir.",
                "antrakozis",
                "Karbon pigmentine bağlı akciğer kararması"
            ),
            make_active_recall(
                "Basit antrakozis tablosunun akciğer dokusunda genellikle fonksiyonel bir bozulmaya yol açmamasının nedeni nedir?",
                "Karbon partiküllerinin kimyasal olarak inert (reaksiyonsuz) olması ve immün sistemi yıkan inflamatuvar mediyatörleri tetiklememesidir."
            )
        ]
    })

    # ADIM 63
    slides.append({
        "slideNumber": 63,
        "title": "Alveoler Makrofajlar, Lenfatik Drenaj ve Kömür İşçisi Pnömokonyozu",
        "subtitle": "Toz hücreleri (dust cells), trakeobronşiyal lenf nodları ve masif progresif fibrozis",
        "badge": "Pnömokonyoz",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Alveol boşluklarına inen karbon partikülleri 'toz hücreleri' (dust cells) olarak da bilinen yerleşik alveoler "
            "makrofajlar tarafından derhal fagosite edilir. Makrofajlar bu partikülleri sindiremez; lenfatik damarlara "
            "geçerek trakeobronşiyal ve hiler lenf düğümlerine taşırlar. Bu nedenle otopsilerde hiler lenf nodları simsiyah kömür "
            "parçası gibi izlenir.\n\n"
            "> [YÜKSEK VERİM] Kömür madencilerinde aşırı yoğun kömür tozu maruziyeti 'Kömür İşçisi Pnömokonyozu'na (CWP) "
            "yol açar; silika karışımı da varsa 'progresif masif fibrozis' (PMF) ve solunum yetmezliği gelişir.\n\n"
            "Bu durum basit bir eksojen birikimin ağır meslek hastalığına nasıl dönüştüğünü gösterir."
        ),
        "medicalTerms": [
            {"term": "Toz Hücresi (Dust Cell)", "explanation": "Akciğer alveollerinde karbon ve yabancı partikülleri yutmuş koyu sitoplazmalı makrofajdır."},
            {"term": "Kömür İşçisi Pnömokonyozu (CWP)", "explanation": "Uzun süreli yoğun kömür tozu inhalasyonuna bağlı akciğer parankim hasarı ve fibrozisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Karbon partikülleri alveoler makrofajlarca lenfatiklerle hiler lenf nodlarına taşınır.",
            "📌 [SINAV SPOTU] Ağır kömür madencisi maruziyetinde masif progresif fibrozis (PMF) gelişebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Fagositoz ve Taşıma", "desc": "Alveoler makrofajlar karbonu lenfatik kanallarla hiler nodlara götürür.", "isKey": True},
                {"title": "Klinik Spektrum", "desc": "Asemptomatik antrakozisten ölümcül progresif masif fibrozise uzanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Karbon İnhalasyonundan Lenf Nodu Antrakozisine Gidiş",
                [
                    "1. İnhalasyon: Karbon partikülleri solunum havasıyla terminal alveollere kadar ulaşır.",
                    "2. Makrofaj Fagositozu: Alveoler makrofajlar (toz hücreleri) karbonu fagozomlarına hapseder.",
                    "3. Lenfatik Göç: Makrofajlar parankim içi lenfatik damarlara girerek hiler bölgeye göç eder.",
                    "4. Lenf Nodu Kararması: Trakeobronşiyal ve hiler lenf düğümlerinde karbon birikerek simsiyah nodlar oluşturur."
                ]
            ),
            make_cloze(
                "Akciğerde karbon partiküllerini fagosite eden alveoler makrofajlara histolojide toz hücreleri adı da verilir.",
                "toz hücreleri",
                "Karbon yutmuş alveoler makrofajların diğer adı"
            )
        ]
    })

    # ADIM 64
    slides.append({
        "slideNumber": 64,
        "title": "Dövme (Tattoo) Pigmentleri ve Dermal Makrofaj Hapsolması",
        "subtitle": "Kutanöz inokülasyon, ekstraselüler mineral tuzları ve ömür boyu kalıcılık",
        "badge": "Dövme Pigmenti",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Dövme (tattooing), eksojen pigment birikiminin en yaygın kutanöz örneğidir. İğnelerle dermis tabakasına "
            "enjekte edilen metalik tuzlar, karbon ve organik boyar maddeler dermisteki fagositer makrofajlar tarafından "
            "yutulur. Hücreler bu inorganik ve sentetik boyaları parçalayacak enzimlere sahip olmadığından pigmentler "
            "ömür boyu sitoplazmada hapsolur.\n\n"
            "> [KLİNİK İPUCU] Bir kısım pigment ekstraselüler kollajen lifleri arasında serbest kalır; makrofajlar öldükçe "
            "açığa çıkan pigment komşu yeni makrofajlarca tekrar fagositoz döngüsüne alınır.\n\n"
            "Zamanla lenfatik drenajla bölgesel lenf nodlarına taşınan dövme pigmentleri, lenf bezi diseksiyonlarında "
            "melanom metastazını taklit eden siyah/mavi pigmentasyonlar yaratabilir."
        ),
        "medicalTerms": [
            {"term": "Dövme Pigmenti", "explanation": "Dermis içine mekanik olarak verilen ve makrofajlarda sindirilemeyen inorganik boyadır."},
            {"term": "Dermal Fagositoz", "explanation": "Dermisteki histiositlerin yabancı boya partiküllerini içine alıp hapsetmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dövme pigmentleri dermisteki makrofajların fagozomlarında kalıcı olarak hapsolur.",
            "📌 [SINAV SPOTU] Bölgesel lenf düğümlerine drene olarak lenf nodunda pigmentsi yalancı metastaz görüntüsü yapabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dermis Tutulumu", "desc": "İğneyle dermise bırakılan boya makrofajlarca ömür boyu saklanır.", "isKey": True},
                {"title": "Lenfatik Kaçış", "desc": "Aksiller veya inguinal lenf bezlerinde fokal boyalanma yapabilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Antrakozis (Akciğer) vs Dövme (Dermis)",
                "Antrakozis",
                "Solunum yoluyla inhalasyon sonucu alveoler makrofajlarda biriken eksojen karbon pigmentasyonudur.",
                "Dövme (Tattoo)",
                "İğne penetrasyonu ile dermise verilen ve dermal histiositlerde hapsolan eksojen mineral boya birikimidir."
            ),
            make_active_recall(
                "Dövme pigmentlerinin insan cildinde on yıllar boyunca silinmeden kalabilmesinin hücresel nedeni nedir?",
                "Pigmentlerin dermisteki makrofajlar tarafından fagosite edilmesi ve hücrelerin bu inorganik boyaları sindirecek hiçbir enzime sahip olmamasıdır."
            )
        ]
    })

    # ADIM 65
    slides.append({
        "slideNumber": 65,
        "title": "Endojen Pigment: Lipofusin (\"Aşınma ve Yıpranma Pigmenti\")",
        "subtitle": "Serbest radikal aracılı lipid peroksidasyonu ve hücre yaşlanmasının imzası",
        "badge": "Lipofusin",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Lipofusin, tıbbi patolojide 'aşınma ve yıpranma pigmenti' (wear-and-tear pigment) veya 'yaşlılık pigmenti' "
            "olarak tanımlanan, çözünmeyen endojen bir pigmenttir. Kendisi hücreye toksik veya zararlı değildir; "
            "ancak geçmiş serbest radikal hasarının ve lipid peroksidasyonunun kalıcı bir 'biyolojik izi'dir.\n\n"
            "> [SINAV SPOTU] Işık mikroskobunda çekirdek çevresinde (perinükleer alanda) toplanmış ince taneli, "
            "altın sarısı-kahverengi intrasitoplazmik granüller olarak izlenir.\n\n"
            "Bölünmeyen veya uzun ömürlü hücrelerde (özellikle kardiyomiyositler, hepatositler ve nöronlar) yaş ilerledikçe "
            "belirgin şekilde birikir."
        ),
        "medicalTerms": [
            {"term": "Lipofusin", "explanation": "Lipid peroksidasyonu sonucu oluşan, yaşlanma ve serbest radikal hasarını gösteren altın-kahve pigmenttir."},
            {"term": "Perinükleer Lokalizasyon", "explanation": "Hücre çekirdeğinin hemen çevresindeki sitoplazmik alanda yerleşme biçimidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lipofusin serbest radikal hasarı ve lipid peroksidasyonunun göstergesidir.",
            "📌 [SINAV SPOTU] Işık mikroskobunda altın sarısı-kahverengi perinükleer granüller olarak görülür.",
            "📌 [SINAV SPOTU] En sık yaşlı bireylerin kalp kası, karaciğer ve nöronlarında birikir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Biyokimyasal Köken", "desc": "Peroksidasyona uğramış polidoymamış membran lipidleri ve protein kompleksleri.", "isKey": True},
                {"title": "Önemli Doku", "desc": "Kardiyomiyositler, hepatositler ve santral sinir sistemi nöronları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "85 yaşında bir hastanın otopsisinde kalbin belirgin şekilde küçüldüğü, miyokardın koyu kahverengi bir renk aldığı izleniyor. Işık mikroskobunda kardiyomiyositlerin çekirdek çevresinde altın sarısı-kahverengi ince granüller saptanıyor. Bu pigment aşağıdakilerden hangisidir?",
                {
                    "A": "Hemosiderin",
                    "B": "Lipofusin",
                    "C": "Melanin",
                    "D": "Karbon pigmenti",
                    "E": "Bilirubin kristalleri"
                },
                "B",
                {
                    "A": "Hemosiderin Prusya mavisiyle boyanan demir pigmentidir, kalp yaşlanmasının primer rengi değildir.",
                    "B": "Doğru! Yaşlı kalpte perinükleer altın sarısı-kahverengi granüller lipofusindir (aşınma pigmenti).",
                    "C": "Melanin deride melanositlerce üretilen UV kalkanıdır.",
                    "D": "Karbon akciğerde siyah pigmentasyon yapar.",
                    "E": "Bilirubin sarılıkta dokuları sarıya boyar."
                }
            ),
            make_cloze(
                "Kardiyomiyosit ve hepatositlerde yaşlanma ile biriken altın sarısı-kahverengi pigmente lipofusin adı verilir.",
                "lipofusin",
                "Aşınma ve yıpranma anlamına gelen yaşlılık pigmenti"
            )
        ]
    })

    # ADIM 66
    slides.append({
        "slideNumber": 66,
        "title": "Lipofusin Biyokimyası: Lipid Peroksidasyonu, Lizozomlar ve Otofaji",
        "subtitle": "Tersiyer lizozomlar (telolizozomlar), rezidüel cisimcikler ve sindirilemeyen artıklar",
        "badge": "Biyokimya ve Otofaji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre yaşlandıkça veya kronik oksidatif strese maruz kaldıkça organel membranlarındaki polidoymamış yağ "
            "asitleri serbest radikallerce peroksidasyona uğrar. Bu hasarlı membran parçaları otofaji fagozomları içine "
            "alınarak sindirilmek üzere lizozomlarla birleştirilir. Ancak lizozomal asit hidrolazlar yüksek derecede "
            "çapraz bağlanmış lipid-protein polimerlerini sindiremez.\n\n"
            "> [YÜKSEK VERİM] Sindirilemeyen bu kalıntılar lizozom içinde kalarak 'rezidüel cisimciğe' (telolizozom) "
            "dönüşür; binlerce telolizozomun kümelenmesi mikroskopta gördüğümüz lipofusin granüllerini meydana getirir.\n\n"
            "Bu durum, hücrenin kendi çöplerini tamamen temizleyemeyip ömrü boyunca organellerinde saklamak zorunda kalışıdır."
        ),
        "medicalTerms": [
            {"term": "Lipid Peroksidasyonu", "explanation": "Serbest radikallerin membran lipidlerindeki çift bağlara saldırarak zincirleme yıkım yapmasıdır."},
            {"term": "Rezidüel Cisimcik (Telolizozom)", "explanation": "Sindirilemeyen substrat kalıntılarını hapseden üçüncü evre lizozomdur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lipofusin sindirilemeyen otofajik kalıntıların lizozomlarda birikmesiyle oluşur.",
            "📌 [SINAV SPOTU] Elektron mikroskobunda lipid peroksidasyon ürünleri içeren rezidüel cisimcikler olarak izlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Otofajik Başlangıç", "desc": "Yaşlanan mitokondri ve membranların fagozoma alınması.", "isKey": True},
                {"title": "Enzimatik Çaresizlik", "desc": "Çapraz bağlı lipid-protein kompleksleri hidrolazlarca parçalanamaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Serbest Radikal Hasarından Lipofusin Granülüne",
                [
                    "1. Oksidatif Stres: Reaktif oksijen türleri hücre membran lipidlerini peroksidasyona uğratır.",
                    "2. Otofaji: Hasarlı membran parçaları otofagozomlar içine paketlenir.",
                    "3. Lizozomal Birleşme: Fagozom lizozomla kaynaşır; ancak hidrolazlar polimerleri eritemez.",
                    "4. Rezidüel Cisimcik: Organel kalıcı bir telolizozoma (çöp organeline) dönüşür.",
                    "5. Lipofusin Birikimi: Çekirdek etrafında altın-kahverengi granüller kümelenerek lipofusini oluşturur."
                ]
            ),
            make_cloze(
                "Lipofusin pigmenti içeren lizozomlar elektron mikroskobunda sindirilemeyen artıklarla dolu rezidüel cisimcikler olarak görülür.",
                "rezidüel cisimcikler",
                "Lizozomal sindirimin son artıklarını taşıyan organeller"
            )
        ]
    })

    # ADIM 67
    slides.append({
        "slideNumber": 67,
        "title": "Kahverengi Atrofi (Brown Atrophy): Yaşlı Kalp ve Karaciğer Morfolojisi",
        "subtitle": "Kardiyak küçülme, kıvrıntılı koronerler ve eşlik eden lipofusin birikimi",
        "badge": "Kahverengi Atrofi",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Ağır malnütrisyon, kanser kaşeksisi veya ileri yaşlanma tablosundaki bireylerde iç organlarda belirgin bir "
            "hacim küçülmesi (atrofi) meydana gelir. Atrofiye uğrayan kardiyomiyositlerin hacmi azalırken, hücre içindeki "
            "lipofusin pigmenti yoğunlaşır ve organın makroskobik rengini değiştirir.\n\n"
            "> [SINAV SPOTU] Kalp ağırlığının 150-200 grama kadar düştüğü, epikardiyal yağın eridiği, koroner arterlerin "
            "kıvrıntılı bir hal aldığı ve miyokardın koyu kahverengi göründüğü bu tabloya 'kahverengi atrofi' (brown atrophy) denir.\n\n"
            "Aynı süreç atrofik karaciğerde de belirgin olup, organın rengini koyu çikolata-kahverengiye çevirir."
        ),
        "medicalTerms": [
            {"term": "Kahverengi Atrofi (Brown Atrophy)", "explanation": "İleri yaş veya kaşekside organ hacminin küçülmesi ve lipofusin yoğunlaşmasıyla rengin kahverengileşmesidir."},
            {"term": "Kaşeksi", "explanation": "Kronik hastalıklarda görülen şiddetli kas ve yağ dokusu kaybı tablosudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kahverengi atrofide organ boyutu küçülür, rengi lipofusin nedeniyle koyu kahverengi olur.",
            "📌 [SINAV SPOTU] En tipik olarak yaşlı veya kaşektik kalpte ve karaciğerde görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kardiyak Makroskopi", "desc": "Küçük kalp, erimiş epikardiyal yağ, kıvrıntılı koronerler, kahverengi kas.", "isKey": True},
                {"title": "Hücresel Mekanizma", "desc": "Proteazomal protein yıkımı (atrofi) + lizozomal lipofusin yoğunlaşması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Patoloji", "Organ Boyutu", "Baskın Pigment", "Tipik Klinik Tablo"],
                [
                    [("Kahverengi Atrofi", False, ""), ("Belirgin Küçülmüş (Atrofik)", True, "Hacim ve ağırlık kaybı gösteren organ"), ("Lipofusin", True, "Perinükleer altın sarısı-kahve pigment"), ("İleri yaşlanma, kanser kaşeksisi")],
                    [("Hemokromatoz", False, ""), ("Büyümüş (Hepatomegali/Kardiyomegali)", False, ""), ("Hemosiderin", True, "Prusya mavisi pozitif demir pigmenti"), ("Genetik demir aşırı yükü, bronz diyabet")],
                    [("Karaciğer Steatozu", False, ""), ("Büyümüş, sarı parlak", False, ""), ("Trigliserid", False, ""), ("Alkolizm, obezite, diyabet")]
                ]
            ),
            make_cloze(
                "İleri yaşlı veya kaşektik bireylerin kalbinde organ küçülmesi ve lipofusin birikimiyle karakterize tabloya kahverengi atrofi denir.",
                "kahverengi atrofi",
                "Yaşlı kalpte görülen hacim küçülmesi ve renk koyulaşması"
            )
        ]
    })

    # ADIM 68
    slides.append({
        "slideNumber": 68,
        "title": "Melanin Biyosentezi, Melanositler, Keratinosit Aktarımı ve UV Koruması",
        "subtitle": "Tirozinaz enzimi, melanozomlar ve bazal keratinositlerin nükleer güneşlik kalkanı",
        "badge": "Melanin",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Melanin, epidermisin bazal tabakasında yerleşik melanositler tarafından sentezlenen tek endojen kahverengi-siyah "
            "pigmenttir. Melanositler nöral krest kökenlidir ve tirozinaz enzimi aracılığıyla tirozini dihidroksifenilalanin "
            "(DOPA) üzerinden melanine dönüştürür. Üretilen melanin 'melanozom' adı verilen organellerde paketlenir.\n\n"
            "> [SINAV SPOTU] Melanositler dendritik uzantılarıyla melanozomları komşu bazal keratinositlere aktarır; "
            "keratinositler melanini çekirdeklerinin üzerine bir 'şemsiye / güneşlik' gibi yerleştirerek DNA'yı UV hasarından korur.\n\n"
            "Dermise dökülen melanin makrofajlarca yutulduğunda bu hücrelere 'melanofor' adı verilir."
        ),
        "medicalTerms": [
            {"term": "Melanin", "explanation": "Melanositlerde tirozinazla üretilen, UV radyasyonunu soğuran endojen pigmenttir."},
            {"term": "Melanofor", "explanation": "Dermiste serbest kalan melanini fagosite etmiş dermal makrofajdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Melanin sentezinin anahtar enzimi bakır bağımlı tirozinaz enzimidir.",
            "📌 [SINAV SPOTU] Melanosit üretir ancak melanin bazal keratinositlerin çekirdek üzerinde kalkan oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sentez Fabrikası", "desc": "Epidermis bazal tabakasındaki melanositler ve melanozomlar.", "isKey": True},
                {"title": "Güneşlik Fonksiyonu", "desc": "Keratinosit DNA'sını timin dimerleri ve mutasyondan korur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Melanosit vs Keratinosit Melanin Dağılımı",
                "Melanosit",
                "Nöral krest kökenlidir; melanozom organellerinde tirozinaz enzimiyle aktif melanin sentezi yapar.",
                "Keratinosit",
                "Ektoderm kökenlidir; sentez yapmaz, melanositin dendritinden aldığı melanini çekirdeği üzerine UV şemsiyesi olarak yerleştirir."
            ),
            make_active_recall(
                "Keratinosit hücrelerinin melanini sitoplazmalarında özellikle hücre çekirdeğinin üzerine yerleştirmesinin biyolojik amacı nedir?",
                "Hücre çekirdeğindeki DNA molekülünü ultraviyole (UV) radyasyonunun mutajenik etkilerinden (timin dimerleşmesinden) korumaktır."
            )
        ]
    })

    # ADIM 69 - CHECKPOINT 7
    slides.append({
        "slideNumber": 69,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Eksojen ve Endojen Pigmentler",
        "subtitle": "Karbon, antrakozis, lipofusin, kahverengi atrofi ve melaninin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 7,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında eksojen ve endojen pigmentleri özetliyoruz. 1) Eksojen karbon: Solunumla alınır, "
            "alveoler makrofajlarca fagosite edilir, hiler lenf nodlarına taşınır; antrakozis yapar (genellikle inerttir). "
            "2) Endojen lipofusin: Serbest radikal hasarı ve membran lipid peroksidasyonunun göstergesidir; bölünmeyen "
            "hücrelerde (kalp, karaciğer, nöron) perinükleer altın-kahverengi granüller oluşturur; kaşektik ve yaşlı "
            "kalpte 'kahverengi atrofi' yapar. 3) Endojen melanin: Melanositlerce tirozinazla üretilir, keratinosit "
            "DNA'sını UV'den korur.\n\n"
            "> [KLİNİK İPUCU] Sınavda altın sarısı-kahve yaşlılık granülü lipofusin; kömür siyahı karbon; UV koruyucu siyah pigment melanindir.\n\n"
            "Aşağıdaki 3 akıl kartını hafızanıza sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Antrakozis", "explanation": "Akciğer ve lenf nodlarında karbon pigmenti depolanmasıdır."},
            {"term": "Lipofusin", "explanation": "Lipid peroksidasyonu ve hücresel yaşlanmanın altın-kahverengi göstergesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Karbon = Eksojen, inert, alveoler makrofaj, antrakozis.",
            "📌 [SINAV SPOTU] Lipofusin = Endojen, lipid peroksidasyonu, yaşlılık, kahverengi atrofi.",
            "📌 [SINAV SPOTU] Melanin = Endojen, tirozinaz, melanosit, keratinosit kalkanı."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eksojen Pigment", "desc": "Karbon (antrakozis) ve dövme mineral tuzları.", "isKey": True},
                {"title": "Lipofusin", "desc": "Peroksidasyon kalıntısı, rezidüel lizozom, yaşlı miyokard.", "isKey": True},
                {"title": "Melanin", "desc": "Nöral krest türevi melanosit, UV bariyeri.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-19",
                "Lipofusin pigmentinin hücresel kökeni ve biyokimyasal anlamı nedir?",
                "Serbest radikaller aracılığıyla membran lipidlerinin peroksidasyona uğraması ve parçalanamayan lipid-protein komplekslerinin lizozomlarda kalmasıdır; hücre yaşlanmasını belgeler.",
                "Lipid peroksidasyonu ve hücresel yaşlanma izi"
            ),
            make_flashcard(
                "k1-07-fc-20",
                "Kahverengi atrofi (brown atrophy) tablosunda organın makroskobik rengini kahverengine çeviren temel birikinti nedir?",
                "Atrofiye uğrayan parankim hücrelerinde yoğunlaşan lipofusin pigmentidir.",
                "Yaşlı kalpte atrofi ve renk değişimi"
            ),
            make_flashcard(
                "k1-07-fc-21",
                "Antrakozis patolojisinde karbon partiküllerini akciğer parankiminden lenf nodlarına taşıyan anahtar hücre hangisidir?",
                "Alveoler makrofajlardır (toz hücreleri - dust cells).",
                "Fagositoz ve lenfatik transport hücresi"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Yaşlı bireylerin kalp kası liflerinde perinükleer alanda biriken lipofusin granülleri altın sarısı-kahverengi renktedir.",
                "altın sarısı-kahverengi",
                "Lipofusin pigmentinin mikroskop altındaki karakteristik rengi"
            )
        ]
    })

    # ADIM 70
    slides.append({
        "slideNumber": 70,
        "title": "Pigmentlerin Mikroskobik Ayırıcı Tanısı ve Klinik Önemi",
        "subtitle": "Kahverengi pigmentlerin (lipofusin, hemosiderin, melanin) ayırıcı tanı algoritması",
        "badge": "Ayırıcı Tanı",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Işık mikroskobunda kahverengi pigment saptandığında patoloğun önünde üç büyük endojen aday vardır: "
            "lipofusin, hemosiderin ve melanin. Bu pigmentler standart H&E kesitlerinde birbirini taklit edebilir. "
            "Doğru ayırıcı tanı için histokimyasal boyalardan yararlanılır.\n\n"
            "> [SINAV SPOTU] Hemosiderin Prusya mavisi (Perls) ile masmavi boyanırken; lipofusin ve melanin bu boyayla "
            "asla boyanmaz. Melanin Fontana-Masson gümüş boyası ile siyaha boyanır ve çamaşır suyu (ağartma) ile silinir.\n\n"
            "Lipofusin ise autofloresan verir ve Sudan Black ile soluk lipid boyanması gösterir. Bu algoritma klinikte "
            "yanlış tanı konulmasını engeller."
        ),
        "medicalTerms": [
            {"term": "Prusya Mavisi (Perls)", "explanation": "Hemosiderin içindeki demiri (Fe3+) potasyum ferrosiyanürle parlak maviye boyayan reaksiyondur."},
            {"term": "Fontana-Masson", "explanation": "Melaninin gümüş tuzlarını indirgeme yeteneğini kullanarak onu siyaha boyayan yöntemdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Prusya mavisi sadece hemosiderini maviye boyar; lipofusin ve melanini boyamaz.",
            "📌 [SINAV SPOTU] Fontana-Masson melanini siyaha boyar; ağartma (bleaching) ile melanin silinir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Prusya Mavisi", "desc": "Demir varsa masmavi = Hemosiderin.", "isKey": True},
                {"title": "Fontana-Masson", "desc": "Gümüşü indirgerse siyah = Melanin.", "isKey": True},
                {"title": "Perinükleer Sarı-Kahve", "desc": "Özel boya negatif, yaşlılık izi = Lipofusin.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Karaciğer biyopsisinde hepatosit ve Kupffer hücrelerinde bol miktarda altın sarısı-kahverengi granüler pigment izleniyor. Pigmentin türünü belirlemek için yapılan Prusya mavisi boyaması tamamen negatif bulunuyor. Fontana-Masson boyası da negatif. Bu pigment en yüksek olasılıkla hangisidir?",
                [
                    {
                        "text": "Hemosiderin: Kronik kan transfüzyonuna bağlı aşırı demir yüklenmesi",
                        "isCorrect": False,
                        "feedback": "Yanlış! Hemosiderin olsaydı Prusya mavisi ile kuvvetli pozitif masmavi boyanırdı."
                    },
                    {
                        "text": "Lipofusin: İleri yaş veya serbest radikal hasarına bağlı aşınma pigmenti",
                        "isCorrect": True,
                        "feedback": "Mükemmel! Prusya mavisi ve gümüş boyaları negatif olan perinükleer sarı-kahverengi pigment lipofusindir."
                    }
                ]
            ),
            make_active_recall(
                "Hemosiderin pigmentini lipofusin ve melaninden kesin olarak ayıran histokimyasal özel boya hangisidir?",
                "Prusya mavisi (Perls) boyasıdır; hemosiderini parlak mavi renge boyarken diğer iki pigmenti boyamaz."
            )
        ]
    })

    return slides
