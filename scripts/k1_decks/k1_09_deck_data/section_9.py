"""
Akut Enflamasyon (Ders 9) - Bölüm 9: Fagositoz, Solunumsal Patlama, NET'ler ve CGD
Slayt 81 - 90 (Checkpoint 9: Slayt 89)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "slideNumber": 81,
        "title": "Fagositozun Üç Aşaması: Tanıma, Yutulma ve İntrasellüler İmha",
        "subtitle": "Savunma hücrelerinin mikroorganizmaları kucaklayıp fagozom içine hapsetmesi",
        "badge": "Fagositoz",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Dokuya ulaşan nötrofil ve makrofajların nihai varoluş amacı **Fagositozdur** (hücresel yeme). "
            "Bu süreç üç kusursuz ardışık basamakta tamamlanır:\n\n"
            "1. **Tanıma ve Bağlanma (Recognition and Attachment):** Mikroorganizma doğrudan PRR'lerle veya çok daha "
            "güçlü şekilde **Opsoninler** ile kaplanarak lökosit yüzeyindeki spesifik opsonin reseptörlerine bağlanır.\n\n"
            "2. **Yutulma (Engulfment):** Mikrop bağlandığı anda lökosit plazma zarından iki taraflı yalancı ayaklar "
            "(psödopodlar) uzanır. Psödopodlar mikrobun etrafını sararak uç uca birleşir. Mikrop, plazma zarından "
            "kopan bir kesecik olan **Fagozom** içine hapsedilir.\n\n"
            "3. **Öldürme ve Yıkım (Killing and Degradation):** Fagozom, sitoplazmadaki lizozomlarla kaynaşarak "
            "**Fago-lizozomu** oluşturur. Serbest radikaller ve litik enzimler mikroorganizmayı dakikalar içinde parçalar."
        ),
        "medicalTerms": [
            {"term": "Fagositoz", "explanation": "Nötrofil ve makrofajların 0.5 mikrometreden büyük mikropları ve partikülleri yutarak sindirmesidir."},
            {"term": "Fagozom", "explanation": "Yutulan mikrobun hücre içinde plazma zarı kökenli bir lipid kesecik içine alınmış halidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fagositozun 3 basamağı: 1) Tanıma/Bağlanma, 2) Yutulma (fagozom), 3) Öldürme/Yıkım (fago-lizozom).",
            "📌 [SINAV SPOTU] Yutulma basamağı aktin iskeletinin polimerizasyonu ile yürütülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. Tanıma", "desc": "Opsoninler mikrobu kaplar ve lökosit reseptörüne kilitler.", "isKey": True},
                {"title": "2. Yutulma", "desc": "Psödopodlar birleşerek mikrobu fagozom içine hapseder.", "isKey": True},
                {"title": "3. İmha", "desc": "Lizozom füzyonu ve solunumsal patlama ile sindirim tamamlanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Fagositozun Mekanik İlerleyiş Zinciri",
                [
                    "1. Bakteri yüzeyindeki antijenler IgG veya C3b opsoninleriyle kaplanır",
                    "2. Nötrofil yüzeyindeki Fc-gamma ve CR1 reseptörleri opsoninlere sıkıca bağlanır",
                    "3. Aktin polimerizasyonuyla uzayan psödopodlar bakteriyi çepeçevre sarar",
                    "4. Membranlar birleşerek bakteriyi hücre içinde fagozom keseciğine hapseder",
                    "5. Lizozomlar fagozomla füzyona uğrayarak mikrobisidal enzimleri ve radikalleri ortama boşaltır"
                ]
            ),
            make_cloze(
                "Fagositoz sırasında lökosit psödopodlarının birleşmesiyle mikroorganizmanın hücre içinde hapsedildiği zarla çevrili veziküle fagozom adı verilir.",
                "fagozom",
                "Lizozom ile birleşerek sindirim odacığını kuran fagositer kesecik"
            )
        ]
    })

    # Slide 82
    slides.append({
        "slideNumber": 82,
        "title": "Opsonizasyon: Hedefi İşaretleyen Moleküler Soslar",
        "subtitle": "IgG Fc parçası, Kompleman C3b ve Mannoz Bağlayıcı Lektin (MBL) mucizesi",
        "badge": "Opsoninler",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Nötrofil ve makrofajlar çıplak bakterileri tanımakta zorlanabilir; özellikle kapsüllü bakteriler "
            "(örneğin Streptococcus pneumoniae) kaygan polisakkarit kılıflarıyla fagositozdan kaçarlar.\n\n"
            "İmmün sistem bu sorunu **Opsonizasyon** (Yunanca 'yemeğe lezzet katmak / soslamak') ile çözer:\n\n"
            "En önemli üç opsonin:\n"
            "1. **İmmünglobülin G (Özellikle IgG1 ve IgG3):** Antikorun Fab ucu bakteriye bağlanırken, dışarı bakan "
            "**Fc parçası** nötrofil ve makrofajın en güçlü reseptörü olan **FcγRI'e (CD64)** kilitlenir. Fagositozu "
            "yüzlerce kat hızlandırır.\n\n"
            "2. **Kompleman C3b ve iC3b Fragmanları:** Kompleman kaskadı aktive olduğunda C3b bakteriyi zift gibi kaplar. "
            "Lökositlerdeki **Kompleman Reseptörü 1 (CR1 / CD35)** ve **Mac-1 (CR3 / CD11b/CD18)** C3b'yi tanır.\n\n"
            "3. **Plazma Lektinleri (MBL ve Fibrinojen):** Bakteriyel karbonhidratları sararak fagositozu kolaylaştırır."
        ),
        "medicalTerms": [
            {"term": "Opsonin", "explanation": "Mikroorganizma yüzeyini kaplayarak fagositer hücrelerin reseptörlerine bağlanmasını ve yutulmasını dramatik hızlandıran moleküldür."},
            {"term": "FcγRI (CD64)", "explanation": "Makrofaj ve nötrofillerde bulunan, IgG ile kaplı patojenleri en yüksek afiniteyle bağlayan opsonin reseptörüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] En güçlü iki opsonin: IgG (Fc parçası) ve Kompleman C3b'dir.",
            "📌 [SINAV SPOTU] IgG'yi bağlayan lökosit reseptörü FcγRI (CD64); C3b'yi bağlayan reseptör ise CR1 ve Mac-1'dir (CR3).",
            "📌 [SINAV SPOTU] Kapsüllü bakterilerin öldürülmesi mutlak opsonizasyon bağımlıdır (dalağın önemi)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Opsonin Çifti", "desc": "IgG antikoru ve Kompleman C3b başroldedir.", "isKey": True},
                {"title": "Reseptör Uyumu", "desc": "FcγRI ve CR1 ile mikrop yutulmak üzere kilitlenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Opsonin Molekülü", "Bağlandığı Lökosit Yüzey Reseptörü", "Fagositozdaki Kritik Önemi"],
                [
                    [("İmmünglobülin G (IgG)", False, ""), ("Fc-gama Reseptör I (FcγRI / CD64)", False, ""), ("Kapsüllü bakterileri nötralize edip yutulmayı yüz kat artırır", True, "Antikor bağımlı opsonizasyonun anahtarı")],
                    [("Kompleman C3b / iC3b", False, ""), ("Kompleman Reseptörü 1 (CR1 / CD35) ve Mac-1", False, ""), ("Doğal immünitenin mikrop yüzeyini işaretleyen kovalent etiketi", True, "Alternatif ve lektin yolağı ile kaplama")],
                    [("Mannoz Bağlayıcı Lektin (MBL)", False, ""), ("C-tipi lektin reseptörleri", False, ""), ("Mikrop yüzeyindeki mannoz dizilerini bağlayarak yutmayı tetikler", True, "Hümoral lektin ailesi opsonini")]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi nötrofillerin ve makrofajların fagositoz yeteneğini dramatik olarak artıran en güçlü iki primer opsonin molekülüdür?",
                {
                    "A": "İmmünglobülin G (IgG) ve Kompleman C3b",
                    "B": "Histamin ve Serotonin",
                    "C": "İnterlökin-1 ve TNF-alfa",
                    "D": "Bradikinin ve Prostaglandin E2",
                    "E": "Nitrik Oksit ve Heparin"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: IgG (Fc kısmı) ve kompleman parçası C3b/iC3b vücudun en güçlü opsoninleridir.",
                    "B": "Histamin vazodilatatördür.",
                    "C": "IL-1 ve TNF sitokindir, opsonin değildir.",
                    "D": "Bradikinin ağrı yapar.",
                    "E": "Heparin antikoagülandır."
                }
            )
        ]
    })

    # Slide 83
    slides.append({
        "slideNumber": 83,
        "title": "Solunumsal Patlama (Respiratory Burst) ve NADPH Oksidaz",
        "subtitle": "Oksijen tüketiminde dev sıçrama ve süperoksit radikalinin üretilmesi",
        "badge": "Oksidatif Patlama",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fagositoz başladığı anda nötrofilin oksijen tüketimi aniden 10 ila 20 kat fırlar; bu olağanüstü metabolik "
            "patlamaya **Solunumsal Patlama (Respiratory Burst)** denir.\n\n"
            "- Bu oksijen ATP üretmek için değil; mikrobu öldürecek ölümcül **Reaktif Oksijen Türlerini (ROS)** "
            "sentezlemek için kullanılır.\n\n"
            "> **Enzimatik Mimari - NADPH Oksidaz Kompleksi:**\n"
            "- Çok alt birimli dev bir enzimdir (phox = phagocyte oxidase).\n"
            "- İstirahat halindeki nötrofilde enzimin iki alt birimi (**gp91phox ve p22phox**) fagozom zarında beklerken; "
            "diğer alt birimler (**p47phox, p67phox, p40phox ve Rac**) sitoplazmada dağınık durur.\n"
            "- Fagositoz uyarısıyla sitoplazmik parçalar fagozom zarına göç eder ve **aktif holoenzim monte edilir**.\n"
            "- NADPH oksidaz, sitozoldeki NADPH'tan iki elektronu fagozom lümenindeki moleküler oksijene (O2) aktarır:\n"
            "  $$\\text{NADPH} + 2\\text{O}_2 \\xrightarrow{\\text{NADPH Oksidaz}} \\text{NADP}^+ + \\text{H}^+ + 2\\text{O}_2^{\\bullet -}$$\n"
            "- Böylece fagozom içine ilk reaktif serbest radikal olan **Süperoksit anyonu ($O_2^{\\bullet -}$)** fışkırır."
        ),
        "medicalTerms": [
            {"term": "Solunumsal Patlama", "explanation": "Fagositoz anında mikrobisidal oksijen radikalleri üretmek amacıyla lökositin oksijen tüketiminde görülen masif artıştır."},
            {"term": "NADPH Oksidaz (Phox)", "explanation": "Moleküler oksijeni süperoksit anyonuna indirgeyen çok alt birimli membranöz enzim kompleksidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Solunumsal patlamanın ilk basamağını yürüten anahtar enzim NADPH OKSİDAZ'dır.",
            "📌 [SINAV SPOTU] NADPH oksidazın ilk ürettiği reaktif oksijen radikali SÜPEROKSİT ANYONU'dur ($O_2^{\\bullet -}$).",
            "📌 [SINAV SPOTU] Enzimin en önemli transmembran katalitik alt birimi gp91phox'tur (CYBB geni)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "O2 Tüketim Sıçraması", "desc": "Dakikalar içinde oksijen radikali üretimi başlar.", "isKey": True},
                {"title": "gp91phox Çekirdeği", "desc": "Sitoplazmik ve membran alt birimleri birleşerek süperoksit üretir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Solunumsal Patlamanın İlk Fazı",
                [
                    "1. Fagositer uyarım alan nötrofilde sitoplazmik p47phox ve p67phox alt birimleri fosforillenir",
                    "2. Sitoplazmik parçalar fagozom zarına göç ederek membranöz gp91phox ile birleşir",
                    "3. Aktifleşen NADPH oksidaz sitozolik NADPH'tan bir elektron koparır",
                    "4. Elektron fagozom lümenindeki moleküler oksijene aktarılarak süperoksit anyonu (O2.-) üretilir"
                ]
            ),
            make_cloze(
                "Lökositlerde fagositoz sırasında solunumsal patlamayı başlatarak moleküler oksijenden süperoksit radikali üreten enzim NADPH oksidaz enzimidir.",
                "NADPH oksidaz",
                "Fagosit oksidaz (phox) kompleksinin temel biyokimyasal adı"
            )
        ]
    })

    # Slide 84
    slides.append({
        "slideNumber": 84,
        "title": "Miyeloperoksidaz (MPO) ve Hipokloröz Asit: Hücresel Çamaşır Suyu",
        "subtitle": "H2O2 ve klorürden HOCl üretimi: Nötrofillerin en güçlü ve ölümcül mikrobisidal silahı",
        "badge": "MPO Sistemi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Süperoksit anyonu üretildikten sonra nötrofilin kimyasal cephanesinde asıl ölümcül silah kurulur:\n\n"
            "1. **Süperoksit Dismutaz (SOD):** Fagozomdaki süperoksit radikallerini hızla **Hidrojen Peroksite (H2O2)** "
            "dönüştürür:\n"
            "   $$2\\text{O}_2^{\\bullet -} + 2\\text{H}^+ \\xrightarrow{\\text{SOD}} \\text{H}_2\\text{O}_2 + \\text{O}_2$$\n\n"
            "2. **Miyeloperoksidaz (MPO) Enzimi:**\n"
            "- Nötrofillerin **primer (azurofilik) granüllerinde** devasa konsantrasyonlarda depolanır.\n"
            "- Fago-lizozom birleştiğinde granüldeki MPO lümene dökülür.\n"
            "- MPO, hidrojen peroksiti fizyolojik plazma **Klorür (Cl-)** iyonu ile reaksiyona sokar:\n"
            "   $$\\text{H}_2\\text{O}_2 + \\text{Cl}^- \\xrightarrow{\\text{MPO}} \\text{HOCl} + \\text{H}_2\\text{O}$$\n\n"
            "> **Sonuç - Hipokloröz Asit (HOCl):**\n"
            "HOCl, evlerimizde dezenfektan olarak kullandığımız **çamaşır suyunun (hipoklorit)** aktif etken maddesidir! "
            "Bakteriyel proteinleri klorlayıp oksitleyerek, lipid membranları parçalayarak mikroorganizmaları milisaniyeler "
            "içinde yok eder. Bu sistem **nötrofillerin sahip olduğu en güçlü bakterisidal mekanizmadır**."
        ),
        "medicalTerms": [
            {"term": "Miyeloperoksidaz (MPO)", "explanation": "Nötrofil azurofilik granüllerinde bulunan, yeşil renkli ve H2O2 ile klorürden HOCl üreten demir içeren enzimdir."},
            {"term": "Hipokloröz Asit (HOCl)", "explanation": "Nötrofillerin MPO-H2O2-Halid sistemiyle ürettiği ve çamaşır suyu etkisiyle mikropları öldüren en güçlü biyolojik radikaldir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nötrofillerin EN GÜÇLÜ mikrobisidal mekanizması: MPO - H2O2 - Halid (Klorür) sistemidir.",
            "📌 [SINAV SPOTU] MPO azurofilik (primer) granüllerde bulunur ve cerahate karakteristik yeşilimsi rengi verir.",
            "📌 [SINAV SPOTU] Üretilen nihai öldürücü molekül Hipokloröz Asittir (HOCl)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "SOD ve MPO", "desc": "Süperoksit -> H2O2 -> HOCl zincirleme kaskadı.", "isKey": True},
                {"title": "Çamaşır Suyu Etkisi", "desc": "HOCl bakterileri saniyeler içinde lize eden en güçlü ajandır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "O2'den Hipokloröz Asite Uzanan Bakterisidal Yol",
                [
                    "1. NADPH oksidaz moleküler oksijenden süperoksit anyonu üretir",
                    "2. Süperoksit dismutaz (SOD) süperoksiti hidrojen peroksite (H2O2) çevirir",
                    "3. Azurofilik granüllerden ortama bol miktarda Miyeloperoksidaz (MPO) dökülür",
                    "4. MPO, H2O2 ile klorür iyonunu (Cl-) birleştirerek hipokloröz asit (HOCl) sentezler",
                    "5. Hipokloröz asit bakteriyel hücre duvarını ve proteinlerini klorlayıp mikrobu imha eder"
                ]
            ),
            make_cloze(
                "Nötrofillerin azurofilik granüllerinde bulunan ve hidrojen peroksiti klorür ile birleştirerek güçlü hipokloröz asit (HOCl) üreten enzim miyeloperoksidaz enzimidir.",
                "miyeloperoksidaz",
                "İrin ve balgama yeşilimsi rengini veren demirli fagositik enzim"
            )
        ]
    })

    # Slide 85
    slides.append({
        "slideNumber": 85,
        "title": "Kronik Granülomatöz Hastalık (KGH / CGD): NADPH Oksidaz İflası",
        "subtitle": "Katalaz-pozitif mikroplarla tekrarlayan granülomlar, NBT testi ve DHR akım sitometrisi",
        "badge": "Genetik Mikrobisidal Kusur",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fagositoz biyolojisinin en ünlü hastalık modeli **Kronik Granülomatöz Hastalıktır (KGH / CGD)**:\n\n"
            "- **Genetik Kusur:** Olguların %70'i **X'e bağlı resesif** (gp91phox / CYBB gen mutasyonu), %30'u otozomal "
            "resesiftir (p47phox vb.).\n"
            "- **Moleküler Bozukluk:** **NADPH Oksidaz enzimi çalışmaz**. Nötrofil bakteriyi tanır, yutar, fagozom yapar; "
            "ancak **solunumsal patlama yapamaz ve H2O2 / HOCl üretemez**.\n\n"
            "> **Neden Sadece Katalaz-Pozitif Mikroplar? (Klasik Sınav Sorusu):**\n"
            "- Bakteriler metabolizmaları sırasında kendileri de az miktarda H2O2 üretirler.\n"
            "- **Katalaz-Negatif mikroplar (örneğin Streptokoklar):** Kendi ürettikleri H2O2'yi yok edemezler. Nötrofil, "
            "bakterinin bu kendi H2O2'sini çalar, MPO ile HOCl yapar ve bakteriyi kendi silahıyla öldürür!\n"
            "- **Katalaz-Pozitif mikroplar (Staphylococcus aureus, Aspergillus, Serratia marcescens, Burkholderia cepacia, Nocardia):** "
            "Kendi H2O2'lerini kendi katalaz enzimiyle anında yıkarak parçalarlar. Nötrofilde de H2O2 olmadığı için bu "
            "bakteriler **asla öldürülemez**; dokuda canlı kalıp kronik granülomatöz apselere yol açarlar."
        ),
        "medicalTerms": [
            {"term": "Kronik Granülomatöz Hastalık (CGD)", "explanation": "NADPH oksidaz gen mutasyonu sonucu lökositlerin serbest radikal üretemediği ve tekrarlayan granülomlarla seyreden immün yetmezliktir."},
            {"term": "Katalaz-Pozitif Bakteri", "explanation": "H2O2'yi su ve oksijene parçalayarak CGD'li hastaların nötrofillerinden kaçabilen mikroorganizmalardır (S. aureus vb.)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] CGD'de mutasyon NADPH OKSİDAZ kompleksindedir (en sık X'e bağlı gp91phox).",
            "📌 [SINAV SPOTU] CGD hastaları sadece KATALAZ-POZİTİF mikroplarla (Staph aureus, Aspergillus, Serratia, Burkholderia, Nocardia) hastalanır.",
            "📌 [SINAV SPOTU] Tanı: DHR (Dihidrorodamin) akım sitometrisi floresan vermez; NBT (Nitroblue Tetrazolium) boyanmaz (renksiz kalır)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "NADPH Oksidaz Yok", "desc": "Süperoksit ve hidrojen peroksit üretilemez.", "isKey": True},
                {"title": "Katalaz Tuzağı", "desc": "Katalaz-pozitif mikroplar kendi H2O2'sini yıktığı için öldürülemez.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Tekrarlayan Staphylococcus aureus karaciğer apseleri ve Aspergillus pnömonisi geçiren 4 yaşındaki bir erkek çocuğun nötrofillerinde Dihidrorodamin (DHR) akım sitometri testinde floresan artışı saptanamıyor (negatif). Bu hastadaki temel moleküler bozukluk nedir?",
                [
                    {"text": "NADPH oksidaz kompleksinin (gp91phox) genetik defekti nedeniyle solunumsal patlama ve serbest oksijen radikali üretiminin olmaması (Kronik Granülomatöz Hastalık)", "isCorrect": True, "feedback": "Kusursuz tıp muhakemesi! DHR negatifliği ve katalaz-pozitif mikroplarla apseler KGH'nin patognomonik tablosudur."},
                    {"text": "Miyeloperoksidaz (MPO) enziminin primer granüllerde depolanamaması", "isCorrect": False, "feedback": "MPO eksikliğinde DHR testi normaldir (H2O2 üretilir)."},
                    {"text": "CD18 eksikliğine bağlı lökosit adezyon defekti", "isCorrect": False, "feedback": "LAD-1'de radikal üretimi normaldir, dokuya göç bozuktur."}
                ]
            ),
            make_cloze(
                "Kronik Granülomatöz Hastalıkta (CGD) lökositlerin serbest oksijen radikali ve H2O2 üretememesinden sorumlu mutant enzim kompleksi NADPH oksidaz kompleksidir.",
                "NADPH oksidaz",
                "Phox alt birimlerinden oluşan solunumsal patlama enzimi"
            )
        ]
    })

    # Slide 86
    slides.append({
        "slideNumber": 86,
        "title": "Miyeloperoksidaz Eksikliği vs CGD: Ayırıcı Tanı İncelemeleri",
        "subtitle": "Neden MPO eksikliği çoğunlukla asemptomatiktir ve NBT testi neden pozitiftir?",
        "badge": "Enzim Karşılaştırması",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Patoloji ve immünolojide sık karıştırılan iki oksidatif kusurun klinik ve laboratuvar ayrımı "
            "hayret verici bir fizyopatolojik ders sunar:\n\n"
            "- **Miyeloperoksidaz (MPO) Eksikliği:**\n"
            "  * Toplumda oldukça sıktır (1/2000).\n"
            "  * Bireylerin ezici çoğunluğu **tamamen asemptomatiktir** ve normal bir ömür sürer.\n"
            "  * Bunun nedeni, NADPH oksidazın tıkır tıkır çalışarak **süperoksit ve H2O2 üretmeye devam etmesidir**.\n"
            "  * H2O2 tek başına da mikropları (HOCl kadar hızlı olmasa da) öldürebilir; ayrıca lökositlerin diğer oksijensiz "
            "silahları devreye girer.\n"
            "  * Yalnızca diyabetik bireylerde **Candida albicans** gibi fırsatçı mantar enfeksiyonlarına hafif yatkınlık görülür.\n\n"
            "> **Tanısal Test Farkı (NBT ve DHR):**\n"
            "- **KGH / CGD:** NADPH oksidaz olmadığı için **H2O2 üretilemez**. NBT sarı kalır (renk değişmez), DHR ışıma yapmaz (**Negatif**).\n"
            "- **MPO Eksikliği:** NADPH oksidaz sağlamdır; **bolca H2O2 üretilir**. Bu nedenle NBT maviye boyanır, "
            "DHR akım sitometrisi parlar (**POZİTİF / Normal**)."
        ),
        "medicalTerms": [
            {"term": "NBT Testi (Nitroblue Tetrazolium)", "explanation": "Fagositozda üretilen süperoksit radikaliyle sarı boyanın çözünmeyen koyu mavi formazan kristaline dönüştüğü klasik laboratuvar testidir."},
            {"term": "DHR Testi (Dihidrorodamin)", "explanation": "H2O2 varlığında floresan veren ve CGD tanısında NBT'nin yerini alan modern akım sitometri testidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] MPO eksikliğinde NBT ve DHR testleri POZİTİF (normal) çıkar; çünkü NADPH oksidaz ve H2O2 sağlamdır.",
            "📌 [SINAV SPOTU] CGD ağır ve ölümcül apseler yaparken, MPO eksikliği çoğunlukla klinik olarak asemptomatiktir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "MPO Asemptomatik", "desc": "H2O2 tek başına bakterileri öldürmeye yeterlidir.", "isKey": True},
                {"title": "Test Farkı", "desc": "CGD'de DHR/NBT negatif, MPO eksikliğinde pozitiftir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Özellik / Parametre", "Kronik Granülomatöz Hastalık (CGD)", "Miyeloperoksidaz (MPO) Eksikliği"],
                [
                    [("Defektif Enzim", False, ""), ("NADPH Oksidaz kompleksi (gp91phox)", False, ""), ("Miyeloperoksidaz (MPO)", True, "Azurofilik granüldeki klorlayıcı enzim")],
                    [("Süperoksit ve H2O2 Üretimi", False, ""), ("Tamamen Sıfır (Yoktur)", False, ""), ("Normal veya Artmış (Mevcuttur)", True, "Oksidatif radikal üretim basamağı")],
                    [("Hipokloröz Asit (HOCl) Üretimi", False, ""), ("Sıfır", False, ""), ("Sıfır", True, "Her iki hastalıkta da üretilemeyen son ürün")],
                    [("DHR / NBT Laboratuvar Testi", False, ""), ("Negatif (Boya indirgenemez)", False, ""), ("Pozitif (Normal, maviye boyanır)", True, "Ayırıcı tanıda kullanılan en kritik laboratuvar testi")],
                    [("Klinik Seyir ve Şiddet", False, ""), ("Katalaz (+) mikroplarla ağır letal apseler", False, ""), ("Çoğunlukla tamamen asemptomatik, hafif Candida", True, "Hastalığın prognoz ve klinik tablosu")]
                ]
            ),
            make_cloze(
                "Miyeloperoksidaz eksikliğinde Kronik Granülomatöz Hastalığın aksine NBT ve DHR testlerinin normal çıkmasının nedeni NADPH oksidaz enziminin sağlam olmasıdır.",
                "NADPH oksidaz",
                "H2O2 üretimini aksatmadan yürüten ilk basamak enzimi"
            )
        ]
    })

    # Slide 87
    slides.append({
        "slideNumber": 87,
        "title": "Oksijenden Bağımsız Öldürme Mekanizmaları ve Lizozomal Enzimler",
        "subtitle": "Defensinler, Lizozim, Laktoferrin ve Bakterisidal Permeabilite Artıran Protein (BPI)",
        "badge": "Alternatif Cephane",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Lökositler sadece serbest oksijen radikalleriyle değil; oksijensiz ortamlarda da mikropları imha edebilen "
            "zengin bir **oksijenden bağımsız biyokimyasal cephaneye** sahiptir:\n\n"
            "1. **Bakterisidal Permeabilite Artıran Protein (BPI):** Gram-negatif bakterilerin dış zarındaki LPS'ye "
            "bağlanarak zarda gözenekler açar ve bakteriyi lize eder.\n\n"
            "2. **Defensinler:** Nötrofil granüllerinde bulunan katyonik arjinin zengini peptitlerdir; mikrop membranında "
            "biyofiziksel delikler açarak iyon dengesini bozar.\n\n"
            "3. **Lizozim (Muramidaz):** Bakteri hücre duvarındaki peptidoglikanın glikozidik bağlarını hidrolize ederek "
            "özellikle Gram-pozitif bakterilerin çeperini parçalar.\n\n"
            "4. **Laktoferrin:** Serbest demiri ($Fe^{3+}$) şelatlayarak bağlar; mikropların çoğalmak için muhtaç olduğu "
            "demiri ortamdan çalarak bakterileri açlıktan öldürür (bakteriyostatik etki).\n\n"
            "5. **Majör Basic Protein (MBP):** Eozinofillerin kristaloid granüllerinde bulunur ve parazit kütikulasını eritir."
        ),
        "medicalTerms": [
            {"term": "Defensin", "explanation": "Mikrobiyal hücre membranlarını delerek öldüren küçük katyonik antimikrobiyal peptitlerdir."},
            {"term": "Laktoferrin", "explanation": "Nötrofil spesifik granüllerinde bulunan ve demiri bağlayarak bakteriyel üremeyi durduran glikoproteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Laktoferrin demiri bağlayarak bakterilerin çoğalmasını engeller.",
            "📌 [SINAV SPOTU] Lizozim peptidoglikan bağlarını hidrolize eder.",
            "📌 [SINAV SPOTU] Majör basic protein eozinofillerin granülünde yer alır ve helmintleri öldürür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "BPI ve Defensin", "desc": "Membranda porlar açarak mikrop duvarını parçalar.", "isKey": True},
                {"title": "Laktoferrin", "desc": "Demiri şelatlayarak bakteriyi besinsiz bırakır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Antimikrobiyal Madde", "Bulunduğu Granül / Hücre", "Bakterisidal Etki Mekanizması"],
                [
                    [("BPI (Bakterisidal Protein)", False, ""), ("Nötrofil Azurofilik Granülleri", False, ""), ("Gram-negatif LPS'ye bağlanarak dış zarı deler", True, "Endotoksini nötralize eden lizozomal ajan")],
                    [("Lizozim (Muramidaz)", False, ""), ("Nötrofil Granülleri ve Makrofajlar", False, ""), ("Bakteriyel peptidoglikan omurgasını enzimatik parçalar", True, "Gram-pozitif çeperini eriten enzim")],
                    [("Laktoferrin", False, ""), ("Nötrofil Spesifik (Sekonder) Granülleri", False, ""), ("Demiri şelatlayıp bağlayarak mikrobu aç bırakır", True, "Mikrobiyal demir metabolizmasını felç eden protein")],
                    [("Majör Basic Protein (MBP)", False, ""), ("Eozinofil Kristaloid Granülleri", False, ""), ("Parazit helmintlerin kütikulasına toksik hasar verir", True, "Eozinofillerin en güçlü antiparaziter silahı")]
                ]
            ),
            make_cloze(
                "Nötrofillerin sekonder granüllerinde bulunan ve ortamdaki serbest demiri bağlayarak bakterilerin çoğalmasını engelleyen protein laktoferrin proteinidir.",
                "laktoferrin",
                "Demir şelasyonu yaparak bakteriyostatik etki gösteren granül proteini"
            )
        ]
    })

    # Slide 88
    slides.append({
        "slideNumber": 88,
        "title": "Nötrofil Ekstrasellüler Tuzakları (NET'ler) ve NETosis",
        "subtitle": "Kendi DNA'sını fırlatan nötrofil intiharı: Mikropları yakalayan yapışkan kromatin ağı",
        "badge": "NETosis",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "2004 yılında keşfedilen ve tıp dünyasını sarsan en dramatik nötrofil öldürme mekanizması "
            "**Nötrofil Ekstrasellüler Tuzaklarıdır (NETs / Neutrophil Extracellular Traps)**:\n\n"
            "- Bazı mikroplar (örneğin mantar hifleri veya büyük bakteri kümeleri) nötrofilin fagositozla yutamayacağı "
            "kadar büyüktür.\n"
            "- Bu durumda nötrofil benzersiz bir programlı hücre ölümüne girer: **NETosis**.\n\n"
            "> **NET Mekanizması:**\n"
            "1. **PAD4 (Peptidilarjinin Deiminaz 4)** enzimi histonları sitrülinleştirir; nükleer kromatin yoğunluğunu kaybedip çözülür.\n"
            "2. Nükleer membran parçalanır; çözülmüş kromatin sitoplazmadaki granül enzimleri (**MPO, nötrofil elastazı, "
            "katepsin G**) ile harmanlanır.\n"
            "3. Plazma zarı yırtılır ve nötrofil **kendi DNA ve histon ağını hücre dışına fırlatır**.\n"
            "- Ekstrasellüler alana saçılan bu yapışkan ağ, mikropları fiziksel olarak hapseder ve üzerindeki yüksek "
            "konsantrasyonlu antimikrobiyal enzimlerle öldürür.\n\n"
            "> **Karanlık Taraf:** NET'ler otoantijen kaynağıdır (**Lupus/SLE** patogenezi) ve damar içinde pıhtılaşmayı "
            "tetikleyerek **tromboza** (immünotromboz) yol açar."
        ),
        "medicalTerms": [
            {"term": "NETosis", "explanation": "Nötrofilin nükleer kromatinini antimikrobiyal granül proteinleriyle birlikte hücre dışına fırlatarak öldüğü özel hücre ölümüdür."},
            {"term": "PAD4", "explanation": "Histonları sitrülinleştirerek kromatinin gevşemesini ve NET oluşumunu sağlayan kritik enzimdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] NET'ler nötrofil DNA'sı, histonlar ve granül enzimlerinin (MPO, elastaz) ekstrasellüler ağıdır.",
            "📌 [SINAV SPOTU] NETosis nükleer kromatinin açılmasıyla olur; PAD4 enzimi histon sitrülinasyonu yapar.",
            "📌 [SINAV SPOTU] NET'ler sistemik lupus eritematozus (SLE) patogenezinde ve venöz trombozda rol oynar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "DNA Ağı", "desc": "Nötrofil kendi kromatinini fırlatarak mikropları hapseder.", "isKey": True},
                {"title": "Patolojik Rol", "desc": "Lupus otoantijenleri ve damar içi trombozu tetikler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Klasik Fagositoz vs NETosis ile Öldürme",
                "Klasik Fagositoz",
                "Mikrop hücre içine (fagozoma) alınır, nötrofil sağlam kalır veya apoptoza gider, sindirim içeride biter.",
                "NETosis (Ekstrasellüler Tuzak)",
                "Nötrofil zarı yırtılır, kendi DNA ve enzim ağını dışarı kusar, yutulamayacak büyüklükteki mikroplar dışarıda avlanır."
            ),
            make_cloze(
                "Nötrofil ekstrasellüler tuzaklarının (NET) oluşumunda nükleer kromatinin gevşemesini histonları sitrülinleştirerek sağlayan anahtar enzim PAD4 enzimidir.",
                "PAD4",
                "Peptidylarginine deiminase 4 enziminin kısaltması"
            )
        ]
    })

    # Slide 89 (CHECKPOINT 9)
    slides.append({
        "slideNumber": 89,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Fagositoz, Oksidatif Patlama ve NETosis",
        "subtitle": "Bölüm 9 Opsoninler, NADPH Oksidaz, MPO, CGD Ayrımı ve Antimikrobiyal Cephane",
        "badge": "Checkpoint 9",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Dokuzuncu kontrol noktasında lökositlerin mikrobisidal cephanesini sabitliyoruz:\n\n"
            "1. **Fagositoz:** Tanıma/Bağlanma -> Yutulma (fagozom) -> Öldürme (fago-lizozom).\n"
            "2. **Opsoninler:** **IgG (FcγRI / CD64)** ve **Kompleman C3b (CR1 ve Mac-1)** en güçlüleridir.\n"
            "3. **Solunumsal Patlama:**\n"
            "   - **NADPH Oksidaz:** $O_2 \\rightarrow O_2^{\\bullet -}$ (Süperoksit anyonu).\n"
            "   - **SOD:** $O_2^{\\bullet -} \\rightarrow H_2O_2$ (Hidrojen peroksit).\n"
            "   - **Miyeloperoksidaz (MPO):** $H_2O_2 + Cl^- \\rightarrow \\mathbf{HOCl}$ (Hipokloröz asit / Çamaşır suyu; en güçlü ajan).\n"
            "4. **KGH / CGD:** NADPH oksidaz mutasyonu -> $H_2O_2$ yok -> Katalaz (+) mikroplarla (S. aureus, Aspergillus) "
            "tekrarlayan apseler. **DHR ve NBT testleri negatif**.\n"
            "5. **MPO Eksikliği:** Çoğu asemptomatik; $H_2O_2$ sağlam olduğu için **DHR ve NBT pozitif (normal)**.\n"
            "6. **Oksijensiz Silahlar:** BPI (LPS deler), Lizozim (peptidoglikan yıkar), Laktoferrin (demir çalar), Defensin (membran deler).\n"
            "7. **NETosis:** PAD4 ile kromatin fırlatma; mikropları yakalar, tromboz ve otoimmüniteyi (SLE) körükler."
        ),
        "medicalTerms": [
            {"term": "Bakterisidal Kaskad", "explanation": "Oksijenin alınıp sırasıyla süperoksit, hidrojen peroksit ve hipokloröz asite dönüştürüldüğü öldürücü zincirdir."},
            {"term": "İmmünotromboz", "explanation": "NET'lerin ve doku faktörünün koagülasyonu aktive ederek damar içinde koruyucu veya patolojik pıhtı oluşturmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] En güçlü opsoninler: IgG ve C3b.",
            "📌 [SINAV SPOTU] En güçlü mikrobisidal ajan: MPO kaynaklı HOCl (hipokloröz asit).",
            "📌 [SINAV SPOTU] CGD = NADPH oksidaz kusuru (DHR negatif); MPO eksikliği = MPO kusuru (DHR pozitif).",
            "📌 [SINAV SPOTU] Laktoferrin demir bağlar, defensin membran deler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Oksijenli Öldürme", "desc": "NADPH oksidaz -> Süperoksit -> MPO -> HOCl (çamaşır suyu).", "isKey": True},
                {"title": "Klinik Kusurlar", "desc": "CGD (DHR negatif/ağır apse) vs MPO eksikliği (DHR pozitif/hafif).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Nötrofillerin oksijene bağımlı intrasellüler öldürme kaskadında yer alan üç enzimi ve bu enzimlerin ürettikleri reaktif molekülleri sırasıyla belirtiniz?",
                "1) NADPH Oksidaz: Moleküler oksijenden Süperoksit anyonu ($O_2^{\\bullet -}$) üretir; 2) Süperoksit Dismutaz (SOD): Süperoksitten Hidrojen Peroksit ($H_2O_2$) üretir; 3) Miyeloperoksidaz (MPO): $H_2O_2$ ve klorürden Hipokloröz Asit (HOCl) üretir."
            ),
            make_micro_quiz(
                "Kronik Granülomatöz Hastalığı (CGD) olan çocuklarda en sık hayatı tehdit eden enfeksiyonlara ve apselere yol açan, kendi ürettiği hidrojen peroksiti yıkarak nötrofil savunmasından kaçan mikroorganizma grubu hangisidir?",
                {
                    "A": "Katalaz-pozitif mikroorganizmalar (Staphylococcus aureus vb.)",
                    "B": "Katalaz-negatif mikroorganizmalar (Streptococcus pneumoniae vb.)",
                    "C": "Zorunlu anaerop sporlu basiller",
                    "D": "DNA virüsleri",
                    "E": "Prion partikülleri"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Katalaz-pozitif mikroplar kendi H2O2'lerini yıkar; CGD hastasının lökositinde de H2O2 olmadığı için öldürülemezler.",
                    "B": "Katalaz-negatif mikropların ürettiği H2O2'yi MPO kullanarak bakteriyi öldürür.",
                    "C": "Anaeroplar fagositozda birinci hedef değildir.",
                    "D": "Virüsler intrasellüler lenfositlerle kontrol edilir.",
                    "E": "Prionlar enfeksiyöz proteinlerdir."
                }
            ),
            make_cloze(
                "Nötrofillerin fagositozla öldüremeyecekleri kadar büyük mikropları yakalamak için kendi nükleer DNA'larını ve enzimlerini dışarı fırlatarak oluşturdukları ağ yapılarına nötrofil ekstrasellüler tuzakları (NET) adı verilir.",
                "nötrofil ekstrasellüler tuzakları",
                "NETosis olarak adlandırılan özel hücre ölümüyle saçılan kromatin ağları"
            )
        ]
    })

    # Slide 90
    slides.append({
        "slideNumber": 90,
        "title": "Bölüm 9 Entegrasyonu: Lökosit Aracılı Doku Hasarı Hastalıkları",
        "subtitle": "Romatoid artrit, gut, ARDS ve glomerülonefritte lökositlerin kontrolsüz fagozom sızıntısı",
        "badge": "İmmünopatoloji",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Lökositlerin muhteşem antimikrobiyal silahları (ROS, MPO, elastaz) konak için de ölümcül olabilir. "
            "Lökositlerin çevre dokuyu tahrip ettiği üç patolojik mekanizma vardır:\n\n"
            "1. **Yutulamayan Hedef / Boşa Çıkan Fagositoz (Frustrated Phagocytosis):** Lökosit düz bir yüzeye "
            "(örneğin glomerül bazal membranı veya eklem kıkırdağı) yapışmış immün kompleksleri yutmaya çalışır. "
            "Hedef çok büyük olduğu için psödopodlar birleşemez; fagozom kapanamaz. Lizozomlar enzimlerini "
            "doğrudan doku yüzeyine kusar (**glomerülonefrit ve romatoid artrit kıkırdak erozyonu**).\n\n"
            "2. **Membran Yırtılması (Sitotoksik Kaçak):** Kristaller (ürat, silika) fago-lizozomu içeriden deler; "
            "enzimler sitoplazmaya ve dokuya saçılır (**Gut ve Silikozis**).\n\n"
            "3. **Regürjitasyon:** Fagozom henüz dışarıya açıkken lizozomun erken füzyon yapması sonucu enzimlerin dışarı kaçması."
        ),
        "medicalTerms": [
            {"term": "Frustrated Phagocytosis (Boşa Çıkan Fagositoz)", "explanation": "Yutulamayacak kadar geniş düz yüzeylere yapışan lökositlerin lizozomal içeriklerini doğrudan ekstrasellüler dokuya boşaltmasıdır."},
            {"term": "İmmün Kompleks Glomerülonefriti", "explanation": "Glomerül bazal membranına çöken antikor-antijen komplekslerine saldıran nötrofillerin böbrek filtresini eritmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Düz yüzeylerdeki immün komplekslere saldıran nötrofillerin dokuyu eritmesi 'Frustrated Phagocytosis' örneğidir.",
            "📌 [SINAV SPOTU] Glomerülonefrit ve romatoid artritteki kıkırdak yıkımı lökosit enzimlerinin ekstrasellüler regürjitasyonudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Boşa Çıkan Fagositoz", "desc": "Büyük yüzeylerde fagozom kapanamaz, enzimler dokuya dökülür.", "isKey": True},
                {"title": "Klinik Yıkım", "desc": "Glomerülonefrit ve artritte kıkırdak ve bazal membran erir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Nötrofillerin düz bir bazal membran yüzeyine çökmüş geniş immün kompleksleri yutmaya çalışırken fagozomu kapatamayıp enzimlerini dokuya kusması olayına frustrated phagocytosis adı verilir.",
                "frustrated phagocytosis",
                "Boşa çıkan veya sonuçsuz fagositoz anlamına gelen uluslararası tıbbi kavram"
            ),
            make_active_recall(
                "Akut glomerülonefritte böbrek glomerül filtrasyon bariyerinin delinerek hastanın idrarından masif protein ve kan (hematüri) kaçmasının primer hücresel mekanizması nedir?",
                "Glomerül bazal membranına çöken immün komplekslere saldıran nötrofillerin fagositozu tamamlayamayarak (frustrated phagocytosis) ortama nötrofil elastazı ve reaktif oksijen radikalleri saçması, bazal membran tip IV kollajenini eritmesidir."
            )
        ]
    })

    return slides
