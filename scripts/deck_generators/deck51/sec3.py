# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec3():
    slides = []

    # Slide 21: Bulaş ve Yayılım Yollarına Genel Bakış: Dört Temel Rota
    s21_narrative = (
        "Mikroorganizmaların steril olan üriner traktusa ulaşması ve enfeksiyon tablosu başlatması, "
        "dört farklı anatomik ve fizyopatolojik yayılım yolu üzerinden gerçekleşir.\n\n"
        "- **Asendan Yol (%99):** En yaygın ve ezici çoğunluğu oluşturan yoldur; bağırsak kökenli "
        "bakterilerin perine ve üretradan mesaneye, oradan da üreterlerle böbreğe tırmanmasıdır.\n"
        "- **Hematojen Yol:** Vücudun başka bir odağındaki primer enfeksiyondan bakteriyemi yoluyla "
        "böbrek parankimine ulaşılmasıdır (S. aureus, Salmonella, Tbc, Candida).\n"
        "- **Lenfojen ve Direkt Yol:** Rektal ve periuterin lenfatiklerle olan lenfojen yayılım ile "
        "komşu pelvik apseler, İBH ve fistüllerden kaynaklanan direkt penetrasyondur.\n\n"
        "> [!NOTE]\n"
        "> Klinik pratikte karşılaşılan ÜSE vakalarının %99'u asendan yolla oluşur; diğer yollar nadir fakat spesifik etkenlerle seyreder."
    )
    s21_bullets = [
        "Asendan yol vakaların %99'unu oluşturur ve en önemli yayılım yoludur.",
        "Hematojen yol primer bakteriyemi sonrası böbreğin tutulmasıdır.",
        "Lenfojen yol ve fistüllerden kaynaklanan direkt yayılım nadir alternatiflerdir."
    ]
    s21_elements = [
        make_cloze("Üriner sistem enfeksiyonlarının ezici çoğunluğu olan %99'u asendan yol ile meydana gelir.", "%99'u", "Yüzde doksan dokuzluk ezici yayılım oranı"),
        make_table("ÜSE Bulaş ve Yayılım Yolları", ["Yayılım Yolu", "Görülme Oranı", "Tipik Etkenler / Durumlar"], [
            {"cells": [{"text": "Asendan Yol", "isMasked": False}, {"text": "%99 (en sık ve en önemli)", "isMasked": True, "hint": "vakaların neredeyse tamamı"}, {"text": "Enterobacteriaceae (E. coli, Proteus, Klebsiella)"}]},
            {"cells": [{"text": "Hematojen Yol", "isMasked": False}, {"text": "<%2 (nadir)", "isMasked": False}, {"text": "S. aureus, Salmonella, Candida, Tbc", "isMasked": True, "hint": "kan yoluyla böbreğe gelen etkenler"}]},
            {"cells": [{"text": "Direkt / Fistül", "isMasked": False}, {"text": "Nadir", "isMasked": False}, {"text": "Vezikovajinal / vezikointestinal fistüller, İBH", "isMasked": False}]}
        ]),
        make_chain("Bulaş Yollarının Anatomik Akışı", [
            "1. Asendan: Perine → Eksternal meatus → Üretra → Mesane → Böbrek.",
            "2. Hematojen: Uzak enfeksiyon odağı → Kan dolaşımı (bakteriyemi) → Renal korteks.",
            "3. Lenfojen: Kolonik/periuterin lenf damarları → Üriner traktus.",
            "4. Direkt: Komşu apse veya organ fistülü → Mesane lümeni."
        ]),
        make_recall("Üriner sistem enfeksiyonlarının yaklaşık yüzde kaçı asendan yolla meydana gelir?", "Yaklaşık %99'u asendan yolla meydana gelir (en sık ve en önemli yayılım yoludur)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bulaş Yolları", [
            {"text": "Asendan yol ÜSE'lerin %99'unu oluşturan en önemli yayılım yoludur.", "isLie": False, "explanation": "Doğru. Vakaların neredeyse tamamıdır."},
            {"text": "Hematojen yolla gelen etkenler arasında S. aureus ve Salmonella yer alır.", "isLie": False, "explanation": "Doğru. Kan yoluyla böbreğe ulaşırlar."},
            {"text": "ÜSE vakalarının %99'u sadece sivrisinek ısırığı ile hematojen yoldan bulaşır.", "isLie": True, "explanation": "Tuzak! ÜSE sivrisinekle bulaşmaz; %99 asendan yolla bağırsak florasından kaynaklanır."},
            {"text": "İntraperitoneal apseler ve fistüller direkt yayılma ile enfeksiyon yapabilir.", "isLie": False, "explanation": "Doğru. Komşuluk yoluyla geçer."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarında en sık ve en önemli bulaş yolu aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Asendan yol (%99)", "isCorrect": True, "explanation": "Ders notunda asendan yolun %99 oranında görüldüğü ve en sık/en önemli yol olduğu açıkça belirtilmiştir."},
            {"key": "B", "text": "Hematojen yol (%80)", "isCorrect": False, "explanation": "Hematojen yol <%2'dir."},
            {"key": "C", "text": "Hava yoluyla damlacık inhalasyonu", "isCorrect": False, "explanation": "ÜSE solunumla bulaşmaz."},
            {"key": "D", "text": "Retrograd lenfatik akım (%50)", "isCorrect": False, "explanation": "Lenfatik yol çok nadirdir."}
        ])
    ]
    slides.append(make_slide(21, "Bulaş ve Yayılım Yollarına Genel Bakış: Dört Temel Rota", "Asendan %99, hematojen, lenfojen ve direkt yayılım anatomisi", "Patogenez", s21_narrative, s21_bullets, s21_elements))

    # Slide 22: Asendan Yayılım Mekanizması (%99) ve Kadın Anatomisi
    s22_narrative = (
        "Asendan enfeksiyon yolu, bağırsak florasında yaşayan fekal bakterilerin perineal bölgeden "
        "üretraya ve oradan üst üriner sisteme yukarı doğru tırmanışını tanımlar.\n\n"
        "- **Kadın Yatkınlığının Anatomik Temeli:** Asendan yolun kadınlarda belirgin şekilde baskın "
        "olmasının en temel nedeni **üretranın kısa olması (yaklaşık 4 cm)** ve eksternal meatusun "
        "anüse ve perineye son derece yakın yerleşimidir.\n"
        "- **Kolonizasyon Basamakları:** Fekal Enterobacteriaceae üyeleri önce vajinal introitus ve "
        "periüretral dokuya kolonize olur; ardından kısa üretrayı hızla aşarak mesaneye ulaşır.\n"
        "- **Diğer Anatomik Faktörler:** Prostatik bakterisidal sekresyonların bulunmaması, menstrüel "
        "siklusa bağlı mukozal değişimler ve cinsel ilişki asendan geçişi kolaylaştırır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kadınlarda ÜSE'nin erkeklerden katbekat sık olmasının temel nedeni: Kısa üretra, anüse yakınlık ve periüretral kolonizasyondur."
    )
    s22_bullets = [
        "Kadın üretrasının kısa olması (4 cm) asendan yayılımı kolaylaştırır.",
        "Eksternal meatusun anal ve vajinal bölgeye yakınlığı kolonizasyon nedenidir.",
        "Prostat salgısının olmaması ve cinsel aktivite asendan geçişi tetikler."
    ]
    s22_elements = [
        make_cloze("Kadınlarda asendan enfeksiyonlara yatkınlığı artıran en temel anatomik faktör üretranın kısa olması ve anüse yakınlığıdır.", "üretranın kısa olması", "Yaklaşık 4 santimetrelik kadın üretrası"),
        make_table("Kadınlarda Asendan Yatkınlık Unsurları", ["Anatomik / Fizyolojik Faktör", "Erkekten Farkı", "Sonuç"], [
            {"cells": [{"text": "Üretra Uzunluğu", "isMasked": False}, {"text": "Kadında ~4 cm (erkekte ~20 cm)", "isMasked": True, "hint": "kadın üretrasının kısalığı"}, {"text": "Bakterilerin mesaneye çok hızlı tırmanması"}]},
            {"cells": [{"text": "Anüse Yakınlık", "isMasked": False}, {"text": "Perine ve rektuma komşu yerleşim", "isMasked": False}, {"text": "Fekal floranın periüretral kolonizasyonu", "isMasked": True, "hint": "dışkı bakterilerinin meatusa yerleşmesi"}]},
            {"cells": [{"text": "Prostat Salgısı", "isMasked": False}, {"text": "Kadınlarda mevcut değildir", "isMasked": False}, {"text": "Kimyasal bakterisidal koruma eksikliği", "isMasked": False}]}
        ]),
        make_chain("Asendan Tırmanış Aşamaları", [
            "1. Fekal Rezervuar: Bağırsak florasındaki E. coli perianal bölgeye yayılır.",
            "2. Periüretral Yerleşim: Kısa mesafeyi aşarak eksternal mea çevresine kolonize olur.",
            "3. İntravezikal Giriş: Cinsel aktivite veya türbülans ile 4 cm'lik üretradan mesaneye girer.",
            "4. Sistit Tablosu: Mesane mukozasına tutunarak akut enflamasyon başlatır."
        ]),
        make_recall("Kadınlarda asendan ÜSE gelişimini erkeklere kıyasla kolaylaştıran üç temel anatomik özellik nedir?", "1) Üretranın kısa olması (~4 cm), 2) Eksternal meatusun anüse yakınlığı, 3) Bakterisidal prostat sekresyonlarının bulunmamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Asendan Yayılım", [
            {"text": "Kadınlarda üretranın kısa olması asendan enfeksiyon için majör anatomik yatkınlıktır.", "isLie": False, "explanation": "Doğru. Bakteri tırmanış mesafesi kısadır."},
            {"text": "Perine ve anüse yakınlık periüretral fekal kolonizasyonu kolaylaştırır.", "isLie": False, "explanation": "Doğru. Bulaş kaynağı bağırsak florasıdır."},
            {"text": "Kadınlarda devasa prostat bezinin ürettiği salgılar üretrayı tamamen yıkar.", "isLie": True, "explanation": "Tuzak! Kadınlarda prostat bezi bulunmaz; prostat salgısının olmaması bir yatkınlık unsurudur."},
            {"text": "Asendan yolla gelişen ÜSE'lerin başında Enterobacteriaceae ailesi gelir.", "isLie": False, "explanation": "Doğru. Fekal bakterilerdir."}
        ]),
        make_quiz("Kadınlarda asendan yol ile idrar yolu enfeksiyonunun sık görülmesinin temel anatomik nedeni hangisidir?", [
            {"key": "A", "text": "Üretranın kısa olması, perine ve anüse yakınlığı ve prostat salgısının olmaması", "isCorrect": True, "explanation": "Ders notunda kadın anatomik yatkınlığı bu üç unsurla gerekçelendirilmiştir."},
            {"key": "B", "text": "Kadınlarda böbreklerin mesaneden 2 metre uzakta yerleşmesi", "isCorrect": False, "explanation": "Anatomi dışı ifadedir."},
            {"key": "C", "text": "Kadın idrarının tamamen saf alkolden oluşması", "isCorrect": False, "explanation": "Tıbbi temeli yoktur."},
            {"key": "D", "text": "Kadınlarda mesanenin hiç bulunmaması", "isCorrect": False, "explanation": "Kadında mesane mevcuttur."}
        ])
    ]
    slides.append(make_slide(22, "Asendan Yayılım Mekanizması (%99) ve Kadın Anatomisi", "Asendan rota, kısa üretra, anüse yakınlık ve periüretral kolonizasyon", "Patogenez", s22_narrative, s22_bullets, s22_elements))

    # Slide 23: Hematojen Yayılım Yolu ve Spesifik Mikroorganizmalar
    s23_narrative = (
        "Hematojen yol, üriner sistem enfeksiyonlarının %2'sinden azını oluşturmasına rağmen, altta "
        "yatan hayatı tehdit edici sistemik enfeksiyonların renal tutulumunu temsil eder.\n\n"
        "- **Bakteriyemi Kökeni:** Bakteriler üriner traktusa üretradan değil, vücudun başka bir "
        "bölgesindeki primer enfeksiyon odağından (endokardit, osteomiyelit vb.) kan dolaşımı ile gelir.\n"
        "- **Karakteristik Patojenler:** Bu yolun tipik ve sınav klasiği etkenleri **Staphylococcus aureus, "
        "Salmonella türleri, Candida suşları ve Mycobacterium tuberculosis (Tbc)**'dir.\n"
        "- **Renal Kortikal Tutulum:** Hematojen yayılan bakteriler renal glomerüllere ve kortekse yerleşerek "
        "parankimde multipl mikroapseler (renal kortikal abse / karbunkül) oluşturur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Hematojen yolla ÜSE yapan mikroorganizmalar: S. aureus, Salmonella, Candida ve M. tuberculosis'tir; idrarda S. aureus saptanması bakteriyemi araştırmasını zorunlu kılar!"
    )
    s23_bullets = [
        "Hematojen yol tüm ÜSE'lerin %2'den azını oluşturur.",
        "Tipik etkenler: S. aureus, Salmonella türleri, Candida suşları ve M. tuberculosis.",
        "Bakteriyemi sonrası böbrek korteksinde apseler ve parankim hasarı gelişir."
    ]
    s23_elements = [
        make_cloze("Hematojen yolla böbreğe ulaşarak abse ve enfeksiyon oluşturan klasik Gram pozitif kok Staphylococcus aureus'tur.", "Staphylococcus aureus", "Koagülaz pozitif stafilokok"),
        make_table("Hematojen ÜSE Etkenleri ve Klinik Özellikleri", ["Mikroorganizma", "Primer Kaynak / Giriş", "Renal Patoloji"], [
            {"cells": [{"text": "Staphylococcus aureus", "isMasked": False}, {"text": "Endokardit, kateter bakteriyemisi", "isMasked": True, "hint": "kalp kapakçığı ve damar içi enfeksiyonu"}, {"text": "Renal kortikal mikroapseler (karbunkül)"}]},
            {"cells": [{"text": "Salmonella türleri", "isMasked": False}, {"text": "Gastrointestinal invazyon / tifo", "isMasked": False}, {"text": "Bakteriyemik renal glomerüler ekilim", "isMasked": True, "hint": "kan yoluyla böbreğe yayılım"}]},
            {"cells": [{"text": "Mycobacterium tuberculosis", "isMasked": False}, {"text": "Primer akciğer tüberkülozu odağı", "isMasked": False}, {"text": "Renal tüberküloz ve steril piyüri", "isMasked": False}]}
        ]),
        make_chain("Hematojen Renal Abse Oluşum Zinciri", [
            "1. Primer Odak: Kalp kapağında veya yumuşak dokuda S. aureus enfeksiyonu yerleşir.",
            "2. Bakteriyemi: Bakteriler kan dolaşımına yoğun biçimde dökülür.",
            "3. Renal Filtrasyon: Yüksek kan akımı alan böbrek glomerül ve kapillerlerinde tutulurlar.",
            "4. Karbunkül: Kortekste parankimal harabiyet ve mikroapseler meydana gelir."
        ]),
        make_recall("Hematojen yolla böbreğe ulaşarak ÜSE ve renal apse yapan dört klasik mikroorganizma hangisidir?", "Staphylococcus aureus, Salmonella türleri, Candida suşları ve Mycobacterium tuberculosis'tir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hematojen Yayılım", [
            {"text": "Hematojen yol tüm ÜSE'lerin %2'sinden azını oluşturur.", "isLie": False, "explanation": "Doğru. Asendan yola göre çok nadirdir."},
            {"text": "S. aureus ve Salmonella hematojen yolla böbreği tutan klasik etkenlerdir.", "isLie": False, "explanation": "Doğru. Tipik kan kökenli etkenlerdir."},
            {"text": "İdrarda S. aureus üretilmesi her zaman sadece basit bir dış kontaminasyondur ve önemsizdir.", "isLie": True, "explanation": "Tuzak! İdrarda S. aureus saptanması altta yatan stafilokokal bakteriyemi veya endokardit açısından alarm bulgusudur."},
            {"text": "M. tuberculosis kan yoluyla böbreğe yerleşerek renal tüberküloz yapabilir.", "isLie": False, "explanation": "Doğru. Primer akciğerden hematojen gelir."}
        ]),
        make_quiz("Aşağıdaki mikroorganizmalardan hangisi üriner sisteme HEMATOJEN yolla ulaşarak enfeksiyon ve apse oluşturan klasik etkenlerden biridir?", [
            {"key": "A", "text": "Staphylococcus aureus", "isCorrect": True, "explanation": "Ders notunda hematojen yolun tipik örnekleri S. aureus, candida, salmonella ve M. tuberculosis olarak sıralanmıştır."},
            {"key": "B", "text": "Vibrio cholerae", "isCorrect": False, "explanation": "Kolera bağırsakta kalır, renal tutulum yapmaz."},
            {"key": "C", "text": "Bordetella pertussis", "isCorrect": False, "explanation": "Boğmaca solunum etkenidir."},
            {"key": "D", "text": "Clostridium tetani", "isCorrect": False, "explanation": "Tetanoz toksiniyle sinir sistemini tutar."}
        ])
    ]
    slides.append(make_slide(23, "Hematojen Yayılım Yolu ve Spesifik Mikroorganizmalar", "Hematojen yol (<%2), S. aureus, Salmonella, Candida ve M. tuberculosis", "Patogenez", s23_narrative, s23_bullets, s23_elements))

    # Slide 24: Lenfojen ve Direkt Yayılım Yolları
    s24_narrative = (
        "Asendan ve hematojen rotaların haricinde, üriner traktusa komşu organlardan kaynaklanan "
        "nadir fakat cerrahi önem taşıyan iki yayılım mekanizması daha mevcuttur.\n\n"
        "- **Lenfojen Yayılım:** Rektal ve kolonik lenfatikler ile prostat ve mesane arasında, ya da "
        "periuterin lenfatik pleksuslar ile genitoüriner traktus arasında bakteriyel geçiş olabileceği "
        "çeşitli çalışmalarda ileri sürülmüştür.\n"
        "- **Direkt Yayılma:** Üriner traktusa komşu intraabdominal patolojilerin doğrudan doku sınırlarını "
        "aşarak mesaneye penetre olmasıdır.\n"
        "- **Klinik Nedenler:** İntraperitoneal apseler, İnflamatuar Bağırsak Hastalıkları (özellikle Crohn "
        "hastalığı) ve buna bağlı gelişen **veziko-intestinal veya vezikovajinal fistüller** direkt yayılımın tipik örnekleridir.\n\n"
        "> [!NOTE]\n"
        "> Pnömokolon veya fekalüri (idrarda gaz ve dışkı çıkışı) saptanan bir hastada vezikointestinal fistüle bağlı direkt yayılım düşünülmelidir."
    )
    s24_bullets = [
        "Lenfojen yol rektal, kolonik ve periuterin lenfatik pleksusları kapsar.",
        "Direkt yayılma komşu apseler, İBH ve fistüller üzerinden gerçekleşir.",
        "Vezikointestinal ve vezikovajinal fistüller direkt yayılım örnekleridir."
    ]
    s24_elements = [
        make_cloze("İnflamatuar bağırsak hastalıklarında mesane ile bağırsak arasında gelişen vezikointestinal fistüller direkt yolla ÜSE yapar.", "vezikointestinal", "Mesane ve bağırsak lümenleri arasındaki anormal kanal"),
        make_table("Nadir Yayılım Yolları Karşılaştırması", ["Yayılım Yolu", "Anatomik Güzergah", "Etiyolojik Durum"], [
            {"cells": [{"text": "Lenfojen Yol", "isMasked": False}, {"text": "Kolonik ve periuterin lenfatik kanallar", "isMasked": True, "hint": "lenf damarları üzerinden geçiş"}, {"text": "Pelvik lenfanjit ve komşuluk"}]},
            {"cells": [{"text": "Direkt Yayılım", "isMasked": False}, {"text": "Doku bütünlüğünün delinmesi (fistül)", "isMasked": False}, {"text": "İntraperitoneal apse, Crohn hastalığı, fistül", "isMasked": True, "hint": "apse perforasyonu ve organ birleşimi"}]}
        ]),
        make_chain("Direkt Yayılım ve Fistül Gelişimi", [
            "1. Komşu İnflamasyon: Crohn hastalığı veya divertikülitte bağırsak duvarı perfore olur.",
            "2. Apse Formasyonu: Pelviste mezenterik/perivezikal apse odağı gelişir.",
            "3. Fistül Traktı: Mesane duvarı eriyerek lümenler arasında vezikointestinal fistül açılır.",
            "4. Masif İnokülasyon: Bağırsak içeriği doğrudan mesaneye dökülerek polimikrobiyal ÜSE başlatır."
        ]),
        make_recall("Hangi cerrahi ve gastrointestinal patolojiler direkt yayılma yoluyla üriner sistem enfeksiyonuna yol açabilir?", "İntraperitoneal apseler, inflamatuar barsak hastalıkları (Crohn), vezikointestinal ve vezikovajinal fistüllerdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Lenfojen ve Direkt Yayılım", [
            {"text": "Rektal ve periuterin lenfatiklerle lenfojen yayılım görülebilir.", "isLie": False, "explanation": "Doğru. Literatürde bildirilen nadir yoldur."},
            {"text": "İnflamatuar barsak hastalıkları ve fistüller direkt yayılma ile enfeksiyon yapabilir.", "isLie": False, "explanation": "Doğru. Doku erozyonu ile oluşur."},
            {"text": "Vezikovajinal fistülü olan hastada idrar yolu tamamen mikroptan yalıtılmış kalır.", "isLie": True, "explanation": "Tuzak! Fistül vajinal floranın doğrudan mesaneye akmasına ve ağır ÜSE'ye yol açar."},
            {"text": "İntraperitoneal apseler komşuluk yoluyla mesaneye drene olabilir.", "isLie": False, "explanation": "Doğru. Direkt penetrasyon yapabilir."}
        ]),
        make_quiz("Aşağıdakilerden hangisi üriner sisteme DİREKT YAYILMA yolu ile enfeksiyon bulaşmasına yol açan durumlardan biridir?", [
            {"key": "A", "text": "İntraperitoneal apseler ve vezikointestinal fistüller", "isCorrect": True, "explanation": "Ders notunda intraperitoneal apseler, İBH ve vezikovaginal-vezikointestinal fistüller direkt yayılma örnekleri olarak verilmiştir."},
            {"key": "B", "text": "Üst solunum yolu viral nezlesi", "isCorrect": False, "explanation": "Solunum yolu mesaneye direkt komşu değildir."},
            {"key": "C", "text": "Ayak tırnağında mantar enfeksiyonu", "isCorrect": False, "explanation": "Direkt yayılım oluşturmaz."},
            {"key": "D", "text": "Kulak zarının delinmesi", "isCorrect": False, "explanation": "Mesaneyle ilişkisizdir."}
        ])
    ]
    slides.append(make_slide(24, "Lenfojen ve Direkt Yayılım Yolları", "Rektal/periuterin lenfatikler, intraperitoneal apseler ve vezikal fistüller", "Patogenez", s24_narrative, s24_bullets, s24_elements))

    # Slide 25: Konak Savunma Mekanizmaları: İdrarın Biyokimyasal Özellikleri
    s25_narrative = (
        "İdrar sadece vücuttan atılan bir atık sıvı değil, taşıdığı sert fizikokimyasal parametreler "
        "sayesinde mikroorganizmaların çoğalmasını engelleyen doğal bir antibakteriyel bariyerdir.\n\n"
        "- **Dinamik İdrar Akımı:** Düzenli ve tam mesane boşalması ile sağlanan kesintisiz hidrostatik akım, "
        "üroepitele yapışamayan bakterileri mekanik olarak dışarı süpürür.\n"
        "- **Fizikokimyasal Ekstremler:** İdrarın sahip olduğu **yüksek ozmolarite**, **yüksek üre konsantrasyonu** "
        "ve **düşük pH seviyesi (asidik idrar)** bakteriyel enzim sistemlerini ve hücre zarı stabilitesini bozar.\n"
        "- **Bakterisidal Çevre:** Bu ekstrem kimyasal koşullar, üropatojenlerin logaritmik üreme fazına "
        "geçmesini önleyerek idrar lümeninde çoğalmalarını sınırlar.\n\n"
        "> [!IMPORTANT]\n"
        "> İdrarın antibakteriyel kimyasal gücü: Yüksek ozmolarite, yüksek üre konsantrasyonu ve düşük asidik pH'dan kaynaklanır."
    )
    s25_bullets = [
        "Normal idrar akımı bakterileri mekanik olarak yıkayıp dışarı atar.",
        "Yüksek ozmolarite bakteriyel hücre duvarında osmotik stres yaratır.",
        "Yüksek üre konsantrasyonu ve düşük pH bakterisidal etki gösterir."
    ]
    s25_elements = [
        make_cloze("İdrarın bakteriyel üremeyi engelleyen fiziko-kimyasal özellikleri yüksek üre, yüksek ozmolarite ve düşük pH seviyesidir.", "düşük pH", "İdrarın asidik karakteri"),
        make_table("İdrarın Doğal Savunma Parametreleri", ["Savunma Parametresi", "Biyofiziksel Durum", "Bakteri Üzerindeki Etkisi"], [
            {"cells": [{"text": "Yıkama Etkisi (Washout)", "isMasked": False}, {"text": "Düzenli miksiyon ve laminar akım", "isMasked": True, "hint": "idrarın mekanik süpürme gücü"}, {"text": "Tutunamayan bakterilerin atılması"}]},
            {"cells": [{"text": "Ozmolarite ve Üre", "isMasked": False}, {"text": "Yüksek konsantrasyon", "isMasked": False}, {"text": "Bakteriyel dehidratasyon ve enzim denatürasyonu", "isMasked": True, "hint": "osmotik stres ve protein bozulması"}]},
            {"cells": [{"text": "İdrar pH'sı", "isMasked": False}, {"text": "Düşük (asidik çevre)", "isMasked": False}, {"text": "Bakteri çoğalmasının baskılanması", "isMasked": False}]}
        ]),
        make_chain("Mekanik ve Kimyasal Yıkama Zinciri", [
            "1. Filtrasyon: Glomerüllerden atılan idrar tübüllerde konsantre edilir.",
            "2. Kimyasal Zırh: Yüksek üre, yüksek ozmolarite ve düşük pH ile donatılır.",
            "3. Lüminal Akış: Üreter peristaltizmi ile mesaneye kesintisiz iletilir.",
            "4. Miksiyonel Yıkama: Mesanenin tam kasılmasıyla lümendeki tüm bakteriler tahliye edilir."
        ]),
        make_recall("İdrarın bakteriyel çoğalmayı zorlaştıran üç temel fizikokimyasal özelliği nedir?", "Yüksek ozmolaritesi, yüksek üre konsantrasyonu ve düşük pH (asidite) seviyesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İdrar Savunması", [
            {"text": "İdrar akımının mekanik yıkama etkisi konak savunmasının temelidir.", "isLie": False, "explanation": "Doğru. Bakterileri süpürür."},
            {"text": "Yüksek üre konsantrasyonu ve düşük pH bakterisidal etki gösterir.", "isLie": False, "explanation": "Doğru. Fizikokimyasal bariyerdir."},
            {"text": "İdrarın en ideal savunması saf şekerli, nötr pH'lı ve tamamen durgun olmasıdır.", "isLie": True, "explanation": "Tuzak! Şekerli ve durgun idrar bakteri besiyeridir; koruyucu olan yüksek üre, düşük pH ve akımdır."},
            {"text": "Yüksek ozmolarite bakteriler üzerinde osmotik baskı oluşturur.", "isLie": False, "explanation": "Doğru. Üremeyi engeller."}
        ]),
        make_quiz("Aşağıdakilerden hangisi idrarın konak savunmasında rol oynayan doğal fiziko-kimyasal özelliklerinden biri DEĞİLDİR?", [
            {"key": "A", "text": "Yüksek üre konsantrasyonu", "isCorrect": False, "explanation": "Doğal savunma özelliğidir."},
            {"key": "B", "text": "Düşük pH seviyesi (asidite)", "isCorrect": False, "explanation": "Doğal savunma özelliğidir."},
            {"key": "C", "text": "Yüksek ozmolarite", "isCorrect": False, "explanation": "Doğal savunma özelliğidir."},
            {"key": "D", "text": "Yüksek glukoz konsantrasyonu ve alkali durağanlık", "isCorrect": True, "explanation": "Yüksek glukoz ve durağanlık savunma değil, bakteriyel çoğalmayı hızlandıran patolojik zeminlerdir."}
        ])
    ]
    slides.append(make_slide(25, "Konak Savunma Mekanizmaları: İdrarın Biyokimyasal Özellikleri", "İdrar akımı, yüksek ozmolarite, yüksek üre ve düşük pH savunması", "Konak Savunması", s25_narrative, s25_bullets, s25_elements))

    # Slide 26: Tamm-Horsfall Proteini ve Prostat Sıvısının Rolü
    s26_narrative = (
        "Biyokimyasal savunmanın en özelleşmiş moleküler kalkanları böbrek kökenli Tamm-Horsfall "
        "proteini ile erkek genital sistemine özgü prostat sekresyonlarıdır.\n\n"
        "- **Tamm-Horsfall Proteini (Üromodulin):** Henle kulpunun çıkan kalın kolundaki epitelyal hücreler "
        "tarafından lümene bol miktarda salgılanan özgün bir glikoproteindir.\n"
        "- **Yalancı Hedef Tuzağı:** Tamm-Horsfall proteinleri yoğun mannoz kalıntıları taşır. Üropatojen "
        "E. coli'nin Tip 1 fimbriyaları üroepitelyum yerine **Tamm-Horsfall proteinine yapışır**; böylece "
        "bakteri epitele tutunamadan idrarla dışarı sürüklenir.\n"
        "- **Prostatik Bakterisidal Sıvı:** Erkeklerde prostat bezinden salgılanan yüksek konsantrasyondaki "
        "serbest çinko iyonları ve antimikrobiyal peptidler bakterilerin hücre zarını parçalar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Tamm-Horsfall proteini böbrek kökenlidir; bakteriyel fimbriyaları bağlayarak üroepitele yapışmasını engelleyen doğal bir yem (tuzak) görevi görür."
    )
    s26_bullets = [
        "Tamm-Horsfall proteini (üromodulin) Henle kulpundan salgılanan koruyucu glikoproteindir.",
        "Mannoz kalıntıları E. coli fimbriyalarını bağlayarak epitele tutunmasını önler.",
        "Prostat sıvısı yüksek çinko içeriğiyle bakterisidal sterilizasyon sağlar."
    ]
    s26_elements = [
        make_cloze("Böbrek kökenli Tamm-Horsfall proteini bakterilerin üroepitelyal hücrelere tutunmasını engelleyen doğal glikoproteindir.", "Tamm-Horsfall", "Üromodulin olarak da bilinen renal savunma proteini"),
        make_table("Özelleşmiş Moleküler Savunma Faktörleri", ["Faktör", "Üretim Yeri", "Savunma Mekanizması"], [
            {"cells": [{"text": "Tamm-Horsfall Proteini", "isMasked": False}, {"text": "Böbrek (Henle çıkan kalın kolu)", "isMasked": True, "hint": "renal tübüler orijin"}, {"text": "Bakteriyel fimbriyaları bağlayıp epitele adezyonu bloke etme"}]},
            {"cells": [{"text": "Prostat Sıvısı", "isMasked": False}, {"text": "Prostat asiner epiteli", "isMasked": False}, {"text": "Çinko iyonları ile bakterisidal membran lizisi", "isMasked": True, "hint": "çinko aracılı bakteri öldürme"}]}
        ]),
        make_chain("Tamm-Horsfall Tuzak Mekanizması", [
            "1. Sentez: Henle çıkan kulpundan bol miktarda üromodulin salgılanır.",
            "2. Mannoz Sunumu: Protein zincirindeki mannoz molekülleri lümende serbestçe yüzer.",
            "3. Yarışmalı İnhibisyon: E. coli'nin Tip 1 fimbriyaları ürotelyum yerine bu proteine kilitlenir.",
            "4. Tahliye: Kompleks halinde idrar akımı ile dış ortama atılır."
        ]),
        make_recall("Böbrek tübüllerinden salgılanarak bakterilerin üroepitele tutunmasını yarışmalı olarak engelleyen koruyucu glikoprotein hangisidir?", "Tamm-Horsfall proteinidir (üromodulin)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tamm-Horsfall ve Prostat", [
            {"text": "Tamm-Horsfall proteini böbrek kökenli doğal bir koruyucu glikoproteindir.", "isLie": False, "explanation": "Doğru. Henle kulpundan salgılanır."},
            {"text": "Bakterilerin üroepitelyal hücrelere tutunmasını engeller.", "isLie": False, "explanation": "Doğru. Fimbriyaları bağlar."},
            {"text": "Tamm-Horsfall proteini bakterilere enerji veren ve çoğalmalarını 100 kat artıran bir toksindir.", "isLie": True, "explanation": "Tuzak! Tamm-Horsfall bir toksin değil, konak savunmasının en önemli koruyucu proteinidir."},
            {"text": "Erkeklerde prostat salgısının bakterisidal özelliği ÜSE'ye karşı koruyucudur.", "isLie": False, "explanation": "Doğru. Çinkodan zengin antibakteriyel sıvıdır."}
        ]),
        make_quiz("Böbrek kaynaklı olup bakterilerin üroepitelyal hücrelere yapışmasını önleyerek idrarla atılmasını sağlayan konak savunma proteini hangisidir?", [
            {"key": "A", "text": "Tamm-Horsfall proteini", "isCorrect": True, "explanation": "Ders notunda konağın savunma mekanizmaları arasında böbrek kökenli Tamm-Horsfall proteinleri açıkça vurgulanmıştır."},
            {"key": "B", "text": "Bence Jones proteini", "isCorrect": False, "explanation": "Multipl miyelom hafif zinciridir."},
            {"key": "C", "text": "C-reaktif protein (CRP)", "isCorrect": False, "explanation": "Karaciğer akut faz reaktanıdır."},
            {"key": "D", "text": "Miyoglobin", "isCorrect": False, "explanation": "Kas yıkım ürünüdür."}
        ])
    ]
    slides.append(make_slide(26, "Tamm-Horsfall Proteini ve Prostat Sıvısının Rolü", "Tamm-Horsfall glikoproteini, fimbriya blokajı ve bakterisidal prostat salgısı", "Konak Savunması", s26_narrative, s26_bullets, s26_elements))

    # Slide 27: Etkene Ait Virülans Faktörleri: Adezyon ve Fimbriyalar
    s27_narrative = (
        "Bir mikroorganizmanın idrarın mekanik yıkama gücüne direnerek üriner traktusta enfeksiyon "
        "başlatabilmesi, sahip olduğu özgül virülans faktörlerine bağlıdır.\n\n"
        "- **Üroepitelyal Adherens:** Üropatojenlerin (özellikle E. coli) en kritik ve birinci basamak "
        "virülans özelliği **üroepitelyal hücrelere artmış adherens (tutunma)** yeteneğidir.\n"
        "- **Fimbriya / Pili Sistemleri:** Bakteri yüzeyinden uzanan fimbriyalar iki ana sınıfa ayrılır:\n"
        "  - **Tip 1 Fimbriya:** Mesane mukozasındaki mannoz kalıntılarına bağlanır; sistit patogenezinde rol oynar.\n"
        "  - **P Fimbriyaları (Pap pili):** Renal tübül epiteli ve eritrositlerdeki galaktoz-alfa-(1-4)-galaktoz "
        "reseptörlerine kilitlenir; **akut pyelonefrit etkeni E. coli suşlarının vazgeçilmez işaretidir**.\n"
        "- **Sonuç:** Fimbriyalar sayesinde bakteriler idrar akımıyla sürüklenmeyerek dokuya demir atar.\n\n"
        "> [!IMPORTANT]\n"
        "> P fimbriyası pyelonefrit patogenezinin kilit faktörüdür; böbrek parankimindeki spesifik digalaktozid reseptörlerine yapışmayı sağlar."
    )
    s27_bullets = [
        "Üroepitelyal hücrelere adherens (tutunma) en temel virülans basamağıdır.",
        "Tip 1 fimbriyalar mesanede sistit oluşumunu başlatır.",
        "P fimbriyaları renal parankime tutunarak akut pyelonefrite yol açar."
    ]
    s27_elements = [
        make_cloze("Üropatojen E. coli'nin böbrek parankimine tutunarak pyelonefrit yapmasını sağlayan kilit virülans yapısı P fimbriyalarıdır.", "P fimbriyaları", "Pyelonefrit ile ilişkili Pap pili yapıları"),
        make_table("Üropatojen E. coli Fimbriya Tipleri", ["Fimbriya Tipi", "Bağlandığı Reseptör", "Klinik Tablo"], [
            {"cells": [{"text": "Tip 1 Fimbriya (Mannoz Duyarlı)", "isMasked": False}, {"text": "Ürotelyal mannoz kalıntıları", "isMasked": True, "hint": "mesane yüzey şekeri"}, {"text": "Akut sistit (alt sistem invazyonu)"}]},
            {"cells": [{"text": "P Fimbriyası (Mannoz Dirençli)", "isMasked": False}, {"text": "Gal-alfa(1-4)-Gal reseptörleri", "isMasked": False}, {"text": "Akut pyelonefrit (üst sistem invazyonu)", "isMasked": True, "hint": "böbrek iltihabı ve parankim hasarı"}]}
        ]),
        make_chain("Adezyon ve Dokusal Demir Atma Zinciri", [
            "1. Yaklaşma: Bakteri periüretral alandan mesane lümenine girer.",
            "2. Reseptör Tanıma: Fimbriya uç proteinleri ürotelyum glikoproteinlerine yönelir.",
            "3. Kovalent Olmayan Kenetlenme: Fimbriyalar reseptörlere kilitlenerek bakteriyi sabitler.",
            "4. Yıkamaya Direnç: Miksiyon akımına rağmen bakteri dokuda kalır ve kolonileşir."
        ]),
        make_recall("Üropatojen E. coli'nin böbrek parankimine yapışmasını sağlayarak pyelonefrite yol açan fimbriya türü nedir?", "P fimbriyasıdır (Pap pili)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bakteriyel Adezyon", [
            {"text": "Üroepitelyal hücrelere artmış adherens bakterinin temel virülans faktörüdür.", "isLie": False, "explanation": "Doğru. Tutunma olmadan enfeksiyon başlayamaz."},
            {"text": "P fimbriyaları böbrek dokusuna bağlanarak pyelonefrit gelişiminde rol oynar.", "isLie": False, "explanation": "Doğru. Klasik pyelonefrit virülansıdır."},
            {"text": "Bakteriler üroepitele asla yapışamaz, idrar içinde havada uçarak uzaktan zehir salgılar.", "isLie": True, "explanation": "Tuzak! Bakteriler fimbriyaları ile üroepitele sıkıca tutunmak zorundadır, aksi halde idrarla atılırlar."},
            {"text": "Tip 1 fimbriyalar mannoz kalıntılarına bağlanarak sistit başlatabilir.", "isLie": False, "explanation": "Doğru. Mesane kolonizasyonu yapar."}
        ]),
        make_quiz("Üropatojen E. coli'nin böbrek parankimine tutunmasında ve akut pyelonefrit gelişiminde rol oynayan spesifik virülans faktörü hangisidir?", [
            {"key": "A", "text": "P fimbriyası (Pap pili)", "isCorrect": True, "explanation": "P fimbriyası digalaktozid reseptörlerine bağlanarak üst üriner sistem invazyonunu ve pyelonefriti sağlar."},
            {"key": "B", "text": "Hücre zarı kolesterolü", "isCorrect": False, "explanation": "Bakteri membranında kolesterol bulunmaz."},
            {"key": "C", "text": "Çekirdek zarı porları", "isCorrect": False, "explanation": "Bakteriler prokaryottur, çekirdek zarı yoktur."},
            {"key": "D", "text": "Mitokondriyal krista", "isCorrect": False, "explanation": "Bakterilerde mitokondri bulunmaz."}
        ])
    ]
    slides.append(make_slide(27, "Etkene Ait Virülans Faktörleri: Adezyon ve Fimbriyalar", "Bakteriyel adherens, Tip 1 fimbriya ve pyelonefrit etkeni P fimbriyası", "Virülans Faktörleri", s27_narrative, s27_bullets, s27_elements))

    # Slide 28: İnvazyon, Toksinler ve Endotoksinin Peristaltizme Etkisi
    s28_narrative = (
        "Üropatojen bakteriler adherens sağladıktan sonra doku hasarı oluşturmak ve konağın savunma "
        "hatlarını felç etmek üzere çeşitli toksinler ve enzimler salgılarlar.\n\n"
        "- **Kapsül Kalkanı:** Bakteriyel kapsül (K antijeni), polimorfonükleer lökositlerin fagositozundan "
        "korunma sağlar ve serumun bakterisidal kompleman aktivitesine direnç kazandırır.\n"
        "- **Doku Yıkımı ve Besin Sağlama:** Salgılanan **hemolizin** ve sitotoksik nekrotizan faktör "
        "tip 1 (CNF-1), konak epitelini lize ederek doku invazyonunu kolaylaştırır ve **aerobaktin** "
        "aracılığıyla serbest demiri çeker.\n"
        "- **Üreteral Peristaltizmin Durdurulması:** Gram negatif bakterilerin salgıladıkları **endotoksin "
        "(LPS)**, üreter düz kaslarında tonus kaybı ve peristaltizm azalması yaratarak idrar akımını "
        "felç eder ve bakterilerin böbreğe tırmanışını hızlandırır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Gram negatif bakterilerin endotoksini üreteral peristaltizmi azaltarak fonksiyonel staz yaratır ve asendan tırmanışı kolaylaştırır."
    )
    s28_bullets = [
        "Kapsül (K antijeni) lökosit fagositozundan korunma ve serum direncidir.",
        "Hemolizin ve aerobaktin doku invazyonu ve demir teminini sağlar.",
        "Endotoksin üreteral peristaltizmi azaltarak bakterinin tırmanışını hızlandırır."
    ]
    s28_elements = [
        make_cloze("Gram negatif bakterilerin salgıladığı endotoksin üreteral peristaltizmin azaltılması yoluyla asendan yayılımı kolaylaştırır.", "endotoksin", "Bakteri duvarındaki lipopolisakkarit (LPS) toksini"),
        make_table("Üropatojen Virülans Toksinleri ve Etkileri", ["Virülans Faktörü", "Biyolojik Fonksiyonu", "Patolojik Sonucu"], [
            {"cells": [{"text": "Bakteriyel Kapsül", "isMasked": False}, {"text": "Lökosit fagositozundan korunma", "isMasked": True, "hint": "akyuvarların yutmasını engelleme"}, {"text": "Kompleman ve serum litik etkisine direnç"}]},
            {"cells": [{"text": "Hemolizin ve Aerobaktin", "isMasked": False}, {"text": "Eritrosit lizisi ve demir yakalama", "isMasked": False}, {"text": "Doku invazyonu ve metabolik büyüme", "isMasked": True, "hint": "dokuyu eritip demir temin etme"}]},
            {"cells": [{"text": "Gram (-) Endotoksin", "isMasked": False}, {"text": "Üreter düz kas peristaltizmini felç etme", "isMasked": False}, {"text": "Üreteral fonksiyonel staz ve böbreğe tırmanış", "isMasked": True, "hint": "idrar kanalı kasılmasının durması"}]}
        ]),
        make_chain("Endotoksin ve Asendan Tırmanış", [
            "1. Mesanede Çoğalma: Gram negatif bakteriler lümende endotoksin (LPS) salgılar.",
            "2. Üreter Düz Kas Hasarı: Endotoksin üreterik pacemaker aktivitesini baskılar.",
            "3. Peristaltik Durgunluk: Üreter dalgaları yavaşlar ve dilatasyon gelişir.",
            "4. Ters Akım / Asendan Göç: Bakteriler yerçekimi ve akım engeli olmadan böbreğe tırmanır."
        ]),
        make_recall("Gram negatif üropatojenlerin salgıladığı endotoksinin üreter fonksiyonları üzerindeki spesifik etkisi nedir?", "Üreteral peristaltizmi (kasılma hareketini) azaltarak fonksiyonel staz yaratır ve bakterilerin böbreğe tırmanışını kolaylaştırır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Virülans ve Toksinler", [
            {"text": "Bakteriyel kapsül lökosit fagositozundan korunmada rol oynar.", "isLie": False, "explanation": "Doğru. Fagositozu engeller."},
            {"text": "Hemolizin ve aerobaktin doku invazyonunu ve demir alımını kolaylaştırır.", "isLie": False, "explanation": "Doğru. İnvazyon faktörleridir."},
            {"text": "Gram negatif endotoksin üreterleri 100 kat daha hızlı kastırarak bakterileri derhal dışarı fırlatır.", "isLie": True, "explanation": "Tuzak! Endotoksin üreteral peristaltizmi HIZLANDIRMAZ, tam tersine AZALTARAK staz ve asendan tırmanış sağlar."},
            {"text": "Serumun bakterisidal etkisine direnç üropatojenik suşların özelliğidir.", "isLie": False, "explanation": "Doğru. Komplemana direnç gösterirler."}
        ]),
        make_quiz("Gram negatif üropatojenlerin üreteral peristaltizmi azaltarak bakterilerin böbreğe asendan tırmanışını kolaylaştıran virülans bileşeni hangisidir?", [
            {"key": "A", "text": "Gram negatif bakterilerin salgıladıkları endotoksin", "isCorrect": True, "explanation": "Ders notunda etkene ait virülans faktörleri arasında 'üreteral peristaltizmin azaltılması (gram negatif etkenlerin salgıladıkları endotoksin)' açıkça belirtilmiştir."},
            {"key": "B", "text": "Penisilin bağlayan proteinler (PBP)", "isCorrect": False, "explanation": "Hücre duvarı sentez enzimidir."},
            {"key": "C", "text": "Katalaz enzimi", "isCorrect": False, "explanation": "Peristaltizmi etkilemez."},
            {"key": "D", "text": "DNA giraz enzimi", "isCorrect": False, "explanation": "Bakteriyel replikasyon enzimidir."}
        ])
    ]
    slides.append(make_slide(28, "İnvazyon, Toksinler ve Endotoksinin Peristaltizme Etkisi", "Kapsül fagositoz direnci, hemolizin, aerobaktin ve endotoksinin peristaltizmi azaltması", "Virülans Faktörleri", s28_narrative, s28_bullets, s28_elements))

    # Slide 29: Üçüncü Bölüm Özeti: Bulaş Yolları ve Patojen-Konak Dengesi
    s29_narrative = (
        "Üriner sistem enfeksiyonunun başlangıcı, bakterinin virülans donanımı ile konağın anatomik "
        "ve fizyolojik savunma engelleri arasındaki dinamik bir mücadeledir.\n\n"
        "- **Bulaş Yollarının Dağılımı:** Vakaların %99'u asendan yolla oluşur; hematojen yol (<%2) ise "
        "S. aureus, Salmonella, Candida ve Tbc gibi spesifik etkenlerle kortikal apseler yapar.\n"
        "- **Konak Savunma Kalkanları:** İdrarın mekanik akımı, yüksek ozmolarite, yüksek üre konsantrasyonu, "
        "düşük pH'sı, Henle kulpundan salgılanan Tamm-Horsfall proteini ve erkeklerde prostat salgısıdır.\n"
        "- **Bakteriyel Üstünlük Donanımları:** Epitelyal tutunmayı sağlayan fimbriyalar (Tip 1 ve P pili), "
        "fagositozu önleyen kapsül ve üreteral peristaltizmi felç eden Gram negatif endotoksindir.\n\n"
        "> [!IMPORTANT]\n"
        "> P fimbriyası ile böbreğe tutunan ve endotoksin ile üreter peristaltizmini durduran bakteriler konak direncini kırarak pyelonefrit oluşturur."
    )
    s29_bullets = [
        "Asendan yol %99 ile ana rotadır; hematojen yol <%2 olup apse yapar.",
        "Konak: İdrar akımı, üre, ozmolarite, düşük pH, Tamm-Horsfall ve prostat sıvısı.",
        "Patojen: Fimbriya (adezyon), kapsül (fagositoz direnci) ve endotoksin (peristaltizm kaybı)."
    ]
    s29_elements = [
        make_cloze("Konağın moleküler tuzağı Tamm-Horsfall proteini iken bakterinin pyelonefrit tutunma silahı P fimbriyasıdır.", "P fimbriyası", "Böbrek reseptörlerine bağlanan bakteriyel fimbriya"),
        make_table("Patojen vs Konak Savunma Dengesi", ["Konak Savunma Mekanizması", "Bakteriyel Virülans Yanıtı", "Sonuç"], [
            {"cells": [{"text": "Laminar idrar akımı ve yıkama", "isMasked": False}, {"text": "Fimbriyalarla (Tip 1 ve P pili) sıkı adherens", "isMasked": True, "hint": "üroepitele tutunma uzantıları"}, {"text": "Bakterinin idrarla atılamayıp dokuda kalması"}]},
            {"cells": [{"text": "Lökosit fagositozu ve kompleman", "isMasked": False}, {"text": "Kapsül polisakkaritleri (K antijeni)", "isMasked": False}, {"text": "Fagositozdan kaçış ve doku invazyonu", "isMasked": True, "hint": "akyuvarlar tarafından öldürülememe"}]},
            {"cells": [{"text": "Üreter peristaltik boşalması", "isMasked": False}, {"text": "Endotoksin ile peristaltizmin azaltılması", "isMasked": False}, {"text": "Böbreğe serbest asendan tırmanış", "isMasked": False}]}
        ]),
        make_recall("Gram negatif bakterilerin üreter hareketlerini bozarak asendan yayılımı kolaylaştıran yapısal bileşeni nedir?", "Salgıladıkları endotoksindir (üreteral peristaltizmi azaltır)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Patojen-Konak Dengesi", [
            {"text": "Asendan yol tüm ÜSE'lerin yaklaşık %99'unu oluşturur.", "isLie": False, "explanation": "Doğru. Ezici ana yoldur."},
            {"text": "Tamm-Horsfall proteini bakterilerin üroepitele tutunmasını engelleyen renal bir savunmadır.", "isLie": False, "explanation": "Doğru. Koruyucu glikoproteindir."},
            {"text": "S. aureus ve Salmonella asendan yolla mesaneden yukarı tırmanan tipik bağırsak etkenleridir.", "isLie": True, "explanation": "Tuzak! S. aureus ve Salmonella asendan değil, HEMATOJEN yolla kana ve böbreğe ulaşan etkenlerdir."},
            {"text": "Gram negatif bakterilerin endotoksini üreter peristaltizmini azaltır.", "isLie": False, "explanation": "Doğru. Asendan göçü kolaylaştırır."}
        ]),
        make_quiz("Aşağıdakilerden hangisi patojen bakterilerin konak savunmasını aşmak için kullandığı virülans faktörlerinden biri DEĞİLDİR?", [
            {"key": "A", "text": "Böbrek kaynaklı Tamm-Horsfall proteini salgılamak", "isCorrect": True, "explanation": "Tamm-Horsfall proteini bakteriyel bir virülans faktörü değil, KONAĞIN (böbreğin) ürettiği koruyucu bir savunma glikoproteindir."},
            {"key": "B", "text": "Üroepitelyal hücrelere tutunmayı sağlayan fimbriyalar taşımak", "isCorrect": False, "explanation": "Bakteriyel virülanstır."},
            {"key": "C", "text": "Lökosit fagositozundan koruyan kapsül üretmek", "isCorrect": False, "explanation": "Bakteriyel virülanstır."},
            {"key": "D", "text": "Üreteral peristaltizmi azaltan endotoksin salgılamak", "isCorrect": False, "explanation": "Bakteriyel virülanstır."}
        ])
    ]
    slides.append(make_slide(29, "Üçüncü Bölüm Özeti: Bulaş Yolları ve Patojen-Konak Dengesi", "Asendan rota, konak savunma faktörleri ve bakteriyel virülans silahları", "Konsolidasyon", s29_narrative, s29_bullets, s29_elements))

    # Slide 30: [TEKRAR SAYFASI - CHECKPOINT 3] Bulaş Yolları, Savunma ve Virülans
    s30_narrative = (
        "Bu tekrar sayfasında 3. Bölümün omurgasını oluşturan yayılım rotaları, konağın kimyasal "
        "kalkanları ve bakteriyel virülans faktörlerini konsolide ediyoruz.\n\n"
        "- **Yayılım Yolları:** Asendan yol %99 ile tartışmasız liderdir ve kadın anatomisiyle "
        "(kısa üretra, anüse yakınlık) tetiklenir. Hematojen yol (<%2) ise S. aureus, Salmonella, Tbc ve Candida ile ilişkilidir.\n"
        "- **Konağın Kalkanları:** İdrar akımının mekanik yıkaması; yüksek üre, yüksek ozmolarite, düşük pH; "
        "böbrekten salgılanıp fimbriyaları bağlayan **Tamm-Horsfall proteini** ve bakterisidal prostat sıvısıdır.\n"
        "- **Etkenin Silahları:** Dokuya yapışan fimbriyalar (Tip 1 ve P pili), fagositozu engelleyen kapsül, "
        "demir çeken aerobaktin ve **üreteral peristaltizmi felç eden endotoksindir**.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Hematojen etkenler (S. aureus, Salmonella, Tbc, Candida); koruyucu protein (Tamm-Horsfall); peristaltizmi durduran faktör (endotoksin) 3. Bölümün en kritik sınav triadıdır!"
    )
    s30_bullets = [
        "Asendan yol %99; hematojen yol S. aureus, Salmonella, Candida, Tbc (<%2).",
        "Tamm-Horsfall proteini böbrek kökenlidir ve fimbriyaları bağlar.",
        "Gram (-) endotoksin üreteral peristaltizmi azaltarak böbreğe tırmanışı sağlar."
    ]
    s30_elements = [
        make_cloze("Hematojen yolla böbreğe ulaşarak enfeksiyon ve apse yapan tipik mikroorganizmalardan biri Salmonella türleridir.", "Salmonella", "Gastrointestinal kaynaklı hematojen bakteri"),
        make_table("3. Bölüm Büyük Tekrar Tablosu", ["Bileşen", "Kritik Tıbbi Örnek", "Patofizyolojik Mesaj"], [
            {"cells": [{"text": "Bulaş Rotaları", "isMasked": False}, {"text": "Asendan (%99) vs Hematojen (<%2)", "isMasked": True, "hint": "en sık ve kan yoluyla oranlar"}, {"text": "Asendan bağırsaktan; hematojen bakteriyemiden"}]},
            {"cells": [{"text": "Hematojen Etkenler", "isMasked": False}, {"text": "S. aureus, Salmonella, Candida, Tbc", "isMasked": False}, {"text": "Renal kortikal abse ve sistemik yayılım", "isMasked": True, "hint": "böbrekte iltihap odakları"}]},
            {"cells": [{"text": "Konak Kalkanı", "isMasked": False}, {"text": "Tamm-Horsfall proteini ve prostat sıvısı", "isMasked": True, "hint": "üromodulin ve çinko salgısı"}, {"text": "Yarışmalı fimbriya blokajı ve bakterisidal etki"}]},
            {"cells": [{"text": "Bakteriyel Toksin", "isMasked": False}, {"text": "Gram (-) endotoksin", "isMasked": False}, {"text": "Üreteral peristaltizmin azaltılması", "isMasked": True, "hint": "idrar kanalının motor fonksiyon kaybı"}]}
        ]),
        make_chain("Bölüm 3 Kardinal Mekanizma Özeti", [
            "1. Asendan Giriş: Fekal etkenler kısa kadın üretrasından %99 oranında tırmanır.",
            "2. Moleküler Tuzak: Normal böbrek Tamm-Horsfall proteini salgılayarak fimbriyaları bağlamaya çalışır.",
            "3. Patojen Karşı Hamlesi: P fimbriyası taşıyan suşlar endotoksin ile üreter kasılmalarını durdurur.",
            "4. Üst Sistem İnvazyonu: Bakteri böbrek parankimine ulaşarak pyelonefriti başlatır."
        ]),
        make_recall("Hematojen yolla böbreğe ekilen etkenler ile asendan yolla gelen etkenlerin genel oransal dağılımı nasıldır?", "Asendan yol vakaların yaklaşık %99'unu oluştururken, hematojen yol tüm ÜSE'lerin %2'sinden azını oluşturur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 3. Bölüm Konsolidasyonu", [
            {"text": "Asendan yol ÜSE'lerin %99'unu oluşturan en önemli bulaş yoludur.", "isLie": False, "explanation": "Doğru. Temel yayılım yoludur."},
            {"text": "Tamm-Horsfall proteini böbrek kökenli olup fimbriyaların epitele tutunmasını engeller.", "isLie": False, "explanation": "Doğru. Koruyucu glikoproteindir."},
            {"text": "Gram negatif bakterilerin endotoksini üreteral peristaltizmi artırarak bakterileri böbrekten uzaklaştırır.", "isLie": True, "explanation": "Tuzak! Endotoksin üreteral peristaltizmi AZALTIR ve bakterilerin böbreğe tırmanmasını kolaylaştırır."},
            {"text": "Hematojen yol S. aureus, Candida, Salmonella ve M. tuberculosis ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Klasik hematojen gruptur."}
        ]),
        make_quiz("3. Bölümün temel kazanımlarına göre aşağıdaki patogenez ifadelerinden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Gram negatif bakterilerin endotoksini üreteral peristaltizmi artırarak enfeksiyonu önler", "isCorrect": True, "explanation": "Kesinlikle yanlış! Endotoksin peristaltizmi AZALTARAK idrar stazı yaratır ve bakterinin böbreğe asendan tırmanışını kolaylaştırır."},
            {"key": "B", "text": "Hematojen yolla gelen S. aureus böbrek korteksinde apse oluşturabilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Tamm-Horsfall proteini bakteriyel fimbriyaları bağlayan doğal bir konak savunmasıdır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Asendan yol ÜSE'lerin yaklaşık %99'unu oluşturan ana rotadır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(30, "[TEKRAR SAYFASI - CHECKPOINT 3] Bulaş Yolları, Savunma ve Virülans", "3. Bölümün kapsamlı pekiştirmesi: yayılım rotaları, konak bariyerleri ve virülans faktörleri", "Bölüm Tekrarı", s30_narrative, s30_bullets, s30_elements))

    return slides
