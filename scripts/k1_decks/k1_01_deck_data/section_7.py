#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bölüm 7: Birlikte Görülen Anomaliler: Sekans, Sendrom, Asosiasyon, Kompleks (Adım 47 - 55 + Tekrar Sayfası)
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
            "slideNumber": 47,
            "title": "Birlikte Görülen Anomalilerin Sınıflandırma Mantığı ve Klinik Gereklilik",
            "subtitle": "Sekans, Sendrom, Asosiasyon ve Kompleks kavramlarının ayrımı",
            "badge": "Sınıflandırma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Yenidoğanda birden fazla yapısal anomali bir arada saptandığında, bu bulguların birbiriyle olan biyolojik ilişkisi doğru tanı ve genetik danışma için hayati önem taşır.\n\nKlinik genetik bu çoklu tabloları 4 temel kategoriye ayırır:\n- **1. Sekans (Sequence):** Tek bir primer lokalize defektin (örneğin böbrek yokluğu) başlattığı domino taşı benzeri zincirleme kaskad.\n- **2. Sendrom (Syndrome):** Tek bir ortak etiyolojiye (spesifik bir kromozom anomalisi veya gen mutasyonu) bağlı olarak vücudun birden çok bağımsız organ sisteminde eş zamanlı beliren anomaliler.\n- **3. Asosiasyon (Association):** Birbirinden embriyolojik olarak bağımsız anomalilerin şans eseri beklenenden daha sık bir arada görülmesi; ancak ortak bir genetik nedenin henüz kanıtlanamamış olması (Örn: VACTERL).\n- **4. Kompleks / Gelişimsel Saha Defekti:** Embriyoda coğrafi olarak birbirine komşu olan bir doku alanının ortak morfogenetik hasarı (Örn: Holoprozensefali).",
            "coreContent": {
                "table": {
                    "title": "Çoklu Anomali Gruplarının Karşılaştırması",
                    "headers": ["Kavram", "Temel Mekanizma", "İlişki Tipi", "Klasik Örnek"],
                    "rows": [
                        ["Sekans (Sequence)", "Tek bir primer defekt -> Ardışık kaskad", "Neden-Sonuç zinciri (Domino etkisi)", "Potter Sekansı, Pierre Robin Sekansı"],
                        ["Sendrom (Syndrome)", "Tek bir ortak etiyoloji (gen/kromozom)", "Farklı organlarda eş zamanlı tutulum", "Down Sendromu, Marfan Sendromu"],
                        ["Asosiasyon (Association)", "Bilinmeyen etiyoloji / İstatistiki kümelenme", "Şans eserinden daha sık birliktelik", "VACTERL Asosiasyonu, CHARGE (ilk tanımı)"],
                        ["Kompleks (Saha Defekti)", "Bitişik embriyonik alanın ortak hasarı", "Coğrafi / bölgesel morfogenez defekti", "Holoprozensefali, Kloakal ekstrofi"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Sekans (Sequence)", "explanation": "Tek bir primer anomalinin ardışık ikincil ve üçüncül defektler zincirine yol açması."},
                {"term": "Asosiasyon (Association)", "explanation": "Aralarında doğrudan patogenetik bağ bilinmeyen anomalilerin istatistiksel birlikteliği."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Sekansta domino taşı gibi bir 'neden-sonuç' zinciri vardır; Sendromda ise tek bir genetik neden farklı sistemleri aynı anda etkiler."
            ],
            "interactiveElements": [
                make_before_after(
                    "Sekans (Neden-Sonuç Zinciri)",
                    "Sendrom (Ortak Etiyoloji)",
                    ["Tek bir primer başlangıç noktası vardır", "Bulgular birbirinin ardışık sonucudur (Domino taşı)", "Örnek: Böbrek agenezisi -> Oligohidramniyos -> Potter"],
                    ["Tek bir gen veya kromozom kusuru vardır", "Bulgular birbirinin sonucu değil, aynı genin farklı organlardaki etkisidir", "Örnek: Trizomi 21 -> Kalp defekti + Epikantus + Zeka geriliği"]
                ),
                make_micro_quiz(
                    "Tek bir primer malformasyonun veya mekanik engelin başlattığı ve domino taşları gibi ardışık ikincil doku bozukluklarına yol açtığı klinik tabloya ne ad verilir?",
                    {
                        "A": "Sekans (Sequence)",
                        "B": "Sendrom (Syndrome)",
                        "C": "Asosiasyon (Association)",
                        "D": "İzole Displazi"
                    },
                    "A",
                    {
                        "A": "Doğru! Tek bir primer olayın ardışık zincirleme kaskada yol açtığı durumlara Sekans adı verilir.",
                        "B": "Yanlış. Sendromda tek bir ortak etiyoloji farklı organları bağımsız olarak etkiler.",
                        "C": "Yanlış. Asosiasyon istatistiki birlikteliktir.",
                        "D": "Yanlış. Displazi hücresel mimari bozukluğudur."
                    }
                )
            ]
        },
        {
            "slideNumber": 48,
            "title": "Potter Sekansı: Bilateral Renal Agenezisten Anüriye ve Akciğer Hipoplazisine",
            "subtitle": "Klinik genetiğin ve patolojinin en kusursuz sekans modeli",
            "badge": "Klasik Sekans",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Potter sekansı, sekans kavramının tıptaki en kusursuz ve en öğretici prototipidir.\n\nPotter sekansının adım adım neden-sonuç kaskadı:\n- **1. Primer Olay:** Fetal üreter tomurcuğunun gelişmemesi sonucu ==Bilateral Renal Agenezi== (veya posterior üretral valv obstrüksiyonu) meydana gelir.\n- **2. Fetal Anüri:** Fetal böbrekler idrar üretemez; amniyon sıvısının ana kaynağı fetal idrar olduğu için şiddetli ==Oligohidramniyos== gelişir.\n- **3. Uterin Kompresyon (Deformasyon):** Koruyucu sıvı yastığı kalmadığı için uterus fetüsün üzerine yapışır; gaga burun, basık kulaklar, kırışık deri (Potter yüzü) ve pes ekinovarus deformasyonları oluşur.\n- **4. Pulmoner Hipoplazi (Ölüm Nedeni):** Fetal akciğerlerin gelişmesi için amniyon sıvısını soluması (solunum hareketleri) ve toraksın genişlemesi şarttır. Sıvı yokluğu nedeniyle akciğerler hipoplastik kalır.\n- **Sonuç:** Bebek doğumdan sonraki ilk saatlerde akciğer yetmezliğinden (pulmoner hipoplazi) kaybedilir.",
            "medicalTerms": [
                {"term": "Potter Sekansı", "explanation": "Böbrek yokluğu veya anürinin oligohidramniyos, basık yüz ve ölümcül akciğer hipoplazisine yol açtığı kaskad."},
                {"term": "Pulmoner Hipoplazi", "explanation": "Akciğer alveollerinin amniyon sıvısı eksikliği nedeniyle gelişemeyip güdük kalması (Potter'da ölüm nedeni)."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Potter sekansında bebeğin ölümüne yol açan temel patoloji böbrek yokluğu değil, oligohidramniyosa ikincil gelişen Pulmoner Hipoplazidir!"
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Potter Sekansı Domino Kaskadı",
                    [
                        "Primer Olay: Bilateral renal agenezi (böbreklerin oluşmaması).",
                        "Fetal idrar üretilemez ve fetal anüri gelişir.",
                        "Amniyon sıvısı tükenir (Ağır Oligohidramniyos).",
                        "Mekanik bası: Potter yüzü (gaga burun, basık kulak) ve çomak ayak (pes ekinovarus).",
                        "Ölümcül Sonuç: Akciğerler genişleyemez -> Pulmoner hipoplazi ve neonatal ölüm."
                    ]
                ),
                make_micro_quiz(
                    "Potter sekansı ile doğan bir yenidoğanın doğumdan hemen sonra hayatını kaybetmesine yol açan EN TEMEL patoloji hangisidir?",
                    {
                        "A": "Pulmoner hipoplazi (akciğerlerin gelişememesi)",
                        "B": "Böbrek yetmezliğine bağlı üre yüksekliği",
                        "C": "Ayaklardaki pes ekinovarus deformasyonu",
                        "D": "Kafatasındaki skafosefali deformitesi"
                    },
                    "A",
                    {
                        "A": "Doğru! Fetal dönemde böbrek fonksiyonunu anne plasentası kompanse eder; asıl ölüm nedeni amniyon sıvısı yokluğunda akciğerlerin gelişememesidir (pulmoner hipoplazi).",
                        "B": "Yanlış. İntrauterin kanda üre ve elektrolitleri anne temizler, bebek üremiden ölmez.",
                        "C": "Yanlış. Pes ekinovarus kozmetik deformasyondur, öldürmez.",
                        "D": "Yanlış. Skafosefali ölüm nedeni değildir."
                    }
                )
            ]
        },
        {
            "slideNumber": 49,
            "title": "Pierre Robin Sekansı: Mikrognatiden Glossozise ve Yarık Damağa",
            "subtitle": "Mandibula hipoplazisinin başlattığı mekanik solunum obstrüksiyonu kaskadı",
            "badge": "Klasik Sekans",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Pierre Robin sekansı, çene gelişimindeki küçük bir gecikmenin damak ve hava yolunu nasıl kilitlediğini gösteren dramatik bir sekans örneğidir.\n\nPierre Robin sekansının patogenetik basamakları:\n- **1. Primer Olay (Mikrognati):** 7-10. haftalarda alt çene (mandibula) embriyolojik olarak yetersiz gelişir ve geride kalır (mikrognati / retrognati).\n- **2. Dilin Arkaya Kayması (Glossozis):** Küçük çene tabanında dil öne doğru yerleşemez; farenkse doğru geriye ve yukarıya itilir.\n- **3. Damağın Birleşememesi (U Şekilli Yarık Damak):** Normalde embriyonun 8. haftasında palatin çıkıntılar yataylaşarak orta hatta birleşecektir. Ancak araya giren dev dil kitlesi palatin çıkıntıların birbirine kavuşmasını fiziksel olarak engeller. Sonuçta geniş, ==U şeklinde yarık damak== oluşur.\n- **4. Hava Yolu Obstrüksiyonu:** Doğumda dil geriye düşerek hava yolunu tıkar; acil prone pozisyon veya cerrahi müdahale gerekebilir.",
            "coreContent": {
                "table": {
                    "title": "Pierre Robin Sekansı Triadı",
                    "headers": ["Bulgu", "Patolojik Nitelik", "Klinik Yansıması"],
                    "rows": [
                        ["1. Mikrognati", "Primer Defekt", "Aşırı küçük ve geride alt çene"],
                        ["2. Glossozis", "İkincil Mekanik Sonuç", "Dilin laringofarenkse geriye düşmesi ve obstrüksiyon"],
                        ["3. U Şekilli Yarık Damak", "Üçüncül Mekanik Engel", "Dilin araya girmesiyle palatin rafların birleşememesi"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Pierre Robin Sekansı", "explanation": "Mikrognati, glossozis ve U şeklinde yarık damak triadı ile seyreden sekans tablosu."},
                {"term": "Glossozis", "explanation": "Dilin geriye doğru farenks hava yolunu tıkayacak şekilde yer değiştirmesi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] Pierre Robin sekansında yarık damak klasik malformasyonel V şeklinde değil, dilin araya girmesi nedeniyle geniş 'U şeklinde'dir!"
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Pierre Robin Kaskadı",
                    [
                        "Primer Defekt: Alt çene büyümesi gecikir (Mikrognati).",
                        "Dil öne uzayamaz ve orofarenkse geriye itilir (Glossozis).",
                        "Geriye ve yukarı kalkan dil, damak raflarının birleşmesini engeller.",
                        "Sonuç Triadı: Mikrognati + Glossozis + U Şekilli Yarık Damak."
                    ]
                ),
                make_micro_quiz(
                    "Pierre Robin sekansında görülen yarık damağın embriyolojik oluşum mekanizması nedir?",
                    {
                        "A": "Geriye kayan dilin (glossozis) palatin rafların orta hatta birleşmesini mekanik olarak engellemesi",
                        "B": "Damak kemiğini kodlayan kolajen geninin primer intrinsik delesyonu",
                        "C": "Amniyotik bantların üst çeneyi fiziksel olarak kesmesi",
                        "D": "Maternal folik asit fazlalığına bağlı hücre ölümü"
                    },
                    "A",
                    {
                        "A": "Doğru! Pierre Robin'de damak dokusu aslında normaldir; araya giren dil mekanik bir bariyer oluşturduğu için raflar birleşemez ve U şeklinde yarık kalır.",
                        "B": "Yanlış. Bu primer intrinsik malformasyon olurdu, sekans olmazdı.",
                        "C": "Yanlış. Amniyotik bant disrupsiyonudur.",
                        "D": "Yanlış. Folik asit fazlalığı yarık damak yapmaz."
                    }
                )
            ]
        },
        {
            "slideNumber": 50,
            "title": "Sendrom (Syndrome): Tek Bir Ortak Etiyoloji ve Çoklu Sistem Tutulumu",
            "subtitle": "Kromozom anomalileri veya pleiotropik gen mutasyonlarının geniş yelpazesi",
            "badge": "Sendrom",
            "badgeColor": "violet",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Sendrom; tek bir ortak genetik veya çevresel etiyolojiye bağlı olarak, embriyolojik açıdan birbirinden tamamen bağımsız çoklu doku ve organ sistemlerinde eş zamanlı ortaya çıkan anomaliler bütünüdür.\n\nSendromu sekanstan ayıran temel prensip:\n- **Bağımsız Organ Kusurları:** Down sendromunda görülen konjenital kalp defekti (AVSD), zeka geriliği ve duodenal atrezi birbirinin sonucu DEĞİLDİR; her biri 21. kromozomdaki fazla gen dozajının farklı organlardaki bağımsız ifadesidir.\n- **Etiyolojik Çeşitlilik:** Sendromlar kromozomal (Trizomi 21, Turner), mikrodelesyonel (DiGeorge 22q11.2, Williams), monogenik (Marfan sendromu - FBN1 geni) veya teratojenik (Fetal Alkol Sendromu) kökenli olabilir.",
            "medicalTerms": [
                {"term": "Sendrom", "explanation": "Tek bir patogenetik nedene bağlı olarak birden çok organda eş zamanlı beliren anomaliler topluluğu."},
                {"term": "Pleiotropi", "explanation": "Tek bir mutasyonun birbiriyle doğrudan ilişkisiz çoklu sistemlerde klinik bulgu vermesi."}
            ],
            "spotPearls": [
                "Sendromda bulgular birbirinin sonucu değil, aynı kök etiyolojinin farklı dokulardaki eş zamanlı tezahürleridir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Sendrom (Down Sendromu)",
                    "Sekans (Potter Sekansı)",
                    ["Tek bir etiyoloji (Trizomi 21)", "Kalp, beyin, barsak anomalileri birbirinden BAĞIMSIZDIR", "Ortak kök nedenden beslenir"],
                    ["Tek bir primer organ defekti (Böbrek agenezisi)", "Tüm bulgular birbirine ZİNCİRLEME BAĞLIDIR", "Böbrek yokluğu -> Sıvı yokluğu -> Akciğer hipoplazisi"]
                ),
                make_micro_quiz(
                    "Fibrillin-1 (FBN1) genindeki tek bir mutasyonun aort anevrizması, lens luksasyonu ve uzun parmaklar (araknodaktili) ile seyreden 'Marfan Sendromu'na yol açması aşağıdaki genetik kavramlardan hangisiyle açıklanır?",
                    {
                        "A": "Pleiotropik etki gösteren Sendrom",
                        "B": "Mekanik dış basıya bağlı Sekans",
                        "C": "Vasküler Disrupsiyon",
                        "D": "İzole Saha Defekti"
                    },
                    "A",
                    {
                        "A": "Doğru! Tek bir gen mutasyonunun göz, kardiyovasküler sistem ve iskelette bağımsız klinik bulgular üretmesi klasik pleiotropik sendromdur.",
                        "B": "Yanlış. Marfan bir sekans değildir, organlar birbirini bozmaz.",
                        "C": "Yanlış. Disrupsiyon dış doku kopmasıdır.",
                        "D": "Yanlış. Marfan tüm vücudu tutan sistemik bağ dokusu sendromudur."
                    }
                )
            ]
        },
        {
            "slideNumber": 51,
            "title": "Asosiasyon (Association): İstatistiki Birliktelik ve VACTERL Modeli",
            "subtitle": "Ortak etiyolojisi kanıtlanmamış, şansın ötesinde sık kümelenen anomaliler",
            "badge": "Asosiasyon",
            "badgeColor": "amber",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Asosiasyon; embriyolojik veya patogenetik olarak aralarında doğrudan bir neden-sonuç bağı bulunmayan iki veya daha fazla anomalinin, popülasyonda şans eseri beklenenden istatistiksel olarak çok daha sık bir arada görülmesidir.\n\nAsosiasyonun klinik kuralları:\n- **Etiyoloji Bilinmez:** Spesifik tek bir gen mutasyonu veya kromozom anomalisi henüz saptanamamıştır (saptanırsa sendrom sınıfına terfi eder; örneğin CHARGE tablosu CHD7 geni bulununca sendrom olmuştur!).\n- **Rekürrens Riski Yoktur:** Bir ailede VACTERL'li çocuk doğduğunda, sonraki çocukta tekrarlama riski toplum bazal riski kadardır (<%1).\n- **En Klasik Örnek: ==VACTERL (VATER) Asosiasyonu==:**\n  - **V:** Vertebral anomaliler\n  - **A:** Anal atrezi\n  - **C:** Kardiyak defektler (VSD)\n  - **TE:** Trakeoözofageal fistül ve özofagus atrezisi\n  - **R:** Renal anomaliler (agenezi/displazi)\n  - **L:** Limb (uzuv) anomalileri (radial aplazi)",
            "coreContent": {
                "table": {
                    "title": "VACTERL Asosiasyonunun Anatomik Bileşenleri",
                    "headers": ["Harf", "İngilizce Karşılık", "Klinik Anomali", "Sıklık / Tanı Kriteri"],
                    "rows": [
                        ["V", "Vertebral", "Hemivertebra, skolyoz, kelebek vertebra", "Tanı için bu bileşenlerden"],
                        ["A", "Anal", "İmperfore anüs / Anal atrezi", "en az 3 tanesinin"],
                        ["C", "Cardiac", "VSD, Fallot, ASD", "aynı hastada bulunması"],
                        ["TE", "Tracheo-Esophageal", "Özofagus atrezisi + Trakeoözofageal fistül", "VACTERL tanısı koydurur"],
                        ["R", "Renal", "Renal agenezi, polikistik böbrek", "(Rekürrens riski <%1)"],
                        ["L", "Limb", "Radial hipoplazi / aplazi, başparmak yokluğu", "Zeka genellikle NORMALDİR!"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "VACTERL Asosiasyonu", "explanation": "Vertebral, anal, kardiyak, trakeoözofageal, renal ve ekstremite defektlerinin istatistiki birlikteliği."},
                {"term": "CHARGE Asosiasyonu -> Sendromu", "explanation": "Kolobom, kalp, koanal atrezi tablosunun CHD7 geni keşfedilerek sendroma dönüşmesi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] VACTERL bir sendrom değil asosiasyondur; bilinen tek bir genetik sebebi yoktur, zeka genellikle tamamen normaldir ve rekürrens riski <%1'dir!"
            ],
            "interactiveElements": [
                make_interactive_table(
                    "VACTERL Kısaltması ve Organ Defektleri Ezber Tablosu",
                    ["Harf", "Organ Bölgesi", "Klasik Malformasyon"],
                    [
                        [("V", False), ("Vertebra", False), ("Hemivertebra / Skolyoz", True, "Omurga")],
                        [("A", False), ("Anüs", False), ("Anal Atrezi (İmperfore)", True, "Makat")],
                        [("C", False), ("Kardiyak", False), ("VSD / Fallot", True, "Kalp")],
                        [("TE", False), ("Trakeo-Özofageal", False), ("Özofagus atrezisi + Fistül", True, "Yemek borusu")],
                        [("R", False), ("Renal", False), ("Böbrek Agenezisi / Displazi", True, "Böbrek")],
                        [("L", False), ("Limb (Uzuv)", False), ("Radial Aplazi / Başparmak", True, "Önkol / Radius")]
                    ]
                ),
                make_micro_quiz(
                    "Anal atrezi, trakeoözofageal fistül ve radial kemik aplazisi saptanan bir bebekte VACTERL tanısı konulmuştur. Ailenin bir sonraki gebeliğinde bu tablonun tekrarlama (rekürrens) riski yaklaşık ne kadardır?",
                    {
                        "A": "Toplum bazal riski kadar (<%1)",
                        "B": "%50 (Otozomal dominant)",
                        "C": "%25 (Otozomal resesif)",
                        "D": "%100 (Kromozomal aktarım)"
                    },
                    "A",
                    {
                        "A": "Doğru! VACTERL bir asosiasyondur, Mendeliyen veya kromozomal bir kalıtım göstermez; tekrarlama riski ihmal edilecek kadar düşüktür (<%1).",
                        "B": "Yanlış. Dominant kalıtılmaz.",
                        "C": "Yanlış. Resesif kalıtılmaz.",
                        "D": "Yanlış. Kromozomal translokasyon değildir."
                    }
                )
            ]
        },
        {
            "slideNumber": 52,
            "title": "Kompleks ve Gelişimsel Saha Defekti (Developmental Field Defect)",
            "subtitle": "Komşu embriyonik doku alanının bölgesel morfogenetik çöküşü",
            "badge": "Saha Defekti",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Gelişimsel saha (developmental field); embriyoda birbirine komşu olan ve tek bir morfogenetik birim gibi davranarak koordineli gelişen doku bölgesidir.\n\nSaha defektlerinin klinik doğası:\n- **Bölgesel Etki:** Erken dönemde bu sahaya gelen bir hasar, o coğrafi alandaki tüm yapıları birden bozar.\n- **Holoprozensefali:** Prekordal mezoderm ve ön beyin sahasının ayrışamamasıdır. Ön beyin iki yarımküreye bölünemezken, hemen komşusu olan orta yüz de bölünemez; siklopi (tek göz), tek burun deliği (probosis) ve tek santral kesici diş oluşur.\n- **Kloakal Ekstrofi:** Kaudal mezoderm sahasının çökmesiyle mesane ekstrosifisi, imperfore anüs ve omfalosel bir arada görülür.",
            "medicalTerms": [
                {"term": "Gelişimsel Saha Defekti", "explanation": "Embriyoda mekansal olarak komşu olan ve koordineli gelişen doku alanının ortak hasarı."},
                {"term": "Holoprozensefali", "explanation": "Ön beynin iki hemisfere ayrılamamasıyla seyreden ağır kraniofasiyal orta hat saha defekti."}
            ],
            "spotPearls": [
                "Holoprozensefali klasik bir gelişimsel saha defektidir; ön beyin ve orta yüz tek bir morfogenetik alandan birlikte hasar görür."
            ],
            "interactiveElements": [
                make_cloze(
                    "Ön beynin iki yarımküreye ayrılamaması ile orta yüzün gelişimsel çöküşünü birleştiren gelişimsel saha defektine holoprozensefali adı verilir.",
                    "holoprozensefali",
                    "Orta hat kraniofasiyal saha defekti"
                ),
                make_micro_quiz(
                    "Siklopi (tek göz), probosis (tüp burun) ve tek lopluk ön beyin anomalisi ile seyreden bir bebekteki Holoprozensefali tablosu hangi gelişimsel kategoriye girer?",
                    {
                        "A": "Gelişimsel Saha Defekti (Kompleks)",
                        "B": "Amniyotik Bant Disrupsiyonu",
                        "C": "Pozisyonel Deformasyon",
                        "D": "İzole İskelet Displazisi"
                    },
                    "A",
                    {
                        "A": "Doğru! Holoprozensefali prekordal plak ve ön beyin gelişimsel sahasının ortak bölgesel hasarıdır (kompleks / field defect).",
                        "B": "Yanlış. Amniyotik bant dış doku kopmasıdır.",
                        "C": "Yanlış. Deformasyon mekanik basıdır.",
                        "D": "Yanlış. İskelet displazisi kıkırdak mimari bozukluğudur."
                    }
                )
            ]
        },
        {
            "slideNumber": 53,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Sekans, Sendrom, Asosiasyon & Kompleks Sentezi",
            "subtitle": "Potter, Pierre Robin, Down ve VACTERL ayırıcı tanı ezber tablosu",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu modül, Bölüm 7'de işlenen çoklu anomali sınıflamasının tüm klinik ayrımlarını ve sınav tuzaklarını tek bir hafıza matrisinde birleştirmektedir.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Sekans:** Tek bir primer olay -> Domino kaskadı (Potter: Renal agenezi -> Oligohidramniyos -> Pulmoner hipoplazi; Pierre Robin: Mikrognati -> Glossozis -> U yarık damak).\n- **Sendrom:** Tek bir etiyoloji (Trizomi 21, FBN1 mutasyonu) -> Bağımsız organ tutulumları.\n- **Asosiasyon:** Şanstan daha sık birliktelik; etiyoloji ==BİLİNMEZ==, zeka ==NORMALDİR==, rekürrens ==YOKTUR (<%1)==. Örnek: VACTERL.\n- **Kompleks / Saha Defekti:** Bitişik embriyonik coğrafi alanın ortak çöküşü (Holoprozensefali).\n- **Pierre Robin Yarık Damak:** Dil araya girdiği için ==U şeklindedir!==\n- **Potter Ölüm Nedeni:** Böbrek değil, ==Pulmoner Hipoplazidir!==\n- **VACTERL:** Vertebral, Anal, Kardiyak, TE fistül, Renal, Limb.",
            "coreContent": {
                "table": {
                    "title": "Çoklu Anomali Tipleri Büyük Sentez Matrisi",
                    "headers": ["Grup", "Patogenetik Mantık", "Rekürrens Riski", "Karakteristik Örnek"],
                    "rows": [
                        ["Sekans", "Primer defekt -> Ardışık domino etkisi", "Primer defektin genetiğine bağlıdır", "Potter Sekansı, Pierre Robin Sekansı"],
                        ["Sendrom", "Tek ortak etiyoloji (Kromozom/Gen)", "Mendeliyen / Kromozomal risk", "Down Sendromu, Marfan Sendromu"],
                        ["Asosiasyon", "İstatistiki kümelenme, etiyoloji meçhul", "Toplum bazali kadar (< %1)", "VACTERL Asosiasyonu"],
                        ["Kompleks", "Gelişimsel sahanın bölgesel hasarı", "Etiyolojiye göre değişir", "Holoprozensefali, Kloakal ekstrofi"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Potter Yüzü", "explanation": "Oligohidramniyos basısına bağlı gaga burun, basık kulaklar ve derin göz altı çizgileri."},
                {"term": "U Şekilli Damak", "explanation": "Pierre Robin sekansında dilin araya girmesiyle palatin rafların birleşememesi sonucu oluşan geniş damak yarığı."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] Sekans = Domino kaskadı | Sendrom = Ortak genetik kök | Asosiasyon = İstatistiki kümelenme (Risk yok) | Kompleks = Komşu saha defekti.",
                "📌 [TEKRAR SPOTU] Potter'da ölüm nedeni: Pulmoner Hipoplazi | Pierre Robin damak şekli: U şeklinde | VACTERL rekürrens riski: <%1."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Çoklu Anomali Grupları ve Ayırt Edici Özellikler Ezber Tablosu",
                    ["Grup Adı", "Temel Tanım Kriteri", "Kritik Klinik Örnek"],
                    [
                        [("Sekans", False), ("Neden-Sonuç Domino Zinciri", True, "Domino kaskadı"), ("Potter & Pierre Robin", True, "Potter / PR")],
                        [("Sendrom", False), ("Tek Ortak Genetik Etiyoloji", True, "Gen/Kromozom"), ("Down & Marfan Sendromu", True, "Down / Marfan")],
                        [("Asosiasyon", False), ("İstatistiki Birliktelik (Gen Yok)", True, "Bilinmeyen gen"), ("VACTERL Asosiasyonu", True, "VACTERL")],
                        [("Kompleks (Saha Defekti)", False), ("Bitişik Alanın Bölgesel Hasarı", True, "Coğrafi saha"), ("Holoprozensefali", True, "Holoprozensefali")]
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdaki klinik tablolardan hangisi 'TEK BİR PRİMER DEFEKTİN BAŞLATTIĞI ARDIŞIK ZİNCİRLEME NEDEN-SONUÇ KASKADI' (Sekans) için en doğru örnektir?",
                    {
                        "A": "Bilateral renal agenezinin oligohidramniyos ve pulmoner hipoplaziye yol açması (Potter Sekansı)",
                        "B": "21. kromozom trizomisinin kalp defekti ve zeka geriliği yapması (Down Sendromu)",
                        "C": "Anal atrezi ile trakeoözofageal fistülün şans eseri birlikteliği (VACTERL)",
                        "D": "FGFR3 gen mutasyonunun tüm kemiklerde boy kısalığı yapması (Akondroplazi)"
                    },
                    "A",
                    {
                        "A": "Doğru! Böbrek yokluğunun sıvı azlığına, onun da mekanik bası ve akciğer hipoplazisine yol açması kusursuz bir sekans örneğidir.",
                        "B": "Yanlış. Down bir sendromdur.",
                        "C": "Yanlış. VACTERL bir asosiasyondur.",
                        "D": "Yanlış. Akondroplazi bir displazidir."
                    }
                ),
                make_micro_quiz(
                    "VACTERL asosiasyonunda görülen uzuv (Limb) anomalileri arasında EN SIK rastlanan karakteristik kemik defekti hangisidir?",
                    {
                        "A": "Radius hipoplazisi veya aplazisi (başparmak yokluğu/gelişmeme)",
                        "B": "Femur kemiğinin aşırı uzaması",
                        "C": "Tüm parmakların sekiz adet olması",
                        "D": "Patella kemiğinin ikiye ayrılması"
                    },
                    "A",
                    {
                        "A": "Doğru! VACTERL'in L (Limb) bileşeni tipik olarak radial kemik hipoplazisi/aplazisi ve başparmak anomalileridir.",
                        "B": "Yanlış. Femur uzaması görülmez.",
                        "C": "Yanlış. Aşırı polidaktili VACTERL'in primer özelliği değildir.",
                        "D": "Yanlış. Patella anomalisi tırnak-patella sendromundadır."
                    }
                )
            ]
        }
    ]
