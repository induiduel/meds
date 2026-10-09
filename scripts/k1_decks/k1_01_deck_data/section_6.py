#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 6: Primer Tek Defektler: Malformasyon, Deformasyon, Disrupsiyon, Displazi (Adım 41 - 49 + Tekrar Sayfası)
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
            "slideNumber": 41,
            "title": "Primer Tek Defektlerin 4 Temel Mekanizması: Malformasyon, Deformasyon, Disrupsiyon, Displazi",
            "subtitle": "Embriyolojik doku hasarının doğası ve patogenetik sınıflama",
            "badge": "Patogenetik Sınıflama",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Klinik dismorfolojide tek bir anatomik yapıda görülen izole kusurlar patogenetik kökenlerine göre 4 ana mekanizmaya ayrılır:\n\n- **1. Malformasyon:** Dokunun gelişimi en başından itibaren ==intrinsik (içsel)== olarak anormaldir; genetik programlama hatalıdır (Örn: Yarık dudak, VSD).\n- **2. Deformasyon:** Doku embriyolojik olarak tamamen normal başlamış ve gelişmiştir; ancak intrauterin ==mekanik dış bası== nedeniyle şekli bozulmuştur (Örn: Pes ekinovarus / çomak ayak).\n- **3. Disrupsiyon:** Normal gelişen bir dokunun dışarıdan gelen ==yıkıcı bir faktörle== (amniyotik bant, iskemi, enfeksiyon) parçalanması veya kopmasıdır (Örn: Amniyotik bant amputasyonu).\n- **4. Displazi:** Belirli bir doku tipini oluşturan hücrelerin hücresel mimarisinin ve matriks organizasyonunun anormal olmasıdır (Örn: Akondroplazi / iskelet displazisi).",
            "coreContent": {
                "table": {
                    "title": "4 Primer Defekt Tipinin Karşılaştırma Matrisi",
                    "headers": ["Defekt Tipi", "Başlangıçtaki Doku", "Hasarın Nedeni", "Kalıtım / Rekürrens Riski"],
                    "rows": [
                        ["Malformasyon", "İntrinsik anormal (en baştan hatalı)", "Genetik mutasyon, kromozomal hata", "Yüksek (%3 - %5 multifaktöriyel / Mendeliyen)"],
                        ["Deformasyon", "Tamamen normal", "Mekanik dış bası (oligohidramniyos vb.)", "Çok düşük (< %1 mekanik faktör kalkarsa)"],
                        ["Disrupsiyon", "Tamamen normal", "Dış yıkıcı olay (amniyotik bant, iskemi)", "Yok denecek kadar az (Rastlantısaldır)"],
                        ["Displazi", "Doku düzeyinde anormal", "Spesifik tek gen mutasyonları (enzim/reseptör)", "Mendeliyen kalıtım kurallarına uyar"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "İntrinsik Hasar", "explanation": "Doku taslağının genetik veya hücresel programındaki içsel başlangıç hatası (Malformasyon)."},
                {"term": "Ekstrinsik Hasar", "explanation": "Normal gelişen dokuya dışarıdan uygulanan mekanik veya yıkıcı faktörün etkisi (Deformasyon / Disrupsiyon)."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Malformasyonda doku en başından intrinsik olarak anormaldir; Deformasyon ve Disrupsiyonda ise doku başlangıçta tamamen normaldir!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "4 Temel Patogenetik Defekt Ezber Tablosu",
                    ["Defekt Türü", "Başlangıç Dokusu", "Hasar Mekanizması"],
                    [
                        [("Malformasyon", False), ("İntrinsik Anormal", True, "İçsel hatalı"), ("Genetik programlama defekti", False)],
                        [("Deformasyon", False), ("Tamamen Normal", True, "Normal doku"), ("Mekanik dış bası (Oligohidramniyos)", False)],
                        [("Disrupsiyon", False), ("Tamamen Normal", True, "Normal doku"), ("Yıkıcı olay / Vasküler kopma (Bant)", False)],
                        [("Displazi", False), ("Doku Mimarisi Bozuk", True, "Hücre organizasyonu"), ("Spesifik tek gen defekti (FGFR3 vb.)", False)]
                    ]
                ),
                make_micro_quiz(
                    "Doğumsal bir anomalinin 'MALFORMASYON' olarak kabul edilebilmesi için doku gelişiminin başlangıç durumu nasıl olmalıdır?",
                    {
                        "A": "Doku oluşumunun en başından itibaren intrinsik (içsel) olarak anormal programlanmış olması",
                        "B": "Tamamen normal gelişen dokunun amniyotik bantla sonradan kopması",
                        "C": "Normal dokunun oligohidramniyos nedeniyle mekanik olarak bükülmesi",
                        "D": "Yalnızca kemik iliğinde histolojik hücre dizilim bozukluğu bulunması"
                    },
                    "A",
                    {
                        "A": "Doğru! Malformasyonun ayırt edici özelliği dokunun en baştan itibaren intrinsik olarak anormal olmasıdır.",
                        "B": "Yanlış. Amniyotik bantla kopma Disrupsiyondur.",
                        "C": "Yanlış. Mekanik bükülme Deformasyondur.",
                        "D": "Yanlış. Hücresel organizasyon bozukluğu Displazidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 42,
            "title": "Malformasyon: İntrinsik Morfogenez Hataları ve Rekürrens Riski",
            "subtitle": "Kromozom anomalileri, tek gen mutasyonları ve organ taslağı defektleri",
            "badge": "Malformasyon",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Malformasyon; bir organın veya vücut parçasının oluşumundaki içsel (intrinsik) bir gelişim hatası sonucu tam olarak meydana gelememesi veya hatalı biçimlenmesidir.\n\nMalformasyonun klinik özellikleri:\n- **Oluşum Zamanı:** Neredeyse istisnasız olarak ilk 8 haftadaki ==organogenez evresinde== şekillenir.\n- **Kalıtım ve Aile Riski:** Malformasyonlar güçlü bir genetik altyapıya sahiptir (Mendeliyen tek gen mutasyonları, kromozom anomalileri veya multifaktöriyel eşik kalıtımı). Bu nedenle sonraki gebeliklerde tekrarlama (rekürrens) riski yüksektir (multifaktöriyelde yaklaşık ==%3 - %5==).\n- **Klasik Örnekler:** Konjenital kalp defektleri (VSD, ASD, Fallot), Dudak-Damak Yarığı, Nöral Tüp Defektleri (Anansefali, Spina Bifida), Renal Agenezi.",
            "medicalTerms": [
                {"term": "Malformasyon", "explanation": "İntrinsik anormal doku gelişimi sonucu organın eksik veya hatalı şekillenmesi."},
                {"term": "Multifaktöriyel Eşik Kalıtımı", "explanation": "Birden çok genin çevresel faktörlerle etkileşerek bir yatkınlık eşiğini aşması sonucu ortaya çıkan anomali modeli."}
            ],
            "spotPearls": [
                "Malformasyonlar intrinsik kökenli oldukları için diğer defekt tiplerine kıyasla en yüksek tekrarlama (rekürrens) riskine sahiptir (%3-5)."
            ],
            "interactiveElements": [
                make_before_after(
                    "Malformasyon (İntrinsik)",
                    "Deformasyon (Ekstrinsik)",
                    ["Doku en başından anormaldir", "Organogenezde (4-8. hafta) oluşur", "Genetik altyapısı güçlüdür", "Rekürrens riski %3-5 veya daha yüksektir"],
                    ["Doku başlangıçta tamamen normaldir", "Fetogenezde (9. hafta sonrası) oluşur", "Mekanik ortam kaynaklıdır", "Rekürrens riski son derece düşüktür (<%1)"]
                ),
                make_micro_quiz(
                    "Aşağıdaki konjenital defektlerden hangisi tipik bir 'MALFORMASYON' örneğidir?",
                    {
                        "A": "Ventriküler Septal Defekt (VSD)",
                        "B": "Oligohidramniyosa bağlı pes ekinovarus (çomak ayak)",
                        "C": "Amniyotik bant amputasyonu sonucu parmak kopması",
                        "D": "Uterin miyoma bağlı kafa asimetrisi"
                    },
                    "A",
                    {
                        "A": "Doğru! VSD kardiyak septanın intrinsik kapanma hatasıdır (malformasyon).",
                        "B": "Yanlış. Oligohidramniyos basısı Deformasyondur.",
                        "C": "Yanlış. Amniyotik bant Disrupsiyondur.",
                        "D": "Yanlış. Miyom mekanik basısı Deformasyondur."
                    }
                )
            ]
        },
        {
            "slideNumber": 43,
            "title": "Deformasyon: Mekanik Dış Bası ve Geri Döndürülebilirlik",
            "subtitle": "Oligohidramniyos, uterus anomalileri, çoğul gebelik ve fetal sıkışma",
            "badge": "Deformasyon",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Deformasyon; embriyolojik olarak tamamen normal gelişmiş olan bir vücut parçasının intrauterin mekanik bası ve fiziksel kısıtlanma kuvvetleri nedeniyle biçim veya pozisyon bozukluğuna uğramasıdır.\n\nDeformasyonun belirleyici klinik özellikleri:\n- **Zamanlama:** İkinci ve üçüncü trimesterde (fetogenez periyodu), fetüs büyüdükçe ve intrauterin alan daraldıkça ortaya çıkar.\n- **Etiyolojik Faktörler:** Oligohidramniyos (amniyon sıvısının azalması en sık nedendir), uterus bikornis/septat uterus, büyük uterin miyomlar, çoğul gebelik (ikiz/üçüz sıkışması), makrozomi.\n- **Geri Döndürülebilirlik (Reversibility):** Deformasyonlar intrinsik bir doku defekti içermediği için doğum sonrasında mekanik baskı kalktığında fizik tedavi, masaj veya alçılama ile ==tamamen düzelebilir!==\n- **Rekürrens:** Mekanik neden ortadan kaldırılırsa sonraki gebelikte tekrarlama riski yok denecek kadar azdır (<%1).",
            "coreContent": {
                "table": {
                    "title": "Deformasyon Etiyolojisi ve Tedavi Yaklaşımı",
                    "headers": ["Deformasyon Örneği", "Temel Mekanik Neden", "Tedavi / Prognoz"],
                    "rows": [
                        ["Pes Ekinovarus (Pozisyonel)", "Oligohidramniyos, fetal ayak sıkışması", "Ponseti yöntemi (alçılama/fizik tedavi) ile tam düzelme"],
                        ["Pozisyonel Plagiosefali", "Uterus içi kafa basısı, sırtüstü yatış", "Pozisyon değiştirme, kask tedavisi ile spontan düzelme"],
                        ["Konjenital Kalça Çıkığı (Gelişimsel)", "Makat geliş (breech), oligohidramniyos", "Pavlik bandajı ve takip ile tam anatomik iyileşme"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Deformasyon", "explanation": "Normal gelişen dokunun mekanik dış baskılar nedeniyle şekil ve pozisyon değiştirmesi."},
                {"term": "Pes Ekinovarus", "explanation": "Ayağın içe ve aşağıya doğru bükülü durması ile karakterize, sıklıkla deformasyonel ayak anomalisi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Deformasyonlar doğum sonrası fizik tedavi veya pozisyonlama ile spontan düzelebilir; rekürrens riskleri <%1 ile son derece düşüktür."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Oligohidramniyos ve Deformasyon Kaskadı",
                    [
                        "Maternal veya fetal nedenle amniyon sıvısı ileri derecede azalır (Oligohidramniyos).",
                        "Uterus duvarı fetüsün üzerine doğrudan yaslanır ve koruyucu sıvı yastığı kaybolur.",
                        "Ekstremiteler uterus duvarına sıkışarak mekanik bükülmeye zorlanır.",
                        "Doğumda pes ekinovarus (çomak ayak) ve basık yüz gibi tipik deformasyonlar görülür."
                    ]
                ),
                make_micro_quiz(
                    "Makat geliş ve oligohidramniyos öyküsü olan bir yenidoğanda saptanan pes ekinovarus (çomak ayak) tablosunun patogenetik sınıflaması ve prognozu hangisidir?",
                    {
                        "A": "Deformasyon — Mekanik baskı kalktığı için fizik tedavi ve alçılama ile düzelme şansı çok yüksektir",
                        "B": "Malformasyon — Genetik mutasyon nedeniyle cerrahi yapılsa dahi asla düzelmez",
                        "C": "Disrupsiyon — Damar koptuğu için bacağın kesilmesi gerekir",
                        "D": "Displazi — Ömür boyu ilerleyici kemik yıkımıyla seyreder"
                    },
                    "A",
                    {
                        "A": "Doğru! Mekanik basıya bağlı şekil bozuklukları deformasyondur; doku sağlam olduğu için konservatif tedaviye mükemmel yanıt verir.",
                        "B": "Yanlış. Malformasyon intrinsik hasardır, burada doku normaldir.",
                        "C": "Yanlış. Damar kopması yoktur.",
                        "D": "Yanlış. Displazi hücresel mimari bozukluğudur."
                    }
                )
            ]
        },
        {
            "slideNumber": 44,
            "title": "Disrupsiyon: Normal Dokunun Ekstrinsik Faktörlerle Yıkımı ve Parçalanması",
            "subtitle": "Amniyotik bant sekansı, vasküler oklüzyon ve iskemi nekrozu",
            "badge": "Disrupsiyon",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Disrupsiyon; embriyolojik gelişimi tamamen normal ilerleyen bir organ veya vücut bölgesinin, sonradan dışarıdan gelen ==yıkıcı bir ekstrinsik olayla== tahrip olması, parçalanması veya amputasyona uğramasıdır.\n\nDisrupsiyonun patofizyolojik özellikleri:\n- **Geri Dönüşsüz Kayıp:** Doku nekroze olur veya fiziksel olarak kopar; bu nedenle deformasyon gibi asla spontan düzelemez, kalıcı kayıp bırakır.\n- **Kalıtımsal Değildir:** Genetik bir mutasyondan kaynaklanmaz; tamamen intrauterin rastlantısal bir kaza sonucudur. Bu nedenle ailede sonraki gebeliklerde tekrarlama riski ==YOK DENECEK KADAR AZDIR (Sıfıra yakındır)==.\n- **Amniyotik Bant Sendromu:** Amniyon zarının yırtılarak fetal ekstremiteleri iplik gibi sarması ve dolaşımı boğarak parmak veya kol amputasyonu yapması en klasik disrupsiyon örneğidir.\n- **Vasküler Oklüzyon (Barsak Atrezileri):** Mezenter arterin trombozu sonucu gelişen jejunum atrezisi de vasküler bir disrupsiyondur.",
            "coreContent": {
                "table": {
                    "title": "Disrupsiyon Nedenleri ve Klinik Görünümleri",
                    "headers": ["Yıkıcı Neden", "Oluşan Disrupsiyon", "Klinik Özellik"],
                    "rows": [
                        ["Amniyotik Bantlar", "Dijital amputasyon, konstriksiyon halkaları", "Parmakların uç kısımlarının boğularak kopması"],
                        ["Vasküler Oklüzyon / Emboli", "Jejunoileal atrezi, gövde duvarı defektleri", "Normal gelişen barsak segmentinin iskemik nekrozu"],
                        ["Teratojenik İskemi (Kokain)", "Ekstremite terminal transvers defektleri", "Şiddetli vazokonstriksiyon sonucu doku kangreni"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Disrupsiyon", "explanation": "Normal gelişen bir organ veya dokunun dışsal yıkıcı bir olayla tahrip olması veya kopması."},
                {"term": "Amniyotik Bant Sendromu", "explanation": "Amniyon zar iplikçiklerinin fetal uzuvları boğarak halkasal konstriksiyon ve amputasyon yapması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Amniyotik bant sendromuna bağlı parmak amputasyonları disrupsiyon örneğidir; genetik değildir ve sonraki gebelikte rekürrens riski sıfıra yakındır!"
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Amniyotik Bant Disrupsiyon Kaskadı",
                    [
                        "Erken gebelikte amniyon zarı parsiyel olarak yırtılır.",
                        "Açığa çıkan mezodermal fibröz bantlar serbest amniyon sıvısında yüzer.",
                        "Bantlar fetal el ve ayak parmaklarının etrafına dolanarak sıkı bir halka oluşturur.",
                        "Distal kan akımı kesilir; doku nekroze olarak ampüte olur (konjenital amputasyon)."
                    ]
                ),
                make_micro_quiz(
                    "Doğumda sağ el 2. ve 3. parmaklarında amputasyon ve proksimalinde konstriksiyon halkası saptanan bir bebeğin ailesine verilecek en doğru genetik danışma hangisidir?",
                    {
                        "A": "Bu bir amniyotik bant disrupsiyonudur; sonraki gebelikte tekrarlama riski yok denecek kadar azdır (sıfıra yakındır)",
                        "B": "Bu otozomal dominant bir malformasyondur; sonraki çocukta risk %50'dir",
                        "C": "Bu pozisyonel bir deformasyondur; masajla parmaklar yeniden uzar",
                        "D": "Kromozomal translokasyon test edilmeden risk söylenemez"
                    },
                    "A",
                    {
                        "A": "Doğru! Amniyotik bant sendromu klasik bir disrupsiyondur; genetik değildir, rastlantısaldır ve rekürrens riski yoktur.",
                        "B": "Yanlış. Kalıtsal bir malformasyon değildir.",
                        "C": "Yanlış. Kopan doku masajla geri gelmez.",
                        "D": "Yanlış. Tipik bant konstriksiyonunda kromozomal etiyoloji aranmaz."
                    }
                )
            ]
        },
        {
            "slideNumber": 45,
            "title": "Displazi: Hücrelerin Doku İçinde Anormal Organizasyonu ve Histogenez Hataları",
            "subtitle": "Kıkırdak, kemik ve bağ dokusunun yapısal mimarisinin bozulması",
            "badge": "Displazi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Displazi; belirli bir doku tipini (özellikle kemik, kıkırdak, deri veya kan damarlarını) oluşturan hücrelerin embriyolojik gelişim boyunca doku içindeki organizasyonunun ve histogenezinin bozulmasıdır.\n\nDisplazinin ayırt edici dinamikleri:\n- **Dokuya Özgüllük:** Malformasyon tek bir organı (örneğin sadece kalbi) etkilerken; displazi o dokunun vücutta bulunduğu ==HER YERİ== etkiler (iskelet displazisinde tüm kemikler etkilenir).\n- **İlerleyici (Progresif) Karakter:** Doku büyümesi yaşam boyu sürdüğü için, displazik bozukluklar yaşla birlikte durmaz, fenotip zamanla daha da kötüleşir.\n- **Genetik Temel:** Displaziler hemen daima tek gen mutasyonlarına (yapısal proteinler veya sinyal reseptörleri) bağlıdır ve Mendeliyen kalıtım kurallarına (otozomal dominant/resesif) kesinlikle uyar.\n- **Klasik Örnekler:** Akondroplazi (FGFR3 mutasyonu ile endokondral kemikleşme kusuru), Osteogenezis İmperfekta (Tip 1 kollajen kusuru ile kırılgan kemikler), Marfan Sendromu (Fibrillin-1 kusuru).",
            "coreContent": {
                "table": {
                    "title": "Başlıca Displazi Tipleri ve Genetik Kusurları",
                    "headers": ["Displazi Tablosu", "Etkilenen Doku", "Genetik Mutasyon", "Klinik Özellik"],
                    "rows": [
                        ["Akondroplazi", "Kıkırdak / Endokondral kemikleşme", "FGFR3 geni fonksiyon kazanımı (Gain of function)", "Rizomelik boy kısalığı, makrosefali, çökük burun"],
                        ["Osteogenezis İmperfekta", "Kemik matriksi / Bağ dokusu", "COL1A1 / COL1A2 gen kusurları", "Kırılgan kemikler, mavi sklera, diş anomalisi"],
                        ["Ektodermal Displazi", "Deri, saç, diş, ter bezleri", "EDA / EDAR gen mutasyonları", "Hipohidrozis (terleyememe), konik dişler, saçsızlık"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Displazi", "explanation": "Hücrelerin doku içinde anormal organizasyonu veya histolojik işlev bozukluğu."},
                {"term": "Akondroplazi", "explanation": "FGFR3 mutasyonuna bağlı endokondral kemikleşme yetersizliği ile seyreden en sık orantısız boy kısalığı."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Displazi tek bir organı değil, vücutta o doku tipinin bulunduğu tüm anatomik bölgeleri etkiler ve yaşam boyu ilerleyicidir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Malformasyon (Organ Defekti)",
                    "Displazi (Doku Defekti)",
                    ["Spesifik tek bir organı etkiler (Örn: Kalp, Damak)", "Lezyon lokalizedir", "Zamanla yayılmaz, statiktir"],
                    ["Vücuttaki o dokunun tamamını etkiler (Örn: Tüm kemikler)", "Lezyon generalize ve sistemiktir", "Hücre büyümesi sürdükçe progresiftir"]
                ),
                make_micro_quiz(
                    "Vücuttaki tüm kıkırdak ve kemik dokusunu yaygın olarak etkileyen, FGFR3 gen mutasyonu sonucu oluşan 'Akondroplazi' tablosu patogenetik olarak hangi primer defekt sınıfına girer?",
                    {
                        "A": "Displazi",
                        "B": "Deformasyon",
                        "C": "Disrupsiyon",
                        "D": "İzole Malformasyon"
                    },
                    "A",
                    {
                        "A": "Doğru! Belirli bir doku tipinin (kemik/kıkırdak) tüm vücutta anormal organizasyonu displazidir.",
                        "B": "Yanlış. Deformasyon mekanik dış basıdır.",
                        "C": "Yanlış. Disrupsiyon doku kopmasıdır.",
                        "D": "Yanlış. Malformasyon izole organ kusurudur, akondroplazi tüm iskeleti tutan dokusal displazidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 46,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] 4 Primer Defekt Tipinin Karşılaştırma Matrisi",
            "subtitle": "Malformasyon, Deformasyon, Disrupsiyon ve Displazi ezber tablosu",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu modül, sınavların en yüksek verimli konusu olan 4 primer gelişimsel defekt mekanizmasını tek bir sentez matrisinde birleştirmektedir.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Malformasyon:** Doku en baştan ==İntrinsik Anormaldir==. Rekürrens riski ==Yüksektir (%3-5)==. Örnek: VSD, Dudak-damak yarığı.\n- **Deformasyon:** Doku başlangıçta ==Tamamen Normaldir==. Mekanik dış bası (oligohidramniyos) şekil bozar. Konservatif tedaviyle ==Düzelir==. Rekürrens ==<%1==. Örnek: Pes ekinovarus.\n- **Disrupsiyon:** Doku başlangıçta ==Tamamen Normaldir==. Dış yıkıcı olay (amniyotik bant) dokuyu parçalar. Rekürrens ==Yoktur (0)==. Örnek: Parmak amputasyonu.\n- **Displazi:** Hücrelerin doku içindeki ==Organizasyon Hatasıdır==. Tüm dokuyu tutar, yaşam boyu ==İlerleyicidir==. Örnek: Akondroplazi.",
            "coreContent": {
                "table": {
                    "title": "4 Primer Defektin Eksiksiz Karşılaştırma Matrisi",
                    "headers": ["Parametre", "Malformasyon", "Deformasyon", "Disrupsiyon", "Displazi"],
                    "rows": [
                        ["Başlangıç Dokusu", "İntrinsik Anormal", "Tamamen Normal", "Tamamen Normal", "Hücresel Anormal"],
                        ["Temel Neden", "Genetik mutasyon / Teratojen", "Mekanik dış bası", "Amniyotik bant / İskemi", "Spesifik gen defekti"],
                        ["Prognoz / Düzelme", "Cerrahi onarım şarttır", "Fizik tedaviyle tam düzelir", "Kalıcı doku kaybı kalır", "Yaşla ilerleyicidir"],
                        ["Rekürrens Riski", "%3 - %5 (veya Mendeliyen)", "< %1 (Çok düşük)", "Sıfıra yakın (Yok)", "Mendeliyen kurallara uyar"],
                        ["Klasik Örnek", "VSD, Anansefali", "Pozisyonel pes ekinovarus", "Amniyotik bant amputasyonu", "Akondroplazi, OI"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Primer Tek Defekt", "explanation": "Embriyoda tek bir lokalize anatomik bölgede veya dokuda başlayan birincil anomali."},
                {"term": "Amniyotik Bant", "explanation": "Fetal uzuvları çevreleyerek disrupsiyona yol açan fibröz zar kalıntısı."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] Malformasyon: İntrinsik (Risk yüksek) | Deformasyon: Mekanik bası (Düzelir, risk yok) | Disrupsiyon: Yıkıcı kopma (Kalıtsal değil) | Displazi: Doku mimari bozukluğu (İlerleyici).",
                "📌 [TEKRAR SPOTU] Amniyotik bant = Disrupsiyon | Oligohidramniyosa bağlı çomak ayak = Deformasyon | Fallot tetralojisi = Malformasyon | Akondroplazi = Displazi."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "4 Primer Defekt Tipi Büyük Sentez Tablosu",
                    ["Defekt Sınıfı", "Doku Başlangıcı", "Mekanizma", "Rekürrens Riski"],
                    [
                        [("Malformasyon", False), ("İntrinsik Hatalı", True, "En baştan"), ("Morfogenez bozukluğu", False), ("Yüksek (%3-5)", True, "%3-5")],
                        [("Deformasyon", False), ("Tamamen Normal", True, "Normal"), ("Mekanik dış bası", False), ("Çok Düşük (<%1)", True, "<%1")],
                        [("Disrupsiyon", False), ("Tamamen Normal", True, "Normal"), ("Dış yıkıcı olay / Bant", False), ("Yok denecek kadar az", True, "Sıfır")],
                        [("Displazi", False), ("Doku Düzeyinde Hata", True, "Histolojik"), ("Hücre organizasyon kusuru", False), ("Mendeliyen kurallar", True, "Genetik")]
                    ]
                ),
                make_micro_quiz(
                    "Oligohidramniyosa bağlı olarak ayaklarında pes ekinovarus (çomak ayak) gelişen bir bebeğin tablosu ile amniyotik bant nedeniyle ayak parmakları kopan bir bebeğin tablosunun patogenetik sınıflaması sırasıyla hangisidir?",
                    {
                        "A": "Deformasyon — Disrupsiyon",
                        "B": "Malformasyon — Deformasyon",
                        "C": "Displazi — Malformasyon",
                        "D": "Disrupsiyon — Deformasyon"
                    },
                    "A",
                    {
                        "A": "Doğru! Mekanik sıvı azlığı basısı Deformasyondur; amniyotik bantla parmağın kopması Disrupsiyondur.",
                        "B": "Yanlış. Sıvı azlığı malformasyon değildir.",
                        "C": "Yanlış. Displazi hücresel doku hastalığıdır.",
                        "D": "Yanlış. Sıralama terstir."
                    }
                ),
                make_micro_quiz(
                    "Aşağıdaki defekt tiplerinden hangisi ailesel tekrarlama (rekürrens) riski açısından DİĞERLERİNE GÖRE EN DÜŞÜK (sıfıra yakın) risk profiline sahiptir?",
                    {
                        "A": "Amniyotik bant amputasyon disrupsiyonu",
                        "B": "İzole multifaktöriyel dudak-damak yarığı malformasyonu",
                        "C": "Otozomal dominant akondroplazi displazisi",
                        "D": "Ventriküler septal defekt (VSD) malformasyonu"
                    },
                    "A",
                    {
                        "A": "Doğru! Amniyotik bant sendromu tamamen rastlantısal bir dış olaydır; genetik değildir ve sonraki gebelikte tekrarlamaz.",
                        "B": "Yanlış. Dudak-damak yarığında rekürrens riski %3-5'tir.",
                        "C": "Yanlış. Akondroplazide ebeveyn hastaysa risk %50'dir.",
                        "D": "Yanlış. VSD'de multifaktöriyel rekürrens riski vardır."
                    }
                )
            ]
        }
    ]
