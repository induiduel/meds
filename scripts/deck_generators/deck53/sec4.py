# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec4():
    slides = []

    # Slide 31: Tek Başına Östrojen ve %15-30 Hiperplazi Riski
    s31_narrative = (
        "Menopoz sonrası dönemde eksilen hormonları yerine koyma amacıyla uygulanan hormonal tedaviler, "
        "endometrium üzerinde derin biyolojik etkilere sahiptir.\n\n"
        "- **Karşılanmamış Östrojen:** Progesteron ile dengelenmeksizin **tek başına östrojen tedavisi "
        "alan postmenapozal kadınlarda %15-30 oranında endometrial hiperplazi** gelişmektedir.\n"
        "- **Mitotik Uyarım:** Östrojen kesintisiz bir proliferatif uyarı sağlar; progesteronun "
        "frenleyici etkisi bulunmadığında bez epitelinde aşırı birikim ve hücresel çoğalma başlar.\n"
        "- **Hormon Replasman Tedavisi (HRT):** HRT endometrial proliferasyonu doğrudan stimüle "
        "edebildiğinden, tek başına östrojen kullanımı hem hiperplazi hem de neoplazi için zemin hazırlar.\n"
        "- **Klinik Alarm:** Postmenopozal dönemde östrojen alan bir kadında anormal kanama saptandığında "
        "ilk olarak hiperplazi olasılığı akla getirilmelidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Tek başına östrojen tedavisi alan postmenapozal kadınlarda %15-30 oranında endometrial hiperplazi gelişir."
    )
    s31_bullets = [
        "Tek başına östrojen alan postmenapozal kadınlarda %15-30 endometrial hiperplazi gelişir.",
        "Progesteron ile dengelenmeyen östrojen kesintisiz proliferasyonu tetikler.",
        "Hormon replasman tedavisi endometrial proliferasyonu stimüle ederek neoplazi riskini artırabilir."
    ]
    s31_elements = [
        make_cloze("Tek başına östrojen tedavisi alan postmenapozal kadınlarda %15-30 endometrial hiperplazi gelişir.", "%15-30", "Hiperplazi gelişim yüzdesi aralığı"),
        make_table("Postmenopozal Tek Başına Östrojen Riski", ["Parametre", "Sayısal Değer / Durum", "Klinik Yansıması"], [
            {"cells": [{"text": "Kullanılan Hormon", "isMasked": False}, {"text": "Tek başına ekzojen östrojen", "isMasked": False}, {"text": "Karşılanmamış proliferatif uyarı"}]},
            {"cells": [{"text": "Hiperplazi İnsidansı", "isMasked": False}, {"text": "%15-30", "isMasked": True, "hint": "yüzde on beş ila otuz"}, {"text": "Preneoplastik risk artışı", "isMasked": True, "hint": "kanser öncülü zemin"}]},
            {"cells": [{"text": "Progesteron Desteği", "isMasked": False}, {"text": "Yok (dengelenmemiş)", "isMasked": False}, {"text": "Aşırı glandüler proliferasyon"}]}
        ]),
        make_chain("Karşılanmamış Östrojen Patogenezi", [
            "1. Ekzojen Alım: Postmenopozal kadına tek başına östrojen verilir.",
            "2. Progesteron Yokluğu: Karşılayıcı ve diferansiye edici hormon bulunmaz.",
            "3. Sürekli Mitoz: Endometrial bezler ve stroma durmaksızın çoğalır.",
            "4. Hiperplazi Gelişimi: Olguların %15-30'unda endometrial hiperplazi tablosu oturur."
        ]),
        make_recall("Tek başına östrojen tedavisi alan postmenapozal kadınlarda endometrial hiperplazi gelişme oranı nedir?", "%15-30 oranındadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Postmenopozal Östrojen Riski", [
            {"text": "Tek başına östrojen tedavisi alan postmenapozal kadınlarda %15-30 endometrial hiperplazi gelişir.", "isLie": False, "explanation": "Doğru. Klasik istatistiktir."},
            {"text": "Dengelenmemiş östrojen endometrial glandüler proliferasyonu uyarır.", "isLie": False, "explanation": "Doğru. Mitojenik etkidir."},
            {"text": "Tek başına östrojen kullanımı endometriumu kanserden %100 korur ve tüm hiperplazileri tamamen yok eder.", "isLie": True, "explanation": "Tuzak! Tek başına östrojen hiperplazi (%15-30) ve karsinom riskini belirgin şekilde ARTIRIR; koruyucu olan progesterondur."},
            {"text": "Hormon replasman tedavisi endometrial proliferasyonu stimüle edebilir.", "isLie": False, "explanation": "Doğru. Klinik mekanizmadır."}
        ]),
        make_quiz("Tek başına östrojen tedavisi alan postmenapozal kadınlarda endometrial hiperplazi gelişme sıklığı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "%15-30", "isCorrect": True, "explanation": "Ders notunda açıkça: 'tek başına östrojen tedavisi alan postmenapozal kadınlarda %15-30 endometrial hiperplazi gelişir' denmektedir."},
            {"key": "B", "text": "%0.001", "isCorrect": False, "explanation": "Çok düşüktür."},
            {"key": "C", "text": "%100 (tüm kadınlarda kesin gelişir)", "isCorrect": False, "explanation": "Oran %15-30'dur."},
            {"key": "D", "text": "Yalnızca milyonda bir kişide", "isCorrect": False, "explanation": "Yüksek risk grubudur."}
        ])
    ]
    slides.append(make_slide(31, "Tek Başına Östrojen ve %15-30 Hiperplazi Riski", "Postmenopozal östrojen replasmanı, dengelenmemiş proliferasyon ve %15-30 hiperplazi riski", "Patofizyoloji", s31_narrative, s31_bullets, s31_elements))

    # Slide 32: 10-15 Yıl Östrojen Kullanımı ve 10 Kat Kanser Riski
    s32_narrative = (
        "Uzun süreli ekzojen östrojen maruziyeti, endometrium adenokarsinomu patogenezinde kritik bir karsinojenik basamaktır.\n\n"
        "- **Süre-Risk Bağıntısı:** Yapılan epidemiyolojik çalışmalarda, ekzojen östrojen alımını takiben "
        "**10-15 yıl östrojen kullanımından sonra endometrial kanser riski 10 kat artmaktadır**.\n"
        "- **Tümörün Karakteri:** Bu uzun süreli östrojen stimülasyonu zemininde gelişen adenokarsinomlar, "
        "morfolojik olarak **genellikle düşük gradelidir (iyi diferansiye)**.\n"
        "- **Prognoz:** Bu tümörlerin klinik seyirleri ve prognozları agresif tiplere göre oldukça iyidir.\n"
        "- **Doku Belleği:** Yıllar süren östrojen maruziyeti, bez epitelinde biriken mutasyonlarla "
        "karsinogenezi adım adım tetikler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] 10-15 yıl östrojen kullanımından sonra endometrial kanser riski 10 kat artar; fakat bu kanserler genellikle düşük gradelidir ve prognozları iyidir."
    )
    s32_bullets = [
        "10-15 yıl östrojen kullanımından sonra endometrial kanser riski 10 kat artar.",
        "Östrojen zemininde gelişen bu kanserler genellikle düşük gradelidir.",
        "Düşük gradeli olmaları nedeniyle prognozları oldukça iyidir."
    ]
    s32_elements = [
        make_cloze("Yapılan çalışmalarda 10-15 yıl östrojen kullanımından sonra endometrial kanser riski 10 kat artmaktadır.", "10 kat artmaktadır", "Uzun süreli östrojenin kanser riskini artırma katı"),
        make_table("Uzun Süreli Östrojen ve Kanser Dinamikleri", ["Parametre", "Değer / Nitelik", "Klinik Özellik"], [
            {"cells": [{"text": "Kullanım Süresi", "isMasked": False}, {"text": "10-15 yıl", "isMasked": True, "hint": "on ila on beş yıllık süre"}, {"text": "Kronik maruziyet periyodu"}]},
            {"cells": [{"text": "Kanser Risk Artışı", "isMasked": False}, {"text": "10 kat artış", "isMasked": False}, {"text": "Belirgin neoplastik zemin", "isMasked": True, "hint": "on misli risk artışı"}]},
            {"cells": [{"text": "Tümör Derecesi ve Prognoz", "isMasked": False}, {"text": "Düşük gradeli, prognozu iyi", "isMasked": False}, {"text": "Endometrioid diferansiasyon"}]}
        ]),
        make_chain("Östrojenik Karsinogenez Zaman Çizelgesi", [
            "1. Başlangıç: Postmenopozal dönemde östrojen replasmanına başlanır.",
            "2. Kronik Uyarım: 10-15 yıl boyunca karşılanmamış proliferasyon devam eder.",
            "3. 10 Kat Risk: Endometrial adenokarsinom riski 10 misline fırlar.",
            "4. Diferansiye Tümör: Ortaya çıkan tümör genellikle düşük gradeli olup prognozu iyidir."
        ]),
        make_recall("10-15 yıl östrojen kullanımından sonra endometrial kanser riski kaç kat artar ve bu kanserlerin prognozu nasıldır?", "Kanser riski 10 kat artar; bu kanserler genellikle düşük gradelidir ve prognozları iyidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Uzun Süreli Östrojen ve Kanser", [
            {"text": "10-15 yıl östrojen kullanımından sonra endometrial kanser riski 10 kat artar.", "isLie": False, "explanation": "Doğru. Ders notundaki net veridir."},
            {"text": "Bu kanserler genellikle düşük gradelidir.", "isLie": False, "explanation": "Doğru. İyi diferansiye lezyonlardır."},
            {"text": "Östrojen kullanımına bağlı gelişen endometrial kanserlerin prognozu son derece kötüdür ve hastalar 2 günde ölür.", "isLie": True, "explanation": "Tuzak! Ders notunda açıkça belirtildiği gibi: bu kanserler düşük gradelidir ve prognozları İYİDİR."},
            {"text": "Ekzojen östrojen alınımını takiben adenokarsinom vakaları tespit edilmiştir.", "isLie": False, "explanation": "Doğru. Kanıtlanmış ilişkidir."}
        ]),
        make_quiz("Ekzojen östrojenin 10-15 yıl kullanımı sonrasında endometrial kanser riski ve ortaya çıkan tümörün özellikleri nasıldır?", [
            {"key": "A", "text": "Kanser riski 10 kat artar; kanserler düşük gradelidir ve prognozları iyidir", "isCorrect": True, "explanation": "Ders notunda açıkça: '10-15 yıl östrojen kullanımından sonra endometrial kanser riski 10 kat artmaktadır; fakat bu kanserler düşük gradelidir ve prognozları iyidir' denmektedir."},
            {"key": "B", "text": "Kanser riski sıfıra iner; tümörler tamamen yok olur", "isCorrect": False, "explanation": "Risk 10 kat artar."},
            {"key": "C", "text": "Kanser riski 1 milyon kat artar ve hepsi en ölümcül tiptir", "isCorrect": False, "explanation": "Abartılıdır, düşük gradeli ve iyi prognozludur."},
            {"key": "D", "text": "Yalnızca 1 ay kullanımda tümör gelişir ve prognoz kötüdür", "isCorrect": False, "explanation": "Süreç 10-15 yıl sürer."}
        ])
    ]
    slides.append(make_slide(32, "10-15 Yıl Östrojen Kullanımı ve 10 Kat Kanser Riski", "10-15 yıllık kullanım, 10 kat artan kanser riski, düşük gradeli diferansiasyon ve iyi prognoz", "Onkoloji ve Patoloji", s32_narrative, s32_bullets, s32_elements))

    # Slide 33: Progesteronun Koruyucu Rolü ve Hormon Dengesi
    s33_narrative = (
        "Endometrium patolojisinde östrojen ve progesteron arasındaki denge, neoplazi gelişiminde belirleyici unsurdur.\n\n"
        "- **Mitojenik Uyarım:** Tek başına östrojen kullanımı kontrolsüz proliferasyona yol açarak "
        "endometrial hiperplazi ve neoplaziyi tetikler.\n"
        "- **Progesteron Koruması:** Hormon replasman tedavisine **ilave progesteron eklendiğinde, "
        "endometrial hiperplazi ve karsinom insidansı belirgin şekilde azalır**.\n"
        "- **Biyolojik Fren:** Progesteron, glandüler epiteldeki östrojen reseptörlerini baskılar, "
        "mitozu durdurur ve hücreleri sekretuar diferansiasyona zorlayarak düzenli dökülmeyi sağlar.\n"
        "- **Kombine Tedavi Prensibi:** Bu nedenle uterusu yerinde olan menopozal kadınlarda östrojen "
        "tedavisi hiçbir zaman tek başına verilmemeli, mutlaka progesteron ile kombine edilmelidir.\n\n"
        "> [!NOTE]\n"
        "> Tek başına östrojen hiperplazi ve neoplazi yapar; ilave progesteron kullanımında hiperplazi ve karsinom insidansı azalır."
    )
    s33_bullets = [
        "Tek başına östrojen kullanımında endometrial hiperplazi ve neoplazi ortaya çıkar.",
        "İlave progesteron kullanımında hiperplazi ve karsinom insidansı azalır.",
        "Progesteron proliferasyonu baskılayarak koruyucu biyolojik fren işlevi görür."
    ]
    s33_elements = [
        make_cloze("Tek başına östrojen kullanımında hiperplazi ve neoplazi çıkarken, ilave progesteron kullanımında hiperplazi ve karsinom insidansı azalır.", "karsinom insidansı azalır", "Progesteronun kanser sıklığı üzerindeki koruyucu etkisi"),
        make_table("Östrojen vs Progesteron Kombinasyonu", ["Tedavi Rejimi", "Endometrial Etki", "Hiperplazi / Karsinom Riski"], [
            {"cells": [{"text": "Tek Başına Östrojen", "isMasked": False}, {"text": "Sürekli glandüler proliferasyon", "isMasked": True, "hint": "dengelenmemiş mitoz"}, {"text": "Yüksek hiperplazi ve karsinom riski"}]},
            {"cells": [{"text": "Östrojen + İlave Progesteron", "isMasked": False}, {"text": "Proliferasyon baskılanır, dökülme uyarılır", "isMasked": False}, {"text": "Hiperplazi ve karsinom insidansı azalır", "isMasked": True, "hint": "koruyucu azalma"}]}
        ]),
        make_chain("Progesteron Koruma Mekanizması", [
            "1. Östrojen Uyarısı: Bez epitelinde proliferasyon sinyali üretilir.",
            "2. Progesteron Katılımı: Eklenen progesteron nükleer reseptörlere bağlanır.",
            "3. Reseptör Down-Regülasyonu: Östrojen reseptör yoğunluğu azaltılır ve mitoz frenlenir.",
            "4. Korunma: Hiperplazi ve karsinom insidansı dramatik biçimde düşer."
        ]),
        make_recall("Hormon replasman tedavisinde tek başına östrojene ilave progesteron eklenmesinin sağladığı temel koruyucu etki nedir?", "Endometrial hiperplazi ve karsinom insidansını belirgin şekilde azaltmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Progesteronun Koruyucu Etkisi", [
            {"text": "Tek başına östrojen kullanımında endometrial hiperplazi ve neoplazi ortaya çıkar.", "isLie": False, "explanation": "Doğru. Dengelenmemiş etki sonucudur."},
            {"text": "İlave progesteron kullanımında hiperplazi ve karsinom insidansı azalır.", "isLie": False, "explanation": "Doğru. Koruyucu mekanizmadır."},
            {"text": "Progesteron verilmesi östrojenin karsinojenik etkisini 500 kat artırarak anında kanser yapar.", "isLie": True, "explanation": "Tuzak! Progesteron karsinogenezi artırmaz; tam tersine hiperplazi ve karsinom insidansını AZALTIR."},
            {"text": "Progesteron endometrial proliferasyonu baskılayıcı rol oynar.", "isLie": False, "explanation": "Doğru. Biyolojik etkisidir."}
        ]),
        make_quiz("Hormon tedavisinde tek başına östrojen yerine ilave progesteron kullanılmasının endometrial dokudaki sonucu nedir?", [
            {"key": "A", "text": "Endometrial hiperplazi ve karsinom insidansı azalır", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'ilave progesteron kullanımında hiperplazi ve karsinom insidansı azalır' denmektedir."},
            {"key": "B", "text": "Karsinom insidansı anında %100'e fırlar", "isCorrect": False, "explanation": "Aksine azalır."},
            {"key": "C", "text": "Endometrium tamamen taşlaşarak kemiğe dönüşür", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."},
            {"key": "D", "text": "Uterus 10 kat büyüyerek yırtılır", "isCorrect": False, "explanation": "Fizyolojiye aykırıdır."}
        ])
    ]
    slides.append(make_slide(33, "Progesteronun Koruyucu Rolü ve Hormon Dengesi", "Dengelenmemiş östrojen tehlikesi, progesteronun antiproliferatif etkisi ve kanser insidansında azalma", "Farmakopatoloji", s33_narrative, s33_bullets, s33_elements))

    # Slide 34: Epitelyal Metaplazilerin Genel Patolojisi
    s34_narrative = (
        "Endometrial glandlar ve stroma, çeşitli hormonal ve enflamatuar uyarılara yanıt olarak metaplastik dönüşümler gösterebilir.\n\n"
        "- **Biyolojik Nitelik:** Endometrial metaplastik değişiklikler kesinlikle **non-neoplastiktir** "
        "(kanser değildir); hücrelerin bir diferansiasyon tipinden diğerine dönüşümüdür.\n"
        "- **Etiyolojik Zemin:** Bu değişiklikler sıklıkla **hiperöstrojenizm** ile yakından ilişkilidir.\n"
        "- **Eşlik Eden Durumlar:** Poliplerde, hormon tedavisinde, RIA varlığında, kronik endometrit "
        "ve piyometrada görülebilir.\n"
        "- **Neoplazi Birlikteliği:** Endometrial hiperplazi ve adenokarsinomlara eşlik edebilirler; "
        "metaplazilerle birlikte olan adenokarsinomlar **genellikle düşük gradelidir**.\n"
        "- **Epidemiyolojik Dağılım:** Metaplaziler, endometrial karsinom açısından yüksek riskli toplumlarda daha sıktır.\n\n"
        "> [!NOTE]\n"
        "> Metaplastik değişiklikler non-neoplastiktir ve sıklıkla hiperöstrojenizmle ilişkilidir; eşlik eden kanserler genellikle düşük gradelidir."
    )
    s34_bullets = [
        "Metaplastik değişiklikler non-neoplastiktir ve sıklıkla hiperöstrojenizm ile ilişkilidir.",
        "Poliplerde, hormon tedavisinde, RIA varlığında, kronik endometritte görülebilir.",
        "Endometrial karsinomlara eşlik edebilir; bu kanserler genellikle düşük gradelidir."
    ]
    s34_elements = [
        make_cloze("Endometrial glandlar ve stromadaki metaplastik değişiklikler non-neoplastiktir ve sıklıkla hiperöstrojenizm ile ilişkilidir.", "hiperöstrojenizm", "Metaplazilerle en sık ilişkili hormonal durum"),
        make_table("Endometrial Metaplazilerin Genel Özellikleri", ["Kriter", "Özellik", "Klinik Yansıması"], [
            {"cells": [{"text": "Biyolojik Doğası", "isMasked": False}, {"text": "Non-neoplastik (benign adaptasyon)", "isMasked": True, "hint": "tümör olmama durumu"}, {"text": "Geri dönüşümlü doku yanıtı"}]},
            {"cells": [{"text": "Temel Hormonal İlişki", "isMasked": False}, {"text": "Hiperöstrojenizm", "isMasked": False}, {"text": "Aşırı östrojen uyarımı", "isMasked": True, "hint": "yüksek östrojen durumu"}]},
            {"cells": [{"text": "Karsinom Birlikteliği", "isMasked": False}, {"text": "Genellikle düşük gradeli kanserlere eşlik eder", "isMasked": False}, {"text": "İyi diferansiye tümör birlikteliği"}]}
        ]),
        make_chain("Metaplazi Gelişim Aşamaları", [
            "1. Hormonal Uyarım / İrritasyon: Hiperöstrojenizm, RIA veya kronik endometrit başlar.",
            "2. Kök Hücre Reprogramlaması: Glandüler epitel hücrelerinin farklılaşma yönü değişir.",
            "3. Metaplastik Dönüşüm: Dokuda silyalı, skuamöz veya müsinöz hücre grupları belirir.",
            "4. Birliktelik: Olguların bir kısmında eşlik eden düşük gradeli adenokarsinom saptanır."
        ]),
        make_recall("Endometrial metaplastik değişikliklerin biyolojik doğası nedir ve sıklıkla hangi hormonal durumla ilişkilidir?", "Non-neoplastiktir (benign) ve sıklıkla hiperöstrojenizm ile ilişkilidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrial Metaplaziler", [
            {"text": "Metaplastik değişiklikler non-neoplastiktir.", "isLie": False, "explanation": "Doğru. Kanser değil doku dönüşümüdür."},
            {"text": "Sıklıkla hiperöstrojenizm ile ilişkilidir.", "isLie": False, "explanation": "Doğru. En sık zemindir."},
            {"text": "Endometriumdaki tüm metaplaziler anaplastik yüksek dereceli sarkomlardır ve asla östrojenle ilişkili değildir.", "isLie": True, "explanation": "Tuzak! Metaplaziler non-neoplastiktir, sıklıkla hiperöstrojenizm ile ilişkilidir ve eşlik eden kanserler genellikle düşük gradelidir."},
            {"text": "RIA varlığında, kronik endometritte ve poliplerde izlenebilir.", "isLie": False, "explanation": "Doğru. Eşlik eden durumlardır."}
        ]),
        make_quiz("Endometrial metaplastik değişikliklerin biyolojik yapısı ve hormonal ilişkisi hakkında hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Non-neoplastiktir ve sıklıkla hiperöstrojenizm ile ilişkilidir", "isCorrect": True, "explanation": "Ders notunda açıkça: 'bunlar non-neoplastiktir ve sıklıkla hiperöstrojenizm ile ilişkilidir' denmektedir."},
            {"key": "B", "text": "Doğuştan gelen öldürücü malign metastazlardır", "isCorrect": False, "explanation": "Metaplazi malign değildir."},
            {"key": "C", "text": "Yalnızca saf androjen fazlalığında ortaya çıkar", "isCorrect": False, "explanation": "Hiperöstrojenizmle ilişkilidir."},
            {"key": "D", "text": "Endometrium dokusunda asla metaplazi gelişemez", "isCorrect": False, "explanation": "Pek çok metaplazi tipi tanımlanmıştır."}
        ])
    ]
    slides.append(make_slide(34, "Epitelyal Metaplazilerin Genel Patolojisi", "Non-neoplastik doğa, hiperöstrojenizm zemin, RIA/endometrit ilişkisi ve düşük dereceli kanser birlikteliği", "Patoloji", s34_narrative, s34_bullets, s34_elements))

    # Slide 35: Skuamöz Metaplazi (Adenoakantozis vs Adenoakantoma)
    s35_narrative = (
        "Skuamöz metaplazi, endometriumda en sık karşılaşılan epitelyal metaplazi türüdür.\n\n"
        "- **Sıklık ve Zemin:** Endometriumda **en sık görülen epitelyal metaplazidir**; normal veya "
        "hiperplastik endometriumda karşılaşılabilir, leiomyom veya poliplerle birlikte olabilir.\n"
        "- **Klinik Popülasyon:** Çoğu premenapozal dönemdeki kadınlarda ekzojen hormon alımı veya "
        "polikistik over sendromu (PCOS) ile birliktedir.\n"
        "- **Morfolojik Görünüm:** Genellikle diffüz (**adenoakantozis**) veya moruller (yuvarlak adacıklar) "
        "şeklinde bezlerin lümenlerinde izlenir.\n"
        "- **Ayırıcı Tanı (Adenoakantoma):** Glandüler yapıların benign görünümleri ile **adenoakantomadan** "
        "(skuamöz metaplazi ile birlikte olan iyi diferansiye adenokarsinom) kesin olarak ayrılır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] En sık görülen epitelyal metaplazi skuamöz metaplazidir; bezlerin benign yapısıyla adenoakantomadan (kanserden) ayrılır."
    )
    s35_bullets = [
        "Skuamöz metaplazi en sık görülen epitelyal metaplazidir.",
        "Genellikle diffüz (adenoakantozis) veya moruller şeklinde izlenir.",
        "Glandüler yapıların benign görünümü ile adenoakantomadan (kanserden) ayrılır."
    ]
    s35_elements = [
        make_cloze("Endometriumda en sık görülen epitelyal metaplazi skuamöz metaplazi olup diffüz formu adenoakantozistir.", "skuamöz metaplazi", "En sık görülen epitelyal metaplazi tipi"),
        make_table("Skuamöz Lezyonların Ayırıcı Tanısı", ["Antite", "Glandüler Epitel Yapısı", "Skuamöz Komponent"], [
            {"cells": [{"text": "Skuamöz Metaplazi (Adenoakantozis)", "isMasked": False}, {"text": "Tamamen benign glandlar", "isMasked": True, "hint": "iyi huylu bezler"}, {"text": "Benign skuamöz moruller / adacıklar"}]},
            {"cells": [{"text": "Adenoakantoma", "isMasked": False}, {"text": "İyi diferansiye adenokarsinom", "isMasked": False}, {"text": "Benign skuamöz metaplazi odakları", "isMasked": True, "hint": "malign beze eşlik eden skuamöz yapı"}]}
        ]),
        make_chain("Skuamöz Metaplazi Tanı Basamakları", [
            "1. Biyopsi İncelemesi: Bez lümenlerinde yuvarlak skuamöz moruller saptanır.",
            "2. Gland Mimarisi Kontrolü: Çevreleyen bezlerin nükleer atipisi ve invazyonu incelenir.",
            "3. Benignlik Teyidi: Bezlerin benign proliferatif görünümü doğrulanır (adenoakantozis).",
            "4. Malignite Dışlanması: Atipi saptanmadığı için adenoakantoma tanısı ekarte edilir."
        ]),
        make_recall("Endometriumda en sık görülen epitelyal metaplazi hangisidir ve adenoakantomadan nasıl ayrılır?", "Skuamöz metaplazidir; glandüler yapıların benign görünümleri ile iyi diferansiye adenokarsinom olan adenoakantomadan ayrılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Skuamöz Metaplazi", [
            {"text": "Skuamöz metaplazi endometriumda en sık görülen epitelyal metaplazidir.", "isLie": False, "explanation": "Doğru. Birinci sıradadır."},
            {"text": "Genellikle diffüz (adenoakantozis) veya moruller şeklinde izlenir.", "isLie": False, "explanation": "Doğru. Tipik histolojidir."},
            {"text": "Skuamöz metaplazi görüldüğü anda bezler incelenmeksizin doğrudan Grade 4 sarkom tanısı konur.", "isLie": True, "explanation": "Tuzak! Skuamöz metaplazi benigndir; bezlerin benign görünümü ile adenoakantomadan ayrılır."},
            {"text": "Premenapozal dönemde polikistik over veya hormon alımıyla ilişkili olabilir.", "isLie": False, "explanation": "Doğru. Etyolojik ilişkidir."}
        ]),
        make_quiz("Endometriumda en sık görülen epitelyal metaplazi türü aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Skuamöz metaplazi", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'skuamöz metaplazi en sık görülen epitelyal metaplazidir' denmektedir."},
            {"key": "B", "text": "Osseöz (kemik) metaplazisi", "isCorrect": False, "explanation": "Stromal nadir bir tiptir."},
            {"key": "C", "text": "Glial metaplazi", "isCorrect": False, "explanation": "Çok nadir mezenkimal metaplazidir."},
            {"key": "D", "text": "Mezonefrik metaplazi", "isCorrect": False, "explanation": "En sık olan skuamözdür."}
        ])
    ]
    slides.append(make_slide(35, "Skuamöz Metaplazi (Adenoakantozis vs Adenoakantoma)", "En sık epitelyal metaplazi, moruller, adenoakantozis ve adenoakantoma ayırıcı tanısı", "Patoloji", s35_narrative, s35_bullets, s35_elements))

    # Slide 36: Silyalı (Tubal) ve Sinsityal Papiller Metaplazi
    s36_narrative = (
        "Endometrium epitelinde fallop tüpünü taklit eden veya sinsityal kümeler oluşturan özgül metaplazi paternleri mevcuttur.\n\n"
        "- **Silyalı Hücreli (Tubal) Metaplazi:** Normalde endometrial mukozada az sayıda silyalı hücre bulunur. "
        "Bu hücrelerin sayıları belirgin şekilde arttığında epitel fallop tüpü (tuba uterina) epiteline benzer; "
        "**endometrial hiperplazi ile beraber daha sık görülür**.\n"
        "- **Papiller Metaplazi (Sinsityal Papiller Hiperplazi):** Yüzey epitelinde eozinofilik hücrelerin "
        "oluşturduğu **sinsityal papiller gruplar** ile karakterizedir.\n"
        "- **Uzun Süreli Östrojen:** Genellikle **uzun süreli östrojen stimülasyonu** ile birlikte izlenir.\n"
        "- **İlişkili Tablolar:** Anovulatuar disfonksiyonel uterin kanama, endometrial hiperplazi veya "
        "östrojen tedavisi alan olgularda sıkça karşımıza çıkar.\n\n"
        "> [!NOTE]\n"
        "> Tubal metaplazide silyalı hücreler artar; sinsityal papiller hiperplazi ise eozinofilik papiller gruplarla karakterizedir ve uzun süreli östrojenle ilişkilidir."
    )
    s36_bullets = [
        "Silyalı (tubal) metaplazi: silyalı hücre sayısı artar, tuba epiteline benzer; hiperplazi ile sıktır.",
        "Sinsityal papiller hiperplazi: yüzeyde eozinofilik hücrelerin oluşturduğu papiller gruplardır.",
        "Genellikle uzun süreli östrojen stimülasyonu ve anovulatuar kanamalarla ilişkilidir."
    ]
    s36_elements = [
        make_cloze("Papiller metaplazi (sinsityal papiller hiperplazi) yüzey epitelde eozinofilik hücrelerin oluşturduğu sinsityal papiller gruplar ile karakterizedir.", "sinsityal papiller gruplar", "Papiller metaplazinin histolojik kümelenmesi"),
        make_table("Tubal ve Papiller Metaplazi Karşılaştırması", ["Metaplazi Tipi", "Karakteristik Hücre / Yapı", "Hormonal ve Klinik Zemin"], [
            {"cells": [{"text": "Silyalı (Tubal) Metaplazi", "isMasked": False}, {"text": "Silyalı hücre artışı, tuba benzeri epitel", "isMasked": True, "hint": "silyalı fallop tüpü benzerliği"}, {"text": "Endometrial hiperplazi ile sık birliktelik"}]},
            {"cells": [{"text": "Sinsityal Papiller Metaplazi", "isMasked": False}, {"text": "Eozinofilik sinsityal papiller gruplar", "isMasked": False}, {"text": "Uzun süreli östrojen, anovulatuar kanama", "isMasked": True, "hint": "östrojen stimülasyonu"}]}
        ]),
        make_chain("Papiller Metaplazi Oluşumu", [
            "1. Karşılanmamış Östrojen: Uzun süre progesteronsuz östrojen uyarımı sürer.",
            "2. Epitelyal Değişim: Yüzey hücreleri eozinofilik sitoplazma kazanır.",
            "3. Tomurcuklanma: Hücreler bir araya gelerek sinsityal papiller çıkıntılar yapar.",
            "4. Histolojik Ayırım: Gerçek papiller seröz karsinomdan atipi yokluğu ile ayrılır."
        ]),
        make_recall("Yüzey epitelinde eozinofilik hücrelerin oluşturduğu sinsityal papiller gruplarla karakterize olan metaplazi hangisidir?", "Papiller metaplazidir (sinsityal papiller hiperplazi)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tubal ve Papiller Metaplazi", [
            {"text": "Silyalı hücreli metaplazi endometrial hiperplazi ile beraber daha sık görülür.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Sinsityal papiller hiperplazi eozinofilik sinsityal papiller gruplarla karakterizedir.", "isLie": False, "explanation": "Doğru. Morfolojik tanımdır."},
            {"text": "Tubal metaplazi sadece tiroid bezinde görülür, endometriumda asla tuba hücresi bulunmaz.", "isLie": True, "explanation": "Tuzak! Normal endometrial mukozada silyalı hücreler bulunur; sayıları arttığında tubal metaplazi adını alır."},
            {"text": "Sinsityal papiller metaplazi genellikle uzun süreli östrojen stimülasyonu ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Hormonal zemindir."}
        ]),
        make_quiz("Yüzey epitelinde eozinofilik hücrelerin oluşturduğu sinsityal papiller gruplarla karakterize olan ve uzun süreli östrojen uyarısıyla ilişkili lezyon hangisidir?", [
            {"key": "A", "text": "Papiller metaplazi (sinsityal papiller hiperplazi)", "isCorrect": True, "explanation": "Ders notunda kelimesi kelimesine: 'papiller metaplazi (sinsityal papiller hiperplazi): yüzey epitelde eozinofilik hücrelerin oluşturduğu sinsityal papiller gruplar ile karakterizedir; genellikle uzun süreli östrojen stimülasyonu ile görülür' denmektedir."},
            {"key": "B", "text": "Kemik iliği displazisi", "isCorrect": False, "explanation": "Hemato-onkolojik durumdur."},
            {"key": "C", "text": "Primer lökositik infiltrasyon", "isCorrect": False, "explanation": "Enflamasyon tanımıdır."},
            {"key": "D", "text": "Lipomatozis", "isCorrect": False, "explanation": "Yağ birikimidir."}
        ])
    ]
    slides.append(make_slide(36, "Silyalı (Tubal) ve Sinsityal Papiller Metaplazi", "Tubal silyalı hücre artışı, eozinofilik sinsityal papiller kümeler ve östrojen etkisi", "Patoloji", s36_narrative, s36_bullets, s36_elements))

    # Slide 37: Müsinöz ve Eozinofilik Metaplazi
    s37_narrative = (
        "Endometrium epitelinde müsin birikimi veya sitoplazmik granülasyon ile giden diğer metaplaziler histolojik tanıda dikkat gerektirir.\n\n"
        "- **Müsinöz Metaplazi:** Endometrial mukoza hücreleri intrasitoplazmik müsin vakuolleri kazanır; "
        "morfolojik, histokimyasal ve ultrastrüktürel olarak **endoservikal mukoza ile aynı görünümdedir**.\n"
        "- **Endoserviks Ayırıcı Tanısı:** Küretaj materyalinde müsinöz metaplazi saptandığında, "
        "bunun gerçek bir endometrial metaplazi mi yoksa endoservikal kanal kontaminasyonu mu olduğu ayırt edilmelidir.\n"
        "- **Eozinofilik (Oksifilik) Metaplazi:** Epitel hücrelerinin sitoplazmaları bol mitokondri içeriği "
        "nedeniyle parlak pembe-eozinofilik (onkositik/oksifilik) boyanır.\n"
        "- **Zemin:** Genellikle yaşlı hastalarda, hiperplastik glandlarda veya radyasyon/tedavi sonrasında karşılaşılabilir.\n\n"
        "> [!NOTE]\n"
        "> Müsinöz metaplazi endoservikal mukoza ile aynı görünümdedir; eozinofilik (oksifilik) metaplazi ise bol pembe sitoplazmalı hücrelerle seyreder."
    )
    s37_bullets = [
        "Müsinöz metaplazi: endometrial mukoza endoservikal mukoza ile aynı görünümdedir.",
        "Endoserviks ile morfolojik, histokimyasal ve ultrastrüktürel benzerlik gösterir.",
        "Eozinofilik (oksifilik) metaplazi: sitoplazması belirgin eozinofilik boyanan hücrelerdir."
    ]
    s37_elements = [
        make_cloze("Müsinöz metaplazide endometrial mukoza morfolojik, histokimyasal ve ultrastruktural olarak endoservikal mukoza ile aynı görünümdedir.", "endoservikal mukoza", "Müsinöz metaplazinin benzediği servikal mukoza"),
        make_table("Müsinöz ve Eozinofilik Metaplazi Kriterleri", ["Metaplazi Tipi", "Sitoplazmik Özellik", "Benzerlik / Tanısal Zorluk"], [
            {"cells": [{"text": "Müsinöz Metaplazi", "isMasked": False}, {"text": "Yoğun intraselüler müsin damlacıkları", "isMasked": True, "hint": "müsin depolanması"}, {"text": "Endoservikal mukoza ile farksız görünüm"}]},
            {"cells": [{"text": "Eozinofilik (Oksifilik) Metaplazi", "isMasked": False}, {"text": "Parlak pembe, granüler sitoplazma", "isMasked": False}, {"text": "Onkositik değişim", "isMasked": True, "hint": "mitokondri zenginliği"}]}
        ]),
        make_chain("Müsinöz Metaplazi Tanı Doğrulama", [
            "1. Biyopsi Kesiti: Bez epitelinde yüksek kolumnar müsinöz hücreler izlenir.",
            "2. Müsin Teyidi: PAS ve Alcian Blue ile nötral/asidik müsin gösterilir.",
            "3. Karşılaştırma: Endoservikal mukozaya tıpatıp benzerlik saptanır.",
            "4. Stroma Ayrımı: Hücrelerin endometrial stroma ile ilişkisi incelenerek metaplazi tanısı konur."
        ]),
        make_recall("Müsinöz metaplazide endometrial mukoza hangi anatomik yapının mukozası ile aynı görünümdedir?", "Endoservikal mukoza ile aynı görünümdedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Müsinöz ve Eozinofilik Metaplazi", [
            {"text": "Müsinöz metaplazi endoservikal mukoza ile aynı görünümdedir.", "isLie": False, "explanation": "Doğru. Karakteristik histolojik tanımıdır."},
            {"text": "Eozinofilik (oksifilik) metaplazi endometriumda görülebilen bir metaplazidir.", "isLie": False, "explanation": "Doğru. Tiplerden biridir."},
            {"text": "Müsinöz metaplazide hücreler sadece kıkırdak üretir ve içinde asla müsin bulunmaz.", "isLie": True, "explanation": "Tuzak! Müsinöz metaplazi endoservikal epitel gibi bol müsin salgılar; kıkırdak stromal metaplazide olur."},
            {"text": "Histokimyasal ve ultrastrüktürel olarak endoservikal hücrelere benzer.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Endometrial mukozanın morfolojik, histokimyasal ve ultrastrüktürel olarak endoservikal mukoza ile aynı görünümde olduğu metaplazi hangisidir?", [
            {"key": "A", "text": "Müsinöz metaplazi", "isCorrect": True, "explanation": "Ders notunda kelimesi kelimesine: 'müsinöz metaplazi: endometrial mukoza morfolojik, histokimyasal ve ultrastruktural olarak endoservikal mukoza ile aynı görünümdedir' denmektedir."},
            {"key": "B", "text": "Skuamöz metaplazi", "isCorrect": False, "explanation": "Yassı epitel oluşturur."},
            {"key": "C", "text": "Osseöz metaplazi", "isCorrect": False, "explanation": "Kemik oluşturur."},
            {"key": "D", "text": "Glial metaplazi", "isCorrect": False, "explanation": "Glial doku içerir."}
        ])
    ]
    slides.append(make_slide(37, "Müsinöz ve Eozinofilik Metaplazi", "Endoservikal mukoza benzerliği, intrasellüler müsin ve eozinofilik onkositik dönüşüm", "Patoloji", s37_narrative, s37_bullets, s37_elements))

    # Slide 38: Hobnail (Berrak Hücre) Metaplazisi ve Berrak Hücreli Karsinom Ayırıcı Tanısı
    s38_narrative = (
        "Hobnail metaplazisi, patolog için en kritik tanısal tuzaklardan birini oluşturan özgül bir metaplazi şeklidir.\n\n"
        "- **Hücresel Morfoloji:** Bu lezyonda bez epiteli berrak görünümdedir; hücrelerin **nükleusları "
        "apikal yerleşimli, lümene doğru kabarık (hobnail/ayakkabı çivisi tarzında)** ve uzun hücrelerdir.\n"
        "- **Sinonimler:** Literatürde **hobnail metaplazi, berrak hücre metaplazisi, mezonefrik veya "
        "mezonefroid metaplazi** olarak da adlandırılır.\n"
        "- **En Kritik Ayırıcı Tanı:** Bu lezyonun en hayati özelliği, histopatolojik olarak **berrak "
        "hücreli adenokarsinom (clear cell carcinoma) ile ayırıcı tanısının zorunlu olmasıdır**.\n"
        "- **Ayırım Kriteri:** Hobnail metaplazide nükleer atipi, belirgin nükleol ve invazyon bulunmazken; "
        "berrak hücreli adenokarsinom agresif ve malign bir neoplazidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Hobnail (berrak hücreli) metaplazide apikal nükleuslu uzun berrak hücreler bulunur; ayırıcı tanı berrak hücreli adenokarsinom iledir."
    )
    s38_bullets = [
        "Hobnail (berrak hücre) metaplazisi: berrak epitel, apikal yerleşimli nükleuslu uzun hücreler.",
        "Diğer isimleri: mezonefrik veya mezonefroid metaplazi.",
        "En önemli özelliği: ayırıcı tanısının berrak hücreli adenokarsinom ile yapılmasıdır."
    ]
    s38_elements = [
        make_cloze("Hobnail (berrak hücre, mezonefrik) metaplazide ayırıcı tanı berrak hücreli adenokarsinom iledir.", "berrak hücreli adenokarsinom", "Hobnail metaplazinin en kritik ayırıcı tanısı"),
        make_table("Hobnail Metaplazi vs Berrak Hücreli Adenokarsinom", ["Özellik", "Hobnail Metaplazi", "Berrak Hücreli Karsinom"], [
            {"cells": [{"text": "Biyolojik Doğası", "isMasked": False}, {"text": "Non-neoplastik metaplazi", "isMasked": True, "hint": "iyi huylu değişim"}, {"text": "Agresif malign karsinom"}]},
            {"cells": [{"text": "Nükleer Atipi", "isMasked": False}, {"text": "Yok ya da minimal", "isMasked": False}, {"text": "Belirgin pleomorfizm ve atipi", "isMasked": True, "hint": "kanser çekirdek yapısı"}]},
            {"cells": [{"text": "Nükleus Yerleşimi", "isMasked": False}, {"text": "Apikal kabarık (hobnail)", "isMasked": False}, {"text": "Değişken, malign atipik"}]}
        ]),
        make_chain("Hobnail Ayırıcı Tanı Algoritması", [
            "1. Mikroskopi: Lümene doğru kabaran nükleuslu berrak hücreler görülür.",
            "2. Atipi Analizi: Mitoz, nükleer hiperkromazi ve belirgin nükleol aranır.",
            "3. Malignite Dışlama: Şiddetli atipi yokluğu teyit edilir.",
            "4. Doğru Tanı: Berrak hücreli karsinom yerine benign hobnail metaplazi tanısı verilir."
        ]),
        make_recall("Hobnail (berrak hücre/mezonefrik) metaplazinin en kritik ve hayati ayırıcı tanısı hangi malign tümör iledir?", "Berrak hücreli adenokarsinom (clear cell adenocarcinoma) iledir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hobnail Metaplazi", [
            {"text": "Hobnail metaplazide epitel berrak görünümdedir ve nükleuslar apikal yerleşimlidir.", "isLie": False, "explanation": "Doğru. Tipik mikroskopisidir."},
            {"text": "Bu lezyon mezonefrik veya mezonefroid metaplazi olarak da adlandırılır.", "isLie": False, "explanation": "Doğru. Eş anlamlısıdır."},
            {"text": "Hobnail metaplazinin ayırıcı tanısında karsinomlar asla düşünülmez, sadece basit nezle ile karışır.", "isLie": True, "explanation": "Tuzak! Ders notunun en önemli vurgusu: Hobnail metaplazinin ayırıcı tanısı 'berrak hücreli adenokarsinom' iledir."},
            {"text": "Lümene kabarık ayakkabı çivisi (hobnail) görünümü tipiktir.", "isLie": False, "explanation": "Doğru. Morfolojik ismidir."}
        ]),
        make_quiz("Nükleusları apikal yerleşimli uzun berrak hücrelerle karakterize hobnail (mezonefrik) metaplazinin en kritik ayırıcı tanısı hangisidir?", [
            {"key": "A", "text": "Berrak hücreli adenokarsinom", "isCorrect": True, "explanation": "Ders notunda açıkça: 'hobnail (berrak hücre, mezonefrik) metaplazi: ayırıcı tanı berrak hücreli adenokarsinom iledir' denmektedir."},
            {"key": "B", "text": "Mide taşlı yüzük hücreli karsinomu", "isCorrect": False, "explanation": "Gastrointestinal kanserdir."},
            {"key": "C", "text": "Deri bazal hücreli karsinomu", "isCorrect": False, "explanation": "Cilt tümörüdür."},
            {"key": "D", "text": "Kemik osteosarkomu", "isCorrect": False, "explanation": "Kemik malignitesidir."}
        ])
    ]
    slides.append(make_slide(38, "Hobnail (Berrak Hücre) Metaplazisi ve Berrak Hücreli Karsinom Ayırıcı Tanısı", "Apikal nükleuslar, berrak sitoplazma, mezonefrik patern ve berrak hücreli adenokarsinom ayırıcı tanısı", "Patoloji", s38_narrative, s38_bullets, s38_elements))

    # Slide 39: Stromal (Mezenkimal) Metaplaziler
    s39_narrative = (
        "Endometriumdaki metaplastik potansiyel yalnızca epitelyal hücrelerle sınırlı olmayıp lamina propria stromasında da ortaya çıkar.\n\n"
        "- **Stromal Metaplazi Tanımı:** Endometrium stromasındaki fibroblastik bağ dokusunun farklı "
        "mezenkimal doku yönlerinde ayrımlaşmasıdır.\n"
        "- **Düz Kas Metaplazisi:** Stromal hücrelerin düz kas liflerine dönüşümüdür; bazen leiomyom "
        "ile ayırıcı tanı zorluğu doğurabilir.\n"
        "- **Kıkırdak ve Kemik:** Endometrium stromasında **kartilajinöz (kıkırdak) ve osseöz (kemik) "
        "metaplazi** gelişebilir; genellikle geçirilmiş küretaj veya abortus odaklarına sekonderdir.\n"
        "- **Glial ve Adipöz:** Daha nadir olarak **glial metaplazi** (sinir destek dokusu) ve **adipöz "
        "metaplazi** (matür yağ hücreleri) görülebilir.\n\n"
        "> [!NOTE]\n"
        "> Stromal metaplaziler mezenkimal kökenlidir: düz kas, kartilajinöz, osseöz, glial ve adipöz metaplazi tiplerini içerir."
    )
    s39_bullets = [
        "Endometrium stromasında mezenkimal metaplaziler gelişebilir.",
        "Düz kas metaplazisi izlenebilir.",
        "Kartilajinöz (kıkırdak), osseöz (kemik), glial ve adipöz metaplaziler mevcuttur."
    ]
    s39_elements = [
        make_cloze("Endometrium stromasında düz kas, kartilajinöz, osseöz metaplazi, glial ve adipöz metaplazi gibi mezenkimal metaplaziler izlenir.", "osseöz metaplazi", "Kemik dokusu oluşturan stromal metaplazi"),
        make_table("Stromal (Mezenkimal) Metaplazi Tipleri", ["Metaplazi Tipi", "Oluşan Matür Doku", "Klinik Özellik"], [
            {"cells": [{"text": "Düz Kas Metaplazisi", "isMasked": False}, {"text": "Düz kas hücre demetleri", "isMasked": True, "hint": "myoid farklılaşma"}, {"text": "Stromada leiomyom benzeri odak"}]},
            {"cells": [{"text": "Osseöz ve Kartilajinöz", "isMasked": False}, {"text": "Kemik ve kıkırdak dokusu", "isMasked": False}, {"text": "Küretaj veya abortus sonrası", "isMasked": True, "hint": "travma sonrası sert doku"}]},
            {"cells": [{"text": "Glial ve Adipöz", "isMasked": False}, {"text": "Glial fibriller ve matür yağ hücreleri", "isMasked": False}, {"text": "Nadir mezenkimal varyantlar"}]}
        ]),
        make_chain("Stromal Diferansiasyon Zinciri", [
            "1. Stromal Pluripotensi: Lamina propria multipotan mezenkimal kök hücreler içerir.",
            "2. Uyaran ve Travma: Kronik hormonal etki veya cerrahi girişim uygulanır.",
            "3. Diferansiasyon Değişimi: Hücreler kemik, kıkırdak veya düz kas yönüne sapar.",
            "4. Dokusal Matriks: Stromada matür kemik trabekülleri veya yağ kitleleri şekillenir."
        ]),
        make_recall("Endometrium stromasında görülebilen mezenkimal metaplazi çeşitlerinden dört tanesini belirtiniz.", "Düz kas metaplazisi, kartilajinöz (kıkırdak) metaplazi, osseöz (kemik) metaplazi, glial ve adipöz metaplazilerdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Stromal Metaplaziler", [
            {"text": "Endometrium stromasında düz kas metaplazisi görülebilir.", "isLie": False, "explanation": "Doğru. Mezenkimal tiptir."},
            {"text": "Kartilajinöz ve osseöz metaplaziler endometrium stromasında oluşabilir.", "isLie": False, "explanation": "Doğru. Kemik ve kıkırdak metaplazileridir."},
            {"text": "Endometrium stromasında asla hiçbir mezenkimal metaplazi gelişemez, stroma tamamen taşlaşmış granittir.", "isLie": True, "explanation": "Tuzak! Endometrium stromasında düz kas, kemik, kıkırdak, glial ve adipöz metaplaziler gösterilmiştir."},
            {"text": "Glial ve adipöz metaplazi stromal metaplaziler arasında yer alır.", "isLie": False, "explanation": "Doğru. Ders notu listesindedir."}
        ]),
        make_quiz("Endometrium lamina propriasında görülebilen stromal (mezenkimal) metaplaziler arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Düz kas, kartilajinöz (kıkırdak), osseöz (kemik), glial ve adipöz metaplazi", "isCorrect": True, "explanation": "Ders notunda stromal metaplaziler olarak aynen bu liste sayılmıştır."},
            {"key": "B", "text": "Yalnızca retina çomak hücre metaplazisi", "isCorrect": False, "explanation": "Göz dokusudur."},
            {"key": "C", "text": "Pankreas adacık hücresi metaplazisi", "isCorrect": False, "explanation": "Endokrin bez dokusudur."},
            {"key": "D", "text": "Kardiyak purkinje lif metaplazisi", "isCorrect": False, "explanation": "Kalp ileti sistemidir."}
        ])
    ]
    slides.append(make_slide(39, "Stromal (Mezenkimal) Metaplaziler", "Lamina propria diferansiasyonu, düz kas, osseöz, kartilajinöz, glial ve adipöz metaplaziler", "Patoloji", s39_narrative, s39_bullets, s39_elements))

    # Slide 40: [TEKRAR SAYFASI - CHECKPOINT 4] Hormonal Etkiler ve Epitelyal Metaplaziler
    s40_narrative = (
        "Bu tekrar sayfasında 4. Bölüm boyunca incelediğimiz östrojenin hiperplastik risklerini, "
        "kanser süre-kat bağıntısını, progesteronun koruyucu gücünü ve tüm metaplazi tiplerini konsolide ediyoruz.\n\n"
        "- **Hormonal Riskler:** Postmenopozal tek başına östrojen %15-30 hiperplazi yapar; 10-15 yıl "
        "kullanım kanser riskini 10 kat artırır (kanserler düşük gradelidir, prognoz iyidir); progesteron "
        "ilavesi insidansı belirgin azaltır.\n"
        "- **Epitelyal Metaplaziler:** Non-neoplastiktir, hiperöstrojenizmle ilişkilidir; en sık görüleni "
        "skuamöz metaplazidir (adenoakantomadan benign bezlerle ayrılır).\n"
        "- **Özgül Epitelyal Tipler:** Silyalı (tubal) hiperplaziyle sıktır; sinsityal papiller uzun süreli "
        "östrojenle eozinofilik papiller gruplar yapar; müsinöz endoservikse benzer; hobnail metaplazisi "
        "ise berrak hücreli adenokarsinom ile kritik ayırıcı tanı gerektirir.\n"
        "- **Stromal Tipler:** Düz kas, kartilajinöz, osseöz, glial ve adipöz mezenkimal metaplaziler.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] %15-30 hiperplazi; 10-15 yılda 10 kat kanser; progesteron koruyucu; En sık skuamöz metaplazi; Hobnail ayırıcı tanısı berrak hücreli adenokarsinom iledir."
    )
    s40_bullets = [
        "Tek başına östrojen: %15-30 hiperplazi; 10-15 yıl kullanımda 10 kat kanser riski (düşük gradeli, prognoz iyi).",
        "İlave progesteron koruyucudur; en sık epitelyal metaplazi skuamöz metaplazidir.",
        "Hobnail metaplazide ayırıcı tanı berrak hücreli karsinom iledir; stromal metaplaziler kemik, kıkırdak ve düz kas içerir."
    ]
    s40_elements = [
        make_cloze("En sık görülen epitelyal metaplazi skuamöz metaplazi iken hobnail metaplazide ayırıcı tanı berrak hücreli adenokarsinom iledir.", "skuamöz metaplazi", "En sık görülen epitelyal metaplazi türü"),
        make_table("4. Bölüm Büyük Metaplazi ve Risk Tablosu", ["Lezyon / Durum", "Karakteristik Özellik", "Klinik / Ayırıcı Tanı Önemi"], [
            {"cells": [{"text": "Tek Başına Östrojen", "isMasked": False}, {"text": "%15-30 hiperplazi, 10-15 yılda 10 kat kanser", "isMasked": True, "hint": "yüzde on beş otuz hiperplazi"}, {"text": "Düşük gradeli, iyi prognozlu tümör"}]},
            {"cells": [{"text": "Skuamöz Metaplazi", "isMasked": False}, {"text": "En sık görülen epitelyal metaplazi (moruller)", "isMasked": False}, {"text": "Adenoakantomadan benign bezlerle ayrılır", "isMasked": True, "hint": "kanserden ayırım kriteri"}]},
            {"cells": [{"text": "Hobnail Metaplazi", "isMasked": False}, {"text": "Apikal nükleuslu berrak uzun hücreler", "isMasked": False}, {"text": "Berrak hücreli adenokarsinom ayırıcı tanısı", "isMasked": True, "hint": "clear cell kanser ayırımı"}]},
            {"cells": [{"text": "Stromal Metaplaziler", "isMasked": False}, {"text": "Düz kas, kıkırdak, kemik, glia, yağ", "isMasked": True, "hint": "mezenkimal doku tipleri"}, {"text": "Mezenkimal benign diferansiasyon"}]}
        ]),
        make_chain("Bölüm 4 Konsolidasyon Akışı", [
            "1. Hormonal Aşırılık: Tek başına östrojenle %15-30 hiperplazi tetiklenir.",
            "2. Süreklilik ve Kanser: 10-15 yıl sonra 10 kat düşük gradeli kanser riski doğar.",
            "3. Epitelyal Dönüşüm: En başta skuamöz olmak üzere tubal, papiller, müsinöz metaplaziler gelişir.",
            "4. Kritik Tuzak: Hobnail metaplazi berrak hücreli karsinomdan atipi yokluğuyla ayrılır."
        ]),
        make_recall("4. Bölümün iki altın bilgisi: En sık görülen epitelyal metaplazi hangisidir ve hobnail metaplazinin ayırıcı tanısı ne iledir?", "En sık görülen skuamöz metaplazidir; hobnail metaplazinin ayırıcı tanısı ise berrak hücreli adenokarsinom iledir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 4. Bölüm Konsolidasyonu", [
            {"text": "Tek başına östrojen alan postmenapozal kadınlarda %15-30 hiperplazi gelişir.", "isLie": False, "explanation": "Doğru. Ders notu verisidir."},
            {"text": "Skuamöz metaplazi en sık görülen epitelyal metaplazidir.", "isLie": False, "explanation": "Doğru. Birinci sıradadır."},
            {"text": "Hobnail metaplazinin ayırıcı tanısı asla berrak hücreli karsinomla yapılmaz, sadece apandisit ile karışır.", "isLie": True, "explanation": "Tuzak! Hobnail metaplazinin ayırıcı tanısı berrak hücreli adenokarsinom iledir."},
            {"text": "Endometrium stromasında osseöz (kemik) ve kartilajinöz (kıkırdak) metaplazi izlenebilir.", "isLie": False, "explanation": "Doğru. Stromal tiplerdir."}
        ]),
        make_quiz("Hormonal etkiler ve metaplaziler ile ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Hobnail metaplazi: ayırıcı tanı berrak hücreli adenokarsinom ile yapılır", "isCorrect": False, "explanation": "Doğru bir eşleştirmedir."},
            {"key": "B", "text": "Skuamöz metaplazi: en sık görülen epitelyal metaplazidir", "isCorrect": False, "explanation": "Doğru bir eşleştirmedir."},
            {"key": "C", "text": "10-15 yıl östrojen kullanımı: endometrial kanser riskini 10 kat artırır", "isCorrect": False, "explanation": "Doğru bir eşleştirmedir."},
            {"key": "D", "text": "Tek başına östrojen: hiperplazi riskini sıfırlar ve progesteron kanser yapar", "isCorrect": True, "explanation": "Yanlış! Tek başına östrojen %15-30 hiperplazi yapar; ilave progesteron hiperplazi ve kanseri azaltır."}
        ])
    ]
    slides.append(make_slide(40, "[TEKRAR SAYFASI - CHECKPOINT 4] Hormonal Etkiler ve Epitelyal Metaplaziler", "4. Bölümün konsolidasyonu: %15-30 hiperplazi, 10 kat kanser, progesteron freni, skuamöz ve hobnail ayırıcı tanısı", "Bölüm Tekrarı", s40_narrative, s40_bullets, s40_elements))

    return slides
