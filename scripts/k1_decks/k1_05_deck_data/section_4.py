"""
Bölüm 4: Apoptoza Giriş ve Fizyolojik Rolleri
Adımlar: 31 - 40
Checkpoint: Adım 39 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # ADIM 31
    slides.append({
        "slideNumber": 31,
        "title": "Apoptoz: Programlı ve Düzenlenmiş Hücre İntiharı",
        "subtitle": "Hücrenin kendi ölüm programını aktive ettiği intrensek hücresel süreç",
        "badge": "Apoptoza Giriş",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptoz, Yunanca 'yaprak dökümü' anlamına gelen ve hücrenin kendi genetik programını devreye sokarak "
            "sessizce kendini yok ettiği, son derece düzenli ve programlı bir hücre ölümü biçimidir. "
            "Nekrozun rastgele, kaotik ve kontrolsüz patlamasının tam aksine, apoptoz moleküler olarak "
            "titizlikle koreograflanmış bir hücresel intihar sürecidir.\n\n"
            "Bu süreçte hücre, kendi nükleer DNA'sını ve sitoplazmik proteinlerini parçalayan özel proteolitik "
            "enzimleri (kaspazlar) aktive eder.\n\n"
            "> [SINAV SPOTU] Apoptozun en temel ilkesi: 'Enerji (ATP) bağımlı' bir süreç olması ve plazma zarı "
            "bütünlüğünü koruyarak çevre dokuda HİÇBİR İNFLAMASYON oluşturmamasıdır!\n\n"
            "Hücre yavaşça büzüşür, organellerini sıkıştırır ve zarla çevrili küçük paketlere bölünür."
        ),
        "medicalTerms": [
            {"term": "Apoptoz", "explanation": "Hücrenin genetik programıyla başlatılan, ATP bağımlı, membran bütünlüğü korunan sessiz hücre ölümü."},
            {"term": "Kaspaz (Caspase)", "explanation": "Sistein proteaz ailesinden olan ve aspartat kalıntılarından sonra proteinleri kesen apoptoz enzimi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Apoptoz programlı, düzenlenmiş ve ENERJİ (ATP) BAĞIMLI bir hücre ölümüdür.",
            "📌 [SINAV SPOTU] Plazma zarı bütünlüğünü korur; çevre dokuda inflamasyon oluşmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Programlı İntihar", "desc": "Hücrenin kendi kaspaz kaskadını tetikleyerek ölmesi.", "isKey": True},
                {"title": "Enerji İhtiyacı", "desc": "Nekrozdan farklı olarak aktif ATP tüketimi gerektirmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Nekrozun aksine apoptoz programlı, düzenlenmiş ve aktif enerji yani ATP bağımlı bir hücre ölümüdür.",
                "ATP bağımlı",
                "Hücresel enerji para birimi gereksinimi"
            ),
            make_active_recall(
                "Apoptoz ile nekroz arasındaki enerji kullanımı ve inflamasyon farkı nedir?",
                "Apoptoz ATP bağımlıdır (enerji gerektirir) ve inflamasyon oluşturmaz; nekroz ise enerji gerektirmez ve daima belirgin inflamasyonla birliktedir."
            )
        ]
    })

    # ADIM 32
    slides.append({
        "slideNumber": 32,
        "title": "Apoptozun Biyolojik Çift Yüzü: Fizyolojik ve Patolojik Dengeler",
        "subtitle": "Gereksiz hücrelerin temizlenmesinden DNA hasarlı hücrelerin eliminasyonuna geniş spektrum",
        "badge": "Biyolojik Spektrum",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre ölüm biçimleri incelendiğinde nekroz DAİMA patolojik bir yıkım sonucudur; hiçbir fizyolojik "
            "süreçte nekroz gerçekleşmez. Buna karşılık apoptoz hem fizyolojik doku homeostazında hem de "
            "patolojik hastalıklarda merkezi rol oynayan çift yönlü bir mekanizmadır.\n\n"
            "Fizyolojik olarak apoptoz, görevini tamamlamış yaşlı hücreleri uzaklaştırır, organ boyutunu sabit tutar "
            "ve embriyonik organogenezi şekillendirir. Patolojik olarak ise onarılamayacak düzeyde DNA hasarı almış, "
            "mutasyona uğramış veya virüsle enfekte olmuş hücreleri diğer hücreleri korumak adına feda eder.\n\n"
            "> [KRİTİK UYARI] Aynı dokuda hem nekroz hem apoptoz eşzamanlı olarak bulunabilir; örneğin orta dereceli "
            "iskemide hücrelerin bir kısmı apoptozla, ağır iskemik odakta ise nekrozla ölür.\n\n"
            "Bu durum hasarın şiddetine ve hücresel ATP rezervine göre belirlenir."
        ),
        "medicalTerms": [
            {"term": "Fizyolojik Apoptoz", "explanation": "Sağlıklı organizmada doku dengesini ve organ şekillenmesini sağlayan fizyolojik hücre temizliği."},
            {"term": "Patolojik Apoptoz", "explanation": "Mutasyon, viral enfeksiyon veya radyasyon hasarı sonrası genom bütünlüğünü korumak için tetiklenen apoptoz."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nekroz daima patolojiktir; Apoptoz ise HEM FİZYOLOJİK hem PATOLOJİK olabilir.",
            "📌 [SINAV SPOTU] Aynı dokuda veya iskemik hasarda nekroz ve apoptoz bir arada görülebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Nekroz vs Apoptoz Doğası", "desc": "Nekroz kesinlikle patolojiktir; apoptoz fizyolojinin de temel aracıdır.", "isKey": True},
                {"title": "Eşzamanlı Varlık", "desc": "Hasar gören bir organda nekroz ve apoptozun yan yana ilerleyebilmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Nekroz vs Apoptoz Biyolojik Rolü",
                "Nekroz",
                "DAİMA patolojiktir. İskemi, toksin veya ağır travma sonucu gelişir; fizyolojik bir örneği yoktur.",
                "Apoptoz",
                "ÇOĞUNLUKLA fizyolojiktir (embriyogenez, hormon çekilmesi); ancak DNA hasarı ve virüslerde patolojik olarak da tetiklenir."
            ),
            make_cloze(
                "Nekrozun aksine apoptoz hem fizyolojik süreçlerde hem de patolojik hücresel hasarlarda rol oynayabilir.",
                "fizyolojik",
                "Sağlıklı vücut işleyişi ve gelişim süreçlerine ait nitelik"
            )
        ]
    })

    # ADIM 33
    slides.append({
        "slideNumber": 33,
        "title": "Embriyogenezde Apoptoz: Parmak Aralarının Açılması ve Lümenleşme",
        "subtitle": "Gelişimsel doku fazlalıklarının ve geçici embriyonik yapıların programlı silinmesi",
        "badge": "Embriyoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Embriyonik gelişim sırasında yeni dokuların oluşumu kadar, önceden var olan hücrelerin planlı olarak "
            "yok edilmesi de hayati önem taşır. Fetal el ve ayak gelişimi sırasında parmaklar başlangıçta "
            "tek parça, perdeli bir kürek şeklindedir.\n\n"
            "Parmak aralarındaki interdigital mezenkimal doku hücreleri, aldıkları genetik sinyallerle programlı "
            "apoptoza girerek erir. Böylece bağımsız, hareketli parmaklar oluşur.\n\n"
            "> [SINAV SPOTU] Eğer embriyogenezde interdigital apoptoz yetersiz kalır veya bloke olursa, parmaklar "
            "birbirine yapışık kalır; bu klinik tabloya 'Sindaktili' (perdeli parmak) adı verilir.\n\n"
            "Ayrıca içi boş organların (bağırsak, damar, üretra) lümenlerinin açılması ve Müllerian/Wolffian "
            "kanallarının cinsiyete göre regrese olması tamamen fizyolojik apoptoza bağımlıdır."
        ),
        "medicalTerms": [
            {"term": "İnterdigital Apoptoz", "explanation": "Fetal parmak aralarındaki mezenkim hücrelerinin ölerek parmakları ayrıştırması."},
            {"term": "Sindaktili", "explanation": "Parmak aralarındaki apoptozun yetersiz kalması sonucu parmakların yapışık kalması anomalisi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Embriyogenezde fazla hücrelerin yok edilmesi ve organ lümenlerinin açılması apoptozla gerçekleşir.",
            "📌 [SINAV SPOTU] Parmak aralarındaki apoptoz yetersizliği 'Sindaktili' anomalisiyle sonuçlanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Morfogenez Heykeltıraşı", "desc": "Apoptozun embriyoda dokuları oyarak organ formunu oluşturması.", "isKey": True},
                {"title": "Sindaktili Etyolojisi", "desc": "Perdeli el ve ayak anomalilerinde başarısız apoptoz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Embriyoda Parmak Ayrışması Apoptoz Zinciri",
                [
                    "1. Kürek Formu: Fetal ekstremite tomurcuğu başlangıçta düz, tek parça palet şeklindedir.",
                    "2. BMP Sinyalleri: Kemik morfogenetik proteinleri (BMP) parmak arası mezenkime apoptoz sinyali gönderir.",
                    "3. Kaspaz Kaskadı: İnterdigital hücrelerde mitokondriyal apoptoz yolu tetiklenir.",
                    "4. Sessiz Fagositoz: Apoptotik hücreler makrofajlarca çevreye zarar vermeden yutulur.",
                    "5. Bağımsız Parmaklar: Parmak araları açılarak serbest hareketli parmak anatomisi tamamlanır."
                ]
            ),
            make_cloze(
                "Fetal dönemde parmak aralarındaki interdigital dokuların apoptoza uğramaması sonucu sindaktili anomalisi ortaya çıkar.",
                "sindaktili",
                "Yapışık veya perdeli parmak anomalisi tıp adı"
            )
        ]
    })

    # ADIM 34
    slides.append({
        "slideNumber": 34,
        "title": "Hormon Bağımlı Dokuların İnvolüsyonu: Menstruasyon ve Laktasyon Sonu",
        "subtitle": "Hayatta kalma sinyali olan hormonların çekilmesiyle tetiklenen fizyolojik regresyon",
        "badge": "Endokrin Patoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kadın üreme sistemi hormonların döngüsel ritmine göre sürekli büyüyen ve küçülen dinamik bir doku havuzudur. "
            "Östrojen ve progesteron endometrium bezleri ve meme epiteli için en güçlü 'hayatta kalma (survival)' sinyalleridir.\n\n"
            "Menstrüel siklusun sonunda korpus luteumun gerilemesiyle progesteron ve östrojen seviyeleri aniden düşer. "
            "Hayatta kalma sinyallerinden mahrum kalan endometrium fonksiyonel tabakası hücreleri kitlesel apoptoza girer "
            "ve dökülür (menstruasyon kanaması).\n\n"
            "> [SINAV SPOTU] Doğum sonrası emzirmenin kesilmesiyle birlikte prolaktin ve oksitosin uyarısı biter; "
            "meme bezlerindeki asiner epitel hücreleri yoğun apoptoz ile küçülerek eski boyutuna döner (meme involüsyonu).\n\n"
            "Benzer şekilde kastrasyon sonrasında prostat bezinin küçülmesi de androjen çekilmesine bağlı apoptozdur."
        ),
        "medicalTerms": [
            {"term": "Hormon Çekilmesi (Withdrawal)", "explanation": "Hücreyi canlı tutan trofik hormonun azalmasıyla apoptozun tetiklenmesi."},
            {"term": "Post-Laktasyonel İnvolüsyon", "explanation": "Emzirme bitiminde meme salgı bezlerinin apoptozla küçülüp yağ dokusuna dönüşmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Menstruasyon sırasında endometriumun dökülmesi hormon çekilmesine bağlı fizyolojik apoptozdur.",
            "📌 [SINAV SPOTU] Laktasyon sonrası meme bezlerinin gerilemesi (involüsyon) apoptoz örneğidir.",
            "📌 [SINAV SPOTU] Kastrasyon sonrası prostat epitelinin gerilemesi de apoptozla yürütülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Trofik Sinyal Kaybı", "desc": "Hormon eksikliğinin apoptoz frenini kaldırıp ölümü başlatması.", "isKey": True},
                {"title": "Endometrium ve Meme", "desc": "Siklik dökülme ve post-laktasyonel küçülmenin mekanizması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Klinik Fizyolojik Durum", "Çekilen / Azalan Trofik Hormon", "Hedef Dokudaki Apoptoz Sonucu"],
                [
                    [("Menstruasyon Siklusu", False, ""), ("Progesteron ve Östrojen", True, "Luteal hormon kaybı"), ("Endometrium dökülmesi", False, "")],
                    [("Laktasyonun Sonlanması", False, ""), ("Prolaktin ve Oksitosin", True, "Süt uyarısı kesilmesi"), ("Meme bezlerinin involüsyonu", False, "")],
                    [("Androjen Blokajı / Kastrasyon", False, ""), ("Testosteron ve Dihidrotestosteron", True, "Erkeklik hormonu eksilmesi"), ("Prostat epitelinin atrofisi", False, "")]
                ]
            ),
            make_cloze(
                "Emzirmenin sonlanmasıyla birlikte meme bezi epitel hücreleri hormon çekilmesi sonucu apoptoz ile gerileyerek involüsyona uğrar.",
                "apoptoz",
                "Programlı ve sessiz hücresel ölüm biçimi"
            )
        ]
    })

    # ADIM 35
    slides.append({
        "slideNumber": 35,
        "title": "Proliferatif Dokularda Hücre Dengelemesi: Bağırsak Epiteli ve Kriptler",
        "subtitle": "Kök hücre çoğalması ile lümen ucundaki apoptotik dökülmenin kusursuz dengesi",
        "badge": "Gastroenteroloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gastrointestinal sistem epiteli insan vücudunda hücre yenilenmesinin en yüksek olduğu yerdir. "
            "Kolon ve ince bağırsak kriptlerinin tabanında yer alan kök hücreler sürekli mitoz bölünme ile yeni hücreler üretir.\n\n"
            "Yeni üretilen enterositler villus veya kript ekseni boyunca yukarı doğru göç eder. Göçün sonunda, "
            "villusun en ucuna ulaşan yaşlı epitel hücreleri lümene dökülmeden önce apoptoza uğrar.\n\n"
            "> [SINAV SPOTU] Eğer bu apoptotik temizlik aksarsa, aşırı biriken hücreler polip ve kanser gelişimine "
            "yol açar; apoptozun aşırı artması ise mukozal erozyon ve ülserasyonla sonuçlanır.\n\n"
            "Ders notumuzda belirtildiği üzere, kolonoskopi öncesi uygulanan agresif bağırsak hazırlık solüsyonları "
            "kolon kript epitelinde geçici bir apoptoz patlamasına yol açar; biyopside bolca apoptotik cisim görülür."
        ),
        "medicalTerms": [
            {"term": "Kript-Villus Ekseni", "explanation": "Bağırsakta kök hücre çoğalmasından apoptotik dökülmeye uzanan hücresel göç yolu."},
            {"term": "Mukozal Denge", "explanation": "Mitoz hızı ile apoptoz hızının eşitlenerek mukozanın sabit kalınlıkta tutulması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Proliferatif dokuların (bağırsak epiteli) yenilenmesinde eski hücreler apoptozla uzaklaştırılır.",
            "📌 [SINAV SPOTU] Kolonoskopi hazırlık rejimleri kolon kript epitelinde sıklıkla fizyolojik apoptozu tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücresel Trafik", "desc": "Kript tabanında mitoz, lümen ucunda programlı apoptoz.", "isKey": True},
                {"title": "Kolonoskopi Etkisi", "desc": "Hazırlık solüsyonlarının epitelde apoptotik cisimleri artırması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Kolonoskopi hazırlık rejiminin ardından alınan normal kolon biyopsilerinde kript epitelinde neden bol miktarda apoptotik hücre izlenir?",
                "Çünkü hazırlık solüsyonlarının yarattığı osmotik ve kimyasal stres epitel hücrelerinde fizyolojik apoptozu geçici olarak tetikler."
            ),
            make_cloze(
                "Bağırsak epitelinde sürekli çoğalan hücrelerin sayısını sabit tutmak için yaşlanan enterositler apoptoz mekanizmasıyla elenir.",
                "apoptoz",
                "Doku hücresel dengesini koruyan kontrollü ölüm biçimi"
            )
        ]
    })

    # ADIM 36
    slides.append({
        "slideNumber": 36,
        "title": "İmmün Yanıtın Sonlanması: Görevini Tamamlayan Lökositlerin Tasfiyesi",
        "subtitle": "Enfeksiyon temizlendikten sonra nötrofil ve efektör T hücrelerinin sessizce ortadan kalkması",
        "badge": "İmmünoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Akut bir bakteriyel enfeksiyon sırasında kemik iliğinden trilyonlarca nötrofil dokuya pompalanır ve "
            "antijene özgü T lenfositler klonal olarak devasa ordular halinde çoğalır.\n\n"
            "Mikroorganizma başarıyla temizlendiğinde, inflamasyonu başlatan sitokinler ve bakteri antijenleri "
            "ortamdan kaybolur. Bu durumda lökositleri canlı tutan büyüme faktörleri ve hayatta kalma sinyalleri kesilir.\n\n"
            "> [SINAV SPOTU] Görevini tamamlayan nötrofiller ve efektör T lenfositler kitleler halinde apoptoza gider. "
            "Bu süreç dokunun gereksiz oto-hasardan korunması ve immün homeostazın sağlanması için zorunludur!\n\n"
            "Eğer bu apoptoz gerçekleşmezse, aktive lenfositler kontrolsüz kalır ve 'lenfoproliferatif hastalıklar' "
            "veya kronik yıkıcı otoimmün tablolar meydana gelir."
        ),
        "medicalTerms": [
            {"term": "İmmün Kontraksiyon", "explanation": "Enfeksiyon sonrası aktive efektör lenfositlerin %95'inin apoptozla elenerek hafıza hücrelerinin bırakılması."},
            {"term": "Hayatta Kalma Sinyali Kaybı", "explanation": "İnterlökin (IL-2 vb.) azalmasıyla kaspaz kaskadının aktive olması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İmmün ve inflamatuar yanıtların sonunda lökosit sayısı hayatta kalma sinyallerinin kaybıyla ve apoptozla azalır.",
            "📌 [SINAV SPOTU] Apoptoz eksikliği kronik lenfoproliferasyona ve otoimmüniteye zemin hazırlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Görev Sonu Tasfiye", "desc": "Mikrop temizlenince nötrofil ve efektör T hücrelerinin intiharı.", "isKey": True},
                {"title": "Dokuyu Koruma", "desc": "Artık gereksiz olan lökositlerin dokuyu tahrip etmesinin önlenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Akut pnömonisi başarıyla tedavi edilen hastanın alveollerinde toplanmış olan milyonlarca nötrofilin akıbeti ne olur?",
                [
                    {
                        "text": "Nötrofiller alveol içinde nekroza uğrayarak patlar ve bronşları kazeöz nekrozla tıkar.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Bu durum inflamasyonu daha da alevlendirir ve akciğeri yıkar."
                    },
                    {
                        "text": "Sitokin uyarısı bittiğinde hayatta kalma sinyalleri kesilir; nötrofiller apoptoza girer ve makrofajlarca sessizce fagositozla temizlenir.",
                        "isCorrect": True,
                        "feedback": "Kusursuz immünopatoloji! Görevini tamamlayan lökositler apoptoza giderek doku hasarsız iyileşmeyi sağlar."
                    },
                    {
                        "text": "Nötrofiller kana geri dönüp kırmızı kan hücresine (eritrosite) dönüşür.",
                        "isCorrect": False,
                        "feedback": "Biyolojik olarak olanaksızdır."
                    }
                ]
            ),
            make_cloze(
                "İnflamatuar yanıtın sonunda hayatta kalma sinyallerinin kaybı ile lökosit sayısı apoptoz süreci sayesinde azaltılır.",
                "apoptoz",
                "Programlı hücre ölümü süreci adı"
            )
        ]
    })

    # ADIM 37
    slides.append({
        "slideNumber": 37,
        "title": "Otoreaktif Lenfositlerin Eliminasyonu: Santral ve Periferik Tolerans",
        "subtitle": "Kendi dokularına saldıran klonların timusta ve lenf bezlerinde programlı imhası",
        "badge": "İmmün Tolerans",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Bağışıklık sisteminin kendi vücut antijenlerine saldırmaması durumuna 'immünolojik tolerans' denir. "
            "Kemik iliği ve timusta gelişen lenfositlerin bir kısmı şans eseri vücudun kendi öz proteinlerini "
            "(otoantijenleri) yüksek afiniteyle tanıyan reseptörler üretir.\n\n"
            "Bu potansiyel olarak öldürücü otoreaktif hücreler, timik epiteldeki otoantijenlerle karşılaştığında "
            "hem mitokondriyal hem de ölüm reseptörü (Fas-FasL) yoluyla derhal apoptoza yönlendirilir (negatif seçilim / santral tolerans).\n\n"
            "> [SINAV SPOTU] Dolaşıma kaçan otoreaktif hücreler ise periferik lenfoid dokularda Fas reseptörü "
            "aracılığıyla apoptozla yok edilir. Eğer Fas veya FasL mutasyona uğrarsa, otoreaktif lenfositler elenemez "
            "ve ALPS (Otoimmün Lenfoproliferatif Sendrom) ve ağır otoimmün hastalıklar patlak verir!\n\n"
            "Apoptoz, vücudun kendi kendine saldırmasını engelleyen en güçlü zırhtır."
        ),
        "medicalTerms": [
            {"term": "Santral Tolerans", "explanation": "Timus ve kemik iliğinde otoantijen tanıyan lenfositlerin negatif seçilimle apoptoza uğratılması."},
            {"term": "Otoimmün Lenfoproliferatif Sendrom (ALPS)", "explanation": "Fas/FasL apoptoz yolağındaki genetik kusur nedeniyle lenfositlerin ölememesi ve otoimmünite gelişmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Potansiyel olarak zararlı otoreaktif lenfositlerin eliminasyonu apoptoz ile sağlanır.",
            "📌 [SINAV SPOTU] Hem mitokondriyal (intrinsik) hem de ölüm reseptörü (ekstrinsik / Fas) yolu kullanılır.",
            "📌 [SINAV SPOTU] Fas mutasyonunda apoptoz aksar ve Otoimmün Lenfoproliferatif Sendrom (ALPS) gelişir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Negatif Seçilim", "desc": "Kendi dokusunu tanıyan lenfosit klonlarının intihara zorlanması.", "isKey": True},
                {"title": "Fas-FasL Zırhı", "desc": "Periferik toleransın ölüm reseptörüyle otoimmüniteyi engellemesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Timusta kendi doku antijenlerini yüksek afiniteyle tanıyan otoreaktif T lenfositlerin apoptoz ile ortadan kaldırılması sürecine ne ad verilir?",
                {
                    "A": "Klonal anerji",
                    "B": "Negatif seçilim (Santral tolerans)",
                    "C": "Opsonizasyon",
                    "D": "Pozitif seçilim",
                    "E": "Somatik hipermutasyon"
                },
                "B",
                {
                    "A": "Anerji antijene yanıtsızlıktır, hücre ölmez.",
                    "B": "Doğru cevap B'dir: Kendi antijenini tanıyan hücrelerin apoptozla imhası negatif seçilimdir (santral tolerans).",
                    "C": "Opsonizasyon antikor/komplemanla kaplanmadır.",
                    "D": "Pozitif seçilim MHC tanıyan hücrelerin yaşatılmasıdır.",
                    "E": "Somatik hipermutasyon B hücresinde afinite olgunlaşmasıdır."
                }
            ),
            make_cloze(
                "Kendi vücut dokularına saldırma potansiyeli olan zararlı otoreaktif lenfositlerin ortadan kaldırılması apoptoz yoluyla sağlanır.",
                "otoreaktif lenfositlerin",
                "Kendi antijenlerimize karşı reaksiyon veren bağışıklık hücrelerinin"
            )
        ]
    })

    # ADIM 38
    slides.append({
        "slideNumber": 38,
        "title": "Çıkmış Kurul Sorusu Analizi: Apoptozla İlişkisiz Durum",
        "subtitle": "Dönem 3 Kurul 1 sınavında sorulan fagositoz vs apoptoz ayrımı",
        "badge": "Çıkmış Soru",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Patoloji sınavlarında apoptozun fizyolojik rolleri en yüksek soru potansiyeline sahip alanlardan biridir. "
            "Dönem 3 Kurul 1 tıp fakültesi sınavında sorulan orijinal soruya odaklanalım:\n\n"
            "'Hangisi apoptozla ilişkili değildir?'\n"
            "Öncüllere baktığımızda:\n"
            "A) Sürekli çoğalan aktif hücrelerde hücre sayısının azaltılması (bağırsak/kemik iliği) -> Apoptoz!\n"
            "C) Otoreaktif lenfositlerin ortadan kaldırılması -> Apoptoz!\n"
            "D) Sitotoksik T hücreleri tarafından başlatılan hücre ölümü -> Apoptoz!\n"
            "E) Görevleri sona eren hücrelerin ortadan kaldırılması -> Apoptoz!\n\n"
            "> [SINAV SPOTU] B seçeneğinde yer alan 'Opsonize hücrelerin ortadan kaldırılması' ise antikor (IgG) veya "
            "kompleman (C3b) ile işaretlenmiş bakterilerin nötrofil ve makrofajlar tarafından FAGOSİTOZ ile yutulmasıdır; "
            "apoptoz kapsamında değerlendirilmez!\n\n"
            "Bu ayrım, hekim adayının programlı intihar ile fagositer avlanma arasındaki farkı kavramasını test eder."
        ),
        "medicalTerms": [
            {"term": "Opsonizasyon", "explanation": "Bakteri veya hücrelerin IgG ve C3b ile kaplanarak fagositler için çekici hale getirilmesi olayı."},
            {"term": "Sitotoksik T Hücresi (CTL)", "explanation": "Enfekte hedef hücrede granzim ve perforin salgılayarak apoptoz tetikleyen CD8+ lenfosit."}
        ],
        "spotPearls": [
            "📌 [ÇIKMIŞ SORU SPOTU] Opsonize hücrelerin ortadan kaldırılması fagositozla ilgilidir; apoptoz örneği DEĞİLDİR.",
            "📌 [ÇIKMIŞ SORU SPOTU] Proliferatif doku dengesi, hormon çekilmesi, otoreaktif hücre tasfiyesi ve CTL öldürmesi apoptoz örnekleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Opsonizasyon Tuzağı", "desc": "IgG/C3b aracılı fagositozun apoptozla karıştırılmaması gerekliliği.", "isKey": True},
                {"title": "Kurul Soru Prensibi", "desc": "Hangi sürecin fagositoz, hangisinin programlı intihar olduğunu net ayırma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Aşağıdaki biyolojik durumlardan hangisi apoptoz mekanizması ile doğrudan İLİŞKİLİ DEĞİLDİR? [Kurul 1 Çıkmış Soru]",
                {
                    "A": "Sürekli çoğalan aktif hücrelerde apoptozla hücre sayısının azaltılması",
                    "B": "Opsonize hücrelerin ortadan kaldırılması",
                    "C": "Otoreaktif lenfositlerin ortadan kaldırılması",
                    "D": "Sitotoksik T hücreleri tarafından başlatılan hedef hücre ölümü",
                    "E": "Görevleri sona eren lökositlerin ortadan kaldırılması"
                },
                "B",
                {
                    "A": "Bağırsak kriptlerinde hücre sayısını sabit tutmak için apoptoz şarttır.",
                    "B": "Doğru cevap B'dir: Opsonize hücreler IgG ve C3b yardımıyla fagositoza uğrar; apoptoz örneği değildir.",
                    "C": "Otoantijen tanıyan hücreler apoptozla elenir (tolerans).",
                    "D": "CTL'ler perforin/granzim ile hedef hücrede kaspazları aktive eder.",
                    "E": "Enflamasyon bitince lökositler apoptozla uzaklaştırılır."
                }
            ),
            make_cloze(
                "Opsonize hücrelerin ortadan kaldırılması fagositoz ile ilgili bir süreç olup apoptoz örneği olarak sayılmaz.",
                "fagositoz",
                "Yabancı veya opsonize partiküllerin hücre içine alınıp sindirilmesi"
            )
        ]
    })

    # ADIM 39 (CHECKPOINT 4)
    slides.append({
        "slideNumber": 39,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Apoptozun Temelleri ve Fizyolojik Rolleri",
        "subtitle": "Tanım, enerji gereksinimi, inflamasyon yokluğu ve fizyolojik durumların konsolide özeti",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 4,
        "synthesisNarrative": (
            "Bu kontrol noktasında, programlı hücre ölümünün altyapısını ve sağlıklı vücuttaki 5 ana fizyolojik "
            "senaryosunu eksiksiz biçimde hafızamıza mühürlüyoruz.\n\n"
            "Apoptoz; enerji (ATP) bağımlı, membran bütünlüğünü koruyan, kaspaz enzim kaskadıyla yürütülen ve çevreye "
            "asla inflamasyon yaymayan düzenli bir hücre intiharıdır.\n\n"
            "> [ÖZET REÇETE] Fizyolojik Apoptoz Tablosu:\n"
            "1. Embriyogenez (parmakların ayrılması, lümen açılması)\n"
            "2. Hormon Çekilmesi (menstruasyon, laktasyon sonu meme involüsyonu, kastrasyonda prostat)\n"
            "3. Proliferatif Dokularda Denge (bağırsak epiteli)\n"
            "4. İmmün Yanıt Sonu (büyüme faktörü kesilen lökositlerin tasfiyesi)\n"
            "5. İmmün Tolerans (otoreaktif lenfositlerin eliminasyonu - ALPS riski)!\n\n"
            "Opsonize hücrelerin ortadan kaldırılması ise fagositozdur, apoptoz değildir."
        ),
        "medicalTerms": [
            {"term": "Fizyolojik Hücre Ölümü", "explanation": "Doku gelişimini ve dengesini sağlamak için tasarlanmış apoptoz süreçleri."},
            {"term": "İnvolüsyon", "explanation": "Hormon uyarısı bittiğinde bir organın apoptoz ile küçülerek eski boyutuna dönmesi."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Apoptoz = ATP gerektirir, membran sağlam kalır, inflamasyon YOKTUR.",
            "📌 [CHECKPOINT ÖZETİ] Embriyogenezde parmaklar apoptozla ayrılır (yetersizse sindaktili).",
            "📌 [CHECKPOINT ÖZETİ] Menstruasyon ve meme involüsyonu hormon çekilmesine bağlı apoptozdur.",
            "📌 [CHECKPOINT ÖZETİ] Opsonize hücrelerin temizlenmesi fagositozdur (çıkmış kurul sorusu)."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-10",
                "Apoptozun nekrozdan en temel iki biyolojik ve histopatolojik farkı nedir?",
                "1) Apoptozun ATP (enerji) bağımlı aktif bir süreç olması ve 2) Plazma zarı bütünlüğünü koruduğu için çevre dokuda inflamasyon oluşturmamasıdır."
            ),
            make_flashcard(
                "fc-k1-05-11",
                "Embriyogenezde parmak aralarındaki dokunun apoptoza uğramaması hangi konjenital anomaliye yol açar?",
                "Sindaktili (perdeli / yapışık parmak) anomalisi gelişir."
            ),
            make_flashcard(
                "fc-k1-05-12",
                "Tıp fakültesi kurul sınavında sorulan 'Hangisi apoptozla ilişkili değildir?' sorusunun doğru yanıtı ve tıbbi gerekçesi nedir?",
                "Doğru yanıt 'Opsonize hücrelerin ortadan kaldırılması'dır; çünkü opsonize hedeflerin yok edilmesi fagositoz mekanizmasıdır, apoptoz değildir."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Apoptoz ile İlişkili Fizyolojik Durumlar Tablosu",
                "headers": ["Fizyolojik Durum", "Tetikleyici Mekanizma", "Tipik Klinik / Biyolojik Örnek"],
                "rows": [
                    ["Embriyogenez", "Büyüme faktörü kaybı ve morfogenetik sinyaller", "Parmak aralarının açılması (Sindaktili önlenmesi)"],
                    ["Hormon Bağımlı İnvolüsyon", "Azalan hormon (progesteron/prolaktin) düzeyleri", "Menstruasyon dökülmesi ve laktasyon sonu meme"],
                    ["Proliferatif Doku Yenilenmesi", "Kript-villus ekseninde yaşlı hücre kaybı", "Bağırsak kript epiteli dökülmesi"],
                    ["İmmün Yanıtın Sonlanması", "Lökosit hayatta kalma sinyallerinin kaybolması", "Pnömoni sonrası nötrofillerin sessizce temizlenmesi"],
                    ["İmmün Tolerans Sağlanması", "Otoantijenlerin güçlü tanınması (Negatif seçilim)", "Kendi dokusuna saldıran otoreaktif T/B lenfositler"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Biyolojik Durum", "Temel Mekanizma", "Apoptoz mu Fagositoz mu?"],
                [
                    [("Menstruasyonda Endometrium Dökülmesi", False, ""), ("Hormon Çekilmesi", True, "Tetikleyen endokrin olay"), ("Apoptoz", False, "")],
                    [("Opsonize Bakterilerin Yutulması", False, ""), ("IgG ve C3b Reseptör Bağlanması", True, "Hücre zarı işaretleyicileri"), ("Fagositoz", False, "")],
                    [("Otoreaktif T Hücresi Elenmesi", False, ""), ("Negatif Seçilim / Fas Yolu", True, "İntraselüler ölüm yolağı"), ("Apoptoz", False, "")]
                ]
            ),
            make_active_recall(
                "Laktasyon bitiminde meme bezlerinin küçülmesini ve menstruasyonda endometriumun dökülmesini tetikleyen ortak patofizyolojik prensip nedir?",
                "Hücrelerin hayatta kalmasını sağlayan trofik hormonların (östrojen, progesteron, prolaktin) çekilmesidir."
            )
        ]
    })

    # ADIM 40
    slides.append({
        "slideNumber": 40,
        "title": "Sitotoksik T Lenfosit (CTL) ve NK Hücresi Aracılı Apoptoz",
        "subtitle": "Perforin ve Granzim B moleküllerinin hedef hücre kaspazlarını doğrudan tetiklemesi",
        "badge": "Sitotoksisite",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Bağışıklık sisteminin en elit katil hücreleri olan CD8+ Sitotoksik T Lenfositler (CTL) ve Doğal Katil "
            "(NK) hücreleri, virüsle enfekte olmuş veya tümöral değişime uğramış hücreleri öldürürken apoptoz yolunu kullanır.\n\n"
            "Hedef hücreyi tanıyan CTL, hücrelerarası temas noktasına salgı granüllerini boşaltır. Granüllerdeki 'Perforin' "
            "hedef hücrenin plazma zarında transmembran gözenekler açar.\n\n"
            "> [SINAV SPOTU] Açılan bu gözeneklerden içeri giren nötrofilik granül enzimi 'Granzim B', hedef hücrenin "
            "başlatıcı kaspazlarını ve doğrudan efektör Kaspaz-3'ü parçalayarak aktifler; hücreyi dakikalar içinde apoptoza gömer.\n\n"
            "Ayrıca CTL'ler yüzeylerindeki Fas Ligandını (FasL) hedef hücrenin Fas (CD95) reseptörüne bağlayarak "
            "dışsal ölüm reseptörü yolunu da paralel olarak ateşler."
        ),
        "medicalTerms": [
            {"term": "Perforin", "explanation": "CTL ve NK granüllerinde bulunan, hedef hücre zarında delikler açan gözenek yapıcı protein."},
            {"term": "Granzim B", "explanation": "Perforin deliklerinden hedef hücreye girip doğrudan kaspazları keserek apoptozu başlatan serin proteaz."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sitotoksik T lenfositler (CTL) hedef hücreyi Perforin ve Granzim B salgılayarak apoptoza uğratır.",
            "📌 [SINAV SPOTU] Granzim B doğrudan Kaspaz-3 ve Kaspaz-8'i aktive eder.",
            "📌 [SINAV SPOTU] CTL'ler ayrıca FasL-Fas etkileşimiyle de ölüm reseptörü yolunu tetikler."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Perforin Delikleri", "desc": "Hedef hücre zarında oluşturulan mikroskobik porlar.", "isKey": True},
                {"title": "Granzim İnfazı", "desc": "İçeri sızan proteazın kaspaz kaskadını doğrudan ateşlemesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "CTL Aracılı Hedef Hücre İnfaz Zinciri",
                [
                    "1. Hedef Tanıma: CTL, virüs antijeni taşıyan MHC-I molekülünü T hücre reseptörüyle (TCR) kilitler.",
                    "2. Granül Polarizasyonu: CTL lizozomal granüllerini hedef hücre temas yüzeyine yönlendirir.",
                    "3. Delik Açma: Perforin molekülleri hedef plazma zarına polimerize olarak porlar açar.",
                    "4. Granzim B Girişi: Serin proteaz olan Granzim B deliklerden sitoplazmaya hücum eder.",
                    "5. Kaspaz Aktivasyonu: Granzim B Kaspaz-3'ü doğrudan keserek hedef hücreyi apoptozla öldürür."
                ]
            ),
            make_cloze(
                "Sitotoksik T lenfositlerin granüllerinden salınan granzim B hedef hücrenin sitoplazmasına girerek kaspazları aktive eder.",
                "granzim B",
                "Doğrudan kaspaz aktivasyonu yapan CTL proteazı"
            )
        ]
    })

    return slides
