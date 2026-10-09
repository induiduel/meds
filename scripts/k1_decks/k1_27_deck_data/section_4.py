# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 4: Fizikokimya, Süpersatürasyon ve Çekirdeklenme (Slayt 31 - 40)
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
            "title": "Litogenezin Fizikokimyasal Evreleri: Termodinamik Temeller",
            "content": (
                "Üriner taş oluşumu rastgele bir çökelme süreci olmayıp, kesin fizikokimyasal ve termodinamik yasalara tabi "
                "olan çok basamaklı bir faz değişimidir. Bir çözeltide serbest iyon halinde bulunan moleküllerin katı bir "
                "kristal kafesine dönüşmesi belirli enerji basamaklarını gerektirir. Bu süreç sırasıyla; aşırı doygunluğun "
                "(süpersatürasyon) gelişmesi, kristal çekirdeklenmesi (nükleasyon), kristal büyümesi, kristallerin birbirine "
                "kenetlenerek kümelenmesi (agregasyon) ve nihayetinde bu kitlenin böbrek tübüler sisteminde tutunması (retansiyon) "
                "evrelerinden oluşur. Her evre, ortamdaki çözünmüş iyonların konsantrasyonu, iyonik güç, pH ve inhibitör-promotör dengesiyle belirlenir."
            ),
            "elements": [
                make_causal_chain(
                    "İdrardaki Çözünmüş İyonlardan Katı Taşa Uzanan Fizikokimyasal Evreler",
                    [
                        "1. Süpersatürasyon: Çözünen tuzların konsantrasyonunun termodinamik çözünürlük sınırını aşması",
                        "2. Çekirdeklenme (Nükleasyon): İyonların bir araya gelerek ilk kararlı katı faz kümelerini oluşturması",
                        "3. Kristal Büyümesi: Çözeltideki yeni iyonların mevcut nükleus yüzeyine katılarak kafesi büyütmesi",
                        "4. Agregasyon: Ayrı kristal partiküllerinin kimyasal veya elektriksel kuvvetlerle tek kitlede birleşmesi",
                        "5. Epitelyal Retansiyon: Büyüyen konglomeratın tübül duvarına yapışması ve kalıcı kalkül haline gelmesi"
                    ]
                ),
                make_cloze(
                    "Çözünmüş iyonların katı kristal fazına geçişinde itici termodinamik güç süpersatürasyon olarak adlandırılır.",
                    "süpersatürasyon",
                    "Aşırı doygunluk durumu"
                )
            ]
        },
        # Slayt 32
        {
            "slideNumber": 32,
            "title": "Aşırı Doygunluk (Süpersatürasyon - SS) Kavramı",
            "content": (
                "Aşırı doygunluk (Relative Supersaturation - SS), çözeltideki iyonların aktivite çarpımının (AP), o tuzun "
                "belirli bir sıcaklık ve pH'taki termodinamik çözünürlük çarpımına (Ksp) oranıdır. Eğer SS değeri 1'den küçükse "
                "(SS < 1), çözelti doymamıştır ve mevcut kristaller çözünme eğilimindedir. SS değeri 1'e eşit olduğunda çözelti "
                "tam dengededir. SS değeri 1'in üzerine çıktığında ise çözelti aşırı doygundur ve termodinamik olarak katı fazın "
                "oluşması mümkün hale gelir. Süpersatürasyon, taş hastalığının mutlak ön koşuludur; aşırı doygunluk olmaksızın "
                "hiçbir biyolojik sıvı içerisinde spontan veya uyarılmış taş oluşumu gerçekleşemez."
            ),
            "elements": [
                make_table(
                    "İdrar Doygunluk Durumları ve Termodinamik Davranış",
                    ["Doygunluk Düzeyi (SS)", "Termodinamik Faz", "Kristal Davranışı", "Taş Oluşum Riski"],
                    [
                        {
                            "cells": ["SS < 1.0", "Doymamış Bölge", "Kristaller kendiliğinden çözünür", "Sıfır risk"],
                            "hiddenIndex": 2,
                            "hint": "Mevcut tuzların erimesi"
                        },
                        {
                            "cells": ["1.0 < SS < ULM", "Metastabil Bölge", "Yalnızca önceden var olan nidus üzerinde büyüme", "Orta risk (heterojen)"],
                            "hiddenIndex": 1,
                            "hint": "Yarı dengeli aşırı doygun durum"
                        },
                        {
                            "cells": ["SS > ULM", "Kararsız (Unstabil) Bölge", "Spontan de novo nükleasyon", "Çok yüksek risk (homojen)"],
                            "hiddenIndex": 2,
                            "hint": "Kendiliğinden kristal çökmesi"
                        }
                    ]
                ),
                make_active_recall(
                    "İdrarda süpersatürasyon düzeyi birden küçük olduğunda (SS < 1.0) mevcut kristallerin akıbeti ne olur?",
                    "Çözünerek erir ve kaybolur.",
                    "Sıvı faza geri dönme"
                )
            ]
        },
        # Slayt 33
        {
            "slideNumber": 33,
            "title": "Termodinamik Çözünürlük Çarpımı ve Doymamış Alan",
            "content": (
                "Termodinamik çözünürlük çarpımı (Ksp), bir tuzun çözücüsü ile kurduğu dinamik dengede çözeltide kalabilen "
                "maksimum serbest iyon konsantrasyonunu simgeler. Doymamış alanda (SS < 1.0), iyonların serbest enerjisi "
                "kristal fazın serbest enerjisinden düşüktür; bu termodinamik fark nedeniyle kristal oluşumu imkansızdır. "
                "Bu prensip modern litotripsi sonrası ve tıbbi taş önleme tedavilerinin temel hedefini oluşturur. "
                "Bol sıvı alımıyla idrarı dilüe etmek, kalsiyum ve oksalat konsantrasyonlarını Ksp sınırının altına çekerek "
                "idrarı doymamış faza döndürür ve hem yeni taş oluşumunu engeller hem de mikrokristallerin çözünmesini sağlar."
            ),
            "elements": [
                make_before_after(
                    "İdrar Seyreltilmesinin Termodinamik Etkisi",
                    "Konsantre İdrar (SS > 1)",
                    "İyon aktivite çarpımı Ksp değerini aşmıştır; kristaller hızla büyür ve kümelenir.",
                    "Yüksek Hacimli Dilüe İdrar (SS < 1)",
                    "İyonlar doymamış bölgeye geriler; çözünme teşvik edilir, yeni kristal çekirdeklenmesi tamamen durur.",
                    "Günde 2.5-3 litre idrar çıkarmak idrarı doymamış bölgede tutmanın en fizyolojik yoludur."
                ),
                make_cloze(
                    "İdrarda çözünmüş tuzların aktivite çarpımı termodinamik çözünürlük çarpımının altında kaldığında sistem doymamış fazda yer alır.",
                    "doymamış fazda",
                    "Kristal erimesini sağlayan ortam"
                )
            ]
        },
        # Slayt 34
        {
            "slideNumber": 34,
            "title": "Metastabil Bölge ve Metastabilitenin Üst Sınırı (ULM)",
            "content": (
                "Metastabil bölge, SS değerinin 1.0 ile 'Metastabilitenin Üst Sınırı' (Upper Limit of Metastability - ULM) "
                "arasında yer aldığı aralıktır. Bu bölgede idrar çözünürlük sınırını aşmış durumdadır ancak serbest enerji "
                "bariyeri nedeniyle spontan olarak sıfırdan yeni bir kristal çekirdeği (de novo nükleus) oluşturamaz. "
                "Buna karşın, eğer ortamda önceden var olan yabancı bir yüzey, hücre döküntüsü, epitel plağı veya farklı "
                "bir kristal tohumu (nidus) bulunuyorsa, bu tohum üzerinde kristal büyümesi derhal başlar. ULM değeri sabit "
                "bir kimyasal rakam olmayıp, idrardaki kristalizasyon inhibitörlerinin (özellikle sitrat ve magnezyum) "
                "konsantrasyonuna bağlı olarak yukarı veya aşağı kayabilir."
            ),
            "elements": [
                make_micro_quiz(
                    "Metastabil bölgede (1.0 < SS < ULM) kristal oluşumunun gerçekleşebilmesi için mutlak gerekli olan koşul nedir?",
                    [
                        {
                            "text": "Ortamda önceden var olan bir çekirdek veya nidusun bulunması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; metastabil bölgede heterojen çekirdeklenme için tohum şarttır."
                        },
                        {
                            "text": "İdrarın pH değerinin mutlak olarak 8.0'in üzerine çıkması",
                            "isCorrect": False,
                            "explanation": "pH değeri taşa göre değişir, metastabil bölgenin genel kuralı tohum varlığıdır."
                        },
                        {
                            "text": "Tüm idrar proteinlerinin tamamen idrardan uzaklaştırılması",
                            "isCorrect": False,
                            "explanation": "Proteinler nidus veya inhibitör olabilir, metastabil bölgeyi tek başına tanımlamaz."
                        },
                        {
                            "text": "Sıcaklığın vücut ısısının çok altına düşmesi",
                            "isCorrect": False,
                            "explanation": "Sıcaklık düşüşü in vivo taş oluşumunun koşulu değildir."
                        }
                    ],
                    "Metastabil bölgede spontan homojen nükleasyon oluşamaz; heterojen nidus gereklidir."
                ),
                make_active_recall(
                    "İdrardaki doğal inhibitörlerin (sitrat, magnezyum vb.) artması metastabilitenin üst sınırı (ULM) eğrisini nasıl etkiler?",
                    "ULM sınırını yukarı kaydırarak spontan çökelmeyi zorlaştırır ve koruyucu aralığı genişletir.",
                    "Eşik değerin yükseltilmesi"
                )
            ]
        },
        # Slayt 35
        {
            "slideNumber": 35,
            "title": "Kararsız (Unstabil) Bölge ve Spontan Çökelme",
            "content": (
                "İdrarda çözünen iyonların konsantrasyonu aşırı yükseldiğinde ve metastabilitenin üst sınırı (ULM) aşıldığında, "
                "sistem 'kararsız' (unstabil) bölgeye geçer. Bu bölgede termodinamik itici güç o kadar şiddetlidir ki, aktivasyon "
                "enerjisi bariyeri kendiliğinden aşılır. Herhangi bir yabancı yüzeye veya nidusa ihtiyaç kalmaksızın, "
                "çözeltideki iyonlar de novo olarak birbirleriyle birleşip aniden katı kristal fazına geçerler (homojen nükleasyon). "
                "Bu durum yoğun dehidratasyonda veya primer hiperoksalürili bir hastada idrar oksalatının aşırı yükselmesi "
                "sonucu masif intratübüler kristal yağmurları (kristalüri fırtınası) şeklinde klinik tabloya yansır."
            ),
            "elements": [
                make_cloze(
                    "Metastabilitenin üst sınırı aşıldığında sistem kararsız bölgeye geçerek kendiliğinden kristalleşme başlatır.",
                    "kararsız bölgeye",
                    "Unstabil termodinamik faz"
                ),
                make_before_after(
                    "Metastabil vs Kararsız Bölgenin Kristal Davranışı",
                    "Metastabil Bölge",
                    "Spontan kristal oluşamaz; yalnızca tohum veya plak varlığında yavaş heterojen büyüme gerçekleşir.",
                    "Kararsız (Unstabil) Bölge",
                    "Yabancı çekirdeğe gerek yoktur; aşırı süpersatürasyon nedeniyle anında kitlesel homojen kristal çöker.",
                    "Kararsız bölgeye geçiş akut tübüler obstrüksiyon ve tübüler nekroz riskini dramatik artırır."
                )
            ]
        },
        # Slayt 36
        {
            "slideNumber": 36,
            "title": "Çekirdeklenme (Nükleasyon): Homojen Çekirdeklenme",
            "content": (
                "Çekirdeklenme (nükleasyon), bir çözeltideki serbest iyonların kümelenerek kararlı bir katı kristal nükleusu "
                "oluşturduğu ilk ve en kritik faz değişim basamağıdır. Homojen çekirdeklenme, saf bir çözeltide hiçbir yabancı "
                "partikül veya yüzey olmaksızın, tamamen aynı türden iyonların çarpışarak kararlı kritik küme çapına ulaşması "
                "sürecidir. Kritik yarıçapa ulaşamayan küçük iyon kümeleri kararsızdır ve termodinamik olarak yeniden çözünür; "
                "ancak kritik yarıçap aşıldığında yüzey enerjisi hacim enerjisi tarafından dengelenir ve kristal sürekli "
                "büyümeye başlar. Homojen çekirdeklenme çok yüksek aktivasyon enerjisi gerektirdiğinden in vivo koşullarda nadirdir."
            ),
            "elements": [
                make_active_recall(
                    "Homojen çekirdeklenmenin in vivo biyolojik idrarda nadir görülmesinin temel fizikokimyasal nedeni nedir?",
                    "Aşırı yüksek aktivasyon enerjisi gerektirmesi ve idrarda daima hücresel veya organik yabancı yüzeylerin bulunmasıdır.",
                    "Termodinamik enerji bariyeri"
                ),
                make_micro_quiz(
                    "Kristal nükleusunun kararlı kalıp sürekli büyümesini garantileyen fiziksel eşik kavramı hangisidir?",
                    [
                        {
                            "text": "Kritik nükleus yarıçapının aşılması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; kritik yarıçap aşıldığında serbest enerji kazancı çökelmeyi kalıcı kılar."
                        },
                        {
                            "text": "Çözeltideki tüm su moleküllerinin buharlaşması",
                            "isCorrect": False,
                            "explanation": "İn vivo idrarda böyle bir durum söz konusu olamaz."
                        },
                        {
                            "text": "Ortam pH'ının tam nötr 7.0 olması",
                            "isCorrect": False,
                            "explanation": "pH değeri taşa özgüdür; nükleasyonun genel kuralı kritik yarıçaptır."
                        },
                        {
                            "text": "Bakteriyel endotoksin varlığı",
                            "isCorrect": False,
                            "explanation": "Endotoksin homojen nükleasyonun bir bileşeni değildir."
                        }
                    ],
                    "Kritik çekirdek yarıçapı, kristalin erime ile büyüme arasındaki kararlılık sınırıdır."
                )
            ]
        },
        # Slayt 37
        {
            "slideNumber": 37,
            "title": "Heterojen Çekirdeklenme: Nidus ve Enerji Bariyeri",
            "content": (
                "Heterojen çekirdeklenme, insan vücudundaki taş oluşumunun ezici çoğunluğundan sorumlu olan mekanizmadır. "
                "Bu süreçte kristal nükleasyonu saf çözeltide değil, mevcut yabancı bir katı yüzey (nidus) üzerinde gerçekleşir. "
                "Nidus görevi gören yapılar arasında soyulmuş tübüler epitel hücreleri, hücresel membran lipidleri, eritrositler, "
                "ürat kristalleri, Randall plakları veya bakteri kolonileri yer alır. Yabancı yüzeyin varlığı, kristal kafesi "
                "oluşturmak için gereken yüzey serbest enerjisini ve aktivasyon bariyerini dramatik biçimde düşürür. Böylece "
                "idrar çok daha düşük süpersatürasyon seviyelerindeyken bile hızlı kristal çökelmesi tetiklenebilir."
            ),
            "elements": [
                make_before_after(
                    "Homojen vs Heterojen Çekirdeklenme Mekanizmaları",
                    "Homojen Çekirdeklenme",
                    "Saf ortam, yabancı yüzey yok, devasa aktivasyon enerjisi gerekir, sadece kararsız bölgede (SS > ULM) görülür.",
                    "Heterojen Çekirdeklenme",
                    "Nidus veya epitel yüzeyi var, aktivasyon enerjisi çok düşüktür, ılımlı metastabil bölgede (SS > 1) bile kolayca başlar.",
                    "Böbrek taşlarının neredeyse tamamı biyolojik zeminlerde heterojen çekirdeklenmeyle başlar."
                ),
                make_cloze(
                    "Yabancı bir yüzey veya hücresel döküntü üzerinde düşük enerjiyle başlayan nükleasyona heterojen çekirdeklenme denir.",
                    "heterojen çekirdeklenme",
                    "Nidus aracılı kristal başlangıcı"
                )
            ]
        },
        # Slayt 38
        {
            "slideNumber": 38,
            "title": "Epitaksi Kavramı ve Kafes Uyumlu Kristal Büyümesi",
            "content": (
                "Epitaksi, kristalografide bir kristal türünün yüzeyinde, kristal kafes parametreleri geometrik olarak birbirine "
                "benzeyen tamamen farklı kimyasal yapıdaki ikinci bir kristalin büyümesi olgusudur. Ürolojideki en klasik "
                "ve klinik olarak en önemli epitaksi örneği, sodyum hidrojen ürat veya ürik asit kristallerinin oluşturduğu "
                "bir nidus üzerinde kalsiyum oksalat taşının hızla büyümesidir. Ürik asit kristalinin atomik aralıkları "
                "kalsiyum oksalat kafesine şablon (matris) oluşturacak derecede uyumludur. Bu nedenle hiperürikozürik "
                "hastalarda idrarda ürik asit kristalleri oluştuğunda, bu kristaller kalsiyum oksalat için ideal bir epitaktik "
                "yatak işlevi görerek mikst taş litogenezini kat kat hızlandırır."
            ),
            "elements": [
                make_cloze(
                    "Benzer kafes yapısına sahip farklı bir kristal yüzeyinde yeni bir kristalin büyümesine epitaksi adı verilir.",
                    "epitaksi",
                    "Kafes uyumlu heterojen büyüme"
                ),
                make_causal_chain(
                    "Ürik Asit Nidusundan Kalsiyum Oksalat Taşına Epitaktik Yol",
                    [
                        "1. Hiperürikozüri: Diyetle pürin alımı veya metabolik asidozla idrarda ürik asit/ürat yükselmesi",
                        "2. Ürik Asit Kristalizasyonu: Asidik idrarda mikroskobik ürat veya ürisit kristallerinin çökmesi",
                        "3. Kafes Uyumu: Ürat kristal yüzeyindeki atomik aralıkların kalsiyum oksalat ile geometrik eşleşmesi",
                        "4. Epitaktik Büyüme: Kalsiyum ve oksalat iyonlarının bu hazır şablona tutunarak taşlaşması"
                    ]
                )
            ]
        },
        # Slayt 39 [CHECKPOINT 4]
        {
            "slideNumber": 39,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Fizikokimya, Süpersatürasyon ve Çekirdeklenme",
            "content": (
                "Bu bölümde taş oluşumunun fizikokimyasal ve termodinamik dinamiklerini ayrıntılarıyla inceledik. "
                "Süpersatürasyon (SS), taş oluşumunun vazgeçilmez itici gücüdür; SS < 1 doymamış bölge olup çözünme baskındır. "
                "SS > 1 ile ULM arası metastabil bölgedir; burada spontan kristal oluşamaz, ancak mevcut bir nidus üzerinde büyüme olur. "
                "ULM aşıldığında sistem kararsız hale gelir ve de novo homojen nükleasyonla ani kristal çökelmesi gelişir. "
                "Homojen çekirdeklenme yüksek aktivasyon enerjisi gerektirdiği için in vivo nadirdir; insan taşları temelde heterojen çekirdeklenmeyle başlar. "
                "Hücresel artıklar, Randall plakları ve epitel yüzeyleri enerji bariyerini düşürerek heterojen nükleasyona yataklık eder. "
                "Epitaksi, kafes uyumu sayesinde ürik asit nidusu üzerinde kalsiyum oksalat taşının büyümesi sürecidir."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp04-fc01",
                    "front": "Termodinamik aşırı doygunluğun metastabilitenin üst sınırını (ULM) aşmasıyla başlayan kendiliğinden nükleasyon tipine ne ad verilir?",
                    "back": "Homojen çekirdeklenme adı verilir.",
                    "hint": "Yabancı yüzey gerektirmeyen de novo çökme"
                },
                {
                    "id": "k1-27-cp04-fc02",
                    "front": "Biyolojik sistemlerde aktivasyon enerjisini düşüren yabancı partikül veya doku yüzeyinde gelişen yaygın nükleasyon türü nedir?",
                    "back": "Heterojen çekirdeklenme sürecidir.",
                    "hint": "Nidus varlığında başlayan litik adım"
                },
                {
                    "id": "k1-27-cp04-fc03",
                    "front": "Kristal kafes benzerliği nedeniyle ürik asit kristal tohumu üzerinde kalsiyum oksalatın büyümesini tanımlayan terim nedir?",
                    "back": "Epitaksi kavramıdır.",
                    "hint": "Kafes uyumu temelli geometrik büyüme"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 4 Özet Tablosu: Fizikokimyasal Fazlar ve Termodinamik Eşikler",
                    ["Termodinamik Bölge", "SS Değeri", "Nükleasyon Tipi", "Klinik Özellik"],
                    [
                        {
                            "cells": ["Doymamış", "SS < 1.0", "Yok (Çözünme var)", "Hedeflenen tedavi edici idrar fazı"],
                            "hiddenIndex": 0,
                            "hint": "Erimeyi sağlayan seyreltik durum"
                        },
                        {
                            "cells": ["Metastabil", "1.0 < SS < ULM", "Heterojen (Nidus bağımlı)", "Epitel plağı ve hücresel debrisle taşlaşma"],
                            "hiddenIndex": 2,
                            "hint": "Yabancı yüzey destekli çökme"
                        },
                        {
                            "cells": ["Kararsız", "SS > ULM", "Homojen (Kendiliğinden)", "Masif intratübüler kristal yağmuru"],
                            "hiddenIndex": 2,
                            "hint": "Tohumsuz spontan nükleus"
                        }
                    ]
                )
            ]
        },
        # Slayt 40
        {
            "slideNumber": 40,
            "title": "Klinik Karar: Süpersatürasyon Profiline Dayalı Tedavi",
            "content": (
                "Tekrarlayan taş hastalarında yapılan 24 saatlik idrar analizlerinde kalsiyum oksalat süpersatürasyonu "
                "(CaOx SS) ve ürik asit süpersatürasyonu (UA SS) hesaplanarak risk profili objektif olarak belirlenir. "
                "Eğer CaOx SS değeri metastabil sınırların üzerindeyse, ilk tedavi hedefi idrar hacmini en az 2.5 litrenin "
                "üzerine çıkararak SS değerini 1.0'e yaklaştırmak ve idrar sitratını artırmaktır. Eşlik eden hiperürikozüri "
                "saptanan ve epitaksi riski taşıyan bir hastada ise idrar pH'ı 6.2 - 6.8 aralığında titre edilerek hem "
                "ürik asit nidusu oluşumu engellenmeli hem de kalsiyum fosfat çökmesini tetikleyecek aşırı alkalinizasyondan kaçınılmalıdır."
            ),
            "elements": [
                make_branching_logic(
                    "38 yaşında erkek hasta, son 3 yılda iki kez kalsiyum oksalat taşı düşürmüş. 24 saatlik idrar analizinde idrar hacmi 1100 mL, kalsiyum normal, ancak ürik asit atılımı 850 mg/gün (yüksek) ve idrar pH'ı 5.2 olarak ölçülüyor.",
                    "Bu hastada epitaksi yoluyla kalsiyum oksalat taşı nüksünü önleyecek en akılcı terapötik müdahale nedir?",
                    [
                        {
                            "text": "Günlük idrar hacmini 2.5 litrenin üzerine çıkaracak hidrasyon sağlanmalı ve potasyum sitrat ile idrar pH'ı 6.2-6.8 aralığına yükseltilerek ürik asit nidusu önlenmelidir.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; pH'ı 6.2-6.8'e çekmek ürik asidi çözer ve epitaktik kalsiyum oksalat çökmesini engeller."
                        },
                        {
                            "text": "İdrarı daha da asitleştirmek için askorbik asit (C vitamini) verilmelidir.",
                            "isCorrect": False,
                            "explanation": "C vitamini oksalata dönüşür ve idrarı asitleştirerek ürik asit çökmesini daha da artırır."
                        },
                        {
                            "text": "Kalsiyum emilimini sıfırlamak için diyetten tüm kalsiyum tamamen çıkarılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Diyet kalsiyumunu kısıtlamak bağırsakta oksalat emilimini artırarak taş riskini paradoksal olarak yükseltir."
                        }
                    ]
                )
            ]
        }
    ]
