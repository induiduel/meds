#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 6: Atrofi: Tanım, Etiyoloji ve Fizyolojik/Patolojik Formlar (Adımlar 50 - 59)
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
        # Adım 50
        {
            "slideNumber": 50,
            "title": "Atrofi Tanımı: Hücre Hacmi ve Kütlesindeki Azalma ile Organ Küçülmesi",
            "subtitle": "Atrofi, hücre madde ve boyut kaybı sonucu bir organ veya dokunun hacimce küçülmesidir.",
            "badge": "Temel Tanım",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Atrofi**, daha önce normal gelişimini tamamlamış bir organ veya dokunun, hücre boyutu ve/veya hücre sayısındaki azalma sonucu ==hacimce küçülmesidir==.

Atrofiye uğrayan hücre ölü değildir; fonksiyonel aktivitesi ve metabolik hızı azalmış ancak canlılığını koruyan bir hücredir. Atrofinin temel biyolojik mantığı, azalan kan akımı veya yetersiz besin ortamında hücrenin hayatta kalabilmek için küçülerek enerji tasarrufu sağlamasıdır.

> [TEMEL İLKE] Atrofi bir ölüm süreci değil; kısıtlı kaynaklarla hayatta kalmayı amaçlayan metabolik bir geri çekilme adaptasyonudur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hacimsel Küçülme", "desc": "Hücre içi yapısal protein ve organel kaybıyla hücre küçülür.", "isKey": True},
                    {"title": "Canlılık Korunur", "desc": "Atrofik hücre ölü değildir; düşük enerji düzeyinde hayatta kalır.", "isKey": True},
                    {"title": "Geri Dönüşümlülük", "desc": "Uygun beslenme veya kan akımı sağlandığında doku eski boyutuna dönebilir.", "isKey": False}
                ],
                "table": {
                    "title": "Gelişimsel Kusurlar ve Atrofi Ayrımı",
                    "headers": ["Terim", "Tanım", "Zamanlama / Karakter"],
                    "rows": [
                        ["Atrofi", "Normal gelişmiş organın sonradan küçülmesi", "Edinsel, sonradan gelişen adaptasyon"],
                        ["Hipoplazi", "Organın gelişim sırasında yetersiz büyümesi", "Konjenital, eksik hücre sayısı"],
                        ["Agenesis / Aplazi", "Organ taslağının hiç oluşmaması", "Konjenital, organın tam yokluğu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofi, normal gelişmiş bir organın hücre boyutu ve maddesi kaybıyla sonradan küçülmesidir.",
                "🚨 [KRİTİK UYARI] Hipoplazi konjenital bir eksikliktir; atrofi ise sonradan kazanılan edinsel bir adaptasyondur."
            ],
            "medicalTerms": [
                {"term": "Atrofi", "explanation": "Hücre boyutu ve kütlesindeki azalma sonucu organın sonradan küçülmesidir."},
                {"term": "Hipoplazi", "explanation": "Bir organın embriyonik gelişim sırasında yetersiz kalarak küçük doğmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Normal boyutuna ulaşmış bir organın sonradan hücre kütlesi kaybıyla küçülmesi (atrofi) ile embriyolojik olarak hiç gelişmemesi veya küçük kalması arasındaki temel ayırıcı terim çifti hangisidir?",
                    {
                        "A": "Atrofi sonradan gelişen edinsel küçülmedir; hipoplazi ve aplazi ise doğumsal gelişim defektidir",
                        "B": "Atrofi yalnızca böbreklerde, hipoplazi yalnızca kalpte görülür",
                        "C": "Atrofi malign bir tümördür, aplazi benign bir kisttir",
                        "D": "Atrofide hücre sayısı artar, hipoplazide hücre boyutu artar",
                        "E": "Atrofi geri dönüşsüz bir ölüm şeklidir"
                    },
                    "A",
                    {
                        "A": "Doğru: Atrofi normal gelişmiş organın sonradan küçülmesidir; hipoplazi doğumsal küçüklüktür.",
                        "B": "Yanlış: Tüm dokularda görülebilir.",
                        "C": "Yanlış: İkisi de neoplazi değildir.",
                        "D": "Yanlış: Atrofide boyut/kütle azalır.",
                        "E": "Yanlış: Atrofi uyaran kalkınca geri dönebilen bir adaptasyondur."
                    }
                ),
                make_cloze(
                    "Daha önce normal boyutuna ulaşmış bir organın hücre maddesini kaybederek sonradan küçülmesine [atrofi] adı verilir.",
                    "atrofi",
                    "Edinsel doku küçülmesi terimi"
                )
            ]
        },

        # Adım 51
        {
            "slideNumber": 51,
            "title": "Atrofide Hücre Sayısı vs Hücre Boyutu Azalması Ayrımı",
            "subtitle": "Atrofi hücre boyutunun küçülmesiyle başlar; ileri aşamada apoptozla hücre sayısı da azalabilir.",
            "badge": "Hücresel Dinamik",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atrofi sürecinin başlangıç ve temel bileşeni **hücre boyutundaki küçülmedir**. Hücre, yapısal proteinlerini ve organellerini yıkarak hacmini azaltır; ancak hücre sayısı henüz değişmemiştir.

Eğer atrofiye yol açan stres (örneğin şiddetli iskemi veya tam innervasyon kaybı) çok uzun sürer veya şiddetlenirse, bazı hücreler metabolik krize dayanamaz ve **apoptoz** yoluna girer. Bu durumda organ küçülmesine hem hücre boyutundaki küçülme hem de hücre sayısındaki azalma eşlik eder.

> [TEMEL İLKE] Erken atrofi saf boyut azalmasıdır; kronikleşen ve şiddetlenen atrofide apoptozla hücre sayısı da azalır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Erken Evre", "desc": "Hücre sayısı korunur; hücre içi protein ve mitokondri miktarı azalır.", "isKey": True},
                    {"title": "İleri Evre", "desc": "Enerji krizine dayanamayan hücreler programlı hücre ölümüyle (apoptoz) yok olur.", "isKey": True},
                    {"title": "Kombine Küçülme", "desc": "İleri atrofide hem hücre boyutu hem de hücre sayısı birlikte azalmıştır.", "isKey": False}
                ],
                "table": {
                    "title": "Erken ve İleri Atrofi Karşılaştırması",
                    "headers": ["Parametre", "Erken Evre Atrofi", "İleri / Kronik Atrofi"],
                    "rows": [
                        ["Hücre Boyutu", "Belirgin küçülmüş", "Küçülmüş"],
                        ["Hücre Sayısı", "Değişmemiş (tam korunmuş)", "Azalmış (apoptoz kaybı)"],
                        ["Geri Dönüş Potansiyeli", "Hızlı ve tam iyileşme", "Kısmi iyileşme (kayıp hücreler kalıcıysa skar)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atrofide primer mekanizma hücre boyutunun küçülmesidir; uzayan durumlarda apoptozla sayı da azalır.",
                "📌 [SINAV SPOTU] Atrofik hücre küçülerek oksijen ve besin ihtiyacını minimize eder."
            ],
            "medicalTerms": [
                {"term": "Apoptoz", "explanation": "Hücrenin genetik programıyla çevresine inflamasyon vermeden kendi kendini yok etmesidir."},
                {"term": "Organel Yıkımı", "explanation": "Atrofi sırasında mitokondri ve endoplazmik retikulumun lizozomlarda sindirilmesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Erken Atrofi ile İleri Atrofi Karşılaştırması",
                    "Erken Evre Atrofi",
                    "İleri Evre Atrofi",
                    [
                        "Hücre sayısı tamamen korunmuş",
                        "Yalnızca hücre boyutu küçülmüş",
                        "Uyaran kesilince tam eski boyuta dönüş"
                    ],
                    [
                        "Hücre sayısı apoptozla azalmış",
                        "Hücre boyutu ileri derecede küçülmüş",
                        "Kayıp hücrelerin yerine kısmi fibrozis"
                    ]
                ),
                make_active_recall(
                    "Kronik ve ağır bir atrofide hücre boyutunun küçülmesinin yanı sıra hücre sayısının da azalmasından sorumlu temel mekanizma nedir?",
                    "Programlı hücre ölümü olan apoptoz; aşırı metabolik kısıtlılık altındaki hücrelerin apoptoza gitmesiyle hücre sayısı da azalır."
                )
            ]
        },

        # Adım 52
        {
            "slideNumber": 52,
            "title": "Fizyolojik Atrofi Örnekleri: Notokord, Tiroglossal Kanal ve Uterus İnvolüsyonu",
            "subtitle": "Embriyonik gelişimde ve doğum sonrasında bazı dokular fizyolojik program gereği atrofiye uğrar.",
            "badge": "Fizyolojik Örnek",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atrofi her zaman bir hastalık belirtisi değildir; normal insan yaşam döngüsünün ve embriyogenezisin zorunlu bir parçası olarak **fizyolojik atrofi** gerçekleşir.

Embriyonik dönemde görevini tamamlayan yapılar (notokord, tiroglossal kanal, mezonefroz) programlı atrofi ve apoptozla geriler. Doğumdan sonra ise hormonal desteği aniden kesilen gebelik uterusu hızla küçülerek (involüsyon) normal boyutuna döner. Benzer şekilde laktasyon bitiminde meme bezleri atrofiye uğrar.

> [TEMEL İLKE] Fizyolojik atrofi, embriyogenezde organ şekillenmesini ve doğum sonrası dokuların eski durumuna dönmesini sağlayan normal biyolojik süreçtir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Gelişimsel Gerileme", "desc": "Embriyonik yapıların (tiroglossal kanal, notokord) programlı kaybolmasıdır.", "isKey": True},
                    {"title": "Doğum Sonrası İnvolüsyon", "desc": "Gebelikte büyüyen uterusun doğumdan sonra eski boyutuna küçülmesidir.", "isKey": True},
                    {"title": "Hormon Bağımlılığı", "desc": "Östrojen ve progesteron çekilmesi fizyolojik küçülmeyi tetikler.", "isKey": False}
                ],
                "table": {
                    "title": "Fizyolojik Atrofi Modelleri",
                    "headers": ["Doku / Yapı", "Yaşam Evresi", "Fizyolojik Neden"],
                    "rows": [
                        ["Notokord ve Tiroglossal Kanal", "Embriyonik dönem", "Gelişimsel fonksiyonun tamamlanması"],
                        ["Doğum Sonrası Uterus", "Puerperiyum (doğum lohusalığı)", "Plasental östrojen/progesteron çekilmesi"],
                        ["Laktasyon Sonu Meme", "Sütten kesilme dönemi", "Prolaktin uyarısının ve süt emzirmenin bitmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Doğum sonrası uterusun küçülmesi (involüsyon) fizyolojik atrofidir.",
                "📌 [SINAV SPOTU] Embriyogenezde notokord ve duktus arteriosusun gerilemesi fizyolojik atrofiye örnektir."
            ],
            "medicalTerms": [
                {"term": "İnvolüsyon", "explanation": "Gebelikte veya fonksiyonel periyotta büyüyen bir organın fizyolojik olarak küçülmesidir."},
                {"term": "Tiroglossal Kanal", "explanation": "Tiroid bezinin dil kökünden boyuna iniş yolu olan ve sonradan atrofiye uğrayan kanaldır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Doğumdan hemen sonra 1000 gram ağırlığındaki uterusun hormonların çekilmesiyle birkaç hafta içinde 60-70 gramlık normal boyutuna dönmesi hangi adaptasyon sürecidir?",
                    {
                        "A": "Fizyolojik atrofi (involüsyon)",
                        "B": "Patolojik denervasyon atrofisi",
                        "C": "Kazeöz nekroz",
                        "D": "Skuamöz metaplazi",
                        "E": "Malign lenfoma infiltrasyonu"
                    },
                    "A",
                    {
                        "A": "Doğru: Doğum sonrası uterusun küçülmesi hormon çekilmesine bağlı fizyolojik atrofidir (involüsyon).",
                        "B": "Yanlış: Sinir hasarı yoktur, hormonal fizyolojik süreçtir.",
                        "C": "Yanlış: Enfeksiyöz nekroz değildir.",
                        "D": "Yanlış: Hücre tipi değişmez.",
                        "E": "Yanlış: Neoplazi değildir."
                    }
                ),
                make_cloze(
                    "Gebelikte büyüyen uterusun doğum sonrasında hormonların çekilmesiyle küçülerek normal boyutuna dönmesine [involüsyon] adı verilir.",
                    "involüsyon",
                    "Doğum sonrası küçülme terimi"
                )
            ]
        },

        # Adım 53
        {
            "slideNumber": 53,
            "title": "Kullanılmama Atrofisi (Disuse Atrophy): İmmobilizasyon ve Alçı Etkisi",
            "subtitle": "Kasın hareketsiz kalması veya yük taşımaması hızla miyofibril kaybı ve kullanılmama atrofisi doğurur.",
            "badge": "Mekanik Atrofi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Kas dokusu sürekli mekanik uyarım ve kasılma ile kütlesini korur. Kemik kırığı nedeniyle bir ekstremite alçıya alındığında veya hasta uzun süre yatağa bağımlı kaldığında **kullanılmama atrofisi (disuse atrophy)** hızla gelişir.

Kas liflerinin kasılmaması protein sentezini düşürürken ubikuitin-proteazom aracılı protein yıkımını hızlandırır. Kas liflerinin çapı incelir ve kas kütlesi hızla erir. Kemiklerde de yük binmemesine bağlı olarak trabeküler rezorpsiyon ve lokalize osteoporoz gelişir.

> [KLİNİK İPUCU] Alçı çıkarıldıktan sonra yapılan fizik tedavi ve egzersiz, kullanılmama atrofisini tamamen geri çevirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mekanik Uyarı Kaybı", "desc": "Kas liflerinin kasılmaması protein sentez hızını dramatik düşürür.", "isKey": True},
                    {"title": "Lif Çapı İncelmesi", "desc": "Miyofibril sayısı azalır; kas incelir ancak sinirsel ileti sağlamdır.", "isKey": True},
                    {"title": "Kemik Rezorpsiyonu", "desc": "Uzun süreli immobilizasyonda kemik kalsiyumu kaybedilerek osteoporoz gelişir.", "isKey": False}
                ],
                "table": {
                    "title": "Kullanılmama Atrofisinin Dokusal Dağılımı",
                    "headers": ["Doku", "Patolojik Değişim", "Klinik Yansıma"],
                    "rows": [
                        ["İskelet Kası", "Miyofibril kaybı, lif çapında incelme", "Ekstremite çevresinde küçülme, kas güçsüzlüğü"],
                        ["Kemik Dokusu", "Osteoklastik rezorpsiyon artışı", "Lokalize kullanılmama osteoporozu"],
                        ["Eklem Kıkırdağı", "Sinovyal sıvı hareketinin azalması", "Eklem sertliği ve kontraktür riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kırık nedeniyle alçıya alınan kolda kas kitlesinin erimesi kullanılmama atrofisine (disuse atrophy) örnektir.",
                "📌 [SINAV SPOTU] Kullanılmama atrofisinde sinir iletimi tamamen normaldir; sorun kasılma yükünün olmamasıdır."
            ],
            "medicalTerms": [
                {"term": "Disuse Atrophy", "explanation": "İş yükünün ve mekanik hareketin azalması sonucu kas ve kemikte gelişen küçülmedir."},
                {"term": "İmmobilizasyon", "explanation": "Bir vücut bölümünün veya tüm vücudun hareket kabiliyetinin kısıtlanmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Alçı Sonrası Kullanılmama Atrofisi Kaskadı",
                    [
                        "1. İmmobilizasyon: Kırık tespiti için bacağın alçıya alınması.",
                        "2. Mekanik Sessizlik: Kas liflerinde kasılma ve gerilim uyarısının sıfırlanması.",
                        "3. Protein Yıkımı: Ubikuitin ligazların (MuRF1) aktifleşerek miyofibrilleri parçalaması.",
                        "4. Lif İncelmesi: Çizgili kas liflerinin çapının küçülmesi ve kas kütlesinin erimesi.",
                        "5. İyileşme (Reversibilite): Alçı açılıp egzersiz başladığında liflerin eski boyutuna dönmesi."
                    ]
                ),
                make_cloze(
                    "Kemik kırığı sonrası alçıya alınan kolda hareket kısıtlılığına bağlı gelişen kas erimesine [kullanılmama] atrofisi denir.",
                    "kullanılmama",
                    "Hareketsizlik atrofisi adı"
                )
            ]
        },

        # Adım 54
        {
            "slideNumber": 54,
            "title": "Denervasyon Atrofisi: Motor Nöron ve Periferik Sinir Hasarı",
            "subtitle": "İskelet kası liflerinin trofik motor sinir desteğini kaybetmesi en ağır kas atrofisine yol açar.",
            "badge": "Nörolojik Atrofi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """İskelet kasının normal metabolizması ve sağkalımı, alt motor nörondan gelen **trofik sinirsel uyarılara** kesin olarak bağımlıdır.

Bir periferik sinir kesildiğinde, spinal kord ön boynuz motor nöronları haraplandığında (örneğin poliomyelit veya ALS'de) inerve ettikleri kas lifleri derhal **denervasyon atrofisine** girer. Kas lifleri hızla incelir, kasılma proteinlerinin %80-90'ı birkaç ay içinde yıkılır ve kas lifleri mikroskopta küçük köşeli, üçgenimsi şekiller alır.

> [TEMEL İLKE] Denervasyon atrofisi kullanılmama atrofisinden çok daha hızlı ve yıkıcıdır; sinir onarılmazsa lifler ölerek yerini yağ dokusuna bırakır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Trofik Sinyal Kaybı", "desc": "Sinir uçlarından salınan asetilkolin ve trofik faktörlerin kesilmesidir.", "isKey": True},
                    {"title": "Köşeli Lifler", "desc": "Mikroskopta kas lifleri büzüşerek karakteristik küçük köşeli lif morfolojisi alır.", "isKey": True},
                    {"title": "Klinik Örnekler", "desc": "Polio sekeli, ALS hastalığı, travmatik sinir kesileri.", "isKey": False}
                ],
                "table": {
                    "title": "Kullanılmama Atrofisi vs Denervasyon Atrofisi",
                    "headers": ["Parametre", "Kullanılmama Atrofisi", "Denervasyon Atrofisi"],
                    "rows": [
                        ["Sinir Bağlantısı", "Tamamen sağlam ve fonksiyonel", "Kesilmiş veya nöron ölmüş"],
                        ["İlerleme Hızı", "Yavaş ve orta dereceli", "Çok hızlı ve derin doku kaybı"],
                        ["Histopatoloji", "Yuvarlak homojen incelmiş lifler", "Küçük köşeli (angular) lif demetleri"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sinir kesisi veya motor nöron ölümü (polio, ALS) sonrası gelişen kas erimesine denervasyon atrofisi denir.",
                "📌 [SINAV SPOTU] Denervasyon atrofisinde mikroskopik olarak küçük köşeli (angular) kas lifleri karakteristiktir."
            ],
            "medicalTerms": [
                {"term": "Denervasyon", "explanation": "Bir organ veya kasın motor sinir bağlantısının kopması veya hasarlanmasıdır."},
                {"term": "Trofik Faktör", "explanation": "Sinirler tarafından salgılanarak hedef kasın beslenmesini ve canlılığını sağlayan maddedir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Kullanılmama Atrofisi ile Denervasyon Atrofisi Karşılaştırması",
                    "Kullanılmama Atrofisi (Alçı)",
                    "Denervasyon Atrofisi (Sinir Kesisi)",
                    [
                        "Motor sinir uyarımı ve ileti tam sağlam",
                        "Yalnızca mekanik iş yükü eksik",
                        "Kas lifleri yuvarlak formunu korur"
                    ],
                    [
                        "Motor sinir tamamen hasarlı / kesik",
                        "Trofik sinirsel besleme tamamen kesilmiş",
                        "Kas lifleri büzüşüp küçük köşeli şekil alır"
                    ]
                ),
                make_cloze(
                    "Poliomyelit enfeksiyonu veya periferik sinir kesisi sonrası kaslarda gelişen hızlı erimeye [denervasyon] atrofisi denir.",
                    "denervasyon",
                    "Sinir kaybı atrofisi terimi"
                )
            ]
        },

        # Adım 55
        {
            "slideNumber": 55,
            "title": "İskemik Atrofi: Kronik Aterosklerotik Kan Akımı Azalması",
            "subtitle": "Arteriyel lümenin aterosklerozla yavaş daralması dokularda kronik iskemiye bağlı atrofi oluşturur.",
            "badge": "Vasküler Atrofi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücrelerin yaşaması için gereken oksijen ve besin maddeleri arteriyel kan akımıyla taşınır. Arterin ani ve tam tıkanması nekroza (enfarktüs) yol açarken; **yavaş ve ilerleyici kan akımı azalması** dokuda **iskemik atrofiye** neden olur.

En klasik örneği yaşlılarda ateroskleroza bağlı gelişen beyin ve böbrek atrofisidir. Renal arterin aterosklerotik darlığında böbrek küçülür, nefron tübülleri atrofiye uğrar ve interstisyel fibrozis gelişir. Hücreler ölmemek için boyutlarını küçülterek azalan oksijene adapte olur.

> [TEMEL İLKE] Akut tam iskemi nekroz yaparken; kronik kısmi iskemi hücrelerin küçülerek hayatta kaldığı iskemik atrofi yapar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Yavaş Akım Azalması", "desc": "Aterom plağı lümeni yıllar içinde yavaş yavaş daraltır.", "isKey": True},
                    {"title": "Metabolik Kısılma", "desc": "Hücre azalan oksijenle yaşayabilmek için metabolizma hızını düşürür.", "isKey": True},
                    {"title": "Organ Örnekleri", "desc": "Aterosklerotik senil beyin atrofisi, iskemik böbrek atrofisi.", "isKey": False}
                ],
                "table": {
                    "title": "Akut İskemi vs Kronik İskemi Sonuçları",
                    "headers": ["İskemi Tipi", "Damarsal Süreç", "Doku Yanıtı"],
                    "rows": [
                        ["Akut Tam İskemi", "Tromboz veya emboliyle ani tam oklüzyon", "Enfarktüs ve koagülasyon nekrozu"],
                        ["Kronik Kısmi İskemi", "Aterosklerozla yavaş daralma", "İskemik atrofi ve parankim kaybı"],
                        ["Geçici İskemi", "Vazospazm veya geçici basınç düşüşü", "Geri dönüşümlü hücresel şişme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yavaş ilerleyen ateroskleroz iskemik atrofi yapar; ani damar tıkanması ise nekroz (enfarktüs) yapar.",
                "📌 [SINAV SPOTU] Renal arter darlığında böbreğin küçülmesi iskemik atrofidir."
            ],
            "medicalTerms": [
                {"term": "İskemik Atrofi", "explanation": "Kronik kan akımı ve oksijen azlığına bağlı doku parankiminin küçülmesidir."},
                {"term": "Ateroskleroz", "explanation": "Büyük ve orta boy arterlerin intima tabakasında lipid ve fibröz plak oluşumudur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bir organda arteriyel kan akımının yavaş ve ilerleyici biçimde azalması (örneğin ateroskleroz) ile ani tam tıkanması arasındaki patolojik sonuç farkı nedir?",
                    {
                        "A": "Yavaş azalma iskemik atrofi yaparken, ani tıkanma iskemik nekroz (enfarktüs) yapar",
                        "B": "Yavaş azalma doğrudan hiperplazi yapar, ani tıkanma hiçbir hasar vermez",
                        "C": "Her iki durum da istisnasız kazeöz granülomatöz nekrozla sonuçlanır",
                        "D": "Yavaş azalma hücre boyutunu katlar, ani tıkanma hücreyi küçültür",
                        "E": "Yavaş azalma yalnızca karaciğerde görülür"
                    },
                    "A",
                    {
                        "A": "Doğru: Kronik yavaş iskemi adaptif atrofi yapar; akut tam tıkanma nekroz (enfarktüs) yapar.",
                        "B": "Yanlış: İskemi hiperplazi yapmaz.",
                        "C": "Yanlış: Kazeöz nekroz tüberküloza aittir.",
                        "D": "Yanlış: İskemi hipertrofi yapmaz.",
                        "E": "Yanlış: Tüm arteriyel organlarda görülür."
                    }
                ),
                make_cloze(
                    "Arteriyel lümenin aterosklerozla yavaş daralması sonucu dokuların azalan oksijene küçülerek uyum sağlamasına [iskemik] atrofi denir.",
                    "iskemik",
                    "Kan akımı yetersizliği türü"
                )
            ]
        },

        # Adım 56
        {
            "slideNumber": 56,
            "title": "Yetersiz Beslenme Atrofisi (Kaşeksi): Malnütrisyon ve Kanser Kaşeksisi",
            "subtitle": "Yetersiz protein alımı ve kronik hastalıklarda sitokin salınımı yaygın kas ve yağ atrofisi oluşturur.",
            "badge": "Metabolik Kaşeksi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Şiddetli protein ve kalori malnütrisyonunda (marasmus, açlık) vücut hayati organları (beyin, kalp) besleyebilmek için iskelet kasını enerji kaynağı olarak kullanır. Kas proteinleri parçalanarak amino asitlere çevrilir ve **genel kas atrofisi** gelişir.

İleri evre kanser hastalarında ve kronik enfeksiyonlarda (tüberküloz, AIDS) görülen **kaşeksi** tablosunda ise tümörden ve konak makrofajlarından salınan **TNF-α (kaşektin)** ve **IL-6** gibi proinflamatuvar sitokinler iştahı baskılar ve kas yıkımını patolojik düzeyde hızlandırır.

> [KLİNİK İPUCU] Kanser kaşeksisinde kas erimesi yalnızca iştahsızlıktan değil, TNF-alfa'nın ubikuitin-proteazom sistemini doğrudan ateşlemesinden kaynaklanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Protein Açlığı", "desc": "Kalori yetersizliğinde kas proteinleri katabolize edilerek enerji sağlanır.", "isKey": True},
                    {"title": "TNF-α (Kaşektin)", "desc": "Tümör ilişkili kaşekside kas ve yağ yıkımını tetikleyen temel sitokindir.", "isKey": True},
                    {"title": "Sarkopeni", "desc": "Ağır kas kütlesi kaybı solunum kaslarını da zayıflatarak ölüme yol açar.", "isKey": False}
                ],
                "table": {
                    "title": "Açlık Malnütrisyonu vs Kanser Kaşeksisi",
                    "headers": ["Parametre", "Basit Açlık / Malnütrisyon", "Kanser Kaşeksisi"],
                    "rows": [
                        ["Temel Neden", "Besin ve kalori alım eksikliği", "Sistemik inflamasyon ve proinflamatuvar sitokinler"],
                        ["Kilit Sitokin", "Sitokin artışı yok, metabolik yavaşlama", "Aşırı yüksek TNF-alfa ve IL-6"],
                        ["Beslenmeyle Düzelme", "Yüksek proteinle hızla düzelir", "Yalnızca beslenme desteğiyle kolay düzelmez"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kanser kaşeksisinde yaygın kas ve yağ dokusu atrofisini tetikleyen ana sitokin TNF-alfa (kaşektin)'dır.",
                "📌 [SINAV SPOTU] Protein-enerji malnütrisyonunda kas proteinleri enerji elde etmek amacıyla katabolize edilir."
            ],
            "medicalTerms": [
                {"term": "Kaşeksi", "explanation": "Kronik hastalıklarda aşırı kilo kaybı, kas erimesi ve iştahsızlıkla giden tükenmişlik tablosudur."},
                {"term": "TNF-alfa (Kaşektin)", "explanation": "İştahı kesen ve kas protein yıkımını hızlandıran proinflamatuvar sitokindir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kanser Kaşeksisinde Kas Yıkımı Kaskadı",
                    [
                        "1. Tümör İlerlemesi: Malign tümör ve lökositlerden yoğun TNF-alfa ve IL-6 salgısı.",
                        "2. Hipotalamik Baskı: İştah merkezinin baskılanması ve anoreksi gelişimi.",
                        "3. Proteazom Uyarımı: Sitokinlerin kas hücrelerinde E3 ubikuitin ligazları aktive etmesi.",
                        "4. Aktin-Miyozin Yıkımı: İskelet kası proteinlerinin 26S proteazomda amino asitlere parçalanması.",
                        "5. Kaşeksi Tablosu: Hastada ileri derecede kas erimesi, halsizlik ve genel atrofi oturması."
                    ]
                ),
                make_cloze(
                    "Kanser hastalarında yaygın kas atrofisi ve kilo kaybına (kaşeksi) yol açan ana sitokine [TNF-alfa] (kaşektin) adı verilir.",
                    "TNF-alfa",
                    "Kaşektin olarak bilinen sitokin kısaltması"
                )
            ]
        },

        # Adım 57
        {
            "slideNumber": 57,
            "title": "Endokrin Uyarım Kaybı Atrofisi: Menopoz Sonrası Over ve Endometrium",
            "subtitle": "Hormon bağımlı dokular trofik endokrin uyaranın kesilmesiyle atrofiye uğrar.",
            "badge": "Hormon Yokluğu",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Meme, endometriyum, vajina ve prostat gibi hormon bağımlı organlar canlılık ve yapılarını sürdürebilmek için trofik hormon desteğine ihtiyaç duyar. Bu hormonlar azaldığında veya kesildiğinde **endokrin atrofi** gelişir.

Menopoz döneminde overlerde folikül tükenmesi sonucu östrojen üretimi durur. Trofik desteğini kaybeden **endometriyum incelir ve atrofik** hale gelir; bezler küçülür veya kistik genişlemiş tek sıra yassı epitele döner (senil kistik atrofi). Vajinal mukoza incelir, meme glandları geriler ve overler büzüşerek fibröz bir kitleye dönüşür.

> [TEMEL İLKE] Hormon bağımlı dokularda trofik hormon çekilmesi fizyolojik olarak atrofi ve hücresel büzüşme ile sonuçlanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Trofik Sinyal Yokluğu", "desc": "Östrojen eksikliği hedef hücrelerde protein sentezini durdurur.", "isKey": True},
                    {"title": "Senil Kistik Atrofi", "desc": "Postmenopozal endometriumda bezler kistik genişler ancak epitel incelmiştir.", "isKey": True},
                    {"title": "Organ Küçülmesi", "desc": "Uterus ve overler menopoz sonrası gençlik boyutlarının yarısına iner.", "isKey": False}
                ],
                "table": {
                    "title": "Menopoz Sonrası Kadın Genital Traktus Atrofisi",
                    "headers": ["Organ", "Hormon Öncesi Durum", "Menopoz Sonrası Atrofik Durum"],
                    "rows": [
                        ["Endometrium", "Kalın, bol bezli, mitotik", "İnce, tek sıra yassı epitel, kistik atrofi"],
                        ["Vajina Mukozası", "Çok katlı glikojenden zengin yassı epitel", "İncelmiş, soluk, atrofik vajinit tablosu"],
                        ["Overler", "Gelişen foliküller, korpus luteum", "Büzüşmüş, beyaz, fibröz skar dokusu (korpus albikans)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Menopoz sonrası endometrium, uterus ve memenin küçülmesi endokrin uyarım kaybı atrofisidir.",
                "📌 [SINAV SPOTU] Postmenopozal kistik atrofik endometriumda bezler geniştir ancak epitel tek katlı yassılaşmıştır (mitoz yoktur)."
            ],
            "medicalTerms": [
                {"term": "Endokrin Atrofi", "explanation": "Hedef organı besleyen trofik hormonların azalması veya kesilmesiyle gelişen küçülmedir."},
                {"term": "Kistik Atrofi", "explanation": "Atrofik endometriyumda bezlerin kistik genişleyip epitelinin yassılaşmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Üreme Çağı ve Postmenopozal Endometrium Karşılaştırması",
                    "Üreme Çağı Endometriyumu",
                    "Postmenopozal Atrofik Endometriyum",
                    [
                        "Aktif östrojen ve progesteron uyarımı",
                        "Kalın fonksiyonel tabaka ve bol mitoz",
                        "Siklik kanama ve dökülme periyotları"
                    ],
                    [
                        "Östrojen desteği tamamen kesilmiş",
                        "İnce bazal tabaka, tek sıra yassı bezler",
                        "Mitotik aktivite sıfır, kistik küçülme"
                    ]
                ),
                make_cloze(
                    "Menopoz sonrası östrojenin kesilmesiyle endometriyum ve memede gelişen küçülmeye [endokrin] uyarım kaybı atrofisi denir.",
                    "endokrin",
                    "Hormonal sistem kaynaklı atrofi adı"
                )
            ]
        },

        # Adım 58
        {
            "slideNumber": 58,
            "title": "Yaşlanma Atrofisi (Senil Atrofi): Beyin Atrofisi, Genişleyen Sulkuslar ve Daralan Giruslar",
            "subtitle": "Yaşlanma sürecinde hücre kaybı ve kronik vasküler yetersizlik beyinde senil atrofi oluşturur.",
            "badge": "Senil Dejenerasyon",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Yaşlanma ile birlikte dokularda hücre çoğalma kapasitesi azalır, protein birikimi artar ve damarsal perfüzyon düşer. Bu sürecin en dramatik görüldüğü organ insan **beynidir (senil beyin atrofisi)**.

Yaşlanan beyinde nöron kaybı ve aksonal büzüşme sonucu beyin kütlesi belirgin biçimde hafifler. Makroskobik incelemede kortikal **giruslar incelip daralırken**, giruslar arasındaki **sulkuslar patolojik olarak genişler**. Beyin parankiminin çekilmesiyle lateral ventriküller telafi edici olarak genişler (**hidrosefali ex vacuo**).

> [KLİNİK İPUCU] Yaşlı bir hastanın beyin BT/MRG incelemesinde girusların daralması ve sulkusların açılması senil atrofiyi yansıtır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kortikal İncelme", "desc": "Nöron kaybıyla serebral korteks kalınlığı ve girus genişliği daralır.", "isKey": True},
                    {"title": "Genişleyen Sulkuslar", "desc": "Giruslar küçüldükçe aralarındaki sulkus yarıkları belirginleşir ve derinleşir.", "isKey": True},
                    {"title": "Hidrosefali Ex Vacuo", "desc": "Beyin kütlesi küçüldüğü için boşalan hacmi ventriküler BOS doldurur.", "isKey": False}
                ],
                "table": {
                    "title": "Genç Beyin vs Senil Atrofik Beyin",
                    "headers": ["Ölçüt", "Genç Sağlıklı Beyin", "Senil Atrofik Beyin"],
                    "rows": [
                        ["Beyin Ağırlığı", "1300 - 1400 gram", "1000 - 1150 gram (hafiflemiş)"],
                        ["Girus Morfolojisi", "Dolgun, geniş, birbirine yapışık", "İncelmiş, bıçak sırtı gibi daralmış"],
                        ["Sulkus Açıklığı", "Dar, kapalı yarıklar", "Genişlemiş, belirgin boşluklar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Senil beyin atrofisinde makroskobik olarak giruslar daralır, sulkuslar genişler.",
                "📌 [SINAV SPOTU] Beyin kütle kaybına bağlı ventriküllerin genişlemesine hidrosefali ex vacuo adı verilir."
            ],
            "medicalTerms": [
                {"term": "Senil Atrofi", "explanation": "İleri yaşlanmaya ve azalan damarlanmaya bağlı dokuların küçülmesidir."},
                {"term": "Hidrosefali Ex Vacuo", "explanation": "Beyin doku kaybı nedeniyle oluşan boşluğun telafi amaçlı BOS ile dolmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Genç Beyin ile Senil Atrofik Beyin Morfolojisi",
                    "Genç Yetişkin Beyni",
                    "Senil Atrofik Yaşlı Beyni",
                    [
                        "Beyin ağırlığı 1350-1400 gram",
                        "Geniş ve dolgun kortikal giruslar",
                        "Dar ve sıkı sulkuslar, küçük ventriküller"
                    ],
                    [
                        "Beyin ağırlığı 1000-1100 gram",
                        "Daralmış ve incelmiş kortikal giruslar",
                        "Derin geniş sulkuslar ve genişlemiş ventriküller"
                    ]
                ),
                make_cloze(
                    "Senil beyin atrofisinde nöron kaybı sonucu kortikal giruslar daralırken aralarındaki [sulkuslar] genişler.",
                    "sulkuslar",
                    "Beyin yarıkları anatomik adı"
                )
            ]
        },

        # Adım 59 (CHECKPOINT 6)
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Atrofinin Nedenleri ve Klinik Görünümleri",
            "subtitle": "Atrofi kavramını, fizyolojik involüsyonu, kullanılmama/denervasyon ayrımını ve senil değişiklikleri pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 6,
            "synthesisNarrative": """Bu bölümde atrofinin tanımını, hücresel dinamiklerini ve başlıca etiyolojik tiplerini inceledik.

Atrofi normal gelişmiş organın hücre maddesi kaybıyla sonradan küçülmesidir. Fizyolojik formu embriyogenezde ve doğum sonrası uterus involüsyonunda görülür. Patolojik tipleri arasında hareketsizliğe bağlı kullanılmama atrofisi, motor sinir hasarına bağlı denervasyon atrofisi (köşeli lifler), kronik ateroskleroza bağlı iskemik atrofi, TNF-α aracılı kaşeksi, menopozda endokrin atrofi ve yaşlılıkta beyin atrofisi (daralan giruslar, genişleyen sulkuslar) yer alır.

> [TEKRAR SPOTU] Atrofik hücre metabolik hızını kısıp küçülerek hayatta kalır; stres aşırı uzarsa apoptozla doku kaybı derinleşir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Temel Nedenler", "desc": "İş yükü kaybı, denervasyon, iskemi, malnütrisyon, hormon kaybı ve yaşlanma.", "isKey": True},
                    {"title": "Nörolojik Ayrım", "desc": "Denervasyon atrofisi kullanılmama atrofisine göre çok daha hızlı ve köşeli liflerle seyreder.", "isKey": True},
                    {"title": "Senil Beyin", "desc": "Giruslar daralır, sulkuslar genişler, hidrosefali ex vacuo gelişir.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 6 Sentez Tablosu",
                    "headers": ["Atrofi Tipi", "Etiyolojik Mekanizma", "Karakteristik Örnek"],
                    "rows": [
                        ["Kullanılmama (Disuse)", "Mekanik iş yükü kaybı", "Alçıya alınan bacak kasları"],
                        ["Denervasyon", "Trofik motor sinir kaybı", "Polio veya periferik sinir kesisi"],
                        ["İskemik", "Yavaş damar daralması", "Aterosklerotik küçülmüş böbrek"],
                        ["Senil", "Yaşlanma ve hücre kaybı", "Beyin atrofisi (dar girus, geniş sulkus)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kırık alçısı kullanılmama atrofisi, sinir kesisi denervasyon atrofisidir.",
                "📌 [SINAV SPOTU] Senil beyin atrofisinde giruslar daralır, sulkuslar genişler."
            ],
            "medicalTerms": [
                {"term": "Atrofi", "explanation": "Hücre boyutu ve kütlesindeki azalmayla organın sonradan küçülmesidir."},
                {"term": "Kaşeksi", "explanation": "Kronik hastalıklarda sitokinlerle tetiklenen ağır kas ve yağ atrofisidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc16",
                    "Atrofi ile hipoplazi arasındaki en temel kavramsal ve patolojik fark nedir?",
                    "Atrofi daha önce normal boyutuna ulaşmış bir organın sonradan hücre kaybıyla küçülmesidir; hipoplazi ise organın embriyonik gelişim sırasında doğumsal olarak küçük kalmasıdır."
                ),
                make_flashcard(
                    "k1-03-fc17",
                    "Kullanılmama atrofisi (disuse) ile denervasyon atrofisi arasındaki temel klinikopatolojik fark nedir?",
                    "Kullanılmama atrofisinde sinir bağlantısı tamamen sağlamdır ve süreç yavaştır; denervasyon atrofisinde motor sinir kopmuştur, erime çok daha hızlıdır ve kas lifleri mikroskopta küçük köşeli şekil alır."
                ),
                make_flashcard(
                    "k1-03-fc18",
                    "Yaşlı bir hastanın otopsisinde senil beyin atrofisinin makroskobik tanı kriterleri nelerdir?",
                    "Beyin ağırlığının belirgin azalması, serebral korteks giruslarının incelip daralması ve aralarındaki sulkusların patolojik olarak genişlemesidir."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kanser kaşeksisinde gözlenen yaygın kas atrofisinde rol oynayan ve 'kaşektin' olarak da bilinen anahtar sitokin hangisidir?",
                    "Tümör Nekroz Faktörü-alfa (TNF-α), iştahı keserek ve kaslarda ubikuitin-proteazom yıkımını uyararak kaşeksiye yol açan ana sitokindir."
                )
            ]
        }
    ]
