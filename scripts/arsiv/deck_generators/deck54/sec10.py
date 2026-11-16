"""
Deck 54 Section 10: Gestasyonel Patolojiler, Uteroplasental Damar Hastalıkları ve Entegre Ayırıcı Tanı
Slides 91-100 (Final Checkpoint 10 at slide 100)
Focus:
- Preeklampsi ve eklampsi patofizyolojisi: Uteroplasental spiral arterlerde trofoblastik invazyon yetersizliği
- Spiral arterlerde muskuloelastik duvarın sebat etmesi ve vazodilatasyon eksikliği
- Akut aterozis: Fibrinoid nekroz, köpüksü makrofajlar ve damar tıkanıklığı
- Plasental hipoperfüzyon, retroplasental hematom/dekolman ve yaygın infarktlar
- Maternal endotelyal disfonksiyon: Doku faktörü ve tromboksan salınımı, vazokonstriksiyon, hipertansiyon ve DİC
- Plasenta yapışma anomalileri (akreta, inkreta, perkreta) cerrahi patolojisi, desidua yokluğu ve histerektomi endikasyonu
- Uterus düz kas ve trofoblastik tümörlerinin tam kurul entegre ayırıcı tanı matrisi (Leiomyom vs Leiomyosarkom vs Mol vs Koryokarsinom)
- Kurul 1 Entegre Vaka Senaryoları (Obstetrik ve Onkolojik Karar Verme)
- Final Checkpoint 10: Büyük Kurul Sentezi ve Tam Deste Kapanışı (Slide 100)
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide,
    make_quiz,
    make_cloze,
    make_table,
    make_chain,
    make_recall,
    make_spot_the_lie,
    make_slider,
    make_swipe,
    make_branching,
    make_venn
)

def get_sec10_slides():
    slides = []

    # Slide 91
    slides.append(make_slide(
        slide_num=91,
        title="Preeklampsi ve Eklampsi: Klinik Spektrum ve Epidemiyoloji",
        subtitle="Hipertansiyon, proteinüri ve ödem triadı; konvülsiyonlar",
        clinical_focus="3. trimester gebelik toksemisinin klinik tanımı ve DİC riski",
        narrative=(
            "Preeklampsi, gebeliğin üçüncü trimesterinde (20. haftadan sonra) **hipertansiyon (kan basıncı ≥140/90 mmHg), proteinüri ve belirgin ödem** bulgularının birlikte görülmesiyle karakterize sistemik bir sendromdur.\n\n"
            "- **Epidemiyoloji:** Tüm gebeliklerin yaklaşık %10'unda hipertansiyon izlenir. Preeklampsi özellikle ilk gebeliğini 35 yaşın üzerinde yaşayan (ileri anne yaşı) primigravid kadınlarda %5-10 oranında görülür.\n"
            "- **Eklampsi:** Bu klinik tabloya sara benzeri generalize tonik-klonik **konvülsiyonların (nöbetlerin) eklenmesi eklampsi** olarak adlandırılır.\n"
            "- **Klinik Komplikasyonlar:** Ağır eklampsi olgularında **Yaygın Damar İçi Pıhtılaşma (DİC)**, mikroanjiyopatik hemolitik anemi, karaciğer hematomu/rüptürü (HELLP) ve böbrek kortikal nekrozu gelişebilir; zamanında müdahale edilmezse maternal ve fetal ölüme yol açar.\n\n"
            "> [!IMPORTANT]\n"
            "> 3. trimesterde hipertansiyon, ödem ve proteinüri preeklampsidir; bu tabloya konvülsiyonların eklenmesi eklampsi olarak tanımlanır ve DİC riski taşır."
        ),
        bullets=[
            "Preeklampsi: 3. trimesterde hipertansiyon, ödem ve proteinüri triadıdır",
            "Gebeliklerin yaklaşık %10'unda yüksek tansiyon meydana gelir",
            "Tabloya konvülsiyonların (nöbet) eklenmesi eklampsi olarak adlandırılır",
            "Şiddetli olgularda DİC gelişerek yaygın iskemik organ nekrozu ve ölüme yol açar"
        ],
        elements=[
            make_quiz(
                question="Gebeliğinin 34. haftasında olan 36 yaşındaki ilk gebeliğindeki kadında kan basıncı 165/105 mmHg, idrar analizinde 3+ proteinüri ve bacaklarda masif pretibial ödem saptanıyor. Takipleri sırasında hastada aniden generalize tonik-klonik nöbet (konvülsiyon) gelişiyor. Bu klinik tablonun doğru tanısı hangisidir?",
                options=[
                    {"key": "A", "text": "Eklampsi", "isCorrect": True, "explanation": "Doğru. Preeklampsi triadı (hipertansiyon, ödem, proteinüri) zemininde gelişen konvülsiyonlar eklampsidir."},
                    {"key": "B", "text": "Akut bakteriyel korioamnionit", "isCorrect": False, "explanation": "Korioamnionit ateş ve pürülan akıntı yapar; konvülsiyon ve proteinüri yapmaz."},
                    {"key": "C", "text": "Gestasyonel koryokarsinom beyin metastazı", "isCorrect": False, "explanation": "Metastazda fokal kitle ve kanama olur; gebelik hipertansiyon-proteinüri triadı eklampsidir."},
                    {"key": "D", "text": "İntramural leiomyom kırmızı dejenerasyonu", "isCorrect": False, "explanation": "Miyom dejenerasyonu lokalize karın ağrısı yapar; konvülsiyon yapmaz."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Üçüncü trimesterde hipertansiyon, ödem ve proteinüri tablosuna epileptik nöbetlerin eklenmesine eklampsi denir.",
                masked_term="eklampsi",
                hint="Gebelik toksemisi zemininde gelişen konvülsif nörolojik komplikasyon"
            ),
            make_chain(
                title="Preeklampsiden Eklampsiye Klinik Kaskad",
                steps=[
                    "1. Uteroplasental İskemi: Yetersiz perfüzyon nedeniyle plasentadan maternal kana toksik faktörler salınır.",
                    "2. Sistemik Endotel Hasarı: Damar geçirgenliği artar; hipertansiyon, pretibial ödem ve glomerüler hasarla proteinüri gelişir.",
                    "3. Serebral Ödem: Beyin mikrosirkülasyonundaki spazm ve vazojenik ödem intrakraniyal basıncı artırır.",
                    "4. Eklampsik Nöbet: Hastada generalize tonik-klonik konvülsiyonlar ve DİC tablosu ortaya çıkar."
                ]
            ),
            make_recall(
                question="Preeklampsi sendromunda böbrek glomerüllerinde meydana gelen ve idrarda masif protein kaçağına (proteinüri) yol açan karakteristik endotelyal lezyon nedir?",
                answer="Glomerüler kapiller endotel hücrelerinin şişmesi ve vakuolizasyonu ile karakterize 'glomerüler kapiller endotelyozis'tir."
            )
        ]
    ))

    # Slide 92
    slides.append(make_slide(
        slide_num=92,
        title="Preeklampsinin Temel Mekanizması: Spiral Arteriollerde Yetersiz Dilatasyon",
        subtitle="Muskuloelastik duvarın dönüşüm hatası ve plasental hipoperfüzyon",
        clinical_focus="Normal gebelik ile preeklampsi arasındaki uteroplasental yatak farkı",
        narrative=(
            "Preeklampsi sendromunun başlangıç tetikleyicisi maternal kardiyovasküler sistem değil, plasenta yatağındaki damarsal adaptasyon defektidir.\n\n"
            "- **Normal Gebelikte Vasküler Remodeling:** Normalde ekstravillöz trofoblastlar desiduayı geçip myometriumdaki maternal **spiral arteriollerin** içine girer. Damarların kalın muskuloelastik çeperini tahrip ederek yerine fibrinöz materyal yerleştirir. Böylece spiral arterioller dar ve kasılabilen damarlar olmaktan çıkıp, düşük dirençli, yüksek akımlı dev sinüzoidlere dönüşür; plasentaya bol kan akar.\n"
            "- **Preeklampside Yetersiz Dönüşüm:** Preeklampside ekstravillöz trofoblast invazyonu yüzeyel kalır; spiral arteriollerin myometrial segmentlerine ulaşamaz. Damarların **muskuloelastik duvarı aynen korunur**; damarlar dar kalır ve vazomotor tonusunu kaybetmez. Sonuçta plasental yataktaki kan akımı dramatik şekilde azalır ve kronik **plasental iskemi** gelişir.\n\n"
            "> [!IMPORTANT]\n"
            "> Preeklampsinin tüm olgularındaki temel patolojik özellik, spiral arteriollerdeki yetersiz dilatasyona bağlı maternal kan akımının plasentaya yeterince ulaşamamasıdır."
        ),
        bullets=[
            "Tüm olgularda temel özellik spiral arteriollerdeki yetersiz dilatasyondur",
            "Normalde trofoblastlar damar kas tabakasını eritip damarı genişletir",
            "Preeklampside muskuloelastik duvar aynen kalır ve damarlar dar kalır",
            "Plasentaya yeterli maternal kan ulaşamaz; kronik doku hipoperfüzyonu doğar"
        ],
        elements=[
            make_quiz(
                question="Preeklampsi ve eklampsi patofizyolojisinde tüm olgularda saptanan, plasental hipoperfüzyonun ve maternal endotel hasarının primer tetikleyicisi olan temel histopatolojik anomali hangisidir?",
                options=[
                    {"key": "A", "text": "Uterus korpus myometriumunda multiple girdapsı nodüller bulunması", "isCorrect": False, "explanation": "Bu leiomyomdur; preeklampsi mekanizması değildir."},
                    {"key": "B", "text": "Uteroplasental yataktaki spiral arteriollerde yetersiz dilatasyon ve muskuloelastik duvarın sebat etmesi", "isCorrect": True, "explanation": "Doğru. Spiral arteriollerin trofoblastlarca genişletilememesi ve dar kalması preeklampsinin tüm olgularındaki primer patofizyolojik temelidir."},
                    {"key": "C", "text": "Trofoblastların koryon villusu üretmeyi tamamen durdurması", "isCorrect": False, "explanation": "Villussuz trofoblastik tümör koryokarsinomdur."},
                    {"key": "D", "text": "Amniyon zarında skuamöz metaplazi gelişmesi", "isCorrect": False, "explanation": "Skuamöz metaplazi selim membranöz bir varyasyondur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Preeklampside uteroplasental yataktaki spiral arteriollerdeki yetersiz dilatasyon nedeniyle maternal kan akımı plasentaya yeterince ulaşamaz.",
                masked_term="spiral arteriollerdeki yetersiz dilatasyon",
                hint="Maternal uterin damarların trofoblastlar tarafından genişletilememesi durumu"
            ),
            make_slider(
                left_title="Normal Gebelik Uteroplasental Yatağı",
                right_title="Preeklamptik Plasenta Yatağı",
                left_points=[
                    "Ekstravillöz trofoblastlar spiral arter duvarına derinlemesine girer",
                    "Muskuloelastik tunika media tabakası tamamen erir ve fibrinle dolar",
                    "Damarlar geniş, düşük dirençli, yüksek debili sinüzoidlere dönüşür"
                ],
                right_points=[
                    "Trofoblast invazyonu sığ kalır; damar duvarı dönüşemez",
                    "Muskuloelastik kas duvarı aynen korunur; damarlar dar ve hiperreaktiftir",
                    "Kan akımı belirgin kısıtlanır; kronik plasental iskemi ve hipoperfüzyon gelişir"
                ]
            ),
            make_recall(
                question="Normal gebelikte maternal spiral arteriollerin kas tabakasının fibrinle yer değiştirmesinin (fizyolojik remodeling) temel hemodinamik amacı nedir?",
                answer="Damarların damar daraltıcı (vazokonstriktör) uyaranlara yanıt vermesini engelleyerek plasentaya kesintisiz, bol ve düşük basınçlı maternal kan sağlamaktır."
            )
        ]
    ))

    # Slide 93
    slides.append(make_slide(
        slide_num=93,
        title="Preeklampside Vasküler Lezyonlar: Akut Aterozis ve DİC Patogenezi",
        subtitle="Fibrinoid nekroz, lipid yüklü makrofajlar, doku faktörü ve tromboksan",
        clinical_focus="İskemik plasentadan salınan faktörlerin sistemik pıhtılaşma fırtınası başlatması",
        narrative=(
            "Yetersiz genişleyen dar spiral arterler yüksek akım sürtünmesine ve hipoksiye maruz kaldığında damar duvarında ağır nekroz gelişir.\n\n"
            "- **Akut Aterozis:** Preeklamptik plasenta yatağındaki spiral arteriollerde damar duvarı kalınlaşır, düzensiz **fibrinoid nekroz** odakları ortaya çıkar ve damar çeperinde **fokal lipid yüklü köpüksü makrofaj toplulukları** birikir. Bu aterom benzeri nekrotizan lezyona akut aterozis denir ve damar lümeninde trombozlara yol açar.\n"
            "- **Maternal Sistemik Kaskad:** İskemik plasenta dokusundan dolaşıma vazodilatörlerin (NO, prostasiklin) kullanımını baskılayan ve güçlü vazokonstriktör olan **tromboksan ile doku faktörü (tromboplastin)** salınır.\n"
            "- **DİC Mekanizması:** Doku faktörü maternal endotelde hasar başlatıp pıhtılaşma kaskadını tetikler; sonuçta mikrovasküler trombüsler, trombosit tüketimi ve **Yaygın Damar İçi Pıhtılaşma (DİC)** meydana gelir.\n\n"
            "> [!IMPORTANT]\n"
            "> Preeklamptik damarlarda fibrinoid nekroz ve lipid yüklü makrofajlarla karakterize lezyona akut aterozis denir; iskemik plasentadan salınan doku faktörü ve tromboksan DİC'e yol açar."
        ),
        bullets=[
            "Spiral arterlerde fibrinoid nekroz ve lipid yüklü köpüksü makrofajlar (akut aterozis) izlenir",
            "Trofoblastların vazodilatör kullanımı azalır; sistemik vazokonstriksiyon gelişir",
            "İskemik plasenta dolaşıma doku faktörü ve tromboksan salgılar",
            "Doku faktörü pıhtılaşma kaskadını tetikleyerek Yaygın Damar İçi Pıhtılaşmaya (DİC) yol açar"
        ],
        elements=[
            make_quiz(
                question="Preeklamptik bir gebenin plasenta yatağı biyopsisinde spiral arter duvarlarında kalınlaşma, belirgin fibrinoid nekroz ve damar çeperine toplanmış lipid yüklü köpüksü makrofaj kümeleri saptanıyor. Bu karakteristik mikrovasküler patolojik lezyona ne ad verilir?",
                options=[
                    {"key": "A", "text": "Endometrial stromal sarkom", "isCorrect": False, "explanation": "Stromal tümördür; preeklamptik damar lezyonu değildir."},
                    {"key": "B", "text": "Akut aterozis", "isCorrect": True, "explanation": "Doğru. Spiral arteriollerde fibrinoid nekroz ve lipid yüklü makrofaj birikimi akut aterozis olarak adlandırılır."},
                    {"key": "C", "text": "Akut bakteriyel funisit", "isCorrect": False, "explanation": "Funisit kordon nötrofil infiltrasyonudur."},
                    {"key": "D", "text": "Plasenta akreta", "isCorrect": False, "explanation": "Akreta desidua yokluğunda myometriuma yapışmadır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Preeklampsi olgularında spiral arter duvarlarında fibrinoid nekroz ve lipid yüklü makrofaj infiltrasyonu ile karakterize akut aterozis izlenir.",
                masked_term="akut aterozis",
                hint="Gebelik damarlarında köpüksü histiyositik nekrotizan vaskülopati"
            ),
            make_chain(
                title="Preeklampside İskemiden Sistemik DİC Tablosuna Geçiş",
                steps=[
                    "1. Damar Nekrozu: Yetersiz genişlemiş spiral arterlerde akut aterozis ve mikrotrombozlar oluşur.",
                    "2. Plasental Stres: İskemik trofoblastlar maternal kana yoğun doku faktörü ve tromboksan boşaltır.",
                    "3. Trombosit Aktivasyonu: Tromboksan maternal damarlarda spazm yaparken trombosit agregasyonunu körükler.",
                    "4. Tüketim Koagülopatisi: Doku faktörüyle yaygın mikrovasküler fibrin pıhtıları oluşur; DİC ve kanama eğilimi gelişir."
                ]
            ),
            make_recall(
                question="Preeklampsi patolojisinde iskemik plasentadan salınan hangi iki temel biyokimyasal medyatör maternal dolaşımda vazokonstriksiyon ve DİC gelişiminden sorumludur?",
                answer="Tromboksan (güçlü vazokonstriktör ve trombosit agregatörü) ve doku faktörüdür (pıhtılaşma kaskadını tetikleyen ekstrinsik yolak aktivatörü)."
            )
        ]
    ))

    # Slide 94
    slides.append(make_slide(
        slide_num=94,
        title="Preeklamptik Plasenta Morfolojisi: Erken Yaşlanma, İnfarktlar ve Hematom",
        subtitle="Sinsityal düğümler, yaygın parankim infarktı ve retroplasental hemoraji",
        clinical_focus="Plasenta makroskopi ve histolojisinde preeklampsinin izleri",
        narrative=(
            "Kronik hipoperfüzyon ve iskemi altındaki plasenta parankiminde belirgin makroskobik ve mikroskobik doku harabiyeti izlenir.\n\n"
            "- **Parankim İnfarktları:** Normal term plasentalarda nadiren küçük periferik infarktlar bulunabilir. Ancak şiddetli preeklampsi ve eklampsi hastalarının **üçte birinde (1/3)** plasental parankimde çok sayıda, santral yerleşimli, soluk sarı-beyaz renkli **geniş infarktüs alanları** izlenir.\n"
            "- **Retroplasental Hemoraji (%15):** Hastaların yaklaşık %15'inde desidua basalis ile plasenta arasında damar rüptürlerine bağlı masif kan toplanması (**retroplasental hematom / plasenta dekolmanı**) meydana gelir; plasenta vaktinden önce uterus duvarından ayrılır.\n"
            "- **Mikroskopik Erken Yaşlanma:** Koryon villuslarında ödem, hipovaskülarite ve sinsityotrofoblast nükleuslarının birikmesiyle oluşan **artmış sinsityal epitelyal düğümler (Tenney-Parker değişiklikleri)** erken matürasyon ve yaşlanma kanıtıdır.\n\n"
            "> [!NOTE]\n"
            "> Şiddetli preeklampside plasenta infarktları 1/3 hastada yaygınlaşır; hastaların %15'inde retroplasental hemoraji (dekolman) görülür; villuslarda sinsityal düğümler artar."
        ),
        bullets=[
            "Normalde seyrek olan plasental infarktlar preeklampside 1/3 hastada çok sayıdadır",
            "Hastaların %15'inde retroplasental hemoraji (abruptio placentae) izlenir",
            "Villuslarda hipovaskülarite ve artmış sinsityal düğümler (erken yaşlanma) tipiktir",
            "Bu dokusal kayıplar intrauterin gelişme geriliği ve fetal hipoksiye neden olur"
        ],
        elements=[
            make_quiz(
                question="Şiddetli preeklampsi tanısıyla acil sezaryene alınan bir kadının plasentasının incelenmesinde parankimde çok sayıda soluk sert nekroz odakları (infarktlar) ve maternal yüzeyde desidua tabakasını ayıran taze kan pıhtısı saptanıyor. Bu lezyonların preeklampsideki görülme oranları hakkında hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "İnfarktlar preeklampsili olguların %100'ünde, retroplasental hematom ise %90'ında görülür.", "isCorrect": False, "explanation": "Oranlar bu kadar yüksek değildir."},
                    {"key": "B", "text": "İnfarktlar hastaların yaklaşık üçte birinde (1/3) çok sayıda izlenirken, retroplasental hemorajiler olguların %15'inde görülür.", "isCorrect": True, "explanation": "Doğru. Şiddetli preeklampsi/eklampside yaygın infarktlar 1/3 hastada, retroplasental hemoraji ise %15 hastada izlenir."},
                    {"key": "C", "text": "Preeklampside asla infarkt veya hematom gelişmez; lezyonlar sadece koryon villus ödemidir.", "isCorrect": False, "explanation": "İskemik infarkt ve hematom majör preeklampsi bulgularıdır."},
                    {"key": "D", "text": "Retroplasental hematom koryokarsinoma özgüdür, preeklampside bulunmaz.", "isCorrect": False, "explanation": "Retroplasental hematom preeklampsinin klasik dekolman komplikasyonudur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Şiddetli preeklampsi ve eklampsi olgularının yaklaşık yüzde on beşinde desidua basalis yırtılmasına bağlı retroplasental hemorajiler izlenir.",
                masked_term="retroplasental hemorajiler",
                hint="Plasenta arkasında oluşan ayrılma kanamaları"
            ),
            make_table(
                title="Preeklamptik Plasentada Makroskobik ve Mikroskobik Bulgular",
                headers=["Patolojik Değişiklik", "Görülme Oranı / Sıklık", "Dokusal Karşılık"],
                rows=[
                    [
                        {"text": "Yaygın Plasental İnfarktlar", "isMasked": False},
                        {"text": "Olguların yaklaşık 1/3'ü", "isMasked": True, "hint": "Üçte bir hastada saptanan iskemik lezyon"},
                        {"text": "Soluk sarı-beyaz sert villöz nekroz adacıkları", "isMasked": False}
                    ],
                    [
                        {"text": "Retroplasental Hemoraji", "isMasked": False},
                        {"text": "Hastaların %15'inde", "isMasked": True, "hint": "Yüzde on beş sıklık oranı"},
                        {"text": "Plasentanın erken ayrılması (dekolman hematomu)", "isMasked": False}
                    ],
                    [
                        {"text": "Sinsityal Epitelyal Düğümler", "isMasked": False},
                        {"text": "Mikroskopide belirgin artış", "isMasked": False},
                        {"text": "Villus yüzeyinde nükleer kümelenme ve erken yaşlanma", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Preeklampsi zemininde gelişen retroplasental hemoraji (plasenta dekolmanı) maternal ve fetal açıdan neden çok acil bir obstetrik tablodur?",
                answer="Maternal tarafta masif kan kaybı ve DİC tetiklenirken, fetal tarafta plasenta yüzeyi ayrıldığı için ani asfiksi ve intrauterin fetal ölüm gelişir."
            )
        ]
    ))

    # Slide 95
    slides.append(make_slide(
        slide_num=95,
        title="Plasental Yapışma Anomalileri: Akreta, İnkreta ve Perkreta",
        subtitle="Desidua basalis defekti, myometriyal invazyon derinliği ve uterin rüptür",
        clinical_focus="Postpartum durdurulamayan masif kanama ve peripartum histerektomi",
        narrative=(
            "Normal bir gebelikte koryon villusları ile uterin kas lifleri (myometrium) arasında süngerimsi ve koruyucu bir **desidua basalis (Nitabuch tabakası)** bulunur. Bu tabaka doğumda plasentanın duvardan kolayca soyularak ayrılmasını sağlar.\n\n"
            "- **Patolojik Temel:** Desidua tabakasının konjenital veya önceki cerrahilere (sezaryen skarı, küretaj) bağlı yetersizliği durumunda, villuslar arada desidua olmadan doğrudan myometriuma yapışır veya içine girer.\n"
            "- **Plasenta Akreta:** Desiduanın parsiyel veya komplet yokluğudur; koryon villusları süperfisyel myometriuma sıkıca yapışmıştır fakat kas içine gömülmemiştir.\n"
            "- **Plasenta İnkreta:** Koryon villusları myometrium duvarının derinliklerine kadar girmiş, kas lifleri arasında ilerlemiş ancak myometriumu tamamen aşmamıştır.\n"
            "- **Plasenta Perkreta:** Koryon villusları myometriumu tam kat aşarak dış uterus serozasına ve hatta komşu organlara (mesane duvarına) kadar penetre olmuştur; uterin rüptüre ve katastrofik kanamaya yol açar.\n\n"
            "> [!IMPORTANT]\n"
            "> Akreta süperfisyel myometriuma yapışır; inkreta myometrium içine girer; perkreta myometriumu tam kat aşıp serozaya veya mesaneye kadar ilerler."
        ),
        bullets=[
            "Temel patoloji desidua basalis tabakasının parsiyel veya tam yokluğudur",
            "Akreta: Villuslar süperfisyel myometriuma doğrudan yapışıktır",
            "İnkreta: Villuslar myometrium duvarı içine derinlemesine girmiştir",
            "Perkreta: Villuslar myometriumu tam kat aşarak serozaya ulaşır (rüptür riski)",
            "Doğum sonrasında plasenta ayrılamaz; masif postpartum kanama ve histerektomi gerekir"
        ],
        elements=[
            make_quiz(
                question="Daha önce iki kez sezaryen ameliyatı geçirmiş bir gebenin doğumunda bebek doğurtulduktan sonra plasenta hiçbir şekilde uterus duvarından ayrılamıyor. Elle halas denemesinde şiddetli kontrolsüz kanama başlıyor. Acil histerektomi yapılan hastanın patoloji kesitinde koryon villuslarının myometrium kas tabakasını tam kat delerek dış seroza tabakasına ulaştığı ve mesane peritonunu infiltre ettiği saptanıyor. En doğru tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Plasenta akreta", "isCorrect": False, "explanation": "Akreta sadece süperfisyel myometriuma yapışıktır; kası tam kat delmez."},
                    {"key": "B", "text": "Plasenta inkreta", "isCorrect": False, "explanation": "İnkreta myometrium kası içine girer fakat serozayı aşmaz."},
                    {"key": "C", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Mol hidatiform kistik hidropik villus hastalığıdır."},
                    {"key": "D", "text": "Plasenta perkreta", "isCorrect": True, "explanation": "Doğru. Myometriumu tam kat aşarak serozaya ve komşu organlara kadar penetre olan tablo plasenta perkretadır."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Plasentanın myometriumu tam kat aşarak uterus serozasına kadar ilerlemesine plasenta perkreta denir.",
                masked_term="plasenta perkreta",
                hint="Uterus duvarını delip dış peritona ulaşan en derin koryonik invazyon"
            ),
            make_table(
                title="Plasental Yapışma Anomalileri Derinlik Sınıflaması",
                headers=["Anomali Tipi", "İnvazyon Derinliği", "Klinik Risk ve Sonuç"],
                rows=[
                    [
                        {"text": "Plasenta Akreta", "isMasked": False},
                        {"text": "Süperfisyel myometrium yüzeyine yapışma", "isMasked": True, "hint": "Kas tabakasının sığ sınırına tutunma"},
                        {"text": "Ayrılamayan plasenta; postpartum kanama", "isMasked": False}
                    ],
                    [
                        {"text": "Plasenta İnkreta", "isMasked": False},
                        {"text": "Myometrium kas tabakası içine penetrasyon", "isMasked": True, "hint": "Uterin duvar gövdesi boyunca ilerleme"},
                        {"text": "Cerrahi küretajla çıkarılamaz; histerektomi riski", "isMasked": False}
                    ],
                    [
                        {"text": "Plasenta Perkreta", "isMasked": False},
                        {"text": "Myometriumu tam kat aşıp serozaya ulaşma", "isMasked": True, "hint": "Tüm kalınlığı delip periton sınırına varma"},
                        {"text": "Uterin rüptür, mesane invazyonu, katastrofik şok", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Plasenta yapışma anomalilerinin (akreta/inkreta/perkreta) günümüzde geçmişe kıyasla çok daha sık görülmesinin en temel obstetrik nedeni nedir?",
                answer="Sezaryen ile doğum oranlarının ve intrauterin cerrahi girişimlerin artmasıdır; cerrahi skar dokusu üzerinde desidua gelişemez."
            )
        ]
    ))

    # Slide 96
    slides.append(make_slide(
        slide_num=96,
        title="Uterus Düz Kas Tümörleri Entegre Ayırıcı Tanı Matrisi",
        subtitle="Leiomyom, varyantlar, STUMP ve Leiomyosarkom karşılaştırması",
        clinical_focus="Myometrial lezyonlarda benign-malign ayrımının altın kuralları",
        narrative=(
            "Uterus korpusunun myometrial lezyonları tamamen selim leiomyomdan ölümcül leiomyosarkoma kadar geniş bir histopatolojik spektrum sergiler.\n\n"
            "- **Leiomyom:** Kadınların en sık benign tümörüdür. Reprodüktif çağda, multiple, keskin sınırlı, sert ve girdapsı kesit yüzlüdür. Selim mitotik aktivite (<5), atipi ve nekroz yoktur. Sarkoma dönüşmez.\n"
            "- **Varyantlar ve STUMP:** Sellüler leiomyomda hücre yoğunluğu artmıştır fakat mitoz azdır. Atipik (bizar) leiomyomda nükleer pleomorfizm vardır fakat nekroz ve yüksek mitoz yoktur; selimdir. Kriterlerin sınırda kaldığı şüpheli lezyonlar STUMP olarak izlenir.\n"
            "- **Leiomyosarkom:** Daima soliterdir, postmenopozal dönemde görülür, yumuşak, kanamalı ve nekrotiktir. De novo gelişir. Tanı için nükleer atipi, ≥10 mitoz/10 BÜA ve koagülatif tümör nekrozu triadı aranır. Hematojen yolla en sık akciğere metastaz yapar.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyom multiple ve girdapsıdır, dejenere olsa da selimdir; leiomyosarkom soliter, yumuşak, nekrotiktir, de novo gelişir ve akciğere hematojen metastaz yapar."
        ),
        bullets=[
            "Leiomyom: Multiple, reprodüktif çağ, sert, girdapsı; sarkoma dönüşmez",
            "Atipik bizar miyom: Belirgin atipiye rağmen nekroz ve yüksek mitoz yoktur (selim)",
            "STUMP: Kriterleri tam dolduramayan, yakın takip gerektiren sınırda tümördür",
            "Leiomyosarkom: Soliter, postmenopozal, yumuşak, nekrotik; de novo başlar; akciğer metastazı"
        ],
        elements=[
            make_quiz(
                question="60 yaşındaki postmenopozal bir kadında hızla büyüyen soliter intrauterin kitle nedeniyle histerektomi yapılıyor. Makroskopide 8 cm çapında, yumuşak, sarı-pembe renkli, geniş kanama ve nekroz alanları içeren sınırları düzensiz nodül izleniyor. Mikroskopide ağır nükleer sitolojik atipi, sahada 16 mitoz/10 BÜA ve koagülatif tümör hücresi nekrozu saptanıyor. En doğru tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Atipik (bizar) selim leiomyom", "isCorrect": False, "explanation": "Atipik miyomda atipi olsa da koagülatif nekroz ve ≥10 mitoz bulunmaz."},
                    {"key": "B", "text": "Gestasyonel koryokarsinom", "isCorrect": False, "explanation": "Koryokarsinom trofoblastik epitelyal tümördür; düz kas sarkomu değildir."},
                    {"key": "C", "text": "Uterin leiomyosarkom", "isCorrect": True, "explanation": "Doğru. Postmenopozal soliter nekrotik kitle, nükleer atipi, 16 mitoz ve koagülatif nekroz leiomyosarkomun klasik tanı triadıdır."},
                    {"key": "D", "text": "İntramural klasik leiomyom", "isCorrect": False, "explanation": "Klasik miyom sert, girdapsı, nekrozsuz ve düşük mitozludur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Postmenopozal dönemde soliter yumuşak kitle şeklinde beliren ve belirgin atipi ile koagülatif nekroz içeren malign düz kas tümörüne leiomyosarkom denir.",
                masked_term="leiomyosarkom",
                hint="Uterusun en sık görülen habis mezenkimal düz kas neoplazmı"
            ),
            make_slider(
                left_title="Uterin Leiomyom (Selim)",
                right_title="Uterin Leiomyosarkom (Habis)",
                left_points=[
                    "Reprodüktif çağda sık (%30-50); sıklıkla çok sayıda (multiple)",
                    "Keskin sınırlı, sert elastik kıvamlı, beyaz-gri girdapsı kesit yüzü",
                    "Normal myometrium benzeri iğsi düz kas lifleri; nekroz ve yüksek mitoz yok",
                    "Malign sarkoma dönüşmez; cerrahi enükleasyon mümkündür"
                ],
                right_points=[
                    "Postmenopozal dönemde görülür; daima tek (soliter) kitledir",
                    "Sınırları düzensiz, yumuşak etsi kıvamlı, yaygın kanamalı ve nekrotik",
                    "Şiddetli sitolojik atipi, ≥10 mitoz/10 BÜA ve koagülatif tümör nekrozu",
                    "De novo gelişir; hematojen yolla hızla akciğere metastaz yapar"
                ]
            ),
            make_recall(
                question="Bir genel cerrah veya kadın doğumcu 'bu hastanın çok sayıda büyük miyomu var, bunlar kesinlikle kansere dönüşür' dediğinde patolog bu ifadeyi nasıl düzeltir?",
                answer="'Leiomyomlar sarkoma dönüşmez; multipl olmaları malignite riskini artırmaz; leiomyosarkomlar miyomdan değil de novo olarak sıfırdan başlar' diyerek düzeltir."
            )
        ]
    ))

    # Slide 97
    slides.append(make_slide(
        slide_num=97,
        title="Gestasyonel Trofoblastik Hastalıklar Entegre Karşılaştırma Matrisi",
        subtitle="Komplet mol, parsiyel mol, invaziv mol ve koryokarsinomun tam analizi",
        clinical_focus="Kurul 1 patoloji dersinin trofoblastik hastalıklar özet tablosu",
        narrative=(
            "Gestasyonel trofoblastik hastalıklar agresiflik yönünden benign mol hidatiformdan, lokal invaziv mole ve yüksek maligniteli koryokarsinoma kadar sıralanır.\n\n"
            "- **Genetik Mimari:** Komplet mol diploidtir (46,XX; boş ovum + 2 sperm; p57KIP2 negatif). Parsiyel mol triploidtir (69,XXY; normal ovum + 2 sperm; p57KIP2 pozitif). Koryokarsinom anöploidtir ve paternal antijen taşır.\n"
            "- **Morfoloji ve Villus Durumu:** Komplet molde tüm villuslar avasküler ve hidropiktir, embriyo dokusu yoktur. Parsiyel molde bazı villuslar hidropiktir, fetal dokular ve eritrositler izlenir. İnvaziv molde myometriuma giren hidropik villuslar vardır. Koryokarsinomda ise **koryon villusları KESİNLİKLE YOKTUR**; tamamen anaplastik sito/sinsityotrofoblastlardan oluşur.\n"
            "- **Prognoz ve Tedavi:** Mollerin %80-90'ı küretajla kür olur. Komplet mollerin %10'u invaziv mol, %2-3'ü koryokarsinom geliştirir. Koryokarsinom en sık akciğere (%50) metastaz yapar fakat kemoterapi ile %100 kür şansına sahiptir.\n\n"
            "> [!IMPORTANT]\n"
            "> Komplet molde villusların tümü hidropik ve avaskülerdir (fetüs yok); koryokarsinomda ise villus hiç yoktur. Paternal antijenler koryokarsinomda %100 kür sağlar."
        ),
        bullets=[
            "Komplet mol: Diploid (46,XX), avasküler villus, fetüs yok, p57 negatif, %2 karsinom",
            "Parsiyel mol: Triploid (69,XXY), mikst villus, fetal eritrositler var, p57 pozitif",
            "İnvaziv mol: Myometriuma giren hidropik villuslar; metastaz yapmaz; kemoterapiyle kür",
            "Koryokarsinom: Koryon villusu KESİNLİKLE YOK; anaplastik trofoblastlar; %50 akciğer"
        ],
        elements=[
            make_quiz(
                question="Gestasyonel trofoblastik hastalıklar spektrumunda yer alan patolojilerle ilgili aşağıdaki karşılaştırmalardan hangisi KESİNLİKLE YANLIŞTIR?",
                options=[
                    {"key": "A", "text": "Komplet mol hidatiformda koryon villuslarında fetal eritrositler ve damarlar bulunmaz.", "isCorrect": False, "explanation": "Doğru bir önermedir. Komplet mol avaskülerdir ve fetal doku içermez."},
                    {"key": "B", "text": "Parsiyel mol hidatiform triploid karyotipe (69,XXY) sahiptir ve maternal p57KIP2 ekspresyonu pozitiftir.", "isCorrect": False, "explanation": "Doğru bir önermedir. Parsiyel mol triploidtir ve p57 pozitiftir."},
                    {"key": "C", "text": "Koryokarsinom mikroskopisinde bol miktarda avasküler ödemli koryon villusları izlenir.", "isCorrect": True, "explanation": "Yanlış! Koryokarsinomda koryon villusları KESİNLİKLE YOKTUR; kitle sadece anaplastik sito ve sinsityotrofoblast tabakalarından oluşur."},
                    {"key": "D", "text": "İnvaziv molde hidropik villuslar myometrium derinliğine girer fakat koryokarsinom gibi agresif metastaz yapmaz.", "isCorrect": False, "explanation": "Doğru bir önermedir. İnvaziv molde villus invaziftir fakat metastaz görülmez."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Gestasyonel koryokarsinom mikroskopik incelemesinde mol hidatiformun aksine koryon villusları kesinlikle izlenmez.",
                masked_term="koryon villusları kesinlikle izlenmez",
                hint="Tümörde villöz yapıların tamamen bulunmaması durumu"
            ),
            make_table(
                title="Gestasyonel Trofoblastik Hastalıklar Büyük Karşılaştırma Matrisi",
                headers=["Özellik", "Komplet Mol", "Parsiyel Mol", "Koryokarsinom"],
                rows=[
                    [
                        {"text": "Karyotip Genetiği", "isMasked": False},
                        {"text": "Diploid (46,XX androgenetik)", "isMasked": True, "hint": "İki takım babadan gelen kromozom"},
                        {"text": "Triploid (69,XXY dispermik)", "isMasked": False},
                        {"text": "Kompleks anöploid", "isMasked": False}
                    ],
                    [
                        {"text": "Koryon Villusu Varlığı", "isMasked": False},
                        {"text": "Tüm villuslar hidropik / avasküler", "isMasked": False},
                        {"text": "Fokal hidropik villuslar", "isMasked": False},
                        {"text": "Villus KESİNLİKLE YOKTUR", "isMasked": True, "hint": "Villöz yapıların tamamen bulunmaması"}
                    ],
                    [
                        {"text": "Fetus / Embriyo Dokusu", "isMasked": False},
                        {"text": "Kesinlikle yoktur", "isMasked": False},
                        {"text": "Mevcuttur (fetal eritrositler)", "isMasked": True, "hint": "Embriyoya ait hücresel kanıtlar"},
                        {"text": "Yoktur", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Trofoblastik bir kitlede patoloğun 'villus gördüm' demesi ile 'hiç villus yok, sadece pleomorfik trofoblast tabakaları var' demesi arasındaki yaşamsal tanı farkı nedir?",
                answer="Villus varsa lezyon mol hidatiform veya invaziv moldür; villus kesinlikle yoksa ve anaplastik trofoblastlar varsa lezyon habis koryokarsinomdur."
            )
        ]
    ))

    # Slide 98
    slides.append(make_slide(
        slide_num=98,
        title="Uterus ve Plasenta Patolojisinde Bütünsel Klinik Karar Verme",
        subtitle="Vaka temelli klinik senaryolar ve acil obstetrik-onkolojik kararlar",
        clinical_focus="Klinik pratikte semptomdan patolojik tanıya ulaşma algoritması",
        narrative=(
            "Kurul 1 obstetrik ve jinekolojik patoloji olgularında doğru tanıya ulaşmak, klinik ipuçları ile patolojik morfolojiyi kusursuz birleştirmeyi gerektirir.\n\n"
            "- **Vaka 1 (Akut Karın ve Şok):** 6 haftalık amenore sonrası ani alt karın ağrısı ve şokla gelen hastada öncelikle tubal ektopik gebelik rüptürü düşünülür; laparotomide tuba kesitinde koryon villusları ve hematosalpinks aranır.\n"
            "- **Vaka 2 (Durdurulamayan Postpartum Kanama):** Geçirilmiş sezaryen öyküsü olan kadında plasentanın ayrılmaması ve masif kanama plasenta yapışma anomalilerini (akreta/perkreta) işaret eder; acil histerektomi hayat kurtarır.\n"
            "- **Vaka 3 (Doğum Sonrası Hemoptizi):** Normal doğum veya düşükten aylar sonra nefes darlığı, hemoptizi ve vajinada mor nodül görülen hastada kanda beta-hCG bakılır; koryokarsinom metastazı teşhis edilip kemoterapi başlanır.\n\n"
            "> [!NOTE]\n"
            "> Amenore + şok = ektopik gebelik; ayrılmayan plasenta + skar = perkreta; gebelik sonrası hemoptizi + yüksek hCG = koryokarsinom."
        ),
        bullets=[
            "Amenore + ani akut karın + şok: Rüptüre tubal ektopik gebelik (%90 ampulla)",
            "Doğumda ayrılmayan plasenta + masif kanama: Plasenta akreta/perkreta",
            "Gebelik/düşük sonrası hemoptizi + mor vajinal nodül: Metastatik koryokarsinom",
            "3. trimesterde HT + ödem + proteinüri + nöbet: Eklampsi (spiral arter defekti)"
        ],
        elements=[
            make_quiz(
                question="Doğumdan 6 ay sonra öksürük ve kan tükürme (hemoptizi) şikayetiyle göğüs hastalıklarına başvuran 28 yaşındaki bir kadının akciğer grafisinde her iki parankimde çok sayıda yuvarlak radyoopak 'top güllesi' lezyonları saptanıyor. Jinekolojik öyküsünde doğumdan beri düzensiz lekelenme tarzı kanamaları olduğu öğreniliyor. Bu hastada öncelikle hangi hormon tetkiki istenmelidir?",
                options=[
                    {"key": "A", "text": "Serum kantitatif beta-hCG düzeyi", "isCorrect": True, "explanation": "Doğru. Doğum sonrası hemoptizi ve akciğerde kanamalı nodüller koryokarsinom metastazını düşündürür; tanı kanda beta-hCG yüksekliği ile doğrulanır."},
                    {"key": "B", "text": "Serum paratiroid hormon (PTH)", "isCorrect": False, "explanation": "Kalsiyum metabolizması hormonudur."},
                    {"key": "C", "text": "Serum prolaktin düzeyi", "isCorrect": False, "explanation": "Prolaktin hipofiz hormonudur; pulmoner kitle yapmaz."},
                    {"key": "D", "text": "Serum insülin düzeyi", "isCorrect": False, "explanation": "Glukoz metabolizması hormonudur."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Doğum veya düşük sonrasında gelişen metastatik koryokarsinom olgularında tanı ve tedavi takibinde serum beta-hCG düzeyi kullanılır.",
                masked_term="serum beta-hCG düzeyi",
                hint="Sinsityotrofoblastlar tarafından salgılanan koryonik tümör belirteci"
            ),
            make_swipe(
                title="Klinik Senaryolar ve Patolojik Tanı Eşleştirmeleri",
                left_category="Trofoblastik ve Plasental Patolojiler",
                right_category="Myometrium Düz Kas Patolojileri",
                cards=[
                    {"text": "Term doğum sonrası vajinada mor nodül, hemoptizi ve devasa kanda hCG yüksekliği", "category": "left", "explanation": "Gestasyonel koryokarsinom metastazı tablosudur."},
                    {"text": "Postmenopozal dönemde soliter yumuşak kitle, nükleer atipi ve koagülatif nekroz", "category": "right", "explanation": "Uterin leiomyosarkomun klinik patolojisidir."},
                    {"text": "35 yaşında menorajisi olan kadında çok sayıda keskin sınırlı girdapsı nodül", "category": "right", "explanation": "Klasik intramural leiomyom bulgusudur."},
                    {"text": "Doğumda ayrılmayan plasenta ve myometriumu aşan koryon villusları", "category": "left", "explanation": "Plasenta perkreta komplikasyonudur."}
                ]
            ),
            make_recall(
                question="Genç bir kadında hemoptizi görüldüğünde primer akciğer tüberkülozu veya bronş karsinomu düşünülmeden önce neden mutlaka gestasyonel öykü ve hCG sorgulanmalıdır?",
                answer="Çünkü koryokarsinom üreme çağında akciğere en sık ve en hızlı metastaz yapan tümördür ve kemoterapiyle %100 tedavi edilebilir."
            )
        ]
    ))

    # Slide 99
    slides.append(make_slide(
        slide_num=99,
        title="Uterus Düz Kas ve Trofoblastik Tümörleri: 20 Sınav Altın Kuralı",
        subtitle="Prof. Dr. Hikmet Keleş Ders Notu Özeti ve Kurul 1 Spotları",
        clinical_focus="Tüm ders boyunca vurgulanan en kritik sınav spotlarının sentezi",
        narrative=(
            "Bu slayt, dersin tüm ünitelerinden süzülen 20 temel sınav spotunu özetler.\n\n"
            "- **Düz Kas:** 1) Leiomyom en sık benign tümördür (%30-50). 2) 6. ve 12. kromozom anomalileri görülür. 3) Kesit yüzü girdapsıdır. 4) Sarkoma dönüşmez, multiple olması riski artırmaz. 5) Leiomyosarkom soliterdir, postmenopozaldir, nekrotiktir ve de novo başlar. 6) Akciğere hematojen yayılır.\n"
            "- **Trofoblastlar:** 7) hCG mol < invaziv mol < koryokarsinom sırasıyla artar. 8) Komplet mol diploidtir (46,XX; boş ovum + 2 sperm; fetüs yok; p57 negatif; %2 koryokarsinom). 9) Parsiyel mol triploidtir (69,XXY; fetüs parçaları var; p57 pozitif). 10) İnvaziv molde villus var, metastaz yok, kemoterapiyle kür. 11) Koryokarsinomda villus KESİNLİKLE YOKTUR. 12) Koryokarsinom akciğer metastazı %50'dir. 13) Paternal antijenler nedeniyle kemoterapiyle %100 kürdür.\n"
            "- **Plasenta:** 14) Kordonda 2 arter 1 ven vardır; battledore marjinaldir. 15) Kord girişinde skuamöz metaplazi sıktır. 16) Asendan yol korioamnionit (nötrofil) yapar. 17) Ektopik gebelik %90 tüptedir; en sık neden kronik salpenjittir. 18) Preeklampsi temeli spiral arteriollerde yetersiz dilatasyondur. 19) Akut aterozis fibrinoid nekroz ve köpüksü makrofaj içerir. 20) Akreta/inkreta/perkreta desidua yokluğunda gelişir.\n\n"
            "> [!IMPORTANT]\n"
            "> Bu 20 kural Kurul 1 Patoloji sınavındaki düz kas ve trofoblastik soruların eksiksiz çözüm anahtarıdır."
        ),
        bullets=[
            "Leiomyom: Girdapsı, selim, sarkoma dönüşmez; Leiomyosarkom: Soliter, nekrotik, de novo",
            "Komplet mol: Diploid (46,XX), fetüs yok, p57 negatif; Parsiyel mol: Triploid (69,XXY)",
            "Koryokarsinom: Koryon villusu KESİNLİKLE YOKTUR; kemoterapiyle %100 tedavi edilir",
            "Preeklampsi: Spiral arterlerde yetersiz dilatasyon, akut aterozis ve DİC riski",
            "Plasenta: Kordonda 2 arter 1 ven; asendan korioamnionit; perkreta myometriumu aşar"
        ],
        elements=[
            make_quiz(
                question="Prof. Dr. Hikmet Keleş'in ders notunda vurgulanan ve patoloji sınavlarında en sık sorulan temel ilkelerden hangisi BİREBİR DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Leiomyomlar zamanla malignleşerek leiomyosarkoma dönüşürler ve multiple olmaları riski artırır.", "isCorrect": False, "explanation": "Yanlış! Leiomyomlar sarkoma dönüşmez; leiomyosarkom de novo başlar."},
                    {"key": "B", "text": "Komplet mol triploidtir ve bol miktarda fetal eritrosit içerir.", "isCorrect": False, "explanation": "Yanlış! Komplet mol diploidtir ve fetüs/damar içermez; parsiyel mol triploidtir."},
                    {"key": "C", "text": "Koryokarsinomda koryon villusları bulunmaz ve paternal antijenlerin varlığı sayesinde kemoterapi ile %100'e yakın kür elde edilir.", "isCorrect": True, "explanation": "Doğru. Koryokarsinomda koryon villusu kesinlikle yoktur; allogreft paternal antijenler kemoterapi ile %100 kür sağlar."},
                    {"key": "D", "text": "Preeklampsinin temel sebebi umbilikal kordon damarlarının tıkanmasıdır.", "isCorrect": False, "explanation": "Yanlış! Temel sebep uteroplasental yataktaki spiral arteriollerdeki yetersiz dilatasyondur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Gestasyonel trofoblastik hastalıklarda koryokarsinom koryon villuslarının bulunmaması ve paternal antijenler sayesinde kemoterapiyle tam tedavi edilebilmesi ile karakterizedir.",
                masked_term="paternal antijenler",
                hint="Babadan gelen yabancı doku proteinleri"
            ),
            make_table(
                title="Kurul 1 Uterus ve Trofoblastik Patoloji Altın Sentezi",
                headers=["Konu Alanı", "En Kritik Patolojik Özellik", "Temel Sınav Tuzağı / Çeldirici"],
                rows=[
                    [
                        {"text": "Leiomyom Biyolojisi", "isMasked": False},
                        {"text": "Monoklonal düz kas; girdapsı kesit", "isMasked": True, "hint": "Selim miyomun makroskobik karakteristik dokusu"},
                        {"text": "Sarkoma dönüşmez; multiplite riski artırmaz", "isMasked": False}
                    ],
                    [
                        {"text": "Koryokarsinom Histolojisi", "isMasked": False},
                        {"text": "Koryon villusu KESİNLİKLE YOKTUR", "isMasked": True, "hint": "Tümör parankiminde kistik ağaçsı uzantıların sıfır olması"},
                        {"text": "%50 metastaza rağmen kemoterapiyle %100 kür", "isMasked": False}
                    ],
                    [
                        {"text": "Preeklampsi Mekanizması", "isMasked": False},
                        {"text": "Spiral arteriollerde yetersiz dilatasyon", "isMasked": True, "hint": "Maternal damarların genişleyememesi defekti"},
                        {"text": "Akut aterozis, retroplasental hemoraji ve DİC", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Tıp fakültesi Kurul 1 Patoloji sınavında 'koryokarsinom' sorusu geldiğinde ilk kontrol edilmesi gereken negatif histopatolojik kriter nedir?",
                answer="'Koryon villusunun kesinlikle bulunmaması' kriteridir; villus görülürse tanı koryokarsinom olamaz."
            )
        ]
    ))

    # Slide 100 - Final Checkpoint 10
    slides.append(make_slide(
        slide_num=100,
        title="[TEKRAR SAYFASI - CHECKPOINT 10] Uterus Düz Kas ve Trofoblastik Tümörleri Büyük Finali",
        subtitle="100 Slaytlık Tam Deste Kapsamlı Değerlendirme ve Kurul 1 Sertifikasyonu",
        clinical_focus="Düz kas neoplazmları, gestasyonel trofoblastlar ve plasenta patolojisi büyük sentezi",
        narrative=(
            "Bu 100. adım, Kurul 1 (Ürogenital ve Obstetrik Kurulu) Uterus Düz Kas ve Trofoblastik Tümörleri dersinin tüm kazanımlarını nihai olarak mühürleyen büyük tekrar sayfasıdır.\n\n"
            "- **Myometrium Neoplazmları:** Leiomyom en sık selim neoplazmdır (6/12 kromozom, girdapsı, submukoz/intramural/subseröz, menoraji, dejenerasyonlar); sarkoma dönüşmez. Leiomyosarkom de novo başlar, soliter, postmenopozal, yumuşak, nekrotiktir; tanı triadı atipi, ≥10 mitoz ve koagülatif tümör nekrozudur; akciğere hematojen yayılır.\n"
            "- **Gestasyonel Trofoblastik Neoplaziler:** Komplet mol diploidtir (46,XX; boş ovum + 2 sperm; avasküler villus; p57 negatif; %2 koryokarsinom). Parsiyel mol triploidtir (69,XXY; fetal doku var; p57 pozitif). İnvaziv molde myometriuma giren villuslar vardır, metastaz yoktur, kemoterapiyle kür olur. Koryokarsinomda koryon villusu KESİNLİKLE YOKTUR; anaplastik sito/sinsityotrofoblastlardan oluşur; %50 akciğer metastazı yapar; paternal antijenler sayesinde kemoterapiyle %100 kürdür.\n"
            "- **Plasenta ve Obstetrik Patoloji:** Kordonda 2 arter 1 ven vardır; battledore marjinaldir; kord girişinde skuamöz metaplazi sıktır. Asendan enfeksiyon korioamnionit (nötrofil) yapar. Ektopik gebelik %90 tüptedir (kronik salpenjit). Preeklampsi spiral arteriollerde yetersiz dilatasyona bağlıdır; akut aterozis ve DİC yapar. Akreta/inkreta/perkreta desidua yokluğunda myometriuma yapışma/girme/aşmadır.\n\n"
            "> [!NOTE]\n"
            "> Tebrikler! 100 slaytlık tam deste başarıyla tamamlandı. Uterus düz kası, trofoblastik tümörler ve plasenta patolojisi Kurul 1 standartlarında eksiksiz öğrenildi."
        ),
        bullets=[
            "Leiomyom selim ve girdapsıdır, sarkoma dönüşmez; leiomyosarkom soliter ve nekrotiktir",
            "Komplet mol diploid (46,XX, p57-); parsiyel mol triploid (69,XXY, p57+) yapıdadır",
            "Koryokarsinomda koryon villusu KESİNLİKLE YOKTUR; kemoterapiyle %100 kür elde edilir",
            "Preeklampsi spiral arteriollerin açılamamasıdır; akut aterozis ve DİC riski doğurur",
            "Akreta süperfisyel yapışır; inkreta myometriuma girer; perkreta serozayı aşar"
        ],
        elements=[
            make_quiz(
                question="Deste boyunca öğrenilen patofizyolojik ve morfolojik mekanizmalar ışığında, aşağıdaki klinik-patolojik eşleştirmelerden hangisi DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Komplet mol hidatiform — Maternal p57KIP2 kuvvetli pozitifliği ve bol fetal eritrositler", "isCorrect": False, "explanation": "Yanlış. Komplet molde maternal alel ve fetal eritrosit yoktur; p57 negatiftir."},
                    {"key": "B", "text": "Uterin leiomyosarkom — Çok sayıda intramural girdapsı sert nodül ve östrojenle küçülme", "isCorrect": False, "explanation": "Yanlış. Bu leiomyomdur; sarkom soliter, yumuşak, nekrotiktir."},
                    {"key": "C", "text": "Preeklampsi — Spiral arteriollerde yetersiz dilatasyon, akut aterozis ve plasental iskemi", "isCorrect": True, "explanation": "Doğru. Spiral arteriollerin trofoblastlarca açılamaması ve akut aterozis preeklampsinin patolojik temelidir."},
                    {"key": "D", "text": "Gestasyonel koryokarsinom — Bol koryon villusları ve kemoterapiye tam direnç", "isCorrect": False, "explanation": "Yanlış. Koryokarsinomda villus kesinlikle yoktur ve kemoterapiye %100 duyarlıdır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Preeklampsi patolojisinde spiral arteriollerde yetersiz dilatasyon zemininde gelişen plasental hipoperfüzyon maternal sistemik endotel hasarına yol açar.",
                masked_term="yetersiz dilatasyon",
                hint="Damarların trofoblastik uyarana rağmen genişleyememesi defekti"
            ),
            make_table(
                title="Büyük Final: Kurul 1 Patoloji Başucu Ayırıcı Tanı Tablosu",
                headers=["Patolojik Antite", "Karakteristik Mikroskopi / Biyolojik Belirteç", "En Önemli Klinik Özellik"],
                rows=[
                    [
                        {"text": "Leiomyom", "isMasked": False},
                        {"text": "İğsi düz kas demetleri, girdapsı; mitoz az", "isMasked": True, "hint": "Benign fibröz patern ve düşük bölünme oranı"},
                        {"text": "Kadında en sık selim tümör; menoraji; sarkoma dönüşmez", "isMasked": False}
                    ],
                    [
                        {"text": "Leiomyosarkom", "isMasked": False},
                        {"text": "Atipi, ≥10 mitoz, koagülatif tümör nekrozu", "isMasked": True, "hint": "Malign düz kas tanı triadı"},
                        {"text": "Soliter, postmenopozal; de novo başlar; akciğer metastazı", "isMasked": False}
                    ],
                    [
                        {"text": "Komplet Mol", "isMasked": False},
                        {"text": "Diffüz hidropik avasküler villus; p57 negatif", "isMasked": True, "hint": "Diploid androgenetik yapı"},
                        {"text": "Üzüm salkımı kistler; fetüs yok; %2 koryokarsinom", "isMasked": False}
                    ],
                    [
                        {"text": "Koryokarsinom", "isMasked": False},
                        {"text": "Koryon villusu KESİNLİKLE YOK; anaplastik sito/sinsityo", "isMasked": False},
                        {"text": "Paternal antijenler sayesinde kemoterapiyle %100 kür", "isMasked": True, "hint": "Allogreft immün yanıtıyla sağlanan tam şifa"}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Deste 54 Büyük Final Kontrol Önermeleri",
                items=[
                    {"text": "Leiomyomlar sarkoma dönüşmezler ve multiple olmaları malignite riskini artırmaz.", "isLie": False, "explanation": "Doğru. Düz kas tümörlerinin temel kuralıdır."},
                    {"text": "Komplet mol diploid (46,XX) olup maternal p57KIP2 negatiftir; parsiyel mol ise triploidtir (69,XXY).", "isLie": False, "explanation": "Doğru. Genetik sınıflamanın temelidir."},
                    {"text": "Gestasyonel koryokarsinom paternal antijenler taşır ve koryon villusları içerdiği için kemoterapiye %100 yanıt verir.", "isLie": True, "explanation": "Tuzak! Koryokarsinomda koryon villusları KESİNLİKLE YOKTUR! Paternal antijenler vardır fakat villus bulunmaz."},
                    {"text": "Plasenta perkretada koryon villusları myometriumu tam kat aşarak serozaya ulaşır.", "isLie": False, "explanation": "Doğru. En derin ve rüptür riski en yüksek invazyon tipidir."}
                ]
            ),
            make_recall(
                question="Büyük Final Sorusu: Kurul 1 Patoloji dersinde işlenen 'Uterus Düz Kas ve Trofoblastik Tümörleri' ünitesinde kemoterapiye duyarlılık açısından taban tabana zıt olan iki habis tümör hangileridir ve nedenleri nedir?",
                answer="Leiomyosarkom kemoterapiye son derece dirençlidir (kendi dokusudur, cerrahi şarttır); gestasyonel koryokarsinom ise paternal yabancı antijenler taşıdığı için kemoterapiye aşırı duyarlıdır (%100 kür elde edilir)."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=10
    ))

    return slides
