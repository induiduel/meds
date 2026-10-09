# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 6: Enfarktüs Dinamikleri: İyileşme, Faktörler ve Septik Enfarktüs (Slayt 51 - 60)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_6_slides():
    slides = []

    # Slayt 51: Enfarktüsün Zamansal Evreleri ve Histopatolojik Sırası
    slides.append({
        "id": "k1-24-s51",
        "title": "Enfarktüsün Zamansal Evreleri ve Histopatolojik Kronolojisi",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 51,
        "narrative": (
            "Enfarktüs alanı zaman içinde son derece düzenli bir hücresel ve histopatolojik evrim geçirir: "
            "1. **İlk 0 - 6 Saat:** Işık mikroskobunda doku tamamen normal görünebilir (klinik MI şüphesinde otopsi tuzağı!). "
            "Elektron mikroskobunda mitokondri kristalarında şişme, glikojen kaybı ve nükleer kromatin kümeleşmesi izlenir. "
            "2. **12 - 24 Saat:** Sitoplazmada yoğun eozinofili (kıpkırmızı boyanma), nükleuslarda piknoz ve "
            "damarlardan nekrotik alana doğru marjinal nötrofil göçü başlar. "
            "3. **1 - 3 Gün:** Koagülatif nekroz zirveye ulaşır; nükleuslar kaybolur (karyolizis), doku iskeleti korunmuş hayalet hücreler izlenir. "
            "Alanı yoğun bir nötrofilik infiltrasyon sarar. "
            "4. **3 - 7 Gün:** Nötrofiller apoptozla ölür; sahaya makrofajlar girerek ölü hücre enkazını fagosite etmeye başlar. "
            "5. **1 - 2 Hafta:** Nekroz kenarlarından bol kapiller damarlar ve fibroblastlar içeren **granülasyon dokusu** alana hücum eder. "
            "6. **Haftalar - Aylar:** Granülasyon dokusu yerini yoğun kollajen birikimine bırakarak **kalıcı asellüler fibröz skara** dönüşür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Enfarktüsün histopatolojik seyrinde üçüncü günden sonra nötrofillerin yerini alarak nekrotik doku enkazını fagosite eden primer hücreler makrofajlardır.",
                "makrofajlardır",
                "Ölü hücre artıklarını temizleyen mononükleer fagositik hücreler"
            ),
            make_table(
                "Miyokard ve Solid Organ Enfarktüsünde Histopatolojik Kronoloji",
                ["Zaman Penceresi", "Baskın Hücresel Yanıt", "Histopatolojik Görünüm"],
                [
                    ["0 - 12 Saat", "Mikroskobik olarak sessiz", "Dalgalı miyosit lifleri, hafif ödem"],
                    ["12 - 24 Saat", "İlk nötrofil infiltrasyonu", "Koagülatif nekroz başlangıcı, kontraksiyon bantları"],
                    [
                        "1 - 3 Gün",
                        "Yoğun nötrofilik lökosit infiltrasyonu",
                        {"text": "Tam koagülatif nekroz ve nükleus kaybı (karyolizis)", "isMasked": True, "hint": "Hayalet hücrelerin belirginleştiği pik evre"}
                    ],
                    ["3 - 7 Gün", "Makrofaj fagositozu", "Ölü doku rezorpsiyonu, yumuşama"],
                    ["1 - 2 Hafta", "Granülasyon dokusu (Damarlar + Fibroblastlar)", "Kollajen sentezi ve neovaskülarizasyon"],
                    ["> 2 Ay", "Asellüler dens kollajen skar", "Kalıcı beyaz fibröz doku"]
                ]
            ),
            make_micro_quiz(
                "Akut miyokard enfarktüsü geçiren bir hastada göğüs ağrısı başladıktan 2 saat sonra hasta kaybedilmiş ve acil otopsi yapılmıştır. Kalbin ışık mikroskobik incelemesinde miyositlerde belirgin bir nekroz bulgusunun izlenmemesinin nedeni hangisidir?",
                {
                    "A": "Işık mikroskobunda koagülatif nekroz bulgularının (eozinofili, nükleus kaybı) belirginleşmesi için en az 4-12 saatlik bir sürenin gerekmesi",
                    "B": "Hastanın aslında enfarktüs geçirmemiş olması",
                    "C": "Kalp kasının iskemiden hiçbir zaman etkilenmemesi",
                    "D": "Enfarktüsün yalnızca elektron mikroskobunda tanı alabilen bir klinik sendrom olması",
                    "E": "Tüm nekrozların ilk 2 saatte fibröz skara dönüşmesi"
                },
                "A",
                {
                    "A": "Işık mikroskobunda iskemik nekrozun morfolojik olarak görünür hale gelmesi için minimum 4-6 saat (genellikle 12 saat) gerekir.",
                    "B": "2 saatte MI gerçekleşmiştir fakat ışık mikroskobunda erken evredir.",
                    "C": "Kalp kası iskemiye çok duyarlıdır (20 dakikada ölür).",
                    "D": "Işık mikroskobunda 12 saat sonra net görünür.",
                    "E": "Skar aylar sonra oluşur."
                }
            )
        ]
    })

    # Slayt 52: Enfarktüs İyileşmesi ve Fibröz Skar Oluşumu
    slides.append({
        "id": "k1-24-s52",
        "title": "Enfarktüs İyileşmesi: Rejenerasyon Sınırları ve Fibröz Skar",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 52,
        "narrative": (
            "Enfarktüs alanının nihai akıbeti dokunun hücresel rejenerasyon kapasitesine ve parankimal iskeletin durumuna bağlıdır: "
            "1. **Kalıcı (Permanent) Hücreler:** Kalp kası hücreleri (kardiyomiyositler) ve nöronlar mitoz yeteneğini doğumdan sonra kaybetmiştir. "
            "Bu dokularda bir kez enfarktüs geliştiğinde hücreler kendini kopyalayarak yenileyemez; "
            "iyileşme **tamamen fibröz skar dokusu (bağ dokusu tamiri)** ile gerçekleşir. "
            "2. **Stabil Hücreler ve Stroma Yıkımı:** Karaciğer ve böbrek gibi dokular bölünme potansiyeline sahip stabil hücreler içerir. "
            "Ancak enfarktüs sırasında yalnızca hücreler değil, hücrelerin tutunduğu **hücre dışı matris ve bazal membran iskeleti de koagüle olarak ölür**. "
            "Rejenerasyon için bir kılavuz iskelet kalmadığından, bu organlarda da enfarktüsler rejenerasyonla değil, "
            "fibroblastların kollajen sentezlemesiyle oluşan **dens fibröz skar** ile sonlanır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Kardiyomiyositlerin bölünme yeteneğinin bulunmaması ve hücre dışı matriks iskeletinin koagüle olması nedeniyle miyokard enfarktüsü daima fibröz skar dokusu ile iyileşir.",
                "fibröz skar dokusu",
                "Kas kaybı alanını dolduran kalıcı bağ dokusu tamiri"
            ),
            make_table(
                "Doku Hücre Tipleri ve Enfarktüs Sonrası İyileşme Yanıtı",
                ["Hücre / Doku Tipi", "Mitoz Yeteneği", "Enfarktüsteki Yanıtı", "Nihai İyileşme Dokusu"],
                [
                    ["Kalıcı (Kardiyomiyosit)", "Yok (Kalıcı post-mitotik)", "Hücreler bölünemez, boşluğu bağ dokusu doldurur", "Kollajenöz Fibröz Skar"],
                    [
                        "Kalıcı (Serebral Nöron)",
                        "Yok",
                        {"text": "Sıvılaşma nekrozu ve doku erimesi", "isMasked": True, "hint": "Beyinde doku kaybının kavitasyonla sonuçlanması"},
                        "Kistik Kavite + Astrositik Gliozis"
                    ],
                    ["Stabil (Böbrek Tübülü)", "Var (ancak stroma nekroze)", "İskelet yıkıldığı için parankim organize olamaz", "Çökük Fibröz Renal Skar"]
                ]
            ),
            make_micro_quiz(
                "Böbrek tübül epitel hücreleri normalde replike olma (mitoz) yeteneğine sahip stabil hücreler olmasına rağmen, böbrek enfarktüsü alanının tübüler rejenerasyon yerine fibröz skar dokusu ile iyileşmesinin temel nedeni hangisidir?",
                {
                    "A": "Enfarktüs sırasında hücrelerin yanı sıra hücre dışı matris ve bazal membran iskeletinin de tamamen nekroze olması",
                    "B": "Böbreğe gelen kan akımının ömür boyu sıfırlanması",
                    "C": "İdrarın fibroblastları doğrudan öldürmesi",
                    "D": "Glomerüllerin bağ dokusuna dönüşmesi",
                    "E": "Tübüllerin yalnızca embriyonik dönemde bölünebilmesi"
                },
                "A",
                {
                    "A": "Organize rejenerasyon için bazal membran çatısının korunması şarttır; enfarktüste stroma da koagüle olduğundan skar oluşur.",
                    "B": "Kan akımı çevre sağlam dokuda devam eder.",
                    "C": "İdrar enfarkt alanında birikmez.",
                    "D": "Glomerüller skarla büzüşür.",
                    "E": "Tübüller erişkinde de bölünebilir (ör. ATN'de iyileşir)."
                }
            )
        ]
    })

    # Slayt 53: Böbrek ve Dalak Enfarktlarında İyileşme: Çökük Skar
    slides.append({
        "id": "k1-24-s53",
        "title": "Böbrek ve Dalak Enfarktlarında İyileşme: Çökük Fibrotik Skar Morfolojisi",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 53,
        "narrative": (
            "Katı organlarda iyileşen enfarktüsler, makroskobik olarak organ yüzeyinde kalıcı deformiteler yaratır: "
            "1. **Kollajen Büzüşmesi (Kontraksiyon):** "
            "Granülasyon dokusundaki miyofibroblastlar ve tip I kollajen lifleri aylar içinde organize olurken büzüşür (kontraksiyon). "
            "Bu durum taze enfarktüsteki hafif şişkin alanın zamanla hacim kaybederek içeri çökmesine yol açar. "
            "2. **Böbrekte Çökük Skar:** "
            "Eski bir renal enfarktüs, böbrek korteksinde **V şeklinde, tabanı kapsülde olan derin, soluk beyaz-gri renkli çökük bir skar** bırakır. "
            "Böbrek dış yüzeyi düzgün konturunu kaybeder, çentikli bir görünüm alır (arteriosklerotik skar ile karışabilir). "
            "3. **Dalakta Skar:** Dalağın kapsül yüzeyinde beyazımsı fibröz çekintiler ve yapışıklıklar kalır. "
            "Mikroskopide nekrotik glomerül ve tübüllerin yerinde asellüler hyalinize kollajen kitleleri izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İyileşen eski bir böbrek enfarktüsü, organ kapsülünde içeriye doğru derin bir çöküntü oluşturan beyaz-gri renkli çökük fibrotik skar bırakır.",
                "çökük fibrotik skar",
                "Kollajen büzüşmesiyle organ yüzeyinde oluşan karakteristik çentikli iz"
            ),
            make_table(
                "Taze ve Eski Böbrek Enfarktüsü Karşılaştırması",
                ["Özellik", "Taze Renal Enfarktüs (1-3 Gün)", "Eski İyileşmiş Renal Enfarktüs (>2 Ay)"],
                [
                    ["Yüzey Seviyesi", "Organ yüzeyinden hafif kabarık / şişkin", "Kapsülden içeriye doğru belirgin çökük"],
                    ["Renk", "Sarımsı-beyaz, etrafı kırmızı hiperemik halkalı", "Soluk beyaz-gri, homojen mat fibröz"],
                    [
                        "Histopatoloji",
                        "Koagülatif nekroz ve hayalet tübüller",
                        {"text": "Asellüler yoğun kollajen skar dokusu", "isMasked": True, "hint": "Kalıcı hyalinize bağ dokusu çatısı"}
                    ]
                ]
            ),
            make_micro_quiz(
                "Hipertansiyon ve ateroskleroz öyküsü olan 65 yaşındaki bir hastanın otopsisinde, böbrek dış yüzeyinde kortekse doğru derin çentikler oluşturan V şeklinde, sert, soluk beyaz-gri çökük alanlar saptanmıştır. Bu lezyonların en olası patolojik kökeni hangisidir?",
                {
                    "A": "Eski iyileşmiş renal enfarktüs skarları",
                    "B": "Akut glomerülonefrit kresentleri",
                    "C": "Primer amiloid birikimi",
                    "D": "Konjenital böbrek hipoplazisi",
                    "E": "Tüberküloz kazeifikasyon odakları"
                },
                "A",
                {
                    "A": "V şeklinde, kapsülden içeri çökük sert beyaz alanlar eski iyileşmiş enfarktüsün klasik kollajenöz skarlarıdır.",
                    "B": "Kresentler mikroskobiktir, kortekste derin çentik yapmaz.",
                    "C": "Amiloid böbreği büyütür ve mumsu yapar.",
                    "D": "Hipoplazide tüm böbrek küçüktür.",
                    "E": "Tüberküloz kavitasyon ve kazeifikasyon yapar."
                }
            )
        ]
    })

    # Slayt 54: Beyin Enfarktında Farklılık: Kavitasyon ve Gliozis
    slides.append({
        "id": "k1-24-s54",
        "title": "Beyin Enfarktında Farklılık: Kavitasyon, Gitter Hücreleri ve Gliozis",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 54,
        "narrative": (
            "Santral sinir sisteminde enfarktüs iyileşmesi insan vücudundaki tüm dokulardan radikal biçimde ayrılır: "
            "1. **Sıvılaşma ve Fagositoz:** Beyin parankiminde arter tıkanmasıyla gelişen sıvılaşma nekrozu sonrası, "
            "sahaya kan monositlerinden köken alan **lipid yüklü köpüksü makrofajlar (Gitter hücreleri / Fagositik mikroglia)** girer. "
            "Miyelin ve nöron artıklarını tamamen sindirip temizlerler. "
            "2. **Kistik Kavitasyon Oluşumu:** Beyin parankiminde bağ dokusu ve fibroblast bulunmadığından fibröz doku sentezlenemez! "
            "Eriyen parankimin yerinde içinde berrak beyin-omurilik sıvısına benzer sıvı bulunan **kistik bir boşluk (kavitasyon)** kalır. "
            "3. **Astrositik Gliozis (Beynin Skarı):** "
            "Kistik kavitenin kenarlarındaki reaktif astrositler prolifere olur (gemistositik astrositler) ve "
            "sitoplazmik uzantılarıyla yoğun bir ağ örerek kistin etrafını sınırlar. "
            "Bu sürece **Gliozis** adı verilir ve beynin kollajenöz skara verdiği yegane hücresel tamir karşılığıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Beyin enfarktüsünde sıvılaşan nekrotik alanın makrofajlarca temizlenmesi sonrası kistin etrafında astrositlerin proliferasyonu ile oluşan tamir dokusuna gliozis adı verilir.",
                "gliozis",
                "Santral sinir sisteminde astrositlerin oluşturduğu hücresel skar"
            ),
            make_table(
                "Beyin Enfarktüsü İyileşme Evreleri ve Hücresel Aktörler",
                ["Evre / Zaman", "Baskın Hücresel Eleman", "Patolojik Görünüm"],
                [
                    ["Akut Evre (1-3 Gün)", "Nöronlarda kırmızılık (kırmızı nöron)", "Ödem, parankimde yumuşama"],
                    [
                        "Subakut Evre (1-3 Hafta)",
                        "Lipid yüklü makrofajlar (Gitter hücreleri)",
                        {"text": "Sıvılaşma nekrozunun fagositozla eritilip boşaltılması", "isMasked": True, "hint": "Köpüksü makrofajların lipidleri temizlemesi"}
                    ],
                    ["Kronik Evre (>Ay)", "Prolifere reaktif astrositler", "Sıvı dolu kistik kavitasyon ve çevresel gliozis"]
                ]
            ),
            make_micro_quiz(
                "İskemik inme geçiren ve 1 yıl sonra başka bir nedenden ölen bir hastanın beyin otopsisinde eski enfarktüs alanında saptanması beklenen karakteristik patolojik lezyon hangisidir?",
                {
                    "A": "İçinde berrak sıvı bulunan ve çevresi astrositik gliozis ile sınırlanmış kistik kavitasyon",
                    "B": "Yoğun tip I kollajenden zengin asellüler fibröz skar",
                    "C": "Kalsifiye taşlaşmış osteoid adacıkları",
                    "D": "Kazeifiye granülomatöz tüberkülom",
                    "E": "Taze eritrositlerle dolu hematom kesesi"
                },
                "A",
                {
                    "A": "Eski beyin enfarktüsü fibroblast içermediğinden kavitasyon (kist) ve astrositik gliozis ile iyileşir.",
                    "B": "Kollajen skar kalpte ve böbrekte olur, beyinde fibroblast yoktur.",
                    "C": "Beyinde kemikleşme olmaz.",
                    "D": "Tüberkülom tüberküloz lezyonudur.",
                    "E": "Hematom taze kanamadır."
                }
            )
        ]
    })

    # Slayt 55: Septik Enfarktüs Patogenezi: İnfekte Tromboemboli ve Apseleşme
    slides.append({
        "id": "k1-24-s55",
        "title": "Septik Enfarktüs Patogenezi: İnfekte Tromboemboli ve Apseleşme",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 55,
        "narrative": (
            "Enfarktüsler bakteriyel veya fungal enfeksiyonla kontamine olduğunda seyir radikal biçimde ağırlaşır: "
            "1. **Septik Enfarktüs Tanımı:** İskemik nekroz alanının canlı mikroorganizmalar içermesi tablosudur. "
            "2. **Oluşum Mekanizmaları:** "
            "- **En Sık Mekanizma:** İnfektif endokardit kapak vejetasyonundan kopan bir bakteriyel pıhtının bir organ arterini tıkaması (**septik emboli**). "
            "- **Sekonder Kolonizasyon:** Aseptik bir enfarktüs alanına, bakteriyemi sırasında kandan mikropların yerleşmesi. "
            "3. **Apseleşme Kaskadı:** "
            "İskemik koagülatif nekroz alanı bakteriler için ideal bir kültür ortamıdır. "
            "Bakteriyel toksinler ve bölgeye hücum eden milyonlarca nötrofilin litik enzimleri, "
            "katı koagülatif nekrozu hızla eriterek **irin dolu bir metastatik apseye** dönüştürür. "
            "4. **Klinik Komplikasyonlar:** Apse organ kapsülünü eriterek rüptüre olabilir (böbrek veya dalak rüptürü), "
            "damar duvarını eriterek **mikotik anevrizma** ve ölümcül kanamalara yol açabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İnfektif endokardit vejetasyonundan kopan bakteriyel pıhtının dokuda koagülatif nekrozla birlikte yoğun süpüratif erime yapmasıyla septik enfarktüs ve apse gelişir.",
                "septik enfarktüs",
                "Bakteriyel embolizasyon sonucu dokuda püy oluşumuyla seyreden enfarkt"
            ),
            make_table(
                "Aseptik ve Septik Enfarktüs Karşılaştırma Matrisi",
                ["Özellik", "Aseptik (Steril) Enfarktüs", "Septik Enfarktüs"],
                [
                    ["Mikrobiyal İçerik", "Tamamen sterildir", "Canlı bakteri veya mantar kolonileri içerir"],
                    ["En Sık Kaynak", "Aterom plağı veya sol ventrikül mural trombüsü", "İnfektif endokardit kapak vejetasyonu"],
                    [
                        "Lezyon Morfolojisi",
                        "Katı koagülatif nekroz ve fibröz skar",
                        {"text": "Süpüratif doku erimesi ve metastatik apse formasyonu", "isMasked": True, "hint": "Nötrofil enzimleriyle irinleşen nekroz alanı"}
                    ],
                    ["Vasküler Komplikasyon", "Skar kontraksiyonu", "Damar duvarının erimesiyle Mikotik Anevrizma"]
                ]
            ),
            make_micro_quiz(
                "Aort kapak endokarditi olan bir hastada sağ böbrekte kama şeklinde bir enfarktüs gelişmiş ve 4 gün sonra lezyon alanının eriyerek sarı-yeşil renkli pürülan bir sıvı içerdiği (apseye dönüştüğü) saptanmıştır. Bu lezyonun patolojik tanımı hangisidir?",
                {
                    "A": "Septik Enfarktüs",
                    "B": "Aseptik Anemik Enfarktüs",
                    "C": "Kırmızı Hemorajik Enfarktüs",
                    "D": "Kazeifiye Granülom",
                    "E": "Basit Renal Kortikal Kist"
                },
                "A",
                {
                    "A": "Bakteriyel vejetasyondan köken alan enfarktüsün apseleşmesi septik enfarktüsün prototipidir.",
                    "B": "Aseptik enfarktüste püy ve apseleşme olmaz.",
                    "C": "Kırmızı enfarktüs kanamalıdır, pürülan apse içermez.",
                    "D": "Kazeifiye granülom tüberkülozdur.",
                    "E": "Renal kist benign sıvı kistidir."
                }
            )
        ]
    })

    # Slayt 56: Enfarkt Gelişimini Etkileyen Faktör I: Vasküler Anatomi
    slides.append({
        "id": "k1-24-s56",
        "title": "Enfarkt Gelişimini Etkileyen Faktör I: Vasküler Dolaşım Mimarisi",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 56,
        "narrative": (
            "Bir arter tıkandığında enfarktüs gelişip gelişmeyeceğini belirleyen en kritik faktör o organın alternatif kanlanma yollarıdır: "
            "1. **Çift Kan Dolaşımına Sahip Organlar (Enfarktüs Riski Düşük):** "
            "- **Akciğer:** Pulmoner ve bronşiyal arterler paralel kan akımı sağlar; bir dal tıkansa diğeri parankimi besler. "
            "- **Karaciğer:** Hepatik arter ve Vena Portae olmak üzere iki dev giriş yolu vardır; hepatik arter ligasyonu bile karaciğeri nekroza uğratmaz. "
            "- **Ön Kol ve El:** Arteria radialis ve arteria ulnaris zengin palmar arklarla birbirine bağlıdır; Allen testi bu kollaterali gösterir. "
            "- **İnce Bağırsak:** Mezenterik vasküler arklar zengin anastomozlara sahiptir. "
            "2. **Uç Arter (Terminal) Dolaşımlı Organlar (Enfarktüs Riski Çok Yüksek):** "
            "- **Böbrek:** İnterlober ve arkuat arterler arasında hiçbir anastomoz yoktur; tıkanma kaçınılmaz nekroz yapar. "
            "- **Dalak:** Splenik arter dalları terminaldir. "
            "- **Retina:** Santral retinal arter tıkanması ani kalıcı körlükle sonlanır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Karaciğer dokusu hepatik arter ve vena portae olmak üzere çift kan dolaşımına sahip olduğundan arteriyel tıkanmalarda enfarktüs gelişme riski son derece düşüktür.",
                "çift kan dolaşımına",
                "Karaciğer ve akciğeri iskemiye karşı koruyan iki ayrı vasküler giriş mekanizması"
            ),
            make_table(
                "Vasküler Anatomiye Göre Enfarktüs Risk Dağılımı",
                ["Anatomik Dolaşım Tipi", "Temsilci Organlar", "Enfarktüs Gelişme Riski", "Fizyopatolojik Gerekçe"],
                [
                    ["Çift Arteriyel Giriş", "Akciğer (Pulmoner + Bronşiyal)", "Düşük (Kalp sağlamsa)", "Alternatif sistemin parankimi beslemeyi sürdürmesi"],
                    ["Çift Giriş (Arter + Ven)", "Karaciğer (Hepatik Arter + Portal Ven)", "Çok Düşük", "Portal kanın oksijen ihtiyacının yarısını karşılaması"],
                    ["Zengin Arklar", "El (Radial + Ulnar ark)", "Düşük", "Palmar arkların zengin kollateral desteği"],
                    [
                        "Uç Arter (Anastomozsuz)",
                        "Böbrek, Dalak, Retina",
                        {"text": "Çok Yüksek (Kaçınılmaz Enfarktüs)", "isMasked": True, "hint": "Alternatif kollateral yolu bulunmayan terminal dolaşım"},
                        "Tıkanan damarın beslediği alana başka hiçbir kan girişinin olmaması"
                    ]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki organlardan hangisinde bir ana arter dalının trombozla aniden tıkanması durumunda çift kan dolaşımı veya zengin vasküler arklar nedeniyle enfarktüs gelişme olasılığı DİĞERLERİNE GÖRE ÇOK DAHA DÜŞÜKTÜR?",
                {
                    "A": "Karaciğer (Hepatik arter ve Portal ven çift dolaşımı)",
                    "B": "Böbrek korteksi",
                    "C": "Dalak parankimi",
                    "D": "Retina santral arteri",
                    "E": "Miyokard sol ventrikül duvarı"
                },
                "A",
                {
                    "A": "Karaciğer hepatik arter ve portal ven çift kan dolaşımına sahiptir; arter tıkansa bile portal kan oksijen sağlayarak enfarktüsü engeller.",
                    "B": "Böbrek uç arterdir, hızla enfarktüse gider.",
                    "C": "Dalak uç arterdir.",
                    "D": "Retina uç arterdir.",
                    "E": "Miyokard fonksiyonel uç arterdir."
                }
            )
        ]
    })

    # Slayt 57: Enfarkt Gelişimini Etkileyen Faktör II: Tıkanma Hızı ve Kollateral
    slides.append({
        "id": "k1-24-s57",
        "title": "Enfarkt Gelişimini Etkileyen Faktör II: Tıkanma Hızı ve Kollateral Gelişimi",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 57,
        "narrative": (
            "Damar tıkanmasının zamansal hızı doku canlılığının kaderini tayin eder: "
            "1. **Yavaş Gelişen Tıkanma (Kronik Ateroskleroz):** "
            "Bir arter aterom plağı ile aylar ve yıllar içinde yavaş yavaş daraldığında, "
            "dokuda kronik hafif iskemi oluşur. Bu iskemi **HIF-1alfa ve VEGF (Vasküler Endotelyal Büyüme Faktörü)** salınımını uyarır. "
            "Daralan damarın etrafındaki komşu küçük kapillerler genişler, hipertrofiye uğrar ve **yeni kollateral damar anastomozları (arteriogenez)** gelişir. "
            "Yıllar sonra ana damar %100 tıkandığında dahi bu kollateraller dokuyu besleyerek enfarktüsü tamamen engelleyebilir! "
            "2. **Ani Tıkanma (Akut Tromboemboli / Plak Rüptürü):** "
            "Saniyeler veya dakikalar içinde damar lümeni sıfırlandığında, kollateral damarların genişlemesine veya gelişmesine zaman kalmaz. "
            "Doku aniden kansız kalır ve kaçınılmaz olarak masif enfarktüs gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Kronik aterosklerozda yavaş gelişen darlıklar sırasında dokunun iskemiye yanıt olarak kollateral damar geliştirmesi ani tam tıkanmalarda enfarktüs oluşmasını engelleyebilir.",
                "kollateral damar",
                "İskemik dokuya alternatif kan akımı sağlayan yan damar ağı"
            ),
            make_before_after(
                "Koroner Arterin Yavaş Daralması ile Ani Tıkanması Arasındaki İskemik Sonuç",
                "Yıllar Süren Yavaş Darlık: VEGF uyarısıyla zengin kollateral damar köprüleri oluşur; damar tam tıkandığında dahi hasta enfarktüs geçirmeyebilir.",
                "Ani Akut Emboli / Plak Rüptürü: Kollateral gelişmeye zaman kalmaz; miyokard dakikalar içinde transmural koagülatif nekroza (akut MI) uğrar."
            ),
            make_micro_quiz(
                "Yetmiş yaşında ileri derecede koroner aterosklerozu olan bir hastada Sol Ön İnen (LAD) arterin %100 tıkalı olduğu anjiyografide saptanmış ancak hastada hiçbir miyokard enfarktüsü alanı izlenmemiştir. Bu koruyucu klinik tabloyu açıklayan temel fizyopatolojik mekanizma hangisidir?",
                {
                    "A": "Darlığın yıllar içinde yavaş gelişmesi sayesinde sirkumfleks ve sağ koronerden zengin kollateral damarların gelişmiş olması",
                    "B": "Hastanın kalp kası hücrelerinin oksijene ihtiyaç duymaması",
                    "C": "LAD arterinin kalbi beslemeyen gereksiz bir damar olması",
                    "D": "Kalp kasının doğrudan perikard sıvısından oksijen alması",
                    "E": "Tıkanıklığın arteriyel değil venöz sistemde olması"
                },
                "A",
                {
                    "A": "Yavaş oklüzyon kollateral damar ağı geliştirerek dokuyu tam tıkanmada bile enfarktüsten korur.",
                    "B": "Miyositler oksijensiz yaşayamaz.",
                    "C": "LAD sol ventrikülün en kritik besleyici arteridir.",
                    "D": "Perikard sıvısı difüzyonla miyokardı besleyemez.",
                    "E": "LAD primer ana koroner arterdir."
                }
            )
        ]
    })

    # Slayt 58: Enfarkt Gelişimini Etkileyen Faktör III: Doku Hipoksi Duyarlılığı
    slides.append({
        "id": "k1-24-s58",
        "title": "Enfarkt Gelişimini Etkileyen Faktör III: Doku Hipoksi Duyarlılığı",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 58,
        "narrative": (
            "İnsan vücudundaki farklı hücre tipleri hipoksiye ve iskemiye karşı son derece farklı biyolojik tolerans sürelerine sahiptir: "
            "1. **En Hassas Hücreler: NÖRONLAR (3 - 4 Dakika!):** "
            "Santral sinir sistemi nöronları neredeyse hiç glikojen depolamaz ve enerji için tamamen sürekli glukoz/oksijen perfüzyonuna bağımlıdır. "
            "Kan akımı kesildikten **3 - 4 dakika sonra nöronlarda geri dönüşümsüz iskemik hasar ve ölüm** başlar. "
            "2. **Miyokard Hücreleri (20 - 30 Dakika):** "
            "Kalp kası hücreleri kandan oksijen kesildikten sonra 20-30 dakika boyunca canlı kalabilir; "
            "ilk 20-30 dakikada yapılan anjiyoplasti/trombolitik müdahale miyositleri nekrozdan kurtarır (altın saat!). "
            "3. **Böbrek Proksimal Tübül Epiteli:** Yüksek metabolik aktif taşıma nedeniyle **20 - 30 dakika** iskemiye dayanabilir. "
            "4. **İskelet Kası ve Karaciğer:** Birkaç saat boyunca iskemik hasara direnç gösterebilir. "
            "5. **En Dirençli Hücreler: FİBROBLASTLAR ve Bağ Dokusu:** Düşük metabolik hızları sayesinde **saatlerce ve günlerce** canlı kalabilirler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Santral sinir sistemi nöronları kandan oksijen kesilmesine karşı en duyarlı hücreler olup üç ile dört dakika içinde geri dönüşümsüz iskemik nekroza uğrar.",
                "üç ile dört dakika",
                "Nöronların oksijensizliğe dayanabildiği kritik dakika süresi"
            ),
            make_table(
                "Hücre Tiplerinin İskemiye Dayanma Süreleri Hiyerarşisi",
                ["Hücre / Doku Tipi", "Geri Dönüşümsüz Nekroza Giriş Süresi", "Metabolik Neden"],
                [
                    [
                        "Beyin Nöronları",
                        {"text": "3 - 4 Dakika (En hassas)", "isMasked": True, "hint": "Oksijen kesintisinde ilk ölen hücre grubu"},
                        "Glikojen deposu yok, mutlak oksidatif fosforilasyon bağımlılığı"
                    ],
                    ["Kardiyomiyositler (Kalp Kası)", "20 - 30 Dakika", "Yüksek ATP tüketimi, kreatin kinaz tükenmesi"],
                    ["Böbrek Tübül Epiteli", "~20 - 30 Dakika", "Yoğun Na/K ATPaz pompası enerji gereksinimi"],
                    ["İskelet Kası", "2 - 4 Saat", "Glikojen depoları ve anaerobik glikoliz kapasitesi"],
                    ["Fibroblastlar (Bağ Dokusu)", "Saatler - Günler (En dirençli)", "Minimal metabolik hız ve dayanıklı hücresel yapı"]
                ]
            ),
            make_micro_quiz(
                "Kardiyak arrest (kalp durması) geçiren ve başarılı resüsitasyonla kalbi yeniden çalıştırılan bir hastada, en kısa sürede (3-4 dakika içinde) geri dönüşümsüz iskemik hasara uğrayarak nörolojik sekellere yol açan primer hücre tipi hangisidir?",
                {
                    "A": "Serebral Nöronlar",
                    "B": "Kardiyomiyositler",
                    "C": "Vasküler endotel hücreleri",
                    "D": "Deri fibroblastları",
                    "E": "Kemik osteositleri"
                },
                "A",
                {
                    "A": "Nöronlar glikojen depolamadığından 3-4 dakika içinde geri dönüşümsüz ölür.",
                    "B": "Miyositler 20-30 dakika dayanır.",
                    "C": "Endotel nöronlardan daha dirençlidir.",
                    "D": "Fibroblastlar saatlerce dayanabilir.",
                    "E": "Osteositler saatlerce canlı kalabilir."
                }
            )
        ]
    })

    # Slayt 59: [TEKRAR SAYFASI - CHECKPOINT 6] Enfarkt İyileşmesi, Doku Duyarlılığı ve Septik Enfarktüs
    slides.append({
        "id": "k1-24-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Enfarkt İyileşmesi, Doku Duyarlılığı ve Septik Enfarktüs",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 59,
        "narrative": (
            "Bu altıncı checkpoint sayfasında, enfarktüs iyileşmesini, etkileyen faktörleri ve septik enfarktüsü özetliyoruz: "
            "1. **Zamansal Sıra:** 0-6 saat mikroskobik sessiz; 1-3 gün tam koagülatif nekroz ve nötrofiller; "
            "3-7 gün makrofaj fagositozu; 1-2 hafta granülasyon dokusu; aylar sonra kollajen skar. "
            "2. **Beyin İstisnası:** Beyinde fibroblast olmadığından skar dokusu oluşmaz; nekroz sıvılaşır, "
            "geride KİSTİK KAVİTASYON kalır ve etrafını ASTROSİTİK GLİOZİS sarar. "
            "3. **Septik Enfarktüs:** İnfektif endokardit embolisi gibi mikrobiyal pıhtılarda nekroz alanı eriyerek APSEYE dönüşür; mikotik anevrizma riski doğar. "
            "4. **Çift Dolaşım Koruyucudur:** Akciğer, karaciğer ve ön kolda çift kanlanma enfarktüsü engeller; böbrek ve dalak uç arterdir. "
            "5. **Tıkanma Hızı:** Yavaş darlık kollateral açar (VEGF); ani tıkanma masif enfarktüs yapar. "
            "6. **Hipoksi Duyarlılığı:** Nöronlar 3-4 DAKİKADA, miyokard 20-30 DAKİKADA ölür; fibroblastlar saatlerce dirençlidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s59-1",
                "Beyin dokusunda gelişen iskemik enfarktüsün iyileşmesi sürecinde kollajen skar yerine kistik boşluk çevresinde oluşan astrositer tamir dokusuna ne ad verilir?",
                "Gliozis dokusu adı verilir.",
                "Serebral parankimde astrositlerin çoğalarak kist çeperini örmesi",
                "Serebral İyileşme"
            ),
            make_flashcard(
                "k1-24-fc-s59-2",
                "Vücut dokuları arasında oksijen kesintisine en duyarlı olan ve üç ile dört dakika içinde geri dönüşümsüz iskemik nekroza giren hücre grubu hangisidir?",
                "Santral sinir sistemi nöronlarıdır.",
                "Beyin korteksindeki gri cevher elektroaktif hücreleri",
                "Doku Duyarlılığı"
            ),
            make_flashcard(
                "k1-24-fc-s59-3",
                "İnfektif endokardit vejetasyonlarından kopan bir pıhtının dokuda koagülatif nekroz yerine yoğun nötrofilik püy içeren bir kaviteye dönüşmesi tablosuna ne ad verilir?",
                "Septik enfarktüs ve apseleşmedir.",
                "Canlı bakteri taşıyan embolusların dokuda başlattığı süpüratif erime",
                "Septik Enfarktüs"
            )
        ],
        "interactiveElements": [
            make_table(
                "Enfarktüs İyileşme Dinamikleri Özet Tablosu",
                ["Patolojik Süreç", "Temel Hücresel Aktör", "Nihai Morfolojik Sonuç"],
                [
                    ["Solid Organ Tamiri (Kalp/Böbrek)", "Fibroblastlar ve tip I kollajen", "Asellüler büzüşmüş fibröz skar"],
                    ["Serebral Doku Tamiri (Beyin)", "Köpüksü makrofajlar ve reaktif astrositler", "Sıvı dolu kavitasyon ve çevresel gliozis"],
                    [
                        "Septik Enfarktüs Evrimi",
                        "Bakteriler ve yoğun nötrofiller",
                        {"text": "Doku destrüksiyonu ve metastatik apse", "isMasked": True, "hint": "Süpüratif nekroz ve mikotik anevrizma riski"}
                    ]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki hücresel tolerans ve enfarktüs ifadelerinden hangisi YANLIŞTIR?",
                {
                    "A": "Miyokard hücreleri iskemiden sonra 20-30 dakika içinde canlılığını yitirmeye başlar",
                    "B": "Santral sinir sistemi nöronları 3-4 dakika içinde geri dönüşümsüz nekroza girer",
                    "C": "Fibroblastlar iskemiye nöronlardan çok daha dirençlidir ve saatlerce canlı kalabilir",
                    "D": "Beyin enfarktüsleri iyileşirken yoğun kollajen lifleri içeren kalın bir fibröz skar oluşturur",
                    "E": "Karaciğer çift kan dolaşımına sahip olduğu için arteriyel enfarktüs riski düşüktür"
                },
                "D",
                {
                    "A": "Doğrudur; miyokard 20-30 dakika dayanır.",
                    "B": "Doğrudur; nöronlar 3-4 dakikada ölür.",
                    "C": "Doğrudur; fibroblastlar çok dirençlidir.",
                    "D": "YANLIŞTIR; Beyin dokusunda fibroblast bulunmaz! İyileşme kollajen skar ile DEĞİL, kistik kavitasyon ve ASTROSİTİK GLİOZİS ile gerçekleşir.",
                    "E": "Doğrudur; karaciğer çift dolaşımlıdır."
                }
            )
        ]
    })

    # Slayt 60: Bölüm Özeti: Lokal İskemiden Sistemik Dolaşım Çöküşü Olan Şoka Geçiş
    slides.append({
        "id": "k1-24-s60",
        "title": "Bölüm Özeti: Lokal İskemiden Sistemik Dolaşım Çöküşü Olan Şoka Geçiş",
        "section": "Enfarktüs Dinamikleri: İyileşme ve Etkileyen Faktörler",
        "slideNumber": 60,
        "narrative": (
            "Enfarktüsün patolojik ve klinik dinamiklerini tamamlarken şu büyük resmi netleştiriyoruz: "
            "1. **Enfarktüs Bölgeseldir:** Enfarktüs tek bir damarın sulama alanındaki lokal iskemik hücre ölümüdür. "
            "2. **Zaman Hayattır:** Nöron için 3 dakika, miyosit için 30 dakika altın sınırdır; reaskülarizasyon bu sürelerde yapılmalıdır. "
            "3. **Sonraki Bölümlere Büyük Köprü:** Eğer perfüzyon bozukluğu tek bir organda değil de, "
            "tüm vücutta, sistemik düzeyde ortaya çıkarsa ne olur? "
            "Kalp debisinin veya dolaşan kan hacminin çökmesiyle tüm dokularda yaygın sellüler hipoksinin geliştiği "
            "bu ölümcül klinik tabloya **ŞOK** adı verilir. "
            "Kalan 4 bölümümüzde şokun patolojisini, tiplerini, septik şokun karmaşık immünolojik kaskadını ve klinik evrelerini inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Lokal bir arter tıkanıklığının aksine, tüm vücutta kardiyak debi veya efektif dolaşan hacim azalması sonucu yaygın doku hipoperfüzyonu ve hücresel hipoksi gelişmesi tablosuna şok denir.",
                "şok",
                "Tüm vücutta sistemik dolaşım yetmezliği ve doku hipoksisi tablosu"
            ),
            make_active_recall(
                "Akut miyokard enfarktüsünde nekroza giden sol ventrikül kas kitlesinin yüzde kırkı (%40) aşması durumunda kalbin pompa yetmezliğine girmesiyle gelişen şok türü nedir?",
                "Kardiyojenik şok tablosudur.",
                "Miyokard pompa fonksiyonunun çökmesiyle gelişen şok tipi"
            ),
            make_micro_quiz(
                "Lokalize bir enfarktüs tablosu ile sistemik bir 'Şok' tablosu arasındaki en temel fizyopatolojik fark aşağıdakilerden hangisidir?",
                {
                    "A": "Enfarktüsün tek bir damarın beslediği lokal doku iskemisi olması, şokun ise tüm vücutta generalize doku hipoperfüzyonu olması",
                    "B": "Şokun yalnızca çocuklarda, enfarktüsün yalnızca yaşlılarda görülmesi",
                    "C": "Enfarktüste doku hipoksisinin olmaması",
                    "D": "Şokta kalbin hiçbir zaman etkilenmemesi",
                    "E": "Enfarktüsün her zaman bakteriyel enfeksiyonla başlaması"
                },
                "A",
                {
                    "A": "Enfarktüs lokal bir vasküler tıkanmadır; şok ise tüm organları tutan sistemik dolaşım çöküşüdür.",
                    "B": "Her ikisi de her yaşta görülebilir.",
                    "C": "Enfarktüsün temeli iskemik hipoksidir.",
                    "D": "Kardiyojenik şok doğrudan kalpten kaynaklanır.",
                    "E": "Enfarktüsler çoğunlukla sterildir (%99 trombotik)."
                }
            )
        ]
    })

    return slides
