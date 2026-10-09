#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4: Patolojinin Alt Dalları (Adımlar 30 - 39)
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
        # Adım 30
        {
            "slideNumber": 30,
            "title": "Patolojinin İki Ana Ekseni: Genel Patoloji ve Özel (Sistemik) Patoloji",
            "subtitle": "Tıbbi patoloji eğitimi ve pratiği; temel hücresel prensipleri inceleyen genel patoloji ile organ bazlı özel patoloji olmak üzere iki ana eksende yürütülür.",
            "badge": "Patoloji Dalları",
            "badgeColor": "blue",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Tıbbi patoloji eğitimi ve pratiği; ==Genel Patoloji== ve ==Özel (Sistemik) Patoloji== olmak üzere iki ana eksende yürütülür.

Genel patoloji; zedeleyici etkenlere karşı dokuların verdiği evrensel hücresel yanıtları inceler. Bunlar hücresel adaptasyonlar, nekroz ve apoptoz, akut ve kronik inflamasyon, hemodinamik bozukluklar ve neoplazinin temel mekanizmalarıdır. Özel patoloji ise bu evrensel mekanizmaların kardiyovasküler, solunum veya gastrointestinal gibi spesifik organ sistemlerindeki yansımalarını ele alır. Örneğin genel patolojide iskemi ve koagülasyon nekrozunu kavrayan bir hekim, özel patolojide miyokard enfarktüsünü doğru yorumlar.

> [TEMEL İLKE] Genel patoloji hücresel altyapıyı kurar; özel patoloji ise organ düzeyindeki klinik hastalıkları tanımlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Genel Patoloji", "desc": "Hücresel zedelenme, inflamasyon, tamir, dolaşım bozuklukları ve tümör biyolojisinin evrensel mekanizmalarıdır.", "isKey": True},
                    {"title": "Özel Patoloji", "desc": "Genel prensiplerin organ sistemlerindeki (kalp, akciğer, böbrek) özel hastalık tablolarına yansımasıdır.", "isKey": True},
                    {"title": "Pedagojik Bütünlük", "desc": "Genel patoloji hücresel altyapıyı, özel patoloji ise organ düzeyindeki tanısal pratiği oluşturur.", "isKey": False}
                ],
                "table": {
                    "title": "Genel Patoloji ile Özel (Sistemik) Patoloji Karşılaştırması",
                    "headers": ["Parametre", "Genel Patoloji", "Özel (Sistemik) Patoloji"],
                    "rows": [
                        ["İnceleme Düzeyi", "Hücresel, moleküler ve temel doku yanıtları", "Spesifik organ, sistem ve klinik hastalık tabloları"],
                        ["Temel Konular", "Adaptasyon, nekroz, apoptoz, inflamasyon, tromboz, neoplazi", "Miyokard enfarktüsü, KOAH, siroz, tiroidit, meme karsinomu"],
                        ["Klinik Amacı", "Hastalıkların biyolojik doğasını ve patogenezini kavramak", "Organ spesifik lezyonları ayırt edip tanı ve evreleme yapmak"],
                        ["Müfredat Konumu", "Dönem 2 ve Dönem 3'ün temel giriş blokları", "Organ kurulları ve klinik stajlar (Dönem 3-4-5)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Genel patoloji hücre ve dokuların zedelenmeye verdiği evrensel temel yanıtları (adaptasyon, inflamasyon, nekroz, neoplazi) inceler.",
                "📌 [SINAV SPOTU] Akut apandisit, siroz veya miyokard enfarktüsü gibi organa özgü hastalıklar Özel (Sistemik) Patolojinin konusudur.",
                "💡 [ÖĞRENME İPUCU] Bir yangı hücresinin (nötrofil) damardan çıkış mekanizması genel patolojidir; menenjitli beyin dokusunda yaptığı hasar ise özel patolojidir."
            ],
            "medicalTerms": [
                {"term": "Genel Patoloji", "explanation": "Hücre ve dokuların zedelenmeye karşı verdiği evrensel temel reaksiyonları inceleyen daldır."},
                {"term": "Özel (Sistemik) Patoloji", "explanation": "Temel patolojik süreçlerin organ sistemlerindeki özel hastalık tablolarını inceleyen alandır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Genel Patoloji vs Özel (Sistemik) Patoloji Odak Farkı",
                    "Genel Patoloji (Temel Mekanizmalar)",
                    "Özel Patoloji (Organ Hastalıkları)",
                    [
                        "Hücresel adaptasyon, atrofi, hipertrofi ve metaplazi yolakları",
                        "Nekroz ve apoptozun moleküler mekanizmaları ve biyokimyası",
                        "Akut ve kronik inflamasyonun vasküler ve hücresel basamakları",
                        "Karsinogenezin temel onkogen ve tümör baskılayıcı dinamikleri"
                    ],
                    [
                        "Hipertansiyona bağlı sol ventrikül konsantrik hipertrofisi",
                        "Koroner arter tıkanıklığında miyokard koagülasyon nekrozu",
                        "Akciğer parankiminde kazeöz granülomatöz tüberküloz inflamasyonu",
                        "Meme duktal karsinomasında cerrahi rezeksiyon ve pTNM evrelemesi"
                    ]
                ),
                make_cloze(
                    "Hücrelerin zedeleyici etkenlere karşı geliştirdiği atrofi, nekroz, inflamasyon ve neoplazi gibi temel mekanizmalar genel patoloji kapsamında incelenir.",
                    "genel patoloji",
                    "Organ spesifik olmayan evrensel hücresel yanıtları inceleyen ana dal"
                ),
                make_interactive_table(
                    "Patoloji Disiplinlerinin Kapsam Eşleştirmesi",
                    ["Konu Başlığı", "Patoloji Alanı", "İncelenen Temel Olay"],
                    [
                        [
                            ("Koagülasyon Nekrozu", False),
                            ("Genel Patoloji", True, "Hücresel zedelenme temel yanıtı"),
                            ("İskemi sonucu protein denatürasyonu ve hücre ölümü", False)
                        ],
                        [
                            ("Kresentik Glomerulonefrit", False),
                            ("Özel Patoloji", True, "Böbrek sistemik hastalığı"),
                            ("Bowman aralığında parietal hücre proliferasyonu", False)
                        ],
                        [
                            ("Tümör Anjiyogenezi", False),
                            ("Genel Patoloji", True, "Neoplazinin genel mekanizması"),
                            ("VEGF salınımıyla yeni kılcal damar oluşumu", False)
                        ]
                    ]
                )
            ]
        },

        # Adım 31
        {
            "slideNumber": 31,
            "title": "Patolojik Anatomi (Makroskopik Patoloji): Çıplak Gözün Tanısal Gücü",
            "subtitle": "Patolojik anatomi, hastalıkların organlarda oluşturduğu çıplak gözle görülebilen boyut, kıvam, renk ve sınır değişikliklerini inceler.",
            "badge": "Makroskopi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """==Patolojik anatomi (makroskopik patoloji)==, cerrahi doku tanısının ilk ve en kritik basamağını oluşturur.

Diseksiyon masasında çıplak gözle yapılan bu incelemede organın boyutu, ağırlığı, rengi, kıvamı ve kesit yüzey özellikleri değerlendirilir. Makroskopi, binlerce hücre içeren büyük rezeksiyon materyallerinden mikroskopiye gidecek en kritik alanların seçildiği ==örnekleme (sampling)== kılavuzudur. Rezeksiyon sınırları özel çini mürekkebiyle boyanarak oryantasyon sağlanır; tümörün en derin invazyon noktası ve lenf nodları kasetlenir. Hatalı bir makroskopi, mikroskopta doğru tanının kaçırılmasına yol açar.

> [TEMEL İLKE] Yetersiz makroskobik örnekleme yapıldığında mikroskobik tanının doğruluğu tamamen tehlikeye girer.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Görsel Parametreler", "desc": "Boyut, ağırlık, renk, kıvam, nekroz, kanama alanları ve çevre sınır ilişkisi kaydedilir.", "isKey": True},
                    {"title": "Örnekleme Kılavuzluğu", "desc": "Mikroskop altında incelenecek kasetlerin hangi odaklardan alınacağını belirler.", "isKey": True},
                    {"title": "Cerrahi Sınır Boyama", "desc": "Rezeksiyon sınırları özel çini mürekkebiyle boyanarak oryantasyon sağlanır.", "isKey": False}
                ],
                "table": {
                    "title": "Makroskopik İncelemede Değerlendirilen Temel Kriterler",
                    "headers": ["Makroskobik Kriter", "İncelenen Özellik", "Klinikopatolojik Önemi"],
                    "rows": [
                        ["Organ Boyut ve Ağırlığı", "Milimetrik ölçüm ve gramaj", "Hipertrofi, atrofi, ödem ve konjesyon derecesini belirler"],
                        ["Lezyon Rengi ve Kıvamı", "Soluk, hiperemik, sert, frajil, kistik", "Enfarktüs (soluk), tümör desmoplazisi (sert) ayrımını sağlar"],
                        ["Kesit Yüzeyi", "Kavite, kist, kalsifikasyon, kanama", "Tümör içi sekonder dejenerasyonları ve nekrozu gösterir"],
                        ["Cerrahi Sınır Mesafesi", "En yakın rezeksiyon sınırına milimetre mesafesi", "Tümörün cerrahi olarak tamamen çıkıp çıkmadığını belirler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Makroskopi, histopatolojik tanıda mikroskop altına gidecek dokuların seçildiği 'örnekleme' (sampling) aşamasının rehberidir.",
                "📌 [SINAV SPOTU] Rezeksiyon cerrahi sınırlarının mikroskopta anlaşılabilmesi için makroskopide doku sınırları özel çini mürekkebiyle boyanır.",
                "🚨 [KRİTİK UYARI] Makroskobik inceleme yapılmadan dokunun rastgele parçalanması cerrahi sınır oryantasyonunu kalıcı olarak yok eder."
            ],
            "medicalTerms": [
                {"term": "Patolojik Anatomi", "explanation": "Hastalıkların organlarda oluşturduğu çıplak gözle görülebilen yapısal değişiklikleri inceler."},
                {"term": "Örnekleme (Sampling)", "explanation": "Rezeksiyon dokusundan mikroskopi için en kritik kısımların seçilip kasetlenmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Makroskobik İncelemeden Mikroskopiye Tanı Zinciri",
                    [
                        "1. [Rezeksiyon Kabulü]: Cerrahi organ materyalinin anatomik aksı ve oryantasyonu belirlenir.",
                        "2. [Cerrahi Sınır Boyama]: Rezeksiyon hatları mikroskopik takip için çini mürekkebiyle işaretlenir.",
                        "3. [Dilimleme ve Ölçüm]: Organ paralel kesitlere ayrılarak lezyonun boyutu ve derinliği ölçülür.",
                        "4. [Temsili Örnekleme]: Tümörün en derin invazyon odağı ve cerrahi sınırlar kasetlere alınır.",
                        "5. [Mikroskobik Doğrulama]: Hazırlanan histolojik kesitlerde kesin tanı ve patolojik evre verilir."
                    ]
                ),
                make_micro_quiz(
                    "Bir patoloji uzmanının mastektomi materyalini incelerken cerrahi sınırları çini mürekkebiyle boyamasının temel nedeni nedir?",
                    {
                        "A": "Mastektomi materyalini bakteriyel kontaminasyona karşı sterilize etmek",
                        "B": "Mikroskop altında kesit incelenirken dokunun gerçek cerrahi dış sınırını net olarak görebilmek",
                        "C": "Formalin fiksasyonunun doku derinliklerine nüfuz etmesini hızlandırmak",
                        "D": "Tümör hücrelerinin nükleer atipisini floresan mikroskopta görünür kılmak",
                        "E": "Parafin bloklama esnasında dokunun erimesini önlemek"
                    },
                    "B",
                    {
                        "A": "Çini mürekkebi cerrahi dokuda sterilizasyon amacıyla kullanılmaz.",
                        "B": "Mürekkep mikroskopta koyu bir hat oluşturarak cerrahi sınır invazyonunu netleştirir.",
                        "C": "Mürekkep uygulamasının formalin doku penetrasyon hızına etkisi yoktur.",
                        "D": "Nükleer atipi ve kromatin detayları rutin histopatolojik boyalarla incelenir.",
                        "E": "Parafin bloklama doku gömme adımıdır ve mürekkeple bir ilgisi yoktur."
                    }
                ),
                make_cloze(
                    "Rezeksiyon materyallerinden mikroskobik değerlendirme için en kritik odakların seçilip kasetlere alınması işlemine örnekleme adı verilir.",
                    "örnekleme",
                    "Büyük dokudan mikroskopiye temsil edici parça alma basamağı"
                )
            ]
        },

        # Adım 32
        {
            "slideNumber": 32,
            "title": "Cerrahi Patoloji (Surgical Pathology): Yaşayan Hastanın Tedavi Rotası",
            "subtitle": "Cerrahi patoloji, canlı hastalardan biyopsi ve ameliyatlarla çıkarılan dokuları inceleyerek klinik tanı ve onkolojik tedaviyi yöneten alandır.",
            "badge": "Cerrahi Patoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """==Cerrahi Patoloji==, canlı hastalardan tanı ve tedavi amacıyla çıkarılan dokuları inceleyerek onkolojik yönetimi belirleyen temel daldır.

Küçük bir endoskopik biyopsiden geniş organ rezeksiyonlarına kadar tüm canlı doku örnekleri bu kapsamda değerlendirilir. Cerrahi patolog; kesin histolojik tanıyı koyar, diferansiyasyonu belirten **dereceyi (grade)** saptar ve cerrahi sınırların temizliğini denetler. Diseke edilen lenf nodları ve tümör çapı üzerinden nihai **patolojik evrelemeyi (pTNM)** gerçekleştirir. Klinisyenler kemoterapi, radyoterapi ve immünoterapi kararlarını bu rapordaki prognostik parametrelere göre yapılandırır.

> [TEMEL İLKE] Cerrahi patoloji raporundaki evreleme ve sınır durumu, onkolojik tedavinin yol haritasıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Canlı Doku Analizi", "desc": "Biyopsi, küretaj, rezeksiyon ve amputasyon materyallerini inceler.", "isKey": True},
                    {"title": "Onkolojik Tedavi Rehberi", "desc": "Kemoterapi ve radyoterapi endikasyonunu rapor parametreleri belirler.", "isKey": True},
                    {"title": "pTNM Evrelemesi", "desc": "Patoloğun mikroskopik ölçümleriyle nihai patolojik evre (pTNM) kurulur.", "isKey": False}
                ],
                "table": {
                    "title": "Cerrahi Patoloji İnceleme Yelpazesi",
                    "headers": ["Materyal Düzeyi", "Klinik Örnek", "Cerrahi Patoloğun Yanıtladığı Kritik Soru"],
                    "rows": [
                        ["Küçük Biyopsi", "Mide endoskopik forseps biyopsisi", "H. pylori gastriti mi, intestinal metaplazi mi, adenokarsinom mu?"],
                        ["İnsizyonel Biyopsi", "Uyluk derin kitle insizyonel biyopsisi", "Benign mezenkimal lezyon mu yoksa yüksek dereceli sarkom mu?"],
                        ["Eksizyonel Biyopsi", "Şüpheli pigmente deri lezyonu eksizyonu", "Displastik nevüs mü yoksa malign melanom mu; breslow kalınlığı nedir?"],
                        ["Radikal Rezeksiyon", "Kolon kanseri rezeksiyonu ve lenf diseksiyonu", "Tümör serozayı aşmış mı, kaç adet lenf nodunda metastaz saptandı?"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Cerrahi patoloji, canlı hastalardan tanı ve tedavi amacıyla çıkarılan her türlü dokunun patolojik incelemesini kapsar.",
                "📌 [SINAV SPOTU] TNM sınıflamasında 'c' harfi klinik evreyi (cTNM), 'p' harfi ise cerrahi patolog tarafından doğrulanmış patolojik evreyi (pTNM) ifade eder.",
                "💡 [ÖĞRENME İPUCU] Patolojik evreleme (pTNM), görüntüleme ile yapılan klinik evrelemeden çok daha kesin ve güvenilirdir."
            ],
            "medicalTerms": [
                {"term": "Cerrahi Patoloji", "explanation": "Yaşayan hastalardan alınan biyopsi ve rezeksiyonları inceleyerek kesin tanı koyan daldır."},
                {"term": "pTNM", "explanation": "Rezeksiyon dokusunda tümör, lenf nodu ve metastazı belirleyen patolojik evredir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Kolon rezeksiyonu sonrası cerrahi patoloji raporunda cerrahi sınır pozitifliği saptanması senaryosu.",
                    [
                        {
                            "text": "Pozitif sınır sadece mikroskobik olduğu için ek işlem yapılmaz, hasta rutin 1 yıllık kontrole çağrılır.",
                            "isCorrect": False,
                            "feedback": "Hatalı yaklaşım. Pozitif sınır geride tümör kaldığını gösterir ve lokal nüks riskini katlar."
                        },
                        {
                            "text": "Hasta multidisipliner tümör konseyine sunulur; re-rezeksiyon (cerrahi sınırın genişletilmesi) veya adjuvan kemoradyoterapi planlanır.",
                            "isCorrect": True,
                            "feedback": "Doğru klinik yaklaşım. Pozitif sınırda re-rezeksiyon veya ek adjuvan tedavi planlanmalıdır."
                        },
                        {
                            "text": "Patoloji raporundaki cerrahi sınır dikkate alınmaz; sadece kolonoskopi sonucu beklenir.",
                            "isCorrect": False,
                            "feedback": "Hatalı yaklaşım. Cerrahi sınır patolojisi onkolojik cerrahinin bağlayıcı sonucudur."
                        }
                    ]
                ),
                make_active_recall(
                    "Klinik evreleme (cTNM) ile Patolojik evreleme (pTNM) arasındaki temel fark nedir ve hangisi daha üstündür?",
                    "Klinik evreleme muayene ve radyolojiye dayanırken, patolojik evreleme cerrahi dokunun mikroskobik incelenmesiyle yapılır. pTNM mikroskobik invazyon derinliğini ve lenf nodu metastazını kanıtladığı için çok daha üstün ve güvenilirdir."
                ),
                make_cloze(
                    "Canlı hastalardan tanı ve tedavi amacıyla çıkarılan tüm doku ve organların incelendiği patoloji ana dalına cerrahi patoloji adı verilir.",
                    "cerrahi patoloji",
                    "Yaşayan insan biyopsi ve ameliyat parçalarını inceleyen dal"
                )
            ]
        },

        # Adım 33
        {
            "slideNumber": 33,
            "title": "Otopsi Patolojisi: Klinik (Tıbbi) Otopsi ve Kalite Kontrolü",
            "subtitle": "Klinik otopsi; hastanede vefat eden hastaların ölüm mekanizmasını aydınlatan, klinik tanı doğruluğunu denetleyen ve tıp eğitimini besleyen altın standarttır.",
            "badge": "Klinik Otopsi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """==Klinik (tıbbi) otopsi==; hastanede tedavi altındayken vefat eden hastalarda ailenin yazılı rızasıyla patologlar tarafından gerçekleştirilen postmortem incelemedir.

Bu incelemenin temel amacı, kesin ölüm nedenini ve patogenetik süreci ortaya koyarak klinik tanı doğruluğunu denetlemektir. Ölüm öncesi (**antemortem**) klinik tanılar ile ölüm sonrası (**postmortem**) patolojik bulgular karşılaştırılarak sağlık hizmetinin kalite kontrolü sağlanır. Klinik otopsi ayrıca uygulanan cerrahi veya medikal tedavilerin doku düzeyindeki etkinliğini değerlendirir ve tıp eğitimini zenginleştirir. Modern merkezlerde bile otopsiler, klinik süreçte fark edilmeyen majör tanıları ortaya çıkarabilmektedir.

> [KLİNİK İNCİ] Klinik otopsi; tıbbın tanısal başarısını denetleyen ve hekimlik kalitesini geliştiren bir öz değerlendirmedir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hasta Yakını Onayı", "desc": "Klinik otopsi için aileden bilgilendirilmiş yazılı rıza alınması yasal zorunluluktur.", "isKey": True},
                    {"title": "Tıbbi Kalite Denetimi", "desc": "Klinik tanı ile gerçek patolojik tanı arasındaki uyumu denetler.", "isKey": True},
                    {"title": "Eğitimsel Değer", "desc": "Klinisyenlere ve tıp öğrencilerine hastalıkların doğal seyrini ve komplikasyonlarını öğretir.", "isKey": False}
                ],
                "table": {
                    "title": "Klinik Otopsi İnceleme Süreci",
                    "headers": ["Aşama", "Yapılan İşlem", "Elde Edilen Tıbbi Veri"],
                    "rows": [
                        ["Dış Muayene", "Cesedin boyu, kilosu, ameliyat izleri, kateter girişleri, siyanoz", "Genel beslenme ve dış travma/tedavi izleri"],
                        ["İç Diseksiyon", "Toraks, batın ve kranial kavitelerin açılması; organların çıkarılması", "Sıvı toplanmaları (plevral efüzyon, asit), organomegali"],
                        ["Organ Diseksiyonu", "Kalp, akciğer, beyin, karaciğer vb. organların tartılması ve kesitleri", "Miyokard enfarktüsü, pulmoner tromboemboli, siroz kanıtı"],
                        ["Histopatoloji", "Her organdan alınan parafin blokların mikroskobik incelenmesi", "Hücresel düzeyde nihai ölüm nedeni raporu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Klinik (tıbbi) otopsi, doğal nedenlerle ölen hastalarda ailenin yazılı rızasıyla yapılan ve klinik tanıların doğruluğunu denetleyen otopside.",
                "📌 [SINAV SPOTU] Otopsi kelimesi Yunanca 'kendi gözleriyle görmek' (autopsia) kökünden türetilmiştir.",
                "🚨 [KRİTİK UYARI] Şüpheli, travmatik veya hekim hatası iddiası olan ölümlerde klinik otopsi yapılamaz; savcılık el koyarak Adli Otopsi açılır."
            ],
            "medicalTerms": [
                {"term": "Klinik Otopsi (Tıbbi Otopsi)", "explanation": "Hastanede ölenlerde aile rızasıyla ölüm nedenini ve tanı doğruluğunu denetleyen incelemedir."},
                {"term": "Antemortem", "explanation": "Ölümden önceki klinik süreçleri ve laboratuvar bulgularını tanımlayan terimdir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Otopsi Basamakları ve Tanısal Karşılıkları",
                    ["Basamak", "Yöntem", "Saptanan Kritik Patoloji"],
                    [
                        [
                            ("Kranial Diseksiyon", False),
                            ("Beyin çıkarılması ve koronal kesit", True, "Serebral patoloji değerlendirmesi"),
                            ("Masif hipertansif intraserebral hematom", False)
                        ],
                        [
                            ("Pulmoner Vasküler İnceleme", False),
                            ("Pulmoner arter dallarının açılması", True, "Solunum sistemi damar kontrolü"),
                            ("Saddle (semer) emboli ve akut sağ kalp yetmezliği", False)
                        ],
                        [
                            ("Miyokard Kesitleri", False),
                            ("Ventriküllerin 1 cm aralıkla dilimlenmesi", True, "Kalp kası iskemik hasarı"),
                            ("Sol ventrikülde transumural koagülasyon nekrozu", False)
                        ]
                    ]
                ),
                make_cloze(
                    "Hastanede tedavi altındayken doğal nedenlerle ölen hastalarda aile rızasıyla ölüm nedenini araştıran işleme klinik otopsi adı verilir.",
                    "klinik otopsi",
                    "Hastanede ailenin onayıyla hekim kalitesini denetleyen inceleme"
                ),
                make_micro_quiz(
                    "Klinik otopsinin tıp bilimi ve sağlık sistemindeki rolü ile ilgili aşağıdakilerden hangisi en doğrudur?",
                    {
                        "A": "Modern görüntüleme (MR, PET) sayesinde klinik otopsiye tıp pratiğinde artık hiç gerek kalmamıştır.",
                        "B": "Klinik otopsi antemortem tanıların doğruluğunu test eden ve tıp eğitimini besleyen bir kalite kontrol yöntemidir.",
                        "C": "Klinik otopsi savcılık emriyle zorunlu olarak yapılır ve aile onayı aranmaz.",
                        "D": "Klinik otopside organlardan mikroskobik inceleme için parça alınması yasaktır.",
                        "E": "Klinik otopsiyi yalnızca adli tıp uzmanları yapabilir, patologların otopsi yetkisi yoktur."
                    },
                    "B",
                    {
                        "A": "İleri görüntüleme yöntemlerine rağmen otopsi öngörülemeyen majör klinik patolojileri saptayabilir.",
                        "B": "Klinik otopsi tanısal doğruluğu test eden ve sağlık hizmet kalitesini artıran temel araçtır.",
                        "C": "Savcılık talimatıyla ve rıza aranmaksızın yapılan inceleme adli otopside geçerlidir.",
                        "D": "Histopatolojik doku örneklemesi klinik otopsinin zorunlu bir tamamlayıcısıdır.",
                        "E": "Klinik otopsileri mevzuat uyarınca Tıbbi Patoloji uzmanları yürütür."
                    }
                )
            ]
        },

        # Adım 34
        {
            "slideNumber": 34,
            "title": "Adli Patoloji (Forensic Pathology): Şüpheli Ölümler ve Hukuki Adalet",
            "subtitle": "Adli patoloji; cinayet, intihar, kaza veya ani şüpheli ölümlerde ölüm nedenini, mekanizmasını ve orjinini hukuki kanıt standartlarında belirler.",
            "badge": "Adli Patoloji",
            "badgeColor": "purple",
            "discipline": "Adli Tıp ve Patoloji",
            "synthesisNarrative": """==Adli Patoloji==; şüpheli, ani veya doğal olmayan tüm ölümlerde yargı makamlarının talimatıyla maddi delil üreten uzmanlık dalıdır.

Klinik otopsidekinin aksine bu süreçte ==aile rızası aranmaz==; inceleme savcılık veya mahkeme kararıyla zorunlu yürütülür. Adli patolog ceset üzerinde üç temel soruyu aydınlatır: Ölüme yol açan travma veya hasarı tanımlayan **ölüm nedeni**, buna eşlik eden fizyopatolojik çöküşü açıklayan **ölüm mekanizması** ve olayın niteliğini belirten **ölüm orijini** (cinayet, kaza, intihar veya doğal). Süreç, toksikolojik analizler ve ölüm zamanı tespiti ile tamamlanarak adli makamlara sunulur.

> [YASAL İLKE] Adli patoloji, şüpheli ölümlerde bilimsel delil üreterek adaletin sağlanmasına hizmet eder.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Savcılık Kararı", "desc": "Kamu adına yürütülür, aile izni gerekmez ve reddedilemez.", "isKey": True},
                    {"title": "Üçlü Soru Analizi", "desc": "Ölüm nedeni, mekanizması ve orijini (cinayet/kaza/intihar) belirlenir.", "isKey": True},
                    {"title": "Toksikoloji Entegrasyonu", "desc": "Kan, idrar ve iç organlardan zehir ve ilaç analizleri yapılır.", "isKey": False}
                ],
                "table": {
                    "title": "Klinik Otopsi ile Adli Otopsi Arasındaki Temel Farklar",
                    "headers": ["Özellik", "Klinik (Tıbbi) Otopsi", "Adli (Forensic) Otopsi"],
                    "rows": [
                        ["Yasal Dayanak & Karar", "Hekimin talebi ve ailenin yazılı rızası", "Cumhuriyet Savcılığı veya Hakimlik kararı (zorunlu)"],
                        ["Vaka Niteliği", "Hastanede doğal hastalık seyrinde ölen hastalar", "Ani, şüpheli, travmatik, zehirlenme veya cinayet vakaları"],
                        ["Yapan Uzman", "Tıbbi Patoloji Uzmanı", "Adli Tıp Uzmanı ve Adli Patolog"],
                        ["Temel Amaç", "Klinik tanı başarısı ve patofizyolojik eğitim", "Ölüm nedeni, orijini ve ceza hukukuna kanıt üretimi"],
                        ["Toksikolojik İnceleme", "Nadiren gerekir", "Rutin olarak kan, idrar ve organ örnekleri alınır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Adli otopsilerde aile onayı aranmaz; Cumhuriyet Savcılığı kararıyla re'sen yapılır.",
                "📌 [SINAV SPOTU] Ölüm orijini (manner of death) 5 temel kategoriden oluşur: Doğal, Cinayet, İntihar, Kaza ve Belirlenemeyen.",
                "💡 [ÖĞRENME İPUCU] 'Hemorajik şok' ölüm mekanizmasıdır; 'ateşli silah yaralanması' ise ölüm nedenidir."
            ],
            "medicalTerms": [
                {"term": "Adli Patoloji", "explanation": "Şüpheli ve adli ölümlerde ölüm nedeni, mekanizması ve orijinini belirleyen uzmanlık alanıdır."},
                {"term": "Ölüm Orijini (Manner of Death)", "explanation": "Ölümün cinayet, intihar, kaza veya doğal niteliğini tanımlayan hukuki kategoridir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Klinik Otopsi vs Adli Otopsi Yetki ve Prosedür Farkları",
                    "Klinik Otopsi",
                    "Adli Otopsi",
                    [
                        "Hasta yakınlarının yazılı rıza ve onayı şarttır",
                        "Hastanede doğal hastalık komplikasyonuyla ölenler incelenir",
                        "Tıbbi kalite kontrolü ve akademik eğitim hedeflenir",
                        "Rapor hastane arşivine ve tıp literatürüne girer"
                    ],
                    [
                        "Cumhuriyet Savcısının yasal talimatıyla zorunlu yapılır",
                        "Şüpheli, cinayet, intihar veya kaza ölümleri incelenir",
                        "Maddi gerçeğin ortaya çıkarılması ve adalet hedeflenir",
                        "Rapor adli mahkemeye resmi delil olarak sunulur"
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdaki ölüm durumlarından hangisinde klinik otopsi yapılması YASAL OLARAK İMKANSIZDIR ve derhal adli makamlara bildirilmelidir?",
                    {
                        "A": "İleri evre pankreas kanseri tanısıyla onkoloji servisinde takip edilirken vefat eden hasta",
                        "B": "Diyabetik ketoasidoz koması nedeniyle yoğun bakımda tüm tedavilere rağmen kaybedilen hasta",
                        "C": "Evinde merdivenden düşme sonrası kafa travmasıyla acil servise getirilip 2 saat sonra ölen şahıs",
                        "D": "Son dönem kalp yetmezliği bulunan ve kardiyoloji servisinde arrest olan hasta",
                        "E": "Tüberküloz pnömonisi tanısıyla izlenirken solunum yetmezliğinden vefat eden hasta"
                    },
                    "C",
                    {
                        "A": "Onkolojik doğal ölüm olgularında aile rızasıyla klinik otopsi yapılabilir.",
                        "B": "Diyabet komplikasyonuna bağlı doğal ölümler klinik otopsi kapsamında kalır.",
                        "C": "Travmatik kafa yaralanması adli bir vaka olup derhal savcılığa bildirilmelidir.",
                        "D": "Kronik kardiyak yetmezliğe bağlı ölümler doğal ölüm niteliğindedir.",
                        "E": "Tüberküloz enfeksiyonu seyrindeki kayıplar klinik patoloji alanına girer."
                    }
                ),
                make_cloze(
                    "Adli otopsilerde ölümün hukuki gerçekleşme biçimini tanımlayan cinayet, intihar veya kaza sınıflamasına ölüm orijini adı verilir.",
                    "ölüm orijini",
                    "Ölümün adli gerçekleşme biçimi kavramı"
                )
            ]
        },

        # Adım 35
        {
            "slideNumber": 35,
            "title": "Sitopatoloji: Doku Bütünlüğü Olmadan Hücreden Teşhise",
            "subtitle": "Sitopatoloji; vücut sıvıları, dökülen veya iğneyle aspire edilen tek tek hücrelerin morfolojisinden hızlı ve minimal invaziv tanı koyma sanatıdır.",
            "badge": "Sitopatoloji",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """==Sitopatoloji==; doku bütünlüğü aranmaksızın tek tek dökülen veya aspire edilen hücrelerin incelenmesine dayanan hızlı ve minimal invaziv bir tanı dalıdır.

İnceleme başlıca üç yöntemle toplanan hücrelerde yapılır: Kendiliğinden dökülen hücrelerin incelendiği **eksfolyatif sitoloji** (PAP smear, idrar veya plevra sıvısı), endoskopik fırçalama sitolojisi ve palpabl kitlelerden vakumla hücre çekilen **ince iğne aspirasyon sitolojisi (İİAS)**. Sitoloji poliklinik şartlarında dakikalar içinde ön tanı sağlar. Ancak stroma ve bazal membran ilişkisi görülemediğinden, invazyon derinliğinin kanıtlanması gereken durumlarda histopatolojik biyopsi doğrulaması şarttır.

> [TEMEL İLKE] Sitopatoloji mükemmel bir tarama ve ön tanı aracıdır; doku mimarisi gerektiren durumlarda cerrahi biyopsi esastır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hücresel Düzey", "desc": "Nükleus büyüklüğü, pleomorfizm, N/S oranı ve kromatin paterni incelenir.", "isKey": True},
                    {"title": "Minimal İnvaziv", "desc": "Cerrahi kesi olmadan poliklinik şartlarında hızlıca uygulanabilir.", "isKey": True},
                    {"title": "Mimarinin Yokluğu", "desc": "İnvazyon derinliği ve doku stroması görülemediği için bazen biyopsiyle teyit gerekir.", "isKey": False}
                ],
                "table": {
                    "title": "Sitopatoloji ile Histopatoloji Karşılaştırması",
                    "headers": ["Kriter", "Sitopatoloji", "Histopatoloji"],
                    "rows": [
                        ["İncelenen Birim", "Tek tek hücreler veya küçük hücre grupları", "Hücreler + hücreler arası stroma + doku mimarisi"],
                        ["Örnek Alma Şekli", "Sürüntü, sıvı aspirasyonu, ince iğne (22G)", "Punch, forseps biyopsi, eksizyon, cerrahi rezeksiyon"],
                        ["İşlem Hızı", "Çok hızlı (dakikalar veya saatler)", "Doku takibi gerektirir (24-48 saat)"],
                        ["İnvazyon Tespiti", "Bazal membran ilişkisi görülemez", "Kanser invazyonu kesin olarak kanıtlanır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sitopatoloji hücre düzeyinde inceleme yapar; stroma ve bazal membran mimarisi değerlendirilemez.",
                "📌 [SINAV SPOTU] Servikal PAP smear, tıp tarihindeki en başarılı ve mortaliteyi en çok düşüren eksfolyatif sitoloji tarama yöntemidir.",
                "💡 [ÖĞRENME İPUCU] Bir tiroid nodülüne ameliyat kararı vermeden önce yapılan ilk tanı adımı İnce İğne Aspirasyon Sitolojisidir (İİAS)."
            ],
            "medicalTerms": [
                {"term": "Sitopatoloji", "explanation": "İzole hücrelerin morfolojik özelliklerini inceleyerek hızlı tanı koyan patoloji dalıdır."},
                {"term": "Eksfolyatif Sitoloji", "explanation": "Epitel yüzeylerinden kendiliğinden dökülen hücrelerin incelenmesi yöntemidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İnce İğne Aspirasyon Sitolojisi (İİAS) Tanı Zinciri",
                    [
                        "1. [Lezyon Odaklama]: Tiroid veya meme kitlesi ultrason ya da palpasyonla netleştirilir.",
                        "2. [Hücresel Aspirasyon]: İnce iğne ve negatif basınç yardımıyla kitleden hücre aspire edilir.",
                        "3. [Yayma ve Fiksasyon]: Aspire edilen materyal lama yayılıp alkol veya havayla fikse edilir.",
                        "4. [Sitolojik Boyama]: Preparatlar Giemsa veya PAP boyasıyla boyanarak çekirdek detayları incelenir.",
                        "5. [Tanısal Raporlama]: Standart sitopatoloji sınıflamasına göre selim, kuşkulu veya habis tanı verilir."
                    ]
                ),
                make_micro_quiz(
                    "Sitopatolojinin cerrahi histopatolojiye kıyasla en belirgin kısıtlılığı ve zayıf yönü aşağıdakilerden hangisidir?",
                    {
                        "A": "Hücrelerin çekirdek morfolojisinin ve kromatin yapısının değerlendirilememesi",
                        "B": "Doku mimarisi ve bazal membran ilişkisi görülemediğinden mikroinvazyonun kanıtlanamaması",
                        "C": "Hiçbir malign tümör hücresinin sitolojide ayırt edilememesi",
                        "D": "Sonuç alma süresinin histopatolojiden çok daha uzun (haftalar) sürmesi",
                        "E": "Örnekleme sırasında hastaya genel anestezi verilmesinin zorunlu olması"
                    },
                    "B",
                    {
                        "A": "Sitopatoloji çekirdek yapısını ve kromatin özelliklerini son derece net gösterir.",
                        "B": "Doku mimarisi korunamadığı için bazal membran invazyonu sitolojide doğrudan gösterilemez.",
                        "C": "Malign hücre kriterleri sitopatolojik preparatlarda yüksek duyarlılıkla tanımlanır.",
                        "D": "Sitopatolojik inceleme histopatolojiye göre çok daha hızlı sonuç verir.",
                        "E": "Sitolojik aspirasyon anestezi gerektirmeyen ayaktan poliklinik işlemidir."
                    }
                ),
                make_cloze(
                    "Vücut epitel yüzeylerinden veya organ boşluklarından kendiliğinden dökülen hücrelerin incelenmesine eksfolyatif sitoloji adı verilir.",
                    "eksfolyatif sitoloji",
                    "Dökülen hücrelerin incelendiği sitoloji türü"
                )
            ]
        },

        # Adım 36
        {
            "slideNumber": 36,
            "title": "Moleküler Patoloji ve Kişiselleştirilmiş Tıp (Personalized Medicine)",
            "subtitle": "Moleküler patoloji; doku ve hücrelerdeki DNA, RNA ve protein değişimlerini analiz ederek hedefe yönelik onkolojik tedavilerin kapısını aralar.",
            "badge": "Moleküler Patoloji",
            "badgeColor": "emerald",
            "discipline": "Moleküler Patoloji",
            "synthesisNarrative": """==Moleküler Patoloji==; tümör dokularındaki DNA, RNA ve protein değişimlerini analiz ederek hedefe yönelik tedavilere rehberlik eder.

Bu disiplinde **PCR**, kromozomal translokasyon ve gen amplifikasyonlarını gösteren **FISH** ve yüzlerce geni eşzamanlı tarayan **Yeni Nesil Dizileme (NGS)** teknikleri kullanılır. Moleküler testler yalnızca tanıyı kesinleştirmekle kalmaz; tümörün hedefe yönelik ilaçlara yanıtını belirleyen ==prediktif bilgiler== sağlar. Örneğin akciğer karsinomunda EGFR mutasyonu hedefe kilitli tirozin kinaz inhibitörlerinin yolunu açarken, kolorektal karsinomda KRAS mutasyonu anti-EGFR tedavisine direnci öngörür.

> [YENİ UFUK] Moleküler patoloji, standart tedavilerin yerini alan kişiselleştirilmiş onkolojinin temelidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Genetik Biyobelirteçler", "desc": "EGFR, ALK, KRAS, BRAF gibi mutasyonlar tedavi seçimini yönetir.", "isKey": True},
                    {"title": "FISH ve NGS Teknolojileri", "desc": "Gen amplifikasyonu, delesyon ve translokasyonlar mikron düzeyinde haritalanır.", "isKey": True},
                    {"title": "Kişiselleştirilmiş Onkoloji", "desc": "Hasta tümörünün spesifik moleküler defektine yönelik hedefe kilitli ilaç seçilir.", "isKey": False}
                ],
                "table": {
                    "title": "Klinik Onkolojide Rutin Moleküler Patoloji Testleri",
                    "headers": ["Tümör Tipi", "Test Edilen Gen / Belirteç", "Hedefe Yönelik Tedavi / Klinik Karar"],
                    "rows": [
                        ["Akciğer Adenokarsinomu", "EGFR ekzon 19 delesyonu / L858R", "Oral tirozin kinaz inhibitörleri (Osimertinib, Erlotinib) yanıtı"],
                        ["Akciğer Adenokarsinomu", "ALK veya ROS1 gen füzyonu", "ALK inhibitörleri (Krizotinib, Alektinib) endikasyonu"],
                        ["Kolorektal Karsinom", "KRAS / NRAS mutasyon durumu", "Mutasyon varsa anti-EGFR (Setuksimab) etkisizdir, verilmez"],
                        ["Meme Karsinomu", "HER2 (ERBB2) amplifikasyonu (FISH)", "Trastuzumab (anti-HER2 monoklonal antikor) tedavisi"],
                        ["Malign Melanom", "BRAF V600E mutasyonu", "BRAF inhibitörleri (Dabrafenib/Trametinib) yanıtı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Meme kanserinde İHK ile şüpheli (+2) bulunan HER2 pozitifliğini kesinleştirmek için FISH (Floresan In Situ Hibridizasyon) testi yapılır.",
                "📌 [SINAV SPOTU] Kolon kanserinde KRAS geni mutant ise anti-EGFR hedefli biyolojik tedaviler direnç nedeniyle uygulanamaz.",
                "🔬 [TEKNOLOJİ SPOTU] NGS (Yeni Nesil Dizileme), tek bir formalin parafin bloktan onlarca gen mutasyonunu eşzamanlı saptar."
            ],
            "medicalTerms": [
                {"term": "Moleküler Patoloji", "explanation": "Doku ve hücrelerdeki DNA/RNA düzeyindeki genetik anomalileri inceleyen patoloji dalıdır."},
                {"term": "FISH (Floresan In Situ Hibridizasyon)", "explanation": "Floresan problarla gen amplifikasyonlarını ve translokasyonları gösteren moleküler yöntemdir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Moleküler Belirteçler ve Tedavi Eşleştirmesi",
                    ["Kanser Türü", "Moleküler Hedef", "Klinik Tedavi Kararı"],
                    [
                        [
                            ("Meme Kanserinde HER2", False),
                            ("Gen Amplifikasyonu", True, "Gen kopya sayısının aşırı artması"),
                            ("Trastuzumab hedefe yönelik antikor tedavisi", False)
                        ],
                        [
                            ("Kolon Kanserinde KRAS", False),
                            ("Nokta Mutasyonu", True, "GTPaz aktivitesinin sürekli açık kalması"),
                            ("Anti-EGFR tedavisine direnç gelişir", False)
                        ],
                        [
                            ("Melanomda BRAF V600E", False),
                            ("Sinyal Yolağı Aktivasyonu", True, "MAPK yolağının aşırı çalışması"),
                            ("Dabrafenib/Trametinib kombinasyonu", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Kolon adenokarsinomlu bir hastada moleküler patoloji raporunda 'KRAS Ekzon 2 Kodon 12 Mutasyonu Saptandı' sonucu gelmiştir. Onkoloji konseyinin bu hastadaki kararı ne olmalıdır?",
                    {
                        "A": "Hasta derhal anti-EGFR monoklonal antikor tedavisine (Setuksimab) alınmalıdır.",
                        "B": "KRAS mutasyonu olduğunda EGFR yolağı reseptörden bağımsız downstream aktifleştiğinden anti-EGFR tedavisi etkisizdir ve verilmemelidir.",
                        "C": "KRAS mutasyonu sadece cerrahi sınır değerlendirmesinde kullanılır, ilaç seçiminde önemi yoktur.",
                        "D": "Hasta doğrudan kür olmuş kabul edilir ve kemoterapi sonlandırılır.",
                        "E": "Tümör benign kabul edilir ve evreleme iptal edilir."
                    },
                    "B",
                    {
                        "A": "KRAS mutasyonu varlığında anti-EGFR tedavisi direnç nedeniyle etkisiz kalır.",
                        "B": "Downstream KRAS mutasyonu yolağı sürekli aktif tuttuğundan üst reseptörü bloklamak fayda sağlamaz.",
                        "C": "KRAS analizi cerrahi sınırdan ziyade hedefe yönelik ilaç seçimini belirler.",
                        "D": "Genetik mutasyon varlığı tümörün kür olduğunu göstermez, tedavi yanıtını yönlendirir.",
                        "E": "Moleküler analiz sonucu tümörün malignite potansiyelini ortadan kaldırmaz."
                    }
                ),
                make_cloze(
                    "Meme karsinomlarında gen kopya sayısı artışını floresan problarla hücre çekirdeğinde gösteren moleküler yönteme FISH adı verilir.",
                    "FISH",
                    "Floresan işaretli in situ hibridizasyon yönteminin kısaltması"
                )
            ]
        },

        # Adım 37
        {
            "slideNumber": 37,
            "title": "Deneysel Patoloji (Experimental Pathology): Hastalık Mekanizmalarının Laboratuvarda Çözülmesi",
            "subtitle": "Deneysel patoloji; klinik gözlemleri laboratuvar ortamına taşıyarak hücre kültürü ve hayvan modellerinde hastalık mekanizmalarını araştıran akademik daldır.",
            "badge": "Deneysel Patoloji",
            "badgeColor": "indigo",
            "discipline": "Deneysel Patoloji",
            "synthesisNarrative": """==Deneysel Patoloji==; hastalıkların etiyoloji ve mekanizmalarını kontrollü laboratuvar modelleri üzerinde aydınlatan temel tıp disiplinidir.

Bu alanda hücresel stres yanıtlarını ölçen **in vitro hücre kültürleri**, belirli genlerin susturulduğu **knock-out hayvan modelleri** ve organ hasarını taklit eden iskemi-reperfüzyon düzenekleri kullanılır. İnsanlarda doğrudan denenmesi etik olmayan toksik süreçler, genetik manipülasyonlar ve yeni moleküller bu modellerde araştırılır. Yeni geliştirilen ilaçların doku düzeyindeki etkinliği ve toksisite profili histopatolojik olarak kanıtlanarak klinik denemelere hazır hale getirilir.

> [BİLİMSEL İLKE] Deneysel patoloji, laboratuvarda keşfedilen temel hücresel mekanizmaları hasta yatağına bağlayan köprüdür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hastalık Modelleri", "desc": "Kemirgenlerde ateroskleroz, diyabet, neoplazi ve otoimmün modeller oluşturulur.", "isKey": True},
                    {"title": "Yeni İlaç Geliştirme", "desc": "Terapötik moleküllerin in vivo toksisitesi ve etkinliği histopatolojik olarak kanıtlanır.", "isKey": True},
                    {"title": "Genetik Manipülasyon", "desc": "Knock-out farelerle hastalık patogenezindeki spesifik genlerin işlevi aydınlatılır.", "isKey": False}
                ],
                "table": {
                    "title": "Deneysel Patolojide Kullanılan Başlıca Araştırma Modelleri",
                    "headers": ["Model Türü", "Uygulama Şekli", "Aydınlatılan Patolojik Süreç"],
                    "rows": [
                        ["Knock-out Fare Modeli", "Hedef genin embriyonik kök hücrede inaktive edilmesi", "Tümör baskılayıcı genlerin (p53, Rb) yokluğunda kanserojenez"],
                        ["İskemi-Reperfüzyon Modeli", "Koroner arterin geçici ligasyonu ve açılması", "Serbest oksijen radikallerinin doku hasarındaki mekanizması"],
                        ["Karsinojen İndüksiyonu", "Kimyasal ajanların (DMBA vb.) dokuya uygulanması", "Tümör başlangıç (initiation) ve ilerleme (progression) fazları"],
                        ["Hücre Kültürü (İn Vitro)", "Primer veya transforme hücre dizilerinin beslenmesi", "Apoptoz sinyal yolaklarının ve ilaç sitotoksisitesinin ölçümü"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Deneysel patoloji, hastalıkların hücresel ve moleküler mekanizmalarını aydınlatmak için in vitro ve hayvan modellerini kullanan araştırma dalıdır.",
                "📌 [BİLİMSEL SPOT] Bir genin fonksiyonunu anlamak için yapılan gen susturma deneylerindeki hayvanlara 'Knock-out' modeli denir.",
                "💡 [ÖĞRENME İPUCU] Klinik patoloji 'hastalığın adı nedir?' sorusunu yanıtlarken, deneysel patoloji 'bu hastalık hücresel düzeyde tam olarak nasıl oluştu?' sorusunu çözer."
            ],
            "medicalTerms": [
                {"term": "Deneysel Patoloji", "explanation": "Hastalık mekanizmalarını ve yeni molekülleri laboratuvar modellerinde araştıran daldır."},
                {"term": "Knock-out Modeli", "explanation": "Belirli bir genin yapay olarak susturulduğu deneysel hayvan modelidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Deneysel Patolojide İlaç Keşif Zinciri",
                    [
                        "1. [Hedef Belirleme]: Hastalık patogenezindeki kritik moleküler yolak tanımlanır.",
                        "2. [İn Vitro Tarama]: Hücre kültürlerinde hedef molekülün apoptoz ve sitotoksisite etkisi ölçülür.",
                        "3. [İn Vivo Uygulama]: Tümör taşıyan deney hayvanlarında ilacın biyolojik etkinliği test edilir.",
                        "4. [Histopatolojik Analiz]: Doku kesitlerinde tümör gerilemesi ve organ toksisitesi değerlendirilir.",
                        "5. [Klinik Faz Geçişi]: Güvenli ve etkili bulunan molekül insan denemelerine aktarılır."
                    ]
                ),
                make_cloze(
                    "Deneysel patolojide bir genin işlevini ve patolojideki rolünü anlamak için o genin inaktive edildiği hayvan modellerine knock-out modeli denir.",
                    "knock-out",
                    "Gen susturma hayvan modeli terimi"
                ),
                make_active_recall(
                    "Deneysel patolojinin modern klinik onkolojiye ve farmakolojiye en büyük katkısı nedir?",
                    "Hastalık patogenezindeki hücresel yolakları aydınlatır. Yeni geliştirilen ilaçların insana verilmeden önce etkinlik ve doku toksisite profillerini kanıtlar."
                )
            ]
        },

        # Adım 38
        {
            "slideNumber": 38,
            "title": "Ultrastrüktürel Patoloji ve Elektron Mikroskopisi (TEM & SEM)",
            "subtitle": "Işık mikroskobunun çözünürlük sınırını aşarak hücresel organelleri, bazal membran kalınlaşmalarını ve viral partikülleri gösteren tanı dalıdır.",
            "badge": "Ultrastrüktür",
            "badgeColor": "orange",
            "discipline": "Ultrastrüktürel Patoloji",
            "synthesisNarrative": """Işık mikroskobunun çözünürlük sınırını aşarak nanometre düzeyindeki hücresel yapıları inceleyen bilim dalına ==Ultrastrüktürel Patoloji== adı verilir.

İncelemede elektron demeti kullanan sistemlerden yararlanılır: Ultra ince kesitlerden geçerek iki boyutlu organel mimarisini gösteren **Transmisyon Elektron Mikroskobu (TEM)** ve üç boyutlu yüzey topografyası sunan **SEM**. Yöntem özellikle medikal nefropatolojide vazgeçilmezdir. Işık mikroskobunda tamamen normal izlenen Minimal Değişiklik Hastalığında podosit ayak çıkıntısı silinmesi ve bazal membran defektleri ancak TEM ile kanıtlanır. Fiksasyonda formalin yerine glutaraldehit kullanılır.

> [TANI KURALI] Glomerüler podosit ayak çıkıntısı hasarı ve bazal membran yarılmaları ancak elektron mikroskobuyla teşhis edilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Elektron Demeti Gücü", "desc": "Işık mikroskobundan yüzlerce kat yüksek çözünürlükle nanometre düzeyinde görüntü sağlar.", "isKey": True},
                    {"title": "Nefropatolojide Şart", "desc": "Glomerüler bazal membran ve podosit defektlerinin tanısında zorunludur.", "isKey": True},
                    {"title": "Özel Fiksasyon", "desc": "Standart formalin yerine %2.5 Glutaraldehit ve Osmik Asit fiksatifi gerektirir.", "isKey": False}
                ],
                "table": {
                    "title": "Işık Mikroskobu ile Transmisyon Elektron Mikroskobu (TEM) Karşılaştırması",
                    "headers": ["Özellik", "Işık Mikroskobu", "Transmisyon Elektron Mikroskobu (TEM)"],
                    "rows": [
                        ["Işın Kaynağı", "Görünür ışık fotonları", "Yüksek voltajlı elektron demeti"],
                        ["Çözünürlük Sınırı", "~0.2 µm (200 nm)", "~0.1-0.2 nm (nanometre)"],
                        ["Kesit Kalınlığı", "3 - 5 mikrometre (µm)", "50 - 80 nanometre (nm) (ultra ince kesit)"],
                        ["Gömme Maddesi", "Parafin", "Epoksi reçine (Epon / Araldite)"],
                        ["Kritik Kullanım Alanı", "Rutin tümör ve cerrahi patoloji", "Glomerülonefritler, primer siliyer diskinezi, virüsler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Minimal Değişiklik Hastalığında (Minimal Change Disease) ışık mikroskopisi tamamen normaldir; podosit ayak çıkıntısı silinmesi yalnız Elektron Mikroskobu ile saptanır.",
                "📌 [SINAV SPOTU] Elektron mikroskopisi için dokular formalin yerine glutaraldehit içinde tespit edilmeli ve epoksi reçineye gömülmelidir.",
                "💡 [ÖĞRENME İPUCU] SEM hücrenin dış yüzey heykelini (3D), TEM ise hücrenin iç organel röntgenini (2D) verir."
            ],
            "medicalTerms": [
                {"term": "Ultrastrüktür", "explanation": "Hücrelerin elektron mikroskobuyla incelenen nanometre düzeyindeki ince organel mimarisidir."},
                {"term": "Transmisyon Elektron Mikroskobu (TEM)", "explanation": "Elektron demetiyle hücre içi organel mimarisini nanometre düzeyinde gösteren mikroskoptur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Işık Mikroskopisi vs Elektron Mikroskopisi (TEM) Tanı Gücü",
                    "Işık Mikroskopisi",
                    "Elektron Mikroskopisi (TEM)",
                    [
                        "Işık dalga boyu sınırı nedeniyle en fazla 1000-1500x büyütür",
                        "Kesit kalınlığı 3-5 mikrondur; parafin bloktan rotary mikrotomla kesilir",
                        "Hücre çekirdeği ve sitoplazma sınırlarını genel hatlarıyla gösterir",
                        "Glomerül bazal membranının iç lamina katmanlarını ayıramaz"
                    ],
                    [
                        "Elektron dalga boyu sayesinde 500.000x büyütme sağlar",
                        "Kesit kalınlığı 50-80 nanometredir; epoksi reçineden elmas bıçakla kesilir",
                        "Ribozom, lizozom, desmozom ve mikrotübül çiftlerini gösterir",
                        "Podosit ayak çıkıntısı füzyonunu ve subendotelyal birikimleri kanıtlar"
                    ]
                ),
                make_micro_quiz(
                    "Çocukluk çağında masif nefrotik sendrom (ağır proteinüri) ile başvuran bir hastanın böbrek biyopsisinde ışık mikroskobunda glomerüller tamamen normal izlenmiştir. Bu hastada kesin tanı koymak için hangi patoloji yöntemine başvurulmalıdır?",
                    {
                        "A": "Rutin Hematoksilen-Eozin boyasını tekrarlamak",
                        "B": "Transmisyon Elektron Mikroskobu (TEM) ile podosit ayak çıkıntılarını incelemek",
                        "C": "Rezeksiyon cerrahi sınırlarını çini mürekkebiyle boyamak",
                        "D": "Klinik otopsi için aile onayı istemek",
                        "E": "Dondurulmuş frozen kesit yapmak"
                    },
                    "B",
                    {
                        "A": "Işık mikroskobu podosit ayak çıkıntılarının nanometre düzeyindeki silinmesini gösteremez.",
                        "B": "Minimal Değişiklik Hastalığında podosit ayak füzyonu ancak TEM ile kesinleştirilir.",
                        "C": "Çini mürekkebi boyaması tümör cerrahisinde cerrahi sınır değerlendirmesi için kullanılır.",
                        "D": "Nefrotik sendromlu canlı hastada klinik otopsi endikasyonu bulunmaz.",
                        "E": "Frozen kesit kaba morfolojik inceleme sağlar, ultrastrüktürel detay veremez."
                    }
                ),
                make_cloze(
                    "Hücre içi organellerin ve glomerüler podosit ayak çıkıntılarının nanometre düzeyinde incelenmesini sağlayan yönteme elektron mikroskopisi adı verilir.",
                    "elektron mikroskopisi",
                    "Nanometre çözünürlüklü mikroskopik inceleme türü"
                )
            ]
        },

        # Adım 39: [TEKRAR SAYFASI - CHECKPOINT 4]
        {
            "slideNumber": 39,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Patolojinin Alt Dalları ve Disiplinlerarası Entegrasyon",
            "subtitle": "Bölüm 4'ün genel patoloji, cerrahi patoloji, otopsi, sitoloji, moleküler patoloji ve elektron mikroskopisi konularını toparlayan kritik sentez ve pekiştirme istasyonu.",
            "badge": "Checkpoint 4",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 4,
            "synthesisNarrative": """Patoloji; makroskobik diseksiyondan moleküler genetiğe uzanan ==geniş bir alt uzmanlık yelpazesine== sahiptir.

Genel patoloji hücresel zedelenme ve inflamasyonun evrensel yasalarını incelerken, özel patoloji bu süreçlerin organ sistemlerindeki yansımalarını ele alır. Cerrahi patoloji biyopsi ve rezeksiyonlarla yaşayan hastanın tedavi haritasını çizer. Klinik otopsi tanısal kaliteyi denetlerken, adli patoloji şüpheli ölümlerde yasal delil üretir. Sitopatoloji tek tek hücrelerden hızlı ön tanı sağlarken, moleküler patoloji hedefe yönelik ilaç seçimini belirler; elektron mikroskopisi ise podosit defektleri gibi nanometre düzeyindeki lezyonları aydınlatır.

> [BÖLÜM ÖZETİ] Doğru klinik yönetim; lezyonun niteliğine uygun patoloji alt dalının ve doğru doku örneğinin seçilmesiyle başlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Geniş Spektrum", "desc": "Makroskopi, histopatoloji, sitoloji, adli, moleküler ve ultrastrüktür bir bütündür.", "isKey": True},
                    {"title": "Doğru İstem Mantığı", "desc": "Hastalığın niteliğine uygun materyal ve patoloji alt dalı seçilmelidir.", "isKey": True},
                    {"title": "Kişiselleştirilmiş Entegrasyon", "desc": "Işık mikroskopisi günümüzde İHK, moleküler NGS ve FISH ile tamamlanır.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 4 Patoloji Alt Dalları Sentez Tablosu",
                    "headers": ["Patoloji Alt Dalı", "İncelenen Temel Materyal", "Klinik Tıptaki En Kritik Görevi"],
                    "rows": [
                        ["Genel Patoloji", "Hücre ve doku genel yanıtları", "Zedelenme, nekroz ve inflamasyonun evrensel yasalarını öğretmek"],
                        ["Cerrahi Patoloji", "Biyopsi ve rezeksiyon parçaları", "Kanser tanısı, histolojik grade, pTNM evreleme ve sınır kontrolü"],
                        ["Klinik Otopsi", "Hastanede vefat eden hasta cesedi", "Klinik tanı doğruluğunu denetlemek ve tıp eğitimini beslemek"],
                        ["Adli Patoloji", "Şüpheli ve adli ölüm vakaları", "Ölüm nedeni, mekanizması ve orijinini (cinayet/kaza) kanıtlamak"],
                        ["Sitopatoloji", "Vücut sıvıları, sürüntü ve İİAS", "Hızlı, ucuz, poliklinik şartlarında kanser taraması ve ön tanı"],
                        ["Moleküler Patoloji", "Tümör DNA ve RNA'sı", "Hedefe yönelik akıllı ilaç (tirozin kinaz inh. vb.) seçimi"],
                        ["Elektron Mikroskobu", "Glutaraldehitli ultra ince kesit", "Glomerülonefritlerde podosit ve bazal membran defektlerini çözmek"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Minimal Değişiklik Hastalığında podosit silinmesi yalnızca Elektron Mikroskobuyla saptanır.",
                "📌 [SINAV SPOTU] Adli otopside aile izni gerekmez, savcılık kararıyla zorunlu yürütülür; klinik otopside aile rızası şarttır.",
                "📌 [SINAV SPOTU] Kanser hastasında pTNM evresini cerrahi patolog belirler; EGFR ve KRAS mutasyonlarını moleküler patolog çözer."
            ],
            "medicalTerms": [
                {"term": "Entegre Patoloji", "explanation": "Morfolojik bulgular ile moleküler verilerin tek raporda birleştirilerek sunulmasıdır."},
                {"term": "Ölüm Nedeni vs Mekanizması", "explanation": "Ölüm nedeni primer etkeni, mekanizma ise ölüme yol açan fizyopatolojik bozukluğu belirtir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p4-1",
                    "Klinik otopsi ile Adli otopsi arasındaki karar verici makam ve rıza zorunluluğu farkı nedir?",
                    "Klinik otopsi hekimin önerisi ve ailenin yazılı rızasıyla yapılır. Adli otopsi ise şüpheli ölümlerde Cumhuriyet Savcılığı kararıyla aile izni aranmaksızın zorunlu olarak icra edilir.",
                    "Hukuki otorite ve aile rızası",
                    "Otopsi Patolojisi"
                ),
                make_flashcard(
                    "fc-p4-2",
                    "Moleküler patolojide KRAS mutasyon analizi kolorektal kanser tedavisinde neden hayati bir 'prediktif' testtir?",
                    "KRAS mutant kolon kanserlerinde EGFR yolağı sürekli aktif olduğundan, anti-EGFR monoklonal antikor tedavileri (Setuksimab) etkisizdir ve verilmemelidir.",
                    "Tedavi direnci öngörüsü",
                    "Moleküler Patoloji"
                ),
                make_flashcard(
                    "fc-p4-3",
                    "Transmisyon Elektron Mikroskobunun (TEM) nefropatolojide (böbrek biyopsisinde) ışık mikroskobuna karşı vazgeçilmez üstünlüğü nedir?",
                    "TEM nanometre çözünürlüğüyle podosit ayak çıkıntısı silinmesini (Minimal Değişiklik Hastalığı) ve bazal membran katmanlarındaki ince defektleri kesin olarak kanıtlar.",
                    "Podosit ayak silinmesi ve nanometre çözünürlük",
                    "Ultrastrüktürel Patoloji"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 4'te incelenen patolojinin alt dalları ve yöntemleri dikkate alındığında, aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                    {
                        "A": "Minimal Değişiklik Hastalığı tanısı → Transmisyon Elektron Mikroskopisi (TEM)",
                        "B": "Kolon kanserinde anti-EGFR tedavi yanıtı öngörüsü → KRAS Moleküler Mutasyon Analizi",
                        "C": "Şüpheli ateşli silah yaralanması ölümü → Aile izniyle Klinik Otopsi",
                        "D": "Tiroid nodülünde poliklinik şartlarında ilk hızlı değerlendirme → İnce İğne Aspirasyon Sitolojisi (İİAS)",
                        "E": "Meme karsinomunda mikroskobik cerrahi sınır tespiti → Cerrahi Patoloji İncelemesi"
                    },
                    "C",
                    {
                        "A": "TEM podosit ayak silinmelerini nanometre düzeyinde gösteren referans yöntemdir.",
                        "B": "KRAS mutasyon testi anti-EGFR ilaçlara direnci gösteren prediktif bir biyobelirteçtir.",
                        "C": "Ateşli silah yaralanması adli bir vaka olup savcılık kararıyla Adli Otopsi gerektirir.",
                        "D": "İİAS tiroid nodüllerinde poliklinik şartlarında uygulanan ilk minimal invaziv basamaktır.",
                        "E": "Cerrahi sınırlar rezeksiyon materyallerinde cerrahi patolog tarafından değerlendirilir."
                    }
                ),
                make_interactive_table(
                    "Patoloji Alt Dalları Vaka Eşleştirmesi",
                    ["Klinik Vaka", "İstenmesi Gereken İnceleme", "Temel Beklenti"],
                    [
                        [
                            ("Masif proteinürili çocuk", False),
                            ("Elektron Mikroskobu (TEM)", True, "Ultrastrüktürel podosit analizi"),
                            ("Podosit ayak silinmesi teyidi", False)
                        ],
                        [
                            ("Akciğer Adenokarsinomu", False),
                            ("EGFR / ALK Moleküler Testi", True, "Nükleik asit mutasyon tayini"),
                            ("Tirozin kinaz inhibitörü başlama", False)
                        ],
                        [
                            ("Servikal Tarama", False),
                            ("PAP Smear Eksfolyatif Sitoloji", True, "Dökülen epitel hücre analizi"),
                            ("Displazi ve preinvaziv lezyon tespiti", False)
                        ]
                    ]
                )
            ]
        }
    ]
