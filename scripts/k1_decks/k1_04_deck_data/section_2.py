# -*- coding: utf-8 -*-
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
        {
            "slideNumber": 10,
            "title": "Genetik Kusurlar ve Hücre Hasarı",
            "subtitle": "Kromozom anomalilerinden yanlış katlanmış protein birikimine",
            "badge": "Genetik",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Genetik anormallikler hücre hasarına yol açan en temel intrinsik faktörlerdendir. Genetik "
                "kusurlar Down sendromunda olduğu gibi kaba kromozomal anomalilerden, orak hücreli anemideki "
                "gibi tek bir baz mutasyonuna kadar uzanır. Bu kusurlar enzim eksikliğine bağlı metabolik "
                "ara ürün birikimine veya fonksiyonel protein yetersizliğine neden olabilir.\n\n"
                "> [TEMEL İLKE] Yanlış katlanmış proteinlerin endoplazmik retikulumda birikmesi 'ER stresi' "
                "yaratarak hücreyi apoptoza sürükleyen kritik bir genetik hasar mekanizmasıdır.\n\n"
                "Ayrıca tümör baskılayıcı gen mutasyonları hücrenin DNA hasarını tanımasını engelleyerek "
                "hasarlı hücrelerin çoğalmasına ve malign transformasyona yol açar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Kromozom Anomalileri", "desc": "Geniş DNA delesyonu veya trizomilerin hücresel metabolizmayı bozmasıdır.", "isKey": True},
                    {"title": "Nokta Mutasyonları", "desc": "Hemoglobinopatiler gibi tek aminoasit değişimiyle oluşan moleküler patolojidir.", "isKey": False},
                    {"title": "ER Stresi", "desc": "Katlanamamış hatalı proteinlerin hücreyi intihara sürüklemesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Genetik Hasar Mekanizmaları",
                    "headers": ["Genetik Kusur", "Klinik Örnek", "Hücresel Hasar Mekanizması"],
                    "rows": [
                        ["Kromozom Trizomisi", "Down Sendromu", "Gen dozu dengesizliği ve gelişimsel arrest"],
                        ["Nokta Mutasyonu", "Orak Hücreli Anemi", "HbS polimerizasyonu, eritrosit lizisi ve oraklaşma"],
                        ["Katlanma Defekti", "Alfa-1 Antitripsin Eksikliği", "Hepatik ER stresi ve apoptoz, akciğerde amfizem"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yanlış katlanmış protein birikimi endoplazmik retikulumda birikerek 'ER stresi' üzerinden apoptozu tetikler.",
                "📌 [YÜKSEK VERİM] Orak hücreli anemide tek bir nokta mutasyonu mikrovasküler tıkanmaya ve iskemik doku nekrozuna yol açar."
            ],
            "medicalTerms": [
                {"term": "ER Stresi", "explanation": "Endoplazmik retikulum lümeninde hatalı katlanmış protein birikimiyle tetiklenen apoptoz yolağıdır."},
                {"term": "Polimerizasyon", "explanation": "Anormal hemoglobin moleküllerinin deoksijene halde fibriller oluşturarak eritrositi deforme etmesidir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Endoplazmik retikulumda yanlış katlanmış proteinlerin birikmesi sonucu hücreyi apoptoza sürükleyen duruma ER stresi adı verilir.",
                    "ER stresi",
                    "Organel Stresi"
                ),
                make_active_recall(
                    "Genetik bir bozukluk olan Alfa-1 Antitripsin eksikliğinde karaciğerde hasar nasıl oluşur?",
                    "Anormal katlanan Z mutant proteini hepatosit ER'sinden salgılanamaz; ER lümeninde birikerek kronik ER stresine, hepatosit ölümüne ve siroza yol açar."
                )
            ]
        },
        {
            "slideNumber": 11,
            "title": "Beslenme Dengesizlikleri ve Hücresel Hasar",
            "subtitle": "Protein-kalori malnütrisyonundan obezite ve ateroskleroza",
            "badge": "Metabolizma",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Beslenme dengesizlikleri hem yetersizlik hem de aşırılık boyutlarıyla hücresel zedelenmeye "
                "yol açar. Yetersiz beslenme durumunda (protein-kalori malnütrisyonu: Marasmus ve Kwaşiorkor) "
                "hücreler protein sentezi için aminoasit bulamaz; plazma proteinleri düşer ve hücresel atrofi "
                "gelişir. Vitamin eksiklikleri spesifik hücresel enzim kofaktörlerini tüketir.\n\n"
                "> [KRİTİK UYARI] Aşırı beslenme ise obezite, tip 2 diyabet ve aterosklerozun temel nedenidir; "
                "vasküler endotelde aşırı kolesterol birikimi hücre hasarını başlatır.\n\n"
                "Aşırı serbest yağ asitleri ve glukoz hücre içinde mitokondriyal elektron kaçağını artırarak "
                "endoplazmik retikulum stresini ve reaktif oksijen radikali (ROS) üretimini körükler."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Yetersiz Alım", "desc": "Marasmus (kalori) ve Kwaşiorkor (protein) sonucu hücresel atrofi ve steatozdur.", "isKey": True},
                    {"title": "Vitamin Eksikliği", "desc": "C vitamini (kollajen sentezi) veya B12 vitamini (DNA sentezi) yetersizliğidir.", "isKey": False},
                    {"title": "Aşırı Alım", "desc": "Hiperkolesterolemi sonucu damar endotel hasarı ve aterom plağı oluşumudur.", "isKey": True}
                ],
                "table": {
                    "title": "Beslenme Bozuklukları ve Hücresel Etkileri",
                    "headers": ["Durum", "Biyokimyasal Kusur", "Morfolojik Hücresel Sonuç"],
                    "rows": [
                        ["Kwaşiorkor", "Ağır protein yetersizliği", "Apoprotein sentezlenemez, karaciğerde yağlanma (steatoz)"],
                        ["Marasmus", "Kalori ve protein eksikliği", "İskelet kası protein yıkımı ve genel atrofi"],
                        ["Aşırı Kolesterol", "LDL oksidasyonu", "Köpük hücresi oluşumu, endotel hasarı, ateroskleroz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kwaşiorkor hastalarında apoprotein sentezlenemediği için trigliseritler hepatositten atılamaz ve masif karaciğer yağlanması gelişir.",
                "📌 [YÜKSEK VERİM] Aterosklerozda endotel hücre hasarını başlatan en önemli etken okside LDL kolesteroldür."
            ],
            "medicalTerms": [
                {"term": "Kwaşiorkor", "explanation": "Yeterli kaloriye rağmen ağır diyet proteini eksikliği sonucu gelişen ödemli malnütrisyon tablosudur."},
                {"term": "Köpük Hücresi", "explanation": "Okside LDL kolesterolü fagosite ederek sitoplazması lipitle dolan makrofaj veya düz kas hücresidir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Protein eksikliğinde apoprotein üretilemediği için karaciğerde trigliserit birikmesiyle steatoz tablosu gelişir.",
                    "steatoz",
                    "Karaciğer Patolojisi"
                ),
                make_before_after(
                    "Beslenme Kaynaklı Hasar",
                    "Protein Yetersizliği (Kwaşiorkor)",
                    "Aşırı Lipit Yükü (Ateroskleroz)",
                    [
                        "Apoprotein sentezi çöker",
                        "Hepatositlerde yağ depolanır",
                        "Hipoalbüminemi ve anazarka ödem"
                    ],
                    [
                        "Dolaşımda okside LDL yükselir",
                        "Endotel altı makrofajlar köpük hücresine döner",
                        "Damar lümeninde darlık ve iskemi"
                    ]
                )
            ]
        },
        {
            "slideNumber": 12,
            "title": "Fiziksel Etkenlerin Neden Olduğu Hücre Hasarı",
            "subtitle": "Travma, sıcaklık uçları, radyasyon ve elektrik akımı",
            "badge": "Fiziksel Hasar",
            "badgeColor": "orange",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Fiziksel etkenler hücreye doğrudan mekanik enerji veya radyasyon aktararak hasar oluşturur. "
                "Mekanik travma hücre zarlarını ve iskeletini fiziksel olarak yırtar. Aşırı yüksek sıcaklıklar "
                "(yanıklar) intraselüler proteinleri hızla pıhtılaştırır (denatürasyon); aşırı soğuk ise "
                "hücre içi buz kristalleri oluşturarak zarları mekanik olarak deler.\n\n"
                "> [TEMEL İLKE] İyonizan radyasyon (X ve gama ışınları), hücre içi suyu radyolize uğratarak "
                "hidroksil serbest radikali (OH*) üretir ve DNA çift zincir kırıklarına yol açar.\n\n"
                "Ani atmosferik basınç düşüşleri (dekompresyon hastalığı / vurgun) kanda çözünmüş nitrojen "
                "gazının kabarcıklaşarak damarları tıkamasına ve kemiklerde avasküler nekroza neden olur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Mekanik Travma", "desc": "Doku bütünlüğünün ve hücre membranlarının doğrudan yırtılmasıdır.", "isKey": False},
                    {"title": "Isı Ekstremleri", "desc": "Yanıkta protein denatürasyonu; donmada buz kristali hasarıdır.", "isKey": True},
                    {"title": "İyonizan Radyasyon", "desc": "Su radyoliziyle hidroksil radikali üretip DNA çift sarmalını kırmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Fiziksel Etkenler ve Hücresel Sonuçları",
                    "headers": ["Fiziksel Etken", "Birincil Hücresel Hedef", "Patolojik Tablo"],
                    "rows": [
                        ["Yüksek Sıcaklık (>45°C)", "Enzimler ve yapısal proteinler", "Protein koagülasyonu ve nekroz"],
                        ["Dondurucu Soğuk", "Hücre zarları ve damarlar", "Buz kristalleri, vazokonstrüksiyon, iskemi"],
                        ["İyonizan Radyasyon", "Nükleer DNA ve su molekülü", "Çift zincir kırıkları, serbest radikal hasarı"],
                        ["Basınç Değişimi", "Mikrosirkülasyon", "Nitrojen gaz embolisi, avasküler nekroz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İyonizan radyasyonun hücreye verdiği hasarın ana aracısı, suyun radyoliziyle oluşan hidroksil (OH*) serbest radikalidir.",
                "📌 [YÜKSEK VERİM] Donma hasarında hücre ölümü sadece buz kristallerinden değil, çözülme sırasındaki mikrovasküler trombozdan kaynaklanır."
            ],
            "medicalTerms": [
                {"term": "Radyoliz", "explanation": "İyonizan radyasyon enerjisiyle su molekülünün parçalanarak serbest radikaller üretmesidir."},
                {"term": "Dekompresyon Hastalığı", "explanation": "Ani basınç azalmasında kanda erimiş nitrojenin gaz kabarcıkları oluşturup damarları tıkamasıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "İyonizan radyasyonun dokularda DNA hasarı yapmasında en etkili serbest radikal suyun radyoliziyle oluşan hidroksil radikalidir.",
                    "hidroksil radikalidir",
                    "Reaktif Oksijen Türü"
                ),
                make_active_recall(
                    "Aşırı soğuk (donma) dokuda hücre ölümünü hangi iki temel mekanizmayla gerçekleştirir?",
                    "1) Hücre içinde oluşan sivri buz kristallerinin membranları delmesi, 2) Soğuğa bağlı vazokonstrüksiyon ve endotel hasarının mikrovasküler tromboza yol açarak iskemi oluşturması."
                )
            ]
        },
        {
            "slideNumber": 13,
            "title": "Hücre Hasarında Genel İlkeler: Tür, Süre ve Şiddet",
            "subtitle": "Etkenin özellikleri ile hücre yanıtı arasındaki biyolojik ilişki",
            "badge": "Genel İlkeler",
            "badgeColor": "blue",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücrenin maruz kaldığı stres karşısındaki kaderi tesadüfi değildir; üç temel kurala dayanır: "
                "1) Zararlı etkenin türü, 2) Etkenin maruziyet süresi, 3) Etkenin şiddeti (dozu). Aynı zararlı "
                "etken, düşük dozda veya kısa süreli uygulandığında hücrede yalnızca geri dönüşümlü şişme yaparken; "
                "yüksek dozda veya uzun süreli maruziyette kaçınılmaz nekroza yol açar.\n\n"
                "> [TEMEL İLKE] Örneğin iskemik bir miyokard dokusu 10. dakikada reperfüzyonla tamamen kurtulabilirken, "
                "iskemi 40 dakikayı aştığında aynı dokuda geri dönüşümsüz transmural nekroz gelişir.\n\n"
                "Dolayısıyla bir lezyonun patolojik boyutu yalnızca etkenin adıyla değil, zaman ve şiddet "
                "dinamikleriyle birlikte değerlendirilmelidir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Etkenin Türü", "desc": "Toksin, iskemi veya mekanik travmanın etkilediği hücresel organel farklıdır.", "isKey": True},
                    {"title": "Maruziyet Süresi", "desc": "Kısa süreli hasar geri dönebilirken, uzayan hasar geri dönüşümsüzleşir.", "isKey": True},
                    {"title": "Hasar Şiddeti", "desc": "Hafif hipoksi adaptasyon yaparken, tam anoksi saniyeler içinde ATP'yi sıfırlar.", "isKey": True}
                ],
                "table": {
                    "title": "Süre ve Şiddetin Hücresel Sonuçları",
                    "headers": ["İskemi Süresi (Miyokard)", "Hücresel Durum", "Geri Dönüş Olasılığı"],
                    "rows": [
                        ["< 2 dakika", "Kontraktilite kaybı, erken ATP düşüşü", "Tam geri dönüşümlü"],
                        ["10 - 20 dakika", "Hücresel şişme, ER dilatasyonu, bleb", "Reperfüzyonla tam geri dönüşümlü"],
                        ["> 20 - 40 dakika", "Mitokondri ve membran rüptürü", "Geri dönüşümsüz (Nekroz)"],
                        ["> 6 - 12 saat", "Işık mikroskobunda koagülasyon nekrozu", "Kalıcı skar dokusu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyokard hücresinde kontraktilite iskemi başladıktan sonra saniyeler (1-2 dk) içinde durur, ancak ölüm 20-30 dakikada başlar.",
                "📌 [YÜKSEK VERİM] Hücrenin hasara yanıtı etkenin türü, süresi ve şiddetinin birleşik fonksiyonudur."
            ],
            "medicalTerms": [
                {"term": "Reperfüzyon", "explanation": "İskemiye uğramış bir dokuya tıkanıklığın açılarak yeniden kan akımının sağlanmasıdır."},
                {"term": "Kontraktilite", "explanation": "Kas hücresinin ATP harcayarak mekanik gerim ve kasılma oluşturma yeteneğidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İskemi Süresine Bağlı Kardiyak Hasar Zinciri",
                    [
                        "1. Saniyeler İçinde: Oksidatif fosforilasyon durur, ATP hızla düşer.",
                        "2. 1-2. Dakika: Kalp kası kasılmayı (kontraktiliteyi) tamamen durdurur.",
                        "3. 10. Dakika: Na+/K+ pompası durur, hücresel şişme ve ER dilatasyonu gelişir (geri dönüşümlü).",
                        "4. 20-30. Dakika: Mitokondri membranları parçalanır, hücre geri dönüşümsüz hasara girer.",
                        "5. 2-4. Saat: Hücre zarı lize olur, troponin ve CK-MB kana dökülür."
                    ]
                ),
                make_cloze(
                    "Miyokard iskemisinde kasılma 1-2 dakikada dururken geri dönüşümsüz hasar yaklaşık 20-30 dakika sonra başlar.",
                    "20-30 dakika",
                    "Kritik Süre Eşiği"
                )
            ]
        },
        {
            "slideNumber": 14,
            "title": "Doku Toleransı ve Hücre Tipi Duyarlılıkları",
            "subtitle": "Nöron, kardiyomiyosit, fibroblast ve iskelet kasının iskemi toleransı",
            "badge": "Doku Toleransı",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Farklı dokular aynı şiddetteki iskemi ve hipoksiye son derece farklı direnç gösterir. Bir "
                "dokunun iskemiye dayanma süresi metabolik hızına, glikojen rezervine ve hücre tipinin "
                "fizyolojik özelliklerine bağlıdır. Beyin nöronları yüksek metabolik hızları ve glikojensiz "
                "olmaları nedeniyle tam iskemiye yalnızca 3 ila 5 dakika dayanabilir.\n\n"
                "> [SINAV SPOTU] Kalp kası hücreleri 20-30 dakikada geri dönüşümsüz hasara uğrarken, "
                "iskelet kası hücreleri bol glikojen depoları sayesinde 2 ila 3 saat tam iskemiyi tolere edebilir.\n\n"
                "Fibroblastlar ise düşük metabolizmalarıyla saatlerce canlı kalabilir. Bu farklar resüsitasyon, "
                "turnike uygulamaları ve organ nakli sürelerinin temelini belirler."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Nöronlar", "desc": "3-5 dakikada geri dönüşümsüz ölür; iskemik hasara en duyarlı hücrelerdir.", "isKey": True},
                    {"title": "Miyositler", "desc": "20-30 dakikada geri dönüşümsüz nekroza girer.", "isKey": True},
                    {"title": "İskelet Kası", "desc": "2-3 saatlik tam iskemiyi fonksiyonel kayıpsız tolere edebilir.", "isKey": True}
                ],
                "table": {
                    "title": "Dokuların İskemiye Dayanıklılık Süreleri",
                    "headers": ["Doku / Hücre Tipi", "Geri Dönüşümsüz Hasar Başlama Süresi", "Metabolik Özellik"],
                    "rows": [
                        ["Serebral Nöronlar", "3 - 5 dakika", "En duyarlı doku, glikojen yok, yüksek O2 tüketimi"],
                        ["Kalp Kası (Miyokard)", "20 - 30 dakika", "Yüksek enerji ihtiyacı, sınırlı glikolitik kapasite"],
                        ["Böbrek Tübül Epiteli", "30 - 60 dakika", "Yüksek iyon pompası yükü, orta duyarlılık"],
                        ["İskelet Kası", "2 - 3 saat", "Zengin glikojen deposu, anaerobik kapasite"],
                        ["Fibroblastlar", "Saatler - günler", "Düşük metabolizma hızı, en dirençli hücre grubu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Tam iskemiye tolerans: İskelet kası 2-3 saat dayanabilirken kalp kası 20-30 dakikada ölür.",
                "📌 [SINAV SPOTU] Santral sinir sistemi nöronları hipoksiye en duyarlı hücrelerdir; 3-5 dakikada geri dönüşümsüz hasar gelişir."
            ],
            "medicalTerms": [
                {"term": "İskemik Tolerans", "explanation": "Bir dokunun kan akımı kesildiğinde canlılığını koruyabildiği maksimum süredir."},
                {"term": "Glikoliz", "explanation": "Glukozun oksijensiz ortamda parçalanarak kısıtlı ATP ürettiği metabolik yoldur."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Doku İskemi Toleransları",
                    ["Hücre Tipi", "Dayanma Süresi", "Duyarlılık Derecesi"],
                    [
                        [("Serebral Nöron", False), ("3-5 dakika", True, "Dakika Düzeyi"), ("En yüksek duyarlılık", False)],
                        [("Kardiyomiyosit", False), ("20-30 dakika", True, "Yarım Saat"), ("Yüksek duyarlılık", False)],
                        [("İskelet Kası", False), ("2-3 saat", True, "Saat Düzeyi"), ("Orta direnç", False)],
                        [("Fibroblast", False), ("Saatler boyu", True, "Uzun Süre"), ("Maksimum direnç", False)]
                    ]
                ),
                make_micro_quiz(
                    "İskemiye tolerans açısından değerlendirildiğinde tam kan akımı kesilmesine en uzun süre dayanabilen ve en dirençli olan hücre grubu hangisidir?",
                    {
                        "A": "Serebral korteks nöronları",
                        "B": "Kalp kası hücreleri (miyositler)",
                        "C": "Böbrek proksimal tübül epitel hücreleri",
                        "D": "İskelet kası hücreleri",
                        "E": "Karaciğer santrilobüler hepatositleri"
                    },
                    "D",
                    {
                        "A": "Nöronlar en duyarlıdır (3-5 dakika).",
                        "B": "Kalp kası 20-30 dakikada ölür.",
                        "C": "Tübül epiteli 30-60 dakikada zedelenir.",
                        "D": "Doğru cevap D'dir: İskelet kası hücreleri zengin glikojen depoları sayesinde 2-3 saat iskemiyi tolere edebilir.",
                        "E": "Hepatositler iskelet kası kadar uzun süre tam iskemiyi tolere edemez."
                    }
                )
            ]
        },
        {
            "slideNumber": 15,
            "title": "Hücresel Hasarda Kritik Biyokimyasal Hedefler",
            "subtitle": "Mitokondri, membranlar, protein mekanizması ve DNA",
            "badge": "Hedefler",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Zararlı etkenler hücreye gelişi güzel zarar vermez; hücre canlılığının devamı için zorunlu "
                "olan 4 temel hücresel sisteme odaklanır: 1) Mitokondriler (ATP üretimi ve apoptoz kontrolü), "
                "2) Hücre ve organel membranları (iyonik ve ozmotik homeostaz), 3) Protein sentez mekanizması "
                "(yapısal ve enzimatik devamlılık), 4) DNA ve nükleer kromatin (genetik şifre ve bölünme).\n\n"
                "> [TEMEL İLKE] Bu hedefler birbirinden bağımsız değildir; mitokondri hasarı ATP'yi tüketir, "
                "ATP eksikliği membran pompalarını bozar, bozulan membran kalsiyum akışına ve enzim aktivasyonuna yol açar.\n\n"
                "Herhangi bir hedefin çöküşü saniyeler içinde diğer tüm hedefleri yıkarak hasarı kartopu gibi büyütür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Mitokondri", "desc": "ATP sentezinin merkezidir; geçirgenlik geçiş gözeneği (MPTP) açılırsa ölüm başlar.", "isKey": True},
                    {"title": "Plazma Zarı", "desc": "İyon dengesini korur; parçalanması hücre içine masif kalsiyum girişine yol açar.", "isKey": True},
                    {"title": "Genetik Bütünlük", "desc": "DNA hasarı onarılamazsa p53 yolağı üzerinden apoptoz tetiklenir.", "isKey": False}
                ],
                "table": {
                    "title": "Hücre Hasarının 4 Kritik Hedefi",
                    "headers": ["Hedef Sistem", "Bozulma Nedeni", "Hücresel Yıkıcı Sonuç"],
                    "rows": [
                        ["Mitokondri", "Hipoksi, toksinler, yüksek Ca2+", "ATP tükenmesi, Sitokrom c salınımı"],
                        ["Hücre Zarı", "ROS, fosfolipazlar, kompleman", "Ozmotik şişme, enzimlerin hücre dışına sızması"],
                        ["Protein Sentezi", "ER dilatasyonu, ribozom ayrılması", "Enzim yetmezliği, membran onarımının durması"],
                        ["Nükleer DNA", "Radyasyon, ROS, alkilleyici ajanlar", "p53 aktivasyonu, hücre döngüsü durması veya apoptoz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarında 4 ana hedef: Mitokondri, plazma ve lizozom zarları, protein sentezi ve DNA'dır.",
                "📌 [YÜKSEK VERİM] Bir hedefin hasarı diğerlerini tetikleyerek pozitif geri bildirimli bir hücresel kriz yaratır."
            ],
            "medicalTerms": [
                {"term": "MPTP", "explanation": "Mitokondriyal Geçirgenlik Geçiş Gözeneği; mitokondri zarında açılarak membran potansiyelini sıfırlayan kanaldır."},
                {"term": "Sitokrom c", "explanation": "Mitokondri iç zarında elektron taşıyan, sitoplazmaya sızdığında apoptozu başlatan proteindir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hedeflerin Birbirini Tetikleme Kısırdöngüsü",
                    [
                        "1. Mitokondri Hasarı: Hipoksi oksidatif fosforilasyonu durdurur, ATP tükenir.",
                        "2. Pompa İflası: Na+/K+ ATPaz çalışmaz, hücre içine sodyum ve su dolar.",
                        "3. Membran Gerilmesi: Şişen hücrede plazma zarı gerilir ve mikrovilluslar kaybolur.",
                        "4. Kalsiyum İntrakolasyonu: Hücre içine kalsiyum dolarak fosfolipaz ve proteazları aktive eder.",
                        "5. Tam Membran Yıkımı: Aktive fosfolipazlar lipidleri parçalar, sitoplazmik içerik kana dökülür."
                    ]
                ),
                make_cloze(
                    "Mitokondri zar potansiyelinin sıfırlanmasına ve sitokrom c salınımına yol açan mitokondriyal kanala MPTP adı verilir.",
                    "MPTP",
                    "Mitokondri Kanalı"
                )
            ]
        },
        {
            "slideNumber": 16,
            "title": "Hücresel Hasarın Zaman ve Morfoloji İlişkisi",
            "subtitle": "Fonksiyon kaybı, hücre ölümü ve mikroskobik değişikliklerin kronolojisi",
            "badge": "Kronoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre hasarında son derece kritik ve sınavların en sevdiği pedagojik kural şudur: "
                "Hücresel fonksiyon kaybı ve hücre ölümü, morfolojik değişikliklerden çok daha önce gerçekleşir! "
                "Bir hücre öldüğünde mikroskop altında anında 'ölü' olarak görünmez; morfolojik değişikliklerin "
                "ortaya çıkması için enzimatik sindirim ve protein pıhtılaşması için zaman gerekir.\n\n"
                "> [KRİTİK UYARI] Kronolojik sıralama: Fonksiyon kaybı → Hücre ölümü → Elektron mikroskopik "
                "değişiklikler → Işık mikroskobik değişiklikler → Makroskobik değişiklikler.\n\n"
                "Örneğin miyokard enfarktüsünde hasta ilk 1 saat içinde ölümcül aritmiyle hayatını kaybedebilir; "
                "ancak otopside kalbe ışık mikroskobunda bakıldığında ilk 4-12 saatte hiçbir nekroz bulgusu saptanamayabilir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Erken Fonksiyon Kaybı", "desc": "Hücre zedelenir zedelenmez (dakikalar içinde) işlevini durdurur.", "isKey": True},
                    {"title": "Hücre Ölümü Eşiği", "desc": "Geri dönüşümsüz hasar morfolojik yapı bozulmadan önce kesinleşir.", "isKey": True},
                    {"title": "Morfolojik Gecikme", "desc": "Işık mikroskobunda nekrozun belirmesi 4-12 saat, makroskobide 12-24 saat sürer.", "isKey": True}
                ],
                "table": {
                    "title": "Hücre Hasarının Morfolojik Kronolojisi",
                    "headers": ["Aşama", "Zaman Aralığı (Miyokard)", "Gözlenen Değişiklik"],
                    "rows": [
                        ["Fonksiyon Kaybı", "1 - 2 dakika", "Kasılma durur, EKG değişiklikleri başlar"],
                        ["Geri Dönüşümsüz Ölüm", "20 - 40 dakika", "Mitokondri rüptürü, biyokimyasal ölüm"],
                        ["Elektron Mikroskobu", "30 - 60 dakika", "Miyelin figürleri, amorf mitokondriyal yoğunluklar"],
                        ["Işık Mikroskobu", "4 - 12 saat", "Artmış eozinofili, nükleer piknoz, koagülasyon nekrozu"],
                        ["Makroskopik İnceleme", "12 - 24 saat", "Soluk, alacalı infarkt alanı, hiperemik sınır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre ölümü, ışık mikroskobu ve makroskopideki morfolojik değişikliklerden çok daha önce gerçekleşir.",
                "📌 [SINAV SPOTU] Kronolojik sıra: Fonksiyon kaybı → Hücre ölümü → EM değişiklikleri → Işık mikroskobisi → Makroskopi.",
                "🚨 [KRİTİK UYARI] İlk 2 saatte ölen bir miyokard enfarktüsü hastasının kalbinde ışık mikroskobunda nekroz izlenmez."
            ],
            "medicalTerms": [
                {"term": "Morfolojik Gecikme", "explanation": "Hücre biyokimyasal olarak öldükten sonra yapısal mikroskobik bozulmanın saatler sonra belirmesidir."},
                {"term": "Ultrastrüktür", "explanation": "Yalnızca transmisyon elektron mikroskobu (TEM) ile incelenebilen nanometrik organel düzeyidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hasar Bulgularının Kronolojik Sıralaması",
                    [
                        "1. Fonksiyon Kaybı: Saniyeler ve dakikalar içinde hücrenin fizyolojik görevi durur.",
                        "2. Biyokimyasal Hücre Ölümü: 20-40 dakikada membran ve mitokondri geri dönüşsüz çöker.",
                        "3. Ultrastrüktürel Değişiklik: 30-120 dakikada elektron mikroskobunda zarlar ve organeller bozulur.",
                        "4. Işık Mikroskobik Nekroz: 4-12 saat sonra artmış eozinofili ve nükleer erime görülür.",
                        "5. Makroskobik Görünüm: 12-24 saat sonra çıplak gözle soluk enfarkt alanı belirginleşir."
                    ]
                ),
                make_cloze(
                    "İskemik dokuda biyokimyasal hücre ölümü ışık mikroskobundaki morfolojik değişikliklerden çok daha önce gerçekleşir.",
                    "önce",
                    "Zaman İlişkisi"
                )
            ]
        },
        {
            "slideNumber": 17,
            "title": "Geri Dönüşümlü Hücre Hasarı Kavramı ve Sınırları",
            "subtitle": "Hücresel homeostazın geçici bozulması ve geri kazanım potansiyeli",
            "badge": "Geri Dönüşümlü",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Geri dönüşümlü hücre hasarı, zararlı uyarı ortadan kaldırıldığında hücrenin normal yapı ve "
                "fonksiyonuna dönebildiği erken patolojik evredir. Bu evrede hücrenin enerji üretimi düşmüş, "
                "iyon pompaları zayıflamış ve organeller şişmiştir; ancak hücreyi hayatta tutan en temel "
                "biyolojik kalkan olan plazma ve organel membranlarının bütünlüğü KORUNMUŞTUR.\n\n"
                "> [TEMEL İLKE] Geri dönüşümlü hasarın iki ana morfolojik kalıbı vardır: 1) Hücresel şişme "
                "(hidropik değişim), 2) Yağlanma (steatoz).\n\n"
                "Zararlı etken (örneğin kısa süreli iskemi) kaldırıldığında hücre içi ATP sentezi yeniden başlar, "
                "iyon pompaları fazla sodyumu dışarı pompalar ve hücre eski sağlıklı hacmine kavuşur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Membran Bütünlüğü", "desc": "Geri dönüşümlü hasarın en kritik özelliği zarların yırtılmamış olmasıdır.", "isKey": True},
                    {"title": "İki Klasik Kalıp", "desc": "Hücresel şişme (en erken bulgu) ve yağlanmadır (lipit metabolizma hasarı).", "isKey": True},
                    {"title": "Fonksiyonel Rezerv", "desc": "Hücre işlevini durdurmuş olsa da canlılığını sürdürür.", "isKey": False}
                ],
                "table": {
                    "title": "Geri Dönüşümlü Hasarın Temel Nitelikleri",
                    "headers": ["Parametre", "Geri Dönüşümlü Evre", "Geri Dönüşümsüz Evre (Nekroz)"],
                    "rows": [
                        ["Plazma Zarı", "Bütünlüğü korunmuş, blebler var", "Parçalanmış, geçirgenlik sınırsız"],
                        ["Mitokondriler", "Hafif şişme, küçük amorf birikinti", "Belirgin şişme, büyük amorf kalsiyum yoğunlukları"],
                        ["Hücre İçi Enzimler", "Hücre içinde hapsolmuş", "Kana sızmış (Troponin, ALT, AST)"],
                        ["Enflamasyon", "Yok", "Belirgin nötrofilik infiltrasyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Geri dönüşümlü hücre hasarında membran bütünlüğü korunmuştur; bu nedenle hücre içi enzimler kana sızmaz.",
                "📌 [YÜKSEK VERİM] Geri dönüşümlü hasarın iki morfolojik göstergesi: Hücresel şişme (hidropik değişim) ve yağlanmadır."
            ],
            "medicalTerms": [
                {"term": "Hidropik Değişim", "explanation": "İyon pompalarının durmasıyla hücre içine su girerek sitoplazmanın vakuollü şişmesidir."},
                {"term": "Steatoz", "explanation": "Trigliseritlerin sitoplazmada anormal vakuoller halinde birikmesi durumudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Hücre Hasarının Sınırları",
                    "Geri Dönüşümlü Hasar",
                    "Geri Dönüşümsüz Hasar",
                    [
                        "Membran bütünlüğü korunur",
                        "Enzimler hücre içinde kalır",
                        "Mitokondride hafif şişme vardır",
                        "Enflamasyon görülmez"
                    ],
                    [
                        "Membran bütünlüğü parçalanır",
                        "Enzimler kana sızar (CK-MB, Troponin)",
                        "Mitokondride kalsiyum birikir",
                        "Çevre dokuda yoğun enflamasyon başlar"
                    ]
                ),
                make_cloze(
                    "Geri dönüşümlü hücre hasarının en kritik ve vazgeçilmez morfolojik özelliği membran bütünlüğünün korunmasıdır.",
                    "membran bütünlüğünün korunmasıdır",
                    "Hayati Bariyer"
                )
            ]
        },
        {
            "slideNumber": 18,
            "title": "Hücresel Şişme (Hidropik Değişim): En Erken Morfolojik Bulgu",
            "subtitle": "ATP tükenmesi, Na+/K+ ATPaz pompa yetmezliği ve su girişi",
            "badge": "Mekanizma",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücresel şişme (hidropik değişim veya vakuoler dejenerasyon), hemen hemen tüm hücre hasarı "
                "tiplerinde ortaya çıkan EN ERKEN morfolojik değişikliktir. Hücre içi ozmotik dengeyi sağlayan "
                "en önemli yapı, hücre zarına yerleşik enerji bağımlı Na+/K+ ATPaz pompasıdır. Bu pompa "
                "her döngüde 3 Na+ iyonunu dışarı atarken 2 K+ iyonunu içeri alır.\n\n"
                "> [TEMEL İLKE] İskemi veya toksinler nedeniyle ATP düzeyi düştüğünde Na+/K+ ATPaz pompası durur; "
                "sodyum hücre dışına atılamaz ve hücre içinde birikir.\n\n"
                "Artan hücre içi sodyum konsantrasyonu, ozmotik gradient yaratarak ekstraselüler suyu pasif "
                "olarak hücre içine çeker. Hücre şişer, endoplazmik retikulum genişler ve berrak vakuoller belirir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "En Erken Bulgu", "desc": "Hücre zedelenmesinin ilk mikroskobik kanıtı hücresel şişmedir.", "isKey": True},
                    {"title": "Na+/K+ Pompası", "desc": "ATP yokluğunda pompanın durması hücre içi sodyum birikimine yol açar.", "isKey": True},
                    {"title": "Ozmotik Su Akışı", "desc": "Hücre içi artan sodyum ve klor iyonları suyu içeri çekerek şişirir.", "isKey": True}
                ],
                "table": {
                    "title": "Na+/K+ ATPaz Bozulmasının İyonik Sonuçları",
                    "headers": ["İyon / Molekül", "Hücre İçi Değişim", "Patofizyolojik Sonuç"],
                    "rows": [
                        ["Sodyum (Na+)", "Hücre içinde birikir (Artar)", "Ozmotik su çekişini başlatır"],
                        ["Potasyum (K+)", "Hücre dışına kaçar (Azalır)", "Membran potansiyeli kaybolur"],
                        ["Klorür (Cl-)", "Pasif olarak hücreye girer", "İntraselüler ozmolariteyi daha da artırır"],
                        ["Su (H2O)", "Hücre içine masif giriş yapar", "Hücresel şişme ve organel dilatasyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarının ilk ve en erken morfolojik bulgusu hücresel şişmedir (hidropik değişim).",
                "📌 [SINAV SPOTU] Hücresel şişmenin temel biyokimyasal mekanizması ATP azalmasına bağlı Na+/K+ ATPaz pompasının iflasıdır.",
                "🚨 [KRİTİK UYARI] ATP azalması sonucu hücre dışına Na+ çıkışı OLMAZ; Na+ hücre içinde birikir!"
            ],
            "medicalTerms": [
                {"term": "Na+/K+ ATPaz", "explanation": "ATP enerjisiyle 3 sodyumu dışarı atıp 2 potasyumu içeri alan hücre zarı pompasıdır."},
                {"term": "Vakuoler Dejenerasyon", "explanation": "Şişen endoplazmik retikulum sisternalarının ışık mikroskobunda berrak vakuoller olarak görünmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hücresel Şişmenin Biyokimyasal Patogenezi",
                    [
                        "1. İskemi / Toksin: Mitokondride oksidatif fosforilasyon durur, ATP hızla tükenir.",
                        "2. Pompa Yetmezliği: Na+/K+ ATPaz pompası çalışamaz hale gelir.",
                        "3. Sodyum Birikimi: Sodyum hücre dışına pompalanamaz, hücre içi Na+ konsantrasyonu fırlar.",
                        "4. İzoozmotik Su Girişi: Sodyumun yarattığı ozmotik çekimle su hücre içine hücum eder.",
                        "5. ER Dilatasyonu: Endoplazmik retikulum suyla dolarak genişler ve berrak vakuoller oluşturur."
                    ]
                ),
                make_micro_quiz(
                    "Hücrede iskemiye bağlı ATP azalması sonucu aşağıdakilerden hangisi MEYDANA GELMEZ?",
                    {
                        "A": "Hücre içine kalsiyum girişi",
                        "B": "Hücre içine su girişi ve şişme",
                        "C": "Hücre dışına sodyum atılımının artması",
                        "D": "Anaerobik glikolizle hücre içi pH'ın düşmesi",
                        "E": "Hücre içi glikojen depolarının tükenmesi"
                    },
                    "C",
                    {
                        "A": "Membran pompaları bozulunca hücre içine Ca2+ girişi artar.",
                        "B": "Hücreye su girer ve hidropik şişme gelişir.",
                        "C": "Doğru cevap C'dir: ATP azalınca Na+/K+ pompası durur, sodyum hücre dışına atılamaz; hücre içinde birikir!",
                        "D": "Glikoliz laktat üretir ve pH asidik olur.",
                        "E": "Glikoliz hızlandığı için glikojen depoları hızla tükenir."
                    }
                )
            ]
        },
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Hasar İlkeleri ve Doku Toleransı",
            "subtitle": "Etiyoloji ilkeleri, iskemi toleransları, kronoloji ve hücresel şişme",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 2,
            "synthesisNarrative": (
                "Bu ikinci kontrol noktasında, hücre hasarının etiyolojik mekanizmalarını, dokuların iskemiye "
                "karşı değişken tolerans sürelerini ve en erken hasar bulgusu olan hidropik şişmeyi özetliyoruz. "
                "Dokular arasında devasa tolerans farkları vardır; nöronlar dakikalar içinde ölürken iskelet "
                "kası saatlerce hayatta kalabilir.\n\n"
                "> [ÖZET VURGU] Hücre hasarının en erken morfolojik bulgusu hücresel şişmedir; temel mekanizma "
                "ATP eksikliği nedeniyle Na+/K+ ATPaz pompasının durması ve hücre içine sodyum/su dolmasıdır.\n\n"
                "Aşağıdaki 3 kritik akıl kartını inceleyerek ikinci bölümün kazanımlarını pekiştirin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Doku Toleransı", "desc": "Nöron (3-5 dk) < Kalp kası (20-30 dk) < İskelet kası (2-3 saat).", "isKey": True},
                    {"title": "Kronolojik Kural", "desc": "Fonksiyon kaybı ve hücre ölümü mikroskobik değişikliklerden önce gelir.", "isKey": True},
                    {"title": "Hidropik Şişme", "desc": "ATP tükenmesi → Na+/K+ ATPaz bozulması → Na+ ve su girişi.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 2 Sentez Tablosu",
                    "headers": ["Kavram", "Biyolojik Mekanizma", "Sınavda Çıkış Şekli"],
                    "rows": [
                        ["Hücresel Şişme", "Na+/K+ ATPaz pompa yetmezliği", "Hasarın ilk ve en erken morfolojik bulgusu"],
                        ["İskemi Toleransı", "Glikojen deposu ve metabolizma hızı", "İskelet kası 2-3 saat, kalp kası 20-30 dk"],
                        ["Morfolojik Kronoloji", "Enzimatik sindirim için gereken süre", "Ölüm morfolojiden önce gerçekleşir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarının ilk morfolojik bulgusu hücresel şişmedir (hidropik değişim).",
                "📌 [SINAV SPOTU] Nöron 3-5 dk, kalp kası 20-30 dk, iskelet kası 2-3 saat iskemiyi tolere edebilir."
            ],
            "medicalTerms": [
                {"term": "Reperfüzyon Hasarı", "explanation": "İskemik dokuya kan akımının yeniden sağlanmasıyla reaktif oksijen ürünlerinin dokuyu daha ağır zedelemesidir."},
                {"term": "Turgor", "explanation": "Hücre veya dokunun sıvı içeriğine bağlı iç gerginliği ve dolgunluğudur."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-004",
                    "Miyokard enfarktüsünde iskemik dokuda biyokimyasal ölüm ile ışık mikroskobik nekroz arasındaki zaman ilişkisi nasıldır?",
                    "Miyositlerde biyokimyasal ölüm 20-40 dakikada geri dönüşsüz olarak gerçekleşir; ancak ışık mikroskobunda nekrozun (eozinofili, piknoz) belirmesi en az 4-12 saat sürer."
                ),
                make_flashcard(
                    "fc-k1-04-005",
                    "Hücre hasarının en erken morfolojik bulgusu nedir ve altta yatan biyokimyasal defekt hangisidir?",
                    "En erken bulgu hücresel şişmedir (hidropik değişim); altta yatan neden ATP azalmasına bağlı plazma membranı Na+/K+ ATPaz pompasının iflasıdır."
                ),
                make_flashcard(
                    "fc-k1-04-006",
                    "İskelet kası hücreleri neden kalp kası hücrelerine kıyasla iskemiye çok daha uzun süre dayanabilir?",
                    "İskelet kası hücreleri zengin glikojen depolarına sahiptir ve anaerobik glikolizle ATP üretebilir; ayrıca bazal metabolik hızları kalp kasına göre çok daha düşüktür."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 2 Sentezi: Bir hücrede ATP tükendiğinde hücre içi ve dışı sodyum konsantrasyonunda ne değişir?",
                    "Na+/K+ ATPaz pompası durduğu için sodyum hücre dışına atılamaz; hücre içinde sodyum birikir, hücre dışındaki sodyum azalır ve ozmotik olarak su içeri çekilir."
                ),
                make_cloze(
                    "Hücre hasarının en erken morfolojik bulgusu olan hücresel şişmeye hidropik değişim adı da verilir.",
                    "hidropik değişim",
                    "Patolojik Değişim"
                )
            ]
        }
    ]
