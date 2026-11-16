"""
Bölüm 2: Steatoz (Yağlı Değişim) Patofizyolojisi, Etiyolojisi ve Morfolojisi
Adımlar: 11 - 20
Checkpoint: Adım 19 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # ADIM 11
    slides.append({
        "slideNumber": 11,
        "title": "Steatoz (Yağlı Değişim) Tanımı ve Tutulan Başlıca Organlar",
        "subtitle": "Parankimal hücrelerde nötral trigliserid birikiminin hücresel temelleri",
        "badge": "Steatoz Tanımı",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Steatoz veya diğer adıyla yağlı değişim (fatty change), parankimal hücrelerin sitoplazmasında anormal "
            "miktarda trigliserid birikmesiyle tanımlanan patolojik bir durumdur. Yağ metabolizmasının merkezi "
            "organı olması sebebiyle en sık ve en dramatik olarak karaciğerde görülür. Ancak lipid metabolizmasına "
            "bağımlı diğer parankimatöz organlar da belirgin şekilde etkilenebilir.\n\n"
            "> [YÜKSEK VERİM] Karaciğer dışında kalp kası (miyokardiyum), iskelet kası ve böbrek tübül epitel "
            "hücreleri de belirgin steatoz gelişimine yatkındır.\n\n"
            "Normal koşullarda hücre içinde yalnızca çok az miktarda lipid damlacıkları bulunurken, metabolik stres "
            "altında trigliseridler sitoplazmayı tamamen dolduracak vakuollere dönüşür."
        ),
        "medicalTerms": [
            {"term": "Trigliserid", "explanation": "Gliserol ve üç yağ asidinden oluşan, ana enerji depolayan nötral lipid molekülüdür."},
            {"term": "Yağlı Değişim", "explanation": "Hücre sitoplazmasında optik olarak boş görünen lipid vakuollerinin birikmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Steatoz parankim hücrelerinde trigliserid birikimini ifade eder.",
            "📌 [SINAV SPOTU] En sık karaciğerde, ardından miyokard ve böbrek tübüllerinde görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Biriken Molekül", "desc": "Nötral trigliseridlerdir (esterleşmiş serbest yağ asitleri).", "isKey": True},
                {"title": "Hedef Dokular", "desc": "Hepatositler, kardiyomiyositler, proksimal tübül hücreleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Parankimal hücrelerin sitoplazmasında aşırı trigliserid birikimi tablosuna steatoz veya yağlı değişim adı verilir.",
                "steatoz",
                "Trigliseridlerin hücre içi anormal göllenmesini tanımlayan tıbbi terim"
            ),
            make_active_recall(
                "Steatoz karaciğer dışında en sık hangi organ parankimlerinde gözlenir?",
                "Kalp kası (miyokardiyum), iskelet kası ve böbrek tübül epitel hücrelerinde gözlenir."
            )
        ]
    })

    # ADIM 12
    slides.append({
        "slideNumber": 12,
        "title": "Karaciğerde Lipid Metabolizması ve Yağ Asidi Döngüsü",
        "subtitle": "Hepatosit içine serbest yağ asidi alımı, esterleşme ve lipoprotein salınımı",
        "badge": "Metabolizma",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Hepatositlerde serbest yağ asitleri (FFA) iki ana kaynaktan temin edilir: yağ dokusundan lipoliz yoluyla "
            "salınan dolaşımdaki FFA'lar ve diyetle alınan kşilomikron yıkım ürünleri. Hepatosit içine giren FFA'lar "
            "ya mitokondride beta-oksidasyon ile yakılarak enerjiye dönüştürülür ya da gliserol ile esterleşerek "
            "trigliseridleri oluşturur.\n\n"
            "> [TEMEL İLKE] Trigliseridlerin karaciğerden kana verilebilmesi için apolipoproteinler (özellikle ApoB-100) "
            "ile birleşip çok düşük yoğunluklu lipoprotein (VLDL) kompleksini oluşturması zorunludur.\n\n"
            "Bu basamakların herhangi birindeki aksaklık (aşırı FFA girişi, bozulmuş beta-oksidasyon, yetersiz apoprotein "
            "sentezi veya salgılama bloğu) trigliseridlerin hücrede hapsolmasına yol açar."
        ),
        "medicalTerms": [
            {"term": "Serbest Yağ Asidi (FFA)", "explanation": "Dolaşımda albümine bağlı taşınan ve karaciğerde trigliseride dönüştürülen lipidlerdir."},
            {"term": "VLDL", "explanation": "Karaciğerde sentezlenen trigliseridleri periferik dokulara taşıyan lipoproteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Karaciğerden lipid çıkışı için ApoB-100 ve VLDL sentezi şarttır.",
            "📌 [SINAV SPOTU] Trigliserid sentez hızı VLDL sekresyon hızını aştığında steatoz başlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Giriş Yolları", "desc": "Adipoz lipolizi, diyet emilimi ve hepatik de novo lipogenez.", "isKey": True},
                {"title": "Çıkış Yolu", "desc": "Mitokondriyal oksidasyon veya VLDL salınımı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Hepatositte Normalden Steatoza Geçiş Basamakları",
                [
                    "1. FFA Artışı: Yağ dokusundan salınan serbest yağ asitleri karaciğere yoğun şekilde ulaşır.",
                    "2. Esterleşme: Hepatosit içinde yağ asitleri hızla trigliserid moleküllerine dönüştürülür.",
                    "3. Apolipoprotein Sınırı: ApoB-100 sentez kapasitesi aşılır veya salgılama yetersiz kalır.",
                    "4. Vakuol Oluşumu: Salınamayan trigliseridler sitoplazmada vakuoller halinde toplanarak steatozu başlatır."
                ]
            ),
            make_cloze(
                "Karaciğerde sentezlenen trigliseridlerin kana salgılanabilmesi için apolipoprotein molekülleriyle paketlenmesi gerekir.",
                "apolipoprotein",
                "Lipidleri lipoprotein formunda dolaşıma çıkaran protein grubu"
            )
        ]
    })

    # ADIM 13
    slides.append({
        "slideNumber": 13,
        "title": "Steatoz Etiyolojisi: Alkol Toksisitesi ve Biyokimyasal Yıkım",
        "subtitle": "Etanol metabolizması, NADH artışı ve mitokondriyal yağ asidi oksidasyon blokajı",
        "badge": "Alkolik Steatoz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gelişmiş ülkelerde karaciğer steatozunun en sık ve en klasik etiyolojik nedeni aşırı alkol tüketimidir. "
            "Etanol, hepatosit sitozolünde alkol dehidrogenaz (ADH) ve mikrozomlarda CYP2E1 tarafından asetaldehite, "
            "ardından mitokondride asetaldehit dehidrogenaz (ALDH) tarafından asetata dönüştürülür.\n\n"
            "> [SINAV SPOTU] Etanolün metabolizması hücre içi NAD+'ı tüketir ve muazzam bir NADH/NAD+ oranı artışına yol açar; "
            "bu yüksek NADH düzeyi mitokondriyal beta-oksidasyonu doğrudan inhibe eder.\n\n"
            "Sonuç olarak serbest yağ asitleri mitokondride yakılamaz; zorunlu olarak trigliserid sentezine yönlendirilir. "
            "Ayrıca mikrotübül fonksiyonu bozularak lipoproteinlerin hücre dışına sekresyonu bloke olur."
        ),
        "medicalTerms": [
            {"term": "NADH / NAD+ Oranı", "explanation": "Alkol metabolizmasıyla yükselen ve yağ asidi oksidasyonunu durduran redoks dengesidir."},
            {"term": "Asetaldehit", "explanation": "Alkolün toksik ara metaboliti olup hücre proteinleriyle kovalent bağ kurar."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Alkol alımında artan NADH/NAD+ oranı mitokondriyal yağ asidi beta-oksidasyonunu bloke eder.",
            "📌 [SINAV SPOTU] Alkolik steatoz alkol tüketimi kesildiğinde tamamen gerileyebilen dinamik bir lezyondur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Oksidasyon İnhibisyonu", "desc": "NADH fazlalığı yağ asitlerinin yakılmasını önler.", "isKey": True},
                {"title": "Sekresyon Defekti", "desc": "Mikrotübül hasarı VLDL ekzositozunu engeller.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Alkol tüketimine bağlı karaciğer steatozu gelişiminde yağ asitlerinin mitokondriyal beta-oksidasyonunu doğrudan inhibe eden temel biyokimyasal değişiklik hangisidir?",
                {
                    "A": "Hücre içi ATP düzeyinin aşırı artması",
                    "B": "Sitoplazma ve mitokondride NADH / NAD+ oranının belirgin yükselmesi",
                    "C": "Apolipoprotein B-100 transkripsiyonunun uyarılması",
                    "D": "Lizozomal asit lipaz enziminin mutasyonu",
                    "E": "Glutatyon peroksidaz aktivitesinin iki katına çıkması"
                },
                "B",
                {
                    "A": "Alkol toksisitesinde ATP artışı değil mitokondriyal hasar ve ATP azalması görülür.",
                    "B": "Doğru! Alkol oksidasyonu NAD+'ı tüketip NADH üretir; yüksek NADH/NAD+ beta-oksidasyonu kilitler.",
                    "C": "Apolipoprotein sentezi uyarılmaz, aksine salgılama bozulur.",
                    "D": "Lizozomal asit lipaz Wolman hastalığıyla ilgilidir, alkol steatozuyla değil.",
                    "E": "Glutatyon alkolün oksidatif stresinde tükenir, artmaz."
                }
            ),
            make_cloze(
                "Etanol oksidasyonu sonucu yükselen sitozolik NADH düzeyi yağ asitlerinin mitokondriyal oksidasyonunu inhibe eder.",
                "NADH",
                "Etanol yıkımında açığa çıkan indirgenmiş koenzim molekülü"
            )
        ]
    })

    # ADIM 14
    slides.append({
        "slideNumber": 14,
        "title": "Steatoz Etiyolojisi: Obezite, Tip 2 Diyabet ve İnsülin Direnci",
        "subtitle": "Metabolik disfonksiyon ilişkili steatotik karaciğer hastalığı (MASLD) mekanizması",
        "badge": "Metabolik Steatoz",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Günümüzde alkol dışı karaciğer yağlanması (yeni adıyla MASLD - metabolik disfonksiyon ilişkili steatotik "
            "karaciğer hastalığı), obezite ve tip 2 diabetes mellitusun küresel artışıyla en yaygın karaciğer patolojisi "
            "haline gelmiştir. Patogenezin kalbinde periferik insülin direnci yer alır.\n\n"
            "> [KLİNİK İPUCU] İnsülin direnci varlığında adipoz dokudaki hormon duyarlı lipaz inhibe edilemez; kontrolsüz "
            "lipoliz ile dolaşıma devasa miktarda serbest yağ asidi boşalır ve karaciğere hücum eder.\n\n"
            "Aynı zamanda hiperinsülinemi karaciğerde de novo lipogenezi (SREBP-1c transkripsiyon faktörü üzerinden) "
            "kamçılar. Gelen ve üretilen aşırı yağ asitleri hepatositleri trigliserid havuzuna boğar."
        ),
        "medicalTerms": [
            {"term": "MASLD", "explanation": "Metabolik disfonksiyonla ilişkili yağlı karaciğer hastalığı spektrumudur."},
            {"term": "İnsülin Direnci", "explanation": "Hedef dokuların insülin sinyaline beklenen fizyolojik yanıtı verememesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İnsülin direncinde kontrolsüz yağ dokusu lipolizi karaciğere serbest yağ asidi girişini katlar.",
            "📌 [SINAV SPOTU] Obezite ve tip 2 diyabet alkol dışı steatozun en sık nedenleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yağ Akışı", "desc": "Adipoz dokudan hepatik dolaşıma serbest yağ asidi seli.", "isKey": True},
                {"title": "De Novo Lipogenez", "desc": "Karaciğerin bizzat kendi içinde karbonhidratlardan yağ üretmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Alkolik Steatoz vs Metabolik (Diyabet/Obezite) Steatoz",
                "Alkolik Steatoz",
                "Etanol metabolizmasıyla artan NADH'nin beta-oksidasyonu bloke etmesi ve mikrotübül toksisitesiyle oluşur.",
                "Metabolik Steatoz (MASLD)",
                "İnsülin direnci kaynaklı aşırı adipoz lipolizi ve uyarılmış de novo lipogenez sonucu karaciğere aşırı FFA yüklenmesiyle oluşur."
            ),
            make_active_recall(
                "İnsülin direnci adipoz dokuyu ve karaciğeri etkileyerek steatozu nasıl tetikler?",
                "Adipoz dokuda lipolizi artırarak karaciğere serbest yağ asidi akışını yükseltir ve karaciğerde de novo lipid sentezini uyarır."
            )
        ]
    })

    # ADIM 15
    slides.append({
        "slideNumber": 15,
        "title": "Protein-Kalori Malnütrisyonu (Kvaşiorkor) ve Toksinlere Bağlı Steatoz",
        "subtitle": "Apolipoprotein sentezinin çöküşü ve toksik sekresyon blokajı",
        "badge": "Malnütrisyon ve Toksin",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Steatoz yalnızca aşırı kalori ve yağ yüküyle değil, şiddetli protein yetersizliğinde de meydana gelir. "
            "Şiddetli protein-kalori malnütrisyonu olan Kvaşiorkor hastası çocuklarda karaciğer ileri derecede yağlı "
            "ve büyümüştür. Bunun temel nedeni, hepatositlerin trigliseridleri kanda taşıyacak apolipoproteinleri "
            "(özellikle ApoB-100) sentezleyecek amino asit bulamamasıdır.\n\n"
            "> [YÜKSEK VERİM] Karbon tetraklorür (CCl4) gibi hepatotoksinler ise granüllü ER'yi parçalayarak protein "
            "sentezini durdurur; lipidler paketlenemez ve saatler içinde masif steatoz gelişir.\n\n"
            "Bu iki durum, steatozun 'lipoprotein paketleme ve sekresyon defekti' mekanizmasını kusursuz şekilde belgeler."
        ),
        "medicalTerms": [
            {"term": "Kvaşiorkor", "explanation": "Yetersiz protein alımıyla seyreden, hepatomegali, ödem ve steatozla karakterize çocukluk malnütrisyonudur."},
            {"term": "Karbon Tetraklorür (CCl4)", "explanation": "Serbest radikallere dönüşerek ER membranlarını peroksidasyonla yıkan kimyasal toksindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kvaşiorkorda steatoz gelişiminin nedeni apolipoprotein sentezinin yetersiz kalmasıdır.",
            "📌 [SINAV SPOTU] CCl4 zehirlenmesinde ER hasarı nedeniyle apoprotein sentezi durur ve steatoz oluşur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Protein Açlığı", "desc": "Amino asit yokluğu apolipoprotein üretimini sıfırlar.", "isKey": True},
                {"title": "Toksik Yıkım", "desc": "Serbest radikaller protein sentez organellerini tahrip eder.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Kvaşiorkor hastalarında gelişen karaciğer yağlanmasının temel nedeni apolipoprotein sentezinin yetersiz kalmasıdır.",
                "apolipoprotein",
                "Trigliseridi bağlayıp kana salan protein yapısı"
            ),
            make_active_recall(
                "CCl4 toksisitesi karaciğerde hangi organeli tahrip ederek dakikalar/saatler içinde steatoza yol açar?",
                "Granüllü endoplazmik retikulumu parçalayarak apolipoprotein sentezini ve lipid sekresyonunu durdurur."
            )
        ]
    })

    # ADIM 16
    slides.append({
        "slideNumber": 16,
        "title": "Hipoksi ve Hücre Hasarının Trigliserid Birikimine Etkisi",
        "subtitle": "Miyokardda kaplan derisi (tigroid) görünümü ve santrilobüler hepatik steatoz",
        "badge": "Hipoksik Steatoz",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Oksijen yetersizliği (hipoksi ve iskemi), hücrelerin oksidatif fosforilasyonunu ve mitokondriyal yağ asidi "
            "oksidasyonunu felce uğratır. Enerji üretemeyen ve yağ asitlerini yakamayan parankim hücreleri yağ "
            "damlacıklarını sitoplazmada biriktirir. Karaciğerde oksijen seviyesinin en düşük olduğu santral ven "
            "çevresi (Zon 3), hipoksiye bağlı steatozdan ilk ve en ağır etkilenen bölgedir.\n\n"
            "> [SINAV SPOTU] Kronik şiddetli anemide kalp kasında hipoksiye bağlı olarak sarı yağlı çizgiler ile "
            "kırmızı-kahverengi normal miyokardın ardışık dizilimi 'kaplan derisi' (tigroid kalp) görünümünü oluşturur.\n\n"
            "Bu durum, yağlı değişimin doğrudan hücresel oksijenlenme ve mitokondri bütünlüğüyle bağını gösterir."
        ),
        "medicalTerms": [
            {"term": "Tigroid Kalp", "explanation": "Kronik hipokside miyokardda yağlı sarı bantların oluşturduğu kaplan derisi manzarasıdır."},
            {"term": "Zon 3 (Santrilobüler)", "explanation": "Karaciğer asinüsünde oksijenden en fakir olan santral ven komşuluğundaki alandır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kronik anemide kalpte kaplan derisi (tigroid) manzarası hipoksik yağlı değişimin sonucudur.",
            "📌 [SINAV SPOTU] Hipoksi mitokondriyal beta-oksidasyonu bozarak lipid birikimini tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mitokondri Felci", "desc": "Oksijen yokluğunda yağ asidi beta-oksidasyonu durur.", "isKey": True},
                {"title": "Miyokard Tutulumu", "desc": "Papiller kaslar ve sol ventrikülde sarı-kırmızı alacalı bantlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Kronik şiddetli anemi tanılı bir hastanın otopsisinde kalpte sarı yağlı bantlar ile normal kırmızı kas liflerinin ardışık diziliminden oluşan 'kaplan derisi' (tigroid kalp) manzarası izleniyor. Bu patolojinin altta yatan temel mekanizması hangisidir?",
                {
                    "A": "Miyokardit sonrası gelişen distrofik kalsiyum birikimi",
                    "B": "Hipoksiye bağlı mitokondriyal beta-oksidasyon bozukluğu ve miyokardiyal steatoz",
                    "C": "Aşırı demir yüklenmesine bağlı hemosiderin birikimi",
                    "D": "Kardiyomiyositlerde glikojen depo hastalığı gelişimi",
                    "E": "Apolipoproteinlerin genetik mutasyonla yıkılması"
                },
                "B",
                {
                    "A": "Kaplan derisi kalsiyum birikimi değil yağlı değişimdir.",
                    "B": "Doğru! Hipoksi yağ asidi oksidasyonunu bozar; kardiyomiyositlerde trigliserid birikir.",
                    "C": "Demir birikimi hemosiderozdur ve çikolata-kahve renk verir.",
                    "D": "Glikojen depo hastalığı konjenitaldir ve tigroid kalıbı yapmaz.",
                    "E": "Miyokardiyal tigroid görünüm genetik apoprotein mutasyonuna bağlı değildir."
                }
            ),
            make_cloze(
                "Kronik hipoksi zemininde kalp kasında gelişen alacalı yağlı değişim kaplan derisi görünümü olarak adlandırılır.",
                "kaplan derisi",
                "Kronik anemide kalpteki sarı-kırmızı çizgili makroskopi"
            )
        ]
    })

    # ADIM 17
    slides.append({
        "slideNumber": 17,
        "title": "Steatozun Morfolojisi: Makroveziküler vs Mikroveziküler Yağlanma",
        "subtitle": "Karaciğer makroskopisi ve mikroskobide çekirdek itilmesi dinamikleri",
        "badge": "Morfoloji",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Makroskobik olarak steatotik karaciğer belirgin şekilde büyür (hepatomegali, 4-6 kg'a ulaşabilir), "
            "kapsülü gergindir, rengi sarımsı-turuncu ve kıvamı yumuşaktır. Kesit yüzeyi parlak, yağlı bir tabaka ile "
            "kaplanır. Mikroskobik incelemede ise iki ana patern ayırt edilir: makroveziküler ve mikroveziküler steatoz.\n\n"
            "> [SINAV SPOTU] Makroveziküler steatozda tek ve dev bir lipid vakuolü çekirdeği hücre kenarına iterek taşlı "
            "yüzük görünümü verir; alkol, obezite ve diyabette tipiktir.\n\n"
            "Mikroveziküler steatozda ise sitoplazma sayısız köpüksü küçük lipid vakuolüyle doludur ancak çekirdek "
            "merkezde kalır; Reye sendromu ve gebeliğin akut yağlı karaciğerinde izlenen acil tablodur."
        ),
        "medicalTerms": [
            {"term": "Makroveziküler Steatoz", "explanation": "Tek büyük yağ damlasının çekirdeği perifere ittiği yaygın kronik yağlanma tipidir."},
            {"term": "Mikroveziküler Steatoz", "explanation": "Çekirdeği itmeyen küçük çok sayıda vakuol içeren, mitokondriopatilerde görülen akut tablodur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Makroveziküler steatozda çekirdek perifere itilir; alkol ve obezitede görülür.",
            "📌 [SINAV SPOTU] Mikroveziküler steatozda çekirdek merkezdedir; Reye sendromu ve gebelik akut karaciğer yağlanmasında görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Makroskopi", "desc": "Büyük, sarı, yumuşak, kesit yüzeyi parlak ve yağlı karaciğer.", "isKey": True},
                {"title": "Mikro vs Makro", "desc": "Çekirdeğin konumu (merkezde vs kenara itilmiş) ayırt edicidir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Özellik", "Makroveziküler Steatoz", "Mikroveziküler Steatoz"],
                [
                    [("Vakuol Boyutu", False, ""), ("Tek, büyük vakuol", True, "Sitoplazmayı kaplayan dev yağ damlası"), ("Çok sayıda minik vakuol", False, "")],
                    [("Çekirdeğin Konumu", False, ""), ("Hücre kenarına itilmiş (taşlı yüzük)", True, "Perifere doğru sıkıştırılmış nükleus"), ("Merkezde korunmuş", False, "")],
                    [("Tipik Etiyolojiler", False, ""), ("Alkol, obezite, tip 2 diyabet", False, ""), ("Reye sendromu, gebelik akut yağlı KC", True, "Akut mitokondri hasarıyla giden ağır tablo")]
                ]
            ),
            make_cloze(
                "Makroveziküler steatozda biriken dev lipid damlası hücre çekirdeğini perifere doğru iter.",
                "perifere",
                "Hücrenin kenar zarına doğru yönelme durumu"
            )
        ]
    })

    # ADIM 18
    slides.append({
        "slideNumber": 18,
        "title": "Steatohepatit, İlerleyici Fibrozis ve Siroz Gelişim Riski",
        "subtitle": "Lipid peroksidasyonu, inflamatuvar hücre infiltrasyonu ve yıldızsı hücre aktivasyonu",
        "badge": "İlerleyici Hasar",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Basit steatoz çoğunlukla geri dönüşümlü ve sessiz bir durum olsa da, aşırı serbest yağ asitlerinin lipid "
            "peroksidasyonuna uğraması toksik reaktif oksijen türlerini (ROS) üretir. Bu durum hepatositlerde nekroz, "
            "apoptoz ve balonlaşma dejenerasyonunu başlatır. Parankime nötrofiller ve lenfositler hücum ettiğinde "
            "tablo steatohepatite (NASH/MASH veya alkolik hepatit) döner.\n\n"
            "> [KRİTİK UYARI] Hasarlanan hepatositlerden salınan sitokinler Disse mesafesindeki Ito (hepatik stellat) "
            "hücrelerini aktive ederek kollajen sentezletir; perisinüzoidal fibrozis siroza kadar ilerler.\n\n"
            "Bu süreç, basit bir lipid birikiminin kronik inflamasyon ve organ yetmezliğine nasıl evrilebileceğinin kanıtıdır."
        ),
        "medicalTerms": [
            {"term": "Steatohepatit", "explanation": "Yağ birikimine hepatosit hasarı, balonlaşma ve inflamasyonun eşlik ettiği tablodur."},
            {"term": "Hepatik Stellat Hücre (Ito)", "explanation": "A vitamini depolayan, hasar anında miyofibroblasta dönüşüp kollajen üreten hücredir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Basit steatoza balonlaşma ve nötrofil infiltrasyonu eklendiğinde steatohepatit adını alır.",
            "📌 [SINAV SPOTU] Fibrozis gelişiminden sorumlu ana hücre Disse aralığındaki hepatik stellat (Ito) hücresidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lipid Toksisitesi", "desc": "Serbest yağ asitleri membranları peroksidasyonla zedeler.", "isKey": True},
                {"title": "Fibrozis ve Siroz", "desc": "Stellat hücrelerin kollajen üretimiyle parankim nodüllere bölünür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Steatozdan Siroza Giden Fibrogenetik Yol",
                [
                    "1. Basit Steatoz: Hepatosit sitoplazmasında aşırı trigliserid birikir.",
                    "2. Lipotoksisite ve ROS: Lipid peroksidasyonu hepatositte balonlaşma ve zedelenme yapar.",
                    "3. İnflamasyon: Parankime nötrofiller infiltre olarak steatohepatit tablosunu kurar.",
                    "4. Stellat Hücre Aktivasyonu: Ito hücreleri miyofibroblasta dönüşerek Tip I kollajen üretir.",
                    "5. Siroz: Yaygın perisinüzoidal fibrozis parankimi nodüllere ayırarak sirozu oluşturur."
                ]
            ),
            make_cloze(
                "Karaciğer hasarında kollajen sentezleyerek fibrozisi başlatan hücreler Disse aralığındaki hepatik stellat hücreleridir.",
                "hepatik stellat",
                "A vitamini depolayan ve miyofibroblasta dönüşen Ito hücreleri"
            )
        ]
    })

    # ADIM 19 - CHECKPOINT 2
    slides.append({
        "slideNumber": 19,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Steatoz Patogenezi ve Morfolojik Özellikleri",
        "subtitle": "Trigliserid metabolizması, alkol, diyabet ve morfolojik tiplerin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 2,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında parankimal hücrelerde trigliserid birikimini (steatoz) tüm boyutlarıyla sentezliyoruz. "
            "Steatoz en sık karaciğerde, ardından miyokardiyum ve böbreklerde izlenir. Etiyolojide alkol (artan NADH/NAD+ ile "
            "beta-oksidasyon blokajı), obezite ve diyabet (insülin direnciyle aşırı serbest yağ asidi girişi), Kvaşiorkor ve "
            "toksinler (apolipoprotein sentez yetersizliği) ve hipoksi (tigroid kalp) yer alır.\n\n"
            "> [KLİNİK İPUCU] Makroveziküler steatozda çekirdek kenara itilir; mikroveziküler tipte merkezdedir.\n\n"
            "Aşağıdaki 3 akıl kartını inceleyerek steatozun moleküler mekanizmalarını kalıcı hale getiriniz."
        ),
        "medicalTerms": [
            {"term": "Steatoz", "explanation": "Parankimal hücrelerde trigliserid depolanmasıdır."},
            {"term": "Makroveziküler Yağlanma", "explanation": "Çekirdeğin kenara itildiği büyük tek lipid vakuolü paternidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Alkolde NADH yüksekliği, Kvaşiorkorda apolipoprotein eksikliği steatoz yapar.",
            "📌 [SINAV SPOTU] Kronik anemide hipoksiye bağlı miyokardiyal steatoz 'kaplan derisi' görünümü verir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Alkol Mekanizması", "desc": "NADH artışı, beta-oksidasyon felci.", "isKey": True},
                {"title": "Kvaşiorkor", "desc": "Protein açlığı, ApoB-100 sentez defekti.", "isKey": True},
                {"title": "Morfoloji", "desc": "Sarı-büyük karaciğer; mikro ve makroveziküler vakuoller.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-04",
                "Steatozda parankimal hücrelerde biriken temel lipid türü nedir?",
                "Nötral trigliseridlerdir (gliserol ve yağ asidi esterleri).",
                "Hücre içi yağ depolanmasının temel molekülü"
            ),
            make_flashcard(
                "k1-07-fc-05",
                "Alkol alımında steatoza yol açan temel biyokimyasal bozukluk nedir?",
                "Etanol oksidasyonu sonucu hücre içi NADH/NAD+ oranının aşırı yükselmesi ve bunun mitokondriyal yağ asidi beta-oksidasyonunu bloke etmesidir.",
                "Etanol metabolizması ve oksidasyon inhibisyonu"
            ),
            make_flashcard(
                "k1-07-fc-06",
                "Makroveziküler ile mikroveziküler steatoz arasındaki temel mikroskobik fark nedir?",
                "Makrovezikülerde tek büyük vakuol çekirdeği kenara iter; mikrovezikülerde çok sayıda küçük vakuol bulunur ve çekirdek merkezde kalır.",
                "Hücre çekirdeğinin konumu ve vakuol boyutu"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Kronik alkol tüketimi karaciğerde çekirdeği kenara iten makroveziküler steatoz tablosuna yol açar.",
                "makroveziküler",
                "Tek büyük vakuollü kronik yağlanma morfolojisi"
            )
        ]
    })

    # ADIM 20
    slides.append({
        "slideNumber": 20,
        "title": "Steatoz Klinik Yönetimi ve Karşılaştırmalı Değerlendirme",
        "subtitle": "Geri dönüşümlü evreden irreversibl siroza geçişin önlenmesi",
        "badge": "Klinik Yönetim",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Klinik pratikte steatoz çoğunlukla asemptomatiktir ve rutin kan testlerinde hafif ALT/AST yüksekliği veya "
            "ultrasonda parankim ekojenite artışı ile tesadüfen saptanır. Hastalığın en kritik özelliği, erken evredeki "
            "basit yağlanmanın tamamen geri dönüşümlü (reversibl) olmasıdır. Alkolün tamamen kesilmesi, kilo kaybı ve "
            "diyabetin kontrol altına alınmasıyla birkaç hafta içinde karaciğer normale döner.\n\n"
            "> [KLİNİK İPUCU] Ancak steatohepatit ve perisinüzoidal fibrozis geliştiğinde tablo irreversibl siroz ve "
            "hepatosellüler karsinom (HCC) riskine doğru ilerler.\n\n"
            "Bu nedenle erken tanı, etiyolojik faktörün süratle eliminasyonu ve yaşam tarzı değişiklikleri hayati önem taşır."
        ),
        "medicalTerms": [
            {"term": "Reversibilite", "explanation": "Stres faktörünün kalkmasıyla dokunun orijinal sağlıklı yapısına dönebilmesidir."},
            {"term": "Hepatosellüler Karsinom", "explanation": "Siroz ve kronik steatohepatit zemininde gelişebilen primer karaciğer kanseridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Basit steatoz etiyolojik etken ortadan kaldırıldığında tamamen geri dönüşümlüdür.",
            "📌 [SINAV SPOTU] Fibrozis ve siroz evresine geçiş geri dönüşsüz organ hasarı anlamına gelir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Erken Evre", "desc": "Tamamen reversibl, fonksiyonel rezerv korunmuş.", "isKey": True},
                {"title": "Geç Evre", "desc": "Fibrotik bantlar, rejenerasyon nodülleri, portal hipertansiyon.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "45 yaşında obez ve haftada yüksek miktarda alkol tüketen bir hastada ultrasonda karaciğerde yaygın ekojenite artışı saptanıyor. Biyopside çekirdeği kenara itilmiş makroveziküler steatoz görülüyor, fibrozis izlenmiyor. En doğru yaklaşım hangisidir?",
                [
                    {
                        "text": "Karaciğer nakil listesine acil başvuru yapılmalıdır çünkü lezyon geri dönüşsüzdür.",
                        "isCorrect": False,
                        "feedback": "Yanlış! Fibrozis olmayan erken steatoz tamamen geri dönüşümlüdür; nakil endikasyonu yoktur."
                    },
                    {
                        "text": "Alkolün kesilmesi ve kilo kontrolü sağlanmalıdır; zira fibrozis gelişmemiş erken evre tamamen geri dönüşümlüdür.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Etiyolojinin kaldırılmasıyla hepatositlerdeki trigliseridler metabolize edilir ve karaciğer normale döner."
                    }
                ]
            ),
            make_active_recall(
                "Steatozda erken evrenin en umut verici klinik özelliği nedir?",
                "Tetikleyici etken (alkol, obezite, toksin) ortadan kaldırıldığında dokunun tamamen normale dönebilmesi (reversibl olmasıdır)."
            )
        ]
    })

    return slides
