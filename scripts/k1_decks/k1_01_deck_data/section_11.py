#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 11: Derste Örneklenen Temel Sendromlar ve Sınav Sentezi (Adım 87 - 100)
"""

from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall
)

def get_steps():
    return [
        {
            "slideNumber": 89,
            "title": "Frajil X Sendromu Moleküler Mekanizması: FMR1 Geni ve Dinamik CGG Tekrar Artışı",
            "subtitle": "Kalıtsal zihinsel geriliğin en sık monogenik nedeni ve dinamik mutasyon doğası",
            "badge": "Dinamik Mutasyon",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Frajil X Sendromu; erkek çocuklarında Down sendromundan sonra zeka geriliğinin en sık ikinci genetik nedeni, kalıtsal (monogenik) zihinsel yetersizliğin ise EN SIK BİRİNCİ nedenidir:\n\n- **Moleküler Mekanizma (Dinamik Trinükleotid Tekrarı):** Xq27.3 bölgesindeki **FMR1** geninin 5' UTR bölgesinde yer alan **CGG** trinükleotid tekrar sayısının patolojik artışıdır:\n  - **Normal Birey:** 5 - 44 tekrar.\n  - **Gri Zon:** 45 - 54 tekrar.\n  - **Premutasyon:** 55 - 200 tekrar (gen metillenmemiştir ancak sonraki kuşaklara aktarılırken anneden geçerken tam mutasyona genişleyebilir).\n  - **Tam Mutasyon:** >200 tekrar. Gen promötörü aşırı CpG metilasyonuna uğrar, FMR1 geni susturulur ve sinaps gelişiminde kritik olan **FMRP proteini üretilemez**.",
            "coreContent": {
                "table": {
                    "title": "FMR1 Geninde CGG Tekrar Sayısı Basamakları",
                    "headers": ["Durum", "CGG Tekrar Sayısı", "Metilasyon Durumu", "Klinik Fenotip"],
                    "rows": [
                        ["Normal", "5 - 44 tekrar", "Metilasyon Yok", "Tamamen normal, sağlıklı"],
                        ["Gri Zon", "45 - 54 tekrar", "Metilasyon Yok", "Sağlıklı, hafif instabilite"],
                        ["Premutasyon", "55 - 200 tekrar", "Metilasyon Yok (RNA toksisitesi)", "FXTAS (Ataksi) ve FXPOI (Erken Menopoz)"],
                        ["Tam Mutasyon", ">200 tekrar", "HİPERMETİLASYON (Gen susturuldu)", "Klasik Frajil X Sendromu (Zeka geriliği + Makroorşidizm)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "FMR1 Geni", "explanation": "Frajil X zihinsel gerilik proteinini (FMRP) kodlayan, CGG tekrar artışıyla susturulan gen."},
                {"term": "CGG Tekrarı", "explanation": "FMR1 geninde 200'ün üzerine çıktığında hipermetilasyonla gen inaktivasyonuna yol açan triplet dizisi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalıtsal zihinsel geriliğin en sık nedeni Frajil X sendromudur; FMR1 geninde >200 CGG tekrar artışı ve promötör metilasyonu ile seyreder."
            ],
            "interactiveElements": [
                make_cloze(
                    "Frajil X sendromunda patogenezden sorumlu dinamik mutasyon FMR1 geninin 5' UTR bölgesindeki [CGG] trinükleotid tekrar artışıdır.",
                    "CGG",
                    "Sitozin-Guanin-Guanin nükleotid tripleti",
                    "FMR1 geninde CGG tekrar sayısı 200'ü aştığında DNA hipermetillenir ve FMRP proteini sentezlenemez."
                ),
                make_micro_quiz(
                    "FMR1 geninde CGG trinükleotid tekrar sayısı 200'ün üzerine çıktığında genin susturulmasına ve Frajil X sendromu fenotipinin ortaya çıkmasına yol açan epigenetik mekanizma hangisidir?",
                    {
                        "A": "Promötör bölgesinin hipermetilasyonu (CpG adacıkları metilasyonu)",
                        "B": "Histon asetilasyonu artışı",
                        "C": "Translasyon hızlanması",
                        "D": "Gen delesyonu"
                    },
                    "A",
                    {
                        "A": "Doğru! 200 tekrar aşıldığında promötördeki CpG adacıkları yoğun şekilde metillenir; gen transkripsiyonu tamamen durur ve FMRP proteini yok olur.",
                        "B": "Yanlış. Histon asetilasyonu geni açar, susturmaz.",
                        "C": "Yanlış. Translasyon durur.",
                        "D": "Yanlış. Bu bir delesyon değil dinamik tekrar artışıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 90,
            "title": "Frajil X Premutasyon Taşıyıcıları: FXTAS ve FXPOI Sendromları",
            "subtitle": "55-200 tekrar aralığındaki bireylerde görülen erişkin başlangıçlı patolojiler",
            "badge": "Premutasyon Kliniği",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "FMR1 premütasyon taşıyıcıları (55-200 CGG tekrarı) klasik Frajil X zihinsel yetersizliğini göstermezler; ancak aşırı miktarda üretilen anormal FMR1 mRNA'sının çekirdekte birikmesi (RNA toksisitesi) nedeniyle iki önemli hastalığa yakalanırlar:\n\n- **1. FXPOI (Fragile X-associated Primary Ovarian Insufficiency):** Premutasyon taşıyıcısı kadınların yaklaşık %20'sinde 40 yaşından önce gelişen **erken menopoz ve over yetmezliğidir**.\n- **2. FXTAS (Fragile X-associated Tremor/Ataxia Syndrome):** 50 yaş üzerindeki premutasyon taşıyıcısı erkeklerin yaklaşık %40'ında gelişen; Parkinsonizm, intansiyonel tremor, serebellar ataksi ve kognitif yıkımla seyreden nörodejeneratif bir tablodur.\n- **Kuşaktan Kuşağa Geçiş:** Premutasyon taşıyıcısı bir anne, oogenez sırasında tekrar sayısını genişleterek (>200) tam mutasyonlu bir erkek çocuk dünyaya getirebilir.",
            "coreContent": {
                "table": {
                    "title": "Frajil X Premutasyon Taşıyıcılarında Görülen Tablolar",
                    "headers": ["Sendrom", "Kimlerde Görülür?", "Mekanizma", "Kardinal Klinik"],
                    "rows": [
                        ["FXPOI", "Premutasyon taşıyıcısı kadınlar (%20)", "mRNA toksisitesi -> Follikül tükenmesi", "40 yaş altı erken over yetmezliği / menopoz"],
                        ["FXTAS", "Premutasyon taşıyıcısı yaşlı erkekler (%40)", "mRNA toksisitesi -> İntranükleer inklüzyon", "Serebellar ataksi, el titremesi (tremor), kognitif gerileme"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "FXTAS", "explanation": "Frajil X premütasyon taşıyıcısı erkeklerde 50 yaş sonrası gelişen ilerleyici ataksi ve tremor sendromu."},
                {"term": "FXPOI", "explanation": "Premutasyon taşıyıcısı kadınlarda 40 yaş öncesi gelişen kalıtsal erken over yetmezliği."}
            ],
            "spotPearls": [
                "Premutasyon taşıyıcısı (55-200 CGG) kadınlarda erken menopoz (FXPOI); 50 yaş üstü erkeklerde ise ataksi ve tremor (FXTAS) riski vardır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Frajil X sendromlu bir çocuğun 34 yaşındaki annesinde 40 yaşından önce menopoza girme (erken over yetmezliği) saptanması aşağıdaki durumlardan hangisi ile ilişkilidir?",
                    {
                        "A": "FMR1 premutasyon taşıyıcılığına bağlı FXPOI sendromu",
                        "B": "Turner sendromu mozaisizmi",
                        "C": "Williams sendromu hiperkalsemisi",
                        "D": "Otoimmün poliglandüler sendrom"
                    },
                    "A",
                    {
                        "A": "Doğru! FMR1 geninde 55-200 CGG premutasyonu taşıyan kadınların %20'sinde FXPOI (erken over yetmezliği) gelişir.",
                        "B": "Yanlış. Turner sendromunda Frajil X mutasyonu görülmez.",
                        "C": "Yanlış. Williams 7q11.23 delesyonudur.",
                        "D": "Yanlış. Bu olgu ailevi FMR1 premütasyon öyküsünü yansıtır."
                    }
                )
            ]
        },
        {
            "slideNumber": 91,
            "title": "Frajil X Sendromu Kardinal Kliniği: Makroorşidizm, Uzun Yüz ve Otizm",
            "subtitle": "Puberteyle birlikte belirginleşen fiziksel ve nöropsikiyatrik bulgular",
            "badge": "Klinik Fenotip",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Frajil X sendromlu erkek hastalar puberte çağına geldiklerinde son derece tipik bir dismorfik ve davranışsal portre sergilerler:\n\n- **1. Makroorşidizm (Büyük Testisler):** Puberte sonrası hastaların %90'ından fazlasında testis hacmi normalin 2-3 katına (genellikle >25-30 mL) çıkar. Bu bulgu Frajil X için en patognomonik fizik muayene işaretidir.\n- **2. Kraniyofasiyal Özellikler:** Uzun ve dar yüz yapısı, belirgin geniş ve dışa dönük kulak kepçeleri, belirgin mandibula (prognatizm) ve yüksek damak kubbesi.\n- **3. Bağ Dokusu Laksitesi:** Parmak eklemlerinde aşırı hiperekstansibilite, pes planus (düz tabanlık) ve mitral kapak prolapsusu (MVP).\n- **4. Nöropsikiyatrik Profil:** Ağır zeka geriliği (IQ 30-50), göz temasından kaçınma, el çırpma/ısırma hareketleri ve yüksek oranda otizm spektrum bozukluğu eşliği.",
            "coreContent": {
                "table": {
                    "title": "Frajil X Sendromunun Kardinal Klinik Tetradı",
                    "headers": ["Klinik Alan", "Fizik Muayene / Semptom", "Tanısal İpucu"],
                    "rows": [
                        ["Ürogenital", "Makroorşidizm (>25 mL testis hacmi)", "Puberte sonrasında %90+ görülür (patognomonik)"],
                        ["Fasiyal", "Uzun ince yüz, belirgin prognatizm, büyük kulaklar", "Yenidoğanda siliktir, ergenlikte kristalize olur"],
                        ["İskelet/Kardiyak", "Eklem hiperlaksitesi, MVP, düz tabanlık", "Bağ dokusu elastik lif gevşekliği"],
                        ["Davranışsal", "Otizm spektrumu, el ısırma, göz temasından kaçış", "Kalıtsal otizmin en sık tek gen nedenidir"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Makroorşidizm", "explanation": "Testis hacminin orşidometre ile ölçüldüğünde yaşa göre normalin çok üzerinde (>25 mL) olması."},
                {"term": "FMRP Eksikliği", "explanation": "Nöronal sinapslarda protein sentezini denetleyen FMRP proteininin üretilememesi sonucu sinaptik plastisitenin çökmesi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Uzun yüz, büyük kulaklar, eklem hiperlaksitesi ve pubertede Makroorşidizm görülen zeka gerilikli bir erkek çocukta İLK DÜŞÜNÜLECEK tanı Frajil X sendromudur."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Zihinsel yetersizlik, belirgin büyük kulaklar, uzun yüz ve pubertede iki taraflı makroorşidizm saptanan 16 yaşındaki bir erkek hastada kesin tanı için hangi test istenmelidir?",
                    {
                        "A": "FMR1 geni CGG trinükleotid tekrar analizi (Triplet PCR / Southern Blot)",
                        "B": "Standart periferik kan karyotipi",
                        "C": "Tiroid hormon profili",
                        "D": "Serum bakır ve seruloplazmin düzeyi"
                    },
                    "A",
                    {
                        "A": "Doğru! Tablo Frajil X sendromunun klasik kliniğidir ve kesin tanı FMR1 genindeki CGG tekrar sayısının PCR/Southern blot ile ölçülmesiyle konur.",
                        "B": "Yanlış. Standart karyotip tekrar sayısını net veremez.",
                        "C": "Yanlış. Hipotiroidi makroorşidizm yapmaz.",
                        "D": "Yanlış. Wilson hastalığı taramasıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 92,
            "title": "Waardenburg Sendromu: Nöral Krest Göç Kusuru, İris Heterokromisi ve Sağırlık",
            "subtitle": "Melanosit öncüllerinin göç edememesi sonucu pigment ve iç kulak defektleri",
            "badge": "Klinik Sendrom",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Waardenburg Sendromu; embriyogenezde nöral krest hücrelerinin yüz taslaklarına, iç kulağa ve deriye göçünün bozulmasıyla ortaya çıkan otozomal dominant kalıtımlı bir hastalıktır:\n\n- **Moleküler Temel:** En sık görülen Waardenburg Tip 1'de 2. kromozomdaki (2q36.1) **PAX3** transkripsiyon faktörü geninde mutasyon bulunur.\n- **Kardinal Klinik Dörtlü:**\n  - **1. Distelekanzi (Dystopia canthorum):** İç kantal açıların ve lakrimal punktumların laterale doğru kayması (Tip 1'in ayırt edici bulgusudur).\n  - **2. Pigment Anomalileri (Heterokromi):** İris renklerinin birbirinden farklı olması (bir göz kahverengi, diğer göz parlak safir mavisi) veya aynı iriste iki renk segmenti.\n  - **3. Saç Anomalisi (Poliosis):** Alnın tam orta çizgisinde doğuştan beyaz saç perçemi.\n  - **4. Sensorinöral İşitme Kaybı:** Kokleanın stria vaskülaris tabakasındaki melanositlerin yokluğuna bağlı konjenital sağırlık.",
            "coreContent": {
                "table": {
                    "title": "Waardenburg Sendromu Kardinal Bulguları",
                    "headers": ["Bulgu Adı", "Klinik Görünüm", "Embriyolojik / Moleküler Neden"],
                    "rows": [
                        ["Distelekanzi", "İç göz pınarlarının yana kayması (W indeksi >1.95)", "Frontonazal nöral krest göç kusuru"],
                        ["İris Heterokromisi", "İki gözün farklı renkte olması (mavi/kahve)", "İris stromasında melanosit dağılım asimetrisi"],
                        ["Poliosis", "Alın orta hattında beyaz saç perçemi", "Saç follikülünde melanosit yokluğu"],
                        ["Sensorinöral Sağırlık", "Tek veya iki taraflı iç kulak işitme kaybı", "Kokleada stria vaskülaris melanosit yokluğu"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "PAX3 Geni", "explanation": "Waardenburg Sendromu Tip 1'e neden olan, nöral krest hücre göçünü yöneten transkripsiyon faktörü."},
                {"term": "Poliosis (Beyaz Saç Perçemi)", "explanation": "Alın orta hattında melanosit göç eksikliğine bağlı doğuştan beyaz saç tutamı bulunması."}
            ],
            "spotPearls": [
                "Waardenburg sendromunda sağırlığın ve pigment defektlerinin ortak nedeni NÖRAL KREST hücrelerinin göç kusurudur."
            ],
            "interactiveElements": [
                make_cloze(
                    "Waardenburg sendromunda iç kantal açıların ve alt lakrimal punktumların dışa doğru kayması bulgusuna [Distelekanzi] (Dystopia canthorum) adı verilir.",
                    "Distelekanzi",
                    "Dystopia canthorum",
                    "Distelekanzi Waardenburg Tip 1 için patognomonik bir kantal deplasman bulgusudur; W-indeksi ile hesaplanır."
                )
            ]
        },
        {
            "slideNumber": 93,
            "title": "Waardenburg Tipleri Ayırıcı Tanısı: Tip 1 vs Tip 2 Ayrımında Distelekanzi Kriteri",
            "subtitle": "PAX3 ile MITF gen mutasyonları ve kantal açılanma farkı",
            "badge": "Ayırıcı Tanı",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Waardenburg sendromunun 4 klinik tipi tanımlanmıştır; ancak sınavlarda ve klinikte en kritik ayrım Tip 1 ile Tip 2 arasındadır:\n\n- **Waardenburg Tip 1 (PAX3 Geni):** Olgularda **DİSTELEKANZİ KESİNLİKLE VARDIR** (hastaların %99'unda mevcuttur). Sensorinöral işitme kaybı oranı yaklaşık %60'tır.\n- **Waardenburg Tip 2 (MITF Geni):** Olgularda **DİSTELEKANZİ KESİNLİKLE YOKTUR!** İç göz açıları tamamen normaldir. Buna karşılık sensorinöral işitme kaybı sıklığı (%85-90) Tip 1'den belirgin şekilde daha yüksektir.\n- **Tip 3 (Klein-Waardenburg):** Tip 1 bulgularına ek olarak üst ekstremite ve omuz kas-iskelet defektleri eşlik eder.\n- **Tip 4 (Shah-Waardenburg):** Bulgulara ek olarak Hirschsprung hastalığı (aganglionik megakolon) eşlik eder (SOX10 / EDNRB genleri).",
            "coreContent": {
                "table": {
                    "title": "Waardenburg Tip 1 ve Tip 2 Karşılaştırma Matrisi",
                    "headers": ["Klinik Özellik", "Waardenburg Tip 1", "Waardenburg Tip 2"],
                    "rows": [
                        ["Sorumlu Gen", "PAX3 (2q36.1)", "MITF (3p14.1)"],
                        ["Distelekanzi (Dystopia canthorum)", "VARDIR (%99 olguda)", "YOKTUR (%0 - Kantus normaldir!)"],
                        ["Sensorinöral Sağırlık Sıklığı", "%60 olguda", "%85 - 90 olguda (Daha yüksek!)"],
                        ["Heterokromi & Beyaz Perçem", "Her ikisinde de görülür", "Her ikisinde de görülür"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "MITF Geni", "explanation": "Mikroftalmi ilişkili transkripsiyon faktörü; Waardenburg Tip 2'den sorumlu melanosit regülatörü."},
                {"term": "W-İndeksi", "explanation": "İç kantal mesafe, dış kantal mesafe ve interpupiller mesafeyle distelekanziyi kanıtlayan formül."}
            ],
            "spotPearls": [
                "❓ [ÇIKMIŞ SORU ODAĞI] Waardenburg Tip 1 ile Tip 2 arasındaki en kritik ayrım DİSTELEKANZİDİR; Tip 1'de distelekanzi (PAX3) varken Tip 2'de (MITF) distelekanzi yoktur."
            ],
            "interactiveElements": [
                make_before_after(
                    "Waardenburg Tip 1 vs Tip 2 Büyük Ayrımı",
                    "Waardenburg Tip 1",
                    "Waardenburg Tip 2",
                    [
                        "Sorumlu gen: PAX3 transkripsiyon faktörü",
                        "Distelekanzi (dystopia canthorum) KESİNLİKLE VARDIR",
                        "İç kantal açılar yana kaymıştır (W indeksi > 1.95)",
                        "Sensorinöral sağırlık sıklığı yaklaşık %60'tır"
                    ],
                    [
                        "Sorumlu gen: MITF transkripsiyon faktörü",
                        "Distelekanzi KESİNLİKLE YOKTUR (İç göz pınarları normaldir)",
                        "W indeksi normal sınırlardadır (< 1.95)",
                        "Sensorinöral sağırlık sıklığı çok daha yüksektir (%85-90)"
                    ]
                ),
                make_micro_quiz(
                    "Doğuştan beyaz saç perçemi, bir gözü kahverengi bir gözü mavi olan (heterokromi) ve sensorinöral işitme kaybı bulunan bir çocukta yapılan kantal ölçümlerde distelekanzi (dystopia canthorum) saptanmamıştır. Bu çocukta en olası tanı ve sorumlu gen hangisidir?",
                    {
                        "A": "Waardenburg Sendromu Tip 2 - MITF geni",
                        "B": "Waardenburg Sendromu Tip 1 - PAX3 geni",
                        "C": "Treacher Collins Sendromu - TCOF1 geni",
                        "D": "Pierre Robin Sekansı - SOX9 geni"
                    },
                    "A",
                    {
                        "A": "Doğru! Distelekanzi OLMAYAN Waardenburg olguları Tip 2'dir ve sorumlu gen MITF'tir.",
                        "B": "Yanlış. Tip 1'de distelekanzi mutlaka bulunur.",
                        "C": "Yanlış. Treacher Collins'te heterokromi veya beyaz perçem olmaz, zigoma hipoplazisi olur.",
                        "D": "Yanlış. Pierre Robin mikrognati ve yarık damak sekansıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 94,
            "title": "Akondroplazi Moleküler Temeli: FGFR3 Geni Fonksiyon Kazanımı ve İleri Baba Yaşı",
            "subtitle": "Kondrosit proliferasyonunun baskılanması ve spermatogenezde de novo mutasyon",
            "badge": "İskelet Displazisi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Akondroplazi; insanlarda orantısız boy kısalığı (cücelik) yapan en yaygın iskelet displazisidir (1/15.000-40.000 canlı doğum):\n\n- **Moleküler Mekanizma:** Vakaların %99'unda **FGFR3** (Fibroblast Growth Factor Receptor 3) geninde glisin aminoasidinin arjinine dönüşmesi (**Gly380Arg**) mutasyonudur. Bu bir **kazanılmış fonksiyon (gain-of-function)** mutasyonudur; reseptör sinyali sürekli açık kalarak enkondral kemikleşmeyi ve kondrosit proliferasyonunu anormal derecede baskılar.\n- **De Novo Mutasyon ve Baba Yaşı:** Hastaların **%80'inin anne ve babası tamamen normal boydadır**; mutasyon **ileri baba yaşına (>35-40)** bağlı olarak spermatogenez sırasındaki replikasyon hatalarıyla taze (de novo) gelişir.\n- **Kalıtım:** Otozomal dominanttır; homozigot FGFR3 mutasyonu ise yaşamla bağdaşmaz (yenidoğanda letaldir).",
            "coreContent": {
                "table": {
                    "title": "Akondroplazinin Genetik ve Moleküler Parametreleri",
                    "headers": ["Parametre", "Biyolojik Gerçeklik", "Klinik / Sınav Anlamı"],
                    "rows": [
                        ["Sorumlu Gen", "FGFR3 (4p16.3 lokusu)", "Tirozin kinaz reseptörü"],
                        ["En Sık Mutasyon", "c.1138G>A (Gly380Arg) (%98+)", "İnsan genomunun en mutajenik tek bazıdır"],
                        ["Mutasyon Tipi", "Kazanılmış Fonksiyon (Gain-of-Function)", "Reseptör ligansız sürekli aktif kalır"],
                        ["De Novo Oranı", "%80 olgu taze mutasyondur", "İleri baba yaşı ile doğrudan ilişkilidir"],
                        ["Homozigot Durum", "FGFR3 / FGFR3", "Yaşamla bağdaşmaz; doğumda letaldir"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "FGFR3 Geni", "explanation": "Fibroblast büyüme faktörü reseptörü 3; Akondroplazi ve Tanatoforik displaziye neden olan tirozin kinaz reseptörü."},
                {"term": "Kazanılmış Fonksiyon (Gain-of-function)", "explanation": "Mutasyonun protein aktivitesini kapatmak yerine sürekli aktif ve hiperfonksiyonel hale getirmesi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Akondroplazi FGFR3 geninde kazanılmış fonksiyon (gain-of-function) mutasyonudur; %80 de novo gelişir ve ileri baba yaşı ile ilişkilidir."
            ],
            "interactiveElements": [
                make_cloze(
                    "Akondroplazide FGFR3 reseptörünün ligand bağlanmaksızın sürekli aktif kalarak kondrosit çoğalmasını frenlemesi [kazanılmış fonksiyon] (gain-of-function) mutasyonu mekanizmasıdır.",
                    "kazanılmış fonksiyon",
                    "Gain-of-function mutasyon türü",
                    "Reseptörün sürekli aktif kalması kemik büyüme plaklarındaki kondrositleri baskılar."
                ),
                make_micro_quiz(
                    "Normal boydaki bir anne ve babadan akondroplazili bir çocuk doğması durumunda en olası etiyolojik risk faktörü aşağıdakilerden hangisidir?",
                    {
                        "A": "İleri baba yaşı (spermatogenezde taze de novo mutasyon)",
                        "B": "İleri anne yaşı (mayotik ayrılamama)",
                        "C": "Gebelikte folik asit eksikliği",
                        "D": "Akraba evliliği (otozomal resesif kalıtım)"
                    },
                    "A",
                    {
                        "A": "Doğru! Akondroplazi %80 de novo gelişir ve ileri baba yaşı ile doğrudan ilişkilidir (taze monogenik nokta mutasyonları spermatogenezde artar).",
                        "B": "Yanlış. İleri anne yaşı trizomilere yol açar.",
                        "C": "Yanlış. Folik asit nöral tüp defektini önler.",
                        "D": "Yanlış. Akondroplazi otozomal dominanttır."
                    }
                )
            ]
        },
        {
            "slideNumber": 95,
            "title": "Akondroplazi Kliniği: Rizomeli, Foramen Magnum Stenozu ve Trident El",
            "subtitle": "Orantısız boy kısalığı, nöroşirürjikal bası riski ve kraniyofasiyal anatomi",
            "badge": "Klinik Belirteçler",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Akondroplazili bir hastanın fizik muayenesinde göze çarpan kardinal bulgular:\n\n- **1. Rizomelik Ekstremite Kısalığı:** Kollar ve uyluklar (proksimal segmentler) gövdeye oranla çok kısadır; gövde uzunluğu ve omurga boyutu tamamen normaldir (orantısız cücelik).\n- **2. Kraniyofasiyal Bulgular:** Belirgin makrosefali, frontal bombelik (çıkık alın), basık burun kökü (midfasiyal hipoplazi).\n- **3. Trident (Üç Dişli Mızrak) El:** 3. ve 4. parmaklar birbirine yaklaşamaz, parmaklar kısa ve kalındır (brakidaktili); el üç dişli mızrak gibi ayrık durur.\n- **4. Nöroşirürjikal Acil Durum (Foramen Magnum Darlığı):** Kafatası tabanındaki foramen magnum kıkırdak kökenli olduğu için dar kalır; kranioservikal bileşkeye ve medulla spinalise bası yaparak bebekte **ani uyku apnesi ve ani bebek ölümüne** yol açabilir. Tüm akondroplazili bebekler foramen magnum açısından MR ile taranmalıdır.",
            "coreContent": {
                "table": {
                    "title": "Akondroplazi Fizik Muayene Bulguları ve Yönetimi",
                    "headers": ["Vücut Bölgesi", "Fizik Muayene Özelliği", "Klinik / Cerrahi Önemi"],
                    "rows": [
                        ["Ekstremiteler", "Rizomeli (uyluk ve kol kısalığı), Trident el", "Proksimal tutulum tipiktir"],
                        ["Baş ve Yüz", "Makrosefali, frontal belirginlik, basık burun", "Enkondral kemikleşme yetersizliği"],
                        ["Kraniyoservikal Bileşke", "Foramen Magnum Stenozu", "HAYATİ TEHLİKE: Santral apne ve ani ölüm riski (Cerrahi dekompresyon)"],
                        ["Omurga", "Lomber lordoz, torakolomber kifoz", "Erişkin dönemde spinal kanal darlığı"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Rizomeli", "explanation": "Ekstremitelerin proksimal segmentlerinin (kol ve uyluk) distal segmentlere oranla kısa olması."},
                {"term": "Trident El", "explanation": "Akondroplazide 3. ve 4. parmakların birbirinden ayrılarak elin üç dişli mızrak görünümü alması."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Akondroplazili bebeklerde foramen magnum darlığı medulla spinalise bası yaparak ani uyku apnesi ve ani ölüme yol açabilir; kraniyoservikal MR şarttır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Akondroplazi tanısı alan 3 aylık bir bebeğin takibinde ani solunum durması (apne) ve mortalite riskini önlemek için öncelikle taranması gereken anatomik bölge neresidir?",
                    {
                        "A": "Kraniyoservikal bileşke ve Foramen Magnum darlığı",
                        "B": "Aort kökü ve çıkan aort",
                        "C": "Göz içi lens stabilitesi",
                        "D": "Distal femur metafizi"
                    },
                    "A",
                    {
                        "A": "Doğru! Akondroplazide kafatası tabanı darlığı (foramen magnum stenozu) beyin sapı basısı ile ani uyku apnesi ve ölüm riski oluşturur; cerrahi dekompresyon gerekebilir.",
                        "B": "Yanlış. Aort kökü dilatasyonu Marfan sendromu takibidir.",
                        "C": "Yanlış. Lens subluksasyonu Marfan/Homosistinüri takibidir.",
                        "D": "Yanlış. Femur kısalığı tanısaldır ama ani ölüm riski taşımaz."
                    }
                )
            ]
        },
        {
            "slideNumber": 96,
            "title": "Williams Sendromu: 7q11.23 Mikrodelesyonu, Elastin Gen Kaybı ve Elfin Yüzü",
            "subtitle": "Kokteyl partisi kişiliği, supravalvüler aort darlığı ve infantil hiperkalsemi",
            "badge": "Mikrodelesyon",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Williams-Beuren Sendromu; 7. kromozomun uzun kolunda yaklaşık 1.5-1.8 Mb'lık bir mikrodelesyon (**7q11.23**) sonucu ortaya çıkan sendromdur:\n\n- **Moleküler Temel:** Delesyon bölgesinde yer alan yaklaşık 26-28 genden en kritiği **ELN (Elastin)** genidir. Elastin proteini arter duvarlarının esnekliğini sağlar; kaybı arteriyopatilere yol açar.\n- **Kardiyovasküler Bulgular:** Olguların %75'inde **Supravalvüler Aort Darlığı (SVAS)** ve periferik pulmoner arter stenozu gelişir.\n- **Fasiyal Morfoloji (Elfin Yüzü):** Periorbital dolgunluk, basık burun kökü, kalkık burun ucu, uzun filtrum, dolgun dudaklar, açık ağız ve mavi gözlülerde karakteristik **yıldızsı (stellat) iris** deseni.\n- **Bilişsel ve Davranışsal Profil:** Hafif-orta zeka geriliği (IQ 50-60); aşırı sosyal, yabancılardan korkmayan, empati düzeyi yüksek 'Kokteyl Partisi Kişiliği'.\n- **Metabolik:** İntrauterin dönemde ve bebeklikte geçici **infantil hiperkalsemi** atakları görülür.",
            "coreContent": {
                "table": {
                    "title": "Williams Sendromunun Kardinal Klinik ve Genetik Bulguları",
                    "headers": ["Sistem / Alan", "Bulgu", "Sorumlu Gen / Mekanizma"],
                    "rows": [
                        ["Kromozomal Lokus", "7q11.23 mikrodelesyonu (~1.5 Mb)", "FISH veya CMA ile saptanır"],
                        ["Kardiyovasküler", "Supravalvüler Aort Stenozu (SVAS)", "ELN (Elastin) geni hemizigotluğu"],
                        ["Yüz Görünümü", "Elfin yüzü, yıldızsı iris, periorbital ödem", "Karakteristik dismorfik örüntü"],
                        ["Davranış", "Aşırı cana yakın, konuşkan (Kokteyl partisi)", "Spesifik nörobilişsel profil"],
                        ["Metabolizma", "İnfantil Hiperkalsemi", "D vitamini metabolizma anormalliği"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "7q11.23 Mikrodelesyonu", "explanation": "Williams sendromuna yol açan, elastin (ELN) genini içeren submikroskobik kromozom kaybı."},
                {"term": "Supravalvüler Aort Stenozu (SVAS)", "explanation": "Aort kapağının hemen üzerinde arter duvarında gelişen konjenital daralma."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Williams sendromu 7q11.23 (ELN geni) mikrodelesyonudur; Elfin yüzü, yıldızsı iris, Supravalvüler Aort Stenozu (SVAS) ve aşırı sosyal kokteyl kişiliği ile seyreder."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Elfin benzeri yüz görünümü, irisinde yıldızsı desen, aşırı konuşkan ve sosyal davranış örüntüsü olan 4 yaşındaki bir çocukta supravalvüler aort stenozu (SVAS) saptanıyor. Bu hastada kesin tanı için hangi mikrodelesyon araştırılmalıdır?",
                    {
                        "A": "7q11.23 mikrodelesyonu (Williams sendromu)",
                        "B": "22q11.2 mikrodelesyonu (DiGeorge sendromu)",
                        "C": "5p delesyonu (Cri du Chat sendromu)",
                        "D": "4p delesyonu (Wolf-Hirschhorn sendromu)"
                    },
                    "A",
                    {
                        "A": "Doğru! Elfin yüzü, yıldızsı iris, SVAS ve aşırı sosyal kişilik Williams sendromunun (7q11.23 mikrodelesyonu) klasik kliniğidir.",
                        "B": "Yanlış. 22q11.2 DiGeorge'dur (trunkus arteriyozus, hipokalsemi).",
                        "C": "Yanlış. 5p kedi miyavlaması sesidir.",
                        "D": "Yanlış. 4p miğfer yüzüdür."
                    }
                )
            ]
        },
        {
            "slideNumber": 97,
            "title": "Majör Trizomilerin Ayırıcı Tanısı: Down (T21), Edwards (T18) ve Patau (T13)",
            "subtitle": "Kromozom anomalilerinin kardinal dismorfolojik ipuçları ve yaşam beklentisi",
            "badge": "Trizomi Karşılaştırma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Canlı doğabilen üç majör otozomal trizomi birbirine karışmayacak kadar net fiziksel belirteçlere sahiptir:\n\n- **Trizomi 21 (Down Sendromu):** En sık görülen canlı trizomidir (1/800). Brakisefali, basık burun kökü, yukarı çekik gözler (mongoloid çekiklik), epikantus, fırça benzeri Brushfield lekeleri, avuç içinde tek transvers palmar çizgi (Simian çizgisi), ayak 1-2. parmak arası geniş açıklık (sandalet boşluğu) ve AV septal defekt (AVSD).\n- **Trizomi 18 (Edwards Sendromu):** Belirgin çıkık oksiput, mikrognati, düşük kulaklar, üst üste binen parmaklar (**Clenched hand:** 2. ve 5. parmakların 3. ve 4. parmak üzerine binmesi), beşik taban ayak (**Rocker-bottom feet**). Vakaların %90'ı ilk 1 yılda kaybedilir.\n- **Trizomi 13 (Patau Sendromu):** En ağır tablodur. Ön beyin bölünme kusuru (**Holoprosensefali**), mikroftalmi/anoftalmi, orta hat yarık dudak/damak, el ve ayaklarda **Postaksiyel Polidaktili** ve skalpte doku yokluğu (**Aplasia cutis congenita**). Yaşam süresi birkaç gündür.",
            "coreContent": {
                "table": {
                    "title": "Down, Edwards ve Patau Sendromlarının Ayırıcı Tanı Matrisi",
                    "headers": ["Klinik Özellik", "Down (Trizomi 21)", "Edwards (Trizomi 18)", "Patau (Trizomi 13)"],
                    "rows": [
                        ["İnsidans", "1 / 800 canlı doğum", "1 / 6.000 canlı doğum", "1 / 10.000 canlı doğum"],
                        ["Kardinal Kafa/Yüz", "Brakisefali, epikantus, basık burun", "Çıkık oksiput, mikrognati", "Holoprosensefali, yarık dudak/damak"],
                        ["Tipik El Bulgusu", "Tek palmar çizgi (Simian)", "Üst üste binen parmaklar (Clenched hand)", "Postaksiyel Polidaktili"],
                        ["Tipik Ayak Bulgusu", "Sandalet açıklığı (1-2. parmak)", "Beşik taban ayak (Rocker-bottom)", "Beşik taban ayak"],
                        ["Tipik Ek Organ Bulgusu", "AVSD, Duodenal atrezi", "VSD, Horseshoe (At nalı) böbrek", "Skalpte aplazia kutis, Kistik böbrek"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Clenched Hand", "explanation": "Edwards sendromunda 2. parmağın 3. parmağın, 5. parmağın da 4. parmağın üzerine bindiği karakteristik yumruk postürü."},
                {"term": "Holoprosensefali", "explanation": "Patau sendromunda prosensefalonun iki serebral hemisfere bölünememesi sonucu oluşan ağır beyin malformasyonu."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Üst üste binen parmaklar (Clenched hand) ve çıkık oksiput EDWARDS (T18); holoprosensefali, yarık dudak/damak ve polidaktili PATAU (T13) sendromudur."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Yenidoğan yoğun bakımında izlenen bir bebekte holoprosensefali, mikrosefali, mikroftalmi, bilateral yarık dudak/damak, skalpte cilt defekti (aplasia cutis) ve ellerde postaksiyel polidaktili saptanıyor. En olası sitogenetik tanı hangisidir?",
                    {
                        "A": "Trizomi 13 (Patau Sendromu)",
                        "B": "Trizomi 18 (Edwards Sendromu)",
                        "C": "Trizomi 21 (Down Sendromu)",
                        "D": "45,X (Turner Sendromu)"
                    },
                    "A",
                    {
                        "A": "Doğru! Holoprosensefali, orta hat yüz yarıkları, aplazia kutis ve polidaktili triadı Patau sendromu (Trizomi 13) için patognomoniktir.",
                        "B": "Yanlış. Edwards'ta clenched hand ve çıkık oksiput olur.",
                        "C": "Yanlış. Down sendromunda holoprosensefali veya aplazia kutis görülmez.",
                        "D": "Yanlış. Turner monozomidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 98,
            "title": "Cinsiyet Kromozomu Aneuploidileri: Turner (45,X) vs Klinefelter (47,XXY)",
            "subtitle": "Canlı tek monozomi ile en sık erkek hipogonadizm nedeninin karşılaştırması",
            "badge": "Gonosom Anomalileri",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Cinsiyet kromozomlarındaki sayısal anomaliler otozomal trizomilere göre zeka üzerinde çok daha az yıkıcı etkiye sahiptir:\n\n- **Turner Sendromu (45,X):**\n  - **Canlı doğabilen TEK tam monozomidir** (vakaların %99'u abortusla sonuçlanır).\n  - **Kardinal Bulgular:** Kısa boy (<3 persantil; SHOX gen kaybı), yele boyun (pterigiyum kolli), düşük arka saç çizgisi, geniş göğüs (kalkan göğüs), meme uçlarında ayrıklık, periferik lenfödem.\n  - **Kardiyovasküler:** Biküspit aort kapağı ve **Aort Koarktasyonu**.\n  - **Gonadal:** Fibröz çizgilenme gonadlar (**Streak gonad**), primer amenore ve infertilite. Zeka genellikle tamamen normaldir.\n- **Klinefelter Sendromu (47,XXY):**\n  - Erkeklerde hipogonadizmin ve erkek infertilitesinin en sık genetik nedenidir (1/600).\n  - **Kardinal Bulgular:** Uzun boy, orantısız uzun bacaklar (öknoid yapı), küçük ve sert testisler, testosteron düşüklüğü, **Jinekomasti** (erkek meme kanseri riski 20-50 kat artar) ve azoospermi.",
            "coreContent": {
                "table": {
                    "title": "Turner (45,X) ve Klinefelter (47,XXY) Karşılaştırma Matrisi",
                    "headers": ["Parametre", "Turner Sendromu", "Klinefelter Sendromu"],
                    "rows": [
                        ["Karyotip", "45,X (Canlı tek monozomi)", "47,XXY (Ek X kromozomu)"],
                        ["Cinsiyet Fenotipi", "Dişi", "Erkek"],
                        ["Boy Özelliği", "Kısa boy (<145 cm; SHOX eksikliği)", "Uzun boy (orantısız uzun bacaklar)"],
                        ["Gonad Durumu", "Streak (çizgi) overler, primer amenore", "Küçük sert testisler, azoospermi"],
                        ["Karakteristik Risk", "Aort Koarktasyonu, Yele boyun", "Jinekomasti, Erkek Meme Kanseri riski"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Streak Gonad (Çizgi Over)", "explanation": "Turner sendromunda over folliküllerinin erken atreziye uğrayarak fibröz bağ dokusu bantlarına dönüşmesi."},
                {"term": "Yele Boyun (Pterigium Colli)", "explanation": "İntrauterin kistik higromanın gerilemesi sonucu boyun lateralinde kalan deri katlantısı."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Turner sendromunda kardiyak lezyon Aort Koarktasyonu; Klinefelter'da ise 50 kat artan malignite riski Erkek Meme Kanseridir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Turner vs Klinefelter Temel Ayırımı",
                    "Turner Sendromu (45,X)",
                    "Klinefelter Sendromu (47,XXY)",
                    [
                        "Canlı doğabilen TEK tam monozomi tablosudur",
                        "Fenotipik olarak DİŞİDİR; boy belirgin KISADIR",
                        "Yele boyun ve kalkan göğüs eşlik eder",
                        "En sık kardiyak patoloji Aort Koarktasyonudur"
                    ],
                    [
                        "Ekstra X kromozomu taşıyan ERKEK tablosudur",
                        "Boy belirgin şekilde UZUNDUR (öknoid ekstremiteler)",
                        "Küçük sert testisler ve Jinekomasti (meme büyümesi) tipiktir",
                        "Erkek meme kanseri riski 20-50 kat artmıştır"
                    ]
                )
            ]
        },
        {
            "slideNumber": 99,
            "title": "Prader-Willi ve Angelman Ayırıcı Tanı Laboratuvar Testleri: Metilasyon Spesifik PCR",
            "subtitle": "15q11-q13 imprinting bozukluklarında delesyon, UPD ve imprinting merkezi analizi",
            "badge": "Laboratuvar Tanısı",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "15q11-q13 bölgesinde Prader-Willi veya Angelman sendromu kliniği olan bir hastada tanı rastgele testlerle konmaz; basamaklı moleküler algoritma izlenir:\n\n- **1. Basamak (Metilasyon Spesifik PCR - MS-PCR):** Olguların %99'unda anormal metilasyon paternini yakalayarak tanıyı doğrular (Prader-Willi'de yalnızca maternal metillenmiş bant; Angelman'da yalnızca paternal metillenmemiş bant çıkar).\n- **2. Basamak (Mekanizmayı Aydınlatma):**\n  - **FISH veya CMA:** Olguların %70'indeki mikrodelesyonu saptar.\n  - **Mikrosatellit Belirteçleri (STR Analizi):** Delesyon yoksa Uniparental Dizomi (Maternal UPD veya Paternal UPD) ayrımını yapar.\n  - **Dizi Analizi:** Angelman şüphesinde delesyon ve UPD yoksa anneden gelen **UBE3A** gen mutasyonu aranır (%10).\n- **Tekrarlama Riski:** Delesyonda <%1 iken, imprinting merkez defektlerinde %50'ye kadar çıkabilir.",
            "coreContent": {
                "table": {
                    "title": "Prader-Willi ve Angelman Tanı Algoritması",
                    "headers": ["Test Basamağı", "Saptanan Anomali", "Klinik Yorum"],
                    "rows": [
                        ["Metilasyon Spesifik PCR", "Anormal metilasyon varlığı", "Tanıyı %99 doğrular ama mekanizmayı söylemez"],
                        ["FISH / CMA", "15q11-q13 mikrodelesyonu", "Olguların %70'ini açıklar (tekrarlama riski <%1)"],
                        ["STR Mikrosatellit Belirteçleri", "Uniparental Dizomi (UPD)", "Maternal UPD (PWS) veya Paternal UPD (AS) kanıtlar"],
                        ["UBE3A Dizi Analizi", "Nokta mutasyonu", "İzole Angelman sendromlu olguların %10'unda tanı koyar"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Metilasyon Spesifik PCR (MS-PCR)", "explanation": "DNA'daki metillenmiş ve metillenmemiş sitozinleri ayırt ederek imprinting hastalıklarını tarayan altın standart test."},
                {"term": "UBE3A Geni", "explanation": "Yalnızca beyin nöronlarında maternal alelden eksprese olan, Angelman sendromundan sorumlu ubikitin ligaz geni."}
            ],
            "spotPearls": [
                "Prader-Willi ve Angelman şüphesinde İLK İSTENECEK test Metilasyon Spesifik PCR'dır (MS-PCR); vakaların %99'unu tarar."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Yenidoğan döneminde ağır hipotoni ve zayıf emme nedeniyle Prader-Willi sendromundan şüphelenilen bir bebekte tanıyı doğrulamak için İLK BASAMAKTA hangi moleküler test istenmelidir?",
                    {
                        "A": "Metilasyon Spesifik PCR (MS-PCR)",
                        "B": "Standart Karyotip analizi",
                        "C": "WES (Tüm Ekzom Dizileme)",
                        "D": "Serum karnitin düzeyi"
                    },
                    "A",
                    {
                        "A": "Doğru! Prader-Willi ve Angelman sendromlarının taranmasında 1. basamak test, delesyon, UPD ve imprinting merkez hatalarının %99'unu yakalayan Metilasyon Spesifik PCR'dır.",
                        "B": "Yanlış. Karyotip 15q11 mikrodelesyonunu göremez.",
                        "C": "Yanlış. WES metilasyon durumunu gösteremez.",
                        "D": "Yanlış. Metabolik testtir."
                    }
                )
            ]
        },
        {
            "slideNumber": 100,
            "title": "Konjenital Anomalilerde Prevalans ve Etiyoloji Dağılımı: %50-60 Bilinmeyen Neden",
            "subtitle": "Tüm yenidoğanların %2-4'ünde görülen defektlerin epidemiyolojik gerçekliği",
            "badge": "Epidemiyoloji",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Tıbbi genetik ve dismorfolojinin en önemli halk sağlığı gerçeklerinden biri konjenital anomalilerin toplumdaki dağılımıdır:\n\n- **Doğumdaki Sıklık:** Canlı doğan bebeklerin **%2-4'ünde (yaklaşık %3)** doğumsal bir anomali mevcuttur.\n- **Birlikte Görülme Dağılımı:**\n  - **%60 - 65:** İzole majör anomaliler (yarık damak, VSD, pilor stenozu vb.).\n  - **%20:** Sendromlar (Down, Williams, Marfan vb.).\n  - **%8 - 13:** Sekanslar (Potter sekansı, Pierre Robin sekansı).\n  - **%3:** Asosiasyonlar (VACTERL, MURCS).\n- **Etiyolojik Dağılım:**\n  - **%50 - 60:** **BİLİNMEYEN NEDENLER** (günümüz teknolojisiyle dahi aydınlatılamayan grup).\n  - **%20 - 25:** Multifaktöriyel (genetik zemin + çevresel faktörler).\n  - **%7 - 10:** Çevresel faktörler ve teratojenler (alkol, diyabet, enfeksiyonlar).\n  - **%7 - 8:** Mutant tek gen hastalıkları.\n  - **%6 - 7:** Kromozomal sayısal ve yapısal anomaliler.",
            "coreContent": {
                "table": {
                    "title": "Konjenital Anomalilerin Etiyolojik Dağılım Tablosu",
                    "headers": ["Etiyolojik Kategori", "Görülme Oranı (%)", "Tipik Örnek"],
                    "rows": [
                        ["Bilinmeyen Nedenler", "%50 - 60 (EN BÜYÜK GRUP)", "Etiyolojisi çözülemeyen sporadik defektler"],
                        ["Multifaktöriyel Kalıtım", "%20 - 25", "Nöral tüp defektleri, yarık dudak/damak"],
                        ["Çevresel ve Teratojenler", "%7 - 10", "FAS (alkol), talidomid, maternal diyabet"],
                        ["Mutant Tek Genler", "%7 - 8", "Akondroplazi, Marfan sendromu"],
                        ["Kromozom Anomalileri", "%6 - 7", "Trizomi 21 (Down), Turner (45,X)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Konjenital Anomali Prevalansı", "explanation": "Yenidoğan popülasyonunda doğumsal yapısal bozuklukların görülme sıklığı (%2-4)."},
                {"term": "İdiyopatik Malformasyon", "explanation": "Bilinen tüm genetik ve çevresel testlere rağmen nedeni aydınlatılamayan (%50-60) anomali grubu."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Konjenital anomalilerin etiyolojisinde EN BÜYÜK PAY (%50-60) nedeni bilinmeyen (idiyopatik) gruba aittir; kromozomal nedenler yalnızca %6-7'dir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Canlı doğan bebeklerde saptanan konjenital anomalilerin etiyolojik nedenleri incelendiğinde en büyük yüzdeyi (%50-60) aşağıdakilerden hangisi oluşturur?",
                    {
                        "A": "Etiyolojisi bilinmeyen (idiyopatik) nedenler",
                        "B": "Sayısal kromozom anomalileri",
                        "C": "Teratojenik ilaç maruziyeti",
                        "D": "Tek gen mutasyonları"
                    },
                    "A",
                    {
                        "A": "Doğru! Tüm gelişmiş tanı teknolojilerine rağmen konjenital anomalilerin %50-60'ında spesifik bir neden saptanamaz (bilinmeyen etiyoloji).",
                        "B": "Yanlış. Kromozom anomalileri sadece %6-7'sini oluşturur.",
                        "C": "Yanlış. Teratojenler %7-10 oranındadır.",
                        "D": "Yanlış. Tek gen mutasyonları %7-8 oranındadır."
                    }
                )
            ]
        },
        {
            "slideNumber": 101,
            "title": "Genetik Danışmanın 4 Temel İlkesi: Yönlendirici Olmayan (Non-directive) Yaklaşım",
            "subtitle": "Tanı, risk hesabı, otonomiye saygı ve uzun dönem psikososyal destek",
            "badge": "Klinik Etik",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Genetik danışma; bir ailede genetik hastalık riski veya tanısı varlığında, ailenin tıbbi gerçekleri anlamasını, riskleri kavramasını ve kendi özgür kararlarını vermesini sağlayan profesyonel bir iletişim sürecidir:\n\n- **1. Doğru Tanı (Tanı Kesinleştirmesi):** Danışmanın ilk adımı hastanın klinik, sitogenetik veya moleküler tanısını doğrulamaktır; tanı olmadan risk hesaplanamaz.\n- **2. Tekrarlama Riskinin Hesaplanması:** Hastalığın kalıtım modeline göre (otozomal resesifte her gebelikte %25; dominantta %50; trizomide maternal yaş riski) kesin matematiksel risk açıklanır.\n- **3. YÖNLENDİRİCİ OLMAYAN (NON-DIRECTIVE) YAKLAŞIM:** Genetik hekimi ailenin yerine ASLA karar vermez. 'Bu gebeliği sonlandırmalısınız' veya 'Mutlaka çocuk yapmalısınız' gibi yönlendirici cümleler kurulamaz. Seçenekler tarafsızca sunulur; karar ailenin otonomisine aittir.\n- **4. Psikososyal Destek ve Uzun Dönem İzlem:** Ailenin suçluluk duygularının giderilmesi, akraba taramaları ve hasta destek derneklerine yönlendirilmesi sağlanır.",
            "coreContent": {
                "table": {
                    "title": "Genetik Danışmanın 4 Basamağı ve Hekimin Rolü",
                    "headers": ["Basamak", "Eylem", "Etik İlke / Kural"],
                    "rows": [
                        ["1. Tanı", "Klinik ve moleküler doğrulamayı tamamlamak", "Tıbbi doğruluk şarttır"],
                        ["2. Risk Tayini", "Mendelyen veya ampirik tekrarlama riskini hesaplamak", "Açık, anlaşılır matematiksel oranlar"],
                        ["3. Seçenekler", "Prenatal tanı, PGT, evlat edinme seçeneklerini sunmak", "YÖNLENDİRİCİ OLMAMAK (Non-directive)"],
                        ["4. Destek", "Psikolojik destek ve takip planlamak", "Ailenin otonomisine ve sırrına saygı"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Non-Direktif (Yönlendirici Olmayan) Danışma", "explanation": "Hekimin kişisel görüşlerini dayatmadan, ailenin kendi inanç ve değerleriyle özgürce karar vermesini sağlayan etik ilke."},
                {"term": "Konsültan", "explanation": "Genetik danışma almak amacıyla kliniğe başvuran birey veya aile üyesi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Genetik danışmanın en temel etik kuralı 'Yönlendirici Olmamaktır' (Non-directive); hekim seçenekleri sunar, karar verme hakkı tamamen aileye aittir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Genetik danışmanlık hizmeti sunan bir hekimin 'Bu bebek kesinlikle termine edilmelidir, başka çareniz yok' şeklinde kesin bir hüküm vermesi genetik danışmanın hangi temel ilkesinin doğrudan ihlalidir?",
                    {
                        "A": "Yönlendirici olmayan (Non-directive) danışmanlık ilkesi",
                        "B": "Mendelyen risk hesabı ilkesi",
                        "C": "Pedigri çizim standardı",
                        "D": "Çözünürlük hiyerarşisi ilkesi"
                    },
                    "A",
                    {
                        "A": "Doğru! Genetik danışma kesinlikle non-direktif (yönlendirici olmayan) olmalıdır; hekim seçenekleri ve riskleri tarafsızca anlatır, son kararı aile verir.",
                        "B": "Yanlış. Risk hesabı matematikseldir.",
                        "C": "Yanlış. Pedigri soyağacı çizimidir.",
                        "D": "Yanlış. Test tekniği kuralıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 100,
            "title": "[BÜYÜK FİNAL TEKRAR SAYFASI - MASTER CHECKPOINT 11] Tüm Dersin 10 Kritik Sınav Tuzağı ve İnteraktif Sentez Matrisi",
            "subtitle": "Dismorfolojide Genetik Terminoloji dersinin en yüksek verimli 10 altın kuralı",
            "badge": "Büyük Final Sentezi",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Tebrikler! Dismorfolojide Genetik Terminoloji dersinin 100 atomik adımını tamamladınız.\n\nSınavlara girmeden önce kurul ve komite sorularında puan kaybettiren en kritik 10 kuralı bu son interaktif hafıza tablosunda test edin. Maskeli hücrelere tıklayarak bilgilerinizi kalıcı belleğe kilitleyin!",
            "coreContent": {
                "table": {
                    "title": "Tüm Dersin 10 Kritik Sınav Tuzağı ve Altın Kuralları",
                    "headers": ["Kural No", "Konu Alanı", "Kritik Sınav İlkesi", "Sık Yapılan Hata"],
                    "rows": [
                        ["1", "Monozomi", "Canlı doğabilen tek tam monozomi 45,X'tir (Turner)", "Otozomal monozomilerin canlı doğabileceğini sanmak (letaldir!)"],
                        ["2", "İnversiyon", "Parasentrik krosing-over'da letal gamet üretir; Perisentrik canlı anomalili çocuk doğurabilir", "Parasentriğin canlı anomali yapacağını sanmak"],
                        ["3", "Translokasyon", "Robertsonian yalnızca akrosentriklerde (13,14,15,21,22) olur; taşıyıcıda 45 kromozom vardır", "Metasentrik kromozomlarda aramak"],
                        ["4", "Anomali Sayısı", "3 ve üzeri minör anomali varlığında majör anomali riski %90'a fırlar", "1 minör anomalide hemen paniklemek (risk sadece %3'tür)"],
                        ["5", "Defekt Tipi", "Malformasyon intrinsiktir (cerrahi gerekir); Deformasyon mekaniktir (spontan düzelebilir)", "Deformasyona baştan doku hatası demek"],
                        ["6", "Disrupsiyon", "Amniyotik bant sendromu genetik DEĞİLDİR; tekrarlama riski yoktur", "Amniyotik banda genetik sendrom demek"],
                        ["7", "Potter Sekansı", "Ölüm nedeni böbrek yetmezliği DEĞİL; Pulmoner Hipoplazidir", "Potter'da bebeğin üremiden öldüğünü sanmak"],
                        ["8", "Pierre Robin", "Primer defekt mikrognatidir; dilin geriye kaçmasıyla U şeklinde damak yarılır", "Primer defektin damak yarığı olduğunu sanmak"],
                        ["9", "Birinci Basamak", "Açıklanamayan MKA/MR'de ilk test Mikrodizidir (CMA); CMA dengeli translokasyonu GÖREMEZ", "CMA'nın her şeyi görebileceğini sanmak"],
                        ["10", "Danışma", "Genetik danışma kesinlikle Yönlendirici Olmamalıdır (Non-directive)", "Hekimin aile yerine terminasyon kararı alması"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "10 Altın Kural", "explanation": "Dismorfolojide genetik terminoloji dersinin en yüksek puan getiren komite ve kurul sınav prensipleri."},
                {"term": "Büyük Final Sentezi", "explanation": "Müfredat kazanımlarının tümünün tek bir interaktif kontrol noktasında kilitlenmesi."}
            ],
            "spotPearls": [
                "🚨 [BÜYÜK FİNAL SPOTU] Sınavın en sık sorulan 3 tuzağı: Potter'da ölüm nedeni pulmoner hipoplazidir; CMA dengeli translokasyonu göremez; 3+ minör anomalide majör risk %90'dır!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Tüm Dersin 10 Kritik Sınav Tuzağı Ezber Matrisi",
                    ["Klinik Durum / Soru", "Doğru Bilgi / Mekanizma", "Tuzak / Yanılgı"],
                    [
                        [
                            ("Canlı doğabilen tek monozomi hangisidir?", False),
                            ("45,X (Turner Sendromu)", True, "Turner"),
                            ("Otozomal monozomiler letaldir", False)
                        ],
                        [
                            ("Potter sekansında yenidoğanın asıl ölüm nedeni nedir?", False),
                            ("Pulmoner Hipoplazi (Akciğer gelişememesi)", True, "Pulmoner Hipoplazi"),
                            ("Böbrek yetmezliği DEĞİLDİR!", False)
                        ],
                        [
                            ("Kromozomal Mikrodizi (CMA) hangi tabloyu KESİNLİKLE saptayamaz?", False),
                            ("Dengeli translokasyon ve inversiyonlar", True, "Dengeli translokasyon"),
                            ("Kopya sayısı nötr olduğu için kördür", False)
                        ],
                        [
                            ("3 veya daha fazla minör anomalisi olan bir bebekte majör anomali riski kaçtır?", False),
                            ("%90", True, "%90"),
                            ("1 minör anomalide sadece %3'tür", False)
                        ],
                        [
                            ("Robertsonian translokasyon taşıyıcısında toplam kromozom sayısı kaçtır?", False),
                            ("45 kromozom", True, "45"),
                            ("Fenotipik olarak tamamen sağlıklıdır", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdakilerden hangisi dismorfolojide konjenital defektlerin özellikleriyle ilgili YANLIŞ bir bilgidir?",
                    {
                        "A": "Potter sekansında yenidoğanın kaybedilme nedeni bilateral renal ageneziye bağlı üremidir",
                        "B": "Amniyotik bant sendromu bir disrupsiyondur ve genetik tekrarlama riski yoktur",
                        "C": "Malformasyon intrinsik bir doku hatası iken, deformasyon ekstrinsik mekanik kuvvete bağlıdır",
                        "D": "Kromozomal mikrodizi (CMA), dengeli resiprokal translokasyonları saptayamaz"
                    },
                    "A",
                    {
                        "A": "Doğru yanıt (Yanlış öncül)! Potter sekansında bebek üremiden değil, oligohidramniyosa bağlı gelişen Pulmoner Hipoplazi (akciğer yetmezliği) nedeniyle doğumdan hemen sonra kaybedilir.",
                        "B": "Bu bilgi doğrudur; amniyotik bant disrupsiyondur ve tekrarlamaz.",
                        "C": "Bu bilgi doğrudur; malformasyon intrinsik, deformasyon ekstrinsiktir.",
                        "D": "Bu bilgi doğrudur; CMA kopya sayısı nötr dengeli translokasyonları göremez."
                    }
                )
            ]
        }
    ]
