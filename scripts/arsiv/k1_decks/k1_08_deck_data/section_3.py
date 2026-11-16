"""
Bölüm 3: Reaktif Oksijen Türleri (ROS), Oksidatif Stres ve Antioksidan Savunma
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
        "title": "Serbest Radikal ve ROS Biyokimyası: Üç Anahtar Molekül",
        "subtitle": "Süperoksit (O2•-), hidrojen peroksit (H2O2) ve en reaktif hidroksil radikali (•OH)",
        "badge": "ROS Biyokimyası",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Serbest radikal, en dış yörüngesinde eşleşmemiş tek bir elektron taşıyan, bu nedenle kimyasal olarak son "
            "derece kararsız ve agresif reaktif olan kimyasal türdür. Oksijenden türeyen serbest radikaller ve onların "
            "reaktif öncüllerine topluca 'Reaktif Oksijen Türleri' (ROS) adı verilir. Biyolojik sistemlerde sırasıyla "
            "üç anahtar ROS basamağı izlenir.\n\n"
            "> [SINAV SPOTU] Oksijenin tek elektron almasıyla 'süperoksit anyonu' (O2•-), onun dismutasyonuyla 'hidrojen "
            "peroksit' (H2O2) ve demir katalizli Fenton reaksiyonu ile biyolojik dokulara en ölümcül darbeyi vuran "
            "'hidroksil radikali' (•OH) meydana gelir.\n\n"
            "Hidroksil radikali o kadar reaktiftir ki oluştuğu yerde mikrosaniyeler içinde temas ettiği ilk biyomolekülü parçalar."
        ),
        "medicalTerms": [
            {"term": "Serbest Radikal", "explanation": "Dış orbitalinde eşleşmemiş tek elektron içeren, yüksek reaktiviteye sahip moleküldür."},
            {"term": "Hidroksil Radikali (•OH)", "explanation": "Fenton reaksiyonuyla oluşan, yarı ömrü en kısa ve hücreye en toksik serbest radikaldir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Süperoksit dismutaz ile H2O2'ye, ardından Fenton reaksiyonuyla •OH'ye dönüşür.",
            "📌 [SINAV SPOTU] Biyolojik dokularda en yıkıcı ve en reaktif serbest radikal hidroksil radikalidir (•OH)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Süperoksit (O2•-)", "desc": "Mitokondri solunum zincirinden kaçan ilk tek elektronlu radikal.", "isKey": True},
                {"title": "Hidrojen Peroksit (H2O2)", "desc": "Zarları kolayca aşan, demirle hidroksile dönüşen oksidan.", "isKey": True},
                {"title": "Hidroksil (•OH)", "desc": "Membran lipidi, protein ve DNA'yı saniyede yıkan nihai canavar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Demir varlığında Fenton reaksiyonu ile üretilen ve biyolojik sistemlere en ağır hasarı veren radikal hidroksil radikali formudur.",
                "hidroksil radikali",
                "Hücredeki en reaktif ve yıkıcı serbest radikal"
            ),
            make_active_recall(
                "Oksijenin mitokondride suya indirgenmesi sürecinde basamak basamak oluşan 3 temel reaktif oksijen türü (ROS) sırasıyla hangileridir?",
                "Sırasıyla süperoksit anyonu (O2•-), hidrojen peroksit (H2O2) ve hidroksil radikalidir (•OH)."
            )
        ]
    })

    # ADIM 22
    slides.append({
        "slideNumber": 22,
        "title": "ROS Üretim Kaynakları: Mitokondri Kaçakları ve Lökosit Patlaması",
        "subtitle": "Kompleks I ve III kaçakları, NADPH oksidaz solunum patlaması ve çevresel toksinler",
        "badge": "Üretim Kaynakları",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Hücre içinde fizyolojik ve patolojik koşullarda iki dev ROS fabrikası çalışır. Birincisi ve en süreklisi, "
            "tüm aerobik hücrelerin mitokondrilerindeki elektron taşıma zinciridir (özellikle Kompleks I ve Kompleks III). "
            "Mitokondriden geçen elektronların yaklaşık %1-2'si moleküler oksijene erken sızarak (elektron kaçağı) sürekli "
            "süperoksit anyonu üretir.\n\n"
            "> [SINAV SPOTU] İkinci büyük kaynak ise fagositoz yapan lökositlerin (nötrofil ve makrofaj) membranındaki "
            "'NADPH oksidaz' enzimidir; solunum patlaması (respiratory burst) ile bakterileri öldürmek için devasa ROS salar.\n\n"
            "Ayrıca iyonize radyasyon suyu radyolize ederek doğrudan hidroksil radikali fırtınası koparır."
        ),
        "medicalTerms": [
            {"term": "Elektron Kaçağı", "explanation": "Mitokondri solunum zincirinde elektronların Kompleks I/III'ten oksijene erken sızıp süperoksit yapmasıdır."},
            {"term": "Solunum Patlaması (Respiratory Burst)", "explanation": "Fagositik lökositlerin NADPH oksidaz ile mikrop öldürmek için aniden aşırı ROS üretmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücre içinde bazal ROS üretiminin ana kaynağı mitokondriyal elektron taşıma zinciridir.",
            "📌 [SINAV SPOTU] İnflamasyonda lökosit NADPH oksidazı mikropları yok etmek için solunum patlaması yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mitokondriyal Kaçak", "desc": "Kompleks I ve III'ten sızan elektronlar süperoksite döner.", "isKey": True},
                {"title": "Lökosit Patlaması", "desc": "NADPH oksidaz fagositoz sırasında mikropları yakar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Mitokondriyal Elektron Kaçağından Serbest Radikal Üretimine",
                [
                    "1. Oksidatif Fosforilasyon: Elektronlar solunum zinciri kompleksleri boyunca aktarılır.",
                    "2. Erken Elektron Kaçağı: Kompleks I veya III'ten elektronlar moleküler oksijene sızar.",
                    "3. Süperoksit Oluşumu: Oksijen tek elektron alarak süperoksit anyonuna (O2•-) dönüşür.",
                    "4. Dismutasyon: SOD enzimi süperoksiti hidrojen peroksite (H2O2) çevirir.",
                    "5. Fenton Hasarı: Serbest Fe2+ varlığında H2O2 parçalanarak dokuyu yıkan •OH radikallerini saçar."
                ]
            ),
            make_cloze(
                "Fagositik hücrelerin mikrop öldürmek amacıyla ani ve yoğun ROS üretmesine solunum patlaması adı verilir.",
                "solunum patlaması",
                "NADPH oksidaz aracılı ani radikal deşarjı"
            )
        ]
    })

    # ADIM 23
    slides.append({
        "slideNumber": 23,
        "title": "Antioksidan Enzim Savunma Sistemleri: SOD, Katalaz ve GPX",
        "subtitle": "Hücresel kompartımanların özelleşmiş enzimatik kalkanları ve kofaktörleri",
        "badge": "Enzimatik Savunma",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Hücreler ölümcül serbest radikal saldırılarına karşı üç ana enzimatik kalkan geliştirmiştir: "
            "1) Süperoksit Dismutaz (SOD): Süperoksiti hidrojen peroksite çevirir (mitokondride manganez bağımlı Mn-SOD, "
            "sitozolde bakır-çinko bağımlı Cu/Zn-SOD). 2) Katalaz: Peroksizomlarda yerleşiktir; hidrojen peroksiti "
            "doğrudan su ve oksijene parçalayarak (2 H2O2 → 2 H2O + O2) etkisiz hale getirir.\n\n"
            "> [SINAV SPOTU] 3) Glutatyon Peroksidaz (GPX): Selenyum bağımlı bir enzimdir; sitozol ve mitokondride "
            "indirgenmiş glutatyonu (GSH) kullanarak H2O2'yi suya indirger (2 GSH + H2O2 → GSSG + 2 H2O).\n\n"
            "Yaşlanmayla birlikte bu üç enzimin aktivitesi ve selenyum/çinko kofaktör desteği azalır."
        ),
        "medicalTerms": [
            {"term": "Süperoksit Dismutaz (SOD)", "explanation": "Süperoksit radikallerini hidrojen peroksite dönüştüren ilk basamak enzimidir."},
            {"term": "Glutatyon Peroksidaz (GPX)", "explanation": "Selenyum kofaktörüyle indirgenmiş glutatyonu kullanarak peroksitleri suya çeviren enzimdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Katalaz peroksizomda H2O2'yi suya çevirir; GPX ise selenyum bağımlıdır.",
            "📌 [SINAV SPOTU] Mitokondride Mn-SOD, sitoplazmada Cu/Zn-SOD görev yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "SOD Enzimi", "desc": "Süperoksiti (O2•-) H2O2'ye dismute eder.", "isKey": True},
                {"title": "Katalaz", "desc": "Peroksizomda H2O2'yi su ve moleküler oksijene parçalar.", "isKey": True},
                {"title": "Glutatyon Peroksidaz", "desc": "Selenyum içeren, GSH kullanarak peroksitleri nötralize eden enzim.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Antioksidan Enzim", "Hücresel Lokalizasyon", "Katalizlediği Reaksiyon", "Gerekli Kofaktör"],
                [
                    [("Mn-SOD", False, ""), ("Mitokondri matriksi", False, ""), ("Süperoksit → Hidrojen peroksit", False, ""), ("Manganez (Mn)", True, "Mitokondriyal izoform kofaktörü")],
                    [("Katalaz", False, ""), ("Peroksizomlar", False, ""), ("2 H2O2 → 2 H2O + O2", True, "Suyu ve oksijeni açığa çıkaran reaksiyon"), ("Demir (Hem grubu)", False, "")],
                    [("Glutatyon Peroksidaz (GPX)", False, ""), ("Sitozol ve mitokondri", False, ""), ("H2O2 + 2 GSH → GSSG + 2 H2O", False, ""), ("Selenyum (Se)", True, "Antioksidan enzim için şart olan eser element")]
                ]
            ),
            make_cloze(
                "Glutatyon peroksidaz enziminin aktif merkezinde kofaktör olarak görev yapan temel eser element selenyum mineralidir.",
                "selenyum",
                "GPX enziminin yapısındaki antioksidan mineral"
            )
        ]
    })

    # ADIM 24
    slides.append({
        "slideNumber": 24,
        "title": "Non-Enzimatik Antioksidanlar: Vitamin E, C, A ve Glutatyon",
        "subtitle": "Lipid fazı koruyucusu alfa-tokoferol, askorbik asit redüksiyonu ve tiyol tamponu",
        "badge": "Non-Enzimatik Kalkan",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Enzimatik savunmanın yanı sıra hücreler ve vücut sıvıları zengin bir non-enzimatik antioksidan havuzuna "
            "sahiptir. Bu sistemin iki büyük kahramanı Vitamin E ve Vitamin C'dir. Vitamin E (alfa-tokoferol) yağda çözünür; "
            "hücre membranlarının içine gömülerek membran lipit peroksidasyonu zincirini kıran birincil kalkandır.\n\n"
            "> [SINAV SPOTU] Vitamin E radikali yakalayıp okside olduğunda, sitozolde suda çözünen Vitamin C (askorbik "
            "asit) devreye girerek Vitamin E'yi tekrar indirger ve işlevsel hale getirir.\n\n"
            "İndirgenmiş glutatyon (GSH) ise hücre içindeki en yoğun tiyol (-SH) tamponudur; protein sülfhidril gruplarını "
            "oksidasyondan korur. Glutatyon redüktaz enzimi NADPH kullanarak okside GSSG'yi tekrar GSH'ye dönüştürür."
        ),
        "medicalTerms": [
            {"term": "Vitamin E (Tokoferol)", "explanation": "Hücre membranlarında lipid peroksidasyon zincirini kıran temel yağda çözünen antioksidandır."},
            {"term": "Glutatyon (GSH)", "explanation": "Glutamat, sistein ve glisinden oluşan, hücrenin ana redoks tamponu tripeptitidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Vitamin E membran lipid peroksidasyonunu durdurur; Vitamin C onu rejenere eder.",
            "📌 [SINAV SPOTU] GSH/GSSG oranı hücrenin redoks sağlığının en hassas göstergesidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Membran Kalkanı", "desc": "Alfa-tokoferol lipid çift katmanında peroksi radikallerini yakalar.", "isKey": True},
                {"title": "Sitozolik Destek", "desc": "Askorbik asit ve GSH su fazında radikalleri söndürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Vitamin E (Lipid Fazı) vs Vitamin C (Sulu Faz)",
                "Vitamin E (Alfa-Tokoferol)",
                "Hidrofobiktir; hücre zarına ve organel membranlarına yerleşerek lipid peroksidasyon zincirini doğrudan kırar.",
                "Vitamin C (Askorbik Asit)",
                "Hidrofiliktir; sitoplazmada ve ekstraselüler sıvıda serbest radikalleri nötralize eder ve okside olan Vitamin E'yi geri indirger."
            ),
            make_active_recall(
                "Hücre zarında lipid peroksidasyonu zincirini kıran Vitamin E molekülü radikali tuttuktan sonra sitoplazmada hangi vitamin tarafından tekrar indirgenir?",
                "Suda çözünen Vitamin C (askorbik asit) tarafından tekrar indirgenerek aktif formuna döndürülür."
            )
        ]
    })

    # ADIM 25
    slides.append({
        "slideNumber": 25,
        "title": "ROS'un Hedefleri 1: Lipid Peroksidasyonu ve Lipofusin",
        "subtitle": "Karbon-karbon çift bağlarına saldırı, malondialdehit (MDA) ve telolizozomlar",
        "badge": "Lipid Hasarı",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Serbest radikallerin hücredeki en yıkıcı hedeflerinden ilki plazma ve organel membranlarındaki polidoymamış "
            "yağ asitleridir (PUFA). Hidroksil radikali PUFA'nın çift bağ komşuluğundaki hidrojeni kopararak lipid "
            "radikali üretir. Oksijenle birleşen lipid radikali lipid peroksil radikaline dönüşür ve komşu yağ asitlerine "
            "saldırarak kendi kendini besleyen otokatalitik bir zincirleme reaksiyon başlatır.\n\n"
            "> [SINAV SPOTU] Membranlar parçalanır, akışkanlık ve geçirgenlik bariyeri çöker; son ürün olarak toksik "
            "malondialdehit (MDA) ve 4-hidroksinonenal (4-HNE) açığa çıkar.\n\n"
            "Bu oksitlenmiş membran artıkları otofajiyle lizozoma taşınır; parçalanamayan kalıntılar yaşlanma pigmenti "
            "olan 'lipofusin' granüllerini oluşturur."
        ),
        "medicalTerms": [
            {"term": "Lipid Peroksidasyonu", "explanation": "Serbest radikallerin membran yağ asitlerini zincirleme reaksiyonla parçalamasıdır."},
            {"term": "Malondialdehit (MDA)", "explanation": "Lipid peroksidasyonunun son ürünü olan ve doku oksidatif hasarını ölçen biyobelirteçtir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lipid peroksidasyonu otokatalitik zincirleme bir reaksiyondur; zarları deler.",
            "📌 [SINAV SPOTU] Lipofusin pigmenti lipid peroksidasyonunun parçalanamayan lizozomal son ürünüdür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Zincirleme Reaksiyon", "desc": "Bir tek serbest radikal yüzlerce lipid molekülünü peroksitler.", "isKey": True},
                {"title": "Toksik Artıklar", "desc": "MDA, 4-HNE oluşumu ve rezidüel lipofusin kümelenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Membran lipid peroksidasyonunun dokulardaki şiddetini belirlemek için kullanılan temel toksik son ürün malondialdehit molekülüdür.",
                "malondialdehit",
                "Lipid hasarını kanda ölçen aldehit belirteci"
            ),
            make_active_recall(
                "Lipid peroksidasyonunun hücresel yaşlanmadaki en karakteristik morfolojik mikroskobik yansıması nedir?",
                "Kardiyomiyosit ve hepatositlerin perinükleer sitoplazmasında biriken altın sarısı-kahverengi lipofusin granülleridir."
            )
        ]
    })

    # ADIM 26
    slides.append({
        "slideNumber": 26,
        "title": "ROS'un Hedefleri 2: Protein Oksidasyonu ve Karbonilasyon",
        "subtitle": "Sülfhidril köprüleri, karbonil grupları eklenmesi ve proteolitik yıkım yetersizliği",
        "badge": "Protein Oksidasyonu",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "ROS'un ikinci ana hedefi hücresel proteinlerdir. Serbest radikaller proteinlerin kritik amino asit "
            "yan zincirlerine (özellikle sistein ve metiyonin) saldırır. Sisteinlerin -SH grupları oksitlenerek anormal "
            "disülfit bağları oluşturur; polipeptit zincirleri çapraz bağlanarak üçüncül konformasyonunu ve enzimatik "
            "kataliz yeteneğini tamamen kaybeder.\n\n"
            "> [YÜKSEK VERİM] Prolin, lizin ve arginin gibi amino asitlerin oksidasyonuyla proteinlere 'karbonil grupları' "
            "(protein karbonilasyonu) eklenir; karbonillenmiş proteinler hücresel yaşlanmanın en güvenilir kan belirtecidir.\n\n"
            "Bu okside proteinler zamanla kümelenir, 26S proteazomunun giriş kanalını tıkar ve hücre içi proteostazın "
            "çökmesine zemin hazırlar."
        ),
        "medicalTerms": [
            {"term": "Protein Karbonilasyonu", "explanation": "ROS saldırısıyla protein amino asit yan zincirlerine aldehit/keton karbonil gruplarının eklenmesidir."},
            {"term": "Disülfit Çapraz Bağlanması", "explanation": "Oksidasyon sonucu sisteinlerin anormal kovalent bağlarla proteini katlanamaz hale getirmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Protein karbonilasyonu doku oksidatif hasarının en stabil biyobelirtecidir.",
            "📌 [SINAV SPOTU] Oksitlenmiş protein agregatları proteazom sistemini tıkayarak ER stresini tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Konformasyon İflası", "desc": "Anormal disülfit bağları enzimleri inaktive eder.", "isKey": True},
                {"title": "Proteazom Blokajı", "desc": "Karbonilli agregatlar proteolitik yıkım makinelerini bozar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Serbest radikal hasarı sonucu protein yan zincirlerine karbonil grupları eklenmesi hücresel protein oksidasyonunun göstergesidir.",
                "karbonil",
                "Oksitlenmiş proteinlerde saptanan aldehit/keton grubu"
            ),
            make_active_recall(
                "Oksidasyona uğramış hatalı proteinlerin hücre içi proteazom sistemi tarafından eritilememesinin yarattığı tehlike nedir?",
                "Agregatların proteazom girişini tıkaması, hücre içi protein temizliğini felç etmesi ve toksik ER stresini tetiklemesidir."
            )
        ]
    })

    # ADIM 27
    slides.append({
        "slideNumber": 27,
        "title": "ROS'un Hedefleri 3: DNA Oksidasyonu (8-Okso-Guanin) ve Mutajenez",
        "subtitle": "Guanin bazının hidroksilasyonu, G:C'den T:A'ya transversiyon ve mitokondriyal genom",
        "badge": "DNA Oksidasyonu",
        "badgeColor": "red",
        "synthesisNarrative": (
            "ROS'un üçüncü ve en tehlikeli hedefi nükleer ve mitokondriyal DNA'dır. DNA bazları arasında oksidasyona "
            "en duyarlı olanı guanindir. Hidroksil radikali guaninin 8. karbonuna saldırarak '8-hidroksi-2'-deoksiguanozin' "
            "(8-OHdG veya 8-okso-guanin) lezyonunu oluşturur.\n\n"
            "> [SINAV SPOTU] 8-okso-guanin replikasyon sırasında sitozin yerine yanlışlıkla adenin ile baz eşleşmesi yapar; "
            "bu durum G:C baz çiftinin T:A çiftine dönüştüğü 'transversiyon mutasyonlarına' yol açar.\n\n"
            "Mitokondriyal DNA (mtDNA), koruyucu histon proteinlerinden yoksun olduğu ve ROS kaynağının hemen bitişiğinde "
            "yer aldığı için nükleer DNA'ya göre 10-20 kat daha fazla 8-OHdG hasarına uğrar."
        ),
        "medicalTerms": [
            {"term": "8-Okso-Guanin (8-OHdG)", "explanation": "ROS saldırısıyla guaninin oksitlenmesi sonucu oluşan ve transversiyon mutasyonu yapan lezyondur."},
            {"term": "Transversiyon Mutasyonu", "explanation": "Bir pürin bazının primidine (veya tersi) dönüşmesiyle giden somatik DNA hatasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] 8-OHdG (8-okso-guanin) oksidatif DNA hasarının altın standart laboratuvar belirtecidir.",
            "📌 [SINAV SPOTU] Mitokondriyal DNA histonsuz olduğu için oksidatif hasara nükleer DNA'dan 10-20 kat daha duyarlıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Guanin Oksidasyonu", "desc": "8-oksoG oluşumu ve adeninle hatalı baz eşleşmesi.", "isKey": True},
                {"title": "Mitokondriyal Hassasiyet", "desc": "Histon koruması yok, tamir enzimi zayıf, hasar çok yüksek.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Serbest oksijen radikallerinin DNA molekülüne saldırısı sonucu en sık hasarlanan baz ve oksidatif DNA hasarının tayininde biyobelirteç olarak kullanılan modifiye nükleozid hangisidir?",
                {
                    "A": "Metilsitozin",
                    "B": "8-Hidroksi-2'-deoksiguanozin (8-OHdG / 8-okso-guanin)",
                    "C": "Timin dimeri",
                    "D": "Urasil",
                    "E": "Hipoksantin"
                },
                "B",
                {
                    "A": "Metilsitozin epigenetik metilasyon ürünüdür.",
                    "B": "Doğru! Guanin oksidasyonuyla oluşan 8-OHdG oksidatif DNA hasarının klasik belirtecidir.",
                    "C": "Timin dimeri UV radyasyon lezyonudur.",
                    "D": "Urasil sitozin deaminasyon ürünüdür.",
                    "E": "Hipoksantin adenin deaminasyon ürünüdür."
                }
            ),
            make_cloze(
                "Oksidatif DNA hasarının laboratuvarda tespitinde en sık ölçülen modifiye baz 8-okso-guanin molekülüdür.",
                "8-okso-guanin",
                "Guaninin hidroksilasyonuyla oluşan oksidatif mutajenik lezyon"
            )
        ]
    })

    # ADIM 28
    slides.append({
        "slideNumber": 28,
        "title": "Serbest Radikal Yaşlanma Teorisi (Harman Teorisi) ve Kısır Döngü",
        "subtitle": "Denham Harman'ın 1956 hipotezi, mitokondriyal kaçaklar ve kümülatif doku erozyonu",
        "badge": "Harman Teorisi",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "1956 yılında Denham Harman tarafından ortaya atılan 'Serbest Radikal Yaşlanma Teorisi' (Free Radical Theory of "
            "Aging), yaşlanmanın temel motorunun aerobik metabolizma sırasında kaçınılmaz olarak üretilen ROS'ların "
            "dokularda yarattığı kümülatif hasar olduğunu öne sürer. 1970'lerde teori 'Mitokondriyal Yaşlanma Teorisi' "
            "olarak rafine edilmiştir.\n\n"
            "> [SINAV SPOTU] Teoriye göre mitokondriden kaçan ROS mitokondriyal DNA'yı (mtDNA) vurur; mutant mtDNA "
            "solunum zincirini bozar; bozuk zincir daha fazla ROS üretir ve ölümcül bir kısır döngü kurulur.\n\n"
            "Her ne kadar tek başına tüm yaşlanmayı açıklamaya yetmese de, mitokondriyal hasar döngüsü yaşlanmanın en "
            "güçlü bileşenlerinden biri olarak kabul edilir."
        ),
        "medicalTerms": [
            {"term": "Harman Yaşlanma Teorisi", "explanation": "Yaşlanmanın hücresel metabolizmada biriken serbest radikal hasarından kaynaklandığını savunan teoridir."},
            {"term": "Mitokondriyal Kısır Döngü", "explanation": "ROS'un mtDNA'yı vurması, bunun solunumu bozarak daha fazla ROS üretmesi döngüsüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Denham Harman serbest radikal yaşlanma teorisinin kurucusudur.",
            "📌 [SINAV SPOTU] Mitokondriyal ROS üretimi ve mtDNA hasarı birbirini besleyen bir kısır döngüdür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Temel Hipotez", "desc": "Aerobik solunumun bedeli kümülatif oksidatif doku aşınmasıdır.", "isKey": True},
                {"title": "Mitokondri Sarmalı", "desc": "Bozuk solunum kompleksi daha çok kaçak elektron ve ROS saçar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Mitokondriyal Serbest Radikal Kısır Döngüsü",
                [
                    "1. Bazal Kaçak: Normal solunum sırasında az miktarda süperoksit üretilir.",
                    "2. mtDNA Mutasyonu: Korunmasız mitokondri DNA'sında 8-OHdG ve delesyonlar birikir.",
                    "3. Bozuk Solunum Kompleksi: Hatalı solunum enzimleri elektronları düzgün aktaramaz.",
                    "4. Şiddetlenen Elektron Kaçağı: Mitokondri devasa miktarda kaçak ROS üretmeye başlar.",
                    "5. Hücre Enerji İflası: ATP üretimi çöker, hücre senesens veya nekroza sürüklenir."
                ]
            ),
            make_cloze(
                "Yaşlanmanın hücresel metabolizmada biriken serbest radikal hasarlarından kaynaklandığını öne süren teori Harman teorisi olarak bilinir.",
                "Harman teorisi",
                "Serbest radikal yaşlanma teorisinin kurucusunun adı"
            )
        ]
    })

    # ADIM 29 - CHECKPOINT 3
    slides.append({
        "slideNumber": 29,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] ROS, Oksidatif Stres ve Antioksidan Savunma",
        "subtitle": "Süperoksit, hidroksil, SOD, katalaz, GPX, MDA ve 8-OHdG'nin büyük sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 3,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında oksidatif stres biyolojisini ve savunma kalkanlarını özetliyoruz. 1) Başlıca ROS: "
            "Süperoksit (O2•-), H2O2 ve en reaktif/yıkıcı olan hidroksil radikali (•OH). 2) Kaynaklar: Mitokondriyal Kompleks "
            "I/III kaçakları ve lökosit NADPH oksidazı (solunum patlaması). 3) Enzimatik kalkanlar: SOD (süperoksiti "
            "H2O2 yapar; mitokondride Mn, sitozolde Cu/Zn), Katalaz (peroksizomda H2O2'yi suya yıkar), Glutatyon "
            "peroksidaz (selenyum bağımlı, GSH kullanır). 4) Non-enzimatik: Vitamin E (membran lipidini korur), "
            "Vitamin C (Vitamin E'yi rejenere eder). 5) Hücresel hasar imzaları: Membranda malondialdehit (MDA) ve lipofusin; "
            "proteinde karbonilasyon; DNA'da 8-okso-guanin (8-OHdG).\n\n"
            "> [KLİNİK İPUCU] Sınavda en reaktif radikal •OH, selenyumlu enzim GPX, DNA oksidasyon belirteci 8-OHdG'dir.\n\n"
            "Aşağıdaki 3 akıl kartını hafızanıza sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Oksidatif Stres", "explanation": "ROS üretimi ile antioksidan savunma kapasitesi arasındaki dengenin hasar lehine bozulmasıdır."},
            {"term": "8-OHdG", "explanation": "Oksidatif DNA hasarının idrar ve dokuda ölçülen en hassas biyobelirtecidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] En reaktif ROS = Hidroksil radikali (•OH).",
            "📌 [SINAV SPOTU] Glutatyon peroksidaz selenyum bağımlıdır; Katalaz peroksizomdadır.",
            "📌 [SINAV SPOTU] DNA'da 8-OHdG, lipitte MDA, proteinde karbonilasyon oksidatif hasarı gösterir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Radikal Basamakları", "desc": "O2 -> O2•- -> H2O2 -> •OH (en toksik).", "isKey": True},
                {"title": "Enzim Üçlüsü", "desc": "SOD, Katalaz ve Selenyumlu Glutatyon Peroksidaz.", "isKey": True},
                {"title": "Hasar İzleri", "desc": "Lipofusin, malondialdehit ve 8-okso-guanin.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-08-fc-07",
                "Biyolojik dokularda üretilen serbest radikaller arasında hücre zarlarına ve DNA'ya en hızlı ve en yıkıcı zararı veren tür hangisidir?",
                "Fenton reaksiyonu sonucu demir kataliziyle oluşan hidroksil radikalidir (•OH).",
                "Biyolojik sistemlerdeki en reaktif serbest oksijen radikali"
            ),
            make_flashcard(
                "k1-08-fc-08",
                "Glutatyon peroksidaz (GPX) enziminin katalitik fonksiyonunu yerine getirebilmesi için hangi mineral kofaktörüne ihtiyacı vardır?",
                "Selenyum (Se) mineraline ihtiyacı vardır (aktif merkezinde selenosistein amino asidi bulunur).",
                "Glutatyon peroksidaz enzim kofaktörü"
            ),
            make_flashcard(
                "k1-08-fc-09",
                "Serbest radikallerin DNA molekülüne saldırması sonucu oluşan ve kanda/idrarda oksidatif DNA hasarını gösteren altın standart metabolit nedir?",
                "8-Hidroksi-2'-deoksiguanozin (8-OHdG veya 8-okso-guanin) molekülüdür.",
                "Oksidatif DNA hasarının primer laboratuvar belirteci"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Peroksizomlarda hidrojen peroksiti su ve moleküler oksijene parçalayan antioksidan enzim katalaz enzimidir.",
                "katalaz",
                "Peroksizomun karakteristik hidrojen peroksit yıkıcı enzimi"
            )
        ]
    })

    # ADIM 30
    slides.append({
        "slideNumber": 30,
        "title": "Antioksidan Tedavilerin Yaşlanmadaki Sınırları ve Klinik Sentez",
        "subtitle": "Klinik çalışma paradoksları, ROS'un fizyolojik sinyal rolü ve hormezis ilkesi",
        "badge": "Antioksidan Paradoks",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Serbest radikal yaşlanma teorisi ilk ortaya atıldığında, yüksek doz antioksidan vitamin takviyelerinin "
            "(C, E vitamini, beta-karoten) insan ömrünü uzatacağı ve hastalıkları önleyeceği düşünülmüştü. Ancak yüz "
            "binlerce kişi üzerinde yapılan geniş çaplı randomize klinik çalışmalar büyük bir hayal kırıklığı yarattı: "
            "Aşırı antioksidan kullanımı ömrü uzatmamış, bazı kanser türlerinde mortaliteyi paradoksal olarak artırmıştır.\n\n"
            "> [KLİNİK İPUCU] Bunun nedeni ROS'ların yalnız hasar ajanı değil; hücre içi sinyal iletimi, lökosit immün "
            "savunması ve mitoz kontrolünde fizyolojik 'ikincil haberci' olarak zorunlu görev yapmalarıdır.\n\n"
            "Ayrıca hafif düzeydeki stres (egzersiz kaynaklı ROS), 'hormezis' yoluyla endojen savunma genlerini (NRF2 "
            "yolağı) uyararak hücreyi daha dayanıklı kılar."
        ),
        "medicalTerms": [
            {"term": "Hormezis", "explanation": "Düşük dozda zararlı olan bir stres faktörünün (hafif ROS, egzersiz) hücresel adaptasyonu uyararak fayda sağlamasıdır."},
            {"term": "NRF2 Transkripsiyon Faktörü", "explanation": "Hafif oksidatif stresle çekirdeğe geçip yüzlerce antioksidan geni açan ana koruyucu faktördür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yüksek doz yapay antioksidan takviyeleri insan ömrünü uzatmaz; fizyolojik ROS sinyallerini bozar.",
            "📌 [SINAV SPOTU] Egzersiz, hormezis yoluyla NRF2 faktörünü uyararak endojen antioksidan kapasiteyi artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Antioksidan Paradoksu", "desc": "Megadoz vitaminler doğal immüniteyi ve redoks dengesini sekteye uğratır.", "isKey": True},
                {"title": "Hormezis İlkesi", "desc": "Kontrollü hafif stres hücresel dayanıklılığı ve antioksidan genleri kamçılar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "60 yaşında sağlıklı bir birey internet reklamlarında gördüğü yüksek doz Vitamin E ve beta-karoten haplarını günde 5 katı dozda almaya başladığını söylüyor. Hekimin bu hastaya kanıta dayalı patofizyolojik açıklaması ne olmalıdır?",
                [
                    {
                        "text": "Megadoz antioksidanlar telomerazı sürekli açık tutarak tüm yaşlanmayı tamamen durdurur.",
                        "isCorrect": False,
                        "feedback": "Yanlış! Antioksidanlar telomerazı açmaz; kontrolsüz yüksek dozlar toksisite yaratabilir."
                    },
                    {
                        "text": "Yüksek doz yapay antioksidanların ömrü uzatmadığı kanıtlanmıştır; fizyolojik ROS sinyallerini bozabilir ve doğal beslenme önerilmelidir.",
                        "isCorrect": True,
                        "feedback": "Mükemmel! Geniş klinik çalışmalar yüksek doz antioksidanların ömrü uzatmadığını ve fizyolojik redoks dengesini bozduğunu göstermiştir."
                    }
                ]
            ),
            make_active_recall(
                "Egzersiz sırasında kasta geçici olarak artan hafif serbest radikallerin hücreye uzun vadede zarar yerine fayda sağlamasını açıklayan biyolojik ilke nedir?",
                "Hormezis ilkesidir (hafif stresin NRF2 transkripsiyon faktörünü uyararak hücrenin kendi endojen antioksidan enzimlerini artırmasıdır)."
            )
        ]
    })

    return slides
