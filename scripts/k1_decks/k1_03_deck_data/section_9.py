#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 9: Mezenkimal Metaplazi, Malignite Riski ve Otofaji Yolağı (Adımlar 80 - 89)
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
        # Adım 80
        {
            "slideNumber": 80,
            "title": "Mezenkimal (Bağ Dokusu) Metaplazisi: Yumuşak Dokuda Kemik Oluşumu",
            "subtitle": "Metaplazi yalnızca epitelde değil; fibroblast ve mezenkimal kök hücrelerin osteoblasta dönüşümüyle bağ dokusunda da görülür.",
            "badge": "Mezenkimal Adaptasyon",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Metaplazi sadece epitel dokulara özgü bir süreç değildir; bağ dokusu ve mezenkimal hücreler de metaplazi geliştirebilir. Buna **mezenkimal (bağ dokusu) metaplazisi** denir.

En klasik örneği, normalde kemik bulunmayan yumuşak dokularda, arter duvarlarında, kronik skar alanlarında veya travmaya uğramış kas içinde kemik (osseöz metaplazi) veya kıkırdak (kondroid metaplazi) dokusunun belirmesidir. Buradaki mekanizma, multipotent mezenkimal kök hücrelerin BMP (kemik morfogenetik proteini) sinyaliyle osteoblastik yönde farklılaşmasıdır.

> [TEMEL İLKE] Mezenkimal metaplazi koruyucu bir uyumdan ziyade doku hasarına verilen reaktif ve anormal bir farklılaşma yanıtıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kemik / Kıkırdak Oluşumu", "desc": "Fibroblast ve mezenkimal kök hücreler osteoblast veya kondroblasta dönüşür.", "isKey": True},
                    {"title": "Heterotopik Doku", "desc": "Kemik dokusunun normalde bulunmadığı anatomik lokalizasyonda gelişmesidir.", "isKey": True},
                    {"title": "Tetikleyici Faktörler", "desc": "Lokal travma, kalsifikasyon odakları, kronik inflamasyon ve BMP salınımı.", "isKey": False}
                ],
                "table": {
                    "title": "Mezenkimal Metaplazi Örnekleri",
                    "headers": ["Lokalizasyon", "Orijinal Doku", "Metaplastik Yeni Doku"],
                    "rows": [
                        ["İskelet Kası (Travma)", "Çizgili kas ve interstisyel bağ dokusu", "Lameller kemik (Miyozitis ossifikans)"],
                        ["Aterom Plakları", "Fibröz damar intaması", "Kalsifiye osseöz kemik trabekülleri"],
                        ["Eski Cerrahi Skarlar", "Kollajenöz fibröz doku", "Kondroid kıkırdak veya kemik adacıkları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yumuşak dokuda travma veya skar alanında kemik oluşumu mezenkimal (osseöz) metaplazidir.",
                "📌 [SINAV SPOTU] BMP (Kemik Morfogenetik Proteini) mezenkimal kök hücreleri osteoblastik metaplaziye yönlendirir."
            ],
            "medicalTerms": [
                {"term": "Mezenkimal Metaplazi", "explanation": "Bağ dokusu kök hücrelerinin kemik, kıkırdak veya yağ hücresi yönünde farklılaşmasıdır."},
                {"term": "Heterotopik Kemikleşme", "explanation": "Normalde iskelet sistemi dışındaki yumuşak dokularda kemik dokusu gelişmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Uyluk kasına ağır darbe alan bir futbolcunun birkaç ay sonra uyluk kası içinde radyolojik ve histopatolojik olarak olgun kemik dokusu saptanması hangi süreçtir?",
                    {
                        "A": "Miyozitis ossifikans (Mezenkimal / Osseöz metaplazi)",
                        "B": "Osteosarkom (Primer kemik kanseri)",
                        "C": "Kazeifiye granülom",
                        "D": "Kompanse hipertrofi",
                        "E": "Disuse atrofisi"
                    },
                    "A",
                    {
                        "A": "Doğru: Kas içi travma sonrası mezenkimal hücrelerin kemiğe dönüşümü miyozitis ossifikanstır (osseöz metaplazi).",
                        "B": "Yanlış: Malign kemik tümörü değildir, travmaya reaktif benign metaplazidir.",
                        "C": "Yanlış: Enfeksiyöz tüberküloz granülomu değildir.",
                        "D": "Yanlış: Kas boyut artışı değildir.",
                        "E": "Yanlış: Atrofi değil yeni doku oluşumudur."
                    }
                ),
                make_cloze(
                    "Yumuşak dokularda ve kas içi travma alanlarında mezenkimal kök hücrelerin kemik dokusuna dönüşmesine [osseöz] metaplazi denir.",
                    "osseöz",
                    "Kemikleşme metaplazisi sıfatı"
                )
            ]
        },

        # Adım 81
        {
            "slideNumber": 81,
            "title": "Miyozitis Ossifikans: Kas İçi Travma Sonrası Heterotopik Kemikleşme",
            "subtitle": "Kas içi hematom ve travma sonrası mezenkimal hücrelerin osteoblastlara dönüşmesiyle kas içinde kemik kitlesi oluşur.",
            "badge": "Klinik Patoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Mezenkimal metaplazinin en klasik klinik tablosu **miyozitis ossifikanstır**. Genellikle genç atletlerde uyluk (kuadriseps) veya kol (brakialis) kasına gelen künt travma ve kas içi hematom sonrası gelişir.

Hematomun iyileşmesi sırasında dokudaki fibroblastlar ve mezenkimal kök hücreler osteojenik sinyaller alır. Lezyonun merkezinde fibroblastik proliferasyon sürerken, periferinde **olgun lameller kemik trabekülleri** şekillenir. Bu zonal mimari radyolojide ve patolojide osteosarkomdan (kanserden) ayıran en kritik bulgudur.

> [KLİNİK İPUCU] Miyozitis ossifikansın periferinde olgun kemik, merkezinde hücresel fibroblastik zon bulunur; bu zonal organizasyon malign kemik tümörünü dışlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Zonal Organizasyon", "desc": "Dışta olgun kemik trabekülleri, içte genç fibroblastik alanlar karakteristiktir.", "isKey": True},
                    {"title": "Osteosarkom Taklidi", "desc": "Radyolojide agresif görünebilir ancak benign bir reaktif metaplazidir.", "isKey": True},
                    {"title": "Travma Öyküsü", "desc": "Olguların büyük kısmında kas içi kanama ve hematom öyküsü mevcuttur.", "isKey": False}
                ],
                "table": {
                    "title": "Miyozitis Ossifikans vs Osteosarkom",
                    "headers": ["Özellik", "Miyozitis Ossifikans (Metaplazi)", "Osteosarkom (Kanser)"],
                    "rows": [
                        ["Zonal Mimari", "Dışta olgun kemik, içte hücresel merkez", "Düzensiz, kural tanımaz anaplastik büyüme"],
                        ["Hücresel Atipi", "Atipi yok, düzenli osteoblastlar", "Belirgin pleomorfizm, atipik mitozlar"],
                        ["Klinik Davranış", "Zamanla maturasyon ve sınırlanma", "İlerleyici kemik yıkımı ve metastaz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyozitis ossifikans kas içi travma sonrası heterotopik kemikleşmeyle giden mezenkimal metaplazidir.",
                "📌 [SINAV SPOTU] Dışta olgun kemik, içte fibroblastik doku zonal mimarisi miyozitis ossifikansı osteosarkomdan ayırt eder."
            ],
            "medicalTerms": [
                {"term": "Miyozitis Ossifikans", "explanation": "İskelet kası içinde travma veya inflamasyon sonrası heterotopik kemik oluşumudur."},
                {"term": "Zonal Mimari", "explanation": "Lezyonun merkezden perifere doğru düzenli olgunlaşma katmanları göstermesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Miyozitis Ossifikans ile Osteosarkom Ayrımı",
                    "Miyozitis Ossifikans (Benign Metaplazi)",
                    "Osteosarkom (Malign Neoplazi)",
                    [
                        "Dış kenarlarda olgun lameller kemik",
                        "Sitotolojik atipi ve anormal mitoz yok",
                        "Lezyon zamanla matürleşip durur"
                    ],
                    [
                        "Düzensiz dantelsi malign osteoid",
                        "Belirgin nükleer atipi ve tümör dev hücreleri",
                        "Durdurulamaz kemik yıkımı ve akciğer metastazı"
                    ]
                ),
                make_cloze(
                    "Kas içi travma sonrası heterotopik kemikleşmeyle karakterize mezenkimal metaplazi tablosuna [miyozitis ossifikans] denir.",
                    "miyozitis ossifikans",
                    "Kas içi kemikleşme lezyonu adı"
                )
            ]
        },

        # Adım 82
        {
            "slideNumber": 82,
            "title": "Metaplazi: Çift Uçlu Kılıç (Dayanıklılık Artışı vs Fonksiyon Kaybı)",
            "subtitle": "Metaplazi dokuyu fiziksel tahrişten korur; ancak orijinal organ fonksiyonlarının kaybı ve malignite riski yaratır.",
            "badge": "Biyolojik Bilanço",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojide metaplazi tam anlamıyla bir **çift uçlu kılıçtır (double-edged sword)**. Bir taraftan dokuyu o anki öldürücü stresten kurtarır: Bronştaki yassı epitel sigara dumanından dökülmez, özofagustaki kolumnar epitel mide asidiyle delinmez.

Ancak madalyonun diğer yüzünde çok ağır kayıplar vardır. Orijinal dokunun koruyucu fonksiyonları (mukus salgısı, siliyer temizlik, esneklik) tamamen yok olur. Daha da önemlisi, sürekli bölünen metaplastik kök hücre havuzu genetik mutasyon birikimine açık hale gelir.

> [TEMEL İLKE] Metaplazi kısa vadede bir hayatta kalma zaferidir; uzun vadede ise fonksiyon kaybı ve kanser riskidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kazanım (Avantaj)", "desc": "Mevcut fiziksel, termal veya kimyasal stresi tolere edebilme gücü.", "isKey": True},
                    {"title": "Kayıp (Dezavantaj)", "desc": "Mukosiliyer temizlik, lokal bağışıklık ve özgül salgıların sıfırlanması.", "isKey": True},
                    {"title": "Onkolojik Tehdit", "desc": "Uyaran devam ederse metaplazi displaziye ve kansere ilerleyebilir.", "isKey": False}
                ],
                "table": {
                    "title": "Metaplazinin Kar-Zarar Bilançosu",
                    "headers": ["Metaplazi Modeli", "Sağladığı Avantaj", "Yarattığı Hayati Tehlike"],
                    "rows": [
                        ["Bronş Skuamöz Metaplazisi", "Dumana karşı epitel bütünlüğünü koruma", "Siliya kaybı, enfeksiyonlar, Skuamöz Hücreli Kanser riski"],
                        ["Barrett Özofagusu", "Mide asidine karşı mukozal direnç", "Özofagus Adenokarsinomu riski (30-40 kat artış)"],
                        ["Mesane Skuamöz Metaplazisi", "Kronik taş tahrişine dayanıklılık", "Mesane Skuamöz Hücreli Karsinom riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Metaplazi dokuyu korur ancak özelleşmiş fonksiyonların kaybına ve malignite zeminine yol açar.",
                "🚨 [KRİTİK UYARI] Kalıcı zararlı uyaran varlığında metaplazi displaziye ve invaziv karsinoma dönüşebilir."
            ],
            "medicalTerms": [
                {"term": "Malign Dönüşüm", "explanation": "Benign veya adaptif bir hücre popülasyonunun mutasyonlarla kansere evrilmesidir."},
                {"term": "Displazi", "explanation": "Hücrelerin yapısal ve sitolojik düzenini kaybederek kanser öncüsü atipik özellikler kazanmasıdır."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "Metaplazinin 'çift uçlu bir kılıç' olarak tanımlanmasının temel patolojik gerekçesi nedir?",
                    "Çünkü yeni hücre tipi mevcut zararlı uyarana karşı dokuyu korurken; orijinal hücrelerin özelleşmiş fonksiyonları (ör. siliya, mukus) kaybolur ve lezyon kanserleşme (displazi) riski taşır."
                ),
                make_cloze(
                    "Metaplazi dokuyu kronik tahrişten korur; ancak uyaran devam ederse malign transformasyon göstererek [karsinoma] ilerleyebilir.",
                    "karsinoma",
                    "Epitel kanseri genel adı"
                )
            ]
        },

        # Adım 83
        {
            "slideNumber": 83,
            "title": "Metaplazi-Displazi-Karsinom Dizilimi: Barrett'ten Özofagus Adenokarsinomuna",
            "subtitle": "Kronik irritasyon sürdükçe metaplastik epitel displazi basamaklarından geçerek invaziv kansere dönüşür.",
            "badge": "Kanserleşme Dizilimi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Metaplazinin en korkulan sonucu **Metaplazi -> Displazi -> İnvaziv Karsinom** kaskadıdır. Bu onkolojik zincirin en tipik klinik örneği Barrett özofagusudur.

Kronik reflü sürdükçe metaplastik kolumnar hücrelerde zamanla p53 ve CDKN2A gen mutasyonları birikir. Hücreler polaritelerini kaybeder, çekirdekleri büyür ve **Düşük Dereceli Displazi (LGD)** gelişir. Mutasyonlar arttıkça **Yüksek Dereceli Displaziye (HGD)** ve sonunda bazal membranı yıkarak **Özofagus Adenokarsinomuna** dönüşür.

> [KLİNİK İPUCU] Barrett özofagusu hastaları displazi gelişimi açısından düzenli endoskopik biyopsilerle takip edilir; HGD cerrahi/ablasyon endikasyonudur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Onkolojik Sıralama", "desc": "Normal epitel -> Metaplazi -> Düşük displazi -> Yüksek displazi -> Kanser.", "isKey": True},
                    {"title": "Adenokarsinom Riski", "desc": "Barrett özofaguslu bireylerde adenokarsinom riski topluma göre 30-40 kat yüksektir.", "isKey": True},
                    {"title": "Endoskopik Tarama", "desc": "Amaç displaziyi erken evrede yakalayarak invaziv kanser gelişmeden ablasyon yapmaktır.", "isKey": False}
                ],
                "table": {
                    "title": "Barrett Karsinojenez Aşamaları",
                    "headers": ["Aşama", "Histolojik Bulgular", "Klinik Yönetim"],
                    "rows": [
                        ["Barrett Metaplazisi", "İntestinal goblet hücreleri, atipi yok", "3-5 yılda bir endoskopik takip"],
                        ["Düşük Dereceli Displazi", "Nükleer irileşme, bazal polarite korunmuş", "Radyofrekans ablasyon veya 6 ayda bir kontrol"],
                        ["Yüksek Dereceli Displazi", "Belirgin pleomorfizm, nükleer polarite kaybı", "Endoskopik mukozal rezeksiyon / ablasyon"],
                        ["İnvaziv Adenokarsinom", "Bezlerin submukozaya ve kas tabakasına invazyonu", "Özofajektomi ve onkolojik tedavi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Barrett özofagusu distal özofagus ADENOKARSİNOMUNUN en önemli prekanseröz öncülüdür.",
                "📌 [SINAV SPOTU] Metaplazi-displazi-kanser diziliminde yüksek dereceli displazi (HGD) invazyon öncesi son basamaktır."
            ],
            "medicalTerms": [
                {"term": "Displazi", "explanation": "Epitel dokusunda nükleer atipi, polarite kaybı ve düzensiz çoğalmayla karakterize kanser öncüsü lezyondur."},
                {"term": "Karsinom", "explanation": "Epitel dokusundan köken alarak bazal membranı aşan malign neoplazidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Barrett Karsinojenez Kaskadı",
                    [
                        "1. Kronik Reflü: Distal özofagusta mide asidi ve safra tahrişi.",
                        "2. Kolumnar Metaplazi: Yassı epitelin yerini goblet hücreli Barrett epitelinin alması.",
                        "3. Genetik Hasar: Sürekli inflamasyon ortamında p53 ve p16 mutasyonlarının birikmesi.",
                        "4. Displazi Gelişimi: Hücrelerin atipikleşmesi (LGD -> HGD).",
                        "5. İnvaziv Karsinom: Malign bezlerin bazal membranı delerek submukozaya invaze olması."
                    ]
                ),
                make_branching_logic(
                    "Kronik reflü hastasının endoskopik biyopsisinde 'Barrett Özofagusu zemininde Yüksek Dereceli Displazi (HGD)' raporlanması senaryosu.",
                    [
                        {
                            "text": "Yalnızca antiasit şurup verilerek 5 yıl sonra kontrole çağrılır.",
                            "isCorrect": False,
                            "feedback": "Ağır hata! HGD kanserden bir önceki adımdır; 5 yıl içinde invaziv kanser kaçınılmazdır."
                        },
                        {
                            "text": "Lezyon erken karsinom öncülü kabul edilir; endoskopik mukozal rezeksiyon (EMR) veya radyofrekans ablasyon ile displazik alan tamamen ortadan kaldırılır.",
                            "isCorrect": True,
                            "feedback": "Mükemmel klinik onkoloji yönetimi! HGD invaziv adenokarsinoma dönüşmeden ablasyonla tedavi edilir."
                        },
                        {
                            "text": "Hastaya acilen kemoterapi başlanır.",
                            "isCorrect": False,
                            "feedback": "Hatalı! İnvaziv kanser olmadan sistemik kemoterapi verilmez."
                        }
                    ]
                )
            ]
        },

        # Adım 84
        {
            "slideNumber": 84,
            "title": "Otofaji Tanımı: Hücrenin Kendi İçeriğini Lizozomda Sindirmesi",
            "subtitle": "Otofaji, hücrenin besin kıtlığında veya hasar durumunda kendi bileşenlerini lizozomlarda sindirmesidir.",
            "badge": "Hücresel Temizlik",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Otofaji (autophagy)**, kelime anlamıyla ==hücrenin kendi kendini yemesi== (self-eating) demektir. Hücrenin besin kıtlığı, iskemi veya stres anlarında kendi sitoplazmik proteinlerini ve yaşlanmış organellerini lizozomlar içinde sindirerek geri dönüştürdüğü yaşamsal bir adaptasyon sürecidir.

Otofaji hücreyi bir taraftan açlıkta enerji ve amino asit sağlayarak hayatta tutar; diğer taraftan hasarlı mitokondrileri ve toksik protein yumaklarını temizleyerek hücresel kalite kontrolü sağlar. Nobel ödüllü bu mekanizma hücresel sağkalımın merkezindedir.

> [TEMEL İLKE] Otofaji, hücrenin kıtlıkta kendi parçalarını yakıt olarak kullanarak yaşamını sürdürmesini sağlayan koruyucu bir adaptasyondur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kendi Kendini Sindirme", "desc": "Hücre içi organel ve proteinlerin lizozomal asit hidrolazlarla parçalanmasıdır.", "isKey": True},
                    {"title": "Enerji Kurtarma", "desc": "Açlıkta amino asit ve yağ asidi sağlayarak ATP üretimini devam ettirir.", "isKey": True},
                    {"title": "Kalite Kontrol", "desc": "Bozulmuş mitokondri ve protein agregatlarını temizleyerek apoptozu engeller.", "isKey": False}
                ],
                "table": {
                    "title": "Otofajinin İki Temel Biyolojik Rolü",
                    "headers": ["Fonksiyon", "Biyolojik Mekanizma", "Klinik / Hücresel Fayda"],
                    "rows": [
                        ["Metabolik Sağkalım", "Proteinlerin amino asitlere yıkımı", "Açlık ve iskemide hücre ölümünün önlenmesi"],
                        ["Organel Temizliği", "Hasarlı mitokondrilerin sindirilmesi (mitofaji)", "Reaktif oksijen türevlerinin (ROS) azaltılması"],
                        ["Agregat Temizliği", "Yanlış katlanmış protein yumaklarının yıkımı", "Nörodejeneratif hastalıklara (Alzheimer) karşı koruma"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Otofaji, hücrenin kendi organel ve sitoplazma içeriğini lizozomlarda sindirerek enerji sağladığı adaptif süreçtir.",
                "📌 [SINAV SPOTU] Otofaji açlıkta hayatta kalmayı sağlar ve hasarlı organelleri ortadan kaldırır."
            ],
            "medicalTerms": [
                {"term": "Otofaji", "explanation": "Hücrenin sitoplazmik bileşenlerini ve organellerini lizozomlarda parçalama sürecidir."},
                {"term": "Mitofaji", "explanation": "Hasarlanmış mitokondrilerin otofaji yoluyla seçici olarak sindirilip temizlenmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Besin ve enerji kıtlığıyla karşılaşan bir hücrenin kendi yaşlanmış organellerini ve proteinlerini lizozomlar içinde sindirerek amino asit ve enerji elde ettiği temel adaptasyon süreci hangisidir?",
                    {
                        "A": "Otofaji",
                        "B": "Heterotopik ossifikasyon",
                        "C": "Kazeöz nekroz",
                        "D": "Kompansatuvar hiperplazi",
                        "E": "Displazi"
                    },
                    "A",
                    {
                        "A": "Doğru: Hücrenin kendi bileşenlerini lizozomda sindirmesi otofajidir.",
                        "B": "Yanlış: Heterotopik ossifikasyon kemikleşme metaplazisidir.",
                        "C": "Yanlış: Kazeöz nekroz tüberküloz ölümüdür.",
                        "D": "Yanlış: Hiperplazi hücre çoğalmasıdır.",
                        "E": "Yanlış: Displazi kanser öncülü atipidir."
                    }
                ),
                make_cloze(
                    "Hücrenin besin kıtlığında kendi organellerini lizozomda sindirerek enerji ürettiği koruyucu adaptasyona [otofaji] adı verilir.",
                    "otofaji",
                    "Kendi kendini yeme terimi"
                )
            ]
        },

        # Adım 85
        {
            "slideNumber": 85,
            "title": "Otofajinin Üç Temel Tipi: Makrootofaji, Mikrootofaji ve Şaperon Aracılı Otofaji",
            "subtitle": "Kargoların lizozoma ulaştırılma biçimine göre üç farklı otofajik yolak bulunur.",
            "badge": "Yolak Çeşitleri",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücre biyolojisinde otofaji kargonun lizozom içine alınış mekanizmasına göre üç temel tipe ayrılır: **Makrootofaji**, **Mikrootofaji** ve **Şaperon Aracılı Otofaji (CMA)**.

Genel olarak 'otofaji' denildiğinde kastedilen ana form **makrootofajidir**; burada sitoplazmik kargo çift katlı bir zarla kuşatılarak otofagozom oluşturulur. **Mikrootofajide** lizozom zarı doğrudan içeriye doğru çöker (invaginasyon) ve kargoyu yutar. **Şaperon aracılı otofajide** ise KFERQ motifi taşıyan proteinler şaperonlarca (Hsc70) tanınarak LAMP-2A reseptörüyle lizozoma sokulur.

> [TEMEL İLKE] Makrootofaji organelleri çift zarlı keselerle taşırken; şaperon aracılı otofaji tek tek proteinleri translokasyonla lizozoma sokar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Makrootofaji", "desc": "Çift zarlı otofagozom oluşturarak organelleri lizozoma taşıyan ana formdur.", "isKey": True},
                    {"title": "Mikrootofaji", "desc": "Lizozom zarının doğrudan içeri çökerek kargoyu yutmasıdır.", "isKey": True},
                    {"title": "Şaperon Aracılı (CMA)", "desc": "Hsc70 ve LAMP-2A reseptörü aracılığıyla seçici protein translokasyonudur.", "isKey": False}
                ],
                "table": {
                    "title": "Otofaji Tiplerinin Karşılaştırması",
                    "headers": ["Otofaji Tipi", "Taşıma Mekanizması", "Tipik Kargo"],
                    "rows": [
                        ["Makrootofaji", "Çift zarlı otofagozom kesesi oluşturma", "Mitokondri, ribozom, büyük protein yumakları"],
                        ["Mikrootofaji", "Lizozom membranının doğrudan invaginasyonu", "Küçük sitoplazmik parçalar ve moleküller"],
                        ["Şaperon Aracılı (CMA)", "Hsc70 şaperonu ve LAMP-2A kapısı", "KFERQ amino asit motifi taşıyan çözünür proteinler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] En yaygın otofaji biçimi çift zarlı otofagozom oluşturan makrootofajidir.",
                "📌 [SINAV SPOTU] Şaperon aracılı otofajide LAMP-2A reseptörü kilit kapı görevi görür."
            ],
            "medicalTerms": [
                {"term": "Makrootofaji", "explanation": "Sitoplazma parçalarının çift zarlı otofagozom içine alınıp lizozomla kaynaştırılmasıdır."},
                {"term": "LAMP-2A", "explanation": "Şaperon aracılı otofajide hedef proteinlerin lizozoma girmesini sağlayan membran reseptörüdür."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Makrootofaji ile Şaperon Aracılı Otofaji (CMA)",
                    "Makrootofaji",
                    "Şaperon Aracılı Otofaji (CMA)",
                    [
                        "Çift zarlı otofagozom vezikülü kurulur",
                        "Tüm organelleri ve kitleleri içine alır",
                        "Vezikül lizozomla füzyona uğrar"
                    ],
                    [
                        "Vezikül oluşmaz, zardan geçiş vardır",
                        "KFERQ motifi taşıyan tekil proteinleri seçer",
                        "Hsc70 ve LAMP-2A kanalıyla lizozoma girer"
                    ]
                ),
                make_cloze(
                    "Çift zarlı otofagozom keseleri oluşturarak organelleri lizozoma taşıyan ana otofaji tipine [makrootofaji] adı verilir.",
                    "makrootofaji",
                    "Büyük ölçekli otofaji terimi"
                )
            ]
        },

        # Adım 86
        {
            "slideNumber": 86,
            "title": "Otofajinin Biyolojik Adımları: İzolasyon Membranı, Otofagozom ve Otofagolizozom",
            "subtitle": "Makrootofaji başlangıç zarından çift zarlı otofagozoma ve lizozom füzyonuna uzanan adımlarla yürütülür.",
            "badge": "Hücresel Basamaklar",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Makrootofaji kusursuz koordine edilen dört morfolojik evrede gerçekleşir: **Başlama**, **Nükleasyon**, **Otofagozom Oluşumu** ve **Otofagolizozom Füzyonu**.

Açlık sinyaliyle (mTOR inhibisyonu, AMPK aktivasyonu) endoplazmik retikulumdan köken alan hilal şeklinde bir **izolasyon membranı (fagofor)** doğar. Membran uzayarak sitoplazmik kargoyu sarar ve uçları birleşerek çift zarlı **otofagozomu** oluşturur. Otofagozom daha sonra bir lizozomla kaynaşarak **otofagolizozomu** meydana getirir; asit hidrolazlar kargoyu sindirir.

> [TEMEL İLKE] Otofagozom + Lizozom = Otofagolizozom formülü otofajik sindirimin merkezindedir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Fagofor (İzolasyon Zarı)", "desc": "Endoplazmik retikulumdan tomurcuklanan hilal şeklindeki ilk çift zar yapısıdır.", "isKey": True},
                    {"title": "Otofagozom", "desc": "Kargoyu tamamen hapseden çift zarlı kapalı veziküldür.", "isKey": True},
                    {"title": "Füzyon ve Sindirim", "desc": "Lizozomla birleşerek içeriğin asidik enzimlerle monomerlere yıkılmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Otofajik Keselerin Evreleri",
                    "headers": ["Yapı", "Zar Sayısı", "Biyolojik Durumu"],
                    "rows": [
                        ["Fagofor", "Çift zar (açık hilal)", "Kargoyu kuşatmak üzere uzama evresinde"],
                        ["Otofagozom", "Çift zar (kapalı küre)", "Sindirim enzimi içermeyen kapalı kargo paketi"],
                        ["Otofagolizozom", "Tek zar (dış zar füzyonu)", "Lizozom enzimleri içeren aktif sindirim vezikülü"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Otofagozom çift zarlıdır; lizozomla kaynaştığında oluşan otofagolizozomda sindirim gerçekleşir.",
                "📌 [SINAV SPOTU] mTOR kinazın baskılanması otofaji sürecini başlatan ana metabolik anahtardır."
            ],
            "medicalTerms": [
                {"term": "Fagofor", "explanation": "Otofajinin başlangıcında kargoyu sarmak üzere oluşan hilal şeklindeki izolasyon zarıdır."},
                {"term": "Otofagolizozom", "explanation": "Otofagozomun lizozomla birleşmesi sonucu oluşan sindirim vakuolüdür."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Otofaji Biyolojik Kaskadı",
                    [
                        "1. Kıtlık Sinyali: Açlık durumunda AMPK aktivasyonu ve mTOR kinazın susması.",
                        "2. Fagofor Oluşumu: ER zarından hilal şeklinde çift katlı izolasyon zarının belirmesi.",
                        "3. Kargo Kuşatması: LC3-II proteinleri yardımıyla zarın hasarlı organelleri sarması.",
                        "4. Otofagozom Kapanması: Zar uçlarının birleşerek kapalı çift zarlı vezikül oluşturması.",
                        "5. Füzyon ve Yıkım: Lizozomla birleşip otofagolizozom oluşturularak içeriğin sindirilmesi."
                    ]
                ),
                make_cloze(
                    "Çift zarlı otofagozomun hidrolitik enzimler içeren lizozom ile kaynaşması sonucu oluşan sindirim kesesine [otofagolizozom] adı verilir.",
                    "otofagolizozom",
                    "Füzyon kesesi birleşik adı"
                )
            ]
        },

        # Adım 87
        {
            "slideNumber": 87,
            "title": "Açlık ve Metabolik Stres Yanıtında Otofajinin Yaşamsal Kurtarıcı Rolü",
            "subtitle": "Besin yokluğunda otofaji hücresel yapı taşlarını geri dönüştürerek yaşamsal ATP sentezini sürdürür.",
            "badge": "Metabolik Kurtarma",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Akut besin veya glukoz kıtlığında hücre içi ATP düzeyi düşerken AMP seviyesi yükselir. Bu durum hücresel enerji sensörü olan **AMPK (AMP ile aktive olan protein kinaz)** enzimini uyarır.

AMPK, hücre büyümesini tetikleyen mTOR kompleksini baskılar ve **otofajiyi tam güçle başlatır**. Otofaji ile parçalanan proteinlerden elde edilen amino asitler karaciğerde glukoneogeneze sokulur; yağ asitleri ise mitokondriyal beta-oksidasyonla ATP'ye çevrilir. Bu adaptasyon sayesinde hücre haftalarca açlığa direnebilir.

> [TEMEL İLKE] Otofaji, dışarıdan besin gelmediğinde hücrenin kendi depolarını yakarak canlı kalmasını sağlayan acil durum jeneratörüdür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "AMPK Aktivasyonu", "desc": "Enerji düşüklüğünü algılayan AMPK enzimi otofajinin ana açma anahtarıdır.", "isKey": True},
                    {"title": "mTOR İnhibisyonu", "desc": "Besin yokluğunda mTOR susturularak anabolizma durdurulur, otofaji açılır.", "isKey": True},
                    {"title": "Substrat Geri Kazanımı", "desc": "Açığa çıkan amino asitler ve serbest yağ asitleri yaşamsal metabolizmayı besler.", "isKey": False}
                ],
                "table": {
                    "title": "Tokluk vs Açlık Durumunda Otofaji Dengesi",
                    "headers": ["Parametre", "Tokluk (Bol Besin)", "Açlık / Kıtlık (Metabolik Stres)"],
                    "rows": [
                        ["Aktif Sensör", "mTOR kompleksi aktif", "AMPK aktif, mTOR inaktif"],
                        ["Hücresel Süreç", "Protein sentezi, büyüme, hipertrofi", "Protein yıkımı, otofaji, enerji tasarrufu"],
                        ["Otofaji Düzeyi", "Bazal kalite kontrol düzeyinde", "Maksimum indüklenmiş düzeyde"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Açlıkta otofajiyi başlatan anahtar enzim AMPK'dir; otofajiyi frenleyen enzim mTOR'dur.",
                "📌 [SINAV SPOTU] Otofaji amino asit ve yağ asidi sağlayarak açlıkta hücrenin canlı kalmasını temin eder."
            ],
            "medicalTerms": [
                {"term": "AMPK", "explanation": "Hücresel enerji düşüşünü (yüksek AMP/ATP) algılayarak otofajiyi başlatan kinazdır."},
                {"term": "mTOR", "explanation": "Besin bolluğunda protein sentezini artıran, açlıkta susarak otofajiye izin veren kinazdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Tokluk ve Açlık Durumlarında Hücresel Sinyal Ayrımı",
                    "Tokluk Durumu (Besin Zenginliği)",
                    "Açlık Durumu (Metabolik Kriz)",
                    [
                        "İnsülin ve büyüme faktörleri yüksek",
                        "mTOR aktif, protein sentezi açık",
                        "Otofaji kaskadı baskılanmış"
                    ],
                    [
                        "Hücre içi AMP/ATP oranı yükselmiş",
                        "AMPK aktif, mTOR tamamen baskılı",
                        "Otofaji maksimum hızda indüklenmiş"
                    ]
                ),
                make_active_recall(
                    "Açlık durumunda hücresel enerji sensörü olan AMPK aktifleştiğinde otofajiyi tetiklemek için hangi ana büyüme düzenleyici kinazı baskılar?",
                    "mTOR (mammalian target of rapamycin) kinazını baskılar; mTOR susunca otofaji başlatıcı kompleksler serbest kalarak otofajiyi ateşler."
                )
            ]
        },

        # Adım 88
        {
            "slideNumber": 88,
            "title": "Otofaji Genleri (ATG) ve Hücre İçi Organel Kalite Kontrolü",
            "subtitle": "Otofaji kaskadı evrimsel olarak korunan ATG genleri ve LC3 proteini tarafından yürütülür.",
            "badge": "Genetik Kontrol",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Otofaji süreci rastgele bir lizozomal hareket değil; mayalardan insana son derece korunmuş **ATG (Autophagy-related Genes)** ailesi tarafından yürütülür.

Bu sistemde en önemli moleküler belirteç **LC3 (Mikrotübül ilişkili protein 1 hafif zincir 3)** proteinidir. Otofaji başladığında sitozolik LC3-I formu fosfatidiletanolamin ile lipitlenerek **LC3-II** formuna döner ve otofagozom zarına yerleşir. Laboratuvarda LC3-II artışının gösterilmesi hücrede otofajinin aktif olduğunun altın standart kanıtıdır.

> [TEMEL İLKE] Otofaji genlerindeki (ATG) mutasyonlar Parkinson, Alzheimer ve Crohn hastalığı gibi otofajik kalite kontrol defektlerine yol açar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "ATG Gen Ailesi", "desc": "Fagofor oluşumundan lizozom füzyonuna kadar tüm basamakları yöneten genlerdir.", "isKey": True},
                    {"title": "LC3-II Belirteci", "desc": "Otofagozom zarına bağlanan ve otofaji aktivitesini kanıtlayan kilit proteindir.", "isKey": True},
                    {"title": "Klinik Korelasyon", "desc": "Otofaji yetersizliği yaşlanma, kanser ve nörodejenerasyonda birikim hastalıklarına yol açar.", "isKey": False}
                ],
                "table": {
                    "title": "Kilit Otofaji Molekülleri",
                    "headers": ["Molekül", "Biyolojik Görevi", "Tanısal / Klinik Önemi"],
                    "rows": [
                        ["ATG5 / ATG12 Kompleksi", "İzolasyon zarının uzamasını yönetir", "Otofagozom oluşumu için zorunlu"],
                        ["LC3-II", "Otofagozom zarına lipidlenerek bağlanır", "Otofajinin biyokimyasal altın standart belirteci"],
                        ["Beclin-1 (ATG6)", "Vesikül nükleasyon kompleksini kurar", "Tümör baskılayıcı fonksiyon taşır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Otofajinin deneysel ve patolojik olarak gösterilmesinde LC3-II proteini altın standart belirteçtir.",
                "📌 [SINAV SPOTU] Beclin-1 otofaji nükleasyonunda rol oynayan temel düzenleyicidir."
            ],
            "medicalTerms": [
                {"term": "LC3-II", "explanation": "Otofagozom zarına entegre olan ve otofajik aktiviteyi gösteren lipitlenmiş proteindir."},
                {"term": "Beclin-1", "explanation": "Otofajinin başlangıç vezikül oluşumunu düzenleyen kilit regülatör proteindir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Araştırma laboratuvarında bir hücrede otofajinin aktif olarak gerçekleştiğini Western Blot veya immünofloresan yöntemle kanıtlamak isteyen bir patoloğun bakması gereken altın standart otofagozom belirteci protein hangisidir?",
                    {
                        "A": "LC3-II (Mikrotübül ilişkili protein hafif zincir 3 lipidli formu)",
                        "B": "Sitokeratin 20",
                        "C": "Karsinoembriyonik antijen (CEA)",
                        "D": "Kaldesmon",
                        "E": "Alfafetoprotein (AFP)"
                    },
                    "A",
                    {
                        "A": "Doğru: LC3-II otofagozom zarına giren ve otofajiyi kanıtlayan altın standart moleküler belirteçtir.",
                        "B": "Yanlış: CK20 kolorektal epitel keratinidir.",
                        "C": "Yanlış: CEA gastrointestinal tümör belirtecidir.",
                        "D": "Yanlış: Kaldesmon düz kas belirtecidir.",
                        "E": "Yanlış: AFP hepatosellüler karsinom ve testis tümör belirtecidir."
                    }
                ),
                make_cloze(
                    "Otofagozom zarına entegre olarak otofaji aktivitesini kesin olarak kanıtlayan altın standart moleküler belirtece [LC3-II] adı verilir.",
                    "LC3-II",
                    "Lipitlenmiş otofaji belirteç proteini"
                )
            ]
        },

        # Adım 89 (CHECKPOINT 9)
        {
            "slideNumber": 89,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Mezenkimal Metaplazi ve Otofaji",
            "subtitle": "Miyozitis ossifikansı, Barrett karsinojenez zincirini ve otofajinin moleküler adımlarını pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 9,
            "synthesisNarrative": """Bu bölümde mezenkimal doku metaplazilerini, metaplazinin kanserleşme dizilimini ve yaşamsal hücresel geri dönüşüm mekanizması olan otofajiyi inceledik.

Miyozitis ossifikans travma sonrası kasta heterotopik kemik oluşumuyla seyreden benign mezenkimal metaplazidir. Epitelyal metaplazi ise çift uçlu bir kılıçtır; Barrett özofagusunda reflüye direnç sağlarken displazi üzerinden adenokarsinoma ilerleyebilir. Otofaji ise açlıkta AMPK uyarımı ve mTOR baskılanmasıyla başlayan, ATG genleri ve LC3-II aracılığıyla organelleri lizozomda yıkarak enerji üreten yaşamsal adaptasyondur.

> [TEKRAR SPOTU] Metaplazi kanser öncüsü zemin oluşturabilir; otofaji ise hücreyi açlıkta canlı tutan temel enerji jeneratörüdür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Miyozitis Ossifikans", "desc": "Kas içi travma sonrası heterotopik kemikleşmeyle giden mezenkimal metaplazidir.", "isKey": True},
                    {"title": "Kanser Dizilimi", "desc": "Metaplazi -> Displazi -> İnvaziv Karsinom zinciri Barrett'in temel tehlikesidir.", "isKey": True},
                    {"title": "Otofaji Makinesi", "desc": "AMPK uyarımı, otofagozom oluşumu, LC3-II belirteci ve lizozomal sindirim.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 9 Sentez Tablosu",
                    "headers": ["Kavram", "Biyolojik Mekanizma", "Kritik Klinik Anlam"],
                    "rows": [
                        ["Miyozitis Ossifikans", "Kas içi heterotopik kemikleşme", "Osteosarkomla karışabilen benign metaplazi"],
                        ["Barrett Displazisi", "Metaplastik epitelde atipi gelişimi", "Özofagus adenokarsinomu öncülü"],
                        ["Makrootofaji", "Çift zarlı vezikülle lizozomal sindirim", "Açlıkta enerji sağlama ve kalite kontrol"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyozitis ossifikans kas içi travma sonrası heterotopik kemikleşmeyle giden mezenkimal metaplazidir.",
                "📌 [SINAV SPOTU] Otofajinin moleküler göstergesi LC3-II proteinidir; açlıkta AMPK uyarımıyla başlar."
            ],
            "medicalTerms": [
                {"term": "Mezenkimal Metaplazi", "explanation": "Bağ dokusu kök hücrelerinin kemik veya kıkırdak hücresine dönüşmesidir."},
                {"term": "LC3-II", "explanation": "Otofagozom zarına bağlanarak otofaji aktivitesini kanıtlayan kilit proteindir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc25",
                    "Miyozitis ossifikans nedir ve osteosarkomdan histolojik ve radyolojik olarak nasıl ayırt edilir?",
                    "Kas içi hematom sonrası gelişen heterotopik kemikleşmedir (mezenkimal metaplazi); lezyonun periferinde olgun lameller kemik, merkezinde hücresel doku bulunmasıyla (zonal mimari) osteosarkomdan ayrılır."
                ),
                make_flashcard(
                    "k1-03-fc26",
                    "Barrett özofagusunda kanserleşme dizilimi nasıl ilerler ve klinik önemi nedir?",
                    "Normal yassı epitel -> Kolumnar intestinal metaplazi -> Düşük dereceli displazi -> Yüksek dereceli displazi -> İnvaziv adenokarsinom şeklinde ilerler; hastalar düzenli biyopsiyle taranır."
                ),
                make_flashcard(
                    "k1-03-fc27",
                    "Otofaji nedir ve açlık durumunda hücresel enerji sensörleri tarafından nasıl aktive edilir?",
                    "Hücrenin kendi organel ve proteinlerini lizozomda sindirmesidir; açlıkta yükselen AMP düzeyi AMPK kinazı uyarır, AMPK ise mTOR kinazı baskılayarak otofajiyi tam güçle başlatır."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Barrett özofagusu zemininde gelişen adenokarsinom ile klasik sigara ve alkole bağlı özofagus kanserinin histopatolojik tip farkı nedir?",
                    "Barrett özofagusu zemininde glandüler kolumnar epitelden kaynaklanan Adenokarsinom gelişirken; sigara ve alkole bağlı klasik özofagus kanseri çok katlı yassı epitelden kaynaklanan Skuamöz Hücreli Karsinomdur."
                )
            ]
        }
    ]
