"""
Section 5: Apoptozun İntrensek (Mitokondriyal) Yolağı ve Kaspaz Kaskadı (Slayt 41 - 50)
"""
from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-08-s41",
        "title": "Senesens vs Apoptoz: Hücresel Kaderin Hakemliği",
        "subtitle": "DNA hasarının şiddetine göre hücrenin hayatta kalma veya intihar kararı",
        "badge": "Hücre Kaderi",
        "badgeColor": "indigo",
        "coreContent": {
            "text": (
                "Hücre ağır stres, telomer kısalması veya DNA hasarıyla karşılaştığında iki temel yoldan birini seçer:\n\n"
                "1. **Senesens:** Hasar orta derecelidir; hücre bölünmeyi kalıcı olarak durdurur ancak hayatta kalmaya devam eder.\n"
                "2. **Apoptoz:** Hasar hücrenin tolere edemeyeceği kadar ağırdır veya malign transformasyon riski taşır; "
                "hücre sessizce kendini imha eden ==programlı hücre ölümünü== başlatır.\n\n"
                "> Her iki yolun da merkezinde **p53** tümör baskılayıcı proteini yer alır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Ağır ve onarılamaz DNA hasarı varlığında hücrenin inflamasyon yaratmadan kendini imha etmesine programlı hücre ölümü denir.",
                "programlı hücre ölümü",
                "Apoptoz sürecinin biyolojik tanımı"
            ),
            make_active_recall(
                "Hücrenin senesense mi yoksa apoptoza mı gideceğine karar veren en kritik faktörler nelerdir?",
                "DNA hasarının ve oksidatif stresin şiddeti, hücre tipi ve p53'ün aktive ettiği pro-apoptotik proteinlerin (PUMA, NOXA, BAX) eşik konsantrasyonudur."
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-08-s42",
        "title": "BCL-2 Protein Ailesi: Mitokondriyal Dış Zar Bekçileri",
        "subtitle": "Anti-apoptotik kalkanlar ile pro-apoptotik öldürücüler arasındaki denge",
        "badge": "Onkogenetik",
        "badgeColor": "blue",
        "coreContent": {
            "text": (
                "Apoptozun intrensek (mitokondriyal) yolağı **BCL-2 ailesi proteinleri** arasındaki hassas dengeyle yönetilir.\n\n"
                "Bu aile üç alt gruptan oluşur:\n"
                "- **Anti-Apoptotikler:** BCL-2, BCL-XL, MCL-1. Mitokondri dış zarında bekçilik yaparak zarı kapalı tutarlar.\n"
                "- **Pro-Apoptotik Efektörler:** BAX ve BAK. Zarda gözenek açarak sitokrom c'yi salarlar.\n"
                "- **BH3-Only Sensörler:** BIM, PUMA, NOXA, BAD, BID. Hasarı algılayıp anti-apoptotikleri etkisizleştirirler."
            )
        },
        "interactiveElements": [
            make_table(
                ["Grup Adı", "Örnek Moleküller", "Hücresel Görevi"],
                [
                    [("Anti-Apoptotik Koruyucular", False, ""), ("BCL-2, BCL-XL, MCL-1", False, ""), ("Dış zar bütünlüğünü koruyarak sitokrom sızıntısını engellemek", True, "Hücre intiharını bloke eden koruyucu kalkan")],
                    [("Pro-Apoptotik Efektörler", False, ""), ("BAX, BAK", False, ""), ("Zarda oligomerik gözenekler açarak MOMP oluşturmak", True, "Sitokrom sızıntısını başlatan kanal oluşturucu rol")],
                    [("BH3-Only Sensörler", False, ""), ("BIM, PUMA, NOXA, BAD", False, ""), ("Stresi algılayıp koruyucu kalkanları nötralize etmek", True, "Hasar durumunda apoptotik blokajı kaldıran sensör")]
                ]
            ),
            make_cloze(
                "Mitokondri dış zarında bekçilik yaparak apoptozu engelleyen temel anti-apoptotik protein BCL-2 proteinidir.",
                "BCL-2",
                "Foliküler lenfomada t(14;18) translokasyonu ile aşırı eksprese olan onkogenik protein"
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-08-s43",
        "title": "BAX ve BAK: Mitokondriyal Dış Zarın Geçirgenleşmesi (MOMP)",
        "subtitle": "Oligomerizasyon, lipid gözenekleri ve geri dönüşsüz intihar kapısı",
        "badge": "Membran Biyofiziği",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "Hücre ölüm sinyali aldığında pro-apoptotik proteinler olan **BAX ve BAK** konformasyonel değişime uğrar.\n\n"
                "Mitokondri dış zarında bir araya gelerek oligomerik halkalar oluştururlar.\n\n"
                "Bu halkalar zarda devasa gözenekler açar; bu olaya **MOMP** (==Mitochondrial Outer Membrane Permeabilization==) denir.\n\n"
                "> MOMP oluştuktan sonra hücre için geri dönüş yoktur; mitokondriler arası boşluktaki öldürücü proteinler sitozole boşalır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Mitokondri dış zarında BAX ve BAK tarafından gözenek açılması olayına MOMP adı verilir.",
                "MOMP",
                "Mitochondrial outer membrane permeabilization kısaltması"
            ),
            make_causal_chain(
                "MOMP Oluşum ve Zar Delinme Basamakları",
                [
                    "1. Stres Algısı: Ağır DNA hasarı BH3-only proteinlerini serbest bırakır.",
                    "2. İnhibisyonun Kırılması: BCL-2 ve BCL-XL nötralize edilir.",
                    "3. BAX/BAK Aktivasyonu: BAX sitozolden mitokondri dış zarına transloke olur.",
                    "4. Oligomerizasyon: BAX ve BAK birleşerek zarda gözenek oluşturur.",
                    "5. Sızıntı: Sitokrom c ve Smac/DIABLO sitoplazmaya fışkırır."
                ]
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-08-s44",
        "title": "BH3-Only Sensörler: PUMA ve NOXA'nın p53 Kontrolü",
        "subtitle": "DNA hasarından mitokondriye haber taşıyan moleküler haberciler",
        "badge": "Genomik Bekçi",
        "badgeColor": "purple",
        "coreContent": {
            "text": (
                "p53 transkripsiyon faktörü ağır DNA hasarı saptadığında apoptozu başlatmak için özel BH3-only genleri aktive eder.\n\n"
                "Bunların başında ==PUMA== (p53 Upregulated Modulator of Apoptosis) ve ==NOXA== gelir.\n\n"
                "Sentezlenen PUMA ve NOXA, mitokondri zarındaki anti-apoptotik BCL-2 ve MCL-1'e sımsıkı bağlanarak onları kilitler.\n\n"
                "> Fren mekanizması kalktığı anda serbest kalan BAX ve BAK derhal zarı delerek apoptozu infaz eder."
            )
        },
        "interactiveElements": [
            make_cloze(
                "p53 tarafından transkripsiyonu doğrudan başlatılan güçlü pro-apoptotik BH3-only proteini PUMA molekülüdür.",
                "PUMA",
                "p53 upregulated modulator of apoptosis kısaltması"
            ),
            make_active_recall(
                "BH3-only proteinlerin (PUMA, NOXA, BIM) apoptozdaki temel görevi nedir?",
                "Anti-apoptotik BCL-2/MCL-1 proteinlerini kompetitif olarak bağlayıp etkisizleştirerek, pro-apoptotik efektörler olan BAX ve BAK'ın zarda serbestçe gözenek açmasını sağlamaktır."
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-08-s45",
        "title": "Sitokrom c Salınımı ve APAF-1 ile Birleşme",
        "subtitle": "Solunum elektron taşıyıcısından sitoplazmik ölüm sinyaline dönüşüm",
        "badge": "Hücresel Biyokimya",
        "badgeColor": "rose",
        "coreContent": {
            "text": (
                "**Sitokrom c**, normalde mitokondri iç zarı ile dış zarı arasındaki boşlukta elektron taşıyan küçük bir hemoproteindir.\n\n"
                "BAX/BAK gözeneklerinden sitozole sızdığı anda hücresel kimliği tamamen değişir; elektron taşıyıcılığından **ölüm tetiğine** dönüşür.\n\n"
                "Sitozolde **APAF-1** (Apoptotic Protease Activating Factor-1) adaptör proteini ile karşılaşır.\n\n"
                "> dATP/ATP varlığında sitokrom c APAF-1'e bağlanarak devasa bir heptamerik ölüm makinesinin montajını başlatır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Mitokondriden sitozole salınan sitokrom c APAF-1 proteini ile birleşerek apoptozom çarkını kurar.",
                "APAF-1",
                "Apoptotic protease activating factor-1 adaptör proteini"
            ),
            make_before_after(
                "Normal Mitokondriyal Sitokrom c ile Sitozolik Sitokrom c",
                "Normal Mitokondri İçinde",
                "Kompleks III'ten Kompleks IV'e elektron taşıyarak ATP sentezini destekleyen yaşamsal molekül.",
                "Sitozole Sızdığında",
                "APAF-1'i aktive ederek kaspaz kaskadını başlatan ve hücreyi imhaya sürükleyen ölüm sinyali."
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-08-s46",
        "title": "Apoptozom (Apoptosome): Kaspaz-9 Aktivasyon Çarkı",
        "subtitle": "Yedi kollu tekerlek kompleksi ve başlatıcı pro-kaspaz-9 kesimi",
        "badge": "Enzim Aktivasyonu",
        "badgeColor": "cyan",
        "coreContent": {
            "text": (
                "Yedi adet APAF-1, yedi adet sitokrom c ve dATP birleşerek tekerlek şeklinde **Apoptozom** kompleksini oluşturur.\n\n"
                "Apoptozomun merkezindeki CARD (Caspase Activation and Recruitment Domain) bölgeleri sitozoldeki **pro-kaspaz-9** moleküllerini toplar.\n\n"
                "Yakın komşuluğa gelen pro-kaspaz-9 monomerleri birbirini proteolitik olarak keserek aktif ==kaspaz-9== haline gelir.\n\n"
                "> Kaspaz-9, mitokondriyal (intrensek) apoptoz yolağının **başlatıcı kaspazıdır** (initiator caspase)."
            )
        },
        "interactiveElements": [
            make_cloze(
                "İntrensek mitokondriyal apoptoz yolağının temel başlatıcı kaspazı kaspaz-9 enzimidir.",
                "kaspaz-9",
                "Apoptozom tarafından aktive edilen initiator kaspaz"
            ),
            make_causal_chain(
                "Sitokrom c'den Kaspaz-9 Aktivasyonuna Zincir",
                [
                    "1. Zardan Çıkış: Sitokrom c BAX gözeneklerinden sitoplazmaya dökülür.",
                    "2. APAF-1 Bağlanması: Sitokrom c dATP varlığında APAF-1'e kenetlenir.",
                    "3. Tekerlek Kurulumu: 7'li APAF-1 oligomeri apoptozom çarkını inşa eder.",
                    "4. Prokaspaz Toplanması: Pro-kaspaz-9 CARD bölgeleriyle merkeze bağlanır.",
                    "5. Otolitik Kesim: Başlatıcı kaspaz-9 aktive olarak infazcıları kesmeye başlar."
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-08-s47",
        "title": "İnfazcı Kaspazlar (Kaspaz-3 ve Kaspaz-7): Hücrenin Yıkımı",
        "subtitle": "Hücre iskeletinin, laminanın ve nükleer proteinlerin koordineli parçalanması",
        "badge": "İnfaz Fazı",
        "badgeColor": "amber",
        "coreContent": {
            "text": (
                "Aktif kaspaz-9, sitoplazmada inaktif bekleyen **pro-kaspaz-3** ve **pro-kaspaz-7**'yi keserek aktive eder.\n\n"
                "**Kaspaz-3**, apoptozun ana infazcı kaspazıdır (executioner caspase):\n\n"
                "- Nükleer zarın **lamin** proteinlerini keserek çekirdek kılıfını yıkar.\n"
                "- Hücre iskeletini (aktin, tubulin) parçalayarak hücrenin küçülmesini ve büzüşmesini sağlar.\n"
                "- DNA tamir enzimi **PARP**'ı (Poli-ADP Riboz Polimeraz) parçalayarak gereksiz ATP tüketimini önler."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Hem intrensek hem ekstrensek apoptoz yolaklarının ortak ana infazcı kaspazı kaspaz-3 enzimidir.",
                "kaspaz-3",
                "Hücresel proteinleri parçalayan anahtar infazcı enzim"
            ),
            make_micro_quiz(
                "Apoptoz sürecinde hem nükleer laminayı parçalayarak çekirdeği dağıtan hem de hücre iskeletini kesen temel infazcı kaspaz hangisidir?",
                {
                    "A": "Kaspaz-8",
                    "B": "Kaspaz-9",
                    "C": "Kaspaz-3",
                    "D": "Kaspaz-1",
                    "E": "Kaspaz-12"
                },
                "C",
                {
                    "A": "Kaspaz-8 ekstrensek (ölüm reseptörü) yolunun başlatıcısıdır.",
                    "B": "Kaspaz-9 intrensek yolun başlatıcısıdır.",
                    "C": "Doğru cevap C'dir: Kaspaz-3 her iki yolun ortak ana yürütücü/infazcı (executioner) kaspazıdır.",
                    "D": "Kaspaz-1 piroptoz ve IL-1 aktivasyonunda görev alır.",
                    "E": "Kaspaz-12 ER stresinde rol oynar."
                }
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-08-s48",
        "title": "DNA Fragmantasyonu ve Apoptotik Cisimcikler",
        "subtitle": "CAD endonükleazı, 180-200 baz çiftlik merdiven deseni ve fagositoz sinyalleri",
        "badge": "Apoptotik Morfoloji",
        "badgeColor": "slate",
        "coreContent": {
            "text": (
                "Kaspaz-3, normalde inaktif olan **ICAD** (İnhibitor of CAD) proteinini parçalar.\n\n"
                "Serbest kalan **CAD** (Kaspazla Aktive Olan DNaz) enzimi çekirdeğe girerek DNA'yı nükleozomlar arasından keser.\n\n"
                "Jel elektroforezinde tipik ==180-200 baz çifti ve katları== merdiven deseni (DNA ladder) ortaya çıkar.\n\n"
                "Hücre zarı tomurcuklanarak organel içeren **apoptotik cisimcikler** oluşturur; zardaki **fosfatidilserin** dış yaprağa dönerek ('ye beni' sinyali) makrofajlarca sessizce yutulmasını sağlar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Apoptotik hücrelerin makrofajlar tarafından tanınıp inflamasyonsuz yutulmasını sağlayan dış zar fosfolipidi fosfatidilserin molekülüdür.",
                "fosfatidilserin",
                "Flipaz inhibisyonuyla dış tabakaya takla atan fagositoz belirteci"
            ),
            make_active_recall(
                "Apoptoz ile nekroz arasındaki jel elektroforezi DNA kesim paterni farkı nedir?",
                "Apoptozda nükleozomlar arası spesifik kesim nedeniyle düzenli 180-200 bç basamaklı merdiven (ladder) deseni oluşurken; nekrozda gelişigüzel sindirim sonucu yaygın leke (smear) deseni oluşur."
            )
        ]
    })

    # Slide 49 (CHECKPOINT 5)
    slides.append({
        "id": "k1-08-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] İntrensek Apoptoz ve Kaspaz Kaskadı",
        "subtitle": "Bölüm 5 BCL-2 Dengesi, BAX/BAK, Sitokrom c, Apoptozom ve Kaspazlar",
        "badge": "Checkpoint 5",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 5,
        "coreContent": {
            "text": (
                "Beşinci kontrol noktasında intrensek apoptoz kaskadını özetliyoruz:\n\n"
                "1. **BCL-2 Ailesi:** Anti-apoptotik (BCL-2, BCL-XL) vs Pro-apoptotik (BAX, BAK) vs Sensörler (PUMA, BIM).\n"
                "2. **MOMP:** BAX ve BAK dış zarda gözenek açarak sitokrom c'yi sitozole fırlatır.\n"
                "3. **Apoptozom:** 7 APAF-1 + 7 Sitokrom c + dATP = Başlatıcı kaspaz-9 aktivasyonu.\n"
                "4. **İnfaz:** Kaspaz-3 hücre iskeletini ve laminayı yıkar, CAD endonükleazı DNA'yı merdiven yapar.\n"
                "5. **Fagositoz:** Zarda fosfatidilserin dışarı takla atar; nötrofil/inflamasyon çekmeden sessizce temizlenir."
            )
        },
        "interactiveElements": [
            make_micro_quiz(
                "İntrensek (mitokondriyal) apoptoz yolağında mitokondri dış zarı geçirgenliğini engelleyerek hücreyi hayatta tutan anahtar protein hangisidir?",
                {
                    "A": "BAX",
                    "B": "BAK",
                    "C": "BCL-2",
                    "D": "Kaspaz-9",
                    "E": "APAF-1"
                },
                "C",
                {
                    "A": "BAX zarda gözenek açar (ölümcül).",
                    "B": "BAK zarda gözenek açar (ölümcül).",
                    "C": "Doğru cevap C'dir: BCL-2 ana anti-apoptotik koruyucudur ve zarı kapalı tutar.",
                    "D": "Kaspaz-9 başlatıcı proteazdır.",
                    "E": "APAF-1 apoptozom bileşenidir."
                }
            ),
            make_active_recall(
                "Neden apoptoz çevre dokularda inflamasyon yapmazken nekroz şiddetli inflamasyona yol açar?",
                "Çünkü apoptozda hücre içi enzimler dışarı sızmadan membran kaplı apoptotik cisimcikler halinde fosfatidilserin sinyaliyle makrofajlarca hızla yutulur; nekrozda ise plazma zarı parçalanır ve sitoplazmik içerik dışarı saçılarak inflamasyonu tetikler."
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-08-s50",
        "title": "Senesent Hücrelerde Apoptotik Direnç ve Senolitik Mantığı",
        "subtitle": "Senesent hücrelerin BCL-2 aşırı ekspresyonu ile ölümden kaçması",
        "badge": "Hedefli Tedavi",
        "badgeColor": "emerald",
        "coreContent": {
            "text": (
                "Senesent hücreler aşırı derecede hasarlı olmalarına rağmen intrensek apoptoza gitmezler.\n\n"
                "Bunun nedeni hücresel yaşlanma sırasında **BCL-2 ve BCL-XL** düzeylerini anormal yükselterek ==apoptoza dirençli== hale gelmeleridir (**SCAPs** / Senescent Cell Anti-Apoptotic Pathways).\n\n"
                "Güncel farmakolojide **Senolitik İlaçlar** (örneğin BCL-2/BCL-XL inhibitörü **Navitoclax**), senesent hücrelerin bu koruyucu kalkanını kırarak "
                "onları seçici biçimde apoptoza sürükler ve dokuları toksik yaşlı hücrelerden temizler."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Senesent hücreleri seçici olarak apoptoza uğratıp dokudan temizleyen modern ilaç sınıfına senolitik ilaçlar denir.",
                "senolitik ilaçlar",
                "Yaşlı hücreleri öldüren anti-aging ajanlar sınıfı"
            ),
            make_branching_logic(
                "Laboratuvar araştırmasında yaşlı farelerin dokularında biriken senesent hücrelerin kronik inflamasyon (SASP) yaptığı saptanıyor. Bu dokuları gençleştirmek için BCL-2 yolağına yönelik farmakolojik strateji ne olmalıdır?",
                [
                    {"text": "BCL-2 sentezini artıran büyüme faktörleri vererek hücreleri korumak", "isCorrect": False, "feedback": "BCL-2'yi artırmak toksik senesent hücrelerin ömrünü daha da uzatır."},
                    {"text": "BCL-2 inhibitörü (Navitoclax) gibi senolitik bir ajan kullanarak senesent hücrelerin apoptotik direncini kırmak ve onları ölüme sevk etmek", "isCorrect": True, "feedback": "Mükemmel farmakolojik hedefleme! Senolitikler BCL-2 kalkanını kırarak yaşlı hücreleri apoptozla temizler ve doku fonksiyonunu geri kazandırır."},
                    {"text": "Hücre zarına kalsiyum pompalayarak tüm hücreleri nekroza uğratmak", "isCorrect": False, "feedback": "Masif nekroz ve inflamatuvar yıkım yapar."}
                ]
            )
        ]
    })

    return slides
