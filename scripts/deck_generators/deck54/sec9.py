"""
Deck 54 Section 9: Plasenta Patolojisi ve İntrauterin Enfeksiyonlar
Slides 81-90 (Checkpoint 9 at slide 90)
Focus:
- Umbilikal kord anomalileri (tek umbilikal arter, velamentöz kord insersiyonu, vasa previa)
- Kordona ait battledore plasenta vs santral insersiyon
- Amniyon ve koryon zarlarının patolojisi (kord girişinde skuamöz metaplazi, amnion nodozum)
- Asendan enfeksiyonlar (korioamnionit, funisit, lökosit infiltrasyonu)
- Erken membran rüptürü (EMR) ve preterm eylem patofizyolojisi
- Fetal inflamatuar yanıt sendromu (FİRS) ve sistemik fetal riskler (BPD, serebral palsi)
- Hematojen transplasental enfeksiyonlar ve villit histolojisi (intervillöz boşluk vs villöz parankim)
- TORCH kompleksi (Toksoplazma, Rubella, CMV, Herpes) ve Treponema pallidum / Sifiliz plasentası
- Listeria monocytogenes mikroabseleri ve granülomatöz villit
- Checkpoint 9
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

def get_sec9_slides():
    slides = []

    # Slide 81
    slides.append(make_slide(
        slide_num=81,
        title="Umbilikal Kord Morfolojisi ve Giriş Anomalileri",
        subtitle="Wharton jeli, damar anatomisi, battledore insersiyon ve velamentöz kord",
        clinical_focus="Kordonun plasentaya yapışma tipleri ve fetal hipoksi riskleri",
        narrative=(
            "Termdeki normal umbilikal kord ortalama 55-60 cm uzunluğunda olup, fetal uçta stratifiye amniyotik epitelle döşelidir ve Wharton jeli içinde **2 arter ve 1 ven** barındırır.\n\n"
            "- **Battledore Plasenta (Marjinal İnsersiyon):** Normalde santral veya parasantral bağlanan kordonun, plasental diskin tam kenarına (marjine) yapışması durumudur. Kord plasenta kenarından raket şeklinde ayrılır; genellikle fetal dolaşımı tıkamaz fakat doğum eyleminde avülsiyon riski taşır.\n"
            "- **Velamentöz Kord İnsersiyonu:** Kord plasental diske hiç ulaşamaz; kordon damarları plasentadan uzakta, amniyon ve koryon membranları arasında çıplak olarak dallanır. Damarlar Wharton jeli korumasından tamamen yoksundur.\n"
            "- **Klinik Yansıma:** Çıplak membranöz damarlar doğum kanalının üzerine gelirse (vasa previa) membran rüptürüyle birlikte yırtılarak dakikalar içinde fetüsün kan kaybından ölümüne neden olur.\n\n"
            "> [!IMPORTANT]\n"
            "> Kordonun plasenta kenarına yapışmasına battledore plasenta; plasentaya ulaşamayıp zarlar arasında çıplak dallanmasına ise velamentöz insersiyon denir."
        ),
        bullets=[
            "Normal kordonda Wharton jeli içinde 2 arter ve 1 ven bulunur",
            "Battledore insersiyon: Kordonun plasenta kenarına marjinal yapışmasıdır",
            "Velamentöz insersiyon: Damarların zarlar arasında çıplak olarak seyretmesidir",
            "Zarlar arasındaki çıplak damarlar yırtılmaya ve masif fetal kanamaya açıktır"
        ],
        elements=[
            make_quiz(
                question="Doğum sonrasında plasentanın incelenmesinde, umbilikal kordun plasental parankim diskinin tam kenarına yapıştığı ve tenis raketine benzer bir görünüm sergilediği saptanıyor. Bu gross plasental anatomik varyasyon hangisidir?",
                options=[
                    {"key": "A", "text": "Battledore plasenta", "isCorrect": True, "explanation": "Doğru. Umbilikal kordonun plasental diskin tam kenarına marjinal yapışması battledore plasenta olarak adlandırılır."},
                    {"key": "B", "text": "Plasenta akreta", "isCorrect": False, "explanation": "Akreta myometriuma anormal yapışmadır; kord varyasyonu değildir."},
                    {"key": "C", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Mol hidatiform avasküler kistik veziküllerdir."},
                    {"key": "D", "text": "Plasenta perkreta", "isCorrect": False, "explanation": "Perkreta myometriumu ve serozayı aşan invazyondur."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Umbilikal kordonun plasental diske merkez yerine tam kenardan giriş yaptığı varyasyona battledore plasenta denir.",
                masked_term="battledore plasenta",
                hint="Raket manzaralı marjinal göbek kordonu bağlantısı"
            ),
            make_slider(
                left_title="Battledore Plasenta (Marjinal Kord)",
                right_title="Velamentöz Kord İnsersiyonu",
                left_points=[
                    "Kordon plasental diskin tam kenar sınırına yapışır",
                    "Damarlar disk kenarına kadar Wharton jeli kılıfı içindedir",
                    "Rüptür riski düşüktür; mekanik çekintide kopma riski vardır"
                ],
                right_points=[
                    "Kordon plasental parankime ulaşmadan zarlara yapışır",
                    "Fetal damarlar membranlar arasında korumasız ve çıplak seyreder",
                    "Vasa previa ve membran yırtılmasında masif fetal exsanguinasyon riski taşır"
                ]
            ),
            make_recall(
                question="Velamentöz kord insersiyonu olan bir gebelikte amniyotik zarlar açıldığında çıplak kordon damarlarının yırtılması neden anne için değil doğrudan fetüs için ölümcül kanamaya yol açar?",
                answer="Çünkü yırtılan çıplak damarlar maternal değil fetal dolaşıma aittir; fetüsün toplam kan hacmi çok az olduğundan hızla hipovolemik şoktan ölür."
            )
        ]
    ))

    # Slide 82
    slides.append(make_slide(
        slide_num=82,
        title="Tek Umbilikal Arter (TUA) ve Damar Anomalileri",
        subtitle="İki arter bir ven kuralının bozulması ve konjenital anomali taraması",
        clinical_focus="Kordon kesitinde 1 arter 1 ven görülmesinin klinik anlamı",
        narrative=(
            "Normal insan umbilikal kordonunun transvers kesitinde üç adet damar lümeni izlenir: kirli kanı fetüsten plasentaya taşıyan iki umbilikal arter ve oksijenlenmiş temiz kanı fetüse getiren bir umbilikal ven.\n\n"
            "- **Tek Umbilikal Arter (TUA):** Arterlerden birinin agenezi veya erken embriyonik tromboz sonucu atrezik kalmasıyla kordonda sadece **1 arter ve 1 ven** bulunması durumudur.\n"
            "- **Görülme Sıklığı:** Tekil gebeliklerin yaklaşık %1'inde, ikiz gebeliklerde ise daha yüksek oranda görülür.\n"
            "- **Klinik Önemi:** Tek umbilikal arter saptanan bebeklerin yaklaşık %20-30'unda kardiyovasküler, renal ve gastrointestinal sistem anomalileri ile kromozomal anöploidiler (Trizomi 18/Edwards, Trizomi 13) eşlik eder. Bu nedenle doğum öncesi ultrasonda kordonda tek arter görülmesi, detaylı fetal anomali taraması için majör bir endikasyondur.\n\n"
            "> [!NOTE]\n"
            "> Kordonda 2 arter 1 ven yerine tek arter bulunması (TUA), kardiyovasküler ve renal konjenital malformasyon riskini artırır."
        ),
        bullets=[
            "Normal umbilikal kordonda 2 arter ve 1 ven bulunur",
            "Tek umbilikal arterde arterlerden biri agenezik veya atreziktir",
            "TUA olgularının %20-30'unda majör fetal konjenital anomaliler eşlik eder",
            "Kardiyak, renal malformasyonlar ve trizomiler açısından ileri tarama gerekir"
        ],
        elements=[
            make_quiz(
                question="Yeni doğan bir bebeğin göbek kordonu transvers kesitinde Wharton jeli içinde sadece bir adet kalın duvarlı dar lümenli arter ve bir adet geniş lümenli ven saptanıyor (tek umbilikal arter). Bu bulgu klinisyeni öncelikle hangi yönde araştırmaya sevk etmelidir?",
                options=[
                    {"key": "A", "text": "Hiçbir tetkik yapmadan bebeği hemen taburcu etmek", "isCorrect": False, "explanation": "Tek umbilikal arter konjenital anomali riskini belirgin artırır; araştırılmalıdır."},
                    {"key": "B", "text": "Eşlik edebilecek kardiyovasküler, renal ve kromozomal anomalileri araştırmak", "isCorrect": True, "explanation": "Doğru. Tek umbilikal arter olgularının %20-30'unda konjenital kardiyak, renal ve yapısal defektler eşlik eder."},
                    {"key": "C", "text": "Hemen acil laparotomi ile apandisit ameliyatı planlamak", "isCorrect": False, "explanation": "Apandisitle hiçbir ilişkisi yoktur."},
                    {"key": "D", "text": "Maternal kanda beta-hCG seviyelerini ölçüp mol aramak", "isCorrect": False, "explanation": "Kord anomalisi plasental molar hastalıkla ilişkili değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Göbek kordonu kesitinde iki arter yerine tek umbilikal arter saptanması fetal kardiyak ve renal konjenital anomaliler açısından uyarıcıdır.",
                masked_term="tek umbilikal arter",
                hint="Çift atardamar yerine yalnız bir atardamar içeren vasküler malformasyon"
            ),
            make_table(
                title="Umbilikal Kord Vasküler Anatomisi ve Varyasyonları",
                headers=["Kordon Damar Sayısı", "Lümen Morfolojisi", "Klinik Yansıma / İlişki"],
                rows=[
                    [
                        {"text": "Normal Kordon (3 Damar)", "isMasked": False},
                        {"text": "2 arter (küçük, kaslı) + 1 ven (geniş)", "isMasked": True, "hint": "Wharton jeli içindeki standart üçlü damar yapısı"},
                        {"text": "Fizyolojik plasental-fetal gaz değişimi", "isMasked": False}
                    ],
                    [
                        {"text": "Tek Umbilikal Arter (2 Damar)", "isMasked": False},
                        {"text": "1 arter + 1 ven", "isMasked": True, "hint": "Tekil atardamar kalması durumu"},
                        {"text": "Kardiyak, renal malformasyon ve anöploidi riski (%20-30)", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Doğum salonunda ebe veya çocuk hekimi plasentayı kestiğinde göbek kordonunun kesit yüzeyini neden rutin olarak inceler?",
                answer="Kordonda normalde bulunması gereken 2 arter ve 1 ven yapısının tam olup olmadığını (tek umbilikal arter varlığını) teyit etmek için inceler."
            )
        ]
    ))

    # Slide 83
    slides.append(make_slide(
        slide_num=83,
        title="Fetal Membranlar ve Kord Girişinde Skuamöz Metaplazi",
        subtitle="Amniyon, koryon ve yüzey epitelinin fizyolojik metaplazisi",
        clinical_focus="Amniyon zarındaki beyaz plakların tümörle karışmaması",
        narrative=(
            "Plasental membranlar içte amniyotik kaviteyi sınırlayan amniyon ve dışta fetal damarları taşıyan koryon tabakalarından oluşur.\n\n"
            "- **Amniyotik Epitel ve Skuamöz Metaplazi:** Amniyon zarı normalde bazal membran üzerinde tek katlı küboid-yassı epitel hücreleri ile döşelidir. Özellikle term gebeliklerde ve **umbilikal kordun plasentaya giriş yaptığı bölgenin yakınında**, amniyotik epitelde tabakalanma ve keratinizasyon gelişerek **skuamöz metaplazi** odakları ortaya çıkar. Makroskopik olarak kord kökünde küçük, sert, beyazımsı nodüller ve plaklar şeklinde görülür. Bu tamamen selim bir matürasyon değişikliğidir; enfeksiyon veya tümör değildir.\n"
            "- **Amnion Nodozum Ayrımı:** Amniyon üzerindeki küçük plaklar oligohidramniyosa (fetal idrar yokluğuna) bağlı dökülen fetal squam ve saç kümelerinin oluşturduğu 'amnion nodozum' ile karışabilir. Amnion nodozumda epitel metaplazisi değil, yüzeye yapışmış keratinize debris birikimi izlenir.\n\n"
            "> [!NOTE]\n"
            "> Umbilikal kord girişinde amniyon zarında izlenen skuamöz metaplazi sık görülen selim bir bulgudur; neoplazi veya aktif enfeksiyon değildir."
        ),
        bullets=[
            "Amniyon tek katlı küboid epiteldir; kord girişinde skuamöz metaplazi sıktır",
            "Kord kökünde küçük beyaz sert nodüller ve keratinize plaklar görülebilir",
            "Bu durum tamamen fizyolojik ve selimdir; maligniteyle karıştırılmamalıdır",
            "Amnion nodozum ise oligohidramniyos zemininde yüzey debris yapışmasıdır"
        ],
        elements=[
            make_quiz(
                question="Term bir plasentanın makroskobik incelemesinde umbilikal kordun plasentaya giriş yaptığı bölgenin hemen çevresindeki amniyon zarında birkaç milimetre çapında, beyaz renkli, sert, parlak nodüler odaklar izleniyor. Mikroskopide bu odaklarda tek katlı amniyotik epitelin yerini çok katlı yassı epitelyal hücrelerin aldığı saptanıyor. En olası tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Plasental karsinosarkom", "isCorrect": False, "explanation": "Plasentada karsinosarkom görülmez; uterus korpus malignitesidir."},
                    {"key": "B", "text": "Komplet mol hidatiform kistleri", "isCorrect": False, "explanation": "Mol hidatiform villöz hidroptur; amniyon zarı metaplazisi değildir."},
                    {"key": "C", "text": "Koryokarsinomun kord metastazı", "isCorrect": False, "explanation": "Koryokarsinom kanamalı nekrotik kitle yapar; selim plak yapmaz."},
                    {"key": "D", "text": "Amniyon zarında skuamöz metaplazi", "isCorrect": True, "explanation": "Doğru. Özellikle kord giriş yerinde amniyonda skuamöz metaplazi sık görülen selim bir lezyondur."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Amniyotik kaviteyi çevreleyen amniyon zarında, özellikle umbilikal kordun giriş yerinde skuamöz metaplazi sıklıkla izlenir.",
                masked_term="skuamöz metaplazi",
                hint="Tek katlı epitelin çok katlı yassı koruyucu epitele dönüşmesi"
            ),
            make_venn(
                title="Amniyon Skuamöz Metaplazisi vs Amnion Nodozum",
                label_a="Amniyon Skuamöz Metaplazisi",
                label_b="Amnion Nodozum",
                items=[
                    {"criterion": "Amniyotik epitelin bizzat kendisinin çok katlı yassı epitele dönüşmesi", "correct": "A", "explanation": "Skuamöz metaplazi epitelin hücresel diferansiasyonudur."},
                    {"criterion": "Şiddetli oligohidramniyos zemininde fetal verniks, kıl ve deskuame hücre yığılması", "correct": "B", "explanation": "Amnion nodozum fetal idrar azlığında dökülen döküntülerin agregatıdır."},
                    {"criterion": "Amniyon yüzeyinde makroskopik olarak küçük beyaz nodüller şeklinde belirebilme", "correct": "both", "explanation": "Her iki durum da amniyon zarında granüler nodüler lezyon manzarası verir."},
                    {"criterion": "Maternal desidua tabakasının tam kat yokluğuyla myometriuma yapışma", "correct": "neither", "explanation": "Bu plasenta akretadır; amniyon lezyonu değildir."}
                ]
            ),
            make_recall(
                question="Amniyon zarında görülen skuamöz metaplazi patolojik bir karsinom öncülü müdür, klinik önemi nedir?",
                answer="Karsinom öncülü değildir; klinik önemi selim bir matürasyon bulgusu olup enfeksiyon veya tümörlerle karıştırılmaması gerektiğidir."
            )
        ]
    ))

    # Slide 84
    slides.append(make_slide(
        slide_num=84,
        title="Asendan Plasental Enfeksiyonlar ve Korioamnionit Patolojisi",
        subtitle="Vajinal flora patojenleri, membran rüptürü ve nötrofil infiltrasyonu",
        clinical_focus="Erken membran rüptürü ve prematüre doğumun temel nedeni",
        narrative=(
            "Plasentanın enfeksiyonları temelde iki ana yol ile meydana gelir: doğum kanalından yukarıya doğru ilerleyen **asendan enfeksiyonlar** ve maternal kandan gelen **hematojen (transplasental) enfeksiyonlar**.\n\n"
            "- **En Sık Yol (Asendan Enfeksiyon):** Plasental enfeksiyonların ezici çoğunluğu doğum kanalından (vajina ve serviksten) yukarıya doğru asendan yolla tırmanır. Çoğu olguda bakteriyeldir (Ureaplasma, Mycoplasma hominis, B grubu streptokoklar, E. coli ve Gardnerella vaginalis).\n"
            "- **Korioamnionit Morfolojisi:** Bakteriler amniyotik kaviteye ulaştığında koryoamniyotik membranlarda ödem, yoğun konjesyon ve nötrofil lökosit infiltrasyonu oluşturur (**korioamnionit**). Amniyotik sıvı bulanıklaşır ve pürülan kötü kokulu bir hal alır.\n"
            "- **Klinik Tetikleyici:** Korioamnionit erken membran rüptürünün (EMR) ve spontan preterm doğumların (erken doğum) en sık ve en önemli nedenidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Plasentanın en sık enfeksiyon yolu asendan yoldur; koryoamniyotik zarlarda nötrofil infiltrasyonu (korioamnionit) yapar ve erken doğumu tetikler."
        ),
        bullets=[
            "En sık enfeksiyon yolu doğum kanalından tırmanan asendan yoldur",
            "Genellikle bakteriyeldir (Ureaplasma, Mycoplasma, vajinal flora bakterileri)",
            "Membranlarda ödem, konjesyon ve nötrofil infiltrasyonu (korioamnionit) izlenir",
            "Erken membran rüptürü (EMR) ve preterm doğumların en sık sebebidir"
        ],
        elements=[
            make_quiz(
                question="32 haftalık bir gebede vajinadan kötü kokulu sıvı gelmesi, ateş (38.8 °C) ve uterus hassasiyeti sonrası erken doğum gerçekleşiyor. Plasentanın incelenmesinde koryoamniyotik zarların donuklaştığı, mikroskopide zarların stromasında yoğun nötrofil lökosit infiltrasyonu ve ödem bulunduğu saptanıyor. En olası patolojik tablo hangisidir?",
                options=[
                    {"key": "A", "text": "Transplasental kronik villit", "isCorrect": False, "explanation": "Transplasental enfeksiyonlar villit yapar ve lenfohistiyositerdir; asendan membran tutulumu değildir."},
                    {"key": "B", "text": "Plasental koryokarsinom perforasyonu", "isCorrect": False, "explanation": "Koryokarsinom trofoblastik tümördür; zarlarda akut nötrofil infiltrasyonu ve ateş yapmaz."},
                    {"key": "C", "text": "Akut bakteriyel korioamnionit", "isCorrect": True, "explanation": "Doğru. Vajinal yoldan asendan tırmanan bakterilerin zarlarda yaptığı akut nötrofilik iltihap korioamnionittir."},
                    {"key": "D", "text": "İskemik kırmızı dejenerasyon", "isCorrect": False, "explanation": "Kırmızı dejenerasyon leiomyomun iskemik nekrozudur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Doğum kanalından yukarıya doğru ulaşan asendan bakteriyel enfeksiyonlar zarlarda akut korioamnionit tablosuna neden olur.",
                masked_term="korioamnionit",
                hint="Amniyon ve koryon zarlarının akut nötrofilik iltihabı"
            ),
            make_chain(
                title="Asendan Plasental Enfeksiyon ve Erken Doğum Mekanizması",
                steps=[
                    "1. Kolonizasyon: Vajina ve serviksteki bakteriyel patojenler servikal kanalı aşarak ilerler.",
                    "2. Membran İstilası: Koryon ve amniyon zarları enfekte olarak yoğun nötrofilik korioamnionit gelişir.",
                    "3. Enzimatik Zayıflama: Lökosit kaynaklı elastaz ve matriks metalloproteinazlar zarları eriterek erken membran rüptürüne yol açar.",
                    "4. Preterm Eylem: Açığa çıkan sitokinler ve prostaglandinler uterus kasılmalarını başlatarak erken doğuma neden olur."
                ]
            ),
            make_recall(
                question="Doğum eyleminde plasenta zarlarının normal şeffaf-parlak görünümünü kaybedip donuk, sarı-yeşil renkli ve kötü kokulu olması makroskobik olarak neyi gösterir?",
                answer="Şiddetli bakteriyel akut korioamnioniti (asendan zarlar enfeksiyonunu) gösterir."
            )
        ]
    ))

    # Slide 85
    slides.append(make_slide(
        slide_num=85,
        title="Göbek Kordonu Enfeksiyonu: Funisit ve Akut Vaskülit",
        subtitle="Umbilikal ven ve arter duvarlarında lökosit göçü ve fetal risk",
        clinical_focus="Kordon vaskülitinin fetal inflamatuar yanıt ile ilişkisi",
        narrative=(
            "Asendan bakteriyel enfeksiyon koryoamniyotik zarlarla sınırlı kalmayıp amniyotik sıvı aracılığıyla umbilikal kordona ulaştığında **funisit (kordon iltihabı)** gelişir.\n\n"
            "- **Histopatolojik Progresyon (Vaskülit):** İltihap önce umbilikal ven duvarındaki lökosit infiltrasyonu ile başlar (**akut flebit**). Süreç ilerledikçe umbilikal arter duvarlarına geçer (**akut arterit**) ve en sonunda Wharton jeline yayılarak tüm kordonda yaygın panvaskülite ve funisite dönüşür.\n"
            "- **Fetal Köken:** Kordon damarlarındaki nötrofiller maternal değil, **fetüsün kendi lökositleridir**. Fetüs enfeksiyona karşı damar duvarlarından Wharton jeline doğru lökosit göçü (kemotaksis) başlatmıştır.\n"
            "- **Klinik Önem:** Funisit varlığı, enfeksiyonun artık zarlardan fetüse geçtiğini ve fetüste sistemik inflamatuar yanıt başladığını gösteren kesin kanıttır.\n\n"
            "> [!IMPORTANT]\n"
            "> Umbilikal kordondaki akut vaskülit ve Wharton jeli nötrofil infiltrasyonuna funisit denir; bu damarlardaki nötrofiller fetüsün kendi lökositleridir."
        ),
        bullets=[
            "İnfeksiyon membranlardan göbek kordonuna yayıldığında funisit gelişir",
            "İlk tutulan damar umbilikal vendir (flebit), ardından arterler tutulur (arterit)",
            "Kordon damarlarından göç eden nötrofiller doğrudan fetüse aittir",
            "Funisit, fetüsün intrauterin enfeksiyona aktif bağışıklık yanıtı verdiğini gösterir"
        ],
        elements=[
            make_quiz(
                question="Korioamnionitli bir doğum sonrasında göbek kordonunun histolojik kesitinde, umbilikal ven ve arterlerin musküler duvarlarında ve Wharton jelinde yoğun nötrofil lökosit birikimi saptanıyor. Bu lökositlerin kökeni ve patolojik tablonun adı hangisinde doğru eşleştirilmiştir?",
                options=[
                    {"key": "A", "text": "Maternal lökositler — Battledore plasenta", "isCorrect": False, "explanation": "Battledore kord yapışma anomalisidir; lökosit infiltrasyonu değildir."},
                    {"key": "B", "text": "Tümör hücreleri — Koryokarsinom metastazı", "isCorrect": False, "explanation": "İnfiltre hücreler trofoblastik tümör değil nötrofildir."},
                    {"key": "C", "text": "Fetal nötrofiller — Funisit (akut kordon iltihabı)", "isCorrect": True, "explanation": "Doğru. Umbilikal kordon damarlarındaki nötrofiller doğrudan fetüse aittir ve tabloya funisit denir."},
                    {"key": "D", "text": "Desidual hücreler — Plasenta akreta", "isCorrect": False, "explanation": "Akreta myometriyal yapışmadır; kordon iltihabı değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Asendan enfeksiyonun göbek kordonuna ulaşarak umbilikal damar duvarlarında akut vaskülit ve Wharton jeli iltihabı oluşturmasına funisit denir.",
                masked_term="funisit",
                hint="Umbilikal kordonun akut lökositik inflamasyonu"
            ),
            make_slider(
                left_title="Korioamnionit (Zarlar)",
                right_title="Funisit (Göbek Kordonu)",
                left_points=[
                    "Amniyon ve koryon zarlarının nötrofilik infiltrasyonudur",
                    "İnflamasyonun öncü basamağıdır; sıklıkla maternal lökositler hakimdir",
                    "Membran rüptürü ve erken doğum sancılarını tetikler"
                ],
                right_points=[
                    "Umbilikal damar duvarlarının ve Wharton jelinin iltihabıdır",
                    "Damarlardan çıkan nötrofiller doğrudan fetüsün kendi lökositleridir",
                    "Enfeksiyonun fetüse ulaştığını ve fetal sepsisi gösterir"
                ]
            ),
            make_recall(
                question="Bir göbek kordonu kesitinde funisit saptandığında, bu kordon damarlarından dokuya göç eden lökositlerin fetal dolaşımdan geldiğini nasıl anlarız?",
                answer="Çünkü umbilikal kordondaki kan tamamen fetüse aittir; kordon damarları anne kanı taşımaz, dolayısıyla lökositler de fetüsün kendi kan hücreleridir."
            )
        ]
    ))

    # Slide 86
    slides.append(make_slide(
        slide_num=86,
        title="Fetal İnflamatuar Yanıt Sendromu (FİRS) ve Sistemik Sekeller",
        subtitle="İntrauterin sitokin fırtınası, bronkopulmoner displazi ve serebral palsi",
        clinical_focus="İntraamniyotik enfeksiyonun yenidoğan üzerindeki nörolojik sonuçları",
        narrative=(
            "Korioamnionit ve funisit sadece lokal bir plasenta problemi değildir; fetüste sistemik bir immün kaskadı tetikler (**Fetal İnflamatuar Yanıt Sendromu - FİRS**).\n\n"
            "- **Patofizyoloji:** Amniyotik sıvıdaki bakterileri yutan veya aspire eden fetüsün dolaşımında yüksek düzeyde proinflamatuar sitokinler (özellikle **İnterlökin-6, IL-1 ve TNF-alfa**) salgılanır.\n"
            "- **Fetal Organ Hasarı:** Bu sitokin fırtınası fetal beyin, akciğer ve damar endotelinde yaygın mikrovasküler hasara neden olur.\n"
            "- **Uzun Dönem Sekeller:** FİRS gelişen prematüre bebeklerde doğum sonrasında **bronkopulmoner displazi (BPD)**, nekrotizan enterokolit (NEK), periventriküler lökomalazi ve yaşam boyu kalıcı motor sekellere yol açan **serebral palsi** riski katlanarak artar.\n\n"
            "> [!NOTE]\n"
            "> Korioamnionite bağlı salınan fetal İnterlökin-6 ve sitokinler, beyinde periventriküler lökomalaziye yol açarak serebral palsi riskini artırır."
        ),
        bullets=[
            "Korioamnionit fetüste Fetal İnflamatuar Yanıt Sendromunu (FİRS) tetikler",
            "Fetal kanda İnterlökin-6 (IL-6) ve sitokin seviyeleri dramatik yükselir",
            "Beyinde periventriküler lökomalazi yaparak serebral palsiye zemin hazırlar",
            "Akciğerde matürasyonu bozarak bronkopulmoner displazi (BPD) yapar"
        ],
        elements=[
            make_quiz(
                question="İntrauterin bakteriyel korioamnionit ve funisit zemininde doğan prematüre bir bebekte kordon kanında belirgin yükseldiği saptanan ve neonatal dönemde periventriküler lökomalazi ile serebral palsi gelişiminden sorumlu tutulan temel proinflamatuar sitokin hangisidir?",
                options=[
                    {"key": "A", "text": "Human koryonik gonadotropin (hCG)", "isCorrect": False, "explanation": "hCG plasental trofoblastik hormondur; inflamatuar sitokin değildir."},
                    {"key": "B", "text": "İnterlökin-6 (IL-6)", "isCorrect": True, "explanation": "Doğru. FİRS tablosunda kordon kanında yükselen IL-6, fetal beyin beyaz cevher hasarı (periventriküler lökomalazi) ve serebral palsinin temel biyobelirtecidir."},
                    {"key": "C", "text": "Östrojen", "isCorrect": False, "explanation": "Steroid hormondur."},
                    {"key": "D", "text": "Human plasental laktojen (hPL)", "isCorrect": False, "explanation": "Metabolik plasenta hormonudur."},
                    {"key": "E", "text": "Progesteron", "isCorrect": False, "explanation": "Gebelik koruyucu hormondur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Korioamnionit zemininde fetal kanda İnterlökin-6 yükselmesiyle karakterize Fetal İnflamatuar Yanıt Sendromu beyinde periventriküler lökomalazi tablosuna yol açabilir.",
                masked_term="periventriküler lökomalazi",
                hint="Fetal beyin beyaz cevherinde sitokin kaynaklı iskemik-nekrotik hasar"
            ),
            make_table(
                title="Fetal İnflamatuar Yanıt Sendromu (FİRS) Hedef Organ Hasarları",
                headers=["Hedef Organ", "Patolojik Mekanizma", "Yenidoğandaki Klinik Sekel"],
                rows=[
                    [
                        {"text": "Merkezi Sinir Sistemi", "isMasked": False},
                        {"text": "Sitokin aracılı beyaz cevher hasarı", "isMasked": True, "hint": "Glia ve nöral dokunun toksik dejenerasyonu"},
                        {"text": "Periventriküler lökomalazi ve Serebral Palsi", "isMasked": False}
                    ],
                    [
                        {"text": "Fetal Akciğer", "isMasked": False},
                        {"text": "Alveolar gelişim duraklaması", "isMasked": False},
                        {"text": "Bronkopulmoner Displazi (BPD)", "isMasked": True, "hint": "Prematüre yenidoğanın kronik akciğer hastalığı"}
                    ],
                    [
                        {"text": "Gastrointestinal Sistem", "isMasked": False},
                        {"text": "Mukozal iskemi ve bakteriyel translokasyon", "isMasked": False},
                        {"text": "Nekrotizan Enterokolit (NEK)", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Klinisyenlerin korioamnionitli gebeleri hızla doğurtmak istemelerinin arkasındaki en kritik nörolojik korku nedir?",
                answer="Fetüsün maruz kaldığı sitokin fırtınasının (FİRS) beyinde kalıcı periventriküler lökomalazi ve serebral palsi hasarı oluşturması korkusudur."
            )
        ]
    ))

    # Slide 87
    slides.append(make_slide(
        slide_num=87,
        title="Hematojen (Transplasental) Enfeksiyonlar ve Kronik Villit",
        subtitle="Maternal kandan koryon villuslarına yayılım ve histopatolojik ayrım",
        clinical_focus="Asendan korioamnionit ile hematojen villit patolojisinin karşılaştırılması",
        narrative=(
            "Asendan enfeksiyonların aksine, **hematojen (transplasental) enfeksiyonlar** anne kanında dolaşan mikroorganizmaların plasenta villöz parankimine ulaşmasıyla gerçekleşir.\n\n"
            "- **Histopatolojik Odak (Villit):** Asendan enfeksiyon zarları (korioamnionit) tutarken, transplasental enfeksiyonlar doğrudan koryon villuslarının parankimini ve stroma dokusunu tutar (**villit** veya **villitis**). Villus stromasında mononükleer hücre infiltrasyonu (lenfositler, plazma hücreleri ve histiyositler) izlenir.\n"
            "- **İntervillöz Aralık vs Villus:** Patojen maternal dolaşım yoluyla intervillöz aralıktan geçer ve sinsityotrofoblast bariyerini aşarak villus çekirdeğine girer. Burada nekroz, skleroz ve fetal kapiller obliterasyonu oluşturarak fetal beslenmeyi bozar.\n"
            "- **Etiyoloji:** Transplasental enfeksiyonlar klasik olarak **TORCH grubu ajanlar** (Toksoplazma, Rubella, CMV, Herpes) ve bakteriyel spiroketler (Treponema pallidum) tarafından oluşturulur.\n\n"
            "> [!IMPORTANT]\n"
            "> Asendan enfeksiyonlar membranları (korioamnionit) nötrofillerle tutar; hematojen transplasental enfeksiyonlar ise villusları (villit) lenfohistiyositlerle tutar ve TORCH etkenleriyle oluşur."
        ),
        bullets=[
            "Hematojen enfeksiyonlar maternal kandan transplasental yolla bulaşır",
            "Histolojik olarak villus parankimini tutar; lenfomononükleer villit yapar",
            "Asendan enfeksiyondan farklı olarak zarlar değil koryon villusları tutulur",
            "Klasik olarak TORCH grubu enfeksiyonlar ve sifiliz bu yolla yayılır"
        ],
        elements=[
            make_quiz(
                question="Term bir plasentanın histopatolojik incelemesinde amniyon ve koryon zarlarının tamamen temiz ve salim olduğu, ancak koryon villuslarının stromasında mononükleer lenfosit ve histiyosit infiltrasyonunun (kronik villit) eşlik ettiği fokal villöz nekrozlar saptanıyor. Bu mikroskopik patern öncelikle hangi enfeksiyon mekanizmasını işaret eder?",
                options=[
                    {"key": "A", "text": "Vajinadan yukarıya tırmanan asendan bakteriyel korioamnionit", "isCorrect": False, "explanation": "Asendan yol zarları tutar ve nötrofiliktir; villus mononükleer infiltrasyonu yapmaz."},
                    {"key": "B", "text": "Hematojen yolla bulaşan transplasental enfeksiyon (villit)", "isCorrect": True, "explanation": "Doğru. Zarlar temizken villus parankiminin mononükleer hücrelerle tutulması hematojen (transplasental) yayılımın kesin bulgusudur."},
                    {"key": "C", "text": "İntramural leiomyom dejenerasyonu", "isCorrect": False, "explanation": "Leiomyom uterus myometriumundadır; plasenta villiti yapmaz."},
                    {"key": "D", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Mol hidatiformda avasküler villus ödemi ve trofoblastik hiperplazi olur; villit tablosu değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Maternal kandan transplasental yolla ulaşan patojenlerin koryon villuslarında oluşturduğu mononükleer iltihaba villit denir.",
                masked_term="villit",
                hint="Koryonik villus parankiminin dokusal iltihabı"
            ),
            make_slider(
                left_title="Asendan Plasental Enfeksiyon",
                right_title="Transplasental (Hematojen) Enfeksiyon",
                left_points=[
                    "Doğum kanalından yukarıya doğru yayılır",
                    "Amniyon ve koryon zarları tutulur (korioamnionit)",
                    "Nötrofil lökositler hakimdir; akut pürülan iltihaptır",
                    "Erken membran rüptürü ve prematüre doğuma yol açar"
                ],
                right_points=[
                    "Maternal kan akımıyla intervillöz alana ulaşır",
                    "Doğrudan koryon villus parankimi tutulur (kronik villit)",
                    "Lenfosit, plazma hücresi ve histiyositler hakimdir",
                    "TORCH kompleksi ve intrauterin fetal malformasyonlar yapar"
                ]
            ),
            make_recall(
                question="Bir patoloji raporunda 'akut korioamnionit' yerine 'kronik villitis' tanımı yer alıyorsa, mikrobiyolojik etken arayışı vajinal floraya mı yoksa maternal sistemik enfeksiyonlara (TORCH vb.) mı yönelmelidir?",
                answer="Maternal sistemik ve transplasental TORCH enfeksiyonlarına yönelmelidir; çünkü villit maternal kan yoluyla bulaşır."
            )
        ]
    ))

    # Slide 88
    slides.append(make_slide(
        slide_num=88,
        title="TORCH Kompleksi Patojenleri ve Viral Villit Histolojisi",
        subtitle="CMV intranükleer inklüzyonları, Toksoplazma kistleri ve kalsifikasyon",
        clinical_focus="Virüslerin plasentada bıraktığı karakteristik patolojik parmak izleri",
        narrative=(
            "Transplasental yolla plasentayı aşıp fetüsü enfekte eden mikroorganizmalar klasik olarak **TORCH kompleksi** (Toxoplasma, Others/Syphilis, Rubella, Cytomegalovirus, Herpes simplex) olarak gruplandırılır.\n\n"
            "- **Sitomegalovirüs (CMV) Villiti:** Konjenital enfeksiyonların en sık viral etkenidir. Koryon villus endotelinde ve stromal hücrelerde dev büyüme (sitomegali) ve belirgin **'baykuş gözü' tarzında geniş intranükleer inklüzyon cisimcikleri** oluşturur. Villuslarda yaygın fibrozis ve kalsifikasyon izlenir.\n"
            "- **Toksoplazmozis:** Villus stromasında lenfohistiyositik infiltrasyon ve kist/trofozoit formları izlenir.\n"
            "- **Fetal Sonuçlar:** Bu ajanlar koryon villus bariyerini aşarak fetüste mikrosefali, intrakraniyal kalsifikasyonlar, korioretinit, sensörinöral işitme kaybı ve hepatosplenomegali gibi ağır intrauterin sekellere yol açar.\n\n"
            "> [!NOTE]\n"
            "> Transplasental CMV enfeksiyonunda koryon villuslarında dev hücreler ve baykuş gözü intranükleer inklüzyonları ile yaygın kalsifikasyon izlenir."
        ),
        bullets=[
            "Transplasental enfeksiyonların başında TORCH kompleksi patojenleri gelir",
            "CMV: En sık viral ajandır; koryon villuslarında baykuş gözü inklüzyonları yapar",
            "Villöz endotel ve stromada devleşme, fibrozis ve kalsifikasyon oluşturur",
            "Fetüste mikrosefali, korioretinit ve intrakraniyal kalsifikasyon yapar"
        ],
        elements=[
            make_quiz(
                question="İntrauterin gelişme geriliği ve mikrosefali ile doğan bir bebeğin plasenta incelemesinde kronik lenfohistiyositik villit, koryon villus endotel hücrelerinde belirgin sitomegali ve nükleus içinde geniş bazofilik 'baykuş gözü' inklüzyon cisimcikleri saptanıyor. En olası viral patojen hangisidir?",
                options=[
                    {"key": "A", "text": "Sitomegalovirüs (CMV)", "isCorrect": True, "explanation": "Doğru. Koryon villuslarında sitomegali ve baykuş gözü intranükleer inklüzyonları CMV enfeksiyonunun patognomonik bulgusudur."},
                    {"key": "B", "text": "Hepatit B virüsü", "isCorrect": False, "explanation": "Hepatit B bu inklüzyonları yapmaz."},
                    {"key": "C", "text": "Kızamık virüsü", "isCorrect": False, "explanation": "Warthin-Finkeldey dev hücreleri yapar."},
                    {"key": "D", "text": "İnsan papilloma virüsü (HPV)", "isCorrect": False, "explanation": "Koilositoz yapar; plasental villit yapmaz."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Transplasental Sitomegalovirüs enfeksiyonunda koryon villus hücrelerinde karakteristik baykuş gözü intranükleer inklüzyonları izlenir.",
                masked_term="baykuş gözü",
                hint="CMV viral nükleer replikasyonunun klasik morfolojik görüntüsü"
            ),
            make_table(
                title="Transplasental TORCH Patojenleri ve Plasenta Bulguları",
                headers=["Patojen Etken", "Karakteristik Plasental Morfoloji", "Fetal Klinik Tablo"],
                rows=[
                    [
                        {"text": "Sitomegalovirüs (CMV)", "isMasked": False},
                        {"text": "Baykuş gözü inklüzyonları ve kalsifikasyon", "isMasked": True, "hint": "Koryon villuslarında dev nükleer morfoloji ve mineral birikimi"},
                        {"text": "Mikrosefali, sağırlık, periventriküler kalsifikasyon", "isMasked": False}
                    ],
                    [
                        {"text": "Toxoplasma gondii", "isMasked": False},
                        {"text": "Kronik villit ve psödokistler", "isMasked": False},
                        {"text": "Hidrosefali, korioretinit, serebral kalsifikasyon", "isMasked": True, "hint": "Klasik intrakraniyal ve oküler konjenital triad"}
                    ]
                ]
            ),
            make_recall(
                question="Transplasental viral villitlerde villusların fibrotik ve kalsifiye hale gelmesi fetus üzerinde doğrudan nasıl bir fizyopatolojik sonuç doğurur?",
                answer="Villusların gaz ve besin değişim yüzeyi azalarak plasental yetmezliğe ve intrauterin gelişme geriliğine (İUGG) yol açar."
            )
        ]
    ))

    # Slide 89
    slides.append(make_slide(
        slide_num=89,
        title="Spesifik Bakteriyel Villitler: Sifiliz ve Listeria Monocytogenes",
        subtitle="Soluk büyük plasenta, endarteritis obliterans ve mikroapseler",
        clinical_focus="Transplasental bakteriyel enfeksiyonların özgün patolojik bulguları",
        narrative=(
            "Bazı özgün bakteriyel patojenler asendan yol yerine maternal kanla transplasental olarak villus parankimine oturur ve kendilerine has lezyonlar üretir.\n\n"
            "- **Konjenital Sifiliz (Treponema pallidum):** Plasenta makroskopik olarak **belirgin derecede büyük, ödemli, ağır ve soluk sarımsı renktedir**. Mikroskopide koryon villusları hidrofik ve immatür kalmıştır; villus damarlarında konsantrik proliferasyon ve daralma (**endarteritis obliterans**) ile plazma hücrelerinden zengin perivasküler infiltrasyon izlenir.\n"
            "- **Listeria Monocytogenes Villiti:** Anneye kontamine süt veya et ürünlerinden bulaşan Listeria, plasentada hematolojik yayılımla **yaygın granülomatöz villit ve akut mikroapseler** oluşturur. Villusların içinde ve intervillöz alanda makrofajlar ve nötrofillerden oluşan mikroapse odakları görülmesi Listeria için oldukça karakteristiktir; erken intrauterin fetal ölüme ve düşüklere yol açar.\n\n"
            "> [!IMPORTANT]\n"
            "> Konjenital sifilizde dev, soluk, ödemli plasenta ve endarteritis obliterans görülür; Listeria enfeksiyonunda ise villuslarda karakteristik mikroapseler izlenir."
        ),
        bullets=[
            "Sifiliz: Plasenta devasa, ödemli, soluk ve ağırdır; villuslar immatür kalır",
            "Sifiliz histolojisinde villus damarlarında endarteritis obliterans tipiktir",
            "Listeria: Transplasental hematojen yolla villuslarda akut mikroapseler yapar",
            "Listeria enfeksiyonu maternal gıda kontaminasyonu sonrası intrauterin fetal kayıp yapar"
        ],
        elements=[
            make_quiz(
                question="İntrauterin fetal kayıp sonrası incelenen plasentanın normalden iki kat daha ağır, hidropik, soluk renkli olduğu; mikroskopik kesitlerinde ise koryon villus damarlarının çevresinde plazma hücreleri ve belirgin konsantrik intimal kalınlaşma (endarteritis obliterans) izlendiği olguda öncelikle hangi maternal enfeksiyon düşünülmelidir?",
                options=[
                    {"key": "A", "text": "Ureaplasma urealyticum asendan enfeksiyonu", "isCorrect": False, "explanation": "Ureaplasma zarlarda korioamnionit yapar; soluk dev plasenta ve endarterit yapmaz."},
                    {"key": "B", "text": "Treponema pallidum (Konjenital Sifiliz)", "isCorrect": True, "explanation": "Doğru. Büyük, ödemli, soluk plasenta ve villus damarlarında endarteritis obliterans sifilizin klasik histopatolojisidir."},
                    {"key": "C", "text": "Maternal leiomyom basısı", "isCorrect": False, "explanation": "Miyom plasental endarterit yapmaz."},
                    {"key": "D", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Mol hidatiformda villus damarları tamamen yoktur (avaskülerdir)."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Konjenital sifiliz enfeksiyonunda plasenta koryon villus damarlarında konsantrik lümen daralmasıyla karakterize endarteritis obliterans izlenir.",
                masked_term="endarteritis obliterans",
                hint="Damar iç tabakasının kalınlaşarak damar lümenini tıkaması tablosu"
            ),
            make_slider(
                left_title="Konjenital Sifiliz Plasentası",
                right_title="Listeria Monocytogenes Plasentası",
                left_points=[
                    "Plasenta normalden çok daha büyük, ağır, hidropik ve soluktur",
                    "Villus damarlarında endarteritis obliterans ve plazma hücreleri izlenir",
                    "Spiroketler gümüşleme boyaları (Warthin-Starry) ile gösterilebilir"
                ],
                right_points=[
                    "Villus parankiminde ve intervillöz alanda çok sayıda mikroapseler izlenir",
                    "Nötrofil ve makrofaj odakları granülomatöz villit manzarası verir",
                    "Pastörize edilmemiş süt/peynir tüketimi sonrası akut bakteriyemiyle gelişir"
                ]
            ),
            make_recall(
                question="Gebelikte çiğ süt veya taze peynir tüketimi sonrası ateş ve sepsis gelişen bir annede plasentada mikroapseler görülmesi hangi bakteriyi işaret eder?",
                answer="Listeria monocytogenes bakterisini işaret eder; gram pozitif basildir ve plasentada mikroapseli granülomatöz villit yapar."
            )
        ]
    ))

    # Slide 90 - Checkpoint 9
    slides.append(make_slide(
        slide_num=90,
        title="[TEKRAR SAYFASI - CHECKPOINT 9] Plasenta Patolojisi ve İntrauterin Enfeksiyonlar",
        subtitle="Bölüm 9 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Kordon anomalileri, korioamnionit, funisit, FİRS, villit, CMV ve sifiliz sentezi",
        narrative=(
            "Bu tekrar sayfası, 81-89. adımlarda incelenen Umbilikal Kord Morfolojisi ve Plasental Enfeksiyonlar ünitesini konsolide etmek amacıyla hazırlanmıştır.\n\n"
            "- **Kordon Anomalileri:** Battledore kordon plasenta marjinine yapışır. Velamentöz insersiyonda damarlar zarlar arasında korumasız çıplaktır (vasa previa riski). Tek umbilikal arter (TUA) renal/kardiyak malformasyon riskini gösterir.\n"
            "- **Membran Metaplazisi:** Kord girişinde amniyonda skuamöz metaplazi sık ve selimdir.\n"
            "- **Asendan vs Hematojen Enfeksiyonlar:** Asendan yol en sıktır; zarlarda korioamnionit ve kordonda funisit (fetal nötrofiller) yapar; FİRS üzerinden İnterlökin-6 ile periventriküler lökomalazi ve serebral palsi riskini artırır. Hematojen yol ise villusları tutarak villit yapar (TORCH grubu).\n"
            "- **Spesifik Patojenler:** CMV baykuş gözü inklüzyonları ve kalsifikasyon yapar; Sifiliz soluk dev plasenta ve endarteritis obliterans ile seyreder; Listeria ise villöz mikroapseler üretir.\n\n"
            "> [!NOTE]\n"
            "> Asendan enfeksiyon korioamnionit (nötrofil) yapar; hematojen enfeksiyon villit (TORCH) yapar; funisitteki lökositler fetüse aittir; sifilizde endarteritis obliterans izlenir."
        ),
        bullets=[
            "Battledore: Marjinal giriş; Velamentöz: Zarlar arasında çıplak damarlar",
            "Kord girişinde amniyonda skuamöz metaplazi sık görülen selim bir bulgudur",
            "Asendan korioamnionit erken doğumun en sık sebebidir; funisit fetal lökosit içerir",
            "FİRS: Kordon kanında IL-6 yükselir; periventriküler lökomalazi ve serebral palsi riski doğurur",
            "CMV baykuş gözü inklüzyonu; Sifiliz endarteritis obliterans; Listeria mikroapse yapar"
        ],
        elements=[
            make_quiz(
                question="Plasenta patolojisi ve intrauterin enfeksiyonlarla ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Umbilikal kordon damarlarındaki nötrofilik vaskülitte (funisit) damar duvarını infiltre eden lökositler anne kanından gelir.", "isCorrect": False, "explanation": "Yanlış. Kordon damarları tamamen fetal dolaşıma aittir; lökositler fetal kökenlidir."},
                    {"key": "B", "text": "Asendan enfeksiyonlar koryon villuslarında izole kronik mononükleer villite yol açar.", "isCorrect": False, "explanation": "Yanlış. Asendan enfeksiyonlar zarlarda akut nötrofilik korioamnionit yapar; villit hematojen yoldur."},
                    {"key": "C", "text": "Velamentöz kord insersiyonunda çıplak damarların yırtılması fetüs için dakikalar içinde ölümcül masif hipovolemik şok tablosu doğurur.", "isCorrect": True, "explanation": "Doğru. Korunmasız fetal damarlar yırtıldığında kan kaybeden doğrudan fetüstür ve hızla kaybedilir."},
                    {"key": "D", "text": "Konjenital sifilizde koryon villuslarında nötrofilik mikroapseler ve baykuş gözü inklüzyonları patognomoniktir.", "isCorrect": False, "explanation": "Yanlış. Mikroapseler Listeria'ya, inklüzyonlar CMV'ye aittir; sifilizde endarteritis obliterans görülür."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Asendan korioamnionit tablosunda kordon kanında yükselen İnterlökin-6 sitokini fetal beyinde periventriküler lökomalazi ve serebral palsi riskini artırır.",
                masked_term="periventriküler lökomalazi",
                hint="Fetal beyin dokusunda sitokin ilişkili nörolojik beyaz cevher hasarı"
            ),
            make_table(
                title="Bölüm 9 Plasenta Enfeksiyonları ve Ayırıcı Tanı Özeti",
                headers=["Enfeksiyon Yolu / Antite", "Primer Tutulan Bölge", "Karakteristik Patoloji / Patojen"],
                rows=[
                    [
                        {"text": "Asendan Enfeksiyon", "isMasked": False},
                        {"text": "Amniyon ve koryon zarları", "isMasked": True, "hint": "Fetal keseyi çevreleyen dış ve iç kılıflar"},
                        {"text": "Akut korioamnionit (nötrofilik); vajinal flora", "isMasked": False}
                    ],
                    [
                        {"text": "Transplasental Hematojen", "isMasked": False},
                        {"text": "Koryon villus stroması", "isMasked": True, "hint": "Plasental villöz ağaç parankimi"},
                        {"text": "Kronik villit; TORCH, CMV (baykuş gözü), Sifiliz", "isMasked": False}
                    ],
                    [
                        {"text": "Listeria Monocytogenes", "isMasked": False},
                        {"text": "Villus içi ve intervillöz alan", "isMasked": False},
                        {"text": "Akut mikroapseler ve granülomatöz villit", "isMasked": True, "hint": "Nötrofil ve makrofaj içeren fokal cerahat odakları"}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 9 Kontrol Önermeleri",
                items=[
                    {"text": "Kordonda 2 arter yerine tek umbilikal arter saptanması fetal konjenital anomali riskini artırır.", "isLie": False, "explanation": "Doğru. %20-30 renal ve kardiyak defekt eşlik eder."},
                    {"text": "Kord girişinde amniyonda izlenen skuamöz metaplazi sık rastlanan selim bir matürasyon bulgusudur.", "isLie": False, "explanation": "Doğru. Malign öncülü değildir."},
                    {"text": "Transplasental sifiliz enfeksiyonunda plasenta aşırı derecede küçülüp atrofik kalsifiye bir taş haline gelir.", "isLie": True, "explanation": "Tuzak! Konjenital sifilizde plasenta tam tersine normalden iki kat büyük, ağır, soluk ve hidropiktir; damarlarda endarteritis obliterans görülür."},
                    {"text": "Kordon vaskülitindeki (funisit) nötrofil lökositler bizzat fetüsün kendi bağışıklık sistemine aittir.", "isLie": False, "explanation": "Doğru. Kordon damarları fetal kan taşır."}
                ]
            ),
            make_recall(
                question="Checkpoint 9: Asendan korioamnionit ile transplasental enfeksiyonların histopatolojik tutulum yeri ve baskın inflamatuar hücre tipi açısından temel farkı nedir?",
                answer="Asendan enfeksiyon zarları (koryoamnion) tutar ve akut nötrofil lökositler hakimdir; transplasental enfeksiyon ise doğrudan koryon villuslarını (villit) tutar ve mononükleer lenfosit/histiyositler hakimdir."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=9
    ))

    return slides
