"""
Bölüm 5: Yanlış Katlanmış Protein Hastalıkları: α1-Antitripsin, Kistik Fibrozis ve Prionlar
Adımlar: 41 - 50
Checkpoint: Adım 49 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # ADIM 41
    slides.append({
        "slideNumber": 41,
        "title": "Protein Katlanma Biyolojisi, Şaperonlar ve Ubikitin-Proteazom Yolağı",
        "subtitle": "Hücresel kalite kontrol ağları, HSP şaperonları ve polipeptit konformasyonu",
        "badge": "Katlanma Biyolojisi",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Ribozomlarda sentezlenen polipeptit zincirlerinin biyolojik olarak aktif hale gelebilmesi için doğru "
            "üç boyutlu (tersiyer) konformasyona katlanması zorunludur. Bu kritik süreç, ısı şoku proteinleri (HSP70, "
            "HSP90) ve endoplazmik retikulum (ER) şaperonları (kalneksin, BiP) tarafından titizlikle yönlendirilir.\n\n"
            "> [TEMEL İLKE] Hatalı katlanan proteinler şaperonlar tarafından tanınır; düzeltilemeyenler ER ile ilişkili "
            "yıkım (ERAD) yolağıyla sitozole aktarılıp ubikitinlenir ve 26S proteazomunda parçalanır.\n\n"
            "Bu kalite kontrol sistemi aşıldığında veya mutasyonlar şaperon sistemini kilitlediğinde yanlış katlanmış "
            "proteinler birikerek 'konformasyonel hastalıklara' yol açar."
        ),
        "medicalTerms": [
            {"term": "Şaperon", "explanation": "Yeni sentezlenen proteinlerin doğru üç boyutlu konformasyona katlanmasını sağlayan yardımcı proteinlerdir."},
            {"term": "Ubikitin-Proteazom Yolağı", "explanation": "Hatalı veya ömrü bitmiş proteinleri ubikitinle işaretleyip 26S proteazomda yıkan ana sistemdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Doğru katlanamayan proteinler ERAD yolağıyla proteazomlara gönderilir.",
            "📌 [SINAV SPOTU] Şaperonlar protein agregasyonunu önleyen hücresel koruyuculardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Katlanma Kontrolü", "desc": "BiP, kalneksin ve HSP ailesi doğru üçüncül yapıyı denetler.", "isKey": True},
                {"title": "Geri Dönüşümsüz Yıkım", "desc": "Kurtarılamayan mutant proteinler proteazomda amino asitlere ayrılır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Yeni sentezlenen polipeptitlerin doğru katlanmasını denetleyen ve agregasyonu önleyen proteinlere şaperon adı verilir.",
                "şaperon",
                "Protein katlanmasına refakat eden moleküler bekçiler"
            ),
            make_active_recall(
                "Hücrede yanlış katlanan ve düzeltilemeyen proteinlerin parçalanması için görev yapan iki anahtar sistem nedir?",
                "Ubikitin işaretleme sistemi ve 26S proteazom kompleksidir."
            )
        ]
    })

    # ADIM 42
    slides.append({
        "slideNumber": 42,
        "title": "Endoplazmik Retikulum (ER) Stresi ve Açılmamış Protein Yanıtı (UPR)",
        "subtitle": "Lümende hatalı protein göllenmesi, BiP ayrılması ve apoptoz tetiği",
        "badge": "ER Stresi ve UPR",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Endoplazmik retikulum lümeninde yanlış katlanmış veya katlanmamış proteinlerin aşırı miktarda toplanması "
            "'ER stresi' durumunu başlatır. ER stres sensörleri olan IRE1, PERK ve ATF6, normalde BiP şaperonuna bağlıdır; "
            "hatalı proteinler BiP'i kendine çekince bu sensörler aktive olur ve açılmamış protein yanıtını (UPR) tetikler.\n\n"
            "> [YÜKSEK VERİM] UPR başlangıçta genel protein translasyonunu durdurur ve şaperon üretimini artırarak "
            "hücreyi kurtarmaya çalışır; ancak stres devam ederse CHOP transkripsiyon faktörü üzerinden apoptozu başlatır.\n\n"
            "Bu durum, hücrenin hatalı proteinleri tolere edemediğinde intiharı seçerek dokuyu koruma refleksidir."
        ),
        "medicalTerms": [
            {"term": "ER Stresi", "explanation": "ER lümeninde hatalı katlanmış proteinlerin aşırı birikmesiyle doğan patolojik hücresel durumdur."},
            {"term": "Açılmamış Protein Yanıtı (UPR)", "explanation": "ER stresine karşı hücresel homeostazı restore etmeye veya apoptozu tetiklemeye yarayan adaptif sinyal yolağıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] UPR çözülemediğinde CHOP ve kaspaz-12/kaspaz-9 üzerinden apoptoz başlatır.",
            "📌 [SINAV SPOTU] BiP şaperonunun sensörlerden ayrılması ER stres yanıtını aktive eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Adaptif Evre", "desc": "Yeni protein sentezini durdur, şaperon ve proteazom kapasitesini artır.", "isKey": True},
                {"title": "Apoptotik Evre", "desc": "Kronik ER stresinde CHOP aktivasyonu ile mitokondriyal apoptoz tetiklenir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "ER Stresinden Hücre Ölümüne Uzanan Zincir",
                [
                    "1. Protein Göllenmesi: ER lümeninde yanlış katlanmış mutant polipeptitler yığılır.",
                    "2. BiP Ayrılması: Şaperon BiP sensörlerden (PERK, IRE1) ayrılarak agregatlara bağlanır.",
                    "3. UPR İndüksiyonu: Sensörler aktive olarak translasyonu frenler ve UPR genlerini uyarır.",
                    "4. CHOP Aktivasyonu: Stres çözülemezse pro-apoptotik CHOP proteini indüklenir.",
                    "5. Apoptoz: Pro-apoptotik proteinler (Bim, Bax) mitokondriyi delerek hücre ölümünü gerçekleştirir."
                ]
            ),
            make_cloze(
                "Çözülemeyen ağır ER stresi durumunda apoptozu tetikleyen temel transkripsiyon faktörü CHOP proteinidir.",
                "CHOP",
                "ER stresine bağlı apoptozun anahtar transkripsiyon faktörü"
            )
        ]
    })

    # ADIM 43
    slides.append({
        "slideNumber": 43,
        "title": "Yanlış Katlanmış Protein Hastalıklarının İki Ana Mekanizması",
        "subtitle": "Fonksiyon kaybı (erken yıkım/eksiklik) vs Toksik fonksiyon kazanımı (ER stresi/hücre kaybı)",
        "badge": "Mekanizma Ayrımı",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Yanlış katlanan proteinlerin neden olduğu patolojiler temel olarak iki ana mekanizmaya ayrılır: "
            "1) Mutant proteinin şaperonlarca erkenden tanınıp aşırı hevesle yıkılması sonucu kanda veya hedef dokuda "
            "işlevsel protein eksikliği (fonksiyon kaybı), 2) Mutant proteinin hücre içinde birikerek şiddetli ER stresi "
            "ve toksik agregatlar oluşturup hücre ölümüne yol açması (hücre kaybı / toksik fonksiyon kazanımı).\n\n"
            "> [SINAV SPOTU] Kistik fibrozis ve ailesel hiperkolesterolemi primer fonksiyon kaybı; prion ve retinitis "
            "pigmentosa ER stresi kaynaklı hücre kaybı; α1-antitripsin eksikliği ise her iki mekanizmayı birden barındırır.\n\n"
            "Bu ayrım, ders kitabının (Robbins) Tablo 1.4 sınıflandırmasının temelini oluşturur."
        ),
        "medicalTerms": [
            {"term": "Fonksiyon Kaybı (Loss of Function)", "explanation": "Mutant proteinin hızla yıkılması nedeniyle dokunun o proteinin eksikliğini yaşamasıdır."},
            {"term": "Toksik Birikim (Toxic Aggregation)", "explanation": "Mutant proteinin hücrede agregat yaparak ER stresi ve apoptoza yol açmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] CFTR ve LDLR mutant proteinlerin erkenden yıkılıp eksikliğe yol açtığı gruptadır.",
            "📌 [SINAV SPOTU] Prion hastalığı ve retinitis pigmentosa ER stresiyle hücre ölümünün baskın olduğu gruptadır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Grup 1: Eksiklik", "desc": "Hücre proteini erkenden imha eder, hedef dokuda protein bulunamaz.", "isKey": True},
                {"title": "Grup 2: ER Stresi", "desc": "Agregatlar hücreyi zehirler ve apoptozla hücre kaybı yapar.", "isKey": True},
                {"title": "Grup 3: Çift Yönlü", "desc": "α1-Antitripsin hem karaciğerde birikim hem akciğerde eksiklik yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Grup", "Hastalık Örneği", "Etkilenen Protein", "Temel Patogenetik Sonuç"],
                [
                    [("Erken Yıkım / Eksiklik", False, ""), ("Kistik Fibrozis", False, ""), ("CFTR", True, "Klor iletkenlik düzenleyici iyon kanalı"), ("İyon taşınma bozukluğu, koyu sekresyon")],
                    [("ER Stresi / Hücre Kaybı", False, ""), ("Creutzfeldt-Jakob", False, ""), ("Prion Proteini (PrP)", True, "Nörodejenerasyona yol açan enfeksiyöz konformasyon"), ("Nöron apoptozu, spongioform ensefalopati")],
                    [("Her İki Mekanizma", False, ""), ("α1-Antitripsin Eksikliği", False, ""), ("α1-Antitripsin (AAT)", True, "SERPINA1 gen ürünü proteaz inhibitörü"), ("KC'de ER stresi/siroz + AC'de amfizem")]
                ]
            ),
            make_cloze(
                "Kistik fibrozis hastalığında mutant CFTR proteini ER'de tanınıp erkenden proteazomda yıkıldığı için hücre membranında eksiklik gelişir.",
                "CFTR",
                "Kistik fibroziste mutant olan transmembran klor kanalı"
            )
        ]
    })

    # ADIM 44
    slides.append({
        "slideNumber": 44,
        "title": "Kistik Fibrozis (CFTR) ve ER'de Yıkım Nedeniyle Fonksiyon Kaybı",
        "subtitle": "ΔF508 delesyonu, şaperon yakalaması ve klor iyonu transportunun felci",
        "badge": "Kistik Fibrozis",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Kistik fibrozis (CF), 7. kromozomdaki CFTR geninde meydana gelen mutasyonlar (en sık 508. pozisyondaki "
            "fenilalanin amino asidinin delesyonu: ΔF508) sonucu ortaya çıkar. İlginç olan şudur: ΔF508 mutant CFTR "
            "proteini aslında hücre membranına ulaşabilse kısmi klor kanalı aktivitesi gösterebilecek durumdadır.\n\n"
            "> [SINAV SPOTU] Ancak ER şaperonları proteini 'yanlış katlanmış' olarak etiketler, hücre zarına gitmesine "
            "izin vermez ve ERAD yolağıyla proteazoma göndererek tamamen yok eder.\n\n"
            "Sonuçta epitel apikal zarında CFTR kanalı hiç bulunamaz; klor sekresyonu durur, lümen suyu çekilir ve "
            "akciğer, pankreas ve bağırsakta son derece yapışkan, koyu müküs tıkaçları oluşur."
        ),
        "medicalTerms": [
            {"term": "CFTR", "explanation": "Epitel apikal zarında klor salınımını ve sodyum emilimini düzenleyen ABC taşıyıcı proteinidir."},
            {"term": "ΔF508 Mutasyonu", "explanation": "CFTR'nin en sık görülen katlanma hatası ve proteazomal erken yıkım mutasyonudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kistik fibroziste patoloji mutant proteinin agregat yapması değil, ER'de erkenden yıkılmasıdır.",
            "📌 [SINAV SPOTU] Zarda CFTR bulunamaması klor sekresyonunu ve su taşınmasını kilitler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Moleküler Kusur", "desc": "ΔF508 mutasyonu şaperonlarca tanınır ve proteazoma sürülür.", "isKey": True},
                {"title": "Klinik Tablo", "desc": "Kronik bronşiektazi, Pseudomonas enfeksiyonları, mekonyum ileusu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Kistik fibrozis patogenezinde en sık görülen ΔF508 mutasyonuna sahip CFTR proteininin hücresel kaderi aşağıdakilerden hangisidir?",
                {
                    "A": "Mitokondriye giderek sitokrom c salınımına yol açması",
                    "B": "ER kalite kontrol sistemleri tarafından tanınıp membrana ulaşamadan proteazomda yıkılması",
                    "C": "Hücre çekirdeğine girerek RNA polimerazı inhibe etmesi",
                    "D": "Lizozomlarda sindirilemeyen glukoserebrozid kristallerine dönüşmesi",
                    "E": "Plazma membranında kalsiyum kanalı olarak ters çalışması"
                },
                "B",
                {
                    "A": "CFTR mitokondriye gitmez, bir epitel iyon kanalıdır.",
                    "B": "Doğru! ΔF508 proteini ER'de hatalı katlanmış kabul edilerek erkenden proteazomda imha edilir.",
                    "C": "Çekirdeğe girip transkripsiyonu durdurmaz.",
                    "D": "Glukoserebrozid Gaucher hastalığına aittir.",
                    "E": "Zarda kalsiyum kanalı olmaz, zarda hiç bulunamaz."
                }
            ),
            make_cloze(
                "Kistik fibroziste en sık görülen katlanma ve erken yıkım mutasyonu ΔF508 delesyonudur.",
                "ΔF508",
                "Fenilalanin kaybıyla giden klasik kistik fibrozis mutasyonu"
            )
        ]
    })

    # ADIM 45
    slides.append({
        "slideNumber": 45,
        "title": "Ailesel Hiperkolesterolemi (LDLR) ve Tay-Sachs'ta Katlanma Hataları",
        "subtitle": "Reseptör ve enzim moleküllerinin ER'de takılması ve fonksiyon eksikliği",
        "badge": "LDLR ve Tay-Sachs",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Yanlış katlanma nedeniyle erken proteazomal yıkıma uğrayan ve fonksiyon eksikliği yaratan iki çarpıcı "
            "örnek daha vardır: Ailesel hiperkolesterolemi (Sınıf 2 LDLR mutasyonları) ve Tay-Sachs hastalığı. "
            "Sınıf 2 LDLR mutasyonlarında LDL reseptör proteini ER'de sentezlenir ancak katlanamadığı için Golgi "
            "aygıtına ve hücre yüzeyine taşınamaz; ER'de parçalanır.\n\n"
            "> [YÜKSEK VERİM] Karaciğer yüzeyinde LDL reseptörü bulunmadığından LDL kandan temizlenemez ve ağır "
            "erken ateroskleroz gelişir.\n\n"
            "Tay-Sachs hastalığının bazı moleküler varyantlarında ise heksozaminidaz A'nın alfa alt birimi yanlış "
            "katlandığı için lizozoma ulaşamadan ER'de yıkılır; nöronlarda GM2 gangliozid depolanır."
        ),
        "medicalTerms": [
            {"term": "Sınıf 2 LDLR Mutasyonu", "explanation": "LDL reseptörünün ER'de sentezlenip Golgi'ye taşınamadan yıkıldığı mutasyon sınıfıdır."},
            {"term": "Heksozaminidaz Alfa Alt Birimi", "explanation": "Tay-Sachs hastalığında katlanma kusuru veya delesyon gösteren enzim alt birimidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ailesel hiperkolesterolemi Sınıf 2 mutasyonlarında LDLR, ER'den çıkamaz ve yıkılır.",
            "📌 [SINAV SPOTU] Tay-Sachs'ta heksozaminidaz alfa alt birimi eksikliği GM2 gangliozid biriktirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "LDLR Taşınma Hatası", "desc": "Reseptör plazma membranına gidemez, klirens sıfırlanır.", "isKey": True},
                {"title": "Heksozaminidaz Hatası", "desc": "Enzim lizozoma ulaşamaz, nöronal lipid depolanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "CFTR vs LDLR Yanlış Katlanma Mekanizması",
                "CFTR (Kistik Fibrozis)",
                "Klor kanalı ER'de hatalı katlanır; ERAD ile proteazomda erken yıkılır ve epitelde salgı koyulaşması yapar.",
                "LDLR (Ailesel Hiperkolesterolemi)",
                "LDL reseptörü ER'de yanlış katlanıp takılır; hücre zarına çıkamadığı için plazma LDL'si temizlenemez ve damarı tıkar."
            ),
            make_active_recall(
                "Ailesel hiperkolesterolemide Sınıf 2 mutasyonların ortak moleküler özelliği nedir?",
                "LDL reseptör proteininin ER'de yanlış katlanması nedeniyle Golgi aygıtına ve hücre yüzeyine taşınamadan ER'de yıkılmasıdır."
            )
        ]
    })

    # ADIM 46
    slides.append({
        "slideNumber": 46,
        "title": "Retinitis Pigmentosa (Rodopsin) ve Nöronal ER Stresi / Hücre Kaybı",
        "subtitle": "Fotoreseptör apoptozu, gece körlüğü ve ilerleyici tünel görme defekti",
        "badge": "Retinitis Pigmentosa",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "İkinci hastalık grubunda patoloji eksiklikten ziyade yanlış katlanan proteinin hücrede yarattığı toksik ER "
            "stresi ve buna bağlı hücre ölümüdür. Bunun klasik modeli otozomal dominant retinitis pigmentosadır. "
            "Retinadaki çubuk (rod) hücrelerinde rodopsin pigment geninde meydana gelen mutasyonlar yanlış katlanmış "
            "anormal rodopsin üretimine yol açar.\n\n"
            "> [SINAV SPOTU] Anormal rodopsin ER'den çıkamaz, fotoreseptör hücre ER'sinde birikerek kronik ER stresini ve "
            "apoptozu tetikler; fotoreseptör hücre kaybı ilerleyici körlüğe neden olur.\n\n"
            "Hastalar başlangıçta gece körlüğü (niktalopi), ardından çevre görme kaybı (tünel görme) ve nihayetinde tam görme kaybı yaşar."
        ),
        "medicalTerms": [
            {"term": "Retinitis Pigmentosa", "explanation": "Mutant rodopsinin ER stresiyle fotoreseptör apoptozuna yol açtığı genetik körlük tablosudur."},
            {"term": "Rodopsin", "explanation": "Retina çubuk hücrelerinde loş ışık algısını sağlayan G protein kenetli fotopigmenttir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Retinitis pigmentosada rodopsin yanlış katlanması ER stresiyle fotoreseptör ölümüne yol açar.",
            "📌 [SINAV SPOTU] Patogenezde primer olay eksiklik değil, hücrenin apoptozla kaybıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hatalı Pigment", "desc": "Rodopsin tersiyer yapısını kazanamaz ve ER'de hapsolur.", "isKey": True},
                {"title": "Fotoreseptör Ölümü", "desc": "CHOP indüksiyonu ile rod ve koni hücreleri apoptoza gider.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Retinitis pigmentosa tablosunda mutant rodopsin proteini fotoreseptörlerde ER stresi tetikleyerek hücre ölümüne yol açar.",
                "ER stresi",
                "Hatalı katlanan proteinin organelde oluşturduğu apoptotik gerilim"
            ),
            make_active_recall(
                "Retinitis pigmentosada körlüğe yol açan temel patolojik süreç nedir?",
                "Mutant rodopsinin ER'de birikip ER stresini ve fotoreseptör hücre apoptozunu tetiklemesi sonucu fotoreseptörlerin geri dönüşsüz kaybıdır."
            )
        ]
    })

    # ADIM 47
    slides.append({
        "slideNumber": 47,
        "title": "Creutzfeldt-Jakob Hastalığı (CJD): Prion Proteini Konformasyonel Değişimi",
        "subtitle": "PrPC'den PrPSc'ye beta kırmalı bükülme, bulaşıcılık ve spongioform vakuolizasyon",
        "badge": "Prion Hastalıkları",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Prion hastalıkları (Creutzfeldt-Jakob, Kuru, deli dana), tıp tarihindeki en sıra dışı protein katlanma "
            "patolojisidir. Normalde nöron membranında alfa-heliks zengini fizyolojik hücresel prion proteini (PrPC) "
            "bulunur. Patolojik durumda bu protein konformasyonel olarak beta-kırmalı (beta-pleated sheet) dayanıklı bir "
            "yapıya bükülerek PrPSc (scrapie formu) haline gelir.\n\n"
            "> [KRİTİK UYARI] PrPSc bir şablon gibi davranarak temas ettiği diğer normal PrPC moleküllerini de kendi "
            "hatalı formuna bükülmeye zorlar; proteazlara aşırı dirençli bu agregatlar nöronları öldürür.\n\n"
            "Serebral kortekste süngerimsi (spongioform) vakuolizasyon ve hızlı seyirli ölümcül demans tablosu gelişir."
        ),
        "medicalTerms": [
            {"term": "PrPC", "explanation": "Nöronlarda doğal olarak bulunan, alfa heliks zengini, proteazlara duyarlı normal hücresel prion proteinidir."},
            {"term": "PrPSc", "explanation": "Beta kırmalı, proteaz dirençli, bulaşıcı ve nörotoksik patolojik prion formudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Prion hastalığında nükleik asit yoktur; patoloji konformasyonel beta kırmalı protein bükülmesidir.",
            "📌 [SINAV SPOTU] CJD histolojisinde nöropilde süngerimsi (spongioform) boşluklar ve nöron ölümü izlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Konformasyonel Dönüşüm", "desc": "Alfa heliks yapısından beta kırmalı çözünmez forma geçiş.", "isKey": True},
                {"title": "Spongioform Dejenerasyon", "desc": "Korteks nöronlarında mikrovakuoler lizis ve gliozis.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Fizyolojik PrPC vs Patojenik PrPSc",
                "Fizyolojik PrPC",
                "Alfa heliks zengini, monomerik, proteinaz K ile kolayca parçalanabilen, normal nöronal membran proteini.",
                "Patojenik PrPSc",
                "Beta kırmalı yapıda, yüksek derecede agregasyon oluşturan, proteazlara son derece dirençli bulaşıcı prion formu."
            ),
            make_active_recall(
                "Creutzfeldt-Jakob hastalığında normal prion proteinini patolojik forma dönüştüren temel fiziksel-kimyasal değişim nedir?",
                "Alfa-heliks yapısının çözünmeyen ve proteazlara dirençli beta-kırmalı (beta-sheet) konformasyona bükülmesidir."
            )
        ]
    })

    # ADIM 48
    slides.append({
        "slideNumber": 48,
        "title": "α1-Antitripsin Eksikliği: Hem ER Stresi Hem Fonksiyon Kaybı",
        "subtitle": "SERPINA1 mutasyonu (PiZZ), hepatosit ER'sinde PAS(+) granüller ve pulmoner amfizem",
        "badge": "AAT Eksikliği",
        "badgeColor": "red",
        "synthesisNarrative": (
            "α1-Antitripsin (AAT) eksikliği, yanlış katlanmış protein hastalıklarının her iki mekanizmasını birden "
            "kusursuz şekilde sergileyen en klasik modeldir. Normalde SERPINA1 geni tarafından kodlanan AAT karaciğerde "
            "üretilip kana salınır ve akciğerde nötrofil elastazını nötralize ederek alveol elastik liflerini korur. "
            "PiZZ mutasyonunda üretilen protein yanlış katlanır ve hepatosit ER'sinden salınamaz.\n\n"
            "> [SINAV SPOTU] Karaciğerde: ER'de biriken mutant AAT polimerleri ER stresi, hepatosit apoptozu ve siroza "
            "yol açar; histolojide hepatositlerde diyastaza dirençli PAS pozitif yuvarlak globüller izlenir.\n\n"
            "> [SINAV SPOTU] Akciğerde: Kanda AAT bulunmadığından kontrolsüz nötrofil elastazı alveol duvarlarını parçalar "
            "ve panasinüs amfizemine neden olur."
        ),
        "medicalTerms": [
            {"term": "α1-Antitripsin (AAT)", "explanation": "Nötrofil elastazını inhibe ederek akciğer parankimini koruyan serin proteaz inhibitörüdür."},
            {"term": "PiZZ Genotipi", "explanation": "AAT geninde glutamat yerine lizin geçişiyle mutant proteinin ER'de polimerleştiği homozigot tablodur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] AAT eksikliğinde karaciğerde ER stresi ve siroz; akciğerde elastaz aktivitesiyle amfizem gelişir.",
            "📌 [SINAV SPOTU] Hepatosit sitoplazmasındaki AAT globülleri diyastaz sindirimine dirençli PAS(+) boyanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Karaciğer Patolojisi", "desc": "Mutant proteinin ER'de birikimi, ER stresi, siroz ve PAS(+) granüller.", "isKey": True},
                {"title": "Akciğer Patolojisi", "desc": "Plazma proteaz inhibitör yokluğu, kontrolsüz elastaz, panasinüs amfizem.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "AAT Eksikliğinde İki Yönlü Patoloji Mekanizması",
                [
                    "1. PiZZ Mutasyonu: SERPINA1 geninde tek amino asit değişimi proteinin katlanmasını bozar.",
                    "2. ER Polimerizasyonu: Mutant AAT molekülleri hepatosit granüllü ER'sinde kümeleşir.",
                    "3. Hepatosit Hasarı: ER stresi ve apoptoz zamanla kronik hepatit ve karaciğer sirozuna yol açar.",
                    "4. Plazma Eksikliği: Kana AAT salınamadığı için serum proteaz inhibitör seviyesi çöker.",
                    "5. Pulmoner Amfizem: Alveollerde nötrofil elastazı frenlenemez ve elastik septumları eriterek amfizem yapar."
                ]
            ),
            make_cloze(
                "α1-Antitripsin eksikliğinde hepatosit sitoplazmasında biriken eozinofilik küreler PAS pozitif boyanır.",
                "PAS pozitif",
                "Glikoprotein yapısını gösteren periyodik asit-Schiff reaksiyonu"
            )
        ]
    })

    # ADIM 49 - CHECKPOINT 5
    slides.append({
        "slideNumber": 49,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Yanlış Katlanmış Protein Hastalıkları Tablosu",
        "subtitle": "Kistik fibrozis, LDLR, prion, retinitis pigmentosa ve AAT'nin büyük sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 5,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında Robbins Tablo 1.4 kapsamındaki yanlış katlanmış protein hastalıklarını "
            "özetliyoruz. 1) Erken yıkım ve eksiklik grubu: Kistik fibrozis (CFTR kaybı ile iyon blokajı), Ailesel "
            "hiperkolesterolemi (LDLR kaybı ile hiperkolesterolemi), Tay-Sachs (Heksozaminidaz A yokluğu ile gangliozid birikimi). "
            "2) ER stresi ve hücre kaybı grubu: Retinitis pigmentosa (mutant rodopsin ile fotoreseptör apoptozu), "
            "Creutzfeldt-Jakob (PrPSc ile süngerimsi nöron ölümü). 3) Her iki mekanizma: α1-antitripsin eksikliği "
            "(hepatositte birikimle siroz, kanda eksiklikle amfizem).\n\n"
            "> [KLİNİK İPUCU] Karaciğer biyopsisinde PAS(+) diyastaz dirençli küreler daima AAT eksikliğini akla getirmelidir.\n\n"
            "Aşağıdaki 3 akıl kartını hafızanıza sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Diyastaz Dirençli PAS", "explanation": "Glikojeni eriten amilaz (diyastaz) uygulandığında boyanmayı sürdüren AAT granüllerinin özelliğidir."},
            {"term": "Spongioform Dejenerasyon", "explanation": "Prion hastalıklarında kortikal nöropilde izlenen mikrovakuoler vakuolizasyondur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] CFTR ve LDLR mutant proteinin erken yıkımıyla giden eksiklik hastalıklarıdır.",
            "📌 [SINAV SPOTU] AAT eksikliği hem karaciğerde ER stresi/siroz hem akciğerde elastaz aracılı amfizem yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Eksiklik", "desc": "CFTR, LDLR, Heksozaminidaz A.", "isKey": True},
                {"title": "ER Toksisitesi", "desc": "Rodopsin, PrPSc.", "isKey": True},
                {"title": "Kombine Model", "desc": "SERPINA1 / AAT eksikliği.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-13",
                "Kistik fibroziste mutant CFTR proteininin hücresel zedelenmeye yol açan temel kaderi nedir?",
                "ER kalite kontrol sistemleri tarafından yanlış katlanmış olarak tanınması ve plazma zarına ulaşamadan proteazomda erkenden yıkılmasıdır.",
                "CFTR erken yıkımı ve fonksiyonel klor kanalı yokluğu"
            ),
            make_flashcard(
                "k1-07-fc-14",
                "α1-Antitripsin eksikliğinde karaciğer hasarı ile akciğer amfizeminin mekanizmaları arasındaki temel fark nedir?",
                "Karaciğerde mutant protein ER'de birikip ER stresi ve apoptoz yapar; akciğerde ise kanda inhibitör bulunmadığından kontrolsüz nötrofil elastazı dokuyu yıkar.",
                "Karaciğerde toksik birikim, akciğerde fonksiyonel eksiklik"
            ),
            make_flashcard(
                "k1-07-fc-15",
                "Creutzfeldt-Jakob prion hastalığında hücresel hasara yol açan temel biyofiziksel dönüşüm nedir?",
                "Normal hücresel prion proteininin (PrPC) proteazlara dirençli ve beta-kırmalı patolojik forma (PrPSc) yanlış bükülerek birikmesidir.",
                "Prion proteini konformasyonel beta dönüşümü"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "α1-Antitripsin eksikliği olan hastaların karaciğer biyopsisinde diyastaza dirençli PAS pozitif küresel granüller izlenir.",
                "PAS pozitif",
                "Karaciğerde biriken AAT glikoproteininin histokimyasal boyanma özelliği"
            )
        ]
    })

    # ADIM 50
    slides.append({
        "slideNumber": 50,
        "title": "Yanlış Katlanma Hastalıklarında Terapötik Yaklaşımlar ve Moleküler Sentez",
        "subtitle": "Farmakolojik şaperonlar, translasyon düzenleyiciler ve proteostaz hedefleri",
        "badge": "Terapötik Sentez",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Yanlış katlanmış protein hastalıklarının moleküler mekanizmalarının aydınlatılması, modern tıpta devrim "
            "niteliğinde yeni tedavi stratejileri doğurmuştur. Özellikle kistik fibroziste kullanılan 'kırıcılar' "
            "(correctors: örneğin Lumakaftor, Eleksakaftor) mutant CFTR'nin ER'de doğru katlanmasına yardım eden "
            "farmakolojik şaperonlar gibi davranarak proteinin proteazomdan kaçıp hücre zarına çıkmasını sağlar.\n\n"
            "> [KLİNİK İPUCU] α1-Antitripsin eksikliğinde ise akciğer hasarı için intravenöz AAT enzim replasmanı, "
            "karaciğerdeki toksik birikim içinse gen susturma (RNAi) tedavileri araştırılmaktadır.\n\n"
            "Bu hedefe yönelik yaklaşımlar, patolojinin doğrudan moleküler tedaviye dönüştüğü en somut örneklerdir."
        ),
        "medicalTerms": [
            {"term": "Farmakolojik Şaperon", "explanation": "Mutant proteine bağlanarak onun doğru üç boyutlu yapısını stabilize eden ve yıkımdan koruyan küçük moleküllerdir."},
            {"term": "Proteostaz", "explanation": "Hücre içindeki tüm proteinlerin sentez, katlanma, taşınma ve yıkım dengesini ifade eden homeostaz ağıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Farmakolojik düzelticiler (correctors) CFTR'nin ER'den kaçıp hücre zarına gitmesini sağlar.",
            "📌 [SINAV SPOTU] AAT eksikliğinde amfizem için AAT infüzyonu yapılırken siroz için karaciğer nakli gerekebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Düzeltici Tedavi", "desc": "Proteinin doğru katlanmasını sağlayarak zarda işlev görmesini sağlama.", "isKey": True},
                {"title": "Enzim İnfüzyonu", "desc": "Eksik dolaşım proteininin dışarıdan rekombinant olarak verilmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "32 yaşında sigara içmeyen bir hasta nefes darlığı ve sarılık şikayetiyle başvuruyor. Akciğer grafisinde alt loblarda belirgin panasinüs amfizemi, karaciğer biyopsisinde ise hepatosit ER'sinde PAS(+) diyastaza dirençli inklüzyonlar ve erken siroz bulguları saptanıyor. En olası tanı ve mekanizma nedir?",
                [
                    {
                        "text": "Kistik fibrozis: CFTR kanalının akciğer ve karaciğerde aşırı kalsiyum pompalaması",
                        "isCorrect": False,
                        "feedback": "Kistik fibroziste amfizemden çok bronşiektazi görülür ve PAS(+) granüller izlenmez."
                    },
                    {
                        "text": "α1-Antitripsin eksikliği (PiZZ): Karaciğerde ER'de mutant protein birikimi, akciğerde elastaz frenlenememesi",
                        "isCorrect": True,
                        "feedback": "Mükemmel! Karaciğerde PAS(+) AAT globülleri ve genç yaşta amfizem birlikteliği α1-antitripsin eksikliğinin patognomonik tablosudur."
                    }
                ]
            ),
            make_active_recall(
                "Modern tıpta kistik fibrozis tedavisinde kullanılan farmakolojik şaperonların (düzelticilerin) çalışma mekanizması nedir?",
                "Mutant CFTR proteinine bağlanarak onun doğru üç boyutlu konformasyona katlanmasını sağlamak ve ER'de erkenden parçalanmasını önleyerek hücre zarına ulaşmasını sağlamaktır."
            )
        ]
    })

    return slides
