# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec7():
    slides = []

    # Slide 61: Tanısal Yaklaşım: Anamnez ve Semptom Analizi
    s61_narrative = (
        "Üriner sistem enfeksiyonu şüphesiyle başvuran bir hastada tanı süreci, dikkatli ve kapsamlı "
        "bir anamnez ile başlar; semptomların anatomik lokalizasyonu ilk ipucunu verir.\n\n"
        "- **Mevcut Şikayetler:** Dizüri (idrarda yanma), pollaküri (sık idrara çıkma), sıkışma hissi "
        "(urgency), suprapubik ağrı, hematüri ve sistemik bulgu olarak ateş, titreme ve bel/böğür ağrısı sorgulanır.\n"
        "- **Özgeçmiş Sorgusu:** Daha önce geçirilmiş ÜSE atakları, üriner sistemde taş öyküsü, VUR, "
        "kanser veya diyabet gibi **komplike edici faktörler** ayrıntılandırılır.\n"
        "- **Soygeçmiş Sorgusu:** Anne ve kız kardeşlerde tekrarlayan ÜSE öyküsü veya ebeveynlerde "
        "konjenital vezikoüreteral reflü (VUR) varlığı ailesel yatkınlığı ortaya koyar.\n\n"
        "> [!NOTE]\n"
        "> Anamnezde alt üriner semptomlara (dizüri, pollaküri) ek olarak ateş ve böğür ağrısı tariflenmesi üst üriner sistem invazyonunun primer göstergesidir."
    )
    s61_bullets = [
        "Dizüri, pollaküri, hematüri ve ateş temel sorgulama semptomlarıdır.",
        "Özgeçmişte geçirilmiş ÜSE, taş, VUR ve kanser gibi faktörler aranır.",
        "Soygeçmişte anne ve kardeşlerde rekürren ÜSE ve VUR sorgulanmalıdır."
    ]
    s61_elements = [
        make_cloze("ÜSE anamnezinde hastanın özgeçmişinde geçirilmiş ÜSE, taş, VUR ve kanser varlığı komplike durumları belirler.", "komplike", "Ek risk ve anatomik bozukluk içeren durumlar"),
        make_table("Anamnezde Kritik Sorgulama Katmanları", ["Katman", "Sorgulanan Unsurlar", "Klinik Yansıması"], [
            {"cells": [{"text": "Mevcut Semptomlar", "isMasked": False}, {"text": "Dizüri, pollaküri, hematüri, ateş", "isMasked": True, "hint": "güncel işeme ve sıcaklık şikayetleri"}, {"text": "Sistit vs pyelonefrit klinik ayrımı"}]},
            {"cells": [{"text": "Özgeçmiş", "isMasked": False}, {"text": "Taş, VUR, geçirilmiş ÜSE, DM, kanser", "isMasked": False}, {"text": "Komplike edici faktörlerin tespiti", "isMasked": True, "hint": "tedaviyi güçleştiren altyapı"}]},
            {"cells": [{"text": "Soygeçmiş", "isMasked": False}, {"text": "Anne-kardeşte ÜSE, anne-babada VUR", "isMasked": False}, {"text": "Genetik ve ailesel anatomik yatkınlık", "isMasked": False}]}
        ]),
        make_chain("Anamnezden Klinik Ön Tanıya Akış", [
            "1. Semptom Tespiti: Dizüri ve pollaküri saptanır (alt üriner sistem).",
            "2. Sistemik Kontrol: Ateş ve böğür ağrısı varlığı araştırılır (üst sistem tutulumu).",
            "3. Özgeçmiş Taraması: Taş, kateter veya diyabet varlığı kontrol edilir (komplike zemin).",
            "4. Yol Haritası: Basit sistit veya komplike pyelonefrit ön tanısı ile tetkik seçilir."
        ]),
        make_recall("ÜSE anamnezinde hastanın özgeçmişinde sorgulanması gereken başlıca komplike edici durumlar nelerdir?", "Geçirilmiş ÜSE öyküsü, nefrolitiazis (taş), vezikoüreteral reflü (VUR), kanser ve diyabettir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Anamnez Sorgusu", [
            {"text": "Anamnezde dizüri, pollaküri, hematüri ve ateş mutlaka sorgulanır.", "isLie": False, "explanation": "Doğru. Temel şikayetlerdir."},
            {"text": "Özgeçmişte geçirilmiş ÜSE, taş ve VUR varlığı araştırılır.", "isLie": False, "explanation": "Doğru. Komplike faktörlerdir."},
            {"text": "Soygeçmişte anne ve kız kardeşlerde ÜSE olması tamamen önemsizdir ve dosyaya yazılmaz.", "isLie": True, "explanation": "Tuzak! Soygeçmişte anne ve kardeşlerde ÜSE veya ebeveynde VUR olması genetik yatkınlığı gösteren önemli bir veridir."},
            {"text": "Hematüri varlığı mesane mukozasındaki vasküler hasarı düşündürür.", "isLie": False, "explanation": "Doğru. Sık eşlik eder."}
        ]),
        make_quiz("ÜSE şüpheli bir hastada anamnez alınırken özgeçmiş ve soygeçmişte sorgulanması gereken parametrelerle ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Özgeçmişte taş, VUR ve geçirilmiş ÜSE; soygeçmişte anne-kardeşlerde ÜSE ve VUR sorgulanmalıdır", "isCorrect": True, "explanation": "Ders notunda anamnez başlığı altında bu parametreler eksiksiz olarak vurgulanmıştır."},
            {"key": "B", "text": "Hastanın sadece göz rengi sorgulanır, idrar şikayetleri dinlenmez", "isCorrect": False, "explanation": "Tıbbi anamnez dışıdır."},
            {"key": "C", "text": "Taş öyküsü ÜSE ile hiçbir ilişkisi olmayan bir durumdur", "isCorrect": False, "explanation": "Taş majör risk faktörüdür."},
            {"key": "D", "text": "Diyabet varlığı anamnezde asla sorulmamalıdır", "isCorrect": False, "explanation": "DM kritik sistemik faktördür."}
        ])
    ]
    slides.append(make_slide(61, "Tanısal Yaklaşım: Anamnez ve Semptom Analizi", "Dizüri, pollaküri, ateş sorgusu; özgeçmişte taş, VUR, kanser ve soygeçmiş dinamikleri", "Tanı Yöntemleri", s61_narrative, s61_bullets, s61_elements))

    # Slide 62: Fizik Muayene Bulguları ve Çocukluk Çağında Cinsiyet Oranı
    s62_narrative = (
        "ÜSE şüphesinde fizik muayene, enfeksiyonun anatomik seviyesini (alt vs üst sistem) ve altta "
        "yatan genital anomalileri objektif olarak belirler.\n\n"
        "- **Kardinal Muayene Bulguları:** Suprapubik bölgede palpasyonla hassasiyet (sistit bulgusu) "
        "ve renal lojlarda perküsyonla **kostavertebral açı hassasiyeti (KVAH)** (pyelonefrit bulgusu) aranır.\n"
        "- **Genital ve Perineal Muayene:** Erkeklerde sünnet durumu ve eksternal meatus darlıkları; kızlarda "
        "vajinit bulguları; enkoprezis/konstipasyonu olan çocuklarda ise perineal duyu ve alt ekstremite "
        "refleksleri nörojenik mesane açısından incelenmelidir.\n"
        "- **Çocukluk Çağı Cinsiyet Oranı:** Çocuklarda genel sıklık erkeklerde %1'dir; ilk 3 ayda E>K "
        "iken, ilk 3 aydan sonra kızlarda belirgin artışla **Erkek/Kadın oranı 1/10 seviyesine geriler**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İlk 3 aydan sonra çocuklarda ÜSE kız çocuklarında belirgin artar ve Erkek / Kadın oranı 1/10 olur."
    )
    s62_bullets = [
        "Suprapubik hassasiyet sistiti, KVAH pyelonefriti gösterir.",
        "Sünnet, meatus darlığı, vajinit ve perineal refleksler muayene edilir.",
        "İlk 3 aydan sonra çocuklarda ÜSE kızlarda sıklaşır ve E/K oranı 1/10 olur."
    ]
    s62_elements = [
        make_cloze("Çocuklarda ilk 3 aydan sonra kız çocuklarında artışla Erkek / Kadın oranı 1/10 düzeyine ulaşır.", "1/10", "Çocukluk çağında kız baskınlığını gösteren bire on oranı"),
        make_table("Fizik Muayene ve Pediatrik Cinsiyet Oranı", ["İnceleme Alanı", "Saptanan Patolojik Bulgu", "Klinik Karşılığı"], [
            {"cells": [{"text": "Böbrek Lojları Perküsyonu", "isMasked": False}, {"text": "Kostavertebral açı hassasiyeti (KVAH)", "isMasked": True, "hint": "böğür perküsyonunda şiddetli ağrı"}, {"text": "Akut pyelonefrit varlığı"}]},
            {"cells": [{"text": "Pediatrik Cinsiyet (>3 ay)", "isMasked": False}, {"text": "Erkek / Kadın oranı: 1 / 10", "isMasked": True, "hint": "kız çocuklarında 10 kat sıklık"}, {"text": "Kızlarda kısa üretra ve tuvalet eğitimi yatkınlığı"}]},
            {"cells": [{"text": "Perine ve Refleksler", "isMasked": False}, {"text": "Perineal duyu ve refleks kaybı", "isMasked": False}, {"text": "Nörojenik mesane ve spinal anomali şüphesi", "isMasked": False}]}
        ]),
        make_chain("Çocukluk Çağı Cinsiyet Değişim Zinciri", [
            "1. İlk 3 Ay: Konjenital ürolojik malformasyonlar erkeklerde fazladır (E > K).",
            "2. 3. Aydan Sonra: Erkeklerde anatomik anomaliler elenir ve sünnet koruması başlar.",
            "3. Kız Anatomisi: Kız çocuklarında kısa üretra ve perineal temas öne çıkar.",
            "4. 1/10 Oranı: 3 aydan sonra kız çocukları 10 kat baskın hale gelir (E/K: 1/10)."
        ]),
        make_recall("Çocukluk çağında ilk 3 aydan sonra ÜSE görülen çocuklarda Erkek / Kadın oranı kaçtır?", "Erkek / Kadın oranı 1 / 10'dur (kız çocuklarında 10 kat daha sıktır)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fizik Muayene ve Pediatri", [
            {"text": "Suprapubik hassasiyet sistiti, kostavertebral açı hassasiyeti pyelonefriti düşündürür.", "isLie": False, "explanation": "Doğru. Temel fizik bulgulardır."},
            {"text": "İlk 3 aydan sonra çocuklarda ÜSE kızlarda sık olup E/K oranı 1/10'dur.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "İlk 3 aydan sonra erkek çocuklarda ÜSE kızlardan 100 kat daha fazladır.", "isLie": True, "explanation": "Tuzak! İlk 3 aydan sonra kız çocuklarında çok daha sıktır (E/K oranı 1/10'dur)."},
            {"text": "Konstipasyonu olan çocuklarda perineal duyu ve refleksler incelenmelidir.", "isLie": False, "explanation": "Doğru. Nörolojik mesane dışlanmalıdır."}
        ]),
        make_quiz("Çocukluk çağında ilk 3 aydan sonra görülen üriner sistem enfeksiyonlarında Erkek / Kadın oranı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "1 / 10 (kız çocuklarında belirgin sık)", "isCorrect": True, "explanation": "Ders notunda 'ilk 3 aydan sonra kızlarda sık olup E/K: 1/10'dur' ifadesi yer almaktadır."},
            {"key": "B", "text": "10 / 1 (erkek çocuklarında belirgin sık)", "isCorrect": False, "explanation": "Tam tersidir."},
            {"key": "C", "text": "1 / 1 (tamamen eşit)", "isCorrect": False, "explanation": "Oran 1/10'dur."},
            {"key": "D", "text": "Sadece erkeklerde görülür, kızlarda sıfırdır", "isCorrect": False, "explanation": "Kızlarda 10 kat sıktır."}
        ])
    ]
    slides.append(make_slide(62, "Fizik Muayene Bulguları ve Çocukluk Çağında Cinsiyet Oranı", "Suprapubik hassasiyet, KVAH, genital muayene ve çocukluk çağı E/K: 1/10 oranı", "Tanı Yöntemleri", s62_narrative, s62_bullets, s62_elements))

    # Slide 63: İdrar Örneği Alma Yöntemleri: Temiz Orta Akım İdrarı
    s63_narrative = (
        "İdrar analizinin ve mikrobiyolojik kültürün güvenilirliği, örneğin perineal ve üretral "
        "kommensal florayla kontamine edilmeden doğru teknikle toplanmasına bağlıdır.\n\n"
        "- **Temiz Orta Akım İdrarı (MSU):** Mesane kontrolü olan yetişkinlerde ve büyük çocuklarda "
        "kullanılan en yaygın ve standart yöntemdir.\n"
        "- **Sabah İlk İdrar İlkesi:** İdrar kültürü ve analizi için **en uygun örnek sabah ilk idrardır**; "
        "gece boyunca mesanede bekleyen idrarda bakteri sayısı yüksek konsantrasyona ulaşır (fazla sıvı alımı ise idrarı sulandırarak bakteri sayısını azaltır).\n"
        "- **Hijyenik Hazırlık:** Sünnetsiz erkeklerde prepisyum geri çekilip sabunla temizlenmeli; "
        "kadınlarda labialar ayrılarak perine önden arkaya temizlenmeli; ilk gelen 10-15 ml idrar "
        "üretrayı yıkaması için tuvalete döküldükten sonra orta akım kaba alınmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> İdrar örneği için en uygun örnek mesanede uzun süre beklemiş olan sabah ilk idrardır; aşırı sıvı alımı bakteri sayısını seyreltir."
    )
    s63_bullets = [
        "Temiz orta akım idrarı rutin pratikte standart toplama yöntemidir.",
        "En uygun örnek bakteri konsantrasyonu en yüksek olan sabah ilk idrardır.",
        "Prepisyum veya labialar temizlenmeli, ilk akım dışarı atılıp orta akım alınmalıdır."
    ]
    s63_elements = [
        make_cloze("İdrar kültürü ve analizinde bakteri sayısının en yüksek konsantrasyonda olduğu en uygun örnek sabah ilk idrar örneğidir.", "sabah ilk idrar", "Gece mesanede beklemiş konsantre idrar"),
        make_table("Temiz Orta Akım Alma Protokolü", ["Adım", "Uygulama Kuralı", "Hatanın Doğuracağı Sonuç"], [
            {"cells": [{"text": "Zamanlama", "isMasked": False}, {"text": "Sabah ilk idrar (en uygun)", "isMasked": True, "hint": "gece boyu beklemiş idrar"}, {"text": "Gün içi aşırı sıvıyla bakterinin seyreltilmesi"}]},
            {"cells": [{"text": "Perineal Temizlik", "isMasked": False}, {"text": "Labialar açık, prepisyum geride sabunla temizlik", "isMasked": False}, {"text": "Deri florası kontaminasyonu (yalancı pozitif)", "isMasked": True, "hint": "cilt bakterilerinin kaba dökülmesi"}]},
            {"cells": [{"text": "Fraksiyon Ayrımı", "isMasked": False}, {"text": "İlk kısım tuvalete, orta akım steril kaba", "isMasked": True, "hint": "üretra yıkayıcı ilk idrarın atılması"}, {"text": "Distal üretradaki kommensallerin elenmesi"}]}
        ]),
        make_chain("Doğru Orta Akım İdrar Alma Zinciri", [
            "1. Hazırlık: Hasta ellerini ve genital bölgesini yıkayıp kurular.",
            "2. İlk Akım: İdrarın ilk 10-20 mililitresi üretradaki mikropları süpürmek için tuvalete yapılır.",
            "3. Orta Akım: İdrar yapma durdurulmadan steril kaba 20-50 ml örnek alınır.",
            "4. Son Akım: Kalan idrar tuvalete tamamlanır ve kap derhal kapatılır."
        ]),
        make_recall("İdrar kültürü ve tetkiki için günün hangi idrar örneği en uygundur ve neden?", "Sabah ilk idrardır; çünkü gece boyunca mesanede beklediği için bakteri sayısı ve konsantrasyonu en yüksek düzeydedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Orta Akım İdrarı", [
            {"text": "Temiz orta akım idrarı için en uygun örnek sabah ilk idrardır.", "isLie": False, "explanation": "Doğru. Konsantrasyonu en yüksektir."},
            {"text": "Aşırı sıvı alımı idrardaki bakteri sayısını azaltarak seyreltebilir.", "isLie": False, "explanation": "Doğru. Dilüsyon yapar."},
            {"text": "İdrar kabı doldurulurken tuvaletteki kirli suyla kaba ekleme yapılması idealdir.", "isLie": True, "explanation": "Tuzak! İdrar kabı tamamen steril olmalı, hiçbir dış sıvı veya klozet suyu karışmamalıdır."},
            {"text": "Sünnetsiz erkeklerde prepisyum geri çekilerek temizlik yapılmalıdır.", "isLie": False, "explanation": "Doğru. Smegma kontaminasyonunu önler."}
        ]),
        make_quiz("İdrar analizi ve kültürü için en uygun idrar örneği zamanlaması aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Sabah ilk idrar örneği", "isCorrect": True, "explanation": "Ders notunda 'en uygun sabah ilk idrar; sabah bakteri sayısı yüksek, fazla sıvı bakteri sayısını düşürür' kuralı yer almaktadır."},
            {"key": "B", "text": "5 litre su içtikten 10 dakika sonraki aşırı sulu idrar", "isCorrect": False, "explanation": "Bakteriyi aşırı seyreltir."},
            {"key": "C", "text": "Ağır egzersiz ve terleme sonrası çıkan son 1 damla", "isCorrect": False, "explanation": "Yetersiz volümdür."},
            {"key": "D", "text": "Gece yarısı uykudan uyandırılıp zorla alınan örnek", "isCorrect": False, "explanation": "Sabah ilk idrar esastır."}
        ])
    ]
    slides.append(make_slide(63, "İdrar Örneği Alma Yöntemleri: Temiz Orta Akım İdrarı", "Temiz orta akım idrarı tekniği, sabah ilk idrar avantajı ve genital hazırlık", "Tanı Yöntemleri", s63_narrative, s63_bullets, s63_elements))

    # Slide 64: Suprapubik Aspirasyon: Kontaminasyonsuz Altın Standart
    s64_narrative = (
        "Üretral yolun tamamen bypass edildiği suprapubik mesane aspirasyonu, kontaminasyon ihtimalini "
        "sıfıra indiren tanısal referans yöntemidir.\n\n"
        "- **Altın Standart Niteliği:** İdrar kültürü için **kontaminasyonsuz kesin altın standart** "
        "suprapubik mesane aspirasyonudur.\n"
        "- **Tanısal Eşik Değeri:** Doğrudan mesane kubbesinden iğneyle steril idrar çekildiği için, "
        "orta akımdaki 100.000 kuralı burada geçerli değildir; **tek bir mikroorganizmanın (herhangi bir sayıda Gram negatif basil) üremesi dahi kesinlikle tanısal önem taşır**.\n"
        "- **Uygulama Alanı ve Kısıtlılık:** İnvaziv bir girişim olduğundan **rutinde kullanılmaz**; USG "
        "eşliğinde, orta akım idrar alınamayan şüpheli bebeklerde veya tanı konamayan özel hastalarda uygulanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Suprapubik aspirasyon idrar kültürü için ALTIN STANDARTTIR; kontaminasyonsuzdur ve tek bir üropatojenin üremesi dahi tanı için yeterlidir."
    )
    s64_bullets = [
        "Suprapubik aspirasyon idrar kültürü için ALTIN STANDARTTIR.",
        "Kontaminasyonsuz örnektir; tek bir mikroorganizma üremesi tanı koydurur.",
        "İnvaziv olduğundan rutinde kullanılmaz; USG eşliğinde uygulanır."
    ]
    s64_elements = [
        make_cloze("İdrar kültürü için kontaminasyonsuz kesin altın standart yöntem suprapubik aspirasyon tekniğidir.", "suprapubik aspirasyon", "Mesane üzerinden enjektörle steril idrar çekilmesi"),
        make_table("Suprapubik Aspirasyon Özellikleri", ["Ölçüt", "Suprapubik Aspirasyon", "Orta Akım İdrarı"], [
            {"cells": [{"text": "Tanısal Değer", "isMasked": False}, {"text": "Kültür için ALTIN STANDART", "isMasked": True, "hint": "en güvenilir referans metot"}, {"text": "Standart rutin tarama yöntemi"}]},
            {"cells": [{"text": "Kontaminasyon Riski", "isMasked": False}, {"text": "Sıfır (kontaminasyonsuz)", "isMasked": False}, {"text": "Perine ve deri florası karışabilir", "isMasked": True, "hint": "flora bulaşma olasılığı"}]},
            {"cells": [{"text": "Tanısal Koloni Eşiği", "isMasked": False}, {"text": "Tek bir bakteri üremesi tanısal", "isMasked": True, "hint": "herhangi bir sayıda üropatojen"}, {"text": "≥10⁵ (100.000) KOB/ml aranır"}]}
        ]),
        make_chain("Suprapubik Aspirasyon Prosedürü", [
            "1. Mesane Dolumu: Mesanenin idrarla dolu olduğu palpasyon veya USG ile doğrulanır.",
            "2. Cilt Antisepsisi: Suprapubik simfizis üzeri steril olarak temizlenir.",
            "3. Perkütan Giriş: İğne dik açıyla mesane lümenine batırılır.",
            "4. Doğrudan Aspirasyon: Çekilen idrarda tek bir basil üremesi enfeksiyonu kanıtlar."
        ]),
        make_recall("İdrar kültürü için kontaminasyonsuz altın standart yöntem nedir ve bu yöntemde tanısal koloni sayısı kuralı nasıldır?", "Suprapubik aspirasyondur; bu yöntemde tek bir mikroorganizmanın (herhangi bir sayıda basil) üremesi dahi tanısal kabul edilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Suprapubik Aspirasyon", [
            {"text": "Suprapubik aspirasyon idrar kültürü için altın standarttır.", "isLie": False, "explanation": "Doğru. Kontaminasyonsuz örnektir."},
            {"text": "Suprapubik aspirasyonda tek bir mikroorganizma tanısal önem taşır.", "isLie": False, "explanation": "Doğru. 10⁵ kuralı aranmaz."},
            {"text": "Suprapubik aspirasyon her gün sabah akşam tüm grip hastalarına zorunlu rutin testtir.", "isLie": True, "explanation": "Tuzak! İnvaziv bir işlem olduğu için rutinde KULLANILMAZ; özel durumlarda uygulanır."},
            {"text": "İşlem genellikle ultrasonografi eşliğinde güvenle yapılır.", "isLie": False, "explanation": "Doğru. Mesaneyi görmek komplikasyonu önler."}
        ]),
        make_quiz("İdrar kültürü için kontaminasyonsuz altın standart olan ve tek bir bakterinin üremesinin dahi tanısal önem taşıdığı örnek alma yöntemi hangisidir?", [
            {"key": "A", "text": "Suprapubik mesane aspirasyonu", "isCorrect": True, "explanation": "Ders notunda 'suprapubik aspirasyon: altın standart; kontaminasyonsuz örnek; tek bir mikroorganizma tanısal önem taşır' şeklinde belirtilmiştir."},
            {"key": "B", "text": "Klozete yapılmış idrardan enjektörle çekilen örnek", "isCorrect": False, "explanation": "Aşırı kontaminedir."},
            {"key": "C", "text": "Çocuğun bezinden sıkılan idrar", "isCorrect": False, "explanation": "Bakteriüri tanısında yetersizdir."},
            {"key": "D", "text": "Sadece kulak kiri sürüntüsü", "isCorrect": False, "explanation": "İdrar örneği değildir."}
        ])
    ]
    slides.append(make_slide(64, "Suprapubik Aspirasyon: Kontaminasyonsuz Altın Standart", "Suprapubik aspirasyon, altın standart niteliği, tek bakteri kuralı ve USG kullanımı", "Tanı Yöntemleri", s64_narrative, s64_bullets, s64_elements))

    # Slide 65: Torba Örneği, Kateter ve Prezervatif Sondalar
    s65_narrative = (
        "Tuvalet eğitimi almamış küçük çocuklarda veya yatalak erişkinlerde idrar toplama yöntemleri "
        "kolaylık sağlasa da ciddi kontaminasyon tuzakları barındırır.\n\n"
        "- **Torba Örneği (Poşet):** Küçük çocuklarda genital bölgeye yapıştırılan torbalarla alınır. "
        "En kritik kural: **30 dakikada idrar alınamadıysa kontaminasyon riski katlanır ve torba değiştirilmelidir**.\n"
        "- **Torbanın Tanısal Değeri:** Torba örneği **İYE'yi ekarte ettirmede etkilidir (kültür negatifse "
        "enfeksiyon yoktur); ancak tanı koydurmada yetersizdir**, çünkü yanlış pozitiflik oranı çok yüksektir.\n"
        "- **Kateter ve Prezervatif Sonda:** Yatalak hastalarda üretral foley kateter ile doğrudan idrar "
        "alınabilir; erkeklerde prezervatif sondalar kullanılabilir ancak cilt florası kontaminasyonu unutulmamalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Çocuklarda torba idrar örneği: Negatifse İYE'yi ekarte ettirir; ancak yanlış pozitifliği yüksek olduğu için pozitif kültürle kesin tanı konulamaz (doğrulama gerekir)."
    )
    s65_bullets = [
        "Torba örneğinde 30 dakikada idrar çıkmazsa torba yenilenmelidir.",
        "Torba örneği İYE'yi ekarte ettirmede etkili, kesin tanıda yetersizdir (yanlış pozitiflik yüksek).",
        "Yatalak hastalarda kateterle örnek alınabilir; prezervatif sonda cilt kontaminasyonu taşır."
    ]
    s65_elements = [
        make_cloze("Çocuklarda torba idrar örneği İYE'yi ekarte ettirmede etkili ancak yüksek yanlış pozitiflik nedeniyle kesin tanıda yetersizdir.", "ekarte ettirmede", "Hastalığın olmadığını kanıtlama işlevi"),
        make_table("Torba Örneği ve Diğer Metotların Sınırları", ["Yöntem", "Güçlü Yönü", "Zayıf Yönü / Kısıtlılığı"], [
            {"cells": [{"text": "Torba Örneği (Çocuk)", "isMasked": False}, {"text": "Non-invaziv, negatifse İYE'yi ekarte ettirir", "isMasked": True, "hint": "kolay uygulanır ve negatifi dışlar"}, {"text": "30 dk kuralı aşılırsa yanlış pozitiflik fırlar"}]},
            {"cells": [{"text": "Üretral Kateter", "isMasked": False}, {"text": "Yatalak hastada hızlı ve doğrudan örnek", "isMasked": False}, {"text": "Üretral travma ve iyatrojenik enfeksiyon riski", "isMasked": True, "hint": "girişime bağlı mikrop sokma riski"}]},
            {"cells": [{"text": "Prezervatif Sonda", "isMasked": False}, {"text": "Erkekte konforlu toplama", "isMasked": False}, {"text": "Peristomal cilt florası kolonizasyonu", "isMasked": False}]}
        ]),
        make_chain("Çocukta Torba İdrar Değerlendirme Algoritması", [
            "1. Torba Yapıştırma: Cilt temizlenip steril torba yapıştırılır.",
            "2. 30 Dakika Kuralı: İdrar 30 dakikada gelmezse torba çıkarılıp yenisi takılır.",
            "3. Negatif Sonuç: Torba kültürü üremezse → İYE kesinlikle dışlanır (ekarte edilir).",
            "4. Pozitif Sonuç: Üreme olursa → Yanlış pozitiflik şüphesiyle kateter/orta akımla doğrulanır."
        ]),
        make_recall("Çocuklarda kullanılan torba idrar örneğinin tanısal güvenilirliği ve 30 dakika kuralı nedir?", "30 dakikada idrar alınamazsa kontaminasyon riski artar ve torba değiştirilmelidir. Negatif çıkarsa İYE'yi ekarte ettirir, fakat yanlış pozitifliği yüksek olduğundan tek başına kesin tanı koydurmaz."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Torba ve Kateter Örneği", [
            {"text": "Çocuklarda torba örneğinde 30 dakikada idrar alınamazsa kontaminasyon riski artar.", "isLie": False, "explanation": "Doğru. Süre kuralıdır."},
            {"text": "Torba örneği İYE'yi ekarte ettirmekte etkilidir.", "isLie": False, "explanation": "Doğru. Negatif prediktif değeri yüksektir."},
            {"text": "Torba örneği kültüründe bakteri ürediğinde hiçbir doğrulama yapmadan derhal böbrek ameliyatı yapılır.", "isLie": True, "explanation": "Tuzak! Torba örneğinin yanlış pozitiflik oranı çok yüksektir; tanıda yetersizdir ve mutlaka doğrulanmalıdır."},
            {"text": "Yatalak hastalarda üretral kateterle idrar örneği alınabilir.", "isLie": False, "explanation": "Doğru. Standart yaklaşımdır."}
        ]),
        make_quiz("Çocuklarda idrar torbası ile toplanan idrar örneğinin tanısal değeri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "İYE'yi ekarte ettirmekte etkilidir ancak yanlış pozitifliği yüksek olduğundan kesin tanıda yetersizdir", "isCorrect": True, "explanation": "Ders notunda 'İYE'yi ekarte ettirmekte etkili ancak tanısında yetersizdir; yanlış pozitiflik oranı yüksektir' ifadesi yer almaktadır."},
            {"key": "B", "text": "Kültür için dünyadaki tek kontaminasyonsuz altın standart yöntemdir", "isCorrect": False, "explanation": "Altın standart suprapubik aspirasyondur."},
            {"key": "C", "text": "Torba yapıştırıldıktan sonra 3 hafta boyunca hiç çıkarılmamalıdır", "isCorrect": False, "explanation": "30 dakikada değiştirilmelidir."},
            {"key": "D", "text": "Sadece yetişkin erkeklerde kullanılır", "isCorrect": False, "explanation": "Küçük çocuklarda kullanılır."}
        ])
    ]
    slides.append(make_slide(65, "Torba Örneği, Kateter ve Prezervatif Sondalar", "Torba örneği, 30 dakika kuralı, ekarte ettirme gücü ve yanlış pozitiflik riski", "Tanı Yöntemleri", s65_narrative, s65_bullets, s65_elements))

    # Slide 66: İdrar Örneğinin Laboratuvara Ulaşması: 1 Saat Kuralı ve 4°C
    s66_narrative = (
        "Doğru teknikle alınan bir idrar örneğinin laboratuvara ulaştırılması ve ekim süreci, tanısal "
        "sonucun doğruluğunu belirleyen en hassas zaman çizelgesidir.\n\n"
        "- **1 Saat Kuralı:** İdrar vücuttan çıktıktan sonra oda sıcaklığında bekletilirse içindeki "
        "bakteriler hızla bölünmeye devam eder ve lökositler parçalanır. Bu nedenle **idrar örneği "
        "alındıktan sonra EN GEÇ 1 SAAT İÇİNDE tetkik edilmelidir**.\n"
        "- **Soğukta Saklama (4°C):** Eğer örneğin 1 saat içinde laboratuvarda çalışılması veya ekilmesi "
        "mümkün değilse, bakteri çoğalmasını durdurmak amacıyla **buzdolabında 4°C'de saklanmalı** "
        "ve bekleme süresi **en fazla 24 saati** aşmamalıdır.\n"
        "- **Gecikmenin Zararı:** Beklemiş idrarda yalancı yüksek bakteri sayıları (yanlış pozitiflik) "
        "ve parçalanan lökositler nedeniyle mikroskopide piyürinin kaçırılması meydana gelir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İdrar örneği alındıktan sonra 1 SAAT içinde incelenmelidir; hemen ekilemeyecekse 4°C'de (en fazla 24 saat) saklanmalıdır."
    )
    s66_bullets = [
        "İdrar örneği alındıktan sonra en geç 1 saat içinde tetkik edilmelidir.",
        "Hemen incelenemeyecekse buzdolabında 4°C'de en fazla 24 saat saklanabilir.",
        "Oda ısısında bekleme bakteriyel üremeyi yapay olarak artırır ve lökositleri eritir."
    ]
    s66_elements = [
        make_cloze("İdrar örneği oda ısısında bekletilmeden alındıktan sonraki 1 saat içinde tetkik edilmelidir.", "1 saat içinde", "Altmış dakikalık laboratuvara teslim süresi"),
        make_table("İdrar Saklama ve Transport Koşulları", ["Koşul", "İzin Verilen Süre", "Patolojik Risk"], [
            {"cells": [{"text": "Oda Sıcaklığı (Transport)", "isMasked": False}, {"text": "En fazla 1 saat içinde", "isMasked": True, "hint": "bir saatlik maksimum süre"}, {"text": "Bakterilerin yapay çoğalması ve lökosit lizisi"}]},
            {"cells": [{"text": "Buzdolabı Saklama (4°C)", "isMasked": False}, {"text": "En fazla 24 saat", "isMasked": True, "hint": "yirmi dört saatlik soğuk saklama"}, {"text": "24 saat aşılırsa kültür güvenilirliğini kaybeder"}]}
        ]),
        make_chain("Zamanında Transport Zinciri", [
            "1. Örnek Alımı: Sabah temiz orta akım idrarı steril tüpe alınır.",
            "2. Hızlı Gönderim: 1 saat kuralına uyularak derhal laboratuvara ulaştırılır.",
            "3. Alternatif Saklama: Gecikme olacaksa tüp derhal 4°C buzdolabına konur.",
            "4. Güvenilir Sonuç: Zamanında yapılan analizde gerçek lökosit ve koloni sayısı saptanır."
        ]),
        make_recall("Alınan bir idrar örneği oda sıcaklığında en geç kaç saat içinde tetkik edilmelidir; bekleyecekse nasıl saklanmalıdır?", "En geç 1 saat içinde tetkik edilmelidir; bekleyecekse 4°C'de buzdolabında en fazla 24 saat saklanmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 1 Saat Kuralı", [
            {"text": "İdrar örneği 1 saat içinde tetkik edilmelidir.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Bekleyecekse 4°C'de buzdolabında en fazla 24 saat saklanabilir.", "isLie": False, "explanation": "Doğru. Soğuk zincir kuralıdır."},
            {"text": "İdrar örneği kalorifer üzerinde 1 hafta bekletildikten sonra incelenirse çok daha taze olur.", "isLie": True, "explanation": "Tuzak! Kaloriferde bekleyen idrarda bakteriler aşırı çoğalır, lökositler parçalanır ve test tamamen çöpe döner."},
            {"text": "Beklemiş idrarda lökositler mikroskopide parçalanıp kaybolabilir.", "isLie": False, "explanation": "Doğru. Lizis meydana gelir."}
        ]),
        make_quiz("İdrar örneği alındıktan sonra oda sıcaklığında en geç ne kadar süre içinde tetkik edilmelidir?", [
            {"key": "A", "text": "1 saat içinde (bekleyecekse 4°C'de en fazla 24 saat)", "isCorrect": True, "explanation": "Ders notunda 'İdrar 1 saat içinde tetkik edilmelidir; bekleyecekse 4°C'de (en fazla 24 saat) saklanmalıdır' açıkça ifade edilmiştir."},
            {"key": "B", "text": "5 gün sonra", "isCorrect": False, "explanation": "Çok geçtir."},
            {"key": "C", "text": "Tam 1 ay sonra", "isCorrect": False, "explanation": "Tamamen bozulur."},
            {"key": "D", "text": "Sadece 3 saniye içinde", "isCorrect": False, "explanation": "Gerçekçi değildir."}
        ])
    ]
    slides.append(make_slide(66, "İdrar Örneğinin Laboratuvara Ulaşması: 1 Saat Kuralı ve 4°C", "1 saat içinde tetkik kuralı, 4°C buzdolabında saklama ve lökosit lizisi riski", "Tanı Yöntemleri", s66_narrative, s66_bullets, s66_elements))

    # Slide 67: İdrar Analizinin Bileşenleri: Fiziksel, Kimyasal ve Mikroskopik
    s67_narrative = (
        "Tam idrar tahlili (TİT), üriner sistemin durumunu ve böbreğin fonksiyonlarını üç temel "
        "kategoride inceleyen hızlı, ucuz ve kapsamlı bir laboratuvar panelidir.\n\n"
        "- **1. Fiziksel İnceleme:** İdrarın çıplak gözle görünümü, berraklık veya bulanıklığı, volümü, "
        "rengi ve dansitesi (yoğunluğu) değerlendirilir.\n"
        "- **2. Kimyasal İnceleme (Dipstik):** Strip reaktifleri ile pH, protein, glukoz, keton, "
        "bilirubin, ürobilinojen, gizli kan ve enfeksiyonun iki kardinal kimyasal belirteci olan "
        "**lökosit esteraz ve nitrit** test edilir.\n"
        "- **3. Mikroskopik İnceleme (Sediment):** Santrifüj veya nativ idrarda lökositler, eritrositler, "
        "silendirler (özellikle lökosit silendiri), bakteriler ve kristaller mikroskop altında sayılır.\n\n"
        "> [!NOTE]\n"
        "> Tam idrar analizi bu üç basamağın (fiziksel, kimyasal ve mikroskopik) harmonik değerlendirilmesiyle kesin tanıya götürür."
    )
    s67_bullets = [
        "Fiziksel: Görünüm, berraklık/bulanıklık, renk, volüm ve dansite.",
        "Kimyasal: pH, protein, glukoz, nitrit ve lökosit esteraz.",
        "Mikroskopik: Lökosit, eritrosit, silendirler, bakteriler ve kristaller."
    ]
    s67_elements = [
        make_cloze("Tam idrar analizinde dipstik şeritleri ile pH, glukoz, protein, lökosit esteraz ve nitrit testleri yapılır.", "lökosit esteraz", "Piyüriyi gösteren kimyasal enzim testi"),
        make_table("Tam İdrar Analizinin Üç Ana Bileşeni", ["Kategori", "İncelenen Parametreler", "Temel Tanısal Amaç"], [
            {"cells": [{"text": "Fiziksel Analiz", "isMasked": False}, {"text": "Görünüm, renk, bulanıklık, dansite", "isMasked": True, "hint": "gözle yapılan fiziksel gözlem"}, {"text": "Konsantrasyon ve bulanıklık değerlendirmesi"}]},
            {"cells": [{"text": "Kimyasal Analiz", "isMasked": False}, {"text": "pH, protein, glukoz, nitrit, lökosit esteraz", "isMasked": False}, {"text": "Enflamasyon ve metabolik tarama", "isMasked": True, "hint": "şerit reaksiyonuyla kimyasal tespit"}]},
            {"cells": [{"text": "Mikroskopik Analiz", "isMasked": False}, {"text": "Lökosit, eritrosit, silendir, bakteri", "isMasked": False}, {"text": "Hücresel düzeyde parankim ve lümen incelemesi", "isMasked": False}]}
        ]),
        make_chain("İdrar Analiz Basamakları", [
            "1. Makroskopi: İdrarın açık sarı, berrak veya pürülan bulanık rengi not edilir.",
            "2. Dipstik: Şerit batırılarak nitrit ve lökosit esteraz renk reaksiyonları okunur.",
            "3. Santrifüj: İdrar 2000 devirde çevrilip çökelti lam-lamel arasına yayılır.",
            "4. Mikroskopi: Lökosit sayısı ve lökosit silendirleri yüksek büyütmede sayılır."
        ]),
        make_recall("Tam idrar analizini oluşturan üç temel inceleme kategorisi nelerdir?", "Fiziksel inceleme (görünüm, dansite), kimyasal inceleme (dipstik/nitrit/LE) ve mikroskopik incelemedir (hücre, silendir, bakteri)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İdrar Analizi Bileşenleri", [
            {"text": "Fiziksel analizde idrarın görünümü, volümü ve dansitesi incelenir.", "isLie": False, "explanation": "Doğru. Fiziksel özelliklerdir."},
            {"text": "Kimyasal analizde nitrit ve lökosit esteraz taranır.", "isLie": False, "explanation": "Doğru. Strip testidir."},
            {"text": "İdrar mikroskopisinde sadece yıldız haritası çıkarılır, hücrelere asla bakılmaz.", "isLie": True, "explanation": "Tuzak! İdrar mikroskopisinde lökositler, eritrositler, silendirler ve bakteriler sayılır."},
            {"text": "Mikroskopik incelemede lökosit silendirleri böbrek hasarını gösterir.", "isLie": False, "explanation": "Doğru. Pyelonefrit göstergesidir."}
        ]),
        make_quiz("Aşağıdakilerden hangisi tam idrar analizinin KİMYASAL (dipstik) inceleme parametrelerinden biridir?", [
            {"key": "A", "text": "Lökosit esteraz ve nitrit", "isCorrect": True, "explanation": "Ders notunda kimyasal inceleme parametreleri arasında pH, protein, glukoz, nitrit, lökosit esteraz vb. sayılmıştır."},
            {"key": "B", "text": "İdrarın sadece mililitre cinsinden volümü", "isCorrect": False, "explanation": "Fiziksel parametredir."},
            {"key": "C", "text": "Lökosit kamerasında mm³'teki lökosit sayısı", "isCorrect": False, "explanation": "Mikroskopik parametredir."},
            {"key": "D", "text": "Lökosit silendirlerinin mikroskopta görülmesi", "isCorrect": False, "explanation": "Mikroskopik parametredir."}
        ])
    ]
    slides.append(make_slide(67, "İdrar Analizinin Bileşenleri: Fiziksel, Kimyasal ve Mikroskopik", "Fiziksel (dansite/görünüm), kimyasal (dipstik/nitrit/LE) ve mikroskopik inceleme", "Tanı Yöntemleri", s67_narrative, s67_bullets, s67_elements))

    # Slide 68: İdrarın Fiziksel Özellikleri: Ürokrom, Renk ve Bulanıklık
    s68_narrative = (
        "İdrarın çıplak gözle yapılan fiziksel değerlendirmesi, hekime hastanın hidrasyon durumu ve "
        "üriner sistemdeki masif patolojiler hakkında anında görsel bilgi sağlar.\n\n"
        "- **Normal Renk ve Ürokrom:** Normal koşullarda idrar, endojen bir pigment olan **ürokrom "
        "(ve ürobilin) nedeniyle açık sarı renktedir**; konsantrasyon arttıkça renk koyulaşır.\n"
        "- **Bulanıklık ve Koku:** Şeffaf bir tüpte idrarın berraklığı incelenir; yoğun lökosit (piyüri), "
        "bakteriüri, kristalüri veya mukus varlığında **idrar bulanıklaşır** ve kötü kokulu hale gelebilir.\n"
        "- **Renk Değişiklikleri:** Hematüride çay veya et suyu rengi; bilirubinüride koyu çay/bira rengi; "
        "kullanılan antibiyotikler (ör. rifampisin ile kırmızı-turuncu; nitrofurantoin ile kahverengi) "
        "idrar rengini değiştirebilir.\n\n"
        "> [!NOTE]\n"
        "> Normal idrar berrak ve açık sarıdır; pürülan bulanık görünüm yoğun piyüri ve bakteriyel enfeksiyon lehinedir."
    )
    s68_bullets = [
        "Normal idrar içindeki ürokrom maddesinden dolayı açık sarı renktedir.",
        "Yoğun piyüri ve bakteriüri idrarda belirgin bulanıklık ve koku yaratır.",
        "İlaçlar ve hematüri idrar renginde patolojik değişikliklere yol açabilir."
    ]
    s68_elements = [
        make_cloze("Normal idrar rengi içinde bulunan ürokrom pigmentinden dolayı açık sarı renkte izlenir.", "ürokrom", "İdrara doğal sarı rengini veren endojen madde"),
        make_table("İdrar Fiziksel Özellikleri ve Anlamları", ["Fiziksel Özellik", "Normal Durum", "Patolojik Görünüm ve Neden"], [
            {"cells": [{"text": "Renk", "isMasked": False}, {"text": "Açık sarı (ürokrom ile)", "isMasked": True, "hint": "normal idrarın sarılığı"}, {"text": "Kırmızı/çay rengi (hematüri), koyu kahve (bilirubin)"}]},
            {"cells": [{"text": "Berraklık", "isMasked": False}, {"text": "Tamamen şeffaf ve berrak", "isMasked": False}, {"text": "Bulanık (piyüri, bakteri, fosfat kristalleri)", "isMasked": True, "hint": "iltihap ve mikrop bulanıklığı"}]},
            {"cells": [{"text": "Dansite", "isMasked": False}, {"text": "1010 - 1025 arası", "isMasked": False}, {"text": "Dilüe idrarda <1005; konsantre dehidrate >1030", "isMasked": False}]}
        ]),
        make_chain("Fiziksel Gözlem Akışı", [
            "1. Işığa Tutma: Temiz cam tüpte idrar ışığa karşı tutulur.",
            "2. Renk Tespiti: Açık sarı ürokrom rengi doğrulanır.",
            "3. Bulanıklık Tespiti: Yazı arkasından okunabiliyor mu (bulanıklık piyüriyi düşündürür).",
            "4. Koku Değerlendirmesi: Amonyak veya pis koku üreaz pozitif bakterileri düşündürür."
        ]),
        make_recall("Normal idrara açık sarı rengini veren endojen metabolit nedir?", "Ürokrom maddesidir (ürokrom pigmenti)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İdrar Fiziksel Özellikleri", [
            {"text": "Normal idrar içindeki ürokromdan dolayı açık sarı renktedir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "İdrar konsantrasyonu arttıkça renk daha da koyulaşır.", "isLie": False, "explanation": "Doğru. Dehidratasyonda koyulaşır."},
            {"text": "Normal sağlıklı idrar masmavi, simli ve fosforlu parlayan bir sıvıdır.", "isLie": True, "explanation": "Tuzak! Normal idrar şeffaf berrak ve açık sarı renklidir."},
            {"text": "Piyüri ve bakteriüri idrarda belirgin bulanıklığa yol açabilir.", "isLie": False, "explanation": "Doğru. Bulanıklık enflamasyon işaretidir."}
        ]),
        make_quiz("Normal idrara karakteristik açık sarı rengini veren madde aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Ürokrom", "isCorrect": True, "explanation": "Ders notunda 'normal idrar içindeki ürokromdan dolayı açık sarı renktedir' cümlesi açıkça yer almaktadır."},
            {"key": "B", "text": "Melanin", "isCorrect": False, "explanation": "Deri pigmentidir."},
            {"key": "C", "text": "Klorofil", "isCorrect": False, "explanation": "Bitki pigmentidir."},
            {"key": "D", "text": "Karoten", "isCorrect": False, "explanation": "Havuç pigmentidir."}
        ])
    ]
    slides.append(make_slide(68, "İdrarın Fiziksel Özellikleri: Ürokrom, Renk ve Bulanıklık", "Ürokrom pigmenti, açık sarı renk, dansite, bulanıklık ve renk anomalileri", "Tanı Yöntemleri", s68_narrative, s68_bullets, s68_elements))

    # Slide 69: Yedinci Bölüm Özeti: Tanı Yöntemleri ve Örnek Alma İlkeleri
    s69_narrative = (
        "Üriner sistem enfeksiyonlarında doğru laboratuvar tanısı, titiz bir anamnez ve doğru teknikle "
        "alınmış idrar örneği üzerine inşa edilir.\n\n"
        "- **Klinik Muayene:** Suprapubik hassasiyet sistiti, kostavertebral açı hassasiyeti (KVAH) "
        "akut pyelonefriti gösterir; çocuklarda 3 aydan sonra kız baskınlığı (E/K: 1/10) başlar.\n"
        "- **Örnek Alma Yöntemleri:** En uygun örnek bakteri yoğunluğu en yüksek olan sabah ilk orta akım "
        "idrarıdır. **Suprapubik aspirasyon altın standarttır** ve tek bir bakteri bile tanı koydurur; "
        "torba örneği ise negatifse İYE'yi ekarte ettirir ancak yanlış pozitifliği yüksektir.\n"
        "- **Laboratuvar Transportu:** İdrar örneği oda sıcaklığında **en geç 1 saat içinde** incelenmeli; "
        "bekleyecekse buzdolabında **4°C'de (en fazla 24 saat)** saklanmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> Doğru tanı: Sabah ilk idrarı, 1 saat içinde çalışma, suprapubik aspirasyon altın standart ve KVAH ile pyelonefrit tespiti ile sağlanır."
    )
    s69_bullets = [
        "Suprapubik hassasiyet (sistit), KVAH (pyelonefrit); çocukta 3 aydan sonra E/K: 1/10.",
        "Sabah ilk idrar en uygundur; suprapubik aspirasyon kesin ALTIN STANDARTTIR.",
        "İdrar 1 saat içinde incelenmeli veya 4°C'de en fazla 24 saat saklanmalıdır."
    ]
    s69_elements = [
        make_cloze("Örnek alma yöntemleri içinde kontaminasyonsuz altın standart suprapubik aspirasyon yöntemidir.", "suprapubik aspirasyon", "Mesane iğne aspirasyonu referans yöntemi"),
        make_table("Bölüm 7 Anahtar Tanısal Standartlar", ["Aşama / Yöntem", "Kritik Standart", "Klinik Mesaj"], [
            {"cells": [{"text": "En Uygun Örnek", "isMasked": False}, {"text": "Sabah ilk idrar örneği", "isMasked": True, "hint": "gece beklemiş idrar"}, {"text": "Bakteri konsantrasyonu en yüksek örnektir"}]},
            {"cells": [{"text": "Kültür Altın Standardı", "isMasked": False}, {"text": "Suprapubik aspirasyon", "isMasked": True, "hint": "kontaminasyonsuz mesane ponksiyonu"}, {"text": "Tek bakteri dahi tanısal kabul edilir"}]},
            {"cells": [{"text": "Laboratuvar Zamanı", "isMasked": False}, {"text": "1 saat kuralı (veya 4°C'de 24 saat)", "isMasked": False}, {"text": "Yapay üreme ve lökosit lizisini önler", "isMasked": True, "hint": "örneğin bozulmasını engelleme"}]}
        ]),
        make_recall("İdrar kültürü için altın standart yöntem ile pediatrik torba örneğinin temel tanısal farkı nedir?", "Suprapubik aspirasyon kontaminasyonsuz altın standarttır ve tek bakteriyle tanı koydurur; torba örneği ise yanlış pozitifliği yüksek olduğu için sadece negatifse İYE'yi ekarte ettirmede etkilidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 7 Özeti", [
            {"text": "İdrar kültürü için altın standart suprapubik aspirasyondur.", "isLie": False, "explanation": "Doğru. Kontaminasyonsuz referanstır."},
            {"text": "İdrar 1 saat içinde tetkik edilmeli veya 4°C'de saklanmalıdır.", "isLie": False, "explanation": "Doğru. Temel saklama kuralıdır."},
            {"text": "Torba örneği pozitif çıktığında %100 kesin altın standart tanı sayılır.", "isLie": True, "explanation": "Tuzak! Torba örneğinin yanlış pozitifliği çok yüksektir; sadece negatifken ekarte ettirir, pozitifken doğrulama gerekir."},
            {"text": "Sabah ilk idrar bakteri konsantrasyonu en yüksek örnek olduğu için en uygundur.", "isLie": False, "explanation": "Doğru. İdeal örnektir."}
        ]),
        make_quiz("İdrar toplama ve transport kuralları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Suprapubik aspirasyon altın standarttır ve idrar en geç 1 saat içinde tetkik edilmelidir", "isCorrect": True, "explanation": "Ders notunda belirtilen iki kardinal tanısal kuraldır."},
            {"key": "B", "text": "Torba örneği suprapubik aspirasyondan çok daha üstün bir altın standarttır", "isCorrect": False, "explanation": "Torba örneğinin yanlış pozitifliği yüksektir."},
            {"key": "C", "text": "İdrar örneği fırında 200 derecede pişirilip laboratuvara yollanmalıdır", "isCorrect": False, "explanation": "Tıbbi saçmalıktır."},
            {"key": "D", "text": "İdrar mikroskopisinde hücrelere bakılmaz sadece kokuya bakılır", "isCorrect": False, "explanation": "Hücre sayımı esastır."}
        ])
    ]
    slides.append(make_slide(69, "Yedinci Bölüm Özeti: Tanı Yöntemleri ve Örnek Alma İlkeleri", "Anamnez, KVAH, sabah ilk idrar, suprapubik altın standart ve 1 saat kuralı", "Konsolidasyon", s69_narrative, s69_bullets, s69_elements))

    # Slide 70: [TEKRAR SAYFASI - CHECKPOINT 7] Anamnez, İdrar Toplama ve Fiziksel Analiz
    s70_narrative = (
        "Bu tekrar sayfasında 7. Bölümde işlenen anamnez sorgulamalarını, fizik muayene bulgularını, "
        "örnek toplama tekniklerini ve idrarın fiziksel analizini konsolide ediyoruz.\n\n"
        "- **Klinik ve Muayene:** Suprapubik hassasiyet alt sistemi (sistit), kostavertebral açı hassasiyeti "
        "(KVAH) üst sistemi (pyelonefrit) gösterir. Çocuklarda 3 aydan sonra kız üstünlüğüyle **E/K: 1/10** olur.\n"
        "- **Örnek Alma Yöntemleri:** En uygun örnek konsantre olan **sabah ilk idrardır**. Kontaminasyonsuz "
        "kesin **altın standart suprapubik aspirasyondur** (tek bir basil dahi tanısal). Torba örneği "
        "İYE'yi ekarte ettirmede etkili fakat yanlış pozitifliği yüksektir (30 dk kuralı).\n"
        "- **Laboratuvar Transportu:** Örnek **1 saat içinde** incelenmeli; bekleyecekse **4°C'de en fazla "
        "24 saat** buzdolabında tutulmalıdır. İdrara sarı rengini **ürokrom** verir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] 1) Altın standart = Suprapubik aspirasyon (tek bakteri dahi tanısal)! 2) En uygun = Sabah ilk idrar! 3) Süre = 1 saat içinde (veya 4°C'de 24 saat)! 4) Çocuk >3 ay = E/K: 1/10!"
    )
    s70_bullets = [
        "Suprapubik aspirasyon kontaminasyonsuz ALTIN STANDARTTIR (tek bakteri tanısal).",
        "En uygun örnek sabah ilk idrardır; 1 saat içinde tetkik edilmelidir.",
        "Torba örneği ekarte ettirir ama yanlış pozitifi sıktır; çocukta E/K: 1/10'dur."
    ]
    s70_elements = [
        make_cloze("Kontaminasyonsuz kesin altın standart olan suprapubik aspirasyonda tek bir bakterinin üremesi dahi tanısal kabul edilir.", "tek bir", "Herhangi bir sayıda basilin yeterli olması"),
        make_table("7. Bölüm Büyük Tekrar Tablosu", ["Konu / Parametre", "Doğru Tıbbi Kabul", "Tanısal Değer"], [
            {"cells": [{"text": "Örnek Altın Standardı", "isMasked": False}, {"text": "Suprapubik mesane aspirasyonu", "isMasked": True, "hint": "kontaminasyonsuz iğne aspirasyonu"}, {"text": "Tek mikroorganizma üremesi kesin tanı koydurur"}]},
            {"cells": [{"text": "En Uygun İdrar", "isMasked": False}, {"text": "Sabah ilk idrar örneği", "isMasked": False}, {"text": "Bakteri konsantrasyonu en yüksek", "isMasked": True, "hint": "gece boyu yoğunlaşan bakteri sayısı"}]},
            {"cells": [{"text": "Transport Zamanı", "isMasked": False}, {"text": "1 saat içinde tetkik edilmeli", "isMasked": True, "hint": "altmış dakikalık sınır"}, {"text": "Bekleyecekse 4°C'de en fazla 24 saat"}]},
            {"cells": [{"text": "Pediatrik Cinsiyet (>3 ay)", "isMasked": False}, {"text": "Erkek / Kadın oranı: 1 / 10", "isMasked": False}, {"text": "Kız çocuklarında belirgin sıklık", "isMasked": False}]}
        ]),
        make_chain("7. Bölüm Tanısal Karar Akışı", [
            "1. Örnek Alma: Sabah ilk orta akım idrarı meatus temizliği sonrası alınır.",
            "2. Transport: 1 saat içinde laboratuvara ulaştırılır (gecikirse 4°C buzdolabına alınır).",
            "3. Şüpheli Bebek: Çocukta torba yerine kesinlik gerekiyorsa USG ile suprapubik aspirasyon yapılır.",
            "4. Değerlendirme: Suprapubik örnekte tek bir basil üremesiyle tanı kesinleştirilir."
        ]),
        make_recall("Suprapubik aspirasyonun idrar kültüründeki tanısal konumu ve koloni eşiği kuralı nedir?", "Kontaminasyonsuz ALTIN STANDARTTIR; tek bir mikroorganizmanın (herhangi bir sayıda basil) üremesi dahi tanısal kabul edilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 7. Bölüm Konsolidasyonu", [
            {"text": "Suprapubik aspirasyon idrar kültürü için altın standarttır.", "isLie": False, "explanation": "Doğru. Referans yöntemdir."},
            {"text": "İdrar 1 saat içinde tetkik edilmeli veya 4°C'de buzdolabında saklanmalıdır.", "isLie": False, "explanation": "Doğru. Transport kuralıdır."},
            {"text": "Suprapubik aspirasyonda tanı koymak için en az 10 trilyon bakteri üremesi şarttır.", "isLie": True, "explanation": "Tuzak! Suprapubik aspirasyonda TEK BİR mikroorganizmanın üremesi dahi kesin tanı koydurur."},
            {"text": "Normal idrara sarı rengini ürokrom maddesi verir.", "isLie": False, "explanation": "Doğru. Endojen pigmenttir."}
        ]),
        make_quiz("7. Bölümün temel kazanımlarına göre aşağıdaki tanısal kurallardan hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Suprapubik aspirasyon örneğinde tanı koyabilmek için en az 100.000 koloni üremesi beklenmelidir", "isCorrect": True, "explanation": "Kesinlikle yanlış! Suprapubik aspirasyonda 100.000 kuralı aranmaz; tek bir mikroorganizmanın (herhangi bir sayıda) üremesi tanısal önem taşır."},
            {"key": "B", "text": "İdrar kültürü için kontaminasyonsuz altın standart yöntem suprapubik aspirasyondur", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "En uygun idrar örneği sabah ilk idrardır", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "İdrar örneği alındıktan sonra 1 saat içinde tetkik edilmelidir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(70, "[TEKRAR SAYFASI - CHECKPOINT 7] Anamnez, İdrar Toplama ve Fiziksel Analiz", "7. Bölümün kapsamlı pekiştirmesi: anamnez, KVAH, suprapubik altın standart ve 1 saat kuralı", "Bölüm Tekrarı", s70_narrative, s70_bullets, s70_elements))

    return slides
