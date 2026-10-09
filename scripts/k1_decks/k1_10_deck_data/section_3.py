"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 3 (Slayt 21 - 30)
Konu: Translokasyon Biyolojisi, Resiprokal ve Robertsonian Translokasyonlar, Segregasyon Riskleri
Checkpoint: Slayt 29 ([TEKRAR SAYFASI - CHECKPOINT 3])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_3_slides():
    return [
        # Slayt 21
        {
            "title": "Translokasyon Çeşitleri: Resiprokal Translokasyon ve Kuadrivalan Yapısı",
            "subtitle": "Homolog Olmayan Kromozomlar Arasında Parça Değişimi",
            "badge": "Resiprokal Translokasyon",
            "coreContent": {
                "text": "Translokasyon, genetik materyalin homolog olmayan iki (veya daha fazla) kromozom arasında yer değiştirmesidir. En yaygın iki tipi resiprokal ve Robertsonian translokasyonlardır. Resiprokal translokasyon, homolog olmayan iki kromozomda birer kırık meydana gelmesi ve sentromersiz kırık parçaların karşılıklı olarak yer değiştirmesiyle oluşur. Genomik materyalin net miktarı değişmediği için taşıyıcı birey fenotipik olarak tamamen sağlıklıdır. Ancak mayoz I profazında homolog segmentlerin eşleşebilmesi için iki normal ve iki türev (der) kromozom bir araya gelerek 'kuadrivalan' (dörtlü haç biçimli yapı) oluşturmak zorundadır. Bu kuadrivalan yapısının anafaz I'de kutuplara ayrılma (segregasyon) biçimi, gametlerin dengeli mi yoksa ağır delesyon ve duplikasyonlar içeren dengesiz mi olacağını belirler. Bu nedenle resiprokal translokasyon taşıyıcıları infertilite ve tekrarlayan düşük riskiyle başvururlar.",
                "keyBullets": [
                    {"title": "Resiprokal Translokasyon", "desc": "Homolog olmayan iki kromozom arasında karşılıklı parça değişimidir.", "isKey": True},
                    {"title": "Kuadrivalan Yapısı", "desc": "Mayoz I'de homolog bölgelerin eşleşmesi için oluşan haç biçimli dörtlü komplekstir.", "isKey": True},
                    {"title": "Taşıyıcı Durumu", "desc": "Net genetik kayıp yoktur; taşıyıcı sağlıklıdır ancak üremede dengesiz gamet riski taşır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Resiprokal Translokasyonda Kuadrivalan ve Gamet Dağılım Zinciri",
                    [
                        "1. Homolog olmayan iki kromozom kırılır ve parçalarını karşılıklı değiş tokuş eder",
                        "2. Mayoz I zigoten/pakitende homolog dizilerin eşleşebilmesi için 4 kromozom haç şeklinde (kuadrivalan) dizilir",
                        "3. Anafaz I'de kromatitler kutuplara alternatif, bitişik-1 veya bitişik-2 modelleriyle çekilir",
                        "4. Ayrılma paternine bağlı olarak ya dengeli normal gametler ya da letal dengesiz gametler oluşur"
                    ]
                ),
                make_cloze(
                    "Mayoz I profazında iki normal ve iki transloke kromozomun homolog bölgelerini eşleştirmek için oluşturduğu dörtlü haç yapısına kuadrivalan denir.",
                    "kuadrivalan",
                    "Dörtlü mayotik kromozom yapısını anımsayınız"
                ),
                make_active_recall(
                    "Dengeli resiprokal translokasyon taşıyan bireyler klinik genetik merkezlerine en sık hangi şikayet ve öykü ile başvururlar?",
                    "Tekrarlayan spontan düşükler (habitüel abortus) ve açıklanamayan infertilite öyküsüyle başvururlar.",
                    "Üreme başarısızlığı ve fetal kayıplar"
                )
            ],
            "spotPearls": [
                "Resiprokal translokasyon homolog olmayan kromozomlar arası parça değişimidir.",
                "Mayoz I'de homolog eşleşme için kuadrivalan (dörtlü haç) yapısı kurulur.",
                "Taşıyıcılar fenotipik olarak normaldir ancak tekrarlayan düşük riski taşırlar."
            ]
        },

        # Slayt 22
        {
            "title": "Resiprokal Translokasyonlarda Mayotik Segregasyon Modelleri",
            "subtitle": "Alternatif, Bitişik-1 (Adjacent-1) ve Bitişik-2 Dağılımları",
            "badge": "Segregasyon Modelleri",
            "coreContent": {
                "text": "Kuadrivalan yapısındaki dört kromozomun mayoz I anafazında ikişerli olarak kutuplara çekilmesi 2:2 segregasyon modellerini doğurur. Bu modeller: Alternatif (Alternate), Bitişik-1 (Adjacent-1) ve Bitişik-2 (Adjacent-2) ayrılmalarıdır. Alternatif segregasyonda zıt kutuplardaki iki normal kromozom bir kutba, iki türev kromozom diğer kutba gider; oluşan gametler ya tamamen normal ya da ebeveyn gibi dengeli translokasyon taşır; bu ayrılma yaşayabilen sağlıklı bebekler üretir. Bitişik-1 segregasyonda homolog olmayan sentromerler aynı kutba çekilir; segmentler için parsiyel duplikasyon ve parsiyel delesyon oluşur; en sık görülen dengesiz canlı doğum nedenidir. Bitişik-2 segregasyonda ise homolog sentromerler aynı kutba çekilir; son derece ağır genetik dengesizlik doğurur ve neredeyse daima embriyonik letaldir. Nadir 3:1 segregasyonda ise kutuplara 3 ve 1 kromozom çekilerek 47 veya 45 kromozomlu ürünler oluşur.",
                "keyBullets": [
                    {"title": "Alternatif Ayrılma", "desc": "Normal veya dengeli gametler üretir; sağlıklı canlı doğum sağlayan tek modeldir.", "isKey": True},
                    {"title": "Bitişik-1 (Adjacent-1)", "desc": "Homolog olmayan sentromerler birlikte gider; dengesiz canlı doğumların ana kaynağıdır.", "isKey": True},
                    {"title": "Bitişik-2 (Adjacent-2)", "desc": "Homolog sentromerler birlikte gider; aşırı dengesizdir, erken letal seyreder.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Segregasyon Modeli", "Sentromer Dağılımı", "Gamet Yapısı", "Klinik Çıktı"],
                    [
                        [("Alternatif (Alternate)", False, ""), ("Zıt köşelerdeki kromozomlar birlikte", True, "Diyagonal kutup çekilmesi"), ("Normal veya Dengeli Taşıyıcı", False, ""), ("Sağlıklı canlı doğum (%100 yaşar)", False, "")],
                        [("Bitişik-1 (Adjacent-1)", False, ""), ("Farklı (homolog olmayan) sentromerler", True, "Yatay/dikey komşu çekilmesi"), ("Delesyon + Duplikasyon içerir", False, ""), ("Dengesiz gamet; anomalili canlı doğum", False, "")],
                        [("Bitişik-2 (Adjacent-2)", False, ""), ("Aynı (homolog) sentromerler birlikte", True, "Homolog komşu çekilmesi"), ("Ağır delesyon + trizomi etkisi", False, ""), ("Çok erken embriyonik letalite", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Resiprokal translokasyon taşıyıcısı bir bireyde kuadrivalan ayrılması sırasında sağlıklı, fenotipik olarak normal bir çocuğun doğabilmesi için hangi segregasyon modelinin gerçekleşmesi zorunludur?",
                    {
                        "A": "Bitişik-1 (Adjacent-1) segregasyonu",
                        "B": "Bitişik-2 (Adjacent-2) segregasyonu",
                        "C": "Alternatif (Alternate) segregasyon",
                        "D": "3:1 tersiyer segregasyon",
                        "E": "4:0 segregasyon"
                    },
                    "C",
                    {
                        "A": "Bitişik-1 delesyon ve duplikasyonlu dengesiz ürün verir.",
                        "B": "Bitişik-2 mutlak letal dengesiz ürün verir.",
                        "C": "Doğru cevap C'dir: Yalnızca alternatif segregasyon genetik dengesi tam olan (normal ya da dengeli) gametler üretir.",
                        "D": "3:1 anöploid gamet üretir.",
                        "E": "4:0 imkansız ve tamamen letaldir."
                    }
                ),
                make_active_recall(
                    "Resiprokal translokasyonlarda homolog sentromerlerin aynı kutba çekildiği ve neredeyse daima letaliteyle sonuçlanan 2:2 segregasyon modeli hangisidir?",
                    "Bitişik-2 (Adjacent-2) segregasyon modelidir.",
                    "Homolog sentromer komşu ayrılması"
                )
            ],
            "spotPearls": [
                "Alternatif segregasyon dengeli ve sağlıklı çocuklar doğurur.",
                "Bitişik-1 segregasyon anomalili canlı doğumların en sık kaynağıdır.",
                "Bitişik-2 segregasyonda homolog sentromerler birlikte gider ve neredeyse daima letaldir."
            ]
        },

        # Slayt 23
        {
            "title": "Robertsonian Translokasyonlar: Akrosentrik Kromozomların Sentromerik Füzyonu",
            "subtitle": "İnsan Türünde En Yaygın Yapısal Kromozom Anomalisi",
            "badge": "Robertsonian Mekanizması",
            "coreContent": {
                "text": "Robertsonian translokasyon (sentrik füzyon), insan popülasyonunda en sık rastlanan yapısal kromozom anomalisidir (yaklaşık 1/1000 sıklıkta). Bu anomali yalnızca akrosentrik kromozomlar (13, 14, 15, 21 ve 22) arasında gerçekleşir. İki akrosentrik kromozomun sentromerik veya perisentrik bölgesinde kırıklar oluşur; kısa kolları (p) koparak kaybolurken, uzun kolları (q) sentromer düzeyinde birleşerek tek bir büyük türev kromozom meydana getirir. Kaybedilen kısa kollarda yalnızca bol kopyalı ribozomal RNA (rRNA) genleri ve heterokromatin satellit dizileri bulunduğu için, bu kayıp taşıyıcı bireyde hiçbir klinik eksikliğe veya fenotipik belirtiye yol açmaz. Robertsonian translokasyon taşıyıcısı bir bireyin karyotipinde toplam 45 kromozom bulunur; ancak genetik içerik tam ve dengeli olduğu için taşıyıcı 'görünürde dengeli' ve tamamen sağlıklıdır.",
                "keyBullets": [
                    {"title": "En Yaygın Yapısal Anomali", "desc": "İnsanlarda en sık görülen yapısal bozukluktur; sıklığı ~1/1000'dir.", "isKey": True},
                    {"title": "Akrosentrik Spesifikliği", "desc": "Yalnızca 13, 14, 15, 21 ve 22 numaralı akrosentrik kromozomlar arasında gerçekleşir.", "isKey": True},
                    {"title": "Kromozom Sayısı", "desc": "Kısa kolların kaybı ve uzun kolların füzyonuyla taşıyıcıda 45 kromozom bulunur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Resiprokal vs Robertsonian Translokasyon",
                    "Resiprokal Translokasyon",
                    "Herhangi iki homolog olmayan kromozom arasında; toplam kromozom sayısı 46 olarak korunur; kuadrivalan kurar.",
                    "Robertsonian Translokasyon",
                    "Yalnızca akrosentrik kromozomlar (13,14,15,21,22) arasında; kısa kollar kaybolur, toplam kromozom sayısı 45'e düşer; trivalan kurar."
                ),
                make_cloze(
                    "Robertsonian translokasyon taşıyıcısı sağlıklı bir bireyin somatik hücrelerinde 45 kromozom bulunur.",
                    "45",
                    "Sentrik füzyon taşıyıcısının kromozom sayısını anımsayınız"
                ),
                make_active_recall(
                    "Robertsonian translokasyonda iki akrosentrik kromozomun kısa kolları kopup kaybolduğu halde taşıyıcı bireyin fenotipik olarak sağlıklı kalmasının nedeni nedir?",
                    "Kısa kollarda yalnızca çok kopyalı rRNA genleri ve satellit heterokromatin bulunduğu, kritik tek kopya gen içermediği için.",
                    "rRNA genlerinin yedekliliği ve heterokromatin kaybı"
                )
            ],
            "spotPearls": [
                "Robertsonian translokasyon insanlarda EN YAYGIN kromozom anomalisidir.",
                "Yalnızca akrosentrik kromozomlar arasında gerçekleşir (13, 14, 15, 21, 22).",
                "Taşıyıcı bireyler dengelidir ve 45 kromozoma sahiptir."
            ]
        },

        # Slayt 24
        {
            "title": "En Sık Robertsonian Translokasyonlar: rob(13;14) ve rob(14;21)",
            "subtitle": "Kromozomal Rekombinasyon Sıcak Noktaları ve Klinik Spektrum",
            "badge": "Translokasyon Tipleri",
            "coreContent": {
                "text": "Tüm Robertsonian translokasyonlar arasında görülme sıklığı açısından iki spesifik tip dramatik bir üstünlüğe sahiptir. Popülasyonda tek başına en sık rastlanan Robertsonian translokasyon rob(13;14) füzyonudur (tüm Robertsonian olgularının yaklaşık %75'ini oluşturur). Taşıyıcı karyotipi erkekte 45,XY,rob(13;14)(q10;q10), kadında 45,XX,rob(13;14)(q10;q10) şeklindedir. İkinci en sık tip ise rob(14;21) füzyonudur (olguların yaklaşık %10'u). rob(14;21) taşıyıcılığı klinik açıdan en büyük öneme sahip translokasyondur; çünkü 21. kromozomun uzun kolunu içerdiğinden, dengesiz segregasyon durumunda translokasyon tipi Down sendromlu (46,XX veya XY,rob(14;21),+21) çocukların doğmasına zemin hazırlar. Homolog akrosentrikler arasındaki translokasyonlar (örneğin rob(21;21)) ise son derece nadir olup dramatik üreme sonuçları doğurur.",
                "keyBullets": [
                    {"title": "En Sık Robertsonian", "desc": "rob(13;14) tüm Robertsonian translokasyonların yaklaşık %75'ini oluşturur.", "isKey": True},
                    {"title": "İkinci En Sık (Klinik Önem)", "desc": "rob(14;21) Down sendromlu çocuk doğurma riski nedeniyle en kritik olandır.", "isKey": True},
                    {"title": "Sitogenetik Kodlama", "desc": "Sentromer füzyon noktası q10;q10 olarak karyotipte belirtilir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Translokasyon Tipi", "Toplumdaki Payı", "Klinik / Üreme Önemi"],
                    [
                        [("rob(13;14)", False, ""), ("Tüm Robertsonian olgularının ~%75'i", True, "Tek başına en sık füzyon"), ("En sık tip; Patau sendromu riski düşüktür", False, "")],
                        [("rob(14;21)", False, ""), ("Olguların yaklaşık %10'u", True, "İkinci en sık füzyon"), ("Translokasyon tipi Down sendromunun ana kaynağıdır", False, "")],
                        [("rob(21;21)", False, ""), ("Oldukça nadir izokromozom benzeri", True, "Homolog füzyon"), ("Tüm canlı doğan çocukları istisnasız Down sendromlu olur", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "İnsan popülasyonunda en sık rastlanan spesifik Robertsonian translokasyon çifti aşağıdakilerden hangisidir?",
                    {
                        "A": "rob(14;21)",
                        "B": "rob(13;14)",
                        "C": "rob(15;21)",
                        "D": "rob(21;22)",
                        "E": "rob(13;15)"
                    },
                    "B",
                    {
                        "A": "rob(14;21) ikinci en sıktır.",
                        "B": "Doğru cevap B'dir: rob(13;14) tüm Robertsonian translokasyonların yaklaşık %75'ini oluşturarak en sık görülen tiptir.",
                        "C": "rob(15;21) çok daha nadirdir.",
                        "D": "rob(21;22) nadirdir.",
                        "E": "rob(13;15) nadirdir."
                    }
                ),
                make_active_recall(
                    "Homolog iki 21. kromozomun füzyonuyla oluşan rob(21;21) taşıyıcısı bir ebeveynin canlı doğacak çocuklarının Down sendromlu olma riski teorik ve pratik olarak yüzde kaçtır?",
                    "Yüzde yüzdür (%100); çünkü gamet ya çift 21 taşır (Down) ya da hiç 21 taşımaz (letal monozomi 21).",
                    "Homolog rob(21;21) mutlak Down riski"
                )
            ],
            "spotPearls": [
                "En sık Robertsonian translokasyon rob(13;14)'tür (~%75).",
                "Klinik olarak en önemli Robertsonian translokasyon rob(14;21)'dir (Down sendromu riski).",
                "rob(21;21) taşıyıcısının canlı doğan tüm çocukları istisnasız Down sendromludur (%100 risk)."
            ]
        },

        # Slayt 25
        {
            "title": "Robertsonian Taşıyıcılarda Gametogenez ve Trivalan Segregasyonu",
            "subtitle": "Üçlü Kromozom Kompleksi ve Teorik Gamet İhtimalleri",
            "badge": "Trivalan Ayrılması",
            "coreContent": {
                "text": "Robertsonian translokasyon taşıyıcısı bireylerde (örneğin 45,XX,rob(14;21)), mayoz I profazında homolog bölgelerin eşleşmesi için bir adet transloke kromozom ve iki adet normal serbest kromozom (normal 14 ve normal 21) bir araya gelerek 'trivalan' adı verilen üçlü bir kompleks oluşturur. Bu trivalan kompleksi anafaz I'de kutuplara çekilirken teorik olarak 6 farklı gamet tipi üretir: (1) Normal gamet (14 ve 21 taşır; normal çocuk), (2) Dengeli gamet (rob(14;21) taşır; taşıyıcı çocuk), (3) Trizomi 21 gameti (rob(14;21) ve normal 21 taşır; translokasyon Down), (4) Monozomi 21 gameti (yalnız 14 taşır; embriyonik letal), (5) Trizomi 14 gameti (rob(14;21) ve normal 14 taşır; embriyonik letal), (6) Monozomi 14 gameti (yalniz 21 taşır; embriyonik letal). Teorik olarak 6 ihtimalden 3'ü letaldir; kalan 3 canlı ihtimal arasında teorik Down sendromu riski 1/3 (%33) olarak hesaplansa da gerçek ampirik riskler çok daha düşüktür.",
                "keyBullets": [
                    {"title": "Trivalan Kompleksi", "desc": "Transsloke kromozom ile iki normal akrosentriğin mayozda oluşturduğu üçlü yapıdır.", "isKey": True},
                    {"title": "Teorik Gamet Tipleri", "desc": "6 farklı gamet oluşur; bunlardan 3'ü (monozomi 21, monozomi 14, trizomi 14) letaldir.", "isKey": True},
                    {"title": "Teorik vs Ampirik Risk", "desc": "Teorik canlı doğum riski 1/3 (%33) iken biyolojik seleksiyon nedeniyle ampirik risk daha düşüktür.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Gamet Tipi", "Kromozom İçeriği", "Döllenme Sonucu Zigot", "Embriyonik Akıbet"],
                    [
                        [("Normal Gamet", False, ""), ("Normal 14 + Normal 21", False, ""), ("46,XX veya 46,XY", False, ""), ("Normal sağlıklı birey", False, "")],
                        [("Dengeli Gamet", False, ""), ("rob(14;21) türev kromozomu", False, ""), ("45,XX veya XY,rob(14;21)", True, "Taşıyıcı 45 kromozom"), ("Sağlıklı dengeli taşıyıcı", False, "")],
                        [("Trizomik Gamet", False, ""), ("rob(14;21) + Normal 21", True, "Fazladan 21 taşıyan gamet"), ("46,XX veya XY,rob(14;21),+21", True, "Translokasyon Down karyotipi"), ("Canlı doğar: Translokasyon Down", False, "")],
                        [("Monozomik Gamet", False, ""), ("Sadece normal 14 (21 yok)", True, "21 eksik nullizomik"), ("45,XX veya XY,rob(14;21),-21", False, ""), ("Erken embriyonik letalite", False, "")],
                        [("Trizomi 14 Gameti", False, ""), ("rob(14;21) + Normal 14", False, ""), ("46,XX veya XY,rob(14;21),+14", False, ""), ("Erken embriyonik letalite", False, "")],
                        [("Monozomi 14 Gameti", False, ""), ("Sadece normal 21 (14 yok)", False, ""), ("45,XX veya XY,rob(14;21),-14", False, ""), ("Erken embriyonik letalite", False, "")]
                    ]
                ),
                make_active_recall(
                    "rob(14;21) taşıyıcısı bir ebeveynin mayoz bölünmesinde trivalan segregasyonu sonucu teorik olarak ortaya çıkan 6 gamet tipinden kaç tanesi mutlak letaliteye yol açar?",
                    "3 tanesi mutlak letaldir (Monozomi 21, Trizomi 14 ve Monozomi 14).",
                    "Letal trivalan ürünleri sayısı"
                ),
                make_cloze(
                    "rob(14;21) taşıyıcısında mayoz sırasında bir transloke ve iki serbest kromozomun kurduğu üçlü komplekse trivalan adı verilir.",
                    "trivalan",
                    "Üçlü mayotik yapı terimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Robertsonian mayozunda trivalan (üçlü kromozom) kompleksi oluşur.",
                "Oluşan 6 teorik gametten 3'ü mutlak letaldir (Trizomi 14, Monozomi 14, Monozomi 21).",
                "Canlı doğabilen tek anöploid ürün Translokasyon tipi Down sendromudur."
            ]
        },

        # Slayt 26
        {
            "title": "Translokasyon Taşıyıcılarında Ebeveyn Cinsiyetine Göre Risk Farklılıkları",
            "subtitle": "Anne Taşıyıcılığı (%15) ve Baba Taşıyıcılığı (%4-5) Dinamiği",
            "badge": "Ebeveyn Riski",
            "coreContent": {
                "text": "Translokasyon taşıyıcısı ebeveynlerde anomalili çocuk sahibi olma riski, taşıyıcı ebeveynin cinsiyetine göre belirgin farklılık sergiler. Bu durum özellikle rob(14;21) taşıyıcılarında klinik genetik danışmanlığın en temel kuralıdır. Eğer rob(14;21) taşıyıcısı anne ise, translokasyon tipi Down sendromlu çocuk doğurma riski yaklaşık %10-15 (literatür ve ders notlarında %15) civarındadır. Buna karşın rob(14;21) taşıyıcısı baba ise bu risk sadece %4-5 düzeyindedir. Baba taşıyıcılığında riskin bu kadar belirgin derecede düşük olmasının biyolojik nedeni 'sperm seleksiyonu'dur; dengesiz ve ekstra kromozom taşıyan spermlerin motilitesi düşüktür ve fertilizasyon yarışında normal veya dengeli spermlere karşı selektif olarak elenirler. Oogenezde ise böyle bir motilite filtresi bulunmadığı için anne taşıyıcılığında risk yaklaşık 3 kat daha yüksektir.",
                "keyBullets": [
                    {"title": "Anne Taşıyıcılığı Riski", "desc": "rob(14;21) taşıyıcısı annede Down sendromlu çocuk riski yaklaşık %15'tir.", "isKey": True},
                    {"title": "Baba Taşıyıcılığı Riski", "desc": "rob(14;21) taşıyıcısı babada Down sendromlu çocuk riski yalnızca %4-5'tir.", "isKey": True},
                    {"title": "Sperm Seleksiyonu Mekanizması", "desc": "Anormal spermlerin motilite yetersizliği babadaki ampirik riski düşüren temel nedendir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "rob(14;21) Taşıyıcılığında Anne vs Baba Riski",
                    "Anne Taşıyıcı İse",
                    "Down sendromlu çocuk riski yaklaşık %15'tir; oositlerde fonksiyonel seleksiyon filtresi yoktur.",
                    "Baba Taşıyıcı İse",
                    "Down sendromlu çocuk riski yalnızca %4-5'tir; disomik spermler motilite ve fertilizasyon yarışında elenir."
                ),
                make_micro_quiz(
                    "Dengeli Robertsonian translokasyonu [rob(14;21)] taşıyıcısı olduğu bilinen bir kadının gebe kalması durumunda, canlı doğacak çocuğunun translokasyon tipi Down sendromlu olma ampirik riski yaklaşık yüzde kaçtır?",
                    {
                        "A": "Yaklaşık %1",
                        "B": "Yaklaşık %4-5",
                        "C": "Yaklaşık %15",
                        "D": "Yaklaşık %50",
                        "E": "Yüzde 100"
                    },
                    "C",
                    {
                        "A": "%1 klasik trizomi 21 tekrarlama riskidir.",
                        "B": "%4-5 baba taşıyıcı olduğundaki ampirik risktir.",
                        "C": "Doğru cevap C'dir: rob(14;21) taşıyıcısı kadınlarda Down sendromlu çocuk riski yaklaşık %15'tir.",
                        "D": "%50 aşırı yüksektir.",
                        "E": "%100 rob(21;21) riskidir."
                    }
                ),
                make_cloze(
                    "rob(14;21) dengeli taşıyıcısı bir babada translokasyon Down sendromlu çocuk doğma riski sperm seleksiyonu nedeniyle yaklaşık %4-5 seviyesine iner.",
                    "%4-5",
                    "Baba taşıyıcılık risk yüzdesini anımsayınız"
                )
            ],
            "spotPearls": [
                "rob(14;21) taşıyıcısı ANNE ise Down riski %15'tir.",
                "rob(14;21) taşıyıcısı BABA ise Down riski %4-5'tir.",
                "Babadaki risk düşüklüğünün nedeni dengesiz spermlerin motilite yarışında elenmesidir."
            ]
        },

        # Slayt 27
        {
            "title": "Tekrarlayan Fetal Kayıplar ve İnfertilitede Sitogenetik Tarama",
            "subtitle": "Habitüel Abortus Etiyolojisinde Dengeli Ebeveyn Taşıyıcılığı",
            "badge": "İnfertilite ve Düşükler",
            "coreContent": {
                "text": "Tekrarlayan gebelik kaybı (habitüel abortus; ardışık iki veya daha fazla spontan düşük), üreme çağındaki çiftlerin yaklaşık %2-5'ini etkileyen karmaşık bir klinik tablodur. Bu çiftlerin yaklaşık %3-5'inde ebeveynlerden birinde dengeli bir kromozomal anomali (en sık resiprokal translokasyon, ikinci sırada Robertsonian translokasyon veya perisentrik inversiyon) saptanır. Taşıyıcı ebeveynde fenotipik bulgu olmamasına karşın, her gebelikte mayotik segregasyon kusurları nedeniyle oluşan ağır dengesiz gametler embriyonun organogenez evresine ulaşamadan düşükle sonuçlanmasına yol açar. Bu nedenle tekrarlayan düşük veya açıklanamayan primer infertilite öyküsü olan her çifte kanda periferik lenfosit kültürü ile rutin ebeveyn karyotip analizi yapılması zorunlu bir kılavuz önerisidir. Taşıyıcılık saptanan çiftlere Preimplantasyon Genetik Tanı (PGT-SR) seçeneği sunulur.",
                "keyBullets": [
                    {"title": "Tekrarlayan Düşüklerde Sıklık", "desc": "Habitüel abortuslu çiftlerin %3-5'inde ebeveynlerden birinde dengeli anomali bulunur.", "isKey": True},
                    {"title": "En Sık Anomali", "desc": "Resiprokal translokasyonlar düşük öykülü çiftlerde en sık rastlanan anomalidir.", "isKey": True},
                    {"title": "Klinik Yaklaşım", "desc": "İki veya daha fazla düşüğü olan her çifte periferik karyotip analizi yapılmalıdır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_branching_logic(
                    "Ardışık 3 kez 8-10. gebelik haftalarında spontan düşük yaşayan 28 yaşında bir kadın ve 30 yaşında eşi jinekoloji polikliniğine başvuruyor. Çiftin anatomik ve hormonal incelemeleri normal bulunuyor. Bir sonraki en uygun tanısal ve yönetimsel adım ne olmalıdır?",
                    [
                        {"text": "Her iki eşe de periferik kandan sitogenetik karyotip analizi yapılmalı; dengeli translokasyon saptanırsa tüp bebek ve PGT-SR (yapısal yeniden düzenlenme PGT) planlanmalıdır", "isCorrect": True, "feedback": "Mükemmel klinik karar! Tekrarlayan düşüklerde eşlerin karyotipi taranmalı ve dengeli anomali saptanırsa embriyolara PGT-SR uygulanmalıdır."},
                        {"text": "Hiçbir tetkike gerek yoktur, dördüncü gebelik hemen denenmeli ve sadece yüksek doz progesteron başlanmalıdır", "isCorrect": False, "feedback": "Kromozomal etiyoloji aydınlatılmadan ampirik tedavi tekrarlayan düşüklere yol açar."},
                        {"text": "Kadına hemen histerektomi yapılmalıdır", "isCorrect": False, "feedback": "Tamamen tıbbi endikasyon dışıdır."}
                    ]
                ),
                make_cloze(
                    "Tekrarlayan düşük öyküsü olan çiftlerin yaklaşık %3-5 kadarında ebeveynlerden birinde dengeli yapısal kromozom anomalisi saptanır.",
                    "%3-5",
                    "Düşüklerde ebeveyn anomali sıklığı yüzdesini düşününüz"
                ),
                make_active_recall(
                    "Dengeli translokasyon taşıyıcısı olduğu saptanan ve tekrarlayan düşükler yaşayan bir çifte sağlıklı bir gebelik elde edebilmeleri için önerilen en gelişmiş üreme teknolojisi nedir?",
                    "Preimplantasyon Genetik Tanı - Yapısal Yeniden Düzenlenmeler (PGT-SR) eşliğinde IVF yöntemidir.",
                    "Embriyo düzeyinde genetik ayıklama"
                )
            ],
            "spotPearls": [
                "Tekrarlayan spontan düşük yapan çiftlerin %3-5'inde ebeveyn dengeli translokasyon taşır.",
                "En sık saptanan ebeveyn anomalisi dengeli resiprokal translokasyondur.",
                "Tedavide dengeli embriyoların seçilmesini sağlayan PGT-SR yöntemi kullanılır."
            ]
        },

        # Slayt 28
        {
            "title": "Kanser Sitogenetiğinde Somatik Translokasyonlar",
            "subtitle": "Onkojenik Füzyon Genleri ve Kimerik Protein Oluşumu",
            "badge": "Onkogenetik Translokasyonlar",
            "coreContent": {
                "text": "Translokasyonlar yalnızca germline hücrelerinde kalıtsal olarak görülmez; somatik hücrelerde sonradan kazanılan edinsel translokasyonlar birçok hematolojik malignitenin ve sarkomun temel sürücü (driver) mutasyonudur. Somatik translokasyonlar iki ana onkojenik mekanizmayla tümör gelişimini tetikler: (1) Bir onkojenin güçlü bir immünglobülin veya TCR promotörünün kontrolü altına girmesiyle aşırı ekspresyonu; örneğin Burkitt lenfomada t(8;14)(q24;q32) translokasyonu sonucu MYC onkojeninin Ig ağır zincir lokusunun yanına gelerek aşırı üretilmesi. (2) İki farklı genin kırık noktalarında birleşerek kimerik bir onkoprotein üretmesi; en klasik örnek Kronik Miyelositer Lösemideki (KML) Philadelphia kromozomudur [t(9;22)(q34;q11.2)]. Bu translokasyonda 9. kromozomdaki ABL1 tirozin kinaz geni ile 22. kromozomdaki BCR geni birleşerek kontrolsüz kinaz aktivitesine sahip BCR-ABL1 füzyon proteinini üretir.",
                "keyBullets": [
                    {"title": "Philadelphia Kromozomu", "desc": "t(9;22)(q34;q11.2) BCR-ABL1 kinaz füzyonudur; KML'nin patognomonik belirtecidir.", "isKey": True},
                    {"title": "Burkitt Lenfoma", "desc": "t(8;14)(q24;q32) MYC onkojeninin IgH promotörü kontrolüne girip aşırı artmasıdır.", "isKey": True},
                    {"title": "Kimerik Protein Hedefi", "desc": "Füzyon kinazlar hedefe yönelik tedavilerin (örneğin İmatinib) primer hedefidir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Malignite Tipi", "Spesifik Translokasyon", "Oluşan Füzyon / Mekanizma", "Klinik Önemi"],
                    [
                        [("Kronik Miyelositer Lösemi (KML)", False, ""), ("t(9;22)(q34;q11.2)", True, "Philadelphia kromozomu translokasyonu"), ("BCR-ABL1 füzyon kinazı", False, ""), ("İmatinib (tirozin kinaz inhibitörü) hedefidir", False, "")],
                        [("Burkitt Lenfoma", False, ""), ("t(8;14)(q24;q32)", True, "MYC-IgH translokasyonu"), ("MYC onkojeninin aşırı transkripsiyonu", False, ""), ("Yıldızlı gökyüzü manzaralı agresif B lenfoma", False, "")],
                        [("Foliküler Lenfoma", False, ""), ("t(14;18)(q32;q21)", False, ""), ("BCL2 aşırı ekspresyonu (apoptoz blokajı)", False, ""), ("İndolent B hücreli lenfoma prototipi", False, "")],
                        [("Ewing Sarkomu", False, ""), ("t(11;22)(q24;q12)", False, ""), ("EWS-FLI1 aberan transkripsiyon faktörü", False, ""), ("Küçük yuvarlak mavi hücreli kemik tümörü", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Kronik miyelositer lösemi (KML) patogenezinde 9 ve 22 numaralı kromozomlar arasındaki resiprokal translokasyon [t(9;22)] sonucu 22. kromozomun kısalmasıyla oluşan aberan kromozoma ne ad verilir?",
                    {
                        "A": "Philadelphia kromozomu",
                        "B": "Robertsonian kromozomu",
                        "C": "Ring kromozom",
                        "D": "İzokromozom 22q",
                        "E": "Marker kromozom"
                    },
                    "A",
                    {
                        "A": "Doğru cevap A'dır: t(9;22) sonucu türev 22 kromozomuna Philadelphia kromozomu denir ve BCR-ABL1 füzyonunu taşır.",
                        "B": "Robertsonian akrosentrik füzyonudur.",
                        "C": "Ring halka biçimlidir.",
                        "D": "İzokromozom sentromer transvers bölünmesidir.",
                        "E": "Marker tanımlanamayan küçük parçadır."
                    }
                ),
                make_active_recall(
                    "Burkitt lenfomada t(8;14) translokasyonu ile 14. kromozomdaki immünglobülin ağır zincir promotörünün yanına taşınarak aşırı transkribe edilen onkojen hangisidir?",
                    "c-MYC (MYC) transkripsiyon faktörü onkojenidir.",
                    "8q24 yerleşimli nükleer onkojen"
                )
            ],
            "spotPearls": [
                "KML'deki t(9;22) Philadelphia kromozomu BCR-ABL1 kinaz füzyonunu kodlar.",
                "Burkitt lenfomadaki t(8;14) MYC onkojenini immünglobülin ağır zincir lokusunun yanına taşır.",
                "Foliküler lenfomadaki t(14;18) anti-apoptotik BCL2 geninin aşırı ekspresyonuna yol açar."
            ]
        },

        # Slayt 29 (CHECKPOINT 3)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Translokasyon Biyolojisi, Segregasyon ve Robertsonian Mekanizma",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 3",
            "coreContent": {
                "text": "Bu bölümde resiprokal ve Robertsonian translokasyonların biyolojik ve klinik özelliklerini entegre ettik. Resiprokal translokasyonlar homolog olmayan kromozomlar arası parça değişimidir; mayozda kuadrivalan yapısı kurar; alternatif segregasyon normal ve dengeli sağlıklı bebekler üretirken, bitişik-1 canlı doğabilen anomalili bebeklere, bitişik-2 ise mutlak erken letaliteye yol açar. Robertsonian translokasyon yalnızca akrosentrikler (13, 14, 15, 21, 22) arasında sentrik füzyonla oluşur; taşıyıcıda 45 kromozom bulunur ve sağlıklıdır. Popülasyonda en sık tip rob(13;14) (%75), klinik olarak en riskli tip rob(14;21)'dir (%10). rob(14;21) taşıyıcısı anne olduğunda Down riski %15, baba olduğunda sperm seleksiyonu nedeniyle %4-5'tir. Homolog rob(21;21) taşıyıcısının canlı doğan çocuklarında Down riski %100'dür. Tekrarlayan düşük yapan çiftlerin %3-5'inde dengeli translokasyon saptanır. Somatik translokasyonlar kanserde kimerik onkoproteinler üretir (KML'de t(9;22) Philadelphia).",
                "keyBullets": [
                    {"title": "Resiprokal Ayrılma", "desc": "Alternatif (sağlıklı), Bitişik-1 (dengesiz canlı), Bitişik-2 (mutlak letal) segregasyon modelleri.", "isKey": True},
                    {"title": "Robertsonian Özellikleri", "desc": "Yalnızca akrosentrikler; en sık rob(13;14); Down riski rob(14;21)'de anne %15, baba %4-5.", "isKey": True},
                    {"title": "Klinik Önem", "desc": "Tekrarlayan düşüklerde %3-5 ebeveyn translokasyonu; kanserde t(9;22) ve t(8;14).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Translokasyon Olgusu", "Kromozom Sayısı ve Yapı", "Üreme / Klinik Yansıma"],
                    [
                        [("Dengeli Resiprokal Taşıyıcı", False, ""), ("46 kromozom; 2 türev kromozom", True, "Materyal korunumlu 46 kromozom"), ("Tekrarlayan düşükler ve infertilite", False, "")],
                        [("rob(13;14) Taşıyıcısı", False, ""), ("45 kromozom; tek sentrik füzyon", True, "En sık akrosentrik füzyon"), ("En sık tip; fenotip tamamen normal", False, "")],
                        [("rob(14;21) Anne Taşıyıcılığı", False, ""), ("45 kromozom; der(14;21)", True, "Maternal füzyon taşıyıcılığı"), ("Çocukta Down riski yaklaşık %15", False, "")],
                        [("rob(14;21) Baba Taşıyıcılığı", False, ""), ("45 kromozom; der(14;21)", True, "Paternal füzyon taşıyıcılığı"), ("Çocukta Down riski yalnızca %4-5", False, "")],
                        [("rob(21;21) Homolog Taşıyıcı", False, ""), ("45 kromozom; izokromozom 21q", True, "Homolog 21 füzyonu"), ("Çocuklarda Down riski %100", False, "")]
                    ]
                ),
                make_cloze(
                    "Robertsonian translokasyon rob(14;21) taşıyıcısı bir annenin çocuğunda Down sendromu görülme ampirik riski yaklaşık %15 düzeyindedir.",
                    "%15",
                    "Maternal taşıyıcılık Down risk yüzdesini anımsayınız"
                ),
                make_active_recall(
                    "rob(14;21) taşıyıcısı olan bir erkekte Down sendromlu çocuk doğma riskinin (%4-5) anneye göre (%15) belirgin düşük olmasının temel nedeni nedir?",
                    "Anormal ve ekstra kromozom taşıyan spermlerin motilite yarışında elenmesi (sperm seleksiyonu) mekanizmasıdır.",
                    "Spermatozoa kalite kontrol filtresi"
                )
            ],
            "spotPearls": [
                "En yaygın kromozom anomalisi Robertsonian translokasyondur; taşıyıcı 45 kromozomludur.",
                "rob(14;21) Down riski: Anne taşıyıcı ise %15, baba taşıyıcı ise %4-5.",
                "rob(21;21) taşıyıcısının canlı doğan tüm çocukları istisnasız Down sendromludur (%100)."
            ]
        },

        # Slayt 30
        {
            "title": "İnsersiyonel Translokasyonlar ve Kompleks Kromozomal Düzenlenmeler",
            "subtitle": "Üç Kırıklı Segment Transferleri ve CCR Dinamikleri",
            "badge": "Kompleks Düzenlenmeler",
            "coreContent": {
                "text": "İnsersiyonel translokasyonlar, bir kromozomdan kopan bir segmentin karşılıklı parça değişimi olmaksızın başka bir kromozomun içine (veya aynı kromozomun farklı bir bölgesine) girmesiyle oluşan nadir ve karmaşık yapısal anomalilerdir. Bir insersiyonun gerçekleşebilmesi için en az üç ayrı DNA kırığı gereklidir: verici kromozomda segmenti çıkarmak için iki kırık, alıcı kromozomda ise segmenti araya almak için bir kırık oluşmalıdır. İnsersiyon taşıyıcıları toplam genetik materyal korunduğunda dengelidir; ancak mayoz bölünmede bu segmentlerin homolog eşleşmesi son derece zorlu bir konfigürasyon gerektirir. Mayotik segregasyon sonucunda gametlerin yaklaşık %50'si insersiyona uğrayan bölge için ya tam duplikasyon ya da tam delesyon içerir. Bu nedenle insersiyon taşıyıcılarında anomalili çocuk doğurma veya düşük riski çok yüksektir; bu çiftlere kesinlikle prenatal tanı veya PGT önerilmelidir.",
                "keyBullets": [
                    {"title": "İnsersiyon Mekanizması", "desc": "En az üç kırık gerektirir; kopan parça başka kromozomun içine yerleşir.", "isKey": True},
                    {"title": "Yüksek Dengesiz Gamet Riski", "desc": "Segregasyon sonucu gametlerin yaklaşık yarısı delesyon veya duplikasyon taşır.", "isKey": True},
                    {"title": "Klinik Yönetim", "desc": "Dengesiz ürün riski çok yüksek olduğundan kesin prenatal tanı endikasyonudur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "İnsersiyonel Translokasyon ve Dengesiz Gamet Zinciri",
                    [
                        "1. Verici kromozomda 2 kırıkla bir interstisyel segment serbest kalır",
                        "2. Alıcı kromozomda tek kırık oluşur ve serbest segment bu kırık noktasına integre olur",
                        "3. Taşıyıcı dengelidir ancak mayozda kromatitler birbirinden bağımsız ayrılır",
                        "4. Gamet ya fazladan segment alarak duplikasyonlu ya da segmentsiz kalarak delesyonlu zigot doğurur"
                    ]
                ),
                make_cloze(
                    "Bir insersiyonel translokasyonun meydana gelebilmesi için genomda en az 3 ayrı kırık oluşması zorunludur.",
                    "3",
                    "İnsersiyon için minimum kırık sayısını düşününüz"
                ),
                make_active_recall(
                    "İnsersiyonel translokasyon taşıyıcısı bir ebeveynin çocuklarında neden resiprokal translokasyonlara göre çok daha yüksek oranda (%50'ye varan) delesyon/duplikasyon riski bulunur?",
                    "Çünkü tek yönlü transfer edilen segment mayozda normal homologundan bağımsız segrege olarak gametlerin yarısında eksik veya fazla kalır.",
                    "Bağımsız segregasyon ve kompanse edilmemiş segment"
                )
            ],
            "spotPearls": [
                "İnsersiyonel translokasyon için en az 3 kromozomal kırık gereklidir.",
                "Dengesiz gamet riski son derece yüksektir (yaklaşık %50 delesyon/duplikasyon).",
                "İnsersiyon taşıyıcılarında gebelikte prenatal tanı (KVS/Amniyosentez) zorunludur."
            ]
        }
    ]
