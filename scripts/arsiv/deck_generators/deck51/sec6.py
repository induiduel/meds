# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec6():
    slides = []

    # Slide 51: Tekrarlayan ÜSE: Relaps (Yineleme) Tanımı ve 2 Hafta Kuralı
    s51_narrative = (
        "Üriner sistem enfeksiyonunun başarılı kabul edilen bir antibiyotik tedavisi sonrasında "
        "kısa sürede yeniden alevlenmesi, relaps veya reenfeksiyon mekanizmalarına göre ayrışır.\n\n"
        "- **Relapsın Kardinal Tanımı:** ÜSE geçirmiş bir hastada, **tedavi bitimini takiben iki hafta "
        "(14 gün) içinde AYNI bakteri ile** yeniden ÜSE gelişmesidir.\n"
        "- **Etiyolojik Nedenler:** Bakterinin tam olarak eradike edilememesi (yetersiz süre veya yetersiz "
        "dozda tedavi) ya da üriner sistemde bakterilerin saklandığı kalıcı bir enfeksiyon odağının "
        "(enfekte taş, kateter, yabancı cisim, kronik bakteriyel prostatit vb.) bulunmasıdır.\n"
        "- **Klinik Anlamı:** Relaps saptanan bir hastada basit bir sistit tedavisi tekrarlanmamalı; "
        "altta yatan yapısal odak aranmalı ve tedavi süresi uzatılmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Relaps: Tedavi bitiminden sonraki 2 HAFTA içinde AYNI bakteriyle gelişen enfeksiyondur; yetersiz tedavi veya enfekte odak (taş, prostatit) göstergesidir."
    )
    s51_bullets = [
        "Tedavi bitimini takiben 2 hafta içinde AYNI bakteriyle gelişen ÜSE'dir.",
        "Temel nedeni yetersiz tedavi veya kalıcı enfekte odaktır (taş, kateter, prostatit).",
        "Basit reenfeksiyondan farklı olarak anatomik inceleme ve uzun tedavi gerektirir."
    ]
    s51_elements = [
        make_cloze("Tedavi bitiminden sonraki iki hafta içinde aynı bakteriyle gelişen enfeksiyon relaps olarak adlandırılır.", "iki hafta", "Ondört günlük relaps zaman sınırı"),
        make_table("Relapsın Temel Parametreleri", ["Ölçüt", "Relaps Kriteri", "Klinik Yansıması"], [
            {"cells": [{"text": "Zaman Sınırı", "isMasked": False}, {"text": "Tedavi bitiminden sonra ≤2 hafta", "isMasked": True, "hint": "iki haftalık süre"}, {"text": "Bakterinin vücuttan hiç atılamadığının kanıtı"}]},
            {"cells": [{"text": "Mikrobiyolojik Etken", "isMasked": False}, {"text": "Öncekiyle birebir AYNI bakteri", "isMasked": True, "hint": "etkenin değişmemesi"}, {"text": "Aynı suşun yeniden çoğalması"}]},
            {"cells": [{"text": "Altta Yatan Sebep", "isMasked": False}, {"text": "Yetersiz tedavi, enfekte taş, prostatit", "isMasked": False}, {"text": "Kalıcı rezervuar odağının temizlenmesi gerekir", "isMasked": False}]}
        ]),
        make_chain("Relapsın Oluşum Mekanizması", [
            "1. Başlangıç: Hastaya akut sistit için 3 günlük antibiyotik verilir.",
            "2. Saklanma: Bakteriler mesane taşının biyofilm tabakasına veya prostata sığınır.",
            "3. Tedavi Sonu: İlaç kesildiğinde hayatta kalan bakteriler logaritmik olarak ürer.",
            "4. Erken Nüks: 10. günde aynı E. coli ile hasta yeniden alevlenir (Relaps)."
        ]),
        make_recall("ÜSE'de relaps tanımı için gereken iki temel kriter nedir?", "Tedavi bitimini takiben iki hafta içinde gelişmesi ve öncekiyle birebir AYNI bakteri ile olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Relaps Tanımı", [
            {"text": "Relaps, tedavi bitimini takiben iki hafta içinde gelişen enfeksiyondur.", "isLie": False, "explanation": "Doğru. Zaman kriteri 2 haftadır."},
            {"text": "Relapsta üreyen mikroorganizma önceki enfeksiyondaki ile AYNI bakteridir.", "isLie": False, "explanation": "Doğru. Aynı klondur."},
            {"text": "Relaps her zaman 20 yıl sonra bambaşka yeni bir virüsle gelişen durumdur.", "isLie": True, "explanation": "Tuzak! Relaps tedavi bitiminden sonraki İLK 2 HAFTA içinde AYNI bakteriyle meydana gelir."},
            {"text": "Enfekte taş veya kronik prostatit relapsın en sık nedenlerindendir.", "isLie": False, "explanation": "Doğru. Kalıcı odaktır."}
        ]),
        make_quiz("Bir hastada geçirilmiş ÜSE tedavisinin bitiminden 10 gün sonra idrar kültüründe yine öncekiyle AYNI suş E. coli üremesi saptanıyor. Bu durum nasıl tanımlanır?", [
            {"key": "A", "text": "Relaps", "isCorrect": True, "explanation": "Tedavi bitiminden sonraki 2 hafta içinde aynı bakteriyle gelişen enfeksiyon relapstır."},
            {"key": "B", "text": "Reenfeksiyon", "isCorrect": False, "explanation": "Reenfeksiyon farklı bakteriyle veya >2 hafta sonra gelişir."},
            {"key": "C", "text": "Asemptomatik sterilizasyon", "isCorrect": False, "explanation": "Kültür pozitiftir."},
            {"key": "D", "text": "Viral reaktivasyon", "isCorrect": False, "explanation": "Etken bakteridir."}
        ])
    ]
    slides.append(make_slide(51, "Tekrarlayan ÜSE: Relaps (Yineleme) Tanımı ve 2 Hafta Kuralı", "Relaps tanımı, 2 hafta sınırı, aynı bakteri kuralı ve kalıcı enfeksiyon odakları", "Tekrarlayan ÜSE", s51_narrative, s51_bullets, s51_elements))

    # Slide 52: Reenfeksiyon Tanımı: İlk 6 Ay ve Farklı Bakteri İlkesi
    s52_narrative = (
        "Tekrarlayan üriner sistem enfeksiyonlarının ezici çoğunluğunu oluşturan klinik mekanizma "
        "relaps değil, yeni bir girişle karakterize olan reenfeksiyondur.\n\n"
        "- **Reenfeksiyonun Kardinal Tanımı:** Geçirilmiş başarılı bir ÜSE tedavisini takiben, "
        "**ilk 6 ay içerisinde FARKLI bir bakteri ya da aynı bakterinin başka bir suşu ile** "
        "yeni bir ÜSE atağının gelişmesidir.\n"
        "- **Patojenik Kaynak:** Reenfeksiyonda sorun içeride saklanan bir taş veya apse değil, dış ortamdan "
        "(genellikle hastanın fekal florasından) yeni bir bakterinin asendan yolla içeri girmesidir.\n"
        "- **Predispozan Faktörler:** Kadınlarda genetik yatkınlık (reseptör yoğunluğu), periüretral "
        "veya vajinal üropatojen kolonizasyonu, fistüller ve cinsel ilişki sıklığı rol oynar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Reenfeksiyon: Tedaviden sonraki 6 ay içinde FARKLI bir bakteri veya farklı bir suşla gelişen yeni ekzojen enfeksiyondur; tekrarların %80'den fazlasıdır."
    )
    s52_bullets = [
        "Tedaviden sonraki ilk 6 ay içinde FARKLI bir bakteri veya farklı suşla gelişir.",
        "Tekrarlayan ÜSE'lerin büyük çoğunluğunu ekzojen reenfeksiyonlar oluşturur.",
        "Vajinal/üretral kolonizasyon, genetik faktörler ve fistüller zemin hazırlar."
    ]
    s52_elements = [
        make_cloze("Geçirilmiş ÜSE'yi takiben ilk 6 ay içinde farklı bir bakteri ile gelişen yeni enfeksiyona reenfeksiyon adı verilir.", "reenfeksiyon", "Dışarıdan yeni bakteri girişiyle oluşan enfeksiyon"),
        make_table("Relaps ve Reenfeksiyon Karşılaştırması", ["Özellik", "Relaps", "Reenfeksiyon"], [
            {"cells": [{"text": "Zamanlama", "isMasked": False}, {"text": "Tedavi bitiminden sonraki 2 hafta içinde", "isMasked": True, "hint": "iki haftalık erken süre"}, {"text": "Genellikle ilk 6 ay içerisinde", "isMasked": True, "hint": "altı aylık zaman dilimi"}]},
            {"cells": [{"text": "Mikrobiyolojik Etken", "isMasked": False}, {"text": "Öncekiyle birebir AYNI bakteri", "isMasked": False}, {"text": "FARKLI bakteri veya farklı suş", "isMasked": True, "hint": "başka mikroorganizma türü"}]},
            {"cells": [{"text": "Patojenik Mekanizma", "isMasked": False}, {"text": "Kalıcı odak / yetersiz tedavi (endojen)", "isMasked": False}, {"text": "Dışarıdan yeni kolonizasyon (ekzojen)", "isMasked": False}]}
        ]),
        make_chain("Ekzojen Reenfeksiyon Basamakları", [
            "1. Tam Kür: İlk enfeksiyon antibiyotikle tamamen temizlenir ve idrar steril olur.",
            "2. Yeni Kolonizasyon: Haftalar sonra bağırsaktan yeni bir bakteri suşu perineye yerleşir.",
            "3. Asendan Giriş: Cinsel ilişki veya hijyen faktörüyle yeni suş mesaneye girer.",
            "4. Reenfeksiyon: Kültürde öncekinden farklı bir patojen ürer (ör. Klebsiella sonrası Proteus)."
        ]),
        make_recall("Reenfeksiyonu relapstan ayıran iki temel özellik nedir?", "Reenfeksiyonun tedaviden sonraki 6 ay içinde meydana gelmesi ve FARKLI bir bakteri (veya farklı suş) ile oluşmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Reenfeksiyon Tanımı", [
            {"text": "Reenfeksiyon geçirilmiş ÜSE'den sonraki ilk 6 ay içinde gelişir.", "isLie": False, "explanation": "Doğru. Tanısal süre 6 aydır."},
            {"text": "Reenfeksiyonda etken farklı bir bakteri ya da aynı bakterinin başka bir suşudur.", "isLie": False, "explanation": "Doğru. Yeni bir mikroorganizmadır."},
            {"text": "Reenfeksiyonda hastanın mesanesinde 40 yıldır hiç ölmeyen aynı bakteri yatmaktadır.", "isLie": True, "explanation": "Tuzak! Aynı bakterinin içeride saklanıp erken nüksetmesi relapstır; reenfeksiyon dışarıdan yeni girişle olur."},
            {"text": "Kadınlarda genetik faktörler ve vajinal kolonizasyon reenfeksiyonda rol oynar.", "isLie": False, "explanation": "Doğru. Ders notu bilgisi."},
        ]),
        make_quiz("Tedavisi tamamlandıktan 2 ay sonra yeni bir sistit atağı ile başvuran hastanın kültüründe ilk etkenden FARKLI bir bakteri ürüyor. Bu durum hangisidir?", [
            {"key": "A", "text": "Reenfeksiyon", "isCorrect": True, "explanation": "Farklı bir bakteri ile 6 ay içinde gelişen yeni enfeksiyon reenfeksiyondur."},
            {"key": "B", "text": "Relaps", "isCorrect": False, "explanation": "Relaps ilk 2 haftada ve aynı bakteriyle olur."},
            {"key": "C", "text": "Komplike amfizem", "isCorrect": False, "explanation": "Alakasız tanıdır."},
            {"key": "D", "text": "Kalıcı taş erüpsiyonu", "isCorrect": False, "explanation": "Taş relaps yapar, reenfeksiyon değil."}
        ])
    ]
    slides.append(make_slide(52, "Reenfeksiyon Tanımı: İlk 6 Ay ve Farklı Bakteri İlkesi", "Reenfeksiyon kriterleri, 6 ay süresi, farklı bakteri/suş ve relapstan ayrımı", "Tekrarlayan ÜSE", s52_narrative, s52_bullets, s52_elements))

    # Slide 53: Relaps Tedavisi: En Az 4 Hafta ve Odak Eradikasyonu
    s53_narrative = (
        "Relaps tablosu, bakterilerin doku derinliklerinde veya yabancı cisim üzerinde antibiyotikten "
        "kaçtığını kanıtladığı için standart 3-7 günlük tedaviler kesinlikle başarısız olur.\n\n"
        "- **Minimum Tedavi Süresi:** Relaps saptanan bir hastada antibiyograma uygun spesifik "
        "antibiyotik tedavisi **EN AZ 4 HAFTA (28 gün)** süreyle kesintisiz uygulanmalıdır.\n"
        "- **Odak Araştırması ve Cerrahi:** Relapsın altında yatan kronik bakteriyel prostatit, infekte "
        "üriner taş veya anatomik defekt mutlaka araştırılmalı; yapısal anomali varsa **antibiyotik "
        "tedavisine cerrahi müdahale eklenmelidir**.\n"
        "- **Kronik Süpresyon:** Odak çıkarılamıyorsa veya rekürrens durdurulamıyorsa düşük doz "
        "nitrofurantoin, TMP-SMX veya 10 günde bir fosfomisin ile kronik süpresyon yapılır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Relaps tedavisi en az 4 HAFTADIR; yapısal anomali (taş, prostatit) varlığında cerrahi müdahale ile kombine edilir."
    )
    s53_bullets = [
        "Relaps durumunda antibiyotik tedavi süresi EN AZ 4 HAFTADIR.",
        "Kronik prostatit veya enfekte taş varlığında cerrahi müdahale eklenir.",
        "Gerektiğinde nitrofurantoin veya fosfomisin ile kronik süpresyon verilir."
    ]
    s53_elements = [
        make_cloze("Relaps saptanan bir hastada antibiyograma uygun antibakteriyel tedavi süresi en az 4 hafta olmalıdır.", "en az 4 hafta", "Minimum yirmi sekiz günlük relaps tedavi süresi"),
        make_table("Relaps Tedavi Stratejisi", ["Aşama", "Gereken Yaklaşım", "Klinik Amaç"], [
            {"cells": [{"text": "Medikal Süre", "isMasked": False}, {"text": "En az 4 hafta kesintisiz antibiyoterapi", "isMasked": True, "hint": "minimum yirmi sekiz gün"}, {"text": "Doku derinliklerindeki bakterilerin tam eradikasyonu"}]},
            {"cells": [{"text": "Cerrahi Müdahale", "isMasked": False}, {"text": "Taş ekstraksiyonu, prostat tedavisi", "isMasked": False}, {"text": "Bakterilerin saklandığı enfekte odağın çıkarılması", "isMasked": True, "hint": "biyofilm yuvasının ameliyatla alınması"}]},
            {"cells": [{"text": "Kronik Süpresyon", "isMasked": False}, {"text": "Nitrofurantoin, TMP-SMX, Fosfomisin", "isMasked": False}, {"text": "Uzun süreli nükslerin engellenmesi", "isMasked": False}]}
        ]),
        make_chain("Relaps Yönetim Algoritması", [
            "1. Relaps Teşhisi: 2 hafta içinde aynı bakteriyle nüks teyit edilir.",
            "2. Radyolojik Tarama: Taş, divertikül veya kronik prostatit odağı tespit edilir.",
            "3. Tedavi Planı: Antibiyograma göre en az 4 haftalık tam doz ilaç başlanır.",
            "4. Cerrahi ve Süpresyon: Taş ameliyatla alınır; dirençli olguda süpresyona geçilir."
        ]),
        make_recall("Relaps saptanan bir hastada antibiyotik tedavi süresi kural olarak en az kaç hafta olmalıdır?", "En az 4 haftadır (28 gündür)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Relaps Tedavisi", [
            {"text": "Relaps tedavisinde antibiyotik süresi en az 4 haftadır.", "isLie": False, "explanation": "Doğru. Minimum 28 gün verilir."},
            {"text": "Yapısal bir anomali (taş gibi) varsa antibiyoterapiye cerrahi eklenir.", "isLie": False, "explanation": "Doğru. Odak çıkarılmalıdır."},
            {"text": "Relaps tedavisinde 1 günlük tek doz antibiyotik kesin kür sağlar.", "isLie": True, "explanation": "Tuzak! Relaps derin doku veya biyofilm enfeksiyonudur; en az 4 hafta tedavi gerektirir."},
            {"text": "Kronik süpresyonda nitrofurantoin veya fosfomisin kullanılabilir.", "isLie": False, "explanation": "Doğru. Profilaktik ajanlardır."}
        ]),
        make_quiz("Üriner sistem enfeksiyonu sonrası relaps gelişen bir hastada antibiyograma uygun antibakteriyel tedavi süresi en az ne kadar olmalıdır?", [
            {"key": "A", "text": "En az 4 hafta", "isCorrect": True, "explanation": "Ders notunda 'relaps tedavisi: nedeni yetersiz tedavi ya da yapısal bir anomali; antibiyograma uygun tedavi en az 4 hafta' olarak belirtilmiştir."},
            {"key": "B", "text": "3 gün", "isCorrect": False, "explanation": "3 gün basit sistit süresidir."},
            {"key": "C", "text": "Sadece 12 saat", "isCorrect": False, "explanation": "Tamamen yetersizdir."},
            {"key": "D", "text": "10 yıl", "isCorrect": False, "explanation": "Gereksiz aşırı süredir."}
        ])
    ]
    slides.append(make_slide(53, "Relaps Tedavisi: En Az 4 Hafta ve Odak Eradikasyonu", "Relapsta en az 4 hafta antibiyoterapi, taş/prostat cerrahisi ve kronik süpresyon", "Tekrarlayan ÜSE", s53_narrative, s53_bullets, s53_elements))

    # Slide 54: Reenfeksiyon Tedavisi ve Profilaksi İlkeleri
    s54_narrative = (
        "Reenfeksiyon tedavisinde hedef içerideki bir odağı kurutmak değil, dışarıdan bakterinin "
        "yeniden girişini engellemek ve hastanın atak sıklığına göre basamaklı tedavi uygulamaktır.\n\n"
        "- **Koitus İlişkili Reenfeksiyon:** Eğer nüksler cinsel ilişki ile tetikleniyorsa, koit sonrası "
        "miksiyon önerilir ve **ilişki sonrası tek doz post-koital profilaksi** (TMP-SMX, florokinolon "
        "veya nitrofurantoin) verilir.\n"
        "- **Yılda >3 Atak (Sık Rekürrens):** Yılda 3'ten fazla atak geçiren kadınlarda **6 ay süreyle "
        "sürekli düşük doz gece profilaksisi** uygulanır (gece 150-200 mg TMP-SMX, 50 mg nitrofurantoin "
        "veya 10 günde bir 3 g fosfomisin).\n"
        "- **Yılda <2 Atak (Seyrek Rekürrens):** Seyrek ataklarda uzun profilaksi verilmez; hastaya semptom "
        "başladığında kendi kendine uygulayacağı **3 günlük kısa süreli tedavi** reçete edilir.\n\n"
        "> [!IMPORTANT]\n"
        "> Yılda >3 atak geçiren kadınlarda 6 ay sürekli düşük doz profilaksi; yılda <2 atak geçirenlerde ise 3 günlük hasta kontrollü tedavi uygulanır."
    )
    s54_bullets = [
        "Koitus ilişkili nükslerde tek doz post-koital profilaksi verilir.",
        "Yılda >3 atak varsa 6 ay sürekli düşük doz antibiyotik profilaksisi uygulanır.",
        "Yılda <2 atak varsa hastanın kendi uyguladığı 3 günlük tedavi yeterlidir."
    ]
    s54_elements = [
        make_cloze("Yılda 3'ten fazla ÜSE atağı geçiren kadınlarda önerilen profilaksi süresi 6 ay sürekli düşük doz tedavidir.", "6 ay", "Yarım yıllık koruyucu antibiyotik rejimi"),
        make_table("Reenfeksiyon Atak Sıklığına Göre Yönetim", ["Atak Sıklığı / Tip", "Uygulanan Tedavi Şeması", "İlaç ve Doz Örneği"], [
            {"cells": [{"text": "Koitus İlişkili", "isMasked": False}, {"text": "Tek doz post-koital profilaksi", "isMasked": True, "hint": "ilişki sonrası tek tablet"}, {"text": "Koit sonrası miksiyon + TMP-SMX / Nitrofurantoin"}]},
            {"cells": [{"text": "Yılda >3 Atak", "isMasked": False}, {"text": "6 ay sürekli düşük doz profilaksi", "isMasked": True, "hint": "altı aylık gece tedavisi"}, {"text": "Gece tek doz 50 mg nitrofurantoin veya 10 günde 3 g fosfomisin"}]},
            {"cells": [{"text": "Yılda <2 Atak", "isMasked": False}, {"text": "3 günlük kendi kendini tedavi", "isMasked": False}, {"text": "Semptom başlayınca TMP-SMX veya kinolon", "isMasked": False}]}
        ]),
        make_chain("Reenfeksiyon Profilaksi Basamakları", [
            "1. Anamnez: Atakların koitus ile ilişkisi ve yıllık sayısı sorgulanır.",
            "2. Davranışsal Tedavi: Sıvı artışı ve ilişki sonrası idrar yapma anlatılır.",
            "3. Sayı Değerlendirmesi: Yılda >3 atak varsa 6 aylık düşük doz gece rejimine başlanır.",
            "4. Seyrek Nüks: Yılda <2 atak varsa evde bulunduracağı 3 günlük kutu verilir."
        ]),
        make_recall("Yılda 3'ten fazla ÜSE atağı geçiren bir kadında önerilen profilaktik tedavi süresi ne kadardır?", "6 ay süreyle sürekli düşük doz antibiyotik profilaksisidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Reenfeksiyon Profilaksisi", [
            {"text": "Koitus ilişkili reenfeksiyonlarda tek doz post-koital profilaksi verilebilir.", "isLie": False, "explanation": "Doğru. İlişki sonrası tek dozdur."},
            {"text": "Yılda >3 atak geçirenlerde 6 ay sürekli düşük doz profilaksi uygulanır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Yılda 1 kez sistit olan hastaya 25 yıl boyunca günde 4 kutu antibiyotik içirilir.", "isLie": True, "explanation": "Tuzak! Yılda <2 atak geçirenlerde uzun profilaksi verilmez, 3 günlük kendi kendine tedavi yeterlidir."},
            {"text": "Gece tek doz nitrofurantoin veya 10 günde bir fosfomisin profilakside seçilebilir.", "isLie": False, "explanation": "Doğru. Profilaksi şemalarıdır."}
        ]),
        make_quiz("Tekrarlayan ÜSE öyküsü olan ve yılda 3'ten fazla atak geçiren bir kadında önerilen profilaksi yaklaşımı hangisidir?", [
            {"key": "A", "text": "6 ay sürekli düşük doz antibiyotik profilaksisi", "isCorrect": True, "explanation": "Ders notunda 'yılda >3 atak: 6 ay sürekli düşük doz antibiyotik profilaksisi' açıkça belirtilmiştir."},
            {"key": "B", "text": "Ömür boyu hastanede yatış", "isCorrect": False, "explanation": "Yatış gerekmez."},
            {"key": "C", "text": "Mesanenin cerrahi olarak çıkarılması", "isCorrect": False, "explanation": "Endike değildir."},
            {"key": "D", "text": "Sadece 1 gün vitamin hapı verilmesi", "isCorrect": False, "explanation": "Yetersizdir."}
        ])
    ]
    slides.append(make_slide(54, "Reenfeksiyon Tedavisi ve Profilaksi İlkeleri", "Koital profilaksi, yılda >3 atakta 6 ay profilaksi ve yılda <2 atakta 3 gün rejim", "Tekrarlayan ÜSE", s54_narrative, s54_bullets, s54_elements))

    # Slide 55: Asemptomatik Bakteriüri (ASB) Tanım Kriterleri
    s55_narrative = (
        "Asemptomatik bakteriüri, idrarda yüksek miktarda bakteri bulunmasına rağmen hastada hiçbir "
        "enfeksiyon semptomunun eşlik etmediği klinik ve mikrobiyolojik bir fenomendir.\n\n"
        "- **Kardinal Tanım Kriteri:** Üriner sisteme ait hiçbir semptom veya klinik bulgusu (dizüri, "
        "pollaküri, ateş vb.) olmayan bir kişide tanı konur.\n"
        "- **İki Kültür Şartı:** Tanının kesinleşmesi için **24 saat ara ile alınan 2 ayrı temiz orta akım "
        "idrar kültüründe AYNI bakterinin en az 100.000 (10⁵) KOB/ml üretilmesi** zorunludur.\n"
        "- **Tek Kültür Tuzağı:** Tek bir kültürde üreme olması kontaminasyondan ayırt edilemeyeceği "
        "için asemptomatik bir hastada ASB tanısı için asla tek örnekle karar verilmez.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Asemptomatik bakteriüri: Semptomu olmayan hastada 24 saat ara ile alınan 2 idrar kültüründe AYNI bakterinin ≥100.000 (10⁵) KOB/ml üremesidir."
    )
    s55_bullets = [
        "Hastada dizüri, pollaküri veya ateş gibi hiçbir semptom bulunmaz.",
        "24 saat ara ile alınan 2 idrar kültüründe AYNI bakteri üremelidir.",
        "Kültürde tanısal eşik değer ≥100.000 (10⁵) KOB/ml bakteri sayısıdır."
    ]
    s55_elements = [
        make_cloze("Asemptomatik bakteriüri tanısı için 24 saat ara ile alınan 2 idrar kültüründe aynı bakterinin 100.000 KOB/ml üremesi gerekir.", "100.000 KOB/ml", "On üzeri beş koloni oluşturan birim eşiği"),
        make_table("Asemptomatik Bakteriüri Tanı Kriterleri", ["Kriter Bileşeni", "Gereken Şart", "Tanısal Amacı"], [
            {"cells": [{"text": "Klinik Durum", "isMasked": False}, {"text": "Üriner semptom veya bulgu YOKTUR", "isMasked": True, "hint": "hastanın yakınmasız olması"}, {"text": "Sistit ve pyelonefritin dışlanması"}]},
            {"cells": [{"text": "Örnekleme Zamanı", "isMasked": False}, {"text": "24 saat ara ile alınan 2 ayrı kültür", "isMasked": True, "hint": "bir gün arayla çift kültür"}, {"text": "Geçici kontaminasyonun ekarte edilmesi"}]},
            {"cells": [{"text": "Kantitatif Üreme", "isMasked": False}, {"text": "Aynı bakterinin ≥10⁵ (100.000) KOB/ml", "isMasked": False}, {"text": "Gerçek mesane kolonizasyonunun kanıtlanması", "isMasked": False}]}
        ]),
        make_chain("ASB Tanısal Doğrulama Zinciri", [
            "1. Tarama: Şikayeti olmayan gebeden rutin idrar kültürü istenir.",
            "2. İlk Sonuç: Kültürde 10⁵ KOB/ml E. coli ürer.",
            "3. Doğrulama: 24 saat sonra ikinci temiz orta akım kültürü gönderilir.",
            "4. ASB Tanısı: İkinci kültürde de aynı E. coli ≥10⁵ KOB/ml ürerse tanı kesinleşir."
        ]),
        make_recall("Asemptomatik bakteriüri tanısı koyabilmek için gereken kültür sayısı, zaman aralığı ve koloni eşiği nedir?", "24 saat ara ile alınan 2 idrar kültüründe aynı bakterinin ≥100.000 (10⁵) KOB/ml üremesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ASB Tanımı", [
            {"text": "ASB tanısında hastada hiçbir üriner semptom bulunmaz.", "isLie": False, "explanation": "Doğru. Asemptomatiktir."},
            {"text": "24 saat ara ile alınan 2 idrar kültüründe aynı bakterinin üremesi gerekir.", "isLie": False, "explanation": "Doğru. Çift kültür kuralıdır."},
            {"text": "ASB tanısı için idrarda sadece 1 adet bakteri görülmesi ve hastanın kıvranması şarttır.", "isLie": True, "explanation": "Tuzak! ASB'de hasta kıvranmaz (semptomsuzdur) ve kültürde ≥100.000 KOB/ml üreme aranır."},
            {"text": "Tanısal koloni eşiği 100.000 (10⁵) KOB/ml'dir.", "isLie": False, "explanation": "Doğru. Kantitatif sınır 10⁵'tir."}
        ]),
        make_quiz("Asemptomatik bakteriüri tanımı aşağıdakilerden hangisinde eksiksiz ve doğru olarak verilmiştir?", [
            {"key": "A", "text": "Semptomu olmayan hastada 24 saat ara ile alınan 2 idrar kültüründe aynı bakterinin 100.000 KOB/ml üretilmesi", "isCorrect": True, "explanation": "Ders notundaki birebir resmi tanı kriteridir."},
            {"key": "B", "text": "Şiddetli böğür ağrısı olan hastada 1 adet lökosit görülmesi", "isCorrect": False, "explanation": "Asemptomatik değildir."},
            {"key": "C", "text": "Tek bir kültürde 10 koloni virüs üremesi", "isCorrect": False, "explanation": "Bakteri 10⁵ olmalıdır."},
            {"key": "D", "text": "Her idrar tahlilinde kesinlikle kan bulunması", "isCorrect": False, "explanation": "Hematüri tanımıdır."}
        ])
    ]
    slides.append(make_slide(55, "Asemptomatik Bakteriüri (ASB) Tanım Kriterleri", "ASB tanımı, 24 saat arayla 2 kültür kuralı ve 100.000 KOB/ml eşiği", "Asemptomatik Bakteriüri", s55_narrative, s55_bullets, s55_elements))

    # Slide 56: Asemptomatik Bakteriüride Genel İlke: Tedavi Edilmez!
    s56_narrative = (
        "Modern enfeksiyon hastalıkları ve üroloji kılavuzlarının en katı ilkelerinden biri, semptomu "
        "olmayan bir hastada sırf idrarda bakteri ürüyor diye antibiyotik başlanmaması kuralıdır.\n\n"
        "- **Tedavi Edilmeme İlkesi:** Genel kural olarak **asemptomatik bakteriüri TEDAVİ EDİLMEZ**.\n"
        "- **Gereksiz Tedavinin Zararları:** Semptomsuz hastaya antibiyotik verilmesi bakteriyi kalıcı "
        "olarak temizlemez; aksine florayı bozarak çok ilaca dirençli (ÇİD) mikroorganizmaların "
        "seçilmesine ve Clostridioides difficile kolitine yol açar.\n"
        "- **Organ Nakli İstisnası:** Böbrek nakli veya diğer solid organ nakli yapılmış hastalarda "
        "dahi asemptomatik bakteriüri taraması veya tedavisi kılavuzlarca önerilmemektedir.\n\n"
        "> [!IMPORTANT]\n"
        "> Asemptomatik bakteriüri toplumda sık görülen selim bir kolonizasyondur; özel endikasyonlar haricinde antibiyotik verilmesi kesinlikle yanlıştır."
    )
    s56_bullets = [
        "Genel kural olarak asemptomatik bakteriüri tedavi edilmez.",
        "Gereksiz antibiyotik kullanımı dirençli suşların seçilmesine yol açar.",
        "Böbrek veya solid organ nakilli hastalarda rutin tarama ve tedavi önerilmez."
    ]
    s56_elements = [
        make_cloze("Enfeksiyon kılavuzlarının temel ilkesine göre genel kural olarak asemptomatik bakteriüri tedavi edilmez.", "tedavi edilmez", "Antibiyotik vermeme yaklaşımı"),
        make_table("ASB'de Tedavisiz İzlem Mantığı", ["Parametre", "Antibiyotik Verilirse", "Tedavisiz Bırakılırsa"], [
            {"cells": [{"text": "Bakteriyel Direnç", "isMasked": False}, {"text": "GSBL ve çoklu dirençli suşlar gelişir", "isMasked": True, "hint": "antibiyotiğe direnç kazanma"}, {"text": "Direnç gelişimi önlenir"}]},
            {"cells": [{"text": "Klinik Fayda", "isMasked": False}, {"text": "Semptom olmadığı için klinik fayda sıfırdır", "isMasked": False}, {"text": "Konak-bakteri dengesi korunur", "isMasked": True, "hint": "doğal dengenin sürmesi"}]},
            {"cells": [{"text": "Organ Nakli Durumu", "isMasked": False}, {"text": "Tarama ve tedavi önerilmez", "isMasked": False}, {"text": "Graft fonksiyonuna katkısı yoktur", "isMasked": False}]}
        ]),
        make_chain("Gereksiz Antibiyotik Hasar Zinciri", [
            "1. Hatalı Karar: Asemptomatik yaşlı hastaya idrarda bakteri var diye sefalosporin başlanır.",
            "2. Flora Kaybı: Bağırsak ve vajinadaki koruyucu laktobasiller ve flora silinir.",
            "3. Süperenfeksiyon: Boşalan alana dirençli Pseudomonas veya C. difficile yerleşir.",
            "4. Klinik Ağırlaşma: Hasta gereksiz tedavi yüzünden dirençli ürosepsis veya kolit yaşar."
        ]),
        make_recall("Genel popülasyonda asemptomatik bakteriüri saptandığında temel tıbbi yaklaşım nedir?", "Genel kural olarak tedavi edilmez (antibiyotik verilmez)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ASB Tedavi İlkesi", [
            {"text": "Genel kural olarak asemptomatik bakteriüri tedavi edilmez.", "isLie": False, "explanation": "Doğru. Temel kılavuz ilkesidir."},
            {"text": "Böbrek nakli yapılmış kişilerde ASB taraması veya tedavisi önerilmemektedir.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "İdrarında semptomsuz bakteri üreyen her insana derhal 1 yıl damardan ilaç verilmelidir.", "isLie": True, "explanation": "Tuzak! Asemptomatik bakteriüri genel kural olarak tedavi edilmez; gereksiz antibiyotik direnç doğurur."},
            {"text": "Gereksiz tedavi dirençli bakterilerin seçilmesine yol açar.", "isLie": False, "explanation": "Doğru. Ekolojik yan hasar oluşur."}
        ]),
        make_quiz("Asemptomatik bakteriüri saptanan genel bir hastada antibiyotik tedavisi ile ilgili temel kural hangisidir?", [
            {"key": "A", "text": "Asemptomatik bakteriüri genel kural olarak tedavi edilmez", "isCorrect": True, "explanation": "Ders notunda 'Asemptomatik bakteriüri tedavi edilmez' ilkesi açıkça vurgulanmıştır."},
            {"key": "B", "text": "Tüm hastalara derhal 3 farklı antibiyotik başlanmalıdır", "isCorrect": False, "explanation": "Kesinlikle yanlıştır."},
            {"key": "C", "text": "Böbrekler hemen ameliyatla alınmalıdır", "isCorrect": False, "explanation": "Tıbbi endikasyon yoktur."},
            {"key": "D", "text": "Sadece her gün 10 litre gazoz içirilir", "isCorrect": False, "explanation": "Tıbbi tedavi değildir."}
        ])
    ]
    slides.append(make_slide(56, "Asemptomatik Bakteriüride Genel İlke: Tedavi Edilmez!", "ASB genel tedavi edilmeme kuralı, direnç gelişimi ve organ naklindeki yaklaşım", "Asemptomatik Bakteriüri", s56_narrative, s56_bullets, s56_elements))

    # Slide 57: ASB'nin İki Mutlak Tedavi Endikasyonu: Gebeler ve İnvaziv Girişimler
    s57_narrative = (
        "Asemptomatik bakteriürinin tedavi edilmeme kuralının tıpta KESİN ve TARTIŞMASIZ iki "
        "hayati istisnası bulunmaktadır.\n\n"
        "- **1. Hamile Kadınlar (Gebeler):** Gebelikte tedavi edilmeyen ASB vakalarının %30-40'ı "
        "gebelik ilerledikçe ağır akut pyelonefrite dönüşür; bu durum erken doğum (preterm eylem), "
        "düşük doğum ağırlığı ve perinatal mortalite riskini katlar. Bu nedenle gebelerde ASB **mutlaka taranır ve tedavi edilir**.\n"
        "- **2. Ürolojik İnvaziv Girişim Planlanan Hastalar:** Mukozal kanama veya hasar riski taşıyan "
        "ürolojik cerrahi (TUR, biyopsi vb.) yapılacak hastalarda bakteriüri kana karışarak fatal sepsise yol açar; **işlem öncesi tedavi zorunludur**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Asemptomatik bakteriürinin MUTLAK tedavi edildiği iki durum: 1) GEBELER, 2) Genitoüriner sisteme İNVAZİV GİRİŞİM yapılacak hastalardır!"
    )
    s57_bullets = [
        "ASB SADECE gebelerde ve invaziv ürolojik girişim yapılacaklarda tedavi edilir.",
        "Gebelikte tedavi edilmezse %40 pyelonefrit ve erken doğum riski doğurur.",
        "İnvaziv ürolojik girişimde bakteriyemi ve sepsisi önlemek için tedavi şarttır."
    ]
    s57_elements = [
        make_cloze("Asemptomatik bakteriürinin kesin olarak tedavi edilmesi gereken en önemli hasta grubu gebeler ve invaziv cerrahi yapılacaklardır.", "gebeler", "Hamile kadın popülasyonu"),
        make_table("ASB Mutlak Tedavi Endikasyonları", ["Hasta Grubu", "Tedavi Edilmeme Riski", "Tedavi Protokolü"], [
            {"cells": [{"text": "Hamile Kadınlar (Gebeler)", "isMasked": False}, {"text": "%30-40 akut pyelonefrit, erken doğum", "isMasked": True, "hint": "gebelikte böbrek enfeksiyonu ve prematüre"}, {"text": "3 gün uygun antibiyotik + kültür takibi"}]},
            {"cells": [{"text": "İnvaziv Ürolojik Girişim", "isMasked": False}, {"text": "İşlem sırasında bakteriyemi ve septik şok", "isMasked": False}, {"text": "Girişimden önce idrarın sterilizasyonu", "isMasked": True, "hint": "cerrahi öncesi bakterinin temizlenmesi"}]}
        ]),
        make_chain("Gebelikte ASB Tedavi Gerekçesi", [
            "1. Tarama: Gebeliğin ilk vizitinde rutin idrar kültürü alınır.",
            "2. Sessiz Kolonizasyon: Gebe asemptomatiktir ancak kültürde 10⁵ E. coli ürer.",
            "3. Progesteron Genişlemesi: Tedavi edilmezse bakteriler gevşek üreterden hızla böbreğe çıkar.",
            "4. Koruma: 3 günlük antibiyotik ile pyelonefrit ve erken doğum engellenir."
        ]),
        make_recall("Asemptomatik bakteriürinin kesin olarak tedavi edilmesi gereken iki hasta grubu hangisidir?", "1) Gebe kadınlar, 2) Genitoüriner sisteme mukozal invaziv girişim yapılacak hastalardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ASB Tedavi Endikasyonları", [
            {"text": "Sadece gebeler ve genitoüriner invaziv girişim yapılacak hastalar tedavi edilir.", "isLie": False, "explanation": "Doğru. İki mutlak endikasyondur."},
            {"text": "Gebelikte tedavi edilmeyen ASB pyelonefrite ve erken doğuma yol açabilir.", "isLie": False, "explanation": "Doğru. %40 pyelonefrit riski vardır."},
            {"text": "Gebelikte idrarda bakteri çıksa bile asla ilaç verilmez ve hasta evine yollanır.", "isLie": True, "explanation": "Tuzak! Gebelik ASB'nin mutlak tedavi endikasyonudur; tedavi edilmezse anne ve bebek hayatı riske girer."},
            {"text": "İnvaziv ürolojik girişim öncesi bakteriüri tedavi edilmezse ürosepsis gelişebilir.", "isLie": False, "explanation": "Doğru. Mukozal kanamada bakteriyemi olur."}
        ]),
        make_quiz("Asemptomatik bakteriürinin kesinlikle taranması ve antibiyotikle tedavi edilmesi gereken İKİ klinik durum hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Gebeler ve genitoüriner sisteme invaziv girişim yapılacak hastalar", "isCorrect": True, "explanation": "Ders notunda 'Sadece gebeler ve genitoüriner sisteme invaziv girişim yapılacak hastalar tedavi edilir' kuralı yer almaktadır."},
            {"key": "B", "text": "Tüm sağlıklı üniversite öğrencileri ve sporcular", "isCorrect": False, "explanation": "Tedavi endikasyonu yoktur."},
            {"key": "C", "text": "Sadece nezle olan çocuklar", "isCorrect": False, "explanation": "Üriner endikasyon değildir."},
            {"key": "D", "text": "Hiçbir insan grubu tedavi edilmez", "isCorrect": False, "explanation": "Gebeler ve cerrahi mutlak istisnadır."}
        ])
    ]
    slides.append(make_slide(57, "ASB'nin İki Mutlak Tedavi Endikasyonu: Gebeler ve İnvaziv Girişimler", "Gebelerde ASB ve pyelonefrit riski, invaziv cerrahi öncesi sterilizasyon", "Asemptomatik Bakteriüri", s57_narrative, s57_bullets, s57_elements))

    # Slide 58: Gebelikte ASB Yönetimi ve Takip Protokolü
    s58_narrative = (
        "Gebelikte asemptomatik bakteriüri saptandığında hem fetusun güvenliği hem de maternal kür "
        "için özelleşmiş bir tedavi ve izlem algoritması yürütülür.\n\n"
        "- **Tedavi Süresi ve İlaç Seçimi:** Kültürde üreyen mikroorganizmanın antibiyogramına uygun "
        "gebelikte güvenli bir antibiyotik (beta-laktamlar, fosfomisin vb.) **3 gün süreyle** verilir.\n"
        "- **Kürün Doğrulanması:** Tedavi bitiminden **7-14 gün sonra kontrol idrar kültürü** alınır; "
        "kültür steril ise tam kür kabul edilir.\n"
        "- **Gebelikte Rutin İzlem:** Tedavi edilmiş gebelerde her kadın doğum vizitinde kontrol idrar "
        "kültürü tekrarlanır; doğum sonrası ise **post-partum 4-6. haftaya kadar** takip sürdürülür.\n\n"
        "> [!IMPORTANT]\n"
        "> Gebelerde ASB tedavisi 3 gündür; tedaviden 7-14 gün sonra kontrol kültürü alınır ve post-partum 4-6. haftaya kadar izlenir."
    )
    s58_bullets = [
        "Gebelikte kültür duyarlılığına göre 3 gün antibiyotik verilir.",
        "Tedaviden 7-14 gün sonra kontrol kültürü ile kür teyit edilir.",
        "Takip gebelik boyunca vizitlerde ve doğum sonrası 4-6. haftaya kadar sürer."
    ]
    s58_elements = [
        make_cloze("Gebelikte ASB tedavisinden 7-14 gün sonra kür kontrolü için kontrol idrar kültürü alınmalıdır.", "kontrol idrar kültürü", "Bakterinin temizlendiğini gösteren laboratuvar ekimi"),
        make_table("Gebelikte ASB Takip Protokolü", ["Zaman Dilimi", "Yapılacak İşlem", "Klinik Değerlendirme"], [
            {"cells": [{"text": "Tedavi Aşaması", "isMasked": False}, {"text": "3 gün uygun antibiyotik", "isMasked": True, "hint": "üç günlük güvenli tedavi"}, {"text": "Gebelikte güvenli beta-laktam veya fosfomisin"}]},
            {"cells": [{"text": "Tedaviden 7-14 Gün Sonra", "isMasked": False}, {"text": "Kontrol idrar kültürü", "isMasked": False}, {"text": "Steril ise kür; üreme varsa relaps/yetersiz tedavi", "isMasked": True, "hint": "başarılı sonuç veya nüks ayrımı"}]},
            {"cells": [{"text": "Doğum Sonrası Dönem", "isMasked": False}, {"text": "Post-partum 4-6. haftaya kadar izlem", "isMasked": True, "hint": "lohusalık sonu kontrolü"}, {"text": "Gereğinde doğum sonrası USG ve radyografi"}]}
        ]),
        make_chain("Gebelikte ASB Protokol Akışı", [
            "1. Tarama: ASB tespit edilir.",
            "2. 3 Günlük Tedavi: Fetus için güvenli antibiyotik verilir.",
            "3. 7-14. Gün Kültürü: İdrar ekilir; steril ise kür tescillenir.",
            "4. Postpartum Takip: Doğumdan sonra 4-6. haftaya kadar anne izlenir."
        ]),
        make_recall("Gebelikte ASB tedavisinden ne kadar süre sonra kontrol idrar kültürü alınarak kür teyit edilmelidir?", "Tedavi bitiminden 7 ila 14 gün sonra kontrol kültürü alınmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Gebelikte ASB", [
            {"text": "Gebelikte ASB için 3 gün antibiyotik tedavisi verilir.", "isLie": False, "explanation": "Doğru. Standart rejimdir."},
            {"text": "Tedaviden 7-14 gün sonra idrar kültürü ile izlem yapılır.", "isLie": False, "explanation": "Doğru. Kür kontrolüdür."},
            {"text": "Gebelikte ASB olan anneye 9 ay boyunca her gün damardan 10 şişe kolistin verilir.", "isLie": True, "explanation": "Tuzak! Gebelikte güvenli ilaçlarla 3 günlük kısa tedavi verilir ve kültürle izlenir."},
            {"text": "Post-partum 4-6. haftaya kadar hasta izlenmeye devam edilir.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("Gebelikte asemptomatik bakteriüri tedavisi sonrası kürün değerlendirilmesi için kontrol idrar kültürü ne zaman alınmalıdır?", [
            {"key": "A", "text": "Tedaviden 7-14 gün sonra", "isCorrect": True, "explanation": "Ders notunda '3 gün tedavi; 7-14 gün sonra idrar kültürü ile izlem' açıkça belirtilmiştir."},
            {"key": "B", "text": "İlk hapı yuttuktan 5 saniye sonra", "isCorrect": False, "explanation": "İmkansızdır."},
            {"key": "C", "text": "Tam 20 yıl sonra", "isCorrect": False, "explanation": "Geçersiz süredir."},
            {"key": "D", "text": "Hiçbir zaman kültür alınmaz", "isCorrect": False, "explanation": "Kültür takibi zorunludur."}
        ])
    ]
    slides.append(make_slide(58, "Gebelikte ASB Yönetimi ve Takip Protokolü", "Gebelikte 3 gün tedavi, 7-14 gün sonra kontrol kültürü ve postpartum 4-6 hafta izlem", "Asemptomatik Bakteriüri", s58_narrative, s58_bullets, s58_elements))

    # Slide 59: Altıncı Bölüm Özeti: Tekrarlayan ÜSE ve ASB Ayrımı
    s59_narrative = (
        "Tekrarlayan üriner enfeksiyonların ve asemptomatik bakteriürinin doğru yönetimi, hastayı "
        "gereksiz antibiyotik toksisitesinden korurken gerçek patolojileri eradike etmeyi sağlar.\n\n"
        "- **Relaps vs Reenfeksiyon:** Relaps tedavi bitiminden sonraki **2 hafta içinde AYNI bakteriyle** "
        "(en az 4 hafta tedavi + cerrahi); reenfeksiyon ise **ilk 6 ayda FARKLI bakteriyle** (profilaksi) gelişir.\n"
        "- **Profilaksi Ayrımı:** Koital nükste tek doz post-koital ilaç; yılda >3 atakta 6 ay sürekli "
        "düşük doz profilaksi; yılda <2 atakta ise 3 günlük hasta kontrollü tedavi uygulanır.\n"
        "- **ASB Kuralları:** 24 saat arayla 2 kültürde ≥10⁵ KOB/ml ile tanı konur; genel olarak tedavi "
        "edilmez; ancak **gebeler ve invaziv cerrahi planlananlar mutlak tedavi edilir**.\n\n"
        "> [!IMPORTANT]\n"
        "> Relapsta süre en az 4 hafta; gebelikte ASB süresi 3 gün; sık reenfeksiyonda profilaksi süresi 6 aydır."
    )
    s59_bullets = [
        "Relaps: ≤2 hafta + AYNI bakteri | Reenfeksiyon: ≤6 ay + FARKLI bakteri.",
        "Relaps tedavisi en az 4 haftadır; reenfeksiyonda (>3 atak) 6 ay profilaksi uygulanır.",
        "ASB çift kültürle tanınır; yalnız GEBELER ve İNVAZİV GİRİŞİMLER tedavi edilir."
    ]
    s59_elements = [
        make_cloze("Relaps tedavisinde süre en az 4 hafta iken sık tekrarlayan reenfeksiyonda profilaksi süresi 6 aydır.", "6 aydır", "Yarım yıllık profilaktik süre"),
        make_table("Bölüm 6 Kardinal Süre ve Kriter Özeti", ["Klinik Tablo", "Zaman Kriteri", "Tedavi / Girişim Yaklaşımı"], [
            {"cells": [{"text": "Relaps", "isMasked": False}, {"text": "≤2 hafta içinde AYNI bakteri", "isMasked": True, "hint": "iki hafta ve aynı suş"}, {"text": "En az 4 hafta antibiyoterapi + cerrahi odak"}]},
            {"cells": [{"text": "Reenfeksiyon (>3 atak)", "isMasked": False}, {"text": "≤6 ay içinde FARKLI bakteri", "isMasked": False}, {"text": "6 ay sürekli düşük doz gece profilaksisi", "isMasked": True, "hint": "altı aylık koruyucu tedavi"}]},
            {"cells": [{"text": "Gebelikte ASB", "isMasked": False}, {"text": "24 saat arayla 2 kültürde ≥10⁵", "isMasked": False}, {"text": "3 gün güvenli tedavi + 7-14. gün kontrolü", "isMasked": False}]}
        ]),
        make_recall("Relaps ile reenfeksiyonun tanısal zaman sınırları ve etken özellikleri nasıldır?", "Relaps: Tedaviden sonraki 2 hafta içinde AYNI bakteri; Reenfeksiyon: Tedaviden sonraki 6 ay içinde FARKLI bakteri (veya farklı suş)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 6 Özeti", [
            {"text": "Relaps tedavisinde antibiyotik süresi en az 4 haftadır.", "isLie": False, "explanation": "Doğru. Minimum 28 gündür."},
            {"text": "Yılda >3 atak geçirenlerde 6 ay sürekli düşük doz profilaksi önerilir.", "isLie": False, "explanation": "Doğru. Uzun dönem profilaksidir."},
            {"text": "Asemptomatik bakteriüri tüm insanlarda kesinlikle 5 yıl boyunca damardan tedavi edilir.", "isLie": True, "explanation": "Tuzak! ASB genel kural olarak tedavi edilmez; sadece gebeler ve invaziv cerrahi yapılacaklar tedavi edilir."},
            {"text": "Gebelikte ASB tedavisinden 7-14 gün sonra kontrol kültürü alınır.", "isLie": False, "explanation": "Doğru. Kür kontrolüdür."}
        ]),
        make_quiz("Aşağıdaki klinik durum ve tedavi süresi eşleştirmelerinden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Relaps tedavisi — En az 4 hafta", "isCorrect": True, "explanation": "Ders notunda relaps tedavisinin en az 4 hafta olduğu açıkça belirtilmiştir."},
            {"key": "B", "text": "Relaps tedavisi — Sadece 1 gün", "isCorrect": False, "explanation": "Yetersizdir."},
            {"key": "C", "text": "Gebelikte ASB tedavisi — Kesintisiz 9 yıl", "isCorrect": False, "explanation": "Gebelikte 3 gün tedavi verilir."},
            {"key": "D", "text": "Sık reenfeksiyon profilaksisi — 10 saniye", "isCorrect": False, "explanation": "6 aydır."}
        ])
    ]
    slides.append(make_slide(59, "Altıncı Bölüm Özeti: Tekrarlayan ÜSE ve ASB Ayrımı", "Relaps, reenfeksiyon, profilaksi rejimleri, ASB tanı kriterleri ve gebelik yönetimi", "Konsolidasyon", s59_narrative, s59_bullets, s59_elements))

    # Slide 60: [TEKRAR SAYFASI - CHECKPOINT 6] Tekrarlayan ÜSE ve Asemptomatik Bakteriüri
    s60_narrative = (
        "Bu tekrar sayfasında 6. Bölümde işlenen relaps, reenfeksiyon, profilaksi prensipleri ve "
        "asemptomatik bakteriürinin tanı ve tedavi kurallarını konsolide ediyoruz.\n\n"
        "- **Relaps vs Reenfeksiyon:** Tedaviden sonraki 2 hafta içinde AYNI bakteriyle nüks = **Relaps** "
        "(en az 4 hafta tedavi + cerrahi odak kontrolü). İlk 6 ayda FARKLI bakteriyle nüks = **Reenfeksiyon**.\n"
        "- **Profilaksi Algoritması:** Koitus ilişkiliyse post-koital tek doz; yılda >3 atakta 6 ay "
        "düşük doz profilaksi; yılda <2 atakta ise 3 günlük hasta kontrollü tedavi.\n"
        "- **ASB Kardinal Kuralları:** Semptomsuz hastada 24 saat arayla 2 kültürde ≥10⁵ KOB/ml ile tanı konur. "
        "Genel kural olarak **tedavi edilmez**. Yalnızca **gebeler (3 gün tedavi + 7-14 gün kontrol)** ve "
        "**invaziv ürolojik girişim planlananlar** mutlak tedavi edilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Relaps = 2 hafta + Aynı bakteri + 4 hafta tedavi! Reenfeksiyon = 6 ay + Farklı bakteri! ASB = Tedavi edilmez; istisna GEBELER ve İNVAZİV GİRİŞİMDİR!"
    )
    s60_bullets = [
        "Relaps (≤2 hafta, aynı bakteri) en az 4 hafta tedavi gerektirir.",
        "Reenfeksiyonda yılda >3 atakta 6 ay düşük doz profilaksi verilir.",
        "ASB genel kural olarak tedavi edilmez; yalnız GEBELER ve İNVAZİV GİRİŞİM tedavi edilir."
    ]
    s60_elements = [
        make_cloze("Asemptomatik bakteriüride tedavi verilmesi zorunlu olan iki gruptan biri gebeler diğeri invaziv girişim yapılacak hastalardır.", "invaziv girişim", "Cerrahi ve aletli mukozal müdahale"),
        make_table("6. Bölüm Büyük Tekrar Tablosu", ["Konu / Tablo", "Tanısal Kriter", "Kritik Klinik İlke"], [
            {"cells": [{"text": "Relaps", "isMasked": False}, {"text": "≤2 hafta içinde AYNI bakteri", "isMasked": True, "hint": "iki haftalık aynı suş"}, {"text": "En az 4 hafta tedavi + cerrahi odak temizliği"}]},
            {"cells": [{"text": "Reenfeksiyon", "isMasked": False}, {"text": "≤6 ay içinde FARKLI bakteri", "isMasked": False}, {"text": ">3 atakta 6 ay sürekli düşük doz profilaksi", "isMasked": True, "hint": "yarım yıllık koruyucu antibiyotik"}]},
            {"cells": [{"text": "ASB Tanısı", "isMasked": False}, {"text": "24 saat arayla 2 kültürde ≥10⁵", "isMasked": True, "hint": "çift kültürde yüz bin koloni"}, {"text": "Semptomsuz hastada tek kültür yetersizdir"}]},
            {"cells": [{"text": "ASB Tedavisi", "isMasked": False}, {"text": "Genel kural: TEDAVİ EDİLMEZ", "isMasked": False}, {"text": "Mutlak istisna: GEBELER ve İNVAZİV GİRİŞİM", "isMasked": True, "hint": "iki zorunlu tedavi grubu"}]}
        ]),
        make_chain("6. Bölüm Entegre Karar Şeması", [
            "1. Hasta Değerlendirmesi: Semptomsuz hastada kültürde bakteri saptanır.",
            "2. ASB Doğrulaması: 24 saat sonra 2. kültür alınır; aynı bakteri ≥10⁵ ürerse ASB denir.",
            "3. Endikasyon Kontrolü: Hasta gebe mi veya cerrahiye girecek mi? Hayırsa tedavi verilmez.",
            "4. Gebe ise: 3 gün güvenli ilaç verilir, 7-14. gün kontrol kültürüyle kür tescillenir."
        ]),
        make_recall("Tekrarlayan ÜSE'de relaps için önerilen antibiyotik tedavi süresi ile sık reenfeksiyonda önerilen profilaksi süresi nedir?", "Relaps tedavisi en az 4 hafta; sık reenfeksiyonda (>3 atak/yıl) profilaksi süresi ise 6 aydır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 6. Bölüm Konsolidasyonu", [
            {"text": "Relaps, tedavi bitimini takiben iki hafta içinde AYNI bakteri ile nüksetmedir.", "isLie": False, "explanation": "Doğru. Tanım kuralıdır."},
            {"text": "Reenfeksiyon genellikle ilk 6 ayda FARKLI bir bakteri ile meydana gelir.", "isLie": False, "explanation": "Doğru. Ekzojen yeni enfeksiyondur."},
            {"text": "Gebelikte saptanan asemptomatik bakteriüri asla tedavi edilmez ve anneye antibiyotik yasaktır.", "isLie": True, "explanation": "Tuzak! Gebelik ASB'nin MUTLAK tedavi endikasyonudur; tedavi edilmezse %40 pyelonefrit ve erken doğum yapar."},
            {"text": "Genel popülasyonda asemptomatik bakteriüri tedavi edilmez.", "isLie": False, "explanation": "Doğru. Genel kuraldır."}
        ]),
        make_quiz("6. Bölümün temel kazanımlarına göre aşağıdaki klinik ifadelerden hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Gebelikte saptanan asemptomatik bakteriüri hiçbir zaman tedavi edilmez", "isCorrect": True, "explanation": "Kesinlikle yanlış! Gebeler, ASB'nin kesinlikle tedavi edilmesi gereken iki mutlak grubundan birincisidir."},
            {"key": "B", "text": "Relaps saptanan bir hastada antibiyotik tedavisi en az 4 hafta sürdürülmelidir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Reenfeksiyon tedavisinde yılda >3 atak varsa 6 ay profilaksi önerilir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "ASB tanısı için 24 saat arayla alınan 2 kültürde ≥10⁵ KOB/ml aynı bakteri üremelidir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(60, "[TEKRAR SAYFASI - CHECKPOINT 6] Tekrarlayan ÜSE ve Asemptomatik Bakteriüri", "6. Bölümün kapsamlı pekiştirmesi: relaps vs reenfeksiyon, profilaksi ve ASB mutlak endikasyonları", "Bölüm Tekrarı", s60_narrative, s60_bullets, s60_elements))

    return slides
