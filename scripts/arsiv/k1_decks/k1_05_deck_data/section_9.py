"""
Bölüm 9: Hücre Hasarının Biyokimyasal Mekanizmaları - I: DNA, ER ve Kalsiyum
Adımlar: 81 - 90
Checkpoint: Adım 89 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # ADIM 81
    slides.append({
        "slideNumber": 81,
        "title": "DNA Hasarı ve p53: 'Genom Bekçisi'nin İkili Karar Mekanizması",
        "subtitle": "Radyasyon ve kimyasallara karşı hücre döngüsünü durdurma veya apoptoza gönderme dengesi",
        "badge": "p53 Genom Bekçisi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre çekirdeğindeki genetik materyal radyasyon, kemoterapi, oksidatif stres veya spontan replikasyon "
            "hatalarıyla sürekli tehdit altındadır. Bu tehditlere karşı hücrenin en güçlü tümör baskılayıcı kalkanı "
            "'TP53' geni tarafından kodlanan p53 proteinidir.\n\n"
            "Normal koşullarda p53 çok kısa ömürlüdür ve MDM2 tarafından ubikitinlenerek hızla parçalanır. "
            "Ancak DNA'da çift sarmal kırığı oluştuğunda ATM ve ATR kinazları p53'ü fosforiller; p53 parçalanmaktan "
            "kurtulup çekirdekte birikir.\n\n"
            "> [SINAV SPOTU] p53 proteini tıp literatüründe 'Genom Bekçisi' (Guardian of the Genome) olarak bilinir. "
            "Hafif hasarda hücre döngüsünü G1/S sınırında durdurup onarıma izin verir; ağır hasarda ise apoptozu emreder!\n\n"
            "Bu sayede mutasyonlu DNA'nın yavru hücrelere aktarılması kesin olarak engellenir."
        ),
        "medicalTerms": [
            {"term": "p53 Proteini", "explanation": "DNA hasarını algılayıp hücre döngüsünü durduran veya apoptozu tetikleyen ana tümör baskılayıcı molekül."},
            {"term": "Genom Bekçisi", "explanation": "p53'ün genetik bütünlüğü mutasyonlara karşı koruma misyonunu tanımlayan klasik unvan."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] p53 'Genom Bekçisi' olarak görev yapan ana tümör baskılayıcı proteindir.",
            "📌 [SINAV SPOTU] Hafif hasarda hücre döngüsünü durdurup onarıma zaman tanır.",
            "📌 [SINAV SPOTU] Şiddetli onarılamaz hasarda mitokondriyal apoptozu indükler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Genom Bekçisi Rolü", "desc": "Hücre çekirdeğindeki DNA kırıklarını denetleyen santral protein.", "isKey": True},
                {"title": "İkili Karar Kavşağı", "desc": "Tamir edilebilir hasarda duraklama, tamir edilemezse intihar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "DNA hasarı karşısında hücre döngüsünü durduran veya apoptozu tetikleyen genom bekçisi tümör baskılayıcı protein p53 proteinidir.",
                "p53",
                "17. kromozomda kodlanan ana tümör baskılayıcı protein adı"
            ),
            make_active_recall(
                "p53 proteini hafif DNA hasarı ile şiddetli DNA hasarı karşısında sırasıyla nasıl iki farklı karar verir?",
                "Hafif hasarda p21 aracılığıyla hücre döngüsünü G1 evresinde durdurup DNA onarımına izin verir; şiddetli hasarda ise Puma/Bax üzerinden apoptozu tetikler."
            )
        ]
    })

    # ADIM 82
    slides.append({
        "slideNumber": 82,
        "title": "p53'ün Moleküler Yolu: p21 ile Döngü Blokajından BAX ile İnfaza",
        "subtitle": "CDK inhibitörü p21 indüksiyonu ve mitokondriyal apoptozun ateşlenmesi",
        "badge": "p53 Mekanizması",
        "badgeColor": "red",
        "synthesisNarrative": (
            "p53 bir transkripsiyon faktörüdür ve kararlarını hedef genlerin promoterlarına bağlanarak icra eder. "
            "DNA hasarı hafif olduğunda, p53 ilk olarak 'CDKN1A' genini uyararak 'p21' (WAF1/CIP1) proteinini sentezletir.\n\n"
            "p21 güçlü bir Siklin Bağımlı Kinaz (CDK) inhibitörüdür. Siklin D-CDK4/6 kompleksini bloke ederek "
            "Rb proteininin fosforillenmesini önler; böylece hücre döngüsü G1 evresinde kilitlenir. "
            "Hücre GADD45 enzimiyle DNA'yı onarırsa p53 düzeyi düşer ve döngü devam eder.\n\n"
            "> [SINAV SPOTU] Hasar tamir edilemeyecek kadar ağırsa, p53 pro-apoptotik 'BAX', 'Puma' ve 'Noxa' "
            "genlerinin transkripsiyonunu başlatır. Bu proteinler mitokondriyi delerek Sitokrom c salar ve apoptozu tetikler!\n\n"
            "Böylece mutasyonlu hücre sessizce ortadan kaldırılmış olur."
        ),
        "medicalTerms": [
            {"term": "p21 Proteini", "explanation": "p53 tarafından indüklenen, Siklin-CDK komplekslerini inhibe ederek hücreyi G1'de durduran protein."},
            {"term": "Puma ve Noxa", "explanation": "p53 tarafından doğrudan sentezletilen, BAX/BAK'ı açıp apoptozu tetikleyen BH3-only proteinler."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] p53 hücre döngüsünü durdurmak için p21 (CDK inhibitörü) proteinini indükler.",
            "📌 [SINAV SPOTU] p53 apoptozu indüklemek için BAX, Puma ve Noxa genlerini aktive eder.",
            "📌 [SINAV SPOTU] Mitokondriyal yol üzerinden kaspaz kaskadı devreye girer."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "G1/S Freni: p21", "desc": "CDK inhibisyonu ile DNA onarım enzimlerine zaman kazandırma.", "isKey": True},
                {"title": "İntihar Butonu: BAX/Puma", "desc": "Tamir edilemeyen hasarda mitokondriyal apoptozun tetiklenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "p53 Hasar Yanıtı ve Apoptoz Zinciri",
                [
                    "1. DNA Kırığı: Radyasyon veya kemoterapi DNA çift zincirinde kırıklar oluşturur.",
                    "2. p53 Fosforilasyonu: ATM kinazı p53'ü fosforilleyerek MDM2 yıkımından kurtarır.",
                    "3. G1 Duraklaması: p53 p21 genini aktive eder; p21 Siklin-CDK'yı bloke ederek hücreyi G1'de durdurur.",
                    "4. Onarım Başarısızlığı: Hasar çok ağır olduğundan tamir mekanizmaları yetersiz kalır.",
                    "5. Apoptoz Aktivasyonu: p53 BAX ve Puma genlerini açar; mitokondriden sitokrom c sızarak hücre ölür."
                ]
            ),
            make_cloze(
                "p53 proteini DNA hasarı oluştuğunda hücre döngüsünü G1 evresinde durdurmak için p21 adlı CDK inhibitörünü aktive eder.",
                "p21",
                "p53'ün hücre döngüsünü durduran CDK inhibitörü proteini adı"
            )
        ]
    })

    # ADIM 83
    slides.append({
        "slideNumber": 83,
        "title": "p53 Mutasyonu ve Neoplazik Dönüşüm: Li-Fraumeni Sendromu",
        "subtitle": "Genom bekçisinin kaybıyla durdurulamayan genomik instabilite ve çoklu kanser riski",
        "badge": "Onkopatoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Eğer bir hücrede TP53 geninde inaktivasyon veya fonksiyon kaybı (loss-of-function) mutasyonu gelişirse, "
            "hücrenin genetik denetim mekanizması tamamen çöker.\n\n"
            "Radyasyon veya mutajenlerle DNA hasarına uğrayan hücre döngüsünü durduramaz ve apoptoza gidemez. "
            "Hasarlı ve mutasyonlu DNA ile bölünmeye devam eden hücrelerde 'genomik instabilite' katlanarak artar. "
            "Zamanla onkogenik mutasyonlar birikir ve hücre kontrolsüz bir malign tümöre dönüşür.\n\n"
            "> [SINAV SPOTU] İnsan kanserlerinin %50'den fazlasında p53 mutasyonu bulunur. TP53 geninin kalıtsal "
            "tek allel mutasyonu ile doğan bireylerde ise 'Li-Fraumeni Sendromu' görülür!\n\n"
            "Bu hastalarda genç yaşta meme kanseri, sarkomlar, beyin tümörleri ve lösemiler gibi çoklu maligniteler patlak verir."
        ),
        "medicalTerms": [
            {"term": "Genomik İnstabilite", "explanation": "DNA onarım ve apoptoz kusurları nedeniyle hücrede mutasyonların çığ gibi büyümesi durumu."},
            {"term": "Li-Fraumeni Sendromu", "explanation": "TP53 geninde herediter germline mutasyon sonucu erken yaşta çoklu kanserler geliştiren sendrom."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] p53 mutasyonunda hasarlı hücreler apoptoza gidemez; genomik instabilite ve neoplastik dönüşüm artar.",
            "📌 [SINAV SPOTU] İnsan kanserlerinin çoğunda p53 inaktivasyonu mevcuttur.",
            "📌 [SINAV SPOTU] Herediter p53 mutasyonu Li-Fraumeni sendromuna yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bekçisiz Genom", "desc": "Hasarlı hücrelerin apoptozdan kaçarak kontrolsüzce çoğalması.", "isKey": True},
                {"title": "Li-Fraumeni Tablosu", "desc": "Genç yaşta sarkom, meme kanseri, lösemi ve beyin tümörleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Ailesinde genç yaşta osteosarkom, meme kanseri, beyin tümörü ve lösemi öyküsü olan 24 yaşındaki hastada TP53 geninde germline inaktive edici mutasyon saptanıyor. En olası herediter kanser sendromu nedir?",
                {
                    "A": "Lynch Sendromu (HNPCC)",
                    "B": "Li-Fraumeni Sendromu",
                    "C": "Multipl Endokrin Neoplazi (MEN-1)",
                    "D": "Cowden Sendromu",
                    "E": "Nörofibromatozis Tip 1"
                },
                "B",
                {
                    "A": "Lynch sendromunda DNA mismatch onarım (MSH2, MLH1) mutasyonu vardır.",
                    "B": "Doğru cevap B'dir: Herediter TP53 germline mutasyonu Li-Fraumeni sendromunun nedenidir.",
                    "C": "MEN-1 menin mutasyonudur.",
                    "D": "Cowden sendromu PTEN mutasyonudur.",
                    "E": "NF-1 nörofibromin kusurudur."
                }
            ),
            make_cloze(
                "p53 geninin kalıtsal germline mutasyonu sonucu erken yaşta çoklu sarkom ve meme kanserleri ile seyreden tabloya Li-Fraumeni sendromu denir.",
                "Li-Fraumeni",
                "Kalıtsal p53 kanser sendromunun adı"
            )
        ]
    })

    # ADIM 84
    slides.append({
        "slideNumber": 84,
        "title": "Endoplazmik Retikulum (ER) Stresi: Katlanmamış Protein Yanıtı (UPR)",
        "subtitle": "ER lümenindeki şaperon kapasitesinin aşılması ve sensör kinazların uyarılması",
        "badge": "ER Stresi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücrede translasyonu tamamlanan tüm salgı ve membran proteinleri doğru üç boyutlu yapılarına "
            "endoplazmik retikulum (ER) lümeninde kavuşur. Proteinlerin doğru kıvrılması için ortamda yeterli glukoz, "
            "oksijen, nötral redoks dengesi ve şaperon proteinleri (BiP/GRP78) bulunmalıdır.\n\n"
            "Hipoksi, serbest radikaller, kalsiyum tükenmesi veya mutasyonlar ER lümeninde yanlış katlanmış "
            "proteinlerin yığılmasına neden olur; bu metabolik krize 'ER Stresi' denir.\n\n"
            "> [SINAV SPOTU] Normalde şaperon BiP/GRP78, ER zarındaki 3 ana sensöre (IRE1, PERK, ATF6) bağlı durarak "
            "onları inaktif tutar. Yanlış katlanmış proteinler çoğalınca BiP sensörleri bırakıp proteinlere koşar; "
            "sensörler serbest kalarak 'Katlanmamış Protein Yanıtı'nı (UPR) başlatır!\n\n"
            "Bu süreç hücrenin kendini onarmak için verdiği ilk büyük alarmdır."
        ),
        "medicalTerms": [
            {"term": "Katlanmamış Protein Yanıtı (UPR)", "explanation": "Unfolded Protein Response; ER lümenindeki protein yükünü hafifletmek için başlatılan sinyal yolu."},
            {"term": "BiP / GRP78", "explanation": "ER lümeninde protein katlanmasını denetleyen ve UPR sensörlerini inaktif tutan ana şaperon proteini."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] ER'de yanlış katlanmış protein birikimi 'Katlanmamış Protein Yanıtı'nı (UPR) tetikler.",
            "📌 [SINAV SPOTU] ER zarı sensörleri: IRE1 kinazı, PERK ve ATF6'dır.",
            "📌 [SINAV SPOTU] Ana düzenleyici şaperon molekülü BiP/GRP78'dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lümen Yükü", "desc": "Kıvrılamayan proteinlerin ER lümeninde agregat oluşturması.", "isKey": True},
                {"title": "Üç Sensör Sistemi", "desc": "BiP'in ayrılmasıyla aktive olan IRE1, PERK ve ATF6.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["ER Stres Sensörü", "Aktivasyon Mekanizması", "Hücresel Yanıtı"],
                [
                    [("IRE1 Kinazı", False, ""), ("Oligomerizasyon ve otofosforilasyon", True, "Sensör aktivasyon şekli"), ("XBP1 mRNA'sını kırparak şaperon üretimini artırır", False, "")],
                    [("PERK Kinazı", False, ""), ("Dimerleşme ve eIF2alfa fosforilasyonu", True, "Translasyon freni mekanizması"), ("Genel protein sentezini geçici olarak durdurur", False, "")],
                    [("ATF6", False, ""), ("Golgiye taşınarak proteolitik kesim", True, "Golgi proteaz aktivasyonu"), ("Çekirdeğe gidip ER lipid ve şaperon genlerini açar", False, "")]
                ]
            ),
            make_cloze(
                "Endoplazmik retikulumda katlanmamış protein birikimi karşısında başlatılan hücresel kurtarma yanıtına katlanmamış protein yanıtı veya UPR denir.",
                "katlanmamış protein yanıtı",
                "UPR teriminin Türkçe açılımı"
            )
        ]
    })

    # ADIM 85
    slides.append({
        "slideNumber": 85,
        "title": "Adaptif UPR'den Terminal UPR'ye: CHOP ile Apoptotik İnfaz",
        "subtitle": "Kapasite aşıldığında şaperon üretiminden kaspaz aktivasyonuna geçen hücresel rota",
        "badge": "Terminal UPR",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Katlanmamış protein yanıtı (UPR) iki fazlı bir savunma hattıdır:\n"
            "1. Adaptif UPR (Kurtarma Fazı): Hücre ilk evrede genel protein translasyonunu durdurur (yeni protein "
            "girişi kesilir), şaperon üretimini artırır ve yanlış katlanmış proteinleri proteazomlarda yıkar (ERAD). "
            "Bu sayede ER yükü hafifletilmeye çalışılır.\n\n"
            "2. Terminal UPR (İnfaz Fazı): Eğer stres devam eder ve protein yükü düzeltilemeyecek kadar yüksek olursa "
            "adaptif kapasite aşılır. Hücre yaşam umudunu keserek intihar yoluna girer.\n\n"
            "> [SINAV SPOTU] Terminal UPR evresinde 'CHOP' (C/EBP Homology Protein) transkripsiyon faktörü aktive olur. "
            "CHOP anti-apoptotik BCL-2'yi baskılarken pro-apoptotik Bim ve Bax'ı tetikler; mitokondriyal apoptoz "
            "başlar ve hücre sessizce ölür!\n\n"
            "Ders notunda vurgulandığı gibi bu durum onarılamaz şekilde hasar görmüş hücrelerin dokuyu zehirlemesini önler."
        ),
        "medicalTerms": [
            {"term": "Adaptif UPR", "explanation": "Şaperonları artırıp protein sentezini yavaşlatarak hücreyi yaşatmayı hedefleyen erken ER yanıtı."},
            {"term": "CHOP Proteini", "explanation": "Terminal ER stresinde BCL-2'yi baskılayıp apoptozu patlatan ana transkripsiyon faktörü."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hafif/erken ER stresinde şaperonlar artar, protein sentezi yavaşlar (adaptif yanıt).",
            "📌 [SINAV SPOTU] Yük fazla ve stres çözülemezse terminal UPR devreye girer; CHOP ve mitokondriyal apoptoz aktive olur.",
            "📌 [SINAV SPOTU] Terminal UPR onarılamaz hücreyi öldürerek çevreyi korur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kurtarma: Şaperonlar", "desc": "BiP ve ERAD ile hatalı proteinlerin imhası.", "isKey": True},
                {"title": "İnfaz: CHOP Faktörü", "desc": "Stres aşıldığında mitokondriyal apoptozun tetiklenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Adaptif UPR vs Terminal UPR Karşılaştırması",
                "Adaptif UPR (Hafif Stres)",
                "Şaperon proteinleri artar, genel protein sentezi yavaşlar, yanlış katlanmış protein yükü azaltılır ve hücre kurtulur.",
                "Terminal UPR (Ağır / Çözümsüz Stres)",
                "Adaptif kapasite aşılır; CHOP aktive olur, BCL-2 baskılanır, mitokondriyal apoptoz yolu tetiklenir ve hücre ölür."
            ),
            make_cloze(
                "Terminal ER stresinde adaptif kapasite aşıldığında hücreyi mitokondriyal apoptoza sevk eden anahtar protein CHOP faktörüdür.",
                "CHOP",
                "Terminal katlanmamış protein yanıtı transkripsiyon faktörü adı"
            )
        ]
    })

    # ADIM 86
    slides.append({
        "slideNumber": 86,
        "title": "Hücre İçi Kalsiyum Dengesi: 10.000 Katlık Gradyan ve Depolar",
        "subtitle": "Ekstraselüler milimolar kalsiyuma karşı sitozolün 100 nanomolarlık kırılgan kalkanı",
        "badge": "Kalsiyum Gradyanı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kalsiyum (Ca²⁺) iyonu hücre içinde son derece güçlü bir ikinci habercidir; ancak fazlası tam anlamıyla "
            "ölümcül bir toksindir. Bu nedenle sağlıklı bir hücre sitoplazmik serbest kalsiyum düzeyini "
            "inanılmaz derecede düşük tutar.\n\n"
            "Ekstraselüler sıvıda kalsiyum konsantrasyonu yaklaşık 1.3 mM (milimolar) iken, sitozoldeki serbest "
            "kalsiyum konsantrasyonu 0.1 μM (100 nanomolar) düzeyindedir; aralarında tam 10.000 KAT fark vardır!\n\n"
            "> [SINAV SPOTU] Hücre içindeki kalsiyum sitozolde serbest durmaz; ATP bağımlı kalsiyum pompaları "
            "(SERCA) ile Endoplazmik Retikulum lümeninde ve mitokondri matriksinde hapsedilmiştir!\n\n"
            "Bu devasa gradyanı korumak sürekli ve kesintisiz ATP harcanmasını gerektirir."
        ),
        "medicalTerms": [
            {"term": "Sitozolik Ca2+ Düzeyi", "explanation": "Sağlıklı hücrede 0.1 mikromolar (nanomolar düzeyde) tutulan serbest kalsiyum miktarı."},
            {"term": "SERCA Pompası", "explanation": "Sarkoplazmik/Endoplazmik Retikulum Ca2+ ATPaz pompası; kalsiyumu ER lümenine pompalayan enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Normalde hücre sitoplazmasında serbest Ca²⁺ düzeyi çok düşüktür (< 0.1 μM).",
            "📌 [SINAV SPOTU] Kalsiyum hücre içinde mitokondri ve endoplazmik retikulumda (ER) depolanır.",
            "📌 [SINAV SPOTU] Hücre dışı ile sitozol arasında yaklaşık 10.000 katlık konsantrasyon gradyanı vardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "10.000 Katlık Uçurum", "desc": "Ekstraselüler 1.3 mM vs intraselüler 0.1 uM konsantrasyon farkı.", "isKey": True},
                {"title": "SERCA Muhafızı", "desc": "Kalsiyumun ER ve mitokondride ATP harcanarak saklanması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Sağlıklı bir hücrede sitoplazmik kalsiyum konsantrasyonu normalde nasıldır ve hücre içi depoları nerelerdir?",
                "Sitozolde çok düşüktür (< 0.1 uM); hücre içindeki kalsiyum Endoplazmik Retikulum (ER) lümeninde ve mitokondride depolanır."
            ),
            make_cloze(
                "Normal hücrede sitoplazmik serbest kalsiyum düzeyi çok düşüktür ve kalsiyum başlıca endoplazmik retikulum ve mitokondride depolanır.",
                "endoplazmik retikulum",
                "Hücre içi kalsiyum depolayan ana organel"
            )
        ]
    })

    # ADIM 87
    slides.append({
        "slideNumber": 87,
        "title": "İskemik Hasarda Kalsiyum Kaosu: Pompaların Çöküşü ve Sitozolik Tufan",
        "subtitle": "ATP tükenmesiyle plazma zarı ve ER pompalarının iflası ve hücreye kalsiyum hücumu",
        "badge": "Kalsiyum Tufanı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İskemi veya toksik hasar meydana geldiğinde mitokondriyal oksidatif fosforilasyon durur ve ATP hızla tükenir. "
            "ATP azlığı ilk olarak plazma zarındaki Na+/K+ ATPaz ve Ca²⁺ ATPaz pompalarını, ardından ER zarındaki "
            "SERCA pompasını felç eder.\n\n"
            "Pompalar durduğunda hücrenin kalsiyum dengesi çöker. Bir yandan hücre dışındaki 10.000 kat yoğun kalsiyum "
            "açılan kanallardan sitoplazmaya hücum eder; diğer yandan ER ve mitokondri depolarındaki kalsiyum serbest kalarak sitozole dökülür.\n\n"
            "> [SINAV SPOTU] Hücre içi kalsiyum düzeyinin kontrolsüzce patlamasına 'Kalsiyum Tufanı' denir. "
            "Sitozolik Ca²⁺ artışı mitokondri membran geçirgenlik porunu (MPTP) açarak ATP üretimini sonsuza dek imkansız kılar!\n\n"
            "Bu durum hücreyi geri dönüşsüz nekroz girdabına sokar."
        ),
        "medicalTerms": [
            {"term": "Kalsiyum Tufanı (Ca2+ Influx)", "explanation": "Pompaların çökmesiyle ekstraselüler ve organel içi kalsiyumun sitozole kontrolsüz dolması."},
            {"term": "MPTP (Mitokondriyal Geçirgenlik Poru)", "explanation": "Yüksek kalsiyumla açılan ve mitokondri zar potansiyelini sıfırlayan ölümcül por."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücre hasarında hücre içine Ca²⁺ girişi artar ve depolardan (ER/mitokondri) sitozole Ca²⁺ salınır.",
            "📌 [SINAV SPOTU] Sitozolik Ca²⁺ artışı mitokondri membran potansiyelini sıfırlayarak ATP üretimini tamamen bitirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Pompa İflası", "desc": "ATP tükenince Ca2+ ATPaz ve SERCA'nın durması.", "isKey": True},
                {"title": "Çift Yönlü İstilâ", "desc": "Hem dış ortamdan hem ER depolarından sitozole kalsiyum boşalması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "İskemide Kalsiyum Kaosu Gelişim Basamakları",
                [
                    "1. İskemi ve Hipoksi: Oksijen kesilince mitokondriyal ATP sentezi çöker.",
                    "2. Pompa İflası: Plazma zarı Ca2+ ATPaz ve ER SERCA pompaları enerjisiz kalıp durur.",
                    "3. Kalsiyum Hücumu: Hücre dışındaki kalsiyum derişim farkıyla hücre içine kontrolsüz akar.",
                    "4. Depo Boşalması: Endoplazmik retikulum ve mitokondri içindeki kalsiyumu sitozole kusar.",
                    "5. Sitozolik Patlama: Sitozolik kalsiyum mikromolar düzeylere fırlayarak ölümcül enzimleri tetikler."
                ]
            ),
            make_cloze(
                "Hücre hasarında plazma zarı pompalarının bozulması sonucu hücre içine kalsiyum girişi artar ve depolardan sitoplazmaya salınır.",
                "kalsiyum",
                "İntraselüler seviyesi artınca enzimleri aktive eden katyon"
            )
        ]
    })

    # ADIM 88
    slides.append({
        "slideNumber": 88,
        "title": "Kalsiyumun Aktive Ettiği Yıkıcı Enzimler: Dörtlü İnfaz Mangası",
        "subtitle": "Fosfolipaz, proteaz, endonükleaz ve ATPaz enzimlerinin hücreyi içeriden sindirmesi",
        "badge": "Yıkıcı Enzimler",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Sitozolik kalsiyum patlaması hücre için neden bu kadar öldürücüdür? Çünkü kalsiyum iyonu, normalde "
            "sitoplazmada uyuyan en tahripkar 4 hidrolitik enzim ailesinin evrensel açma anahtarıdır!\n\n"
            "Kalsiyum fırladığında şu 4 enzim eşzamanlı olarak tetiklenir:\n"
            "1. Fosfolipazlar: Plazma zarı ve organel zarlarındaki fosfolipidleri parçalayarak membran delinmesini hızlandırır.\n"
            "2. Proteazlar (Kalpain vb.): Hücre iskeleti ve membran proteinlerini keserek hücre mimarisini çökertir.\n"
            "3. Endonükleazlar: Nükleer kromatini ve DNA'yı parçalayarak çekirdek erimesine (karyolizis) yol açar.\n\n"
            "> [SINAV SPOTU] 4. ATPazlar: Hücrenin elinde kalan son damla ATP moleküllerini de hızla hidrolize ederek "
            "enerji krizini mutlaklaştırır!\n\n"
            "Bu dörtlü yıkım enzimi geri dönüşümsüz hasarın ve nekrotik ölümün biyokimyasal cellatlarıdır."
        ),
        "medicalTerms": [
            {"term": "Fosfolipaz Aktivasyonu", "explanation": "Kalsiyum uyarısıyla membran fosfolipidlerini hidrolize edip zarları eriten enzim aktivitesi."},
            {"term": "Kalpain", "explanation": "Kalsiyum bağımlı sitozolik proteaz; sitoskeleton proteinlerini parçalayarak hücreyi çözen enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sitozolik Ca²⁺ artışının aktive ettiği başlıca 4 enzim: Fosfolipaz, Proteaz, Endonükleaz ve ATPaz'dır.",
            "📌 [SINAV SPOTU] Fosfolipaz membranları, Proteaz sitoskeletonu, Endonükleaz DNA'yı yıkar; ATPaz enerjiyi tüketir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dörtlü Cellat", "desc": "Fosfolipaz (zar), Proteaz (iskelet), Endonükleaz (DNA), ATPaz (enerji).", "isKey": True},
                {"title": "Membran İflası", "desc": "Fosfolipid yıkım ürünlerinin deterjan etkisiyle zarları eritmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Kalsiyumla Aktive Olan Enzim", "Hücresel Hedefi", "Patolojik Hasar Sonucu"],
                [
                    [("Fosfolipazlar", False, ""), ("Plazma ve organel membran fosfolipidleri", True, "Zar yıkım hedefi"), ("Membran hasarı ve parçalanması", False, "")],
                    [("Proteazlar (Kalpain vb.)", False, ""), ("Hücre iskeleti ve membran proteinleri", True, "İskelet yıkım hedefi"), ("Sitoskeleton yıkımı ve tomurcuklanma", False, "")],
                    [("Endonükleazlar", False, ""), ("Genomik DNA ve kromatin yapısı", True, "Nükleer yıkım hedefi"), ("Karyolizis ve DNA parçalanması", False, "")],
                    [("ATPazlar", False, ""), ("Mevcut hücresel ATP molekülleri", True, "Enerji yıkım hedefi"), ("ATP tükenmesinin hızlanması", False, "")]
                ]
            ),
            make_cloze(
                "Hücre hasarında artan sitozolik kalsiyum proteaz, endonükleaz, ATPaz ve hücre zarlarını parçalayan fosfolipaz enzimlerini aktive eder.",
                "fosfolipaz",
                "Membran lipidlerini parçalayan kalsiyum bağımlı enzim"
            )
        ]
    })

    # ADIM 89 (CHECKPOINT 9)
    slides.append({
        "slideNumber": 89,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] DNA Hasarı, ER Stresi ve Kalsiyum Kaosu",
        "subtitle": "p53 mekanizması, UPR evreleri, SERCA iflası ve dörtlü kalsiyum enzimlerinin konsolide özeti",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 9,
        "synthesisNarrative": (
            "Bu kontrol noktasında, hücre içi hasarın 3 büyük biyokimyasal motorunu eksiksiz biçimde hafızamıza mühürlüyoruz.\n\n"
            "1. DNA Hasarı ve p53: p53 'Genom Bekçisi'dir. Hafif hasarda p21 ile hücre döngüsünü G1'de durdurup onarıma "
            "izin verir; onarılamazsa BAX ve Puma ile apoptozu patlatır. p53 kaybı kansere (Li-Fraumeni) zemin hazırlar.\n\n"
            "2. ER Stresi ve UPR: Yanlış katlanmış proteinler BiP'i meşgul ederek IRE1, PERK ve ATF6 sensörlerini serbest "
            "bırakır. Hafif krizde adaptif şaperon yanıtı; ağır krizde CHOP faktörü ile terminal UPR apoptozu çalışır.\n\n"
            "> [ÖZET REÇETE] Kalsiyum Kaosu Formülü:\n"
            "ATP tükenmesi -> Ca²⁺ Pompaları (SERCA) durur -> Sitozole kalsiyum tufanı -> 4 Yıkıcı Enzim Aktifleşir:\n"
            "Fosfolipaz (zar), Proteaz (iskelet), Endonükleaz (DNA), ATPaz (enerji) -> Geri Dönüşsüz Hücre Nekrozu!\n\n"
            "Bu biyokimyasal zincir tüm iskemik ve toksik nekrozların ortak paydasıdır."
        ),
        "medicalTerms": [
            {"term": "Biyokimyasal Hasar Üçlüsü", "explanation": "DNA hasarı (p53), protein yanlış katlanması (ER stresi) ve intraselüler kalsiyum patlaması."},
            {"term": "Dörtlü Kalsiyum Enzimi", "explanation": "Fosfolipaz, proteaz, endonükleaz ve ATPaz'dan oluşan nekroz infaz mangası."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] p53 = Genom Bekçisi. p21 ile döngüyü durdurur, BAX/Puma ile apoptoz yapar.",
            "📌 [CHECKPOINT ÖZETİ] ER Stresi = Yanlış katlanmış proteinler. Erken şaperon adaptasyonu; terminalde CHOP ile apoptoz.",
            "📌 [CHECKPOINT ÖZETİ] Ca²⁺ Tufanı = Sitozole hücum eden kalsiyum Fosfolipaz, Proteaz, Endonükleaz ve ATPaz'ı açar."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-25",
                "p53 proteininin hafif DNA hasarında hücre döngüsünü G1 evresinde durdurmasını sağlayan temel CDK inhibitörü protein hangisidir?",
                "p21 (CDKN1A / WAF1/CIP1) proteinidir."
            ),
            make_flashcard(
                "fc-k1-05-26",
                "Endoplazmik retikulumda yanlış katlanmış protein birikimi adaptif kapasiteyi aştığında hücreyi apoptoza sevk eden terminal transkripsiyon faktörü nedir?",
                "CHOP (C/EBP Homology Protein) faktörüdür."
            ),
            make_flashcard(
                "fc-k1-05-27",
                "Hücre hasarında sitoplazmaya hücum eden kalsiyum iyonlarının aktive ettiği başlıca 4 yıkıcı enzim grubu hangileridir?",
                "Fosfolipazlar (membranı yıkar), Proteazlar (sitoskeletonu yıkar), Endonükleazlar (DNA'yı parçalar) ve ATPazlar (kalan ATP'yi tüketir)."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Hücre Hasarının Moleküler Savunma ve Yıkım Hatları Tablosu",
                "headers": ["Hasar Mekanizması", "Savunma / Sensör Sistemi", "Geri Dönüşsüz İnfaz Kararı"],
                "rows": [
                    ["DNA Kırıkları / Radyasyon", "p53 birikimi -> p21 ile G1 blokajı", "BAX, Puma, Noxa ile mitokondriyal apoptoz"],
                    ["Yanlış Katlanmış Proteinler", "BiP/GRP78, IRE1, PERK, ATF6 (Adaptif UPR)", "CHOP faktörü ve terminal UPR apoptozu"],
                    ["ATP Azlığı ve Ca2+ Kaosu", "SERCA ve Ca2+ ATPaz pompaları", "Fosfolipaz, proteaz, endonükleaz ile nekroz"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Patolojik Durum", "Primer Moleküler Hasar", "Hücrenin Yanıtı"],
                [
                    [("Radyasyon / Kemoterapi", False, ""), ("DNA Çift Sarmal Kırıkları", True, "Genotoksik moleküler hasar"), ("p53 bağımlı G1 duraklaması veya apoptoz", False, "")],
                    [("Protein Katlanma Kusurları", False, ""), ("ER Lümeninde Agregat Yığılması", True, "Proteotoksik ER hasarı"), ("Adaptif UPR şaperon yanıtı veya CHOP apoptozu", False, "")],
                    [("İskemi / Hipoksi", False, ""), ("SERCA Durması ve Sitozolik Ca2+ Tufanı", True, "İyonik gradyan çöküşü"), ("Fosfolipaz ve proteaz aktivasyonuyla nekroz", False, "")]
                ]
            ),
            make_active_recall(
                "İskemiye uğrayan bir hücrede ATPaz enziminin kalsiyumla aşırı aktive olmasının yarattığı kısır döngü nedir?",
                "Hücrenin elinde kalan son eser miktardaki ATP'yi de hızla parçalayarak enerji krizini derinleştirir ve hücreyi kesin nekroza sürükler."
            )
        ]
    })

    # ADIM 90
    slides.append({
        "slideNumber": 90,
        "title": "Kalsiyum Kanal Blokörlerinin Sitoprotektif Potansiyeli",
        "subtitle": "İskemik dokularda hücre içine kalsiyum girişini sınırlayan farmakolojik stratejiler",
        "badge": "Farmakoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre içi kalsiyum aşırı yüklenmesinin nekroz patogenezindeki merkezi rolü anlaşıldıktan sonra, "
            "tıp dünyası sitoprotektif (hücre koruyucu) tedaviler geliştirmeye odaklanmıştır.\n\n"
            "Akut miyokard infarktüsü ve serebral iskemide plazma zarındaki voltaj bağımlı L-tipi kalsiyum "
            "kanallarını bloke eden ajanlar (Kalsiyum Kanal Blokörleri / CCB) araştırılmıştır.\n\n"
            "> [KLİNİK İPUCU] Kalsiyum antagonistleri hücre içine kalsiyum girişini azaltarak vazospazmı çözer, "
            "kardiyak iş yükünü ve oksijen tüketimini düşürür ve fosfolipaz/proteaz aktivasyonunu kısmen frenler.\n\n"
            "Ancak intraselüler depolardan (ER) kalsiyum sızıntısı devam ettiği için tek başına CCB'ler hücre nekrozunu "
            "tamamen durduramaz; en etkili tedavi daima damarın acil reperfüzyonudur (primer PTCA)."
        ),
        "medicalTerms": [
            {"term": "Sitoproteksiyon", "explanation": "İskemik veya toksik hasara maruz kalan hücrelerin canlılığını korumaya yönelik farmakolojik müdahaleler."},
            {"term": "Kalsiyum Kanal Blokörü (CCB)", "explanation": "Plazma membranındaki voltaj bağımlı kalsiyum kanallarını tıkayarak hücreye Ca2+ girişini azaltan ilaç."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kalsiyum kanal blokajı hücre içine aşırı Ca²⁺ girişini sınırlayarak vazospazmı ve enzim aktivasyonunu azaltır.",
            "📌 [SINAV SPOTU] İskemik hasarda en kesin kurtuluş dokunun acil reperfüzyonudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kalsiyum Giriş Engeli", "desc": "L-tipi voltaj kanallarının ilaçla kapatılması.", "isKey": True},
                {"title": "Sınırlı Sitoproteksiyon", "desc": "İntraselüler ER sızıntısını engelleyememesi gerçeği.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut miyokard enfarktüsü geçiren hastada koroner damar açılana kadar kardiyomiyositlerin nekroza gitmesini yavaşlatmak amacıyla hekim kalsiyum girişini azaltmayı hedefler. Hücresel gerekçe nedir?",
                [
                    {
                        "text": "Kalsiyum azalırsa hücrede ATP üretimi on kat artar.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Kalsiyum azalması doğrudan ATP üretimini artırmaz."
                    },
                    {
                        "text": "Sitozolik kalsiyum yükselmesi engellenirse zarları ve iskeleti eriten fosfolipaz ve proteaz enzimlerinin aktivasyonu geciktirilir.",
                        "isCorrect": True,
                        "feedback": "Kusursuz patofizyolojik mantık! Kalsiyum girişini kısmak yıkıcı enzimlerin patlamasını geciktirir."
                    },
                    {
                        "text": "Kalsiyum azalınca hücre anında apoptoza gider.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Amaç hücreyi canlı tutmaktır."
                    }
                ]
            ),
            make_cloze(
                "Hücre hasarında sitozolik kalsiyum girişini sınırlamak zarları parçalayan fosfolipaz ve proteaz enzimlerinin yıkıcı etkilerini yavaşlatır.",
                "fosfolipaz",
                "Hücre zarlarını parçalayan kalsiyum bağımlı enzim grubu"
            )
        ]
    })

    return slides
