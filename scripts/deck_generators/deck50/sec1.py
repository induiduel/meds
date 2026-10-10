import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec1():
    slides = []

    # Slide 1: Spiroketler ve Treponema Cinsinin Morfolojisi
    s1_narrative = (
        "Spiroketler (Spirochaetales), ince, uzun ve tirbüşon benzeri helikal spiral kıvrımlara "
        "sahip mikroaerofilik veya anaerobik özelleşmiş bakteriler grubudur.\n\n"
        "- **Hücre Duvarı Mimarisi:** Sitoplazmik membran, ince bir peptidoglikan tabakası ve dış membrandan "
        "meydana gelen, yapısal olarak **Gram negatif bakterilere benzeyen** bir hücre duvarına sahiptir.\n"
        "- **Boyanma Kısıtlılığı:** Son derece ince ve narin gövde yapısı (çapı 0.1-0.2 mikron) nedeniyle "
        "rutin ışık mikroskobunda ve **standart Gram boyası ile iyi boyanmaz ve görülemez**.\n"
        "- **Doğrudan İnceleme:** Canlı mikroorganizmanın görselleştirilmesinde **karanlık saha mikroskobisi** "
        "veya gümüşleme yöntemleri altın standarttır.\n\n"
        "> [!NOTE]\n"
        "> Treponema pallidum Gram negatif benzeri duvar yapısına sahip olmasına karşın narinliği nedeniyle Gram boyasıyla boyanamaz; karanlık saha ile izlenir."
    )
    s1_bullets = [
        "Spiral helikal kıvrımlı, ince yapılı spiroketlerdir.",
        "Gram negatif benzeri duvara sahiptir ancak Gram boyasıyla boyanmaz.",
        "Canlı bakteriler karanlık saha mikroskobisi ile incelenir."
    ]
    s1_elements = [
        make_cloze("Treponema pallidum standart Gram boyasıyla boyanamadığından canlı hareketleri karanlık saha mikroskopisi ile incelenir.", "karanlık saha", "Işık yerine kırılan ışınlarla mikroorganizmayı aydınlatan yöntem"),
        make_table("Spiroketlerin Morfolojik Özellikleri", ["Özellik", "Yapısal Karakteri", "Klinik / Tanısal Yansıması"], [
            {"cells": [{"text": "Morfolojik Şekil", "isMasked": False}, {"text": "Helikal spiral, tirbüşon kıvrımları", "isMasked": True, "hint": "burgu şeklinde kıvrımlı gövde"}, {"text": "Doku aralıklarına vidalanarak penetrasyon"}]},
            {"cells": [{"text": "Gram Boyanma", "isMasked": False}, {"text": "Çok ince olduğundan boya tutmaz", "isMasked": False}, {"text": "Karanlık saha veya gümüşleme zorunluluğu", "isMasked": True, "hint": "özel optik veya kimyasal boyama gereği"}]}
        ]),
        make_chain("Spiroket Morfolojisi ve Mikroskopi", [
            "1. İnce Boyut: Bakteri çapı 0.2 mikron gibi ışık dalga boyu sınırındadır.",
            "2. Standart Boya Yetersizliği: Rutin Gram boyamada kristal viyoleyi gösteremez.",
            "3. Karanlık Saha Optiği: Yan açıdan gelen ışık demeti spiroket yüzeyinden yansır.",
            "4. Parlak Görüntü: Karanlık fon üzerinde parlak gümüşi helezonlar seçilir."
        ]),
        make_recall("Treponema pallidum neden standart Gram boyası ile ışık mikroskobunda incelenemez ve hangi yöntemle görülür?", "Çok ince ve narin duvar yapısı nedeniyle Gram boyasını seçtirmez; canlı bakteriler karanlık saha mikroskopisi ile görülür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Spiroket Morfolojisi", [
            {"text": "Spiroketler spiral şekilli, ince duvar yapılı bakterilerdir.", "isLie": False, "explanation": "Doğru. Tipik spiral bakterilerdir."},
            {"text": "Gram boyası ile iyi boyanmazlar, karanlık sahada görülürler.", "isLie": False, "explanation": "Doğru. Standart Gram ile saptanamazlar."},
            {"text": "Treponema pallidum kalın zırhlı ve 10 santimetre boyunda bir bağırsak solucanıdır.", "isLie": True, "explanation": "Tuzak! Treponema bir helmint değil, mikroskobik ince bir spiroket bakterisidir."},
            {"text": "Gram negatif hücre duvarına benzer membran tabakaları taşır.", "isLie": False, "explanation": "Doğru. Dış membran ve peptidoglikan içerir."}
        ]),
        make_quiz("Treponema pallidum'un mikroskobik yapısı ve boyanma özelliği ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Gram boyası ile iyi boyanmaz; karanlık saha mikroskobisi ile görülür", "isCorrect": True, "explanation": "Çok ince yapısı nedeniyle Gram tutmaz ve karanlık sahada izlenir."},
            {"key": "B", "text": "Gram pozitif kalın sporlu dev bir basildir", "isCorrect": False, "explanation": "Spor oluşturmaz, spiraldir."},
            {"key": "C", "text": "Hücre zarı bulunmayan çıplak bir virüstür", "isCorrect": False, "explanation": "Prokaryot bir bakteridir."},
            {"key": "D", "text": "Sadece asido-rezistan Erlich-Ziehl-Neelsen ile boyanan bir mantardır", "isCorrect": False, "explanation": "Mantar veya mikobakteri değildir."}
        ])
    ]
    slides.append(make_slide(1, "Spiroketler ve Treponema Cinsinin Morfolojisi", "Helikal spiroket mimarisi, Gram boyanma kısıtlılığı ve karanlık saha mikroskobisi", "Genel Mikrobiyoloji", s1_narrative, s1_bullets, s1_elements))

    # Slide 2: Periplazmik Flajella ve Burgu Hareketi
    s2_narrative = (
        "Treponema cinsine ait spiroketlerin dokularda son derece hızlı yayılmasını ve mukozal "
        "bariyerleri aşmasını sağlayan en özgün lokomotor donanımı **periplazmik flajellalarıdır**.\n\n"
        "- **Periplazmik Yerleşim:** Klasik bakteriler gibi hücre dışına uzanan serbest kamçılar taşımazlar. "
        "Aksiyel filamentler (endoflajella), **dış membran ile peptidoglikan tabakası arasındaki periplazmik aralıkta** yerleşmiştir.\n"
        "- **Burgu (Tirbüşon) Hareketi:** Bu aksiyel flajellaların zıt yönlü kasılmaları, bakterinin gövdesinin "
        "kendi ekseni etrafında dönmesine ve **karakteristik burgu/tirbüşon hareketi** yapmasına olanak tanır.\n"
        "- **Doku Penetrasyonu:** Bu dinamik vidalama hareketi sayesinde spiroket, visköz mukozal sıvıları "
        "ve hücreler arası sıkı bağlantıları burgu gibi delerek damar lümenine hızla penetre olur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Treponema'ların periplazmik aralıkta yer alan flajellaları, bakteriye karakteristik burgu (tirbüşon) hareketini kazandırır ve doku penetrasyonunu sağlar."
    )
    s2_bullets = [
        "Flajellalar dış membran ile duvar arasındaki periplazmik aralıktadır.",
        "Aksiyel filamentler karakteristik burgu (tirbüşon) hareketi yaptırır.",
        "Burgu hareketi visköz mukozayı delerek dokuya hızla girmesini sağlar."
    ]
    s2_elements = [
        make_cloze("Treponema pallidum'a karakteristik burgu hareketini kazandıran aksiyel flajellalar periplazmik aralıkta yerleşmiştir.", "periplazmik", "Dış zar ile peptidoglikan arasındaki anatomik boşluk"),
        make_table("Treponema Motilite Mekanizması", ["Komponent", "Anatomik Konumu", "Fonksiyonu"], [
            {"cells": [{"text": "Aksiyel Filamentler", "isMasked": False}, {"text": "Periplazmik boşluk (endoflajella)", "isMasked": True, "hint": "içte kalan kamçı sistemi"}, {"text": "Gövdeye helikal rotasyon gücü verme"}]},
            {"cells": [{"text": "Burgu Hareketi", "isMasked": False}, {"text": "Tirbüşon şeklinde kendi ekseninde dönme", "isMasked": False}, {"text": "Visköz doku ve mukozaya vidalanma", "isMasked": True, "hint": "dokuları delip geçme yeteneği"}]}
        ]),
        make_chain("Hareketten İnvazyona", [
            "1. Motor Protein Uyarısı: Periplazmik flajellalar mikrotübüler tork üretir.",
            "2. Gövde Rotasyonu: Spiroket gövdesi tirbüşon gibi hızla kendi ekseninde döner.",
            "3. Mukozal Vidalanma: Dönüş kuvveti vajinal/servikal mukus bariyerini aşar.",
            "4. Endotelyal Temas: Bakteri dakikalar içinde perivasküler alana ulaşır."
        ]),
        make_recall("Treponema cinsinde bakterinin tirbüşon (burgu) hareketi yapmasını sağlayan yapay donanım nerededir?", "Dış membran ile hücre duvarı arasındaki periplazmik aralıkta yer alan flajellalardır (endoflajella)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Treponema Motilitesi", [
            {"text": "Periplazmik aralıkta flajellaları bulunur.", "isLie": False, "explanation": "Doğru. Aksiyel filamentler periplazmadadır."},
            {"text": "Bakteri karakteristik burgu hareketi sergiler.", "isLie": False, "explanation": "Doğru. Tirbüşon benzeri hareket eder."},
            {"text": "Treponema pallidum tamamen hareketsiz olup ancak kan grubu değiştiğinde yüzebilen bir mikroptur.", "isLie": True, "explanation": "Tuzak! Treponema son derece hareketlidir; periplazmik kamçılarıyla burgu hareketi yapar."},
            {"text": "Burgu hareketi doku içine vidalanarak penetrasyonu kolaylaştırır.", "isLie": False, "explanation": "Doğru. Patogenezin kilit unsurudur."}
        ]),
        make_quiz("Treponema pallidum'un dokularda hızla ilerlemesini sağlayan tirbüşon (burgu) hareketini oluşturan yapı nerededir?", [
            {"key": "A", "text": "Dış membran ile hücre duvarı arasındaki periplazmik aralıkta", "isCorrect": True, "explanation": "Aksiyel flajellalar periplazmik aralıkta yer alır."},
            {"key": "B", "text": "Hücre çekirdeğinin tam merkezinde", "isCorrect": False, "explanation": "Bakteride çekirdek zarı yoktur."},
            {"key": "C", "text": "Hücrenin en dışındaki 1 metrelik kuyrukta", "isCorrect": False, "explanation": "Dış kamçısı yoktur."},
            {"key": "D", "text": "Mitokondri kristalarında", "isCorrect": False, "explanation": "Bakteride mitokondri bulunmaz."}
        ])
    ]
    slides.append(make_slide(2, "Periplazmik Flajella ve Burgu Hareketi", "Aksiyel filamentler, endoflajella, periplazmik aralık ve tirbüşon penetrasyonu", "Hücresel Motilite", s2_narrative, s2_bullets, s2_elements))

    # Slide 3: Treponema Alt Türleri: Sifiliz, Yaws, Bejel ve Pinta
    s3_narrative = (
        "Treponema cinsi altında morfolojik ve serolojik olarak birbirine çok benzeyen, ancak oluşturdukları "
        "klinik tablolar ve bulaş yolları farklı olan önemli insan patojenleri yer alır.\n\n"
        "- **Treponema pallidum subsp. pallidum:** Veneral **sifiliz (frengi)** etkenidir; cinsel temasla bulaşır "
        "ve tüm dünyada yaygın küresel bir sağlık sorunudur.\n"
        "- **Treponema pallidum subsp. pertenue:** Tropikal bölgelerde (Afrika, Asya, Amerika) cilt temasıyla "
        "bulaşan **Yaws (frambezi)** hastalığının etkenidir; cilt ve kemik tutulumu yapar.\n"
        "- **Treponema pallidum subsp. endemicum:** Orta Doğu ve kurak Afrika'da temas ve ortak kaplarla bulaşan "
        "**Bejel (endemik sifiliz)** etkenidir; cilt ve kemik tutulumu yapar.\n"
        "- **Treponema carateum:** Orta ve Güney Amerika'da cilt temasıyla bulaşan **Pinta** etkenidir; "
        "kronik depigmente cilt lezyonları yapar, **kemik tutulumu kesinlikle yapmaz**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Veneral sifiliz etkeni T. pallidum subsp. pallidum'dur. Yaws ve bejelde cilt ve kemik tutulurken; pintada (T. carateum) cilt tutulur fakat KEMİK TUTULUMU YOKTUR."
    )
    s3_bullets = [
        "Veneral sifiliz etkeni T. pallidum subsp. pallidum'dur (cinsel bulaş).",
        "Yaws (pertenue) ve bejel (endemicum) cilt ve kemik tutulumu yapar.",
        "Pinta (T. carateum) sadece cilt tutulumu yapar, kemik tutulumu yapmaz."
    ]
    s3_elements = [
        make_cloze("Treponema türleri arasında yalnız cilt tutulumu yapıp kemik tutulumu yapmayan etken Treponema carateum olarak bilinir.", "Treponema carateum", "Pinta hastalığının etkeni olan spiroket"),
        make_table("Treponema Türleri ve Hastalık Matrisi", ["Treponema Türü / Alt Türü", "Yol Açtığı Hastalık", "Bulaş ve Organ Tutulumu"], [
            {"cells": [{"text": "T. pallidum subsp. pallidum", "isMasked": False}, {"text": "Veneral Sifiliz (Frengi)", "isMasked": True, "hint": "cinsel yolla bulaşan klasik sifiliz"}, {"text": "Cinsel temas, tüm dünyada yaygın"}]},
            {"cells": [{"text": "T. pallidum subsp. pertenue", "isMasked": False}, {"text": "Yaws (Frambezi)", "isMasked": False}, {"text": "Cilt teması; cilt ve kemik tutulumu", "isMasked": True, "hint": "tropikal cilt ve iskelet tutulumu"}]},
            {"cells": [{"text": "Treponema carateum", "isMasked": False}, {"text": "Pinta", "isMasked": False}, {"text": "Cilt tutulur, KEMİK TUTULUMU YOKTUR", "isMasked": True, "hint": "iskelet tutulumu olmayan form"}]}
        ]),
        make_chain("Treponemal Ayrım Mantığı", [
            "1. Cinsel Bulaş: Veneral sifiliz (subsp. pallidum) genital lezyonla başlar.",
            "2. Non-Veneral Tropikal: Yaws ve bejel cilt temasıyla bulaşıp kemiğe iner.",
            "3. Pinta Farkı: T. carateum dermiste depigmentasyon yapar fakat periostu tutmaz.",
            "4. Serolojik Çaprazlık: Bu türlerin hepsi benzer antikorlar üreterek serolojide pozitifleşir."
        ]),
        make_recall("Yaws ve bejel hastalıkları ile pinta hastalığı arasındaki en kritik kemik tutulumu farkı nedir?", "Yaws ve bejelde cilt ve kemik tutulumu görülürken; pintada (Treponema carateum) cilt tutulumu vardır, kemik tutulumu kesinlikle yoktur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Treponema Alt Türleri", [
            {"text": "T. pallidum subsp. pallidum cinsel yolla bulaşan veneral sifiliz etkenidir.", "isLie": False, "explanation": "Doğru. Klasik sifiliz ajanıdır."},
            {"text": "Yaws ve bejelde cilt ve kemik tutulumu izlenir.", "isLie": False, "explanation": "Doğru. Kemik lezyonları yaparlar."},
            {"text": "Pintada (T. carateum) ağır osteomiyelit ve tüm iskeletin erimesi karakteristiktir.", "isLie": True, "explanation": "Tuzak! Pintada kemik tutulumu YOKTUR; sadece cilt tutulumu görülür."},
            {"text": "T. pallidum subsp. endemicum bejel hastalığına yol açar.", "isLie": False, "explanation": "Doğru. Endemik sifilizdir."}
        ]),
        make_quiz("Treponema türleri içerisinde yalnızca cilt lezyonları oluşturan, kemik tutulumu yapmayan hastalık ve etkeni hangisidir?", [
            {"key": "A", "text": "Pinta (Treponema carateum)", "isCorrect": True, "explanation": "Pinta sadece cilt tutulumu yapar, kemik tutulumu yapmaz."},
            {"key": "B", "text": "Yaws (T. pallidum pertenue)", "isCorrect": False, "explanation": "Kemik tutulumu yapar."},
            {"key": "C", "text": "Bejel (T. pallidum endemicum)", "isCorrect": False, "explanation": "Kemik tutulumu yapar."},
            {"key": "D", "text": "Veneral sifiliz", "isCorrect": False, "explanation": "Tersiyer dönemde kemik tutulumu (gom) yapar."}
        ])
    ]
    slides.append(make_slide(3, "Treponema Alt Türleri: Sifiliz, Yaws, Bejel ve Pinta", "Subsp. pallidum, pertenue (yaws), endemicum (bejel), T. carateum (pinta ve kemik yokluğu)", "Treponema Taksonomisi", s3_narrative, s3_bullets, s3_elements))

    # Slide 4: Küresel Epidemiyoloji ve DSÖ Verileri
    s4_narrative = (
        "Sifiliz, modern antibiyotik çağında kolaylıkla tedavi edilebilmesine karşın dünya genelinde "
        "önemli bir halk sağlığı tehdidi olmaya devam etmektedir.\n\n"
        "- **Küresel Olgu Sayısı:** Dünya Sağlık Örgütü (DSÖ) verilerine göre dünyada tahmini "
        "**yaklaşık 18 milyon aktif sifiliz olgusu** bulunmaktadır; yıllık **6.3 milyon yeni saptanmış olgu** bildirilmektedir.\n"
        "- **Gebelikte Sifiliz Tehdidi:** Her yıl yaklaşık **1 milyon gebede aktif sifiliz** görülmektedir; "
        "tedavi edilmeyen olgularda transplasental geçiş son derece yüksektir.\n"
        "- **İstenmeyen Gebelik Sonuçları:** 930 bin sifilizli gebede yılda **350 bin istenmeyen olay** "
        "(ölü doğum, preterm doğum, neonatal ölüm ve konjenital sifilizli bebek) gerçekleşmektedir.\n\n"
        "> [!NOTE]\n"
        "> Dünyada ~18 milyon sifiliz hastası vardır; her yıl 1 milyon gebe enfekte olmakta ve 350 bin istenmeyen fetal sonuç doğmaktadır."
    )
    s4_bullets = [
        "Dünyada yaklaşık 18 milyon aktif sifiliz olgusu vardır.",
        "Yılda 6.3 milyon yeni olgu bildirilmektedir.",
        "1 milyon gebe enfektedir; yılda 350 bin istenmeyen fetal olay gelişir."
    ]
    s4_elements = [
        make_cloze("DSÖ verilerine göre dünyada yaklaşık 18 milyon aktif sifiliz hastası bulunmaktadır.", "18 milyon", "Dünyadaki tahmini toplam sifiliz hasta sayısı"),
        make_table("DSÖ Küresel Sifiliz İstatistikleri", ["Gösterge", "Sayısal Değer", "Halk Sağlığı Önemi"], [
            {"cells": [{"text": "Aktif Global Havuz", "isMasked": False}, {"text": "Yaklaşık 18 milyon olgu", "isMasked": True, "hint": "dünya genelindeki toplam vaka"}, {"text": "Küresel enfeksiyon rezervuarı"}]},
            {"cells": [{"text": "Enfekte Gebe Sayısı", "isMasked": False}, {"text": "Yılda ~1 milyon gebe", "isMasked": False}, {"text": "350 bin fetal kayıp ve neonatal ölüm", "isMasked": True, "hint": "istenmeyen gebelik komplikasyonu"}]}
        ]),
        make_chain("Epidemiyolojik Yayılım Aşamaları", [
            "1. Cinsel Sirkülasyon: Asemptomatik bireyler bakteriyi topluma aktarır.",
            "2. Yıllık İnsidans: Her yıl 6.3 milyon yeni enfeksiyon havuza eklenir.",
            "3. Gebelikte Geçiş: Tedavisiz gebede spiroket plasentayı aşar.",
            "4. Konjenital Fatura: 350 bin bebek ölü doğum veya ağır sekelle doğar."
        ]),
        make_recall("Dünya Sağlık Örgütü verilerine göre dünyadaki aktif sifiliz vaka sayısı ve enfekte gebe sayısı yaklaşık ne kadardır?", "Yaklaşık 18 milyon aktif olgu ve yılda yaklaşık 1 milyon enfekte gebe bulunmaktadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifiliz Epidemiyolojisi", [
            {"text": "Dünyada yaklaşık 18 milyon sifiliz olgusu bulunmaktadır.", "isLie": False, "explanation": "Doğru. DSÖ küresel tahminidir."},
            {"text": "Yılda yaklaşık 1 milyon gebede aktif sifiliz görülür.", "isLie": False, "explanation": "Doğru. Maternal sifiliz yüküdür."},
            {"text": "Sifiliz dünyadaki tüm ülkelerden tamamen silinmiş, sıfır olgulu bir antik hastalıktır.", "isLie": True, "explanation": "Tuzak! Sifiliz halen yılda 6.3 milyon yeni vaka ile aktif küresel tehdittir."},
            {"text": "Gebelikte sifiliz ölü doğum ve prematüriteye yol açabilir.", "isLie": False, "explanation": "Doğru. 350 bin fetal kayıp bildirilmektedir."}
        ]),
        make_quiz("Dünya Sağlık Örgütü (DSÖ) verilerine göre küresel düzeyde aktif sifiliz olgu sayısı yaklaşık kaçtır?", [
            {"key": "A", "text": "Yaklaşık 18 milyon olgu", "isCorrect": True, "explanation": "DSÖ verilerine göre dünyada ~18 milyon sifiliz olgusu vardır."},
            {"key": "B", "text": "Yalnızca 12 kişi", "isCorrect": False, "explanation": "Çok yaygın küresel hastalıktır."},
            {"key": "C", "text": "8 milyar insanın tamamı", "isCorrect": False, "explanation": "Tüm dünya enfekte değildir."},
            {"key": "D", "text": "Sıfır (Eradike edilmiştir)", "isCorrect": False, "explanation": "Eradike edilmemiştir."}
        ])
    ]
    slides.append(make_slide(4, "Küresel Epidemiyoloji ve DSÖ Verileri", "18 milyon global olgu, 6.3 milyon yıllık insidans, 1 milyon gebe ve konjenital riskler", "Epidemiyoloji ve Halk Sağlığı", s4_narrative, s4_bullets, s4_elements))

    # Slide 5: Bulaş Yolları: Cinsel Temas, Transplasental ve Kan
    s5_narrative = (
        "Treponema pallidum konağa doğrudan temas yollarıyla transfer olan ve dış ortamda "
        "canlılığını hızla kaybeden hassas bir patojendir.\n\n"
        "- **Doğrudan Cinsel Temas:** En sık görülen bulaş yoludur; primer sifilizdeki **şankr** "
        "veya sekonder sifilizdeki **kondiloma lata** gibi spiroketten zengin enfekte mukokutanöz lezyonlarla "
        "doğrudan temas sonucu gerçekleşir.\n"
        "- **Transplasental ve Doğum Yolu:** Enfekte anneden gebeliğin her evresinde plasenta yoluyla fetüse "
        "veya doğum sırasında vajinal kanaldaki lezyonlardan yenidoğana bulaşabilir (konjenital sifiliz).\n"
        "- **Kan Transfüzyonu ve Perkutan Temas:** Bakteriyemik evredeki donörden alınan taze kan transfüzyonu "
        "veya sağlık çalışanlarında enjektör iğnesi batmasıyla perkutan olarak da bulaşabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Sifiliz temel olarak enfekte aktif lezyonlara (şankr, kondiloma lata) doğrudan cinsel temasla, transplasental yolla ve kan transfüzyonuyla bulaşır."
    )
    s5_bullets = [
        "En sık bulaş aktif lezyonlarla (şankr, kondiloma lata) cinsel temastır.",
        "Gebelikte transplasental yolla bebeğe bulaşır.",
        "Kan transfüzyonu ve perkutan yaralanmalar diğer bulaş yollarıdır."
    ]
    s5_elements = [
        make_cloze("Sifiliz bulaşında en tehlikeli lezyonlar bol spiroket içeren primer şankr ve sekonder kondiloma lata plaklarıdır.", "kondiloma lata", "Sekonder sifilizin yüksek bulaştırıcı genital lezyonu"),
        make_table("Sifiliz Bulaş Yolları ve Riskleri", ["Bulaş Yolu", "Etken Kaynağı", "Bulaş Riski / Karakteri"], [
            {"cells": [{"text": "Cinsel Temas", "isMasked": False}, {"text": "Şankr ve kondiloma lata eksüdası", "isMasked": True, "hint": "canlı spiroket dolu lezyon salgısı"}, {"text": "En sık ve primer bulaşma modu"}]},
            {"cells": [{"text": "Transplasental", "isMasked": False}, {"text": "Maternal spiroketemi (kan yolu)", "isMasked": False}, {"text": "Konjenital sifiliz ve fetal ölüm", "isMasked": True, "hint": "bebeğe anne karnında bulaşma"}]}
        ]),
        make_chain("Bulaş Mekanizması Zinciri", [
            "1. Aktif Lezyon Teması: Partnerdeki şankr veya kondiloma lata ile temas edilir.",
            "2. Mikrotravma: Sürtünmeyle mukozada mikroskobik çatlaklar oluşur.",
            "3. Spiroket Girişi: T. pallidum saniyeler içinde epitel aralıklarına dalar.",
            "4. İnokülasyon: Giriş yerinde çoğalarak inkübasyon evresine başlar."
        ]),
        make_recall("Sifilizin insandan insana bulaşmasında rol oynayan üç ana bulaş yolu nedir?", "Doğrudan cinsel temas (lezyon teması), transplasental (gebelikte fetüse) ve kan transfüzyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifiliz Bulaş Yolları", [
            {"text": "Şankr ve kondiloma lata ile cinsel temas en sık bulaş yoludur.", "isLie": False, "explanation": "Doğru. Majör bulaş şeklidir."},
            {"text": "Transplasental yolla anneden fetüse geçebilir.", "isLie": False, "explanation": "Doğru. Konjenital sifiliz yapar."},
            {"text": "Sifiliz sadece sivrisineklerin ısırmasıyla bulaşan bir parazit hastalığıdır.", "isLie": True, "explanation": "Tuzak! Sivrisinekle bulaşmaz; doğrudan temas, cinsel ilişki ve kanla bulaşır."},
            {"text": "Kan transfüzyonu ve perkutan yaralanmayla bulaşabilir.", "isLie": False, "explanation": "Doğru. Hematojen bulaş mümkündür."}
        ]),
        make_quiz("Sifilizin insandan insana bulaşmasında en sık karşılaşılan temel mekanizma nedir?", [
            {"key": "A", "text": "Aktif lezyonlara (şankr, kondiloma lata) doğrudan cinsel temas", "isCorrect": True, "explanation": "Cinsel temas en yaygın bulaş yoludur."},
            {"key": "B", "text": "Klorlu yüzme havuzlarında yüzmek", "isCorrect": False, "explanation": "Havuz suyuyla bulaşmaz."},
            {"key": "C", "text": "Evcil hayvanların tüylerini sevmek", "isCorrect": False, "explanation": "Zoonoz değildir, insana özgüdür."},
            {"key": "D", "text": "Konserve bezelye tüketmek", "isCorrect": False, "explanation": "Gıda kaynaklı değildir."}
        ])
    ]
    slides.append(make_slide(5, "Bulaş Yolları: Cinsel Temas, Transplasental ve Kan", "Şankr teması, kondiloma lata, transplasental geçiş, kan transfüzyonu ve mikrotravma", "Bulaş Dinamikleri", s5_narrative, s5_bullets, s5_elements))

    # Slide 6: Patogenez: Mukozal Giriş ve Endotel Tropizmi
    s6_narrative = (
        "Treponema pallidum'un patogenezindeki en çarpıcı hücresel özellik, kan damarlarına ve "
        "endotelyal hücrelere karşı gösterdiği yüksek afinite (**endotel tropizmi**) ve perivasküler yayılımdır.\n\n"
        "- **Mukozal Giriş:** Spiroket mukozal yüzeylerden veya bütünlüğü bozulmuş mikroskopik cilt çatlaklarından "
        "içeri girer ve inokülasyon yerindeki bağ dokusunda hızla çoğalmaya başlar.\n"
        "- **Endotelde Çoğalma:** Bakteri kapiller ve postkapiller venüllerin **damar endotellerinde çoğalır "
        "ve perivasküler alana yerleşir**; endotel hücre hasarı ve proliferasyonuna yol açar.\n"
        "- **Lenfohematojen Yayılım:** Giriş yerinde çoğalırken aynı zamanda lenfatik damarlar ve kan dolaşımı "
        "yoluyla daha ilk saatlerden itibaren tüm vücuda sessizce yayılmaya başlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Treponema pallidum damar endotellerinde çoğalır ve perivasküler hücrelere girer; bu endotelyal hasar sifilizin tüm histopatolojik lezyonlarının temelini oluşturur."
    )
    s6_bullets = [
        "Mukozal mikroçatlaklardan girip inokülasyon yerinde çoğalır.",
        "Damar endotellerinde çoğalır ve perivasküler alana yerleşir.",
        "Daha ilk günlerden itibaren kan ve lenfle sistemik yayılır."
    ]
    s6_elements = [
        make_cloze("Treponema pallidum dokularda damar endotellerinde çoğalarak perivasküler alana girer.", "damar endotellerinde", "Bakterinin çoğaldığı vasküler hücre katmanı"),
        make_table("Patogenezin Temel Basamakları", ["Aşama", "Hücresel Olay", "Patolojik Sonuç"], [
            {"cells": [{"text": "Mukozal Giriş", "isMasked": False}, {"text": "Mikroabrazyondan dokuya penetrasyon", "isMasked": True, "hint": "çatlaklardan sızma"}, {"text": "Lokal dokuda bakteriyel çoğalma"}]},
            {"cells": [{"text": "Endotel Tutulumu", "isMasked": False}, {"text": "Endotel içi çoğalma ve perivasküler yerleşim", "isMasked": False}, {"text": "Endarteritis obliterans ve iskemi", "isMasked": True, "hint": "damar lümen daralması patolojisi"}]}
        ]),
        make_chain("Hücresel Patogenez Yolu", [
            "1. Mukozal Giriş: Cinsel temasla spiroket epitel çatlağına sızar.",
            "2. Vasküler Tutunma: Bakteri endotel hücre reseptörlerine bağlanır.",
            "3. Endotelyal Proliferasyon: Endotel lümeninde çoğalarak perivasküler alana geçer.",
            "4. Erken Yayılım: Primer şankr henüz çıkmadan önce spiroketemi başlar."
        ]),
        make_recall("Treponema pallidum dokularda özellikle hangi hücresel yapılarda çoğalır ve yerleşir?", "Damar endotellerinde çoğalır ve perivasküler hücrelerin arasına yerleşir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifiliz Patogenezi", [
            {"text": "Bakteri mukozal yüzeyden veya çatlak ciltten girer.", "isLie": False, "explanation": "Doğru. Giriş kapısı mukozadır."},
            {"text": "Damar endotellerinde çoğalır ve perivasküler alana girer.", "isLie": False, "explanation": "Doğru. Endotel tropizmi karakteristiktir."},
            {"text": "Treponema pallidum sadece saç telinin en ucundaki cansız keratinde çoğalır.", "isLie": True, "explanation": "Tuzak! Damar endotellerinde ve canlı perivasküler dokuda çoğalır; saç ucuyla ilgisizdir."},
            {"text": "Kan ve lenf yoluyla tüm vücuda yayılabilir.", "isLie": False, "explanation": "Doğru. Sistemik dissemine olur."}
        ]),
        make_quiz("Treponema pallidum'un dokulardaki hücresel yerleşimi ve çoğalma odağı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Damar endotellerinde çoğalır ve perivasküler hücrelere girer", "isCorrect": True, "explanation": "T. pallidum damar endotellerinde çoğalır ve perivasküler dokuya yerleşir."},
            {"key": "B", "text": "Mide asidinin içinde serbest yüzer", "isCorrect": False, "explanation": "Mide asidine dayanamaz."},
            {"key": "C", "text": "Kemik iliğinde hemoglobin molekülü sentezler", "isCorrect": False, "explanation": "Bakteridir, hemoglobin yapmaz."},
            {"key": "D", "text": "Sadece gözyaşı bezinde lakrimal kanal döşer", "isCorrect": False, "explanation": "Gözyaşı bezi odağı değildir."}
        ])
    ]
    slides.append(make_slide(6, "Patogenez: Mukozal Giriş ve Endotel Tropizmi", "Mukozal penetrasyon, endotelyal çoğalma, perivasküler yerleşim ve lenfohematojen dissemine", "Hücresel Patogenez", s6_narrative, s6_bullets, s6_elements))

    # Slide 7: İnkübasyon Süresi (3-90 Gün, Ortalama 3 Hafta)
    s7_narrative = (
        "Sifilizin primer klinik bulgusu olan şankr ortaya çıkmadan önce, bakterinin sessizce çoğaldığı "
        "ve dokuyu hazırladığı belirli bir inkübasyon (kuluçka) periyodu yaşanır.\n\n"
        "- **İnkübasyon Süresi Genişliği:** Bakteri vücuda girdikten sonra ilk klinik lezyonun belirmesine "
        "kadar geçen süre **3 ila 90 gün arasında** çok geniş bir varyasyon gösterebilir.\n"
        "- **Ortalama Süre (Klasik Periyot):** Hastaların ezici çoğunluğunda inkübasyon süresi **ortalama "
        "yaklaşık 3 haftadır (21 gün)**.\n"
        "- **Belirleyici Faktörler:** İnkübasyon süresinin kısalığı veya uzunluğu, temas anında alınan "
        "bakteri miktarına (inokülüm dozu) ve konağın immünolojik savunma durumuna bağlıdır; yüksek dozda süre kısalır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Sifilizin inkübasyon süresi 3-90 gün arasındadır; olguların çoğunda ortalama genellikle 3 haftadır (yaklaşık 21 gün)."
    )
    s7_bullets = [
        "İnkübasyon süresi 3 ila 90 gün arasında değişir.",
        "Olguların çoğunda ortalama süre yaklaşık 3 haftadır (21 gün).",
        "İnokülüm dozu yüksekse inkübasyon süresi kısalır."
    ]
    s7_elements = [
        make_cloze("Sifiliz enfeksiyonunda ortalama inkübasyon süresi genellikle 3 hafta (21 gün) olarak bilinir.", "3 hafta", "Kuluçka süresinin ortalama süresi"),
        make_table("İnkübasyon Süresi Parametreleri", ["Parametre", "Zaman Aralığı", "Klinik Özellik"], [
            {"cells": [{"text": "Uç Sınırlar", "isMasked": False}, {"text": "3 ila 90 gün", "isMasked": True, "hint": "en kısa ve en uzun kuluçka aralığı"}, {"text": "Tanıda 3 aya kadar geçmiş sorgulanmalıdır"}]},
            {"cells": [{"text": "Ortalama Süre", "isMasked": False}, {"text": "Genellikle 3 hafta (21 gün)", "isMasked": False}, {"text": "Şankrın belirdiği en tipik zaman", "isMasked": True, "hint": "primer lezyonun klasik çıkış zamanı"}]}
        ]),
        make_chain("İnkübasyon Dönemi İlerlemesi", [
            "1. İnokülasyon: Cinsel temasla az sayıda spiroket dokuya girer.",
            "2. Sessiz Bölünme: Bakterinin ikiye katlanma süresi uzundur (yaklaşık 30 saat).",
            "3. 21. Gün Eşiği: 3 hafta sonunda bakteri sayısı kritik inflamatuvar eşiğe ulaşır.",
            "4. Şankr Patlaması: Giriş yerinde eritemli papül açılır ve ülsere dönüşür."
        ]),
        make_recall("Sifilizde bakteri vücuda girdikten sonra şankr çıkana kadar geçen inkübasyon süresi ne kadardır?", "İnkübasyon süresi 3-90 gündür; genellikle ortalama 3 haftadır (21 gün)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifiliz İnkübasyon Süresi", [
            {"text": "İnkübasyon süresi 3-90 gün arasındadır.", "isLie": False, "explanation": "Doğru. Literatür sınırları 3-90 gündür."},
            {"text": "Genellikle ortalama inkübasyon süresi 3 haftadır.", "isLie": False, "explanation": "Doğru. Tipik olarak 21 gündür."},
            {"text": "Sifiliz mikrobu temas ettiği andan 2 saniye sonra anında şankr oluşturur.", "isLie": True, "explanation": "Tuzak! Bakteri yavaş çoğalır; kuluçka süresi ortalama 3 haftadır."},
            {"text": "İnokülüm miktarı inkübasyon süresini etkileyebilir.", "isLie": False, "explanation": "Doğru. Yüksek dozda süre kısalır."}
        ]),
        make_quiz("Sifiliz enfeksiyonunda şankr lezyonunun ortaya çıkması için gereken ortalama inkübasyon süresi kaçtır?", [
            {"key": "A", "text": "Genellikle 3 hafta (3-90 gün aralığı)", "isCorrect": True, "explanation": "İnkübasyon 3-90 gün, ortalama 3 haftadır."},
            {"key": "B", "text": "Kesin olarak 40 yıl", "isCorrect": False, "explanation": "Bu kadar uzun inkübasyon olmaz."},
            {"key": "C", "text": "Sadece 1 milisaniye", "isCorrect": False, "explanation": "Bakteriyel çoğalma zaman alır."},
            {"key": "D", "text": "Doğumdan 100 yıl sonra", "isCorrect": False, "explanation": "Gerçek dışıdır."}
        ])
    ]
    slides.append(make_slide(7, "İnkübasyon Süresi (3-90 Gün, Ortalama 3 Hafta)", "Kuluçka aralığı (3-90 gün), ortalama 21 gün eşiği, yavaş bakteriyel bölünme ve lezyon hazırlığı", "İnkübasyon ve Kuluçka Dinamiği", s7_narrative, s7_bullets, s7_elements))

    # Slide 8: Sifilizin Dönemleri ve Klinik Sınıflama
    s8_narrative = (
        "Treponema pallidum enfeksiyonu, tedavi edilmediği takdirde hastanın yaşamı boyunca yıllara yayılan "
        "ve birbirini takip eden dört ana klinik evre sergiler.\n\n"
        "- **1. Primer Sifiliz:** Giriş yerinde gelişen ağrısız sert ülser (**şankr**) ve bölgesel lenfadenopati ile karakterizedir.\n"
        "- **2. Sekonder Sifiliz:** Spiroketemiye bağlı olarak ortaya çıkan yaygın cilt-mukoza döküntüleri, "
        "**kondiloma lata**, sistemik lenfadenopati ve organ tutulumları evresidir.\n"
        "- **3. Latent Sifiliz:** Sekonder bulguların kaybolduğu, hastanın tamamen asemptomatik olduğu, "
        "ancak serolojik testlerin pozitifliğini koruduğu sessiz bekleme dönemidir (erken ve geç latent).\n"
        "- **4. Tersiyer Sifiliz:** Yıllar sonra gelişen; gomlar, kardiyovasküler sifiliz ve nörosifiliz ile "
        "seyreden destrüktif evredir.\n\n"
        "> [!NOTE]\n"
        "> Sifilizin dört ana dönemi: Primer (şankr), Sekonder (döküntü/kondilom), Latent (asemptomatik seropozitif) ve Tersiyer (gom/nörosifiliz) evrelerdir."
    )
    s8_bullets = [
        "Sifiliz primer, sekonder, latent ve tersiyer olmak üzere dört evrelidir.",
        "Primer evrede şankr, sekonderde yaygın döküntü izlenir.",
        "Latent evre asemptomatiktir; tersiyer evre destrüktif lezyonlar yapar."
    ]
    s8_elements = [
        make_cloze("Sifilizin klinik evreleri primer, sekonder, latent ve tersiyer dönemler olarak sınıflanır.", "tersiyer", "Yıllar sonra ortaya çıkan destrüktif son dönem adı"),
        make_table("Sifilizin Dört Klinik Dönemi", ["Dönem", "Kardinal Özellik", "Bulaştırıcılık Durumu"], [
            {"cells": [{"text": "Primer Sifiliz", "isMasked": False}, {"text": "Ağrısız şankr ve bölgesel LAP", "isMasked": True, "hint": "tek ağrısız sert ülser"}, {"text": "Yüksek oranda bulaştırıcı"}]},
            {"cells": [{"text": "Sekonder Sifiliz", "isMasked": False}, {"text": "Yaygın döküntü ve kondiloma lata", "isMasked": False}, {"text": "Çok yüksek oranda bulaştırıcı", "isMasked": True, "hint": "en aktif lezyonel bulaşma"}]},
            {"cells": [{"text": "Tersiyer Sifiliz", "isMasked": False}, {"text": "Gom, aortit, nörosifiliz", "isMasked": False}, {"text": "Bulaştırıcı DEĞİLDİR", "isMasked": True, "hint": "bulaştırıcılığın kaybolduğu dönem"}]}
        ]),
        make_chain("Sifilizin Doğal Evreleme Yolu", [
            "1. Primer Faz: 3. haftada genital şankr belirir.",
            "2. Sekonder Faz: 2-8 hafta sonra kanla yayılarak simetrik döküntüler yapar.",
            "3. Latent Faz: Semptomlar söner, hasta yıllarca sessiz seropozitif kalır.",
            "4. Tersiyer Faz: Yıllar sonra gom ve nörovasküler yıkımla son aşamaya girilir."
        ]),
        make_recall("Tedavi edilmeyen sifilizin yaşam boyu sergilediği dört ana klinik dönem sırasıyla nelerdir?", "Primer sifiliz, sekonder sifiliz, latent sifiliz ve tersiyer sifilizdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilizin Dönemleri", [
            {"text": "Sifiliz primer, sekonder, latent ve tersiyer dönemlere ayrılır.", "isLie": False, "explanation": "Doğru. Dört ana evredir."},
            {"text": "Primer dönemde şankr, sekonderde cilt döküntüleri izlenir.", "isLie": False, "explanation": "Doğru. Evrelerin tipik bulgularıdır."},
            {"text": "Tersiyer dönem sifiliz hastanın derhal kuşa dönüşüp gökyüzüne uçmasıdır.", "isLie": True, "explanation": "Tuzak! Tersiyer dönem gom, kardiyovasküler sifiliz ve nörosifiliz gibi ağır organ yıkımlarıdır."},
            {"text": "Latent dönem hastanın asemptomatik olduğu dönemdir.", "isLie": False, "explanation": "Doğru. Klinik sessizlik evresidir."}
        ]),
        make_quiz("Sifilizin klinik evreleri ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Primer sifiliz - Şankr (ağrısız ülser)", "isCorrect": True, "explanation": "Primer sifilizin kardinal lezyonu şankrdır."},
            {"key": "B", "text": "Sekonder sifiliz - Hiçbir döküntünün olmadığı saf kemik kırığı", "isCorrect": False, "explanation": "Sekonderde yaygın döküntü olur."},
            {"key": "C", "text": "Tersiyer sifiliz - Sadece 2 saat süren hafif burun akıntısı", "isCorrect": False, "explanation": "Yıkıcı kronik dönemdir."},
            {"key": "D", "text": "Latent sifiliz - Her gün 40 derece ateşle seyreden fırtına", "isCorrect": False, "explanation": "Latent dönem asemptomatiktir."}
        ])
    ]
    slides.append(make_slide(8, "Sifilizin Dönemleri ve Klinik Sınıflama", "Dört ana evre: Primer (şankr), Sekonder (döküntü), Latent (sessiz), Tersiyer (gom/nörosifiliz)", "Klinik Evreleme", s8_narrative, s8_bullets, s8_elements))

    # Slide 9: Spiroketemi ve Erken Organ İstilası
    s9_narrative = (
        "Sifiliz, primer lezyonun (şankr) ortaya çıktığı ilk evrede dahi yalnızca lokal bir genital "
        "hastalık olarak kalmaz; son derece erken bir **spiroketemi** geliştirir.\n\n"
        "- **Erken Hematojen Giriş:** Spiroketler mikrotravma yerindeki lenfatik kanallara ve endotel "
        "aralıklarına girerek **daha şankr tam olarak belirginleşmeden kan dolaşımına sızar**.\n"
        "- **Organ İstilası Kaynağı:** Bu erken spiroketemi, bakterinin santral sinir sistemi, karaciğer, "
        "kemikler ve göz gibi derin dokulara daha ilk haftalardan itibaren tohumlanmasına yol açar.\n"
        "- **Biyolojik Sonuç:** Primer sifiliz lokalize bir yara gibi görünse de sistemik bir enfeksiyondur; "
        "bu nedenle lokal kremlerle değil, daima sistemik penisilinle tedavi edilmek zorundadır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Primer dönemdeki spiroketemi, erken dönemden itibaren santral sinir sistemi dahil tüm organ invazyonları için temel biyolojik kaynak oluşturur."
    )
    s9_bullets = [
        "Spiroketler daha primer dönemde kana geçerek spiroketemi yapar.",
        "Spiroketemi organ invazyonu için temel biyolojik kaynaktır.",
        "Lokal gibi görünen primer şankr aslında sistemik bir hastalıktır."
    ]
    s9_elements = [
        make_cloze("Primer dönemde bakterilerin kana karışarak organlara tohumlanmasına spiroketemi adı verilir.", "spiroketemi", "Kanda canlı spiroketlerin dolaşması durumu"),
        make_table("Spiroketemi ve Erken Yayılım Dinamikleri", ["Basamak", "Biyolojik Mekanizma", "Klinik / Patolojik Sonuç"], [
            {"cells": [{"text": "Vasküler Sızıntı", "isMasked": False}, {"text": "Endotel aralıklarından kapillere geçiş", "isMasked": True, "hint": "damar içine bakteriyel geçiş"}, {"text": "Dolaşımda canlı Treponema varlığı"}]},
            {"cells": [{"text": "Sistemik Tohumlanma", "isMasked": False}, {"text": "BOS ve iç organlara erken yerleşim", "isMasked": False}, {"text": "Sekonder ve nörolojik lezyonların tohumu", "isMasked": True, "hint": "gelecekteki komplikasyon temeli"}]}
        ]),
        make_chain("Spiroketemi Yayılım Yolu", [
            "1. İnokülasyon: Genital mukozaya giren bakteri çoğalır.",
            "2. Kapiller İntrüzyon: İnce spiroketler vasküler lümene geçer.",
            "3. Kan Yoluyla Dolaşım: Canlı spiroketler arteriyel kanla tüm organlara dağılır.",
            "4. Sistemik Zemin: Primer şankr iyileşse bile vücut tamamen enfekte kalır."
        ]),
        make_recall("Primer sifiliz döneminde bakterinin kana karışmasını ifade eden ve organ invazyonuna zemin hazırlayan duruma ne ad verilir?", "Spiroketemi adı verilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Spiroketemi ve Yayılım", [
            {"text": "Primer dönemde spiroketemi gelişebilir.", "isLie": False, "explanation": "Doğru. Bakteri kana karışır."},
            {"text": "Spiroketemi organ invazyonu için kaynak oluşturur.", "isLie": False, "explanation": "Doğru. Tüm vücuda tohumlanır."},
            {"text": "Spiroketemi sadece saç tellerinin elektriğe çarpılmasıyla oluşan bir fiziksel olaydır.", "isLie": True, "explanation": "Tuzak! Spiroketemi Treponema bakterilerinin kan dolaşımında yayılmasıdır; saç elektriğiyle ilgisi yoktur."},
            {"text": "Sifiliz lezyon lokal olsa da sistemik bir enfeksiyondur.", "isLie": False, "explanation": "Doğru. Erken sistemik yayılım gösterir."}
        ]),
        make_quiz("Primer sifilizde görülen spiroketeminin klinik ve patofizyolojik önemi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Erken dönemden itibaren organ invazyonu ve dissemine hastalık için kaynak olması", "isCorrect": True, "explanation": "Spiroketemi tüm organlara bakterinin yayılmasını sağlar."},
            {"key": "B", "text": "Hastanın göz rengini maviye dönüştürmesi", "isCorrect": False, "explanation": "Göz rengiyle ilgisizdir."},
            {"key": "C", "text": "Sadece tırnak uzamasını hızlandırması", "isCorrect": False, "explanation": "Tırnakla ilgisi yoktur."},
            {"key": "D", "text": "Hastalığı anında tamamen yok etmesi", "isCorrect": False, "explanation": "Tam tersine yayılmasına yol açar."}
        ])
    ]
    slides.append(make_slide(9, "Spiroketemi ve Erken Organ İstilası", "Lenfohematojen dissemine, kan yoluyla tohumlanma, erken BOS geçişi ve sistemik enfeksiyon", "Sistemik Patofizyoloji", s9_narrative, s9_bullets, s9_elements))

    # Slide 10: [TEKRAR SAYFASI - CHECKPOINT 1] Spiroket Biyolojisi, Türler ve Patogenez
    s10_narrative = (
        "Bu tekrar sayfasında Bölüm 1 boyunca işlediğimiz Treponema biyolojisini, taksonomik tür ayrımlarını "
        "ve sifiliz patogenezinin ilk adımlarını konsolide ediyoruz.\n\n"
        "- **Morfoloji ve Hareket:** İnce spiral bakterilerdir; Gram negatif benzeri duvarı olmasına rağmen "
        "narinliği nedeniyle **Gram ile boyanmaz, karanlık saha ile izlenir**. Periplazmik aralıktaki "
        "aksiyel flajellaları bakteriye **burgu (tirbüşon) hareketi** kazandırır.\n"
        "- **Treponema Türleri:** Sifiliz etkeni *T. pallidum subsp. pallidum*dur. Yaws ve bejel cilt ve kemik "
        "tutulumu yaparken; **Pintada (T. carateum) kemik tutulumu kesinlikle yoktur**.\n"
        "- **Bulaş ve Patogenez:** Şankr ve kondiloma lataya temasla bulaşır. Bakteri **damar endotellerinde "
        "çoğalır ve perivasküler alana girer**. İnkübasyon süresi 3-90 gün (ortalama **3 hafta**) olup "
        "daha bu evrede **spiroketemi** ile sistemik yayılım başlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 1 SENTEZİ] Treponema karanlık sahada burgu hareketiyle tanınır; pintada kemik tutulmaz; bakteri damar endotellerinde çoğalır; kuluçka süresi ortalama 3 haftadır."
    )
    s10_bullets = [
        "Gram ile boyanmaz, karanlık sahada burgu hareketi ile görülür.",
        "Pintada (T. carateum) cilt tutulur fakat kemik tutulumu yoktur.",
        "Damar endotellerinde çoğalır; inkübasyon süresi ortalama 3 haftadır."
    ]
    s10_elements = [
        make_cloze("Bölüm 1 sentezinde incelenen Treponema türleri arasında kemik tutulumu yapmayan etken Treponema carateum olarak pekiştirilmiştir.", "Treponema carateum", "Kemik tutulumu yapmayan Pinta etkeni"),
        make_table("Bölüm 1 Temel Kazanımları Sentez Tablosu", ["Konsept", "Kritik Bilimsel Kural", "Sınav Spotu Notu"], [
            {"cells": [{"text": "Boyanma ve Hareket", "isMasked": False}, {"text": "Gram ile boyanmaz; periplazmik burgu hareketi", "isMasked": True, "hint": "özel mikroskopi ve aksiyel kamçı"}, {"text": "Karanlık saha ile teşhis"}]},
            {"cells": [{"text": "Pinta Karakteri", "isMasked": False}, {"text": "Yalnız cilt tutulur, KEMİK TUTULMAZ", "isMasked": False}, {"text": "Yaws ve bejelden en kritik ayrım", "isMasked": True, "hint": "kemik lezyonu bulunmama özelliği"}]},
            {"cells": [{"text": "Hücresel Tropizm", "isMasked": False}, {"text": "Damar endotellerinde çoğalma", "isMasked": True, "hint": "vasküler hücre içi replikasyon"}, {"text": "Perivasküler infiltrasyon ve erken spiroketemi"}]}
        ]),
        make_chain("Bölüm 1 Süreç Bütünleştirmesi", [
            "1. Spiroket Yapısı: İnce helikal gövde periplazmik flajellalarla donatılmıştır.",
            "2. Burgu Penetrasyonu: Tirbüşon dönüşüyle mukozayı aşar.",
            "3. Endotel Tropizmi: Damar endotellerinde çoğalarak perivasküler alana yerleşir.",
            "4. 3 Haftalık Kuluçka: 21 günlük sessiz inkübasyon sonrası primer evreye adım atılır."
        ]),
        make_recall("Bölüm 1'de öğrendiğimiz: (1) Karanlık sahada görülen hareket türü, (2) Kemik tutulumu yapmayan tür ve (3) Ortalama kuluçka süresi nedir?", "(1) Burgu (tirbüşon) hareketi, (2) Treponema carateum (pinta), (3) Ortalama 3 haftadır (21 gün)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 1 Checkpoint Sentezi", [
            {"text": "Treponema pallidum Gram boyası ile boyanmaz, karanlık sahada görülür.", "isLie": False, "explanation": "Doğru. Tipik mikrobiyolojik kuraldır."},
            {"text": "Pintada (T. carateum) kemik tutulumu yoktur.", "isLie": False, "explanation": "Doğru. Sadece cilt tutulur."},
            {"text": "Treponema pallidum dokuda çoğalmak yerine sadece cam bardakların üzerinde çoğalır.", "isLie": True, "explanation": "Tuzak! Bakteri damar endotellerinde ve canlı perivasküler dokuda çoğalır; camda üremez."},
            {"text": "İnkübasyon süresi ortalama 3 haftadır.", "isLie": False, "explanation": "Doğru. Klasik kuluçka periyodudur."}
        ]),
        make_quiz("Bölüm 1'de ele alınan mikrobiyolojik ve patogenetik özelliklere göre aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Treponema pallidum damar endotellerinde çoğalır ve ortalama 3 haftada lezyon oluşturur", "isCorrect": True, "explanation": "Endotel tropizmi ve 3 haftalık kuluçka kardinal bulgudur."},
            {"key": "B", "text": "Pinta hastalığı vücuttaki tüm kemikleri eriten en ağır kemik hastalığıdır", "isCorrect": False, "explanation": "Pintada kemik tutulumu YOKTUR."},
            {"key": "C", "text": "Spiroketler standart Gram boyasıyla masmavi boyanan koklardır", "isCorrect": False, "explanation": "Gram boyası tutmaz ve spiraldir."},
            {"key": "D", "text": "Sifilizin inkübasyon süresi kesinlikle 10 saniyedir", "isCorrect": False, "explanation": "3-90 gün, ortalama 3 haftadır."}
        ])
    ]
    slides.append(make_slide(10, "[TEKRAR SAYFASI - CHECKPOINT 1] Spiroket Biyolojisi, Türler ve Patogenez", "Bölüm 1 kapsamlı tekrarı: spiroket yapısı, burgu hareketi, taksonomi ve endotel tropizmi", "Bölüm Tekrarı ve Konsolidasyon", s10_narrative, s10_bullets, s10_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec1()
    print(f"Sec1 generated: {len(slides)} slides (Slide 1 to 10)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
