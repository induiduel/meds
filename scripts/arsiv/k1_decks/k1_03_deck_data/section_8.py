#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 8: Metaplazi: Tanım, Kök Hücre Reprogramlaması ve Epitelyal Örnekler (Adımlar 70 - 79)
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
        # Adım 70
        {
            "slideNumber": 70,
            "title": "Metaplazi Tanımı: Bir Erişkin Hücre Tipinin Diğerine Dönüşümü",
            "subtitle": "Metaplazi, strese duyarlı bir erişkin hücre tipinin strese daha dayanıklı başka bir hücre tipine dönüşmesidir.",
            "badge": "Temel Tanım",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Metaplazi**, bir diferansiye (olgun) hücre tipinin (epitelyal veya mezenkimal), maruz kaldığı kronik zararlı uyarana karşı daha dayanıklı olan ==başka bir diferansiye hücre tipi ile geri dönüşümlü olarak yer değiştirmesidir==.

Buradaki temel biyolojik mantık, mevcut olumsuz çevre koşullarına dayanamayan hassas hücrelerin yerini, o stres ortamında hayatta kalabilecek daha dirençli bir hücre popülasyonuna bırakmasıdır. En sık epitel dokularda görülmekle birlikte mezenkimal dokularda da gelişebilir.

> [TEMEL İLKE] Metaplazi koruyucu bir adaptasyondur; ancak yeni hücre tipi dayanıklı olsa da orijinal hücrenin özelleşmiş fonksiyonlarını yerine getiremez.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Diferansiasyon Değişimi", "desc": "Olgun bir hücre tipinin yerini başka bir olgun hücre tipi alır.", "isKey": True},
                    {"title": "Dayanıklılık Amacı", "desc": "Yeni hücre tipi mevcut fiziksel/kimyasal strese karşı çok daha dirençlidir.", "isKey": True},
                    {"title": "Geri Dönüşümlülük", "desc": "Zararlı kronik uyaran kesildiğinde epitel orijinal haline dönebilir.", "isKey": False}
                ],
                "table": {
                    "title": "Klasik Metaplazi Tipleri ve Çevre Koşulları",
                    "headers": ["Orijinal Epitel", "Metaplastik Yeni Epitel", "Tetikleyici Kronik Stres"],
                    "rows": [
                        ["Siliyalı Kolumnar (Bronş)", "Çok katlı yassı (Skuamöz)", "Kronik sigara dumanı toksisitesi"],
                        ["Çok Katlı Yassı (Özofagus)", "Müsinöz Kolumnar (Barrett)", "Mide asidi ve safra reflüsü"],
                        ["Transizyonel Epitel (Mesane)", "Çok katlı yassı (Skuamöz)", "Kronik mesane taşı veya Schistosoma enfeksiyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Metaplazi, bir olgun hücre tipinin başka bir olgun hücre tipine geri dönüşümlü dönüşümüdür.",
                "📌 [SINAV SPOTU] Metaplazide yeni hücre tipi strese daha dayanıklıdır ancak koruyucu fonksiyonları (mukus/sil) eksiktir."
            ],
            "medicalTerms": [
                {"term": "Metaplazi", "explanation": "Bir diferansiye hücre tipinin yerini başka bir diferansiye hücre tipinin almasıdır."},
                {"term": "Skuamöz Metaplazi", "explanation": "Kolumnar veya transizyonel epitelin basınca dayanıklı çok katlı yassı epitele dönüşmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Metaplazi kavramının biyolojik tanımı aşağıdakilerden hangisinde eksiksiz verilmiştir?",
                    {
                        "A": "Bir olgun hücre tipinin strese daha dayanıklı başka bir olgun hücre tipine geri dönüşümlü dönüşümü",
                        "B": "Hücre sayısının kontrolsüzce artarak kitle oluşturması",
                        "C": "Hücrelerin yapısal proteinlerini kaybederek küçülmesi",
                        "D": "Hücre zarının parçalanmasıyla gelişen ölüm süreci",
                        "E": "Embriyolojik dönemde dokunun hiç oluşmaması"
                    },
                    "A",
                    {
                        "A": "Doğru: Metaplazi bir erişkin hücre tipinin diğeriyle geri dönüşümlü yer değiştirmesidir.",
                        "B": "Yanlış: Hücre sayısı artışı hiperplazidir.",
                        "C": "Yanlış: Küçülme atrofidir.",
                        "D": "Yanlış: Membran parçalanması nekrozdur.",
                        "E": "Yanlış: Dokunun oluşmaması aplazidir."
                    }
                ),
                make_cloze(
                    "Kronik zararlı uyarana karşı bir olgun hücre tipinin yerini daha dirençli başka bir hücre tipinin almasına [metaplazi] denir.",
                    "metaplazi",
                    "Hücre tipi dönüşüm adaptasyonu"
                )
            ]
        },

        # Adım 71
        {
            "slideNumber": 71,
            "title": "Metaplazinin Moleküler Mekanizması: Kök Hücrelerin Yeniden Programlanması",
            "subtitle": "Metaplazi olgun hücrelerin birbirine dönüşmesiyle değil, doku kök hücrelerinin yeniden programlanmasıyla gerçekleşir.",
            "badge": "Genetik Reprogramlama",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Metaplazinin moleküler mekanizması sık yapılan bir kavram yanılgısını düzeltir: Olgunlaşmış bir kolumnar hücre doğrudan yassı epitel hücresine dönüşmez.

Metaplazi, dokuda yerleşik **erişkin kök hücrelerin (stem cells)** veya indiferansiye rezerv hücrelerin ==yeniden programlanması (reprogramming)== ile gerçekleşir. Kronik stres ortamındaki sitokinler ve büyüme faktörleri, kök hücrelerdeki özgül transkripsiyon faktörlerini modüle eder. Kök hücreler eski hücre tipi yerine yeni hücre tipine farklılaşacak şekilde bölünür.

> [TEMEL İLKE] Metaplazi olgun hücrenin şekil değiştirmesi değil; kök hücrenin farklılaşma komutunun değiştirilmesidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kök Hücre Kaynağı", "desc": "Dönüşüm bazal tabakadaki erişkin kök ve rezerv hücrelerde başlar.", "isKey": True},
                    {"title": "Transkripsiyon Faktörleri", "desc": "Sitokinler ve vitaminler farklılaşmayı yöneten transkripsiyon genlerini değiştirir.", "isKey": True},
                    {"title": "Mevcut Hücrelerin Kaderi", "desc": "Eski olgun hücreler dökülür; alttan gelen yeni kök hücre soyu metaplastiktir.", "isKey": False}
                ],
                "table": {
                    "title": "Metaplazide Moleküler Farklılaşma Anahtarları",
                    "headers": ["Doku", "Reprogramlanan Kök Hücre", "Yeni Diferansiasyon Yönü"],
                    "rows": [
                        ["Solunum Yolu", "Bronşiyal bazal rezerv hücreleri", "Skuamöz (yassı) keratinosit diferansiasyonu"],
                        ["Distal Özofagus", "Gastroözofageal kök hücreler", "İntestinal kolumnar ve goblet diferansiasyonu"],
                        ["İskelet Kası / Bağ Dokusu", "Mezenkimal multipotent kök hücreler", "Osteoblastik / Kondroblastik diferansiasyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Metaplazi olgun hücrelerin dönüşümüyle değil, doku kök hücrelerinin yeniden programlanmasıyla oluşur.",
                "📌 [SINAV SPOTU] Kök hücrelerdeki transkripsiyon faktörü ekspresyonunun değişmesi yeni hücre tipini belirler."
            ],
            "medicalTerms": [
                {"term": "Reprogramlama", "explanation": "Kök hücrenin gen ifadesini değiştirerek farklı bir hücre tipine olgunlaşmasını sağlama sürecidir."},
                {"term": "Rezerv Hücre", "explanation": "Epitel tabanında bekleyen ve hasar durumunda çoğalarak farklılaşan öncül hücredir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kök Hücre Reprogramlaması ve Metaplazi Kaskadı",
                    [
                        "1. Kronik İrritasyon: Sigara dumanı veya asit reflüsünün bazal tabakaya ulaşması.",
                        "2. Sitokin Sinyali: Hasarlı epitelden IL-1, TNF ve büyüme faktörlerinin salınımı.",
                        "3. Transkripsiyonel Değişim: Kök hücrede Notch veya Wnt yolaklarının yeniden programlanması.",
                        "4. Yeni Diferansiasyon: Kök hücre bölünmesinde skuamöz veya kolumnar gen kaskadının açılması.",
                        "5. Yüzey Değişimi: Eski siliyalı epitel dökülürken yüzeyi basınca dayanıklı yeni epitelin kaplaması."
                    ]
                ),
                make_cloze(
                    "Metaplazi olgun hücrelerin dönüşümüyle değil, bazal tabakadaki [kök hücrelerin] yeniden programlanmasıyla gerçekleşir.",
                    "kök hücrelerin",
                    "Doku yenileyici hücreler tamlaması"
                )
            ]
        },

        # Adım 72
        {
            "slideNumber": 72,
            "title": "Transdiferensiasyon vs Kök Hücre Diferensiasyon Değişimi",
            "subtitle": "Klasik insan patolojisindeki metaplazi kök hücre reprogramlamasıdır; saf transdiferensiasyon son derece nadirdir.",
            "badge": "Biyolojik Mekanizma",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücre biyolojisinde diferansiyasyon değişimi iki teorik yolla açıklanır: **Transdiferensiasyon** ve **Kök hücre diferensiasyon değişimi**.

Transdiferensiasyon, tamamen olgunlaşmış ve bölünmeyen bir hücrenin kök hücre evresine dönmeksizin doğrudan başka bir olgun hücreye dönüşmesidir. Ancak memeli dokularındaki ve insan patolojisindeki metaplazilerin neredeyse tamamı bu yolla değil; **doku kök hücrelerinin farklı bir fenotipte çoğalmasıyla** gerçekleşir.

> [TEMEL İLKE] İnsan metaplazilerinde ana mekanizma her zaman kök hücrelerin yeniden yönlendirilmiş diferansiasyonudur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Transdiferensiasyon", "desc": "Olgun bir hücrenin bölünmeden doğrudan başka bir olgun hücreye dönüşmesi (çok nadir).", "isKey": True},
                    {"title": "Kök Hücre Aracılı", "desc": "İnsan metaplazilerinde geçerli olan asıl mekanizma; kök hücrelerin yeni yönde farklılaşmasıdır.", "isKey": True},
                    {"title": "Epigenetik Modifikasyon", "desc": "DNA metilasyonu ve histon asetilasyon değişiklikleri yeni gen programını stabilize eder.", "isKey": False}
                ],
                "table": {
                    "title": "İki Farklılaşma Modelinin Karşılaştırması",
                    "headers": ["Model", "Başlangıç Hücresi", "Patolojideki Yeri"],
                    "rows": [
                        ["Transdiferensiasyon", "Olgun, diferansiye hücre", "Deneysel modellerde nadir"],
                        ["Kök Hücre Reprogramlaması", "İndiferansiye bazal kök hücre", "İnsan epitelyal metaplazilerinin tamamı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İnsanda metaplazi olgun hücrelerin transdiferensiasyonu ile değil, kök hücrelerin yeniden programlanmasıyla yürütülür.",
                "📌 [SINAV SPOTU] Epigenetik değişiklikler kök hücrenin yeni fenotipini kalıcılaştırır."
            ],
            "medicalTerms": [
                {"term": "Transdiferensiasyon", "explanation": "Tamamen olgunlaşmış bir hücrenin doğrudan başka bir olgun hücreye dönüşmesidir."},
                {"term": "Diferansiasyon", "explanation": "Kök hücrenin özelleşmiş yapısal ve fonksiyonel özellikler kazanarak olgunlaşmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Transdiferensiasyon ile Kök Hücre Diferensiasyon Değişimi",
                    "Transdiferensiasyon Teorisi",
                    "Kök Hücre Reprogramlaması (Gerçek Mekanizma)",
                    [
                        "Olgun hücre doğrudan dönüşür",
                        "Mitoz bölünme gerektirmez",
                        "İnsan patolojisinde pratik olarak görülmez"
                    ],
                    [
                        "Bazal kök hücreler yeniden programlanır",
                        "Yeni nesil hücreler mitozla üretilir",
                        "İnsan metaplazilerinin gerçek temelidir"
                    ]
                ),
                make_active_recall(
                    "İnsan solunum yolu epiteli sigaraya maruz kaldığında siliyalı hücreler doğrudan yassı epitele dönüşebilir mi?",
                    "Hayır; olgun siliyalı hücreler dönüşemez, dökülürler. Metaplazi, bazal kök hücrelerin yeni bölünen hücreleri çok katlı yassı epitele farklılaştırmasıyla gerçekleşir."
                )
            ]
        },

        # Adım 73
        {
            "slideNumber": 73,
            "title": "Solunum Epitelinde Skuamöz Metaplazi: Sigara Dumanı ve Kimyasal Toksisite",
            "subtitle": "Kronik sigara içicilerinde bronşların siliyalı kolumnar epiteli dayanıklı çok katlı yassı epitele dönüşür.",
            "badge": "Klasik Örnek",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Epitelyal metaplazinin en klasik örneği sigara içen bireylerin solunum yollarında gözlenir. Normal trakea ve bronş epiteli, havayı temizleyen ve nemlendiren **yalancı çok katlı siliyalı prizmatik (kolumnar) epiteldir**.

Sigara dumanındaki binlerce toksik kimyasal ve sıcak gazlar bu narin siliyalı hücreleri sürekli tahriş eder. Bronşiyal kök hücreler bu kimyasal strese dayanabilmek için yeniden programlanır ve yüzey epiteli basınca ve kimyasallara çok daha dirençli olan **çok katlı yassı (skuamöz) epitele** dönüşür.

> [KLİNİK İPUCU] Skuamöz metaplazi dumanın tahrişine karşı mekanik bir zırh oluşturur; ancak bu zırh solunum savunma sistemini felç eder.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Orijinal Doku", "desc": "Mukus üreten kadeh (goblet) hücreleri ve partikülleri süpüren silyalı kolumnar epitel.", "isKey": True},
                    {"title": "Metaplastik Zırh", "desc": "Kimyasal ve fiziksel travmaya dayanıklı tabakalı çok katlı yassı epitel.", "isKey": True},
                    {"title": "Reversibilite", "desc": "Sigara bırakıldığında bazal kök hücreler aylar içinde yeniden silyalı epitel üretir.", "isKey": False}
                ],
                "table": {
                    "title": "Normal Bronş vs Skuamöz Metaplastik Bronş",
                    "headers": ["Özellik", "Normal Bronş Epiteli", "Metaplastik Bronş Epiteli"],
                    "rows": [
                        ["Hücre Tipi", "Yalancı çok katlı siliyalı kolumnar", "Çok katlı yassı (skuamöz)"],
                        ["Siliya (Tüy)", "Var (sürekli mukus süpürür)", "Tamamen yok"],
                        ["Stres Direnci", "Düşük (tahrişle hızla dökülür)", "Yüksek (mekanik ve kimyasal zırh)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kronik sigara içicilerinde bronş epitelinde siliyalı kolumnar epitelden çok katlı yassı epitele dönüşüm (skuamöz metaplazi) görülür.",
                "📌 [SINAV SPOTU] Sigara bırakıldığında skuamöz metaplazi geri dönebilen (reversible) bir adaptasyondur."
            ],
            "medicalTerms": [
                {"term": "Siliyalı Epitel", "explanation": "Yüzeyinde yabancı partikülleri dışarı süpüren mikroskobik tüycükler taşıyan epiteldir."},
                {"term": "Skuamöz Metaplazi", "explanation": "Silindir veya kübik epitelin çok katlı yassı epitele dönüşmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Uzun yıllardır günde 2 paket sigara içen 50 yaşındaki bir hastanın bronş biyopsisinde siliyalı kolumnar epitel yerine çok katlı yassı epitel görülmesi hangi patolojik adaptasyondur?",
                    {
                        "A": "Skuamöz metaplazi",
                        "B": "Primer bronş karsinoid tümörü",
                        "C": "Kazeifikasyon nekrozu",
                        "D": "Kompansatuvar hiperplazi",
                        "E": "Akut flegmonöz bronşit"
                    },
                    "A",
                    {
                        "A": "Doğru: Sigara dumanına bağlı kolumnar epitelin yassı epitele dönmesi skuamöz metaplazidir.",
                        "B": "Yanlış: Karsinoid tümör nöroendokrin neoplazidir.",
                        "C": "Yanlış: Kazeifikasyon tüberküloz nekrozudur.",
                        "D": "Yanlış: Hiperplazi sayı artışıdır, hücre tipi dönüşümü değildir.",
                        "E": "Yanlış: Flegmonöz lezyon yaygın süpüratif inflamasyondur."
                    }
                ),
                make_cloze(
                    "Sigara dumanının kronik tahrişine maruz kalan bronş epitelinde gelişen adaptif hücre tipi değişimine [skuamöz] metaplazi adı verilir.",
                    "skuamöz",
                    "Yassı epitel türü adı"
                )
            ]
        },

        # Adım 74
        {
            "slideNumber": 74,
            "title": "Skuamöz Metaplazinin Bedeli: Mukosiliyer Temizlenme Kaybı ve Enfeksiyon Riski",
            "subtitle": "Dirençli yassı epitel dumanı tolere eder ancak mukus salgısı ve siliyer temizleme mekanizması yok olur.",
            "badge": "Fonksiyonel Bedel",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Metaplazi çift uçlu bir kılıçtır. Bronşta gelişen skuamöz metaplazi hücreleri dumanın yakıcı etkisinden korur; ancak bu dayanıklılık çok ağır bir fonksiyonel bedelle satın alınır.

Yeni oluşan çok katlı yassı epitelde mukus üreten goblet hücreleri ve partikülleri yukarı süpüren **siliyalar (titrek tüyler) bulunmaz**. Solunum yolunun en hayati savunma mekanizması olan **mukosiliyer yürüyen merdiven (eskalatör)** tamamen felç olur. Bakteriler ve toz partikülleri akciğerin derinliklerine kolayca ulaşarak kronik bronşit ve pnömoni riskini katlar.

> [TEMEL İLKE] Metaplazik epitel fiziksel olarak dayanıklıdır; ancak orijinal epitelin özelleşmiş fizyolojik koruma fonksiyonlarını yerine getiremez.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Siliya Kaybı", "desc": "Mukusu ve mikropları yukarı süpüren tüycükler ortadan kalkar.", "isKey": True},
                    {"title": "Mukus Durgunluğu", "desc": "Sekresyonlar temizlenemez, hava yollarında tıkaçlar oluşur.", "isKey": True},
                    {"title": "Enfeksiyon Yatkınlığı", "desc": "Bariyer savunması çöktüğünden tekrarlayan akciğer enfeksiyonları gelişir.", "isKey": False}
                ],
                "table": {
                    "title": "Bronş Metaplazisinde Korunma ve Kayıp Dengesi",
                    "headers": ["Parametre", "Kazanılan Avantaj", "Kaybedilen Hayati Fonksiyon"],
                    "rows": [
                        ["Fiziksel Yapı", "Dumana ve kimyasal ısıya yüksek direnç", "Esnek lümen mimarisi kaybı"],
                        ["Temizleme Mekanizması", "Hücre dökülmesine direnç", "Mukosiliyer klirensin tamamen durması"],
                        ["İmmünolojik Durum", "Keratinize zırh etkisi", "Lokal sekretuar IgA ve antibakteriyel bariyer kaybı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Skuamöz metaplazinin en kritik klinik dezavantajı mukosiliyer temizleme mekanizmasının kaybıdır.",
                "🚨 [KRİTİK UYARI] Mukosiliyer bariyerin kaybı kronik obstrüktif akciğer hastalığı (KOAH) ve bronşiektaziye zemin hazırlar."
            ],
            "medicalTerms": [
                {"term": "Mukosiliyer Klirens", "explanation": "Solunum yollarına giren yabancı partikül ve mikropların siliyalarca yukarı süpürülmesidir."},
                {"term": "Goblet Hücresi", "explanation": "Epitel yüzeyini nemlendiren ve koruyan mukus salgılayan kadeh hücresidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Mukosiliyer Epitel ile Metaplastik Skuamöz Epitel",
                    "Normal Siliyalı Kolumnar Epitel",
                    "Metaplastik Çok Katlı Yassı Epitel",
                    [
                        "Aktif çalışan titrek tüyler (siliya)",
                        "Mukus salgılayan goblet hücreleri",
                        "Sürekli yukarı doğru partikül temizliği"
                    ],
                    [
                        "Siliya tamamen kayıp, süpürme yok",
                        "Goblet hücresi ve mukus bariyeri yok",
                        "Partiküller akciğere çöker, enfeksiyon artar"
                    ]
                ),
                make_active_recall(
                    "Kronik sigara içicisinde gelişen skuamöz metaplazi hücreleri dumana karşı koruduğu halde hastada neden inatçı sabah öksürükleri ve sık akciğer enfeksiyonları görülür?",
                    "Çünkü metaplastik yassı epitelde mukus üreten goblet hücreleri ve partikülleri süpüren siliyalar yoktur; mukosiliyer klirens felç olduğundan sekresyonlar ancak öksürük refleksiyle atılabilir."
                )
            ]
        },

        # Adım 75
        {
            "slideNumber": 75,
            "title": "A Vitamini (Retinoik Asit) Eksikliği ve Epitelyal Metaplazi",
            "subtitle": "Retinoik asit epitel diferansiasyonunu kontrol eder; eksikliğinde göz, solunum ve üriner sistemde skuamöz metaplazi gelişir.",
            "badge": "Nutrisyonel Metaplazi",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Epitelyal metaplazi yalnızca kronik tahrişle değil, besinsel eksikliklerle de indüklenebilir. Bunun en bilinen modeli **A Vitamini (Retinoik Asit) eksikliğidir**.

A vitamini nükleer retinoik asit reseptörleri (RAR) aracılığıyla epitel kök hücrelerinin normal mukus salgılayan kolumnar veya transizyonel yönde farklılaşmasını sağlar. A vitamini eksik olduğunda kök hücre kontrolü bozulur; göz konjonktivasında (**kseroftalmi, Bitot lekeleri**), solunum yollarında ve mesanede yaygın **keratinize skuamöz metaplazi** gelişir.

> [TEMEL İLKE] A vitamini epitelin normal diferansiasyon bekçisidir; eksikliği yaygın skuamöz metaplazi ve enfeksiyon yatkınlığı doğurur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Retinoik Asit Rolü", "desc": "Kök hücrelerin mukus salgılayan normal epitele farklılaşmasını yönetir.", "isKey": True},
                    {"title": "Eksiklik Tablosu", "desc": "Solunum yolları, mesane ve konjonktivada keratinize yassı epitele dönüşüm.", "isKey": True},
                    {"title": "Kseroftalmi", "desc": "Gözyaşı epitelinin metaplazisi ve korneanın kuruyup körleşmesi sürecidir.", "isKey": False}
                ],
                "table": {
                    "title": "A Vitamini Eksikliğinde Metaplazi Alanları",
                    "headers": ["Organ / Doku", "Normal Epitel", "Eksiklikte Gelişen Metaplazi"],
                    "rows": [
                        ["Göz Konjonktivası", "Nemli non-keratinize epitel", "Kurumuş keratinize skuamöz metaplazi (Bitot lekeleri)"],
                        ["Bronş Ağacı", "Siliyalı kolumnar epitel", "Skuamöz metaplazi ve solunum enfeksiyonları"],
                        ["Üriner Mesane", "Transizyonel (ürotelyum)", "Skuamöz metaplazi ve taş oluşum riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] A vitamini (retinoik asit) eksikliği solunum ve üriner sistemde skuamöz metaplaziye yol açar.",
                "📌 [SINAV SPOTU] A vitamini eksikliğinde göz konjonktivasında keratinize metaplazi sonucu Bitot lekeleri oluşur."
            ],
            "medicalTerms": [
                {"term": "Retinoik Asit", "explanation": "Epitel hücrelerinin farklılaşmasını ve gen ekspresyonunu yöneten A vitamini aktif formudur."},
                {"term": "Kseroftalmi", "explanation": "A vitamini eksikliğinde konjonktiva metaplazisi sonucu gözün aşırı kuruması ve körlüğe gitmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Beslenmesinde uzun süre A vitamini (retinoik asit) eksikliği bulunan bir hastada solunum yolu ve mesane epitelinde gözlenmesi en muhtemel hücresel adaptasyon hangisidir?",
                    {
                        "A": "Skuamöz metaplazi",
                        "B": "Müsinöz karsinoid tümör",
                        "C": "Kazeöz nekroz",
                        "D": "Saf glandüler hipertrofi",
                        "E": "Hiperplastik polipozis"
                    },
                    "A",
                    {
                        "A": "Doğru: A vitamini eksikliği epitel kök hücrelerinde skuamöz metaplaziye neden olur.",
                        "B": "Yanlış: Karsinoid tümör neoplazidir.",
                        "C": "Yanlış: Kazeöz nekroz tüberkülozdur.",
                        "D": "Yanlış: A vitamini eksikliği hipertrofi yapmaz.",
                        "E": "Yanlış: Polipozis kolona ait lezyondur."
                    }
                ),
                make_cloze(
                    "Epitel farklılaşmasını yöneten [A vitamini] eksikliğinde solunum ve üriner sistem epitelinde skuamöz metaplazi gelişir.",
                    "A vitamini",
                    "Epitel koruyucu vitamin adı"
                )
            ]
        },

        # Adım 76
        {
            "slideNumber": 76,
            "title": "Barrett Özofagusu: Kronik Gastroözofageal Reflüde Kolumnar Metaplazi",
            "subtitle": "Mide asidi ve safranın kronik reflüsü distal özofagustaki yassı epiteli kolumnar epitele dönüştürür.",
            "badge": "Gastroenterolojik Metaplazi",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Skuamöz metaplazinin tam tersi yönde işleyen en kritik klinik model **Barrett Özofagusudur**. Normalde özofagusun lümeni lokma geçişine uygun, mekanik sürtünmeye dayanıklı **çok katlı yassı epitel** ile döşelidir.

Kronik gastroözofageal reflü hastalığında (GÖRH) mide asidi ve duodenal safra tuzları alt özofagusa sürekli geri kaçar. Yassı epitel aside karşı son derece savunmasızdır ve hızla ülsere olur. Kök hücreler asit ortamında yaşayabilmek için yeniden programlanır ve yassı epitelin yerini asitten etkilenmeyen **müsin salgılayan kolumnar epitel** alır.

> [TEMEL İLKE] Barrett özofagusunda epitel yassıdan kolumnara döner; bu adaptasyon asitten korur ancak kanser riskini katlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Ters Yönlü Dönüşüm", "desc": "Skuamöz epitelden kolumnar epitele geçiştir (bronşun tam tersi yönde).", "isKey": True},
                    {"title": "Asit Dayanıklılığı", "desc": "Müsin salgılayan kolumnar hücreler mide asidine karşı doğal koruma sağlar.", "isKey": True},
                    {"title": "Endoskopik Görünüm", "desc": "Sedefsi beyaz yassı epitel yerine somon kırmızısı kadifemsi kolumnar mukoza izlenir.", "isKey": False}
                ],
                "table": {
                    "title": "Bronş Metaplazisi ve Barrett Özofagusu Karşılaştırması",
                    "headers": ["Parametre", "Bronş Metaplazisi", "Barrett Özofagusu"],
                    "rows": [
                        ["Orijinal Epitel", "Kolumnar siliyalı epitel", "Çok katlı yassı epitel"],
                        ["Metaplastik Epitel", "Çok katlı yassı (skuamöz)", "İntestinal tip kolumnar epitel"],
                        ["Tetikleyici Stres", "Sigara dumanı toksisitesi", "Mide asidi ve safra reflüsü"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Barrett özofagusu kronik reflüye bağlı olarak çok katlı yassı epitelin kolumnar epitele dönüşmesidir.",
                "📌 [SINAV SPOTU] Bronşta kolumnardan skuamöze; Barrett özofagusunda ise skuamözden kolumnara metaplazi olur."
            ],
            "medicalTerms": [
                {"term": "Barrett Özofagusu", "explanation": "Distal özofagusta çok katlı yassı epitelin yerini kolumnar epitelin almasıyla oluşan metaplazidir."},
                {"term": "GÖRH", "explanation": "Mide içeriğinin özofagusa kaçarak mukozal hasar ve semptom oluşturmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Özofagus ile Barrett Özofagusu Karşılaştırması",
                    "Normal Distal Özofagus",
                    "Barrett Özofagusu (Metaplastik)",
                    [
                        "Sedefsi beyaz parlak mukoza",
                        "Non-keratinize çok katlı yassı epitel",
                        "Mide asidine karşı dayanıksız"
                    ],
                    [
                        "Somon pembesi/kırmızısı kadifemsi mukoza",
                        "Goblet hücreli intestinal kolumnar epitel",
                        "Asit ve safraya kimyasal olarak dirençli"
                    ]
                ),
                make_cloze(
                    "Kronik gastroözofageal reflüde distal özofagustaki çok katlı yassı epitelin yerini kolumnar epitelin almasına [Barrett] özofagusu denir.",
                    "Barrett",
                    "Metaplastik reflü hastalığı eponim adı"
                )
            ]
        },

        # Adım 77
        {
            "slideNumber": 77,
            "title": "Barrett Özofagusunda İntestinal Metaplazi: Goblet Hücrelerinin Tanısal Rolü",
            "subtitle": "Barrett tanısı için endoskopik şüphenin biyopside goblet hücreli intestinal metaplazi ile kanıtlanması şarttır.",
            "badge": "Histopatolojik Kriter",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Endoskopide alt özofagusta yukarı tırmanan somon kırmızısı diller görülmesi Barrett şüphesi doğurur; ancak kesin patolojik tanı için biyopsi zorunludur.

Uluslararası patoloji kriterlerine göre Barrett özofagusu tanısı koyabilmek için kolumnar epitel tabakası içinde **asit müsin içeren Goblet hücrelerinin (çanak hücreleri)** gösterilmesi şarttır. Bu histolojik tabloya **özofagusta intestinal metaplazi** adı verilir. Goblet hücreleri rutin Hematoksilen-Eozinde soluk mavi vakuolleriyle, Alcian Blue boyamasında ise parlak mavi renkle seçilir.

> [KLİNİK İPUCU] Biyopside goblet hücresi görülmeyen gastrik tip kolumnar epitel birçok kılavuzda gerçek Barrett sayılmaz; kanser riski goblet hücreli intestinal metaplazide yüksektir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Goblet Hücresi Şartı", "desc": "Müsin dolu kadeh hücresinin gösterilmesi Barrett'in altın standart tanı ölçütüdür.", "isKey": True},
                    {"title": "Alcian Blue Boyası", "desc": "Goblet hücrelerindeki asidik müsini parlak maviye boyayarak tanıyı kesinleştirir.", "isKey": True},
                    {"title": "İntestinal Tip", "desc": "İnce barsak benzeri epitel diferansiasyonu geliştiğini kanıtlar.", "isKey": False}
                ],
                "table": {
                    "title": "Barrett Özofagusunda Tanısal İpuçları",
                    "headers": ["Yöntem", "Gözlenen Özellik", "Tanısal Değeri"],
                    "rows": [
                        ["Endoskopi", "Gastroözofageal bileşkeden yukarı uzanan kırmızı mukoza", "Ön tanı ve biyopsi haritalama"],
                        ["Rutin H&E", "Kolumnar hücreler arasında şişkin müsin vakuollü hücreler", "Goblet hücresi varlığı"],
                        ["Alcian Blue (pH 2.5)", "Asit müsinin parlak turkuaz-mavi boyanması", "Goblet hücrelerinin histokimyasal teyidi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Barrett özofagusunun histopatolojik kesin tanısı için biyopside GOBLET HÜCRELERİNİN gösterilmesi şarttır.",
                "📌 [SINAV SPOTU] Alcian Blue boyası goblet hücrelerindeki asit müsini boyayarak Barrett tanısını doğrular."
            ],
            "medicalTerms": [
                {"term": "Goblet Hücresi", "explanation": "İnce ve kalın barsakta asidik müsin salgılayan şişkin kadeh biçimli epitel hücresidir."},
                {"term": "İntestinal Metaplazi", "explanation": "Özofagus veya mide epitelinin barsak tipi goblet hücreli epitele dönüşmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Gastroözofageal reflü şikayetiyle endoskopi yapılan bir hastanın distal özofagus biyopsisinde 'Barrett Özofagusu' tanısı koyabilmek için patoloğun mikroskop altında mutlaka görmesi gereken kilit hücre tipi hangisidir?",
                    {
                        "A": "Goblet hücreleri (Çanak hücreleri)",
                        "B": "Pariyetal hücreler",
                        "C": "Kupffer hücreleri",
                        "D": "Paneth hücreleri",
                        "E": "Langerhans hücreleri"
                    },
                    "A",
                    {
                        "A": "Doğru: Barrett özofagusu tanısı intestinal metaplazinin kanıtı olan goblet hücrelerinin varlığıyla konulur.",
                        "B": "Yanlış: Pariyetal hücreler mide korpusunda asit salgılar.",
                        "C": "Yanlış: Kupffer hücreleri karaciğer makrofajlarıdır.",
                        "D": "Yanlış: Paneth hücreleri ince barsak kript tabanında antibakteriyel enzim salgılar.",
                        "E": "Yanlış: Langerhans hücreleri epidermisteki dendritik antijen sunucu hücrelerdir."
                    }
                ),
                make_cloze(
                    "Barrett özofagusunun histopatolojik kesin tanısında kolumnar epitel arasında [goblet] hücrelerinin gösterilmesi altın standarttır.",
                    "goblet",
                    "Müsin salgılayan kadeh hücresi adı"
                )
            ]
        },

        # Adım 78
        {
            "slideNumber": 78,
            "title": "Servikal Transformasyon Zonunda Skuamöz Metaplazi: Fizyolojik vs Patolojik Süreç",
            "subtitle": "Uterin servikste endoservikal kolumnar epitelin vajinal asit etkisiyle yassılaşması fizyolojik bir adaptasyondur.",
            "badge": "Jinekolojik Metaplazi",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Metaplazinin jinekolojideki en önemli örneği **uterin servikste (rahim ağzı)** gerçekleşir. Ektoserviks çok katlı yassı epitel ile döşeliyken, endoservikal kanal tek katlı mukus salgılayan kolumnar epitel ile döşelidir.

Pubertede hormonal etkiyle endoservikal epitel dışarı doğru taşar (ektropiyon). Vajinanın laktobasillerce üretilen asidik ortamına (pH ~4.0) maruz kalan bu narin kolumnar epitel, kök hücrelerin reprogramlamasıyla basınca ve aside dayanıklı **çok katlı yassı epitele** dönüşür. Bu bölgeye **transformasyon zonu** adı verilir.

> [KLİNİK İPUCU] Servikal skuamöz metaplazi tamamen normal fizyolojik bir süreçtir; ancak bu zon HPV enfeksiyonuna ve serviks kanserine en duyarlı anatomik kavşaktır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Fizyolojik Süreç", "desc": "Vajinal asiditeye karşı endoservikal epitelin doğal korunma adaptasyonudur.", "isKey": True},
                    {"title": "Transformasyon Zonu", "desc": "Orijinal ve yeni skuamokolumnar bileşkeler arasında kalan metaplastik alandır.", "isKey": True},
                    {"title": "Kanserleşme Hassasiyeti", "desc": "Metaplastik olgunlaşmamış hücreler HPV enfeksiyonunun primer hedefidir.", "isKey": False}
                ],
                "table": {
                    "title": "Serviks Epitel Zonları",
                    "headers": ["Bölge", "Normal Epitel Tipi", "Klinik / Patolojik Önemi"],
                    "rows": [
                        ["Ektoserviks", "Non-keratinize çok katlı yassı epitel", "Vajinal sürtünmeye dayanıklı"],
                        ["Endoserviks", "Tek katlı müsinöz kolumnar epitel", "Servikal mukus salgısı"],
                        ["Transformasyon Zonu", "Skuamöz metaplazik epitel", "Serviks kanseri ve CIN lezyonlarının çıktığı ana odak"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Servikal transformasyon zonundaki skuamöz metaplazi vajina asidine karşı gelişen FİZYOLOJİK bir metaplazidir.",
                "🚨 [KRİTİK UYARI] Serviks kanseri öncülü displaziler (CIN) neredeyse istisnasız olarak transformasyon zonundan köken alır."
            ],
            "medicalTerms": [
                {"term": "Transformasyon Zonu", "explanation": "Servikste endoservikal kolumnar epitelin skuamöz metaplaziye uğradığı dinamik bölgedir."},
                {"term": "Ektropiyon", "explanation": "Endoservikal mukozanın dışarı ektoservikse doğru taşması durumudur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Servikal Pap smear taramalarında patoloğun smearin 'yeterli' olduğunu söyleyebilmesi için preparatta mutlaka transformasyon zonunu temsil eden hangi hücre grubunu görmesi gerekir?",
                    {
                        "A": "Endoservikal kolumnar hücreler veya metaplastik skuamöz hücreler",
                        "B": "Yalnızca anükleer keratin pulları",
                        "C": "Yoğun polimorfonükleer lökosit kümeleri",
                        "D": "Çizgili kas lifleri ve miyosit nükleusları",
                        "E": "Tiroid folikül epitel hücreleri"
                    },
                    "A",
                    {
                        "A": "Doğru: Transformasyon zonu metaplastik hücreler ve endoservikal hücrelerle temsil edilir; kanser taraması için şarttır.",
                        "B": "Yanlış: Anükleer keratin aşırı hiperkeratoz bulgusudur.",
                        "C": "Yanlış: Lökositler inflamasyonu gösterir, yeterlilik kriteri değildir.",
                        "D": "Yanlış: Servikste çizgili kas bulunmaz.",
                        "E": "Yanlış: Tiroid hücresi servikste bulunmaz."
                    }
                ),
                make_cloze(
                    "Servikste kolumnar epitelin vajina asidine maruz kalarak skuamöz metaplaziye uğradığı dinamik bölgeye [transformasyon] zonu adı verilir.",
                    "transformasyon",
                    "Metaplastik servikal zon adı"
                )
            ]
        },

        # Adım 79 (CHECKPOINT 8)
        {
            "slideNumber": 79,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Epitelyal Metaplazi ve Kök Hücre Biyolojisi",
            "subtitle": "Metaplazi kavramını, kök hücre reprogramlamasını, bronş, Barrett ve serviks modellerini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 8,
            "synthesisNarrative": """Bu bölümde bir olgun hücre tipinin diğerine dönüşümü olan metaplaziyi, kök hücre reprogramlama mekanizmasını ve klasik epitelyal modelleri inceledik.

Metaplazi olgun hücrelerin değil, doku kök hücrelerinin yeni yönde farklılaşmasıdır. Sigara içenlerde bronşta siliyalı kolumnar epitel çok katlı yassı epitele döner; mukosiliyer klirens kaybolur. Reflüde özofagusta yassı epitel goblet hücreli kolumnar epitele (Barrett) döner. A vitamini eksikliği yaygın skuamöz metaplazi yaparken; servikal transformasyon zonundaki yassılaşma fizyolojik adaptasyondur.

> [TEKRAR SPOTU] Metaplazi uyaran kesildiğinde geri dönebilen bir adaptasyondur; ancak kronikleştiğinde neoplaziye giden yolda ilk basamak olabilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kök Hücre Temeli", "desc": "Metaplazi transdiferensiasyon değil, kök hücrelerin transkripsiyonel reprogramlamasıdır.", "isKey": True},
                    {"title": "Yön Farklılıkları", "desc": "Bronşta kolumnar -> yassı; Barrett özofagusunda yassı -> kolumnar dönüşüm.", "isKey": True},
                    {"title": "Tanısal İmzalar", "desc": "Barrett için goblet hücresi ve Alcian blue pozitifliği zorunludur.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 8 Sentez Tablosu",
                    "headers": ["Klinik Model", "Dönüşüm Yönü", "Temel Tanısal / Klinik Özellik"],
                    "rows": [
                        ["Sigara Bronşu", "Kolumnar -> Skuamöz", "Mukosiliyer temizlenme kaybı, enfeksiyon riski"],
                        ["Barrett Özofagusu", "Skuamöz -> Kolumnar", "Goblet hücresi şartı, adenokarsinom öncülü"],
                        ["Servikal Zon", "Kolumnar -> Skuamöz", "Vajinal aside fizyolojik adaptasyon, HPV odağı"],
                        ["A Vitamini Eksikliği", "Kolumnar -> Skuamöz", "Kseroftalmi, Bitot lekeleri, mesane metaplazisi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Metaplazi kök hücrelerin yeniden programlanmasıyla gerçekleşir.",
                "📌 [SINAV SPOTU] Barrett özofagusu tanısı için intestinal tip GOBLET hücrelerinin görülmesi şarttır."
            ],
            "medicalTerms": [
                {"term": "Metaplazi", "explanation": "Bir olgun hücre tipinin yerini başka bir olgun hücre tipinin almasıdır."},
                {"term": "Barrett Özofagusu", "explanation": "Kronik reflüde alt özofagusta gelişen goblet hücreli kolumnar metaplazidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc22",
                    "Metaplazinin hücresel oluşum mekanizması nedir; olgun hücreler doğrudan birbirine dönüşür mü?",
                    "Hayır; olgun hücreler doğrudan dönüşmez. Doku kök hücreleri veya indiferansiye rezerv hücreler yeni transkripsiyon faktörleriyle yeniden programlanarak farklı bir hücre tipine olgunlaşır."
                ),
                make_flashcard(
                    "k1-03-fc23",
                    "Sigara içicisinin bronşundaki skuamöz metaplazi ile reflü hastasının özofagusundaki Barrett metaplazisinin dönüşüm yönü farkı nedir?",
                    "Bronşta narin siliyalı kolumnar epitel dumana dayanıklı çok katlı yassı epitele döner; Barrett özofagusunda ise yassı epitel aside dayanıklı goblet hücreli kolumnar epitele döner."
                ),
                make_flashcard(
                    "k1-03-fc24",
                    "Barrett özofagusu tanısı koyabilmek için biyopside mutlaka gösterilmesi gereken anahtar hücre ve histokimyasal boya hangisidir?",
                    "İntestinal metaplaziyi kanıtlayan asit müsin dolu Goblet hücreleridir; Alcian Blue boyası ile parlak mavi renkte doğrulanır."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Skuamöz metaplaziye uğramış bir bronş epiteli sigara dumanının fiziksel ve kimyasal travmasına daha dayanıklı olduğu halde hasta neden daha sık pnömoni (zatürre) geçirir?",
                    "Çünkü metaplastik yassı epitelde mukus üreten goblet hücreleri ve partikülleri süpüren siliyalar yoktur; mukosiliyer klirens felç olduğundan solunan mikroorganizmalar temizlenemez."
                )
            ]
        }
    ]
