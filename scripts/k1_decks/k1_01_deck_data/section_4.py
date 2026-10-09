#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4 Builder: Minör ve Majör Anomaliler & Risk Basamakları (Adım 30 - 38 + Tekrar Sayfası)
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
            "slideNumber": 30,
            "title": "Minör ve Majör Anomali Sınıflamasının Temel Felsefesi",
            "subtitle": "Kozmetik varyasyon ile cerrahi/fonksiyonel defektin ayrımı",
            "badge": "Sınıflandırma",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Konjenital anomaliler, hastanın yaşam süresine, organ fonksiyonlarına ve cerrahi gereksinimine göre iki temel gruba ayrılır: ==Minör Anomaliler== ve ==Majör Anomaliler==.\n\nBu sınıflamanın arkasındaki klinik mantık:\n- **Fonksiyonel Etki:** Minör anomali tek başına tıbbi bir tedavi gerektirmez ve sağlığı tehdit etmez (örneğin kulak memesi yarığı veya ayak 2-3 sindaktilisi).\n  - **Majör Tehdit:** Majör anomali cerrahi onarım gerektirir, morbiditeyi ve mortaliteyi belirgin artırır (örneğin transpozisyon, meningomiyelosel).\n  - **İşaret Fişeği Rolü:** Minör anomaliler hiçbir zaman önemsiz kabul edilemez; çünkü minör anomaliler derinlerde gizlenmiş bir majör malformasyonun veya kromozomal sendromun dışarıya yansıyan ilk görsel sinyalleridir.",
            "coreContent": {
                "table": {
                    "title": "Minör ve Majör Anomali Temel Kriterleri",
                    "headers": ["Özellik", "Minör Anomali", "Majör Anomali"],
                    "rows": [
                        ["Medikal / Cerrahi Tedavi", "Gerektirmez (Kozmetiktir)", "Acil cerrahi veya medikal tedavi şarttır"],
                        ["Yaşam Süresine Etki", "Yaşam süresini kısaltmaz", "Yaşamı tehdit eder, mortalite oluşturur"],
                        ["Toplumdaki Sıklığı", "Nüfusun yaklaşık %15'inde bulunur", "Yenidoğanların yaklaşık %2 - %3'ünde görülür"],
                        ["Klinik Anlamı", "Majör anomali ve sendrom habercisidir", "Doğrudan organ yetmezliği ve sakatlık yaratır"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Minör Anomali", "explanation": "Cerrahi veya fonksiyonel tedavi gerektirmeyen, ancak sendromik tanıya rehberlik eden yapısal varyasyon."},
                {"term": "Majör Anomali", "explanation": "Bebeğin yaşamını tehdit eden, cerrahi onarım gerektiren ağır yapısal ve fonksiyonel organ defekti."}
            ],
            "spotPearls": [
                "Minör anomaliler cerrahi tedavi gerektirmez ancak sendromların ve gizli majör iç organ anomalilerinin en duyarlı belirteçleridir."
            ],
            "interactiveElements": [
                make_before_after(
                    "Minör Anomali",
                    "Majör Anomali",
                    ["Cerrahi tedavi gerektirmez", "Yaşam süresini kısaltmaz", "Toplumda sıktır (%15)", "İç organ defekti için haberci rolü oynar"],
                    ["Cerrahi veya medikal müdahale şarttır", "Mortalite ve ağır sakatlık yaratır", "Yenidoğanlarda %2-3 oranında görülür", "Organ fonksiyonunu doğrudan bozar"]
                ),
                make_micro_quiz(
                    "Bir konjenital anomalinin 'minör anomali' olarak tanımlanabilmesi için temel kriter hangisidir?",
                    {
                        "A": "Cerrahi onarım gerektirmemesi ve tek başına yaşamı tehdit etmemesi",
                        "B": "Yalnızca göz kapağında yerleşmesi",
                        "C": "Sadece 18 yaşından sonra ortaya çıkması",
                        "D": "Genetik testlerde hiçbir zaman saptanamaması"
                    },
                    "A",
                    {
                        "A": "Doğru! Minör anomaliler fonksiyonel veya cerrahi müdahale gerektirmeyen, yaşamı doğrudan tehdit etmeyen yapısal kusurlardır.",
                        "B": "Yanlış. Vücudun her anatomik bölgesinde minör anomali olabilir.",
                        "C": "Yanlış. Konjenitaldir, doğumda mevcuttur.",
                        "D": "Yanlış. Genetik sendromların parçası olarak saptanabilir."
                    }
                )
            ]
        },
        {
            "slideNumber": 31,
            "title": "Minör Anomalilerin Sayısal Yükü: Majör Risk Sıçraması (%3 - %10 - %90)",
            "subtitle": "Klinik genetiğin en ünlü istatistiksel kuralı",
            "badge": "Sınav Odağı",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Fizik muayenede saptanan minör anomali sayısı, bebekte eşlik eden bir majör malformasyon (örneğin gizli bir VSD veya renal agenezi) bulunma olasılığını doğrudan belirler.\n\nDavid Smith ve Marden'in klasik dismorfoloji istatistiği:\n- **0 Minör Anomali:** Majör anomali riski toplum bazal riski kadardır (~%2).\n- **1 Minör Anomali:** Yenidoğanda majör anomali eşlik etme riski ==%3'tür== (Toplumdan çok farklı değildir).\n- **2 Minör Anomali:** Majör anomali riski belirgin bir artışla ==%10'a== yükselir.\n- **3 veya Daha Fazla (3+) Minör Anomali:** Majör anomali veya genetik sendrom riski ==%90'a fırlar!==\n\n> 🚨 **Altın Kural:** Bir yenidoğanda 3 adet minör anomali (örn: düşük kulak + klinodaktili + tek avuç içi çizgisi) gördüyseniz, aksi kanıtlanana kadar bebekte gizli bir majör iç organ malformasyonu veya kromozom sendromu aramalısınız!",
            "coreContent": {
                "table": {
                    "title": "Minör Anomali Sayısına Göre Majör Anomali Riski",
                    "headers": ["Minör Anomali Sayısı", "Eşlik Eden Majör Anomali Riski", "Klinik Yönetim Stratejisi"],
                    "rows": [
                        ["0 Minör Anomali", "%1.5 - %2 (Popülasyon bazali)", "Rutin neonatal takip yeterlidir"],
                        ["1 Minör Anomali", "%3", "İzlem, dikkatli rutin muayene"],
                        ["2 Minör Anomali", "%10", "Ayrıntılı sistemik muayene, ekokardiyografi düşünülebilir"],
                        ["3 veya Daha Fazla (3+)", "%90", "EKO, USG, Genetik analiz (Karyotip/CMA) ŞARTTIR!"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Majör Risk Sıçraması", "explanation": "Minör anomali sayısının 1'den 3'e çıkmasıyla majör anomali olasılığının %3'ten %90'a dramatik artışı."},
                {"term": "Sistemik Tarama", "explanation": "Çoklu minör anomalisi olan olgularda iç organları taramak için yapılan ekokardiyografi ve batın ultrasonografisi."}
            ],
            "spotPearls": [
                "📌 [SINAV SPOTU] 1 minör anomaliye majör anomali eşlik etme riski %3 iken; 3 veya daha fazla minör anomali saptanan bir bebekte majör anomali eşlik etme riski %90'a fırlar!"
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Fizik muayenesinde 3 adet minör anomali (düşük kulak, 5. parmak klinodaktilisi ve tek transvers palmar çizgi) saptanan bir yenidoğanda eşlik eden majör bir anomali veya sendrom bulunma riski yaklaşık yüzde kaçtır?",
                    {
                        "A": "%90",
                        "B": "%3",
                        "C": "%10",
                        "D": "%50"
                    },
                    "A",
                    {
                        "A": "Doğru! Klasik dismorfoloji basamağına göre 1 minörde risk %3, 2 minörde %10, 3 veya daha fazlasında ise %90'dır.",
                        "B": "Yanlış. %3 sadece 1 minör anomali riskidir.",
                        "C": "Yanlış. %10 sadece 2 minör anomali riskidir.",
                        "D": "Yanlış. 3 anomalide risk %50 değil %90'a ulaşır."
                    }
                ),
                make_interactive_table(
                    "Minör Anomali Sayısı ve Majör Risk Ezber Tablosu",
                    ["Minör Anomali Sayısı", "Majör Anomali Riski", "Klinik Yaklaşım"],
                    [
                        [("1 Minör Anomali", False), ("%3", True, "%3"), ("Rutin Pediatrik İzlem", False)],
                        [("2 Minör Anomali", False), ("%10", True, "%10"), ("Hedefe Yönelik Detaylı Muayene", False)],
                        [("3 veya Daha Fazla Minör", False), ("%90", True, "%90"), ("EKO + USG + Genetik Test ŞART", True, "Tam tarama")]
                    ]
                )
            ]
        },
        {
            "slideNumber": 32,
            "title": "Klasik Minör Anomali Örnekleri: Yüz ve Ekstremite İpuçları",
            "subtitle": "Klinodaktili, Simian çizgisi, preauriküler pit, sandal aralığı",
            "badge": "Klinik Belirteç",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Klinik pratikte en sık karşılaşılan minör anomaliler eller, ayaklar ve kulak kepçesinde kümelenir:\n\n- **1. Tek Transvers Palmar Çizgi (Simian Çizgisi):** Avuç içindeki iki yatay çizginin tek bir transvers hatta birleşmesidir. Sağlıklı toplumda %1-2, Down sendromunda %50 oranında görülür.\n- **2. Klinodaktili:** 5. parmağın (küçük parmak) orta falanks hipoplazisi nedeniyle 4. parmağa doğru içe eğrilmesidir (Down sendromu).\n- **3. Sandal Aralığı (Sandal Gap):** Ayakta 1. ve 2. parmaklar arasındaki mesafenin anormal derecede geniş olmasıdır.\n- **4. Preauriküler Çukurcuk (Pit) ve Çıkıntı (Tag):** Kulak tragusu önünde 1. faringeal arktan kalan minik fistül veya deri uzantısıdır (böbrek anomalileri ile ilişkili olabilir).",
            "medicalTerms": [
                {"term": "Klinodaktili", "explanation": "Parmağın (en sık 5. parmak) orta falanks az gelişimi sonucu komşu parmağa doğru eğri durması."},
                {"term": "Simian Çizgisi", "explanation": "Avuç içini boydan boya geçen tek transvers fleksion çizgisi."},
                {"term": "Sandal Aralığı", "explanation": "Ayakta 1. ve 2. ayak parmakları arasındaki açıklığın normalden geniş olması."}
            ],
            "spotPearls": [
                "Tek transvers palmar çizgi sağlıklı popülasyonda %1-2 oranında görülebilen bir minör anomalidir; ancak Down sendromlu bebeklerde bu oran %50'ye çıkar."
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal El Morfolojisi",
                    "Down Sendromlu El Morfolojisi",
                    ["İki ayrı oblik palmar fleksiyon çizgisi", "5. parmak orta falanksı normal boyutta", "Düz, uzun parmak yapısı"],
                    ["Tek transvers palmar çizgi (Simian çizgisi)", "5. parmak orta falanks hipoplazisi ve klinodaktili", "Kısa, geniş el (brakidaktili)"]
                ),
                make_micro_quiz(
                    "Beşinci parmağın (küçük parmak) orta falanksındaki hipoplazi nedeniyle komşu dördüncü parmağa doğru eğrilmesi durumunu tanımlayan tıbbi terim hangisidir?",
                    {
                        "A": "Klinodaktili",
                        "B": "Kamptodaktili",
                        "C": "Sindaktili",
                        "D": "Polidaktili"
                    },
                    "A",
                    {
                        "A": "Doğru! Parmağın medio-lateral planda eğrilmesine klinodaktili denir.",
                        "B": "Yanlış. Kamptodaktili parmağın interfalangeal eklemden fleksiyon kontraktürüdür (bükük parmak).",
                        "C": "Yanlış. Sindaktili parmakların yapışık olmasıdır.",
                        "D": "Yanlış. Polidaktili fazla parmak varlığıdır."
                    }
                )
            ]
        },
        {
            "slideNumber": 33,
            "title": "Majör Anomaliler: Cerrahi Müdahale, Yaşamı Tehdit ve Ağır Morbidite",
            "subtitle": "Kardiyak, nöral tüp, gastrointestinal ve ekstremite agenezileri",
            "badge": "Klinik Ağırlık",
            "badgeColor": "rose",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Majör konjenital anomali; bebeğin yaşam süresini kısaltan, organ fonksiyonlarını ciddi biçimde bozan, acil cerrahi onarım gerektiren veya ileri derecede kozmetik deformiteye yol açan yapısal kusurdur.\n\nSistemlere göre majör malformasyon örnekleri:\n- **Santral Sinir Sistemi:** Nöral tüp defektleri (Meningomiyelosel, Anansefali), Holoprozensefali, Konjenital Ağır Hidrosefali.\n- **Kardiyovasküler Sistem:** Fallot Tetralojisi, Büyük Arter Transpozisyonu, Hipoplastik Sol Kalp Sendromu, Geniş VSD.\n- **Gastrointestinal & Duvar Defektleri:** Omfalosel (zarla kaplı göbek kordonu fıtığı), Gastroşizis (serbest barsak evisserasyonu), Özofagus Atrezisi, Anal Atrezi.\n- **Ekstremite:** Fokomeli (uzuvların yokluğu / güdük ekstremite), Ektrodaktili (ıstakoz kıskacı el/ayak).",
            "coreContent": {
                "table": {
                    "title": "Sistemik Majör Anomali Yelpazesi",
                    "headers": ["Sistem", "Majör Anomali Örneği", "Acil Klinik / Cerrahi Yaklaşım"],
                    "rows": [
                        ["Santral Sinir Sistemi", "Meningomiyelosel", "İlk 24-48 saatte cerrahi kapatma, enfeksiyon profilaksisi"],
                        ["Kardiyak", "Büyük Arter Transpozisyonu", "Prostaglandin E1 infüzyonu, acil arteryel switch cerrahisi"],
                        ["Karın Duvarı", "Omfalosel", "Kese perforasyonunu önleme, aşamalı cerrahi redüksiyon"],
                        ["Gastrointestinal", "Anal Atrezi", "Acil kolostomi veya posterior sagital anorektoplasti"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Meningomiyelosel", "explanation": "Omurga kanalı arkasının kapanamaması sonucu medulla spinalis ve meninkslerin kese şeklinde dışarı fıtıklaşması."},
                {"term": "Omfalosel", "explanation": "Karın içi organların göbek kordonu tabanından amniyon ve periton zarı ile kaplı olarak fıtıklaşması."}
            ],
            "spotPearls": [
                "Meningomiyelosel, Fallot tetralojisi, omfalosel ve anal atrezi; acil cerrahi onarım gerektiren klasik majör anomalilerdir."
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Aşağıdakilerden hangisi cerrahi müdahale gerektirmeyen bir 'MİNÖR ANOMALİ' örneğidir?",
                    {
                        "A": "Preauriküler kulak çukurcuğu (pit)",
                        "B": "Meningomiyelosel",
                        "C": "Fallot Tetralojisi",
                        "D": "Omfalosel"
                    },
                    "A",
                    {
                        "A": "Doğru! Preauriküler pit kozmetik bir varyasyondur ve cerrahi tedavi gerektirmez (minör anomali).",
                        "B": "Yanlış. Meningomiyelosel nöral tüp defektidir, acil cerrahi şarttır (majör).",
                        "C": "Yanlış. Fallot tetralojisi siyanotik konjenital kalp hastalığıdır (majör).",
                        "D": "Yanlış. Omfalosel karın duvarı defektidir (majör)."
                    }
                ),
                make_cloze(
                    "Omurganın kapanamaması sonucu medulla spinalis ve sinir köklerinin kese şeklinde dışarı fıtıklaştığı majör nöral tüp defektine meningomiyelosel adı verilir.",
                    "meningomiyelosel",
                    "Açık nöral tüp defekti"
                )
            ]
        },
        {
            "slideNumber": 34,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Minör ve Majör Anomaliler & Risk Basamakları",
            "subtitle": "%3, %10 ve %90 kurallarının ve klinik belirteçlerin tam sentezi",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Genetik",
            "synthesisNarrative": "Bu modül, minör ve majör konjenital anomali ayrımını, klinik risk basamaklarını ve amfilerde sıkça sorulan istatistiki oranları hafızaya kalıcı olarak yerleştirmek için hazırlanmıştır.\n\n### 🧠 Kritik Ezber Kontrol Listesi:\n- **Minör Anomali:** Tedavi gerektirmez; ancak sendrom ve majör defektin en hassas habercisidir.\n- **1 Minör Anomali:** Majör anomali eşlik etme riski ==%3==.\n- **2 Minör Anomali:** Majör anomali eşlik etme riski ==%10==.\n- **3+ Minör Anomali:** Majör anomali veya sendrom eşlik etme riski ==%90!==\n- **Preauriküler Pit / Tag:** Kulak önü minör anomalisi; böbrek USG taranmasını düşündürebilir.\n- **Simian Çizgisi:** Tek transvers palmar çizgi; Down sendromunda %50 sıklıktadır.\n- **Klinodaktili:** 5. parmağın içe eğriliğidir; orta falanks hipoplazisi nedeniyledir.",
            "coreContent": {
                "table": {
                    "title": "Anomali Sınıflaması ve İstatistiki Basamaklar Matrisi",
                    "headers": ["Anomali Sayısı / Tipi", "Majör Risk Yüzdesi", "Klinik Önem", "Örnek"],
                    "rows": [
                        ["1 Minör Anomali", "%3", "Popülasyon bazaline çok yakındır", "İzole klinodaktili"],
                        ["2 Minör Anomali", "%10", "Belirgin risk artışı başlar", "Simian çizgisi + preauriküler pit"],
                        ["3 veya Daha Fazla Minör", "%90", "Sendrom ve majör organ defekti neredeyse kesindir", "Düşük kulak + Simian + Sandal gap"],
                        ["Majör Anomali", "Tanım gereği ağır", "Doğrudan cerrahi ve yoğun bakım gerektirir", "Fallot, Omfalosel, Meningomiyelosel"]
                    ]
                }
            },
            "medicalTerms": [
                {"term": "Simian Çizgisi", "explanation": "Avuç içindeki iki ana çizginin tek bir transvers çizgi olarak birleşmesi."},
                {"term": "Klinodaktili", "explanation": "Küçük parmağın hipoplastik orta falanks nedeniyle dördüncü parmağa doğru eğrilmesi."}
            ],
            "spotPearls": [
                "📌 [TEKRAR SPOTU] 1 minör = %3 risk | 2 minör = %10 risk | 3+ minör = %90 risk!",
                "📌 [TEKRAR SPOTU] Minör anomali cerrahi gerektirmez, majör anomali yaşamı tehdit eder ve cerrahi gerektirir."
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Minör - Majör Ayrımı ve İstatistiksel Risk Ezber Tablosu",
                    ["Klinik Durum", "Majör Anomali / Sendrom Riski", "Klinik Müdahale Şekli"],
                    [
                        [("1 Adet Minör Anomali", False), ("%3", True, "%3"), ("Tedavi gerekmez, rutin izlem", False)],
                        [("2 Adet Minör Anomali", False), ("%10", True, "%10"), ("Ayrıntılı muayene ve takip", False)],
                        [("3 veya Daha Fazla Minör", False), ("%90", True, "%90"), ("EKO, Batın USG ve Genetik Test", True, "Tam tarama")],
                        [("Majör Organ Malformasyonu", False), ("Tanım gereği mevcuttur", True, "Mevcut"), ("Acil cerrahi onarım ve takip", True, "Cerrahi")]
                    ]
                ),
                make_micro_quiz(
                    "Yenidoğan servisinde takip edilen bir bebeğin muayenesinde tek transvers palmar çizgi, 5. parmakta klinodaktili ve bilateral preauriküler pit saptanmıştır. Bu bebek için en doğru klinik yaklaşım hangisidir?",
                    {
                        "A": "3 minör anomaliye %90 majör anomali eşlik edebileceğinden EKO, batın USG ve genetik inceleme planlanmalıdır",
                        "B": "Hiçbir tetkike gerek yoktur, bebek taburcu edilebilir",
                        "C": "Yalnızca preauriküler pit cerrahi olarak derhal çıkarılmalıdır",
                        "D": "Sadece 18 yaşına geldiğinde kontrol önerilmelidir"
                    },
                    "A",
                    {
                        "A": "Doğru! 3 adet minör anomalisi olan bebekte majör organ veya sendrom riski %90'dır; EKO, batın USG ve genetik konsültasyon şarttır.",
                        "B": "Yanlış. %90'lık risk göz ardı edilemez.",
                        "C": "Yanlış. Preauriküler pit acil cerrahi gerektirmez, asıl tehlike içerideki majör defektlerdir.",
                        "D": "Yanlış. Erken neonatal dönemde tanı konulmalıdır."
                    }
                ),
                make_micro_quiz(
                    "Klasik dismorfolojik epidemiyolojik çalışmalara göre, 2 adet minör anomalisi olan bir bebekte eşlik eden bir majör malformasyon bulunma riski yüzde kaçtır?",
                    {
                        "A": "%10",
                        "B": "%3",
                        "C": "%90",
                        "D": "%50"
                    },
                    "A",
                    {
                        "A": "Doğru! 1 minörde risk %3, 2 minörde risk %10, 3 veya daha fazlasında %90'dır.",
                        "B": "Yanlış. %3 tek minör anomali riskidir.",
                        "C": "Yanlış. %90 üç ve üzeri minör anomali riskidir.",
                        "D": "Yanlış. İstatistiki basamak %10'dur."
                    }
                )
            ]
        }
    ]
