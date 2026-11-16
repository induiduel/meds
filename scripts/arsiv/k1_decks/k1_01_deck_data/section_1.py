#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 1: Genetik ve Tıbbi Genetiğe Giriş & Disiplinler (Adım 1 - 8 + Tekrar Sayfası)
"""

from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall
)

def get_steps():
    return [
        {
            "slideNumber": 1,
            "title": "Tıbbi Genetiğin Tanımı, Amacı ve İnsan Hastalıklarındaki Rolü",
            "subtitle": "Kalıtım ilkelerinin insan sağlığı ve patolojisiyle entegrasyonu",
            "badge": "Temel Disiplin",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Tıbbi genetik; insan biyolojisinde kalıtım mekanizmalarını, genomik varyasyonları ve bu varyasyonların neden olduğu patolojik fenotipleri inceleyen multidisipliner bir klinik ve laboratuvar tıp dalıdır.\n\nKlasik biyolojik genetik tüm canlılardaki gen yapısı ve aktarımını incelerken; tıbbi genetik doğrudan insan sağlığına, hastalıkların etiyopatogenezine ve klinik yönetimine odaklanır:\n- **Hastalık Etiyolojisi:** Monogenik hastalıklardan multifaktöriyel kompleks bozukluklara kadar patolojilerin moleküler altyapısını aydınlatır.\n  - **Klinik Fenotip:** Genotipik değişimlerin organ sistemleri ve morfolojik gelişim üzerindeki yansımalarını inceler.\n  - **Bireyselleştirilmiş Tıp:** Hastaya özgü farmakogenetik yaklaşımları ve hedefe yönelik gen terapilerini yönlendirir.\n\n> 📌 **Temel İlke:** ==Tıbbi genetik== sadece laboratuvar analizinden ibaret olmayıp, klinik muayene (dismorfoloji) ve aileye yönelik genetik danışma ile bir bütündür.",
            "coreContent": {
                "table": {
                    "title": "Klasik Genetik ve Tıbbi Genetik Karşılaştırması",
                    "headers": ["Parametre", "Klasik / Genel Genetik", "Tıbbi Genetik"],
                    "rows": [
                        ["Çalışma Odağı", "Model organizmalar (bakteri, sirke sineği, fare)", "Doğrudan insan sağlığı ve klinik patolojiler"],
                        ["Temel Amaç", "Kalıtım kurallarının evrensel biyolojik tespiti", "Tanı, risk hesabı, korunma ve tedavi yönetimi"],
                        ["Klinik Boyut", "Klinik muayene ve danışma içermez", "Dismorfolojik muayene, genetik danışma ve etik boyut şarttır"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Tıbbi Genetik", "explanation": "İnsandaki kalıtım süreçlerini, genetik temelli varyasyonları ve hastalık patogenezini inceleyen klinik ve laboratuvar tıp disiplini."},
                {"term": "Fenotip-Genotip Korelasyonu", "explanation": "Bireyin DNA dizilimindeki spesifik genetik mutasyonun klinik belirti ve morfolojiye yansıma derecesi."}
            ],
            "spotPearls": [
                "Tıbbi genetik, klasik genetik prensiplerini insan kliniğine, hasta bakımına ve hastalık önleme stratejilerine uyarlayan tıp dalıdır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tıbbi genetiği klasik temel biyolojik genetikten ayıran en temel klinik yaklaşım hangisidir?",
                    {
                        "A": "Yalnızca bakteriyel plazmidleri ve model organizmaları incelemesi",
                        "B": "İnsan hastalıklarının etiyolojisini, fenotipik yansımasını ve ailevi risk yönetimini hedeflemesi",
                        "C": "DNA analizlerini tamamen terk edip sadece fenotipik gözlem yapması",
                        "D": "Kalıtım kurallarını Mendel ilkelerinden bağımsız kabul etmesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. Model organizmalar klasik genetiğin konusudur, tıbbi genetik doğrudan insana odaklanır.",
                        "B": "Doğru! Tıbbi genetik insan sağlığı, hastalık etiyolojisi, dismorfoloji ve ailevi rekürrens riskleri ile doğrudan ilgilidir.",
                        "C": "Yanlış. Tıbbi genetik ileri moleküler ve sitogenetik laboratuvar testleriyle entegre çalışır.",
                        "D": "Yanlış. Mendel ilkeleri tıbbi genetiğin de temel omurgasını oluşturur."
                    }
                ),
                make_cloze(
                    "Bireyin DNA dizilimindeki spesifik moleküler mutasyonun hastadaki klinik belirti ve fiziksel bulgulara yansıma derecesine fenotip-genotip korelasyonu adı verilir.",
                    "fenotip-genotip korelasyonu",
                    "Genetik mutasyon ile klinik tablo arasındaki uyum derecesi"
                )
            ]
        },
        {
            "slideNumber": 2,
            "title": "Sitogenetik Disiplini: Kromozom Morfolojisi ve Klasik Karyotipleme",
            "subtitle": "Hücre bölünmesi evresindeki kromozomların ışık mikroskobik mimarisi",
            "badge": "Laboratuvar",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Sitogenetik; hücre bölünmesinin metafaz evresinde kromatin ipliklerinin yoğunlaşmasıyla görünür hale gelen kromozomların sayısını, morfolojik yapısını ve mikroskobik düzeydeki anormalliklerini inceleyen genetik alt alanıdır.\n\nKlasik G-bantlama (Giemsa) yöntemiyle elde edilen karyotip analizi, sitogenetiğin temel tanı aracıdır:\n- **Karyotip Haritası:** Kromozomlar büyüklüklerine ve sentromer konumlarına göre 1'den 22'ye kadar otozomlar ve gonozomlar (X, Y) olarak dizilir.\n  - **Çözünürlük Sınırı:** Işık mikroskobunda standart karyotip analizi yaklaşık ==4-5 megabaz (Mb)== ve üzerindeki yapısal bozuklukları yakalayabilir.\n  - **Klinik Uygulama:** Sayısal kromozom anomalileri (Down, Turner, Klinefelter) ile büyük dengeli veya dengesiz translokasyonların tanısında altın standart başlangıç testidir.\n\n> ⚠️ **Sınav Tuzağı:** 4-5 Mb'ın altındaki delesyonlar ışık mikroskobunda kesinlikle ayırt edilemez!",
            "coreContent": {
                "table": {
                    "title": "Sitogenetik İncelemenin Temel Parametreleri",
                    "headers": ["Özellik", "Standart Karyotip (G-Bantlama)", "Klinik Yorum"],
                    "rows": [
                        ["Hücre Evresi", "Metafaz (Kolisin ile durdurulmuş)", "Kromozomların en yoğun ve ayrışık olduğu evredir"],
                        ["Bant Çözünürlüğü", "400 - 550 bant düzeyi", "Rutin periferik kanda standart uygulanan çözünürlüktür"],
                        ["Çözünürlük Eşiği", "4 - 5 Megabaz (Mb)", "Bu eşiğin altındaki mikrodelesyonlar görünmez"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Sitogenetik", "explanation": "Kromozomların sayısını, mikroskobik yapısını ve anomalilerini hücre düzeyinde inceleyen bilim dalı."},
                {"term": "Karyotipleme (G-Bantlama)", "explanation": "Metafaz kromozomlarının tripsin ve Giemsa boyası ile bantlanarak morfolojik ve sayısal olarak dizilmesi işlemi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Işık mikroskobu altında yapılan konvansiyonel karyotip analizinin çözünürlük sınırı 4-5 Mb'tır; bu boyutun altındaki mikrodelesyonlar karyotipte görülemez."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Rutin periferik kan lenfosit kültüründe Giemsa (G-bantlama) ile yapılan standart bir karyotip analizinin ışık mikroskobik çözünürlük sınırı yaklaşık ne kadardır?",
                    {
                        "A": "4 - 5 Megabaz (Mb)",
                        "B": "10 - 20 Kilobaz (kb)",
                        "C": "1 Tek Nükleotid (bp)",
                        "D": "50 - 100 Megabaz (Mb)"
                    },
                    "A",
                    {
                        "A": "Doğru! Standart 400-550 bant düzeyindeki karyotip analizi yaklaşık 4-5 Mb ve üzerindeki kromozomal sapmaları gösterir.",
                        "B": "Yanlış. Kilobaz düzeyindeki lezyonlar mikroarray (CMA) veya moleküler yöntemlerle saptanır.",
                        "C": "Yanlış. Tek baz değişimleri sadece DNA sekanslaması (Sanger, NGS) ile yakalanır.",
                        "D": "Yanlış. 50-100 Mb tüm kromozom kolu boyutundadır; karyotip bundan çok daha hassastır."
                    }
                ),
                make_interactive_table(
                    "Sitogenetik Çözünürlük ve Hücre Döngüsü Ezber Tablosu",
                    ["Parametre", "Standart Değer", "Klinik Anlamı"],
                    [
                        [("İncelenen Evre", False), ("Metafaz", True, "Hücre bölünmesi evresi"), ("Kromatin yoğunlaşması maksimaldir", False)],
                        [("Kullanılan İğ İpliği İnhibitörü", False), ("Kolsisin / Kolsemid", True, "İğ ipliklerini yıkar"), ("Hücreyi metafazda kilitler", False)],
                        [("Standart Çözünürlük Sınırı", False), ("4 - 5 Mb", True, "Megabaz cinsinden eşik"), ("Mikrodelesyonlar bu sınırın altındadır", False)]
                    ]
                )
            ]
        },
        {
            "slideNumber": 3,
            "title": "Moleküler Genetik: DNA Sekansı, Varyantlar ve Yeni Nesil Dizileme (NGS)",
            "subtitle": "Nükleotid baz dizilimi ve gen ekspresyonunun kimyasal düzeyde incelenmesi",
            "badge": "Laboratuvar",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Moleküler genetik; DNA ve RNA moleküllerinin kimyasal yapısını, baz dizilimini (adenin, timin, guanin, sitozin), transkripsiyon-translasyon mekanizmalarını ve nükleotid düzeyindeki mutasyonları araştıran daldır.\n\nSitogenetiğin çözünürlük gücünün yetersiz kaldığı submikroskobik ve tek nükleotid düzeyindeki patolojiler moleküler genetik yöntemlerle tespit edilir:\n- **Nokta Mutasyonları ve Küçük Delesyonlar:** Tek baz değişimleri (SNV), küçük çerçeve kayması (frameshift) mutasyonları Sanger dizileme veya ==Yeni Nesil Dizileme (NGS)== ile gösterilir.\n  - **Dinamik Mutasyonlar:** Frajil X ve Huntington gibi hastalıklarda görülen trinükleotid tekrar artışları özgül moleküler PCR ve triplet-repeat analizleriyle saptanır.\n  - **Ekzom ve Genom Dizileme (WES/WGS):** Protein kodlayan tüm bölgelerin (ekzom) aynı anda taranmasıyla bilinmeyen nadir sendromların moleküler tanısı konur.",
            "coreContent": {
                "table": {
                    "title": "Moleküler Genetik Tanı Yöntemleri ve Hedefleri",
                    "headers": ["Yöntem", "Hedef Patoloji", "Klinik Örnek"],
                    "rows": [
                        ["Sanger Dizileme", "Hedefe yönelik tek gen / ekzon dizilimi", "Kistik Fibrozis CFTR mutasyon analizi"],
                        ["Yeni Nesil Dizileme (NGS)", "Çoklu gen panelleri ve tüm ekzom (WES)", "Açıklanamayan dismorfik tablolar, nörolojik sendromlar"],
                        ["Triplet Repeat PCR", "Trinükleotid tekrar genişlemeleri", "Frajil X sendromu (CGG tekrarı), Huntington (CAG)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Moleküler Genetik", "explanation": "Genlerin DNA ve RNA düzeyindeki baz dizilimini, ekspresyonunu ve patolojik varyantlarını inceleyen alan."},
                {"term": "Yeni Nesil Dizileme (NGS)", "explanation": "Milyonlarca DNA parçasını paralel olarak dizileyerek tüm gen panellerini veya ekzomu hızlıca analiz eden yüksek verimli teknoloji."}
            ],
            "spotPearls": [
                "Tek gen hastalıklarında ve nokta mutasyonlarında sitogenetik mikroskopik inceleme yetersizdir; moleküler genetik yöntemler (NGS, PCR) zorunludur."
            ],
            "interactiveElements": [
                make_before_after(
                    "Sitogenetik (Karyotip)",
                    "Moleküler Genetik (NGS / PCR)",
                    ["Kromozom sayısı ve büyük yapısal kusurlar", "Işık mikroskobu kullanılır", "Çözünürlük 4-5 Mb ile sınırlı"],
                    ["Nükleotid baz dizilimi ve nokta mutasyonlar", "DNA dizi analizi ve elektroforez kullanılır", "Çözünürlük 1 tek baza (bp) kadar iner"]
                ),
                make_micro_quiz(
                    "Frajil X sendromunda FMR1 geninde görülen patolojik değişim tipi ve bunu saptamak için en uygun genetik disiplin hangisidir?",
                    {
                        "A": "Trinükleotid tekrar artışı — Moleküler Genetik (PCR/Southern Blot)",
                        "B": "Trizomi — Klasik Sitogenetik (G-Bantlama)",
                        "C": "Perisentrik inversiyon — Floresan mikroskopi",
                        "D": "Kromozom kol kaybı — Işık mikroskobik karyotip"
                    },
                    "A",
                    {
                        "A": "Doğru! Frajil X sendromu dinamik bir trinükleotid (CGG) tekrar genişlemesidir ve moleküler yöntemlerle incelenir.",
                        "B": "Yanlış. Trizomi sayısal kromozom anomalisidir.",
                        "C": "Yanlış. İnversiyon yapısal kromozom anomalisidir.",
                        "D": "Yanlış. Karyotip trinükleotid tekrar sayısını tayin edemez."
                    }
                )
            ]
        },
        {
            "slideNumber": 4,
            "title": "Klinik Genetik ve Dismorfoloji: Hasta Başı Tanı Sanatı",
            "subtitle": "Fizik muayene, fenotipik ipuçları ve sendrom tanıma metodolojisi",
            "badge": "Klinik Yaklaşım",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Klinik genetik; laboratuvar sonuçları ile hasta ve ailesinin klinik tablosunu birleştiren hekimlik dalıdır. Bu alanın en hayati bileşeni ==dismorfolojidir==.\n\nDismorfoloji (anormal morfolojinin incelenmesi); fetal gelişim sürecinde organ ve doku oluşumundaki aksaklıkların fiziksel yansımalarını analiz eder:\n- **Fenotipik Gözlem:** Hastanın yüz morfolojisi, kafa yapısı, el-ayak çizgileri ve iç organ anomalileri taranır.\n  - **Sendromik Örüntü Tanıma (Gestalt):** Birbirinden farklı anatomik bölgelerdeki minör ve majör bulgular birleştirilerek sendromik tanıya gidilir.\n  - **Test Seçim Rehberliği:** Klinisyenin doğru dismorfolojik saptaması, hastaya gereksiz yüzlerce test yapılmasını engelleyip doğrudan hedefe yönelik testi seçtirir.",
            "medicalTerms": [
                {"term": "Dismorfoloji", "explanation": "İnsan yapısındaki doğumsal yapısal anomalileri ve anormal morfolojik gelişimi inceleyen klinik tıp dalı."},
                {"term": "Gestalt / Sendromik Örüntü", "explanation": "Bir sendroma özgü yüz ve vücut bulgularının hekim tarafından bir bütün olarak anında tanınabilmesi durumu."}
            ],
            "spotPearls": [
                "Dismorfoloji, tıbbi genetikte laboratuvara gönderilecek doğru testi belirleyen en kritik klinik basamaktır."
            ],
            "interactiveElements": [
                make_cloze(
                    "Fetal gelişim sürecinde doku ve organ biçimlenmesindeki aksaklıkları ve doğumsal yapısal anomalileri inceleyen klinik alana dismorfoloji adı verilir.",
                    "dismorfoloji",
                    "Doğumsal şekil bozukluklarını inceleyen genetik dalı"
                ),
                make_micro_quiz(
                    "Çoklu konjenital anomalisi olan bir yenidoğanda dismorfolojik değerlendirmenin en birincil klinik katkısı nedir?",
                    {
                        "A": "Rastgele tüm testleri aynı anda yaptırmak",
                        "B": "Sendromik örüntüyü tanıyarak hedefe yönelik en doğru genetik testi ve klinik takibi belirlemek",
                        "C": "Laboratuvar testlerine gerek olmadığını kanıtlamak",
                        "D": "Genetik danışmayı tamamen gereksiz kılmak"
                    },
                    "B",
                    {
                        "A": "Yanlış. Rastgele test istemek zaman ve maliyet kaybına yol açar.",
                        "B": "Doğru! Dismorfolojik örüntü tanıma doğrudan hedefe yönelik tanısal algoritmayı ve takip planını çizer.",
                        "C": "Yanlış. Dismorfoloji laboratuvar ile el ele yürür.",
                        "D": "Yanlış. Dismorfolojik tanı genetik danışmanın temel zeminidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 5,
            "title": "İnsan Genomunun Büyüklüğü, Organizasyonu ve Genomik Mimarisi",
            "subtitle": "3 milyar baz çifti, 20.000 protein kodlayan gen ve kodlamayan bölgeler",
            "badge": "Genom Mimarisi",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "İnsan haploid genomu yaklaşık ==3.2 milyar baz çiftinden (bp)== oluşur ve 23 kromozom içine paketlenmiştir. Diploid bir somatik hücrede ise toplam 46 kromozom ve yaklaşık 6.4 milyar baz çifti bulunur.\n\nGenomun fonksiyonel dağılımı şaşırtıcı bir organizasyona sahiptir:\n- **Protein Kodlayan Bölgeler (Ekzom):** Tüm genomun sadece ==%1.5 - %2'lik== kısmını oluşturur (~20.000 protein kodlayan gen).\n  - **Kodlamayan Bölgeler (Non-coding DNA):** Genomun %98'den fazlası protein kodlamaz; intronlar, düzenleyici diziler (promotör, enhancer), mikroRNA'lar ve yapısal tekrar dizilerinden oluşur.\n  - **Miyokardiyal ve Klinik Önemi:** Genetik hastalıkların ve sendromların yaklaşık %85'i bu %1.5'lik ekzom bölgesindeki mutasyonlardan kaynaklanır; bu nedenle WES (Tüm Ekzom Dizileme) son derece yüksek tanı verimine sahiptir.",
            "coreContent": {
                "table": {
                    "title": "İnsan Genomunun Sayısal Özeti",
                    "headers": ["Genomik Bileşen", "Büyüklük / Oran", "Klinik / Biyolojik Önemi"],
                    "rows": [
                        ["Haploid Genom Boyutu", "3.2 x 10^9 baz çifti (3.2 Gb)", "23 kromozoma dağılmış toplam nükleotid sayısı"],
                        ["Protein Kodlayan Gen Sayısı", "~20.000 gen", "Tüm hücresel enzimleri ve yapısal proteinleri kodlar"],
                        ["Ekzomun Genoma Oranı", "%1.5 - %2.0", "Mendeliyen monogenik hastalıkların %85'i bu bölgededir"],
                        ["Kodlamayan Bölgeler", "> %98", "Gen regülasyonu, epigenetik kontrol ve yapısal mimari"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Ekzom", "explanation": "Genomda protein kodlayan tüm ekzonların bütünü; tüm genomun yalnızca %1.5-2'sini oluşturur."},
                {"term": "Haploid Genom", "explanation": "Gametlerde (sperm ve ovum) bulunan tek takım 23 kromozomluk genetik bilgi (n=23)."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Protein kodlayan ekzonlar tüm genomun sadece %1.5 - %2'sini oluşturmasına rağmen, bilinen klinik genetik hastalıkların yaklaşık %85'inden sorumludur."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "İnsan Genomu Temel Metrikleri Ezber Tablosu",
                    ["Genomik Parametre", "Sayısal Değer", "Sınav Notu"],
                    [
                        [("Haploid Baz Çifti Sayısı", False), ("3.2 Milyar bp", True, "Gb cinsinden"), ("23 kromozomluk haploid set", False)],
                        [("Protein Kodlayan Gen Sayısı", False), ("~20.000 gen", True, "Yaklaşık gen adedi"), ("Toplam protein çeşitliliğini kodlar", False)],
                        [("Ekzomun Genoma Yüzdesi", False), ("%1.5 - %2", True, "Ekzon oranı"), ("Hastalıkların %85'ini barındırır", False)]
                    ]
                ),
                make_micro_quiz(
                    "İnsan genomunda protein kodlayan bölgelerin (ekzom) tüm genoma oranı yaklaşık yüzde kaçtır?",
                    {
                        "A": "%1.5 - %2",
                        "B": "%25 - %30",
                        "C": "%50",
                        "D": "%85"
                    },
                    "A",
                    {
                        "A": "Doğru! Protein kodlayan ekzonlar insan genomunun yalnızca %1.5 - %2'lik kısmını oluşturur.",
                        "B": "Yanlış. Bu oran çok yüksektir; genomun %98'i kodlamayan dizilerden oluşur.",
                        "C": "Yanlış. Genomun yarısı protein kodlamaz.",
                        "D": "Yanlış. %85, bilinen monogenik hastalıkların ekzomda bulunma oranıdır, ekzomun boyutu değildir."
                    }
                )
            ]
        },
        {
            "slideNumber": 6,
            "title": "Kromozomların Yapısal Mimarisi: Sentromer, Telomer ve Kromatitler",
            "subtitle": "Hücre bölünmesinde stabiliteyi sağlayan temel anatomik kısımlar",
            "badge": "Kromozom Mimarisi",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Metafaz kromozomu, DNA'nın histon proteinleri etrafına sarılarak nükleozomları ve ileri derecede yoğunlaşmış kromatitleri oluşturmasıyla şekillenir.\n\nBir kromozomun fonksiyonel anatomisinde üç vazgeçilmez yapı bulunur:\n- **Sentromer (Primer Boğum):** Kinetokor proteinlerinin tutunduğu, mitotik ve mayotik iğ ipliklerinin bağlandığı kısımdır. Kromozomu kısa (p: petit) ve uzun (q: queue) olmak üzere iki kola ayırır.\n  - **Telomerler (Uç Bölgeler):** Kromozom uçlarında bulunan TTAGGG tekrar dizileridir. Kromozomların birbirine yapışmasını önler, stabiliteyi sağlar ve hücresel yaşlanmayı (replikatif senesens) kontrol eder.\n  - **Kardeş Kromatitler:** Sentromerle birbirine bağlı, DNA replikasyonu sonucu oluşmuş birbirinin kopyası iki ipliktir.",
            "medicalTerms": [
                {"term": "Sentromer", "explanation": "Kromozom kollarını ayıran, hücre bölünmesinde iğ ipliklerinin bağlandığı primer boğum bölgesi."},
                {"term": "Telomer", "explanation": "Kromozom uçlarını koruyan, TTAGGG hekzanükleotid tekrarlarından oluşan koruyucu başlık yapısı."}
            ],
            "spotPearls": [
                "Telomerler kromozom uçlarının parçalanmasını ve birbirine uç uca yapışmasını önler; sentromer ise anafazda doğru kutuplara çekilmeyi sağlar."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kromozomal Ayrılma Mekanizması",
                    [
                        "Metafazda kromatin maksimum yoğunlaşmaya ulaşır ve ekvatoryal düzleme dizilir.",
                        "Sentromerdeki kinetokor komplekslerine mikrotübül iğ iplikleri tutunur.",
                        "Kohezin proteinlerinin parçalanmasıyla anafazda kardeş kromatitler zıt kutuplara çekilir.",
                        "Sentromeri olmayan (asentrik) parçalar iğ ipliğine tutunamaz ve hücre bölünmesinde kaybolur."
                    ]
                ),
                make_micro_quiz(
                    "Hücre bölünmesi sırasında sentromerini kaybetmiş asentrik bir kromozom parçasının akıbeti ne olur?",
                    {
                        "A": "Kinetokor iğ ipliklerine bağlanamadığı için yavru hücrelere aktarılamaz ve sitoplazmada kaybolur",
                        "B": "Hemen yeni bir telomer sentezleyerek bağımsız bir kromozom haline gelir",
                        "C": "Hücre bölünmesini interfaz evresinde sonsuza dek kilitler",
                        "D": "Diploid hücrede trizomi tablosuna yol açar"
                    },
                    "A",
                    {
                        "A": "Doğru! Sentromeri olmayan parçalar (asentrik) anafazda kutuplara çekilemez ve mikronükleus oluşturup kaybolur (letal dengesizlik).",
                        "B": "Yanlış. Sentromer olmadan kromozom bağımsız yaşayamaz.",
                        "C": "Yanlış. Bölünme anafazda ilerler fakat asentrik parça kaybolur.",
                        "D": "Yanlış. Trizomi sentromerli tam kromozomun fazlalığıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 7,
            "title": "Sentromer Konumuna Göre Kromozom Sınıflaması",
            "subtitle": "Metasentrik, submetasentrik ve akrosentrik kromozom morfolojileri",
            "badge": "Sınıflandırma",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "İnsan kromozomları sentromerin kollar üzerindeki lokalizasyonuna göre morfolojik olarak üç ana gruba ayrılır:\n\n- **1. Metasentrik Kromozomlar:** Sentromer tam ortadadır; p kolu ile q kolunun uzunluğu birbirine eşittir (p ≈ q). Örnek: Kromozom 1, 3, 16, 19, 20.\n- **2. Submetasentrik Kromozomlar:** Sentromer merkeze yakındır ancak belirgin bir şekilde p kolu q kolundan daha kısadır (p < q). Örnek: Kromozom 2, 4-12, 17, 18, X.\n- **3. Akrosentrik Kromozomlar:** Sentromer uca çok yakındır. p kolu son derece kısadır ve ucunda genetik kod taşımayan heterokromatin sap (stalk) ve satellit (uydu) yapıları bulunur.\n\n> 🚨 **Hayati Sınav Kuralı:** İnsanda ==telosentrik kromozom YOKTUR!== Telosentrik kromozomlarda sentromer tam uçtadır ve p kolu hiç yoktur; bu durum insan karyotipinde patolojiktir (izokromozom hariç normal karyotipte bulunmaz).",
            "coreContent": {
                "table": {
                    "title": "Sentromer Konumuna Göre Kromozom Tipleri",
                    "headers": ["Kromozom Tipi", "Sentromer Konumu", "Kol Oranı (p/q)", "İnsan Karyotipindeki Örnekler"],
                    "rows": [
                        ["Metasentrik", "Tam ortada", "p ≈ q (eşit)", "Kromozom 1, 3, 16, 19, 20"],
                        ["Submetasentrik", "Merkeze yakın, kola kaymış", "p < q (p belirgin kısa)", "Kromozom 2, 4-12, 17, 18, X"],
                        ["Akrosentrik", "Uca çok yakın, satellitli", "p çok minik, q çok uzun", "13, 14, 15, 21, 22 ve Y"],
                        ["Telosentrik", "Tam uçta (p kolu yok)", "p = 0", "İnsan normal karyotipinde BULUNMAZ!"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Metasentrik", "explanation": "Sentromeri ortada olan ve p ile q kol boyları birbirine eşit olan kromozom tipi."},
                {"term": "Akrosentrik", "explanation": "Sentromeri uca çok yakın, kısa kolunda satellit taşıyan kromozom tipi (13, 14, 15, 21, 22)."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] İnsan normal karyotipinde telosentrik kromozom bulunmaz; insandaki kromozomlar metasentrik, submetasentrik veya akrosentriktir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Aşağıdaki kromozom tiplerinden hangisi normal insan karyotipinde KESİNLİKLE bulunmaz?",
                    {
                        "A": "Telosentrik kromozom",
                        "B": "Metasentrik kromozom",
                        "C": "Submetasentrik kromozom",
                        "D": "Akrosentrik kromozom"
                    },
                    "A",
                    {
                        "A": "Doğru! İnsanda telosentrik (sentromeri tam uçta, p kolu olmayan) kromozom bulunmaz. Fare gibi kemirgenlerde görülür.",
                        "B": "Yanlış. Kromozom 1 ve 3 tipik metasentrik kromozomlardır.",
                        "C": "Yanlış. İnsan kromozomlarının çoğu submetasentriktir.",
                        "D": "Yanlış. 13, 14, 15, 21, 22 akrosentrik kromozomlardır."
                    }
                ),
                make_before_after(
                    "Metasentrik Kromozom",
                    "Akrosentrik Kromozom",
                    ["Sentromer tam ortadadır", "p ve q kol boyları eşittir", "Satellit yapısı içermez", "Örnek: Kromozom 1 ve 3"],
                    ["Sentromer uca çok yakındır", "p kolu minik sap ve satellittir", "Robertsonyan translokasyona girer", "Örnek: Kromozom 13, 14, 15, 21, 22"]
                )
            ]
        },
        {
            "slideNumber": 8,
            "title": "Akrosentrik Kromozomlar: Robertsonyan Translokasyonun Anatomik Yuvası",
            "subtitle": "13, 14, 15, 21 ve 22 numaralı kromozomların özel morfolojisi",
            "badge": "Sınav Odağı",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "İnsan genomunda 5 çift akrosentrik otozom bulunur: ==13, 14, 15, 21 ve 22== (ayrıca Y kromozomu da akrosentriktir ancak satellit taşımaz).\n\nAkrosentrik kromozomların p (kısa) kolları eşsiz bir yapıya sahiptir:\n- **Stalk (Sap) Bölgesi:** Nükleolus Organizatör Bölge (NOR) olarak bilinir ve çok kopyalı ribozomal RNA (rRNA) genlerini kodlar.\n  - **Satellit (Uydu):** Kısa kolun en ucundaki heterokromatin kütlesidir; kritik protein kodlayan gen içermez.\n  - **Klinik ve Onkolojik Önemi:** Akrosentrik kromozomların p kolları kaybedildiğinde bireyde fenotipik bir kayıp oluşmaz. Bu durum iki akrosentrik kromozomun sentromerlerinden birleşerek ==Robertsonyan translokasyon== yapabilmesine olanak tanır (Örn: Der(14;21) taşıyıcılığı Down sendromu riskini doğurur).",
            "medicalTerms": [
                {"term": "Nükleolus Organizatör Bölge (NOR)", "explanation": "Akrosentrik kromozomların p kollarında yer alan ve ribozomal RNA (rRNA) sentezleyen gen kümeleri."},
                {"term": "Robertsonyan Translokasyon", "explanation": "İki akrosentrik kromozomun kısa kollarını kaybederek sentromer bölgesinden uç uca birleşmesi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] İnsandaki akrosentrik kromozomlar 13, 14, 15, 21 ve 22'dir. Yalnızca bu kromozomlar Robertsonyan translokasyon oluşturabilir!"
            ],
            "interactiveElements": [
                make_cloze(
                    "İnsan karyotipinde Robertsonyan translokasyona katılabilen satellitli akrosentrik kromozomlar 13, 14, 15, 21 ve 22 numaralı kromozomlardır.",
                    "13, 14, 15, 21 ve 22",
                    "5 çift akrosentrik otozom grubu"
                ),
                make_micro_quiz(
                    "Aşağıdaki kromozomlardan hangisi Robertsonyan translokasyona KATILAMAZ?",
                    {
                        "A": "Kromozom 18",
                        "B": "Kromozom 14",
                        "C": "Kromozom 21",
                        "D": "Kromozom 13"
                    },
                    "A",
                    {
                        "A": "Doğru! Kromozom 18 bir submetasentrik kromozomdur; akrosentrik olmadığı için Robertsonyan translokasyona katılamaz.",
                        "B": "Yanlış. 14 numara akrosentriktir ve en sık Robertsonyan translokasyon yapan kromozomlardandır.",
                        "C": "Yanlış. 21 numara akrosentriktir ve ailesel Down sendromunda rol oynar.",
                        "D": "Yanlış. 13 numara akrosentriktir ve Patau sendromu translokasyonlarında rol alır."
                    }
                )
            ]
        },
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Genetik Disiplinleri ve Çözünürlük Matrisi",
            "subtitle": "Karyotip, FISH, CMA, WES çözünürlükleri ve akrosentrik kromozomlar sentezi",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu tekrar modülü, Bölüm 1'de öğrenilen temel genetik disiplinlerini, kromozom anatomisini ve sınavda sıkça sorulan çözünürlük sınırlarını kalıcı hafızaya kodlamak için tasarlanmıştır.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Standart Karyotip:** Çözünürlük ==4-5 Mb==. Trizomiler ve büyük translokasyonlar için ilk basamaktır.\n- **Moleküler Genetik:** Çözünürlük ==1 baz çifti (bp)==. Nokta mutasyonları ve küçük delesyonlar için şarttır.\n- **Akrosentrik Kromozomlar:** ==13, 14, 15, 21, 22==. Robertsonyan translokasyonun tek adresidir.\n- **Telosentrik Kromozom:** İnsan normal karyotipinde ==KESİNLİKLE YOKTUR!==\n- **Ekzom Oranı:** Genomun ==%1.5 - %2'si== olmasına karşın, genetik hastalıkların ==%85'inden== sorumludur.",
            "coreContent": {
                "table": {
                    "title": "Bölüm 1 Kapsamlı Sentez ve Karşılaştırma Matrisi",
                    "headers": ["Yöntem / Yapı", "Çözünürlük Düzeyi", "Temel Endikasyon", "Sınav Tuzağı"],
                    "rows": [
                        ["Standart Karyotip", "4 - 5 Mb", "Sayısal anomaliler, dengeli translokasyonlar", "Mikrodelesyonları (1-3 Mb) ASLA göremez"],
                        ["Floresan İn Situ Hibridizasyon (FISH)", "100 - 200 kb", "Hedefe yönelik spesifik mikrodelesyonlar", "Hedef dışı bölgeleri tarayamaz (kör analiz)"],
                        ["Kromozomal Mikroarray (CMA)", "10 - 50 kb", "Dengesiz kopya sayısı varyantları (CNV)", "Dengeli translokasyon ve inversiyonları göremez"],
                        ["Yeni Nesil Dizileme (NGS/WES)", "1 baz (nükleotid)", "Nokta mutasyonları, tek gen hastalıkları", "Dengeli yapısal translokasyonları doğrudan saptayamaz"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Kopya Sayısı Değişimi (CNV)", "explanation": "Genomda 1 kb'dan büyük DNA parçalarının duplikasyon veya delesyon ile normal kopya sayısından sapması."},
                {"term": "Heterokromatin", "explanation": "Kromatinin transkripsiyonel olarak inaktif, sıkı paketlenmiş ve Giemsa ile koyu boyanan bölümü."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] Karyotip: 4-5 Mb | FISH: 100-200 kb | CMA: 10-50 kb | NGS: 1 baz çifti. Çözünürlük sırasını ezberlemek sınav sorularını saniyeler içinde çözdürür!",
                "📌 [TEKRAR SPOTU] 13, 14, 15, 21, 22 numaralı kromozomlar akrosentriktir ve Robertsonyan translokasyon yapabilen yegane gruptur."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Genetik Tanı Yöntemleri Çözünürlük ve Sınır Ezber Tablosu",
                    ["Tanı Yöntemi", "Çözünürlük Eşiği", "Saptayamadığı Kritik Durum"],
                    [
                        [("Standart Karyotip (G-Bantlama)", False), ("4 - 5 Mb", True, "Megabaz"), ("Mikrodelesyonlar (<4 Mb)", True, "Submikroskobik delesyon")],
                        [("Kromozomal Mikroarray (CMA)", False), ("10 - 50 kb", True, "Kilobaz"), ("Dengeli Translokasyon / İnversiyon", True, "Kopya sayısı değişmez")],
                        [("FISH (Hedefe Yönelik)", False), ("100 - 200 kb", True, "Prob boyutu"), ("Bilinmeyen / hedeflenmemiş bölgeler", True, "Hedef dışı körlük")],
                        [("Tüm Ekzom Dizileme (WES)", False), ("1 Nükleotid (bp)", True, "Tek baz"), ("İntronik derin mutasyonlar & dengeli yapısal", True, "Sadece ekzonları okur")]
                    ]
                ),
                make_micro_quiz(
                    "Dismorfik bir bebekte 2 Mb boyutundaki bir 22q11.2 mikrodelesyonunun rutin karyotip analizinde GÖRÜLEMEMESİNİN temel nedeni nedir?",
                    {
                        "A": "Delesyon boyutunun standart karyotipin 4-5 Mb'lık çözünürlük sınırının altında kalması",
                        "B": "22. kromozomun metafaz evresinde DNA replikasyonu yapmaması",
                        "C": "Karyotipin yalnızca cinsiyet kromozomlarını analiz edebilmesi",
                        "D": "Mikrodelesyonun yalnızca RNA düzeyinde gerçekleşen bir translasyon hatası olması"
                    },
                    "A",
                    {
                        "A": "Doğru! Standart karyotipin ışık mikroskobik çözünürlük sınırı 4-5 Mb'tır; 2 Mb'lık delesyonlar ışık mikroskobuyla fiziksel olarak ayırt edilemez.",
                        "B": "Yanlış. 22. kromozom normal replikasyon yapar.",
                        "C": "Yanlış. Karyotip tüm 22 çift otozomu da inceler.",
                        "D": "Yanlış. Mikrodelesyon yapısal bir DNA kaybıdır."
                    }
                ),
                make_micro_quiz(
                    "Robertsonyan translokasyon taşıyıcısı olduğu bilinen bir babanın hangi kromozomunda translokasyon bulunması MÜMKÜN DEĞİLDİR?",
                    {
                        "A": "Kromozom 16",
                        "B": "Kromozom 14",
                        "C": "Kromozom 21",
                        "D": "Kromozom 13"
                    },
                    "A",
                    {
                        "A": "Doğru! Kromozom 16 metasentriktir; Robertsonyan translokasyon YALNIZCA akrosentrik kromozomlarda (13, 14, 15, 21, 22) gerçekleşir.",
                        "B": "Yanlış. 14 numara akrosentriktir ve Robertsonyan translokasyona katılır.",
                        "C": "Yanlış. 21 numara akrosentriktir.",
                        "D": "Yanlış. 13 numara akrosentriktir."
                    }
                )
            ]
        }
    ]
