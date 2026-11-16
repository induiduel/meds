import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec9():
    slides = []

    # Slide 81: Sentez: Etyolojiden Kliniğe Serviks Karsinogenez Zinciri
    s81_narrative = (
        "Serviks karsinogenezi, enfeksiyon hastalıkları, moleküler biyoloji ve cerrahi patolojinin "
        "iç içe geçtiği çok basamaklı ve uzun yıllara yayılan kusursuz bir karsinogenez modelidir.\n\n"
        "- **Viral Giriş ve Persistans:** Cinsel temasla bulaşan yüksek onkojenik riskli HPV tipleri "
        "(özellikle **Tip 16 ve 18**), serviksin metaplastik **transformasyon bölgesindeki** çoğalan "
        "olgunlaşmamış skuamöz hücreleri enfekte eder; karsinogenez için persistan enfeksiyon şarttır.\n"
        "- **Genomik Dönüşüm:** Viral DNA konak genomuna entegre olurken **E2 repressör geni parçalanır**; "
        "böylece serbest kalan **E6 (p53'ü yıkar)** ve **E7 (RB'ye bağlanıp E2F'yi salar)** onkoproteinleri kontrolsüz proliferasyonu başlatır.\n"
        "- **Preinvazivden İnvazive:** Süreç LSIL'den HSIL'e (CIN II-III) ve ortalama 10-15 yıl sonra "
        "bazal membranın delinmesiyle invaziv karsinoma evrilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [KARSİNOGENEZ ZİNCİRİ] Yüksek riskli HPV → Transformasyon zonu → E2 kırılması → E6 (p53 yıkımı) ve E7 (RB blokajı) → CIN I/II/III → İnvaziv karsinom."
    )
    s81_bullets = [
        "HPV 16 ve 18 transformasyon bölgesindeki immatür hücreleri hedefler.",
        "Genom entegrasyonu E2'yi bozar; kontrolsüz E6 ve E7 sentezlenir.",
        "E6 p53'ü yıkar, E7 RB'yi inaktive eder; 10-15 yılda invaziv kanser gelişir."
    ]
    s81_elements = [
        make_cloze("Karsinogenez zincirinde entegrasyonla E2 geninin parçalanması E6 ve E7 ekspresyon patlamasına yol açar.", "E2", "Viral negatif regülatör gen"),
        make_table("Karsinogenez Zincirinin Moleküler ve Hücresel Durakları", ["Basamak", "Moleküler Olay", "Morfolojik Karşılık"], [
            {"cells": [{"text": "Enfeksiyon ve Entegrasyon", "isMasked": False}, {"text": "HPV 16/18 konak genomuna girer, E2 parçalanır", "isMasked": True, "hint": "viral DNA'nın insan kromozomuna katılması"}, {"text": "Asemptomatik transformasyon zonu"}]},
            {"cells": [{"text": "Tümör Baskılayıcı İflası", "isMasked": False}, {"text": "E6 ile p53 yıkımı, E7 ile RB inhibisyonu", "isMasked": False}, {"text": "HSIL / CIN III (tam kat displazi)", "isMasked": True, "hint": "şiddetli hücresel atipi evresi"}]}
        ]),
        make_chain("Tüm Karsinogenez Omurgası", [
            "1. Cinsel Bulaş: HPV 16/18 transformasyon bölgesine girer.",
            "2. Genomik Entegrasyon: Viral DNA insan kromozomuna monte edilirken E2 kırılır.",
            "3. Moleküler Onkoloji: E6 p53'ü yok eder, E7 RB'yi devreden çıkarır.",
            "4. İnvaziv Kanser: Yıllar süren sessiz displazi stromal invazyonla karsinoma dönüşür."
        ]),
        make_recall("Serviks karsinogenezinin moleküler omurgasını oluşturan iki viral onkoprotein ve inaktive ettikleri hücresel proteinler nelerdir?", "E6 onkoproteini p53'ü; E7 onkoproteini ise RB proteinini inaktive eder."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Karsinogenez Zinciri Sentezi", [
            {"text": "HPV 16 ve 18 karsinogenezin ana viral etkenleridir.", "isLie": False, "explanation": "Doğru. Yüksek riskli prototip tiplerdir."},
            {"text": "E2 geninin bozulması E6 ve E7 ekspresyonunu artırır.", "isLie": False, "explanation": "Doğru. Negatif fren ortadan kalkar."},
            {"text": "Karsinogenez zincirinde E6 proteini hücreye kalsiyum pompalayarak kemik oluşturur.", "isLie": True, "explanation": "Tuzak! E6 kemik yapmaz; p53'ü yıkarak apoptozu engeller."},
            {"text": "Preinvaziv dönemden invaziv kansere geçiş 10-15 yıl alabilir.", "isLie": False, "explanation": "Doğru. Geniş bir zaman aralığı vardır."}
        ]),
        make_quiz("Servikal karsinogenez zincirinde konak genomuna entegrasyon sonrası kontrolsüz hücre çoğalmasını başlatan anahtar moleküler tetikleyici nedir?", [
            {"key": "A", "text": "E2 geninin bozulmasıyla E6 ve E7 onkoproteinlerinin aşırı ekspresyonu", "isCorrect": True, "explanation": "E2'nin kırılması E6 ve E7 fırtınasını başlatır."},
            {"key": "B", "text": "Hücrenin aniden hemoglobin üretmeye başlaması", "isCorrect": False, "explanation": "Eritrosit fonksiyonudur."},
            {"key": "C", "text": "Mide asidinin servikse dökülmesi", "isCorrect": False, "explanation": "Anatomik olarak imkansızdır."},
            {"key": "D", "text": "Tümör baskılayıcı p53 proteininin 1000 kat artması", "isCorrect": False, "explanation": "p53 artmaz, E6 ile parçalanır."}
        ])
    ]
    slides.append(make_slide(81, "Sentez: Etyolojiden Kliniğe Serviks Karsinogenez Zinciri", "HPV 16/18, transformasyon zonu, E2 kırılması, E6/E7 onkoproteinleri ve karsinom yolu", "Sentez: Karsinogenez Omurgası", s81_narrative, s81_bullets, s81_elements))

    # Slide 82: Sentez: Benign ve Malign Serviks Lezyonları Ayrımı
    s82_narrative = (
        "Klinik ve patolojik pratikte servikste karşılaşılan kitle ve lezyonların selim (benign) ve "
        "habis (malign) ayrımı, hastaya gereksiz radikal cerrahi yapılmasını önlemek açısından hayatidir.\n\n"
        "- **Endoservikal Polip (Benign):** Fibröz stroma ve mukus bezlerinden oluşur; **malign potansiyeli "
        "yoktur**. Ancak yüzeyel ülserasyonla kanama yaparak karsinomu taklit eder; **basit polipektomi** ile tam kür sağlanır.\n"
        "- **Naboth Kisti (Benign):** Skuamöz metaplazinin gland ağızlarını tıkamasıyla oluşan mukus dolu "
        "zararsız retansiyon kistleridir; tedavi dahi gerektirmez.\n"
        "- **İnvaziv Karsinom (Malign):** Stromal invazyon, atipi, nekroz ve metastaz potansiyeli taşır; "
        "fıçı serviks, parametrial fiksasyon ve üremiye yol açabilir; **radikal histerektomi veya kemoradyoterapi** gerektirir.\n\n"
        "> [!IMPORTANT]\n"
        "> [AYIRICI TANI] Endoservikal polip tamamen benigndir ve basit küretajla tedavi edilir; invaziv karsinom ise malign olup radikal cerrahi/kemoradyoterapi gerektirir."
    )
    s82_bullets = [
        "Endoservikal polip benigndir; kanamayla kanseri taklit eder, polipektomi yeterlidir.",
        "Naboth kistleri metaplazik tıkanmaya bağlı selim retansiyon kistleridir.",
        "İnvaziv karsinom stromayı yıkan, radikal tedavi gerektiren malignitedir."
    ]
    s82_elements = [
        make_cloze("Endoservikal polip tamamen benign olup malign potansiyeli kesinlikle bulunmayan ekzofitik bir lezyondur.", "benign", "Selim biyolojik davranış özelliği"),
        make_table("Servikal Lezyonlar Ayırıcı Tanı Tablosu", ["Patoloji", "Biyolojik Doğası", "Histolojik Karakter", "Tedavi Yaklaşımı"], [
            {"cells": [{"text": "Endoservikal Polip", "isMasked": False}, {"text": "Tamamen benign", "isMasked": True, "hint": "selim kitle lezyonu"}, {"text": "Mukus bezleri ve fibröz stroma", "isMasked": False}, {"text": "Basit polipektomi / küretaj"}]},
            {"cells": [{"text": "Naboth Kisti", "isMasked": False}, {"text": "Benign retansiyon kisti", "isMasked": False}, {"text": "Genişlemiş müsin dolu kleft", "isMasked": True, "hint": "mukus retansiyonu"}, {"text": "Tedavi gerekmez"}]},
            {"cells": [{"text": "İnvaziv SCC", "isMasked": False}, {"text": "Malign karsinom", "isMasked": False}, {"text": "Desmoplazi ve atipik skuamöz adalar", "isMasked": True, "hint": "stromayı istila eden kanser yuvaları"}, {"text": "Radikal cerrahi / Kemoradyoterapi"}]}
        ]),
        make_chain("Klinik Ayırıcı Tanı Yolu", [
            "1. Kanama Şikayeti: Hasta lekelenme veya ilişki sonrası kanamayla gelir.",
            "2. Spekulum Bakısı: Eksternal ostan sarkan polipoid kitle görülür.",
            "3. Biyopsi / Eksizyon: Lezyon patolojiye gönderilir.",
            "4. Ayrım: Eğer polipse polipektomi ile iş biter; kanserse radikal onkolojiye geçilir."
        ]),
        make_recall("Klinikte kanama yaparak serviks kanserini taklit eden en sık benign ekzofitik serviks lezyonu nedir?", "Endoservikal poliptir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Benign ve Malign Serviks Lezyonları", [
            {"text": "Endoservikal poliplerin malign potansiyeli yoktur.", "isLie": False, "explanation": "Doğru. Kesinlikle selim lezyonlardır."},
            {"text": "Naboth kistleri metaplazik bez tıkanmasına bağlı selim kistlerdir.", "isLie": False, "explanation": "Doğru. Tehlikesiz mukus birikimidir."},
            {"text": "Endoservikal polip saptanan hastaya derhal her iki bacağı ampute edilmelidir.", "isLie": True, "explanation": "Tuzak! Polip benign bir lezyondur, basit polipektomi yeterlidir; amputasyon yapılmaz."},
            {"text": "İnvaziv karsinom radikal histerektomi veya kemoradyoterapi gerektirir.", "isLie": False, "explanation": "Doğru. Malign onkolojik protokoldür."}
        ]),
        make_quiz("Servikal lezyonların klinik ve patolojik özellikleri ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Endoservikal polip - Malign potansiyeli olmayan benign ekzofitik lezyon", "isCorrect": True, "explanation": "Endoservikal polip selimdir ve malign potansiyel taşımaz."},
            {"key": "B", "text": "Naboth kisti - Kemik iliğine yayılan ölümcül sarkom", "isCorrect": False, "explanation": "Selim mukus retansiyon kistidir."},
            {"key": "C", "text": "İnvaziv skuamöz karsinom - Tedavi gerektirmeyen fizyolojik durum", "isCorrect": False, "explanation": "Hayatı tehdit eden malignitedir."},
            {"key": "D", "text": "Endoservikal polip - Sadece erkeklerde görülen testis lezyonu", "isCorrect": False, "explanation": "Uterus serviksine aittir."}
        ])
    ]
    slides.append(make_slide(82, "Sentez: Benign ve Malign Serviks Lezyonları Ayrımı", "Endoservikal polip, Naboth kisti, invaziv karsinom ayırıcı tanısı ve klinik davranış", "Sentez: Ayırıcı Tanı", s82_narrative, s82_bullets, s82_elements))

    # Slide 83: Sentez: SIL Doğal Seyir Tablosunun Konsolidasyonu
    s83_narrative = (
        "Servikal intraepitelyal lezyonların doğal seyrini özetleyen Robbins ve amfi ders notu tablosu, "
        "tüm klinik takip ve cerrahi karar algoritmalarının temel matematiksel dayanağıdır.\n\n"
        "- **LSIL (CIN I) Dinamiği:** Lezyonların **%60'ı spontan olarak geriler (regresyon)**; "
        "**%30'u sebat eder (persistans)**; yalnızca **%10'u HSIL'e ilerler**. Bu nedenle LSIL'e hemen "
        "bıçak vurulmaz, yakın takiple izlenir.\n"
        "- **HSIL (CIN II-III) Dinamiği:** Lezyonların **%30'u geriler**; **%60'ı sebat eder**; "
        "**%10'u invaziv karsinoma ilerler**. İlerleme **2 ila 10 yıllık** bir zaman aralığında gerçekleşir.\n"
        "- **Kritik Karşıtlık:** LSIL'de gerileme (%60) sebatın (%30) iki katıyken; HSIL'de sebat (%60) gerilemenin (%30) iki katıdır!\n\n"
        "> [!IMPORTANT]\n"
        "> [DOĞAL SEYİR SENTEZİ] LSIL: %60 geriler, %30 kalır, %10 HSIL'e gider. HSIL: %30 geriler, %60 kalır, %10 kansere gider (2-10 yıl). Bu oranlar ezbere bilinmelidir."
    )
    s83_bullets = [
        "LSIL: %60 geriler, %30 persiste kalır, %10 HSIL'e ilerler.",
        "HSIL: %30 geriler, %60 persiste kalır, %10 karsinoma ilerler.",
        "HSIL'den kansere ilerleme 2 ila 10 yıllık sürede gerçekleşir."
    ]
    s83_elements = [
        make_cloze("HSIL lezyonlarının sebat etme oranı yüzde 60 iken invaziv karsinoma ilerleme oranı yüzde 10'dur.", "yüzde 10", "HSIL'den kansere ilerleme yüzdesi"),
        make_table("SIL Doğal Seyir Matematiksel Matrisi", ["Lezyon Tipi", "Geriler (Regresyon)", "Persiste Kalır (Sebat)", "İlerler (Progresyon)"], [
            {"cells": [{"text": "LSIL (CIN I)", "isMasked": False}, {"text": "%60", "isMasked": True, "hint": "en büyük oran"}, {"text": "%30", "isMasked": False}, {"text": "%10 (HSIL'e)", "isMasked": True, "hint": "yüksek dereceye geçiş"}]},
            {"cells": [{"text": "HSIL (CIN II/III)", "isMasked": False}, {"text": "%30", "isMasked": False}, {"text": "%60", "isMasked": True, "hint": "sebat eden çoğunluk"}, {"text": "%10 (Karsinoma / 2-10 yıl)", "isMasked": False}]}
        ]),
        make_chain("Doğal Seyir Karşılaştırma Mantığı", [
            "1. LSIL Evresi: %60 gerileme gücü sayesinde lezyon çoğunlukla vücuttan silinir.",
            "2. İlerleyen %10: Azınlık grup HSIL basamağına sıçrar.",
            "3. HSIL Evresi: Sebat oranı %60'a fırlar, hücresel mutasyonlar kilitlenir.",
            "4. Kansere Geçiş: Kalan %10'luk grup 2-10 yıl içinde invaziv karsinoma dönüşür."
        ]),
        make_recall("LSIL ve HSIL lezyonlarının spontan gerileme (regresyon) ve sebat (persistans) oranları sırasıyla nasıldır?", "LSIL: %60 geriler, %30 sebat eder. HSIL: %30 geriler, %60 sebat eder."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SIL Doğal Seyir Tablosu", [
            {"text": "LSIL vakalarının %60'ı spontan geriler.", "isLie": False, "explanation": "Doğru. Regresyon baskındır."},
            {"text": "HSIL vakalarının %60'ı sebat eder, %10'u karsinoma ilerler.", "isLie": False, "explanation": "Doğru. Sebat baskındır, %10 kansere gider."},
            {"text": "LSIL vakalarının %100'ü 3 saniye içinde akciğere metastaz yapar.", "isLie": True, "explanation": "Tuzak! LSIL'in %60'ı kendiliğinden tamamen geriler; metastaz yapmaz."},
            {"text": "HSIL'den karsinoma ilerleme 2-10 yıl içinde gerçekleşir.", "isLie": False, "explanation": "Doğru. Zaman aralığı 2-10 yıldır."}
        ]),
        make_quiz("Robbins ve amfi ders notuna göre HSIL (CIN II-III) lezyonlarının doğal seyrinde sebat etme (persistans) oranı yüzde kaçtır?", [
            {"key": "A", "text": "%60", "isCorrect": True, "explanation": "HSIL vakalarının %60'ı persiste kalır."},
            {"key": "B", "text": "%0", "isCorrect": False, "explanation": "Sebat oranı çok yüksektir."},
            {"key": "C", "text": "%100", "isCorrect": False, "explanation": "%30'u geriler, %10'u ilerler."},
            {"key": "D", "text": "%1", "isCorrect": False, "explanation": "Gerçek oran %60'tır."}
        ])
    ]
    slides.append(make_slide(83, "Sentez: SIL Doğal Seyir Tablosunun Konsolidasyonu", "LSIL (%60 geriler / %30 kalır / %10 HSIL), HSIL (%30 geriler / %60 kalır / %10 kanser), 2-10 yıl", "Sentez: Doğal Seyir Matrisi", s83_narrative, s83_bullets, s83_elements))

    # Slide 84: Sentez: Pap Smear, Kolposkopi ve Biyopsi Entegrasyonu
    s84_narrative = (
        "Servikal neoplazi tanı triadında yer alan üç modalite (sitopatoloji, optik kolposkopi ve "
        "histopatoloji), birbirini tamamlayan kusursuz bir klinik akış oluşturur.\n\n"
        "- **Pap Smear (Sitolojik Filtre):** Dökülen hücrelerin incelenmesiyle asemptomatik popülasyonda "
        "displaziyi tarar. Hızlı, ucuz ve geniş kitlelere uygulanabilir; mortaliteyi %75 düşürmüştür.\n"
        "- **Kolposkopi (Optik Haritalama):** Asetik asit (%3-5) sürülerek artmış nükleer proteinlerin "
        "çökelmesi sağlanır; **asetobeyaz epitel** oluşturularak lezyonun sınırları mikroskobik lenslerle haritalanır.\n"
        "- **Biyopsi (Altın Standart Histoloji):** Asetobeyaz odaktan alınan doku örneğinde nükleer atipi, "
        "mitoz katmanı ve bazal membran bütünlüğü incelenerek kesin CIN evresi ve invazyon durumu rapor edilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [TANI TRİADI] Pap smear tarar ve şüpheyi doğurur; kolposkopi asetik asitle lezyonu görünür kılar; biyopsi kesin histopatolojik tanıyı koyar."
    )
    s84_bullets = [
        "Pap smear asemptomatik geniş kitleleri tarar.",
        "Kolposkopide asetik asit lezyonları asetobeyaz yapar ve hedefler.",
        "Biyopsi kesin CIN evresini ve stromal invazyonu kanıtlar."
    ]
    s84_elements = [
        make_cloze("Kolposkopi altında şüpheli asetobeyaz alandan alınan biyopsi kesin histopatolojik tanıyı koyan altın standarttır.", "biyopsi", "Kesin doku tanısını sağlayan örnekleme işlemi"),
        make_table("Tanı Triadının Karşılaştırmalı Rolleri", ["Modalite", "Tanı Düzeyi", "Başarı Anahtarı"], [
            {"cells": [{"text": "Pap Smear", "isMasked": False}, {"text": "Eksfoliyatif Sitoloji (Tarama)", "isMasked": True, "hint": "hücresel ön eleme"}, {"text": "Transformasyon zonunun örneklenmesi"}]},
            {"cells": [{"text": "Kolposkopi", "isMasked": False}, {"text": "Görsel Büyütme ve Haritalama", "isMasked": False}, {"text": "%3-5 asetik asit ile asetobeyaz odak", "isMasked": True, "hint": "protein çökmesiyle odak belirleme"}]},
            {"cells": [{"text": "Doku Biyopsisi", "isMasked": False}, {"text": "Histopatoloji (Kesin Tanı)", "isMasked": False}, {"text": "Katman derinliği ve invazyon kontrolü", "isMasked": True, "hint": "CIN evresi ve bazal membran kontrolü"}]}
        ]),
        make_chain("Üçlü Tanı Entegrasyon Akışı", [
            "1. Smear Filtresi: Yıllık taramada nükleer atipili SIL hücreleri dökülür.",
            "2. Kolposkopik Görselleştirme: Asetik asit uygulanarak beyaz displastik plaklar aydınlatılır.",
            "3. Punch Örnekleme: En yoğun asetobeyaz odaktan milimetrik doku parçası koparılır.",
            "4. Kesin Rapor: Patolog lezyonu CIN II olarak etiketleyip cerrahiye sevk eder."
        ]),
        make_recall("Serviks neoplazilerinin tanı sürecinde Pap smear, kolposkopi ve biyopsinin üstlendikleri temel görevler nelerdir?", "Pap smear şüpheyi tarar; kolposkopi asetik asitle lezyonu haritalar; biyopsi kesin histolojik tanıyı koyar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tanı Triadı Entegrasyonu", [
            {"text": "Pap smear tarama testidir ve mortaliteyi düşürmüştür.", "isLie": False, "explanation": "Doğru. Birincil tarama aracıdır."},
            {"text": "Kolposkopide asetik asit asetobeyaz reaksiyon oluşturur.", "isLie": False, "explanation": "Doğru. Lezyon opak beyazlaşır."},
            {"text": "Biyopsi yerine hastanın kahve falına bakılarak kanser evresi tayin edilir.", "isLie": True, "explanation": "Tuzak! Tıpta fal bakılmaz; kesin tanı histopatolojik doku biyopsisiyle konur."},
            {"text": "Kesin tanı biyopsi ile konur.", "isLie": False, "explanation": "Doğru. Altın standart histopatolojidir."}
        ]),
        make_quiz("Servikal intraepitelyal lezyonların klinik algoritmasında kesin tanıyı koyan altın standart basamak hangisidir?", [
            {"key": "A", "text": "Hedefe yönelik doku biyopsisinin histopatolojik incelemesi", "isCorrect": True, "explanation": "Kesin tanı daima doku biyopsisinin histopatolojisiyle konur."},
            {"key": "B", "text": "Yalnızca uzaktan çekilen cep telefonu fotoğrafı", "isCorrect": False, "explanation": "Tanısal değeri yoktur."},
            {"key": "C", "text": "Hastanın nabız sayısının dinlenmesi", "isCorrect": False, "explanation": "Vital bulgudur, karsinom tanısı koymaz."},
            {"key": "D", "text": "Kandaki kalsiyum düzeyi", "isCorrect": False, "explanation": "Biyokimyasal parametredir."}
        ])
    ]
    slides.append(make_slide(84, "Sentez: Pap Smear, Kolposkopi ve Biyopsi Entegrasyonu", "Sitolojik filtre, kolposkopik asetobeyaz haritalama, histopatolojik altın standart", "Sentez: Tanı Triadı", s84_narrative, s84_bullets, s84_elements))

    # Slide 85: Sentez: Histopatolojik Diferansiasyon ve Keratin İncileri
    s85_narrative = (
        "İnvaziv skuamöz hücreli karsinomun patoloji raporlarında yer alan diferansiasyon derecesi, "
        "tümörün ne kadar olgunlaştığını ve biyolojik agresyonunu yansıtır.\n\n"
        "- **İyi Diferansiye Skuamöz Karsinom (Grade 1):** Malign hücreler normal skuamöz epitelin "
        "özelliklerini büyük ölçüde taklit eder. Belirgin hücreler arası köprüler (dezmozomlar) ve en önemlisi "
        "doku merkezinde konsantrik laminasyon gösteren **keratin incileri (horn pearls)** izlenir.\n"
        "- **Zayıf (Kötü) Diferansiye Karsinom (Grade 3):** Hücreler anaplastik, aşırı pleomorfik ve "
        "yüksek mitotik indekslidir; **az keratinizasyon** gösterir veya hiç keratin üretmez.\n"
        "- **Klinik Yansıması:** Keratin incilerinin varlığı iyi diferansiasyon göstergesidir; diferansiasyon "
        "azaldıkça nüks ve lenf nodu metastazı riski tırmanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İyi diferansiye skuamöz serviks karsinomunda keratin incileri karakteristikken; zayıf diferansiye karsinomda az keratinizasyon saptanır."
    )
    s85_bullets = [
        "İyi diferansiye karsinomda konsantrik keratin incileri karakteristiktir.",
        "Zayıf diferansiye karsinomda az keratinizasyon ve belirgin anaplazi izlenir.",
        "Diferansiasyon azaldıkça lenf metastazı ve agresyon artar."
    ]
    s85_elements = [
        make_cloze("İyi diferansiye skuamöz karsinomun histopatolojik tanısında konsantrik keratin incileri patognomonik birikimdir.", "keratin incileri", "Laminasyon gösteren eozinofilik boynuz incisi"),
        make_table("Histopatolojik Diferansiasyon Karşılaştırma Matrisi", ["Derece", "Keratin İncesi Varlığı", "Sitomorfoloji ve Mitoz"], [
            {"cells": [{"text": "İyi Diferansiye (Grade 1)", "isMasked": False}, {"text": "Bol miktarda keratin incileri", "isMasked": True, "hint": "konsantrik keratin tabakaları"}, {"text": "Dezmozomlar belirgin, hafif-orta pleomorfizm"}]},
            {"cells": [{"text": "Zayıf Diferansiye (Grade 3)", "isMasked": False}, {"text": "Az keratinizasyon veya hiç yok", "isMasked": False}, {"text": "Aşırı anaplastik hücreler ve atipik bol mitoz", "isMasked": True, "hint": "şiddetli hücresel atipi"}]}
        ]),
        make_chain("Diferansiasyondan Dereceye", [
            "1. Stromal Yuvalar: Malign skuamöz hücreler desmoplastik stromaya oturur.",
            "2. Keratin Üretimi: Eğer hücreler olgunlaşabiliyorsa merkezde keratin toplar.",
            "3. İnci Oluşumu: Konsantrik lamine keratin incisi iyi diferansiasyonu kanıtlar.",
            "4. Olgunlaşma Kaybı: Hücreler keratin üretemezse zayıf diferansiye olarak derecelendirilir."
        ]),
        make_recall("Servikal invaziv skuamöz karsinomda histopatolojik olarak iyi diferansiyasyon ile zayıf diferansiyasyonu ayıran temel keratin bulgusu nedir?", "İyi diferansiyede belirgin keratin incileri izlenirken; zayıf diferansiyede az keratinizasyon izlenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Diferansiasyon ve Keratin İncileri", [
            {"text": "İyi diferansiye karsinomda keratin incileri karakteristiktir.", "isLie": False, "explanation": "Doğru. Klasik histopatoloji bulgusudur."},
            {"text": "Zayıf diferansiye tümörlerde az keratinizasyon saptanır.", "isLie": False, "explanation": "Doğru. Diferansiasyon kaybı göstergesidir."},
            {"text": "Keratin incileri tümör dokusunun içine yerleştirilmiş gerçek inci kolyelerdir.", "isLie": True, "explanation": "Tuzak! İstiridye incisi değil; mikroskobik konsantrik keratinize skuamöz protein birikimleridir."},
            {"text": "Diferansiasyon tümörün histopatolojik derecesini belirler.", "isLie": False, "explanation": "Doğru. Grade tayininde esastır."}
        ]),
        make_quiz("İnvaziv skuamöz serviks karsinomunda iyi diferansiasyonun mikroskobik kanıtı olan histolojik oluşum nedir?", [
            {"key": "A", "text": "Konsantrik keratin incileri (horn pearls)", "isCorrect": True, "explanation": "İyi diferansiye SCC'de keratin incileri karakteristiktir."},
            {"key": "B", "text": "Müsin gölleri", "isCorrect": False, "explanation": "Müsinöz adenokarsinoma aittir."},
            {"key": "C", "text": "Kemik iliği yağ vakuolleri", "isCorrect": False, "explanation": "Kemik dokusu bulgusudur."},
            {"key": "D", "text": "Psammoma cisimcikleri", "isCorrect": False, "explanation": "Seröz over veya tiroid tümörlerine aittir."}
        ])
    ]
    slides.append(make_slide(85, "Sentez: Histopatolojik Diferansiasyon ve Keratin İncileri", "İyi diferansiye SCC, keratin incileri, zayıf diferansiyede az keratinizasyon ve desmoplazi", "Sentez: Diferansiasyon", s85_narrative, s85_bullets, s85_elements))

    # Slide 86: Sentez: Lokal Yayılım ve Fıçı Serviks
    s86_narrative = (
        "İnvaziv serviks karsinomunun lokal yayılım biyolojisi, tümörün çevre dokuları nasıl kuşattığını "
        "ve cerrahi rezektabilite sınırlarının nasıl aşıldığını modeller.\n\n"
        "- **Fıçı Serviks Mekanizması:** Karsinom endoservikal mukozadan başlayarak servikal stromayı "
        "çepeçevre sarar ve derinlemesine infiltre eder. Serviks kalınlaşır, sertleşir ve palpasyonda "
        "**rijit bir silindir/fıçı halini alır (fıçı serviks)**.\n"
        "- **Parametrial Yayılım ve Fiksasyon:** Tümör lateraldeki bağ dokusuna taştığında uterus "
        "pelvik yan duvarlara yapışır; **pelvik fiksasyon** gelişir ve cerrahi şansı ortadan kalkar.\n"
        "- **Klinik Önem:** Fıçı serviks ve parametrial tutulum varlığı, hastanın radikal cerrahiden "
        "çıkarılıp doğrudan kemoradyoterapiye yönlendirilmesini gerektirir.\n\n"
        "> [!IMPORTANT]\n"
        "> [LOKAL YAYILIM SENTEZİ] Derin stromal invazyon = Fıçı serviks (kalın, rijit silindir). Lateral bağ dokusu tutulumu = Parametrial yayılım ve pelvik fiksasyon."
    )
    s86_bullets = [
        "Derin stromal invazyon kalın, rijit silindirik 'fıçı serviks' oluşturur.",
        "Lateral parametrial yayılım uterusun pelvise fikse olmasına yol açar.",
        "Pelvik fiksasyon inoperabilite ve kemoradyoterapi endikasyonudur."
    ]
    s86_elements = [
        make_cloze("Servikal stromanın derin invazyonuyla serviksin sert silindirik şekil almasına fıçı serviks adı verilir.", "fıçı serviks", "Derin stromal invazyonun karakteristik morfolojik adı"),
        make_table("Lokal Yayılım Durakları ve Klinik Karşılıkları", ["Yayılım Yönü", "Patolojik İnvazyon", "Klinik Yansıması"], [
            {"cells": [{"text": "Derin Servikal Stroma", "isMasked": False}, {"text": "Çepeçevre stromal kalınlaşma", "isMasked": True, "hint": "stromanın tam kat tutulumu"}, {"text": "Fıçı serviks (kalın, rijit silindir palpasyonu)"}]},
            {"cells": [{"text": "Lateral Parametrium", "isMasked": False}, {"text": "Pelvik bağ dokusu infiltrasyonu", "isMasked": False}, {"text": "Uterusun pelvik duvara fiksasyonu", "isMasked": True, "hint": "uterusun hareketsizleşmesi"}]}
        ]),
        make_chain("Lokal Yayılım Basamakları", [
            "1. Endoservikal Kitle: Tümör stromal lifler arasına derinlemesine sızar.",
            "2. Fıçı Serviks: Serviks sertleşip kalınlaşarak fıçı kıvamına gelir.",
            "3. Parametrial Köprü: Kanser lateral pelvik ligamentleri ve bağ dokusunu istila eder.",
            "4. Pelvik Fiksasyon: Uterus yan duvarlara kilitlenir ve inoperabilite ilan edilir."
        ]),
        make_recall("Serviks kanserinde derin stromal invazyon ile lateral parametrial yayılımın jinekolojik muayenedeki iki majör bulgusu nedir?", "Derin stromal invazyon 'fıçı serviks'e; parametrial yayılım ise 'pelvik fiksasyon'a (uterusun hareketsizleşmesine) yol açar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Lokal Yayılım ve Fıçı Serviks", [
            {"text": "Fıçı serviks derin stromal invazyon sonucu kalın, rijit bir servikstir.", "isLie": False, "explanation": "Doğru. Tipik klinik makroskopi bulgusudur."},
            {"text": "Parametrial yayılım uterusun pelvik yan duvara fikse olmasına yol açar.", "isLie": False, "explanation": "Doğru. Pelvik fiksasyon nedenidir."},
            {"text": "Fıçı serviks geliştiğinde hastanın kalbi tamamen durup yerini bir fıçı şaraba bırakır.", "isLie": True, "explanation": "Tuzak! Fıçı serviks tümörün serviksi kalınlaştırıp rijit bir silindir yapmasıdır; kalple veya şarapla ilgisi yoktur."},
            {"text": "Parametrial tutulum cerrahi yerine kemoradyoterapi gerektirir.", "isLie": False, "explanation": "Doğru. İnoperabilite kriteridir."}
        ]),
        make_quiz("İnvaziv serviks karsinomunda uterusun pelvik yan duvarlara fikse olmasına yol açan yayılım yolu hangisidir?", [
            {"key": "A", "text": "Tümörün lateralde parametriumlara yayılması", "isCorrect": True, "explanation": "Parametrial yayılım pelvik fiksasyon oluşturur."},
            {"key": "B", "text": "Yalnızca saç diplerinde kepeklenme olması", "isCorrect": False, "explanation": "Dermatolojik durumdur."},
            {"key": "C", "text": "Topuk dikeninin büyümesi", "isCorrect": False, "explanation": "Ortopedik patolojidir."},
            {"key": "D", "text": "Kanda demir düşüklüğü", "isCorrect": False, "explanation": "Anemi bulgusudur."}
        ])
    ]
    slides.append(make_slide(86, "Sentez: Lokal Yayılım ve Fıçı Serviks", "Stromal derinlik, fıçı serviks morfolojisi, lateral parametrium invazyonu ve pelvik fiksasyon", "Sentez: Lokal Yayılım", s86_narrative, s86_bullets, s86_elements))

    # Slide 87: Sentez: Üremi ve Ölümcül Komplikasyonlar
    s87_narrative = (
        "İleri evre serviks kanserli hastalarda gelişen ölümcül komplikasyonlar spektrumu, "
        "tümörün üreterler, damarlar ve komşu organlarla kurduğu yıkıcı ilişkiyi gösterir.\n\n"
        "- **Bilateral Üreter Basısı ve Üremi:** Serviksin hemen iki yanından geçen üreterler "
        "tümör kitlesi tarafından dışarıdan ezilir. Bilateral idrar akımı durur, böbrekler genişler "
        "(hidronefroz) ve hasta **terminal üremi (böbrek yetmezliği)** koması ile kaybedilir; **bu en sık ölüm nedenidir**.\n"
        "- **Fistüller ve İnfeksiyonlar:** Mesane veya rektumun delinmesiyle vezikovajinal/rektovajinal "
        "fistüller açılır; sürekli idrar/gayta kaçağı ağır pelvik peritonit ve ürosepsise zemin hazırlar.\n"
        "- **Vasküler ve Nöral Baskı:** Masif lenfödem ve dindirilemeyen siyataljiler hastanın genel durumunu çökertir.\n\n"
        "> [!IMPORTANT]\n"
        "> [ÖLÜM NEDENİ SENTEZİ] İleri evre serviks kanserinde en sık ölüm nedeni: Parametrial yayılımla üreterlerin sıkışması → Bilateral hidronefroz → Terminal üremidir."
    )
    s87_bullets = [
        "En sık ölüm nedeni bilateral üreter obstrüksiyonuna bağlı üremidir.",
        "Parametrial tümör üreterleri dışarıdan sıkıştırarak hidronefroz yapar.",
        "Fistüller ve ürosepsis tabloyu ağırlaştıran diğer ölümcül komplikasyonlardır."
    ]
    s87_elements = [
        make_cloze("İleri evre serviks karsinomunda üreterlerin tıkanmasıyla oluşan bilateral hidronefroz ve terminal üremi en sık ölüm nedenidir.", "üremi", "Böbrek iflasına bağlı fatal son tablo"),
        make_table("Ölümcül Komplikasyonlar Sentez Tablosu", ["Komplikasyon", "Temel Patofizyoloji", "Sonuç"], [
            {"cells": [{"text": "Terminal Üremi", "isMasked": False}, {"text": "Bilateral üreter obstrüksiyonu ve hidronefroz", "isMasked": True, "hint": "üreter kanalının kapanması"}, {"text": "En sık ölüm nedeni (renal yetmezlik)"}]},
            {"cells": [{"text": "Vezikovajinal Fistül", "isMasked": False}, {"text": "Tümörün mesaneyi delmesi ve nekrozu", "isMasked": False}, {"text": "Sürekli idrar kaçağı ve ağır pelvik sepsisi", "isMasked": True, "hint": "enfeksiyon ve idrar sızıntısı"}]}
        ]),
        make_chain("Ölümcül Zincirin Konsolidasyonu", [
            "1. Parametrial İnvazyon: Karsinom üreterlerin geçtiği tüneli infiltre eder.",
            "2. Üreter Lümen Tıkanması: İdrar yukarıda birikerek hidroüreter ve hidronefroz yapar.",
            "3. Renal Parankim Atrofisi: Nefronlar ezilerek glomerüler filtrasyon çöker.",
            "4. Terminal Üremi: Kanda toksik nitrojen birikimiyle hasta kaybedilir."
        ]),
        make_recall("İleri evre serviks karsinomunda hastaların hayatını kaybetmesine yol açan en yaygın komplikasyon nedir?", "Tümörün üreterleri bilateral sıkıştırması sonucu gelişen hidronefroz ve terminal üremidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ölümcül Komplikasyonlar", [
            {"text": "En sık ölüm nedeni bilateral üreter basısına bağlı üremidir.", "isLie": False, "explanation": "Doğru. Majör ölüm mekanizmasıdır."},
            {"text": "Bilateral hidronefroz böbrek yetmezliğine yol açar.", "isLie": False, "explanation": "Doğru. İdrar çıkışı engellenir."},
            {"text": "Serviks kanseri hastaları sadece kulak kepçesinin donması nedeniyle ölür.", "isLie": True, "explanation": "Tuzak! Fatal neden üreter basısına bağlı gelişen terminal üremidir; kulak donması değildir."},
            {"text": "Vezikovajinal ve rektovajinal fistüller ileri evrede görülebilir.", "isLie": False, "explanation": "Doğru. Ağır organ perforasyonlarıdır."}
        ]),
        make_quiz("İleri evre serviks karsinomunun doğal seyrinde en sık görülen ölüm nedeni hangisidir?", [
            {"key": "A", "text": "Bilateral üreter obstrüksiyonu sonucu gelişen terminal üremi", "isCorrect": True, "explanation": "Üreter basısına bağlı üremi en sık ölüm nedenidir."},
            {"key": "B", "text": "Bilateral katarakt ameliyatı komplikasyonu", "isCorrect": False, "explanation": "Göz cerrahisidir."},
            {"key": "C", "text": "Günde bir fincan kahve içilmesi", "isCorrect": False, "explanation": "Ölümcül değildir."},
            {"key": "D", "text": "Ayak tırnağı batması", "isCorrect": False, "explanation": "Ölüm nedeni olamaz."}
        ])
    ]
    slides.append(make_slide(87, "Sentez: Üremi ve Ölümcül Komplikasyonlar", "Üreter komşuluğu, hidronefroz, renal yetmezlik, fistüller ve fatal komplikasyonlar", "Sentez: Terminal Komplikasyonlar", s87_narrative, s87_bullets, s87_elements))

    # Slide 88: Sentez: Mikroinvazyondan Radikal Cerrahiye Tedavi
    s88_narrative = (
        "İnvaziv serviks karsinomunda cerrahi ve onkolojik tedavi haritası, tümörün stromal derinliği "
        "ve pelvik yayılım sınırlarına göre katı basamaklara ayrılır.\n\n"
        "- **Mikroinvaziv Karsinom (≤3 mm):** Pelvik lenf nodu metastaz riski <%1 olduğundan doğurganlığı "
        "korumak isteyen genç kadınlarda cerrahi sınırları temiz **konik biyopsi (konizasyon)** ile kür sağlanabilir.\n"
        "- **Erken İnvaziv Karsinom (Evre IB - IIA):** Mikroinvazyonu aşmış fakat pelvise fikse olmamış olgularda "
        "altın standart **radikal histerektomi ve bilateral pelvik lenf düğümü diseksiyonudur**.\n"
        "- **İleri Evre Karsinom (Evre IIB - IV):** Parametriumların dışına taşmış veya pelvik duvara fikse olgularda "
        "cerrahi şansı kalmamıştır; kür şansı sunan tek yöntem **kombine kemoradyoterapidir**.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEDAVİ ALGORİTMASI] Mikroinvaziv (≤3 mm) → Konik biyopsi. Erken invaziv → Radikal histerektomi + Lenfadenektomi. İleri evre / Fikse → Kemoradyoterapi."
    )
    s88_bullets = [
        "Mikroinvaziv karsinom (≤3 mm) konik biyopsi ile tedavi edilebilir.",
        "Erken invaziv kanserde radikal histerektomi + pelvik lenf diseksiyonu esastır.",
        "İleri evre/fikse olgularda standart tedavi kombine kemoradyoterapidir."
    ]
    s88_elements = [
        make_cloze("Mikroinvaziv karsinom olgularında doğurganlığı koruyan cerrahi yöntem konik biyopsi olarak bilinir.", "konik biyopsi", "Mikroinvazyonda uygulanan organ koruyucu rezeksiyon"),
        make_table("Evrelere Göre Tedavi Modaliteleri Sentezi", ["Klinik Evre / Durum", "Primer Tedavi Yaklaşımı", "Klinik Amaç ve Not"], [
            {"cells": [{"text": "Mikroinvaziv (≤3 mm)", "isMasked": False}, {"text": "Konik biyopsi (konizasyon)", "isMasked": True, "hint": "organ koruyucu küçük cerrahi"}, {"text": "Lenf nodu riski <%1, fertilite korunur"}]},
            {"cells": [{"text": "Erken İnvaziv (IB - IIA)", "isMasked": False}, {"text": "Radikal histerektomi + Pelvik lenfadenektomi", "isMasked": False}, {"text": "Primer kitle ve lenf istasyonlarının rezeksiyonu", "isMasked": True, "hint": "geniş cerrahi sınırla çıkarma"}]},
            {"cells": [{"text": "İleri Evre / Fikse (≥IIB)", "isMasked": False}, {"text": "Kombine kemoradyoterapi", "isMasked": True, "hint": "radyasyon ve kemoterapi birlikteliği"}, {"text": "İnoperabl olguda lokal kontrol ve kür"}]}
        ]),
        make_chain("Tedavi Karar Algoritması Sentezi", [
            "1. Biyopsi Derinliği: Stromal invazyon 2 mm ise konik biyopsi ile kür sağlanır.",
            "2. Makroskopik Kitle: 3 cm'lik servikse sınırlı kitlede radikal histerektomi yapılır.",
            "3. Parametrial Tutulum: Tümör duvara fikseyse cerrahi iptal edilir.",
            "4. Radyoterapi Masası: İnoperabl hastaya eksternal ışın ve sisplatin verilir."
        ]),
        make_recall("Serviks kanserinde (1) Mikroinvaziv karsinom, (2) Erken invaziv karsinom ve (3) İleri evre karsinomun standart primer tedavileri nelerdir?", "(1) Konik biyopsi, (2) Radikal histerektomi + pelvik lenf diseksiyonu, (3) Kemoradyoterapidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tedavi Algoritması Sentezi", [
            {"text": "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.", "isLie": False, "explanation": "Doğru. Lenf riski <%1'dir."},
            {"text": "Erken invaziv kanserde radikal histerektomi ve lenf diseksiyonu uygulanır.", "isLie": False, "explanation": "Doğru. Standart cerrahidir."},
            {"text": "İleri evre kanser hastalarına sadece papatya çayı içirilip eve gönderilir.", "isLie": True, "explanation": "Tuzak! İleri evrede kemoradyoterapi gibi yoğun ve agresif onkolojik tedavi uygulanır."},
            {"text": "Pelvik duvara fikse olgularda kemoradyoterapi verilir.", "isLie": False, "explanation": "Doğru. Cerrahi dışı standarttır."}
        ]),
        make_quiz("Serviks karsinomunda mikroinvaziv karsinomun standart küratif cerrahi tedavisi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Konik biyopsi (konizasyon)", "isCorrect": True, "explanation": "Mikroinvaziv karsinom konik biyopsi ile küratif tedavi edilebilir."},
            {"key": "B", "text": "Karaciğer nakli", "isCorrect": False, "explanation": "Endikasyonu yoktur."},
            {"key": "C", "text": "Sadece kolesterol düşürücü hap", "isCorrect": False, "explanation": "Kanser cerrahisi değildir."},
            {"key": "D", "text": "Mide küçültme ameliyatı", "isCorrect": False, "explanation": "Bariyatrik cerrahidir."}
        ])
    ]
    slides.append(make_slide(88, "Sentez: Mikroinvazyondan Radikal Cerrahiye Tedavi", "Mikroinvaziv konizasyon, radikal Wertheim operasyonu, inoperabilite ve kemoradyoterapi", "Sentez: Tedavi Algoritması", s88_narrative, s88_bullets, s88_elements))

    # Slide 89: Sentez: Aşılama, Tarama ve Koruyucu Onkoloji Zaferi
    s89_narrative = (
        "Modern koruyucu tıbbın en büyük zaferi, serviks kanserinin etiyolojisi bilinen, aşısı "
        "bulunan ve preinvaziv lezyonları taranarak %100'e yakın önlenebilen bir hastalık olmasıdır.\n\n"
        "- **Halk Sağlığı Başarısı:** Pap smear eksfoliyatif sitolojisi mortaliteyi **%75 oranında düşürmüştür**. "
        "HPV DNA testi eklenerek 30 yaş üstünde **5 yıllık negatif güvence** sağlanmıştır.\n"
        "- **Aşı İle Eradikasyon:** Rekombinant L1 VLP aşıları (4'lü ve 9'lu) 11-12 yaş kız ve erkeklere "
        "uygulanarak enfeksiyon rezervuarını kurutur ve **en az 10 yıl** koruma sağlar.\n"
        "- **Geleceğin Vizyonu:** DSÖ hedefi doğrultusunda aşı, moleküler test ve sitoloji entegre "
        "edildiğinde serviks kanseri insanlık tarihinde yeryüzünden silinen ilk malignite olma potansiyeline sahiptir.\n\n"
        "> [!IMPORTANT]\n"
        "> [KORUYUCU HEKİMLİK ZİRVESİ] Pap smear ölümleri %75 azalttı; HPV testi 5 yıllık güvence verdi; VLP aşısı cinsiyetsiz uygulandığında serviks kanserini tamamen önlenebilir kıldı."
    )
    s89_bullets = [
        "Pap smear serviks kanseri mortalitesini %75 azalttı.",
        "HPV DNA testi negatifliği 5 yıllık güçlü güvence sağlar.",
        "VLP aşıları en az 10 yıl korur ve hastalığı eradike edebilir."
    ]
    s89_elements = [
        make_cloze("Pap smear tarama programları serviks kanseri mortalitesinde yaklaşık yüzde 75 azalma sağlamıştır.", "yüzde 75", "Sitolojik taramanın sağladığı mortalite düşüş yüzdesi"),
        make_table("Koruyucu Onkoloji Kazanımları Matrisi", ["Koruyucu Araç", "Sağlanan Klinik / Epidemiyolojik Başarı", "Kritik Kural"], [
            {"cells": [{"text": "Pap Smear", "isMasked": False}, {"text": "%75 mortalite azalması", "isMasked": True, "hint": "ölüm oranındaki düşüş"}, {"text": "Transformasyon zonu örneklenmeli"}]},
            {"cells": [{"text": "HPV DNA Testi", "isMasked": False}, {"text": "5 yıllık güvenli neoplazisiz pencere", "isMasked": False}, {"text": "Özellikle ≥30 yaşta değerli", "isMasked": True, "hint": "erişkin tarama eşiği"}]},
            {"cells": [{"text": "HPV Aşılaması", "isMasked": False}, {"text": "En az 10 yıl koruma, >%90 kanser önleme", "isMasked": False}, {"text": "Taramanın yerine geçmez, birlikte uygulanır", "isMasked": True, "hint": "tarama zorunluluğunun devamı"}]}
        ]),
        make_chain("Koruyucu Onkoloji Entegrasyonu", [
            "1. Aşılama: Çocuklukta VLP aşısı ile immün nötralizan bariyer kurulur.",
            "2. Erişkin Tarama: 30 yaş üstünde HPV DNA ve Pap ko-testi yapılır.",
            "3. 5 Yıllık Güven: Negatif sonuçlarla hasta 5 yıl boyunca güvenle izlenir.",
            "4. Sıfır Mortalite: İnvaziv kanser gelişimi tamamen durdurularak başarı tamamlanır."
        ]),
        make_recall("Serviks kanserinde koruyucu onkolojinin üç temel kazanımı olan (1) Pap smear mortalite düşüşü, (2) HPV DNA negatiflik süresi ve (3) Minimum aşı koruma süresi nedir?", "(1) %75 mortalite düşüşü, (2) 5 yıllık güvenlik güvencesi, (3) En az 10 yıllık aşı korumasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Koruyucu Onkoloji Zaferi", [
            {"text": "Pap smear mortalitede yaklaşık %75 azalma sağlamıştır.", "isLie": False, "explanation": "Doğru. Kanıtlanmış başarıdır."},
            {"text": "HPV aşısının koruma süresi en az 10 yıldır.", "isLie": False, "explanation": "Doğru. Klinik takiple sabittir."},
            {"text": "Aşılanan bir kadında kanser taramaları yasaklanır ve hekime gitmek suç sayılır.", "isLie": True, "explanation": "Tuzak! Aşı taramanın yerine geçmez; aşılananlar da rutin taramaya devam etmelidir."},
            {"text": "HPV DNA testi negatifse 5 yıl neoplazi riski çok düşüktür.", "isLie": False, "explanation": "Doğru. 5 yıllık penceredir."}
        ]),
        make_quiz("Servikal kanser tarama ve korunma protokollerinin entegre başarısı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Pap testi ölümleri %75 azaltmıştır ve aşıyla birlikte kanser önlenebilir hale gelmiştir", "isCorrect": True, "explanation": "Pap smear %75 düşüş sağlamış, aşıyla koruma zirveye ulaşmıştır."},
            {"key": "B", "text": "Tarama ve aşıların serviks kanserine hiçbir faydası olmamıştır", "isCorrect": False, "explanation": "Aksine tıbbın en büyük başarısıdır."},
            {"key": "C", "text": "Aşılar kanser sıklığını 50 kat artırmıştır", "isCorrect": False, "explanation": "Kanser sıklığını dramatik azaltmıştır."},
            {"key": "D", "text": "Sadece 80 yaş üstü erkeklerde aşı yapılmalıdır", "isCorrect": False, "explanation": "11-12 yaş kız ve erkeklere yapılır."}
        ])
    ]
    slides.append(make_slide(89, "Sentez: Aşılama, Tarama ve Koruyucu Onkoloji Zaferi", "%75 mortalite düşüşü, 5 yıl güvencesi, en az 10 yıl aşı koruması ve üçlü eliminasyon", "Sentez: Koruyucu Zafer", s89_narrative, s89_bullets, s89_elements))

    # Slide 90: [TEKRAR SAYFASI - CHECKPOINT 9] Karsinogenez, Tanı ve Tedavi Büyük Sentezi
    s90_narrative = (
        "Bölüm 9'da serviks hastalıkları, HPV virolojisi, preinvaziv lezyonlar ve invaziv karsinomun "
        "tüm klinik-patolojik omurgasını büyük bir sentez halinde konsolide ettik.\n\n"
        "- **Karsinogenez Formülü:** HPV 16/18 → Transformasyon zonu → E2 parçalanması → E6 (p53 yıkımı) ve E7 (RB blokajı).\n"
        "- **Doğal Seyir Matrisi:** LSIL: %60 geriler, %30 kalır, %10 HSIL. HSIL: %30 geriler, %60 kalır, %10 kanser (2-10 yıl).\n"
        "- **Klinik ve Ölüm:** En sık semptom beklenmedik/postkoital vajinal kanama; en sık ölüm nedeni "
        "bilateral üreter basısına bağlı **terminal üremidir**.\n"
        "- **Tedavi Protokolü:** Mikroinvaziv (≤3 mm) = **konik biyopsi**; erken evre = **radikal histerektomi**; "
        "ileri evre / pelvik fiksasyon = **kemoradyoterapi**.\n"
        "- **Koruyucu Zafer:** Pap smear mortaliteyi **%75 azalttı**; aşı **en az 10 yıl korur**; formül **Pap + HPV + Aşıdır**.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 9 BÜYÜK SENTEZİ] HPV E6/E7 ile başlar; LSIL %60 gerilerken HSIL kansere ilerler; fıçı serviks derin invazyonu, üremi ölümü simgeler; mikroinvazyonda konizasyon, ileri evrede kemoradyoterapi kür sağlar."
    )
    s90_bullets = [
        "HPV E6 (p53) ve E7 (RB) onkoproteinleri karsinogenezin ana motorudur.",
        "LSIL %60 geriler; HSIL %60 sebat edip %10 kansere ilerler (2-10 yıl).",
        "En sık ölüm nedeni bilateral üreter basısına bağlı terminal üremidir.",
        "Mikroinvaziv konik biyopsi ile, ileri evre kemoradyoterapi ile tedavi edilir."
    ]
    s90_elements = [
        make_cloze("Bölüm 9 büyük sentezinde yinelenen en sık ölüm nedeni üreter basısına bağlı terminal üremi tablosudur.", "üremi", "Checkpoint 9'da konsolide edilen fatal böbrek komplikasyonu"),
        make_table("Büyük Sentez Konsolidasyon Tablosu", ["Konsept", "Kritik Tıbbi Kural / Değer", "Klinik Yansıması"], [
            {"cells": [{"text": "Karsinogenez Motoru", "isMasked": False}, {"text": "E6 (p53 yıkımı) ve E7 (RB inaktivasyonu)", "isMasked": True, "hint": "tümör baskılayıcı yıkımı"}, {"text": "Hücre döngüsü kontrolünün bozulması"}]},
            {"cells": [{"text": "En Sık Ölüm Nedeni", "isMasked": False}, {"text": "Üreter basısına bağlı terminal üremi", "isMasked": False}, {"text": "Bilateral hidronefroz ve renal iflas", "isMasked": True, "hint": "idrar kanalının kapanması"}]},
            {"cells": [{"text": "Mikroinvaziv Tedavi", "isMasked": False}, {"text": "Konik biyopsi (konizasyon)", "isMasked": True, "hint": "organ koruyucu eksizyon"}, {"text": "Lenf riski <%1 olduğundan tam kür"}]}
        ]),
        make_chain("Büyük Sentez Süreç Entegrasyonu", [
            "1. Moleküler Başlangıç: E6 ve E7 p53 ve RB'yi yok ederek genomu yıkar.",
            "2. Preinvaziv Durak: HSIL epitelin tam katını kaplar ve 2-10 yılda kansere gider.",
            "3. Klinik Tablo: Fıçı serviks ve parametrial yayılım üreterleri boğar.",
            "4. Tedavi ve Koruma: Mikroinvazyonda konizasyon hayat kurtarır; üçlü strateji kanseri bitirir."
        ]),
        make_recall("Bölüm 9 büyük sentezinde öğrendiğimiz: (1) İki onkoprotein hedefi, (2) En sık ölüm nedeni ve (3) Mikroinvaziv karsinom tedavisi nedir?", "(1) E6 p53'ü yıkar, E7 RB'yi inaktive eder, (2) Terminal üremi, (3) Konik biyopsidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 9 Büyük Sentez", [
            {"text": "E6 p53'ü yıkar, E7 RB'ye bağlanarak E2F'yi serbest bırakır.", "isLie": False, "explanation": "Doğru. Klasik moleküler formüldür."},
            {"text": "En sık ölüm nedeni üreter obstrüksiyonuna bağlı üremidir.", "isLie": False, "explanation": "Doğru. Majör ölüm nedenidir."},
            {"text": "Serviks kanseri hastalarında tümör hücresi yerine sadece altın külçeleri ürer.", "isLie": True, "explanation": "Tuzak! Malign karsinom dokusu ürer; altın veya maden üretimi imkansızdır."},
            {"text": "Mikroinvaziv karsinom konik biyopsi ile tedavi edilebilir.", "isLie": False, "explanation": "Doğru. Cerrahi kür yöntemidir."}
        ]),
        make_quiz("Bölüm 9'da konsolide edilen tüm serviks kanseri patolojisinde aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Mikroinvaziv karsinom - Zorunlu kemoradyoterapi ve kemik iliği nakli", "isCorrect": True, "explanation": "Yanlış eşleştirme! Mikroinvaziv karsinom konik biyopsi ile tedavi edilir, kemoradyoterapi gerekmez."},
            {"key": "B", "text": "E6 onkoproteini - p53 yıkımı ve telomeraz artışı", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "C", "text": "E7 onkoproteini - Retinoblastoma (RB) bağlanması ve E2F salınımı", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "D", "text": "En sık ölüm nedeni - Bilateral hidronefroz ve terminal üremi", "isCorrect": False, "explanation": "Doğru eşleştirmedir."}
        ])
    ]
    slides.append(make_slide(90, "[TEKRAR SAYFASI - CHECKPOINT 9] Karsinogenez, Tanı ve Tedavi Büyük Sentezi", "Bölüm 9 kapsamlı tekrarı: moleküler omurga, ayırıcı tanı, doğal seyir matrisi ve tedavi", "Bölüm Tekrarı ve Konsolidasyon", s90_narrative, s90_bullets, s90_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec9()
    print(f"Sec9 generated: {len(slides)} slides (Slide 81 to 90)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
