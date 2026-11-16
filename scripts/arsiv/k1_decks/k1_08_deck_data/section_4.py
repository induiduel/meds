"""
Bölüm 4: Mitokondriyal Disfonksiyon, Oksidatif Fosforilasyon Kaybı ve Hücre Hasarı
Adımlar: 31 - 40
Checkpoint: Adım 39 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # ADIM 31
    slides.append({
        "slideNumber": 31,
        "title": "Mitokondrinin Çift Rolü: Enerji Santrali ve Hasar Odağı",
        "subtitle": "ATP biyosentezi, hücresel metabolizma merkezi ve intraselüler ROS fabrikası",
        "badge": "Mitokondri Paradoksu",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Mitokondri, ökaryotik hücrelerin enerji santralidir; glukoz, yağ asitleri ve amino asitlerin yıkımından "
            "elde edilen indirgenmiş koenzimler (NADH, FADH2) aracılığıyla oksidatif fosforilasyon yaparak hücresel "
            "ATP'nin %90'ından fazlasını üretir. Ancak mitokondri aynı zamanda yaşamın en büyük paradoksunu barındırır.\n\n"
            "> [TEMEL İLKE] Mitokondri hem hücrenin hayatta kalması için vazgeçilmez ATP kaynağıdır, hem de serbest "
            "radikal üretiminin ana merkezi ve apoptoz ölüm makinelerinin (sitokrom c) saklandığı cephaneliktir.\n\n"
            "Yaşlanma sürecinde mitokondrilerin verimliliği kademeli olarak düşer; enerji üretimi azalırken serbest radikal "
            "ve ölüm sinyali salgılama potansiyeli katlanır."
        ),
        "medicalTerms": [
            {"term": "Oksidatif Fosforilasyon", "explanation": "Mitokondri iç zarında proton gradyanı kullanılarak ADP'den ATP sentezlenmesi sürecidir."},
            {"term": "Mitokondriyal Biyojenez", "explanation": "Hücrede yeni mitokondrilerin bölünerek çoğalması ve fonksiyonel kütlenin yenilenmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mitokondri hem ATP üretiminin hem de bazal ROS üretiminin ana merkezidir.",
            "📌 [SINAV SPOTU] Yaşlanma mitokondriyal enerji verimliliğini düşürürken hasar salınımını artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enerji İhtiyacı", "desc": "Kardiyomiyosit ve nöronlar mitokondriyal ATP'ye mutlak bağımlıdır.", "isKey": True},
                {"title": "Ölüm Cephaneliği", "desc": "Membran geçirgenliği bozulduğunda sitokrom c salarak apoptozu başlatır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Aerobik hücrelerde ATP üretiminin ve hücresel serbest radikal üretiminin ana merkezi mitokondri organelidir.",
                "mitokondri",
                "Hücrenin çift zarlı enerji santrali organeli"
            ),
            make_active_recall(
                "Mitokondrinin hücresel yaşlanma ve hücre ölümü sürecindeki 'çift rollü paradoksu' nedir?",
                "Bir yandan hücrenin yaşaması için gereken ATP'yi üretirken, diğer yandan hücreyi yıkan ROS'ların ana kaynağı ve apoptozu başlatan sitokrom c'nin deposu olmasıdır."
            )
        ]
    })

    # ADIM 32
    slides.append({
        "slideNumber": 32,
        "title": "Mitokondriyal DNA'nın (mtDNA) Özellikleri ve Hassasiyeti",
        "subtitle": "Histonsuz dairesel yapı, zayıf DNA onarımı ve 10-20 kat yüksek mutasyon hızı",
        "badge": "mtDNA Hassasiyeti",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İnsan mitokondrisi kendi bağımsız genomuna (mtDNA) sahiptir. Bu genom 16.569 baz çiftinden oluşan dairesel, "
            "çift zincirli bir moleküldür ve solunum zincirinin 13 kritik alt birimini, 22 tRNA'yı ve 2 rRNA'yı kodlar. "
            "Ancak mtDNA, nükleer DNA'ya kıyasla mutasyonlara karşı olağanüstü derecede savunmasızdır.\n\n"
            "> [SINAV SPOTU] mtDNA'nın etrafını koruyucu histon proteinleri sarmalamaz, intron içermez (her mutasyon "
            "doğrudan kodlayan bölgeyi vurur), nükleotit eksizyon onarımı (NER) yoktur ve ROS üretiminin tam göbeğindedir.\n\n"
            "Bu nedenlerle yaşlanan hücrelerde mtDNA mutasyon ve delesyon sıklığı nükleer DNA'ya göre 10 ila 20 kat daha yüksektir."
        ),
        "medicalTerms": [
            {"term": "Mitokondriyal DNA (mtDNA)", "explanation": "Mitokondri matriksinde yerleşik, maternal kalıtılan, histonsuz dairesel genetik materyaldir."},
            {"term": "Histonsuz Genom", "explanation": "DNA sarmalının histon proteinleriyle paketlenmeyip çıplak kalması ve hasara açık olmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] mtDNA histon proteinlerinden yoksundur ve intron içermez.",
            "📌 [SINAV SPOTU] Yaşlanmayla mtDNA'da nükleer DNA'dan 10-20 kat daha fazla delesyon ve mutasyon birikir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Çıplak DNA", "desc": "Histon koruması yok, serbest radikal kaynağının dibinde yerleşik.", "isKey": True},
                {"title": "Zayıf Onarım", "desc": "Nükleotid eksizyon mekanizması bulunmaz; hasar kalıcılaşır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Özellik", "Mitokondriyal DNA (mtDNA)", "Nükleer DNA (nDNA)"],
                [
                    [("Yapısal Biçim", False, ""), ("Dairesel, histonsuz, çıplak", True, "Paketlenmemiş dairesel genom"), ("Lineer, histonlarla paketli kromatin", False, "")],
                    [("İntron Varlığı", False, ""), ("Yok (hemen her baz kodlayıcıdır)", True, "Her hasar protein yapısını bozar"), ("Var (geniş kodlamayan intronlar)", False, "")],
                    [("Mutasyon Birikim Hızı", False, ""), ("10 - 20 kat daha yüksek", True, "Yaşlanmada aşırı mutasyon yükü"), ("Düşük (gelişmiş onarım kalkanı)", False, "")]
                ]
            ),
            make_cloze(
                "Mitokondriyal DNA'nın serbest radikal hasarına nükleer DNA'dan çok daha duyarlı olmasının nedeni histon proteinlerinden yoksun olmasıdır.",
                "histon",
                "DNA'yı sarıp koruyan bazik çekirdek protein grubu"
            )
        ]
    })

    # ADIM 33
    slides.append({
        "slideNumber": 33,
        "title": "Oksidatif Fosforilasyonun Bozulması: Solunum Çöküşü",
        "subtitle": "Kompleks I ve IV aktivite kaybı, elektron kaçağı ve hücresel enerji krizi",
        "badge": "Solunum Çöküşü",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "mtDNA'da biriken mutasyonlar doğrudan elektron taşıma zinciri (ETS) komplekslerinin protein alt birimlerini "
            "hedef alır. Özellikle Kompleks I (NADH dehidrogenaz) ve Kompleks IV (sitokrom c oksidaz) enzimatik aktiviteleri "
            "ileri yaşla birlikte belirgin şekilde geriler. Elektron akışı duraklar, proton pompalama kapasitesi çöker "
            "ve mitokondri iç zar potansiyeli (ΔΨm) kaybolur.\n\n"
            "> [SINAV SPOTU] Solunum zinciri komplekslerinin hasarlanması bir yandan ATP sentezini durdururken, diğer "
            "yandan elektronların oksijene kontrolsüz kaçışını artırarak daha fazla ROS üretilmesine neden olur.\n\n"
            "Bu durum, hücrenin enerji ihtiyacını karşılayamaz hale gelerek metabolik tükenişe sürüklenmesidir."
        ),
        "medicalTerms": [
            {"term": "Elektron Taşıma Zinciri (ETS)", "explanation": "Mitokondri iç zarında proton pompalayarak ATP sentezleten 4 büyük enzim kompleksidir."},
            {"term": "Membran Potansiyeli (ΔΨm)", "explanation": "İç zarın iki tarafı arasındaki proton farkıyla oluşan elektriksel enerjidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaşlanmada Kompleks I ve Kompleks IV aktiviteleri belirgin şekilde azalır.",
            "📌 [SINAV SPOTU] Membran potansiyelinin kaybı ATP sentezini kilitler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enzim Çöküşü", "desc": "NADH dehidrogenaz ve sitokrom oksidazın verimi düşer.", "isKey": True},
                {"title": "Enerji İflası", "desc": "ATP/ADP oranı dramatik olarak azalır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Mitokondriyal Oksidatif Fosforilasyon Çöküş Zinciri",
                [
                    "1. mtDNA Delesyonu: Yaşla biriken radikaller solunum kompleksi genlerini bozar.",
                    "2. Hatalı Kompleks Sentezi: Kompleks I ve IV alt birimleri düzgün birleştirilemez.",
                    "3. Proton Pompası İflası: İç zarda proton gradyanı (ΔΨm) oluşturulamaz.",
                    "4. ATP Sentaz Durması: Kemiozmoz durarak hücre içi ATP sentezi hızla düşer.",
                    "5. Hücre Disfonksiyonu: Enerjiye bağımlı iyon pompaları ve anabolik yollar kilitlenir."
                ]
            ),
            make_cloze(
                "Yaşlanmayla birlikte mitokondriyal iç zar potansiyelinin kaybı ATP sentaz enziminin çalışmasını durdurur.",
                "ATP sentaz",
                "Proton gradyanını kullanarak ATP üreten döner motor enzimi"
            )
        ]
    })

    # ADIM 34
    slides.append({
        "slideNumber": 34,
        "title": "ATP Tüketimi ve Nekroz Eğilimi: İyon Pompalarının İflası",
        "subtitle": "Na+/K+ ATPaz durması, kalsiyum göllenmesi, hücresel şişme ve membran yırtılması",
        "badge": "Enerji ve Nekroz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Mitokondriyal hasarın hücre sağkalımı üzerinde iki temel kaderi vardır: ATP azalması nekroza, sitokrom c "
            "salınımı ise apoptoza yol açar. Eğer mitokondri hasarı çok ani ve ağır ise hücre içi ATP hızla kritik eşiğin "
            "(normalin <%20'si) altına iner. ATP bulunmadığında hücre apoptoz gibi enerji gerektiren programlı bir ölümü "
            "bile yürütemez.\n\n"
            "> [SINAV SPOTU] Plazma membranındaki Na+/K+ ATPaz pompası durur; hücre içine sodyum ve su dolarak masif "
            "hücresel şişme (onkozis) başlar. Ca2+ ATPaz durunca sitozole kalsiyum hücum eder.\n\n"
            "Aşırı kalsiyum fosfolipaz ve proteazları aktive ederek plazma zarını patlatır; hücre koagülatif nekrozla dağılır."
        ),
        "medicalTerms": [
            {"term": "Onkozis", "explanation": "ATP tükenmesi ve iyon pompası iflasıyla hücrenin su alarak şişmesi ve nekroza gitmesidir."},
            {"term": "Na+/K+ ATPaz", "explanation": "Hücre hacmini ve membran potansiyelini koruyan ATP bağımlı sodyum-potasyum pompasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Masif ATP tükenmesi nekroz eğilimi yaratır; çünkü apoptoz ATP'ye bağımlıdır.",
            "📌 [SINAV SPOTU] Na+/K+ ATPaz iflası hücresel şişme ve membran lizisine neden olur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Masif ATP Kaybı", "desc": "İyon pompaları felç olur, hücre içine su hücum eder.", "isKey": True},
                {"title": "Nekrotik Yırtılma", "desc": "Kalsiyum bağımlı proteazlar plazma membranını parçalar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Ağır ATP Tükenmesi (Nekroz) vs Kısmi Mitokondri Hasarı (Apoptoz)",
                "Masif ATP Tükenmesi (Nekroz)",
                "ATP tamamen sıfırlanır; iyon pompaları iflas eder, hücre su alarak şişer (onkozis), membran yırtılır ve inflamatuvar nekroz gelişir.",
                "Kısmi Mitokondri Hasarı (Apoptoz)",
                "ATP düzeyi korunur; mitokondri zarı açılarak sitokrom c salınır ve kaspazlar ATP kullanarak hücreyi sessizce paketler."
            ),
            make_active_recall(
                "Ağır mitokondri hasarında ATP düzeyinin tamamen sıfırlanmasının hücreyi apoptoz yerine nekroza sürüklemesinin nedeni nedir?",
                "Apoptozun kaspaz aktivasyonu, apaptozom kurulumu ve kromatin paketlenmesi için mutlaka ATP enerjisine ihtiyaç duymasıdır; ATP yoksa hücre zorunlu olarak nekrozla patlar."
            )
        ]
    })

    # ADIM 35
    slides.append({
        "slideNumber": 35,
        "title": "Mitokondriyal Membran Geçirgenlik Gözenekleri (MPTP)",
        "subtitle": "Siklofilin D, iç zar kilitlenmesi, mitokondriyal şişme ve geri dönüşsüz hasar",
        "badge": "MPTP ve Geçirgenlik",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "İskemi-reperfüzyon hasarında, yüksek oksidatif streste veya aşırı sitozolik kalsiyum göllenmesinde "
            "mitokondri iç zarında yüksek iletkenlikli dev bir kanal açılır: 'Mitokondriyal Membran Geçirgenlik Geçiş "
            "Gözeneği' (Mitochondrial Permeability Transition Pore - MPTP). MPTP kompleksinin regülasyonunda iç zar "
            "proteini olan 'Siklofilin D' kritik rol oynar.\n\n"
            "> [SINAV SPOTU] MPTP açıldığında iç zarın proton bariyeri tamamen çöker; mitokondri matriksine su ve iyon "
            "hücum ederek organel balon gibi şişer ve kristalar parçalanır.\n\n"
            "Bu olay mitokondri için geri dönüşümsüz ölüm kararıdır; Siklosporin A gibi Siklofilin D inhibitörleri deneysel "
            "olarak MPTP açılmasını engelleyerek dokuyu koruyabilir."
        ),
        "medicalTerms": [
            {"term": "MPTP", "explanation": "İç mitokondriyal zarda kalsiyum ve ROS etkisiyle açılan, proton gradyanını sıfırlayan dev kanaldır."},
            {"term": "Siklofilin D", "explanation": "MPTP gözeneğinin açılmasını kolaylaştıran matriks ilişkili düzenleyici proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] MPTP açılması mitokondriyal membran potansiyelini tamamen sıfırlar ve mitokondriyi şişirir.",
            "📌 [SINAV SPOTU] Siklofilin D, MPTP açılmasında kilit rol oynayan proteindir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dev Gözenek", "desc": "Kalsiyum ve ROS etkisiyle iç zarda yüksek iletkenlikli kanal açılır.", "isKey": True},
                {"title": "Geri Dönüşsüz Son", "desc": "Mitokondri şişer, dış zar yırtılır, ATP sentezi tamamen durur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "İskemi-reperfüzyon hasarında ve ağır hücresel yaşlanmada mitokondri iç zarında açılarak proton gradyanını sıfırlayan ve mitokondriyal şişmeye yol açan dev kanal kompleksi aşağıdakilerden hangisidir?",
                {
                    "A": "CFTR klor kanalı",
                    "B": "Mitokondriyal membran geçirgenlik geçiş gözeneği (MPTP)",
                    "C": "Voltaj bağımlı sodyum kanalı",
                    "D": "Glukoz taşıyıcı GLUT-4",
                    "E": "Arakidonik asit poru"
                },
                "B",
                {
                    "A": "CFTR epitel hücre zarı klor kanalıdır.",
                    "B": "Doğru! MPTP iç zarda proton gradyanını yok eden geçiş gözeneğidir.",
                    "C": "Voltaj kapılı sodyum kanalı nöron aksiyon potansiyelindedir.",
                    "D": "GLUT-4 insülinle glukoz alır.",
                    "E": "Arakidonik asit poru bulunmaz."
                }
            ),
            make_cloze(
                "Mitokondri iç zarında MPTP gözeneğinin açılmasını kolaylaştıran matriks proteini Siklofilin D molekülüdür.",
                "Siklofilin D",
                "MPTP açılışını regüle eden matriks proteini"
            )
        ]
    })

    # ADIM 36
    slides.append({
        "slideNumber": 36,
        "title": "Mitofaji (Mitokondriyal Otofaji): PINK1/Parkin Kalite Kontrolü",
        "subtitle": "İç zar potansiyel kaybının algılanması, ubikitinlenme ve fagozomal temizlik",
        "badge": "Mitofaji ve PINK1",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Hücrenin mitokondri sağlığını korumak için geliştirdiği en zarif otofajik kalite kontrol mekanizması 'Mitofaji'dir "
            "(mitokondriye özgü seçici otofaji). Sağlıklı mitokondrilerde iç zar potansiyeli yüksek olduğu için dış zara "
            "ulaşan PINK1 kinaz proteini hızla iç zara çekilip parçalanır. Ancak mitokondri hasarlanıp iç zar potansiyelini "
            "kaybettiğinde PINK1 artık parçalanamaz ve dış mitokondriyal zarda birikir.\n\n"
            "> [SINAV SPOTU] Dış zarda biriken aktif PINK1, sitozolden bir E3 ubikitin ligaz olan 'Parkin' enzimini çağırır; "
            "Parkin hasarlı mitokondriyi ubikitinle donatır ve otofagozoma teslim ederek lizozomda erittirir.\n\n"
            "Bu yolağın mutasyonları Parkinson hastalığına ve hızlı nöronal yaşlanmaya yol açar."
        ),
        "medicalTerms": [
            {"term": "Mitofaji", "explanation": "Hasarlı, depolarize olmuş mitokondrilerin otofagozomlarca yutulup lizozomda eritilmesidir."},
            {"term": "PINK1 / Parkin Yolağı", "explanation": "Mitokondri hasarını algılayıp organeli ubikitinle işaretleyen otofajik kalite kontrol eksenidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mitofajide hasarlı mitokondriyi dış zarda PINK1 birikimi ve Parkin ubikitinlemesi işaretler.",
            "📌 [SINAV SPOTU] PINK1 ve Parkin mutasyonları erken başlangıçlı ailesel Parkinson hastalığı yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sensör (PINK1)", "desc": "Depolarize olmuş mitokondrinin dış zarında biriken kinaz.", "isKey": True},
                {"title": "İşaretleyici (Parkin)", "desc": "Dış zarı ubikitinleyerek otofaji reseptörlerine (p62) bağlayan ligaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Hasarlı Mitokondrinin Mitofaji ile Temizlenme Zinciri",
                [
                    "1. Membran Depolarizasyonu: Hasarlı mitokondri iç zar potansiyelini kaybeder.",
                    "2. PINK1 Birikimi: PINK1 iç zara çekilemez ve dış mitokondri zarında birikir.",
                    "3. Parkin Çağrısı: Aktif PINK1 sitozolik Parkin ligazını dış zara çeker.",
                    "4. Ubikitin İşaretlemesi: Parkin dış membran proteinlerini poli-ubikitinle etiketler.",
                    "5. Lizozomal Yıkım: Otofagozom hasarlı organeli yutar ve lizozomda tamamen eritir."
                ]
            ),
            make_cloze(
                "Hasarlı mitokondrileri ubikitinle işaretleyerek mitofajiye sevk eden E3 ligaz enzimi Parkin enzimidir.",
                "Parkin",
                "PINK1 ile birlikte mitofajiyi yürüten Parkinson ilişkili ligaz"
            )
        ]
    })

    # ADIM 37
    slides.append({
        "slideNumber": 37,
        "title": "Yaşlanan Hücrede Mitofaji Yetmezliği ve Megamitokondriler",
        "subtitle": "Bozuk füzyon/fisyon dengesi, dev şişkin organeller ve sitotoksisite",
        "badge": "Megamitokondri",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Genç hücrelerde mitofaji mekanizması bozuk mitokondrileri hızla temizlerken; yaşlanan hücrelerde otofaji "
            "kapasitesi ve lizozomal enzim desteği yetersiz kalır. Hasarlı mitokondriler temizlenemez ve sitoplazmada "
            "birikir. Eş zamanlı olarak mitokondriyal dinamikler (fisyon ve füzyon dengesi) bozulur.\n\n"
            "> [YÜKSEK VERİM] Hasarlı mitokondriler birbirine kaynaşarak normalin 10-20 katı büyüklüğünde, kristaları "
            "silinmiş dev 'megamitokondriler' (megamitochondria) oluşturur.\n\n"
            "Bu devasa anormal organeller hem ATP üretemez hem de sitoplazmaya sürekli kalsiyum ve serbest radikal "
            "boşaltarak hücreyi kronik bir metabolik kriz içinde tutar."
        ),
        "medicalTerms": [
            {"term": "Megamitokondri", "explanation": "Yaşlanma ve mitofaji yetmezliğinde organellerin anormal kaynaşmasıyla oluşan dev mitokondrilerdir."},
            {"term": "Mitokondriyal Dinamikler", "explanation": "Mitokondrilerin sürekli bölünme (fisyon: DRP1) ve birleşme (füzyon: Mfn1/2) dengesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaşlı hücrelerde mitofaji yetersizliği sonucu anormal megamitokondriler birikir.",
            "📌 [SINAV SPOTU] Megamitokondriler solunum yapamaz ancak aşırı ROS sızdırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Otofajik Tıkanma", "desc": "Lizozomlar yaşlı mitokondrileri sindirmeye yetişemez.", "isKey": True},
                {"title": "Anormal Morfoloji", "desc": "Parçalanmış kristalı devasa organel kitleleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Yaşlanan hücrelerde mitofaji yetersizliği sonucu oluşan devasa anormal organellere megamitokondriler adı verilir.",
                "megamitokondriler",
                "Bozuk mitofajide biriken dev mitokondri yapıları"
            ),
            make_active_recall(
                "Yaşlanma sürecinde mitofaji yetmezliğinin hücresel metabolizma üzerindeki en kritik negatif sonucu nedir?",
                "Hasarlı ve depolarize olmuş mitokondrilerin temizlenemeyerek birikmesi, enerji üretiminin çökmesi ve hücre içine sürekli toksik ROS sızmasıdır."
            )
        ]
    })

    # ADIM 38
    slides.append({
        "slideNumber": 38,
        "title": "Kalp Kası ve Beyinde Mitokondri Yaşlanması",
        "subtitle": "Kardiyomiyosit sarkopenisi, diyastolik disfonksiyon ve nörodejeneratif enerji açlığı",
        "badge": "Organ Tutulumu",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Mitokondriyal disfonksiyonun en ağır klinik sonuçları vücudun enerjiye en bağımlı ve bölünmeyen iki "
            "dokusunda görülür: kalp kası (miyokard) ve santral sinir sistemi (beyin). Yaşlanan kardiyomiyositlerin "
            "hacminin %40'ını mitokondriler kaplar. Mitokondriyal çöküş, diyastolde kalsiyumun sarkoplazmik retikuluma "
            "geri pompalanmasını bozar; kalp kası gevşeyemez ve yaşlılarda 'korunmuş ejeksiyon fraksiyonlu kalp yetmezliği' "
            "(HFpEF / diyastolik yetmezlik) gelişir.\n\n"
            "> [SINAV SPOTU] Beyinde ise nöronlar sinaptik vezikül taşınması ve membran polarizasyonu için mitokondriye "
            "muhtaçtır; mitokondriyal yetmezlik sinaps kaybına ve Alzheimer/Parkinson nörodejenerasyonuna yol açar.\n\n"
            "Bu durum mitokondri yaşlanmasının doğrudan ölümcül organ patolojilerine dönüşümüdür."
        ),
        "medicalTerms": [
            {"term": "Diyastolik Kalp Yetmezliği (HFpEF)", "explanation": "Miyokardın mitokondriyal ATP yetersizliği nedeniyle gevşeyememesi sonucu gelişen tablodur."},
            {"term": "Sinaptik Enerji Açlığı", "explanation": "Nöron akson terminallerinde ATP yetersizliğine bağlı nörotransmitter salınımının durmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaşlı kalpte mitokondri disfonksiyonu diyastolik gevşeme bozukluğuna yol açar.",
            "📌 [SINAV SPOTU] Nöronlarda mitokondri çöküşü sinaps kaybını ve nörodejenerasyonu başlatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Miyokard", "desc": "Gevşeme (lüsitropi) bozukluğu ve senil kardiyomiyopati.", "isKey": True},
                {"title": "Nöronlar", "desc": "Aksonal transport felci ve bilişsel yıkım.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Doku / Organ", "Mitokondri Bağımlılığı Nedeni", "Yaşlanmadaki Spesifik Klinik Patoloji"],
                [
                    [("Kalp Kası (Miyokard)", False, ""), ("Sürekli kasılma ve kalsiyum geri alımı", False, ""), ("Diyastolik kalp yetmezliği (HFpEF)", True, "Gevşeyemeyen sert ventrikül tablosu")],
                    [("Santral Sinir Sistemi", False, ""), ("Sinaptik iletim ve aksonal taşıma", False, ""), ("Nörodejenerasyon ve bilişsel gerileme", True, "Alzheimer ve Parkinson patolojileri")],
                    [("İskelet Kası", False, ""), ("Kas lifi kasılması ve protein dengesi", False, ""), ("Senil sarkopeni ve kas güçsüzlüğü", True, "Kas kütlesi ve kuvvet kaybı")]
                ]
            ),
            make_cloze(
                "Yaşlı bireylerde kardiyomiyositlerin mitokondriyal ATP yetersizliği sonucu gevşeyememesi diyastolik kalp yetmezliği tablosunu doğurur.",
                "diyastolik",
                "Kalbin gevşeme fazını tanımlayan kardiyak terim"
            )
        ]
    })

    # ADIM 39 - CHECKPOINT 4
    slides.append({
        "slideNumber": 39,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Mitokondriyal Disfonksiyon ve Enerji Biyolojisi",
        "subtitle": "mtDNA hassasiyeti, Kompleks I/IV çöküşü, MPTP, PINK1/Parkin ve mitofajinin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 4,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında mitokondriyal yaşlanma eksenini özetliyoruz. 1) Paradoks: Mitokondri hem ATP'nin "
            "hem bazal ROS'un ana kaynağıdır. 2) mtDNA: Histonsuzdur, intron içermez; nükleer DNA'dan 10-20 kat daha hızlı "
            "mutasyona uğrar. 3) Solunum çöküşü: Kompleks I ve IV aktivitesi azalır, iç zar potansiyeli kaybolur, ATP "
            "sentezi durur ve elektron kaçağı artar. 4) Akıbet: Ağır ATP kaybı Na/K pompasını felç edip nekroz yapar; "
            "kısmi hasar MPTP açarak sitokrom c ile apoptoz yapar. 5) Mitofaji: PINK1 depolarize mitokondri dış zarında "
            "birikir, Parkin ligazını çağırır ve organeli ubikitinle otofajiye gönderir; yetersizliğinde megamitokondriler birikir.\n\n"
            "> [KLİNİK İPUCU] Sınavda mitofajiden sorumlu genler PINK1 ve Parkin'dir; mutasyonları Parkinson yapar.\n\n"
            "Aşağıdaki 3 akıl kartını hafızanıza sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Mitofaji", "explanation": "PINK1/Parkin aracılığıyla hasarlı mitokondrilerin lizozomda eritilmesidir."},
            {"term": "MPTP", "explanation": "İç zarda Siklofilin D ile açılan ölümcül membran geçirgenlik kanalıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] mtDNA histonsuzdur; yaşlanmayla mutasyon yükü nükleustan 10-20 kat fazladır.",
            "📌 [SINAV SPOTU] PINK1 dış zarda birikir, Parkin E3 ligazı çağırarak mitofajiyi başlatır.",
            "📌 [SINAV SPOTU] Masif ATP kaybı nekroz, sitokrom c salınımı apoptoz eğilimi yaratır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Genomik Kusur", "desc": "mtDNA delesyonları ve solunum zincirinin kilitlenmesi.", "isKey": True},
                {"title": "Kalite Kontrol", "desc": "PINK1/Parkin ile mitofaji; yaşlılıkta megamitokondri oluşumu.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-08-fc-10",
                "Mitokondriyal DNA'nın nükleer DNA'ya kıyasla yaşlanma sürecinde 10-20 kat daha fazla mutasyona uğramasının 3 temel nedeni nedir?",
                "1) Koruyucu histon proteinlerinden tamamen yoksun olması, 2) İntron içermediği için her mutasyonun kodlayıcı bölgeyi vurması, 3) Sürekli ROS üretilen elektron taşıma zincirinin hemen bitişiğinde yer almasıdır.",
                "Mitokondriyal DNA'nın mutajenik duyarlılık nedenleri"
            ),
            make_flashcard(
                "k1-08-fc-11",
                "Mitofaji (mitokondriyal seçici otofaji) sürecinde hasarlı organeli tespit edip işaretleyen anahtar protein çifti hangisidir?",
                "Dış zarda biriken kinaz olan PINK1 ve sitozolden gelip organeli ubikitinleyen E3 ligaz olan Parkin proteinidir.",
                "Mitofajinin temel düzenleyici protein çifti"
            ),
            make_flashcard(
                "k1-08-fc-12",
                "Mitokondri hasarında ATP tükenmesi ile iç zar geçirgenliği artışının (sitokrom c salınımı) yol açtığı hücre ölüm tipleri sırasıyla hangileridir?",
                "Masif ATP tükenmesi iyon pompalarını durdurarak nekroza (onkozis); sitokrom c salınımı ise kaspaz kaskadını başlatarak apoptoza yol açar.",
                "Mitokondriyal hasarın nekroz ve apoptoz ayrımı"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Mitokondri iç zar potansiyeli çöktüğünde dış zarda birikerek Parkin ligazını çağıran kinaz proteini PINK1 proteinidir.",
                "PINK1",
                "Mitofaji sürecini başlatan mitokondriyal kinaz"
            )
        ]
    })

    # ADIM 40
    slides.append({
        "slideNumber": 40,
        "title": "Mitokondri Hedefli Yaşlanma Karşıtı Stratejiler ve Sentez",
        "subtitle": "Mitokondriyal antioksidanlar (MitoQ), NAD+ öncülleri (NMN/NR) ve biyojenez uyarımı",
        "badge": "Mitokondriyal Tedavi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Mitokondriyal disfonksiyonun hücresel yaşlanmadaki merkezi rolünün anlaşılması, doğrudan organel içine "
            "ulaşabilen yeni nesil farmakolojik yaklaşımların geliştirilmesini sağlamıştır. Klasik antioksidanlar "
            "mitokondriye giremezken, trifenilfosfonyum (TPP+) katyonu ile eşleştirilen moleküller (örneğin 'MitoQ') "
            "iç zar potansiyelini kullanarak mitokondri matriksinde yüzlerce kat yoğunlaşır ve radikalleri kaynağında söndürür.\n\n"
            "> [KLİNİK İPUCU] Diğer devrimsel strateji NAD+ düzeylerini artırmaktır; NMN ve NR gibi NAD+ öncülleri sirtuinleri "
            "(SIRT1/SIRT3) ve PGC-1α'yı aktive ederek mitokondriyal biyojenezi ve mitofajiyi tetikler.\n\n"
            "Bu müdahaleler, yaşlanan organlarda hücresel enerji metabolizmasını restore etmeyi amaçlar."
        ),
        "medicalTerms": [
            {"term": "MitoQ", "explanation": "Mitokondri içine seçici olarak girip biriken mitokondri hedefli koenzim Q türevi antioksidandır."},
            {"term": "PGC-1α", "explanation": "Yeni mitokondri yapımını (biyojenez) ve oksidatif solunumu yöneten ana transkripsiyon koaktivatörüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] MitoQ mitokondri içine seçici giren hedefli antioksidandır.",
            "📌 [SINAV SPOTU] PGC-1α mitokondriyal biyojenezi yöneten anahtar faktördür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hedefli Antioksidan", "desc": "MitoQ ile serbest radikalleri mitokondri matriksinde yakalama.", "isKey": True},
                {"title": "Biyojenez Uyarımı", "desc": "NAD+/SIRT1/PGC-1α aksı ile taze mitokondri üretimini tetikleme.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Deneysel bir araştırmada yaşlanan kas hücrelerinde yeni mitokondri üretimini (biyojenez) ve oksidatif kapasiteyi artırmak amacıyla bir genetik faktör aşırı eksprese ettiriliyor. Bu amaçla uyarılması gereken anahtar transkripsiyon koaktivatörü hangisidir?",
                [
                    {
                        "text": "CHOP apoptoz faktörü",
                        "isCorrect": False,
                        "feedback": "CHOP ER stresinde apoptozu başlatır; mitokondri yapmaz."
                    },
                    {
                        "text": "PGC-1α (Peroksizom proliferatör aktif reseptör gama koaktivatör 1-alfa)",
                        "isCorrect": True,
                        "feedback": "Tebrikler! PGC-1α mitokondriyal biyojenezin ve enerji metabolizmasının ana şef regülatörüdür."
                    }
                ]
            ),
            make_active_recall(
                "Mitokondri hedefli antioksidanların (örneğin MitoQ) klasik C ve E vitaminlerine göre en temel üstünlüğü nedir?",
                "Pozitif yüklü lipofilik katyonlar sayesinde mitokondri iç zarına ve matriksine seçici olarak girip yüzlerce kat yoğunlaşarak serbest radikalleri tam üretim odağında etkisizleştirebilmesidir."
            )
        ]
    })

    return slides
