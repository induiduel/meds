# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec6():
    slides = []

    # Slide 51: Kateterle İlişkili ÜSE (Kİ-ÜSE) Tanımı ve Zaman Kriteri
    s51_narrative = (
        "Sağlık bakımı ilişkili enfeksiyonlar arasında en yüksek insidansa sahip tablolardan biri, "
        "üriner kateter uygulamalarına bağlı olarak gelişen enfeksiyonlardır.\n\n"
        "- **Kİ-ÜSE Tanımı:** Kateterle ilişkili üriner sistem enfeksiyonu (Kİ-ÜSE), **üriner kateteri "
        "olan veya son 48 saat içinde kateter takılma öyküsü olan kişide** gelişen ÜSE'dir.\n"
        "- **Zaman Penceresi:** Kateterin çıkarılmasının üzerinden 48 saatten az süre geçmiş bir hastada "
        "ortaya çıkan idrar yolu enfeksiyonu da patofizyolojik olarak Kİ-ÜSE kapsamında değerlendirilir.\n"
        "- **Klinik Önem:** Kateter, mukozal bariyeri mekanik olarak delip doğrudan mesaneye yabancı "
        "bir cisim yerleştirdiği için patojen girişini dramatik olarak kolaylaştırır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kİ-ÜSE: Üriner kateteri olan veya son 48 saat içinde kateter takılma öyküsü olan kişide gelişen üriner sistem enfeksiyonudur."
    )
    s51_bullets = [
        "Kİ-ÜSE: Üriner kateteri olan veya son 48 saat içinde kateter öyküsü olan kişide gelişir.",
        "Kateter çekildikten sonraki ilk 48 saatlik dönem de bu tanı tanımına dahildir.",
        "Hastane kaynaklı bakteriyemilerin en sık başlangıç odaklarından biridir."
    ]
    s51_elements = [
        make_cloze("Kİ-ÜSE, üriner kateteri olan veya son 48 saat içinde kateter takılma öyküsü olan kişide gelişen ÜSE'dir.", "son 48 saat içinde", "Kateter çıkarıldıktan sonra enfeksiyonun Kİ-ÜSE sayıldığı kritik zaman penceresi"),
        make_table("Kİ-ÜSE Zaman ve Tanım Kriterleri", ["Hasta Durumu", "Kateter Zamanlaması", "Klinik Sınıflama"], [
            {"cells": [{"text": "Mevcut Kateterli", "isMasked": False}, {"text": "Kateter halihazırda takılı", "isMasked": True, "hint": "kateteri bulunan hasta"}, {"text": "Aktif Kİ-ÜSE riski"}]},
            {"cells": [{"text": "Kateteri Çıkarılmış", "isMasked": False}, {"text": "Son 48 saat içinde çekilmiş", "isMasked": False}, {"text": "Kİ-ÜSE kapsamında kabul edilir", "isMasked": True, "hint": "kırk sekiz saat kuralı"}]}
        ]),
        make_chain("Kİ-ÜSE Tanısal Zaman Akışı", [
            "1. Kateterizasyon: İdrar sondası takılması.",
            "2. Takip veya Çekilme: Kateterin takılı kalması veya çekilmesi.",
            "3. 48 Saatlik Pencere: Çekildikten sonraki ilk 48 saatte semptom gelişimi.",
            "4. Tanı: Kİ-ÜSE olarak sınıflanıp tedavi protokolünün başlatılması."
        ]),
        make_recall("Kİ-ÜSE (Kateterle ilişkili ÜSE) tanımındaki kateter öyküsü zaman kriteri nedir?", "Üriner kateteri olan veya son 48 saat içinde kateter takılma öyküsü olan kişidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kİ-ÜSE Tanımı", [
            {"text": "Kİ-ÜSE üriner kateteri olan kişilerde gelişen ÜSE'dir.", "isLie": False, "explanation": "Doğru. Temel tanımdır."},
            {"text": "Son 48 saat içinde kateter takılma öyküsü olan hastalar da bu tanıma dahildir.", "isLie": False, "explanation": "Doğru. 48 saatlik penceredir."},
            {"text": "Kateteri 10 yıl önce çekilmiş bir hastadaki akut sistit mutlaka Kİ-ÜSE kabul edilir.", "isLie": True, "explanation": "Tuzak! Kİ-ÜSE zaman kriteri 'son 48 saat içinde' kateter takılma öyküsüdür."},
            {"text": "Kateter lümeni bakterilerin mesaneye tırmanmasını kolaylaştırır.", "isLie": False, "explanation": "Doğru. Asendan yoldur."}
        ]),
        make_quiz("Kateterle ilişkili üriner sistem enfeksiyonu (Kİ-ÜSE) tanımında yer alan kateter öyküsü süresi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Üriner kateteri olan veya son 48 saat içinde kateter takılma öyküsü olan", "isCorrect": True, "explanation": "Ders notundaki birebir tanımdır: 'Üriner kateteri olan veya son 48 saat içinde kateter takılma öyküsü olan kişide gelişen ÜSE'dir'."},
            {"key": "B", "text": "Yalnızca son 6 ay içinde kateter takılanlar", "isCorrect": False, "explanation": "Süre 48 saattir."},
            {"key": "C", "text": "Kateteri hiç olmamış ve asla takılmayacak olanlar", "isCorrect": False, "explanation": "Kİ-ÜSE kateterle ilişkilidir."},
            {"key": "D", "text": "Sadece 10 yaş altındaki sünnetsiz çocuklar", "isCorrect": False, "explanation": "Tanım süreye ve katetere bağlıdır."}
        ])
    ]
    slides.append(make_slide(51, "Kateterle İlişkili ÜSE (Kİ-ÜSE) Tanımı", "Kİ-ÜSE tanımı, mevcut kateter ve son 48 saat kuralının önemi", "Kİ-ÜSE", s51_narrative, s51_bullets, s51_elements))

    # Slide 52: En Önemli Risk Faktörü: Kateter Süresi
    s52_narrative = (
        "Kateterize hastalarda bakteriüri ve semptomatik enfeksiyon gelişiminde birçok değişken "
        "rol oynasa da, bir parametre diğer tüm faktörleri geride bırakır.\n\n"
        "- **En Önemli Risk:** Kİ-ÜSE gelişiminde **kateter süresi en önemli risk faktörüdür**.\n"
        "- **Günlük Risk Artışı:** Kateterin mesanede kaldığı her geçen gün bakteriüri riski yaklaşık "
        "%3-7 oranında artış gösterir ve 30. günün sonunda neredeyse tüm hastalarda bakteriüri gelişir.\n"
        "- **Önleme Stratejisi:** Kateterle ilişkili enfeksiyonları önlemenin en etkili ve kanıtlanmış "
        "yolu, kateter endikasyonunu her gün sorgulamak ve kateteri mümkün olan en kısa sürede çekmektir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) EN ÖNEMLİ risk faktörü: Kateter süresidir."
    )
    s52_bullets = [
        "Kateter süresi en önemli risk faktörüdür.",
        "Kateter kaldığı sürece günlük kümülatif kolonizasyon riski artar.",
        "Kateterin gereksiz yere takılı kalmasının önlenmesi temel koruyucu tedbirdir."
    ]
    s52_elements = [
        make_cloze("Kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) en önemli risk faktörü kateter süresidir.", "kateter süresidir", "Kateterin mesanede takılı kalma gün sayısı"),
        make_table("Kİ-ÜSE Risk Faktörleri ve Öncelik Hiyerarşisi", ["Risk Faktörü", "Önem Düzeyi", "Klinik Karar"], [
            {"cells": [{"text": "Kateter Süresi", "isMasked": False}, {"text": "En önemli risk faktörü", "isMasked": True, "hint": "birinci sıradaki risk unsuru"}, {"text": "Gereksiz kateter derhal çekilmeli"}]},
            {"cells": [{"text": "Takılış Şekli / Bakım", "isMasked": False}, {"text": "Önemli destekleyici faktör", "isMasked": False}, {"text": "Aseptik teknik ve kapalı drenaj", "isMasked": True, "hint": "steril uygulama kuralları"}]}
        ]),
        make_chain("Kateter Süresi ve Kolonizasyon Dinamiği", [
            "1. Kateter Takılması: Yabancı cismin üretral yolla mesaneye yerleşmesi.",
            "2. Günlük Kolonizasyon: İntraluminal ve ekstraluminal bakteri tırmanışı.",
            "3. Biyofilm Kalınlaşması: Günler içinde silikon yüzeyde mikrobiyal tabaka.",
            "4. Kİ-ÜSE: Süre uzadıkça enfeksiyonun kaçınılmaz hale gelmesi."
        ]),
        make_recall("Kİ-ÜSE gelişiminde ders notunda açıkça vurgulanan 'en önemli risk faktörü' nedir?", "Kateter süresidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kateter Süresi", [
            {"text": "Kateter süresi Kİ-ÜSE'de en önemli risk faktörüdür.", "isLie": False, "explanation": "Doğru. Ders notunun en temel spotudur."},
            {"text": "Kateterin takılı kaldığı süre uzadıkça enfeksiyon riski artar.", "isLie": False, "explanation": "Doğru. Kümülatif risk artışı vardır."},
            {"text": "Kateterin mesanede 5 yıl boyunca hiç çıkarılmadan kalması enfeksiyon riskini sıfıra indirir.", "isLie": True, "explanation": "Tuzak! Tam aksine kateter süresi uzadıkça enfeksiyon riski %100'e yaklaşır, en önemli risk faktörüdür."},
            {"text": "Kateterin erken çekilmesi enfeksiyonu önlemede en kritik adımdır.", "isLie": False, "explanation": "Doğru. Temel koruyucu yaklaşımdır."}
        ]),
        make_quiz("Kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) EN ÖNEMLİ risk faktörü aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Kateter süresi", "isCorrect": True, "explanation": "Ders notunda net olarak 'Kateter süresi en önemli risk faktörüdür' ifadesi yer almaktadır."},
            {"key": "B", "text": "Hastanın göz rengi", "isCorrect": False, "explanation": "Klinik risk faktörü değildir."},
            {"key": "C", "text": "Hastanenin bulunduğu coğrafi rakım", "isCorrect": False, "explanation": "Kİ-ÜSE ile ilgisizdir."},
            {"key": "D", "text": "Kateter torbasının rengi", "isCorrect": False, "explanation": "Risk faktörü kateterin kalış süresidir."}
        ])
    ]
    slides.append(make_slide(52, "Kİ-ÜSE'de En Önemli Risk Faktörü: Kateter Süresi", "Kateter kalış süresinin kümülatif riski ve biyofilm oluşumuna etkisi", "Kİ-ÜSE", s52_narrative, s52_bullets, s52_elements))

    # Slide 53: Kİ-ÜSE Mikrobiyolojik Özelliği: Polimikrobiyalite ve ÇİD
    s53_narrative = (
        "Toplum kökenli sistit olgularında neredeyse her zaman tek bir bakteri izole edilirken, "
        "kateterli hastalarda mikrobiyolojik manzara son derece karmaşık bir yapı kazanır.\n\n"
        "- **Polimikrobiyal Yapı:** Kİ-ÜSE enfeksiyonları **sıklıkla polimikrobiyaldir**; yani idrar "
        "kültüründe aynı anda iki veya daha fazla farklı mikroorganizma ürer.\n"
        "- **Çok İlaca Direnç:** Bu enfeksiyonlar sıklıkla **çok ilaca dirençli (ÇİD) patojenlerle "
        "ilişkilidir** ve standart antibiyotiklere yanıt vermez.\n"
        "- **Biyofilm Ortaklığı:** Kateter yüzeyinde oluşan biyofilm matrisi içerisinde farklı türden "
        "bakteriler bir arada yaşayarak genetik plazmid transferi ile direnç genlerini paylaşır.\n\n"
        "> [!IMPORTANT]\n"
        "> Kateterle ilişkili enfeksiyonlar sıklıkla polimikrobiyaldir ve çok ilaca dirençli (ÇİD) patojenlerle yakından ilişkilidir."
    )
    s53_bullets = [
        "Kİ-ÜSE enfeksiyonları sıklıkla polimikrobiyaldir.",
        "Çok ilaca dirençli (ÇİD) patojenlerle ilişkilidir.",
        "Kateter biyofilmi farklı türlerin bir arada direnç geliştirmesine zemin hazırlar."
    ]
    s53_elements = [
        make_cloze("Kateterle ilişkili üriner sistem enfeksiyonları sıklıkla polimikrobiyaldir ve çok ilaca dirençli patojenlerle ilişkilidir.", "polimikrobiyaldir", "Birden fazla farklı mikrop türünün aynı anda üremesi"),
        make_table("Kİ-ÜSE Mikrobiyolojik Profili", ["Özellik", "Kİ-ÜSE Karakteri", "Toplum Kökenli Karşılaştırması"], [
            {"cells": [{"text": "Etken Sayısı", "isMasked": False}, {"text": "Sıklıkla polimikrobiyal (≥2 tür)", "isMasked": True, "hint": "birden fazla bakteri türü"}, {"text": "Mononükleer/tek bakteri baskın"}]},
            {"cells": [{"text": "Direnç Durumu", "isMasked": False}, {"text": "Çok ilaca dirençli (ÇİD) patojenler", "isMasked": False}, {"text": "Daha duyarlı suşlar", "isMasked": True, "hint": "standart antibiyotiğe duyarlılık"}]}
        ]),
        make_chain("Polimikrobiyal Kolonizasyon Süreci", [
            "1. Kateter Yerleşimi: Lümen içi ve dışı yüzeyin açılması.",
            "2. İlk Kolonizasyon: Birincil bakterinin katetere tutunması.",
            "3. Biyofilm Matrisi: Diğer fırsatçı türlerin biyofilme katılması.",
            "4. Polimikrobiyal ÇİD: Birden fazla dirençli bakterinin enfeksiyon yapması."
        ]),
        make_recall("Kİ-ÜSE'lerin etken sayısı ve direnç yapısı bakımından iki temel özelliği nedir?", "Sıklıkla polimikrobiyaldir ve çok ilaca dirençli (ÇİD) patojenlerle ilişkilidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Polimikrobiyalite ve ÇİD", [
            {"text": "Kİ-ÜSE enfeksiyonları sıklıkla polimikrobiyaldir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Kİ-ÜSE çok ilaca dirençli patojenlerle ilişkilidir.", "isLie": False, "explanation": "Doğru. Direnç oranı çok yüksektir."},
            {"text": "Kİ-ÜSE'de idrarda asla iki bakteri bir arada yaşayamaz, biri diğerini 1 saniyede yutar.", "isLie": True, "explanation": "Tuzak! Kİ-ÜSE sıklıkla polimikrobiyaldir; birden fazla bakteri türü biyofilmde birlikte yaşar."},
            {"text": "Biyofilm yapısı antibiyotik direncini artıran önemli bir bariyerdir.", "isLie": False, "explanation": "Doğru. Penetrasyonu bozar."}
        ]),
        make_quiz("Kateterle ilişkili üriner sistem enfeksiyonlarının (Kİ-ÜSE) mikrobiyolojik özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Sıklıkla polimikrobiyaldir ve çok ilaca dirençli patojenlerle ilişkilidir", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Enfeksiyonlar sıklıkla polimikrobiyaldir ve çok ilaca dirençli patojenlerle ilişkilidir' denmektedir."},
            {"key": "B", "text": "Her zaman tek bir duyarlı bakteriyle seyreder", "isCorrect": False, "explanation": "Sıklıkla polimikrobiyal ve dirençlidir."},
            {"key": "C", "text": "Hiçbir zaman antibiyotik tedavisi gerektirmez", "isCorrect": False, "explanation": "Kİ-ÜSE klinik enfeksiyon tablosudur."},
            {"key": "D", "text": "Yalnızca A grubu beta hemolitik streptokoklarla oluşur", "isCorrect": False, "explanation": "Dirençli Gram negatifler ve enterokoklar sıktır."}
        ])
    ]
    slides.append(make_slide(53, "Kİ-ÜSE'de Polimikrobiyalite ve Direnç", "Polimikrobiyal enfeksiyon karakteri ve çok ilaca dirençli (ÇİD) patojenler", "Kİ-ÜSE", s53_narrative, s53_bullets, s53_elements))

    # Slide 54: Kİ-ÜSE Etiyolojik Ajan Yelpazesi
    s54_narrative = (
        "Kateter varlığı, normalde üriner traktusta nadiren enfeksiyon yapan birçok fırsatçı ve "
        "hastane kaynaklı patojenin kolonize olmasına olanak tanır.\n\n"
        "- **Bakteriyel Yelpaze:** Kİ-ÜSE'de etkenler polimikrobiyal enfeksiyon zemininde **E. coli, "
        "Providencia, Proteus, Morganella, Pseudomonas, Acinetobacter** türleridir.\n"
        "- **Gram Pozitif Direnç:** Gram pozitif etkenler arasında ise özellikle **MRSA (metisiline "
        "dirençli S. aureus)** ve **dirençli enterokoklar (VRE vb.)** ön plana çıkar.\n"
        "- **Klinik Güçlük:** Morganella morganii veya Providencia stuartii gibi bakteriler biyofilm "
        "üreterek kateterin lümenini tıkayabilir ve taş oluşumuna katkıda bulunabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kİ-ÜSE etkenleri: E. coli, Providencia, Proteus, Morganella, Pseudomonas, Acinetobacter, MRSA ve dirençli enterokoklardır."
    )
    s54_bullets = [
        "Etkenler: E. coli, Providencia, Proteus, Morganella, Pseudomonas, Acinetobacter.",
        "Gram pozitif dirençli etkenler: MRSA ve dirençli enterokoklar.",
        "Bu patojenler kateter yüzeylerinde biyofilm oluşturarak kalıcılık sağlar."
    ]
    s54_elements = [
        make_cloze("Kİ-ÜSE etkenleri arasında Providencia, Proteus, Morganella, Pseudomonas, Acinetobacter, MRSA ve dirençli enterokoklar yer alır.", "Providencia, Proteus, Morganella", "Kateter enfeksiyonlarında sık görülen enterik üçlü"),
        make_table("Kİ-ÜSE Patojen Grupları", ["Patojen Grubu", "Örnek Bakteriler", "Özel Direnç / Klinik Nitelik"], [
            {"cells": [{"text": "Gram Negatif Basiller", "isMasked": False}, {"text": "Providencia, Morganella, Proteus, E. coli", "isMasked": True, "hint": "enterik çomaklar"}, {"text": "Üreaz üretimi ve biyofilm oluşumu"}]},
            {"cells": [{"text": "Non-fermentatifler", "isMasked": False}, {"text": "Pseudomonas ve Acinetobacter", "isMasked": False}, {"text": "Yoğun bakım ve çoklu antibiyotik direnci", "isMasked": True, "hint": "hastane kökenli direnç devleri"}]},
            {"cells": [{"text": "Dirençli Gram Pozitifler", "isMasked": False}, {"text": "MRSA ve dirençli enterokoklar", "isMasked": True, "hint": "dirençli stafilokok ve enterokok"}, {"text": "Glikopeptid ihtiyacı doğuran etkenler"}]}
        ]),
        make_chain("Kİ-ÜSE Patojen Çeşitlenmesi", [
            "1. Kateter Girişi: Dış ortamdan yabancı materyalin mesaneye uzanması.",
            "2. Nozokomiyal Temas: Providencia, Morganella ve Pseudomonas girişi.",
            "3. Gram Pozitif Süperenfeksiyon: MRSA ve dirençli enterokok kolonizasyonu.",
            "4. Polimikrobiyal ÇİD: Çoklu etkenle karmaşık sepsise yatkınlık."
        ]),
        make_recall("Ders notuna göre Kİ-ÜSE'de izole edilen başlıca patojenler hangileridir?", "E. coli, Providencia, Proteus, Morganella, Pseudomonas, Acinetobacter, MRSA ve dirençli enterokoklardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kİ-ÜSE Patojenleri", [
            {"text": "Providencia ve Morganella Kİ-ÜSE etkenleri arasında sayılır.", "isLie": False, "explanation": "Doğru. Ders notu patojenleridir."},
            {"text": "Acinetobacter ve Pseudomonas dirençli Kİ-ÜSE etkenlerindendir.", "isLie": False, "explanation": "Doğru. Nozokomiyal basillerdir."},
            {"text": "Kİ-ÜSE'de MRSA ve dirençli enterokoklar hiçbir zaman bulunmaz, sadece çiçek poleni ürer.", "isLie": True, "explanation": "Tuzak! MRSA ve dirençli enterokoklar Kİ-ÜSE'nin önemli Gram pozitif etkenleridir."},
            {"text": "Kİ-ÜSE patojenleri polimikrobiyal olarak bir arada bulunabilir.", "isLie": False, "explanation": "Doğru. Çoklu üreme sıktır."}
        ]),
        make_quiz("Ders notuna göre kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) rol oynayan etkenler arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "E. coli, Providencia, Proteus, Morganella, Pseudomonas, Acinetobacter, MRSA, dirençli enterokoklar", "isCorrect": True, "explanation": "Ders notundaki eksiksiz Kİ-ÜSE patojen listesidir."},
            {"key": "B", "text": "Yalnızca Bordetella ve Brucella", "isCorrect": False, "explanation": "Kİ-ÜSE patojenleri değildir."},
            {"key": "C", "text": "Sadece Vibrio cholerae", "isCorrect": False, "explanation": "Kolera bağırsak hastalığıdır."},
            {"key": "D", "text": "Clostridium botulinum", "isCorrect": False, "explanation": "Botulizm toksini üretir, Kİ-ÜSE etkeni değildir."}
        ])
    ]
    slides.append(make_slide(54, "Kİ-ÜSE Etiyolojik Ajan Yelpazesi", "Providencia, Morganella, Pseudomonas, Acinetobacter, MRSA ve enterokoklar", "Kİ-ÜSE", s54_narrative, s54_bullets, s54_elements))

    # Slide 55: Kİ-ÜSE Klinik Bulguları: Kateter Takılı İken
    s55_narrative = (
        "Kateteri olan hastalarda klasik alt üriner sistem semptomları (dizüri, sık idrara çıkma) "
        "kateter balonu ve drenajı nedeniyle maskelendiğinden klinik bulgular daha sistemiktir.\n\n"
        "- **Sistemik Bulgular:** Kateteri takılı olan hastada Kİ-ÜSE şüphesi uyandıran bulgular: **yeni "
        "başlayan ateş, titreme, mental durum değişikliği, halsizlik/letarji** (başka neden yoksa).\n"
        "- **Lokal / Bölgesel Bulgular:** Üst veya alt üriner traktus tutulumuna işaret eden **yan ağrısı, "
        "kostavertebral açı (KVA) hassasiyeti, akut hematüri ve pelvik rahatsızlık**tır.\n"
        "- **Mental Değişiklik:** Özellikle geriatrik ve yoğun bakım hastalarında başka bir odak bulunmaksızın "
        "ortaya çıkan bilinç bulanıklığı ve letarji Kİ-ÜSE'nin ilk ve tek prezentasyonu olabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> Kateteri olan hastada Kİ-ÜSE kliniği: Yeni başlayan ateş, titreme, mental durum değişikliği, halsizlik/letarji, yan ağrısı, KVA hassasiyeti, akut hematüri ve pelvik rahatsızlıktır."
    )
    s55_bullets = [
        "Sistemik: Yeni başlayan ateş, titreme, mental durum değişikliği, halsizlik/letarji.",
        "Bölgesel/Lokal: Yan ağrısı, KVA hassasiyeti, akut hematüri, pelvik rahatsızlık.",
        "Yaşlı hastalarda mental durum değişikliği ve letarji tek erken bulgu olabilir."
    ]
    s55_elements = [
        make_cloze("Kateteri takılı hastada Kİ-ÜSE kliniğinde yeni başlayan ateş, titreme, mental durum değişikliği ve halsizlik/letarji görülebilir.", "mental durum değişikliği", "Bilinç ve kognitif fonksiyonlarda akut bozulma"),
        make_table("Kateter Takılı İken Kİ-ÜSE Belirtileri", ["Belirti Kategorisi", "Klinik Bulgular", "Fizyopatolojik Neden"], [
            {"cells": [{"text": "Sistemik Belirtiler", "isMasked": False}, {"text": "Ateş, titreme, letarji, mental değişiklik", "isMasked": True, "hint": "genel vücut yanıtı bulguları"}, {"text": "Sitokin salınımı ve bakteriyemi riski"}]},
            {"cells": [{"text": "Renal ve Pelvik", "isMasked": False}, {"text": "Yan ağrısı, KVAH, akut hematüri", "isMasked": False}, {"text": "Parankim invazyonu ve mukoza nekrozu", "isMasked": True, "hint": "böbrek ve mesane doku zedelenmesi"}]}
        ]),
        make_chain("Kateterli Hastada Semptom Gelişimi", [
            "1. Mesanede Biyofilm: Bakteriyel çoğalma ve mukozal irritasyon.",
            "2. Pelvik Rahatsızlık: Mesane tabanında enflamasyon ve hematüri.",
            "3. Asendan Tırmanış: Üreterden böbreğe geçip KVAH ve yan ağrısı yapması.",
            "4. Sistemik Yayılım: Ateş, titreme ve akut mental durum değişikliği."
        ]),
        make_recall("Kateteri takılı olan bir hastada Kİ-ÜSE düşündüren temel klinik bulgular nelerdir?", "Yeni başlayan ateş, titreme, mental durum değişikliği, halsizlik/letarji, yan ağrısı, KVA hassasiyeti, akut hematüri ve pelvik rahatsızlıktır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kateterli Hasta Kliniği", [
            {"text": "Yeni başlayan ateş ve titreme Kİ-ÜSE düşündürür.", "isLie": False, "explanation": "Doğru. Sistemik enfeksiyon belirtisidir."},
            {"text": "Mental durum değişikliği ve letarji klinik bulgular arasındadır.", "isLie": False, "explanation": "Doğru. Özellikle yaşlıda sıktır."},
            {"text": "Kateterli hastada Kİ-ÜSE geliştiğinde hasta 100 metre yükseğe zıplayıp şarkı söylemeye başlar.", "isLie": True, "explanation": "Tuzak! Kİ-ÜSE halsizlik, letarji, ateş ve kostavertebral açı hassasiyeti yapar."},
            {"text": "Akut hematüri ve KVA hassasiyeti klinik bulgulara dahildir.", "isLie": False, "explanation": "Doğru. Ders notu listesidir."}
        ]),
        make_quiz("Üriner kateteri takılı olan bir hastada başka bir odak bulunmaksızın Kİ-ÜSE tablosunu düşündüren klinik bulgular arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Yeni başlayan ateş, titreme, mental durum değişikliği, halsizlik/letarji, yan ağrısı, KVA hassasiyeti, akut hematüri", "isCorrect": True, "explanation": "Ders notunda kateter takılı hastadaki Kİ-ÜSE semptomları olarak eksiksiz listelenmiştir."},
            {"key": "B", "text": "Yalnızca ayak parmaklarında kaşıntı", "isCorrect": False, "explanation": "Kİ-ÜSE bulgusu değildir."},
            {"key": "C", "text": "Göz bebeklerinde büyüme ve tat alma kaybı", "isCorrect": False, "explanation": "ÜSE ile ilgisiz nörolojik bulgulardır."},
            {"key": "D", "text": "Aşırı neşeli olma ve saç uzaması", "isCorrect": False, "explanation": "Hastalık belirtisi değildir."}
        ])
    ]
    slides.append(make_slide(55, "Kİ-ÜSE Kliniği: Kateter Takılı İken Bulgular", "Ateş, titreme, mental değişiklik, yan ağrısı, KVAH ve akut hematüri", "Kİ-ÜSE", s55_narrative, s55_bullets, s55_elements))

    # Slide 56: Kateter Çıkarılmış Hastada Klinik Bulgular
    s56_narrative = (
        "Kateteri son 48 saat içinde çekilmiş olan hastalar, kateterin oluşturduğu mekanik şant "
        "kalktığı için klasik alt üriner traktus irritasyon bulgularını doğrudan hissederler.\n\n"
        "- **Çekildikten Sonraki Semptomlar:** Kateter çıkarılmışsa **dizüri, sıkışma (urgency), "
        "sıklık (frequency) ve suprapubik ağrı** gibi tipik sistit yakınmaları belirginleşir.\n"
        "- **Mekanik İrritasyon:** Kateter balonunun mesane trigonunda yarattığı ödem ve bakteriyel "
        "enflamasyon, idrar yaparken yanma (dizüri) ve ani işeme hissini şiddetlendirir.\n"
        "- **Klinik Yaklaşım:** Kateter çekildikten sonra bu şikayetleri tarifleyen hastada Kİ-ÜSE "
        "akla gelmeli ve idrar kültürü ile doğrulanmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> Kateter çıkarılmış hastalarda Kİ-ÜSE kliniği: Dizüri, sıkışma, sıklık ve suprapubik ağrıdır."
    )
    s56_bullets = [
        "Kateter çıkarılmışsa: Dizüri, sıkışma (urgency), sıklık (frequency), suprapubik ağrı.",
        "Kateter drenajı sonlandığında lokal ürotelyal enflamasyon semptomları ön plana çıkar.",
        "Son 48 saat içinde kateter çekilme öyküsü bu semptomlarla birleştiğinde Kİ-ÜSE tanısını koydurur."
    ]
    s56_elements = [
        make_cloze("Kateter çıkarılmış olan hastalarda Kİ-ÜSE kliniğinde dizüri, sıkışma, sıklık ve suprapubik ağrı görülür.", "suprapubik ağrı", "Mesane izdüşümünde hissedilen lokal enflamatuar ağrı"),
        make_table("Kateter Çıkarıldıktan Sonraki Kİ-ÜSE Bulguları", ["Semptom", "Tıbbi Anlamı", "Patofizyolojik Köken"], [
            {"cells": [{"text": "Dizüri", "isMasked": False}, {"text": "İdrar yaparken yanma/ağrı", "isMasked": True, "hint": "işeme esnasında yanma"}, {"text": "Üretral mukozal enflamasyon"}]},
            {"cells": [{"text": "Sıkışma ve Sıklık", "isMasked": False}, {"text": "Ani acil işeme ve sık idrara çıkma", "isMasked": False}, {"text": "Detrüsor irritabilitesi", "isMasked": True, "hint": "mesane kasının uyarılması"}]},
            {"cells": [{"text": "Suprapubik Ağrı", "isMasked": False}, {"text": "Alt karında dolgunluk ve hassasiyet", "isMasked": True, "hint": "mesane üzeri ağrı"}, {"text": "Mesane duvar enflamasyonu"}]}
        ]),
        make_chain("Kateter Çekilme Sonrası Semptom Zinciri", [
            "1. Kateter Çekilmesi: Mekanik drenaj borusunun alınması.",
            "2. Doğal İdrar Teması: İdrarın enflame mesane ve üretradan geçişi.",
            "3. Reseptör Aktivasyonu: Yanma (dizüri) ve ani sıkışma hissi.",
            "4. Klinik Başvuru: Dizüri, sıklık ve suprapubik ağrıyla tanı konması."
        ]),
        make_recall("Kateteri çıkarılmış bir hastada Kİ-ÜSE düşündüren dört lokal semptom nedir?", "Dizüri, sıkışma (urgency), sıklık (frequency) ve suprapubik ağrıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kateter Çıkarılmış Hasta", [
            {"text": "Kateter çıkarılmışsa dizüri ve sıkışma Kİ-ÜSE belirtisidir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Sıklık ve suprapubik ağrı kateter çekildikten sonra görülebilir.", "isLie": False, "explanation": "Doğru. Tipik lokal bulgulardır."},
            {"text": "Kateter çıkarıldıktan sonra hastada dizüri olması imkansızdır, dizüri sadece kuşlarda olur.", "isLie": True, "explanation": "Tuzak! Kateter çıkarıldıktan sonra dizüri, sıkışma, sıklık ve suprapubik ağrı en tipik Kİ-ÜSE bulgularıdır."},
            {"text": "Kateter çekildikten sonraki ilk 48 saat Kİ-ÜSE kapsamındadır.", "isLie": False, "explanation": "Doğru. Zaman penceresidir."}
        ]),
        make_quiz("Son 48 saat içinde mesane kateteri çıkarılmış bir hastada Kİ-ÜSE'ye işaret eden lokal semptomlar aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Dizüri, sıkışma, sıklık ve suprapubik ağrı", "isCorrect": True, "explanation": "Ders notunda 'kateter çıkarılmışsa dizüri, sıkışma, sıklık, suprapubik ağrı' denmektedir."},
            {"key": "B", "text": "Göğüs ağrısı ve sol kolda uyuşma", "isCorrect": False, "explanation": "Miyokard enfarktüsü bulgusudur."},
            {"key": "C", "text": "Kulak çınlaması ve burun kanaması", "isCorrect": False, "explanation": "ÜSE ile ilgisizdir."},
            {"key": "D", "text": "Sadece ayak bileği burkulması", "isCorrect": False, "explanation": "Ortopedik bir durumdur."}
        ])
    ]
    slides.append(make_slide(56, "Kİ-ÜSE Kliniği: Kateter Çıkarılmış İken Bulgular", "Kateter çekildikten sonra dizüri, sıkışma, sıklık ve suprapubik ağrı", "Kİ-ÜSE", s56_narrative, s56_bullets, s56_elements))

    # Slide 57: Kİ-ÜSE Mikrobiyolojik Tanım Eşiği (≥10³ KOB/mL)
    s57_narrative = (
        "Kateterize hastalarda mikrobiyolojik kültürün değerlendirilmesi, toplum kökenli klasik "
        "eşik değerlerden (10⁵ CFU/mL) belirgin biçimde farklıdır.\n\n"
        "- **Mikrobiyolojik Eşik:** Kİ-ÜSE mikrobiyolojik tanısı için **≥10³ KOB/mL (1000 koloni) "
        "üreme** eşik değer olarak kabul edilir.\n"
        "- **Örnekleme Koşulları:** Bu eşik; **tek kateter idrar örneğinde** veya son 48 saatte "
        "kateteri çıkarılmış hastanın **orta akım örneğinde** bir veya daha fazla türde aranır.\n"
        "- **Düşük Eşik Nedeni:** Kateter takılıyken mesane idrarı sürekli drene olduğundan bakteriler "
        "mesanede uzun süre kalamaz; bu nedenle 10³ KOB/mL gibi daha düşük sayılar dahi enfeksiyon için tanısal kabul edilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kİ-ÜSE mikrobiyolojik tanı eşiği: Kateter idrarında veya kateteri çıkarılmış hastanın orta akımında ≥10³ KOB/mL üremedir."
    )
    s57_bullets = [
        "Kİ-ÜSE mikrobiyolojik eşiği: ≥10³ KOB/mL üreme (bir veya daha fazla türde).",
        "Örnek türü: Tek kateter idrarı veya son 48 saatte çekilmiş hastanın orta akım idrarı.",
        "Sürekli drenaj nedeniyle klasik 10⁵ eşiği yerine 10³ KOB/mL tanısal kabul edilir."
    ]
    s57_elements = [
        make_cloze("Kİ-ÜSE mikrobiyolojik tanısı için kateter idrarında veya son 48 saatte çekilen hastanın orta akım idrarında ≥10³ KOB/mL üreme gerekir.", "≥10³ KOB/mL", "Kİ-ÜSE'deki mikrobiyolojik koloni eşik değeri"),
        make_table("Kİ-ÜSE Mikrobiyolojik Kriterleri", ["Örnek Alma Şekli", "Patojen Türü", "Tanısal Koloni Sayısı"], [
            {"cells": [{"text": "Tek Kateter İdrarı", "isMasked": False}, {"text": "Bir veya daha fazla tür", "isMasked": True, "hint": "polimikrobiyal olabilir"}, {"text": "≥10³ KOB/mL"}]},
            {"cells": [{"text": "Son 48 Saatte Çıkarılanın Orta Akımı", "isMasked": False}, {"text": "Bir veya daha fazla tür", "isMasked": False}, {"text": "≥10³ KOB/mL", "isMasked": True, "hint": "bin koloni ve üzeri"}]}
        ]),
        make_chain("Kİ-ÜSE Mikrobiyolojik Tanı Akışı", [
            "1. İdrar Alma: Kateter portundan aseptik teknikle idrar çekilmesi.",
            "2. Kültür Ekimi: Kantitatif besiyerine standart inokülasyon.",
            "3. Koloni Sayımı: İnkübasyon sonrası koloni tespiti.",
            "4. Eşik Doğrulaması: ≥10³ KOB/mL üreme ile Kİ-ÜSE mikrobiyolojisinin kanıtlanması."
        ]),
        make_recall("Kİ-ÜSE'nin mikrobiyolojik tanımı için gereken koloni sayısı eşik değeri nedir?", "Bir veya daha fazla türde ≥10³ KOB/mL (1000 koloni) üremedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kİ-ÜSE Mikrobiyolojik Eşik", [
            {"text": "Kİ-ÜSE için mikrobiyolojik eşik ≥10³ KOB/mL üremedir.", "isLie": False, "explanation": "Doğru. Ders notu kesin kriteridir."},
            {"text": "Bu eşik bir veya daha fazla türde geçerlidir.", "isLie": False, "explanation": "Doğru. Polimikrobiyal olabilir."},
            {"text": "Kİ-ÜSE tanısı koyabilmek için idrarda en az 100 milyar koloni üremesi şarttır, 10³ asla kabul edilmez.", "isLie": True, "explanation": "Tuzak! Kİ-ÜSE tanı eşiği tam olarak ≥10³ KOB/mL'dir."},
            {"text": "Son 48 saatte kateteri çıkarılmış hastanın orta akım idrarında da bu eşik kullanılır.", "isLie": False, "explanation": "Doğru. Tanım kapsamındadır."}
        ]),
        make_quiz("Kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) mikrobiyolojik tanı için kabul edilen koloni eşik değeri aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "≥10³ KOB/mL", "isCorrect": True, "explanation": "Ders notunda 'tek kateter idrar örneğinde veya son 48 saatte kateteri çıkarılmış hastanın orta akım örneğinde bir veya daha fazla türde ≥10³ KOB/mL üreme' denmektedir."},
            {"key": "B", "text": "≥10⁸ KOB/mL", "isCorrect": False, "explanation": "Çok yüksek bir eşiktir."},
            {"key": "C", "text": "≥10⁵ CFU/mL tek tür şartı", "isCorrect": False, "explanation": "Bu klasik asemptomatik bakteriüri kriteridir, Kİ-ÜSE'de eşik 10³'tür."},
            {"key": "D", "text": "Sıfır üreme", "isCorrect": False, "explanation": "Üreme olması şarttır."}
        ])
    ]
    slides.append(make_slide(57, "Kİ-ÜSE Mikrobiyolojik Eşiği: ≥10³ KOB/mL", "Kateter idrarında veya çekildikten sonra orta akımda ≥10³ KOB/mL tanı kriteri", "Kİ-ÜSE", s57_narrative, s57_bullets, s57_elements))

    # Slide 58: Kokulu ve Bulanık İdrar Tuzağı: Kİ-ABU vs Kİ-ÜSE Ayırımı
    s58_narrative = (
        "Kateter takılı hastalarda idrar torbasında görülen bulanıklık ve duyulan ağır koku, klinik "
        "pratikte en sık gereksiz antibiyotik başlanmasına yol açan tuzak bulgulardır.\n\n"
        "- **Kritik Kural:** **Kokulu veya bulanık idrar tek başına kateterle ilişkili asemptomatik "
        "bakteriüri (Kİ-ABU) ile Kİ-ÜSE'yi ayırt etmez**.\n"
        "- **Biyofilm Ürünleri:** Kateter yüzeyindeki bakterilerin üreaz aktivitesi ve metabolitleri "
        "idrarda koku ve tortu yapsa da, hastada klinik semptom yoksa bu tablo yalnızca kolonizasyondur (Kİ-ABU).\n"
        "- **Klinik Yaklaşım:** Sadece idrar kokuyor veya bulanık diye antibiyotik başlanmamalıdır; "
        "ateş, KVAH veya letarji gibi gerçek klinik enfeksiyon bulguları aranmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [KRİTİK UYARI] Kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez; tedavi kararı için semptomların varlığı şarttır."
    )
    s58_bullets = [
        "Kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez.",
        "Kateterli hastada sadece koku/bulanıklık nedeniyle antibiyotik başlanmamalıdır.",
        "Kİ-ABU tedavi edilmez; Kİ-ÜSE tanısı için klinik semptomların eşlik etmesi zorunludur."
    ]
    s58_elements = [
        make_cloze("Kateterli hastalarda kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez.", "ayırt etmez", "Koku ve bulanıklığın tanısal ayırım gücünün olmadığını belirten kural"),
        make_table("Kİ-ABU ve Kİ-ÜSE Ayırıcı Tanı Kriterleri", ["Klinik Parametre", "Kİ-ABU", "Kİ-ÜSE"], [
            {"cells": [{"text": "Bulanık / Kokulu İdrar", "isMasked": False}, {"text": "Sıklıkla bulunabilir", "isMasked": False}, {"text": "Sıklıkla bulunabilir (ayırıcı değildir)", "isMasked": True, "hint": "iki grupta da görülebilen bulgu"}]},
            {"cells": [{"text": "Klinik Semptomlar", "isMasked": False}, {"text": "Semptom yoktur", "isMasked": True, "hint": "şikayetsiz tablo"}, {"text": "Ateş, KVAH, letarji veya dizüri vardır"}]},
            {"cells": [{"text": "Antibiyotik Tedavisi", "isMasked": False}, {"text": "Tedavi ÖNERİLMEZ", "isMasked": True, "hint": "ilaç verilmemesi kuralı"}, {"text": "Tedavi EDİLMELİDİR"}]}
        ]),
        make_chain("Koku ve Bulanıklık Karar Akışı", [
            "1. İdrar Torbası Muayenesi: İdrarın bulanık ve kokulu olduğunun görülmesi.",
            "2. Tuzaktan Kaçınma: Koku/bulanıklığın tek başına ayırıcı olmadığını hatırlama.",
            "3. Semptom Sorgusu: Ateş, letarji, yan ağrısı veya pelvik rahatsızlık arama.",
            "4. Karar: Semptom yoksa Kİ-ABU kabul edip antibiyotik vermeme."
        ]),
        make_recall("Kateterli hastada idrarın kokulu veya bulanık olması tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt eder mi?", "Hayır, tek başına ayırt etmez; klinik semptomların varlığı aranmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Koku ve Bulanıklık", [
            {"text": "Kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez.", "isLie": False, "explanation": "Doğru. Ders notundaki kesin uyarıdır."},
            {"text": "Kateterli hastada semptom yoksa sadece koku için antibiyotik verilmemelidir.", "isLie": False, "explanation": "Doğru. Gereksiz antibiyotikten kaçınılmalıdır."},
            {"text": "İdrarda en ufak koku duyulduğu an hasta derhal ameliyata alınıp tüm mesanesi çıkarılmalıdır.", "isLie": True, "explanation": "Tuzak! Koku kateter biyofilminde çok sık görülür ve tek başına tedavi endikasyonu bile değildir."},
            {"text": "Kİ-ÜSE tanısı koymak için klinik enfeksiyon semptomları aranmalıdır.", "isLie": False, "explanation": "Doğru. Semptom şarttır."}
        ]),
        make_quiz("Kateter takılı bir hastada idrarın bulanık ve kokulu olması ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Kokulu veya bulanık idrar tek başına kateterle ilişkili asemptomatik bakteriüri (Kİ-ABU) ile Kİ-ÜSE'yi ayırt etmez' denmektedir."},
            {"key": "B", "text": "Kesinlikle septik şok başladığını gösterir", "isCorrect": False, "explanation": "Septik şok kanıtı değildir."},
            {"key": "C", "text": "Hastada kesin piyelonefrit olduğunu kanıtlar", "isCorrect": False, "explanation": "Ayırt edici değildir."},
            {"key": "D", "text": "Derhal 4'lü antibiyotik başlanmasını gerektirir", "isCorrect": False, "explanation": "Semptomsuz ise tedavi önerilmez."}
        ])
    ]
    slides.append(make_slide(58, "Kokulu ve Bulanık İdrar: Kİ-ABU vs Kİ-ÜSE", "Bulanık ve kokulu idrarın tanısal tuzakları ve semptom arama gereksinimi", "Kİ-ÜSE", s58_narrative, s58_bullets, s58_elements))

    # Slide 59: Piyürinin Kİ-ÜSE'deki Rolü: Tanısal Olmama ve Yokluğunun Anlamı
    s59_narrative = (
        "Kateterli hastalarda lökosit varlığı (piyüri), kateterin mesane mukozasına yaptığı "
        "doğal mekanik irritasyon nedeniyle son derece yanıltıcı olabilir.\n\n"
        "- **Tanısal Değildir:** Kİ-ÜSE değerlendirmesinde **piyüri tanısal değildir**; çünkü kateteri "
        "olan neredeyse her hastada mekanik sürtünmeye bağlı lökosit idrara dökülür.\n"
        "- **Yokluğunun Değeri:** Ancak **semptomlu hastada piyüri yokluğu başka tanıyı düşündürür**.\n"
        "- **Negatif Prediktif Güç:** Ateşi ve titremesi olan kateterli bir hastanın idrarında hiç "
        "lökosit saptanmaması (piyüri olmaması), ateşin üriner sistemden değil pnömoni veya kateter bakteriyemisi gibi başka bir odaktan kaynaklandığını gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kİ-ÜSE'de piyüri tanısal değildir; ancak semptomlu hastada piyüri yokluğu başka tanıyı düşündürür."
    )
    s59_bullets = [
        "Piyüri tanısal değildir (kateter irritasyonuna bağlı olarak neredeyse her hastada görülür).",
        "Semptomlu hastada piyüri yokluğu başka tanıyı düşündürür.",
        "Piyürinin varlığı değil, yokluğu negatif prediktif olarak değerlidir."
    ]
    s59_elements = [
        make_cloze("Kİ-ÜSE'de piyüri tanısal değildir; ancak semptomlu hastada piyüri yokluğu başka tanıyı düşündürür.", "başka tanıyı düşündürür", "Ateşli hastada idrarda lökosit yokluğunun gösterdiği klinik yönelim"),
        make_table("Piyürinin Kİ-ÜSE'deki İki Yönlü Anlamı", ["Piyüri Durumu", "Tanısal Değeri", "Klinik Yorum"], [
            {"cells": [{"text": "Piyüri VAR (+)", "isMasked": False}, {"text": "Tanısal DEĞİLDİR", "isMasked": True, "hint": "tanı koydurmayan durum"}, {"text": "Kateterin mekanik irritasyonu ile de oluşur"}]},
            {"cells": [{"text": "Piyüri YOK (-)", "isMasked": False}, {"text": "Dışlayıcı / Yol gösterici", "isMasked": False}, {"text": "Semptomlu hastada başka tanı düşünülür", "isMasked": True, "hint": "üriner dışı odak arayışı"}]}
        ]),
        make_chain("Piyüri Değerlendirme Algoritması", [
            "1. Semptomlu Kateterli Hasta: Ateş ve titreme ile başvuru.",
            "2. İdrar Mikroskopisi: Piyüri (lökosit) araştırılması.",
            "3. Piyüri Yokluğu Saptanması: İdrarda lökosit görülmemesi.",
            "4. Tanı Değişimi: Odağın üriner sistem dışı aranması (pnömoni vb.)."
        ]),
        make_recall("Kİ-ÜSE'de piyürinin tanısal değeri nedir ve semptomlu hastada piyüri yokluğu neyi düşündürür?", "Piyüri tanısal değildir; ancak semptomlu hastada piyüri yokluğu başka tanıyı düşündürür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Piyürinin Rolü", [
            {"text": "Kİ-ÜSE'de piyüri tanısal değildir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Semptomlu hastada piyüri yokluğu başka tanıyı düşündürür.", "isLie": False, "explanation": "Doğru. Dışlayıcı değere sahiptir."},
            {"text": "Kateterli hastada piyüri görülmesi o hastanın anında ameliyat edilmesini gerektiren kesin kanser kanıtıdır.", "isLie": True, "explanation": "Tuzak! Piyüri kateterli hastada çok yaygındır ve tanısal bile değildir."},
            {"text": "Kateterin kendisi üroepitele mekanik sürtünmeyle lökosit döktürebilir.", "isLie": False, "explanation": "Doğru. İrritasyon yapar."}
        ]),
        make_quiz("Kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) piyürinin (idrarda lökosit) tanısal değeri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Piyüri tanısal değildir; semptomlu hastada piyüri yokluğu başka tanıyı düşündürür", "isCorrect": True, "explanation": "Ders notunda aynen 'Piyüri tanısal değildir; semptomlu hastada piyüri yokluğu başka tanıyı düşündürür' denmektedir."},
            {"key": "B", "text": "Piyüri Kİ-ÜSE için %100 özgül tek altın standart tanı kriteridir", "isCorrect": False, "explanation": "Piyüri tanısal değildir."},
            {"key": "C", "text": "Piyüri sadece genç kızlarda görülür, kateterli erkekte asla görülmez", "isCorrect": False, "explanation": "Her iki cinste de görülür."},
            {"key": "D", "text": "Semptomlu hastada piyüri olmaması Kİ-ÜSE tanısını kesinleştirir", "isCorrect": False, "explanation": "Piyüri yokluğu başka tanıyı düşündürür."}
        ])
    ]
    slides.append(make_slide(59, "Kİ-ÜSE'de Piyürinin Değeri ve Yokluğunun Anlamı", "Piyürinin tanısal olmaması ve semptomlu hastada yokluğunun ayırıcı değeri", "Kİ-ÜSE", s59_narrative, s59_bullets, s59_elements))

    # Slide 60: [TEKRAR SAYFASI - CHECKPOINT 6] Kateterle İlişkili ÜSE (Kİ-ÜSE)
    s60_narrative = (
        "Bu tekrar sayfasında 6. Bölümde işlenen Kİ-ÜSE tanımını, en önemli risk faktörünü, mikrobiyolojik "
        "kriterlerini ve tanısal tuzakları pekiştiriyoruz.\n\n"
        "- **Tanım ve Risk:** Kateteri olan veya **son 48 saat içinde** kateter öyküsü olan kişide gelişir; "
        "**kateter süresi en önemli risk faktörüdür**.\n"
        "- **Mikrobiyoloji:** Sıklıkla polimikrobiyaldir; etkenler E. coli, Providencia, Proteus, Morganella, "
        "Pseudomonas, Acinetobacter, MRSA ve enterokoklardır; tanı eşiği **≥10³ KOB/mL**dir.\n"
        "- **Klinik Tuzaklar:** Kokulu/bulanık idrar tek başına **Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez**; "
        "**piyüri tanısal değildir**, ancak semptomlu hastada piyüri yokluğu başka tanıyı düşündürür.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 6] Kİ-ÜSE'de en önemli risk kateter süresidir; eşik ≥10³ KOB/mL ve polimikrobiyaldir; koku/bulanıklık ayırt etmez, piyüri tanısal değildir ama yokluğu başka tanı düşündürür."
    )
    s60_bullets = [
        "Kateteri olan veya son 48 saatte çekilen hastada gelişir; en önemli risk kateter süresidir.",
        "Mikrobiyoloji: Sıklıkla polimikrobiyal, ÇİD etkenler, eşik ≥10³ KOB/mL.",
        "Koku/bulanıklık tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez.",
        "Piyüri tanısal değildir; semptomlu hastada piyüri yokluğu başka tanıyı düşündürür."
    ]
    s60_elements = [
        make_cloze("Kİ-ÜSE gelişiminde en önemli risk faktörü kateter süresi olup mikrobiyolojik tanı eşiği ≥10³ KOB/mL üremedir.", "kateter süresi", "Kİ-ÜSE'deki en kritik risk faktörü"),
        make_table("6. Bölüm Büyük Tekrar Tablosu", ["Kavram / Parametre", "Kriter / Değer", "Klinik Anlamı"], [
            {"cells": [{"text": "En Önemli Risk Faktörü", "isMasked": False}, {"text": "Kateter süresi", "isMasked": True, "hint": "kateterin kaldığı gün sayısı"}, {"text": "Gereksiz kateterin çekilmesi esastır"}]},
            {"cells": [{"text": "Mikrobiyolojik Eşik", "isMasked": False}, {"text": "≥10³ KOB/mL", "isMasked": False}, {"text": "Bir veya daha fazla türde üreme", "isMasked": True, "hint": "polimikrobiyal tanı eşiği"}]},
            {"cells": [{"text": "Koku ve Bulanıklık", "isMasked": False}, {"text": "Tek başına ayırt etmez", "isMasked": True, "hint": "ayırıcı tanı gücü yok"}, {"text": "Semptom olmadan tedavi verilmez"}]},
            {"cells": [{"text": "Piyürinin Rolü", "isMasked": False}, {"text": "Tanısal değildir (yokluğu değerlidir)", "isMasked": False}, {"text": "Yoksa başka odak araştırılır", "isMasked": True, "hint": "farklı enfeksiyon odağı"}]}
        ]),
        make_chain("6. Bölüm Konsolidasyon Zinciri", [
            "1. Kateterizasyon: Kateter süresinin en önemli risk faktörü olması.",
            "2. Mikrobiyoloji: ≥10³ KOB/mL polimikrobiyal üreme tespiti.",
            "3. Tuzakların Ayıklanması: Koku/bulanıklık ve piyürinin tek başına yetersizliği.",
            "4. Doğru Tanı: Semptomların varlığıyla Kİ-ÜSE tanısının doğrulanması."
        ]),
        make_recall("Checkpoint 6: Kİ-ÜSE'de en önemli risk faktörü, mikrobiyolojik eşik değeri ve koku/bulanıklık kuralı nedir?", "En önemli risk faktörü kateter süresidir; mikrobiyolojik eşik ≥10³ KOB/mL'dir; kokulu/bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 6 Konsolidasyonu", [
            {"text": "Kateter süresi Kİ-ÜSE'de en önemli risk faktörüdür.", "isLie": False, "explanation": "Doğru. 6. bölümün ana kuralıdır."},
            {"text": "Kİ-ÜSE mikrobiyolojik eşiği bir veya daha fazla türde ≥10³ KOB/mL üremedir.", "isLie": False, "explanation": "Doğru. Kesin tanısal eşiktir."},
            {"text": "Kokulu veya bulanık idrar Kİ-ÜSE'nin %100 kesin kanıtıdır ve başka hiçbir şeye bakılmadan derhal ameliyat gerektirir.", "isLie": True, "explanation": "Tuzak! Kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez."},
            {"text": "Piyüri tanısal değildir; ancak semptomlu hastada piyüri yokluğu başka tanıyı düşündürür.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("6. Bölümün tamamı (Kateterle İlişkili ÜSE) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Kİ-ÜSE'de mikrobiyolojik tanı için en az 10⁵ CFU/mL tek tür bakteri şarttır, 10³ üreme tanı koydurmaz", "isCorrect": True, "explanation": "Yanlış! Kİ-ÜSE mikrobiyolojik tanımı için ≥10³ KOB/mL (bir veya daha fazla türde) üreme yeterlidir."},
            {"key": "B", "text": "Kateter süresi Kİ-ÜSE'de en önemli risk faktörüdür", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Kokulu veya bulanık idrar tek başına Kİ-ABU ile Kİ-ÜSE'yi ayırt etmez", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Piyüri tanısal değildir; semptomlu hastada piyüri yokluğu başka tanıyı düşündürür", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(60, "[TEKRAR SAYFASI - CHECKPOINT 6] Kateterle İlişkili ÜSE (Kİ-ÜSE)", "6. Bölümün kapsamlı pekiştirmesi: Kİ-ÜSE tanımı, kateter süresi, ≥10³ eşiği ve tanısal tuzaklar", "Bölüm Tekrarı", s60_narrative, s60_bullets, s60_elements))

    return slides
