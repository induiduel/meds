#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 2 Builder: Kromozom Düzensizlikleri & Mekanizmalar
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
            "slideNumber": 10,
            "title": "Kromozom Düzensizliklerinin Genel Sınıflaması: Sayısal ve Yapısal Değişimler",
            "subtitle": "Genomun mikroskobik düzeydeki mimari ve dozaj dengesizlikleri",
            "badge": "Sınıflandırma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Kromozom anomalileri, insan patolojisinde spontan düşüklerin ve multipl konjenital malformasyonların en yaygın genetik nedenlerindendir.\n\nKromozomal patolojiler temel mekanizmalarına göre iki ana grupta incelenir:\n- **Sayısal Anomaliler:** Normal diploid kromozom sayısının (2n = 46) değişmesidir; fazladan veya eksik kromozom bulunması gen dozaj dengesini bozar.\n  - **Yapısal Anomaliler:** Kromozom kolları arasında meydana gelen kırıklar ve hatalı birleşmeler sonucu parça kaybı, fazlalığı veya yön değiştirmesidir.\n  - **Klinik Ağırlık:** Sayısal anomaliler ve dengesiz yapısal anomaliler genellikle çoklu organ yetmezliği ve zihinsel etkilenim ile seyreder.\n\n> 📌 **Temel Kural:** Spontan düşüklerin yaklaşık ==%50'sinden== kromozomal anomaliler sorumludur!",
            "coreContent": {
                "table": {
                    "title": "Kromozomal Anomali Ana Grupları",
                    "headers": ["Anomali Tipi", "Mekanizma", "En Sık Klinik Örnekler"],
                    "rows": [
                        ["Sayısal (Aneuploidi)", "Mayotik ayrılmama (nondisjunction)", "Trizomi 21 (Down), 45,X (Turner), 47,XXY (Klinefelter)"],
                        ["Sayısal (Poliploidi)", "Polispermi veya mayotik blokaj", "Triploidi (69,XXX / 69,XXY), Tetraploidi (92,XXYY)"],
                        ["Yapısal Dengeli", "Kırık ve birleşme, gen kaybı yok", "Resiprokal translokasyon, perisentrik/parasentrik inversiyon"],
                        ["Yapısal Dengesiz", "Parça kaybı (delesyon) veya kazanımı (duplikasyon)", "Cri-du-chat (5p-), DiGeorge (22q11.2 del), Halka kromozom"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Aneuploidi", "explanation": "Kromozom sayısının haploid takımın tam katı olmayacak şekilde bir veya birkaç kromozom eksikliği veya fazlalığı göstermesi."},
                {"term": "Poliploidi", "explanation": "Hücrede haploid kromozom takımının (n) tam katları şeklinde (3n, 4n) artış bulunması durumu."}
            ],
            "spotPearls": [
                "İlk trimester spontan düşüklerinin yaklaşık %50'sinden kromozomal anomaliler (en sık Trizomi 16 ve 45,X) sorumludur."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "İlk trimesterde gerçekleşen spontan düşük materyallerinde en sık saptanan genetik patoloji sınıfı hangisidir?",
                    {
                        "A": "Kromozomal anomaliler (yaklaşık %50)",
                        "B": "X'e bağlı resesif tek gen mutasyonları",
                        "C": "Otozomal dominant mitokondriyal DNA delesyonları",
                        "D": "Yalnızca çevresel toksin maruziyeti"
                    },
                    "A",
                    {
                        "A": "Doğru! İlk trimester abortuslarının yaklaşık %50'sinde sayısal veya ağır yapısal kromozom anomalileri bulunur.",
                        "B": "Yanlış. Tek gen mutasyonları erken spontan abortusların birincil çoğunluğunu oluşturmaz.",
                        "C": "Yanlış. Mitokondriyal kalıtım maternaldir ve erken abortusların yarısından sorumlu değildir.",
                        "D": "Yanlış. Çevresel toksinler önemlidir ancak abortusların yarısı doğrudan kromozomal dengesizlik kökenlidir."
                    }
                ),
                make_before_after(
                    "Sayısal Anomaliler (Aneuploidi)",
                    "Dengeli Yapısal Anomaliler",
                    ["Gen dozajı bozulmuştur (2n+1 veya 2n-1)", "Genellikle ağır fenotipik bulgu verir", "Spontan abortus veya sendrom oluşturur"],
                    ["Genetik materyal miktarı korunmuştur", "Taşıyıcı birey fenotipik olarak tamamen normaldir", "Asıl risk gametlerinde dengesizlik oluşmasıdır"]
                )
            ]
        },
        {
            "slideNumber": 11,
            "title": "Sayısal Kromozom Anomalileri: Aneuploidi ve Trizomi/Monozomi Kavramı",
            "subtitle": "Tek bir kromozomun fazlalığı veya eksikliğinin biyolojik sonuçları",
            "badge": "Mekanizma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Aneuploidi; hücrede normalde ikişer adet bulunan homolog kromozom çiftlerinden birinin üç kopyaya çıkması (trizomi: 2n+1) veya tek kopyaya inmesidir (monozomi: 2n-1).\n\nİnsan genomunda gen dozajı katı bir dengeye tabidir:\n- **Otozomal Monozomiler:** Otozomal bir kromozomun tam monozomisi (örneğin monozomi 21) embriyonik yaşamla kesinlikle bağdaşmaz ve erken dönemde letaldir.\n  - **Gonozomal Monozomi:** Canlı doğabilen tek tam monozomi ==Turner Sendromudur (45,X)==.\n  - **Otozomal Trizomiler:** Canlı doğuma ulaşabilen başlıca otozomal trizomiler Trizomi 21 (Down), Trizomi 18 (Edwards) ve Trizomi 13 (Patau) sendromlarıdır.\n\n> 🚨 **Hayati Sınav Kuralı:** İnsanda canlı doğabilen TEK tam monozomi 45,X'tir; hiçbir otozomal tam monozomi canlı doğamaz!",
            "coreContent": {
                "table": {
                    "title": "Canlı Doğabilen Başlıca Aneuploidiler",
                    "headers": ["Kromozom Formülü", "Sendrom Adı", "Temel Fenotipik Özellik"],
                    "rows": [
                        ["47,XX,+21 / 47,XY,+21", "Down Sendromu", "Brakisefali, epikantus, hipotoni, endokardiyal yastık defekti, zeka geriliği"],
                        ["47,XX,+18 / 47,XY,+18", "Edwards Sendromu", "Belirgin oksiput, fleksiyon kontraktürlü el (üst üste binen parmaklar), rocker-bottom ayak"],
                        ["47,XX,+13 / 47,XY,+13", "Patau Sendromu", "Holoprozensefali, mikroftalmi, yarık dudak/damak, postaksiyel polidaktili"],
                        ["45,X", "Turner Sendromu", "Kısa boy, yele boyun, gonadal disgenezi (çizgi gonad), aort koarktasyonu"],
                        ["47,XXY", "Klinefelter Sendromu", "Uzun boy, jinekomasti, küçük sert testisler, infertilite, hipergonadotropik hipogonadizm"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Trizomi", "explanation": "Belirli bir kromozomun iki yerine üç kopya halinde bulunması durumu (örneğin Trizomi 21)."},
                {"term": "Turner Sendromu (45,X)", "explanation": "Tek bir X kromozomu varlığıyla karakterize, yele boyun ve gonadal disgenezi ile seyreden canlı monozomi."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Canlı doğumla bağdaşan tek tam monozomi 45,X (Turner Sendromu) tablosudur; otozomal tam monozomiler uterusta letaldir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "İnsan türünde canlı doğumla bağdaşan ve fenotipik olarak yaşayabilen TEK tam monozomi tablosu hangisidir?",
                    {
                        "A": "Turner Sendromu (45,X)",
                        "B": "Monozomi 21",
                        "C": "Monozomi 1",
                        "D": "Monozomi 18"
                    },
                    "A",
                    {
                        "A": "Doğru! Canlı doğumla bağdaşan tek tam monozomi 45,X'tir. Tüm tam otozomal monozomiler erken embriyonik letaldir.",
                        "B": "Yanlış. Monozomi 21 tam monozomi olarak canlı doğamaz.",
                        "C": "Yanlış. Kromozom 1 en büyük otozomdur ve monozomisi derhal letaldir.",
                        "D": "Yanlış. Trizomisi (Edwards) canlı doğabilir ancak monozomisi letaldir."
                    }
                ),
                make_cloze(
                    "İnsan genomunda canlı doğumla bağdaşabilen tek tam monozomi tablosu Turner sendromu (45,X) olarak adlandırılır.",
                    "Turner sendromu",
                    "45,X karyotipi"
                )
            ]
        },
        {
            "slideNumber": 12,
            "title": "Mayotik Ayrılmama (Nondisjunction): İleri Anne Yaşı ve Trizomi 21 Mekanizması",
            "subtitle": "Mayoz bölünmedeki kohezin kaybı ve kromozomların aynı kutba göçü",
            "badge": "Mekanizma",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Aneuploidilerin ezici çoğunluğu, gametogenez sırasında homolog kromozomların (Mayoz I) veya kardeş kromatitlerin (Mayoz II) birbirinden ayrılamayıp aynı kutba gitmesi (nondisjunction) sonucu ortaya çıkar.\n\nBu patolojinin altında yatan en belirleyici faktör maternal yaşlanmadır:\n- **Mayotik Duraklama:** Oositler intrauterin 5. ayda ==Mayoz I profazında (diploten/diktiyoten evresi)== duraklar ve ovülasyona kadar on yıllarca bu şekilde bekler.\n  - **Kohezin Bozulması:** Bekleme süresi uzadıkça kromozomları bir arada tutan kohezin proteinleri degrade olur ve iğ iplikleri mikrotübül kinetokor bağlantıları kararsızlaşır.\n  - **Sonuç Gametler:** Döllenme sonrasında trizomik (2n+1) veya monozomik (2n-1) zigotlar meydana gelir.",
            "medicalTerms": [
                {"term": "Nondisjunction (Ayrılmama)", "explanation": "Hücre bölünmesinde homolog kromozomların veya kromatitlerin zıt kutuplara ayrılamaması olayı."},
                {"term": "Diktiyoten Evresi", "explanation": "Dişi oositlerinin fötal dönemden ovülasyona kadar yıllarca beklediği Mayoz I profaz duraklama basamağı."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Trizomi 21 olgularının %95'i maternal Mayoz I'deki ayrılmama (nondisjunction) hatasından kaynaklanır ve ileri anne yaşıyla doğrudan ilişkilidir."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Maternal Nondisjunction ve Trizomi Kaskadı",
                    [
                        "Fetal oogenezde oositler Mayoz I diploten (diktiyoten) evresinde duraklar.",
                        "Yıllar geçtikçe (özellikle 35 yaş üstü) kohezin kompleksleri zayıflar.",
                        "Mayoz I tamamlanırken 21. kromozom çifti ayrılamaz ve aynı oosite gider.",
                        "Normal haploid sperm (n=23) ile döllenen disomik oosit (n=24) trizomi 21 (2n=47) zigotunu oluşturur."
                    ]
                ),
                make_micro_quiz(
                    "Serbest Trizomi 21 (Down Sendromu) vakalarının yaklaşık %95'inde temel mekanizma ve hücresel köken hangisidir?",
                    {
                        "A": "Maternal Mayoz I nondisjunction (ayrılmama)",
                        "B": "Paternal Mayoz II nondisjunction",
                        "C": "Mitotik anafaz gecikmesi (anaphase lag)",
                        "D": "Robertsonyan dengeli translokasyon"
                    },
                    "A",
                    {
                        "A": "Doğru! Down sendromunun %95'i serbest trizomidir ve bunun ezici çoğunluğu maternal Mayoz I evresindeki ayrılmama hatasından türer.",
                        "B": "Yanlış. Paternal köken yalnızca %5-10 civarındadır.",
                        "C": "Yanlış. Anafaz gecikmesi mozaikliğe yol açar.",
                        "D": "Yanlış. Robertsonyan translokasyon Down sendromunun sadece %3-4'ünden sorumludur."
                    }
                )
            ]
        },
        {
            "slideNumber": 13,
            "title": "Mitotik Ayrılmama ve Mozaiklik (Mosaicism)",
            "subtitle": "Postzigotik bölünmelerde oluşan iki veya daha fazla hücre serisi",
            "badge": "Genetik Çeşitlilik",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Mozaiklik; tek bir zigottan köken alan bir bireyde genetik veya kromozomal olarak birbirinden farklı en az iki hücre serisinin bir arada bulunmasıdır.\n\nMozaiklik mekanizması mayotik değil, postzigotik (fertilizasyon sonrası) mitoz bölünmelerdeki aksaklıklardan doğar:\n- **Postzigotik Nondisjunction:** Normal diploid (46,XX) bir zigotun erken embriyonik mitozunda ayrılmama gerçekleşirse 47,XX,+21 ve 45,XX,-21 hücreleri oluşur; monozomik hücre ölürken trizomik ve normal hücreler yaşar.\n  - **Trizomi Kurtarma (Trisomy Rescue):** Trizomik bir zigottan mitoz sırasında fazla kromozomun atılmasıyla normal diploid hücre hattı kurtarılır (ancak bu uniparental dizomiye yol açabilir!).\n  - **Klinik Fenotip:** Mozaik olgularda klinik tablo, etkilenen hücrelerin organ dağılımına ve oranına bağlı olarak tam trizomiye göre belirgin şekilde daha hafif seyreder.",
            "medicalTerms": [
                {"term": "Mozaiklik", "explanation": "Tek bir zigottan gelişen organizmada genetik yapıları birbirinden farklı hücre hatlarının bulunması."},
                {"term": "Trizomi Kurtarma (Trisomy Rescue)", "explanation": "Trizomik bir hücreden mitotik hata sonucu fazla üçüncü kromozomun dışarı atılması mekanizması."}
            ],
            "spotPearls": [
                "Mozaik Down sendromlu bireylerde zihinsel etkilenim ve fenotipik dismorfik bulgular normal hücre hattının varlığı nedeniyle daha ılımlıdır."
            ],
            "interactiveElements": [
                make_before_after(
                    "Tam (Serbest) Trizomi",
                    "Mozaik Trizomi",
                    ["Hata mayozda (gametogenez) oluşur", "Vücuttaki TÜM hücreler 47 kromozomludur", "Fenotipik tablo tam şiddetinde yansır"],
                    ["Hata mitozda (postzigotik) oluşur", "Normal (46) ve trizomik (47) hücreler bir aradadır", "Fenotip etkilenen doku oranına göre daha hafiftir"]
                ),
                make_micro_quiz(
                    "Mozaik karyotipli bir Down sendromu hastasında hücresel anormalliğin başlangıç zamanı ve mekanizması nedir?",
                    {
                        "A": "Fertilizasyon sonrasında mitoz bölünmede gerçekleşen postzigotik nondisjunction",
                        "B": "Oogenez sırasında Mayoz I evresinde gerçekleşen mayotik nondisjunction",
                        "C": "Spermatogenez sırasında Mayoz II'de kromatitlerin yapışması",
                        "D": "İki ayrı spermin aynı yumurtayı döllemesi (dispermi)"
                    },
                    "A",
                    {
                        "A": "Doğru! Mozaiklik tek bir zigot oluştuktan sonra mitotik bölünmeler esnasında (postzigotik) ortaya çıkar.",
                        "B": "Yanlış. Mayotik nondisjunction vücuttaki tüm hücrelerin trizomik olmasına (serbest trizomi) yol açar.",
                        "C": "Yanlış. Mayotik hatalar tam aneuploidi yapar.",
                        "D": "Yanlış. Dispermi triploidiye (69 kromozom) yol açar."
                    }
                )
            ]
        },
        {
            "slideNumber": 14,
            "title": "Poliploidi: Triploidi (69 Kromozom) ve Tetraploidi (92 Kromozom)",
            "subtitle": "Tüm genom setinin katlanması ve hidatidiform mol patolojisi",
            "badge": "Genom Katlanması",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Poliploidi, haploid kromozom takımının (n=23) tam katları şeklinde bulunmasıdır. En sık rastlanan form ==Triploidi (3n = 69)== ve Tetraploididir (4n = 92).\n\nTriploidinin etiyolojisinde iki temel mekanizma ve çok farklı iki klinik fenotip vardır:\n- **Diandri (Fazla Paternal Genom):** Bir oositin iki sperm tarafından döllenmesi (dispermi) veya diploid bir spermle döllenmesiyle oluşur. Genişlemiş, kistik plasenta (parsiyel mol hidatidiform) ve mikroensefalik ufak fetüs ile karakterizedir.\n  - **Digini (Fazla Maternal Genom):** Mayoz bölünmesini tamamlayamamış diploid bir oositin normal spermle döllenmesiyle oluşur. Çok küçük plasenta, şiddetli intrauterin gelişme geriliği ve büyük kafa ile seyreder.\n  - **Klinik Sonuç:** Triploidiler spontan abortusların %15-20'sini oluşturur; canlı doğan çok nadir olgular ise doğumdan sonraki ilk saatler/günler içinde kaybedilir.",
            "coreContent": {
                "table": {
                    "title": "Diandrik ve Diginik Triploidi Karşılaştırması",
                    "headers": ["Özellik", "Diandrik Triploidi (Fazla Babadan)", "Diginik Triploidi (Fazla Anneden)"],
                    "rows": [
                        ["Köken", "2 sperm + 1 yumurta (dispermi) (%80)", "1 diploid yumurta + 1 sperm (%20)"],
                        ["Plasenta Morfolojisi", "Çok büyük, kistik, parsiyel mol hidatidiform", "Çok küçük, fibrotik, kistsiz plasenta"],
                        ["Fetal Gelişim", "Nispeten korunmuş beden, mikroensefali", "Şiddetli asimetrik IUGR, makrosefali"],
                        ["Maternal Risk", "Koryokarsinom ve preeklampsi riski yüksek", "Preeklampsi riski daha düşük"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Triploidi", "explanation": "Hücrede 3 takım haploid kromozom (3n = 69) bulunması durumu."},
                {"term": "Dispermi", "explanation": "Tek bir oositin aynı anda iki ayrı sperm tarafından döllenmesi mekanizması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Parsiyel mol hidatidiform tablosu diandrik triploidi (iki sperm + bir yumurta) sonucu oluşur; kistik dev plasenta tipiktir."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Triploidi Mekanizmaları ve Ayırıcı Tanı Tablosu",
                    ["Parametre", "Diandrik (Paternal Fazlalık)", "Diginik (Maternal Fazlalık)"],
                    [
                        [("Oluşum Mekanizması", False), ("Dispermi (2 Sperm)", True, "İki sperm"), ("Diploid Oosit", True, "Yumurta hatası")],
                        [("Plasenta Boyutu", False), ("Dev, Kistik Mol", True, "Parsiyel mol"), ("Çok Küçük, Atrofik", True, "Kistsiz")],
                        [("Fetus Morfolojisi", False), ("Orantılı, Mikrosefali", True, "Küçük baş"), ("Ağır IUGR, Makrosefali", True, "Büyük baş")]
                    ]
                ),
                make_micro_quiz(
                    "Ultrasonografide dev kistik plasenta (parsiyel mol hidatidiform) ve çoklu anomalili triploidik bir fetüs saptandığında en olası genetik mekanizma nedir?",
                    {
                        "A": "Diandri (Bir yumurtanın iki sperm tarafından döllenmesi)",
                        "B": "Digini (Diploid bir yumurtanın döllenmesi)",
                        "C": "Maternal Mayoz I nondisjunction",
                        "D": "Robertsonyan translokasyon"
                    },
                    "A",
                    {
                        "A": "Doğru! Fazla paternal genom (diandri / dispermi) plasental aşırı proliferasyona ve parsiyel mole yol açar.",
                        "B": "Yanlış. Diginik triploidide plasenta kistik değil, tam aksine çok küçük ve fibrotiktir.",
                        "C": "Yanlış. Mayotik nondisjunction trizomi yapar (47 kromozom), triploidi (69 kromozom) yapmaz.",
                        "D": "Yanlış. Translokasyon yapısal bir anomalisidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 15,
            "title": "Yapısal Kromozom Düzensizlikleri: Kırıklar, Yeniden Düzenlenmeler ve Dozaj",
            "subtitle": "Kromatin ipliklerinin kopması, DNA tamir defektleri ve dengesizlikler",
            "badge": "Mekanizma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Yapısal kromozom anomalileri, DNA çift zincir kırıkları (double-strand break) ve ardından gelen hatalı yeniden birleşmeler sonucu ortaya çıkar.\n\nYapısal anomalilerin klinik kaderini 'denge' belirler:\n- **Dengeli Yeniden Düzenlenmeler (Balanced):** Genetik materyalde net bir kayıp veya kazanım yoktur; sadece parçaların konumu değişmiştir. Taşıyıcı birey genellikle sağlıklıdır ancak gametogenezde dengesiz gamet üretme riski taşır.\n  - **Dengesiz Yeniden Düzenlenmeler (Unbalanced):** Kromozom parçasında delesyon (kayıp) veya duplikasyon (fazlalık) vardır. Dozaj dengesizliği nedeniyle zeka geriliği, dismorfoloji ve konjenital malformasyonlar kaçınılmazdır.\n  - **Kritik Kural:** Yapısal anomalilerin çoğu de novo ortaya çıkabileceği gibi dengeli taşıyıcı ebeveynden de kalıtılabilir.",
            "medicalTerms": [
                {"term": "Dengeli Düzenlenme", "explanation": "Genomda net baz kaybı veya fazlalığı olmaksızın parçaların yer değiştirmesi."},
                {"term": "Dengesiz Düzenlenme", "explanation": "Genetik materyal kaybı (delesyon) veya kazanımı (duplikasyon) içeren anomali."}
            ],
            "spotPearls": [
                "Dengeli translokasyon taşıyıcısı bireyler fenotipik olarak sağlıklıdır; ancak tekrarlayan gebelik kayıpları ve anomalili çocuk doğurma riski yüksektir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Dengeli Düzenlenme (Balanced)",
                    "Dengesiz Düzenlenme (Unbalanced)",
                    ["Materyal kaybı veya kazanımı yoktur", "Birey genellikle tamamen sağlıklıdır", "Klinik risk: Gamet anomalileri ve düşükler"],
                    ["Materyal kaybı (delesyon) veya fazlalığı vardır", "Bireyde sendrom, dismorfoloji ve zeka geriliği görülür", "Gen dozaj dengesi bozulmuştur"]
                ),
                make_micro_quiz(
                    "Fenotipik olarak tamamen sağlıklı olan ancak tekrarlayan 3 adet spontan abortus öyküsü bulunan bir çiftte öncelikle şüphelenilmesi gereken genetik patoloji nedir?",
                    {
                        "A": "Ebeveynlerden birinde dengeli resiprokal veya Robertsonyan translokasyon taşıyıcılığı",
                        "B": "Ebeveynde serbest trizomi 21 varlığı",
                        "C": "Ebeveynde homozigot letal delesyon bulunması",
                        "D": "Bebeklerin hepsinde triploidi mutasyonu kalıtılması"
                    },
                    "A",
                    {
                        "A": "Doğru! Dengeli translokasyon taşıyıcıları fenotipik olarak sağlıklıdır ancak mayozda dengesiz gametler üreterek tekrarlayan düşüklere yol açarlar.",
                        "B": "Yanlış. Serbest trizomi 21 taşıyıcı değil, fenotipik Down sendromludur.",
                        "C": "Yanlış. Homozigot letal ebeveyn yaşayamaz.",
                        "D": "Yanlış. Triploidi kalıtılmaz, rastlantısal döllenme hatasıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 16,
            "title": "Resiprokal Translokasyonlar: Homolog Olmayan Kromozomlar Arası Değiş-Tokuş",
            "subtitle": "Kromozom kollarındaki kırıklar ve karşılıklı parça transferi",
            "badge": "Translokasyon",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Resiprokal translokasyon; homolog olmayan iki kromozomda meydana gelen birer kırık sonucu kopan parçaların karşılıklı olarak yer değiştirmesidir.\n\nResiprokal translokasyonun biyolojik ve klinik dinamikleri:\n- **Dengeli Taşıyıcı:** Kırık noktası kritik bir genin gövdesini parçalamadığı sürece birey 46 kromozomludur ve fenotipik olarak tamamen normaldir.\n  - **Mayozda Kuadrivalan (Dörtlü) Yapı:** Mayoz I profazında homolog segmentlerin eşleşebilmesi için iki normal ve iki derivatif kromozom 'artı' (+) şeklinde kuadrivalan oluşturur.\n  - **Segregasyon Modelleri:** 2:2 ayrılmada 'Alternatif' segregasyon normal veya dengeli gamet üretirken; 'Adjacent-1' ve 'Adjacent-2' modelleri parsiyel monozomi ve parsiyel trizomili dengesiz letal gametler doğurur.",
            "coreContent": {
                "table": {
                    "title": "Resiprokal Translokasyonda Mayotik Segregasyon Modelleri",
                    "headers": ["Ayrılma Tipi", "Kromozom Dağılımı", "Gamet Genetiği", "Klinik Sonuç"],
                    "rows": [
                        ["Alternatif Segregasyon", "İki normal veya iki derivatif kutba gider", "Dengeli veya Tam Normal", "Sağlıklı çocuk / Taşıyıcı çocuk"],
                        ["Adjacent-1 Segregasyon", "Homolog olmayan sentromerler birlikte gider", "Dengesiz (Duplikasyon + Delesyon)", "Spontan düşük veya ağır anomalili bebek"],
                        ["Adjacent-2 Segregasyon", "Homolog sentromerler aynı kutba gider (nadir)", "Ağır Dengesiz", "Erken embriyonik letalite / Düşük"],
                        ["3:1 Segregasyon", "Üç kromozom bir kutba, biri diğerine", "Aneuploid Dengesiz (47 veya 45)", "Spontan düşük / Çok ağır malformasyon"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Resiprokal Translokasyon", "explanation": "Homolog olmayan iki ayrı kromozom arasında karşılıklı parça değiş-tokuşu."},
                {"term": "Kuadrivalan", "explanation": "Translokasyon taşıyıcılarında mayoz I evresinde dört kromozomun oluşturduğu artı şeklindeki eşleşme kompleksi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Resiprokal translokasyon taşıyıcısında sağlıklı canlı doğum sağlayabilen YEGANE mayotik segregasyon tipi 'Alternatif Segregasyon'dur."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Mayotik Segregasyon ve Klinik Sonuç Ezber Tablosu",
                    ["Segregasyon Tipi", "Gamet Yapısı", "Klinik Tablo"],
                    [
                        [("Alternatif Segregasyon", False), ("Normal veya Dengeli", True, "Dengeli set"), ("Fenotipik Sağlıklı Birey", False)],
                        [("Adjacent-1 Segregasyon", False), ("Parsiyel Trizomi / Monozomi", True, "Dengesiz"), ("Düşük veya Malformasyon", False)],
                        [("Adjacent-2 Segregasyon", False), ("Ağır Dengesiz Homolog", True, "Homolog birlikte"), ("Erken Embriyonik Kayıp", False)]
                    ]
                ),
                make_micro_quiz(
                    "Resiprokal translokasyon taşıyıcısı bir annenin çocuğunun fenotipik olarak sağlıklı doğabilmesi için mayozda hangi segregasyon modelinin gerçekleşmesi ŞARTTIR?",
                    {
                        "A": "Alternatif segregasyon",
                        "B": "Adjacent-1 segregasyon",
                        "C": "Adjacent-2 segregasyon",
                        "D": "3:1 tersiyer segregasyon"
                    },
                    "A",
                    {
                        "A": "Doğru! Sadece alternatif segregasyonda kutuplara ya her iki normal kromozom ya da her iki derivatif kromozom dengeli olarak gider.",
                        "B": "Yanlış. Adjacent-1 parçalı duplikasyon ve delesyonlu dengesiz gametler üretir.",
                        "C": "Yanlış. Adjacent-2 ağır dengesizlik ve letaliteye yol açar.",
                        "D": "Yanlış. 3:1 segregasyon trizomik/monozomik dengesiz tablolar doğurur."
                    }
                )
            ]
        },
        {
            "slideNumber": 17,
            "title": "Robertsonyan Translokasyon: Akrosentrik Kromozomların Füzyonu",
            "subtitle": "13, 14, 15, 21 ve 22 numaralı kromozomların kısa kollarının kaybı",
            "badge": "Translokasyon",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Robertsonyan translokasyon; yalnızca akrosentrik kromozomlar (13, 14, 15, 21, 22) arasında gerçekleşen özel bir sentrik füzyon tipidir.\n\nRobertsonyan translokasyonun mekanik özellikleri:\n- **Kromozom Sayısı:** İki akrosentrik kromozom sentromerlerinden birleşirken p kollarındaki önemsiz satellitler kaybolur. Dengeli bir taşıyıcının karyotipinde ==45 kromozom== bulunur.\n  - **En Sık Tipler:** En sık rastlanan Robertsonyan translokasyon ==der(13;14)== ve ardından ==der(14;21)=='dir.\n  - **Homolog Robertsonyan Translokasyon:** Eğer translokasyon aynı kromozom çifti arasındaysa (Örn: der(21;21)), taşıyıcının normal çocuk sahibi olma şansı ==YÜZDE SIFIRDIR!== Tüm gametleri ya disomik (Down) ya da nulizomik (letal monozomi) olur.",
            "coreContent": {
                "table": {
                    "title": "Robertsonyan Translokasyon Risk Tablosu",
                    "headers": ["Translokasyon Tipi", "Taşıyıcı Ebeveyn", "Canlı Doğumda Down Sendromu Riski"],
                    "rows": [
                        ["der(14;21)", "Anne Taşıyıcı", "%10 - %15 (Teorik %33 iken ampirik düşüktür)"],
                        ["der(14;21)", "Baba Taşıyıcı", "%1 - %2 (Dengesiz spermler yarışta elenir)"],
                        ["der(21;21) (Homolog)", "Anne veya Baba", "%100 (Normal çocuk şansı KESİNLİKLE YOKTUR!)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Sentrik Füzyon", "explanation": "İki akrosentrik kromozomun sentromerlerinden kırılarak uzun kollarının tek bir büyük kromozom halinde birleşmesi."},
                {"term": "der(21;21) Translokasyonu", "explanation": "İki 21. kromozomun birleşmesi; taşıyıcının tüm canlı çocukları istisnasız Down sendromlu olur."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] der(21;21) taşıyıcısı bir ebeveynin normal çocuk sahibi olma olasılığı %0'dır; canlı doğan tüm bebekler %100 Down sendromlu olur!"
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "der(21q21q) taşıyıcısı olan bir annenin gebe kalması durumunda canlı doğacak bir bebeğin Down sendromlu olma riski yüzde kaçtır?",
                    {
                        "A": "%100",
                        "B": "%50",
                        "C": "%15",
                        "D": "%0"
                    },
                    "A",
                    {
                        "A": "Doğru! Homolog 21;21 translokasyonunda gamet ya iki tane 21 taşır (Down) ya da hiç taşımaz (letal monozomi 21). Canlı doğan bebeklerin %100'ü Down sendromludur.",
                        "B": "Yanlış. Normal gamet oluşma şansı hiç yoktur.",
                        "C": "Yanlış. %10-15 heterolog der(14;21) anne taşıyıcılığı riskidir.",
                        "D": "Yanlış. Risk tam aksine %100'dür."
                    }
                ),
                make_cloze(
                    "Dengeli bir Robertsonyan translokasyon taşıyıcısının vücut hücrelerinde toplam 45 adet kromozom bulunur.",
                    "45",
                    "İki akrosentrik tek bir derivatif kromozom oluşturur"
                )
            ]
        },
        {
            "slideNumber": 18,
            "title": "İnversiyonlar: Parasentrik ve Perisentrik Ayrımı",
            "subtitle": "Sentromerin kırık halkası içindeki konumu ve mayotik krosing-over felaketleri",
            "badge": "İnversiyon",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "İnversiyon; tek bir kromozomda iki ayrı kırık meydana gelmesi ve kırılan parçanın 180° ters dönerek aynı yere yapışmasıdır.\n\nİnversiyonun tipi sentromerin kırık noktalarına göre belirlenir:\n- **Parasentrik İnversiyon:** Kırıkların her ikisi de aynı koldadır; sentromer kırıkların ==DIŞINDADIR==. Kol oranı (p/q) kesinlikle değişmez.\n- **Perisentrik İnversiyon:** Kırıkların biri p kolunda, diğeri q kolundadır; sentromer kırıkların ==İÇİNDEDİR==. Sentromer yer değiştirdiği için p ve q kol oranları belirgin şekilde değişir.\n\n> ⚠️ **Mayoz Felaketi:** Mayozda inversiyon halkası içinde krosing-over gerçekleşirse; parasentrik inversiyonda ==disentrik ve asentrik== letal kromatitler oluşurken; perisentrik inversiyonda duplikasyon/delesyonlu canlı doğabilen anomalili bebekler doğabilir!",
            "coreContent": {
                "table": {
                    "title": "Parasentrik ve Perisentrik İnversiyon Karşılaştırması",
                    "headers": ["Özellik", "Parasentrik İnversiyon", "Perisentrik İnversiyon"],
                    "rows": [
                        ["Sentromer Durumu", "Kırıkların DIŞINDADIR (tek kolda)", "Kırıkların İÇİNDEDİR (iki kolda)"],
                        ["Kol Oranı (p/q)", "Değişmez (morfoloji aynı kalır)", "Değişir (sentromer yer değiştirir)"],
                        ["Krosing-Over Ürünü", "Disentrik ve Asentrik kromatitler", "Duplikasyonlu ve Delesyonlu kromatitler"],
                        ["Klinik Yansıması", "Gametler erken ölür (abortus/infertilite)", "Canlı anomalili/dismorfik bebek doğabilir"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Parasentrik İnversiyon", "explanation": "Sentromeri içermeyen, tek bir kromozom kolunda gerçekleşen 180 derecelik ters dönüş."},
                {"term": "Perisentrik İnversiyon", "explanation": "Sentromeri içine alan, p ve q kollarındaki kırıklarla oluşan inversiyon tipi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Parasentrik inversiyonda krosing-over disentrik ve asentrik kromatitler üretir; bu gametler yaşayamaz (canlı anomalili çocuk riski yok denecek kadar azdır). Perisentrikte ise canlı anomalili çocuk doğabilir!"
            ],
            "interactiveElements": [
                make_before_after(
                    "Parasentrik İnversiyon",
                    "Perisentrik İnversiyon",
                    ["Sentromer kırıkların DIŞINDADIR", "Kol oranı (p/q) DEĞİŞMEZ", "Krosing-over: Disentrik + Asentrik kromatit", "Klinik: Erken düşük / infertilite"],
                    ["Sentromer kırıkların İÇİNDEDİR", "Kol oranı (p/q) DEĞİŞİR", "Krosing-over: Duplikasyon + Delesyon", "Klinik: Canlı anomalili çocuk doğabilir"]
                ),
                make_micro_quiz(
                    "Parasentrik inversiyon taşıyıcısı bir bireyde krosing-over sonucu canlı anomalili çocuk doğma riskinin neredeyse hiç olmamasının temel sebebi nedir?",
                    {
                        "A": "Oluşan rekombinant kromatitlerin disentrik ve asentrik olması sebebiyle embriyoların erken dönemde ölmesi",
                        "B": "Parasentrik inversiyonların mayoz bölünmeyi tamamen durdurması",
                        "C": "Sentromerin kaybolması sonucu hücrenin mitoza girmemesi",
                        "D": "Parasentrik parçaların hiçbir gen içermemesi"
                    },
                    "A",
                    {
                        "A": "Doğru! Disentrik (iki sentromerli) kromatit yırtılır, asentrik kromatit kaybolur; bu gametler canlı doğuma ulaşamaz, gebelik çok erken sonlanır.",
                        "B": "Yanlış. Mayoz ilerler fakat gametler letaldir.",
                        "C": "Yanlış. Sentromer korunur ancak krosing-over rekombinantları letaldir.",
                        "D": "Yanlış. Çok sayıda kritik gen içerir."
                    }
                )
            ]
        },
        {
            "slideNumber": 19,
            "title": "Halka Kromozom (Ring Chromosome): Telomer Kaybı ve Halka Kapanması",
            "subtitle": "Kromozom uçlarının kırılması ve yapışkan uçların dairesel füzyonu",
            "badge": "Yapısal Anomali",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Halka kromozom; bir kromozomun hem p (kısa) hem de q (uzun) kolunun telomerik uçlarında kırık oluşması ve açığa çıkan yapışkan uçların birbirine dairesel olarak kaynamasıyla meydana gelir (Örn: r(46,XX,r(20))).\n\nHalka kromozomların klinik ve mitotik özellikleri:\n- **Terminal Delesyon:** Halka oluşurken her iki kolun en uç bölgeleri kopup kaybolduğu için daima terminal delesyon (gen kaybı) eşlik eder.\n  - **Mitotik Kararsızlık (Instability):** Halka kromozomlar mitoz bölünme sırasında kromatit kilitlenmelerine ve köprüleşmeye uğrar; parçalanıp mozaik hücre hatları üretir.\n  - **Ring Sendromu Fenotipi:** Hangi kromozomdan kaynaklandığına bakılmaksızın tüm halka kromozom taşıyıcılarında ortak bir 'ring sendromu' tablosu (şiddetli boy kısalığı, mikrosefali ve hafif dismorfoloji) izlenir.",
            "medicalTerms": [
                {"term": "Halka Kromozom (Ring Chromosome)", "explanation": "İki kol ucundaki kırıkların dairesel olarak birleşmesiyle oluşan dairesel kromozom yapısı."},
                {"term": "Mitotik Kararsızlık", "explanation": "Dairesel kromozomların replikasyon sonrası anafazda birbirine dolanarak kırılması ve hücrede kararsız kalması."}
            ],
            "spotPearls": [
                "Halka kromozomlarda hem p hem q kol uçlarında delesyon vardır; mitozda kararsız oldukları için hastalarda şiddetli büyüme geriliği tipiktir."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Halka Kromozom Oluşum Kaskadı",
                    [
                        "Kromozomun hem p hem q kolunun telomerik uçlarında çift zincir kırığı oluşur.",
                        "Koruyucu telomer başlıkları kopar ve yapışkan uçlar açığa çıkar.",
                        "DNA tamir mekanizması iki yapışkan ucu dairesel olarak birleştirir (Halka kapanması).",
                        "Mitozda halka kromatitler birbirine dolanarak mitotik instabiliteye ve büyüme geriliğine yol açar."
                    ]
                ),
                make_micro_quiz(
                    "Bir halka kromozomun (ring chromosome) oluşumu esnasında DNA düzeyinde gerçekleşen kaçınılmaz genetik kayıp nedir?",
                    {
                        "A": "Kromozomun hem p hem q kollarının en uç bölgelerinde (subtelomerik) delesyon",
                        "B": "Sentromerin tamamen hücreden atılması",
                        "C": "Kromozomun tüm ekzonlarının silinmesi",
                        "D": "Yalnızca ribozomal RNA genlerinin kaybolması"
                    },
                    "A",
                    {
                        "A": "Doğru! Halka kapanabilmesi için her iki kol ucunda kırık oluşmalı ve telomerik/subtelomerik parçalar silinmelidir.",
                        "B": "Yanlış. Sentromer korunmazsa halka mitozda derhal kaybolur.",
                        "C": "Yanlış. Sadece uç bölgeler kaybolur.",
                        "D": "Yanlış. Yalnızca akrosentriklerde rRNA vardır, halka tüm kromozomlarda oluşabilir."
                    }
                )
            ]
        },
        {
            "slideNumber": 20,
            "title": "İzokromozom: Sentromerin Enine Bölünmesi ve Ayna Hayali Kollar",
            "subtitle": "Bir kolun duplikasyonu, diğer kolun tam monozomisi",
            "badge": "Yapısal Anomali",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "İzokromozom; hücre bölünmesi sırasında sentromerin normalde olması gereken boyuna (longitudinal) eksen yerine hatalı olarak ==enine (transvers)== yarılması sonucu oluşur.\n\nİzokromozomun genetik yapısı kusursuz bir ayna görüntüsüdür:\n- **Gen Dozajı:** Bir kolun tamamen kopyalanması (parsiyel trizomi) ve diğer kolun tamamen silinmesi (tam monozomi) anlamına gelir.\n  - **En Sık Klinik Örnek: i(Xq):** Turner sendromu olgularının yaklaşık %15-18'inde izokromozom Xq [46,X,i(Xq)] görülür. Bu bireylerde iki adet uzun kol (Xq) bulunurken, kısa kol (Xp) hiç yoktur (Xp monozomisi boy kısalığı ve Turner stigması yapar).\n  - **Onkolojik Örnek: i(12p):** Testis germ hücreli tümörlerinde patognomonik olarak izokromozom 12p saptanır (Pallister-Killian sendromunda da mozaik i(12p) görülür).",
            "coreContent": {
                "table": {
                    "title": "Klinikte En Önemli İzokromozom Örnekleri",
                    "headers": ["İzokromozom", "Genetik Durum", "Klinik Tablo / Önemi"],
                    "rows": [
                        ["i(Xq)", "İki adet Xq kolu, sıfır Xp kolu", "Turner sendromu (%15-18) (Kısa boy ve gonadal disgenezi)"],
                        ["i(12p)", "Dört kopya 12p kolu (tetrazomi)", "Testis germ hücreli tümörleri ve Pallister-Killian Sendromu"],
                        ["i(17q)", "İki adet 17q kolu, 17p kaybı (TP53 kaybı)", "Miyeloid lösemilerde ve medulloblastomda kötü prognoz"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "İzokromozom", "explanation": "Sentromerin enlemesine bölünmesiyle oluşan, bir kolu eksik diğer kolu çift olan ayna hayali kromozom."},
                {"term": "i(Xq)", "explanation": "İki uzun kola sahip, kısa kolu bulunmayan ve Turner sendromuna yol açan izokromozom formu."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Turner sendromunda en sık görülen yapısal anomali izokromozom Xq'dur [i(Xq)]; p kolu delesyonu kısa boya neden olur.",
                "📌 [SINAV SPOTU] Testis germ hücreli tümörlerinde patognomonik sitogenetik belirteç izokromozom 12p'dir [i(12p)]."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Turner sendromlu bir hastada en sık saptanan YAPISAL kromozom anomalisi hangisidir?",
                    {
                        "A": "İzokromozom Xq [46,X,i(Xq)]",
                        "B": "Halka kromozom Y [46,X,r(Y)]",
                        "C": "Resiprokal translokasyon t(9;22)",
                        "D": "Parasentrik inversiyon inv(X)"
                    },
                    "A",
                    {
                        "A": "Doğru! Turner sendromunun yapısal varyantları arasında en sık görüleni sentromerin enine bölünmesiyle oluşan izokromozom Xq'dur (%15-18).",
                        "B": "Yanlış. Halka Y virilizasyon riski taşır ancak en sık anomali değildir.",
                        "C": "Yanlış. t(9;22) KML'deki Philadelphia kromozomudur.",
                        "D": "Yanlış. İnversiyonlar Turner'ın birincil yapısal nedeni değildir."
                    }
                ),
                make_cloze(
                    "Hücre bölünmesi esnasında sentromerin boyuna değil enine bölünmesi sonucu oluşan ayna hayali kollara sahip yapısal kromozoma izokromozom adı verilir.",
                    "izokromozom",
                    "Ayna hayali kol yapısı"
                )
            ]
        },
        {
            "slideNumber": 21,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Kromozom Anomalileri ve Mayotik Riskler Sentez Tablosu",
            "subtitle": "Aneuploidi, translokasyon ve inversiyon kurallarının eksiksiz ezber matrisi",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu modül, Bölüm 2 boyunca işlenen sayısal ve yapısal kromozom anomalilerinin mekanizmalarını, ayrılma modellerini ve amfi/TUS sorularında tuzak kurulan noktalarını tek bir hafıza matrisinde birleştirir.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Canlı Doğabilen Tek Tam Monozomi:** ==45,X (Turner)==.\n- **Spontan Abortuslarda En Sık Aneuploidi:** ==Trizomi 16== (ancak canlı doğamaz) ve ==45,X==.\n- **Robertsonyan Translokasyon:** Sadece ==13, 14, 15, 21, 22== arasında olur; dengeli taşıyıcıda ==45 kromozom== vardır.\n- **der(21;21) Homolog Taşıyıcı:** Canlı doğan bebeklerin ==%100'ü Down sendromludur!==\n- **Parasentrik İnversiyon:** Sentromer ==Dışta== -> Disentrik/Asentrik gamet -> Canlı anomalili çocuk riski ==YOK==.\n- **Perisentrik İnversiyon:** Sentromer ==İçte== -> Duplikasyon/Delesyon -> Canlı anomalili çocuk doğabilir!",
            "coreContent": {
                "table": {
                    "title": "Kromozomal Düzensizlikler Büyük Sentez Tablosu",
                    "headers": ["Anomali Tipi", "Sentromer / Bölünme Hilesi", "Gamet Sonucu", "Kritik Klinik Kural"],
                    "rows": [
                        ["Serbest Trizomi 21", "Maternal Mayoz I nondisjunction (%95)", "Disomik gamet (n=24)", "İleri anne yaşıyla riski katlanarak artar"],
                        ["Robertsonyan Translokasyon", "Akrosentrik p kolları kaybolur (45 kr.)", "Taşıyıcı / Dengesiz", "der(21;21) taşıyıcısında sağlıklı çocuk şansı %0'dır"],
                        ["Parasentrik İnversiyon", "Sentromer kırıkların DIŞINDADIR", "Disentrik + Asentrik", "Erken düşük yapar, canlı sakat çocuk riski yoktur"],
                        ["Perisentrik İnversiyon", "Sentromer kırıkların İÇİNDEDİR", "Duplikasyon + Delesyon", "Canlı malformasyonlu çocuk riski taşır"],
                        ["İzokromozom [i(Xq)]", "Sentromer enine bölünür", "Bir kol çifter, diğeri sıfır", "Turner sendromunun en sık yapısal nedenidir"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Disentrik Kromozom", "explanation": "İki sentromer birden taşıyan ve anafazda kutuplar arasında çekilip yırtılan kararsız kromozom."},
                {"term": "Asentrik Kromozom", "explanation": "Hiç sentromer taşımayan, iğ ipliğine bağlanamadığı için hücre bölünmesinde kaybolan kromozom parçası."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] der(21;21) taşıyıcısının canlı çocuklarında Down sendromu riski %100'dür!",
                "📌 [TEKRAR SPOTU] Parasentrik inversiyonda krosing-over disentrik/asentrik kromatit üretir ve letaldir. Perisentrik inversiyonda ise canlı anomalili bebek riski vardır!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Kromozomal Riskler ve Mekanizmalar Sentez Tablosu",
                    ["Patoloji", "Temel Mekanizma", "Kritik Sınav Kuralı"],
                    [
                        [("Turner Sendromu", False), ("45,X Monozomisi", True, "45,X"), ("Canlı doğabilen TEK tam monozomidir", False)],
                        [("Homolog der(21;21)", False), ("Robertsonyan sentrik füzyon", True, "Akrosentrik 21"), ("Canlı çocukta Down riski %100'dür", True, "%100")],
                        [("Parasentrik İnversiyon", False), ("Sentromersiz tek kolda kırık", True, "Dışta"), ("Canlı anomalili bebek riski YOKTUR (Düşük)", True, "Letal")],
                        [("Perisentrik İnversiyon", False), ("Sentromeri içine alan iki kolda kırık", True, "İçte"), ("Canlı anomalili çocuk doğabilir", True, "Canlı risk")],
                        [("İzokromozom Xq", False), ("Sentromerin enine yarılması", True, "Enine"), ("Turner'da en sık yapısal anomalidir", True, "i(Xq)")]
                    ]
                ),
                make_micro_quiz(
                    "Evlilik öncesi genetik taramada babanın 45,XY,der(14;21) taşıyıcısı olduğu saptanmıştır. Bu çiftin canlı doğacak çocuklarında Down sendromu görülme ampirik riski yaklaşık yüzde kaçtır?",
                    {
                        "A": "%1 - %2",
                        "B": "%10 - %15",
                        "C": "%33",
                        "D": "%100"
                    },
                    "A",
                    {
                        "A": "Doğru! Baba der(14;21) taşıyıcısı olduğunda dengesiz spermler fertilizasyon yarışında elendiği için canlı doğumda Down riski sadece %1-2'dir (Anne taşıyıcı olsaydı risk %10-15 olurdu).",
                        "B": "Yanlış. %10-15 oranı anne taşıyıcı olduğundaki ampirik risktir.",
                        "C": "Yanlış. %33 teorik segregasyon oranıdır ancak pratikte gözlenmez.",
                        "D": "Yanlış. %100 riski sadece der(21;21) homolog taşıyıcılarda geçerlidir."
                    }
                ),
                make_micro_quiz(
                    "Mayoz bölünme sırasında gerçekleşen krosing-over sonucunda bir kromatitin İKİ ADET sentromer birden kazanması (disentrik) hangi inversiyon tipinin tipik sonucudur?",
                    {
                        "A": "Parasentrik inversiyon",
                        "B": "Perisentrik inversiyon",
                        "C": "Robertsonyan translokasyon",
                        "D": "Halka kromozom füzyonu"
                    },
                    "A",
                    {
                        "A": "Doğru! Parasentrik inversiyonda krosing-over bir adet disentrik (iki sentromerli) ve bir adet asentrik (sentromersiz) kromatit üretir.",
                        "B": "Yanlış. Perisentrik inversiyonda kromatitlerin her biri tek sentromerlidir ancak delesyon ve duplikasyon içerirler.",
                        "C": "Yanlış. Robertsonyan bir translokasyondur.",
                        "D": "Yanlış. Halka kromozom uç birleşmesidir."
                    }
                )
            ]
        }
    ]
