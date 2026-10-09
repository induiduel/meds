"""
Bölüm 1: Hücresel Yaşlanma Kavramı, Evrimsel ve Moleküler Temeller
Adımlar: 1 - 10
Checkpoint: Adım 9 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # ADIM 1
    slides.append({
        "slideNumber": 1,
        "title": "Hücresel Yaşlanma Tanımı ve Biyolojik Boyutları",
        "subtitle": "Çoğalma kapasitesinde ve fonksiyonel rezervde zamanla ortaya çıkan ilerleyici azalma",
        "badge": "Yaşlanma Tanımı",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Hücresel yaşlanma (cellular aging), hücrelerin replikatif çoğalma kapasitelerinde ve metabolik-fonksiyonel "
            "aktivitelerinde zaman içinde ortaya çıkan, geri dönüşsüz ve ilerleyici bir azalma sürecidir. Bu süreç "
            "yalnızca tek tek hücreler düzeyinde kalmaz; doku rejenerasyonunun yavaşlamasına, organ fonksiyonel rezervinin "
            "çökmesine ve nihayetinde tüm organizma düzeyinde homeostazın bozulmasına yol açar.\n\n"
            "> [TEMEL İLKE] Hücresel yaşlanma, hücrelerin dış veya iç stres faktörlerine karşı gösterdiği adaptif bir "
            "yanıt olarak başlar; kontrolsüz mutasyon birikimini ve tümörijenezi önlemek için hücre döngüsünü kalıcı olarak durdurur.\n\n"
            "Ancak senesent hücrelerin dokularda birikmesi, doku mimarisini bozar ve kronik dejeneratif hastalıklara zemin hazırlar."
        ),
        "medicalTerms": [
            {"term": "Hücresel Yaşlanma", "explanation": "Hücrelerin bölünme kapasitesini kalıcı olarak kaybedip fonksiyonel aktivitesinin gerilemesidir."},
            {"term": "Homeostaz", "explanation": "Hücre, doku ve organizmanın iç ortam parametrelerini kararlı dengede tutabilme yeteneğidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücresel yaşlanma çoğalma kapasitesi ve fonksiyonel aktivitenin ilerleyici azalmasıdır.",
            "📌 [SINAV SPOTU] Yaşlanma hücresel boyuttan tüm organizma düzeyine kadar basamaklı bir etki yaratır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İlerleyici Kayıp", "desc": "Mitotik kapasite ve fonksiyonel yanıtlar zamanla azalır.", "isKey": True},
                {"title": "Doku İflası", "desc": "Rejenerasyon yetersizliği kronik organ yetmezliklerine yol açar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hücrelerin çoğalma kapasitesinde ve fonksiyonel aktivitesinde zamanla ortaya çıkan ilerleyici azalmaya hücresel yaşlanma adı verilir.",
                "hücresel yaşlanma",
                "Mitotik ve metabolik kapasitenin zamanla gerilemesi süreci"
            ),
            make_active_recall(
                "Hücresel yaşlanma sürecinin doku ve organ düzeyindeki nihai biyolojik sonucu nedir?",
                "Doku onarım ve yenilenme kapasitesinin düşmesi, organ fonksiyonel rezervinin azalması ve homeostazın bozulmasıdır."
            )
        ]
    })

    # ADIM 2
    slides.append({
        "slideNumber": 2,
        "title": "Yaşlanmanın Klinik Önemi: Kronik Hastalıkların Bağımsız Risk Faktörü",
        "subtitle": "Kanserler, kardiyovasküler patolojiler ve nörodejenerasyon epidemiyolojisi",
        "badge": "Klinik Önem",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Modern tıpta kronolojik yaş, insan morbidite ve mortalitesinin en güçlü bağımsız risk faktörüdür. Yaş "
            "ilerledikçe neredeyse tüm büyük kronik hastalıkların insidansı eksponansiyel olarak artar: 1) Malign kanserler "
            "(kümülatif mutasyonlar nedeniyle), 2) Ateroskleroz, iskemik kalp hastalığı ve inme (endotel senesensi nedeniyle), "
            "3) Nörodejeneratif hastalıklar (Alzheimer, Parkinson) ve 4) Metabolik disfonksiyon (Tip 2 diyabet).\n\n"
            "> [KLİNİK İPUCU] Küresel nüfusun hızla yaşlanması kronik hastalık yükünü tarihin en yüksek seviyesine çıkarmıştır; "
            "yaşlanma biyolojisini aydınlatmak koruyucu tıbbın en temel önceliğidir.\n\n"
            "Patoloji, tüm bu hastalıkların kökeninde yer alan ortak hücresel yaşlanma hasarlarını inceler."
        ),
        "medicalTerms": [
            {"term": "Bağımsız Risk Faktörü", "explanation": "Diğer klinik değişkenlerden bağımsız olarak hastalık gelişme olasılığını doğrudan artıran faktördür."},
            {"term": "Nörodejenerasyon", "explanation": "Nöronların ilerleyici fonksiyon kaybı ve ölümüyle seyreden santral sinir sistemi hastalıklarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaş, kanser ve ateroskleroz için en güçlü bağımsız risk faktörüdür.",
            "📌 [SINAV SPOTU] Toplum yaşlandıkça dejeneratif ve neoplastik hastalık yükü hızla artar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Maligniteler", "desc": "On yıllar boyunca biriken genomik hasar ve onkojenik mutasyonlar.", "isKey": True},
                {"title": "Vasküler Risk", "desc": "Arter duvarında sertleşme, elastik lif yıkımı ve aterom oluşumu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "İleri yaş; kanserler, ateroskleroz ve Alzheimer gibi nörodejeneratif hastalıklar için en güçlü bağımsız risk faktörüdür.",
                "bağımsız risk faktörü",
                "Hastalık olasılığını doğrudan artıran temel klinik belirteç"
            ),
            make_active_recall(
                "İleri yaşın kanser gelişiminde bağımsız bir risk faktörü olmasının temel hücresel gerekçesi nedir?",
                "On yıllar boyunca DNA hasarlarının, somatik mutasyonların ve epigenetik bozuklukların hücre genomunda kümülatif olarak birikmesidir."
            )
        ]
    })

    # ADIM 3
    slides.append({
        "slideNumber": 3,
        "title": "Yaşlanma Basit Bir \"Zaman Geçişi\" Değildir",
        "subtitle": "Genetik kontrol, modüle edilebilir sinyal ağları ve evrimsel programlanma",
        "badge": "Moleküler Paradigma",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Tıp ve biyoloji dünyasında uzun yıllar boyunca yaşlanmanın kaçınılmaz bir mekanik aşınma, 'enerjinin tükenmesi' "
            "veya basit bir kum saati akışı olduğu düşünülmüştür. Ancak son çeyrek asırdaki moleküler genetik keşifler bu "
            "dogmayı tamamen yıkmıştır. Mayadan insana kadar tüm ökaryotlarda yaşlanma, özgül genler ve sinyal yolları "
            "tarafından son derece sıkı şekilde regüle edilen aktif bir biyolojik süreçtir.\n\n"
            "> [YÜKSEK VERİM] Deneysel hayvan modellerinde tek bir gen mutasyonu (örneğin IGF-1 reseptör mutasyonu) veya "
            "çevresel müdahale (kalori kısıtlaması) yaşam süresini 2-3 katına kadar uzatabilmektedir.\n\n"
            "Bu durum, hücresel yaşlanmanın hızının genetik ve farmakolojik olarak manipüle edilebileceğini kanıtlar."
        ),
        "medicalTerms": [
            {"term": "Programlı Yaşlanma", "explanation": "Hücresel ömür ve fonksiyon kaybının genetik sinyal yolaklarınca aktif kontrol edilmesidir."},
            {"term": "Ömür Modülasyonu", "explanation": "Metabolik veya farmakolojik müdahalelerle yaşam süresinin ve sağkalımın uzatılabilmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaşlanma pasif bir yıpranma değil, genetik yollarla kontrol edilen aktif bir süreçtir.",
            "📌 [SINAV SPOTU] Sinyal yolaklarının modülasyonu hayvan modellerinde ömrü belirgin şekilde uzatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eski Teori", "desc": "Pasif aşınma ve enerji tükenmesi (artık geçersiz).", "isKey": True},
                {"title": "Modern Paradigma", "desc": "Genetik programlar, besin sensörleri ve DNA onarım ağları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Pasif Aşınma Teorisi vs Genetik Düzenlenme Paradigması",
                "Pasif Aşınma Teorisi (Eski)",
                "Yaşlanmanın sadece zamanın geçişiyle hücresel enerjinin tükenmesi ve kaçınılmaz mekanik bozulma olduğunu savunur.",
                "Genetik Düzenlenme Paradigması (Modern)",
                "Yaşlanmanın IGF-1, mTOR ve sirtuinler gibi özgül genetik sinyal yolaklarıyla denetlenen, müdahale edilebilir bir süreç olduğunu belgeler."
            ),
            make_active_recall(
                "Modern moleküler biyolojinin hücresel yaşlanma kavramına getirdiği en devrimci bakış açısı nedir?",
                "Yaşlanmanın pasif bir zaman geçişi değil; özgül genler, besin sensörleri ve onarım sinyal ağları tarafından aktif olarak düzenlenen ve yavaşlatılabilen bir süreç olduğudur."
            )
        ]
    })

    # ADIM 4
    slides.append({
        "slideNumber": 4,
        "title": "Yaşlanmayı Yöneten Başlıca 6 Moleküler Mekanizmaya Kuşbakışı",
        "subtitle": "DNA hasarı, replikatif senesens, proteostaz, mitokondri, besin algısı ve inflamasyon",
        "badge": "6 Temel Mekanizma",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Robbins Patoloji sınıflamasına göre hücresel yaşlanma, birbiriyle sürekli etkileşim halinde olan 6 temel "
            "moleküler mekanizmanın ortak çıktısıdır: 1) DNA hasarı ve onarım yetersizliği, 2) Hücre çoğalmasının azalması "
            "(telomer kısalması ve replikatif yaşlanma), 3) Protein homeostazında (proteostaz) bozulma, 4) Mitokondriyal "
            "disfonksiyon ve aşırı ROS birikimi, 5) Besin algılama sinyal yollarında değişiklikler (IGF-1 / mTOR ekseni) "
            "ve 6) Kalıcı düşük dereceli kronik inflamasyon ('inflammaging').\n\n"
            "> [TEMEL İLKE] Bu 6 mekanizma izole çalışmaz; örneğin DNA hasarı p53'ü aktive ederek mitokondriyi vurur, "
            "mitokondriden sızan ROS proteostazı bozar ve açığa çıkan artıklar inflamasyonu besler.\n\n"
            "Bu zincirleme kısır döngü dokunun fonksiyonel çöküşünü hızlandırır."
        ),
        "medicalTerms": [
            {"term": "Hücresel Senesens", "explanation": "Hücrenin metabolik olarak canlı kalırken bölünme döngüsünden kalıcı olarak çıkmasıdır."},
            {"term": "İnflammaging", "explanation": "Yaşlanmayla birlikte dokularda gelişen düşük dereceli, steril ve kalıcı kronik inflamasyondur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaşlanmanın 6 temel mekanizması vardır: DNA hasarı, telomer, proteostaz, mitokondri, IGF/mTOR ve inflamasyon.",
            "📌 [SINAV SPOTU] Mekanizmalar birbirini tetikleyen bir hasar döngüsü halinde çalışır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Genomik ve Telomerik", "desc": "DNA mutasyonları birikimi ve kromozom uçlarının erimesi.", "isKey": True},
                {"title": "Metabolik ve Proteomik", "desc": "Mitokondriyal enerji düşüşü, ROS artışı ve hatalı protein agregatları.", "isKey": True},
                {"title": "Sinyal ve İnflamasyon", "desc": "mTOR hiperaktivitesi ve düşük dereceli sürekli doku yangısı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Yaşlanma Mekanizması", "Temel Moleküler Olay", "Hücresel / Dokusal Sonuç"],
                [
                    [("1. DNA Hasarı", False, ""), ("Nükleer ve mitokondriyal mutasyon birikimi", False, ""), ("Transkripsiyon bozulması, senesens", True, "Hücrenin çoğalmayı durdurması")],
                    [("2. Replikatif Yaşlanma", False, ""), ("Her bölünmede telomer kısalması", False, ""), ("Hayflick sınırı, kök hücre tükenmesi", True, "Yenilenme kapasitesinin bitmesi")],
                    [("3. Proteostaz Bozulması", False, ""), ("Şaperon ve proteazom kapasite kaybı", False, ""), ("Toksik protein agregatları, ER stresi", True, "Nörodejenerasyon ve apoptoz")]
                ]
            ),
            make_cloze(
                "Yaşlanmayla birlikte dokularda gelişen düşük dereceli, steril kronik inflamasyon tablosuna inflammaging adı verilir.",
                "inflammaging",
                "Yaşlanma ve inflamasyonun birleşimini ifade eden kavram"
            )
        ]
    })

    # ADIM 5
    slides.append({
        "slideNumber": 5,
        "title": "Yaşlanma ve Hücre Döngüsü Düzenleyicileri: p53, p21 ve p16INK4a",
        "subtitle": "CDK inhibitörleri, Rb hipofosforilasyonu ve G1/S fazı kalıcı blokajı",
        "badge": "Hücre Döngüsü Blokajı",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Hücrelerin yaşlanıp bölünmeyi durdurması rastgele bir olay değildir; hücre döngüsü kontrol noktası bekçileri "
            "tarafından yönetilen kesin bir kilitlenmedir. DNA hasarı biriktiğinde ATM/ATR kinazlar 'genomun koruyucusu' "
            "p53'ü fosforilleyerek stabilize eder. Aktif p53, siklin bağımlı kinaz (CDK) inhibitörü olan 'p21'i sentezletir.\n\n"
            "> [SINAV SPOTU] Eş zamanlı olarak telomer aşınması ve onkojenik stres, CDKN2A lokusundan 'p16INK4a' transkripsiyonunu "
            "belirgin şekilde artırır. p16INK4a, CDK4/6-Siklin D kompleksini inhibe eder.\n\n"
            "CDK'lar baskılanınca Rb proteini hipofosforile (aktif) kalır, E2F transkripsiyon faktörünü sıkıca hapseder ve "
            "hücrenin G1 fazından S fazına geçişini kalıcı olarak kilitler."
        ),
        "medicalTerms": [
            {"term": "p16INK4a", "explanation": "CDK4/6'yı inhibe ederek Rb'yi aktif tutan ve hücresel senesensi sabitleyen tümör baskılayıcı proteindir."},
            {"term": "Hipofosforile Rb", "explanation": "E2F'ye bağlı kalarak hücrenin S fazına girmesini engelleyen aktif retinoblastom formudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] p16INK4a artışı hücresel senesensin ve yaşlanmanın en güvenilir biyolojik belirtecidir.",
            "📌 [SINAV SPOTU] p21 ve p16INK4a, Rb'nin fosforillenmesini önleyerek G1 fazında kalıcı tutukluk yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "p53 - p21 Aksı", "desc": "DNA çift zincir kırıkları sonrasında geçici/kalıcı döngü freni.", "isKey": True},
                {"title": "p16INK4a - Rb Aksı", "desc": "Senesent hücrelerde geri dönüşsüz proliferasyon blokajı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Senesens Hücre Döngüsü Kilitlenme Zinciri",
                [
                    "1. Genomik Hasar / Telomer Kaybı: Çift zincir kırıkları ATM/ATR kinazları uyarır.",
                    "2. p53 ve p16 İndüksiyonu: p53 p21'i üretir; CDKN2A lokusundan p16INK4a salınır.",
                    "3. CDK İnhibisyonu: p21 ve p16 Siklin D-CDK4/6 kinaz aktivitesini felç eder.",
                    "4. Rb Hipofosforilasyonu: Retinoblastom (Rb) fosforillenemez ve E2F'yi bırakmaz.",
                    "5. Kalıcı Senesens: E2F serbest kalamadığı için S fazı genleri okunamaz ve bölünme durur."
                ]
            ),
            make_cloze(
                "Hücresel yaşlanma ve senesensin en karakteristik moleküler biyobelirteci p16INK4a proteininin ekspresyon artışıdır.",
                "p16INK4a",
                "CDK4/6'yı inhibe eden senesens belirteç proteini"
            )
        ]
    })

    # ADIM 6
    slides.append({
        "slideNumber": 6,
        "title": "Senesent Hücre Fenotipi: Büyüme Tutukluğu ve Morfolojik Şişme",
        "subtitle": "Geniş yassılaşmış sitoplazma, SA-β-galaktozidaz aktivitesi ve apoptoz direnci",
        "badge": "Senesent Morfoloji",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Senesent (yaşlanmış) hücreler ölü hücreler değildir; aksine metabolik olarak oldukça aktiftirler ancak "
            "büyüme faktörlerine yanıt vermez ve asla bölünmezler. Mikroskop altında genç hücrelere göre belirgin "
            "şekilde büyümüş, yayvanlaşmış, vakuollü ve düzensiz sınırlı bir morfoloji sergilerler.\n\n"
            "> [SINAV SPOTU] Senesent hücrelerin laboratuvarda gösterilmesinde altın standart belirteç 'Senesensle "
            "İlişkili Beta-Galaktozidaz' (SA-β-galaktozidaz) enzim aktivitesidir; asidik pH 6.0'da mavi renk verir.\n\n"
            "Ayrıca senesent hücreler anti-apoptotik BCL-2 ailesi proteinlerini yukarı regüle ederek ölüme karşı "
            "inanılmaz bir direnç kazanır; dokudan kolay kolay temizlenemezler."
        ),
        "medicalTerms": [
            {"term": "SA-β-Galaktozidaz", "explanation": "Senesent hücrelerin lizozomlarında aşırı biriken ve pH 6.0'da boyanan tanısal enzimdir."},
            {"term": "Apoptoz Direnci", "explanation": "Senesent hücrelerin ölüm sinyallerine rağmen canlı kalıp dokuda birikmesini sağlayan özelliktir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] SA-β-galaktozidaz aktivitesi senesent hücreleri histolojide saptayan temel belirteçtir.",
            "📌 [SINAV SPOTU] Senesent hücreler morfolojik olarak genişlemiş, yassılaşmış ve apoptoza dirençlidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Morfolojik İmza", "desc": "Devasa genişlemiş, düzensiz ve bol lizozomlu sitoplazma.", "isKey": True},
                {"title": "Enzimatik Boyanma", "desc": "pH 6.0'da SA-β-gal pozitifliği (mavi boyanma).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Doku kültüründe yaşlanan ve kalıcı senesense giren fibroblastların tespiti için histokimyasal olarak kullanılan ve pH 6.0'da aktif olan en özgül enzim belirteci hangisidir?",
                {
                    "A": "Miyeloperoksidaz",
                    "B": "Senesensle ilişkili beta-galaktozidaz (SA-β-gal)",
                    "C": "Alkalen fosfataz",
                    "D": "Asit maltaz",
                    "E": "Tirozinaz"
                },
                "B",
                {
                    "A": "Miyeloperoksidaz nötrofillere aittir.",
                    "B": "Doğru! SA-β-galaktozidaz senesent hücrelerin klasik laboratuvar belirtecidir.",
                    "C": "Alkalen fosfataz safra ve kemiktedir.",
                    "D": "Asit maltaz Pompe hastalığında eksiktir.",
                    "E": "Tirozinaz melanin sentezler."
                }
            ),
            make_cloze(
                "Senesent hücrelerin laboratuvarda tespitinde kullanılan anahtar enzim belirteci SA-β-galaktozidaz aktivitesidir.",
                "SA-β-galaktozidaz",
                "pH 6'da boyanan senesens belirteç enzimi"
            )
        ]
    })

    # ADIM 7
    slides.append({
        "slideNumber": 7,
        "title": "Senesens İlişkili Salgı Fenotipi (SASP): Parakrin Toksisite",
        "subtitle": "İnterlökinler (IL-6, IL-8), matriks metalloproteinazlar ve komşu doku harabiyeti",
        "badge": "SASP ve Toksisite",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Senesent hücreler bölünmeyi durdurmuş olsalar da çevre dokuya karşı pasif kalmazlar. Sitoplazmalarındaki "
            "NF-κB ve cGAS-STING yollarının sürekli tetiklenmesiyle devasa miktarda biyoaktif faktör salgılarlar. Bu sekretuar "
            "profile 'Senesensle İlişkili Salgı Fenotipi' (Senescence-Associated Secretory Phenotype - SASP) adı verilir.\n\n"
            "> [SINAV SPOTU] SASP; pro-inflamatuvar sitokinler (IL-6, IL-1β), kemokinler (IL-8), büyüme faktörleri (TGF-β) "
            "ve matriks yıkan metalloproteinazlar (MMP-1, MMP-3) içerir.\n\n"
            "SASP faktörleri çevreleyen genç hücreleri de senesense zorlar (parakrin senesens), doku matriksini yıkar "
            "ve tümör gelişimini paradoksal olarak destekler."
        ),
        "medicalTerms": [
            {"term": "SASP", "explanation": "Senesent hücrelerin salgıladığı sitokin, kemokin ve proteazlardan oluşan toksik salgı kokteylidir."},
            {"term": "Parakrin Senesens", "explanation": "Senesent hücrelerin salgılarıyla komşu sağlıklı hücreleri de yaşlandırması olayıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] SASP'ın anahtar bileşenleri IL-6, IL-8 ve matriks metalloproteinazlardır (MMP).",
            "📌 [SINAV SPOTU] SASP komşu dokuda kronik inflamasyon ve maligniteye yatkın mikroçevre yaratır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Zehirli Salgı", "desc": "IL-6, IL-1, TNF ve doku eriten metalloproteinazlar.", "isKey": True},
                {"title": "Bulaşıcı Yaşlanma", "desc": "Parakrin etkiyle çevre hücrelerde de yaşlanma indüklenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "İstirahat Hücresi vs SASP Salgılayan Senesent Hücre",
                "İstirahat Hücresi (G0 Fazı)",
                "Minimal bazal sitokin salgısı, korunmuş doku desteği ve gerektiğinde tekrar hücre döngüsüne girme yeteneği.",
                "SASP Senesent Hücre",
                "Asla bölünemeyen, çevreye sürekli IL-6, IL-8 ve matriks yıkan metalloproteinazlar pompalayan kronik toksik hücre profili."
            ),
            make_active_recall(
                "Senesent hücrelerin çevre dokuya salgıladığı toksik faktörler kokteyline ne ad verilir ve en önemli 2 sitokin bileşeni nedir?",
                "SASP (Senesens İlişkili Salgı Fenotipi) adı verilir; en önemli bileşenleri IL-6 ve IL-8'dir (ayrıca MMP'ler)."
            )
        ]
    })

    # ADIM 8
    slides.append({
        "slideNumber": 8,
        "title": "Fizyolojik Yaşlanma vs Patolojik Hızlanmış Yaşlanma Dinamikleri",
        "subtitle": "Biyolojik yaş vs kronolojik yaş ve progeroid sendromların klinik dersleri",
        "badge": "Fizyolojik vs Hızlanmış",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Klinik pratikte bireylerin takvim yaşı (kronolojik yaş) ile dokularının gerçek hücresel yıpranma düzeyi "
            "(biyolojik yaş) her zaman örtüşmez. Kronik stres, sigara, kötü beslenme, kontrolsüz diyabet ve toksinler "
            "telomer kısalmasını ve DNA hasarını hızlandırarak 'hızlanmış hücresel yaşlanmaya' yol açar.\n\n"
            "> [YÜKSEK VERİM] Patolojik yaşlanmanın en uç modelleri progeroid sendromlardır; örneğin Hutchinson-Gilford "
            "progeria sendromunda lamin A mutasyonu (progerin) nükleer membranı bozar ve çocuklarda 80 yaşında bir ihtiyarın "
            "damar ve cilt fenotipini yaratır.\n\n"
            "Bu durum, hücresel bütünlüğün korunmasının sistemik yaşam beklentisindeki belirleyici gücünü simgeler."
        ),
        "medicalTerms": [
            {"term": "Biyolojik Yaş", "explanation": "Hücresel telomer uzunluğu, DNA hasarı ve fonksiyonel rezerve göre belirlenen gerçek doku yaşıdır."},
            {"term": "Progeria (HGPS)", "explanation": "Lamin A mutasyonuna bağlı çocukluk çağında masif erken yaşlanma ve kardiyovasküler ölüm sendromudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Progeria lamin A (progerin) mutasyonuyla nükleer laminayı yıkar.",
            "📌 [SINAV SPOTU] Biyolojik yaş telomer uzunluğu ve epigenetik metilasyon saatleriyle ölçülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Biyolojik Fark", "desc": "Aynı takvim yaşındaki iki bireyde organ rezervleri dramatik farklı olabilir.", "isKey": True},
                {"title": "Genetik Hızlanma", "desc": "Nükleer zar veya DNA onarım defektleri çocuklukta ölümcül yaşlılık yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hutchinson-Gilford progeria sendromunda nükleer membran proteinini bozan temel mutasyon lamin A gen mutasyonudur.",
                "lamin A",
                "Çocukluk erken yaşlanmasında mutant nükleer zar proteini"
            ),
            make_active_recall(
                "Kronolojik yaş ile biyolojik yaş arasındaki kavramsal fark nedir?",
                "Kronolojik yaş doğumdan itibaren geçen takvim süresini ifade ederken; biyolojik yaş hücrelerin telomer boyu, DNA hasarı ve organ rezervine dayanan gerçek yıpranma düzeyini ifade eder."
            )
        ]
    })

    # ADIM 9 - CHECKPOINT 1
    slides.append({
        "slideNumber": 9,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Hücresel Yaşlanma Kavramı ve Temel Mekanizmalar",
        "subtitle": "Klinik önem, moleküler 6 mekanizma, p16/p53 kilitlenmesi ve SASP'ın sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 1,
        "synthesisNarrative": (
            "Bu ilk checkpoint sayfasında hücresel yaşlanmanın temel kavramlarını ve moleküler omurgasını sentezliyoruz. "
            "1) Tanım: Çoğalma kapasitesi ve fonksiyonel aktivitenin zamanla ilerleyici azalmasıdır; yaş bağımsız "
            "en güçlü kronik hastalık risk faktörüdür. 2) Yaşlanma pasif bir zaman akışı değil; genler ve sinyal yollarıyla "
            "aktif kontrol edilen bir süreçtir. 3) 6 temel mekanizma: DNA hasarı, replikatif senesens, proteostaz çöküşü, "
            "mitokondri/ROS, IGF-1/mTOR ekseni ve inflammaging. 4) Hücre döngüsü blokajı: p53-p21 ve p16INK4a artışıyla "
            "Rb hipofosforile kalır, E2F kilitlenir ve G1/S geçişi durur. 5) Senesent hücre: SA-β-gal pozitif, geniş ve SASP "
            "(IL-6, IL-8, MMP) salgılayarak dokuyu zehirler.\n\n"
            "> [KLİNİK İPUCU] Sınavda senesens belirteci sorulduğunda akla ilk gelen p16INK4a ve SA-β-galaktozidaz olmalıdır.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle pekiştiriniz."
        ),
        "medicalTerms": [
            {"term": "Hücresel Senesens", "explanation": "Bölünme döngüsünden kalıcı çıkış ve SASP salgılanması durumudur."},
            {"term": "SA-β-Gal", "explanation": "pH 6.0'da aktif senesens belirteç enzimidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] p16INK4a ve SA-β-gal hücresel senesensin değişmez iki temel belirtecidir.",
            "📌 [SINAV SPOTU] Senesent hücreler bölünmez ancak SASP salgılayarak çevre dokuyu tahrip eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Döngü Freni", "desc": "p16INK4a ve p21 aracılığıyla Rb kilitlenmesi.", "isKey": True},
                {"title": "Sekretuar Toksisite", "desc": "SASP ile IL-6, IL-8 ve proteaz fırtınası.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-08-fc-01",
                "Hücresel yaşlanmanın (senesens) laboratuvarda gösterilmesinde kullanılan en karakteristik enzim ve gen belirteçleri nelerdir?",
                "Enzim belirteci pH 6.0'da aktif Senesensle İlişkili Beta-Galaktozidazdır (SA-β-gal); gen/protein belirteci ise CDK inhibitörü olan p16INK4a proteinidir.",
                "Senesens tanısında kullanılan temel belirteçler"
            ),
            make_flashcard(
                "k1-08-fc-02",
                "Senesent hücrelerin salgıladığı SASP (Senesens İlişkili Salgı Fenotipi) çevre dokuda neye yol açar?",
                "İçerdiği IL-6, IL-8 ve matriks metalloproteinazlar (MMP) nedeniyle çevre dokuda kronik inflamasyon, doku matriksi yıkımı ve parakrin olarak komşu hücrelerin de senesense girmesine yol açar.",
                "SASP kokteylinin çevre dokudaki toksik etkileri"
            ),
            make_flashcard(
                "k1-08-fc-03",
                "Yaşlanma sürecinde hücre döngüsünü G1 fazında kalıcı olarak kilitleyen temel moleküler mekanizma nedir?",
                "p16INK4a ve p21'in CDK4/6'yı inhibe etmesi, bunun sonucunda Retinoblastom (Rb) proteininin hipofosforile kalarak E2F transkripsiyon faktörünü sürekli bağlı tutmasıdır.",
                "Hücre döngüsü G1/S kontrol noktası ve Rb blokajı"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Hücresel senesens durumunda E2F faktörünü sürekli bağlı tutarak S fazına geçişi engelleyen molekül hipofosforile Rb proteinidir.",
                "Rb",
                "Retinoblastom tümör baskılayıcı proteini"
            )
        ]
    })

    # ADIM 10
    slides.append({
        "slideNumber": 10,
        "title": "Bölüm Sentezi ve Senesens Değerlendirme Algoritması",
        "subtitle": "Klinik araştırmalarda senolitik tedaviler ve hücresel temizlik stratejileri",
        "badge": "Senolitik Algoritma",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Modern biyogerontolojide senesent hücrelerin dokularda birikerek kronik hastalıkları körüklediğinin "
            "anlaşılması, yeni bir tedavi sınıfı doğurmuştur: 'Senolitikler'. Senolitik ajanlar (örneğin dasatinib, "
            "kuversetin, navitoklaks), senesent hücrelerin hayatta kalmak için kullandığı anti-apoptotik BCL-2/BCL-XL "
            "yolaklarını hedef alarak onları seçici olarak apoptoza gönderir.\n\n"
            "> [KLİNİK İPUCU] Deneysel çalışmalarda senolitiklerle yaşlı farelerin dokularındaki senesent hücrelerin "
            "temizlenmesi; damar elastikiyetini düzeltmiş, böbrek fonksiyonlarını restore etmiş ve genel yaşam kalitesini artırmıştır.\n\n"
            "Bu bulgular, yaşlanmanın kaçınılmaz bir son değil, tedavi edilebilir bir patolojik süreç olabileceğini müjdeler."
        ),
        "medicalTerms": [
            {"term": "Senolitik Tedavi", "explanation": "Senesent hücreleri seçici olarak tanıyıp apoptozla dokulardan temizleyen ilaç grubudur."},
            {"term": "Biyogerontoloji", "explanation": "Yaşlanmanın biyolojik, moleküler ve genetik süreçlerini inceleyen bilim dalıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Senolitikler senesent hücreleri seçici apoptozla yok eden deneysel ilaçlardır.",
            "📌 [SINAV SPOTU] Senesent hücrelerin temizlenmesi doku rejenerasyonunu ve fonksiyonunu restore eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hedefli Temizlik", "desc": "SASP salgılayan toksik senesent hücrelerin apoptozla elenmesi.", "isKey": True},
                {"title": "Doku İyileşmesi", "desc": "Fibrozisin gerilemesi ve kök hücre nişlerinin rahatlaması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Deneysel bir anti-aging çalışmasında yaşlı farelere uygulanan bir molekülün dokulardaki p16INK4a ve SA-β-gal pozitif hücreleri seçici olarak apoptoza uğrattığı ve doku inflamasyonunu (IL-6, IL-8) dramatik olarak düşürdüğü saptanıyor. Bu ilacın farmakolojik sınıfı nedir?",
                [
                    {
                        "text": "Telomeraz inhibitörü",
                        "isCorrect": False,
                        "feedback": "Telomeraz inhibitörü telomerleri kısaltır; senesent hücreleri seçici temizlemez."
                    },
                    {
                        "text": "Senolitik ajan",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Senesent hücreleri seçici olarak apoptoza gönderen ilaç sınıfı senolitiklerdir."
                    }
                ]
            ),
            make_active_recall(
                "Senolitik ilaçların senesent hücreleri yok etmek için hedef aldığı temel hücresel zayıflık nedir?",
                "Senesent hücrelerin hayatta kalmak için aşırı bağımlı olduğu anti-apoptotik sinyal yolaklarıdır (özellikle BCL-2 ve BCL-XL proteinleridir)."
            )
        ]
    })

    return slides
