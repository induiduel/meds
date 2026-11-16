#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 8: Dismorfik Hastaya Yaklaşım, Pedigri & Teratojenler (Adım 54 - 61 + Tekrar Sayfası)
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
            "slideNumber": 54,
            "title": "Dismorfik Hastaya Yaklaşımda Altın Standartlar ve Klinik Basamaklar",
            "subtitle": "Anamnezden laboratuvara sistematik dismorfolojik muayene protokolü",
            "badge": "Klinik Protokol",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Dismorfik bir bebek veya çocukla karşılaşıldığında hekimin rastgele testler istemesi zaman, maliyet ve tanı kaybına yol açar. Sistematik bir algoritma şarttır.\n\nAltın standart basamaklar:\n- **1. Doğum ve Gebelik Öyküsü:** Anne yaşı, teratojen maruziyeti, fetal hareketler, oligohidramniyos/polihidramniyos ve doğum haftası sorgulanır.\n- **2. Üç Kuşak Soyağacı (Pedigri):** Akrabalık, tekrarlayan düşükler, erken ölümler ve ailedeki benzer fenotipler çizilir.\n- **3. Tepeden Tırnağa Fizik Muayene:** Baş çevresi, iç kantal mesafe, kulak boyutu, el-ayak çizgileri cetvelle ölçülür (Antropometri).\n- **4. Tıbbi Fotoğraflama:** Hastanın onam alınarak standart açılardan fotoğraflanması ve sendrom veri tabanları (London Dysmorphology Database, Face2Gene) ile taranması sağlanır.",
            "medicalTerms": [
                {"term": "Antropometri", "explanation": "İnsan vücudunun boyutlarının, oranlarının ve mesafelerinin standart persentil eğrilerine göre ölçülmesi."},
                {"term": "Soyağacı (Pedigri)", "explanation": "Bir ailenin en az üç kuşak boyunca sağlık ve kalıtım öyküsünün standart tıbbi sembollerle çizilmiş şeması."}
            ],
            "spotPearls": [
                "Dismorfolojide tanı göz kararı ile değil; kumpas ve cetvelle yapılan objektif antropometrik ölçümlerle konur."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Dismorfik Hastaya Sistematik Yaklaşım Adımları",
                    [
                        "1. Adım: Ayrıntılı prenatal, natal ve teratojenik anamnez alınır.",
                        "2. Adım: En az üç kuşağı kapsayan standart sembollü pedigri çizilir.",
                        "3. Adım: Tepeden tırnağa antropometrik ölçümlerle minör ve majör anomaliler saptanır.",
                        "4. Adım: Sendromik örüntüye yönelik hedefe özel sitogenetik/moleküler test seçilir."
                    ]
                ),
                make_micro_quiz(
                    "Çoklu konjenital anomalili bir bebekte dismorfolojik değerlendirme yapılırken aile öyküsü en az kaç kuşağı kapsayacak şekilde çizilmelidir?",
                    {
                        "A": "En az 3 kuşak",
                        "B": "Yalnızca anne ve baba (1 kuşak)",
                        "C": "Yalnızca kardeşler",
                        "D": "En az 10 kuşak"
                    },
                    "A",
                    {
                        "A": "Doğru! Standart klinik genetik protokolünde soyağacı (pedigri) en az üç kuşağı (çocuk, ebeveynler, büyükanne ve büyükbabalar) eksiksiz içermelidir.",
                        "B": "Yanlış. Tek kuşak resesif veya X'e bağlı kalıtımı yakalayamaz.",
                        "C": "Yanlış. Kardeşler ailevi geçişi göstermede yetersiz kalır.",
                        "D": "Yanlış. 10 kuşak pratikte ulaşılamaz ve rutin gereksizdir."
                    }
                )
            ]
        },
        {
            "slideNumber": 55,
            "title": "Üç Kuşak Pedigri (Soyağacı) Çiziminin Standart Sembolleri",
            "subtitle": "Kare erkek, daire dişi, çift çizgi akraba evliliği",
            "badge": "Pedigri Analizi",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Klinik genetikte soyağacı çizimi uluslararası standart sembollerle yapılır ve hastanın genetik haritasını oluşturur:\n\n- **Kare (□):** Erkek birey.\n- **Daire (○):** Dişi birey.\n- **Eşkenar Dörtgen (◇):** Cinsiyeti bilinmeyen birey veya fötus.\n- **İçi Dolu Sembol (■ / ●):** Hastalıktan etkilenmiş (fenotipik hasta) birey.\n- **Noktalı veya Yarı Dolu Sembol:** Taşıyıcı birey (X'e bağlı veya otozomal resesif).\n- **Çift Yatay Çizgi (=):** ==Akraba Evliliği (Konsanguinite)==; otozomal resesif hastalık riskinin en önemli belirtecidir.\n- **Ok İşareti (↗ P):** ==Proband (Propozitus)==; ailede genetik hekime ilk başvuran indeks hasta.\n- **Üzerine Eğik Çizgi:** Vefat etmiş birey.",
            "coreContent": {
                "table": {
                    "title": "Standart Pedigri Sembolleri ve Klinik Anlamları",
                    "headers": ["Sembol", "Temsil Ettiği Durum", "Klinik / Kalıtım Notu"],
                    "rows": [
                        ["Kare (□)", "Erkek birey", "Normal / Sağlıklı"],
                        ["Daire (○)", "Dişi birey", "Normal / Sağlıklı"],
                        ["İçi Dolu (■ / ●)", "Etkilenmiş (Hasta) birey", "Fenotipik klinik tablo mevcuttur"],
                        ["Çift Çizgi (=)", "Akraba Evliliği (Konsanguinite)", "Otozomal resesif hastalık riskini fırlatır"],
                        ["Ok ile İşaretli (P)", "Proband / İndeks Vaka", "Klinisyene ilk başvuran hasta birey"],
                        ["Üçgen (▲)", "Spontan Abortus (Düşük)", "Kromozom anomalisi ipucudur"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Proband (İndeks Vaka)", "explanation": "Bir ailede genetik danışmaya veya tetkike ilk yönlendirilen hasta birey."},
                {"term": "Konsanguinite", "explanation": "Aralarında en az bir ortak ata bulunan biyolojik akrabalar arasındaki evlilik."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Pedigride iki birey arasındaki 'çift yatay çizgi' akraba evliliğini (konsanguinite) simgeler ve otozomal resesif hastalık riskini katlar."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Pedigri Sembolleri Hızlı Ezber Tablosu",
                    ["Sembol Şekli", "Biyolojik Anlamı", "Sınav Püf Noktası"],
                    [
                        [("Kare (□)", False), ("Erkek Birey", True, "Erkek"), ("Standart erkek", False)],
                        [("Daire (○)", False), ("Dişi Birey", True, "Dişi"), ("Standart kadın", False)],
                        [("Çift Çizgi (=)", False), ("Akraba Evliliği", True, "Konsanguinite"), ("Resesif hastalık habercisi", False)],
                        [("Ok İşareti (P)", False), ("Proband (İndeks)", True, "İlk hasta"), ("Hastaneye ilk gelen vaka", False)]
                    ]
                ),
                make_micro_quiz(
                    "Tıbbi genetik soyağacı çiziminde ebeveynler arasında 'ÇİFT YATAY ÇİZGİ' bulunması ne anlama gelir?",
                    {
                        "A": "Akraba evliliği (Konsanguinite)",
                        "B": "Boşanmış ebeveynler",
                        "C": "Tek yumurta ikizliği",
                        "D": "Her iki ebeveynin de ölmüş olması"
                    },
                    "A",
                    {
                        "A": "Doğru! Uluslararası pedigri kuralına göre çift çizgi akraba evliliğini simgeler.",
                        "B": "Yanlış. Boşanma tek çizginin üzerine iki eğik çizgi ile gösterilir.",
                        "C": "Yanlış. İkizlik aynı noktadan çıkan çatallı çizgiyle gösterilir.",
                        "D": "Yanlış. Ölüm sembolün üzerine çapraz çizgi çekilmesidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 56,
            "title": "Klasik Teratojenler I: Talidomid Embriyopatisi ve Ekstremite Defektleri",
            "subtitle": "Kritik embriyonik pencere: 20-36. günler ve fokomeli",
            "badge": "Teratoloji",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Talidomid, teratoloji tarihinin en trajik ve en öğretici ilacıdır. 1950'lerin sonunda gebelik bulantı ilacı ve sedatif olarak piyasaya sürülmüş, on binden fazla sakat doğuma yol açmıştır.\n\nTalidomidin embriyolojik etki mekanizması:\n- **Kritik Hasar Penceresi:** Konsepsiyondan sonraki ==20 - 36. günler== arasıdır. Bu 16 günlük pencere dışında alındığında uzuv defekti yapmaz!\n- **Moleküler Mekanizma (SALL4 Yıkımı):** Talidomid, E3 ubiquitin ligaz kompleksi proteini olan ==Cereblon (CRBN)== ile bağlanır. Bu bağlanma, ekstremite ve kulak gelişiminde hayati transkripsiyon faktörü olan ==SALL4== proteininin parçalanmasına yol açar.\n- **Klasik Fenotip (Fokomeli):** Kol ve bacak uzun kemiklerinin hiç oluşmaması sonucu ellerin ve ayakların doğrudan gövdeye yapışık 'fok foku yüzgeci' şeklinde belirmesidir (Fokomeli / Ameli). Ayrıca mikroti ve iç organ defektleri eşlik eder.",
            "coreContent": {
                "table": {
                    "title": "Talidomid Embriyopatisinin Temel Karakteristikleri",
                    "headers": ["Parametre", "Özellik", "Klinik / Biyolojik Not"],
                    "rows": [
                        ["Kritik Zaman Aralığı", "20 - 36. postkonsepsiyonel günler", "Ekstremite tomurcuklarının çıktığı dar pencere"],
                        ["Moleküler Hedef", "Cereblon (CRBN) -> SALL4 yıkımı", "Transkripsiyonel kaskad duraklar"],
                        ["Karakteristik Anomali", "Fokomeli / Ameli (Uzuv yokluğu)", "Eller omuzdan, ayaklar kalçadan çıkar"],
                        ["Ek Bulgular", "Anotia/Mikrotia, kardiyak defektler", "Dış kulak yolu atrezisi ve sağırlık"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Fokomeli", "explanation": "Uzun ekstremite kemiklerinin gelişmemesi sonucu el ve ayakların doğrudan gövdeye tutunduğu ağır defekt."},
                {"term": "Cereblon (CRBN)", "explanation": "Talidomidin bağlanarak SALL4 transkripsiyon faktörünü yıktığı primer hücresel hedef protein."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Talidomid, Cereblon proteinine bağlanarak SALL4 yıkımına neden olur ve 20-36. günler arasında fokomeliye (güdük uzuv) yol açar."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Talidomid Teratogenez Kaskadı",
                    [
                        "Anne gebeliğin 20-36. günlerinde bulantı için talidomid kullanır.",
                        "Talidomid fötal hücrelerde Cereblon (CRBN) E3 ligazına bağlanır.",
                        "Ekstremite morfogenezinde şart olan SALL4 transkripsiyon faktörü parçalanır.",
                        "Ekstremite tomurcukları uzayamaz; fokomeli (uzuv yokluğu) tablosu oluşur."
                    ]
                ),
                make_micro_quiz(
                    "Gebelikte kullanılan Talidomid ilacının hücre içinde bağlandığı ve SALL4 proteininin parçalanmasını tetikleyerek fokomeliye yol açtığı moleküler hedef hangisidir?",
                    {
                        "A": "Cereblon (CRBN)",
                        "B": "Dihidrofolat Redüktaz (DHFR)",
                        "C": "HMG-CoA Redüktaz",
                        "D": "Asetilkolinesteraz"
                    },
                    "A",
                    {
                        "A": "Doğru! Talidomid doğrudan Cereblon (CRBN) proteinine bağlanarak teratojenik etkisini başlatır.",
                        "B": "Yanlış. DHFR metotreksatın hedefidir.",
                        "C": "Yanlış. Statinlerin hedefidir.",
                        "D": "Yanlış. Organofosfatların hedefidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 57,
            "title": "Klasik Teratojenler II: Fetal Alkol Sendromu (FAS) ve Nörogelişimsel Hasar",
            "subtitle": "Önlenebilir zeka geriliğinin dünyadaki bir numaralı nedeni",
            "badge": "Teratoloji",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Fetal Alkol Sendromu (FAS), gelişmiş ülkelerde önlenebilir zeka geriliğinin en sık sebebidir. Alkol için fötal gelişimde 'güvenli bir doz veya güvenli bir trimester' KESİNLİKLE YOKTUR.\n\nFAS'ın üç kardinal tanı kriteri:\n- **1. Karakteristik Fasiyal Dismorfoloji:** ==Düz/silik filtrum==, ==çok ince üst dudak (vermilion)== ve ==kısa palpebral fissürler== (ayrıca düz burun kökü ve antevert burun).\n- **2. Büyüme Geriliği:** Hem doğum öncesi (prenatal) hem de doğum sonrası (postnatal) persentil düşüklüğü (<10. persentil).\n- **3. Santral Sinir Sistemi Hasarı:** Mikrosefali, korpus kallozum agenezisi, zeka geriliği, dikkat eksikliği ve davranışsal bozukluklar.\n\n> ⚠️ **Hayati İlke:** Alkol tüm gebelik boyunca beyin parankimine ve nöronal göçe doğrudan toksiktir!",
            "medicalTerms": [
                {"term": "Fetal Alkol Spektrum Bozukluğu (FASD)", "explanation": "Gebelikte alkol maruziyetine bağlı nörogelişimsel ve yapısal hasarların genel yelpazesi."},
                {"term": "Mikrosefali", "explanation": "Baş çevresinin yaş ve cinsiyete göre ortalamanın 2 standart sapma (-2 SD) altında olması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] FAS triadının bileşenleri: 1) Düz filtrum + ince üst dudak, 2) Pre-postnatal büyüme geriliği, 3) Mikrosefali ve zeka geriliği."
            ],
            "interactiveElements": [
                make_before_after(
                    "FAS Fasiyal Görünümü",
                    "Normal Fasiyal Görünüm",
                    ["Düz ve silik filtrum oluğu", "Çok ince üst dudak çizgisi (thin vermilion)", "Kısa palpebral fissürler", "Düz burun kökü"],
                    ["Belirgin derin filtrum oluğu", "Dolgun, normal üst dudak", "Normal genişlikte palpebral fissürler", "Normal belirgin burun kökü"]
                ),
                make_micro_quiz(
                    "Aşağıdakilerden hangisi Fetal Alkol Sendromunun (FAS) kardinal yüz dismorfolojisi bulguları arasında YER ALMAZ?",
                    {
                        "A": "Dolgun ve belirgin kalın üst dudak",
                        "B": "Düz ve silik filtrum",
                        "C": "Kısa palpebral fissürler",
                        "D": "Düz burun kökü ve antevert burun delikleri"
                    },
                    "A",
                    {
                        "A": "Doğru! FAS'ta üst dudak kalın değil, tam aksine patognomonik olarak çok incedir (thin vermilion border).",
                        "B": "Yanlış. Düz filtrum FAS'ın ana kriteridir.",
                        "C": "Yanlış. Kısa palpebral fissür kardinal bulgudur.",
                        "D": "Yanlış. Düz burun kökü FAS'ta tipiktir."
                    }
                )
            ]
        },
        {
            "slideNumber": 58,
            "title": "Klasik Teratojenler III: Valproik Asit, Retinoidler ve TORCH Ajanları",
            "subtitle": "Nöral tüp defektleri, kraniofasiyal hipoplazi ve konjenital enfeksiyonlar",
            "badge": "Teratojen Yelpazesi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Klinikte sık kullanılan diğer ilaçlar ve maternal enfeksiyonlar da özgül embriyopatilere yol açar:\n\n- **Valproik Asit (Antiepileptik):** Folat metabolizmasını inhibe ederek ==Lumbosakral Spina Bifida (Nöral tüp defekti)== riskini 10-20 kat artırır. Ayrıca trigonoensefali ve parmak hipoplazisi yapar.\n- **İzotretinoin / Retinoik Asit (Akne Tedavisi):** Nöral krest hücresi göçünü bloke eder. Sonuçta mikrotia/anotia (kulak yokluğu), konotrunkal kalp anomalileri (Fallot) ve timus aplazisi (DiGeorge benzeri fenotip) gelişir.\n- **TORCH Enfeksiyonları (Toksoplazma, Rubella, CMV, Herpes):** Mikrosefali, intrakraniyal kalsifikasyonlar, korioretinit, katarakt ve hepatosplenomegali ile seyreder. CMV konjenital sensorinöral işitme kaybının en sık enfeksiyöz nedenidir.",
            "coreContent": {
                "table": {
                    "title": "Klinik Teratojenler ve Hedef Patolojileri",
                    "headers": ["Teratojen Ajan", "Kritik Mekanizma", "Spesifik Anomali Tablosu"],
                    "rows": [
                        ["Valproik Asit", "Folat metabolizması blokajı", "Meningomiyelosel (Spina bifida), Yarık damak"],
                        ["İzotretinoin (A vitamini türevi)", "Nöral krest göç blokajı", "Anotia (kulaksızlık), Konotrunkal kalp defektleri"],
                        ["Varfarin", "Gla proteinleri blokajı", "Nazal hipoplazi (küçük burun), kondrodisplazi punktata"],
                        ["ACE İnhibitörleri", "Fetal renal perfüzyon kaybı", "Renal tübüler disgenezis, anüri, oligohidramniyos"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Fetal Valproat Sendromu", "explanation": "Gebelikte valproik asit kullanımına bağlı nöral tüp defekti ve dismorfoloji ile seyreden tablo."},
                {"term": "Retinoid Embriyopatisi", "explanation": "A vitamini türevlerinin nöral krest göçünü bozarak kulak ve kalp defektleri oluşturması."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Valproik asit nöral tüp defekti (spina bifida) riskini katlar; İzotretinoin ise nöral krest hücrelerini vurarak anotia ve kalp defekti yapar."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "İlaç Teratojenleri ve Tipik Defekt Ezber Tablosu",
                    ["Teratojen İlaç", "Hedef Embriyolojik Doku", "Karakteristik Anomali"],
                    [
                        [("Valproik Asit", False), ("Folat yolağı / Nöral tüp", False), ("Spina Bifida / Meningomiyelosel", True, "Nöral tüp")],
                        [("İzotretinoin", False), ("Nöral Krest Hücreleri", False), ("Anotia / Kulak yokluğu & Kalp", True, "Kulak/Kalp")],
                        [("Varfarin", False), ("Kalsiyum bağlayan kemik matriksi", False), ("Nazal Hipoplazi (Kondrodisplazi)", True, "Burun basıklığı")],
                        [("ACE İnhibitörü", False), ("Fetal Renal Dolaşım", False), ("Renal Disgenezis & Oligohidramniyos", True, "Böbrek yetmezliği")]
                    ]
                ),
                make_micro_quiz(
                    "Ağır kistik akne tedavisi amacıyla oral izotretinoin kullanan bir kadının plansız gebe kalması durumunda bebekte aşağıdaki embriyopatik bulgulardan hangisinin görülmesi EN OLASIDIR?",
                    {
                        "A": "Mikrotia/Anotia (dış kulak yokluğu) ve konotrunkal kalp defektleri",
                        "B": "Yalnızca hafif tırnak kırılması",
                        "C": "Sirenomeli (denizkızı bacak)",
                        "D": "Osteogenezis imperfekta kemik kırıkları"
                    },
                    "A",
                    {
                        "A": "Doğru! İzotretinoin kranial nöral krest göçünü felç eder; dış kulak yokluğu (anotia/mikrotia) ve konotrunkal kalp defektleri tipiktir.",
                        "B": "Yanlış. Çok ağır majör malformasyonlar yapar.",
                        "C": "Yanlış. Sirenomeli blastogenez kaudal mezoderm hasarıdır.",
                        "D": "Yanlış. Osteogenezis imperfekta monogenik kollajen mutasyonudur."
                    }
                )
            ]
        },
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Teratojenler ve Kritik Embriyonik Pencereler",
            "subtitle": "Talidomid, FAS, Valproat ve İzotretinoin ezber matrisi",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu modül, teratoloji prensiplerini, klasik teratojenik ilaçları ve bunların hedef aldığı kritik embriyolojik pencereleri tek bir hafıza matrisinde birleştirmektedir.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Talidomid:** 20-36. günler arasında ==Cereblon (CRBN)== üzerinden ==SALL4== transkripsiyon faktörünü yıkar -> ==Fokomeli==.\n- **Fetal Alkol Sendromu:** Düz/silik filtrum + İnce üst dudak + Büyüme geriliği + Zeka geriliği.\n- **Valproik Asit:** Nöral tüp kapanmasını bozar -> ==Spina Bifida==.\n- **İzotretinoin:** Nöral krest göçünü bozar -> ==Anotia/Mikrotia== ve ==Konotrunkal Kalp Defektleri==.\n- **Varfarin:** ==Nazal Hipoplazi== ve kondrodisplazi punktata.\n- **ACE İnhibitörleri:** Fetal ==Renal Disgenezis== ve oligohidramniyos.",
            "coreContent": {
                "table": {
                    "title": "Teratojenler ve Hedef Organlar Büyük Sentez Tablosu",
                    "headers": ["Ajan", "Kritik Süreç", "Patognomonik / Tipik Anomali", "Sınav Notu"],
                    "rows": [
                        ["Talidomid", "20 - 36. günler", "Fokomeli (Güdük uzuv), Ameli", "Cereblon / SALL4 hedefli"],
                        ["Alkol (FAS)", "Tüm gebelik", "Düz filtrum, ince üst dudak, mikrosefali", "Önlenebilir zeka geriliğinde 1 numara"],
                        ["Valproik Asit", "İlk 28 gün", "Lumbosakral Spina Bifida", "Folat antagonizması"],
                        ["İzotretinoin", "Organogenez", "Mikrotia, kulak atrezisi, Fallot", "Nöral krest hücresi blokajı"],
                        ["Varfarin", "6 - 9. haftalar", "Nazal hipoplazi, epifiz kalsifikasyonları", "Kemik Gla proteinleri blokajı"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Teratojen", "explanation": "Gebelikte maruz kalındığında fetüste yapısal, fonksiyonel veya davranışsal anomali oluşturan dış etken."},
                {"term": "Fokomeli", "explanation": "Ekstremite uzun kemiklerinin yokluğu sonucu el ve ayakların gövdeden çıkması."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] Talidomid = Fokomeli (Cereblon) | Valproat = Spina Bifida | İzotretinoin = Anotia/Kalp | Alkol = Düz filtrum + Zeka geriliği.",
                "📌 [TEKRAR SPOTU] Pedigride konsanguinite çift çizgi ile, proband ok ile, düşük üçgen ile gösterilir."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Teratojenler ve Karakteristik Malformasyonlar Ezber Tablosu",
                    ["Teratojen Madde", "Kritik Hedef Doku", "Karakteristik Anomali"],
                    [
                        [("Talidomid", False), ("Cereblon / SALL4", True, "Cereblon"), ("Fokomeli (Uzuv yokluğu)", True, "Fokomeli")],
                        [("Alkol", False), ("SSS ve Nöronal Göç", True, "Nöronal göç"), ("Düz Filtrum + Mikrosefali", True, "FAS")],
                        [("Valproik Asit", False), ("Folat metabolizması", True, "Folat yolağı"), ("Meningomiyelosel (Spina bifida)", True, "Spina bifida")],
                        [("İzotretinoin", False), ("Nöral krest hücreleri", True, "Nöral krest"), ("Anotia / Kulak yokluğu & Kalp", True, "Anotia")]
                    ]
                ),
                make_micro_quiz(
                    "Gebelikte maruz kalınan teratojenik bir ajanın fötusta yol açtığı hasarın şiddetini ve tipini belirleyen EN KRİTİK faktör hangisidir?",
                    {
                        "A": "Maruziyetin gerçekleştiği gebelik haftası (kritik embriyonik pencere)",
                        "B": "Bebeğin cinsiyeti",
                        "C": "Annenin kan grubu",
                        "D": "Doğumun gerçekleştiği hastane koşulları"
                    },
                    "A",
                    {
                        "A": "Doğru! Teratolojinin bir numaralı kuralı zamanlamadır; hasarın niteliğini maruziyetin hangi embriyonik haftada gerçekleştiği belirler.",
                        "B": "Yanlış. Çoğu teratojende cinsiyet belirleyici faktör değildir.",
                        "C": "Yanlış. Kan grubu teratogenezi belirlemez.",
                        "D": "Yanlış. Hasar intrauterin dönemde çoktan gerçekleşmiştir."
                    }
                ),
                make_micro_quiz(
                    "Bipolar bozukluk veya epilepsi nedeniyle gebeliğinde Valproik asit kullanan bir kadının bebeğinde hangi majör anomalinin gelişme riski en belirgin şekilde artar?",
                    {
                        "A": "Lumbosakral Spina Bifida (Meningomiyelosel)",
                        "B": "Fokomeli",
                        "C": "Anotia (kulak yokluğu)",
                        "D": "Sirenomeli"
                    },
                    "A",
                    {
                        "A": "Doğru! Valproik asit folat metabolizmasını bozarak lumbosakral nöral tüp defekti (spina bifida) riskini katlar.",
                        "B": "Yanlış. Fokomeli talidomid hasarıdır.",
                        "C": "Yanlış. Anotia izotretinoin hasarıdır.",
                        "D": "Yanlış. Sirenomeli maternal kontrolsüz diyabetle ilişkilidir."
                    }
                )
            ]
        }
    ]
