"""
Deck 54 - Section 5: Plasenta Anatomisi ve Histolojisi (Slayt 41-50)
Slayt 50: Checkpoint 5
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec5_slides():
    slides = []
    
    # Slide 41
    slides.append(make_slide(
        slide_num=41,
        title="Plasenta Anatomisi: Genel Boyutlar ve Komponentler",
        subtitle="Disk çapı, kalınlığı, desidual tabaka ve villöz parankim",
        clinical_focus="Normal term plasentanın makroskobik mimarisi ve ağırlığı",
        narrative=(
            "Plasenta, intrauterin yaşam boyunca fetüs ile anne arasındaki metabolik, solunumsal ve endokrin alışverişi sağlayan geçici fakat hayati bir organdır. "
            "Miadında (termde) normal bir plasenta diskoid şekilde olup yaklaşık **15-20 cm çapında**, 2-3 cm kalınlığında ve 500 gram ağırlığındadır.\n\n"
            "- **Dört Temel Komponent:** Plasental ünite anatomik olarak dört ana bileşenden meydana gelir: **1) Umbilikal kord (göbek kordonu)**, **2) Plasental membranlar (amniyon ve koryon)**, **3) Villöz parankim (kotiledonlar)** ve **4) Maternal desidual doku (bazal plak)**.\n"
            "- **Maternal ve Fetal Yüzler:** Fetal yüz parlak ve düzgün amniyon zarı ile kaplı olup kordon damarlarının dallandığı taraftır. Maternal yüz ise myometriumdan ayrılan, kotiledon adı verilen 15-20 adet çatlaklı lobülden oluşan desidua bazalisi içerir.\n\n"
            "> [!NOTE]\n"
            "> Termdeki normal bir plasenta diski 15-20 cm çapındadır ve dört temel anatomik komponentten meydana gelir."
        ),
        bullets=[
            "Termde disk çapı 15-20 cm, ağırlığı yaklaşık 500 gramdır",
            "Dört bileşen: Umbilikal kord, membranlar, villöz parankim, maternal desidua",
            "Fetal yüzey parlak amniyon zarı ve kord damarlarıyla örtülüdür",
            "Maternal yüzey 15-20 kotiledondan oluşan desidua bazalistir"
        ],
        elements=[
            make_quiz(
                question="Miadında (termde) normal bir insan plasentasının ortalama disk çapı ve anatomik komponentleri ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Termde plasenta çapı 3-5 cm olup yalnızca amniyon zarından ibarettir.", "isCorrect": False, "explanation": "3-5 cm çok küçüktür; normal term plasenta 15-20 cm çapındadır."},
                    {"key": "B", "text": "Termdeki plasenta 15-20 cm çapındadır; umbilikal kord, membranlar, villöz parankim ve maternal desiduadan oluşur.", "isCorrect": True, "explanation": "Doğru. Miadındaki plasenta 15-20 cm çapında olup bu dört temel komponenti içerir."},
                    {"key": "C", "text": "Plasenta hiçbir zaman maternal doku içermez; %100 oranında sadece fetal kıkırdaktan oluşur.", "isCorrect": False, "explanation": "Plasenta maternal desiduayı da içerir; kıkırdak barındırmaz."},
                    {"key": "D", "text": "Term plasenta çapı 50 cm'dir ve kotiledon lobülasyonu bulunmaz.", "isCorrect": False, "explanation": "50 cm kord uzunluğudur; plasenta diski 15-20 cm'dir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Miadındaki normal bir plasenta 15-20 cm çapındadır; umbilikal kord, membranlar, villöz parankim ve maternal desiduadan oluşur.",
                masked_term="15-20 cm çapındadır",
                hint="Term plasenta diskinin santimetre cinsinden ortalama genişliği"
            ),
            make_table(
                title="Plasental Yüzler ve Anatomik Özellikler",
                headers=["Yüzey", "Örtücü Tabaka", "Morfolojik Karakteristik"],
                rows=[
                    [
                        {"text": "Fetal Yüzey (İç)", "isMasked": False},
                        {"text": "Amniyon zarı", "isMasked": True, "hint": "Fetal sıvıyla temas eden şeffaf parlak örtü"},
                        {"text": "Parlak, düzgün; umbilikal damarların radyiter dallanması", "isMasked": False}
                    ],
                    [
                        {"text": "Maternal Yüzey (Dış)", "isMasked": False},
                        {"text": "Desidua bazalis", "isMasked": True, "hint": "Uterustan ayrılan anneye ait mukozal plak"},
                        {"text": "15-20 adet oluklarla ayrılmış koyu kırmızı kotiledon", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Termdeki normal bir insan plasentasının dört temel anatomik komponenti hangileridir?",
                answer="Umbilikal kord, plasental membranlar (amnion ve koryon), villöz parankim ve maternal desidual dokudur."
            )
        ]
    ))

    # Slide 42
    slides.append(make_slide(
        slide_num=42,
        title="Umbilikal Kord: Boyutlar, Wharton Jeli ve Damar Anatomisi",
        subtitle="55-60 cm uzunluk, mukoid konnektif doku ve 2 arter + 1 ven kuralı",
        clinical_focus="Kordon anomalileri ve damar sayısının klinik önemi",
        narrative=(
            "Umbilikal kord (göbek kordonu), fetüs ile plasenta diski arasındaki vasküler bağlantıyı sağlayan esnek anatomik köprüdür.\n\n"
            "- **Boyutlar:** Miadında normal bir göbek kordonu yaklaşık **55-60 cm uzunluğunda** ve 1.5-2 cm kalınlığındadır. Dış yüzü tek katlı yassı/küboid amniyotik epitel ile örtülüdür (fetal uca doğru çok katlılaşabilir).\n"
            "- **Wharton Jeli:** Kordonun gövdesi, fibroblastlar ve bol miktarda asidik mukopolisakkarit (hyaluronik asit) içeren, jelatinöz mukoid bağ dokusundan (**Wharton's jelly**) yapılmıştır. Bu jel damarların bükülmesini, bası altında ezilmesini ve trombozunu önleyen elastik bir yastık görevi görür.\n"
            "- **Damar Sayısı (2 Arter, 1 Ven):** Wharton jeli içinde helikal olarak dönen **2 adet umbilikal arter** ve **1 adet umbilikal ven** yer alır. Ven oksijenlenmiş temiz kanı fetüse taşırken, 2 arter venöz kirli kanı plasentaya geri getirir.\n\n"
            "> [!IMPORTANT]\n"
            "> Termdeki umbilikal kord 55-60 cm uzunluğundadır; Wharton jeli içinde 2 arter ve 1 ven yer alır (tek umbilikal arter saptanması fetal konjenital anomali uyarısıdır)."
        ),
        bullets=[
            "Termde kordon uzunluğu ortalama 55-60 cm'dir",
            "Gövdesi elastik mukoid Wharton jeli ile doludur",
            "Wharton jeli içinde 2 adet umbilikal arter ve 1 adet umbilikal ven bulunur",
            "Ven temiz kanı taşır; arterler venöz kanı plasentaya iletir"
        ],
        elements=[
            make_quiz(
                question="Termdeki normal bir umbilikal kordonun uzunluğu ve Wharton jeli içinde taşıdığı normal damar kombinasyonu hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "15-20 cm — 1 arter ve 2 ven", "isCorrect": False, "explanation": "15-20 cm plasenta çapıdır; kordon 55-60 cm'dir ve 2 arter, 1 ven taşır."},
                    {"key": "B", "text": "55-60 cm — 2 arter ve 1 ven", "isCorrect": True, "explanation": "Doğru. Termde kordon 55-60 cm olup Wharton jeli içinde 2 arter ve 1 ven içerir."},
                    {"key": "C", "text": "100 cm — 3 arter ve 3 ven", "isCorrect": False, "explanation": "Aşırı uzun kordon anomalisi ve gerçek dışı damar sayısıdır."},
                    {"key": "D", "text": "30 cm — Saf lenfatik damarlar", "isCorrect": False, "explanation": "Kordonda lenfatik damar bulunmaz; 2 arter ve 1 ven vardır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Termdeki umbilikal kord yaklaşık 55-60 cm olup konnektif doku içinde 2 arter ve 1 ven vardır.",
                masked_term="2 arter ve 1 ven",
                hint="Göbek kordonundaki normal kan damarı dağılım sayısı"
            ),
            make_chain(
                "Fetoplasental Dolaşım Zinciri",
                [
                    "1. Pulmoner/Sistemik Dönüş: Fetüsün desatüre venöz kanı 2 adet umbilikal arter yoluyla plasenta villuslarına pompalanır.",
                    "2. Villöz Difüzyon: Koryonik villus kapillerlerinde anne kanıyla gaz değişimi yapılır; oksijen kana difüze olur.",
                    "3. Oksijenli Kan İletimi: Oksijenlenmiş temiz kan tek bir geniş umbilikal ven aracılığıyla duktus venozus üzerinden fetal dolaşıma aktarılır."
                ]
            ),
            make_recall(
                question="Yeni doğan bebeğin göbek kordonu kesitinde 2 arter yerine tek bir umbilikal arter saptanması klinisyeni hangi risk açısından uyarır?",
                answer="Kardiyovasküler ve renal sistem konjenital malformasyonları (özellikle trizomiler) açısından araştırma uyarısıdır."
            )
        ]
    ))

    # Slide 43
    slides.append(make_slide(
        slide_num=43,
        title="Plasental Kord İnsersiyonu: Battledore Plasenta",
        subtitle="Santral, eksantrik, marjinal (battledore) ve velamentöz insersiyon",
        clinical_focus="Kordon yapışma yeri varyasyonları ve marjinal insersiyon",
        narrative=(
            "Umbilikal kord normal koşullarda plasenta diskinin geometrik merkezine (santral) veya merkeze yakın bir bölgesine (eksantrik) insere olur. "
            "Ancak bazı olgularda kordon giriş yerinde gelişimsel anatomik varyasyonlar ortaya çıkar.\n\n"
            "- **Battledore Plasenta (Marjinal İnsersiyon):** Umbilikal kordun plasenta diskinin tam periferik kenarına yapışması durumuna **battledore plasenta** adı verilir. Bu görünüm eski tip tahta tenis raketine (battledore) benzetilmiştir.\n"
            "- **Klinik Risk:** Marjinal giriş, doğum sırasında kordona binen traksiyon kuvvetlerinin kordun plasentadan erken ayrılmasına (avülsiyon) ve fetal distrese yol açma riskini artırır.\n"
            "- **Velamentöz İnsersiyon Ayrımı:** Battledore plasentada kordon kenara yapışsa da damarlar disk dokusu üzerindedir; velamentöz insersiyonda ise kord membranlara yapışır ve damarlar çıplak kalarak yırtılma riski (vasa previa) taşır.\n\n"
            "> [!NOTE]\n"
            "> Umbilikal kordun plasenta diskinin tam kenar sınırından giriş yapmasına 'battledore plasenta' denir."
        ),
        bullets=[
            "Normal giriş diskin santralinde veya eksantriğindedir",
            "Battledore plasenta: Kordonun plasentanın tam kenarına (marjinal) yapışmasıdır",
            "Raket benzeri morfolojik konfigürasyon sergiler",
            "Doğum eyleminde traksiyonla kopma ve bası riski oluşturabilir"
        ],
        elements=[
            make_quiz(
                question="Umbilikal kordonun plasenta diskinin merkezine değil de tam kenar marjinal sınırına yapışması ile karakterize anatomik varyasyona ne ad verilir?",
                options=[
                    {"key": "A", "text": "Plasenta perkreta", "isCorrect": False, "explanation": "Perkreta miyometriumu aşan invazyon anomalisidir; kord girişiyle ilgili değildir."},
                    {"key": "B", "text": "Plasenta süksentüriyata", "isCorrect": False, "explanation": "Aksesuar bir ek plasental lobun bulunmasıdır."},
                    {"key": "C", "text": "Sirkumvallat plasenta", "isCorrect": False, "explanation": "Membranların kenarda çift katlanıp fibröz halka oluşturmasıdır."},
                    {"key": "D", "text": "Battledore plasenta", "isCorrect": True, "explanation": "Doğru. Kordonun diskin tam marjinal kenarına girmesine battledore plasenta denir."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Umbilikal kord plasentaya merkez yerine en dış kısmından giriş yapabilir; bu giriş yaptığı kısım battledore plasenta olarak adlandırılır.",
                masked_term="battledore plasenta",
                hint="Marjinal kord girişine verilen raket benzetmeli terim"
            ),
            make_slider(
                left_title="Normal Kord Girişi",
                right_title="Battledore Plasenta Girişi",
                left_points=[
                    "Kordon plasenta diskinin merkezine veya merkeze yakınına girer",
                    "Traksiyon kuvvetleri plasenta gövdesine eşit dağılır",
                    "Doğumda kord kopma ve damar avülsiyon riski düşüktür"
                ],
                right_points=[
                    "Kordon diskin tam marjinal kenar sınırına yapışır",
                    "Kuvvetler kenarda toplanarak asimetrik gerilim yaratır",
                    "Doğum eyleminde kord avülsiyonu ve fetal distres riski artabilir"
                ]
            ),
            make_recall(
                question="Battledore plasenta terimi plasentanın hangi anatomik özelliğini tanımlar?",
                answer="Umbilikal kordonun plasenta diskine merkezden değil, tam periferik kenarından (marjinal) yapışmasını tanımlar."
            )
        ]
    ))

    # Slide 44
    slides.append(make_slide(
        slide_num=44,
        title="Plasental Membranlar: Amniyon, Koryon ve Skuamöz Metaplazi",
        subtitle="Tek tabaka amniyotik epitel ve kord girişinde skuamöz adacıklar",
        clinical_focus="Fetal membranların histolojisi ve fizyolojik metaplastik lezyonlar",
        narrative=(
            "Plasental membranlar (fetal zarlar), amniyotik kaviteyi çepeçevre sararak bebeği steril bir sıvı ortamda koruyan amniyon ve koryon katmanlarından oluşur.\n\n"
            "- **Amniyon Histolojisi:** Amniyotik sıvıyla doğrudan temas eden en iç tabakadır. Bazal membran üzerinde oturan tek katlı yassı veya alçak küboid epitelyal hücrelerle döşelidir.\n"
            "- **Amniyonda Skuamöz Metaplazi:** Özellikle umbilikal kordun plasentaya giriş bölgesine yakın alanlarda tek katlı amniyotik epitel çok katlı yassı epitele dönüşebilir (**skuamöz metaplazi**). Bu durum makroskopide amniyon yüzeyinde beyazımsı, sedefimsi, 1-2 mm'lik sert pürüzler şeklinde görülür; tamamen benign ve fizyolojik bir metaplazidir, hiçbir malignite potansiyeli taşımaz.\n"
            "- **Koryon Tabakası:** Amniyonun dış yüzeyinde yer alan konnektif dokudur; fetal vasküler yapıları taşır ve trofoblastik hücrelerle temas eder.\n\n"
            "> [!NOTE]\n"
            "> Amniyotik zarda, özellikle kordon giriş bölgesinde skuamöz metaplazi sıktır; makroskopik beyaz nodüller selimdir."
        ),
        bullets=[
            "Membranlar içte amniyon, dışta koryon katmanlarından oluşur",
            "Amniyon tek katlı yassı-küboid epitelle döşelidir",
            "Kordon giriş yerinde amniyonda skuamöz metaplazi sıktır",
            "Metaplastik odaklar selimdir; malignite veya enfeksiyon göstergesi değildir"
        ],
        elements=[
            make_quiz(
                question="Term plasentasının fetal yüzeyinde, özellikle umbilikal kordun giriş yerine yakın amniyon zarında sıkça rastlanan ve selim kabul edilen metaplastik epitel değişikliği hangisidir?",
                options=[
                    {"key": "A", "text": "Müsinöz intestinal metaplazi", "isCorrect": False, "explanation": "İntestinal metaplazi midede gastrit zemininde görülür; amniyonda izlenmez."},
                    {"key": "B", "text": "Kemikleşme (osseöz metaplazi)", "isCorrect": False, "explanation": "Amniyonda kemikleşme tipik değildir."},
                    {"key": "C", "text": "Skuamöz metaplazi", "isCorrect": True, "explanation": "Doğru. Amniyon zarında, özellikle kord girişinde tek katlı epitelin çok katlı yassı epitele dönüşmesi (skuamöz metaplazi) sıktır ve selimdir."},
                    {"key": "D", "text": "Apokrin metaplazi", "isCorrect": False, "explanation": "Apokrin metaplazi meme duktuslarında görülür."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Amniyotik kaviteyi çevreleyen amniyon zarı tek tabaka yassı epitel ile döşelidir ve kordun giriş yerinde skuamöz metaplazi sıktır.",
                masked_term="skuamöz metaplazi",
                hint="Çok katlı yassı epitel transformasyonu"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Plasental Membran Histolojisi",
                items=[
                    {"text": "Amniyon zarı bazal membran üzerinde tek tabaka epitel içerir.", "isLie": False, "explanation": "Doğru. Normal amniyon tek katlıdır."},
                    {"text": "Kord girişine yakın alanlarda amniyonda skuamöz metaplazi adacıkları görülebilir.", "isLie": False, "explanation": "Doğru. Skuamöz adacıklar sık ve selimdir."},
                    {"text": "Amniyondaki skuamöz metaplazi odakları anaplastik invaziv skuamöz kanserin habercisidir.", "isLie": True, "explanation": "Tuzak! Amniyondaki skuamöz metaplazi fizyolojik ve tamamen selim bir değişimdir; maligniteye dönüşmez."},
                    {"text": "Koryon tabakası fetal vasküler yapıları taşıyan fibröz konnektif dokudur.", "isLie": False, "explanation": "Doğru. Amniyon ile villuslar arasında yer alır."}
                ]
            ),
            make_recall(
                question="Amniyon zarında makroskopik olarak beyaz sedefimsi minik nodüller şeklinde izlenen metaplazi tipi nedir?",
                answer="Kordon giriş yerine komşu amniyonda sıkça izlenen selim 'skuamöz metaplazi' odaklarıdır."
            )
        ]
    ))

    # Slide 45
    slides.append(make_slide(
        slide_num=45,
        title="Koryon Villus Histolojisi: Sito- ve Sinsityotrofoblastlar",
        subtitle="İçte tek tek sitotrofoblastlar, dışta multinükleer sinsityum",
        clinical_focus="Koryon villuslarının trofoblastik örtüsü ve hücresel rolleri",
        narrative=(
            "Koryonik villuslar plasentanın anne kanıyla doğrudan temas eden fonksiyonel birimleridir. Villusların yüzeyi iki farklı trofoblast hücresi tarafından döşenir:\n\n"
            "- **Sinsityotrofoblastlar (Dış Tabaka):** Anne kanının bulunduğu intervillöz aralıkla doğrudan temas eden dış tabakadır. Hücre sınırları bulunmayan, bol koyu **eozinofilik (pembe) sitoplazmalı, multinükleer dev sinsityal örtüdür**. Başta hCG, hPL ve steroid hormonların sentezinden ve besin transferinden sorumludur.\n"
            "- **Sitotrofoblastlar (Langhans Hücreleri - İç Tabaka):** Sinsityotrofoblast tabakasının hemen altında, bazal membrana oturan tek tek dizilmiş hücrelerdir. **Belirgin hücre sınırları ve soluk berrak sitoplazmaları** vardır; sinsityotrofoblastları yenileyen kök hücre havuzudur.\n"
            "- **Maturasyonel Değişim:** Erken gebelikte her iki tabaka belirginken, miadında sitotrofoblastlar atrofiye uğrar.\n\n"
            "> [!IMPORTANT]\n"
            "> Sinsityotrofoblastlar eozinofilik multinükleer dev sinsityumdur ve hCG salgılar; sitotrofoblastlar ise berrak sitoplazmalı, belirgin sınırlı kök hücrelerdir."
        ),
        bullets=[
            "Sinsityotrofoblast: Dışta yer alır, multinükleer dev sinsityumdur, hCG üretir",
            "Sitotrofoblast: İçte yer alır, belirgin sınırlı, berrak sitoplazmalıdır",
            "Sitotrofoblastlar mitozla çoğalarak sinsityotrofoblastları oluşturur",
            "İki tabaka intervillöz kan ile fetal stroma arasında bariyer kurar"
        ],
        elements=[
            make_quiz(
                question="Normal koryonik villusların mikroskobisinde dış tabakayı oluşturan, anne kanıyla doğrudan temas eden, bol eozinofilik sitoplazmalı ve multinükleer dev hücre karakterinde olan hücre tipi hangisidir?",
                options=[
                    {"key": "A", "text": "Sitotrofoblast", "isCorrect": False, "explanation": "Sitotrofoblast içtedir, tek nükleuslu ve belirgin sınırlıdır."},
                    {"key": "B", "text": "Hofbauer hücresi", "isCorrect": False, "explanation": "Hofbauer hücresi stroma içindeki fetal makrofajdır; yüzey epiteli değildir."},
                    {"key": "C", "text": "Sinsityotrofoblast", "isCorrect": True, "explanation": "Doğru. Sinsityotrofoblastlar multinükleer dev sinsityum yapısında olup eozinofilik sitoplazmalıdır ve hCG salgılarlar."},
                    {"key": "D", "text": "Desidual stromal hücre", "isCorrect": False, "explanation": "Desidua maternal uterin hücredir; villus örtüsü değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Villuslar sinsityo ve sitotrofoblastik hücrelerle döşelidir; sinsityotrofoblastlar bol eozinofilik sitoplazmalı multinükleer dev hücrelerdir.",
                masked_term="multinükleer dev hücrelerdir",
                hint="Membran sınırları kaybolmuş çok çekirdekli sinsityal kitle"
            ),
            make_slider(
                left_title="Sinsityotrofoblast Özellikleri",
                right_title="Sitotrofoblast Özellikleri",
                left_points=[
                    "Villusun en dış tabakasında yer alır",
                    "Hücre sınırları belirsizdir, multinükleer sinsityumdur",
                    "Bol eozinofilik sitoplazmalıdır; hormon (hCG) üretir"
                ],
                right_points=[
                    "İçte bazal membran üzerinde yer alır",
                    "Hücre sınırları çok belirgindir (Langhans hücreleri)",
                    "Soluk-berrak sitoplazmalıdır; proliferatif kök hücredir"
                ]
            ),
            make_recall(
                question="Koryonik villuslarda hCG hormonunun primer sentez yeri olan ve anne kanıyla temas eden dev hücre tabakası hangisidir?",
                answer="Multinükleer eozinofilik 'sinsityotrofoblast' tabakasıdır."
            )
        ]
    ))

    # Slide 46
    slides.append(make_slide(
        slide_num=46,
        title="Koryon Villus Maturasyonu: Erken vs Term Plasenta",
        subtitle="Erken gebelikte çift tabaka, termde sinsityal düğümler ve ince bariyer",
        clinical_focus="Plasental yaşlanma ve gaz difüzyon kapasitesinin mikroskobisi",
        narrative=(
            "Koryonik villuslar gebelik haftaları ilerledikçe fetüsün artan oksijen ve besin talebini karşılamak üzere belirgin bir maturasyonel (olgunlaşma) değişime uğrarlar.\n\n"
            "- **Erken Gebelik Villusları:** Geniş çaplıdır. Stroması gevşek ve ödematözdür. Villus çevresinde **çift tabaka trofoblast** (içte belirgin sitotrofoblast, dışta sinsityotrofoblast) kesintisiz bir bariyer oluşturur. Fetal kapillerler villusun merkezinde yer alır.\n"
            "- **Term (Miadında) Plasenta Villusları:** Villuslar küçülmüş ve dallanmıştır. Sitotrofoblast tabakası atrofiye uğrayarak mikroskop altında adeta **belirsiz hale gelmiştir**. Sinsityotrofoblast çekirdekleri kümelenerek karakteristik **sinsityal düğümleri (syncytial knots)** oluşturur.\n"
            "- **Vaskülosinsityal Membran:** Fetal kapillerler villus periferine kayarak incelmiş sinsityotrofoblast örtüsüne doğrudan yapışır; böylece anne kanı ile fetal kan arasındaki difüzyon mesafesi minimuma iner.\n\n"
            "> [!NOTE]\n"
            "> Term plasentada sitotrofoblastlar belirsizleşir, sinsityal düğümler belirir ve fetal kapillerler periferik yerleşerek difüzyon hızını maksimize eder."
        ),
        bullets=[
            "Erken plasenta: Geniş villuslar, çift tabaka trofoblast örtüsü",
            "Term plasenta: Küçük dallanmış villuslar, tek tabaka incelmiş örtü",
            "Termde sitotrofoblastlar belirsizleşir; sinsityal düğümler kümelenir",
            "Fetal kapillerler periferikleşerek vaskülosinsityal difüzyon membranını kurar"
        ],
        elements=[
            make_quiz(
                question="Miadında (termde) normal bir plasentanın mikroskobik incelemesinde erken gebelik villuslarına kıyasla saptanan en karakteristik maturasyonel bulgu nedir?",
                options=[
                    {"key": "A", "text": "Sitotrofoblastların devasa hiperplazi göstererek villusları tamamen tıkaması", "isCorrect": False, "explanation": "Sitotrofoblastlar termde çoğalmaz; tam tersine atrofiye uğrayarak belirsizleşir."},
                    {"key": "B", "text": "Sitotrofoblastların belirsizleşmesi, sinsityal düğümlerin kümelenmesi ve fetal kapillerlerin periferikleşmesi", "isCorrect": True, "explanation": "Doğru. Termde difüzyonu artırmak için sitotrofoblastlar silinir, sinsityal nükleuslar düğümlenir ve kapillerler dış sınıra dayanır."},
                    {"key": "C", "text": "Villus içi tüm fetal kapillerlerin trombozla oblitere olması", "isCorrect": False, "explanation": "Patolojik enfarktüs bulgusudur; fizyolojik maturasyon değildir."},
                    {"key": "D", "text": "Villus stromasının yoğun kıkırdak metaplazisine uğraması", "isCorrect": False, "explanation": "Kıkırdak metaplazisi plasentada izlenmez."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Term plasentada sitotrofoblastlar belirsizdir ve sinsityotrofoblastlar sinsityal kümeler halinde tomurcuklanırlar.",
                masked_term="sinsityal kümeler",
                hint="Çekirdeklerin oluşturduğu multinükleer agregatlar (syncytial knots)"
            ),
            make_table(
                title="Erken Gebelik vs Term Plasenta Villus Karşılaştırması",
                headers=["Özellik", "Erken Gebelik Villusu", "Term (Miadında) Villus"],
                rows=[
                    [
                        {"text": "Villus Çapı", "isMasked": False},
                        {"text": "Geniş ve kalın villuslar", "isMasked": False},
                        {"text": "Küçük, ince ve dallanmış", "isMasked": True, "hint": "Yüzey alanını artıran dar mikromorfometri"}
                    ],
                    [
                        {"text": "Sitotrofoblast Tabakası", "isMasked": False},
                        {"text": "Kesintisiz ve belirgin iç tabaka", "isMasked": False},
                        {"text": "Atrofik ve belirsizleşmiş", "isMasked": True, "hint": "Gözden kaybolacak kadar silinmiş"}
                    ],
                    [
                        {"text": "Sinsityotrofoblast Nükleusları", "isMasked": False},
                        {"text": "Düzenli periferik dağılım", "isMasked": False},
                        {"text": "Sinsityal düğümler (kümeler)", "isMasked": True, "hint": "Karakteristik çekirdek yığılmaları"}
                    ]
                ]
            ),
            make_recall(
                question="Term plasenta villuslarında fetal kapillerlerin periferikleşerek sinsityotrofoblasta yapışmasının fizyolojik amacı nedir?",
                answer="Anne kanı ile fetal kan arasındaki mesafeyi incelterek oksijen ve karbondioksit difüzyon hızını en üst düzeye çıkarmaktır."
            )
        ]
    ))

    # Slide 47
    slides.append(make_slide(
        slide_num=47,
        title="Plasenta İnflamasyonu: Asendan Yol ve Koryoamnionit",
        subtitle="Erken membran rüptürü, bakteriyel flora ve nötrofilik infiltrasyon",
        clinical_focus="Koryoamnionitin patogenezi, histolojisi ve fetal vaskülit riski",
        narrative=(
            "Plasental dokunun enfeksiyonları iki temel anatomik yoldan biriyle organa ulaşır: **asendan (yukarı çıkan) yol** veya **hematojen (transplasental) yol**.\n\n"
            "- **En Sık İletim Yolu:** Doğum kanalından yukarıya doğru ilerleyen **asendan enfeksiyonlar açık ara daha sıktır** ve olguların ezici çoğunluğunda bakteriyel kökenlidir.\n"
            "- **Tetikleyici ve Etkenler:** Vajinal floraya ait bakteriler, mikoplazmalar veya kandidalar servikal kanalı aşarak membranlara ulaşır; sıklıkla **erken membran rüptürü (EMR)** ve preterm eylemle birliktedir.\n"
            "- **Histopatoloji (Korioamnionit):** Amniyon ve koryon zarlarında konjesyon, ödem ve yoğun **nötrofil lökosit infiltrasyonu (korioamnionit)** izlenir.\n"
            "- **Fetal Vaskülit (Funisit):** Enfeksiyon membranlardan göbek kordonuna ilerlediğinde umbilikal ven ve arter duvarlarında akut nötrofilik vaskülit (**funisit**) gelişir; bu durum fetal sepsisin habercisidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Plasentaya asendan enfeksiyonlar çok daha sıktır, bakteriyeldir ve koryoamnionit oluşturur; kordona yayılım funisite (akut fetal vaskülit) yol açar."
        ),
        bullets=[
            "Asendan (doğum kanalından yukarı) enfeksiyonlar en sık yoldur",
            "Çoğu olguda bakteriyeldir; erken membran rüptürü ile ilişkilidir",
            "Koryoamnion zarlarında yoğun nötrofilik infiltrasyon (korioamnionit) yapar",
            "Kordon damarlarına yayılarak akut vaskülit (funisit) tablosu doğurur"
        ],
        elements=[
            make_quiz(
                question="Gebelikte plasenta ve fetal zarların enfeksiyonlarında mikroorganizmaların en sık kullandığı bulaş yolu ve oluşturduğu temel histopatolojik tablo hangisidir?",
                options=[
                    {"key": "A", "text": "Hematojen yol — Kazeifiye granülomatöz villit", "isCorrect": False, "explanation": "Hematojen yol daha nadirdir; transplasental villit yapar."},
                    {"key": "B", "text": "Asendan yol — Zarlarda nötrofilik korioamnionit", "isCorrect": True, "explanation": "Doğru. Asendan yol en sık bulaş yoludur, bakteriyeldir ve fetal zarlarda nötrofilik korioamnionite yol açar."},
                    {"key": "C", "text": "Retrograd lenfatik yol — Wharton jeli kalsifikasyonu", "isCorrect": False, "explanation": "Lenfatik yayılım plasental enfeksiyonda primer yol değildir."},
                    {"key": "D", "text": "Transfallopik dökülme — Amniyon skuamöz metaplazisi", "isCorrect": False, "explanation": "Skuamöz metaplazi enfeksiyon değil selim bir fizyolojik değişimdir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Doğum kanalından yukarıya doğru ulaşan asendan infeksiyonlar daha sıktır, çoğu olguda bakteriyeldir ve koryoamnionda nötrofiller ile korioamnionit oluşturur.",
                masked_term="korioamnionit",
                hint="Amniyon ve koryon zarlarının akut nötrofilik iltihabı"
            ),
            make_chain(
                "Asendan Plasental Enfeksiyon Yayılım Zinciri",
                [
                    "1. Vajinal Kolonizasyon ve EMR: Vajinal bakteriler serviksi aşar veya erken membran rüptürü zemininde amniyotik boşluğa girer.",
                    "2. Koryoamnion Zarlarının İltihabı: Bakteriyel toksinler koryon ve amniyon zarlarında yoğun nötrofil birikimi ve ödem (korioamnionit) başlatır.",
                    "3. Umbilikal Vaskülit (Funisit): İnflamasyon göbek kordonuna sıçrayarak umbilikal damar duvarlarında lökositik infiltrasyon ve fetal sepsis riski üretir."
                ]
            ),
            make_recall(
                question="Koryoamnionitli bir gebenin plasentasında enfeksiyonun umbilikal kordondaki damarlara sıçraması patolojide hangi özel terimle adlandırılır?",
                answer="Akut funisit (göbek kordonu damarlarının akut lökositik vasküliti) olarak adlandırılır."
            )
        ]
    ))

    # Slide 48
    slides.append(make_slide(
        slide_num=48,
        title="Plasenta İnflamasyonu: Hematojen Yol, Villit ve TORCH",
        subtitle="Transplasental yayılım, koryon villiti ve konjenital enfeksiyonlar",
        clinical_focus="Hematojen enfeksiyonların villit paterni ve fetal anomali riski",
        narrative=(
            "Plasentaya mikroorganizmaların ikinci ulaşma yolu anne kan dolaşımı aracılığıyla gerçekleşen **hematojen (transplasental) yoldur**.\n\n"
            "- **Histopatolojik Tablo (Villitis):** Asendan yolda membranlar (korioamnionit) tutulurken, hematojen yolda mikroorganizmalar doğrudan anne kanının yıkadığı intervillöz aralıktan koryonik villuslara saldırır; bu nedenle temel histolojik tablo **villit (villitis)** olarak adlandırılır.\n"
            "- **Etkenler:** Sifiliz (Treponema pallidum), listeriozis, tüberküloz, toksoplazmozis, kandidiazis ve başta kızamıkçık (rubella), sitomegalovirüs (CMV) ve herpes simpleks (HSV) olmak üzere çeşitli virüsler plasental villitise neden olur.\n"
            "- **TORCH Kompleksi:** Bu hematojen transplasental enfeksiyonlar plasental bariyeri aşarak doğrudan fetüse geçer ve mikrosefali, korioretinit, intrakraniyal kalsifikasyonlar ve sağırlık gibi ağır fetal hasarlarla seyreden **TORCH kompleksini** oluştururlar.\n\n"
            "> [!IMPORTANT]\n"
            "> Hematojen transplasental enfeksiyonlar histolojik olarak villusları tutarak villite yol açar; fetüse geçerek TORCH kompleksi anomalilerini doğurur."
        ),
        bullets=[
            "Anne kanı yoluyla intervillöz aralıktan ulaşan hematojen enfeksiyondur",
            "Histolojik olarak villus parankimini tutarak villit (villitis) yapar",
            "Etkenler: Sifiliz, listeria, toksoplazma, CMV, rubella, HSV",
            "Plasental bariyeri aşarak fetüste klasik TORCH kompleksini oluşturur"
        ],
        elements=[
            make_quiz(
                question="Plasentanın hematojen (transplasental) enfeksiyonlarının histopatolojik incelemesinde en sık tutulan doku komponenti ve klinik yansıması hangisidir?",
                options=[
                    {"key": "A", "text": "Koryon villusları (Villit) — Fetal TORCH kompleksi", "isCorrect": True, "explanation": "Doğru. Hematojen yayılımda koryon villusları tutulur (villit) ve enfeksiyon fetüse geçerek TORCH tablosuna yol açar."},
                    {"key": "B", "text": "Wharton jeli — Battledore plasenta gelişimi", "isCorrect": False, "explanation": "Battledore anatomik kord girişidir; enfeksiyonla ilgisi yoktur."},
                    {"key": "C", "text": "Amniyotik tek katlı epitel — Skuamöz karsinom", "isCorrect": False, "explanation": "Amniyonda karsinom gelişmez."},
                    {"key": "D", "text": "Myometrium düz kası — Leiomyom torsiyonu", "isCorrect": False, "explanation": "Leiomyom düz kas neoplazmıdır; transplasental enfeksiyon tutulum yeri değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Hematojen yolla ulaşan transplasental infeksiyonlar histolojik olarak villusları tutarak villit oluşturur ve fetüsü etkileyerek TORCH kompleksi antitesine yol açar.",
                masked_term="TORCH kompleksi",
                hint="Toksoplazma, Rubella, CMV, Herpes konjenital sendrom grubu"
            ),
            make_slider(
                left_title="Asendan Plasental Enfeksiyon",
                right_title="Hematojen Plasental Enfeksiyon",
                left_points=[
                    "Bulaş: Vajina ve doğum kanalından yukarıya doğru",
                    "Primer tutulan doku: Amniyon ve koryon zarları",
                    "Histopatolojik tanı: Nötrofilik korioamnionit",
                    "Klinik ilişki: Erken membran rüptürü ve erken doğum"
                ],
                right_points=[
                    "Bulaş: Anne kan dolaşımı ile intervillöz aralığa",
                    "Primer tutulan doku: Koryon villusları parankimi",
                    "Histopatolojik tanı: Kronik/granülomatöz villit (villitis)",
                    "Klinik ilişki: Fetal anomaliler ve TORCH sendromu"
                ]
            ),
            make_recall(
                question="Plasentaya ulaşan asendan ve hematojen enfeksiyonların histopatolojik tutulum odakları arasındaki temel fark nedir?",
                answer="Asendan enfeksiyonlar fetal zarları tutarak 'korioamnionit' yaparken; hematojen enfeksiyonlar koryon villuslarını tutarak 'villit' yapar."
            )
        ]
    ))

    # Slide 49
    slides.append(make_slide(
        slide_num=49,
        title="Plasenta İnflamasyonunda Ayırıcı Tanı ve Patojenler",
        subtitle="Asendan bakteriler vs transplasental virüs ve parazitler",
        clinical_focus="Korioamnionit ve villitis olgularında mikrobiyolojik etkenler",
        narrative=(
            "Plasental inflamasyonun patolojik tanısında histolojik patern (korioamnionit vs villitis) altta yatan mikroorganizma sınıfını öngörmede yol göstericidir.\n\n"
            "- **Korioamnionit Patojenleri:** Asendan yolla gelen etkenlerdir. En sık vajinal anaeroplar, Grup B Streptokoklar (S. agalactiae), E. coli, Ureaplasma urealyticum, Mycoplasma hominis ve Candida türleridir. Amniyon sıvısı bulanık, pürülan ve kötü kokuludur.\n"
            "- **Villitis Patojenleri:** Hematojen anne bakteriyemisi veya viremisinden kaynaklanır. Treponema pallidum (solgun soliter villuslar, spiroketler), Listeria monocytogenes (mikroapseler), Mycobacterium tuberculosis (kazeifiye granülomlar), Toxoplasma gondii ve Sitomegalovirüs (dev hücre içi nükleer baykuş gözü inklüzyonlar) tipik villit yapıcı ajanlardır.\n\n"
            "> [!NOTE]\n"
            "> Zarlarda nötrofilik infiltrasyon bakteriyel asendan korioamnioniti; villus parankimindeki mononükleer iltihap ise transplasental hematojen villiti işaret eder."
        ),
        bullets=[
            "Korioamnionit: Vajinal flora bakterileri, GBS, E. coli, mikoplazma",
            "Villitis: Treponema, Listeria, Tbc, Toxoplasma, CMV, Rubella",
            "Listeria mikroapseli villit; Tbc granülomatöz villit yapar",
            "CMV sinsityotrofoblastlarda baykuş gözü inklüzyonlar oluşturur"
        ],
        elements=[
            make_swipe(
                title="Plasental Enfeksiyon Refleks Eşleme",
                left_category="Asendan Korioamnionit",
                right_category="Hematojen Transplasental Villit",
                cards=[
                    {"text": "Erken membran rüptürü sonrası fetal membranlarda nötrofil infiltrasyonu.", "category": "left", "explanation": "Doğum kanalından yukarı çıkan bakteriyel korioamnionittir."},
                    {"text": "Koryon villusları tutularak fetüste konjenital TORCH anomalileri oluşturulması.", "category": "right", "explanation": "Hematojen yayılımla gelişen villit ve fetal enfeksiyondur."},
                    {"text": "Vajinal flora bakterileri ve mikoplazmaların servikal kanaldan yayılması.", "category": "left", "explanation": "Asendan bakteriyel bulaş yoludur."},
                    {"text": "CMV, sifiliz ve toksoplazmanın anne kanı yoluyla intervillöz aralığa ulaşması.", "category": "right", "explanation": "Hematojen transplasental villit etkenleridir."}
                ]
            ),
            make_quiz(
                question="Gebelikte erken membran rüptürü gelişen bir hastanın plasenta membranlarında yoğun nötrofilik eksüda saptanırken koryon villuslarında inflamasyon izlenmemesi öncelikle hangi antiteyi destekler?",
                options=[
                    {"key": "A", "text": "Kronik tüberkülöz villitis", "isCorrect": False, "explanation": "Tbc villusları tutar; zarlarda akut nötrofilik korioamnionit yapmaz."},
                    {"key": "B", "text": "Akut bakteriyel korioamnionit", "isCorrect": True, "explanation": "Doğru. Membranların nötrofillerle tutulması ve villusların korunması klasik asendan korioamnionit bulgusudur."},
                    {"key": "C", "text": "Battledore plasenta anomalisi", "isCorrect": False, "explanation": "Anatomik kord insersiyonudur; enfeksiyon değildir."},
                    {"key": "D", "text": "Koryokarsinom metastazı", "isCorrect": False, "explanation": "Koryokarsinom malign neoplazmdır; akut lökositik membran iltihabı değildir."}
                ],
                correct_key="B"
            ),
            make_recall(
                question="Plasenta biyopsisinde sitomegalovirüs (CMV) villitini düşündüren karakteristik mikroskobik sitopatik bulgu nedir?",
                answer="Trofoblast veya endotel hücre çekirdeklerinde geniş eozinofilik 'baykuş gözü' (owl-eye) nükleer inklüzyonların izlenmesidir."
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Plasenta İnflamasyon Etkenleri",
                items=[
                    {"text": "Asendan infeksiyonlar çoğunlukla vajinal floraya ait bakterilerden kaynaklanır.", "isLie": False, "explanation": "Doğru. Bakteriyel asendan yol en sıktır."},
                    {"text": "Listeria monocytogenes plasentaya kan yoluyla ulaşarak villuslarda mikroapse odakları yapabilir.", "isLie": False, "explanation": "Doğru. Listeria klasik hematojen etkendir."},
                    {"text": "Plasenta kord girişindeki skuamöz metaplazi gonokokal korioamnionitin kesin tanı kriteridir.", "isLie": True, "explanation": "Tuzak! Skuamöz metaplazi enfeksiyonla ilişkisiz, fizyolojik ve selim bir epitel değişimidir."},
                    {"text": "Transplasental virüsler fetüse geçerek nörosensoriyel hasar ve mikrosefali yapabilir.", "isLie": False, "explanation": "Doğru. TORCH kompleksi hasarıdır."}
                ]
            )
        ]
    ))

    # Slide 50 - Checkpoint 5
    slides.append(make_slide(
        slide_num=50,
        title="[TEKRAR SAYFASI - CHECKPOINT 5] Plasenta Anatomisi ve İnflamasyonu",
        subtitle="Bölüm 5 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Plasenta boyutları, Wharton jeli, kord anatomisi ve enfeksiyon yolları özeti",
        narrative=(
            "Bu tekrar sayfası, 41-49. adımlarda işlenen Plasenta Anatomisi ve İnflamasyonu kazanımlarını pekiştirmek için hazırlanmıştır. "
            "Termdeki normal plasenta 15-20 cm çapındadır ve umbilikal kord, membranlar, villöz parankim ile maternal desiduadan meydana gelir.\n\n"
            "- **Kordon ve Membranlar:** Umbilikal kord 55-60 cm olup mukoid Wharton jeli içinde 2 arter ve 1 ven taşır. Kenara yapışmasına 'battledore plasenta' denir. Amniyon tek katlı epiteldir ve kord girişinde selim skuamöz metaplazi sıktır.\n"
            "- **Trofoblast Katmanları:** Sinsityotrofoblast dışta, eozinofilik multinükleer dev sinsityumdur ve hCG salgılar. Sitotrofoblast içte, berrak sitoplazmalı kök hücresidir; termde belirsizleşir ve sinsityal düğümler belirir.\n"
            "- **Enfeksiyon Yolları:** Asendan yol daha sıktır, bakteriyeldir, erken membran rüptürüyle ilişkilidir ve zarlarda nötrofilik korioamnionit (kordonda funisit) yapar. Hematojen yol villusları tutarak villit oluşturur ve fetüste konjenital TORCH sendromuna yol açar.\n\n"
            "> [!NOTE]\n"
            "> Kordonda 2 arter + 1 ven vardır; marjinal giriş battledore'dur; asendan enfeksiyon korioamnionit, hematojen enfeksiyon ise villit (TORCH) yapar."
        ),
        bullets=[
            "Term plasenta 15-20 cm çapında; umbilikal kord 55-60 cm uzunluğundadır",
            "Wharton jeli içinde 2 arter ve 1 ven bulunur; kenar girişi battledore plasentadır",
            "Sinsityotrofoblast: Dışta, multinükleer dev hücre, hCG üretir; Sitotrofoblast: İçte, berrak",
            "Asendan enfeksiyon: En sık yol, bakteriyel, nötrofilik korioamnionit ve funisit",
            "Hematojen enfeksiyon: Transplasental, koryon villiti ve fetal TORCH kompleksi"
        ],
        elements=[
            make_quiz(
                question="Plasentanın normal anatomisi ve inflamasyon paternleri hakkında aşağıdaki ifadelerden hangisi doğru bir sınav spotudur?",
                options=[
                    {"key": "A", "text": "Normal göbek kordonunda 1 arter ve 2 ven bulunur; asendan enfeksiyon villitis yapar.", "isCorrect": False, "explanation": "Yanlış. Normalde 2 arter ve 1 ven vardır; asendan enfeksiyon korioamnionit yapar."},
                    {"key": "B", "text": "Umbilikal kordon Wharton jeli içinde 2 arter ve 1 ven taşır; asendan bakteriyel enfeksiyon zarlarda korioamnionite yol açar.", "isCorrect": True, "explanation": "Doğru. Damar kuralı 2 arter + 1 vendir ve asendan enfeksiyon korioamnionit üretir."},
                    {"key": "C", "text": "Battledore plasentada göbek kordonu karaciğere yapışır.", "isCorrect": False, "explanation": "Yanlış. Battledore kordun plasenta diski kenarına yapışmasıdır."},
                    {"key": "D", "text": "Sinsityotrofoblastlar iç tabakada yer alan tek nükleuslu kök hücrelerdir.", "isCorrect": False, "explanation": "Yanlış. İçteki kök hücre sitotrofoblasttır; sinsityotrofoblast dışta multinükleer dev hücredir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Termdeki umbilikal kord konnektif dokusu olan Wharton jeli içinde 2 arter ve 1 ven barındırır.",
                masked_term="2 arter ve 1 ven",
                hint="Göbek kordonundaki normal vasküler yapı sayısı"
            ),
            make_table(
                title="Bölüm 5 Temel Plasental Kazanımlar Özeti",
                headers=["Anatomik / Patolojik Öğe", "Normal / Tipik Bulgu", "Klinik Yansıma"],
                rows=[
                    [
                        {"text": "Umbilikal Kord Damarları", "isMasked": False},
                        {"text": "2 arter ve 1 ven", "isMasked": True, "hint": "İki atardamar ve bir toplardamar"},
                        {"text": "Tek arter konjenital anomali uyarısıdır", "isMasked": False}
                    ],
                    [
                        {"text": "Marjinal Kord Girişi", "isMasked": False},
                        {"text": "Battledore plasenta", "isMasked": True, "hint": "Raket benzeri periferik giriş terimi"},
                        {"text": "Doğumda traksiyonla kopma riski", "isMasked": False}
                    ],
                    [
                        {"text": "Asendan Enfeksiyon Tablosu", "isMasked": False},
                        {"text": "Korioamnionit", "isMasked": True, "hint": "Fetal zarların akut nötrofilik iltihabı"},
                        {"text": "Erken membran rüptürü ve erken doğum", "isMasked": False}
                    ],
                    [
                        {"text": "Hematojen Enfeksiyon Tablosu", "isMasked": False},
                        {"text": "Koryon villiti ve TORCH", "isMasked": True, "hint": "Villus tutulumu ve konjenital fetal sendrom"},
                        {"text": "Fetal mikrosefali ve organ hasarı", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 5 Kontrol Önermeleri",
                items=[
                    {"text": "Term plasenta diski yaklaşık 15-20 cm çapındadır.", "isLie": False, "explanation": "Doğru. Normal miadındaki plasenta boyutudur."},
                    {"text": "Sinsityotrofoblastlar bol eozinofilik sitoplazmalı multinükleer dev hücrelerdir.", "isLie": False, "explanation": "Doğru. Klasik dış trofoblast tabakasıdır."},
                    {"text": "Amniyon zarında kord girişindeki skuamöz metaplazi acil cerrahi histerektomi gerektiren prekanseröz bir lezyondur.", "isLie": True, "explanation": "Tuzak! Amniyondaki skuamöz metaplazi tamamen selim, fizyolojik bir fenomendir; kanserleşmez ve tedavi gerektirmez."},
                    {"text": "Hematojen transplasental enfeksiyonlar villusları tutarak villite neden olur.", "isLie": False, "explanation": "Doğru. Transplasental yayılımın patolojik bulgusu villittir."}
                ]
            ),
            make_recall(
                question="Checkpoint 5: Plasentanın iki majör enfeksiyon yolunu ve oluşturdukları spesifik histopatolojik tanıları belirtiniz.",
                answer="Asendan yol fetal membranlarda 'korioamnionit' (ve kordonda funisit) yapar; hematojen yol ise koryon villuslarında 'villit' (ve fetal TORCH tablosu) yapar."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=5
    ))
    
    return slides
