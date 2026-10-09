"""
Akut Enflamasyon (Ders 9) - Bölüm 3: PAMPs, DAMPs, TLR ve İnflamazom Biyolojisi
Slayt 21 - 30 (Checkpoint 3: Slayt 29)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "slideNumber": 21,
        "title": "Tehlike Sinyallerinin Sınıflandırılması: PAMPs ve DAMPs",
        "subtitle": "Eksojen mikrobiyal istilacılar ile endojen hücresel hasar moleküllerinin ayrımı",
        "badge": "İmmün Tanıma",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Enflamasyonun başlayabilmesi için vücudun doku bütünlüğünün bozulduğunu veya yabancı bir mikroorganizmanın "
            "içeri sızdığını anında fark etmesi gerekir. İmmün sistem bu farkındalığı iki büyük tehlike sinyali sınıfı "
            "aracılığıyla sağlar:\n\n"
            "1. **PAMPs (Pathogen-Associated Molecular Patterns):** Mikropların yaşaması için zorunlu olan ve insanda "
            "asla bulunmayan korunmuş moleküler yapılardır (örneğin Gram-negatif bakteri lipopolisakariti [LPS], "
            "bakteriyel peptidoglikan, viral çift zincirli RNA ve metillenmemiş CpG DNA dizileri).\n\n"
            "2. **DAMPs (Damage-Associated Molecular Patterns / Alarminler):** Hücreler nekroza gittiğinde, yandığında veya "
            "mekanik olarak parçalandığında sitoplazma ve çekirdekten dışarı saçılan endojen moleküllerdir "
            "(örneğin hücre dışı ATP, ürik asit kristalleri, HMGB1 ve nükleer histonlar)."
        ),
        "medicalTerms": [
            {"term": "PAMPs", "explanation": "Patojen mikroorganizmaların yüzeyinde veya genomunda bulunan, konak hücrelerinde bulunmayan evrensel mikrobiyal yapılardır."},
            {"term": "DAMPs (Alarmin)", "explanation": "Hücre nekrozu veya ağır hücresel stres sonucu ekstrasellüler alana dökülen endojen alarm molekülleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] PAMPs mikrobiyal enfeksiyonları, DAMPs ise steril doku hasarını ve nekrozu gösterir.",
            "📌 [SINAV SPOTU] Apoptozda hücre zarı sağlam kaldığı için DAMPs ortama saçılmaz; bu yüzden apoptoz enflamasyon yapmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "PAMP Kaynağı", "desc": "Bakteri, virüs ve mantarların evrensel yapı taşları.", "isKey": True},
                {"title": "DAMP Kaynağı", "desc": "Nekrotik insan hücresinden ortama sızan ATP ve ürik asit.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Tehlike Sinyali Grubu", "Temel Biyolojik Kaynağı", "Tipik Moleküler Örnekler"],
                [
                    [("PAMPs (Patojen İlişkili)", False, ""), ("Bakteri, Virüs, Mantar ve Parazitler", False, ""), ("LPS (Endotoksin), Peptidoglikan, Çift zincirli viral RNA", True, "Mikroorganizmalara özgü yabancı yapılar")],
                    [("DAMPs (Hasar İlişkili)", False, ""), ("Nekroza uğrayan konak hücreleri", False, ""), ("Hücre dışı ATP, Ürik asit kristalleri, HMGB1 proteini", True, "Steril doku ölümünde saçılan endojen alarminler")]
                ]
            ),
            make_cloze(
                "Nekroza uğrayan hücrelerin parçalanmasıyla ekstrasellüler ortama dökülen ve steril yangıyı başlatan moleküllere DAMPs adı verilir.",
                "DAMPs",
                "Damage-Associated Molecular Patterns kavramının uluslararası kabul görmüş kısaltması"
            )
        ]
    })

    # Slide 22
    slides.append({
        "slideNumber": 22,
        "title": "Toll-Like Reseptörler (TLR): Hücresel Sınır Bekçileri",
        "subtitle": "Plazma membranı ve endozomal kompartımanlarda nöbet tutan transmembran sensörler",
        "badge": "Reseptör Biyolojisi",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Konağın en iyi karakterize edilmiş örüntü tanıma reseptörleri **Toll-Like Reseptörler (TLR)** ailesidir. "
            "İnsanda 10 farklı fonksiyonel TLR tanımlanmıştır ve hücresel lokalizasyonlarına göre ikiye ayrılırlar:\n\n"
            "- **Plazma Membranı TLR'leri (Dış Tehditler):** Hücre yüzeyinde yer alarak ekstrasellüler mikropların "
            "yüzey moleküllerini tanırlar.\n"
            "  * **TLR4:** Gram-negatif bakterilerin lipopolisakaritini (LPS / Endotoksin) tanır (CD14 ve MD2 ile birlikte).\n"
            "  * **TLR2:** Gram-pozitif bakteri peptidoglikanlarını ve mikobakteriyel lipoarabinomannan'ı tanır.\n"
            "  * **TLR5:** Bakteriyel kamçı proteini olan flagellin'i tanır.\n\n"
            "- **Endozomal TLR'ler (İç Tehditler):** Fago-endozomal veziküllerin lümenine bakarak yutulan virüs ve "
            "bakterilerin nükleik asitlerini saptarlar.\n"
            "  * **TLR3:** Viral çift zincirli RNA (dsRNA).\n"
            "  * **TLR7 ve TLR8:** Viral tek zincirli RNA (ssRNA).\n"
            "  * **TLR9:** Metillenmemiş mikrobiyal CpG DNA motifleri."
        ),
        "medicalTerms": [
            {"term": "TLR4", "explanation": "Gram-negatif bakteri endotoksini olan lipopolisakariti (LPS) tanıyan ve septik şok patogenezinde kritik olan yüzey reseptörüdür."},
            {"term": "Endozomal Reseptör", "explanation": "Hücre zarı yerine fagositozla içeri alınan veziküllerin iç zarında yerleşmiş nükleik asit sensörleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gram-negatif bakteri LPS'sini tanıyan anahtar reseptör TLR4'tür.",
            "📌 [SINAV SPOTU] TLR3, 7, 8 ve 9 endozomal zarlarda yerleşiktir ve mikrobiyal nükleik asitleri tanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yüzey TLR'leri", "desc": "TLR1, 2, 4, 5, 6 bakteri çeperini ve flagellayı tanır.", "isKey": True},
                {"title": "Endozom TLR'leri", "desc": "TLR3, 7, 8, 9 viral genetik materyali tanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Reseptör", "Hücre İçi Lokalizasyonu", "Spesifik Olarak Tanıdığı PAMP Molekülü"],
                [
                    [("TLR4", False, ""), ("Plazma Membranı", False, ""), ("Gram-negatif bakteri lipopolisakariti (LPS / Endotoksin)", True, "Septik şokta kilit rol oynayan yüzeyel ligand")],
                    [("TLR2", False, ""), ("Plazma Membranı", False, ""), ("Gram-pozitif peptidoglikan ve teikoik asit", True, "Gram-pozitif bakteri duvarının kalın katmanı")],
                    [("TLR3", False, ""), ("Endozomal Membran", False, ""), ("Viral çift zincirli RNA (dsRNA)", True, "Virüs replikasyon ara ürünü olan nükleik asit")],
                    [("TLR9", False, ""), ("Endozomal Membran", False, ""), ("Metillenmemiş mikrobiyal CpG DNA motifleri", True, "Bakteri genomunda bol bulunan metilsiz dinükleotid")]
                ]
            ),
            make_cloze(
                "Gram-negatif bakterilerin dış zarında bulunan lipopolisakariti (LPS) tanıyan temel Toll-like reseptör TLR4 reseptörüdür.",
                "TLR4",
                "Endotoksin uyarımını MyD88 yolağına aktaran plazma zarı reseptör numarası"
            )
        ]
    })

    # Slide 23
    slides.append({
        "slideNumber": 23,
        "title": "TLR Sinyal İletimi: MyD88 ve NF-kappaB Aktivasyonu",
        "subtitle": "Reseptör uyarımından nükleer transkripsiyona ve sitokin fırtınasına giden moleküler otoyol",
        "badge": "Sinyal İletimi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Bir mikrop TLR reseptörüne bağlandığında hücre içinde muazzam bir sinyal kaskadı başlar:\n\n"
            "1. TLR'nin sitoplazmik TIR (Toll/IL-1 Reseptör) domeyni, **MyD88** adaptör proteinini kendine çeker.\n"
            "2. MyD88, IRAK kinazları ve TRAF6 üzerinden **IκB Kinaz (IKK)** kompleksini aktive eder.\n"
            "3. Normalde sitozolde IκB (İnhibitör kappa B) proteini tarafından kelepçeli tutulan **NF-κB** transkripsiyon faktörü, "
            "IκB'nin fosforillenip proteazomda yıkılmasıyla serbest kalır.\n"
            "4. Çekirdeğe göç eden aktif NF-κB; **TNF-α, IL-1β, IL-6, kemokinler (IL-8)** ve endotelyal adezyon "
            "moleküllerinin genlerini güçlü bir şekilde transkribe ettirir.\n\n"
            "> Alternatif yol: TLR3 ve TLR4 **TRIF** adaptörünü kullanarak **IRF (İnterferon Regülatuvar Faktör)** faktörlerini "
            "aktive eder ve antiviral Tip I İnterferon (IFN-α/β) üretimini sağlar."
        ),
        "medicalTerms": [
            {"term": "NF-κB", "explanation": "İnflamatuvar gen ekspresyonunun merkezi yöneticisi olan ve IκB tarafından inhibe edilen anahtar transkripsiyon faktörüdür."},
            {"term": "MyD88", "explanation": "TLR3 hariç neredeyse tüm TLR'lerin sinyalini IKK kompleksine bağlayan kritik sitozolik adaptör proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] TLR sinyalinin nihai hedefi NF-kappaB'yi serbestleştirerek TNF, IL-1 ve sitokin sentezini başlatmaktır.",
            "📌 [SINAV SPOTU] TLR3 sinyali MyD88 kullanmaz; sadece TRIF adaptörüyle antiviral Tip I İnterferon üretir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "MyD88 Ekseni", "desc": "TIR -> MyD88 -> IKK -> NF-κB aktivasyonu.", "isKey": True},
                {"title": "Gen İndüksiyonu", "desc": "TNF, IL-1 ve kemokin transkripsiyonu tavan yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "TLR4'ten NF-kappaB Aktivasyonuna Uzanan Kaskad",
                [
                    "1. Gram-negatif bakteri LPS'si hücre yüzeyindeki TLR4/MD2 kompleksine bağlanır",
                    "2. TLR4 sitoplazmik domeyni MyD88 adaptör proteinini bağlayarak oligomerleşir",
                    "3. Aktive olan IKK kompleksi NF-kappaB'yi tutan inhibitör IkB proteinini fosforiller",
                    "4. IkB ubikitinlenip yıkılınca serbest kalan NF-kappaB çekirdeğe girerek TNF ve IL-1 genlerini açar"
                ]
            ),
            make_active_recall(
                "İstirahat halindeki bir makrofajda NF-kappaB transkripsiyon faktörünün çekirdeğe girmesini engelleyen sitoplazmik inhibitör protein hangisidir?",
                "IκB (İnhibitör kappa B) proteinidir; IKK tarafından fosforillendiğinde parçalanır ve NF-κB çekirdeğe geçer."
            )
        ]
    })

    # Slide 24
    slides.append({
        "slideNumber": 24,
        "title": "NLR Reseptörleri ve İnflamazom Kompleksinin Mimarisi",
        "subtitle": "Sitozolik tehlike sensörü NLRP3, adaptör ASC ve efektör prokaspaz-1 üçlüsü",
        "badge": "İnflamazom",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre zarını aşarak sitoplazmaya sızan tehlikeleri yakalamak için sitozolik sensörler görev yapar. "
            "Bunların en önemlisi **NOD-Like Reseptörler (NLR)** ailesidir. Bu ailenin yıldızı olan **NLRP3**, tehlike "
            "algıladığında dev bir sitoplazmik protein fabrikası olan **İnflamazom** kompleksini kurar.\n\n"
            "İnflamazom üç ana bileşenden oluşur:\n"
            "1. **Sensör:** NLRP3 proteini (tehlikeyi algılar ve oligomerleşir).\n"
            "2. **Adaptör:** ASC proteini (sensör ile enzimi birbirine kilitler).\n"
            "3. **Efektör Enzim:** **Prokaspaz-1** (inaktif zimojen haldeki kaspaz).\n\n"
            "> İnflamazom bir araya geldiğinde prokaspaz-1 oto-katalitik olarak parçalanır ve aktif **Kaspaz-1** enzimine dönüşür."
        ),
        "medicalTerms": [
            {"term": "İnflamazom", "explanation": "NLRP3, ASC ve Prokaspaz-1'in bir araya gelmesiyle oluşan ve aktif Kaspaz-1 üreten multiprotein oligomerik komplekstir."},
            {"term": "Kaspaz-1 (ICE)", "explanation": "Pro-IL-1beta ve pro-IL-18'i keserek aktif olgun sitokinlere dönüştüren sistein proteazdır (İnterlökin-1 Dönüştürücü Enzim)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İnflamazomun efektör enzimi KASPAZ-1'dir (eski adıyla ICE).",
            "📌 [SINAV SPOTU] İnflamazomun temel görevi inaktif pro-IL-1beta'yı aktif IL-1beta'ya çevirmektir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Üçlü Yapı", "desc": "NLRP3 (sensör) + ASC (köprü) + Prokaspaz-1 (enzim).", "isKey": True},
                {"title": "Aktif Enzim", "desc": "Kaspaz-1 olgunlaşarak sitokin kesme görevini üstlenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "İnflamazom kompleksinin aktive ettiği ve pro-IL-1beta'yı aktif formuna kesen temel sistein proteaz enzimi kaspaz-1 enzimidir.",
                "kaspaz-1",
                "İnterleukin-1 converting enzyme (ICE) olarak da adlandırılan efektör kaspaz numarası"
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi NLRP3 inflamazom kompleksinin doğrudan hücresel çıktısı ve enzimatik sonucudur?",
                {
                    "A": "Aktif Kaspaz-3 üretimi ve apoptoz indüksiyonu",
                    "B": "Prokaspaz-1'in aktif Kaspaz-1'e dönüştürülmesi ve pro-IL-1β'nın aktif IL-1β olarak salınması",
                    "C": "TNF-alfa reseptörlerinin endositozla parçalanması",
                    "D": "Histaminin mast hücre granüllerinden boşaltılması",
                    "E": "Kompleman C3 proteininin C3b'ye parçalanması"
                },
                "B",
                {
                    "A": "Kaspaz-3 klasik apoptoz enzimidir, inflamazom kaspaz-1'i aktive eder.",
                    "B": "Doğru cevap B'dir: İnflamazom Prokaspaz-1'i keser; aktif Kaspaz-1 de pro-IL-1β ve pro-IL-18'i olgun sitokine dönüştürür.",
                    "C": "TNF reseptör regülasyonu ile doğrudan ilgisi yoktur.",
                    "D": "Histamin degranülasyonu IgE veya C3a/C5a ile tetiklenir.",
                    "E": "C3 parçalanması kompleman konvertazlarıyla olur."
                }
            )
        ]
    })

    # Slide 25
    slides.append({
        "slideNumber": 25,
        "title": "İnflamazomun İki Aşamalı Çalışma Mekanizması",
        "subtitle": "Sinyal 1 (Priming: NF-kappaB) ve Sinyal 2 (Tetikleme: Potasyum çıkışı ve ROS)",
        "badge": "Aktivasyon Modeli",
        "badgeColor": "orange",
        "synthesisNarrative": (
            "Hücrenin kontrolsüzce IL-1β üretip ölümcül sitokin fırtınasına girmemesi için inflamazom aktivasyonu "
            "**iki aşamalı emniyet kilidine** bağlanmıştır:\n\n"
            "- **Sinyal 1 (Priming / Hazırlık):** TLR veya TNF uyarımı ile NF-κB aktive olur. NF-κB çekirdekte "
            "inaktif **pro-IL-1β** ve **NLRP3** genlerini transkribe ettirir. Hücrede hammadde birikir ancak henüz kesilip "
            "salınamaz (silah doldurulur ama tetiğe basılmaz).\n\n"
            "- **Sinyal 2 (Triggering / Tetikleme):** Çeşitli hücresel stres faktörleri inflamazom montajını başlatır:\n"
            "  * Hücre dışı yüksek ATP (hasarlı hücrelerden) -> P2X7 reseptörü uyarımı -> **Hücreden masif Potasyum (K+) çıkışı**.\n"
            "  * Fagositozla yutulan silika veya kristallerin lizozomu patlatması.\n"
            "  * Mitokondriyal ROS üretimi.\n\n"
            "> Bu sinyaller NLRP3'ü oligomerleştirir, Kaspaz-1 devreye girer ve aktif IL-1β dışarı fışkırır."
        ),
        "medicalTerms": [
            {"term": "Priming Sinyali", "explanation": "TLR aracılığıyla NF-kappaB'nin uyarılıp pro-IL-1beta ve NLRP3 proteinlerinin sentezletilmesidir."},
            {"term": "Potasyum Çıkışı (K+ Efflux)", "explanation": "İntrasellüler potasyum konsantrasyonunun düşmesinin NLRP3 inflamazom montajını tetikleyen en evrensel uyaran olmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sinyal 1 (Priming) hammaddeyi (pro-IL-1beta) üretir; Sinyal 2 (Tetikleme) Kaspaz-1'i kurup kesimi yapar.",
            "📌 [SINAV SPOTU] İntrasellüler Potasyum (K+) düşüşü inflamazom montajının en yaygın ortak tetikleyicisidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sinyal 1: Priming", "desc": "NF-κB ile pro-IL-1β ve NLRP3 transkripsiyonu.", "isKey": True},
                {"title": "Sinyal 2: Tetik", "desc": "K+ çıkışı, kristaller ve ROS ile montaj ve kesim.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "İnflamazom Sinyal 1 (Priming) vs Sinyal 2 (Assembly)",
                "Sinyal 1 (Priming Aşaması)",
                "TLR uyarımıyla pro-IL-1β ve NLRP3 proteinleri sitoplazmada sentezlenir; ancak Kaspaz-1 inaktiftir ve sitokin salgılanamaz.",
                "Sinyal 2 (Assembly Aşaması)",
                "K+ çıkışı veya kristallerle NLRP3, ASC ve Prokaspaz-1 birleşir; Kaspaz-1 kesimi yapar ve aktif IL-1β dokuya saçılır."
            ),
            make_active_recall(
                "Makrofajlarda inflamazomun Sinyal 2 (tetikleme) aşamasında NLRP3 proteinlerinin oligomerleşmesini tetikleyen en yaygın iyonik değişiklik nedir?",
                "Plazma membranındaki kanallardan (P2X7 gibi) hücre dışına masif Potasyum (K+) çıkışı (K+ efflux) ve intrasellüler potasyum seviyesinin düşmesidir."
            )
        ]
    })

    # Slide 26
    slides.append({
        "slideNumber": 26,
        "title": "İnflamazom İlişkili Klinik Hastalıklar: Gut, Ateroskleroz ve Diyabet",
        "subtitle": "Ürat kristalleri, kolesterol kristalleri ve amiloidin steril yangıyı alevlendirmesi",
        "badge": "Metabolik Yangı",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "İnflamazom sadece enfeksiyonlarda değil, günümüzün en yaygın metabolik ve steril hastalıklarının patogenezinde "
            "baş aktördür:\n\n"
            "1. **Gut Artriti:** Kanda yükselen ürik asit eklemlerde **monosodyum ürat kristalleri** olarak çöker. "
            "Eklemdeki makrofajlar bu sivri kristalleri fagositozla yutar; kristaller fago-lizozomu delerek sitoplazmaya "
            "dökülür. NLRP3 inflamazomu aşırı aktive olur; masif IL-1β salınımı eklemde kızılca kıyamet koparır "
            "(dayanılmaz artrit ağrısı).\n\n"
            "2. **Ateroskleroz:** Damar duvarında biriken **kolesterol kristalleri** inflamazomu tetikleyerek plak enflamasyonunu besler.\n\n"
            "3. **Tip 2 Diyabet:** Serbest yağ asitleri ve adacık amiloid polipeptidi (IAPP) beta hücrelerinde inflamazomu uyararak "
            "insülin salgılayan hücreleri tüketir."
        ),
        "medicalTerms": [
            {"term": "Monosodyum Ürat", "explanation": "Gut hastalığında eklem ve periartiküler dokularda çöken ve inflamazomu güçlü şekilde tetikleyen iğnemsi kristallerdir."},
            {"term": "Anakinra", "explanation": "İnflamazom kaynaklı aşırı IL-1 aktivitesini durdurmak için kullanılan rekombinant IL-1 reseptör antagonistidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gut hastalığında akut artriti başlatan anahtar moleküler kompleks NLRP3 İNFLAMAZOMU'dur.",
            "📌 [SINAV SPOTU] Aterosklerozda kolesterol kristalleri, gutta ürat kristalleri inflamazom aktivatörüdür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Gut Mekanizması", "desc": "Ürat kristalleri -> Lizozom yırtılması -> NLRP3 -> IL-1β.", "isKey": True},
                {"title": "Damar Sertliği", "desc": "Kolesterol kristalleri ile makrofaj uyarımı ve plak kararsızlığı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Klinik Hastalık", "İnflamazomu Tetikleyen Kristal / Partikül", "Nihai Patolojik Doku Yanıtı"],
                [
                    [("Akut Gut Artriti", False, ""), ("Monosodyum ürat (MSÜ) kristalleri", False, ""), ("Masif nötrofil infiltrasyonu ve şiddetli eklem ağrısı", True, "Birinci metatarsofalengeal eklemde podagra")],
                    [("Ateroskleroz", False, ""), ("Ekstrasellüler kolesterol kristalleri", False, ""), ("Damar intimasında köpük hücre yangısı ve plak çatlaması", True, "Lümen obstrüksiyonu ve tromboz riski")],
                    [("Silikozis / Asbestozis", False, ""), ("Solunan inorganik silika ve asbest lifleri", False, ""), ("Alveoler makrofaj ölümü ve ilerleyici akciğer fibrozisi", True, "Mesleki interstisyel akciğer hastalığı")]
                ]
            ),
            make_cloze(
                "Gut artritinde eklem içine çöken monosodyum ürat kristalleri makrofajlarda NLRP3 inflamazom kompleksini aktive ederek akut yangıyı başlatır.",
                "NLRP3",
                "Gut artritinde Kaspaz-1 aktivasyonunu yöneten NLR sensör ailesi üyesi"
            )
        ]
    })

    # Slide 27
    slides.append({
        "slideNumber": 27,
        "title": "Piroptozis: İnflamazom Aracılı Enflamatuvar Hücre İntiharı",
        "subtitle": "Kaspaz-1 aktivasyonu, Gazdermin D gözenekleri ve sitokinlerin patlayarak salınması",
        "badge": "Ölüm Biçimleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İnflamazom sadece IL-1β üretmekle kalmaz; aynı zamanda hücreyi özel ve son derece gürültülü bir programlı "
            "ölüm biçimine sürükler: **Piroptozis** (Pyro = ateş, ptosis = düşüş).\n\n"
            "Mekanizması:\n"
            "1. Aktive olan **Kaspaz-1 (veya kaspaz-4/5/11)**, sitoplazmadaki **Gasdermin D (GSDMD)** proteinini keser.\n"
            "2. Kesilen Gasdermin D'nin N-terminal parçaları plazma zarına göç eder ve oligomerleşerek zarda "
            "**dev porlar (delikler)** açar.\n"
            "3. Bu porlardan hücre içine kontrolsüzce su ve sodyum girer; hücre şişer ve patlar (lizis).\n"
            "4. Açılan porlardan ve hücrenin yırtılmasıyla tüm hücre içi IL-1β, IL-18 ve DAMPs (HMGB1, ATP) etrafa "
            "saçılarak devasa bir yangı fırtınası başlatır.\n\n"
            "> Piroptozis, hücre içinde saklanan mikropların (Salmonella, Shigella) sığınağını yok etmek için evrilmiştir."
        ),
        "medicalTerms": [
            {"term": "Piroptozis", "explanation": "İnflamazom ve kaspaz-1/4/5 aracılığıyla Gasdermin D gözenekleri açılarak hücrenin şişip patlamasıyla karakterize enflamatuvar hücre ölümüdür."},
            {"term": "Gasdermin D (GSDMD)", "explanation": "Kaspaz-1 tarafından kesildiğinde plazma membranında litik delikler oluşturan piroptotik por yapıcı proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Piroptoziste plazma membranını delen anahtar efektör protein GASDERMİN D'dir.",
            "📌 [SINAV SPOTU] Apoptoz sessiz ve anti-enflamatuvardır; piroptozis ise patlamalı ve aşırı pro-enflamatuvardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "GSDMD Delikleri", "desc": "Kaspaz-1 Gasdermin D'yi keser, zarda porlar açılır.", "isKey": True},
                {"title": "Patlayıcı Salınım", "desc": "Hücre lize olur, IL-1 ve DAMP'lar mikroçevreye saçılır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Apoptoz vs Piroptozis Hücre Ölümü",
                "Klasik Apoptoz",
                "Membran bütünlüğü korunur, apoptotik cisimcikler oluşur, makrofajlar sessizce yutar, sıfır enflamasyon.",
                "Piroptozis",
                "Gasdermin D ile zarda dev delikler açılır, hücre şişip patlar, IL-1 ve DAMP'lar saçılarak şiddetli yangı oluşur."
            ),
            make_cloze(
                "Piroptozis sürecinde kaspaz-1 tarafından kesilerek hücre zarında gözenekler açan efektör protein Gasdermin D proteinidir.",
                "Gasdermin D",
                "GSDMD kısaltmasıyla bilinen ve piroptotik membran lizisini gerçekleştiren protein"
            )
        ]
    })

    # Slide 28
    slides.append({
        "slideNumber": 28,
        "title": "Diğer Örüntü Tanıma Reseptörleri: CLR ve RLR Aileleri",
        "subtitle": "Mantar glukanlarını yakalayan C-tipi lektinler ve intrasellüler viral RNA avcısı RIG-I",
        "badge": "Genişletilmiş PRR",
        "badgeColor": "slate",
        "synthesisNarrative": (
            "Konağın gözetleme sistemi TLR ve NLR'lerle sınırlı değildir. Farklı mikrop sınıflarına özelleşmiş "
            "ek PRR aileleri mevcuttur:\n\n"
            "- **C-Tipi Lektin Reseptörleri (CLR / Dectin-1, Dectin-2, Mannoz Reseptörü):**\n"
            "  * Plazma zarında yer alırlar ve kalsiyum bağımlı olarak mikrobiyal karbonhidratları bağlarlar.\n"
            "  * Özellikle **mantar (Candida, Aspergillus)** hücre duvarındaki beta-glukan ve mannan yapılarını tanırlar.\n"
            "  * Eksikliklerinde kronik mukokutanöz kandidiyazis gibi inatçı mantar enfeksiyonları gelişir.\n\n"
            "- **RIG-I Benzeri Reseptörler (RLR / RIG-I, MDA5):**\n"
            "  * Sitozolde serbest yüzen viral RNA sensörleridir.\n"
            "  * Hücre içine girip replike olan RNA virüslerinin 5'-trifosfat uçlu RNA'larını yakalarlar.\n"
            "  * Uyarılmaları güçlü **Tip I İnterferon (IFN-α/β)** sentezini tetikleyerek komşu hücreleri viral enfeksiyona karşı zırhlar."
        ),
        "medicalTerms": [
            {"term": "Dectin-1", "explanation": "Mantar hücre duvarındaki beta-glukanları tanıyan ve antifungal immüniteyi başlatan C-tipi lektin reseptörüdür."},
            {"term": "Tip I İnterferon", "explanation": "Viral enfeksiyonlarda RLR ve TLR3/7 uyarımıyla salınan ve viral replikasyonu durduran sitokinlerdir (IFN-alfa/beta)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mantar hücre duvarı beta-glukanlarını tanıyan PRR ailesi C-Tipi Lektinlerdir (Dectin-1).",
            "📌 [SINAV SPOTU] Sitozolik viral RNA'yı tanıyıp Tip I İnterferon üreten sensörler RIG-I ve MDA5'tir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "C-Tipi Lektinler", "desc": "Mantar karbonhidratlarını (glukan/mannan) tanır.", "isKey": True},
                {"title": "RIG-I Reseptörleri", "desc": "Sitozolik viral RNA'yı tanıyıp interferon salgılatır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["PRR Reseptör Ailesi", "Hücresel Yerleşimi", "Hedef Patojen ve Temel İmmün Çıktı"],
                [
                    [("Toll-Like Reseptörler (TLR)", False, ""), ("Plazma zarı ve Endozomlar", False, ""), ("Bakteri çeperi ve nükleik asitler -> NF-κB ve sitokinler", True, "LPS, flagellin ve nükleik asit uyarımı")],
                    [("NOD-Like Reseptörler (NLR)", False, ""), ("Sitoplazma (Sitozol)", False, ""), ("Kristaller ve DAMPs -> İnflamazom, Kaspaz-1 ve IL-1β", True, "Ürat ve kolesterol kristalleriyle aktivasyon")],
                    [("C-Tipi Lektinler (CLR)", False, ""), ("Plazma zarı", False, ""), ("Mantar hücre duvarı (Beta-glukan) -> Antifungal yangı", True, "Candida ve Aspergillus çeperini tanıma")],
                    [("RIG-I Benzeri (RLR)", False, ""), ("Sitoplazma (Sitozol)", False, ""), ("Viral genomik RNA -> Tip I İnterferon (Antiviral savunma)", True, "Viral replikasyonu durduran kaskad")]
                ]
            ),
            make_cloze(
                "Mantar hücre duvarında bulunan beta-glukan polisakkaritlerini spesifik olarak tanıyan C-tipi lektin reseptörü Dectin-1 reseptörüdür.",
                "Dectin-1",
                "Kandidiyazis savunmasında kilit rol oynayan temel lektin reseptörü"
            )
        ]
    })

    # Slide 29 (CHECKPOINT 3)
    slides.append({
        "slideNumber": 29,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Tehlike Algılama ve İnflamazom Mimarisi",
        "subtitle": "Bölüm 3 PAMPs, DAMPs, TLR4/MyD88/NF-kappaB ve NLRP3/Kaspaz-1/IL-1 Sentezi",
        "badge": "Checkpoint 3",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "synthesisNarrative": (
            "Üçüncü kontrol noktasında tehlike algılama biyolojisini kilit taşlarıyla sabitliyoruz:\n\n"
            "1. **Tehlike Sinyalleri:** PAMPs mikrobiyal yapıları (LPS, peptidoglikan, viral RNA), DAMPs nekrotik "
            "hücre artıklarını (ekstrasellüler ATP, ürik asit) ifade eder.\n"
            "2. **TLR Mimarisi:** Membranda TLR4 (LPS), TLR2 (Gram-pozitif), TLR5 (flagellin); endozomda TLR3 (dsRNA), "
            "TLR7/8 (ssRNA), TLR9 (CpG DNA) görev yapar.\n"
            "3. **TLR Sinyali:** MyD88 adaptörü -> IKK -> IκB yıkımı -> **NF-κB nükleer translokasyonu** -> TNF ve IL-1 transkripsiyonu.\n"
            "4. **İnflamazom:** NLRP3 + ASC + Prokaspaz-1. Sinyal 1 (NF-κB ile priming) + Sinyal 2 (K+ çıkışı ile tetikleme). "
            "Efektör **Kaspaz-1**'dir; pro-IL-1β'yı keser.\n"
            "5. **Piroptozis ve Hastalık:** Kaspaz-1 **Gasdermin D**'yi keserek zarda delikler açar; hücre şişip patlar. "
            "Gut hastalığında monosodyum ürat, aterosklerozda kolesterol kristalleri inflamazomu alevlendirir."
        ),
        "medicalTerms": [
            {"term": "İnterlökin-1beta (IL-1beta)", "explanation": "İnflamazom aracılığıyla üretilen, lökosit alımını ve hipotalamik ateşi yöneten güçlü pro-enflamatuvar sitokindir."},
            {"term": "Steril Yangı", "explanation": "Mikroorganizma olmaksızın kristaller, nekroz veya mekanik hasarla inflamazomun tetiklendiği enflamasyondur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] TLR sinyali NF-kappaB'yi aktive eder; İnflamazom sinyali Kaspaz-1'i aktive eder.",
            "📌 [SINAV SPOTU] Piroptotik porları açan protein Gasdermin D'dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "TLR Çıktısı", "desc": "TNF-α, IL-1β (pro-form) ve kemokin sentezi.", "isKey": True},
                {"title": "İnflamazom Çıktısı", "desc": "Kaspaz-1 ile aktif IL-1β salınımı ve piroptozis.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "İnflamazom aracılı IL-1beta salınımında rol oynayan iki emniyet sinyali (Sinyal 1 ve Sinyal 2) arasındaki iş bölümü nasıldır?",
                "Sinyal 1 (Priming - TLR/NF-κB) inaktif pro-IL-1β ve NLRP3 proteinlerinin genetik transkripsiyonunu ve sentezini sağlar; Sinyal 2 (Tetikleme - K+ çıkışı/kristaller) ise inflamazom kompleksini kurarak Prokaspaz-1'i aktif Kaspaz-1'e dönüştürür ve pro-IL-1β'yı kesip aktif forma sokar."
            ),
            make_micro_quiz(
                "Akut gut artritinde eklem içine çöken monosodyum ürat kristallerinin şiddetli ağrı ve nötrofilik yangı oluşturmasını sağlayan kilit enzim aşağıdakilerden hangisidir?",
                {
                    "A": "Kaspaz-1 (İnflamazom ilişkili sistein proteaz)",
                    "B": "Kaspaz-8 (Ekstrensek ölüm reseptörü kaspazı)",
                    "C": "Kollajenaz (MMP-1)",
                    "D": "Siklooksijenaz-1 (COX-1)",
                    "E": "Alkalen fosfataz"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Ürat kristalleri NLRP3 inflamazomunu aktive eder; Kaspaz-1 pro-IL-1β'yı aktif IL-1β'ya keserek masif yangıyı başlatır.",
                    "B": "Kaspaz-8 ölüm reseptör apoptozundadır.",
                    "C": "Kollajenaz matriks yıkar.",
                    "D": "COX-1 prostaglandin üretir, kristali doğrudan algılamaz.",
                    "E": "Alkalen fosfataz kemik/karaciğer enzimidir."
                }
            ),
            make_cloze(
                "Gram-negatif sepsis ve septik şok patogenezinde bakteriyel lipopolisakariti (LPS) bağlayarak inflamatuvar kaskadı başlatan yüzey reseptörü TLR4 reseptörüdür.",
                "TLR4",
                "Endotoksin tanıyan birinci basamak Toll-like reseptör numarası"
            )
        ]
    })

    # Slide 30
    slides.append({
        "slideNumber": 30,
        "title": "Bölüm 3 Entegrasyonu: İnflamazomun Farmakolojik Hedeflenmesi",
        "subtitle": "Kolkisin, Anakinra ve MCC950 ile IL-1 yolağının kilitlenmesi",
        "badge": "İlaç Hedefleri",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "İnflamazom biyolojisinin aydınlatılması klinik tıpta devrim niteliğinde tedavi stratejileri doğurmuştur:\n\n"
            "- **Kolkisin:** Yüzyıllardır gut tedavisinde kullanılan bu antik ilaç, mikrotübül polimerizasyonunu "
            "engelleyerek NLRP3 inflamazomunun hücre içinde bir araya gelmesini (montajını) ve lökosit göçünü felç eder.\n"
            "- **Anakinra (IL-1 Reseptör Antagonisti):** Rekombinant IL-1Ra proteini olup IL-1'in reseptörüne bağlanmasını "
            "bloke eder; gut krizlerinde ve Ailesel Akdeniz Ateşi (FMF) gibi otoinflamatuvar sendromlarda hayat kurtarır.\n"
            "- **Kanakinumab (Anti-IL-1β Monoklonal Antikoru):** CANTOS çalışmasında aterosklerozlu hastalarda lipitleri "
            "değiştirmeksizin sadece IL-1β'yı nötralize ederek miyokard enfarktüsü ve kardiyovasküler ölüm riskini azaltmıştır."
        ),
        "medicalTerms": [
            {"term": "Kolkisin", "explanation": "Tubuline bağlanarak mikrotübül montajını ve dolayısıyla inflamazom kurulumu ile lökosit kemotaksisini engelleyen alkaloiddir."},
            {"term": "Kanakinumab", "explanation": "Doğrudan IL-1beta sitokinini nötralize eden insan monoklonal antikorudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kolkisin mikrotübül polimerizasyonunu bozarak inflamazom montajını ve nötrofil göçünü engeller.",
            "📌 [SINAV SPOTU] Anakinra IL-1 reseptör antagonisti, Kanakinumab ise IL-1beta nötralizan antikorudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kolkisin Etkisi", "desc": "Mikrotübül blokajı ile inflamazom birleşmesini durdurur.", "isKey": True},
                {"title": "IL-1 Blokajı", "desc": "Anakinra ve Kanakinumab ile steril yangı söndürülür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Akut gut artritinde mikrotübül polimerizasyonunu bozarak inflamazom montajını ve lökosit göçünü engelleyen klasik ilaç Kolkisin ilacıdır.",
                "Kolkisin",
                "Colchicum autumnale bitkisinden elde edilen tarihi antigut alkaloidi"
            ),
            make_active_recall(
                "Kardiyovasküler tıpta dönüm noktası olan CANTOS çalışmasında aterosklerotik olayları azaltmak amacıyla doğrudan hedeflenen pro-enflamatuvar sitokin hangisidir?",
                "İnterlökin-1 beta (IL-1β) sitokinidir; kanakinumab monoklonal antikoru ile hedeflenerek steril damar yangısı baskılanmıştır."
            )
        ]
    })

    return slides
