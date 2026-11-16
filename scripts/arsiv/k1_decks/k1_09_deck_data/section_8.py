"""
Akut Enflamasyon (Ders 9) - Bölüm 8: Diapedez (PECAM-1), Kemotaksi ve Hücresel Göç
Slayt 71 - 80 (Checkpoint 8: Slayt 79)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "slideNumber": 71,
        "title": "Transmigrasyon (Diapedez): Damar Duvarını Aşmak",
        "subtitle": "Endotel kavşaklarından sürünerek geçiş ve PECAM-1 (CD31) molekülünün homofilik köprüsü",
        "badge": "Diapedez",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Lökosit integrinleri sayesinde endotel üzerinde tamamen durdurulduktan sonra sıra damar duvarını "
            "aşmaya gelir: Bu olaya **Transmigrasyon** veya **Diapedez** denir.\n\n"
            "- **Anatomik Bölge:** Neredeyse tamamen **Postkapiller Venüllerde** gerçekleşir.\n"
            "- **Mekanizma:** Lökosit psödopodlarını (yalancı ayaklarını) iki komşu endotel hücresinin arasındaki "
            "bağlantı kompleksine (junction) sokar.\n"
            "- **Anahtar Molekül - PECAM-1 (CD31 / Platelet Endothelial Cell Adhesion Molecule-1):**\n"
            "  * Hem lökositin yüzeyinde hem de endotel hücrelerinin birbirine bakan yan yüzeylerinde bulunur.\n"
            "  * İki hücre arasındaki temas **homofilik bağlanma** (CD31'in CD31'e tutunması) ile kurulur.\n"
            "  * Bu etkileşim lökositi endotel hücrelerinin arasından geçirerek subendotelyal bazal membrana doğru "
            "bir fermuar gibi çeker.\n\n"
            "> Not: CD31 / PECAM-1 blokajı yapıldığında lökositler endotel yüzeyinde sıkıca yapışık kalır ama "
            "damar dışına asla çıkamaz."
        ),
        "medicalTerms": [
            {"term": "Diapedez (Transmigrasyon)", "explanation": "Lökositlerin endotel hücre kavşaklarından geçerek damar lümeninden perivasküler alana çıkmasıdır."},
            {"term": "PECAM-1 (CD31)", "explanation": "Lökosit ve endotel hücre temas yüzeylerinde yer alan, homofilik bağlanmayla transmigrasyonu sağlayan immünglobülin ailesi moleküldür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lökosit transmigrasyonundan (diapedez) sorumlu temel molekül PECAM-1'dir (CD31).",
            "📌 [SINAV SPOTU] PECAM-1 homofilik bağlanma yapar (lökosit CD31'i endotel CD31'ine bağlanır).",
            "📌 [SINAV SPOTU] Patolojide CD31 aynı zamanda endotel hücrelerinin ve vasküler tümörlerin en güvenilir immünhistokimyasal belirtecidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "CD31 Fermuarı", "desc": "Lökosit ve endotel CD31'i birleşerek geçişi sağlar.", "isKey": True},
                {"title": "Venüler Çıkış", "desc": "Hücre psödopod uzatarak endotel arasından süzülür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Lökositlerin postkapiller venül endotel kavşaklarından doku aralığına geçişini (diapedez) sağlayan temel adezyon molekülü PECAM-1 molekülüdür.",
                "PECAM-1",
                "CD31 adıyla da bilinen trombosit-endotel hücre adezyon molekülü kısaltması"
            ),
            make_active_recall(
                "Deneysel bir çalışmada antikorlarla bloke edildiğinde lökositlerin endotel üzerinde sıkıca yapışık kalmasına rağmen damar dışına çıkamadığı saptanan adezyon molekülü hangisidir?",
                "PECAM-1 (CD31) molekülüdür; çünkü transmigrasyon / diapedez basamağından spesifik olarak sorumludur."
            )
        ]
    })

    # Slide 72
    slides.append({
        "slideNumber": 72,
        "title": "Bazal Membranın Delinmesi: Matriks Metalloproteinazların (MMP) Rolü",
        "subtitle": "Kollajenazların tip IV kollajeni sindirmesi ve lökositin ekstravasküler alana ayak basması",
        "badge": "Enzimatik Geçiş",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Endotel hücrelerinin arasından geçen lökosit henüz tam olarak dokuda değildir; önünde aşılması gereken "
            "son ve en sert mekanik engel vardır: **Vasküler Bazal Membran**.\n\n"
            "- Bazal membran yoğun bir Tip IV kollajen, laminin ve proteoglikan örgüsünden oluşmuştur.\n"
            "- Lökosit bu engeli mekanik bir güçle yırtamaz; **kimyasal ve enzimatik sindirim** kullanır.\n\n"
            "> **Enzimatik Delinme:**\n"
            "Nötrofiller ve monositler salgıladıkları **Matriks Metalloproteinazlar (özellikle MMP-9 / Jelatinaz B "
            "ve Tip IV Kollajenaz)** ile bazal membrandaki tip IV kollajen liflerini lokal olarak sindirirler.\n"
            "Açılan mikroskobik pencereden geçen lökosit artık serbestçe doku interstisyumundadır.\n"
            "Bazal membran geçişten hemen sonra fibroblastlar ve perisitler tarafından hızla onarılır."
        ),
        "medicalTerms": [
            {"term": "Tip IV Kollajenaz", "explanation": "Damar bazal membranının ana iskeleti olan tip IV kollajeni parçalayarak lökosite yol açan matriks metalloproteinazdır."},
            {"term": "Perisit", "explanation": "Kapiller ve venül bazal membranına gömülü duran, damar geçirgenliği ve duvar stabilitesini denetleyen kontraktil hücredir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lökositler bazal membranı Tip IV kollajenaz (MMP-9) salgılayarak enzimatik olarak delerler.",
            "📌 [SINAV SPOTU] Bazal membran delinmesi geçicidir; doku bütünlüğü hızla restore edilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "MMP-9 Salınımı", "desc": "Lökosit jelatinaz ve kollajenaz boşaltarak lifleri eritir.", "isKey": True},
                {"title": "Dokuya Çıkış", "desc": "Açılan pencereden geçerek perivasküler stroma ile buluşur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Endoteli Aşmaktan Dokuda Yürümeye Geçiş Zinciri",
                [
                    "1. Lökosit PECAM-1 (CD31) aracılığıyla endotel hücreler arası kavşaktan süzülür",
                    "2. Endotelin hemen altında kalın Tip IV kollajen bazal membranına çarpar",
                    "3. Lökosit lizozomlarından ve granüllerinden Tip IV kollajenaz (MMP) salgılar",
                    "4. Bazal membranda açılan fokal yarıktan geçerek bağ dokusu matriksine ayak basar"
                ]
            ),
            make_cloze(
                "Lökositlerin vasküler bazal membranı eriterek doku interstisyumuna geçebilmek için salgıladıkları temel proteolitik enzim tip IV kollajenaz enzimidir.",
                "kollajenaz",
                "Bazal membran kollajen liflerini parçalayan matriks metalloproteinaz türü"
            )
        ]
    })

    # Slide 73
    slides.append({
        "slideNumber": 73,
        "title": "Kemotaksi (Chemotaxis): Kimyasal Gradyan Boyunca Hedefe Koşmak",
        "subtitle": "Konsantrasyon farkını sezen lökositlerin hasar odağına yönlendirilmiş amip benzeri hareketi",
        "badge": "Yönlendirilmiş Göç",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Damardan doku aralığına çıkan bir nötrofil nerede savaşacağını nasıl bilir? Rastgele mi dolanır, "
            "yoksa hedefine kilitlenmiş bir füze gibi mi ilerler?\n\n"
            "Bu mucizevi yön bulma süreci **Kemotaksi (Chemotaxis)** ile gerçekleşir:\n\n"
            "- Kemotaksi, hücrelerin kimyasal bir maddenin **artan konsantrasyon gradyanı boyunca** hasar odağına "
            "doğru yönlendirilmiş lokomosyonudur (hareketidir).\n"
            "- Hasar merkezinde bakteriler ve sentinel hücreler yüksek miktarda kemotaktik madde üretir.\n"
            "- Bu maddeler doku interstisyumunda difüze olarak bir gradyan (eğim) kurar; hasar odağında en yoğun, "
            "damar çevresinde daha seyrektir.\n"
            "- Lökosit, yüzeyindeki reseptörlerle bu gradyanın en yoğun olduğu yönü hisseder ve psödopodlarını o yöne "
            "uzatarak dakikada onlarca mikrometre hızla hedefe doğru koşar."
        ),
        "medicalTerms": [
            {"term": "Kemotaksi", "explanation": "Hücrelerin ekstrasellüler bir kimyasal uyaranın yoğunluk farkını izleyerek hedefe doğru yönlendirilmiş hareketidir."},
            {"term": "Kemotaktik Gradyan", "explanation": "Kaynaktan uzaklaştıkça azalan kimyasal madde konsantrasyon farkıdır; hücrelere pusula görevi görür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kemotaksi kimyasal bir gradyan boyunca gerçekleşen yönlendirilmiş lokomosyondur.",
            "📌 [SINAV SPOTU] Hem eksojen (bakteriyel) hem endojen (sitokin/kompleman) kaynaklı kemoatraktanlar mevcuttur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kimyasal Pusula", "desc": "Yoğunluk farkını algılayıp hedefe yönelir.", "isKey": True},
                {"title": "Lokomosyon", "desc": "Amip benzeri yalancı ayaklarla bağ dokusunda yürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Rastgele Hücresel Hareket vs Kemotaktik Yönlendirilmiş Göç",
                "Rastgele Hareket (Kemotaksi Yok)",
                "Lökosit bağ dokusunda yön tayin edemez, her yöne dağınık psödopod uzatır, bakteriye ulaşamaz.",
                "Kemotaktik Göç (Gradyan Var)",
                "Lökosit kimyasal konsantrasyonun arttığı yöne kilitlenir, polarize olur ve doğrudan bakteri odağına ilerler."
            ),
            make_cloze(
                "Lökositlerin bir kimyasal ajanın artan konsantrasyon gradyanı boyunca hasar odağına doğru yönlendirilmiş hareketine kemotaksi adı verilir.",
                "kemotaksi",
                "Kimyasal pusula ile hedefe göçü tanımlayan biyolojik terim"
            )
        ]
    })

    # Slide 74
    slides.append({
        "slideNumber": 74,
        "title": "Kemotaktik Ajanlar: Eksojen ve Endojen Pusulalar",
        "subtitle": "Bakteriyel formil peptitler, C5a, Lökotrien B4 ve İnterlökin-8 (CXCL8) kalkanı",
        "badge": "Kemoatraktanlar",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "Lökositleri hasar odağına çeken kemotaktik ajanlar kaynaklarına göre ikiye ayrılır:\n\n"
            "1. **Eksojen Kemoatraktanlar (Mikrobiyal Ürünler):**\n"
            "- Bakteriler protein sentezine insanlardan farklı olarak **N-formilmetiyonin** aminoasiti ile başlar.\n"
            "- Bakterilerden sızan **N-formil oligopeptitler** (örneğin fMet-Leu-Phe / fMLP), lökositler için en güçlü "
            "eksojen alarm kokusudur.\n\n"
            "2. **Endojen Kemoatraktanlar (Konak Kaynaklı):**\n"
            "- **Kompleman Sistemi:** **C5a** (ve daha zayıf olarak C3a). Özellikle C5a nötrofiller için en güçlü endojen çekicidir.\n"
            "- **Lipid Mediyatörler:** Arakidonik asit 5-lipoksijenaz yolağından üretilen **Lökotrien B4 (LTB4)**.\n"
            "- **Kemokinler:** Özellikle nötrofiller için özelleşmiş bir kemokin olan **CXCL8 (İnterlökin-8 / IL-8)**; "
            "monositler için MCP-1 (CCL2); eozinofiller için Eotaksin (CCL11)."
        ),
        "medicalTerms": [
            {"term": "N-formil Peptitler", "explanation": "Bakteri protein sentezine özgü olan ve nötrofil FPR1 reseptörünü uyararak kemotaksi başlatan eksojen peptitlerdir."},
            {"term": "Lökotrien B4 (LTB4)", "explanation": "Nötrofillerin güçlü endojen kemotaktik ajanı ve lökosit aktivatörü olan lipid mediyatördür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] En önemli 4 kemotaktik ajan: 1) Bakteriyel formil peptitler, 2) C5a, 3) LTB4, 4) IL-8 (CXCL8)'dir.",
            "📌 [SINAV SPOTU] Nötrofil için en spesifik kemokin İNTERLÖKİN-8'dir (CXCL8).",
            "📌 [SINAV SPOTU] Eozinofiller için spesifik kemokin EOTAKSİN'dir (CCL11)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eksojen: Bakteri", "desc": "N-formilmetiyonin peptitleri en güçlü yabancı çekicidir.", "isKey": True},
                {"title": "Endojen: Konak", "desc": "C5a, LTB4 ve IL-8 nötrofilleri hasar odağına çeker.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Kemotaktik Ajan", "Moleküler Kaynağı", "Hedef Lökosit ve Biyolojik Rolü"],
                [
                    [("N-Formil Peptitler (fMLP)", False, ""), ("Bakteriyel Protein Sentez Artıkları", False, ""), ("Nötrofiller; bakterinin yerini haber veren en güçlü eksojen koku", True, "Mikrobiyal proteinlerin başlangıç aminoasiti")],
                    [("Kompleman C5a", False, ""), ("Plazma Kompleman Kaskadı Parçalanması", False, ""), ("Nötrofil, monosit; güçlü endojen kemotaksi ve fagositoz aktivasyonu", True, "Klasik ve alternatif kompleman yolağı ürünü")],
                    [("Lökotrien B4 (LTB4)", False, ""), ("Arakidonik Asit 5-LOX Metabolizması", False, ""), ("Nötrofiller; lökosit kümelenmesi ve lizozomal degranülasyon", True, "Membran fosfolipitlerinden sentezlenen lipid")],
                    [("İnterlökin-8 (CXCL8)", False, ""), ("Aktive Makrofaj ve Endotel Hücreleri", False, ""), ("Nötrofiller; dokuya özgül göçü yöneten primer kemokin", True, "Kemotaktik sitokin ailesinin prototipi")]
                ]
            ),
            make_micro_quiz(
                "Akut enflamasyonda arakidonik asit metabolizmasından köken alan ve nötrofiller için en güçlü kemotaktik etkiyi gösteren lipid mediyatör aşağıdakilerden hangisidir?",
                {
                    "A": "Lökotrien B4 (LTB4)",
                    "B": "Prostaglandin E2 (PGE2)",
                    "C": "Tromboksan A2 (TXA2)",
                    "D": "Prostasiklin (PGI2)",
                    "E": "Lökotrien C4 (LTC4)"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: LTB4 nötrofillerin primer kemotaktik lipid ajanıdır; LTC4, LTD4 ve LTE4 ise vasküler geçirgenlik ve bronkospazm yapar.",
                    "B": "PGE2 ağrı ve ateş yapar.",
                    "C": "TXA2 trombosit kümeleştirir ve damar büzer.",
                    "D": "PGI2 vazodilatatördür.",
                    "E": "LTC4 venüler geçirgenliği artırır."
                }
            )
        ]
    })

    # Slide 75
    slides.append({
        "slideNumber": 75,
        "title": "Kemotaktik Sinyal İletimi: GPCR ve Aktin İskeleti Lokomosyonu",
        "subtitle": "G-protein kenetli yedi transmembran reseptör, Rho-GTPazlar ve lamellipod itişi",
        "badge": "Hücre Biyofiziği",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Kemotaktik maddeler nötrofil zarına ulaştığında hücrenin içinde büyüleyici bir motor çalışmaya başlar:\n\n"
            "1. **Yedi Transmembran GPCR:** N-formil peptitler, C5a, LTB4 ve kemokinler lökosit yüzeyindeki **G-Protein "
            "Kenetli Reseptörlere (GPCR)** bağlanırlar.\n"
            "2. **İkinci Haberciler:** Reseptör uyarımı ile Fosfolipaz C (PLC) ve Fosfatidilinozitol 3-kinaz (PI3K) devreye girer. "
            "Sitozolik serbest kalsiyum patlaması yaşanır.\n"
            "3. **Rho Ailesi Küçük GTPazlar (Rac, Rho, Cdc42):**\n"
            "   - **Cdc42:** Hücrenin ön ucunda ince ipliksi sensörler (**filopodlar**) oluşturur; yönü koklar.\n"
            "   - **Rac:** Ön uçta geniş yapraksı yalancı ayaklar (**lamellipodlar**) oluşturur ve **G-aktin'i F-aktin "
            "iplikçiklerine polimerize eder**.\n"
            "   - **Rho:** Hücrenin arka ucundaki (üropod) aktomiyozin kompleksini kasar; hücre gövdesini ve çekirdeği "
            "öne doğru fırlatır.\n\n"
            "> Lökosit bu itme-çekme motoruyla bağ dokusunda tıpkı bir paletli tank gibi ilerler."
        ),
        "medicalTerms": [
            {"term": "Lamellipod", "explanation": "Göç eden lökositin ön ucunda aktin polimerizasyonuyla oluşan geniş, yapraksı hareket çıkıntısıdır."},
            {"term": "Rac ve Cdc42", "explanation": "Hücre iskeletinin aktin polimerizasyonunu ve psödopod uzatmasını yöneten küçük G-proteinleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tüm kemotaktik ajanlar G-Protein Kenetli Reseptörler (GPCR) üzerinden sinyal verir.",
            "📌 [SINAV SPOTU] Kemotaktik hareketi sağlayan asıl güç hücrenin ön ucundaki AKTİN POLİMERİZASYONUDUR.",
            "📌 [SINAV SPOTU] Rac ve Cdc42 yalancı ayakları açar, Rho arka ucu kasarak hücreyi öne iter."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "GPCR Motoru", "desc": "Kalsiyum ve kinaz sinyalleriyle aktin iskeletini yönetir.", "isKey": True},
                {"title": "Aktin İtişi", "desc": "Ön uçta lamellipod açılır, arka uç kasılarak ilerler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Kemotaktik Reseptörden Aktin Hareketine Giden Yol",
                [
                    "1. Kemokin (IL-8) lökosit plazma zarındaki G-protein kenetli reseptöre (CXCR1/2) bağlanır",
                    "2. Hücre içinde Fosfolipaz C ve PI3K aktive olarak sitozolik kalsiyumu artırır",
                    "3. Rac ve Cdc42 GTPazları kemotaktik uyarının geldiği ön uçta aktin polimerizasyonunu tetikler",
                    "4. F-aktin lifleri hücre zarını iterek lamellipod ve psödopodları oluşturur",
                    "5. Arka uçtaki Rho aktomiyozini kasarak hücreyi hedefe doğru yürütür"
                ]
            ),
            make_cloze(
                "Lökositlerin kemotaktik uyaran yönünde amip benzeri hareket etmesini sağlayan temel hücre iskeleti olayı aktin polimerizasyonu olayıdır.",
                "aktin",
                "Hücrenin ön ucunda lamellipod oluşturan mikrofilaman proteini"
            )
        ]
    })

    # Slide 76
    slides.append({
        "slideNumber": 76,
        "title": "İnfiltrasyon Kinetiğinin İstisnaları: Standart Nötrofil-Monosit Kuralını Bozanlar",
        "subtitle": "Pseudomonas'ta günlerce nötrofil, virüslerde ilk andan lenfosit, alerjide eozinofil",
        "badge": "Özel Kinetik",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Klasik kural 'ilk 24 saat nötrofil, sonra makrofaj' olsa da patolojide bu kuralı bozan **üç büyük klinik "
            "istisna** vardır ve sınavlarda sıkça sorulur:\n\n"
            "1. **Pseudomonas aeruginosa Enfeksiyonları:**\n"
            "- Pseudomonas enfeksiyonlarında nötrofil infiltrasyonu birkaç gün içinde sonlanmaz; **günlerce (2-4 gün "
            "veya daha uzun süre) kesintisiz nötrofilik kalır**.\n"
            "- Bakterinin sürekli salgıladığı kemotaktik faktörler ve lökositleri öldüren ekzotoksin A nötrofil çağrısını taze tutar.\n\n"
            "2. **Viral Enfeksiyonlar:**\n"
            "- Akut viral enfeksiyonlarda (örneğin viral menenjit, viral miyokardit, influenza) nötrofil evresi neredeyse "
            "hiç görülmez.\n"
            "- Yangının **en başından itibaren ilk gelen ve hakim olan hücreler Lenfositlerdir**.\n\n"
            "3. **Alerjik Reaksiyonlar ve Paraziter İstilalar:**\n"
            "- Tip I aşırı duyarlıkta (astım, saman nezlesi) ve helmint (bağırsak kurdu, hidatik kist) enfeksiyonlarında "
            "ortamdaki eotaksin ve IL-5 nedeniyle **Eozinofiller** baskındır."
        ),
        "medicalTerms": [
            {"term": "Pseudomonas Enflamasyonu", "explanation": "Geleneksel kinetiğin aksine nötrofilik infiltrasyonun günlerce kesintisiz devam ettiği bakteriyel enfeksiyon tablosudur."},
            {"term": "Viral Lenfositoz", "explanation": "Virüslerin intrasellüler patojen olması nedeniyle nötrofil yerine doğrudan T ve B lenfosit yanıtı tetiklemesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Pseudomonas enfeksiyonlarında nötrofil infiltrasyonu 2-4 gün boyunca kesintisiz devam eder.",
            "📌 [SINAV SPOTU] Viral enfeksiyonlarda ilk gelen ve hakim hücre LENFOSİTTİR (nötrofil değil).",
            "📌 [SINAV SPOTU] Alerji ve helmint enfeksiyonlarında hakim hücre EOZİNOFİLDİR."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Pseudomonas İstisnası", "desc": "Nötrofiller günlerce sahadan ayrılmaz.", "isKey": True},
                {"title": "Viral İstisna", "desc": "İlk dakikadan itibaren nötrofil değil lenfosit gelir.", "isKey": True},
                {"title": "Alerji/Helmint", "desc": "Eotaksin ve IL-5 ile sahaya eozinofiller hakim olur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Enfeksiyöz / İmmün Etken", "Klasik Hücresel Kinetik İstisnası", "Baskın Olan Hücre Tipi"],
                [
                    [("Pseudomonas aeruginosa", False, ""), ("İlk 24 saat kuralı bozulur; nötrofiller günlerce kesintisiz gelir", False, ""), ("Polimorfonükleer Nötrofiller", True, "Uzamış nötrofilik süpüratif infiltrat")],
                    [("Akut Viral Enfeksiyonlar", False, ""), ("Nötrofil fazı atlanır; ilk andan itibaren mononükleer yanıt başlar", False, ""), ("Lenfositler (ve Plazma Hücreleri)", True, "Virüslere karşı özgül sitotoksik infiltrat")],
                    [("Helmint Parazitleri / Alerji", False, ""), ("IL-5 ve Eotaksin uyarımıyla eozinofiller bölgeye çekilir", False, ""), ("Eozinofiller", True, "Parazit kütikulasını eriten granüllü hücreler")]
                ]
            ),
            make_micro_quiz(
                "Akut enflamasyonda tipik olarak ilk 6-24 saatte nötrofillerin, ardından monositlerin gelmesi beklenirken; aşağıdaki enfeksiyonların hangisinde nötrofilik infiltrasyon günlerce (2-4 gün boyunca) kesintisiz olarak devam eder?",
                {
                    "A": "Viral aseptik menenjit",
                    "B": "Pseudomonas aeruginosa enfeksiyonu",
                    "C": "Mycobacterium tuberculosis plöriti",
                    "D": "Aspergillus fumigatus pnömonisi",
                    "E": "Ascaris lumbricoides enteriti"
                },
                "B",
                {
                    "A": "Viral menenjitte ilk andan itibaren lenfosit hakimdir.",
                    "B": "Doğru cevap B'dir: Pseudomonas enfeksiyonları standart kinetiğin en bilinen istisnasıdır; nötrofil yanıtı günlerce devam eder.",
                    "C": "Tüberkülozda lenfosit ve epitelioid histiosit hakimdir.",
                    "D": "Aspergillus mantardır.",
                    "E": "Ascaris eozinofili yapar."
                }
            )
        ]
    })

    # Slide 77
    slides.append({
        "slideNumber": 77,
        "title": "Eozinofilik ve Lenfositik Kemotaksi: Özelleşmiş Çağrıcılar",
        "subtitle": "Eotaksin-1 (CCL11), IL-5, VLA-4 ve CXCR3 kemokin eksenleri",
        "badge": "Özgül Trafik",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Nötrofil dışındaki lökositlerin dokuya göçü, kendilerine özel kemokin ve adezyon molekülü kodlarıyla yönetilir:\n\n"
            "- **Eozinofiller:**\n"
            "  * Kemotaktik pusulaları **Eotaksin-1 (CCL11)** ve **Eotaksin-2 (CCL24)** dir.\n"
            "  * Eozinofil yüzeyindeki **CCR3** reseptörüne bağlanırlar.\n"
            "  * Th2 lenfositlerden salınan **İnterlökin-5 (IL-5)** kemik iliğinden eozinofil üretim ve salınımını patlatır.\n"
            "  * Endotel VCAM-1'e tutunmak için kendi yüzeylerindeki **VLA-4** integrinini kullanırlar.\n\n"
            "- **Lenfositler ve Monositler:**\n"
            "  * Monositler için primer kemotaktik ajan **MCP-1 (Monocyte Chemoattractant Protein-1 / CCL2)** dir (CCR2 reseptörü).\n"
            "  * T lenfositler özellikle IFN-γ ile indüklenen **CXCL9, CXCL10 ve CXCL11** kemokinlerini (CXCR3 reseptörü) "
            "izleyerek viral ve granülomatöz odaklara göç ederler."
        ),
        "medicalTerms": [
            {"term": "Eotaksin (CCL11)", "explanation": "Eozinofilleri CCR3 reseptörü aracılığıyla alerji ve parazit alanlarına çeken özgül kemokindir."},
            {"term": "MCP-1 (CCL2)", "explanation": "Monositlerin dokuya göçünü ve makrofaja dönüşümünü yöneten temel kemokindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Eozinofil kemotaksisinin anahtar kemokini EOTAKSİN (CCR3), aktivatörü IL-5'tir.",
            "📌 [SINAV SPOTU] Monosit kemotaksisinin anahtarı MCP-1'dir (CCL2)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eozinofil Kodu", "desc": "Eotaksin + CCR3 + IL-5 ile alerji ve parazite göç.", "isKey": True},
                {"title": "Monosit Kodu", "desc": "MCP-1 + CCR2 ile kronikleşen dokuya göç.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hücre Tipi", "Karakteristik Kemokin Reseptörü", "Spesifik Kemotaktik Ligandı"],
                [
                    [("Nötrofiller", False, ""), ("CXCR1 ve CXCR2", False, ""), ("İnterlökin-8 (CXCL8) ve C5a", True, "Akut bakteriyel yangının ana çağrıcısı")],
                    [("Eozinofiller", False, ""), ("CCR3", False, ""), ("Eotaksin-1 (CCL11) ve Eotaksin-2", True, "Alerjik astım ve parazit odağına çeken ligand")],
                    [("Monositler", False, ""), ("CCR2", False, ""), ("Monosit Kemoatraktan Protein-1 (MCP-1 / CCL2)", True, "Dokuda makrofaj birikimini yöneten kemokin")]
                ]
            ),
            make_cloze(
                "Alerjik astımda ve paraziter enfeksiyonlarda eozinofillerin dokuya göçünü sağlayan en önemli özgül kemokin Eotaksin kemokinidir.",
                "Eotaksin",
                "CCL11 olarak da adlandırılan ve eozinofil CCR3 reseptörüne bağlanan kemokin"
            )
        ]
    })

    # Slide 78
    slides.append({
        "slideNumber": 78,
        "title": "Chédiak-Higashi Sendromu: Mikrotübül ve Vezikül Trafik İflası",
        "subtitle": "LYST gen mutasyonu, dev lizozomal granüller, kemotaksi felci ve parsiyel albinizm",
        "badge": "Genetik Trafik Kusuru",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Lökosit kemotaksisinin ve vezikül trafiğinin patolojik çöküşünü gösteren en klasik hastalık "
            "**Chédiak-Higashi Sendromudur**:\n\n"
            "- **Genetik Kusur:** Otozomal resesif geçişlidir. Lizozomal taşıma regülatör proteinini kodlayan "
            "**LYST (CHS1) geninde mutasyon** vardır.\n"
            "- Mikrotübül polimerizasyonu ve organel füzyon mekanizması felç olur.\n\n"
            "> **Hastalığın Dört Temel Histopatolojik ve Klinik Manifestasyonu:**\n"
            "1. **Bozulmuş Kemotaksi:** Lökosit mikrotübül iskeletini organize edemediği için psödopod uzatıp "
            "kemotaktik gradyana doğru yürüyemez (lokomosyon felci).\n"
            "2. **Dev Lizozomal Granüller:** Lökositlerin içinde lizozomlar kontrolsüzce birbirine kaynar; periferik "
            "yaymada nötrofil sitoplazmasında **devasa, kaba lizozom agregatları** patognomoniktir.\n"
            "3. **Fago-lizozom Füzyon Kusuru:** Nötrofil bakteriyi yutsa bile dev lizozom fagozomla birleşemez; mikrop öldürülemez.\n"
            "4. **Parsiyel Albinizm ve Nöropati:** Melanozomlar keratinositlere aktarılamaz (göz ve saçta pigment azlığı) "
            "ve periferik sinirlerde aksonal taşınma bozulur."
        ),
        "medicalTerms": [
            {"term": "Chédiak-Higashi Sendromu", "explanation": "LYST gen mutasyonu sonucu mikrotübül ve lizozomal füzyon defektiyle giden, dev granüller ve albinizmle seyreden immün yetmezliktir."},
            {"term": "Dev Lizozom", "explanation": "Vezikül trafiği bozulduğu için lizozomların parçalanamayıp kontrolsüz kaynaşmasıyla oluşan devasa organeldir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Chédiak-Higashi sendromunda mutasyon LYST genindedir; mikrotübül ve vezikül füzyonu bozuktur.",
            "📌 [SINAV SPOTU] Periferik yaymada nötrofillerde DEV LİZOZOMAL GRANÜLLER görülmesi patognomoniktir.",
            "📌 [SINAV SPOTU] Kemotaksi bozukluğu + Fago-lizozom füzyon yetersizliği + Parsiyel albinizm triadı vardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "LYST Mutasyonu", "desc": "Mikrotübül felci ile kemotaksi ve fagositoz durur.", "isKey": True},
                {"title": "Dev Granüller", "desc": "Nötrofillerde kaynaşmış devasa lizozomlar görülür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Açık renk saçları, açık teni (albinizm), nistagmusu olan ve tekrarlayan piyojenik cilt apseleri geçiren bir çocuğun periferik kan yaymasında nötrofillerin sitoplazmasında dev, kaba mor-mavi granüller izleniyor. Bu hastadaki temel hücresel patoloji nedir?",
                [
                    {"text": "LYST gen mutasyonuna bağlı mikrotübül trafiği bozukluğu, kemotaksi felci ve fago-lizozom füzyon yetersizliği (Chédiak-Higashi sendromu)", "isCorrect": True, "feedback": "Harika teşhis! Parsiyel albinizm ve dev nötrofil granülleri Chédiak-Higashi sendromunun tartışmasız göstergesidir."},
                    {"text": "NADPH oksidaz gen defektine bağlı serbest oksijen radikali üretememe (Kronik Granülomatöz Hastalık)", "isCorrect": False, "feedback": "KGH'de granüller normaldir ve albinizm eşlik etmez."},
                    {"text": "CD18 eksikliğine bağlı lökosit integrin adezyon kusuru (LAD-1)", "isCorrect": False, "feedback": "LAD-1'de dev granül ve albinizm görülmez."}
                ]
            ),
            make_cloze(
                "Chédiak-Higashi sendromunda mikrotübül polimerizasyonunu bozarak lökosit kemotaksisini ve fago-lizozom füzyonunu felç eden mutant gen LYST genidir.",
                "LYST",
                "Lizozomal transport regülatör proteinini kodlayan sorumlu gen kısaltması"
            )
        ]
    })

    # Slide 79 (CHECKPOINT 8)
    slides.append({
        "slideNumber": 79,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Diapedez, Kemotaksi ve Hücresel Göç",
        "subtitle": "Bölüm 8 PECAM-1 (CD31), MMP-9, Kemotaktik Gradyan, GPCR, Kinetik ve Chédiak-Higashi",
        "badge": "Checkpoint 8",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Sekizinci kontrol noktasında damardan hasar odağına hücresel intikali sabitliyoruz:\n\n"
            "1. **Transmigrasyon (Diapedez):** Postkapiller venüllerde **PECAM-1 (CD31)** homofilik bağlanmasıyla "
            "endotel kavşağından geçiş.\n"
            "2. **Bazal Membran Delinmesi:** Lökosit kaynaklı **Tip IV kollajenaz (MMP-9)** ile enzimatik sindirim.\n"
            "3. **Kemotaksi:** Kimyasal konsantrasyon gradyanı boyunca yönlendirilmiş hareket. Reseptörler **GPCR**'dir; "
            "lokomosyonu hücre ön ucundaki **aktin polimerizasyonu** (Rac/Cdc42) sağlar.\n"
            "4. **Kemoatraktanlar:**\n"
            "   - Eksojen: Bakteriyel **N-formilmetiyonin peptitleri**.\n"
            "   - Endojen: **C5a**, **Lökotrien B4 (LTB4)** ve **İnterlökin-8 (CXCL8)**.\n"
            "5. **Özel Kinetikler:** Pseudomonas (günlerce nötrofil), Virüsler (ilk andan lenfosit), Parazit/Alerji (eozinofil / eotaksin).\n"
            "6. **Chédiak-Higashi:** LYST mutasyonu -> Mikrotübül felci -> Bozuk kemotaksi + Dev lizozomlar + Fago-lizozom "
            "füzyon kusuru + Parsiyel albinizm."
        ),
        "medicalTerms": [
            {"term": "Homofilik Etkileşim", "explanation": "İki hücrenin birbirine aynı yüzey molekülü üzerinden (CD31'in CD31'e) kilitlenmesidir."},
            {"term": "Füzyon Defekti", "explanation": "Veziküllerin hedef membranla birleşemeyerek içeriğini aktaramamasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Diapedez = PECAM-1 (CD31).",
            "📌 [SINAV SPOTU] Kemotaktik pusulalar: fMLP, C5a, LTB4, IL-8.",
            "📌 [SINAV SPOTU] Chédiak-Higashi = LYST mutasyonu, dev lizozomal granüller, bozuk kemotaksi, albinizm."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "CD31 ve MMP", "desc": "Endoteli PECAM-1 ile, bazal membranı kollajenazla deler.", "isKey": True},
                {"title": "Kemotaktik Pusula", "desc": "C5a, LTB4, IL-8 gradyanı aktin polimerizasyonuyla izlenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Akut enflamasyon gelişen bir dokuda lökositlerin damar lümeninden çıkarak bakterinin bulunduğu odağa ulaşmasında rol oynayan iki ardışık basamak olan 'Diapedez' ile 'Kemotaksi'nin temel moleküler yöneticilerini belirtiniz?",
                "Diapedez basamağını endotel ve lökositteki PECAM-1 (CD31) homofilik etkileşimi ile bazal membranı delen Tip IV kollajenaz yönetir; Kemotaksi basamağını ise kemoatraktanlar (bakteriyel formil peptitler, C5a, LTB4, IL-8) ve GPCR uyarımıyla tetiklenen hücre içi aktin polimerizasyonu yönetir."
            ),
            make_micro_quiz(
                "Lökosit transmigrasyonu (diapedez) sırasında lökositin endotel hücre kavşağından geçebilmesi için hem lökositte hem endotelde karşılıklı homofilik bağlanma yapan adezyon molekülü hangisidir?",
                {
                    "A": "PECAM-1 (CD31)",
                    "B": "ICAM-1 (CD54)",
                    "C": "VLA-4 (CD49d/CD29)",
                    "D": "P-selektin (CD62P)",
                    "E": "E-selektin (CD62E)"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: PECAM-1 (CD31) lökosit-endotel kavşağında homofilik bağlanarak transmigrasyonu sağlar.",
                    "B": "ICAM-1 sıkı adezyondadır.",
                    "C": "VLA-4 lökosit integrinidir.",
                    "D": "P-selektin yuvarlanmadadır.",
                    "E": "E-selektin yuvarlanmadadır."
                }
            ),
            make_cloze(
                "Chédiak-Higashi sendromunda periferik kan yaymasında nötrofillerin sitoplazmasında görülen ve hastalığın patognomonik morfolojik bulgusu olan yapılar dev lizozomal granüller yapılarıdır.",
                "dev lizozomal granüller",
                "Lizozomların kontrolsüz füzyonu sonucu oluşan devasa mikroskobik inklüzyonlar"
            )
        ]
    })

    # Slide 80
    slides.append({
        "slideNumber": 80,
        "title": "Bölüm 8 Entegrasyonu: Lökosit Göç Kusurlarının Ayırıcı Tanı Tablosu",
        "subtitle": "LAD-1, LAD-2 ve Chédiak-Higashi sendromlarının patolojik karşılaştırması",
        "badge": "Genetik Karşılaştırma",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Tıbbi patoloji ve pediatrik immünoloji sınavlarının vazgeçilmez konusu, lökosit göçünün üç büyük "
            "genetik hastalığının ayırıcı tanısıdır:\n\n"
            "1. **LAD-1 (Lökosit Adezyon Eksikliği Tip 1):**\n"
            "   - Defekt: **CD18 (beta-2 integrin)** geni.\n"
            "   - Bozulan Basamak: **Sıkı Adezyon (Firm Adhesion)**.\n"
            "   - Klinik: Göbek kordonu geç düşer, kanda masif lökositoz (100.000), yaralarda **irin (pus) yoktur**.\n\n"
            "2. **LAD-2 (Lökosit Adezyon Eksikliği Tip 2):**\n"
            "   - Defekt: GDP-fruktoz taşıyıcısı -> **Sialyl-Lewis X yokluğu**.\n"
            "   - Bozulan Basamak: **Yuvarlanma (Rolling)**.\n"
            "   - Klinik: Zeka geriliği, kısa boy, dismorfik yüz, Bombay kan grubu.\n\n"
            "3. **Chédiak-Higashi Sendromu:**\n"
            "   - Defekt: **LYST geni** (mikrotübül ve organel füzyon regülatörü).\n"
            "   - Bozulan Basamak: **Kemotaksi** ve **Fago-lizozom füzyonu**.\n"
            "   - Klinik: Nötrofillerde **dev lizozomlar**, parsiyel okülokutanöz albinizm, nöropati."
        ),
        "medicalTerms": [
            {"term": "Ayırıcı Tanı", "explanation": "Benzer klinik semptomlar gösteren hastalıkların patolojik ve moleküler testlerle birbirinden kesin olarak ayırt edilmesidir."},
            {"term": "Lökosit Fonksiyon Testi", "explanation": "Nötrofillerin adezyon, kemotaksi ve öldürme yeteneklerinin in vitro ölçülmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] LAD-1 = Adezyon bozuk (CD18); LAD-2 = Yuvarlanma bozuk (Sialyl-Lewis X); Chédiak-Higashi = Kemotaksi bozuk (LYST).",
            "📌 [SINAV SPOTU] Göbek kordonu geç düşüyorsa LAD-1, albinizm ve dev granül varsa Chédiak-Higashi düşünülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "LAD-1", "desc": "CD18 mutasyonu -> Sıkı adezyon yok -> İrinsiz yara.", "isKey": True},
                {"title": "LAD-2", "desc": "Sialyl-Lewis X yok -> Yuvarlanma yok -> Zeka geriliği.", "isKey": True},
                {"title": "Chédiak-Higashi", "desc": "LYST mutasyonu -> Bozuk kemotaksi -> Dev lizozomlar ve albinizm.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Genetik İmmün Hastalık", "Mutasyona Uğrayan Gen ve Molekül", "Kusurlu Ekstravazasyon Basamağı", "Ayırt Edici Majör Klinik Bulgu"],
                [
                    [("LAD-1", False, ""), ("ITGB2 geni; CD18 (Beta-2 İntegrin)", False, ""), ("Sıkı Adezyon (Firm Adhesion)", False, ""), ("Göbek kordonunun geç düşmesi, aşırı lökositoz, irinsiz yara", True, "Nötrofilin dokuya hiç çıkamaması tablosu")],
                    [("LAD-2", False, ""), ("SLC35C1 geni; Sialyl-Lewis X (CD15s)", False, ""), ("Yuvarlanma (Rolling)", False, ""), ("Mental retardasyon, kısa boy, Bombay kan grubu", True, "Fukozilasyon kusuruyla giden sendrom")],
                    [("Chédiak-Higashi", False, ""), ("LYST geni; Mikrotübül organel trafiği", False, ""), ("Kemotaksi ve Fago-lizozom Füzyonu", False, ""), ("Nötrofillerde dev granüller, parsiyel albinizm, nöropati", True, "Mikrotübül felcine bağlı lizozom birikimi")]
                ]
            ),
            make_cloze(
                "Lökosit göç bozuklukları içinde nötrofillerde dev lizozomal granüller ve parsiyel okülokutanöz albinizmle karakterize hastalık Chédiak-Higashi sendromudur.",
                "Chédiak-Higashi",
                "LYST mutasyonu ile giden otozomal resesif vezikül füzyon sendromu"
            )
        ]
    })

    return slides
