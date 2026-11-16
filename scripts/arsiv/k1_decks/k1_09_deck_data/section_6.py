"""
Akut Enflamasyon (Ders 9) - Bölüm 6: Transüda vs Eksüda, Staz ve Lenfatik Sistem
Slayt 51 - 60 (Checkpoint 6: Slayt 59)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "slideNumber": 51,
        "title": "Vücut Boşluklarında Sıvı Birikimi: Transüda ve Eksüda Kavramları",
        "subtitle": "Kardiyovasküler hemodinami bozukluğu mu, yoksa enflamatuvar bariyer yıkımı mı?",
        "badge": "Sıvı Biyopatolojisi",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Patolojide ve klinik tıpta interstisyel dokularda veya seröz vücut boşluklarında (plevra, periton, perikard) "
            "sıvı toplanmasına genel olarak **Ödem (veya efüzyon)** adı verilir. Ancak toplanan bu sıvının patogenetik "
            "kökeni iki zıt kutba ayrılır: **Transüda** ve **Eksüda**.\n\n"
            "- **Transüda (Hemodinamik Kaçak):** Damar endotel geçirgenliği tamamen normaldir. Sıvı kaçışı; ya kapiller "
            "içi **hidrostatik basıncın artması** (örneğin konjestif kalp yetmezliğinde venöz göllenme) ya da plazma "
            "**kolloid onkotik basıncının düşmesi** (örneğin nefrotik sendrom veya karaciğer sirozunda hipoalbüminemi) "
            "sonucu gelişir. Proteinden ve hücreden fakirdir; ultrafiltrat niteliğindedir.\n\n"
            "- **Eksüda (Enflamatuvar Kaçak):** Altta yatan temel bozukluk **mikrovasküler endotel geçirgenliğinin artmasıdır**. "
            "Proteinler, fibrinojen ve lökositler damar dışına fırlar. Yüksek proteinli, yüksek dansiteli ve hücreden zengindir."
        ),
        "medicalTerms": [
            {"term": "Transüda", "explanation": "Damar geçirgenliği bozulmaksızın hidrostatik basınç artışı veya onkotik basınç düşüşüyle oluşan berrak, düşük proteinli sıvıdır."},
            {"term": "Eksüda", "explanation": "Enflamasyona bağlı artmış vasküler geçirgenlik sonucu damar dışına çıkan bulanık, yüksek proteinli ve hücresel sıvıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Transüdada damar geçirgenliği NORMALDİR; eksüdada ise damar geçirgenliği ARTMIŞTIR.",
            "📌 [SINAV SPOTU] Kalp yetmezliği ve siroz transüda, apandisit ve bakteriyel plörit eksüda yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Transüda Kökeni", "desc": "Bozulmuş hemodinami (basınç dengesizliği), normal endotel.", "isKey": True},
                {"title": "Eksüda Kökeni", "desc": "Enflamasyon, delinmiş endotel bariyeri, zengin içerik.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Transüda Sıvısı vs Eksüda Sıvısı",
                "Transüda (Hemodinamik Sıvı)",
                "Berrak, açık sarı; protein < 3 g/dL; dansite < 1.012; lökosit sayısı çok az; fibrin yok, pıhtılaşmaz.",
                "Eksüda (Enflamatuvar Sıvı)",
                "Bulanık, koyu renk; protein > 3 g/dL; dansite > 1.020; bol nötrofil ve hücresel debris; fibrinojen var, pıhtılaşır."
            ),
            make_cloze(
                "Damar endotel geçirgenliği bozulmaksızın hidrostatik basınç artışı veya hipoalbüminemi nedeniyle oluşan düşük proteinli sıvıya transüda adı verilir.",
                "transüda",
                "Kalp yetmezliği ve sirozda oluşan berrak sızıntı sıvısının tıbbi adı"
            )
        ]
    })

    # Slide 52
    slides.append({
        "slideNumber": 52,
        "title": "Transüda ve Eksüdanın Laboratuvar Ayrımı: Light Kriterleri ve Dansite",
        "subtitle": "Dansite, total protein, LDH düzeyi ve hücresel içerik parametreleri",
        "badge": "Laboratuvar Tanı",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Klinik pratikte parasentez veya torasentez ile alınan bir sıvının enflamatuvar (eksüda) mı yoksa hemodinamik "
            "(transüda) mi olduğunu anlamak için kesin laboratuvar kriterleri kullanılır:\n\n"
            "1. **Spesifik Dansite (Özgül Ağırlık):**\n"
            "   - Transüda: **< 1.012** (neredeyse saf su gibi hafiftir).\n"
            "   - Eksüda: **> 1.020** (ağır protein molekülleri ve hücreler sıvıyı ağırlaştırır).\n\n"
            "2. **Total Protein Konsantrasyonu:**\n"
            "   - Transüda: **< 3.0 g/dL** (genellikle < 1.5 - 2 g/dL).\n"
            "   - Eksüda: **> 3.0 g/dL** (plazma albümin ve globülinleri dokuya kaçmıştır).\n\n"
            "3. **Light Kriterleri (Plevral Efüzyon Altın Standardı):**\n"
            "   - Plevra sıvısı protein / Serum protein oranı **> 0.5** ise EKSÜDA.\n"
            "   - Plevra sıvısı LDH / Serum LDH oranı **> 0.6** ise EKSÜDA.\n"
            "   - Plevra sıvısı LDH düzeyi normal serum üst sınırının **2/3'ünden yüksek** ise EKSÜDA."
        ),
        "medicalTerms": [
            {"term": "Spesifik Dansite", "explanation": "Sıvının birim hacminin distile suya göre ağırlığıdır; içindeki çözünmüş protein ve hücre miktarıyla doğru orantılıdır."},
            {"term": "Light Kriterleri", "explanation": "Plevral efüzyonların transüda-eksüda ayrımında kullanılan protein ve LDH oranlarına dayalı uluslararası tanı kriterleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dansite > 1.020 ve Protein > 3.0 g/dL EKSÜDA için tanı koydurucudur.",
            "📌 [SINAV SPOTU] Sıvı / Serum protein oranı > 0.5 olması Light kriterlerine göre eksüda lehinedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dansite Sınırı", "desc": "1.012 altı transüda, 1.020 üstü eksüdadır.", "isKey": True},
                {"title": "Protein ve LDH", "desc": "Eksüda yüksek protein ve laktat dehidrogenaz içerir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Laboratuvar Parametresi", "Transüda Sıvısı (Hemodinamik)", "Eksüda Sıvısı (Enflamatuvar)"],
                [
                    [("Spesifik Dansite (Özgül Ağırlık)", False, ""), ("Düşük (< 1.012)", False, ""), ("Yüksek (> 1.020)", True, "Ağır proteinler ve hücrelerle yoğunlaşmış sıvı eşiği")],
                    [("Total Protein Konsantrasyonu", False, ""), ("Düşük (< 3.0 g/dL)", False, ""), ("Yüksek (> 3.0 g/dL)", True, "Damardan sızan albümin ve immünglobülin bolluğu")],
                    [("Sıvı / Serum Protein Oranı", False, ""), ("< 0.5", False, ""), ("> 0.5", True, "Light kriterlerine göre protein oran eşiği")],
                    [("Sıvı / Serum LDH Oranı", False, ""), ("< 0.6", False, ""), ("> 0.6", True, "Hücre yıkımını yansıtan enzim oran eşiği")],
                    [("Fibrinojen ve Pıhtılaşma", False, ""), ("Yok, spontan pıhtılaşmaz", False, ""), ("Var, bekleyince spontan pıhtılaşır", True, "Fibrin polimerizasyonu ile jelleşen yapı")]
                ]
            ),
            make_micro_quiz(
                "Akciğerinde sıvı toplanan bir hastadan yapılan torasentezde; sıvının dansitesi 1.026, total proteini 4.2 g/dL ve bol nötrofil içerdiği saptanıyor. Bu sıvı için en doğru tanımlama hangisidir?",
                {
                    "A": "Konjestif kalp yetmezliğine bağlı transüda",
                    "B": "Nefrotik sendroma bağlı hipoalbüminemik ödem",
                    "C": "Akut bakteriyel pnömoniye sekonder paraponömonik eksüda",
                    "D": "Karaciğer sirozuna bağlı asit sıvısı",
                    "E": "Açlık malnütrisyonuna bağlı transüda"
                },
                "C",
                {
                    "A": "Kalp yetmezliği transüda yapar; dansite <1.012, protein <3 g/dL olur.",
                    "B": "Nefrotik sendrom transüdadır.",
                    "C": "Doğru cevap C'dir: Dansite >1.020, protein >3 g/dL ve bol nötrofil varlığı tipik bir enflamatuvar eksüdadır (bakteriyel enfeksiyon).",
                    "D": "Siroz transüdadır.",
                    "E": "Malnütrisyon transüdadır."
                }
            )
        ]
    })

    # Slide 53
    slides.append({
        "slideNumber": 53,
        "title": "İltihaplı Sıvının Tipleri: Seröz, Fibrinöz, Pürülan ve Hemorajik",
        "subtitle": "Eksüdanın protein, fibrin, canlı/ölü lökosit ve eritrosit içeriğine göre morfolojik spektrumu",
        "badge": "Eksüda Tipleri",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Enflamatuvar eksüda homojen tek bir sıvı değildir; doku hasarının şiddetine ve etkenin doğasına göre "
            "dört ana morfolojik tipe bürünür:\n\n"
            "1. **Seröz Eksüda:** En hafif formdur. Nispeten proteinden zengin ancak hücreden fakir, berrak sarımsı "
            "sıvıdır. Tipik örnek: Deri su toplaması (bül), hafif yanık veya viral perikardit.\n\n"
            "2. **Fibrinöz Eksüda:** Vasküler geçirgenlik çok daha büyüktür; kandan dev **fibrinojen** molekülleri sızar "
            "ve dokuda çözünmeyen fibrin liflerine dönüşür. Kalpte veya plevrada tereyağlı ekmek manzarası "
            "(bread and butter perikardit) oluşturur.\n\n"
            "3. **Pürülan (Süpüratif) Eksüda / İrin (Pus):** Piyojenik (irin yapıcı) bakteriyel enfeksiyonlarda görülür. "
            "Kitleler halinde canlı ve ölü nötrofiller, nekrotik parankim hücreleri ve sıvıdan oluşur (koyu kıvamlı, sarı-yeşil).\n\n"
            "4. **Hemorajik Eksüda:** Damar duvarı yırtılmış veya eritilmiş, ortama masif eritrosit karışmıştır "
            "(örneğin antraks enfeksiyonu, tümör invazyonu veya tüberküloz plöriti)."
        ),
        "medicalTerms": [
            {"term": "Pus (İrin)", "explanation": "Nötrofiller, sıvılaşmış nekrotik doku artıkları ve mikroplardan oluşan koyu kıvamlı süpüratif eksüdadır."},
            {"term": "Piyojenik Bakteri", "explanation": "Dokuya masif nötrofil çekerek irin (abse) oluşturan bakterilerdir (Staphylococcus aureus, Streptococcus pyogenes)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Pus (irin) = Nötrofil + Sıvılaşmış nekrotik doku + Ölü bakteri + Eksüdadır.",
            "📌 [SINAV SPOTU] Fibrinöz eksüda temizlenemezse organize olarak fibröz yapışıklıklara (adezyon) yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Seröz ve Fibrinöz", "desc": "Hafif proteinli bül sıvısından ağır fibrin liflerine.", "isKey": True},
                {"title": "Pürülan ve Hemorajik", "desc": "Nötrofil zengini irin ve damar yırtılmasıyla kanlı eksüda.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Eksüda Tipi", "Baskın Mikroskobik İçeriği", "Karakteristik Klinik Örneği"],
                [
                    [("Seröz Eksüda", False, ""), ("Hücreden fakir berrak protein sıvısı", False, ""), ("İkinci derece yüzeyel yanık bülü, vezikül", True, "Güneş yanığında deriyi kabartan su kabarcığı")],
                    [("Fibrinöz Eksüda", False, ""), ("Yoğun ağsı fibrin iplikçikleri ve lifler", False, ""), ("Üremik perikardit ('tereyağlı ekmek' manzarası)", True, "Seröz zarların birbirine yapıştığı lezyon")],
                    [("Pürülan Eksüda (Pus)", False, ""), ("Masif canlı/ölü nötrofil ve nekrotik debris", False, ""), ("Akut apandisit, pyojenik bakteriyel abse", True, "Stafilokok enfeksiyonlarında sarı-yeşil irin")],
                    [("Hemorajik Eksüda", False, ""), ("Yüksek konsantrasyonda intakt eritrositler", False, ""), ("Malign plevral mezotelyoma, antraks enfeksiyonu", True, "Damar duvarının erimesiyle kanlı sıvı")]
                ]
            ),
            make_cloze(
                "Piyojenik bakteriyel enfeksiyonlarda çok sayıda ölü ve canlı nötrofil ile erimiş nekrotik doku artıklarından oluşan süpüratif sıvıya pus (irin) adı verilir.",
                "pus",
                "Halk arasında cerahat veya irin olarak bilinen tıbbi Latince terim"
            )
        ]
    })

    # Slide 54
    slides.append({
        "slideNumber": 54,
        "title": "Kan Akımının Duraklaması (Staz): Eritrosit Yığılması ve Asidoz",
        "subtitle": "Kılcal damarlarda eritrositlerin birbirine kenetlenmesi, lokal hipoksi ve doku pH düşüşü",
        "badge": "Hemoreoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Vasküler geçirgenliğin artmasıyla damar içi sıvının dokuya boşalması mikrodolaşımda derin bir reolojik "
            "felakete yol açar:\n\n"
            "- Plazma kaybettikçe damar lümeninde eritrosit konsantrasyonu tavan yapar (**hemokonsantrasyon**).\n"
            "- Fibrinojenin de etkisiyle eritrositler diskoid yüzeylerinden birbirine yapışır ve madeni paralar gibi "
            "dizilerek **rulo formasyonu** oluşturur.\n"
            "- Kan akımı durma noktasına gelir (**staz**); venüller eritrositlerle ağzına kadar tıka basa dolar (vasküler konjesyon).\n\n"
            "> **Stazın Biyokimyasal Faturası:**\n"
            "Kan akımı durakladığında dokuya taze oksijen girişi kesilir; lokal **hipoksi** gelişir. Dokuda biriken "
            "laktik asit ve karbondioksit lokal doku pH'sını asidik seviyelere (**asidoz**) çeker. Bu asidoz nötrofillerin "
            "lizozomal enzimlerinin çalışması için ideal bir asidik ortam hazırlar."
        ),
        "medicalTerms": [
            {"term": "Vasküler Konjesyon", "explanation": "Damarların kan hücreleri ve özellikle eritrositlerle pasif olarak aşırı dolup tıkanmasıdır."},
            {"term": "Lokal Doku Asidozu", "explanation": "Staz ve hipoksiye bağlı anaerobik glikoliz sonucu laktik asit birikerek doku pH'sının düşmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Stazın histopatolojik görüntüsü postkapiller venüllerin sıkışık eritrosit kütleleriyle tıkalı olmasıdır.",
            "📌 [SINAV SPOTU] Doku asidozu hem lizozomal asit hidrolazların aktivitesini destekler hem de ağrı hissini (dolor) alevlendirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemokonsantrasyon", "desc": "Sıvı kaybolur, eritrositler lümende balık istifi yığılır.", "isKey": True},
                {"title": "Lokal Asidoz", "desc": "Hipoksi anaerobik metabolizmayı ve laktik asidi tetikler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Stazdan Doku Asidozuna Giden Hemodinamik Yol",
                [
                    "1. Mikrovasküler geçirgenlik artışıyla plazma doku aralığına kaçar",
                    "2. Damar içi hematokrit yükselir, eritrositler rulo dizilimi oluşturarak lümeni tıkar",
                    "3. Kan akım hızı neredeyse sıfırlanır ve lokal doku hipoksisi gelişir",
                    "4. Parankim hücreleri anaerobik glikolize geçerek ortama laktat pompalar ve doku asidozu oturur"
                ]
            ),
            make_active_recall(
                "Akut enflamasyonda kan akımının duraklamasıyla (staz) ortaya çıkan lokal doku asidozunun hücresel savunma açısından önemi nedir?",
                "Nötrofil ve makrofajların lizozomlarında bulunan mikrobisidal asit hidrolaz enzimlerinin optimal çalışabilmesi için asidik pH ortamına ihtiyaç duymasıdır."
            )
        ]
    })

    # Slide 55
    slides.append({
        "slideNumber": 55,
        "title": "Lenfatik Sistemin Enflamasyondaki Dinamiği: Drenaj ve Taşıma",
        "subtitle": "Kör uçlu lenf kapillerlerinin gerilmesi, lenf akım hızının artışı ve immün gözetim",
        "badge": "Lenfatik Dolaşım",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Doku aralığına fışkıran eksüda sıvısı sadece interstisyumda beklemez; vücudun drenaj kanalları olan "
            "**lenfatik damarlar** tarafından emilir:\n\n"
            "- Enflamasyonlu dokuda lenfatik kapillerlerin çevresindeki çapa filamanları (anchoring filaments) gerilir; "
            "lenf kapiller lümeni sonuna kadar açılır.\n"
            "- Hasarlı bölgeden drene olan **lenf sıvısı akım hızı kat kat artar**.\n"
            "- Bu artmış drenaj dokudaki aşırı ödem sıvısını boşaltarak doku basıncını düşürmeye çalışır.\n\n"
            "> **İmmünolojik Misyon:**\n"
            "Lenf sıvısı sadece su taşımaz; hasar bölgesindeki **bakterileri, mikrobiyal antijenleri, toksinleri ve "
            "dendritik hücreleri** sırtlayarak en yakın bölgesel lenf düğümüne (sentinel lenf nodu) taşır.\n"
            "Burada bekleyen T ve B lenfositleri uyarılarak edinsel (adaptif) immün yanıt başlatılır."
        ),
        "medicalTerms": [
            {"term": "Çapa Filamanları (Anchoring Filaments)", "explanation": "Lenf kapiller endotelini çevre bağ dokusuna bağlayan ve ödem anında lümeni açan elastik liflerdir."},
            {"term": "Antijen Sunumu", "explanation": "Dokudan lenfle taşınan mikropların lenf nodunda T lenfositlere gösterilerek bağışıklık kurulmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enflamasyonda lenf akım hızı dramatik şekilde artar; lenfatikler ödemi tahliye eder.",
            "📌 [SINAV SPOTU] Lenf akımı mikropları bölgesel lenf noduna taşıyarak adaptif immün yanıtı tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Drenaj Patlaması", "desc": "Lenf kapillerleri genişleyerek eksüdayı drene eder.", "isKey": True},
                {"title": "Antijen Taşınması", "desc": "Mikroplar lenf noduna götürülüp lenfositlere sunulur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "İstirahat Lenf Damarı vs Enflamatuvar Lenf Damarı",
                "İstirahat Lenf Damarı",
                "Lümen dardır, lenf akımı çok yavaştır, sıvı berraktır, içinde neredeyse hiç mikrop ve lökosit bulunmaz.",
                "Enflamatuvar Lenf Damarı",
                "Çapa lifleriyle sonuna kadar açılmış lümen, hızla akan bol eksüda, içinde bakteriler, antijenler ve göç eden lökositler."
            ),
            make_cloze(
                "Doku ödemi sırasında lenf kapiller endotelini çekerek lümenin sonuna kadar açılmasını sağlayan bağ dokusu liflerine çapa filamanları adı verilir.",
                "çapa filamanları",
                "İngilizce anchoring filaments olarak bilinen mikroskopik elastik askı lifleri"
            )
        ]
    })

    # Slide 56
    slides.append({
        "slideNumber": 56,
        "title": "Lenfanjit (Lymphangitis): Yangının Drenaj Yollarını Sarması",
        "subtitle": "Ciltte enfeksiyon odağından lenf bezine uzanan ağrılı kırmızı çizgiler",
        "badge": "Klinik Patoloji",
        "badgeColor": "rose",
        "synthesisNarrative": (
            "Bazen hasar bölgesindeki mikrobiyal yük veya toksin yoğunluğu lenfatik damarın taşıma kapasitesini aşar; "
            "lenf damarının kendi duvarı enfekte olur ve iltihaplanır: **Lenfanjit (Lymphangitis)**.\n\n"
            "- En sık etken deriden giren **Streptococcus pyogenes (A grubu beta-hemolitik streptokok)** veya "
            "Staphylococcus aureus'tur.\n"
            "- Lenf damarı duvarında endotel nekrozu, lümende nötrofiller ve fibrin pıhtıları gelişir.\n\n"
            "> **Klasik Fizik Muayene Bulgusu:**\n"
            "Hastanın ekstremitesindeki enfekte yara odağından (örneğin parmaktaki panaris veya enfekte çizik) "
            "koltuk altına (aksilla) veya kasığa (inguinal) doğru uzanan, deri üzerinde **kırmızı, sıcak, hassas ve "
            "ağrılı çizgilenmeler (eritematöz bantlar)** izlenir.\n"
            "Bu durum mikropların lenf yoluyla hızla yayılmakta olduğunun alarm verici klinik kanıtıdır."
        ),
        "medicalTerms": [
            {"term": "Lenfanjit", "explanation": "Mikroorganizma veya toksinlerin lenf kapillerlerini ve toplayıcı lenf damarlarını enfekte edip iltihaplandırmasıdır."},
            {"term": "Eritematöz Çizgilenme", "explanation": "İltihaplı lenf damarı boyunca deri yüzeyinde beliren parlak kırmızı yangı hattıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Deride enfeksiyon odağından lenf noduna uzanan kırmızı çizgiler LENFANJİT tanısı koydurur.",
            "📌 [SINAV SPOTU] Lenfanjitin en sık bakteriyel etkeni Streptococcus pyogenes'tir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kırmızı Hat", "desc": "Lenf damarı trasesi boyunca uzanan ağrılı kırmızı çizgi.", "isKey": True},
                {"title": "Bakteriyel Yayılım", "desc": "Streptokokların lenf damarı endotelini istila etmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Enfeksiyon odağından bölgesel lenf bezlerine doğru uzanan ağrılı ve sıcak kırmızı çizgilenmelerle karakterize lenf damarı iltihabına lenfanjit adı verilir.",
                "lenfanjit",
                "Lenfatik kanalların bakteriyel enflamasyonunu ifade eden klinik patoloji terimi"
            ),
            make_active_recall(
                "Ayağındaki enfekte tırnak batması sonrası bacağı boyunca kasığa doğru uzanan ağrılı kırmızı çizgiler beliren bir hastada bu lezyonun anatomik ve histopatolojik temeli nedir?",
                "Ayaktaki streptokok veya stafilokokların lenf kapillerlerine girerek toplayıcı lenf damarı duvarını enfekte etmesi (lenfanjit), damar çevresinde hiperemi ve nötrofilik eksüdasyon yaratmasıdır."
            )
        ]
    })

    # Slide 57
    slides.append({
        "slideNumber": 57,
        "title": "Reaktif Lenfadenit (Lymphadenitis): Lenf Düğümünün Alarm Yanıtı",
        "subtitle": "Kapsül gerilimi, foliküler hiperplazi, sinüs histiyositozu ve hassas lenfadenopati",
        "badge": "Lenf Nodu Patolojisi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Lenfatik damarlarla taşınan mikroplar ve eksüda ilk filtreleme istasyonu olan **Bölgesel Lenf Düğümüne** ulaşır. "
            "Lenf nodu bu istilaya karşı şiddetli bir enflamatuvar ve proliferatif yanıt verir: **Reaktif Lenfadenit**.\n\n"
            "Patofizyolojik Değişiklikler:\n"
            "1. **Sinüs Histiyositozu:** Subkapsüler ve medüller sinüsler mikropları yakalayan aktive makrofajlarla tıka basa dolar.\n"
            "2. **Foliküler Hiperplazi:** B lenfosit alanlarındaki germinal merkezler hızla büyür; antikor üretimi için "
            "klonal proliferasyon başlar.\n"
            "3. **Parakortikal Hiperplazi:** T lenfosit bölgeleri genişler.\n\n"
            "> **Ağrının Nedeni:** Lenf nodu içine hücum eden lökositler ve ödem nedeniyle lenf bezi saatler içinde "
            "hızla şişer. Dışını saran **fibröz kapsül gerilir**. Kapsüldeki nosiseptörler uyarıldığı için reaktif "
            "lenfadenitlerde lenf bezi **büyümüş, yumuşak ve son derece HASSAS / AĞRILIDIR** (malignite infiltrasyonlarında "
            "ise yavaş büyüdüğü için genellikle ağrısız ve serttir)."
        ),
        "medicalTerms": [
            {"term": "Lenfadenit", "explanation": "Bölgesel lenf düğümünün mikrobiyal ve enflamatuvar ajanlarla enfekte olarak büyümesi ve iltihaplanmasıdır."},
            {"term": "Kapsüler Gerilim Ağrısı", "explanation": "Akut şişen lenf bezinin gerilen fibröz kapsülündeki duyusal sinirlerin ağrı üretmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut reaktif enflamatuvar lenfadenopatinin ayırt edici özelliği lenf nodunun AĞRILI ve HASSAS olmasıdır.",
            "📌 [SINAV SPOTU] Ağrının nedeni lenf nodu kapsülünün hızla gerilmesidir; metastatik kanser nodları ise genellikle ağrısız ve fiksedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Filtre İstasyonu", "desc": "Sinüsler makrofajla dolar, mikroplar yakalanır.", "isKey": True},
                {"title": "Hassas Büyüme", "desc": "Kapsül gerilmesiyle ağrılı reaktif lenf bezi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Akut Enflamatuvar Lenfadenit vs Metastatik Kanserli Lenf Nodu",
                "Akut Enflamatuvar Lenfadenit",
                "Hızla büyür, kapsülü gerildiği için ağrılı ve hassastır, yumuşak-elastik kıvamdadır, çevreye hareketlidir.",
                "Metastatik Kanserli Lenf Nodu",
                "Aylar içinde sinsi büyür, ağrısızdır, taş gibi serttir, çevre dokulara yapışık (fikse) ve hareketsizdir."
            ),
            make_cloze(
                "Akut bakteriyel tonsillit geçiren bir çocukta çene altı lenf bezlerinin palpasyonda belirgin şekilde ağrılı ve hassas olmasının temel patolojik sebebi lenf nodu kapsülünün gerilmesidir.",
                "kapsülünün",
                "Organı dıştan saran ve hızla şiştiğinde duyusal sinirleri uyarılan fibröz kılıfı"
            )
        ]
    })

    # Slide 58
    slides.append({
        "slideNumber": 58,
        "title": "Bakteriyemi ve Sepsise Açılan Kapı: Bariyerlerin İflası",
        "subtitle": "Lenf nodu filtresi delindiğinde mikropların duktus torasikus yoluyla kana karışması",
        "badge": "Sistemik İstilâ",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Lenfatik sistem konağı koruyan harika bir savunma barajıdır; ancak mikroorganizmalar aşırı virülan ise "
            "veya konak immünitesi zayıfsa bu baraj çöker:\n\n"
            "1. Enfeksiyon odağından kalkan bakteriler lenf kapillerlerini istila eder (**lenfanjit**).\n"
            "2. Bölgesel lenf düğümüne ulaşırlar; lenf nodu makrofajları mikropları fagosite etmeye çalışır ancak "
            "mikroplar lenf nodu parankimini nekroze ederek filtreyi deler (**süpüratif lenfadenit**).\n"
            "3. Lenf nodunu aşan mikroorganizmalar eferent lenf damarlarına geçer.\n"
            "4. Büyük lenfatik kanallar (özellikle **Duktus Torasikus**) yoluyla sol subklaviyan ven bileşkesinden "
            "doğrudan sistemik kan dolaşımına dökülürler.\n\n"
            "> **Sonuç:** Kanda serbest canlı bakterilerin çoğalması (**Bakteriyemi ve Sepsis**); bakterilerin dalak, "
            "karaciğer, kemik iliği ve kalp kapaklarına tutunarak metastatik apseler (piyemi) ve septik şok oluşturmasıdır."
        ),
        "medicalTerms": [
            {"term": "Bakteriyemi", "explanation": "Canlı bakterilerin lenfatik bariyerleri aşarak sistemik kan dolaşımına geçmesidir."},
            {"term": "Piyemi", "explanation": "Kana karışan pyojenik bakterilerin uzak organlara yerleşerek çoklu metastatik apseler oluşturmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lenf nodu filtresi aşıldığında mikroplar duktus torasikus üzerinden doğrudan venöz kana dökülür.",
            "📌 [SINAV SPOTU] Sepsis, lenfatik ve immün bariyerlerin mikrobu lokalize etmekte yetersiz kaldığının kanıtıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Barajın Yıkılması", "desc": "Lenf nodu aşılır, mikroplar eferent lenfe sızar.", "isKey": True},
                {"title": "Kana Dökülme", "desc": "Duktus torasikus ile kan dolaşımına ve sepsise geçiş.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Lokal Odaktan Septik Şoka Uzanan Yayılım Zinciri",
                [
                    "1. Lokal dokudaki apse odağından mikroplar lenfatik kapillerlere girer",
                    "2. Lenf damarı iltihaplanır ve ciltte kırmızı hat belirir (lenfanjit)",
                    "3. Bölgesel lenf nodu şişer ancak bakteriyel yükle delinir (lenfadenit)",
                    "4. Eferent lenf damarları mikropları duktus torasikusa ve venöz dolaşıma boşaltır",
                    "5. Kanda yayılan bakteriler sistemik sitokin fırtınası ve septik şok tablosu yaratır"
                ]
            ),
            make_micro_quiz(
                "Lokal bir doku enfeksiyonunda bakterilerin lenfatik drenaj yoluyla kan dolaşımına karışmasında anatomik son geçiş kapısı olan ana lenf damarı hangisidir?",
                {
                    "A": "Vena kava inferior",
                    "B": "Duktus torasikus (Thoracic duct)",
                    "C": "Portal ven",
                    "D": "Splenik ven",
                    "E": "Pulmoner arter"
                },
                "B",
                {
                    "A": "Vena kava ana venöz damardır, lenfatik kanal değildir.",
                    "B": "Doğru cevap B'dir: Vücudun büyük kısmının lenfini toplayan duktus torasikus, sol subklaviyan-juguler ven birleşiminden doğrudan venöz kana açılır.",
                    "C": "Portal ven bağırsak kanını karaciğere taşır.",
                    "D": "Splenik ven dalak venidir.",
                    "E": "Pulmoner arter sağ ventrikülden akciğere kan götürür."
                }
            )
        ]
    })

    # Slide 59 (CHECKPOINT 6)
    slides.append({
        "slideNumber": 59,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Transüda vs Eksüda ve Lenfatik Patoloji",
        "subtitle": "Bölüm 6 Sıvı Tipleri, Light Kriterleri, Staz Asidozu, Lenfanjit ve Lenfadenit",
        "badge": "Checkpoint 6",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Altıncı kontrol noktasında sıvı dinamikleri ve lenfatik savunmayı sabitliyoruz:\n\n"
            "1. **Transüda vs Eksüda:**\n"
            "   - **Transüda:** Normal endotel, bozuk hemodinami (hidrostatik artış/onkotik düşüş), berrak, dansite < 1.012, "
            "protein < 3.0 g/dL, hücre yok.\n"
            "   - **Eksüda:** Artmış vasküler geçirgenlik, bulanık, dansite > 1.020, protein > 3.0 g/dL, bol lökosit ve fibrin.\n"
            "2. **Eksüda Türleri:** Seröz (berrak bül), Fibrinöz (lifli adezyon), Pürülan/Pus (nötrofil zengini irin), "
            "Hemorajik (eritrositli yıkım).\n"
            "3. **Staz:** Sıvı kaçağıyla hemokonsantrasyon -> Kan vizkozitesi artar -> Rulo formasyonu -> Akım duraklar -> "
            "Hipoksi ve lokal doku asidozu.\n"
            "4. **Lenfatik Yanıt:** Çapa lifleriyle açılan lenf damarları aşırı sıvıyı drene eder; antijenleri lenf noduna taşır.\n"
            "5. **Lenfanjit:** Lenf damarı iltihabı (kırmızı çizgilenmeler; en sık S. pyogenes).\n"
            "6. **Reaktif Lenfadenit:** Lenf nodu kapsülünün hızla gerilmesiyle karakterize **ağrılı, hassas ve yumuşak** lenf bezi."
        ),
        "medicalTerms": [
            {"term": "Reaktif Hiperplazi", "explanation": "Enflamatuvar uyarana yanıt olarak lenf nodundaki lenfosit ve makrofajların hızla çoğalmasıdır."},
            {"term": "Hemodinamik Denge", "explanation": "Starling kuralları çerçevesinde damar içi ve interstisyel sıvı hareketinin dengede kalmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dansite > 1.020 ve protein > 3.0 g/dL EKSÜDA'dır.",
            "📌 [SINAV SPOTU] Akut lenfadenitin en tipik klinik özelliği kapsül gerilmesine bağlı AĞRILI olmasıdır.",
            "📌 [SINAV SPOTU] Kırmızı çizgiler = Lenfanjit (Streptococcus pyogenes)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sıvı Ayrımı", "desc": "Transüda (hemodinamik/temiz) vs Eksüda (enflamatuvar/proteinli).", "isKey": True},
                {"title": "Lenfatik İkili", "desc": "Lenfanjit (kırmızı çizgi) ve Lenfadenit (ağrılı beze).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Akut bakteriyel enfeksiyonlarda bölgesel lenf nodunun hızla büyüyüp palpasyonda son derece ağrılı ve hassas olmasına karşın, metastatik kanser tutulumlarında lenf nodunun neden ağrısız ve sert olduğunu açıklayınız?",
                "Akut enflamasyonda masif ödem ve hücre göçüyle lenf nodu saatler içinde hızla şişerek dışındaki fibröz kapsülü aniden gerer ve ağrı yapar; kanser metastazında ise tümör hücreleri haftalar-aylar içinde yavaşça çoğaldığı için kapsül gerilmez ve ağrı oluşmaz."
            ),
            make_cloze(
                "Enflamasyonlu bir dokudan bölgesel lenf düğümlerine doğru uzanan ağrılı eritematöz kırmızı çizgilerin varlığı lenfanjit tablosunu gösterir.",
                "lenfanjit",
                "Lenf damarlarının bakteriyel enfeksiyonu ve yangısı"
            ),
            make_before_after(
                "Transüda Sıvısı (Kalp Yetmezliği) vs Eksüda Sıvısı (Akut Apandisit)",
                "Transüda Sıvısı",
                "Berrak sarı, dansite <1.012, protein <3 g/dL, LDH düşük, pıhtılaşmaz, nötrofil içermez.",
                "Eksüda Sıvısı",
                "Bulanık, sarı-yeşil, dansite >1.020, protein >3 g/dL, LDH yüksek, spontan pıhtılaşır, bol nötrofil içerir."
            )
        ]
    })

    # Slide 60
    slides.append({
        "slideNumber": 60,
        "title": "Bölüm 6 Entegrasyonu: Plevral Efüzyonlu Hastaya Klinik Yaklaşım",
        "subtitle": "Torasentez örneğinin laboratuvar algoritması: Siroz mu, Pnömoni mi, Malignite mi?",
        "badge": "Klinik Karar Algoritması",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Klinik pratikte göğüs hastalıkları ve iç hastalıkları uzmanlarının her gün uyguladığı algoritma, "
            "bu bölümün tam bir sentezidir:\n\n"
            "Hastaya torasentez yapılır ve plevra sıvısı incelenir:\n"
            "1. **Adım 1 - Transüda / Eksüda Ayrımı:** Dansite, protein ve LDH bakılır (Light kriterleri).\n"
            "   - Eğer Transüda ise: Akciğer masumdur; hastada kalp yetmezliği, karaciğer sirozu veya nefrotik sendrom araştırılır.\n"
            "   - Eğer Eksüda ise: Akciğerde lokal bir patoloji vardır; Adım 2'ye geçilir.\n\n"
            "2. **Adım 2 - Eksüdanın Hücresel Tipi:**\n"
            "   - Baskın hücre **Nötrofil** ise: Parapnömonik efüzyon veya ampiyem (akut bakteriyel pnömoni).\n"
            "   - Baskın hücre **Lenfosit** ise: Tüberküloz plöriti veya metastatik kanser (malign efüzyon).\n"
            "   - Sıvı kanlı (Hemorajik) ise: Malignite (akciğer ca, mezotelyoma) veya pulmoner enfarktüs."
        ),
        "medicalTerms": [
            {"term": "Ampiyem", "explanation": "Plevra boşluğu gibi anatomik bir vücut boşluğunun tamamen pürülan eksüda (irin) ile dolmasıdır."},
            {"term": "Parapnömonik Efüzyon", "explanation": "Bakteriyel pnömoniye komşu plevra yapraklarında gelişen enflamatuvar eksüda birikimidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Plevra sıvısında nötrofil hakimiyeti akut pnömoni/ampiyem, lenfosit hakimiyeti tüberküloz/kanser göstergesidir.",
            "📌 [SINAV SPOTU] Ampiyem plevral boşlukta yerleşik irin topluluğudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Adım 1: Kriter", "desc": "Light kriterleri ile transüda ve eksüda ayrımı.", "isKey": True},
                {"title": "Adım 2: Sitoloji", "desc": "Nötrofil ise pnömoni, lenfosit ise tüberküloz veya kanser.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Nefes darlığı ve ateşle başvuran bir hastanın plevral sıvısında protein 4.8 g/dL, dansite 1.024 ve lökositlerin %85'i nötrofil olarak saptanıyor. En olası patolojik tanı ve doğru klinik yaklaşım ne olmalıdır?",
                [
                    {"text": "Bakteriyel pnömoniye sekonder gelişmiş akut parapnömonik eksüda; uygun antibiyotik tedavisi ve drenaj planlanmalıdır", "isCorrect": True, "feedback": "Kusursuz klinik akıl yürütme! Yüksek protein, yüksek dansite ve nötrofil baskınlığı tipik akut bakteriyel eksüdadır."},
                    {"text": "Konjestif kalp yetmezliğine bağlı transüda; hastaya hemen diüretik başlanmalıdır", "isCorrect": False, "feedback": "Kalp yetmezliği proteini düşük transüda yapar; nötrofil içermez."},
                    {"text": "Primer nefrotik sendrom kaçağı; hastaya immünsüpresif başlanmalıdır", "isCorrect": False, "feedback": "Nefrotik sendrom hipoalbüminemik transüda yapar."}
                ]
            ),
            make_cloze(
                "Plevra boşluğunun bakteriyel enfeksiyon sonucu tamamen pürülan eksüda (irin) ile dolması tablosuna ampiyem adı verilir.",
                "ampiyem",
                "Doğal anatomik boşluklarda biriken kapalı irin koleksiyonunun tıbbi adı"
            )
        ]
    })

    return slides
