"""
Akut Enflamasyon (Ders 9) - Bölüm 7: Lökosit Marginasyonu, Yuvarlanma ve Sıkı Adezyon
Slayt 61 - 70 (Checkpoint 7: Slayt 69)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "slideNumber": 61,
        "title": "Lökositlerin Göreve Alımı (Recruitment): Adım Adım Kaskad",
        "subtitle": "Kandan dokuya uzanan dört aşamalı yolculuk: Marginasyon, Yuvarlanma, Adezyon ve Diapedez",
        "badge": "Lökosit Trafiği",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Akut enflamasyonun en kritik dönüm noktası, savunmanın ana savaşçıları olan lökositlerin (özellikle "
            "nötrofillerin) damar lümeninden çıkarak hasarlı doku interstisyumuna ulaşmasıdır.\n\n"
            "Bu süreç rastgele veya pasif bir sızma değildir; endotel ile lökosit arasında son derece hassas "
            "bir moleküler diyalogla yürütülen **dört sıralı aşamadan** oluşur:\n\n"
            "1. **Marginasyon (Lümende Kenara İtilme):** Staz nedeniyle lökositlerin merkezden çepere savrulması.\n"
            "2. **Yuvarlanma (Rolling):** Selektinler aracılığıyla zayıf, geçici bağlar kurulması ve hücrenin frenlenmesi.\n"
            "3. **Sıkı Adezyon (Firm Adhesion):** İntegrinlerin aktive olmasıyla lökositin endotel yüzeyine kilitlenip durması.\n"
            "4. **Transmigrasyon (Diapedez):** PECAM-1 (CD31) rehberliğinde endotel aralığından ve bazal membrandan dokuya geçiş."
        ),
        "medicalTerms": [
            {"term": "Lökosit Ekstravazasyonu", "explanation": "Beyaz kan hücrelerinin dolaşım sisteminden ayrılarak doku interstisyumuna göç etmesi sürecinin tamamıdır."},
            {"term": "Adezyon Kaskadı", "explanation": "Lökositin selektinlerle yuvarlanıp integrinlerle durdurulduğu moleküler etkileşimler dizisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ekstravazasyonun sıralı evreleri: Marginasyon -> Yuvarlanma (Rolling) -> Sıkı Adezyon -> Diapedez'dir.",
            "📌 [SINAV SPOTU] Yuvarlanmayı selektinler, sıkı tutunmayı ise integrinler yönetir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dörtlü Kaskad", "desc": "Marginasyon -> Yuvarlanma -> Sıkı Adezyon -> Diapedez.", "isKey": True},
                {"title": "Moleküler Rol Dağılımı", "desc": "Zayıf bağlar selektinlerle, güçlü kilit integrinlerle kurulur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Lökosit Göç Kaskadının Sıralı Evreleri",
                [
                    "1. Staz ve eritrosit agregasyonu nötrofilleri damar lümeni çeperine iter (Marginasyon)",
                    "2. Selektinler ile Sialyl-Lewis X arasında zayıf bağlar kurulup koparak lökosit frenlenir (Yuvarlanma)",
                    "3. Kemokinler integrinleri yüksek afiniteli konformasyona sokarak ICAM-1'e kilitler (Sıkı Adezyon)",
                    "4. Nötrofil PECAM-1 (CD31) aracılığıyla endotel kavşağından geçip bazal membranı deler (Diapedez)"
                ]
            ),
            make_cloze(
                "Lökositlerin damar lümeninden doku aralığına göç etmesi sürecinde endotel yüzeyine sımsıkı kenetlenmelerini sağlayan adezyon molekülü ailesi integrinler ailesidir.",
                "integrinler",
                "LFA-1 ve Mac-1 gibi heterodimerik transmembran adezyon reseptörleri"
            )
        ]
    })

    # Slide 62
    slides.append({
        "slideNumber": 62,
        "title": "Selektin Ailesi ve Yuvarlanma (Rolling) Biyolojisi",
        "subtitle": "Kalsiyum bağımlı lektinler: Hızlı akan kanda lökosite ilk freni yaptıran zayıf bağlar",
        "badge": "Selektinler",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Lökositler normalde kanda saniyede binlerce mikrometre hızla akar. Onları aniden durdurmaya çalışmak "
            "hücrenin parçalanmasına yol açardı. Bu nedenle doğa **Selektinler** adı verilen 'yumuşak frenleme' "
            "sistemini geliştirmiştir.\n\n"
            "Selektinler, hücre yüzeyindeki sialillenmiş oligosakkaritleri (özellikle **Sialyl-Lewis X**) kalsiyum bağımlı "
            "olarak bağlayan transmembran glikoproteinlerdir. Bu bağlar son derece zayıftır ve milisaniyeler içinde "
            "kopar. Kan akımının itici gücüyle lökosit endotel üzerinde dönerek yuvarlanır (**Rolling**); tıpkı rüzgarda "
            "sürüklenen bir çalı kümesi gibi.\n\n"
            "Selektin ailesinin üç üyesi vardır:\n"
            "- **L-Selektin (CD62L):** Lökositlerin üzerinde yerleşik bulunur.\n"
            "- **E-Selektin (CD62E):** Enflame endotel hücresinde sitokinlerle üretilir.\n"
            "- **P-Selektin (CD62P):** Trombositlerde ve endotel granüllerinde depolanır."
        ),
        "medicalTerms": [
            {"term": "Selektin", "explanation": "Damar endoteli, lökosit ve trombositlerde bulunan, karbonhidrat ligandlarına bağlanarak yuvarlanma sağlayan lektin ailesidir."},
            {"term": "Sialyl-Lewis X", "explanation": "Lökosit glikoproteinlerinin ucunda bulunan ve selektinlerin tanıdığı tetrasakkarit karbonhidrat yapısıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yuvarlanma (rolling) fazından sorumlu molekül ailesi SELEKTİNLER'dir.",
            "📌 [SINAV SPOTU] Selektinlerin bağlandığı lökosit yüzey ligandı Sialyl-Lewis X'tir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Zayıf Bağlar", "desc": "Sürekli kopup kurulan bağlarla lökosit yavaşlatılır.", "isKey": True},
                {"title": "L, E, P Üyeleri", "desc": "L lökositte, E endotelde, P granüllerde ve trombositte bulunur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Selektin Tipi", "Hücresel Yerleşimi", "Temel Ligandı ve Biyolojik Özelliği"],
                [
                    [("L-Selektin (CD62L)", False, ""), ("Nötrofil, Monosit ve T lenfositler", False, ""), ("Endoteldeki GlyCAM-1 ve CD34; adezyon sonrası hücreden dökülür", True, "Lökositin kendi üzerinde taşıdığı selektin türü")],
                    [("E-Selektin (CD62E)", False, ""), ("Yalnızca Enflame Damar Endoteli", False, ""), ("Lökositteki Sialyl-Lewis X; TNF ve IL-1 ile 1-2 saatte sentezlenir", True, "Sitokin uyarımıyla de novo gen transkripsiyonu")],
                    [("P-Selektin (CD62P)", False, ""), ("Endotel Weibel-Palade ve Trombositler", False, ""), ("Lökositteki PSGL-1; Histamin ve trombinle dakikalar içinde dışa vurulur", True, "Granüllerde hazır depolanan en hızlı selektin")]
                ]
            ),
            make_cloze(
                "Lökositlerin endotel üzerindeki yuvarlanma hareketinde selektin moleküllerinin bağlandığı özgül karbonhidrat yapısına Sialyl-Lewis X adı verilir.",
                "Sialyl-Lewis X",
                "Selektinlerin tanıdığı fruktoz içeren karakteristik tetrasakkarit ligandı"
            )
        ]
    })

    # Slide 63
    slides.append({
        "slideNumber": 63,
        "title": "P-Selektin ve Weibel-Palade Cisimcikleri: Yıldırım Hızında Dışavurum",
        "subtitle": "Histamin ve trombin ile dakikalar içinde hücre zarına füzyon olan sekretuvar granüller",
        "badge": "Endotel Sırları",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "E-selektin sentezlenmek için sitokin uyarımı ve saatler süren gen transkripsiyonuna ihtiyaç duyarken, "
            "**P-Selektin** acil durumlar için endotel hücresinde önceden paketlenmiş olarak bekletilir:\n\n"
            "- Endotel hücrelerinin sitoplazmasında **Weibel-Palade cisimcikleri** adı verilen özel çubuksu organeller vardır.\n"
            "- Bu organellerin içinde iki kritik molekül hazır depolanır: **P-Selektin** ve hemostaz proteini olan "
            "**von Willebrand Faktörü (vWF)**.\n\n"
            "> **Yıldırım Yanıtı:**\n"
            "Hasar anında mast hücresinden salınan **Histamin** veya pıhtılaşmadan gelen **Trombin**, endoteli uyardığında; "
            "Weibel-Palade cisimcikleri **dakikalar (1-5 dakika)** içinde plazma zarıyla kaynaşır (ekzositoz).\n"
            "P-selektin anında damar lümenine döşenir ve geçen nötrofilleri saniyeler içinde yakalamaya başlar."
        ),
        "medicalTerms": [
            {"term": "Weibel-Palade Cisimciği", "explanation": "Endotel hücrelerinde P-selektin ve von Willebrand faktörünü depolayan karakteristik elektron-mikroskobik granüllerdir."},
            {"term": "vWF (von Willebrand Faktörü)", "explanation": "Trombositlerin subendotelyal kollojene yapışmasını sağlayan multimerik plazma proteinidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Weibel-Palade cisimciklerinde depolanan iki molekül: P-SELEKTİN ve von Willebrand Faktörüdür (vWF).",
            "📌 [SINAV SPOTU] P-selektin histamin veya trombin uyarısıyla DAKİKALAR içinde yüzeye çıkar (transkripsiyon gerekmez).",
            "📌 [SINAV SPOTU] E-selektin ise depolanmaz; TNF ve IL-1 ile saatler içinde sıfırdan sentezlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Weibel-Palade İkili", "desc": "P-selektin + vWF hazır depolanır.", "isKey": True},
                {"title": "Hız Farkı", "desc": "P-selektin dakikalar içinde, E-selektin 1-2 saatte yüzeye çıkar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "P-Selektin vs E-Selektin Aktivasyon Dinamiği",
                "P-Selektin (Weibel-Palade)",
                "Hazır depolanmıştır; histamin ve trombinle dakikalar içinde plazma zarına eksozitozla çıkar; yeni protein sentezi gerekmez.",
                "E-Selektin (De Novo Sentez)",
                "Depolanmaz; TNF ve IL-1 uyarımıyla mRNA transkripsiyonu yapılır; yüzeye çıkması 1-2 saat sürer."
            ),
            make_micro_quiz(
                "Endotel hücrelerinde Weibel-Palade cisimcikleri içinde depolanan ve histamin uyarısıyla dakikalar içinde hücre yüzeyine taşınan iki temel molekül hangisinde birlikte verilmiştir?",
                {
                    "A": "P-selektin ve von Willebrand faktörü (vWF)",
                    "B": "E-selektin ve Fibrinojen",
                    "C": "ICAM-1 ve Doku faktörü",
                    "D": "PECAM-1 ve İnterlökin-8",
                    "E": "L-selektin ve Tromboksan A2"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Weibel-Palade cisimcikleri spesifik olarak P-selektin ve vWF depolar.",
                    "B": "E-selektin depolanmaz, yeni sentezlenir.",
                    "C": "ICAM-1 sitokinlerle indüklenir.",
                    "D": "PECAM-1 hücreler arası bağlantıdadır.",
                    "E": "L-selektin lökosittedir."
                }
            )
        ]
    })

    # Slide 64
    slides.append({
        "slideNumber": 64,
        "title": "İntegrin Ailesi ve Sıkı Adezyon (Firm Adhesion) Kilitlenmesi",
        "subtitle": "LFA-1, Mac-1 ve VLA-4: Düşük afiniteli katlanmış formdan yüksek afiniteli dik forma geçiş",
        "badge": "İntegrin Kilitlenmesi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Yuvarlanma lökositi yavaşlatır ancak durduramaz. Lökositin akıntıya karşı koyup endotel üzerinde "
            "taş gibi çakılı kalmasını sağlayan sistem **İntegrinlerdir**.\n\n"
            "- İntegrinler lökosit yüzeyinde bulunan alfa ve beta polipeptid zincirlerinden oluşmuş heterodimerik reseptörlerdir:\n"
            "  * **LFA-1 (CD11a/CD18):** Nötrofil ve lenfositlerde bulunur.\n"
            "  * **Mac-1 (CD11b/CD18):** Nötrofil ve monositlerde bulunur.\n"
            "  * **VLA-4 (alfa4beta1 / CD49d/CD29):** Eozinofil, monosit ve lenfositlerde bulunur.\n\n"
            "> **Konformasyonel Aktivasyon (İçten Dışa Sinyal):**\n"
            "Normalde kanda dolaşan lökositin integrinleri bükülmüş, düşük afiniteli (inaktif) durumdadır. "
            "Yuvarlanan lökosit endotel yüzeyinde proteoglikanlara bağlı duran **Kemokinlerle (örneğin CXCL8 / IL-8)** temas eder. "
            "Kemokin reseptörü hücre içine sinyal gönderir; integrinler aniden dikleşir, uzar ve **yüksek afiniteli kancaya** dönüşür."
        ),
        "medicalTerms": [
            {"term": "İntegrin", "explanation": "Hücre-hücre ve hücre-matriks bağlantısını sağlayan alfa ve beta zincirli transmembran adhezyon glikoproteinleridir."},
            {"term": "Yüksek Afiniteli Konformasyon", "explanation": "Kemokin uyarımıyla integrin baş bölgesinin açılarak endotel ligandlarını sımsıkı bağlayacak gergin forma geçmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sıkı tutunmayı (firm adhesion) yöneten moleküller İNTEGRİNLER ve endoteldeki ligandlarıdır.",
            "📌 [SINAV SPOTU] İntegrinlerin düşük afinite halinden yüksek afinite haline geçişini KEMOKİNLER tetikler.",
            "📌 [SINAV SPOTU] LFA-1 ve Mac-1'in ortak beta zinciri CD18'dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Heterodimer Yapı", "desc": "Alfa ve beta zincirleri (CD11/CD18) birleşerek çalışır.", "isKey": True},
                {"title": "Kemokin Tetikleyici", "desc": "CXCL8 temasıyla integrinler dikleşip kenetlenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "İnaktif İntegrin vs Yüksek Afiniteli Aktif İntegrin",
                "İnaktif İntegrin (Düşük Afinite)",
                "Lökosit serbest akarken molekül bükülmüş ve katlanmıştır, endotel ligandlarına bağlanamaz.",
                "Aktif İntegrin (Yüksek Afinite)",
                "Kemokin uyarımıyla molekül dikleşir, bağlanma cepleri açılır, endoteldeki ICAM-1'e mengene gibi kenetlenir."
            ),
            make_cloze(
                "Lökosit yüzeyindeki integrinlerin bükülmüş inaktif formdan dikleşerek yüksek afiniteli adezyon kancalarına dönüşmesini sağlayan kimyasal mediyatörler kemokinler ailesidir.",
                "kemokinler",
                "Endotel yüzeyinde lökositleri aktive eden kemotaktik sitokin grubu"
            )
        ]
    })

    # Slide 65
    slides.append({
        "slideNumber": 65,
        "title": "Endotelyal İntegrin Ligandları: ICAM-1 ve VCAM-1",
        "subtitle": "İmmünglobülin süperailesi üyeleri ve TNF/IL-1 sitokinleri ile güçlü indüksiyon",
        "badge": "Endotel Ligandları",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Lökositin integrin kancalarının damar duvarında tutunacağı karşı moleküller **İmmünglobülin Süperailesi (IgSF)** "
            "üyeleridir:\n\n"
            "1. **ICAM-1 (İntrasellüler Adezyon Molekülü-1 / CD54):**\n"
            "- Endotel hücresinde eksprese edilir.\n"
            "- Lökosit üzerindeki **LFA-1 (CD11a/CD18)** ve **Mac-1 (CD11b/CD18)** integrinlerini sımsıkı bağlar.\n"
            "- İstirahat endotelinde bazal düzeyde vardır; ancak dokudan gelen **TNF-α ve IL-1** uyarısıyla "
            "birkaç saat içinde ekspresyonu tavan yapar.\n\n"
            "2. **VCAM-1 (Vasküler Hücre Adezyon Molekülü-1 / CD106):**\n"
            "- Endotel hücresinde sitokinlerle indüklenir.\n"
            "- Eozinofil, monosit ve lenfositlerdeki **VLA-4 (alfa4beta1)** integrinini bağlar.\n"
            "- Not: Nötrofillerde VLA-4 bulunmaz; bu nedenle VCAM-1 nötrofil tutunmasında değil, eozinofil/monosit/lenfosit "
            "tutunmasında görev alır."
        ),
        "medicalTerms": [
            {"term": "ICAM-1 (CD54)", "explanation": "Endotelde yer alan ve nötrofil LFA-1/Mac-1 integrinlerini bağlayan immünglobülin süperailesi adezyon reseptörüdür."},
            {"term": "VCAM-1 (CD106)", "explanation": "Endotelde yer alan ve eozinofil/monosit VLA-4 integrinini bağlayan adezyon molekülüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] LFA-1 ve Mac-1'in endoteldeki ligandı ICAM-1'dir.",
            "📌 [SINAV SPOTU] VLA-4'ün endoteldeki ligandı VCAM-1'dir.",
            "📌 [SINAV SPOTU] TNF ve IL-1 endotelde hem E-selektin hem ICAM-1 ve VCAM-1 genlerini açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "ICAM-1", "desc": "Nötrofilleri durduran LFA-1 ve Mac-1 ligandı.", "isKey": True},
                {"title": "VCAM-1", "desc": "Eozinofil ve monositleri durduran VLA-4 ligandı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Lökosit İntegrini", "Bulunduğu Lökosit Tipi", "Endoteldeki Karşı Ligandı (IgSF)"],
                [
                    [("LFA-1 (CD11a/CD18)", False, ""), ("Nötrofil, Monosit ve Lenfositler", False, ""), ("ICAM-1 (CD54)", True, "Nötrofillerin sıkı tutunmasını sağlayan anahtar endotel reseptörü")],
                    [("Mac-1 (CD11b/CD18)", False, ""), ("Nötrofil ve Monositler", False, ""), ("ICAM-1 (CD54)", True, "Hem adezyon hem kompleman C3b fagositozu yapan integrin")],
                    [("VLA-4 (alfa4beta1)", False, ""), ("Eozinofil, Monosit ve Lenfositler", False, ""), ("VCAM-1 (CD106)", True, "Alerjik ve kronik yangıda eozinofil/lenfosit tutunma ligandı")]
                ]
            ),
            make_micro_quiz(
                "Akut enflamasyon gelişen bir dokuda polimorfonükleer nötrofillerin endotel yüzeyine sıkıca kilitlenmesini sağlayan LFA-1 integrininin endotel üzerindeki karşı ligandı hangisidir?",
                {
                    "A": "ICAM-1 (CD54)",
                    "B": "VCAM-1 (CD106)",
                    "C": "PECAM-1 (CD31)",
                    "D": "P-selektin glikoprotein ligandı-1 (PSGL-1)",
                    "E": "Fibronektin"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Nötrofil LFA-1 ve Mac-1 integrinleri endoteldeki ICAM-1'e bağlanarak sıkı adezyon sağlar.",
                    "B": "VCAM-1 eozinofil ve monosit VLA-4 ligandıdır.",
                    "C": "PECAM-1 diapedezdedir.",
                    "D": "PSGL-1 selektin ligandıdır.",
                    "E": "Fibronektin ekstrasellüler matrikstedir."
                }
            )
        ]
    })

    # Slide 66
    slides.append({
        "slideNumber": 66,
        "title": "Lökosit Adezyon Eksikliği Tip 1 (LAD-1): CD18 İntegrin Mutasyonu",
        "subtitle": "Kanda yüz bin nötrofil varken dokuda sıfır irin: İmmünolojinin en çarpıcı paradoksu",
        "badge": "Genetik İmmün Yetmezlik",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İntegrin biyolojisinin yaşamsal önemini kanıtlayan en dramatik genetik hastalık **Lökosit Adezyon "
            "Eksikliği Tip 1'dir (LAD-1 / Leukocyte Adhesion Deficiency-1)**:\n\n"
            "- **Genetik Kusur:** Otozomal resesif geçişlidir. Beta-2 integrin zincirini kodlayan **ITGB2 (CD18) "
            "geninde mutasyon** vardır.\n"
            "- CD18 sentezlenemediği için ne **LFA-1 (CD11a/CD18)** ne de **Mac-1 (CD11b/CD18)** integrinleri hücre yüzeyinde "
            "fonksiyonel olarak kurulamaz.\n\n"
            "> **Klinik ve Patolojik Tablo (Klasik Sınav Vakası):**\n"
            "1. **Göbek Kordonunun Geç Düşmesi:** Normalde doğumdan sonra kordonu lökositler enzimatik olarak eritip düşürür; "
            "LAD-1'li bebeklerde kordon haftalarca düşmez (omfalit gelişir).\n"
            "2. **Tekrarlayan Bakteriyel Nekrotizan Enfeksiyonlar:** Cilt, diş eti ve mukozalarda derin ülserler çıkar.\n"
            "3. **İrin (Pus) Oluşamaması:** Nötrofiller damar endoteline sıkı tutunup dokuya geçemez. Bu nedenle "
            "**enfeksiyon odaklarında hiç nötrofil ve irin yoktur**.\n"
            "4. **Kanda Masif Lökositoz:** Nötrofiller kemik iliğinde üretilir ama dokuya çıkamadığı için damarda hapsolur "
            "(kanda 50.000 - 100.000/mm3 nötrofil sayılır)."
        ),
        "medicalTerms": [
            {"term": "LAD-1", "explanation": "CD18 (beta-2 integrin) gen mutasyonu sonucu lökositlerin endotel adezyonu yapamaması ve dokuya göç edememesidir."},
            {"term": "Omfalit", "explanation": "Göbek kordonu kökünün nekrotizan bakteriyel enfeksiyonudur; LAD-1'de göbek kordonu geç düşer ve omfalit gelişir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] LAD-1 = CD18 (beta-2 integrin) mutasyonu.",
            "📌 [SINAV SPOTU] LAD-1'in klasik triadı: Göbek kordonunun geç düşmesi + İrinsiz nekrotik yaralar + Kanda aşırı lökositoz.",
            "📌 [SINAV SPOTU] Dokuda nötrofil yoktur çünkü sıkı adezyon yapılamaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "CD18 Eksikliği", "desc": "LFA-1 ve Mac-1 yokluğuyla adezyon felci.", "isKey": True},
                {"title": "İrinsiz Enfeksiyon", "desc": "Kanda 100 bin nötrofil varken dokuda tek bir nötrofil bile bulunamaz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Doğumdan 4 hafta geçmesine rağmen göbek kordonu düşmeyen, perine bölgesinde nekrotik derin ülserleri olan ancak yaralarında hiç irin (pus) saptanmayan bir yenidoğanın kan sayımında 85.000/mm3 lökosit bulunuyor. Bu tablonun moleküler nedeni nedir?",
                [
                    {"text": "ITGB2 (CD18) gen mutasyonu nedeniyle beta-2 integrinlerin sentezlenememesi ve nötrofillerin endotel adezyonunun felç olması (LAD-1)", "isCorrect": True, "feedback": "Kusursuz klinik patoloji teşhisi! Bu tablo LAD-1'in ders kitaplarındaki en saf prezentasyonudur."},
                    {"text": "Kemik iliğinde nötrofil üretimini baskılayan G-CSF reseptör mutasyonu", "isCorrect": False, "feedback": "Kanda 85.000 lökosit vardır, üretimde sorun yoktur."},
                    {"text": "Nötrofillerin fagozom oluşturamamasına yol açan miyeloperoksidaz eksikliği", "isCorrect": False, "feedback": "MPO eksikliğinde göbek kordonu gecikmez ve adezyon normaldir."}
                ]
            ),
            make_cloze(
                "Lökosit Adezyon Eksikliği Tip 1 (LAD-1) hastalığında lökositlerin endotel üzerindeki ICAM-1'e tutunmasını engelleyen temel moleküler defekt CD18 integrin alt biriminin eksikliğidir.",
                "CD18",
                "Beta-2 integrin ailesinin ortak polipeptid zincir numarası"
            )
        ]
    })

    # Slide 67
    slides.append({
        "slideNumber": 67,
        "title": "Lökosit Adezyon Eksikliği Tip 2 (LAD-2): Selektin Ligand Kusuru",
        "subtitle": "Fruktoz taşıyıcı mutasyonu, Sialyl-Lewis X yokluğu ve yuvarlanma (rolling) kusuru",
        "badge": "Karbonhidrat Defekti",
        "badgeColor": "rose",
        "synthesisNarrative": (
            "Lökosit göçünün bir diğer kalıtsal modeli **Lökosit Adezyon Eksikliği Tip 2'dir (LAD-2)**:\n\n"
            "- **Genetik Kusur:** Fruktozu Golgi aygıtına taşıyan GDP-fruktoz transporter proteinini kodlayan "
            "**SLC35C1 geninde mutasyon** vardır.\n"
            "- Hücreler fukozillenmiş karbonhidratları sentezleyemez.\n"
            "- Lökositlerin yüzeyinde selektinlerin bağlandığı **Sialyl-Lewis X (CD15s)** karbonhidrat epitopu üretilemez.\n\n"
            "> **LAD-1 ile LAD-2 Karşılaştırması:**\n"
            "- LAD-1 bir **integrin ve adezyon** kusurudur (CD18 eksikliği).\n"
            "- LAD-2 ise bir **selektin ligandı ve yuvarlanma (rolling)** kusurudur.\n"
            "- LAD-2'de göbek kordonunun düşmesi genellikle gecikmez.\n"
            "- Hastalarda enfeksiyonlara ek olarak **büyüme-gelişme geriliği, dismorfik yüz özellikleri, mental retardasyon "
            "ve Bombay kan grubu fenotipi** (H antijeninde fruktoz olmaması nedeniyle) görülür."
        ),
        "medicalTerms": [
            {"term": "LAD-2", "explanation": "GDP-fruktoz transporter mutasyonu sonucu Sialyl-Lewis X sentezlenememesi ve lökosit yuvarlanmasının bozulmasıdır."},
            {"term": "Bombay Fenotipi", "explanation": "Fukozilasyon kusuru nedeniyle alyuvar yüzeyinde H antijeninin kurulamaması ve kan grubunun sahte 0 görünmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] LAD-1 integrin (CD18) kusurudur; LAD-2 selektin ligandı (Sialyl-Lewis X) kusurudur.",
            "📌 [SINAV SPOTU] LAD-2'de yuvarlanma (rolling) bozuktur; zeka geriliği ve Bombay kan grubu eşlik eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "LAD-1 vs LAD-2", "desc": "LAD-1 sıkı adezyonu, LAD-2 yuvarlanmayı bozar.", "isKey": True},
                {"title": "LAD-2 Kliniği", "desc": "Sialyl-Lewis X yokluğu, zeka geriliği, fukoz metabolizma defekti.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "LAD-1 (İntegrin Kusuru) vs LAD-2 (Selektin Ligand Kusuru)",
                "LAD-1 (CD18 Mutasyonu)",
                "Sıkı adezyon bozuktur; göbek kordonu geç düşer; zeka normaldir; kanda nötrofiller aşırı yüksektir; irin sıfırdır.",
                "LAD-2 (Sialyl-Lewis X Kusuru)",
                "Yuvarlanma bozuktur; kordon gecikmesi nadirdir; mental retardasyon, kısa boy ve Bombay kan grubu eşlik eder."
            ),
            make_cloze(
                "Lökosit Adezyon Eksikliği Tip 2 (LAD-2) hastalığında fukozilasyon defekti nedeniyle lökosit yüzeyinde sentezlenemeyen temel selektin ligandı Sialyl-Lewis X molekülüdür.",
                "Sialyl-Lewis X",
                "LAD-2'de eksik olan fukozlu karbonhidrat adezyon yapısı"
            )
        ]
    })

    # Slide 68
    slides.append({
        "slideNumber": 68,
        "title": "Adezyon Moleküllerinin Tedavide Hedeflenmesi",
        "subtitle": "Natalizumab ve Efalizumab: İntegrin blokajıyla yangıyı damarda durdurmak",
        "badge": "Monoklonal Tedaviler",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Lökosit adezyon mekanizmalarının keşfi, otoimmün hastalıklarda hedefe yönelik biyolojik ilaç devrimini başlatmıştır:\n\n"
            "- **Natalizumab (Anti-VLA-4 Monoklonal Antikoru):**\n"
            "  * Lenfositlerin ve monositlerin yüzeyindeki **VLA-4 (alfa-4 integrin)** molekülünü bloke eder.\n"
            "  * Lenfositlerin kan-beyin bariyeri endotelindeki VCAM-1'e tutunmasını engeller.\n"
            "  * Otoreaktif T hücreleri santral sinir sistemine sızamaz; **Multipl Skleroz (MS)** ve Crohn hastalığında "
            "hastalık alevlenmelerini dramatik olarak durdurur.\n"
            "  * Risk: Beyindeki immün gözetim aşırı baskılandığı için JC virüs reaktivasyonu ve ölümcül Progresif "
            "Multifokal Lökoensefalopati (PML) riski taşır.\n\n"
            "- **Vedolizumab (Anti-alfa4beta7 İntegrin):** Yalnızca bağırsak endotelindeki MAdCAM-1'e tutunmayı engelleyerek "
            "inflamatuvar bağırsak hastalıklarında (Ülseratif Kolit, Crohn) bağırsağa özgü hedefe yönelik tedavi sağlar."
        ),
        "medicalTerms": [
            {"term": "Natalizumab", "explanation": "VLA-4 (alfa-4 integrin) inhibitörü olan ve lenfositlerin beyne ve bağırsağa göçünü durduran monoklonal antikordur."},
            {"term": "PML (Progresif Multifokal Lökoensefalopati)", "explanation": "Natalizumab gibi güçlü integrin inhibitörleriyle beyin immünitesinin çökmesi sonucu JC virüsünün yaptığı demiyelinizan ensefalittir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Natalizumab alfa-4 integrini (VLA-4) bloke ederek lenfositlerin santral sinir sistemine girişini engeller.",
            "📌 [SINAV SPOTU] Vedolizumab bağırsağa özgü alfa4beta7 integrinini bloke eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "VLA-4 Blokajı", "desc": "Natalizumab ile T hücrelerinin beyne girişi durdurulur.", "isKey": True},
                {"title": "Klinik Kullanım", "desc": "Multipl Skleroz ve Crohn hastalığında kanıtlanmış etkinlik.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Biyolojik İlaç", "Hedeflediği Adezyon Molekülü", "Klinik Endikasyonu ve Etki Mekanizması"],
                [
                    [("Natalizumab", False, ""), ("VLA-4 (Alfa-4 İntegrin)", False, ""), ("Multipl Skleroz; otoreaktif T hücrelerinin beyne sızmasını engeller", True, "Kan-beyin bariyeri geçişini durduran monoklonal antikor")],
                    [("Vedolizumab", False, ""), ("Alfa-4 Beta-7 İntegrin", False, ""), ("Ülseratif Kolit; lökositlerin bağırsak duvarına göçünü bloke eder", True, "Gastrointestinal sisteme selektif integrin antagonisti")],
                    [("Efalizumab", False, ""), ("LFA-1 (CD11a alt birimi)", False, ""), ("Psoriasis (sedef); nötrofil ve T hücre adezyonunu durdurur", True, "Kutanöz yangıyı baskılayan integrin inhibitörü")]
                ]
            ),
            make_cloze(
                "Multipl Skleroz tedavisinde lökositlerin VLA-4 integrinini bloke ederek kan-beyin bariyerini aşmasını engelleyen monoklonal antikor Natalizumab ilacıdır.",
                "Natalizumab",
                "Alfa-4 integrin antagonisti olan nöroimmünolojik biyolojik ajan"
            )
        ]
    })

    # Slide 69 (CHECKPOINT 7)
    slides.append({
        "slideNumber": 69,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Lökosit Marginasyonu, Yuvarlanma ve Adezyon",
        "subtitle": "Bölüm 7 Selektinler, Weibel-Palade, İntegrinler, ICAM-1, LAD-1 ve LAD-2 Entegrasyonu",
        "badge": "Checkpoint 7",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Yedinci kontrol noktasında lökosit adhezyon basamaklarını özetliyoruz:\n\n"
            "1. **Marginasyon:** Staz ve eritrosit agregasyonuyla lökositlerin damar merkezinden çepere itilmesi.\n"
            "2. **Yuvarlanma (Rolling):**\n"
            "   - **Selektinler:** L-selektin (lökosit), E-selektin (endotel/sitokinler), P-selektin (Weibel-Palade granülleri/histamin).\n"
            "   - **Ligand:** Karbonhidrat yapısındaki **Sialyl-Lewis X**.\n"
            "3. **Sıkı Adezyon (Firm Adhesion):**\n"
            "   - **İntegrinler:** LFA-1 (CD11a/CD18), Mac-1 (CD11b/CD18), VLA-4 (alfa4beta1). Kemokinlerle yüksek afiniteye geçer.\n"
            "   - **Ligandlar:** Endoteldeki **ICAM-1** ve **VCAM-1**.\n"
            "4. **Kalıtsal Kusurlar:**\n"
            "   - **LAD-1:** CD18 mutasyonu -> Sıkı adezyon yok -> Göbek kordonu geç düşer, kanda aşırı lökositoz, dokuda **sıfır irin**.\n"
            "   - **LAD-2:** Fukozilasyon defekti -> Sialyl-Lewis X yok -> Yuvarlanma yok -> Zeka geriliği, kısa boy, Bombay kan grubu.\n"
            "5. **Tedavi:** Natalizumab (anti-VLA-4) MS'te lökositlerin beyne girişini keser."
        ),
        "medicalTerms": [
            {"term": "Firm Adhesion", "explanation": "Lökosit integrinlerinin endotel ICAM-1'e yüksek afiniteyle kenetlenip hücre hareketini tamamen durdurmasıdır."},
            {"term": "Ligand Çifti", "explanation": "Hücreler arası adhezyonda kilit-anahtar uyumu gösteren karşılıklı iki yüzey molekülüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yuvarlanma = Selektinler; Sıkı Adezyon = İntegrinler.",
            "📌 [SINAV SPOTU] P-selektin Weibel-Palade'de vWF ile depolanır.",
            "📌 [SINAV SPOTU] LAD-1 = CD18 eksikliği (adezyon bozuk, irinsiz yara, kordon geç düşer).",
            "📌 [SINAV SPOTU] LAD-2 = Sialyl-Lewis X eksikliği (yuvarlanma bozuk, Bombay fenotipi)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kaskad Sırası", "desc": "Marginasyon -> Selektin (Yuvarlan) -> İntegrin (Dur).", "isKey": True},
                {"title": "Klinik Genetik", "desc": "LAD-1 (CD18) ve LAD-2 (Sialyl-Lewis X) ders kitabı kusurlarıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Lökosit Adezyon Eksikliği Tip 1 (LAD-1) ile Tip 2 (LAD-2) arasındaki moleküler defekt ve etkilenen ekstravazasyon basamağı farklarını özetleyiniz?",
                "LAD-1'de beta-2 integrin zinciri olan CD18 mutasyona uğramıştır ve 'sıkı adezyon' (firm adhesion) basamağı bozuktur; LAD-2'de ise fukozilasyon kusuru nedeniyle Sialyl-Lewis X ligandı sentezlenemez ve 'yuvarlanma' (rolling) basamağı bozuktur."
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi akut enflamasyonda lökositlerin damar endoteline sıkıca tutunup durmasını (sıkı adezyon) sağlayan primer moleküler etkileşimdir?",
                {
                    "A": "P-selektin ile PSGL-1 etkileşimi",
                    "B": "LFA-1 integrini ile ICAM-1 etkileşimi",
                    "C": "E-selektin ile Sialyl-Lewis X etkileşimi",
                    "D": "PECAM-1 ile PECAM-1 homofilik bağlanması",
                    "E": "L-selektin ile GlyCAM-1 etkileşimi"
                },
                "B",
                {
                    "A": "P-selektin yuvarlanmayı sağlar.",
                    "B": "Doğru cevap B'dir: LFA-1 (ve Mac-1) integrinleri endoteldeki ICAM-1'e bağlanarak lökositi endotel üzerinde kilitler (sıkı adezyon).",
                    "C": "E-selektin yuvarlanmayı sağlar.",
                    "D": "PECAM-1 transmigrasyonu (diapedez) sağlar.",
                    "E": "L-selektin yuvarlanmayı sağlar."
                }
            ),
            make_cloze(
                "Endotel hücrelerinde Weibel-Palade cisimcikleri içinde önceden depolanmış olarak bekleyen ve histaminle dakikalar içinde yüzeye çıkan selektin türü P-selektin türüdür.",
                "P-selektin",
                "Trombositlerde ve endotelde hazır depolanan hızlı selektin"
            )
        ]
    })

    # Slide 70
    slides.append({
        "slideNumber": 70,
        "title": "Bölüm 7 Entegrasyonu: Neden Nötrofiller Önce, Monositler Sonra Gelir?",
        "subtitle": "Kandaki sayısal üstünlük, selektin bağlanma hızı ve adezyon moleküllerinin zamansal ardıllığı",
        "badge": "Hücresel Kinetik",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Akut enflamasyon odağına bakıldığında ilk 6-24 saatte dokunun **nötrofillerle**, 24-48 saatten sonra ise "
            "**monosit ve makrofajlarla** dolduğu görülür. Bu zamansal kinetiğin üç temel patolojik nedeni vardır:\n\n"
            "1. **Sayısal Üstünlük:** Kanda nötrofiller monositlerden çok daha fazladır (dolaşımdaki lökositlerin %60'ı "
            "nötrofil, sadece %5'i monosittir).\n"
            "2. **Hızlı Reseptör Cevabı:** Nötrofillerdeki adezyon molekülleri ve kemokin reseptörleri (CXCR1, CXCR2) "
            "akut sinyallere çok daha süratli konformasyonel yanıt verir.\n"
            "3. **Ömür Farkı ve Takip Eden Dalga:** Nötrofiller dokuda sadece 24-48 saat yaşar ve hızla apoptoza giderler. "
            "Monositler ise dokuya girdikten sonra uzun ömürlü **makrofajlara** dönüşür; ölü nötrofil artıklarını ve "
            "enkazı temizleyerek doku onarımının liderliğini devralırlar."
        ),
        "medicalTerms": [
            {"term": "Hücresel Kinetik", "explanation": "Farklı lökosit tiplerinin enflamasyon alanına geliş sırası, dokuda kalış süresi ve akıbetini inceleyen dinamiktir."},
            {"term": "Monosit-Makrofaj Dönüşümü", "explanation": "Kandaki monositin damar dışına çıkarak dokuda fagositik ve immün düzenleyici olgun makrofaja başkalaşmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun ilk 6-24 saatinde nötrofiller, 24-48 saat sonrasında ise monositler/makrofajlar hakimdir.",
            "📌 [SINAV SPOTU] Nötrofillerin ömrü dokuda 1-2 gündür; hızla apoptoza uğrarlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İlk Dalga (6-24 saat)", "desc": "Nötrofiller kandan hızla hücum eder.", "isKey": True},
                {"title": "İkinci Dalga (24-48 saat)", "desc": "Monositler gelip makrofaja dönüşür ve temizliği devralır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Akut Enflamasyonun 12. Saati vs 48. Saati",
                "Hasarın 12. Saati",
                "Dokuda yoğun nötrofil infiltrasyonu vardır, ödem ve fibrin eksüdası belirgindir, bakteriler fagositozla öldürülmektedir.",
                "Hasarın 48. Saati",
                "Nötrofiller apoptoza gitmiştir, dokuya monositler hakimdir, makrofajlar nekrotik artıkları temizleyip onarımı başlatır."
            ),
            make_cloze(
                "Akut enflamasyon odağında ilk 6-24 saatte nötrofillerin hakimiyetinden sonra 24-48 saat içinde dokuyu devralan mononükleer hücreler monositler hücreleridir.",
                "monositler",
                "Dokuya geçerek makrofaja dönüşen dolaşım lökositleri"
            )
        ]
    })

    return slides
