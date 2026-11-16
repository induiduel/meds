#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 8: Histopatolojik Teknik ve Doku Takip Basamakları (Adımlar 70 - 79)
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
        # Adım 70
        {
            "slideNumber": 70,
            "title": "Histopatolojik Tekniğin Amacı ve Doku Takibinin Mantığı",
            "subtitle": "Canlı doku yumuşaktır ve %70-80'i sudur; mikroskopta 3-5 mikron incelikte kesilebilmesi için suyun yerine katı parafin yerleştirilmelidir.",
            "badge": "Doku Takibi",
            "badgeColor": "blue",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Histopatolojik doku takibinin amacı; sulu ve yumuşak dokuyu, ışık mikroskobunda incelenebilecek ==3 ila 5 mikrometre (µm)== incelikte kesilebilen katı bir bloğa dönüştürmektir.

Dokuların %70-80'i sudur; dokuyu sertleştiren parafin ise hidrofobiktir. Parafin su dolu hücrelere doğrudan giremediğinden ==Doku Takibi== şu sırayla yürütülür:
1. ==Dehidrasyon:== Hücre içi su artan alkol serileriyle çekilir.
2. ==Şeffaflaştırma:== Alkol kovularak yerine parafinle karışabilen ksilen konur.
3. ==İnfiltrasyon:== 60°C erimiş parafin ksilenin yerini alarak dokuyu doyurur.
4. ==Bloklama:== Soğutulan parafin katılaşarak mikrotomda kesime hazır hale gelir.

> [FİZİKOKİMYASAL İLKE] Doku takibi; hücreleri büzüştürmeden kurutup içlerine katı parafin yerleştirme sürecidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "3-5 µm Kesit Hedefi", "desc": "Işığın hücre çekirdeğinden geçebilmesi için doku mikron düzeyinde inceltilmelidir.", "isKey": True},
                    {"title": "Su-Parafin Uyuşmazlığı", "desc": "Su ile parafin karışmadığından aracı kimyasallar (alkol ve ksilen) zorunludur.", "isKey": True},
                    {"title": "Dört Temel İstasyon", "desc": "Fiksasyon → Dehidrasyon → Şeffaflaştırma → Parafin İnfiltrasyonu.", "isKey": False}
                ],
                "table": {
                    "title": "Doku Takip Aşamalarının Kimyasal Görevleri",
                    "headers": ["Aşama Sırası", "Kullanılan Kimyasal", "Fizikokimyasal Görevi"],
                    "rows": [
                        ["1. Fiksasyon (Tespit)", "%10 Nötral Tamponlu Formalin", "Proteazları inaktive eder, otolizi durdurur, dokuyu çapraz bağlarla sertleştirir"],
                        ["2. Dehidrasyon", "Artan konsantrasyonlarda Etanol (%70→%100)", "Doku ve hücre içindeki tüm serbest ve bağlı suyu uzaklaştırır"],
                        ["3. Şeffaflaştırma (Clearing)", "Ksilen (veya Toluen)", "Alkolü dokudan uzaklaştırır, parafinin dokuya girmesini sağlayacak köprüyü kurar"],
                        ["4. İnfiltrasyon (Emdirme)", "Erimiş Parafin (56-60°C)", "Ksilenin yerini alarak tüm hücre ve lif boşluklarını parafinle doyurur"],
                        ["5. Bloklama (Gömme)", "Sıvı Parafin + Soğutucu tabla", "Dokuyu metal kalıpta yönlendirip dondurarak katı kesim bloğu oluşturur"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Doku takip basamaklarının doğru sırası: Fiksasyon → Dehidrasyon (Alkol) → Şeffaflaştırma (Ksilen) → İnfiltrasyon (Parafin) → Bloklama.",
                "📌 [TEKNİK SPOT] Parafin suya karışamadığı için aracı solvent olarak ksilen (veya toluen) kullanılır.",
                "💡 [ÖĞRENME İPUCU] Mikroskop lamı üzerindeki doku kesitleri standart olarak 3-5 mikrometre (eritrosit çapından daha ince) kalınlıktadır."
            ],
            "medicalTerms": [
                {"term": "Doku Takibi (Tissue Processing)", "explanation": "Doku suyunun alınıp yerine mikrotomda kesilebilmesi için parafin emdirilmesi işlemidir."},
                {"term": "İnfiltrasyon", "explanation": "Doku boşluklarındaki çözücünün yerine erimiş sıvı parafinin hücre içine nüfuz etmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Doku Takibinin Kimyasal Mantık Zinciri",
                    [
                        "1. Fiksasyon: Doku %10 formalinde tespit edilerek otoliz ve çürüme durdurulur.",
                        "2. Dehidrasyon: Kademeli alkol serileriyle hücre içindeki su uzaklaştırılır.",
                        "3. Şeffaflaştırma: Alkol çıkarılarak parafinde eriyen ksilen solventi dokuya sokulur.",
                        "4. İnfiltrasyon: 60°C'deki erimiş sıvı parafin dokuya nüfuz ederek ksileni buharlaştırır.",
                        "5. Bloklama: Soğutulan parafin katılaşarak mikrotomda 3-5 µm kesilmeye hazır hale gelir."
                    ]
                ),
                make_micro_quiz(
                    "Patoloji laboratuvarında doku takibi yapılırken dokunun doğrudan erimiş sıvı parafin içine ATILAMAMASININ ve öncesinde alkol-ksilen basamaklarının uygulanmasının temel kimyasal gerekçesi nedir?",
                    {
                        "A": "Sıvı parafinin oda sıcaklığında patlayıcı olması",
                        "B": "Doku içindeki su ile hidrofobik parafinin birbiriyle karışamaması; suyun alkolle çekilip ksilenle köprü kurulmasının zorunlu olması",
                        "C": "Parafinin hematoksilen boyasını bozması",
                        "D": "Doku kasetlerinin parafine batınca erimesi",
                        "E": "Formalinin doku takibinde hiç kullanılmaması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Parafin oda sıcaklığında patlayıcı özellik göstermez.",
                        "B": "Doğru. Su ile apolar parafin karışamadığından suyun alkolle çekilip ksilenle köprü kurulması zorunludur.",
                        "C": "Yanlış. Hematoksilen boyaması doku takibinden sonra lam üzerinde yapılır.",
                        "D": "Yanlış. Plastik kasetler etüvdeki erimiş parafin sıcaklığına dayanıklıdır.",
                        "E": "Yanlış. Formalin doku takibinin başlangıcındaki temel tespit solüsyonudur."
                    }
                ),
                make_cloze(
                    "Doku takibinde suyun alkolle uzaklaştırılmasından sonra parafinin dokuya girmesini sağlayan aracı organik çözücüye ksilen adı verilir.",
                    "ksilen",
                    "Şeffaflaştırma basamağında kullanılan hidrokarbon çözücü"
                )
            ]
        },

        # Adım 71
        {
            "slideNumber": 71,
            "title": "Fiksasyonun Biyokimyası: Otoliz ve Putrefaksiyonun Engellenmesi",
            "subtitle": "Fiksasyon; doku ölür ölmez başlayan lizozomal kendi kendini sindirmeyi (otoliz) ve bakteriyel çürümeyi (putrefaksiyon) kimyasal çapraz bağlarla durdurur.",
            "badge": "Fiksasyon Biyokimyası",
            "badgeColor": "teal",
            "discipline": "Histopatoloji",
            "synthesisNarrative": """Dolaşımdan ayrılan canlı dokuda oksijen tükenmesiyle birlikte lizozom kaynaklı enzimlerin başlattığı kendi kendini eritme sürecine ==Otoliz==, bakteriyel çürümeye ise ==Putrefaksiyon== denir.

Histopatolojinin ilk basamağı olan ==Fiksasyon (Tespit)==, bu yıkıcı süreçleri hızla durdurur. Rutin histopatolojide altın standart **%10 Nötral Tamponlu Formalin**dir (%3.7-4 formaldehit gazı).
- Formaldehit, proteinlerdeki serbest amino gruplarıyla kovalent reaksiyona girer.
- Peptit zincirleri arasında **Metilen Köprüleri ($-CH_2-$ çapraz bağları)** kurarak enzim ve yapısal proteinleri kilitler.
- Proteolitik sindirim önlenir, hücre morfolojisi ve nükleer detaylar canlıdaki haline en yakın biçimde sabitlenir.

> [HAYATİ İLKE] Fiksatife zamanında girmeyen doku otolize uğrar; nükleer detayları silinmiş bir preparatta kanser tanısı konulamaz.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Otoliz Önleme", "desc": "Lizozomal proteazları kovalent bağlarla denatüre ederek doku erimesini durdurur.", "isKey": True},
                    {"title": "Metilen Köprüleri", "desc": "Formaldehit proteinler arasında $-CH_2-$ çapraz bağları kurarak dokuyu stabilize eder.", "isKey": True},
                    {"title": "Nötral Tamponlama", "desc": "pH 7.0-7.4 tutularak asit hematin pigmenti oluşumu engellenir.", "isKey": False}
                ],
                "table": {
                    "title": "Otoliz, Putrefaksiyon ve Fiksasyonun Karşılaştırması",
                    "headers": ["Süreç", "Etken Mekanizma", "Doku Üzerindeki Etkisi", "Fiksasyonun Müdahalesi"],
                    "rows": [
                        ["Otoliz", "Hücrenin kendi lizozomal enzimleri (katepsinler, hidrolazlar)", "Hücre sınırlarının silinmesi, nükleus soluklaşması (karyolizis)", "Enzimleri kovalent çapraz bağlarla inaktive ederek durdurur"],
                        ["Putrefaksiyon", "Saprofıt ve anaerobik bakterilerin dokuyu istilası", "Doku kokuşması, gaz kabarcıkları, doku sıvılaşması", "Bakteri proteinlerini pıhtılaştırıp sterilizasyon sağlar"],
                        ["Fiksasyon (Tespit)", "%10 Nötral Tamponlu Formalin kimyasal etkisi", "Proteinleri stabilize eder, dokuyu sertleştirir ve korur", "Hücre morfolojisini canlıdaki haline en yakın sabitler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Fiksasyonun temel amacı hücre ve dokuları otoliz ve putrefaksiyondan korumaktır.",
                "📌 [BİYOKİMYA SPOTU] Formaldehit proteinler arasında metilen ($-CH_2-$) çapraz bağları kurarak fiksasyon yapar.",
                "🚨 [KRİTİK UYARI] Fiksatife geç konulan dokularda otoliz nedeniyle nükleuslar 'hayalet hücre' şeklinde soluklaşır ve tanı imkansızlaşır."
            ],
            "medicalTerms": [
                {"term": "Otoliz (Autolysis)", "explanation": "Hücre ölümünün ardından lizozomal enzimlerin dokuyu kendi kendine sindirip eritmesidir."},
                {"term": "Metilen Köprüsü", "explanation": "Formaldehitin proteinler arasında oluşturduğu stabil kovalent çapraz bağ yapısıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Oksijensizlikten Otolize ve Fiksasyonla Kurtarılma Zinciri",
                    [
                        "1. Dolaşım Kesilmesi: Çıkarılan dokuda oksijensizlik ve ATP tükenmesi başlar.",
                        "2. Lizozom Yırtılması: Zarları bozulan lizozomlardan litik enzimler sitoplazmaya dökülür.",
                        "3. Enzimatik Sindirim: Serbest kalan proteazlar hücresel yapıları parçalamaya başlar.",
                        "4. Formalin Girişi: Dokunun formaline atılmasıyla formaldehit hücre içine difüze olur.",
                        "5. Metilen Kilitlenmesi: Kovalent çapraz bağlar enzimleri durdurarak morfolojiyi korur."
                    ]
                ),
                make_micro_quiz(
                    "Ameliyathanede çıkarılan bir apandisit materyalinin fiksatif konulmadan hafta sonu boyunca oda sıcaklığında bekletilmesi sonucu lümendeki ve duvardaki hücrelerin kendi lizozomal enzimleri tarafından sindirilip morfolojisinin tamamen bozulması olayına ne ad verilir?",
                    {
                        "A": "Metaplazi",
                        "B": "Otoliz (Autolysis)",
                        "C": "Hipertrofi",
                        "D": "Kalsifikasyon",
                        "E": "Anapilaksi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Metaplazi olgun bir hücre tipinin başka bir hücre tipine dönüşmesidir.",
                        "B": "Doğru. Otoliz, ölüm sonrası hücrenin kendi lizozomal enzimleri tarafından sindirilerek parçalanmasıdır.",
                        "C": "Yanlış. Hipertrofi hücre hacminin ve organ büyüklüğünün artışıdır.",
                        "D": "Yanlış. Kalsifikasyon dokularda anormal kalsiyum tuzlarının birikmesidir.",
                        "E": "Yanlış. Anafilaksi yaşamı tehdit eden sistemik tip 1 alerjik yanıttır."
                    }
                ),
                make_cloze(
                    "Hücrelerin ölümünden sonra kendi lizozom enzimleriyle sindirilerek yapısal bütünlüğünü kaybetmesi olayına otoliz adı verilir.",
                    "otoliz",
                    "Hücrenin kendi kendini eritmesi süreci"
                )
            ]
        },

        # Adım 72
        {
            "slideNumber": 72,
            "title": "Fiksasyon Kuralları: Hacim Oranı, Penetrasyon Hızı ve Doku Kalınlığı",
            "subtitle": "Kusursuz bir fiksasyon için; fiksatif hacmi dokunun en az 10-20 katı olmalı, doku kalınlığı 3-4 mm'yi geçmemeli ve saatte 1 mm penetrasyon hızı gözetilmelidir.",
            "badge": "Fiksasyon Standartları",
            "badgeColor": "amber",
            "discipline": "Histopatoloji",
            "synthesisNarrative": """Histopatolojide kaliteli bir preparat elde edebilmek için fiksasyonun üç temel kuralına eksiksiz uyulmalıdır.

==1. Hacim Oranı:== Numune kabındaki formalin hacmi doku hacminin **en az 10 ila 20 katı** olmalıdır; yetersiz fiksatif hızla tükenir ve dokuda otoliz başlar.
==2. Penetrasyon Hızı:== Formaldehit dokuya saatte yaklaşık **1 milimetre ($1\\text{ mm/saat}$)** hızla difüze olur; merkeze doğru ilerleme yavaşlar.
==3. Doku Kalınlığı ve Lümen Açılması:== Kasetlenen dokular **3-4 milimetreyi aşmamalıdır**. Mide ve bağırsak gibi lümenli rezeksiyon materyalleri hemen açılarak temizlenmeli; aksi halde iç kısımlarda merkezi otoliz ve çürüme gelişir.

> [ALTIN FORMÜL] Hacim = Dokunun 10-20 katı | Penetrasyon = 1 mm/saat | Doku kalınlığı = 3-4 mm.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "10-20 Kat Hacim Kuralı", "desc": "Formalin hacmi doku hacminin en az 10-20 katı olmalıdır.", "isKey": True},
                    {"title": "Saatte 1 mm Penetrasyon", "desc": "Formalin dokuya difüzyonla saatte yaklaşık 1 mm ilerler.", "isKey": True},
                    {"title": "Lümenlerin Açılması", "desc": "İçi boş organlar açılıp temizlenmeden fiksatif içine atılamaz.", "isKey": False}
                ],
                "table": {
                    "title": "Fiksasyonun Fiziksel Parametreleri ve Klinik Karşılıkları",
                    "headers": ["Parametre", "Standart Değer", "Kuralın İhlal Edilmesinin Doğuracağı Sonuç"],
                    "rows": [
                        ["Fiksatif / Doku Hacmi", "10 - 20 kat formalin", "Formalin molekülleri tükenir; doku yetersiz fikse olup otolize uğrar"],
                        ["Penetrasyon Hızı", "Saatte ~1 mm", "Büyük parçaların merkezine fiksatif 24 saatte bile ulaşamaz"],
                        ["Kasetlenen Parça Kalınlığı", "3 - 4 mm", "4 mm'den kalın parçaların merkezinde 'çiğ kalma' ve yumuşama oluşur"],
                        ["İdeal Fiksasyon Süresi", "Küçük biyopsi: 6-12 saat; Rezeksiyon: 24-48 saat", "Yetersiz sürede otoliz; aşırı sürede (haftalarca) antijenik kayıp oluşur"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Fiksatif hacmi doku hacminin en az 10-20 katı olmalıdır.",
                "📌 [SINAV SPOTU] Formaldehitin dokuya ortalama penetrasyon hızı saatte ~1 mm'dir.",
                "📌 [TEKNİK SPOT] Doku takip kasetine konulacak parçalar 3-4 mm kalınlığı aşmamalıdır.",
                "🚨 [KRİTİK UYARI] Mide ve bağırsak rezeksiyonları açılarak yıkanmadan fiksatife atılırsa lümendeki asit ve bakteriler mukozayı hızla eritir."
            ],
            "medicalTerms": [
                {"term": "Penetrasyon Hızı", "explanation": "Fiksatifin doku yüzeyinden merkeze doğru saatte kat ettiği difüzyon mesafesidir."},
                {"term": "Merkezi Otoliz", "explanation": "Fiksatifin ulaşamadığı kalın doku merkezlerinin kendi enzimleri ile sindirilmesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Fiksasyon Kuralları ve Standartları",
                    ["Parametre", "Kritik Değer", "Amacı"],
                    [
                        [
                            ("Fiksatif Hacmi", False),
                            ("Dokunun 10-20 katı", True, "Hacim oranı gereksinimi"),
                            ("Formalin moleküllerinin tükenmesini önlemek", False)
                        ],
                        [
                            ("Penetrasyon Hızı", False),
                            ("Saatte ~1 mm", True, "Difüzyon katsayısı"),
                            ("Fiksasyon süresini doğru hesaplamak", False)
                        ],
                        [
                            ("Kasetleme Kalınlığı", False),
                            ("3 - 4 mm", True, "Dilimleme kalınlığı"),
                            ("Doku merkezinde otolizi engellemek", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Kolon rezeksiyonu yapılan bir ameliyatta hemşire 20 cm'lik kolon segmentini açmadan küçük bir kavanoza koymuş ve üzerine dokunun yarısını ancak örtecek kadar formalin eklemiştir. Bu materyalde patoloji incelemesinde yaşanacak en büyük sorun nedir?",
                    {
                        "A": "Kolon mukozasında aşırı bazofilik boyanma artışı",
                        "B": "Yetersiz hacim ve lümenin açılmaması nedeniyle fiksatifin penetre olamaması ve bağırsak mukozasının otolize uğrayıp dökülmesi",
                        "C": "Kolonun mikrotom bıçaklarını kırması",
                        "D": "Ksilenin dokuyu aşırı sertleştirmesi",
                        "E": "Tümör evresinin pT4 olarak yükselmesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Otolize uğrayan dokularda nükleus bazofilisi kaybolur.",
                        "B": "Doğru. Hacim yetersizliği ve lümenin açılmaması fiksatif nüfuzunu engeller, mukozada otoliz ve dökülme oluşur.",
                        "C": "Yanlış. Fikse olmamış doku yumuşar, bıçağı kırmaz.",
                        "D": "Yanlış. Ksilen sertleşmesi doku takip aşamasında gelişir.",
                        "E": "Yanlış. Tümör evresi doku çürümesi nedeniyle yükselmez."
                    }
                ),
                make_cloze(
                    "Histopatolojide dokunun mükemmel fikse olabilmesi için fiksatif hacminin doku hacmine oranı en az 10-20 kat olmalıdır.",
                    "10-20",
                    "Fiksatifin dokuya asgari hacim katı aralığı"
                )
            ]
        },

        # Adım 73
        {
            "slideNumber": 73,
            "title": "Alternatif Fiksatifler: Zenker, Bouin, Carnoy ve Glutaraldehit",
            "subtitle": "Rutin fiksatif formalindir; ancak testis, böbrek, kemik iliği veya elektron mikroskopisi için özel kimyasal bileşimli fiksatifler kullanılır.",
            "badge": "Özel Fiksatifler",
            "badgeColor": "purple",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Histopatolojide rutin fiksatif %10 formalin olmakla birlikte, özel doku ve hedefler için farklı fiksatifler tercih edilir.

1. ==Bouin Solüsyonu (Pikrik Asitli):== **Testis Biyopsilerinde** (spermatogenez) ve endokrin dokularda nükleer detayları çok net korur.
2. ==Zenker ve B5 Fiksatifleri (Cıvalı):== **Kemik İliği** ve lenf nodlarında nükleer kromatini mükemmel gösterir; cıva toksisitesi nedeniyle kullanımı sınırlıdır.
3. ==Carnoy Fiksatifi (Susuz):== Hızlı nüfuz eder; suda eriyen **Glikojen ve Nükleik Asitleri (RNA/DNA)** korur, eritrositleri parçalar.
4. ==Glutaraldehit (%2.5):== **Elektron Mikroskopisi (TEM)** için organelleri nanometre düzeyinde çapraz bağlarla sabitler.

> [ÖZEL KURAL] Testis için Bouin, elektron mikroskobu için Glutaraldehit, glikojen için Carnoy kullanılır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Bouin: Testis Biyopsisi", "desc": "Pikrik asit içerir; testis tübüllerinde spermogenez morfolojisini mükemmel korur.", "isKey": True},
                    {"title": "Glutaraldehit: TEM", "desc": "Elektron mikroskopisi için nanometre organel fiksasyonu sağlar.", "isKey": True},
                    {"title": "Carnoy: Glikojen ve RNA", "desc": "Susuz fiksatif; glikojenin suda erimesini engelleyerek korur.", "isKey": False}
                ],
                "table": {
                    "title": "Özel Fiksatifler ve Klinikopatolojik Kullanım Alanları",
                    "headers": ["Fiksatif Adı", "Temel Bileşenleri", "En Sık Kullanıldığı Alan", "Ayırt Edici Özelliği"],
                    "rows": [
                        ["Bouin", "Pikrik asit, formalin, asetik asit", "Testis biyopsisi, endokrin dokular", "Sarı renklidir; nükleer detayları çok net korur"],
                        ["Zenker / B5", "Cıva klorür, potasyum dikromat", "Kemik iliği, lenf nodu biyopsileri", "Harika nükleer kromatin; cıva pigmenti temizliği gerektirir"],
                        ["Carnoy", "Etanol, kloroform, asetik asit", "Glikojen depo hastalıkları, sitogenetik", "Hızlı penetrasyon, eritrositleri parçalar, glikojeni korur"],
                        ["Glutaraldehit (%2.5)", "Bifonksiyonel dialdehit", "Transmisyon Elektron Mikroskopisi (TEM)", "Ultra ince kesitler için organelleri nanometre düzeyinde kilitler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Testis biyopsilerinde spermogenezi ve nükleer detayları en iyi koruyan fiksatif Bouin fiksatifidir.",
                "📌 [SINAV SPOTU] Transmisyon Elektron Mikroskopisi (TEM) için standart fiksatif %2.5 Glutaraldehit solüsyonudur.",
                "📌 [SINAV SPOTU] Glikojeni ve RNA'yı suda erimeden korumak için susuz Carnoy fiksatifi tercih edilir."
            ],
            "medicalTerms": [
                {"term": "Bouin Fiksatifi", "explanation": "Pikrik asit içeren, özellikle testis biyopsisinde nükleer detayları koruyan fiksatiftir."},
                {"term": "Glutaraldehit", "explanation": "Elektron mikroskopisinde organelleri nanometre düzeyinde sabitleyen güçlü fiksatiftir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Fiksatif ve Klinik İnceleme Eşleştirmesi",
                    ["İncelenecek Doku / Yöntem", "Altın Standart Fiksatif", "Kimyasal Özellik"],
                    [
                        [
                            ("Testis İğne Biyopsisi", False),
                            ("Bouin Solüsyonu", True, "Pikrik asitli fiksatif"),
                            ("Spermatojenik hücrelerin nükleer netliği", False)
                        ],
                        [
                            ("Elektron Mikroskopisi (TEM)", False),
                            ("Glutaraldehit (%2.5)", True, "Bifonksiyonel dialdehit"),
                            ("Organel ultrastrüktürünün korunması", False)
                        ],
                        [
                            ("Glikojen Depo Gösterimi", False),
                            ("Carnoy Fiksatifi", True, "Susuz alkol-kloroform karışımı"),
                            ("Glikojenin suda çözünmesini engelleme", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "İnfertilite araştırması amacıyla erkek hastadan alınan testis biyopsisinde spermatogenez basamaklarını ve nükleer kromatin ayrıntılarını en net şekilde değerlendirebilmek için dokunun konulması gereken en uygun fiksatif hangisidir?",
                    {
                        "A": "%100 Aseton",
                        "B": "Bouin Fiksatifi",
                        "C": "Saf Distile Su",
                        "D": "Ksilen",
                        "E": "Sıvı Azot"
                    },
                    "B",
                    {
                        "A": "Yanlış. Aseton dokuyu aşırı büzüştürür ve nükleer detayları bozar.",
                        "B": "Doğru. Bouin solüsyonu testis biyopsisinde spermatogenez morfolojisini ve nükleus detaylarını en iyi koruyan fiksatiftir.",
                        "C": "Yanlış. Distile su hipotonik lizise yol açarak hücreleri patlatır.",
                        "D": "Yanlış. Ksilen takip basamağında kullanılan bir solventtir, fiksatif değildir.",
                        "E": "Yanlış. Sıvı azot dondurma hasarı ve buz kristali artefaktı oluşturur."
                    }
                ),
                make_cloze(
                    "Testis biyopsilerinde spermatojenik hücreleri ve nükleer detayları korumak için pikrik asit içeren Bouin fiksatifi tercih edilir.",
                    "Bouin",
                    "Testis biyopsisinde kullanılan pikrik asitli özel fiksatifin adı"
                )
            ]
        },

        # Adım 74
        {
            "slideNumber": 74,
            "title": "Dehidrasyon Basamağı: Kademeli Alkol Serileri ile Suyun Uzaklaştırılması",
            "subtitle": "Dehidrasyon; dokudaki suyun kademeli artan etanol dereceleriyle (%70 → %80 → %95 → %100) dokuda büzüşme yaratmadan çekilmesidir.",
            "badge": "Dehidrasyon",
            "badgeColor": "cyan",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Fiksasyonu tamamlanan doku kasetlerinde takibin ilk kimyasal basamağı ==Dehidrasyon (Suyun Uzaklaştırılması)== işlemidir.

Doku suyunu çekmek için etil alkol (etanol) kullanılır. Su dolu doku doğrudan **%100 mutlak alkole** atılırsa ani ozmotik çıkışla hücreler büzüşür ve doku mimarisi çöker. Bu hasarı önlemek için dehidrasyon **kademeli artan alkol serileri** ile yürütülür:
- ==%70 Etanol:== Formalin tuzlarını temizler ve yumuşak ozmotik geçiş başlatır.
- ==%80 - %90 Etanol:== Su yavaşça alkolle yer değiştirir.
- ==%95 - %100 Mutlak Etanol:== Dokudaki son su izleri tamamen çekilir.
Yetersiz dehidrasyon parafinin içeri girmesini engeller ve blokta yumuşama yapar.

> [KİMYASAL İLKE] Kademeli artan alkol serileri; hücre mimarisini koruyarak suyu çekmenin tek yoludur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kademeli Alkol Serisi", "desc": "%70 → %80 → %95 → %100 etanol basamaklarıyla ani ozmotik şok önlenir.", "isKey": True},
                    {"title": "Tam Kuruma Şartı", "desc": "Dokuda %1 bile su kalırsa sonraki aşamada parafin içeri giremez.", "isKey": True},
                    {"title": "Aşırı Dehidrasyon Riski", "desc": "Dokunun alkolde günlerce unutulması aşırı sertleşme ve kırılganlığa yol açar.", "isKey": False}
                ],
                "table": {
                    "title": "Dehidrasyon Basamağında Alkol Banyoları ve Süreleri",
                    "headers": ["Banyo İstasyonu", "Alkol Konsantrasyonu", "Ortalama Süre", "Hücresel Olay"],
                    "rows": [
                        ["1. İstasyon", "%70 Etil Alkol", "1 - 2 saat", "Tuzların yıkanması ve hafif su çıkışı"],
                        ["2. İstasyon", "%80 Etil Alkol", "1 - 2 saat", "Ozmotik dengenin korunarak suyun seyreltilmesi"],
                        ["3. İstasyon", "%95 Etil Alkol", "1 - 2 saat", "Sitoplazmik suyun büyük kısmının yer değiştirmesi"],
                        ["4. İstasyon", "%100 Mutlak Alkol (I)", "1 saat", "Dokuda kalan bağlı suyun çekilmesi"],
                        ["5. İstasyon", "%100 Mutlak Alkol (II)", "1 saat", "Tamamen susuz (anhidröz) doku elde edilmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Dehidrasyon basamağında dokudaki su kademeli olarak artan etanol (%70 → %80 → %95 → %100) serileriyle uzaklaştırılır.",
                "📌 [TEKNİK SPOT] Dehidrasyon yetersiz kalırsa parafin infiltrasyonu başarısız olur ve kesit alınamaz.",
                "💡 [ÖĞRENME İPUCU] Dokunun aniden %100 alkole atılmamasının tek nedeni hücrelerin ani su kaybıyla büzüşmesini (plazmoliz) engellemektir."
            ],
            "medicalTerms": [
                {"term": "Dehidrasyon", "explanation": "Fikse dokunun parafine hazırlanması için suyunun kademeli alkol serileriyle çekilmesidir."},
                {"term": "Mutlak (Absolü) Alkol", "explanation": "İçinde su bulunmayan ve dokudaki son su kalıntılarını çeken saf etanoldür."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Dehidrasyon Kademeli Geçiş Zinciri",
                    [
                        "1. %70 Alkol: Fikse dokudan formalin tuzları yıkanarak yumuşak geçiş başlatılır.",
                        "2. %80-%90 Alkol: Su molekülleri büzüşme yaratmadan yavaşça alkolle yer değiştirir.",
                        "3. %95 Alkol: Serbest doku suyunun büyük bölümü uzaklaştırılır.",
                        "4. %100 Mutlak Alkol: Dokuda kalan son mikroskobik su izleri tamamen çekilir.",
                        "5. Ksilene Hazırlık: Tamamen susuz kalan doku şeffaflaştırma aşamasına hazır hale gelir."
                    ]
                ),
                make_micro_quiz(
                    "Doku takip cihazında dehidrasyon basamağında dokunun doğrudan %100'lük mutlak alkole atılmayıp %70'ten başlayan artan dereceli alkol serilerinden geçirilmesinin temel biyolojik gerekçesi nedir?",
                    {
                        "A": "Laboratuvarda kullanılan alkol maliyetini düşürmek",
                        "B": "Ani ozmotik su çıkışına bağlı hücrelerin aşırı büzüşmesini, distorsiyonunu ve doku çatlamasını engellemek",
                        "C": "Hematoksilen boyasının solmasını sağlamak",
                        "D": "Formaldehit gazının açığa çıkmasını hızlandırmak",
                        "E": "Mikrotom bıçaklarının körelmesini önlemek"
                    },
                    "B",
                    {
                        "A": "Yanlış. Kademeli serinin amacı reaktif tasarrufu değil doku mimarisini korumaktır.",
                        "B": "Doğru. Kademeli alkol geçişi ani ozmotik su çıkışına bağlı hücresel büzüşmeyi ve doku çatlamasını engeller.",
                        "C": "Yanlış. Hematoksilen boyaması takipten sonra preparat aşamasında yapılır.",
                        "D": "Yanlış. Formaldehit gazı bu basamaktan önce yıkanmıştır.",
                        "E": "Yanlış. Mikrotom jiletinin ömrüyle alkol serisinin ilgisi yoktur."
                    }
                ),
                make_cloze(
                    "Doku takibinde hücre içi suyun dokudan kademeli olarak uzaklaştırılması işlemine dehidrasyon adı verilir.",
                    "dehidrasyon",
                    "Suyun alkolle uzaklaştırılması aşamasının adı"
                )
            ]
        },

        # Adım 75
        {
            "slideNumber": 75,
            "title": "Şeffaflaştırma (Clearing): Ksilenin Rolü ve Alkol-Parafin Köprüsü",
            "subtitle": "Şeffaflaştırma; dehidrasyon alkolünü dokudan uzaklaştırıp yerine parafinde çözünen ksileni koyarak dokuyu yarı saydam hale getirir.",
            "badge": "Şeffaflaştırma",
            "badgeColor": "emerald",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Dehidrasyonla suyu çekilen dokuda hücreler alkolle doludur; ancak hidrofobik parafin alkolle karışmadığından aracı bir çözücüye ihtiyaç duyulur.

Bu aşamaya ==Şeffaflaştırma (Clearing)==, kullanılan organik çözücüye ise en sık ==Ksilen (Ksilol)== adı verilir.
- Ksilen hem etanolle hem de erimiş parafinle tam karışır; alkolü dokudan kovar ve parafine yol açar.
- Ksilenin kırma indeksi doku proteinlerine çok yakın olduğu için doku optik olarak **yarı saydam / şeffaf** bir görünüm kazanır.
- Dokunun ksilende gereğinden fazla bekletilmesi dokuyu **aşırı sert ve kırılgan (gevrek)** hale getirir; mikrotomda kesilirken ufalanmaya yol açar. Yetersiz bekletilirse alkol atılamaz ve parafin infiltrasyonu çöker.

> [KİMYASAL KÖPRÜ] Ksilen; alkol ile parafin arasındaki vazgeçilmez çözücü köprüdür; alkolü uzaklaştırıp parafini içeri alır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Çift Yönlü Çözünürlük", "desc": "Ksilen hem etanolde hem de erimiş parafinde mükemmel çözünür.", "isKey": True},
                    {"title": "Kırılma İndeksi Uyumu", "desc": "Işık kırma indeksi dokuyla eşitlenerek doku yarı saydam görünüm alır.", "isKey": True},
                    {"title": "Kırılganlık Riski", "desc": "Ksilende aşırı bekletilen doku aşırı sertleşir ve mikrotomda ufalanır.", "isKey": False}
                ],
                "table": {
                    "title": "Şeffaflaştırma Ajanlarının Özellikleri",
                    "headers": ["Ajan", "Avantajı", "Dezavantajı / Tehlikesi"],
                    "rows": [
                        ["Ksilen (Ksilol)", "En hızlı ve en etkili şeffaflaştırıcı; parafinle mükemmel uyum", "Toksik, yanıcı, dokuda aşırı kalırsa sertleşme ve gevreklik yapar"],
                        ["Toluen", "Ksilene göre dokuyu daha az sertleştirir", "Ksilenden daha yavaş etki eder, pahalıdır"],
                        ["Kloroform", "Dokuyu sertleştirmez, kırılganlık yapmaz", "Ağır toksik buharlar çıkarır, çevreye zararlıdır"],
                        ["Ksilen Alternatifleri (Limonen vb.)", "Daha az toksik, narenciye kokulu", "Parafini eritme gücü ksilenden düşüktür"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Doku takibinde dehidrasyon alkolünü dokudan uzaklaştırıp parafinin dokuya girmesini sağlayan 'şeffaflaştırma' basamağında en sık Ksilen kullanılır.",
                "📌 [TEKNİK SPOT] Doku ksilende aşırı uzun süre bekletilirse aşırı sertleşir ve mikrotomda kesilirken kırılır (gevreklik).",
                "💡 [ÖĞRENME İPUCU] Bu basamağa 'clearing' (şeffaflaştırma) denmesinin sebebi dokunun optik olarak yarı saydam hale gelmesidir."
            ],
            "medicalTerms": [
                {"term": "Şeffaflaştırma (Clearing)", "explanation": "Alkolün dokudan atılıp parafinle karışabilen ksilen ile yer değiştirmesi aşamasıdır."},
                {"term": "Kırılma İndeksi", "explanation": "Işığın bir maddeden geçerken hızının ve yayılma doğrultusunun değişme katsayısıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Şeffaflaştırmada Ksilenin Etki Zinciri",
                    [
                        "1. Alkolün Çözünmesi: Ksilen banyosuna giren dokudan alkol molekülleri uzaklaştırılır.",
                        "2. Ksilen Doygunluğu: Hücre içi ve stroma boşlukları bütünüyle ksilene doyar.",
                        "3. Saydamlaşma: Işık kırma indeksleri eşitlendiği için doku yarı saydam hale gelir.",
                        "4. Parafin Köprüsü: Dokudaki ksilen, sıcak parafinin içeri nüfuz etmesini kolaylaştırır.",
                        "5. Süre Kontrolü: Doku aşırı sertleşip kırılganlaşmadan parafin banyosuna aktarılır."
                    ]
                ),
                make_micro_quiz(
                    "Doku takip cihazında şeffaflaştırma aşamasında doku kasetlerinin ksilende unutulması ve 48 saat boyunca ksilende kalması mikrotom kesiti esnasında hangi teknik probleme yol açar?",
                    {
                        "A": "Dokunun su çekip şişmesine ve parçalanmasına",
                        "B": "Dokunun aşırı sertleşip kırılgan (gevrek) hale gelmesine ve kesit alınırken ufalanıp yırtılmasına",
                        "C": "Hücre çekirdeklerinin büyümesine",
                        "D": "Formaldehit gazı açığa çıkarak patlama olmasına",
                        "E": "Hematoksilen boyasının kırmızıya dönmesine"
                    },
                    "B",
                    {
                        "A": "Yanlış. Ksilen hidrokarbon solventidir, su çekmez.",
                        "B": "Doğru. Ksilende aşırı bekleyen doku aşırı sertleşir, gevrek hale gelir ve mikrotomda ufalanır.",
                        "C": "Yanlış. Hücre çekirdeği boyutu organik solventlerle büyümez.",
                        "D": "Yanlış. Cihazda patlamaya yol açacak gaz reaksiyonu gelişmez.",
                        "E": "Yanlış. Hematoksilen boyasının rengi doku takibinden etkilenmez."
                    }
                ),
                make_cloze(
                    "Doku takibinde dehidrasyon ile parafin infiltrasyonu arasında köprü kurarak dokuyu yarı saydam hale getiren basamağa şeffaflaştırma adı verilir.",
                    "şeffaflaştırma",
                    "Alkolü kovan ve dokuyu saydamlaştıran basamak"
                )
            ]
        },

        # Adım 76
        {
            "slideNumber": 76,
            "title": "İnfiltrasyon ve Parafin Bloklama (Gömme): Doku Oryantasyonu",
            "subtitle": "İnfiltrasyonla erimiş parafine doyan doku; metal kalıplarda doğru anatomik açıyla (oryantasyon) yönlendirilip soğutularak blok haline getirilir.",
            "badge": "Bloklama",
            "badgeColor": "teal",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Doku takibinin son basamağında ksilen buharlaştırılarak yerine erimiş parafin emdirilir ve bloklama istasyonunda yönlendirilir.

Kasetler 56-60°C'deki erimiş parafinde bekletilerek doku boşlukları doyurulur (İnfiltrasyon). Ardından ==Bloklama (Embedding)== aşamasında doku kalıba alınır. Bu basamağın en kritik unsuru **Doku Oryantasyonu (Yönlendirme)**dur:
- ==Deri Biyopsileri:== Epidermis, dermis ve subkutan yağın birlikte kesilmesi için kalıba **dik (vertikal)** yerleştirilir.
- ==Lümenli Organlar:== Mide ve bağırsak duvar katmanlarının tümü görülecek şekilde dik açıyla dizilir.
Kalıp soğutucu tablaya (-5°C) konulduğunda parafin hızla donarak sert bir kesim bloğuna dönüşür.

> [BLOKLAMA KURALI] Hatalı yönlendirilen bir doku bloğundan organ katmanlarını veya tümör invazyon derinliğini görmek imkansızdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "56-60°C Parafin İnfiltrasyonu", "desc": "Ksilenin yerini erimiş parafin alarak doku doyurulur.", "isKey": True},
                    {"title": "Anatomik Oryantasyon", "desc": "Deri ve tübüler organ katmanları kalıba dik açılandırılmalıdır.", "isKey": True},
                    {"title": "Hızlı Soğutma", "desc": "Soğuk tabloda hızlı katılaşma parafinin kristalleşmesini ve çatlamasını önler.", "isKey": False}
                ],
                "table": {
                    "title": "Doku Tiplerine Göre Doğru Gömme (Oryantasyon) Kuralları",
                    "headers": ["Doku / Organ Tipi", "Hatalı Gömme Pozisyonu", "Doğru Gömme Oryantasyonu", "Tanısal Önemi"],
                    "rows": [
                        ["Deri Punch / Eksizyon", "Yatay (horizontal) düz yatırma", "Kalıba dik (vertikal) gömme", "Epidermis, dermis ve cerrahi sınır aynı kesitte görünür"],
                        ["Bağırsak / Mide Duvarı", "Serosa veya mukoza üzerine yatırma", "Tüm duvar katmanları dik kesit açısında", "Kanser invazyon derinliğinin (muskularis propria) ölçülebilmesi"],
                        ["İğne Kor (Tru-cut) Biyopsileri", "Dağınık veya eğri yerleştirme", "Tüm korlar paralel ve aynı seviyede düz", "Tüm korların aynı bıçak darbesinde eksiksiz kesilebilmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Deri biyopsilerinde epidermis, dermis ve subkutan yağ dokusunun aynı anda incelenebilmesi için doku kalıba 'dik' (vertikal) oryante edilmelidir.",
                "📌 [TEKNİK SPOT] Parafin gömmede kullanılan erimiş parafinin sıcaklığı genellikle 56-60°C arasındadır; aşırı sıcaklık dokuyu yakar.",
                "💡 [ÖĞRENME İPUCU] Hızlı soğutma parafinin homojen katılaşmasını sağlar; yavaş soğursa büyük mum kristalleri oluşur ve kesit yırtılır."
            ],
            "medicalTerms": [
                {"term": "Doku Oryantasyonu", "explanation": "Doku parçasının parafin kalıba uygun anatomik açıyla yerleştirilmesidir."},
                {"term": "Parafin Blok", "explanation": "İçine doku gömülüp dondurulmuş, mikrotomda kesime hazır katı parafin yapıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Deri Biyopsisinde Hatalı vs Doğru Gömme (Oryantasyon)",
                    "Hatalı Oryantasyon (Yatay Gömme)",
                    "Doğru Oryantasyon (Dik / Vertikal Gömme)",
                    [
                        "Deri kalıp tabanına yassı olarak yatırılmıştır",
                        "Mikrotom bıçağı sadece yüzeydeki epidermisi sıyırır",
                        "Dermis ve derin invazyon hattı kesite hiç girmez",
                        "Displazi veya tümör derinliği değerlendirilemez"
                    ],
                    [
                        "Doku kalıba dik açıyla kesit yüzeyi tabana gelecek şekilde konur",
                        "Tek bir kesitte epidermis, dermis ve subkutis birlikte izlenir",
                        "Tümörün derinliği ve cerrahi alt sınır net ölçülür",
                        "Kusursuz histopatolojik tanı ve evreleme sağlanır"
                    ]
                ),
                make_micro_quiz(
                    "Histoteknoloji laboratuvarında teknisyenin bir deri punch biyopsisini parafin kalıbına gömerken kalıba 'dik (vertikal)' olarak yerleştirmesinin temel amacı nedir?",
                    {
                        "A": "Parafinin daha çabuk donmasını sağlamak",
                        "B": "Mikroskop altında epidermis, dermis ve subkutan yağ dokusunun üç katmanının da aynı kesitte tam olarak görülebilmesi",
                        "C": "Eozin boyasının deriye daha iyi bağlanmasını sağlamak",
                        "D": "Doku kasetinin barkodunun okunmasını kolaylaştırmak",
                        "E": "Deri kıllarının dökülmesini önlemek"
                    },
                    "B",
                    {
                        "A": "Yanlış. Donma hızı kalıbın yerleştirildiği soğuk tablanın ısısına bağlıdır.",
                        "B": "Doğru. Dik yerleşim epidermis, dermis ve subkutan dokunun aynı kesitte tam kat izlenmesini sağlar.",
                        "C": "Yanlış. Boyanın kimyasal afinitesi dokunun gömülme açısıyla ilişkili değildir.",
                        "D": "Yanlış. Barkod kasetin dış yüzeyindedir, yönlendirmeyle değişmez.",
                        "E": "Yanlış. Kılların dökülmesiyle gömme oryantasyonunun ilgisi yoktur."
                    }
                ),
                make_cloze(
                    "Doku parçalarının parafin kalıbı içerisine doğru anatomik açıyla yerleştirilerek tüm katmanlarının görünür kılınması işlemine doku oryantasyonu adı verilir.",
                    "doku oryantasyonu",
                    "Gömme esnasında dokunun doğru açıda yerleştirilmesi kavramı"
                )
            ]
        },

        # Adım 77
        {
            "slideNumber": 77,
            "title": "Mikrotomi: Rotary Mikrotom ile 3-5 µm Kesit Alma ve Su Banyosu",
            "subtitle": "Rotary mikrotom; çelik veya tek kullanımlık jiletlerle parafin bloktan 3-5 mikronluk şerit kesitler alır ve ılık su banyosunda kırışıksız açar.",
            "badge": "Mikrotomi",
            "badgeColor": "indigo",
            "discipline": "Histoteknoloji",
            "synthesisNarrative": """Hazırlanan katı parafin bloklardan mikroskopta incelenecek incelikte şeritler elde etme sürecine ==Mikrotomi== denir.

Rutin patolojide en sık **Rotary (Döner) Mikrotom** kullanılır. Kesit alma basamakları şu sırayla yürütülür:
1. ==Trimleme:== Blok cihaza bağlanır, doku yüzeyine ulaşılana kadar 15-20 µm'lik kaba kesimle düzeltilir.
2. ==İnce Kesim:== Mikrometre vidasıyla bloktan **3 ila 5 µm inceliğinde** şerit (kurdele) kesit alınır.
3. ==Ilık Su Banyosu (Flotasyon, 40-45°C):== Parafin şerit suyun üzerine bırakılarak kırışıklıkları açılır.
4. ==Lama Alma ve Etüv:== Kesit adezyonlu cama alınır, 60°C etüvde ısıtılarak parafin eritilir ve doku sabitlenir.

> [HASSASİYET STANDARDI] 3-5 mikrometrelik kesit kalınlığı; hücre çekirdeklerinin üst üste binmeden tek tabaka halinde incelenmesini sağlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Rotary Mikrotom Standardı", "desc": "Rutin histopatolojide döner kollu mekanik mikrotom kullanılır.", "isKey": True},
                    {"title": "3-5 µm Kesit Kalınlığı", "desc": "Hücrelerin üst üste binmesini engelleyen ideal optik kalınlıktır.", "isKey": True},
                    {"title": "40-45°C Su Banyosu", "desc": "Parafin şeridin kırışıklıklarını açarak lama kusursuz transferini sağlar.", "isKey": False}
                ],
                "table": {
                    "title": "Mikrotomi ve Kesit Alma Basamakları",
                    "headers": ["İşlem Adımı", "Kullanılan Araç / Isı", "Temel Amacı"],
                    "rows": [
                        ["Trimleme (Düzeltme)", "Mikrotom jileti (15-20 µm)", "Blok yüzeyindeki fazla parafini traşlayıp doku yüzeyine ulaşmak"],
                        ["İnce Kesit Alma", "Rotary mikrotom (3-5 µm)", "Hücre çekirdeklerini tek tabaka halinde gösterecek kesit şeridi üretmek"],
                        ["Flotasyon (Yüzdürme)", "Ilık su banyosu (40-45°C)", "Parafin kesitin kırışıklıklarını ve katlantılarını su üzerinde açmak"],
                        ["Lama Alma", "Adezyonlu (polilizinli) lam", "Açılmış kesiti lam üzerine merkezleyerek almak"],
                        ["Etüvde Kurutma", "Etüv fırını (60°C, 30-60 dk)", "Dokuyu lama fırınlayarak sabitlemek ve fazla parafini eritmek"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Işık mikroskobunda rutin histopatolojik inceleme için en sık kullanılan mikrotom tipi Rotary (Döner) Mikrotomdur.",
                "📌 [SINAV SPOTU] Parafin bloklardan alınan standart rutin kesit kalınlığı 3-5 mikrometredir (µm).",
                "📌 [TEKNİK SPOT] Kesitlerin kırışıklıklarının açıldığı ılık su banyosu sıcaklığı 40-45°C civarında olmalıdır."
            ],
            "medicalTerms": [
                {"term": "Rotary Mikrotom", "explanation": "Döner çark mekanizmasıyla parafin bloktan 3-5 µm kesit alan temel laboratuvar cihazıdır."},
                {"term": "Flotasyon Banyosu", "explanation": "Kesitlerin kırışıklıklarını açıp lama aktarmayı sağlayan 40-45°C'lik su küvetidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Mikrotom Kesitinden Boyamaya Hazırlık Zinciri",
                    [
                        "1. Trimleme: Parafin blok mikrotoma bağlanarak kaba traşlamayla doku yüzeyi açığa çıkarılır.",
                        "2. İnce Kesim: Çark çevrilerek 3-5 µm inceliğinde kesintisiz parafin şerit kesit alınır.",
                        "3. Flotasyon: Kesit 40-45°C ılık su banyosuna bırakılarak kırışıklıkları gerilimle açılır.",
                        "4. Lama Transfer: Açılan düzgün doku kesiti adezyonlu cam lam üzerine alınır.",
                        "5. Etüvde Fırınlama: Lam 60°C etüvde ısıtılarak parafin eritilir ve doku cama sabitlenir."
                    ]
                ),
                make_micro_quiz(
                    "Rutin ışık mikroskobu histopatolojik incelemeleri için parafin bloklardan rotary mikrotom yardımıyla alınan standart kesit kalınlığı ne kadardır?",
                    {
                        "A": "50 - 100 mikrometre",
                        "B": "3 - 5 mikrometre (µm)",
                        "C": "1 milimetre",
                        "D": "50 - 80 nanometre",
                        "E": "0.1 milimetre"
                    },
                    "B",
                    {
                        "A": "Yanlış. Bu kalınlıkta ışık dokudan geçemez ve hücreler siyah kütle olarak görünür.",
                        "B": "Doğru. Rutin ışık mikroskopisi için standart doku kesiti kalınlığı 3 ila 5 mikrometredir.",
                        "C": "Yanlış. Milimetre kalınlığındaki örnekler mikroskopta hücresel incelenemez.",
                        "D": "Yanlış. Nanometre boyutundaki kesitler elektron mikroskopisine (TEM) özgüdür.",
                        "E": "Yanlış. 100 mikrometre rutin ışık mikroskopisi için aşırı kalındır."
                    }
                ),
                make_cloze(
                    "Rutin histopatoloji laboratuvarında parafin bloklardan 3-5 mikronluk kesitler almak için en yaygın kullanılan cihaz tipi rotary mikrotom olarak adlandırılır.",
                    "rotary mikrotom",
                    "Rutin patolojide kesit alan döner mekanizmalı mikrotom türü"
                )
            ]
        },

        # Adım 78
        {
            "slideNumber": 78,
            "title": "İntraoperatif Konsültasyon: Frozen (Kriostat) Kesit Tekniği",
            "subtitle": "Frozen kesit; hasta ameliyat masasındayken dokuyu -20°C'de dondurarak 5-10 dakikada cerrahi sınır ve malignite tanısı veren acil konsültasyondur.",
            "badge": "Frozen Kesit",
            "badgeColor": "red",
            "discipline": "Cerrahi Patoloji",
            "synthesisNarrative": """Ameliyat sürerken cerrahi sınırı veya maligniteyi dakikalar içinde belirlemek için ==Frozen Kesit (İntraoperatif Konsültasyon)== uygulanır.

Rutin takip 24 saat sürdüğünden operasyondaki hastada bu süre beklenemez. Frozen süreci yaklaşık **5-10 dakikada** tamamlanır:
1. ==Fiksatifsiz Ulaşım:== Doku formalinsiz, taze olarak kuru gazlı bezde ulaştırılır.
2. ==Dondurma ve Kesim:== Doku jel içinde -20°C **Kriostat** kabininde dondurulup 5-6 µm kesilir.
3. ==Hızlı Boyama ve Rapor:== 1 dakikalık boyama sonrası patolog cerraha sonucu bildirir.
Buz kristalleri nedeniyle hücresel morfoloji zayıftır; bu nedenle cerrahi planı değiştirecek durumlarda istenir.

> [AMELİYATHANE KURALI] Frozen kesit cerrahi sınır kontrolü veya rezeksiyon kararını etkileyecekse istenir; kesin evreleme parafinde verilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "5-10 Dakikada Sonuç", "desc": "Ameliyat bitmeden cerraha anlık mikroskobik rehberlik sağlar.", "isKey": True},
                    {"title": "-20°C Kriostat Cihazı", "desc": "Kimyasal takip olmadan fiziksel dondurma ile kesim sertliği sağlanır.", "isKey": True},
                    {"title": "Buz Kristali Sınırı", "desc": "Morfolojik kalite parafin kadar iyi değildir; kesin tanı parafinde onaylanır.", "isKey": False}
                ],
                "table": {
                    "title": "Frozen (Kriostat) Kesit ile Rutin Parafin Kesit Karşılaştırması",
                    "headers": ["Parametre", "Frozen (Dondurma) Kesit", "Rutin Parafin Kesit"],
                    "rows": [
                        ["Sonuç Çıkış Süresi", "5 - 10 dakika (İntraoperatif)", "24 - 48 saat (Rutin takip)"],
                        ["Doku Durumu", "Taze (kesinlikle fiksatifsiz)", "Formalin fiksasyonlu doku"],
                        ["Sertleştirme Yöntemi", "Fiziksel dondurma (-20°C)", "Dehidrasyon, ksilen ve parafin infiltrasyonu"],
                        ["Morfolojik Kalite", "Kaba, buz kristali artefaktları içerir", "Mükemmel nükleer ve sitoplazmik detay"],
                        ["Temel Endikasyon", "Cerrahi sınır kontrolü, acil malign/benign ayrımı", "Kesin histopatolojik tanı, pTNM evreleme, İHK"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Frozen (intraoperatif konsültasyon) kesit yaklaşık 5-10 dakikada sonuç verir; doku taze dondurulur ancak morfolojisi rutin parafin kadar kaliteli değildir.",
                "📌 [SINAV SPOTU] Frozen kesitin en temel cerrahi endikasyonları: Cerrahi sınır değerlendirmesi ve ameliyat planını değiştirecek benign/malign ayrımıdır.",
                "🚨 [KRİTİK UYARI] Kemik, kalsifiye lezyonlar veya 1 mm'den küçük lezyonlarda doku kaybı riski nedeniyle frozen kesit önerilmez."
            ],
            "medicalTerms": [
                {"term": "Frozen Kesit (Kriostat)", "explanation": "Ameliyat esnasında taze dokunun -20°C'de dondurularak 5-10 dakikada incelenmesidir."},
                {"term": "İntraoperatif Konsültasyon", "explanation": "Ameliyat esnasında cerrahi sınır ve tanı için yapılan acil patolojik değerlendirmedir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Frozen Kesit vs Rutin Parafin Takip Karşılaştırması",
                    "Frozen (Dondurma) Kesit",
                    "Rutin Parafin Kesit",
                    [
                        "5-10 dakika içinde acil sonuç bildirilir",
                        "Doku dondurularak sertleştirilir, kimyasal takip yoktur",
                        "Buz kristalleri nedeniyle hücresel morfoloji zayıftır",
                        "Ameliyat esnasında cerrahi sınırı belirlemek için yapılır"
                    ],
                    [
                        "24 ila 48 saatlik titiz kimyasal takip gerektirir",
                        "Dehidrasyon, ksilen ve parafin emdirilerek sertleştirilir",
                        "Hücre çekirdeği ve sitoplazma detayları kusursuzdur",
                        "Nihai kanser tanısı, pTNM evresi ve İHK testleri için esastır"
                    ]
                ),
                make_micro_quiz(
                    "Meme koruyucu cerrahi operasyonu esnasında cerrahın kitleyi çıkardıktan sonra cerrahi sınırlarda tümör kalıp kalmadığını hasta masadan kalkmadan öğrenmek amacıyla patolojiye başvurduğu intraoperatif yöntem ve yaklaşık sonuç verme süresi nedir?",
                    {
                        "A": "Rutin parafin doku takibi — 48 saat",
                        "B": "Frozen (Kriostat) kesit incelemesi — Yaklaşık 5-10 dakika",
                        "C": "Klinik otopsi — 1 hafta",
                        "D": "Elektron mikroskopisi — 3 gün",
                        "E": "Transgenik hayvan modeli — 1 ay"
                    },
                    "B",
                    {
                        "A": "Yanlış. Rutin parafin takibi 24-48 saat sürer ve ameliyat sırasında beklenemez.",
                        "B": "Doğru. Frozen kesit taze dokunun dondurulmasıyla 5-10 dakikada sonuç veren intraoperatif tanı yöntemidir.",
                        "C": "Yanlış. Hasta hayattadır, otopsi endikasyonu yoktur.",
                        "D": "Yanlış. Elektron mikroskopisi günlerce süren ultrastrüktürel bir tetkiktir.",
                        "E": "Yanlış. Hayvan modeli ameliyatta tanısal amaçla kullanılamaz."
                    }
                ),
                make_cloze(
                    "Ameliyat esnasında cerrahi sınırları belirlemek için dokunun -20°C'de dondurularak 5-10 dakikada incelendiği acil yönteme frozen kesit adı verilir.",
                    "frozen kesit",
                    "Ameliyat içi hızlı dondurma incelemesinin adı"
                )
            ]
        },

        # Adım 79: [TEKRAR SAYFASI - CHECKPOINT 8]
        {
            "slideNumber": 79,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Doku Takibi, Fiksasyon Parametreleri ve Frozen Kesit",
            "subtitle": "Bölüm 8'in fiksasyon biyokimyası, takip basamakları (dehidrasyon, ksilen, parafin), rotary mikrotomi ve frozen kesit konularını toparlayan sentez istasyonu.",
            "badge": "Checkpoint 8",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 8,
            "synthesisNarrative": """Bu kontrol noktası; fiksasyon kurallarını, doku takibi basamaklarını ve frozen kesit tekniğini sentezler.

Doku takibi; hücreleri parafinle doldurarak 3-5 µm kesilebilir kılma sürecidir:
1. ==Fiksasyon:== %10 formalin proteinleri kilitler (hacim 10-20 kat, penetrasyon 1 mm/saat, kalınlık 3-4 mm).
2. ==Dehidrasyon:== Artan alkol serileriyle (%70-%100) su büzüşme olmadan çekilir.
3. ==Şeffaflaştırma:== Ksilen alkolü uzaklaştırarak parafin köprüsü kurar.
4. ==İnfiltrasyon ve Bloklama:== 60°C sıvı parafin emdirilir; deri ve lümen kalıba dik yerleştirilir.
5. ==Mikrotomi ve Frozen:== Rotary mikrotomla 3-5 µm kesit alınır; acilde taze dokudan 5-10 dakikada Frozen kesit raporlanır.

> [BÖLÜM ÖZETİ] Fiksasyon (10-20x) → Alkol (%70-100) → Ksilen → Parafin (60°C) → Dik Bloklama → Rotary Mikrotom (3-5 µm) → Acilde Frozen (5-10 dk).""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Doku Takip Formülü", "desc": "Fiksasyon → Dehidrasyon (Alkol) → Şeffaflaştırma (Ksilen) → İnfiltrasyon (Parafin).", "isKey": True},
                    {"title": "Fiksasyon Standartları", "desc": "%10 formalin, 10-20 kat hacim, 3-4 mm kalınlık, saatte 1 mm penetrasyon.", "isKey": True},
                    {"title": "Frozen Hızı ve Sınırı", "desc": "5-10 dakikada cerrahi sınır kontrolü sağlar; morfolojisi parafin kadar kaliteli değildir.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 8 Histoteknoloji ve Doku Takibi Sentez Tablosu",
                    "headers": ["İşlem / Basamak", "Kullanılan Kimyasal / Cihaz", "Kritik Standart Değer", "En Büyük Hata / Artefakt Riski"],
                    "rows": [
                        ["Fiksasyon (Tespit)", "%10 Nötral Tamponlu Formalin", "Hacim dokunun 10-20 katı", "Yetersiz hacimde otoliz; asit pH'da formalin pigmenti"],
                        ["Dehidrasyon", "Kademeli Etanol (%70→%100)", "Artan dereceli seriler", "Doğrudan %100 alkole atılırsa aşırı büzüşme (plazmoliz)"],
                        ["Şeffaflaştırma", "Ksilen (Ksilol)", "1 - 2 saat ideal süre", "Ksilende aşırı bekletilirse doku taşlaşır ve mikrotomda ufalanır"],
                        ["Bloklama (Gömme)", "Erimiş Parafin (56-60°C)", "Deri ve lümen kalıba DİK oryantasyon", "Yatay gömülürse katmanlar ve invazyon derinliği görülemez"],
                        ["Mikrotomi", "Rotary Mikrotom + Jilet", "3 - 5 mikrometre (µm) kesit", "Körelmiş bıçakla çentik izi, chatter (titreme) çizgileri"],
                        ["Flotasyon Banyosu", "Ilık su banyosu", "40 - 45°C sıcaklık", "Aşırı sıcak suda doku erir ve dağılır"],
                        ["Frozen Kesit", "Kriostat kabini (-20°C)", "5 - 10 dakikada sonuç", "Taze dokuya yanlışlıkla formalin konulması dondurmayı bozar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Doku takip basamakları sırası: Fiksasyon → Dehidrasyon → Şeffaflaştırma → İnfiltrasyon → Gömme.",
                "📌 [SINAV SPOTU] Standart fiksatif %10 formalin, hacmi dokunun 10-20 katı, penetrasyon hızı saatte ~1 mm'dir.",
                "📌 [SINAV SPOTU] Parafin bloktan rotary mikrotomla alınan standart kesit kalınlığı 3-5 mikrondur; frozen kesit ise 5-10 dakikada intraoperatif tanı verir."
            ],
            "medicalTerms": [
                {"term": "Doku Takip Cihazı (Tissue Processor)", "explanation": "Doku kasetlerini otomatik sırayla alkol, ksilen ve parafin banyolarından geçiren cihazdır."},
                {"term": "OCT Maddesi", "explanation": "Frozen kesitte dokunun -20°C'de donarak mikrotom tutucusuna yapışmasını sağlayan jeldir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p8-1",
                    "Histopatolojik doku takibinde Dehidrasyon (Alkol) ve Şeffaflaştırma (Ksilen) basamaklarının birbirini izleyen kimyasal görevleri nelerdir?",
                    "Dehidrasyon kademeli alkol serileriyle (%70-%100) hücre içindeki suyu tamamen uzaklaştırır. Şeffaflaştırma ise hem alkolle hem parafinle karışabilen ksilen ile dokudaki alkolü kovar ve hidrofobik parafinin hücre içine nüfuz edebilmesi için aracı kimyasal köprüyü kurar.",
                    "Su çıkarma ve parafin köprüsü kurma",
                    "Histoteknoloji"
                ),
                make_flashcard(
                    "fc-p8-2",
                    "Fiksasyon işleminde fiksatif hacminin doku hacmine oranı ne olmalıdır ve formalinin ortalama penetrasyon hızı nedir?",
                    "Fiksatif hacmi doku hacminin en az 10 ila 20 katı olmalıdır. Formaldehitin doku içine ortalama penetrasyon (nüfuz etme) hızı ise saatte yaklaşık 1 milimetredir (1 mm/saat). Bu nedenle doku parçaları 3-4 mm'den kalın olmamalıdır.",
                    "10-20 kat hacim ve 1 mm/saat hız",
                    "Fiksasyon Standartları"
                ),
                make_flashcard(
                    "fc-p8-3",
                    "Ameliyat esnasında yapılan Frozen Kesit incelemesinin cerrahiye en büyük katkısı nedir ve neden tüm dokulara rutin olarak uygulanmaz?",
                    "En büyük katkısı 5-10 dakika içinde cerrahi sınırın temiz olup olmadığını ve lezyonun malign/benign ayrımını cerraha bildirerek rezeksiyonun genişletilmesini sağlamaktır. Rutin uygulanmama nedeni ise dondurma sırasında oluşan buz kristalleri nedeniyle morfolojik kalitenin parafin blok kadar kusursuz olmamasıdır.",
                    "Acil cerrahi sınır kontrolü ve morfolojik sınır",
                    "İntraoperatif Konsültasyon"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 8'de incelenen histoteknolojik takip basamakları dikkate alındığında, aşağıdaki aşama - kimyasal ajan eşleştirmelerinden hangisi YANLIŞTIR?",
                    {
                        "A": "Otolizi durdurma ve protein çapraz bağlama → %10 Nötral Tamponlu Formalin",
                        "B": "Suyun hücreden kademeli uzaklaştırılması (Dehidrasyon) → Artan dereceli Etil Alkol serileri",
                        "C": "Alkolü kovup parafinle köprü kurma (Şeffaflaştırma) → Ksilen (Ksilol)",
                        "D": "Doku boşluklarını katılaştırıcı maddeyle doyurma (İnfiltrasyon) → Erimiş Parafin (56-60°C)",
                        "E": "Dondurma (Frozen) kesit alırken dokuyu fikse etme → %100 Mutlak Alkol içinde 24 saat bekletme"
                    },
                    "E",
                    {
                        "A": "Doğru. %10 nötral tamponlu formalin doku tespitinde altın standart fiksatiftir.",
                        "B": "Doğru. Dehidrasyon basamağında kademeli artan etanol serileri kullanılır.",
                        "C": "Doğru. Şeffaflaştırmada ksilen alkolü kovar ve parafin köprüsü kurar.",
                        "D": "Doğru. İnfiltrasyon 56-60°C sıcaklıktaki erimiş parafin banyolarında yapılır.",
                        "E": "Yanlış (aranan cevap): Frozen kesit dokuları kesinlikle fiksatif içine konulmaz; taze dondurularak 5-10 dakikada incelenir."
                    }
                ),
                make_interactive_table(
                    "Doku Takip Ajanları ve Kimyasal Görevleri",
                    ["Takip Basamağı", "Standart Kimyasal", "Moleküler Fonksiyon"],
                    [
                        [
                            ("Fiksasyon (Tespit)", False),
                            ("%10 Nötral Tamponlu Formalin", True, "Rutin fiksatif solüsyon"),
                            ("Metilen köprüleriyle otolizi önleme", False)
                        ],
                        [
                            ("Dehidrasyon", False),
                            ("Kademeli Etanol Serileri", True, "%70-%100 alkol banyoları"),
                            ("Doku içindeki suyu tamamen çekme", False)
                        ],
                        [
                            ("Şeffaflaştırma", False),
                            ("Ksilen (Ksilol)", True, "Aromatik hidrokarbon solvent"),
                            ("Alkolü kovup parafine yol açma", False)
                        ]
                    ]
                )
            ]
        }
    ]
