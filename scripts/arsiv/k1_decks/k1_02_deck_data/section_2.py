#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 2: Hastalık Sürecinin Dört Temel Öğesi (Adımlar 10 - 19)
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
        # Adım 10
        {
            "slideNumber": 10,
            "title": "Hastalık Sürecinin Dört Çekirdeği: Etiyolojiden Sonuca Mantıksal Akış",
            "subtitle": "Etiyoloji nedeni, patogenez mekanizmayı, morfoloji yapısal hasarı, klinik sonuç ise hastadaki fonksiyonel kaybı açıklar.",
            "badge": "Hastalık Çekirdeği",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hastalık süreci rastgele bir kaos değil, ==nedensellik ilkesine dayalı dört aşamalı bir zincirdir==:
1. **Etiyoloji (Neden):** Hastalığı başlatan genetik kusur veya edinsel ajandır; "hastalık neden başladı?" sorusuna yanıt arar.
2. **Patogenez (Mekanizma):** Hücre ve dokularda tetiklenen moleküler ve biyokimyasal basamaklar silsilesidir; "hastalık nasıl gelişti?" sorusunu açıklar.
3. **Morfolojik Değişiklikler (Hasar):** Doku ve hücrelerde gözlenen makroskobik ve mikroskobik yapısal bozulmalardır.
4. **Fonksiyonel ve Klinik Sonuçlar:** Hasarın organ işlevini bozmasıyla beliren semptomlar, bulgular ve klinik tablodur.

> [TEMEL İLKE] Hekim hastayı klinik semptomlarıyla karşılar; doğru tedavi için morfoloji, patogenez ve etiyolojiyi geriye doğru çözmek zorundadır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "1. Etiyoloji", "desc": "Neden: Genetik intrinsik veya edinsel ekstrinsik tetikleyiciler.", "isKey": True},
                    {"title": "2. Patogenez", "desc": "Mekanizma: Moleküler sinyal yollarından hücresel hasara giden biyolojik akış.", "isKey": True},
                    {"title": "3. Morfoloji", "desc": "Yapı: Makroskobik ve mikroskobik görsel doku bozulmaları.", "isKey": True},
                    {"title": "4. Klinik Sonuç", "desc": "İşlev kaybı: Semptomlar, klinik bulgular ve laboratuvar anomalileri.", "isKey": True}
                ],
                "table": {
                    "title": "Hastalık Sürecinin Dört Çekirdeği ve Klinik Karşılıkları",
                    "headers": ["Çekirdek Öğe", "Temel Soru", "Miyokard Enfarktüsü Örneği"],
                    "rows": [
                        ["Etiyoloji", "Hastalık neden başladı?", "Koroner arter aterosklerozu ve plak rüptürü"],
                        ["Patogenez", "Hastalık nasıl gelişti?", "Akut trombüs, koroner oklüzyon, iskemi, ATP tükenmesi, nekroz"],
                        ["Morfoloji", "Dokuda ne değişti?", "Sol ventrikülde koagülasyon nekrozu ve nötrofil infiltrasyonu"],
                        ["Klinik Sonuç", "Hastada ne ortaya çıktı?", "Ezici göğüs ağrısı, kardiyojenik şok, troponin yüksekliği"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hastalık sürecinin dört temel öğesi sırasıyla: Etiyoloji $\\to$ Patogenez $\\to$ Morfoloji $\\to$ Klinikopatolojik sonuçtur.",
                "📌 [SINAV SPOTU] Etiyoloji 'neden', patogenez ise 'nasıl' sorusunun biyolojik karşılığıdır.",
                "🚨 [KRİTİK UYARI] Tek bir etiyolojik neden birden çok patogenetik yolak üzerinden farklı morfolojik sonuçlar doğurabilir."
            ],
            "medicalTerms": [
                {"term": "Etiyoloji", "explanation": "Hastalığın başlangıcından sorumlu olan genetik veya çevresel faktörlerin bütünüdür."},
                {"term": "Patogenez", "explanation": "Etiyolojik etkenin tetiklediği ardışık hücresel ve moleküler mekanizmalar sürecidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hastalık Sürecinin Dört Çekirdek Basamağı",
                    [
                        "1. Etiyoloji: Genetik mutasyonun veya çevresel etkenin süreci tetiklemesi",
                        "2. Patogenez: Hücresel stres ve biyokimyasal kaskatların aktive olması",
                        "3. Morfoloji: Hücre hasarı ve doku mimarisinin mikroskopta bozulması",
                        "4. Klinik Sonuç: Organ rezervinin tükenmesiyle fonksiyonel semptomların belirmesi"
                    ]
                ),
                make_cloze(
                    "Hastalık sürecinde 'hastalık neden başladı?' sorusuna yanıt arayan öğe etiyoloji iken; 'hastalık nasıl gelişti?' sorusunun biyolojik mekanizmasını açıklayan öğe [patogenez] öğesidir.",
                    "patogenez",
                    "Hastalığın gelişim mekanizması ve basamaklar zinciri"
                )
            ]
        },

        # Adım 11
        {
            "slideNumber": 11,
            "title": "Etiyoloji 1: Genetik (İntrinsik) Nedenler ve Tümör Baskılayıcı Genler",
            "subtitle": "Kalıtsal ve somatik gen mutasyonları; hücre döngüsü kontrolünü bozarak neoplazilere ve genetik hastalıklara yol açar.",
            "badge": "Genetik Etiyoloji",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hastalık etiyolojisi **intrinsik (genetik)** ve **ekstrinsik (edinsel)** nedenler olmak üzere ikiye ayrılır. Genetik nedenler bireyin kendi genomundaki kalıtsal veya sonradan kazanılmış kusurları kapsar.

Genetik etiyolojinin temel prototipi **tümör baskılayıcı gen** inaktivasyonudur. Örneğin **BRCA1** ve **BRCA2** genleri çift zincirli DNA kırıklarını onaran nükleer proteinleri kodlar. Bu genlerde mutasyon geliştiğinde DNA hasarı giderilemez, hücrede kontrolsüz çoğalma başlar ve kalıtsal meme ile over karsinomu riski belirgin biçimde artar. Benzer şekilde genomun koruyucusu olan **p53** gen mutasyonları da insan kanserlerinin yarısından fazlasında saptanan ana genetik nedendir.

> [YÜKSEK VERİM] Genetik etiyolojide dış etken olmaksızın hücrenin kendi iç kontrol mekanizmalarının çökmesiyle patoloji başlar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "İntrinsik Doğa", "desc": "Kusur bireyin genomunda (kromozom, gen veya epigenetik) kodlanmıştır.", "isKey": True},
                    {"title": "BRCA1 / BRCA2", "desc": "DNA çift zincir kırık onarımı yapan tümör baskılayıcı genlerdir.", "isKey": True},
                    {"title": "Onkogenez", "desc": "Tümör baskılayıcı gen kaybı malign transformasyonun ana genetik etiyolojisidir.", "isKey": False}
                ],
                "table": {
                    "title": "Kritik Tümör Baskılayıcı Genler ve İlişkili Kanser Sendromları",
                    "headers": ["Gen", "Normal Hücresel Fonksiyonu", "Etiyolojik Mutasyonun Klinik Sonucu"],
                    "rows": [
                        ["BRCA1 / BRCA2", "Homolog rekombinasyon ile DNA çift zincir kırık onarımı", "Herediter meme ve over karsinomu sendromu"],
                        ["TP53 (p53)", "Hücre döngüsü kontrolü (G1/S), apoptoz indüksiyonu", "Li-Fraumeni sendromu ve çoklu organ karsinomları"],
                        ["RB1", "E2F transkripsiyon faktörünü bağlayarak G1/S geçişini frenleme", "Retinoblastom ve osteosarkom gelişimi"],
                        ["APC", "Wnt yolağında beta-katenini yıkarak proliferasyonu baskılama", "Familyal Adenomatöz Polipozis (FAP) ve kolon kanseri"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] BRCA1 ve BRCA2, DNA onarımında görev yapan tümör baskılayıcı genlerdir; mutasyonları meme ve over kanserine neden olur.",
                "📌 [SINAV SPOTU] Tümör baskılayıcı genler hücre çoğalmasını frenler; proto-onkogenler ise hücre büyümesini uyarır.",
                "🚨 [KRİTİK UYARI] Li-Fraumeni sendromunda germline TP53 mutasyonu vardır ve genç yaşta çoklu maligniteler görülür."
            ],
            "medicalTerms": [
                {"term": "Tümör Baskılayıcı Gen", "explanation": "Hücre bölünmesini frenleyen ve inaktivasyonu kansere yol açan koruyucu gendir."},
                {"term": "Germline Mutasyon", "explanation": "Üreme hücrelerinde bulunan ve sonraki nesillere aktarılan kalıtsal mutasyondur."},
                {"term": "Somatik Mutasyon", "explanation": "Yalnızca belirli bir vücut hücresinde sonradan oluşan ve kalıtılmayan mutasyondur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Hastalıkların genetik etiyolojisi kapsamında incelenen BRCA1 ve BRCA2 genleri ile ilgili aşağıdaki ifadelerden hangisi biyolojik olarak doğrudur?",
                    {
                        "A": "Hücre büyümesini uyaran ve mutasyonuyla aşırı çoğalma başlatan proto-onkogenlerdir.",
                        "B": "DNA çift zincir kırıklarını onararak kontrolsüz çoğalmayı önleyen tümör baskılayıcı genlerdir.",
                        "C": "Hücre dışı matrikste kollajen liflerinin çapraz bağlanmasını sağlayan yapısal enzim genleridir.",
                        "D": "Yalnızca viral enfeksiyonlar sırasında devreye giren antiviral interferon genleridir.",
                        "E": "Mitoz bölünmede iğ ipliklerinin sentrozomlara tutunmasını engelleyen mikrotübül genleridir."
                    },
                    "B",
                    {
                        "A": "Yanlış: BRCA genleri onkogen değil, tümör baskılayıcı genlerdir.",
                        "B": "Doğru: BRCA1/2 genleri DNA tamiri yapan tümör baskılayıcı genlerdir.",
                        "C": "Yanlış: Kollajen çapraz bağlanması lizil oksidaz enziminin görevidir.",
                        "D": "Yanlış: BRCA genlerinin antiviral savunma ile doğrudan ilgisi yoktur.",
                        "E": "Yanlış: Mikrotübül tutunması kinetokor proteinlerinin görevidir."
                    }
                ),
                make_cloze(
                    "BRCA1 ve BRCA2 genleri DNA hasarını onaran, inaktivasyonunda herediter meme ve over karsinomu gelişen [tümör baskılayıcı] genler sınıfındadır.",
                    "tümör baskılayıcı",
                    "Hücre bölünmesini frenleyen koruyucu gen kategorisi"
                )
            ]
        },

        # Adım 12
        {
            "slideNumber": 12,
            "title": "Etiyoloji 2: Kromozomal Anomaliler ve Aneuploidiler",
            "subtitle": "Kromozom sayısındaki veya yapısındaki sapmalar; çoklu organ sistemlerini etkileyen sendromik etiyolojilerdir.",
            "badge": "Kromozomal Etiyoloji",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Genetik etiyolojinin kromozom düzeyindeki boyutunu **sitogenetik anomaliler** oluşturur. Burada tek bir nükleotid değişikliği yerine binlerce geni taşıyan kromozom parçaları veya tam kromozomlar eksik ya da fazladır.

Bu durumun klasik prototipi **Trizomi 21 (Down Sendromu)** tablosudur. Mayotik ayrılamama (nondisjunction) sonucu 21. kromozom çiftinde fazladan bir kopya bulunur ve toplam sayı ==47 kromozoma== yükselir. Bu ekstra genetik materyal; kraniofasiyal dismorfoloji, konjenital kalp defektleri (AV kanal defekti), duodenal atrezi ve lösemi yatkınlığı ile seyreden sistemik bir tablo doğurur. Canlı doğan tek monozomi ise 45,X karyotipli Turner sendromudur.

> [KLİNİK İPUCU] Trizomi 21'de tek bir gen değil; 21. kromozomdaki APP ve SOD1 gibi yüzlerce genin aşırı dozu klinik tabloyu belirler.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Aneuploidi", "desc": "Kromozom sayısının 46'nın katları olmayan bir sayıda sapmasıdır.", "isKey": True},
                    {"title": "Trizomi 21", "desc": "21. kromozomun fazladan bir kopyasıyla toplam 47 kromozom bulunmasıdır.", "isKey": True},
                    {"title": "Sistemik Patoloji", "desc": "Konjenital kalp anomalileri, intestinal atreziler ve lösemi yatkınlığı yaratır.", "isKey": False}
                ],
                "table": {
                    "title": "En Sık Canlı Doğan Kromozomal Sayı Anomalileri",
                    "headers": ["Sendrom", "Karyotip Formülü", "Başlıca Patolojik Bulgular"],
                    "rows": [
                        ["Down Sendromu", "47,XX,+21 veya 47,XY,+21", "Brakisefali, epikantus, AV kanal defekti, duodenal atrezi, lösemi riski"],
                        ["Edwards Sendromu", "47,XX,+18 veya 47,XY,+18", "Oksiput belirginliği, mikrosfere fleksiyon, rocker-bottom ayak, VSD"],
                        ["Patau Sendromu", "47,XX,+13 veya 47,XY,+13", "Holoprozensefali, yarık dudak/damak, mikroftalmi, polidaktili"],
                        ["Turner Sendromu", "45,X", "Canlı doğan tek monozomi; yele boyun, aort koarktasyonu, streak over"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Down sendromunun genetik temeli 21. kromozom trizomisidir (toplam 47 kromozom).",
                "📌 [SINAV SPOTU] Canlı doğumla bağdaşan TEK tam monozomi 45,X (Turner Sendromu) tablosudur; otozomal monozomiler letaldir.",
                "🚨 [KRİTİK UYARI] Trizomi 21 olgularında erken yaşta (40 yaş civarı) Alzheimer nöropatolojisi gelişir çünkü APP geni 21. kromozomdadır."
            ],
            "medicalTerms": [
                {"term": "Aneuploidi", "explanation": "Kromozom sayısının normal haploid sayının tam katı olmaması durumudur."},
                {"term": "Nondisjunction", "explanation": "Bölünme sırasında kromozomların ayrılamayarak aynı yavru hücreye gitmesi kusurudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Diploid Hücre vs Trizomi 21 Genetik Yapısı",
                    "Normal Diploid Karyotip (46 Kromozom)",
                    "Down Sendromu / Trizomi 21 (47 Kromozom)",
                    [
                        "2 adet serbest kromozom 21 bulunur",
                        "Normal gen dozu ve dengeli protein sentezi",
                        "Normal kardiyak ve kraniyofasiyal embriyogenez"
                    ],
                    [
                        "3 adet serbest kromozom 21 bulunur",
                        "Gen dozajı %150 artmış (APP, SOD1 aşırı ekspresyonu)",
                        "Endokardiyal yastık defekti ve lösemi yatkınlığı"
                    ]
                ),
                make_cloze(
                    "Down sendromlu bireylerde 21. kromozom çiftinde fazladan bir kromozom bulunması nedeniyle toplam kromozom sayısı [47] olarak saptanır.",
                    "47",
                    "Down sendromundaki toplam diploid kromozom sayısı"
                )
            ]
        },

        # Adım 13
        {
            "slideNumber": 13,
            "title": "Etiyoloji 3: Edinsel (Ekstrinsik) Biyolojik Etkenler ve Enfeksiyonlar",
            "subtitle": "Bakteriler, virüsler, mantarlar ve parazitler; doğrudan sitopatik etki veya immün yanıt yoluyla doku zedelenmesi başlatır.",
            "badge": "Biyolojik Etiyoloji",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Edinsel etiyolojinin başında biyolojik enfeksiyöz ajanlar gelir. Patojenler dokularda üç temel yolla hasar oluşturur:
1. **Doğrudan Sitopatik Hasar:** Virüslerin konak hücre içine girerek replike olması, hücre membranını parçalaması veya apoptozu tetiklemesidir.
2. **Toksin Üretimi:** Bakterilerin protein sentezini bozan ekzotoksinleri veya septik şoka yol açan hücre duvarı endotoksinleridir (LPS).
3. **İmmün Aracılı İkincil Hasar:** Patojenin kendisinden ziyade konağın geliştirdiği aşırı bağışıklık yanıtının dokuyu yıkmasıdır. Örneğin **Tüberküloz** basili tek başına toksin üretmez; akciğerdeki kazeifikasyon nekrozunu başlatan CD4+ T hücre aracılı Tip IV aşırı duyarlılık yanıtıdır.

> [TEMEL İLKE] Enfeksiyonda doku hasarı; patojenin virülansı ile konak bağışıklık yanıtı arasındaki dengenin ürünüdür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Patojen Yelpazesi", "desc": "Prionlar, virüsler, bakteriler, mantarlar ve parazitler etiyolojik ajandır.", "isKey": True},
                    {"title": "Sitopatik Etki", "desc": "Virüslerin konak hücreyi doğrudan patlatması veya apoptoza sürüklemesidir.", "isKey": True},
                    {"title": "İmmün Hasar", "desc": "Patojene saldıran konağın nötrofil ve makrofajlarının çevre dokuyu yıkmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Biyolojik Etkenlerin Patolojik Hasar Oluşturma Mekanizmaları",
                    "headers": ["Mikroorganizma Grubu", "Patojen Örneği", "Temel Patolojik Hasar Mekanizması"],
                    "rows": [
                        ["Virüsler", "Hepatit B ve C Virüsü (HBV/HCV)", "Sitotoksik CD8+ T lenfositlerin enfekte hepatositleri öldürmesi (apoptoz)"],
                        ["Bakteriler (Toksin)", "Clostridium tetani (Tetanospazmin)", "İnhibitör nörotransmitter (GABA/glisin) salınımının blokajı ve spastik felç"],
                        ["Bakteriler (İmmün)", "Mycobacterium tuberculosis", "Gecikmiş tip aşırı duyarlılık ve epiteloid histiositlerden kazeifiye granülom"],
                        ["Mantarlar", "Candida albicans / Aspergillus", "Hif invazyonu, angioinvazyon, vasküler tromboz ve iskemik infarktüs"],
                        ["Parazitler", "Echinococcus granulosus", "Karaciğer ve akciğerde yavaş büyüyen kist hidatik ve bası atrofisi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Tüberkülozda kazeifikasyon nekrozunu yapan basilin toksini DEĞİLDİR; konak T lenfositlerinin oluşturduğu Tip IV aşırı duyarlıktır.",
                "📌 [SINAV SPOTU] Gram negatif bakterilerin hücre duvarındaki Lipopolisakkarit (LPS / Endotoksin) masif sitokin fırtınası ve septik şok başlatır.",
                "🚨 [KRİTİK UYARI] Virüsler zorunlu hücre içi parazitleridir; konak hücre metabolizmasını gasp etmeden canlı kalamaz ve çoğalamazlar."
            ],
            "medicalTerms": [
                {"term": "Sitopatik Etki", "explanation": "Virüslerin konak hücrede oluşturduğu dejeneratif ve öldürücü yapısal hasardır."},
                {"term": "Kazeifiye Granülom", "explanation": "Merkezinde peynirimsi nekroz ve etrafında epiteloid histiositler bulunan kronik odaktır."},
                {"term": "Endotoksin (LPS)", "explanation": "Gram negatif bakterilerin lizisiyle serbest kalan pirojenik lipopolisakkarittir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tüberküloz patolojisinde akciğerde oluşan kazeifikasyon nekrozu ve doku destrüksiyonunun primer mekanizması aşağıdakilerden hangisidir?",
                    {
                        "A": "Basilin salgıladığı güçlü bir ekzotoksinin hücre membranlarını doğrudan eritmesi",
                        "B": "M. tuberculosis'in hücre içine girerek mitokondriyal DNA'yı parçalaması",
                        "C": "Konağın basile karşı geliştirdiği T lenfosit aracılı hücresel immün yanıtın (Tip IV aşırı duyarlılık) dokuyu nekroza uğratması",
                        "D": "Basilin damar lümenini tıkayarak anında arteriyel emboli oluşturması",
                        "E": "Hastanın antikorlarının komplemanı aktive ederek akut lökositoklastik vaskülit yapması"
                    },
                    "C",
                    {
                        "A": "Yanlış: M. tuberculosis dokuyu eriten bir ekzotoksin salgılamaz.",
                        "B": "Yanlış: Basil mitokondriyi doğrudan parçalamak yerine fagozomda yaşar.",
                        "C": "Doğru: Kazeifikasyon nekrozu konağın CD4+ Th1 hücre aracılı Tip IV immün yanıtıyla oluşur.",
                        "D": "Yanlış: Tüberküloz primer arteriyel tromboz yapan bir hastalık değildir.",
                        "E": "Yanlış: Tüberküloz granülomu hücresel immün yanıtla gelişir, humoral vaskülit değildir."
                    }
                ),
                make_active_recall(
                    "Bakteriyel toksinlerden endotoksin (LPS) ile ekzotoksin arasındaki en kritik yapısal ve salınım farkı nedir?",
                    "Ekzotoksinler canlı bakterilerce aktif salgılanan protein yapılı toksinlerdir. Endotoksin (LPS) ise yalnızca Gram negatif bakterilerin dış zarında bulunan ve bakteri öldüğünde açığa çıkan lipopolisakkarittir."
                )
            ]
        },

        # Adım 14
        {
            "slideNumber": 14,
            "title": "Etiyoloji 4: Fiziksel, Kimyasal ve Beslenme Zedeleyicileri",
            "subtitle": "Travma, radyasyon, sıcak-soğuk, ilaçlar, toksinler, hipoksi ve beslenme yetersizlikleri hücresel hasarı tetikler.",
            "badge": "Çevresel Etiyoloji",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Edinsel etiyolojinin enfeksiyon dışı bölümünü fiziksel, kimyasal ve nutrisyonel etkenler oluşturur:
1. **Fiziksel Etkenler:** Travma, termal yanıklar, aşırı soğuk ve DNA'da çift zincir kırıkları oluşturan **iyonize radyasyon**.
2. **Kimyasal Etkenler:** Karaciğerde toksik NAPQI metaboliti ile sentrilobüler nekroz yapan parasetamol aşırı dozu, ağır metaller ve alkol.
3. **Hipoksi ve İskemi:** Hücre zedelenmesinin ==en yaygın ve evrensel nedenidir==. İskemi (kan akımı kesintisi), glukoz girişini de durdurup asidik metabolitleri biriktirdiği için izole hipoksiden çok daha yıkıcıdır.
4. **Beslenme Bozuklukları:** Protein-enerji malnütrisyonu, vitamin eksiklikleri (skorbüt) veya obezite.

> [TEMEL İLKE] İskemi ve hipoksi; ATP üretimini durdurup iyon pompalarını felç ederek zedelenmeyi başlatır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hipoksi vs İskemi", "desc": "İskemi kan akımı kesintisi olduğu için tek başına hipoksiden çok daha yıkıcıdır.", "isKey": True},
                    {"title": "İyonize Radyasyon", "desc": "Radyolizis ile serbest oksijen radikalleri (ROS) ve DNA kırıkları oluşturur.", "isKey": True},
                    {"title": "Kimyasal Hasar", "desc": "Doğrudan sitotoksisite ya da karaciğerde reaktif metabolitlere dönüşerek hasar verir.", "isKey": False}
                ],
                "table": {
                    "title": "Fiziksel, Kimyasal ve Beslenme Zedeleyicilerinin Özet Tablosu",
                    "headers": ["Etiyoloji Türü", "Özgül Etken", "Temel Hücresel Patoloji"],
                    "rows": [
                        ["Fiziksel", "İyonize Radyasyon", "DNA çift zincir kırığı, p53 aktivasyonu ve endotel hasarı"],
                        ["Fiziksel", "Aşırı Sıcak (Termal Yanık)", "Protein denatürasyonu, koagülasyon nekrozu, plazma kaybı"],
                        ["Kimyasal", "Parasetamol Aşırı Dozu", "GSH tükenmesi, NAPQI metaboliti ile karaciğer Zone 3 nekrozu"],
                        ["Oksijen Azlığı", "Koroner Arter Trombozu (İskemi)", "Mitokondriyal oksidatif fosforilasyon durması, ATP kaybı"],
                        ["Beslenme", "C Vitamini Eksikliği (Skorbüt)", "Prolil ve lizil hidroksilaz kofaktör eksikliği, kollajen sentez kusuru"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarının klinik pratikte en sık rastlanan evrensel nedeni hipoksi ve iskemidir.",
                "📌 [SINAV SPOTU] İskemi hipoksiden daha tehlikelidir; çünkü anaerobik glikoliz için gerekli glukoz akışı da durur ve metabolitler birikir.",
                "🚨 [KRİTİK UYARI] Parasetamol karaciğerde CYP2E1 ile toksik NAPQI'ye dönüşür; glutatyon (GSH) tükenince masif sentrilobüler nekroz başlar."
            ],
            "medicalTerms": [
                {"term": "Hipoksi", "explanation": "Hücre ve dokuların gereksinim duyduğu oksijen düzeyinin yetersiz olması durumudur."},
                {"term": "İskemi", "explanation": "Dokuya arteriyel kan akımının azalması veya tamamen kesilmesi tablosudur."},
                {"term": "Reaktif Oksijen Türleri (ROS)", "explanation": "Lipit peroksidasyonu ve DNA hasarı yapan yüksek reaktiviteli serbest radikallerdir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "İskemi ile İzole Hipoksi Arasındaki Patofizyolojik Fark",
                    "İzole Hipoksi (Ör. Anemi / Yüksek İrtifa)",
                    "İskemi (Arteriyel Kan Akımının Kesilmesi)",
                    [
                        "Kan akımı devam eder, glukoz dokuya ulaşır",
                        "Glikolitik substrat varlığıyla bir süre anaerobik ATP üretilir",
                        "Laktik asit ve metabolitler venöz yolla yıkanarak uzaklaştırılır"
                    ],
                    [
                        "Kan akımı tamamen durmuştur, glukoz girişi yoktur",
                        "Glikoliz çok hızlı durur ve ATP dakikalar içinde tükenir",
                        "Asidik metabolitler dokuda birikerek hücreyi hızla nekroza sokar"
                    ]
                ),
                make_cloze(
                    "Hücre zedelenmesinde kan akımının durması anlamına gelen [iskemi] tablosu, tek başına arteryel oksijen düşüklüğü olan hipoksiye göre çok daha hızlı ve ağır doku nekrozu yaratır.",
                    "iskemi",
                    "Dokuya arteryel kan akışının kesilmesi durumu"
                )
            ]
        },

        # Adım 15
        {
            "slideNumber": 15,
            "title": "Patogenez: Etiyolojik Uyarandan Klinik Tabloya Giden Olaylar Zinciri",
            "subtitle": "Patogenez; başlatıcı nedenden itibaren hücre ve dokuda sırayla gelişen mekanizmalar dizisidir.",
            "badge": "Mekanizma Zinciri",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Etiyoloji hastalığın nedenini sorgularken, **patogenez** ==etkenin hücre ve dokularda tetiklediği biyolojik mekanizmalar kaskadıdır==.

Başlatıcı uyarandan klinik tablonun ortaya çıkışına kadar gerçekleşen tüm biyokimyasal, moleküler ve morfolojik olaylar patogenezi oluşturur. Patogenezi kavramak modern farmakoterapinin temelidir. Etiyolojik nedeni doğrudan yok etmek her zaman mümkün olmasa bile (örneğin genetik bir mutasyonu değiştiremesek de), **patogenetik basamaklar ilaçlarla bloke edilerek** hastalık durdurulabilir. Örneğin romatoid artritte eklem kıkırdağını yıkan patogenetik TNF-alfa sitokini, anti-TNF biyolojik ajanlarla hedeflenerek eklem hasarı başarıyla önlenir.

> [YÜKSEK VERİM] Etiyoloji hastalığı ateşleyen kıvılcım; patogenez ise hasara ilerleyen biyolojik olaylar zinciridir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mekanizma Bütünlüğü", "desc": "Nedenden doku hasarına kadar ardışık basamaklar zinciridir.", "isKey": True},
                    {"title": "Tedavi Hedefi", "desc": "Farmakolojik tedavilerin büyük kısmı patogenetik yolakları bloke eder.", "isKey": True},
                    {"title": "Zaman Boyutu", "desc": "Moleküler sinyal iletiminden kronik fibrozise kadar zamansal evreleri kapsar.", "isKey": False}
                ],
                "table": {
                    "title": "Etiyoloji, Patogenez ve Farmakolojik Müdahale Karşılaştırması",
                    "headers": ["Hastalık", "Etiyolojik Başlangıç", "Patogenetik Kaskat Basamağı", "Patogenezi Hedefleyen Tedavi"],
                    "rows": [
                        ["Romatoid Artrit", "Bilinmeyen otoantijen / HLA-DRB1", "Sinovyal makrofajlardan TNF-alfa ve IL-1 salınımı", "Anti-TNF biyolojik ajanlar (İnfliksimab)"],
                        ["Ateroskleroz", "Hiperlipidemi ve endotel hasarı", "Köpük hücre birikimi, inflamasyon, fibröz plak çatlaması", "Statinler ve anti-inflamatuvar tedaviler"],
                        ["Peptik Ülser", "Helicobacter pylori enfeksiyonu", "Mukozal bariyer yıkımı, asit penetrasyonu, doku nekrozu", "Proton pompası inhibitörleri ve antibiyotik"],
                        ["Akut Astım", "Alerjen maruziyeti (IgE yanıtı)", "Mast hücresi degranülasyonu, lökotrien salınımı, bronkospazm", "Lökotrien reseptör antagonistleri (Montelukast)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patogenez, etiyolojik ajanın başlattığı moleküler, hücresel ve dokusal olaylar zinciridir.",
                "📌 [SINAV SPOTU] Etiyoloji bilinmese dahi patogenez aydınlatıldığında hedefe yönelik rasyonel tedavi geliştirilebilir.",
                "🚨 [KRİTİK UYARI] Hastalıkların klinik belirtileri etiyolojinin değil; patogenetik sürecin doku mimarisini bozmasının sonucudur."
            ],
            "medicalTerms": [
                {"term": "Patogenez", "explanation": "Etiyolojik etkenin doku hasarı oluşturana dek tetiklediği hücresel mekanizmalar sürecidir."},
                {"term": "Sitokin Fırtınası", "explanation": "Kontrolsüz sitokin salınımıyla çoklu organ yetmezliğine yol açan aşırı immün yanıttır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Aterosklerozda Etiyolojiden Klinik Sona Patogenez Zinciri",
                    [
                        "1. Etiyolojik Tetikleyici: Kronik endotel hasarının damar duvarını zedelemesi",
                        "2. Moleküler Patogenez: Adezyon molekülleri artışıyla okside LDL'nin intimaya girişi",
                        "3. Hücresel Yanıt: Monositlerin intimada lipit yutarak köpük hücrelerine dönüşmesi",
                        "4. Doku Morfolojisi: Fibröz kılıflı aterom plağının lümeni daraltacak boyuta ulaşması",
                        "5. Klinik Sonuç: Plak çatlaması üzerine oturan trombüsün akut enfarktüs yapması"
                    ]
                ),
                make_branching_logic(
                    "Romatoid artritli bir hastada eklem destrüksiyonunu engellemek amacıyla monoklonal anti-TNF antikor tedavisi başlanıyor. Bu tedavi hastalığın hangi çekirdek öğesini doğrudan hedef almaktadır?",
                    [
                        {"text": "Hastalığın patogenezinde doku yıkımını yöneten kritik sitokin yolağını", "isCorrect": True, "feedback": "Harika bir patolojik kavrayış! Anti-TNF tedavisi etiyolojiyi değil; eklem kıkırdağını yıkan patogenetik basamağı bloke ederek hastalığı durdurur."},
                        {"text": "Hastalığı başlatan primer genetik mutasyonu", "isCorrect": False, "feedback": "Hatalı bilgi. Monoklonal antikorlar genetik yapıyı değiştirmez; patogenetik mediyatörü bağlar."},
                        {"text": "Hastanın eklemindeki morfolojik nekrozu cerrahi olarak çıkarmayı", "isCorrect": False, "feedback": "Hatalı seçenek. Medikal tedavi cerrahi bir eksizyon değildir."}
                    ]
                )
            ]
        },

        # Adım 16
        {
            "slideNumber": 16,
            "title": "Patogenez Düzeyleri: Moleküler, Hücresel ve Doku Kaskatları",
            "subtitle": "Patogenetik olaylar moleküler sinyal yollarında başlar, hücresel fenotipe yansır ve doku düzeyinde organize olur.",
            "badge": "Kaskat Düzeyleri",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patogenetik kaskat zamansal ve mekansal olarak üç ana katmanda gerçekleşir:
1. **Moleküler Düzey:** Patogenezin ilk evresidir. Gen mutasyonları, reseptör artışı (HER2) ve kontrolsüz sinyal aktivasyonları (MAPK, PI3K/Akt) bu basamaktadır; hücre morfolojik olarak henüz normal görünebilir.
2. **Hücresel Düzey:** Moleküler sapmaların organellere yansımasıdır. Mitokondriyal hasar, sitokrom c sızıntısı, ATP tükenmesi ve membran yırtılması veya programlı apoptoz bu evrede gerçekleşir.
3. **Doku ve Organ Düzeyi:** Hücresel hasarın kümülatif sonucudur. Nekrotik hücreler inflamasyonu uyarır, matriks yıkılır ve ardından fibröz doku yanıtı (desmoplazi veya skar) gelişir.

> [KLİNİK İPUCU] Patogenez moleküler sinyalle başlar, organel hasarıyla ilerler ve dokuda inflamasyonla organize olur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Moleküler Faz", "desc": "Gen transkripsiyonu, sinyal kaskatları ve biyokimyasal hasarlar.", "isKey": True},
                    {"title": "Hücresel Faz", "desc": "Organel disfonksiyonu, ATP tükenmesi, lizozomal sızıntı ve hücre ölümü.", "isKey": True},
                    {"title": "Doku Fazı", "desc": "İnflamatuvar eksüda, anjiyogenez, matriks yıkımı ve skar dokusu.", "isKey": True}
                ],
                "table": {
                    "title": "Patogenezin Üç Düzeyinin Karşılaştırmalı Dinamiği",
                    "headers": ["Patogenez Düzeyi", "Temel Biyolojik Olay", "Klinik Örnek (Kanser Patogenezi)"],
                    "rows": [
                        ["Moleküler Düzey", "Sinyal yolları, onkogen aktivasyonu, DNA tamir defekti", "KRAS geninde kodon 12 nokta mutasyonu ile sürekli GTP bağlanması"],
                        ["Hücresel Düzey", "Apoptoza direnç, kontrolsüz mitoz, telomeraz aktivasyonu", "Kolon epitel hücresinin ölümsüzleşip displastik klona dönüşmesi"],
                        ["Doku Düzeyi", "Bazal membran invazyonu, anjiyogenez, stromal desmoplazi", "Tümör hücrelerinin muskularis mukozayı delip lenfatiklere girmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patogenez moleküler sinyal anomalisiyle başlar, hücresel organel hasarıyla ilerler, dokuda inflamasyon ve nekrozla sonuçlanır.",
                "📌 [SINAV SPOTU] Apoptoz hücre büzüşmesi ve nükleer parçalanma ile giden, çevreye inflamasyon sızdırmayan programlı hücre ölümüdür.",
                "🚨 [KRİTİK UYARI] Nekroz daima patolojiktir ve hücre zarının yırtılmasıyla çevre dokuda masif inflamatuvar yanıt başlatır."
            ],
            "medicalTerms": [
                {"term": "Apoptoz", "explanation": "Membran bütünlüğünün korunduğu ve inflamasyon yaratmayan programlı hücre ölümüdür."},
                {"term": "Nekroz", "explanation": "Hücre zarının parçalandığı ve çevre dokuda inflamasyon başlatan patolojik ölümdür."},
                {"term": "Desmoplazi", "explanation": "Malign tümörlerin çevre stromada uyardığı kolajenden zengin sert bağ dokusu yanıtıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Hücresel Düzeyde İki Ölüm Biçimi: Apoptoz vs Nekroz",
                    "Apoptoz (Programlı Hücre Ölümü)",
                    "Nekroz (Patolojik Hücre Ölümü)",
                    [
                        "Hücre büzüşür, kromatin yoğunlaşır",
                        "Hücre zarı sağlam kalır, apoptotik cisimcikler oluşur",
                        "Çevre dokuda inflamatuvar yanıt oluşturmaz"
                    ],
                    [
                        "Hücre ve organeller şişerek patlar",
                        "Hücre zarı parçalanır, enzimler dışarı sızar",
                        "Çevre dokuda daima belirgin inflamasyon tetikler"
                    ]
                ),
                make_cloze(
                    "İnvaziv malign epitelyal tümörlerin çevre stromada indüklediği yoğun, kolajenden zengin sert bağ dokusu reaksiyonuna [desmoplazi] adı verilir.",
                    "desmoplazi",
                    "Malign tümörlerin oluşturduğu sert fibröz stroma yanıtı"
                )
            ]
        },

        # Adım 17
        {
            "slideNumber": 17,
            "title": "Morfolojik Değişiklikler: Makroskopi, Mikroskopi ve Ultrastrüktür",
            "subtitle": "Yapısal hasar çıplak gözle organda başlar, ışık mikroskobunda dokuya, elektron mikroskobunda organele kadar izlenir.",
            "badge": "Morfolojik Düzey",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojinin alametifarikası olan **morfolojik değişiklikler**, hastalık sürecinin dokuda bıraktığı yapısal izlerdir. Morfolojik inceleme üç kademede yürütülür:
1. **Makroskobik İnceleme (Brüt Morfoloji):** Dokunun çıplak gözle incelenmesidir. Lezyonun boyutu, rengi, kıvamı ve cerrahi sınıra mesafesi değerlendirilerek doğru örnekleme haritası çıkarılır.
2. **Mikroskobik İnceleme (Işık Mikroskopisi):** Doku kesitlerinin Hematoksilen-Eozin (HE) ile değerlendirilmesidir. Doku mimarisi, hücresel pleomorfizm ve mitotik aktivite bu aşamada belirlenir.
3. **Ultrastrüktürel İnceleme (Elektron Mikroskopisi):** Glomerül bazal membranı ve podosit ayakları gibi nanometrik organel ayrıntılarını aydınlatır.

> [TEMEL İLKE] Hatalı bir makroskopi mikroskopla telafi edilemez; doğru doku örneklemesi tanının temel şartıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Makroskopi", "desc": "Çıplak gözle organın rengi, boyutu, kıvamı ve cerrahi sınırları incelenir.", "isKey": True},
                    {"title": "Mikroskopi", "desc": "Işık mikroskobunda doku mimarisi, hücresel atipi ve mitoz değerlendirilir.", "isKey": True},
                    {"title": "Ultrastrüktür", "desc": "Elektron mikroskobuyla organel düzeyindeki nanometrik hasarlar saptanır.", "isKey": False}
                ],
                "table": {
                    "title": "Morfolojik İnceleme Kademelerinin Karşılaştırması",
                    "headers": ["İnceleme Düzeyi", "Çözünürlük ve Büyütme", "Değerlendirilen Patolojik Parametreler"],
                    "rows": [
                        ["Makroskopi", "Çıplak göz / Büyüteç (1x - 10x)", "Kitle boyutu, rengi, nekroz alanları, cerrahi sınıra mesafe"],
                        ["Işık Mikroskopisi", "0.2 mikrometre (40x - 1000x)", "Doku mimarisi, hücresel pleomorfizm, mitotik figürler, anjiyogenez"],
                        ["Elektron Mikroskobu (TEM)", "0.2 nanometre (10.000x - 500.000x)", "Bazal membran immün kompleks birikintileri, mikrovilluslar, organeller"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Makroskopi, mikroskopik tanının kalitesini belirleyen en kritik ilk basamaktır; lezyonun cerrahi sınıra mesafesi makroskopide ölçülür.",
                "📌 [SINAV SPOTU] Işık mikroskobunun çözünürlük sınırı ~0.2 mikrometre, transmisyon elektron mikroskobunun sınırı ~0.2 nanometredir.",
                "🚨 [KRİTİK UYARI] Makroskobik incelemede şüpheli alanlardan yeterli sayıda parça (örnekleme) alınmazsa mikroskopta tümör atlanabilir."
            ],
            "medicalTerms": [
                {"term": "Makroskopi", "explanation": "Doku ve organların mikroskop öncesi çıplak gözle incelenip disseke edilmesidir."},
                {"term": "Pleomorfizm", "explanation": "Tümör hücrelerinin ve çekirdeklerinin boyut ve şekil değişkenliği göstermesidir."},
                {"term": "Lenfovasküler İnvazyon", "explanation": "Tümör hücrelerinin damar ve lenfatik kanalların lümenine girmesi durumudur."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Morfolojik Değerlendirme Basamakları ve Tanısal Karşılıkları",
                    ["İnceleme Düzeyi", "Kullanılan Araç", "Görülen Tipik Bulgu", "Klinik Anlamı"],
                    [
                        [("Makroskopi", False), ("Çıplak Göz / Kumpas", False), ("3 cm çaplı sert düzensiz kitle", False), ("Tümör boyut evrelemesi (T2)", True, "TNM parametresi")],
                        [("Işık Mikroskopisi", False), ("Optik Mikroskop (HE)", False), ("Atipik mitotik figürler ve nekroz", False), ("Yüksek histolojik derece (Grade 3)", True, "Agresiflik derecesi")],
                        [("Elektron Mikroskobu", False), ("Transmisyon EM", False), ("Elektron yoğun subepitelyal birikim", False), ("Membranöz glomerülonefrit", True, "Nefrotik hastalık tipi")]
                    ]
                ),
                make_cloze(
                    "Malign tümör dokusunda hücrelerin ve çekirdeklerinin birbirine benzemeyip boyut ve şekil olarak aşırı değişkenlik göstermesine [pleomorfizm] adı verilir.",
                    "pleomorfizm",
                    "Hücresel ve nükleer şekil-boyut çeşitliliği"
                )
            ]
        },

        # Adım 18
        {
            "slideNumber": 18,
            "title": "Fonksiyonel ve Klinik Sonuçlar: Kliniko-Patolojik Korelasyonun Esasları",
            "subtitle": "Morfolojik hasarın organ fonksiyonunu bozmasıyla hastalık hastanın semptom ve bulgularına yansır.",
            "badge": "Klinik Yansıma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hastalık sürecinin dördüncü ve nihai halkası **fonksiyonel ve klinik sonuçlardır**. Hücre ve dokularda biriken yapısal hasar belirli bir eşiği aştığında organın fonksiyonel rezervi tükenir ve klinik belirtiler patlak verir.

Örneğin sirozda karaciğerin yaygın fibrozis ve rejenerasyon nodülleriyle dolması (morfolojik hasar), portal kan akımını mekanik olarak engeller. Bu yapısal tıkanıklık portal hipertansiyona (fonksiyonel sonuç), o da özofagus varis kanamalarına ve asite (klinik tablo) yol açar. Patoloji eğitiminin nihai gayesi **Kliniko-Patolojik Korelasyon (CPC)** kurarak, hastanın klinik şikayetlerini mikroskop altındaki doku patolojisiyle eksiksiz bağdaştırabilmektir.

> [TEMEL İLKE] Kliniko-patolojik korelasyon; hastanın semptomlarını hücresel hasar temeline oturtan hekimlik sanatıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Fonksiyonel Bozulma", "desc": "Yapısal hasarın organ rezervini tüketerek fizyolojik işleyişi aksatmasıdır.", "isKey": True},
                    {"title": "Klinik Belirti ve Bulgular", "desc": "Hastanın hissettiği semptomlar ve hekimin muayenede saptadığı bulgulardır.", "isKey": True},
                    {"title": "CPC Kavramı", "desc": "Klinik tablo ile patolojik tanının karşılıklı örtüşmesi ve doğrulanmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Morfolojik Hasardan Klinik Semptoma Uzanan Patofizyolojik Zincir",
                    "headers": ["Organ", "Primer Morfolojik Hasar", "Fonksiyonel Bozukluk", "Klinik Semptom ve Bulgu"],
                    "rows": [
                        ["Karaciğer", "Yaygın fibrozis ve rejenerasyon nodülleri (Siroz)", "Portal vasküler direnç artışı ve albumin sentez azlığı", "Asit, bacaklarda ödem, özofagus varis kanaması"],
                        ["Akciğer", "Alveol lümenlerinde fibrin ve nötrofil dolumu (Lobar Pnömoni)", "Ventilasyon-perfüzyon uyumsuzluğu ve difüzyon bloku", "Hipoşemi, siyanoz, takipne, balgamlı öksürük"],
                        ["Kalp", "Sol ventrikül ön duvarında koagülasyon nekrozu (MI)", "Miyokardiyal kontraktilite kaybı ve ejeksiyon fraksiyonu düşüşü", "Akut akciğer ödemi, hipotansiyon, ezici göğüs ağrısı"],
                        ["Böbrek", "Glomerül podosit ayaksı çıkıntılarının silinmesi", "Glomerüler filtrasyon bariyerinin negatif yükünü yitirmesi", "Günde >3.5 gram masif proteinüri, anazarka ödemi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kliniko-patolojik korelasyon (CPC), klinik semptomların altta yatan doku morfolojisi ile açıklanmasıdır.",
                "📌 [SINAV SPOTU] Bir organın morfolojik hasarı belirli bir eşiği (organ rezervi) aşmadıkça klinik belirti vermeyebilir (subklinik dönem).",
                "🚨 [KRİTİK UYARI] Tedavi yalnızca semptomları değil; o semptomları doğuran altta yatan primer patolojiyi hedeflemelidir."
            ],
            "medicalTerms": [
                {"term": "Kliniko-Patolojik Korelasyon (CPC)", "explanation": "Klinik semptomların altta yatan mikroskobik doku lezyonlarıyla eşleştirilmesidir."},
                {"term": "Organ Rezervi", "explanation": "Bir organın normal fizyolojik ihtiyacın üzerinde sahip olduğu yedek fonksiyonel kapasitedir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Sirozlu bir hastada gelişen asit (karında sıvı birikimi) ve özofagus varis kanamaları hastalık sürecinin hangi öğesini temsil eder?",
                    {
                        "A": "Primer etiyolojik başlangıç nedenini",
                        "B": "Mikroskop altındaki hücresel gen mutasyonunu",
                        "C": "Karaciğerdeki morfolojik hasarın doğurduğu fonksiyonel ve klinik sonuçları",
                        "D": "Klinisyenin patoloğa yazdığı istek formundaki ön tanıyı",
                        "E": "Doku takibinde alkol serileriyle yapılan dehidrasyon aşamasını"
                    },
                    "C",
                    {
                        "A": "Yanlış: Etiyolojik neden viral hepatit veya alkoldür; asit sonuçtur.",
                        "B": "Yanlış: Asit klinik bir bulgudur, hücresel mutasyon değildir.",
                        "C": "Doğru: Karaciğerdeki yapısal hasarın portal hipertansiyonla doğurduğu klinik sonuçtur.",
                        "D": "Yanlış: Bu işlem klinik ve idari bir adımdır.",
                        "E": "Yanlış: Dehidrasyon patoloji laboratuvarındaki doku takibi basamağıdır."
                    }
                ),
                make_active_recall(
                    "Tıpta 'Organ Rezervi' kavramı hastalıkların klinik tablosunun ortaya çıkışında neden kritik bir rol oynar?",
                    "Organlar normal ihtiyacın üzerinde yüksek yedek kapasiteye sahiptir. Yapısal doku harabiyeti bu rezervi aşana kadar hastalık sessiz (subklinik) seyreder; rezerv tükendiğinde ise dekompanse yetmezlik tablosu aniden ortaya çıkar."
                )
            ]
        },

        # Adım 19 (CHECKPOINT 2)
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Hastalık Sürecinin Dört Temel Öğesi",
            "subtitle": "Etiyoloji, patogenez, morfoloji ve klinik sonuç eksenindeki sınav ayrımlarını akıl kartlarıyla pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 2,
            "synthesisNarrative": """Hastalık sürecinin ikinci büyük kavşağı tamamlandı. Her patolojik süreç; **etiyoloji** (neden) ile başlar, **patogenez** (biyolojik mekanizmalar) ile ilerler, **morfolojik değişiklikler** (makroskopi, mikroskopi, ultrastrüktür) ile yapısal hasar oluşturur ve **fonksiyonel-klinik sonuçlar** (semptom, bulgu) ile hastada belirir.

Etiyolojide intrinsik genetik mutasyonlar (BRCA1/2, Down sendromu) ile ekstrinsik faktörler (biyolojik enfeksiyonlar, kimyasallar ve en sık neden olan iskemi/hipoksi) yer alır. Patogenez moleküler düzeyde başlar, hücresel düzeyde apoptoz veya nekroz doğurur ve dokuda organize olur. Teşhis, klinik tablodan geriye giderek bu dört halkayı aydınlatma sanatıdır.

> [BÖLÜM ÖZETİ] Tanı ve tedavi; klinik semptomdan geriye doğru giderek doku morfolojisini, patogenezi ve etiyolojiyi çözme sürecidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Dörtlü Mantık", "desc": "Neden (Etiyoloji) -> Mekanizma (Patogenez) -> Hasar (Morfoloji) -> Sonuç (Klinik).", "isKey": True},
                    {"title": "İskemi Önemi", "desc": "Hücresel zedelenmenin klinikteki en yaygın evrensel etiyolojisidir.", "isKey": True},
                    {"title": "BRCA ve Down", "desc": "Genetik etiyolojinin tümör baskılayıcı ve aneuploidi prototipleridir.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 2 Dört Çekirdek Öğe Sentez Tablosu",
                    "headers": ["Çekirdek Öğe", "Biyolojik Karşılık", "Kilit Sınav Vurgusu"],
                    "rows": [
                        ["Etiyoloji", "Hastalığı başlatan intrinsik/ekstrinsik neden", "İskemi en sık edinsel; BRCA1/2 ve Trizomi 21 klasik genetik nedenlerdir"],
                        ["Patogenez", "Nedenden hasara giden biyolojik basamaklar", "Tedavi ilaçlarının çoğu etiyolojiyi değil patogenetik kaskadı hedefler"],
                        ["Morfoloji", "Doku ve hücrede oluşan yapısal bozulma", "Makroskopi, mikroskopi ve ultrastrüktür olmak üzere üç düzeyde incelenir"],
                        ["Klinik Sonuç", "Yapısal hasarın hastadaki semptom ve bulguları", "Kliniko-patolojik korelasyon (CPC) tanının doğrulanmasında esastır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hastalık sürecinin dört bileşeni: Etiyoloji, patogenez, morfolojik değişiklik ve klinik sonuçtur.",
                "📌 [SINAV SPOTU] Hücre zedelenmesinin en sık edinsel nedeni hipoksi ve iskemidir; iskemi anaerobik yolu da kestiği için daha ağırdır.",
                "🚨 [KRİTİK UYARI] Tüberkülozda doku nekrozunu yapan basilin toksini değil; konağın T hücreli aşırı duyarlık yanıtıdır."
            ],
            "medicalTerms": [
                {"term": "Patogenez", "explanation": "Etiyolojik etkenin doku hasarı oluşturana dek tetiklediği hücresel mekanizmalar sürecidir."},
                {"term": "Desmoplazi", "explanation": "Malign tümörlerin çevre stromada indüklediği kolajenden zengin sert bağ dokusu yanıtıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p2-1",
                    "Hastalık etiyolojisinde BRCA1 ve BRCA2 gen mutasyonlarının hücresel mekanizması ve klinik riski nedir?",
                    "BRCA1 ve BRCA2 DNA çift zincir kırıklarını homolog rekombinasyonla onaran tümör baskılayıcı genlerdir. İnaktivasyonlarında DNA hasarı onarılamaz ve herediter meme ile over karsinomu riski dramatik olarak artar.",
                    "DNA onarımı ve kanser",
                    "Genetik Etiyoloji"
                ),
                make_flashcard(
                    "fc-p2-2",
                    "İskemi ile izole hipoksi arasındaki patofizyolojik fark nedir ve hangisi dokuyu daha hızlı nekroza sokar?",
                    "İzole hipokside kan akımı sürer, glukoz girişi ve metabolit uzaklaştırılması devam eder. İskemide ise kan akımı tamamen durduğundan glukoz girişi de kesilir ve asidik metabolitler birikir; bu nedenle iskemi dokuyu hipoksiden çok daha hızlı nekroza sokar.",
                    "Kan akımı kesintisi",
                    "Hücre Zedelenmesi"
                ),
                make_flashcard(
                    "fc-p2-3",
                    "Patolojide 'Kliniko-Patolojik Korelasyon (CPC)' ne anlama gelir?",
                    "Hastanın fizik muayene semptomları, laboratuvar sapmaları ve radyolojik görüntülerinin; biyopsi veya otopside saptanan histopatolojik doku lezyonlarıyla karşılıklı olarak eşleştirilip doğrulanması sürecidir.",
                    "Klinik ve patoloji uyumu",
                    "Klinik Patoloji"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 2'de ele alınan hastalık süreci basamakları değerlendirildiğinde, aşağıdakilerden hangisi yanlıştır?",
                    {
                        "A": "Patogenez aydınlatıldığında etiyoloji tam bilinmese bile hedefe yönelik ilaç geliştirilebilir.",
                        "B": "Down sendromunda toplam kromozom sayısı 47'dir ve 21. kromozom trizomisidir.",
                        "C": "Hücre zedelenmesinin en sık evrensel edinsel nedeni iskemi ve hipoksidir.",
                        "D": "Apoptoz hücre zarını parçalayarak çevre dokuda daima masif nötrofilik inflamasyon başlatır.",
                        "E": "Makroskobik inceleme, cerrahi sınırların ve doku örneklemesinin yapıldığı ilk kritik basamaktır."
                    },
                    "D",
                    {
                        "A": "Doğru: Romatoid artritte anti-TNF tedavisi etiyolojiyi değil patogenezi hedefler.",
                        "B": "Doğru: Down sendromu 21. kromozom trizomisidir ve toplam 47 kromozom bulunur.",
                        "C": "Doğru: Hücre zedelenmesinin klinikteki en yaygın nedeni iskemi ve hipoksidir.",
                        "D": "Yanlış (aranan cevap): Apoptoz inflamasyon yapmaz; çevre dokuda inflamasyon başlatan ölüm tipi nekrozdur.",
                        "E": "Doğru: Makroskobik inceleme doğru doku örneklemesi ve cerrahi sınır için zorunludur."
                    }
                ),
                make_active_recall(
                    "Tüberküloz patolojisinde akciğerde oluşan kazeifikasyon nekrozunun primer sorumlusu basilin kendisi midir yoksa konağın immün sistemi midir?",
                    "Primer sorumlu konağın kendi immün sistemidir. M. tuberculosis hiçbir toksin salgılamaz; doku nekrozu konağın CD4+ T lenfositlerinin basili sınırlamak için başlattığı Tip IV aşırı duyarlılık yanıtının sonucudur."
                )
            ]
        }
    ]
