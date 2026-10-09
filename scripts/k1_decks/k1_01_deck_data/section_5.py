#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 5: İntrauterin Gelişim Periyotları & Anomalileri (Adım 35 - 41 + Tekrar Sayfası)
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
            "slideNumber": 35,
            "title": "İntrauterin Gelişim Periyotlarının Genel Çerçevesi: Blastogenez, Embriyogenez, Fetogenez",
            "subtitle": "Zaman çizelgesi ve gelişimsel duyarlılık pencereleri",
            "badge": "Gelişim Dönemleri",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Fetal gelişim, fertilizasyondan doğuma kadar geçen yaklaşık 38-40 haftalık süreçte üç belirgin biyolojik evreye ayrılır: ==Blastogenez==, ==Embriyogenez== ve ==Fetogenez==.\n\nBu üç dönemin klinik ve morfolojik sınırları:\n- **1. Blastogenez (0 - 4. Hafta):** Fertilizasyon, segmentasyon, blastosist oluşumu, implantasyon ve gastrulasyon (üç germ yaprağının oluşumu) basamaklarını kapsar.\n- **2. Embriyogenez (4 - 8. Hafta):** Organ taslaklarının oluştuğu birincil ==organogenez== evresidir. Hücre göçü ve farklılaşması maksimal hızdadır; teratojenik etkilere en savunmasız dönemdir.\n- **3. Fetogenez (9. Hafta - Doğum):** Oluşmuş organların büyümesi, histolojik olgunlaşması (histogenez) ve fonksiyon kazanması evresidir.",
            "coreContent": {
                "table": {
                    "title": "İntrauterin Gelişim Dönemleri ve Klinik Özellikleri",
                    "headers": ["Dönem", "Zaman Aralığı", "Temel Biyolojik Olay", "Teratojenik Yanıt"],
                    "rows": [
                        ["Blastogenez", "0 - 4. Hafta (İlk 28 gün)", "Segmentasyon, gastrulasyon, germ yaprakları", "'Ya Hep Ya Hiç' kuralı (Düşük veya Tam İyileşme)"],
                        ["Embriyogenez", "4 - 8. Hafta", "Primer organogenez (kalp, uzuv, SSS oluşumu)", "AĞIR MAJÖR MALFORMASYONLAR (Maksimum duyarlılık)"],
                        ["Fetogenez", "9. Hafta - Doğum", "Büyüme, histogenez, fonksiyonel matürasyon", "Deformasyonlar, disrupsiyonlar, fonksiyonel gerilik"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Blastogenez", "explanation": "Fertilizasyondan gastrulasyonun tamamlanmasına kadar geçen ilk 4 haftalık erken embriyonik evre."},
                {"term": "Organogenez", "explanation": "Embriyonik 4-8. haftalarda organ taslaklarının birincil olarak farklılaşıp biçimlenmesi süreci."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Teratojenlere karşı majör malformasyon riskinin en yüksek olduğu kritik zaman penceresi embriyogenez (4 - 8. haftalar) periyodudur."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Gelişim Periyotları ve Teratojenik Risk Ezber Tablosu",
                    ["Gelişim Periyodu", "Zaman Aralığı", "Tipik Hasar Sonucu"],
                    [
                        [("Blastogenez", False), ("0 - 4. Hafta", True, "İlk 4 hafta"), ("Ya Hep Ya Hiç (Düşük veya İyileşme)", False)],
                        [("Embriyogenez", False), ("4 - 8. Hafta", True, "4-8. hafta"), ("AĞIR MAJÖR MALFORMASYON (En hassas)", True, "Maksimum risk")],
                        [("Fetogenez", False), ("9. Hafta - Doğum", True, "9. hafta sonrası"), ("Deformasyon & Fonksiyonel Kusurlar", False)]
                    ]
                ),
                make_micro_quiz(
                    "İntrauterin gelişim sürecinde teratojenik bir ajana maruziyet durumunda AĞIR MAJÖR ORGAN MALFORMASYONLARININ oluşma riskinin en yüksek olduğu dönem hangisidir?",
                    {
                        "A": "Embriyogenez dönemi (4 - 8. haftalar)",
                        "B": "Blastogenez dönemi (0 - 4. haftalar)",
                        "C": "Geç fetogenez dönemi (32 - 38. haftalar)",
                        "D": "Doğum anı ve neonatal ilk gün"
                    },
                    "A",
                    {
                        "A": "Doğru! 4-8. haftalar organ taslaklarının oluştuğu primer organogenez evresidir; bu evredeki hasarlar geri dönüşsüz majör malformasyonlara yol açar.",
                        "B": "Yanlış. Blastogenezde 'ya hep ya hiç' kuralı işler (ya embriyo ölür ya da tam iyileşir).",
                        "C": "Yanlış. Fetogenezde organlar zaten oluşmuştur, büyüme ve fonksiyonel matürasyon etkilenir.",
                        "D": "Yanlış. Doğum sonrası konjenital organogenez gerçekleşmez."
                    }
                )
            ]
        },
        {
            "slideNumber": 36,
            "title": "Blastogenez Periyodu (0-4. Hafta): Hücresel Totipotensi ve 'Ya Hep Ya Hiç' Kuralı",
            "subtitle": "Kök hücrelerin esnekliği, spontan düşükler ve tam kompanzasyon",
            "badge": "Mekanizma",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Blastogenez evresinde hücreler henüz nihai organ kaderlerine kesin olarak kilitlenmemiştir; yüksek düzeyde totipotensi ve plastisite sergilerler.\n\nBu biyolojik özelliğin yarattığı klinik fenomen: ==Ya Hep Ya Hiç (All-or-None) Prensibi==:\n- **Ağır Hasar (Hiç):** Eğer çevresel toksin, radyasyon veya kimyasal ajan blastogenez evresindeki hücrelerin büyük kısmını öldürürse; embriyo bölünmeyi sürdüremez, adet kanaması benzeri bir kanamayla fark edilmeden spontan düşer (preklinik abortus).\n  - **Hafif Hasar (Hep):** Eğer hücrelerin yalnızca küçük bir kısmı ölürse; kalan totipotent hücreler ölenlerin yerini doldurarak eksiği tamamen kompanse eder ve bebek hiçbir anomali olmadan tamamen sağlıklı doğar.\n  - **İstisna:** Blastogenez sürecinde gastrulasyon ekseni bozulursa çok ağır orta hat blastogenez anomalileri (sakrokoksigeal teratom, sirenomeli, yapışık ikizler) ortaya çıkar.",
            "medicalTerms": [
                {"term": "Ya Hep Ya Hiç Prensibi", "explanation": "İlk 4 haftadaki teratojenik hasarın ya embriyoyu tamamen öldürmesi ya da hiçbir hasar bırakmadan tam iyileşmesi kuralı."},
                {"term": "Totipotensi", "explanation": "Erken embriyonik hücrelerin hem tüm embriyonik dokuları hem de ekstraembriyonik zarları oluşturabilme yeteneği."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Gebeliğin ilk 2-4 haftasında maruz kalınan teratojenlerde 'Ya Hep Ya Hiç' prensibi geçerlidir: Hasar ya düşüğe yol açar ya da çocuk tamamen sağlıklı doğar."
            ],
            "interactiveElements": [
                make_before_after(
                    "Ağır Blastogenez Hasarı ('Hiç')",
                    "Hafif Blastogenez Hasarı ('Hep')",
                    ["Hücrelerin büyük bölümü ölür", "İmplantasyon veya gastrulasyon çöker", "Fark edilmeyen çok erken spontan abortus"],
                    ["Kalan totipotent hücreler çoğalır", "Ölen hücrelerin fonksiyonunu tamamen kompanse eder", "Bebek tamamen kusursuz ve sağlıklı doğar"]
                ),
                make_micro_quiz(
                    "Son adet tarihinden 2 hafta sonra yüksek doz radyasyona maruz kalan bir kadının gebeliğinde 'Ya Hep Ya Hiç' prensibine göre beklenmesi gereken en olası iki sonuç nedir?",
                    {
                        "A": "Ya embriyo fark edilmeden düşer ya da tam kompanzasyonla tamamen sağlıklı doğar",
                        "B": "Kesinlikle fokomeli (kol yokluğu) ile doğar",
                        "C": "Sadece hafif tırnak displazisi oluşur",
                        "D": "Yalnızca zeka geriliği gelişir, organlar sağlam kalır"
                    },
                    "A",
                    {
                        "A": "Doğru! İlk haftalarda hücreler totipotenttir; hasar ya öldürür ya da geride hiçbir yapısal defekt bırakmadan tam iyileşir.",
                        "B": "Yanlış. Fokomeli 4-8. haftalardaki ekstremite tomurcuğu hasarında görülür.",
                        "C": "Yanlış. Bu fetogenez dönemi bulgusudur.",
                        "D": "Yanlış. Blastogenezde izole nörolojik defekt değil 'ya hep ya hiç' işler."
                    }
                )
            ]
        },
        {
            "slideNumber": 37,
            "title": "Blastogenez Anomalileri: Sakrokoksigeal Teratom, Sirenomeli ve Yapışık İkizler",
            "subtitle": "İlkel çizgi (primitive streak) ve kaudal morfogenez felaketleri",
            "badge": "Klinik Patoloji",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Blastogenez evresinin en kritik basamağı 3. haftadaki ==gastrulasyondur==. Bu evrede primitif çizgi (primitive streak) üzerinden epiblast hücreleri içeri göçerek ektoderm, mezoderm ve endodermi oluşturur.\n\nPrimitif çizgi anomalileri şu ağır tablolara yol açar:\n- **1. Sakrokoksigeal Teratom:** Primitif çizgi kalıntılarının kaudal bölgede regrese olmayıp kontrolsüz çoğalmasıyla oluşan, her üç germ yaprağını da içeren yenidoğanın en sık konjenital tümörüdür.\n- **2. Sirenomeli (Denizkızı Sendromu):** Kaudal mezodermin yetersiz göçü sonucu alt ekstremitelerin tek bir uzuv halinde birbirine yapışması, renal agenezi ve anüri ile seyreden ölümcül defekttir (maternal diyabetle güçlü ilişkili).\n- **3. Yapışık İkizler (Conjoined Twins):** Tek bir embriyonik diskin 13-15. günlerde tam olarak ikiye ayrılamaması sonucu ortaya çıkan monokoryonik monoamniyotik blastogenez anomalisidir.",
            "coreContent": {
                "table": {
                    "title": "Başlıca Blastogenez Dönemi Defektleri",
                    "headers": ["Anomali", "Embriyolojik Hata Mekanizması", "Temel Klinik Tablo"],
                    "rows": [
                        ["Sakrokoksigeal Teratom", "Primitif çizgi pluripotent hücrelerinin persistansı", "Sakrumda üç germ yaprağı içeren dev tümör (en sık yenidoğan tümörü)"],
                        ["Sirenomeli (Kaudal Regresyon)", "Kaudal mezodermin yetersiz göçü ve vasküler hırsızlık", "Alt uzuvların yapışıklığı, renal agenezi, oligohidramniyos"],
                        ["Yapışık İkizler", "Embriyonik diskin 13. günden sonra eksik ayrılması", "Torakopagus, kraniyopagus gibi gövde/kafa yapışıklıkları"],
                        ["Holoprozensefali (Ağır Form)", "Prekordal plağın erken orta hat belirleme hatası", "Siklopi, tek ventrikül, yüz ve ön beyin ayrılma kusuru"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Sakrokoksigeal Teratom", "explanation": "Primitif çizgi kalıntısından köken alan ve her 3 embriyonik tabakayı içeren en sık neonatal kitle."},
                {"term": "Sirenomeli", "explanation": "Kaudal mezoderm göç yetersizliğine bağlı alt uzuvların tek bir bacak halinde füzyonu (denizkızı sendromu)."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Sakrokoksigeal teratom, sirenomeli ve yapışık ikizler; fertilizasyonu takip eden ilk 4 haftadaki blastogenez/gastrulasyon evresinin defektleridir."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Sakrokoksigeal Teratom Oluşum Kaskadı",
                    [
                        "Gastrulasyonun 3. haftasında primitif çizgi kaudal uçta epiblast göçünü yönetir.",
                        "Normalde 4. haftanın sonunda primitif çizginin kaybolması ve dejenere olması gerekir.",
                        "Primitif çizgi kalıntıları sakrokoksigeal bölgede pluripotent kök hücreler olarak kalır.",
                        "Doğumda ektoderm, mezoderm ve endoderm türevleri içeren dev bir kitle (teratom) belirir."
                    ]
                ),
                make_micro_quiz(
                    "Yenidoğan bir bebekte saptanan en sık konjenital germ hücreli kitle olan 'sakrokoksigeal teratom' embriyolojik gelişim sürecinde hangi yapının kalıntısından köken alır?",
                    {
                        "A": "Primitif çizgi (Primitive streak)",
                        "B": "Nöral krest hücreleri",
                        "C": "Kardiyojenik mezoderm",
                        "D": "Rathke kesesi"
                    },
                    "A",
                    {
                        "A": "Doğru! Sakrokoksigeal teratom gastrulasyonda görev alan primitif çizginin pluripotent hücre kalıntılarından köken alır.",
                        "B": "Yanlış. Nöral krest nöroblastom veya melanom kökenidir.",
                        "C": "Yanlış. Kardiyojenik mezoderm kalbi oluşturur.",
                        "D": "Yanlış. Rathke kesesi kraniyofarenjiyom kökenidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 38,
            "title": "Embriyogenez Periyodu (4-8. Hafta): Primer Organogenez ve Maksimum Hasar Penceresi",
            "subtitle": "Kardiyak, nöral, ekstremite ve yüz taslaklarının geri dönüşsüz biçimlenmesi",
            "badge": "Maksimum Duyarlılık",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "4. hafta ile 8. hafta arası dönem (28 - 56. günler), insan yaşamının morfolojik açıdan en fırtınalı ve kader belirleyici zamanıdır.\n\nEmbriyogenez evresinin temel biyolojik dinamikleri:\n- **Organ Taslakları:** Kalp tüpü kıvrılır ve septalar oluşur; nöral tüp kapanır; optik ve otik veziküller belirir; kol ve bacak tomurcukları uzar.\n  - **Maksimum Hassasiyet:** Bu 4 haftalık dar pencerede maruz kalınan tek bir doz teratojenik ilaç (örneğin Talidomid) veya viral enfeksiyon (Rubella), ilgili organın oluşumunu kalıcı olarak durdurur ve ==majör malformasyon== üretir.\n  - **Özgül Pencereler:** Nöral tüp 4. haftanın sonunda kapanırken, kalp septasyonu 7. haftada, damak birleşmesi ise 8-9. haftada tamamlanır.",
            "medicalTerms": [
                {"term": "Embriyogenez", "explanation": "Fertilizasyonun 4. ile 8. haftaları arasında tüm temel organ taslaklarının şekillendiği kritik evre."},
                {"term": "Kritik Organogenez Penceresi", "explanation": "Belirli bir organın morfogenezinin sürdüğü ve teratojenik hasara en hassas olduğu dar zaman aralığı."}
            ],
            "spotPearls": [
                "Nöral tüp intrauterin 28. günde (4. haftanın sonu) tamamen kapanır; folik asit desteği bu nedenle konsepsiyondan ÖNCE başlanmalıdır!"
            ],
            "interactiveElements": [
                make_before_after(
                    "Embriyogenez Hasarı (4-8. Hafta)",
                    "Fetogenez Hasarı (9. Hafta Sonrası)",
                    ["Primer organogenez duraklar", "Ağır yapısal MAJÖR MALFORMASYON oluşur", "Örnek: Kalp defekti, uzuv yokluğu (fokomeli)"],
                    ["Oluşmuş organın dokusu etkilenir", "Hafif minör anomali, deformasyon veya fonksiyonel gerilik oluşur", "Örnek: Eklem kontraktürü, zeka geriliği, büyüme kısıtlılığı"]
                ),
                make_micro_quiz(
                    "Nöral tüp defektlerinin (örneğin meningomiyelosel ve anansefali) önlenmesinde folik asit desteğinin mutlaka gebelik planlanırken (konsepsiyondan önce) başlanmasının temel embriyolojik gerekçesi nedir?",
                    {
                        "A": "Nöral tüpün fertilizasyondan sonraki 28. günde (4. haftanın sonu) kapanmasını tamamlamış olması",
                        "B": "Folik asidin yalnızca sperm hücrelerini aktive etmesi",
                        "C": "Nöral dokunun 20. haftadan sonra oluşmaya başlaması",
                        "D": "Plasentanın ilk 8 hafta folik asit emilimi yapamaması"
                    },
                    "A",
                    {
                        "A": "Doğru! Nöral tüp gebeliğin ilk 28 gününde (henüz anne gebeliğini fark etmeden) kapanır; bu nedenle folik asit önceden kanda doygun olmalıdır.",
                        "B": "Yanlış. Folik asit maternal dokularda nöroepitelyal kapanma için gereklidir.",
                        "C": "Yanlış. Nöral plak 3. haftada başlar.",
                        "D": "Yanlış. Folik asit doğrudan maternal dolaşımdan diffüze olur."
                    }
                )
            ]
        },
        {
            "slideNumber": 39,
            "title": "Fetogenez Periyodu (9. Hafta - Doğum): Doku Büyümesi, Matürasyon ve Deformasyonlar",
            "subtitle": "Morfogenezden histogeneze geçiş ve mekanik intrauterin kısıtlanmalar",
            "badge": "Fetal Olgunlaşma",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "9. gebelik haftasından doğuma kadar olan süreç 'fetus' dönemi olarak adlandırılır. Bu evrede organların kaba anatomik taslakları zaten çizilmiştir; asıl olay büyüme ve dokusal farklılaşmadır (histogenez).\n\nFetogenez evresinin patoloji dinamikleri:\n- **Malformasyon Oluşmaz:** Bu dönemde artık yeni bir organ malformasyonu (örneğin Fallot tetralojisi veya anansefali) ortaya çıkamaz; çünkü o yapılar çoktan oluşmuştur.\n- **Deformasyonlar Ön Plandadır:** Büyüyen fetüsün intrauterin ortamda mekanik baskıya maruz kalması (oligohidramniyos, uterus anomalisi, çoğul gebelik) sonucu pes ekinovarus (çomak ayak) veya kafa deformasyonları şekillenir.\n- **Fonksiyonel Matürasyon Hasarı:** Bu dönemdeki alkol maruziyeti veya enfeksiyonlar beyin büyümesini ve nöronal göçü bozarak zeka geriliği ve mikrosefaliye neden olur.",
            "medicalTerms": [
                {"term": "Fetogenez", "explanation": "İntrauterin 9. haftadan doğuma kadar süren, dokusal büyüme ve fonksiyonel olgunlaşma evresi."},
                {"term": "Histogenez", "explanation": "Fetal dokularda hücrelerin özgül fonksiyonel hücre tiplerine ve matriks yapısına farklılaşması süreci."}
            ],
            "spotPearls": [
                "Fetogenez döneminde maruz kalınan etkenler majör anatomik malformasyon oluşturmaz; büyüme geriliği, deformasyon veya fonksiyonel hasar oluşturur."
            ],
            "interactiveElements": [
                make_cloze(
                    "İntrauterin 9. haftadan doğuma kadar süren ve organların büyümesi ile dokusal olgunlaşmasını kapsayan evreye fetogenez periyodu adı verilir.",
                    "fetogenez",
                    "Fetal büyüme periyodu"
                ),
                make_micro_quiz(
                    "Gebeliğin 24. haftasında geçirilen bir sitomegalovirüs (CMV) enfeksiyonunda aşağıdaki patolojilerden hangisinin ortaya çıkması embriyolojik olarak BEKLENMEZ?",
                    {
                        "A": "Fallot Tetralojisi (Kardiyak malformasyon)",
                        "B": "Mikrosefali (Beyin parankim büyüme geriliği)",
                        "C": "Sensörinöral işitme kaybı",
                        "D": "İntrauterin gelişme geriliği (IUGR)"
                    },
                    "A",
                    {
                        "A": "Doğru! Kalp septasyonu 7-8. haftada tamamlanır. 24. haftadaki bir enfeksiyon yeni bir Fallot tetralojisi malformasyonu oluşturamaz.",
                        "B": "Yanlış. Beyin gelişimi fetogenez boyunca sürer, mikrosefali oluşabilir.",
                        "C": "Yanlış. Koklea ve işitme siniri fetogenezde enfekte olabilir.",
                        "D": "Yanlış. Fetal enfeksiyonlar tipik olarak IUGR yapar."
                    }
                )
            ]
        },
        {
            "slideNumber": 40,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] İntrauterin Gelişim Dönemleri & Biyolojik Duyarlılık",
            "subtitle": "Blastogenez, embriyogenez ve fetogenezin eksiksiz karşılaştırma matrisi",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu modül, intrauterin gelişim dönemlerini, teratojenik duyarlılık pencerelerini ve tipik klinik hasar kalıplarını tek bir hafıza matrisinde birleştirmektedir.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Blastogenez (0 - 4. Hafta):** 'Ya Hep Ya Hiç' kuralı geçerlidir. Hasar ya düşüğe yol açar ya da çocuk tamamen sağlıklı doğar.\n- **Blastogenez İstisnaları:** Sakrokoksigeal teratom (primitif çizgi kalıntısı), Sirenomeli ve Yapışık ikizler bu evrede oluşur.\n- **Embriyogenez (4 - 8. Hafta):** Primer organogenez evresidir. Teratojenlere karşı ==MAKSİMUM DUYARLILIK== penceresidir; majör malformasyonlar bu evrede şekillenir.\n- **Nöral Tüp Kapanması:** ==28. Günde (4. haftanın sonu)== tamamlanır.\n- **Fetogenez (9. Hafta - Doğum):** Organlar oluşmuştur; büyüme ve histogenez sürer. Malformasyon oluşmaz; ==Deformasyon==, ==Disrupsiyon== ve ==Bilişsel Gerilik== oluşur.",
            "coreContent": {
                "table": {
                    "title": "Gelişim Dönemleri Büyük Karşılaştırma Matrisi",
                    "headers": ["Parametre", "Blastogenez (0 - 4. Hafta)", "Embriyogenez (4 - 8. Hafta)", "Fetogenez (9. Hafta - Doğum)"],
                    "rows": [
                        ["Hücresel Durum", "Totipotensi ve plastisite", "Hızlı hücre göçü ve farklılaşma", "Histogenez ve parankimal büyüme"],
                        ["Temel Biyolojik Olay", "İmplantasyon, gastrulasyon", "Primer organogenez (taslaklar)", "Fonksiyonel matürasyon"],
                        ["Teratojenik Hasar", "Ya Hep Ya Hiç (Düşük veya Sağlam)", "AĞIR MAJÖR MALFORMASYONLAR", "Deformasyonlar, IUGR, fonksiyonel kusur"],
                        ["Tipik Anomali Örneği", "Sakrokoksigeal teratom, Sirenomeli", "Fallot, Meningomiyelosel, Fokomeli", "Pes ekinovarus, Mikrosefali, Zeka geriliği"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Gastrulasyon", "explanation": "İlkel çizgi boyunca hücrelerin içe göçerek 3 embriyonik tabakayı (ektoderm, mezoderm, endoderm) oluşturması."},
                {"term": "Totipotent", "explanation": "Gelişimin en erken evresinde vücuttaki her türlü dokuyu oluşturabilme esnekliği."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] 0-4. Hafta: Ya Hep Ya Hiç | 4-8. Hafta: Maksimum Majör Malformasyon Riski | 9+ Hafta: Deformasyon ve Büyüme Kusuru.",
                "📌 [TEKRAR SPOTU] Nöral tüp 28. günde kapandığı için folik asit gebelikten önce alınmalıdır!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "İntrauterin Gelişim Dönemleri ve Hasar Yelpazesi Ezber Tablosu",
                    ["Gelişim Evresi", "Zaman Aralığı", "Temel Hasar Tipi"],
                    [
                        [("Blastogenez", False), ("0 - 4. Hafta", True, "İlk ay"), ("Ya Hep Ya Hiç Kuralı", True, "Düşük / Sağlam")],
                        [("Embriyogenez (En Hassas)", False), ("4 - 8. Hafta", True, "2. ay"), ("Ağır Majör Organ Malformasyonu", True, "Majör kusur")],
                        [("Fetogenez", False), ("9. Hafta - Doğum", True, "Fetal dönem"), ("Deformasyon & Bilişsel Kusurlar", True, "Deformasyon")]
                    ]
                ),
                make_micro_quiz(
                    "Gebe bir kadının 6. gebelik haftasında rubella (kızamıkçık) virüsü ile enfekte olması durumunda bebekte aşağıdaki kardiyak malformasyonlardan hangisinin gelişme riski en yüksektir?",
                    {
                        "A": "Patent Duktus Arteriyozus (PDA) ve Pulmoner Arter Stenozu",
                        "B": "Hiçbir hasar oluşmaz (Ya hep ya hiç kuralı işler)",
                        "C": "Yalnızca hafif tırnak hipoplazisi gelişir",
                        "D": "Doğumdan sonra kendiliğinden düzelen pozisyonel deformasyon oluşur"
                    },
                    "A",
                    {
                        "A": "Doğru! 6. hafta kardiyak organogenezin kalbidir; konjenital rubella sendromu tipik olarak PDA ve pulmoner arter darlığı malformasyonuna yol açar.",
                        "B": "Yanlış. 'Ya hep ya hiç' ilk 4 haftada geçerlidir, 6. hafta organogenez zirvesidir.",
                        "C": "Yanlış. Rubella ağır kardiyak ve nörosensoriyel defektler yapar.",
                        "D": "Yanlış. Malformasyonlar kendiliğinden düzelmez, cerrahi onarım gerektirir."
                    }
                ),
                make_micro_quiz(
                    "Gastrulasyon evresinde primitif çizginin kaudal ucunun zamanında regrese olmaması ve pluripotent hücrelerin aşırı çoğalması sonucu ortaya çıkan anomali hangisidir?",
                    {
                        "A": "Sakrokoksigeal Teratom",
                        "B": "Meningomiyelosel",
                        "C": "Fallot Tetralojisi",
                        "D": "DiGeorge Sendromu"
                    },
                    "A",
                    {
                        "A": "Doğru! Primitif çizgi kalıntısı sakrokoksigeal teratoma yol açar; yenidoğanın en sık görülen teratomudur.",
                        "B": "Yanlış. Meningomiyelosel nöral tüp kapanma kusurudur.",
                        "C": "Yanlış. Fallot kardiyak konotrunkustur.",
                        "D": "Yanlış. DiGeorge 22q11.2 mikrodelesyonudur."
                    }
                )
            ]
        }
    ]
