# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec1():
    slides = []

    # Slide 1: Üriner Sistem Enfeksiyonu (ÜSE) Temel Tanımı
    s1_narrative = (
        "Üriner sistem enfeksiyonu (ÜSE), üriner traktusun herhangi bir anatomik dokusunun "
        "bakteriyel invazyonu ile tetiklenen geniş klinik spektrumlu bir tablodur.\n\n"
        "- **Enflamasyon Birlikteliği:** ÜSE yalnızca steril idrarda mikroorganizma bulunması değil, "
        "etkilenen konakta **enflamatuar reaksiyonla birlikte idrarda bakteri bulunması** şeklinde tanımlanır.\n"
        "- **Klinik Spektrum:** Tablo tamamen sessiz seyreden asemptomatik bakteriüriden, ürosepsise "
        "ve septik şoka kadar uzanan ağır sistemik tabloları içerir.\n"
        "- **Hücresel Yanıt:** Ürotelyumun bakteriyel antijenlerle uyarılması lokal sitokin salınımına "
        "ve idrara polimorfonükleer lökositlerin (piyüri) dökülmesine yol açar.\n\n"
        "> [!NOTE]\n"
        "> Gerçek bir üriner enfeksiyon için idrarda üropatojen varlığına mutlaka konak dokusunun enflamatuar yanıtı eşlik etmelidir."
    )
    s1_bullets = [
        "Üriner traktusun bakteriyel invazyonu ile gelişen enfeksiyondur.",
        "İdrarda bakteri varlığına enflamatuar reaksiyon eşlik eder.",
        "Klinik tablo asemptomatik bakteriüriden sepsise kadar uzanır."
    ]
    s1_elements = [
        make_cloze("Üriner sistem enfeksiyonu, etkilenen konakta enflamatuar reaksiyonla birlikte idrarda bakteri bulunmasıdır.", "enflamatuar reaksiyonla", "Lökosit göçü ve hücresel doku yanıtı süreci"),
        make_table("ÜSE Tanımının Temel Bileşenleri", ["Bileşen", "Biyolojik Anlamı", "Klinik Yansıması"], [
            {"cells": [{"text": "Bakteriyel Varlık", "isMasked": False}, {"text": "Üropatojen mikroorganizma kolonizasyonu", "isMasked": True, "hint": "idrarda mikrop çoğalması"}, {"text": "Kültürde koloni oluşumu"}]},
            {"cells": [{"text": "Konak Enflamasyonu", "isMasked": False}, {"text": "Ürotelyal lökosit göçü ve sitokin yanıtı", "isMasked": False}, {"text": "İdrar analizinde piyüri saptanması", "isMasked": True, "hint": "idrarda akyuvar bulunması"}]}
        ]),
        make_chain("Üriner Enfeksiyon Patogenez Başlangıcı", [
            "1. Kolonizasyon: Bakteriler periüretral alanda çoğalır.",
            "2. Mukozal Temas: Ürotelyum yüzey reseptörlerine tutunma gerçekleşir.",
            "3. Enflamatuar Sinyal: Konak hücrelerinden sitokin ve kemokinler salınır.",
            "4. Piyüri Oluşumu: Polimorfonükleer lökositler idrar lümenine göç eder."
        ]),
        make_recall("Üriner sistem enfeksiyonunun tıbbi tanımında yer alan iki temel unsur nedir?", "İdrarda üropatojen bakteri bulunması ve buna eşlik eden konak dokusunun enflamatuar reaksiyonudur (piyüri)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ÜSE Temel Tanımı", [
            {"text": "ÜSE, idrarda bakteri ile birlikte konak enflamatuar reaksiyonunu içerir.", "isLie": False, "explanation": "Doğru. Tanımın temeli bakteri + enflamasyondur."},
            {"text": "Klinik spektrum asemptomatik bakteriüriden ürosepsise kadar uzanabilir.", "isLie": False, "explanation": "Doğru. Çok geniş bir klinik skala gösterir."},
            {"text": "ÜSE tanısı için idrarda sadece lökosit olması yeterlidir, bakteri üremesi asla aranmaz.", "isLie": True, "explanation": "Tuzak! ÜSE bakteriyel bir enfeksiyondur; mikrobiyal etkenin varlığı tanımın ayrılmaz parçasıdır."},
            {"text": "Ürotelyumun bakteriyel uyarısı lökositlerin idrara dökülmesini tetikler.", "isLie": False, "explanation": "Doğru. Enflamasyon piyüri oluşturur."}
        ]),
        make_quiz("Üriner sistem enfeksiyonunun (ÜSE) temel tıbbi tanımı aşağıdakilerden hangisinde eksiksiz olarak verilmiştir?", [
            {"key": "A", "text": "Etkilenen konakta enflamatuar reaksiyonla birlikte idrarda bakteri bulunması", "isCorrect": True, "explanation": "Ders notundaki resmi tanım tam olarak bakteri varlığı ve konak enflamatuar reaksiyonunun birlikteliğidir."},
            {"key": "B", "text": "Yalnızca böbrek parankiminde kalsiyum oksalat taşlarının birikmesi", "isCorrect": False, "explanation": "Bu nefrolitiazistir."},
            {"key": "C", "text": "Mesane mukozasının enflamasyon olmaksızın sadece gerilmesi", "isCorrect": False, "explanation": "Enflamatuar reaksiyon şarttır."},
            {"key": "D", "text": "Glomerüllerde immün kompleks birikimine bağlı non-bakteriyel hematüri", "isCorrect": False, "explanation": "Bu glomerülonefrittir."}
        ])
    ]
    slides.append(make_slide(1, "Üriner Sistem Enfeksiyonu (ÜSE) Temel Tanımı", "ÜSE'nin patofizyolojik tanımı, enflamatuar reaksiyon ve klinik spektrumu", "Genel Üroloji ve Enfeksiyon", s1_narrative, s1_bullets, s1_elements))

    # Slide 2: Epidemiyolojik İstatistikler ve Sağlık Sistemi Yükü
    s2_narrative = (
        "Üriner sistem enfeksiyonları, toplumda insanların doktora ve polikliniklere en sık başvuru "
        "gereksinimi yaratan primer bakteriyel enfeksiyonların başında gelir.\n\n"
        "- **Başvuru Sayıları:** Yalnızca ABD'de her yıl 7 milyondan fazla ÜSE vakası görülmekte olup "
        "hastaların yaklaşık **%21'i doğrudan acil servislere** başvurmaktadır.\n"
        "- **Hastaneye Yatış Oranı:** Akut pyelonefrit komplikasyonu nedeniyle yılda 100.000'in üzerinde "
        "hasta hastaneye yatırılarak parenteral tedaviye alınmaktadır.\n"
        "- **Ekonomik Maliyet:** İş gücü kaybı, tanısal tetkikler ve antibiyotik harcamaları ile birlikte "
        "ÜSE'lerin yıllık doğrudan ve dolaylı maliyeti **1 milyar doların üzerindedir**.\n\n"
        "> [!NOTE]\n"
        "> ÜSE polikliniklerde en sık reçete yazılan ve acil servislere yüksek oranda başvuruya neden olan bakteriyel enfeksiyondur."
    )
    s2_bullets = [
        "Doktora en sık başvuru nedeni olan bakteriyel enfeksiyon grubudur.",
        "ABD'de yıllık >7 milyon vaka görülür; %21'i acil servise başvurur.",
        "Pyelonefrit nedeniyle yılda 100.000'den fazla yatış ve >1 milyar dolar maliyet yaratır."
    ]
    s2_elements = [
        make_cloze("ABD'de her yıl görülen 7 milyondan fazla ÜSE vakasının yaklaşık %21'i acil servislere başvurmaktadır.", "%21'i", "Yüzde yirmi birlik akut başvuru oranı"),
        make_table("ÜSE Epidemiyolojik İstatistikleri", ["Metrik", "Sayısal Değer", "Klinik Önemi"], [
            {"cells": [{"text": "Yıllık ABD Vaka Sayısı", "isMasked": False}, {"text": ">7 milyon vaka", "isMasked": True, "hint": "yedi milyonu aşan olgu"}, {"text": "Toplumda yaygın görülme"}]},
            {"cells": [{"text": "Pyelonefrit Yatış Sayısı", "isMasked": False}, {"text": ">100.000 hasta/yıl", "isMasked": False}, {"text": "Parenteral tedavi gereksinimi", "isMasked": True, "hint": "damar içi tedavi zorunluluğu"}]}
        ]),
        make_recall("ÜSE neden sağlık ekonomisi ve acil servisler için bu denli büyük bir yük oluşturur?", "Yılda milyonlarca başvuru oluşturması (%21 acil servis), pyelonefritte 100.000'i aşan yatış gerektirmesi ve milyar doları aşan maliyetidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ÜSE Epidemiyolojisi", [
            {"text": "ÜSE, hekime en sık başvuru gereksinimi yaratan bakteriyel enfeksiyonlardandır.", "isLie": False, "explanation": "Doğru. Toplumda son derece yaygındır."},
            {"text": "Vakaların yaklaşık %21'i acil servislere başvurur.", "isLie": False, "explanation": "Doğru. İstatistiksel veridir."},
            {"text": "ÜSE son derece nadir bir hastalık olup yılda tüm dünyada sadece 50 vaka bildirilir.", "isLie": True, "explanation": "Tuzak! Yalnızca ABD'de yılda 7 milyondan fazla vaka görülmektedir."},
            {"text": "Akut pyelonefrit nedeniyle yılda yüz binden fazla hasta yatarak tedavi edilir.", "isLie": False, "explanation": "Doğru. Ağır vakalarda hastane yatışı gerekir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarının epidemiyolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "ABD'de yılda 7 milyondan fazla vaka görülür ve %21'i acil servise başvurur", "isCorrect": True, "explanation": "Ders notu verilerine göre >7 milyon vaka ve %21 acil başvuru mevcuttur."},
            {"key": "B", "text": "Hastalık hiçbir zaman hastaneye yatış gerektirmez, tamamen ayaktan tedavi edilir", "isCorrect": False, "explanation": "Yılda >100.000 pyelonefrit hastası yatırılmaktadır."},
            {"key": "C", "text": "Tüm dünyada toplam yıllık maliyeti 100 Türk lirasını geçmez", "isCorrect": False, "explanation": "Maliyeti 1 milyar doların üzerindedir."},
            {"key": "D", "text": "Yalnızca yoğun bakım ünitelerinde görülen bir hastane enfeksiyonudur", "isCorrect": False, "explanation": "Toplum kökenli vakalar büyük çoğunluktadır."}
        ])
    ]
    slides.append(make_slide(2, "Epidemiyolojik İstatistikler ve Sağlık Sistemi Yükü", "ÜSE görülme sıklığı, acil servis başvuruları ve ekonomik maliyeti", "Epidemiyoloji", s2_narrative, s2_bullets, s2_elements))

    # Slide 3: Cinsiyet Dağılımı ve Kadın Baskınlığı
    s3_narrative = (
        "Üriner sistem enfeksiyonları bütün yaş gruplarında görülebilmekle beraber, yenidoğan dönemi "
        "ve ileri yaşlılık hariç tutulduğunda **esas olarak kadınları etkileyen** bir hastalıktır.\n\n"
        "- **Kadın Oranı:** Klinik olarak ÜSE tanısı alan hastaların **%67,5'inin kadın olduğu** "
        "kanıtlanmıştır.\n"
        "- **Yaşam Boyu Risk:** Kadınların yaklaşık **%50'si (yarısı)** yaşamları boyunca en az bir kez "
        "semptomatik ÜSE atağı geçirmektedir.\n"
        "- **İkinci Atak Dinamiği:** Bir kez ÜSE geçiren bir kadında ikinci kez enfeksiyon geçirme riski, "
        "hiç geçirmemiş olanlara kıyasla çok daha yüksektir.\n\n"
        "> [!IMPORTANT]\n"
        "> Reprodüktif çağda ÜSE belirgin şekilde kadın hastalığıdır; her iki kadından biri hayatında en az bir kez sistit atağı yaşar."
    )
    s3_bullets = [
        "Yenidoğan ve ileri yaş hariç ÜSE esas olarak kadınları etkiler.",
        "ÜSE tanısı alan hastaların %67,5'i kadındır.",
        "Kadınların %50'si yaşam boyu en az bir kez ÜSE atağı geçirir."
    ]
    s3_elements = [
        make_cloze("Üriner sistem enfeksiyonu tanısı alan tüm hastaların yaklaşık %67,5'i kadındır.", "%67,5'i", "Yüzde altmış yedi buçukluk kadın oranı"),
        make_table("Cinsiyete Göre Yaşam Boyu ÜSE Riski", ["Parametre", "Kadınlarda Durum", "Erkeklerde Durum"], [
            {"cells": [{"text": "Yaşam Boyu Geçirme Oranı", "isMasked": False}, {"text": "%50 (her iki kadından biri)", "isMasked": True, "hint": "yarı yarıya görülme sıklığı"}, {"text": "Gençlikte %1'in altında"}]},
            {"cells": [{"text": "Toplam ÜSE Olgularındaki Pay", "isMasked": False}, {"text": "%67,5 kadın baskınlığı", "isMasked": False}, {"text": "%32,5 erkek payı", "isMasked": True, "hint": "erkek hasta oranı"}]}
        ]),
        make_recall("Kadınların yaşam boyu en az bir kez ÜSE geçirme olasılığı yaklaşık yüzde kaçtır?", "Yaklaşık %50'dir (kadınların yarısı yaşamları boyunca en az bir kez ÜSE geçirir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Cinsiyet Dağılımı", [
            {"text": "Yenidoğan ve ileri yaş hariç ÜSE esas olarak kadınları etkiler.", "isLie": False, "explanation": "Doğru. Kadınlarda belirgin sıktır."},
            {"text": "Kadınların yaklaşık %50'si yaşamları boyunca en az bir kez ÜSE geçirir.", "isLie": False, "explanation": "Doğru. Yaşam boyu risk %50'dir."},
            {"text": "ÜSE geçiren hastaların %99'u erkektir, kadınlarda bu hastalık imkansızdır.", "isLie": True, "explanation": "Tuzak! Hastaların %67,5'i kadındır; kadınlarda erkeklere göre çok daha yaygındır."},
            {"text": "Bir kez ÜSE geçiren kadında ikinci atak geçirme riski artar.", "isLie": False, "explanation": "Doğru. Geçirilmiş ÜSE rekürrens için risk faktörüdür."}
        ]),
        make_quiz("ÜSE tanısı alan hastaların cinsiyet dağılımı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Hastaların %67,5'i kadındır ve kadınların %50'si yaşam boyu en az bir kez ÜSE geçirir", "isCorrect": True, "explanation": "Ders notu istatistiklerine göre %67,5 kadın ve %50 yaşam boyu risk mevcuttur."},
            {"key": "B", "text": "Erkeklerde kadınlardan 20 kat daha sık görülür", "isCorrect": False, "explanation": "Tam tersine kadınlarda çok daha sıktır."},
            {"key": "C", "text": "Kadınlarda sadece menopozdan sonra görülür, genç kadınlarda hiç görülmez", "isCorrect": False, "explanation": "Genç cinsel aktif kadınlarda pik yapar."},
            {"key": "D", "text": "İki cinsiyette de yaşam boyu risk %0,01'dir", "isCorrect": False, "explanation": "Kadınlarda %50'dir."}
        ])
    ]
    slides.append(make_slide(3, "Cinsiyet Dağılımı ve Kadın Baskınlığı", "ÜSE'de kadın cinsiyet baskınlığı, %67,5 oranı ve yaşam boyu risk", "Epidemiyoloji", s3_narrative, s3_bullets, s3_elements))

    # Slide 4: Genç Erkeklerde Düşük İnsidans ve Koruyucu Mekanizmalar
    s4_narrative = (
        "Sağlıklı genç ve orta yaşlı erkeklerde üriner sistem anatomisi ve biyokimyası, enfeksiyonlara "
        "karşı son derece güçlü doğal bir bariyer oluşturur.\n\n"
        "- **Düşük İnsidans:** 1 ile 50 yaş arasındaki erkeklerde ÜSE görülme sıklığı **%1'in altındadır**.\n"
        "- **Üretra Uzunluğu:** Erkek üretrasının kadınlara kıyasla belirgin şekilde uzun olması (yaklaşık 20 cm), "
        "bakterilerin mesaneye asendan göçünü fiziksel olarak engeller.\n"
        "- **Bakterisidal Prostat Sıvısı:** Prostat bezinden salgılanan çinko ve antibakteriyel peptidlerden "
        "zengin sekresyonlar, üretral lümene giren mikroorganizmaları kimyasal olarak yok eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] 1-50 yaş arası erkeklerde ÜSE insidansı <%1'dir; koruyucu mekanizmalar uzun üretra ve bakterisidal prostat salgısıdır."
    )
    s4_bullets = [
        "1-50 yaş arası erkeklerde ÜSE görülme sıklığı %1'in altındadır.",
        "Uzun üretra anatomisi bakterilerin asendan tırmanışını engeller.",
        "Prostat sıvısı güçlü bakterisidal antibakteriyel özellik taşır."
    ]
    s4_elements = [
        make_cloze("1-50 yaş arası erkeklerde ÜSE insidansı uzun üretra ve prostat sıvısı sayesinde %1'in altındadır.", "%1'in altındadır", "Yüzde birden küçük olma durumu"),
        make_table("Erkeklerde Doğal Koruyucu Mekanizmalar", ["Koruyucu Faktör", "Mekanizma", "Biyolojik Sonuç"], [
            {"cells": [{"text": "Uzun Üretra", "isMasked": False}, {"text": "Mesaneye olan fiziksel mesafenin uzunluğu", "isMasked": True, "hint": "anatomik uzaklık bariyeri"}, {"text": "Asendan bakteriyel tırmanışın engellenmesi"}]},
            {"cells": [{"text": "Prostat Sıvısı", "isMasked": False}, {"text": "Çinko ve antibakteriyel peptidler", "isMasked": False}, {"text": "Bakterisidal kimyasal sterilizasyon", "isMasked": True, "hint": "mikropları öldürücü kimyasal etki"}]}
        ]),
        make_chain("Erkek Üretra Savunma Zinciri", [
            "1. Giriş: Bakteri eksternal meatusa temas eder.",
            "2. Fiziksel Engel: Yaklaşık 20 cm'lik uzun üretra yolu boyunca ilerlemesi gerekir.",
            "3. Kimyasal Temas: Prostat sıvısındaki çinko ve bakterisidal proteinlerle karşılaşır.",
            "4. Lizis: Bakteriler mesaneye ulaşamadan parçalanır ve <%1 insidans korunur."
        ]),
        make_recall("1-50 yaş arasındaki erkeklerde ÜSE görülme sıklığı neden %1'in altındadır?", "Üretrasının uzun olması ve prostat sıvısının bakterisidal (antibakteriyel) özelliği sayesindedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Genç Erkek Savunması", [
            {"text": "1-50 yaş arasındaki erkeklerde ÜSE görülme sıklığı %1'in altındadır.", "isLie": False, "explanation": "Doğru. Bu yaş grubunda son derece nadirdir."},
            {"text": "Erkek üretrasının uzun olması bakterilerin mesaneye ulaşmasını zorlaştırır.", "isLie": False, "explanation": "Doğru. Önemli bir mekanik bariyerdir."},
            {"text": "Prostat sıvısı bakteriler için mükemmel bir besiyeridir ve çoğalmalarını uyarır.", "isLie": True, "explanation": "Tuzak! Prostat sıvısı besiyeri değil, bakterisidal (bakteri öldürücü) özelliğe sahip koruyucu bir salgıdır."},
            {"text": "Genç erkekte ÜSE saptandığında altta yatan anomali araştırılmalıdır.", "isLie": False, "explanation": "Doğru. Nadir olduğu için komplike kabul edilir."}
        ]),
        make_quiz("1-50 yaş arası erkeklerde ÜSE insidansının <%1 olmasını sağlayan temel koruyucu faktörler hangileridir?", [
            {"key": "A", "text": "Üretranın uzun olması ve prostat sıvısının bakterisidal özelliği", "isCorrect": True, "explanation": "Ders notunda belirtilen iki kardinal savunma mekanizmasıdır."},
            {"key": "B", "text": "Mesanede sürekli yüksek oranda glukoz bulunması", "isCorrect": False, "explanation": "Glukozüri enfeksiyon riskini artırır."},
            {"key": "C", "text": "Erkeklerin hiç idrar yapmaması", "isCorrect": False, "explanation": "İdrar akımı koruyucudur."},
            {"key": "D", "text": "Testosteronun doğrudan bakterileri fagositoz etmesi", "isCorrect": False, "explanation": "Hormon fagositoz yapmaz."}
        ])
    ]
    slides.append(make_slide(4, "Genç Erkeklerde Düşük İnsidans ve Koruyucu Mekanizmalar", "1-50 yaş arası erkekte <%1 sıklık, uzun üretra ve bakterisidal prostat salgısı", "Anatomi ve Fizyoloji", s4_narrative, s4_bullets, s4_elements))

    # Slide 5: Yineleyen ÜSE Dinamikleri ve Kadınlarda Rekürrens
    s5_narrative = (
        "Üriner sistem enfeksiyonları tek bir atakla sonlanabildiği gibi, özellikle kadınlarda "
        "sık tekrarlayan kronik bir problem haline dönüşebilir.\n\n"
        "- **Yineleyen ÜSE Oranı:** ÜSE geçiren kadınların **%10-20'sinde yineleyen (rekürren) ÜSE** "
        "tablosu gelişmektedir.\n"
        "- **Erken Dönem Rekürrens:** İlk ÜSE atağını takiben ilk 6 ay içerisinde kadınların yaklaşık "
        "**dörtte birinde (1/4) ikinci atak**, %3'ünde ise üçüncü atak gelişme riski mevcuttur.\n"
        "- **Oluşum Şekli:** Bu tekrarlamaların büyük çoğunluğu dış ortamdan yeni bir bakterinin girmesiyle "
        "oluşan **ekzojen reenfeksiyon** şeklindedir; nadiren kalıcı bir odaktan kaynaklanan relapstır.\n\n"
        "> [!NOTE]\n"
        "> İlk sistit atağından sonraki 6 ay kadınlarda en kırılgan dönemdir; hastaların 1/4'ü bu sürede yeniden enfekte olur."
    )
    s5_bullets = [
        "Kadınların %10-20'sinde yineleyen ÜSE gelişir.",
        "İlk ÜSE'den sonraki 6 ayda kadınların 1/4'ünde 2. atak, %3'ünde 3. atak görülür.",
        "Yinelemeler çoğunlukla ekzojen reenfeksiyon şeklinde meydana gelir."
    ]
    s5_elements = [
        make_cloze("İlk ÜSE atağını takiben 6 ay içinde kadınların yaklaşık dörtte birinde (1/4) ikinci atak gelişir.", "dörtte birinde", "Yüzde 25'lik ikinci atak oranı"),
        make_table("Kadınlarda Rekürrens İstatistikleri", ["Zaman Dilimi", "Tekrarlama Oranı", "Klinik Özellik"], [
            {"cells": [{"text": "Genel Kadın Popülasyonu", "isMasked": False}, {"text": "%10-20 yineleyen ÜSE", "isMasked": True, "hint": "kronik tekrarlama yüzdesi"}, {"text": "Uzun süreli takip gerektirir"}]},
            {"cells": [{"text": "İlk Ataktan Sonraki 6 Ay", "isMasked": False}, {"text": "1/4 hastada 2. atak, %3'te 3. atak", "isMasked": False}, {"text": "Çoğunlukla ekzojen reenfeksiyon", "isMasked": True, "hint": "dışarıdan yeni bakteri girişi"}]}
        ]),
        make_recall("İlk ÜSE atağını geçiren bir kadında sonraki 6 ay içinde ikinci atak gelişme olasılığı yaklaşık kaçtır?", "Yaklaşık 1/4'tür (%25 oranında ikinci atak görülür)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Rekürren ÜSE", [
            {"text": "Yineleyen ÜSE kadınların %10-20'sini etkiler.", "isLie": False, "explanation": "Doğru. Ders notu istatistiğidir."},
            {"text": "İlk ÜSE'den sonraki 6 ayda kadınların yaklaşık 1/4'ünde ikinci atak gelişebilir.", "isLie": False, "explanation": "Doğru. Erken nüks sıktır."},
            {"text": "Bir kez ÜSE geçiren kadın ömür boyu tam bağışık kalır ve bir daha asla ÜSE geçirmez.", "isLie": True, "explanation": "Tuzak! ÜSE kalıcı koruyucu bağışıklık bırakmaz; tersine geçirilmiş ÜSE yeni ataklar için risk faktörüdür."},
            {"text": "Tekrarlamalar çoğunlukla ekzojen reenfeksiyon mekanizması ile meydana gelir.", "isLie": False, "explanation": "Doğru. Dışarıdan yeni suş girişi esastır."}
        ]),
        make_quiz("İlk kez ÜSE atağı geçiren bir kadında sonraki 6 ay içinde 2. atak gelişme riski nedir?", [
            {"key": "A", "text": "Yaklaşık dörtte bir (1/4)", "isCorrect": True, "explanation": "Ders notunda açıkça kadınların 1/4'ünde 6 ay içinde ikinci atak geliştiği belirtilmiştir."},
            {"key": "B", "text": "Yüzde sıfır (tam bağışıklık gelişir)", "isCorrect": False, "explanation": "ÜSE kalıcı bağışıklık bırakmaz."},
            {"key": "C", "text": "Yalnızca milyonda bir", "isCorrect": False, "explanation": "Oldukça yüksek oranda nükseder."},
            {"key": "D", "text": "%100 (tüm kadınlar kesinlikle her ay geçirir)", "isCorrect": False, "explanation": "Oran 1/4'tür."}
        ])
    ]
    slides.append(make_slide(5, "Yineleyen ÜSE Dinamikleri ve Kadınlarda Rekürrens", "Kadınlarda %10-20 yineleyen ÜSE, 6 ay içinde 1/4 ikinci atak riski", "Epidemiyoloji", s5_narrative, s5_bullets, s5_elements))

    # Slide 6: Yaşam Dönemlerine Göre Prevalans: Neonatal ve Çocukluk
    s6_narrative = (
        "Üriner sistem enfeksiyonlarının insidansı ve cinsiyet dağılımı, bireyin yaşam dönemlerine "
        "ve üriner sistemin anatomik olgunlaşmasına göre belirgin farklılıklar gösterir.\n\n"
        "- **Neonatal Dönem (Yenidoğan):** Prevalans yaklaşık **%1 civarındadır**. Bu dönemde konjenital "
        "ürolojik anomalilerin sık olması nedeniyle erkek/kadın oranı **1,5 / 1 ile erkek lehinedir**.\n"
        "- **Okul Öncesi Dönem:** Prevalans %2-3 seviyesine yükselir ve tuvalet eğitimi ile birlikte "
        "kız çocuklarında baskınlık başlar.\n"
        "- **Okul Dönemi:** Görülme sıklığı **%1-2 civarındadır**; yine anatomik yatkınlık nedeniyle "
        "kız çocuklarında erkeklere göre belirgin olarak daha sıktır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Neonatal dönem, ÜSE'nin erkeklerde kızlardan daha sık görüldüğü (E/K: 1,5/1) TEK yaşam dönemidir; konjenital anomaliler rol oynar."
    )
    s6_bullets = [
        "Neonatal dönemde prevalans %1'dir ve E/K oranı 1,5 / 1 ile erkek baskındır.",
        "Okul öncesi dönemde prevalans %2-3 seviyesindedir.",
        "Okul döneminde prevalans %1-2 olup kız çocuklarında daha sıktır."
    ]
    s6_elements = [
        make_cloze("Neonatal dönemde ÜSE prevalansı %1 olup erkek/kadın oranı 1,5 / 1 ile erkek lehinedir.", "1,5 / 1", "Yenidoğanda erkek baskınlığını gösteren oran"),
        make_table("Çocukluk Yaşam Dönemlerinde ÜSE Prevalansı", ["Yaşam Dönemi", "Prevalans", "Cinsiyet Özelliği"], [
            {"cells": [{"text": "Neonatal (Yenidoğan)", "isMasked": False}, {"text": "%1", "isMasked": True, "hint": "yüzde bir prevalans"}, {"text": "Erkek / Kadın: 1,5 / 1 (erkek baskın)"}]},
            {"cells": [{"text": "Okul Öncesi", "isMasked": False}, {"text": "%2-3", "isMasked": False}, {"text": "Kız çocuklarında artış başlar", "isMasked": True, "hint": "tuvalet eğitimi ve kısa üretra"}]},
            {"cells": [{"text": "Okul Dönemi", "isMasked": False}, {"text": "%1-2", "isMasked": False}, {"text": "Kız çocuklarında daha sık", "isMasked": False}]}
        ]),
        make_recall("Neonatal dönemde ÜSE cinsiyet dağılımının erişkinden temel farkı nedir?", "Neonatal dönemde erkeklerde kızlardan daha sıktır (E/K oranı 1,5 / 1); erişkinde ise kadınlar belirgin baskındır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Çocukluk Çağı Prevalansı", [
            {"text": "Neonatal dönemde ÜSE prevalansı yaklaşık %1'dir.", "isLie": False, "explanation": "Doğru. Yenidoğan prevalansıdır."},
            {"text": "Neonatal dönemde erkek/kadın oranı 1,5 / 1'dir.", "isLie": False, "explanation": "Doğru. Erkeklerde daha sık görüldüğü istisnai dönemdir."},
            {"text": "Okul öncesi dönemde ÜSE prevalansı %95'e ulaşır ve tüm çocuklar enfektedir.", "isLie": True, "explanation": "Tuzak! Okul öncesi dönemde prevalans yalnızca %2-3'tür."},
            {"text": "Okul döneminde prevalans %1-2 civarındadır.", "isLie": False, "explanation": "Doğru. Ders notu tablosu verisidir."}
        ]),
        make_quiz("Neonatal dönemde ÜSE görülme sıklığı ve cinsiyet oranı aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Prevalans %1, Erkek / Kadın oranı 1,5 / 1", "isCorrect": True, "explanation": "Ders notu tablosunda neonatal prevalans %1 ve E/K oranı 1,5 / 1 olarak belirtilmiştir."},
            {"key": "B", "text": "Prevalans %50, Erkek / Kadın oranı 1 / 100", "isCorrect": False, "explanation": "Yenidoğanda oran bu değildir."},
            {"key": "C", "text": "Prevalans %10, sadece kız bebeklerde görülür", "isCorrect": False, "explanation": "Yenidoğanda erkeklerde daha sıktır."},
            {"key": "D", "text": "Prevalans %0, neonatal dönemde ÜSE gelişemez", "isCorrect": False, "explanation": "Yenidoğanda %1 oranında görülür."}
        ])
    ]
    slides.append(make_slide(6, "Yaşam Dönemlerine Göre Prevalans: Neonatal ve Çocukluk", "Neonatal %1 ve E/K 1,5/1, okul öncesi %2-3, okul çağı %1-2 dinamikleri", "Epidemiyoloji", s6_narrative, s6_bullets, s6_elements))

    # Slide 7: Yaşam Dönemlerine Göre Prevalans: Erişkin ve Geriatrik Dönem
    s7_narrative = (
        "Yaşın ilerlemesi, hormonal değişiklikler ve komorbiditelerin eklenmesi ile ÜSE prevalansı "
        "yaşamın ileri evrelerinde dramatik bir artış gösterir.\n\n"
        "- **Reprodüktif Dönem:** Doğurganlık çağındaki genç erişkin popülasyonda ÜSE prevalansı "
        "ortalama **%2,5 seviyesindedir** (kadınlarda cinsel aktiviteye bağlı olarak daha yüksektir).\n"
        "- **65-70 Yaş Dönemi:** Yaşlılıkla birlikte prevalans **%20'ye fırlar**. Bu dönemde kadınlarda "
        "östrojen kaybı, erkeklerde ise benign prostat hiperplazisi (BPH) nedeniyle cinsiyet farkı kapanır (E/K: 1/1).\n"
        "- **Hastanede Yatan Hastalar:** Üretral kateterizasyon ve girişimler nedeniyle yatan hastalarda "
        "prevalans **%30 gibi devasa bir düzeye** ulaşır.\n\n"
        "> [!NOTE]\n"
        "> Yaşlılıkta erkeklerde prostat büyümesi idrar stazı yaratarak ÜSE sıklığını kadın seviyesine çıkarır."
    )
    s7_bullets = [
        "Reprodüktif dönemde toplum prevalansı ortalama %2,5'tir.",
        "65-70 yaş grubunda prevalans %20'ye yükselir ve cinsiyet farkı kapanır.",
        "Hastanede yatan hastalarda prevalans %30 seviyesine ulaşır."
    ]
    s7_elements = [
        make_cloze("65-70 yaş grubundaki geriatrik popülasyonda ÜSE prevalansı yaklaşık %20 seviyesine yükselmektedir.", "%20", "Yüzde yirmilik geriatrik prevalans"),
        make_table("İleri Yaş ve Hastane Ortamında ÜSE Prevalansı", ["Grup", "Prevalans", "Altta Yatan Temel Faktör"], [
            {"cells": [{"text": "Reprodüktif Dönem", "isMasked": False}, {"text": "%2,5", "isMasked": True, "hint": "genç erişkin prevalansı"}, {"text": "Cinsel aktivite ve hormonal denge"}]},
            {"cells": [{"text": "65-70 Yaşları", "isMasked": False}, {"text": "%20", "isMasked": False}, {"text": "BPH, staz, östrojen eksikliği", "isMasked": True, "hint": "prostat ve menopoz değişiklikleri"}]},
            {"cells": [{"text": "Hastanede Yatanlar", "isMasked": False}, {"text": "%30", "isMasked": True, "hint": "en yüksek prevalans grubu"}, {"text": "Üretral kateter ve enstrümantasyon"}]}
        ]),
        make_recall("Hastanede yatan hastalarda ÜSE prevalansının %30'a kadar çıkmasının başlıca nedeni nedir?", "Üretral kateterizasyon, ürolojik girişimler ve altta yatan kronik yatış hastalıklarıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İleri Yaş Prevalansı", [
            {"text": "Reprodüktif dönemde ÜSE prevalansı yaklaşık %2,5'tir.", "isLie": False, "explanation": "Doğru. Genel erişkin oranıdır."},
            {"text": "65-70 yaş grubunda ÜSE prevalansı %20 seviyesine ulaşır.", "isLie": False, "explanation": "Doğru. Geriatrik dönemde belirgin artar."},
            {"text": "Hastanede yatan hastalarda ÜSE sıklığı %0'a iner çünkü hastaneler tamamen sterildir.", "isLie": True, "explanation": "Tuzak! Hastanede yatanlarda kateter kullanımı nedeniyle prevalans %30'a fırlar."},
            {"text": "İleri yaşta erkeklerde prostat hipertrofisi enfeksiyon riskini artırır.", "isLie": False, "explanation": "Doğru. Obstrüksiyon staz oluşturur."}
        ]),
        make_quiz("Yaşam dönemlerine göre ÜSE prevalansı eşleştirmelerinden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Reprodüktif dönem: %2,5 | 65-70 yaş: %20 | Hastanede yatma: %30", "isCorrect": True, "explanation": "Ders notu tablosundaki prevalans değerleri birebir bu şekildedir."},
            {"key": "B", "text": "Reprodüktif dönem: %90 | 65-70 yaş: %1 | Hastanede yatma: %0", "isCorrect": False, "explanation": "Değerler tamamen hatalıdır."},
            {"key": "C", "text": "65-70 yaşında ÜSE tamamen yok olur", "isCorrect": False, "explanation": "Aksine %20'ye fırlar."},
            {"key": "D", "text": "Hastanede yatanlarda sadece %0,1 görülür", "isCorrect": False, "explanation": "Yatanlarda %30 görülür."}
        ])
    ]
    slides.append(make_slide(7, "Yaşam Dönemlerine Göre Prevalans: Erişkin ve Geriatrik Dönem", "Reprodüktif %2,5, geriatrik %20 ve hastane yatışında %30 oranları", "Epidemiyoloji", s7_narrative, s7_bullets, s7_elements))

    # Slide 8: ÜSE'nin Klinik Formları: Asemptomatik Bakteriüriden Sepsise
    s8_narrative = (
        "Üriner sistem enfeksiyonları tek tip bir hastalık olmayıp, etkilenen anatomik bölgeye, konağın "
        "savunma gücüne ve bakterinin özelliklerine göre geniş bir klinik tablolar dizisidir.\n\n"
        "- **Asemptomatik Bakteriüri:** Hastada hiçbir subjektif şikayet veya dizüri olmaksızın "
        "kültürde anlamlı bakteri üremesi ile seyreder.\n"
        "- **Lokal Alt Sistem Enfeksiyonu (Sistit):** Mesane mukozası ile sınırlı, dizüri, pollaküri "
        "ve suprapubik ağrıyla karakterize, sistemik ateşin eşlik etmediği tablodur.\n"
        "- **Üst Sistem Enfeksiyonu ve Sepsis:** Bakterilerin böbrek parankimine ulaşmasıyla akut pyelonefrit, "
        "ardından kana karışmasıyla ürosepsis ve hayatı tehdit eden septik şok tablosu gelişebilir.\n\n"
        "> [!NOTE]\n"
        "> Klinik tablonun şiddeti, bakterinin virülansı ile konağın anatomik ve immünolojik direnci arasındaki dengeye bağlıdır."
    )
    s8_bullets = [
        "ÜSE spektrumu asemptomatik bakteriüriden sepsise kadar uzanır.",
        "Sistit alt üriner sistemi tutar ve sistemik bulgu vermez.",
        "Pyelonefrit ve ürosepsis sistemik tutulum ve hayati risk taşır."
    ]
    s8_elements = [
        make_cloze("ÜSE spektrumu hiçbir şikayeti olmayan asemptomatik bakteriüriden hayatı tehdit eden sepsise kadar uzanır.", "asemptomatik bakteriüriden", "Klinik tablonun en hafif semptomsuz ucu"),
        make_table("ÜSE Klinik Şiddet Spektrumu", ["Klinik Form", "Tutulan Anatomik Yapı", "Temel Belirti"], [
            {"cells": [{"text": "Asemptomatik Bakteriüri", "isMasked": False}, {"text": "Mesane / İdrar lümeni", "isMasked": True, "hint": "semptomsuz mikrop varlığı"}, {"text": "Şikayet yok, kültür pozitif"}]},
            {"cells": [{"text": "Akut Sistit", "isMasked": False}, {"text": "Mesane mukozası (alt sistem)", "isMasked": False}, {"text": "Dizüri, sık idrar, suprapubik ağrı", "isMasked": True, "hint": "idrarda yanma ve sıkışma"}]},
            {"cells": [{"text": "Ürosepsis", "isMasked": False}, {"text": "Sistemik dolaşım / Böbrek", "isMasked": False}, {"text": "Hipotansiyon, taşikardi, organ yetmezliği", "isMasked": True, "hint": "şok ve sistemik çöküş"}]}
        ]),
        make_chain("ÜSE Şiddet İlerleme Basamakları", [
            "1. Kolonizasyon: Bakteriüri oluşur (asemptomatik kalabilir).",
            "2. Lokal İnvazyon: Mesanede akut sistit gelişir (dizüri, pollaküri).",
            "3. Asendan Tırmanış: Böbrek parankimine ulaşarak akut pyelonefrit yapar (ateş, böğür ağrısı).",
            "4. Dolaşıma Yayılım: Bakteriyemi ve ürosepsis tablosu gelişir."
        ]),
        make_recall("ÜSE spektrumunda yer alan en hafif ve en ağır klinik formlar hangileridir?", "En hafif form asemptomatik bakteriüri, en ağır form ise hayatı tehdit eden ürosepsis / septik şoktur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Klinik Formlar", [
            {"text": "ÜSE, asemptomatik bakteriüriden sepsise kadar geniş bir klinik spektrum gösterir.", "isLie": False, "explanation": "Doğru. Hastalık tek bir tablo değildir."},
            {"text": "Sistit tablosunda enfeksiyon mesane mukozası ile sınırlıdır.", "isLie": False, "explanation": "Doğru. Alt sistem enfeksiyonudur."},
            {"text": "Her ÜSE vakası ilk dakikadan itibaren kesinlikle koma ve septik şokla başlar.", "isLie": True, "explanation": "Tuzak! Vakaların çoğu lokal sistit veya asemptomatik bakteriüri şeklinde hafif seyreder."},
            {"text": "Böbrek parankiminin tutulması akut pyelonefrit tablosuna yol açar.", "isLie": False, "explanation": "Doğru. Üst sistem enfeksiyonudur."}
        ]),
        make_quiz("Aşağıdakilerden hangisi ÜSE'nin klinik spektrumunun en geniş tanımını ifade eder?", [
            {"key": "A", "text": "Asemptomatik bakteriüriden sepsisle seyreden akut pyelonefrite kadar uzanan klinik skala", "isCorrect": True, "explanation": "Ders notunda belirtilen resmi klinik spektrum tanımıdır."},
            {"key": "B", "text": "Yalnızca böbrek taşlarının oluşturduğu mekanik obstrüksiyon", "isCorrect": False, "explanation": "Taş enfeksiyonun kendisi değildir."},
            {"key": "C", "text": "Sadece erkeklerde görülen izole testis enfeksiyonu", "isCorrect": False, "explanation": "ÜSE tüm üriner sistemi kapsar."},
            {"key": "D", "text": "Hiçbir zaman bakteri içermeyen otoimmün glomerulonefrit", "isCorrect": False, "explanation": "ÜSE bakteriyeldir."}
        ])
    ]
    slides.append(make_slide(8, "ÜSE'nin Klinik Formları: Asemptomatik Bakteriüriden Sepsise", "Asemptomatik bakteriüri, akut sistit, pyelonefrit ve ürosepsis spektrumu", "Klinik Sınıflama", s8_narrative, s8_bullets, s8_elements))

    # Slide 9: Birinci Bölüm Özeti: Tanım ve Epidemiyolojik Temeller
    s9_narrative = (
        "Üriner sistem enfeksiyonları, yüksek prevalansı, kadın yatkınlığı ve geniş klinik spektrumu "
        "ile modern tıbbın en temel enfeksiyon başlıklarından birini oluşturur.\n\n"
        "- **Kardinal Tanım:** İdrarda üropatojen bakteri ile birlikte konak enflamatuar reaksiyonunun "
        "(piyüri) bulunmasıdır.\n"
        "- **Kadın Yatkınlığı:** Hastaların %67,5'i kadındır; kadınların %50'si yaşam boyu en az bir kez "
        "atağı geçirir ve %10-20'sinde yineleyen enfeksiyonlar görülür.\n"
        "- **Erkek Korunması:** Genç erkeklerde (%1 altı sıklık) uzun üretra ve bakterisidal prostat "
        "sıvısı enfeksiyonu önler; yenidoğanda ise E/K oranı 1,5/1 ile istisnai olarak erkek lehinedir.\n\n"
        "> [!IMPORTANT]\n"
        "> Tanım, cinsiyet oranları ve yaş gruplarına göre prevalans dinamikleri ÜSE kliniğini anlamanın vazgeçilmez temelidir."
    )
    s9_bullets = [
        "ÜSE = İdrarda bakteri + konak enflamatuar reaksiyonu (piyüri).",
        "Kadınlarda yaşam boyu risk %50; olguların %67,5'i kadındır.",
        "1-50 yaş erkekte <%1 sıklık; yenidoğanda E/K: 1,5/1 oranı tipiktir."
    ]
    s9_elements = [
        make_cloze("ÜSE patolojisinde temel kural idrarda bakteri ile birlikte konak dokusunda piyüri (enflamasyon) bulunmasıdır.", "piyüri", "İdrarda lökosit varlığı"),
        make_table("Epidemiyolojik Anahtar Veriler", ["Kavram", "Temel İstatistik", "Klinik Mesaj"], [
            {"cells": [{"text": "Kadın Hasta Oranı", "isMasked": False}, {"text": "%67,5", "isMasked": True, "hint": "tüm hastalar içindeki kadın yüzdesi"}, {"text": "Belirgin kadın baskınlığı"}]},
            {"cells": [{"text": "Genç Erkek İnsidansı", "isMasked": False}, {"text": "<%1", "isMasked": False}, {"text": "Uzun üretra ve prostat sıvısı korur", "isMasked": True, "hint": "erkek anatomik savunması"}]},
            {"cells": [{"text": "Neonatal Cinsiyet Oranı", "isMasked": False}, {"text": "Erkek / Kadın: 1,5 / 1", "isMasked": True, "hint": "yenidoğan cinsiyet oranı"}, {"text": "Erkeklerde daha sık tek dönem"}]}
        ]),
        make_recall("Hangi yaşam döneminde ÜSE erkek çocuklarda kız çocuklarından daha sık görülür?", "Yenidoğan (neonatal) döneminde (Erkek/Kadın oranı 1,5 / 1'dir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Epidemiyolojik Temeller", [
            {"text": "ÜSE tanısı alan hastaların %67,5'i kadındır.", "isLie": False, "explanation": "Doğru. Ders notu verisidir."},
            {"text": "Kadınların yaklaşık yarısı (%50) yaşam boyu en az bir kez ÜSE atağı yaşar.", "isLie": False, "explanation": "Doğru. Çok yüksek bir insidanstır."},
            {"text": "1-50 yaş arası erkeklerde ÜSE görülme sıklığı %90'dır.", "isLie": True, "explanation": "Tuzak! 1-50 yaş arası erkeklerde ÜSE insidansı %1'in altındadır."},
            {"text": "Hastanede yatan hastalarda ÜSE prevalansı kateterler nedeniyle %30'a ulaşır.", "isLie": False, "explanation": "Doğru. Nozokomiyal risk yüksektir."}
        ]),
        make_quiz("ÜSE epidemiyolojisi ile ilgili aşağıdaki istatistiklerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "1-50 yaş arası sağlıklı erkeklerde ÜSE insidansı %50'dir", "isCorrect": True, "explanation": "Yanlış! Bu yaş grubundaki erkeklerde insidans %1'in altındadır; %50 olan oran kadınların yaşam boyu riskidir."},
            {"key": "B", "text": "Kadınların yaklaşık %50'si yaşamları boyunca en az bir kez ÜSE geçirir", "isCorrect": False, "explanation": "Doğru bir istatistiktir."},
            {"key": "C", "text": "Yenidoğan döneminde E/K oranı 1,5/1 olup erkek baskındır", "isCorrect": False, "explanation": "Doğru bir istatistiktir."},
            {"key": "D", "text": "Hastanede yatan hastalarda ÜSE prevalansı %30 civarındadır", "isCorrect": False, "explanation": "Doğru bir istatistiktir."}
        ])
    ]
    slides.append(make_slide(9, "Birinci Bölüm Özeti: Tanım ve Epidemiyolojik Temeller", "ÜSE tanımı, kadın baskınlığı, erkek anatomik bariyeri ve yaşam dönemi oranları", "Konsolidasyon", s9_narrative, s9_bullets, s9_elements))

    # Slide 10: [TEKRAR SAYFASI - CHECKPOINT 1] Tanım ve Epidemiyoloji
    s10_narrative = (
        "Bu tekrar sayfasında 1. Bölümde işlenen ÜSE tanımı, cinsiyet farklılıkları, doğal konak "
        "engelleri ve yaş dönemlerine özgü prevalans verilerini pekiştiriyoruz.\n\n"
        "- **Bakteri ve Enflamasyon:** İdrarda mikrop üremesi ile birlikte ürotelyal enflamatuar yanıtın "
        "(piyüri) varlığı ÜSE'nin vazgeçilmez tanısal kriteridir.\n"
        "- **Kadın vs Erkek:** Kadınlarda kısa üretra ve perineal yakınlık %50 yaşam boyu risk doğururken; "
        "erkeklerde uzun üretra ve bakterisidal prostat salgısı 1-50 yaşta insidansı <%1 düzeyinde tutar.\n"
        "- **Yaşam Döngüsü:** Yenidoğanda erkek fazlalığı (1,5/1), reprodüktif dönemde kadın patlaması (%2,5), "
        "65-70 yaşta BPH ile eşitlenme (%20) ve hastanede kateterle zirve (%30) görülür.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] ÜSE, enflamatuar yanıtla giden bakteriyel bir süreçtir; genç erkekte <%1, neonatalde E>K, erişkinde ise ezici şekilde kadın baskındır."
    )
    s10_bullets = [
        "ÜSE = İdrarda bakteri + enflamatuar reaksiyon (piyüri).",
        "Genç erkekte uzun üretra ve prostat sıvısı insidansı <%1 yapar.",
        "Yenidoğanda E/K 1,5/1 iken erişkinde hastaların %67,5'i kadındır."
    ]
    s10_elements = [
        make_cloze("Neonatal dönem hariç ÜSE esas olarak kadınları etkilerken genç erkekte insidans %1'in altındadır.", "%1'in altındadır", "Genç erkekteki düşük insidans oranı"),
        make_table("1. Bölüm Büyük Tekrar Tablosu", ["Dönem / Grup", "Görülme Sıklığı / Oran", "Temel Mekanizma"], [
            {"cells": [{"text": "Yenidoğan (Neonatal)", "isMasked": False}, {"text": "%1 (Erkek/Kadın: 1,5/1)", "isMasked": True, "hint": "erkek baskın oran"}, {"text": "Konjenital ürolojik anomaliler"}]},
            {"cells": [{"text": "1-50 Yaş Erkek", "isMasked": False}, {"text": "<%1 insidans", "isMasked": False}, {"text": "Uzun üretra + bakterisidal prostat sıvısı", "isMasked": True, "hint": "erkek koruyucu faktörleri"}]},
            {"cells": [{"text": "Tüm Yaşam Kadın", "isMasked": False}, {"text": "%50 yaşam boyu risk", "isMasked": True, "hint": "kadınların yarısı"}, {"text": "Kısa üretra ve asendan kolonizasyon"}]},
            {"cells": [{"text": "Hastanede Yatanlar", "isMasked": False}, {"text": "%30 prevalans", "isMasked": False}, {"text": "Kateterizasyon ve enstrümantasyon", "isMasked": True, "hint": "hastane risk faktörü"}]}
        ]),
        make_chain("Klinik Spektrum Hiyerarşisi", [
            "1. Asemptomatik Bakteriüri: Semptomsuz idrarda bakteri üremesi.",
            "2. Akut Sistit: Mesane mukozasında dizüri ve pollaküri (ateşsiz).",
            "3. Akut Pyelonefrit: Böbrek parankim tutulumu (yüksek ateş, KVAH).",
            "4. Ürosepsis: Sistemik dolaşıma yayılım ve hemodinamik bozulma."
        ]),
        make_recall("ÜSE tanısı alan hastaların yüzde kaçı kadındır ve kadınların yaşam boyu ÜSE geçirme riski nedir?", "Hastaların %67,5'i kadındır; kadınların yaşam boyu en az bir kez ÜSE geçirme riski ise yaklaşık %50'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 1. Bölüm Konsolidasyonu", [
            {"text": "ÜSE'de idrarda bakteri bulunmasına mutlaka konak enflamatuar reaksiyonu eşlik eder.", "isLie": False, "explanation": "Doğru. Tanımın temel koşuludur."},
            {"text": "1-50 yaş arası erkeklerde ÜSE insidansı %1'in altındadır.", "isLie": False, "explanation": "Doğru. Anatomik ve kimyasal koruma vardır."},
            {"text": "Yenidoğan döneminde kız bebeklerde ÜSE erkek bebeklerden 10 kat daha sıktır.", "isLie": True, "explanation": "Tuzak! Yenidoğan döneminde tam tersine erkek bebeklerde daha sıktır (E/K: 1,5 / 1)."},
            {"text": "Hastanede yatan hastalarda ÜSE prevalansı kateterler nedeniyle %30'a ulaşabilir.", "isLie": False, "explanation": "Doğru. En yüksek prevalans grubudur."}
        ]),
        make_quiz("1. Bölümün temel kazanımlarına göre aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Neonatal dönemde kız bebeklerde ÜSE erkeklerden belirgin şekilde daha sıktır", "isCorrect": True, "explanation": "Yanlış! Neonatal dönem ÜSE'nin erkeklerde daha sık görüldüğü (E/K: 1,5/1) tek dönemdir."},
            {"key": "B", "text": "Üriner sistem enfeksiyonu tanısı alan hastaların %67,5'i kadındır", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "1-50 yaş arası erkeklerde uzun üretra ve prostat sıvısı insidansı <%1 yapar", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Akut pyelonefrit nedeniyle yılda 100.000'in üzerinde hasta hastaneye yatırılmaktadır", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(10, "[TEKRAR SAYFASI - CHECKPOINT 1] Tanım ve Epidemiyoloji", "1. Bölümün kapsamlı pekiştirmesi: tanım, epidemiyoloji, cinsiyet ve yaş dinamikleri", "Bölüm Tekrarı", s10_narrative, s10_bullets, s10_elements))

    return slides
