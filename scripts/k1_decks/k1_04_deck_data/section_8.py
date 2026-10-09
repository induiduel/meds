# -*- coding: utf-8 -*-
from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_steps():
    return [
        {
            "slideNumber": 70,
            "title": "Sıvılaşma (Likefaksiyon) Nekrozu: Kavram ve Biyolojik Mekanizma",
            "subtitle": "Enzimatik sindirimin protein denatürasyonuna baskın olduğu erime nekrozu",
            "badge": "Sıvılaşma",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Sıvılaşma (likefaksiyon) nekrozu, ölü hücrelerin hızla ve tamamen sindirilerek dokunun "
                "kıvamlı, viskoz bir sıvı kütlesine dönüştüğü nekroz kalıbıdır. Koagülatif nekrozun tam "
                "aksine, burada proteinlerin denatüre olarak doku mimarisini korumasına fırsat kalmaz; "
                "enzimatik litik sindirim sürece mutlak olarak egemen olur.\n\n"
                "> [TEMEL İLKE] Sıvılaşma nekrozu iki klasik klinik tabloda görülür: 1) Fokal bakteriyel "
                "veya mantar enfeksiyonları (apse, püy), 2) Santral sinir sisteminin (beyin) iskemik infarktları.\n\n"
                "Her iki durumda da lökositlerden veya dokunun kendisinden salınan güçlü hidrolitik "
                "enzimler ölü hücreleri eritir ve doku mimarisini saatler içinde tamamen yok eder."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Enzimatik Sindirim", "desc": "Hidrolaz ve proteazların doku çatısını tamamen sıvıya çevirmesidir.", "isKey": True},
                    {"title": "Mimari Kaybı", "desc": "Koagülatif nekrozun aksine doku iskeleti ve hücre sınırları anında silinir.", "isKey": True},
                    {"title": "İki Klasik Ortam", "desc": "Piyojenik bakteriyel enfeksiyonlar ve serebral iskemik enfarktüslerdir.", "isKey": True}
                ],
                "table": {
                    "title": "Koagülatif vs Sıvılaşma Nekrozu",
                    "headers": ["Parametre", "Koagülatif Nekroz", "Sıvılaşma (Likefaksiyon) Nekrozu"],
                    "rows": [
                        ["Baskın Süreç", "Protein denatürasyonu (asidoz)", "Enzimatik litik sindirim (hidroliz)"],
                        ["Doku Kıvamı", "Sert, katı, pişmiş et gibi", "Viskoz sıvı, akışkan veya kremsi püy"],
                        ["Doku Mimarisi", "Günlerce korunur (hayalet hücreler)", "Hemen erir, mimari tamamen kaybolur"],
                        ["Tipik Örnek", "Miyokard ve böbrek enfarktüsü", "Beyin infarktı ve piyojenik apse"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sıvılaşma nekrozunda temel mekanizma enzimatik sindirimin protein denatürasyonuna baskın olmasıdır.",
                "📌 [SINAV SPOTU] Sıvılaşma nekrozu iki durumda görülür: Piyojenik enfeksiyonlar (apse) ve Beyin iskemik infarktları."
            ],
            "medicalTerms": [
                {"term": "Likefaksiyon", "explanation": "Katı bir dokunun proteolitik enzimler tarafından tamamen eritilerek sıvılaştırılmasıdır."},
                {"term": "Piyojenik", "explanation": "İrin (püy) oluşturan nötrofil çekici akut bakteriyel enfeksiyon ajanlarıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Sıvılaşma nekrozunda doku mimarisinin tamamen kaybolarak sıvıya dönüşmesinin nedeni enzimatik sindirimin baskın olmasıdır.",
                    "enzimatik sindirimin baskın olmasıdır",
                    "Litik Mekanizma"
                ),
                make_active_recall(
                    "Sıvılaşma nekrozunun klinik tıptaki iki ana prototip lezyonu hangileridir?",
                    "1) Bakteriyel ve fungal enfeksiyonlar sonucu oluşan püy/apse odakları, 2) Santral sinir sisteminde (beyinde) hipoksi ve iskemi sonucu gelişen serebral infarktlardır."
                )
            ]
        },
        {
            "slideNumber": 71,
            "title": "Püy (İrin) Oluşumu ve Lökositik Enzimler",
            "subtitle": "Ölü nötrofiller, sıvılaşmış doku artıkları ve sarı-krem eksuda",
            "badge": "Püy Patolojisi",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Bakteriyel enfeksiyonlarda (özellikle stafilokok ve streptokok gibi piyojenik mikroplarda) "
                "sıvılaşma nekrozunun en somut klinik göstergesi 'püy' (irin / pus) oluşumudur. Bakteriyel "
                "ürünler bölgeye yüz binlerce nötrofil lökositi çeker. Nötrofiller fagositoz yaparken "
                "ve ölürken içerdikleri lizozomal enzimleri (miyeloperoksidaz, elastaz, kollajenaz) çevreye boşaltır.\n\n"
                "> [TEMEL İLKE] Püy; sıvılaşmış nekrotik parankim hücreleri, ölü ve canlı nötrofiller, bakteriler "
                "ve proteinden zengin iltihabi eksudanın oluşturduğu sarı-krem renkli viskoz bir sıvıdır.\n\n"
                "Miyeloperoksidaz enziminin demir pigmenti püye karakteristik sarı-yeşil rengini kazandırır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Püy İçeriği", "desc": "Nötrofil enkazı + erimiş parankim dokusu + canlı/ölü bakterilerdir.", "isKey": True},
                    {"title": "Nötrofil Enzimleri", "desc": "Elastaz ve katepsinlerin doku kollajenini eriterek kavitasyon yapmasıdır.", "isKey": True},
                    {"title": "Miyeloperoksidaz", "desc": "Püye yeşilimsi sarı rengini veren nötrofil granül enzimidir.", "isKey": False}
                ],
                "table": {
                    "title": "Püyün Biyokimyasal ve Hücresel Bileşenleri",
                    "headers": ["Bileşen", "Kökeni", "Fonksiyonu / Patolojik Görünüm"],
                    "rows": [
                        ["Ölü Nötrofiller", "Kemotaksisle göç eden lökositler", "Fagositoz sonrası lize olmuş iltihap hücreleri"],
                        ["Sıvılaşmış Doku", "Parankim hücreleri ve matriks", "Elastazla parçalanmış amorf protein sıvısı"],
                        ["Bakteriler", "Enfeksiyöz piyojenik ajan", "LPS ve toksin salgılayarak kemotaksisi sürdürür"],
                        ["Miyeloperoksidaz", "Nötrofil primer granülleri", "Bakterisidal ROS üretimi ve yeşil-sarı renk"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Püy (irin), sıvılaşma nekrozunun klasik örneğidir; ölü nötrofiller ve sindirilmiş doku artıklarından oluşur.",
                "📌 [YÜKSEK VERİM] Piyojenik bakterilerin oluşturduğu doku nekrozu tipi istisnasız sıvılaşma (likefaksiyon) nekrozudur."
            ],
            "medicalTerms": [
                {"term": "Püy (İrin)", "explanation": "Akut bakteriyel inflamasyonda nekrotik doku artıkları ve ölü nötrofillerden oluşan sarı viskoz sıvıdır."},
                {"term": "Miyeloperoksidaz", "explanation": "Nötrofillerde hidrojen peroksiti hipokloröz aside (çamaşır suyu) çeviren yeşil renkli enzimdir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Piyojenik bakteriyel enfeksiyonlarda ölü nötrofiller ve sindirilmiş doku artıklarının oluşturduğu sıvılaşma nekrozu ürününe püy adı verilir.",
                    "püy",
                    "İltihabi Sıvı"
                ),
                make_active_recall(
                    "Püyün (irinin) sarı-yeşilimsi rengi hangi lökosit enzimine bağlıdır?",
                    "Nötrofillerin primer (azurofilik) granüllerinde bol miktarda bulunan ve demir hemoforu içeren Miyeloperoksidaz (MPO) enzimine bağlıdır."
                )
            ]
        },
        {
            "slideNumber": 72,
            "title": "Apse (Abscess) Patolojisi ve Kavitasyon",
            "subtitle": "Lokalize püy koleksiyonu, piyojenik membran ve fibröz kapsül",
            "badge": "Apse",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Apse, bir doku, organ veya kapalı anatomik boşluk içinde sınırları belirgin, lokalize bir "
                "sıvılaşma nekrozu ve püy birikimidir. Genellikle piyojenik bir bakterinin (örneğin Staphylococcus "
                "aureus) dokuya ekilmesiyle başlar. Nötrofillerin saldığı enzimler parankimi eriterek "
                "ortada bir kavite (boşluk) açar.\n\n"
                "> [KLİNİK İPUCU] Bir apsenin üç histolojik zonu vardır: 1) Merkezde sıvılaşmış nekrotik püy, "
                "2) Çevresinde yoğun canlı nötrofiller ve konjesyone damarlardan oluşan 'piyojenik membran', "
                "3) En dışta fibroblastik fibröz kapsül.\n\n"
                "Fibröz kapsül antibiyotiklerin apsenin içine nüfuz etmesini engeller; bu nedenle cerrahi "
                "drenaj (boşaltma) yapılmadan apselerin medikal tedavisi neredeyse imkansızdır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Lokalize Püy", "desc": "Doku içinde sınırlı sıvılaşma nekrozu boşluğudur.", "isKey": True},
                    {"title": "Üçlü Katman", "desc": "Merkezi püy → Piyojenik membran → Fibröz sınırlayıcı kapsüldür.", "isKey": True},
                    {"title": "Drenaj Kuralı", "desc": "'Ubi pus, ibi evacua' (Nerede püy varsa orayı boşalt) temel cerrahi ilkesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Bir Apsenin Mikroskobik Mimarisi",
                    "headers": ["Zon", "İçerik", "Fonksiyonel Durum"],
                    "rows": [
                        ["Merkezi Zon", "Nekrotik sıvı, ölü nötrofiller, mikroplar", "Sıvılaşma nekrozunun kalbi, damarsız alan"],
                        ["Piyojenik Membran", "Genişlemiş kapillerler, canlı nötrofiller", "Aktif iltihabi sınır ve eksüdasyon kaynağı"],
                        ["Dış Kapsül", "Prolifere fibroblastlar ve kollajen", "Enfeksiyonun komşu dokulara yayılmasını sınırlayan kalkan"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Apse, bir doku içinde gelişen lokalize sıvılaşma (likefaksiyon) nekrozu ve püy odağıdır.",
                "📌 [KLİNİK İPUCU] Apsenin dışındaki fibröz kapsül vaskülarize olmadığı için sistemik antibiyotikler püy merkezine ulaşamaz; drenaj şarttır."
            ],
            "medicalTerms": [
                {"term": "Apse (Abscess)", "explanation": "Doku yıkımıyla oluşan, içi püy ile dolu sınırlı sıvılaşma nekrozu kavitesidir."},
                {"term": "Piyojenik Membran", "explanation": "Apse kavitesini çevreleyen, yeni damarlar ve yoğun nötrofillerden oluşan iltihabi sınırdır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Diş enfeksiyonu sonrası yanağında 4 cm çapında fluktuasyon veren, sıcak, ağrılı kitle oluşan hastada klinik yönetim senaryosu.",
                    [
                        {
                            "text": "Sadece ağızdan yüksek doz antibiyotik verilip hasta evine gönderilir.",
                            "isCorrect": False,
                            "feedback": "Yetersiz! Apsenin avasküler püy merkezine antibiyotik difüze olamaz; tedavi başarısız olur."
                        },
                        {
                            "text": "Kitle aspire edilerek püy drene edilir (cerrahi insizyon ve drenaj); ardından etken bakteriye yönelik uygun antibiyoterapi başlanır.",
                            "isCorrect": True,
                            "feedback": "Kusursuz cerrahi ve mikrobiyolojik karar! Sıvılaşma nekrozu odağı drene edilmeden apse iyileşemez."
                        },
                        {
                            "text": "Kitleye doğrudan masaj yapılarak dokunun içine dağılması sağlanır.",
                            "isCorrect": False,
                            "feedback": "Ağır felaket! Masaj bakterilerin kana karışmasına ve sepsise yol açar."
                        }
                    ]
                ),
                make_cloze(
                    "Doku içinde sınırları belirli lokalize sıvılaşma nekrozu ve püy birikimine apse adı verilir.",
                    "apse",
                    "Klinik Enfeksiyon"
                )
            ]
        },
        {
            "slideNumber": 73,
            "title": "Serebral İnfarkt: Beyinde Sıvılaşma Nekrozu",
            "subtitle": "Ensefalomalazi, mikroglial fagositler ve kistik kavite oluşumu",
            "badge": "Nöropatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Santral sinir sisteminde (beyin ve medulla spinalis) arteriyel tıkanma sonucu gelişen iskemik "
                "hasar, vücudun diğer tüm katı organlarından tamamen farklı bir patolojik seyir izler. "
                "Beyin parankimi iskemiye maruz kaldığında dakikalar içinde litik enzimler devreye girer. "
                "Doku birkaç gün içinde pelte gibi yumuşar; bu duruma makroskopide 'ensefalomalazi' denir.\n\n"
                "> [TEMEL İLKE] Beyin dokusunda fibroblast bulunmadığı için kollajenöz skar dokusu gelişemez; "
                "makrofajlar erimiş dokuyu temizledikten sonra geride içi berrak sıvı dolu kistik bir kavite kalır.\n\n"
                "Kavitenin çevresindeki astrositler uzantılarını artırıp prolifere olarak (gemistositik astrositler) "
                "glial skar (gliozis) kuşağı oluşturur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Ensefalomalazi", "desc": "İskemik beyin dokusunun yumuşayıp pelteleşerek sıvılaşmasıdır.", "isKey": True},
                    {"title": "Lipid Fagositleri", "desc": "Parçalanan miyelin lipitlerini yutan köpüksü mikroglialardır.", "isKey": True},
                    {"title": "Kistik Kavite", "desc": "Fibroblastik skar yerine geride sıvı dolu kalıcı boşluk kalmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Beyin İnfarktüsünün Zamansal Evreleri",
                    "headers": ["Zaman", "Makroskobik Durum", "Mikroskobik Hücresel Yanıt"],
                    "rows": [
                        ["İlk 12 - 24 Saat", "Doku yumuşak, sınırları belirsiz, ödemli", "Kırmızı nöronlar (iskemik eozinofili), piknoz"],
                        ["2 - 5. Gün", "Ensefalomalazi (çamursu sıvılaşma)", "Yoğun makrofaj/mikroglia göçü, doku erimesi"],
                        ["1 - 3. Hafta", "Sıvı dolu kavite belirginleşir", "Köpüksü lipid fagositleri (Foamy histiocytes)"],
                        ["> 1 - 2 Ay", "Berrak sıvı dolu kalıcı kist", "Reaktif astrositler ve glial skar (Gliozis) kuşağı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Beyin dokusu iskemik enfarktüsünde kollajenöz skar gelişmez; sıvılaşan alan 'kistik kavite' ve çevresinde 'gliozis' ile iyileşir.",
                "📌 [SINAV SPOTU] Beyin infarktında miyelin lipidlerini yutarak sitoplazması köpüksü hale gelen hücreler mikroglial kökenli 'lipid fagositleri'dir."
            ],
            "medicalTerms": [
                {"term": "Lipid Fagositi", "explanation": "Beyin nekrozunda parçalanan miyelin artıklarını yutarak köpüksü sitoplazma kazanan makrofajdır."},
                {"term": "Kistik Kavite", "explanation": "Sıvılaşma nekrozu sonrası doku enkazının temizlenmesiyle beyinde kalan sıvı dolu boşluktur."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Serebral Sıvılaşma Nekrozu ve İyileşme Zinciri",
                    [
                        "1. Serebral İskemi: Beyin damarı tıkanır, nöronlar 3-5 dakikada ölür.",
                        "2. Enzimatik Çözünme: Zengin hidrolazlar ve düşük protein dokuyu hızla sıvılaştırır.",
                        "3. Mikroglial Temizlik: Mikroglia hücreleri köpüksü lipid fagositlerine dönerek miyelini yutar.",
                        "4. Kistik Boşalma: Eritilen nekrotik doku temizlenir ve yerinde kistik kavite açılır.",
                        "5. Astrositer Gliozis: Çevre astrositler uzantılarını örerek kavitenin etrafında glial nedbe yapar."
                    ]
                ),
                make_cloze(
                    "Beyin iskemik enfarktüsü alanında miyelin artıklarını fagosite eden köpüksü hücrelere lipid fagositleri adı verilir.",
                    "lipid fagositleri",
                    "Nöromakrofaj"
                )
            ]
        },
        {
            "slideNumber": 74,
            "title": "Kırmızı Nöron (Red Neuron): Erken İskemik Nöron Hasarı",
            "subtitle": "Serebral iskeminin ilk 12-24 saatteki en karakteristik mikroskobik damgası",
            "badge": "Nöropatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Serebral korteks nöronları hipoksi ve iskemiye vücuttaki en duyarlı hücrelerdir. Bir "
                "beyin iskemisinde ilk 12 ila 24 saat içinde ışık mikroskobunda henüz sıvılaşma kavitesi "
                "açılmamışken, nöronların sergilediği morfoloji 'kırmızı nöron' (red neuron) olarak adlandırılır.\n\n"
                "> [SINAV SPOTU] İskemik kırmızı nöron: Nöron gövdesi büzüşmüştür, Nissl cisimcikleri (rRNA) "
                "kaybolmuştur, sitoplazma yoğun parlak pembe (eozinofilik) boyanır ve çekirdek piknotiktir.\n\n"
                "Nissl cisimciklerinin erimesine 'kromatolizis' denir. Bu kırmızı nöronlar serebral iskeminin "
                "erken ve geri dönüşümsüz döneminin patognomonik histolojik göstergesidir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Kırmızı Nöron", "desc": "Yoğun eozinofilik, büzülmüş iskemik ölü nörondur.", "isKey": True},
                    {"title": "Kromatolizis", "desc": "Ribozomal RNA içeren Nissl cisimciklerinin sitoplazmada erimesidir.", "isKey": True},
                    {"title": "Piknotik Çekirdek", "desc": "Kromatinin büzüşerek üçgenimsi siyah nükleus oluşturmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Normal Nöron vs Kırmızı Nöron",
                    "headers": ["Özellik", "Normal Canlı Nöron", "İskemik Kırmızı Nöron"],
                    "rows": [
                        ["Hücre Gövdesi", "Geniş, poligonal, belirgin uzantılar", "Büzüşmüş, açılı, sivrileşmiş"],
                        ["Sitoplazma Rengi", "Mavimsi-pembe granüllü (amfofilik)", "Parlak, homojen, alev kırmızısı (hiperozeinofilik)"],
                        ["Nissl Maddesi", "Bol miktarda bazofilik granüller", "Tamamen erimiş ve kaybolmuş (Kromatolizis)"],
                        ["Çekirdek", "Açık ökromatik, dev nükleolus", "Küçük, büzük, piknotik, nükleolus kayıp"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İskemik beyin hasarının ilk 12-24 saatteki en tipik ışık mikroskobu bulgusu 'Kırmızı Nöron' (Red Neuron) görüntüsüdür.",
                "📌 [YÜKSEK VERİM] Kırmızı nöronda Nissl cisimcikleri parçalanır (kromatolizis) ve sitoplazma yoğun eozinofili kazanır."
            ],
            "medicalTerms": [
                {"term": "Kırmızı Nöron", "explanation": "Akut iskemi sonucu sitoplazması aşırı eozinofilik, nükleusu piknotik hale gelen ölü nörondur."},
                {"term": "Nissl Cisimciği", "explanation": "Nöron sitoplazmasında protein sentezi yapan granüllü endoplazmik retikulum ve ribozom kümeleridir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Nöron Morfolojisi Karşılaştırması",
                    "Sağlıklı Canlı Nöron",
                    "İskemik Kırmızı Nöron",
                    [
                        "Geniş piramidal hücre gövdesi",
                        "Sitoplazmada koyu mavi Nissl granülleri",
                        "Açık renk veziküler nükleus",
                        "Belirgin 'baykuş gözü' nükleolus"
                    ],
                    [
                        "Büzüşmüş, açılı ve üçgenimsi gövde",
                        "Nissl cisimcikleri tamamen erimiş",
                        "Sitoplazma parlak alev kırmızısı (eozinofilik)",
                        "Küçülmüş kapkara piknotik çekirdek"
                    ]
                ),
                make_cloze(
                    "Akut serebral iskeminin ilk 12-24 saatinde nöronların büzüşüp aşırı eozinofilik boyanmasıyla karakterize hücreye kırmızı nöron denir.",
                    "kırmızı nöron",
                    "Nöropatolojik Hücre"
                )
            ]
        },
        {
            "slideNumber": 75,
            "title": "Koagülatif Nekroz ile Sıvılaşma Nekrozunun Karşılaştırmalı Tablosu",
            "subtitle": "Mekanizma, doku mimarisi, klinik ortam ve iyileşme farkları",
            "badge": "Karşılaştırma",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patolojide koagülatif nekroz ile sıvılaşma nekrozu birbirine taban tabana zıt iki morfolojik "
                "dünyayı temsil eder. Koagülatif nekrozda asidoz proteinleri pıhtılaştırır; doku mimarisi "
                "ve hücre hatları günlerce ayakta kalır (hayalet hücreler) ve doku sert bir kıvamdadır. "
                "Beyin dışındaki tüm katı organ enfarktlarının değişmez kuralıdır.\n\n"
                "> [TEMEL İLKE] Sıvılaşma nekrozunda ise litik hidrolazlar dokuyu anında viskoz sıvıya "
                "çevirir; doku mimarisi hızla silinir ve geride püy/apse veya kistik kavite kalır.\n\n"
                "Koagülatif nekroz fibroblastik kollajenöz skar ile iyileşirken; beyindeki sıvılaşma nekrozu "
                "astrositer gliozis kuşağı ile çevrili kist ile sonlanır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Mekanizma Farkı", "desc": "Koagülatif = Protein denatürasyonu; Sıvılaşma = Enzimatik proteoliz.", "isKey": True},
                    {"title": "Mimari Farkı", "desc": "Koagülatifte mimari korunur; Sıvılaşmada mimari tamamen erir.", "isKey": True},
                    {"title": "İyileşme Farkı", "desc": "Koagülatif fibröz skar; Serebral sıvılaşma kistik kavite yapar.", "isKey": True}
                ],
                "table": {
                    "title": "Koagülatif vs Sıvılaşma Nekrozu Tam Matrisi",
                    "headers": ["Karşılaştırma Ölçütü", "Koagülatif Nekroz", "Sıvılaşma (Likefaksiyon) Nekrozu"],
                    "rows": [
                        ["Baskın Biyokimya", "Protein denatürasyonu (Asidoz)", "Enzimatik litik sindirim (Asit hidrolazlar)"],
                        ["Makroskobik Kıvam", "Sert, katı, kuru, pişmiş et gibi", "Yumuşak, akışkan sıvı, viskoz püy"],
                        ["Doku Mimarisi", "Günlerce korunur (Hayalet hücreler)", "Hemen silinir ve kavitasyon oluşur"],
                        ["Tipik Etyoloji", "İskemi (Beyin hariç tüm katı organlar)", "Bakteriyel enfeksiyonlar ve Beyin iskemisi"],
                        ["Nihai Akıbet", "Kollajenöz fibröz nedbe (Skar)", "Püy drenajı veya kistik kavite + gliozis"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Koagülatif nekrozda doku mimarisi korunur; Sıvılaşma nekrozunda doku mimarisi tamamen erir.",
                "📌 [SINAV SPOTU] Miyokard enfarktüsü koagülatif nekroza; Serebral enfarktüs sıvılaşma nekrozuna örnektir."
            ],
            "medicalTerms": [
                {"term": "Doku Mimarisinin Korunması", "explanation": "Hücreler ölse bile hücrelerarası çatı ve konturların mikroskopta tanınabilir kalmasıdır."},
                {"term": "Kavitasyon", "explanation": "Nekrotik dokunun erimesi veya dışarı boşalması sonucu organda içi boş bir oyuk açılmasıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "İki Ana Nekrozun Karşılaştırması",
                    ["Ölçüt", "Koagülatif Nekroz", "Sıvılaşma Nekrozu"],
                    [
                        [("Baskın Süreç", False), ("Protein denatürasyonu", True, "Pıhtılaşma"), ("Enzimatik sindirim", True, "Eritme")],
                        [("Doku Mimarisi", False), ("Günlerce korunur", True, "Hayalet Hatlar"), ("Hemen silinir", True, "Litik Erime")],
                        [("Kıvam", False), ("Sert ve kuru", True, "Katılaşma"), ("Viskoz sıvı veya püy", True, "Akışkanlık")],
                        [("Tipik Organ", False), ("Kalp, böbrek, dalak", True, "Katı Organlar"), ("Beyin infarktı, apse", True, "İstisna / İrin")]
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdakilerden hangisi koagülatif nekrozu sıvılaşma (likefaksiyon) nekrozundan ayıran en karakteristik histopatolojik özelliktir?",
                    {
                        "A": "Hücre zarlarının parçalanması",
                        "B": "Doku mimarisinin ve hücre sınırlarının en az birkaç gün boyunca korunması",
                        "C": "Hücre çekirdeğinde karyolizis gelişmesi",
                        "D": "Dokuya nötrofillerin infiltre olması",
                        "E": "Sitoplazmada kalsiyum birikmesi"
                    },
                    "B",
                    {
                        "A": "Her iki nekrozda da membran parçalanır.",
                        "B": "Doğru cevap B'dir: Koagülatif nekrozda protein denatürasyonu sayesinde doku mimarisi ve hücre hatları günlerce ayakta kalır; sıvılaşmada ise anında silinir.",
                        "C": "Nükleer erime tüm nekroz tiplerinde ortaktır.",
                        "D": "Enflamasyon tüm nekrozlarda görülür.",
                        "E": "Kalsiyum her iki tipte de çökebilir."
                    }
                )
            ]
        },
        {
            "slideNumber": 76,
            "title": "Akut Enflamasyonda Sıvılaşma Nekrozunun Rolü",
            "subtitle": "Kollajenaz, elastaz ve granülasyon dokusu bariyeri",
            "badge": "Enflamasyon",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Sıvılaşma nekrozu sadece pasif bir doku ölümü değildir; akut inflamasyonun biyolojik "
                "savaş alanını temsil eder. Piyojenik bakteriler dokuya yerleştiğinde, bakteriyel toksinler "
                "ve konak nötrofilleri arasında devasa bir kimyasal çatışma başlar. Nötrofiller degranüle "
                "oldukça ortama matriks metalloproteinazları (MMP'ler), kollajenaz ve elastaz saçar.\n\n"
                "> [TEMEL İLKE] Bu proteolitik enzimler sağlam bağ dokusu çatısını eriterek nötrofillerin "
                "bakterilere ulaşmasını sağlar; ancak bu sırada doku da sıvılaşarak kavitasyon oluşturur.\n\n"
                "Canlı vücut bu yıkımın tüm vücuda yayılmasını engellemek için hızla granülasyon dokusu "
                "ve endotel bariyeri kurarak lezyonu sınırlar ve apse duvarını oluşturur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "MMP ve Elastaz", "desc": "Nötrofil enzimlerinin ekstraselüler matriksi eriterek dokuyu sıvılaştırmasıdır.", "isKey": True},
                    {"title": "Kavitasyon Bedeli", "desc": "Bakteriyi yok etmeye çalışan bağışıklığın kendi dokusunda delik açmasıdır.", "isKey": True},
                    {"title": "Bariyer Oluşumu", "desc": "Canlı çevre dokunun fibroblastlarla lezyonu hapsedip apsede sınırlandırmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Sıvılaşma Nekrozunda Lökositik Enzimler",
                    "headers": ["Enzim", "Hücresel Kaynak", "Doku Yıkımındaki Rolü"],
                    "rows": [
                        ["Nötrofil Elastazı", "Azurofilik granüller", "Elastik lifleri ve hücre dışı matriksi yıkar"],
                        ["Kollajenaz (MMP-8)", "Spesifik granüller", "Tip I ve III kollajeni keserek doku çatısını çözer"],
                        ["Jelatinaz (MMP-9)", "Tersiyer granüller", "Bazal membran tip IV kollajenini eritir"],
                        ["Miyeloperoksidaz", "Primer granüller", "Bakteri duvarını lize eder, püye renk verir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Akut inflamasyonda sıvılaşma nekrozunu ve püy oluşumunu sağlayan ana hücresel kaynak nötrofil lizozomal enzimleridir.",
                "📌 [YÜKSEK VERİM] Nötrofil enzimlerinin aşırı salınımı bakteriyi öldürürken çevredeki sağlıklı parankimi de sıvılaştırır (dost ateşi hasarı)."
            ],
            "medicalTerms": [
                {"term": "Matriks Metalloproteinaz (MMP)", "explanation": "Çinko bağımlı çalışan ve ekstraselüler matriks proteinlerini sindiren enzim ailesidir."},
                {"term": "Degranülasyon", "explanation": "Lökositlerin fagositoz sırasında veziküllerindeki enzimleri ekstraselüler alana boşaltmasıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Akut inflamasyonda bağ dokusu çatısını eriterek dokunun sıvılaşmasına yol açan temel nötrofil enzimleri matriks metalloproteinazlarıdır.",
                    "matriks metalloproteinazlarıdır",
                    "Enzim Ailesi"
                ),
                make_active_recall(
                    "Nötrofillerin bakteriyel enfeksiyon bölgesinde dokuyu sıvılaştırmasının evrimsel ve biyolojik avantajı nedir?",
                    "Dokunun ekstraselüler matriksini eriterek diğer nötrofillerin ve antikorların mikroorganizmaya doğru sıvı ortamda hızla hareket etmesini ve bakterinin etrafını sarmasını sağlar."
                )
            ]
        },
        {
            "slideNumber": 77,
            "title": "Santral Sinir Sisteminde Gliozis ve Onarım Özellikleri",
            "subtitle": "Kollajen yokluğu, astrosit hipertrofisi ve gemistositik hücreler",
            "badge": "Nöropatoloji",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Santral sinir sisteminin hücre hasarına verdiği onarım yanıtı, vücudun diğer tüm dokularından "
                "tamamen farklıdır. Beyinde kan damarlarının adventisyası hariç bağ dokusu ve fibroblast "
                "bulunmaz. Bu nedenle beyinde bir nekroz alanı (örneğin enfarktüs) iyileşirken fibroblastlar "
                "gelip kollajen üretemez ve klasik bir 'fibröz skar' oluşamaz.\n\n"
                "> [TEMEL İLKE] Beynin onarım mekanizması 'Gliozis'tir; nekroz alanının çevresindeki reaktif "
                "astrositler çoğalır, sitoplazmaları genişler (gemistositik astrosit) ve uzantılarıyla bir ağ örer.\n\n"
                "Makrofajlar sıvılaşmış nekrotik nöron ve miyelin enkazını tamamen temizlediğinde, geride "
                "içi sıvı dolu kistik bir kavite ve bu kavitenin duvarında astrositik glial nedbe kalır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Gliozis Tanımı", "desc": "Beyinde fibröz skar yerine astrositlerin oluşturduğu hücresel nedbe dokusudur.", "isKey": True},
                    {"title": "Gemistositik Astrosit", "desc": "Geniş pembe sitoplazmalı, eksantrik çekirdekli reaktif astrositlerdir.", "isKey": True},
                    {"title": "Kistik Sonuç", "desc": "Kollajen dolgusu yapılamadığı için eriyen alanın kalıcı bir kiste dönüşmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Genel Doku Onarımı vs Beyin Dokusu Onarımı",
                    "headers": ["Özellik", "Genel Doku (Kalp, Böbrek vb.)", "Santral Sinir Sistemi (Beyin)"],
                    "rows": [
                        ["Onarım Hücresi", "Fibroblastlar ve miyofibroblastlar", "Reaktif astrositler (Gemistositler)"],
                        ["Temel Matriks", "Tip I ve Tip III Kollajen lifleri", "GFAP (Glial Fibriler Asidik Protein) ağları"],
                        ["Nihai Morfoloji", "Sert, beyaz, büzüşmüş fibröz skar", "Sıvı dolu kistik kavite + Glial sınır"],
                        ["Kavitasyon", "Genellikle olmaz (skar alanı doldurur)", "Kural olarak kavitasyonla sonuçlanır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Beyin hasarında kollajenöz skar oluşmaz; astrositlerin çoğalmasıyla oluşan hücresel nedbeye 'Gliozis' denir.",
                "📌 [YÜKSEK VERİM] Reaktif astrositler GFAP (Glial fibriler asidik protein) ile immünhistokimyasal olarak kuvvetli pozitif boyanır."
            ],
            "medicalTerms": [
                {"term": "Gliozis", "explanation": "Santral sinir sisteminde hasar sonrası astrositlerin prolifere olup glial lifler üretmesidir."},
                {"term": "GFAP", "explanation": "Glial Fibrillary Acidic Protein; astrosit sitoiskeletinde bulunan tanısal ara filamandır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Doku Onarım Mekanizmaları",
                    "Genel Parankimatöz Doku",
                    "Santral Sinir Sistemi (Beyin)",
                    [
                        "Fibroblastlar aktive olur",
                        "Tip I ve III kollajen sentezlenir",
                        "Nekroz alanı sert fibröz skarla dolar",
                        "Doku büzüşür ve çöküntü oluşur"
                    ],
                    [
                        "Reaktif astrositler çoğalır (Gliozis)",
                        "GFAP zengini glial uzantılar örülür",
                        "Kollajen dolgu yapılamaz, kist kalır",
                        "Sıvı dolu kistik kavite duvarı sınırlanır"
                    ]
                ),
                make_cloze(
                    "Santral sinir sisteminde hasar sonrası astrositlerin çoğalarak oluşturduğu hücresel nedbe dokusuna gliozis adı verilir.",
                    "gliozis",
                    "Nöral Onarım"
                )
            ]
        },
        {
            "slideNumber": 78,
            "title": "Sıvılaşma Nekrozunda Özel Boyalar ve Tanı Yöntemleri",
            "subtitle": "Gram, GMS, LFB (Luxol Fast Blue) ve GFAP immünohistokimyası",
            "badge": "Laboratuvar",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Sıvılaşma nekrozuyla karşılaşan bir patolog, lezyonun enfeksiyöz mü (apse) yoksa iskemik mi "
                "(serebral infarkt) olduğunu netleştirmek için özel histokimyasal ve immünhistokimyasal "
                "boyalardan yararlanır. Enfeksiyöz şüphede püy içinde bakteri aramak için Gram boyası, "
                "mantar hiflerini göstermek için Gomori Metenamin Gümüş (GMS) boyası yapılır.\n\n"
                "> [TEMEL İLKE] Beyin infarktında miyelin kılıf kaybını göstermek için Luxol Fast Blue (LFB), "
                "lipid fagositlerini işaretlemek için CD68, reaktif astrositleri kanıtlamak için GFAP boyanır.\n\n"
                "LFB boyasında sağlıklı beyaz cevher parlak mavi görünürken, nekrotik sıvılaşma alanında "
                "mavi renk tamamen silinir ve miyelin kaybı objektif olarak belgelenir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Enfeksiyon Boyaları", "desc": "Gram (bakteri) ve GMS (mantar) ile etiyolojik mikrobun saptanmasıdır.", "isKey": True},
                    {"title": "Miyelin Boyası", "desc": "Luxol Fast Blue (LFB) ile serebral enfarktta miyelin kaybının gösterilmesidir.", "isKey": True},
                    {"title": "GFAP İmmünohistokimyası", "desc": "Kavite kenarındaki reaktif glial skarın doğrulanmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Sıvılaşma Nekrozunda Kullanılan Özel Boyalar",
                    "headers": ["Boya / Belirteç", "Hedeflenen Yapı", "Pozitif Boyanma Anlamı"],
                    "rows": [
                        ["Gram Boyası", "Bakteri hücre duvarı", "Gram(+) mor / Gram(-) pembe bakteriler (Apse etkeni)"],
                        ["GMS (Gümüş Boyası)", "Mantar hücre duvarı polisakkaritleri", "Siyah boyanan fungal hifler ve sporlar"],
                        ["Luxol Fast Blue (LFB)", "Miyelin kılıf lipoproteinleri", "Sağlamda mavi, nekrotik enfarkt alanında renksiz"],
                        ["CD68 İmmünoboyası", "Makrofaj / Mikroglia lizozomu", "Köpüksü lipid fagositlerinin kahverengi boyanması"],
                        ["GFAP İmmünoboyası", "Astrosit ara filamanları", "Kavite çevresindeki gliozis kuşağının gösterilmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Beyin dokusunda miyelin kılıf bütünlüğünü değerlendirmek için Luxol Fast Blue (LFB) özel boyası kullanılır.",
                "📌 [YÜKSEK VERİM] GFAP (Glial Fibriler Asidik Protein), serebral infarkt çevresindeki astrositleri ve gliozisi gösteren en duyarlı belirteçtir."
            ],
            "medicalTerms": [
                {"term": "Luxol Fast Blue", "explanation": "Miyelin lipoproteinlerini bağlayarak sinir liflerini parlak maviye boyayan histopatolojik boyadır."},
                {"term": "GMS Boyası", "explanation": "Gomori Methenamine Silver; mantar duvarındaki karbonhidratları indirgeyerek siyah gümüş çökeltisi yapan boyadır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Sıvılaşma Nekrozu Boyaları",
                    ["Boya Adı", "Hedef Yapı", "Klinik Kullanım"],
                    [
                        [("Gram", False), ("Bakteri duvarı", True, "Mikrop"), ("Apse etiyolojisi", False)],
                        [("GMS", False), ("Fungal polisakkarit", True, "Mantar"), ("Fungal apse tanısı", False)],
                        [("Luxol Fast Blue", False), ("Miyelin kılıfı", True, "Sinir Kılıfı"), ("Beyin infarktında miyelin kaybı", False)],
                        [("GFAP", False), ("Astrosit ara filamanı", True, "Glial Protein"), ("Gliozis kuşağının kanıtı", False)]
                    ]
                ),
                make_cloze(
                    "Beyin infarktüsünde sağlam beyaz cevher ile nekrotik alanı ayırmak için miyelini maviye boyayan Luxol Fast Blue boyası kullanılır.",
                    "Luxol Fast Blue",
                    "Nörohistolojik Boya"
                )
            ]
        },
        {
            "slideNumber": 79,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Sıvılaşma Nekrozu ve Apseleşme",
            "subtitle": "Litik sindirim, püy ve apse mimarisi, ensefalomalazi ve kırmızı nöron",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 8,
            "synthesisNarrative": (
                "Sekizinci kontrol noktasında, sıvılaşma nekrozunun tüm moleküler ve klinik boyutlarını "
                "özetliyoruz. Sıvılaşma nekrozunda enzimatik litik sindirim protein denatürasyonuna baskındır; "
                "doku mimarisi anında erir ve geride püy veya kistik kavite kalır.\n\n"
                "> [ÖZET VURGU] Piyojenik enfeksiyonlarda ölü nötrofil ve doku enkazı püyü (apse) oluştururken; "
                "beyin iskemisinde lipid fagositleri ve astrositik gliozis kistik kaviteyi sınırlar.\n\n"
                "Aşağıdaki 3 kritik akıl kartını dikkatle inceleyerek sıvılaşma nekrozunu tam olarak öğrenin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Litik Baskınlık", "desc": "Koagülatifin aksine doku mimarisinin dakikalar/saatler içinde erimesidir.", "isKey": True},
                    {"title": "Püy ve Apse", "desc": "Nötrofil enzimleriyle parankimin sıvılaşıp kavite oluşturmasıdır.", "isKey": True},
                    {"title": "Serebral Kist", "desc": "Beyinde kollajen skar yerine sıvı dolu kistik kavite ve gliozis kalmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 8 Sentez Tablosu",
                    "headers": ["Lezyon / Kavram", "Baskın Mekanizma", "Karakteristik Görünüm"],
                    "rows": [
                        ["Sıvılaşma Nekrozu", "Enzimatik hidroliz baskınlığı", "Doku mimarisinin tamamen eridiği viskoz kütle"],
                        ["Püy (İrin)", "Nötrofillerin litik enzim salınımı", "Ölü nötrofil ve doku artıklarından sarı-krem sıvı"],
                        ["Apse", "Lokalize püy koleksiyonu", "Piyojenik membran ve fibröz kapsülle çevrili kavite"],
                        ["Kırmızı Nöron", "Akut iskemik kromatolizis (12-24 st)", "Büzülmüş, eozinofilik, piknotik nükleuslu nöron"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sıvılaşma nekrozu iki durumda görülür: 1) Bakteriyel ve fungal enfeksiyonlar (apse), 2) Beyin iskemik infarktları.",
                "📌 [SINAV SPOTU] Beyin dokusunda fibroblastik skar gelişmez; lezyon kistik kavite ve çevresinde gliozis ile iyileşir."
            ],
            "medicalTerms": [
                {"term": "Ensefalomalazi", "explanation": "Beyin parankiminin iskemik sıvılaşma nekrozu sonucu yumuşayıp erimesi tablosudur."},
                {"term": "Gemistosit", "explanation": "Gliozis sırasında bol pembe sitoplazma kazanan reaktif astrosit formudur."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-022",
                    "Sıvılaşma (likefaksiyon) nekrozunun temel patofizyolojik mekanizması nedir ve koagülatif nekrozdan nasıl ayrılır?",
                    "Sıvılaşma nekrozunda enzimatik hidrolitik sindirim protein denatürasyonuna mutlak olarak üstündür; bu nedenle koagülatif nekrozdaki gibi doku mimarisi korunamaz, hücreler hızla eriyerek viskoz bir sıvı kütlesine döner."
                ),
                make_flashcard(
                    "fc-k1-04-023",
                    "Bir beyin iskemisinde ilk 12-24 saatte izlenen 'Kırmızı Nöron' (Red Neuron) morfolojisi nasıldır?",
                    "Nöron gövdesi büzüşmüş ve üçgenleşmiştir, Nissl cisimcikleri erimiştir (kromatolizis), sitoplazma yoğun parlak pembe (eozinofilik) boyanır ve çekirdek koyu piknotiktir."
                ),
                make_flashcard(
                    "fc-k1-04-024",
                    "İskemiye uğramış beyin dokusunda kalp veya böbrekteki gibi kollajenöz fibröz skar neden gelişemez?",
                    "Çünkü santral sinir sisteminde damar adventisyası hariç fibroblast ve intersellüler kollajen çatısı bulunmaz; bu nedenle nekrotik alan makrofajlarca temizlendikten sonra yerinde sıvı dolu kistik kavite kalır ve duvarı astrositlerce (gliozis) sınırlanır."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 8 Sentezi: Bir apsenin cerrahi olarak boşaltılmadan (drene edilmeden) yalnızca sistemik antibiyotikle tam olarak iyileşememesinin patolojik gerekçesi nedir?",
                    "Çünkü apse odağının merkezi tamamen avasküler (damarsız) bir nekrotik püy kitlesidir ve çevresinde kalın bir fibröz kapsül bulunur; damardan verilen antibiyotikler bu damarsız nekroz merkezine yeterli bakterisidal konsantrasyonda difüze olamaz."
                ),
                make_cloze(
                    "Beyin infarktüsünde sıvılaşan dokunun temizlenmesiyle oluşan boşluğa kistik kavite adı verilir.",
                    "kistik kavite",
                    "Nöropatolojik Lezyon"
                )
            ]
        }
    ]
