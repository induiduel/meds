# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-17-s01",
        "title": "Cinsel Yolla Bulaşan Enfeksiyonlara Giriş: Tanım ve Küresel Yük",
        "content": "Cinsel yolla bulaşan enfeksiyonlar (CYBE / CYBH), temel olarak cinsel temasla kişiden kişiye aktarılan çok çeşitli patojenlerin yol açtığı enfeksiyonlar grubudur:\n\n- **Epidemiyolojik Ölçek:** Dünya Sağlık Örgütü (DSÖ) verilerine göre her gün dünya genelinde 1 milyondan fazla yeni tedavi edilebilir CYBE vakası edinilmektedir.\n- **Halk Sağlığı Etkisi:** Bu enfeksiyonlar yalnızca lokal genital rahatsızlık yaratmakla kalmaz; infertilite (kısırlık), dış gebelik, perinatal ölüm, konjenital malformasyonlar ve genital kanserlerin başlıca nedenidir.\n- **Tedavi Edilebilir vs Tedavi Edilemeyen:** Bakteriyel ve protozoal etkenler (klamidya, gonore, sifiliz, trikomoniyazis) uygun antimikrobiyallerle tamamen kür sağlanabilirken; viral etkenler (HIV, HSV, HPV, HBV) kronik kalıcı enfeksiyonlar oluşturur.\n- **Damgalanma ve Gizlilik:** Sosyal tabular ve yüksek asemptomatik oranlar nedeniyle hastalar sağlık kuruluşlarına geç başvurmakta ve bulaş zinciri sessizce sürmektedir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Tedavi Edilebilir Bakteriyel CYBE vs Kronik Viral CYBE",
                "Tedavi Edilebilir (Kür Sağlanan) CYBE",
                "Klamidya, gonore, sifiliz ve trikomoniyazis; uygun antibiyotik ve antiprotozoal rejimlerle tamamen eradike edilir.",
                "Kronik Kalıcı Viral CYBE",
                "HIV, HSV, HPV ve HBV; viral yük baskılanabilir ancak latent rezervuarlar nedeniyle tam mikrobiyolojik kür zordur."
            ),
            make_cloze(
                "Temel olarak cinsel temasla bulaşan ve infertilite ile dış gebeliğe yol açabilen hastalıklara cinsel yolla bulaşan enfeksiyonlar denir.",
                "cinsel yolla bulaşan enfeksiyonlar",
                "Genital temasla aktarılan enfeksiyonlar kümesi"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-17-s02",
        "title": "Bulaş Yolları: Mukozal Temastan Vertikal ve Kan Geçişine",
        "content": "CYBE etkenlerinin konağa giriş yolları ve bulaş dinamikleri patojenin tropizmine göre şekillenir:\n\n- **1. Cinsel Temas Yolu (Primer Yol):**\n  - Enfekte vajinal, penil, anal veya oral mukozanın doğrudan temasıyla aktarılır.\n  - Korunmasız vajinal ilişki, anal ilişki veya oral seks sırasında mikroskobik epitel abrazyonlarından patojen dokuya invaze olur.\n- **2. Kan ve Kan Ürünleri Yolu:**\n  - Özellikle HBV, HCV ve HIV gibi viral etkenler kontamine kan transfüzyonu, enjektör paylaşımı veya kesici-delici alet yaralanmalarıyla bulaşır.\n- **3. Vertikal (Anneden Bebeğe) Bulaş:**\n  - **İntrauterin (Transplasental):** Sifiliz (Treponema pallidum) plasentayı geçerek konjenital sifilize yol açar.\n  - **İntrapartum (Doğum Sırasında):** Doğum kanalından geçerken bebeğin gözüne ve solunum yoluna bulaşma (N. gonorrhoeae ve C. trachomatis ile oftalmiya neonatorum; HSV ile neonatal herpes).\n  - **Postpartum:** Emzirme yoluyla HIV ve HBV geçişi.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Bulaş Yolu", "Tipik Patojen Örnekleri", "Kritik Klinik Sonuç"],
                [
                    ["Mukozal Cinsel Temas", "N. gonorrhoeae, C. trachomatis, T. vaginalis, HSV-2", "Üretrit, servisit, genital ülser"],
                    ["Transplasental (Vertikal)", "Treponema pallidum (Sifiliz)", "Konjenital sifiliz, abortus, ölü doğum"],
                    ["Doğum Kanalı Teması", "N. gonorrhoeae, C. trachomatis, HSV", "Neonatal konjonktivit (körlük riski), neonatal pnömoni"],
                    ["Parenteral / Kan Yolu", "HBV, HCV, HIV", "Kronik hepatit, siroz ve immün yetmezlik (AIDS)"]
                ]
            ),
            make_quiz(
                "Doğum eylemi sırasında enfekte servikovajinal sekresyonlarla temas eden bir yenidoğanda purülan göz enfeksiyonuna (oftalmiya neonatorum) yol açabilen iki klasik CYBE bakterisi hangisidir?",
                [
                    {"key": "A", "text": "Neisseria gonorrhoeae ve Chlamydia trachomatis", "isCorrect": True, "explanation": "Doğru cevap A'dır: Gonokok ve klamidya doğum kanalından geçerken yenidoğanın gözüne bulaşarak neonatal konjonktivit oluşturur."},
                    {"key": "B", "text": "Helicobacter pylori ve Salmonella enterica", "isCorrect": False, "explanation": "Gastrointestinal patojenlerdir, CYBE değildir."},
                    {"key": "C", "text": "Mycobacterium tuberculosis ve Corynebacterium diphtheriae", "isCorrect": False, "explanation": "Solunum yolu patojenleridir."},
                    {"key": "D", "text": "Clostridium tetani ve Bacillus anthracis", "isCorrect": False, "explanation": "Toprak ve sporlu anaerop bakterilerdir."}
                ]
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-17-s03",
        "title": "Bakteriyel CYBE Etkenleri: Taksonomi ve Temel Patolojiler",
        "content": "CYBE spektrumunda bakteriler en sık ve en çeşitli tedavi edilebilir tabloyu oluşturur (Sınav Spotu):\n\n- **1. Neisseria gonorrhoeae (Gonokok):** Gram (-) diplokok; bol pürülan akıntılı üretrit, servisit ve pelvik inflamatuvar hastalık (PİH) yapar.\n- **2. Chlamydia trachomatis (D-K Serovarları):** Zorunlu hücre içi bakteri; nongonokokal üretrit, mukopürülan servisit ve sessiz tübal infertilite etkenidir. L1-L3 serovarları lenfogranüloma venereum (LGV) yapar.\n- **3. Treponema pallidum:** Spiroket; primer evrede sert ağrısız şankr, sekonder evrede döküntüler ve kondiloma lata, tersiyer evrede gomlar ve nörosifiliz yapar.\n- **4. Haemophilus ducreyi:** Gram (-) kokobasil; son derece ağrılı, tabanı pürülan ülserlerle seyreden şankroid (yumuşak şankr / ulkus molle) yapar.\n- **5. Mycoplasma genitalium ve Ureaplasma urealyticum:** Hücre duvarı olmayan bakteriler; dirençli nongonokokal üretrit ve servisit etkenleridir.\n- **6. Klebsiella granulomatis:** Donovan cisimcikleri ile karakterize ağrısız granüloma inguinale (donovanozis) etkenidir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Bakteriyel Etken", "Morfoloji ve Biyoloji", "Karakteristik Klinik Tablo"],
                [
                    ["Neisseria gonorrhoeae", "Gram (-) böbrek şeklinde diplokok", "Pürülan üretrit, servisit, disemine gonokoksemi"],
                    ["Chlamydia trachomatis (D-K)", "Zorunlu hücre içi paraziti", "Mukoid akıntılı üretrit, servisit, PİH"],
                    ["Treponema pallidum", "Hareketli spiral spiroket", "Sert ağrısız şankr (sifiliz), sistemik yayılım"],
                    ["Haemophilus ducreyi", "Gram (-) pleomorfik kokobasil", "Yumuşak ve çok ağrılı şankroid ülseri"],
                    ["Mycoplasma genitalium", "Hücre duvarsız mikroorganizma", "Makrolid dirençli inatçı nongonokokal üretrit"]
                ]
            ),
            make_cloze(
                "Cinsel temasla bulaşan ve genital bölgede son derece ağrılı, sarımsı pürülan tabanlı şankroid ülseri yapan bakteri Haemophilus ducreyi etkenidir.",
                "Haemophilus ducreyi",
                "Şankroid (ulkus molle) etkeni olan kokobasil"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-17-s04",
        "title": "Viral CYBE Etkenleri: Kronikleşme ve Onkogenez",
        "content": "Viral CYBE'ler konak genomuna entegre olma veya sinir gangliyonlarında latent kalma yetenekleriyle kronik seyreder:\n\n- **1. Herpes Simpleks Virüsleri (HSV-1 ve HSV-2 - Sınav Spotu):**\n  - Genital herpeste esas etken **HSV-2** olmakla birlikte oral-genital temasla **HSV-1** sıklığı da hızla artmaktadır.\n  - Duyusal sakral ganglionlarda latent kalır; periyodik reaktivasyonlarla ağrılı vezikülo-ülseratif lezyonlar açar.\n- **2. İnsan Papilloma Virüsü (HPV):**\n  - Düşük riskli tipler (**HPV 6 ve 11**): Anogenital siğillere (kondiloma akuminata) yol açar.\n  - Yüksek riskli onkojenik tipler (**HPV 16 ve 18**): Serviks, anüs, penis ve orofarenks kanserlerinin temel nedenidir.\n- **3. İnsan İmmün Yetmezlik Virüsü (HIV):** CD4+ T lenfositleri parçalayarak hücresel bağışıklığı çökertir (AIDS).\n- **4. Hepatit B Virüsü (HBV) ve HCV:** Cinsel sıvılar ve kanla geçer; kronik hepatit, karaciğer sirozu ve hepatosellüler karsinom yapar.\n- **5. Molluscum Contagiosum:** Poxvirüs ailesinden; ortası göbekli (umblike) kubbe şeklinde ağrısız papüller yapar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Düşük Riskli HPV (Tip 6/11) vs Yüksek Riskli HPV (Tip 16/18)",
                "Düşük Riskli HPV (Tip 6 ve 11)",
                "Karnabahar benzeri benign anogenital siğiller (kondiloma akuminata) oluşturur; kanser riski taşımaz.",
                "Yüksek Riskli HPV (Tip 16 ve 18)",
                "E6 ve E7 onkoproteinleri ile p53 ve Rb tümör baskılayıcıları yıkarak serviks karsinomuna yol açar."
            ),
            make_quiz(
                "Genital bölgede ağrısız, karnabahar benzeri ekzofitik siğillerle (kondiloma akuminata) başvuran bir hastada sorumlu primer viral etkenler hangileridir?",
                [
                    {"key": "A", "text": "HPV Tip 16 ve 18", "isCorrect": False, "explanation": "Tip 16 ve 18 yüksek riskli serviks kanseri tipleridir, siğil yapmazlar."},
                    {"key": "B", "text": "HPV Tip 6 ve 11", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kondiloma akuminata lezyonlarının %90'ından düşük riskli HPV 6 ve 11 sorumludur."},
                    {"key": "C", "text": "HSV Tip 1", "isCorrect": False, "explanation": "HSV vezikülo-ülseratif ağrılı lezyon yapar."},
                    {"key": "D", "text": "Hepatit B virüsü", "isCorrect": False, "explanation": "HBV siğil yapmaz, karaciğeri tutar."}
                ]
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-17-s05",
        "title": "Paraziter ve Ektoparaziter Etkenler: Trikomonas ve Kasık Biti",
        "content": "CYBE etkenleri yalnızca mikroskobik bakteri ve virüslerden ibaret değildir; parazitler ve ektoparazitler de bu gruptadır:\n\n- **1. Trichomonas vaginalis (Protozoon - Sınav Spotu):**\n  - Kamçılı (flagellat) bir tek hücreli parazittir.\n  - Morfolojik Özellik: **Kist formu yoktur; yalnızca trofozoit formu bulunur**; bu yüzden dış ortamda hızla ölür ve mutlak doğrudan cinsel temasla bulaşır.\n  - Klinik: Kadınlarda köpüklü, sarı-yeşil, kötü kokulu bol vajinal akıntı ve 'çilek serviks' oluştururken; erkeklerde genellikle asemptomatik üretral kolonizasyon yapar.\n- **2. Phthirus pubis (Kasık Biti / Ektoparazit):**\n  - Kasık kıllarına tutunan ve kan emen yassı bir parazittir (yengeç biti).\n  - Şiddetli perineal kaşıntı, kılların dibinde sirke (yumurta) ve deride mavi-gri lekeler (maculae caeruleae) oluşturur.\n- **3. Sarcoptes scabiei (Uyuz Akarı):**\n  - Epidermiste stratum korneumda tüneller açarak şiddetli gece kaşıntısı yapar; genital bölgede papül ve nodüller sıktır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Paraziter Etken", "Biyolojik Sınıfı", "Karakteristik Klinik Bulgusu", "Tanı Yöntemi"],
                [
                    ["Trichomonas vaginalis", "Kamçılı protozoon (trofozoit)", "Köpüklü sarı-yeşil akıntı, çilek serviks", "SF ile taze bakıda hareketli trofozoitler"],
                    ["Phthirus pubis", "Ektoparazit böcek (kasık biti)", "Kıllarda yumurta (sirke), şiddetli kaşıntı", "Kıllara yapışık bit ve sirkelerin gözle görülmesi"],
                    ["Sarcoptes scabiei", "Ektoparazit akar (uyuz)", "Gece artan kaşıntı, genital tünel ve papüller", "Deri kazıntısında akar, yumurta veya dışkı"]
                ]
            ),
            make_cloze(
                "Dış ortamda kist formu bulunmayan ve sadece hareketli trofozoit formuyla cinsel temasla bulaşan protozoon Trichomonas vaginalis parazitidir.",
                "Trichomonas vaginalis",
                "Köpüklü akıntı ve çilek serviks yapan kamçılı parazit"
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-17-s06",
        "title": "CYBE Sendromik Yelpazesi: Akıntı, Ülser ve Pelvik Ağrı",
        "content": "Dünya Sağlık Örgütü ve Sağlık Bakanlığı protokollerinde CYBE hastaları laboratuvar sonuçları çıkana kadar sendromik yaklaşımla sınıflandırılır:\n\n- **1. Vajinal Akıntı Sendromu:** Vajinal floranın bozulması veya serviksin enfeksiyonu (Bakteriyel vajinozis, Kandidiyazis, Trikomoniyazis).\n- **2. Üretral Akıntı Sendromu:** Erkekte penisten sarı-yeşil veya berrak akıntı gelmesi, idrar yaparken yanma (Gonore, Klamidya, Mikoplazma).\n- **3. Genital Ülser Sendromu:** Genital deride veya mukozada açık yaralar:\n  - Ağrılı ülserler: Şankroid (H. ducreyi), Genital herpes (HSV).\n  - Ağrısız ülserler: Sifiliz (T. pallidum şankrı), Granüloma inguinale, LGV erken lezyonu.\n- **4. Pelvik İnflamatuvar Hastalık (PİH) Sendromu:** Alt karın ve kasık ağrısı, adneksiyal hassasiyet, servikal hareket ağrısı, ateş.\n- **5. İnmemiş Skrotal Şişlik / Epididimit Sendromu:** Skrotumda akut tek taraflı ağrılı şişlik ve kızarıklık.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Sendrom Adı", "Kardinal Yakınmalar", "En Sık Patojenler", "İlk Ampirik Yaklaşım"],
                [
                    ["Vajinal Akıntı", "Kötü koku, kaşıntı, akıntı rengi", "Gardnerella (BV), Candida, T. vaginalis", "Metronidazol ± Flukonazol"],
                    ["Üretral Akıntı", "Dizüri, pürülan/mukoid akıntı", "N. gonorrhoeae, C. trachomatis", "Seftriakson + Azitromisin kombine"],
                    ["Ağrılı Genital Ülser", "Deride yanma, pürülan tabanlı yara", "Haemophilus ducreyi, HSV-2", "Azitromisin/Seftriakson veya Asiklovir"],
                    ["Ağrısız Genital Ülser", "Sert tabanlı, temiz, ağrısız yara", "Treponema pallidum (Primer Sifiliz)", "Benzatin Penisilin G"],
                    ["Pelvik İnflamatuvar Hastalık", "Alt karın ağrısı, ateş, disparoni", "C. trachomatis, N. gonorrhoeae, anaeroblar", "Geniş spektrumlu İV/oral kombinasyon"]
                ]
            ),
            make_quiz(
                "Aşağıdaki genital lezyonlardan hangisi klinik muayenede tipik olarak 'ağrısız' karakterde olmasıyla şankroid ve genital herpesten kesin olarak ayrılır?",
                [
                    {"key": "A", "text": "Haemophilus ducreyi'ye bağlı şankroid ülseri", "isCorrect": False, "explanation": "Şankroid son derece ağrılıdır."},
                    {"key": "B", "text": "HSV-2'ye bağlı genital herpes ülserleri", "isCorrect": False, "explanation": "Herpes vezikül ve ülserleri çok ağrılıdır."},
                    {"key": "C", "text": "Treponema pallidum'a bağlı primer sifiliz sert şankrı", "isCorrect": True, "explanation": "Doğru cevap C'dir: Primer sifiliz şankrı ağrısız, sert tabanlı ve temiz yüzeylidir."},
                    {"key": "D", "text": "Akut flegmonöz abse", "isCorrect": False, "explanation": "Abseler şiddetli ağrılıdır."}
                ]
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-17-s07",
        "title": "Asemptomatik Taşıyıcılık Oranları ve Cinsiyetler Arası Uçurum",
        "content": "CYBE epidemiyolojisinin en tehlikeli boyutu hastaların önemli bir kısmının hiçbir semptom göstermeden enfeksiyonu bulaştırmaya devam etmesidir (Sınav Spotu):\n\n- **Klamidya Asemptomatik Oranları (Uçurum Tablosu):**\n  - **Kadınlarda:** Chlamydia trachomatis ile enfekte kadınların **yaklaşık %80-90'ı tamamen asemptomatiktir** (sessiz enfeksiyon).\n  - **Erkeklerde:** Enfekte erkeklerin yaklaşık %50'si asemptomatiktir.\n  - Tehlike: Semptomsuz kadın doktora gitmez; enfeksiyon yukarıya tırmanarak sessizce fallop tüplerini tıkar ve sekonder infertilite veya dış gebelikle sonuçlanır.\n- **Gonore Asemptomatik Oranları:**\n  - **Kadınlarda:** Enfekte kadınların yaklaşık **%50'si asemptomatiktir**.\n  - **Erkeklerde:** Erkeklerin yalnızca **yaklaşık %10'u asemptomatiktir**; erkeklerin %90'ında şiddetli yanma ve sarı pürülan akıntı başlar ve hasta hızla doktora koşar.\n- **Trikomoniyazis:** Kadınların %10-50'sinde, erkeklerin ise büyük çoğunluğunda subklinik seyreder.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Enfeksiyon Etkeni", "Kadında Asemptomatik Oranı", "Erkekte Asemptomatik Oranı", "Klinik Yansıması"],
                [
                    ["Chlamydia trachomatis", "%80 - 90'a varan (çok yüksek)", "%50'ye varan", "Kadında sessiz tübal hasar ve kısırlık riski"],
                    ["Neisseria gonorrhoeae", "%50'ye varan", "~%10 (erkeklerin %90'ı semptomatik)", "Erkek hızla tedaviye gider, kadın bulaştırıcı kalabilir"],
                    ["Trichomonas vaginalis", "%10 - 50", "Çoğunlukla asemptomatik", "Erkek partner rezervuar görevi görür"]
                ]
            ),
            make_quiz(
                "Cinsel yolla bulaşan enfeksiyonlar içinde kadınlarda asemptomatik seyretme oranı en yüksek (%80-90'a varan) olan ve sessiz tübal hasarla infertiliteye yol açan bakteri hangisidir?",
                [
                    {"key": "A", "text": "Neisseria gonorrhoeae", "isCorrect": False, "explanation": "Gonorede kadında asemptomatik oran ~%50'dir."},
                    {"key": "B", "text": "Chlamydia trachomatis", "isCorrect": True, "explanation": "Doğru cevap B'dir: Klamidya kadınlarda %90'a varan oranda asemptomatiktir ve kısırlığın en sinsi nedenidir."},
                    {"key": "C", "text": "Haemophilus ducreyi", "isCorrect": False, "explanation": "Şankroid ağrılı ülser yapar, asemptomatik kalmaz."},
                    {"key": "D", "text": "Phthirus pubis", "isCorrect": False, "explanation": "Kasık biti şiddetli kaşıntı yapar."}
                ]
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-17-s08",
        "title": "Tanısal Yöntemler: Direkt Mikroskopi, NAAT ve Kültürün Rolü",
        "content": "CYBE tanısında doğru örnek alma ve uygun laboratuvar yöntemi seçimi tedavinin başarısını belirler:\n\n- **1. Direkt Mikroskopi ve Boyama:**\n  - **Gram Boyama:** Erkek üretral akıntısında nötrofiller içinde Gram (-) diplokok görülmesi gonore için **%95'in üzerinde duyarlı ve özgüldür**.\n  - **Serum Fizyolojik Taze Bakı:** Hareketli kamçılı T. vaginalis trofozoitleri ve Clue cell (ipucu hücreleri) anında saptanır.\n  - **%10 KOH Preparatı:** Candida mayaları ve psödohifleri görünür hale gelir; Whiff testiyle amin kokusu araştırılır.\n- **2. Nükleik Asit Amplifikasyon Testleri (NAAT - Altın Standart - Sınav Spotu):**\n  - Chlamydia trachomatis, N. gonorrhoeae, M. genitalium ve HSV tanısında en yüksek duyarlılık ve özgüllüğe sahip altın standarttır.\n  - Kadında vajinal sürüntü, erkekte ilk idrar örneğinde kolayca çalışılır; canlı bakteri gerekmez.\n- **3. Mikrobiyolojik Kültür:**\n  - N. gonorrhoeae kültürü (Thayer-Martin besiyeri, %10 CO2) canlı organizma gerektirir; en büyük avantajı **antimikrobiyal duyarlılık testi (antibiyogram)** yapılabilmesidir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Nükleik Asit Testleri (NAAT) vs Mikrobiyolojik Kültür",
                "NAAT (Moleküler Test)",
                "En yüksek duyarlılığa sahiptir; ölü bakteriyi bile saptar; klamidya ve gonorede ilk basamak altın standarttır.",
                "Mikrobiyolojik Kültür",
                "Canlı bakteri gerektirir; zahmetlidir ancak antibiyotik direnç profili ve antibiyogram için vazgeçilmezdir."
            ),
            make_cloze(
                "Klamidya ve gonore tanısında günümüzde en yüksek duyarlılık ve özgüllüğe sahip altın standart yöntem nükleik asit amplifikasyon testleri (NAAT) yöntemidir.",
                "nükleik asit amplifikasyon testleri",
                "Moleküler DNA/RNA çoğaltma tanı testi"
            )
        ]
    })

    # Slide 9 - CHECKPOINT 1
    slides.append({
        "id": "k1-17-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] CYBE Epidemiyolojisi ve Etken Sınıflaması",
        "content": "Bu checkpointte CYBE etkenlerinin sınıflamasını, bulaş yollarını ve asemptomatik seyir dinamiklerini pekiştiriyoruz:\n\n- **Bakteriyel Etkenler:** N. gonorrhoeae (diplokok), C. trachomatis (hücre içi), T. pallidum (spiroket), H. ducreyi (ağrılı şankroid), M. genitalium (duvarsız).\n- **Viral Etkenler:** HSV-2 (ağrılı vezikülo-ülser), HPV 6/11 (siğil), HPV 16/18 (kanser), HIV ve HBV/HCV.\n- **Parazitler:** T. vaginalis (kisti olmayan kamçılı protozoon), Phthirus pubis (kasık biti), Sarcoptes scabiei (uyuz).\n- **Bulaş:** Mukozal temas, transplasental (sifiliz), doğum kanalı (neonatal konjonktivit), kan ürünleri.\n- **Asemptomatik Uçurum:** Kadınlarda klamidya %90, gonore %50 asemptomatiktir; erkeklerde gonore %90 belirgin semptom verir.\n- **Tanı Kriterleri:** NAAT altın standarttır; N. gonorrhoeae kültürü ise antibiyogram için zorunludur.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Patojen", "Taksonomi", "Asemptomatik Oranı (Kadın / Erkek)", "Başlıca Klinik Sonuç"],
                [
                    ["C. trachomatis", "Hücre içi bakteri", "%80-90 / %50", "Mukopürülan servisit, tübal infertilite, PİH"],
                    ["N. gonorrhoeae", "Gram (-) diplokok", "%50 / %10", "Pürülan üretrit/servisit, disemine gonokoksemi"],
                    ["T. vaginalis", "Kamçılı protozoon", "%10-50 / Yüksek", "Köpüklü vajinit, çilek serviks"],
                    ["T. pallidum", "Spiroket", "Gizli (latent) evreler", "Sert şankr, konjenital sifiliz, nörosifiliz"]
                ]
            ),
            make_chain(
                "CYBE Patojen İnvazyonundan Kliniğe Gidiş",
                [
                    "1. Mukozal İnokülasyon: Korunmasız cinsel temasla patojen genital mukozaya yerleşir.",
                    "2. Kolonizasyon ve Sessiz Evre: Kadınlarda klamidya %90 oranında semptomsuz çoğalır.",
                    "3. Asendan Yayılım: Bakteri serviksten endometriyum ve fallop tüplerine tırmanır.",
                    "4. İnfertilite Komplikasyonu: Tüplerde fibrozis ve tıkanma kalıcı kısırlık yaratır."
                ]
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-17-s10",
        "title": "Bölüm Özeti: Epidemiyolojiden Vajinal ve Servikal Akıntılara Geçiş",
        "content": "Bölüm 1 boyunca cinsel yolla bulaşan enfeksiyonların mikrobiyolojik etkenlerini, bulaş yollarını ve laboratuvar tanı ilkelerini inceledik:\n\n- **Kritik Çıkarım:** Semptomsuz bireyler toplumdaki en büyük rezervuardır; tarama ve partner tedavisi bu zinciri kırmada esastır.\n- **Sonraki Bölüm:** Bir sonraki bölümde kadınlarda en sık başvuru nedeni olan vajinal akıntı sendromunu, **vajinit (Bakteriyel vajinozis, Kandidiyazis) ile servisit ayrımını** ve tanısal püf noktalarını inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Cinsel yolla bulaşan enfeksiyonların tanısında canlı bakteri gerektirmeyen ve en yüksek duyarlılık/özgüllüğe sahip altın standart moleküler yöntem nedir?",
                "Nükleik asit amplifikasyon testleri (NAAT)",
                "DNA/RNA çoğaltma temelli altın standart yöntem"
            ),
            make_quiz(
                "Neisseria gonorrhoeae enfeksiyonunda NAAT testi mevcut olmasına rağmen mikrobiyolojik kültürün halen vazgeçilmez bir tanı basamağı olmasının en önemli nedeni nedir?",
                [
                    {"key": "A", "text": "Kültürün 10 dakikada sonuç vermesi", "isCorrect": False, "explanation": "Kültür 24-48 saat sürer."},
                    {"key": "B", "text": "Antibiyotik direnç profilinin belirlenebilmesi ve antibiyogram yapılabilmesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kültürün en kritik üstünlüğü izole edilen canlı bakteride antibiyogram yapılabilmesidir."},
                    {"key": "C", "text": "Kültürün klamidyayı da aynı anda üretmesi", "isCorrect": False, "explanation": "Klamidya rutin Thayer-Martin besiyerinde üremez."},
                    {"key": "D", "text": "Kültürün sadece kanda çalışılabilmesi", "isCorrect": False, "explanation": "Genital sürüntüden ekilir."}
                ]
            )
        ]
    })

    return slides
