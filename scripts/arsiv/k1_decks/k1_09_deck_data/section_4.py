"""
Akut Enflamasyon (Ders 9) - Bölüm 4: Vasküler Olaylar I: Vazodilatasyon ve Akım Dinamikleri
Slayt 31 - 40 (Checkpoint 4: Slayt 39)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "slideNumber": 31,
        "title": "Vasküler Yanıtın İlk Saniyeleri: Geçici Vazokonstriksiyon",
        "subtitle": "Mekanik travma anında nörojenik refleks ve endotelin aracılı koruyucu damar büzüşmesi",
        "badge": "Vasküler Başlangıç",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Doku mekanik bir travmaya (kesik, darbe) veya kimyasal bir hasara maruz kaldığında damarların "
            "verdiği ilk hemodinamik tepki genişleme değil; şaşırtıcı şekilde son derece kısa süreli bir "
            "**Geçici Vazokonstriksiyondur**.\n\n"
            "- Hasar anında sempatik otonom sinir uçları uyarılır; prekapiller arteriyol düz kasları aniden kasılır.\n"
            "- Bu vazokonstriksiyon sadece **birkaç saniye ile birkaç dakika** sürer.\n"
            "- Temel amacı; zedelenen damardan ilk anda olabilecek masif kan kaybını mekanik olarak kısıtlamak ve "
            "kanamayı frenlemektir.\n\n"
            "> [KLİNİK GÖZLEM] Deriye sert bir cisimle çizik atıldığında saniyeler içinde beliren beyaz çizgi "
            "(lokal solukluk), bu geçici vazokonstriksiyonun klinik kanıtıdır. Ancak bu faz çok geçicidir ve yerini "
            "hemen kalıcı vazodilatasyona bırakır."
        ),
        "medicalTerms": [
            {"term": "Geçici Vazokonstriksiyon", "explanation": "Travma anında arteriyollerin sempatik refleks ve lokal endotelin ile saniyeler süren koruyucu büzülmesidir."},
            {"term": "Beyaz Çizgi Reaksiyonu", "explanation": "Mekanik uyarandan hemen sonra arteriyol büzüşmesine bağlı deride beliren geçici solukluktur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hasar anında damarların İLK yanıtı birkaç saniye süren geçici vazokonstriksiyondur.",
            "📌 [SINAV SPOTU] Geçici vazokonstriksiyon sempatik nörojenik refleksle yönetilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İlk Tepki", "desc": "Saniyeler süren koruyucu arteriyoler daralma.", "isKey": True},
                {"title": "Mekanizma", "desc": "Sempatik akson refleksi ve düz kas spazmı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Akut doku hasarında arteriyollerin verdiği ilk ve saniyeler süren geçici vasküler yanıt geçici vazokonstriksiyon fazıdır.",
                "vazokonstriksiyon",
                "Damar lümeninin sempatik refleksle kısa süreli daralmasını ifade eden terim"
            ),
            make_active_recall(
                "Deriye künt bir cisimle sertçe çizik atıldığında ilk saniyelerde beliren beyaz çizginin (solukluk) fizyopatolojik mekanizması nedir?",
                "Hasar anında sempatik nörojenik refleksle prekapiller arteriyollerin aniden kasılması ve mikrodolaşıma kan girişinin saniyeler boyunca durmasıdır (geçici vazokonstriksiyon)."
            )
        ]
    })

    # Slide 32
    slides.append({
        "slideNumber": 32,
        "title": "Arteriyoler Vazodilatasyon: Akut Enflamasyonun Temel Vasküler Belirteci",
        "subtitle": "Prekapiller arteriyollerin gevşemesi, kapiller yatakların açılması ve hiperemi dalgası",
        "badge": "Hemodinami",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Geçici vazokonstriksiyonu takip eden ve akut enflamasyonun en belirgin vasküler manifestasyonu olan "
            "evre **Arteriyoler Vazodilatasyondur**.\n\n"
            "- Öncelikle hasar odağını besleyen prekapiller arteriyoller genişler.\n"
            "- Ardından daha önce kapalı duran yeni kapiller yataklar (mikrosirkülasyon üniteleri) birbiri ardına perfüzyona açılır.\n"
            "- Hasarlı dokuya birim zamanda ulaşan kan hacmi 10 kata kadar artar; bu duruma **enflamatuvar aktif hiperemi** denir.\n"
            "- Arteriyoler genişleme, Celsus'un tarif ettiği **Rubor (Kızarıklık)** ve **Calor (Sıcaklık)** bulgularının "
            "asıl mimarıdır.\n\n"
            "> Vazodilatasyon hasarın şiddetine göre saatler veya günler boyunca kesintisiz devam edebilir."
        ),
        "medicalTerms": [
            {"term": "Arteriyoler Vazodilatasyon", "explanation": "Prekapiller arteriyol düz kaslarının gevşeyerek lümen çapını artırması ve kapiller yatağa kan hücum ettirmesidir."},
            {"term": "Kapiller Açılma", "explanation": "İstirahat halinde kan geçmeyen prekapiller sfinkterlerin gevşeyerek tüm mikrovasküler ağı aktif dolaşıma katmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun en erken ve en kalıcı vasküler değişikliği arteriyoler vazodilatasyondur.",
            "📌 [SINAV SPOTU] Vazodilatasyon kapiller hidrostatik basıncı artırarak ödem sıvısının damar dışına itilmesini kolaylaştırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lümen Genişlemesi", "desc": "Arteriyol düz kasları gevşeyerek kan akımını katlar.", "isKey": True},
                {"title": "Klinik Yansıma", "desc": "Doku kırmızıya boyanır (rubor) ve ısınır (calor).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Geçici Vazokonstriksiyon vs Arteriyoler Vazodilatasyon",
                "Geçici Vazokonstriksiyon (İlk saniyeler)",
                "Arteriyoller büzülür, kan akımı duraklar, hasarlı doku soluk ve beyaz görünür.",
                "Arteriyoler Vazodilatasyon (Sonraki saatler)",
                "Prekapiller sfinkterler tamamen açılır, kapiller yatak kanla dolar, doku parlak kırmızı (rubor) ve sıcak (calor) olur."
            ),
            make_cloze(
                "Akut enflamasyonda hasarlı bölgedeki kapiller yatakların kanla dolup taşmasına neden olan vasküler olay arteriyoler vazodilatasyon olayıdır.",
                "vazodilatasyon",
                "Damar lümeninin genişleyerek aktif hiperemi oluşturması"
            )
        ]
    })

    # Slide 33
    slides.append({
        "slideNumber": 33,
        "title": "Vazodilatasyonun Kimyasal Mediyatörleri: Histamin ve Nitrik Oksit",
        "subtitle": "H1 reseptör uyarımı, endotelyal eNOS aktivasyonu ve düz kasta cGMP artışı",
        "badge": "Vazomotor Biyokimya",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Arteriyollerin genişlemesi pasif bir süreç değildir; güçlü kimyasal mediyatörlerin düz kas hücrelerini "
            "gevşetmesiyle yürütülür:\n\n"
            "1. **Histamin:** Perivasküler mast hücreleri mekanik travma veya kompleman (C3a, C5a) uyarısıyla dakikalar "
            "içinde granüllerini boşaltır. Histamin, damar düz kasındaki **H1 reseptörlerine** bağlanarak çok hızlı bir "
            "vazodilatasyon dalgası başlatır.\n\n"
            "2. **Nitrik Oksit (NO):** Hasarlı bölgedeki endotel hücreleri kalsiyum akışıyla **eNOS (endotelyal NO sentaz)** "
            "enzimini aktive eder. L-argininden üretilen serbest gaz halindeki NO, komşu düz kas hücresine difüze olur.\n"
            "3. NO, düz kasta **çözünür guanilat siklazı** uyararak **cGMP** düzeyini yükseltir; kalsiyum sitozolden "
            "uzaklaştırılır ve damar düz kası gevşer."
        ),
        "medicalTerms": [
            {"term": "H1 Reseptörü", "explanation": "Damar endotelinde ve düz kasında yer alan, histamin bağlandığında vazodilatasyon ve geçirgenlik artıran G-protein kenetli reseptördür."},
            {"term": "cGMP (Siklik GMP)", "explanation": "Nitrik oksit uyarımıyla düz kasta artarak miyozin hafif zincir fosfatazını aktive eden ve gevşeme sağlayan ikinci habercidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Akut enflamasyonun en hızlı etki gösteren vazodilatatör mediyatörü HİSTAMİN'dir.",
            "📌 [SINAV SPOTU] Nitrik Oksit (NO) guanilat siklaz ve cGMP yolağı üzerinden vasküler düz kas gevşemesi sağlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Histamin", "desc": "Mast hücresinden dakikalar içinde boşalıp H1 reseptörünü uyarır.", "isKey": True},
                {"title": "Nitrik Oksit", "desc": "eNOS kaynaklı NO gazı cGMP artışı ile düz kası gevşetir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Nitrik Oksit Aracılı Vazodilatasyon Kaskadı",
                [
                    "1. Enflamatuvar mediyatörler endotel hücresinde sitozolik kalsiyum konsantrasyonunu artırır",
                    "2. Kalsiyum-kalmodulin kompleksi endotelyal nitrik oksit sentaz (eNOS) enzimini aktive eder",
                    "3. L-argininden sentezlenen gaz halindeki NO komşu vasküler düz kas hücresine difüze olur",
                    "4. NO çözünür guanilat siklazı aktive ederek hücresel cGMP düzeyini fırlatır",
                    "5. cGMP hücre içi serbest kalsiyumu düşürerek düz kası gevşetir ve arteriyoler vazodilatasyon gelişir"
                ]
            ),
            make_micro_quiz(
                "Akut enflamasyonda endotel kaynaklı Nitrik Oksitin (NO) damar düz kasını gevşeterek vazodilatasyon yapmasında rol oynayan hücre içi ikinci haberci molekül hangisidir?",
                {
                    "A": "Siklik AMP (cAMP)",
                    "B": "Siklik GMP (cGMP)",
                    "C": "İnozitol trifosfat (IP3)",
                    "D": "Diaçilgliserol (DAG)",
                    "E": "Tirozin kinaz"
                },
                "B",
                {
                    "A": "cAMP adenilat siklaz kaynaklıdır.",
                    "B": "Doğru cevap B'dir: NO çözünür guanilat siklazı uyararak GTP'den cGMP sentezletir; cGMP kalsiyumu düşürerek gevşeme sağlar.",
                    "C": "IP3 kalsiyum salar, kasılma yapar.",
                    "D": "DAG protein kinaz C'yi uyarır.",
                    "E": "Tirozin kinaz büyüme faktörü reseptörüdür."
                }
            )
        ]
    })

    # Slide 34
    slides.append({
        "slideNumber": 34,
        "title": "Lewis'in Üçlü Yanıtı (Triple Response of Lewis)",
        "subtitle": "Kırmızı çizgi, alev dalgası (flare) ve kabarcık (wheal): Deneysel enflamasyon modeli",
        "badge": "Klasik Fizyoloji",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "İngiliz kardiyolog Sir Thomas Lewis (1927), insan derisine künt bir iğne ucuyla sert bir çizik atıldığında "
            "gelişen mikrovasküler olayları **Üçlü Yanıt (Triple Response)** olarak tanımlamıştır:\n\n"
            "1. **Kırmızı Çizgi (Red Line):** Çizikten 3-10 saniye sonra tam çizik hattında beliren ince kırmızı çizgi. "
            "Lokal histamin salınımı ve doğrudan kapiller dilatasyonu yansıtır.\n"
            "2. **Alev Dalgası (Flare / Kızarıklık Halesi):** Birkaç dakika içinde kırmızı çizginin etrafına doğru genişleyen, "
            "düzensiz sınırlı parlak kırmızı hale. Akson refleksi aracılığıyla komşu prekapiller arteriyollerin vazodilatasyonudur.\n"
            "3. **Kabarcık (Wheal / Ödem Plakı):** Çizik hattının ortasında 3-5 dakika içinde şişen, kabarık, soluk beyazımsı "
            "ödem alanı. Artmış vasküler geçirgenlikle plazma eksüdasının deriyi kabartmasıdır.\n\n"
            "> Bu model ürtiker (kurdeşen) patolojisinin minyatür bir laboratuvar kopyasıdır."
        ),
        "medicalTerms": [
            {"term": "Triple Response", "explanation": "Deriye mekanik çizik atıldığında sırasıyla kırmızı çizgi, alev dalgası ve kabarcık oluşması triadıdır."},
            {"term": "Akson Refleksi", "explanation": "Duyusal sinir ucundan kalkan uyarının merkezi sinir sistemine gitmeksizin yan dallar yoluyla komşu arteriyollere antidromik vazodilatasyon taşımasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lewis'in üçlü yanıtı: Kırmızı çizgi (kapiller dilatasyon) -> Alev/Flare (akson refleksi ile arteriyol dilatasyonu) -> Kabarcık/Wheal (ödem eksüdasyonu).",
            "📌 [SINAV SPOTU] Wheal (kabarcık) mikrovasküler geçirgenlik artışının doğrudan sonucudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1. Kırmızı Çizgi", "desc": "Doğrudan lokal kapiller dilatasyon.", "isKey": True},
                {"title": "2. Flare (Alev)", "desc": "Akson refleksiyle yayılan arteriyoler hiperemi.", "isKey": True},
                {"title": "3. Wheal (Kabarcık)", "desc": "Artmış venüler geçirgenlikle oluşan eksüda ödemi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Lewis Üçlü Yanıt Bileşeni", "Klinik Görünüm", "Altta Yatan Hemodinamik Mekanizma"],
                [
                    [("1. Kırmızı Çizgi (Red Line)", False, ""), ("Çizik hattında ince kırmızı çizgi", False, ""), ("Lokal histamin salınımıyla doğrudan kapiller dilatasyon", True, "Hasar hattındaki ilk mikrovasküler genişleme")],
                    [("2. Alev Dalgası (Flare)", False, ""), ("Çevrede düzensiz parlak kırmızı hale", False, ""), ("Duyusal akson refleksi aracılı komşu arteriyol dilatasyonu", True, "Sinir dalları üzerinden yayılan genişleme")],
                    [("3. Kabarcık (Wheal)", False, ""), ("Ortada kabarık, gergin ödem plağı", False, ""), ("Venüler geçirgenlik artışı sonucu lokalize eksüda birikimi", True, "Dokuya sızan proteinli plazma kabarması")]
                ]
            ),
            make_cloze(
                "Lewis'in üçlü yanıtında çizik hattında beliren kabarcık (wheal) lezyonunun oluşumundan sorumlu temel olay artmış mikrovasküler geçirgenlik sonucudur.",
                "geçirgenlik",
                "Damar duvarından dokuya protein ve sıvı sızmasını sağlayan vasküler değişim"
            )
        ]
    })

    # Slide 35
    slides.append({
        "slideNumber": 35,
        "title": "Mikrodolaşımda Kan Akımının Yavaşlaması ve Staz Gelişimi",
        "subtitle": "Sıvı kaybıyla kanın vizkozitesinin artması, eritrosit yoğunlaşması ve akımın durma noktasına gelmesi",
        "badge": "Hemoreoloji",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Vazodilatasyon ilk başladığında kan akımı çok hızlıdır; ancak dakikalar ilerledikçe dramatik bir "
            "hemodinamik değişim yaşanır ve kan akımı giderek yavaşlar; bu duruma **Staz** denir.\n\n"
            "Stazın basamakları:\n"
            "1. Endotel aralıklarından dışarı sürekli protein ve su (eksüda) kaçar.\n"
            "2. Damar lümeni içindeki sıvı hızla tükenirken şekilli elemanlar (eritrositler) damar içinde hapsolur.\n"
            "3. Kanın lümen içi hematokrit değeri ve vizkozitesi (koyuluğu/ağdalılığı) kat kat artar (hemokonsantrasyon).\n"
            "4. Postkapiller venüllerde eritrositler birbirine yapışarak rulo (rouleaux) oluşturur ve lümeni tıkaç gibi doldurur.\n"
            "5. Kan akım hızı neredeyse durma noktasına geriler (staz)."
        ),
        "medicalTerms": [
            {"term": "Staz", "explanation": "Mikrosirkülasyonda sıvı kaybı ve vizkozite artışına bağlı olarak kan akım hızının ileri derecede yavaşlaması veya durmasıdır."},
            {"term": "Hemokonsantrasyon", "explanation": "Plazma sıvısının dokuya kaçması sonucu damar içi eritrosit yoğunluğunun aşırı artmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Staz gelişimi sıvı eksüdasyonuna bağlı hemokonsantrasyon ve artmış kan vizkozitesinin sonucudur.",
            "📌 [SINAV SPOTU] Kan akımının yavaşlaması (staz), lökositlerin damar duvarına yanaşması (marginasyon) için zorunlu fiziksel ön koşuldur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sıvı Kaçağı", "desc": "Plazma dokuya sızdıkça damar içi kan koyulaşır.", "isKey": True},
                {"title": "Vizkozite Artışı", "desc": "Eritrosit yığılması kan akım hızını sıfıra yaklaştırır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Akut Enflamasyonda Staz Gelişim Zinciri",
                [
                    "1. Postkapiller venüllerde vasküler geçirgenlik artar ve protein zengini plazma sıvısı dokuya sızar",
                    "2. Damar içi sıvı hacmi azalırken eritrositler lümende yoğunlaşır (hemokonsantrasyon)",
                    "3. Kanın vizkozitesi (akış direnci) aşırı yükselir ve eritrositler rulo dizilimi oluşturur",
                    "4. Mikrodolaşımda kan akımı dramatik şekilde yavaşlar ve vasküler staz tablosu oturur"
                ]
            ),
            make_active_recall(
                "Akut enflamasyonda kan akımının yavaşlamasının (staz) lökositlerin savunma görevini yerine getirebilmesi açısından en kritik avantajı nedir?",
                "Hızlı laminer akımda damarın merkezinde sürüklenen lökositlerin kenara, endotel yüzeyine savrulmasına (marginasyon) ve endotelle temas ederek tutunmasına olanak sağlamasıdır."
            )
        ]
    })

    # Slide 36
    slides.append({
        "slideNumber": 36,
        "title": "Aksiyal Akımdan Marginasyona Geçiş: Lökositlerin Kenara İtilmesi",
        "subtitle": "Laminer akım fiziği, reolojik itilme kuvvetleri ve lökosit-endotel buluşması",
        "badge": "Biyofizik",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Normal fizyolojik koşullarda kan damarlarında **Laminer Akım** kuralları geçerlidir:\n\n"
            "- Daha ağır ve büyük olan şekilli elemanlar (eritrositler ve lökositler) damar lümeninin en ortasında, "
            "en hızlı akan **aksiyal akım sütununda** seyahat ederler.\n"
            "- Damar duvarına (endotele) temas eden periferik tabakada ise sadece hücresiz, berrak bir plazma kılıfı akar; "
            "böylece lökositlerin endotele sürtünmesi ve gereksiz yere aktive olması önlenir.\n\n"
            "> **Enflamasyonda Reolojik Dönüşüm:**\n"
            "Staz gelişip akım yavaşladığında eritrositler birbirine yapışarak büyük rulo agregatları kurar. "
            "Bu dev eritrosit kümeleri damar merkezini doldurarak daha hafif olan lökositleri fiziksel olarak "
            "lümenin kenarına, endotel çeperine doğru iter. Bu periferik yer değiştirmeye **Marginasyon** denir."
        ),
        "medicalTerms": [
            {"term": "Aksiyal Akım", "explanation": "Laminer akımda kan hücrelerinin damar merkez ekseninde yoğunlaşarak akmasıdır."},
            {"term": "Marginasyon", "explanation": "Staz sonucu kan hücrelerinin merkezden damar çeperine itilerek endotel yüzeyine dizilmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Normalde lökositler merkezdeki aksiyal sütunda akar; staz onları çepere iterek marginasyona yol açar.",
            "📌 [SINAV SPOTU] Eritrosit agregatları (rulo) lökositleri mekanik olarak endotel yüzeyine süpürür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Normal Laminer Akım", "desc": "Hücreler ortada akar, endotelde sadece plazma kılıfı vardır.", "isKey": True},
                {"title": "Marginasyon", "desc": "Stazla birlikte lökositler endotel duvarına yaslanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Normal Aksiyal Akım vs Enflamatuvar Marginasyon",
                "Normal Aksiyal Akım",
                "Lökositler damar merkezindeki hızlı akım sütununda ilerler, endotel ile temas sıfırdır, plazma kılıfı korur.",
                "Enflamatuvar Marginasyon",
                "Kan akımı duraklar, eritrosit agregatları lökositleri çepere iter, lökositler endotel yüzeyine dizilir."
            ),
            make_cloze(
                "Kan akımının yavaşlaması sonucu lökositlerin damarın merkez ekseninden çeperine doğru itilerek endotel yüzeyine yaklaşmasına marginasyon adı verilir.",
                "marginasyon",
                "Lökositlerin adezyon öncesi damar kenarına dizilmesini ifade eden morfolojik terim"
            )
        ]
    })

    # Slide 37
    slides.append({
        "slideNumber": 37,
        "title": "Postkapiller Venüller: Vasküler Yanıtın Anatomik Odak Noktası",
        "subtitle": "Neden kapiller veya arteriyoller değil de venüller sızıntı ve lökosit göçünün merkezidir?",
        "badge": "Mikrovasküler Anatomi",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Tıp öğrencilerinin en çok merak ettiği sorulardan biri şudur: Enflamatuvar geçirgenlik artışı ve lökosit göçü "
            "neden kapillerlerde veya arteriyollerde değil de spesifik olarak **Postkapiller Venüllerde** gerçekleşir?\n\n"
            "Bunun üç temel anatomik ve fizyolojik nedeni vardır:\n"
            "1. **En Yüksek Reseptör Yoğunluğu:** Histamin (H1), bradikinin ve lökotrien reseptörleri en yoğun şekilde "
            "postkapiller venül endotelinde kümelenmiştir.\n"
            "2. **Düşük Kesme Gerilimi (Shear Stress):** Venüllerde kan akım hızı ve duvar sürtünme basıncı arteriyollere "
            "göre çok düşüktür; bu sayede lökositler akıntıya kapılıp sürüklenmeden endotel yüzeyine tutunabilir.\n"
            "3. **Gevşek İnterendotelyal Bağlantılar:** Venül endotelleri arasındaki bağlantı kompleksleri (junctions) "
            "arteriyollere göre çok daha esnek ve kasılmaya müsaittir."
        ),
        "medicalTerms": [
            {"term": "Postkapiller Venül", "explanation": "Kapiller yatağın hemen çıkışında yer alan, enflamatuvar eksüdasyon ve lökosit ekstravazasyonunun primer anatomik sahası olan damardır."},
            {"term": "Kesme Gerilimi (Shear Stress)", "explanation": "Akan kanın damar endoteli üzerine uyguladığı teğetsel sürtünme kuvvetidir; lökosit adezyonunu zorlaştırır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Histamin aracılı endotel kasılması ve lökosit transmigrasyonu primer olarak POSTKAPİLLER VENÜLLERDE gerçekleşir.",
            "📌 [SINAV SPOTU] Düşük akım hızı ve yüksek reseptör yoğunluğu postkapiller venülleri ideal göç sahası yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Reseptör Zenginliği", "desc": "Histamin ve bradikinin reseptörleri en çok venüldedir.", "isKey": True},
                {"title": "Düşük Sürtünme", "desc": "Düşük shear stress lökositlerin tutunmasını kolaylaştırır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Damar Segmenti", "Kan Akım Hızı / Basınç", "Enflamasyondaki Baskın Görevi"],
                [
                    [("Prekapiller Arteriyol", False, ""), ("Yüksek basınç ve yüksek hız", False, ""), ("Vazodilatasyon yaparak dokuya gelen toplam kan hacmini artırmak", True, "Aktif hiperemiyi yöneten düzenleyici segment")],
                    [("Kapiller Yatak", False, ""), ("Geniş yüzey alanı, orta hız", False, ""), ("Besin ve gaz alışverişi; ağır hasarda doğrudan nekrozla sızıntı", True, "Mikrosirkülasyonun en yaygın kılcal ağı")],
                    [("Postkapiller Venül", False, ""), ("En düşük hız ve en düşük shear stress", False, ""), ("Endotel kasılmasıyla eksüda sızdırmak ve lökositleri dokuya geçirmek", True, "Enflamatuvar kaçak ve göçün ana meydanı")]
                ]
            ),
            make_active_recall(
                "Akut enflasyonda mast hücrelerinden salınan histaminin endotel hücrelerini kasarak sıvı sızdırmasına yol açtığı primer mikrovasküler damar segmenti hangisidir?",
                "Postkapiller venüllerdir; çünkü histamin reseptörleri en yoğun bu segmentte bulunur ve interendotelyal bağlantılar ayrışmaya en müsaittir."
            )
        ]
    })

    # Slide 38
    slides.append({
        "slideNumber": 38,
        "title": "Vasküler Yanıtın Zamansal Fazları: Erken vs Uzamış Yanıt",
        "subtitle": "Histaminin dakikalar süren ani geçici fazı ve sitokinlerin saatler süren gecikmiş fazı",
        "badge": "Zaman Çizelgesi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Vasküler hemodinami hasarın şiddetine göre iki farklı zamansal patern çizer:\n\n"
            "1. **Ani Geçici Yanıt (Immediate Transient Response):**\n"
            "- Hafif hasarlarda (yüzeyel çizik, hafif yanık) görülür.\n"
            "- Hasardan hemen sonra başlar, 15-30 dakikada zirve yapar ve 1 saat içinde söner.\n"
            "- Yalnızca **histamin, bradikinin ve lökotrienlerin** postkapiller venüllerde yaptığı endotel kasılmasına bağlıdır.\n\n"
            "2. **Gecikmiş Uzamış Yanıt (Delayed Prolonged Response):**\n"
            "- Güneş yanığı (UV hasarı), termal yanıklar, radyasyon veya bakteriyel toksinlerde görülür.\n"
            "- Hasardan **2 ila 12 saat sonra** başlar, 24 saat veya günlerce sürer.\n"
            "- Hem endotelin doğrudan nekrozu (yanık) hem de TNF ve IL-1'in endotel iskeletini genetik olarak "
            "yeniden düzenlemesiyle (sitotoksik retraksiyon) şekillenir; hem venülleri hem kapillerleri tutar."
        ),
        "medicalTerms": [
            {"term": "Ani Geçici Yanıt", "explanation": "Histamin gibi hazır mediyatörlerle başlayan ve 15-30 dakikada sönen erken faz venüler sızıntıdır."},
            {"term": "Gecikmiş Uzamış Yanıt", "explanation": "Güneş yanığında olduğu gibi saatler sonra başlayıp günlerce süren direkt endotel nekrozu ve sitokin aracılı hasardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ani geçici yanıt sadece postkapiller venüllerde olur ve histaminle yürütülür.",
            "📌 [SINAV SPOTU] Güneş yanığı gecikmiş uzamış yanıta klasik örnektir (saatler sonra kızarıklık ve bül gelişir)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Ani Faz", "desc": "Histaminle 15-30 dakikada başlayıp biten venüler sızıntı.", "isKey": True},
                {"title": "Gecikmiş Faz", "desc": "Güneş yanığında saatler sonra başlayan kapiller ve venüler yıkım.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Ani Geçici Yanıt vs Gecikmiş Uzamış Yanıt",
                "Ani Geçici Yanıt (Hafif Travma)",
                "Dakikalar içinde başlar, 30 dakikada söner, sadece venülleri tutar, histamin aracılıdır.",
                "Gecikmiş Uzamış Yanıt (Güneş Yanığı)",
                "2-12 saat sonra başlar, günlerce sürer, kapiller ve venülleri tutar, direkt endotel hasarı ve sitokinlerle yürür."
            ),
            make_micro_quiz(
                "Plajda güneşlendikten 4 saat sonra deride kızarıklık, sıcaklık artışı ve ertesi gün su kabarcıkları (bül) gelişen bir tatilcideki vasküler yanıt paterni hangisidir?",
                {
                    "A": "Ani geçici yanıt (Immediate transient)",
                    "B": "Gecikmiş uzamış yanıt (Delayed prolonged)",
                    "C": "Saf nörojenik vazokonstriksiyon",
                    "D": "Kronik granülomatöz hiperemi",
                    "E": "Akut kapiller tromboz"
                },
                "B",
                {
                    "A": "Ani geçici yanıt 15-30 dakikada söner.",
                    "B": "Doğru cevap B'dir: UV radyasyonu kaynaklı güneş yanığı tipik bir gecikmiş uzamış yanıt örneğidir; saatler sonra başlar ve günlerce sürer.",
                    "C": "Vazokonstriksiyon saniyeler sürer.",
                    "D": "Granülom aylar sürer.",
                    "E": "Tromboz infarkt yapar."
                }
            )
        ]
    })

    # Slide 39 (CHECKPOINT 4)
    slides.append({
        "slideNumber": 39,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Vasküler Yanıt ve Akım Dinamikleri",
        "subtitle": "Bölüm 4 Vazokonstriksiyon, Arteriyoler Dilatasyon, NO/Histamin, Lewis Üçlüsü ve Staz",
        "badge": "Checkpoint 4",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Dördüncü kontrol noktasında vasküler olayların hemodinamik haritasını özetliyoruz:\n\n"
            "1. **İlk Yanıt:** Sempatik refleksle saniyeler süren **geçici vazokonstriksiyon** (beyaz çizgi).\n"
            "2. **Arteriyoler Vazodilatasyon:** Prekapiller arteriyollerin gevşemesi ve kapillerlerin açılmasıyla **aktif hiperemi**; "
            "Rubor ve Calor'un temelidir.\n"
            "3. **Mediyatörler:** Mast hücresi kaynaklı **Histamin (H1)** ve endotel kaynaklı **Nitrik Oksit (NO / cGMP)** düz kası gevşetir.\n"
            "4. **Lewis Üçlü Yanıtı:** Kırmızı çizgi (kapiller dilatasyon) -> Alev/Flare (akson refleksiyle arteriyol dilatasyonu) -> "
            "Kabarcık/Wheal (venüler geçirgenlikle ödem).\n"
            "5. **Staz ve Marginasyon:** Sıvı kaçağıyla kan koyulaşır (hemokonsantrasyon), vizkozite artar, akım yavaşlar (staz); "
            "eritrosit agregatları lökositleri damar çeperine iter (marginasyon).\n"
            "6. **Postkapiller Venüller:** Düşük shear stress ve bol histamin reseptörüyle lökosit göçü ve sızıntının merkez üssüdür."
        ),
        "medicalTerms": [
            {"term": "Vasküler Yatak", "explanation": "Arteriyol, kapiller ve venüllerden oluşan fonksiyonel mikrodolaşım ağıdır."},
            {"term": "Hemodinamik Kaskad", "explanation": "Damar çapı, kan akım hızı ve vizkozitesinin hasar sonrası sırayla değiştiği fiziksel süreçtir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Damarın ilk yanıtı geçici vazokonstriksiyondur; ancak en belirgin ve uzun yanıt arteriyoler vazodilatasyondur.",
            "📌 [SINAV SPOTU] Staz kan vizkozitesinin artmasıyla olur ve lökositlerin marginasyonuna zemin hazırlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemodinami", "desc": "Vazokonstriksiyon -> Vazodilatasyon -> Hiperemi -> Staz.", "isKey": True},
                {"title": "Reoloji", "desc": "Hemokonsantrasyon lökositleri çepere iter (marginasyon).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Akut enflamasyon gelişen bir dokuda mikrodolaşımda kan akımının başlangıçtaki hızlanmasının ardından giderek yavaşlayarak durma noktasına gelmesinin (staz) iki temel nedeni nedir?",
                "1) Mikrovasküler geçirgenlik artışı nedeniyle protein ve sıvı kaybı (hemokonsantrasyon), 2) Hematokrit ve kan vizkozitesinin aşırı yükselerek eritrositlerin rulo agregatları oluşturmasıdır."
            ),
            make_cloze(
                "Lewis'in üçlü yanıtında akson refleksi aracılığıyla komşu prekapiller arteriyollerin genişlemesi sonucu oluşan kızarıklık halesine alev dalgası adı verilir.",
                "alev dalgası",
                "İngilizce flare olarak adlandırılan yaygın eritematöz parlak kırmızı alan"
            ),
            make_before_after(
                "İstirahat Postkapiller Venülü vs Enflamatuvar Postkapiller Venül",
                "İstirahat Postkapiller Venülü",
                "Endotel hücreleri sıkıca kenetlidir, lümen geniştir, kan hücreleri merkezde hızla akar, sızıntı yoktur.",
                "Enflamatuvar Postkapiller Venül",
                "Endotel kasılmıştır, porlar açılmıştır, plazma dokuya fışkırır, akım duraklamış (staz) ve lökositler çepere yapışmıştır."
            )
        ]
    })

    # Slide 40
    slides.append({
        "slideNumber": 40,
        "title": "Bölüm 4 Entegrasyonu: Şok ve Sepsiste Vazodilatasyon Felaketi",
        "subtitle": "Lokal koruyucu hiperemiden sistemik kollapsa uzanan patolojik köprü",
        "badge": "Kritik Bakım",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Vasküler değişikliklerin lokal dokudaki amacı savunma hücrelerini taşımaktır. Ancak bu yanıt kontrolsüzce "
            "tüm vücuda yayıldığında letal bir felakete dönüşür: **Septik Şok**.\n\n"
            "- Kana karışan Gram-negatif bakteri endotoksini (LPS), tüm vücuttaki monosit ve makrofajları uyarır.\n"
            "- Masif **TNF ve IL-1** salınımı, damar endotelinde ve düz kasında indüklenebilir nitrik oksit sentaz "
            "(**iNOS**) ekspresyonunu patlatır.\n"
            "- Milyarlarca damarda eşzamanlı ve kontrolsüz **masif vazodilatasyon** gelişir; sistemik vasküler rezistans (SVR) çöker.\n"
            "- Eşlik eden yaygın kapiller kaçak nedeniyle damar içi sıvı interstisyuma boşalır; santral venöz basınç sıfırlanır.\n"
            "- Sıvı resüsitasyonuna ve vazopressörlere yanıt vermeyen **distribütif şok ve çoklu organ yetmezliği (MODS)** tablosu oturur."
        ),
        "medicalTerms": [
            {"term": "iNOS (İndüklenebilir NO Sentaz)", "explanation": "İnflamatuvar sitokinlerle aktive olan ve eNOS'tan kat kat daha yüksek miktarda toksik NO üreten enzimdir."},
            {"term": "Distribütif Şok", "explanation": "Damar tonusunun yaygın kaybı ve kapiller kaçak sonucu kanın periferde göllenmesiyle oluşan şok tipidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Septik şoktaki masif hipotansiyon ve dirençli vazodilatasyonun temel sorumlusu sitokinlerle indüklenen iNOS aktivasyonudur.",
            "📌 [SINAV SPOTU] Septik şok patolojik olarak 'sistemik akut enflamasyon' sendromudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "iNOS İndüksiyonu", "desc": "TNF ve IL-1 ile kontrolsüz nitrik oksit üretimi.", "isKey": True},
                {"title": "Dolaşım Çöküşü", "desc": "Sistemik vazodilatasyon ve kapiller kaçak ile letal şok.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Septik şokta sistemik masif vazodilatasyon ve dirençli hipotansiyona yol açan aşırı nitrik oksit üretiminden sorumlu enzim iNOS enzimidir.",
                "iNOS",
                "İndüklenebilir nitrik oksit sentaz enziminin kısaltması"
            ),
            make_active_recall(
                "Lokal enflamasyonda hayat kurtarıcı olan vazodilatasyon ve geçirgenlik artışının septik şokta ölümcül olmasının hemodinamik nedeni nedir?",
                "Yanıtın lokal bir dokuyla sınırlı kalmayıp tüm vücut damar yatağına yayılması, sistemik vasküler rezistansın (SVR) çökmesi ve plazmanın tüm dokulara kaçarak efektif dolaşım kan hacmini sıfırlamasıdır."
            )
        ]
    })

    return slides
