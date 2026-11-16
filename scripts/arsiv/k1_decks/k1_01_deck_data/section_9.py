#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 9: Genetik Tanı Yöntemleri ve Algoritmik Seçim (Adım 62 - 76 + Tekrar Sayfası)
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
            "slideNumber": 62,
            "title": "Multipl Konjenital Anomali ve Zihinsel Yetersizlikte Basamaklı Tanı Algoritması",
            "subtitle": "Klinik genetik kılavuzlarının (ACMG) önerdiği rasyonel test sıralaması",
            "badge": "Tanı Algoritması",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Açıklanamayan multipl konjenital anomalili (MKA) ve gelişimsel gecikmeli/otizmli bir hastada genetik test istemi rastgele yapılmaz; kılavuzların basamaklı algoritmaya uyulur:\n\n- **1. Basamak (Spesifik Sendrom Şüphesi Varsa):** Belirgin bir sendrom düşünülüyorsa hedefe yönelik test seçilir (Down için Karyotip; Williams/DiGeorge için FISH; Frajil X için triplet PCR).\n- **2. Basamak (Klinik Olarak Tanımlanamayan MKA/MR):** Spesifik bir klinik sendrom tanınamıyorsa **Kromozomal Mikrodizi (CMA / Array CGH)** birinci basamak altın standart testtir.\n- **3. Basamak (CMA Normal İse):** Submikroskobik kopya sayısı değişimi (CNV) saptanmayan olgularda **Yeni Nesil Dizileme (Hedefe yönelik gen paneli veya Tüm Ekzom Dizileme - WES)** uygulanır.\n- **4. Basamak:** Negatif WES olgularında Tüm Genom Dizileme (WGS), metilasyon analizleri veya fonksiyonel RNA çalışmaları devreye girer.",
            "coreContent": {
                "table": {
                    "title": "MKA ve Gelişimsel Gerilikte Basamaklı Tanı Protokolü",
                    "headers": ["Basamak", "Klinik Durum", "Önerilen Altın Standart Test"],
                    "rows": [
                        ["1. Basamak", "Spesifik sendrom şüphesi (Down, Turner, Williams)", "Karyotip, FISH veya hedefe yönelik PCR"],
                        ["2. Basamak", "Klinik olarak tanımlanamayan çoklu anomali / zeka geriliği", "Kromozomal Mikrodizi (CMA / Array CGH)"],
                        ["3. Basamak", "CMA normal; monogenik sendrom şüphesi", "Hedefe Yönelik NGS Paneli veya Trio-WES"],
                        ["4. Basamak", "WES normal; nadir non-kodlayan mutasyon şüphesi", "Tüm Genom Dizileme (WGS) & Epigenomik"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "MKA/MR Tanı Algoritması", "explanation": "Çoklu doğumsal anomali ve zeka geriliğinde CMA ve WES basamaklarını izleyen uluslararası klinik yol haritası."},
                {"term": "Tüm Ekzom Dizileme (WES)", "explanation": "İnsan genomundaki yaklaşık 20.000 genin tüm protein kodlayan bölgelerini (ekzonları) eş zamanlı okuyan moleküler yöntem."}
            ],
            "spotPearls": [
                "Tanımlanamayan multipl konjenital anomali, zihinsel yetersizlik ve otizm spektrumunda birinci basamak genetik test Kromozomal Mikrodizidir (CMA)."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Dismorfik Çocukta Genetik Tanı Basamakları",
                    [
                        "1. Adım: Dismorfik muayene ve spesifik sendrom ipucu araştırması.",
                        "2. Adım: Belirgin fenotip yoksa 1. basamak test olarak Kromozomal Mikrodizi (CMA) uygulanması.",
                        "3. Adım: CMA normal ise tek nükleotid mutasyonları için Trio-WES (Ekzom Dizileme).",
                        "4. Adım: İleri analizlerde negatifse WGS ve fonksiyonel transkriptomik testler."
                    ]
                ),
                make_micro_quiz(
                    "Fenotipik olarak belirli bir sendroma uydurulamayan, çoklu konjenital anomalili ve zihinsel yetersizlikli bir çocukta uluslararası kılavuzlarca önerilen İLK BASAMAK genetik tetkik hangisidir?",
                    {
                        "A": "Kromozomal Mikrodizi (CMA / Array CGH)",
                        "B": "Tüm Genom Dizileme (WGS)",
                        "C": "Sanger Dizileme",
                        "D": "Konvansiyonel Bantlama Karyotip"
                    },
                    "A",
                    {
                        "A": "Doğru! ACMG kılavuzlarına göre tanımlanamayan MKA ve otizm/zeka geriliğinde birinci basamak tetkik Kromozomal Mikrodizidir (CMA).",
                        "B": "Yanlış. WGS son basamak ileri moleküler tetkiktir.",
                        "C": "Yanlış. Sanger tek gen bilindiğinde kullanılır, tüm genomu tarayamaz.",
                        "D": "Yanlış. Karyotip sadece aşikar aneuploidi şüphesinde ilk basamaktır, mikrodelesyonları göremez."
                    }
                )
            ]
        },
        {
            "slideNumber": 63,
            "title": "Konvansiyonel Sitogenetik (G-Bantlama Karyotip): 4-5 Mb Sınırı ve Endikasyonlar",
            "subtitle": "Metafaz kromozomlarının ışık mikroskobu altında doğrudan morfolojik analizi",
            "badge": "Laboratuvar",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "G-bantlama karyotip analizi, 1970'lerden bu yana tıbbi genetiğin temel taşı olmaya devam eden klasik sitogenetik tanı yöntemidir:\n\n- **Teknik ve Çözünürlük:** Periferik kandan lenfositler fitohemaglütinin ile kültüre edilir, kolşisinle metafazda durdurulur ve Giemsa ile boyanır. Standart bir rutin karyotipin çözünürlüğü yaklaşık **4-5 megabaz (Mb)** ve üzerindedir (400-550 bant düzeyi).\n- **Temel Endikasyonlar:**\n  - Aşikar aneuploidi şüphesi (Down, Edwards, Patau, Turner, Klinefelter sendromları).\n  - Tekrarlayan gebelik kaybı ve infertilite araştırması (ebeveynlerde dengeli resiprokal veya Robertsonian translokasyon taraması).\n  - Cinsel gelişim bozuklukları (46,XX / 46,XY ayrımı).\n  - Hematolojik maligniteler (lösemilerdeki translokasyonlar).",
            "coreContent": {
                "table": {
                    "title": "G-Bantlama Karyotip Özellikleri",
                    "headers": ["Parametre", "Değer / Durum", "Klinik Yorum"],
                    "rows": [
                        ["Çözünürlük Sınırı", "4 - 5 Megabaz (Mb)", "5 Mb altındaki delesyonlar normal görünür"],
                        ["Hücre Döngüsü Evresi", "Metafaz", "Canlı bölünen hücre kültürü şarttır"],
                        ["Bant Sayısı", "400 - 550 bant", "Yüksek çözünürlüklü bantlamada 850 bant"],
                        ["En Güçlü Olduğu Alan", "Dengeli translokasyon ve inversiyonlar", "Mikrodizinin göremediği yapısal kırıkları yakalar"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "G-Bantlama Karyotip", "explanation": "Tripsin ve Giemsa ile metafaz kromozomlarında açık ve koyu bantlar oluşturarak mikroskopta inceleme yöntemi."},
                {"term": "4-5 Mb Çözünürlük Sınırı", "explanation": "Işık mikroskobunda gözle görülebilen en küçük kromozomal parça kaybı veya fazlalığı boyutu."}
            ],
            "spotPearls": [
                "Konvansiyonel karyotip analizinin çözünürlük sınırı 4-5 Mb'tır; bu boyutun altındaki mikrodelesyon sendromları karyotipte görülemez, normal raporlanır."
            ],
            "interactiveElements": [
                make_cloze(
                    "Standart G-bantlama konvansiyonel karyotip analizinin çözünürlük sınırı yaklaşık [4-5 Mb] düzeyindedir.",
                    "4-5 Mb",
                    "Megabaz cinsinden mikroskobik çözünürlük",
                    "4-5 megabazın altındaki kromozomal parça kayıpları mikroskopta görülemez ve normal kabul edilir."
                ),
                make_micro_quiz(
                    "Aşağıdaki klinik tablolardan hangisinde konvansiyonel G-bantlama karyotip analizi İLK TERCİH edilecek testtir?",
                    {
                        "A": "Açıklanamayan hafif zihinsel yetersizlik",
                        "B": "Tekrarlayan düşük öyküsü olan çiftlerde dengeli translokasyon araştırması",
                        "C": "Williams sendromu şüphesi (7q11.23 delesyonu)",
                        "D": "Kistik fibrozis mutasyon taraması"
                    },
                    "B",
                    {
                        "A": "Yanlış. Açıklanamayan zeka geriliğinde ilk basamak mikrodizidir (CMA).",
                        "B": "Doğru! Ebeveynlerde dengeli resiprokal veya Robertsonian translokasyonlar DNA miktarı değişmediği için yalnızca karyotipte saptanabilir.",
                        "C": "Yanlış. Williams 1.5 Mb'lık mikrodelesyondur, FISH veya CMA gerekir.",
                        "D": "Yanlış. CFTR gen mutasyonu tek gendir, dizi analizi gerekir."
                    }
                )
            ]
        },
        {
            "slideNumber": 64,
            "title": "Karyotipin Teknik Kısıtlılıkları: Metafaz Zorunluluğu ve Uzun Kültür Süresi",
            "subtitle": "Canlı hücre kültürü gereksinimi ve acil durumlarda sitogenetiğin zaman kaybı",
            "badge": "Laboratuvar Kısıtı",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Karyotip analizinin altın standart olmasına rağmen pratik klinikte önemli kısıtlılıkları vardır:\n\n- **Canlı Hücre Kültürü Şartı:** Karyotip için hücrelerin fitohemaglütinin (PHA) ile uyarılıp mitoza girmesi şarttır. Ölü dokudan, fikse preparatlardan veya pıhtılaşmış kandan karyotip çalışılamaz.\n- **Sonuçlanma Süresi (10-21 Gün):** Lenfosit kültürünün üremesi, metafaz plağı hazırlanması ve mikroskop altında tek tek 20-30 metafazın sayılması haftalar sürer. Yenidoğan yoğun bakımında kritik saatler yaşayan konjenital anomalili bir bebek için bu süre çok uzundur.\n- **Düşük Mozaiklikleri Atlama Riski:** Rutinde 20 metafaz incelenir; bu da %10'un altındaki mozaik klonların gözden kaçmasına yol açabilir.",
            "medicalTerms": [
                {"term": "Fitohemaglütinin (PHA)", "explanation": "T lenfositlerini mitoza girmeye zorlayan mitojenik bir lektin bileşiği."},
                {"term": "Metafaz Plağı", "explanation": "Kromozomların en yoğun ve mikroskopta sayılabilir hale geldiği mitoz evresindeki yayma görüntüsü."}
            ],
            "spotPearls": [
                "Karyotip analizi canlı bölünen hücre gerektirir ve sonuçlanması 2-3 hafta sürer; acil yenidoğan tanısında bu yüzden interfaz FISH tercih edilir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Karyotip vs Hızlı Tanı İhtiyacı",
                    "Konvansiyonel Karyotip",
                    "Acil İnterfaz FISH / QF-PCR",
                    [
                        "Canlı hücre kültürü zorunludur (hücreler mitoza sokulur)",
                        "Sonuçlanması ortalama 10-21 gün sürer",
                        "Metafaz kromozomları tek tek mikroskopta sayılır",
                        "Ölü fötus dokusunda kültür başarısız olabilir"
                    ],
                    [
                        "Kültür gerektirmez; bölünmeyen çekirdeklerde çalışır",
                        "Sonuç 24 - 48 saat içinde hızla elde edilir",
                        "Floresan sinyaller doğrudan interfaz çekirdeğinde sayılır",
                        "Yenidoğan yoğun bakımında hayat kurtarıcı hız sağlar"
                    ]
                )
            ]
        },
        {
            "slideNumber": 65,
            "title": "Floresan İn Situ Hibridizasyon (FISH): Bilinen Lokuslara Özgü Hızlı Mikrodelesyon Testi",
            "subtitle": "Spesifik DNA problarının floresan ışımasıyla hedefe kilitlenen moleküler sitogenetik",
            "badge": "Laboratuvar",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Floresan İn Situ Hibridizasyon (FISH); mikroskopta incelenen hücrelerin içine floresan boyalarla etiketlenmiş hedefe özgü DNA problarının salınması ve komplementer bölgeye bağlanması (hibridizasyon) prensibine dayanır:\n\n- **Yüksek Çözünürlük (100-200 kb):** Standart karyotipin 4-5 Mb olan sınırını aşarak 100 kilobazlık submikroskobik delesyonları doğrudan floresan mikroskobunda gösterir.\n- **Avantajı (Hız ve Metafaz Dışı İnceleme):** Hücre kültürüne gerek kalmadan bölünmeyen interfaz çekirdeklerinde bile 24-48 saat içinde sonuç verir (özellikle yenidoğan yoğun bakımında hızlı trizomi ve DiGeorge tanısı için hayatidir).\n- **Sınırı (Kör Tarama Yapamaz):** FISH testi 'hedefe yöneliktir'; yani hekim ne aradığını önceden bilmek zorundadır (örneğin Williams şüphesi varsa ELN probu, DiGeorge şüphesi varsa 22q11.2 probu istenir). Bilinmeyen bir sendromu tüm genomda tarayamaz.",
            "coreContent": {
                "table": {
                    "title": "FISH Yöntemi Özellikleri ve Uygulamaları",
                    "headers": ["Özellik", "FISH Metodu", "Klinik Avantajı"],
                    "rows": [
                        ["Çözünürlük", "100 - 200 Kilobaz (kb)", "Submikroskobik mikrodelesyonları gösterir"],
                        ["Süre", "24 - 48 saat", "Acil yoğun bakım kararlarını hızlandırır"],
                        ["Kültür Şartı", "Yok (İnterfazda çalışabilir)", "Bölünmeyen hücrelerde de uygulanabilir"],
                        ["Kısıtlılık", "Yalnızca hedeflenen lokusu gösterir", "Tüm genomu tarayamaz"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "FISH (Floresan İn Situ Hibridizasyon)", "explanation": "Hedef DNA bölgesine bağlanan floresan işaretli problarla spesifik mikrodelesyonları gösteren yöntem."},
                {"term": "Hedefe Yönelik Prob", "explanation": "Yalnızca araştırılmak istenen spesifik gen bölgesine (örneğin 22q11.2) bağlanan etiketli DNA dizisi."}
            ],
            "spotPearls": [
                "FISH hedefe yönelik bir testtir; tüm genomu tarayamaz, hekimin önceden şüphelendiği spesifik mikrodelesyon bölgesini (Williams, DiGeorge vb.) doğrulamak için kullanılır."
            ],
            "interactiveElements": [
                make_cloze(
                    "FISH yöntemi hücre kültürüne gerek duymaksızın bölünmeyen [İnterfaz] çekirdeklerinde 24-48 saatte hızlı trizomi ve delesyon tanısı koyabilir.",
                    "İnterfaz",
                    "Mitoz öncesi bölünmeyen çekirdek evresi",
                    "İnterfaz FISH acil yenidoğan tanısında kültür beklemeden floresan sinyalleri saymayı sağlar."
                ),
                make_micro_quiz(
                    "Aşağıdakilerden hangisi Floresan İn Situ Hibridizasyon (FISH) yönteminin en önemli teknik kısıtlılığıdır?",
                    {
                        "A": "Sonuçlanmasının 4 haftadan uzun sürmesi",
                        "B": "Sadece hekimin önceden belirlediği spesifik gen bölgesini inceleyebilmesi, tüm genomu tarayamaması",
                        "C": "Kromozom trizomilerini kesinlikle gösterememesi",
                        "D": "Yalnızca canlı bölünen metafaz hücrelerinde çalışabilmesi"
                    },
                    "B",
                    {
                        "A": "Yanlış. FISH çok hızlıdır (24-48 saat).",
                        "B": "Doğru! FISH hedefe yöneliktir; hekim hangi probu isterse sadece o lokusu görür, bilinmeyen sendromlarda tüm genomu tarayamaz.",
                        "C": "Yanlış. Trizomi 13, 18, 21 için özgül problarla trizomiyi hızla gösterir.",
                        "D": "Yanlış. İnterfaz çekirdeklerinde de mükemmel çalışır."
                    }
                )
            ]
        },
        {
            "slideNumber": 66,
            "title": "Kromozomal Mikrodizi (CMA / Array CGH): Birinci Basamak Genetik Test Olarak Üstünlüğü",
            "subtitle": "Tüm genomdaki submikroskobik kopya sayısı değişimlerini (CNV) eş zamanlı tarayan teknoloji",
            "badge": "Altın Standart",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Kromozomal Mikrodizi (Chromosomal Microarray - CMA / Array CGH); hastanın genomik DNA'sı ile referans normal insan DNA'sını farklı floresan renklerle etiketleyip mikrodizi çipi üzerinde yüz binlerce oligonükleotid proba karşı yarıştıran devrim niteliğinde bir yöntemdir:\n\n- **Birinci Basamak Test Statüsü:** Tanımlanamayan multipl konjenital anomali (MKA), zihinsel gerilik ve otizm spektrum bozukluğunda **BİRİNCİ BASAMAK TANI TESTİDİR**.\n- **Çözünürlük Gücü (20-50 kb):** Karyotipe göre yaklaşık 100 kat daha yüksek çözünürlüktedir. Işık mikroskobunda görülemeyen tüm mikrodelesyon ve mikroduplikasyonları (CNV) tek bir seansta tüm kromozomlarda tarar.\n- **Tanı Verimliliği:** Karyotipi normal çıkan dismorfik çocukların yaklaşık **%15-20'sinde** patojenik bir CNV yakalayarak kesin tanı koyar.",
            "coreContent": {
                "table": {
                    "title": "Kromozomal Mikrodizi (CMA) ve Karyotip Karşılaştırması",
                    "headers": ["Özellik", "Karyotip (G-Bantlama)", "Kromozomal Mikrodizi (CMA)"],
                    "rows": [
                        ["Çözünürlük", "4 - 5 Megabaz (Mb)", "20 - 50 Kilobaz (kb) (100 kat üstün)"],
                        ["İnceleme Alanı", "Mikroskopta görünen büyük bantlar", "Tüm genomdaki yüz binlerce oligonükleotid prob"],
                        ["MKA/MR Tanı Verimi", "%3 - 5", "%15 - 20 ek tanı verimi"],
                        ["Dengeli Translokasyon Tespiti", "EVET (Mükemmel görür)", "HAYIR (DNA miktarı değişmediği için KÖRDÜR)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Kromozomal Mikrodizi (CMA)", "explanation": "Tüm kromozomlardaki submikroskobik kopya sayısı kazanım ve kayıplarını tarayan mikrodizi yöntemi."},
                {"term": "Tanı Verimi (Diagnostic Yield)", "explanation": "Birinci basamak test olarak CMA'nın karyotip-negatif olgularda sağladığı %15-20 ek tanı başarısı."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Açıklanamayan zihinsel yetersizlik, otizm ve çoklu doğumsal anomalide uluslararası kılavuzlarca önerilen BİRİNCİ BASAMAK genetik test Kromozomal Mikrodizidir (CMA / Array CGH)."
            ],
            "interactiveElements": [
                make_cloze(
                    "Açıklanamayan zihinsel yetersizlik ve multipl konjenital anomalili çocuklarda kılavuzların önerdiği birinci basamak tanı testi [Kromozomal Mikrodizi] (CMA / Array CGH) analizidir.",
                    "Kromozomal Mikrodizi",
                    "Array CGH olarak da bilinen genomik mikrodizi testi",
                    "CMA, klasik karyotipin çözünürlüğünü 100 kat aşarak tüm genomdaki mikrodelesyon ve mikroduplikasyonları saptayan birinci basamak testtir."
                ),
                make_micro_quiz(
                    "Kromozomal mikrodizi (CMA) testi, karyotipi normal çıkan dismorfik ve gelişimsel gecikmeli çocukların yaklaşık yüzde kaçında ek patojenik kopya sayısı değişimi (CNV) saptar?",
                    {
                        "A": "%15 - 20",
                        "B": "%0.1",
                        "C": "%85 - 90",
                        "D": "%50 - 60"
                    },
                    "A",
                    {
                        "A": "Doğru! CMA, karyotip-negatif dismorfik çocukların %15-20'sinde mikrodelesyon/duplikasyon yakalayarak tanı koyar.",
                        "B": "Yanlış. %0.1 çok düşüktür; CMA'nın tanı verimi yüksektir.",
                        "C": "Yanlış. %85-90 WES'in dahi üzerinde abartılı bir orandır.",
                        "D": "Yanlış. CMA için literatürde kabul edilen tanı verimi %15-20'dir."
                    }
                )
            ]
        },
        {
            "slideNumber": 67,
            "title": "CMA'nın Teknik Sınırları: Dengeli Translokasyonları ve İnversiyonları Yakalayamaması",
            "subtitle": "Kopya sayısı değişmediğinde mikrodizinin kör kaldığı durumlar",
            "badge": "Teknik Kısıtlılık",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Kromozomal Mikrodizi (CMA) olağanüstü çözünürlüğüne rağmen her şeyi gösteremez. CMA'nın yapamadığı durumlar tıp fakültesi kurullarının ve TUS'un en sevdiği tuzak sorularındandır:\n\n- **1. Dengeli Yapısal Değişimleri GÖREMEZ:** CMA yalnızca DNA miktarı artışını (duplikasyon) veya azalışını (delesyon) ölçer. Dengeli resiprokal translokasyonlarda veya inversiyonlarda net DNA kaybı ya da kazancı OLMADIĞI için CMA sonucu **TAMAMEN NORMAL** çıkar!\n- **2. Tek Nükleotid Mutasyonlarını GÖREMEZ:** Akondroplazi veya Kistik Fibrozis gibi tek bir baz değişimine (nokta mutasyonu) bağlı hastalıkları saptayamaz (dizileme gerekir).\n- **3. Düşük Düzeyli Mozaiklikleri Atlar:** Anormal hücre oranı %15-20'nin altındaysa mikrodizi sinyali arka planda kaybolur.\n- **Klinik Çıkarım:** Dengeli translokasyon ve inversiyon şüphesinde KARYOTİP; tek gen hastalığı şüphesinde NGS dizileme zorunludur.",
            "coreContent": {
                "table": {
                    "title": "CMA'nın Görebildiği ve Kesinlikle Göremediği Durumlar",
                    "headers": ["Genetik Bozukluk Tipi", "CMA Sonucu", "Uygun Tanı Testi"],
                    "rows": [
                        ["Mikrodelesyon / Mikroduplikasyon (CNV)", "SAPTAR (Mükemmel)", "Kromozomal Mikrodizi (CMA)"],
                        ["Dengeli Resiprokal Translokasyon", "KÖRDÜR (Normal çıkar!)", "G-Bantlama Karyotip"],
                        ["Dengeli Perisentrik / Parasentrik İnversiyon", "KÖRDÜR (Normal çıkar!)", "G-Bantlama Karyotip"],
                        ["Tek Nükleotid Nokta Mutasyonu", "KÖRDÜR (Normal çıkar!)", "Sanger / NGS Dizi Analizi"],
                        ["Triplet Tekrar Artışı (Frajil X)", "KÖRDÜR (Normal çıkar!)", "Triplet Repeat PCR / Southern Blot"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Dengeli Yeniden Düzenlenme Körlüğü", "explanation": "CMA'nın DNA miktarı değişmeyen translokasyon ve inversiyonları prensip gereği yakalayamaması."},
                {"term": "Kopya Sayısı Nötralitesi", "explanation": "İnversiyon veya dengeli translokasyonda genomik materyalin net miktar olarak korunduğu durum."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Kromozomal Mikrodizi (CMA / Array CGH) DENGELİ TRANSLOKASYONLARI ve İNVERSİYONLARI KESİNLİKLE GÖSTEREMEZ; çünkü net DNA kaybı veya kazancı yoktur!"
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Aşağıdaki kromozomal düzensizliklerden hangisi Kromozomal Mikrodizi (CMA / Array CGH) testi ile KESİNLİKLE SAPTANAMAZ?",
                    {
                        "A": "Dengeli resiprokal translokasyon",
                        "B": "22q11.2 mikrodelesyonu (DiGeorge sendromu)",
                        "C": "7q11.23 mikrodelesyonu (Williams sendromu)",
                        "D": "17p11.2 mikroduplikasyonu (Potocki-Lupski sendromu)"
                    },
                    "A",
                    {
                        "A": "Doğru! Dengeli translokasyonlarda net DNA miktarı kaybı veya kazancı olmadığı için CMA kördür; normal raporlanır.",
                        "B": "Yanlış. DiGeorge mikrodelesyonu bir kopya sayısı kaybıdır (CNV), CMA çok rahat saptar.",
                        "C": "Yanlış. Williams delesyonu CMA ile saptanır.",
                        "D": "Yanlış. Mikroduplikasyon bir kopya sayısı kazancıdır, CMA kolayca gösterir."
                    }
                ),
                make_active_recall(
                    "CMA Testinin 3 Büyük Sınırı",
                    "Kromozomal Mikrodizi (CMA) hangi 3 genetik tabloyu prensip gereği saptayamaz?",
                    "1) Dengeli translokasyon ve inversiyonlar (kopya sayısı nötrdür)\n2) Tek nükleotid nokta mutasyonları (sekanslama gerekir)\n3) Düşük düzeyli mozaiklikler (<%15-20)"
                )
            ]
        },
        {
            "slideNumber": 68,
            "title": "MLPA (Multiplex Ligation-dependent Probe Amplification) ve Subtelomerik Taramalar",
            "subtitle": "Kromozom uçlarındaki delesyonları ve spesifik gen kopya sayılarını hızlı tarama tekniği",
            "badge": "Moleküler Test",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "MLPA (Multiplex Ligation-dependent Probe Amplification); tek bir PCR reaksiyonu içinde 50-60 farklı spesifik DNA dizisinin kopya sayısını ölçebilen pratik bir moleküler yöntemdir:\n\n- **Subtelomerik Delesyonlar:** İdiyopatik zihinsel yetersizliği olan çocukların yaklaşık %5'inde kromozomların subtelomerik (uç) bölgelerinde mikrodelesyonlar bulunur. MLPA subtelomer kiti tüm kromozom uçlarını eş zamanlı tarar.\n- **Spesifik Gen Ekzon Delesyonları:** Duchenne Müsküler Distrofi (DMD geni) veya Spinal Müsküler Atrofi (SMN1 geni) gibi hastalıklarda ekzon delesyonlarını saptamada altın standarttır.\n- **Maliyet-Etkinlik:** CMA'ya göre çok daha ucuz ve hızlıdır; ancak yalnızca kitin içerdiği 50-60 probu ölçebilir, tüm genomu tarayamaz.",
            "coreContent": {
                "table": {
                    "title": "MLPA Yönteminin Temel Endikasyonları",
                    "headers": ["Uygulama Alanı", "Hedef Gen / Bölge", "Klinik Örnek"],
                    "rows": [
                        ["Subtelomerik Taramalar", "Tüm kromozomların p ve q telomer uçları", "Açıklanamayan zihinsel yetersizlik"],
                        ["Nöromüsküler Hastalıklar", "DMD ekzonları, SMN1/SMN2", "Duchenne Distrofi ve SMA tanısı"],
                        ["Tümör Baskılayıcı Genler", "BRCA1, BRCA2 delesyon/duplikasyonları", "Kalıtsal meme/over kanseri paneli"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "MLPA", "explanation": "Ligasyon temelli problarla onlarca gen bölgesinin kopya sayısını tek tüpte ölçen moleküler yöntem."},
                {"term": "Subtelomerik Yeniden Düzenlenme", "explanation": "Kromozomların uç bölgelerindeki mikrodelesyonların yol açtığı gelişimsel gerilik tablosu."}
            ],
            "spotPearls": [
                "MLPA, SMA'da SMN1 ekzon 7 delesyonunu ve Duchenne'de distrofin ekzon delesyonlarını saptamada en hızlı ve maliyet-etkin yöntemdir."
            ],
            "interactiveElements": [
                make_cloze(
                    "Kromozom uçlarındaki delesyonları ve DMD/SMN1 ekzon kayıplarını tek bir reaksiyonda ölçen moleküler teknik [MLPA] analizidir.",
                    "MLPA",
                    "Multiplex Ligation-dependent Probe Amplification",
                    "MLPA, ekzon düzeyinde kopya sayısı delesyon ve duplikasyonlarını saptayan yüksek verimli bir yöntemdir."
                )
            ]
        },
        {
            "slideNumber": 69,
            "title": "Yeni Nesil Dizileme (NGS): Hedefe Yönelik Gen Panelleri ve Monogenik Hastalıklar",
            "subtitle": "Milyonlarca DNA parçasının paralel okunmasıyla monogenik sendromların aydınlatılması",
            "badge": "Yeni Nesil Teknoloji",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Yeni Nesil Dizileme (Next Generation Sequencing - NGS); DNA parçalarını devasa paralel reaksiyonlarla eş zamanlı dizileyen yüksek verimli moleküler teknolojidir:\n\n- **Hedefe Yönelik Gen Panelleri:** Hastanın klinik tablosu belirli bir hastalık grubuna uyuyorsa (örneğin 'İskelet Displazisi Paneli', 'Kardiyomiyopati Paneli', 'Kraniyosinostoz Paneli'), o tabloyla ilişkili 50-200 gen aynı anda yüksek derinlikte (yüksek coverage) dizilenir.\n- **Klinik Avantaj:** Tek tek Sanger dizileme yapmaya kıyasla haftalar sürecek analizi birkaç güne indirir ve maliyeti dramatik biçimde düşürür.\n- **Tek Gen Mutasyonlarını Yakalama:** CMA'nın göremediği missense, nonsense, frameshift ve splice-site tek nükleotid patojenik varyantlarını eksiksiz ortaya çıkarır.",
            "coreContent": {
                "table": {
                    "title": "Hedefe Yönelik NGS Panelleri vs Genomik Dizileme",
                    "headers": ["Yöntem", "Taranan Gen Sayısı", "Dizileme Derinliği (Coverage)", "Klinik Kullanım"],
                    "rows": [
                        ["Hedefe Yönelik Panel", "50 - 250 gen", "Yüksek (>100x - 500x)", "Belirli klinik fenotip (örn: Noonan, Kraniyosinostoz)"],
                        ["Tüm Ekzom Dizileme (WES)", "~20.000 gen (ekzonlar)", "Orta (>50x - 100x)", "Tanımlanamayan nadir sendromlar"],
                        ["Tüm Genom Dizileme (WGS)", "Tüm genom (ekzon + intron)", "Standart (30x)", "Negatif WES olguları ve araştırma"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Hedefe Yönelik Gen Paneli (Targeted Panel)", "explanation": "Belirli bir klinik fenotiple ilişkili onlarca genin NGS teknolojisiyle eş zamanlı taranması."},
                {"term": "Dizileme Derinliği (Coverage)", "explanation": "Her bir bazın güvenilir varyant tespiti için kaç kez bağımsız olarak okunduğunu gösteren metrik."}
            ],
            "spotPearls": [
                "Klinik olarak belirli bir organ tutulumu olan monogenik hastalıklarda (örneğin osteogenezis imperfekta) hedefe yönelik NGS gen panelleri en hızlı ve ekonomik tanı aracıdır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Fenotipik olarak Noonan sendromu veya kraniyosinostoz gibi belirli bir klinik antitiden kuvvetle şüphelenilen bir hastada en akılcı ve maliyet-etkin moleküler test hangisidir?",
                    {
                        "A": "Hedefe yönelik NGS gen paneli",
                        "B": "Tüm Genom Dizileme (WGS)",
                        "C": "Konvansiyonel Karyotip",
                        "D": "Rutin İdrar Aminoasit Kromatografisi"
                    },
                    "A",
                    {
                        "A": "Doğru! Fenotip belirli bir sendromik grubu işaret ediyorsa, ilgili genleri yüksek derinlikte okuyan hedefe yönelik NGS paneli en akılcı yaklaşımdır.",
                        "B": "Yanlış. WGS gereksiz pahalıdır ve varyant yükü fazladır.",
                        "C": "Yanlış. Karyotip tek gen mutasyonlarını göremez.",
                        "D": "Yanlış. Metabolik taramadır, monogenik dismorfolojide hedefe yönelik test değildir."
                    }
                )
            ]
        },
        {
            "slideNumber": 70,
            "title": "Tüm Ekzom Dizileme (WES) ve Tüm Genom Dizileme (WGS): Klinik Uygulama Alanları",
            "subtitle": "Tanı konulamayan nadir sendromlarda protein kodlayan tüm ekzonların taranması",
            "badge": "İleri Genomik",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Karyotip ve Kromozomal Mikrodizi (CMA) normal çıktığı halde ağır dismorfik bulguları ve gelişimsel geriliği süren olgularda genetik tanının zirve noktası Ekzom ve Genom dizilemedir:\n\n- **Tüm Ekzom Dizileme (WES):** İnsan genomunun yalnızca %1-2'sini oluşturan ancak bilinen genetik hastalıkların %85'inden sorumlu olan protein kodlayan ekzon bölgelerinin (yaklaşık 20.000 gen, 180.000 ekzon) tamamını diziler.\n- **Trio WES (Anne-Baba-Çocuk Analizi):** Hastanın DNA'sı anne ve babanın DNA'sı ile eş zamanlı karşılaştırılır; bu sayede anne ve babada olmayıp çocukta yeni ortaya çıkan **de novo mutasyonlar** ve otozomal resesif bileşik heterozigot varyantlar hızla filtrelenir.\n- **Tüm Genom Dizileme (WGS):** Ekzonların yanı sıra intronik bölgeleri, promötörleri ve yapısal kırıkları da kapsayan en kapsamlı genomik analizdir.",
            "coreContent": {
                "table": {
                    "title": "WES ve WGS Karşılaştırmalı Analiz Matrisi",
                    "headers": ["Özellik", "Tüm Ekzom Dizileme (WES)", "Tüm Genom Dizileme (WGS)"],
                    "rows": [
                        ["Hedef Bölge", "Protein kodlayan ekzonlar (%1-2 genom)", "Tüm DNA dizisi (ekzon + intron + regülatör)"],
                        ["Kapsanan Hastalık Oranı", "Mendelyen hastalıkların %85'i", "Tüm genomik varyantlar"],
                        ["İntronik Varyantlar", "GÖREMEZ (sadece ekzon-intron sınırları)", "GÖRÜR (derin intronik mutasyonlar)"],
                        ["Kopya Sayısı Değişimi (CNV)", "Sınırlı (algoritmalara bağımlı)", "Mükemmel (yapısal kırıkları doğrudan okur)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Tüm Ekzom Dizileme (WES)", "explanation": "Genomdaki tüm protein kodlayan ekzonik bölgelerin dizilenmesi; nadir sendrom tanısında altın standarttır."},
                {"term": "Trio Analizi", "explanation": "Çocuk ve her iki ebeveynin DNA'sının paralel analiz edilerek de novo varyantların anında yakalanması yöntemi."}
            ],
            "spotPearls": [
                "CMA testi negatif çıkan açıklanamayan dismorfik çocuklarda Trio-WES (anne-baba-çocuk ekzom analizi) tanı koyma oranını %35-40'a ulaştırır."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tüm Ekzom Dizileme (WES) analizinde ebeveynlerin ve hastanın eş zamanlı dizilendiği 'Trio Analizi' yaklaşımının en büyük tanısal avantajı nedir?",
                    {
                        "A": "Sadece çocukta yeni ortaya çıkan (de novo) patojenik mutasyonları hızla filtreleyebilmesi",
                        "B": "Testin maliyetini sıfıra indirmesi",
                        "C": "Kromozomların mikroskopta sayılmasını sağlaması",
                        "D": "Dengeli translokasyonları karyotipten daha iyi göstermesi"
                    },
                    "A",
                    {
                        "A": "Doğru! Anne ve babada bulunmayıp sadece çocukta saptanan de novo varyantlar, on binlerce zararsız varyant arasından hızla elenerek tanıya ulaşmayı sağlar.",
                        "B": "Yanlış. Üç kişinin dizilenmesi maliyeti artırır ama tanı verimini fırlatır.",
                        "C": "Yanlış. WES dizilemedir, mikroskobik sayım yapmaz.",
                        "D": "Yanlış. WES dengeli translokasyonları göstermez."
                    }
                )
            ]
        },
        {
            "slideNumber": 71,
            "title": "WES'in Teknik Kısıtları: İntronlar, Triplet Tekrarları ve Devasa Varyant Yükü",
            "subtitle": "Karyotip ve CMA yapılmamış bir hastaya doğrudan WES istenmemesinin gerekçeleri",
            "badge": "Genomik Sınırlar",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Tüm Ekzom Dizileme (WES) olağanüstü bir güç sunsa da klinik genetikte her hastaya doğrudan WES istenemez:\n\n- **1. İntronik ve Regülatör Bölgeler:** Genomun %98'ini oluşturan kodlamayan bölgeleri ve promötör mutasyonlarını kapsamaz.\n- **2. Triplet Tekrar Artışları:** Frajil X veya Huntington gibi dinamik tekrar mutasyonlarını standart NGS/WES okuyamaz (kısa okuma kısıtlılığı).\n- **3. Büyük Kopya Sayısı Değişimleri (CNV):** Ekzom analizi büyük delesyon ve duplikasyonları her zaman güvenilir gösteremez (CMA bu konuda çok üstündür).\n- **4. Devasa Varyant Yükü ve VUS:** Her hastada 10.000-15.000 varyant çıkar; bunların klinik yorumu zordur ve hastaya anksiyete yaratan VUS (belirsiz varyant) riski taşır.",
            "coreContent": {
                "table": {
                    "title": "WES'in Göremediği Kritik Genetik Bozukluklar",
                    "headers": ["Genetik Tablo", "Neden WES Göremez?", "Gereken Doğru Test"],
                    "rows": [
                        ["Frajil X (CGG tekrarı)", "Kısa NGS okumaları triplet tekrarını dizileyemez", "Triplet Repeat PCR / Southern Blot"],
                        ["Büyük Mikrodelesyon (22q11.2)", "WES kopya sayısını güvenle sayamaz", "Kromozomal Mikrodizi (CMA)"],
                        ["Dengeli Translokasyon", "Kırık noktası introna denk gelir ve dizi normaldir", "G-Bantlama Karyotip"],
                        ["Derin İntronik Splice Mutasyonu", "WES sadece ekzonları yakalar", "Tüm Genom Dizileme (WGS)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Ekzonik Yakalama (Exome Capture)", "explanation": "DNA kütüphanesinden yalnızca kodlayan ekzon parçalarının problarla balık gibi tutulması yöntemi."},
                {"term": "Kısa Okuma Kısıtlılığı (Short-read Limitation)", "explanation": "150 bazlık kısa DNA parçalarının uzun triplet tekrar dizilerini kapsayamaması."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Karyotip ve Kromozomal Mikrodizi (CMA) yapılmamış bir hastaya doğrudan WES istenmesi kılavuzlarca önerilmez; çünkü WES büyük CNV'leri ve triplet tekrarlarını atlayabilir."
            ],
            "interactiveElements": [
                make_active_recall(
                    "WES Testinin 4 Temel Kısıtlılığı",
                    "Tüm Ekzom Dizileme (WES) analizinin klinikteki 4 temel sınırlılığı nelerdir?",
                    "1) İntronik ve promötör bölgeleri kapsamaz (%98 genom dışarıda kalır)\n2) Trinükleotid tekrar artışlarını (Frajil X vb.) okuyamaz\n3) Büyük delesyon/duplikasyonları (CNV) güvenilir yakalayamaz\n4) Hasta başına 10.000-15.000 varyant üretir ve VUS yükü çok yüksektir"
                )
            ]
        },
        {
            "slideNumber": 72,
            "title": "Bilgisayar Destekli Tanı Veritabanları: OMIM, POSSUM, London Dysmorphology ve DECIPHER",
            "subtitle": "Klinik genetikçinin sendromik ayırıcı tanıdaki küresel referans kütüphaneleri",
            "badge": "Veritabanları",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Tıpta tanımlanmış 10.000'den fazla genetik hastalık ve sendrom mevcuttur; hiçbir hekimin tüm bu varyasyonları hafızasında tutması mümkün değildir. Bu nedenle uluslararası bilgisayar veritabanları klinik pratiğin ayrılmaz parçasıdır:\n\n- **OMIM (Online Mendelian Inheritance in Man):** Tüm insan genlerinin, monogenik hastalıkların ve fenotiplerin küresel ana ansiklopedisidir (Dr. Victor McKusick mirası).\n- **POSSUM ve London Dysmorphology Database (LDDB):** Hastada saptanan dismorfik özelliklerin (örneğin hipertelorizm + yarık damak + sindaktili) sisteme girilmesiyle olası sendromların listelendiği görsel ve metrik dismorfoloji veritabanlarıdır.\n- **DECIPHER:** Kromozomal mikrodizi ile bulunan submikroskobik kopya sayısı değişimlerinin (CNV) patojenitesini ve dünyadaki benzer olguları haritalayan küresel veritabanıdır.\n- **Orphanet:** Nadir hastalıklar, yetim ilaçlar ve uzman merkezler portalıdır.",
            "coreContent": {
                "table": {
                    "title": "Klinik Genetik Veritabanları ve İşlevleri",
                    "headers": ["Veritabanı", "Odak Alanı", "Klinik Kullanım Amacı"],
                    "rows": [
                        ["OMIM", "Mendelyen genler ve monogenik hastalıklar", "Gen-hastalık ilişkisinin resmi kataloğu"],
                        ["POSSUM / LDDB", "Dismorfik bulgular ve sendrom fotoğrafları", "Fizik muayene bulgularıyla sendrom arama motoru"],
                        ["DECIPHER", "Submikroskobik mikrodelesyon ve CNV'ler", "CMA'da bulunan kopya sayısı değişiminin anlamlandırılması"],
                        ["Orphanet", "Nadir hastalıklar ve yetim ilaçlar", "Klinik kılavuzlar ve uzman merkez ağları"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "OMIM", "explanation": "İnsan genleri ve genetik hastalıklarının tüm dünyada kabul gören resmi çevrimiçi kataloğu."},
                {"term": "DECIPHER", "explanation": "Submikroskobik mikrodelesyon ve mikroduplikasyonların (CNV) klinik sonuçlarını paylaşan küresel veritabanı."}
            ],
            "spotPearls": [
                "OMIM tüm genetik hastalıkların resmi kataloğudur; POSSUM ve LDDB ise dismorfik bulgularla sendrom aramak için kullanılan özel fenotip veritabanlarıdır."
            ],
            "interactiveElements": [
                make_cloze(
                    "Kromozomal mikrodizi analizinde bulunan submikroskobik kopya sayısı değişimlerinin (CNV) patojenitesini ve dünya olgularını haritalayan küresel veritabanı [DECIPHER] portalıdır.",
                    "DECIPHER",
                    "Database of Chromosomal Imbalance and Phenotype in Humans",
                    "DECIPHER, mikrodelesyon ve mikroduplikasyonların fenotipik etkilerini haritalayan uluslararası havuzdur."
                )
            ]
        },
        {
            "slideNumber": 73,
            "title": "Genetik Varyantların Sınıflandırılması: Patojenik, Muhtemel Patojenik, VUS ve Benign",
            "subtitle": "ACMG/AMP kılavuzlarına göre moleküler DNA bulgularının klinik anlamı",
            "badge": "Varyant Yorumu",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Yeni Nesil Dizileme (WES/WGS) sonucunda her insanda yüz binlerce genetik varyant saptanır. Bu varyantların hangisinin hastalığa yol açtığı ACMG standartlarına göre 5 sınıfta değerlendirilir:\n\n- **Sınıf 5 - Patojenik:** Hastalık yaptığı kesin olarak kanıtlanmış varyanttır (literatürde doğrulanmış, fonksiyonel testle gösterilmiş).\n- **Sınıf 4 - Muhtemel Patojenik:** %90'ın üzerinde hastalık yapıcı olduğu düşünülen varyanttır; klinik kararlarda patojenik gibi yönetilir.\n- **Sınıf 3 - VUS (Belirsiz Anlamlı Varyant - Variant of Uncertain Significance):** Klinik genetiğin en büyük ikilemidir. Hastalık yapıp yapmadığına dair yeterli bilimsel kanıt yoktur; **VUS'a dayanarak ASLA gebelik sonlandırma veya radikal cerrahi karar alınamaz!**\n- **Sınıf 2 - Muhtemel Benign / Sınıf 1 - Benign:** Normal popülasyonda yaygın bulunan, hastalığa yol açmayan masum varyantlardır.",
            "coreContent": {
                "table": {
                    "title": "ACMG/AMP 5 Basamaklı Varyant Sınıflaması",
                    "headers": ["Sınıf", "Kategori", "Hastalık Yapma Olasılığı", "Klinik Yönetim"],
                    "rows": [
                        ["Sınıf 5", "Patojenik (Pathogenic)", ">%99 (Kesin)", "Tanı konur; aile taraması ve tedavi planlanır"],
                        ["Sınıf 4", "Muhtemel Patojenik", ">%90", "Patojenik gibi yönetilir; klinik uyum aranır"],
                        ["Sınıf 3", "VUS (Belirsiz Anlamlı)", "%10 - %90 (Belirsiz)", "ASLA gebelik sonlandırma veya radikal işlem yapılamaz!"],
                        ["Sınıf 2", "Muhtemel Benign", "<%10", "Zararsız kabul edilir; raporda arka plandadır"],
                        ["Sınıf 1", "Benign (Zararsız)", "<%1", "Normal popülasyon varyasyonudur; raporlanmaz"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "VUS (Belirsiz Anlamlı Varyant)", "explanation": "Hastalık yapma potansiyeli henüz kesinleşmemiş, klinik karar almada tek başına kullanılamayan varyant."},
                {"term": "ACMG Kılavuzu", "explanation": "Amerikan Tıbbi Genetik Koleji'nin DNA varyantlarını sınıflandırmak için belirlediği evrensel kanıt puanlama sistemi."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] VUS (Belirsiz Anlamlı Varyant) raporlandığında bu varyanta dayanılarak KESİNLİKLE gebelik terminasyonu veya radikal cerrahi karar alınamaz!"
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Prenatal genetik test sonucunda fetüste ACMG sınıflamasına göre 'VUS' (Variant of Uncertain Significance - Klinik Önemi Belirsiz Varyant) saptandığında hekimin yaklaşımı ne olmalıdır?",
                    {
                        "A": "VUS'a dayanılarak kesinlikle gebelik sonlandırma kararı verilmemeli; aileye varyantın hastalıkla nedenselliğinin kanıtlanmadığı anlatılmalıdır",
                        "B": "Derhal gebelik termine edilmelidir",
                        "C": "Varyant patojenik kabul edilerek kesin malformasyon gelişeceği söylenmelidir",
                        "D": "Tüm diğer ultrasonografi ve klinik takipler sonlandırılmalıdır"
                    },
                    "A",
                    {
                        "A": "Doğru! VUS hastalık yapıp yapmadığı kanıtlanmamış varyanttır; tek başına radikal cerrahi veya gebelik sonlandırma kararı için KESİNLİKLE kullanılamaz.",
                        "B": "Yanlış. VUS nedeniyle sağlıklı bir fetüsün sonlandırılması büyük bir tıbbi hatadır.",
                        "C": "Yanlış. VUS patojenik değildir.",
                        "D": "Yanlış. Tam tersine klinik takip ve ultrason sürdürülmelidir."
                    }
                )
            ]
        },
        {
            "slideNumber": 74,
            "title": "Genetik Testlerin Çözünürlük Hiyerarşisi: Megabazdan Tek Nükleotide",
            "subtitle": "Karyotip, FISH, CMA ve NGS yöntemlerinin boyut skalasındaki kesin yerleri",
            "badge": "Çözünürlük Skalası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Genetik tanı testlerinin doğru seçilmesi, araştırılan defektin genomik boyutu ile testin çözünürlük gücünün örtüşmesine bağlıdır:\n\n- **Karyotip (G-Bantlama):** >= 4-5 Megabaz (Mb) = >= 4.000.000 - 5.000.000 baz çifti. Yalnızca mikroskopta görünen devasa anormallikleri saptar.\n- **FISH:** 100 - 200 Kilobaz (kb) = 100.000 - 200.000 baz çifti. Bilinen hedef lokustaki mikrodelesyonları yakalar.\n- **Kromozomal Mikrodizi (CMA):** 20 - 50 Kilobaz (kb) = 20.000 - 50.000 baz çifti. Tüm genomda mikrodelesyon ve mikroduplikasyonları yakalar.\n- **MLPA:** 50 - 100 baz çifti düzeyindeki ekzon delesyonlarını gösterir.\n- **NGS / Sanger:** 1 Tek Nükleotid Baz Çifti (bp). Nokta mutasyonlarını, çerçeve kaymalarını ve küçük insersiyon/delesyonları (indel) ortaya çıkarır.",
            "coreContent": {
                "table": {
                    "title": "Genetik Yöntemlerin Çözünürlük Hiyerarşisi",
                    "headers": ["Yöntem", "Çözünürlük Boyutu", "Büyüklük Mertebesi", "Hedef Defekt"],
                    "rows": [
                        ["Karyotip", "4 - 5 Mb", "Milyonlarca baz", "Aneuploidi, büyük translokasyon"],
                        ["FISH", "100 - 200 kb", "Yüz binlerce baz", "Hedefe özgü mikrodelesyon"],
                        ["Kromozomal Mikrodizi (CMA)", "20 - 50 kb", "On binlerce baz", "Genom boyu tüm CNV'ler"],
                        ["MLPA", "50 - 100 bp", "Ekzon düzeyi", "Ekzon delesyon/duplikasyonu"],
                        ["Sanger / NGS", "1 bp", "Tek baz çifti", "Nokta mutasyonları (missense, nonsense)"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Megabaz (Mb)", "explanation": "Bir milyon nükleotid baz çiftine eşit genomik uzunluk birimi."},
                {"term": "Kilobaz (kb)", "explanation": "Bin nükleotid baz çiftine eşit genomik uzunluk birimi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Çözünürlük sıralaması (büyükten küçüğe tespit gücü): Karyotip (Mb) -> FISH (yüzler kb) -> CMA (onlar kb) -> MLPA (ekzon) -> NGS (tek baz)."
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Genomik Çözünürlük Merdiveni (Kaba Yapıdan Tek Baza)",
                    [
                        "1. Karyotip: 4-5 Mb (Milyonlarca bazlık kromozom anomalileri)",
                        "2. FISH: 100-200 kb (Yüz binlerce bazlık hedef lokuslar)",
                        "3. CMA (Mikrodizi): 20-50 kb (On binlerce bazlık tüm genom mikrodelesyonları)",
                        "4. MLPA: 50-100 bp (Tek tek ekzon delesyonları)",
                        "5. NGS / Sanger: 1 bp (Tek nükleotid nokta mutasyonları)"
                    ]
                )
            ]
        },
        {
            "slideNumber": 75,
            "title": "Genetik Test Seçim Matrisi: Hangi Klinik Tabloda Hangi Test İstenmelidir?",
            "subtitle": "Dismorfolojide maliyet-etkin ve doğru tanıya götüren klinik test seçim kılavuzu",
            "badge": "Özet Kılavuz",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Hangi klinik tabloda hangi genetik testin ilk basamak olarak seçileceğinin özeti:\n\n- **Klasik Aneuploidi Şüphesi (Down, Turner, Klinefelter):** Konvansiyonel G-bantlama Karyotip (veya acil interfaz FISH).\n- **Spesifik Mikrodelesyon Şüphesi (Williams, DiGeorge):** Hedefe yönelik FISH veya Kromozomal Mikrodizi (CMA).\n- **Açıklanamayan Zihinsel Yetersizlik, Otizm veya Multipl Anomali:** Kromozomal Mikrodizi (CMA / Array CGH) - Birinci basamak altın standart.\n- **Spesifik Monogenik Hastalık Şüphesi (Akondroplazi, Marfan):** İlgili gene yönelik Sanger dizileme veya hedefe yönelik NGS gen paneli.\n- **Tanımlanamayan Nadir Sendromlar (CMA Negatif Olgular):** Tüm Ekzom Dizileme (Trio-WES).\n- **Dengeli Translokasyon / İnversiyon Şüphesi (Tekrarlayan Düşükler):** Ebeveynlerde Konvansiyonel Karyotip analizi (CMA göremez!).",
            "coreContent": {
                "table": {
                    "title": "Klinik Endikasyon - Altın Standart Genetik Test Matrisi",
                    "headers": ["Klinik Başvuru Tablosu", "Öncelikli Test", "Gerekçe / Püf Noktası"],
                    "rows": [
                        ["Tipik Down Sendromu bulguları", "G-Bantlama Karyotip", "Trizomi tipini (serbest vs translokasyon) ayırır"],
                        ["Açıklanamayan zeka geriliği + çoklu minör anomali", "Kromozomal Mikrodizi (CMA)", "Kılavuzların önerdiği 1. basamak altın standart"],
                        ["Tekrarlayan gebelik kaybı olan çiftler", "Ebeveyn Karyotip Analizi", "Dengeli translokasyonu sadece karyotip yakalar"],
                        ["Spesifik DiGeorge şüphesi (kalp + hipokalsemi)", "FISH (22q11.2) veya CMA", "Hızlı ve hedefe yönelik mikrodelesyon tespiti"],
                        ["Karyotip ve CMA normal çıkan ağır dismorfik çocuk", "Trio-WES (Ekzom Dizileme)", "Tüm kodlayan ekzonlarda de novo mutasyon arar"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Genetik Test Seçim Matrisi", "explanation": "Klinik ön tanıya göre en hızlı ve maliyet-etkin genetik testi belirleyen uygulama haritası."},
                {"term": "Hedefe Yönelik Genetik Tanı", "explanation": "Fenotipik ipuçlarına göre en dar ve özgül test basamağını seçerek kaynak israfını önleme yaklaşımı."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Tekrarlayan düşük yapan çiftlerde dengeli translokasyon taraması için KARYOTİP; açıklanamayan zeka geriliği ve çoklu anomalide ise MİKRODİZİ (CMA) istenir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tekrarlayan ilk trimester gebelik kayıpları nedeniyle başvuran sağlıklı genç bir çiftte ebeveynlerde dengeli resiprokal veya Robertsonian translokasyon araştırmak için hangi test istenmelidir?",
                    {
                        "A": "Periferik kandan G-bantlama konvansiyonel Karyotip analizi",
                        "B": "Kromozomal Mikrodizi (CMA / Array CGH)",
                        "C": "Tüm Ekzom Dizileme (WES)",
                        "D": "MLPA subtelomer kiti"
                    },
                    "A",
                    {
                        "A": "Doğru! Dengeli translokasyonlarda DNA miktarı değişmediği için mikrodizi veya ekzom dizileme kördür; yalnızca mikroskop altında karyotip analizi ile saptanabilir.",
                        "B": "Yanlış. CMA dengeli translokasyonları kesinlikle göremez, normal raporlar!",
                        "C": "Yanlış. WES translokasyon kırık noktalarını yakalayamaz.",
                        "D": "Yanlış. MLPA sadece subtelomerik CNV'leri ölçer."
                    }
                )
            ]
        },
        {
            "slideNumber": 76,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Genetik Tanı Yöntemleri ve Çözünürlük Ezber Matrisi",
            "subtitle": "Karyotip, FISH, CMA ve NGS testlerinin güçleri ve sınırları kilit tablosu",
            "badge": "Hafıza Matrisi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu kontrol noktası; tıp fakültesi kurullarında ve uzmanlık sınavlarında en çok karıştırılan 'hangi yöntem neyi görür, neyi göremez' kurallarını tek bir interaktif ezber tablosunda pekiştirmenizi sağlar.\n\nMaskeli hücrelere tıklayarak gizlenen tanı yöntemlerini, çözünürlük sınırlarını ve kritik klinik endikasyonları hafızanızdan geri çağırın!",
            "coreContent": {
                "table": {
                    "title": "Genetik Tanı Yöntemleri Karşılaştırma Matrisi",
                    "headers": ["Yöntem", "Çözünürlük", "Temel Gücü", "Kritik Kör Noktası"],
                    "rows": [
                        ["Karyotip", "4 - 5 Mb", "Dengeli translokasyon / inversiyon", "4 Mb altı mikrodelesyonları göremez"],
                        ["FISH", "100 - 200 kb", "Hedef mikrodelesyon ve hızlı interfaz", "Tüm genomu tarayamaz (kör tarama yapamaz)"],
                        ["CMA (Array CGH)", "20 - 50 kb", "Tüm genom mikrodelesyon/duplikasyon (1. basamak)", "Dengeli translokasyonları ve nokta mutasyonları göremez"],
                        ["Trio-WES", "1 bp (ekzonlar)", "Nadir monogenik de novo varyantlar", "Büyük CNV'leri ve triplet tekrarları atlayabilir"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Hafıza Matrisi", "explanation": "Klinik genetik tanı yöntemlerinin endikasyon ve çözünürlük parametrelerini sentezleyen ezber tablosu."},
                {"term": "Aktif Geri Çağırma (Active Recall)", "explanation": "Gizlenmiş bilgiyi zihinden çekerek uzun süreli hafızaya kodlama tekniği."}
            ],
            "spotPearls": [
                "🚨 [KRİTİK UYARI] Sınavda en sık sorulan ikilem: CMA dengeli translokasyonu göremez; Karyotip mikrodelesyonu göremez; WES triplet tekrarını göremez!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Genetik Tanı Yöntemleri Kilit Ezber Tablosu",
                    ["Tanı Yöntemi", "Çözünürlük Gücü", "En Güçlü Endikasyonu", "En Kritik Kör Noktası"],
                    [
                        [
                            ("G-Bantlama Karyotip", False),
                            ("4-5 Mb", True, "Mb"),
                            ("Dengeli translokasyon taraması", True, "Dengeli translokasyon"),
                            ("Mikrodelesyonları göremez", False)
                        ],
                        [
                            ("Floresan İn Situ Hibridizasyon (FISH)", False),
                            ("100-200 kb", True, "kb"),
                            ("Hedefe yönelik mikrodelesyon & hızlı interfaz", True, "Hızlı interfaz"),
                            ("Tüm genomu tarayamaz", False)
                        ],
                        [
                            ("Kromozomal Mikrodizi (CMA)", False),
                            ("20-50 kb", True, "kb"),
                            ("Açıklanamayan MKA/MR'de 1. basamak", True, "1. basamak altın standart"),
                            ("Dengeli translokasyon ve inversiyonları göremez", True, "Dengeli translokasyonu göremez")
                        ],
                        [
                            ("Tüm Ekzom Dizileme (Trio-WES)", False),
                            ("1 bp (kodlayan ekzonlar)", True, "1 baz çifti"),
                            ("CMA-negatif açıklanamayan nadir sendromlar", True, "De novo varyantlar"),
                            ("Triplet tekrar artışlarını ve derin intronları göremez", True, "Triplet tekrarları göremez")
                        ]
                    ]
                ),
                make_micro_quiz(
                    "Multipl konjenital anomali ve zeka geriliği olan bir hastada sırasıyla hangi iki test basamaklı olarak istenmelidir?",
                    {
                        "A": "Önce Kromozomal Mikrodizi (CMA) -> Normal çıkarsa Trio-WES",
                        "B": "Önce Sanger Dizileme -> Normal çıkarsa Karyotip",
                        "C": "Önce FISH -> Normal çıkarsa İdrar aminoasidi",
                        "D": "Önce WGS -> Normal çıkarsa Karyotip"
                    },
                    "A",
                    {
                        "A": "Doğru! Kılavuz algoritması: 1. Basamakta CMA ile kopya sayısı değişimleri (CNV) taranır; negatifse 2. Basamakta Trio-WES ile tek nükleotid ekzonik mutasyonlar taranır.",
                        "B": "Yanlış. Sanger tek gen bilindiğinde istenir.",
                        "C": "Yanlış. FISH bilinmeyen sendromda kör tarama yapamaz.",
                        "D": "Yanlış. Sıralama terstir ve WGS maliyetli son basamaktır."
                    }
                )
            ]
        }
    ]
