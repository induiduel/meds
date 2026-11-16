# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-18-s31",
        "title": "Çiçek Hastalığı (Variola): Tarihin En Yıkıcı Enfeksiyonu",
        "content": "Çiçek hastalığı (Variola virüsü), insanlık tarihinde savaşlardan ve tüm diğer felaketlerden daha fazla can almıştır (Sınav Spotu):\n\n- **Klinik Tablo ve Ölüm Oranı:**\n  - Yüksek ateş, sırt ağrısı ve tüm vücutta derin, iz bırakan püstüllerle seyreder.\n  - Hastaların **%30'unu öldürür**, hayatta kalanların çoğunda derin yüz nedbeleri (pockmarks) ve kornea tutulumuna bağlı kalıcı körlük bırakır.\n- **Demografik Yıkım:**\n  - Yalnızca 18. yüzyıl Avrupa'sında yılda yaklaşık 400.000 kişinin ölümüne yol açmıştır.\n  - Amerika kıtasına Avrupalıların taşımasıyla yerli Amerikan (Kızılderili) nüfusunun %90'a yakını çiçek salgınlarıyla yok olmuştur.\n- **Kalıcı Bağışıklık:** Çiçek geçiren bir kişinin hayatı boyunca bir daha çiçek hastalığına yakalanmadığı antik çağlardan beri biliniyordu; bu gözlem aşılamanın temelini oluşturmuştur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Çiçek Hastalığının Mortalitesi vs Kalıcı Bağışıklık",
                "Yüksek Mortalite ve Sakatlık",
                "Olguların %30'u hayatını kaybeder; yaşayanlarda derin yüz çukurları ve kalıcı körlük kalır.",
                "Ömür Boyu Kalıcı Bağışıklık",
                "Hastalığı atlatan birey hayatı boyunca bu virüse karşı tam bağışık hale gelir."
            ),
            make_quiz(
                "Tarihte insanlığın üçte birini öldüren, hayatta kalanlarda derin yüz çukurları ve körlük bırakan ancak geçirenlerde ömür boyu kalıcı bağışıklık oluşturan viral hastalık hangisidir?",
                [
                    {"key": "A", "text": "Çiçek hastalığı (Variola)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Çiçek hastalığı yüksek öldürücülüğüne karşın geçirenlerde kalıcı bağışıklık bırakan ve aşılamanın temelini atan hastalıktır."},
                    {"key": "B", "text": "Veba", "isCorrect": False, "explanation": "Bakteriyel bir pandemidir."},
                    {"key": "C", "text": "Kuduz", "isCorrect": False, "explanation": "Tedavisiz mortalitesi %100'dür, sağ kalan olmaz."},
                    {"key": "D", "text": "Kolera", "isCorrect": False, "explanation": "Bakteriyel ishal salgınıdır."}
                ]
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-18-s32",
        "title": "Osmanlı'da Çiçek Aşılama Geleneği: Variolasyon Yöntemi",
        "content": "Modern aşılama Edward Jenner ile popülerleşmeden çok önce, Osmanlı İmparatorluğu'nda halk arasında güvenle uygulanan bir çiçek aşılama geleneği vardı (Sınav Spotu):\n\n- **Variolasyon (Çiçekleme) Yöntemi:**\n  - Hafif seyirli çiçek hastalarının olgunlaşmış püstüllerinden ceviz kabuğu içinde cerahat toplanırdı.\n  - Bu canlı virüs sıvısı, sağlıklı çocukların kol derisine çizik atılarak veya iğne batırılarak aşılanırdı.\n  - Çocuklar hafif bir çiçek geçirir ve ömür boyu ölümcül çiçekten korunmuş olurlardı.\n- **Aşıcı Kadınlar Geleneği:**\n  - İstanbul'da ve Anadolu köylerinde bu işlemi yaşlı kadınlar ('aşıcı kadınlar') her yıl sonbaharda düzenli olarak yapardı.\n  - Bu uygulama, organize halk sağlığı bağışıklamasının tarihteki en eski halk tipi örneklerinden biridir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Osmanlı Variolasyon (Çiçekleme) Basamakları",
                [
                    "1. Uygun Donör Tespiti: Hafif seyreden çiçek hastası bir çocuğun püstülü seçilir.",
                    "2. Cerahatin Saklanması: Taze püstül sıvısı ceviz kabuğunda sterilize edilerek saklanır.",
                    "3. Deri Çiziği: Sağlıklı çocuğun kol derisine hafif bir çizik atılır.",
                    "4. İnokülasyon ve Bağışıklık: Sıvı çizikten sürülür; çocuk hafif bir döküntüyle tam bağışıklık kazanır."
                ]
            ),
            make_cloze(
                "Osmanlı İmparatorluğu'nda hafif çiçek hastalarının cerahatinin sağlıklı bireylerin derisine çizik atılarak aşılanması yöntemine variolasyon adı verilir.",
                "variolasyon",
                "İnsan çiçek virüsü ile yapılan geleneksel aşılama terimi"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-18-s33",
        "title": "Lady Mary Wortley Montagu ve Çiçek Aşısının Avrupa'ya Aktarımı (1721)",
        "content": "Osmanlı'nın çiçek aşılama uygulamasının Avrupa tıbbına ve dünyaya kazandırılmasında İngiliz elçisinin eşi Lady Montagu tarihi bir rol oynamıştır (Sınav Spotu):\n\n- **Lady Montagu'nun Tanıklığı (1717-1718):**\n  - Kendisi de İngiltere'de çiçek hastalığı geçirip güzelliğini ve yüz pürüzsüzlüğünü kaybeden, kardeşini çiçekten yitiren Lady Montagu, İstanbul'a geldiğinde Türklerin çiçek hastalığını bir şölen havasında aşılayarak önlediğini gördü.\n- **Kendi Çocuğunu Aşılatması:**\n  - 1718'de İstanbul'da elçilik hekimi Dr. Maitland ve bir Türk aşıcı kadına 5 yaşındaki oğlunu aşılatmış; çocuk hastalığı hafifçe atlatmıştır.\n- **İngiltere'ye Mektuplar ve Yayılım (1721):**\n  - Londra'ya yazdığı mektuplarla yöntemi anlattı; İngiltere'ye döndüğünde kızını da aşılatarak saray hekimlerini ikna etti.\n  - Mahkumlarda ve yetimlerde yapılan başarılı denemelerden sonra İngiliz Kraliyet ailesi çocukları aşılandı ve variolasyon tüm Avrupa'ya yayıldı.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Avrupa'da Çiçek Dehşeti vs Osmanlı'da Variolasyon",
                "Avrupa'da Çiçek Çaresizliği",
                "Her yıl yüz binlerce insan ölürken saraylar ve hekimler hiçbir koruyucu önlem bilmiyordu.",
                "Lady Montagu'nun Aktarımı",
                "İstanbul'daki halk tipi çiçek aşılama geleneğini 1721'de Londra'ya taşıyarak Avrupa tıbbına tanıttı."
            ),
            make_cloze(
                "Osmanlı İmparatorluğu'ndaki çiçek aşılama uygulamasını 1721 yılında İngiltere'ye ve Avrupa tıbbına tanıtan İngiliz elçisinin eşi Lady Montagu'dur.",
                "Lady Montagu",
                "Osmanlı variolasyonunu mektuplarıyla Batı'ya aktaran tarihi yazar"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-18-s34",
        "title": "Edward Jenner (1796): Sığır Çiçeği (Cowpox) İle Güvenli Aşılama",
        "content": "Variolasyon başarılı olsa da, gerçek insan çiçek virüsü kullanıldığı için %1-2 oranında ölüm veya ağır hastalık riski taşıyordu; bu riski sıfırlayan hekim Edward Jenner olmuştur (Sınav Spotu):\n\n- **Kırsal Gözlem:**\n  - İngiliz kır hekimi Edward Jenner, inek sağan sütçü kızların ellerinde inek memelerinden bulaşan sığır çiçeği (**cowpox - Variola vaccina**) lezyonları çıktığını, ancak bu kızların ölümcül insan çiçeğine (smallpox) **asla yakalanmadığını** fark etti.\n- **Tarihi Deney (14 Mayıs 1796):**\n  - Sütçü kız Sarah Nelmes'in elindeki sığır çiçeği kabarcığından aldığı cerahati 8 yaşındaki James Phipps'in koluna aşıladı.\n  - Çocuk hafif bir kırıklık geçirdi.\n  - Birkaç ay sonra Jenner çocuğa **gerçek ölümcül insan çiçeği (variola) inoküle etti; çocuk hastalanmadı**!\n- **Vaccine Teriminin Doğuşu:** İnek anlamına gelen Latince **'vacca'** kelimesinden türetilerek bu yönteme **'vaccination' (aşılama)** adı verildi.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Jenner'ın Bilimsel Aşı Keşif Adımları",
                [
                    "1. Saha Gözlemi: Süt sağan kadınların çiçek salgınlarından hiç etkilenmediği fark edilir.",
                    "2. Çapraz Bağışıklık Hipotezi: Sığır çiçeğinin insanı insan çiçeğinden koruduğu varsayılır.",
                    "3. Güvenli Aşılama: James Phipps'in koluna sığır çiçeği (cowpox) sıvısı aşılanır.",
                    "4. Çiçekle Karşılaştırma Testi: Çocuğa ölümcül virüs verildiğinde tam korunduğu ispatlanır.",
                    "5. Tıbbi Bildirim: 1798'de yöntem yayınlanır ve tıp literatürüne 'vaccine' terimi girer."
                ]
            ),
            make_quiz(
                "Edward Jenner'ın 1796 yılında insan çiçeğine karşı geliştirdiği ilk güvenli aşıda kullandığı ve yönteme 'vaccination' adının verilmesini sağlayan kaynak virüs hangisidir?",
                [
                    {"key": "A", "text": "Sığır çiçeği virüsü (Cowpox - Variola vaccina)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Jenner sığır çiçeği (cowpox) kullanarak insanı ölümcül çiçekten korumuş, 'vacca' (inek) kelimesinden vaccine terimi doğmuştur."},
                    {"key": "B", "text": "Kuduz virüsü", "isCorrect": False, "explanation": "Pasteur 1885'te kuduz aşısını yapmıştır."},
                    {"key": "C", "text": "Çocuk felci virüsü", "isCorrect": False, "explanation": "Salk ve Sabin 20. yüzyılda bulmuştur."},
                    {"key": "D", "text": "Boğmaca bakterisi", "isCorrect": False, "explanation": "Bordetella pertussis aşısıdır."}
                ]
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-18-s35",
        "title": "Louis Pasteur'ün Aşı Çalışmaları: Tavuk Kolerası, Şarbon ve Kuduz (1885)",
        "content": "Pasteur, Jenner'ın tesadüfi sığır çiçeği modelini laboratuvarda bilinçli ve sistematik bir 'virülans zayıflatma (atenüasyon)' ilkesine dönüştürmüştür (Sınav Spotu):\n\n- **Atenüasyon İlkesinin Keşfi (Tavuk Kolerası):**\n  - Yaz tatilinde masada unutulup bayatlayan tavuk kolerası kültürünün tavukları öldürmediğini, aksine onları taze ölümcül kültüre karşı koruduğunu tesadüfen keşfetmiştir.\n- **Şarbon Aşısı (Pouilly-le-Fort Deneyi - 1881):**\n  - 25 koyunu aşılayıp 25 koyunu aşısız bıraktı; tümüne ölümcül şarbon basili verdiğinde aşılı 25 koyunun tümü yaşarken, aşısız 25 koyunun tümü ölmüştür.\n- **Kuduz Aşısı (1885):**\n  - Kuduz virüsünü tavşan omuriliğinde pasajlayarak kurutma yöntemiyle zayıflattı.\n  - Kuduz bir köpek tarafından 14 yerinden ısırılan 9 yaşındaki **Joseph Meister'a** aşıyı uygulayarak çocuğu kesin bir ölümden kurtarmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Pasteur'ün Geliştirdiği Aşı", "Yıl", "Atenüasyon Yöntemi ve Sonuç"],
                [
                    ["Tavuk Kolerası", "1879", "Kültürün havada eskitilmesiyle virülansın zayıflatılması (ilk atenüe aşı)"],
                    ["Şarbon Aşısı", "1881", "Bakterinin 42-43°C'de ısıtılarak spor yapma yeteneğinin kırılması"],
                    ["Kuduz Aşısı", "1885", "Tavşan omuriliğinde virüsün kurutularak zayıflatılması (Joseph Meister olgusu)"]
                ]
            ),
            make_cloze(
                "Louis Pasteur 1885 yılında kuduz bir köpek tarafından ısırılan dokuz yaşındaki Joseph Meister isimli çocuğa ilk insan kuduz aşısını uygulayarak hayatını kurtarmıştır.",
                "Joseph Meister",
                "Tarihte ilk kuduz aşısı uygulanan ve kurtarılan çocuğun adı"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-18-s36",
        "title": "Emil von Behring ve Kitasato: Difteri ve Tetanos Antitoksini (1890)",
        "content": "19. yüzyılın sonlarında difteri, 'boğan melek' adıyla her kış binlerce çocuğu nefessiz bırakarak öldüren korkunç bir kabustu (Sınav Spotu):\n\n- **Toksin ve Antitoksin Keşfi:**\n  - Emil von Behring ve Japon araştırmacı Shibasaburo Kitasato, difteri ve tetanos bakterilerinin hastalık yapıcı zehirlerini (**ekzotoksin**) keşfettiler.\n- **Serum Terapisi (Pasif Bağışıklık - 1890):**\n  - Kademeli olarak artan dozlarda difteri toksini verilen atların kanında bu toksini nötralize eden koruyucu maddelerin (**antitoksin / antikor**) oluştuğunu gördüler.\n  - Bu atların kan serumunu (difteri serumu) ölüm döşeğindeki difterili çocuklara enjekte ettiklerinde sahte zarlar (psödomembran) eridi ve çocuklar hızla iyileşti.\n- **İlk Nobel Tıp Ödülü (1901):** Serum terapisi ile difteriyi yenen Emil von Behring, **tarihin ilk Nobel Fizyoloji ve Tıp Ödülü'ne** layık görülmüştür.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Aktif Bağışıklama (Aşı) vs Pasif Bağışıklama (Serum / Antitoksin)",
                "Aktif Bağışıklama (Jenner / Pasteur)",
                "Antijen verilerek vücudun kendi antikorunu üretmesi sağlanır; etki geç başlar ama kalıcı hafıza bırakır.",
                "Pasif Bağışıklama (Behring Antitoksini)",
                "Hazır antikor (serum) doğrudan verilir; etki anında başlar, akut hayat kurtarır ancak kalıcı hafıza bırakmaz."
            ),
            make_quiz(
                "1890 yılında difteri ve tetanosa karşı at kanından serum üreterek pasif bağışıklamayı başlatan ve 1901'de ilk Nobel Tıp Ödülü'nü alan bilim insanı kimdir?",
                [
                    {"key": "A", "text": "Emil von Behring", "isCorrect": True, "explanation": "Doğru cevap A'dır: Emil von Behring difteri antitoksini ile 1901 yılında ilk Nobel Tıp Ödülü'nü almıştır."},
                    {"key": "B", "text": "Paul Ehrlich", "isCorrect": False, "explanation": "Kemoterapinin kurucusudur."},
                    {"key": "C", "text": "Alexander Fleming", "isCorrect": False, "explanation": "Penisilini 1928'de bulmuştur."},
                    {"key": "D", "text": "Robert Koch", "isCorrect": False, "explanation": "1905'te tüberküloz araştırmalarıyla Nobel almıştır."}
                ]
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-18-s37",
        "title": "Calmette ve Guérin: BCG Aşısının Geliştirilmesi (1921)",
        "content": "Tüberküloz basili Koch tarafından 1882'de bulunmuş olsa da, etkin bir aşı geliştirmek 40 yıl süren olağanüstü bir sabır gerektirmiştir (Sınav Spotu):\n\n- **Albert Calmette ve Camille Guérin'in Çalışması:**\n  - Pasteur Enstitüsü'nde çalışan iki Fransız araştırmacı, sığır tüberkülozu basili olan **Mycobacterium bovis** suşunu aldılar.\n  - Bu basili gliserin, patates ve sığır safrası içeren özel bir besiyerinde tam **13 yıl boyunca (1908-1921) kesintisiz 230 kez pasajladılar (alt kültür yaptılar)**.\n- **BCG Aşısının Doğuşu (1921):**\n  - 230 pasaj sonunda basil hastalık yapma yeteneğini (virülansını) tamamen kaybetti ancak güçlü bir bağışıklık uyarma yeteneğini korudu.\n  - Bu canlı atenüe aşıya **Bacille Calmette-Guérin (BCG)** adı verildi.\n  - 1921 yılından itibaren insanlarda uygulanmaya başlanmış, çocukları tüberküloz menenjiti ve miliyer tüberkülozdan koruyan temel küresel aşı haline gelmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "BCG Aşısının Geliştirilme Süreci",
                [
                    "1. Suş Seçimi: Mycobacterium bovis basili sığır lezyonundan izole edilir.",
                    "2. 230 Kez Pasaj: 13 yıl boyunca safralı besiyerinde her 3 haftada bir alt kültüre ekilir.",
                    "3. Atenüasyonun Kanıtı: Basilin artık kobay ve sığırlarda tüberküloz yapmadığı gösterilir.",
                    "4. İnsan Kullanımı: 1921'de Paris'te ilk yenidoğana ağızdan verilerek kitlesel tüberküloz aşısı başlatılır."
                ]
            ),
            make_cloze(
                "Mycobacterium bovis basilinin 230 kez pasajlanmasıyla 1921 yılında geliştirilen canlı atenüe tüberküloz aşısına BCG aşısı adı verilir.",
                "BCG aşısı",
                "Calmette ve Guérin'in adını taşıyan verem aşısı"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-18-s38",
        "title": "Çiçek Hastalığının Global Eradikasyonu (1980): Halk Sağlığının Zaferi",
        "content": "Halk sağlığı tarihinin en büyük, en kusursuz ve eşsiz küresel zaferi çiçek hastalığının yeryüzünden tamamen silinmesidir (Sınav Spotu):\n\n- **DSÖ Küresel Kampanyası (1967-1977):**\n  - Dünya Sağlık Örgütü 1967'de yoğunlaştırılmış çiçek eradikasyon programını başlattı.\n  - **Bifurcated (Çatallı) İğne:** Aşı maliyetini düşüren ve tek batırmayla binlerce insanı aşılayan pratik çatallı iğne teknolojisi kullanıldı.\n  - **Halka Aşılama (Ring Vaccination):** Vaka görülen yerin etrafındaki tüm temaslılar çember içine alınarak aşılandı ve virüsün yayılacak insan bulması engellendi.\n- **Son Doğal Vaka (1977 - Somali):** Ali Maow Maalin yeryüzündeki son doğal çiçek hastası oldu ve iyileşti.\n- **Resmi Eradikasyon İlanı (8 Mayıs 1980):** DSÖ, çiçek hastalığının dünya üzerinden **tamamen yok edildiğini (eradikasyon)** resmen ilan etti. İnsan eliyle kökü kazınan ilk ve tek insan bulaşıcı hastalığıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Aşama", "Tarih / Yer", "Halk Sağlığı Olayı"],
                [
                    ["Yoğun Eradikasyon Kararı", "1967 (DSÖ)", "Tüm dünyada eşgüdümlü sürveyans ve halka aşılama başlatıldı"],
                    ["Son Doğal Vaka", "1977 (Somali)", "Hastanede aşçı olan Ali Maow Maalin son doğal çiçek hastası olarak kayda geçti"],
                    ["Resmi Eradikasyon Tescili", "8 Mayıs 1980 (Cenevre)", "Dünya Sağlık Asamblesi çiçeğin yeryüzünden silindiğini ilan etti"]
                ]
            ),
            make_quiz(
                "Dünya Sağlık Örgütü (DSÖ) tarafından 1980 yılında yeryüzünden tamamen silindiği (eradikasyon) resmen ilan edilen ilk ve tek insan bulaşıcı hastalığı hangisidir?",
                [
                    {"key": "A", "text": "Çiçek hastalığı (Variola)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Çiçek hastalığı 1980 yılında global olarak eradike edilen ilk ve tek insan enfeksiyonudur."},
                    {"key": "B", "text": "Çocuk felci (Poliomyelit)", "isCorrect": False, "explanation": "Büyük oranda kontrol altına alınmışsa da bazı ülkelerde endemiktir."},
                    {"key": "C", "text": "Kızamık", "isCorrect": False, "explanation": "Hala salgınlar yapmaktadır."},
                    {"key": "D", "text": "Tüberküloz", "isCorrect": False, "explanation": "Milyonlarca insan hala enfektedir."}
                ]
            )
        ]
    })

    # Slide 39 - CHECKPOINT 4
    slides.append({
        "id": "k1-18-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Bağışıklama Tarihi ve Aşıların Zaferi",
        "content": "Bu checkpointte bağışıklamanın tarihsel evrimini ve büyük aşı zaferlerini özetliyoruz:\n\n- **Çiçek Hastalığı:** Yüzyıllarca nüfusun üçte birini öldüren en ölümcül virüstü.\n- **Osmanlı Variolasyonu:** Canlı püstül sıvısı çizik atılarak aşılanıyordu; Lady Montagu 1721'de bu yöntemi İngiltere'ye ve Avrupa'ya taşıdı.\n- **Edward Jenner (1796):** Sığır çiçeği (cowpox) ile James Phipps'i aşılayarak modern aşılamayı (vaccination) başlattı.\n- **Louis Pasteur:** Atenüasyon ilkesini kurdu; tavuk kolerası, şarbon ve 1885'te Joseph Meister'da kuduz aşısını başardı.\n- **Emil von Behring (1890):** At serumu ile difteri antitoksinini geliştirdi; 1901'de ilk Nobel Tıp Ödülü'nü aldı.\n- **Calmette ve Guérin (1921):** M. bovis'i 230 kez pasajlayarak BCG verem aşısını üretti.\n- **Global Eradikasyon (1980):** Çiçek hastalığı yeryüzünden tamamen silinen ilk hastalıktır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Aşı / Bağışıklama", "Geliştiren Kişi / Toplum", "Tarih", "Yöntem Özelliği"],
                [
                    ["Variolasyon", "Osmanlı Halkı / Lady Montagu", "1718-1721", "Canlı insan çiçeği püstülüyle hafif geçirtme"],
                    ["Çiçek Aşısı (Cowpox)", "Edward Jenner", "1796", "Sığır çiçeği ile çapraz koruma ('vaccine')"],
                    ["Kuduz Aşısı", "Louis Pasteur", "1885", "Kurutulmuş tavşan omuriliği atenüasyonu"],
                    ["Difteri Antitoksini", "Emil von Behring", "1890", "At serumuyla pasif bağışıklama (İlk Nobel)"],
                    ["BCG Verem Aşısı", "Calmette ve Guérin", "1921", "M. bovis'in 230 kez safralı besiyerinde pasajı"],
                    ["Çiçek Eradikasyonu", "DSÖ Küresel İşbirliği", "1980", "Yeryüzünden tamamen silinen ilk insan hastalığı"]
                ]
            ),
            make_chain(
                "Aşılamanın Tarihsel Dönüm Noktaları",
                [
                    "1. Variolasyon: Osmanlı'da canlı insan püstülüyle başlayan halk koruması.",
                    "2. Jenner Devrimi: Sığır çiçeğiyle güvenli aşılamanın keşfi.",
                    "3. Pasteur Atenüasyonu: Laboratuvarda mikropların zayıflatılma prensibi.",
                    "4. Behring Antitoksini: Serum tedavisiyle difteri ölümlerinin durdurulması.",
                    "5. Çiçek Eradikasyonu: 1980'de hastalığın yeryüzünden tamamen silinmesi."
                ]
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-18-s40",
        "title": "Bölüm Özeti: Aşılamadan Çevre Sağlığı ve Epidemiyolojiye Geçiş",
        "content": "Bölüm 4 boyunca bağışıklama tarihinin kilometre taşlarını ve çiçek hastalığının eradikasyonunu inceledik:\n\n- **Özet:** Aşılar bireysel bağışıklığın ötesinde toplumsal bağışıklık (sürü bağışıklığı) sağlayarak insanlığı kitlesel ölümlerden kurtarmıştır.\n- **Sonraki Bölüm (Bölüm 5):** Salgınların havadan değil sudan bulaştığını etken bulunmadan 30 yıl önce kanıtlayan **John Snow'u, 1854 Londra Broad Street kolera salgınını ve çevre sağlığı ile modern epidemiyolojinin doğuşunu** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "Edward Jenner'ın 1796 yılında sığır çiçeği cerahati ile ilk kez aşıladığı ve tarihe geçen sekiz yaşındaki çocuğun adı nedir?",
                "James Phipps",
                "Jenner'ın ilk çiçek aşısını uyguladığı çocuğun adı"
            ),
            make_quiz(
                "Albert Calmette ve Camille Guérin'in 13 yıl boyunca 230 kez pasajlayarak geliştirdikleri BCG aşısı hangi bakteriyel enfeksiyona karşı koruma sağlar?",
                [
                    {"key": "A", "text": "Tüberküloz (Verem)", "isCorrect": True, "explanation": "Doğru cevap A'dır: BCG (Bacille Calmette-Guérin) aşısı tüberküloz menenjiti ve miliyer tüberküloza karşı korur."},
                    {"key": "B", "text": "Tetanos", "isCorrect": False, "explanation": "Tetanos toksoid aşısıyla korunur."},
                    {"key": "C", "text": "Boğmaca", "isCorrect": False, "explanation": "Pertussis aşısıdır."},
                    {"key": "D", "text": "Kızamıkçık", "isCorrect": False, "explanation": "Viral rubella aşısıdır."}
                ]
            )
        ]
    })

    return slides
