# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 2: Taş Sınıflaması, Kimyasal Bileşim ve Mineral Adları (Slayt 11 - 20)
Checkpoint: Slayt 19
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_2_slides():
    return [
        # Slayt 11
        {
            "slideNumber": 11,
            "title": "Etiyolojik Taş Sınıflaması: Dört Temel Kategori",
            "content": (
                "Üriner sistem taşları patofizyolojik kökenlerine ve litogenik itici güçlerine göre dört ana grupta incelenir: "
                "enfeksiyon dışı taşlar, enfeksiyon taşları, genetik taşlar ve ilaç taşları. Enfeksiyon dışı taşlar tüm üriner "
                "kalküllerin en büyük bölümünü oluşturur; kalsiyum oksalat, kalsiyum fosfat ve ürik asit bu kümenin temel taşlarıdır. "
                "Enfeksiyon taşları, üreaz pozitif mikroorganizmaların oluşturduğu alkali ortamda magnezyum amonyum fosfat (strüvit) "
                "ve karbonat apatit şeklinde gelişir. Genetik taşlar sistin, ksantin ve 2,8-dihidroksiadenin metabolik enzim ya da "
                "taşıyıcı defektlerinden kaynaklanır. İlaç taşları ise doğrudan idrarda kristalleşen ya da biyokimyasal dengeyi bozan farmakolojik ajanlardır."
            ),
            "elements": [
                make_table(
                    "Etiyolojik Taş Sınıflandırması ve Karakteristik Örnekler",
                    ["Etiyolojik Grup", "Ana Taş Tipleri", "Temel Patofizyolojik Zemin"],
                    [
                        {
                            "cells": ["Enfeksiyon Dışı", "Kalsiyum oksalat, kalsiyum fosfat, ürik asit", "Metabolik anormallikler, diyet ve dehidratasyon"],
                            "hiddenIndex": 1,
                            "hint": "En yaygın görülen kalsiyum ve ürat bileşikleri"
                        },
                        {
                            "cells": ["Enfeksiyon Taşları", "Strüvit, karbonat apatit, amonyum ürat", "Üreaz üreten bakteriyel enfeksiyonlar"],
                            "hiddenIndex": 2,
                            "hint": "Mikroorganizma kaynaklı enzim aktivitesi"
                        },
                        {
                            "cells": ["Genetik Taşlar", "Sistin, ksantin, 2,8-dihidroksiadenin", "Monogenik enzim veya taşıyıcı protein mutasyonları"],
                            "hiddenIndex": 1,
                            "hint": "Metabolik ve aminoasit kökenli taşlar"
                        }
                    ]
                ),
                make_cloze(
                    "Böbrek taşlarının büyük kısmını oluşturan kalsiyum oksalat ve ürik asit taşları enfeksiyon dışı taşlar kategorisinde yer alır.",
                    "enfeksiyon dışı taşlar",
                    "Metabolik kaynaklı kalkül grubu"
                )
            ]
        },
        # Slayt 12
        {
            "slideNumber": 12,
            "title": "Kalsiyum Oksalat Monohidrat (Whewellit)",
            "content": (
                "Kalsiyum oksalat monohidrat (COM), mineralojik adıyla whewellit, insanlarda en sık saptanan üriner taş formudur. "
                "Oldukça sert, yoğun, koyu kahverengi veya siyah renkte olup pürüzsüz ya da nodüler bir yüzeye sahiptir. "
                "Whewellit oluşumu idrardaki serbest oksalat konsantrasyonu ile son derece yakından ilişkilidir; oksalat "
                "konsantrasyonundaki küçük bir artış bile çözünürlük çarpımını hızla aşarak bu kristalin çökmesini tetikler. "
                "Elektron mikroskopisinde elips veya halter (dumbbell) şeklinde görülür. Whewellit kristalleri tübüler epitel "
                "hücrelerinin apikal membranındaki fosfatidilserin ve sialik asit kalıntılarına güçlü bir afinite ile bağlanır."
            ),
            "elements": [
                make_cloze(
                    "Kalsiyum oksalat monohidrat kristalinin standart mineralojik literatürdeki adı whewellit olarak bilinir.",
                    "whewellit",
                    "Monohidrat formun mineral ismi"
                ),
                make_active_recall(
                    "Kalsiyum oksalat monohidrat (whewellit) oluşumunda idrardaki hangi iyonun artışı kalsiyuma kıyasla litogenezi kat kat daha güçlü tetikler?",
                    "Oksalat iyonunun konsantrasyonundaki artış çok daha belirleyici bir itici güçtür.",
                    "Dikarbonik asit tuzu"
                )
            ]
        },
        # Slayt 13
        {
            "slideNumber": 13,
            "title": "Kalsiyum Oksalat Dihidrat (Weddellit)",
            "content": (
                "Kalsiyum oksalat dihidrat (COD), mineralojik adıyla weddellit, idrarda kalsiyum konsantrasyonunun yüksek "
                "olduğu durumlarda (hiperkalsiüri) öncelikli olarak kristalleşir. Morfolojik olarak açık sarı veya bal renginde, "
                "yüzeyinde keskin çıkıntılar ve piramidal uçlar bulunan kırılgan bir yapı sergiler. İdrar mikroskopisinde "
                "karakteristik olarak 'mektup zarfı' veya çift piramit (bipiramidal) geometrisinde gözlenir. Whewellite kıyasla "
                "böbrek epitel hücrelerine adezyon yeteneği daha zayıftır; bu nedenle spontan pasajla idrarla atılma şansı "
                "daha yüksektir. Ancak yüksek kalsiyum süpersatürasyonu devam ettiğinde agregasyona uğrayarak kalikslerde takılı kalabilir."
            ),
            "elements": [
                make_before_after(
                    "Kalsiyum Oksalat Kristal Türlerinin Karşılaştırması",
                    "Monohidrat (Whewellit)",
                    "Aşırı oksalat bağımlı, koyu renkli, çok sert, yüksek epitel yapışma afinitesi, mikroskopide halter/oval şekil.",
                    "Dihidrat (Weddellit)",
                    "Aşırı kalsiyum bağımlı, açık renkli, kırılgan, zarf şeklinde bipiramidal kristaller, daha düşük epitel afinitesi.",
                    "Taş analizinde weddellit baskınlığı primer olarak hiperkalsiüriyi düşündürür."
                ),
                make_micro_quiz(
                    "İdrar mikroskopisinde klasik 'mektup zarfı' görünümü veren ve hiperkalsiüri ile ilişkili olan mineral hangisidir?",
                    [
                        {
                            "text": "Weddellit (Kalsiyum oksalat dihidrat)",
                            "isCorrect": True,
                            "explanation": "Doğrudur; dihidrat formu karakteristik bipiramidal zarf görünümündedir."
                        },
                        {
                            "text": "Whewellit (Kalsiyum oksalat monohidrat)",
                            "isCorrect": False,
                            "explanation": "Whewellit halter veya oval biçimli mikroskobik kristaller oluşturur."
                        },
                        {
                            "text": "Strüvit (Magnezyum amonyum fosfat)",
                            "isCorrect": False,
                            "explanation": "Strüvit kristalleri tabut kapağı (coffin-lid) görünümündedir."
                        },
                        {
                            "text": "Sistin kristalleri",
                            "isCorrect": False,
                            "explanation": "Sistin kristalleri karakteristik altıgen (hekzagonal) plaklar şeklindedir."
                        }
                    ],
                    "Kalsiyum oksalat dihidrat kristalleri zarf geometrisiyle ayırt edilir."
                )
            ]
        },
        # Slayt 14
        {
            "slideNumber": 14,
            "title": "Kalsiyum Fosfat Taşları: Apatit ve Bruşit",
            "content": (
                "Kalsiyum fosfat taşları, alkali idrar ortamında (pH >6.5) çöken ve renal tübüllere ciddi hasar verme potansiyeline "
                "sahip iki temel mineral formunda bulunur: apatit ve bruşit. Bazik kalsiyum fosfat (karbonat apatit), böbreğin "
                "Randall plaklarının çekirdek yapısını oluşturan ana bileşendir. Kalsiyum hidrojen fosfat dihidrat (bruşit) ise "
                "son derece sert, kristal yapısı yoğun ve ekstrakorporeal şok dalga litotripsiye (ESWL) en dirençli taş formudur. "
                "Bruşit taşları genellikle renal tübüllerde tıkaçlar oluşturarak hızlı nefrokalsinozis ve nefron kaybına yol açar; "
                "distal renal tübüler asidoz ve primer hiperparatiroidi zemininde sıklıkla görülür."
            ),
            "elements": [
                make_table(
                    "Kalsiyum Fosfat Taşlarının Mineral Özellikleri",
                    ["Mineral Adı", "Kimyasal Yapı", "Optimal pH Ortamı", "Klinik ve Tedavi Özelliği"],
                    [
                        {
                            "cells": ["Apatit", "Bazik kalsiyum fosfat", "Alkali (pH > 6.5)", "Randall plaklarının temel minerali"],
                            "hiddenIndex": 3,
                            "hint": "Papilla altındaki kalsiyum plağı"
                        },
                        {
                            "cells": ["Bruşit", "Kalsiyum hidrojen fosfat", "Hafif alkali/nötr", "ESWL kırmaya en dirençli taş formu"],
                            "hiddenIndex": 3,
                            "hint": "Şok dalga tedavisinde kırılmama özelliği"
                        }
                    ]
                ),
                make_active_recall(
                    "Şok dalga litotripsi (ESWL) tedavisine en dirençli olan kalsiyum fosfat minerali hangisidir?",
                    "Bruşit (kalsiyum hidrojen fosfat) mineralidir.",
                    "Sert kalsiyum fosfat türevi"
                )
            ]
        },
        # Slayt 15
        {
            "slideNumber": 15,
            "title": "Strüvit ve Karbonat Apatit: Enfeksiyon Taşları",
            "content": (
                "Magnezyum amonyum fosfat hekzahidrat, mineralojik adıyla strüvit, klasik enfeksiyon taşıdır. Üreaz enzimine "
                "sahip bakterilerin (başta Proteus mirabilis olmak üzere Klebsiella, Pseudomonas ve Staphylococcus türleri) "
                "üriner sistemde kolonize olmasıyla oluşur. Bakteriyel üreaz üreyi amonyak ve karbondioksite hidrolize eder; "
                "amonyak ortamdaki protonları bağlayarak amonyuma dönüşür ve idrar pH'ı dramatik biçimde 7.2 - 8.0'in üzerine çıkar. "
                "Bu aşırı alkali ve amonyum zengini ortamda strüvit ve karbonat apatit eş zamanlı çökerek pelvikaliseal sistemi "
                "tamamen dolduran geyik boynuzu (staghorn) taşlarını meydana getirir."
            ),
            "elements": [
                make_causal_chain(
                    "Üreaz Pozitif Enfeksiyondan Strüvit Taşına Giden Biyokimyasal Yol",
                    [
                        "1. Bakteriyel Kolonizasyon: Proteus mirabilis gibi üreaz pozitif bakterilerin üriner traktusa yerleşmesi",
                        "2. Üre Hidrolizi: Üreazın üreyi amonyak ve karbondioksite parçalaması",
                        "3. İdrar Alkalinizasyonu: Amonyağın tamponlanarak amonyuma dönmesi ve idrar pH'ının 7.5 üzerine fırlaması",
                        "4. Kristal Çökelmesi: Amonyum, magnezyum ve fosfat iyonlarının birleşerek strüvit kristallerini oluşturması",
                        "5. Staghorn Gelişimi: Organik biyofilm ve matris desteğiyle tüm toplayıcı sistemi dolduran kitle oluşumu"
                    ]
                ),
                make_cloze(
                    "Enfeksiyon taşlarının prototipi olan magnezyum amonyum fosfat bileşiğinin mineral adı strüvit olarak adlandırılır.",
                    "strüvit",
                    "Geyik boynuzu taş minerali"
                )
            ]
        },
        # Slayt 16
        {
            "slideNumber": 16,
            "title": "Ürik Asit (Ürisit) ve Amonyum Ürat Taşları",
            "content": (
                "Ürik asit taşları mineralojik olarak ürisit olarak adlandırılır ve tüm taşların yaklaşık %8-10'unu teşkil eder. "
                "Ürik asit zayıf bir organik asittir ve pKa değeri 5.35'tir. İdrar pH'ı 5.35'in altına düştüğünde çözünürlüğü "
                "yüksek olan ürat iyonları hızla çözünmeyen serbest ürik aside dönüşür ve kristalleşir. Ürik asit taşlarının "
                "oluşumundaki primer belirleyici hiperürikozüriden ziyade persistan asidik idrardır. Amonyum ürat taşları ise "
                "hem hiperürikozüri hem de aşırı amonyum varlığında (örneğin laksatif suistimali veya malnütrisyon zemininde) "
                "gelişen nadir bir taş formudur."
            ),
            "elements": [
                make_cloze(
                    "Ürik asidin dissosiasyon sabiti olan pKa değeri beş virgül otuz beş seviyesindedir.",
                    "beş virgül otuz beş",
                    "Asit yarı iyonizasyon eşik sabiti"
                ),
                make_active_recall(
                    "Ürik asit taşlarının oluşumunda hiperürikozüriden çok daha kritik olan fizyopatolojik belirleyici nedir?",
                    "İdrar pH'ının kronik olarak aşırı asidik (5.5'in altında) seyretmesidir.",
                    "Düşük hidrojen konsantrasyon tamponu"
                )
            ]
        },
        # Slayt 17
        {
            "slideNumber": 17,
            "title": "Genetik Taş Tipleri: Sistin, Ksantin ve 2,8-DHA",
            "content": (
                "Genetik taşlar nadir görülmekle birlikte genç yaşta başlamaları ve agresif rekürrens sergilemeleri nedeniyle "
                "büyük klinik öneme sahiptir. Sistinüri, proksimal tübül ve ince bağırsaktaki dibazik amino asit taşıyıcılarının "
                "(sistin, ornitin, lizin, arjinin - COLA) otozomal resesif bozukluğudur; idrarda çözünürlüğü son derece kısıtlı "
                "olan sistin birikerek taşlaşır. Ksantinüri, ksantin dehidrogenaz enzim eksikliği sonucu pürin yıkımının ksantin "
                "aşamasında durmasıyla oluşur. 2,8-dihidroksiadenin (2,8-DHA) taşları ise adenin fosforiboziltransferaz (APRT) "
                "enzim eksikliğinde gelişir; ürik asit taşı ile sıkça karıştırılır ancak allopurinole dirençli renal hasar yapar."
            ),
            "elements": [
                make_table(
                    "Monogenik Metabolik Taş Bozuklukları ve Enzim/Taşıyıcı Defektleri",
                    ["Taş Tipi", "Defektif Protein / Enzim", "Kalıtım Kalıbı", "İdrar Özelliği"],
                    [
                        {
                            "cells": ["Sistin Taşı", "SLC3A1 / SLC7A9 (COLA taşıyıcısı)", "Otozomal Resesif", "Hekzagonal kristaller, pozitif sodyum nitroprussid"],
                            "hiddenIndex": 3,
                            "hint": "Altıgen kristal morfolojisi"
                        },
                        {
                            "cells": ["2,8-DHA Taşı", "Adenin fosforiboziltransferaz (APRT)", "Otozomal Resesif", "Yuvarlak kahverengi kristaller, polarize ışıkta haç deseni"],
                            "hiddenIndex": 1,
                            "hint": "Adenin metabolizma enzimi"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Dibazik amino asitlerin renal geri emilim bozukluğu sonucu gelişen sistinüride taşınan amino asit grubu hangisidir?",
                    [
                        {
                            "text": "Sistin, Ornitin, Lizin, Arjinin (COLA)",
                            "isCorrect": True,
                            "explanation": "Doğrudur; bu dört amino asidin epitelyal taşıyıcı sistemi ortaktır."
                        },
                        {
                            "text": "Glisin, Alanin, Serin, Treonin",
                            "isCorrect": False,
                            "explanation": "Nötral amino asitlerdir; sistinüri taşıyıcısıyla ilişkili değildir."
                        },
                        {
                            "text": "Fenilalanin, Tirozin, Triptofan",
                            "isCorrect": False,
                            "explanation": "Aromatik amino asitlerdir; sistinüri ile ilgisi yoktur."
                        },
                        {
                            "text": "Aspartat, Glutamat",
                            "isCorrect": False,
                            "explanation": "Asidik amino asitlerdir; farklı taşıyıcılar kullanırlar."
                        }
                    ],
                    "Sistinüri, COLA akronimiyle kodlanan dibazik amino asitlerin transport defektidir."
                )
            ]
        },
        # Slayt 18
        {
            "slideNumber": 18,
            "title": "İlaç Taşları ve Matris Taşlarının Ayırıcı Tanısı",
            "content": (
                "İlaç taşları iki ana mekanizmayla oluşur: ilacın kendisinin idrarda doğrudan çözünmeyip kristalleşmesi "
                "(örneğin HIV tedavisinde kullanılan proteaz inhibitörü indinavir, triamteren, sülfonamidler, guaifenesin) "
                "veya ilacın metabolik dengeyi bozarak ikincil litogeneze yol açması (karbonik anhidraz inhibitörleri asetazolamid "
                "ve topiramat gibi hipositratüri ve alkali idrar yapan ajanlar). Matris taşları ise mineral içeriği çok düşük "
                "(<%35), organik protein ve mukopolisakkarit içeriği ise %65'e varan yumuşak kıvamlı taşlardır. Genellikle "
                "kronik piyelonefrit ve Proteus enfeksiyonu zemininde radyolüsen kitleler olarak izlenir."
            ),
            "elements": [
                make_before_after(
                    "İlaç Taşı Mekanizmalarının Karşılaştırması",
                    "Doğrudan Çöken İlaç Taşları (İndinavir vb.)",
                    "İlacın kendisi veya metaboliti idrarda doygunluğa ulaşır, radyolüsen kristaller çöker, metabolik tarama normaldir.",
                    "İkincil Metabolik İlaç Taşları (Topiramat / Tiyazid)",
                    "İlaç renal tübülleri etkiler; sistemik asidoz, hipositratüri veya hücre içi asidoz yaratarak kalsiyum fosfat taşını tetikler.",
                    "İlaç öyküsü alınmadan yapılan metabolik değerlendirmeler yanıltıcı tanıya sebep olabilir."
                ),
                make_active_recall(
                    "Yüksek organik protein içeriğine (%65'e kadar) sahip olan ve kronik enfeksiyon zemininde gelişen yumuşak kıvamlı taş hangisidir?",
                    "Matris taşıdır.",
                    "Düşük mineralli jelatinöz taş"
                )
            ]
        },
        # Slayt 19 [CHECKPOINT 2]
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Taş Sınıflaması ve Mineral Terminolojisi",
            "content": (
                "Bu bölümde taşların etiyolojik sınıflandırmasını ve standart mineralojik adlandırmalarını ele aldık. "
                "Taşlar enfeksiyon dışı, enfeksiyon, genetik ve ilaç kaynaklı olarak dört ana gruba ayrılır. "
                "Kalsiyum oksalat monohidrat 'whewellit' adını alır; oksalata duyarlıdır ve sert, koyu renkli taşlar yapar. "
                "Kalsiyum oksalat dihidrat 'weddellit'tir; hiperkalsiüri zemininde mektup zarfı şeklinde piramidal kristaller oluşturur. "
                "Kalsiyum fosfatlar apatit ve bruşit olarak ikiye ayrılır; bruşit ESWL'ye en dirençli taş türüdür. "
                "Strüvit, üreaz pozitif bakterilerin alkali idrar ortamında oluşturduğu magnezyum amonyum fosfattır. "
                "Ürik asit taşları (ürisit) düşük idrar pH'ı zemininde çökerken, sistin taşları COLA taşıyıcı defektinden doğar. "
                "İndinavir doğrudan çöken ilaç taşlarının, matris taşları ise organik protein içeriği zengin enfeksiyon kitlelerinin örneğidir."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp02-fc01",
                    "front": "Kalsiyum oksalat monohidrat ve kalsiyum oksalat dihidrat bileşiklerinin literatürdeki mineral isimleri sırasıyla nedir?",
                    "back": "Sırasıyla whewellit ve weddellit isimlerini alır.",
                    "hint": "Monohidrat ve dihidrat mineralojik terimleri"
                },
                {
                    "id": "k1-27-cp02-fc02",
                    "front": "Ekstrakorporeal şok dalga litotripsiye (ESWL) mekanik olarak en dirençli kabul edilen kalsiyum fosfat türevi hangisidir?",
                    "back": "Kalsiyum hidrojen fosfat dihidrat türevi olan bruşittir.",
                    "hint": "Kırılması en çetin çökelek"
                },
                {
                    "id": "k1-27-cp02-fc03",
                    "front": "Proteus mirabilis üreaz aktivitesiyle ortaya çıkan magnezyum amonyum fosfat hekzahidratın mineral adı nedir?",
                    "back": "Strüvit olarak adlandırılır.",
                    "hint": "Enfeksiyon kalkülünün literatürdeki unvanı"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 2 Özet Tablosu: Taşların Mineral ve Kimyasal Eşleşmesi",
                    ["Kimyasal Bileşim", "Mineralojik Adı", "Karakteristik Özellik"],
                    [
                        {
                            "cells": ["Kalsiyum oksalat monohidrat", "Whewellit", "Aşırı sert, koyu renkli, oksalat bağımlı"],
                            "hiddenIndex": 1,
                            "hint": "En yaygın monohidrat minerali"
                        },
                        {
                            "cells": ["Kalsiyum hidrojen fosfat", "Bruşit", "ESWL kırmaya dirençli, nefrokalsinozis riski"],
                            "hiddenIndex": 1,
                            "hint": "Dirençli kalsiyum fosfat türü"
                        }
                    ]
                )
            ]
        },
        # Slayt 20
        {
            "slideNumber": 20,
            "title": "Klinik Karar: Taş Analiz Raporunun Yorumlanması",
            "content": (
                "Spontan düşürülen veya endoürolojik cerrahi ile çıkarılan tüm taşlara X-ışını difraksiyonu veya Fourier "
                "dönüşümlü kızılötesi spektroskopisi (FTIR) ile mineralojik analiz yapılmalıdır. Taş analizinde %100 "
                "oranında weddellit saptanması primer hiperkalsiüriyi düşündürürken, whewellit baskınlığı enterik hiperoksalüriyi "
                "veya diyet kaynaklı oksalat aşırılığını işaret eder. Taşın strüvit çıkması mutlaka geçirilmiş veya mevcut üreaz "
                "pozitif enfeksiyon varlığını kanıtlar ve cerrahi sonrası idrar kültürlerinin steril kalmasını zorunlu kılar. "
                "Sistin saptanması ise hastanın ömür boyu alkali idrar ve yüksek hidrasyon tedavisi almasını gerektirir."
            ),
            "elements": [
                make_branching_logic(
                    "28 yaşında kadın hastadan perkütan nefrolitotomi ile çıkarılan geyik boynuzu taşın FTIR analizinde magnezyum amonyum fosfat (strüvit) ve karbonat apatit karışımı rapor ediliyor.",
                    "Bu patolojik analiz sonucuna göre hastanın nüks önleme ve medikal yönetim stratejisi ne olmalıdır?",
                    [
                        {
                            "text": "Üreaz üreten bakteriyel enfeksiyon tamamen eradike edilmeli, taş fragmanı kalmadığından emin olunmalı ve idrar kültürleri düzenli izlenmelidir.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; strüvit taşları enfeksiyon taşlarıdır ve bakteriyel eradikasyon olmadan hızla tekrarlarlar."
                        },
                        {
                            "text": "İdrarı daha da alkalileştirmek için yüksek doz potasyum sitrat başlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Strüvit taşları alkali ortamda çöker; sitratla daha fazla alkalileştirmek taşı büyütür."
                        },
                        {
                            "text": "Hastada pürin kısıtlaması yapılarak allopurinol tedavisi planlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Pürin metabolizması ürik asit taşıyla ilgilidir, strüvit taşıyla bağlantısı yoktur."
                        }
                    ]
                )
            ]
        }
    ]
