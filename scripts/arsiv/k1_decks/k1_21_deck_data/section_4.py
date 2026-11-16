# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 4: Ökaryotik Patojenler: Mantarlar ve Parazitler (Slayt 31 - 40)
Checkpoint 4: Slayt 39
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # Slayt 31: Mantarların Genel Biyolojisi ve Morfolojisi
    slides.append({
        "id": "k1-21-s31",
        "title": "Mantarların Genel Biyolojisi: Maya, Küf ve Dimorfizm",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 31,
        "narrative": (
            "Mantarlar (Fungi), gerçek çekirdek zarı, mitokondrisi ve membranlı organelleri bulunan **ökaryotik** mikroorganizmalardır. "
            "Bakterilerden farklı olarak hücre zarlarında kolesterol yerine **ergosterol** taşırlar; hücre duvarları ise "
            "peptidoglikan yerine **kitin, glukan ve mannan** polisakkaritlerinden örülüdür. "
            "Morfolojik olarak iki temel grupta incelenirler: "
            "1. **Mayalar (Yeasts):** Tek hücreli, yuvarlak veya oval mantarlardır; aseksüel olarak **tomurcuklanma (blastokonidya)** "
            "veya fisyon ile çoğalırlar (örneğin Candida albicans, Cryptococcus neoformans). "
            "2. **Küfler (Molds):** Çok hücreli, tübüler ipliksi yapılardan (**hif**) oluşan mantarlardır; "
            "hiflerin oluşturduğu keçemsi yumağa **miselyum** denir; sporlarla çevreye yayılırlar (örneğin Aspergillus, Mucor). "
            "3. **Dimorfik Mantarlar:** Ortam sıcaklığına bağlı olarak şekil değiştiren bukalemun mantarlardır! "
            "Oda sıcaklığında (25°C) doğada küf (misel) formunda yaşarken; insan vücut sıcaklığında (37°C) dokularda **maya** formuna dönüşürler "
            "('Kalıpta küf, kanda maya' kuralı: Histoplasma, Blastomyces, Coccidioides)."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mantar hücre zarında memelilerdeki kolesterolün yerini alan ve antifungal ilaçların ana hedefi olan sterol ergosterol molekülüdür.",
                "ergosterol",
                "Azol ve amfoterisin B ilaçlarının hedef aldığı mantar hücre zarı sterolü"
            ),
            make_before_after(
                "Maya Mantarları ile Küf Mantarlarının Karşılaştırması",
                "Maya Mantarları (Örn. Candida)",
                [
                    "Hücresel yapı: Tek hücreli, oval veya sferik organizmalar",
                    "Üreme biçimi: Tomurcuklanma (blastokonidya) ile çoğalma",
                    "Koloni morfolojisi: Bakteri kolonilerine benzer nemli, kremsi görünüm",
                    "Klinik örnekler: Candida albicans, Cryptococcus neoformans"
                ],
                "Küf Mantarları (Örn. Aspergillus)",
                [
                    "Hücresel yapı: Çok hücreli, dallanan ipliksi tüpler (hifler)",
                    "Üreme biçimi: Hiflerin uzaması ve havai konidyum/spor saçılımı",
                    "Koloni morfolojisi: Kadifemsi, pamuksu veya renkli keçemsi miselyum",
                    "Klinik örnekler: Aspergillus fumigatus, Mucor, Rhizopus"
                ]
            ),
            make_active_recall(
                "Doğada ve 25°C oda sıcaklığında küf formunda, 37°C insan dokusunda ise maya formunda yaşayan mantarlar hangi sınıfa girer?",
                "Termal dimorfik mantarlar (dimorfik mikozlar) sınıfına girer.",
                "Sıcaklığa göre şekil değiştiren mantar grubu"
            )
        ]
    })

    # Slayt 32: Mikozların Derinlik Sınıflandırması
    slides.append({
        "id": "k1-21-s32",
        "title": "Mikozların Derinlik Sınıflandırması: Yüzeyel, Kutanöz ve Subkutan",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 32,
        "narrative": (
            "Mantar enfeksiyonları (mikozlar), doku tutulumunun derinliğine ve invazyon kapasitesine göre anatomik olarak sınıflandırılır: "
            "1. **Yüzeyel Mikozlar:** Stratum korneumun en dış ölü katmanına ve saç şaftına sınırlıdır; konakta hiçbir inflamatuar yanıt uyarılmaz. "
            "En klasik örnek **Malassezia furfur** etkenli **Pitiriyazis Versikolor**'dur; gövdede hipopigmente veya hiperpigmente pullanan lekeler yapar "
            "(deri kazıntısında mikroskopta 'köfte-makarna' manzarası izlenir). "
            "2. **Kutanöz Mikozlar (Dermatofitozlar):** Derinin keratinize tabakasını, saçları ve tırnakları keratinaz enzimi ile sindiren "
            "**Dermatofitler** (Trichophyton, Microsporum, Epidermophyton) tarafından oluşturulur. "
            "Kızarık, kaşıntılı, kenarları aktif halkasal lezyonlara **Tinea (Halka kurdu)** denir (Tinea pedis / atlet ayağı, Tinea korporis, Tinea kapitis). "
            "3. **Subkutan Mikozlar:** Travmatik batma (örneğin gül dikeni batması) ile dermis ve subkutan dokuya inoküle olan mantarlardır. "
            "Prototipi **Sporothrix schenckii** kaynaklı **Sporotrikoz (Bahçıvan Hastalığı)**'dur; inokülasyon yerinde nodül ve lenfatik damar boyunca dizilen zincirleme ülserlerle seyreder."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Gül dikeni batması sonrası lenfatik damarlar boyunca nodüler ülserasyonlarla seyreden subkutan mikoz tablosuna sporotrikoz adı verilir.",
                "sporotrikoz",
                "Bahçıvan hastalığı olarak da bilinen Sporothrix enfeksiyonu"
            ),
            make_table(
                ["Mikoz Grubu", "Hedeflenen Anatomik Doku", "Klasik Etken ve Hastalık"],
                [
                    ["Yüzeyel Mikoz", "Stratum korneum en dışı (yangısız)", "Malassezia furfur (Pitiriyazis versikolor)"],
                    [
                        "Kutanöz Mikoz",
                        {"text": "Keratinize deri, saç ve tırnaklar", "isMasked": True, "hint": "Keratinaz enzimiyle beslenen mantarlar"},
                        "Dermatofitler (Tinea pedis, Tinea korporis, Tinea unguium)"
                    ],
                    ["Subkutan Mikoz", "Dermis, subkutan bağ dokusu, lenfatikler", "Sporothrix schenckii (Sporotrikoz / Bahçıvan hastalığı)"]
                ]
            ),
            make_micro_quiz(
                "Gövdede kaşıntısız hipopigmente lekelerle başvuran bir hastanın lezyon kazıntısında mikroskop altında maya hücreleri ve kısa hiflerin oluşturduğu 'köfte-makarna' görüntüsü saptanıyor. En olası etken hangisidir?",
                {
                    "A": "Malassezia furfur",
                    "B": "Candida albicans",
                    "C": "Trichophyton rubrum",
                    "D": "Sporothrix schenckii",
                    "E": "Aspergillus fumigatus"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Malassezia furfur pitiriyazis versikolor etkenidir ve kazıntıda 'spagetti ve köfte' manzarası patognomoniktir.",
                    "B": "B seçeneği psödohif ve tomurcuklanan maya gösterir.",
                    "C": "C seçeneği dermatofittir, septalı hif yapar.",
                    "D": "D seçeneği puro şeklinde mayalar yapar.",
                    "E": "E seçeneği küftür."
                }
            )
        ]
    })

    # Slayt 33: Sistemik Endemik Mikozlar
    slides.append({
        "id": "k1-21-s33",
        "title": "Sistemik Endemik Mikozlar: Toprak ve Solunum Kaynaklı Tehditler",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 33,
        "narrative": (
            "Sistemik endemik mikozlar, belirli coğrafi bölgelerin topraklarında doğal olarak yaşayan, "
            "konidia sporlarının solunması ile primer olarak akciğerleri enfekte eden ve bağışıklığı tam bireylerde bile "
            "granülomatöz hastalık oluşturabilen **termal dimorfik mantarlardır**. Üç majör prototipi vardır: "
            "1. **Histoplasma capsulatum:** Kuş ve yarasa gübresi ile zenginleşmiş topraklarda (mağaralar, kümesler) yaşar. "
            "Sporları solunduğunda alveoler makrofajlar tarafından fagosite edilir ve **makrofajların içinde yaşayan minik mayalar** haline gelir. "
            "Akciğerde tüberküloz benzeri granülomlar, kalsifikasyonlar ve immünsüprese konakta kemik iliği tutulumuyla yaygın histoplazmoz yapar. "
            "2. **Coccidioides immitis:** Amerika'nın kurak güneybatı çöllerinde yaşar. Toz fırtınalarıyla solunan artrokonidyalar "
            "akciğer dokusunda endosporlarla dolu devasa kalın duvarlı kürelere (**sferül**) dönüşür. "
            "'Vadi humması (San Joaquin Valley Fever)' veya eritema nodozumlu 'çöl romatizması' tablosuna yol açar. "
            "3. **Blastomyces dermatitidis:** Nemli toprak ve çürüyen ağaç kütüklerinde bulunur; dokuda karakteristik geniş tabanlı tomurcuklanan büyük mayalar oluşturur."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Yarasa ve kuş gübresiyle kontamine mağaralarda sporların solunmasıyla bulaşan ve makrofaj içinde maya oluşturan mantar Histoplasma capsulatum etkenidir.",
                "Histoplasma capsulatum",
                "İntrasellüler makrofaj parazitizmi yapan dimorfik endemik mikoz"
            ),
            make_table(
                ["Endemik Mikoz", "Ekolojik Rezervuar", "Dokudaki Mikroskobik Morfoloji"],
                [
                    ["Histoplasma capsulatum", "Kuş ve yarasa dışkılı toprak / mağaralar", "Makrofaj sitoplazması içinde minik mayalar"],
                    [
                        "Coccidioides immitis",
                        {"text": "Kurak çöl kumu ve toz fırtınaları", "isMasked": True, "hint": "Coccidioides türlerinin endemik vadi humması ekolojisi"},
                        "İçi endospor dolu dev kalın duvarlı sferüller"
                    ],
                    ["Blastomyces dermatitidis", "Çürüyen tahta ve nemli nehir toprağı", "Geniş tabanlı tomurcuklanan kalın duvarlı mayalar"]
                ]
            ),
            make_micro_quiz(
                "Akciğer biyopsisinde makrofajların sitoplazması içinde çok sayıda küçük maya hücreleri saptanan ve mağara keşfi öyküsü olan bir hastada en olası mantar hangisidir?",
                {
                    "A": "Coccidioides immitis",
                    "B": "Histoplasma capsulatum",
                    "C": "Aspergillus fumigatus",
                    "D": "Cryptococcus neoformans",
                    "E": "Rhizopus oryzae"
                },
                "B",
                {
                    "A": "A seçeneği dokuda dev sferül oluşturur, makrofaj içi minik maya yapmaz.",
                    "B": "B seçeneği doğrudur: Histoplasma capsulatum makrofajlar içinde yaşayan minik mayalarla karakterizedir; yarasa gübresi mağara maruziyeti tipiktir.",
                    "C": "C seçeneği dik açılı hif yapar.",
                    "D": "D seçeneği kalın kapsüllü serbest mayadır.",
                    "E": "E seçeneği geniş hifli mukormikoz etkenidir."
                }
            )
        ]
    })

    # Slayt 34: Fırsatçı Sistemik Mikozlar
    slides.append({
        "id": "k1-21-s34",
        "title": "Fırsatçı Sistemik Mikozlar: Candida, Aspergillus, Kriptokok ve Mukor",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 34,
        "narrative": (
            "Bağışıklığı baskılanmış, nötropenik veya yoğun bakımda yatan hastalarda fatal enfeksiyonlara yol açan 4 ana fırsatçı mantar grubu vardır: "
            "1. **Candida albicans:** Normal flora üyesidir; psödohif ve gerçek hif oluşturabilme yeteneğindedir (37°C serumda **germ tüpü** oluşturması tanı dikeçidir). "
            "Mukozal pamukçuktan yoğun bakım kateter ilişkili ölümcül kandidiyemiye kadar geniş bir spektrum oluşturur. "
            "2. **Aspergillus fumigatus:** Çevre havasında yaygın küftür; dokuda karakteristik **45° dik açıyla dallanan septalı hifler** yapar. "
            "Eski tüberküloz kaviteleri içine yerleşerek hareketli mantar topu (**Aspergilloma**) veya nötropeniklerde anjiyoinvaziv nekrotizan pnömoni yapar. "
            "3. **Cryptococcus neoformans:** Güvercin dışkısıyla zengin topraklarda bulunan kalın **polisakkarit kapsüllü** mayadır. "
            "Çini mürekkebi (India ink) boyasında geniş kapsülü negatif parlama verir; AIDS hastalarında subakut fungal menenjitin 1 numaralı nedenidir. "
            "4. **Mucorales (Mucor, Rhizopus):** **90° geniş açıyla dallanan septasız kalın hifler** taşır. Diyabetik ketoasidozlu veya nötropenik hastalarda "
            "kan damarlarını invaze edip burun, göz ve beyni dakikalar içinde çürüten ölümcül **Rinoserebral Mukormikoz** tablosuna yol açar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Diyabetik ketoasidozlu hastada damar invazyonuyla siyah nekrotik eskar ve rinoserebral enfeksiyon yapan doksan derece dallanan hifli mantar Mukor mantarıdır.",
                "Mukor",
                "Septasız geniş açılı hifleri olan agresif anjiyoinvaziv küf cinsi"
            ),
            make_table(
                ["Fırsatçı Mantar", "Histopatolojik Mikroskobik Özellik", "Karakteristik Klinik Tablo"],
                [
                    ["Candida albicans", "Mayalar, psödohifler ve germ tüpü pozitifliği", "Pamukçuk, vajinit, kateter kandidiyemisi"],
                    [
                        "Aspergillus fumigatus",
                        {"text": "45 derece dik açıyla dallanan septalı hifler", "isMasked": True, "hint": "Kavitelerde mantar topu oluşturan küf"},
                        "Akciğer aspergilloması ve anjiyoinvaziv pnömoni"
                    ],
                    ["Cryptococcus neoformans", "Geniş polisakkarit kapsülü (Çini mürekkebi +)", "AIDS hastalarında fungal menenjit"],
                    ["Mucor / Rhizopus", "90 derece dik/geniş açılı septasız küt hifler", "Diyabetik ketoasidozda rinoserebral nekroz"]
                ]
            ),
            make_micro_quiz(
                "AIDS tanılı 38 yaşındaki hastada subakut baş ağrısı ve ense sertliği üzerine yapılan lomber ponksiyonda BOS çini mürekkebi preparatında kalın kapsüllü maya hücreleri izleniyor. Tanı nedir?",
                {
                    "A": "Kandida menenjiti",
                    "B": "Kriptokoksik menenjit (Cryptococcus neoformans)",
                    "C": "Aspergillus absesi",
                    "D": "Pnömosistis menenjiti",
                    "E": "Toksoplazma ensefaliti"
                },
                "B",
                {
                    "A": "A seçeneği çini mürekkebinde geniş negatif kapsül halesi vermez.",
                    "B": "B seçeneği doğrudur: Cryptococcus neoformans kalın glukuronoksilomannan kapsüllü bir mayadır; çini mürekkebi ile AIDS menenjiti tipiktir.",
                    "C": "C seçeneği hif oluşturur.",
                    "D": "D seçeneği akciğer enfeksiyonu yapar.",
                    "E": "E seçeneği hücre içi protozoondur."
                }
            )
        ]
    })

    # Slayt 35: Parazitlerin Sınıflandırılması: Protozoonlar ve Helmintler
    slides.append({
        "id": "k1-21-s35",
        "title": "Tıbbi Parazitolojiye Giriş: Protozoonlar ve Helmintler",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 35,
        "narrative": (
            "Parazitler, insan konak üzerinde veya içinde yaşayarak konağın besinlerini tüketen ve doku hasarı "
            "oluşturan ökaryotik organizmalardır. Tıbbi parazitoloji 2 büyük biyolojik sınıfa ayrılır: "
            "1. **Protozoonlar (Tek Hücreli Ökaryotlar):** Hücre duvarı içermezler; konak içinde çoğalma (replikasyon) "
            "yeteneğine sahiptirler. Genellikle hareket organellerine göre sınıflanırlar: "
            "- **Amipler (Sarcodina):** Psödopodlarla (yalancı ayak) hareket ederler (Entamoeba histolytica). "
            "- **Kamçılılar (Flagellata):** Flagella ile hareket ederler (Giardia duodenalis, Trichomonas vaginalis, Leishmania). "
            "- **Silliler (Ciliata):** Sillerle hareket ederler (Balantidium coli). "
            "- **Sporozoonlar (Apicomplexa):** Karmaşık apikal kompleks taşırlar, hareket organelleri yoktur, hücre içi yaşarlar (Plasmodium, Toxoplasma). "
            "2. **Helmintler (Çok Hücreli Solucanlar / Metazoonlar):** Gözle görülebilen makroskobik parazitlerdir. "
            "Kural olarak **erişkin helmintler insan vücudu içinde çoğalarak sayılarını artıramazlar** "
            "(dışarıdan alınan yumurta veya larva sayısı kadar erişkin oluşur; istisna: Strongyloides otoenfeksiyonu). "
            "Helmintler morfolojilerine göre Nematodlar (yuvarlak), Sestodlar (şerit) ve Trematodlar (yaprak) olarak ayrılır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Helmint enfeksiyonlarında kural olarak erişkin parazitler insan vücudu içinde çoğalarak doğrudan sayılarını artıramazlar.",
                "sayılarını artıramazlar",
                "Helmintlerin protozoonlardan farklı olan biyolojik üreme kısıtlılığı"
            ),
            make_before_after(
                "Protozoonlar ile Helmintlerin Temel Biyolojik Farkları",
                "Protozoonlar (Tek Hücreliler)",
                [
                    "Mikroskobik tek hücreli ökaryotlardır",
                    "İnsan konağın içinde hızla bölünerek sayılarını katlayabilirler",
                    "Tek bir trofozoit veya kist girişi ağır klinik tablo başlatabilir",
                    "Hücre içi (Plasmodium) veya lümen içi (Giardia) yerleşirler"
                ],
                "Helmintler (Çok Hücreli Solucanlar)",
                [
                    "Makroskobik, dokuları ve organ sistemleri olan kurtçuklardır",
                    "İnsan vücudunda yumurtadan yeni erişkin üretemezler (çoğalmazlar)",
                    "Hastalığın ağırlığı doğrudan yutulan yumurta/larva yüküne bağlıdır",
                    "Tipik olarak kanda eozinofili ve yüksek IgE yanıtı uyarırlar"
                ]
            ),
            make_active_recall(
                "Hücre duvarı olmayan, tek hücreli ökaryotik mikroorganizmalar parazitolojide hangi üst gruba dahil edilir?",
                "Protozoonlar (Protozoa) grubuna dahil edilir.",
                "Tek hücreli ökaryot parazitlerin genel sınıf adı"
            )
        ]
    })

    # Slayt 36: Protozoon Enfeksiyonları: Sıtma, Toksoplazma ve Amipler
    slides.append({
        "id": "k1-21-s36",
        "title": "Kritik Protozoon Enfeksiyonları: Sıtma, Toksoplazmoz ve Amipler",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 36,
        "narrative": (
            "İnsan sağlığını küresel ölçekte en çok tehdit eden majör protozoonlar şunlardır: "
            "1. **Plasmodium Türleri (Sıtma / Malaria):** Dişi **Anopheles** sivrisineğinin ısırmasıyla bulaşır. "
            "Karaciğerdeki ilk çoğalmanın (ekzoeritrositer evre) ardından eritrositleri enfekte eder (**eritrositer şizogoni**). "
            "Eritrositlerin periyodik patlamasıyla titremeyle yükselen nöbetler halinde ateş ortaya çıkar. "
            "**Plasmodium falciparum** eritrositleri enfekte ederek mikrovasküler tıkanma (sekestrasyon), serebral sıtma ve ölüme yol açan en virülan türdür. "
            "2. **Toxoplasma gondii:** Kesin konağı **kedilerdir**. Kedi dışkısıyla atılan ookistlerin veya az pişmiş kistli etlerin yenmesiyle bulaşır. "
            "Gebelikte primer enfeksiyon konjenital triada yol açar: **Koryoretinit, Hidrosefali ve İntrakraniyal Kalsifikasyonlar**. "
            "3. **Entamoeba histolytica:** Fekal-oral yolla bulaşır; kolonda şişe benzeri (flakon/flask-shaped) derin ülserler yaparak **kanlı-mukuslu amip dizanterisine** "
            "ve portal yolla karaciğere giderek 'ançuez ezmesi' kıvamında **karaciğer amip apsesine** neden olur. "
            "4. **Giardia duodenalis:** Duodenum epiteline emici diskiyle yapışarak villus atrofisi ve yağlı pis kokulu ishal (steatore/malabsorpsiyon) yapar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Gebelikte geçirilen primer toksoplazmoz enfeksiyonunda bebekte hidrosefali, intrakraniyal kalsifikasyon ve koryoretinit klasik triadı görülür.",
                "koryoretinit",
                "Konjenital toksoplazmozun göz retinasını tahrip eden lezyonu"
            ),
            make_table(
                ["Protozoon Türü", "Bulaşma Yolu ve Vektörü", "Karakteristik Klinik Tablo"],
                [
                    ["Plasmodium falciparum", "Dişi Anopheles sivrisineği", "Malign tersiyana sıtma, serebral sıtma, siyah su ateşi"],
                    [
                        "Toxoplasma gondii",
                        {"text": "Kedi dışkısı ve az pişmiş et", "isMasked": True, "hint": "Kedilerin kesin konak olduğu parazit"},
                        "Lenfadenopati, konjenital enfeksiyon triadı, AIDS ensefaliti"
                    ],
                    ["Entamoeba histolytica", "Fekal-oral kist yutulması", "Flakon ülserleri, kanlı dizanteri, karaciğer amip apsesi"],
                    ["Giardia duodenalis", "Kontamine durgun yüzey suları", "Duodenojejunal malabsorpsiyon, yağlı sulu ishal"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki protozoonlardan hangisi kolon mukozasında tipik 'şişe / flakon benzeri (flask-shaped)' ülserler oluşturarak kanlı mukuslu dizanteri tablosuna yol açar?",
                {
                    "A": "Giardia duodenalis",
                    "B": "Entamoeba histolytica",
                    "C": "Trichomonas vaginalis",
                    "D": "Toxoplasma gondii",
                    "E": "Plasmodium vivax"
                },
                "B",
                {
                    "A": "A seçeneği duodenuma yapışır, invaziv kolonik flakon ülseri yapmaz.",
                    "B": "B seçeneği doğrudur: Entamoeba histolytica kolon submukozasında genişleyen tipik flakon (şişe) ülserleri ve amip dizanterisi yapar.",
                    "C": "C seçeneği ürogenital vajinit etkenidir.",
                    "D": "D seçeneği sistemik kist yapar.",
                    "E": "E seçeneği eritrositleri enfekte eder."
                }
            )
        ]
    })

    # Slayt 37: Helmintler I: Nematodlar (Yuvarlak Solucanlar)
    slides.append({
        "id": "k1-21-s37",
        "title": "Helmintler I: Nematodlar (Yuvarlak Solucanlar)",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 37,
        "narrative": (
            "Nematodlar, enine kesitleri yuvarlak, silindirik, segmentsiz ve tam bir sindirim kanalına (ağız ve anüs) "
            "sahip olan solucanlardır. Tıbbi önem taşıyan başlıca nematodlar şunlardır: "
            "1. **Enterobius vermicularis (Kıl Kurdu):** Dünyada ve ülkemizde çocuklarda en sık görülen helminttir. "
            "Dişi kıl kurdu geceleri perianal bölgeye göç ederek yumurtalarını bırakır; bu durum şiddetli **noktürnal perianal kaşıntıya** yol açar. "
            "Yumurtalar dışkıda değil, sabah uyanınca anal bölgeye yapıştırılan **selofan bant (Sellotape) yöntemi** ile mikroskopta saptanır. "
            "2. **Ascaris lumbricoides:** İnsan bağırsağındaki en büyük nematoddur (20-35 cm). Fekal-oral yumurta yutulmasıyla bulaşır. "
            "Larvaları bağırsaktan kana geçip akciğer alveollerine tırmanır (**Loeffler sendromu / eozinofilik pnömoni**), "
            "yutularak tekrar bağırsağa döner ve lümeni tıkayarak ileusa neden olabilir. "
            "3. **Kancalı Kurtlar (Ancylostoma duodenale, Necator americanus):** Larvaları topraktan çıplak ayak derisini delerek girer. "
            "Ağız kapsülleriyle bağırsak mukozasına tutunup günde 0.2 ml kan emerek ağır **mikrositik hipokrom demir eksikliği anemisine** yol açarlar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Enterobius vermicularis kıl kurdu enfeksiyonunun tanısında dışkı incelemesi yetersiz olup altın standart yöntem perianal selofan bant testidir.",
                "selofan bant",
                "Enterobius vermicularis mikroskobik incelemesinde yapışkan şerit uygulaması"
            ),
            make_table(
                ["Nematod Türü", "Bulaşma Mekanizması", "Karakteristik Klinik Belirti"],
                [
                    [
                        "Enterobius vermicularis (Kıl kurdu)",
                        {"text": "Fekal-oral ve otoenfeksiyon", "isMasked": True, "hint": "Tırnak aralarından ağza taşınma"},
                        "Gece artan şiddetli perianal kaşıntı ve uykusuzluk"
                    ],
                    ["Ascaris lumbricoides", "Embriyonlu yumurtaların yutulması", "Akciğerde Loeffler pnömonisi ve bağırsak obstrüksiyonu"],
                    ["Ancylostoma / Necator (Kancalı kurt)", "Topraktan çıplak ayak derisini delme", "Kronik kan kaybına bağlı derin demir eksikliği anemisi"],
                    ["Trichinella spiralis", "Az pişmiş domuz/ayı eti kistleri", "Periorbital ödem, şiddetli kas ağrısı ve aşırı eozinofili"]
                ]
            ),
            make_micro_quiz(
                "Gece uykudan uyandıran şiddetli makat kaşıntısı şikayeti olan 6 yaşındaki bir çocukta kıl kurdu (Enterobius vermicularis) şüphesinde tanı için ilk yapılması gereken işlem nedir?",
                {
                    "A": "Rutin gaita mikroskopisi ile amip kisti aramak",
                    "B": "Sabah dışkılamadan önce perianal bölgeye selofan bant yapıştırıp mikroskopta incelemek",
                    "C": "Kolonoskopi yaparak çekumu görüntülemek",
                    "D": "Kanda parazit spesifik IgM antikorlarına bakmak",
                    "E": "Karın ultrasonografisi çekmek"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; kıl kurdu yumurtaları dışkıya değil perianal cilde bırakılır, gaitada %95 negatiftir.",
                    "B": "B seçeneği doğrudur: Selofan bant yöntemi perianal derideki asimetrik düzleşmiş yumurtaları saptamada altın standarttır.",
                    "C": "C seçeneği gereksiz invazivdir.",
                    "D": "D seçeneği seroloji gerektirmez.",
                    "E": "E seçeneği kıl kurdunu göstermez."
                }
            )
        ]
    })

    # Slayt 38: Helmintler II: Sestodlar (Şeritler / Yassı Solucanlar)
    slides.append({
        "id": "k1-21-s38",
        "title": "Helmintler II: Sestodlar (Şeritler ve Kistler)",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 38,
        "narrative": (
            "Sestodlar (şeritler / tenyalar), yassı, şerit şeklinde, sindirim kanalı bulunmayan (besinleri tegüment yüzeyinden emerler) "
            "ve halkalardan (**proglottid**) oluşan hermafrodit solucanlardır. Baş kısımlarına tutunma organeli olan **skoleks** denir: "
            "1. **Taenia saginata (Sığır Şeriti):** Az pişmiş larvalı (sistiserkus bovis) sığır etlerinin yenmesiyle bulaşır. "
            "İnsan bağırsağında 5-10 metreye ulaşabilir; halkaları anüsten kendiliğinden hareket ederek çıkabilir. Sadece bağırsakta yaşar, kist yapmaz. "
            "2. **Taenia solium (Domuz Şeriti):** İki farklı klinik oluşturur: Az pişmiş domuz etiyle larva alınırsa bağırsakta tenyazis yapar. "
            "Ancak insan T. solium **yumurtasını fekal-oral yolla doğrudan yutarsa**, yumurtadan çıkan larvalar beyne ve göze yerleşerek "
            "epilepsi nöbetleri ve körlükle seyreden ölümcül **Nörosistiserkoz** tablosuna yol açar! "
            "3. **Echinococcus granulosus (Köpek Kisti):** Kesin konağı köpektir. Köpek dışkısıyla atılan yumurtaların insan tarafından yutulmasıyla "
            "karaciğerde (%70) ve akciğerde kist hidatik (**Kistik Ekinokokkoz**) oluşur. "
            "Kist sıvısı patlarsa veya cerrahi sırasında sızarsa öldürücü **anafilaktik şok** tetiklenir!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Köpek dışkısıyla kirlenmiş gıdaların yenmesiyle insanda karaciğer ve akciğerde hidatik kist oluşturan sestod Echinococcus granulosus parazitidir.",
                "Echinococcus granulosus",
                "Hidatidoz etkeni olan küçük köpek tenyası"
            ),
            make_table(
                ["Sestod Türü", "İnsanın Aldığı Bulaş Formu", "İnsanda Gelişen Patolojik Tablo"],
                [
                    ["Taenia saginata", "Az pişmiş sığır etindeki larva (sistiserk)", "Yalnızca lüminal bağırsak tenyazisi (kist yapmaz)"],
                    [
                        "Taenia solium (Yumurta alımı)",
                        {"text": "Fekal-oral yolla T. solium yumurtası", "isMasked": True, "hint": "İnsanın ara konak olduğu ölümcül durum"},
                        "Nörosistiserkoz (Beyinde parazitik kistler ve epilepsi)"
                    ],
                    ["Echinococcus granulosus", "Köpek dışkısından yumurta yutulması", "Karaciğer hidatik kisti, bası ve anafilaksi riski"],
                    ["Diphyllobothrium latum", "Çiğ tatlı su balığı larvaları", "B12 vitamini yarışması sonucu megaloblastik anemi"]
                ]
            ),
            make_micro_quiz(
                "Taenia solium yumurtalarının fekal-oral yolla doğrudan yutulması sonucunda merkezi sinir sisteminde kistik lezyonlar ve epilepsi nöbetleri ile seyreden ağır tablo hangisidir?",
                {
                    "A": "Sistiserkoz (Nörosistiserkoz)",
                    "B": "Kistik ekinokokkoz",
                    "C": "Bağırsak tenyazisi",
                    "D": "Şistozomiyaz",
                    "E": "Trikinoz"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: T. solium yumurtası yutulduğunda larva beyne göç ederek nörosistiserkoz tablosuna yol açar.",
                    "B": "B seçeneği Echinococcus granulosus ile oluşur.",
                    "C": "C seçeneği iyi pişmemiş etle larva yutulunca bağırsakta oluşur.",
                    "D": "D seçeneği trematod enfeksiyonudur.",
                    "E": "E seçeneği çizgili kas kistidir."
                }
            )
        ]
    })

    # Slayt 39: [TEKRAR SAYFASI - CHECKPOINT 4]
    slides.append({
        "id": "k1-21-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Mantarlar ve Parazitler",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 39,
        "narrative": (
            "Bu dördüncü checkpoint sayfasında ökaryotik patojenler dünyasını, "
            "mantar hücre zarındaki ergosterol hedefini, fırsatçı küf ve mayaların (Aspergillus, Kriptokok, Mukor) histopatolojik ayırt edici morfolojilerini, "
            "protozoonlar ile helmintlerin biyolojik çoğalma farkını "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp4-1",
                "Mantar hücre zarı ve hücre duvarının bakterilerden ve insan hücrelerinden temel biyokimyasal farkları nelerdir?",
                "Mantar hücre zarında kolesterol yerine ergosterol bulunur; hücre duvarı ise peptidoglikan içermeyip kitin, glukan ve mannan polisakkaritlerinden yapılmıştır.",
                "Ökaryotik misellerin zar lipidi ile sert dış kabuk dizilimi",
                "Mantar Biyokimyası"
            ),
            make_flashcard(
                "fc-k1-21-cp4-2",
                "Aspergillus fumigatus ile Mucor mantarlarının histopatolojik doku kesitlerindeki hif morfolojisi farkı nedir?",
                "Aspergillus hifleri septalıdır ve 45 derecelik dar/dik açılarla dallanır. Mukor hifleri ise septasızdır (senositik), düzensiz genişliktedir ve 90 derecelik dik açılarla dallanır.",
                "Bölmeli misel kolları ile bölmesiz misel kollarının geometrik çatallanma ayrımı",
                "Fungal Morfoloji"
            ),
            make_flashcard(
                "fc-k1-21-cp4-3",
                "Protozoonlar ile helmintlerin konak içi üreme potansiyeli farkı nedir ve klinik ağırlığı nasıl etkiler?",
                "Protozoonlar konak içinde bölünerek hızla çoğalabilir. Helmintler ise kural olarak konak içinde çoğalamaz; hastalık şiddeti dışarıdan yutulan yumurta veya larva yükü ile belirlenir.",
                "Tek hücreli parazit üremesi ile bağırsak solucanlarının inokulum adedi kaidesi",
                "Parazitoloji İlkeleri"
            )
        ]
    })

    # Slayt 40: Helmintler III: Trematodlar ve Bölüm Özeti
    slides.append({
        "id": "k1-21-s40",
        "title": "Trematodlar (Kelebekler) ve Ökaryotik Patojenler Özeti",
        "section": "Mantarlar ve Parazitler",
        "slideNumber": 40,
        "narrative": (
            "Ökaryotik parazitler alemini tamamlarken yaprak benzeri yassı solucanlar olan **Trematodları (Kelebekler / Flukes)** incelemek gerekir. "
            "Tüm trematodların ilk ara konağı mutlaka tatlı su salyangozlarıdır: "
            "1. **Fasciola hepatica (Karaciğer Kelebeği):** Durgun sularda yetişen yabani su teresi gibi yeşilliklerin yenmesiyle metaserker formunda bulaşır. "
            "Safra yollarına yerleşerek kolanjit, biliyer obstrüksiyon ve karaciğer hasarı yapar. "
            "2. **Schistosoma Türleri (Kan Kelebekleri):** Tatlı suda yüzen serkaryaların deriyi delerek girmesiyle bulaşır (yutulmazlar!). "
            "Erişkin dişiler venöz pleksuslarda yaşar. "
            "**Schistosoma haematobium** mesane venöz pleksusuna yerleşerek terminal hematüriye, mesane kalsifikasyonuna "
            "ve kronik inflamasyon zemininde **Mesanenin Skuamöz Hücreli Karsinomuna (SCC)** yol açan kanıtlanmış bir paraziter kanser etkenidir! "
            "Özetle; ökaryotik patojenler karmaşık hücresel yapıları ve yaşam döngüleriyle tanıda ve tedavide özgün stratejiler gerektirir. "
            "Beşinci bölümümüzde bu enfeksiyonların doğadan insana taşınmasında kilit rol oynayan **vektörleri ve artropodları** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Tatlı sulardan deriyi delerek giren ve mesane venöz pleksusuna yerleşerek mesane skuamöz hücreli karsinomuna yol açan trematod Schistosoma haematobium parazitidir.",
                "Schistosoma haematobium",
                "Mesanede hematüri ve malign karsinom yapan kan kelebeği"
            ),
            make_table(
                ["Trematod Türü", "İnsana Giriş Mekanizması", "Hedef Organ ve Kanser Riski"],
                [
                    ["Fasciola hepatica", "Su teresi / yeşilliklerle metaserker alımı", "Karaciğer parankimi ve safra kanalları (kolanjit)"],
                    [
                        "Schistosoma haematobium",
                        {"text": "Tatlı sularda deriyi delerek serkarya girişi", "isMasked": True, "hint": "Yutulmadan deriden giren kurtçuk"},
                        "Mesane duvarı (Terminal hematüri ve Skuamöz Hücreli Kanser)"
                    ],
                    ["Schistosoma mansoni / japonicum", "Tatlı sudan deriyi delme", "Mezenterik venler, portal hipertansiyon ve hepatosplenomegali"],
                    ["Clonorchis sinensis", "Çiğ tatlı su balığı tüketimi", "Safra yolları (Kolanjiyokarsinom riski)"]
                ]
            ),
            make_micro_quiz(
                "Tatlı su göletinde yüzme öyküsü olan bir hastada ağrısız terminal hematüri saptanıyor. Biyopside yumurtalar çevresinde granülomlar ve mesanede skuamöz hücreli karsinom gelişimi izleniyor. Etken nedir?",
                {
                    "A": "Fasciola hepatica",
                    "B": "Schistosoma haematobium",
                    "C": "Taenia solium",
                    "D": "Ascaris lumbricoides",
                    "E": "Enterobius vermicularis"
                },
                "B",
                {
                    "A": "A seçeneği safra yollarını tutar, mesane kanseri yapmaz.",
                    "B": "B seçeneği doğrudur: Schistosoma haematobium mesane venöz pleksusuna yerleşerek terminal hematüri ve skuamöz hücreli mesane kanserine yol açar.",
                    "C": "C seçeneği sestoddur.",
                    "D": "D seçeneği nematoddur.",
                    "E": "E seçeneği kıl kurdudur."
                }
            )
        ]
    })

    return slides
