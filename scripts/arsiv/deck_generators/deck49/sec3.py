import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec3():
    slides = []

    # Slide 21: HPV Virolojik Yapısı ve Çift İplikli DNA Genomu
    s21_narrative = (
        "Human Papilloma Virus (HPV), Papillomaviridae familyasına ait olan, zarfsız ve çift iplikli "
        "dairesel DNA genomuna sahip bir DNA virüsüdür. Servikal kanserin primer etiyolojik ajanıdır.\n\n"
        "- **Viral Kapsid ve Dayanıklılık:** Dış lipid zarfı bulunmadığından dolayı çevresel fiziksel ve kimyasal "
        "etkenlere, kuruluğa ve deterjanlara karşı oldukça dirençlidir; bulaşma kolaylığı sağlar.\n"
        "- **Genomik Organizasyon:** Yaklaşık 8000 baz çiftinden oluşan genomu erken genleri (E1-E8) ve "
        "geç yapısal kapsid proteinlerini kodlayan L1 ve L2 genlerini barındırır.\n"
        "- **Hücresel Hedef:** HPV, çok katlı skuamöz epitelin derinlerinde bulunan çoğalma yeteneğindeki "
        "bazal tabaka kök hücrelerini enfekte eder.\n\n"
        "> [!NOTE]\n"
        "> HPV bir DNA virüsüdür; zarsız kapsidi ve çift iplikli dairesel DNA genomu ile karakterizedir."
    )
    s21_bullets = [
        "Zarfsız, ikozahedral simetrili bir DNA virüsüdür.",
        "Genomu çift iplikli dairesel DNA'dan meydana gelir.",
        "Epitelin bazal tabakasındaki prolifere olabilen hücreleri enfekte eder."
    ]
    s21_elements = [
        make_cloze("Human Papilloma Virus genomik yapı olarak çift iplikli dairesel DNA virüsüdür.", "DNA", "Virüsün nükleik asit molekül tipi"),
        make_table("HPV Virolojik Mimarisi", ["Özellik", "Yapısal Karakter", "Biyolojik Fonksiyon"], [
            {"cells": [{"text": "Zarf Durumu", "isMasked": False}, {"text": "Zarfsız ikozahedral kapsid", "isMasked": True, "hint": "lipid örtüsü bulunmayan kapsid"}, {"text": "Çevresel faktörlere yüksek direnç"}]},
            {"cells": [{"text": "Genom Tipi", "isMasked": False}, {"text": "Çift iplikli dairesel nükleik asit", "isMasked": False}, {"text": "Konak çekirdeğinde replike olur", "isMasked": True, "hint": "nükleer çoğalma süreci"}]}
        ]),
        make_chain("HPV Hücresel Giriş Basamakları", [
            "1. Mukozal Mikrotravma: Cinsel temas veya sürtünme epitelde mikro-çatlaklar açar.",
            "2. Bazal Hücre Teması: Zarfsız virionlar doğrudan bazal membrandaki kök hücrelere ulaşır.",
            "3. Endositoz: Virüs hücre yüzeyindeki heparan sülfat reseptörlerine bağlanarak içeri alınır.",
            "4. Nükleer Taşınma: Viral DNA serbest kalarak çekirdeğe girer ve replikasyon programını başlatır."
        ]),
        make_recall("HPV'nin temel genetik ve yapısal sınıflandırması nedir?", "Zarfsız, çift iplikli dairesel bir DNA virüsüdür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Virolojisi", [
            {"text": "HPV çift iplikli dairesel bir DNA virüsüdür.", "isLie": False, "explanation": "Doğru. Papillomaviridae ailesine ait DNA virüsüdür."},
            {"text": "Zarfsız kapsidi sayesinde dış çevre koşullarına karşı oldukça dayanıklıdır.", "isLie": False, "explanation": "Doğru. Lipid zarfı yoktur, deterjanlara dirençlidir."},
            {"text": "HPV tek iplikli negatif polariteli bir RNA virüsüdür ve akciğer alveollerini enfekte eder.", "isLie": True, "explanation": "Tuzak! HPV bir RNA virüsü değil, çift iplikli DNA virüsüdür ve mukokutanöz epiteli enfekte eder."},
            {"text": "Hücresel hedefi çok katlı yassı epitelin bazal tabakasındaki hücrelerdir.", "isLie": False, "explanation": "Doğru. Çoğalan bazal hücrelere mikrotravmayla ulaşır."}
        ]),
        make_quiz("HPV'nin temel virolojik yapısı ile ilgili aşağıdaki seçeneklerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Zarfsız, çift iplikli dairesel bir DNA virüsüdür", "isCorrect": True, "explanation": "HPV zarfsız, çift iplikli dairesel DNA virüsüdür."},
            {"key": "B", "text": "Hücre çekirdeği bulunmayan bir protozoon parazitidir", "isCorrect": False, "explanation": "Virüstür, parazit değildir."},
            {"key": "C", "text": "Zarfında ters transkriptaz taşıyan bir retrovirüstür", "isCorrect": False, "explanation": "Retrovirüs değildir, DNA virüsüdür."},
            {"key": "D", "text": "Gram negatif spor oluşturan bir basildir", "isCorrect": False, "explanation": "Bakteri değil virüstür."}
        ])
    ]
    slides.append(make_slide(21, "HPV Virolojik Yapısı ve Çift İplikli DNA Genomu", "Zarfsız kapsid, çift iplikli dairesel DNA, bazal hücre afinitesi", "HPV Virolojisi", s21_narrative, s21_bullets, s21_elements))

    # Slide 22: HPV Onkojenik Risk Ayrımı: Yüksek ve Düşük Risk
    s22_narrative = (
        "Human Papilloma Virus genotipleri, servikal ve anogenital epitelde displazi ve malignite "
        "oluşturma potansiyellerine göre iki temel kategoriye ayrılır.\n\n"
        "- **Yüksek Onkojenik Riskli Tipler:** Başta **HPV 16 ve HPV 18** olmak üzere (ayrıca 31, 33, 45, 52, 58 vb.) "
        "karsinom gelişiminde doğrudan rol oynayan tiplerdir. Serviks, vajina, vulva, penis, anüs ve orofarenks kanserlerine yol açarlar.\n"
        "- **Düşük Onkojenik Riskli Tipler:** En sık karşılaşılanları **HPV 6 ve HPV 11**'dir. Bunlar kanser oluşturmaz; "
        "benign genital siğiller (kondiloma aküminata) ve laringeal papillomlara neden olurlar.\n"
        "- **Klinik Yaklaşım:** Genital siğil varlığı karsinom öncülü sayılmazken; yüksek riskli tiplerle kronik enfeksiyon displazi habercisidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Yüksek riskli HPV tipleri (16, 18) karsinom etkeniyken; düşük riskli tipler (6, 11) benign genital siğillerle (kondilom) ilişkilidir."
    )
    s22_bullets = [
        "HPV tipleri yüksek ve düşük onkojenik riskli olarak ikiye ayrılır.",
        "Yüksek riskli tipler (özellikle 16 ve 18) karsinogenezden sorumludur.",
        "Düşük riskli tipler (6 ve 11) benign kondilomlara yol açar."
    ]
    s22_elements = [
        make_cloze("Servikal karsinom ve CIN gelişiminde en sık sorumlu yüksek riskli HPV tipleri HPV 16 ve HPV 18'dir.", "HPV 16", "En sık görülen yüksek onkojenik riskli tip"),
        make_table("HPV Tipleri ve Klinik Tablolar", ["Genotip Grubu", "Örnek Tipler", "Oluşturduğu Patoloji"], [
            {"cells": [{"text": "Yüksek Riskli Tipler", "isMasked": False}, {"text": "HPV 16, 18, 31, 33, 45", "isMasked": True, "hint": "malign potansiyelli tipler"}, {"text": "Servikal intraepitelyal lezyonlar ve karsinom"}]},
            {"cells": [{"text": "Düşük Riskli Tipler", "isMasked": False}, {"text": "HPV 6 ve 11", "isMasked": False}, {"text": "Kondiloma aküminata ve laringeal papillom", "isMasked": True, "hint": "selim genital siğil tablosu"}]}
        ]),
        make_chain("Viral Genotip Ayrımı ve Klinik Sonuç", [
            "1. Genotipik Özellik: Virüsün genomik yapısı onkoprotein gücünü ve biyolojisini belirler.",
            "2. Düşük Risk (6, 11): Epitelde iyi diferansiye hiperplazi ve ekzofitik siğil yapar, kanser yapmaz.",
            "3. Yüksek Risk (16, 18): Hücre döngüsü kontrolünü bozarak genomik dengesizlik ve displazi üretir.",
            "4. Malignite: Yüksek riskli tipler zaman içinde invaziv skuamöz karsinoma evrilir."
        ]),
        make_recall("Yüksek riskli HPV tipleri ile düşük riskli tiplerin oluşturduğu temel klinik tablolar nelerdir?", "Yüksek riskli tipler (16, 18) karsinom ve öncü displazilere; düşük riskli tipler (6, 11) selim genital siğillere (kondilom) yol açar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Onkojenik Risk Grupları", [
            {"text": "HPV 16 ve 18 yüksek onkojenik riskli tiplerdir.", "isLie": False, "explanation": "Doğru. Serviks kanserinin en önemli etkenleridir."},
            {"text": "HPV 6 ve 11 benign genital siğillere (kondiloma aküminata) neden olur.", "isLie": False, "explanation": "Doğru. Düşük riskli tipler kondilom yapar."},
            {"text": "HPV 6 ve 11 tipleri tüm dünyadaki serviks kanserlerinin %99'undan tek başına sorumludur.", "isLie": True, "explanation": "Tuzak! HPV 6 ve 11 düşük risklidir ve kanser yapmaz; kanserlerin çoğundan HPV 16 ve 18 sorumludur."},
            {"text": "Yüksek riskli tipler serviks dışında anüs ve vulva kanserlerinde de rol oynar.", "isLie": False, "explanation": "Doğru. Diğer anogenital bölgelerde de karsinom etkenidir."}
        ]),
        make_quiz("Kondiloma aküminata (genital siğil) etyolojisinde en sık rol oynayan düşük riskli HPV tipleri hangileridir?", [
            {"key": "A", "text": "HPV tip 6 ve HPV tip 11", "isCorrect": True, "explanation": "HPV 6 ve 11 düşük riskli olup kondilomların etkenidir."},
            {"key": "B", "text": "HPV tip 16 ve HPV tip 18", "isCorrect": False, "explanation": "Bunlar yüksek riskli karsinom etkenleridir."},
            {"key": "C", "text": "Yalnızca Epstein-Barr virüsü tip 1", "isCorrect": False, "explanation": "EBV herpesvirüs ailesindendir."},
            {"key": "D", "text": "Hepatit B ve Hepatit C virüsleri", "isCorrect": False, "explanation": "Hepatotrop virüslerdir."}
        ])
    ]
    slides.append(make_slide(22, "HPV Onkojenik Risk Ayrımı: Yüksek ve Düşük Risk", "Onkojenik potansiyel, tip 16/18 karsinomu, tip 6/11 kondilomları", "Viral Onkoloji Sınıflaması", s22_narrative, s22_bullets, s22_elements))

    # Slide 23: HPV Enfeksiyonunun Doğal Seyri ve Geçici Enfeksiyonlar
    s23_narrative = (
        "Cinsel yönden aktif toplumlarda HPV enfeksiyonu son derece yaygın bir durum olmasına karşın, "
        "enfekte olan kadınların yalnızca çok küçük bir kısmında kanser veya ağır displazi gelişir.\n\n"
        "- **Geçici Enfeksiyon Kuralı:** Toplumda saptanan HPV enfeksiyonlarının **yaklaşık %80-90'ı geçicidir** "
        "ve aylar/yıllar içinde konağın immün sistemi tarafından kendiliğinden temizlenir.\n"
        "- **Kalıcılık Süresi:** Enfeksiyonun süresi virüsün tipine bağlıdır; yüksek riskli HPV tiplerinin "
        "vücutta kalma süresi düşük riskli tiplere oranla belirgin şekilde daha uzundur.\n"
        "- **Spontan Klirens:** İmmün sistemi sağlam kadınlarda enfeksiyon genellikle subklinik seyreder ve "
        "herhangi bir kalıcı epitelyal hasar bırakmadan geriler.\n\n"
        "> [!NOTE]\n"
        "> Çoğu HPV enfeksiyonu geçicidir ve aylar içinde immün sistem tarafından kendiliğinden temizlenir."
    )
    s23_bullets = [
        "HPV enfeksiyonlarının %80-90'ı geçici karakterdedir.",
        "Sağlıklı bağışıklık sistemi virüsü aylar içinde temizler.",
        "Yüksek riskli tiplerin dokuda kalış süresi daha uzundur."
    ]
    s23_elements = [
        make_cloze("Toplumda saptanan HPV enfeksiyonlarının yaklaşık yüzde 80'i aylar içinde immün sistem tarafından kendiliğinden temizlenir.", "yüzde 80", "Kendiliğinden gerileyen enfeksiyonların yaklaşık oranı"),
        make_table("HPV Enfeksiyonunun Doğal Seyir Dinamikleri", ["Enfeksiyon Durumu", "Görülme Oranı", "Klinik Seyir ve Sonuç"], [
            {"cells": [{"text": "Geçici Enfeksiyon", "isMasked": False}, {"text": "Olguların %80-90'ı", "isMasked": True, "hint": "ezici çoğunluğu oluşturan oran"}, {"text": "1-2 yıl içinde kendiliğinden klirens"}]},
            {"cells": [{"text": "Persistan Enfeksiyon", "isMasked": False}, {"text": "Olguların %10-15'i", "isMasked": False}, {"text": "Prekanseröz displazi ve karsinom riski", "isMasked": True, "hint": "progresyon gösteren riskli grup"}]}
        ]),
        make_chain("HPV Klirens Aşamaları", [
            "1. Viral Temas: Mukozaya giren virüs bazal hücrelerde düşük düzeyde çoğalır.",
            "2. İmmün Tanıma: Dendritik hücreler viral proteinleri T lenfositlere sunar.",
            "3. Hücresel İmmün Yanıt: CD4+ ve CD8+ T lenfositler enfekte hücreleri ortadan kaldırır.",
            "4. Spontan Klirens: Virüs dokudan temizlenir ve mukoza tamamen normale döner."
        ]),
        make_recall("HPV enfeksiyonuna maruz kalan kadınların büyük çoğunluğunda enfeksiyonun doğal seyri nasıldır?", "Olguların %80-90'ında enfeksiyon geçicidir ve 1-2 yıl içinde immün sistem tarafından kendiliğinden temizlenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Enfeksiyonu Doğal Seyri", [
            {"text": "Çoğu HPV enfeksiyonu geçicidir ve immün sistem tarafından temizlenir.", "isLie": False, "explanation": "Doğru. Enfeksiyonların %80-90'ı kendiliğinden geçer."},
            {"text": "Yüksek riskli tipler düşük riskli tiplere göre vücutta daha uzun süre kalabilir.", "isLie": False, "explanation": "Doğru. Klirens süreleri daha uzundur."},
            {"text": "HPV ile temas eden her kadında 48 saat içinde kesinlikle terminal evre kanser gelişir.", "isLie": True, "explanation": "Tuzak! Enfeksiyonların büyük çoğunluğu kanserleşmez, kendiliğinden temizlenir; kanserleşme yıllar alan nadir bir durumdur."},
            {"text": "Konağın hücresel bağışıklık sistemi viral klirenste kritik rol oynar.", "isLie": False, "explanation": "Doğru. İmmün yanıt klirensi sağlar."}
        ]),
        make_quiz("HPV enfeksiyonlarının toplumdaki doğal seyri ile ilgili aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Çoğu enfeksiyon geçicidir ve aylar içinde immün sistemce temizlenir", "isCorrect": True, "explanation": "Olguların %80-90'ı kendiliğinden tamamen geriler."},
            {"key": "B", "text": "İstisnasız her enfekte birey birkaç hafta içinde yaşamını yitirir", "isCorrect": False, "explanation": "Ölümcül akut enfeksiyon yapmaz."},
            {"key": "C", "text": "İnsan bağışıklık sistemi hiçbir zaman HPV virüsünü tanıyamaz", "isCorrect": False, "explanation": "Hücresel bağışıklık virüsü başarıyla temizler."},
            {"key": "D", "text": "Sadece kan nakli yoluyla temizlenen bir bakteriyel enfeksiyondur", "isCorrect": False, "explanation": "Viral enfeksiyondur."}
        ])
    ]
    slides.append(make_slide(23, "HPV Enfeksiyonunun Doğal Seyri ve Geçici Enfeksiyonlar", "Viral klirens, konak immün yanıtı, spontan gerileme ve epidemiyoloji", "Doğal Seyir ve Klirens", s23_narrative, s23_bullets, s23_elements))

    # Slide 24: Persistan HPV Enfeksiyonu: Karsinogenezin Anahtarı
    s24_narrative = (
        "HPV enfeksiyonlarının çoğu temizlenirken, bazı olgularda virüs bağışıklıktan kaçarak konak epitelinde "
        "yıllar boyu canlılığını sürdürür. Bu tabloya **persistan (kalıcı) enfeksiyon** adı verilir.\n\n"
        "- **Kritik Etyolojik Rol:** Servikal karsinogenezdeki ==ana risk faktörü yüksek riskli HPV ile persistan enfeksiyondur==. "
        "Geçici enfeksiyonlar displaziye ilerlemezken, kalıcı enfeksiyon hücresel mutasyonların birikmesine zaman tanır.\n"
        "- **Kalıcılığı Artıran Faktörler:** Virüsün genotipi (özellikle HPV 16), yüksek viral yük, ileri yaş ve "
        "enfeksiyonun 1-2 yıldan uzun süre pozitif kalması karsinogenez riskini katlar.\n"
        "- **Hücresel Sonuç:** Virüs epitelde kaldıkça kontrolsüz onkoprotein ekspresyonu yapar ve epitelyal displazi sürecini başlatır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Serviks kanseri ve öncü lezyonların (CIN) gelişiminde en kritik temel risk faktörü yüksek riskli HPV ile persistan enfeksiyondur."
    )
    s24_bullets = [
        "Karsinogenezdeki ana faktör yüksek riskli HPV ile kalıcı enfeksiyondur.",
        "Geçici enfeksiyonlar temizlenirken kalıcı enfeksiyonlar neoplaziye ilerler.",
        "Yüksek viral yük ve persistan enfeksiyon displazi riskini katlar."
    ]
    s24_elements = [
        make_cloze("Serviks öncü lezyonları ve kanser gelişiminde en kritik risk faktörü persistan enfeksiyon tablosudur.", "persistan", "Virüsün dokuda uzun süre kalıcı olması durumu"),
        make_table("Geçici ve Persistan HPV Enfeksiyonu Kıyaslaması", ["Parametre", "Geçici Enfeksiyon", "Persistan Enfeksiyon"], [
            {"cells": [{"text": "Süreç", "isMasked": False}, {"text": "< 1-2 yıl içinde klirens", "isMasked": False}, {"text": "Yıllarca sebat eden viral varlık", "isMasked": True, "hint": "uzun süreli kalıcılık"}]},
            {"cells": [{"text": "Karsinom Riski", "isMasked": False}, {"text": "Malignite riski ihmal edilebilir", "isMasked": True, "hint": "kanser tehlikesi yok denecek kadar az"}, {"text": "Yüksek oranda CIN ve invaziv karsinom", "isMasked": False}]}
        ]),
        make_chain("Persistan Enfeksiyondan Kanser Öncüsüne", [
            "1. İmmün Kaçış: Yüksek riskli HPV lokal immün baskıyı aşarak bazal hücrelerde kalır.",
            "2. Sebat Eden Varlık: Enfeksiyon 2 yıldan uzun süre persistan olarak pozitif kalır.",
            "3. Sürekli Onkoprotein Salımı: E6 ve E7 proteinleri hücre döngüsünü sürekli uyarır.",
            "4. Prekanseröz Displazi: Genomik kırılmalar birikerek servikal intraepitelyal lezyon (SIL) oturur."
        ]),
        make_recall("Serviks karsinogenezinde geçici enfeksiyondan ziyade hangi durum kanser gelişiminin ana itici gücüdür?", "Yüksek riskli HPV ile meydana gelen persistan (kalıcı) enfeksiyondur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Persistan HPV Enfeksiyonu", [
            {"text": "Persistan enfeksiyon servikal öncü lezyon riskini belirgin artırır.", "isLie": False, "explanation": "Doğru. Kalıcılık displazinin ön şartıdır."},
            {"text": "Karsinogenezdeki ana risk faktörü yüksek riskli HPV ile kalıcı enfeksiyondur.", "isLie": False, "explanation": "Doğru. En kritik etiyolojik belirteçtir."},
            {"text": "Persistan enfeksiyon hiçbir hücreye dokunmadan 10 saniye içinde vücuttan buharlaşır.", "isLie": True, "explanation": "Tuzak! Persistan enfeksiyon aylarca/yıllarca dokuda sebat eden kalıcı enfeksiyondur."},
            {"text": "Viral kalıcılık onkoproteinlerin kontrolsüz çalışmasına zemin hazırlar.", "isLie": False, "explanation": "Doğru. E6 ve E7 sürekli baskı oluşturur."}
        ]),
        make_quiz("Servikal karsinogenez sürecinde en kritik tek etiyolojik risk faktörü aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Yüksek riskli HPV tipleri ile persistan (kalıcı) enfeksiyon", "isCorrect": True, "explanation": "Yüksek riskli HPV'nin kalıcı enfeksiyonu karsinogenezin ana itici gücüdür."},
            {"key": "B", "text": "Çocukluk çağında bir kez soğuk algınlığı geçirilmesi", "isCorrect": False, "explanation": "Rinovirus veya nezle ile ilişkisi yoktur."},
            {"key": "C", "text": "Düzenli sebze ve meyve tüketimi", "isCorrect": False, "explanation": "Kanser koruyucu bir faktördür."},
            {"key": "D", "text": "Düşük riskli HPV tip 6'nın 1 hafta sonra temizlenmesi", "isCorrect": False, "explanation": "Geçici düşük riskli enfeksiyon karsinom yapmaz."}
        ])
    ]
    slides.append(make_slide(24, "Persistan HPV Enfeksiyonu: Karsinogenezin Anahtarı", "Viral sebat, immün kaçış mekanizmaları, displazi riski ve onkolojik zemin", "Persistan Enfeksiyon", s24_narrative, s24_bullets, s24_elements))

    # Slide 25: HPV Bulaşı ve Epidemiyolojik Risk Faktörleri
    s25_narrative = (
        "HPV, insandan insana temel olarak doğrudan genital deri ve mukoza teması (cinsel ilişki) yoluyla bulaşır. "
        "Enfeksiyonun toplumdaki sıklığı cinsel davranış kalıpları ile doğrudan ilişkilidir.\n\n"
        "- **Temel Risk Faktörleri:** Erken yaşta ilk cinsel ilişki (transformasyon zonunun immatür olduğu dönem), "
        "çok sayıda cinsel partnere sahip olmak ve çok partnerli bir eşe sahip olmak en önemli maruziyet faktörleridir.\n"
        "- **Bariyer Yöntemleri:** Kondom kullanımı bulaş riskini azaltsa da, virüs kondomun örtmediği çevre genital "
        "deri alanlarından da bulaşabildiği için %100 tam koruma sağlamaz.\n"
        "- **Asemptomatik Bulaş:** Virüsü taşıyan bireylerin büyük çoğunluğu asemptomatik olduğundan bulaş fark edilmeksizin yayılır.\n\n"
        "> [!NOTE]\n"
        "> Erken yaşta ilk cinsel ilişki ve çok sayıda cinsel partner HPV maruziyeti ve enfeksiyon riskini en çok artıran faktörlerdir."
    )
    s25_bullets = [
        "HPV temel olarak cinsel temas yoluyla bulaşır.",
        "Erken yaşta ilk ilişki ve partner sayısı riski artırır.",
        "Taşıyıcıların çoğunluğu asemptomatik olduğundan yayılım kolaydır."
    ]
    s25_elements = [
        make_cloze("HPV maruziyetinde transformasyon bölgesinin duyarlı olduğu erken yaşta ilk cinsel ilişki en önemli risk faktörlerindendir.", "erken yaşta", "Maruziyet riskini artıran yaşam dönemi"),
        make_table("HPV Bulaşı ve Epidemiyolojik Değişkenler", ["Risk Faktörü", "Biyolojik Mekanizma", "Enfeksiyon Riski"], [
            {"cells": [{"text": "Çok Sayıda Partner", "isMasked": False}, {"text": "Viral temas ve farklı genotiplerle karşılaşma sıklığı", "isMasked": True, "hint": "farklı kökenli virüslerle karşılaşma"}, {"text": "Katlanarak artar"}]},
            {"cells": [{"text": "Erken Yaşta İlk İlişki", "isMasked": False}, {"text": "Transformasyon bölgesinde immatür hücre varlığı", "isMasked": False}, {"text": "Kolay viral penetrasyon ve entegrasyon", "isMasked": True, "hint": "genç epitele yerleşme kolaylığı"}]}
        ]),
        make_chain("Cinsel Temastan Servikal Enfeksiyona", [
            "1. Cinsel Maruziyet: Enfekte partnerden mikro-abrazyon yoluyla virionlar transfer olur.",
            "2. Epitelyal Penetrasyon: Virüs çatlaklardan geçerek servikal bazal tabakaya ulaşır.",
            "3. İntraselüler Yerleşim: Hücre reseptörlerine tutunarak episomal çoğalmaya başlar.",
            "4. Asemptomatik Yayılım: Taşıyıcı hiçbir semptom hissetmeksizin enfeksiyonu yayabilir."
        ]),
        make_recall("HPV maruziyetini artıran en belirleyici iki epidemiyolojik cinsel risk faktörü nedir?", "Erken yaşta ilk cinsel ilişki ve partner sayısının fazla olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Epidemiyolojisi", [
            {"text": "HPV esas olarak doğrudan mukozal cinsel temasla bulaşır.", "isLie": False, "explanation": "Doğru. Temel bulaşma yolu cinsel temastır."},
            {"text": "Erken yaşta ilk cinsel ilişki ve çok partnerlilik riski artırır.", "isLie": False, "explanation": "Doğru. En klasik epidemiyolojik risk faktörleridir."},
            {"text": "HPV sadece havada asılı kalan toz zerreciklerinin solunmasıyla bulaşan bir akciğer virüsüdür.", "isLie": True, "explanation": "Tuzak! HPV hava yoluyla bulaşmaz; genital ve mukokutanöz temasla bulaşır."},
            {"text": "Enfekte bireylerin çoğu asemptomatiktir.", "isLie": False, "explanation": "Doğru. Çoğu kişi taşıyıcı olduğunu bilmez."}
        ]),
        make_quiz("Aşağıdakilerden hangisi HPV maruziyeti ve enfeksiyon riskini artıran temel faktörlerdendir?", [
            {"key": "A", "text": "Erken yaşta ilk cinsel ilişki ve çok sayıda cinsel partner", "isCorrect": True, "explanation": "Erken yaş ve çok partnerlilik en önemli maruziyet faktörleridir."},
            {"key": "B", "text": "Haftada üç gün düzenli spor yapılması", "isCorrect": False, "explanation": "Spor ile bulaşın ilişkisi yoktur."},
            {"key": "C", "text": "Kan grubu 0 Rh pozitif olmak", "isCorrect": False, "explanation": "Kan grubuyla ilişkisi gösterilmemiştir."},
            {"key": "D", "text": "Yalnızca steril cam bardaktan su içmek", "isCorrect": False, "explanation": "Su yoluyla bulaşmaz."}
        ])
    ]
    slides.append(make_slide(25, "HPV Bulaşı ve Epidemiyolojik Risk Faktörleri", "Cinsel temas, erken cinsel yaşam, partner sayısı ve taşıyıcılık", "Epidemiyoloji ve Bulaş", s25_narrative, s25_bullets, s25_elements))

    # Slide 26: Kofaktörler: Sigara ve İmmün Yetmezlik
    s26_narrative = (
        "HPV enfeksiyonu serviks kanseri gelişimi için zorunlu bir faktör olmakla birlikte, kanserleşme "
        "sürecinde tek başına yeterli değildir; ek kofaktörlerin devreye girmesi gerekir.\n\n"
        "- **Sigara Kullanımı:** Tütün dumanındaki karsinojenik metabolitler (örneğin nikotin ve kotinin) "
        "servikal mukusta birikir; lokal DNA hasarını artırarak ve Langerhans hücrelerini baskılayarak kanser riskini katlar.\n"
        "- **İmmün Yetmezlik:** HIV enfeksiyonu, organ nakli sonrası immünsüpresif tedavi veya kemoterapi alan "
        "bireylerde hücresel immünite çöktüğü için HPV klirensi bozulur; persistan enfeksiyon ve hızlı displazi gelişir.\n"
        "- **Diğer Faktörler:** Eşlik eden klamidya veya herpes enfeksiyonları gibi inflamatuvar süreçler de kofaktör olarak rol oynayabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HPV enfeksiyonunda karsinogeneze ilerlemeyi en çok hızlandıran iki kritik kofaktör sigara içimi ve immün yetmezliktir."
    )
    s26_bullets = [
        "HPV gereklidir ancak karsinogenez için tek başına yeterli değildir.",
        "Sigara karsinojenleri servikal mukusta birikerek DNA hasarı yapar.",
        "İmmün yetmezlik viral klirensi engelleyerek persistan enfeksiyona yol açar."
    ]
    s26_elements = [
        make_cloze("Servikal mukusta birikerek DNA hasarını artıran ve kanserleşmeyi tetikleyen en önemli kimyasal kofaktör sigara içimidir.", "sigara", "Servikal karsinogenezde kanıtlanmış kimyasal kofaktör"),
        make_table("Karsinogenezi Hızlandıran Temel Kofaktörler", ["Kofaktör", "Etki Mekanizması", "Patolojik Sonuç"], [
            {"cells": [{"text": "Sigara (Tütün)", "isMasked": False}, {"text": "Mukusta kotinin birikimi ve DNA hasarı", "isMasked": True, "hint": "tütün karsinojenlerinin mukozal birikimi"}, {"text": "Mutasyon birikiminde hızlanma"}]},
            {"cells": [{"text": "İmmün Yetmezlik (HIV vb.)", "isMasked": False}, {"text": "T lenfosit aracılı hücresel savunma çöküşü", "isMasked": False}, {"text": "Viral klirens bozulması ve kalıcılık", "isMasked": True, "hint": "temizlenemeyen inatçı enfeksiyon"}]}
        ]),
        make_chain("Kofaktörlerin Karsinogeneze Etkisi", [
            "1. Viral Varlık: Servikal epitelde yüksek riskli HPV bulunmaktadır.",
            "2. Toksik/İmmün Baskı: Sigara karsinojenleri mukozaya yerleşir ve immün yanıt zayıflar.",
            "3. Klirens Başarısızlığı: İmmünite virüsü temizleyemez ve kalıcı enfeksiyon oturur.",
            "4. Hızlı Progresyon: Hücresel mutasyonlar birikerek displazi invaziv karsinoma evrilir."
        ]),
        make_recall("HPV varlığında servikal karsinom gelişim riskini belirgin biçimde artıran iki temel kofaktör nedir?", "Sigara içimi ve immün yetmezliktir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Serviks Karsinogenez Kofaktörleri", [
            {"text": "HPV serviks kanseri için gereklidir ancak tek başına her zaman yeterli değildir.", "isLie": False, "explanation": "Doğru. Ek kofaktörler karsinogenezi tetikler."},
            {"text": "Sigara içimi ve immün yetmezlik riski artıran önemli kofaktörlerdir.", "isLie": False, "explanation": "Doğru. Kanıtlanmış iki majör kofaktördür."},
            {"text": "Günde 2 paket sigara içmek serviks epitelini tüm virüslere karşı zırh gibi korur.", "isLie": True, "explanation": "Tuzak! Sigara servikal karsinojen birikimine yol açarak kanser riskini katlar, korumaz."},
            {"text": "İmmün sistemi baskılanmış kişilerde persistan enfeksiyon gelişme riski yüksektir.", "isLie": False, "explanation": "Doğru. Klirens yapılamaz."}
        ]),
        make_quiz("HPV enfeksiyonunun servikal karsinoma ilerlemesinde rol oynayan ek risk artırıcı faktörler hangileridir?", [
            {"key": "A", "text": "Sigara içme ve immün yetmezlik", "isCorrect": True, "explanation": "Sigara karsinojenleri ve immün çöküş karsinogenezi hızlandırır."},
            {"key": "B", "text": "Yüksek rakımda temiz dağ havası solumak", "isCorrect": False, "explanation": "Kanser riskini artırmaz."},
            {"key": "C", "text": "Çinko ve C vitamini içeren taze besinler tüketmek", "isCorrect": False, "explanation": "Zararlı kofaktör değildir."},
            {"key": "D", "text": "Günde sekiz saat kesintisiz uyumak", "isCorrect": False, "explanation": "Fizyolojik bir durumdur."}
        ])
    ]
    slides.append(make_slide(26, "Kofaktörler: Sigara ve İmmün Yetmezlik", "Tütün karsinojenleri, kotinin birikimi, hücresel immünite yetersizliği ve progresyon", "Kofaktörler ve İlerleme", s26_narrative, s26_bullets, s26_elements))

    # Slide 27: HPV Onkoproteinleri ve Hücre Döngüsü
    s27_narrative = (
        "Human Papilloma Virus, konak hücrenin replikasyon mekanizmasını kendi lehine çevirebilmek amacıyla "
        "özelleşmiş onkoproteinler üretir. Normalde skuamöz epitel olgunlaşırken hücre döngüsü G1 fazında durur.\n\n"
        "- **Büyüme Durmasının Engellenmesi:** HPV viral genomunu çoğaltabilmek için konak hücrenin bölünmeye devam etmesine muhtaçtır; "
        "bu nedenle fizyolojik **büyüme durmasını engeller**.\n"
        "- **Erken Onkoproteinler:** Bu sürecin merkezinde virüsün erken gen bölgesi tarafından kodlanan "
        "**E6 ve E7 onkoproteinleri** yer alır.\n"
        "- **Hücresel Kaos:** E6 ve E7, konağın hücre döngüsünü ve apoptoz mekanizmalarını kontrol eden en kritik "
        "tümör baskılayıcı gen ürünlerini hedef alarak inaktive eder.\n\n"
        "> [!NOTE]\n"
        "> HPV'nin viral replikasyonu ve yayılımı için konak epitel hücresinin büyüme durmasını engellemesi zorunludur."
    )
    s27_bullets = [
        "HPV olgunlaşan skuamöz hücrelerde büyüme durmasını engeller.",
        "Viral replikasyon konak DNA sentez mekanizmasına bağımlıdır.",
        "Merkezi rol oynayan temel viral faktörler E6 ve E7 onkoproteinleridir."
    ]
    s27_elements = [
        make_cloze("HPV konak epitel hücresinin fizyolojik büyüme durmasını engelleyerek viral replikasyonu sürdürür.", "büyüme durmasını", "Normal epitelde G1 fazında gerçekleşen duraklama"),
        make_table("HPV Onkoproteinlerinin Genel Hedefleri", ["Viral Protein", "Temel Hücresel Hedef", "Yol Açtığı Biyolojik Değişim"], [
            {"cells": [{"text": "E6 Onkoproteini", "isMasked": False}, {"text": "p53 tümör baskılayıcı protein", "isMasked": True, "hint": "genom koruyucusu protein"}, {"text": "Apoptozun önlenmesi ve telomeraz aktivasyonu"}]},
            {"cells": [{"text": "E7 Onkoproteini", "isMasked": False}, {"text": "Retinoblastoma (RB) proteini", "isMasked": False}, {"text": "G1/S kontrolünün kalkması ve kontrolsüz mitoz", "isMasked": True, "hint": "hücre döngüsü kısıtlamasının kalkması"}]}
        ]),
        make_chain("Viral Döngü Kontrolünün Bozulması", [
            "1. Viral İfade: Enfekte bazal hücrede E6 ve E7 onkoproteinleri üretilir.",
            "2. Fren Mekanizmasının Kırılması: Hücre döngüsünün G1 fazında durması engellenir.",
            "3. Sürekli Sentez: Konak hücre DNA sentez fazında (S fazı) tutulur.",
            "4. Viral Yayılım: Virüs konak mekanizmasıyla çoğalarak üst epitel katmanlarına yayılır."
        ]),
        make_recall("HPV'nin viral replikasyonunu gerçekleştirebilmek için konak hücre döngüsünde yaptığı temel müdahale nedir?", "Olgunlaşan hücrelerde fizyolojik büyüme durmasını engellemek ve hücreyi sürekli DNA sentezinde tutmaktır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Onkoproteinleri ve Döngü", [
            {"text": "HPV enfekte hücrelerde büyüme durmasını engeller.", "isLie": False, "explanation": "Doğru. Replikasyon için döngüyü sürdürür."},
            {"text": "E6 ve E7 viral karsinogenezde rol oynayan erken proteinlerdir.", "isLie": False, "explanation": "Doğru. Temel onkoproteinlerdir."},
            {"text": "HPV hücreye girdiği anda hücrenin tüm DNA'sını yok edip hücreyi taşa dönüştürür.", "isLie": True, "explanation": "Tuzak! Hücreyi yok etmez, aksine çoğalmasını uyararak kendi genomunu replike ettirir."},
            {"text": "Virüs replikasyon için konak DNA sentez enzimlerini kullanır.", "isLie": False, "explanation": "Doğru. Konağın polimeraz sistemini sömürür."}
        ]),
        make_quiz("HPV'nin karsinogenezinde rol oynayan ve hücre döngüsünü kontrolsüzce uyaran temel viral proteinler hangileridir?", [
            {"key": "A", "text": "E6 ve E7 onkoproteinleri", "isCorrect": True, "explanation": "E6 ve E7 karsinogenezin iki ana viral onkoproteinidir."},
            {"key": "B", "text": "Sadece hemoglobin ve miyoglobin", "isCorrect": False, "explanation": "Oksijen taşıyıcı konak proteinleridir."},
            {"key": "C", "text": "İnsülin ve glukagon", "isCorrect": False, "explanation": "Pankreatik hormonlardır."},
            {"key": "D", "text": "Kazein ve laktoz", "isCorrect": False, "explanation": "Süt bileşenleridir."}
        ])
    ]
    slides.append(make_slide(27, "HPV Onkoproteinleri ve Hücre Döngüsü", "G1/S fazı, büyüme durmasının engellenmesi, erken genler ve viral replikasyon", "Viral Onkogenez Mekanizması", s27_narrative, s27_bullets, s27_elements))

    # Slide 28: Onkoprotein E6: p53 İnhibisyonu ve Telomeraz Aktivasyonu
    s28_narrative = (
        "Yüksek riskli HPV tiplerinin en önemli virülans silahlarından biri olan **E6 onkoproteini**, "
        "hücrenin genomik bekçisi kabul edilen p53 yolağını tamamen felç eder.\n\n"
        "- **p53 Yıkımı:** E6, hücresel E6AP ubikitin ligaz ile birleşerek tümör baskılayıcı **p53 proteinine bağlanır** "
        "ve p53'ün ubikitin-proteazom yoluyla hızla parçalanmasına (proteolizine) yol açar.\n"
        "- **Apoptozun Engellenmesi:** DNA hasarı olduğunda p53 devreye giremediği için hücre apoptoza gidemez; "
        "hasarlı ve mutasyonlu DNA taşıyan hücreler yaşamaya devam eder.\n"
        "- **Telomeraz Aktivasyonu (hTERT):** E6 aynı zamanda konak telomeraz enzim ekspresyonunu artırarak "
        "hücre telomerlerinin kısalmasını engeller; böylece hücreye **ölümsüzlük (immortalizasyon)** kazandırır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HPV E6 onkoproteini p53'ü parçalayarak apoptozu engeller ve telomeraz aktivasyonunu artırarak hücresel ölümsüzlük sağlar."
    )
    s28_bullets = [
        "E6, p53 tümör baskılayıcısına bağlanarak proteazomal yıkımını sağlar.",
        "p53 yokluğu DNA hasarına yanıt olarak gelişecek apoptozu önler.",
        "Telomerazı aktive ederek hücre ömrünü uzatır ve immortalizasyon sağlar."
    ]
    s28_elements = [
        make_cloze("HPV E6 onkoproteini tümör baskılayıcı p53 proteinine bağlanarak yıkımına aracılık eder.", "p53", "Genom koruyucusu tümör baskılayıcı protein"),
        make_table("E6 Onkoproteininin Hücresel Etkileri", ["Hedef / Molekül", "E6'nın Etkisi", "Hücresel Sonuç"], [
            {"cells": [{"text": "p53 Proteini", "isMasked": False}, {"text": "Ubikitin-proteazom ile hızlı yıkım", "isMasked": True, "hint": "proteoliz ile parçalanma"}, {"text": "Apoptoz inhibisyonu ve mutasyon birikimi"}]},
            {"cells": [{"text": "Telomeraz Enzimi", "isMasked": False}, {"text": "Ekspresyonun belirgin artırılması", "isMasked": False}, {"text": "Telomer kısalmasının önlenmesi ve ölümsüzlük", "isMasked": True, "hint": "sınırsız bölünme potansiyeli"}]}
        ]),
        make_chain("E6 Yoluyla Karsinogenez", [
            "1. E6 Sentezi: Viral E6 onkoproteini hücre sitoplazmasında sentezlenir.",
            "2. p53 Kompleksi: E6AP ligaz ile birleşerek p53 proteinine kovalent bağlanır.",
            "3. Proteazomal Yıkım: p53 proteazomlarda parçalanarak hücredeki düzeyi sıfırlanır.",
            "4. Apoptozsuz Proliferasyon: Mutasyonlu hücreler ölmeyip telomeraz uyarısıyla ölümsüzleşir."
        ]),
        make_recall("Yüksek riskli HPV E6 onkoproteininin karsinogenezdeki iki temel fonksiyonu nedir?", "p53'e bağlanıp yıkarak apoptozu engellemek ve telomerazı aktive ederek hücresel ölümsüzlük sağlamaktır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: E6 Onkoproteini", [
            {"text": "E6 onkoproteini p53 tümör baskılayıcı proteinin yıkımına aracılık eder.", "isLie": False, "explanation": "Doğru. Proteazomal yıkımı tetikler."},
            {"text": "E6 telomeraz ekspresyonunu artırarak hücresel ölümsüzlük sağlar.", "isLie": False, "explanation": "Doğru. Telomerazı aktive eder."},
            {"text": "E6 onkoproteini p53 miktarını 100 kat artırarak tüm hücreleri anında apoptoza zorlar.", "isLie": True, "explanation": "Tuzak! E6 p53'ü artırmaz, tam tersine parçalayarak yok eder ve apoptozu engeller."},
            {"text": "p53 inaktivasyonu sonucu mutasyonlu hücreler canlı kalır.", "isLie": False, "explanation": "Doğru. Hücre ölümü baskılanır."}
        ]),
        make_quiz("Yüksek riskli HPV onkoproteini E6'nın konak hücredeki temel moleküler etkisi nedir?", [
            {"key": "A", "text": "p53'e bağlanarak proteazomal yıkımını sağlamak ve telomerazı artırmak", "isCorrect": True, "explanation": "E6 p53'ü yıkar, apoptozu önler ve telomerazı uyarır."},
            {"key": "B", "text": "Kalsiyum kanallarını bloke ederek nöromüsküler kavşağı felç etmek", "isCorrect": False, "explanation": "Toksin etkisi göstermez."},
            {"key": "C", "text": "Hücre zarını eritip sitoplazmayı tamamen dışarı akıtmak", "isCorrect": False, "explanation": "Lizis yapmaz."},
            {"key": "D", "text": "Sadece tiroksin hormon sentezini durdurmak", "isCorrect": False, "explanation": "Tiroidle ilişkisi yoktur."}
        ])
    ]
    slides.append(make_slide(28, "Onkoprotein E6: p53 İnhibisyonu ve Telomeraz Aktivasyonu", "Proteazomal proteoliz, apoptoz direnci, telomerik uzama ve ölümsüzleşme", "Moleküler Onkoloji: E6", s28_narrative, s28_bullets, s28_elements))

    # Slide 29: Onkoprotein E7: Retinoblastoma (RB) ve E2F Salınımı
    s29_narrative = (
        "HPV'nin diğer majör onkoproteini olan **E7**, hücre döngüsünün en önemli kontrol noktası olan "
        "G1/S geçiş fren mekanizmasını doğrudan hedef alır.\n\n"
        "- **RB Proteinine Bağlanma:** Normalde hipofosforile durumdaki Retinoblastoma (RB) proteini, "
        "E2F transkripsiyon faktörünü sıkıca bağlayarak hücrenin DNA sentezine (S fazı) girmesini engeller.\n"
        "- **E2F'nin Serbest Kalması:** Yüksek riskli HPV E7 proteini, **RB'ye yüksek afiniteyle bağlanır** ve "
        "RB'nin tuttuğu E2F transkripsiyon faktörlerini serbest bırakır.\n"
        "- **Kontrolsüz Hücre Döngüsü:** Serbest kalan E2F, siklin E ve siklin A gibi DNA sentez genlerini aktive eder; "
        "böylece hücre döngüsü kontrolü bozulur ve hücre kontrolsüzce S fazına sürüklenir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HPV E7 onkoproteini RB proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakır ve kontrolsüz G1/S hücre döngüsü geçişine yol açar."
    )
    s29_bullets = [
        "E7 proteini Retinoblastoma (RB) tümör baskılayıcısına bağlanır.",
        "RB'den ayrılan E2F transkripsiyon faktörü serbest kalır.",
        "G1/S geçiş kontrolü bozularak kontrolsüz DNA sentezi tetiklenir."
    ]
    s29_elements = [
        make_cloze("HPV E7 onkoproteini RB proteinine bağlanarak serbest bıraktığı E2F transkripsiyon faktörü ile S fazını başlatır.", "E2F", "Döngüyü S fazına sokan serbest transkripsiyon faktörü"),
        make_table("E7 Onkoproteininin Moleküler Mekanizması", ["Komponent", "Fizyolojik Durumu", "E7 Varlığında Durumu"], [
            {"cells": [{"text": "RB Proteini", "isMasked": False}, {"text": "E2F'yi bağlayarak döngüyü durdurur", "isMasked": False}, {"text": "E7 tarafından bağlanıp inaktive edilir", "isMasked": True, "hint": "frenin devreden çıkarılması"}]},
            {"cells": [{"text": "E2F Faktörü", "isMasked": False}, {"text": "RB tarafından bağlı ve inaktif tutulur", "isMasked": True, "hint": "baskılanmış faktör"}, {"text": "Serbest kalarak DNA sentezini başlatır", "isMasked": False}]}
        ]),
        make_chain("E7 ile Hücre Döngüsünün Hızlanması", [
            "1. E7 Üretimi: Viral E7 proteini hücresel hedeflerine doğru ilerler.",
            "2. RB Kompleksi: E7 yüksek afiniteyle hipofosforile RB'ye kilitlenir.",
            "3. E2F Salınımı: RB konformasyonu değişir ve bağlı E2F serbest kalır.",
            "4. S Fazı Girişi: E2F çekirdekte transkripsiyonu başlatarak hücreyi hızla mitoza sokar."
        ]),
        make_recall("Yüksek riskli HPV E7 onkoproteininin hücre döngüsündeki kritik etkisi nedir?", "RB proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakmak ve hücreyi kontrolsüz biçimde G1'den S fazına geçirmektir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: E7 Onkoproteini", [
            {"text": "E7 onkoproteini Retinoblastoma (RB) proteinine bağlanır.", "isLie": False, "explanation": "Doğru. Temel hücresel hedefi RB'dir."},
            {"text": "RB inaktive olunca E2F serbest kalarak hücreyi S fazına sokar.", "isLie": False, "explanation": "Doğru. Kontrolsüz DNA sentezi başlar."},
            {"text": "E7 proteini hücre döngüsünü tamamen dondurup hücreyi ömür boyu G0 fazında hapseder.", "isLie": True, "explanation": "Tuzak! E7 döngüyü dondurmaz; tam aksine G1/S frenini kırarak kontrolsüzce hızlandırır."},
            {"text": "Yüksek riskli tiplerin E7 proteini RB'ye çok yüksek afiniteyle bağlanır.", "isLie": False, "explanation": "Doğru. Düşük risklilere göre afinitesi çok daha yüksektir."}
        ]),
        make_quiz("HPV onkoproteini E7'nin hücre döngüsündeki temel etki mekanizması aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "RB proteinine bağlanıp E2F'yi serbest bırakarak G1/S geçişini hızlandırmak", "isCorrect": True, "explanation": "E7 RB'ye bağlanır, E2F serbest kalır ve hücre S fazına geçer."},
            {"key": "B", "text": "Hücre zarına por açarak sodyum girişini engellemek", "isCorrect": False, "explanation": "İyon kanalı etkisi yoktur."},
            {"key": "C", "text": "Sadece hemoglobin sentezini artırıp eritrosit üretmek", "isCorrect": False, "explanation": "Hematopoetik etkisi yoktur."},
            {"key": "D", "text": "Tümör baskılayıcı p53 proteinini uyararak hücreyi intihara zorlamak", "isCorrect": False, "explanation": "Bu E7'nin değil, fizyolojik mekanizmanın işidir; virüs bunu engeller."}
        ])
    ]
    slides.append(make_slide(29, "Onkoprotein E7: Retinoblastoma (RB) ve E2F Salınımı", "RB inaktivasyonu, E2F salınımı, G1/S siklin aktivasyonu ve kontrolsüz mitoz", "Moleküler Onkoloji: E7", s29_narrative, s29_bullets, s29_elements))

    # Slide 30: [TEKRAR SAYFASI - CHECKPOINT 3] HPV Virolojisi ve Onkoproteinleri (E6/E7)
    s30_narrative = (
        "Bölüm 3'te serviks kanserinin moleküler temelini oluşturan HPV virolojisini, risk sınıflamasını ve "
        "karsinogenezin iki ana motoru olan E6 ve E7 onkoproteinlerini detaylarıyla öğrendik.\n\n"
        "- **HPV Mimarisi:** Zarfsız, çift iplikli dairesel DNA virüsüdür; çoğalan bazal hücreleri enfekte eder.\n"
        "- **Risk Tipleri:** Yüksek riskli tipler (özellikle **HPV 16 ve 18**) karsinom etkeniyken; düşük riskli tipler "
        "(özellikle **HPV 6 ve 11**) selim kondilomlara yol açar.\n"
        "- **Doğal Seyir ve Kofaktörler:** Enfeksiyonların %80-90'ı geçicidir; karsinoma gidişte **persistan enfeksiyon** ana risk faktörüdür; "
        "sigara ve immün yetmezlik süreci hızlandıran kilit kofaktörlerdir.\n"
        "- **E6 ve E7 Mekanizması:** E6 **p53'ü yıkarak** apoptozu engeller ve telomerazı uyarır; E7 ise **RB'ye bağlanarak E2F'yi serbest bırakır** "
        "ve kontrolsüz G1/S geçişine yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 3 SENTEZİ] Yüksek riskli HPV'de persistan enfeksiyon şarttır; E6 p53'ü yok ederek apoptozu önlerken, E7 RB'yi devreden çıkararak hücreyi durmaksızın mitoza sokar."
    )
    s30_bullets = [
        "HPV çift iplikli DNA virüsüdür; Tip 16/18 karsinom, Tip 6/11 kondilom yapar.",
        "Persistan enfeksiyon karsinogenezin anahtarıdır; sigara ve immün çöküş kofaktördür.",
        "E6 p53'ü parçalar (apoptoz yok); E7 RB'ye bağlanıp E2F'yi salar (kontrolsüz S fazı)."
    ]
    s30_elements = [
        make_cloze("HPV E6 onkoproteini p53 proteinini yıkar; E7 ise RB proteinine bağlanarak E2F faktörünü serbest bırakır.", "p53", "Bölüm 3 sentezinde pekiştirilen temel tümör baskılayıcı hedef"),
        make_table("Bölüm 3 Moleküler Özet Tablosu", ["Viral Faktör / Tip", "Hücresel Hedef", "Nihai Patolojik Sonuç"], [
            {"cells": [{"text": "Yüksek Riskli Tip 16, 18", "isMasked": False}, {"text": "Kalıcı enfeksiyon ve genomik hasar", "isMasked": True, "hint": "uzun süreli sebat ve mutasyon"}, {"text": "Servikal karsinom ve CIN öncülleri"}]},
            {"cells": [{"text": "Viral E6 Onkoproteini", "isMasked": False}, {"text": "p53 yıkımı ve telomeraz artışı", "isMasked": False}, {"text": "Apoptoz direnci ve hücresel immortalizasyon", "isMasked": True, "hint": "ölümsüzlük ve hücre ölümü engeli"}]},
            {"cells": [{"text": "Viral E7 Onkoproteini", "isMasked": False}, {"text": "RB inaktivasyonu ve E2F salınımı", "isMasked": False}, {"text": "G1/S kontrolünün kaybı ve kontrolsüz mitoz", "isMasked": True, "hint": "frenin kalkması ve hücre bölünmesi"}]}
        ]),
        make_chain("Bölüm 3 Mekanizma Bütünleştirmesi", [
            "1. Viral İnokülasyon: Yüksek riskli HPV çift iplikli DNA'sı bazal hücreye girer.",
            "2. Viral Persistans: Sigara ve immün kaçışla virüs vücutta kalıcı hale gelir.",
            "3. İkili Onkojenik Saldırı: E6 p53'ü parçalayarak ölümü engeller; E7 RB'yi bağlayarak bölünmeyi hızlandırır.",
            "4. Kanser Zeminine Giriş: Hücreler ölümsüzleşerek genetik instabilite ve prekanseröz displaziye ilerler."
        ]),
        make_recall("HPV onkoproteinleri E6 ve E7'nin inaktive ettiği iki temel tümör baskılayıcı protein hangileridir?", "E6 p53 proteinini; E7 ise Retinoblastoma (RB) proteinini inaktive eder."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 3 Checkpoint Sentezi", [
            {"text": "HPV 16 ve 18 karsinomlarla, HPV 6 ve 11 kondilomlarla ilişkilidir.", "isLie": False, "explanation": "Doğru. Yüksek ve düşük risk ayrımıdır."},
            {"text": "E6 p53'ü yıkar; E7 ise RB'ye bağlanıp E2F'yi serbest bırakır.", "isLie": False, "explanation": "Doğru. Temel karsinogenez formülüdür."},
            {"text": "HPV enfeksiyonlarının %80-90'ı geçicidir ve bağışıklık sistemiyle temizlenir.", "isLie": False, "explanation": "Doğru. Çoğu enfeksiyon kendiliğinden geçer."},
            {"text": "Düşük riskli HPV 6 ve 11 insan genomuna entegre olarak her hastada karsinom yapar.", "isLie": True, "explanation": "Tuzak! HPV 6 ve 11 episomal kalır, entegre olmaz ve kanser yapmaz; selim kondilom yapar."}
        ]),
        make_quiz("Bölüm 3 boyunca işlenen viral onkogenez mekanizmasında aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "E6 onkoproteini p53'ü aktive ederek hücreyi hızla apoptoza sürükler", "isCorrect": True, "explanation": "Yanlış önerme! E6 p53'ü aktive etmez, yıkar ve apoptozu engeller."},
            {"key": "B", "text": "E7 onkoproteini RB'ye bağlanarak E2F'yi serbest bırakır", "isCorrect": False, "explanation": "Doğru mekanizmadır."},
            {"key": "C", "text": "Servikal karsinogenezde en kritik risk faktörü persistan enfeksiyondur", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Sigara içimi ve immün yetmezlik riski artıran önemli kofaktörlerdir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(30, "[TEKRAR SAYFASI - CHECKPOINT 3] HPV Virolojisi ve Onkoproteinleri (E6/E7)", "Bölüm 3 kapsamlı tekrarı: virolojik yapı, tipler, doğal seyir ve E6/E7 yolağı", "Bölüm Tekrarı ve Konsolidasyon", s30_narrative, s30_bullets, s30_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec3()
    print(f"Sec3 generated: {len(slides)} slides (Slide 21 to 30)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
