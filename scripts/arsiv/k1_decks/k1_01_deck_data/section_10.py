#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 10: Klinik Genetik Kuralları ve Sendrom Tanımadaki Güçlükler (Adım 77 - 88 + Tekrar Sayfası)
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
            "slideNumber": 77,
            "title": "Sendrom Tanısını Zorlaştıran Biyolojik Faktörlerin Genel Çerçevesi",
            "subtitle": "Genotip ile fenotip arasındaki doğrusal olmayan karmaşık etkileşimler",
            "badge": "Genetik İlkeler",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Klinik genetik pratiğinde bir sendromun tanınması her zaman ders kitaplarındaki klasik fotoğraflar kadar net değildir. Aynı genetik bozukluğa sahip bireyler birbirine hiç benzemeyen tablolara sahip olabilir.\n\nTanıyı güçleştiren bu durumlar genetik bilimin temel mekanizmalarıyla açıklanır:\n- **Pleiotropi:** Tek bir gendeki kusurun vücudun birbiriyle alakasız birçok farklı organ sistemini aynı anda bozmasıdır.\n- **Değişken Ekspresyon:** Aynı mutasyonu taşıyan aile bireylerinin hastalığı farklı şiddette yaşamasıdır.\n- **Azalmış Penetrans:** Bireyin patojenik genotipi taşımasına rağmen hiçbir klinik belirti vermemesidir.\n- **Fenokopi:** Çevresel bir ajanın genetik bir sendromu birebir taklit etmesidir.\n- **Genetik Heterojenite:** Farklı genlerin aynı hastalığı (lokus) veya aynı genin farklı hastalıkları (alilik) oluşturabilmesidir.",
            "coreContent": {
                "table": {
                    "title": "Genotip-Fenotip Diskordansına Yol Açan Temel Mekanizmalar",
                    "headers": ["Genetik Prensip", "Biyolojik Tanım", "Prototip Klinik Hastalık"],
                    "rows": [
                        ["Pleiotropi", "Tek gen -> Birden çok bağımsız sistem tutulumu", "Marfan Sendromu (FBN1)"],
                        ["Değişken Ekspresyon", "Aynı mutasyon -> Farklı klinik şiddet", "Nörofibromatozis Tip 1 (NF1)"],
                        ["Azalmış Penetrans", "Mutasyon var -> Klinik belirti yok (sessiz)", "BRCA1 Meme Kanseri"],
                        ["Fenokopi", "Çevresel etken -> Genetik hastalığın birebir taklidi", "Talidomid vs Holt-Oram"],
                        ["Lokus Heterojenitesi", "Farklı genler -> Aynı klinik hastalık", "Tuberoz Skleroz (TSC1 / TSC2)"],
                        ["Alilik Heterojenite", "Aynı gen -> Farklı hastalık tabloları", "DMD: Duchenne vs Becker"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Non-lineer Fenotip", "explanation": "DNA dizisindeki mutasyon ile klinik bulgular arasındaki karmaşık ve değişken ilişki."},
                {"term": "Genetik Değişkenlik", "explanation": "Modifiye edici genler ve epigenetik faktörlerin hastalık kliniğini farklılaştırması."}
            ],
            "spotPearls": [
                "Aynı genetik mutasyonun farklı bireylerde farklı tablolara yol açması; değişken ekspresyon, azalmış penetrans ve epigenetik regülasyon ilkeleriyle açıklanır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Aynı ailede tamamen aynı genetik mutasyona sahip iki kardeşten birinin hastalığı çok hafif birkaç cilt lekesiyle, diğerinin ise ağır nörolojik komplikasyonlarla geçirmesi hangi genetik ilkeyle tanımlanır?",
                    {
                        "A": "Değişken Ekspresyon (Variable Expressivity)",
                        "B": "Tam Penetrans",
                        "C": "Fenokopi",
                        "D": "Genomik İmprinting"
                    },
                    "A",
                    {
                        "A": "Doğru! Aynı genotipin bireyler arasında farklı klinik ağırlık ve belirti şiddetiyle seyretmesi değişken ekspresyondur.",
                        "B": "Yanlış. Tam penetrans sadece hastalığın ortaya çıkıp çıkmadığıyla ilgilidir.",
                        "C": "Yanlış. Fenokopide genetik mutasyon yoktur, çevresel taklit vardır.",
                        "D": "Yanlış. İmprinting ebeveyn kökenine göre gen susturulmasıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 78,
            "title": "Pleiotropi Mekanizması: Tek Bir Genetik Kusurun Birbiriyle İlişkisiz Çoklu Sistemleri Etkilemesi",
            "subtitle": "Fibrillin-1 veya Marfan sendromu örneğinde bağ dokusunun yaygın dağılımı",
            "badge": "Temel İlke",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Pleiotropi; tek bir gendeki mutasyonun veya tek bir kromozom anomalisinin, embriyolojik ve fonksiyonel olarak birbiriyle tamamen ilişkisiz görünen birden çok organ sisteminde patolojilere yol açması fenomenidir.\n\nPleiotropinin tıp tarihindeki en klasik örneği Marfan Sendromudur:\n- **Tek Bir Gen (FBN1):** 15q21.1 bölgesindeki FBN1 geni, hücre dışı matriksin temel bileşeni olan fibrillin-1 glikoproteinini kodlar.\n- **Çoklu Sistem Tutulumu (Pleiotropik Etkiler):**\n  - **Göz:** Lens subluksasyonu (ektropia lentis; genellikle yukarı-dışa dislokasyon).\n  - **Kardiyovasküler:** Aort kökü dilatasyonu, aort diseksiyonu ve mitral kapak prolapsusu (MVP).\n  - **İskelet Sistemi:** Araknodaktili (uzun parmaklar), pektus ekskavatum/karinatum, aşırı boy uzunluğu ve skolyoz.\n  - **Akciğer:** Spontan pnömotoraks.",
            "coreContent": {
                "table": {
                    "title": "Marfan Sendromunda FBN1 Gen Mutasyonunun Pleiotropik Hedefleri",
                    "headers": ["Organ Sistemi", "Patolojik Bulgusu", "Mekanizma / Klinik Risk"],
                    "rows": [
                        ["Göz", "Ektropia Lentis (Yukarı-dışa subluksasyon)", "Zonüler liflerin gevşemesi"],
                        ["Kardiyovasküler", "Aort Kökü Dilatasyonu & Diseksiyon", "Elastik liflerin zayıflaması (en mortal komplikasyon)"],
                        ["İskelet", "Araknodaktili, Pektus Deformitesi, Skolyoz", "Uzun kemiklerin aşırı büyümesi"],
                        ["Solunum", "Spontan Pnömotoraks", "Apikal büllerin rüptürü"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Pleiotropi", "explanation": "Tek bir gendeki mutasyonun birden fazla bağımsız organ sisteminde fenotipik etki oluşturması."},
                {"term": "Marfan Sendromu (FBN1)", "explanation": "Fibrillin-1 gen mutasyonu sonucu göz, kalp ve iskelet sistemini tutan klasik pleiotropik otozomal dominant hastalık."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Marfan sendromunda tek bir gen mutasyonunun (FBN1) gözde lens dislokasyonu, kalpte aort diseksiyonu ve iskelette araknodaktili yapması PLEİOTROPİ ilkesinin en klasik örneğidir."
            ],
            "interactiveElements": [
                make_cloze(
                    "Tek bir gendeki kusurun göz, iskelet ve kalp gibi bağımsız sistemlerde çoklu patolojilere yol açması biyolojik ilkesine [Pleiotropi] denir.",
                    "Pleiotropi",
                    "Tek genden çoklu organ etkisi",
                    "Pleiotropi, aynı gen ürününün farklı dokularda farklı kritik görevler üstlenmesi nedeniyle oluşur."
                ),
                make_micro_quiz(
                    "Fibrillin-1 (FBN1) geninde tek bir nokta mutasyonu bulunan bir hastada aynı anda lens ektopisi, mitral kapak prolapsusu, aort anevrizması ve uzun parmaklar (araknodaktili) gelişmesi aşağıdaki genetik kavramlardan hangisi ile açıklanır?",
                    {
                        "A": "Pleiotropi",
                        "B": "Lokus heterojenitesi",
                        "C": "Antisipasyon",
                        "D": "Fenokopi"
                    },
                    "A",
                    {
                        "A": "Doğru! Tek bir gendeki (FBN1) bozukluğun birçok farklı organda (göz, kalp, kemik) belirti vermesi pleiotropidir.",
                        "B": "Yanlış. Lokus heterojenitesinde farklı genler aynı hastalığı yapar.",
                        "C": "Yanlış. Antisipasyon kuşaktan kuşağa tablonun ağırlaşmasıdır.",
                        "D": "Yanlış. Fenokopi çevresel taklittir."
                    }
                )
            ]
        },
        {
            "slideNumber": 79,
            "title": "Değişken Ekspresyon (Variable Expressivity): Aynı Genotipin Farklı Bireylerde Farklı Şiddette Belirmesi",
            "subtitle": "Hafif bir cilt lekesinden ağır nörofibromlara uzanan klinik spektrum",
            "badge": "Klinik Çeşitlilik",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Değişken ekspresyon (variable expressivity); aynı genetik mutasyonu veya sendromu taşıyan farklı bireylerin (hatta aynı ailenin birinci derece akrabalarının), hastalığın belirtilerini çok farklı şiddet, ağırlık ve klinik spektrumda sergilemesidir.\n\nBu ilkenin prototipi Nörofibromatozis Tip 1 (NF1) tablosudur:\n- **Aynı Ailede Farklı Tablolar:** NF1 geninde tamamen aynı mutasyonu taşıyan bir ailede:\n  - Baba: Yalnızca vücudunda birkaç adet zararsız açık kahverengi 'Cafe-au-lait' (sütlü kahve) lekesi ve Lisch nodülü taşırken,\n  - Çocuğu: Ağır pleksiform nörofibromlar, optik gliyom (görme kaybı), skolyoz ve öğrenme güçlüğü ile doğabilir.\n- **Nedenleri:** Modifiye edici genler, çevre faktörleri ve rastlantısal somatik ikinci vuruş (second-hit) mutasyonları bu değişkenliği yönetir.",
            "coreContent": {
                "table": {
                    "title": "Nörofibromatozis Tip 1'de Değişken Ekspresyon Spektrumu",
                    "headers": ["Klinik Şiddet", "Görülen Bulgular", "Hasta Yaşamına Etkisi"],
                    "rows": [
                        ["Hafif Düzey", "6+ Cafe-au-lait lekesi, aksiller çillenme, Lisch nodülü", "Normal yaşam süresi, asemptomatik"],
                        ["Orta Düzey", "Subkutan kutanöz nörofibromlar, hafif skolyoz", "Kozmetik kaygı, hafif fonksiyon kaybı"],
                        ["Ağır Düzey", "Pleksiform nörofibrom, optik gliyom, psödoartroz, malign periferik sinir kılıfı tümörü", "Görme kaybı, nörolojik defisit, mortalite"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Değişken Ekspresyon (Variable Expressivity)", "explanation": "Aynı genotipi taşıyan bireyler arasında fenotipik şiddet ve belirti farklılıkları bulunması."},
                {"term": "Nörofibromatozis Tip 1 (NF1)", "explanation": "Cafe-au-lait lekeleri, Lisch nodülleri ve nörofibromlarla seyreden, değişken ekspresyonun klasik örneği olan sendrom."}
            ],
            "spotPearls": [
                "Değişken ekspresyonda herkes hastadır ancak hastalığın 'şiddeti' kişiden kişiye değişir; Nörofibromatozis Tip 1 (NF1) bunun en tipik örneğidir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Nörofibromatozis Tip 1 (NF1) tanılı bir annenin sadece hafif cafe-au-lait lekeleri varken, çocuğunda optik gliyom ve ağır pleksiform nörofibromlar gelişmesi hangi kavramla açıklanır?",
                    {
                        "A": "Değişken Ekspresyon (Variable Expressivity)",
                        "B": "Eksik Penetrans",
                        "C": "Genomik İmprinting",
                        "D": "X'e Bağlı Resesif Kalıtım"
                    },
                    "A",
                    {
                        "A": "Doğru! Anne de çocuk da mutasyonu taşır ve hastadır; ancak hastalığın klinik şiddeti birbirinden tamamen farklıdır (değişken ekspresyon).",
                        "B": "Yanlış. Eksik penetransta annede hiçbir belirti olmaması gerekirdi; oysa annede leke vardır.",
                        "C": "Yanlış. NF1 imprinting göstermez.",
                        "D": "Yanlış. NF1 otozomal dominanttır."
                    }
                )
            ]
        },
        {
            "slideNumber": 80,
            "title": "Eksik / Azalmış Penetrans: Genotipi Taşıdığı Halde Fenotipik Olarak Sağlıklı Bireyler",
            "subtitle": "'Ya Hep Ya Hiç' mantığı: Hastalık geni var ama birey tamamen asemptomatik",
            "badge": "Kalıtım Prensibi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Penetrans; bir patojenik mutasyonu taşıyan bireyler arasında hastalığın klinik fenotipini gösterenlerin yüzdesidir. Penetrans ya vardır ya yoktur (% oran olarak ifade edilir):\n\n- **Tam Penetrans (%100):** Mutasyonu taşıyan her birey istisnasız hastalığı geliştirir (örneğin Akondroplazi veya Huntington hastalığı).\n- **Eksik / Azalmış Penetrans (<%100):** Birey hastalığa neden olan dominant mutasyonu genetik olarak kesinlikle taşır, ancak hayatı boyunca hiçbir klinik belirti göstermez; tamamen sağlıklıdır!\n  - **Atlayan Kuşaklar:** Soyağacında anne sağlam görünürken torun hasta doğar; dışarıdan bakıldığında hastalık bir kuşağı atlamış (skip generation) gibi algılanır.\n  - **BRCA1/2 Örneği:** BRCA1 mutasyonu taşıyan bir kadının hayat boyu meme kanseri geliştirme penetransı yaklaşık %70-80'dir; yani %20-30 kadın mutasyona rağmen kanser geliştirmez.",
            "coreContent": {
                "table": {
                    "title": "Penetrans ve Ekspresyon Karşılaştırma Matrisi",
                    "headers": ["Parametre", "Penetrans (Kavramsal Doğası)", "Ekspresyon (Kavramsal Doğası)"],
                    "rows": [
                        ["Soru Tipi", "Hastalık var mı? Yok mu?", "Hastalık ne kadar şiddetli?"],
                        ["Matematiksel Boyut", "Kalitatif (Var/Yok - Yüzde %)", "Kantitatif (Klinik ağırlık spektrumu)"],
                        ["Örnek Durum", "Mutasyonu taşıyan kadının hiç kanser olmaması", "NF1'li hastanın hafif veya ağır lezyon taşıması"],
                        ["Soyağacı Etkisi", "Kuşak atlama (Skipped generation) yanılsaması", "Kuşaktan kuşağa farklı semptom kombinasyonları"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Azalmış Penetrans (Reduced Penetrance)", "explanation": "Hastalık yapıcı genotipi taşıyan bazı bireylerin tamamen sağlıklı kalması ve fenotip göstermemesi."},
                {"term": "Penetrans vs Ekspresyon", "explanation": "Penetrans 'hastalık var mı yok mu' (kalitatif), ekspresyon ise 'hastalık ne kadar şiddetli' (kantitatif) sorusudur."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Penetrans kalitatif bir kavramdır (hastalık var mı/yok mu: ya hep ya hiç); ekspresyon ise kantitatiftir (hastalığın klinik şiddet derecesi)."
            ],
            "interactiveElements": [
                make_before_after(
                    "Penetrans vs Ekspresyon Büyük Ayrımı",
                    "Azalmış Penetrans",
                    "Değişken Ekspresyon",
                    [
                        "Birey mutasyonu taşır ama HİÇBİR klinik belirti vermez",
                        "Kalitatif bir kavramdır ('Ya Hep Ya Hiç' kuralı)",
                        "Soyağacında kuşak atlamış gibi yanılsama yaratır",
                        "Örnek: BRCA1 taşıyıcısı olup hiç kanser geliştirmemek"
                    ],
                    [
                        "Birey mutasyonu taşır ve KESİNLİKLE klinik belirti verir",
                        "Kantitatif bir kavramdır (klinik şiddet derecesi değişir)",
                        "Kuşaklar arasında hafif lekelerden ağır tümörlere spektrum sunar",
                        "Örnek: NF1'de anne hafif lekeli, çocuk ağır pleksiform nörofibromlu"
                    ]
                )
            ]
        },
        {
            "slideNumber": 81,
            "title": "Fenokopi: Çevresel Bir Teratojenin Genetik Sendromu Birebir Taklit Etmesi",
            "subtitle": "Kalıtsal mutasyon olmaksızın çevresel faktörle ortaya çıkan ikiz fenotip",
            "badge": "Klinik Taklit",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Fenokopi; tamamen çevresel veya teratojenik bir etkenin (ilaç, enfeksiyon, mekanik hasar), genetik temelli bir sendromun veya mutasyonun oluşturduğu fenotipi birebir taklit etmesi durumudur.\n\nFenokopinin ayırıcı tanıdaki önemi:\n- **Genom Normaldir:** Hastanın DNA'sında o sendroma ait hiçbir genetik mutasyon bulunmaz.\n- **Örnek 1 - Fetal Alkol Sendromu (FAS):** İntrauterin alkol maruziyeti, mikrosefali, düz filtrum ve kalp anomalileriyle genetik sendromları taklit edebilir.\n- **Örnek 2 - Talidomid ve Holt-Oram Sendromu:** Talidomid maruziyeti, TBX5 gen mutasyonuyla seyreden kalıtsal Holt-Oram sendromunun başparmak ve radyal ışın defektlerini birebir kopyalar.\n- **Genetik Danışma:** Fenokopilerde sonraki gebeliklerde tekrarlama riski genel popülasyon kadardır; aileye genetik hastalık olmadığı anlatılarak korkuları giderilir.",
            "coreContent": {
                "table": {
                    "title": "Klasik Fenokopi Çiftleri ve Ayırıcı Tanı",
                    "headers": ["Genetik Sendrom (Mutasyonlu)", "Çevresel Fenokopi Etkeni", "Ortak Paylaşılan Fenotip"],
                    "rows": [
                        ["Holt-Oram Sendromu (TBX5 geni)", "Talidomid İntrauterin Maruziyeti", "Radyal ışın defekti, fokomeli, kardiyak ASD/VSD"],
                        ["Dubowitz / Williams Sendromu", "Fetal Alkol Spektrum Bozukluğu (FAS)", "Mikrosefali, basık burun kökü, zeka geriliği"],
                        ["Kretinizm (Kalıtsal Tiroit Diskenezisi)", "İntrauterin Ağır İyot Eksikliği", "Büyüme geriliği, zeka geriliği, kaba yüz hatları"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Fenokopi", "explanation": "Çevresel faktörlerin etkisiyle genetik bir hastalığın fenotipik tablosunun taklit edilmesi."},
                {"term": "Holt-Oram Sendromu (TBX5)", "explanation": "Radyal ışın/başparmak anomalileri ve kalpte ASD defektiyle seyreden, talidomidle taklit edilen sendrom."}
            ],
            "spotPearls": [
                "Fenokopide tablo genetik bir sendromu birebir taklit eder ancak hastada hiçbir genetik mutasyon yoktur; neden çevresel veya teratojeniktir."
            ],
            "interactiveElements": [
                make_cloze(
                    "Çevresel veya teratojenik bir etkenin genetik bir sendromun fenotipini birebir taklit etmesi durumuna [Fenokopi] adı verilir.",
                    "Fenokopi",
                    "Çevresel fenotipik ikiz",
                    "Fenokopilerde genom tamamen normaldir ve sonraki gebeliklerde tekrarlama riski yoktur."
                )
            ]
        },
        {
            "slideNumber": 82,
            "title": "Lokus Heterojenitesi: Farklı Kromozomlardaki Farklı Genlerin Aynı Hastalığı Yapması",
            "subtitle": "Osteogenezis İmperfekta ve Tuberoz Skleroz örneklerinde çoklu genetik yolaklar",
            "badge": "Heterojenite",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Lokus heterojenitesi; insan genomunun tamamen farklı kromozomlarında yer alan bağımsız genlerdeki mutasyonların, klinikte birbirinin tıpatıp aynısı olan tek bir hastalık tablosuna yol açmasıdır:\n\n- **Mekanizma:** Birbiriyle aynı biyokimyasal yolağın farklı basamaklarında görev alan proteinlerin bozulması sonucu son fenotip aynı olur.\n- **Klinik Örnek 1 - Tuberoz Skleroz:** Hastalık 9. kromozomdaki **TSC1 (Hamartin)** geni veya 16. kromozomdaki **TSC2 (Tüberin)** geni mutasyonuyla oluşur; her iki durumda da klinikte subepandimal nodüller, rabdomiyom ve anjiomiyolipom görülür.\n- **Klinik Örnek 2 - Osteogenezis İmperfekta (Cam Kemik):** 17. kromozomdaki **COL1A1** veya 7. kromozomdaki **COL1A2** geni mutasyonuyla aynı kemik kırılganlığı tablosu doğar.\n- **Klinik Örnek 3 - Sensorinöral İşitme Kaybı:** Doğuştan sağırlığa yol açan 100'den fazla bağımsız gen lokusu tanımlanmıştır.",
            "coreContent": {
                "table": {
                    "title": "Lokus Heterojenitesinin Prototipik Klinik Örnekleri",
                    "headers": ["Hastalık Adı", "Rol Oynayan Farklı Gen Lokusları", "Ortak Klinik Fenotip"],
                    "rows": [
                        ["Tuberoz Skleroz", "TSC1 (9q34) veya TSC2 (16p13.3)", "Kortikal tüberler, fasial anjiofibrom, renal AML"],
                        ["Osteogenezis İmperfekta", "COL1A1 (17q21) veya COL1A2 (7q21)", "Kemik kırılganlığı, mavi sklera, dentinogenezis"],
                        ["Polikistik Böbrek Hastalığı (ADPKD)", "PKD1 (16p13.3) veya PKD2 (4q21)", "Bilateral renal kistler, hipertansiyon, intrakraniyal anevrizma"],
                        ["Herediter Nonpolipozis Kolon Kanseri (Lynch)", "MLH1, MSH2, MSH6, PMS2", "Mikrosatellit instabilitesi ve erken yaşta kolon kanseri"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Lokus Heterojenitesi", "explanation": "Farklı genlerdeki mutasyonların aynı klinik fenotipi oluşturması (Örn: Tuberoz Skleroz: TSC1 ve TSC2)."},
                {"term": "Biyokimyasal Yolak Ortaklığı", "explanation": "Aynı protein kompleksinin farklı alt birimlerinin bozulmasıyla aynı hastalığın doğması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Tuberoz sklerozun hem TSC1 (9. kromozom) hem TSC2 (16. kromozom) mutasyonuyla tamamen aynı tabloda oluşması LOKUS HETEROJENİTESİDİR."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Otozomal dominant geçişli Tuberoz Skleroz hastalığının hem 9. kromozomdaki TSC1 (hamartin) hem de 16. kromozomdaki TSC2 (tüberin) gen mutasyonu sonucu aynı klinikle ortaya çıkabilmesi hangi genetik mekanizmanın kanıtıdır?",
                    {
                        "A": "Lokus Heterojenitesi",
                        "B": "Alilik Heterojenite",
                        "C": "Antisipasyon",
                        "D": "Genomik İmprinting"
                    },
                    "A",
                    {
                        "A": "Doğru! Farklı kromozomlardaki farklı bağımsız genlerin (TSC1 ve TSC2) aynı klinik tabloyu oluşturması lokus heterojenitesidir.",
                        "B": "Yanlış. Alilik heterojenitede tek bir gen üzerindeki farklı mutasyonlar söz konusudur.",
                        "C": "Yanlış. Antisipasyon tekrar artışlarıdır.",
                        "D": "Yanlış. İmprinting epigenetiktir."
                    }
                )
            ]
        },
        {
            "slideNumber": 83,
            "title": "Alilik Heterojenite: Aynı Tek Bir Gendeki Farklı Mutasyonların Farklı Tablolar Doğurması",
            "subtitle": "Distrofin geninde Duchenne vs Becker ve FGFR3 geninde Akondroplazi vs Tanatoforik Displazi",
            "badge": "Alilik Çeşitlilik",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Alilik heterojenite; tek bir gen lokusu üzerinde meydana gelen farklı mutasyon türlerinin, aynı hastalığın farklı ağırlık derecelerine veya birbirinden tamamen farklı klinik tablolara yol açmasıdır:\n\n- **Klinik Örnek 1 - Distrofin (DMD Geni):**\n  - **Duchenne Müsküler Distrofi (Ağır):** Mutasyon okuma çerçevesini kaydırır (frameshift); distrofin proteini hiç üretilemez. Çocuk 10-12 yaşında tekerlekli sandalyeye mahkum olur.\n  - **Becker Müsküler Distrofi (Hafif):** Çerçeve korunur (in-frame); kısaltılmış ama fonksiyon gören distrofin üretilir. Hasta erişkin yaşa kadar yürüyebilir.\n- **Klinik Örnek 2 - FGFR3 Geni:**\n  - FGFR3 Gly380Arg mutasyonu yaşamla bağdaşan **Akondroplazi** yaparken;\n  - FGFR3'teki farklı aminoasit mutasyonları yenidoğan döneminde ölümcül olan **Tanatoforik Displaziye** neden olur.\n- **Klinik Örnek 3 - CFTR Geni:** Ağır mutasyonlar klasik kistik fibrozis yaparken, hafif mutasyonlar yalnızca erkek infertilitesine (CBAVD) yol açar.",
            "coreContent": {
                "table": {
                    "title": "Alilik Heterojenitenin Prototipik Klinik Çiftleri",
                    "headers": ["Gen Adı", "Hafif / Farklı Fenotip", "Ağır / Letal Fenotip", "Moleküler Ayrım"],
                    "rows": [
                        ["DMD (Distrofin)", "Becker Müsküler Distrofi (İn-frame)", "Duchenne Müsküler Distrofi (Frameshift)", "Protein varlığı vs tam yokluğu"],
                        ["FGFR3", "Akondroplazi (Yaşamla bağdaşır)", "Tanatoforik Displazi (Yenidoğanda letal)", "Reseptörün bazal aktivasyon derecesi"],
                        ["CFTR", "İzole Konjenital Vas Deferens Yokluğu (CBAVD)", "Klasik Pulmoner-GİS Kistik Fibrozis", "Klor kanal iletim kapasitesi yüzdesi"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Alilik Heterojenite", "explanation": "Aynı gendeki farklı mutasyonların farklı fenotiplere yol açması (Örn: Duchenne vs Becker)."},
                {"term": "Çerçeve Koruyucu (In-frame) Mutasyon", "explanation": "Üçün katı nükleotid delesyonlarında okuma çerçevesinin bozulmaması, daha hafif fenotip doğurması."}
            ],
            "spotPearls": [
                "❓ [ÇIKMIŞ SORU ODAĞI] Farklı genlerin aynı hastalığı yapması = Lokus Heterojenitesi; Aynı gendeki farklı mutasyonların farklı hastalık yapması = Alilik Heterojenitedir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Distrofin (DMD) geninde çerçeve kayması yapan mutasyonların ölümcül Duchenne distrofisine, çerçeveyi koruyan mutasyonların ise çok daha ılımlı seyreden Becker distrofisine yol açması hangi genetik kuraldır?",
                    {
                        "A": "Alilik Heterojenite",
                        "B": "Lokus Heterojenitesi",
                        "C": "Pleiotropi",
                        "D": "Fenokopi"
                    },
                    "A",
                    {
                        "A": "Doğru! Aynı gen (DMD) üzerinde farklı mutasyonların farklı ağırlıkta hastalık tabloları doğurması alilik heterojenitenin ders kitabı örneğidir.",
                        "B": "Yanlış. Lokus heterojenitesinde farklı genler söz konusudur.",
                        "C": "Yanlış. Pleiotropi tek genin farklı organları tutmasıdır.",
                        "D": "Yanlış. Fenokopi çevresel taklittir."
                    }
                )
            ]
        },
        {
            "slideNumber": 84,
            "title": "Mozaiklik Mekanizması: Somatik Mozaiklik vs Germline (Gonadal) Mozaiklik",
            "subtitle": "Postzigotik mutasyonlar ve sağlıklı ebeveynden tekrarlayan dominant çocuk doğumları",
            "badge": "Mozaiklik",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Mozaiklik; döllenmiş tek bir zigottan köken alan bir bireyde, genetik yapısı birbirinden farklı en az iki veya daha fazla hücre serisinin bir arada bulunmasıdır. Postzigotik (mitotik) mutasyonla oluşur:\n\n- **1. Somatik Mozaiklik:**\n  - Vücut hücrelerinde meydana gelir. Bireyde Blaschko çizgilerini takip eden asimetrik lezyonlar veya segmental tutulum görülür (örneğin McCune-Albright sendromu).\n  - Gelecek kuşaklara aktarılmaz.\n- **2. Germline (Gonadal) Mozaiklik:**\n  - Mutasyon sadece ebeveynin over veya testisindeki germ kök hücrelerinde bulunur; ebeveynin kanında veya vücudunda mutasyon YOKTUR (ebeveyn tamamen sağlıklıdır!).\n  - **Klinik Çıkarım:** Sağlıklı anne ve babadan otozomal dominant bir hastalığa (örneğin Osteogenezis İmperfekta veya Duchenne) sahip birden fazla çocuk doğabilir. Aileye 'yeni mutasyon' denilip %1 yerine yanlışlıkla %0 risk verilirse büyük hekimlik hatası yapılır!",
            "coreContent": {
                "table": {
                    "title": "Somatik ve Germline Mozaiklik Karşılaştırması",
                    "headers": ["Mozaiklik Tipi", "Mutasyonun Oluştuğu Hücre", "Bireydeki Klinik", "Kalıtım ve Tekrarlama Riski"],
                    "rows": [
                        ["Somatik Mozaiklik", "Postzigotik embriyonik somatik hücre", "Segmental lezyon, asimetrik fenotip", "Çocuklara AKTARILMAZ (risk %0)"],
                        ["Germline (Gonadal) Mozaiklik", "Yalnızca over veya testis kök hücresi", "Ebeveyn TAMAMEN SAĞLIKLIDIR", "Sonraki çocuklarda TEKRARLAYABİLİR (%1-5 risk)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Germline (Gonadal) Mozaiklik", "explanation": "Yalnızca gamet üreten gonad hücrelerinde mutasyon bulunması; sağlıklı ebeveynden hasta çocuklar doğmasına yol açar."},
                {"term": "Somatik Mozaiklik", "explanation": "Postzigotik olarak vücut dokularında iki farklı hücre soyunun mozaik olarak bulunması."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Sağlıklı ebeveynlerin birden fazla çocuğunda otozomal dominant bir hastalığın ortaya çıkması GONADAL (GERMLİNE) MOZAİKLİK ile açıklanır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tamamen sağlıklı bir anne ve babanın ilk çocuğu osteogenezis imperfekta (otozomal dominant cam kemik) tanısı alıyor. İkinci gebelikte de aynı dominant hastalığın tekrarlaması en olası hangi genetik mekanizma ile açıklanır?",
                    {
                        "A": "Ebeveynlerden birinde Germline (Gonadal) Mozaiklik bulunması",
                        "B": "X'e bağlı resesif kalıtım",
                        "C": "Azalmış penetrans",
                        "D": "Fenokopi"
                    },
                    "A",
                    {
                        "A": "Doğru! Sağlıklı ebeveynlerin birden fazla dominant anomalili çocuk doğurmasının temel nedeni ebeveyn gonadlarındaki germline mozaikliktir.",
                        "B": "Yanlış. Osteogenezis otozomal dominanttır.",
                        "C": "Yanlış. Penetrans tekrarlamayı açıklamaz.",
                        "D": "Yanlış. Çevresel değildir."
                    }
                )
            ]
        },
        {
            "slideNumber": 85,
            "title": "Yaşa Bağlı Dinamik Fenotip Değişimi: Bebeklikten Erişkinliğe Morfolojik Dönüşüm",
            "subtitle": "Yenidoğanda silik olan dismorfik bulguların puberte ve ergenlikte kristalize olması",
            "badge": "Klinik Seyir",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Dismorfik sendromların fenotipik görünümü donuk bir heykel gibi sabit değildir; büyüme, kemikleşme ve hormonal gelişimle dinamik bir evrim geçirir:\n\n- **Yenidoğan Dönemi Güçlüğü:** Bebeklerde subkutan yağ dokusunun fazlalığı, ödem ve kemiklerin henüz kıkırdak yapıda olması birçok sendromun yüz hatlarını birbirine benzer kılar (yuvarlak yüz, basık burun kökü vb.).\n- **Çocukluk ve Ergenlikte Dönüşüm:**\n  - **Frajil X Sendromu:** Bebeklikte yüz tamamen normal görünebilir; puberteyle birlikte yüz belirgin uzar, çene öne fırlar (prognatizm), kulaklar büyür ve masif **makroorşidizm** ortaya çıkar.\n  - **Williams Sendromu:** Bebeklikteki hafif periorbital dolgunluk, yaş ilerledikçe karakteristik yıldızsı iris ve elfin yüzüne dönüşür.\n  - **Sotos Sendromu (Serebral Gigantizm):** Çocuklukta aşırı hızlı büyüme ve belirgin sivri çene varken, erişkinlikte boy normal sınırlara yaklaşabilir.",
            "coreContent": {
                "table": {
                    "title": "Yaşa Bağlı Fenotip Değişiminin Klasik Örnekleri",
                    "headers": ["Sendrom", "Bebeklik / Yenidoğan Fenotipi", "Puberte ve Erişkinlik Fenotipi"],
                    "rows": [
                        ["Frajil X Sendromu", "Normal yüz, hafif hipotoni, nonspesifik", "Uzun ince yüz, belirgin çene, makroorşidizm"],
                        ["Williams Sendromu", "Periorbital ödem, huzursuzluk, kolik", "Elfin yüzü, yıldızsı iris, kalın dudaklar"],
                        ["Prader-Willi Sendromu", "Ağır hipotoni, zayıf emme, zayıflık", "Doymak bilmeyen iştah (hiperfaji), masif obezite"],
                        ["Down Sendromu (T21)", "Brakisefali, basık burun kökü, tek fleksiyon çizgisi", "Erken yaşta katarakt, Alzheimer benzeri demans"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Dinamik Fenotip", "explanation": "Genetik hastalığın fiziksel morfolojisinin yaş evrelerine göre başkalaşım göstermesi."},
                {"term": "Sotos Sendromu (NSD1)", "explanation": "Çocuklukta aşırı büyüme, makrosefali, geniş alın ve sivri çene ile seyreden sendrom."}
            ],
            "spotPearls": [
                "Frajil X sendromunun tipik fenotipi (uzun yüz, büyük kulaklar, makroorşidizm) yenidoğan döneminde saptanamaz; puberteyle birlikte belirginleşir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Frajil X Sendromunda Yaşa Bağlı Değişim",
                    "Yenidoğan ve Erken Süt Çocukluğu",
                    "Puberte ve Erişkin Dönemi",
                    [
                        "Yüz hatları tamamen normal veya nonspesifiktir",
                        "Testis boyutları normal sınırlardadır",
                        "Hafif hipotoni ve gelişim basamaklarında gecikme vardır",
                        "Klinik tanı koymak çok zordur"
                    ],
                    [
                        "Yüz belirgin şekilde uzar ve daralır",
                        "Prognatizm (çene çıkıklığı) ve devasa kulaklar kristalize olur",
                        "Puberte sonrası masif Makroorşidizm (testis büyümesi) gelişir",
                        "Otizm spektrum bozukluğu ve hiperaktivite belirginleşir"
                    ]
                )
            ]
        },
        {
            "slideNumber": 86,
            "title": "Epigenetik Mekanizmalar: Genomik İmprinting ve Uniparental Dizomi (UPD)",
            "subtitle": "DNA sekansı değişmeden gen ifadesinin ebeveyn kökenine göre susturulması",
            "badge": "Epigenetik",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Epigenetik; DNA baz diziliminde hiçbir nükleotid değişikliği olmaksızın, DNA metilasyonu ve histon modifikasyonlarıyla gen ifadesinin (ekspresyonunun) kapatılması veya açılmasıdır:\n\n- **Genomik İmprinting:** Bazı genler yalnızca anneden geldiğinde aktifken, bazıları yalnızca babadan geldiğinde aktiftir (monogenik monoalelik ekspresyon).\n- **15q11-q13 Bölgesi ve İki Zıt Sendrom:**\n  - **Prader-Willi Sendromu:** Babadan gelen 15q11-q13 bölgesinin delesyonu veya Maternal Uniparental Dizomi (her iki 15. kromozomun da anneden gelmesi). Yenidoğanda hipotoni, çocuklukta doymama hissi (hiperfaji) ve obezite.\n  - **Angelman Sendromu:** Anneden gelen 15q11-q13 bölgesindeki UBE3A geninin delesyonu veya Paternal Uniparental Dizomi. Ağır zeka geriliği, konuşamama, ataksik kukla yürüyüşü ve uygunsuz kahkahalar (Mutlu Kukla / Happy Puppet).\n- **Uniparental Dizomi (UPD):** Bireyin belirli bir kromozom çiftinin her iki kopyasını da tek bir ebeveynden alması durumudur.",
            "coreContent": {
                "table": {
                    "title": "15q11-q13 Lokusunda Prader-Willi vs Angelman Ayırıcı Tanısı",
                    "headers": ["Özellik", "Prader-Willi Sendromu (PWS)", "Angelman Sendromu (AS)"],
                    "rows": [
                        ["Eksik Olan Ebeveyn İfadesi", "Babadan gelen aktif alel eksik", "Anneden gelen aktif alel eksik (UBE3A)"],
                        ["En Sık Genetik Neden (%70)", "Paternal 15q11-q13 delesyonu", "Maternal 15q11-q13 delesyonu"],
                        ["Uniparental Dizomi Tipi (%25)", "Maternal UPD (Her iki kromozom anneden)", "Paternal UPD (Her iki kromozom babadan)"],
                        ["Kardinal Klinik Tablo", "Yenidoğanda hipotoni, çocukta hiperfaji ve obezite", "Konuşamama, mikrosefali, ataksik yürüyüş, uygunsuz kahkaha"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Genomik İmprinting", "explanation": "Gen ifadesinin alelin anne ya da babadan kalıtılmasına bağlı olarak epigenetik susturulması."},
                {"term": "Uniparental Dizomi (UPD)", "explanation": "Bir kromozom çiftinin her iki kopyasının da tek bir ebeveynden miras alınması durumu."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] 15q11-q13 bölgesinde paternal delesyon PRADER-WILLI sendromuna; maternal UBE3A delesyonu ise ANGELMAN sendromuna yol açar."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bir çocukta 15. kromozom çiftinin her ikisinin de anneden kalıtıldığı (maternal uniparental dizomi) ve babadan gelen 15. kromozomun bulunmadığı saptanıyor. Bu çocukta hangi klinik sendrom gelişir?",
                    {
                        "A": "Prader-Willi Sendromu",
                        "B": "Angelman Sendromu",
                        "C": "Williams Sendromu",
                        "D": "Turner Sendromu"
                    },
                    "A",
                    {
                        "A": "Doğru! Babadan gelen aktif 15q11-q13 genleri bulunmadığında (maternal UPD) çocukta Prader-Willi sendromu gelişir.",
                        "B": "Yanlış. Paternal UPD olsaydı Angelman sendromu gelişirdi.",
                        "C": "Yanlış. Williams 7q11.23 delesyonudur.",
                        "D": "Yanlış. Turner 45,X'tir."
                    }
                )
            ]
        },
        {
            "slideNumber": 87,
            "title": "X Kromozomu İnaktivasyonu (Lyonizasyon): Taşıyıcı Dişilerde Fenotipik Belirtiler",
            "subtitle": "Dişi embriyoda blastokist evresinde rastlantısal susturulan X kromozomu",
            "badge": "Epigenetik Dozaj",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Memeli dişilerinde (46,XX) iki X kromozomu bulunurken erkeklerde (46,XY) tek X kromozomu bulunur. Dozaj dengesini sağlamak için embriyogenezin blastokist aşamasında (yaklaşık 16. gün) her somatik hücredeki X kromozomlarından biri rastlantısal ve kalıcı olarak susturulur (Lyon Hipotezi):\n\n- **Barr Cismimi:** Susturulan heterokromatinleşmiş inaktif X kromozomu, interfaz çekirdeğinde nükleer membranın kenarında koyu boyanan Barr cisimciği olarak görülür.\n- **Çarpık (Skewed) X İnaktivasyonu:** Normalde %50 anne X'i, %50 baba X'i susturulur. Ancak rastlantısal olarak normal geni taşıyan X kromozomu hücrelerin %80-90'ında susturulursa, **X'e bağlı resesif bir hastalığı taşıyan dişi birey (örneğin hemofili veya Duchenne taşıyıcısı bir kız çocuğu) erkekler gibi klinik hastalık belirtileri gösterebilir!**",
            "coreContent": {
                "table": {
                    "title": "Lyonizasyon Prensibi ve Klinik Yansımaları",
                    "headers": ["Parametre", "Biyolojik Mekanizma", "Klinik Yansıması"],
                    "rows": [
                        ["Susturucu Gen", "XIST lncRNA geni (Xq13.2)", "X kromozomunu metilleyerek susturur"],
                        ["İnaktif X Morfolojisi", "Barr Cisimciği (Seks kromatini)", "Dişilerde 1 adet, Klinefelter'da 1 adet, Turner'da 0 adet"],
                        ["Çarpık (Skewed) İnaktivasyon", "Sağlam alelin aşırı oranda susturulması", "Taşıyıcı kadında semptomatik Duchenne / Hemofili"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Lyonizasyon", "explanation": "Dişi memeli embriyosunda blastokist evresinde bir X kromozomunun rastlantısal ve kalıcı olarak susturulması."},
                {"term": "Barr Cisimciği", "explanation": "İnaktive olmuş heterokromatik X kromozomunun mikroskop altında görülen kondanse hali."}
            ],
            "spotPearls": [
                "X'e bağlı resesif hastalık taşıyıcısı olan bir kadının semptom göstermesi, sağlam X kromozomunun aşırı oranda inaktive olduğu 'Çarpık (Skewed) X İnaktivasyonu' ile açıklanır."
            ],
            "interactiveElements": [
                make_cloze(
                    "Dişi somatik hücrelerinde inaktive olan heterokromatik X kromozomunun çekirdekte oluşturduğu yoğun kütleye [Barr cisimciği] adı verilir.",
                    "Barr cisimciği",
                    "Seks kromatini gövdesi",
                    "Barr cisimciği formülü: X kromozomu sayısı - 1'dir (Normal dişi: 1, Turner: 0, Klinefelter: 1)."
                )
            ]
        },
        {
            "slideNumber": 88,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Klinik Genetik Kuralları ve Mekanizmalar Sentez Tablosu",
            "subtitle": "Pleiotropi, heterojenite, penetrans ve epigenetik kurallarını tek tabloda pekiştirin",
            "badge": "Hafıza Matrisi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu kontrol noktası; genetik hastalıkların kalıtım kalıplarını ve fenotipik çeşitliliğini yöneten temel ilkeleri tek bir interaktif ezber tablosunda sentezler.\n\nMaskeli hücrelere tıklayarak gizlenen genetik kuralları, mekanizma tanımlarını ve klasik hastalık örneklerini hafızanızdan geri çağırın!",
            "coreContent": {
                "table": {
                    "title": "Klinik Genetik Kuralları Büyük Sentez Tablosu",
                    "headers": ["Genetik İlke", "Temel Mekanizma", "Kritik Prototip Hastalık", "Sınav Püf Noktası"],
                    "rows": [
                        ["Pleiotropi", "Tek gen -> Çoklu bağımsız sistem", "Marfan Sendromu (FBN1)", "Göz + Kalp + İskelet tutulumu"],
                        ["Değişken Ekspresyon", "Aynı mutasyon -> Farklı şiddet", "Nörofibromatozis Tip 1 (NF1)", "Herkes hasta, ağırlık derecesi farklı"],
                        ["Azalmış Penetrans", "Mutasyon var -> Klinik tablo yok", "BRCA1 / Retinoblastom", "Soyağacında kuşak atlama yanılsaması"],
                        ["Lokus Heterojenitesi", "Farklı genler -> Aynı hastalık", "Tuberoz Skleroz (TSC1 / TSC2)", "Farklı kromozomlardaki bağımsız genler"],
                        ["Alilik Heterojenite", "Aynı gen -> Farklı hastalıklar", "DMD: Duchenne vs Becker", "Aynı gende frameshift vs in-frame farkı"],
                        ["Fenokopi", "Çevresel etken -> Genetik taklit", "Talidomid vs Holt-Oram", "DNA normaldir, tekrarlama riski yoktur"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Hafıza Matrisi", "explanation": "Genetik ilkelerin moleküler tanımlarını ve prototip hastalıklarını özetleyen kilit tablo."},
                {"term": "Klinik Genetik Sentezi", "explanation": "Genotip ile fenotip arasındaki non-lineer kuralların ayırıcı tanıda kullanılması."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Sınavda en sık sorulan 3 ayrım: Pleiotropi = tek gen çoklu organ; Lokus heterojenitesi = farklı gen aynı hastalık; Alilik heterojenite = aynı gen farklı hastalık!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Genetik İlkeler ve Prototip Hastalıklar Ezber Matrisi",
                    ["Genetik Kural", "Biyolojik Mekanizması", "Ders Kitabı Prototipi", "Sınav Soru İpucu"],
                    [
                        [
                            ("Pleiotropi", False),
                            ("Tek gen -> Çoklu bağımsız sistem tutulumu", True, "Tek gen çoklu organ"),
                            ("Marfan Sendromu (FBN1)", True, "Marfan"),
                            ("Göz, kalp ve iskelet aynı anda tutulur", False)
                        ],
                        [
                            ("Değişken Ekspresyon", False),
                            ("Aynı mutasyon -> Bireylerde farklı klinik şiddet", True, "Farklı şiddet"),
                            ("Nörofibromatozis Tip 1 (NF1)", True, "NF1"),
                            ("Herkes hastadır ama ağırlık değişir", False)
                        ],
                        [
                            ("Lokus Heterojenitesi", False),
                            ("Farklı genler -> Aynı klinik hastalık tablosu", True, "Farklı gen aynı hastalık"),
                            ("Tuberoz Skleroz (TSC1 ve TSC2)", True, "Tuberoz skleroz"),
                            ("Farklı kromozomlardaki mutasyonlar", False)
                        ],
                        [
                            ("Alilik Heterojenite", False),
                            ("Aynı tek gen -> Farklı ağırlıkta hastalıklar", True, "Aynı gen farklı hastalık"),
                            ("Distrofin (Duchenne vs Becker)", True, "Duchenne vs Becker"),
                            ("Frameshift ağır, in-frame hafiftir", False)
                        ],
                        [
                            ("Fenokopi", False),
                            ("Çevresel etkenin genetik sendromu taklit etmesi", True, "Çevresel taklit"),
                            ("Talidomid vs Holt-Oram sendromu", True, "Talidomid"),
                            ("Genom normaldir, tekrarlama riski yoktur", False)
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Tek bir genetik mekanizmanın hem Marfan'daki çoklu sistem bulgularını hem de bir gendeki kusurun bağımsız organları etkilemesini tanımlayan terim hangisidir?",
                    {
                        "A": "Pleiotropi",
                        "B": "Penetrans",
                        "C": "Mozaiklik",
                        "D": "Fenokopi"
                    },
                    "A",
                    {
                        "A": "Doğru! Tek bir gendeki kusurun çoklu bağımsız organları etkilemesi pleiotropidir.",
                        "B": "Yanlış. Penetrans hastalığın ortaya çıkma yüzdesidir.",
                        "C": "Yanlış. Mozaiklik iki farklı hücre hattıdır.",
                        "D": "Yanlış. Fenokopi çevresel taklittir."
                    }
                )
            ]
        }
    ]
