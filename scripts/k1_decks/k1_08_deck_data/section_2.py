"""
Bölüm 2: DNA Hasarı Birikimi, Onarım Sistemleri ve Werner Sendromu
Adımlar: 11 - 20
Checkpoint: Adım 19 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # ADIM 11
    slides.append({
        "slideNumber": 11,
        "title": "Yaşam Boyu DNA Hasarı: Endojen ve Çevresel Tehditler",
        "subtitle": "Spontan deaminasyon, replikasyon hataları, ROS saldırıları ve radyasyon",
        "badge": "Genomik Hasar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İnsan vücudundaki her bir somatik hücrenin genomu günde ortalama 10.000 ila 100.000 adet DNA hasarı "
            "lezyonuna maruz kalır. Bu hasarlar iki ana kaynaktan türer: 1) Endojen kaynaklar (hücresel metabolizmanın "
            "doğal yan ürünü olan reaktif oksijen türleri, suyun yarattığı spontan hidrolitik deaminasyon ve DNA "
            "polimerazın replikasyon hataları), 2) Eksojen çevresel tehditler (güneşten gelen UV radyasyon, iyonize "
            "radyasyon, sigara dumanı ve kimyasal karsinojenler).\n\n"
            "> [TEMEL İLKE] Hücrelerin son derece gelişmiş DNA onarım enzim orduları vardır; hasarların %99.9'u "
            "kusursuz onarılır. Ancak kaçan mikroskobik hatalar on yıllar boyunca genomda kümülatif olarak birikir.\n\n"
            "Bu mutasyon birikimi, yaşlanan hücrelerin transkripsiyonel profilini derinden bozar."
        ),
        "medicalTerms": [
            {"term": "Spontan Deaminasyon", "explanation": "Sitozinin urasile dönüşmesi gibi DNA bazlarının kendiliğinden kimyasal amino grubunu kaybetmesidir."},
            {"term": "Kümülatif Mutasyon Yükü", "explanation": "Yıllar içinde tamir mekanizmalarından kaçarak genomda kalıcılaşan toplam mutasyon sayısıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Her hücre günde on binlerce endojen ve eksojen DNA hasarına maruz kalır.",
            "📌 [SINAV SPOTU] Onarım sistemlerinin kaçırdığı bakiye hasarlar kümülatif yaşlanmayı yönlendirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Endojen Tehdit", "desc": "Mitokondriyal ROS, hidroliz, deaminasyon ve polimeraz kayması.", "isKey": True},
                {"title": "Eksojen Tehdit", "desc": "Ultraviyole ışık, X-ışınları, çevresel toksinler ve sigara.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hücrelerin kendi metabolizmasında üretilen reaktif oksijen türleri genomda sürekli endojen DNA hasarı oluşturur.",
                "endojen",
                "Hücrenin kendi iç metabolik faaliyetlerinden kaynaklanan hasar tipi"
            ),
            make_active_recall(
                "Her somatik hücre günde on binlerce DNA lezyonuna maruz kalırken organizmanın on yıllarca sağlıklı yaşayabilmesinin sırrı nedir?",
                "Hücrelerin baz eksizyonu, nükleotid eksizyonu ve çift zincir tamiri gibi olağanüstü yüksek kapasiteli DNA onarım mekanizmalarına sahip olmasıdır."
            )
        ]
    })

    # ADIM 12
    slides.append({
        "slideNumber": 12,
        "title": "Tek Zincir vs Çift Zincir Kırıkları ve Onarım Yetersizliği",
        "subtitle": "Homolog rekombinasyon vs Hatalı uç birleştirme (NHEJ) ve kromozomal anomaliler",
        "badge": "Kırık Tipleri",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "DNA hasarları arasında biyolojik etkisi en yıkıcı olanlar çift zincir kırıklarıdır (double-strand breaks - DSB). "
            "Tek zincir kırıkları karşıdaki sağlam zincir kalıp alınarak hatasız onarılabilirken, her iki zincirin birden "
            "koptuğu DSB'lerin tamiri çok daha zordur. Bölünmeyen veya G1 fazındaki hücrelerde DSB'ler 'homolog olmayan "
            "uç birleştirme' (NHEJ) yolağıyla körü körüne birleştirilir.\n\n"
            "> [SINAV SPOTU] NHEJ onarım yolağı hataya son derece meyillidir (error-prone); nükleotid delesyonlarına, "
            "eklemelere ve translokasyonlara yol açarak genomik kararsızlığı katlar.\n\n"
            "Yaşlandıkça bu hatalı onarımlar kromozomal anomalileri artırır ve hücreyi kalıcı proliferasyon bloğuna iter."
        ),
        "medicalTerms": [
            {"term": "Çift Zincir Kırığı (DSB)", "explanation": "DNA sarmalının her iki zincirinin de aynı anda koptuğu en tehlikeli lezyon tipidir."},
            {"term": "NHEJ (Homolog Olmayan Uç Birleştirme)", "explanation": "Kalıp DNA olmadan kırık uçları doğrudan birbirine yapıştıran hataya meyilli tamir yoludur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Çift zincir kırıkları hücre için en sitotoksik ve mutajenik DNA lezyonudur.",
            "📌 [SINAV SPOTU] NHEJ onarımı nükleotid kaybına yol açarak yaşlı hücrelerde mutasyon yükünü artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Tek Zincir", "desc": "Kalıp zincir mevcuttur; hatasız ligasyonla tamir edilir.", "isKey": True},
                {"title": "Çift Zincir", "desc": "Kalıp yoktur; NHEJ ile delesyon ve kromozom aberasyonları doğar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Homolog Rekombinasyon vs Homolog Olmayan Uç Birleştirme (NHEJ)",
                "Homolog Rekombinasyon (HR)",
                "Kardeş kromatidi kusursuz bir kalıp olarak kullanarak çift zincir kırığını tamamen hatasız onaran S/G2 fazı yolağıdır.",
                "NHEJ Yolağı",
                "Kalıp kullanmadan kırık DNA uçlarını doğrudan birbirine tutturan, nükleotid delesyonu ve mutasyon riski çok yüksek olan G1/senesens yolağıdır."
            ),
            make_active_recall(
                "Bölünmeyen yaşlı hücrelerde çift zincir kırıklarının onarımında neden sıklıkla delesyonel mutasyonlar meydana gelir?",
                "Hücrelerin kardeş kromatide sahip olmadığı için hatasız homolog rekombinasyon yapamaması ve hataya meyilli NHEJ yolağını kullanmak zorunda kalmasıdır."
            )
        ]
    })

    # ADIM 13
    slides.append({
        "slideNumber": 13,
        "title": "DNA Onarım Sistemleri: NER, BER ve Mismatch Repair",
        "subtitle": "Kseroderma pigmentozum, kolorektal kanser ve onarım yetersizliği spektrumu",
        "badge": "Onarım Sistemleri",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Hücresel bütünlük, farklı DNA hasar tiplerine özelleşmiş üç temel eksizyon onarım sistemiyle korunur: "
            "1) Nükleotid Eksizyon Onarımı (NER): UV ışığının oluşturduğu hacimli pirimidin (timin) dimerlerini ve kimyasal "
            "adüktleri tamir eder; kalıtsal eksikliğinde 'Kseroderma Pigmentozum' (XP) ve aşırı cilt kanseri görülür. "
            "2) Baz Eksizyon Onarımı (BER): Oksitlenmiş bazları (örneğin 8-okso-guanin) DNA glikozilazlarla temizler.\n\n"
            "> [YÜKSEK VERİM] 3) Uyumsuzluk Onarımı (Mismatch Repair - MMR): Replikasyonda kayan yanlış eşleşmiş bazları "
            "(MLH1, MSH2) düzeltir; defektinde Lynch sendromu ve mikrosatellit instabilitesi gelişir.\n\n"
            "Yaşlanmayla birlikte bu enzimlerin sentez hızı ve enzimatik verimliliği kademeli olarak düşer."
        ),
        "medicalTerms": [
            {"term": "NER (Nükleotid Eksizyon)", "explanation": "UV timin dimerleri gibi sarmalı büken hacimli lezyonları 24-32 nükleotidlik parçayla kesip çıkaran sistemdir."},
            {"term": "BER (Baz Eksizyon)", "explanation": "Oksidasyon veya deaminasyona uğramış tek bir anormal bazı glikozilaz ile kesen tamir yoludur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kseroderma pigmentozumda NER eksiktir; güneş ışığı aşırı karsinojenik hale gelir.",
            "📌 [SINAV SPOTU] Yaşlanma sürecinde tüm eksizyon onarım sistemlerinin verimliliği azalır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "NER Sistemi", "desc": "UV timin dimerlerini ve hacimli kimyasal adüktleri temizler.", "isKey": True},
                {"title": "BER Sistemi", "desc": "ROS aracılı oksitlenmiş bazları (8-oksoG) glikozilazla onarır.", "isKey": True},
                {"title": "MMR Sistemi", "desc": "Replikasyonda takılan baz kaymalarını düzeltir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Onarım Yolağı", "Hedeflenen Lezyon Tipi", "Kalıtsal Hastalık Örneği", "Yaşlanma Etkisi"],
                [
                    [("NER (Nükleotid Eksizyon)", False, ""), ("UV timin dimerleri, hacimli adüktler", False, ""), ("Kseroderma Pigmentozum", True, "Aşırı cilt kanseri ve erken kutanöz yaşlanma"), ("Kutanöz fotoyaşlanma hızlanır", False, "")],
                    [("BER (Baz Eksizyon)", False, ""), ("Oksitlenmiş bazlar (8-oksoG)", False, ""), ("MUTYH ilişkili polipozis", True, "Kolon adenomları ve kanseri"), ("Nöronal mitokondriyal DNA hasarı", False, "")],
                    [("MMR (Uyumsuzluk Onarımı)", False, ""), ("Eşleşmemiş bazlar, mikrosatellitler", False, ""), ("Lynch Sendromu", True, "Herediter polipozis dışı kolon kanseri"), ("Genomik mikrosatellit kaymaları", False, "")]
                ]
            ),
            make_cloze(
                "Güneş ışığının DNA'da oluşturduğu pirimidin dimerlerini tamir eden nükleotid eksizyon onarımı yolağı Kseroderma pigmentozumda defektiftir.",
                "nükleotid eksizyon onarımı",
                "Hacimli UV lezyonlarını onaran temel hücresel sistem"
            )
        ]
    })

    # ADIM 14
    slides.append({
        "slideNumber": 14,
        "title": "Werner Sendromu (Yetişkin Progeriası): WRN Helikaz Gen Mutasyonu",
        "subtitle": "Otozomal resesif RecQ DNA helikaz/ekzonükleaz defekti ve genomik çöküş",
        "badge": "Werner Sendromu",
        "badgeColor": "red",
        "synthesisNarrative": (
            "DNA onarım bozukluklarının hücresel yaşlanmayı nasıl hızlandırdığının dünyadaki en kusursuz klinik modeli "
            "'Werner Sendromu'dur (erişkin progeriası). Werner sendromu, 8. kromozomdaki WRN geninde meydana gelen "
            "inaktive edici mutasyonlar sonucu otozomal resesif olarak kalıtılır. WRN proteini, RecQ ailesine ait özelleşmiş "
            "bir DNA helikaz ve ekzonükleaz enzimidir.\n\n"
            "> [SINAV SPOTU] WRN enzimi; replikasyon çatallarının ilerlemesini, homolog rekombinasyonu ve telomer "
            "bütünlüğünü korur; yokluğunda DNA replikasyonunda tıkanma, aşırı çift zincir kırıkları ve masif telomer erimesi gelişir.\n\n"
            "Werner sendromlu bireylerden alınan fibroblastlar doku kültüründe yalnızca 10-15 bölünmede senesense girerek durur."
        ),
        "medicalTerms": [
            {"term": "Werner Sendromu", "explanation": "WRN DNA helikaz mutasyonuna bağlı erişkin çağda hızlanmış yaşlanma ve erken ölüm tablosudur."},
            {"term": "WRN Helikaz", "explanation": "DNA replikasyonunda takılan çatalları çözen ve telomerleri koruyan RecQ ailesi enzimidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Werner sendromunun temel genetik nedeni WRN DNA helikaz gen mutasyonudur.",
            "📌 [SINAV SPOTU] Replikasyon ve telomer onarımı çöktüğü için hücrelerin bölünme kapasitesi dramatik düşer."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Genetik Kusur", "desc": "WRN geni (RecQ DNA helikaz / ekzonükleaz) delesyonu.", "isKey": True},
                {"title": "Hücresel Fenotip", "desc": "Fibroblastların erken replikatif tükenmesi ve senesens.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Erişkin yaşta saçlarda erken beyazlama ve dökülme, iki taraflı katarakt, deri atrofisi, erken agresif ateroskleroz ve erken ölümle seyreden Werner sendromunda mutasyona uğrayan gen ürünü aşağıdakilerden hangisidir?",
                {
                    "A": "Telomeraz ters transkriptaz (TERT)",
                    "B": "WRN DNA helikaz / ekzonükleaz enzimi",
                    "C": "Lamin A nükleer matriks proteini",
                    "D": "CFTR klor iyon kanalı",
                    "E": "Glukoz-6-fosfataz enzimi"
                },
                "B",
                {
                    "A": "TERT diskeratozis konjenitada mutanttır.",
                    "B": "Doğru! Werner sendromu WRN DNA helikaz gen mutasyonu sonucu gelişen progeroid tablodur.",
                    "C": "Lamin A Hutchinson-Gilford çocukluk progeriasıdır.",
                    "D": "CFTR kistik fibrozistir.",
                    "E": "G6Paz Von Gierke hastalığıdır."
                }
            ),
            make_cloze(
                "Werner sendromunda DNA replikasyonunu ve telomer onarımını yürüten WRN helikaz enzimi mutasyona uğramıştır.",
                "WRN helikaz",
                "Werner sendromundan sorumlu DNA onarım enzimi"
            )
        ]
    })

    # ADIM 15
    slides.append({
        "slideNumber": 15,
        "title": "Werner Sendromunun Klinik Fenotipi ve Erken Komplikasyonlar",
        "subtitle": "Katarakt, kuş yüzü görünümü, osteoporoz, sarkomlar ve 40-50 yaşta kardiyovasküler ölüm",
        "badge": "Werner Kliniği",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Werner sendromlu hastalar ergenlik dönemine kadar genellikle normal gelişim gösterirler. Ancak 20'li yaşların "
            "başında dramatik bir hızlanmış yaşlanma tablosu başlar: Saçlar hızla beyazlar ve dökülür (alopesi), ses incelir, "
            "cilt atrofiye uğrayarak parşömen kağıdına döner ve deri altı yağ erir (kuş yüzü / bird-like facies).\n\n"
            "> [SINAV SPOTU] 30'lu yaşlarda bilateral senil katarakt, tip 2 diyabet, hipogonadizm ve şiddetli osteoporoz "
            "eklenir. 40'lı yaşlarda ise yaygın koroner ateroskleroz ve malign mezenşimal tümörler (sarkomlar) patlak verir.\n\n"
            "Hastalar çoğunlukla 45-50 yaş civarında miyokard enfarktüsü veya metastatik sarkomlar nedeniyle kaybedilir."
        ),
        "medicalTerms": [
            {"term": "Kuş Yüzü Görünümü", "explanation": "Yüz yağ dokusunun erimesi ve burnun sivrileşmesiyle oluşan yaşlılık simasıdır."},
            {"term": "Malign Sarkom Yatkınlığı", "explanation": "Werner sendromunda genomik instabilite nedeniyle yumuşak doku ve kemik sarkomlarının sık görülmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Werner sendromu 20'li yaşlarda başlar; katarakt, ateroskleroz ve sarkomlarla seyreder.",
            "📌 [SINAV SPOTU] En sık ölüm nedenleri erken miyokard enfarktüsü ve malign sarkomlardır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Erken Belirtiler", "desc": "20'li yaşta saç beyazlaması, deri incelmesi, ses kısıklığı.", "isKey": True},
                {"title": "Ölümcül Sonuçlar", "desc": "Miyokard enfarktüsü ve osteosarkom / yumuşak doku sarkomu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Klinik Bulgu", "Werner Sendromu (Erişkin Progeria)", "Fizyolojik Normal Yaşlanma"],
                [
                    [("Başlangıç Yaşı", False, ""), ("20 - 30 yaş arası genç erişkinlik", True, "Dramatik erken başlangıç"), ("65 yaş ve üzeri ileri dönem", False, "")],
                    [("Temel Genetik Defekt", False, ""), ("WRN DNA helikaz gen mutasyonu", True, "RecQ ailesi DNA onarım defekti"), ("Kümülatif multifaktöriyel hasar", False, "")],
                    [("Kanser Profili", False, ""), ("Yüksek sıklıkta malign mezenşimal sarkomlar", True, "Nadir sarkom yatkınlığı"), ("Daha çok karsinomlar (epitelyal)", False, "")]
                ]
            ),
            make_cloze(
                "Werner sendromlu hastalarda genç yaşta katarakt ve aterosklerozun yanı sıra malign sarkomlar sık gelişir.",
                "sarkomlar",
                "Werner hastalarında sık görülen malign mezenşimal tümör grubu"
            )
        ]
    })

    # ADIM 16
    slides.append({
        "slideNumber": 16,
        "title": "Diğer DNA Onarım Defekti Sendromları: Bloom, Cockayne ve AT",
        "subtitle": "Kromozom kırılma sendromları, fotosensitivite ve immün yetmezlik spektrumu",
        "badge": "Progeroid Sendromlar",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Werner sendromu dışında DNA onarım sistemlerinin genetik bozuklukları da belirgin erken yaşlanma ve kanser "
            "fenotipleri doğurur: 1) Bloom Sendromu: BLM helikaz mutasyonuna bağlıdır; kardeş kromatid değişimleri (SCE) "
            "aşırı artar, telenjiektazik eritem, immün yetmezlik ve erken kanserler gelişir. 2) Cockayne Sendromu: Transkripsiyonla "
            "ilişkili NER defektidir (CSB/CSA genleri); nöronal demiyelinizasyon, fotosensitivite ve erken yaşlanma yapar.\n\n"
            "> [YÜKSEK VERİM] 3) Ataksi Telenjiektazi: ATM kinaz mutasyonudur; çift zincir kırıkları algılanamaz, "
            "serebellar ataksi, okülokutanöz telenjiektazi ve lenfoma/lösemi riski taşır.\n\n"
            "Bu hastalıklar DNA onarımının doku sağkalımı ve gençliğin korunmasındaki vazgeçilmez yerini kanıtlar."
        ),
        "medicalTerms": [
            {"term": "Bloom Sendromu", "explanation": "BLM helikaz mutasyonuna bağlı genomik instabilite ve yüksek kardeş kromatid değişimi tablosudur."},
            {"term": "Ataksi Telenjiektazi (AT)", "explanation": "ATM kinaz mutasyonu sonucu çift zincir kırıklarının tanınamadığı nörolojik ve onkolojik sendromdur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Bloom'da BLM helikaz, Cockayne'de transkripsiyonel NER, AT'de ATM kinaz defektiftir.",
            "📌 [SINAV SPOTU] Ortak özellikleri hücresel senesensin hızlanması ve erken kanser/doku kaybıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Bloom Sendromu", "desc": "BLM helikaz kaybı, aşırı kardeş kromatid değişimi (SCE).", "isKey": True},
                {"title": "Ataksi Telenjiektazi", "desc": "ATM kinaz kaybı, DSB hasarını hissedememe, ataksi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Werner Sendromu vs Cockayne Sendromu",
                "Werner Sendromu (Erişkin)",
                "WRN helikaz defektidir; 20'li yaşlarda başlar, katarakt, ateroskleroz ve sarkomlarla seyreder.",
                "Cockayne Sendromu (Pediatrik)",
                "Transkripsiyonel NER defektidir; erken çocuklukta başlar, mikrosefali, fotosensitivite ve nörodejenerasyonla seyreder (kanser riski düşüktür)."
            ),
            make_active_recall(
                "Ataksi telenjiektazi hastalığında hücrelerin çift zincir DNA kırıklarını algılayamamasına yol açan genetik defekt nedir?",
                "ATM serin/treonin protein kinaz genindeki mutasyondur."
            )
        ]
    })

    # ADIM 17
    slides.append({
        "slideNumber": 17,
        "title": "DNA Hasarı ve Epigenetik Değişiklikler: DNA Metilasyon Saatleri",
        "subtitle": "CpG adacıkları metilasyonu, Horvath epigenetik saati ve kromatin erozyonu",
        "badge": "Epigenetik Saat",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Yaşlanma sürecinde DNA'nın yalnızca birincil nükleotid dizisi bozulmaz; genlerin açık veya kapalı olmasını "
            "denetleyen epigenetik desenler de dramatik bir erozyona uğrar. Yaşlandıkça heterokromatin bölgeleri çözülür, "
            "genom genelinde global bir hipometilasyon görülürken, belirli promotor CpG adacıklarında hipermetilasyon gelişir.\n\n"
            "> [SINAV SPOTU] Steve Horvath tarafından tanımlanan 'Epigenetik Saat' (DNA metilasyon saati), kandaki veya "
            "dokudaki belirli 353 CpG bölgesinin metilasyon düzeyini ölçerek bireyin biyolojik yaşını ±2-3 yıl kesinlikle hesaplar.\n\n"
            "Epigenetik yaşlanma hızı yüksek olan bireylerde erken kardiyovasküler ölüm ve kanser riski anlamlı derecede yüksektir."
        ),
        "medicalTerms": [
            {"term": "Epigenetik Saat (Horvath Saati)", "explanation": "Belirli CpG sitelerindeki DNA metilasyon paternlerine bakarak biyolojik yaşı hesaplayan matematiksel algoritmadır."},
            {"term": "CpG Metilasyonu", "explanation": "Sitozin bazına metil grubu eklenerek gen ekspresyonunun epigenetik olarak susturulmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] DNA metilasyon saati (Horvath saati) biyolojik doku yaşını en hassas gösteren belirteçtir.",
            "📌 [SINAV SPOTU] Yaşlanmayla birlikte global hipometilasyon ve promotor hipermetilasyonu gelişir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kromatin Erozyonu", "desc": "Histon modifikasyonlarının ve heterokromatin adalarının dağılması.", "isKey": True},
                {"title": "Biyolojik Ölçüm", "desc": "CpG metilasyon profili kronolojik takvim yaşından bağımsız gerçek doku yaşını verir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Belirli CpG adacıklarındaki DNA metilasyon düzeylerini analiz ederek biyolojik yaşı ölçen algoritmaya Horvath saati adı verilir.",
                "Horvath saati",
                "Epigenetik yaşlanmayı ölçen matematiksel metilasyon saati"
            ),
            make_active_recall(
                "Yaşlanma sürecinde genomik DNA'nın epigenetik metilasyon profilinde meydana gelen iki temel zıt değişiklik nedir?",
                "Genom genelinde global hipometilasyon (heterokromatin çözülmesi) görülürken, belirli gen promotorlarındaki CpG adacıklarında hipermetilasyon (susturulma) gelişmesidir."
            )
        ]
    })

    # ADIM 18
    slides.append({
        "slideNumber": 18,
        "title": "Kümülatif Mutasyon Yükü, Gen Ekspresyon Değişimi ve Hücre Kaybı",
        "subtitle": "Kritik genlerin transkripsiyon yetersizliği, kök hücre tükenmesi ve doku atrofisi",
        "badge": "Doku Atrofisi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Yıllar içinde biriken onarılmamış DNA lezyonları, RNA polimeraz II enziminin transkripsiyon sırasında "
            "duraksamasına ve kritik yapısal/metabolik protein genlerinin okunamamasına neden olur. Hücre bu kilitlenmeyi "
            "aşamazsa iki yoldan birine girer: Ya p53 aracılığıyla kontrollü apoptoza gider ya da p16INK4a ile senesense girer.\n\n"
            "> [YÜKSEK VERİM] Her iki senaryonun da doku düzeyindeki net faturası 'parankimal hücre kaybı' ve 'kök "
            "hücre havuzunun tükenmesidir'.\n\n"
            "Beyinde nöron kaybı kortikal atrofiye, böbrekte glomerül kaybı nefroskleroza, kas dokusunda lif kaybı ise "
            "sarkopeniye yol açarak yaşlılığın klasik organ yetersizliklerini doğurur."
        ),
        "medicalTerms": [
            {"term": "Sarkopeni", "explanation": "İleri yaşlanmayla birlikte iskelet kası kütlesinin ve kas gücünün ilerleyici kaybıdır."},
            {"term": "Kök Hücre Tükenmesi", "explanation": "Doku progenitör hücrelerinin DNA hasarı ve senesens nedeniyle rejenerasyon havuzunu kaybetmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] DNA hasarı kök hücre tükenmesi ve parankim kaybı yaparak organ atrofisine yol açar.",
            "📌 [SINAV SPOTU] Yaşlı bireylerde iskelet kası kaybı sarkopeni tablosunu oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Transkripsiyonel Felç", "desc": "Polimerazın hasarlı DNA bölgelerinde takılıp kalması.", "isKey": True},
                {"title": "Organ Çıktıları", "desc": "Serebral kortikal atrofi, böbrek nefrosklerozu ve sarkopeni.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "DNA Hasarından Organ Atrofisine Gidiş",
                [
                    "1. Kümülatif Hasar: Somatik hücrelerde çift zincir kırıkları ve mutasyonlar birikir.",
                    "2. Transkripsiyon Bloğu: RNA polimeraz hasarlı kalıbı okuyamaz ve protein sentezi aksar.",
                    "3. Hücre Döngüsü Freni: p53 ve p16 aktivasyonu hücreyi senesens veya apoptoza sevk eder.",
                    "4. Kök Hücre Tükenmesi: Doku öncül hücreleri tükendiği için ölen hücrelerin yeri doldurulamaz.",
                    "5. Organ Atrofisi: Parankimal hücre sayısı azalarak dokuda hacim kaybı ve atrofi gelişir."
                ]
            ),
            make_cloze(
                "İleri yaşlanmayla birlikte iskelet kası liflerinin ve kas gücünün ilerleyici kaybına sarkopeni adı verilir.",
                "sarkopeni",
                "Yaşlılığa bağlı kas erimesi ve güçsüzlüğü tablosu"
            )
        ]
    })

    # ADIM 19 - CHECKPOINT 2
    slides.append({
        "slideNumber": 19,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] DNA Hasarı ve Erken Yaşlanma Sendromları",
        "subtitle": "Kümülatif mutasyonlar, NHEJ, NER, Werner sendromu ve epigenetik saatin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 2,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında genomik instabilite, DNA onarım defektleri ve erken yaşlanma sendromlarını "
            "özetliyoruz. 1) Hücre içi ROS ve metabolizma sürekli DNA hasarı yapar; kaçan hasarlar kümülatif olarak "
            "birikir. 2) Çift zincir kırıkları (DSB) en toksik hasardır; kalıpsız NHEJ tamiri delesyonel mutasyonlara yol açar. "
            "3) Onarım sistemleri: NER (timin dimerleri, Kseroderma Pigmentozum), BER (oksitlenmiş bazlar), MMR (eşleşme hataları). "
            "4) Werner Sendromu (erişkin progeriası): WRN DNA helikaz/ekzonükleaz mutasyonu, 20'li yaşta erken yaşlanma, "
            "katarakt, erken ateroskleroz ve ölümcül sarkomlar. 5) Epigenetik: Horvath saati CpG metilasyonuyla biyolojik doku "
            "yaşını kesin ölçer.\n\n"
            "> [KLİNİK İPUCU] Sınavda WRN helikaz mutasyonu sorulduğunda doğrudan Werner sendromunu işaretleyiniz.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle inceleyiniz."
        ),
        "medicalTerms": [
            {"term": "Werner Sendromu", "explanation": "WRN DNA helikaz defektine bağlı erişkin progeroid sendromdur."},
            {"term": "NHEJ", "explanation": "Homolog olmayan uç birleştirme ile mutajenik çift zincir DNA tamiridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Werner sendromu WRN DNA helikaz mutasyonuna bağlıdır.",
            "📌 [SINAV SPOTU] Horvath saati DNA metilasyon düzeyini ölçerek biyolojik yaşı belirler.",
            "📌 [SINAV SPOTU] NHEJ çift zincir kırıklarını kalıpsız tamir ederken delesyon mutasyonu yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Werner Defekti", "desc": "WRN geni, RecQ helikaz kaybı, 40 yaşta ölüm.", "isKey": True},
                {"title": "Onarım Yetersizliği", "desc": "NER defekti (XP), DSB algı defekti (AT).", "isKey": True},
                {"title": "Epigenetik Saat", "desc": "CpG metilasyonu ile biyolojik yaş tespiti.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-08-fc-04",
                "Werner sendromunun (erişkin progeriası) moleküler genetik nedeni ve hücre düzeyindeki etkisi nedir?",
                "WRN geninde meydana gelen mutasyon sonucu RecQ DNA helikaz/ekzonükleaz enziminin kaybolmasıdır; replikasyon çatalları tıkanır, telomerler korunamaz ve hücreler erken senesense girer.",
                "Werner sendromu genetik defekti ve hücresel mekanizması"
            ),
            make_flashcard(
                "k1-08-fc-05",
                "Horvath epigenetik saati bireyin biyolojik yaşını hangi hücresel mekanizmayı ölçerek hesaplar?",
                "Genomdaki belirli CpG dinükleotid adacıklarının DNA metilasyon düzeylerini ve profilini analiz ederek hesaplar.",
                "DNA metilasyon saatleri ve biyolojik yaş hesabı"
            ),
            make_flashcard(
                "k1-08-fc-06",
                "Homolog olmayan uç birleştirme (NHEJ) yolağının yaşlanan hücrelerde mutasyon birikimine katkısı nedir?",
                "Çift zincir DNA kırıklarını tamir ederken kardeş kromatit kalıbı kullanmadığı için nükleotid delesyonlarına ve kromozomal aberasyonlara yol açarak mutasyon yükünü artırmasıdır.",
                "NHEJ tamirinin mutajenik delesyonel doğası"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Werner sendromlu hastalarda 8. kromozomda kodlanan WRN helikaz enzimi mutasyona uğramıştır.",
                "WRN helikaz",
                "Werner sendromundaki mutant RecQ ailesi enzimi"
            )
        ]
    })

    # ADIM 20
    slides.append({
        "slideNumber": 20,
        "title": "DNA Onarım Kapasitesinin Ömür Belirlemedeki Rolü ve Sentez",
        "subtitle": "Türler arası karşılaştırmalar, fare vs insan tamir hızı ve uzun yaşamın genetik şifresi",
        "badge": "Evrimsel Sentez",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Farklı memeli türlerinin maksimal yaşam süreleri incelendiğinde, DNA onarım kapasitesi ile ömür uzunluğu "
            "arasında mükemmel bir doğru orantı olduğu görülür. Örneğin 3 yıl yaşayan farelerin DNA onarım enzimleri "
            "oldukça yavaş çalışırken; 80-100 yıl yaşayan insanların ve 200 yıldan fazla yaşayan Grönland balinalarının "
            "DNA onarım hızı ve telomer koruma kapasitesi son derece gelişmiştir.\n\n"
            "> [KLİNİK İPUCU] Bu evrimsel gerçek, genomik stabilitenin korunmasının organizma sağkalımının en temel "
            "belirleyicisi olduğunu kanıtlar.\n\n"
            "Geleceğin gen terapileri, DNA onarım enzimlerinin (PARP, ligazlar, helikazlar) ekspresyonunu artırarak "
            "hücrelerin kümülatif hasara karşı direncini yükseltmeyi hedeflemektedir."
        ),
        "medicalTerms": [
            {"term": "Genomik Stabilite", "explanation": "Hücre genomunun mutasyonlara ve yapısal kırıklara karşı kararlılığını koruma kapasitesidir."},
            {"term": "Maksimal Yaşam Süresi", "explanation": "Bir biyolojik türün ideal koşullarda ulaşabileceği en uzun yaşam süresidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Türler arasında DNA onarım hızı ile maksimal yaşam süresi doğru orantılıdır.",
            "📌 [SINAV SPOTU] Genomik bütünlüğün korunması uzun yaşamın en temel evrimsel şartıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Evrimsel Kural", "desc": "Uzun yaşayan türler üstün DNA onarım donanımına sahiptir.", "isKey": True},
                {"title": "Terapötik Ufuk", "desc": "Onarım yollarının aktivasyonuyla hücre ömrünü uzatma vizyonu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "35 yaşında bir hasta her iki gözde katarakt, saçlarda yaygın beyazlama ve ayak tabanında iyileşmeyen iskemik ülser şikayetleriyle başvuruyor. Hastaya yapılan genetik incelemede 8. kromozomda RecQ ailesine ait DNA helikaz enziminde homozigot mutasyon saptanıyor. En olası tanı ve beklenen komplikasyon nedir?",
                [
                    {
                        "text": "Kistik fibrozis ve kronik bronşiektazi atağı",
                        "isCorrect": False,
                        "feedback": "Kistik fibrozis CFTR mutasyonudur; helikaz mutasyonu ve erken katarakt Werner sendromuna aittir."
                    },
                    {
                        "text": "Werner sendromu; erken koroner ateroskleroz ve malign sarkom riski yüksektir.",
                        "isCorrect": True,
                        "feedback": "Mükemmel! WRN helikaz mutasyonu, genç erişkin kataraktı ve ateroskleroz Werner sendromunu doğrular; sarkom ve MI riski taşır."
                    }
                ]
            ),
            make_active_recall(
                "Memeli türlerinin ömür uzunluğu ile DNA onarım kapasitesi arasındaki evrimsel ilişki nasıldır?",
                "DNA onarım hızı ve kapasitesi ne kadar yüksekse türün maksimal yaşam süresi o kadar uzundur; insan ve balinalar kemirgenlere göre çok daha üstün onarım donanımına sahiptir."
            )
        ]
    })

    return slides
