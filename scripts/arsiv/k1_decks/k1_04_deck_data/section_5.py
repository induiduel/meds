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
            "slideNumber": 40,
            "title": "Hücre Ölümü Spektrumu: Nekroz ile Apoptozun Temel Ayrımı",
            "subtitle": "Kazara feci ölüm ile programlı temiz hücresel intiharın karşılaştırması",
            "badge": "Hücre Ölümü",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre ölümü canlı dokuda iki ana morfolojik ve biyokimyasal yolla gerçekleşir: Nekroz ve "
                "Apoptoz. Bu iki ölüm biçimi gerek tetikleyici nedenleri gerekse dokuda yarattıkları "
                "sonuçlar açısından birbirinin tam zıddıdır. Nekroz, ağır iskemi, toksin veya fiziksel travma "
                "sonucu enerji metabolizmasının çökmesiyle gelişen 'kazara' (accidental) hücre ölümüdür.\n\n"
                "> [TEMEL İLKE] Nekroz HER ZAMAN patolojiktir; hücre şişer, zarları parçalanır, içerik dışarı "
                "sızar ve çevre dokuda kaçınılmaz olarak yoğun bir lökositik İNFLAMASYON başlar.\n\n"
                "Apoptoz ise hücresel intihar programıdır; fizyolojik veya patolojik olabilir, hücre büzülür, "
                "zarlar sağlam kalır ve inflamasyon asla oluşmaz."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Nekroz", "desc": "Daima patolojik, membran parçalanır, hücre şişer, belirgin inflamasyon vardır.", "isKey": True},
                    {"title": "Apoptoz", "desc": "Fizyolojik veya patolojik, membran intaktır, hücre büzülür, sıfır inflamasyon.", "isKey": True},
                    {"title": "İnflamasyon Farkı", "desc": "Hücre içeriğinin dışarı saçılması nekrozu inflamatuar bir fırtınaya çevirir.", "isKey": True}
                ],
                "table": {
                    "title": "Nekroz ve Apoptozun Temel Karşılaştırması",
                    "headers": ["Özellik", "Nekroz", "Apoptoz"],
                    "rows": [
                        ["Hücre Boyutu", "Şişmiş (irileşmiş)", "Büzülmüş (küçülmüş)"],
                        ["Hücre Zarı", "Parçalanmış, geçirgen, delik", "Bütünlüğü korunmuş, apoptotik cisimcikler"],
                        ["Hücre İçi İçerik", "Dışarı sızar, otolizle sindirilir", "Apoptotik cisimciklerde paketlenir"],
                        ["İnflamatuar Yanıt", "Belirgin, yoğun nötrofilik", "YOKTUR (temiz makrofaj fagositozu)"],
                        ["Fizyolojik / Patolojik", "DAİMA patolojiktir", "Fizyolojik (embriyogenez) veya patolojik"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekroz daima patolojiktir ve her zaman çevre dokuda inflamasyona yol açar; apoptoz ise inflamasyon oluşturmaz.",
                "📌 [SINAV SPOTU] Nekrozda hücre şişer ve patlar; apoptozda hücre büzülür ve apoptotik cisimciklere bölünür."
            ],
            "medicalTerms": [
                {"term": "Nekroz", "explanation": "Hücre zarlarının parçalanması ve lizozomal enzimlerin sızmasıyla oluşan daima patolojik hücre ölümüdür."},
                {"term": "Apoptotik Cisimcik", "explanation": "Apoptoza giden hücrenin organellerini içeren, zarla çevrili paketlenmiş parçacıklardır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Nekroz ile Apoptozun Kesin Ayrımı",
                    "Nekroz (Patolojik Yıkım)",
                    "Apoptoz (Programlı İntihar)",
                    [
                        "Daima patolojiktir",
                        "Hücre şişer ve lizise uğrar",
                        "Hücre zarı yırtılır ve içerik sızar",
                        "Çevre dokuda yoğun inflamasyon olur",
                        "Enerji tükenmesi (ATP yokluğu) vardır"
                    ],
                    [
                        "Fizyolojik veya patolojik olabilir",
                        "Hücre büzülür ve yoğunlaşır",
                        "Hücre zarı sağlam kalır",
                        "Asla inflamasyon oluşmaz",
                        "ATP bağımlı aktif enzim kaskadı çalışır"
                    ]
                ),
                make_cloze(
                    "Nekroz hücre zarlarının parçalanması nedeniyle çevre dokuda daima yoğun bir inflamasyon reaksiyonu başlatır.",
                    "inflamasyon",
                    "Doku Yanıtı"
                )
            ]
        },
        {
            "slideNumber": 41,
            "title": "Nekrozun Tanımı ve Doku Düzeyindeki Sonuçları",
            "subtitle": "Canlı organizmada doku ölümü, enzim salınımı ve lökosit göçü",
            "badge": "Patoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patolojide nekroz, canlı bir organizmada hücrelerin veya dokuların geri dönüşümsüz olarak "
                "ölmesi ve bunu takiben hücrenin kendi lizozomal enzimleri ile çevreye göç eden inflamatuar "
                "hücrelerin enzimleri tarafından parçalanması sürecidir. Nekroz terimi canlı bir bedendeki "
                "doku ölümü için kullanılır; ölümden sonra tüm bedende gelişen erimeye ise postmortem otoliz denir.\n\n"
                "> [TEMEL İLKE] Nekrotik hücrelerden çevreye dökülen moleküler kalıntılar (DAMP: Hasarla ilişkili "
                "moleküler paternler), çevre damarlardaki lökositleri bölgeye çeken kemotaktik sinyaller yayar.\n\n"
                "Bölgeye dolan nötrofiller ve makrofajlar nekrotik enkazı temizlemek için fagositoz yapar; "
                "ardından granülasyon dokusu ve fibrozis (skar) ile yara onarımı başlatılır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Canlı Dokuda Ölüm", "desc": "Nekroz canlı organizmada gerçekleşir ve çevre doku canlıdır.", "isKey": True},
                    {"title": "DAMP Molekülleri", "desc": "Ölü hücreden saçılan ATP, DNA ve HMGB1 lökositleri uyarır.", "isKey": True},
                    {"title": "Skar Oluşumu", "desc": "Nekrotik alan temizlendikten sonra yerini fibröz bağ dokusuna bırakır.", "isKey": False}
                ],
                "table": {
                    "title": "Nekrozun Doku Aşamaları",
                    "headers": ["Aşama", "Zaman Aralığı", "Baskın Hücresel Olay"],
                    "rows": [
                        ["Akut Nekroz", "0 - 24 saat", "Zar rüptürü, enzim salınımı, DAMP molekülleri yayılımı"],
                        ["Akut İnflamasyon", "24 - 72 saat", "Masif nötrofil infiltrasyonu, otoliz ve heteroliz"],
                        ["Kronik Temizlenme", "3 - 7 gün", "Makrofaj fagositozu, nekrotik enkazın yutulması"],
                        ["Onarım ve Skar", "1 - 6 hafta", "Anjiyogenez, fibroblast göçü, kollajen birikimi (skar)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekroz canlı dokuda meydana gelen hücre ölümüdür; çevresinde mutlaka canlı dokunun verdiği inflamatuar reaksiyon bulunur.",
                "📌 [YÜKSEK VERİM] Nekrotik hücrelerin saldığı DAMP molekülleri nötrofilleri uyararak steril nekrozda bile yoğun inflamasyon başlatır."
            ],
            "medicalTerms": [
                {"term": "DAMP", "explanation": "Damage-Associated Molecular Patterns; hasarlı hücrelerden salınıp lökositleri uyaran endojen moleküllerdir."},
                {"term": "Skar", "explanation": "Nekroza uğrayan parankim dokusunun yerine oluşan kollajenden zengin fibröz bağ dokusudur."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Nekrotik hücrelerden salınarak mikrosirkülasyondaki lökositleri bölgeye çeken endojen tehlike sinyallerine DAMP molekülleri denir.",
                    "DAMP molekülleri",
                    "İmmün Sinyal"
                ),
                make_active_recall(
                    "Canlı bir organizmadaki 'Nekroz' ile ölüm sonrası gelişen 'Postmortem Otoliz' arasındaki en kritik patolojik fark nedir?",
                    "Nekroz canlı organizmada gerçekleşir ve nekrotik alanın çevresinde mutlaka canlı dokunun verdiği damarsal ve hücresel bir İNFLAMASYON yanıtı bulunur; postmortem otolizde ise tüm canlılık bittiği için sıfır inflamasyon vardır."
                )
            ]
        },
        {
            "slideNumber": 42,
            "title": "Doku Nekrozu Kalıpları: Morfolojik Sınıflandırma",
            "subtitle": "Koagülatif, likefaksiyon, gangrenöz, kazeöz, yağ ve fibrinoid nekroz",
            "badge": "Sınıflandırma",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Büyük bir doku parçası veya tüm bir organ segmenti nekroza uğradığında, dokunun makroskobik "
                "ve mikroskobik görünümü lezyonun etiyolojisine göre son derece tipik morfolojik kalıplar "
                "oluşturur. Tıbbi patolojide 6 klasik doku nekrozu kalıbı tanımlanmıştır: 1) Koagülatif nekroz, "
                "2) Sıvılaşma (likefaksiyon) nekrozu, 3) Gangrenöz nekroz, 4) Kazeöz nekroz, 5) Yağ nekrozu, "
                "6) Fibrinoid nekroz.\n\n"
                "> [TEMEL İLKE] Bu derste (Hücre Hasarı ve Nekroz - I) klinik patolojide en sık karşılaşılan "
                "ilk üç kalıp olan koagülatif, sıvılaşma ve gangrenöz nekroz ayrıntılı olarak incelenecektir.\n\n"
                "Her bir nekroz tipi hekime altta yatan etken (iskemi, bakteri, tüberküloz, immün reaksiyon) "
                "hakkında çok güçlü ipuçları sağlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Morfolojik Kalıplar", "desc": "Nekrozun makro ve mikro görüntüsü etiyolojik mekanizmayı yansıtır.", "isKey": True},
                    {"title": "En Sık Tip", "desc": "Koagülatif nekroz, iskemik enfarktların evrensel kalıbıdır.", "isKey": True},
                    {"title": "İkincil Tipler", "desc": "Kazeöz, yağ ve fibrinoid nekroz sonraki derslerde derinleştirilecektir.", "isKey": False}
                ],
                "table": {
                    "title": "6 Klasik Doku Nekrozu Kalıbı",
                    "headers": ["Nekroz Kalıbı", "Temel Mekanizma", "En Tipik Klinik Örnek"],
                    "rows": [
                        ["Koagülatif Nekroz", "Protein denatürasyonu baskın", "Miyokard, böbrek ve dalak enfarktları"],
                        ["Sıvılaşma (Likefaksiyon)", "Enzimatik sindirim baskın", "Beyin infarktı, piyojenik apseler"],
                        ["Gangrenöz Nekroz", "İskemi + sekonder enfeksiyon", "Diyabetik ayak, alt ekstremite kangreni"],
                        ["Kazeöz Nekroz", "Granülomatoz immün yıkım", "Tüberküloz enfeksiyonu (akciğer/lenf nodu)"],
                        ["Yağ Nekrozu", "Lipazların trigliseritleri yıkması", "Akut pankreatit, travmatik meme yağı hasarı"],
                        ["Fibrinoid Nekroz", "İmmün kompleks ve fibrin çökmesi", "Malign hipertansiyon, vaskülitler"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Tıbbi patolojide 6 doku nekrozu kalıbı vardır; en sık görüleni iskemik enfarktlarda izlenen Koagülatif nekrozdur.",
                "📌 [YÜKSEK VERİM] Nekroz kalıbının doğru tanınması, etiyolojik ajanın aydınlatılmasında patoloğun en güçlü rehberidir."
            ],
            "medicalTerms": [
                {"term": "Enfarktüs", "explanation": "Arteriyel tıkanma veya venöz drenaj kesilmesi sonucu bir dokuda gelişen iskemik nekroz alanıdır."},
                {"term": "Likefaksiyon", "explanation": "Nekrotik dokunun güçlü litik enzimler tarafından tamamen eritilerek viskoz sıvıya dönüştürülmesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Nekroz Kalıpları Özeti",
                    ["Nekroz Tipi", "Baskın Mekanizma", "Tipik Lezyon"],
                    [
                        [("Koagülatif", False), ("Protein denatürasyonu", True, "Protein Çökmesi"), ("Miyokard enfarktüsü", False)],
                        [("Sıvılaşma", False), ("Enzimatik sindirim", True, "Litik Erime"), ("Beyin infarktı, apse", False)],
                        [("Gangrenöz", False), ("Geniş koagülatif iskemi", True, "Klinik Kangren"), ("Diyabetik ayak", False)],
                        [("Kazeöz", False), ("Peynirleşme nekrozu", True, "Granülom"), ("Tüberküloz", False)]
                    ]
                ),
                make_cloze(
                    "Tıbbi patolojide ve klinik uygulamada en sık karşılaşılan doku nekrozu kalıbı koagülatif nekrozdur.",
                    "koagülatif nekrozdur",
                    "En Sık Nekroz"
                )
            ]
        },
        {
            "slideNumber": 43,
            "title": "Koagülatif Nekroz: En Sık Görülen Nekroz Kalıbı",
            "subtitle": "İskemik dokularda protein denatürasyonunun enzimatik sindirime üstünlüğü",
            "badge": "Koagülatif",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Koagülatif nekroz, iskeminin neden olduğu hücresel ölümlerde ortaya çıkan en karakteristik "
                "ve en yaygın nekroz kalıbıdır. Beyin hariç, vücuttaki hemen hemen tüm katı parankimatöz "
                "organlarda (kalp, böbrek, dalak, karaciğer) arter tıkanması sonucu gelişen enfarktlar "
                "istisnasız koagülatif nekrozla seyreder.\n\n"
                "> [TEMEL İLKE] İskemi sırasında gelişen ağır asidoz, sadece yapısal proteinleri değil; "
                "ölü hücreleri sindirecek olan lizozomal litik enzimleri de denatüre eder (pıhtılaştırır).\n\n"
                "Enzimler de denatüre olduğu için hücre içi proteoliz gecikir; bu durum ölü dokunun "
                "sıvılaşmasını engeller ve doku sert, soluk, pişmiş et kıvamında kalır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "En Yaygın Tip", "desc": "Beyin dışındaki tüm katı organların iskemik enfarktüs kalıbıdır.", "isKey": True},
                    {"title": "Enzim Denatürasyonu", "desc": "Ağır asidozun lizozomal enzimleri bloke ederek doku erimesini geciktirmesidir.", "isKey": True},
                    {"title": "Sert Kıvam", "desc": "Protein pıhtılaşması nedeniyle dokunun pişmiş et gibi sert ve kuru kalmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Koagülatif Nekrozun Biyofiziksel Özellikleri",
                    "headers": ["Parametre", "Durum", "Biyolojik Gerekçe"],
                    "rows": [
                        ["Sıklık", "En sık görülen nekroz tipi", "Arteriyel tromboz ve embolilerin yaygınlığı"],
                        ["Doku Kıvamı", "Sert, katı, yoğun", "Denatüre proteinlerin pıhtılaşması"],
                        ["Doku Rengi", "Soluk, gri-beyaz veya sarımsı", "Vasküler perfüzyon kaybı ve protein koagülasyonu"],
                        ["Proteoliz Hızı", "Belirgin yavaşlamış ve gecikmiş", "Asidozun litik enzimleri de inaktive etmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Koagülatif nekroz en sık görülen nekroz tipidir; beyin hariç tüm katı organ iskemik enfarktlarında izlenir.",
                "📌 [SINAV SPOTU] Koagülatif nekrozun temel mekanizması, hem yapısal proteinlerin hem de litik enzimlerin asidozla denatüre olmasıdır."
            ],
            "medicalTerms": [
                {"term": "Protein Denatürasyonu", "explanation": "Yüksek asit veya ısıyla proteinlerin üçüncül yapısını kaybedip pıhtılaşmasıdır."},
                {"term": "Katı Parankim Organı", "explanation": "Geniş lümenli boşluk içermeyen, hücre yoğunluğu yüksek organlardır (kalp, böbrek, dalak)."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Koagülatif nekrozda dokunun hemen sıvılaşmamasının nedeni asidozun litik enzimleri de denatüre etmesidir.",
                    "litik enzimleri de denatüre etmesidir",
                    "Enzimatik Blokaj"
                ),
                make_micro_quiz(
                    "Koagülatif nekrozun patofizyolojisinde ölü dokunun günlerce sert ve mimarisini korur halde kalmasının ana nedeni aşağıdakilerden hangisidir?",
                    {
                        "A": "Bakterilerin aşırı kollajen üretmesi",
                        "B": "Ağır asidozun yapısal proteinlerle birlikte litik enzimleri de denatüre etmesi",
                        "C": "Kalsiyum pompalarının aşırı çalışması",
                        "D": "Dokuya aşırı miktarda nötrofil hücum etmesi",
                        "E": "Apoptoz kaspazlarının aşırı aktive olması"
                    },
                    "B",
                    {
                        "A": "Koagülatif nekrozda bakteri şart değildir.",
                        "B": "Doğru cevap B'dir: Ağır iskemik asidoz lizozomal enzimleri de denatüre ederek proteolizi geciktirir.",
                        "C": "Kalsiyum pompaları durmuştur.",
                        "D": "Nötrofiller ilk anda yoktur, günler sonra temizlemeye gelir.",
                        "E": "Koagülatif nekroz kaspaz bağımsız nekrotik bir tablodur."
                    }
                )
            ]
        },
        {
            "slideNumber": 44,
            "title": "Koagülatif Nekrozda Doku Mimarisinin Korunması: Hayalet Hücreler",
            "subtitle": "Çekirdek kaybı, korunmuş hücre konturları ve 'Tombstone' görünümü",
            "badge": "Histopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Koagülatif nekrozun mikroskop altındaki en büyüleyici ve karakteristik özelliği, doku "
                "mimarisinin en az birkaç gün boyunca neredeyse mükemmel bir şekilde KORUNMASIDIR. Hücreler "
                "biyokimyasal olarak tamamen ölmüştür, ancak yapısal iskelet pıhtılaşarak donup kalmıştır.\n\n"
                "> [SINAV SPOTU] Mikroskopta hücrelerin sınırları ve konturları seçilebilir, ancak çekirdekleri "
                "tamamen kaybolmuştur; bu hücrelere 'hayalet hücreler' (ghost cells) veya mezar taşı (tombstone) denir.\n\n"
                "Patolog kesite baktığında dokunun bir böbrek glomerülü veya miyokard çizgilenmesi olduğunu "
                "rahatlıkla tanıyabilir. Zamanla çevre dokudan lökositler bölgeye sızarak bu hayalet hücreleri yavaşça eritir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Mimari Korunması", "desc": "Ölü hücre konturlarının ve doku çatısının günlerce bozulmadan kalmasıdır.", "isKey": True},
                    {"title": "Hayalet Hücreler", "desc": "Çekirdeğini tamamen yitirmiş, yoğun eozinofilik pıhtılaşmış hücrelerdir.", "isKey": True},
                    {"title": "Tombstone Deseni", "desc": "Hücre sınırlarının mezar taşları gibi ayakta durmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Koagülatif Nekrozun Mikroskobik Bulguları",
                    "headers": ["Hücresel Bileşen", "Mikroskobik Durum", "Histolojik Terim"],
                    "rows": [
                        ["Hücre Dış Sınırları", "Belirgin, konturlar korunmuş", "Hücresel taslak (Outline)"],
                        ["Hücre Çekirdeği", "Piknoz, karyoreksis sonrası tamamen erimiş", "Nükleus kaybı (Akarion)"],
                        ["Sitoplazma", "Yoğun pembe, homojen, camsı", "Artmış eozinofili"],
                        ["Bütünsel Görünüm", "Çekirdeksiz ölü hücreler dizisi", "Hayalet hücreler (Ghost cells)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Koagülatif nekrozun mikroskobik damgası: Çekirdek kaybına rağmen hücre sınırlarının ve temel doku mimarisinin birkaç gün boyunca korunmasıdır.",
                "📌 [YÜKSEK VERİM] 'Hayalet hücreler' (ghost cells), koagülatif nekrozda konturu sağlam fakat nükleusu erimiş hücreleri tanımlar."
            ],
            "medicalTerms": [
                {"term": "Hayalet Hücre", "explanation": "Koagülatif nekrozda dış sınırları korunmuş fakat çekirdeği tamamen erimiş ölü hücre kalıntısıdır."},
                {"term": "Artmış Eozinofili", "explanation": "Denatüre sitoplazmik proteinlerin eozin boyasını aşırı bağlayarak koyu pembe-kırmızı boyanmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Doku vs Koagülatif Nekroz",
                    "Normal Sağlıklı Doku",
                    "Koagülatif Nekrotik Doku",
                    [
                        "Canlı bazofilik nükleuslar izlenir",
                        "Normal pembe granüllü sitoplazma",
                        "Aktif metabolizma ve bölünme yeteneği",
                        "İnflamatuar infiltrasyon yoktur"
                    ],
                    [
                        "Çekirdekler tamamen erimiş ve kaybolmuştur",
                        "Aşırı koyu pembe (eozinofilik) camsı sitoplazma",
                        "Hücre hatları korunmuş 'hayalet hücreler'",
                        "Çevrede nötrofilik infiltrasyon başlar"
                    ]
                ),
                make_cloze(
                    "Koagülatif nekrozda çekirdeğini kaybetmiş ancak hücresel dış konturları korunmuş hücrelere hayalet hücreler denir.",
                    "hayalet hücreler",
                    "Histopatolojik Terim"
                )
            ]
        },
        {
            "slideNumber": 45,
            "title": "Böbrek ve Dalak Enfarktüsü: Kama Şeklinde Koagülatif Nekroz",
            "subtitle": "Uç arter tıkanmaları, soluk infarkt ve hiperemik inflamatuar sınır",
            "badge": "Organ Patolojisi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Böbrek ve dalak, kollateral dolaşımı olmayan 'uç arter' (end-arter) sistemine sahip katı "
                "organlardır. Bir tromboemboli bu organların arteriyel dallarından birini tıkadığında, "
                "o damarın beslediği parankim alanında tipik bir koagülatif enfarktüs alanı gelişir. "
                "Bu alan damarlanma geometrisi nedeniyle daima 'kama şeklinde' (wedge-shaped) bir morfoloji sergiler.\n\n"
                "> [TEMEL İLKE] Kamanın tabanı organın dış kapsülüne, tepesi ise tıkanan arter dalının bulunduğu "
                "organ hilusuna doğru bakar; doku kansız kaldığı için 'soluk (anemik) enfarkt' olarak adlandırılır.\n\n"
                "Makroskopide enfarkt alanı soluk sarı-beyaz, sert ve keskin sınırlıdır. Lezyonun çevresinde "
                "canlı dokunun verdiği yangısal yanıtı gösteren kırmızı, hiperemik bir sınır kuşağı bulunur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Kama Şekli", "desc": "Tabanı kapsüle, apeksi tıkanan arteriyel dala bakan üçgen geometridir.", "isKey": True},
                    {"title": "Soluk Enfarkt", "desc": "Katı organlarda kanama olmaksızın gelişen anemik nekroz alanıdır.", "isKey": True},
                    {"title": "Hiperemik Sınır", "desc": "Nekrotik alanı çevreleyen canlı dokunun vazodilatasyon ve nötrofil kuşağıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Böbrek İskemik Enfarktüsünün Özellikleri",
                    "headers": ["Parametre", "Makroskobik Görünüm", "Mikroskobik Karşılık"],
                    "rows": [
                        ["Şekil", "Kama (üçgen) biçimli", "Tıkanan segmental arterin dallanma sahası"],
                        ["Merkez", "Soluk sarı-beyaz, kuru ve sert", "Koagüle olmuş tübül ve glomerül hayaletleri"],
                        ["Kenar Sınırı", "Kırmızı, konjesyone, kanamalı halka", "Genişlemiş canlı kapillerler ve nötrofiller"],
                        ["Geç Dönem", "Çökük, beyaz, yıldızsı skar", "Kollajenize bağ dokusu ile iyileşme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Böbrek ve dalak enfarktları tipik olarak kama (üçgen) şeklindedir; tabanı kapsüle, tepesi hilusa bakar.",
                "📌 [YÜKSEK VERİM] Katı organlarda tek damar tıkanmasıyla oluşan koagülatif enfarktlar soluk (beyaz) enfarkttır."
            ],
            "medicalTerms": [
                {"term": "Uç Arter (End-Arter)", "explanation": "Diğer damarlarla anastomoz yapmayan, tıkandığında enfarktüsü kaçınılmaz kılan arterdir."},
                {"term": "Soluk (Beyaz) Enfarkt", "explanation": "Katı dokularda kanama olmaksızın gelişen avasküler iskemik nekroz alanıdır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Atriyal fibrilasyonu olan 68 yaşındaki bir hastada aniden yan ağrısı ve hematüri gelişmesi senaryosu.",
                    [
                        {
                            "text": "Sol atriyumdan kopan trombüs renal arteri tıkamış ve böbrekte kama şeklinde soluk koagülatif enfarktüs yapmıştır.",
                            "isCorrect": True,
                            "feedback": "Mükemmel klinik patoloji teşhisi! Atriyal fibrilasyon tromboemboli kaynağıdır; böbrek uç arterli olduğu için kama biçimli koagülatif nekroz gelişir."
                        },
                        {
                            "text": "Böbrekte sıvılaşma nekrozu gelişmiş ve tüm böbrek apseye dönmüştür.",
                            "isCorrect": False,
                            "feedback": "Hatalı! Böbrek iskemisinde sıvılaşma değil koagülatif nekroz gelişir."
                        },
                        {
                            "text": "Böbrek hücreleri hızla hiperplaziye uğrayarak damarı genişletmiştir.",
                            "isCorrect": False,
                            "feedback": "Biyolojik olarak anlamsızdır."
                        }
                    ]
                ),
                make_cloze(
                    "Böbrek ve dalak gibi uç arterli katı organlarda gelişen iskemik enfarktüsler makroskobik olarak kama şeklinde görünür.",
                    "kama şeklinde",
                    "Geometrik Görünüm"
                )
            ]
        },
        {
            "slideNumber": 46,
            "title": "Miyokard Enfarktüsü: Kardiyak Koagülatif Nekroz",
            "subtitle": "Koroner arter trombozu, kas liflerinde dalgalanma ve koagülasyon",
            "badge": "Kardiyopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Miyokard enfarktüsü (kalp krizi), dünyada en sık ölüme yol açan koagülatif nekroz tablosudur. "
                "Koroner arterin aterosklerotik plağının rüptüre olması ve üzerine trombüs oturması sonucu "
                "beslenen miyokard alanı iskemik kalır. İskemi 20-30 dakikayı aştığında subendokardiyal "
                "bölgeden başlayarak transmural koagülatif nekroz dalgası yayılır.\n\n"
                "> [TEMEL İLKE] Işık mikroskobunda en erken değişiklik (ilk 1-3 saat), canlı kasın çekişiyle "
                "iskemik liflerin gerilmesi sonucu oluşan 'dalgalı kas lifleri' (wavy fibers) görünümüdür.\n\n"
                "4-12 saat sonra miyositlerde artmış sitoplazmik eozinofili, nükleer piknoz ve tipik koagülasyon "
                "nekrozu oturur; 12-24 saatte alana yoğun nötrofil infiltrasyonu başlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Dalgalı Kas Lifleri", "desc": "Canlı komşu kasların kasılmasıyla iskemik gevşek liflerin dalgalanmasıdır.", "isKey": True},
                    {"title": "Koagülasyon Tablosu", "desc": "4-12 saatte nükleusunu kaybetmiş yoğun pembe eozinofilik miyositlerdir.", "isKey": True},
                    {"title": "Nötrofil Yanıtı", "desc": "Ölü hücrelerin saldığı DAMP sinyalleriyle 1-3 günde masif lökosit göçüdür.", "isKey": False}
                ],
                "table": {
                    "title": "Miyokard Enfarktüsünün Histopatolojik Evreleri",
                    "headers": ["Zaman", "Mikroskobik Görünüm", "Klinik / Biyokimyasal Durum"],
                    "rows": [
                        ["0 - 30 dakika", "Işık mikroskobunda belirgin değişiklik yok", "Troponin kana sızmaya başlar, aritmi riski"],
                        ["1 - 4 saat", "Dalgalı lifler (wavy fibers), erken ödem", "Kontraktilite kaybı, ST elevasyonu"],
                        ["4 - 12 saat", "Erken koagülasyon nekrozu, artmış eozinofili", "Piknotik çekirdekler, marjinal nötrofiller"],
                        ["1 - 3 gün", "Tam koagülasyon nekrozu, yoğun nötrofiller", "Nükleus kaybı, sarı-kahverengi yumuşama"],
                        ["7 - 10 gün", "Granülasyon dokusu, makrofaj fagositozu", "Miyokard rüptürü için en riskli dönem!"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyokard enfarktüsünün en erken ışık mikroskobik bulgusu 'dalgalı lifler'dir (wavy fibers, 1-3 saat).",
                "📌 [SINAV SPOTU] Miyokard enfarktüsü klasik bir koagülatif nekrozdur; 4-12 saatte artmış eozinofili ve nükleer piknoz belirginleşir."
            ],
            "medicalTerms": [
                {"term": "Dalgalı Lifler", "explanation": "İskemik gevşemiş miyositlerin canlı komşu kaslar tarafından çekilerek dalgalı görünmesidir."},
                {"term": "Transmural Enfarkt", "explanation": "Nekrozun tüm ventrikül duvarı kalınlığı boyunca (endokarttan epikarda) uzanmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Miyokard Enfarktüsünün Mikroskobik Evreleri",
                    [
                        "1. 1-3 Saat: İskemik miyositler kasılamaz, canlı komşuların çekişiyle dalgalı lifler oluşur.",
                        "2. 4-12 Saat: Sitoplazmik proteinler koagüle olur, eozinofili artar ve nükleer piknoz başlar.",
                        "3. 1-3 Gün: Çekirdekler tamamen erir, alana masif nötrofil infiltrasyonu dolar.",
                        "4. 3-7 Gün: Makrofajlar ölü miyosit enkazını temizler; doku en kırılgan evresindedir.",
                        "5. 2-8 Hafta: Fibröz skar dokusu gelişerek ventrikül duvarında kalıcı kollajen bandı oluşturur."
                    ]
                ),
                make_cloze(
                    "Miyokard iskemisinde ilk 1-3 saatte ışık mikroskobunda izlenen en erken histolojik bulgu dalgalı lifler görünümüdür.",
                    "dalgalı lifler",
                    "Erken İskemik Bulgusu"
                )
            ]
        },
        {
            "slideNumber": 47,
            "title": "Büyük İstisna: Beyin İnfarktlarında Sıvılaşma Nekrozu",
            "subtitle": "İskemiye rağmen koagüle olamayan ve sıvılaşan santral sinir sistemi",
            "badge": "Kritik İstisna",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patoloji sınavlarının ve kurul komitelerinin en sevdiği, tıbbın en meşhur kurallarından "
                "biri şudur: Vücuttaki tüm katı organlar iskemik enfarktüste koagülatif nekroza uğrarken, "
                "SANTRAL SİNİR SİSTEMİ (BEYİN) İSKEMİK ENFARKTÜSÜNDE SIVILAŞMA (LİKEFAKSİYON) NEKROZU GÖRÜLÜR!\n\n"
                "> [KRİTİK UYARI] Beyin dokusu koagüle olamaz; çünkü beynin protein içeriği çok düşük, miyelin "
                "lipit içeriği ise son derece yüksektir ve otolitik hidrolitik enzimler son derece zengindir.\n\n"
                "İskemi sonucu ölen nöronlar ve glial hücreler hızla sıvılaşır; mikroglia ve makrofajlar "
                "lipitleri yutarak köpüksü 'lipid fagositleri' oluşturur ve geride kistik bir kavite kalır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Büyük İstisna", "desc": "İskemik nekroza uğradığı halde koagüle OLMAYAN tek organ beyindir.", "isKey": True},
                    {"title": "Sıvılaşma Nedeni", "desc": "Düşük protein, yüksek lipit ve zengin hidrolitik enzim içeriğidir.", "isKey": True},
                    {"title": "Kistik Boşluk", "desc": "Sıvılaşan alan temizlendikten sonra yerinde sıvı dolu kistik kavite kalmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "İskemik Nekroz Kalıbı: Kalp/Böbrek vs Beyin",
                    "headers": ["Özellik", "Kalp / Böbrek Enfarktüsü", "Beyin (Serebral) İnfarktüsü"],
                    "rows": [
                        ["Nekroz Tipi", "Koagülatif Nekroz", "Sıvılaşma (Likefaksiyon) Nekrozu"],
                        ["Doku Kıvamı", "Sert, kuru, katı", "Yumuşak, çamursu, viskoz sıvı"],
                        ["Doku Mimarisi", "Birkaç gün korunur (hayalet hücreler)", "Hemen erir, mimari hızla kaybolur"],
                        ["İyileşme Sonucu", "Kollajenöz skar dokusu", "Sıvı dolu kistik boşluk (Kavite) ve gliozis"]
                    ]
                }
            },
            "spotPearls": [
                "🚨 [KRİTİK UYARI] İskemik enfarktlar kural olarak koagülatif nekrozla seyreder; tek istisnası SIVILAŞMA (likefaksiyon) nekrozu görülen BEYİN infarktlarıdır.",
                "📌 [SINAV SPOTU] Beyin dokusunun iskemide sıvılaşmasının nedeni yüksek miyelin lipid içeriği ve zengin litik enzimleridir."
            ],
            "medicalTerms": [
                {"term": "Ensefalomalazi", "explanation": "İskemi veya enfeksiyon sonucu beyin dokusunun yumuşayıp sıvılaşması tablosudur."},
                {"term": "Gliozis", "explanation": "Beyin hasarı sonrası astrositlerin çoğalarak oluşturduğu nöral nedbe dokusudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "İskemik Nekrozun Büyük İstisnası",
                    "Katı Organlar (Böbrek / Kalp)",
                    "Santral Sinir Sistemi (Beyin)",
                    [
                        "İskemide koagülatif nekroz gelişir",
                        "Doku mimarisi günlerce korunur",
                        "Protein denatürasyonu baskındır",
                        "İyileşme fibröz skar ile sonuçlanır"
                    ],
                    [
                        "İskemide SIVILAŞMA nekrozu gelişir",
                        "Doku mimarisi anında erir ve kaybolur",
                        "Enzimatik litik sindirim baskındır",
                        "İyileşme kistik kavite ve gliozis ile biter"
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdaki organların hangisinde arteriyel tıkanmaya bağlı gelişen iskemik enfarktüs koagülatif nekroz YERİNE sıvılaşma (likefaksiyon) nekrozu ile seyreder?",
                    {
                        "A": "Böbrek",
                        "B": "Kalp kası (Miyokard)",
                        "C": "Dalak",
                        "D": "Beyin (Serebrum)",
                        "E": "Karaciğer"
                    },
                    "D",
                    {
                        "A": "Böbrek iskemisinde koagülatif nekroz gelişir.",
                        "B": "Kalp kasında koagülatif nekroz gelişir.",
                        "C": "Dalakta kama şeklinde koagülatif nekroz gelişir.",
                        "D": "Doğru cevap D'dir: Beyin iskemik enfarktüsleri koagülatif nekrozun tek istisnasıdır; zengin litik enzim ve lipit nedeniyle sıvılaşma nekrozu gelişir!",
                        "E": "Karaciğer iskemisinde koagülatif nekroz gelişir."
                    }
                )
            ]
        },
        {
            "slideNumber": 48,
            "title": "Koagülatif Nekrotik Dokunun Akıbeti",
            "subtitle": "Lökosit infiltrasyonu, fagositoz ve fibröz skar oluşumu",
            "badge": "Onarım",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Koagülatif nekroz sonsuza dek donmuş ve sert bir şekilde kalamaz. Ölü hücrelerin çevreye "
                "saldığı kimyasal mediyatörler (sitokinler, lökotrienler, DAMP'lar) çevre canlı damarlardan "
                "masif bir nötrofil akını başlatır. İlk 24-72 saatte alana dolan nötrofiller kendi lizozomal "
                "enzimlerini salarak (heteroliz) denatüre hücreleri sindirmeye başlar.\n\n"
                "> [TEMEL İLKE] 3. günden itibaren nötrofillerin yerini doku makrofajları alır; makrofajlar "
                "tüm nekrotik hücresel artıkları, parçalanmış membranları ve lipidleri fagosite ederek temizler.\n\n"
                "Temizlenen alana endotel hücreleri ve fibroblastlar girerek 'granülasyon dokusu' kurar. "
                "Haftalar içinde kollajen sentezlenir ve nekroz alanı büzüşerek sert bir fibröz skar oluşturur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Heterolitik Çözünme", "desc": "Nötrofillerin litik enzimleri sayesinde sert dokunun yumuşatılmasıdır.", "isKey": True},
                    {"title": "Makrofaj Temizliği", "desc": "Enkazın tamamen yutularak dokunun onarıma hazırlanmasıdır.", "isKey": True},
                    {"title": "Fibröz Skar", "desc": "Bölünemeyen kalıcı dokularda nekrotik alanın kalıcı kollajenle doldurulmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Nekroz Alanının İyileşme Kronolojisi",
                    "headers": ["Günler / Haftalar", "Baskın Hücre Tipi", "Doku Görünümü ve Olay"],
                    "rows": [
                        ["1 - 3. Gün", "Nötrofiller", "Heteroliz başlangıcı, nekrotik sınırda hiperemi"],
                        ["3 - 7. Gün", "Makrofajlar", "Aktif fagositoz, doku enkazının temizlenmesi, sarı yumuşama"],
                        ["1 - 2. Hafta", "Endotel ve Fibroblastlar", "Granülasyon dokusu, yeni kapiller damarlar"],
                        ["2 - 8. Hafta", "Kollajen lifleri (Skar)", "Damarsız, beyaz, büzüşmüş fibröz skar dokusu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Koagülatif nekroz alanı lökositlerin heterolitik enzimleri tarafından eritilir ve makrofajlarca temizlenir.",
                "📌 [YÜKSEK VERİM] Kalıcı dokulardaki (miyokard) geniş nekroz alanları parankimal rejenerasyonla değil fibröz skar ile iyileşir."
            ],
            "medicalTerms": [
                {"term": "Granülasyon Dokusu", "explanation": "Yara ve nekroz iyileşmesinde yeni oluşan kılcal damarlar ve genç fibroblastlardan zengin pembe dokudur."},
                {"term": "Skarizasyon", "explanation": "Hasarlı dokunun fonksiyonel parankim yerine fibröz kollajen bağ dokusuyla tamir edilmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Koagülatif Nekrozun İyileşme Zinciri",
                    [
                        "1. Nekroz Oluşumu: İskemiyle hücreler ölür, proteinler koagüle olur ve mimari donar.",
                        "2. Nötrofil Hücumu: DAMP sinyalleriyle nötrofiller alana dolar ve heteroliz başlatır.",
                        "3. Makrofaj Temizliği: 3. günden itibaren makrofajlar nekrotik enkazı fagosite eder.",
                        "4. Granülasyon Dokusu: Yeni kılcal damarlar ve fibroblastlar bölgeye göç eder.",
                        "5. Fibröz Skar: Tip I kollajen birikerek sert, fonksiyon görmeyen nedbe dokusu oluşturur."
                    ]
                ),
                make_cloze(
                    "Nekroz alanındaki hücresel enkazın tamamen fagosite edilerek temizlenmesinde görev alan temel hücre makrofajdır.",
                    "makrofajdır",
                    "Fagositik Hücre"
                )
            ]
        },
        {
            "slideNumber": 49,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Nekroz vs Apoptoz ve Koagülatif Nekroz",
            "subtitle": "Nekrozun temel nitelikleri, hayalet hücreler, kama şekli ve beyin istisnası",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 5,
            "synthesisNarrative": (
                "Beşinci kontrol noktasında, hücre ölümünün iki ana tipi olan nekroz ile apoptoz arasındaki "
                "farkları ve en sık görülen nekroz formu olan koagülatif nekrozu özetliyoruz. Nekroz daima "
                "patolojiktir, membran yırtılır ve yoğun inflamasyon başlar.\n\n"
                "> [ÖZET VURGU] Koagülatif nekrozda asidoz enzimleri de denatüre ettiği için doku mimarisi "
                "birkaç gün korunur (hayalet hücreler); en büyük istisna ise iskemide sıvılaşan BEYİNDİR!\n\n"
                "Aşağıdaki 3 akıl kartını dikkatle inceleyerek bu kritik sınav bilgilerini hafızanıza sabitleyin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Nekroz vs Apoptoz", "desc": "Nekroz = patolojik + şişme + inflamasyon; Apoptoz = programlı + büzülme + sessiz.", "isKey": True},
                    {"title": "Hayalet Hücreler", "desc": "Koagülatif nekrozda konturları sağlam fakat çekirdeksiz hücrelerdir.", "isKey": True},
                    {"title": "Beyin İstisnası", "desc": "Beyin iskemik enfarktüsü koagülatif DEĞİL, sıvılaşma nekrozudur.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 5 Sentez Tablosu",
                    "headers": ["Kavram", "Temel Özellik", "Klinik / Sınav Değeri"],
                    "rows": [
                        ["Koagülatif Nekroz", "En sık nekroz, protein denatürasyonu", "Kalp, böbrek, dalak iskemik enfarktları"],
                        ["Hayalet Hücre", "Çekirdeksiz korunmuş hücre konturu", "Koagülatif nekrozun mikroskobik damgası"],
                        ["Kama Şekilli Enfarkt", "Uç arter dallanma geometrisi", "Böbrek ve dalak soluk enfarktları"],
                        ["Beyin İnfarktı", "Sıvılaşma (likefaksiyon) nekrozu", "Koagülatif kuralının en meşhur istisnası"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekroz daima patolojiktir ve daima inflamasyon oluşturur; apoptoz inflamasyon oluşturmaz.",
                "🚨 [KRİTİK UYARI] İskemik enfarktlar kural olarak koagülatif nekrozdur; beyin iskemisi ise SIVILAŞMA nekrozudur."
            ],
            "medicalTerms": [
                {"term": "Doku İskeleti", "explanation": "Ekstraselüler matriks ve hücre konturlarının oluşturduğu mimari çatıdır."},
                {"term": "İnflamatuar Eksuda", "explanation": "Damar geçirgenliği artışıyla nekroz alanına sızan protein ve lökosit zengini sıvıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-013",
                    "Koagülatif nekrozda mikroskop altında doku mimarisinin ve hücre hatlarının birkaç gün boyunca korunmasının nedeni nedir?",
                    "İskemik dokuda gelişen ağır asidozun, yalnızca yapısal proteinleri değil ölü hücreyi eritecek olan lizozomal litik enzimleri de denatüre ederek proteolizi geciktirmesidir."
                ),
                make_flashcard(
                    "fc-k1-04-014",
                    "İskemik doku enfarktlarında koagülatif nekroz kuralının en meşhur istisnası hangi organdır ve neden?",
                    "Santral sinir sistemidir (BEYİN); beyin dokusunda protein az, miyelin lipiti ve litik enzimler çok yüksek olduğu için iskemik infarktta koagülatif değil SIVILAŞMA (likefaksiyon) nekrozu gelişir."
                ),
                make_flashcard(
                    "fc-k1-04-015",
                    "Nekroz ile apoptoz arasındaki inflamatuar yanıt farkının hücresel nedeni nedir?",
                    "Nekrozda hücre zarı parçalanır ve sitoplazmik içerik (DAMP'lar) dışarı dökülerek lökositleri uyarır; apoptozda ise hücre zarı sağlam kalır ve içerik apoptotik cisimcikler halinde sessizce fagosite edilir."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 5 Sentezi: Bir böbrek biyopsisinde 'hayalet hücreler' (ghost cells) izlenmesi ne anlama gelir?",
                    "Böbrek parankiminde arteriyel tıkanmaya bağlı koagülatif nekroz geliştiğini; hücrelerin çekirdeklerini kaybettiğini ancak protein denatürasyonu sayesinde dış sınırlarının henüz ayakta durduğunu gösterir."
                ),
                make_cloze(
                    "İskemik enfarktlar kural olarak koagülatif nekrozla seyrederken beyin infarktlarında sıvılaşma nekrozu görülür.",
                    "sıvılaşma nekrozu",
                    "İstisnai Nekroz"
                )
            ]
        }
    ]
