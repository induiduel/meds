# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 2: Mendel Kalıtımı ve Marfan Sendromu (Slayt 11-20)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_2_slides():
    slides = []

    # Slayt 11: Mendel Tipi Tek Gen Hastalıklarına Genel Bakış
    slides.append({
        "id": "k1-26-s11",
        "title": "Mendel Tipi Tek Gen Hastalıklarına Genel Bakış",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 11,
        "narrative": (
            "Mendel tipi hastalıklar, nükleer DNA'daki tek bir gendeki mutasyonun belirleyici olduğu kalıtsal tablolardır: "
            "1. **Yüksek Penetrans:** Tek gen bozuklukları genellikle çevre faktörlerinden bağımsız olarak yüksek penetrans "
            "gösterir ve aile ağacında (pedigri) karakteristik kalıtım örüntüleri sergiler. "
            "2. **Penetrans ve Değişken Ekspresyon:** "
            "- **Penetrans:** Mutant aleli taşıyan bireylerin yüzde kaçında klinik hastalığın ortaya çıktığıdır (Örn: %80 penetrans, "
            "mutasyonu taşıyan 10 kişiden 8'inin hasta olmasıdır). "
            "- **Değişken Ekspresyon (Expressivity):** Aynı mutasyonu taşıyan bireyler arasında klinik şiddetin ve tutulan organ "
            "dağılımının farklılık göstermesidir (Örn: Bir ailede Marfan hastası bir bireyde sadece uzun parmaklar varken, kardeşinde letal aort diseksiyonu gelişmesi). "
            "3. **Pleiotropizm:** Tek bir gen defektinin vücutta birden fazla organ sisteminde tamamen farklı ikincil etkilere yol açmasıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Genetik Terminoloji ve Klinik Anlamları",
                ["Genetik Terim", "Moleküler / Epistemolojik Tanım", "Klinik Örnek"],
                [
                    ["Penetrans (İşleme)", "Mutant genotipin fenotipe yansıma yüzdesi", "%100 penetran Huntington, eksik penetran BRCA1"],
                    ["Değişken Ekspresyon", "Aynı genotipe sahip bireylerde şiddet farkı", "Nörofibromatozis Tip 1'de hafif lekeler vs dev nörofibromlar"],
                    [
                        "Pleiotropizm",
                        {"text": "Tek gen defektinin çok sayıda farklı organ sistemini etkilemesi", "isMasked": True, "hint": "Tek bir mutasyonun iskelet, göz ve kardiyovasküler sistemde eşzamanlı patoloji yapması"},
                        "Marfan sendromu (iskelet, göz merceği ve aort duvarı)"
                    ]
                ]
            ),
            make_active_recall(
                "Tek bir genetik mutasyonun vücutta birbiriyle ilgisiz görünen birden fazla doku ve organ sisteminde klinik bulgular oluşturması fenomenine ne ad verilir?",
                "Pleiotropizmdir (pleiotropik etki).",
                "Marfan sendromunda tek bir FBN1 geninin göz, kemik ve damarları eşzamanlı vurması durumu"
            )
        ]
    })

    # Slayt 12: Otozomal Dominant Kalıtımın İlkeleri
    slides.append({
        "id": "k1-26-s12",
        "title": "Otozomal Dominant Kalıtımın İlkeleri",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 12,
        "narrative": (
            "Otozomal dominant (OD) kalıtım, klinik fenotipin tek bir mutant alel varlığında (heterozigot durumda) ortaya çıktığı tablodur: "
            "1. **Kalıtım Dinamiği:** "
            "- Etkilenen bir ebeveyn ile normal bir ebeveynin çocuklarına hastalığı aktarma riski **her gebelikte %50'dir (1/2)**. "
            "- Cinsiyet ayrımı yoktur; kız ve erkek çocuklar eşit oranda etkilenir. Dikey geçiş (kuşak atlamama) tipiktir. "
            "2. **Kodlanan Protein Tipleri:** "
            "- OD mutasyonlar genellikle **yapısal proteinleri** (kollajen, fibrillin, spektrin), hücre yüzey **reseptörlerini** "
            "(LDL reseptörü - ailesel hiperkolesterolemi) veya transkripsiyon faktörlerini etkiler. "
            "3. **Moleküler Mekanizmalar:** "
            "- **Dominant Negatif Etki:** Mutant protein yalnızca işlevsiz olmakla kalmaz, normal alelden üretilen sağlam proteinin de "
            "polimerize olmasını ve doku yapısına katılmasını bozar (Örn: Osteogenezis imperfekta kollajeni, Marfan fibrillini). "
            "- **Haployetmezlik (Haploinsufficiency):** Tek bir sağlam alelin ürettiği %50 protein miktarının normal fizyolojik işlev "
            "için yetersiz kalması durumudur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Dominant Negatif Etki vs Haployetmezlik Mekanizmaları",
                "Dominant Negatif Mekanizma",
                "Mutant protein polimerik yapıya katılarak sağlam alelden üretilen normal alt birimleri de zehirler ve multimeri bozar",
                "Haployetmezlik Mekanizması",
                "Mutant alel sıfır protein üretir; tek sağlam alelin %50'lik üretimi biyolojik eşiği aşmaya yetmez ve fonksiyon aksar"
            ),
            make_cloze(
                "Otozomal dominant hastalıklarda mutant proteinin sağlam alelden üretilen normal proteinin montajını da bozmasına dominant negatif etki denir.",
                "dominant negatif",
                "Kusurlu polipeptidin oligomerik yapıya katılarak tüm hücresel iskeleti felç etmesi mekanizması"
            )
        ]
    })

    # Slayt 13: Otozomal Resesif Kalıtımın İlkeleri
    slides.append({
        "id": "k1-26-s13",
        "title": "Otozomal Resesif Kalıtımın İlkeleri",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 13,
        "narrative": (
            "Otozomal resesif (OR) kalıtım, klinik hastalığın ancak her iki alel de mutant olduğunda (homozigot durumda) belirdiği tablodur: "
            "1. **Kalıtım Dinamiği:** "
            "- Heterozigot ebeveynler fenotipik olarak tamamen sağlıklıdır (**asemptomatik taşıyıcı**). "
            "- İki taşıyıcının her gebelikte hasta çocuk sahibi olma riski **%25 (1/4)**; taşıyıcı çocuk riski **%50**; tamamen sağlam çocuk riski **%25'tir**. "
            "- Aile ağacında yatay geçiş izlenir (kardeşler etkilenir, ebeveynler sağlıklıdır). "
            "2. **Akraba Evliliği:** Nadir resesif mutant alellerin bir araya gelme olasılığını katbekat artırır. "
            "3. **Etkilenen Protein Tipleri:** "
            "- OR hastalıkların neredeyse tamamı **enzim proteinlerindeki mutasyonlardan** kaynaklanır (doğuştan metabolizma hastalıkları, depo hastalıkları). "
            "- Fizyolojik enzim fazlalığı nedeniyle %50 enzim düzeyi normal hayata yettiğinden heterozigotlar sağlıklıdır. "
            "4. **Klinik Seyir:** OD hastalıklara kıyasla daha erken yaşta (genellikle bebeklik ve erken çocuklukta) başlar ve homojen bir seyir izler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Otozomal Dominant vs Otozomal Resesif Karşılaştırma Cetveli",
                ["Özellik", "Otozomal Dominant (OD)", "Otozomal Resesif (OR)"],
                [
                    ["Klinik Fenotip", "Heterozigotta belirir (tek mutant alel)", "Homozigotta belirir (çift mutant alel)"],
                    ["Ebeveyn Durumu", "Genellikle bir ebeveyn hastadır", "Ebeveynler asemptomatik taşıyıcıdır"],
                    ["Çocukta Risk", "Her gebelikte %50", "Her gebelikte %25 (taşıyıcı x taşıyıcı)"],
                    [
                        "Etkilenen Protein Türü",
                        "Yapısal proteinler, reseptörler",
                        {"text": "Hücresel enzimler (metabolizma bozuklukları)", "isMasked": True, "hint": "Katalitik aktivite gösteren ve %50 düzeyi taşıyıcıda yeterli olan protein sınıfı"}
                    ],
                    ["Başlangıç Yaşı", "Ergenlik veya erişkinlikte de başlayabilir", "Genellikle erken çocukluk ve bebeklik"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi otozomal resesif kalıtım gösteren genetik hastalıkların temel biyolojik ve epidemiyolojik özelliklerinden biridir?",
                {
                    "A": "Mutasyonların çoğunlukla hücresel enzim proteinlerini etkilemesi",
                    "B": "Hastalığın tek bir mutant alel varlığında doğrudan ortaya çıkması",
                    "C": "Kuşaklar boyunca dikey geçiş göstererek ebeveynlerin mutlaka hasta olması",
                    "D": "Kollajen ve spektrin gibi yapısal protein defektlerinin baskın olması",
                    "E": "Akraba evliliklerinden tamamen bağımsız bir sıklık sergilemesi"
                },
                "A",
                {
                    "A": "Doğrudur; enzim defektlerinde %50 üretim taşıyıcıyı kurtarır, hastalık ancak homozigot çift defektte patlar.",
                    "B": "Yanlış; tek alelde beliren dominant kalıtımdır.",
                    "C": "Yanlış; dikey geçiş OD kalıtıma özgüdür.",
                    "D": "Yanlış; yapısal proteinler dominant kalıtılır.",
                    "E": "Yanlış; akraba evliliği resesif sıklığını doğrudan artırır."
                }
            )
        ]
    })

    # Slayt 14: X'e Bağlı ve Atipik Kalıtım Modelleri
    slides.append({
        "id": "k1-26-s14",
        "title": "X'e Bağlı ve Atipik Kalıtım Modelleri",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 14,
        "narrative": (
            "Cinsiyet kromozomlarına bağlı ve Mendel dışı kalıtım modelleri özel klinik dinamiklere sahiptir: "
            "1. **X'e Bağlı Resesif Kalıtım:** "
            "- Mutant gen X kromozomu üzerindedir. Erkekler tek X kromozomuna sahip olduğundan (**hemizigot**) mutasyonu aldıklarında "
            "kaçınılmaz olarak hasta olurlar. "
            "- Dişiler ise iki X kromozomuna sahip oldukları için genellikle asemptomatik taşıyıcıdır. "
            "- **Altın Kural:** Hastalıklı bir erkek hastalığını **asla oğullarına aktaramaz** (çünkü oğluna Y kromozomu verir); "
            "ancak **tüm kız çocukları zorunlu taşıyıcı** olur. "
            "- Örnekler: Duchenne Musküler Distrofi, Hemofili A ve B, G6PD eksikliği. "
            "2. **Mitokondriyal (Maternal) Kalıtım:** "
            "- Mitokondriyal DNA (mtDNA) yalnızca annenin oosit sitoplazmasından döle geçer; sperm mitokondrileri zigota katılmaz. "
            "- Hasta bir annenin **tüm çocukları** (kız ve erkek) hastalığı alır; hasta erkek ise hastalığı çocuklarına aktaramaz. "
            "Örnek: Leber herediter optik nöropatisi (LHON)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "X'e Bağlı Kalıtım vs Mitokondriyal Kalıtım Zıtlığı",
                "X'e Bağlı Resesif Kalıtım",
                "Hasta erkek hastalığı asla oğluna aktaramaz; tüm kızları zorunlu taşıyıcı olur; klinik hastalık erkeklerde patlar",
                "Mitokondriyal Kalıtım (Maternal)",
                "Hasta annenin tüm çocukları mutant mtDNA'yı alır; babadan çocuklara hiçbir zaman geçiş gerçekleşmez"
            ),
            make_active_recall(
                "Hemofili A veya Duchenne musküler distrofi gibi X'e bağlı resesif bir hastalığı olan babanın erkek çocuklarına bu hastalığı geçirememe nedeni nedir?",
                "Babanın erkek çocuklarına X değil yalnızca Y cinsiyet kromozomunu aktarmasıdır.",
                "Erkek cinsiyeti belirleyen paternal gonozom kalıtım kuralı"
            )
        ]
    })

    # Slayt 15: Marfan Sendromu Etyolojisi: FBN1 ve Fibrillin-1
    slides.append({
        "id": "k1-26-s15",
        "title": "Marfan Sendromu Etyolojisi: FBN1 ve Fibrillin-1",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 15,
        "narrative": (
            "Marfan sendromu, bağ dokusunun elastik lif bütünlüğünü bozan klasik bir **otozomal dominant** hastalıktır: "
            "1. **Genetik Temel:** Kromozom **15q21.1** lokusunda yer alan **FBN1 (Fibrillin-1)** genindeki mutasyonlardan kaynaklanır. "
            "Vakaların yaklaşık %75-85'i ailesel kalıtılırken, %15-25'i sporadik yeni (de novo) mutasyonlarla ortaya çıkar. "
            "2. **Fibrillin-1 Proteini:** 350 kDa ağırlığında büyük bir ekstraselüler glikoproteindir. "
            "- Fibroblastlar tarafından sentezlenir ve mikrofibrillerin temel iskeletini oluşturur. "
            "- Mikrofibriller, elastik liflerin üzerine yerleştiği yapısal bir kılıf görevi görür; aorta, bağ dokusu ligamentlerine "
            "ve göz merceğini tutan siliyer zonüllere mekanik direnç sağlar. "
            "3. **Dominant Negatif Hasar:** Mutant fibrillin-1 monomerleri sağlam monomerlerle birleşerek mikrofibril polimerizasyonunu "
            "bozar; dokularda elastik liflerin parçalanmasına ve bağ dokusu zafiyetine yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Fibrillin-1 Biyolojisi ve Marfan Mutasyonu",
                ["Bileşen", "Biyolojik Karşılığı", "Patofizyolojik Sonucu"],
                [
                    ["Kromozomal Lokus", "15q21.1", "FBN1 gen haritası"],
                    ["Kalıtım Modeli", "Otozomal Dominant (%75 ailesel, %25 de novo)", "Her gebelikte %50 aktarım riski"],
                    [
                        "Proteinin Fonksiyonu",
                        {"text": "Elastik lifler için mikrofibriler iskelet çatısı oluşturmak", "isMasked": True, "hint": "Aort duvarı ve göz zonüllerinde elastine destek sağlayan fibröz ağ"},
                        "Doku gerilme direncini sağlamak"
                    ],
                    ["Moleküler Hasar Tipi", "Dominant negatif etki ve haployetmezlik", "Elastik liflerin fragmantasyonu ve doku laksisitesi"]
                ]
            ),
            make_active_recall(
                "Marfan sendromunun etyolojisinde rol oynayan ve elastik dokularda mikrofibrillerin temel yapıtaşı olan proteini kodlayan gen hangisidir?",
                "FBN1 genidir (Fibrillin-1 proteini).",
                "On beşinci kromozomda yerleşik mikrofibril glikoproteini geni"
            )
        ]
    })

    # Slayt 16: Marfan Sendromunda TGF-β Aşırı Sinyalizasyonu
    slides.append({
        "id": "k1-26-s16",
        "title": "Marfan Sendromunda TGF-β Aşırı Sinyalizasyonu",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 16,
        "narrative": (
            "Geleneksel olarak Marfan sendromu yalnızca mekanik bir bağ dokusu zayıflığı olarak kabul edilirdi; "
            "ancak modern patoloji doku hasarının merkezinde aktif bir sitokin disregülasyonu olduğunu kanıtlamıştır: "
            "1. **Fibrillin-1'in Sekestrasyon Görevi:** Sağlam mikrofibriller, latent TGF-β bağlayıcı proteini (LTBP) bağlayarak "
            "büyüme faktörü **TGF-β'yı inaktif formda ekstraselüler matriks içinde hapseder (sekestre eder)**. "
            "2. **Aşırı TGF-β Sinyali:** Fibrillin-1 azaldığında veya yapısı bozulduğunda, TGF-β matriks içinde tutulamaz ve "
            "dokularda **aşırı miktarda serbest kalarak reseptörlerini aktive eder**. "
            "3. **Matriks Yıkımı:** Serbest TGF-β sinyali; vasküler düz kas hücrelerinde apoptozu tetikler, aşırı kollajen depolanması "
            "ve paradoksal olarak **matriks metalloproteinazların (MMP-2, MMP-9)** ekspresyonunu artırır. "
            "MMP'ler elastik lifleri sindirerek aort duvarını zayıflatır. "
            "4. **Klinik İlaç Hedefi:** TGF-β sinyalini baskılayan Anjiyotensin Reseptör Blokörleri (**Losartan**), "
            "Marfan hastalarında aort kökü genişlemesini yavaşlatmak amacıyla klinik protokollere girmiştir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Marfan Sendromunda TGF-β Kaynaklı Aort Duvar Yıkımı Zinciri",
                [
                    "1. FBN1 Mutasyonu: Kusurlu veya yetersiz fibrillin-1 sentezi ve mikrofibril mimarisinin çökmesi",
                    "2. Sekestrasyon Kaybı: İnaktif TGF-β'nın matriks içinde tutulamayıp kontrolsüz serbest kalması",
                    "3. Reseptör Hiperaktivasyonu: Serbest TGF-β'nın damar düz kas hücrelerindeki reseptörleri aşırı uyarması",
                    "4. MMP İndüksiyonu: Matriks metalloproteinazların (MMP) dokuda sentezlenip elastik lamelleri eritmesi",
                    "5. Kistik Medial Nekroz: Aort tunika medyasında elastik lif kaybı ve anevrizmatik genişleme"
                ]
            ),
            make_cloze(
                "Marfan sendromunda fibrillin-1 defekti sonucu dokularda sekestre edilemeyip aşırı aktifleşen ve aort yıkımını hızlandıran büyüme faktörü TGF-β faktörüdür.",
                "TGF-β",
                "Mikrofibrillere bağlı inaktif depolanan ve zedelenmede serbestleşen transforme edici sitokin"
            )
        ]
    })

    # Slayt 17: Marfan Sendromunda İskelet Sistemi Bulguları
    slides.append({
        "id": "k1-26-s17",
        "title": "Marfan Sendromunda İskelet Sistemi Bulguları",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 17,
        "narrative": (
            "Marfan sendromunun en çarpıcı ve hekimin kapıdan girerken tanı koymasını sağlayan bulguları iskelet sistemindedir: "
            "1. **Habitus ve Boy:** Hastalar boy ve kulaç uzunluğuyla dikkat çeker; boy ortalamanın çok üzerindedir. "
            "Kulaç açıklığı (kollar iki yana açıldığında parmak uçları arası mesafe), boy uzunluğundan belirgin olarak fazladır. "
            "Üst segment / alt segment oranı azalmıştır (uzun bacaklar). "
            "2. **Araknodaktili (Örümcek Parmaklar):** El ve ayak parmakları aşırı derecede uzun, ince ve narincedir. "
            "- **Steinberg Belirtisi (Başparmak Belirtisi):** Başparmak avuç içine kapatılıp yumruk yapıldığında, başparmak tırnağının "
            "ulnar el kenarını belirgin şekilde aşmasıdır. "
            "- **Walker-Murdoch Belirtisi (Bilek Belirtisi):** Karşı elin başparmağı ve küçük parmağıyla bilek sarıldığında, "
            "parmak uçlarının birbiri üzerine binmesidir. "
            "3. **Göğüs Deformiteleri:** Kostal kıkırdakların aşırı uzaması sonucu **pektus ekskavatum (kunduracı göğsü)** "
            "veya **pektus karinatum (güvercin göğsü)** gelişir. "
            "4. **Omurga:** İlerleyici kifoz, skolyoz ve eklem kapsülü laksisitesine bağlı eklem hipermobilitesi eşlik eder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Marfan Sendromunda Klasik İskelet Belirteçleri",
                ["Fizik Muayene Bulgusu", "Morfolojik Görünüm", "Klinik / Biyomekanik Anlamı"],
                [
                    ["Araknodaktili", "Uzun, ince, örümcek benzeri parmaklar", "Eklem ligament gevşekliği ile el parmaklarının aşırı uzaması"],
                    ["Steinberg Başparmak Testi", "Yumrukta başparmağın ulnar kenarı aşması", "Metakarp ve falanks kemiklerinin orantısız uzunluğu"],
                    [
                        "Walker-Murdoch Bilek Testi",
                        {"text": "Bilek sarıldığında baş ve küçük parmakların örtüşmesi", "isMasked": True, "hint": "El bileği çevresinin zayıf kemik yapısı ve uzun parmaklarla tamamen kavranması"},
                        "Kemik inceliği ve uzun falanks belirteci"
                    ],
                    ["Göğüs Kafesi Deformitesi", "Pektus ekskavatum veya karinatum", "Kostal kıkırdakların elastik gevşeklikle aşırı büyümesi"],
                    ["Omurga Patolojisi", "Ağır kifoskolyoz", "Toraks hacmini daraltarak restriktif solunum sıkıntısı riski"]
                ]
            ),
            make_active_recall(
                "Marfan sendromunda el parmaklarının orantısız biçimde aşırı uzun, ince ve narin olması durumunu tanımlayan klasik tıbbi terim nedir?",
                "Araknodaktilidir (örümcek parmaklar).",
                "El ve ayak parmaklarının uzun kemik büyümesiyle örümcek bacaklarına benzetilmesi"
            )
        ]
    })

    # Slayt 18: Marfan Sendromunda Oküler Tutulum: Ektopia Lentis
    slides.append({
        "id": "k1-26-s18",
        "title": "Marfan Sendromunda Oküler Tutulum: Ektopia Lentis",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 18,
        "narrative": (
            "Göz, Marfan sendromunun tanısal kriterleri arasında yer alan majör hedef organlardan biridir: "
            "1. **Ektopia Lentis (Göz Merceği Subluksasyonu):** "
            "- Hastaların yaklaşık %60-70'inde saptanır ve Marfan için son derece karakteristiktir. "
            "- Göz merceğini siliyer cisimciğe asan ve asılı kalmasını sağlayan lifler (**siliyer zonüller - Zinn lifleri**) "
            "tamamen fibrillin-1 mikrofibrillerinden yapılmıştır. "
            "- Fibrillin-1 kusuru zonül liflerinin zayıflamasına ve yer yer kopmasına yol açar. "
            "2. **Subluksasyon Yönü (Kritik Ayrım):** "
            "- Marfan sendromunda lens tipik olarak **yukarı ve dışa (superior-temporal)** doğru kayar (sublukse olur). "
            "- Bu bulgu, otozomal resesif homosistinüride görülen **aşağı ve içe (inferior-nazal)** lens subluksasyonundan "
            "ayırt edici altın standart sınav ve kurul sorusudur! "
            "3. **Diğer Oküler Bulgular:** Ağır miyopi, düzleşmiş kornea ve zonül lif zayıflığı zemininde artmış **retina dekolmanı** riski."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Lens Subluksasyonunda Marfan vs Homosistinüri Ayrımı",
                "Marfan Sendromu (FBN1 Defekti)",
                "Otozomal dominant; siliyer zonül zayıflığı ile göz merceğinin YUKARI ve DIŞA (superotemporal) kayması",
                "Homosistinüri (Sistationin Sentaz Defekti)",
                "Otozomal resesif; enzim eksikliği ve tromboz zemininde göz merceğinin AŞAĞI ve İÇE (inferonazal) kayması"
            ),
            make_micro_quiz(
                "Göz muayenesinde bilateral lens subluksasyonu (ektopia lentis) saptanan uzun boylu ve ince parmaklı genç bir hastada lensin YUKARI VE DIŞA yer değiştirdiği izlenmiştir. Bu hastadaki kesin kalıtsal patoloji hangisidir?",
                {
                    "A": "Marfan Sendromu (FBN1 gen mutasyonu)",
                    "B": "Homosistinüri (Sistationin beta-sentaz eksikliği)",
                    "C": "Ehlers-Danlos Sendromu Tip IV",
                    "D": "Kistik Fibrozis (CFTR mutasyonu)",
                    "E": "Osteogenezis İmperfekta Tip I"
                },
                "A",
                {
                    "A": "Doğrudur; siliyer zonül zafiyetinde lensin yukarı-dışa subluksasyonu Marfan sendromunun patognomonik oküler bulgusudur.",
                    "B": "Yanlış; homosistinüride lens aşağı ve içe kayar.",
                    "C": "Yanlış; EDS damar rüptürleri yapar, lens subluksasyonu primer değildir.",
                    "D": "Yanlış; CFTR epitel klor kanalıdır.",
                    "E": "Yanlış; osteogenezis imperfektada mavi sklera görülür."
                }
            )
        ]
    })

    # Slayt 19: Checkpoint 2
    slides.append({
        "id": "k1-26-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Mendel Kalıtımı ve Marfan Sendromu Patolojisi",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 19,
        "narrative": (
            "İkinci bölüm kontrol noktamızda tek gen hastalıklarını ve Marfan sendromu patolojisini pekiştiriyoruz: "
            "1. **Mendel Tipleri:** OD yapısal proteinleri tutar (her gebelikte %50 risk, dominant negatif/haployetmezlik); "
            "OR enzim defektleridir (her gebelikte %25 risk, taşıyıcı ebeveynler, akraba evliliği). "
            "2. **Marfan Moleküler Temeli:** 15q21'deki FBN1 geni; mikrofibrillerin ana proteini fibrillin-1 sentezlenemez. "
            "3. **TGF-β Mekanizması:** Fibrillin-1 eksikliğinde TGF-β sekestre edilemez; serbest TGF-β aşırı sinyal vererek MMP'leri "
            "tetikler ve elastik dokuyu eritir. "
            "4. **İskelet Triadı:** Uzun boy, kulaç > boy, araknodaktili (Steinberg ve Walker-Murdoch pozitif), pektus deformiteleri. "
            "5. **Oküler İmza:** Siliyer zonül zafiyetiyle lensin yukarı ve dışa (superotemporal) subluksasyonu (Ektopia lentis). "
            "6. **Kardiyovasküler Tehdit:** Aort kökünde kistik medial nekroz, dilatasyon, diseksiyon ve letal rüptür riski."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s19-1",
                "Marfan sendromuna yol açan ve mikrofibrillerin yapıtaşı olan fibrillin-1 proteinini kodlayan mutant gen nedir?",
                "FBN1 genidir.",
                "On beşinci kromozom üzerinde haritalanmış fibröz glikoprotein şifresi",
                "FBN1 ve Marfan"
            ),
            make_flashcard(
                "k1-26-fc-s19-2",
                "Marfan sendromunda fibrillin-1 eksikliği nedeniyle dokularda kontrolsüz şekilde aşırı aktifleşerek ekstraselüler matriksi yıkan büyüme faktörü yolağı nedir?",
                "TGF-beta sinyal yolağıdır.",
                "Fibröz doku elastisitesini bozan ve reseptör kinazları uyaran transforme edici faktör",
                "TGF-beta Patogenezi"
            ),
            make_flashcard(
                "k1-26-fc-s19-3",
                "Marfan sendromlu hastalarda morbidite ve erken mortalitenin en sık nedeni olan hayati kardiyovasküler komplikasyon nedir?",
                "Aort kökü diseksiyonu ve rüptürüdür.",
                "Çıkan ana arter lümeninde intima yırtılması ve kistik medial nekroz zemininde yırtılma",
                "Marfan Kardiyovasküler"
            )
        ],
        "interactiveElements": [
            make_table(
                "Marfan Sendromunun Organ Sistemlerine Göre Dağılımı",
                ["Sistem", "Patolojik Lezyon", "Moleküler / Histolojik Mekanizma", "Klinik Sonuç"],
                [
                    ["Kardiyovasküler", "Aort kökü dilatasyonu ve diseksiyon", "Kistik medial nekroz, elastik lif lizisi", "Letal aort rüptürü, kapak yetmezliği"],
                    [
                        "Göz (Oküler)",
                        "Ektopia lentis (yukarı-dışa)",
                        {"text": "Siliyer zonül mikrofibrillerinin zayıflaması", "isMasked": True, "hint": "Göz merceğini siliyer cisimciğe asan fibrillin-1 zengin asıcı bağlar"},
                        "Görme kusuru, miyopi, retina dekolmanı"
                    ],
                    ["İskelet", "Araknodaktili, pektus, skolyoz", "Uzun kemik epifiz kıkırdak elastisite kaybı", "Uzun parmaklar, toraks deformitesi"],
                    ["Deri / Akciğer", "Striae distensae, spontan pnömotoraks", "Dermal ve subplevral elastik lif zayıflığı", "Cilt çatlakları, apikal bül rüptürü"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi Marfan sendromlu bir hastada fizik muayenede araknodaktili varlığını gösteren pozitif bir muayene bulgusudur?",
                {
                    "A": "Steinberg belirtisi (başparmağın kapalı yumrukta ulnar kenarı aşması)",
                    "B": "Nikolsky belirtisi (cilt bülünün parmak basısıyla kayması)",
                    "C": "Trousseau belirtisi (tansiyon aletiyle kolda ebe eli spazmı)",
                    "D": "Chvostek belirtisi (fasiyal sinire vurunca yüzde seğirme)",
                    "E": "Babinski belirtisi (ayak tabanı uyarısıyla başparmak ekstansiyonu)"
                },
                "A",
                {
                    "A": "Doğrudur; Steinberg başparmak ve Walker-Murdoch bilek testleri araknodaktili belirteçleridir.",
                    "B": "Yanlış; Nikolsky pemfigus vulgariste pozitiftir.",
                    "C": "Yanlış; Trousseau hipokalsemi tetanisidir.",
                    "D": "Yanlış; Chvostek hipokalsemi tetanisidir.",
                    "E": "Yanlış; Babinski üst motor nöron lezyonudur."
                }
            )
        ]
    })

    # Slayt 20: Marfan Sendromunda Kardiyovasküler Felaket
    slides.append({
        "id": "k1-26-s20",
        "title": "Marfan Sendromunda Kardiyovasküler Felaket: Kistik Medial Nekroz ve Diseksiyon",
        "section": "Mendel Kalıtımı ve Marfan Sendromu",
        "slideNumber": 20,
        "narrative": (
            "Marfan sendromlu hastaların yaşam beklentisini belirleyen ve vakaların %30-45'inde erken ölüme yol açan "
            "en kritik patoloji kardiyovasküler sistemdedir: "
            "1. **Kistik Medial Nekroz (Cystic Medial Degeneration):** "
            "- Çıkan aort tunika medyasında elastik liflerin parçalanması (elastolizis), düz kas hücrelerinin kaybı ve "
            "arada amorf mukopolisakkarid (glikozaminoglikan) dolu kistik boşlukların oluşmasıdır. "
            "2. **Aort Kökü Dilatasyonu ve Anevrizması:** "
            "- Elastik geri çekilme direncini kaybeden aort kökü, sol ventrikülün sistolik vuruş basıncına dayanamayarak "
            "giderek balonlaşır (asendan aort anevrizması). "
            "- Aort kapak halkası genişler; kapaklar kapanamaz ve **ağır aort yetersizliği** ve sol kalp yetmezliği gelişir. "
            "3. **Aort Diseksiyonu ve Rüptürü (En Ölümcül Komplikasyon):** "
            "- İntimada meydana gelen yırtıktan giren yüksek basınçlı kan, zayıflamış tunika medyayı boylu boyunca iki yaprağa "
            "ayırır (Stanford Tip A Aort Diseksiyonu). "
            "- Kanın adventisyayı yırtarak perikard boşluğuna boşalmasıyla **kardiyak tamponad** ve dakikalar içinde ani ölüm gerçekleşir. "
            "4. **Mitral Kapak Prolapsusu (MVP):** Kapak yaprakçıklarında miksomatöz dejenerasyonla 'paraşüt kapak' ve mitral yetmezlik izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Marfan Sendromunda Letal Aort Diseksiyonu Mekanizması",
                [
                    "1. Medial Elastoliz: Tunika medyada elastik liflerin erimesi ve kistik mukoid birikim (kistik medial nekroz)",
                    "2. Damar Duvarı Zayıflığı: Aort kökünün sistolik atım basıncına dayanamayıp anevrizmatik genişlemesi",
                    "3. İntimal Yırtılma: Mekanik gerilim noktasında intima endotelinde yırtık açılması",
                    "4. Medyal Diseksiyon: Basınçlı kanın medyanın iki tabakası arasına girerek yalancı lümen oluşturması",
                    "5. Perikarda Rüptür: Kanın perikardiyal kese içine patlayarak akut tamponad ve ani ölüme yol açması"
                ]
            ),
            make_active_recall(
                "Marfan sendromlu bir hastada çıkan aort duvarında mikroskobik olarak elastik liflerin parçalanması, düz kas hücre kaybı ve aralarında bazofilik mukopolisakkarid gölcükleri birikmesiyle karakterize histopatolojik lezyon nedir?",
                "Kistik medial nekrozdur (kistik medial dejenerasyon).",
                "Tunika medyada elastik tabakaların erimesiyle oluşan patognomonik aort zayıflığı lezyonu"
            )
        ]
    })

    return slides
