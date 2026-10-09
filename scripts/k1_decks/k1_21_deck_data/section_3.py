# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 3: Prokaryotlar: Tipik ve Atipik Bakteriler (Slayt 21 - 30)
Checkpoint 3: Slayt 29
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # Slayt 21: Bakteriyel Morfoloji ve Sınıflandırma
    slides.append({
        "id": "k1-21-s21",
        "title": "Bakteriyel Morfoloji ve Genel Sınıflandırma İlkeleri",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 21,
        "narrative": (
            "Bakteriler, gerçek çekirdek zarı ve mitokondri gibi zarlı organelleri bulunmayan, "
            "genetik materyali nükleoid adı verilen sitoplazmik bölgede tek çembersel çift iplikli DNA halinde organize olmuş "
            "prokaryotik tek hücreli mikroorganizmalardır. Mikroskobik morfolojilerine göre 4 ana grupta incelenirler: "
            "1. **Koklar (Yuvarlak/Küre):** Tek tek, ikili (diplokok: Streptococcus pneumoniae, Neisseria), "
            "zincirler halinde (Streptococcus pyogenes) veya üzüm salkımı şeklinde (Staphylococcus aureus) kümelenirler. "
            "2. **Basiller (Çomak):** Düz silindirik çubuklardır (Escherichia coli, Klebsiella pneumoniae, Pseudomonas aeruginosa, Mycobacterium tuberculosis). "
            "3. **Kıvrık / Virgül Şekilli:** Kıvrımlı çomaklardır (Vibrio cholerae, Campylobacter jejuni, Helicobacter pylori). "
            "4. **Spiroketler (Spiral / Tirbüşon):** Aksiyel filamanları sayesinde dalgalı burgu hareketi yapan esnek bakterilerdir "
            "(Treponema pallidum, Borrelia burgdorferi, Leptospira interrogans). "
            "Bakteriler ayrıca oksijen gereksinimlerine göre zorunlu aerop, zorunlu anaerop veya fakültatif anaerop olarak sınıflandırılırlar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Aksiyel filamanları sayesinde tirbüşon şeklinde burgu hareketi yapan spiral morfolojili bakterilere spiroketler adı verilir.",
                "spiroketler",
                "Treponema ve Borrelia'nın dahil olduğu spiral bakteri grubu"
            ),
            make_table(
                ["Morfolojik Sınıf", "Hücresel Şekil ve Dizilim", "Karakteristik Tıbbi Örnekler"],
                [
                    ["Salkım Koklar", "Üzüm salkımı şeklinde kümelenen gram-pozitif koklar", "Staphylococcus aureus, S. epidermidis"],
                    ["Zincir Koklar", "Uç uca zincirler oluşturan gram-pozitif koklar", "Streptococcus pyogenes (GAS), S. agalactiae"],
                    [
                        "Gram-Negatif Basiller",
                        {"text": "Çubuk şeklinde silindirik bakteriler", "isMasked": True, "hint": "GİS ve üriner sistemde en sık görülen morfoloji"},
                        "Escherichia coli, Klebsiella pneumoniae, Salmonella"
                    ],
                    ["Kıvrık / Virgül Basiller", "Virgül veya martı kanadı şeklinde kıvrımlı", "Vibrio cholerae, Campylobacter, Helicobacter pylori"]
                ]
            ),
            make_micro_quiz(
                "Mikroskop altında 'üzüm salkımı' şeklinde kümelenen gram-pozitif kok morfolojisi aşağıdaki bakterilerden hangisi için patognomoniktir?",
                {
                    "A": "Streptococcus pneumoniae",
                    "B": "Neisseria meningitidis",
                    "C": "Staphylococcus aureus",
                    "D": "Escherichia coli",
                    "E": "Treponema pallidum"
                },
                "C",
                {
                    "A": "A seçeneği lanset şeklinde ikili diplokoktur.",
                    "B": "B seçeneği böbrek şeklinde gram-negatif diplokoktur.",
                    "C": "C seçeneği doğrudur: 'Staphyle' Yunanca üzüm salkımı demektir; Staphylococcus türleri salkım kümesi yapar.",
                    "D": "D seçeneği çomak (basil) şekillidir.",
                    "E": "E seçeneği spiral spirokettir."
                }
            )
        ]
    })

    # Slayt 22: Bakteri Hücre Duvarı Mimarisi ve Gram Boyanma
    slides.append({
        "id": "k1-21-s22",
        "title": "Hücre Duvarı Mimarisi ve Gram Boyanma Biyokimyası",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 22,
        "narrative": (
            "Mikroplazmalar hariç tüm bakterilerin plazma zarını dıştan saran sağlam bir **hücre duvarı** bulunur. "
            "Hücre duvarı bakteriyi ozmotik lizisten korur ve Christian Gram tarafından 1884'te geliştirilen "
            "Gram boyama yönteminin temelini oluşturur: "
            "1. **Gram-Pozitif Hücre Duvarı:** Çok katmanlı, son derece kalın bir **peptidoglikan** zırhına (murein) sahiptir. "
            "Peptidoglikan tabakasına dik olarak yerleşmiş **teikoik asit** ve **lipoteikoik asit** molekülleri içerir. "
            "Gram boyamada kristal viyole-iyot kompleksini kalın gözeneklerinde tutarak mor/koyu mavi boyanır. "
            "Dış membran taşımazlar. "
            "2. **Gram-Negatif Hücre Duvarı:** Yalnızca tek veya iki katmanlı incecik bir peptidoglikan tabakası içerir. "
            "Bunun üzerinde fosfolipidler, porin proteinleri ve **Lipopolisakkarit (LPS)** içeren bir **Dış Membran** bulunur. "
            "İnce peptidoglikan tabakası alkol ile renksizleşir ve zıt boya safranin/fuksin ile pembe/kırmızı boyanır. "
            "LPS'nin **Lipid A** kısmı insan bağışıklık sisteminde septik şoku tetikleyen meşhur **endotoksindir**!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Gram-negatif bakterilerin dış membranında bulunan ve endotoksin aktivitesinden sorumlu olan bileşen Lipopolisakkaritin Lipid A parçasıdır.",
                "Lipid A",
                "Septik şok ve sitokin fırtınasını tetikleyen endotoksin toksik ucu"
            ),
            make_before_after(
                "Gram-Pozitif ile Gram-Negatif Hücre Duvarı Karşılaştırması",
                "Gram-Pozitif Hücre Duvarı",
                [
                    "Çok kalın (40-80 kat) sağlam peptidoglikan tabakası",
                    "Teikoik asit ve lipoteikoik asit antijenleri bulunur",
                    "Dış membran ve lipopolisakkarit (LPS) kesinlikle içermez",
                    "Gram boyama sonucunda koyu mor/mavi renk alır"
                ],
                "Gram-Negatif Hücre Duvarı",
                [
                    "Oldukça ince (1-2 kat) peptidoglikan tabakası ve periplazmik aralık",
                    "Porinler ve Lipopolisakkarit (LPS) içeren asimetrik Dış Membran var",
                    "Lipid A endotoksini ile mortalitesi yüksek septik şok tetikler",
                    "Gram boyama sonucunda pembe/kırmızı renk alır"
                ]
            ),
            make_active_recall(
                "Gram-negatif bakterilerde iç sitoplazmik membran ile dış membran arasında bulunan ve beta-laktamaz enzimlerinin salgılandığı boşluğa ne ad verilir?",
                "Periplazmik aralık (periplazma) adı verilir.",
                "Gram negatiflerde peptidoglikanı barındıran membranlar arası aralık"
            )
        ]
    })

    # Slayt 23: Bakteriyel Virülans ve Hareket Organelleri
    slides.append({
        "id": "k1-21-s23",
        "title": "Bakteriyel Organeller: Kapsül, Pili, Flagella ve Spor",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 23,
        "narrative": (
            "Bakteriler hücre duvarlarının dışında yaşamsal avantaj ve virülans sağlayan özelleşmiş yapılar taşırlar: "
            "1. **Kapsül:** Genellikle polisakkarit (istisna: Bacillus anthracis poli-D-glutamik asit protein kapsülü taşır) yapılı gevşek dış tabakadır. "
            "Bakteriyi nötrofil ve makrofajların fagositozundan korur; kapsüllü bakteriler (S. pneumoniae, N. meningitidis, H. influenzae) "
            "dalağı alınmış (asplenik) bireylerde öldürücü fulminan sepsise yol açar. "
            "2. **Pili (Fimbriya):** Bakterinin konak epitel hücrelerine tutunmasını sağlayan ince kılcal uzantılardır (adezyon organeli). "
            "Üropatojen E. coli P-pilileri ile mesane/üreter epiteline, Neisseria gonorrhoeae ise üretral mukozaya tutunur. "
            "Özel seks pilisi (F-pilus) ise konjugasyon ile plazmid aktarımını sağlar. "
            "3. **Flagella (Kamçı):** Flagellin proteininden oluşan ve bakteriye aktif hareket (motilite) kazandıran pervanemsi yapıdır. "
            "4. **Endospor:** Yalnızca **Bacillus** ve **Clostridium** cinslerinde görülen, besin kıtlığında oluşan metabolik olarak uykuda (dormant) yapılardır. "
            "Kalsiyum dipikolinat içeriği sayesinde kaynatmaya, kuruluğa, dezenfektanlara yıllarca direnç gösterir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Bakteriyel endosporun yüksek ısıya ve kuruluğa olağanüstü direnç kazanmasını sağlayan kilit kimyasal madde kalsiyum dipikolinat bileşiğidir.",
                "kalsiyum dipikolinat",
                "Sporda dehidrasyon ve termal stabilite sağlayan tuz kompleksi"
            ),
            make_table(
                ["Bakteriyel Yapı", "Biyokimyasal İçerik", "Primer Virülans ve Fonksiyonu"],
                [
                    ["Kapsül", "Polisakkarit (B. anthracis'te polipeptid)", "Fagositozu engelleme ve komplemandan kaçış"],
                    [
                        "Pili (Fimbriya)",
                        {"text": "Pilin proteini", "isMasked": True, "hint": "Mukozal epitele tutunma faktörü"},
                        "Epitel hücrelerine adezyon ve konjugasyonla gen aktarımı"
                    ],
                    ["Flagella", "Flagellin proteini (H antijeni)", "Kemotaksis doğrultusunda aktif burgu hareketi"],
                    ["Endospor", "Kalsiyum dipikolinat ve keratin kılıf", "Çevre koşullarında onlarca yıl metabolik dormant sağkalım"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki bakteri türlerinden hangisi polisakkarit yerine 'poli-D-glutamik asit (protein)' yapısında kapsül taşımasıyla mikrobiyolojide benzersiz bir istisnadır?",
                {
                    "A": "Streptococcus pneumoniae",
                    "B": "Neisseria meningitidis",
                    "C": "Bacillus anthracis (Şarbon basili)",
                    "D": "Klebsiella pneumoniae",
                    "E": "Haemophilus influenzae"
                },
                "C",
                {
                    "A": "A seçeneği polisakkarit kapsüllüdür.",
                    "B": "B seçeneği polisakkarit kapsüllüdür.",
                    "C": "C seçeneği doğrudur: Şarbon etkeni Bacillus anthracis protein (poli-D-glutamik asit) kapsüllü tek bakteridir.",
                    "D": "D seçeneği kalın mukoid polisakkarit kapsüllüdür.",
                    "E": "E seçeneği polisakkarit (PRP) kapsüllüdür."
                }
            )
        ]
    })

    # Slayt 24: Atipik Bakteriler I: Klamidyalar
    slides.append({
        "id": "k1-21-s24",
        "title": "Atipik Bakteriler I: Klamidyalar ve Enerji Parazitliği",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 24,
        "narrative": (
            "Klamidyalar (Chlamydiaceae familyası), prokaryotik yapıda olmalarına rağmen biyokimyasal olarak "
            "kendi ATP'lerini sentezleyemedikleri için konak hücresinin enerjisine tam bağımlı olan "
            "**zorunlu hücre içi (obligat intrasellüler) enerji parazitleridir**. "
            "Hücre duvarlarında Gram-negatif dış membran benzeri bir yapı bulunmasına rağmen peptidoglikan tabakası "
            "klasik bakterilerdeki gibi saptanamaz. Cansız yapay besiyerlerinde asla üreyemezler; "
            "laboratuvarda hücre kültürlerinde veya embriyonlu yumurtada üretilirler. "
            "Klamidyaların yaşam döngüsü iki farklı morfolojik form arasında gidip gelir: "
            "1. **Elementer Cisimcik (EB):** Metabolik olarak inaktiftir ancak dış ortamda stabil ve **enfeksiyöz** formdur; "
            "konak epitel hücresine tutunup endositozla içeri girer. "
            "2. **Retiküler Cisimcik (RB):** Hücre içinde fagozomda oluşan, metabolik olarak aktif, "
            "bölünerek çoğalan ancak hücre dışında yaşayamayan **non-enfeksiyöz** replikasyon formudur. "
            "Bölünme tamamlanınca RB'ler yeniden EB'ye dönüşür, hücre patlar ve yeni hücreleri enfekte eder."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Klamidyaların yaşam döngüsünde hücre dışında stabil olan enfeksiyöz forma elementer cisimcik adı verilir.",
                "elementer cisimcik",
                "Klamidyanın dış ortamda bulaşıcı olan küçük dayanıklı formu"
            ),
            make_before_after(
                "Klamidya Yaşam Döngüsünün İki Formu",
                "Elementer Cisimcik (EB)",
                [
                    "Morfoloji: Küçük (0.3 µm), yoğun kromatinli sert yapı",
                    "Metabolik durum: Metabolik olarak uykuda (inaktif)",
                    "Enfektivite: Hücre dışı ortamda stabil ve yüksek derecede enfeksiyöz",
                    "Fonksiyon: Konak hücreye tutunma ve enfeksiyonu başlatma"
                ],
                "Retiküler Cisimcik (RB)",
                [
                    "Morfoloji: Daha büyük (1 µm), gevşek yapılı metabolik hücre",
                    "Metabolik durum: Metabolik olarak aktif, konak ATP'sini kullanan form",
                    "Enfektivite: Hücre dışında yaşayamaz ve non-enfeksiyözdür",
                    "Fonksiyon: Fagozom içinde ikili fizyonla çoğalma ve replikasyon"
                ]
            ),
            make_active_recall(
                "Klamidyaların kendi başlarına ATP sentezleyememeleri ve konak hücresinin metabolik enerjisine mutlak bağımlı olmaları hangi mikrobiyolojik terimle adlandırılır?",
                "Enerji parazitliği (enerji paraziti) adı verilir.",
                "Konak nükleotid havuzuna bağımlı zorunlu hücre içi yaşam tarzı"
            )
        ]
    })

    # Slayt 25: Klamidya Türleri ve Kliniği
    slides.append({
        "id": "k1-21-s25",
        "title": "Klamidya Türleri: C. trachomatis, C. pneumoniae ve C. psittaci",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 25,
        "narrative": (
            "Klamidya cinsinde insan patolojisinde kritik rol oynayan 3 temel tür bulunur: "
            "1. **Chlamydia trachomatis:** İmmünolojik serovarlarına göre tamamen farklı hastalıklar oluşturur: "
            "- **Serovar A, B, Ba, C:** Göz enfeksiyonu olan **Trahom** etkenidir; dünyada önlenebilir körlüğün 1 numaralı bulaşıcı nedenidir. "
            "- **Serovar D - K:** Dünyada en sık görülen bakteriyel **cinsel yolla bulaşan enfeksiyon (CYBE)** etkenidir. "
            "Erkekte nongonokoksik üretrit; kadında servisit, pelvik inflamatuar hastalık (PİH), ektopik gebelik ve infertilite yapar. "
            "Enfekte doğum kanalından geçen bebekte inklüzyon konjonktiviti ve atipik yenidoğan pnömonisi oluşturur. "
            "- **Serovar L1, L2, L3:** Kasık lenf bezlerinde süpürasyon ve fistülleşmeyle seyreden **Lenfogranüloma Venereum (LGV)** etkenidir. "
            "2. **Chlamydia pneumoniae:** Toplum kökenli atipik pnömoni, farenjit ve bronşit yapar; ateroskleroz patogeneziyle ilişkisi araştırılmaktadır. "
            "3. **Chlamydia psittaci:** Papağan ve muhabbet kuşu gibi kafes kuşlarının dışkı tozlarının solunmasıyla bulaşan "
            "ve hepatosplenomegali ile seyredebilen ağır atipik pnömoni (**Psittakoz / Papağan humması**) etkenidir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Chlamydia trachomatis serovar A, B ve C suşları dünyada önlenebilir bulaşıcı körlüğün en sık nedeni olan trahom tablosuna yol açar.",
                "trahom",
                "Göz kapağında skatrisyel körlük yapan klamidya hastalığı"
            ),
            make_table(
                ["Klamidya Türü ve Serovarı", "Bulaş Yolu / Rezervuar", "Karakteristik Klinik Hastalık"],
                [
                    ["C. trachomatis Serovar A-C", "Gözden göze temas, sinekler, havlu", "Trahom (kronik keratokonjonktivit ve körlük)"],
                    [
                        "C. trachomatis Serovar D-K",
                        {"text": "Cinsel temas ve doğum kanalı", "isMasked": True, "hint": "En yaygın ürogenital klamidya patolojisi"},
                        "Nongonokoksik üretrit, servisit, PİH ve yenidoğan konjonktiviti"
                    ],
                    ["C. trachomatis Serovar L1-L3", "Cinsel temas", "Lenfogranüloma Venereum (Ağrılı oluklu kasık bubonları)"],
                    ["Chlamydia psittaci", "Enfekte kuş dışkısı / aerosolleri", "Psittakoz (Ağır atipik pnömoni ve splenomegali)"]
                ]
            ),
            make_micro_quiz(
                "Evinde papağan besleyen bir kuş meraklısında yüksek ateş, kuru öksürük, baş ağrısı ve splenomegali ile seyreden atipik pnömoni tablosunda en olası etken hangisidir?",
                {
                    "A": "Mycoplasma hominis",
                    "B": "Chlamydia psittaci",
                    "C": "Streptococcus pyogenes",
                    "D": "Rickettsia prowazekii",
                    "E": "Treponema pallidum"
                },
                "B",
                {
                    "A": "A seçeneği ürogenital patojendir.",
                    "B": "B seçeneği doğrudur: Psittasin kuşlardan (papağan, muhabbet kuşu) bulaşan Chlamydia psittaci psittakoz (papağan humması) etkenidir.",
                    "C": "C seçeneği bakteriyel farenjit ve lober pnömoni yapar, kuşlarla ilişkisizdir.",
                    "D": "D seçeneği bit kaynaklı tifüs etkenidir.",
                    "E": "E seçeneği sifilis etkenidir."
                }
            )
        ]
    })

    # Slayt 26: Atipik Bakteriler II: Mikoplazmalar
    slides.append({
        "id": "k1-21-s26",
        "title": "Atipik Bakteriler II: Mikoplazmalar ve Hücre Duvarı Yokluğu",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 26,
        "narrative": (
            "Mikoplazmalar (Mycoplasmataceae), serbest yaşayabilen ve yapay cansız besiyerlerinde üreyebilen "
            "en küçük prokaryotik mikroorganizmalardır. Mikoplazmaların mikrobiyolojideki en çarpıcı ve eşsiz özelliği: "
            "**Hücre duvarlarının (peptidoglikan tabakasının) kesinlikle bulunmamasıdır!** "
            "Hücre duvarı bulunmadığı için rijit bir şekilleri yoktur, son derece esnek ve pleomorfiktirler (küre, ipliksi, armut şeklinde). "
            "Hücre duvarının yokluğunda ozmotik basınca direnebilmek için sitoplazmik zarlarında konaktan aldıkları **kolesterol** moleküllerini taşırlar "
            "(zarlarında sterol taşıyan tek bakteri grubudur). "
            "Bu biyokimyasal özellik iki devrimsel tıbbi sonuç doğurur: "
            "1. **Gram ile Boyanmazlar:** Hücre duvarı olmadığı için Gram boyamada mikroskopta görülemezler. "
            "2. **Doğal (İntrensek) Antibiyotik Direnci:** Hücre duvarı sentezini hedef alan tüm antibiyotiklere "
            "(penisilinler, ampisilin, sefalosporinler, karbapenemler, vankomisin) karşı **tamamen dirençlidirler!** "
            "Tedavide ribozomal protein sentezini bozan makrolidler (azitromisin) veya doksisiklin kullanılır. "
            "Klinikte **Mycoplasma pneumoniae** genç erişkinlerde soğuk aglütinin pozitifliği ile seyreden atipik 'yürüyen pnömoni' (walking pneumonia) yapar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mikoplazmalar hücre duvarı taşımadıkları için hücre duvarı sentezini hedefleyen beta-laktam antibiyotiklere karşı doğal olarak intrensek dirençlidir.",
                "intrensek dirençlidir",
                "Bakterinin yapısından kaynaklanan doğal ilaç direnci durumu"
            ),
            make_table(
                ["Mikoplazma Özelliği", "Biyokimyasal Açıklaması", "Klinik / Laboratuvar Sonucu"],
                [
                    ["Hücre Duvarı Durumu", "Peptidoglikan tabakası tamamen yok", "Gram boyama ile mikroskopta görülemez"],
                    [
                        "Hücre Zarı Yapısı",
                        {"text": "Zarda kolesterol (sterol) barındırma", "isMasked": True, "hint": "Memeli hücre zarına benzeyen lipid stabilizasyonu"},
                        "Ozmotik basınca dayanıklılık ve esnek pleomorfik şekil"
                    ],
                    ["Antibiyotik Duyarlılığı", "Penisilin bağlayan protein (PBP) ve peptidoglikan yok", "Beta-laktamlar etkisiz; makrolid ve tetrasiklin zorunlu"],
                    ["Yapay Besiyeri Üremesi", "Sterol zengin PPLO agarda ürer", "Karakteristik 'sahanda yumurta' kolonileri"]
                ]
            ),
            make_micro_quiz(
                "Mycoplasma pneumoniae kaynaklı atipik pnömoni tanısı alan 22 yaşındaki bir üniversite öğrencisinde aşağıdaki antibiyotiklerden hangisinin reçete edilmesi farmakolojik olarak tamamen etkisizdir?",
                {
                    "A": "Azitromisin",
                    "B": "Doksisiklin",
                    "C": "Levofloksasin",
                    "D": "Amoksisilin-Klavulanat (Beta-laktam)",
                    "E": "Klaritromisin"
                },
                "D",
                {
                    "A": "A seçeneği 50S ribozom inhibitörüdür, mikoplazmada oldukça etkilidir.",
                    "B": "B seçeneği 30S inhibitörüdür, etkilidir.",
                    "C": "C seçeneği DNA giraz inhibitörüdür, etkilidir.",
                    "D": "D seçeneği doğrudur: Amoksisilin hücre duvarı peptidoglikan sentezini hedefler; mikoplazmada hücre duvarı hiç bulunmadığı için amoksisilin tamamen etkisizdir.",
                    "E": "E seçeneği makroliddir, etkilidir."
                }
            )
        ]
    })

    # Slayt 27: Atipik Bakteriler III: Riketsiyalar
    slides.append({
        "id": "k1-21-s27",
        "title": "Atipik Bakteriler III: Riketsiyalar ve Endotel Tropizmi",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 27,
        "narrative": (
            "Riketsiyalar (Rickettsiaceae familyası), küçük, pleomorfik, Gram-negatif hücre duvarı yapısına sahip "
            "ancak klamidyalar gibi konak hücresi dışında çoğalamayan **zorunlu hücre içi (obligat intrasellüler)** bakterilerdir. "
            "Riketsiyaların patolojideki en belirleyici ve karakteristik niteliği **vasküler endotel hücre tropizmidir**. "
            "İnsan vücuduna girdiklerinde özellikle küçük kan damarlarının (kapiller ve venüller) endotel hücrelerini enfekte ederler. "
            "Endotel içinde çoğalarak hücre lizisine, yaygın mikrovasküler endotel hasarına ve perivasküler mononükleer inflamasyona yol açarlar. "
            "Bu patofizyolojik süreç yaygın **vaskülit, mikrotrombüsler, vasküler geçirgenlik artışı, ekstravazasyon ve peteşiyal deri döküntüleri** ile sonlanır. "
            "Hemen hemen tüm riketsiyozlar insanlara eklem bacaklı (artropod) vektörlerin (kene, pire, bit, akar) "
            "ısırması veya dışkısının kaşınarak deriye yedirilmesi ile bulaşır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Riketsiyaların insan vücudunda küçük damarların endotel hücrelerini hedef alarak çoğalması yaygın vaskülit tablosuna yol açar.",
                "vaskülit",
                "Damar duvarı inflamasyonunu ifade eden patolojik lezyon"
            ),
            make_causal_chain(
                "Riketsiyal Vaskülit ve Döküntü Mekanizması",
                [
                    "1. Artropod Isırığı: Kene veya bitin inokülasyonu ile riketsiya dermal kapillere girer.",
                    "2. Endotelyal Giriş: Bakteri vasküler endotel hücrelerine fagositozla alınır ve sitoplazmaya kaçar.",
                    "3. Hücre İçi Çoğalma: Endotel hücreleri içinde ikili bölünmeyle hızla çoğalır.",
                    "4. Endotelyal Hasar: Hücrelerin parçalanmasıyla yaygın lökositoklastik vaskülit ve tromboz gelişir.",
                    "5. Peteşiyal Döküntü: Damar geçirgenliğinin bozulması ve eritrosit sızıntısıyla purpurik döküntüler belirir."
                ]
            ),
            make_active_recall(
                "Riketsiya cinsi bakterilerin konak dokusunda primer olarak enfekte edip çoğaldığı ve vaskülit oluşturduğu anahtar hedef hücre türü hangisidir?",
                "Vasküler endotel hücreleridir (damar endoteli).",
                "Kan damarlarının iç yüzeyini döşeyen hücre"
            )
        ]
    })

    # Slayt 28: Akdeniz Benekli Ateşi ve Tifüs
    slides.append({
        "id": "k1-21-s28",
        "title": "Akdeniz Benekli Ateşi (Tache Noire) ve Epidemik Tifüs",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 28,
        "narrative": (
            "Riketsiyozlar tıbbi ve coğrafi özelliklerine göre iki büyük gruba ayrılır: "
            "1. **Benekli Ateş Grubu:** "
            "- **Akdeniz Benekli Ateşi (Boutonneuse Fever):** Etkeni **Rickettsia conorii**'dir. "
            "Vektörü kahverengi köpek kenesi (**Rhipicephalus sanguineus**)'dir. "
            "Türkiye'de ve tüm Akdeniz havzasında son derece yaygın ve klinik olarak çok önemlidir. "
            "Kenenin ısırdığı yerde merkezinde nekrotik siyah bir kabuk bulunan ağrısız primer lezyon gelişir; "
            "bu lezyona **Tache Noire (Kara Leke)** adı verilir ve tanı için patognomoniktir! "
            "Bunu takiben yüksek ateş ve avuç içi ile ayak tabanlarını da tutan makülopapüler-peteşiyal döküntü gelişir. "
            "- **Kayalık Dağlar Benekli Ateşi (RMSF):** Kuzey Amerika'da Rickettsia rickettsii kaynaklı fatal vaskülittir. "
            "2. **Tifüs Grubu:** "
            "- **Epidemik Tifüs:** Etkeni **Rickettsia prowazekii**'dir. İnsan vücut biti (**Pediculus humanus**) ile bulaşır; "
            "savaşlar, mülteci kampları ve hijyenin çöktüğü kalabalık ortamlarda ölümcül salgınlar yapar. "
            "Yıllar sonra reaktivasyonuna **Brill-Zinsser hastalığı** denir. "
            "- **Endemik (Murin) Tifüs:** Etkeni Rickettsia typhi'dir; sıçan piresi (Xenopsylla cheopis) ile bulaşır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Akdeniz benekli ateşinde kenenin ısırdığı yerde gelişen ortası siyah nekrotik eskar lezyonuna tache noire adı verilir.",
                "tache noire",
                "Fransızca kara leke anlamına gelen patognomonik deri lezyonu"
            ),
            make_table(
                ["Riketsiyoz Hastalığı", "Patojen Etken", "Vektör Artropod", "Tipik Klinik Belirteç"],
                [
                    [
                        "Akdeniz Benekli Ateşi",
                        "Rickettsia conorii",
                        {"text": "Kahverengi köpek kenesi (Rhipicephalus)", "isMasked": True, "hint": "Köpeklerde yaşayan yaygın kene türü"},
                        "Tache Noire (kara leke), avuç içi-ayak tabanı döküntüsü"
                    ],
                    ["Epidemik Tifüs", "Rickettsia prowazekii", "İnsan vücut biti (Pediculus humanus)", "Gövdeden başlayan döküntü, Brill-Zinsser nüksü"],
                    ["Endemik (Murin) Tifüs", "Rickettsia typhi", "Sıçan piresi (Xenopsylla cheopis)", "Kemirici rezervuarlı hafif seyirli tifüs"],
                    ["Kayalık Dağlar Ateşi", "Rickettsia rickettsii", "Dermacentor cinsi sert keneler", "Bilek ve ayak bileğinden merkeze yayılan peteşi"]
                ]
            ),
            make_micro_quiz(
                "Türkiye'de özellikle yaz aylarında köpek teması ve kene tutunması sonrası yüksek ateş, avuç içlerini tutan döküntü ve kene ısırık yerinde 'tache noire (kara leke)' saptanan hastada en olası etken hangisidir?",
                {
                    "A": "Rickettsia conorii",
                    "B": "Rickettsia prowazekii",
                    "C": "Treponema pallidum",
                    "D": "Chlamydia trachomatis",
                    "E": "Mycoplasma pneumoniae"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Rickettsia conorii Akdeniz benekli ateşinin etkenidir; kene vektörü ve tache noire patognomoniktir.",
                    "B": "B seçeneği bit ile bulaşan epidemik tifüs etkenidir, tache noire yapmaz.",
                    "C": "C seçeneği sifilis etkenidir.",
                    "D": "D seçeneği klamidya etkenidir.",
                    "E": "E seçeneği mikoplazma atipik pnömoni etkenidir."
                }
            )
        ]
    })

    # Slayt 29: [TEKRAR SAYFASI - CHECKPOINT 3]
    slides.append({
        "id": "k1-21-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Tipik ve Atipik Bakteriler",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 29,
        "narrative": (
            "Bu üçüncü checkpoint sayfasında bakterilerin prokaryotik mimarisini, "
            "Gram-pozitif ve Gram-negatif hücre duvarı farklarını (peptidoglikan vs LPS Lipid A), "
            "hücre duvarı olmayan mikoplazmaların beta-laktam direncini ve "
            "enerji paraziti klamidyalar ile endotel tropizmli riketsiyaları "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp3-1",
                "Gram-negatif bakteri hücre duvarındaki endotoksin hangi tabakada yer alır ve biyokimyasal toksik kısmı nedir?",
                "Dış membranın dış yaprağında bulunan Lipopolisakkarit (LPS) molekülüdür; toksik ve şok tetikleyici kısmı Lipid A bileşenidir.",
                "Gram-negatif bakteriyel çeper amfifilik yapısının pirojen ucu",
                "Bakteri Hücre Duvarı"
            ),
            make_flashcard(
                "fc-k1-21-cp3-2",
                "Mikoplazmaların hücre duvarı taşımaması hangi iki kritik laboratuvar ve farmakolojik sonuca yol açar?",
                "Gram boyama ile mikroskopta boyanamaz/görülemezler ve hücre duvarı sentezini hedefleyen tüm beta-laktam antibiyotiklere (penisilin, sefalosporin) intrensek dirençlidirler.",
                "Peptidoglikan kılıfın eksikliğinin optik inceleme ve tedaviye yansıması",
                "Atipik Bakteriyoloji"
            ),
            make_flashcard(
                "fc-k1-21-cp3-3",
                "Akdeniz benekli ateşinin etkeni, vektörü ve kene ısırık yerindeki patognomonik lezyonun adı nedir?",
                "Etken Rickettsia conorii, vektör kahverengi köpek kenesi (Rhipicephalus sanguineus), lezyon ise nekrotik siyah kabuklu Tache Noire'dır (Kara Leke).",
                "Akdeniz benekli hummasında görülen koyu renkli primer eskar",
                "Vektörel Bakteriyoloji"
            )
        ]
    })

    # Slayt 30: Spiroketler ve Bakteriyoloji Bölüm Özeti
    slides.append({
        "id": "k1-21-s30",
        "title": "Spiroketler ve Bakteriyoloji Özeti: Ökaryotlara Geçiş",
        "section": "Tipik ve Atipik Bakteriler",
        "slideNumber": 30,
        "narrative": (
            "Bakteriler alemini tamamlarken aksiyel flamanlarıyla dalgalı burgu hareketi yapan **spiroketleri** incelemek şarttır: "
            "1. **Treponema pallidum:** Cinsel yolla bulaşan **Sifilis (Frengi)** etkenidir. Primer dönemde ağrısız sert şankr, "
            "sekonder dönemde avuç içi/ayak tabanında makülopapüler döküntüler ve kondiloma lata, tersiyer dönemde gomlar ve nörosifilis yapar. "
            "Işık mikroskobunda görülemez, karanlık saha mikroskopisi ile incelenir. "
            "2. **Borrelia burgdorferi:** İxodes keneleriyle bulaşan **Lyme hastalığı** etkenidir; hedef tahtası şeklinde eritema migrans döküntüsü, artrit ve fasiyal paralizi yapar. "
            "3. **Leptospira interrogans:** Kemirici idrarıyla kirlenmiş sulardan derideki çiziklerden bulaşan **Leptospiroz (Weil hastalığı)** etkenidir; "
            "sarılık, böbrek yetmezliği ve kanamalarla seyreder. "
            "Özetle; prokaryotik bakteriler hücresel duvarları, virülans faktörleri ve metabolik çeşitlilikleriyle insan enfeksiyonlarının ana gövdesini oluşturur. "
            "Dördüncü bölümümüzde çekirdeği ve zarlı organelleri olan ökaryotik patojenler alemini; yani **mantarlar ve parazitleri** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Ixodes cinsi sert kenelerin ısırmasıyla bulaşan ve hedef tahtası benzeri eritema migrans lezyonuyla başlayan hastalık Lyme hastalığı tablosudur.",
                "Lyme hastalığı",
                "Borrelia burgdorferi etkenli kene kaynaklı spiroket patolojisi"
            ),
            make_table(
                ["Spiroket Türü", "Bulaşma Yolu / Vektörü", "Karakteristik Klinik Bulgular"],
                [
                    ["Treponema pallidum", "Cinsel temas ve transplasental", "Ağrısız sert şankr, kondiloma lata, tabes dorsalis"],
                    [
                        "Borrelia burgdorferi",
                        {"text": "İxodes cinsi sert keneler", "isMasked": True, "hint": "Geyik ve kemiricilerde yaşayan kene"},
                        "Eritema migrans (boğa gözü döküntü), gezici artrit, Bell felci"
                    ],
                    ["Leptospira interrogans", "Kemirici idrarı ile kontamine sular", "Weil sendromu (sarılık, nefrit, konjonktival süfüzyon)"]
                ]
            ),
            make_micro_quiz(
                "Spiroketler sınıfında yer alan Treponema pallidum etkeninin mikroskobik incelenmesinde ışık mikroskobu yerine tercih edilen özel mikroskopi tekniği hangisidir?",
                {
                    "A": "Elektron mikroskopisi",
                    "B": "Karanlık saha mikroskopisi",
                    "C": "Faz kontrast mikroskopisi",
                    "D": "Polarizasyon mikroskopisi",
                    "E": "Floresan mikroskopisi"
                },
                "B",
                {
                    "A": "A seçeneği virüsler için kullanılır, rutin şankr tanısında yeri yoktur.",
                    "B": "B seçeneği doğrudur: Canlı şankr eksüdasında hareketli spiroketleri görmek için karanlık saha mikroskopisi altın standart yöntemdir.",
                    "C": "C seçeneği hücre biyolojisinde kullanılır.",
                    "D": "D seçeneği amiloid ve kristaller için kullanılır.",
                    "E": "E seçeneği florokrom boyalar gerektirir."
                }
            )
        ]
    })

    return slides
