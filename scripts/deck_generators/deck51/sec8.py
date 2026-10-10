# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec8():
    slides = []

    # Slide 71: İdrarda Nitrit Testi ve 4 Saat Kuralı
    s71_narrative = (
        "İdrar dipstik şeridinde yer alan nitrit reaksiyonu, üriner sistemde nitrat redüktaz enzimi "
        "taşıyan bakterilerin metabolik aktivitesini saptayan son derece özgül bir biyokimyasal testtir.\n\n"
        "- **Biyokimyasal Reaksiyon:** Normal koşullarda idrarda nitrit bulunmaz; diyetle alınan nitratlar, "
        "Gram negatif enterik bakterilerin salgıladığı **nitrat redüktaz enzimi** aracılığıyla nitrite dönüştürülür.\n"
        "- **4 Saat Kuralı:** Bakterilerin idrardaki nitratı yeterli düzeyde nitrite indirgeyebilmesi "
        "için, idrarın **mesanede en az 4 saat süreyle beklemiş olması** zorunludur.\n"
        "- **Çocuklardaki Yetersizlik:** Küçük çocuklar mesanelerini sık boşalttıkları için (idrar "
        "mesanede 4 saat kalamaz), çocukluk çağında **nitrit testinin duyarlılığı yoktur**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Nitrit testinin pozitifleşmesi için bakterinin mesanede en az 4 SAAT beklemiş olması gerekir; çocuklarda mesane sık boşaldığından nitrit testinin duyarlılığı yoktur."
    )
    s71_bullets = [
        "Gram (-) enterik bakteriler nitrat redüktaz ile nitratı nitrite çevirir.",
        "Bu dönüşüm için bakterinin mesanede en az 4 saattir bulunuyor olması gerekir.",
        "Çocuklarda mesane sık boşaltıldığı için nitrit testinin duyarlılığı yoktur."
    ]
    s71_elements = [
        make_cloze("Nitratın nitrite dönüştürülebilmesi için bakterinin mesanede en az 4 saat beklemiş olması gerekmektedir.", "en az 4 saat", "Dört saatlik mesane inkübasyon süresi"),
        make_table("Nitrit Testi Dinamikleri", ["Parametre", "Biyokimyasal Koşul", "Klinik Yansıması"], [
            {"cells": [{"text": "Enzim ve Bakteri", "isMasked": False}, {"text": "Gram (-) bakterilerin nitrat redüktazı", "isMasked": True, "hint": "enterik basillerin enzimi"}, {"text": "Nitratın nitrite indirgenmesi"}]},
            {"cells": [{"text": "Mesane Süresi", "isMasked": False}, {"text": "En az 4 saat mesanede bekleme", "isMasked": True, "hint": "dört saatlik asgari bekleme"}, {"text": "Sabah ilk idrar örneğinde en yüksek verim"}]},
            {"cells": [{"text": "Pediatrik Popülasyon", "isMasked": False}, {"text": "Sık işeme nedeniyle süre yetersiz", "isMasked": False}, {"text": "Çocuklarda nitrit testinin DUYARLILIĞI YOKTUR", "isMasked": True, "hint": "çocukta testin güvenilmezliği"}]}
        ]),
        make_chain("Nitrit Biyokimyasal Reaksiyon Zinciri", [
            "1. Diyet Alımı: Sebzelerden alınan nitratlar glomerüler filtrasyonla idrara geçer.",
            "2. Bakteriyel Temas: Enterik Gram (-) basil nitrat redüktaz salgılar.",
            "3. 4 Saatlik İnkübasyon: Mesanede en az 4 saat bekleyen idrarda nitrit birikir.",
            "4. Renk Reaksiyonu: Dipstik şeridindeki amin emdirilmiş kağıt pembe renge döner."
        ]),
        make_recall("İdrarda nitrit testinin pozitifleşebilmesi için gereken asgari mesane bekleme süresi ne kadardır?", "Bakterinin mesanede en az 4 saattir bulunuyor olması gerekir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Nitrit Testi ve 4 Saat", [
            {"text": "Gram (-) enterik bakteriler nitratı nitrite çevirir.", "isLie": False, "explanation": "Doğru. Nitrat redüktaz salgılarlar."},
            {"text": "Bu dönüşüm için bakterinin mesanede en az 4 saat bulunması gerekir.", "isLie": False, "explanation": "Doğru. Zaman kuralıdır."},
            {"text": "Çocuklarda mesanelerini çok sık boşalttıkları için nitrit testinin duyarlılığı mükemmeldir.", "isLie": True, "explanation": "Tuzak! Çocuklarda mesane sık boşaltıldığı için idrar 4 saat kalamaz; bu nedenle çocuklarda nitrit testinin DUYARLILIĞI YOKTUR."},
            {"text": "Normal koşullarda idrarda nitrit bulunmaz.", "isLie": False, "explanation": "Doğru. Sadece bakteri varsa oluşur."}
        ]),
        make_quiz("İdrarda nitrit testinin pozitifleşebilmesi için bakterinin mesanede en az ne kadar süre bulunuyor olması gerekir?", [
            {"key": "A", "text": "En az 4 saat", "isCorrect": True, "explanation": "Ders notunda 'bu dönüşüm için bakterinin mesanede en az 4 saattir bulunuyor olması gerekir' açıkça belirtilmiştir."},
            {"key": "B", "text": "En az 4 gün", "isCorrect": False, "explanation": "Aşırı süredir."},
            {"key": "C", "text": "Sadece 3 saniye", "isCorrect": False, "explanation": "Enzimatik dönüşüm için yetersizdir."},
            {"key": "D", "text": "Hiç beklemesine gerek yoktur", "isCorrect": False, "explanation": "4 saat şarttır."}
        ])
    ]
    slides.append(make_slide(71, "İdrarda Nitrit Testi ve 4 Saat Kuralı", "Nitrat redüktaz enzimi, 4 saat mesane bekleme kuralı ve çocuklardaki duyarsızlık", "Laboratuvar Bulguları", s71_narrative, s71_bullets, s71_elements))

    # Slide 72: Nitrit Testinde Yanlış Negatiflik Nedenleri
    s72_narrative = (
        "Klinik pratikte nitrit testinin negatif çıkması, hastada üriner sistem enfeksiyonunun "
        "kesinlikle bulunmadığı anlamına gelmez; testin duyarlılığı %53 civarındadır.\n\n"
        "- **Ekarte Ettirmeme Kuralı:** Nitrit testi bakteriüriyi saptar ancak **negatif sonuç İYE'nin "
        "ekarte edilmesi için ASLA yeterli değildir**.\n"
        "- **Diyetsel ve Fiziksel Nedenler:** Diyetle yetersiz nitrat alımı (sebze tüketmeme), aşırı "
        "sıvı alımı sonucu **dilüe (seyreltik) idrar** ve hızlı/sık idrar örneği alınması (4 saat dolmaması) "
        "yanlış negatiflik yapar.\n"
        "- **Biyokimyasal ve Mikrobiyolojik Nedenler:** **Yüksek doz C vitamini (askorbik asit)** dipstik "
        "reaksiyonunu bloke eder; ayrıca enterokoklar, S. saprophyticus ve Acinetobacter gibi **nitratı "
        "indirgeyemeyen Gram pozitif bakteriler** enfeksiyon yapsa dahi nitrit daima negatif kalır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Nitrit yanlış negatif nedenleri: Yüksek doz C vitamini, dilüe idrar, hızlı örnek alımı, yetersiz diyet nitratı ve nitratı indirgeyemeyen Gram (+) bakterilerdir."
    )
    s72_bullets = [
        "Negatif sonuç İYE'nin ekarte edilmesi için kesinlikle yeterli değildir.",
        "Yüksek doz C vitamini (askorbik asit) şerit reaksiyonunu inhibe eder.",
        "Dilüe idrar, hızlı örnek alımı ve Gram (+) bakteriler testi negatif çıkarır."
    ]
    s72_elements = [
        make_cloze("İdrarda nitrit testinde şerit reaksiyonunu baskılayarak yalancı negatiflik yapan vitamin C vitamini (askorbik asit) alımıdır.", "C vitamini", "Askorbik asit antioksidan vitamini"),
        make_table("Nitrit Testinde Yalancı Negatiflik Nedenleri", ["Mekanizma", "Spesifik Neden", "Kimyasal / Mikrobiyolojik Süreç"], [
            {"cells": [{"text": "Bakteriyel Neden", "isMasked": False}, {"text": "Nitratı indirgeyemeyen Gram (+) bakteriler", "isMasked": True, "hint": "nitrat redüktazı olmayan mikroplar"}, {"text": "Enterokok ve S. saprophyticus nitrit üretmez"}]},
            {"cells": [{"text": "Kimyasal Girişim", "isMasked": False}, {"text": "Yüksek doz vitamin C (askorbik asit)", "isMasked": True, "hint": "şerit reaktifini bozan vitamin"}, {"text": "Dipstik diazonyum renk reaksiyonunun blokajı"}]},
            {"cells": [{"text": "Fiziksel / Preanalitik", "isMasked": False}, {"text": "Dilüe idrar veya hızlı örnek alımı", "isMasked": False}, {"text": "Konsantrasyon düşüklüğü veya <4 saat süre", "isMasked": False}]}
        ]),
        make_chain("Yalancı Negatif Nitrit Oluşumu", [
            "1. Enfeksiyon: Hasta S. saprophyticus sistiti geçirir veya bol C vitamini içer.",
            "2. Enzim Eksikliği / Blokaj: Gram (+) bakteride nitrat redüktaz yoktur veya reaktif bloke olur.",
            "3. Strip Teması: İdrar şeridinde pembe renk değişimi meydana gelmez.",
            "4. Yanıltıcı Sonuç: Hasta ağır enfekte olmasına rağmen nitrit testi negatif raporlanır."
        ]),
        make_recall("İdrarda nitrit testinin yalancı negatif çıkmasına yol açan başlıca durumlar nelerdir?", "Yüksek doz C vitamini, dilüe idrar, hızlı örnek alımı (<4 saat), diyette yetersiz nitrat ve nitratı indirgeyemeyen Gram pozitif bakterilerdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Nitrit Yanlış Negatiflik", [
            {"text": "Negatif nitrit sonucu İYE'nin ekarte edilmesi için yeterli değildir.", "isLie": False, "explanation": "Doğru. Duyarlılığı düşüktür."},
            {"text": "Yüksek doz vitamin C nitrit testinde yanlış negatifliğe yol açabilir.", "isLie": False, "explanation": "Doğru. Reaksiyonu bozar."},
            {"text": "Nitrit negatifse hasta %100 kesinlikle steril kabul edilir ve tüm idrar testleri yırtılıp atılır.", "isLie": True, "explanation": "Tuzak! Nitrit testi %53 duyarlılığa sahiptir; Gram pozitif bakterilerde veya C vitamininde negatif çıkar, asla ekarte ettirmez."},
            {"text": "Nitratı indirgeyemeyen Gram pozitif bakteriler nitrit üretmez.", "isLie": False, "explanation": "Doğru. Enzimleri yoktur."}
        ]),
        make_quiz("Aşağıdakilerden hangisi idrar tahlilinde nitrit testinin YANLIŞ NEGATİF sonuçlanmasına yol açan nedenlerden biridir?", [
            {"key": "A", "text": "Yüksek doz vitamin C kullanımı ve dilüe idrar", "isCorrect": True, "explanation": "Ders notunda yanlış negatif nedenleri arasında diyetle yetersiz nitrat, hızlı örnek alımı, dilüe idrar, yüksek doz vitamin C ve gram (+) bakteriler sayılmıştır."},
            {"key": "B", "text": "Mesanede idrarın 24 saat beklemesi", "isCorrect": False, "explanation": "Bu pozitifliği artırır."},
            {"key": "C", "text": "Yoğun E. coli üremesi", "isCorrect": False, "explanation": "E. coli nitrit pozitiftir."},
            {"key": "D", "text": "İdrarın aşırı konsantre olması", "isCorrect": False, "explanation": "Konsantrasyon tespiti kolaylaştırır."}
        ])
    ]
    slides.append(make_slide(72, "Nitrit Testinde Yanlış Negatiflik Nedenleri", "Nitrit negatifliğinin ekarte ettirmemesi, C vitamini etkisi, dilüe idrar ve Gram (+) etkenler", "Laboratuvar Bulguları", s72_narrative, s72_bullets, s72_elements))

    # Slide 73: Lökosit Esteraz Testi: Piyürinin Biyokimyasal İmzası
    s73_narrative = (
        "Lökosit esteraz testi, idrardaki intakt veya parçalanmış nötrofillerin granüllerinde bulunan "
        "indoksil esteraz enzimini saptayan son derece duyarlı bir kimyasal yöntemdir.\n\n"
        "- **Piyüri Göstergesi:** Lökosit esteraz normal idrarda negatiftir; pozitifliği **piyüri (idrarda "
        "enflamasyon ve lökosit) varlığına işaret eder**.\n"
        "- **Lizise Rağmen Pozitiflik:** Beklemiş veya hipotonik idrarda nötrofiller parçalanıp mikroskopta "
        "hücre olarak görülemese dahi, ortama saçılan esteraz enzimi nedeniyle **lökosit esteraz pozitif kalmaya devam eder**.\n"
        "- **Klinik Duyarlılık ve ASB:** Klinik bulgularla birlikte duyarlılığı **%94'e kadar çıkar**; "
        "asemptomatik bakteriüride lökosit esteraz sıklıkla negatif olduğundan semptomatik sistit ayrımında yardımcıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [ÇIKMIŞ SORU] İdrar analizinde PİYÜRİYİ (idrarda lökosit varlığını) gösteren dipstik testi LÖKOSİT ESTERAZ testidir!"
    )
    s73_bullets = [
        "Lökosit esteraz normal idrarda negatiftir ve PİYÜRİYİ gösterir.",
        "Hücreler mikroskopta parçalansa bile enzim ortamda kalır ve (+) saptanır.",
        "Klinik bulgularla birlikte duyarlılığı %94'e kadar yükselir."
    ]
    s73_elements = [
        make_cloze("İdrar analizinde piyüriyi (idrarda lökosit varlığını) gösteren biyokimyasal test lökosit esteraz testidir.", "lökosit esteraz", "Nötrofil granül enzimi dipstik testi"),
        make_table("Lökosit Esteraz Testi Profili", ["Özellik", "Test Yanıtı", "Klinik Açıklama"], [
            {"cells": [{"text": "Gösterdiği Durum", "isMasked": False}, {"text": "Piyüri (idrarda lökosit varlığı)", "isMasked": True, "hint": "akyuvar ve enflamasyon tespiti"}, {"text": "Ürotelyal enflamatuar reaksiyon"}]},
            {"cells": [{"text": "Parçalanmış Hücreler", "isMasked": False}, {"text": "Esteraz (+) kalmaya devam eder", "isMasked": False}, {"text": "Mikroskopide lökosit görülmese bile tespit", "isMasked": True, "hint": "hücre lizisine rağmen enzim varlığı"}]},
            {"cells": [{"text": "Duyarlılık Oranı", "isMasked": False}, {"text": "%94'e kadar çıkar", "isMasked": False}, {"text": "Yüksek sensitiviteye sahip tarama testi", "isMasked": False}]}
        ]),
        make_chain("Lökosit Esteraz Aktivasyon Zinciri", [
            "1. Enflamasyon: Bakteriyel invazyonla nötrofiller idrar lümenine dökülür.",
            "2. Enzim Salınımı: Lökosit azurofilik granüllerinden indoksil esteraz salgılanır.",
            "3. Hücre Lizisi: Bekleyen idrarda hücre zarı patlasa da esteraz enzimi sağlam kalır.",
            "4. Kolorimetrik Dönüşüm: Dipstik şeridindeki substrat hidroliz olarak mor renk verir."
        ]),
        make_recall("İdrar tahlilinde piyüriyi (idrarda lökosit/akyuvar varlığını) gösteren dipstik parametresi nedir?", "Lökosit esteraz testidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Lökosit Esteraz", [
            {"text": "Lökosit esteraz testi idrarda piyüri varlığını gösterir.", "isLie": False, "explanation": "Doğru. Klasik sınav sorusu kuralıdır."},
            {"text": "Beklemiş idrarda lökosit parçalansa bile lökosit esteraz (+) kalır.", "isLie": False, "explanation": "Doğru. Enzim idrara karışır."},
            {"text": "Lökosit esteraz testi sadece idrardaki şeker miktarını ölçen diyabet testidir.", "isLie": True, "explanation": "Tuzak! Lökosit esteraz şekeri değil, piyüriyi (lökosit enflamasyonunu) gösterir."},
            {"text": "Klinik bulgularla birlikte duyarlılığı %94'e kadar ulaşır.", "isLie": False, "explanation": "Doğru. Çok duyarlıdır."}
        ]),
        make_quiz("İdrar analizinde aşağıdaki parametrelerden hangisi PİYÜRİYİ (idrarda lökosit varlığını) gösterir?", [
            {"key": "A", "text": "Lökosit esteraz testi", "isCorrect": True, "explanation": "Lökosit esteraz piyüriyi; nitrit ise bakteriüriyi gösterir (Kurul 1 çıkmış sorusudur)."},
            {"key": "B", "text": "Nitrit testi", "isCorrect": False, "explanation": "Nitrit bakteriüriyi gösterir."},
            {"key": "C", "text": "Silendirüri", "isCorrect": False, "explanation": "Lökosit varlığını doğrudan göstermez."},
            {"key": "D", "text": "Kristalüri", "isCorrect": False, "explanation": "Taş kristallerini gösterir."}
        ])
    ]
    slides.append(make_slide(73, "Lökosit Esteraz Testi: Piyürinin Biyokimyasal İmzası", "Lökosit esteraz, piyüri göstergesi, parçalanmış hücrelerde pozitiflik ve %94 duyarlılık", "Laboratuvar Bulguları", s73_narrative, s73_bullets, s73_elements))

    # Slide 74: Nitrit ve Lökosit Esteraz Birlikteliği: Klinik Karar Kuralı
    s74_narrative = (
        "Tam idrar tahlilinde nitrit ve lökosit esteraz testlerinin birlikte değerlendirilmesi, "
        "enfeksiyon varlığı veya yokluğu hakkında hekime en yüksek tanısal gücü sunar.\n\n"
        "- **Biyolojik Anlam Ayrımı:** **Lökosit esteraz → Piyüriyi** (konak enflamasyonunu); **Nitrit "
        "→ Bakteriüriyi** (üropatojen varlığını) gösterir.\n"
        "- **Çifte Pozitiflik:** Hem lökosit esteraz hem nitrit pozitif olduğunda (LE+ / Nitrit+), "
        "tanısal özgüllük zirve yapar ve **İYE lehine son derece güçlü bir kanıt** oluşturur.\n"
        "- **Çifte Negatiflik:** Hem lökosit esteraz hem nitrit negatif olduğunda (LE- / Nitrit-), "
        "kombine negatif prediktif değer %99'un üzerine çıkar ve **hastayı İYE tanısından kesin biçimde uzaklaştırır**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] LE (+) piyüriyi, Nitrit (+) bakteriüriyi gösterir. İkisi birden (+) ise İYE lehine son derece güçlü; ikisi birden (-) ise İYE'den uzaklaştıran çok güçlü bir bulgudur!"
    )
    s74_bullets = [
        "Lökosit esteraz = Piyüri (enflamasyon); Nitrit = Bakteriüri (etken).",
        "İkisi birlikte (+) olduğunda İYE lehine son derece güçlü kanıttır.",
        "İkisi birlikte (-) olduğunda hastayı İYE tanısından uzaklaştırır."
    ]
    s74_elements = [
        make_cloze("Tam idrar analizinde lökosit esteraz piyüriyi gösterirken nitrit testi bakteriüriyi gösterir.", "bakteriüriyi", "İdrarda bakteri bulunması durumu"),
        make_table("LE ve Nitrit Birlikteliğinin Klinik Anlamı", ["Dipstik Durumu", "Fizyopatolojik Durum", "Klinik Karar"], [
            {"cells": [{"text": "LE (+) ve Nitrit (+)", "isMasked": False}, {"text": "Piyüri (+) ve Bakteriüri (+)", "isMasked": True, "hint": "hem iltihap hem mikrop varlığı"}, {"text": "İYE lehine son derece güçlü tanı → Tedavi et"}]},
            {"cells": [{"text": "LE (-) ve Nitrit (-)", "isMasked": False}, {"text": "Piyüri (-) ve Bakteriüri (-)", "isMasked": False}, {"text": "İYE'den kesin uzaklaşma → Antibiyotik verme", "isMasked": True, "hint": "enfeksiyonun dışlanması"}]},
            {"cells": [{"text": "LE (+) ve Nitrit (-)", "isMasked": False}, {"text": "Steril piyüri veya Gram (+) enfeksiyon", "isMasked": False}, {"text": "Kültür ve mikroskopi ile ileri inceleme", "isMasked": False}]}
        ]),
        make_chain("Dipstik Klinik Karar Zinciri", [
            "1. Strip Okuma: Şeritte lökosit esteraz ve nitrit bantları incelenir.",
            "2. Çifte Pozitif: İkisi de renk değiştirdiyse İYE kesin kabul edilir.",
            "3. Çifte Negatif: İkisi de negatifse gereksiz antibiyotik derhal engellenir.",
            "4. Uyumsuzluk: Biri (+) biri (-) ise mikroskopi ve kültürle doğrulanır."
        ]),
        make_recall("Lökosit esteraz ve nitrit testlerinin ikisinin birden negatif çıkmasının klinik önemi nedir?", "Hastayı İYE tanısından kesin biçimde uzaklaştıran (İYE olmadığını gösteren) son derece güçlü bir bulgudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: LE ve Nitrit Birlikteliği", [
            {"text": "Lökosit esteraz piyüriyi, nitrit bakteriüriyi gösterir.", "isLie": False, "explanation": "Doğru. Temel biyolojik ayrımdır."},
            {"text": "İkisi birlikte pozitif olduğunda İYE lehine güçlü kanıttır.", "isLie": False, "explanation": "Doğru. Özgüllük çok yüksektir."},
            {"text": "İkisi de negatif çıktığında hasta kesinlikle ağır veba geçiriyordur ve karantinaya alınır.", "isLie": True, "explanation": "Tuzak! İkisi birden negatifse hasta İYE'den uzaklaşır; idrar yolu enfeksiyonu dışlanır."},
            {"text": "İkisi birlikte negatifse İYE tanısından uzaklaşılır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("Tam idrar tahlilinde lökosit esteraz ve nitrit testlerinin her ikisinin birden NEGATİF saptanması klinik olarak ne ifade eder?", [
            {"key": "A", "text": "İdrar yolu enfeksiyonu tanısından uzaklaştıran güçlü bir bulgudur", "isCorrect": True, "explanation": "Ders notunda 'ikisi birlikte negatif olduğunda İYE'den uzaklaşan güçlü bir bulgudur' kuralı açıkça belirtilmiştir."},
            {"key": "B", "text": "Hastada kesinlikle böbrek kanseri olduğunu kanıtlar", "isCorrect": False, "explanation": "İlişkisizdir."},
            {"key": "C", "text": "Hastanın derhal diyalize bağlanmasını gerektirir", "isCorrect": False, "explanation": "İlişkisizdir."},
            {"key": "D", "text": "Bakterilerin antibiyotikleri tamamen yediğini gösterir", "isCorrect": False, "explanation": "Tıbbi temeli yoktur."}
        ])
    ]
    slides.append(make_slide(74, "Nitrit ve Lökosit Esteraz Birlikteliği: Klinik Karar Kuralı", "LE piyüri, nitrit bakteriüri; çifte pozitiflik ve çifte negatiflik kararları", "Laboratuvar Bulguları", s74_narrative, s74_bullets, s74_elements))

    # Slide 75: İdrar Mikroskopisi ve Piyüri Tanımı (>10 lökosit/mm³)
    s75_narrative = (
        "İdrar mikroskopisi, dipstik kimyasal testlerini teyit eden ve hücresel elemanları doğrudan "
        "gözler önüne seren temel tanı basamağıdır.\n\n"
        "- **Santrifüjsüz İnceleme (Piyüri Tanımı):** Santrifüj edilmemiş steril idrarda lökosit "
        "sayım kamerası (hemositometre) ile **milimetreküpte 10'dan fazla lökosit (>10 lökosit/mm³)** "
        "saptanması piyürinin resmi tanı kriteridir.\n"
        "- **Santrifüjlü İnceleme:** İdrar 2000 devirde 5 dakika santrifüj edilip çökelti 40x büyütme "
        "(büyük büyütme sahası - HPF) ile incelendiğinde, **her sahada 5-10'dan fazla lökosit** görülmesi piyüri kabul edilir.\n"
        "- **Kombine İnceleme Üstünlüğü:** Santrifüjsüz idrarda hücre sayımı ile Gram boyalı mikroskobik "
        "incelemenin birlikte yapılması sensitiviteyi en üst düzeye çıkarır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Piyüri tanımı: Santrifüj edilmemiş idrarda mm³'de >10 lökosit; santrifüj edilmiş idrar sedimentinde 40x büyütmede her sahada 5-10 lökosit bulunmasıdır."
    )
    s75_bullets = [
        "Piyüri tanımı: Santrifüj edilmemiş idrarda mm³'de >10 lökosit bulunmasıdır.",
        "Santrifüj edilmiş sedimentte 40x büyütmede her sahada 5-10 lökosit piyüridir.",
        "Hücre sayımı ve Gram incelemenin kombine yapılması duyarlılığı artırır."
    ]
    s75_elements = [
        make_cloze("Santrifüj edilmemiş idrarda hemositometrik lökosit kamerası ile mm³'de >10 lökosit bulunması piyüri olarak tanımlanır.", ">10 lökosit", "Milimetreküpte ondan fazla akyuvar bulunması"),
        make_table("Piyüri Mikroskobik Tanı Kriterleri", ["İnceleme Yöntemi", "Büyütme / Cihaz", "Piyüri Eşik Değeri"], [
            {"cells": [{"text": "Santrifüjsüz İdrar", "isMasked": False}, {"text": "Lökosit sayım kamerası (hemositometre)", "isMasked": True, "hint": "hücre sayım lamı"}, {"text": "mm³'de >10 lökosit bulunması"}]},
            {"cells": [{"text": "Santrifüjlü Çökelti (Sediment)", "isMasked": False}, {"text": "40x büyütme (HPF)", "isMasked": False}, {"text": "Her sahada 5-10 lökosit", "isMasked": True, "hint": "büyük büyütmede saha başına akyuvar"}]},
            {"cells": [{"text": "Lam-Lamel Arası Nativ", "isMasked": False}, {"text": "Doğrudan yayma", "isMasked": False}, {"text": "Her sahada 1-2 lökosit üzeri patolojik", "isMasked": False}]}
        ]),
        make_chain("Mikroskopik Piyüri Doğrulama Zinciri", [
            "1. Örnekleme: Taze idrar santrifüj edilmeden hemositometreye damlatılır.",
            "2. Kamera Sayımı: Milimetreküpteki nötrofiller tek tek sayılır.",
            "3. Eşik Aşımı: mm³'de 15 lökosit (>10 lökosit/mm³) bulunur.",
            "4. Piyüri Teşhisi: Ürotelyal enflamatuar reaksiyon mikroskopik olarak belgelenir."
        ]),
        make_recall("Santrifüj edilmemiş taze idrarda piyüri (lökositüri) tanısı koymak için gereken lökosit eşik değeri nedir?", "Milimetreküpte 10'dan fazla lökosittir (>10 lökosit/mm³)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Piyüri Tanımı", [
            {"text": "Santrifüj edilmemiş idrarda lökosit kamerası ile mm³'de >10 lökosit piyüridir.", "isLie": False, "explanation": "Doğru. Standart kriterdir."},
            {"text": "Santrifüj edilmiş idrarın 40x büyütmesinde her sahada 5-10 lökosit saptanması piyüridir.", "isLie": False, "explanation": "Doğru. Sediment kriteridir."},
            {"text": "Piyüri tanısı için idrarda en az 10 kilo et parçası görülmesi şarttır.", "isLie": True, "explanation": "Tuzak! Piyüri mikroskobik lökosit sayımıdır (>10 lökosit/mm³)."},
            {"text": "Hücre sayımı ve Gram incelemenin kombine yapılması duyarlılığı artırır.", "isLie": False, "explanation": "Doğru. Sensitiviteyi yükseltir."}
        ]),
        make_quiz("Santrifüj edilmemiş idrar örneğinde lökosit sayım kamerası ile yapılan incelemede PİYÜRİ tanısı için eşik değer nedir?", [
            {"key": "A", "text": "mm³'de >10 lökosit", "isCorrect": True, "explanation": "Ders notunda santrifüj edilmemiş idrarda lökosit kamerası ile mm³'de >10 lökosit bulunması piyüri olarak tanımlanmıştır."},
            {"key": "B", "text": "mm³'de >1.000.000 lökosit", "isCorrect": False, "explanation": "Aşırı yüksek eşiktir."},
            {"key": "C", "text": "mm³'de tam 0 lökosit", "isCorrect": False, "explanation": "Normaldir."},
            {"key": "D", "text": "mm³'de sadece 1 adet eritrosit", "isCorrect": False, "explanation": "Piyüriyi göstermez."}
        ])
    ]
    slides.append(make_slide(75, "İdrar Mikroskopisi ve Piyüri Tanımı (>10 lökosit/mm³)", "Piyüri kriteri, santrifüjsüz mm³'de >10 lökosit, 40x büyütmede 5-10 lökosit", "Laboratuvar Bulguları", s75_narrative, s75_bullets, s75_elements))

    # Slide 76: Lökosit Silendirleri ve Renal Parankim Hasarı
    s76_narrative = (
        "İdrar sedimentinde izlenen silendirler, renal tübül lümeninin şeklini alan proteinöz matriks "
        "(Tamm-Horsfall proteini) kalıplarıdır; içerdikleri hücresel eleman hasarın kaynağını gösterir.\n\n"
        "- **Oluşum Mekanizması:** Böbrek tübüllerinde gelişen akut interstisyel enflamasyon sırasında "
        "nötrofiller tübül lümenine sızar ve Tamm-Horsfall proteini jelatinize olurken bu lökositleri hapseder.\n"
        "- **Kardinal Tanısal Anlamı:** İdrar mikroskopisinde **lökosit silendirlerinin görülmesi "
        "BÖBREK HASARINI (akut pyelonefriti) kesin olarak kanıtlar**.\n"
        "- **Sistit Ayrımı:** Alt üriner sistemde (mesane veya üretra) silendir oluşamaz; bu nedenle "
        "lökosit silendiri saptanan bir hastada basit sistit tanısı derhal terk edilmeli, pyelonefrit "
        "tedavisi planlanmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İdrar sedimentinde LÖKOSİT SİLENDİRİ görülmesi BÖBREK HASARINI (akut pyelonefriti) gösterir; alt üriner sistem enfeksiyonunda silendir oluşmaz!"
    )
    s76_bullets = [
        "Lökosit silendirleri tübüllerde Tamm-Horsfall matriksi içinde lökositlerin hapsolmasıdır.",
        "İdrar sedimentinde lökosit silendiri görülmesi BÖBREK HASARINI kanıtlar.",
        "Alt üriner sistemde (sistit) silendir oluşmaz; üst sistem tutulumunu belgeler."
    ]
    s76_elements = [
        make_cloze("İdrar mikroskopisinde lökosit silendirleri görülmesi enfeksiyonun böbrek hasarı ve pyelonefrit kaynaklı olduğunu gösterir.", "böbrek hasarı", "Renal tübüler parankim hasarı"),
        make_table("Silendir Tipleri ve Klinik Anlamları", ["Silendir Tipi", "Oluştuğu Anatomik Yer", "Klinik Yansıması"], [
            {"cells": [{"text": "Lökosit Silendiri", "isMasked": False}, {"text": "Renal tübül lümeni (üst sistem)", "isMasked": True, "hint": "böbrek tübülleri"}, {"text": "Böbrek hasarı ve Akut Pyelonefrit kanıtı"}]},
            {"cells": [{"text": "Eritrosit Silendiri", "isMasked": False}, {"text": "Glomerül ve tübül", "isMasked": False}, {"text": "Glomerülonefrit kanıtı", "isMasked": True, "hint": "glomerüler kanama işareti"}]},
            {"cells": [{"text": "Hiyalin Silendir", "isMasked": False}, {"text": "Renal tübül", "isMasked": False}, {"text": "Ağır egzersiz, ateş veya konsantre idrar (non-spesifik)", "isMasked": False}]}
        ]),
        make_chain("Lökosit Silendiri Oluşum Zinciri", [
            "1. Tübüler İnvazyon: Bakteriler böbrek tübüllerine sızar.",
            "2. Lökosit Akını: Nötrofiller tübül lümenini doldurur.",
            "3. Jelatinizasyon: Tamm-Horsfall proteini nötrofilleri kalıplayarak silendir oluşturur.",
            "4. Dökülme: Kalıp idrarla atılır; mikroskopta görülmesi böbrek parankim hasarını belgeler."
        ]),
        make_recall("İdrar mikroskopisinde lökosit silendirlerinin saptanması enfeksiyonun hangi anatomik organda olduğunu kesin olarak gösterir?", "Böbrek parankiminde olduğunu (böbrek hasarını ve akut pyelonefriti) gösterir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Lökosit Silendirleri", [
            {"text": "Lökosit silendirleri böbrek hasarını gösterir.", "isLie": False, "explanation": "Doğru. Pyelonefrit göstergesidir."},
            {"text": "Silendirler sadece böbrek tübüllerinde oluşabilir, mesanede oluşamaz.", "isLie": False, "explanation": "Doğru. Tübüler kalıplardır."},
            {"text": "Lökosit silendiri basit bir tırnak batmasının idrara yansıyan görüntüsüdür.", "isLie": True, "explanation": "Tuzak! Lökosit silendiri renal tübüler lökosit infiltrasyonunun kesin kanıtıdır."},
            {"text": "Sistitte lökosit silendiri görülmez.", "isLie": False, "explanation": "Doğru. Sistit mesaneyle sınırlıdır."}
        ]),
        make_quiz("İdrar mikroskopisinde LÖKOSİT SİLENDİRLERİ görülmesi aşağıdaki klinik durumlardan hangisinin kesin göstergesidir?", [
            {"key": "A", "text": "Böbrek parankim hasarı ve akut pyelonefrit", "isCorrect": True, "explanation": "Ders notunda 'lökosit silendirleri böbrek hasarını gösterir' ifadesi yer almaktadır."},
            {"key": "B", "text": "Komplike olmayan izole basit üretra tahrişi", "isCorrect": False, "explanation": "Üretrada silendir oluşmaz."},
            {"key": "C", "text": "Yalnızca safra kesesi iltihabı", "isCorrect": False, "explanation": "Kolesistit idrarda lökosit silendiri yapmaz."},
            {"key": "D", "text": "Tamamen sağlıklı steril mesane", "isCorrect": False, "explanation": "Silendir patolojiktir."}
        ])
    ]
    slides.append(make_slide(76, "Lökosit Silendirleri ve Renal Parankim Hasarı", "Lökosit silendirleri, tübüler oluşum mekanizması, böbrek hasarı ve pyelonefrit kanıtı", "Laboratuvar Bulguları", s76_narrative, s76_bullets, s76_elements))

    # Slide 77: Steril Piyüri Nedenleri ve Ayırıcı Tanısı
    s77_narrative = (
        "Steril piyüri, idrar analizinde ve mikroskopisinde yoğun lökosit (piyüri pozitif) saptanmasına "
        "rağmen, standart rutin laboratuvar besiyerlerinde hiçbir bakterinin ürememesi durumudur.\n\n"
        "- **Klasik Sınav Sorusu: Tüberküloz:** Steril piyürinin tıp tarihindeki en klasik ve ünlü "
        "nedeni **ürogenital Mycobacterium tuberculosis enfeksiyonudur**; mikobakteriler standart besiyerinde üremez.\n"
        "- **Atipik ve Cinsel Yolla Bulaşan Etkenler:** Rutin kültürde üremeyen **Chlamydia trachomatis, "
        "Ureaplasma urealyticum ve Mycoplasma hominis** gibi intrasellüler mikroorganizmalar.\n"
        "- **Non-Enfeksiyöz ve İyatrojenik Nedenler:** Yakın zamanda **antibakteriyel tedavi almış olmak** "
        "(bakteri baskılanmıştır), kalıcı kateterizasyon, nefrolitiazis (taş), mesane maligniteleri ve interstisyel sistittir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Steril piyüri [piyüri (+) bakteri (-)] nedenleri: Antibakteriyel tedavi, Tbc, kateter, taş, mesane malinitesi, C. trachomatis ve zor üreyen etkenlerdir."
    )
    s77_bullets = [
        "Steril piyüri: İdrarda lökosit var (+) ancak standart kültürde bakteri üremez (-).",
        "En klasik enfeksiyöz nedenler: Mycobacterium tuberculosis ve Chlamydia trachomatis.",
        "Non-enfeksiyöz nedenler: Yakın zamanda antibiyotik kullanımı, taş, kateter ve mesane tümörü."
    ]
    s77_elements = [
        make_cloze("Steril piyürinin en klasik ve sınavda sık sorulan enfeksiyöz nedeni Mycobacterium tuberculosis enfeksiyonudur.", "Mycobacterium tuberculosis", "Tüberküloz basilinin etkeni"),
        make_table("Steril Piyüri [Piyüri (+) Kültür (-)] Nedenleri", ["Kategori", "Spesifik Klinik Neden", "Neden Üreme Olmaz?"], [
            {"cells": [{"text": "Spesifik Enfeksiyon", "isMasked": False}, {"text": "Ürogenital tüberküloz (M. tuberculosis)", "isMasked": True, "hint": "tüberküloz basili"}, {"text": "Standart kanlı agarda üremez, Löwenstein-Jensen gerekir"}]},
            {"cells": [{"text": "CYBH / Atipik", "isMasked": False}, {"text": "Chlamydia trachomatis, Ureaplasma", "isMasked": False}, {"text": "Zor üreyen intrasellüler bakterilerdir", "isMasked": True, "hint": "hücre içi bakterilerin kültürde çıkmaması"}]},
            {"cells": [{"text": "İyatrojenik / Mekanik", "isMasked": False}, {"text": "Yakın zamanda antibiyotik kullanımı, taş, tümör", "isMasked": False}, {"text": "Bakterilerin baskılanması veya yabancı cisim reaksiyonu", "isMasked": False}]}
        ]),
        make_chain("Steril Piyüri Ayırıcı Tanı Zinciri", [
            "1. Tespit: İdrar tahlilinde 50 lökosit görülür ancak kültür 48 saatte steril kalır.",
            "2. İlaç Sorgusu: Hastanın dün tek doz antibiyotik içip içmediği sorgulanır.",
            "3. Atipik Tarama: PCR ile Chlamydia ve Ureaplasma araştırılır.",
            "4. Tbc Araştırması: Sabah idrarlarında ARB (Ehrlich-Ziehl-Neelsen) ve Tbc PCR istenir."
        ]),
        make_recall("İdrarda lökosit saptanıp rutin kültürde üreme olmaması (steril piyüri) durumunda akla gelmesi gereken başlıca nedenler nelerdir?", "Yakın zamanda antibiyotik kullanımı, Mycobacterium tuberculosis, Chlamydia trachomatis, kateter, taş ve mesane malinitesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Steril Piyüri", [
            {"text": "Steril piyüri nedenleri arasında ürogenital tüberküloz yer alır.", "isLie": False, "explanation": "Doğru. En klasik nedendir."},
            {"text": "Yakın zamanda antibiyotik kullanımı idrarda bakteriyi baskılayarak steril piyüri yapabilir.", "isLie": False, "explanation": "Doğru. Çok yaygın iyatrojenik sebeptir."},
            {"text": "Steril piyüri idrarda piyürinin kesinlikle sıfır olduğu ve hastanın uzaylı olduğu durumdur.", "isLie": True, "explanation": "Tuzak! Steril piyüri piyürinin POZİTİF olduğu ancak bakterinin rutin kültürde üremediği durumdur."},
            {"text": "Taş varlığı ve mesane maligniteleri steril piyüriye yol açabilir.", "isLie": False, "explanation": "Doğru. Mekanik/malign enflamasyondur."}
        ]),
        make_quiz("İdrar mikroskopisinde bol lökosit (piyüri) saptanmasına rağmen standart idrar kültüründe üreme olmaması (steril piyüri) durumunda aşağıdakilerden hangisi ETİYOLOJİDE DÜŞÜNÜLMEZ?", [
            {"key": "A", "text": "Tipik toplum kökenli, antibiyotik almamış akut E. coli sistiti", "isCorrect": True, "explanation": "E. coli standart besiyerlerinde 24 saatte kolayca ve bolca ürer; steril piyüri yapmaz. Tbc, klamidya, taş ve önceden antibiyotik kullanımı ise steril piyüri nedenidir."},
            {"key": "B", "text": "Mycobacterium tuberculosis (renal tüberküloz)", "isCorrect": False, "explanation": "Steril piyüri nedenidir."},
            {"key": "C", "text": "Chlamydia trachomatis üretriti", "isCorrect": False, "explanation": "Steril piyüri nedenidir."},
            {"key": "D", "text": "Mesane taşı veya mesane malignitesi", "isCorrect": False, "explanation": "Steril piyüri nedenidir."}
        ])
    ]
    slides.append(make_slide(77, "Steril Piyüri Nedenleri ve Ayırıcı Tanısı", "Steril piyüri tanımı, Tbc, Chlamydia, yakın antibiyotik kullanımı, taş ve malignite", "Laboratuvar Bulguları", s77_narrative, s77_bullets, s77_elements))

    # Slide 78: İdrarda Hematüri ve Eritrosit Mikroskopisi (Dismorfik vs İzomorfik)
    s78_narrative = (
        "Üriner sistem enfeksiyonlarında mesane ve üreter mukozasındaki vasküler genişleme ve erozyon "
        "sonucu idrara eritrosit dökülmesi sık karşılaşılan bir bulgudur.\n\n"
        "- **Patolojik Eşik:** Santrifüj edilmiş idrar sedimentinde 40x büyütmede **her sahada 2 veya "
        "3'ten fazla eritrosit saptanması patolojik kabul edilmelidir**.\n"
        "- **Sistitteki Sıklık:** Semptomatik İYE olgularında hematüri sıktır; akut sistit olgularının "
        "yaklaşık **%20-25'inde çıplak gözle görülen makroskobik hematüri** gelişebilir.\n"
        "- **Morfolojik Ayrım (Dismorfik Eritrosit):** Renal parankim ve glomerüllerden sızan eritrositler "
        "tübüler ozmotik strese uğrayarak şekil bozukluğuna uğrar (**dismorfik eritrosit**); alt üriner "
        "sistemden kaynaklanan eritrositler ise normal bikonkav disk şeklini korur (izomorfik eritrosit).\n\n"
        "> [!NOTE]\n"
        "> Akut sistit olgularının 1/4'ünde makroskobik hematüri görülebilir; tek başına hematüri tanısal değildir, kadınlarda menstrüasyon kanı dışlanmalıdır."
    )
    s78_bullets = [
        "Her sahada >2-3 eritrosit görülmesi patolojik kabul edilir.",
        "Akut sistit olgularının %20-25'inde makroskobik hematüri gelişebilir.",
        "Renal parankim/glomerül kaynaklı eritrositler dismorfik (şekil bozuk) yapıdadır."
    ]
    s78_elements = [
        make_cloze("Renal parankimden kaynaklanan eritrositlerde tübüler geçişe bağlı olarak dismorfik şekil bozukluğu mevcuttur.", "dismorfik", "Böbrek kaynaklı şekli bozulmuş alyuvar"),
        make_table("Hematüri Değerlendirme Parametreleri", ["Özellik", "Eşik Değer / Durum", "Klinik Yansıması"], [
            {"cells": [{"text": "Patolojik Sınır", "isMasked": False}, {"text": "Her sahada >2 veya 3 eritrosit", "isMasked": True, "hint": "iki veya üçten fazla alyuvar"}, {"text": "Mikroskopik hematüri tanısı"}]},
            {"cells": [{"text": "Akut Sistitte Makroskopi", "isMasked": False}, {"text": "%20-25 olguda makroskobik", "isMasked": True, "hint": "vakaların beşte birinde gözle görülür"}, {"text": "Mukozal inflamatuar kanama"}]},
            {"cells": [{"text": "Renal Orijin Göstergesi", "isMasked": False}, {"text": "Dismorfik eritrosit ve akantositler", "isMasked": False}, {"text": "Parankim veya glomerüler kaynak kanıtı", "isMasked": False}]}
        ]),
        make_chain("Hematüri Değerlendirme Akışı", [
            "1. Makroskopi: İdrarın pembe, çay rengi veya kanlı olduğu görülür.",
            "2. Mikroskopik Sayım: 40x büyütmede sahada 15 eritrosit (>2-3) sayılır.",
            "3. Morfoloji Analizi: Eritrositlerin düzgün (alt sistem) veya dismorfik (böbrek) olduğu belirlenir.",
            "4. Yanıltıcı Ayrım: Kadın hastada menstrüasyon bulaşı sorgulanarak dışlanır."
        ]),
        make_recall("Akut sistit olgularının yaklaşık yüzde kaçında çıplak gözle görülen makroskobik hematüri izlenebilir?", "Yaklaşık %20-25'inde (olguların beşte birinde) izlenebilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hematüri ve Eritrosit", [
            {"text": "İdrar mikroskopisinde her sahada 2 veya 3'ten fazla eritrosit patolojiktir.", "isLie": False, "explanation": "Doğru. Mikroskopik eşiktir."},
            {"text": "Akut sistit olgularının %20-25'inde makroskobik hematüri görülebilir.", "isLie": False, "explanation": "Doğru. Sık bir bulgudur."},
            {"text": "Hematüri sadece ayağı kırılan insanlarda görülen ortopedik bir işarettir.", "isLie": True, "explanation": "Tuzak! Hematüri üriner sistemden idrara kan dökülmesidir."},
            {"text": "Renal parankimden kaynaklanan eritrositlerde dismorfik şekil bozukluğu vardır.", "isLie": False, "explanation": "Doğru. Tübüler hasar göstergesidir."}
        ]),
        make_quiz("Akut sistit olgularında çıplak gözle izlenebilen makroskobik hematüri görülme sıklığı yaklaşık yüzde kaçtır?", [
            {"key": "A", "text": "%20-25", "isCorrect": True, "explanation": "Ders notunda 'akut sistit olgularının %20-25'i makroskobiktir' ifadesi yer almaktadır."},
            {"key": "B", "text": "%99,9", "isCorrect": False, "explanation": "Aşırı yüksek orandır."},
            {"key": "C", "text": "%0,001", "isCorrect": False, "explanation": "Oldukça sıktır, bu kadar düşük olamaz."},
            {"key": "D", "text": "%100", "isCorrect": False, "explanation": "Her sistitte görülmez."}
        ])
    ]
    slides.append(make_slide(78, "İdrarda Hematüri ve Eritrosit Mikroskopisi (Dismorfik vs İzomorfik)", "Hematüri eşiği (>2-3), sistitte %20-25 makroskopi ve dismorfik eritrosit ayrımı", "Laboratuvar Bulguları", s78_narrative, s78_bullets, s78_elements))

    # Slide 79: Sekizinci Bölüm Özeti: Laboratuvar Bulguları ve Tanısal Güç
    s79_narrative = (
        "İdrar analizinin laboratuvar bileşenleri, duyarlılık ve özgüllük parametreleri ile klinik "
        "kararın en sağlam dayanağını oluşturur.\n\n"
        "- **Testlerin Tanısal Gücü:** Lökosit esteraz %83 duyarlılık / %78 özgüllük; Nitrit %53 "
        "duyarlılık / **%98 çok yüksek özgüllük** gösterir. İkisinin birlikte pozitifliği özgüllüğü katlar; "
        "**lökosit esteraz, nitrit veya mikroskopiden herhangi birinin pozitifliği ise %99,8 sensitivite sağlar**.\n"
        "- **Kardinal Kurallar:** Lökosit esteraz → Piyüriyi; Nitrit → Bakteriüriyi gösterir. "
        "Piyüri eşiği santrifüjsüz idrarda **mm³'de >10 lökosittir**.\n"
        "- **Özel Bulgular:** Lökosit silendiri böbrek parankim hasarını kanıtlar; steril piyüri tüberküloz "
        "ve antibiyotik kullanımını düşündürür; sistitte %20-25 makroskobik hematüri izlenir.\n\n"
        "> [!IMPORTANT]\n"
        "> Lökosit esteraz piyüriyi; nitrit bakteriüriyi; lökosit silendiri böbrek hasarını gösterir. Bu üçlü sınavların omurgasıdır."
    )
    s79_bullets = [
        "LE duyarlılık %83; Nitrit özgüllük %98; üçlü kombinasyon duyarlılığı %99,8.",
        "Lökosit esteraz = Piyüri; Nitrit = Bakteriüri; Lökosit silendiri = Böbrek hasarı.",
        "Piyüri: mm³'de >10 lökosit; sistitte %20-25 makroskobik hematüri görülebilir."
    ]
    s79_elements = [
        make_cloze("İdrar analizinde nitrit testinin özgüllüğü %98 gibi son derece yüksek bir seviyededir.", "%98", "Yüzde doksan sekizlik yüksek spesifite"),
        make_table("Laboratuvar Parametrelerinin Tanısal Gücü", ["Parametre", "Duyarlılık (%)", "Özgüllük (%)"], [
            {"cells": [{"text": "Lökosit Esteraz Pozitifliği", "isMasked": False}, {"text": "83", "isMasked": True, "hint": "yüzde seksen üç duyarlılık"}, {"text": "78"}]},
            {"cells": [{"text": "Nitrit Pozitifliği", "isMasked": False}, {"text": "53 (düşük)", "isMasked": False}, {"text": "98 (çok yüksek)", "isMasked": True, "hint": "yüzde doksan sekiz özgüllük"}]},
            {"cells": [{"text": "LE, Nitrit veya Mikroskobi", "isMasked": False}, {"text": "99,8 (zirve duyarlılık)", "isMasked": True, "hint": "neredeyse yüzde yüz tarama gücü"}, {"text": "70"}]}
        ]),
        make_recall("İdrar laboratuvarında lökosit esteraz, nitrit ve lökosit silendirlerinin her birinin spesifik olarak gösterdiği patolojik durumlar nelerdir?", "Lökosit esteraz piyüriyi (enflamasyonu); nitrit bakteriüriyi; lökosit silendiri ise böbrek parankim hasarını (pyelonefriti) gösterir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 8 Özeti", [
            {"text": "Lökosit esteraz piyüriyi, nitrit bakteriüriyi gösterir.", "isLie": False, "explanation": "Doğru. Temel laboratuvar kuralıdır."},
            {"text": "Nitrit testinin özgüllüğü %98 civarındadır.", "isLie": False, "explanation": "Doğru. Yalancı pozitifliği çok düşüktür."},
            {"text": "Lökosit silendirleri alt üriner sistemde sadece mesane boynunda üretilir.", "isLie": True, "explanation": "Tuzak! Silendirler yalnızca renal tübüllerde oluşur ve böbrek hasarını gösterir."},
            {"text": "Santrifüj edilmemiş idrarda mm³'de >10 lökosit piyüri kabul edilir.", "isLie": False, "explanation": "Doğru. Standart kriterdir."}
        ]),
        make_quiz("İdrar analizinde parametrelerin gösterdiği klinik durumlar ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Lökosit esteraz → Piyüri | Nitrit → Bakteriüri | Lökosit silendiri → Böbrek hasarı", "isCorrect": True, "explanation": "Ders notunda vurgulanan ve tıp sınavlarında en sık sorulan üçlü kardinal kuraldır."},
            {"key": "B", "text": "Nitrit → Piyüri | Lökosit esteraz → Bakteriüri", "isCorrect": False, "explanation": "Tam tersidir."},
            {"key": "C", "text": "Lökosit silendiri → Sadece diş eti kanaması", "isCorrect": False, "explanation": "Böbrek hasarını gösterir."},
            {"key": "D", "text": "Lökosit esteraz → İdrar dansitesi", "isCorrect": False, "explanation": "Piyüriyi gösterir."}
        ])
    ]
    slides.append(make_slide(79, "Sekizinci Bölüm Özeti: Laboratuvar Bulguları ve Tanısal Güç", "LE duyarlılığı, nitrit özgüllüğü (%98), piyüri kriterleri ve tanısal güç tablosu", "Konsolidasyon", s79_narrative, s79_bullets, s79_elements))

    # Slide 80: [TEKRAR SAYFASI - CHECKPOINT 8] Nitrit, Lökosit Esteraz ve Mikroskopi
    s80_narrative = (
        "Bu tekrar sayfasında 8. Bölümde incelenen nitrit testinin 4 saat kuralını, lökosit esterazı, "
        "piyüri kriterlerini ve mikroskopik ayırıcı tanıları konsolide ediyoruz.\n\n"
        "- **Nitrit ve 4 Saat:** Nitrat redüktaz için idrar mesanede **en az 4 saat** kalmalıdır (çocuklarda "
        "duyarsızdır). Yüksek doz C vitamini, dilüe idrar ve Gram (+) bakteriler yanlış negatiflik yapar.\n"
        "- **Lökosit Esteraz ve Piyüri:** LE piyüriyi gösterir (hücre erise bile pozitiftir). Santrifüjsüz "
        "idrarda **mm³'de >10 lökosit** piyüri tanısıdır. LE+Nitrit (+) ise güçlü İYE; ikisi (-) ise İYE'den uzaklaşılır.\n"
        "- **Kritik Mikroskopi:** İdrarda **lökosit silendiri = Böbrek hasarı**! Steril piyüri = Tbc ve "
        "antibiyotik kullanımı! Sistitte %20-25 makroskobik hematüri izlenebilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] 1) Nitrit = 4 saat kuralı! 2) LE = Piyüri (Çıkmış soru)! 3) Lökosit silendiri = Böbrek hasarı! 4) Steril piyüri = Tbc/antibiyotik! 5) Piyüri = mm³'de >10 lökosit!"
    )
    s80_bullets = [
        "Nitrit için mesanede en az 4 saat bekleme gerekir; C vitamini yalancı negatif yapar.",
        "Lökosit esteraz PİYÜRİYİ gösterir (Çıkmış Kurul 1 sorusu).",
        "Piyüri: mm³'de >10 lökosit; Lökosit silendiri = BÖBREK HASARI göstergesidir."
    ]
    s80_elements = [
        make_cloze("Kurul 1 çıkmış sorusu: İdrar analizinde piyüriyi gösteren dipstik testi lökosit esteraz testidir.", "lökosit esteraz", "İdrarda lökosit varlığını saptayan dipstik reaksiyonu"),
        make_table("8. Bölüm Büyük Tekrar Tablosu", ["Test / Bulgu", "Kardinal Tanısal Anlamı", "Kritik Sınav Uyarısı"], [
            {"cells": [{"text": "Nitrit Testi", "isMasked": False}, {"text": "Bakteriüriyi gösterir (mesanede ≥4 saat)", "isMasked": True, "hint": "dört saat mesane süresi"}, {"text": "C vitamini ve Gram (+) bakterilerde yanlış (-)"}]},
            {"cells": [{"text": "Lökosit Esteraz", "isMasked": False}, {"text": "PİYÜRİYİ gösterir (Kurul 1 çıkmış)", "isMasked": True, "hint": "piyüri tespit eden test"}, {"text": "Hücre mikroskopta parçalansa bile pozitif kalır"}]},
            {"cells": [{"text": "Lökosit Silendiri", "isMasked": False}, {"text": "BÖBREK HASARINI kanıtlar", "isMasked": False}, {"text": "Sistitte görülmez, pyelonefriti gösterir", "isMasked": True, "hint": "üst üriner tutulum kanıtı"}]},
            {"cells": [{"text": "Piyüri Eşik Değeri", "isMasked": False}, {"text": "Santrifüjsüz mm³'de >10 lökosit", "isMasked": False}, {"text": "Santrifüjlü HPF'de 5-10 lökosit", "isMasked": False}]}
        ]),
        make_chain("8. Bölüm Laboratuvar Akış Şeması", [
            "1. Dipstik İnceleme: LE (+) ise piyüri; Nitrit (+) ise bakteriüri doğrulanır.",
            "2. Mikroskopik Sayım: Hemositometrede mm³'de >10 lökosit tescillenir.",
            "3. Silendir Arama: Lökosit silendiri aranır (varsa pyelonefrit tanısı konur).",
            "4. Kültür Uyumu: Kültürde üreme yoksa steril piyüri (Tbc/antibiyotik) araştırılır."
        ]),
        make_recall("İdrar analizinde piyüriyi gösteren test ile bakteriüriyi gösteren test hangileridir?", "Piyüriyi gösteren test lökosit esteraz; bakteriüriyi gösteren test ise nitrit testidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 8. Bölüm Konsolidasyonu", [
            {"text": "İdrar analizinde lökosit esteraz piyüriyi gösterir.", "isLie": False, "explanation": "Doğru. Çıkmış sınav sorusudur."},
            {"text": "Lökosit silendirleri böbrek hasarını gösterir.", "isLie": False, "explanation": "Doğru. Pyelonefrit göstergesidir."},
            {"text": "Nitrit testi idrarda 1 saniye bile kalsa kesin pozitifleşir ve C vitamini testi bozmaz.", "isLie": True, "explanation": "Tuzak! Nitrit için mesanede en az 4 saat bekleme gerekir ve yüksek doz C vitamini yanlış negatiflik yapar."},
            {"text": "Santrifüj edilmemiş idrarda mm³'de >10 lökosit piyüri kabul edilir.", "isLie": False, "explanation": "Doğru. Standart kriterdir."}
        ]),
        make_quiz("8. Bölümün temel kazanımlarına göre aşağıdaki laboratuvar ifadelerinden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "İdrar dipstik testinde nitrit testi piyüriyi, lökosit esteraz ise kristalüriyi gösterir", "isCorrect": True, "explanation": "Kesinlikle yanlış! Lökosit esteraz piyüriyi; nitrit ise bakteriüriyi gösterir (Kurul 1 çıkmış sorusu)."},
            {"key": "B", "text": "Lökosit silendirleri böbrek hasarını ve akut pyelonefriti gösterir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Nitrit dönüşümü için bakterinin mesanede en az 4 saattir bulunuyor olması gerekir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Santrifüj edilmemiş idrarda mm³'de >10 lökosit bulunması piyüri olarak tanımlanır", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(80, "[TEKRAR SAYFASI - CHECKPOINT 8] Nitrit, Lökosit Esteraz ve Mikroskopi", "8. Bölümün kapsamlı pekiştirmesi: nitrit 4 saat kuralı, LE, piyüri tanımı ve lökosit silendiri", "Bölüm Tekrarı", s80_narrative, s80_bullets, s80_elements))

    return slides
