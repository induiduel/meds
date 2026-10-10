from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec10():
    slides = []

    # Slide 91
    narrative_91 = """Sifiliz tedavisinde altın standart penisilin olmakla birlikte, hastada anafilaktik penisilin alerjisi öyküsü varsa alternatif stratejiler izlenir. Alerji durumunda, enfeksiyonun evresine ve hastanın durumuna (özellikle gebelik) göre karar verilir.
*   **Alternatif İlaçlar:** Gebe olmayan, nörosifiliz dışı evrelerdeki penisilin alerjik hastalarda genellikle **Doksisiklin** (veya Tetrasiklin) kullanılır. (14 veya 28 gün süreli).
*   **Desensitizasyon Zorunluluğu:** Nörosifiliz hastalarında veya gebe kadınlarda (tetrasiklinler teratojenik olduğu için kullanılamaz) penisilinin yerini tutacak tam bir alternatif yoktur. Bu hastalarda zorunlu olarak **penisilin desensitizasyonu** (duyarsızlaştırma) yapılır ve ardından yine penisilin verilir.
> Gebede veya nörosifilizde sifiliz saptanırsa ve hasta penisiline alerjik ise: "Alerjiyi yen ve penisilin ver!" kuralı geçerlidir.
"""
    slide_91 = make_slide(
        title="Penisilin Alerjisinde Alternatif Tedavi Yaklaşımları",
        narrative=narrative_91,
        elements=[
            make_cloze("Gebe olmayan erken sifilizli penisilin alerjik hastalarda genellikle alternatif olarak {{c1::Doksisiklin::ilaç}} veya Tetrasiklin kullanılır."),
            make_cloze("Nörosifiliz hastalarında veya gebe kadınlarda penisilin alerjisi varsa mutlaka penisilin {{c1::desensitizasyonu::işlem}} yapılmalıdır."),
            make_cloze("Gebe kadınlarda fetüse zararlı (teratojenik) oldukları için alternatif tedavi olan {{c1::tetrasiklinler::ilaç grubu}} kesinlikle kontrendikedir."),
            make_recall("Penisilin alerjisi olan, primer sifiliz saptanan GEBE bir kadında tedavi nasıl yönetilir?", "Hastaya penisilin desensitizasyonu uygulanır ve ardından penisilin tedavisi verilir."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilizde penisilin alerjisi yönetimi.",
                "Penisilin alerjisi olan gebe bir hastaya güvenli alternatif olarak doksisiklin başlanmalıdır.",
                "Doksisiklin ve diğer tetrasiklinler gebelikte teratojenik etkileri nedeniyle kesinlikle kullanılamazlar; gebelerde desensitizasyon + penisilin şarttır.",
                [
                    "Gebe olmayan erişkinlerde sekonder sifiliz tedavisinde doksisiklin bir alternatiftir.",
                    "Nörosifiliz tedavisinde desensitizasyon yapılarak kristalize penisilin vermek tek güvenilir yoldur.",
                    "Penisilin desensitizasyonu, alerjiyi geçici olarak baskılamak için küçük dozlarla başlayıp dozu artırarak uygulanan bir protokoldür."
                ]
            )
        ]
    )
    slides.append(slide_91)

    # Slide 92
    narrative_92 = """Sifiliz tedavisinin ne kadar başarılı olduğunu anlamak için, non-treponemal testler (VDRL/RPR) kullanılarak serolojik takip yapılır. Başarılı bir tedavi sonrasında, kandaki inflamasyon azaldıkça lipoidal antikor titrelerinin belirgin şekilde düşmesi beklenir.
*   **Başarı Kriteri:** Tedaviden sonraki 6-12 ay içinde (erken sifilizde), VDRL veya RPR titresinde **en az 4 kat (2 dilüsyon)** düşüş görülmesi (örn; 1:32'den 1:8'e inmesi) kür (iyileşme) kanıtıdır.
*   **Başarısızlık (Klinik Nüks):** Titrenin düşmemesi veya 4 kat artması tedavinin başarısız olduğunu veya hastanın yeniden enfekte olduğunu gösterir.
> Unutmayın, sadece non-treponemal testler miktar (titre) belirtir ve tedavi takibinde kullanılır. Treponemal testler (TPHA) zaten ömür boyu pozitif kalacağı için takibe yaramazlar.
"""
    slide_92 = make_slide(
        title="Tedavi Yanıtının Serolojik Takibi: Titrede Düşüş Kriteri",
        narrative=narrative_92,
        elements=[
            make_cloze("Sifilizde tedavi başarısını izlemek için titre veren {{c1::non-treponemal::test grubu}} testler kullanılır."),
            make_cloze("Başarılı bir tedavinin kanıtı, serolojik titrede en az {{c1::4 kat (2 dilüsyon)::miktar}} düşüş sağlanmasıdır."),
            make_cloze("VDRL titresinin 1:64'ten {{c1::1:16::yeni titre}}'ya inmesi, 4 katlık bir düşüşü (2 dilüsyon) ifade eder."),
            make_chain("Başarılı Tedavi Takibi Süreci", [
                "Tedavi öncesi bazal VDRL/RPR titresinin ölçülmesi (örn. 1:32)",
                "Uygun penisilin tedavisinin verilmesi",
                "6-12. aylarda kontrol VDRL bakılması",
                "Titrenin 4 kat düşmesi (örn. 1:8)",
                "Tedavinin başarılı olduğunun teyit edilmesi"
            ]),
            make_quiz(
                "Sifiliz tedavisi gören bir hastanın başlangıç VDRL titresi 1:128 bulunmuştur. Başarılı bir tedavi yanıtı sayılması için kontrol titresi en fazla kaç olmalıdır?",
                [
                    "1:64",
                    "1:32",
                    "1:16",
                    "1:256"
                ],
                1,
                "En az 4 katlık (2 dilüsyonluk) bir düşüş gereklidir. 1:128 -> 1:64 (1. dilüsyon/2 kat) -> 1:32 (2. dilüsyon/4 kat). Yani titre en fazla 1:32 olmalıdır."
            )
        ]
    )
    slides.append(slide_92)

    # Slide 93
    narrative_93 = """Sifiliz tedavisinde (özellikle ilk penisilin iğnesinden sonra) görülebilen meşhur ve akut bir komplikasyon **Jarisch-Herxheimer reaksiyonu**'dur. Bu, bir penisilin alerjisi DEĞİLDİR; tamamen farklı bir mekanizmaya dayanır.
*   **Mekanizma:** Penisilin enjeksiyonundan hemen sonra (genellikle ilk 24 saat içinde), kanda bulunan milyonlarca *T. pallidum* spiroketinin birden parçalanmasıyla (lizis) kana masif miktarda bakteri endotoksin benzeri ürünleri ve lipoproteini saçılır.
*   **Klinik:** Akut ateş, titreme, kas ağrıları, taşikardi ve mevcut şankr/döküntü lezyonlarında geçici alevlenme görülür.
> Bu reaksiyon ilacın işe yaradığını ve bakterileri yoğun bir şekilde öldürdüğünü gösterir. Kendini sınırlar, 12-24 saatte genellikle spontan geçer. Tedaviyi kesmeyi gerektirmez; semptomatik olarak (NSAİİ vb.) yönetilir.
"""
    slide_93 = make_slide(
        title="Jarisch-Herxheimer Reaksiyonu",
        narrative=narrative_93,
        elements=[
            make_cloze("Jarisch-Herxheimer reaksiyonu, penisilin tedavisi sonrası spiroketlerin hızla {{c1::parçalanması (lizisi)::mekanizma}} sonucu ortaya çıkar."),
            make_cloze("Kana karışan bakteriyel ürünler hastalarda akut {{c1::ateş::semptom}}, titreme ve kas ağrılarına yol açar."),
            make_cloze("Bu reaksiyon bir penisilin {{c1::alerjisi::yanlış bilinen durum}} DEĞİLDİR ve tedaviyi sonlandırmayı gerektirmez."),
            make_recall("Jarisch-Herxheimer reaksiyonu genellikle penisilin uygulamasından sonraki ne kadar sürede başlar?", "Genellikle ilk 24 saat içinde (çoğu zaman birkaç saatte) başlar."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Jarisch-Herxheimer reaksiyonu.",
                "Jarisch-Herxheimer reaksiyonu görülen hastada derhal penisilin tedavisi kesilmeli ve alternatif antibiyotiğe geçilmelidir.",
                "Bu reaksiyon tedavinin kesilmesini gerektirmez; bir alerji değildir, ilacın bakterileri yoğun şekilde yok ettiğinin göstergesidir ve semptomatik olarak destekleyici tedavi ile (ateş düşürücüler vs.) yönetilir.",
                [
                    "İlk doz penisilinden sonra akut ateş, titreme ve üşüme ile kendini gösterir.",
                    "Masif spiroket lizisine bağlı olarak enflamatuar sitokin deşarjı mekanizmasıyla oluşur.",
                    "Sıklıkla 12-24 saat içinde kendiliğinden geriler."
                ]
            )
        ]
    )
    slides.append(slide_93)

    # Slide 94
    narrative_94 = """Sifilizin farklı evreleri, hastalığı bulaştırma potansiyeli açısından büyük zıtlıklar taşır. Bulaştırıcılık (infektivite), lezyonlardaki spiroket yoğunluğuyla doğrudan ilişkilidir.
*   **Primer ve Sekonder Evre:** Bakteri yükünün en fazla olduğu dönemlerdir. Şankr (primer) ve özellikle condylomata lata (sekonder) lezyonlarından sızan eksüda, milyonlarca hareketli spiroket barındırır. Bu dönemlerde **bulaştırıcılık en yüksektir.**
*   **Geç Latent ve Tersiyer Evre:** Yıllar geçtikçe spiroket sayısı çok azalır. Gomlar veya nörosifiliz doku hasarına yol açsa da, bu lezyonların içinde canlı bakteri bulmak çok zordur. Bu nedenle geç evre sifiliz **cinsel yolla bulaştırıcı DEĞİLDİR.** (Not: Anneden fetüse bulaş her evrede risk taşır).
> Sifilizde "Lezyon ne kadar erken, bulaştırıcılık o kadar yüksek; hastalık ne kadar eski, hasar büyük ama bulaştırıcılık düşük" kuralı geçerlidir.
"""
    slide_94 = make_slide(
        title="Sifiliz Evrelerinin Bulaştırıcılık Özeti",
        narrative=narrative_94,
        elements=[
            make_cloze("Sifilizde spiroket yükünün ve dolayısıyla cinsel yolla {{c1::bulaştırıcılığın::risk}} en yüksek olduğu evreler primer ve sekonder evrelerdir."),
            make_cloze("Sekonder sifiliz lezyonlarından olan {{c1::condylomata lata::lezyon}}, spiroket açısından son derece zengindir ve çok bulaştırıcıdır."),
            make_cloze("Yıllar sonra ortaya çıkan tersiyer (gommatöz) evrede cinsel yolla bulaştırıcılık pratikte {{c1::yoktur (sıfırdır)::derece}}."),
            make_table("Evrelere Göre Bulaştırıcılık Kıyaslaması",
                ["Evre", "Bakteri Yükü (Lezyonda)", "Cinsel Yolla Bulaştırıcılık"],
                [
                    ["Primer (Şankr)", "Çok Yüksek", "Çok Yüksek"],
                    ["Sekonder", "En Yüksek", "En Yüksek"],
                    ["Tersiyer (Geç Dönem)", "Çok Düşük / Yok", "Bulaştırıcı Değil"]
                ]
            ),
            make_quiz(
                "Aşağıdaki sifiliz evrelerinin hangisinde bulunan lezyonlardan hastalığın cinsel yolla bulaşma ihtimali pratik olarak yoktur?",
                [
                    "Primer evre",
                    "Sekonder evre",
                    "Erken latent evre",
                    "Tersiyer evre"
                ],
                3,
                "Tersiyer evre (geç dönem), aşırı duyarlılık ve enflamatuar yanıtın ön planda olduğu, spiroket miktarının (dolayısıyla bulaştırıcılığın) sıfıra yakın olduğu dönemdir."
            )
        ]
    )
    slides.append(slide_94)

    # Slide 95
    narrative_95 = """**Çıkmış Sınav Sorusu Analizi 1:** Geçmiş yıllarda TUS/DUS sınavlarında primer sifilizin temel kliniği sıkça sorgulanmıştır. Soru kalıbı genellikle cinsel temas öyküsü olan bir hastada genital bölgede yeni fark edilen bir ülser şeklindedir.
*   **Vurgulanan Anahtar Kelimeler:** "Ağrısız", "temiz tabanlı", "sert kenarlı", "tek ülser". Ek olarak "ağrısız, lastik kıvamında lenfadenopati".
*   **Çeldiriciler:** Ağrılı ve pürülan ülserler Chancroid (Hemophilus ducreyi) veya Herpes Simplex işaretidir. Ağrısız ülser her zaman ilk planda Sifiliz şankrını düşündürmelidir.
> Sınavlarda genellikle bu ağrısız şankrın kendiliğinden iyileştiği ve hastanın bunu önemsemediği senaryosu çizilerek, enfeksiyonun sessizce sekonder evreye ilerlediği mesajı verilir.
"""
    slide_95 = make_slide(
        title="Çıkmış Sınav Sorusu Analizi 1: Primer Şankr",
        narrative=narrative_95,
        elements=[
            make_cloze("Sınav senaryolarında primer sifilizi işaret eden en önemli klinik bulgu, genital bölgedeki {{c1::ağrısız::semptom}} ülserdir (şankr)."),
            make_cloze("Şankr ülserinin kenarları genellikle endüredir ({{c1::serttir::kıvam}}) ve tabanı temizdir."),
            make_cloze("Eşlik eden inguinal lenfadenopati de tıpkı ülser gibi {{c1::ağrısız::bulgu}} ve lastik kıvamındadır."),
            make_recall("Genital bölgesinde ağrılı, pürülan (irinli) ve yumuşak tabanlı bir ülseri olan hastada ön planda sifiliz şankrı düşünülür mü?", "Düşünülmez. Bu bulgular Chancroid (Yumuşak şankr - H. ducreyi) veya Herpes için tipiktir, sifiliz şankrı ağrısız ve serttir."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Primer şankr klinği.",
                "Primer sifiliz lezyonu olan şankr, tedavi edilmezse kalıcı, derin skarlar bırakarak hayat boyu hastada kalır.",
                "Şankr, hastalar tedavi almasa dahi 3-6 hafta içinde genellikle KENDİLİĞİNDEN VE İZSİZ şekilde iyileşir. Bu durum hastanın yanıltıcı bir şekilde tamamen iyileştiğini düşünmesine sebep olur.",
                [
                    "Cinsel temas bölgesinde (çoğunlukla genitalya) tekil, sert kenarlı bir ülser olarak başlar.",
                    "Ülser dokunmakla ağrı yaratmaz.",
                    "Bölgesel (inguinal) lenf nodları büyüyebilir ancak onlar da ağrısızdır."
                ]
            )
        ]
    )
    slides.append(slide_95)

    # Slide 96
    narrative_96 = """**Çıkmış Sınav Sorusu Analizi 2:** Sekonder ve tersiyer sifilizin nörolojik bulguları arasındaki fark, klasik bir sınav tuzağıdır. İki evreyi birbirine karıştırmamak gerekir.
*   **Sekonder Sifiliz Bulguları:** Avuç içi-ayak tabanı makülopapüler döküntüleri, Condylomata lata (genital siğil benzeri ama yassı), alopesi (güve yeniği saç dökülmesi).
*   **Tersiyer Nörosifiliz Bulgusu (Tabes Dorsalis):** Medulla spinalis'in arka kordonunun demiyelinizasyonudur. Semptomları: Duyu kaybı, ataksi (geniş tabanlı yürüyüş), Romberg pozitifliği, ağrıyı ve sıcaklığı hissetmeme, refleks kayıpları.
> Soru kökünde "Condylomata lata" veya "vücutta yaygın döküntü" varsa sekonder sifiliz; "Arka kordon tutulumu, ataksi, propriyosepsiyon kaybı (Tabes dorsalis)" diyorsa kesinlikle Tersiyer (Geç) Nörosifiliz soruluyordur.
"""
    slide_96 = make_slide(
        title="Çıkmış Sınav Sorusu Analizi 2: Sekonder vs Tersiyer Ayrımı",
        narrative=narrative_96,
        elements=[
            make_cloze("Avuç içi ve ayak tabanı döküntüleri, klasik olarak sifilizin {{c1::sekonder::evre}} evresinde görülür."),
            make_cloze("Medulla spinalis'in arka kordonunun harap olmasıyla karakterize nörosifiliz tablosuna {{c1::Tabes dorsalis::hastalık adı}} denir."),
            make_cloze("Tabes dorsalis gelişen bir hastada öncelikle {{c1::propriyosepsiyon::duyu}} (pozisyon/derin duyu) kaybı ve duyusal ataksi görülür."),
            make_table("Klinik Tabloya Göre Evre Eşleştirmesi",
                ["Klinik Bulgu", "İlişkili Olduğu Evre"],
                [
                    ["Güve yeniği tarzı saç dökülmesi", "Sekonder Sifiliz"],
                    ["Gom (Lastiksi Granülom)", "Tersiyer (Benign) Sifiliz"],
                    ["Tabes Dorsalis", "Tersiyer (Nöro) Sifiliz"],
                    ["Condylomata lata", "Sekonder Sifiliz"]
                ]
            ),
            make_quiz(
                "Denge kaybı, karanlıkta yürürken zorlanma (pozisyon duyusu kaybı) ve alt ekstremitelerde refleks azalması (Tabes Dorsalis bulguları) şikayetleriyle başvuran bir hasta, tedavi edilmemiş sifilizin hangi evresindedir?",
                [
                    "Primer Sifiliz",
                    "Sekonder Sifiliz",
                    "Erken Latent Sifiliz",
                    "Tersiyer Sifiliz"
                ],
                3,
                "Tabes dorsalis, medulla spinalisin arka kordonunu tutan, enfeksiyondan on yıllar sonra ortaya çıkabilen geç dönem (tersiyer) bir nörosifiliz formudur."
            )
        ]
    )
    slides.append(slide_96)

    # Slide 97
    narrative_97 = """**Tıp Fakültesi Sınav Spotları (Bölüm 1)**
Mikrobiyoloji ve İntaniye komitelerinde hayat kurtaracak kısa tekrar notları:
1.  **Spiroket Morfolojisi:** *T. pallidum* Gram boyası ile boyanamayacak kadar incedir. Karanlık alan mikroskobisi ile hareketli (tirbuşon gibi dönen) sarmal formlar olarak izlenir.
2.  **Argyll Robertson Pupili:** "Fahişe pupili" olarak da bilinir (Nörosifilizde). Göz ışığa reaksiyon vermez (küçülmez) ama yakına bakarken uyum (akomodasyon) yapar. Akılda tutma: "Accommodates but does not react".
3.  **Hutchinson Dişleri:** Konjenital sifilizin geç bulgularındandır. Üst kesici dişlerin fıçı gibi şekil alıp ortalarının çentikli olması durumudur (Hutchinson triadı'nın parçası).
"""
    slide_97 = make_slide(
        title="Tıp Fakültesi Sınav Spotları: Spiroket Morfolojisinden Argyll Robertson'a",
        narrative=narrative_97,
        elements=[
            make_cloze("*Treponema pallidum*'un morfolojisini canlı ve hareketli olarak görmek için {{c1::karanlık alan::mikroskop türü}} mikroskobisi kullanılır."),
            make_cloze("Işığa tepki vermeyen ancak akomodasyon yapan göz bebeğine {{c1::Argyll Robertson::pupil adı}} pupili denir ve genellikle nörosifilizde görülür."),
            make_cloze("Konjenital sifilizde görülen çentikli ve kama şekilli üst kesici dişlere {{c1::Hutchinson::özel isim}} dişleri adı verilir."),
            make_recall("Karanlık alan mikroskobisinde Treponema pallidum'un karakteristik hareketi nasıldır?", "Kendi ekseni etrafında dönen (tirbuşon / burgu) ve ileri-geri hareket eden spiroket formundadır."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Klasik Sifiliz spotları.",
                "Treponema pallidum, laboratuvarda kanlı agar besiyerine ekilerek 24 saat içinde kolayca üretilir ve kolonileri tanımlanır.",
                "T. pallidum in vitro (hücresiz suni besiyerlerinde) ÜRETİLEMEZ. Tanı için seroloji veya karanlık alan mikroskobisi kullanılmalıdır.",
                [
                    "Argyll Robertson pupili nörosifiliz (özellikle Tabes Dorsalis) için spesifik bir bulgudur.",
                    "Konjenital sifilizde Hutchinson triadı (keratit, sağırlık, çentikli dişler) görülebilir.",
                    "Bakteri çok ince olduğu için standart Işık Mikroskobu (Gram boyası) ile görülemez."
                ]
            )
        ]
    )
    slides.append(slide_97)

    # Slide 98
    narrative_98 = """**Tıp Fakültesi Sınav Spotları (Bölüm 2)**
Seroloji ve Tedavi özet spotları:
1.  **VDRL/RPR (Non-Treponemal):** Tarama testidir. Tedaviyle düşer (takipte kullanılır). Biyolojik yalancı pozitiflik sıktır (Otoimmün hastalıklar, SLE, gebelik).
2.  **TPHA/FTA-ABS (Treponemal):** Doğrulama testidir. Tedaviyle DÜŞMEZ (ömür boyu pozitif).
3.  **Erken Dönem Tedavi (Primer/Sekonder):** Benzatin Penisilin G 2.4 MU, Tek doz IM.
4.  **Geç Dönem Tedavi (Geç Latent/Tersiyer):** Benzatin Penisilin G, 3 hafta (haftada 1) IM.
5.  **Nörosifiliz Tedavisi:** Kristalize Penisilin G, 10-14 gün IV (Hastanede yatış).
"""
    slide_98 = make_slide(
        title="Tıp Fakültesi Sınav Spotları: Seroloji ve Tedavi Kıyaslaması",
        narrative=narrative_98,
        elements=[
            make_cloze("Otoimmün hastalıklarda (örneğin SLE'de) sıkça biyolojik yalancı pozitiflik veren sifiliz tarama testi {{c1::VDRL (veya RPR)::test adı}}'dir."),
            make_cloze("Treponemal testler, hasta kür sağlasa bile {{c1::ömür boyu::süre}} pozitif kalmaya devam eder."),
            make_cloze("Nörosifilizde ilacın KBB'yi geçmesi için mutlaka {{c1::kristalize::penisilin formu}} penisilin intravenöz yolla uygulanır."),
            make_chain("Sınavlar İçin Altın Test Eşleşmeleri", [
                "Tarama ve titre (takip) -> VDRL",
                "Doğrulama ve ömür boyu iz -> TPHA",
                "En erken pozitifleşen test -> FTA-ABS"
            ]),
            make_quiz(
                "Kendisine SLE (Sistemik Lupus Eritematozus) teşhisi konmuş bir kadının rutin taramasında VDRL pozitif bulunuyor. Sifiliz olmadığını doğrulamak için hangi test istenmelidir?",
                [
                    "RPR",
                    "Karanlık alan mikroskobisi",
                    "TPHA (veya FTA-ABS)",
                    "BOS analizi"
                ],
                2,
                "SLE gibi otoimmün hastalıklarda VDRL biyolojik yalancı pozitif sonuç verebilir. Gerçek sifilizi dışlamak için spesifik treponemal doğrulama testi (TPHA/FTA-ABS) yapılmalıdır (ki hastada negatif çıkması beklenir)."
            )
        ]
    )
    slides.append(slide_98)

    # Slide 99
    narrative_99 = """Sifilizin klinik evreleri ve seyri, tedavi edilmediği takdirde on yıllara yayılan kronik bir süreçtir. Tüm klinik bilgiyi tek bir çerçevede konsolide etmek büyük resmi görmenizi sağlar.
*   **Primer:** Temastan 2-3 hafta sonra ağrısız şankr, bölgesel LAP, lokalize enfeksiyon. Kendi kendine geçer.
*   **Sekonder:** Şankrdan haftalar/aylar sonra. Bakteriyemi evresi. Yaygın döküntüler, condylomata lata, sistemik lenfadenopati. Kendi kendine geçer.
*   **Latent:** Klinik bulgu sıfır. Sadece seroloji pozitif (Erken <1 yıl, Geç >1 yıl).
*   **Tersiyer:** Yıllar sonra. Yıkıcı faz. Gomlar, Aort anevrizması, Nörosifiliz (Tabes dorsalis, genel parezi).
> Doğal seyirde, sifiliz alan hastaların yaklaşık 1/3'ü, yıllar süren sessiz latent evrenin ardından ölümcül tersiyer komplikasyonlar geliştirir.
"""
    slide_99 = make_slide(
        title="Sifilizin Klinik Aşamalarının Karşılaştırmalı Büyük Tablosu",
        narrative=narrative_99,
        elements=[
            make_cloze("Tüm klinik bulguların tamamen kaybolduğu, hastanın sadece kan testleriyle pozitif olduğu sessiz evreye {{c1::latent::evre adı}} sifiliz denir."),
            make_cloze("Kan dolaşımı yoluyla bakterilerin tüm vücuda yayıldığı, yaygın döküntülerin görüldüğü sistemik evre {{c1::sekonder::evre adı}} sifilizdir."),
            make_cloze("Kardiyovasküler tutulum (aortit) ve gom oluşumu hastalığın {{c1::tersiyer::evre adı}} fazında ortaya çıkar."),
            make_table("Klinik Evrelerin Büyük Konsolidasyonu",
                ["Evre", "Temel Özellik", "Kritik Semptomlar"],
                [
                    ["Primer", "Lokal İnvazyon", "Ağrısız Şankr, Ağrısız İnguinal LAP"],
                    ["Sekonder", "Sistemik Bakteriyemi", "Avuç içi/Taban Döküntüsü, Condylomata lata"],
                    ["Latent", "Asemptomatik Taşıyıcılık", "Semptom YOK, Sadece pozitif seroloji"],
                    ["Tersiyer", "Geç Yıkıcı Komplikasyonlar", "Gomlar, Aort Anevrizması, Tabes Dorsalis"]
                ]
            ),
            make_recall("Hangi sifiliz evreleri kendiliğinden (tedavi olmaksızın) iyileşip yerini sessiz döneme bırakabilir?", "Primer ve Sekonder evre bulguları zamanla kendiliğinden geriler ve hasta latent evreye girer.")
        ]
    )
    slides.append(slide_99)

    # Slide 100
    narrative_100 = """[TEKRAR SAYFASI - CHECKPOINT 10]
Deste 50'nin sonuna ulaştınız. Bu deste boyunca "Büyük Taklitçi" Treponema pallidum'un tüm gizemlerini çözdük:
1.  **Bakteriyoloji:** İnce sarmal yapısı, karanlık alan mikroskobisi ile tanınması.
2.  **Klinik Seyir:** Primerin ağrısız şankrı, Sekonderin yaygın döküntüleri, Tersiyerin yıkıcı gom ve nörolojik komplikasyonları. Konjenital geçişin kalıcı hasarları.
3.  **Seroloji:** Tarama (VDRL, düşer) ile doğrulama (TPHA, ömür boyu kalır) arasındaki kritik ayrım.
4.  **Tedavi:** Penisiline olan kusursuz duyarlılık. Erken evrede tek doz Benzatin Penisilin; geç evrede 3 haftalık program; Nörosifilizde IV Kristalize Penisilin.
> Artık Sifiliz konusunda klinik, laboratuvar ve tedavi aşamalarının tamamına hakimsiniz. Tebrikler!
"""
    slide_100 = make_slide(
        title="[TEKRAR SAYFASI - CHECKPOINT 10] Deste 50 Büyük Final Tekrarı ve Konsolidasyon",
        narrative=narrative_100,
        elements=[
            make_cloze("Sifilizin etkeni olan spiroket {{c1::Treponema pallidum::bakteri tam adı}}'dur."),
            make_cloze("Primer sifilizin ağrısız sert ülseri {{c1::şankr::lezyon}}, sekonder sifilizin bulaştırıcı yassı lezyonu {{c2::condylomata lata::lezyon}} olarak adlandırılır."),
            make_cloze("Tedavi sonrası başarı takibi spesifik olmayan {{c1::VDRL (veya RPR)::test}} testindeki titre düşüşüne bakılarak yapılır."),
            make_cloze("Penisilin tedavisi sonrası spiroketlerin parçalanmasına bağlı gelişen akut ateşe {{c1::Jarisch-Herxheimer::reaksiyon adı}} reaksiyonu denir."),
            make_quiz(
                "Sifiliz hakkında öğrenilen tüm genel kurallar düşünüldüğünde, aşağıdakilerden hangisi her zaman KESİN ve DOĞRU bir kuraldır?",
                [
                    "Treponemal testler tedavi başarısını takip etmek için düzenli olarak istenmelidir.",
                    "Şankr lezyonu çok ağrılı olduğu için hastayı hemen doktora gitmeye zorlar.",
                    "Sifiliz tedavisinde Treponema pallidum penisiline karşı bilinen hiçbir direnç mekanizması geliştirmemiştir.",
                    "Tersiyer sifiliz evresindeki hastalar, primer evredeki hastalardan daha fazla bulaştırıcıdır."
                ],
                2,
                "T. pallidum'un penisiline direnci sıfırdır, bu nedenle penisilin hala altın standarttır. Diğer tüm şıklar sifilizin temel kurallarına (ağrısızlık, test takibi ve bulaştırıcılık evreleri) terstir."
            )
        ]
    )
    slides.append(slide_100)

    return slides
