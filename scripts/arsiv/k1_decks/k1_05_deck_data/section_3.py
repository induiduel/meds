"""
Bölüm 3: Fibrinoid Nekroz, Damar Patolojisi ve Serum Biyobelirteçleri
Adımlar: 21 - 30
Checkpoint: Adım 29 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # ADIM 21
    slides.append({
        "slideNumber": 21,
        "title": "Fibrinoid Nekroz: Mikroskobik Tanınan Özel Damar Nekrozu",
        "subtitle": "Makroskobik olarak görülemeyen, ışık mikroskobunda damar duvarında izlenen lezyon",
        "badge": "Fibrinoid Nekroz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fibrinoid nekroz, diğer nekroz tiplerinden farklı olarak makroskobik otopsi veya cerrahi masasında "
            "çıplak gözle tanınabilen bir doku kitlesi oluşturmaz. Bu lezyon, sadece ışık mikroskobunda "
            "arter ve arteriol gibi küçük kan damarlarının duvarlarında saptanan son derece özel bir nekroz kalıbıdır.\n\n"
            "Bu patolojiye 'fibrinoid' (fibrin-benzeri) denmesinin sebebi, damar duvarında biriken materyalin "
            "histokimyasal ve boyanma özellikleri açısından pıhtılaşma proteini olan fibrine çok benzemesidir.\n\n"
            "> [SINAV SPOTU] Fibrinoid nekroz; immün kompleks reaksiyonlarında (vaskülitler) ve aşırı yüksek "
            "kan basıncında (malign hipertansiyon) küçük damar duvarlarında ortaya çıkan parlak pembe amorf birikimdir.\n\n"
            "Damar endotelinin ağır hasara uğraması plazma proteinlerinin kontrolsüzce damar tunika mediasına sızmasına yol açar."
        ),
        "medicalTerms": [
            {"term": "Fibrinoid Nekroz", "explanation": "Damar duvarında immün kompleksler ve ekstravaze fibrin birikimiyle karakterize, amorf parlak pembe mikroskobik nekroz."},
            {"term": "Fibrinoid", "explanation": "Fibrine benzeyen, eozinofil boyanan amorf plazma proteini birikintisi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fibrinoid nekroz makroskobik olarak görülemez; ışık mikroskobunda tanınan özel bir tiptir.",
            "📌 [SINAV SPOTU] Özellikle küçük damar (arter ve arteriol) duvarlarında ortaya çıkar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Görünürlük Sınırı", "desc": "Çıplak gözle izlenemez; yalnızca mikroskopta damar duvarında saptanır.", "isKey": True},
                {"title": "Temel Tutulum", "desc": "Küçük muskuler arterler ve arteriollerin tunika media tabakası.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Makroskobik olarak görülemeyen ve yalnızca ışık mikroskobunda küçük damar duvarlarında tanınan özel nekroza fibrinoid nekroz denir.",
                "fibrinoid nekroz",
                "Fibrin benzeri parlayan damar nekrozu türü"
            ),
            make_active_recall(
                "Fibrinoid nekroz neden makroskobik olarak değil de yalnızca mikroskobik olarak tanımlanır?",
                "Çünkü lezyon mikroskobik boyuttaki arter ve arteriol duvarlarında fokal olarak gelişir; çıplak gözle görülebilecek kitle oluşturmaz."
            )
        ]
    })

    # ADIM 22
    slides.append({
        "slideNumber": 22,
        "title": "Fibrinoid Nekrozun Biyokimyasal İçeriği: İmmün Kompleksler ve Fibrin",
        "subtitle": "Antijen-antikor çökeltilerinin damar duvarında plazma proteinleriyle birleşmesi",
        "badge": "İmmünopatoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fibrinoid nekrozun moleküler yapısını oluşturan iki ana bileşen vardır: Dolaşımdaki immün kompleksler "
            "(antijen-antikor agregatları) ve plazmadan damar duvarına sızan fibrinojen/fibrin proteinleri.\n\n"
            "Tip III aşırı duyarlılık reaksiyonlarında antijen-antikor kompleksleri küçük damarların bazal membranına "
            "çöker. Bu kompleksler kompleman sistemini (C5a, C3a) aktive ederek nötrofilleri bölgeye çeker. "
            "Nötrofiller lizozomal enzimlerini damar duvarına boşaltarak endotel ve elastik laminayı parçalar.\n\n"
            "> [KRİTİK UYARI] Endotel bariyeri delindiğinde kandan damar duvarına yüksek molekül ağırlıklı fibrinojen sızar; "
            "doku faktörüyle karşılaşınca fibrine dönüşerek antijen-antikor kompleksleriyle kaynaşır ve 'fibrinoid' kitleyi oluşturur.\n\n"
            "Bu durum damar lümenini daraltarak distal dokularda ağır iskemik enfarktlara zemin hazırlar."
        ),
        "medicalTerms": [
            {"term": "İmmün Kompleks", "explanation": "Dolaşımda antijen ve antikorun birleşmesiyle oluşan ve damar duvarına çöken makromoleküler kompleks."},
            {"term": "Tip III Aşırı Duyarlılık", "explanation": "İmmün komplekslerin dokularda birikerek kompleman ve nötrofiller aracılığıyla doku hasarı yapması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fibrinoid materyalin içeriği: İmmün kompleksler (antijen-antikor) + damar dışına sızan plazma proteinleri (özellikle fibrin).",
            "📌 [SINAV SPOTU] Patogenezde kompleman aktivasyonu ve nötrofil kaynaklı endotel hasarı rol oynar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Moleküler İkili", "desc": "Antijen-antikor agregatları + polimerize fibrin lifleri.", "isKey": True},
                {"title": "Kompleman İstilası", "desc": "C5a kemotaksisi ile nötrofillerin damar duvarını eritmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Fibrinoid Nekroz Oluşum Mekanizması",
                [
                    "1. İmmün Çökme: Dolaşımdaki antijen-antikor kompleksleri damar bazal membranına yapışır.",
                    "2. Kompleman Aktivasyonu: Çöken kompleksler C3a ve C5a üreterek nötrofilleri çağırır.",
                    "3. Endotel Hasarı: Nötrofillerden salınan proteazlar damar duvar bütünlüğünü yırtar.",
                    "4. Fibrin Sızıntısı: Plazmadaki fibrinojen damar duvarına geçip fibrine polimerize olur.",
                    "5. Fibrinoid Birikim: İmmün kompleksler ve fibrin parlak pembe amorf camsı kitle oluşturur."
                ]
            ),
            make_cloze(
                "Fibrinoid nekroz alanında damar duvarında biriken temel materyal immün kompleksler ile plazmadan sızan fibrin proteinidir.",
                "fibrin",
                "Damar duvarında parlak pembe boyanan pıhtılaşma proteini"
            )
        ]
    })

    # ADIM 23
    slides.append({
        "slideNumber": 23,
        "title": "Fibrinoid Nekrozun Mikroskopisi: Parlak Pembe Camsı Halka",
        "subtitle": "Arter lümenini çevreleyen homojen, asellüler ve eozinofilik bant morfolojisi",
        "badge": "Mikroskopi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hematoksilen-eozin boyalı doku kesitlerinde fibrinoid nekroz son derece çarpıcı bir görüntü verir. "
            "Arter duvarının normalde katmanlı olan düz kas mimarisi silinmiş, yerini parlak pembe (koyu eozinofilik), "
            "amorf, homojen ve adeta erimiş camı andıran dairesel bir bant almıştır.\n\n"
            "Bu camsı bandın içinde ve çevresinde, damar duvarına saldıran nötrofillerin nükleer kalıntıları "
            "(nükleer toz / lökositoklazi) serpili olarak izlenir.\n\n"
            "> [SINAV SPOTU] Damar duvarında parlak pembe, amorf, 'camsı' materyal birikimi fibrinoid nekrozun "
            "kesin mikroskobik tanımıdır.\n\n"
            "İmmünofloresan mikroskopide (IF) ise damar duvarında immünoglobulinler (IgG, IgM) ve kompleman faktörleri "
            "(C3) parlak yeşil granüler birikintiler şeklinde parlar."
        ),
        "medicalTerms": [
            {"term": "Camsı (Smudgy) Görünüm", "explanation": "Damar duvarı hücrelerinin eriyip homojen parlak pembe bir kütleye dönüşmesi."},
            {"term": "Lökositoklazi", "explanation": "Nötrofillerin parçalanarak çekirdeklerinin nükleer toz halinde dokuya saçılması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Işık mikroskobunda damar duvarında parlak pembe, amorf, 'camsı' materyal izlenir.",
            "📌 [SINAV SPOTU] Çevrede nötrofil infiltrasyonu ve nükleer toz (lökositoklazi) sıkça eşlik eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Boyanma Karakteri", "desc": "H&E boyasında parlak pembe, refraktil ve homojen halka.", "isKey": True},
                {"title": "Lökosit Parçalanması", "desc": "Nükleer tozların damar duvarına dağılması (lökositoklastik vaskülit).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Nekroz Tipi", "H&E Mikroskobik Boyanma", "Tipik Histolojik Lokasyon"],
                [
                    [("Fibrinoid Nekroz", False, ""), ("Parlak pembe, amorf, camsı bant", True, "H&E görünüm özelliği"), ("Küçük arter ve arteriol duvarı", False, "")],
                    [("Kazeöz Nekroz", False, ""), ("Asellüler, granüler pembe döküntü", True, "Peynirimsi mikroskopi"), ("Akciğer granülom merkezi", False, "")],
                    [("Yağ Nekrozu", False, ""), ("Gölge adipositler ve bazofilik Ca2+", True, "Kalsifiye hücre sınırı"), ("Omentum ve peripankreatik yağ", False, "")]
                ]
            ),
            make_cloze(
                "Fibrinoid nekrozda damar duvarında ışık mikroskobunda amorf, parlak pembe ve camsı bir materyal izlenir.",
                "camsı",
                "Homojen ve erimiş cam benzeri doku görüntüsü"
            )
        ]
    })

    # ADIM 24
    slides.append({
        "slideNumber": 24,
        "title": "Poliarteritis Nodosa (PAN): Klasik Fibrinoid Vaskülit Modeli",
        "subtitle": "Orta ve küçük musküler arterleri tutan, transmural nekroz ve anevrizma odağı",
        "badge": "Vaskülit",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fibrinoid nekrozun ders kitaplarındaki en kusursuz klinik örneği 'Poliarteritis Nodosa (PAN)'dır. "
            "PAN; orta ve küçük çaplı musküler arterleri segmental ve transmural (tüm duvarı tutan) şekilde etkileyen "
            "nekrotizan bir sistemik vaskülittir.\n\n"
            "Arter duvarında akut evrede gelişen fibrinoid nekroz ve yoğun nötrofil infiltrasyonu, damar duvarının "
            "elastik yapısını zayıflatır. Damar içi kan basıncına dayanamayan bu zayıf nekrotik noktalar dışa doğru "
            "balonlaşarak 'mikroanevrizmalar' oluşturur.\n\n"
            "> [SINAV SPOTU] Anjiyografide bir ipteki inciler gibi dizilmiş anevrizmalar izlenir. Hastalığın yaklaşık "
            "%30'unda hepatit B virüsü (HBV) yüzey antijeni (HBsAg) içeren immün kompleksler saptanır.\n\n"
            "Akut lezyonlar fibrinoid nekroz gösterirken, eski lezyonlar fibröz kalınlaşma ve lümen tıkanıklığı sergiler."
        ),
        "medicalTerms": [
            {"term": "Poliarteritis Nodosa (PAN)", "explanation": "Orta ve küçük musküler arterlerde transmural fibrinoid nekroz yapan sistemik nekrotizan vaskülit."},
            {"term": "Mikroanevrizma", "explanation": "Nekrotik damar duvarının elastikiyetini kaybederek dışa doğru balonlaşması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fibrinoid nekrozun klasik vaskülit örneği Poliarteritis Nodosa'dır (PAN).",
            "📌 [SINAV SPOTU] PAN'da arter duvarında segmental transmural fibrinoid nekroz ve mikroanevrizmalar gelişir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Transmural Tutulum", "desc": "İntimadan adventisyaya dek tüm arter katmanlarında fibrinoid nekroz.", "isKey": True},
                {"title": "HBV İlişkisi", "desc": "Olguların bir kısmında HBsAg-antiHBs immün kompleks patogenezi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Orta ve küçük çaplı musküler arter duvarlarında transmural fibrinoid nekroz, nötrofilik infiltrasyon ve anjiyografide mikroanevrizmalarla seyreden sistemik vaskülit hangisidir?",
                {
                    "A": "Temporal (Dev Hücreli) Arterit",
                    "B": "Poliarteritis Nodosa (PAN)",
                    "C": "Takayasu Arteriti",
                    "D": "Granülomatöz Polianjiyitis",
                    "E": "Kawasaki Hastalığı"
                },
                "B",
                {
                    "A": "Temporal arterit büyük damarları tutar ve granülomatözdür.",
                    "B": "Doğru cevap B'dir: Klasik transmural fibrinoid nekroz PAN'ın histopatolojik damgasıdır.",
                    "C": "Takayasu aort ve ana dallarını tutan granülomatöz arterittir.",
                    "D": "Wegener granülom ve nekroz yapar, c-ANCA pozitiftir.",
                    "E": "Kawasaki koronerleri tutan çocukluk vaskülitidir."
                }
            ),
            make_cloze(
                "Poliarteritis nodosa hastalığında musküler arter duvarlarında karakteristik olarak transmural fibrinoid nekroz izlenir.",
                "Poliarteritis nodosa",
                "Klasik nekrotizan musküler arter vasküliti"
            )
        ]
    })

    # ADIM 25
    slides.append({
        "slideNumber": 25,
        "title": "Malign Hipertansiyon ve Hiperakut Rejeksiyon: Non-İmmün Fibrinoid Nekroz",
        "subtitle": "Diyastolik basıncın 120 mmHg'yi aşmasıyla arteriollerde gelişen mekanik yırtılma",
        "badge": "Hipertansiyon",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fibrinoid nekrozun gelişmesi için her zaman bir immün kompleks reaksiyonu (vaskülit) şart değildir. "
            "Ani ve şiddetli mekanik gerilim de aynı histopatolojik tabloyu doğurabilir. Bunun en dramatik örneği "
            "'Malign Hipertansiyon'dur (diyastolik basınç > 120-130 mmHg).\n\n"
            "Aşırı yüksek hemodinamik basınç, böbrek afferent arteriollerinin endotelini fiziksel olarak parçalar. "
            "Yüksek basınç altında kan plazması ve fibrinojen damar duvarına zorla enjekte olur.\n\n"
            "> [SINAV SPOTU] Malign hipertansiyonda böbrek arteriollerinde fibrinoid nekroz ve 'hiperplastik arterioloskleroz' "
            "(soğan zarı görünümü) bir arada bulunur; tablo akut böbrek yetmezliğine sürükler.\n\n"
            "Benzer şekilde, böbrek naklinde alıcıdaki hazır antikorların donör damarını dakikalar içinde yıktığı "
            "'Hiperakut Rejeksiyonda' da damar duvarlarında tromboz ve fibrinoid nekroz izlenir."
        ),
        "medicalTerms": [
            {"term": "Malign Hipertansiyon", "explanation": "Kan basıncının hızla yükselerek arteriollerde fibrinoid nekroz ve akut organ yetmezliği yaptığı kriz tablosu."},
            {"term": "Hiperplastik Arterioloskleroz", "explanation": "Düz kas hücrelerinin soğan zarı şeklinde konsantrik proliferasyonuyla lümenin daralması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fibrinoid nekroz immün olmayan nedenlerle de oluşabilir: En tipik örnek Malign Hipertansiyondur.",
            "📌 [SINAV SPOTU] Böbrek arteriollerinde fibrinoid nekroz + soğan zarı laminasyonu (hiperplastik arterioloskleroz) görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemodinamik Yırtılma", "desc": "Yüksek kan basıncının plazmayı zorla damar duvarına itmesi.", "isKey": True},
                {"title": "Böbrek Hasarı", "desc": "Afferent arteriol nekrozu sonucu 'pire ısırığı' peteşiyal kanamalar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Benign vs Malign Hipertansiyon Arteriyel Hasarı",
                "Benign Hipertansiyon",
                "Hafif-orta basınç artışı; endotelden sızan plazma proteinleri damar duvarında pembe hiyalinleşme (Hiyalin Arterioloskleroz) yapar.",
                "Malign Hipertansiyon",
                "Aşırı şiddetli basınç krizi; damar duvarı yırtılarak Fibrinoid Nekroz ve soğan zarı proliferasyonu (Hiperplastik Arterioloskleroz) gelişir."
            ),
            make_cloze(
                "Malign hipertansiyonda aşırı kan basıncı böbrek arteriollerinde endoteli yırtarak fibrinoid nekroz gelişimine yol açar.",
                "Malign hipertansiyon",
                "Diyastolik basıncın kritik yükseldiği acil klinik durum"
            )
        ]
    })

    # ADIM 26
    slides.append({
        "slideNumber": 26,
        "title": "Nekroz ve Serum Biyobelirteçleri: Hücre Zarı Parçalanmasının Klinik İmzası",
        "subtitle": "Plazma membranı yırtıldığında hücre içi moleküllerin kana sızma mekanizması",
        "badge": "Biyobelirteçler",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Geri dönüşümlü hücre hasarında plazma membranı şişmiş olsa da moleküler bütünlüğünü korur ve "
            "büyük hücre içi proteinler hücre içinde hapsolur. Ancak hücre 'point of no return' çizgisini aşıp "
            "nekroza sürüklendiğinde, plazma zarı tamamen yırtılır ve parçalanır.\n\n"
            "Zar bütünlüğünün yok olmasıyla birlikte sitoplazmada ve organellerde bulunan yüksek molekül ağırlıklı "
            "enzimler ve proteinler ekstraselüler aralığa, oradan da lenfatik ve kapiller damarlar yoluyla kana karışır.\n\n"
            "> [SINAV SPOTU] Nekrotik hücrelerin kana sızdırdığı dokuya özgü enzim ve proteinlere 'Serum Biyobelirteçleri' "
            "(kardiyak/hepatik enzimler) denir. Bu belirteçler organ hasarının varlığını, yerini ve şiddetini gösterir.\n\n"
            "Apoptozda ise plazma zarı bütünlüğünü koruduğu ve parçalar apoptotik cisimcikler halinde fagositoza "
            "uğradığı için serum enzim yüksekliği görülmez."
        ),
        "medicalTerms": [
            {"term": "Serum Biyobelirteci", "explanation": "Doku hasarı veya nekrozu sonucu dolaşımda seviyesi yükselen dokuya özgü hücre içi enzim veya protein."},
            {"term": "Membran Rüptürü", "explanation": "Geri dönüşümsüz hasarın kesin işareti olan plazma zarının mekanik/kimyasal delinmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nekrozda hücre zarı bütünlüğü bozulduğunda hücre içi enzimler kana sızar.",
            "📌 [SINAV SPOTU] Apoptozda zar sağlam kaldığından serum enzim sızıntısı izlenmez."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enzim Sızıntı Prensibi", "desc": "Plazma zarı delinmesi sonucu intraselüler proteinlerin kanda tespiti.", "isKey": True},
                {"title": "Nekroz Ayrımı", "desc": "Nekrozda enzimler fırlar; apoptozda zar korunduğu için sessiz kalır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Nekroza uğrayan bir dokuda serum enzimlerinin kanda belirgin şekilde yükselmesinin temel hücresel nedeni nedir?",
                "Plazma zarı bütünlüğünün bozulması (zar rüptürü) sonucu sitoplazmik enzimlerin ekstraselüler aralığa ve kana kaçmasıdır."
            ),
            make_cloze(
                "Hücre zarı bütünlüğü bozulduğunda sitoplazmik enzimlerin kana sızmasıyla organ hasarını gösteren serum biyobelirteçleri yükselir.",
                "serum biyobelirteçleri",
                "Kana karışan hasar göstergesi doku proteinleri"
            )
        ]
    })

    # ADIM 27
    slides.append({
        "slideNumber": 27,
        "title": "Miyokard Nekrozu Biyobelirteçleri: Troponin ve CK-MB Kinetiği",
        "subtitle": "Kalp kası koagülatif nekrozunda kanda yükselen altın standart proteinler",
        "badge": "Kardiyoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Akut miyokard enfarktüsünde koroner arter tıkanıklığını takip eden 20-30 dakika içinde kardiyomiyositler "
            "geri dönüşümsüz hasara girer ve sarkolemma (plazma zarı) parçalanır. Kalp kasına özgü kontraktil ve "
            "sitoplazmik proteinler dolaşıma dökülür.\n\n"
            "Ders notumuzda özellikle vurgulanan miyokard izoenzimi 'CK-MB'dir (Kreatin Kinaz MB). İnfarkttan 2-4 saat "
            "sonra kanda yükselmeye başlar, 24 saatte pik yapar ve 48-72 saatte normale döner.\n\n"
            "> [SINAV SPOTU] Günümüzde en duyarlı ve özgül kardiyak nekroz belirteci Kardiyak Troponin I ve T'dir (cTnI, cTnT). "
            "Troponinler 7-10 gün boyunca kanda yüksek kalarak geç tanıya da olanak tanır.\n\n"
            "CK-MB'nin ise yarı ömrü kısa olduğu için ilk infarkttan sonraki günlerde gelişen 're-infarkt' (yeniden infarkt) "
            "tanısında troponine üstün bir klinik değere sahiptir."
        ),
        "medicalTerms": [
            {"term": "CK-MB", "explanation": "Kreatin kinazın miyokard dokusuna özgü izoenzimi; erken dönem nekroz belirteci."},
            {"term": "Kardiyak Troponin (cTnI / cTnT)", "explanation": "Miyokard nekrozunun en duyarlı ve özgül altın standart biyobelirteci."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Miyokard nekrozunda serumda CK-MB (Creatin Kinaz Miyokard İzoenzimi) ve Troponin yükselir.",
            "📌 [SINAV SPOTU] CK-MB re-infarkt tanısında kullanılırken, Troponin en duyarlı ve uzun süreli belirteçtir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Miyokardit ve İnfarkt", "desc": "Kardiyomiyosit zarının parçalanmasıyla kana sızan proteinler.", "isKey": True},
                {"title": "Zaman Çizelgesi", "desc": "Troponin 7-10 gün kanda kalır; CK-MB 48-72 saatte temizlenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut miyokard enfarktüsü geçiren ve 5 gün önce başarılı stent uygulanan hastada yeniden şiddetli göğüs ağrısı başlıyor. Hastada yeni bir re-infarkt gelişip gelişmediğini ayırt etmek için hangi serum belirteci en uygundur?",
                [
                    {
                        "text": "Kardiyak Troponin I; çünkü kanda en yüksek konsantrasyona o ulaşır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Troponin ilk infarkttan sonra 7-10 gün yüksek kaldığından yeni atağı ayırt edemez."
                    },
                    {
                        "text": "CK-MB; çünkü yarı ömrü kısadır (48-72 saatte normale döner) ve yeni nekrozda tekrar pik yapar.",
                        "isCorrect": True,
                        "feedback": "Kusursuz klinik karar! CK-MB erken normale döndüğü için re-infarkt tanısında altın standarttır."
                    },
                    {
                        "text": "Alkalen Fosfataz (ALP); çünkü damar endotelinden salınır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! ALP safra yolu ve kemik belirtecidir."
                    }
                ]
            ),
            make_cloze(
                "Miyokard nekrozunda kardiyomiyosit sarkolemması parçalandığında serumda CK-MB ve troponin düzeyleri hızla yükselir.",
                "CK-MB",
                "Kreatin kinazın kalp kasına özgü izoenzimi kısaltması"
            )
        ]
    })

    # ADIM 28
    slides.append({
        "slideNumber": 28,
        "title": "Hepatobiliyer ve Pankreatik Biyobelirteçler: Organ Özgüllüğü",
        "subtitle": "ALT, AST, ALP, Amilaz ve Lipaz enzimlerinin tanısal klinik dağılımı",
        "badge": "Enzimler",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Farklı organların parankim hücreleri kendilerine has metabolik enzimlerle donatılmıştır; bu nedenle "
            "plazma zarının yırtılmasıyla kana sızan enzim profili hekime hasarlı organı doğrudan fısıldar.\n\n"
            "Karaciğer hasarında hepatosit zarları parçalanınca Alanin Aminotransferaz (ALT) ve Aspartat Aminotransferaz (AST) "
            "seruma sızar. ALT karaciğere son derece özgü bir sitozolik enzimdir. AST ise hem mitokondride hem sitozolde "
            "bulunur ve kalpte de mevcuttur (alkolik hepatitte AST/ALT oranı > 2 olur).\n\n"
            "> [SINAV SPOTU] Safra yolları epitel hasarında ve kolestazda 'Alkalen Fosfataz (ALP)' ve GGT artar. "
            "Akut pankreas nekrozunda ise 'Amilaz' ve özellikle daha özgül olan 'Lipaz' serumda tavan yapar.\n\n"
            "Tüm vücut hücrelerinde bulunan LDH ise non-spesifik doku yıkımının (hemoliz, infarkt) genel aynasıdır."
        ),
        "medicalTerms": [
            {"term": "ALT (Alanin Aminotransferaz)", "explanation": "Hepatosit sitoplazmasına özgüllüğü en yüksek olan karaciğer hasar enzimi."},
            {"term": "ALP (Alkalen Fosfataz)", "explanation": "Safra kanalikül membranı ve kemik osteoblastlarında bulunan, kolestazda artan enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hepatosit nekrozu / hasarı: ALT ve AST yükselir (ALT karaciğere daha spesifiktir).",
            "📌 [SINAV SPOTU] Safra yolu hasarı / kolestaz: Alkalen Fosfataz (ALP) yüksekliği görülür.",
            "📌 [SINAV SPOTU] Pankreas nekrozu: Lipaz ve Amilaz yükselir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Karaciğer İmzası", "desc": "Hepatit ve toksik nekrozda fırlayan ALT ve AST.", "isKey": True},
                {"title": "Biliyer ve Pankreas İmzası", "desc": "Safra yolunda ALP artışı, pankreatitte lipaz yüksekliği.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hasar Gören Doku / Organ", "Yükselen Serum Biyobelirteci", "Enzimin Başlıca İntraselüler Kaynağı"],
                [
                    [("Miyokard Nekrozu", False, ""), ("CK-MB ve Troponin (cTnI/T)", True, "Kardiyak enzimler"), ("Kardiyomiyosit sitozolü ve miyofilament", False, "")],
                    [("Hepatosit Nekrozu", False, ""), ("ALT ve AST", True, "Karaciğer transaminazları"), ("Hepatosit sitoplazması ve mitokondrisi", False, "")],
                    [("Safra Yolu Epitel Hasarı", False, ""), ("Alkalen Fosfataz (ALP)", True, "Safra yolu belirteci"), ("Kanaliküler apikal plazma zarı", False, "")],
                    [("Pankreas Asiner Nekrozu", False, ""), ("Lipaz ve Amilaz", True, "Pankreas enzimleri"), ("Asiner zimojen granülleri", False, "")]
                ]
            ),
            make_cloze(
                "Safra yollarında tıkanıklık veya epitel hasarı geliştiğinde serumda alkalen fosfataz düzeyi belirgin şekilde yükselir.",
                "alkalen fosfataz",
                "Kolestazda yükselen kanaliküler enzim tam adı"
            )
        ]
    })

    # ADIM 29 (CHECKPOINT 3)
    slides.append({
        "slideNumber": 29,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Fibrinoid Nekroz ve Biyobelirteçler",
        "subtitle": "Damar nekrozu, immün kompleksler, malign hipertansiyon ve serum enzimlerinin sentezi",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 3,
        "synthesisNarrative": (
            "Bu kontrol noktasında, mikroskopik damar nekrozu olan fibrinoid nekrozu ve hücre ölümüyle "
            "dolaşıma saçılan serum biyobelirteçlerini konsolide ediyoruz.\n\n"
            "Fibrinoid nekroz; küçük damar duvarlarında immün kompleks birikimi (Poliarteritis Nodosa gibi vaskülitler) "
            "veya aşırı mekanik tansiyon (Malign Hipertansiyon) sonucu plazma proteinlerinin (özellikle fibrin) "
            "sızarak damar duvarında parlak pembe, amorf ve camsı bir bant oluşturmasıdır.\n\n"
            "> [ÖZET REÇETE] Damar duvarında camsı parlak pembe = Fibrinoid Nekroz (PAN veya Malign HT)! "
            "Zar parçalanması = Serum enzim kaçışı: Kalp -> CK-MB / Troponin; Karaciğer -> ALT / AST; Safra -> ALP!\n\n"
            "Bu biyokimyasal kaçış prensibi acil tıp ve yoğun bakım pratiğinin temel teşhis omurgasını oluşturur."
        ),
        "medicalTerms": [
            {"term": "Fibrinoid Görünüm", "explanation": "Damar duvarında antijen-antikor ve fibrin birleşimiyle oluşan camsı pembe nekroz."},
            {"term": "Serum Biyobelirteci", "explanation": "Hücre zarı parçalandığında kana karışan dokuya özgü enzim."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Fibrinoid nekroz makroskopide görülmez; mikroskopide damar duvarında parlak pembe amorf camsı materyaldir.",
            "📌 [CHECKPOINT ÖZETİ] Poliarteritis Nodosa (PAN) ve Malign Hipertansiyon en klasik iki örneğidir.",
            "📌 [CHECKPOINT ÖZETİ] Biyobelirteçler: Miyokard -> CK-MB/Troponin, Hepatosit -> ALT/AST, Safra -> ALP, Pankreas -> Lipaz."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-07",
                "Fibrinoid nekrozun ışık mikroskopisindeki karakteristik görüntüsü ve biyokimyasal içeriği nedir?",
                "Damar duvarında parlak pembe, amorf ve 'camsı' bir materyal izlenir; içeriği antijen-antikor immün kompleksleri ve plazmadan sızan fibrin proteinidir."
            ),
            make_flashcard(
                "fc-k1-05-08",
                "Fibrinoid nekrozun görüldüğü iki temel klinik hastalık tablosu nedir?",
                "1) Sistemik vaskülitler (özellikle Poliarteritis Nodosa / PAN) ve 2) Şiddetli kan basıncı yüksekliği (Malign Hipertansiyon)."
            ),
            make_flashcard(
                "fc-k1-05-09",
                "Nekroza uğrayan organların dolaşıma saldığı tipik biyobelirteç eşleşmeleri nelerdir?",
                "Miyokard nekrozu: CK-MB ve Troponin; Hepatosit hasarı: ALT ve AST; Safra yolu hasarı: ALP (Alkalen Fosfataz); Pankreas: Lipaz ve Amilaz."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Fibrinoid Nekroz ve Doku Biyobelirteçleri Sentez Tablosu",
                "headers": ["Klinik Tablo", "Primer Patoloji / Enzim", "Doku / Hücre Hedefi"],
                "rows": [
                    ["Poliarteritis Nodosa", "Transmural Fibrinoid Nekroz", "Küçük ve orta musküler arterler"],
                    ["Malign Hipertansiyon", "Fibrinoid Nekroz + Soğan Zarı", "Afferent renal arterioller"],
                    ["Akut Kalp İnfarktüsü", "Troponin I/T ve CK-MB Kaçışı", "Kardiyomiyosit sarkolemması"],
                    ["Akut Viral Hepatit", "ALT ve AST Kaçışı", "Hepatosit hücre zarı"],
                    ["Biliyer Tıkanma / Kolestaz", "Alkalen Fosfataz (ALP) Kaçışı", "Safra kanalikül apikal zarı"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Klinik Durum", "Etkilenen Vasküler / Parankimal Yapı", "Beklenen Laboratuvar / Patoloji Bulgusu"],
                [
                    [("Poliarteritis Nodosa (PAN)", False, ""), ("Musküler Arter Duvarı", True, "Hedef damar yapısı"), ("Transmural Fibrinoid Nekroz", False, "")],
                    [("Malign Hipertansiyon", False, ""), ("Böbrek Arteriolleri", True, "Basınçtan yırtılan damar"), ("Afferent arteriol nekrozu", False, "")],
                    [("Akut Miyokard İnfarktüsü", False, ""), ("Kardiyomiyositler", True, "Hasar gören kas hücresi"), ("Serum Troponin ve CK-MB artışı", False, "")]
                ]
            ),
            make_active_recall(
                "Neden kazeöz veya koagülatif nekroz çıplak gözle (makroskobik) görülebilirken fibrinoid nekroz yalnızca ışık mikroskobunda tanınır?",
                "Çünkü fibrinoid nekroz mikroskobik çaptaki kan damarlarının duvarlarında fokal olarak gelişir; makroskobik bir doku kitlesi oluşturmaz."
            )
        ]
    })

    # ADIM 30
    slides.append({
        "slideNumber": 30,
        "title": "Serum Enzimlerinin Zamansal Klirensi: Karaciğer ve Böbrek Eliminasyonu",
        "subtitle": "Kanda yükselen enzimlerin yarı ömürleri ve organ yetmezliklerindeki kinetik yanılgılar",
        "badge": "Farmakokinetik",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dolaşıma karışan hücre içi enzimlerin serumdaki düzeyi yalnızca nekrozun şiddetine değil, "
            "aynı zamanda bu proteinlerin plazmadan temizlenme (klirens) hızına da doğrudan bağlıdır.\n\n"
            "Küçük moleküllü kardiyak miyoglobin dakikalar içinde glomerüllerden süzülüp idrarla atılırken "
            "(hızlı yükselir ve birkaç saatte kaybolur), CK-MB karaciğer ve retiküloendotelyal sistem tarafından "
            "48-72 saatte parçalanır. Troponin molekülleri ise miyofibrillere bağlı komplekslerden günlerce "
            "yavaş yavaş kana salındığı için 10-14 gün boyunca yüksek kalır.\n\n"
            "> [KLİNİK İPUCU] Böbrek yetmezliği olan bir hastada idrarla atılan enzimler (örn. amilaz) kanda "
            "daha uzun süre yüksek kalabilir; bu durum hekimi yalancı bir pankreatit nüksü şüphesine düşürebilir.\n\n"
            "Bu nedenle enzim düzeyleri klinik semptomlar ve EKG/radyoloji ile daima kombine değerlendirilmelidir."
        ),
        "medicalTerms": [
            {"term": "Enzim Klirensi", "explanation": "Nekroz enzimlerinin karaciğer, böbrek veya retiküloendotelyal sistem tarafından kandan temizlenme hızı."},
            {"term": "Yalancı Yükseklik", "explanation": "Organ hasarı devam etmediği halde klirens bozukluğuna bağlı enzimin kanda uzun süre kalması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enzimlerin serumda kalış süreleri moleküler ağırlıklarına ve klirens yollarına bağlıdır.",
            "📌 [SINAV SPOTU] Troponin yavaş salınımı nedeniyle 7-14 gün, CK-MB ise 2-3 gün kanda saptanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Klirens Kinetiği", "desc": "Miyoglobin hızla böbrekten atılır; troponin 10 gün salınmaya devam eder.", "isKey": True},
                {"title": "Böbrek Yetmezliği Yanılgısı", "desc": "Böbrek fonksiyon bozukluğunda amilaz klirensinin gecikmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Akut miyokard infarktüsü şüphesi olan bir hastada göğüs ağrısının 8. gününde hala kanda yüksek tespit edilebilen en duyarlı kardiyak nekroz belirteci hangisidir?",
                {
                    "A": "Miyoglobin",
                    "B": "CK-MB",
                    "C": "Kardiyak Troponin I / T",
                    "D": "LDH-5",
                    "E": "Alkalen fosfataz"
                },
                "C",
                {
                    "A": "Miyoglobin ilk 24 saatte hızla normale döner.",
                    "B": "CK-MB 48-72 saatte normale döner.",
                    "C": "Doğru cevap C'dir: Kardiyak troponinler infarkttan sonra 7-14 gün boyunca kanda yüksek kalır.",
                    "D": "LDH-5 karaciğer/iskelet kasına aittir.",
                    "E": "ALP kardiyak belirteç değildir."
                }
            ),
            make_cloze(
                "Miyokard nekrozunun geç döneminde (7-14 gün) dahi kanda yüksek kalarak teşhise olanak tanıyan kardiyak belirteç troponin molekülüdür.",
                "troponin",
                "Miyokard infarktüsünün altın standart uzun ömürlü proteini"
            )
        ]
    })

    return slides
