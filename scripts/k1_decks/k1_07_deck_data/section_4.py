"""
Bölüm 4: Protein Birikimleri: Reabsorpsiyon Damlacıkları, Russell Cisimcikleri ve Alkolik Hiyalin
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
        "title": "Protein Birikimlerinin Genel İlkeleri ve Hiyalin Morfolojisi",
        "subtitle": "Artmış sentez, aşırı alım ve yetersiz yıkıma bağlı eozinofilik agregatlar",
        "badge": "Protein Birikimi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Hücre içi protein birikimleri lipid birikimlerine kıyasla daha az sıklıkta görülmekle birlikte, ciddi "
            "hücresel hasarın ve metabolik aşırı yükün kritik göstergeleridir. Birikim temel olarak üç ana nedenden "
            "kaynaklanır: 1) Hücrenin dışarıdan aşırı miktarda protein alması (pinositoz/endositoz), 2) Hücrenin "
            "normalden kat kat fazla protein sentezlemesi, 3) Protein katlanma, taşınma veya yıkımındaki aksaklıklar.\n\n"
            "> [YÜKSEK VERİM] Mikroskobik olarak biriken proteinler çoğunlukla homojen, camsı, parlak pembe (eozinofilik) "
            "damlacıklar veya kitleler halinde görülür; bu morfolojik görüntüye 'hiyalin' (hyaline) adı verilir.\n\n"
            "Hiyalin terimi özgül bir biyokimyasal maddeyi değil, ışık mikroskobundaki camsı eozinofilik fiziksel paterni tanımlar."
        ),
        "medicalTerms": [
            {"term": "Hiyalin", "explanation": "Işık mikroskobunda homojen, camsı, pembe boyanan amorf yapıyı tanımlayan morfolojik terimdir."},
            {"term": "Eozinofilik Damlacık", "explanation": "Sitoplazmada eozin boyasını kuvvetle tutan yuvarlak protein çökeltisidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hiyalin spesifik bir madde adı değil, camsı pembe morfolojik bir tanımlamadır.",
            "📌 [SINAV SPOTU] Hücre içi protein birikimleri H&E kesitlerinde parlak eozinofilik görünür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mekanik Üçlü", "desc": "Aşırı alım, hipersekresyon veya proteazom yıkım defekti.", "isKey": True},
                {"title": "Görünüm", "desc": "Sitoplazmik parlak pembe damlacıklar veya amorf hiyalin kitleler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Işık mikroskobunda homojen, parlak ve camsı pembe eozinofilik görünüme hiyalin adı verilir.",
                "hiyalin",
                "Camsı pembe protein morfolojisini niteleyen histolojik terim"
            ),
            make_active_recall(
                "Patolojide kullanılan 'hiyalin' terimi ne anlama gelir?",
                "Özgül bir kimyasal maddeyi değil, ışık mikroskobunda homojen, camsı ve pembe (eozinofilik) görünen morfolojik paterni ifade eder."
            )
        ]
    })

    # ADIM 32
    slides.append({
        "slideNumber": 32,
        "title": "Böbrek Proksimal Tübül Hücrelerinde Reabsorpsiyon Damlacıkları",
        "subtitle": "Glomerüler sızıntı, endositoz ve lizozomal füzyonun eozinofilik damlacıkları",
        "badge": "Tübüler Reabsorpsiyon",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Böbrek proksimal tübül hücreleri, normal koşullarda idrar filtratına kaçan çok az miktardaki albümini "
            "apikal mikrovillusları (megalin-kübilin reseptör kompleksi) aracılığıyla pinositozla geri emer. Glomerüler "
            "kapiller geçirgenliğin bozulduğu nefrotik sendrom gibi durumlarda ise idrara masif miktarda protein dökülür.\n\n"
            "> [SINAV SPOTU] Proksimal tübül hücreleri aşırı miktarda albümini içeri alır; pinositoz vezikülleri "
            "lizozomlarla birleşir ve sitoplazmada parlak pembe 'protein reabsorpsiyon damlacıkları' oluşturur.\n\n"
            "Bu süreç hücrenin aşırı iş yükünü yansıtır ve tübül epitelinde belirgin eozinofilik granülasyona neden olur."
        ),
        "medicalTerms": [
            {"term": "Protein Reabsorpsiyon Damlacığı", "explanation": "Aşırı filtrelenen proteinlerin proksimal tübül sitoplazmasında lizozomla birleşip oluşturduğu eozinofilik veziküldür."},
            {"term": "Megalin-Kübilin", "explanation": "Proksimal tübül apikal zarında albümin emilimini yürüten reseptör kompleksidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Proksimal tübül epiteli aşırı protein kaçağında parlak eozinofilik damlacıklar içerir.",
            "📌 [SINAV SPOTU] Proteinüri tedavi edildiğinde bu reabsorpsiyon damlacıkları tamamen kaybolur (reversibldir)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Giriş Yolu", "desc": "Glomerüler kaçak sonrası apikal reseptör aracılı endositoz.", "isKey": True},
                {"title": "Kaderi", "desc": "Lizozomal hidrolazlarla amino asitlere sindirilip kana geri verilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Tübüler Protein Reabsorpsiyon Damlacığı Oluşumu",
                [
                    "1. Glomerüler Hasar: Filtrasyon bariyeri bozularak idrara masif albümin dökülür.",
                    "2. Apikal Pinositoz: Proksimal tübül epitel hücreleri proteini endositoz vezikülleriyle yutar.",
                    "3. Lizozomal Füzyon: Protein yüklü endozomlar primer lizozomlarla kaynaşır.",
                    "4. Eozinofilik Damlacık: Sitoplazmada parlak pembe yuvarlak protein damlacıkları kümelenir."
                ]
            ),
            make_cloze(
                "Nefrotik sendromda idrara kaçan proteinleri geri emen böbrek proksimal tübül hücrelerinde eozinofilik damlacıklar birikir.",
                "proksimal tübül",
                "Filtrattaki proteinleri geri emen nefron segmenti"
            )
        ]
    })

    # ADIM 33
    slides.append({
        "slideNumber": 33,
        "title": "Nefrotik Sendrom Patofizyolojisi ve Proteinüri-Damlacık Korelasyonu",
        "subtitle": "Geri dönüşümlü hücresel yük ve tübüler adaptasyon kapasitesi",
        "badge": "Nefrotik Korelasyon",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Nefrotik sendrom, günde 3.5 gramın üzerinde masif proteinüri, hipoalbüminemi, yaygın periferik ödem ve "
            "hiperlipidemi ile karakterize klinik bir tablodur. Glomerül podositlerinin ayak çıkıntılarının silinmesi "
            "veya bazal membran geçirgenliğinin artması proksimal tübüllere devasa bir protein akışı sağlar.\n\n"
            "> [TEMEL İLKE] Proksimal tübüllerdeki protein reabsorpsiyon damlacıkları tamamen geri dönüşümlü (reversibl) bir "
            "lezyondur; altta yatan glomerülopati tedavi edildiğinde ve proteinüri durduğunda tübüller normale döner.\n\n"
            "Ancak proteinüri kontrol altına alınamaz ve yıllarca sürerse, aşırı protein yükü tübüler epitelde apoptozu ve "
            "tübülointerstisyel fibrozisi tetikleyerek kronik böbrek yetmezliğine katkıda bulunur."
        ),
        "medicalTerms": [
            {"term": "Nefrotik Sendrom", "explanation": "Ağır proteinüri (>3.5 g/gün), hipoalbüminemi ve ödemle seyreden böbrek tablosudur."},
            {"term": "Tübülointerstisyel Fibrozis", "explanation": "Kronik tübüler stres ve protein toksisitesi sonucu interstisyumda bağ dokusu artışıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Proksimal tübüllerdeki protein damlacıkları kalıcı bir doku ölümü değil, geri dönüşümlü bir adaptasyondur.",
            "📌 [SINAV SPOTU] Proteinüri kesildiğinde damlacıklar lizozomlarca sindirilerek sitoplazmadan temizlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Geri Dönüşüm", "desc": "Glomerüler kaçak durduğunda hücreler tamamen temizlenir.", "isKey": True},
                {"title": "Kronik Toksisite", "desc": "Tedavi edilmeyen masif proteinüri interstisyel skara zemin hazırlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Akut Proteinüri vs Tedavi Sonrası Proksimal Tübül",
                "Akut Masif Proteinüri Evresi",
                "Sitoplazma çok sayıda parlak pembe eozinofilik reabsorpsiyon damlacığı ile doludur; tübül epiteli şişmiştir.",
                "Tedavi Sonrası (Proteinürisiz Evre)",
                "Lizozomal hidrolazlar biriken proteini amino asitlere sindirmiştir; sitoplazma berrak ve normal morfolojisine dönmüştür."
            ),
            make_active_recall(
                "Nefrotik sendromlu bir hastada proksimal tübüllerdeki protein birikiminin en önemli prognoz özelliği nedir?",
                "Proteinüri düzeltildiğinde tamamen geri dönüşümlü (reversibl) olması ve sitoplazmanın normale dönebilmesidir."
            )
        ]
    })

    # ADIM 34
    slides.append({
        "slideNumber": 34,
        "title": "Plazma Hücrelerinde İmmünoglobulin Birikimi ve Russell Cisimcikleri",
        "subtitle": "Granüllü endoplazmik retikulum genişlemesi ve eozinofilik küresel inklüzyonlar",
        "badge": "Russell Cisimcikleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Plazma hücreleri vücudun profesyonel antikor (immünoglobulin) fabrikalarıdır. Yoğun kronik inflamatuvar "
            "süreçlerde veya antikor sekresyonunun sentez hızına yetişemediği durumlarda, üretilen immünoglobulinler "
            "granüllü endoplazmik retikulum (GER) sisternalarında hapsolur ve dışarı salınamaz.\n\n"
            "> [SINAV SPOTU] GER sisternaları aşırı protein dolumuyla devasa şekilde genişler ve ışık mikroskobunda "
            "sitoplazmayı dolduran büyük, homojen, eozinofilik küreler oluşturur; bu yapılara 'Russell cisimcikleri' denir.\n\n"
            "Çok sayıda Russell cisimciği içeren ve 'dut meyvesi' görünümü alan plazma hücrelerine literatürde "
            "'Mott hücresi' adı da verilir."
        ),
        "medicalTerms": [
            {"term": "Russell Cisimciği", "explanation": "Plazma hücresinin granüllü ER sisternalarında biriken homojen eozinofilik immünoglobulin küresidir."},
            {"term": "Mott Hücresi", "explanation": "Sitoplazması çok sayıda Russell cisimciğiyle dolu olan plazma hücresidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Russell cisimciği plazma hücresi GER'sinde biriken immünoglobulindir.",
            "📌 [SINAV SPOTU] Histolojide parlak eozinofilik homojen yuvarlak intrasitoplazmik inklüzyondur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücre Tipi", "desc": "Plazma hücresi (B lenfosit kökenli efektör hücre).", "isKey": True},
                {"title": "Organel Lokalizasyonu", "desc": "Granüllü endoplazmik retikulum sisternaları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Kronik osteomiyelit odağından alınan doku biyopsisinde yoğun plazma hücresi infiltrasyonu izleniyor. Bazı plazma hücrelerinin sitoplazmasında granüllü ER'nin aşırı genişlemesine bağlı parlak pembe, homojen küresel yapılar görülüyor. Bu patolojik inklüzyon aşağıdakilerden hangisidir?",
                {
                    "A": "Mallory-Denk cisimciği",
                    "B": "Russell cisimciği",
                    "C": "Lewy cisimciği",
                    "D": "Councilman cisimciği",
                    "E": "Negri cisimciği"
                },
                "B",
                {
                    "A": "Mallory-Denk hepatositlerde sitokeratin birikimidir.",
                    "B": "Doğru! Russell cisimciği plazma hücrelerinde GER içinde biriken immünoglobulin inklüzyonudur.",
                    "C": "Lewy cisimciği Parkinson nöronlarında alfa-sinüklein birikimidir.",
                    "D": "Councilman cisimciği apoptotik hepatosittir.",
                    "E": "Negri cisimciği kuduz virüsü inklüzyonudur."
                }
            ),
            make_cloze(
                "Plazma hücrelerinde üretilen aşırı immünoglobulinlerin granüllü ER sisternalarında birikmesiyle oluşan eozinofilik kürelere Russell cisimcikleri denir.",
                "Russell cisimcikleri",
                "Plazma hücresi ER'sindeki protein küreleri"
            )
        ]
    })

    # ADIM 35
    slides.append({
        "slideNumber": 35,
        "title": "Dutcher Cisimcikleri ve Multipl Miyelomda Plazma Hücre İnfiltrasyonu",
        "subtitle": "İntranükleer yalancı inklüzyonlar ve monoklonal immünoglobulin yükü",
        "badge": "Miyelom İnklüzyonları",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Multipl miyelom ve Waldenström makroglobulinemisi gibi neoplastik plazma hücresi diskrazilerinde immünoglobulin "
            "üretimi aşırı ve kontrolsüzdür. Bu malign plazma hücrelerinde immünoglobulinler bazen çekirdek zarının "
            "içine doğru invagine olarak çekirdek içinde yerleşmiş gibi görünen 'psödoinklüzyonlar' oluşturur.\n\n"
            "> [YÜKSEK VERİM] Çekirdekte izlenen bu eozinofilik immünoglobulin birikintilerine 'Dutcher cisimcikleri' "
            "(Dutcher bodies) adı verilir ve neoplastik plazma hücresi süreçlerinde son derece değerlidir.\n\n"
            "Patolog kemik iliği veya lenf nodu biyopsisinde Russell (sitoplazmik) ve Dutcher (nükleer) cisimciklerini "
            "birlikte gördüğünde plazma hücreli diskraziyi öncelikle düşünür."
        ),
        "medicalTerms": [
            {"term": "Dutcher Cisimciği", "explanation": "Plazma hücresi çekirdeğinde yerleşmiş gibi görünen eozinofilik immünoglobulin psödoinklüzyonudur."},
            {"term": "Multipl Miyelom", "explanation": "Kemik iliğinde monoklonal plazma hücresi proliferasyonuyla giden malign hematolojik hastalıktır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Russell cisimciği sitoplazmada, Dutcher cisimciği nükleusta (psödoinklüzyon) yerleşir.",
            "📌 [SINAV SPOTU] Her iki cisimcik de immünoglobulin kökenli protein agregatlarıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Russell Cisimciği", "desc": "Sitoplazmada GER içinde biriken immünoglobulin.", "isKey": True},
                {"title": "Dutcher Cisimciği", "desc": "Çekirdekte psödoinklüzyon oluşturan immünoglobulin.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["İnklüzyon Adı", "Hücresel Lokalizasyon", "Biriken Madde", "Klinik Önem"],
                [
                    [("Russell Cisimciği", False, ""), ("Sitoplazma (Granüllü ER)", True, "Plazma hücresi sitozolündeki organel"), ("İmmünoglobulin", False, ""), ("Kronik inflamasyon / Miyelom", False, "")],
                    [("Dutcher Cisimciği", False, ""), ("Çekirdek (Nükleus psödoinklüzyon)", True, "Nükleer membran invajinasyonu"), ("İmmünoglobulin", False, ""), ("Multipl miyelom / Lenfoma", False, "")]
                ]
            ),
            make_cloze(
                "Plazma hücre çekirdeğinde izlenen immünoglobulin kaynaklı eozinofilik inklüzyonlara Dutcher cisimcikleri adı verilir.",
                "Dutcher cisimcikleri",
                "Çekirdekte yerleşen immünoglobulin inklüzyonunun adı"
            )
        ]
    })

    # ADIM 36
    slides.append({
        "slideNumber": 36,
        "title": "Hücre İskeleti Proteinlerinin Agregasyonu: Sitokeratinler ve Ara Filamentler",
        "subtitle": "Mikrotübüller, mikrofilamentler ve ara filamentlerin hasar karşısındaki stabilitesi",
        "badge": "Sitoiskelet Agregasyonu",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Hücre iskeleti (sitoiskelet), hücreye şekil veren ve hücre içi organel taşınmasını yürüten üç ana proteinden "
            "oluşur: aktin mikrofilamentleri, tübülin mikrotübülleri ve ara filamentler. Ara filamentler kimyasal ve mekanik "
            "strese en dayanıklı iskelet elemanlarıdır ve hücre tipine göre özgüllük gösterir (epitelde sitokeratinler, "
            "mezenşimde vimentin, kasta desmin, nöronlarda nörofilamentler).\n\n"
            "> [TEMEL İLKE] Ağır toksik, metabolik veya oksidatif hasar altında ara filamentler çapraz bağlanarak "
            "katlanamaz hale gelir ve erimeyen dev agregatlar oluşturur.\n\n"
            "Bu agregatlar ubikitinlenmesine rağmen proteazomlar tarafından eritilemez ve sitoplazmada karakteristik "
            "inklüzyon kitleleri olarak hapsolur."
        ),
        "medicalTerms": [
            {"term": "Ara Filament (Intermediate Filament)", "explanation": "Hücreye gerilme direnci kazandıran 10 nm çapındaki dayanıklı sitoiskelet lifleridir."},
            {"term": "Sitokeratin", "explanation": "Epitel hücrelerinin karakteristik ara filament protein ailesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Epitel hücrelerinin ara filamenti sitokeratin, mezenşimin vimentin, kasın desmindir.",
            "📌 [SINAV SPOTU] Toksik hasarda sitokeratinler ubikitinlenip agregat oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dirençli İskelet", "desc": "Mekanik strese dayanıklı ara filament ailesi.", "isKey": True},
                {"title": "Toksik Agregasyon", "desc": "Aşırı oksidatif hasarla ubikitinli sitokeratin yumakları oluşur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Epitel hücrelerinin karakteristik ara filament proteini sitokeratin olup hasar anında hücre içi agregatlar yapar.",
                "sitokeratin",
                "Epitel hücre iskeletini oluşturan temel ara filament"
            ),
            make_active_recall(
                "Hücre iskeleti proteinleri toksik hasar gördüğünde hücre onları yıkmak için hangi biyokimyasal etiketi ekler?",
                "Ubikitin proteinini kovalent olarak ekler; ancak agregat çok büyükse proteazom sistemi bu kompleksi eritemez."
            )
        ]
    })

    # ADIM 37
    slides.append({
        "slideNumber": 37,
        "title": "Alkolik Hiyalin (Mallory-Denk Cisimcikleri) Patogenezi ve Morfolojisi",
        "subtitle": "Hepatosit sitoplazmasında kıvrıntılı eozinofilik sitokeratin agregatları",
        "badge": "Mallory-Denk",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Mallory-Denk cisimcikleri (eski adıyla alkolik hiyalin), en sık alkolik hepatitte ve şiddetli alkol dışı "
            "steatohepatitte (MASH) balonlaşmış dejenere hepatositlerin sitoplazmasında izlenen son derece özgün inklüzyonlardır. "
            "Biyokimyasal analizleri, bu cisimciklerin ubikitine bağlanmış sitokeratin 8 ve sitokeratin 18 ara filament "
            "yumaklarından ve p62 kofaktöründen oluştuğunu göstermiştir.\n\n"
            "> [SINAV SPOTU] Işık mikroskobunda çekirdek komşuluğunda kıvrıntılı, halat veya ip yumağına benzeyen, "
            "düzensiz sınırlı parlak eozinofilik kitleler olarak izlenirler.\n\n"
            "Mallory-Denk cisimciği içeren hepatositlerin etrafı sıklıkla nötrofil lökositler tarafından kuşatılır; bu durum "
            "şiddetli hücresel hasar ve nekrozun habercisidir."
        ),
        "medicalTerms": [
            {"term": "Mallory-Denk Cisimciği", "explanation": "Hepatositlerde sitokeratin 8/18 ve ubikitinden oluşan eozinofilik halat benzeri inklüzyondur."},
            {"term": "Balonlaşma Dejenerasyonu", "explanation": "Sitoiskelet yıkımı ve sıvı birikimiyle hepatositlerin devasa ve soluk şişmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mallory-Denk cisimcikleri sitokeratin ara filamentleri ve ubikitinden oluşur.",
            "📌 [SINAV SPOTU] En sık alkolik hepatitte, ayrıca Wilson hastalığı ve MASH'te görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Protein İçeriği", "desc": "Sitokeratin 8/18, ubikitin ve p62 proteini.", "isKey": True},
                {"title": "Mikroskobik Şekil", "desc": "Halat/kordon benzeri düzensiz eozinofilik sitoplazmik kitle.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Kronik alkol bağımlısı bir hastada sarılık, ateş ve lökositoz tablosu gelişiyor. Karaciğer biyopsisinde balonlaşmış hepatositlerin sitoplazmasında kıvrıntılı, halat benzeri parlak eozinofilik kitleler ve etrafında nötrofil infiltrasyonu saptanıyor. Bu inklüzyonun temel biyokimyasal içeriği hangisidir?",
                {
                    "A": "Granüllü ER sisternalarında biriken immünoglobulinler",
                    "B": "Sitokeratin ara filamentleri ve ubikitin kompleksi (Mallory-Denk cisimciği)",
                    "C": "Lizozomlarda biriken sfingomiyelin kristalleri",
                    "D": "Pinositozla geri emilmiş albümin damlacıkları",
                    "E": "Çekirdeğe invagine olmuş ferritin molekülleri"
                },
                "B",
                {
                    "A": "GER'de immünoglobulin Russell cisimciğidir.",
                    "B": "Doğru! Mallory-Denk cisimcikleri sitokeratin 8/18 ara filamentleri ve ubikitinden oluşur.",
                    "C": "Sfingomiyelin Niemann-Pick hastalığı lizozomlarında birikir.",
                    "D": "Albümin damlacıkları böbrek proksimal tübülündedir.",
                    "E": "Ferritin hemosiderin pigmentinin öncülüdür."
                }
            ),
            make_cloze(
                "Hepatositlerde sitokeratin ara filamentlerinin ubikitinle agregat yapması sonucu Mallory-Denk cisimcikleri meydana gelir.",
                "Mallory-Denk cisimcikleri",
                "Alkolik hepatitteki sitokeratin içerikli inklüzyonların adı"
            )
        ]
    })

    # ADIM 38
    slides.append({
        "slideNumber": 38,
        "title": "Nörofibriler Yumaklar ve Tau Proteini Agregatları (Alzheimer Modeli)",
        "subtitle": "Hiperfosforile mikrotübül ilişkili proteinlerin nörodejeneratif agregasyonu",
        "badge": "Nörofibriler Yumak",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Nöronal sitoiskeletin kararlılığı, mikrotübülleri bir arada tutan mikrotübül ilişkili proteinlere (özellikle Tau) "
            "bağlıdır. Alzheimer hastalığında ve diğer tauopatilerde Tau proteini anormal şekilde aşırı fosforillenir "
            "(hiperfosforilasyon). Hiperfosforile olan Tau mikrotübüllerden ayrılır, serbest sitozolde eşleşmiş helikal "
            "filamentler (PHF) halinde bükülerek birikir.\n\n"
            "> [YÜKSEK VERİM] Nöron gövdesinde alev veya sepet şeklinde izlenen bu çözünmeyen intraselüler agregatlara "
            "'nörofibriler yumak' (neurofibrillary tangle - NFT) adı verilir.\n\n"
            "NFT'ler nöron içi aksonal taşımayı tamamen çökertir, sinaps kaybına yol açar ve hücreyi apoptoza sürükleyerek "
            "ağır demans tablosuna neden olur."
        ),
        "medicalTerms": [
            {"term": "Nörofibriler Yumak (NFT)", "explanation": "Nöron sitoplazmasında hiperfosforile Tau proteinlerinin oluşturduğu alev benzeri agregattır."},
            {"term": "Hiperfosforile Tau", "explanation": "Mikrotübülleri stabilize etme yeteneğini kaybedip toksik filamentler oluşturan proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nörofibriler yumakların temel proteini hiperfosforile Tau'dur.",
            "📌 [SINAV SPOTU] Alzheimer hastalığında nöron içi Tau yumakları ve nöron dışı amiloid beta plakları bulunur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Protein Modifikasyonu", "desc": "Anormal fosforilasyon mikrotübül ayrılmasına yol açar.", "isKey": True},
                {"title": "Aksonal Blokaj", "desc": "Nörotransmitter ve vezikül taşınması durarak nöron ölür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Mallory-Denk Cisimciği vs Nörofibriler Yumak",
                "Mallory-Denk Cisimciği",
                "Hepatosit sitoplazmasında sitokeratin ara filamentleri ve ubikitinden oluşan, alkolik hepatitte izlenen kord benzeri agregattır.",
                "Nörofibriler Yumak (NFT)",
                "Santral sinir sistemi nöronlarında hiperfosforile Tau proteininden oluşan, Alzheimer hastalığında aksonal taşımayı bozan alev şekilli agregattır."
            ),
            make_active_recall(
                "Alzheimer hastalığında nöron sitoplazmasında biriken nörofibriler yumakların temel protein içeriği nedir?",
                "Hiperfosforile Tau proteinidir."
            )
        ]
    })

    # ADIM 39 - CHECKPOINT 4
    slides.append({
        "slideNumber": 39,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Protein Birikimleri ve Morfolojik Formlar",
        "subtitle": "Tübüler damlacıklar, Russell, Dutcher, Mallory-Denk ve NFT'lerin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 4,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında hücre içi protein birikimlerinin klinik ve patolojik çeşitlerini özetliyoruz. "
            "Protein birikimleri eozinofilik, camsı hiyalin morfolojisiyle tanınır. 1) Böbrek proksimal tübülünde "
            "proteinüriye bağlı reabsorpsiyon damlacıkları (tamamen geri dönüşümlü), 2) Plazma hücrelerinde aşırı "
            "immünoglobulin birikimi: sitoplazmada Russell cisimcikleri, çekirdekte Dutcher cisimcikleri, "
            "3) Hepatositlerde sitokeratin agregatları: Mallory-Denk cisimcikleri (alkolik hepatit), 4) Nöronlarda "
            "hiperfosforile Tau: nörofibriler yumaklar (Alzheimer).\n\n"
            "> [KLİNİK İPUCU] Sınavda organ, tutulan hücre tipi ve proteinin biyokimyasal kaynağını eşleştirmek kritik puandır.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle pekiştiriniz."
        ),
        "medicalTerms": [
            {"term": "Hiyalin İnklüzyon", "explanation": "Hücre içi protein agregatlarının H&E boyasında verdiği camsı parlak pembe yapıdır."},
            {"term": "Mallory-Denk", "explanation": "Sitokeratin 8/18 ara filament yumaklarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Russell cisimciği = Plazma hücresi GER'inde immünoglobulin.",
            "📌 [SINAV SPOTU] Mallory-Denk = Hepatositte sitokeratin ara filamentleri.",
            "📌 [SINAV SPOTU] Proksimal tübül damlacıkları = Albümin reabsorpsiyonu (reversibl)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Böbrek", "desc": "Proksimal tübülde albümin reabsorpsiyon vezikülleri.", "isKey": True},
                {"title": "Plazma Hücresi", "desc": "GER'de Russell cisimcikleri, nükleusta Dutcher.", "isKey": True},
                {"title": "Karaciğer", "desc": "Balonlaşmış hücrede sitokeratinli Mallory-Denk.", "isKey": True},
                {"title": "Nöron", "desc": "Tau proteinli nörofibriler yumaklar.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-10",
                "Russell cisimcikleri hangi hücrede, hangi organelde ve ne birikmesiyle oluşur?",
                "Plazma hücresinde, granüllü endoplazmik retikulum sisternalarında, aşırı immünoglobulin birikmesiyle oluşur.",
                "Plazma hücresi ve immünoglobulin inklüzyonu"
            ),
            make_flashcard(
                "k1-07-fc-11",
                "Mallory-Denk cisimciklerinin (alkolik hiyalin) temel biyokimyasal bileşenleri nelerdir?",
                "Sitokeratin ara filamentleri (özellikle sitokeratin 8 ve 18), ubikitin ve p62 proteinidir.",
                "Hepatosit sitoiskelet agregatı bileşenleri"
            ),
            make_flashcard(
                "k1-07-fc-12",
                "Nefrotik sendromlu hastanın böbrek tübüllerinde görülen protein reabsorpsiyon damlacıklarının geri dönüşümlülük durumu nedir?",
                "Tamamen geri dönüşümlüdür (reversibl); proteinüri ortadan kalktığında tübül hücreleri damlacıkları sindirerek normale döner.",
                "Tübüler proteinüri yanıtı ve reversibilite"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Plazma hücrelerinin granüllü ER sisternalarında biriken eozinofilik immünoglobulin kürelerine Russell cisimcikleri denir.",
                "Russell cisimcikleri",
                "Plazma hücresindeki protein inklüzyonları"
            )
        ]
    })

    # ADIM 40
    slides.append({
        "slideNumber": 40,
        "title": "Protein Birikimlerinin Klinik Ayırıcı Tanısı ve Sentez",
        "subtitle": "Biyopsi değerlendirmesinde proteinopatilerin ve hücresel inklüzyonların haritası",
        "badge": "Klinik Sentez",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Patolojik incelemede eozinofilik hiyalin inklüzyon görüldüğünde hekim klinik tabloyu hızla entegre etmelidir. "
            "Proteinürik bir hastanın böbrek biyopsisinde tübül içi pembe damlacıklar reabsorpsiyonu; multipl miyelom şüpheli "
            "kemik iliğinde Russell ve Dutcher cisimcikleri monoklonal gama-patileri; alkolizm öyküsü olan sarılıklı "
            "hastada Mallory-Denk cisimcikleri hepatiti; demanslı yaşlı hastada nörofibriler yumaklar Alzheimer hastalığını "
            "doğrular.\n\n"
            "> [KLİNİK İPUCU] Bu inklüzyonların varlığı hücrenin ya aşırı iş yükü altında olduğunu ya da yıkım kapasitesinin "
            "iflas ettiğini açıkça gösterir.\n\n"
            "Erken evredeki yükler temizlenebilirken, fibriler agregatlar hücresel ölümü kaçınılmaz hale getirir."
        ),
        "medicalTerms": [
            {"term": "Proteinopati", "explanation": "Hatalı katlanan veya biriken proteinlerin hücre hasarına yol açtığı hastalıklar spektrumudur."},
            {"term": "Gamapati", "explanation": "Plazma hücrelerinin anormal veya monoklonal immünoglobulin üretmesi durumudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Böbrekte albümin, kemik iliğinde immünoglobulin, karaciğerde sitokeratin inklüzyonu aranır.",
            "📌 [SINAV SPOTU] Agregatlar hücresel protein kalitesi kontrol sistemlerinin çöktüğünü gösterir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Doku Ayrımı", "desc": "Böbrek, kemik iliği, karaciğer ve beyin spesifik protein desenleri.", "isKey": True},
                {"title": "Klinik Yansıma", "desc": "Nefrotik sendrom, miyelom, alkolik siroz, Alzheimer.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Kemik ağrıları, anemi ve böbrek fonksiyon bozukluğu olan 65 yaşında bir hastanın kemik iliği biyopsisinde plazma hücre infiltrasyonu izleniyor. Plazma hücrelerinin sitoplazmasında çok sayıda Russell cisimciği ve çekirdeğinde Dutcher psödoinklüzyonları saptanıyor. En uygun tanısal yaklaşım nedir?",
                [
                    {
                        "text": "Karaciğer yetmezliğine bağlı Mallory-Denk birikimi düşünülüp karaciğer nakli planlanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Mallory-Denk karaciğer hepatositlerindedir; bu hasta plazma hücre neoplazisi taşımaktadır."
                    },
                    {
                        "text": "Multipl miyelom / plazma hücreli diskrazi yönünden serum protein elektroforezi ve immünfiksasyon yapılmalıdır.",
                        "isCorrect": True,
                        "feedback": "Kusursuz yaklaşım! Russell ve Dutcher cisimciklerinin kemik iliğinde yoğun plazma hücreleriyle birlikteliği multipl miyelomu işaret eder."
                    }
                ]
            ),
            make_active_recall(
                "Histopatolojide saptanan Mallory-Denk cisimciği ile Russell cisimciği arasındaki en temel 2 fark nedir?",
                "Mallory-Denk hepatositte sitokeratin ara filamentlerinden oluşur; Russell cisimciği ise plazma hücresinde ER içinde immünoglobulinden oluşur."
            )
        ]
    })

    return slides
