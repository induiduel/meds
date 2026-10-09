#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 7: Atrofinin Hücresel Mekanizmaları: Ubikuitin-Proteazom ve Protein Yıkımı (Adımlar 60 - 69)
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
        # Adım 60
        {
            "slideNumber": 60,
            "title": "Atrofinin Biyokimyasal Temeli: Protein Sentezi Azalması ve Yıkım Artışı",
            "subtitle": "Atrofi temelde protein sentezinin azalması ve protein yıkım hızının artması arasındaki dengesizliktir.",
            "badge": "Biyokimyasal Denge",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücre kütlesi protein sentezi ile protein degradasyonu (yıkımı) arasındaki hassas dengeye dayanır. Atrofinin temel biyokimyasal mekanizması bu terazinin bozulmasıdır: **Protein sentez hızı düşerken, protein yıkım hızı katlanarak artar**.

Azalan metabolik aktivite, besin yokluğu veya trofik sinyal eksikliği protein translasyonunu durdurur. Eşzamanlı olarak hücre içi proteolitik sistemler aktive olarak var olan yapısal proteinleri hızla parçalar. Sonuçta hücre yapı taşlarını kaybederek küçülür.

> [TEMEL İLKE] Atrofi iki yönlü bir biyokimyasal krizdir: Azalmış anabolizma (sentez) ve artmış katabolizma (yıkım).""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Düşük Sentez", "desc": "Trofik sinyal ve besin azlığı nedeniyle ribozomal protein yapımı yavaşlar.", "isKey": True},
                    {"title": "Yüksek Katabolizma", "desc": "Ubikuitin-proteazom ve lizozomal yolaklar proteinleri hızla yıkar.", "isKey": True},
                    {"title": "Net Kütle Kaybı", "desc": "Sentezlenen protein miktarı yıkılanın çok altında kaldığından hücre hacmi küçülür.", "isKey": False}
                ],
                "table": {
                    "title": "Hücresel Protein Dengesi ve Atrofi",
                    "headers": ["Durum", "Protein Sentezi", "Protein Yıkımı", "Net Hücresel Sonuç"],
                    "rows": [
                        ["Homeostaz (Normal)", "Dengeli", "Dengeli", "Sabit hücre boyutu"],
                        ["Hipertrofi", "Belirgin artmış", "Normal / düşük", "Hücre boyutunda büyüme"],
                        ["Atrofi", "Belirgin azalmış", "Belirgin artmış", "Hücre boyutunda küçülme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofinin biyokimyasal mekanizması protein sentezinin azalması ve protein yıkımının artmasıdır.",
                "📌 [SINAV SPOTU] Atrofide hücre proteinlerini yıkan temel yolak ubikuitin-proteazom yolağıdır."
            ],
            "medicalTerms": [
                {"term": "Katabolizma", "explanation": "Büyük karmaşık moleküllerin parçalanarak daha küçük bileşenlere ve enerjiye dönüştürülmesidir."},
                {"term": "Proteoliz", "explanation": "Proteinlerin enzimler aracılığıyla peptid ve amino asitlere hidroliz edilerek yıkılmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Atrofiye uğrayan bir hücrede hücresel kütle kaybına yol açan temel biyokimyasal dengesizlik hangisidir?",
                    {
                        "A": "Protein sentezinin azalması ve protein yıkım hızının artması",
                        "B": "Hücre içi kalsiyum depolarının aşırı dolması ve kristalleşmesi",
                        "C": "DNA replikasyonunun durmaksızın hızlanması",
                        "D": "Lipid sentezinin protein sentezini tamamen baskılaması",
                        "E": "Mitokondrilerin devasa füzyonla dev mitokondriye dönüşmesi"
                    },
                    "A",
                    {
                        "A": "Doğru: Atrofinin moleküler temeli sentez azalması ile yıkım artışının birlikteliğidir.",
                        "B": "Yanlış: Kalsiyum birikimi nekroz ve distrofik kalsifikasyonda görülür.",
                        "C": "Yanlış: DNA replikasyonu hiperplaziye aittir, atrofide durur.",
                        "D": "Yanlış: Atrofide genel katabolizma vardır.",
                        "E": "Yanlış: Atrofide mitokondriler otofajiyle parçalanır."
                    }
                ),
                make_cloze(
                    "Atrofi sürecinde hücre kütlesinin azalması temel olarak protein sentezinin azalması ve protein [yıkımının] artmasıyla gerçekleşir.",
                    "yıkımının",
                    "Degradasyon süreci terimi"
                )
            ]
        },

        # Adım 61
        {
            "slideNumber": 61,
            "title": "Metabolik Baskılanma ve Azalmış Hücresel Enerji Tüketimi",
            "subtitle": "Atrofik hücre bazal metabolizmasını kısarak sınırlı enerji kaynaklarıyla yaşamını korur.",
            "badge": "Enerji Tasarrufu",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atrofi sadece bir küçülme değil, planlı bir **metabolik kısıtlama stratejisidir**. Kaynakların yetersiz olduğu bir ortamda hücre normal metabolik hızını sürdürmeye kalkarsa hızla ATP tükenmesi yaşar ve ölür.

Hücre bu tehlikeyi önlemek için iyon pompalarının hızını düşürür, ribozomal translasyonu kısıtlar ve bazal oksijen tüketimini minimuma indirir. Bu metabolik uyku benzeri adaptasyon sayesinde hücre hasar görmeden yeni bir denge düzeyine çekilir.

> [TEMEL İLKE] Atrofi, yetersiz besin ortamında hücrenin canlı kalabilmek için enerji harcamasını tabana indirmesidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Enerji Tasarrufu", "desc": "Bazal metabolizma hızı düşürülerek kıt kaynaklar verimli kullanılır.", "isKey": True},
                    {"title": "Azalmış Oksijen İhtiyacı", "desc": "Küçülen hücre çok daha az kan akımıyla canlılığını koruyabilir.", "isKey": True},
                    {"title": "Düşük Profil", "desc": "Özelleşmiş lüks fonksiyonlar durdurulur; sadece hayatta kalma fonksiyonları çalışır.", "isKey": False}
                ],
                "table": {
                    "title": "Normal vs Atrofik Hücre Metabolizması",
                    "headers": ["Fonksiyon", "Normal Hücre", "Atrofik Hücre"],
                    "rows": [
                        ["Oksijen Tüketimi", "Yüksek / fizyolojik", "Belirgin düşmüş (bazal)"],
                        ["Protein Translasyonu", "Sürekli ve aktif", "Minimum düzeyde baskılanmış"],
                        ["Enerji Dengesi", "Üretim = Geniş tüketim", "Düşük üretim = Kısıtlı tüketim"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofik hücre metabolik hızını düşürerek azalan kan akımına ve besine uyum sağlar.",
                "🚨 [KRİTİK UYARI] Metabolik kısıtlama fonksiyonel kapasiteyi düşürür; atrofik organ normal işlevini tam verimle yapamaz."
            ],
            "medicalTerms": [
                {"term": "Bazal Metabolizma", "explanation": "Hücrenin hiçbir fazladan iş yapmadan yalnızca canlı kalabilmesi için gereken minimum enerji düzeyidir."},
                {"term": "Metabolik Kısıtlama", "explanation": "Kıtlık karşısında hücrenin ATP tüketen lüks süreçleri kapatmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal ve Atrofik Hücrenin Enerji Dengesi",
                    "Normal Hücre Metabolizması",
                    "Atrofik Hücre Metabolizması",
                    [
                        "Geniş oksijen ve glukoz tüketimi",
                        "Aktif iyon pompaları ve salgı işlevi",
                        "Sürekli yapısal protein sentezi"
                    ],
                    [
                        "Minimuma indirilmiş oksijen tüketimi",
                        "Yalnızca canlılığı sürdüren bazal pompalar",
                        "Sentez durdurulmuş, yıkım kontrollü"
                    ]
                ),
                make_active_recall(
                    "İskemiye uğrayan bir böbrek tübül hücresinin doğrudan nekroza gitmek yerine atrofiye uğramasının hücresel avantajı nedir?",
                    "Hücre boyutunu ve metabolik hızını küçülterek oksijen ihtiyacını mevcut kısıtlı kan akımının karşılayabileceği düzeye indirir ve hayatta kalır."
                )
            ]
        },

        # Adım 62
        {
            "slideNumber": 62,
            "title": "Ubikuitin-Proteazom Yolağı: Proteinlerin Kovalent İşaretlenmesi",
            "subtitle": "Sitoplazmik ve nükleer proteinlerin hedeflenmiş yıkımı ubikuitin proteiniyle işaretlenerek yürütülür.",
            "badge": "Yıkım Yolağı",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atrofi sırasında yapısal proteinlerin yıkılmasından sorumlu ana moleküler mekanizma **ubikuitin-proteazom yolağıdır**. Bu yolak sitozolik ve nükleer proteinlerin hedeflenmiş parçalanmasını sağlar.

Parçalanacak hedef proteinler önce küçük bir polipeptid olan **ubikuitin** molekülleriyle kovalent olarak etiketlenir. Protein üzerine arka arkaya çok sayıda ubikuitin eklenmesiyle (**poliubikuitinasyon**) bir 'ölüm işareti' oluşturulur. Bu etiket proteini doğrudan hücresel öğütücü olan proteazoma yönlendirir.

> [TEMEL İLKE] Ubikuitin bir hücresel imha etiketidir; poliubikuitinlenen proteinler kaçınılmaz olarak proteazomda parçalanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Ubikuitin Etiketi", "desc": "76 amino asitlik küçük koruyucu protein hedef proteine kovalent bağlanır.", "isKey": True},
                    {"title": "Poliubikuitinasyon", "desc": "Proteazom tarafından tanınabilmek için en az 4 adet ubikuitin zinciri gerekir.", "isKey": True},
                    {"title": "Hassas Seçicilik", "desc": "Rastgele yıkım olmaz; yalnızca işaretlenmiş hasarlı veya fazla proteinler yıkılır.", "isKey": False}
                ],
                "table": {
                    "title": "Ubikuitinasyonun Temel Aşamaları",
                    "headers": ["Basamak", "Moleküler Olay", "Sonuç"],
                    "rows": [
                        ["Ubikuitin Aktivasyonu", "ATP harcanarak E1 enzimine bağlanma", "Aktif ubikuitin oluşumu"],
                        ["Konjugasyon", "E2 taşıyıcı enzimine aktarım", "Hedefe transfer hazırlığı"],
                        ["Ligasyon", "E3 ligaz ile hedef proteine kovalent bağ", "Poliubikuitin etiketi tamamlanması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofide hücresel proteinlerin hızlanmış yıkımından sorumlu temel yolak ubikuitin-proteazom yolağıdır.",
                "📌 [SINAV SPOTU] Hedef proteinin proteazom tarafından tanınması için poliubikuitin zinciriyle işaretlenmesi şarttır."
            ],
            "medicalTerms": [
                {"term": "Ubikuitin", "explanation": "Yıkılacak proteinlere kovalent bağlanarak onları proteazoma yönlendiren küçük düzenleyici proteindir."},
                {"term": "Poliubikuitinasyon", "explanation": "Hedef protein üzerinde ardışık ubikuitin zinciri kurularak yıkım sinyali verilmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Ubikuitinasyon ve Protein İşaretleme Adımları",
                    [
                        "1. Atrofi Sinyali: Besin veya hormon eksikliğiyle katabolik sinyallerin artması.",
                        "2. E1 Aktivasyonu: ATP harcanarak ubikuitinin aktive edici enzime bağlanması.",
                        "3. E2 Transferi: Ubikuitinin konjuge edici enzim üzerine aktarılması.",
                        "4. E3 Tanıması: E3 ligazın hedef kas proteinini (aktin/miyozin) özgül olarak tanıması.",
                        "5. Kovalent Etiketleme: Hedef proteinin lizin kalıntılarına poliubikuitin zincirinin takılması."
                    ]
                ),
                make_cloze(
                    "Atrofide parçalanacak hücresel proteinlerin proteazoma yönlendirilmesi için kovalent olarak bağlanan küçük proteine [ubikuitin] adı verilir.",
                    "ubikuitin",
                    "Proteazom yıkım etiketi molekülü"
                )
            ]
        },

        # Adım 63
        {
            "slideNumber": 63,
            "title": "Ubikuitin Ligazlar: E1, E2 ve E3 Enzim Kaskadı",
            "subtitle": "Protein işaretleme işlemi üç kademeli hiyerarşik enzim kaskadı tarafından kusursuz yürütülür.",
            "badge": "Enzim Kaskadı",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Ubikuitinasyon rastgele bir süreç değildir; üç enzimli hiyerarşik bir sistem tarafından yönetilir: **E1 (aktive edici enzim)**, **E2 (konjuge edici enzim)** ve **E3 (ubikuitin ligaz)**.

E1 ubikuitini ATP harcayarak aktive eder; ardından bu ubikuitin E2 enzimine devredilir. Kaskadın en kritik ve özgül basamağı **E3 ubikuitin ligazdır**. Hücrede yüzlerce farklı E3 ligaz bulunur ve her biri hangi proteinin parçalanacağını tayin eden özgül tanılayıcıdır.

> [TEMEL İLKE] E3 ligazlar, binlerce hücresel protein arasından hangisinin yıkılacağını belirleyen hedefleme dedektifleridir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "E1 (Aktive Edici)", "desc": "ATP bağımlı çalışır; tüm sistem için ubikuitinleri aktif hale getirir.", "isKey": True},
                    {"title": "E2 (Konjuge Edici)", "desc": "Aktif ubikuitini E1'den alarak E3 kompleksine taşır.", "isKey": True},
                    {"title": "E3 (Ligaz)", "desc": "Substratı özgül olarak tanır ve ubikuitini hedef proteine kovalent bağlar.", "isKey": False}
                ],
                "table": {
                    "title": "Ubikuitin Enzim Kaskadı Bileşenleri",
                    "headers": ["Enzim", "Enzim Adı", "Temel Biyolojik Görevi"],
                    "rows": [
                        ["E1", "Ubikuitin Aktive Edici Enzim", "ATP ile ubikuitini yüksek enerjili tiyoester bağıyla bağlama"],
                        ["E2", "Ubikuitin Konjuge Edici Enzim", "Ubikuitini E1'den E3 ligaza taşıma"],
                        ["E3", "Ubikuitin Ligaz", "Hedef substratı spesifik tanıyıp ubikuitini proteine transfer etme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Ubikuitin kaskadında substrat özgüllüğünü sağlayan ve hedef proteini tanıyan enzim E3 ubikuitin ligazdır.",
                "📌 [SINAV SPOTU] E1 enzimi ATP harcayarak ubikuitini aktive eder."
            ],
            "medicalTerms": [
                {"term": "E3 Ubikuitin Ligaz", "explanation": "Yıkılacak hedef proteini spesifik olarak tanıyıp üzerine ubikuitin bağlayan enzimdir."},
                {"term": "Substrat Özgüllüğü", "explanation": "Bir enzimin binlerce molekül arasından yalnızca kendi hedefini seçebilme yeteneğidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Ubikuitin-proteazom sisteminde parçalanacak hedef proteini doğrudan ve spesifik olarak tanıyan ve ubikuitinin proteine transferini katalizleyen anahtar enzim hangisidir?",
                    {
                        "A": "E3 ubikuitin ligaz",
                        "B": "E1 aktive edici enzim",
                        "C": "E2 konjuge edici enzim",
                        "D": "DNA polimeraz delta",
                        "E": "Alkalen fosfataz"
                    },
                    "A",
                    {
                        "A": "Doğru: E3 ligaz substrat özgüllüğünü sağlayan ve hedefi tanıyan anahtar enzimdir.",
                        "B": "Yanlış: E1 genel aktivasyon yapar, hedef tanımaz.",
                        "C": "Yanlış: E2 ara taşıyıcıdır.",
                        "D": "Yanlış: DNA polimeraz replikasyon enzimidir.",
                        "E": "Yanlış: Alkalen fosfataz fosfat koparır."
                    }
                ),
                make_cloze(
                    "Ubikuitin-proteazom kaskadında parçalanacak hedef proteini spesifik olarak tanıyan enzim [E3] ubikuitin ligazdır.",
                    "E3",
                    "Özgüllük sağlayan ligaz enzimi numarası"
                )
            ]
        },

        # Adım 64
        {
            "slideNumber": 64,
            "title": "Kas Atrofisinde E3 Ligazların Rolü: MuRF1 ve Atrogin-1 Aktivasyonu",
            "subtitle": "İskelet kası atrofisinde kas-özgül E3 ligazlar olan MuRF1 ve Atrogin-1 genleri hızla indüklenir.",
            "badge": "Kas Atrofisi",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """İskelet kası atrofisinin (alçı, açlık, denervasyon, kaşeksi) moleküler mekanizması aydınlatıldığında, iki özgül E3 ligaz geninin aşırı aktive olduğu saptanmıştır: **MuRF1** (Muscle RING Finger 1) ve **Atrogin-1** (MAFbx).

Bu enzimler 'atrojenler' olarak adlandırılır. İnaktif kaslarda veya glukokortikoid/TNF-α uyarımında transkripsiyonları hızla artar. MuRF1 doğrudan sarkomerik kontraktil proteinleri (**miyozin ağır zinciri, aktin, troponin**) tanıyarak etiketler ve hızla yıkılmalarını sağlar.

> [KLİNİK İPUCU] MuRF1 ve Atrogin-1 aktivasyonu iskelet kası erimesinin doğrudan biyokimyasal tetikleyicisidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Atrojen Genler", "desc": "MuRF1 ve Atrogin-1 kas dokusuna özgü E3 ubikuitin ligazlardır.", "isKey": True},
                    {"title": "Miyofilament Hedefleme", "desc": "MuRF1 doğrudan miyozin ağır zincirini ve titini etiketleyerek yıktırır.", "isKey": True},
                    {"title": "Transkripsiyonel Tetik", "desc": "FoxO transkripsiyon faktörleri atrojen genlerini güçlü şekilde aktive eder.", "isKey": False}
                ],
                "table": {
                    "title": "Kas Özgül E3 Ligazlar ve Hedefleri",
                    "headers": ["E3 Ligaz", "Aktive Eden Uyaran", "Yıktığı Hedef Proteinler"],
                    "rows": [
                        ["MuRF1", "İmmobilizasyon, denervasyon, glukokortikoid", "Miyozin ağır zinciri, miyozin bağlayıcı protein C"],
                        ["Atrogin-1 (MAFbx)", "Açlık, kaşeksi, sepsis", "MyoD transkripsiyon faktörü, eIF3f (protein sentez faktörü)"],
                        ["FoxO Faktörleri", "Akt yolağının baskılanması", "MuRF1 ve Atrogin-1 genlerinin promotör aktivasyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kas atrofisinde yapısal miyofibrilleri yıkan kas-özgül E3 ubikuitin ligazlar MuRF1 ve Atrogin-1'dir.",
                "📌 [SINAV SPOTU] FoxO transkripsiyon faktörleri kas atrofisinde MuRF1 ve Atrogin-1 ekspresyonunu artırır."
            ],
            "medicalTerms": [
                {"term": "MuRF1", "explanation": "İskelet kasında miyozin ağır zincirini parçalanmak üzere etiketleyen kas-özgül E3 ligazdır."},
                {"term": "Atrogin-1", "explanation": "Açlık ve kaşekside kas protein sentez inhibitörlerini ve proteinleri yıkan E3 ligazdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kas Atrofisinde MuRF1 Aracılı Yıkım Kaskadı",
                    [
                        "1. Hareketsizlik/Açlık: İnsülin/IGF-1 sinyalinin düşmesi ve Akt kinazın susması.",
                        "2. FoxO Aktivasyonu: Baskılanamayan FoxO transkripsiyon faktörlerinin nükleusa girmesi.",
                        "3. Atrojen İndüksiyonu: MuRF1 ve Atrogin-1 mRNA sentezinin katlanarak artması.",
                        "4. Miyozin İşaretleme: MuRF1'in sarkomerdeki miyozin ağır zincirine ubikuitin takması.",
                        "5. Lif Erimesi: Kasılma proteinlerinin parçalanmasıyla kas kütlesinin hızla erimesi."
                    ]
                ),
                make_cloze(
                    "İskelet kası atrofisinde miyozin ağır zincirini ubikuitinleyerek yıkıma yönlendiren kas-özgül E3 ligaza [MuRF1] adı verilir.",
                    "MuRF1",
                    "Kas-özgül E3 ligaz kısaltması"
                )
            ]
        },

        # Adım 65
        {
            "slideNumber": 65,
            "title": "26S Proteazom Kompleksinde Yapısal Kas Proteinlerinin Yıkımı",
            "subtitle": "Poliubikuitinle işaretlenen proteinler devasa 26S proteazom silindirinde amino asitlere parçalanır.",
            "badge": "Hücresel Öğütücü",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Poliubikuitin etiketi takılmış proteinlerin nihai durağı **26S Proteazom kompleksidir**. Proteazom, sitoplazmada ve çekirdekte serbestçe bulunan varil şeklinde devasa bir proteolitik enzim makinesidir.

Kompleks, ortada proteinleri kesen **20S çekirdek silindiri** ve iki ucunda bekçilik yapan **19S düzenleyici kapaklardan** oluşur. 19S kapağı poliubikuitin etiketini tanır, ubikuitinleri geri dönüşüm için ayırır, proteini ATP harcayarak açar (unfolding) ve 20S tüneline sokar. İçerideki proteazlar proteini küçük peptitlere ve amino asitlere dilimler.

> [TEMEL İLKE] 26S proteazom, işaretlenmiş proteinleri hücreye zarar vermeden kontrollü biçimde amino asitlere dönüştüren hücresel geri dönüşüm merkezidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "19S Kapak", "desc": "Ubikuitini tanır, proteini çözer ve 20S iç tüneline iter.", "isKey": True},
                    {"title": "20S Çekirdek", "desc": "Katalitik proteaz aktivitesiyle peptit bağlarını hızla keser.", "isKey": True},
                    {"title": "Amino Asit Kazanımı", "desc": "Parçalanan proteinlerden çıkan amino asitler enerji veya temel sentezler için kullanılır.", "isKey": False}
                ],
                "table": {
                    "title": "26S Proteazom Mimarisi",
                    "headers": ["Bölüm", "Yapısal Form", "Fonksiyonel Görev"],
                    "rows": [
                        ["19S Düzenleyici Kapak", "Halka şeklinde regülatör kompleks", "Etiketi tanıma, de-ubikuitinasyon, ATP ile protein açma"],
                        ["20S Katalitik Silindir", "Dört halkalı silindirik fıçı", "Kimotripsin benzeri, tripsin benzeri proteolitik kesim"],
                        ["Çıkış Ürünleri", "Kısa oligopeptitler (6-12 aa)", "Sitozolik peptidazlarla serbest amino asitlere ayrılma"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] 26S proteazom, poliubikuitinlenmiş proteinleri ATP bağımlı olarak parçalayan hücresel komplekstir.",
                "📌 [SINAV SPOTU] Proteazom inhibitörleri (örneğin bortezomib) multipl miyelom tedavisinde protein yıkımını engelleyerek etki eder."
            ],
            "medicalTerms": [
                {"term": "26S Proteazom", "explanation": "İşaretli proteinleri peptitlere parçalayan ATP bağımlı silindirik çok alt birimli enzim kompleksidir."},
                {"term": "20S Çekirdek", "explanation": "Proteazomun proteolitik kesim yapan iç aktif tünel kısmıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Poliubikuitin zinciriyle işaretlenmiş kas proteinlerinin girerek küçük peptit parçalarına ve amino asitlere hidrolize edildiği silindirik hücresel kompleks hangisidir?",
                    {
                        "A": "26S Proteazom",
                        "B": "Mitokondri iç zarı",
                        "C": "Sentrozom sentriyolü",
                        "D": "Peroksizom kristali",
                        "E": "Nükleolus granüler zonu"
                    },
                    "A",
                    {
                        "A": "Doğru: 26S proteazom ubikuitinli proteinleri yıkan ana hücresel komplekstir.",
                        "B": "Yanlış: Mitokondri ATP üretir.",
                        "C": "Yanlış: Sentrozom iğ ipliği organize eder.",
                        "D": "Yanlış: Peroksizom yağ asidi okside eder.",
                        "E": "Yanlış: Nükleolus ribozom alt birimi yapar."
                    }
                ),
                make_cloze(
                    "Ubikuitinle işaretlenen proteinleri ATP harcayarak peptitlere parçalayan silindirik enzimatik komplekse [26S proteazom] adı verilir.",
                    "26S proteazom",
                    "Hücresel yıkım kompleksi adı"
                )
            ]
        },

        # Adım 66
        {
            "slideNumber": 66,
            "title": "Lizozomal Enzimler ve Asit Hidrolazların Rolü",
            "subtitle": "Proteazom dışındaki hücresel organeller ve membran bileşenleri lizozomal asit hidrolazlarla sindirilir.",
            "badge": "Lizozomal Yıkım",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Ubikuitin-proteazom sistemi esas olarak serbest sitoplazmik ve nükleer proteinleri parçalarken; hücre içi organeller, membran parçaları ve ekstrasellüler materyal **lizozomlar** tarafından sindirilir.

Atrofi sırasında hücre zarı parçaları ve fonksiyon dışı kalan mitokondriler otofaji yoluyla lizozomlara aktarılır. Lizozomun asidik lümeninde (pH ~4.5-5.0) çalışan **asit hidrolazlar** (katepsinler, nükleazlar, lipazlar) bu makromolekülleri sindirerek hücreye yapı taşı sağlar.

> [TEMEL İLKE] Proteazom proteinleri tek tek parçalarken; lizozomlar organelleri ve membran komplekslerini topluca sindirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Asit Hidrolazlar", "desc": "Düşük pH'da çalışan katepsin ve hidrolaz enzimleri makromolekülleri yıkar.", "isKey": True},
                    {"title": "Organel Sindirimi", "desc": "Mitokondri ve endoplazmik retikulum lizozom içinde parçalanır.", "isKey": True},
                    {"title": "İki Yıkım Sistemi", "desc": "Ubikuitin-proteazom ve lizozom sistemleri atrofide senkronize çalışır.", "isKey": False}
                ],
                "table": {
                    "title": "Proteazom ve Lizozom Sistemlerinin Karşılaştırması",
                    "headers": ["Özellik", "Ubikuitin-Proteazom Yolağı", "Lizozomal Sistem"],
                    "rows": [
                        ["Yıktığı Substrat", "Tek tek proteinler (miyofilamentler)", "Tüm organeller, membranlar, glikojen"],
                        ["İşaretleme Şartı", "Poliubikuitinasyon zorunlu", "Otofagozom kılıfı veya endositoz"],
                        ["Çalışma Ortamı", "Nötral sitozol ve nükleus", "Asidik lizozom içi (pH 4.5-5.0)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofide sitozolik proteinleri proteazom, organel ve membranları lizozomlar yıkar.",
                "📌 [SINAV SPOTU] Lizozomal katepsinler asidik pH'da çalışan temel proteolitik enzimlerdir."
            ],
            "medicalTerms": [
                {"term": "Asit Hidrolaz", "explanation": "Lizozomun asidik ortamında aktif olan ve biyolojik molekülleri parçalayan enzimlerdir."},
                {"term": "Katepsin", "explanation": "Lizozom içinde proteinleri sindiren asit proteaz ailesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Ubikuitin-Proteazom ile Lizozomal Yıkım Karşılaştırması",
                    "Ubikuitin-Proteazom Yolağı",
                    "Lizozomal Asit Hidrolaz Yolağı",
                    [
                        "Yalnızca tekil proteinleri yıkar",
                        "Nötral sitozolde ATP ile çalışır",
                        "Poliubikuitin etiketi gerektirir"
                    ],
                    [
                        "Bütün organel ve membranları yıkar",
                        "Asidik lümende hidrolazlarla çalışır",
                        "Otofajik vakuol füzyonu ile çalışır"
                    ]
                ),
                make_active_recall(
                    "Atrofiye giren bir hücrede mitokondri ve ribozom gibi organellerin parçalanması neden proteazomda değil lizozomda gerçekleşir?",
                    "Çünkü proteazom dar bir silindirdir ve yalnızca çözünmüş tekil protein zincirlerini alabilir; koca bir mitokondri veya membran kompleksi ancak otofaji yoluyla lizozom içine alınarak sindirilebilir."
                )
            ]
        },

        # Adım 67
        {
            "slideNumber": 67,
            "title": "Kahverengi Atrofi (Brown Atrophy): Lipofuksin Pigmenti Birikimi",
            "subtitle": "Lizozomlarda sindirilemeyen lipid peroksidasyon kalıntıları birikerek dokuyu kahverengine boyar.",
            "badge": "Aşınma Pigmenti",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atrofi sırasında lizozomal otofaji ile hücre organelleri sindirilirken, bazı doymamış lipid kalıntıları enzimlerce tamamen parçalanamaz. Bu sindirilemeyen fosfolipid ve protein polimerleri peroksidasyona uğrayarak lizozom içinde çöker ve **lipofuksin pigmentine (yaşlılık / aşınma pigmenti)** dönüşür.

Özellikle yaşlı veya kaşektik bireylerin kalp ve karaciğerinde atrofiye yoğun lipofuksin birikimi eşlik eder. Organ makroskopik olarak belirgin biçimde küçülürken rengi koyu kahverengi-çikolata tonu alır. Bu duruma patolojide **kahverengi atrofi (brown atrophy)** adı verilir.

> [KLİNİK İPUCU] Kahverengi atrofi hücreye doğrudan zarar vermez; hücrenin geçirdiği uzun süreli serbest radikal hasarının ve otofajik sindirimin izidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Lipofuksin Pigmenti", "desc": "Sindirilmemiş lipid-protein peroksidasyon kalıntılarından oluşan sarı-kahverengi pigmenttir.", "isKey": True},
                    {"title": "Kahverengi Atrofi", "desc": "Yaşlı kalpte kütle kaybıyla birlikte belirgin koyu kahverengi renk değişimidir.", "isKey": True},
                    {"title": "Aşınma-Yıpranma", "desc": "Hücrenin maruz kaldığı kronik oksidatif stresin ve geçmiş otofajinin kanıtıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Kahverengi Atrofinin Morfolojik Özellikleri",
                    "headers": ["Düzey", "Görünüm", "Tanısal İpucu"],
                    "rows": [
                        ["Makroskopik", "Küçülmüş, kıvrımlı koronerli, koyu kahverengi kalp", "Subepikardiyal yağ kaybı, kahverengi renk"],
                        ["Işık Mikroskobu", "Nükleus kutuplarında perinükleer altın sarısı granüller", "Hematoksilen-Eozinde kahverengi-sarı pigment"],
                        ["Elektron Mikroskobu", "Tersiyer lizozomlar (telolizozom / artık cisimcik)", "Elektron yoğun lipid membran kalıntıları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yaşlı kalpte atrofi ve lipofuksin pigmenti birikimiyle ortaya çıkan tabloya kahverengi atrofi (brown atrophy) denir.",
                "📌 [SINAV SPOTU] Lipofuksin 'aşınma ve yıpranma (wear and tear)' pigmentidir; nükleus kutuplarında birikir."
            ],
            "medicalTerms": [
                {"term": "Lipofuksin", "explanation": "Hücre içi lipid peroksidasyonu sonucu lizozomlarda biriken sarı-kahverengi yaşlılık pigmentidir."},
                {"term": "Kahverengi Atrofi", "explanation": "Kalp ve karaciğerde atrofi ile lipofuksin birikiminin oluşturduğu koyu renkli organ tablosudur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "85 yaşında kaşektik bir hastanın otopsisinde kalbin belirgin küçüldüğü, koroner damarların kıvrımlaştığı ve miyokardın koyu kahverengi bir renk aldığı izlenmiştir. Mikroskopta miyosit nükleusları etrafında sarı-kahverengi granüller saptanmıştır. Bu tablo hangisidir?",
                    {
                        "A": "Kahverengi Atrofi (Lipofuksin birikimi)",
                        "B": "Akut Romatizmal Miyokardit (Aschoff cisimcikleri)",
                        "C": "Konsantrik Hipertrofi",
                        "D": "Amiloidozis (Kongo kırmızısı)",
                        "E": "Hemokromatozis (Demir yüklenmesi)"
                    },
                    "A",
                    {
                        "A": "Doğru: Yaşlı kalpte küçülme ve perinükleer lipofuksin birikimi kahverengi atrofidir.",
                        "B": "Yanlış: Aschoff cisimcikleri romatizmal ateşte granülomdur.",
                        "C": "Yanlış: Hipertrofide kalp büyür, küçülmez.",
                        "D": "Yanlış: Amiloidozda kalp amorf proteinle büyür.",
                        "E": "Yanlış: Hemokromatoziste Prusya mavisi pozitif hemosiderin birikir."
                    }
                ),
                make_cloze(
                    "Yaşlılıkta ve kaşekside küçülen kalpte miyosit nükleus kutuplarında birikerek kahverengi atrofi yapan aşınma pigmentine [lipofuksin] denir.",
                    "lipofuksin",
                    "Aşınma ve yaşlılık pigmenti adı"
                )
            ]
        },

        # Adım 68
        {
            "slideNumber": 68,
            "title": "Atrofik Hücrede Canlılığın Sürdürülmesi vs Apoptoza Geçiş",
            "subtitle": "Atrofik hücre küçülerek hayatta kalır; ancak eşik aşıldığında mitokondriyal apoptoz kaskadı başlar.",
            "badge": "Hücresel Karar",
            "badgeColor": "violet",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atrofi doğası gereği geri dönüşümlü bir adaptasyondur; hücre minimal metabolizma ile yaşamını korur. Ancak bu koruyucu kalkanın bir sınırı vardır.

Eğer besin yokluğu, iskemi veya sinir kaybı hücrenin tolere edebileceği kritik eşiği aşarsa, kaspaz kaskadları devreye girer. Mitokondri zarından **sitokrom c** sızar, apoptozom kompleksi kurulur ve hücre sessizce **apoptoz** ile elimine edilir. Böylece atrofi saf bir hacim kaybı olmaktan çıkarak kalıcı parankim hücresi kaybına dönüşür.

> [TEMEL İLKE] Atrofik hücre küçülerek hayatta kalmaya çalışır; dayanma eşiği tükendiğinde ise apoptoz ile intihar eder.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Dinamik Eşik", "desc": "Hücrenin ATP üretimini sürdürebildiği sürece atrofi geri dönüşümlüdür.", "isKey": True},
                    {"title": "Apoptoza Kayış", "desc": "Kritik besin ve oksijen seviyesinin altına inildiğinde programlı ölüm başlar.", "isKey": True},
                    {"title": "Kalıcı Parankim Kaybı", "desc": "Apoptozla kaybedilen hücreler kalıcı dokularda geri getirilemez.", "isKey": False}
                ],
                "table": {
                    "title": "Atrofi ve Apoptoz Sınır Çizgisi",
                    "headers": ["Durum", "Hücresel Bütünlük", "Geri Dönüş Olasılığı"],
                    "rows": [
                        ["Başarılı Atrofi", "Membran ve çekirdek sağlam, organel az", "Besin/uyaran verilince tam düzelme"],
                        ["Apoptoza Geçiş", "Sitokrom c salınımı, kaspaz aktivasyonu", "Geri dönüşsüz hücre ölümü"],
                        ["İleri Doku Sonucu", "Hücre sayısı kaybı, yerini alan fibrozis", "Kalıcı kütle kaybı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofinin ileri ve geri dönüşsüz aşamasında hücre ölümü apoptoz yolağı ile gerçekleşir.",
                "📌 [SINAV SPOTU] İntrinsik apoptoz yolağında mitokondriden sitokrom c salınımı kritik adımdır."
            ],
            "medicalTerms": [
                {"term": "İntrinsik Apoptoz", "explanation": "Hücre içi stres ve mitokondriyal geçirgenlik artışıyla başlayan programlı ölümdür."},
                {"term": "Sitokrom c", "explanation": "Mitokondri iç zarından sitoplazmaya sızdığında kaspazları aktive eden proteindir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Atrofiden Apoptoza Geçiş Kaskadı",
                    [
                        "1. Şiddetli ve Uzamış Stres: Besin ve oksijen desteğinin kritik sınırın altına inmesi.",
                        "2. Mitokondriyal Permeabilite: Bcl-2 ailesi protein dengesinin bozulması (Bax/Bak aktivasyonu).",
                        "3. Sitokrom c Salınımı: Mitokondri iç zarından sitoplazmaya sitokrom c sızması.",
                        "4. Apoptozom Aktivasyonu: Apaf-1 ve Prokaspaz-9 birleşimiyle kaspaz kaskadının ateşlenmesi.",
                        "5. Apoptoz ile Eliminasyon: Hücrenin büzüşüp nükleer fragmantasyonla temizlenmesi."
                    ]
                ),
                make_cloze(
                    "Uzamış ağır atrofide hücre dayanma eşiğini aştığında mitokondriden sitoplazmaya [sitokrom c] sızarak apoptozu başlatır.",
                    "sitokrom c",
                    "Mitokondriyal apoptoz başlatıcı molekül adı"
                )
            ]
        },

        # Adım 69 (CHECKPOINT 7)
        {
            "slideNumber": 69,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Atrofinin Moleküler Mekanizmaları",
            "subtitle": "Ubikuitin-proteazom sistemini, E3 ligazları (MuRF1/Atrogin-1), lizozomal yıkımı ve lipofuksin pigmentini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 7,
            "synthesisNarrative": """Bu bölümde atrofinin hücresel ve moleküler yıkım mekanizmalarını, proteazom ve lizozom sistemlerini ve kahverengi atrofiyi inceledik.

Atrofinin temeli protein sentezinin düşmesi ve yıkımının artmasıdır. Kas atrofisinde FoxO faktörleri kas-özgül E3 ligazları (MuRF1 ve Atrogin-1) aktive eder; miyofibriller poliubikuitinle işaretlenerek 26S proteazomda parçalanır. Organeller ise lizozomal asit hidrolazlarla sindirilir. Sindirilemeyen peroksidasyon artıkları lipofuksin pigmentine dönüşerek kalpte kahverengi atrofi tablosunu oluşturur.

> [TEKRAR SPOTU] Ubikuitin-proteazom kaskadı ve lizozomal otofaji, atrofide kütle kaybını yöneten iki temel proteolitik motordur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Yıkım Motoru", "desc": "Poliubikuitinasyonla işaretlenen proteinler 26S proteazomda parçalanır.", "isKey": True},
                    {"title": "Kas Ligazları", "desc": "MuRF1 ve Atrogin-1 miyozin ve kontraktil protein yıkımını yönetir.", "isKey": True},
                    {"title": "Lipofuksin ve Renk", "desc": "Lizozomal artıkların birikimi kahverengi atrofiye (brown atrophy) yol açar.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 7 Sentez Tablosu",
                    "headers": ["Bileşen", "Moleküler Görevi", "Patolojik Önemi"],
                    "rows": [
                        ["Ubikuitin-Proteazom", "Poliubikuitinli proteinleri ATP ile yıkma", "Kas atrofisinin ana yıkım motoru"],
                        ["MuRF1 / Atrogin-1", "Kas-özgül E3 ligaz aktivitesi", "Sarkomerik proteinlerin etiketlenmesi"],
                        ["Lipofuksin", "Sindirilmemiş otofajik lipid artığı", "Kahverengi atrofinin altın standart belirteci"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofide hücresel proteinlerin hızlanmış yıkımından sorumlu temel yolak ubikuitin-proteazom yolağıdır.",
                "📌 [SINAV SPOTU] MuRF1 ve Atrogin-1 kas atrofisinde indüklenen özgül E3 ubikuitin ligazlardır."
            ],
            "medicalTerms": [
                {"term": "Ubikuitin-Proteazom Yolağı", "explanation": "Proteinlerin ubikuitinle işaretlenip 26S proteazomda yıkıldığı temel proteolitik sistemdir."},
                {"term": "Lipofuksin", "explanation": "Hücre içi organel sindirimi artığı olan sarı-kahverengi yaşlılık pigmentidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc19",
                    "Atrofiye uğrayan bir hücrede yapısal proteinlerin yıkılmasında görev alan ana yolak hangisidir ve nasıl çalışır?",
                    "Ubikuitin-proteazom yolağıdır; hedef proteinler E1, E2 ve E3 ligazlar aracılığıyla poliubikuitin zinciriyle işaretlenir ve 26S proteazom silindirinde amino asitlere parçalanır."
                ),
                make_flashcard(
                    "k1-03-fc20",
                    "İskelet kası atrofisinde (açlık, immobilizasyon, kaşeksi) indüklenen kas-özgül E3 ubikuitin ligazlar nelerdir?",
                    "MuRF1 (Muscle RING Finger 1) ve Atrogin-1 (MAFbx) enzimleridir; doğrudan miyozin ve kasılma proteinlerini etiketleyerek yıktırırlar."
                ),
                make_flashcard(
                    "k1-03-fc21",
                    "Kahverengi atrofi (brown atrophy) nedir ve organa kahverengi rengi veren madde hangisidir?",
                    "Yaşlılıkta veya kaşekside küçülen kalp ve karaciğerde, lizozomal otofaji kalıntısı olan sarı-kahverengi lipofuksin pigmentinin perinükleer birikimidir."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Atrofiye uğrayan bir hücrede sitozolik tekil proteinlerin yıkımı ile mitokondri gibi bütün organellerin yıkımı arasındaki yolak farkı nedir?",
                    "Tekil proteinler ubikuitin-proteazom yolağında amino asitlere parçalanırken; mitokondri ve membran kompleksleri otofaji yoluyla lizozom içine alınarak asit hidrolazlarla sindirilir."
                )
            ]
        }
    ]
