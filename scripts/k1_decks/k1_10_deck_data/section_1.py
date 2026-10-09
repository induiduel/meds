"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 1 (Slayt 1 - 10)
Konu: Sitogenetik Temeller, Kromozomal Anomalilerin Sınıflandırılması ve Anöploidi Mekanizmaları
Checkpoint: Slayt 9 ([TEKRAR SAYFASI - CHECKPOINT 1])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_1_slides():
    return [
        # Slayt 1
        {
            "title": "İnsan Genom Organizasyonu: Normal Karyotip ve Sitogenetik Esaslar",
            "subtitle": "Hücresel Genetik Mimari ve Kromozomal Düzen",
            "badge": "Genetik Temeller",
            "coreContent": {
                "text": "İnsan somatik hücrelerinde genetik materyal, **diploid sayıda (2n=46)** kromozom olarak organize olmuştur. Kromozomal mimari mikroskobik düzeyde şu temel ilkelerle incelenir:\n\n"
                        "- **Kromozom Dağılımı:** Toplam 46 kromozom; 22 çift homolog otozom ve 1 çift gonozomdan (dişide XX, erkekte XY) oluşur.\n"
                        "- **Morfolojik Yapı:** Her kromozom sentromer (primer boğum) ile kısa (**p; petit**) ve uzun (**q; queue**) kollara ayrılır.\n"
                        "- **Sentromerik Sınıflandırma:** Kolların boy oranına göre **metasentrik**, **submetasentrik** ve **akrosentrik** olmak üzere 3 morfolojik gruba ayrılır.\n"
                        "- **Akrosentrik Özellik:** 13, 14, 15, 21 ve 22 numaralı kromozomların kısa kolları ribozomal RNA (rRNA) genlerini barındıran satellit ve sap yapıları taşır.\n\n"
                        "> [!NOTE]\n"
                        "> Rutin sitogenetik analiz, hücre döngüsünün **metafaz** evresinde kromatinin maksimum kondanse olmasıyla Giemsa (G-bantlama) yöntemi kullanılarak gerçekleştirilir.",
                "keyBullets": [
                    {"title": "Diploid Kromozom Sayısı", "desc": "İnsan somatik hücrelerinde 46 kromozom (44 otozom + 2 gonozom) bulunur.", "isKey": True},
                    {"title": "Kromozom Kolları", "desc": "Sentromer ile ayrılan kısa kol 'p', uzun kol 'q' olarak adlandırılır.", "isKey": False},
                    {"title": "Akrosentrik Kromozomlar", "desc": "13, 14, 15, 21 ve 22 numaralı kromozomlar satellitli kısa kollara sahiptir.", "isKey": True}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "İnsan somatik hücrelerinde normal karyotip diploid sayıda olup 46 kromozom içerir.",
                    "46",
                    "İnsan somatik kromozom adedini düşününüz"
                ),
                make_table(
                    ["Kromozom Tipi", "Sentromer Konumu", "Kol Oranı Özelliği"],
                    [
                        [("Metasentrik", False, ""), ("Kromozomun tam ortasında", True, "Merkezi yerleşim"), ("p ve q kolları yaklaşık eşit uzunluktadır", False, "")],
                        [("Submetasentrik", False, ""), ("Merkezden belirgin derecede uzakta", True, "Asimetrik yerleşim"), ("p kolu q koluna göre fark edilir derecede kısadır", False, "")],
                        [("Akrosentrik", False, ""), ("Uca çok yakın lokalize", True, "Uçsal primer boğum"), ("Kısa kolda satellit ve rRNA genleri yer alır", False, "")]
                    ]
                ),
                make_active_recall(
                    "İnsan karyotipinde satellitli kısa kollara sahip akrosentrik kromozomlar hangileridir?",
                    "13, 14, 15, 21 ve 22 numaralı kromozomlardır.",
                    "D ve G grubu akrosentrik kromozomlar"
                )
            ],
            "spotPearls": [
                "Normal insan somatik karyotipi 46 kromozomdur (dişide 46,XX, erkekte 46,XY).",
                "Akrosentrik kromozomlar 13, 14, 15, 21 ve 22'dir; kısa kolları rRNA ve satellit içerir.",
                "Sitogenetik analiz rutin olarak metafaz kromozomlarına uygulanan G-bantlama ile yapılır."
            ]
        },

        # Slayt 2
        {
            "title": "Kromozom Anomalilerinin Sınıflandırılması: Sayısal ve Yapısal Ayrım",
            "subtitle": "Kromozomal Bozuklukların Genomik Tipolojisi",
            "badge": "Genomik Sınıflandırma",
            "coreContent": {
                "text": "Kromozom anomalileri, genomik etkilenmenin biçimine göre iki ana kategoriye ayrılır:\n\n"
                        "- **Sayısal (Nümerik) Anomaliler:** Diploid sayıdan (2n=46) sapmalardır. Haploid takımın tam katları şeklindeki değişimlere **öploidi / poliploidi** (triploidi 69, tetraploidi 92); tam katı olmayan tekil kazanım veya kayıplara ise **anöploidi** (trizomi, monozomi) denir.\n"
                        "- **Yapısal (Strüktürel) Anomaliler:** Kromozom kırıkları ve hatalı onarımlar sonucu oluşur. Delesyon, duplikasyon, inversiyon, translokasyon, izokromozom ve halka (ring) kromozomları kapsar.\n\n"
                        "> [!IMPORTANT]\n"
                        "> Tüm canlı doğumların yaklaşık **%1'inde** klinik olarak belirgin bir kromozomal anomali saptanır; bu anomaliler konjenital malformasyonların ve zihinsel yetersizliğin önde gelen nedenleridir.",
                "keyBullets": [
                    {"title": "Sayısal Anomaliler", "desc": "Kromozom adedindeki değişimlerdir; öploidi (poliploidi) veya anöploidi şeklinde görülür.", "isKey": True},
                    {"title": "Yapısal Anomaliler", "desc": "Kromozom kırıkları ve anormal birleşmeler sonucu oluşan mimari bozukluklardır.", "isKey": True},
                    {"title": "Canlı Doğum İnsidansı", "desc": "Tüm canlı doğumların yaklaşık %1'inde majör bir kromozomal anomali mevcuttur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Sayısal vs Yapısal Kromozom Anomalileri",
                    "Sayısal Anomaliler",
                    "Kromozom adedinde değişiklik (anöploidi/poliploidi); mayotik veya mitotik ayrılma hatalarından kaynaklanır.",
                    "Yapısal Anomaliler",
                    "Kromozom morfolojisi ve diziliminde değişiklik; DNA çift zincir kırıkları ve hatalı rekombinasyonla oluşur."
                ),
                make_micro_quiz(
                    "Tüm canlı doğumlar göz önüne alındığında, klinik öneme sahip kromozomal bozuklukların genel insidansı yaklaşık ne kadardır?",
                    {
                        "A": "Canlı doğumların yaklaşık %0.01'i",
                        "B": "Canlı doğumların yaklaşık %1'i",
                        "C": "Canlı doğumların yaklaşık %10'u",
                        "D": "Canlı doğumların yaklaşık %25'i",
                        "E": "Canlı doğumların yaklaşık %50'si"
                    },
                    "B",
                    {
                        "A": "Bu oran çok düşüktür; kromozom anomalileri nadir değildir.",
                        "B": "Doğru cevap B'dir: Canlı doğan bebeklerin yaklaşık %1'inde klinik anlamlı sayısal veya yapısal kromozomal anomali saptanır.",
                        "C": "Canlı doğum için çok yüksektir; bu oran spontan abortuslara yaklaşır.",
                        "D": "Kromozomal bozuklukların canlı doğum oranı %25 olamaz.",
                        "E": "Canlı doğumda imkansız bir orandır."
                    }
                ),
                make_active_recall(
                    "Kromozom anomalilerinin en yaygın klinik tipi nedir ve fenotipik etkisi nasıldır?",
                    "En yaygın tip anöploididir; daima fiziksel malformasyonlar ve/veya zihinsel gerilikle seyreder.",
                    "Sayısal sapmalar ve nörogelişimsel fenotip"
                )
            ],
            "spotPearls": [
                "Canlı doğumların yaklaşık %1'i kromozomal bir sendromla doğar.",
                "En sık klinik anomali tipi anöploididir ve her zaman zihinsel/fiziksel fenotipik etkiler doğurur.",
                "Sayısal anomaliler anöploidi ve poliploidi, yapısal anomaliler ise dengeli ve dengesiz olarak alt gruplara ayrılır."
            ]
        },

        # Slayt 3
        {
            "title": "Dengeli ve Dengesiz Kromozom Anomalileri: Gen Dozajı Prensibi",
            "subtitle": "Kromozomal Dengesizliklerin Klinik ve Fenotipik Yansımaları",
            "badge": "Gen Dozajı",
            "coreContent": {
                "text": "Yapısal anomaliler, net genetik materyal dengesine göre ikiye ayrılır:\n\n"
                        "- **Dengeli (Balanslı) Anomaliler:** Parçalar yer değiştirmiş olsa da net kayıp veya kazanç yoktur (resiprokal translokasyon, inversiyon). Taşıyıcı bireyler fenotipik olarak tamamen sağlıklıdır; ancak kırık noktası fonksiyonel bir genin içinden geçerse istisnai olarak hastalık oluşabilir.\n"
                        "- **Dengesiz (Anbalanslı) Anomaliler:** Net gen kaybı (delesyon) veya kazancı (duplikasyon) mevcuttur. Gen dozajının bozulması kaçınılmaz olarak çoklu organ anomalilerine ve gelişim geriliğine yol açar.\n\n"
                        "> [!WARNING]\n"
                        "> Dengeli taşıyıcıların en kritik klinik riski, mayozda kromatit ayrılması sırasında **dengesiz gametler** üreterek tekrarlayan düşüklere veya anomalili çocuk doğumuna yol açmalarıdır.",
                "keyBullets": [
                    {"title": "Dengeli Taşıyıcı Fenotipi", "desc": "Genetik materyal kaybı olmadığından taşıyıcı birey genellikle sağlıklıdır.", "isKey": True},
                    {"title": "Gen Dozajı Bozulması", "desc": "Dengesiz anomalilerde gen kazanımı veya kaybı kaçınılmaz olarak patoloji üretir.", "isKey": True},
                    {"title": "Üreme Riski", "desc": "Dengeli taşıyıcılar mayoz sırasında dengesiz gametler üreterek infertilite veya anomalili çocuk riski taşır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "Dengeli kromozom anomalilerinde toplam genetik materyal miktarı korunduğundan taşıyıcı bireylerde genellikle fenotipik etki gözlenmez.",
                    "fenotipik",
                    "Dış görünüş veya klinik tabloyu niteleyen terimi anımsayınız"
                ),
                make_branching_logic(
                    "İnfertilite ve tekrarlayan 3 erken gebelik kaybı öyküsü bulunan fenotipik olarak tamamen sağlıklı bir çift genetik kliniğine başvuruyor. Sitogenetik analizde babada dengeli resiprokal translokasyon 46,XY,t(4;8)(q21;q24) saptanıyor. Çifte verilecek genetik danışmanlıkta temel biyolojik mekanizma nasıl açıklanmalıdır?",
                    [
                        {"text": "Babanın kendisinde net genetik materyal kaybı olmadığı için fenotipi normaldir; ancak mayozda kromatitlerin ayrılması sırasında delesyon ve duplikasyon içeren dengesiz gametler oluşmakta ve embriyolar letal gen dozajı nedeniyle düşmektedir", "isCorrect": True, "feedback": "Kusursuz sitogenetik yaklaşım! Dengeli taşıyıcılarda fenotip normaldir ancak mayotik segregasyon dengesiz gamet ve tekrarlayan abortuslara yol açar."},
                        {"text": "Babadaki translokasyon doğrudan babanın spermatogenezini durdurmuş olup babada ağır zekâ geriliği ve somatik malformasyonlar gelişmesi beklenir", "isCorrect": False, "feedback": "Dengeli translokasyon taşıyıcısında somatik malformasyon veya zekâ geriliği beklenmez."},
                        {"text": "Dengeli translokasyonlar hiçbir şekilde sperm hücrelerine aktarılamaz, tekrarlayan düşüklerin nedeni kesinlikle maternal enfeksiyondur", "isCorrect": False, "feedback": "Translokasyonlar mayozda kuadrivalan oluşturarak dengesiz segregasyonla gametlere aktarılır."}
                    ]
                ),
                make_active_recall(
                    "Dengeli bir translokasyon taşıyıcısında istisnai olarak klinik bir fenotipin veya hastalığın ortaya çıkma mekanizması nedir?",
                    "Kromozomal kırık noktasının aktif ve fonksiyonel bir genin ekzonik/regülatuar bölgesini fiziksel olarak parçalamasıdır.",
                    "Kırık noktası gen inaktivasyonu"
                )
            ],
            "spotPearls": [
                "Dengeli taşıyıcılarda net gen kaybı yoktur, bu nedenle fenotip normaldir.",
                "Dengeli taşıyıcıların ana klinik sorunu tekrarlayan düşükler, infertilite ve sonraki nesilde dengesiz çocuk riskidir.",
                "Yenidoğanlarda dengeli yapısal anomali sıklığı yaklaşık 1/500'dür."
            ]
        },

        # Slayt 4
        {
            "title": "Sayısal Kromozom Anomalilerine Giriş: Öploidi ve Anöploidi",
            "subtitle": "Kromozom Sayım Sapmalarının Sitogenetik Tanımları",
            "badge": "Sayısal Anomaliler",
            "coreContent": {
                "text": "Sayısal kromozom sapmaları iki temel mekanik kategoride sınıflandırılır:\n\n"
                        "- **Öploidi / Poliploidi:** Hücredeki kromozom sayısının haploid takımın (n=23) tam katları şeklinde olmasıdır. İnsan somatik hücresi diploiddir (2n=46). Üç kat artış **triploidi (3n=69)**, dört kat artış **tetraploidi (4n=92)** olarak adlandırılır.\n"
                        "- **Anöploidi:** Haploid sayının katı olmayan tekil kromozom kazanımları veya kayıplarıdır. Diploid takıma bir kromozom eklenmesi **trizomi (2n+1=47)**, bir kromozom eksilmesi ise **monozomi (2n-1=45)** ile sonuçlanır.\n\n"
                        "> [!CRITICAL]\n"
                        "> İnsan türünde **tüm otozomal monozomiler embriyonik letaldir**; yaşamla bağdaşabilen tek tam monozomi gonozomal Turner sendromudur (45,X).",
                "keyBullets": [
                    {"title": "Öploidi / Poliploidi", "desc": "Haploid sayının (n=23) tam katı olan kromozom sayılarıdır (3n=69, 4n=92).", "isKey": True},
                    {"title": "Anöploidi", "desc": "Haploid sayının katı olmayan tekil kromozom kazanımları veya kayıplarıdır (2n+1, 2n-1).", "isKey": True},
                    {"title": "Otozomal Monozomi Kuralı", "desc": "Tüm otozomal monozomiler insanlarda embriyonik letaldir, canlı doğumla bağdaşmaz.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Anomali Sınıfı", "Kromozom Formülü", "İnsan Karyotip Örneği", "Canlı Yaşam Durumu"],
                    [
                        [("Haploidi (Normal)", False, ""), ("n = 23", False, ""), ("23,X veya 23,Y (Gamet)", False, ""), ("Normal gamet hücresi", False, "")],
                        [("Triploidi", False, ""), ("3n = 69", True, "Haploid sayının üç katı"), ("69,XXY veya 69,XXX", False, ""), ("Neredeyse daima letal (%99+)", False, "")],
                        [("Trizomi", False, ""), ("2n + 1 = 47", True, "Tek kromozom fazlalığı"), ("47,XX,+21 (Down)", False, ""), ("Bazı otozomlarda (13,18,21) canlı doğum mümkün", False, "")],
                        [("Monozomi", False, ""), ("2n - 1 = 45", True, "Tek kromozom eksikliği"), ("45,X (Turner Sendromu)", False, ""), ("Yalnızca gonozomal (Turner) canlı doğabilir", False, "")]
                    ]
                ),
                make_active_recall(
                    "İnsan türünde yaşamla bağdaşan, canlı doğumda gözlenebilen tek tam monozomi hangisidir?",
                    "Turner Sendromu (45,X monozomisi) yaşamla bağdaşan tek monozomidir.",
                    "Gonozomal tek X monozomisi"
                ),
                make_cloze(
                    "Hücre çekirdeğindeki kromozom sayısının haploid sayının tam katı şeklinde artışına öploidi veya poliploidi denir.",
                    "öploidi",
                    "Tam katı niteleyen sitogenetik terimi anımsayınız"
                )
            ],
            "spotPearls": [
                "Poliploidi (triploidi, tetraploidi) haploid sayının tam katı artışıdır.",
                "Anöploidi (trizomi, monozomi) tek bir kromozomun eksikliği veya fazlalığıdır.",
                "Turner sendromu (45,X) yaşamla bağdaşan TEK monozomidir; tüm otozomal monozomiler letaldir."
            ]
        },

        # Slayt 5
        {
            "title": "Poliploidiler: Triploidi (69 Kromozom) ve Tetraploidi Dinamikleri",
            "subtitle": "Spontan Abortuslarda Yüksek İnsidans ve Ebeveyn Kökeni Etkileri",
            "badge": "Poliploidi Biyolojisi",
            "coreContent": {
                "text": "Triploidi (3n=69 kromozom), birinci trimester spontan abortuslarının yaklaşık %20'sinden sorumlu ağır bir poliploididir:\n\n"
                        "- **En Sık Mekanizma:** Oositin iki farklı sperm tarafından aynı anda döllenmesidir (**dispermi, ~%66**). Diğer yollar diploid sperm (**diandri**) veya diploid oosit (**digini**) ile döllenmedir.\n"
                        "- **Diandrik Triploidi (Baba Kaynaklı):** Aşırı büyümüş kistik plasenta, trofoblastik hiperplazi ve **parsiyel hidatidiform mol** kliniği ile karakterizedir.\n"
                        "- **Diginik Triploidi (Anne Kaynaklı):** Çok küçük ve fibrotik plasenta ile aşırı belirgin, asimetrik fetal gelişme geriliği sergiler.\n\n"
                        "> [!NOTE]\n"
                        "> Triploid fetüsler son derece nadiren canlı doğabilseler de ilk saatler veya günler içinde çoklu konjenital anomaliler ve solunum yetmezliğinden kaybedilirler.",
                "keyBullets": [
                    {"title": "Triploidi Sıklığı", "desc": "1. trimester spontan düşüklerinin yaklaşık %20'sini oluşturur.", "isKey": True},
                    {"title": "Oluşum Mekanizmaları", "desc": "Dispermi (iki spermle döllenme) en yaygın patogenetik mekanizmadır.", "isKey": True},
                    {"title": "Parental Fenotip Farkı", "desc": "Baba kaynaklı ekstra takımda parsiyel mol, anne kaynaklıda ağır fetal kısıtlanma görülür.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Diandrik Triploidi ve Parsiyel Mol Gelişim Zinciri",
                    [
                        "1. Normal bir haploid oosit iki ayrı haploid sperm tarafından eş zamanlı döllenir (dispermi)",
                        "2. Zigotta 69 kromozomluk (3n) triploid genomik yapı kurulur",
                        "3. Paternal genlerin aşırı ekspresyonu plasental trofoblast proliferasyonunu aşırı uyarır",
                        "4. Makroskopik olarak kistik villus dejenerasyonu ve parsiyel hidatidiform mol tablosu gelişir"
                    ]
                ),
                make_before_after(
                    "Diandrik vs Diginik Triploidi Fenotipleri",
                    "Diandrik Triploidi (Baba Kökenli)",
                    "Aşırı büyümüş kistik plasenta, trofoblastik hiperplazi, parsiyel mol görünümü ve orantısız kranium.",
                    "Diginik Triploidi (Anne Kökenli)",
                    "Çok küçük ve fibrotik plasenta, aşırı şiddetli asimetrik intrauterin gelişme geriliği ve erken embriyonik ölüm."
                ),
                make_cloze(
                    "Bir yumurtanın iki farklı sperm hücresi tarafından eş zamanlı döllenmesi olayına dispermi adı verilir.",
                    "dispermi",
                    "İki spermle fertilizasyon terimini düşününüz"
                )
            ],
            "spotPearls": [
                "Triploidi (69 kromozom) kromozomal kaynaklı erken spontan düşüklerin %20'sini oluşturur.",
                "En sık triploidi nedeni dispermidir (iki spermin tek yumurtayı döllemesi).",
                "Baba kaynaklı triploidide parsiyel mol ve trofoblast hiperplazisi, anne kaynaklıda ise küçük plasenta ve fetal büyüme kısıtlılığı hakimdir."
            ]
        },

        # Slayt 6
        {
            "title": "Spontan Abortuslarda Sitogenetik: Fetal Kayıpların Kromozomal Haritası",
            "subtitle": "Erken Gebelik Kayıplarında Kromozomal Etiyolojinin Ağırlığı",
            "badge": "Fetal Sitogenetik",
            "coreContent": {
                "text": "Birinci trimester spontan abortuslarının en az %50'si sitogenetik anomalilerden kaynaklanır:\n\n"
                        "- **Otozomal Trizomiler (~%50):** Kromozomal düşüklerin yarısını oluşturur. Tek başına en sık saptanan trizomi **Trizomi 16'dır** (%15); mutlak embriyonik letal olup canlı doğumu yoktur.\n"
                        "- **Poliploidiler (~%20):** Özellikle dispermi kaynaklı triploidi (69 kromozom) erken gebelik kayıplarında sık görülür.\n"
                        "- **Monozomi X (~%10):** Tekil anomali bazında düşüklerde en sık saptanan spesifik karyotip **45,X'tir** (Turner sendromu); bu konseptüslerin %95'inden fazlası intrauterin dönemde kaybedilir.\n\n"
                        "> [!CRITICAL]\n"
                        "> Otozomal monozomiler insanlarda o kadar erken ve mutlak letaldir ki gebelik klinik olarak fark edilmeden pre-implantasyon evresinde elenirler.",
                "keyBullets": [
                    {"title": "Düşüklerde Kromozom Anomalisi", "desc": "1. trimester spontan abortuslarının en az %50'si kromozomal bozukluk taşır.", "isKey": True},
                    {"title": "Trizomi 16 Letalitesi", "desc": "Spontan düşüklerde en sık görülen trizomidir, asla canlı doğamaz.", "isKey": True},
                    {"title": "45,X Abortus Oranı", "desc": "Turner karyotipinin %95'ten fazlası intrauterin dönemde spontan düşükle elenir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kromozomal Bozukluk", "Abortuslardaki Yaklaşık Payı", "Canlı Doğum Potansiyeli"],
                    [
                        [("Otozomal Trizomiler (Toplam)", False, ""), ("Tüm kromozomal düşüklerin ~%50'si", True, "En geniş anöploidi payı"), ("13, 18, 21 dışındakiler tamamen letaldir", False, "")],
                        [("Trizomi 16", False, ""), ("Düşüklerdeki en sık tekil trizomi (~%15)", True, "Tekil en sık trizomik abortus"), ("Asla canlı doğamaz, mutlak letal", False, "")],
                        [("Monozomi X (45,X)", False, ""), ("Tüm düşüklerin yaklaşık %10'u", True, "Tekil en sık monozomi"), ("%95+ intrauterin kayıp; canlı doğum nadir", False, "")],
                        [("Triploidi (69 kromozom)", False, ""), ("Tüm kromozomal düşüklerin ~%20'si", True, "Poliploidi oranı"), ("Neredeyse daima letal, erken neonatal ölüm", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Birinci trimester spontan abortus materyallerinde sitogenetik analizle en sık saptanan, ancak canlı doğumla hiçbir şekilde bağdaşmayan otozomal trizomi hangisidir?",
                    {
                        "A": "Trizomi 21",
                        "B": "Trizomi 18",
                        "C": "Trizomi 16",
                        "D": "Trizomi 13",
                        "E": "Trizomi 8"
                    },
                    "C",
                    {
                        "A": "Trizomi 21 canlı doğabilen en sık trizomidir.",
                        "B": "Trizomi 18 canlı doğabilir.",
                        "C": "Doğru cevap C'dir: Trizomi 16 spontan abortuslarda en sık saptanan trizomidir ve daima intrauterin letaldir.",
                        "D": "Trizomi 13 canlı doğabilir.",
                        "E": "Trizomi 8 mozaik formda canlı doğabilir."
                    }
                ),
                make_active_recall(
                    "Spontan abortuslarda tek başına en sık rastlanan tekil kromozom anomalisi karyotipi nedir?",
                    "45,X (Turner monozomisi) karyotipidir.",
                    "Gonozomal monozomi tekil frekansı"
                )
            ],
            "spotPearls": [
                "1. trimester spontan düşüklerinin en az %50'si kromozom anomalilerine bağlıdır.",
                "Düşüklerde en sık saptanan otozomal trizomi Trizomi 16'dır (asla canlı doğmaz).",
                "Düşüklerde en sık tekil anomali 45,X'tir; bu gebeliklerin %95'i kaybedilir."
            ]
        },

        # Slayt 7
        {
            "title": "Anöploidi Mekanizmaları: Mayotik Ayrılamama (Nondisjunction)",
            "subtitle": "Kromozom Ayrılma Kusurları ve Gamet Anöploidisi",
            "badge": "Ayrılamama Biyolojisi",
            "coreContent": {
                "text": "Anöploidilerin primer ve en sık hücresel mekanizması **mayotik ayrılamamadır (nondisjunction)**. Normal gametogenezde gerçekleşen kromozom dağılımı şu patogenetik aşamalarla bozulur:\n\n"
                        "- **Ayrılma Kusuru:** Homolog kromozomlar (Mayoz I) veya kardeş kromatitler (Mayoz II) zıt kutuplara çekilemez ve aynı yavru hücrede kalır.\n"
                        "- **Gamet Çıktısı:** Bir yavru hücreye fazla kromozom giderken (**disomik gamet, n+1=24**), diğer yavru hücreye ilgili kromozom hiç gitmez (**nullizomik gamet, n-1=22**).\n"
                        "- **Zigot Gelişimi:** Bu gametler normal bir haploid spermle döllendiğinde sırasıyla **trizomik (2n+1=47)** veya **monozomik (2n-1=45)** embriyolar oluşur.\n\n"
                        "> [!IMPORTANT]\n"
                        "> **Maternal Yaş Faktörü:** Oositlerin fetal dönemden itibaren mayoz I profazında (**diktiyoten evresinde**) onlarca yıl beklemesi, kromozomları bir arada tutan kohezin komplekslerini yıpratır ve ileri anne yaşında ayrılamama riskini katlanarak artırır.",
                "keyBullets": [
                    {"title": "Mayotik Ayrılamama", "desc": "Homolog kromozomların veya kardeş kromatitlerin zıt kutuplara ayrılamamasıdır.", "isKey": True},
                    {"title": "Gamet Çıktıları", "desc": "Bir kutba 24 kromozomlu (n+1), diğer kutba 22 kromozomlu (n-1) gamet gider.", "isKey": True},
                    {"title": "Maternal Yaş Faktörü", "desc": "Oositlerin diktiyoten evresinde uzun yıllar beklemesi kohezin yıkımıyla riski artırır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Maternal Yaş ve Mayotik Ayrılamama Zinciri",
                    [
                        "1. Fetal oogenez sırasında oositler mayoz I profazında (diktiyoten evresinde) beklemeye girer",
                        "2. İleri anne yaşında (özellikle >35 yaş) kromozomları bir arada tutan kohezin proteinleri degrade olur",
                        "3. Ovülasyon sonrası mayoz I anafazında homolog kromozomlar kinetokor mikrotübüllerince eşit ayrılamaz",
                        "4. n+1 (24 kromozomlu) disomik oosit oluşur ve normal spermle döllenerek trizomik zigotu kurar"
                    ]
                ),
                make_cloze(
                    "Homolog kromozomların mayoz I'de veya kardeş kromatitlerin mayoz II'de zıt kutuplara ayrılamaması fenomenine ayrılamama veya nondisjunction denir.",
                    "ayrılamama",
                    "Hücresel kromozomal dağılım defektini düşününüz"
                ),
                make_active_recall(
                    "Mayotik ayrılamama sonucu oluşan 22 kromozomlu (n-1) bir gamet normal bir spermle döllenirse oluşan zigotun karyotipik durumu ne olur?",
                    "2n - 1 = 45 kromozomlu monozomik zigot oluşur (otozomal ise erken dönemde ölür).",
                    "Eksik kromozomlu zigot sonucu"
                )
            ],
            "spotPearls": [
                "Anöploidilerin temel oluşum mekanizması mayotik ayrılamamadır (nondisjunction).",
                "Ayrılamama disomik (n+1) ve nullizomik (n-1) gametler üretir.",
                "İleri anne yaşı, oositlerin diktiyotende bekleme süresine bağlı olarak ayrılamama riskini en çok artıran faktördür."
            ]
        },

        # Slayt 8
        {
            "title": "Mayoz I vs Mayoz II Ayrılamamasının Moleküler Ayrımı",
            "subtitle": "Parental Homologların ve Heterozigotluğun Karyotipik Analizi",
            "badge": "Ayrılamama Analizi",
            "coreContent": {
                "text": "Mayotik ayrılamamanın evresi, anöploid gametteki genetik belirteçlerin allelik dizilimi ve sentromerik analiziyle saptanır:\n\n"
                        "- **Mayoz I Hatası (Homolog Ayrılmama):** Ebeveyne ait iki farklı homolog kromozom aynı kutba gider. Gamet her iki farklı homologu da taşıdığından **heterodisomi** görülür ve sentromere yakın belirteçlerde **heterozigotluk korunur**.\n"
                        "- **Mayoz II Hatası (Kromatit Ayrılmama):** Mayoz I normal tamamlanır ancak kardeş kromatitler ayrılamaz. Fazla kromozom tek bir kromatitin ikiz kopyası olduğundan **izodisomi** gelişir ve sentromere yakın lokuslarda **tam homozigotluk** izlenir.\n\n"
                        "> [!TIP]\n"
                        "> **Klinik Dağılım:** Trizomi 21 (Down sendromu) olgularının yaklaşık %90'ı maternal kökenlidir ve bunların dörtte üçünden fazlası **maternal Mayoz I ayrılamaması** sonucu ortaya çıkar.",
                "keyBullets": [
                    {"title": "Mayoz I Ayrılamaması", "desc": "Gamet her iki farklı parental homoloğu birden taşır (heterodisomi mevcuttur).", "isKey": True},
                    {"title": "Mayoz II Ayrılamaması", "desc": "Gamet aynı homologun özdeş iki kopyasını taşır (izodisomi mevcuttur).", "isKey": True},
                    {"title": "Down Sendromu Dağılımı", "desc": "Trizomi 21 olgularının büyük kısmı maternal Mayoz I ayrılamamasından kaynaklanır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Mayoz I vs Mayoz II Ayrılamaması",
                    "Mayoz I Ayrılamaması",
                    "Homolog çiftler ayrılamaz; ekstra kromozomlu gamet her iki ebeveyn homoloğunu da içerir (heterodisomi; heterozigotluk korunur).",
                    "Mayoz II Ayrılamaması",
                    "Kardeş kromatitler ayrılamaz; ekstra kromozomlu gamet tek bir homoloğun ikiz kopyasını içerir (izodisomi; tam homozigotluk)."
                ),
                make_micro_quiz(
                    "Bir trizomi olgusunda yapılan mikrosatellit DNA analizinde, ekstra kromozomun anneye ait olduğu ve annenin her iki farklı homolog kromozomunu birden taşıdığı saptanmıştır. Bu anöploidi hangi evredeki ayrılamama kusuruna işaret eder?",
                    {
                        "A": "Maternal Mayoz I ayrılamaması",
                        "B": "Maternal Mayoz II ayrılamaması",
                        "C": "Paternal Mayoz I ayrılamaması",
                        "D": "Paternal Mayoz II ayrılamaması",
                        "E": "Post-zigotik mitotik ayrılma"
                    },
                    "A",
                    {
                        "A": "Doğru cevap A'dır: Gamette annenin her iki farklı homologunun birden bulunması (heterodisomi) Mayoz I ayrılma kusurunun tipik kanıtıdır.",
                        "B": "Mayoz II olsaydı kardeş kromatitler ayrılmayacak ve özdeş kopya (izodisomi) taşınacaktı.",
                        "C": "Soruda maternal kaynaklı olduğu belirtilmiştir.",
                        "D": "Paternal kökenli değildir.",
                        "E": "Post-zigotik mitozda mozaisizm gelişir."
                    }
                ),
                make_active_recall(
                    "Mayoz II ayrılamaması sonucunda oluşan gamet ve döllenme sonrası ürün moleküler belirteçler açısından ne gösterir?",
                    "Aynı parental kromatitin ikiz kopyasını taşıdığı için sentromerik bölgede izodisomi (homozigotluk) gösterir.",
                    "Kardeş kromatit özdeşliği"
                )
            ],
            "spotPearls": [
                "Mayoz I ayrılamaması = iki farklı homolog kromozom aynı gamette (heterodisomi).",
                "Mayoz II ayrılamaması = aynı kromatitin özdeş iki kopyası aynı gamette (izodisomi).",
                "Trizomi 21'in en sık nedeni maternal Mayoz I ayrılamamasıdır (~%75)."
            ]
        },

        # Slayt 9 (CHECKPOINT 1)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Sitogenetik Temeller ve Kromozomal Anomalilerin Sınıflandırılması",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 1",
            "coreContent": {
                "text": "Bu ilk öğrenme bölümünde sitogenetik temeller ve sayısal anomalilerin patogenezini inceledik:\n\n"
                        "- **Kromozomal Organizasyon:** 46 kromozom (44 otozom, 2 gonozom); 13, 14, 15, 21 ve 22 numaralı kromozomlar satellitli akrosentrik yapıdadır.\n"
                        "- **Sayısal Sapmalar:** Poliploidiler (3n=69, 4n=92) ve anöploidiler (2n+1, 2n-1). Yaşamla bağdaşan tek tam monozomi **Turner sendromudur (45,X)**; tüm otozomal monozomiler letaldir.\n"
                        "- **Erken Gebelik Kayıpları:** Spontan abortusların %50'sinden fazlası kromozomaldir. Tekil en sık trizomi letal **Trizomi 16**, tekil en sık anomali ise **45,X'tir**.\n"
                        "- **Ayrılma Kusurları:** Mayoz I ayrılamaması **heterodisomi** (farklı homologlar), Mayoz II ayrılamaması **izodisomi** (özdeş kromatitler) ile sonuçlanır.",
                "keyBullets": [
                    {"title": "Normal Karyotip", "desc": "46,XX veya 46,XY; akrosentrikler 13, 14, 15, 21 ve 22.", "isKey": True},
                    {"title": "Monozomi Kuralı", "desc": "Tüm otozomal monozomiler letaldir; tek canlı monozomi 45,X Turner'dır.", "isKey": True},
                    {"title": "Ayrılamama Dinamiği", "desc": "Mayoz I heterodisomi (farklı homologlar), Mayoz II izodisomi (özdeş kromatitler) üretir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kavram", "Temel Tanım / Karakteristik", "Sınav Spotu Değeri"],
                    [
                        [("Canlı Doğum Anomali Oranı", False, ""), ("Tüm canlı doğumların yaklaşık %1'i", True, "Genel prevalans"), ("En sık anomali anöploididir", False, "")],
                        [("Yaşayan Tek Monozomi", False, ""), ("45,X Turner Sendromu", True, "Otozomlarda monozomi yaşamaz"), ("Spontan düşük oranı %95 üzeridir", False, "")],
                        [("Düşükte En Sık Trizomi", False, ""), ("Trizomi 16", True, "Canlı doğumu olmayan abortus trizomisi"), ("Asla canlı doğamaz", False, "")],
                        [("Mayoz I Hatası", False, ""), ("Farklı homologların bir arada kalması", True, "Heterodisomi mekanizması"), ("En sık trizomi 21 mekanizmasıdır", False, "")]
                    ]
                ),
                make_cloze(
                    "Spontan abortuslarda en sık saptanan otozomal trizomi olan Trizomi 16 canlı doğumla hiçbir zaman bağdaşmaz.",
                    "16",
                    "Letal trizomi numarasını anımsayınız"
                ),
                make_active_recall(
                    "Dengeli kromozom anomalisi taşıyan bir ebeveynin kendisi tamamen sağlıklı iken neden çocuk sahibi olmakta sorun yaşar?",
                    "Mayoz bölünmede homologların ayrılması sırasında delesyon ve duplikasyon içeren dengesiz gametler ürettikleri için.",
                    "Dengesiz gamet riski ve erken fetal kayıplar"
                )
            ],
            "spotPearls": [
                "Canlı doğumların %1'inde kromozom anomalisi vardır; en sık tip anöploididir.",
                "Yaşamla bağdaşan tek tam monozomi 45,X Turner sendromudur.",
                "Erken abortuslarda en sık trizomi Trizomi 16'dır; en sık triploidi nedeni dispermidir."
            ]
        },

        # Slayt 10
        {
            "title": "Anafazda Geri Kalma (Anaphase Lagging) ve Post-Zigotik Mozaisizm",
            "subtitle": "Mitotik Ayrılma Hataları ve Hücresel Heterojenite",
            "badge": "Mozaisizm Mekanizmaları",
            "coreContent": {
                "text": "Anöploidi gelişiminde mayotik ayrılma kusurlarının yanı sıra post-zigotik mekanizmalar da kritik rol oynar:\n\n"
                        "- **Anafazda Geri Kalma (Anaphase Lagging):** Anafaz sırasında bir kromozom iğ ipliğine zayıf tutunur veya kutba göçte gecikir. Çekirdek zarı kapanırken dışarıda kalarak sitoplazmik nükleazlarca parçalanır ve monozomik hücre serisi oluşturur.\n"
                        "- **Mitotik Mozaisizm:** Tek bir zigottan köken alan organizmada, embriyonik mitoz hataları sonucu genetik yapısı farklı iki veya daha fazla hücre serisinin (ör. 46,XX / 47,XX,+21) bir arada bulunmasıdır.\n"
                        "- **Fenotipik Yansıma:** Mozaik olgularda klinik şiddet, anormal hücrelerin yüzdesine ve hangi dokulara dağıldığına bağlıdır; saf trizomilere göre belirgin şekilde daha hafif seyreder.\n\n"
                        "> [!NOTE]\n"
                        "> Mozaisizm **tek bir zigottan** gelişen hücresel heterojenitedir; **kimerizm** ise iki ayrı zigotun tek bir embriyoda kaynaşmasıyla oluşur.",
                "keyBullets": [
                    {"title": "Anafazda Geri Kalma", "desc": "Geciken kromozomun nükleusa dahil olamayarak sitoplazmada kaybolmasıdır.", "isKey": True},
                    {"title": "Mozaisizm Tanımı", "desc": "Tek bir zigottan köken alan iki veya daha fazla farklı genetik hücre serisinin varlığıdır.", "isKey": True},
                    {"title": "Klinik Şiddet", "desc": "Mozaik bireylerde fenotip, anormal hücrelerin yüzdesine ve doku dağılımına göre hafiftir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Mitotik Anafaz Gecikmesi ve Mozaisizm Oluşumu",
                    [
                        "1. Normal 46 kromozomlu bir zigot ilk bölünmelerini başarıyla tamamlar",
                        "2. Erken embriyonik mitoz anafazında bir kromatit iğ ipliği tutunma hatasıyla geri kalır",
                        "3. Geri kalan kromatit mikronükleus içinde sitoplazmada dejenere olur",
                        "4. Embriyoda hem normal 46 kromozomlu hem de monozomik hücre serileri bir arada gelişerek mozaisizmi kurar"
                    ]
                ),
                make_micro_quiz(
                    "Tek bir zigottan köken alan bir bireyde, post-zigotik mitotik bölünme hataları sonucunda karyotipik yapısı birbirinden farklı iki veya daha fazla hücre soyunun bulunmasına ne ad verilir?",
                    {
                        "A": "Kimerizm",
                        "B": "Mozaisizm",
                        "C": "Psödogenomi",
                        "D": "Heteroplazmi",
                        "E": "Poliploidi"
                    },
                    "B",
                    {
                        "A": "Kimerizm farklı zigotların birleşmesiyle oluşur.",
                        "B": "Doğru cevap B'dir: Tek bir zigottan türeyen farklı karyotipli hücre soylarına mozaisizm denir.",
                        "C": "Psödogenomik sahte dizilimdir.",
                        "D": "Heteroplazmi mitokondriyal DNA varyasyonudur.",
                        "E": "Poliploidi kromozom takımı katlanmasıdır."
                    }
                ),
                make_active_recall(
                    "Mozaisizm ile kimerizm arasındaki en temel sitogenetik ve embriyolojik fark nedir?",
                    "Mozaisizm tek bir zigottan köken alırken, kimerizm iki farklı zigotun birleşmesiyle meydana gelir.",
                    "Zigot sayısı farkı (tek vs çift)"
                )
            ],
            "spotPearls": [
                "Anafazda geri kalma (anaphase lagging) geciken kromozomun kaybıyla monozomiye yol açar.",
                "Mozaisizm tek bir zigottan gelişir; kimerizm ise iki ayrı zigotun füzyonudur.",
                "Mozaik Down sendromunda klinik fenotip klasik trizomiye göre çok daha hafif seyreder."
            ]
        }
    ]
