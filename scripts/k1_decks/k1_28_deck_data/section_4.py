# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 4: Malign Terminoloji ve Yanıltıcı İstisnalar (Slayt 31 - 40)
Checkpoint: Slayt 39
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_4_slides():
    return [
        # Slayt 31
        {
            "slideNumber": 31,
            "title": "Malign Terminolojinin Temel Ayrımı: Karsinom vs Sarkom",
            "content": (
                "Malign neoplazmların isimlendirilmesinde en temel ayrım dokunun embriyolojik ve histogenetik kökenine dayanır. "
                "Epitelyal dokulardan (ektoderm, mezoderm veya endoderm kaynaklı tüm epitel tabakalarından) türeyen malign "
                "tümörlere 'karsinom' (carcinoma) adı verilir. Buna karşılık mezoderm kökenli embriyonik bağ dokusundan "
                "(mezenkimden) türeyen kemik, kıkırdak, yağ, kas ve fibröz doku malignitelerine 'sarkom' (sarcoma) adı verilir. "
                "Karsinomlar insan kanserlerinin %85'ten fazlasını oluşturarak çok daha sık görülürken, sarkomlar tüm kanserlerin "
                "yaklaşık %1'ini oluşturan nadir kitlelerdir. Bu iki grup yayılım yolları (lenfatik vs hematojen) açısından da zıttır."
            ),
            "elements": [
                make_table(
                    "Karsinom ve Sarkom Temel Karşılaştırması",
                    ["Parametre", "Karsinom", "Sarkom"],
                    [
                        {
                            "cells": ["Histogenetik Köken", "Epitelyal dokular (tüm germ tabakaları)", "Mezenkimal bağ dokuları (kemik, kas, yağ)"],
                            "hiddenIndex": 0,
                            "hint": "Embriyolojik doku kökeni"
                        },
                        {
                            "cells": ["Görülme Sıklığı", "Çok sık (>%85)", "Nadir (~%1)"],
                            "hiddenIndex": 1,
                            "hint": "Toplumda insidans oranı"
                        },
                        {
                            "cells": ["Primer Yayılım Yolu", "Lenfatik damarlar (Lenf nodları)", "Hematojen (Özellikle venler)"],
                            "hiddenIndex": 2,
                            "hint": "Sarkomların ana metastaz yolu"
                        }
                    ]
                ),
                make_cloze(
                    "Epitel dokusundan köken alan tüm kötü huylu malign neoplazmlar genel olarak karsinom adıyla anılır.",
                    "karsinom",
                    "Epitelyal malignite terimi"
                )
            ]
        },
        # Slayt 32
        {
            "slideNumber": 32,
            "title": "Karsinomlar: Adenokarsinom ve Skuamöz Karsinom",
            "content": (
                "Karsinomlar kendi içlerinde sergiledikleri mikroskobik diferansiyasyon çizgisine göre iki dev ana gruba "
                "ayrılır: 'Adenokarsinom' ve 'Skuamöz hücreli karsinom'. Adenokarsinom, glandüler (bez) yapısı oluşturan "
                "veya müsin salgılayan epitel hücrelerinden köken alan malign tümördür; meme, kolon, prostat, mide ve akciğerin "
                "en sık kanser tipidir. Skuamöz hücreli karsinom (yassı hücreli karsinom) ise çok katlı yassı epitel "
                "diferansiyasyonu gösteren malign neoplazmdır. Deri, dudak, özofagus, larenks, serviks ve sigara içenlerin "
                "bronş mukozasında gelişir. İyi diferansiye skuamöz hücreli karsinomların mikroskopik patognomonik bulgusu "
                "hücreler arası köprüler (dezmozomlar) ve konsantrik laminer 'keratin incileri'dir (boynuzsu inciler)."
            ),
            "elements": [
                make_before_after(
                    "Adenokarsinom vs Skuamöz Hücreli Karsinom",
                    "Adenokarsinom",
                    "Lümenli bez yapıları, hücre içi/dışı müsin üretimi, PAS pozitifliği, kolon ve memede klasik.",
                    "Skuamöz Hücreli Karsinom",
                    "Konsantrik keratin incileri, hücreler arası dezmozomal köprüler, eozinofilik sitoplazma, deride ve bronşta klasik.",
                    "Histopatolojik tip organa göre kemoterapi ve hedefe yönelik ajan seçimini doğrudan belirler."
                ),
                make_active_recall(
                    "İyi diferansiye skuamöz hücreli karsinomun mikroskobik incelemesinde saptanan klasik patognomonik oluşum nedir?",
                    "Keratin incileridir (veya boynuzsu inciler).",
                    "Konsantrik keratinize hücresel küreler"
                )
            ]
        },
        # Slayt 33
        {
            "slideNumber": 33,
            "title": "Sarkomlar: Mezenkimal Malignitelerin Nomenklatürü",
            "content": (
                "Sarkomlar (Grekçe 'sarx' yani et kelimesinden türetilmiştir), etsi, balık eti kıvamında kesit yüzeyine "
                "sahip, genellikle derin fasyalarda veya retroperitonda sinsi büyüyen mezenkimal kanserlerdir. Adlandırmaları "
                "köken hücre tipinin sonuna '-sarkom' eklenerek yapılır: Yağ dokusunun malign tümörüne 'liposarkom', kıkırdak "
                "dokusunun malign tümörüne 'kondrosarkom', kemik dokusunun malign tümörüne 'osteosarkom', düz kasın malign "
                "tümörüne 'leiomyosarkom', çizgili kasın malign tümörüne ise 'rabdomyosarkom' denir. Rabdomyosarkom çocukluk "
                "ve adolesan çağının en sık yumuşak doku sarkomudur; osteosarkom ise gençlerde metafiz yerleşimli agresif kemik kanseridir."
            ),
            "elements": [
                make_table(
                    "Mezenkimal Dokuların Malign Karşılıkları",
                    ["Doku Türü", "Benign Neoplazm", "Malign Neoplazm (Sarkom)"],
                    [
                        {
                            "cells": ["Kemik Dokusu", "Osteom", "Osteosarkom"],
                            "hiddenIndex": 2,
                            "hint": "Malign kemik kanseri"
                        },
                        {
                            "cells": ["Kıkırdak Dokusu", "Kondrom", "Kondrosarkom"],
                            "hiddenIndex": 2,
                            "hint": "Malign kıkırdak kanseri"
                        },
                        {
                            "cells": ["Yağ Dokusu", "Lipom", "Liposarkom"],
                            "hiddenIndex": 2,
                            "hint": "Malign lipositer tümör"
                        },
                        {
                            "cells": ["Çizgili Kas Dokusu", "Rabdomyom", "Rabdomyosarkom"],
                            "hiddenIndex": 2,
                            "hint": "Pediatrik malign kas kanseri"
                        }
                    ]
                ),
                make_cloze(
                    "Çocukluk ve gençlik çağında en sık görülen malign çizgili kas kaynaklı mezenkimal kanser rabdomyosarkom olarak adlandırılır.",
                    "rabdomyosarkom",
                    "İskelet kası malignitesi"
                )
            ]
        },
        # Slayt 34
        {
            "slideNumber": 34,
            "title": "Hematopoetik ve Lenfoid Maligniteler",
            "content": (
                "Kemik iliği hematopoetik kök hücrelerinden ve lenfoid organlardan köken alan neoplazmlar klasik karsinom/sarkom "
                "ikilisinin dışındaki özel bir terminolojiye tabidir. Kemik iliğinde başlayıp kana ve dalak gibi organlara "
                "yayılan hematopoetik malignitelere 'lösemi' (lökosit kanseri) adı verilir. Lenf nodlarında veya ekstranodal "
                "lenfoid dokularda solid kitleler oluşturan malign lenfosit proliferasyonlarına ise 'lenfoma' (Hodgkin ve "
                "Non-Hodgkin lenfomalar) denir. Burada en hayati kural şudur: 'Benign lösemi' veya 'benign lenfoma' diye bir "
                "kavram tıpta kesinlikle yoktur; lenfoma veya lösemi tanısı alan her hasta tanım gereği doğrudan ve daima maligndir."
            ),
            "elements": [
                make_active_recall(
                    "Tıbbi terminolojide '-oma' eki taşımasına rağmen kesinlikle iyi huylu formu bulunmayan lenfoid malignite nedir?",
                    "Lenfomadır (tüm lenfomalar daima maligndir).",
                    "Malign lenfosit kitlesi"
                ),
                make_micro_quiz(
                    "Hematopoetik ve lenfoid neoplazmlarla ilgili aşağıdaki ifadelerden hangisi biyolojik olarak doğrudur?",
                    [
                        {
                            "text": "Tüm lenfomalar ve lösemiler tanım gereği istisnasız olarak malign neoplazmlardır",
                            "isCorrect": True,
                            "explanation": "Doğrudur; hematopoetik neoplazmların benign formu yoktur, hepsi maligndir."
                        },
                        {
                            "text": "Lenfomalar daima fibröz kapsülle çevrili benign kitlelerdir",
                            "isCorrect": False,
                            "explanation": "Lenfomalar kapsülsüz malign klonal proliferasyonlardır."
                        },
                        {
                            "text": "Lösemi yalnızca yaşlı bireylerde görülen benign bir lökosit artışıdır",
                            "isCorrect": False,
                            "explanation": "Lösemi malign kemik iliği kanseridir, çocuklarda da çok sıktır."
                        },
                        {
                            "text": "Lenfomalar cerrahiyle tek parça halinde soyularak tamamen biter",
                            "isCorrect": False,
                            "explanation": "Lenfomalar sistemik lenfoid hastalıklardır, sistemik kemoterapi gerektirirler."
                        }
                    ],
                    "Lenfoma ve lösemi terimleri doğrudan maligniteyi ifade eder."
                )
            ]
        },
        # Slayt 35
        {
            "slideNumber": 35,
            "title": "Yanıltıcı '-oma' İstisnası: Malign Melanom",
            "content": (
                "Tıbbi terminolojide '-oma' eki kural olarak benign neoplazmları simgeler; ancak tıp tarihinde yerleşmiş "
                "dört adet ölümcül malign istisna bulunmaktadır. Bu yanıltıcı dörtlünün ilki 'melanom'dur (malign melanom). "
                "Melanositlerin (deri, göz üveası, meningler vb.) benign neoplazmına 'nevüs' (halk arasında ben) adı verilir. "
                "Melanositlerin malign neoplazmı ise '-karsinom' eki almaz, doğrudan 'melanom' veya 'malign melanom' olarak "
                "adlandırılır. Melanom, derinin en ölümcül kanseri olup son derece erken evrede dahi lenfatik ve hematojen "
                "metastaz yapma kabiliyetine sahiptir. Günlük patoloji pratiğinde hiçbir 'benign melanom' tanımı bulunmaz."
            ),
            "elements": [
                make_before_after(
                    "Melanositik Neoplazmların Terminolojisi",
                    "Benign Melanositik Lezyon",
                    "Nevüs (melanositik nevüs, ben); iyi huylu, simetrik, düzgün sınırlı, metastaz riski sıfır.",
                    "Malign Melanositik Kanser",
                    "Melanom (Malign Melanom); asimetrik, alacalı renkli, derin invazyonlu, son derece ölümcül malignite.",
                    "Melanom '-oma' ile bitmesine rağmen en agresif insan kanserlerinden biridir."
                ),
                make_cloze(
                    "Melanositlerden köken alan ve '-oma' eki taşımasına rağmen daima ölümcül malignite gösteren kanser melanom olarak adlandırılır.",
                    "melanom",
                    "En tehlikeli melanositik deri kanseri"
                )
            ]
        },
        # Slayt 36
        {
            "slideNumber": 36,
            "title": "Yanıltıcı '-oma' İstisnası: Mezotelyoma",
            "content": (
                "Yanıltıcı '-oma' istisnalarının ikincisi 'mezotelyoma'dır (malign mezotelyoma). Plevra, periton, perikard "
                "ve tunika vajinalis gibi vücut seröz boşluklarını döşeyen mezotel hücrelerinden köken alır. Özellikle "
                "çevresel veya mesleki 'asbest' (amianto) liflerine maruziyetten 25-40 yıl sonra gelişen, akciğeri zırh gibi "
                "kalınlaştırarak saran ve toraks duvarını istila eden son derece agresif bir malignitedir. Tıpkı melanomda "
                "olduğu gibi, 'mezotelyoma' terimi tek başına kullanıldığında daima malign mezotelyomayı kasteder; benign bir "
                "lezyon olan adenomatoid tümör veya soliter fibröz tümör ile terminolojik olarak kesinlikle karıştırılmamalıdır."
            ),
            "elements": [
                make_active_recall(
                    "Asbest maruziyeti ile doğrudan ilişkili olan ve plevrayı zırh gibi saran ölümcül malign seröz zar kanseri nedir?",
                    "Malign mezotelyomadır.",
                    "Plevral mezotel kaynaklı kanser"
                ),
                make_micro_quiz(
                    "Mezotelyoma tanısı alan bir hastanın patolojik ve klinik durumu hakkında hangisi kesinlikle doğrudur?",
                    [
                        {
                            "text": "İsminde '-oma' eki bulunmasına rağmen daima kötü huylu (malign) bir kanserdir",
                            "isCorrect": True,
                            "explanation": "Doğrudur; mezotelyoma literatürdeki 4 temel malign '-oma' istisnasından biridir."
                        },
                        {
                            "text": "Basit bir antibiyotik tedavisiyle 3 günde tamamen iyileşir",
                            "isCorrect": False,
                            "explanation": "Mezotelyoma agresif bir kanserdir, antibiyotikle düzelmez."
                        },
                        {
                            "text": "Kesinlikle benign bir yağ bezi kistidir",
                            "isCorrect": False,
                            "explanation": "Seröz zarların malign tümörüdür, yağ kisti değildir."
                        },
                        {
                            "text": "Hastanın hiçbir zaman asbeste maruz kalmadığının kanıtıdır",
                            "isCorrect": False,
                            "explanation": "Olguların %80-90'ında asbest maruziyeti kanıtlanmıştır."
                        }
                    ],
                    "Mezotelyoma kötü huylu bir seröz zar kanseridir."
                )
            ]
        },
        # Slayt 37
        {
            "slideNumber": 37,
            "title": "Yanıltıcı '-oma' İstisnası: Seminom",
            "content": (
                "Yanıltıcı '-oma' grubunun üçüncü klasik örneği 'seminom'dur. Seminom, genç erişkin erkeklerde (15-35 yaş) "
                "testisin seminifer tübül germ hücrelerinden köken alan malign bir germ hücreli tümördür (overdeki karşılığı "
                "'disgerminom'dur). Seminomlar belirgin nükleollü, glikojenden zengin berrak sitoplazmalı uniform büyük hücrelerden "
                "ve aralarında lenfosit infiltrasyonu içeren fibröz septalardan meydana gelir. Adındaki '-oma' ekine aldanılmamalıdır; "
                "seminom tedavi edilmediğinde retroperitoneal lenf nodlarına ve akciğere hızla metastaz yapan malign bir kanserdir. "
                "Ancak radyoterapiye ve platin bazlı kemoterapiye son derece duyarlı olup kür şansı en yüksek kanserlerdendir."
            ),
            "elements": [
                make_table(
                    "Malign '-oma' İstisnaları Özet Tablosu",
                    ["Tümör Adı", "Köken Hücre / Doku", "Klinik Özellik / Malignite Niteliği"],
                    [
                        {
                            "cells": ["Lenfoma", "Lenfositler (Lenfoid doku)", "Daima maligndir; benign lenfoma yoktur"],
                            "hiddenIndex": 0,
                            "hint": "Lenfoid malignite adı"
                        },
                        {
                            "cells": ["Melanom", "Melanositler (Deri/Göz)", "Son derece agresif melanositik kanser"],
                            "hiddenIndex": 0,
                            "hint": "Koyu pigmentli deri kanseri"
                        },
                        {
                            "cells": ["Mezotelyoma", "Seröz zar mezoteli", "Asbest ilişkili ölümcül plevra kanseri"],
                            "hiddenIndex": 0,
                            "hint": "Plevral mezotel kanseri"
                        },
                        {
                            "cells": ["Seminom", "Testis germ hücreleri", "Genç erkekte metastatik germ hücreli kanser"],
                            "hiddenIndex": 0,
                            "hint": "Testis kaynaklı germ kanseri"
                        }
                    ]
                ),
                make_cloze(
                    "Testis germ hücrelerinden köken alan ve adındaki '-oma' ekine rağmen malign olan tümör seminom olarak bilinir.",
                    "seminom",
                    "Testisin malign germ hücreli neoplazmı"
                )
            ]
        },
        # Slayt 38
        {
            "slideNumber": 38,
            "title": "Diğer Malign İstisnalar: Hepatoma, Glioblastom ve Koriokarsinom",
            "content": (
                "Patoloji terminolojisinde kural dışı adlandırmaya sahip diğer önemli maligniteler mevcuttur. "
                "Karaciğerin primer malign kanseri olan 'hepatoselüler karsinom', klinik dilde sıkça kısaca 'hepatoma' "
                "olarak anılır; ancak kesinlikle benign bir adenom değil agresif bir karsinomdur. Beynin en sık ve en ölümcül "
                "primer astrositer tümörü olan 'glioblastoma multiforme' (GBM), adında '-karsinom' veya '-sarkom' geçmemesine "
                "rağmen Dünya Sağlık Örgütü Grade IV en yüksek dereceli malign neoplazmdır. Plasental trofoblastların benign "
                "kistik lezyonuna 'hidatidiform mol' denirken, bunun agresif hematojen metastaz yapan malign kanserine "
                "'koriokarsinom' adı verilir."
            ),
            "elements": [
                make_before_after(
                    "Plasental ve Hepatik Neoplazmların Benign-Malign İsimleri",
                    "Benign Karşılık",
                    "Plasentada hidatidiform mol (üzüm gebeliği); karaciğerde hepatoselüler adenom (OKS ilişkili).",
                    "Malign Karşılık",
                    "Plasentada koriokarsinom (akciğere erken kanla yayılan); karaciğerde hepatoselüler karsinom (hepatoma).",
                    "Terminolojik adlandırmalardaki tuzakları bilmek doğru evreleme ve tedavi için şarttır."
                ),
                make_active_recall(
                    "Plasental trofoblastlardan köken alan ve erken dönemde akciğere masif hematojen metastaz yapan malign karsinom nedir?",
                    "Koriokarsinomdur.",
                    "Malign trofoblastik kanser"
                )
            ]
        },
        # Slayt 39 [CHECKPOINT 4]
        {
            "slideNumber": 39,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Malign Terminoloji ve Yanıltıcı İstisnalar",
            "content": (
                "Bu bölümde malign neoplazmların adlandırılmasını, karsinom-sarkom ayrımını ve yanıltıcı istisnaları özetledik. "
                "Epitel dokudan köken alan maligniteler 'karsinom' (adenokarsinom ve skuamöz karsinom) adını alır ve lenfatik yayılır. "
                "Mezenkimal bağ dokudan türeyen kanserler 'sarkom' (osteosarkom, liposarkom vb.) adını alır ve hematojen yayılır. "
                "Hematopoetik neoplazmlar lösemi ve lenfoma olup iyi huylu formları kesinlikle yoktur. "
                "Dört klasik yanıltıcı '-oma' istisnası daima maligndir: Lenfoma, Melanom, Mezotelyoma ve Seminom. "
                "Klinik dilde 'hepatoma' denilen tümör hepatoselüler karsinomdur. "
                "Plasentada hidatidiform mol benign iken, koriokarsinom erken metastaz yapan son derece malign bir tümördür."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp04-fc01",
                    "front": "Tıbbi terminolojide '-oma' ekiyle bitmesine rağmen istisnasız daima malign kabul edilen dörtlü grup hangileridir?",
                    "back": "Lenfoma, melanom, mezotelyoma ve seminom grubudur.",
                    "hint": "Dört klasik kötü huylu istisna"
                },
                {
                    "id": "k1-28-cp04-fc02",
                    "front": "Glandüler bez yapısı oluşturan veya müsin salgılayan epitel kaynaklı malign neoplazmlara genel olarak ne ad verilir?",
                    "back": "Adenokarsinom adı verilir.",
                    "hint": "Meme ve kolonda sık görülen salgı bezi kanseri"
                },
                {
                    "id": "k1-28-cp04-fc03",
                    "front": "Genç erkeklerde testisin seminifer germ hücrelerinden köken alan ve radyosensitif olan malign kanser türü nedir?",
                    "back": "Seminom tümörüdür.",
                    "hint": "Testis kaynaklı malign istisna"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 4 Özet Tablosu: Malign Terminoloji ve İstisnalar",
                    ["Tümör Adı", "Kullanılan Ek", "Gerçek Biyolojik Davranışı", "Köken Hücresi"],
                    [
                        {
                            "cells": ["Melanom", "-oma", "Malign (Ölümcül deri kanseri)", "Melanositler"],
                            "hiddenIndex": 2,
                            "hint": "Kötü huylu melanotik lezyon"
                        },
                        {
                            "cells": ["Seminom", "-oma", "Malign (Germ hücreli kanser)", "Testis germ hücreleri"],
                            "hiddenIndex": 2,
                            "hint": "Testis kökenli kötü huylu neoplazm"
                        },
                        {
                            "cells": ["Osteosarkom", "-sarkom", "Malign (Kemik kanseri)", "Osteoblastlar"],
                            "hiddenIndex": 1,
                            "hint": "Mezenkimal malignite takısı"
                        }
                    ]
                )
            ]
        },
        # Slayt 40
        {
            "slideNumber": 40,
            "title": "Klinik Karar: Yanıltıcı İsimli Biyopsi Raporu Yönetimi",
            "content": (
                "Bir genel cerrahi polikliniğinde cildinde hızla büyüyen pigmente lezyon eksize edilen hastanın patoloji "
                "raporu 'Nodüler Melanom, Breslow kalınlığı 2.4 mm' olarak sonuçlanıyor. Hastanın yakını, raporda '-karsinom' "
                "yazmadığı ve isminin '-oma' ile bittiği için kitlenin iyi huylu olduğunu düşünerek seviniyor. "
                "Hekim bu aşamada melanomun derinin en tehlikeli ve en ölümcül kanseri olduğunu, '-oma' ekinin tarihsel "
                "bir yanıltıcı istisna olduğunu aileye şeffaflıkla açıklamalıdır. Hastaya derhal primer lezyon yatağına "
                "2 cm genişletilmiş cerrahi eksizyon ve bölgesel lenf nodu metastazını ekarte etmek için 'sentinel lenf "
                "nodu biyopsisi' (SLNB) planlanmalıdır."
            ),
            "elements": [
                make_branching_logic(
                    "Patoloji raporunda 'Malign Melanom' bildirilen bir hastanın yakınları ismindeki ek nedeniyle bunun iyi huylu bir et beni olduğunu iddia ederek ek cerrahiyi reddetmek istiyor.",
                    "Bu klinik durumda hekimin alması gereken en doğru tıbbi ve etik tutum ne olmalıdır?",
                    [
                        {
                            "text": "Melanomun '-oma' ile bitmesine rağmen son derece ölümcül bir kanser olduğu anlatılmalı, geniş güvenlik marjinli re-eksizyon ve sentinel lenf nodu biyopsisi planlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; melanom en agresif deri kanseridir, cerrahi marjin ve lenf nodu evrelemesi hayati önemdedir."
                        },
                        {
                            "text": "Hasta yakınlarının haklı olduğu kabul edilip kitleye hiçbir tedavi yapılmadan dosya kapatılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Melanom tedavi edilmezse hızla metastaz yapar ve ölümcüldür."
                        },
                        {
                            "text": "Hastaya sadece nemlendirici krem reçete edilmelidir.",
                            "isCorrect": False,
                            "explanation": "Krem kanser tedavisinde etkisizdir."
                        }
                    ]
                )
            ]
        }
    ]
