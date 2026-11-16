"""
Bölüm 10: Metastatik Kalsifikasyon Etiyolojisi, Organ Tutulumları ve Büyük Ders Sentezi
Adımlar: 91 - 100
Checkpoint: Adım 100 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # ADIM 91
    slides.append({
        "slideNumber": 91,
        "title": "Metastatik Kalsifikasyon Tanımı ve Hiperkalseminin Yansımaları",
        "subtitle": "Kalsiyum-fosfat çözünürlük çarpımının aşılması ve normal dokularda sistemik çöküş",
        "badge": "Metastatik Tanım",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Metastatik kalsifikasyon, serum kalsiyum düzeyinin belirgin şekilde yükseldiği (hiperkalsemi) veya nadiren "
            "aşırı hiperfosfatemi durumlarında, önceden tamamen sağlıklı ve hasarsız olan 'normal dokularda' meydana gelen "
            "kalsiyum tuzu çökelmesidir. 'Metastatik' sözcüğü kanser metastazı anlamına gelmez; kalsiyumun kanda "
            "taşınarak normal dokulara sistemik olarak yayılmasını ifade eder.\n\n"
            "> [TEMEL İLKE] Serum [Kalsiyum] × [Fosfat] iyon çarpımı kritik çözünürlük eşiğini (genellikle > 55-60 mg2/dL2) "
            "aştığında kalsiyum tuzları kanda çözünür kalamaz ve dokulara kristaller halinde çöker.\n\n"
            "Bu durum distrofik formun aksine lokalize değil, vücudun pek çok organında aynı anda diffüz olarak gelişir."
        ),
        "medicalTerms": [
            {"term": "Metastatik Kalsifikasyon", "explanation": "Hiperkalsemi nedeniyle önceden normal olan yumuşak dokularda sistemik kalsiyum fosfat çökmesidir."},
            {"term": "Ca × P İyon Çarpımı", "explanation": "Kalsiyum ve fosfatın kanda çözünürlük sınırını gösteren, 55-60'ı aştığında çökelme başlatan çarpımdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Metastatik kalsifikasyon daima hiperkalsemi ile birliktedir.",
            "📌 [SINAV SPOTU] Birikim hasarlı dokuda değil, önceden tamamen normal dokularda meydana gelir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Biyokimyasal Zemin", "desc": "Yüksek serum kalsiyumu ve aşılmış Ca × P çözünürlük çarpımı.", "isKey": True},
                {"title": "Doku Karakteri", "desc": "Önceden tamamen normal ve canlı yumuşak dokular.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Serum kalsiyumunun yüksek olduğu hiperkalsemi zemininde normal dokularda gelişen patolojik mineralizasyona metastatik kalsifikasyon denir.",
                "metastatik kalsifikasyon",
                "Hiperkalsemi kaynaklı yaygın doku kalsifikasyonunun adı"
            ),
            make_active_recall(
                "Metastatik kalsifikasyonda 'metastatik' terimi ne anlama gelir?",
                "Malign bir tümörün yayılmasını değil; kalsiyum iyonlarının dolaşım yoluyla taşınarak vücuttaki pek çok normal dokuya sistemik olarak çökmesini ifade eder."
            )
        ]
    })

    # ADIM 92
    slides.append({
        "slideNumber": 92,
        "title": "Etiyoloji 1: Primer Hiperparatiroidizm ve Paratiroid Adenomu",
        "subtitle": "Aşırı PTH salgısı, osteoklastik kemik rezorpsiyonu ve renal kalsiyum geri emilimi",
        "badge": "Primer Hiperparatiroidizm",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Metastatik kalsifikasyonun en sık endokrin nedenlerinden biri primer hiperparatiroidizmdir. Olguların "
            "%85-90'ından tek bir iyi huylu 'paratiroid adenomu', geri kalanından ise paratiroid hiperplazisi veya "
            "karsinomu sorumludur. Paratiroid bezlerinden aşırı ve kontrolsüz parathormon (PTH) salgılanır.\n\n"
            "> [SINAV SPOTU] Yüksek PTH üç koldan hiperkalsemi yapar: 1) Kemiklerde osteoklastları uyararak masif "
            "kalsiyum ve fosfat rezorpsiyonu, 2) Böbrek distal tübüllerinden aktif kalsiyum geri emilimi, 3) 1α-hidroksilazı "
            "aktive ederek 1,25-(OH)2D vitamini sentezini artırmak ve bağırsaktan kalsiyum emilimini katlamak.\n\n"
            "Kandaki devasa kalsiyum yükü metastatik kalsifikasyon için zemin hazırlar."
        ),
        "medicalTerms": [
            {"term": "Primer Hiperparatiroidizm", "explanation": "Paratiroid adenomu veya hiperplazisine bağlı kontrolsüz otonom PTH salgılanması tablosudur."},
            {"term": "Parathormon (PTH)", "explanation": "Serum kalsiyumunu yükseltmek üzere kemik, böbrek ve bağırsak üzerine etkiyen ana hormondur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Primer hiperparatiroidizmin en sık nedeni paratiroid adenomudur.",
            "📌 [SINAV SPOTU] PTH osteoklastik rezorpsiyonu artırarak kemikten kana kalsiyum boşaltır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Adenom Etkisi", "desc": "Geri bildirimsiz monoklonal aşırı PTH salgısı.", "isKey": True},
                {"title": "Üçlü Mekanizma", "desc": "Kemik erimesi + böbrekten geri emilim + bağırsaktan D vitamini aracılı emilim.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Primer Hiperparatiroidizmde Hiperkalsemi Zinciri",
                [
                    "1. Paratiroid Adenomu: Paratiroid baş hücreleri otonom olarak kontrolsüz PTH salgılar.",
                    "2. Osteoklast Aktivasyonu: Yüksek PTH RANKL üzerinden kemik matriksini eritir; kana Ca2+ akar.",
                    "3. Renal Hidroksilasyon: Böbrekte D vitamini aktif 1,25-(OH)2D3 formuna çevrilir.",
                    "4. Bağırsak Emilimi: Kalsitriyol bağırsak kalsiyum emilimini maksimuma çıkarır.",
                    "5. Metastatik Çökelme: Kanda yükselen kalsiyum normal dokularda metastatik kalsifikasyonu başlatır."
                ]
            ),
            make_cloze(
                "Primer hiperparatiroidizmin en sık etiyolojik nedeni paratiroid bezinde gelişen tek bir iyi huylu paratiroid adenomu lezyonudur.",
                "paratiroid adenomu",
                "Otonom PTH salgılayan benign paratiroid tümörü"
            )
        ]
    })

    # ADIM 93
    slides.append({
        "slideNumber": 93,
        "title": "Etiyoloji 2: Sekonder Hiperparatiroidizm ve Kronik Böbrek Yetmezliği",
        "subtitle": "Fosfat retansiyonu, kalsitriol sentez çöküşü ve reaktif paratiroid hiperplazisi",
        "badge": "KBY ve Sekonder HPT",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Kronik böbrek yetmezliği (KBY), metastatik kalsifikasyonun en ağır ve en karmaşık görüldüğü klinik tablodur. "
            "Böbrek nefronları azaldığında idrarla fosfat atılamaz ve kanda 'fosfat retansiyonu' (hiperfosfatemi) başlar. "
            "Ayrıca işlevsel parankim kaybı nedeniyle 1α-hidroksilaz enzimi çalışamaz ve aktif D vitamini (kalsitriol) sentezlenemez.\n\n"
            "> [SINAV SPOTU] Kalsitriol eksikliği ve hiperfosfatemi kanda kalsiyumu düşürür; kronik hipokalsemi paratiroid "
            "bezlerini çılgınca uyararak 4 bezde birden 'sekonder hiperparatiroidizm' (diffüz hiperplazi) başlatır.\n\n"
            "PTH kemikleri eriterek kalsiyumu yükseltir; yüksek kalsiyum ile yüksek fosfatın çarpımı (Ca × P) tavan "
            "yapar ve masif metastatik doku kalsifikasyonları patlak verir."
        ),
        "medicalTerms": [
            {"term": "Sekonder Hiperparatiroidizm", "explanation": "KBY'de kronik hipokalsemi ve hiperfosfatemiye reaktif olarak paratiroidlerin hiperplaziye uğramasıdır."},
            {"term": "Fosfat Retansiyonu", "explanation": "Böbrek süzme fonksiyonu çöktüğünde kanda fosfor iyonlarının birikmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] KBY'de sekonder hiperparatiroidizmi başlatan primer olay fosfat retansiyonu ve hipokalsemidir.",
            "📌 [SINAV SPOTU] Ca × P iyon çarpımının aşırı artması yaygın metastatik kalsifikasyona yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Fosfat Birikimi", "desc": "Glomerüler filtrasyon düşünce serum fosfatı yükselir.", "isKey": True},
                {"title": "Reaktif Hiperplazi", "desc": "Tüm paratiroid bezleri sürekli PTH salgılayarak kemikleri eritir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Özellik", "Primer Hiperparatiroidizm", "Sekonder Hiperparatiroidizm (KBY)"],
                [
                    [("Temel Neden", False, ""), ("Paratiroid Adenomu", False, ""), ("Kronik Böbrek Yetmezliği", True, "Fosfat atılamaması ve kalsitriol yokluğu")],
                    [("Serum Kalsiyumu", False, ""), ("Yüksek (Hiperkalsemi)", False, ""), ("Düşük veya Normale Yakın", True, "Kronik hipokalsemik uyarı zemininde")],
                    [("Serum Fosfatı", False, ""), ("Düşük (PTH fosfat atar)", False, ""), ("Çok Yüksek (Böbrek atamaz)", True, "Fosfat retansiyonu tablosu")],
                    [("Paratiroid Morfolojisi", False, ""), ("Tek bezde adenom (%85)", False, ""), ("4 bezde birden hiperplazi", True, "Sistemik hipokalsemiye reaktif büyüme")]
                ]
            ),
            make_cloze(
                "Kronik böbrek yetmezliğinde sekonder hiperparatiroidizmi tetikleyen en temel mekanizma kanda fosfat retansiyonu gelişmesidir.",
                "fosfat retansiyonu",
                "Böbrek yetmezliğinde fosforun atılamayıp kanda birikmesi"
            )
        ]
    })

    # ADIM 94
    slides.append({
        "slideNumber": 94,
        "title": "Etiyoloji 3: Kemik Rezorpsiyonunun Arttığı Durumlar",
        "subtitle": "Kemik metastazları, multipl miyelom osteolizi ve Paget hastalığının hiperkalsemisi",
        "badge": "Kemik Rezorpsiyonu",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Kemik dokusunun hızlanmış yıkımı (osteoliz), kana devasa miktarda kalsiyum tuzlarının salınmasına neden "
            "olarak metastatik kalsifikasyonu tetikleyen üçüncü ana etiyolojidir. En tehlikeli grup ileri evre malign "
            "tümörlerin kemik metastazlarıdır (özellikle meme, akciğer, prostat ve böbrek kanserleri).\n\n"
            "> [SINAV SPOTU] Multipl miyelomda plazma hücreleri osteoklast aktive edici faktörler (RANKL, IL-1, TNF) "
            "salgılayarak kemikte zımba deliği (punched-out) litik lezyonlar açar ve masif hiperkalsemi yaratır.\n\n"
            "İmmobilizasyon (uzun süre yatağa bağımlı kalma) ve ileri evre kemik Paget hastalığında da kemik turnoverı "
            "artarak kana kalsiyum boşalmasına yol açabilir."
        ),
        "medicalTerms": [
            {"term": "Osteolitik Metastaz", "explanation": "Tümör hücrelerinin lokal sitokinlerle kemik dokusunu eritip kalsiyumu kana salmasıdır."},
            {"term": "Punched-Out Lezyon", "explanation": "Multipl miyelomda kemikte görülen zımba deliği biçimli litik kemik defektleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kemik metastazları ve multipl miyelom litik kemik yıkımıyla hiperkalsemi yapar.",
            "📌 [SINAV SPOTU] Miyelomda osteoklast aktive edici sitokinler kemiği zımba deliği gibi eritir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Malign Litik Yıkım", "desc": "Meme/akciğer metastazları ve miyelom osteolizi.", "isKey": True},
                {"title": "İmmobilizasyon", "desc": "Mekanik yük kalktığında kemikten kalsiyumun çözünmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Kemik ağrıları ve anemi şikayeti olan bir hastanın kafa grafisinde zımba deliği (punched-out) litik lezyonlar, kanda aşırı hiperkalsemi saptanıyor. Kemik iliğinde malign plazma hücre infiltrasyonu izleniyor. Bu hastada hiperkalsemiye ve metastatik kalsifikasyona yol açan temel mekanizma hangisidir?",
                {
                    "A": "Paratiroid adenomundan kontrolsüz kalsitonin salgılanması",
                    "B": "Plazma hücrelerinin osteoklastik kemik rezorpsiyonunu aşırı uyarması",
                    "C": "Akciğer makrofajlarında D vitamini inaktivasyonu",
                    "D": "Karaciğerde albümin sentezinin tamamen durması",
                    "E": "Tübüllerde kalsiyum taşıyıcılarının mutasyonu"
                },
                "B",
                {
                    "A": "Kalsitonin kalsiyumu düşürür, yükseltmez.",
                    "B": "Doğru! Multipl miyelomda sitokinler osteoklastları aktive ederek kemiği eritir ve hiperkalsemi yapar.",
                    "C": "Sarkoidozda D vitamini aktive olur, inaktive olmaz.",
                    "D": "Albümin kaybı iyonize kalsiyumu artırmaz.",
                    "E": "Taşıyıcı mutasyonu primer kemik litik lezyonunu açıklamaz."
                }
            ),
            make_cloze(
                "Multipl miyelomda malign plazma hücreleri osteoklast aktive edici sitokinler salgılayarak kemikte osteolitik lezyonlar ve hiperkalsemi oluşturur.",
                "osteolitik",
                "Kemiği eriterek kana kalsiyum salan litik yıkım süreci"
            )
        ]
    })

    # ADIM 95
    slides.append({
        "slideNumber": 95,
        "title": "Etiyoloji 4: D Vitamini İntoksikasyonu ve Sarkoidozda Aktivasyon",
        "subtitle": "1α-hidroksilaz ekspresyonu, epiteloid histiositler ve kontrolsüz kalsitriyol üretimi",
        "badge": "D Vitamini ve Sarkoidoz",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Metastatik kalsifikasyonun dördüncü temel nedeni D vitamini ilişkili hiperkalsemidir. Bu durum ya yüksek "
            "dozda D vitamini takviyesi alınmasıyla (D vitamini intoksikasyonu) ya da granülomatöz hastalıklarda endojen "
            "kontrolsüz D vitamini aktivasyonuyla meydana gelir.\n\n"
            "> [SINAV SPOTU] Sarkoidoz, tüberküloz ve berilyozis gibi granülomatöz hastalıklarda granülomu oluşturan "
            "aktive epiteloid makrofajlar kontrolsüz şekilde 1α-hidroksilaz enzimi eksprese eder.\n\n"
            "Makrofaj kaynaklı bu enzim PTH kontrolünden tamamen bağımsızdır; öncül D vitaminini aktif 1,25-(OH)2D3 "
            "(kalsitriyol) formuna çevirir. Aşırı kalsitriyol bağırsaktan masif kalsiyum emilimi yaptırarak hiperkalsemiye "
            "ve metastatik doku kalsifikasyonuna neden olur."
        ),
        "medicalTerms": [
            {"term": "1α-Hidroksilaz", "explanation": "25-OH D vitaminini en aktif form olan 1,25-(OH)2D3 kalsitriyole çeviren enzimdir."},
            {"term": "Sarkoidoz", "explanation": "Kazeifiye olmayan granülomlarla seyreden, makrofajların D vitamini ürettiği sistemik hastalıktır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sarkoidozda granülom makrofajları kontrolsüz 1α-hidroksilaz salgılayarak hiperkalsemi yapar.",
            "📌 [SINAV SPOTU] Bu aktivasyon PTH denetiminden tamamen bağımsız otonom bir enzim çalışmasıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Ekzojen Toksisite", "desc": "Aşırı D vitamini desteğiyle bağırsaktan sınırsız Ca emilimi.", "isKey": True},
                {"title": "Granülomatöz Sentez", "desc": "Sarkoidoz makrofajlarının PTH'sız 1α-hidroksilaz üretimi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Sarkoidozda Hiperkalsemi ve Kalsifikasyon Mekanizması",
                [
                    "1. Kazeifiye Olmayan Granülom: Akciğer ve lenf nodlarında aktive epiteloid makrofajlar toplanır.",
                    "2. 1α-Hidroksilaz Salgısı: Makrofajlar PTH'dan bağımsız olarak 1α-hidroksilaz üretir.",
                    "3. Kalsitriyol Sentezi: Kanda 1,25-(OH)2D3 seviyesi belirgin şekilde yükselir.",
                    "4. Bağırsak Ca Emilimi: Enterositlerden kana aşırı kalsiyum çekilerek hiperkalsemi gelişir.",
                    "5. Metastatik Kalsifikasyon: Hiperkalsemi böbrek, mide ve akciğer parankiminde kireçlenme yapar."
                ]
            ),
            make_cloze(
                "Sarkoidoz granülomlarındaki epiteloid makrofajlar 1α-hidroksilaz enzimi sentezleyerek kontrolsüz D vitamini aktivasyonu yapar.",
                "1α-hidroksilaz",
                "D vitaminini aktif kalsitriyole çeviren makrofaj enzimi"
            )
        ]
    })

    # ADIM 96
    slides.append({
        "slideNumber": 96,
        "title": "Hedef Organlar: Neden Mide, Akciğer ve Böbrek? (Asit Salınımı ve Alkaloz)",
        "subtitle": "İçsel doku alkalinitesi, hidrojen iyonu kaybı ve kalsiyum tuzu çökelme eğilimi",
        "badge": "Hedef Organ Mantığı",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Metastatik kalsifikasyon vücuttaki herhangi bir dokuda görülebilmekle birlikte, belirgin bir organ seçiciliği "
            "gösterir. En sık ve en erken tutulan organlar: 1) Mide mukozası, 2) Akciğer alveol septaları, 3) Böbrek "
            "tübül epiteli ve bazal membranları, 4) Sistemik arter duvarlarıdır.\n\n"
            "> [SINAV SPOTU] Bu organların ortak fizyolojik sırrı 'asit salgılamaları'dır. Mide HCl salgılar, böbrek H+ "
            "iyonunu idrara atar, akciğer CO2 (karbonik asit) gazını dışarı üfler. Asit dışarı atıldığında hücre içi ve "
            "lokal çevre dokuda geçici bir 'alkaloz' (yüksek pH) meydana gelir.\n\n"
            "Kalsiyum fosfat tuzları alkali pH ortamında çok daha düşük konsantrasyonlarda hızla kristalleşip çöker."
        ),
        "medicalTerms": [
            {"term": "Doku Alkalinitesi", "explanation": "Asit salgılayan hücrelerin çevresinde pH'ın bazik yöne kayması ve kalsiyum çökmesini kolaylaştırmasıdır."},
            {"term": "Organ Seçiciliği", "explanation": "Metastatik kalsifikasyonun lokal pH nedeniyle mide, akciğer ve böbreği hedeflemesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Metastatik kalsifikasyon asit salgılayan organlarda (mide, böbrek, akciğer) en sıktır.",
            "📌 [SINAV SPOTU] Asit kaybı lokal dokuyu alkali yapar; alkali pH kalsiyum tuzlarının çökmesini hızlandırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mide Mukozası", "desc": "Lümene HCl atar; fundus ve korpus mukozasında kalsifikasyon.", "isKey": True},
                {"title": "Böbrek Tübülü", "desc": "İdrara H+ pompalar; tübül bazal membranında kireçlenme (nefrokalsinoz).", "isKey": True},
                {"title": "Akciğer Septumu", "desc": "CO2 solur; alveol kapiller duvarlarında diffüz kalsiyum bantları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Metastatik kalsifikasyonun sistemik hiperkalsemi varlığında özellikle mide mukozası, böbrek tübülleri ve akciğer alveol septalarında yoğunlaşmasının temel fizyopatolojik gerekçesi aşağıdakilerden hangisidir?",
                {
                    "A": "Bu organların endotelinde aşırı miktarda apoferritin bulunması",
                    "B": "Bu dokuların asit salgılayarak lokal mikroçevrede geçici alkaloz oluşturması ve kalsiyum çökmesini kolaylaştırması",
                    "C": "Bu organlarda lizozomal asit lipaz enziminin genetik olarak eksik olması",
                    "D": "Bu dokularda oksijen parsiyel basıncının sıfıra yakın olması",
                    "E": "Bu organların parankiminde sadece koagülatif nekroz gelişmesi"
                },
                "B",
                {
                    "A": "Apoferritin demir bağlar, kalsiyumla ilgisi yoktur.",
                    "B": "Doğru! Asit kaybı (HCl, H+, CO2) dokuda lokal alkaloz yaratır ve kalsiyum fosfat alkali ortamda hızla çöker.",
                    "C": "Asit lipaz Wolman hastalığıyla ilgilidir.",
                    "D": "Akciğer ve böbrek oksijenden zengindir.",
                    "E": "Metastatik kalsifikasyon nekroz olmadan normal dokularda gelişir."
                }
            ),
            make_cloze(
                "Metastatik kalsifikasyonun mide, böbrek ve akciğeri tercih etmesinin nedeni bu dokuların asit atarak lokal alkaloz oluşturmasıdır.",
                "alkaloz",
                "Kalsiyum fosfat tuzlarının kristalleşmesini kolaylaştıran bazik pH ortamı"
            )
        ]
    })

    # ADIM 97
    slides.append({
        "slideNumber": 97,
        "title": "Nefrokalsinoz ve Pulmoner Kalsifikasyonun Komplikasyonları",
        "subtitle": "Tübülointerstisyel kalsiyum silindirleri, böbrek yetmezliği ve restriktif akciğer hastalığı",
        "badge": "Klinik Komplikasyonlar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Metastatik kalsifikasyon başlangıçta asemptomatik olsa da, hedef organlarda ilerlediğinde hayatı tehdit eden "
            "organ disfonksiyonlarına yol açar. Böbreklerde tübül epitelinde ve bazal membranında kalsiyum çökmesi "
            "'nefrokalsinoz' (nephrocalcinosis) olarak adlandırılır. Kalsiyum tübül lümenlerini tıkar, konsantrasyon "
            "yeteneğini bozar (poliüri, polidipsi) ve zamanla tübülointerstisyel nefrit ve kronik böbrek yetmezliğine ilerler.\n\n"
            "> [KLİNİK İPUCU] Akciğerde alveol septalarındaki kalsiyum depolanması elastikiyeti yok eder; gaz difüzyonunu "
            "engeller, restriktif akciğer hastalığı ve solunum yetmezliğine neden olur.\n\n"
            "Mide mukozasındaki kalsifikasyon ise masif kanamalara zemin hazırlayabilir."
        ),
        "medicalTerms": [
            {"term": "Nefrokalsinoz", "explanation": "Böbrek parankiminde, tübüllerinde ve interstisyumunda yaygın kalsiyum tuzu çökelmesidir."},
            {"term": "Restriktif Akciğer Patolojisi", "explanation": "Alveol duvarlarının kalsiyumla sertleşmesi sonucu akciğer ekspansiyonunun kısıtlanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nefrokalsinoz metastatik kalsifikasyonun böbrekteki en ağır tablosudur.",
            "📌 [SINAV SPOTU] Akciğerde metastatik kalsifikasyon restriktif solunum bozukluğuna yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Böbrek Hasarı", "desc": "Nefrokalsinoz, taş oluşumu, konsantrasyon defekti, üremi.", "isKey": True},
                {"title": "Akciğer Hasarı", "desc": "Alveoler sertleşme, hipoksemi, difüzyon kapasitesi kaybı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Nefrolitiyazis vs Nefrokalsinoz",
                "Nefrolitiyazis (Böbrek Taşı)",
                "Kalsiyum tuzlarının toplayıcı sistemde (pelvis, kaliks) lümen içi taş odakları oluşturması ve kolik ağrı yapmasıdır.",
                "Nefrokalsinoz (Parankimal Kireçlenme)",
                "Kalsiyumun doğrudan böbrek parankimi, tübül epitel hücreleri ve interstisyel bağ dokusu içine diffüz çökmesidir."
            ),
            make_active_recall(
                "Metastatik kalsifikasyon zemininde gelişen nefrokalsinozun böbrek fonksiyonları üzerindeki en kritik iki yıkıcı etkisi nedir?",
                "Tübüler konsantrasyon yeteneğini bozarak poliüriye yol açması ve ilerleyici tübülointerstisyel fibrozisle kronik böbrek yetmezliği oluşturmasıdır."
            )
        ]
    })

    # ADIM 98
    slides.append({
        "slideNumber": 98,
        "title": "Kalsifilaksi (Kalsifik Üremik Arteriyolopati): Küçük Damar Nekrozu",
        "subtitle": "Son dönem böbrek yetmezliğinde arteriyol kalsifikasyonu, trombüs ve iskemik deri ülserleri",
        "badge": "Kalsifilaksi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Kalsifilaksi veya resmi adıyla 'kalsifik üremik arteriyolopati', hemodiyaliz alan son dönem böbrek yetmezliği "
            "(SDBY) hastalarında görülen nadir fakat son derece ölümcül (%50'den yüksek mortalite) bir kalsifikasyon tablosudur. "
            "Aşırı yüksek kalsiyum-fosfat çarpımı ve sekonder/tersiyer hiperparatiroidizm zemininde gelişir.\n\n"
            "> [KRİTİK UYARI] Dermis ve subkutan yağ dokusundaki küçük arter ve arteriyollerin tunika media tabakasında "
            "masif kalsifikasyon ve intimal hiperplazi meydana gelir.\n\n"
            "Damarlar kireçle tıkanır ve lümende trombüs oluşur; deride son derece ağrılı, mor-siyah iskemik purpura, büller "
            "ve tedaviye dirençli nekrotik gangrenöz ülserler açılır. Sepsis en sık ölüm nedenidir."
        ),
        "medicalTerms": [
            {"term": "Kalsifilaksi", "explanation": "Üremik hastalarda küçük damarların kalsifiye olup tıkanmasıyla giden iskemik doku nekrozu sendromudur."},
            {"term": "Arteriyol Kalsifikasyonu", "explanation": "Deri altı küçük arterlerin mediasında hidroksiapatit kireçlenmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Kalsifilaksi diyaliz hastalarında küçük damar kalsifikasyonu ve iskemik deri nekrozudur.",
            "📌 [SINAV SPOTU] Ağrılı ülserler, gangren ve yüksek sepsis mortalitesi ile seyreder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hasta Grubu", "desc": "Son dönem böbrek yetmezliği ve hemodiyaliz hastaları.", "isKey": True},
                {"title": "Damar Patolojisi", "desc": "Subkutan arteriyollerin mediasında kalsifikasyon ve mikrotromboz.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hemodiyaliz hastalarında küçük damarların kalsifikasyonu ve deri nekrozuyla seyreden ölümcül tabloya kalsifilaksi denir.",
                "kalsifilaksi",
                "Kalsifik üremik arteriyolopatinin klinik adı"
            ),
            make_active_recall(
                "Kalsifilaksi patolojisinde iskemik deri nekrozuna ve gangrenöz ülserlere yol açan temel vasküler değişiklik nedir?",
                "Subkutanöz küçük arter ve arteriyollerin tunika mediasında kalsiyum çökelmesi, intimal proliferasyon ve sekonder tromboz gelişmesidir."
            )
        ]
    })

    # ADIM 99
    slides.append({
        "slideNumber": 99,
        "title": "Hücresel Yaşlanma ve Hücre İçi Birikimlerin Entegrasyonu",
        "subtitle": "DNA hasarı birikimi, telomer kısalması, proteostaz çöküşü ve lipofusin kilitlenmesi",
        "badge": "Yaşlanma Entegrasyonu",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Ders 7 boyunca incelediğimiz tüm hücre içi ve hücre dışı birikimler, organizmanın kronolojik ve hücresel "
            "yaşlanma süreciyle iç içe geçer. Yaşlanma ilerledikçe hücrelerin replikatif kapasitesi (telomer tükenmesi "
            "nedeniyle Hayflick sınırı) tükenir, nükleer ve mitokondriyal DNA hasarları birikir ve proteazom/şaperon "
            "sistemlerinin fonksiyonel rezervi düşer.\n\n"
            "> [YÜKSEK VERİM] Bu durum lipofusin birikimini hızlandırır, hatalı katlanan proteinlerin temizlenmesini "
            "önler, damar duvarlarında ateroskleroz ve distrofik kalsifikasyonu katlar.\n\n"
            "Birikintiler yaşlanmanın hem kaçınılmaz birer biyolojik ürünü hem de organ yetmezliklerini hızlandıran "
            "patolojik tetikleyicileridir."
        ),
        "medicalTerms": [
            {"term": "Hücresel Yaşlanma (Senesens)", "explanation": "Hücrenin kalıcı olarak bölünme döngüsünden çıkması ve sekresyon profilinin değişmesidir."},
            {"term": "Proteostaz Kaybı", "explanation": "Yaşlanmayla birlikte protein sentez, katlanma ve yıkım dengesinin bozulmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yaşlanmada DNA hasarı, protein kontrol kaybı ve lipofusin birikimi el ele gider.",
            "📌 [SINAV SPOTU] Yaşlı kardiyomiyositlerde lipofusin, damarlarda kalsiyum birikimi kaçınılmazdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yaşlanma Triadı", "desc": "DNA mutasyonları + Telomer kaybı + Proteostaz iflası.", "isKey": True},
                {"title": "Doku İmzaları", "desc": "Lipofusin granülleri, kapak sertleşmesi, amyloid birikimi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Genç Hücre vs Yaşlanmış (Senesent) Hücre",
                "Genç Hücre",
                "Yüksek proteazom aktivitesi, sağlam şaperon kapasitesi, sıfır lipofusin granülü ve yüksek replikatif rezerv.",
                "Yaşlanmış Hücre (Senesent)",
                "Düşmüş proteostaz kapasitesi, perinükleer lipofusin agregatları, kısalarak tükenmiş telomerler ve distrofik kireçlenme eğilimi."
            ),
            make_active_recall(
                "Hücresel yaşlanma sürecinde hücre içi birikintilerin artmasına zemin hazırlayan temel proteomik bozukluk nedir?",
                "Şaperonların ve ubikitin-proteazom sisteminin kapasitesinin azalması (proteostaz kaybı) sonucu hasarlı ve yanlış katlanmış proteinlerin yıkılamamasıdır."
            )
        ]
    })

    # ADIM 100 - CHECKPOINT 10
    slides.append({
        "slideNumber": 100,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Metastatik Kalsifikasyon ve Büyük Kurul Sentezi",
        "subtitle": "Tüm dersin 4 mekanizması, lipid, protein, glikojen, pigment ve kalsifikasyon sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 10,
        "synthesisNarrative": (
            "Ders 7'nin bu büyük final tekrar sayfasında tüm kurulun hücresel birikim haritasını mühürlüyoruz. "
            "1) 4 Birikim Mekanizması: Yetersiz uzaklaştırma (steatoz), Anormal protein (AAT), Eksojen partikül (karbon), "
            "Lizozomal enzim eksikliği (LSD). 2) Lipidler: Steatoz (KC, kalp-kaplan derisi), Kolesterol (köpük hücre, "
            "aterom plağı, Aşil tendon ksantomu, çilek safra kesesi). 3) Proteinler: Tübüler damlacık (reversibl), "
            "Russell/Dutcher cisimcikleri (GER/nükleus), Mallory-Denk (sitokeratin 8/18). 4) Yanlış Katlanma: CFTR (erken yıkım), "
            "Prion (beta dönüşüm), AAT (KC'de siroz, AC'de amfizem). 5) Glikojen: PAS(+)/diyastaz duyarlı, Armanni-Ebstein, "
            "Von Gierke (G6Paz), Pompe (asit maltaz-kalp), McArdle (kas fosforilaz). 6) Pigmentler: Karbon (antrakozis), "
            "Lipofusin (altın-kahve yaşlılık), Melanin (tirozinaz), Hemosiderin (Prusya mavisi). 7) Kalsifikasyon: "
            "Distrofik (Ca normal, nekrotik doku, mitokondri nükleasyonu) vs Metastatik (Hiperkalsemi, normal doku, mide/böbrek/AC).\n\n"
            "> [KLİNİK İPUCU] Bu 100 adımlık anatomik ve patofizyolojik yolculuk sınavdaki tüm vaka ve mekanizma sorularını çözdürür.\n\n"
            "Finaldeki 3 akıl kartını hafızanıza sabitleyerek dersi mükemmeliyetle tamamlayınız."
        ),
        "medicalTerms": [
            {"term": "Hücre İçi Birikimler", "explanation": "Metabolizma veya genetik aksaklıkla hücrede madde toplanmasıdır."},
            {"term": "Patolojik Kalsifikasyon", "explanation": "Yumuşak dokularda distrofik veya metastatik kalsiyum çökelmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Distrofik kalsifikasyonda Ca normal; metastatikte Ca daima yüksektir.",
            "📌 [SINAV SPOTU] Prusya mavisi = Demir; PAS/diyastaz = Glikojen; Fontana-Masson = Melanin.",
            "📌 [SINAV SPOTU] Aşil ksantomu = LDLR; Kalsifiye kapak = Distrofik; Kalsifilaksi = SDBY damar kalsifikasyonu."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mekanizma Dörtlüsü", "desc": "Yetersiz klirens, mutant protein, eksojen partikül, hidrolaz yokluğu.", "isKey": True},
                {"title": "Biyokimyasal İmzalar", "desc": "Trigliserid, kolesterol, sitokeratin, glikojen, lipofusin, hemosiderin.", "isKey": True},
                {"title": "Kalsifikasyon İkilisi", "desc": "Distrofik (normokalsemi/nekroz) vs Metastatik (hiperkalsemi/normal doku).", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-28",
                "Metastatik kalsifikasyona yol açan 4 temel klinik etiyoloji grubu nelerdir?",
                "1) Primer hiperparatiroidizm, 2) Kronik böbrek yetmezliğine bağlı sekonder hiperparatiroidizm, 3) Kemik rezorpsiyonunu artıran durumlar (kemik metastazları, miyelom), 4) D vitamini intoksikasyonu ve sarkoidoz.",
                "Metastatik kalsifikasyonun 4 temel etiyolojik nedeni"
            ),
            make_flashcard(
                "k1-07-fc-29",
                "Metastatik kalsifikasyonun özellikle mide mukozası, böbrek tübülleri ve akciğer alveol septalarını tutmasının gerekçesi nedir?",
                "Bu organların asit (HCl, H+, CO2) salgılayarak kendi lokal doku mikroçevrelerinde geçici bir alkaloz oluşturması ve alkali pH'ın kalsiyum fosfat kristalizasyonunu kolaylaştırmasıdır.",
                "Metastatik kalsifikasyonda organ seçiciliği ve lokal alkaloz"
            ),
            make_flashcard(
                "k1-07-fc-30",
                "Kalsifilaksi (kalsifik üremik arteriyolopati) hangi hasta grubunda görülür ve temel lezyonu nedir?",
                "Son dönem böbrek yetmezliği nedeniyle hemodiyaliz alan hastalarda görülür; subkutan küçük arter ve arteriyollerin kalsifiye olup tıkanmasıyla çok ağrılı iskemik deri nekrozları ve gangrenöz ülserler oluşturur.",
                "Diyaliz hastalarında kalsifilaksi patolojisi ve damar tutulumu"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Metastatik kalsifikasyonda asit kaybı sonucu oluşan doku alkalinitesi kalsiyum tuzlarının kristalleşmesini kolaylaştırır.",
                "kalsiyum tuzlarının",
                "Dokuda hidroksiapatit kristalleri oluşturan mineral bileşenleri"
            )
        ]
    })

    return slides
