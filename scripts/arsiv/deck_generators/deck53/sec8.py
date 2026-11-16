# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec8():
    slides = []

    # Slide 71: Endometritlerin Genel Özellikleri ve Etyolojisi
    s71_narrative = (
        "Endometrit, endometrium mukozasının enfeksiyöz veya reaktif inflamatuar sürecidir.\n\n"
        "- **Epidemiyoloji:** Reprodüktif dönemdeki kadınlarda daha sık olmakla birlikte, postmenopozal "
        "hastalarda da organik lezyonlara sekonder olarak gelişebilir; sıklıkla **pelvik inflamatuar "
        "hastalığa (PİH)** eşlik eder.\n"
        "- **Tetikleyici Durumlar:** Abortus (düşük) ve doğum/gebelik sonrası; endometrial biyopsi, "
        "**rahim içi araç (RİA)** kullanımı, servikal stenoz ve kaviter organik lezyonlar (endometrial "
        "polip, leiomyom, hiperplazi, karsinom) endometrit ile yakından ilişkilidir.\n"
        "- **Klinik Tablo:** Hastalar tamamen **asemptomatik** olabileceği gibi; **intermenstrüel kanama, "
        "menoraji, infertilite, pelvik ağrı ve vajinal akıntı** semptomları ile kliniklere başvurabilirler.\n"
        "- **Önemli Sonuç:** Özellikle tedavi edilmeyen olgular tubal yapışıklıklara ve steriliteye yol açabilir.\n\n"
        "> [!NOTE]\n"
        "> Endometrit reprodüktif dönemde sıktır ve PİH'e eşlik eder; abortus, gebelik, biyopsi, RİA ve polip/myom ile ilişkili olabilir; asemptomatik veya kanamalı seyredebilir."
    )
    s71_bullets = [
        "Reprodüktif dönemde sıktır ve pelvik inflamatuar hastalığa (PİH) eşlik eder.",
        "Abortus, gebelik, biyopsi, RİA, servikal stenoz ve organik lezyonlarla (polip, myom) ilişkilidir.",
        "Semptomlar: asemptomatik olabilir; intermenstrüel kanama, menoraji, infertilite, ağrı, akıntı."
    ]
    s71_elements = [
        make_cloze("Endometrit sıklıkla pelvik inflamatuar hastalığa eşlik eder ve RİA kullanımı ile ilişkili olabilir.", "pelvik inflamatuar hastalığa", "Endometritin sıklıkla eşlik ettiği pelvik tablo"),
        make_table("Endometrit Etiyoloji ve Klinik Yelpazesi", ["Kategori", "İlişkili Faktörler", "Semptomlar"], [
            {"cells": [{"text": "Girişimsel / Obstetrik", "isMasked": False}, {"text": "Abortus, doğum, küretaj, RİA kullanımı", "isMasked": True, "hint": "mekanik ve obstetrik nedenler"}, {"text": "Ağrı, kanama, kötü kokulu akıntı"}]},
            {"cells": [{"text": "Organik Zemin", "isMasked": False}, {"text": "Endometrial polip, myom, karsinom, stenoz", "isMasked": False}, {"text": "Menoraji, ara kanama", "isMasked": True, "hint": "kanama bozuklukları"}]},
            {"cells": [{"text": "Sessiz Seyir", "isMasked": False}, {"text": "Subklinik kronik enfeksiyon", "isMasked": False}, {"text": "Asemptomatik veya infertilite"}]}
        ]),
        make_chain("Endometrit Patogenez Zinciri", [
            "1. Mukozal Bariyer Hasarı: Doğum, abortus, biyopsi veya RİA ile servikal bariyer aşılır.",
            "2. Mikrobiyal Giriş: Vajinal/servikal bakteriler endometrial lümene tırmanır.",
            "3. Enflamatuar İnfiltrasyon: Dokuda lökosit yanıtı ve vasküler konjesyon gelişir.",
            "4. Klinik Semptom: İntermenstrüel kanama, menoraji veya pelvik ağrı ortaya çıkar."
        ]),
        make_recall("Endometritin ilişkili olduğu obstetrik, jinekolojik ve mekanik faktörlerden dördünü belirtiniz.", "Abortus ve gebelik, endometrial biyopsi, RİA kullanımı, servikal stenoz ve organik lezyonlardır (polip, myom, hiperplazi)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrit Genel Özellikleri", [
            {"text": "Endometrit sıklıkla pelvik inflamatuar hastalığa eşlik eder.", "isLie": False, "explanation": "Doğru. Klinik birlikteliktir."},
            {"text": "Abortus, biyopsi ve RİA endometrit ile ilişkili olabilecek durumlardır.", "isLie": False, "explanation": "Doğru. Risk faktörleridir."},
            {"text": "Endometrit her zaman sıfır kanama yapar ve kadınlarda doğurganlığı 100 kat artırır.", "isLie": True, "explanation": "Tuzak! Endometrit intermenstrüel kanama, menoraji, ağrı ve infertiliteye (kısırlığa) yol açabilir."},
            {"text": "Hastalar asemptomatik de olabilir.", "isLie": False, "explanation": "Doğru. Sessiz vakalar sıktır."}
        ]),
        make_quiz("Endometritin etiyolojisi ve klinik semptomları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "PİH, abortus ve RİA ile ilişkili olabilir; intermenstrüel kanama, menoraji ve infertilite yapabilir", "isCorrect": True, "explanation": "Ders notunda endometritin risk faktörleri ve semptomları eksiksiz bu şekilde verilmiştir."},
            {"key": "B", "text": "Yalnızca menopozdan 50 yıl sonra ortaya çıkan genetik bir anomalidir", "isCorrect": False, "explanation": "Reprodüktif çağda daha sıktır."},
            {"key": "C", "text": "Sadece erkeklerde görülen bir mesane hastalığıdır", "isCorrect": False, "explanation": "Uterus mukozası hastalığıdır."},
            {"key": "D", "text": "Asla hiçbir mikroorganizma ile ilişkili olamaz", "isCorrect": False, "explanation": "Bakteriyel ve viral etkenler sıktır."}
        ])
    ]
    slides.append(make_slide(71, "Endometritlerin Genel Özellikleri ve Etyolojisi", "Reprodüktif sıklık, PİH birlikteliği, abortus, RİA faktörü ve infertilite/kanama semptomları", "Klinik Patoloji", s71_narrative, s71_bullets, s71_elements))

    # Slide 72: Endometriumda Lökositlerin Fizyolojik Varlığı Paradoksu
    s72_narrative = (
        "Endometriumun inflamatuar değerlendirmesinde patoloğu bekleyen en büyük biyolojik tuzak, dokunun doğal lökosit zenginliğidir.\n\n"
        "- **Genel Patoloji Paradoksu:** Genel olarak herhangi bir insan dokusunda iltihabi hücre görülmesi "
        "enflamasyon göstergesi olmasına karşın, **bu durum endometrium için geçerli değildir**.\n"
        "- **Tanısal Kriter:** Endometriumda iltihabi hücrelerin görülmesi inflamasyonun sabit bulgusu "
        "olarak kabul edilemez.\n"
        "- **Fizyolojik Lökositler:** Endometrit tanısı konmadan önce, menstruasyonla birlikte fizyolojik "
        "olarak artış gösteren **normal lenfoid ve polimorfonükleer lökosit (PMNL) populasyonunun** "
        "çok iyi tanınması gerekmektedir.\n"
        "- **Doku Hazırlığı:** İmplantasyon immünolojisi ve menstrüel doku yıkımı için lökositler siklik "
        "olarak endometriuma çağrılır; bu fizyolojik infiltrasyon enfeksiyonla karıştırılmamalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [KRİTİK UYARI] Genel olarak dokularda iltihabi hücre inflamasyon kanıtı iken, endometrium için geçerli değildir; iltihabi hücre görülmesi inflamasyonun sabit bulgusu sayılamaz."
    )
    s72_bullets = [
        "Genel doku kuralı endometrium için geçerli değildir; iltihabi hücre inflamasyonun sabit bulgusu değildir.",
        "Menstruasyonla birlikte artan normal lenfoid ve PMNL populasyonu mutlaka tanınmalıdır.",
        "Fizyolojik lökosit varlığı patolojik endometrit tanısı ile karıştırılmamalıdır."
    ]
    s72_elements = [
        make_cloze("Bir dokuda inflamasyon göstergesi iltihabi hücre olmasına karşın bu durum endometrium için geçerli değildir.", "bu durum endometrium için geçerli değildir", "Endometriumdaki fizyolojik lökosit kuralı"),
        make_table("Endometriumda Lökosit Paradoksu", ["Doku Tipi", "İltihabi Hücrenin Anlamı", "Patolojik Yorum"], [
            {"cells": [{"text": "Diğer Vücut Dokuları", "isMasked": False}, {"text": "Kesin inflamasyon / enfeksiyon bulgusu", "isMasked": False}, {"text": "Patolojik reaksiyon"}]},
            {"cells": [{"text": "Endometrium", "isMasked": False}, {"text": "İnflamasyonun sabit bulgusu kabul edilemez", "isMasked": True, "hint": "sabit bulgu sayılmama"}, {"text": "Fizyolojik siklik lökosit göçü mevcuttur", "isMasked": True, "hint": "normal hormonal yanıt"}]}
        ]),
        make_chain("Endometrial İnflamasyon Değerlendirme Algoritması", [
            "1. Lökosit Tespiti: Endometrium biyopsisinde lökositler görülür.",
            "2. Genel Kural Tuzağı: 'Lökosit var = kesin endometrit' yanılgısına düşülmez.",
            "3. Siklus Günü Kontrolü: Menstrüel fazda fizyolojik PMNL artışı teyit edilir.",
            "4. Ayırıcı Kriter: Sabit inflamasyon kriteri aranmaksızın özgül patolojik hücreler (plazma hücresi) araştırılır."
        ]),
        make_recall("Genel patolojide iltihabi hücre varlığı inflamasyon kanıtı iken, bu kural neden endometrium için doğrudan geçerli değildir?", "Çünkü endometriumda menstruasyonla birlikte lenfoid hücreler ve PMNL'ler fizyolojik olarak artar; bu nedenle iltihabi hücre görülmesi inflamasyonun sabit bulgusu sayılamaz."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrium Lökosit Paradoksu", [
            {"text": "İltihabi hücre görülmesi kuralı endometrium için geçerli değildir.", "isLie": False, "explanation": "Doğru. Ders notunun anahtar cümlesidir."},
            {"text": "Endometriumda iltihabi hücre görülmesi inflamasyonun sabit bulgusu olarak kabul edilemez.", "isLie": False, "explanation": "Doğru. Fizyolojik infiltrasyon vardır."},
            {"text": "Endometriumda tek bir lenfosit görüldüğü anda hasta derhal septik şok kabul edilip yoğun bakıma alınmalıdır.", "isLie": True, "explanation": "Tuzak! Endometriumda lenfositler ve PMNL'ler siklusun belirli dönemlerinde tamamen fizyolojiktir."},
            {"text": "Menstruasyonla artış gösteren normal lökosit populasyonu iyi tanınmalıdır.", "isLie": False, "explanation": "Doğru. Tanısal zorunluluktur."}
        ]),
        make_quiz("Endometriumda iltihabi hücrelerin izlenmesi ile ilgili patolojik yaklaşım prensibi hangisidir?", [
            {"key": "A", "text": "Genel inflamasyon göstergesi kuralı endometrium için geçerli değildir; iltihabi hücre sabit bulgu kabul edilemez", "isCorrect": True, "explanation": "Ders notunda açıkça: 'genel olarak bir dokuda inflamasyon göstergesi iltihabi hücre olmasına karşın bu durum endometrium için geçerli değildir; iltihabi hücrelerin görülmesi inflamasyonun sabit bulgusu olarak kabul edilemez' denmektedir."},
            {"key": "B", "text": "Her lökosit görülen endometrium derhal cerrahi olarak çıkarılmalıdır", "isCorrect": False, "explanation": "Fizyolojik hücrelerdir."},
            {"key": "C", "text": "Endometriumda hiçbir zaman lökosit hücresi bulunamaz, tamamen sterildir", "isCorrect": False, "explanation": "Fizyolojik lökositler boldur."},
            {"key": "D", "text": "Lökositler sadece karsinom varlığında ortaya çıkar", "isCorrect": False, "explanation": "Menstruasyonda da artar."}
        ])
    ]
    slides.append(make_slide(72, "Endometriumda Lökositlerin Fizyolojik Varlığı Paradoksu", "Endometriumun lökosit zenginliği, genel inflamasyon kuralının geçersizliği ve fizyolojik infiltrasyon", "Histopatoloji", s72_narrative, s72_bullets, s72_elements))

    # Slide 73: PMNL'ler ve Akut Endometrit Kriteri (Siklus Ortası)
    s73_narrative = (
        "Polimorfonükleer lökositlerin (PMNL / nötrofil) endometriumdaki zamansal lokasyonu tanısal açıdan belirleyicidir.\n\n"
        "- **Fizyolojik PMNL Varlığı:** PMNL'ler normal şartlarda **menstruasyondan hemen önce, menstruasyon "
        "sırasında ya da hemen sonrasında** dokuda yoğun şekilde izlenir; bu durum iskemik yıkımın doğal parçasıdır.\n"
        "- **Patolojik PMNL Varlığı (Akut Endometrit):** Buna karşılık, PMNL'ler **siklus ortasında "
        "(proliferatif fazda veya erken sekretuar fazda) görüldüklerinde akut endometrit düşünülmelidir**.\n"
        "- **Hücresel Dağılım:** Akut endometritte PMNL infiltrasyonu stromada fokal agregatlar, "
        "mikroapseler oluşturur; bez lümenlerini doldurarak bez epitelini destrükte eder.\n"
        "- **Klinik İpucu:** Siklus gününe uymayan nötrofil infiltrasyonu, bakteriyel invazyonun en güvenilir erken işaretidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] PMNL'ler normalde menstruasyon çevresinde izlenir; SİKLUS ORTASINDA görüldüklerinde akut endometrit düşünülmelidir."
    )
    s73_bullets = [
        "PMNL'ler normal menstruasyondan hemen önce, menstruasyon sırasında veya sonrasında izlenir.",
        "Siklus ortasında PMNL görüldüğünde akut endometrit düşünülmelidir.",
        "Akut endometritte bez lümenlerinde PMNL agregatları, mikroapseler ve doku yıkımı izlenir."
    ]
    s73_elements = [
        make_cloze("PMNL'ler menstruasyon çevresinde izlenirken siklus ortasında görüldüklerinde akut endometrit düşünülmelidir.", "akut endometrit", "Siklus ortası PMNL varlığında düşünülecek tanı"),
        make_table("PMNL Zamanlaması ve Tanısal Anlamı", ["Siklus Zamanı", "PMNL Varlığı", "Patolojik Anlam"], [
            {"cells": [{"text": "Menstruasyon Çevresi (Öncesi, sırası, sonrası)", "isMasked": False}, {"text": "Yoğun PMNL infiltrasyonu", "isMasked": False}, {"text": "Fizyolojik menstrüel dökülme yanıtı", "isMasked": True, "hint": "normal fizyolojik durum"}]},
            {"cells": [{"text": "Siklus Ortası (Mid-siklus)", "isMasked": False}, {"text": "PMNL agregatları / mikroapseler", "isMasked": True, "hint": "ara dönemde nötrofil"}, {"text": "Akut endometrit göstergesi", "isMasked": True, "hint": "akut enfeksiyon"}]}
        ]),
        make_chain("Akut Endometrit Histolojik Tanı Zinciri", [
            "1. Biyopsi Zamanlaması: Hastanın siklus ortasında olduğu (proliferatif faz) doğrulanır.",
            "2. Nötrofil Taraması: Stromada ve bez içinde PMNL kümeleri saptanır.",
            "3. Fizyoloji Dışı Zaman: Siklus ortasında PMNL varlığı patolojik kabul edilir.",
            "4. Tanı: Mikroapse ve epitel destrüksiyonu ile 'Akut Endometrit' tanısı verilir."
        ]),
        make_recall("PMNL'ler normal menstrüel siklusta ne zaman fizyolojiktir ve ne zaman görüldüklerinde akut endometrit düşünülmelidir?", "Menstruasyondan hemen önce, sırasında veya sonrasında fizyolojiktir; SİKLUS ORTASINDA görüldüklerinde akut endometrit düşünülmelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: PMNL ve Akut Endometrit", [
            {"text": "PMNL'ler normal menstruasyondan hemen önce veya sırasında izlenebilir.", "isLie": False, "explanation": "Doğru. Fizyolojik dökülmedir."},
            {"text": "Siklus ortasında görüldüklerinde akut endometrit düşünülmelidir.", "isLie": False, "explanation": "Doğru. Kardinal tanı zamanlamasıdır."},
            {"text": "Menstruasyon kanaması sırasında PMNL görülmesi kesinlikle ölümcül bir akut endometrittir.", "isLie": True, "explanation": "Tuzak! Menstruasyon sırasında PMNL görülmesi normal fizyolojik bir bulgudur; patolojik olan siklus ortasında görülmesidir."},
            {"text": "Akut endometritte bez lümenlerinde mikroapseler izlenebilir.", "isLie": False, "explanation": "Doğru. Histolojik bulgudur."}
        ]),
        make_quiz("Endometrium biyopsisinde polimorfonükleer lökositlerin (PMNL) ne zaman görülmesi akut endometrit lehine değerlendirilir?", [
            {"key": "A", "text": "Siklus ortasında görüldüklerinde", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'PMNL'ler normal menstruasyondan hemen önce, menstruasyon sırasında ya da sonrasında izlenir; siklus ortasında görüldüklerinde akut endometrit düşünülmelidir' denmektedir."},
            {"key": "B", "text": "Menstruasyonun en kanamalı ilk gününde", "isCorrect": False, "explanation": "Bu fizyolojiktir."},
            {"key": "C", "text": "Sadece 80 yaşından sonra", "isCorrect": False, "explanation": "Her yaşta siklus ortası önemlidir."},
            {"key": "D", "text": "Plasenta tam doğarken", "isCorrect": False, "explanation": "Doğum fizyolojisidir."}
        ])
    ]
    slides.append(make_slide(73, "PMNL'ler ve Akut Endometrit Kriteri (Siklus Ortası)", "Menstrüel fizyolojik nötrofiller, siklus ortası PMNL alarmı ve akut endometrit morfolojisi", "Histopatoloji", s73_narrative, s73_bullets, s73_elements))

    # Slide 74: Lenfosit Agregatları ve Mast Hücreleri
    s74_narrative = (
        "Endometrium mukozasında mononükleer inflamatuar hücrelerin fizyolojik dağılımı belirli lokalizasyon kurallarına uyar.\n\n"
        "- **Lenfositik Agregatlar:** Lenfositler herhangi bir patoloji olmaksızın, özellikle **bazal "
        "tabakada lenfositik agregatlar şeklinde** yer alır.\n"
        "- **İmmünolojik Fenotip:** Bu bazal agregatların çoğunluğunu **B lenfositler** oluşturur; "
        "sekretuar ve menstrüel fazda sayıları giderek artar.\n"
        "- **Mast Hücreleri:** Mast hücreleri **normal endometriumda son derece nadirdir**.\n"
        "- **Patolojik Mast Artışı:** Endometriumda mast hücresi artışı saptandığında, sıklıkla altta "
        "yatan bir **endometrial polip veya leiomyom** varlığı akla gelmelidir.\n\n"
        "> [!NOTE]\n"
        "> Lenfositler bazal tabakada fizyolojik agregatlar yapar (çoğu B lenfosit); mast hücreleri normalde çok nadirdir, polip ve myomda sayıları artabilir."
    )
    s74_bullets = [
        "Lenfositler bazal tabakada lenfositik agregatlar şeklinde normalde bulunur (çoğu B lenfosit).",
        "Sekretuar ve menstrüel fazda lenfosit sayıları fizyolojik olarak artar.",
        "Mast hücreleri normalde son derece nadirdir; endometrial polip ve leiomyomda artabilir."
    ]
    s74_elements = [
        make_cloze("Lenfositler patoloji olmaksızın özellikle bazal tabakada yer alır ve çoğu B lenfositlerdir.", "B lenfositlerdir", "Bazal agregatlardaki baskın lenfosit tipi"),
        make_table("Lenfosit ve Mast Hücresi Dağılımı", ["Hücre Tipi", "Normal Endometriumdaki Durumu", "Patolojik İlişkisi"], [
            {"cells": [{"text": "Lenfositler", "isMasked": False}, {"text": "Bazal tabakada agregatlar yapar (B lenfosit)", "isMasked": True, "hint": "fizyolojik lenfoid odaklar"}, {"text": "Sekretuar/menstrüel fazda artar (normal)"}]},
            {"cells": [{"text": "Mast Hücreleri", "isMasked": False}, {"text": "Son derece nadirdir (yok denecek kadar az)", "isMasked": False}, {"text": "Endometrial polip ve leiomyomda artar", "isMasked": True, "hint": "polip ve myom birlikteliği"}]}
        ]),
        make_chain("Endometrial Mononükleer Hücre Dağılımı", [
            "1. İmmün Gözetim: Bazal tabakada fizyolojik B lenfosit agregatları konumlanır.",
            "2. Fazik Dalgalanma: Sekretuar fazda lenfosit yoğunluğu fizyolojik olarak artar.",
            "3. Mast Hücresi Yokluğu: Normal fonksiyonel dokuda mast hücresi hemen hiç görülmez.",
            "4. Polip Uyarısı: Biyopside mast hücresi artışı komşu polip veya myom varlığını düşündürür."
        ]),
        make_recall("Endometriumda lenfositler normalde nerede toplanır ve mast hücreleri hangi lezyonlarda artabilir?", "Lenfositler özellikle bazal tabakada lenfositik agregatlar şeklinde yer alır (çoğu B lenfosit); mast hücreleri ise endometrial polip ve leiomyomda artabilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Lenfositler ve Mast Hücreleri", [
            {"text": "Lenfositler patoloji olmaksızın bazal tabakada agregatlar şeklinde yer alabilir.", "isLie": False, "explanation": "Doğru. Fizyolojik dağılımdır."},
            {"text": "Bazal tabakadaki lenfositlerin çoğu B lenfositlerdir.", "isLie": False, "explanation": "Doğru. İmmünofenotiptir."},
            {"text": "Normal endometrium tamamen mast hücreleri ile doludur ve her milimetrekarede 1 milyon mast hücresi bulunur.", "isLie": True, "explanation": "Tuzak! Mast hücreleri normal endometriumda son derece nadirdir; polip ve leiomyomda artabilir."},
            {"text": "Mast hücreleri endometrial polip ve leiomyomda artmış sayıda bulunabilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Endometriumda mast hücrelerinin normal varlığı ve artış gösterdiği lezyonlar hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Normalde son derece nadirdir; endometrial polip ve leiomyomda artmış sayıda bulunabilirler", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'mast hücreleri normal endometriumda son derece nadirdir; endometrial polip ve leiomyomda artmış sayıda bulunabilirler' denmektedir."},
            {"key": "B", "text": "Normalde en baskın hücredir; kanserde tamamen yok olur", "isCorrect": False, "explanation": "Normalde çok nadirdir."},
            {"key": "C", "text": "Sadece sekretuar fazın 1. saniyesinde salgılanır", "isCorrect": False, "explanation": "Hücredir, salgı değildir."},
            {"key": "D", "text": "Kemik iliğinde kalsiyum depolar", "isCorrect": False, "explanation": "Mast hücresi fonksiyonu değildir."}
        ])
    ]
    slides.append(make_slide(74, "Lenfosit Agregatları ve Mast Hücreleri", "Bazal B lenfosit agregatları, fazik lenfosit artışı ve polip/myomda artan mast hücreleri", "Histoloji", s74_narrative, s74_bullets, s74_elements))

    # Slide 75: Eozinofiller: Biyopside Plazma Hücresi Alarmı
    s75_narrative = (
        "Eozinofil lökositler, endometrium patolojisinde tanısal bir tetikleyici (alarm) hücresi işlevi görür.\n\n"
        "- **Normalde Yokluk:** Eozinofiller **normal endometrial populasyonda yer almaz** ve patolojik "
        "olarak da dokuda çok az izlenirler.\n"
        "- **Alarm Fonksiyonu:** Biyopsi kesitlerinde tek bir eozinofil dahi görülmesi patolog için "
        "hayati bir uyarıcıdır; **biyopside eozinofil görülmesi plazma hücresi aranması için uyarıcıdır**.\n"
        "- **Klinik Zemin:** Eozinofiller özellikle **küretajı takiben**, geçirilmiş mekanik travma, "
        "alerjik/toksik durumlar veya kronik pelvik enfeksiyon zemininde karşımıza çıkar.\n"
        "- **Tanısal Değer:** Eozinofilin saptanması, gözden kaçabilecek plazma hücrelerinin immünohistokimya "
        "ile aranmasını tetikleyerek kronik endometrit tanısının konmasını sağlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Eozinofiller normalde yer almaz; biyopside eozinofil görülmesi plazma hücresi aranması için mutlak bir uyarıcıdır; küretajı takiben görülebilir."
    )
    s75_bullets = [
        "Eozinofiller normal endometrial populasyonda yer almaz ve patolojik olarak da çok az izlenir.",
        "Biyopside eozinofil görülmesi plazma hücresi aranması için uyarıcıdır.",
        "Küretajı takiben biyopsilerde eozinofiller izlenebilir."
    ]
    s75_elements = [
        make_cloze("Endometrium biyopsisinde eozinofil görülmesi plazma hücresi aranması için uyarıcıdır.", "plazma hücresi", "Eozinofil görüldüğünde aranması gereken patolojik hücre"),
        make_table("Eozinofilin Endometriumdaki Anlamı", ["Özellik", "Durum", "Klinik / Patolojik Sonuç"], [
            {"cells": [{"text": "Normal Varlık", "isMasked": False}, {"text": "Normal populasyonda yer almaz", "isMasked": True, "hint": "normalde bulunmama"}, {"text": "Görülmesi patolojiktir"}]},
            {"cells": [{"text": "Tanısal İpucu", "isMasked": False}, {"text": "Plazma hücresi aranması için uyarıcı", "isMasked": False}, {"text": "Kronik endometritin yakalanması", "isMasked": True, "hint": "kronik iltihap tespiti"}]},
            {"cells": [{"text": "Görüldüğü Durum", "isMasked": False}, {"text": "Küretajı takiben", "isMasked": False}, {"text": "Mekanik travma ve doku reaksiyonu"}]}
        ]),
        make_chain("Eozinofil Alarm Zinciri", [
            "1. Biyopsi Taraması: Stromada pembe granüllü eozinofil lökosit fark edilir.",
            "2. Alarm Durumu: Patolog normalde eozinofil olmadığını hatırlar.",
            "3. Hedefli İnceleme: Kesitler dikkatle plazma hücresi bulmak için taranır.",
            "4. Kesin Tanı: Plazma hücresi doğrulanarak kronik endometrit tanısı kesinleşir."
        ]),
        make_recall("Endometrium biyopsisinde eozinofil görülmesinin en önemli tanısal anlamı ve uyarıcı rolü nedir?", "Biyopside eozinofil görülmesi, kronik endometrit tanısı için 'plazma hücresi aranması için uyarıcıdır' (küretaj sonrası da görülebilir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Eozinofiller ve Alarm Rolü", [
            {"text": "Eozinofiller normal endometrial populasyonda yer almaz.", "isLie": False, "explanation": "Doğru. Normalde bulunmaz."},
            {"text": "Biyopside eozinofil görülmesi plazma hücresi aranması için uyarıcıdır.", "isLie": False, "explanation": "Doğru. Ders notunun kritik uyarısıdır."},
            {"text": "Eozinofil görülmesi durumunda patolog incelemeyi derhal bırakıp dokunun tamamen normal olduğunu rapor etmelidir.", "isLie": True, "explanation": "Tuzak! Eozinofil görülmesi plazma hücresi aranması için UYARICIDIR; kronik endometrit aranmalıdır."},
            {"text": "Küretajı takiben eozinofiller görülebilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Endometrium biyopsisinde eozinofil lökosit görülmesinin patolojideki en önemli tanısal anlamı nedir?", [
            {"key": "A", "text": "Kronik endometrit tanısı için plazma hücresi aranması konusunda uyarıcı olması", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'eozinofiller normal populasyonda yer almaz; biyopside eozinofil görülmesi plazma hücresi aranması için uyarıcıdır; küretajı takiben görülebilir' denmektedir."},
            {"key": "B", "text": "Hastada gebelik olduğunu kesin olarak kanıtlaması", "isCorrect": False, "explanation": "Eozinofil gebelik kanıtı değildir."},
            {"key": "C", "text": "Uterus kanserinin 4. evreye ulaştığını göstermesi", "isCorrect": False, "explanation": "Kanser evrelemesiyle ilgisizdir."},
            {"key": "D", "text": "Normal sekretuar fazın bittiğini ilan etmesi", "isCorrect": False, "explanation": "Fizyolojik bir belirteç değildir."}
        ])
    ]
    slides.append(make_slide(75, "Eozinofiller: Biyopside Plazma Hücresi Alarmı", "Normalde yokluk, küretaj sonrası görünüm ve plazma hücresi aranması için uyarıcı eozinofiller", "Patoloji", s75_narrative, s75_bullets, s75_elements))

    # Slide 76: Kronik Endometritin Kardinal Şartı: Plazma Hücreleri
    s76_narrative = (
        "Kronik endometrit tanısında patolojinin en katı ve vazgeçilmez altın standardı plazma hücresinin varlığıdır.\n\n"
        "- **Normalde Kesinlikle Yokluk:** **Plazma hücreleri normal endometriumun komponenti DEĞİLDİR "
        "ve görüldükleri zaman kesinlikle patolojik kabul edilirler**.\n"
        "- **Mutlak Tanı Şartı:** Bir biyopside **kronik endometrit tanısı koyabilmek için plazma "
        "hücrelerinin gösterilmesi KESİNLİKLE ŞARTTIR**.\n"
        "- **Tanısal Zorluk:** Rutin hematoksilen-eozin (HE) boyamalarda plazma hücreleri kolaylıkla "
        "gözden kaçabilir; çünkü stroma içindeki **plazmasitoid stromal hücreler ve makrofajlarla "
        "morfolojik olarak karışabilirler**.\n"
        "- **Stromal Değişim:** Kronik nonspesifik endometritte plazma hücrelerine ek olarak, stromal "
        "hücrelerin iğsi değişimi ve bez çevrelerinde 'araba tekerleği' dizilimi izlenir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Plazma hücreleri normal endometriumda ASLA bulunmaz; görüldüklerinde patolojiktir ve kronik endometrit tanısı için GÖSTERİLMELERİ ŞARTTIR."
    )
    s76_bullets = [
        "Plazma hücreleri normal endometriumun komponenti değildir, görüldüklerinde patolojiktir.",
        "Kronik endometrit tanısı için plazma hücresinin gösterilmesi ŞARTTIR.",
        "Rutin HE boyamada plazmasitoid stromal hücreler ve makrofajlarla karışabilir.",
        "Kronik endometritte stromal hücrelerde iğsi değişim ve araba tekerleği dizilimi izlenir."
    ]
    s76_elements = [
        make_cloze("Plazma hücreleri normal endometriumun komponenti değildir ve kronik endometrit tanısı için şarttır.", "kronik endometrit tanısı için şarttır", "Plazma hücresinin varlığının zorunlu olduğu tanı"),
        make_table("Kronik Endometrit ve Plazma Hücresi Kriteri", ["Kriter", "Patolojik Özellik", "Klinik Değeri"], [
            {"cells": [{"text": "Normal Dokuda Durum", "isMasked": False}, {"text": "Kesinlikle bulunmaz (komponenti değildir)", "isMasked": True, "hint": "normalde sıfır hücre"}, {"text": "Görüldüğü an patolojiktir"}]},
            {"cells": [{"text": "Tanısal Zorunluluk", "isMasked": False}, {"text": "Kronik endometrit için şarttır", "isMasked": False}, {"text": "Olmazsa olmaz altın kural", "isMasked": True, "hint": "mutlak tanı şartı"}]},
            {"cells": [{"text": "Tanısal Karışıklık", "isMasked": False}, {"text": "Plazmasitoid stromal hücreler ve makrofajlar", "isMasked": False}, {"text": "Rutin HE'de gözden kaçabilir"}]}
        ]),
        make_chain("Kronik Endometrit Patolojik Tanı Basamakları", [
            "1. Endometrial Biyopsi: AUK veya infertilite nedeniyle küretaj kesiti incelenir.",
            "2. HE Taraması: Stromada lenfositler ve şüpheli plazmasitoid hücreler aranır.",
            "3. Karışıklık Tuzağı: Makrofajlar ve iğsi stromal hücreler plazma hücresini gizleyebilir.",
            "4. Plazma Hücresi Teyidi: Eksantrik çekirdekli ve perinükleer halolu plazma hücresi kanıtlanarak tanı konur."
        ]),
        make_recall("Kronik endometrit tanısı koyabilmek için biyopside görülmesi kesinlikle şart olan hücre hangisidir ve normal endometriumda bulunur mu?", "Plazma hücresidir; normal endometriumun komponenti değildir ve görüldüğü zaman kesinlikle patolojiktir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Plazma Hücresi ve Kronik Endometrit", [
            {"text": "Plazma hücreleri normal endometriumun komponenti değildir.", "isLie": False, "explanation": "Doğru. Normalde bulunmaz."},
            {"text": "Kronik endometrit tanısı için plazma hücresi şarttır.", "isLie": False, "explanation": "Doğru. Altın kuraldır."},
            {"text": "Plazma hücreleri tüm kadınların normal endometriumunda en bol bulunan fizyolojik hücrelerdir.", "isLie": True, "explanation": "Tuzak! Plazma hücreleri normal endometriumda ASLA bulunmaz; görüldüklerinde patolojiktir ve kronik endometrit şartıdır."},
            {"text": "Rutin HE boyamada plazmasitoid stromal hücreler ve makrofajlarla karışabilirler.", "isLie": False, "explanation": "Doğru. Tanısal güçlüktür."}
        ]),
        make_quiz("Kronik endometrit histopatolojik tanısının konulabilmesi için endometrial stromada görülmesi KESİNLİKLE ŞART olan hücre hangisidir?", [
            {"key": "A", "text": "Plazma hücresi", "isCorrect": True, "explanation": "Ders notunda açıkça: 'plazma hücreleri normal endometriumun komponenti değildir ve görüldükleri zaman patolojik kabul edilirler; kronik endometrit tanısı için şarttır' denmektedir."},
            {"key": "B", "text": "Eritrosit", "isCorrect": False, "explanation": "Kanamada doğal olarak bulunur."},
            {"key": "C", "text": "Bazal tabaka kök hücresi", "isCorrect": False, "explanation": "Fizyolojik hücredir."},
            {"key": "D", "text": "Osteoklast", "isCorrect": False, "explanation": "Kemik hücresidir."}
        ])
    ]
    slides.append(make_slide(76, "Kronik Endometritin Kardinal Şartı: Plazma Hücreleri", "Normalde bulunmama kuralı, mutlak tanı şartı, plazmasitoid stroma ile karışma ve araba tekerleği dizilimi", "Histopatoloji", s76_narrative, s76_bullets, s76_elements))

    # Slide 77: İmmünohistokimyasal Tanı: CD138 ve CD38
    s77_narrative = (
        "Plazma hücrelerinin rutin HE boyamalarda stromal hücrelerle karışması nedeniyle ileri boyama teknikleri kullanılır.\n\n"
        "- **Özel Histokimya:** Plazma hücrelerinin sitoplazmik RNA zenginliğini göstermek amacıyla "
        "**Methyl Green Pyronin** boyaması kullanılabilir.\n"
        "- **İmmünohistokimyasal Altın Standart:** Plazma hücrelerinin kesin ve tartışmasız tanısında "
        "en duyarlı ve özgül belirteçler **CD138 (Syndecan-1)** ve **CD38** antikorlarıdır.\n"
        "- **Klonalite Analizi:** Enfeksiyöz poliklonaliteyi teyit etmek veya nadir plazmasitomları "
        "dışlamak için **kappa ve lambda hafif zincir boyamaları** uygulanır.\n"
        "- **Klinik Kurtarıcı:** Özellikle tekrarlayan tüp bebek (IVF) başarısızlıkları ve açıklanamayan "
        "infertilite olgularında CD138 boyaması, gözden kaçan kronik endometritleri başarıyla saptar.\n\n"
        "> [!NOTE]\n"
        "> Plazma hücresi boyaması: Methyl green pyronin; İmmünohistokimya: CD38, CD138, kappa ve lambdadır."
    )
    s77_bullets = [
        "Plazma hücresi özel boyaması: Methyl green pyronin.",
        "İmmünohistokimya: CD138 (en duyarlı) ve CD38.",
        "Hafif zincir analizi: kappa ve lambda immünohistokimyası."
    ]
    s77_elements = [
        make_cloze("Kronik endometritte plazma hücrelerini doğrulamak için immünohistokimyada CD38, CD138, kappa ve lambda kullanılır.", "CD138", "Plazma hücresi için en yaygın tanısal İHK belirteci"),
        make_table("Plazma Hücresi Tanı Boyaları", ["Yöntem", "Boyama / Antikor", "Hedeflenen Yapı"], [
            {"cells": [{"text": "Özel Histokimyasal Boya", "isMasked": False}, {"text": "Methyl green pyronin", "isMasked": True, "hint": "RNA boyayan histokimyasal yöntem"}, {"text": "Plazma hücresi sitoplazmik RNA'sı"}]},
            {"cells": [{"text": "İmmünohistokimya (İHK)", "isMasked": False}, {"text": "CD138 ve CD38", "isMasked": False}, {"text": "Plazma hücresi yüzey antijenleri", "isMasked": True, "hint": "hücre zarı belirteçleri"}]},
            {"cells": [{"text": "Hafif Zincir Analizi", "isMasked": False}, {"text": "Kappa ve lambda", "isMasked": False}, {"text": "Poliklonal plazma hücresi infiltrasyonu"}]}
        ]),
        make_chain("İHK ile Plazma Hücresi Kanıtlama Zinciri", [
            "1. HE Şüphesi: İnfertilite biyopsisinde belirsiz mononükleer hücreler görülür.",
            "2. İHK İstem: Patolog CD138 ve CD38 antikorlarını uygular.",
            "3. Membran Boyanması: Plazma hücre zarlarında güçlü kahverengi boyanma izlenir.",
            "4. Doğrulama: Kronik endometrit tanısı objektif olarak kesinleştirilir."
        ]),
        make_recall("Kronik endometrit tanısında plazma hücrelerini göstermek için kullanılan özel histokimya ve immünohistokimya belirteçleri nelerdir?", "Özel boyama: Methyl green pyronin; İmmünohistokimya: CD38, CD138, kappa ve lambdadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Plazma Hücresi İHK", [
            {"text": "Plazma hücresi boyamasında methyl green pyronin kullanılabilir.", "isLie": False, "explanation": "Doğru. Özel boyadır."},
            {"text": "İmmünohistokimyada CD38 ve CD138 kullanılır.", "isLie": False, "explanation": "Doğru. Plazma hücresi belirteçleridir."},
            {"text": "Kronik endometritte CD138 boyanması kesinlikle imkansızdır, plazma hücreleri sadece demir boyasıyla boyanır.", "isLie": True, "explanation": "Tuzak! CD138 ve CD38 plazma hücresi tanısında standart immünohistokimyasal belirteçlerdir."},
            {"text": "Kappa ve lambda antikorları ile inceleme yapılabilir.", "isLie": False, "explanation": "Doğru. Hafif zincir tayinidir."}
        ]),
        make_quiz("Kronik endometrit tanısında plazma hücrelerinin immünohistokimyasal yöntemle gösterilmesinde kullanılan temel belirteçler hangileridir?", [
            {"key": "A", "text": "CD38, CD138, kappa ve lambda", "isCorrect": True, "explanation": "Ders notunda plazma hücresi için: 'immünohistokimya: CD38, CD138, kappa, lambda' açıkça listelenmiştir."},
            {"key": "B", "text": "Yalnızca PSA ve tiroglubin", "isCorrect": False, "explanation": "Prostat ve tiroid belirteçleridir."},
            {"key": "C", "text": "Sadece sitokeratin 20 ve CDX2", "isCorrect": False, "explanation": "Kolon epitel belirteçleridir."},
            {"key": "D", "text": "Desmin ve myogenin", "isCorrect": False, "explanation": "Kas belirteçleridir."}
        ])
    ]
    slides.append(make_slide(77, "İmmünohistokimyasal Tanı: CD138 ve CD38", "Methyl green pyronin boyası, CD138 ve CD38 immünbelirteçleri ve hafif zincir analizi", "Patoloji", s77_narrative, s77_bullets, s77_elements))

    # Slide 78: Endometrit Tipleri: Akut, Subakut ve Kronik Nonspesifik
    s78_narrative = (
        "Endometritler dokusal hasarın şiddetine ve hücresel infiltrasyonun karakterine göre üç temel histolojik tipe ayrılır.\n\n"
        "- **Akut Endometrit:** Yaygın kanama, doku yıkımı, ödem ve vasküler genişleme yanı sıra "
        "**yoğun PMNL infiltrasyonu** izlenir; PMNL'ler stromada mikroapseler yapar ve bez epitelini destrükte eder.\n"
        "- **Subakut Endometrit:** **PMNL'lerin bez içinde toplanması ve bez çevresinde plazma hücre "
        "infiltrasyonu** ile karakterizedir; doku yıkımı ve kanama izlenmez ya da az izlenir.\n"
        "- **Kronik Nonspesifik Endometrit:** **Plazma hücreleri**, stromal hücrelerin iğsi değişimi "
        "ve bez çevrelerinde **araba tekerleği (cartwheel / storiform) dizilimi** izlenir.\n"
        "- **Siklus Uyumsuzluğu:** Kronik formda bezlerin **siklus gününü yansıtmada yetersiz kalması** "
        "kardinal bir morfolojik bulgudur; plazma hücreleri yanı sıra lenfosit, makrofaj ve eozinofiller eşlik edebilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Akut: yaygın doku yıkımı, kanama, PMNL mikroapseleri; Subakut: bez içi PMNL + bez çevresi plazma hücresi; Kronik: plazma hücreleri, iğsi stroma, araba tekerleği dizilimi ve siklus uyumsuzluğu."
    )
    s78_bullets = [
        "Akut endometrit: yaygın kanama, doku yıkımı, ödem, yoğun PMNL mikroapseleri ve bez destrüksiyonu.",
        "Subakut endometrit: bez içinde PMNL toplanması ve bez çevresinde plazma hücresi; yıkım azdır.",
        "Kronik nonspesifik endometrit: plazma hücreleri, iğsi stroma, araba tekerleği dizilimi, siklus uyumsuzluğu."
    ]
    s78_elements = [
        make_cloze("Subakut endometritte PMNL'lerin bez içinde toplanması bez çevresi plazma hücre infiltrasyonu ile beraberdir.", "plazma hücre infiltrasyonu", "Subakut endometritte bez çevresindeki hücre yanıtı"),
        make_table("Endometrit Histolojik Tipleri Karşılaştırması", ["Endometrit Tipi", "Hücresel İnfiltrasyon", "Doku Yıkımı ve Kanama"], [
            {"cells": [{"text": "Akut Endometrit", "isMasked": False}, {"text": "Yoğun PMNL, mikroapseler, bez destrüksiyonu", "isMasked": True, "hint": "nötrofil baskınlığı"}, {"text": "Yaygın doku yıkımı, kanama, ödem"}]},
            {"cells": [{"text": "Subakut Endometrit", "isMasked": False}, {"text": "Bez içinde PMNL + bez çevresinde plazma hücresi", "isMasked": False}, {"text": "Doku yıkımı ve kanama yok ya da az", "isMasked": True, "hint": "hafif doku hasarı"}]},
            {"cells": [{"text": "Kronik Nonspesifik", "isMasked": False}, {"text": "Plazma hücresi, lenfosit, iğsi stroma", "isMasked": False}, {"text": "Araba tekerleği dizilimi, siklus uyumsuzluğu"}]}
        ]),
        make_chain("Endometrit Evrelerinin Ayrımı", [
            "1. Hücre Tipi Belirleme: PMNL mi, plazma hücresi mi, mikst mi?",
            "2. Akut Ayrımı: Masif kanama ve epitel yıkan PMNL mikroapseleri varsa Akut Endometrit.",
            "3. Subakut Ayrımı: Bez içinde nötrofil, etrafında plazma hücresi varsa Subakut Endometrit.",
            "4. Kronik Ayrımı: İğsi stroma, araba tekerleği paterni ve plazma hücreleri varsa Kronik Endometrit."
        ]),
        make_recall("Akut, subakut ve kronik endometritin en karakteristik histolojik ayırıcı özellikleri nelerdir?", "Akut: doku yıkımı, kanama ve yoğun PMNL mikroapseleri; Subakut: bez içinde PMNL + bez çevresinde plazma hücresi; Kronik: plazma hücreleri, iğsi stroma, araba tekerleği dizilimi ve bezlerin siklus gününü yansıtamamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrit Tipleri", [
            {"text": "Akut endometritte yaygın kanama, doku yıkımı ve yoğun PMNL izlenir.", "isLie": False, "explanation": "Doğru. Akut tablodur."},
            {"text": "Subakut endometritte bez içi PMNL ve bez çevresi plazma hücre infiltrasyonu izlenir.", "isLie": False, "explanation": "Doğru. Geçiş tablosudur."},
            {"text": "Kronik endometritte hiçbir iltihabi hücre bulunmaz, endometrium tamamen saf altından bir plakaya dönüşür.", "isLie": True, "explanation": "Tuzak! Kronik endometritte plazma hücreleri, lenfositler, iğsi stromal hücreler ve araba tekerleği dizilimi izlenir."},
            {"text": "Kronik endometritte bezler siklus gününü yansıtmada yetersiz kalır.", "isLie": False, "explanation": "Doğru. Siklus uyumsuzluğu esastır."}
        ]),
        make_quiz("Bez içinde PMNL toplanması ve bez çevresinde plazma hücresi infiltrasyonu ile karakterize, doku yıkımının az olduğu endometrit tipi hangisidir?", [
            {"key": "A", "text": "Subakut endometrit", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'subakut endometrit: PMNL'lerin bez içinde toplanması, bez çevresi plazma hücre infiltrasyonu ile beraberdir; doku yıkımı ve kanama izlenmez ya da az izlenir' denmektedir."},
            {"key": "B", "text": "Akut fulminan endometrit", "isCorrect": False, "explanation": "Akut tipte yaygın doku yıkımı ve kanama vardır."},
            {"key": "C", "text": "Sarkomatöz endometrit", "isCorrect": False, "explanation": "Tümöral durumdur."},
            {"key": "D", "text": "Fizyolojik proliferatif faz", "isCorrect": False, "explanation": "Enfeksiyon değildir."}
        ])
    ]
    slides.append(make_slide(78, "Endometrit Tipleri: Akut, Subakut ve Kronik Nonspesifik", "Akut PMNL mikroapseleri, subakut geçiş paternleri, kronik plazma hücresi ve araba tekerleği stroması", "Histopatoloji", s78_narrative, s78_bullets, s78_elements))

    # Slide 79: Spesifik Etkenler: Klamidya, Gonore ve Granülomatöz Tüberküloz
    s79_narrative = (
        "Endometritler mikroorganizma türüne bağlı olarak özgül patolojik ve epidemiyolojik paternler sergiler.\n\n"
        "- **Mikrobiyolojik Yelpaze:** Viral (HSV, CMV); klamidya; bakteriyel (Tbc, N. gonorrhoeae, "
        "N. meningitidis, Actinomyces israelii, Treponema pallidum); mikoplazma, mantar ve parazitler "
        "(Toksoplazmozis, Şistozomiazis) endometrit yapabilir.\n"
        "- **En Sık Spesifik Etkenler:** Spesifik endometritler içinde **en sık görülen klamidya "
        "(Chlamydia trachomatis) ve neisseria (Neisseria gonorrhoeae) endometritidir**.\n"
        "- **Granülomatöz Endometrit ve Tüberküloz:** Dokuda kazeifiye veya non-kazeifiye granülomlarla "
        "seyreden **granülomatöz endometritler ise en sık tüberküloza (Mycobacterium tuberculosis) bağlıdır**.\n"
        "- **Klinik Sonuç:** Tüberküloz endometriti genellikle hematojen yolla akciğerden yayılır "
        "ve endometriumda şiddetli yapışıklıklara (Asherman sendromu benzeri) ve kalıcı steriliteye neden olur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Spesifik endometritler içinde EN SIK görülen klamidya ve neisseria endometritidir; Granülomatöz endometritler ise en sık TÜBERKÜLOZA bağlıdır."
    )
    s79_bullets = [
        "Spesifik endometritler içinde en sık görülen: Chlamydia trachomatis ve Neisseria gonorrhoeae.",
        "Granülomatöz endometritler en sık tüberküloza (Mycobacterium tuberculosis) bağlıdır.",
        "Diğer etkenler: HSV, CMV, Actinomyces, Treponema pallidum, mikoplazma ve parazitler."
    ]
    s79_elements = [
        make_cloze("Spesifik endometritler içinde en sık görülen klamidya ve neisseria iken granülomatöz endometritler en sık tüberküloza bağlıdır.", "tüberküloza bağlıdır", "Granülomatöz endometritin en sık etkeni"),
        make_table("Spesifik Endometrit Etkenleri ve Özellikleri", ["Kategori", "En Sık Mikroorganizma", "Karakteristik Histopatoloji"], [
            {"cells": [{"text": "En Sık Spesifik Endometrit", "isMasked": False}, {"text": "Chlamydia trachomatis ve Neisseria gonorrhoeae", "isMasked": True, "hint": "klamidya ve gonokok"}, {"text": "Plazma hücresi ve lenfositik infiltrasyon"}]},
            {"cells": [{"text": "Granülomatöz Endometrit", "isMasked": False}, {"text": "Mycobacterium tuberculosis (Tbc)", "isMasked": False}, {"text": "Kazeifiye granülomlar, epiteloid histiositler", "isMasked": True, "hint": "tüberküloz granülomu"}]},
            {"cells": [{"text": "RİA Birlikteliği", "isMasked": False}, {"text": "Actinomyces israelii", "isMasked": False}, {"text": "Sülfür granülleri"}]}
        ]),
        make_chain("Spesifik Endometrit Etyolojik Akışı", [
            "1. Cinsel Yolla İletim: Chlamydia ve Neisseria serviksten endometriuma tırmanır (en sık).",
            "2. Kronik İnflamasyon: Stromada yaygın plazma hücresi ve lenfosit infiltrasyonu gelişir.",
            "3. Hematojen Yayılım: Akciğer tüberkülozu hematojen yolla uterusu tutar.",
            "4. Granülom Oluşumu: Tüberküloz basilinin etkisiyle granülomatöz endometrit şekillenir."
        ]),
        make_recall("Spesifik endometritler içinde en sık görülen etkenler hangileridir ve granülomatöz endometrit en sık neye bağlıdır?", "En sık görülenler klamidya ve neisseria'dır; granülomatöz endometritler ise en sık tüberküloza bağlıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Spesifik Endometrit Etkenleri", [
            {"text": "Spesifik endometritler içinde en sık görülen klamidya ve neisseria endometritidir.", "isLie": False, "explanation": "Doğru. En sık spesifik etkenlerdir."},
            {"text": "Granülomatöz endometritler en sık tüberküloza bağlıdır.", "isLie": False, "explanation": "Doğru. En sık granülomatöz nedendir."},
            {"text": "Endometriumda tüberküloz mikrobu asla yaşayamaz ve tüberküloz granülomu oluşturması imkansızdır.", "isLie": True, "explanation": "Tuzak! Tüberküloz granülomatöz endometritin en sık nedenidir ve kalıcı infertiliteye yol açabilir."},
            {"text": "Actinomyces israelii ve Treponema pallidum da endometrit etkenleri arasındadır.", "isLie": False, "explanation": "Doğru. Bakteriyel etkenlerdir."}
        ]),
        make_quiz("Spesifik endometritler içinde en sık izlenen etkenler ve granülomatöz endometritin en sık nedeni hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "En sık spesifik: Klamidya ve Neisseria | Granülomatöz: Tüberküloz", "isCorrect": True, "explanation": "Ders notunda açıkça: 'spesifik endometritler içinde en sık görülen klamidya ve neisseria endometritidir; granülomatöz endometritler ise en sık tüberküloza bağlıdır' denmektedir."},
            {"key": "B", "text": "En sık spesifik: Kuduz virüsü | Granülomatöz: Grip virüsü", "isCorrect": False, "explanation": "Uterus tutulumu yapmazlar."},
            {"key": "C", "text": "En sık spesifik: Kolera | Granülomatöz: Veba", "isCorrect": False, "explanation": "Gastrointestinal/sistemik hastalıklardır."},
            {"key": "D", "text": "Her iki grupta da tek etken saf mantar sporlarıdır", "isCorrect": False, "explanation": "Bakteriyel etkenler ön plandadır."}
        ])
    ]
    slides.append(make_slide(79, "Spesifik Etkenler: Klamidya, Gonore ve Granülomatöz Tüberküloz", "En sık klamidya ve neisseria endometriti, tüberküloza bağlı granülomatöz endometrit ve mikrobiyal spektrum", "Mikrobiyoloji ve Patoloji", s79_narrative, s79_bullets, s79_elements))

    # Slide 80: [TEKRAR SAYFASI - CHECKPOINT 8] Endometritler
    s80_narrative = (
        "Bu tekrar sayfasında 8. Bölümde ele aldığımız endometrium lökosit paradoksunu, PMNL zamanlamasını, "
        "kronik endometritin şartı olan plazma hücrelerini, İHK belirteçlerini ve spesifik etkenleri konsolide ediyoruz.\n\n"
        "- **Lökosit Paradoksu:** Dokuda lökosit olması endometriumda sabit bir inflamasyon kriteri "
        "değildir; menstruasyon çevresinde PMNL fizyolojiktir; SİKLUS ORTASINDA PMNL = akut endometrit.\n"
        "- **Hücresel Kriterler:** Lenfositler bazal agregat yapar (B lenfosit); mast hücreleri normalde "
        "çok nadirdir (polip/myomda artar); eozinofil görülmesi plazma hücresi aranması için alarmdır.\n"
        "- **Kronik Endometrit Şartı:** Plazma hücreleri normalde ASLA bulunmaz; kronik endometrit için "
        "ŞARTTIR; stromal hücrelerde araba tekerleği dizilimi ve siklus uyumsuzluğu izlenir; İHK'da CD138, "
        "CD38, kappa/lambda ve pyronin kullanılır.\n"
        "- **Spesifik Etkenler:** En sık spesifik etkenler Klamidya ve Neisseria; granülomatöz endometritte "
        "en sık etken Tüberkülozdur.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Siklus ortasında PMNL = akut endometrit; Plazma hücresi normalde YOKTUR, kronik endometrit için ŞARTTIR; İHK: CD138/CD38; Eozinofil alarmdır; En sık klamidya/gonore, granülomatöz = tüberküloz."
    )
    s80_bullets = [
        "Siklus ortasında PMNL = akut endometrit; eozinofil görülmesi plazma hücresi alarmıdır.",
        "Plazma hücresi normalde yoktur, kronik endometrit için şarttır; İHK'da CD138 ve CD38 kullanılır.",
        "En sık spesifik etkenler: klamidya ve neisseria; granülomatöz endometrit en sık tüberküloza bağlıdır."
    ]
    s80_elements = [
        make_cloze("Kronik endometrit tanısı için plazma hücresi şart olup spesifik etkenlerde en sık klamidya ve neisseria izlenir.", "plazma hücresi şart olup", "Kronik endometritin mutlak histopatolojik kuralı"),
        make_table("8. Bölüm Büyük Endometrit Konsolidasyon Tablosu", ["Tanısal Parametre", "Patolojik Kriter", "Klinik / Tanısal Anlamı"], [
            {"cells": [{"text": "Akut Endometrit", "isMasked": False}, {"text": "Siklus ortasında PMNL infiltrasyonu", "isMasked": True, "hint": "mid-siklus nötrofili"}, {"text": "Mikroapseler, doku yıkımı"}]},
            {"cells": [{"text": "Kronik Endometrit", "isMasked": False}, {"text": "Plazma hücresi varlığı (şarttır)", "isMasked": False}, {"text": "CD138 / CD38 pozitifliği", "isMasked": True, "hint": "immünohistokimyasal kanıt"}]},
            {"cells": [{"text": "En Sık Spesifik Etken", "isMasked": False}, {"text": "Chlamydia ve Neisseria gonorrhoeae", "isMasked": True, "hint": "klamidya ve gonore"}, {"text": "Cinsel yolla bulaşan pelvik enfeksiyon"}]},
            {"cells": [{"text": "Granülomatöz Tip", "isMasked": False}, {"text": "Mycobacterium tuberculosis", "isMasked": False}, {"text": "Kazeifiye granülom ve sterilite"}]}
        ]),
        make_chain("Bölüm 8 Tanısal Algoritma Özeti", [
            "1. Lökosit Zamanı: Siklus ortasında nötrofil varsa Akut Endometrit düşünülür.",
            "2. Alarm Sinyali: Eozinofil görülürse plazma hücresi aranmaya başlanır.",
            "3. Altın Standart: CD138 ile plazma hücresi doğrulanıp Kronik Endometrit kesinleştirilir.",
            "4. Mikrobiyal Etiyoloji: Klamidya/gonore PCR ve tüberküloz granülom taraması yapılır."
        ]),
        make_recall("8. Bölümün üç altın kuralı: Siklus ortasında PMNL neyi gösterir, kronik endometrit şartı nedir ve en sık granülomatöz etken nedir?", "Siklus ortasında PMNL akut endometriti gösterir; kronik endometrit için 'plazma hücresi şarttır'; granülomatöz endometritin en sık etkeni ise tüberkülozdur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 8. Bölüm Konsolidasyonu", [
            {"text": "Siklus ortasında PMNL görüldüğünde akut endometrit düşünülmelidir.", "isLie": False, "explanation": "Doğru. Zamanlama kriteridir."},
            {"text": "Kronik endometrit tanısı için plazma hücresi şarttır.", "isLie": False, "explanation": "Doğru. Altın kuraldır."},
            {"text": "Spesifik endometritler içinde en sık görülen etken kızamık virüsüdür ve klamidya asla enfeksiyon yapmaz.", "isLie": True, "explanation": "Tuzak! En sık görülen spesifik etkenler klamidya ve neisseria'dır; granülomatöz tip ise tüberküloza bağlıdır."},
            {"text": "Plazma hücresi tanısında CD138 ve CD38 kullanılır.", "isLie": False, "explanation": "Doğru. İHK belirteçleridir."}
        ]),
        make_quiz("Endometritler ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Plazma hücreleri normal endometriumun en bol fizyolojik hücresidir ve kronik endometritte tamamen yok olurlar", "isCorrect": True, "explanation": "Yanlış! Plazma hücreleri normal endometriumda ASLA bulunmaz; görüldüklerinde patolojiktir ve kronik endometrit tanısı için gösterilmeleri ŞARTTIR."},
            {"key": "B", "text": "Siklus ortasında PMNL görüldüğünde akut endometrit düşünülmelidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Biyopside eozinofil görülmesi plazma hücresi aranması için uyarıcıdır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Granülomatöz endometritler en sık tüberküloza bağlıdır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(80, "[TEKRAR SAYFASI - CHECKPOINT 8] Endometritler", "8. Bölümün konsolidasyonu: lökosit paradoksu, siklus ortası PMNL, plazma hücresi şartı, CD138, eozinofil alarmı ve klamidya/tüberküloz", "Bölüm Tekrarı", s80_narrative, s80_bullets, s80_elements))

    return slides
