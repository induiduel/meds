"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 6 (Slayt 51 - 60)
Konu: Yapısal Delesyon Sendromları, Cri du Chat, Wolf-Hirschhorn, Mikrodelesyonlar (DiGeorge, Williams) ve PMP22
Checkpoint: Slayt 59 ([TEKRAR SAYFASI - CHECKPOINT 6])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_6_slides():
    return [
        # Slayt 51
        {
            "title": "Klasik Otozomal Delesyon Sendromlarına Genel Bakış",
            "subtitle": "Kromozom Kol Kayıpları, Parsiyel Monozomiler ve Fenotip",
            "badge": "Delesyon Sendromları",
            "coreContent": {
                "text": "Otozomal delesyon sendromları, bir otozomun kısa veya uzun kolundaki spesifik bir segmentin kalıcı olarak kaybı (parsiyel monozomi) sonucunda ortaya çıkan dismorfik tabloları kapsar. Tam otozomal monozomiler insanlarda mutlak letal olduğundan, delesyonlar embriyonun hayatta kalabildiği parsiyel monozomik pencereleri temsil eder. Delesyon sendromları sitogenetik olarak iki büyük grupta toplanır: Klasik sitogenetik delesyonlar (G-bantlama karyotipinde ışık mikroskobuyla doğrudan görülebilen >4-5 Mb kayıplar; en tipik örnekleri Cri du chat ve Wolf-Hirschhorn sendromlarıdır) ve Mikrodelesyon sendromları (ancak FISH ve Kromozomal Mikroarray ile saptanabilen <3-5 Mb submikroskobik kayıplar; DiGeorge, Williams, Smith-Magenis). Delesyon sendromlarında fenotipik ağırlık, kaybedilen segmentin büyüklüğüne ve o bölgede yer alan haploinsüfisyent genlerin kritik gelişimsel rollerine doğrudan bağlıdır.",
                "keyBullets": [
                    {"title": "Parsiyel Monozomi Prensibi", "desc": "Tam monozomiler letalken delesyonlar yaşayabilen parsiyel monozomilerdir.", "isKey": True},
                    {"title": "Klasik vs Mikrodelesyon", "desc": "Klasik olanlar (Cri du chat, 4p-) karyotipte görülür; mikrodelesyonlar FISH/CMA gerektirir.", "isKey": True},
                    {"title": "Haploinsüfisyens Temeli", "desc": "Fenotip, bölgedeki dozaja duyarlı genlerin tek kopyaya düşmesiyle şekillenir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Klasik Delesyon vs Mikrodelesyon Ayrımı",
                    "Klasik Sitogenetik Delesyonlar",
                    ">5 Mb büyüklüğünde parça kaybı; standart G-bantlama karyotip analiziyle ışık mikroskobunda doğrudan tanınır (ör. Cri du chat 5p-, Wolf-Hirschhorn 4p-).",
                    "Mikrodelesyon Sendromları",
                    "<3-5 Mb submikroskobik kayıplar; standart karyotipte normal görünür, tanıda FISH veya Kromozomal Mikroarray (CMA) zorunludur (ör. 22q11.2, 7q11.23)."
                ),
                make_cloze(
                    "Işık mikroskobunda klasik G-bantlama ile görülemeyen submikroskobik gen kayıplarına mikrodelesyon sendromları adı verilir.",
                    "mikrodelesyon",
                    "Submikroskobik delesyon terimini anımsayınız"
                ),
                make_active_recall(
                    "Standart ışık mikroskobik karyotip analizinin kromozomal delesyonları yakalama çözünürlük sınırı yaklaşık kaç milyon baz çiftidir (Mb)?",
                    "Yaklaşık 4-5 milyon baz çifti (Mb) düzeyindedir.",
                    "G-bantlama çözünürlük eşiği"
                )
            ],
            "spotPearls": [
                "Delesyonlar parsiyel monozomidir ve haploinsüfisyensle klinik verir.",
                "Klasik delesyonlar (5p-, 4p-) karyotipte görülür.",
                "Mikrodelesyonlar (22q11, 7q11, 15q11) ancak FISH veya CMA ile saptanır."
            ]
        },

        # Slayt 52
        {
            "title": "Cri du Chat (Kedi Ağlaması) Sendromu: del(5p15) Sitogenetiği",
            "subtitle": "5. Kromozom Kısa Kol Delesyonunun Moleküler Anatomisi",
            "badge": "Cri du Chat Sendromu",
            "coreContent": {
                "text": "Cri du chat (Kedi Ağlaması) sendromu, 5. kromozomun kısa kolunun (p) terminal veya interstisyel delesyonu sonucu ortaya çıkan klasik bir yapısal kromozom anomalisidir [46,XX veya XY,del(5)(p15.2)]. Canlı doğumlardaki görülme sıklığı yaklaşık 1/20.000 ila 1/50.000 arasındadır. Olguların yaklaşık %85'inde delesyon de novo olarak (çoğunlukla paternal spermatogenez sırasında tek kırıklı terminal kayıp şeklinde) gelişir; olguların yaklaşık %10-15'inde ise ebeveynlerden birinde dengeli resiprokal translokasyon veya perisentrik inversiyon mevcuttur. Sitogenetik haritalama çalışmaları, sendroma adını veren karakteristik larinks hipoplazisi ve kedi miyavlaması benzeri tiz ağlama sesinin 5p15.3 kritik bölgesindeki gen kaybına bağlı olduğunu; zihinsel gerilik, mikrosefali ve dismorfik yüz bulgularının ise komşu 5p15.2 bölgesinin delesyonundan kaynaklandığını göstermiştir.",
                "keyBullets": [
                    {"title": "Sitogenetik Kod", "desc": "5. kromozom kısa kol delesyonudur: del(5)(p15.2) veya del(5p).", "isKey": True},
                    {"title": "Kritik Bölgeler", "desc": "Kedi ağlaması sesi 5p15.3 bölgesine, dismorfik özellikler 5p15.2 bölgesine aittir.", "isKey": True},
                    {"title": "Etiyoloji", "desc": "%85 de novo (çoğu paternal), %10-15 dengeli ebeveyn translokasyonu kaynaklıdır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kromozomal Kritik Bölge", "İçerdiği Fonksiyon / Fenotip", "Sorumlu Olduğu Klinik Bulgu"],
                    [
                        [("5p15.3 Bölgesi", False, ""), ("Larinks kıkırdak ve sinir gelişimi", True, "Ağlama bölgesi"), ("Karakteristik kedi miyavlaması benzeri tiz ağlama"), ],
                        [("5p15.2 Bölgesi", False, ""), ("Serebral ve kraniyofasiyal morfogenez", True, "Klinik bölge"), ("Zihinsel yetersizlik, mikrosefali, dismorfik yüz"), ],
                        [("5p14 ve Proksimal Bölge", False, ""), ("Kalp ve diğer visseral organ gelişimi", False, ""), ("Geniş delesyonlarda ağır konjenital kalp defektleri"), ]
                    ]
                ),
                make_micro_quiz(
                    "Cri du chat sendromuna yol açan 5p delesyonunda, sendroma adını veren tiz kedi ağlaması benzeri fonasyon kusurundan sorumlu olan spesifik kromozomal bant hangisidir?",
                    {
                        "A": "5p15.3",
                        "B": "5p15.2",
                        "C": "5q31",
                        "D": "5q11",
                        "E": "5p12"
                    },
                    "A",
                    {
                        "A": "Doğru cevap A'dır: Kedi ağlaması sesi 5p15.3 kritik bölgesinin kaybıyla ilişkilidir (5p15.2 ise diğer klinik özellikleri belirler).",
                        "B": "5p15.2 dismorfik yüz ve mental retardasyon bölgesidir.",
                        "C": "5q uzun koldur.",
                        "D": "5q uzun koldur.",
                        "E": "5p12 proksimal bölgedir."
                    }
                ),
                make_cloze(
                    "Cri du chat sendromunda kedi miyavlaması benzeri ağlamadan 5p15.3 bandı sorumlu iken, dismorfik klinik tablodan 5p15.2 bandı sorumludur.",
                    "5p15.2",
                    "Dismorfik özellikler kritik bant numarasını anımsayınız"
                )
            ],
            "spotPearls": [
                "Cri du chat sendromu 5p delesyonudur [del(5p15)].",
                "Ağlama sesi 5p15.3; dismorfik stigmalar 5p15.2 delesyonu ile ortaya çıkar.",
                "Olguların %85'i de novo, %15'i ebeveyn translokasyonu kökenlidir."
            ]
        },

        # Slayt 53
        {
            "title": "Cri du Chat Sendromunda Larinks Hipoplazisi ve Karakteristik Ağlama",
            "subtitle": "Kedi Miyavlamasını Andıran Akustik İmza ve Yaşla Evrimi",
            "badge": "Kedi Ağlaması İmzası",
            "coreContent": {
                "text": "Cri du chat sendromlu yenidoğanların en patognomonik fiziksel bulgusu, adını Fransızca 'kedi ağlaması' teriminden alan yüksek frekanslı, monoton ve tiz ağlama sesidir. Akustik spektrografik analizlerde bebeğin ağlaması aç bir yavru kedinin miyavlamasıyla birebir örtüşen akustik frekans özellikleri sergiler. Bu ses anomalisi iki temel patofizyolojik mekanizmanın bileşimidir: (1) Larinksin anatomik malformasyonu; larinks küçük, dar, kıkırdak yapısı hipoplastik ve epiglot küçük, sarkık ve yaprak biçimindedir. (2) Santral sinir sistemindeki nöromotor fonasyon denetiminin disfonksiyonu. Çok önemli bir klinik ve sınav spotu olarak: Bu karakteristik tiz kedi ağlaması sesi BEBEKLİK DÖNEMİNE ÖZGÜDÜR; çocuk büyüdükçe larinks kıkırdaklarının olgunlaşmasıyla genellikle yaşamın ilk birkaç yılı içinde veya yetişkinlikte tamamen kaybolur.",
                "keyBullets": [
                    {"title": "Patognomonik Ağlama", "desc": "Tiz, yüksek frekanslı ve monoton kedi miyavlaması sesidir.", "isKey": True},
                    {"title": "Larinks Hipoplazisi", "desc": "Küçük larinks ve sarkık epiglot akustik tablonun anatomik zeminidir.", "isKey": True},
                    {"title": "Yaşla Kaybolma Kuralı", "desc": "Ağlama sesi bebeklikte vardır, çocukluk ve erişkinlik döneminde KAYBOLUR.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Cri du Chat Ağlama Sesinin Yaşla Evrimi",
                    "Yenidoğan ve Erken Süt Çocukluğu",
                    "Patognomonik tiz, yüksek perdeli, monoton kedi miyavlaması ağlaması; larinks hipoplazisi belirgindir.",
                    "Büyük Çocukluk ve Yetişkinlik Dönemi",
                    "Karakteristik kedi ağlaması sesi tamamen kaybolur; ses kalınlaşır, belirgin artikülasyon ve konuşma güçlüğü kalır."
                ),
                make_cloze(
                    "Cri du chat sendromunda karakteristik tiz kedi miyavlaması benzeri ağlama sesi yetişkinlikte tamamen kaybolur.",
                    "kaybolur",
                    "Sesin yaşla değişim durumunu anımsayınız"
                ),
                make_active_recall(
                    "Cri du chat sendromundaki tipik tiz kedi ağlaması sesinin ortaya çıkmasına yol açan anatomik laringeal defekt nedir?",
                    "Larinksin küçük ve dar olması ile epiglotun sarkık, hipoplastik yapıda bulunmasıdır.",
                    "Larinks kıkırdak ve epiglot hipoplazisi"
                )
            ],
            "spotPearls": [
                "Cri du chat'daki kedi ağlaması larinks hipoplazisi ve nöromotor kusura bağlıdır.",
                "Kedi ağlaması sesi kalıcı değildir; yaş ilerledikçe ve erişkinlikte KAYBOLUR.",
                "Büyüyen çocuklarda ses boğuklaşır ve ağır konuşma geriliği devam eder."
            ]
        },

        # Slayt 54
        {
            "title": "Cri du Chat Sendromunda Klinik Seyir, Dismorfoloji ve Bilişsel Tablo",
            "subtitle": "Ay Yüz Görünümü, Mikrosefali ve Şiddetli Zihinsel Engellilik",
            "badge": "Cri du Chat Fenotipi",
            "coreContent": {
                "text": "Cri du chat sendromlu çocukların kraniyofasiyal muayenesinde belirgin dismorfik stigmalar dikkati çeker. Bebeklik döneminde yuvarlak ve dolgun bir yüz görünümü ('ay yüz' / moon face) tipiktir; yaş ilerledikçe bu yuvarlaklık kaybolarak yüz uzun ve dar bir hal alır. Şiddetli mikrosefali hemen her olguda mevcuttur. Göz muayenesinde iki göz küresi arasındaki mesafenin belirgin arttığı hipertelorizm, aşağıya doğru eğimli palpebral fissürler (antimongoloid eğim), epikantal kıvrımlar ve strabismus saptanır. Burun kökü geniş ve basıktır; mikrognati (küçük çene), düşük yerleşimli kulaklar ve dar damak eşlik eder. Bilişsel açıdan derin veya ağır derecede zihinsel yetersizlik (IQ genellikle <20-30) izlenir. Şiddetli psikomotor retardasyon nedeniyle yürüme çok geç kazanılır, sözlü dil gelişimi son derece sınırlıdır ancak alıcı dil becerileri ifade edici dilden daha iyidir.",
                "keyBullets": [
                    {"title": "Ay Yüz (Moon Face)", "desc": "Bebeklikte yuvarlak yüz tipiktir; yaşla birlikte uzayarak daralır.", "isKey": True},
                    {"title": "Göz Stigmaları", "desc": "Hipertelorizm (ayrık gözler) ve aşağı eğimli palpebral fissürler karakteristiktir.", "isKey": True},
                    {"title": "Derin Zekâ Geriliği", "desc": "IQ genellikle 20-30 altındadır; mikrosefali ve ağır konuşma geriliği sabittir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Anatomik Bölge", "Bebeklik Bulgusu", "Erişkinlik / İleri Çocukluk Bulgusu"],
                    [
                        [("Yüz Şekli", False, ""), ("Yuvarlak dolgun 'ay yüz' (moon face)", True, "Dolgun yüz morfolojisi"), ("Uzun, dar ve asimetrik yüz yapısı", False, "")],
                        [("Kranium", False, ""), ("Belirgin mikrosefali", True, "Küçük kafa çevresi"), ("Kalıcı şiddetli mikrosefali", False, "")],
                        [("Gözler", False, ""), ("Hipertelorizm, aşağı çekik fissürler", True, "Ayrık göz aralığı"), ("Strabismus ve miyopi", False, "")],
                        [("Ses / Ağlama", False, ""), ("Tiz kedi miyavlaması ağlaması", False, ""), ("Ağlama kaybolur; boğuk ses, konuşamama", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Cri du chat sendromlu çocukların dismorfik kraniofasiyal muayenesinde aşağıdakilerden hangisi beklenen karakteristik bir bulgu DEĞİLDİR?",
                    {
                        "A": "Bebeklikte yuvarlak 'ay yüz' (moon face) görünümü",
                        "B": "Hipertelorizm (gözler arası mesafenin artması)",
                        "C": "Aşağı eğimli palpebral fissürler",
                        "D": "Mikrosefali",
                        "E": "Makrosefali ve belirgin çıkıntılı oksiput"
                    },
                    "E",
                    {
                        "A": "Ay yüz tipik bebeklik bulgusudur.",
                        "B": "Hipertelorizm çok karakteristiktir.",
                        "C": "Aşağı eğimli fissürler karakteristiktir.",
                        "D": "Mikrosefali kardinal bulgudur.",
                        "E": "Doğru cevap E'dir: Makrosefali ve çıkıntılı oksiput Cri du chat'da görülmez (mikrosefali görülür; çıkıntılı oksiput Edwards'a özgüdür)."
                    }
                ),
                make_active_recall(
                    "Cri du chat sendromlu bebeklerin yüz görünümünde özellikle ilk aylarda dikkati çeken yuvarlak yüz manzarasına ne ad verilir?",
                    "Ay yüz (moon face) görünümü adı verilir.",
                    "Dolgun yuvarlak yüz eponimi"
                )
            ],
            "spotPearls": [
                "Cri du chat'da bebeklikte 'ay yüz' (moon face), hipertelorizm ve mikrosefali vardır.",
                "Göz kapak fissürleri aşağı eğimlidir (Down'ın aksine).",
                "Derin zihinsel yetersizlik (IQ < 30) ve şiddetli konuşma geriliği tipiktir."
            ]
        },

        # Slayt 55
        {
            "title": "Wolf-Hirschhorn Sendromu: del(4p16.3) ve Yunan Miğferi Görünümü",
            "subtitle": "4. Kromozom Kısa Kol Delesyonu ve Patognomonik Yüz Dismorfizmi",
            "badge": "Wolf-Hirschhorn",
            "coreContent": {
                "text": "Wolf-Hirschhorn sendromu (4p- sendromu), 4. kromozomun kısa kolunun terminal bölgesindeki delesyon sonucu gelişen ağır bir genetik hastalıktır [46,XX veya XY,del(4)(p16.3)]. Görülme sıklığı yaklaşık 1/50.000 canlı doğumdur ve kızlarda iki kat daha sıktır. Olguların %85'i de novo delesyon, %15'i ebeveyn translokasyonuna bağlıdır. Delesyon bölgesinin küçüklüğü nedeniyle geleneksel karyotipte saptanamayabilir; tanıda Floresan İn Situ Hibridizasyon (FISH) veya Kromozomal Mikroarray (CMA) altın standarttır. Sendromun en karakteristik ve patognomonik fizik muayene bulgusu, geniş burun kökünün alından aşağıya kesintisiz devam etmesiyle oluşan 'Yunan savaşçı miğferi' (Greek warrior helmet) yüz görünümüdür. Belirgin glabella, yüksek kavisli kaşlar, hipertelorizm, ptozis ve kısa filtrum bu dramatik kraniofasiyal tabloyu tamamlar.",
                "keyBullets": [
                    {"title": "Sitogenetik Kod", "desc": "4. kromozom kısa kol terminal delesyonudur: del(4)(p16.3).", "isKey": True},
                    {"title": "Yunan Miğferi Yüzü", "desc": "Geniş burun kökünün alınla birleştiği 'Greek warrior helmet' patognomoniktir.", "isKey": True},
                    {"title": "Tanı Yöntemi", "desc": "Karyotipte sıklıkla atlanır; kesin tanı FISH veya CMA ile konur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Boyut", "Wolf-Hirschhorn Sendromu (4p-)", "Klinik Özellik"],
                    [
                        [("Kromozomal Bölge", False, ""), ("4p16.3 delesyonu", True, "4. kromozom kısa kol ucu"), ("WHCR1 ve WHCR2 kritik bölgeleri"), ],
                        [("Patognomonik Yüz", False, ""), ("Yunan savaşçı miğferi görünümü", True, "Greek warrior helmet"), ("Geniş burun köprüsü ve belirgin glabella"), ],
                        [("Tanı Aracı", False, ""), ("FISH veya Kromozomal Mikroarray (CMA)", True, "Moleküler sitogenetik"), ("Standart karyotipte sıklıkla gözden kaçar"), ],
                        [("Cinsiyet Dağılımı", False, ""), ("Kızlarda 2 kat daha sık (K/E: 2/1)", False, ""), ("Kız çocuklarında belirgin fazlalık"), ]
                    ]
                ),
                make_micro_quiz(
                    "Geniş ve basık burun köprüsünün alına doğru kesintisiz devam etmesiyle 'Yunan savaşçı miğferi' (Greek warrior helmet) yüz görünümü sergileyen bir bebekte en olası kromozom anomalisi hangisidir?",
                    {
                        "A": "del(5)(p15.2)",
                        "B": "del(4)(p16.3)",
                        "C": "del(22)(q11.2)",
                        "D": "del(7)(q11.23)",
                        "E": "del(17)(p11.2)"
                    },
                    "B",
                    {
                        "A": "5p delesyonu Cri du chat sendromudur.",
                        "B": "Doğru cevap B'dir: del(4)(p16.3) Wolf-Hirschhorn sendromudur ve Yunan miğferi yüzü patognomoniktir.",
                        "C": "22q11 DiGeorge sendromudur.",
                        "D": "7q11 Williams sendromudur.",
                        "E": "17p11 Smith-Magenis sendromudur."
                    }
                ),
                make_cloze(
                    "Wolf-Hirschhorn sendromunda geniş burun köprüsünün alından devam etmesiyle oluşan klasik yüz profiline Yunan miğferi görünümü denir.",
                    "Yunan miğferi",
                    "Karakteristik savaşçı kaskı profilini anımsayınız"
                )
            ],
            "spotPearls": [
                "Wolf-Hirschhorn sendromu del(4p16.3) delesyonudur.",
                "Patognomonik yüz stigmati 'Yunan savaşçı miğferi' (Greek warrior helmet) görünümüdür.",
                "Tanıda geleneksel karyotip yetersiz kalabilir; FISH veya Mikroarray şarttır."
            ]
        },

        # Slayt 56
        {
            "title": "Wolf-Hirschhorn Sendromunda Nöbetler, Ağır Büyüme Geriliği ve Balık Ağzı",
            "subtitle": "Kritik Genler, İnatçı Epilepsi ve Ağız Dismorfizmi",
            "badge": "Wolf-Hirschhorn Kliniği",
            "coreContent": {
                "text": "Wolf-Hirschhorn sendromunun (4p-) klinik seyri, insan genetiğindeki en ağır büyüme ve nörogelişimsel kısıtlanma tablolarından biridir. İntrauterin dönemde başlayan ağır büyüme geriliği postnatal dönemde de devam eder; mikrosefali belirgindir. Ağız muayenesinde köşeleri aşağıya doğru kıvrık üst dudak ile karakterize 'balık ağzı' (carp mouth) manzarası, kısa filtrum ve yarık dudak/damak görülür. Nörolojik açıdan en yıkıcı bulgu, olguların %90-100'ünde erken süt çocukluğunda başlayan inatçı, tedaviye dirençli epileptik nöbetlerdir. Bu nöbetlerin moleküler temeli, 4p16.3 bölgesinde yer alan ve GABA-A reseptör alt birimlerini kodlayan GABRG1 geninin delesyonudur. Beyin MRG'sinde korpus kallozum agenezisi ve ventrikülomegali sık saptanır; derin mental retardasyon (IQ < 20) ve hipotoni ile birlikte çocukların çoğu yürüyemez ve konuşamaz.",
                "keyBullets": [
                    {"title": "Balık Ağzı (Carp Mouth)", "desc": "Ağız köşeleri aşağı sarkık, ters 'V' şeklinde üst dudak manzarasıdır.", "isKey": True},
                    {"title": "Tedaviye Dirençli Nöbetler", "desc": "GABRG1 geni kaybı nedeniyle olguların %90'ından fazlasında epilepsi görülür.", "isKey": True},
                    {"title": "Derin Zekâ Geriliği", "desc": "Ağır mikrosefali ve korpus kallozum agenezisiyle derin bilişsel yetersizlik sabittir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Cri du Chat vs Wolf-Hirschhorn Karşılaştırması",
                    "Cri du Chat [del(5p15)]",
                    "Kedi miyavlaması ağlaması, ay yüz, hipertelorizm, mikrosefali; karyotipte genellikle rahat görünür.",
                    "Wolf-Hirschhorn [del(4p16.3)]",
                    "Yunan miğferi yüzü, balık ağzı, inatçı nöbetler (epilepsi), ağır gelişme geriliği; tanıda FISH/CMA gerekir."
                ),
                make_cloze(
                    "Wolf-Hirschhorn sendromunda ağız köşelerinin aşağıya doğru çekilmesiyle oluşan tipik dudak anomalisi balık ağzı görünümü olarak adlandırılır.",
                    "balık ağzı",
                    "Tipik ağız morfolojisini anımsayınız"
                ),
                make_active_recall(
                    "Wolf-Hirschhorn sendromlu olguların %90'ından fazlasında erken çocuklukta dirençli epileptik nöbetler gelişmesinden sorumlu olan 4p16.3 yerleşimli nöronal gen hangisidir?",
                    "GABA-A reseptör alt birimini kodlayan GABRG1 genidir.",
                    "İnhibitör nörotransmitter reseptör geni"
                )
            ],
            "spotPearls": [
                "Wolf-Hirschhorn'da 'balık ağzı' görünümü ve yarık damak/dudak sıktır.",
                "Dirençli nöbetler (epilepsi) olguların %90'ında görülür (GABA reseptör gen kaybı).",
                "Ağır büyüme geriliği ve korpus kallozum agenezisi eşlik eder."
            ]
        },

        # Slayt 57
        {
            "title": "DiGeorge Sendromu (22q11.2 Delesyonu / CATCH-22 Fenotipi)",
            "subtitle": "Farinks Poşlarının Embriyolojik Disgenezisi ve Çoklu Organ Tutulumu",
            "badge": "DiGeorge Sendromu",
            "coreContent": {
                "text": "DiGeorge sendromu (Velokardiyofasiyal sendrom / 22q11.2 mikrodelesyonu), canlı doğumlarda yaklaşık 1/4000 sıklıkla en sık rastlanan mikrodelesyon sendromudur. 3. ve 4. faringeal (yutak) poşlarının embriyolojik morfogenez kusuru sonucu gelişir. Klasik klinik tablo 'CATCH-22' akronimi ile özetlenir: C (Cardiac defects; özellikle Fallot tetralojisi, kesintili aort yayı, trunkus arteriyozus gibi konotrunkal kalp anomalileri), A (Abnormal facies; tübüler burun, dar gözler), T (Thymic hypoplasia / aplasia; T lenfosit olgunlaşma defekti ve hücresel immün yetersizlik), C (Cleft palate / velofaringeal yetmezlik; bifid uvula, submüköz yarık), H (Hypocalcemia; paratiroid bezlerinin aplazisine bağlı neonatal inatçı hipokalsemik tetani), 22 (22q11.2 delesyonu). Bu sendromdaki vasküler ve faringeal anomalilerin temel orkestratörü, bölgede silinen TBX1 transkripsiyon faktörü genidir.",
                "keyBullets": [
                    {"title": "En Sık Mikrodelesyon", "desc": "22q11.2 delesyonudur; canlı doğumlarda 1/4000 sıklıkla en yaygın olandır.", "isKey": True},
                    {"title": "CATCH-22 Akronimi", "desc": "Kalp defekti, Anormal yüz, Timus yokluğu, Damak yarığı, Hipokalsemi, 22q11.", "isKey": True},
                    {"title": "Kritik TBX1 Geni", "desc": "Konotrunkal kardiyak ve faringeal malformasyonların ana sorumlusu TBX1'dir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["CATCH-22 Harfi", "Klinik Bileşen", "Embriyolojik / Patofizyolojik Mekanizma"],
                    [
                        [("C (Cardiac)", False, ""), ("Konotrunkal kalp anomalileri (Fallot, Truncus)", True, "Kalp çıkım yolu defektleri"), ("Kardiyak nöral krest göç kusuru", False, "")],
                        [("A (Abnormal)", False, ""), ("Dismorfik yüz (tübüler burun, mikrognati)", True, "Tipik yüz stigmaları"), ("Faringeal ark mezenkim hipoplazisi", False, "")],
                        [("T (Thymic)", False, ""), ("Timus aplazisi / hipoplazisi", True, "Timus yokluğu"), ("T lenfosit yetmezliği, fungal/viral enfeksiyonlar", False, "")],
                        [("C (Cleft)", False, ""), ("Yarık damak, velofaringeal yetersizlik", True, "Damak kapanma kusuru"), ("Hipernazal konuşma ve beslenme reflüsü", False, "")],
                        [("H (Hypocalcemia)", False, ""), ("Neonatal hipokalsemi ve tetani", True, "Parathormon eksikliği"), ("Paratiroid bezi aplazisi / agenezisi", False, "")],
                        [("22 (Delesyon)", False, ""), ("22q11.2 mikrodelesyonu", False, ""), ("FISH veya Kromozomal Mikroarray ile tanı", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Yenidoğan döneminde inatçı hipokalsemik konvülsiyonlar geçiren, ekokardiyografisinde Fallot tetralojisi saptanan ve periferik kanda T lenfosit sayısı belirgin düşük bulunan bir bebekte kesin tanı için hangi genetik test ilk sırada istenmelidir?",
                    {
                        "A": "Klasik G-bantlama karyotip analizi",
                        "B": "22q11.2 bölgesine yönelik FISH veya Kromozomal Mikroarray (CMA)",
                        "C": "Karyotipte 5p delesyonu taraması",
                        "D": "FMR1 geni CGG tekrar analizi",
                        "E": "DMD geni delesyon taraması"
                    },
                    "B",
                    {
                        "A": "Standart karyotip mikrodelesyonu yakalayamaz.",
                        "B": "Doğru cevap B'dir: DiGeorge sendromu (22q11.2) mikrodelesyondur; standart karyotipte görülmez, FISH veya CMA şarttır.",
                        "C": "5p Cri du chat'dır.",
                        "D": "FMR1 Frajil X sendromudur.",
                        "E": "DMD kas distrofisidir."
                    }
                ),
                make_cloze(
                    "DiGeorge sendromunda konotrunkal kalp anomalileri ve faringeal ark disgenezisinden sorumlu anahtar transkripsiyon faktörü TBX1 genidir.",
                    "TBX1",
                    "T-box ailesi transkripsiyon genini anımsayınız"
                )
            ],
            "spotPearls": [
                "DiGeorge sendromu 22q11.2 mikrodelesyonudur (en sık mikrodelesyon).",
                "CATCH-22: Kalp anomalisi (Fallot), Timus yokluğu, Yarık damak, Hipokalsemi (paratiroid yokluğu).",
                "Patogenezdeki anahtar gen TBX1'dir; standart karyotipte görülmez (FISH/CMA gerekir)."
            ]
        },

        # Slayt 58
        {
            "title": "Williams-Beuren Sendromu: del(7q11.23) ve Kokteyl Kişilik",
            "subtitle": "Elastin Geni Dozajı, Supravalvüler Aort Stenozu ve Peri Yüzü",
            "badge": "Williams Sendromu",
            "coreContent": {
                "text": "Williams-Beuren sendromu, 7. kromozomun uzun kolundaki 7q11.23 bandının mikrodelesyonu sonucu ortaya çıkan nörogelişimsel bir tablodur (yaklaşık 1/10.000 canlı doğum). Bu mikrodelesyon bölgesinde yaklaşık 26-28 gen silinir; bu genler arasında en kritik olanı vasküler elastik liflerin ana yapıtaşı olan Elastin (ELN) genidir. ELN geninin haploinsüfisyensi nedeniyle damar duvarlarında elastik doku sentezlenemez; olguların büyük kısmında Supravalvüler Aort Stenozu (SVAS) ve periferik pulmoner arter stenozları gelişir. Karakteristik dismorfik yüz 'elf yüzü' (elfin facies / peri yüzü) olarak tanımlanır: dolgun yanaklar, basık burun kökü, kalkık burun ucu, geniş ağız, dolgun dudaklar ve iriste yıldızsı (stellat) patern görülür. Bebeklikte idiyopatik hiperkalsemi sıktır. Davranışsal profili son derece özgündür: 'kokteyl partisi kişiliği' (yabancılara karşı aşırı sosyal, aşırı konuşkan, empati dolu, kelime haznesi zengin ancak derin bilişsel yetersizlik ve uzamsal algı bozukluğu olan profil) sergilerler.",
                "keyBullets": [
                    {"title": "Sitogenetik Kod", "desc": "7. kromozom uzun kol mikrodelesyonudur: del(7q11.23).", "isKey": True},
                    {"title": "Elastin (ELN) Geni", "desc": "Supravalvüler aort stenozu (SVAS) gelişiminin ana sorumlusudur.", "isKey": True},
                    {"title": "Kokteyl Kişilik", "desc": "Aşırı sosyal, yabancılardan korkmayan, konuşkan davranış fenotipidir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Boyut", "Williams-Beuren Sendromu (7q11.23)", "Patofizyolojik / Moleküler Temel"],
                    [
                        [("Kardiyovasküler Defekt", False, ""), ("Supravalvüler Aort Stenozu (SVAS)", True, "Aort kapak üstü darlık"), ("Elastin (ELN) geni haploinsüfisyensi", False, "")],
                        [("Fasiyal Dismorfoloji", False, ""), ("Elfin facies (peri yüzü), yıldızsı iris", True, "Elf / peri benzeri yüz"), ("Dolgun yanaklar ve kalkık burun ucu", False, "")],
                        [("Davranışsal Profil", False, ""), ("Kokteyl partisi kişiliği (aşırı sosyallik)", True, "Aşırı dışadönük kişilik"), ("Sosyal inhibisyon kaybı ve müzikal yetenek", False, "")],
                        [("Metabolik Belirteç", False, ""), ("İnfantil idiyopatik hiperkalsemi", False, ""), ("Artmış D vitamini duyarlılığı", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Williams-Beuren sendromlu [del(7q11.23)] çocuklarda görülen supravalvüler aort stenozu (SVAS) ve yaygın arteriyel darlıkların gelişiminden sorumlu olan delesyon bölgesi geni hangisidir?",
                    {
                        "A": "TBX1",
                        "B": "Elastin (ELN)",
                        "C": "PMP22",
                        "D": "FBN1",
                        "E": "COL1A1"
                    },
                    "B",
                    {
                        "A": "TBX1 DiGeorge genidir.",
                        "B": "Doğru cevap B'dir: Williams sendromundaki vasküler lezyonlardan 7q11.23'teki Elastin (ELN) geni delesyonu sorumludur.",
                        "C": "PMP22 Charcot-Marie-Tooth genidir.",
                        "D": "FBN1 Marfan genidir.",
                        "E": "COL1A1 Osteogenezis imperfekta genidir."
                    }
                ),
                make_cloze(
                    "Williams sendromlu çocukların yabancılardan korkmayan, aşırı sosyal, konuşkan ve dışadönük davranış profiline kokteyl partisi kişiliği denir.",
                    "kokteyl partisi",
                    "Aşırı sosyal davranış profilinin eponimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Williams sendromu 7q11.23 mikrodelesyonudur.",
                "Elastin (ELN) geni kaybı Supravalvüler Aort Stenozuna (SVAS) yol açar.",
                "Karakteristik davranış: 'kokteyl partisi kişiliği' (aşırı sosyal, yabancılardan korkusuz)."
            ]
        },

        # Slayt 59 (CHECKPOINT 6)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Yapısal Delesyon ve Mikrodelesyon Sendromları",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 6",
            "coreContent": {
                "text": "Bu bölümde yapısal delesyonların ve mikrodelesyonların klinik spektrumunu entegre ettik. Klasik delesyonlar ışık mikroskobik karyotipte görülebilir: Cri du chat [del(5p15.2)] kedi miyavlaması benzeri tiz ağlama (larinks hipoplazisi, yaşla KAYBOLUR), ay yüz ve hipertelorizmle seyreder; ses 5p15.3, dismorfoloji 5p15.2 delesyonuyla ilişkilidir. Wolf-Hirschhorn [del(4p16.3)] 'Yunan savaşçı miğferi' (Greek warrior helmet) yüz görünümü, balık ağzı ve GABRG1 kaybına bağlı dirençli nöbetlerle (epilepsi) karakterizedir; tanıda FISH/CMA gerekir. Mikrodelesyonlar standart karyotipte görülemez: DiGeorge [del(22q11.2)] en sık mikrodelesyondur; CATCH-22 tablosu (Fallot, Timus yokluğu, Damak yarığı, Hipokalsemi) ve TBX1 gen kaybı hakimdir. Williams sendromu [del(7q11.23)] Elastin (ELN) gen kaybına bağlı Supravalvüler Aort Stenozu (SVAS), elfin facies ve kokteyl partisi kişiliği ile tanınır.",
                "keyBullets": [
                    {"title": "Cri du Chat (5p-)", "desc": "Kedi ağlaması (yaşla kaybolur), ay yüz, mikrosefali; %85 de novo.", "isKey": True},
                    {"title": "Wolf-Hirschhorn (4p-)", "desc": "Yunan miğferi yüzü, balık ağzı, dirençli epilepsi; FISH/CMA şarttır.", "isKey": True},
                    {"title": "DiGeorge vs Williams", "desc": "22q11 CATCH-22 (TBX1); 7q11 SVAS ve kokteyl partisi kişiliği (ELN).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sendrom", "Kromozom Bölgesi", "Patognomonik İpucu", "Kritik Gen"],
                    [
                        [("Cri du Chat", False, ""), ("del(5p15)", False, ""), ("Kedi miyavlaması ağlaması (yaşla geçer)", True, "Larinks hipoplazisi sesi"), ("5p15.3 / 5p15.2", False, "")],
                        [("Wolf-Hirschhorn", False, ""), ("del(4p16.3)", False, ""), ("Yunan miğferi yüzü + Erken nöbetler", True, "Greek warrior helmet"), ("GABRG1 / WHCR", False, "")],
                        [("DiGeorge", False, ""), ("del(22q11.2)", False, ""), ("CATCH-22: Hipokalsemi, Timus yokluğu, Fallot", True, "Farinks poş defekti"), ("TBX1", False, "")],
                        [("Williams-Beuren", False, ""), ("del(7q11.23)", False, ""), ("Kokteyl kişiliği, peri yüzü, SVAS", True, "Aşırı dışadönüklük"), ("Elastin (ELN)", False, "")]
                    ]
                ),
                make_cloze(
                    "Cri du chat sendromunda kedi ağlaması sesi 5p15.3 delesyonundan, Wolf-Hirschhorn'daki Yunan miğferi yüzü ise 4p16.3 delesyonundan kaynaklanır.",
                    "4p16.3",
                    "Wolf-Hirschhorn delesyon bandını anımsayınız"
                ),
                make_active_recall(
                    "DiGeorge sendromunda yenidoğan yoğun bakımda konvülsiyonlara yol açan hipokalseminin embriyolojik nedeni nedir?",
                    "3. ve 4. faringeal poş disgenezisine bağlı paratiroid bezlerinin konjenital aplazisi/agenezisidir.",
                    "Paratiroid bezi yokluğu"
                )
            ],
            "spotPearls": [
                "Cri du chat = 5p15 delesyonu, kedi ağlaması (erişkinlikte kaybolur).",
                "Wolf-Hirschhorn = 4p16.3 delesyonu, Yunan miğferi yüzü, inatçı nöbetler.",
                "DiGeorge = 22q11.2 delesyonu, TBX1, CATCH-22.",
                "Williams = 7q11.23 delesyonu, Elastin (SVAS), kokteyl kişiliği."
            ]
        },

        # Slayt 60
        {
            "title": "Gen Dozajının Zıt Uçları: CMT-1A (17p12 Duplikasyonu) ve HNPP (17p12 Delesyonu)",
            "subtitle": "PMP22 Gen Dozajına Bağlı Resiprokal Periferik Nöropatiler",
            "badge": "PMP22 Gen Dozajı",
            "coreContent": {
                "text": "17p12 kromozomal bölgesi, insan tıbbi genetiğinde gen dozajı kavramının ve alelik olmayan homolog rekombinasyonun (NAHR) en kusursuz ders kitabı modelidir. Bu bölgede Periferik Miyelin Proteini 22'yi kodlayan PMP22 geni yer alır. Bölgeyi çevreleyen homoloji gösteren düşük kopya tekrarları (LCR) mayozda eşit olmayan krossing-overa girdiğinde iki resiprokal kromatit üretir: (1) 17p12 bölgesinin DUPLİKASYONU (PMP22'nin 3 kopyası): Charcot-Marie-Tooth Tip 1A (CMT-1A) hastalığına yol açar. Schwann hücrelerinde aşırı PMP22 birikimi demiyelinizasyona, sinir ileti hızında belirgin yavaşlamaya (<38 m/sn), distal kas atrofisine (leylek bacağı manzarası) ve pes kavus deformitesine neden olur. (2) 17p12 bölgesinin DELESYONU (PMP22'nin tek kopyası): Basınca Duyarlı Herediter Nöropatiye (HNPP) yol açar. Tek kopya PMP22 miyelini mekanik basınca hassas hale getirir; hafif basılar sonrasında geçici fokal sinir felçleri (düşük el, peroneal felç) ve sinir biyopsisinde 'tomaküla' (sosis benzeri miyelin şişlikleri) görülür.",
                "keyBullets": [
                    {"title": "CMT-1A (Duplikasyon)", "desc": "17p12 duplikasyonu (3 kopya PMP22); demiyelinizan polinöropati, pes kavus.", "isKey": True},
                    {"title": "HNPP (Delesyon)", "desc": "17p12 delesyonu (tek kopya PMP22); basınca duyarlı geçici fokal felçler, tomaküla.", "isKey": True},
                    {"title": "Resiprokal Mekanizma", "desc": "Mayozdaki tek bir eşit olmayan krossing-over olayı iki zıt hastalığı üretir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "PMP22 Gen Dozajı: CMT-1A vs HNPP",
                    "CMT-1A (17p12 Duplikasyonu - 3 Kopya)",
                    "Aşırı PMP22 üretimi; kronik ilerleyici simetrik distal sensorimotor demiyelinizan nöropati, leylek bacağı, pes kavus.",
                    "HNPP (17p12 Delesyonu - 1 Kopya)",
                    "Yetersiz PMP22 (haploinsüfisyens); hafif bası ile tetiklenen ağrısız geçici mononöropatiler (tomaküloz nöropati)."
                ),
                make_micro_quiz(
                    "17. kromozomun kısa kolundaki 17p12 bölgesinde yer alan PMP22 geninin duplikasyonu ve delesyonu sonucu ortaya çıkan nöropatiler sırasıyla hangisinde doğru eşleştirilmiştir?",
                    {
                        "A": "CMT-1A (Duplikasyon) — HNPP (Delesyon)",
                        "B": "HNPP (Duplikasyon) — CMT-1A (Delesyon)",
                        "C": "DiGeorge (Duplikasyon) — Williams (Delesyon)",
                        "D": "Cri du chat (Duplikasyon) — Wolf-Hirschhorn (Delesyon)",
                        "E": "Smith-Magenis (Duplikasyon) — Potocki-Lupski (Delesyon)"
                    },
                    "A",
                    {
                        "A": "Doğru cevap A'dır: 17p12 duplikasyonu CMT-1A, 17p12 delesyonu ise HNPP hastalığına yol açar.",
                        "B": "Kombinasyon tam tersidir.",
                        "C": "22q ve 7q bölgeleridir.",
                        "D": "5p ve 4p bölgeleridir.",
                        "E": "Potocki-Lupski duplikasyon, Smith-Magenis delesyonudur."
                    }
                ),
                make_cloze(
                    "17p12 bölgesindeki PMP22 geninin delesyonu sonucu hafif basılarla fokal felçler gelişen hastalığa basınca duyarlı herediter nöropati veya HNPP denir.",
                    "HNPP",
                    "Basınca duyarlı nöropati kısaltmasını yazınız"
                )
            ],
            "spotPearls": [
                "17p12 DUPLİKASYONU (3 kopya PMP22) = Charcot-Marie-Tooth Tip 1A (CMT-1A).",
                "17p12 DELESYONU (tek kopya PMP22) = Basınca Duyarlı Herediter Nöropati (HNPP).",
                "Bu iki hastalık eşit olmayan krossing-overın resiprokal ürünleridir."
            ]
        }
    ]
