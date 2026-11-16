#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 2: Hipertrofi: Tanım, Moleküler Mekanizmalar ve Fizyolojik Örnekler (Adımlar 10 - 19)
Ders: Tıbbi Patoloji - Hücresel Adaptasyonlar
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
        # Adım 10
        {
            "slideNumber": 10,
            "title": "Hipertrofi Tanımı: Hücre Boyutunda Artış ve Organ Büyümesi",
            "subtitle": "Hipertrofi, hücre sayısında artış olmaksızın hücre hacminin büyümesiyle organın büyümesidir.",
            "badge": "Temel Tanım",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Hipertrofi**, hücre sayısında herhangi bir artış olmaksızın, hücre içi yapısal protein ve organellerin miktarının artması sonucu ==hücre boyutunun büyümesi== ve buna bağlı olarak organ kütlesinin artmasıdır.

Hücrenin büyümesi sıvı toplanmasına (hücresel ödem) bağlı bir şişme değildir; hücrenin aktif olarak ek sarkomer, miyofilament ve mitokondri sentezlemesiyle gerçekleşen gerçek bir yapısal büyümedir. Artan mekanik yük veya trofik uyarana karşı hücre fonksiyonel kapasitesini yükseltir.

> [TEMEL İLKE] Hipertrofide organı büyüten temel faktör hücre sayısı değil, tek tek her bir hücrenin hacimsel büyümesidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hacimsel Büyüme", "desc": "Hücre sayısı sabittir; hücre boyutunun artmasıyla doku kitlesi büyür.", "isKey": True},
                    {"title": "Aktif Sentez", "desc": "Ödemden farklı olarak yeni yapısal protein ve organellerin biyosentezi söz konusudur.", "isKey": True},
                    {"title": "Artmış Fonksiyon", "desc": "Büyüyen hücre daha fazla mekanik iş yapabilecek donanıma kavuşur.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofi ve Hücresel Şişme Karşılaştırması",
                    "headers": ["Parametre", "Hipertrofi", "Hücresel Şişme (Ödem)"],
                    "rows": [
                        ["Büyüme Nedeni", "Yapısal protein ve organel sentezi", "Sodyum ve suyun hücre içine girişi"],
                        ["İşlevsel Durum", "Artmış kasılma ve fonksiyon", "Bozulmuş metabolizma ve hasar"],
                        ["Süreç Niteliği", "Uyum sağlayan fizyolojik/patolojik adaptasyon", "Geri dönüşümlü erken hücre hasarı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofi hücre sayısında artış olmaksızın hücre boyutunun büyümesidir.",
                "📌 [SINAV SPOTU] Hipertrofi hücresel şişme (ödem) değildir; yapısal proteinlerin biyosentezine dayanır."
            ],
            "medicalTerms": [
                {"term": "Hipertrofi", "explanation": "Hücre içi yapısal protein artışıyla hücre hacminin büyümesidir."},
                {"term": "Miyofilament", "explanation": "Kasılmayı sağlayan aktin ve miyozin protein iplikçikleridir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Hipertrofi ile hücresel şişme (hidropik dejenerasyon) arasındaki temel biyolojik ayrım nedir?",
                    {
                        "A": "Hipertrofide hücre içine su girer, hücresel şişmede protein sentezlenir",
                        "B": "Hipertrofi yapısal protein sentezine dayanırken, şişme membran iyon pompası yetmezliğiyle su birikimidir",
                        "C": "Hücresel şişme bir adaptasyon türüdür, hipertrofi ise geri dönüşsüz ölümdür",
                        "D": "Hipertrofide hücre sayısı katlanarak artar",
                        "E": "Hipertrofi yalnızca ölü dokularda mikroskop altında izlenir"
                    },
                    "B",
                    {
                        "A": "Yanlış: Tam tersi geçerlidir; hipertrofi protein sentezidir.",
                        "B": "Doğru: Hipertrofi yapısal protein artışıdır; şişme ise su ve sodyum birikimidir.",
                        "C": "Yanlış: Şişme erken hasar belirtecidir, hipertrofi ise adaptasyondur.",
                        "D": "Yanlış: Sayı artışı hiperplazidir, hipertrofide sayı sabittir.",
                        "E": "Yanlış: Hipertrofi yaşayan organizmanın dinamik biyolojik sürecidir."
                    }
                ),
                make_cloze(
                    "Hücre içi yapısal protein ve organellerin sentezlenmesi sonucu hücre hacminin büyümesine [hipertrofi] adı verilir.",
                    "hipertrofi",
                    "Hücre boyut artışı terimi"
                )
            ]
        },

        # Adım 11
        {
            "slideNumber": 11,
            "title": "Hücresel Mekanizma: Yapısal Protein ve Organel Biyosentezi",
            "subtitle": "Hipertrofi sürecinde transkripsiyon faktörleri aktive edilerek kontraktil proteinlerin sentezi artırılır.",
            "badge": "Moleküler Mekanizma",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofi karmaşık bir biyokimyasal kaskadın ürünüdür. Hücre zarı üzerindeki mekanosensörler veya büyüme faktörü reseptörleri uyarıldığında, hücre içi sinyal iletim yolakları devreye girer.

Bu sinyaller çekirdekte transkripsiyon faktörlerini aktive ederek ==protein sentezini== tetikler. Hücrede ribozom sayısı, endoplazmik retikulum hacmi ve mitokondri kütlesi genişler. Kas dokusunda yeni sarkomerler üretilerek mevcut miyofibrillere paralel veya seri olarak eklenir.

> [TEMEL İLKE] Hipertrofik büyüme, DNA transkripsiyonu ve ribozomal translasyon hızının koordineli biçimde artırılmasıyla yürütülür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mekanik Algılama", "desc": "Hücre zarındaki integrinler ve gerilim sensörleri iş yükünü algılar.", "isKey": True},
                    {"title": "Gen Aktivasyonu", "desc": "Aktin, miyozin ve troponin gibi kontraktil protein genleri açılır.", "isKey": True},
                    {"title": "Organel Çoğalması", "desc": "Artan enerji ihtiyacını karşılamak için mitokondri ve ribozom sayısı artar.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofide Sentezlenen Hücresel Bileşenler",
                    "headers": ["Bileşen", "Biyolojik Fonksiyon", "Klinik Yansıma"],
                    "rows": [
                        ["Miyofibriller", "Kasılma gücünü artırma", "Organ duvarının kalınlaşması"],
                        ["Mitokondriler", "ATP üretimini karşılama", "Metabolik kapasitenin korunması"],
                        ["Sarkoplazmik Retikulum", "Kalsiyum depolama ve salma", "Uyarılma-kasılma kenetinin sürdürülmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofi mekanizmasında hücre içi sinyal yolakları aktive olarak yapısal protein sentezini uyarır.",
                "📌 [SINAV SPOTU] Kas hipertrofisinde yeni sarkomerlerin üretimi temel hücresel mekanizmadır."
            ],
            "medicalTerms": [
                {"term": "Sarkomer", "explanation": "Çizgili kas hücresinin iki Z çizgisi arasında kalan temel kasılma birimidir."},
                {"term": "Mekanosensör", "explanation": "Hücre zarında fiziksel gerilimi algılayarak kimyasal sinyale çeviren yapıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hipertrofi İndüksiyon Kaskadı",
                    [
                        "1. Mekanik Yük: Kas lifinde gerilim artışı ve integrin aktivasyonu.",
                        "2. Sinyal İletimi: Protein kinaz kaskadları ve kalsiyum akışının tetiklenmesi.",
                        "3. Transkripsiyon: GATA4 ve NFAT faktörleriyle hedef genlerin okunması.",
                        "4. Biyosentez: Ribozomlarda yeni aktin ve miyozin moleküllerinin üretimi.",
                        "5. Sarkomer Montajı: Yeni sarkomerlerin miyofibrillere eklenerek hücrenin kalınlaşması."
                    ]
                ),
                make_active_recall(
                    "Hipertrofi gelişen bir kas hücresinde mikroskopik olarak en belirgin organel artışı hangi yapılarda görülür?",
                    "Kasılmayı sağlayan miyofibrillerde (sarkomerler) ve enerji üreten mitokondrilerde artış izlenir."
                )
            ]
        },

        # Adım 12
        {
            "slideNumber": 12,
            "title": "Bölünemeyen (Kalıcı) Hücrelerde Saf Hipertrofi Prensibi",
            "subtitle": "Kardiyomiyositler ve iskelet kası lifleri mitoz yeteneğine sahip olmadığından yalnızca saf hipertrofi geliştirebilir.",
            "badge": "Hücre Biyolojisi",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """İnsan vücudunda kardiyak miyositler ve iskelet kası lifleri postmitotik, kalıcı (permanent) hücrelerdir. Bu hücreler doğum sonrası dönemde hücre döngüsünü geri dönüşsüz biçimde terk etmiştir.

Bu nedenle bölünme kapasiteleri son derece sınırlıdır. İskelet kası aşırı egzersize maruz kaldığında veya sol ventrikül hipertansiyona direndiğinde, dokuda hücre sayısını artırmak (hiperplazi) biyolojik olarak imkansızdır. Tek adaptasyon yolu, her bir hücrenin hacmini büyüterek ==saf hipertrofi== geliştirmektir.

> [TEMEL İLKE] Bölünme kapasitesi olmayan dokularda iş yükü artışına verilen tek adaptif yanıt saf hipertrofidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kalıcı Hücre Kısıtı", "desc": "Mitoz yeteneği yoktur; hücre sayısı doğumdan sonra çoğaltılamaz.", "isKey": True},
                    {"title": "Saf Hipertrofi", "desc": "Hiperplazi olmaksızın sadece hücre büyümesiyle gerçekleşir.", "isKey": True},
                    {"title": "Klinik Örnekler", "desc": "Vücut geliştirmede pazu kası, aort stenozunda sol ventrikül kası.", "isKey": False}
                ],
                "table": {
                    "title": "Kalıcı Dokuların Adaptif Yanıtı",
                    "headers": ["Doku Tipi", "Hücre Döngüsü Durumu", "Geçerli Adaptasyon Modeli"],
                    "rows": [
                        ["Kalp Kası", "G0 fazında kalıcı, bölünemez", "Saf Hipertrofi"],
                        ["İskelet Kası", "Çok çekirdekli lifler bölünemez", "Saf Hipertrofi (satellit hücre desteğiyle)"],
                        ["Nöronlar", "Santral sinir sistemi nöronları bölünemez", "Aksonal rejenerasyon veya atrofi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalp kası ve iskelet kasında yük artışına verilen tek yanıt saf hipertrofidir; hiperplazi gelişemez.",
                "🚨 [KRİTİK UYARI] Gebelik uterusu kalıcı doku değildir; düz kas hücreleri hem hipertrofi hem hiperplazi yapar."
            ],
            "medicalTerms": [
                {"term": "Saf Hipertrofi", "explanation": "Hücre sayısı hiç artmadan yalnızca hücre boyutunun büyümesiyle oluşan adaptasyondur."},
                {"term": "Postmitotik Hücre", "explanation": "Mitoz bölünme yeteneğini kalıcı olarak yitirmiş olgun hücredir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Bölünemeyen (Kalıcı) Doku ile Bölünebilen Doku Yanıtı",
                    "Kalıcı Doku (Kalp / İskelet Kası)",
                    "Bölünebilen Doku (Uterus / Karaciğer)",
                    [
                        "Hücre döngüsüne giremez",
                        "Sadece saf hipertrofi yapabilir",
                        "Hücre sayısı kesinlikle artmaz"
                    ],
                    [
                        "Hücre döngüsüne aktif girer",
                        "Hipertrofi ve hiperplazi birlikte",
                        "Hücre sayısı belirgin biçimde artar"
                    ]
                ),
                make_cloze(
                    "Kardiyak miyositler ve iskelet kası lifleri bölünme kapasitesinden yoksun oldukları için aşırı yüke yalnızca [saf hipertrofi] ile yanıt verir.",
                    "saf hipertrofi",
                    "Tek başına boyut artışı terimi"
                )
            ]
        },

        # Adım 13
        {
            "slideNumber": 13,
            "title": "Mekanik Gerilim Reseptörleri ve İntraselüler Sinyal İletimi",
            "subtitle": "Hücre zarındaki integrinler ve mekanik sensörler fiziksel yükü biyokimyasal sinyale çevirir.",
            "badge": "Sinyal İletimi",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofiyi başlatan en kritik tetikleyici ==mekanik gerilme (stretch)== uyarısıdır. Kas hücresi gerildiğinde, hücre zarı ile ekstrasellüler matriksi birbirine bağlayan **integrin reseptörleri** fiziksel deformasyonu hisseder.

Bu mekanik algılama, hücre içinde fokal adezyon kinaz (FAK) ve mitojenle aktive olan protein kinaz (MAPK) yolaklarını aktive eder. Fiziksel çekme kuvveti böylece saniyeler içinde kimyasal fosforilasyon kaskadına dönüştürülür.

> [TEMEL İLKE] Mekanik gerilme, büyüme faktörleri olmaksızın da tek başına hipertrofik gen programını başlatabilen güçlü bir tetikleyicidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "İntegrinler", "desc": "Mekanik stresi hisseden transmembran adezyon molekülleridir.", "isKey": True},
                    {"title": "Mekanotransdüksiyon", "desc": "Fiziksel gerilim kuvvetinin kimyasal sinyale çevrilmesi sürecidir.", "isKey": True},
                    {"title": "Kinaz Kaskadı", "desc": "MAPK ve Akt yolakları üzerinden çekirdeğe sinyal iletilir.", "isKey": False}
                ],
                "table": {
                    "title": "Mekanotransdüksiyonun Temel Bileşenleri",
                    "headers": ["Bileşen", "Biyolojik Konum", "İşlev"],
                    "rows": [
                        ["İntegrin Kompleksi", "Hücre zarı / Matriks arayüzü", "Fiziksel gerilimi algılama"],
                        ["Fokal Adezyon Kinaz", "Sitozolik zar yüzeyi", "Tirozin fosforilasyonu başlatma"],
                        ["MAP Kinazlar (ERK/p38)", "Sitoplazma / Nükleus", "Transkripsiyon faktörlerini fosforilleme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Mekanik gerilmenin kimyasal sinyale çevrilmesine mekanotransdüksiyon adı verilir.",
                "📌 [SINAV SPOTU] İntegrinler mekanik gerilimi algılayan temel transmembran sensörlerdir."
            ],
            "medicalTerms": [
                {"term": "Mekanotransdüksiyon", "explanation": "Mekanik kuvvetlerin hücre içinde biyokimyasal sinyallere dönüştürülmesidir."},
                {"term": "İntegrin", "explanation": "Hücre iskeletini hücre dışı matrikse bağlayan transmembran reseptör proteinidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Kas hücrelerinde fiziksel gerilmenin (mekanik yük) algılanıp hipertrofi sinyaline dönüştürülmesinde görev alan temel membran sensörü hangisidir?",
                    {
                        "A": "İntegrin reseptörleri",
                        "B": "Asetilkolin reseptörleri",
                        "C": "İnsülin reseptörleri",
                        "D": "GABA reseptörleri",
                        "E": "Glukagon reseptörleri"
                    },
                    "A",
                    {
                        "A": "Doğru: İntegrinler mekanik stresi algılayıp hücre içine ileten ana sensörlerdir.",
                        "B": "Yanlış: Asetilkolin nöromüsküler kavşakta elektriksel iletiyi sağlar.",
                        "C": "Yanlış: İnsülin reseptörleri glikoz metabolizmasını düzenler.",
                        "D": "Yanlış: GABA santral inhibitör nörotransmiter reseptörüdür.",
                        "E": "Yanlış: Glukagon glikojenolizi tetikler, mekanik sensör değildir."
                    }
                ),
                make_cloze(
                    "Hücre zarında fiziksel gerilimi algılayarak hücre içi sinyal kaskadını başlatan adezyon moleküllerine [integrin] adı verilir.",
                    "integrin",
                    "Hücre-matriks bağlayıcı reseptör"
                )
            ]
        },

        # Adım 14
        {
            "slideNumber": 14,
            "title": "Büyüme Faktörleri ve Vazoaktif Ajanlar: TGF-β, IGF-1, Endotelin-1",
            "subtitle": "Mekanik yükün yanı sıra humoral ajanlar ve büyüme faktörleri hipertrofiyi güçlü biçimde uyarır.",
            "badge": "Biyokimyasal Uyarım",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofi yalnızca mekanik çekmeyle değil, çözünür ligandlar ve büyüme faktörleriyle de tetiklenir. Bunlar arasında en önemlileri **IGF-1** (insülin benzeri büyüme faktörü-1), **TGF-β** (transforme edici büyüme faktörü-beta) ve **Endotelin-1** ile **Anjiyotensin II**'dir.

IGF-1 özellikle fizyolojik (egzersiz) hipertrofisinde PI3K/Akt yolağı üzerinden protein sentezini uyarır. Buna karşılık Anjiyotensin II ve Endotelin-1 patolojik kardiyak hipertrofide G-protein kenetli reseptörler üzerinden kalsiyum bağımlı sinyal yolaklarını ateşler.

> [TEMEL İLKE] Fizyolojik hipertrofi ağırlıklı olarak IGF-1 yolağını kullanırken; patolojik hipertrofi anjiyotensin, endotelin ve adrenerjik sinyallerle yönlendirilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "IGF-1 / Akt Yolağı", "desc": "Fizyolojik hipertrofide protein sentezini artıran temel büyüme faktörüdür.", "isKey": True},
                    {"title": "Vazoaktif Peptitler", "desc": "Endotelin-1 ve Anjiyotensin II patolojik hipertrofiyi tetikler.", "isKey": True},
                    {"title": "TGF-β Rolü", "desc": "Protein sentezinin yanı sıra interstisyel fibrozisi de stimüle eder.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofiyi Uyaran Biyokimyasal Faktörler",
                    "headers": ["Mediyatör", "Reseptör Tipi", "Baskın Hipertrofi Türü"],
                    "rows": [
                        ["IGF-1", "Tirozin kinaz reseptörü", "Fizyolojik hipertrofi (egzersiz)"],
                        ["Anjiyotensin II", "G-protein kenetli reseptör (AT1)", "Patolojik kardiyak hipertrofi"],
                        ["Endotelin-1", "G-protein kenetli reseptör (ETA)", "Patolojik vasküler ve kardiyak hipertrofi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] IGF-1 fizyolojik hipertrofinin, Anjiyotensin II ve Endotelin-1 patolojik hipertrofinin anahtar mediyatörleridir.",
                "📌 [SINAV SPOTU] Anjiyotensin II reseptör blokerleri (ARB) hipertansif hipertrofiyi geriletmede bu nedenle kullanılır."
            ],
            "medicalTerms": [
                {"term": "IGF-1", "explanation": "Hücre büyümesini ve protein sentezini uyaran insülin benzeri büyüme faktörüdür."},
                {"term": "Vazoaktif Ajan", "explanation": "Damar tonusunu değiştiren ve hücresel büyüme sinyali veren kimyasal maddedir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Hipertrofi Tetikleyicileri ve Etki Mekanizmaları",
                    ["Tetikleyici Faktör", "Etki Mekanizması", "Baskın Klinik Durum"],
                    [
                        [
                            ("IGF-1 uyarımı", False),
                            ("PI3K / Akt yolağı aktivasyonu", True, "Hücresel anabolizma"),
                            ("Sporcu kalbi ve egzersiz hipertrofisi", False)
                        ],
                        [
                            ("Anjiyotensin II uyarımı", False),
                            ("Gq kenetli kalsiyum kaskadı", True, "Patolojik vazokonstrüktör"),
                            ("Hipertansif kalp hastalığı", False)
                        ],
                        [
                            ("Mekanik gerilme", False),
                            ("İntegrin aracılı fokal adezyon sinyali", True, "Fiziksel yük algısı"),
                            ("Aort darlığına bağlı sol ventrikül yükü", False)
                        ]
                    ]
                ),
                make_active_recall(
                    "Fizyolojik sporcu hipertrofisi ile patolojik hipertansif hipertrofi arasındaki biyokimyasal sinyal farkı nedir?",
                    "Fizyolojik hipertrofi temel olarak IGF-1 ve PI3K/Akt yolağını kullanır; patolojik hipertrofi ise Anjiyotensin II, Endotelin-1 ve G-protein yolaklarıyla tetiklenir."
                )
            ]
        },

        # Adım 15
        {
            "slideNumber": 15,
            "title": "Transkripsiyonel Aktivasyon: GATA4, NFAT ve MEF2 Yolakları",
            "subtitle": "Sitoplazmik sinyaller çekirdeğe ulaşarak özgül hipertrofi transkripsiyon faktörlerini aktive eder.",
            "badge": "Genetik Regülasyon",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofik sinyaller çekirdeğe ulaştığında üç ana transkripsiyon faktörü ailesini aktive eder: **GATA4**, **NFAT** (aktive T hücreleri nükleer faktörü) ve **MEF2** (miyosit güçlendirici faktör-2).

Özellikle kalsiyum-kalmodülin bağımlı bir fosfataz olan **kalsinörin**, NFAT'ı defosforille ederek çekirdeğe girmesini sağlar. Çekirdeğe geçen NFAT, GATA4 ile birleşerek kasılma proteinlerinin ve fetal kardiyak genlerin okunmasını başlatır.

> [TEMEL İLKE] Kalsinörin-NFAT yolağı patolojik kardiyak hipertrofinin en kritik moleküler kontrol anahtarıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kalsinörin / NFAT", "desc": "Kalsiyum bağımlı fosfataz kalsinörin NFAT'ı aktive ederek nükleusa gönderir.", "isKey": True},
                    {"title": "GATA4 ve MEF2", "desc": "Kontraktil protein genlerinin promotörlerine bağlanan transkripsiyon faktörleridir.", "isKey": True},
                    {"title": "Fetal Gen İndüksiyonu", "desc": "Erişkin kalpte normalde kapalı olan fetal izoform genleri yeniden açılır.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofi Transkripsiyon Faktörleri",
                    "headers": ["Transkripsiyon Faktörü", "Aktivasyon Mekanizması", "Hedef Genler"],
                    "rows": [
                        ["NFAT", "Kalsinörin aracılı defosforilasyon", "BNP, fetal kardiyak proteinler"],
                        ["GATA4", "MAPK fosforilasyonu", "Alfa-aktin, troponin genleri"],
                        ["MEF2", "Kalsiyum/kalmodülin kinaz (CaMK)", "Sarkomerik yapı proteinleri"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalsinörin, NFAT transkripsiyon faktörünü aktive ederek kardiyak hipertrofiyi başlatan enzimdir.",
                "📌 [SINAV SPOTU] GATA4, NFAT ve MEF2 kardiyak hipertrofinin ana transkripsiyonel düzenleyicileridir."
            ],
            "medicalTerms": [
                {"term": "Kalsinörin", "explanation": "Hücre içi kalsiyum artışıyla aktifleşen ve NFAT'ı nükleusa yönlendiren fosfatazdır."},
                {"term": "Transkripsiyon Faktörü", "explanation": "DNA'ya bağlanarak özgül genlerin mRNA'ya yazılmasını kontrol eden proteindir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kalsinörin-NFAT Yolağı ve Gen Aktivasyonu",
                    [
                        "1. Kalsiyum Girişi: Hücre içi serbest kalsiyum konsantrasyonunun yükselmesi.",
                        "2. Kalsinörin Aktivasyonu: Kalsiyum-kalmodülin kompleksinin fosfatazı uyarması.",
                        "3. NFAT Defosforilasyonu: Sitoplazmik NFAT'ın nükleer lokalizasyon sinyalinin açılması.",
                        "4. Nükleusa Geçiş: NFAT'ın nükleer porlardan çekirdeğe translokasyonu.",
                        "5. Promotör Bağlanması: GATA4 ile birlikte kontraktil genlerin transkripsiyonunu başlatması."
                    ]
                ),
                make_cloze(
                    "Kalsiyum bağımlı bir fosfataz olan [kalsinörin] NFAT faktörünü aktive ederek nükleusa geçişini sağlar.",
                    "kalsinörin",
                    "Hipertrofiyi başlatan fosfataz enzimi"
                )
            ]
        },

        # Adım 16
        {
            "slideNumber": 16,
            "title": "İskelet Kasında Fizyolojik Hipertrofi: Egzersiz ve Yük Artışı",
            "subtitle": "Ağırlık antrenmanı ve direnç egzersizleri iskelet kası liflerinde saf fizyolojik hipertrofi oluşturur.",
            "badge": "Fizyolojik Örnek",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """İskelet kasının iş yükü artışına verdiği yanıt fizyolojik hipertrofinin en somut örneğidir. Ağır direnç antrenmanı yapan sporcularda kas lifleri yoğun mekanik yüke maruz kalır.

Kas hücreleri bölünemediği için, her bir kas lifi paralel olarak yeni miyofibriller sentezler. Kas liflerinin çapı genişler, glikojen depoları zenginleşir ve kas kütlesi belirgin biçimde artar. Bu süreçte eşlik eden bir fibrozis veya hücre ölümü yoktur.

> [TEMEL İLKE] Egzersize bağlı iskelet kası hipertrofisi patolojik fibrozis içermeyen, tamamen geri dönüşümlü sağlıklı bir adaptasyondur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Direnç Yükü", "desc": "Mekanik gerilim kas liflerinde aktin ve miyozin sentezini hızlandırır.", "isKey": True},
                    {"title": "Lif Çapı Artışı", "desc": "Lif sayısı sabit kalırken liflerin kalınlığı ve kasılma gücü katlanır.", "isKey": True},
                    {"title": "Tam Reversibilite", "desc": "Egzersiz bırakıldığında kullanılmama nedeniyle lifler normal çapına geri döner.", "isKey": False}
                ],
                "table": {
                    "title": "İskelet Kası Hipertrofisi Özellikleri",
                    "headers": ["Özellik", "Fizyolojik İskelet Kası Hipertrofisi", "Patolojik Durum"],
                    "rows": [
                        ["Tetikleyici", "Dirençli egzersiz, ağırlık çalışması", "Kas distrofileri (yalancı hipertrofi)"],
                        ["Doku Mimarisi", "Düzenli, paralel kalınlaşmış lifler", "Düzensiz lifler ve yağ/bağ dokusu birikimi"],
                        ["İnterstisyel Doku", "Normal damarlanma, fibrozis yok", "İlerleyici fibrozis ve skar dokusu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Ağırlık çalışan sporcunun kol kaslarındaki büyüme fizyolojik saf hipertrofi örneğidir.",
                "📌 [SINAV SPOTU] Egzersiz bırakıldığında kas liflerinin eski boyutuna dönmesi adaptasyonun geri dönüşümlülüğünü kanıtlar."
            ],
            "medicalTerms": [
                {"term": "Direnç Egzersizi", "explanation": "Kasın dış dirence karşı kasılarak miyofibril sentezini uyaran egzersizdir."},
                {"term": "Satellit Hücre", "explanation": "İskelet kası bazal laminasında bulunan ve tamirde nükleus sağlayan kök hücredir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Yoğun ağırlık antrenmanı yapan bir haltercinin pazu (biceps) kasındaki kütle artışının temel histopatolojik mekanizması nedir?",
                    {
                        "A": "Mevcut kas liflerinde yapısal miyofilament senteziyle hücre boyutunun artması (hipertrofi)",
                        "B": "Miyoblastların kontrolsüz mitoz bölünmesiyle lif sayısının artması (hiperplazi)",
                        "C": "Kas liflerinin yağ dokusuna dönüşmesi (metaplazi)",
                        "D": "Kas liflerinde hücre içi kalsiyum çökmesi (distrofik kalsifikasyon)",
                        "E": "Lifler arasında kronik granülomatöz inflamasyon gelişmesi"
                    },
                    "A",
                    {
                        "A": "Doğru: İskelet kasında büyüme lif sayısının değil lif çapının artmasıyla (hipertrofi) olur.",
                        "B": "Yanlış: İskelet kası lifleri bölünemez; hiperplazi yapamaz.",
                        "C": "Yanlış: Metaplazi değil fizyolojik hacim artışıdır.",
                        "D": "Yanlış: Kalsifikasyon patolojik doku kireçlenmesidir.",
                        "E": "Yanlış: Egzersiz hipertrofisinde inflamasyon yoktur."
                    }
                ),
                make_cloze(
                    "Düzenli ağırlık çalışan bir sporcunun iskelet kasında lif sayısı değişmez; kas liflerinin [çapı] genişler.",
                    "çapı",
                    "Hücre enine boyutsal büyümesi"
                )
            ]
        },

        # Adım 17
        {
            "slideNumber": 17,
            "title": "Gebelik Uterusunda Hipertrofi: Östrojen Uyarımı ve Düz Kas Büyümesi",
            "subtitle": "Gebelikte uterusun devasa büyümesi fizyolojik hormonal adaptasyonun klasik modelidir.",
            "badge": "Hormonal Adaptasyon",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Fizyolojik hipertrofinin en çarpıcı örneği gebelik sırasında **uterus miyometriyumunda** gözlenir. Gebe olmayan bir kadında yaklaşık 50-70 gram ağırlığında ve armut büyüklüğünde olan uterus, term gebelikte 1000-1100 grama ve devasa bir hacme ulaşır.

Bu muazzam büyümenin ana itici gücü plasenta ve over kaynaklı **östrojen hormonudur**. Östrojen, nükleer östrojen reseptörlerine bağlanarak düz kas hücrelerinde protein sentezini uyarır. Düz kas hücreleri uzar, kalınlaşır ve hipertrofiye uğrar.

> [TEMEL İLKE] Gebelikte uterus düz kas hücreleri normal boyutlarının 10 katına kadar uzayarak fetüsü taşıyacak güce ulaşır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hormonal Tetik", "desc": "Östrojen hormonu miyometriyum düz kas hücrelerini doğrudan uyarır.", "isKey": True},
                    {"title": "Boyut Artışı", "desc": "İğsi küçük hücreler dev, şişkin hipertrofik kas hücrelerine dönüşür.", "isKey": True},
                    {"title": "Kütle Artışı", "desc": "Uterus kütlesi yaklaşık 15-20 kat artarak 1 kilogramı aşar.", "isKey": False}
                ],
                "table": {
                    "title": "Gebe ve Gebe Olmayan Uterus Karşılaştırması",
                    "headers": ["Parametre", "Gebe Olmayan Uterus", "Term Gebe Uterus"],
                    "rows": [
                        ["Organ Ağırlığı", "50 - 70 gram", "1000 - 1100 gram"],
                        ["Miyosit Morfolojisi", "Küçük, iğsi, dar sitoplazmalı", "Büyük, uzamış, bol eozinofilik sitoplazmalı"],
                        ["Hormonal Durum", "Siklik bazal östrojen/progesteron", "Yüksek düzeyde sürekli östrojen"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gebelik uterusu fizyolojik hormonal hipertrofinin vücuttaki en belirgin örneğidir.",
                "📌 [SINAV SPOTU] Miyometriyumdaki büyüme doğumdan sonra hormonların çekilmesiyle tamamen geriler (involüsyon)."
            ],
            "medicalTerms": [
                {"term": "Miyometriyum", "explanation": "Uterusun düz kas liflerinden oluşan orta kalın kas tabakasıdır."},
                {"term": "İnvolüsyon", "explanation": "Gebelikte büyüyen uterusun doğum sonrasında küçülerek normal boyutuna dönmesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Gebe Olmayan vs Gebe Uterus Düz Kas Morfolojisi",
                    "Gebe Olmayan Miyometriyum",
                    "Gebe Miyometriyum",
                    [
                        "Organ ağırlığı 50-70 gram",
                        "Küçük, iğsi düz kas hücreleri",
                        "Dar sitoplazma ve küçük nükleus"
                    ],
                    [
                        "Organ ağırlığı 1000-1100 gram",
                        "Devasa uzamış hipertrofik miyositler",
                        "Geniş bol sitoplazma ve iri nükleus"
                    ]
                ),
                make_cloze(
                    "Gebelikte uterus miyometriyumunun devasa büyümesini tetikleyen temel hormonal uyaran [östrojen] hormonudur.",
                    "östrojen",
                    "Temel kadın steroid hormonu"
                )
            ]
        },

        # Adım 18
        {
            "slideNumber": 18,
            "title": "Gebelik Uterusunda Hipertrofi ve Hiperplazi Birlikteliği",
            "subtitle": "Düz kas hücreleri bölünebilme yeteneğine sahip olduğundan miyometriyumda hipertrofi ve hiperplazi bir arada yürür.",
            "badge": "Kombine Yanıt",
            "badgeColor": "emerald",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Kalp kasının aksine, uterusun düz kas hücreleri hücre döngüsüne girme yeteneğini koruyan stabil hücrelerdir. Bu biyolojik özellik nedeniyle gebelik uterusundaki büyüme **saf hipertrofi değildir**.

Gebelikte miyometriyumda hem hücre boyutunda muazzam bir artış (**hipertrofi**) hem de kök hücrelerden ve var olan düz kaslardan yeni hücrelerin türemesiyle hücre sayısında artış (**hiperplazi**) birlikte gerçekleşir. Ancak organın dev kütle artışına en büyük katkı hipertrofiden gelir.

> [TEMEL İLKE] Düz kas dokusu bölünebildiği için östrojen uyarımına hem hipertrofi hem de hiperplazi ile yanıt verir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kombine Adaptasyon", "desc": "Hipertrofi ve hiperplazinin eşzamanlı olarak birlikte gerçekleşmesidir.", "isKey": True},
                    {"title": "Düz Kas Özelliği", "desc": "Çizgili kasın aksine düz kas hücreleri mitoz yapabilme kapasitesine sahiptir.", "isKey": True},
                    {"title": "Baskın Bileşen", "desc": "Kütle artışının hacimsel olarak en büyük kısmı hücresel hipertrofiye aittir.", "isKey": False}
                ],
                "table": {
                    "title": "Uterus ve Kalp Adaptasyonunun Karşılaştırması",
                    "headers": ["Özellik", "Gebelik Uterusu", "Hipertansif Sol Ventrikül"],
                    "rows": [
                        ["Kas Tipi", "Düz kas (bölünebilir)", "Çizgili kalp kası (bölünemez)"],
                        ["Adaptasyon Şekli", "Hipertrofi + Hiperplazi", "Yalnızca Saf Hipertrofi"],
                        ["Uyaran Niteliği", "Fizyolojik östrojen hormonu", "Patolojik mekanik basınç yükü"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gebelik uterusunda hem hipertrofi hem de hiperplazi birlikte görülür.",
                "🚨 [KRİTİK UYARI] Kalp kası kalıcı olduğu için yalnız hipertrofi yaparken, uterus düz kası bölünebildiğinden hiperplazi de yapar."
            ],
            "medicalTerms": [
                {"term": "Kombine Adaptasyon", "explanation": "Bir organda hipertrofi ve hiperplazinin eşzamanlı olarak birlikte görülmesidir."},
                {"term": "Düz Kas Mitozu", "explanation": "Düz kas hücrelerinin hormon veya büyüme faktörleriyle bölünerek çoğalmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Gebelik sırasında büyüyen uterus miyometriyumu ile hipertansiyonda kalınlaşan sol ventrikül miyokardı karşılaştırıldığında en temel fark nedir?",
                    {
                        "A": "Miyokardda hem hipertrofi hem hiperplazi varken, uterusta sadece hipertrofi vardır",
                        "B": "Uterusta hem hipertrofi hem hiperplazi birlikte görülürken, miyokardda hücre bölünemediği için sadece saf hipertrofi görülür",
                        "C": "Her iki organda da yalnızca hiperplazi görülür",
                        "D": "Uterustaki büyüme geri dönüşsüzdür, miyokarddaki büyüme geri dönüşümlüdür",
                        "E": "Miyokard düz kas yapısındadır, uterus çizgili kas yapısındadır"
                    },
                    "B",
                    {
                        "A": "Yanlış: Miyokard bölünemez, hiperplazi yapamaz.",
                        "B": "Doğru: Uterus düz kası bölünebildiğinden hipertrofi+hiperplazi yapar; kalp kası sadece hipertrofi yapar.",
                        "C": "Yanlış: Her iki organda da baskın olan boyut artışıdır (hipertrofi).",
                        "D": "Yanlış: Uterus doğumdan sonra involüsyonla tamamen geri döner.",
                        "E": "Yanlış: Kalp çizgili kastır, uterus düz kastır."
                    }
                ),
                make_cloze(
                    "Gebelik uterusundaki düz kas hücreleri bölünebilme yeteneğine sahip olduğundan bu organda hipertrofi ile birlikte [hiperplazi] de gerçekleşir.",
                    "hiperplazi",
                    "Hücre çoğalması süreci"
                )
            ]
        },

        # Adım 19 (CHECKPOINT 2)
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Hipertrofinin Temelleri ve Fizyolojik Örnekler",
            "subtitle": "Hipertrofi mekanizmasını, sinyal iletim yolaklarını ve fizyolojik adaptasyon modellerini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 2,
            "synthesisNarrative": """Bu bölümde hipertrofinin hücresel ve moleküler mekanizmalarını, mekanik algılamayı ve fizyolojik örneklerini inceledik.

Hipertrofi hücre sayısı artmadan yapısal proteinlerin sentezlenmesiyle hücre boyutunun büyümesidir. Kalp kası ve iskelet kası gibi bölünemeyen kalıcı dokularda tek adaptasyon şeklidir. Mekanik gerilme integrinlerle algılanırken, humoral uyaranlar (IGF-1) protein sentezini uyarır. İskelet kası egzersizle saf hipertrofiye uğrarken, gebelik uterusu düz kas niteliği sayesinde hipertrofi ve hiperplaziyi bir arada yürütür.

> [TEKRAR SPOTU] Kalıcı dokularda saf hipertrofi, bölünebilen düz kas dokusunda kombine hipertrofi ve hiperplazi görülür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Boyut Artışı", "desc": "Hücre sayısı değişmez; organel ve miyofilament biyosentezi esastır.", "isKey": True},
                    {"title": "Sinyal Kaskadı", "desc": "İntegrinler mekanik gerilimi, kalsinörin-NFAT yolağı gen aktivasyonunu yönetir.", "isKey": True},
                    {"title": "Klinik Örnekler", "desc": "Sporcu pazı kası saf hipertrofiye, gebelik uterusu kombine adaptasyona örnektir.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 2 Sentez Tablosu",
                    "headers": ["Doku", "Adaptasyon Tipi", "Temel Uyaran"],
                    "rows": [
                        ["İskelet Kası", "Saf Hipertrofi", "Egzersiz ve mekanik yük"],
                        ["Gebelik Uterusu", "Hipertrofi + Hiperplazi", "Östrojen hormonu"],
                        ["Miyokard", "Saf Hipertrofi", "Hemodinamik basınç ve vazoaktif peptitler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofi hücre içi yapısal protein ve organel artışıyla hücre boyutunun büyümesidir.",
                "📌 [SINAV SPOTU] Gebelik uterusu östrojenle hem hipertrofiye hem hiperplaziye uğrar."
            ],
            "medicalTerms": [
                {"term": "Saf Hipertrofi", "explanation": "Hücre sayısı değişmeksizin yalnızca hücre boyutunun büyümesidir."},
                {"term": "Mekanotransdüksiyon", "explanation": "Fiziksel gerilim kuvvetinin hücre içi kimyasal sinyallere dönüştürülmesidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc04",
                    "Hipertrofi ile hücresel şişme (ödem) arasındaki temel fark nedir?",
                    "Hipertrofi yeni yapısal protein ve organel sentezine dayanan gerçek büyümedir; hücresel şişme ise bozulmuş iyon dengesi sonucu hücre içine su girmesidir."
                ),
                make_flashcard(
                    "k1-03-fc05",
                    "Gebelik miyometriyumu ile kalp miyokardı aşırı yüke yanıt açısından nasıl farklılaşır?",
                    "Uterus düz kası bölünebildiği için hipertrofi ve hiperplaziyi birlikte kullanır; kalp kası bölünemediği için yalnızca saf hipertrofi geliştirir."
                ),
                make_flashcard(
                    "k1-03-fc06",
                    "Hipertrofide mekanik gerilimi algılayan ve kalsiyum bağımlı gen aktivasyonunu yöneten temel moleküller nelerdir?",
                    "Mekanik gerilimi integrinler algılar; hücre içi sinyali kalsinörin-NFAT ve GATA4 transkripsiyon kaskadı yürütür."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Ağırlık antrenmanı yapan bir haltercide kas liflerinin büyümesi ile gebelikte uterusun büyümesi arasındaki hücresel fark nedir?",
                    "Haltercide çizgili kas bölünemediği için saf hipertrofi (yalnızca lif çapı artışı) olur; gebelikte ise düz kas bölünebildiğinden hipertrofi ve hiperplazi birlikte gerçekleşir."
                )
            ]
        }
    ]
