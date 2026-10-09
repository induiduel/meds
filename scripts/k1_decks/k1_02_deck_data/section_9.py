#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 9: Histopatolojik Teknik Artefaktları (Adımlar 80 - 89)
Ders: Tıbbi Patoloji - Patolojiye Giriş
Öğretim Üyesi: Prof. Dr. Hikmet Keleş
"""

from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_steps():
    return [
        # Adım 80
        {
            "slideNumber": 80,
            "title": "Artefakt Kavramı ve Patolojik Tanıdaki Tuzaklar",
            "subtitle": "Artefakt; canlı dokunun orijinal yapısında bulunmayan, cerrahi çıkarma, fiksasyon, takip veya boyama hatalarıyla sonradan oluşan yapay görünümdür.",
            "badge": "Artefakt Kavramı",
            "badgeColor": "red",
            "discipline": "Histopatoloji",
            "synthesisNarrative": """==Artefakt (Yapay Görünüm)==; canlı dokuda bulunmayan, cerrahi çıkarma, fiksasyon, takip, kesim veya boyama aşamalarındaki ==teknik ve insani hatalar sonucu sonradan oluşan yapay değişikliklerdir==.

Artefaktlar patolojideki en kritik tanısal tuzakların başında gelir. Normal dokuyu malign gibi göstererek ==yalancı pozitifliğe== ya da tümör hücrelerinin morfolojisini bozup üzerini örterek ==yalancı negatifliğe== yol açabilirler. Ayrıca immünohistokimyasal zemin boyanması oluşturarak hedefe yönelik tedavi kararlarını yanıltabilirler. Patoloğun temel becerisi, gerçek hücresel doku tepkisi ile laboratuvarda oluşan bu yapay deformasyonları ayırt edebilmesidir.

> [PATOLOJİ YASASI] Canlıdaki lezyon ile yapay teknik hatayı ayırt etmek, hastayı yanlış tanı ve hatalı tedaviden korur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Dokuya Ait Değildir", "desc": "Preanalitik, takip veya kesim aşamalarında dış müdahaleyle oluşur.", "isKey": True},
                    {"title": "Tanısal Tuzak Kaynağı", "desc": "Yalancı kanser tanısına veya kanserin atlanmasına yol açabilir.", "isKey": True},
                    {"title": "Her Aşamada Oluşabilir", "desc": "Koterden fiksasyona, mikrotomdan lamel yapıştırmaya kadar her basamakta görülebilir.", "isKey": False}
                ],
                "table": {
                    "title": "Histopatolojik Süreç Basamakları ve Tipik Artefaktları",
                    "headers": ["Aşama", "Teknik Hata Nedeni", "Oluşan Karakteristik Artefakt"],
                    "rows": [
                        ["Cerrahi Çıkarma", "Elektrokoter kullanımı veya forsepsle aşırı sıkma", "Termal koagülasyon nekrozu ve nükleer ezilme (crush)"],
                        ["Fiksasyon", "Geç fiksasyon veya asidik formalin kullanımı", "Otoliz (hücre erimesi) ve asit formaldehit hematin pigmenti"],
                        ["Doku Takibi", "Yetersiz dehidrasyon veya kirli ksilen", "Yumuşak blok, soluk boyanma ve sütümsü bulanıklık"],
                        ["Mikrotomi", "Körelmiş bıçak veya gevşek klemens", "Bıçak çentiği (yırtılma) ve chatter (panjur/titreme çizgileri)"],
                        ["Flotasyon / Montaj", "Kirli su banyosu veya hava kabarcığı", "Floater (başka hasta dokusu) ve lamel altı kabarcıklar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Artefakt, dokunun doğal yapısında bulunmayan, cerrahi ve laboratuvar işlemleri esnasında oluşan yapay değişikliklerdir.",
                "📌 [TANI SPOTU] Floater artefaktı (su banyosundan başka hastanın dokusunun bulaşması), sağlıklı hastaya kanser tanısı koydurabilecek en tehlikeli artefakttır.",
                "💡 [ÖĞRENME İPUCU] Patolog bir preparatta şüpheli hücreler gördüğünde önce etrafındaki normal doku mimarisinin ve boyanma kalitesinin artefakttan ari olup olmadığını denetler."
            ],
            "medicalTerms": [
                {"term": "Artefakt", "explanation": "Teknik veya cerrahi işlemler sırasında dokuda sonradan oluşan yapay görünümlerdir."},
                {"term": "Yalancı Pozitiflik", "explanation": "Gerçekte hastalık yokken teknik hata veya artefakt nedeniyle hatalı pozitif tanı konmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Gerçek Patolojik Lezyon vs Teknik Artefakt Ayrımı",
                    "Gerçek Patolojik Lezyon",
                    "Teknik Artefakt (Yapay Görünüm)",
                    [
                        "Hücreler arasında biyolojik doku yanıtı (inflamasyon, fibrozis) vardır",
                        "Komşu doku mimarisiyle fizyolojik ve anatomik uyum gösterir",
                        "Farklı derin seri kesitlerde lezyon varlığını sürdürür",
                        "Hastanın klinik semptomları ve radyolojisiyle koreledir"
                    ],
                    [
                        "Çevresinde hiçbir hücresel yangı veya stromal reaksiyon izlenmez",
                        "Keskin, geometrik veya bıçak hattına paralel yapay çizgiler taşır",
                        "Derin kesit alındığında yapay oluşum tamamen kaybolur",
                        "Hastanın kliniğiyle tamamen uyumsuz, laboratuvar kaynaklıdır"
                    ]
                ),
                make_micro_quiz(
                    "Histopatolojik incelemede 'Artefakt' terimi tıp literatüründe ve patoloji pratiğinde neyi ifade eder?",
                    {
                        "A": "Vücutta genetik mutasyon sonucu kendiliğinden oluşan benign tümörleri",
                        "B": "Cerrahi çıkarma, fiksasyon, doku takibi veya boyama gibi teknik işlemler sırasında dokuda oluşan yapay değişiklikleri",
                        "C": "Sadece elektron mikroskobuyla görülebilen normal hücre organellerini",
                        "D": "Kanser hücrelerinin lenf damarları içine girmesini",
                        "E": "Karaciğerde biriken normal demir depolarını"
                    },
                    "B",
                    {
                        "A": "Yanlış. Neoplazi dokunun kendi kontrolsüz biyolojik proliferasyonudur.",
                        "B": "Doğru. Artefakt cerrahi ve laboratuvar işlemlerinde sonradan oluşan tüm yapay kusurlardır.",
                        "C": "Yanlış. Normal organeller dokunun biyolojik yapı taşlarıdır.",
                        "D": "Yanlış. Bu durum tümörün gerçek lenfovasküler invazyonudur.",
                        "E": "Yanlış. Hemosiderin dokuda fizyolojik veya patolojik biriken demir pigmentidir."
                    }
                ),
                make_cloze(
                    "Cerrahi veya laboratuvar basamaklarındaki teknik hatalar sonucu dokuda beliren ve tanısal yanılgılara yol açabilen yapay görünümlere artefakt adı verilir.",
                    "artefakt",
                    "Teknik işlemler sırasında oluşan yapay lezyon terimi"
                )
            ]
        },

        # Adım 81
        {
            "slideNumber": 81,
            "title": "Fiksasyon Kaynaklı Artefaktlar: Otoliz ve Geç Fiksasyon",
            "subtitle": "Dokunun fiksatife geç konulması veya yetersiz formalinde kalması; nükleusların silinmesine, hücrelerin şişmesine ve 'hayalet hücre' tablosuna yol açar.",
            "badge": "Otoliz Artefaktı",
            "badgeColor": "amber",
            "discipline": "Histopatoloji",
            "synthesisNarrative": """==Geç Fiksasyon ve Otoliz Artefaktı==; dokunun fiksatife geç girmesiyle lizozomal hidrolazların hücre mimarisini sindirmesi sonucu oluşan en sık fiksasyon hatasıdır.

Ameliyatla alınan doku hızla formaline konulmazsa hücrelerde ATP tükenir ve lizozom enzimleri serbest kalır. Hücre zarları parçalanarak sitoplazmalar birbirine karışır, nükleer kromatin erir (karyolizis) ve nükleusu silinmiş ==hayalet hücreler (ghost cells)== belirir. Bağırsak mukozasında epitel bazal membrandan dökülerek nekrozu taklit edebilir. Enzimler protein yapısını ve antijenleri yıktığı için hematoksilen-eozin boyanması soluklaşır ve tüm immünohistokimyasal belirteçler yalancı negatif sonuç verir.

> [GERİ DÖNÜŞSÜZ KAYIP] Otolize uğrayan dokuda antijenler ve nükleuslar eridiğinden kanser tanısı imkansızlaşır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hayalet Hücreler", "desc": "Nükleusların sindirilmesi sonucu çekirdeksiz soluk hücre silüetleri kalır.", "isKey": True},
                    {"title": "Mukozal Dökülme", "desc": "Gastrointestinal epitel bazal membrandan ayrılarak yapay dökülür.", "isKey": True},
                    {"title": "İHK Kaybı", "desc": "Otoliz proteinleri parçaladığından antijenler yok olur ve tüm İHK testleri negatifleşir.", "isKey": False}
                ],
                "table": {
                    "title": "Taze Fikse Edilmiş Doku ile Otolizli Dokunun Mikroskobik Karşılaştırması",
                    "headers": ["Histolojik Özellik", "Kusursuz Fikse Doku", "Geç Fikse / Otolizli Doku"],
                    "rows": [
                        ["Hücre Çekirdeği (Nükleus)", "Koyu mavi-mor (bazofilik), net nükleol ve kromatin", "Soluk, silik, sınırları belirsiz veya tamamen kayıp (hayalet hücre)"],
                        ["Hücre Sınırları", "Hücre zarları ve komşuluklar keskin ve net", "Hücre zarları parçalanmış, sitoplazmalar homojen erimiş"],
                        ["Epitel - Stroma İlişkisi", "Epitel bazal membrana sıkıca tutunur", "Epitel tabakalar halinde bazal membrandan ayrılıp lümene dökülür"],
                        ["İmmünohistokimya", "Antijenler korunmuştur; güçlü ve net pozitiflik", "Antijenler parçalandığı için yalancı negatif sonuçlar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yetersiz veya geç fiksasyon sonucu gelişen otolizde hücre nükleusları soluklaşır ve çekirdeği silinmiş 'hayalet hücreler' (ghost cells) izlenir.",
                "📌 [TANI SPOTU] Bağırsak biyopsisinde epitelin tabaka halinde dökülmesi gerçek bir enfarktüs nekrozu değil, geç fiksasyon otoliz artefaktı olabilir.",
                "🚨 [KRİTİK UYARI] Otoliz olmuş dokuda İHK antijenleri parçalandığından HER2 veya hormon reseptörleri yalancı negatif çıkar."
            ],
            "medicalTerms": [
                {"term": "Karyolizis", "explanation": "Otoliz veya nekrozda nükleaz etkisiyle çekirdeğin eriyip boyanma özelliğini yitirmesidir."},
                {"term": "Hayalet Hücre (Ghost Cell)", "explanation": "Çekirdeği otoliz sonucu eriyerek kaybolmuş, yalnızca hücresel konturu kalan soluk hücredir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Kusursuz Fikse Doku vs Otolizli Doku Görünümü",
                    "Zamanında Fikse Edilmiş Doku",
                    "Geç Fikse Edilmiş (Otolizli) Doku",
                    [
                        "Hücre çekirdeği koyu mavi-mor bazofilik kromatiniyle parlar",
                        "Nükleol ve nükleer membran sınırları milimetrik keskindir",
                        "Sitoplazma organelleri ve hücre zarları tek tek seçilir",
                        "İmmünohistokimyasal antijenler kusursuz boyanır"
                    ],
                    [
                        "Çekirdekler solmuş, erimiş veya tamamen yok olmuştur (hayalet)",
                        "Kromatin yapısı silinmiş, homojen camsı solukluk hakimdir",
                        "Hücre sınırları kaybolmuş, sitoplazmalar birbirine akmıştır",
                        "Proteinler parçalandığından İHK belirteçleri tutunamaz"
                    ]
                ),
                make_micro_quiz(
                    "Ameliyattan sonra fiksatif konulmadan saatlerce bekletilen bir bağırsak rezeksiyon materyalinde patoloğun mikroskopta hücre sınırlarının silindiğini, çekirdeklerin kaybolduğunu ve 'hayalet hücreler' oluştuğunu görmesi aşağıdaki süreçlerden hangisinin sonucudur?",
                    {
                        "A": "Apoptoz mekanizmasının aşırı çalışması",
                        "B": "Otoliz (kendi kendine enzimatik erime) artefaktı",
                        "C": "Ksilenin dokuyu aşırı sertleştirmesi",
                        "D": "Mikrotom bıçağının körelmesi",
                        "E": "Parafinin aşırı soğuması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Apoptoz nükleer fragmantasyon ve büzüşmeyle giden programlı ölümdür.",
                        "B": "Doğru. Fiksatife geç giren dokularda lizozomal enzimler çekirdeği eriterek hayalet hücre yapar.",
                        "C": "Yanlış. Ksilen dokuyu sertleştirir ancak hücresel lizise yol açmaz.",
                        "D": "Yanlış. Mikrotom körelmesi mekanik yırtılma ve çizik artefaktı oluşturur.",
                        "E": "Yanlış. Parafinin soğuması blok sertliğini etkiler, otoliz yapmaz."
                    }
                ),
                make_cloze(
                    "Geç fiksasyon sonucu hücre çekirdeğinin eriyip silinmesiyle geride kalan soluk hücresel konturlara hayalet hücre adı verilir.",
                    "hayalet hücre",
                    "Nükleusu silinmiş otolitik hücre silüeti terimi"
                )
            ]
        },

        # Adım 82
        {
            "slideNumber": 82,
            "title": "Kimyasal Pigment Artefaktı: Formalin Pigmenti (Asit Formaldehit Hematin)",
            "subtitle": "Asidik formalinde bekleyen kanlı dokularda hemoglobin ile formik asidin birleşmesiyle kahverengi-siyah granüler formalin pigmenti çöker.",
            "badge": "Formalin Pigmenti",
            "badgeColor": "purple",
            "discipline": "Histopatoloji",
            "synthesisNarrative": """==Formalin Pigmenti (Asit Formaldehit Hematin)==; tamponlanmamış asidik formalinde hemoglobinin parçalanmasıyla damar lümenlerinde çöken koyu kahverengi-siyah kimyasal artefakttır.

Formalin çözeltisi tamponlanmadığında oksitlenerek ortam pH'sını ==6.0'ın altına== düşürür. Asidik ortamda eritrositlerin hemoglobini parçalanır ve hem grubu asit formaldehitle suda erimeyen hematin tuzu yapar. Polarize ışıkta ==çift kırınım== veren bu siyah granüller; ==melanin, hemosiderin ve antrakoz== pigmentleriyle karışabilir. Artefakt, pH 7.0-7.4 aralığındaki ==nötral tamponlu formalin== ile önlenir ve alkolik pikrik asit solüsyonuyla kesitten yıkanabilir.

> [KİMYASAL KURAL] Formalin pigmenti hastalık değildir; asidik formalinin kanda bıraktığı yapay kimyasal çökeltidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Asit pH (<6.0) Şartı", "desc": "Formaldehitin formik aside oksitlenmesiyle asidik ortamda oluşur.", "isKey": True},
                    {"title": "Siyah-Kahverengi Granüller", "desc": "Kanama alanlarında ve damar içlerinde birikerek melanomla karışabilir.", "isKey": True},
                    {"title": "Nötral Tampon Çözümü", "desc": "%10 nötral tamponlu formalin kullanımı bu artefaktı tamamen engeller.", "isKey": False}
                ],
                "table": {
                    "title": "Formalin Pigmenti ile Diğer Kahverengi-Siyah Pigmentlerin Ayırıcı Tanısı",
                    "headers": ["Pigment Türü", "Kökeni", "Prusya Mavisi", "Polarize Işıkta Çift Kırınım", "Kimyasal Özellik"],
                    "rows": [
                        ["Formalin Pigmenti", "Asit formalin + Hemoglobin (Artefakt)", "Negatif", "Pozitif (Birefringent)", "Alkolik pikrik asit ile dokudan silinir"],
                        ["Hemosiderin", "Demir metabolizması (Patolojik)", "Kuvvetli Pozitif (Mavi)", "Negatif", "Makrofaj sitoplazmasında birikir"],
                        ["Melanin", "Melanositler (Melanom / Nevüs)", "Negatif", "Negatif", "Fontana-Masson ile siyah boyanır"],
                        ["Karbon (Antrakoz)", "Solunan hava kirliliği / Sigara", "Negatif", "Negatif", "Hiçbir kimyasalla ağarmaz, tamamen inerttir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Asit formaldehit hematin (formalin pigmenti), pH 6.0'ın altına düşen asidik formalinde hemoglobinin parçalanmasıyla oluşan siyah-kahverengi granüler bir artefakttır.",
                "📌 [TANI SPOTU] Formalin pigmenti polarize ışık altında çift kırınım (birefringence) gösterir ve alkolik pikrik asitle kesitten temizlenebilir.",
                "💡 [ÖĞRENME İPUCU] Bu artefaktı önlemenin kesin yolu laboratuvarda pH'sı 7.0 olan 'Nötral Tamponlu Formalin' kullanmaktır."
            ],
            "medicalTerms": [
                {"term": "Asit Formaldehit Hematin", "explanation": "Asidik formalinin hemoglobinle birleşmesiyle oluşan siyah-kahverengi yapay pigmenttir."},
                {"term": "Birefringence (Çift Kırınım)", "explanation": "Maddelerin polarize ışığı kırarak karanlık alanda parlak görünmesini sağlayan optik özelliktir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Formalin Pigmenti Oluşum Zinciri",
                    [
                        "1. Tampon Eksikliği: Fiksatif olarak tamponlanmamış asidik formalin solüsyonu kullanılır",
                        "2. Formik Asit Oluşumu: Oksitlenen formaldehit ortam pH'sını 6.0'ın altına düşürür",
                        "3. Hemoglobin Parçalanması: Asidik ortam damar içindeki eritrosit hemoglobinini parçalar",
                        "4. Hematin Çökmesi: Serbest kalan hem grubu asit formaldehitle suda erimeyen hematin tuzu yapar",
                        "5. Tanısal Karışıklık: Dokuda melanin veya hemosiderini taklit eden siyah granüller çöker"
                    ]
                ),
                make_micro_quiz(
                    "Dalak ve karaciğer gibi kan zengini dokuların incelenmesinde damar lümenlerinde ve kanama odaklarında saptanan, polarize ışıkta çift kırınım veren siyah-kahverengi granüllerin 'asit formaldehit hematin (formalin pigmenti)' olduğunu gösteren en temel laboratuvar nedeni nedir?",
                    {
                        "A": "Doku takibinde ksilen yerine aseton kullanılması",
                        "B": "Fiksasyonun nötral tampon yerine pH'sı 6.0'ın altındaki asidik formalinde yapılmış olması",
                        "C": "Dokunun rotary mikrotomda 3 mikron kesilmesi",
                        "D": "Su banyosu sıcaklığının 40°C olması",
                        "E": "Lamelin reçine ile kapatılması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Aseton bir dehidrasyon ajanı olup hematin pigmenti yapmaz.",
                        "B": "Doğru. Asit formaldehit hematin pH 6.0 altındaki asidik formalinde hemoglobin yıkımıyla oluşur.",
                        "C": "Yanlış. 3 mikronluk kesim mikrotomun ideal standart kesit kalınlığıdır.",
                        "D": "Yanlış. 40°C su banyosu kesitlerin açılması için uygun standart sıcaklıktır.",
                        "E": "Yanlış. Lamel kapatma işlemi mikroskopideki son montaj aşamasıdır."
                    }
                ),
                make_cloze(
                    "pH değeri 6.0'ın altındaki asidik formalinde hemoglobinin parçalanmasıyla dokuda oluşan yapay siyah-kahverengi pigment birikimine formalin pigmenti adı verilir.",
                    "formalin pigmenti",
                    "Asit formaldehit hematin artefaktının diğer adı"
                )
            ]
        },

        # Adım 83
        {
            "slideNumber": 83,
            "title": "Dehidrasyon ve Şeffaflaştırma Hataları: Kötü Alkol ve Kirli Ksilen",
            "subtitle": "Alkol serilerinin suyla kirlenmesi veya ksilen banyolarının eskimesi; dokuda soluk boyanmaya, sütümsü bulanıklığa ve parafinin girememesine yol açar.",
            "badge": "Takip Hataları",
            "badgeColor": "cyan",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Doku takip cihazlarında alkol ve ksilen banyolarının kirlenmesi; dokunun parafinle doymasını engelleyerek yumuşak bloklara ve soluk boyanmaya yol açar.

Mutlak alkol banyoları zamanla su çekip doymuş hale geldiğinde ==yetersiz dehidrasyon== gelişir; hücrede kalan su hidrofobik parafinin dokuya girmesini engeller. Dehidrasyondan ksilene su taşındığında ise ksilen tankında karakteristik bir ==sütümsü bulanıklık (milky appearance)== oluşur. Bu emülsiyon dokunun şeffaflaşmasını bozar ve kesitlerde mikro-boşluklar bırakır. Parafin infiltrasyonu yetersiz kalan bloklar mikrotomda merkezden ufalanır; mikroskopta ise soluk, mat ve ayrıntısız boyanma alanları izlenir.

> [KALİTE KONTROLÜ] Sütümsü beyazlık kazanan ksilen derhal dökülmeli ve takip banyoları kaset sayısına göre yenilenmelidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Yetersiz Dehidrasyon", "desc": "Su uzaklaştırılamazsa parafin giremez ve doku mikroskopta soluk kalır.", "isKey": True},
                    {"title": "Sütümsü Ksilen", "desc": "Ksilene su karışması süt benzeri beyaz bulanıklık yapar; doku şeffaflaşamaz.", "isKey": True},
                    {"title": "Periyodik Rotasyon", "desc": "Kimyasal istasyonlar periyodik olarak temizlenip yenilenmelidir.", "isKey": False}
                ],
                "table": {
                    "title": "Takip Reaktif Hataları ve Dokudaki Karşılıkları",
                    "headers": ["Reaktif Problemi", "Teknik Mekanizma", "Makroskobik / Mikroskobik Belirti"],
                    "rows": [
                        ["Su İçeren Alkol", "Son mutlak alkolün su tutması", "Blok merkezinde dokunun yumuşak kalması, parafinin içeri girmemesi"],
                        ["Kirli / Sulu Ksilen", "Ksilende su emülsiyonu oluşması", "Ksilen tankında sütümsü beyazlık; kesitte ince mikro-kabarcıklar"],
                        ["Ksilende Aşırı Bekletme", "Sürenin 24 saati aşması", "Dokunun taş gibi sertleşmesi, mikrotomda bıçağın takılıp dokuyu parçalaması"],
                        ["Yetersiz Parafin Banyosu", "Parafin süresinin kısa tutulması", "Dokunun ksilen kokması, blokta boşluklar ve büzüşme çukurları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Doku takip cihazında ksilen banyosunun süt benzeri beyaz bulanık bir renk alması, ksilene su karıştığını (yetersiz dehidrasyonu) gösterir.",
                "📌 [TEKNİK SPOT] Dehidrasyonu yetersiz yapılan dokularda mikroskopta boyanma soluk ve yamalı kalır; parafin bloğun ortası yumuşak kalır.",
                "💡 [ÖĞRENME İPUCU] Teknisyen ksilen kabına baktığında su damlacıkları veya bulanıklık görüyorsa tüm dehidrasyon serisini sıfırdan değiştirmelidir."
            ],
            "medicalTerms": [
                {"term": "Sütümsü Bulanıklık (Milky Appearance)", "explanation": "Doku takibinde ksilene su karışması sonucu oluşan emülsiyonun yarattığı beyaz bulanıklıktır."},
                {"term": "Reaktif Rotasyonu", "explanation": "Kirlenen ön banyoların atılıp arkadakilerin öne kaydırılması ve sona taze reaktif konmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Takip Reaktifi Kirlenme ve Blok Bozulma Zinciri",
                    [
                        "1. Alkolün Eskimesi: Çok sayıda kaset geçtikten sonra mutlak alkol serileri su toplar",
                        "2. Ksilene Su Taşınması: Yetersiz dehidre olan ıslak doku kasetleri ksilen banyosuna aktarılır",
                        "3. Sütümsü Emülsiyon: Ksilen suyla temas edince süt beyazı bulanık bir görünüm alır",
                        "4. İnfiltrasyon Engeli: Doku gözenekleri kapandığından erimiş parafin hücre içine nüfuz edemez",
                        "5. Blok Ufalanması: Merkezi yumuşak kalan blok mikrotomda kesilemez ve doku bütünlüğü bozulur"
                    ]
                ),
                make_micro_quiz(
                    "Patoloji laboratuvarında teknisyen doku takip cihazının şeffaflaştırma istasyonundaki ksilen banyosunun berrak olması gerekirken 'süt benzeri beyaz bir bulanıklık' kazandığını fark etmiştir. Bu durumun nedeni nedir ve ne yapılmalıdır?",
                    {
                        "A": "Ksilenin fazla soğuduğunu gösterir, ısıtılmalıdır.",
                        "B": "Önceki alkol banyolarından ksilene su taşındığını gösterir; dehidrasyon alkolleri ve ksilen derhal taze reaktiflerle yenilenmelidir.",
                        "C": "Normal bir durumdur, ksilende süt görünümü fiksasyonun bittiğini kanıtlar.",
                        "D": "Formaldehit gazının parafine dönüştüğünü gösterir.",
                        "E": "Mikrotom bıçağının paslandığını gösterir."
                    },
                    "B",
                    {
                        "A": "Yanlış. Ksilen oda sıcaklığında berraktır ve ısıtılması tehlikelidir.",
                        "B": "Doğru. Ksilendeki sütümsü bulanıklık suya işaret eder; alkol ve ksilen banyoları derhal yenilenmelidir.",
                        "C": "Yanlış. Sütümsü görünüm fiksasyonun değil, ağır bir reaktif kirlenmesinin kanıtıdır.",
                        "D": "Yanlış. Formaldehit gazı kimyasal olarak parafine dönüşemez.",
                        "E": "Yanlış. Bu kimyasal sorun mikrotom mekaniğinden bağımsız bir takip hatasıdır."
                    }
                ),
                make_cloze(
                    "Doku takibinde ksilene su bulaşması sonucu solüsyonun süt benzeri bulanık bir görünüm alması yetersiz dehidrasyon göstergesidir.",
                    "süt benzeri",
                    "Ksilene su karıştığında oluşan karakteristik bulanıklık tanımı"
                )
            ]
        },

        # Adım 84
        {
            "slideNumber": 84,
            "title": "Parafin Gömme ve Sıcaklık Artefaktları: Doku Yanığı ve Çatlaklar",
            "subtitle": "Erimiş parafin sıcaklığının 65°C'yi aşması doku proteinlerini pişirerek yanık artefaktı yapar; yavaş soğutma ise parafinde kristal çatlakları oluşturur.",
            "badge": "Termal Artefaktlar",
            "badgeColor": "red",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Parafin infiltrasyonu ve bloklamadaki termal dengesizlikler; doku proteinlerinin pişerek büzüşmesine veya blok yapısının kristallenerek çatlamasına neden olur.

Parafin banyolarının sıcaklığı ==en fazla 60°C== olmalıdır. Sıcaklık 65-70°C üzerine çıktığında doku proteinleri aşırı denatüre olarak ==doku yanığı artefaktı== gelişir. Hücreler büzüşür, nükleuslar kömürleşmiş gibi piknotik siyahlaşır ve doku yapay bir koagülasyon nekrozu görüntüsü alır. Bloklama sonrasında ise kalıplar hızla -5°C soğutucu tablaya alınmalıdır. Oda sıcaklığında yavaş soğuyan parafinde büyük kristaller ve hava boşlukları oluşur; blok mikrotomda kesilirken dağılır ve su banyosunda parçalanır.

> [TERMAL KURAL] Parafin ısısı 60°C'yi aşmamalı, kalıplanan bloklar hızlı soğutma tablasında dondurulmalıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "60°C Tavan Sıcaklık", "desc": "65°C üzeri ısı dokuyu pişirerek yalancı nekroz ve yanık artefaktı yapar.", "isKey": True},
                    {"title": "Hızlı Şok Soğutma", "desc": "Soğuk tabla (-5°C) parafinin homojen, mikrokristalin donmasını sağlar.", "isKey": True},
                    {"title": "Yavaş Soğuma Tehlikesi", "desc": "Büyük parafin kristalleri blokta çatlaklara ve kesit yırtılmasına yol açar.", "isKey": False}
                ],
                "table": {
                    "title": "Parafin Termal Hataları ve Doku Üzerindeki Etkileri",
                    "headers": ["Termal Parametre", "Hatalı Durum", "Dokuda Oluşan Artefakt"],
                    "rows": [
                        ["İnfiltrasyon Isısı", "> 65 - 70°C aşırı sıcak parafin", "Doku yanığı, aşırı büzüşme, yalancı nekroz ve piknotik çekirdekler"],
                        ["Doku Bekletme Süresi", "Parafinde günlerce unutulma", "Doku kırılganlaşır, antijenler tahrip olur, İHK çalışmaz"],
                        ["Blok Soğutma Hızı", "Oda ısısında çok yavaş soğutma", "Büyük parafin kristalleri, blok çatlaması, kesitte ufalanma"],
                        ["Blok Soğutma Tablası", "-5°C soğutucu plaka", "İdeal amorf katılaşma, pürüzsüz 3 mikron kesim performansı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Parafin infiltrasyonunda sıcaklığın 65°C'nin üzerine çıkması dokuda protein denatürasyonuna ve 'doku yanığı' (aşırı sertleşme ve büzüşme) artefaktına yol açar.",
                "📌 [TEKNİK SPOT] Parafin blokların kalıplandıktan sonra hızlı soğutulması (cooling plate) parafin kristallerinin küçülmesini ve bloğun homojen kesilmesini sağlar.",
                "💡 [ÖĞRENME İPUCU] Dokunun fırında aşırı pişmesi nükleusların kömür gibi siyah görünmesine yol açarak lenfoma ile karışabilir."
            ],
            "medicalTerms": [
                {"term": "Doku Yanığı Artefaktı", "explanation": "Yüksek parafin ısısında (>65°C) proteinlerin pişmesiyle oluşan yapay büzüşme ve nekrozdur."},
                {"term": "Soğutma Tablası (Cooling Plate)", "explanation": "Parafin blokların homojen katılaşmasını sağlayan -5°C sıcaklıktaki laboratuvar ünitesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "İdeal Parafin Bloklama vs Aşırı Sıcak Termal Yanık",
                    "İdeal Parafin Bloklama (58-60°C)",
                    "Aşırı Sıcak Termal Yanık (>70°C)",
                    [
                        "Doku esnekliğini ve hücre mimarisini mükemmel korur",
                        "Nükleus kromatini ve nükleol detayları net seçilir",
                        "Mikrotomda kesintisiz kurdele şeklinde şerit kesit verir",
                        "İmmünohistokimyasal antijenler hasar görmez"
                    ],
                    [
                        "Doku proteinleri pişerek aşırı sertleşir ve taşlaşır",
                        "Nükleuslar piknotik, kömürleşmiş siyah topaklar halini alır",
                        "Mikrotom bıçağı dokuya çarptığında çatlar ve dağılır",
                        "Protein yapısı kavrulduğundan İHK antijenleri tamamen yok olur"
                    ]
                ),
                make_micro_quiz(
                    "Doku takip cihazındaki parafin banyolarının termostat arızası nedeniyle 75°C'ye çıkması sonucunda ertesi gün bloklanan biyopsilerde mikroskop altında izlenecek en karakteristik artefakt aşağıdakilerden hangisidir?",
                    {
                        "A": "Hücrelerin aşırı şişmesi ve hidropik dejenerasyon",
                        "B": "Doku yanığı: Proteinlerin aşırı denatürasyonu, büzüşme ve nükleusların kömürleşmiş gibi piknotik görünmesi",
                        "C": "Prusya mavisi pozitifliği",
                        "D": "Lipid damlacıklarının kırmızıya boyanması",
                        "E": "Tümör evresinin gerilemesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Aşırı ısı hücreleri şişirmez, büzüştürüp sertleştirir.",
                        "B": "Doğru. 65°C üzeri ısı dokuyu pişirerek büzüşmeye, piknotik nükleuslara ve yalancı nekroza yol açar.",
                        "C": "Yanlış. Prusya mavisi hemosiderin demirini gösteren özel bir histokimyasal boyadır.",
                        "D": "Yanlış. Doku takibindeki rutin kimyasallar lipidleri tamamen eritir.",
                        "E": "Yanlış. Tümör evresi mikroskobik artefaktlarla geriye dönük değişmez."
                    }
                ),
                make_cloze(
                    "Parafin infiltrasyonu sırasında sıcaklığın 65 derecenin üzerine çıkması dokuda termal yanık ve aşırı büzüşme artefaktına yol açar.",
                    "65",
                    "Parafin doku yanığının başladığı kritik santigrat derece sınırı"
                )
            ]
        },

        # Adım 85
        {
            "slideNumber": 85,
            "title": "Mikrotomi Kesim Hataları I: Bıçak Çentiği (Knife Marks) ve Yırtılmalar",
            "subtitle": "Mikrotom jiletindeki mikroskobik çentikler veya dokudaki sert kalsiyum odakları; kesit boyunca paralel yırtılma çizgilerine yol açar.",
            "badge": "Bıçak Çentiği",
            "badgeColor": "orange",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """==Bıçak Çentiği (Knife Mark)==; mikrotom jiletindeki mikroskobik hasar veya sert odaklar nedeniyle kesit boyunca uzanan paralel yırtılma artefaktıdır.

Mikrotomda 3-5 mikrometre incelikte kesit alınırken jiletin kesici kenarı kusursuz olmalıdır. Jilet ağzında üretim hatası veya eğilme varsa blok her indiğinde dokuyu boydan boya yarar. Ayrıca dokuda unutulan cerrahi zımba telleri, kalsifikasyonlar veya kemik odakları jilete çarptığında bıçak ağzını çentikler. Bu mekanik temas sonucunda doku kesitinde ==kesim doğrultusuna paralel uzanan düz yırtık hatları ve doku kayıpları== oluşur. Kalsifiye dokular önceden dekalsifiye edilmeli, çentik görüldüğünde jilet kaydırılmalı veya yenisiyle değiştirilmelidir.

> [MEKANİK İLKE] Kesim yönünde uzanan düz yırtık çizgisi bıçak hatasıdır; jilet kaydırıldığında düzelir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Paralel Yırtık Çizgileri", "desc": "Kesim hattı boyunca doku boyunca uzanan kesintisiz yarıklar izlenir.", "isKey": True},
                    {"title": "Kalsifikasyon Hasarı", "desc": "Kalsifiye doku ve cerrahi teller jilet ağzını anında çentikler.", "isKey": True},
                    {"title": "Dekalsifikasyon Şartı", "desc": "Kemikli materyaller yumuşatılmadan mikrotoma bağlanamaz.", "isKey": False}
                ],
                "table": {
                    "title": "Mikrotomi Bıçak Çizgileri ve Önleme Yöntemleri",
                    "headers": ["Sorun Nedeni", "Dokudaki Morfolojik Yansıması", "Teknik Çözüm"],
                    "rows": [
                        ["Körelmiş / Çentikli Jilet", "Kesit boyunca düz paralel yırtık hatları", "Jileti lateral olarak kaydırmak veya yeni jilet takmak"],
                        ["Dokuda Sert Kalsiyum", "Bıçağın takılması, dokuda parçalanma ve çizilme", "Bloğu yüzeyel asit solüsyonuna (dekalsifiye edici) basmak"],
                        ["Cerrahi Zımba (Stapler) Teli", "Jilet ağzında derin çentik, dokuda derin yırtık", "Makroskopide tüm zımba ve metallerin mıknatıs/pensle temizlenmesi"],
                        ["Parafin Kalıntısı", "Bıçak arkasında biriken mumun kesiti çizmesi", "Bıçak tutucuyu ksilene batırılmış gazlı bezle temizlemek"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Mikrotom kesitlerinde kesim doğrultusunda paralel yırtık ve çizgi hatlarının görülmesi 'bıçak çentiği' (knife mark) artefaktıdır.",
                "📌 [TEKNİK SPOT] Dokudaki kalsiyum çökeltileri ve cerrahi zımbalar mikrotom jiletini çentikleyen başlıca nedenlerdir.",
                "💡 [ÖĞRENME İPUCU] Bir preparatta bıçak çizgisi tümör alanını yırtmışsa patolog derin seri kesit aldırarak sağlam lam ister."
            ],
            "medicalTerms": [
                {"term": "Bıçak Çentiği (Knife Mark)", "explanation": "Mikrotom jiletindeki hasar nedeniyle kesit boyunca uzanan paralel yırtılma çizgileridir."},
                {"term": "Dekalsifikasyon", "explanation": "Kemik ve sert kireç odaklarından kalsiyumun asit veya EDTA ile uzaklaştırılması işlemidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Bıçak Çentiği Oluşumu ve Düzeltme Zinciri",
                    [
                        "1. Sert Odak Teması: Dokudaki kalsifikasyon veya cerrahi zımba teli mikrotom jiletine çarpar",
                        "2. Jilet Çentiklenmesi: Çarpmanın etkisiyle jiletin kesici ağzında mikroskobik bir çentik açılır",
                        "3. Paralel Yırtılma: Blok her aşağı inişinde hasarlı çentik doku kesitini dikey hat boyunca yarar",
                        "4. Görsel Tespit: Su banyosuna aktarılan parafin şeritte yarık çizgisi çıplak gözle fark edilir",
                        "5. Jilet Değişimi: Teknisyen jileti yana kaydırıp keskin bölgeye geçer ve pürüzsüz kesit elde eder"
                    ]
                ),
                make_micro_quiz(
                    "Mikroskop altında incelenen bir lenf nodu biyopsisinde doku kesiti boyunca birbirine paralel uzanan düz yırtık ve çatlak çizgilerinin görülmesi aşağıdaki teknik hatalardan hangisinin göstergesidir?",
                    {
                        "A": "Formalinin nötral tamponlu olması",
                        "B": "Mikrotom jiletinde çentik bulunması (knife mark artefaktı)",
                        "C": "Eozin boyasının asidik olması",
                        "D": "Dokunun kriostatta dondurulması",
                        "E": "Hastanın yaşının ileri olması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Nötral tamponlu formalin doku morfolojisini en iyi koruyan standart fiksatiftir.",
                        "B": "Doğru. Kesim hattına paralel uzanan düz yırtıklar mikrotom jiletindeki çentiğin dokuyu yırtmasıdır.",
                        "C": "Yanlış. Eozin sitoplazmayı boyayan asidik bir boyadır, mekanik yırtık yapmaz.",
                        "D": "Yanlış. Dondurma kesitleri mikrotom jilet çentiğinden farklı buz artefaktları oluşturur.",
                        "E": "Yanlış. Hastanın yaşının mekanik bıçak çizgileriyle hiçbir biyolojik bağı yoktur."
                    }
                ),
                make_cloze(
                    "Mikrotom jiletindeki kusurlar nedeniyle doku kesiti boyunca oluşan paralel yırtık hatlarına bıçak çentiği artefaktı denir.",
                    "bıçak çentiği",
                    "Jilet hasarına bağlı paralel yırtılma çizgisi terimi"
                )
            ]
        },

        # Adım 86
        {
            "slideNumber": 86,
            "title": "Mikrotomi Kesim Hataları II: Chatter (Titreme / Panjur) ve Kalın-İnce Kesitler",
            "subtitle": "Bıçağın dokuya çarparken mikro-titreşim yapması; mikroskopta panjur benzeri dalgalı kalınlık çizgilerine (chatter) yol açar.",
            "badge": "Chatter Artefaktı",
            "badgeColor": "purple",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """==Chatter (Titreme / Panjur Artefaktı)==; mikrotom bıçağının kesim sırasında titremesi sonucu dokuda dalgalı kalınlık şeritleri oluşturmasıdır.

Bıçak doku bloğuna girdiğinde mikro-titreşimler yaparak doku üzerinden zıplar. Bunun sonucunda kesit üzerinde kesim yönüne dik, birbirine paralel ==panjur veya jaluzi benzeri dalgalı açık ve koyu şeritler== izlenir. Başlıca nedenleri; bıçak tutucusunun veya klemens vidalarının gevşek olması, bıçak eğim açısının (clearance angle) 3-5 derecelik ideal aralık dışına çıkması ve aşırı sertleşmiş dokulardır. Kalın kısımlar ışığı geçirmediğinden hücresel detaylar ve nükleer atipi net değerlendirilemez.

> [MEKANİK TANI] Kesim yönüne dik panjur dalgaları gevşek bıçak veya aşırı sert doku titreşimidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Panjur / Jaluzi Görünümü", "desc": "Bıçağın rezonans titreşimiyle kesit yüzeyinde dalgalı kalınlık çizgileri oluşur.", "isKey": True},
                    {"title": "Gevşek Klemens Nedeni", "desc": "Mikrotom vidalarının gevşekliği veya hatalı bıçak açısı titreşimi tetikler.", "isKey": True},
                    {"title": "Aşırı Sert Doku Rolü", "desc": "Fibröz dokular ve ksilende taşlaşmış bloklar bıçağı zıplatır.", "isKey": False}
                ],
                "table": {
                    "title": "Chatter Artefaktı ve Önleme Kriterleri",
                    "headers": ["Parametre", "Hatalı Durum", "Doğru Standart Değer"],
                    "rows": [
                        ["Bıçak Eğim Açısı (Clearance)", "Aşırı dik (>8°) veya aşırı yatık (<2°)", "3 ila 5 derece ideal kesim açısı"],
                        ["Klemens Vidaları", "Gevşek, titreşime açık", "Alyan anahtarıyla torkunda sıkılmış sabit klemens"],
                        ["Kesim Hızı", "Çarkın aşırı hızlı ve sert çevrilmesi", "Sabit, homojen ve ritmik dönüş hızı"],
                        ["Doku Sertliği", "Ksilende günlerce bekletilmiş taş doku", "Kontrollü şeffaflaştırma, blok yüzeyini nemlendirme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Mikroskopta doku üzerinde kesim yönüne dik panjur (jaluzi) şeklinde dalgalı kalınlık çizgilerinin görülmesine 'chatter' (titreme) artefaktı denir.",
                "📌 [TEKNİK SPOT] Chatter artefaktı en sık bıçak klemens vidalarının gevşek olmasından veya bıçak açısının hatalı ayarlanmasından kaynaklanır.",
                "💡 [ÖĞRENME İPUCU] Uterus leiomiyomu (ur) gibi sert kas dokularında kesim öncesi bloğun üzerine ıslak buz koyarak yumuşatmak chatter'ı önler."
            ],
            "medicalTerms": [
                {"term": "Chatter (Jaluzi Artefaktı)", "explanation": "Mikrotom bıçağının titremesiyle kesit yönüne dik oluşan panjur benzeri dalgalı şeritlerdir."},
                {"term": "Clearance Açısı", "explanation": "Bıçak arkası ile parafin blok arasında titreşimi önleyen ideal eğim açısıdır (3-5°)."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Mikrotomi Kesim Kusurları Karşılaştırması",
                    ["Artefakt Adı", "Mikroskobik Belirti", "Başlıca Nedeni"],
                    [
                        [
                            ("Bıçak Çentiği (Knife Mark)", False),
                            ("Kesim yönüne paralel düz yırtık hatları", True, "Doku boyunca uzanan yarık"),
                            ("Jilet ağzında çentik veya sert kalsiyum", False)
                        ],
                        [
                            ("Chatter (Titreme)", False),
                            ("Panjur / jaluzi benzeri dalgalı açık-koyu bantlar", True, "Kesim yönüne dik dalgalanma"),
                            ("Gevşek bıçak tutucu veya aşırı sert doku", False)
                        ],
                        [
                            ("Floater (Doku Bulaşı)", False),
                            ("Preparatın köşesinde yabancı doku parçası", True, "Başka hastaya ait hücre odağı"),
                            ("Kirli su banyosu veya temizlenmemiş cımbız", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Uterus leiomiyomu (miyom) biyopsisinde mikroskop altında kesit boyunca jaluzi veya panjur şeklinde birbirini izleyen açık ve koyu dalgalı kalınlık çizgilerinin izlenmesi (Chatter artefaktı) en olası hangi teknik kusurdan kaynaklanır?",
                    {
                        "A": "Formalinin %10 konsantrasyonda olması",
                        "B": "Mikrotom bıçağının veya blok klemensinin gevşek olması ve sert dokuyu keserken titremesi",
                        "C": "Hematoksilen boyasının yeni hazırlanmış olması",
                        "D": "Doku takibinde erimiş parafin kullanılması",
                        "E": "Lamelin camdan yapılmış olması"
                    },
                    "B",
                    {
                        "A": "Yanlış. %10 nötral tamponlu formalin standart ve ideal fiksasyon konsantrasyonudur.",
                        "B": "Doğru. Bıçağın veya klemensin gevşek olması sert dokuda titreyerek jaluzi benzeri chatter yapar.",
                        "C": "Yanlış. Boyanın tazeliği boyanma kalitesini artırır, mekanik kalınlık dalgalanması yapmaz.",
                        "D": "Yanlış. Sıvı parafin bloklamanın temel standart ortamıdır.",
                        "E": "Yanlış. Lam camının kalitesi mikrotom kesim mekaniğini etkilemez."
                    }
                ),
                make_cloze(
                    "Mikrotom bıçağının kesim sırasında titremesi sonucu doku kesitinde oluşan panjur veya jaluzi benzeri dalgalı kalınlık çizgilerine chatter adı verilir.",
                    "chatter",
                    "Titreme sonucu oluşan panjur artefaktının İngilizce/evrensel adı"
                )
            ]
        },

        # Adım 87
        {
            "slideNumber": 87,
            "title": "Su Banyosu ve Lam Hataları: Katlantı, Kabarcık ve Floater Tehlikesi",
            "subtitle": "Kirli su banyosundan sıçrayan başka bir hastanın doku parçası (floater); sağlıklı bir preparata yapışarak yalancı kanser tanısına yol açabilir.",
            "badge": "Floater Tehlikesi",
            "badgeColor": "red",
            "discipline": "Tanısal Güvenlik",
            "synthesisNarrative": """Flotasyon ve montaj aşamalarındaki teknik hatalar ile doku bulaşması (floater) hasta tanı güvenliğini doğrudan tehdit eder.

==Floater (Doku Bulaşı)==; önceki hastanın kesitinden su banyosunda kalan tümör kırıntısının yeni hastanın lamına yapışmasıdır. Patolog bu yabancı odağı hastanın lezyonu sanırsa sağlıklı kişiye yalancı kanser tanısı konabilir. Floater; ana dokuyla stromal bağı olmayan, farklı odak düzleminde yüzen ve reaksiyon içermeyen izole bir odaktır. Su banyosunda açılmayan kesitlerin katlanması (fold) koyu boyanarak atipiyi taklit eder; lamel kapatılırken giren hava kabarcıkları ise dokuyu siyah halkalarla örter.

> [GÜVENLİK YASASI] Her bloktan sonra su banyosu temizlenmeli, izole lezyonlarda floater olasılığı dışlanmalıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Floater Malpraktis Riski", "desc": "Başka hastanın kanser kırıntısının preparata yapışması yalancı pozitiflik yaratır.", "isKey": True},
                    {"title": "Su Banyosu Temizliği", "desc": "Her hastadan sonra su banyosu yüzeyi filtre kağıdıyla sıyrılarak temizlenir.", "isKey": True},
                    {"title": "Hava Kabarcığı Karartması", "desc": "Lamel altındaki hava kabarcıkları siyah halkalar yaparak dokuyu gizler.", "isKey": False}
                ],
                "table": {
                    "title": "Su Banyosu ve Montaj Hatalarının Karşılaştırması",
                    "headers": ["Artefakt", "Oluşum Mekanizması", "Doğurduğu Tanısal Tehlike", "Önleme Yöntemi"],
                    "rows": [
                        ["Floater (Kontaminasyon)", "Kirli su banyosu veya cımbızdan başka hasta dokusunun yapışması", "Sağlıklı hastaya yanlışlıkla kanser tanısı verilmesi", "Her blok değişiminde su banyosunun filtre kağıdıyla silinmesi"],
                        ["Doku Katlantısı (Fold)", "Su banyosunda açılmayan kesitin kendi üzerine katlanması", "Çift kat boyanarak yalancı atipik hücre kümesi sanılması", "Su banyosu sıcaklığını 42°C'de tutarak tam açılma sağlamak"],
                        ["Hava Kabarcığı", "Lamel kapatılırken reçine arasına hava girmesi", "Dokunun mikroskopta siyah optik artefaktla örtülmesi", "Lameli 45° açıyla dikkatlice kapatmak, gerekirse lameli söküp yenilemek"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Mikrotom su banyosundan veya cımbızdan başka bir hastanın doku kırıntısının preparata bulaşmasına 'floater' artefaktı denir.",
                "📌 [GÜVENLİK SPOTU] Floater artefaktı dokunun ana kütlesiyle hiçbir hücresel ve stromal bağlantı göstermez, farklı bir odak düzleminde izlenir.",
                "🚨 [KRİTİK UYARI] Normal bir endometrium biyopsisinde tek bir odakta yabancı kolon kanseri hücreleri görülürse derhal floater şüphesiyle blok derinleştirilmelidir."
            ],
            "medicalTerms": [
                {"term": "Floater", "explanation": "Su banyosundan veya aletlerden preparata bulaşan başka hastaya ait yabancı doku parçasıdır."},
                {"term": "Montaj (Mounting)", "explanation": "Boyanmış doku kesitinin reçine damlatılarak lamel ile kalıcı şekilde kapatılması işlemidir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Mide biyopsisinde normal gastrik mukoza yanında dokuyla bağlantısız, lamın kenarında yüzen tek bir küçük 'invaziv karsinom' odağı görülmesi senaryosu.",
                    [
                        {
                            "text": "Hastaya derhal 'Mide İnvaziv Adenokarsinomu' raporu verilerek acil total mide rezeksiyonuna gönderilir.",
                            "isCorrect": False,
                            "feedback": "Korkunç bir tıbbi hata! İzole yüzen, stromal bağlantısı olmayan odak bir floater (başka hastanın bulaşı) olabilir; teyit edilmeden organ çıkarılamaz."
                        },
                        {
                            "text": "Floater şüphesi düşünülür; parafin bloktan derin seri kesitler istenir, o gün kesilen diğer hastaların kasetleri taranır ve klinikle görüşülür.",
                            "isCorrect": True,
                            "feedback": "Mükemmel tanısal güvenlik refleksi! Derin kesitlerde odak kaybolursa ve stromal uyum yoksa bunun bir floater olduğu kanıtlanır ve gereksiz ameliyat önlenir."
                        },
                        {
                            "text": "Preparat çöpe atılır ve inceleme iptal edilir.",
                            "isCorrect": False,
                            "feedback": "Hatalı yaklaşım! Biyopsi değerlidir, derin kesitlerle doğrulanmalıdır."
                        }
                    ]
                ),
                make_cloze(
                    "Mikrotom su banyosundan başka bir hastaya ait doku kırıntısının preparata yapışarak kontaminasyon oluşturmasına floater adı verilir.",
                    "floater",
                    "Laboratuvar bulaşı yabancı doku parçacığının evrensel adı"
                ),
                make_micro_quiz(
                    "Patoloji uzmanının mikroskopta incelerken dokunun kenarında gördüğü küçük bir tümör hücresi odağının hastanın kendi lezyonu mu yoksa laboratuvardan sıçrayan bir 'floater' mı olduğunu ayırt etmede aşağıdaki bulgulardan hangisi FLOATER lehinedir?",
                    {
                        "A": "Odağın çevre stroma ile desmoplastik reaksiyon ve damarsal bağlantı göstermesi",
                        "B": "Odağın doku ana kütlesiyle hiçbir anatomik bağlantısının olmaması, farklı bir derinlik düzleminde yüzmesi ve çevresinde sıfır hücresel reaksiyon olması",
                        "C": "Hastanın tomografisinde o bölgede 5 cm kitle bulunması",
                        "D": "Tümör hücrelerinin sitokeratin pozitif boyanması",
                        "E": "Tümörün cerrahi sınırda devam etmesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Desmoplazi ve stroma bağlantısı lezyonun hastanın kendi gerçek tümörü olduğunu kanıtlar.",
                        "B": "Doğru. Floater ana dokudan bağımsız yüzer, farklı odak düzlemindedir ve çevre doku yanıtı içermez.",
                        "C": "Yanlış. Radyolojik kitle varlığı hastada gerçek bir tümör lehine güçlü bir klinik bulgudur.",
                        "D": "Yanlış. Sitokeratin epitel kökenini gösterir ancak kontaminasyon ayrımı yapmaz.",
                        "E": "Yanlış. Cerrahi sınır pozitifliği ameliyatla çıkarılan dokunun kendi sınır ilişkisidir."
                    }
                )
            ]
        },

        # Adım 88
        {
            "slideNumber": 88,
            "title": "Cerrahi Müdahale Artefaktları: Koter (Termal) Hasarı ve Crush (Ezilme) Hasarı",
            "subtitle": "Cerrahın elektrokoter ile dokuyu yakması veya forsepsle aşırı sıkması; hücreleri kömürleştirip uzatarak kanser tanısını imkansız kılabilir.",
            "badge": "Cerrahi Artefaktlar",
            "badgeColor": "amber",
            "discipline": "Cerrahi Patoloji",
            "synthesisNarrative": """Cerrahi girişimlerde kullanılan elektrokoter ısısı ve forsepslerin ezici mekanik travması hücresel morfolojiyi tanınmaz hale getirebilir.

==Koter (Termal) Hasarı==; elektrokoterin yüksek ısısıyla doku proteinlerinin pişmesidir. Kesim sınırındaki hücreler kömürleşir, nükleuslar iğsi uzar ve sitoplazmalar camsı pembe bir kütleye döner. Bu durum cerrahi sınırda tümör varlığının değerlendirilmesini imkansızlaştırır. ==Crush (Ezilme) Hasarı== ise penslerin dokuyu aşırı sıkmasıyla meydana gelir. Çekirdek zarı yırtılır ve serbest DNA koyu mavi şeritler halinde dokuya akar. Bu artefakt lenfoma ve küçük hücreli akciğer karsinomu tanısını zorlaştırır.

> [CERRAHİ İLKE] Koter cerrahi sınırdan uzak tutulmalı, biyopsiler forsepsle ezilmeden nazikçe taşınmalıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Koter Termal Yanığı", "desc": "Aşırı ısıyla uzamış, kömürleşmiş ipliksi nükleuslar cerrahi sınır değerlendirmesini bozar.", "isKey": True},
                    {"title": "Crush (Ezilme) Hasarı", "desc": "Forseps sıkmasıyla DNA dışarı sızar; kromatin bulaşması (smearing) oluşur.", "isKey": True},
                    {"title": "Lenfoma ve Akciğer Riski", "desc": "Küçük hücreli tümörlerde ezilme morfolojik tanıyı imkansız hale getirebilir.", "isKey": False}
                ],
                "table": {
                    "title": "Cerrahi Kaynaklı Artefaktlar ve Patolojik Sonuçları",
                    "headers": ["Cerrahi Müdahale", "Fiziksel Neden", "Mikroskobik Artefakt Görünümü", "Doğurduğu Tanısal Hasar"],
                    "rows": [
                        ["Elektrokoter", "Yüksek voltajlı ısı ile kesme ve yakma", "İğsi uzamış siyah çekirdekler, amorf eozinofilik bant", "Cerrahi sınırın temiz mi tümörlü mü olduğunun bilinememesi"],
                        ["Forsepsle Aşırı Sıkma", "Mekanik ezici travma (Crush)", "Parçalanmış DNA'nın koyu mavi şeritler halinde akması", "Küçük hücreli karsinom ile lenfosit ayrımının yapılamaması"],
                        ["Kuru Gazlı Beze Koyma", "Havadaki su kaybı ve kuruma", "Hücre zarlarının büzüşmesi, piknotik nükleus", "Sitoplazma sınırlarının silinmesi ve soluk boyanma"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Biyopsi materyalinin cerrahi forsepsle aşırı sıkılması sonucu DNA'nın dışarı akarak koyu mavi şeritler oluşturmasına 'crush artefaktı' denir.",
                "📌 [TANI SPOTU] Elektrokoter artefaktı rezeksiyon sınırındaki hücreleri uzatıp kömürleştirerek cerrahi sınır değerlendirmesini güvenilmez kılar.",
                "💡 [ÖĞRENME İPUCU] Küçük hücreli akciğer karsinomu bronkoskopi forseps biyopsilerinde en sık crush artefaktı gösteren tümördür."
            ],
            "medicalTerms": [
                {"term": "Koter Artefaktı", "explanation": "Elektrokoter ısısıyla hücrelerin kömürleşip uzaması ve nükleer detayların silinmesidir."},
                {"term": "Crush Artefaktı", "explanation": "Pens basısıyla nükleusların patlayarak serbest DNA'nın koyu mavi şeritler yapmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Koter Termal Hasarı vs Crush (Ezilme) Hasarı",
                    "Koter (Termal) Artefaktı",
                    "Crush (Ezilme) Artefaktı",
                    [
                        "Cerrahi elektrokoterin yüksek ısısından kaynaklanır",
                        "Hücre çekirdekleri ipliksi, uzamış ve kömürleşmiş görünür",
                        "Sitoplazma camsı homojen kırmızı kütleye döner",
                        "En çok rezeksiyon cerrahi sınırlarında görülür"
                    ],
                    [
                        "Cerrahi pens ve forsepslerin mekanik sıkmasından kaynaklanır",
                        "Nükleus zarı yırtılır ve serbest DNA mavi şeritler yapar",
                        "Sitoplazma parçalanarak hücre sınırları tamamen kaybolur",
                        "En çok küçük forseps ve lenf nodu biyopsilerinde görülür"
                    ]
                ),
                make_micro_quiz(
                    "Bronkoskopi esnasında akciğerdeki submukozal bir lezyondan forseps ile biyopsi alınırken dokunun pens ile aşırı sıkılması sonucu nükleusların patlayarak kromatin DNA'sının mavi şeritler halinde dokuya saçılması ve hücresel mimarinin kaybolması hangi artefakt türüdür?",
                    {
                        "A": "Chatter artefaktı",
                        "B": "Crush (Ezilme) artefaktı",
                        "C": "Floater artefaktı",
                        "D": "Formalin pigmenti",
                        "E": "Bıçak çentiği"
                    },
                    "B",
                    {
                        "A": "Yanlış. Chatter mikrotom bıçağının titreşmesiyle oluşan mekanik dalgalanmadır.",
                        "B": "Doğru. Forseps sıkmasıyla DNA'nın dışarı akıp mavi şeritler yapması crush (ezilme) artefaktıdır.",
                        "C": "Yanlış. Floater su banyosundan sıçrayan yabancı doku parçacığı kontaminasyonudur.",
                        "D": "Yanlış. Formalin pigmenti asidik ortamda çöken asit formaldehit hematin tuzudur.",
                        "E": "Yanlış. Bıçak çentiği hasarlı mikrotom jiletinin dokuda yarattığı paralel yırtıklardır."
                    }
                ),
                make_cloze(
                    "Cerrahi forsepslerin küçük doku parçalarını aşırı sıkıştırması sonucu nükleer DNA'nın dışarı akarak mavi şeritler oluşturmasına crush artefaktı adı verilir.",
                    "crush",
                    "Ezilme sonucu oluşan artefaktın uluslararası tıbbi adı"
                )
            ]
        },

        # Adım 89: [TEKRAR SAYFASI - CHECKPOINT 9]
        {
            "slideNumber": 89,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Histopatolojik Artefaktlar ve Tanısal Ayırıcı Tanı",
            "subtitle": "Bölüm 9'un otoliz, formalin pigmenti, takip hataları, bıçak çentiği, chatter, floater ve koter/crush konularını toparlayan sentez istasyonu.",
            "badge": "Checkpoint 9",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 9,
            "synthesisNarrative": """Bu kontrol noktası; preanalitik ve laboratuvar basamaklarındaki teknik kusurların nasıl tanısal tuzaklara dönüştüğünü özetler.

Geç fiksasyon otoliz ve 'hayalet hücre' yaratırken, pH < 6.0 asidik formalin siyah 'formalin pigmenti' çöktürür. Takipte su tutan alkol soluk boyanmaya, sulu ksilen 'sütümsü bulanıklığa', >65°C parafin ise 'doku yanığına' yol açar. Mikrotomda hasarlı jilet paralel 'bıçak çentiği' yırtıkları, gevşek klemens ise kesim yönüne dik panjur benzeri 'chatter' bantları üretir. Kirli su banyosundan yapışan 'floater' dokuları yalancı kanser tanısı koydurabilir. Ameliyathanede koter hücreleri kömürleştirirken, forseps sıkması serbest DNA'yı yayarak 'crush' artefaktı yapar.

> [BÖLÜM SENTEZİ] Patolog yalnızca hastalığı değil, cerrahın ve laboratuvarın dokuda bıraktığı teknik izleri de tanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "En Tehlikeli: Floater", "desc": "Başka hastanın kanser hücresinin preparata bulaşması malpraktis riskidir.", "isKey": True},
                    {"title": "Otoliz vs Koter/Crush", "desc": "Otoliz enzimatik erimedir; koter termal kömürleşme, crush ise mekanik ezilmedir.", "isKey": True},
                    {"title": "Mikrotom İkilisi", "desc": "Bıçak çentiği paralel yırtık; chatter ise dik panjur çizgileridir.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 9 Bütün Artefaktların Ayırıcı Tanı ve Çözüm Tablosu",
                    "headers": ["Artefakt Türü", "Oluşum Basamağı", "Mikroskobik Görünüm", "Önleme / Düzeltme Yolu"],
                    "rows": [
                        ["Otoliz", "Geç fiksasyon", "Hayalet hücreler, silik çekirdek, dökülen epitel", "Dokuyu derhal %10 formaline koymak"],
                        ["Formalin Pigmenti", "Asidik fiksatif (pH < 6.0)", "Damar içinde siyah-kahverengi çift kırınımlı granüller", "pH 7.0 nötral tamponlu formalin kullanmak"],
                        ["Sütümsü Ksilen", "Kötü dehidrasyon", "Ksilen tankında beyazlık, dokuda mikro-boşluklar", "Alkol ve ksilen banyolarını düzenli yenilemek"],
                        ["Doku Yanığı", "Aşırı sıcak parafin (>65°C)", "Kavrulmuş büzüşük doku, piknotik nükleus", "Parafin etüv sıcaklığını 58-60°C'de sabitlemek"],
                        ["Bıçak Çentiği", "Hasarlı mikrotom jileti", "Kesim yönüne paralel düz yırtık hatları", "Jileti yana kaydırmak veya değiştirmek"],
                        ["Chatter", "Gevşek mikrotom bıçağı", "Kesim yönüne dik panjur (jaluzi) dalgalanmaları", "Vidaları sıkmak, bıçak açısını 3-5° yapmak"],
                        ["Floater", "Kirli su banyosu / cımbız", "Ana dokudan bağımsız yüzen yabancı kanser odağı", "Su banyosunu her hastada filtre kağıdıyla silmek"],
                        ["Crush Artefaktı", "Forsepsle aşırı sıkma", "Mavi şeritler halinde dokuya yayılan serbest DNA", "Biyopsi alırken dokuyu ezmeden nazik tutmak"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Floater artefaktı, mikrotom su banyosundan başka hastanın dokusunun bulaşmasıdır ve yalancı kanser tanısına yol açabilir.",
                "📌 [SINAV SPOTU] Asit formaldehit hematin (formalin pigmenti) pH < 6.0 asit ortamda oluşur; nötral tamponlu formalinle önlenir.",
                "📌 [SINAV SPOTU] Kesim yönünde paralel yırtıklar 'bıçak çentiği'; kesim yönüne dik panjur dalgaları 'chatter' artefaktıdır."
            ],
            "medicalTerms": [
                {"term": "Dekalsifikasyon", "explanation": "Kemik dokulardan kalsiyumun kimyasal olarak uzaklaştırılarak kesilebilir hale getirilmesidir."},
                {"term": "Entellan", "explanation": "Lam ile lamel arasına konarak dokunun kalıcı saklanmasını sağlayan montaj reçinesidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p9-1",
                    "Patoloji laboratuvarında 'Floater' artefaktı nasıl oluşur ve klinik tanı açısından neden en tehlikeli artefakttır?",
                    "Önceki hastanın tümör kırıntısının su banyosu veya cımbız yoluyla sıradaki hastanın lamına bulaşmasıyla oluşur. Sağlıklı bir hastaya yanlışlıkla malignite tanısı konulmasına ve gereksiz radikal cerrahiye yol açabileceği için en tehlikeli artefakttır.",
                    "Su banyosu kontaminasyonu ve yalancı kanser",
                    "Tanısal Güvenlik"
                ),
                make_flashcard(
                    "fc-p9-2",
                    "Formalin pigmenti (asit formaldehit hematin) hangi biyokimyasal koşulda oluşur ve laboratuvarda nasıl tamamen engellenir?",
                    "Tamponlanmamış formalinin pH'sı 6.0 altına düştüğünde serbest kalan hemoglobinin asit formaldehitle birleşmesi sonucu oluşur. Laboratuvarda daima pH 7.0-7.4 olan nötral tamponlu formalin kullanılarak tamamen engellenir.",
                    "Asit pH (<6.0) ve nötral tamponlama",
                    "Fiksasyon Artefaktları"
                ),
                make_flashcard(
                    "fc-p9-3",
                    "Mikrotomide görülen 'Bıçak Çentiği' (Knife mark) ile 'Chatter' (Panjur/Titreme) artefaktları arasındaki morfolojik ve mekanik farklar nelerdir?",
                    "Bıçak çentiği hasarlı jilet ağzı nedeniyle kesim yönüne paralel uzanan düz yırtık hatlarıdır. Chatter ise gevşek klemens veya sert doku titreşimiyle kesim yönüne dik oluşan panjur benzeri dalgalı şeritlerdir.",
                    "Paralel yırtık (çentik) vs Dik panjur dalgası (chatter)",
                    "Mikrotomi Hataları"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 9'da incelenen histopatolojik artefaktlar dikkate alındığında, aşağıdaki teknik sorun - artefakt eşleştirmelerinden hangisi YANLIŞTIR?",
                    {
                        "A": "Mikrotom su banyosunun temizlenmemesi sonucu başka hastanın tümörünün bulaşması → Floater artefaktı",
                        "B": "Mikrotom bıçak tutucu vidalarının gevşek olması → Chatter (panjur) artefaktı",
                        "C": "Dokunun pH 5.0 asidik formalinde fiksasyona bırakılması → Asit formaldehit hematin (formalin pigmenti)",
                        "D": "Endoskopik biyopside forsepsin dokuyu aşırı sıkması → Crush (ezilme) artefaktı",
                        "E": "Doku parçalarının kalıba dik olarak gömülmesi → Bıçak çentiği ve doku yanığı artefaktı"
                    },
                    "E",
                    {
                        "A": "Doğru eşleştirme. Su banyosundan bulaşan yabancı doku parçası floater artefaktıdır.",
                        "B": "Doğru eşleştirme. Gevşek klemens vidaları kesim sırasında titreşerek chatter oluşturur.",
                        "C": "Doğru eşleştirme. pH 6.0 altındaki asidik formalin asit formaldehit hematin pigmenti çöktürür.",
                        "D": "Doğru eşleştirme. Forsepsle mekanik sıkıştırma nükleer DNA'yı saçarak crush artefaktı yapar.",
                        "E": "Yanlış eşleştirme (aranan cevap). Dokuyu kalıba dik gömmek tüm katmanları gösteren doğru oryantasyon tekniğidir."
                    }
                ),
                make_interactive_table(
                    "Artefaktlar ve Klinik Ayırıcı Tanı Tuzakları",
                    ["Artefakt Adı", "Karıştığı Gerçek Patoloji", "Doğru Ayrım İpucu"],
                    [
                        [
                            ("Formalin Pigmenti", False),
                            ("Malign Melanom / Hemosiderin", True, "Siyah granüler birikim"),
                            ("Damar lümeninde yerleşir, çift kırınımlıdır", False)
                        ],
                        [
                            ("Floater (Bulaş)", False),
                            ("Gerçek Kanser Metastazı", True, "İzole yabancı tümör adacığı"),
                            ("Çevresinde stroma ve hücresel reaksiyon yoktur", False)
                        ],
                        [
                            ("Koter Hasarı", False),
                            ("Cerrahi Sınırda Kanser İnvazyonu", True, "İğsi uzamış nükleuslar"),
                            ("Termal yanık hattında kömürleşme ile birliktedir", False)
                        ]
                    ]
                )
            ]
        }
    ]
