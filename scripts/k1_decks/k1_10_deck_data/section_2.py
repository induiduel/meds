"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 2 (Slayt 11 - 20)
Konu: Yapısal Kromozom Anomalileri, Kırık-Birleşme Mekanizmaları, Delesyon, Duplikasyon, İnversiyon, Ring ve İzokromozomlar
Checkpoint: Slayt 19 ([TEKRAR SAYFASI - CHECKPOINT 2])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_2_slides():
    return [
        # Slayt 11
        {
            "title": "Yapısal Kromozom Anomalilerinin Biyolojik Temeli: Kırıklar ve Onarım",
            "subtitle": "DNA Çift Zincir Kırıkları ve Hatalı Rekombinasyon Mekanizmaları",
            "badge": "Yapısal Anomaliler",
            "coreContent": {
                "text": "Yapısal kromozom anomalileri, kromozom kollarında meydana gelen DNA çift zincir kırıkları (double-strand breaks) ve bu yapışkan kırık uçlarının hücresel DNA onarım mekanizmaları tarafından hatalı birleştirilmesi (homolog olmayan uç birleştirme - NHEJ veya alelik olmayan homolog rekombinasyon - NAHR) sonucu oluşur. Normalde telomerler kromozom uçlarını enzimatik yıkımdan ve füzyondan korur; ancak kırılma meydana geldiğinde telomersiz çıplak uçlar son derece kararsızdır ve diğer kırık uçlarla birleşmeye zorlanır. Yapısal anomaliler dengeli (toplam genetik materyal miktarının değişmediği) ve dengesiz (materyal kaybı veya kazanımının olduğu) olarak ikiye ayrılır. Canlı doğan bebeklerin yaklaşık 1/375'inde yapısal bir kromozom anomalisi mevcuttur. Ebeveynlerin birinde dengeli yapısal anomali bulunması, mayoz sırasında kromatitlerin yanlış dizilimi nedeniyle sonraki kuşakta dengesiz gamet oluşumu ve tekrarlayan düşük riskini ciddi oranda artırır.",
                "keyBullets": [
                    {"title": "Oluşum Prensibi", "desc": "DNA çift zincir kırıklarının telomersiz uçlarla hatalı birleştirilmesidir.", "isKey": True},
                    {"title": "Yenidoğan Sıklığı", "desc": "Canlı doğan her 375 bebekten birinde yapısal bir anomali saptanır.", "isKey": True},
                    {"title": "Kalıtım Riski", "desc": "Dengeli ebeveyn anomalileri mayotik dengesiz gamet riskiyle sonraki kuşağa aktarılır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "Canlı doğan bebeklerin yaklaşık 1/375 oranında yapısal bir kromozom anomalisi saptanmaktadır.",
                    "1/375",
                    "Yapısal kromozom anomalisi yenidoğan oranını düşününüz"
                ),
                make_table(
                    ["Anomali Tipi", "Materyal Dengesi", "Karyotipik Örnekler", "Klinik Özellik"],
                    [
                        [("Dengeli Anomaliler", False, ""), ("Net kayıp veya kazanç yok", True, "Materyal korunum durumu"), ("İnversiyon, Dengeli Translokasyon", False, ""), ("Taşıyıcı sağlıklı; sonraki kuşak riskli", False, "")],
                        [("Dengesiz Anomaliler", False, ""), ("Net genetik kayıp veya artış var", True, "Materyal fazlalığı/azlığı"), ("Delesyon, Duplikasyon, İzokromozom", False, ""), ("Taşıyıcıda konjenital anomali ve zekâ geriliği", False, "")]
                    ]
                ),
                make_active_recall(
                    "Kromozom kollarında kırık oluştuktan sonra uçların birbirine kaynaşmasını önleyen normal koruyucu kromozom yapısı nedir?",
                    "Kromozomların uç bölgelerinde bulunan özelleşmiş telomer yapılarıdır.",
                    "Kromozom ucu koruyucu başlığı"
                )
            ],
            "spotPearls": [
                "Yapısal kromozom anomalilerinin sıklığı yenidoğanda yaklaşık 1/375'tir.",
                "Dengesiz yapısal anomaliler delesyon, duplikasyon, izokromozom ve ring kromozomları içerir.",
                "Dengeli yapısal anomaliler inversiyon ve resiprokal/Robertsonian translokasyonlardır."
            ]
        },

        # Slayt 12
        {
            "title": "Delesyonlar (Parsiyel Monozomiler): Terminal ve İnterstisyel Tipler",
            "subtitle": "Kromozomal Segment Kayıpları ve Sitogenetik Boyut",
            "badge": "Delesyon Biyolojisi",
            "coreContent": {
                "text": "Delesyon, bir kromozom segmentinin ve o segment üzerindeki genlerin kaybıdır; sitogenetik açıdan parsiyel monozomi olarak kabul edilir. Delesyonlar kırık sayısına ve lokalizasyonuna göre ikiye ayrılır: tek bir kırık sonucu kromozomun telomerik uç bölgesinin kopup kaybolması terminal delesyon (örneğin Cri du chat sendromundaki 46,XX,del(5)(p15.2)), aynı kolda iki kırık meydana gelmesi ve aradaki parçanın çıkarak uçların birleşmesi ise interstisyel (interkalar) delesyon (örneğin DiGeorge sendromundaki 22q11.2 delesyonu) olarak tanımlanır. Delesyonun klinik şiddeti, kaybedilen segmentin büyüklüğüne ve içerdiği kritik dozaja duyarlı genlerin sayısına doğrudan bağlıdır. Canlı doğumlarda delesyon sıklığı yaklaşık 1/7000'dir; çünkü geniş boyutlu otozomal delesyonların büyük kısmı intrauterin dönemde letal seyrederek spontan abortusla sonuçlanır.",
                "keyBullets": [
                    {"title": "Terminal Delesyon", "desc": "Tek bir kırıkla uç segmentin kaybıdır; örnek 5p15 delesyonu (Cri du chat).", "isKey": True},
                    {"title": "İnterstisyel Delesyon", "desc": "İki kırık arasında kalan iç segmentin kaybıdır; örnek 22q11.2 delesyonu.", "isKey": True},
                    {"title": "Canlı Doğum Sıklığı", "desc": "Delesyonlar yaklaşık 1/7000 canlı doğumda görülür; çoğu letaldir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Terminal vs İnterstisyel Delesyon",
                    "Terminal Delesyon",
                    "Kromozom kolunda tek bir kırık oluşur; telomer içeren distal uç parça koparak hücrede kaybolur (ör. 5p-).",
                    "İnterstisyel Delesyon",
                    "Kromozom kolunda iki ayrı kırık oluşur; aradaki iç segment çıkar, iki uç kırık birbiriyle kaynaşır (ör. 22q11-)."
                ),
                make_micro_quiz(
                    "5. kromozomun kısa kolunun uç kısmının tek bir kırıkla kopup kaybolması sonucu ortaya çıkan Cri du chat sendromu hangi tip delesyonun klasik örneğidir?",
                    {
                        "A": "İnterstisyel delesyon",
                        "B": "Terminal delesyon",
                        "C": "Parasentrik inversiyon",
                        "D": "İzokromozom",
                        "E": "Robertsonian translokasyon"
                    },
                    "B",
                    {
                        "A": "İnterstisyel delesyonda iki kırık arası segment çıkar.",
                        "B": "Doğru cevap B'dir: Kromozomun uç bölgesinin tek kırıkla kaybı terminal delesyondur (del(5p15)).",
                        "C": "İnversiyonda kayıp yoktur, yön değişir.",
                        "D": "İzokromozom kol duplikasyonudur.",
                        "E": "Translokasyon iki kromozom arası füzyondur."
                    }
                ),
                make_cloze(
                    "Aynı kromozom kolunda iki ayrı kırık meydana gelmesi ve aradaki segmentin kaybıyla oluşan delesyon tipine interstisyel delesyon adı verilir.",
                    "interstisyel",
                    "İki kırık arası ara segment kaybı terimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Terminal delesyon: tek kırık, uç bölge kaybı (ör. Cri du chat; 5p15.2).",
                "İnterstisyel delesyon: çift kırık, ara bölge kaybı (ör. DiGeorge; 22q11.2).",
                "Delesyonlar parsiyel monozomidir ve canlı doğumlarda yaklaşık 1/7000 sıklıkta görülür."
            ]
        },

        # Slayt 13
        {
            "title": "Haploinsüfisyens Kavramı: Dozaja Duyarlı Genlerin Fenotipik İmzası",
            "subtitle": "Kromozomal Delesyonların Moleküler Patogenezi",
            "badge": "Haploinsüfisyens",
            "coreContent": {
                "text": "Delesyonların ve parsiyel monozomilerin klinik fenotipe yol açmasındaki temel moleküler mekanizma haploinsüfisyens (haploinsufficiency) fenomenidir. Normal diploid bir hücrede çoğu gen için tek bir fonksiyonel kopyanın varlığı normal hücresel işlevleri sürdürmek için yeterlidir (resesif kalıtım modeli). Ancak bazı genler son derece kritik düzenleyici roller üstlenir; transkripsiyon faktörleri, sinyal iletim proteinleri ve yapısal hücre iskeleti elemanlarını kodlayan bu genlerde, protein ürününün miktarının %50'ye düşmesi hücresel homeostazın bozulması için yeterlidir. Tek bir fonksiyonel alelin normal fenotipi sürdürmeye yetmemesi durumu haploinsüfisyens olarak tanımlanır. Delesyona uğrayan kromozomal segment ne kadar çok haploinsüfisyent gen içeriyorsa, ortaya çıkan klinik tablo o kadar ağır seyreder. Bu durum mikrodelesyon sendromlarındaki çoklu organ tutulumlarının moleküler zeminini oluşturur.",
                "keyBullets": [
                    {"title": "Haploinsüfisyens Tanımı", "desc": "Genin tek kopyasının ürettiği %50 protein miktarının normal işlev için yetersiz kalmasıdır.", "isKey": True},
                    {"title": "Dozaja Duyarlı Genler", "desc": "Özellikle transkripsiyon faktörleri ve morfogenler haploinsüfisyense son derece duyarlıdır.", "isKey": True},
                    {"title": "Klinik Yansıma", "desc": "Delesyondaki haploinsüfisyent gen sayısı arttıkça fenotipik ağırlık ve malformasyonlar katlanır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Haploinsüfisyens ve Klinik Malformasyon Zinciri",
                    [
                        "1. Kromozomal mikrodelesyon sonucu kritik bir gelişimsel genin tek aleli fiziksel olarak kaybolur",
                        "2. Kalan tek sağlam alel maksimum düzeyde ifade edilse bile hücredeki protein düzeyi %50'de kalır",
                        "3. Eksik protein düzeyi embriyonik doku indüksiyonu ve morfogenez eşik değerinin altında kalır",
                        "4. İlgili organda gelişimsel duraklama, hipoplazi ve konjenital malformasyon sendromu gelişir"
                    ]
                ),
                make_cloze(
                    "Tek bir fonksiyonel gen kopyasının normal fenotipi sürdürmeye yetmemesi ve %50 protein düzeyinin patoloji üretmesi durumuna haploinsüfisyens denir.",
                    "haploinsüfisyens",
                    "Yarı dozaj yetersizliğini ifade eden tıbbi terimi anımsayınız"
                ),
                make_active_recall(
                    "Delesyon sendromlarında fenotipik hasarın temelini oluşturan ve protein ürününün yarıya inmesiyle ortaya çıkan kavram nedir?",
                    "Haploinsüfisyens (haploinsufficiency) mekanizmasıdır.",
                    "Dozaj duyarlılığı ve tek kopya yetersizliği"
                )
            ],
            "spotPearls": [
                "Delesyonların klinik etkisi temelde haploinsüfisyens mekanizmasına dayanır.",
                "Haploinsüfisyens, tek sağlam kopyanın ürettiği proteinin normal fizyolojiye yetmemesidir.",
                "Gelişimsel transkripsiyon faktörleri haploinsüfisyense en duyarlı gen gruplarıdır."
            ]
        },

        # Slayt 14
        {
            "title": "Mikrodelesyon ve Mikroduplikasyon Sendromları: Moleküler Sitogenetik",
            "subtitle": "Kromozomal Mikroarray (CMA) ve FISH ile Tanınan Submikroskobik Lezyonlar",
            "badge": "Mikrodelesyonlar",
            "coreContent": {
                "text": "Mikrodelesyon ve mikroduplikasyon sendromları (bitişik gen sendromları / contiguous gene syndromes), geleneksel ışık mikroskobik G-bantlama karyotip analiziyle (çözünürlük ~4-5 milyon baz çifti / Mb) saptanamayacak kadar küçük submikroskobik genomik dengesizliklerdir. Bu lezyonlar genellikle genomdaki düşük kopya tekrarları (LCR - low copy repeats) arasındaki hatalı rekombinasyon (NAHR) sonucu ortaya çıkar. Tanıda Floresan İn Situ Hibridizasyon (FISH) ve tüm genomu yüksek çözünürlükte tarayan Kromozomal Mikroarray (CMA / aCGH) kullanılır. Mikrodelesyon sendromlarının başlıcaları: Smith-Magenis (17p11.2 delesyonu), Williams sendromu (7q11.23 delesyonu), DiGeorge / Velokardiyofasiyal sendrom (22q11.2 delesyonu), Prader-Willi ve Angelman sendromlarıdır (15q11-q13 delesyonu). Bu sendromlar spesifik dismorfik yüz bulguları, konjenital kalp defektleri ve davranışsal bozukluklarla karakterizedir.",
                "keyBullets": [
                    {"title": "Mikrodelesyon Doğası", "desc": "Klasik karyotipte görülemeyen, FISH veya microarray ile saptanan submikroskobik kayıplardır.", "isKey": True},
                    {"title": "Oluşum Mekanizması", "desc": "Düşük kopya tekrarları (LCR) arasında eşit olmayan krossing-over (NAHR) ile oluşur.", "isKey": True},
                    {"title": "Klasik Örnekler", "desc": "DiGeorge (22q11.2), Williams (7q11.23), Smith-Magenis (17p11.2) ve PWS/AS (15q11-q13).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Sendrom Adı", "Kromozomal Bölge", "Anomali Tipi (Delesyon/Duplikasyon)"],
                    [
                        [("DiGeorge Sendromu", False, ""), ("22q11.2 bölgesi", True, "Farinks poş defekti delesyonu"), ("Mikrodelesyon", False, "")],
                        [("Cat-Eye (Kedi Gözü)", False, ""), ("22q11 bölgesi", True, "22q11 artış tablosu"), ("Duplikasyon", False, "")],
                        [("Williams Sendromu", False, ""), ("7q11.23 bölgesi", True, "Elastin geni delesyonu"), ("Mikrodelesyon", False, "")],
                        [("Smith-Magenis", False, ""), ("17p11.2 bölgesi", True, "RAI1 delesyonu"), ("Mikrodelesyon", False, "")],
                        [("Charcot-Marie-Tooth Tip 1A", False, ""), ("17p12 bölgesi", True, "PMP22 dozaj artışı"), ("Duplikasyon", False, "")],
                        [("Herediter Nöropati (HNPP)", False, ""), ("17p12 bölgesi", True, "PMP22 delesyonu"), ("Mikrodelesyon", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdaki klinik tablolardan hangisi mikrodelesyon değil, submikroskobik bir duplikasyon sendromudur?",
                    {
                        "A": "DiGeorge sendromu (22q11.2)",
                        "B": "Smith-Magenis sendromu (17p11.2)",
                        "C": "Williams sendromu (7q11.23)",
                        "D": "Charcot-Marie-Tooth Tip 1A (17p12)",
                        "E": "Cri du chat sendromu (5p15)"
                    },
                    "D",
                    {
                        "A": "DiGeorge tipik bir mikrodelesyondur.",
                        "B": "Smith-Magenis 17p11.2 delesyonudur.",
                        "C": "Williams 7q11.23 delesyonudur.",
                        "D": "Doğru cevap D'dir: CMT-1A 17p12 bölgesindeki PMP22 geni duplikasyonu ile ortaya çıkar.",
                        "E": "Cri du chat terminal delesyondur."
                    }
                ),
                make_active_recall(
                    "Aynı kromozomal bölge olan 22q11'in delesyonunda DiGeorge sendromu gelişirken, duplikasyonunda hangi sendrom ortaya çıkar?",
                    "Cat-Eye (Kedi Gözü) Sendromu ortaya çıkar.",
                    "22q11 duplikasyon sendromu"
                )
            ],
            "spotPearls": [
                "Mikrodelesyonlar ışık mikroskobunda görülmez; FISH ve Kromozomal Mikroarray (CMA) ile saptanır.",
                "Charcot-Marie-Tooth 1A 17p12 duplikasyonu; HNPP ise 17p12 delesyonudur.",
                "22q11.2 delesyonu DiGeorge sendromuna, duplikasyonu ise Cat-Eye sendromuna yol açar."
            ]
        },

        # Slayt 15
        {
            "title": "Duplikasyonlar (Parsiyel Trizomiler) ve Eşit Olmayan Krossing-Over",
            "subtitle": "Kromozomal Segment Fazlalıkları ve NAHR Mekaniği",
            "badge": "Duplikasyon Mekaniği",
            "coreContent": {
                "text": "Duplikasyon, bir kromozom segmentinin normal kopyasının yanına ek bir kopyasının daha eklenmesiyle karakterize dengesiz bir yapısal anomalidir; sitogenetik olarak parsiyel trizomi olarak sınıflandırılır. Duplikasyonlar genellikle mayoz I profazında, homolog kromozomlar üzerinde bulunan homoloji gösteren düşük kopya tekrarlarının (LCR) yanlış hizalanması ve aralarında gerçekleşen eşit olmayan krossing-over (alelik olmayan homolog rekombinasyon - NAHR) sonucunda meydana gelir. Bu süreçte krossing-overa katılan kromatitlerden birinde duplikasyon (genetik materyal fazlalığı) oluşurken, diğer resiprokal kromatitte eş zamanlı delesyon (genetik materyal kaybı) gelişir. Genel bir genetik kural olarak, duplikasyonların klinik fenotipik etkisi delesyonlara kıyasla belirgin derecede daha hafiftir; çünkü insan hücreleri genetik materyal fazlalığını, materyal eksikliğine (haploinsüfisyens) göre çok daha iyi tolere eder.",
                "keyBullets": [
                    {"title": "Parsiyel Trizomi", "desc": "Kromozom segmentinin duplikasyonu bir bölge için üç kopya (trizomi) etkisi doğurur.", "isKey": True},
                    {"title": "Eşit Olmayan Krossing-Over", "desc": "Mayozda LCR'lerin yanlış hizalanması bir duplikasyon ve bir delesyon ürünü verir.", "isKey": True},
                    {"title": "Tolerans Prensibi", "desc": "Genetik materyal fazlalığı (duplikasyon), eksikliğine (delesyon) göre daha hafif seyreder.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Delesyon vs Duplikasyon Klinik Toleransı",
                    "Delesyon (Parsiyel Monozomi)",
                    "Gen dozu %50'ye düşer; haploinsüfisyens nedeniyle embriyonik letalite ve çok ağır fenotipik malformasyonlar sıktır.",
                    "Duplikasyon (Parsiyel Trizomi)",
                    "Gen dozu %150'ye çıkar; hücre fazlalığı daha iyi tolere eder, fenotipik etkiler delesyona göre belirgin derecede hafiftir."
                ),
                make_causal_chain(
                    "Eşit Olmayan Krossing-Over ve Duplikasyon Oluşumu",
                    [
                        "1. Mayoz I profazında homolog kromozomlardaki düşük kopya tekrarları yanlış hizalanır",
                        "2. Yanlış hizalanmış bölgeler arasında alelik olmayan homolog rekombinasyon (NAHR) gerçekleşir",
                        "3. Resiprokal kromatitlerden biri çift segment alırken diğeri segmentini tamamen kaybeder",
                        "4. Döllenme sonucu bir kromatit duplikasyon (CMT-1A), diğeri delesyon (HNPP) ürünü doğurur"
                    ]
                ),
                make_cloze(
                    "Mayozda eşit olmayan krossing-over gerçekleştiğinde rekombinant kromatitlerden birinde duplikasyon oluşurken diğerinde delesyon meydana gelir.",
                    "delesyon",
                    "Resiprokal kayıp ürününü anımsayınız"
                )
            ],
            "spotPearls": [
                "Duplikasyonlar parsiyel trizomidir ve klinik etkileri delesyona göre daha hafiftir.",
                "Eşit olmayan krossing-over aynı anda bir duplikasyon ve bir delesyon ürünü çıkarır.",
                "Genetik materyal fazlalığı hücre tarafından eksikliğe göre daha iyi tolere edilir."
            ]
        },

        # Slayt 16
        {
            "title": "İnversiyonlar: Parasentrik ve Perisentrik Dinamikler",
            "subtitle": "Kromozomal Segmentlerin 180° Dönüşü ve Dengeli Yapı",
            "badge": "İnversiyon Biyolojisi",
            "coreContent": {
                "text": "İnversiyon, tek bir kromozom üzerinde iki kırık meydana gelmesi, kırılan segmentin kendi ekseni etrafında 180 derece dönerek ters yönde yeniden birleşmesi ile karakterize dengeli bir yapısal anomalidir. Genetik materyal miktarı net olarak değişmediği için inversiyon taşıyıcıları fenotipik olarak tamamen normaldir. İnversiyonlar sentromerin dönen segmentin içinde kalıp kalmamasına göre ikiye ayrılır: Parasentrik inversiyonlarda her iki kırık da aynı koldadır ve ters dönen segment sentromeri içermez (kromozomun kol uzunluk oranı ve morfolojisi değişmez). Perisentrik inversiyonlarda ise kırıkların biri kısa kolda (p), diğeri uzun kolda (q) yer alır ve dönen segment sentromeri içerir. Perisentrik inversiyonlar sentromerin yerini değiştirdiği için kromozomun kol oranını ve morfolojik tipini (örneğin submetasentrik bir kromozomu metasentriğe) dönüştürebilir.",
                "keyBullets": [
                    {"title": "Dengeli Doğası", "desc": "Materyal kaybı veya kazanımı yoktur; taşıyıcı fenotipik olarak sağlıklıdır.", "isKey": True},
                    {"title": "Parasentrik İnversiyon", "desc": "Kırıklar tek bir koldadır; sentromeri İÇERMEZ, kromozom morfolojisi değişmez.", "isKey": True},
                    {"title": "Perisentrik İnversiyon", "desc": "Kırıklar p ve q kollarındadır; sentromeri İÇERİR, kol oranını değiştirebilir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["İnversiyon Tipi", "Kırık Sayısı ve Kolları", "Sentromer Durumu", "Kromozom Şekil Değişimi"],
                    [
                        [("Parasentrik", False, ""), ("Aynı kol üzerinde 2 kırık", False, ""), ("Sentromer segment İÇİNDE DEĞİL", True, "Sentromer hariç"), ("Kol oranı ve sentromer yeri değişmez", False, "")],
                        [("Perisentrik", False, ""), ("Biri p kolunda, biri q kolunda 2 kırık", False, ""), ("Sentromer segment İÇİNDE YER ALIR", True, "Sentromer dahil"), ("Sentromer yeri ve kol oranı değişebilir", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Kromozomun kısa kolunda bir, uzun kolunda bir kırık meydana gelmesi ve aradaki sentromeri içeren parçanın 180 derece dönerek yeniden birleşmesiyle oluşan yapısal anomali hangisidir?",
                    {
                        "A": "Parasentrik inversiyon",
                        "B": "Perisentrik inversiyon",
                        "C": "Robertsonian translokasyon",
                        "D": "İzokromozom",
                        "E": "Terminal delesyon"
                    },
                    "B",
                    {
                        "A": "Parasentrik inversiyon sentromeri içermez.",
                        "B": "Doğru cevap B'dir: Sentromeri içeren ve her iki kola uzanan inversiyon perisentrik inversiyondur.",
                        "C": "Translokasyon iki farklı kromozom arasındadır.",
                        "D": "İzokromozom tek kolun çiftlenmesidir.",
                        "E": "Delesyonda parça kaybı vardır."
                    }
                ),
                make_cloze(
                    "Ters dönen kromozom segmentinin sentromeri içermediği ve kırıkların aynı kolda olduğu inversiyon tipine parasentrik inversiyon denir.",
                    "parasentrik",
                    "Sentromersiz inversiyon tipini anımsayınız"
                )
            ],
            "spotPearls": [
                "Parasentrik inversiyon sentromeri İÇERMEZ (aynı koldadır).",
                "Perisentrik inversiyon sentromeri İÇERİR (biri p'de biri q'dadır).",
                "İnversiyon taşıyıcıları dengelidir ve fenotipik olarak sağlıklıdır."
            ]
        },

        # Slayt 17
        {
            "title": "İnversiyon Taşıyıcılarında Gametogenez ve Rekombinasyon Riskleri",
            "subtitle": "İnversiyon İlmeği (Loop) ve Dengesiz Gamet Üretimi",
            "badge": "İnversiyon Rekombinasyonu",
            "coreContent": {
                "text": "İnversiyon taşıyıcıları fenotipik olarak sağlıklı olsalar da, mayoz I profazında homolog kromozomların sinapsis yapabilmesi için kromozomların anormal bir inversiyon ilmeği (inversion loop) oluşturması zorunludur. Eğer bu ilmek bölgesinin içinde bir krossing-over meydana gelirse rekombinasyon ürünleri dengesizleşir. Parasentrik inversiyon ilmeği içindeki krossing-over; bir adet iki sentromerli (disentrik) kromatit ve bir adet hiç sentromeri olmayan (asentrik) kromatit üretir. Anafazda asentrik parça iğ ipliğine tutunamayıp kaybolurken, disentrik kromatit iki kutup arasında köprü oluşturarak parçalanır; bu aşırı dengesiz ürünler tamamen letaldir ve canlı doğuma ulaşamaz (tekrarlayan düşük veya infertilite yapar). Perisentrik inversiyon ilmeği içindeki krossing-overda ise oluşan kromatitlerin her biri birer sentromere sahiptir ancak segmental delesyon ve duplikasyon taşırlar; bu dengesiz gametler yaşayabilir ve çoklu konjenital anomalili bebek doğumuna yol açabilir.",
                "keyBullets": [
                    {"title": "İnversiyon İlmeği", "desc": "Mayozda homolog bölgelerin eşleşebilmesi için ilmek yapısı kurulması zorunludur.", "isKey": True},
                    {"title": "Parasentrik Rekombinasyon", "desc": "Disentrik ve asentrik kromatitler üretir; mutlak letaldir, canlı doğamaz.", "isKey": True},
                    {"title": "Perisentrik Rekombinasyon", "desc": "Delesyonlu ve duplikasyonlu kromatitler üretir; anomalili canlı doğum riski taşır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Parasentrik vs Perisentrik İlmek İçi Krossing-Over Sonuçları",
                    "Parasentrik Krossing-Over",
                    "Disentrik (iki sentromerli) ve asentrik (sentromersiz) parçalar oluşur; mitozda parçalanır, mutlak letaldir, canlı doğum olmaz.",
                    "Perisentrik Krossing-Over",
                    "Her kromatit bir sentromer taşır ancak segmental delesyon/duplikasyon içerir; canlı doğabilir, dismorfik bebek riski yüksektir."
                ),
                make_branching_logic(
                    "Perisentrik inversiyon 46,XX,inv(9)(p12q13) taşıyıcısı olduğu bilinen bir kadının prenatal genetik danışmanlığında, fetüste ortaya çıkabilecek olası dengesiz rekombinant ürünlerin biyolojik mekanizması nasıl ifade edilmelidir?",
                    [
                        {"text": "Mayoz sırasında inversiyon ilmeği içinde krossing-over gerçekleşirse kromatitlerde duplikasyon ve delesyon kombinasyonları oluşarak anomalili canlı doğum riski doğabilir", "isCorrect": True, "feedback": "Kusursuz genetik açıklama! Perisentrik inversiyon rekombinantları tek sentromerli ancak delesyon/duplikasyonlu olup canlı doğabilir."},
                        {"text": "Perisentrik inversiyonlarda asla krossing-over gerçekleşemez, tüm çocuklar mutlaka %100 sağlıklı ve normal karyotipli doğacaktır", "isCorrect": False, "feedback": "İlmek içinde rekombinasyon gerçekleşebilir ve dengesiz gamet riski mevcuttur."},
                        {"text": "Oluşacak tüm ürünler istisnasız iki sentromerli (disentrik) olacağı için asla gebelik oluşamaz", "isCorrect": False, "feedback": "Disentrik kromatitler perisentrik değil parasentrik inversiyon rekombinasyonunda görülür."}
                    ]
                ),
                make_active_recall(
                    "Parasentrik inversiyon ilmeği içinde krossing-over gerçekleştiğinde ortaya çıkan asentrik ve disentrik kromatitlerin klinik akıbeti nedir?",
                    "Hücre bölünmesinde parçalanıp kayboldukları için mutlak letaldir; canlı doğuma ulaşamaz, gebelik kaybına yol açar.",
                    "Disentrik/asentrik mutlak letalite"
                )
            ],
            "spotPearls": [
                "Parasentrik rekombinasyon = Disentrik + asentrik kromatit (mutlak letal, canlı doğmaz).",
                "Perisentrik rekombinasyon = Delesyon + duplikasyonlu kromatit (anomalili canlı doğum mümkündür).",
                "İnv(9) polimorfizmi popülasyonda sık görülen normal bir varyanttır."
            ]
        },

        # Slayt 18
        {
            "title": "Halka (Ring) Kromozomlar ve İzokromozom Mekanizmaları",
            "subtitle": "Kromozom Uç Füzyonları ve Transvers Sentromer Bölünmesi",
            "badge": "Ring ve İzokromozom",
            "coreContent": {
                "text": "Ring (halka) kromozomlar, bir kromozomun hem kısa (p) hem uzun (q) kolunun uç kısımlarında iki kırık meydana gelmesi, telomerik distal parçaların kaybolması ve yapışkan kırık uçların dairesel olarak birbiriyle kaynaşması sonucu oluşur. En sık X kromozomunda (r(X)) görülür. Ring kromozomlar mitoz bölünme sırasında kromatit düğümlenmeleri ve eşit olmayan dağılımlar nedeniyle ileri derecede kararsızdır (mitotik instabilite); bu durum ring kromozom taşıyıcılarında hızla mozaik hücre hatlarının (örneğin 45,X / 46,X,r(X)) gelişmesine yol açar. İzokromozom ise sentromerin normal longitudinal (boyuna) eksende ayrılması yerine transvers (enine) eksende hatalı bölünmesi sonucu oluşur. Bir kolun tamamen kaybı ve diğer kolun iki kopyasının ayna görüntüsü şeklinde birleşmesiyle meydana gelir. Böylece hücre bir kol için tam monozomi, diğer kol için tam trizomi haline gelir. İnsanlarda en sık rastlanan izokromozom, Turner sendromu olgularının %15'inde saptanan i(Xq) karyotipidir.",
                "keyBullets": [
                    {"title": "Ring Kromozom", "desc": "İki uç kırık sonrası halkalaşmadır; mitotik instabilite nedeniyle sıklıkla mozaiktir.", "isKey": True},
                    {"title": "İzokromozom Mekanizması", "desc": "Sentromerin transvers (enine) bölünmesiyle oluşan ayna simetrisi kopyalanmasıdır.", "isKey": True},
                    {"title": "En Sık İzokromozom", "desc": "i(Xq) karyotipidir; Turner sendromunun yaklaşık %15'ini oluşturur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "İzokromozom i(Xq) Oluşum Zinciri",
                    [
                        "1. Mayoz veya erken mitoz bölünmede sentromer normal boyuna eksen yerine transvers eksende bölünür",
                        "2. X kromozomunun kısa kolu (p) tamamen koparak sitoplazmada kaybolur",
                        "3. İki uzun kol (q) ayna simetrisiyle sentromerde birleşerek tek bir izokromozom kurar",
                        "4. Bireyde Xp monozomisi ve Xq trizomisi gelişerek Turner sendromu fenotipi ortaya çıkar"
                    ]
                ),
                make_cloze(
                    "Sentromerin transvers bölünmesi sonucu bir kolun kaybı ve diğer kolun ayna simetrisiyle çiftlenmesiyle oluşan kromozom tipine izokromozom denir.",
                    "izokromozom",
                    "Ayna simetrili anormal kromozom terimini anımsayınız"
                ),
                make_micro_quiz(
                    "Turner sendromlu bireylerde klasik 45,X karyotipinden sonra yaklaşık %15 sıklıkla en sık görülen yapısal kromozom anomalisi hangisidir?",
                    {
                        "A": "X kromozomu uzun kol izokromozomu [i(Xq)]",
                        "B": "X kromozomu kısa kol izokromozomu [i(Xp)]",
                        "C": "Ring X kromozomu [r(X)]",
                        "D": "X-otozom resiprokal translokasyonu",
                        "E": "X kromozomu tam trizomisi"
                    },
                    "A",
                    {
                        "A": "Doğru cevap A'dır: Turner sendromunda en sık yapısal varyant uzun kol izokromozomudur [46,X,i(Xq)].",
                        "B": "i(Xp) çok daha nadirdir.",
                        "C": "Ring X daha nadir bir varyanttır.",
                        "D": "X-otozom translokasyonları nadirdir.",
                        "E": "Trizomi X Turner değil Triple X sendromudur."
                    }
                )
            ],
            "spotPearls": [
                "İzokromozom sentromerin transvers bölünmesiyle oluşur: bir kol monozomik, diğeri trizomiktir.",
                "En sık izokromozom i(Xq)'dur ve Turner sendromu olgularının %15'ini oluşturur.",
                "Ring kromozomlar mitotik instabilite sergiler ve sıklıkla mozaisizmle seyreder."
            ]
        },

        # Slayt 19 (CHECKPOINT 2)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Yapısal Kromozom Anomalileri ve Kırık-Birleşme Mekanizmaları",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 2",
            "coreContent": {
                "text": "Bu bölümde yapısal kromozom anomalilerinin mekanizmalarını ve tiplerini inceledik. Yapısal anomaliler 1/375 yenidoğanda görülür. Delesyonlar (parsiyel monozomi) terminal (tek kırık; Cri du chat 5p15) ve interstisyel (çift kırık; DiGeorge 22q11.2) olarak ayrılır; patogenetik temel haploinsüfisyenstir. Duplikasyonlar (parsiyel trizomi) eşit olmayan krossing-overla oluşur ve delesyona göre daha iyi tolere edilir; mikrodelesyon ve mikroduplikasyonlar FISH veya microarray ile tanınır. İnversiyonlar sentromer içermeyen parasentrik ve sentromer içeren perisentrik olarak ikiye ayrılır; parasentrik krossing-over mutlak letal asentrik/disentrik ürünler verirken, perisentrik krossing-over anomalili canlı doğabilecek delesyon/duplikasyon ürünleri üretir. İzokromozom transvers sentromer bölünmesiyle oluşur ve en sık örneği Turner sendromundaki i(Xq)'dur. Ring kromozomlar ise uç kırıkların kaynaşmasıyla oluşur ve mitotik instabilite nedeniyle mozaisizm gösterir.",
                "keyBullets": [
                    {"title": "Delesyon Tipleri", "desc": "Terminal (Cri du chat 5p15) ve İnterstisyel (DiGeorge 22q11.2); haploinsüfisyens temeldir.", "isKey": True},
                    {"title": "İnversiyon Rekombinasyonu", "desc": "Parasentrik letal asentrik/disentrik; perisentrik canlı doğabilen delesyon/duplikasyon verir.", "isKey": True},
                    {"title": "İzokromozom Esası", "desc": "Transvers bölünme; tek kol monozomi, diğer kol trizomi (en sık i(Xq) Turner'da).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Anomali Tipi", "Mekanizma / Özellik", "Klinik Prototip"],
                    [
                        [("Terminal Delesyon", False, ""), ("Tek kırık, uç bölge kaybı", True, "Uç bölge eksilmesi"), ("Cri du chat sendromu (5p15)", False, "")],
                        [("İnterstisyel Delesyon", False, ""), ("Çift kırık, iç segment kaybı", True, "Ara segment kaybı"), ("DiGeorge sendromu (22q11.2)", False, "")],
                        [("Perisentrik İnversiyon", False, ""), ("Sentromer segment içinde", True, "Sentromerli 180 derece dönüş"), ("Anomalili canlı doğum riski", False, "")],
                        [("İzokromozom", False, ""), ("Sentromerin transvers bölünmesi", True, "Enine sentromer kırılması"), ("i(Xq) Turner Sendromu (%15)", False, "")]
                    ]
                ),
                make_active_recall(
                    "Neden perisentrik inversiyon taşıyıcılarının anomalili çocuk sahibi olma riski parasentrik inversiyon taşıyıcılarına göre daha yüksektir?",
                    "Çünkü perisentrik krossing-over ürünleri tek sentromerli olup yaşayabilirken, parasentrik ürünler asentrik/disentrik olup erken letaliteyle elenir.",
                    "Tek sentromer ve canlı kalabilme potansiyeli"
                ),
                make_cloze(
                    "İzokromozom oluşumunda sentromer normal boyuna eksen yerine transvers eksende bölünür.",
                    "transvers",
                    "Enine bölünme doğrultusunu anımsayınız"
                )
            ],
            "spotPearls": [
                "Yapısal anomali sıklığı yenidoğanlarda yaklaşık 1/375'tir.",
                "Haploinsüfisyens delesyon sendromlarının temel mekanizmasıdır.",
                "En sık izokromozom i(Xq)'dur; Turner sendromunun %15'ini oluşturur."
            ]
        },

        # Slayt 20
        {
            "title": "Süpernümerer Marker Kromozomlar (sSMC) ve Klinik Değerlendirme",
            "subtitle": "Sitogenetik Olarak Tanımlanamayan Ekstra Küçük Parçalar",
            "badge": "Marker Kromozomlar",
            "coreContent": {
                "text": "Süpernümerer küçük marker kromozomlar (sSMC), geleneksel G-bantlama sitogenetik analizinde bant paterni net olarak çözülemeyen, normal 46 kromozoma ek olarak bulunan küçük yapısal kromozomal anomalilerdir (karyotipte +mar olarak belirtilir). Prenatal tanıda de novo saptanma sıklığı yaklaşık 1/2500'dür. Marker kromozomlar genellikle mozaik formda bulunurlar. Bir marker kromozomun embriyo üzerindeki klinik ve fenotipik etkisi; hangi kromozomdan köken aldığına, aktif genetik materyal içerip içermediğine ve hücrelerdeki mozaisizm oranına bağlı olarak sessiz bir polimorfizmden ağır zekâ geriliği ve çoklu malformasyonlara kadar geniş bir yelpazede değişir. Marker kromozomların büyük çoğunluğu akrosentrik kromozomlardan (özellikle 15. kromozom) ve cinsiyet kromozomlarından köken alır. Fetal karyotipte bir marker saptandığında orijinini belirlemek amacıyla mutlaka FISH veya Kromozomal Mikroarray (CMA) analizi yapılmalıdır.",
                "keyBullets": [
                    {"title": "Marker Kromozom Tanımı", "desc": "Bantlama ile tanımlanamayan, ek olarak bulunan küçük kromozomlardır (+mar).", "isKey": True},
                    {"title": "En Sık Köken", "desc": "Genellikle 15. kromozom ve gonozomlardan (X ve Y) köken alırlar.", "isKey": True},
                    {"title": "İleri Analiz Gereksinimi", "desc": "Klinik riskin belirlenmesi için kökenin FISH veya CMA ile aydınlatılması şarttır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_branching_logic(
                    "32 yaşında primigravid bir gebenin amniyosentez sonucunda fetal karyotip 47,XY,+mar [12] / 46,XY [18] şeklinde mozaik küçük süpernümerer marker kromozom olarak raporlanıyor. Genetik konseyinde bu bulgunun fetal prognozunu belirlemek için atılacak en doğru adım ne olmalıdır?",
                    [
                        {"text": "Marker kromozomun hangi kromozomdan köken aldığını ve fonksiyonel gen içeriğini belirlemek için acilen moleküler sitogenetik (FISH veya Kromozomal Mikroarray) çalışması yapılmalıdır", "isCorrect": True, "feedback": "Kusursuz klinik genetik yaklaşımı! Marker kromozomların klinik etkisi ancak içerdiği genler ve ebeveyn kökeni aydınlatılarak öngörülebilir."},
                        {"text": "Marker kromozomlar her zaman selimdir, hiçbir ileri teste gerek duyulmadan gebelik rutin takibe alınmalıdır", "isCorrect": False, "feedback": "Marker kromozomlar aktif gen içeriyorsa ağır sendromlara yol açabilir."},
                        {"text": "Sonuç kesinlikle mutlak letal bir trizomidir, derhal gebelik sonlandırılmalıdır", "isCorrect": False, "feedback": "Köken belirlenmeden gebeliğin prognozu bilinemez; heterokromatik markerlar tamamen zararsız da olabilir."}
                    ]
                ),
                make_cloze(
                    "Prenatal sitogenetikte saptanan süpernümerer marker kromozomların en sık köken aldığı otozom 15 numaralı kromozomdur.",
                    "15",
                    "En sık marker kromozom otozomunu anımsayınız"
                ),
                make_active_recall(
                    "Geleneksel karyotip analizinde tanımlanamayan bir marker kromozomun genetik içeriğini ve kökenini aydınlatmak için hangi ileri genetik yöntemler kullanılır?",
                    "Kromozomal Mikroarray (CMA / aCGH) ve hedefe yönelik FISH analizleri kullanılır.",
                    "Moleküler sitogenetik tanı araçları"
                )
            ],
            "spotPearls": [
                "Marker kromozomlar (+mar) standart bantlama ile tanınamayan ekstra küçük kromozomlardır.",
                "En sık 15. kromozom ve cinsiyet kromozomlarından köken alırlar.",
                "Marker saptandığında prognoz tayini için FISH veya Kromozomal Mikroarray (CMA) zorunludur."
            ]
        }
    ]
