# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec2():
    slides = []

    # Slide 11: Üriner Sisteme Bulaş Yollarına Genel Bakış
    s11_narrative = (
        "Mikroorganizmaların üriner traktusa ulaşması ve enfeksiyon tablosu oluşturması "
        "farklı anatomik yollar aracılığıyla gerçekleşmektedir.\n\n"
        "- **Bulaş Yolları:** Mikroorganizmalar üriner sisteme dört ana yolla ulaşır: asendan yol, "
        "hematojen yol, lenfatik yol ve komşuluk yolu.\n"
        "- **Klinik Önem:** Bu yollar arasında sıklık ve klinik ağırlık açısından muazzam bir "
        "farklılık bulunmaktadır.\n"
        "- **Baskın Mekanizma:** Enfeksiyonların ezici çoğunluğu anatomik boşluk boyunca yukarı "
        "tırmanma şeklinde seyrederken, diğer yollar özel klinik durumlarda devreye girer.\n\n"
        "> [!NOTE]\n"
        "> Mikroorganizmaların üriner sisteme ulaşma yolları asendan, hematojen, lenfatik ve komşuluk yolu olmak üzere dört ana başlıkta incelenir."
    )
    s11_bullets = [
        "Mikroorganizmalar üriner sisteme dört temel yolla ulaşır.",
        "Asendan yol, hematojen yol, lenfatik yol ve komşuluk yolu.",
        "Bu yollar arasında asendan yol klinik pratikte ezici üstünlüğe sahiptir."
    ]
    s11_elements = [
        make_cloze("Mikroorganizmaların üriner sisteme ulaşmasında en önemli yol asendan yoldur.", "asendan yoldur", "Aşağıdan yukarıya tırmanarak ilerleyen temel bulaş yolu"),
        make_table("Üriner Sisteme Bulaş Yolları Sınıflaması", ["Bulaş Yolu", "Görülme Oranı / Önem", "Temel Özellik"], [
            {"cells": [{"text": "Asendan Yol", "isMasked": False}, {"text": "En önemli yol (%98'den fazla)", "isMasked": True, "hint": "ezici çoğunluğu oluşturan yol"}, {"text": "Üretradan böbreğe retrograd ilerleyiş"}]},
            {"cells": [{"text": "Hematojen Yol", "isMasked": False}, {"text": "Tüm ÜSE'lerin %2'den azı", "isMasked": False}, {"text": "Bakteriyemi sonrası renal parankim tutulumu", "isMasked": True, "hint": "kan yoluyla böbreğe yayılım"}]}
        ]),
        make_chain("Bulaş Yollarının Klinik Sıklık Dağılımı", [
            "1. Asendan Yol: Enfeksiyonların açık ara en sık görülen ana rotasıdır.",
            "2. Hematojen Yol: Bakteriyemi sonucu gelişen ve %2'den az görülen rota.",
            "3. Komşuluk Yolu: Fistül oluşumu ile doğrudan geçiş rotası.",
            "4. Lenfatik Yol: Önemi literatürde ve klinikte belirsiz olan rota."
        ]),
        make_recall("Mikroorganizmaların üriner sisteme ulaşmasında rol oynayan dört temel yol nedir?", "1) Asendan yol, 2) Hematojen yol, 3) Lenfatik yol, 4) Komşuluk yolu (fistül)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bulaş Yollarına Genel Bakış", [
            {"text": "Mikroorganizmalar üriner sisteme asendan, hematojen, lenfatik ve komşuluk yollarıyla ulaşabilir.", "isLie": False, "explanation": "Doğru. Dört temel bulaş yoludur."},
            {"text": "Asendan yol üriner sistem enfeksiyonlarında açık ara en önemli yoldur.", "isLie": False, "explanation": "Doğru. Ezici çoğunluk bu yolla gelişir."},
            {"text": "ÜSE vakalarının %99'u doğrudan solunum havasından böbreklere solunan bakterilerle başlar.", "isLie": True, "explanation": "Tuzak! Üriner sistem aeroben havayla enfekte olmaz; asendan yol temel rotadır."},
            {"text": "Hematojen yol tüm ÜSE'lerin %2'sinden azını oluşturur.", "isLie": False, "explanation": "Doğru. Küçük bir orandır."}
        ]),
        make_quiz("Mikroorganizmaların üriner sisteme ulaşma yolları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Asendan yol en önemli yoldur; hematojen yol ise tüm ÜSE'lerin %2'den azını oluşturur", "isCorrect": True, "explanation": "Ders notundaki kesin hiyerarşik bilgidir."},
            {"key": "B", "text": "Lenfatik yol tüm ÜSE'lerin %95'inden sorumlu ana yoldur", "isCorrect": False, "explanation": "Lenfatik yolun önemi belirsizdir."},
            {"key": "C", "text": "Komşuluk yolu en sık izlenen yayılım şeklidir", "isCorrect": False, "explanation": "Komşuluk fistülle ilişkilidir ve nadirdir."},
            {"key": "D", "text": "Asendan yol insanlarda hiçbir zaman enfeksiyon yapmaz", "isCorrect": False, "explanation": "Asendan yol en önemli ve en sık yoldur."}
        ])
    ]
    slides.append(make_slide(11, "Üriner Sisteme Bulaş Yolları: Genel Bakış", "Asendan, hematojen, lenfatik ve komşuluk yollarının sınıflaması", "Bulaş Yolları", s11_narrative, s11_bullets, s11_elements))

    # Slide 12: Asendan Yolun Önemi ve Mekanizması
    s12_narrative = (
        "Üriner sistem enfeksiyonlarının patogenezinde asendan yol açık ara en kritik ve "
        "en yaygın mekanizmayı temsil eder.\n\n"
        "- **En Önemli Yol:** Asendan yol ÜSE gelişiminde **en önemli yoldur** ve klinik vakaların "
        "neredeyse tamamından sorumludur.\n"
        "- **Tırmanma Prensibi:** Gastrointestinal sistem florasından kaynaklanan fekal bakteriler "
        "önce perine ve üretra çevresini kolonize eder.\n"
        "- **Lümen İçi Göç:** Bakteriler üretral meatusu aşarak lümen içine girer ve idrar akımının "
        "tersi yönünde anatomik olarak yukarıya doğru tırmanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Üriner sistem enfeksiyonlarında mikroorganizmaların sisteme ulaşmasında en önemli yol asendan yoldur."
    )
    s12_bullets = [
        "Asendan yol, mikroorganizmaların üriner sisteme ulaşmasında en önemli yoldur.",
        "Fekal flora kökenli bakterilerin perineal kolonizasyonu ile başlar.",
        "İdrar akımının tersine lümenden yukarı tırmanma prensibine dayanır."
    ]
    s12_elements = [
        make_cloze("Üriner sistem enfeksiyonlarında mikroorganizmaların sisteme ulaşmasında en önemli yol asendan yoldur.", "asendan yoldur", "Üretradan başlayıp yukarı tırmanan ana patogenetik yol"),
        make_table("Asendan Yolun Temel Dinamikleri", ["Basamak", "Anatomik Konum", "Fizyopatolojik Süreç"], [
            {"cells": [{"text": "Floradan Çıkış", "isMasked": False}, {"text": "Perine ve periüretral alan", "isMasked": True, "hint": "üretra çevresi bölge"}, {"text": "Fekal üropatojen kolonizasyonu"}]},
            {"cells": [{"text": "Lümene Giriş", "isMasked": False}, {"text": "Eksternal üretral meatus", "isMasked": False}, {"text": "Retrograd intraluminal tırmanış", "isMasked": True, "hint": "ters yönde ilerleme"}]}
        ]),
        make_chain("Asendan Yayılımın Başlangıç Adımları", [
            "1. Kolonizasyon: Perineal florada enterik üropatojen çoğalması.",
            "2. Meatus İstilası: Eksternal üretral ağza bakteriyel giriş.",
            "3. İntraüretral Göç: Kısa kadın veya erkek üretrasında ilerleme.",
            "4. Mesane İntrakaviter Tutulumu: Asendan yolla mesaneye ulaşım."
        ]),
        make_recall("Üriner sistem enfeksiyonlarında en önemli bulaş yolu hangisidir?", "Asendan yoldur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Asendan Yol", [
            {"text": "Asendan yol üriner sistem enfeksiyonlarında en önemli yoldur.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Asendan yolda bakteriler anatomik kanallar boyunca yukarı doğru ilerler.", "isLie": False, "explanation": "Doğru. Retrograd bir tırmanıştır."},
            {"text": "Asendan yol tıp tarihinde sadece bir kez tanımlanmış ve günümüzde terk edilmiş bir kavramdır.", "isLie": True, "explanation": "Tuzak! Asendan yol günümüzde de ÜSE vakalarının %98'den fazlasından sorumlu temel yoldur."},
            {"text": "Perineal floradaki bakterilerin üretraya geçişi asendan yolun başlangıcıdır.", "isLie": False, "explanation": "Doğru. Kolonizasyon başlangıç basamağıdır."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarında mikroorganizmaların sisteme ulaşmasında EN ÖNEMLİ yol aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Asendan yol", "isCorrect": True, "explanation": "Ders notunda net olarak 'Asendan yol: en önemli yoldur' ifadesi yer almaktadır."},
            {"key": "B", "text": "Hematojen yol", "isCorrect": False, "explanation": "Hematojen yol %2'den azını oluşturur."},
            {"key": "C", "text": "Lenfatik yol", "isCorrect": False, "explanation": "Lenfatik yolun önemi belirsizdir."},
            {"key": "D", "text": "Komşuluk yolu (fistül)", "isCorrect": False, "explanation": "Komşuluk yolu nadir ve istisnai bir yoldur."}
        ])
    ]
    slides.append(make_slide(12, "En Önemli Bulaş Yolu: Asendan Yayılım", "Asendan yolun tanımı, patogenetik üstünlüğü ve lümen içi ilerleme mekanizması", "Bulaş Yolları", s12_narrative, s12_bullets, s12_elements))

    # Slide 13: Asendan Yolun Anatomik İlerleme Sırası
    s13_narrative = (
        "Asendan yol boyunca mikroorganizmaların üriner traktus içerisindeki ilerleyişi belirli bir "
        "anatomik hiyerarşi ve sıra takip eder.\n\n"
        "- **Tam Anatomik Sıra:** Asendan yol **üretra → mesane → üreter → böbrek** şeklinde ilerler.\n"
        "- **Alt Traktus Basamağı:** Enfeksiyon distal üretradan başlayarak mesaneye ulaşır ve burada "
        "çoğalarak lokal sistit tablosunu meydana getirir.\n"
        "- **Üst Traktusa Tırmanış:** Mesanedeki bakteriler vezikoüreteral bileşkeyi aşarak üretere ve "
        "sonrasında böbrek toplayıcı sistemine (pelvis renalis ve parankim) tırmanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Asendan yolun anatomik ilerleyiş sırası: üretra → mesane → üreter → böbrek şeklindedir."
    )
    s13_bullets = [
        "Asendan yolun ilerleme sırası: üretra → mesane → üreter → böbrek.",
        "Alt üriner traktustan üst üriner traktusa doğru kesintisiz anatomik yayılım.",
        "Vezikoüreteral bileşkenin aşılması böbrek parankim tutulumuna zemin hazırlar."
    ]
    s13_elements = [
        make_cloze("Asendan yolun anatomik ilerleme sırası üretra → mesane → üreter → böbrek şeklinde ilerler.", "üretra → mesane → üreter → böbrek", "Distalden proksimale tam anatomik ilerleme dizilimi"),
        make_table("Asendan Yolun Anatomik Basamakları", ["Sıra", "Organ Segmenti", "Klinik Yansıması"], [
            {"cells": [{"text": "1. ve 2. Adım", "isMasked": False}, {"text": "Üretra → Mesane", "isMasked": True, "hint": "alt üriner sistem organları"}, {"text": "Üretrit ve akut sistit tablosu"}]},
            {"cells": [{"text": "3. ve 4. Adım", "isMasked": False}, {"text": "Üreter → Böbrek", "isMasked": False}, {"text": "Üreterit ve akut piyelonefrit", "isMasked": True, "hint": "üst sistem parankimal tablosu"}]}
        ]),
        make_chain("Asendan Yolun Birebir İlerleme Zinciri", [
            "1. Üretra: Giriş kapısı ve distal intraluminal geçiş.",
            "2. Mesane: Bakteriyel çoğalma ve ürotelyal enflamasyon.",
            "3. Üreter: Üreteral peristaltizme karşı yukarı tırmanış.",
            "4. Böbrek: Pelvis renalis ve renal parankim invazyonu."
        ]),
        make_recall("Asendan yolun ders notunda belirtilen tam anatomik ilerleme sırası nasıldır?", "üretra → mesane → üreter → böbrek şeklinde ilerler."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İlerleme Sırası", [
            {"text": "Asendan yol üretra → mesane → üreter → böbrek şeklinde ilerler.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Mesane aşamasında enfeksiyon lokal sistit semptomları verebilir.", "isLie": False, "explanation": "Doğru. Alt sistem tutulumudur."},
            {"text": "Asendan yol böbrekten başlar ve aşağıya üretraya doğru akar.", "isLie": True, "explanation": "Tuzak! Asendan yol 'aşağıdan yukarı tırmanan' yoldur; üretra → mesane → üreter → böbrek sırasıyla gider."},
            {"text": "Üreterden yukarı tırmanış böbrek parankiminin tutulmasına yol açar.", "isLie": False, "explanation": "Doğru. Piyelonefrit bu yolla gelişir."}
        ]),
        make_quiz("Asendan yolla gelişen üriner sistem enfeksiyonunda mikroorganizmaların anatomik ilerleme sırası aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "üretra → mesane → üreter → böbrek", "isCorrect": True, "explanation": "Ders notundaki kesin ve sıralı anatomik akıştır."},
            {"key": "B", "text": "böbrek → üreter → mesane → üretra", "isCorrect": False, "explanation": "Bu desendan akıştır, asendan değil."},
            {"key": "C", "text": "mesane → böbrek → üretra → üreter", "isCorrect": False, "explanation": "Anatomik sıra bozuktur."},
            {"key": "D", "text": "üreter → üretra → böbrek → mesane", "isCorrect": False, "explanation": "Anatomik sıralama yanlıştır."}
        ])
    ]
    slides.append(make_slide(13, "Asendan Yayılımın Anatomik İlerleme Sırası", "Üretra, mesane, üreter ve böbrek hiyerarşisi ile yukarı tırmanış", "Bulaş Yolları", s13_narrative, s13_bullets, s13_elements))

    # Slide 14: Hematojen Yol ve Görülme Sıklığı (<%2)
    s14_narrative = (
        "Üriner sisteme kan dolaşımı yoluyla mikroorganizma ulaşması, asendan yolla kıyaslandığında "
        "oldukça nadir görülen bir durumdur.\n\n"
        "- **Görülme Oranı:** Hematojen yol, tüm üriner sistem enfeksiyonlarının **%2'den azını** "
        "(<%2) oluşturmaktadır.\n"
        "- **Bakteriyemi Gereksinimi:** Bu yolun işlemesi için hastada öncelikle sistemik bir bakteriyemi "
        "veya mikobakteriyemi odağı bulunmalıdır.\n"
        "- **Böbrek Dolaşımı:** Renal kan akımının vücut kalp debisinin yaklaşık %20-25'ini alması "
        "nedeniyle kanda dolaşan bazı özel patojenler glomerüllere ve renal parankime ekilebilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Hematojen yol tüm ÜSE'lerin %2'den azını (<%2) oluşturur."
    )
    s14_bullets = [
        "Hematojen yol tüm ÜSE'lerin %2'den azını (<%2) oluşturur.",
        "Sistemik dolaşımdaki bakteriyemi odağından böbreklere yayılım ile gelişir.",
        "Renal parankimin yüksek kanlanması nedeniyle parankimal tutulum ön plandadır."
    ]
    s14_elements = [
        make_cloze("Hematojen yol ile gelişen üriner sistem enfeksiyonları tüm ÜSE'lerin %2'den azını oluşturur.", "%2'den azını", "Hematojen yolun tüm vakalar içindeki küçük yüzdesi"),
        make_table("Hematojen Yolun Genel Özellikleri", ["Özellik", "Değer / Durum", "Klinik Anlamı"], [
            {"cells": [{"text": "Görülme Sıklığı", "isMasked": False}, {"text": "<%2 (tüm ÜSE'lerin)", "isMasked": True, "hint": "yüzde ikiden az görülme"}, {"text": "Nadir görülen bir yayılım şekli"}]},
            {"cells": [{"text": "Primer Kaynak", "isMasked": False}, {"text": "Kan dolaşımı (bakteriyemi)", "isMasked": False}, {"text": "Sistemik enfeksiyon odağı varlığı", "isMasked": True, "hint": "başka odaktan kana karışma"}]}
        ]),
        make_chain("Hematojen Bulaş Mekanizması", [
            "1. Primer Odak: Vücudun başka bir bölgesinde enfeksiyon gelişmesi.",
            "2. Bakteriyemi: Patojenin venöz ve arteryel kan dolaşımına geçişi.",
            "3. Renal Filtrasyon: Renal arter yoluyla böbrek glomerül ve parankimine ulaşma.",
            "4. Parankimal Hasar: Böbrek dokusunda mikroapseler ve enfeksiyon odağı."
        ]),
        make_recall("Hematojen yol tüm üriner sistem enfeksiyonlarının yüzde kaçını oluşturur?", "Tüm ÜSE'lerin %2'den azını (<%2) oluşturur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hematojen Yol Sıklığı", [
            {"text": "Hematojen yol tüm ÜSE'lerin %2'den azını oluşturur.", "isLie": False, "explanation": "Doğru. Ders notu temel verisidir."},
            {"text": "Hematojen yayılım bakteriyemi zemininde böbreklere mikroorganizma ekilmesiyle olur.", "isLie": False, "explanation": "Doğru. Kan yoluyla bulaşır."},
            {"text": "Tüm dünyadaki ÜSE'lerin %95'i hematojen yolla ortaya çıkar.", "isLie": True, "explanation": "Tuzak! Vakaların %98'den fazlası asendan yolladır; hematojen yol <%2'dir."},
            {"text": "Böbrek kan akımının yüksek olması hematojen ekilmeye zemin hazırlar.", "isLie": False, "explanation": "Doğru. Yüksek debi filtre edilir."}
        ]),
        make_quiz("Hematojen yol ile gelişen üriner sistem enfeksiyonlarının tüm ÜSE'ler içindeki oranı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "%2'den azı", "isCorrect": True, "explanation": "Ders notunda açıkça 'tüm ÜSE'lerin %2'den azı' olarak belirtilmiştir."},
            {"key": "B", "text": "%50'si", "isCorrect": False, "explanation": "Bu oran çok yüksektir."},
            {"key": "C", "text": "%98'den fazlası", "isCorrect": False, "explanation": "Bu asendan yolun payıdır."},
            {"key": "D", "text": "%25'i", "isCorrect": False, "explanation": "Hematojen yol %2'den azdır."}
        ])
    ]
    slides.append(make_slide(14, "Hematojen Yayılım ve Görülme Oranı (<%2)", "Hematojen yolun sıklığı, bakteriyemi ilişkisi ve genel özellikleri", "Bulaş Yolları", s14_narrative, s14_bullets, s14_elements))

    # Slide 15: Hematojen Yolla Bulaşan Klasik Etkenler
    s15_narrative = (
        "Hematojen yolla üriner sisteme ulaşan mikroorganizmalar, klasik asendan yoldaki enterik "
        "bakterilerden oldukça farklı spesifik bir mikrobiyolojik profile sahiptir.\n\n"
        "- **Klasik Patojenler:** Hematojen yolla böbreğe ulaşan en tipik etkenler **Staphylococcus aureus, "
        "Salmonella spp. ve tüberküloz (Mycobacterium tuberculosis)** etkenleridir.\n"
        "- **S. aureus:** Başka bir odaktaki stafilokoksik bakteriyemi veya endokardit sonucu böbrek "
        "korteksine ekilerek renal apselere yol açabilir.\n"
        "- **Salmonella ve Tüberküloz:** Salmonella bakteriyemisi veya tüberkülozun primer akciğer "
        "odağından hematojen yayılımı böbrek parankiminde granülomatöz lezyonlar oluşturur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Hematojen yolla böbreğe ulaşan tipik etkenler: S. aureus, Salmonella spp. ve tüberkülozdur."
    )
    s15_bullets = [
        "Hematojen yolla bulaşan etkenler: S. aureus, Salmonella spp., tüberküloz.",
        "S. aureus bakteriyemisi böbrekte kortikal mikroapseler oluşturabilir.",
        "Salmonella ve Mycobacterium tuberculosis hematojen yayılımla renal parankimi tutar."
    ]
    s15_elements = [
        make_cloze("Hematojen yolla üriner sisteme ulaşan en tipik etkenler S. aureus, Salmonella spp. ve tüberküloz bakterileridir.", "S. aureus, Salmonella spp. ve tüberküloz", "Hematojen yayılım gösteren üç klasik patojen"),
        make_table("Hematojen Patojenler ve Klinik Özellikleri", ["Mikroorganizma", "Bakteriyemi Odağı", "Böbrekteki Patoloji"], [
            {"cells": [{"text": "S. aureus", "isMasked": False}, {"text": "Deri/yumuşak doku veya endokardit", "isMasked": True, "hint": "stafilokok primer odağı"}, {"text": "Böbrek korteks apseleri"}]},
            {"cells": [{"text": "Salmonella spp.", "isMasked": False}, {"text": "Gastrointestinal invazyon ve bakteriyemi", "isMasked": False}, {"text": "Parankimal enfeksiyon ve bakteriüri", "isMasked": True, "hint": "salmonella renal tutulumu"}]},
            {"cells": [{"text": "Tüberküloz", "isMasked": False}, {"text": "Akciğer primer enfeksiyonu", "isMasked": True, "hint": "primer mikobakteri odağı"}, {"text": "Renal granülomatöz parankim hasarı"}]}
        ]),
        make_chain("Hematojen Etkenlerin Böbrek Tutulum Sırası", [
            "1. Bakteriyemi: S. aureus, Salmonella veya Tbc'nin kana karışması.",
            "2. Renal Kortikal Ekilme: Glomerüler kapiller yatakta tutulma.",
            "3. Parankimal Hasar: Apse veya granülomatöz nekroz oluşumu.",
            "4. Toplayıcı Sisteme Açılma: İdrarla mikroorganizmanın atılması."
        ]),
        make_recall("Hematojen yolla üriner sisteme ulaşarak enfeksiyon oluşturan üç temel etken nedir?", "Staphylococcus aureus, Salmonella spp. ve tüberkülozdur (Mycobacterium tuberculosis)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hematojen Etkenler", [
            {"text": "Hematojen yolla bulaşan tipik etkenler S. aureus, Salmonella spp. ve tüberkülozdur.", "isLie": False, "explanation": "Doğru. Ders notundaki birebir listedir."},
            {"text": "S. aureus bakteriyemisi böbrekte apse gelişimine neden olabilir.", "isLie": False, "explanation": "Doğru. Klasik kortikal apse yapar."},
            {"text": "Mycobacterium tuberculosis üriner sisteme sadece havuz suyundan asendan tırmanarak girer.", "isLie": True, "explanation": "Tuzak! Tüberküloz böbreğe akciğer odağından hematojen yolla ulaşır."},
            {"text": "Salmonella bakteriyemisi sonrasında idrarda üreme saptanabilir.", "isLie": False, "explanation": "Doğru. Hematojen yolla böbreği tutar."}
        ]),
        make_quiz("Aşağıdaki mikroorganizmalardan hangisi üriner sisteme tipik olarak HEMATOJEN yolla ulaşan etkenler arasında yer alır?", [
            {"key": "A", "text": "Staphylococcus aureus", "isCorrect": True, "explanation": "Ders notunda hematojen yol etkenleri: S. aureus, Salmonella spp. ve tüberküloz olarak açıkça sıralanmıştır."},
            {"key": "B", "text": "Yalnızca bağırsakta yaşayan non-patojen suşlar", "isCorrect": False, "explanation": "Non-patojen suşlar enfeksiyon yapmaz."},
            {"key": "C", "text": "Adenovirus tip 40", "isCorrect": False, "explanation": "Ders notundaki hematojen listede yer almaz."},
            {"key": "D", "text": "Giardia lamblia", "isCorrect": False, "explanation": "Giardia üriner traktusu tutmaz."}
        ])
    ]
    slides.append(make_slide(15, "Hematojen Etkenler: S. aureus, Salmonella ve Tbc", "Hematojen yolla böbreğe ulaşan spesifik mikroorganizmalar ve parankim hasarı", "Bulaş Yolları", s15_narrative, s15_bullets, s15_elements))

    # Slide 16: Hematojen Yolda Bakteriyemi ve Böbrek Apsesi İlişkisi
    s16_narrative = (
        "Hematojen yolla gelişen üriner enfeksiyonun en belirgin patolojik özelliği, sürecin doğrudan "
        "böbrek parankiminde başlaması ve apse oluşturabilmesidir.\n\n"
        "- **Bakteriyemi → Böbrek:** Kan yoluyla gelen bakteriler mesaneden değil, renal arter "
        "üzerinden glomerüler dolaşıma girer: **bakteriyemi → böbrek (apse +/-)**.\n"
        "- **Renal Apse:** Özellikle Staphylococcus aureus gibi piyojenik bakteriler, kortikal kılcal "
        "damarlarda mikroemboliler oluşturarak lokal nekroz ve parankim apseleri geliştirir.\n"
        "- **Klinik Ayırım:** Asendan piyelonefritte enfeksiyon pelvisten parankime tırmanırken, "
        "hematojende doğrudan parankimden başlayıp toplayıcı sisteme açılır.\n\n"
        "> [!IMPORTANT]\n"
        "> Hematojen yolda patofizyolojik akış 'bakteriyemi → böbrek (apse +/-)' şeklindedir; primer hasar böbrek parankiminde ortaya çıkar."
    )
    s16_bullets = [
        "Hematojen patofizyolojik akış: bakteriyemi → böbrek (apse +/-).",
        "Patojenler doğrudan böbrek parankimine ekilerek apse oluşturabilir.",
        "Asendan enfeksiyondan farklı olarak enfeksiyon merkezden parankime değil, doğrudan parankimde başlar."
    ]
    s16_elements = [
        make_cloze("Hematojen yayılımda patolojik süreç bakteriyemi → böbrek (apse +/-) şeklinde parankimal tutulumla gelişir.", "bakteriyemi → böbrek (apse +/-)", "Kan dolaşımından böbrek parankimine ve apseye uzanan akış"),
        make_table("Asendan vs Hematojen Böbrek Tutulumu", ["Özellik", "Asendan Piyelonefrit", "Hematojen Renal Enfeksiyon"], [
            {"cells": [{"text": "Başlangıç Noktası", "isMasked": False}, {"text": "Mesane ve üreter", "isMasked": True, "hint": "alt üriner yollar"}, {"text": "Kan dolaşımı (bakteriyemi)"}]},
            {"cells": [{"text": "Böbrek İçi Odak", "isMasked": False}, {"text": "Medulla ve pelvis renalis", "isMasked": False}, {"text": "Kortikal parankim apsesi (+/-)", "isMasked": True, "hint": "kortekste apse oluşumu"}]}
        ]),
        make_chain("Hematojen Böbrek Apsesi Gelişim Sırası", [
            "1. Sistemik Bakteriyemi: S. aureus'un kan dolaşımına yayılması.",
            "2. Glomerüler Filtreleme: Renal kortikal kapillerlerde embolizasyon.",
            "3. Nekroz ve Süpürasyon: Nötrofil infiltrasyonu ve doku erimesi.",
            "4. Böbrek Apsesi: Parankimde lokalize apse kavitesinin belirmesi."
        ]),
        make_recall("Hematojen yayılımın ders notundaki patogenetik akış formülü nedir?", "bakteriyemi → böbrek (apse +/-) şeklindedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bakteriyemi ve Böbrek Apsesi", [
            {"text": "Hematojen yolda süreç bakteriyemi → böbrek (apse +/-) şeklinde ilerler.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Hematojen yolla ulaşan S. aureus böbrekte apse yapabilir.", "isLie": False, "explanation": "Doğru. Piyojenik apse etkenidir."},
            {"text": "Hematojen yolda bakteriler böbreğe asla ulaşamaz, daima üretra sfinkterinde bloke olur.", "isLie": True, "explanation": "Tuzak! Hematojen yolda bakteriler kanla doğrudan böbrek parankimine gelir."},
            {"text": "Böbrek parankiminde apse oluşumu hematojen yayılımın önemli bir komplikasyonudur.", "isLie": False, "explanation": "Doğru. Klinik öneme sahiptir."}
        ]),
        make_quiz("Hematojen üriner enfeksiyonun patogenetik seyri ve olası parankimal komplikasyonu aşağıdakilerden hangisinde doğru özetlenmiştir?", [
            {"key": "A", "text": "bakteriyemi → böbrek (apse +/-)", "isCorrect": True, "explanation": "Ders notundaki birebir patofizyolojik tanımdır."},
            {"key": "B", "text": "üretra → mesane → prostat", "isCorrect": False, "explanation": "Bu lokal asendan yayılımdır."},
            {"key": "C", "text": "safra kesesi → karaciğer → akciğer", "isCorrect": False, "explanation": "Üriner sistemle ilgisizdir."},
            {"key": "D", "text": "cilt yarası → lenf nodu → kemik iliği", "isCorrect": False, "explanation": "Üriner sistemi açıklamaz."}
        ])
    ]
    slides.append(make_slide(16, "Bakteriyemi ve Böbrek Apsesi İlişkisi", "Hematojen yayılımda parankim tutulumu ve renal apse patofizyolojisi", "Patofizyoloji", s16_narrative, s16_bullets, s16_elements))

    # Slide 17: Lenfatik Yol: Önemi Belirsiz Rota
    s17_narrative = (
        "Mikroorganizmaların üriner sisteme ulaşmasında teorik olarak öne sürülen yollardan biri "
        "de lenfatik drenaj kanallarıdır.\n\n"
        "- **Klinik Önem:** ÜSE patogenezinde **lenfatik yolun önemi belirsizdir**.\n"
        "- **Anatomik Bağlantılar:** Rektum, kolon veya retroperitoneal lenfatik kanallarla böbrek "
        "kapsülü ve üreter lenfatikleri arasında mikroskobik bağlantılar tanımlanmıştır.\n"
        "- **Deneysel vs Klinik:** Deneysel modellerde lenfatik yolla bakteri geçişi gösterilebilmiş "
        "olsa da, klinik pratikte primer enfeksiyon kaynağı olarak kanıtlanması son derece güçtür.\n\n"
        "> [!NOTE]\n"
        "> Ders notuna göre lenfatik yolun üriner sistem enfeksiyonlarındaki klinik önemi belirsizdir."
    )
    s17_bullets = [
        "Lenfatik yol: ÜSE patogenezindeki önemi belirsizdir.",
        "Retroperitoneal ve pelvik lenfatik damarlar teorik geçiş yollarını oluşturur.",
        "Klinik pratikte asendan ve hematojen yolların gerisinde, kanıtlanması güç bir yoldur."
    ]
    s17_elements = [
        make_cloze("Üriner sistem enfeksiyonlarında mikroorganizmaların yayılımında lenfatik yolun önemi belirsizdir.", "önemi belirsizdir", "Lenfatik yolun tıp literatüründeki klinik durumu"),
        make_table("Bulaş Yollarının Klinik Kanıt Düzeyi", ["Bulaş Yolu", "Klinik Kanıt Durumu", "Pratik Önemi"], [
            {"cells": [{"text": "Asendan Yol", "isMasked": False}, {"text": "Açık ve kesin kanıtlanmış", "isMasked": True, "hint": "en net kanıtlı yol"}, {"text": "En önemli ana yol"}]},
            {"cells": [{"text": "Lenfatik Yol", "isMasked": False}, {"text": "Önemi belirsizdir", "isMasked": False}, {"text": "Rutin klinikte rolü net değildir", "isMasked": True, "hint": "tartışmalı klinik katkı"}]}
        ]),
        make_chain("Lenfatik Yol Teorisi", [
            "1. Bağırsak Duvarı: Kolonik lenfatik pleksusta bakteri girişi.",
            "2. Retroperitoneal Damarlar: Lenfatik akımla üreter komşuluğuna ilerleme.",
            "3. Renal Kapsül: Kapsüler lenfatiklerle böbreğe temas teorisi.",
            "4. Klinik Durum: Bu mekanizmanın pratikteki önemi belirsizdir."
        ]),
        make_recall("Ders notuna göre lenfatik yolun ÜSE patogenezindeki klinik önemi nedir?", "Önemi belirsizdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Lenfatik Yol", [
            {"text": "Lenfatik yolun ÜSE'deki önemi belirsizdir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Lenfatik yolla yayılım teorik olarak tanımlanmış bir olasılıktır.", "isLie": False, "explanation": "Doğru. Literatürde tartışılır."},
            {"text": "Lenfatik yol dünyadaki tüm sistitlerin %100 kesin kanıtlanmış tek nedenidir.", "isLie": True, "explanation": "Tuzak! Lenfatik yolun önemi belirsizdir; sistitlerin nedeni asendan yoldur."},
            {"text": "Klinik pratikte asendan yol lenfatik yoldan çok daha belirleyicidir.", "isLie": False, "explanation": "Doğru. Asendan yol en önemli yoldur."}
        ]),
        make_quiz("Ders notuna göre mikroorganizmaların üriner sisteme ulaşmasında 'lenfatik yol' için aşağıdakilerden hangisi söylenebilir?", [
            {"key": "A", "text": "Önemi belirsizdir", "isCorrect": True, "explanation": "Ders notunda 'Lenfatik yol: önemi belirsizdir' ifadesi açıkça yer almaktadır."},
            {"key": "B", "text": "En sık görülen bulaş yoludur", "isCorrect": False, "explanation": "En sık asendan yoldur."},
            {"key": "C", "text": "Tüm ÜSE'lerin %50'sini oluşturur", "isCorrect": False, "explanation": "Önemi belirsizdir."},
            {"key": "D", "text": "Sadece S. aureus'a özgü bir yoldur", "isCorrect": False, "explanation": "S. aureus hematojen yolla ilişkilidir."}
        ])
    ]
    slides.append(make_slide(17, "Lenfatik Yol: Önemi Belirsiz Yayılım Rotası", "Lenfatik yolun teorik temeli ve literatürdeki belirsiz klinik önemi", "Bulaş Yolları", s17_narrative, s17_bullets, s17_elements))

    # Slide 18: Komşuluk Yolu ve Fistül Mekanizması
    s18_narrative = (
        "Mikroorganizmaların üriner traktusa doğrudan komşu organlardan geçişi, anatomik bütünlüğün "
        "bozulduğu özel cerrahi ve patolojik durumlarda gözlenir.\n\n"
        "- **Komşuluk Yolu:** Dördüncü bulaş yolu **komşuluk yolu** olup temel mekanizması "
        "**fistül** oluşumudur.\n"
        "- **Fistül Tipleri:** En sık izlenen örnek gastrointestinal sistem ile mesane arasındaki bağlantıyı "
        "sağlayan vezikoenterik (kolovezikal) fistüllerdir.\n"
        "- **Etiyoloji ve Bulgular:** Divertikülit, kolorektal kanser veya Crohn hastalığı gibi süreçler "
        "fistül oluşturarak idrarda fekaloid koku, pnömatüri ve polimikrobiyal enfeksiyona yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> Komşuluk yoluyla enfeksiyon geçişinde temel mekanizma fistül oluşumudur (ör. vezikoenterik fistül)."
    )
    s18_bullets = [
        "Komşuluk yolu: Temel mekanizma fistül oluşumudur.",
        "Komşu organlar (özellikle bağırsak) ile üriner traktus arasında patolojik trakt oluşur.",
        "Divertikülit ve malignite gibi durumlarda vezikoenterik fistüllerle ortaya çıkar."
    ]
    s18_elements = [
        make_cloze("Mikroorganizmaların üriner sisteme komşuluk yolu ile ulaşmasında temel mekanizma fistül oluşumudur.", "fistül", "İki epitelize boşluk arasında patolojik kanal oluşumu"),
        make_table("Komşuluk Yolu ve Fistül Dinamikleri", ["Komponent", "Patolojik Özellik", "Klinik Yansıması"], [
            {"cells": [{"text": "Bulaş Mekanizması", "isMasked": False}, {"text": "Komşuluk yolu", "isMasked": False}, {"text": "Doğrudan organ komşuluğundan geçiş"}]},
            {"cells": [{"text": "Temel Neden", "isMasked": False}, {"text": "Fistül oluşumu (kolovezikal vb.)", "isMasked": True, "hint": "patolojik bağlantı kanalı"}, {"text": "Pnömatüri ve fekalüri gelişimi", "isMasked": True, "hint": "idrardan gaz ve dışkı gelmesi"}]}
        ]),
        make_chain("Komşuluk Yolu Fistül Patogenezi", [
            "1. Komşu Organ Enflamasyonu: Divertikülit veya malignite gelişimi.",
            "2. Doku Erozyonu: Enflamasyonun mesane duvarına penetre olması.",
            "3. Fistül Traktı: Bağırsak lümeni ile mesane arasında kanal açılması.",
            "4. Doğrudan Geçiş: Bağırsak içeriğinin doğrudan mesaneye boşalması."
        ]),
        make_recall("Komşuluk yolu ile mikroorganizmaların üriner sisteme ulaşmasında ders notunda belirtilen temel mekanizma nedir?", "Fistül oluşumudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komşuluk Yolu", [
            {"text": "Komşuluk yolunda temel mekanizma fistül oluşumudur.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Bağırsak ile mesane arasındaki fistüller komşuluk yoluyla enfeksiyon yapabilir.", "isLie": False, "explanation": "Doğru. Kolovezikal fistüller buna örnektir."},
            {"text": "Komşuluk yolu havadan geçen virüslerin cildi eritip böbreğe girmesiyle oluşur.", "isLie": True, "explanation": "Tuzak! Komşuluk yolu komşu organ patolojilerinde fistül ile doğrudan geçiştir."},
            {"text": "Divertikülit veya tümörler komşuluk fistüllerine zemin hazırlayabilir.", "isLie": False, "explanation": "Doğru. Klasik fistül nedenleridir."}
        ]),
        make_quiz("Mikroorganizmaların üriner sisteme 'komşuluk yolu' ile ulaşmasında temel patolojik mekanizma aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Fistül", "isCorrect": True, "explanation": "Ders notunda 'Komşuluk yolu: fistül' şeklinde net olarak verilmiştir."},
            {"key": "B", "text": "Sistemik bakteriyemi", "isCorrect": False, "explanation": "Bu hematojen yolun mekanizmasıdır."},
            {"key": "C", "text": "Retrograd intraluminal tırmanış", "isCorrect": False, "explanation": "Bu asendan yolun mekanizmasıdır."},
            {"key": "D", "text": "Aşırı Tamm-Horsfall proteini üretimi", "isCorrect": False, "explanation": "Bu bir konak savunma faktörüdür."},
        ])
    ]
    slides.append(make_slide(18, "Komşuluk Yolu ve Fistül ile Bulaş", "Komşu organlardan doğrudan geçiş ve fistül oluşumu dinamikleri", "Bulaş Yolları", s18_narrative, s18_bullets, s18_elements))

    # Slide 19: İkinci Bölüm Özeti: Bulaş Yolları Karşılaştırması
    s19_narrative = (
        "Mikroorganizmaların üriner sisteme ulaşmasında rol oynayan dört farklı yol, sıklık ve "
        "klinik seyir bakımından net sınırlarla birbirinden ayrılır.\n\n"
        "- **Asendan Yol:** En önemli yoldur (%98+); üretra → mesane → üreter → böbrek sıralamasıyla "
        "retrograd tırmanışı ifade eder.\n"
        "- **Hematojen Yol:** Tüm ÜSE'lerin %2'den azını oluşturur; bakteriyemi zemininde böbreğe "
        "ulaşır (S. aureus, Salmonella, tüberküloz) ve parankim apseleri yapabilir.\n"
        "- **Lenfatik ve Komşuluk:** Lenfatik yolun önemi belirsizdir; komşuluk yolu ise fistül "
        "aracılığıyla doğrudan komşu organlardan geçişle gerçekleşir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] Asendan yol en önemli yoldur; hematojen yol <%2 olup S. aureus, Salmonella ve Tbc ile seyreder; lenfatik yol önemsiz/belirsiz, komşuluk ise fistül ile karakterizedir."
    )
    s19_bullets = [
        "Asendan: En önemli yol; üretra → mesane → üreter → böbrek sırasıyla ilerler.",
        "Hematojen: Tüm ÜSE'lerin <%2'si; S. aureus, Salmonella, tüberküloz etkenleridir.",
        "Lenfatik: Önemi belirsiz; Komşuluk: Fistül mekanizması ile doğrudan geçiştir."
    ]
    s19_elements = [
        make_cloze("Mikroorganizmaların üriner sisteme ulaşmasında en önemli yol asendan yol olup hematojen yol tüm ÜSE'lerin %2'den azını oluşturur.", "%2'den azını", "Hematojen yolun ÜSE içindeki küçük payı"),
        make_table("Bulaş Yollarının Karşılaştırma Matrisi", ["Bulaş Yolu", "Görülme Oranı / Önem", "Tipik Etken / Mekanizma"], [
            {"cells": [{"text": "Asendan", "isMasked": False}, {"text": "En önemli yol", "isMasked": True, "hint": "birinci sıradaki ana yol"}, {"text": "Üretra → mesane → üreter → böbrek"}]},
            {"cells": [{"text": "Hematojen", "isMasked": False}, {"text": "<%2", "isMasked": False}, {"text": "S. aureus, Salmonella, Tbc (apse +/-)", "isMasked": True, "hint": "hematojen klasik etkenler"}]},
            {"cells": [{"text": "Lenfatik", "isMasked": False}, {"text": "Önemi belirsiz", "isMasked": True, "hint": "literatürdeki durumu"}, {"text": "Retroperitoneal lenf kanalları"}]},
            {"cells": [{"text": "Komşuluk", "isMasked": False}, {"text": "Özel durumlar", "isMasked": False}, {"text": "Fistül oluşumu", "isMasked": True, "hint": "organlar arası tünel"}]}
        ]),
        make_recall("Dört bulaş yolunun sıklık ve mekanizma özetini tek cümlede nasıl ifade edersiniz?", "Asendan yol en önemli ve en sık yoldur; hematojen yol <%2 (S. aureus, Salmonella, Tbc); lenfatik yolun önemi belirsizdir; komşuluk yolu ise fistül ile gelişir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bulaş Yolları Özeti", [
            {"text": "Asendan yol mikroorganizmaların üriner sisteme ulaşmasında en önemli yoldur.", "isLie": False, "explanation": "Doğru. Ana yoldur."},
            {"text": "Hematojen yol tüm ÜSE'lerin %2'den azını oluşturur.", "isLie": False, "explanation": "Doğru. Küçük bir orandır."},
            {"text": "S. aureus, Salmonella ve tüberküloz klasik asendan sistit etkenleridir.", "isLie": True, "explanation": "Tuzak! S. aureus, Salmonella ve tüberküloz tipik olarak hematojen yolla böbreğe ulaşan etkenlerdir."},
            {"text": "Komşuluk yolu fistül aracılığıyla gerçekleşir.", "isLie": False, "explanation": "Doğru. Mekanizma fistüldür."}
        ]),
        make_quiz("İkinci bölümdeki bulaş yolları özeti değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Hematojen yol tüm ÜSE'lerin %90'ını oluşturur ve en önemli yoldur", "isCorrect": True, "explanation": "Yanlış! En önemli yol asendan yoldur; hematojen yol tüm ÜSE'lerin %2'den azını oluşturur."},
            {"key": "B", "text": "Asendan yol üretra → mesane → üreter → böbrek şeklinde ilerler", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Lenfatik yolun ÜSE patogenezindeki önemi belirsizdir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Komşuluk yolu ile bulaşta temel mekanizma fistüldür", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(19, "İkinci Bölüm Özeti: Bulaş Yolları Karşılaştırması", "Asendan, hematojen, lenfatik ve komşuluk yollarının tam özeti", "Bölüm Özeti", s19_narrative, s19_bullets, s19_elements))

    # Slide 20: [TEKRAR SAYFASI - CHECKPOINT 2] Bulaş Yolları ve Patofizyoloji
    s20_narrative = (
        "Bu tekrar sayfasında 2. Bölümde işlenen mikroorganizmaların üriner sisteme ulaşma yolları, "
        "asendan ilerleyiş hiyerarşisi ve hematojen patojenleri pekiştiriyoruz.\n\n"
        "- **Asendan Yol:** En önemli yoldur; anatomik sıra **üretra → mesane → üreter → böbrek** "
        "şeklinde yukarı doğru ilerler.\n"
        "- **Hematojen Yol:** Tüm ÜSE'lerin **%2'den azını** oluşturur; bakteriyemi → böbrek (apse +/-) "
        "seyri gösterir ve etkenleri **S. aureus, Salmonella spp., tüberküloz**dur.\n"
        "- **Diğer Yollar:** Lenfatik yolun önemi belirsizdir; komşuluk yolunda ise temel mekanizma "
        "**fistül** oluşumudur.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 2] Asendan yol en sık ve en önemli yoldur (üretra→mesane→üreter→böbrek); hematojen yol <%2 olup S. aureus, Salmonella ve Tbc ile seyreder; lenfatik önemsiz, komşuluk ise fistülle karakterizedir."
    )
    s20_bullets = [
        "Asendan: En önemli yol; sıra üretra → mesane → üreter → böbrek.",
        "Hematojen: Tüm ÜSE'lerin <%2'si; S. aureus, Salmonella spp., tüberküloz (bakteriyemi → apse).",
        "Lenfatik: Önemi belirsiz; Komşuluk: Fistül mekanizması."
    ]
    s20_elements = [
        make_cloze("Asendan yolun ilerleme sırası üretra → mesane → üreter → böbrek olup en önemli yoldur.", "üretra → mesane → üreter → böbrek", "Asendan yolun tam anatomik sırası"),
        make_table("2. Bölüm Büyük Tekrar Tablosu", ["Bulaş Yolu", "Oran / Önem", "Etken / Mekanizma"], [
            {"cells": [{"text": "Asendan Yol", "isMasked": False}, {"text": "En önemli yol", "isMasked": True, "hint": "birinci sıradaki ana rota"}, {"text": "Üretra → mesane → üreter → böbrek"}]},
            {"cells": [{"text": "Hematojen Yol", "isMasked": False}, {"text": "<%2", "isMasked": False}, {"text": "S. aureus, Salmonella, Tbc (apse +/-)", "isMasked": True, "hint": "hematojen klasik etkenler"}]},
            {"cells": [{"text": "Lenfatik Yol", "isMasked": False}, {"text": "Önemi belirsiz", "isMasked": True, "hint": "literatürdeki klinik önemi"}, {"text": "Lenf kanalları"}]},
            {"cells": [{"text": "Komşuluk Yolu", "isMasked": False}, {"text": "Nadir / İstisnai", "isMasked": False}, {"text": "Fistül mekanizması", "isMasked": True, "hint": "organlar arası patolojik geçit"}]}
        ]),
        make_chain("Bulaş Yollarının Karşılaştırmalı Özeti", [
            "1. Asendan: Fekal flora kolonizasyonu → lümenden yukarı tırmanış.",
            "2. Hematojen: Sistemik bakteriyemi → glomerüler ekilme ve apse.",
            "3. Komşuluk: Bağırsak/mesane patolojisi → fistül oluşumu ile geçiş.",
            "4. Lenfatik: Teorik drenaj → önemi klinik olarak belirsiz rota."
        ]),
        make_recall("Checkpoint 2: Hematojen yolla bulaşan üç klasik etken nedir ve hematojen yolun görülme oranı kaçtır?", "S. aureus, Salmonella spp. ve tüberkülozdur; tüm ÜSE'lerin %2'den azını (<%2) oluşturur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 2 Konsolidasyonu", [
            {"text": "Asendan yol en önemli yoldur ve üretra → mesane → üreter → böbrek şeklinde ilerler.", "isLie": False, "explanation": "Doğru. 2. bölümün temel kuralıdır."},
            {"text": "Hematojen yol tüm ÜSE'lerin %2'den azını oluşturur.", "isLie": False, "explanation": "Doğru. Düşük orana sahiptir."},
            {"text": "ÜSE'de lenfatik yol en sık görülen yoldur ve her hastada mutlaka saptanır.", "isLie": True, "explanation": "Tuzak! Lenfatik yolun önemi belirsizdir, en sık yol asendan yoldur."},
            {"text": "Komşuluk yolunda temel mekanizma fistül oluşumudur.", "isLie": False, "explanation": "Doğru. Fistül ile geçiş olur."}
        ]),
        make_quiz("2. Bölümün tamamı (Bulaş Yolları ve Patofizyoloji) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Hematojen yolla böbreğe ulaşan tipik etkenler yalnızca E. coli ve Proteus suşlarıdır", "isCorrect": True, "explanation": "Yanlış! Hematojen yolla bulaşan klasik etkenler S. aureus, Salmonella spp. ve tüberkülozdur (E. coli tipik olarak asendan yolladır)."},
            {"key": "B", "text": "Asendan yol mikroorganizmaların üriner sisteme ulaşmasında en önemli yoldur", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Asendan yolda ilerleme sırası üretra → mesane → üreter → böbrek şeklindedir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Hematojen yol tüm ÜSE'lerin %2'den azını oluşturur", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(20, "[TEKRAR SAYFASI - CHECKPOINT 2] Bulaş Yolları ve Patofizyoloji", "2. Bölümün kapsamlı pekiştirmesi: asendan, hematojen, lenfatik ve komşuluk yolları", "Bölüm Tekrarı", s20_narrative, s20_bullets, s20_elements))

    return slides
