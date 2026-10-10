import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec8():
    slides = []

    # Slide 71: Klinik Başvuru Semptomları: Beklenmedik Kanama
    s71_narrative = (
        "İnvaziv serviks karsinomu preinvaziv evrenin (SIL) aksine sessiz kalmaz; tümörün büyümesi, "
        "stromal damarları istila etmesi ve yüzeyinin ülsere olmasıyla birlikte belirgin semptomlar verir.\n\n"
        "- **Beklenmedik Vajinal Kanama:** En sık ve en kardinal klinik başvuru semptomudur. Özellikle "
        "cinsel ilişki sonrası lekelenme ve kanama (**postkoital kanama**), menstrüasyonlar arası düzensiz "
        "kanama (metroraji) ve en tehlikelisi **postmenopozal kanama** şeklinde karşımıza çıkar.\n"
        "- **Kötü Kokulu Akıntı:** Tümörün yüzeyel doku nekrozu ve ikincil bakteriyel enfeksiyonu sonucu "
        "kanlı, irinli ve oldukça **kötü kokulu vajinal akıntı (lökore)** tabloya eşlik eder.\n"
        "- **Pelvik Rahatsızlık:** Kitle etkisiyle disparoni (ağrılı cinsel ilişki) ve pelvik dolgunluk hissi gelişir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İnvaziv serviks karsinomunun en sık klinik belirtisi beklenmedik vajinal kanamadır (özellikle postkoital ve postmenopozal kanama)."
    )
    s71_bullets = [
        "En sık başvuru yakınması beklenmedik vajinal kanamadır.",
        "Postkoital lekelenme ve postmenopozal kanama alarm semptomlarıdır.",
        "Nekroza bağlı kötü kokulu, kanlı lökore sıklıkla eşlik eder."
    ]
    s71_elements = [
        make_cloze("İnvaziv serviks karsinomunda en sık görülen kardinal klinik belirti beklenmedik vajinal kanama olarak ortaya çıkar.", "vajinal kanama", "Tümör ülserasyonuna bağlı gelişen kardinal semptom"),
        make_table("Klinik Başvuru Semptomları ve Mekanizmaları", ["Semptom", "Mekanizma", "Klinik Özellik"], [
            {"cells": [{"text": "Postkoital Kanama", "isMasked": False}, {"text": "Frajil tümör damarlarının mekanik travması", "isMasked": True, "hint": "ilişki sırasında damar hasarı"}, {"text": "İlişkiden hemen sonra taze lekelenme"}]},
            {"cells": [{"text": "Kötü Kokulu Lökore", "isMasked": False}, {"text": "Tümör nekrozu ve anaerob süperenfeksiyon", "isMasked": False}, {"text": "Sürekli, kanlı ve pürülan akıntı", "isMasked": True, "hint": "iltihaplı nekrotik akıntı"}]}
        ]),
        make_chain("Semptom Gelişim Zinciri", [
            "1. İnvazyon ve Anjiyogenez: Karsinom frajil tümöral yeni damarlar üretir.",
            "2. Yüzeyel Ülserasyon: Kan akımı yetersiz kalır ve tümörün apeksi ülsere olur.",
            "3. Temas Travması: Cinsel ilişki veya spekulum temasında damarlar çatlar.",
            "4. Postkoital Kanama: Hasta taze kırmızı kanamayla hekime başvurur."
        ]),
        make_recall("İnvaziv serviks karsinomu tanısı alan bir kadında hekime başvuruyu sağlayan en sık klinik semptom nedir?", "Beklenmedik vajinal kanamadır (özellikle postkoital kanama veya postmenopozal kanama)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Klinik Başvuru Semptomları", [
            {"text": "En sık görülen semptom beklenmedik vajinal kanamadır.", "isLie": False, "explanation": "Doğru. Kardinal başvuru semptomudur."},
            {"text": "Postkoital kanama ve kötü kokulu lökore sık izlenir.", "isLie": False, "explanation": "Doğru. Temas kanaması ve nekrotik akıntı tipiktir."},
            {"text": "İnvaziv serviks kanseri hastalarında kulaktan sarı renkli motor yağı akar.", "isLie": True, "explanation": "Tuzak! Kulaktan motor yağı akmaz; pelvik vajinal kanama ve akıntı görülür."},
            {"text": "Postmenopozal kanama araştırılması gereken alarm bulgusudur.", "isLie": False, "explanation": "Doğru. Karsinom ekarte edilmelidir."}
        ]),
        make_quiz("İnvaziv serviks karsinomunda hastaları jinekoloji polikliniğine getiren en yaygın kardinal semptom aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Beklenmedik vajinal kanama (özellikle postkoital)", "isCorrect": True, "explanation": "Postkoital ve beklenmedik vajinal kanama en sık semptomdur."},
            {"key": "B", "text": "Parmak uçlarında uyuşma", "isCorrect": False, "explanation": "Periferik nöropatidir."},
            {"key": "C", "text": "Aşırı saç uzaması", "isCorrect": False, "explanation": "Hormonal veya fizyolojik durumdur."},
            {"key": "D", "text": "Bilateral burun tıkanıklığı", "isCorrect": False, "explanation": "Üst solunum yolu bulgusudur."}
        ])
    ]
    slides.append(make_slide(71, "Klinik Başvuru Semptomları: Beklenmedik Kanama", "Postkoital kanama, metroraji, postmenopozal kanama, nekrotik lökore ve disparoni", "Klinik Tablo ve Semptomatoloji", s71_narrative, s71_bullets, s71_elements))

    # Slide 72: Taranmamış Popülasyon Riski ve İhmal Edilmiş Olgular
    s72_narrative = (
        "Modern tıbbın ve tarama programlarının varlığına rağmen, invaziv serviks karsinomu olgularının "
        "büyük bir kısmı önlenebilir ihmaller zemininde gelişir.\n\n"
        "- **Taramasız Hasta Profili:** İnvaziv serviks kanseri saptanan kadınların büyük çoğunluğunun "
        "**yaşamları boyunca hiç Pap smear yaptırmamış** ya da tarama programlarına uzun yıllar ara vermiş "
        "bireyler olduğu görülmektedir.\n"
        "- **İhmal Edilmiş Pencere:** SIL'den invaziv kansere geçiş için gereken 10-15 yıllık latent süre "
        "doktora gidilmediği için değerlendirilememiş; tamamen sessiz geçen bu dönem kaçırılmıştır.\n"
        "- **Sosyoekonomik Boyut:** Sağlık güvencesi yetersizliği, kırsal kesimde yaşama ve sağlık okuryazarlığı "
        "düşüklüğü taranmamış hasta profilinin temel belirleyicileridir.\n\n"
        "> [!NOTE]\n"
        "> İnvaziv serviks karsinomu tanısı alan hastaların ezici çoğunluğu hiç tarama yaptırmamış veya takiplere uzun yıllar ara vermiş kadınlardır."
    )
    s72_bullets = [
        "Hastaların çoğu hiç taranmamış veya takibi aksatmış kadınlardır.",
        "10-15 yıllık koruyucu tarama penceresi kaçırılmıştır.",
        "Düzenli tarama ihmal edilen vakaların neredeyse tamamını önleyebilir."
    ]
    s72_elements = [
        make_cloze("İnvaziv karsinom olgularının büyük kısmı daha önce hiç tarama testi yaptırmamış popülasyonda karşımıza çıkar.", "tarama", "Hastalığın önlenmesinde ihmal edilen koruyucu işlem"),
        make_table("Taranmış ve Taranmamış Popülasyon Karşılaştırması", ["Hasta Grubu", "Ortalama Tanı Evresi", "Kür / Sağkalım Şansı"], [
            {"cells": [{"text": "Düzenli Tarananlar", "isMasked": False}, {"text": "Preinvaziv SIL (CIN I/II/III)", "isMasked": True, "hint": "erken hücresel evre"}, {"text": "> %99 tam kür"}]},
            {"cells": [{"text": "Taranmamış İhmal Olguları", "isMasked": False}, {"text": "İleri evre invaziv karsinom", "isMasked": False}, {"text": "Düşük sağkalım ve yüksek mortalite", "isMasked": True, "hint": "kötü prognoz ve fatal risk"}]}
        ]),
        make_chain("Taranmamış Olgularda Kanser Gelişimi", [
            "1. Taramasız Yıllar: Hasta 20-30 yıl boyunca hiçbir jinekolojik smear yaptırmaz.",
            "2. Sessiz Displazi: HPV 16 enfeksiyonu fark edilmeksizin CIN III'e evrilir.",
            "3. İnvazyon Başlangıcı: Semptomsuz geçen 10 yıllık pencere biter ve bazal membran delinir.",
            "4. Ağır Başvuru: Hasta ileri evrede ilk kez hekime gelir."
        ]),
        make_recall("İnvaziv serviks karsinomu tanısı alan hastaların tıbbi özgeçmişlerindeki en belirgin ortak epidemiyolojik özellik nedir?", "Daha önce hiç Pap smear taraması yaptırmamış veya taramalara çok uzun yıllar ara vermiş olmalarıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Taranmamış Popülasyon", [
            {"text": "İnvaziv serviks kanseri tarama yaptırmamış kadınlarda çok sık görülür.", "isLie": False, "explanation": "Doğru. Majör risk taranmamış olmaktır."},
            {"text": "10-15 yıllık sessiz latent dönem hekime gidilmediği için kaçırılır.", "isLie": False, "explanation": "Doğru. Tarama fırsatı harcanmıştır."},
            {"text": "Haftada 3 kez Pap smear yaptıran kadınlarda ertesi gün %100 ileri evre kanser çıkar.", "isLie": True, "explanation": "Tuzak! Düzenli tarananlarda kanser erken öncülken yakalanır, invaziv kanser gelişimi önlenir."},
            {"text": "Sosyoekonomik yetersizlik tarama eksikliğinde rol oynar.", "isLie": False, "explanation": "Doğru. Önemli bir sosyal belirteçtir."}
        ]),
        make_quiz("İnvaziv serviks karsinomu saptanan hastaların tıbbi geçmişleri incelendiğinde en sık saptanan ortak özellik nedir?", [
            {"key": "A", "text": "Düzenli tarama yaptırmamış veya takiplere uzun yıllar ara vermiş olmak", "isCorrect": True, "explanation": "Taranmamış olmak invaziv kanserlerin en büyük ortak paydasıdır."},
            {"key": "B", "text": "Haftalık rutin kolposkopi yaptırıyor olmak", "isCorrect": False, "explanation": "Aşırı tarananlarda kanser önlenir."},
            {"key": "C", "text": "Dokuz değerlikli aşıyı 4 kez tam doz almış olmak", "isCorrect": False, "explanation": "Aşılananlarda kanser riski düşer."},
            {"key": "D", "text": "Sadece her gün taze balık tüketmek", "isCorrect": False, "explanation": "Beslenme ile tarama ilişkisizdir."}
        ])
    ]
    slides.append(make_slide(72, "Taranmamış Popülasyon Riski ve İhmal Edilmiş Olgular", "Tarama ihmali, sağlık altyapısı eksikliği, kaçırılan 10-15 yıllık pencere ve tanı gecikmesi", "Epidemiyoloji ve Sağlık Eğitimi", s72_narrative, s72_bullets, s72_elements))

    # Slide 73: İleri Evre İnvaziv Karsinomda Klinik Komplikasyonlar
    s73_narrative = (
        "İleri evreye ulaşmış invaziv serviks karsinomunda, tümörün çevre dokulara ve sinirlere "
        "bası yapmasıyla birlikte son derece ağır ve hayatı tehdit edici klinik komplikasyonlar ortaya çıkar.\n\n"
        "- **Şiddetli Pelvik ve Lumbosakral Ağrı:** Tümör retroperitona ve lumbosakral sinir pleksuslarına "
        "(pleksus lumbosakralis) doğrudan infiltre olduğunda, uyluğa ve bacağa yayılan dindirilemeyen **nöropatik ağrılar** başlar.\n"
        "- **Bacakta Tek Taraflı Ödem (Lenfödem):** Kitle veya metastatik lenf nodları iliak lenfatik damarları "
        "ve ana pelvik venleri tamamen tıkayarak alt ekstremitede masif şişliğe ve lenfödeme neden olur.\n"
        "- **Kilo Kaybı ve Kaşeksi:** İlerlemiş tümör yükü, nekroz ve sitokin salımı hastada hızlı tümör kaşeksisi ve anemi tablosu yaratır.\n\n"
        "> [!NOTE]\n"
        "> Lumbosakral sinir infiltrasyonu inatçı bacak ağrısına; pelvik ven ve lenfatik basısı ise alt ekstremitede unilateral masif ödeme yol açar."
    )
    s73_bullets = [
        "Lumbosakral pleksus tutulumu bacağa yayılan şiddetli ağrı yapar.",
        "Pelvik ven ve lenf tıkanması tek taraflı bacak ödemine yol açar.",
        "İlerlemiş tümör yükü ağır kaşeksi ve anemi ile seyreder."
    ]
    s73_elements = [
        make_cloze("Tümörün iliak lenfatikleri ve venleri tıkaması sonucu alt ekstremitede masif lenfödem gelişir.", "lenfödem", "Lenfatik drenaj bozulmasına bağlı bacak şişliği"),
        make_table("İleri Evre Serviks Kanseri Komplikasyonları", ["Etkilenen Yapı", "Fizyopatolojik Süreç", "Klinik Tablo"], [
            {"cells": [{"text": "Lumbosakral Pleksus", "isMasked": False}, {"text": "Derin pelvik nöral infiltrasyon", "isMasked": True, "hint": "sinir köklerine tümör basısı"}, {"text": "Bacağa vuran şiddetli, inatçı siyatalji"}]},
            {"cells": [{"text": "İliak Damarlar", "isMasked": False}, {"text": "Lenfatik ve venöz dönüş obstrüksiyonu", "isMasked": False}, {"text": "Tek taraflı bacakta masif lenfödem", "isMasked": True, "hint": "aşırı bacak şişmesi"}]}
        ]),
        make_chain("İleri Evre Semptom Zinciri", [
            "1. Parametrial Yayılım: Kanser serviks dışına taşarak retroperitona ulaşır.",
            "2. Sinir Pleksusu Basısı: Lumbosakral sinirler tümör kitlesi tarafından sıkıştırılır.",
            "3. Vasküler Bası: İliak ven ve lenf yolları ezilerek sıvı drenajı durur.",
            "4. Ağrı ve Şişlik: Hastada tek taraflı bacak şişmesi ve dindirilemeyen ağrı belirir."
        ]),
        make_recall("İleri evre serviks karsinomlu bir hastada tek taraflı bacakta masif ödem ve bacağa yayılan şiddetli ağrı görülmesinin mekanizması nedir?", "Tümörün lumbosakral sinir pleksusunu infiltre etmesi ve iliak lenfatik/venöz damarları tıkamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İleri Evre Komplikasyonları", [
            {"text": "Lumbosakral pleksus tutulumu bacağa yayılan ağrı yapar.", "isLie": False, "explanation": "Doğru. Sinir basısı siyataljiye yol açar."},
            {"text": "Pelvik lenf ve ven basısı bacakta lenfödeme neden olur.", "isLie": False, "explanation": "Doğru. Drenaj bozukluğu şişlik yapar."},
            {"text": "İleri evre kanser hastalarında bacaklar tamamen havaya uçup kaybolur.", "isLie": True, "explanation": "Tuzak! Bacak kaybolmaz; masif lenfödemle şişer ve ağrılı hale gelir."},
            {"text": "Tümör kaşeksisi ve anemi ileri evreye eşlik eder.", "isLie": False, "explanation": "Doğru. Sistemik tükenme tablosudur."}
        ]),
        make_quiz("İleri evre invaziv serviks kanserinde alt ekstremitede tek taraflı masif ödem gelişmesinin patofizyolojik nedeni nedir?", [
            {"key": "A", "text": "Tümör veya lenf metastazlarının iliak ven ve lenfatikleri tıkaması", "isCorrect": True, "explanation": "Pelvik lenfatik ve venöz tıkanma masif lenfödeme yol açar."},
            {"key": "B", "text": "Hastanın sadece çok fazla şekerli çay içmesi", "isCorrect": False, "explanation": "Beslenme ile lenfödem gelişmez."},
            {"key": "C", "text": "Ayakkabı numarasının yanlış seçilmesi", "isCorrect": False, "explanation": "Onkolojik komplikasyon değildir."},
            {"key": "D", "text": "Yalnızca hafif cilt kuruması", "isCorrect": False, "explanation": "Basit dermatolojik durumdur."}
        ])
    ]
    slides.append(make_slide(73, "İleri Evre İnvaziv Karsinomda Klinik Komplikasyonlar", "Lumbosakral pleksus infiltrasyonu, inatçı ağrı, tek taraflı lenfödem ve tümör kaşeksisi", "İleri Evre Semptomatoloji", s73_narrative, s73_bullets, s73_elements))

    # Slide 74: Terminal Evre ve En Sık Ölüm Nedeni: Üremi
    s74_narrative = (
        "İleri evre ve tedaviye dirençli invaziv serviks karsinomunda hastaların yaşamını kaybetmesine "
        "yol açan mekanizma, pelvik anatomik komşuluklarla doğrudan ilişkilidir.\n\n"
        "- **Üreterlerin Anatomik Komşuluğu:** Üreterler serviksin her iki yanından, parametriumların "
        "içinden geçerek mesaneye ulaşır; servikal tümörün lateral yayılım sahasının tam kalbindedir.\n"
        "- **Bilateral Üreter Basısı:** Lateral parametrial yayılım ve retroperitoneal kitleler her iki üreteri "
        "dışarıdan sıkıştırarak **bilateral üreter obstrüksiyonuna** yol açar.\n"
        "- **Hidronefroz ve Terminal Üremi:** İdrar akımının engellenmesi bilateral hidronefroz, böbrek parankim "
        "atrofisi ve hızla akut-kronik böbrek yetmezliğine yol açar; **üremi invaziv serviks kanserinde en sık "
        "görülen ölüm nedenidir**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İleri evre serviks kanserinde en sık ölüm nedeni, tümörün parametriumlara ve üreterlere bası yaparak bilateral hidronefroz ve terminal üremiye (böbrek yetmezliği) yol açmasıdır."
    )
    s74_bullets = [
        "Tümör parametriumda üreterleri dışarıdan sıkıştırır.",
        "Bilateral üreter obstrüksiyonu şiddetli hidronefroz yapar.",
        "Terminal üremi (böbrek yetmezliği) en sık ölüm nedenidir."
    ]
    s74_elements = [
        make_cloze("İleri evre serviks kanserli hastalarda bilateral hidronefroza bağlı gelişen terminal üremi en sık ölüm nedenidir.", "üremi", "Böbrek yetmezliği sonucu kanda üre birikimi"),
        make_table("Üremiye Gidişin Anatomik ve Klinik Basamakları", ["Basamak", "Patolojik Olay", "Sonuç"], [
            {"cells": [{"text": "Lateral İnvazyon", "isMasked": False}, {"text": "Parametriumdaki üreterlerin tümörle sarılması", "isMasked": True, "hint": "üreter kanalının dıştan basısı"}, {"text": "İdrar pasajında daralma"}]},
            {"cells": [{"text": "Böbrek Parankimi", "isMasked": False}, {"text": "Bilateral hidronefroz ve parankim atrofisi", "isMasked": False}, {"text": "Terminal üremi ve metabolik asidoz", "isMasked": True, "hint": "böbrek yetmezliğine bağlı ölüm"}]}
        ]),
        make_chain("Ölümcül Üremi Mekanizması", [
            "1. Parametrial Yayılım: Serviks kanseri lateral parametrium bağ dokusuna taşar.",
            "2. Üreter Sıkışması: Mesaneye inen her iki üreter tümör kütlesi altında kalır.",
            "3. Bilateral Hidronefroz: İdrar boşalamaz, böbrek pelvisleri şişer ve parankim incelir.",
            "4. Terminal Üremi: Toksinler atılamaz ve hasta metabolik üremi koması ile kaybedilir."
        ]),
        make_recall("İleri evre invaziv serviks kanserli hastalarda en sık karşılaşılan ölüm nedeni nedir ve nasıl gelişir?", "En sık ölüm nedeni üremidir; tümörün üreterleri bilateral sıkıştırarak hidronefroz ve böbrek yetmezliği yapmasıyla gelişir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Serviks Kanserinde Ölüm Nedeni", [
            {"text": "Tümör parametriumda üreterleri dıştan sıkıştırabilir.", "isLie": False, "explanation": "Doğru. Anatomik komşuluk basısıdır."},
            {"text": "Bilateral hidronefroz böbrek yetmezliğine yol açar.", "isLie": False, "explanation": "Doğru. İdrar akımı engellenir."},
            {"text": "Serviks kanserli hastalarda en sık ölüm nedeni ani kalp pili patlamasıdır.", "isLie": True, "explanation": "Tuzak! En sık ölüm nedeni üreter basısına bağlı gelişen terminal üremidir (böbrek yetmezliği)."},
            {"text": "Üremi tablosu ileri evre invaziv serviks kanserinde en sık ölüm nedenidir.", "isLie": False, "explanation": "Doğru. Klasik patoloji spotudur."}
        ]),
        make_quiz("İleri evre invaziv serviks karsinomlu hastalarda en sık görülen ölüm nedeni aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Bilateral üreter obstrüksiyonuna bağlı hidronefroz ve terminal üremi", "isCorrect": True, "explanation": "En sık ölüm nedeni üreter basısı sonucu gelişen üremidir."},
            {"key": "B", "text": "Ani gelişen astım atağı", "isCorrect": False, "explanation": "Solunum alerjisidir."},
            {"key": "C", "text": "Derin uyku sırasında rüya görme", "isCorrect": False, "explanation": "Fizyolojik süreçtir."},
            {"key": "D", "text": "Yalnızca parmak ucu kesiği", "isCorrect": False, "explanation": "Ölümcül değildir."}
        ])
    ]
    slides.append(make_slide(74, "Terminal Evre ve En Sık Ölüm Nedeni: Üremi", "Üreter komşuluğu, bilateral hidronefroz, parankim hasarı ve terminal üremi", "Mortalite ve Terminal Patoloji", s74_narrative, s74_bullets, s74_elements))

    # Slide 75: Mikroinvaziv Karsinom: Tanım ve Tedavi Yaklaşımı
    s75_narrative = (
        "Mikroinvaziv serviks karsinomu, invaziv kanserin başlangıç evresini temsil eden ve invazyon "
        "derinliği mikroskobik milimetrik sınırlarla kesin olarak belirlenmiş özel bir klinik tablodur.\n\n"
        "- **Mikroinvazyon Sınırı:** Stromal invazyon derinliğinin bazal membrandan itibaren **en fazla 3 mm "
        "(veya bazı sınıflamalarda 5 mm)** olduğu ve lateral uzanımının 7 mm'yi aşmadığı odaklardır.\n"
        "- **Lenfatik Risk:** İnvazyon derinliği <3 mm olan ve damar invazyonu (LVSI) bulunmayan olgularda "
        "lenf düğümü metastazı riski **<%1 düzeyindedir**.\n"
        "- **Konservatif Tedavi Şansı:** Bu özellik sayesinde mikroinvaziv karsinom, doğurganlığını korumak isteyen "
        "genç kadınlarda radikal cerrahiye gerek kalmaksızın **geniş konik biyopsi (konizasyon)** ile tam kür sağlanarak tedavi edilebilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Mikroinvaziv serviks karsinomu (stromal derinlik ≤3 mm), lenf nodu riski <%1 olduğu için cerrahi sınırları temiz konik biyopsi ile tedavi edilebilir."
    )
    s75_bullets = [
        "Mikroinvazyon bazal membrandan itibaren ≤3 mm stromal derinliktir.",
        "Lenf nodu metastazı riski <%1 düzeyindedir.",
        "Cerrahi sınırları temiz geniş konik biyopsi ile kür sağlanabilir."
    ]
    s75_elements = [
        make_cloze("Mikroinvaziv serviks karsinomu doğurganlığı korumak amacıyla konik biyopsi ile küratif tedavi edilebilir.", "konik biyopsi", "Mikroinvaziv karsinomda uygulanan organ koruyucu cerrahi"),
        make_table("Mikroinvaziv Karsinom Kriterleri", ["Ölçüt", "Kabul Edilen Eşik", "Klinik Tedaviye Etkisi"], [
            {"cells": [{"text": "Stromal İnvazyon Derinliği", "isMasked": False}, {"text": "En fazla 3 mm (≤3 mm)", "isMasked": True, "hint": "mikroskobik derinlik sınırı"}, {"text": "Lenf nodu metastaz riski <%1"}]},
            {"cells": [{"text": "Uygulanan Tedavi", "isMasked": False}, {"text": "Konik biyopsi (organ koruyucu)", "isMasked": False}, {"text": "Fertilite (doğurganlık) korunabilir", "isMasked": True, "hint": "rahmin korunabilme şansı"}]}
        ]),
        make_chain("Mikroinvazyon Tedavi Karar Yolu", [
            "1. Konizasyon Piyesi: Konik biyopsi seri kesitlerle milimetrik taranır.",
            "2. Derinlik Ölçümü: Patolog invazyon derinliğinin 2 mm olduğunu ve LVSI olmadığını belgeler.",
            "3. Sınır Kontrolü: Cerrahi sınırlarda tümör bulunmadığı doğrulanır.",
            "4. Fertilite Korunması: Radikal histerektomiye gerek kalmadan hasta güvenle izleme alınır."
        ]),
        make_recall("Mikroinvaziv serviks karsinomunun derinlik sınırı nedir ve genç hastalarda hangi yöntemle tedavi edilebilir?", "Stromal derinlik ≤3 mm'dir; cerrahi sınırları temiz konik biyopsi ile tedavi edilebilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Mikroinvaziv Karsinom", [
            {"text": "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.", "isLie": False, "explanation": "Doğru. Erken evrede konizasyon yeterlidir."},
            {"text": "Lenf nodu metastazı riski bu evrede son derece düşüktür (<%1).", "isLie": False, "explanation": "Doğru. Düşük invazyon derinliğidir."},
            {"text": "Mikroinvaziv karsinom tüm serviksi yutmuş 15 kilogramlık bir kitle demektir.", "isLie": True, "explanation": "Tuzak! Mikroinvaziv karsinom gözle görülmeyen, sadece mikroskopta ≤3 mm saptanan odaktır."},
            {"text": "Cerrahi sınırların temiz olması tedavide şarttır.", "isLie": False, "explanation": "Doğru. Rezeksiyon tam olmalıdır."}
        ]),
        make_quiz("Mikroinvaziv serviks karsinomunun klinik tedavisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Konik biyopsi ile başarıyla tedavi edilebilir", "isCorrect": True, "explanation": "Mikroinvaziv karsinom konik biyopsi ile küratif tedavi edilebilir."},
            {"key": "B", "text": "Tek çare hastanın derhal uyutularak dondurulmasıdır", "isCorrect": False, "explanation": "Tıbbi geçerliliği yoktur."},
            {"key": "C", "text": "Hiçbir tedavi yapılamayan terminal bir durumdur", "isCorrect": False, "explanation": "En erken ve en kolay tedavi edilen evredir."},
            {"key": "D", "text": "Zorunlu olarak kalp ve akciğer nakli gerektirir", "isCorrect": False, "explanation": "Organ nakli endikasyonu yoktur."}
        ])
    ]
    slides.append(make_slide(75, "Mikroinvaziv Karsinom: Tanım ve Tedavi Yaklaşımı", "≤3 mm stromal invazyon derinliği, <%1 lenf riski, konik biyopsi ve fertilite korunması", "Erken İnvaziv Yönetim", s75_narrative, s75_bullets, s75_elements))

    # Slide 76: Cerrahi Tedavi: Histerektomi ve Lenf Disseksiyonu
    s76_narrative = (
        "Mikroinvaziv sınırı aşmış, ancak pelvik yan duvarlara fikse olmamış erken evre invaziv serviks "
        "karsinomlarında (Evre IB - IIA) standart primer tedavi cerrahidir.\n\n"
        "- **Radikal Histerektomi (Wertheim Cerrahisi):** Uterus, serviks, parametriumlar ve vajinanın "
        "üst 1/3'lük kısmı tek parça halinde geniş cerrahi sınırlarla çıkarılır.\n"
        "- **Bilateral Pelvik Lenf Düğümü Disseksiyonu:** Obturator, eksternal iliak, internal iliak ve ana iliak "
        "lenf istasyonları metastaz yönünden sistematik olarak temizlenir (diseke edilir).\n"
        "- **Patolojik Evreleme:** Çıkarılan piyesteki tümör boyutu, invazyon derinliği ve lenf nodu tutulum "
        "durumu hastanın ek adjuvan tedavi (kemoradyoterapi) alıp almayacağını belirler.\n\n"
        "> [!NOTE]\n"
        "> Erken evre invaziv karsinomun primer cerrahi tedavisi radikal histerektomi ve pelvik lenf düğümü diseksiyonudur."
    )
    s76_bullets = [
        "Primer cerrahi tedavi radikal histerektomidir.",
        "Pelvik lenf düğümü diseksiyonu standart olarak eklenir.",
        "Çıkarılan lenf nodları patolojik evrelemeyi kesinleştirir."
    ]
    s76_elements = [
        make_cloze("Erken evre invaziv serviks kanserinde uygulanan geniş cerrahiye radikal histerektomi adı verilir.", "radikal histerektomi", "Parametriumları ve üst vajeni de içeren rezeksiyon"),
        make_table("Cerrahi Tedavi Bileşenleri", ["Cerrahi Bileşen", "Çıkarılan Dokular", "Cerrahi Amaç"], [
            {"cells": [{"text": "Radikal Histerektomi", "isMasked": False}, {"text": "Uterus, serviks, parametrium ve üst vajen", "isMasked": True, "hint": "primer kitle ve çevre bağ dokusu"}, {"text": "Primer tümör odağını geniş sınırla temizlemek"}]},
            {"cells": [{"text": "Pelvik Lenf Disseksiyonu", "isMasked": False}, {"text": "İliak ve obturator lenf düğümleri", "isMasked": False}, {"text": "Metastatik istasyonları temizlemek ve evrelemek", "isMasked": True, "hint": "nodal metastaz kontrolü"}]}
        ]),
        make_chain("Radikal Cerrahi Basamakları", [
            "1. Laparatomi/Laparoskopi: Batına girilerek retroperitoneal boşluklar açılır.",
            "2. Damar İzolasyonu: Uterin arter ve venler orijininden bağlanarak kesilir.",
            "3. Parametrium Rezeksiyonu: Uterusu tutan pelvik bağ dokusu genişçe eksize edilir.",
            "4. Lenfadenektomi: Tüm iliak-obturator lenf zincirleri toplanarak patolojiye gönderilir."
        ]),
        make_recall("Erken evre invaziv serviks karsinomunda uygulanan standart primer cerrahi yaklaşım nedir?", "Radikal histerektomi ve bilateral pelvik lenf düğümü diseksiyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Cerrahi Tedavi", [
            {"text": "Primer tedavi histerektomi ve pelvik lenf düğümü diseksiyonudur.", "isLie": False, "explanation": "Doğru. Standart cerrahi protokoldür."},
            {"text": "Radikal cerrahide parametriumlar da çıkarılır.", "isLie": False, "explanation": "Doğru. Geniş doku bloğu alınır."},
            {"text": "Cerrahi sırasında hastanın her iki göz küresi de mutlaka çıkarılmalıdır.", "isLie": True, "explanation": "Tuzak! Gözle hiçbir ilgisi yoktur; cerrahi pelviste uterus ve lenf nodlarına yapılır."},
            {"text": "Patoloji lenf tutulumunu evrelemede kullanır.", "isLie": False, "explanation": "Doğru. Nodal durum prognostiktir."}
        ]),
        make_quiz("Erken evre invaziv serviks karsinomunun primer tedavisinde uygulanan cerrahi yaklaşım aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Histerektomi ve pelvik lenf düğümü diseksiyonu", "isCorrect": True, "explanation": "Radikal histerektomi ve pelvik lenfadenektomi standarttır."},
            {"key": "B", "text": "Yalnızca bademcik ameliyatı (tonsillektomi)", "isCorrect": False, "explanation": "Faringeal cerrahidir."},
            {"key": "C", "text": "Sadece apandisitin çıkarılması", "isCorrect": False, "explanation": "Gastrointestinal cerrahidir."},
            {"key": "D", "text": "Hastaya cerrahi yerine sadece tatlı ikram edilmesi", "isCorrect": False, "explanation": "Tıbbi yaklaşım değildir."}
        ])
    ]
    slides.append(make_slide(76, "Cerrahi Tedavi: Histerektomi ve Lenf Disseksiyonu", "Radikal histerektomi, Wertheim operasyonu, parametrektomi ve pelvik lenfadenektomi", "Primer Cerrahi Onkoloji", s76_narrative, s76_bullets, s76_elements))

    # Slide 77: İleri Evrede Tedavi: Radyoterapi ve Kemoterapi
    s77_narrative = (
        "Tümör parametriumların dış kısımlarına yayıldığında, pelvik yan duvara fikse olduğunda "
        "veya komşu organları (mesane/rektum) tuttuğunda cerrahi uygulanabilirlik (rezektabilite) sınırları aşılır.\n\n"
        "- **Kombine Kemoradyoterapi:** Bu ileri evre olgularda (Evre IIB ve üzeri) küratif şans sunan "
        "standart yaklaşım **eşzamanlı radyoterapi ve kemoterapi (kemoradyoterapi)** kombinasyonudur.\n"
        "- **Brakiterapi (İç Işınlama):** Eksternal pelvik radyoterapiye ek olarak servikal kavite içine "
        "radyoaktif kaynaklar yerleştirilerek tümör yatağına yüksek doz lokal radyasyon verilir.\n"
        "- **Radyoduyarlaştırıcı Kemoterapi:** Haftalık uygulanan düşük doz **Sisplatin** kemoterapisi, "
        "kanser hücrelerini radyasyona karşı aşırı duyarlı hale getirerek lokal tümör kontrolünü artırır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İleri evre invaziv serviks karsinomunda cerrahi yerine radyoterapi ve kemoterapi (kemoradyoterapi) kombinasyonu standart tedavidir."
    )
    s77_bullets = [
        "İleri evre olgularda cerrahi sınır aşılmıştır.",
        "Standart tedavi radyoterapi ve kemoterapi kombinasyonudur.",
        "Sisplatin radyoduyarlaştırıcı ajan olarak kullanılır."
    ]
    s77_elements = [
        make_cloze("İleri evre serviks karsinomunda cerrahi yerine uygulanan kombine yaklaşıma kemoradyoterapi adı verilir.", "kemoradyoterapi", "Kemoterapi ve radyoterapinin eşzamanlı verilmesi"),
        make_table("İleri Evre Onkolojik Tedavi Bileşenleri", ["Modalite", "Uygulama Şekli", "Radyasyon / Onkolojik Amaç"], [
            {"cells": [{"text": "Eksternal Radyoterapi", "isMasked": False}, {"text": "Tüm pelvise dışarıdan ışınlama", "isMasked": True, "hint": "pelvik lenf ve kitle ışınlaması"}, {"text": "Bölgesel kitle ve lenf nodu kontrolü"}]},
            {"cells": [{"text": "Brakiterapi", "isMasked": False}, {"text": "Servikal kaviteye radyoaktif implant", "isMasked": False}, {"text": "Tümör odağına yüksek doz hedefe atış", "isMasked": True, "hint": "içeriden yüksek doz lokal ışın"}]}
        ]),
        make_chain("Kemoradyoterapi Süreci", [
            "1. İnoperabilite Tespiti: Parametrial invazyon ve fiksasyon cerrahiyi eler.",
            "2. Eksternal Işınlama: 5 hafta boyunca fraksiyone pelvik radyoterapi verilir.",
            "3. Sisplatin İnfüzyonu: Haftalık eşzamanlı kemoterapi hücreleri ışına duyarlı kılar.",
            "4. Brakiterapi: Serviks içine aplikatör takılarak tedavi yüksek dozla tamamlanır."
        ]),
        make_recall("İleri evre (ameliyat şansı olmayan) invaziv serviks kanserinde uygulanan standart onkolojik tedavi nedir?", "Eşzamanlı radyoterapi ve kemoterapi (kemoradyoterapi) kombinasyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İleri Evre Tedavi", [
            {"text": "İleri evre olgularda radyoterapi ve kemoterapi kombinasyonu uygulanır.", "isLie": False, "explanation": "Doğru. Standart kemoradyoterapidir."},
            {"text": "Brakiterapi serviks içine radyoaktif kaynak yerleştirilmesidir.", "isLie": False, "explanation": "Doğru. Lokal iç ışınlamadır."},
            {"text": "İleri evre kanser hastalarına sadece günde 10 saat güneşlenmeleri söylenir.", "isLie": True, "explanation": "Tuzak! Güneşlenme tedavi değildir; kemoradyoterapi gibi yoğun onkolojik protokoller gerekir."},
            {"text": "Sisplatin kemoterapisi radyoduyarlaştırıcı olarak eklenir.", "isLie": False, "explanation": "Doğru. Etkinliği belirgin artırır."}
        ]),
        make_quiz("İleri evre serviks karsinomlu hastalarda primer tedavi yaklaşımı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Radyoterapi ve kemoterapi kombinasyonu", "isCorrect": True, "explanation": "İleri evrede kemoradyoterapi standarttır."},
            {"key": "B", "text": "Yalnızca aspiratör ile burun temizliği", "isCorrect": False, "explanation": "İlgisizdir."},
            {"key": "C", "text": "Sadece ayak tırnaklarının kesilmesi", "isCorrect": False, "explanation": "Tedavi değildir."},
            {"key": "D", "text": "Hiçbir şey yapmadan beklemek", "isCorrect": False, "explanation": "Tedavi gereklidir."}
        ])
    ]
    slides.append(make_slide(77, "İleri Evrede Tedavi: Radyoterapi ve Kemoterapi", "Kemoradyoterapi, eksternal radyasyon, intrakaviter brakiterapi ve sisplatin protokolü", "İleri Evre Onkolojik Tedavi", s77_narrative, s77_bullets, s77_elements))

    # Slide 78: Prognoz Belirleyicileri: Evre, Nodal Durum ve Histoloji
    s78_narrative = (
        "İnvaziv serviks karsinomlu bir hastanın yaşam süresini ve tedavi başarısını belirleyen "
        "en kritik prognostik faktörler patolojik ve klinik parametrelerle ölçülür.\n\n"
        "- **Klinik Evre (FIGO Evresi):** Prognozu belirleyen **en güçlü bağımsız faktördür**; lezyonun "
        "servikse sınırlı olması (Evre I) ile uzak metastaz yapması (Evre IV) arasında sağkalım %90'dan %15'e düşer.\n"
        "- **Pelvik Lenf Nodu Tutulumu:** Lenf nodlarında metastaz varlığı sağkalım oranını yarı yarıya "
        "düşürür; paraaortik nod tutulumu ise prognozu çok daha dramatik bozar.\n"
        "- **Tümör Boyutu ve Histolojik Tip:** 4 cm'den büyük tümörler ve **küçük hücreli nöroendokrin "
        "histoloji** son derece olumsuz prognostik faktörlerdir.\n\n"
        "> [!NOTE]\n"
        "> Evre, tümör boyutu, invazyon derinliği, lenf nodu durumu ve histolojik tip prognozu belirleyen en önemli kriterlerdir."
    )
    s78_bullets = [
        "Klinik evre prognozu belirleyen en güçlü faktördür.",
        "Pelvik lenf nodu metastazı sağkalımı yarı yarıya azaltır.",
        "Küçük hücreli histoloji ve büyük tümör hacmi prognozu kötüleştirir."
    ]
    s78_elements = [
        make_cloze("Serviks kanserinde prognozu belirleyen en güçlü bağımsız klinik parametre tümörün evresidir.", "evresi", "FIGO sınıflamasına dayanan yayılım derecesi"),
        make_table("Prognostik Faktörler ve Sağkalım Etkisi", ["Faktör", "İyi Prognostik Gösterge", "Kötü Prognostik Gösterge"], [
            {"cells": [{"text": "Klinik FIGO Evresi", "isMasked": False}, {"text": "Evre I (servikse sınırlı)", "isMasked": True, "hint": "erken lokalize evre"}, {"text": "Evre III-IV (duvar tutulumu/metastaz)"}]},
            {"cells": [{"text": "Lenf Nodu Durumu", "isMasked": False}, {"text": "Tüm lenf nodları negatif", "isMasked": False}, {"text": "Pozitif pelvik veya paraaortik nodlar", "isMasked": True, "hint": "metastatik lenfatik tutulum"}]}
        ]),
        make_chain("Prognostik Ayrım Mantığı", [
            "1. Evreleme: Kitle boyutu ve komşu organ yayılımı taranır.",
            "2. Cerrahi Örnekleme: Çıkarılan 25 pelvik lenf nodu mikroskopta taranır.",
            "3. Negatif Rapor: Nodlar temizse hastanın 5 yıllık sağkalımı %90 civarındadır.",
            "4. Pozitif Rapor: Nod metastazı varsa relaps riski katlanır ve adjuvan tedavi verilir."
        ]),
        make_recall("İnvaziv serviks karsinomunda hastanın 5 yıllık sağkalımını ve prognozunu belirleyen en güçlü tek faktör nedir?", "Hastalığın klinik evresidir (FIGO evresi)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Prognoz Belirleyicileri", [
            {"text": "Klinik evre prognozu belirleyen en önemli parametredir.", "isLie": False, "explanation": "Doğru. En güçlü bağımsız belirteçtir."},
            {"text": "Lenf nodu metastazı sağkalımı belirgin biçimde düşürür.", "isLie": False, "explanation": "Doğru. Nodal tutulum prognozu bozar."},
            {"text": "Evre IV metastatik kanser hastalarında 5 yıllık sağkalım %1000'dir.", "isLie": True, "explanation": "Tuzak! Evre IV'te sağkalım düşüktür (<%15-20); %1000 gibi bir oran imkansızdır."},
            {"text": "Küçük hücreli nöroendokrin karsinom kötü prognoz göstergesidir.", "isLie": False, "explanation": "Doğru. En agresif histolojidir."}
        ]),
        make_quiz("İnvaziv serviks karsinomunda prognozu ve sağkalım oranını en güçlü şekilde belirleyen faktör aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Hastalığın klinik evresi ve lenf nodu tutulum durumu", "isCorrect": True, "explanation": "Evre ve lenf nodu metastazı en kritik belirteçlerdir."},
            {"key": "B", "text": "Hastanın en sevdiği müzik türü", "isCorrect": False, "explanation": "Biyolojik etkisi yoktur."},
            {"key": "C", "text": "Hastanenin bulunduğu caddenin genişliği", "isCorrect": False, "explanation": "Alakasızdır."},
            {"key": "D", "text": "Ameliyatın yapıldığı günün haftanın hangi günü olduğu", "isCorrect": False, "explanation": "Günün prognoza etkisi yoktur."}
        ])
    ]
    slides.append(make_slide(78, "Prognoz Belirleyicileri: Evre, Nodal Durum ve Histoloji", "FIGO evrelemesi, pelvik/paraaortik lenf nodu tutulumu, kitle boyutu ve sağkalım oranları", "Prognostik Faktörler", s78_narrative, s78_bullets, s78_elements))

    # Slide 79: Erken Tanı ve Taramaların Hayati Rolü
    s79_narrative = (
        "İnvaziv serviks karsinomunun tedavi başarısı, tamamen hastalığın teşhis edildiği andaki yayılım "
        "derecesi ile sınırlıdır.\n\n"
        "- **Erken Evrede Başarı:** Tarama ile preinvaziv lezyon (CIN) veya Evre I mikroinvaziv düzeyde "
        "yakalanan olgularda **tedavi başarısı ve tam kür oranı %95-100'e** ulaşmaktadır.\n"
        "- **İleri Evrede Çaresizlik:** Olgular ihmal edilip fıçı serviks, pelvik fiksasyon ve üremi "
        "komplikasyonları geliştikten sonra yakalandığında, en modern kemoradyoterapiye rağmen mortalite son derece yüksektir.\n"
        "- **Yaşamsal İlke:** ==Erken tanı ve tarama programları yaşamsal öneme sahiptir==; serviks kanseri "
        "tedavi edilmekten ziyade taranarak önlenmesi gereken bir hastalıktır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Erken tanı ve düzenli tarama programları serviks kanserinde mortaliteyi önlemede en yaşamsal ve vazgeçilmez unsurdur."
    )
    s79_bullets = [
        "Erken evrede yakalanan karsinomda tam kür oranı %95-100'dür.",
        "İleri evreye geçildiğinde mortalite dramatik biçimde artar.",
        "Erken tanı ve tarama programları yaşamsal öneme sahiptir."
    ]
    s79_elements = [
        make_cloze("Serviks kanserinde mortaliteyi düşürmede en yaşamsal unsur organize tarama programlarıdır.", "tarama", "Hastalığı preinvaziv evrede yakalayan koruyucu sistem"),
        make_table("Evrelere Göre Tedavi Başarısı", ["Yakalanma Zamanı", "Uygulanan Tedavi", "Kür Oranı"], [
            {"cells": [{"text": "Preinvaziv (CIN) / Mikroinvaziv", "isMasked": False}, {"text": "Basit konik biyopsi / LEEP", "isMasked": True, "hint": "organ koruyucu eksizyon"}, {"text": "%95 - %100 tam şifa"}]},
            {"cells": [{"text": "İleri İnvaziv Evre (Evre III/IV)", "isMasked": False}, {"text": "Ağır kemoradyoterapi protokolleri", "isMasked": False}, {"text": "Düşük sağkalım ve yüksek mortalite riski", "isMasked": True, "hint": "kür şansının azalması"}]}
        ]),
        make_chain("Erken Tanının Hayat Kurtarma Zinciri", [
            "1. Taramaya Katılım: Sağlıklı kadın 3-5 yılda bir kontrole gider.",
            "2. Erken Teşhis: Kanser henüz milimetrik mikroinvaziv evrede yakalanır.",
            "3. Basit Cerrahi: Küçük bir eksizyonla tümör tamamen temizlenir.",
            "4. Tam Yaşam: Hasta kanserden tamamen kurtularak sağlıklı ömrünü sürdürür."
        ]),
        make_recall("Serviks kanseri ile mücadelede mortaliteyi engellemenin ve tam şifa sağlamanın en temel anahtarı nedir?", "Erken tanı ve organize düzenli tarama programlarıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erken Tanının Önemi", [
            {"text": "Erken tanı ve tarama programları yaşamsal öneme sahiptir.", "isLie": False, "explanation": "Doğru. En kritik halk sağlığı ilkesidir."},
            {"text": "Erken yakalanan lezyonlarda tedavi başarısı çok yüksektir.", "isLie": False, "explanation": "Doğru. %95-100 kür sağlanır."},
            {"text": "Serviks kanserini erken yakalamak hastanın hemen ölmesine yol açar.", "isLie": True, "explanation": "Tuzak! Erken yakalamak tam kür sağlar ve hayat kurtarır."},
            {"text": "İleri evrede sağkalım oranları belirgin biçimde düşer.", "isLie": False, "explanation": "Doğru. Prognoz kötüleşir."}
        ]),
        make_quiz("Serviks kanserinde erken tanı ve tarama programlarının klinik değeri aşağıdakilerden hangisinde en doğru özetlenmiştir?", [
            {"key": "A", "text": "Erken tanı ve tarama programları tam kür sağlayarak yaşamsal öneme sahiptir", "isCorrect": True, "explanation": "Erken tanı ve tarama hayat kurtarır ve %100'e yakın kür sunar."},
            {"key": "B", "text": "Tarama yapmak hastalığı daha kötü hale getirir", "isCorrect": False, "explanation": "Tarama hayat kurtarır."},
            {"key": "C", "text": "Taramaların sağkalıma hiçbir etkisi olmamıştır", "isCorrect": False, "explanation": "Mortaliteyi %75 düşürmüştür."},
            {"key": "D", "text": "Sadece erkeklerde uygulanan bir yöntemdir", "isCorrect": False, "explanation": "Kadın serviks kanseri taramasıdır."}
        ])
    ]
    slides.append(make_slide(79, "Erken Tanı ve Taramaların Hayati Rolü", "Preinvaziv kür oranları (%95-100), ileri evre mortalitesi, taramanın koruyucu zaferi", "Koruyucu Onkoloji İlkeleri", s79_narrative, s79_bullets, s79_elements))

    # Slide 80: [TEKRAR SAYFASI - CHECKPOINT 8] Klinik Prezentasyon, Komplikasyonlar ve Tedavi
    s80_narrative = (
        "Bölüm 8'de invaziv serviks karsinomunun klinik prezentasyonunu, ölümcül üremi komplikasyonunu, "
        "mikroinvaziv cerrahiyi ve ileri evre kemoradyoterapi protokollerini bütünleştirdik.\n\n"
        "- **Klinik Prezentasyon:** En sık görülen belirti **beklenmedik vajinal kanamadır** (özellikle postkoital). "
        "Hastaların büyük çoğunluğu daha önce **hiç taranmamış** ihmal edilmiş olgulardır.\n"
        "- **En Sık Ölüm Nedeni:** Tümörün parametriumda üreterlere bası yapması sonucu gelişen "
        "**bilateral hidronefroz ve terminal üremi (böbrek yetmezliği)** en sık ölüm nedenidir.\n"
        "- **Mikroinvaziv vs İleri Tedavi:** Mikroinvaziv karsinom (≤3 mm) lenf nodu riski <%1 olduğundan "
        "**konik biyopsi ile tedavi edilebilir**; erken invaziv karsinomda radikal histerektomi + lenf nodu diseksiyonu, "
        "ileri evrede ise **kemoradyoterapi** uygulanır.\n"
        "- **Altın Kural:** Erken tanı ve tarama programları yaşamsal öneme sahiptir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 8 SENTEZİ] En sık semptom vajinal kanamadır; en sık ölüm nedeni üreter basısına bağlı üremidir; mikroinvaziv kanser konik biyopsi ile kür olurken, ileri evrede kemoradyoterapi şarttır."
    )
    s80_bullets = [
        "En sık semptom beklenmedik/postkoital vajinal kanamadır.",
        "En sık ölüm nedeni bilateral üreter basısına bağlı terminal üremidir.",
        "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.",
        "İleri evrede kemoradyoterapi uygulanır; tarama programları yaşamsaldır."
    ]
    s80_elements = [
        make_cloze("İleri evre serviks karsinomlu hastalarda en sık ölüm nedeni bilateral üreter basısına bağlı terminal üremi tablosudur.", "üremi", "Bölüm 8 checkpointinde pekiştirilen ölümcül komplikasyon"),
        make_table("Bölüm 8 Klinik ve Tedavi Sentez Tablosu", ["Klinik Başlık", "Temel Tanım / Mekanizma", "Tedavi / Sonuç"], [
            {"cells": [{"text": "En Sık Belirti", "isMasked": False}, {"text": "Beklenmedik postkoital vajinal kanama", "isMasked": True, "hint": "temasla tetiklenen kanama"}, {"text": "Hastanın hekime başvurmasını sağlar"}]},
            {"cells": [{"text": "En Sık Ölüm Nedeni", "isMasked": False}, {"text": "Üreter basısına bağlı terminal üremi", "isMasked": False}, {"text": "Bilateral hidronefroz ve renal iflas", "isMasked": True, "hint": "böbrek yetmezliği komplikasyonu"}]},
            {"cells": [{"text": "Mikroinvaziv Karsinom", "isMasked": False}, {"text": "≤3 mm stromal derinlik, <%1 lenf riski", "isMasked": False}, {"text": "Konik biyopsi ile küratif tedavi", "isMasked": True, "hint": "organ koruyucu cerrahi kür"}]}
        ]),
        make_chain("Bölüm 8 Süreç Entegrasyonu", [
            "1. Başvuru: Hasta ilişki sonrası taze vajinal kanama ile polikliniğe gelir.",
            "2. Evreleme: Eğer mikroinvazivse konizasyonla kür sağlanır; ileri evreyse kemoradyoterapiye alınır.",
            "3. İhmal Edilirse: Tümör parametriumda üreterleri boğarak hidronefroz yapar.",
            "4. Yaşamsal Ders: Bu fatal tabloyu önlemenin tek yolu organize taramadır."
        ]),
        make_recall("Bölüm 8 boyunca öğrendiğimiz: (1) En sık semptom, (2) En sık ölüm nedeni ve (3) Mikroinvaziv karsinomun cerrahi tedavisi nedir?", "(1) Beklenmedik vajinal kanama, (2) Terminal üremi, (3) Konik biyopsidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 8 Checkpoint Sentezi", [
            {"text": "En sık klinik semptom beklenmedik vajinal kanamadır.", "isLie": False, "explanation": "Doğru. Klasik başvuru bulgusudur."},
            {"text": "En sık ölüm nedeni üreter basısına bağlı terminal üremidir.", "isLie": False, "explanation": "Doğru. Majör fatal nedendir."},
            {"text": "Mikroinvaziv karsinomda hastaya mutlaka tüm organlarının çıkarılması gerekir.", "isLie": True, "explanation": "Tuzak! Mikroinvaziv karsinom konik biyopsi ile basitçe tedavi edilebilir."},
            {"text": "İleri evrede cerrahi yerine radyoterapi ve kemoterapi uygulanır.", "isLie": False, "explanation": "Doğru. Kemoradyoterapi standarttır."}
        ]),
        make_quiz("Bölüm 8'de pekiştirilen klinik ve tedavi ilkelerine göre aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Mikroinvaziv karsinom - Konik biyopsi ile tedavi edilebilir", "isCorrect": True, "explanation": "Mikroinvaziv karsinom konik biyopsi ile kür olabilir."},
            {"key": "B", "text": "En sık ölüm nedeni - İki taraflı kulak zarı patlaması", "isCorrect": False, "explanation": "En sık ölüm nedeni üremidir."},
            {"key": "C", "text": "En sık semptom - Avuç içinde kıllanma", "isCorrect": False, "explanation": "En sık semptom vajinal kanamadır."},
            {"key": "D", "text": "İleri evre tedavi - Sadece soğuk su banyosu", "isCorrect": False, "explanation": "Kemoradyoterapi gerekir."}
        ])
    ]
    slides.append(make_slide(80, "[TEKRAR SAYFASI - CHECKPOINT 8] Klinik Prezentasyon, Komplikasyonlar ve Tedavi", "Bölüm 8 kapsamlı tekrarı: kanama semptomu, üremi ölümü, mikroinvaziv konizasyon ve kemoradyoterapi", "Bölüm Tekrarı ve Konsolidasyon", s80_narrative, s80_bullets, s80_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec8()
    print(f"Sec8 generated: {len(slides)} slides (Slide 71 to 80)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
