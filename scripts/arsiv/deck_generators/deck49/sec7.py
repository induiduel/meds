import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec7():
    slides = []

    # Slide 61: İnvaziv Serviks Karsinomu Histolojik Tipleri
    s61_narrative = (
        "İnvaziv serviks karsinomu, atipik epitel hücrelerinin bazal membranı yıkarak servikal stromaya "
        "infiltre olmasıyla karakterize primer malign epitelyal tümördür.\n\n"
        "- **Skuamöz Hücreli Karsinom (SCC):** En sık görülen histolojik tiptir; tüm serviks kanseri "
        "olgularının **yaklaşık %80'ini** tek başına oluşturur.\n"
        "- **Adenokarsinom ve Adenoskuamöz Karsinom:** İkinci sıklıkta izlenen gruptur; endoservikal bezlerden "
        "köken alır ve olguların **yaklaşık %15'ini** kapsar.\n"
        "- **Küçük Hücreli Nöroendokrin Karsinom:** Olguların **<%5'ini** oluşturan, son derece agresif seyirli "
        "nadir histolojik formdur.\n"
        "- **Ortak Etyoloji:** Bu histolojik tiplerin ==tümü yüksek riskli onkojenik HPV tipleri ile ilişkilidir==.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İnvaziv serviks karsinomunun %80'i skuamöz hücreli karsinom, %15'i adenokarsinom/adenoskuamöz karsinom, <%5'i küçük hücreli nöroendokrin karsinomdur; tümü yüksek riskli HPV ile ilişkilidir."
    )
    s61_bullets = [
        "En sık histolojik tip skuamöz hücreli karsinomdur (~%80).",
        "Adenokarsinom ve adenoskuamöz karsinom ~%15 oranında görülür.",
        "Küçük hücreli nöroendokrin karsinom <%5'tir; tümü HPV ile ilişkilidir."
    ]
    s61_elements = [
        make_cloze("İnvaziv serviks karsinomlarının yaklaşık yüzde 80'ini skuamöz hücreli karsinom oluşturur.", "yüzde 80", "Skuamöz karsinomun görülme sıklığı oranı"),
        make_table("İnvaziv Serviks Karsinomu Histolojik Dağılımı", ["Histolojik Tip", "Görülme Oranı", "Köken Epiteli / Özelliği"], [
            {"cells": [{"text": "Skuamöz Hücreli Karsinom", "isMasked": False}, {"text": "~%80", "isMasked": True, "hint": "ezici çoğunluktaki oran"}, {"text": "Çok katlı yassı / metaplastik epitel"}]},
            {"cells": [{"text": "Adenokarsinom / Adenoskuamöz", "isMasked": False}, {"text": "~%15", "isMasked": False}, {"text": "Endoservikal mukus salgılayan bezler", "isMasked": True, "hint": "glandüler kökenli epitel"}]},
            {"cells": [{"text": "Küçük Hücreli Nöroendokrin", "isMasked": False}, {"text": "<%5", "isMasked": True, "hint": "en nadir ve agresif grup"}, {"text": "Nöroendokrin diferansiasyon, kötü prognoz"}]}
        ]),
        make_chain("Histolojik Ayrım Zinciri", [
            "1. Yüksek Riskli HPV Girişi: Virüs hem skuamöz hem bez hücrelerine girer.",
            "2. %80 Skuamöz Kanal: Çoğu olguda ektoservikal/metaplastik hücreler karsinomlaşır.",
            "3. %15 Glandüler Kanal: Endoservikal kleft hücreleri adenokarsinoma evrilir.",
            "4. <%5 Nöroendokrin: Yüksek dereceli küçük hücreli agresif fenotip ortaya çıkar."
        ]),
        make_recall("İnvaziv serviks karsinomunun en sık görülen üç histolojik tipi ve yaklaşık görülme oranları nelerdir?", "Skuamöz hücreli karsinom (~%80), adenokarsinom/adenoskuamöz karsinom (~%15) ve küçük hücreli nöroendokrin karsinomdur (<%5)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İnvaziv Karsinom Tipleri", [
            {"text": "Skuamöz hücreli karsinom tüm olguların yaklaşık %80'ini oluşturur.", "isLie": False, "explanation": "Doğru. En sık görülen formdur."},
            {"text": "Adenokarsinom ve adenoskuamöz karsinom yaklaşık %15 oranındadır.", "isLie": False, "explanation": "Doğru. İkinci sıklıktadır."},
            {"text": "Küçük hücreli nöroendokrin karsinom olguların %99'unu oluşturup tamamen iyi huyludur.", "isLie": True, "explanation": "Tuzak! <%5 oranında görülür ve son derece agresif, kötü prognozludur."},
            {"text": "Tüm bu histolojik tipler yüksek riskli HPV ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Ortak etken HPV'dir."}
        ]),
        make_quiz("İnvaziv serviks karsinomları arasında en sık görülen histolojik tip ve yaklaşık görülme yüzdesi hangisidir?", [
            {"key": "A", "text": "Skuamöz hücreli karsinom (~%80)", "isCorrect": True, "explanation": "Skuamöz hücreli karsinom olguların yaklaşık %80'ini oluşturur."},
            {"key": "B", "text": "Glioblastoma multiforme (~%95)", "isCorrect": False, "explanation": "Primer beyin tümörüdür."},
            {"key": "C", "text": "Kondrosarkom (~%50)", "isCorrect": False, "explanation": "Kıkırdak tümörüdür."},
            {"key": "D", "text": "Yalnızca anjiyosarkom (<%0.1)", "isCorrect": False, "explanation": "Vasküler malignitedir."}
        ])
    ]
    slides.append(make_slide(61, "İnvaziv Serviks Karsinomu Histolojik Tipleri", "SCC (~%80), adenokarsinom (~%15), küçük hücreli (<%5), yüksek riskli HPV ortak paydası", "Malign Histopatoloji: Tipler", s61_narrative, s61_bullets, s61_elements))

    # Slide 62: Pap Taraması Sonrası Göreceli Adenokarsinom Artışı
    s62_narrative = (
        "Düzenli Pap smear tarama programlarının yaygınlaşması, serviks kanserlerinin histolojik "
        "oranlarında ilginç ve öğretici bir epidemiyolojik değişime yol açmıştır.\n\n"
        "- **Skuamöz İnsidansta Düşüş:** Pap smear eksfoliyatif sitolojisi skuamöz intraepitelyal lezyonları "
        "(SIL) çok yüksek başarıyla yakaladığı için invaziv **skuamöz karsinom insidansı dramatik biçimde azalmıştır**.\n"
        "- **Göreceli Adenokarsinom Artışı:** Endoservikal kanaldaki bez yapıları ve glandüler lezyonlar "
        "(adenokarsinoma in situ) fırça ile daha zor örneklendiğinden, **adenokarsinom oranı göreceli bir artış göstermiştir**.\n"
        "- **Biyolojik Neden:** Mutlak adenokarsinom sayısı patlama yapmamış; skuamöz kanserlerin taranıp önlenmesi "
        "nedeniyle glandüler tümörlerin toplam içindeki yüzdesi yükselmiştir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Pap testi ile invaziv skuamöz karsinom insidansı azaldığı için serviks kanserleri arasında adenokarsinom oranı göreceli artış göstermiştir."
    )
    s62_bullets = [
        "Pap testi skuamöz lezyonları başarıyla yakalayarak SCC insidansını düşürdü.",
        "Glandüler lezyonların tespiti daha zordur.",
        "Toplam kanserler içinde adenokarsinom oranı göreceli artış göstermiştir."
    ]
    s62_elements = [
        make_cloze("Pap smear taramasının SCC'yi azaltması sonucu serviks kanserleri içinde adenokarsinom oranı göreceli artış göstermiştir.", "adenokarsinom", "Göreceli oranı artan bez kaynaklı malignite"),
        make_table("Pap Smear Sonrası Histolojik Oran Değişimi", ["Histolojik Tip", "İnsidans Değişimi", "Epidemiyolojik Neden"], [
            {"cells": [{"text": "Skuamöz Hücreli Karsinom", "isMasked": False}, {"text": "Mutlak insidansta dramatik düşüş", "isMasked": True, "hint": "önlenebilen yassı hücreli kanser"}, {"text": "Pap smear ile preinvaziv başarılı tarama"}]},
            {"cells": [{"text": "Adenokarsinom", "isMasked": False}, {"text": "Göreceli yüzde artışı (~%15)", "isMasked": False}, {"text": "Endoservikal bezlerin taranmasındaki teknik zorluk", "isMasked": True, "hint": "kanal içi gizli glandüler lezyon"}]}
        ]),
        make_chain("Epidemiyolojik Oran Değişim Mekanizması", [
            "1. Taramada Başarı: Yüzeyel skuamöz CIN lezyonları erkenden eksize edilir.",
            "2. SCC Çöküşü: İnvaziv skuamöz karsinom vakaları %75-80 oranında azalır.",
            "3. Kanal İçi Kör Nokta: Endoservikal glandüler prekanseröz lezyonlar bazen atlanır.",
            "4. Göreceli Yükseliş: Kalan vakalar arasında adenokarsinomun payı göreceli olarak büyür."
        ]),
        make_recall("Pap smear tarama programlarının yaygınlaşması serviks kanserlerinin histolojik oranlarında nasıl bir göreceli değişime yol açmıştır?", "İnvaziv skuamöz karsinom insidansı azaldığı için adenokarsinom oranı toplam içinde göreceli bir artış göstermiştir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Göreceli Adenokarsinom Artışı", [
            {"text": "Pap testi ile invaziv skuamöz karsinom insidansı azalmıştır.", "isLie": False, "explanation": "Doğru. Tarama SCC'yi önlemiştir."},
            {"text": "Sonuçta adenokarsinom oranı göreceli artış göstermiştir.", "isLie": False, "explanation": "Doğru. Yüzdesel payı yükselmiştir."},
            {"text": "Pap smear taraması tüm kadınlarda adenokarsinomu tek gecede %1000 artıran bir zehirlenmedir.", "isLie": True, "explanation": "Tuzak! Pap smear zehirlemez; mutlak vaka artmamış, skuamöz azaldığı için adenokarsinom göreceli artmıştır."},
            {"text": "Pap testi bez lezyonlarını skuamöz lezyonlara göre daha zor saptar.", "isLie": False, "explanation": "Doğru. Endoservikal örnekleme kısıtlılığıdır."}
        ]),
        make_quiz("Pap smear tarama programları sonrasında serviks karsinomlarının histolojik tip dağılımında izlenen karakteristik değişim nedir?", [
            {"key": "A", "text": "İnvaziv skuamöz karsinom azalırken adenokarsinom oranının göreceli artış göstermesi", "isCorrect": True, "explanation": "SCC azaldığı için adenokarsinomun oransal payı artmıştır."},
            {"key": "B", "text": "Tüm kanserlerin tek bir günde tamamen osteosarkoma dönüşmesi", "isCorrect": False, "explanation": "Kemik tümörüne dönüşmez."},
            {"key": "C", "text": "Hiçbir histolojik tipte hiçbir oransal değişiklik olmaması", "isCorrect": False, "explanation": "Belirgin göreceli kayma olmuştur."},
            {"key": "D", "text": "Sadece erkeklerde karsinom görülmeye başlanması", "isCorrect": False, "explanation": "Serviks kadına aittir."}
        ])
    ]
    slides.append(make_slide(62, "Pap Taraması Sonrası Göreceli Adenokarsinom Artışı", "SCC insidans gerilemesi, glandüler lezyon kör noktası, göreceli oran kayması", "Epidemiyolojik Histoloji", s62_narrative, s62_bullets, s62_elements))

    # Slide 63: Makroskopik Büyüme Paternleri: Ekzofitik vs Endofitik
    s63_narrative = (
        "İnvaziv serviks karsinomu makroskopik olarak pelvik muayenede ve ameliyat piyeslerinde "
        "farklı morfolojik büyüme şekilleri sergileyebilir.\n\n"
        "- **Ekzofitik (Karnabahar Benzeri) Büyüme:** Tümör serviks yüzeyinden vajina lümenine doğru "
        "kabarık, polipoid, frajil ve karnabahar benzeri kitleler oluşturarak büyür; kolayca ülsere olur ve kanar.\n"
        "- **Endofitik (İnfiltratif) Büyüme:** Yüzeyde belirgin bir kitle yapmaksızın servikal stromanın derinliklerine "
        "doğru sinsi bir infiltrasyon gösterir; servikal kanalı çevreleyerek genişler.\n"
        "- **Ülseratif Büyüme:** Tümör dokusunun santral nekrozu sonucu derin, krater benzeri ülsere oyuklar oluşabilir.\n\n"
        "> [!NOTE]\n"
        "> İnvaziv serviks karsinomu makroskopik olarak ekzofitik karnabahar benzeri kitle veya stromaya infiltre endofitik büyüme gösterebilir."
    )
    s63_bullets = [
        "Ekzofitik büyüme lümene doğru karnabahar benzeri kitle yapar.",
        "Endofitik büyüme servikal stromanın derinlerine infiltre olur.",
        "Santral nekroz ile derin krater ülserleri gelişebilir."
    ]
    s63_elements = [
        make_cloze("Vajina lümenine doğru karnabahar benzeri kitle oluşturan makroskopik tümör büyümesine ekzofitik büyüme denir.", "ekzofitik", "Dışa doğru büyüyen kitle paterni"),
        make_table("Makroskopik Tümör Büyüme Şekilleri", ["Büyüme Tipi", "Görünüm Karakteri", "Klinik Özellik"], [
            {"cells": [{"text": "Ekzofitik Büyüme", "isMasked": False}, {"text": "Karnabahar benzeri polipoid frajil kitle", "isMasked": True, "hint": "dışa doğru kabaran kitle"}, {"text": "Muayenede temasla kolayca kanar"}]},
            {"cells": [{"text": "Endofitik Büyüme", "isMasked": False}, {"text": "Stromaya derin infiltratif yayılım", "isMasked": False}, {"text": "Servikste sertleşme ve silindirik kalınlaşma", "isMasked": True, "hint": "derin doku sertleşmesi"}]}
        ]),
        make_chain("Makroskopik Gelişim Yolu", [
            "1. Mikroskopik Odak: Transformasyon bölgesinde mikroinvazyon başlar.",
            "2. Kitle Gelişimi: Malign hücreler kontrolsüz bölünerek kitle hacmini artırır.",
            "3. Lümene Taşma: Ekzofitik kitle vajinal fornikslere doğru genişler.",
            "4. Nekroz ve Kanama: Dolaşımı yetmeyen tümör yüzeyi ülsere olarak kanar."
        ]),
        make_recall("İnvaziv serviks kanserinin iki ana makroskopik büyüme paterni nedir?", "Lümene doğru büyüyen ekzofitik (karnabahar benzeri) kitle ve derin dokuya ilerleyen endofitik (infiltratif) büyümedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Makroskopik Tümör Paternleri", [
            {"text": "Ekzofitik tümörler vajina lümenine doğru karnabahar benzeri kitle yapabilir.", "isLie": False, "explanation": "Doğru. Tipik ekzofitik morfolojidir."},
            {"text": "Endofitik tümörler servikal stromaya derinlemesine infiltre olur.", "isLie": False, "explanation": "Doğru. İnfiltratif büyümedir."},
            {"text": "Serviks tümörleri makroskopik olarak sadece saydam cam balonlar şeklinde havada uçar.", "isLie": True, "explanation": "Tuzak! Tümör dokusu katı, frajil, etsi veya nekrotik bir kitle lezyonudur."},
            {"text": "Yüzeyel nekroz derin krater benzeri ülserasyonlara yol açabilir.", "isLie": False, "explanation": "Doğru. Ülseratif patern görülebilir."}
        ]),
        make_quiz("İnvaziv serviks karsinomunun lümene doğru kabarık ve frajil kitle oluşturarak büyümesine ne ad verilir?", [
            {"key": "A", "text": "Ekzofitik büyüme", "isCorrect": True, "explanation": "Dışa doğru büyüyen karnabahar lezyonuna ekzofitik kitle denir."},
            {"key": "B", "text": "Atrofik düzleşme", "isCorrect": False, "explanation": "Kitle oluşturmaz."},
            {"key": "C", "text": "Kistik teratom", "isCorrect": False, "explanation": "Germ hücreli tümördür."},
            {"key": "D", "text": "Vasküler hemanjiyom", "isCorrect": False, "explanation": "Benign damar lezyonudur."}
        ])
    ]
    slides.append(make_slide(63, "Makroskopik Büyüme Paternleri: Ekzofitik vs Endofitik", "Karnabahar kitle, endofitik infiltrasyon, krater ülserleri ve vasküler frajilite", "Makroskopik Morfoloji", s63_narrative, s63_bullets, s63_elements))

    # Slide 64: Skuamöz Karsinom Histopatolojisi ve Diferansiasyon
    s64_narrative = (
        "İnvaziv skuamöz hücreli karsinomun histopatolojik incelemesinde, atipik skuamöz epitel hücrelerinin "
        "desmoplastik stroma içine düzensiz adalar, kordonlar ve yuvalar halinde invazyon yaptığı görülür.\n\n"
        "- **İyi Diferansiye Karsinom:** Hücreler belirgin skuamöz özelliklerini korur; intraselüler köprüler "
        "(dezmozomlar) ve konsantrik keratin tabakalarından oluşan **keratin incileri (horn pearls)** içerir.\n"
        "- **Kötü Diferansiye Karsinom:** Skuamöz olgunlaşma kaybolmuştur; **az keratinizasyon** veya "
        "hiç keratin içermeyen, yüksek mitotik aktiviteye sahip pleomorfik hücre tabakaları izlenir.\n"
        "- **Stromal Yanıt:** Malign yuvaların etrafında yoğun lenfoplazmasitik inflamasyon ve fibroblastik "
        "kollajen sentezi (desmoplazi) dikkat çeker.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Histopatolojik derecelendirmede: iyi diferansiye skuamöz karsinomda keratin incileri belirginken; zayıf (kötü) diferansiye karsinomda az keratinizasyon izlenir."
    )
    s64_bullets = [
        "Malign hücre adaları desmoplastik stromaya invazyon yapar.",
        "İyi diferansiye tümörlerde keratin incileri karakteristiktir.",
        "Kötü diferansiye tümörlerde az keratinizasyon ve anaplastik hücreler izlenir."
    ]
    s64_elements = [
        make_cloze("İyi diferansiye servikal skuamöz karsinomda konsantrik keratin tabakalarından oluşan keratin incileri izlenir.", "keratin incileri", "İyi diferansiye skuamöz karsinomun patognomonik birikimi"),
        make_table("Skuamöz Karsinom Diferansiasyon Karşılaştırması", ["Diferansiasyon Derecesi", "Keratinizasyon Durumu", "Hücresel Morfoloji"], [
            {"cells": [{"text": "İyi Diferansiye", "isMasked": False}, {"text": "Belirgin keratin incileri (horn pearls)", "isMasked": True, "hint": "konsantrik keratin odakları"}, {"text": "Hücreler arası köprüler ve yassılaşma"}]},
            {"cells": [{"text": "Kötü Diferansiye", "isMasked": False}, {"text": "Az keratinizasyon veya yokluk", "isMasked": False}, {"text": "Belirgin pleomorfizm ve atipik bol mitoz", "isMasked": True, "hint": "anaplastik hücre tabakaları"}]}
        ]),
        make_chain("Stromal İnvazyon Histolojisi", [
            "1. Bazal Membran Yıkımı: Malign hücreler matriks metalloproteinaz salgılar.",
            "2. Stromaya Giriş: Skuamöz adalar servikal bağ dokusu içine kordonlar halinde dalar.",
            "3. Desmoplastik Yanıt: Çevre stroma reaktif olarak fibroblastik doku üretir.",
            "4. Keratin Birikimi: Diferansiye yuvaların merkezinde keratin incileri çöker."
        ]),
        make_recall("İyi diferansiye skuamöz hücreli karsinom ile zayıf (kötü) diferansiye karsinom arasındaki temel histopatolojik keratinizasyon farkı nedir?", "İyi diferansiyede keratin incileri belirginken; zayıf diferansiyede az keratinizasyon veya hiç keratinizasyon izlenmez."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Skuamöz Karsinom Histopatolojisi", [
            {"text": "İyi diferansiye tümörlerde keratin incileri görülür.", "isLie": False, "explanation": "Doğru. Tipik histolojik belirteçtir."},
            {"text": "Zayıf diferansiye tümörlerde az keratinizasyon izlenir.", "isLie": False, "explanation": "Doğru. Diferansiasyon kaybını gösterir."},
            {"text": "Skuamöz hücreli karsinom histolojisinde sadece saf kıkırdak ve diş minesi izlenir.", "isLie": True, "explanation": "Tuzak! Karsinom skuamöz hücrelerden ve stromadan oluşur; diş minesi veya kıkırdak içermez."},
            {"text": "Tümör yuvaları desmoplastik stroma içine invazyon yapar.", "isLie": False, "explanation": "Doğru. İnvaziv karsinom mimarisidir."}
        ]),
        make_quiz("İyi diferansiye skuamöz hücreli serviks karsinomunun mikroskobik incelemesinde en karakteristik histolojik bulgu nedir?", [
            {"key": "A", "text": "Konsantrik keratin incileri (horn pearls)", "isCorrect": True, "explanation": "İyi diferansiye SCC'de keratin incileri karakteristiktir."},
            {"key": "B", "text": "Hücreler içinde yağ vakuolleri ve safra kristalleri", "isCorrect": False, "explanation": "Hepatoselüler özelliklerdir."},
            {"key": "C", "text": "Sadece multinükleer osteoklastlar", "isCorrect": False, "explanation": "Kemik patolojisidir."},
            {"key": "D", "text": "Amipli kistler", "isCorrect": False, "explanation": "Paraziter bulgudur."}
        ])
    ]
    slides.append(make_slide(64, "Skuamöz Karsinom Histopatolojisi ve Diferansiasyon", "Desmoplazi, keratin incileri, zayıf diferansiasyon ve stromal invazyon adaları", "Histopatolojik Derecelendirme", s64_narrative, s64_bullets, s64_elements))

    # Slide 65: Adenokarsinom ve Küçük Hücreli Nöroendokrin Karsinom
    s65_narrative = (
        "Skuamöz hücreli karsinom dışındaki servikal maligniteler, farklı histogenetik kökenleri "
        "ve agresif biyolojik davranışları ile ayrı bir klinik önem taşır.\n\n"
        "- **Adenokarsinom:** Endoservikal mukus salgılayan kolumnar epitelden köken alır; "
        "**bez yapıları (glandüler mimari) oluşturan** pleomorfik, müsin içeren malign hücrelerden oluşur.\n"
        "- **Adenoskuamöz Karsinom:** Aynı tümör kitlesi içinde hem malign glandüler bez komponenti "
        "hem de malign skuamöz epitel adaları bir arada bulunur.\n"
        "- **Küçük Hücreli Nöroendokrin Karsinom:** Olguların <%5'ini oluşturur; mikroskopta akciğerin küçük "
        "hücreli karsinomuna benzer. Nöroendokrin diferansiasyon gösterir, kan yoluyla çok erken metastaz yapar "
        "ve **prognozu son derece kötüdür**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Küçük hücreli nöroendokrin karsinom <%5 oranında görülür, akciğer küçük hücreli karsinomuna benzer ve prognozu en kötü olan histolojik tiptir."
    )
    s65_bullets = [
        "Adenokarsinom endoservikal glandüler mimari oluşturan malign hücrelerden oluşur.",
        "Adenoskuamöz karsinom hem bez hem skuamöz malign bileşen içerir.",
        "Küçük hücreli nöroendokrin karsinom <%5'tir ve prognozu en kötü tiptir."
    ]
    s65_elements = [
        make_cloze("Serviks kanserleri içinde nöroendokrin özellik gösteren ve prognozu en kötü olan tip küçük hücreli nöroendokrin karsinomdur.", "küçük hücreli", "En agresif serviks karsinomu morfolojik tipi"),
        make_table("Nadir ve Glandüler Serviks Karsinomları", ["Histolojik Tip", "Histopatolojik Görünüm", "Klinik Seyir / Prognoz"], [
            {"cells": [{"text": "Adenokarsinom", "isMasked": False}, {"text": "Malign bez (gland) yapıları oluşturan hücreler", "isMasked": True, "hint": "lümenli salgı bezleri"}, {"text": "Pap smear ile yakalanması daha güç"}]},
            {"cells": [{"text": "Küçük Hücreli Nöroendokrin", "isMasked": False}, {"text": "Akciğer küçük hücreli benzeri ezilme artefaktlı hücreler", "isMasked": False}, {"text": "Erken hematojen yayılım, çok kötü prognoz", "isMasked": True, "hint": "en ölümcül agresif seyir"}]}
        ]),
        make_chain("Küçük Hücreli Karsinom Agresyon Zinciri", [
            "1. Nöroendokrin Diferansiasyon: Rezerv hücreler nöroendokrin fenotipe kayar.",
            "2. Hızlı Çoğalma: Nükleus sitoplazma oranı aşırı yüksek küçük hücreler çoğalır.",
            "3. Erken Vasküler İnvazyon: Kanser hücreleri derin kapillerlere hızla sızar.",
            "4. Hematojen Metastaz: Lenf nodlarını beklemeden uzak organlara yayılarak mortaliteye yol açar."
        ]),
        make_recall("Serviks kanserleri arasında en kötü prognoza sahip olan ve akciğer küçük hücreli karsinomuna benzeyen nadir histolojik tip hangisidir?", "Küçük hücreli nöroendokrin karsinomdur (<%5)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Adenokarsinom ve Küçük Hücreli Karsinom", [
            {"text": "Adenokarsinom endoservikal mukus salgılayan bezlerden gelişir.", "isLie": False, "explanation": "Doğru. Glandüler kökenlidir."},
            {"text": "Küçük hücreli nöroendokrin karsinomun prognozu çok kötüdür.", "isLie": False, "explanation": "Doğru. En agresif histolojik tiptir."},
            {"text": "Küçük hücreli nöroendokrin karsinom hastalarında 1 saat sonra tümör kendiliğinden elmas kristaline dönüşür.", "isLie": True, "explanation": "Tuzak! Tümör hızla metastaz yapan ölümcül bir malignitedir; elmaslaşmaz."},
            {"text": "Adenoskuamöz karsinom hem bez hem skuamöz komponent içerir.", "isLie": False, "explanation": "Doğru. Mikst histolojidir."}
        ]),
        make_quiz("İnvaziv serviks karsinomları içerisinde prognozu en kötü olan ve nöroendokrin özellik gösteren histolojik tip hangisidir?", [
            {"key": "A", "text": "Küçük hücreli nöroendokrin karsinom", "isCorrect": True, "explanation": "Küçük hücreli nöroendokrin karsinom prognozu en kötü olan tiptir."},
            {"key": "B", "text": "İyi diferansiye skuamöz karsinom", "isCorrect": False, "explanation": "Prognozu daha iyidir."},
            {"key": "C", "text": "Endoservikal polip", "isCorrect": False, "explanation": "Benign bir lezyondur."},
            {"key": "D", "text": "Naboth kisti", "isCorrect": False, "explanation": "Malign değildir."}
        ])
    ]
    slides.append(make_slide(65, "Adenokarsinom ve Küçük Hücreli Nöroendokrin Karsinom", "Glandüler yapılar, mikst adenoskuamöz tümörler, nöroendokrin diferansiasyon ve kötü prognoz", "Histopatoloji: Adeno ve Nöroendokrin", s65_narrative, s65_bullets, s65_elements))

    # Slide 66: Fıçı Serviks (Barrel-Shaped Cervix) ve Derin İnvazyon
    s66_narrative = (
        "İnvaziv karsinom endoservikal kanal boyunca stromaya derinlemesine yayıldığında pelvik "
        "anatomide çok karakteristik bir klinik ve makroskopik deformite oluşturur.\n\n"
        "- **Derin Stromal İnvazyon:** Tümör servikal kanal mukozasını çepeçevre sararak servikal "
        "stromanın derinliklerine doğru çepeçevre infiltre olur.\n"
        "- **Fıçı Serviks Morfolojisi:** Bu derin infiltratif büyüme sonucu serviks simetrik veya asimetrik "
        "olarak genişler; palpasyonda **kalın, sert, rijit ve tahta kıvamında bir silindir/fıçı halini alır**.\n"
        "- **Klinik Yansıması:** 'Fıçı serviks' (barrel-shaped cervix) bulgusu, tümörün sadece yüzeyel değil, "
        "derin pelvik parametrium sınırlarına dayandığını gösteren ileri lokal invazyon göstergesidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Tümörün serviksi sararak stromaya derin invazyon yapması ve palpasyonda kalın, rijit bir silindir halini almasına 'fıçı serviks' (barrel-shaped cervix) adı verilir."
    )
    s66_bullets = [
        "Tümör serviksi çepeçevre sararak stromaya derin invazyon yapar.",
        "Palpasyonda kalın, sert ve rijit bir silindir ('fıçı serviks') saptanır.",
        "Derin stromal ve parametrial yayılımın klinik göstergesidir."
    ]
    s66_elements = [
        make_cloze("Tümörün stromaya derin invazyonu ile serviksin kalın ve rijit bir silindire dönüşmesine fıçı serviks adı verilir.", "fıçı serviks", "Derin invazyonlu serviksin makroskopik klinik terimi"),
        make_table("Fıçı Serviks Morfolojik Özellikleri", ["Klinik Unsur", "Muayene Bulgusu", "Patolojik Anlamı"], [
            {"cells": [{"text": "Kıvam ve Şekil", "isMasked": False}, {"text": "Kalın, rijit ve sert silindirik kitle", "isMasked": True, "hint": "sertleşmiş fıçı morfolojisi"}, {"text": "Yaygın stromal tümör infiltrasyonu"}]},
            {"cells": [{"text": "Lokal Yayılım", "isMasked": False}, {"text": "Parametriumlara doğru lateral genişleme", "isMasked": False}, {"text": "Cerrahi sınır riski ve ileri evre göstergesi", "isMasked": True, "hint": "derin doku infiltrasyon tehlikesi"}]}
        ]),
        make_chain("Fıçı Serviks Gelişim Süreci", [
            "1. Kanal İçi İnfiltrasyon: Karsinom endoservikal stromal lifler arasına dalar.",
            "2. Çepeçevre Genişleme: Malign yuvalar serviksin tüm duvar kalınlığını tutar.",
            "3. Desmoplastik Rijidite: Kollajen sentezi dokuyu sert bir kütük kıvamına sokar.",
            "4. Fıçı Palpasyonu: Jinekolog vajinal tuşede kalın, hareketsiz fıçı serviksi palpe eder."
        ]),
        make_recall("Tümörün serviksi sararak stromaya derin invazyon yapması sonucu palpasyonda saptanan kalın, rijit serviks deformitesine ne ad verilir?", "'Fıçı serviks' (barrel-shaped cervix) adı verilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fıçı Serviks", [
            {"text": "Tümör serviksi sararak stromaya derin invazyon yapabilir.", "isLie": False, "explanation": "Doğru. İnfiltratif yayılımdır."},
            {"text": "Fıçı serviks palpasyonda kalın, rijit bir serviks şeklinde hissedilir.", "isLie": False, "explanation": "Doğru. Tipik klinik muayene bulgusudur."},
            {"text": "Fıçı serviks lezyonu hiçbir hücresi olmayan içi tamamen su dolu selim bir balon kistidir.", "isLie": True, "explanation": "Tuzak! Fıçı serviks su balonu değil; derin karsinom infiltrasyonu sonucu serviksin kalınlaşıp sertleşmesidir."},
            {"text": "Derin invazyon parametrial yayılım riskini gösterir.", "isLie": False, "explanation": "Doğru. Lokal ileri evre belirtisidir."}
        ]),
        make_quiz("Tümörün servikal stromaya derin invazyon yapmasıyla serviksin palpasyonda kalın, sert ve rijit bir silindir halini almasına ne ad verilir?", [
            {"key": "A", "text": "Fıçı serviks (barrel-shaped cervix)", "isCorrect": True, "explanation": "Derin stromal invazyonla oluşan bu tablo fıçı servikstir."},
            {"key": "B", "text": "Gartner kisti", "isCorrect": False, "explanation": "Vajinal mezonefrik kisttir."},
            {"key": "C", "text": "Normal ektoserviks", "isCorrect": False, "explanation": "Normal serviks yumuşak ve esnektir."},
            {"key": "D", "text": "Bartholin absesi", "isCorrect": False, "explanation": "Vulvar apse lezyonudur."}
        ])
    ]
    slides.append(make_slide(66, "Fıçı Serviks (Barrel-Shaped Cervix) ve Derin İnvazyon", "Stromal infiltrasyon, rijit silindir serviks, parametrial sınır komşuluğu ve palpasyon bulguları", "Klinik Makroskopi: Fıçı Serviks", s66_narrative, s66_bullets, s66_elements))

    # Slide 67: Parametrial Yayılım ve Pelvik Fiksasyon
    s67_narrative = (
        "Serviks karsinomu çevre dokulara doğrudan (lokal) komşuluk yoluyla yayılma eğilimi "
        "gösteren bir malignitedir.\n\n"
        "- **Parametrium İnvazyonu:** Serviksin her iki yanında yer alan, damar ve sinir ağlarını barındıran "
        "pelvik bağ dokusuna **parametrium** adı verilir. Tümör lateral yönde bu alana taşar.\n"
        "- **Pelvik Fiksasyon:** Parametriumların tam kat tümörle infiltre olması, uterusun pelvik yan duvarlara "
        "adeta yapışmasına yol açar; rektovajinal muayenede uterus tamamen **hareketsiz (fikse)** olarak palpe edilir.\n"
        "- **Operabilite Sınırı:** Parametrial yayılım saptanan olgular cerrahi olarak çıkarılamaz (inopere kabul edilir); "
        "bu aşamada tedavi cerrahiden kemoradyoterapiye kayar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Tümörün lateralde parametriumlara yayılması, uterusun pelvik yan duvarlara fikse olmasına (hareketsizleşmesine) yol açar."
    )
    s67_bullets = [
        "Tümör lateral komşulukla parametriumlara yayılır.",
        "Parametrial yayılım uterusun pelvik duvarlara fikse olmasına yol açar.",
        "Pelvik fiksasyon cerrahi sınırın aşıldığını gösterir."
    ]
    s67_elements = [
        make_cloze("Tümörün lateral pelvik bağ dokusuna yayılmasına parametrial yayılım adı verilir.", "parametrial", "Serviksin iki yanındaki pelvik bağ dokusuna yayılım"),
        make_table("Parametrial Tutulum ve Klinik Sonuçları", ["Anatomik Alan", "Yayılım Yolu", "Klinik Sonuç"], [
            {"cells": [{"text": "Lateral Parametrium", "isMasked": False}, {"text": "Doğrudan lokal stromal infiltrasyon", "isMasked": True, "hint": "komşuluk yoluyla yayılım"}, {"text": "Uterus pelvise fikse hale gelir"}]},
            {"cells": [{"text": "Pelvik Duvar", "isMasked": False}, {"text": "Bağ dokusu infiltrasyonunun kemiğe dayanması", "isMasked": False}, {"text": "Cerrahi şansının kaybı (kemoradyoterapi)", "isMasked": True, "hint": "cerrahi dışı onkolojik tedaviye geçiş"}]}
        ]),
        make_chain("Lokal Yayılım Basamakları", [
            "1. Servikal Kapsül: Tümör servikal fibromusküler stromayı aşar.",
            "2. Parametrial İnvazyon: Kanser hücreleri pelvik yağ ve damar kılıflarına girer.",
            "3. Yan Duvar Fiksasyonu: Pelvik yan duvar kas ve fasyalarına kitle kilitlenir.",
            "4. Rijid Donuk Pelvis: Uterus muayenede milimetrik dahi hareket ettirilemez."
        ]),
        make_recall("Serviks kanserinde tümörün parametriumlara yayılmasının pelvik muayenedeki en belirgin bulgusu nedir?", "Uterusun pelvik yan duvarlara fikse olması (tamamen hareketsizleşmesi) bulgusudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Parametrial Yayılım", [
            {"text": "Tümör lateralde parametriumlara doğrudan yayılabilir.", "isLie": False, "explanation": "Doğru. Majör lokal yayılım yoludur."},
            {"text": "Parametrial yayılım uterusun pelvik duvarlara fikse olmasına yol açar.", "isLie": False, "explanation": "Doğru. Hareket kabiliyeti kaybolur."},
            {"text": "Parametriumlara yayılan karsinom hastanın parmak uçlarından tırnak gibi dışarı uzar.", "isLie": True, "explanation": "Tuzak! Parametrial yayılım pelvik derin dokularla sınırlıdır; tırnak uzaması ile ilgisi yoktur."},
            {"text": "Pelvik fiksasyon cerrahi rezektabiliteyi doğrudan etkiler.", "isLie": False, "explanation": "Doğru. İnoperabilite kriteridir."}
        ]),
        make_quiz("Serviks karsinomunda uterusun pelvik yan duvarlara fikse olmasına (hareketsiz kalmasına) yol açan lokal yayılım hangisidir?", [
            {"key": "A", "text": "Tümörün parametriumlara yayılması", "isCorrect": True, "explanation": "Parametrial yayılım pelvik fiksasyonun nedenidir."},
            {"key": "B", "text": "Yalnızca ayak bileğinde burkulma olması", "isCorrect": False, "explanation": "Ortopedik travmadır."},
            {"key": "C", "text": "Mide ülserinin kanaması", "isCorrect": False, "explanation": "Gastrik hastalıktır."},
            {"key": "D", "text": "Basit bir grip enfeksiyonu geçirilmesi", "isCorrect": False, "explanation": "Solunum yolu viral tablosudur."}
        ])
    ]
    slides.append(make_slide(67, "Parametrial Yayılım ve Pelvik Fiksasyon", "Lateral parametrial infiltrasyon, uterus fiksasyonu, donuk pelvis ve rezektabilite", "Lokal Yayılım Yolları", s67_narrative, s67_bullets, s67_elements))

    # Slide 68: Pelvik Lenf Düğümü Metastazı Dinamikleri
    s68_narrative = (
        "İnvaziv serviks karsinomunun uzak organlara yayılmadan önceki ilk ve en kritik metastatik "
        "durağı bölgesel pelvik lenf düğümleridir.\n\n"
        "- **İnvazyon Derinliği İlişkisi:** Pelvik lenf nodu metastazı riski, tümörün servikal stromadaki "
        "**invazyon derinliği ile doğrudan korelasyon gösterir**; stromaya 3 mm'den az giren mikroinvaziv "
        "lezyonlarda lenf nodu riski <%1 iken, derin invazyonda risk %50'lere tırmanır.\n"
        "- **Vasküler Boşluk İnvazyonu (LVSI):** Mikroskopta tümör hücrelerinin lenfatik veya kılcal damar "
        "lümenlerinde (lenfovasküler boşluklar) görülmesi lenf nodu metastaz riskini katlar.\n"
        "- **Yayılım Sırası:** Paraservikal, obturator, iliak (eksternal/internal) ve presakral lenf düğümleri ilk tutulan istasyonlardır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Pelvik lenf düğümlerine metastaz riski stromal invazyon derinliği ve vasküler boşluklarda tümör varlığı ile doğrudan ilişkilidir."
    )
    s68_bullets = [
        "Pelvik lenf nodu metastazı stromal invazyon derinliği ile doğrudan ilişkilidir.",
        "Vasküler boşluklarda (LVSI) tümör varlığı metastaz riskini katlar.",
        "Obturator ve iliak lenf düğümleri ilk tutulan bölgesel istasyonlardır."
    ]
    s68_elements = [
        make_cloze("Pelvik lenf düğümü metastaz riski tümörün stromal invazyon derinliği ile doğrudan ilişkilidir.", "invazyon derinliği", "Metastaz riskini belirleyen primer histopatolojik ölçüt"),
        make_table("Lenfatik Yayılımı Belirleyen Faktörler", ["Faktör", "Eşik Değer / Özellik", "Lenf Nodu Metastaz Riski"], [
            {"cells": [{"text": "Stromal Derinlik", "isMasked": False}, {"text": "<3 mm (mikroinvaziv) vs >5 mm derin invazyon", "isMasked": True, "hint": "stromaya batma mesafesi"}, {"text": "<%1'den >%30'lara fırlar"}]},
            {"cells": [{"text": "Lenfovasküler İnvazyon (LVSI)", "isMasked": False}, {"text": "Damar lümeninde tümör embolisi", "isMasked": False}, {"text": "Belirgin artmış nodal tutulum riski", "isMasked": True, "hint": "embolik yayılım tehdidi"}]}
        ]),
        make_chain("Lenfatik Metastaz Aşamaları", [
            "1. Stromal İntrüzyon: Karsinom adaları stromal lenfatik endoteline yaklaşır.",
            "2. Lümen Girişi: Lenfatik endoteli delinerek kılcal lümende tümör embolisi oluşur.",
            "3. Bölgesel Göç: Malign hücreler obturator ve iliak lenf nodlarına taşınır.",
            "4. Paraaortik Sıçrama: Pelvik nodlardan sonra retroperitoneal paraaortik zincire ulaşılır."
        ]),
        make_recall("Serviks karsinomunda pelvik lenf düğümü metastazı gelişme olasılığını belirleyen en kritik iki histopatolojik parametre nedir?", "Tümörün stromal invazyon derinliği ve lenfovasküler boşluklarda tümör varlığıdır (LVSI)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Pelvik Lenf Nodu Metastazı", [
            {"text": "Pelvik lenf düğümlerine metastaz invazyon derinliği ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Derinlik arttıkça risk artar."},
            {"text": "Vasküler boşluklarda tümör varlığı lenfatik yayılım riskini artırır.", "isLie": False, "explanation": "Doğru. LVSI pozitifliği riski katlar."},
            {"text": "Serviks kanseri lenf düğümlerini tamamen atlayıp sadece saç tellerinde metastaz yapar.", "isLie": True, "explanation": "Tuzak! Lenfatik metastaz pelvik lenf düğümlerine olur; saç telinde metastaz görülmez."},
            {"text": "Obturator ve iliak lenf nodları ilk tutulan bölgesel istasyonlardır.", "isLie": False, "explanation": "Doğru. Primer drenaj sahasıdır."}
        ]),
        make_quiz("İnvaziv serviks karsinomunda bölgesel pelvik lenf düğümü metastazı gelişme riskini doğrudan belirleyen temel faktör nedir?", [
            {"key": "A", "text": "Stromal invazyon derinliği ve vasküler boşluklarda tümör varlığı", "isCorrect": True, "explanation": "İnvazyon derinliği ve LVSI lenf metastazını belirleyen ana faktörlerdir."},
            {"key": "B", "text": "Hastanın göz rengi", "isCorrect": False, "explanation": "Korelasyon yoktur."},
            {"key": "C", "text": "Kullanılan şampuanın markası", "isCorrect": False, "explanation": "İlişkisizdir."},
            {"key": "D", "text": "Yalnızca havanın nem oranı", "isCorrect": False, "explanation": "Meteorolojik durumla ilgisizdir."}
        ])
    ]
    slides.append(make_slide(68, "Pelvik Lenf Düğümü Metastazı Dinamikleri", "İnvazyon derinliği, lenfovasküler invazyon (LVSI), iliak/obturator lenf istasyonları", "Metastaz Dinamikleri", s68_narrative, s68_bullets, s68_elements))

    # Slide 69: Komşu Organ İnvazyonu: Mesane, Rektum ve Fistüller
    s69_narrative = (
        "İleri evre serviks karsinomlarında tümör yalnızca parametriumlara değil, anterior ve posterior "
        "komşuluğundaki hayati pelvik organlara da yayılım gösterir.\n\n"
        "- **Mesane İnvazyonu:** Tümör anteriora doğru ilerleyerek mesane duvarını ve mukozasını infiltre eder; "
        "hematüri (kanlı idrar) ve dizüriye yol açar.\n"
        "- **Rektum İnvazyonu:** Posteriora ilerleyen tümör rektovajinal septumu yıkarak rektum lümenine ulaşır; "
        "tenezm ve rektal kanama gelişir.\n"
        "- **Fistül Oluşumu:** İlerleyen tümör nekrozu organ duvarlarında delinmelere yol açar; "
        "**vezikovajinal fistül** (vajinadan sürekli idrar kaçışı) ve **rektovajinal fistül** (vajinadan dışkı gelişi) "
        "gibi son derece ızdırap verici komplikasyonlar gelişir.\n\n"
        "> [!NOTE]\n"
        "> İleri evrede mesane ve rektum mukozası tutulabilir; tümör nekrozu vezikovajinal ve rektovajinal fistüllere yol açar."
    )
    s69_bullets = [
        "Tümör öne doğru mesaneyi, arkaya doğru rektumu infiltre edebilir.",
        "Doku nekrozu vezikovajinal ve rektovajinal fistüllere yol açar.",
        "Bu durum ileri evre (Evre IV) hastalığın göstergesidir."
    ]
    s69_elements = [
        make_cloze("Mesane ile vajina arasında tümör nekrozuyla açılan idrar kaçağı yoluna vezikovajinal fistül adı verilir.", "vezikovajinal fistül", "Mesane ve vajina arasındaki patolojik kanal"),
        make_table("Komşu Organ İnvazyonu ve Fistül Tipleri", ["Tutulan Komşu Organ", "Klinik Belirti", "Gelişen Fistül Türü"], [
            {"cells": [{"text": "Mesane (Anterior)", "isMasked": False}, {"text": "Hematüri ve idrar kaçırma", "isMasked": True, "hint": "idrardan kan gelmesi"}, {"text": "Vezikovajinal fistül (vajinadan idrar gelmesi)"}]},
            {"cells": [{"text": "Rektum (Posterior)", "isMasked": False}, {"text": "Rektal kanama ve tenezm", "isMasked": False}, {"text": "Rektovajinal fistül (vajinadan dışkı gelmesi)", "isMasked": True, "hint": "vajinal fekal kontaminasyon"}]}
        ]),
        make_chain("Organ İnvazyonundan Fistüle", [
            "1. Komşuluk İstilası: Tümör serviks sınırını aşarak komşu mesane ve rektuma dayanır.",
            "2. Duvar Penetrasyonu: Müsküler tabaka delinerek mukoza tutulur.",
            "3. İskemik Nekroz: Tümör kitlesinin santrali beslenemeyerek çürür ve erir.",
            "4. Fistül Açılması: Organlar arasında delik oluşarak vajinaya idrar ve feçes dökülür."
        ]),
        make_recall("İleri evre serviks karsinomunda mesane ve rektum tutulumu sonucu gelişen en ağır iki fistül komplikasyonu nedir?", "Vezikovajinal fistül (idrar kaçağı) ve rektovajinal fistüldür (dışkı kaçağı)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komşu Organ Tutulumu ve Fistüller", [
            {"text": "Tümör mesane mukozasına yayılarak hematüri yapabilir.", "isLie": False, "explanation": "Doğru. Mesane invazyonu kanamaya yol açar."},
            {"text": "Tümör nekrozu vezikovajinal ve rektovajinal fistüllere yol açabilir.", "isLie": False, "explanation": "Doğru. İleri evre fistül komplikasyonlarıdır."},
            {"text": "Rektum tutulduğunda hasta parmak uçlarından süt emzirmeye başlar.", "isLie": True, "explanation": "Tuzak! Rektum tutulumu fistül ve kanama yapar; süt emzirme ile ilgisi yoktur."},
            {"text": "Bu bulgular hastalığın ileri lokal evrede olduğunu gösterir.", "isLie": False, "explanation": "Doğru. Evre IV göstergesidir."}
        ]),
        make_quiz("İleri evre serviks kanserinde tümörün rektovajinal septumu delmesi sonucu vajinadan gayta gelmesine ne ad verilir?", [
            {"key": "A", "text": "Rektovajinal fistül", "isCorrect": True, "explanation": "Rektum ile vajina arasındaki patolojik geçit rektovajinal fistüldür."},
            {"key": "B", "text": "Basit lökore", "isCorrect": False, "explanation": "Lökore vajinal akıntıdır, gayta değildir."},
            {"key": "C", "text": "Naboth kisti rüptürü", "isCorrect": False, "explanation": "Benign kist rüptürüdür."},
            {"key": "D", "text": "Gözyaşı kanalı tıkanması", "isCorrect": False, "explanation": "Lakrimal sistemdir."}
        ])
    ]
    slides.append(make_slide(69, "Komşu Organ İnvazyonu: Mesane, Rektum ve Fistüller", "Mesane mukozası, rektum invazyonu, vezikovajinal/rektovajinal fistüller ve komplikasyonlar", "Lokal İleri Komplikasyonlar", s69_narrative, s69_bullets, s69_elements))

    # Slide 70: [TEKRAR SAYFASI - CHECKPOINT 7] İnvaziv Karsinom Tipleri ve Lokal Yayılım
    s70_narrative = (
        "Bölüm 7'de invaziv serviks karsinomunun histopatolojik sınıflamasını, diferansiasyon kriterlerini, "
        "derin stromal fıçı serviks formasyonunu ve pelvik yayılım paternlerini konsolide ettik.\n\n"
        "- **Histolojik Dağılım:** Skuamöz hücreli karsinom **~%80**, adenokarsinom/adenoskuamöz **~%15**, "
        "küçük hücreli nöroendokrin **<%5**; tümü yüksek riskli HPV ile ilişkilidir. Pap taramasıyla SCC azalırken "
        "adenokarsinom oranı **göreceli artış** göstermiştir.\n"
        "- **Histopatoloji ve Diferansiasyon:** İyi diferansiyede **keratin incileri**, zayıf diferansiyede **az keratinizasyon** izlenir. "
        "Küçük hücreli nöroendokrin karsinom **en kötü prognoza** sahiptir.\n"
        "- **Derin ve Lokal Yayılım:** Stromaya derin invazyon palpasyonda rijit **fıçı serviks (barrel-shaped)** yapar; "
        "lateral parametrial yayılım **uterusun pelvik yan duvarlara fikse olmasına** yol açar.\n"
        "- **Lenfatik ve Komşu Organ:** Pelvik lenf nodu metastazı **invazyon derinliği** ve LVSI ile bağlantılıdır; "
        "mesane ve rektum nekrozu vezikovajinal/rektovajinal fistüllere yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 7 SENTEZİ] Karsinomun %80'i skuamözdür ve iyi diferansiyede keratin incileri içerir; fıçı serviks derin stromal tutulumu, pelvik fiksasyon parametrial yayılımı gösterir; en kötü prognoz küçük hücreli tiptedir."
    )
    s70_bullets = [
        "Karsinomun ~%80'i skuamözdür; iyi diferansiyede keratin incileri karakteristiktir.",
        "Pap taramasıyla adenokarsinom oranı göreceli artış göstermiştir.",
        "Fıçı serviks derin stromal invazyonu; fiksasyon parametrial yayılımı gösterir.",
        "Pelvik lenf metastazı invazyon derinliğine bağlıdır; küçük hücreli tip en kötü prognozludur."
    ]
    s70_elements = [
        make_cloze("İnvaziv karsinomun derin stromal invazyonu sonucu palpasyonda rijit silindir halini almasına fıçı serviks adı verilir.", "fıçı serviks", "Bölüm 7 checkpointinde pekiştirilen derin invazyon terimi"),
        make_table("Bölüm 7 Karsinom ve Yayılım Sentez Tablosu", ["Patolojik Parametre", "Tipik Morfoloji / Bulgu", "Klinik / Prognostik Önemi"], [
            {"cells": [{"text": "En Sık Tip ve Diferansiasyon", "isMasked": False}, {"text": "Skuamöz Karsinom (~%80) ve Keratin İncileri", "isMasked": True, "hint": "yassı hücreli kanser ve boynuz incisi"}, {"text": "Tümörlerin ezici çoğunluğu"}]},
            {"cells": [{"text": "Derin İnvazyon Deformitesi", "isMasked": False}, {"text": "Fıçı serviks (rijit kalınlaşma)", "isMasked": False}, {"text": "Derin stromal ve parametrial yayılım riski", "isMasked": True, "hint": "lokal ileri yayılım göstergesi"}]},
            {"cells": [{"text": "En Kötü Prognozlu Tip", "isMasked": False}, {"text": "Küçük hücreli nöroendokrin karsinom (<%5)", "isMasked": True, "hint": "nadir agresif nöroendokrin tümör"}, {"text": "Hızlı hematojen metastaz ve fatal gidiş"}]}
        ]),
        make_chain("Bölüm 7 Süreç Konsolidasyonu", [
            "1. Skuamöz İnvazyon: %80 oranla başlayan SCC desmoplastik stromaya dalar.",
            "2. Diferansiasyon: İyi diferansiyede keratin incileri oluşurken, zayıfta anaplazi hakimdir.",
            "3. Fıçı Serviks ve Parametrium: Derinleşen kitle serviksi rijit silindire çevirip pelvise fikse eder.",
            "4. Nodal ve Fistüler Yayılım: İnvazyon derinliğiyle pelvik nodlar tutulur, mesane/rektumda fistül açılır."
        ]),
        make_recall("Bölüm 7'de öğrendiğimiz: (1) En sık histolojik tip, (2) En kötü prognozlu tip ve (3) Derin stromal kalınlaşma bulgusu nedir?", "(1) Skuamöz hücreli karsinom, (2) Küçük hücreli nöroendokrin karsinom, (3) Fıçı servikstir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 7 Checkpoint Sentezi", [
            {"text": "Skuamöz hücreli karsinom olguların yaklaşık %80'ini oluşturur.", "isLie": False, "explanation": "Doğru. En sık tiptir."},
            {"text": "İyi diferansiye skuamöz karsinomda keratin incileri görülür.", "isLie": False, "explanation": "Doğru. Diferansiasyon göstergesidir."},
            {"text": "Fıçı serviks sadece yeni doğan erkek çocuklarda görülen selim bir göbek bağı kistidir.", "isLie": True, "explanation": "Tuzak! Fıçı serviks kadında invaziv serviks karsinomunun derin stromal invazyonuyla serviksin kalınlaşmasıdır."},
            {"text": "Küçük hücreli nöroendokrin karsinom prognozu en kötü olan histolojik tiptir.", "isLie": False, "explanation": "Doğru. En ölümcül formdur."}
        ]),
        make_quiz("Bölüm 7'de pekiştirilen invaziv serviks karsinomu patolojisiyle ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Küçük hücreli nöroendokrin karsinom tüm serviks kanserleri içinde prognozu en iyi olandır", "isCorrect": True, "explanation": "Yanlış önerme! Prognozu en KÖTÜ olan histolojik tiptir."},
            {"key": "B", "text": "İnvaziv skuamöz karsinomların büyük çoğunluğunda keratin incileri görülebilir", "isCorrect": False, "explanation": "İyi diferansiyede karakteristiktir."},
            {"key": "C", "text": "Parametrial yayılım uterusun pelvik duvarlara fikse olmasına yol açar", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Pelvik lenf nodu metastazı stromal invazyon derinliği ile ilişkilidir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(70, "[TEKRAR SAYFASI - CHECKPOINT 7] İnvaziv Karsinom Tipleri ve Lokal Yayılım", "Bölüm 7 kapsamlı tekrarı: %80 SCC, fıçı serviks, keratin incileri, nöroendokrin karsinom", "Bölüm Tekrarı ve Konsolidasyon", s70_narrative, s70_bullets, s70_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec7()
    print(f"Sec7 generated: {len(slides)} slides (Slide 61 to 70)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
