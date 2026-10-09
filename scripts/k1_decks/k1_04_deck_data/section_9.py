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
            "slideNumber": 80,
            "title": "Gangrenöz Nekroz Kavramı: Klinik Bir Tanım",
            "subtitle": "Spesifik bir histolojik hücre ölüm tipi değil, klinik cerrahi bir terim",
            "badge": "Gangren",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Tıbbi patolojide 'Gangrenöz Nekroz' kavramı diğer nekroz tiplerinden çok temel bir noktada "
                "ayrılır: Gangren bağımsız bir histolojik hücre ölümü tipi değildir; genellikle cerrahlar "
                "tarafından kullanılan KLİNİK bir terimdir. Çoğunlukla alt ekstremitelerde (bacak ve ayak) "
                "veya bağırsak segmentlerinde kan akımının kesilmesiyle gelişen geniş doku nekrozunu tanımlar.\n\n"
                "> [SINAV SPOTU] Gangrenöz nekroz temelde çok katmanlı bir KOAGÜLATİF nekrozdur; ancak üzerine "
                "bakteri enfeksiyonu bindiğinde ikinci bir patolojik süreç olan SIVILAŞMA nekrozu eklenir.\n\n"
                "Bu nedenle gangren, dokunun bakteriyel enfeksiyon içerip içermemesine göre iki ana klinik "
                "forma ayrılır: Kuru gangren ve Islak gangren."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Klinik Terim", "desc": "Ayrı bir hücresel mekanizma değil, cerrahi makroskobik bir tanımlamadır.", "isKey": True},
                    {"title": "Temel Histoloji", "desc": "Zemininde her zaman arteriyel iskemiye bağlı koagülatif nekroz yatar.", "isKey": True},
                    {"title": "İki Ana Form", "desc": "Kuru gangren (saf koagülatif) ve Islak gangren (koagülatif + sıvılaşma).", "isKey": True}
                ],
                "table": {
                    "title": "Gangrenöz Nekrozun Özellikleri",
                    "headers": ["Parametre", "Kuru Gangren", "Islak Gangren"],
                    "rows": [
                        ["Başlatıcı Neden", "Arteriyel tıkanma (Periferik arter hastalığı)", "Venöz/arteriyel tıkanma + Bakteriyel süperenfeksiyon"],
                        ["Baskın Histoloji", "Saf koagülatif nekroz", "Koagülatif nekroz üzerine eklenmiş sıvılaşma nekrozu"],
                        ["Doku Görünümü", "Kuru, büzüşmüş, siyah, mumyalaşmış", "Şiş, ödemli, kötü kokulu, yumuşak, çürümüş"],
                        ["Demarkasyon Sınırı", "Çok belirgin, keskin bir çizgi", "Belirsiz, çevreye hızla yayılan flegmon"],
                        ["Sistemik Toksisite", "Yok veya çok az (toksemi nadir)", "Çok ağır, sepsis ve septik şok riski yüksek"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gangrenöz nekroz spesifik bir histolojik nekroz tipi değildir; klinik cerrahi bir terimdir.",
                "📌 [SINAV SPOTU] Gangren temelde koagülatif nekrozdur; bakteriyel enfeksiyon eklendiğinde sıvılaşma nekrozu bileşeni kazanarak 'ıslak gangren' adını alır."
            ],
            "medicalTerms": [
                {"term": "Gangren", "explanation": "Kan akımının kesilmesi sonucu geniş bir doku bölgesinde (genellikle uzuvda) gelişen nekrozdur."},
                {"term": "Klinik Terim", "explanation": "Mikroskobik biyolojik mekanizmadan ziyade makroskobik muayene ve cerrahi duruma göre adlandırılan terimdir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Gangrenöz nekroz spesifik bir histolojik hücre ölüm tipi olmayıp genellikle alt ekstremitede kullanılan klinik bir terimdir.",
                    "klinik bir terimdir",
                    "Terminoloji İlkesi"
                ),
                make_active_recall(
                    "Gangrenöz nekrozun histopatolojik temeli hangi nekroz tipine dayanır ve enfeksiyon eklenince neye dönüşür?",
                    "Temelde iskemik arter tıkanmasına bağlı Koagülatif nekrozdur; üzerine bakteriyel enfeksiyon eklenip lökosit enzimleri devreye girdiğinde Sıvılaşma nekrozuna (Islak gangren) dönüşür."
                )
            ]
        },
        {
            "slideNumber": 81,
            "title": "Kuru Gangren (Dry Gangrene): Mumyalaşma ve Keskin Sınır",
            "subtitle": "Arteriyel tıkanma, yavaş doku kuruması ve belirgin demarkasyon hattı",
            "badge": "Kuru Gangren",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Kuru gangren, alt ekstremitede (ayak parmakları veya ayak) arteriyel kan akımının yavaşça "
                "ve ilerleyici şekilde kesilmesi sonucu ortaya çıkar. En sık neden ateroskleroz (periferik "
                "arter hastalığı), Buerger hastalığı veya Raynaud fenomenidir. Venöz drenaj açık kaldığı "
                "için dokudaki sıvı buharlaşır ve geri çekilir.\n\n"
                "> [TEMEL İLKE] Doku kurur, büzüşür ve siyah-kahverengi sert bir 'mumya' görünümü alır; "
                "dokuda bakteri enfeksiyonu olmadığı için kokuşma ve püy oluşmaz.\n\n"
                "Ölü kuru doku ile komşu canlı sağlam doku arasında çok net, cetvelle çizilmiş gibi keskin "
                "bir 'demarkasyon hattı' (ayrım çizgisi) bulunur. Toksik maddeler kana karışmaz; hasta stabildir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Mumyalaşma", "desc": "Suyunu kaybeden iskemik dokunun sertleşip kuruması ve büzülmesidir.", "isKey": True},
                    {"title": "Siyah Renk", "desc": "Eritrositlerdeki hemoglobinden açığa çıkan demir sülfür pigmentidir.", "isKey": True},
                    {"title": "Keskin Sınır", "desc": "Canlı doku ile ölü doku arasında belirgin demarkasyon hattı bulunmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Kuru Gangrenin Karakteristik Nitelikleri",
                    "headers": ["Parametre", "Kuru Gangrendeki Durum", "Gerekçe"],
                    "rows": [
                        ["Başlatıcı Damar Sorunu", "Yalnızca arteriyel tıkanma", "Venöz drenaj açık olduğu için doku kurur"],
                        ["Bakteri Enfeksiyonu", "YOKTUR (Steril)", "Patojen mikroorganizma kolonizasyonu gelişmemiştir"],
                        ["Doku Nem Oranı", "Aşırı kuru, sert ve kırılgan", "Sıvı buharlaşması ve venöz drenaj"],
                        ["Koku", "Kötü koku YOKTUR", "Putrefaksiyon (çürüme) bakterileri bulunmaz"],
                        ["Prognoz", "Stabil, sistemik yayılım nadir", "Spontan amputasyon (otoamputasyon) gelişebilir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kuru gangrende doku kurur, büzüşür, kararır ve mumyalaşır; doku ile canlı parankim arasında belirgin demarkasyon hattı vardır.",
                "📌 [YÜKSEK VERİM] Kuru gangren steril bir koagülatif nekrozdur; enfeksiyon ve püy içermez."
            ],
            "medicalTerms": [
                {"term": "Mumifikasyon (Mumyalaşma)", "explanation": "İskemik dokunun suyunu kaybederek sert, kuru ve siyah bir kalıntı haline gelmesidir."},
                {"term": "Otoamputasyon", "explanation": "Demarkasyon hattı boyunca granülasyon dokusunun kuru gangrenli parmağı kendiliğinden koparmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Gangren Formları: Kuru vs Islak",
                    "Kuru Gangren",
                    "Islak Gangren",
                    [
                        "Doku kuru, büzüşmüş ve mumyalaşmıştır",
                        "Bakteri enfeksiyonu yoktur",
                        "Kötü koku oluşmaz",
                        "Keskin ve belirgin demarkasyon hattı vardır",
                        "Sistemik toksemi ve şok riski düşüktür"
                    ],
                    [
                        "Doku ödemli, yumuşak ve çamursudur",
                        "Yoğun bakteri süperenfeksiyonu vardır",
                        "Ağır kokuşma ve pis koku mevcuttur",
                        "Sınır belirsizdir, hızla yukarı yayılır",
                        "Ölümcül sepsis ve septik şok riski çok yüksektir"
                    ]
                ),
                make_cloze(
                    "Kuru gangrende ölü doku ile canlı doku arasında çıplak gözle net olarak seçilebilen demarkasyon hattı bulunur.",
                    "demarkasyon hattı",
                    "Ayırıcı Sınır"
                )
            ]
        },
        {
            "slideNumber": 82,
            "title": "Islak Gangren (Wet Gangrene): İkincil Sıvılaşma ve Sepsis Tehlikesi",
            "subtitle": "Kuru gangrene bakteriyel enfeksiyon eklenmesi ve kokuşma (putrefaksiyon)",
            "badge": "Islak Gangren",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Islak gangren, iskemik nekroz alanına çürüme (putrefaksiyon) bakterilerinin yerleşmesiyle "
                "gelişen son derece tehlikeli ve acil cerrahi müdahale gerektiren bir tablodur. Genellikle "
                "venöz tıkanıklıkla birlikte olan arteriyel yetersizliklerde (dokuda sıvı göllenmesi) veya "
                "kuru gangrenli bir ekstremitenin kirlenmesiyle başlar.\n\n"
                "> [TEMEL İLKE] Bakterilerin litik enzimleri ve nötrofil infiltrasyonu, önceden var olan "
                "koagülatif nekrozu hızla SIVILAŞMA nekrozuna çevirir; doku şişer, çürür ve korkunç bir koku yayar.\n\n"
                "Islak gangrende belirgin bir sınır (demarkasyon hattı) yoktur; enfeksiyon doku planları "
                "boyunca hızla proksimale yayılır. Bakteriyel toksinler hızla kana karışarak masif sepsise "
                "ve ölümcül septik şoka yol açar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Bakteriyel Süperenfeksiyon", "desc": "Saprofıt ve piyojenik bakterilerin iskemik dokuyu istila etmesidir.", "isKey": True},
                    {"title": "İkincil Sıvılaşma", "desc": "Koagülatif nekroz zemininde hızla sıvılaşma ve püy gelişmesidir.", "isKey": True},
                    {"title": "Sepsis Aciliyeti", "desc": "Toksinlerin kana karışmasıyla acil amputasyon gerektiren ölümcül tablodur.", "isKey": True}
                ],
                "table": {
                    "title": "Islak Gangrenin Klinikopatolojik Bulguları",
                    "headers": ["Özellik", "Gözlenen Tablo", "Fizyopatolojik Neden"],
                    "rows": [
                        ["Doku Nem Durumu", "Aşırı ödemli, sulu ve şişmiş", "Venöz göllenme ve bakteriyel damar geçirgenliği"],
                        ["Doku Kokusu", "Ağır, pis, çürük kokusu (Kokuşma)", "Bakterilerin proteinleri parçalayıp hidrojen sülfür üretmesi"],
                        ["Sınır Çizgisi", "Demarkasyon hattı YOK, belirsiz sınır", "Bakteri enzimlerinin doku planlarında hızla ilerlemesi"],
                        ["Sistemik Etki", "Yüksek ateş, lökositoz, şok", "Masif endotoksemi, sitokin fırtınası ve bakteriyemi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Islak gangren: Koagülatif nekroz alanına bakteriyel enfeksiyon eklenmesiyle oluşan ikincil sıvılaşma nekrozudur.",
                "🚨 [KRİTİK UYARI] Islak gangrende demarkasyon hattı yoktur; sınır belirsizdir ve hızla ilerleyerek fatal sepsise yol açar."
            ],
            "medicalTerms": [
                {"term": "Putrefaksiyon (Kokuşma)", "explanation": "Ölü doku proteinlerinin anaerobik bakteriler tarafından çürütülüp kötü kokulu gazlar salmasıdır."},
                {"term": "Flegmon", "explanation": "Sınırları belirsiz, doku aralıkları boyunca hızla yayılan pürülan inflamasyon tablosudur."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Diyabetik hastanın ayağında başlayan yaranın şiştiği, kötü kokulu siyah-yeşil akıntı yaptığı ve hastanın ateşinin 39.5°C'ye çıktığı senaryo.",
                    [
                        {
                            "text": "Tablo kuru gangrendir; ayak sadece pansumanla sarılıp poliklinik takibine alınmalıdır.",
                            "isCorrect": False,
                            "feedback": "Ölümcül hata! Kötü koku, akıntı ve ateş ıslak gangreni ve sepsisi gösterir."
                        },
                        {
                            "text": "Tablo ıslak gangrendir; sekonder bakteriyel sıvılaşma nekrozu ve sepsis riski vardır, acil cerrahi debridman/amputasyon ve parenteral antibiyotik gereklidir.",
                            "isCorrect": True,
                            "feedback": "Mükemmel hayat kurtarıcı karar! Islak gangren acil cerrahi rezeksiyon gerektiren enfeksiyöz bir felakettir."
                        },
                        {
                            "text": "Ayağa sıcak su banyosu yaptırılmalıdır.",
                            "isCorrect": False,
                            "feedback": "Enfeksiyonu daha da azdırır."
                        }
                    ]
                ),
                make_cloze(
                    "Koagülatif nekroz zeminine bakteriyel enfeksiyon eklenmesiyle gelişen ikincil sıvılaşma nekrozu tablosuna ıslak gangren denir.",
                    "ıslak gangren",
                    "Tehlikeli Form"
                )
            ]
        },
        {
            "slideNumber": 83,
            "title": "Gazlı Gangren (Gas Gangrene): Clostridium Enfeksiyonu",
            "subtitle": "Clostridium perfringens, alfa-toksin (lesitinaz), gaz kabarcıkları ve krepitasyon",
            "badge": "Gazlı Gangren",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Gazlı gangren, genellikle toprakla kirlenmiş derin savaş veya kaza yaralanmaları sonrasında "
                "gelişen, klostridyal anaerobik enfeksiyonun yol açtığı özel ve feci bir gangren tipidir. "
                "En sık etken sporlu gram-pozitif anaerobik bir bakteri olan Clostridium perfringens'tir. "
                "Derin ve ezilmiş dokulardaki oksijensiz ortam sporların çimlenmesi için mükemmeldir.\n\n"
                "> [SINAV SPOTU] Bakterinin salgıladığı ölümcül ekzotoksin olan 'Alfa-toksin' (lesitinaz/fosfolipaz C), "
                "eritrosit ve kas zarlarındaki lesitini yıkarak masif miyonekroz ve hemolize yol açar.\n\n"
                "Bakteriler doku karbonhidratlarını fermente ederek gaz üretir; palpasyonda dokuda çıtırtı "
                "hissi ('krepitasyon') alınır ve radyografide kas planları arasında gaz kabarcıkları görülür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Clostridium perfringens", "desc": "Toprakta yaşayan anaerobik, sporlu gram-pozitif basildir.", "isKey": True},
                    {"title": "Alfa-Toksin (Lesitinaz)", "desc": "Membran fosfolipidlerini yıkan güçlü nekrotizan ve hemolitik enzimdir.", "isKey": True},
                    {"title": "Krepitasyon", "desc": "Doku altındaki gaz kabarcıklarının elle muayenede çıtırtı vermesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Gazlı Gangrenin Patolojik Basamakları",
                    "headers": ["Aşama", "Etken / Olay", "Klinik ve Morfolojik Bulgu"],
                    "rows": [
                        ["1. İnokülasyon", "Kirli derin travma, doku iskemisi", "Düşük redoks potansiyeli sporları aktive eder"],
                        ["2. Toksin Salınımı", "Alfa-toksin (Fosfolipaz C / Lesitinaz)", "Kas membranları parçalanır (Miyonekroz)"],
                        ["3. Gaz Fermantasyonu", "Bakteriyel anaerobik metabolizma", "Kas lifleri arasında çözünmeyen gaz kabarcıkları"],
                        ["4. Krepitasyon", "Elle palpasyon muayenesi", "Doku altında kar sesi / çıtırtı (krepitasyon)"],
                        ["5. Toksemik Şok", "Sistemik vasküler çöküş", "Masif hemoliz, hemoglobinüri, ölümcül şok"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gazlı gangrenin en sık etkeni Clostridium perfringens'tir; ana virülans faktörü hücre membranını yıkan Alfa-toksindir (lesitinaz).",
                "📌 [SINAV SPOTU] Gazlı gangrende doku palpasyonunda hissedilen çıtırtı hissine 'krepitasyon' denir; radyografide kaslar arası gaz görülür."
            ],
            "medicalTerms": [
                {"term": "Miyonekroz", "explanation": "İskelet kası liflerinin toksinler veya iskemi nedeniyle yaygın olarak nekroza uğramasıdır."},
                {"term": "Krepitasyon", "explanation": "Dokuda gaz birikimi olduğunda üzerine parmakla basıldığında duyulan çıtırtı sesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Gazlı Gangrenin Moleküler Patogenezi",
                    [
                        "1. Derin Kirli Yara: Ezilme travması dokuyu iskemik ve anaerobik hale getirir.",
                        "2. Spor Çimlenmesi: Clostridium perfringens sporları vejetatif forma döner ve ürer.",
                        "3. Alfa-Toksin Salınımı: Lesitinaz enzimi kas ve endotel hücre membranlarını parçalar.",
                        "4. Gaz Üretimi: Kas glikojenini fermente eden bakteriler dokuda gaz kabarcıkları biriktirir.",
                        "5. Krepitasyon ve Şok: Palpasyonda krepitasyon alınır, toksinler masif şok ve ölüme yol açar."
                    ]
                ),
                make_cloze(
                    "Clostridium perfringens'in salgıladığı ve kas membranlarındaki lesitini yıkarak miyonekroz yapan ekzotoksin alfa-toksindir.",
                    "alfa-toksindir",
                    "Bakteriyel Toksin"
                )
            ]
        },
        {
            "slideNumber": 84,
            "title": "Diyabetik Ayak ve Periferik Arter Hastalığı",
            "subtitle": "Nöropati, mikro/makroanjiyopati ve enfeksiyonun ölümcül üçgeni",
            "badge": "Klinik Patoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Klinik pratikte gangrenle en sık karşılaşılan hasta grubu diabetes mellitus (şeker hastalığı) "
                "hastalarıdır. Diyabetik ayakta gangren gelişimini tetikleyen şey tek bir mekanizma değil, "
                "üçlü bir ölümcül kısırdöngüdür: 1) Diyabetik Nöropati (ağrı ve dokunma duyusunun kaybı), "
                "2) Diyabetik Vaskülopati (ateroskleroz ve mikroanjiyopatiye bağlı ağır doku iskemisi), "
                "3) Bozulmuş İmmün Yanıt (hipergliseminin fagositozu felç etmesi).\n\n"
                "> [KLİNİK İPUCU] Hasta ayağındaki küçük bir vuruğu veya ayakkabı vurmasını hissetmez; "
                "iskemik doku hızla ülsere olur ve enfekte olarak ıslak gangrene dönüşür.\n\n"
                "Zamanında agresif antibiyoterapi ve cerrahi debridman yapılmazsa diz altı veya diz üstü "
                "amputasyon hayat kurtarıcı tek seçenek haline gelir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Duyusal Nöropati", "desc": "Ağrı duyusu kaybolduğu için travmaların fark edilmeyip büyümesidir.", "isKey": True},
                    {"title": "Arteriyel İskemi", "desc": "Tibial damarlardaki yaygın aterosklerozun kan akımını durdurmasıdır.", "isKey": True},
                    {"title": "İmmün Felç", "desc": "Yüksek şekerin nötrofil fagositoz ve kemotaksisini bozmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Diyabetik Gangrenin Üçlü Sacayağı",
                    "headers": ["Bileşen", "Patofizyolojik Mekanizma", "Klinik Yansıma"],
                    "rows": [
                        ["Periferik Nöropati", "Sorbiitol birikimi, miyelin kaybı", "Ağrısız bası ülserleri (Mal perforans)"],
                        ["Makroanjiyopati", "Hızlanmış ve yaygın ateroskleroz", "Distal nabızların kaybı, soğuk ekstremite, iskemi"],
                        ["Mikroanjiyopati", "Kapiller bazal membran kalınlaşması", "Dokuya lökosit ve oksijen difüzyonunun bozulması"],
                        ["İmmün Disfonksiyon", "Nötrofil kemotaksis ve fagositoz bozukluğu", "Hafif yaranın hızla flegmon ve ıslak gangrene ilerlemesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Diyabetik ayak patogenezinde rol oynayan 3 ana faktör: Periferik nöropati (duyu kaybı), Periferik vaskülopati (iskemi) ve Enfeksiyona yatkınlıktır.",
                "📌 [KLİNİK İPUCU] Diyabetik nöropati nedeniyle ülserler ağrısızdır; bu durum hekime geç başvurulmasına ve gangrene yol açar."
            ],
            "medicalTerms": [
                {"term": "Diyabetik Mikroanjiyopati", "explanation": "Kronik hiperglisemide kapiller bazal membranların yaygın olarak kalınlaşmasıdır."},
                {"term": "Mal Perforans", "explanation": "Diyabetik ayakta ayak tabanında bası noktalarında açılan derin, ağrısız trofik ülserdir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Diyabetik ayak ülserlerinin hissedilmemesine ve gangrene ilerlemesine yol açan temel nörolojik defekt periferik duyusal nöropatidir.",
                    "periferik duyusal nöropatidir",
                    "Nörolojik Bozukluk"
                ),
                make_active_recall(
                    "Diyabet hastalarında iskemik dokunun enfeksiyona bu kadar hızlı teslim olup ıslak gangren geliştirmesinin immünolojik nedeni nedir?",
                    "Hiperglisemi nötrofillerin kemotaksisini, adezyonunu ve bakterisidal fagositoz yeteneğini felç eder; ayrıca kalınlaşmış bazal membranlar immünoglobulin ve lökositlerin dokuya geçişini sınırlar."
                )
            ]
        },
        {
            "slideNumber": 85,
            "title": "Gangren Tiplerinin Karşılaştırmalı Sentez Tablosu",
            "subtitle": "Kuru, Islak ve Gazlı gangrenin klinik ve patolojik ayırıcı tanısı",
            "badge": "Ayırıcı Tanı",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Gangren tiplerinin ayırıcı tanısı klinikte ve acil cerrahide saniyeler içinde verilmesi "
                "gereken hayati bir karardır. Kuru gangren steril ve stabildir; hastayı acil sepsise sokmaz "
                "ve demarkasyon hattı bellidir. Islak gangren ise kokuşma bakterileriyle sıvılaşmıştır; "
                "sınır belirsizdir ve hızla proksimale tırmanır.\n\n"
                "> [TEMEL İLKE] Gazlı gangren ise klostridyal ekzotoksinlerle hızla kasları eritir (miyonekroz); "
                "dokuda gaz kabarcıkları, krepitasyon ve saatler içinde ölüme götüren septik şokla seyreder.\n\n"
                "Aşağıdaki karşılaştırma tablosu bu üç formun tüm klinikopatolojik farklarını eksiksiz özetler."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Kuru Gangren", "desc": "Saf iskemik koagülatif nekroz, enfeksiyon yok, mumyalaşma var.", "isKey": True},
                    {"title": "Islak Gangren", "desc": "İkincil sıvılaşma nekrozu, ağır kokuşma, sınır belirsiz, sepsis riski.", "isKey": True},
                    {"title": "Gazlı Gangren", "desc": "Clostridium alfa-toksini, gaz kabarcıkları, miyonekroz, krepitasyon.", "isKey": True}
                ],
                "table": {
                    "title": "3 Gangren Tipinin Karşılaştırmalı Tablosu",
                    "headers": ["Özellik", "Kuru Gangren", "Islak Gangren", "Gazlı Gangren"],
                    "rows": [
                        ["Etiyoloji", "Arteriyel tıkanma (Ateroskleroz)", "Arter/ven tıkanması + Çürüme mikropları", "Clostridium perfringens enfeksiyonu"],
                        ["Temel Nekroz Tipi", "Koagülatif nekroz", "Koagülatif + Sıvılaşma nekrozu", "Miyonekroz + Gaz kavitasyonları"],
                        ["Doku Kıvamı / Renk", "Kuru, sert, büzüşmüş, siyah", "Şiş, ödemli, yumuşak, siyah-yeşil", "Koyu kırmızı-kahverengi, gazlı, süngerimsi"],
                        ["Koku ve Gaz", "Koku yok, gaz yok", "Ağır pis koku, gaz yok", "Tatlı-çürük koku, bol gaz kabarcığı"],
                        ["Krepitasyon", "YOKTUR", "YOKTUR", "VARDIR (çıtırtı hissi)"],
                        ["Demarkasyon Hattı", "Çok net ve keskin", "Belirsiz, sınır seçilemez", "Belirsiz, hızla kas planlarında yayılır"],
                        ["Aciliyet ve Prognoz", "Yarı-acil / Elektif cerrahi", "Acil cerrahi (Sepsis tehlikesi)", "Aşırı acil cerrahi + Hiperbarik O2"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Krepitasyon (çıtırtı) yalnızca Gazlı Gangrende pozitiftir; Kuru ve Islak gangrende gaz/krepitasyon görülmez.",
                "📌 [SINAV SPOTU] Demarkasyon hattı Kuru gangrende çok net iken Islak ve Gazlı gangrende belirsizdir."
            ],
            "medicalTerms": [
                {"term": "Hiperbarik Oksijen", "explanation": "Hastaya yüksek basınçta %100 oksijen solutarak anaerobik bakterileri öldüren tedavidir."},
                {"term": "Miyonekroz", "explanation": "İskelet kası liflerinin Clostridium toksinleriyle yaygın ve ölümcül parçalanmasıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Gangren Ayırıcı Tanı Tablosu",
                    ["Özellik", "Kuru Gangren", "Islak Gangren", "Gazlı Gangren"],
                    [
                        [("Enfeksiyon", False), ("YOK", False), ("VAR (Karışık flora)", True, "Bakteri"), ("VAR (Clostridium)", True, "Anaerop")],
                        [("Doku Hali", False), ("Mumyalaşmış kuru", False), ("Ödemli sıvılaşmış", True, "Çürümüş"), ("Gazlı miyonekroz", True, "Kaviteli")],
                        [("Krepitasyon", False), ("YOK", False), ("YOK", False), ("VAR (Çıtırtı sesi)", True, "Fizik Muayene")],
                        [("Sınır Çizgisi", False), ("Çok net ve keskin", False), ("Belirsiz ve yaygın", True, "Sınırsızlık"), ("Belirsiz ve fulminan", True, "Hızlı Yayılım")]
                    ]
                ),
                make_micro_quiz(
                    "Ağır bacak ezilmesi sonrası yara yerinde hızla ilerleyen koyu renkli doku nekrozu, tatlımsı çürük kokusu ve palpasyonda belirgin çıtırtı hissi (krepitasyon) saptanan hastada en olası tanı ve en sık etken hangisidir?",
                    {
                        "A": "Kuru gangren - Ateroskleroz",
                        "B": "Islak gangren - Pseudomonas aeruginosa",
                        "C": "Gazlı gangren - Clostridium perfringens",
                        "D": "Kazeöz nekroz - Mycobacterium tuberculosis",
                        "E": "Koagülatif nekroz - Candida albicans"
                    },
                    "C",
                    {
                        "A": "Kuru gangrende krepitasyon ve kötü koku olmaz.",
                        "B": "Islak gangrende krepitasyon görülmez.",
                        "C": "Doğru cevap C'dir: Gaz kabarcıkları ve krepitasyon Clostridium perfringens'in gazlı gangrenine özgüdür.",
                        "D": "Tüberküloz akciğerde peynirleşme yapar, kas ezilmesinde krepitasyon yapmaz.",
                        "E": "Kandida mantardır ve gazlı miyonekroz yapmaz."
                    }
                )
            ]
        },
        {
            "slideNumber": 86,
            "title": "Fournier Gangreni: Perine ve Genital Bölgenin Nekrotizan Enfeksiyonu",
            "subtitle": "Polimikrobiyal nekrotizan fasiit, fulminan seyir ve skrotal yıkım",
            "badge": "Acil Patoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Fournier gangreni, perine, skrotum ve perianal bölgede hızla ilerleyen, polimikrobiyal "
                "(aerop + anaerop karma flora) bir nekrotizan fasiit ve gangrenöz nekroz tablosudur. "
                "En sık kontrolsüz diyabetik erkeklerde, kronik alkoliklerde ve immünsüprese bireylerde "
                "görülür. Genellikle küçük bir perianal apse, kıl dönmesi veya ürolojik travma ile tetiklenir.\n\n"
                "> [TEMEL İLKE] Bakterilerin saldığı sinerjistik enzimler, Colles ve Dartos fasiyaları boyunca "
                "saatte birkaç santimetre hızla ilerleyerek mikrovasküler tromboza ve masif cilt nekrozuna yol açar.\n\n"
                "Doku palpasyonunda krepitasyon alınabilir; lezyon saatler içinde karın ön duvarına kadar "
                "tırmanır. Acil ve agresif cerrahi debridman yapılmazsa mortalite %50'nin üzerindedir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Perineal Gangren", "desc": "Skrotum, penis ve perineyi tutan agresif nekrotizan fasiittir.", "isKey": True},
                    {"title": "Polimikrobiyal Sinerji", "desc": "E. coli, Klebsiella, streptokoklar ve Bacteroides türlerinin ortak yıkımıdır.", "isKey": True},
                    {"title": "Fasiyal Yayılım", "desc": "Enfeksiyonun anatomik fasya planları boyunca hızla tırmanmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Fournier Gangreninin Klinikopatolojik Evreleri",
                    "headers": ["Evre", "Klinik Görünüm", "Altta Yatan Doku Patolojisi"],
                    "rows": [
                        ["Erken Evre", "Perinede ağrılı, kızarık, ödemli cilt", "Derin fasyada bakteriyel çoğalma, erken lökosit sızması"],
                        ["İlerleme (24-48 st)", "Mor-siyah büller, deride krepitasyon", "Subkutan damar trombozu, doku iskemisi ve gaz oluşumu"],
                        ["Fulminan Gangren", "Masif cilt dökülmesi, çürümüş fasya", "Tam kat sıvılaşma ve gangrenöz nekroz, septik şok"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Fournier gangreni: Perine ve genital bölgenin hızla yayılan, polimikrobiyal nekrotizan fasiiti ve gangrenöz nekrozudur.",
                "📌 [KLİNİK İPUCU] Skrotal ağrısı ve yüksek ateşi olan bir diyabet hastasında perinede krepitasyon hissedilmesi acil cerrahi endikasyonudur."
            ],
            "medicalTerms": [
                {"term": "Fournier Gangreni", "explanation": "Erkek ve kadın perine/genital bölgesinde fasyaları yıkan fulminan nekrotizan enfeksiyondur."},
                {"term": "Nekrotizan Fasiit", "explanation": "Cilt altı yağ dokusunu ve kas fasyalarını hızla eriterek ilerleyen ölümcül yumuşak doku enfeksiyonudur."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Perine ve skrotumu tutan polimikrobiyal fulminan nekrotizan gangrenöz enfeksiyona Fournier gangreni adı verilir.",
                    "Fournier gangreni",
                    "Özel Gangren"
                ),
                make_active_recall(
                    "Fournier gangreninde enfeksiyonun saatler içinde karın ön duvarına kadar hızla yayılabilmesinin anatomik nedeni nedir?",
                    "Skrotumun Dartos fasyası ile perinenin Colles fasyasının karın ön duvarındaki Scarpa fasyası ile anatomik olarak kesintisiz bir devamlılık göstermesidir; bakteriler bu fasya planında hiçbir engel olmadan ilerler."
                )
            ]
        },
        {
            "slideNumber": 87,
            "title": "Gangrende Demarkasyon Hattı ve Cerrahi Karar",
            "subtitle": "Kuru gangrende otoamputasyon, ıslak gangrende acil eksizyon",
            "badge": "Cerrahi Patoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Gangrenöz nekrozda cerrahın amputasyon (uzvun kesilmesi) kararı ve zamanlaması, gangrenin "
                "türüne ve demarkasyon hattının durumuna doğrudan bağlıdır. Kuru gangrende demarkasyon hattı "
                "çok netleştiğinde, canlı doku sınırındaki makrofajlar ve granülasyon dokusu ölü dokuyu "
                "yavaşça ayırır; bazen parmak kendiliğinden düşer (otoamputasyon).\n\n"
                "> [TEMEL İLKE] Kuru gangrende cerrahi amputasyon, demarkasyon hattının tam olgunlaşması "
                "beklenerek ve canlı doku sınırından elektif şartlarda yapılabilir.\n\n"
                "Islak veya gazlı gangrende ise demarkasyon hattı BEKLENMEZ; çünkü enfeksiyon her saniye "
                "yukarı tırmanır. Canlı doku payı bırakılarak acilen proksimalden radikal amputasyon "
                "yapılmazsa hasta septik şoktan kaybedilir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Demarkasyon Beklentisi", "desc": "Kuru gangrende sınırın olgunlaşması beklenir; ıslakta asla beklenmez.", "isKey": True},
                    {"title": "Otoamputasyon", "desc": "Kuru gangrenli parmağın canlı sınır boyunca kendiliğinden kopup düşmesidir.", "isKey": False},
                    {"title": "Acil Amputasyon", "desc": "Islak ve gazlı gangrende sepsisi durdurmak için derhal uygulanan cerrahidir.", "isKey": True}
                ],
                "table": {
                    "title": "Gangren Tiplerinde Cerrahi Yönetim",
                    "headers": ["Gangren Tipi", "Demarkasyon Hattı", "Cerrahi Yaklaşım ve Zamanlama"],
                    "rows": [
                        ["Kuru Gangren", "Net, belirgin, inflamatuar sınır", "Elektif cerrahi amputasyon veya otoamputasyon takibi"],
                        ["Islak Gangren", "Yok, belirsiz, yukarı ilerleyen sınır", "ACİL cerrahi debridman / Proksimal amputasyon"],
                        ["Gazlı Gangren", "Yok, fasyal planlarda hızla yayılan", "AŞIRI ACİL geniş radikal eksizyon + Fasyotomi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kuru gangrende belirgin demarkasyon hattı oluşur ve elektif cerrahi planlanabilir; Islak gangrende sınır yoktur ve acil cerrahi şarttır.",
                "📌 [KLİNİK İPUCU] Islak gangrende demarkasyon hattının oluşmasını beklemek malpraktistir; hasta sepsisten ölür."
            ],
            "medicalTerms": [
                {"term": "Debridman", "explanation": "Yara veya enfeksiyon alanındaki tüm nekrotik, enfekte ve yabancı dokuların cerrahi olarak kesilip temizlenmesidir."},
                {"term": "Fasyotomi", "explanation": "Kas kompartmanlarındaki yüksek basıncı ve iskemiyi rahatlatmak için fasyanın cerrahi olarak yarılmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Cerrahi Amputasyon Zamanlaması",
                    "Kuru Gangrende Yaklaşım",
                    "Islak Gangrende Yaklaşım",
                    [
                        "Demarkasyon hattı beklenir",
                        "Sistemik toksisite riski düşüktür",
                        "Elektif ve planlı amputasyon yapılır",
                        "Otoamputasyon dahi gelişebilir"
                    ],
                    [
                        "Demarkasyon hattı ASLA beklenmez",
                        "Sepsis ve toksik şok riski çok yüksektir",
                        "Acil saatler içinde amputasyon yapılır",
                        "Geniş sağlam cerrahi sınır hedeflenir"
                    ]
                ),
                make_cloze(
                    "Kuru gangrende ölü dokunun canlı sınır boyunca cerrahiye gerek kalmadan kendiliğinden kopmasına otoamputasyon denir.",
                    "otoamputasyon",
                    "Doğal Ayrılma"
                )
            ]
        },
        {
            "slideNumber": 88,
            "title": "Gangren Tanısında Laboratuvar ve Radyolojik Bulgular",
            "subtitle": "Direkt grafide doku gazı, lökositoz ve anaerobik kültürler",
            "badge": "Laboratuvar",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Gangren şüphesi olan bir hastada tanının doğrulanması ve derin doku yayılımının haritalanması "
                "için laboratuvar ve radyolojik testler eşgüdümle kullanılır. Kuru gangrende laboratuvar "
                "genellikle sakindir; lökositoz hafiftir veya yoktur. Ancak ıslak ve gazlı gangrende "
                "masif bir sistemik inflamatuar yanıt tablosu (SIRS) hakimdir.\n\n"
                "> [TEMEL İLKE] Gazlı gangrende çekilen direkt konvansiyonel röntgende veya BT'de, kas fasikülleri "
                "ve subkutan doku planları arasında tüy benzeri 'radyolusent gaz kabarcıkları' açıkça izlenir.\n\n"
                "Kanda aşırı lökositoz (sola kayma), CRP yüksekliği, metabolik asidoz ve rabdomiyoliz "
                "nedeniyle kreatin kinaz (CK) patlaması görülür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Doku Gazı (Radyoloji)", "desc": "Direkt grafide kas ve fasya planlarında siyah gaz ceplerinin görülmesidir.", "isKey": True},
                    {"title": "Lökosit Sola Kayması", "desc": "Kemik iliğinden dolaşıma immatür nötrofillerin fırlamasıdır.", "isKey": True},
                    {"title": "Kreatin Kinaz (CK)", "desc": "Miyonekroza bağlı çizgili kas enzimlerinin dolaşıma taşmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Gangrende Tanısal İncelemeler",
                    "headers": ["Test / İnceleme", "Beklenen Pozitif Bulgu", "Klinik Anlam"],
                    "rows": [
                        ["Direkt Düz Röntgen", "Yumuşak doku ve kas içinde gaz cepleri", "Gazlı gangren veya gaz oluşturan mikst enfeksiyon"],
                        ["Tam Kan Sayımı (Hemogram)", "Belirgin lökositoz (>20.000) ve toksik granülasyon", "Sistemik inflamatuar yanıt ve sepsis"],
                        ["Serum Kreatin Kinaz (CK)", "Binlerce üniteye ulaşan masif yükselme", "Kas liflerinin parçalandığı (Miyonekroz) kanıtı"],
                        ["Gram Boyası (Yara akıntısı)", "Geniş gram-pozitif basiller, lökosit yokluğu", "Clostridium perfringens morfolojisi (toksin nötrofilleri lize eder)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Direkt röntgende yumuşak dokuda gaz gölgelerinin (radyolusensi) izlenmesi Gazlı Gangrenin en değerli radyolojik bulgusudur.",
                "📌 [YÜKSEK VERİM] Gazlı gangren akıntısının Gram boyamasında gram-pozitif basiller görülürken lökositlerin görülmemesi dikkat çekicidir; çünkü alfa-toksin nötrofilleri de parçalar."
            ],
            "medicalTerms": [
                {"term": "Radyolusent", "explanation": "Röntgen ışınlarını tutmayan ve filmde siyah/koyu görünen hava veya gaz alanlarıdır."},
                {"term": "Sola Kayma (Bandemi)", "explanation": "Enfeksiyona yanıt olarak kanda genç çomak (band) nötrofil oranının artmasıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Gangren Laboratuvarı",
                    ["İnceleme", "Pozitif Bulgu", "Klinik Çıkarım"],
                    [
                        [("Direkt Grafi", False), ("Yumuşak dokuda gaz cepleri", True, "Röntgen"), ("Gazlı gangren tanısı", False)],
                        [("Kreatin Kinaz (CK)", False), ("Masif enzim artışı", True, "Kas Enzimi"), ("Miyonekroz kanıtı", False)],
                        [("Lökosit Sayımı", False), ("Aşırı lökositoz (>20.000)", True, "Hemogram"), ("Sepsis tehdidi", False)],
                        [("Gram Boyası", False), ("Gram(+) sporlu basiller", True, "Mikrobiyoloji"), ("Clostridium türleri", False)]
                    ]
                ),
                make_cloze(
                    "Gazlı gangrende direkt radyografide yumuşak doku ve kas fasikülleri arasında gaz kabarcıkları izlenir.",
                    "gaz kabarcıkları",
                    "Radyolojik Bulgu"
                )
            ]
        },
        {
            "slideNumber": 89,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Gangrenöz Nekroz ve Tipleri",
            "subtitle": "Kuru, ıslak ve gazlı gangren, diyabetik ayak, alfa-toksin ve amputasyon",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 9,
            "synthesisNarrative": (
                "Dokuzuncu kontrol noktasında, klinikte en sık karşılaşılan nekroz formlarından olan "
                "gangrenöz nekrozu tüm tipleriyle özetliyoruz. Gangren bağımsız bir histolojik tip değil, "
                "cerrahi klinik bir terimdir. Temelinde iskemik koagülatif nekroz yatar.\n\n"
                "> [ÖZET VURGU] Kuru gangren steril ve mumyalaşmıştır; Islak gangren süperenfeksiyonlu "
                "sıvılaşma nekrozudur; Gazlı gangren ise Clostridium alfa-toksiniyle oluşan gazlı miyonekrozdur.\n\n"
                "Aşağıdaki 3 akıl kartını dikkatle inceleyerek bu cerrahi patoloji bilgilerini hafızanıza sabitleyin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Klinik Terim", "desc": "Gangren histolojik tip değil, ekstremitedeki geniş iskemik nekrozdur.", "isKey": True},
                    {"title": "3 Tipik Form", "desc": "Kuru (mumyalaşmış), Islak (sıvılaşmış), Gazlı (Clostridium krepitasyonu).", "isKey": True},
                    {"title": "Acil Ayrım", "desc": "Kuru gangrende elektif cerrahi; ıslak ve gazlı gangrende acil amputasyon.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 9 Sentez Tablosu",
                    "headers": ["Gangren Tipi", "Temel Mekanizma", "Kritik Klinik Ayıraç"],
                    "rows": [
                        ["Kuru Gangren", "Arteriyel tıkanma, steril kuruma", "Belirgin demarkasyon hattı, mumyalaşma"],
                        ["Islak Gangren", "Bakteri süperenfeksiyonu + sıvılaşma", "Ağır kokuşma, sınır belirsiz, sepsis tehlikesi"],
                        ["Gazlı Gangren", "Clostridium perfringens alfa-toksini", "Kas nekrozu, gaz kabarcıkları, krepitasyon"],
                        ["Fournier Gangreni", "Perineal polimikrobiyal nekrotizan fasiit", "Skrotal gangren, yüksek mortalite"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gangrenöz nekroz klinik bir terimdir; temelde koagülatif nekrozdur, enfeksiyon eklenince sıvılaşma nekrozu kazanır.",
                "📌 [SINAV SPOTU] Krepitasyon ve doku içi gaz yalnızca Gazlı Gangrende (Clostridium perfringens) görülür."
            ],
            "medicalTerms": [
                {"term": "Demarkasyon Hattı", "explanation": "Kuru gangrende canlı doku ile nekrotik dokuyu ayıran keskin inflamatuar sınırdır."},
                {"term": "Krepitasyon", "explanation": "Doku altındaki gaz kabarcıklarının elle basıldığında oluşturduğu çıtırtı sesidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-025",
                    "Gangrenöz nekroz neden 'bağımsız bir histolojik nekroz tipi' olarak kabul edilmez?",
                    "Çünkü hücresel düzeyde yeni bir ölüm mekanizması içermez; temelde iskemik koagülatif nekrozdur ve üzerine bakteri bindiğinde sıvılaşma nekrozu eklenir. Genellikle cerrahlar tarafından uzuv nekrozunu tanımlamak için kullanılan klinik bir terimdir."
                ),
                make_flashcard(
                    "fc-k1-04-026",
                    "Kuru gangren ile ıslak gangren arasındaki en kritik cerrahi ve patolojik fark nedir?",
                    "Kuru gangren bakteriyel enfeksiyon içermez, steril ve mumyalaşmıştır, doku ile canlı parankim arasında belirgin bir demarkasyon hattı vardır; ıslak gangrende ise çürüme bakterileri sıvılaşma nekrozu yapar, demarkasyon hattı yoktur ve hızla ilerleyerek fatal sepsise yol açar."
                ),
                make_flashcard(
                    "fc-k1-04-027",
                    "Gazlı gangrende kas nekrozuna ve gaz kabarcıklarına yol açan temel mikrobiyolojik etken ve virülans faktörü nedir?",
                    "Etken anaerobik bir bakteri olan Clostridium perfringens'tir; temel virülans faktörü ise hücre zarlarındaki lesitini parçalayan ve miyonekroza yol açan fosfolipaz C enzim yapısındaki Alfa-toksindir."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 9 Sentezi: Bir diyabet hastasının ayağındaki kuruyan gangrenli parmak aniden kötü kokulu, şiş ve akıntılı hale gelirse ne olmuştur?",
                    "Steril koagülatif nekroz tablosu olan 'kuru gangren', piyojenik ve anaerobik bakterilerin kolonize olmasıyla ikincil sıvılaşma nekrozunun eklendiği ölümcül 'ıslak gangrene' dönüşmüştür; hasta acil cerrahi adayıdır."
                ),
                make_cloze(
                    "Kuru gangren tablosuna bakteri enfeksiyonu eklendiğinde tablo hızla ıslak gangrene dönüşür.",
                    "ıslak gangrene",
                    "Gangren Dönüşümü"
                )
            ]
        }
    ]
