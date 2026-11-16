"""
Bölüm 7: Ölüm Reseptörü (Dışsal) Yolu ve Kaspaz Kaskadı
Adımlar: 61 - 70
Checkpoint: Adım 69 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_7_slides():
    slides = []

    # ADIM 61
    slides.append({
        "slideNumber": 61,
        "title": "Ölüm Reseptörü (Dışsal) Yolu: Dış Dünyadan Gelen İntihar Emri",
        "subtitle": "Plazma zarı ölüm reseptörleri aracılığıyla başlatılan hücre dışı apoptoz sinyali",
        "badge": "Dışsal Yol",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun mitokondriyal yolu hücrenin kendi iç krizlerini dinlerken, 'Ölüm Reseptörü (Dışsal) Yolu' "
            "doğrudan komşu hücrelerden veya bağışıklık sisteminden gelen infaz emirlerini yürütür.\n\n"
            "Bu yolak, hücrenin plazma membranında yer alan özelleşmiş 'Ölüm Reseptörleri' (Death Receptors) "
            "tarafından başlatılır. Bu reseptörler Tümör Nekroz Faktörü Reseptör (TNFR) süperailesinin üyeleridir.\n\n"
            "> [SINAV SPOTU] Ölüm reseptörlerinin ortak yapısal özelliği, sitoplazmik kuyruklarında yaklaşık "
            "80 aminoasitlik korunmuş bir 'Ölüm Alanı' (Death Domain - DD) barındırmalarıdır!\n\n"
            "Ligand bağlandığında bu ölüm alanları bir araya gelerek sitoplazmadaki adaptör proteinleri çeker ve "
            "ölüm makinesini çalıştırır."
        ),
        "medicalTerms": [
            {"term": "Ölüm Reseptörü (Death Receptor)", "explanation": "Ligand bağlandığında sitoplazmik ölüm alanı (DD) aracılığıyla apoptoz sinyali ileten transmembran reseptör."},
            {"term": "Ölüm Alanı (Death Domain - DD)", "explanation": "Ölüm reseptörleri ve adaptör proteinlerin sitoplazmik kuyruğundaki protein-protein etkileşim bölgesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dışsal yol plazma membranındaki 'Ölüm Reseptörleri' ile tetiklenir.",
            "📌 [SINAV SPOTU] Ölüm reseptörlerinin sitoplazmik kuyruğunda 'Ölüm Alanı' (Death Domain - DD) bulunur.",
            "📌 [SINAV SPOTU] En iyi bilinen ölüm reseptörleri Fas (CD95) ve Tip I TNF Reseptörüdür (TNFR1)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dışsal Tetikleme", "desc": "Hücre zarına bağlanan ligandlarla gelen apoptoz emri.", "isKey": True},
                {"title": "Ölüm Alanı (DD)", "desc": "Sitoplazmada adaptör proteinleri toplayan anahtar yapı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Ölüm Reseptörü", "Alternatif Adı / Aile", "Bağlandığı Spesifik Ligand"],
                [
                    [("Fas", False, ""), ("CD95 / APO-1", True, "Yüzey diferansiasyon antijeni"), ("Fas Ligandı (FasL / CD95L)", False, "")],
                    [("Tip I TNF Reseptörü", False, ""), ("TNFR1 / CD120a", True, "Sitokin reseptör ailesi"), ("Tümör Nekroz Faktörü-alfa (TNF-α)", False, "")],
                    [("TRAIL-R1 / TRAIL-R2", False, ""), ("DR4 / DR5", True, "Ölüm reseptörü kısaltmaları"), ("TRAIL (Apo2L)", False, "")]
                ]
            ),
            make_cloze(
                "Ölüm reseptörlerinin sitoplazmik kuyruklarında adaptör proteinlerle etkileşimi sağlayan bölgeye ölüm alanı veya Death Domain denir.",
                "ölüm alanı",
                "Reseptör sitoplazmik kuyruğundaki 80 aminoasitlik etkileşim bölgesi"
            )
        ]
    })

    # ADIM 62
    slides.append({
        "slideNumber": 62,
        "title": "Fas (CD95) ve FasL Etkileşimi: Aktive T Hücrelerinin Silahı",
        "subtitle": "Trimerizasyon ile kurulan reseptör kümelenmesi ve otoimmünite kontrolü",
        "badge": "Fas-FasL",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dışsal yolun en karakteristik prototipi 'Fas (CD95)' reseptörüdür. Fas proteini vücuttaki pek çok "
            "hücre tipinin yüzeyinde daima hazır bulunur. Onun eşi olan 'Fas Ligandı (FasL)' ise kural olarak "
            "aktive olmuş T lenfositlerin (özellikle sitotoksik ve regülatuvar T hücreleri) yüzeyinde eksprese edilir.\n\n"
            "Aktive T hücresi hedef hücreye temas ettiğinde, membranındaki üç adet FasL molekülü hedef hücredeki "
            "üç adet Fas reseptörünü bir araya getirerek çapraz bağlar (trimerizasyon).\n\n"
            "> [SINAV SPOTU] Fas reseptörlerinin zarda trimerize olması, hücre içindeki ölüm alanlarını (DD) yan yana "
            "getirerek adaptör proteinler için yüksek afiniteli bir çekim üssü oluşturur!\n\n"
            "Bu mekanizma otoreaktif lenfositlerin elenmesinde ve tümör hücrelerinin yok edilmesinde birincil araçtır."
        ),
        "medicalTerms": [
            {"term": "Fas (CD95)", "explanation": "Plazma zarında bulunan ve FasL bağlandığında trimerleşerek apoptozu başlatan ölüm reseptörü."},
            {"term": "Trimerizasyon", "explanation": "Üç reseptör monomerinin ligand etkisiyle bir araya gelip kümelenmesi olayı."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fas (CD95) reseptörünün ligandı FasL'dir (aktive T lenfositlerde bulunur).",
            "📌 [SINAV SPOTU] FasL bağlanması Fas reseptörlerinin trimerizasyonuna (3'lü kümelenme) yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Reseptör-Ligand Eşleşmesi", "desc": "CD95 ile FasL arasındaki yüksek özgüllüklü temas.", "isKey": True},
                {"title": "Trimerik Tetikleme", "desc": "Üçlü kümelenmenin hücre içine ölüm sinyali yayması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Fas (CD95) reseptörüne bağlanan Fas Ligandı (FasL) başlıca hangi hücrelerin yüzeyinde yer alır?",
                "Aktive olmuş T lenfositlerin (sitotoksik T lenfositler ve efektör T hücreleri) yüzeyinde bulunur."
            ),
            make_cloze(
                "Fas ligandının bağlanması sonucu hedef hücre zarındaki Fas reseptörleri trimerizasyon ile üçlü kümeler oluşturur.",
                "trimerizasyon",
                "Üç molekülün bir araya gelmesi terimi"
            )
        ]
    })

    # ADIM 63
    slides.append({
        "slideNumber": 63,
        "title": "DISC Kompleksi: Ölüm İndükleyici Sinyal Platformu",
        "subtitle": "FADD adaptörü aracılığıyla Prokaspaz-8 moleküllerinin reseptör altına dizilmesi",
        "badge": "DISC",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Fas reseptörleri trimerize olduğunda, sitoplazmik kuyruklarındaki ölüm alanları (DD) sitozolde serbest "
            "dolaşan 'FADD' (Fas-Associated Death Domain) adlı adaptör proteini yakalar. FADD kendi ölüm alanı ile "
            "reseptörün ölüm alanına kenetlenir.\n\n"
            "FADD proteininin diğer ucunda ise 'Ölüm Efektör Alanı' (Death Effector Domain - DED) bulunur. "
            "Bu DED alanı, inaktif 'Prokaspaz-8' (ve Prokaspaz-10) moleküllerinin DED domainlerini mıknatıs gibi çeker.\n\n"
            "> [SINAV SPOTU] Fas reseptörü + FADD adaptörü + Prokaspaz-8 birleşimiyle oluşan bu transmembran "
            "komplekse 'DISC' (Death-Inducing Signaling Complex / Ölüm İndükleyici Sinyal Kompleksi) adı verilir!\n\n"
            "DISC platformu, prokaspaz-8'in kendi kendini keserek aktive olacağı infaz iskelesidir."
        ),
        "medicalTerms": [
            {"term": "FADD", "explanation": "Fas ile İlişkili Ölüm Alanı; Fas reseptörü ile Prokaspaz-8 arasında köprü kuran adaptör protein."},
            {"term": "DISC Kompleksi", "explanation": "Ölüm İndükleyici Sinyal Kompleksi (Death-Inducing Signaling Complex); dışsal yolağın aktivasyon üssü."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Trimerize Fas, adaptör protein FADD aracılığıyla DISC (Death-Inducing Signaling Complex) kompleksini kurar.",
            "📌 [SINAV SPOTU] DISC kompleksi Prokaspaz-8'i toplayarak aktive eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "FADD Köprüsü", "desc": "Ölüm alanı (DD) ve ölüm efektör alanı (DED) arasındaki adaptör geçiş.", "isKey": True},
                {"title": "DISC Montajı", "desc": "Plazma zarı altında kaspaz-8 aktivasyon platformunun kurulması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "DISC Kompleksi Kurulum ve Aktivasyon Zinciri",
                [
                    "1. FasL Bağlanması: Fas Ligandı plazma zarındaki Fas reseptörlerini trimerize eder.",
                    "2. FADD Kenetlenmesi: Reseptörün sitoplazmik DD alanı FADD adaptör proteinini bağlar.",
                    "3. Prokaspaz-8 Çekimi: FADD'ın DED alanı inaktif Prokaspaz-8 moleküllerini toplar.",
                    "4. DISC Oluşumu: Reseptör-FADD-Prokaspaz üçlüsü DISC kompleksini tamamlar.",
                    "5. Otolitik Kesim: Prokaspaz-8 molekülleri birbirini keserek aktif Kaspaz-8 üretir."
                ]
            ),
            make_cloze(
                "Fas reseptörü ile adaptör protein FADD ve prokaspaz-8'in oluşturduğu komplekse DISC veya ölüm indükleyici sinyal kompleksi denir.",
                "DISC",
                "Ölüm indükleyici sinyal kompleksi İngilizce kısaltması"
            )
        ]
    })

    # ADIM 64
    slides.append({
        "slideNumber": 64,
        "title": "Başlatıcı Kaspaz-8 ve Kaspaz-10: Dışsal Yolağın Kesim Motorları",
        "subtitle": "DISC iskelesinde oto-aktivasyonla üretilen heterodimer kaspazlar",
        "badge": "Kaspaz-8",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Mitokondriyal yolda Apaptozom nasıl Kaspaz-9'u devreye sokuyorsa; dışsal yolda da DISC platformu "
            "'Başlatıcı Kaspaz-8'i (ve Kaspaz-10'u) aktive eder.\n\n"
            "DISC üzerinde yüksek yoğunlukta yan yana dizilen prokaspaz-8 monomerleri 'yakınlık indüksiyonu' "
            "(induced proximity) ile karşılıklı olarak birbirlerini spesifik aspartat bölgelerinden keserler. "
            "Ayrılan küçük ve büyük alt birimler bir araya gelerek tam aktif Kaspaz-8 tetramerini oluşturur.\n\n"
            "> [SINAV SPOTU] Dışsal (ölüm reseptörü) yolunun BAŞLATICI kaspazı KASPAZ-8'dir (ve Kaspaz-10).\n\n"
            "Aktif Kaspaz-8 serbest kalarak sitoplazmaya dağılır ve aşağıdaki iki kritik rotayı ateşler: Doğrudan "
            "Kaspaz-3'ü keser veya Bid proteinini keserek mitokondriyal yolu da savaşa katar!"
        ),
        "medicalTerms": [
            {"term": "Kaspaz-8", "explanation": "DISC kompleksi üzerinde aktive olan dışsal (ölüm reseptörü) yol başlatıcı kaspazı."},
            {"term": "Kaspaz-10", "explanation": "İnsanlarda Kaspaz-8 ile birlikte dışsal yolda başlatıcı rol oynayan homolog kaspaz."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ölüm reseptörü (dışsal) yolağının BAŞLATICI kaspazı KASPAZ-8'dir.",
            "📌 [SINAV SPOTU] İçsel yolda Kaspaz-9; Dışsal yolda Kaspaz-8 başlatıcıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dışsal Başlatıcı", "desc": "DISC platformunun ürettiği aktif proteaz enzimi.", "isKey": True},
                {"title": "İkili Rota", "desc": "Doğrudan efektörleri kesme veya mitokondriye köprü kurma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Apoptoz Yolağı", "Başlatıcı Kaspaz", "Aktivasyon Platformu / Kompleks"],
                [
                    [("Mitokondriyal (İçsel) Yol", False, ""), ("Kaspaz-9", True, "İçsel yol başlatıcısı"), ("Apaptozom (Sitokrom c + APAF-1)", False, "")],
                    [("Ölüm Reseptörü (Dışsal) Yol", False, ""), ("Kaspaz-8 ve Kaspaz-10", True, "Dışsal yol başlatıcısı"), ("DISC Kompleksi (Fas + FADD)", False, "")],
                    [("Ortak İnfaz Evresi", False, ""), ("Kaspaz-3, -6, -7 (Efektör)", True, "Yıkımı yapan infazcılar"), ("Sitoplazma geneli", False, "")]
                ]
            ),
            make_cloze(
                "Ölüm reseptörü yani dışsal apoptoz yolunun temel başlatıcı kaspazı kaspaz-8 enzimidir.",
                "kaspaz-8",
                "Dışsal yolağın başlatıcı kaspaz numarası"
            )
        ]
    })

    # ADIM 65
    slides.append({
        "slideNumber": 65,
        "title": "FLIP Proteini: Dışsal Yolun Fizyolojik ve Viral Freni",
        "subtitle": "Kaspaz aktivitesi olmayan sahte prokaspaz molekülünün DISC'i bloke etmesi",
        "badge": "FLIP",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücrelerin ölüm reseptörlerine gelen her zayıf sinyalle hemen apoptoza gitmesini engelleyen kilit "
            "bir moleküler kontrolör vardır: 'FLIP' (FLICE-Inhibitory Protein).\n\n"
            "FLIP proteini yapısal olarak Prokaspaz-8'e inanılmaz derecede benzer; DED ölüm efektör alanlarına "
            "sahiptir ancak aktif proteaz bölgesinde katalitik sistein aminoasidini taşımaz!\n\n"
            "> [SINAV SPOTU] FLIP gidip FADD adaptörüne bağlanır; Prokaspaz-8'in DISC'e bağlanmasını yarışmalı "
            "(kompetitif) olarak bloke eder. Böylece dışsal apoptoz yolu frenlenir!\n\n"
            "Pek çok onkojenik virüs (özellikle Herpesvirüsler) ve dirençli kanser hücreleri bol miktarda v-FLIP "
            "(viral FLIP) üreterek sitotoksik T hücrelerinin FasL ile verdiği ölüm emrinden kaçarlar."
        ),
        "medicalTerms": [
            {"term": "FLIP (c-FLIP)", "explanation": "Kaspaz-8'i taklit eden ancak enzimatik gücü olmayan, DISC'i tıkayarak dışsal apoptozu durduran protein."},
            {"term": "Viral FLIP (v-FLIP)", "explanation": "Virüslerin konak hücresinde apoptozdan kaçmak için ürettiği sahte kaspaz-8 inhibitörü."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] FLIP proteini Prokaspaz-8'e bağlanıp bloke ederek dışsal apoptozu engeller.",
            "📌 [SINAV SPOTU] Virüsler ve tümör hücreleri FLIP üreterek T hücresi infazından kurtulur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yarışmalı Blokaj", "desc": "Sahte DED alanı ile Kaspaz-8'in yerine DISC'e oturma.", "isKey": True},
                {"title": "Viral Kaçış", "desc": "v-FLIP moleküllerinin tümör ve virüsleri apoptozdan koruması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Kaspaz-8 Aktivasyonu vs FLIP Engeli",
                "FLIP Yokluğunda",
                "Prokaspaz-8 serbestçe DISC'e bağlanır, dimerleşir, Kaspaz-8 aktifleşir ve hücre apoptoza gider.",
                "FLIP Varlığında",
                "FLIP DISC'e oturarak Prokaspaz-8'i kovar; katalitik aktivite olmadığı için apoptoz durdurulur ve hücre yaşar."
            ),
            make_cloze(
                "Dışsal apoptoz yolağında prokaspaz-8'e benzeyerek DISC kompleksini bloke eden koruyucu proteine FLIP denir.",
                "FLIP",
                "Dışsal yolun kaspaz aktivitesiz sahte inhibitör proteini adı"
            )
        ]
    })

    # ADIM 66
    slides.append({
        "slideNumber": 66,
        "title": "İki Yol Arasındaki Köprü: Bid Proteini ve tBid Çapraz Geçişi",
        "subtitle": "Kaspaz-8'in BH3-only Bid'i keserek mitokondriyal yolağı da savaşa sokması",
        "badge": "Çapraz Geçiş",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dışsal ve içsel apoptoz yolakları birbirinden tamamen bağımsız iki izole ada değildir. Karaciğer gibi "
            "bazı dokularda (Tip II hücreler), tek başına Kaspaz-8 aktivitesi hücreyi öldürmek için yeterli olmayabilir. "
            "Bu durumda iki yol arasında muazzam bir amplifikasyon köprüsü kurulur.\n\n"
            "Aktif Kaspaz-8, sitoplazmada inaktif bekleyen bir BH3-only proteini olan 'Bid' molekülünü proteolitik "
            "olarak keser. Kesilen aktif parçaya 'tBid' (truncated Bid / budanmış Bid) adı verilir.\n\n"
            "> [SINAV SPOTU] tBid sitozolden mitokondriye uçar, BAX ve BAK'ı doğrudan uyarır ve mitokondri dış "
            "membranından sitokrom c salınmasını tetikler!\n\n"
            "Böylece dışsal yoldan gelen bir sinyal, içsel mitokondriyal yolu da devreye sokarak infaz sinyalini yüzlerce kat büyütür."
        ),
        "medicalTerms": [
            {"term": "Bid", "explanation": "BH3-only ailesi üyesi; Kaspaz-8 tarafından kesilerek içsel yolu aktive eden aracı protein."},
            {"term": "tBid (Truncated Bid)", "explanation": "Bid'in kesilmiş aktif formu; mitokondriye giderek BAX/BAK'ı açan moleküler köprü."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kaspaz-8 proapoptotik Bid proteinini keserek aktif tBid'e dönüştürür.",
            "📌 [SINAV SPOTU] tBid mitokondriyal yolağı (BAX/BAK) aktive eder; böylece dışsal yol içsel yolu amplifiye eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Budanmış Bid (tBid)", "desc": "Kaspaz-8'in kestiği hibrit mesajcı molekül.", "isKey": True},
                {"title": "Sinyal Amplifikasyonu", "desc": "Dışsal sinyalin mitokondriyi de patlatarak kesin ölüm sağlaması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Fas reseptörü uyarılan bir hepatositte Kaspaz-8 aktifleşiyor ancak hücrenin infazı için Kaspaz-8 miktarı yetersiz kalıyor. Hücre bu sinyali nasıl büyüterek apoptozu kesinleştirir?",
                [
                    {
                        "text": "Kaspaz-8 glukoz yakarak ATP sentezini artırır ve hücreyi kurtarır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Bu durum apoptozu durdurmaz ve biyolojik işlevi bu değildir."
                    },
                    {
                        "text": "Kaspaz-8 Bid proteinini tBid haline getirir; tBid mitokondriye gidip BAX/BAK üzerinden sitokrom c salarak içsel yolu da patlatır.",
                        "isCorrect": True,
                        "feedback": "Kusursuz moleküler kavrayış! tBid dışsal yol ile içsel yol arasındaki amplifikasyon köprüsüdür."
                    },
                    {
                        "text": "Hücre çekirdeği bölünerek ikiye ayrılır.",
                        "isCorrect": False,
                        "feedback": "Mitoz bölünme ile ilgisi yoktur."
                    }
                ]
            ),
            make_cloze(
                "Kaspaz-8 tarafından kesilerek mitokondriyal yoldan sitokrom c salınmasını tetikleyen BH3-only proteini Bid proteinidir.",
                "Bid",
                "Dışsal ve içsel yol arasındaki köprü BH3 proteini adı"
            )
        ]
    })

    # ADIM 67
    slides.append({
        "slideNumber": 67,
        "title": "İnfazcı (Efektör) Kaspazlar: Kaspaz-3, Kaspaz-6 ve Kaspaz-7",
        "subtitle": "Başlatıcıların emriyle hücresel yapıları sistematik biçimde yıkan infaz mangası",
        "badge": "İnfazcı Kaspazlar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hem mitokondriyal yoldan (Kaspaz-9) hem de ölüm reseptörü yolundan (Kaspaz-8) gelen sinyaller, "
            "nihai yıkımı yapacak olan 'İnfazcı / Efektör Kaspazlar' üzerinde toplanır.\n\n"
            "Bu grubun tartışmasız en güçlü ve baş aktörü 'KASPAZ-3'tür; ona Kaspaz-6 ve Kaspaz-7 eşlik eder. "
            "Başlatıcı kaspazlar bu infazcı prokaspazların koruyucu halkalarını keserek onları serbest bırakır.\n\n"
            "> [SINAV SPOTU] İnfazcı kaspazlar hücrede yüzlerce kritik hedef proteini eşzamanlı olarak keser: "
            "Nükleer laminleri parçalayarak çekirdek zarını çökertir, aktin ve tubulini keserek hücre iskeletini "
            "yıkar ve DNA onarım enzimi olan PARP'ı (Poli-ADP Riboz Polimeraz) parçalayarak onarımı imkansız kılar!\n\n"
            "Bu aşamadan sonra hücre için hiçbir kurtuluş şansı kalmaz."
        ),
        "medicalTerms": [
            {"term": "İnfazcı Kaspaz (Executioner)", "explanation": "Başlatıcı kaspazlarca aktive edilip hücresel proteinleri yıkan efektör proteazlar (Kaspaz-3, -6, -7)."},
            {"term": "PARP", "explanation": "DNA onarımında rol alan, Kaspaz-3 tarafından parçalanarak inaktive edilen nükleer enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İnfazcı (efektör) kaspazlar: KASPAZ-3, Kaspaz-6 ve Kaspaz-7'dir.",
            "📌 [SINAV SPOTU] Apoptozun ana yürütücü infazcısı KASPAZ-3'tür.",
            "📌 [SINAV SPOTU] Nükleer laminleri keserek nükleer bütünlüğü bozar, PARP'ı keserek DNA onarımını felç eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İnfaz Mangası", "desc": "Kaspaz-3, 6 ve 7'nin hücresel mimariyi parçalaması.", "isKey": True},
                {"title": "PARP Yıkımı", "desc": "DNA onarım mekanizmasının kasten imha edilmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Kaspaz Grubu", "Üye Enzimler", "Apoptozdaki Özel Görevi"],
                [
                    [("Başlatıcı Kaspazlar", False, ""), ("Kaspaz-8, Kaspaz-9, Kaspaz-10", True, "Tetikleyici öncüler"), ("Sinyali algılar, infazcıları keserek aktive eder", False, "")],
                    [("İnfazcı (Efektör) Kaspazlar", False, ""), ("Kaspaz-3, Kaspaz-6, Kaspaz-7", True, "Hücreyi yıkan infazcılar"), ("Lamin, sitoskeleton ve PARP'ı parçalar", False, "")],
                    [("İnflamatuar Kaspazlar", False, ""), ("Kaspaz-1, Kaspaz-4, Kaspaz-5", True, "Sitokin işleyen enzimler"), ("Piroptozda IL-1beta salgılar", False, "")]
                ]
            ),
            make_cloze(
                "Apoptozda hem içsel hem dışsal yolun aktivasyonuyla devreye giren ana infazcı efektör kaspaz kaspaz-3 enzimidir.",
                "kaspaz-3",
                "Hücreyi bütünüyle parçalayan ana efektör kaspaz numarası"
            )
        ]
    })

    # ADIM 68
    slides.append({
        "slideNumber": 68,
        "title": "DNA Merdiveni (DNA Laddering): CAD ve İnternükleozomal Parçalanma",
        "subtitle": "Kaspaz-Aktive Deoksiribonükleaz (CAD) ile 180-200 baz çiftlik oligonükleozomal kesim",
        "badge": "DNA Merdiveni",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun biyokimyasal olarak en zarif ve ayırt edici olayı nükleer DNA'nın parçalanma biçimidir. "
            "Sağlıklı hücrede 'CAD' (Kaspaz-Aktive Deoksiribonükleaz) enzimi, inhibitörü olan 'ICAD'e bağlı olarak "
            "inaktif halde tutulur.\n\n"
            "İnfazcı Kaspaz-3 aktive olduğunda gidip ICAD'i parçalar. Serbest kalan CAD enzimi hızla çekirdeğe girer. "
            "CAD, histon proteinlerinin etrafına sarılı DNA'ya dokunamaz; nükleozomlar arasındaki çıplak DNA bölgelerini keser.\n\n"
            "> [SINAV SPOTU] Nükleozomlar arası mesafe tam 180-200 baz çifti (bç) olduğundan, agaroz jel elektroforezinde "
            "DNA tam 200, 400, 600, 800 bç'lik düzenli basamaklar halinde 'DNA Merdiveni' (DNA Ladder) paterni verir!\n\n"
            "Nekrozda ise lizozomal enzimler DNA'yı rastgele parçaladığı için agaroz jelde 'yayma' (smear) görüntüsü oluşur."
        ),
        "medicalTerms": [
            {"term": "CAD (Caspase-Activated DNase)", "explanation": "ICAD kaspaz-3 ile yıkılınca aktifleşen ve nükleozomlar arası DNA'yı kesen enzim."},
            {"term": "DNA Merdiveni (DNA Laddering)", "explanation": "Agaroz jel elektroforezinde 180-200 baz çiftinin katları şeklinde oluşan apoptoza özgü basamaklı bant paterni."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Apoptozda DNA nükleozomlar arası mesafelerden 180-200 baz çiftinin katları şeklinde düzenli kesilir.",
            "📌 [SINAV SPOTU] Agaroz jel elektroforezinde 'DNA Merdiveni' (DNA Ladder) paterni oluşturur.",
            "📌 [SINAV SPOTU] Nekrozda ise DNA rastgele parçalanır ve jelde yayma (smear) görüntüsü verir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İnternükleozomal Kesim", "desc": "CAD enziminin 180-200 bç katları halinde düzenli kırıklar yapması.", "isKey": True},
                {"title": "Merdiven vs Yayma", "desc": "Apoptozda basamaklı merdiven, nekrozda kaotik yayma (smear).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Apoptoz vs Nekroz Agaroz Jel DNA Kırılma Paterni",
                "Apoptoz DNA Paterni (Merdiven)",
                "CAD enzimi internükleozomal kesim yapar. Agaroz jelde 180-200 baz çiftinin katları olan düzenli 'DNA Merdiveni' (Ladder) izlenir.",
                "Nekroz DNA Paterni (Yayma / Smear)",
                "Lizozomal enzimler DNA'yı rastgele ve kontrolsüzce parçalar. Agaroz jelde sınırsız ve düzensiz bir 'Yayma' (Smear) izlenir."
            ),
            make_cloze(
                "Apoptozda DNA'nın 180-200 baz çiftlik düzenli parçalara ayrılmasıyla agaroz jelde oluşan karakteristik görüntüye DNA merdiveni denir.",
                "DNA merdiveni",
                "Agaroz jelde basamaklar halinde görülen apoptoz paterni"
            )
        ]
    })

    # ADIM 69 (CHECKPOINT 7)
    slides.append({
        "slideNumber": 69,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Dışsal Yol, DISC ve Kaspaz Kaskadı",
        "subtitle": "Fas/FasL, FADD, DISC, Kaspaz-8, Bid köprüsü, Kaspaz-3 ve DNA merdiveninin konsolide sentezi",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 7,
        "synthesisNarrative": (
            "Bu kontrol noktasında, ölüm reseptörleri üzerinden yürütülen Dışsal Apoptoz yolağını ve "
            "hücrenin sonunu getiren infazcı kaspaz kaskadını konsolide ediyoruz.\n\n"
            "Dışsal yol plazma membranındaki Fas (CD95) veya TNFR1 reseptörlerine ligand bağlanmasıyla başlar. "
            "Reseptör trimerize olur, sitoplazmik ölüm alanı (DD) FADD adaptörünü çeker ve Prokaspaz-8 bağlanarak "
            "DISC kompleksi kurulur.\n\n"
            "> [ÖZET REÇETE] Kaspaz Komuta Zinciri:\n"
            "1. Başlatıcılar = Kaspaz-8 (dışsal) ve Kaspaz-9 (içsel)\n"
            "2. Köprü = Kaspaz-8 Bid'i keser -> tBid mitokondriyi deler\n"
            "3. İnfazcılar = KASPAZ-3, Kaspaz-6, Kaspaz-7 (lamin, aktin, PARP parçalanır)\n"
            "4. DNA Kesimi = Kaspaz-3 ICAD'i yıkar -> CAD serbest kalır -> 180-200 bç DNA Merdiveni!\n\n"
            "Nekrozda rastgele DNA yayması (smear) varken, apoptozda muntazam DNA merdiveni oluşur."
        ),
        "medicalTerms": [
            {"term": "DISC Üssü", "explanation": "Fas, FADD ve Prokaspaz-8'den oluşan zar altı aktivasyon kompleksi."},
            {"term": "CAD/ICAD Sistemi", "explanation": "Kaspaz-3 ile tetiklenen nükleozomal DNA parçalama mekanizması."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] FasL + Fas (CD95) -> FADD -> DISC -> Başlatıcı KASPAZ-8.",
            "📌 [CHECKPOINT ÖZETİ] FLIP proteini Prokaspaz-8'i bloke ederek dışsal apoptozu engeller.",
            "📌 [CHECKPOINT ÖZETİ] İnfazcı KASPAZ-3 hücresel proteinleri ve PARP'ı parçalar.",
            "📌 [CHECKPOINT ÖZETİ] İnternükleozomal kesim (180-200 bç) = DNA Merdiveni (DNA Laddering)."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-19",
                "Ölüm reseptörü (dışsal) apoptoz yolunda FasL bağlandığında kurulan DISC kompleksinin üç ana bileşeni nedir?",
                "Trimerize Fas (CD95) reseptörü, adaptör protein FADD ve inaktif Prokaspaz-8 molekülüdür."
            ),
            make_flashcard(
                "fc-k1-05-20",
                "Dışsal yol başlatıcısı olan Kaspaz-8 ile içsel mitokondriyal yol başlatıcısı olan Kaspaz-9'un birleştiği ana infazcı (efektör) kaspaz hangisidir?",
                "Kaspaz-3'tür (Kaspaz-6 ve Kaspaz-7 ile birlikte)."
            ),
            make_flashcard(
                "fc-k1-05-21",
                "Agaroz jel elektroforezinde apoptoz ile nekroz arasındaki nükleer DNA kırılma paterni farkı nasıldır?",
                "Apoptozda internükleozomal kesimle 180-200 baz çiftlik düzenli 'DNA Merdiveni' oluşurken; nekrozda rastgele lizozomal yıkım sonucu düzensiz 'Yayma' (Smear) izlenir."
            )
        ],
        "coreContent": {
            "table": {
                "title": "İçsel ve Dışsal Apoptoz Yolaklarının Karşılaştırma Matrisi",
                "headers": ["Parametre", "Mitokondriyal (İçsel) Yol", "Ölüm Reseptörü (Dışsal) Yol"],
                "rows": [
                    ["Başlatıcı Tetikleyici", "DNA hasarı, ER stresi, büyüme faktörü yokluğu", "FasL, TNF-alfa, TRAIL ligandları"],
                    ["Sensör Moleküller", "BH3-only proteinler (Bim, Puma vb.)", "Fas (CD95), TNFR1 (Ölüm Alanı / DD)"],
                    ["Aktivasyon Platformu", "Apaptozom (Sitokrom c + APAF-1)", "DISC (Fas + FADD)"],
                    ["Başlatıcı Kaspaz", "Kaspaz-9", "Kaspaz-8 ve Kaspaz-10"],
                    ["Temel Engelleyici", "BCL-2, BCL-XL, IAP", "FLIP (c-FLIP)"],
                    ["Ortak İnfazcı Kaspaz", "Kaspaz-3, Kaspaz-6, Kaspaz-7", "Kaspaz-3, Kaspaz-6, Kaspaz-7"],
                    ["DNA Parçalanması", "180-200 bç DNA Merdiveni", "180-200 bç DNA Merdiveni"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Apoptoz Bileşeni", "Aktör Molekül", "İşlevsel Tanımı"],
                [
                    [("Dışsal Yol Başlatıcı Kaspazı", False, ""), ("Kaspaz-8", True, "DISC proteazı"), ("Ölüm reseptörleri aracılığıyla aktifleşir", False, "")],
                    [("İçsel Yol Başlatıcı Kaspazı", False, ""), ("Kaspaz-9", True, "Apaptozom proteazı"), ("Apaptozom üzerinde aktifleşir", False, "")],
                    [("Ana Yürütücü İnfazcı Kaspaz", False, ""), ("Kaspaz-3", True, "Genel efektör"), ("PARP, lamin ve aktini parçalar", False, "")]
                ]
            ),
            make_active_recall(
                "Neden nekrozda DNA elektroforezinde yayma (smear) görülürken apoptozda 180-200 baz çiftlik merdiven basamakları oluşur?",
                "Çünkü apoptozda CAD enzimi histonlarla korunan nükleozomlara dokunamaz, yalnızca nükleozomlar arasındaki düzenli çıplak DNA aralıklarını keser; nekrozda ise enzimler her yeri rastgele parçalar."
            )
        ]
    })

    # ADIM 70
    slides.append({
        "slideNumber": 70,
        "title": "TUNEL Yöntemi: Apoptotik DNA Kırıklarını Floresanla Yakalama",
        "subtitle": "Terminal deoksinükleotidil transferaz ile kırık 3'-OH uçlarının işaretlenmesi",
        "badge": "Laboratuvar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Patoloji araştırmalarında ve doku biyopsilerinde apoptotik hücreleri in situ (yerinde) mikroskop "
            "altında sayabilmek için altın standart histokimyasal yöntem 'TUNEL' testidir.\n\n"
            "Açılımı 'TdT-mediated dUTP Nick End Labeling' olan bu teknik, CAD endonükleazının DNA'yı kestiğinde "
            "açığa çıkardığı milyonlarca serbest 3'-hidroksil (3'-OH) ucunu kullanır.\n\n"
            "> [SINAV SPOTU] Ekzojen olarak verilen 'TdT' (Terminal Deoksinükleotidil Transferaz) enzimi, floresan "
            "veya biotinle etiketlenmiş dUTP nükleotidlerini bu serbest 3'-OH kırık uçlarına art arda ekler!\n\n"
            "Mikroskop altında incelendiğinde apoptoz geçiren hücrelerin çekirdekleri parlak yeşil veya kahverengi "
            "olarak parlar; böylece sağlıklı hücrelerin arasında tek tük apoptoza giden hücreler kesin olarak sayılabilir."
        ),
        "medicalTerms": [
            {"term": "TUNEL Testi", "explanation": "DNA kırıklarının 3'-OH uçlarına TdT enzimiyle floresan nükleotid ekleyerek apoptotik hücreleri gösteren yöntem."},
            {"term": "TdT (Terminal Transferaz)", "explanation": "Kalıp DNA olmadan serbest 3'-OH uçlarına dNTP polimerize eden enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Doku kesitlerinde apoptotik hücreleri DNA kırıkları üzerinden saptamak için TUNEL yöntemi kullanılır.",
            "📌 [SINAV SPOTU] Yöntem serbest 3'-OH uçlarına floresan dUTP ekleyen Terminal Deoksinükleotidil Transferaz (TdT) enzimine dayanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "3'-OH Uçları", "desc": "CAD kesimiyle ortaya çıkan serbest nükleik asit kırıkları.", "isKey": True},
                {"title": "TdT Enzimi", "desc": "Kırık uçlara floresan dUTP ekleyerek çekirdeği parlatma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Doku kesitlerinde apoptoza uğrayan hücreleri internükleozomal DNA kırıklarının serbest 3'-OH uçlarına floresan işaretli dUTP ekleyerek tespit eden özel yöntem hangisidir?",
                {
                    "A": "Western Blotting",
                    "B": "TUNEL Yöntemi",
                    "C": "Southern Blotting",
                    "D": "Karyotipleme",
                    "E": "Polimeraz Zincir Reaksiyonu (PZR)"
                },
                "B",
                {
                    "A": "Western blot protein analizi yapar.",
                    "B": "Doğru cevap B'dir: TUNEL testi (TdT-mediated dUTP Nick End Labeling) apoptotik DNA kırıklarını boyar.",
                    "C": "Southern blot DNA analizi yapar ama in situ apoptoz göstermez.",
                    "D": "Karyotip kromozom haritasıdır.",
                    "E": "PZR DNA çoğaltma yöntemidir."
                }
            ),
            make_cloze(
                "Doku kesitlerinde apoptoz geçiren hücrelerin DNA kırıklarını saptamak için uygulanan floresan boyama testine TUNEL yöntemi denir.",
                "TUNEL",
                "Apoptotik DNA nick end labeling testi kısaltması"
            )
        ]
    })

    return slides
