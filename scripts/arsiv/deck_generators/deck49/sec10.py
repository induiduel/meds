import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec10():
    slides = []

    # Slide 91: Spot Bilgiler Sentezi: Servisit ve Endoservikal Polip
    s91_narrative = (
        "Kurul 1 Tıbbi Patoloji amfi ders notunun ilk bölümünde yer alan non-neoplastik servikal "
        "patolojilerin sınav spotlarını eksiksiz olarak konsolide ediyoruz.\n\n"
        "- **En Yaygın Servisit Etkeni:** Cinsel yolla bulaşan hastalık kliniklerinde servisit vakalarının "
        "**%40'ına kadarından sorumlu olan en yaygın etken Chlamydia trachomatis'tir**.\n"
        "- **Klinik Belirti (Lökore):** Servisitte en sık başvuru semptomu normalden farklı renk, koku "
        "veya kıvamdaki **irinli/mukopürülan vajinal akıntıdır (lökore)**; tedavi ampiriktir.\n"
        "- **Endoservikal Polip Özeti:** Kanal mukozasından lümene sarkan benign ekzofitik kitlelerdir; "
        "**malign potansiyelleri kesinlikle yoktur**. Yüzeyel ülserasyon ve kanamayla serviks karsinomu "
        "şüphesi yaratırlar; basit küretaj veya **polipektomi** ile tedavi edilirler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Servisitin en yaygın etkeni Chlamydia trachomatis'tir (%40); endoservikal polip benigndir ve malign potansiyeli yoktur, kanamayla kanseri taklit eder."
    )
    s91_bullets = [
        "Chlamydia trachomatis en yaygın servisit etkenidir (%40).",
        "Servisitte irinli/mukopürülan lökore tipik bulgudur.",
        "Endoservikal polip benigndir; malign potansiyeli yoktur, kanama yapar."
    ]
    s91_elements = [
        make_cloze("CYBH kliniklerinde servisit vakalarının yüzde 40'ına kadarından sorumlu olan en yaygın bakteri Chlamydia trachomatis'tir.", "Chlamydia trachomatis", "En yaygın servisit bakteriyel etkeni"),
        make_table("Servisit ve Polip Kilit Spotları", ["Konu", "Kritik Sınav Spotu", "Klinik Yansıması"], [
            {"cells": [{"text": "En Yaygın Servisit Bakterisi", "isMasked": False}, {"text": "Chlamydia trachomatis (vakaların %40'ı)", "isMasked": True, "hint": "en sık bakteriyel servisit etkeni"}, {"text": "Ampirik doksisiklin/azitromisin tedavisi"}]},
            {"cells": [{"text": "Endoservikal Polip Malignitesi", "isMasked": False}, {"text": "Malign potansiyeli kesinlikle yoktur", "isMasked": False}, {"text": "Kanama karsinom şüphesi doğurur, polipektomi küratiftir", "isMasked": True, "hint": "selim lezyonun kanser taklidi"}]}
        ]),
        make_chain("Erken Bölüm Hatırlama Zinciri", [
            "1. Servisit Semptomu: İrinli lökore akıntısı görülür.",
            "2. Etiyoloji: Chlamydia trachomatis %40 oranında saptanır.",
            "3. Benign Kitle: Kanal içinde endoservikal polip büyür.",
            "4. Polipektomi: Kanamayı durdurmak ve kanseri ekarte etmek için polip eksize edilir."
        ]),
        make_recall("Servisitin en sık bakteriyel etkeni nedir ve endoservikal polipin malign potansiyeli var mıdır?", "En sık etken Chlamydia trachomatis'tir (%40); endoservikal polipin malign potansiyeli kesinlikle yoktur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Servisit ve Polip Spotları", [
            {"text": "Chlamydia trachomatis en yaygın servisit etkenidir (%40).", "isLie": False, "explanation": "Doğru. En sık bakteriyel patojendir."},
            {"text": "Endoservikal polipin malign potansiyeli yoktur.", "isLie": False, "explanation": "Doğru. Tamamen selim lezyondur."},
            {"text": "Endoservikal polip her kadında kesinlikle beyin kanaması yaparak ölüme yol açar.", "isLie": True, "explanation": "Tuzak! Polip benign lokal mukozal bir lezyondur; beyin kanaması yapmaz."},
            {"text": "Polip yüzey ülserasyonuyla düzensiz vajinal kanama yapabilir.", "isLie": False, "explanation": "Doğru. Kanser taklidi kanamadır."}
        ]),
        make_quiz("Servisit olgularında en sık sorumlu bakteriyel patojen ve endoservikal polipin biyolojik davranışı hangisidir?", [
            {"key": "A", "text": "Chlamydia trachomatis - Benign lezyon (malign potansiyel yok)", "isCorrect": True, "explanation": "Klamidya en yaygındır ve polip selimdir."},
            {"key": "B", "text": "Vibrio cholerae - Yüksek dereceli osteosarkom", "isCorrect": False, "explanation": "Kolera kolondadır."},
            {"key": "C", "text": "Mycobacterium leprae - Malign lenfoma", "isCorrect": False, "explanation": "Lepra basili lezyonu değildir."},
            {"key": "D", "text": "Treponema pallidum - Zorunlu histerektomi kisti", "isCorrect": False, "explanation": "Sifiliz ayrı bir derstir."}
        ])
    ]
    slides.append(make_slide(91, "Spot Bilgiler Sentezi: Servisit ve Endoservikal Polip", "Chlamydia trachomatis (%40), pürülan lökore, selim endoservikal polip ve polipektomi", "Spot Bilgiler: Servisit ve Polip", s91_narrative, s91_bullets, s91_elements))

    # Slide 92: Spot Bilgiler Sentezi: Transformasyon Bölgesi ve Eversiyon
    s92_narrative = (
        "Serviks karsinogenezinin anatomik sahnesi olan transformasyon bölgesi ve skuamöz metaplazi "
        "kavramlarının temel sınav spotlarını netleştiriyoruz.\n\n"
        "- **Eversiyon (Ektropion):** Ergenlikte hormonal etkiyle endoservikal tek katlı kolumnar "
        "epitelin **ektoservikse doğru dışarı kaymasıdır**.\n"
        "- **Skuamöz Metaplazi:** Açığa çıkan kolumnar epitel, vajinal asidik ortama karşı koruyucu "
        "bir adaptasyon olarak çok katlı yassı epitele dönüşür.\n"
        "- **Karsinogenezin Beşiği:** Metaplazi ile oluşan **transformasyon bölgesi**, hızla çoğalan "
        "olgunlaşmamış skuamöz hücrelerden oluşur; **onkojenik HPV enfeksiyonuna en duyarlı alandır** "
        "ve serviks tümörleri en sık bu alanda gelişir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Transformasyon bölgesi olgunlaşmamış metaplastik skuamöz hücrelerden oluştuğu için onkojenik HPV enfeksiyonuna en duyarlı alandır ve tümörler en sık burada gelişir."
    )
    s92_bullets = [
        "Ergenlikte eversiyon kolumnar epitelin dışarı kaymasıdır.",
        "Asidik ortama yanıt olarak koruyucu skuamöz metaplazi gelişir.",
        "Transformasyon bölgesi HPV'ye en duyarlı alandır ve kanser merkezidir."
    ]
    s92_elements = [
        make_cloze("Servikste tümörlerin en sık kaynaklandığı ve HPV'ye en duyarlı alan transformasyon bölgesi olarak adlandırılır.", "transformasyon bölgesi", "Karsinogenezin başlangıç zonu"),
        make_table("Transformasyon Bölgesi Kilit Sınav Noktaları", ["Kavram", "Biyolojik Mekanizma", "Sınav Spotu Önemi"], [
            {"cells": [{"text": "Eversiyon", "isMasked": False}, {"text": "Kolumnar epitelin vajinal alana taşması", "isMasked": True, "hint": "mukozanın dışarı dönmesi"}, {"text": "Metaplaziyi başlatan ilk adım"}]},
            {"cells": [{"text": "Transformasyon Zonu", "isMasked": False}, {"text": "İmmatür metaplastik skuamöz epitel", "isMasked": False}, {"text": "HPV'ye en duyarlı alan; tümörler en sık burada", "isMasked": True, "hint": "en kritik karsinogenez odağı"}]}
        ]),
        make_chain("Zon Oluşum Spotu Zinciri", [
            "1. Puberte Eversiyonu: Kolumnar mukoza dışarı sarkar.",
            "2. Asit İrritasyonu: Vajinal asit epitelde reaktif metaplazi uyarır.",
            "3. Transformasyon Zonu: İmmatür skuamöz hücre tabakası kurulur.",
            "4. Onkojenik Duyarlılık: HPV virüsü bu genç hücreleri hedef alarak kanseri başlatır."
        ]),
        make_recall("Servikal karsinomların en sık transformasyon bölgesinde gelişmesinin temel nedeni nedir?", "Bölgenin olgunlaşmamış skuamöz hücrelerden oluşması ve onkojenik HPV'ye en duyarlı alan olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Transformasyon Bölgesi Spotları", [
            {"text": "Transformasyon bölgesi olgunlaşmamış skuamöz hücrelerden oluşur.", "isLie": False, "explanation": "Doğru. Metaplastik immatür hücrelerdir."},
            {"text": "Bu bölge onkojenik HPV enfeksiyonuna en duyarlı alandır.", "isLie": False, "explanation": "Doğru. Karsinogenez merkezidir."},
            {"text": "Transformasyon bölgesinde epitel yerine sadece saf motor yağı ve cıva bulunur.", "isLie": True, "explanation": "Tuzak! Canlı metaplastik skuamöz epitel bulunur; kimyasal cıva veya yağ bulunmaz."},
            {"text": "Tümörler servikste en sık bu bölgeden köken alır.", "isLie": False, "explanation": "Doğru. Karsinomların başlangıç yeridir."}
        ]),
        make_quiz("Servikste skuamöz karsinomların ve CIN lezyonlarının en sık kaynaklandığı anatomik bölge neresidir?", [
            {"key": "A", "text": "Transformasyon bölgesi (skuamokolumnar bileşke)", "isCorrect": True, "explanation": "En sık başlangıç yeri transformasyon bölgesidir."},
            {"key": "B", "text": "Uterus fundusunun dış serozası", "isCorrect": False, "explanation": "Fundus serozasından karsinom başlamaz."},
            {"key": "C", "text": "Over medullası", "isCorrect": False, "explanation": "Over dokusudur."},
            {"key": "D", "text": "Vajina introitusunun dış derisi", "isCorrect": False, "explanation": "Vulvar alandır."}
        ])
    ]
    slides.append(make_slide(92, "Spot Bilgiler Sentezi: Transformasyon Bölgesi ve Eversiyon", "Eversiyon mekanizması, immatür skuamöz epitel, viral duyarlılık ve kanser odağı", "Spot Bilgiler: Transformasyon Zonu", s92_narrative, s92_bullets, s92_elements))

    # Slide 93: Spot Bilgiler Sentezi: HPV Onkoproteinleri (E6 ve E7)
    s93_narrative = (
        "Human Papilloma Virus onkoproteinleri E6 ve E7'nin hücre döngüsüne müdahaleleri, tıp patoloji "
        "sınavlarının en klasik ve en yüksek verimli soru alanıdır.\n\n"
        "- **E6 Onkoproteini:** Tümör baskılayıcı **p53'e bağlanır**, ubikitin-proteazom aracılığıyla "
        "p53'ün yıkımına yol açar ve **telomeraz aktivasyonunu artırır**; sonuç **apoptoz inhibisyonu "
        "ve hücre ömrünün uzamasıdır (ölümsüzlük)**.\n"
        "- **E7 Onkoproteini:** Retinoblastoma **(RB) proteinine bağlanır**, RB'nin tuttuğu **E2F transkripsiyon "
        "faktörünü serbest bırakır**; sonuç **G1/S hücre döngüsü kontrolünün bozulması ve frensiz mitozdur**.\n"
        "- **Viral Genom Ayrımı:** Yüksek risklilerde (16, 18) DNA **konak genomuna entegre olur**; "
        "düşük risklilerde (6, 11) DNA **episomal kalır**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] E6 → p53 yıkımı ve telomeraz artışı; E7 → RB bağlanması, E2F salınımı ve G1/S hızlanması. Tip 16/18 entegre olur, Tip 6/11 episomal kalır."
    )
    s93_bullets = [
        "E6 onkoproteini p53'ü yıkar ve telomerazı artırır (apoptoz engellenir).",
        "E7 onkoproteini RB'ye bağlanıp E2F'yi salar (kontrolsüz S fazı).",
        "Tip 16/18 konak DNA'sına entegre olurken Tip 6/11 episomal kalır."
    ]
    s93_elements = [
        make_cloze("HPV E6 onkoproteini p53 tümör baskılayıcısını yıkar; E7 ise RB proteinine bağlanarak E2F faktörünü serbest bırakır.", "E2F", "E7 ile serbest kalan transkripsiyon faktörü"),
        make_table("E6 ve E7 Karşılaştırmalı Sınav Spotları", ["Onkoprotein", "Hücresel Hedef Protein", "Nihai Moleküler Sonuç"], [
            {"cells": [{"text": "E6 Onkoproteini", "isMasked": False}, {"text": "p53 yıkımı ve telomeraz artışı", "isMasked": True, "hint": "apoptoz engeli ve telomer uzaması"}, {"text": "Apoptoz direnci ve ölümsüzleşme"}]},
            {"cells": [{"text": "E7 Onkoproteini", "isMasked": False}, {"text": "RB bağlanması ve E2F salınımı", "isMasked": False}, {"text": "G1/S fazı geçişi ve frensiz mitoz", "isMasked": True, "hint": "kontrolsüz hücre bölünmesi"}]}
        ]),
        make_chain("Moleküler Onkogenez Spotu", [
            "1. Viral İfade: E6 ve E7 hücreye pompalanır.",
            "2. p53 Parçalanması: E6 ile p53 proteazomda yok edilir.",
            "3. RB İnaktivasyonu: E7 ile RB kilitlenir ve E2F salınır.",
            "4. Hücresel Kaos: Ölmeyen ve durmaksızın bölünen kanser klonları oluşur."
        ]),
        make_recall("HPV onkoproteinleri E6 ve E7'nin moleküler etki mekanizmalarını tek bir cümleyle özetleyiniz.", "E6 p53'ü yıkarak apoptozu engeller ve telomerazı artırır; E7 ise RB'ye bağlanıp E2F'yi salarak G1/S döngüsünü kontrolsüzce hızlandırır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: E6 ve E7 Spotları", [
            {"text": "E6 p53 yıkımına ve telomeraz aktivasyonuna yol açar.", "isLie": False, "explanation": "Doğru. Apoptozu durdurur."},
            {"text": "E7 RB'ye bağlanarak E2F transkripsiyon faktörünü serbest bırakır.", "isLie": False, "explanation": "Doğru. S fazını tetikler."},
            {"text": "E7 onkoproteini tümör baskılayıcı p53'ü 500 kat çoğaltan bir hormondur.", "isLie": True, "explanation": "Tuzak! E7 RB'yi hedefler, p53'ü E6 yıkar; hiçbir onkoprotein p53'ü artırmaz."},
            {"text": "Düşük riskli HPV tiplerinde (6 ve 11) DNA episomal kalır.", "isLie": False, "explanation": "Doğru. Genoma entegre olmaz."}
        ]),
        make_quiz("HPV karsinogenezinde E7 onkoproteininin temel hücresel hedefi ve moleküler sonucu nedir?", [
            {"key": "A", "text": "RB'ye bağlanarak E2F'yi serbest bırakmak ve G1/S geçişini hızlandırmak", "isCorrect": True, "explanation": "E7'nin temel görevi RB inhibisyonu ve E2F salınımıdır."},
            {"key": "B", "text": "Hücre zarını eritip sitoplazmayı akıtmak", "isCorrect": False, "explanation": "Lizis yapmaz."},
            {"key": "C", "text": "Yalnızca p53'ü aktive etmek", "isCorrect": False, "explanation": "p53'ü hedef alan E6'dır."},
            {"key": "D", "text": "Sadece kolesterol sentezini durdurmak", "isCorrect": False, "explanation": "Lipit metabolizmasıyla ilgisizdir."}
        ])
    ]
    slides.append(make_slide(93, "Spot Bilgiler Sentezi: HPV Onkoproteinleri (E6 ve E7)", "E6 ve p53 yıkımı, E7 ve RB/E2F yolağı, telomeraz artışı ve genomik entegrasyon", "Spot Bilgiler: Onkoproteinler", s93_narrative, s93_bullets, s93_elements))

    # Slide 94: Spot Bilgiler Sentezi: SIL/CIN Histopatolojisi ve Doğal Seyir
    s94_narrative = (
        "Prekanseröz servikal intraepitelyal lezyonların histopatolojik sınırlarını ve doğal seyrini "
        "Robbins referanslarıyla son kez pekiştiriyoruz.\n\n"
        "- **LSIL (CIN I):** Displazi skuamöz epitelin **alt üçte birindedir (1/3)**; yüzeysel katmanlarda "
        "**koilositik değişiklik** belirgindir. Vakaların **%60'ı spontan gerilediğinden** prekanseröz kabul edilmez.\n"
        "- **HSIL (CIN II-III):** CIN II alt 2/3'ü, CIN III **epitelin tam kalınlığını (tam kat)** tutar. "
        "Polarite kaybolur, atipik mitozlar üst katmanlara yayılır ve olgunlaşma durduğu için **koilositik "
        "değişiklik genellikle yoktur**.\n"
        "- **Doğal Seyir Tablosu:** HSIL vakalarının **%30'u geriler, %60'ı sebat eder, %10'u 2-10 yıl içinde karsinoma ilerler**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] LSIL alt 1/3'ü tutar, koilositoz vardır, %60 geriler (prekanseröz sayılmaz). CIN III tam kalınlığı tutar, koilositoz yoktur, %10 karsinoma ilerler (2-10 yıl)."
    )
    s94_bullets = [
        "CIN I alt 1/3'tedir, koilositoz vardır, %60 geriler (prekanseröz sayılmaz).",
        "CIN III tam kalınlıktadır, koilositoz yoktur, polarite çökmüştür.",
        "HSIL'in %10'u 2-10 yıl içinde invaziv karsinoma ilerler."
    ]
    s94_elements = [
        make_cloze("CIN III lezyonunda displazi epitelin tam kalınlığını kaplarken koilositik değişiklik genellikle izlenmez.", "koilositik", "CIN III'te bulunmayan viral sitopatik değişiklik"),
        make_table("CIN I ve CIN III Karşılaştırmalı Spotları", ["Özellik", "CIN I (LSIL)", "CIN III (HSIL)"], [
            {"cells": [{"text": "Tutulum Seviyesi", "isMasked": False}, {"text": "Epitelin alt 1/3 tabakası", "isMasked": False}, {"text": "Tam kalınlık (bütün katmanlar)", "isMasked": True, "hint": "tam kat epitel atipisi"}]},
            {"cells": [{"text": "Koilositoz Varlığı", "isMasked": False}, {"text": "Belirgin perinükleer halo", "isMasked": True, "hint": "yüzeyel koilositler"}, {"text": "Genellikle yoktur (olgunlaşma durmuştur)", "isMasked": False}]},
            {"cells": [{"text": "Doğal Seyir Karakteri", "isMasked": False}, {"text": "%60 spontan gerileme", "isMasked": False}, {"text": "%10 invaziv kansere ilerleme (2-10 yıl)", "isMasked": True, "hint": "maligniteye dönüşüm oranı"}]}
        ]),
        make_chain("CIN Histopatolojik Ayrım Zinciri", [
            "1. Biyopsi Taraması: Displazi sadece alt 1/3'teyse ve koilositoz varsa CIN I denir.",
            "2. CIN I Yönetimi: Prekanseröz sayılmaz, %60 gerileyeceğinden izlenir.",
            "3. Tam Kat Atipi: Displazi tüm katları tutmuşsa ve koilositoz yoksa CIN III denir.",
            "4. CIN III Yönetimi: Kanserleşme riski %10 olduğundan cerrahiyle eksize edilir."
        ]),
        make_recall("CIN I ile CIN III lezyonlarının epitel tutulum derinlikleri ve koilositik değişiklik varlığı nasıldır?", "CIN I alt 1/3'ü tutar ve koilositoz vardır; CIN III tam kalınlığı tutar ve koilositoz genellikle yoktur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SIL/CIN Spotları", [
            {"text": "CIN I epitelin alt üçte birinde sınırlıdır.", "isLie": False, "explanation": "Doğru. Alt 1/3 derinliktir."},
            {"text": "CIN III'te koilositik değişiklik genellikle yoktur.", "isLie": False, "explanation": "Doğru. Olgunlaşma durduğu için koilositoz silinir."},
            {"text": "CIN I olgularının %100'ü 24 saat içinde terminal kemik kanserine dönüşür.", "isLie": True, "explanation": "Tuzak! CIN I'in %60'ı kendiliğinden geriler, prekanseröz bile kabul edilmez."},
            {"text": "HSIL vakalarının %10'u 2-10 yıl içinde karsinoma ilerler.", "isLie": False, "explanation": "Doğru. Karsinoma gidiş süresidir."}
        ]),
        make_quiz("Epitelin tam kalınlığını tutan, skuamöz olgunlaşması durmuş ve koilositik değişiklik içermeyen lezyon hangisidir?", [
            {"key": "A", "text": "CIN III (HSIL)", "isCorrect": True, "explanation": "CIN III tam kat tutulum yapar ve koilositoz genellikle bulunmaz."},
            {"key": "B", "text": "CIN I (LSIL)", "isCorrect": False, "explanation": "CIN I alt 1/3'ü tutar ve koilositoz boldur."},
            {"key": "C", "text": "Endoservikal polip", "isCorrect": False, "explanation": "Benign glandüler lezyondur."},
            {"key": "D", "text": "Normal ektoserviks", "isCorrect": False, "explanation": "Normal epitelde atipi olmaz."}
        ])
    ]
    slides.append(make_slide(94, "Spot Bilgiler Sentezi: SIL/CIN Histopatolojisi ve Doğal Seyir", "CIN I (alt 1/3, koilositoz, %60 regresyon), CIN III (tam kat, koilositoz yok, %10 progresyon)", "Spot Bilgiler: SIL/CIN", s94_narrative, s94_bullets, s94_elements))

    # Slide 95: Spot Bilgiler Sentezi: Yaş Zirveleri ve Taramalar
    s95_narrative = (
        "Serviks kanseri tarama dinamiklerinde yer alan yaş istatistikleri ve halk sağlığı "
        "kriterlerinin sınav spotlarını özetliyoruz.\n\n"
        "- **Zirve Yaşları:** SIL insidansı **yaklaşık 30 yaşta** zirve yaparken; invaziv serviks karsinomu "
        "insidansı **10-15 yıl sonra yaklaşık 45 yaş civarında** zirve yapar.\n"
        "- **Pap Smear Zaferi:** Transformasyon bölgesinden yapılan Pap smear taramaları mortalitede "
        "**yaklaşık %75 azalma** sağlamış ve hastalığı önde gelen ölüm nedenleri arasından çıkarmıştır.\n"
        "- **HPV DNA Testi:** Özellikle **30 yaş ve üzerindeki kadınlarda** değerlidir; negatif çıktığında "
        "izleyen **5 yıl içinde servikal neoplazi riski son derece düşüktür**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] SIL pik: ~30 yaş; Kanser pik: ~45 yaş (10-15 yıl sonra). Pap smear mortaliteyi %75 azalttı. HPV DNA testi ≥30 yaşta değerli olup negatifliği 5 yıllık güvence verir."
    )
    s95_bullets = [
        "SIL insidansı ~30 yaşta, invaziv karsinom ~45 yaşta zirve yapar.",
        "Pap smear taraması serviks kanseri mortalitesini ~%75 azaltmıştır.",
        "HPV DNA testi ≥30 yaşta değerlidir ve negatifliği 5 yıl güvence sağlar."
    ]
    s95_elements = [
        make_cloze("HPV DNA testi negatif sonuçlandığında izleyen 5 yıl boyunca servikal neoplazi riski son derece düşüktür.", "5 yıl", "Negatif testin sağladığı koruyucu güvence süresi"),
        make_table("Yaş ve Tarama Kilit Spotları", ["Kriter / Test", "Kritik Değer / Yaş", "Klinik / Halk Sağlığı Sonucu"], [
            {"cells": [{"text": "SIL Zirve Yaşı", "isMasked": False}, {"text": "~30 yaş (Karsinom ~45 yaş)", "isMasked": True, "hint": "genç erişkin pik yaşı"}, {"text": "10-15 yıllık koruyucu tarama penceresi"}]},
            {"cells": [{"text": "Pap Smear Mortalite Etkisi", "isMasked": False}, {"text": "~%75 azalma", "isMasked": False}, {"text": "Önde gelen ölüm nedenleri arasından çıkış", "isMasked": True, "hint": "başarılı halk sağlığı düşüşü"}]},
            {"cells": [{"text": "HPV Test Güvencesi", "isMasked": False}, {"text": "5 yıl güvenli negatiflik", "isMasked": True, "hint": "uzatılmış tarama aralığı"}, {"text": "≥30 yaş kadınlarda tarama aralığını uzatma"}]}
        ]),
        make_chain("Zaman ve Tarama Spotları", [
            "1. 30 Yaş Piki: SIL olguları bu yaşta zirveye ulaşır.",
            "2. Tarama Müdahalesi: Pap smear ve HPV testi devreye sokulur.",
            "3. 5 Yıllık Pencere: HPV negatifse kadın 5 yıl rahat takip edilir.",
            "4. %75 Düşüş: 45 yaştaki invaziv karsinom piki engellenir."
        ]),
        make_recall("SIL ve karsinom insidanslarının pik yaptığı yaşlar ile Pap smearin sağladığı mortalite azalma yüzdesi nedir?", "SIL ~30 yaş, karsinom ~45 yaş; Pap smear mortalitede yaklaşık %75 azalma sağlamıştır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Yaş ve Tarama Spotları", [
            {"text": "SIL insidansı ~30 yaşta, invaziv karsinom ~45 yaşta zirve yapar.", "isLie": False, "explanation": "Doğru. İki pik arasında 10-15 yıl vardır."},
            {"text": "Pap smear mortalitede yaklaşık %75 azalma sağlamıştır.", "isLie": False, "explanation": "Doğru. Tarihsel başarıdır."},
            {"text": "HPV DNA testi sadece 3 günlük bebeklerde göbek kordonunda yapılır.", "isLie": True, "explanation": "Tuzak! HPV testi yetişkin kadınlarda ≥30 yaşta servikal sürüntüde yapılır."},
            {"text": "HPV testi negatifse izleyen 5 yılda neoplazi riski çok düşüktür.", "isLie": False, "explanation": "Doğru. 5 yıllık negatif prediktif güvencedir."}
        ]),
        make_quiz("Rutin servikal kanser taramasında HPV DNA testi negatif gelen bir kadında neoplazi riski kaç yıl boyunca son derece düşüktür?", [
            {"key": "A", "text": "İzleyen 5 yıl boyunca", "isCorrect": True, "explanation": "HPV negatifliği 5 yıllık güçlü güvence sağlar."},
            {"key": "B", "text": "Yalnızca 20 saniye boyunca", "isCorrect": False, "explanation": "Geçici değildir."},
            {"key": "C", "text": "Sadece 1 saat boyunca", "isCorrect": False, "explanation": "5 yıllık uzun süreli takip konforudur."},
            {"key": "D", "text": "Hiçbir süre güvence sağlamaz", "isCorrect": False, "explanation": "Negatif prediktif değeri çok yüksektir."}
        ])
    ]
    slides.append(make_slide(95, "Spot Bilgiler Sentezi: Yaş Zirveleri ve Taramalar", "SIL piki (30 yaş), kanser piki (45 yaş), %75 mortalite düşüşü ve 5 yıllık HPV güvencesi", "Spot Bilgiler: Tarama ve Yaş", s95_narrative, s95_bullets, s95_elements))

    # Slide 96: Spot Bilgiler Sentezi: HPV Aşılaması İlkeleri
    s96_narrative = (
        "HPV aşılamasının hedef popülasyonu, antijenik içeriği ve sağladığı immünolojik korumanın "
        "kilit sınav spotlarını konsolide ediyoruz.\n\n"
        "- **Hedef Yaş Grubu:** Aşı rutin olarak **11-12 yaş kız ve erkek çocuklara** önerilir (9 yaştan "
        "itibaren başlanabilir); **26 yaşına kadar** catch-up (yakalama) aşılaması yapılabilir.\n"
        "- **Erkek Aşılaması:** Erkeklerin aşılanması kadınlara bulaş zincirini kırar; ayrıca erkeklerde "
        "görülen **anal kanser ve orofaringeal kanserleri** doğrudan önler.\n"
        "- **Koruma Süresi:** Aşıların sağladığı nötralizan koruma süresi **en az 10 yıldır**.\n"
        "- **Tarama Devamlılığı:** Aşı önceki enfeksiyonları temizlemez ve tüm tipleri kapsamaz; bu nedenle "
        "==HPV aşısı servikal kanser taramasının yerine geçmez==.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Aşı 11-12 yaş kız ve erkeklere önerilir, 26 yaşa kadar yapılabilir. Erkek aşılaması anal/orofarenks kanserini önler. Koruma süresi en az 10 yıldır. Aşı taramanın yerine geçmez."
    )
    s96_bullets = [
        "Aşı 11-12 yaş kız ve erkeklere önerilir, 26 yaşa kadar catch-up yapılır.",
        "Erkek aşılaması anal ve orofaringeal kanserleri önler.",
        "Koruma süresi en az 10 yıldır; aşı taramanın yerine geçmez."
    ]
    s96_elements = [
        make_cloze("HPV aşısı rutin takvimde 11-12 yaş kız ve erkek çocuklara uygulanması önerilen bir aşıdır.", "11-12 yaş", "Rutin aşılamanın önerildiği standart yaş grubu"),
        make_table("HPV Aşısı Temel Sınav Parametreleri", ["Özellik", "Kabul Edilen Standart", "Sınav Notu"], [
            {"cells": [{"text": "Rutin Yaş Grubu", "isMasked": False}, {"text": "11-12 yaş kız ve erkek çocuklar", "isMasked": True, "hint": "pediatrik hedef yaş"}, {"text": "26 yaşa kadar catch-up yapılabilir"}]},
            {"cells": [{"text": "Erkeklerde Kazanım", "isMasked": False}, {"text": "Anal ve orofaringeal kanserlerin önlenmesi", "isMasked": False}, {"text": "Bulaş zincirini kırma ve sürü bağışıklığı", "isMasked": True, "hint": "erkek malignite koruması"}]},
            {"cells": [{"text": "Koruma Süresi", "isMasked": False}, {"text": "En az 10 yıl", "isMasked": True, "hint": "minimum kanıtlanmış süre"}, {"text": "Taramanın yerine geçmez (tarama şarttır)"}]}
        ]),
        make_chain("Aşılama Spot Zinciri", [
            "1. 11-12 Yaş Dozu: Çocuklukta her iki cinse de aşı yapılır.",
            "2. Erkek Koruması: Bulaş kırılır, erkekte anal kanser önlenir.",
            "3. 10 Yıllık Süre: Antikorlar en az 10 yıl boyunca yüksek kalır.",
            "4. Tarama Sürdürülür: Yetişkinlikte Pap ve HPV testleri asla terk edilmez."
        ]),
        make_recall("HPV aşısının rutin hedef yaşı, koruma süresi ve aşılanan kadınlarda taramanın bırakılıp bırakılamayacağı nedir?", "Rutin yaş 11-12 yaştır; koruma süresi en az 10 yıldır; aşı taramanın yerine geçmez, tarama sürdürülür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Aşısı Spotları", [
            {"text": "Aşı 11-12 yaş kız ve erkek çocuklara önerilir.", "isLie": False, "explanation": "Doğru. Rutin hedef gruptur."},
            {"text": "Erkek aşılaması anal ve orofaringeal kanserleri önler.", "isLie": False, "explanation": "Doğru. Erkek kanserlerine karşı korur."},
            {"text": "HPV aşısı yapıldıktan sonra tüm kadınların tarama yaptırması yasaktır.", "isLie": True, "explanation": "Tuzak! Aşı taramanın yerine geçmez; rutin tarama devam etmelidir."},
            {"text": "Koruma süresi en az 10 yıldır.", "isLie": False, "explanation": "Doğru. Kanıtlanmış asgari süredir."}
        ]),
        make_quiz("HPV aşılaması ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "HPV aşıları rutin servikal kanser taramasının yerine geçer ve tarama bırakılır", "isCorrect": True, "explanation": "Yanlış ifade! Aşı taramanın yerine GEÇMEZ, tarama devam etmek zorundadır."},
            {"key": "B", "text": "Rutin aşılama 11-12 yaş kız ve erkek çocuklara önerilir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Erkek aşılaması anal ve orofarenks kanserlerini önler", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Aşının kanıtlanmış koruma süresi en az 10 yıldır", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(96, "Spot Bilgiler Sentezi: HPV Aşılaması İlkeleri", "11-12 yaş, anal/orofarenks kanser önlemi, en az 10 yıl koruma, tarama devamlılığı", "Spot Bilgiler: Aşı İlkeleri", s96_narrative, s96_bullets, s96_elements))

    # Slide 97: Spot Bilgiler Sentezi: İnvaziv Karsinom Histolojisi ve Tipleri
    s97_narrative = (
        "İnvaziv serviks karsinomunun histolojik tiplerine ve mikroskobik diferansiasyonuna "
        "dair kilit sınav spotlarını konsolide ediyoruz.\n\n"
        "- **Histolojik Dağılım Oranları:** Olguların **~%80'i skuamöz hücreli karsinom**, "
        "**~%15'i adenokarsinom ve adenoskuamöz karsinom**, **<%5'i küçük hücreli nöroendokrin karsinomdur**; "
        "tümü yüksek riskli HPV ile ilişkilidir.\n"
        "- **Diferansiasyon Spotu:** İyi diferansiye skuamöz karsinomda **keratin incileri (horn pearls)** "
        "karakteristikken; zayıf diferansiye karsinomda **az keratinizasyon** izlenir.\n"
        "- **En Kötü Prognoz:** Küçük hücreli nöroendokrin karsinom, akciğer küçük hücreli kanserine benzer "
        "ve **tüm tipler arasında prognozu en kötü olandır**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] ~%80 SCC, ~%15 Adenokarsinom, <%5 Küçük hücreli nöroendokrin. İyi diferansiyede keratin incileri; zayıf diferansiyede az keratinizasyon. Küçük hücreli tip en kötü prognozludur."
    )
    s97_bullets = [
        "SCC ~%80, Adenokarsinom ~%15, Küçük hücreli nöroendokrin <%5'tir.",
        "İyi diferansiyede keratin incileri, zayıfta az keratinizasyon izlenir.",
        "Küçük hücreli nöroendokrin karsinom prognozu en kötü histolojik tiptir."
    ]
    s97_elements = [
        make_cloze("İnvaziv serviks karsinomunda histolojik olarak keratin incileri iyi diferansiye skuamöz karsinomda karakteristiktir.", "keratin incileri", "İyi diferansiye SCC mikroskobik belirteci"),
        make_table("Histolojik Tipler Kilit Sınav Spotları", ["Histolojik Tip", "Görülme Sıklığı", "Histopatolojik Karakter / Prognoz"], [
            {"cells": [{"text": "Skuamöz Karsinom", "isMasked": False}, {"text": "~%80", "isMasked": True, "hint": "en sık tip oranı"}, {"text": "İyi diferansiyede keratin incileri izlenir"}]},
            {"cells": [{"text": "Adenokarsinom", "isMasked": False}, {"text": "~%15", "isMasked": False}, {"text": "Endoservikal bez mimarisi, göreceli oranı arttı", "isMasked": True, "hint": "glandüler kanser artışı"}]},
            {"cells": [{"text": "Küçük Hücreli Nöroendokrin", "isMasked": False}, {"text": "<%5", "isMasked": True, "hint": "nadir agresif tip"}, {"text": "Akciğer küçük hücreliye benzer, prognozu en kötü", "isMasked": False}]}
        ]),
        make_chain("Histolojik Sınıflama Spotu", [
            "1. İnvazyon Tespiti: Bazal membran delinecek aşamaya gelmiştir.",
            "2. %80 Skuamöz Tip: Keratin incileri aranarak iyi diferansiye SCC denir.",
            "3. %15 Bez Tipi: Bez yapıları görülerek adenokarsinom tanısı konur.",
            "4. <%5 Agresif Tip: Küçük hücreli morfolojiyle en kötü prognoz belirlenir."
        ]),
        make_recall("Serviks kanserinde (1) En sık histolojik tip, (2) İyi diferansiyede görülen keratin yapısı ve (3) En kötü prognozlu tip nedir?", "(1) Skuamöz hücreli karsinom (~%80), (2) Keratin incileri, (3) Küçük hücreli nöroendokrin karsinomdur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İnvaziv Karsinom Histolojisi Spotları", [
            {"text": "Skuamöz hücreli karsinom tüm vakaların yaklaşık %80'ini oluşturur.", "isLie": False, "explanation": "Doğru. Ezici çoğunluktur."},
            {"text": "İyi diferansiye karsinomda keratin incileri karakteristiktir.", "isLie": False, "explanation": "Doğru. Tanısal histolojik bulgudur."},
            {"text": "Küçük hücreli nöroendokrin karsinom tümörlerin %99'udur ve grip gibi 2 günde geçer.", "isLie": True, "explanation": "Tuzak! <%5 oranındadır ve prognozu en kötü, en ölümcül malignitedir."},
            {"text": "Zayıf diferansiye karsinomda az keratinizasyon saptanır.", "isLie": False, "explanation": "Doğru. Olgunlaşma kaybıdır."}
        ]),
        make_quiz("İnvaziv serviks karsinomu histolojik tipleri ve prognozu ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Olguların %80'i skuamözdür ve küçük hücreli nöroendokrin tip en kötü prognozludur", "isCorrect": True, "explanation": "SCC %80'dir ve küçük hücreli tip en kötü prognozludur."},
            {"key": "B", "text": "Serviks kanserlerinin tamamı kemik kaynaklı osteosarkomdur", "isCorrect": False, "explanation": "Epitelyal karsinomdur."},
            {"key": "C", "text": "Adenokarsinom hiçbir zaman servikste görülmez", "isCorrect": False, "explanation": "%15 oranında görülür."},
            {"key": "D", "text": "İyi diferansiye karsinomda keratin üretimi sıfırdır", "isCorrect": False, "explanation": "Bol keratin incisi içerir."}
        ])
    ]
    slides.append(make_slide(97, "Spot Bilgiler Sentezi: İnvaziv Karsinom Histolojisi ve Tipleri", "%80 SCC, %15 adenokarsinom, <%5 küçük hücreli, keratin incileri ve en kötü prognoz", "Spot Bilgiler: Histolojik Tipler", s97_narrative, s97_bullets, s97_elements))

    # Slide 98: Spot Bilgiler Sentezi: Yayılım, Fıçı Serviks ve Üremi
    s98_narrative = (
        "İnvaziv karsinomun lokal yayılım paternleri, fıçı serviks deformitesi ve ölümcül komplikasyonlarına "
        "dair sınav spotlarını son kez netleştiriyoruz.\n\n"
        "- **Fıçı Serviks:** Tümörün serviksi çepeçevre sararak stromaya derin invazyon yapması ve palpasyonda "
        "**kalın, rijit bir silindir halini almasına 'fıçı serviks' adı verilir**.\n"
        "- **Pelvik Fiksasyon:** Tümör lateralde parametriumlara yayıldığında **uterus pelvik yan duvarlara fikse olur**.\n"
        "- **En Sık Ölüm Nedeni:** Tümörün parametriumlarda üreterlere bası yaparak **bilateral hidronefroz "
        "ve terminal üremiye (böbrek yetmezliği)** yol açmasıdır.\n"
        "- **Metastaz Kuralı:** Pelvik lenf düğümü metastazı riski **invazyon derinliği** ve vasküler boşluk "
        "tutulumu ile doğrudan ilişkilidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Derin stromal invazyon = Fıçı serviks; Parametrial yayılım = Pelvik fiksasyon; En sık ölüm nedeni = Bilateral hidronefroz ve terminal üremi."
    )
    s98_bullets = [
        "Derin stromal invazyon palpasyonda rijit 'fıçı serviks' oluşturur.",
        "Parametrial yayılım uterusun pelvik duvarlara fikse olmasına yol açar.",
        "En sık ölüm nedeni üreter basısına bağlı terminal üremidir."
    ]
    s98_elements = [
        make_cloze("İleri evre serviks karsinomunda bilateral üreter basısına bağlı gelişen terminal üremi en sık ölüm nedenidir.", "üremi", "En sık karşılaşılan fatal komplikasyon"),
        make_table("Yayılım ve Komplikasyon Sınav Spotları", ["Klinik Tablo / Bulgu", "Patolojik Mekanizma", "Sınav Spotu Değeri"], [
            {"cells": [{"text": "Fıçı Serviks", "isMasked": False}, {"text": "Stromaya derin invazyon", "isMasked": True, "hint": "tam kat stromal kitle"}, {"text": "Palpasyonda kalın, rijit silindirik serviks"}]},
            {"cells": [{"text": "Pelvik Fiksasyon", "isMasked": False}, {"text": "Lateral parametrial infiltrasyon", "isMasked": False}, {"text": "Uterusun pelvise kilitlenmesi, inoperabilite", "isMasked": True, "hint": "hareketsiz uterus bulgusu"}]},
            {"cells": [{"text": "En Sık Ölüm Nedeni", "isMasked": False}, {"text": "Bilateral üreter basısı ve hidronefroz", "isMasked": False}, {"text": "Terminal üremi (böbrek yetmezliği)", "isMasked": True, "hint": "böbrek yetmezliği ile ölüm"}]}
        ]),
        make_chain("Ölümcül Yayılım Zinciri Spotu", [
            "1. Derin İnvazyon: Fıçı serviks morfolojisi oturur.",
            "2. Parametrial Köprü: Uterus pelvise fikse hale gelir.",
            "3. Üreter Darlığı: İki üreter de kitle altında boğulur.",
            "4. Terminal Üremi: Bilateral hidronefroz hastayı ölüme götürür."
        ]),
        make_recall("Serviks kanserinde derin stromal invazyonun palpasyon bulgusu ve hastaların en sık ölüm nedeni nedir?", "Derin stromal invazyon 'fıçı serviks' yapar; en sık ölüm nedeni ise üreter basısına bağlı 'terminal üremi'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Yayılım ve Üremi Spotları", [
            {"text": "Fıçı serviks palpasyonda kalın, rijit serviks şeklinde hissedilir.", "isLie": False, "explanation": "Doğru. Tipik derin invazyon bulgusudur."},
            {"text": "Parametrial yayılım uterusun pelvik duvarlara fikse olmasına yol açar.", "isLie": False, "explanation": "Doğru. Donuk pelvis oluşturur."},
            {"text": "En sık ölüm nedeni hastaların yüksek sesle şarkı söylemesidir.", "isLie": True, "explanation": "Tuzak! En sık ölüm nedeni üreter obstrüksiyonuna bağlı gelişen terminal üremidir."},
            {"text": "Bilateral hidronefroz böbrek yetmezliğiyle sonuçlanır.", "isLie": False, "explanation": "Doğru. Üreminin mekanizmasıdır."}
        ]),
        make_quiz("İnvaziv serviks karsinomunda fıçı serviks oluşumu ve en sık ölüm nedeni aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Fıçı serviks: Derin stromal invazyon; En sık ölüm: Terminal üremi", "isCorrect": True, "explanation": "Fıçı serviks derin stromal tutulumu gösterir, en sık ölüm nedeni üremidir."},
            {"key": "B", "text": "Fıçı serviks: Safra taşı; En sık ölüm: Astım", "isCorrect": False, "explanation": "İlgisiz organ patolojileridir."},
            {"key": "C", "text": "Fıçı serviks: Beyin absesi; En sık ölüm: Menenjit", "isCorrect": False, "explanation": "Santral sinir sistemi hastalıklarıdır."},
            {"key": "D", "text": "Fıçı serviks: Burun kırığı; En sık ölüm: Grip", "isCorrect": False, "explanation": "Alakasızdır."}
        ])
    ]
    slides.append(make_slide(98, "Spot Bilgiler Sentezi: Yayılım, Fıçı Serviks ve Üremi", "Derin stromal invazyon, fıçı serviks, parametrial pelvik fiksasyon ve terminal üremi", "Spot Bilgiler: Yayılım ve Ölüm", s98_narrative, s98_bullets, s98_elements))

    # Slide 99: Spot Bilgiler Sentezi: Tedavi ve Tarama Başarısı
    s99_narrative = (
        "Serviks kanserinin evrelere göre cerrahi-onkolojik tedavisini ve erken tanının yaşamsal "
        "rolünü özetleyen sınav spotlarını son kez konsolide ediyoruz.\n\n"
        "- **Mikroinvaziv Karsinom (≤3 mm):** Pelvik lenf nodu metastaz riski <%1 olduğu için cerrahi sınırları "
        "temiz **konik biyopsi ile küratif tedavi edilebilir**.\n"
        "- **Erken İnvaziv Karsinom:** Primer tedavi **histerektomi ve pelvik lenf düğümü diseksiyonudur**.\n"
        "- **İleri Evre Karsinom:** Cerrahi sınır aşıldığından **radyoterapi ve kemoterapi (kemoradyoterapi)** kombinasyonu uygulanır.\n"
        "- **Yaşamsal İlke:** ==Erken tanı ve tarama programları yaşamsal öneme sahiptir==; preinvaziv lezyon "
        "evresinde yakalanan kadınlarda yaşam kaybı sıfıra yakındır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir; erken invaziv histerektomi + lenf diseksiyonu, ileri evre radyoterapi + kemoterapi gerektirir. Erken tanı ve tarama yaşamsaldır."
    )
    s99_bullets = [
        "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.",
        "Erken evrede radikal histerektomi + pelvik lenf diseksiyonu uygulanır.",
        "İleri evrede kemoradyoterapi verilir; erken tanı yaşamsaldır."
    ]
    s99_elements = [
        make_cloze("Mikroinvaziv karsinom olgularında doğurganlığı koruyan küratif tedavi konik biyopsi ile sağlanır.", "konik biyopsi", "Mikroinvazyonda küratif olan eksizyonel işlem"),
        make_table("Tedavi Modaliteleri Kilit Sınav Spotları", ["Evre / Durum", "Standart Tedavi Yöntemi", "Sınav Notu"], [
            {"cells": [{"text": "Mikroinvaziv Karsinom", "isMasked": False}, {"text": "Konik biyopsi (konizasyon)", "isMasked": True, "hint": "organ koruyucu rezeksiyon"}, {"text": "Lenf metastaz riski <%1, tam kür"}]},
            {"cells": [{"text": "Erken İnvaziv Karsinom", "isMasked": False}, {"text": "Histerektomi + Pelvik lenf diseksiyonu", "isMasked": False}, {"text": "Primer cerrahi rezeksiyon", "isMasked": True, "hint": "radikal cerrahi protokol"}]},
            {"cells": [{"text": "İleri Evre Karsinom", "isMasked": False}, {"text": "Radyoterapi + Kemoterapi kombinasyonu", "isMasked": True, "hint": "eşzamanlı kemoradyoterapi"}, {"text": "Cerrahi inoperabl olgularda standart"}]}
        ]),
        make_chain("Tedavi Kararı Spot Zinciri", [
            "1. Mikroinvaziv Ayrım: Stromal derinlik ≤3 mm ise konik biyopsi yapılır.",
            "2. Erken Evre Ayrım: Servikse sınırlı kitlede radikal histerektomi uygulanır.",
            "3. İleri Evre Ayrım: Pelvise fikse olguda kemoradyoterapiye başlanır.",
            "4. Altın Sonuç: Erken tanı ve tarama hayat kurtarır."
        ]),
        make_recall("Serviks kanserinde mikroinvaziv karsinomun tedavisi nedir ve ileri evrede cerrahi yerine ne uygulanır?", "Mikroinvaziv karsinom konik biyopsi ile tedavi edilir; ileri evrede ise radyoterapi ve kemoterapi kombinasyonu uygulanır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tedavi ve Tarama Spotları", [
            {"text": "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.", "isLie": False, "explanation": "Doğru. Düşük invazyon derinliğinde yeterlidir."},
            {"text": "Primer cerrahi tedavi histerektomi ve pelvik lenf düğümü diseksiyonudur.", "isLie": False, "explanation": "Doğru. Standart cerrahidir."},
            {"text": "İleri evre serviks kanseri sadece hastaya buzlu limonata içirilerek tamamen iyileştirilir.", "isLie": True, "explanation": "Tuzak! İleri evrede kemoradyoterapi (radyoterapi + kemoterapi) uygulanır; limonata tedavi değildir."},
            {"text": "Erken tanı ve tarama programları yaşamsal öneme sahiptir.", "isLie": False, "explanation": "Doğru. En temel halk sağlığı kuralıdır."}
        ]),
        make_quiz("Mikroinvaziv serviks karsinomunun ve ileri evre serviks karsinomunun standart tedavileri hangileridir?", [
            {"key": "A", "text": "Mikroinvaziv: Konik biyopsi; İleri evre: Radyoterapi ve kemoterapi kombinasyonu", "isCorrect": True, "explanation": "Mikroinvazyonda konik biyopsi, ileri evrede kemoradyoterapi standarttır."},
            {"key": "B", "text": "Mikroinvaziv: Akciğer nakli; İleri evre: Sadece aspirin", "isCorrect": False, "explanation": "Tıbbi tedavi protokolü değildir."},
            {"key": "C", "text": "Mikroinvaziv: Hiçbir şey yapmamak; İleri evre: Tonsillektomi", "isCorrect": False, "explanation": "Hatalı ve yetersizdir."},
            {"key": "D", "text": "Her iki evrede de sadece kolesterol ilacı", "isCorrect": False, "explanation": "Onkolojik tedavi değildir."}
        ])
    ]
    slides.append(make_slide(99, "Spot Bilgiler Sentezi: Tedavi ve Tarama Başarısı", "Mikroinvaziv konizasyon, radikal cerrahi, ileri evre kemoradyoterapi ve erken tanı zaferi", "Spot Bilgiler: Tedavi ve Kür", s99_narrative, s99_bullets, s99_elements))

    # Slide 100: [TEKRAR SAYFASI - CHECKPOINT 10] Deste 49 Genel Sınav ve Müfredat Sentezi
    s100_narrative = (
        "Tebrikler! Deste 49 boyunca İnvaziv Serviks Kanseri ve Endometriyozis dersinin amfi ders notu "
        "ve Robbins kılavuzlarındaki tüm kazanımlarını 100 slaytlık eksiksiz bir öğrenme zinciriyle tamamladınız.\n\n"
        "- **1. Servisit ve Polip:** En sık servisit etkeni Chlamydia trachomatis'tir (%40); endoservikal polip "
        "benigndir, malign potansiyeli yoktur, kanamayla kanseri taklit eder.\n"
        "- **2. Transformasyon Zonu ve HPV:** Eversiyon sonrası skuamöz metaplazi gelişir; immatür hücreler "
        "HPV'ye en duyarlı alandır. E6 p53'ü yıkar, E7 RB'yi inaktive edip E2F'yi salar.\n"
        "- **3. Doğal Seyir ve Tarama:** LSIL %60 geriler (prekanseröz sayılmaz); CIN III tam kalınlıktadır "
        "ve koilositoz yoktur. SIL 30 yaşta, kanser 45 yaşta pik yapar. Pap smear mortaliteyi %75 azalttı, "
        "HPV DNA testi 5 yıllık güvence verir; aşı en az 10 yıl korur.\n"
        "- **4. Karsinom ve Ölüm:** %80 SCC'dir (iyi diferansiyede keratin incileri); fıçı serviks derin invazyonu, "
        "pelvik fiksasyon parametrial yayılımı gösterir. En sık ölüm nedeni bilateral hidronefroz ve terminal üremidir.\n"
        "- **5. Tedavi:** Mikroinvaziv = konik biyopsi; erken invaziv = radikal histerektomi + lenfadenektomi; "
        "ileri evre = kemoradyoterapi.\n\n"
        "> [!IMPORTANT]\n"
        "> [KURS TAMAMLANDI - DESTE 49] Servisit ve polipten başlayarak moleküler onkogenez, CIN evreleri, tanı triadları, fıçı serviks ve ölümcül üremiye kadar 100 slaytlık tam yetkinlik sağlandı."
    )
    s100_bullets = [
        "En sık servisit: Chlamydia trachomatis; Polip: Benign, kanama yapar.",
        "Transformasyon zonu HPV'ye en duyarlıdır; E6 p53'ü, E7 RB'yi yıkar.",
        "LSIL %60 geriler; CIN III tam kat ve koilositozsuz; SIL 30 yaşta pik yapar.",
        "SCC %80'dir; fıçı serviks derin invazyon; en sık ölüm terminal üremidir.",
        "Mikroinvazyonda konik biyopsi, erken invazivde histerektomi, ileri evrede kemoradyoterapi uygulanır."
    ]
    s100_elements = [
        make_cloze("Deste 49 genel sentezinde incelenen ileri evre serviks kanserinde en sık ölüm nedeni terminal üremi tablosudur.", "üremi", "100 slaytlık kursun finalinde pekiştirilen en sık ölüm nedeni"),
        make_table("Deste 49 Büyük Final Sentez Tablosu", ["Konu Başlığı", "Altın Standart Sınav Spotu", "Klinik Yansıması"], [
            {"cells": [{"text": "En Sık Servisit Bakterisi", "isMasked": False}, {"text": "Chlamydia trachomatis (%40)", "isMasked": True, "hint": "en yaygın servisit patojeni"}, {"text": "Pürülan lökore ve ampirik tedavi"}]},
            {"cells": [{"text": "Viral Karsinogenez", "isMasked": False}, {"text": "E6 (p53 yıkımı) ve E7 (RB/E2F aktivasyonu)", "isMasked": False}, {"text": "Apoptoz direnci ve kontrolsüz S fazı", "isMasked": True, "hint": "tümör baskılayıcı yıkımı"}]},
            {"cells": [{"text": "En Sık Karsinom ve Ölüm", "isMasked": False}, {"text": "SCC (%80) ve Terminal Üremi", "isMasked": True, "hint": "en sık tip ve en sık ölüm nedeni"}, {"text": "Bilateral üreter basısı ve renal iflas"}]}
        ]),
        make_chain("Deste 49 Büyük Final Akışı", [
            "1. Başlangıç: Servisit (Klamidya %40) ve selim polip kanamasıyla klinikte karşılaşılır.",
            "2. Viral Temel: HPV 16/18 transformasyon zonuna girip E6/E7 ile CIN'i kurar.",
            "3. Tarama Zaferi: Pap smear mortaliteyi %75 düşürür, aşı en az 10 yıl korur.",
            "4. Karsinom Finali: Fıçı serviks ve üremiye giden yolda erken konizasyon ve kemoradyoterapi hayat kurtarır."
        ]),
        make_recall("Deste 49'un 5 ana kilit spotu: (1) En sık servisit etkeni, (2) E6/E7 hedefleri, (3) SIL pik yaşı, (4) En sık ölüm nedeni ve (5) Mikroinvaziv tedavi nedir?", "(1) Chlamydia trachomatis (%40), (2) E6 p53'ü yıkar, E7 RB'yi inaktive eder, (3) ~30 yaş, (4) Terminal üremi, (5) Konik biyopsidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Deste 49 Büyük Final", [
            {"text": "Chlamydia trachomatis en yaygın servisit etkenidir (%40).", "isLie": False, "explanation": "Doğru. En sık bakteriyel ajandır."},
            {"text": "İleri evre serviks kanserinde en sık ölüm nedeni terminal üremidir.", "isLie": False, "explanation": "Doğru. Bilateral üreter basısıyla gelişir."},
            {"text": "Deste 49 boyunca işlenen tüm serviks hastalıkları sadece kedilerde görülen bir tüy dökülmesidir.", "isLie": True, "explanation": "Tuzak! Serviks kadın genital sisteminin boyun kısmıdır; kedilerle veya tüy dökülmesiyle hiçbir ilgisi yoktur."},
            {"text": "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.", "isLie": False, "explanation": "Doğru. Organ koruyucu küratif yaklaşımdır."}
        ]),
        make_quiz("Deste 49'da işlenen 100 slaytlık müfredat sentezine göre aşağıdaki tıbbi ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Serviks karsinomunda en sık ölüm nedeni üreter basısına bağlı terminal üremidir", "isCorrect": True, "explanation": "Bilateral hidronefroz ve terminal üremi en sık ölüm nedenidir."},
            {"key": "B", "text": "Endoservikal polip hemen histerektomi gerektiren çok öldürücü bir karsinomdur", "isCorrect": False, "explanation": "Tamamen benigndir."},
            {"key": "C", "text": "HPV aşısı olan kadınların tarama yaptırması yasaktır", "isCorrect": False, "explanation": "Tarama aksatılmadan sürdürülür."},
            {"key": "D", "text": "CIN I vakalarının %100'ü 1 haftada metastaz yapar", "isCorrect": False, "explanation": "%60'ı kendiliğinden geriler."}
        ])
    ]
    slides.append(make_slide(100, "[TEKRAR SAYFASI - CHECKPOINT 10] Deste 49 Genel Sınav ve Müfredat Sentezi", "Deste 49 büyük final konsolidasyonu: servisit, karsinogenez, CIN, fıçı serviks, üremi ve tedavi", "Büyük Final Sentezi", s100_narrative, s100_bullets, s100_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec10()
    print(f"Sec10 generated: {len(slides)} slides (Slide 91 to 100)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
