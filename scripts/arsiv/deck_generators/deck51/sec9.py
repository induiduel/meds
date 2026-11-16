# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec9():
    slides = []

    # Slide 81: İdrar Kültürü Kriterleri ve Koloni Sayımı (CFU/ml)
    s81_narrative = (
        "İdrar kültürü, üriner sistem enfeksiyonlarında etken mikroorganizmanın izolasyonu, kantitatif "
        "sayımı ve antibiyotik duyarlılığının belirlenmesinde altın standart mikrobiyolojik yöntemdir.\n\n"
        "- **Semptomatik Hastada Eşik:** Tipik dizüri veya pollaküri semptomları olan bir kadında, temiz "
        "orta akım idrar kültüründe **tek bir organizmanın ≥10⁵ (100.000) CFU/ml (KOB/ml)** üremesi "
        "olguların %95'inde kesin enfeksiyonu kanıtlar.\n"
        "- **Suprapubik Aspirasyon İstisnası:** Suprapubik aspirasyon örneğinde kontaminasyon riski "
        "olmadığından, koloni sayısı ne olursa olsun **herhangi bir sayıda Gram (-) basil** tanısal kabul edilir.\n"
        "- **Antiseptik Uyarısı:** Örnek alımı sırasında genital bölgeye kimyasal antiseptik solüsyon "
        "sürülmesi idrara karışarak **yalancı negatif sonuçlara** yol açabileceğinden sadece sabunlu su kullanılmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kültür altın standarttır; semptomatik orta akımda ≥10⁵ CFU/ml tek organizma, suprapubik aspirasyonda ise herhangi bir sayıda üreme tanı koydurur; antiseptik kullanımı yalancı negatif yapar."
    )
    s81_bullets = [
        "İdrar kültürü kesin tanı ve antibiyogram için altın standarttır.",
        "Semptomatik orta akımda tek bakterinin ≥10⁵ CFU/ml üremesi %95 tanı koydurur.",
        "Suprapubik aspirasyonda herhangi bir sayıda Gram (-) basil üremesi tanısal kabul edilir."
    ]
    s81_elements = [
        make_cloze("Semptomatik hastanın temiz orta akım idrar kültüründe tek bir organizmanın ≥10⁵ CFU/ml üremesi tanı koydurur.", "≥10⁵ CFU/ml", "Yüz bin koloni oluşturan birim eşiği"),
        make_table("İdrar Kültüründe Tanısal Üreme Kriterleri", ["Örnek Alma Yöntemi", "Hasta Durumu", "Tanısal Koloni Sayısı"], [
            {"cells": [{"text": "Suprapubik Aspirasyon", "isMasked": False}, {"text": "Tüm hastalar", "isMasked": False}, {"text": "Herhangi bir sayıda Gram (-) basil", "isMasked": True, "hint": "tek bakteri dahi yeterli"}]},
            {"cells": [{"text": "Temiz Orta Akım", "isMasked": False}, {"text": "Semptomatik hasta", "isMasked": False}, {"text": "≥10⁵ CFU/ml (tek organizma) %95", "isMasked": True, "hint": "yüz bin koloni tek bakteri"}]},
            {"cells": [{"text": "Temiz Orta Akım", "isMasked": False}, {"text": "Asemptomatik hasta", "isMasked": False}, {"text": "2 ayrı günde aynı bakterinin 10⁵ CFU/ml", "isMasked": False}]}
        ]),
        make_chain("Kültür Kantitatif Değerlendirme Zinciri", [
            "1. Ekim: Kalibre öze ile 0.001 ml idrar kanlı ve EMB besiyerine ekilir.",
            "2. İnkübasyon: 37°C'de 24-48 saat bekletilir.",
            "3. Koloni Sayımı: Petrideki koloniler sayılarak 1000 ile çarpılır.",
            "4. Eşik Kararı: Semptomatik kadında 100 koloni (≥10⁵ CFU/ml) varsa pozitif raporlanır."
        ]),
        make_recall("Semptomatik bir hastanın temiz orta akım idrar kültüründe enfeksiyon tanısı için aranan standart koloni eşiği nedir?", "Tek bir mikroorganizmanın ≥10⁵ CFU/ml (100.000 KOB/ml) üremesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kültür Kriterleri", [
            {"text": "İdrar kültürü İYE düşünülen bütün hastalarda altın standarttır.", "isLie": False, "explanation": "Doğru. Kesin tanı yöntemidir."},
            {"text": "Suprapubik aspirasyonda herhangi bir sayıda Gram (-) basil tanısal kabul edilir.", "isLie": False, "explanation": "Doğru. Kontaminasyonsuzdur."},
            {"text": "Örnek alınırken genital bölgeye bolca çamaşır suyu ve zefiran dökmek kültürü güzelleştirir.", "isLie": True, "explanation": "Tuzak! Antiseptik kullanımı idrara karışarak bakterileri öldürür ve YALANCI NEGATİF sonuçlara yol açar."},
            {"text": "Semptomatik hastada ≥10⁵ CFU/ml üreme %95 tanı koydurur.", "isLie": False, "explanation": "Doğru. Standart kriterdir."}
        ]),
        make_quiz("İdrar kültürü için örnek alınırken antiseptik solüsyon kullanılması laboratuvar sonucunu nasıl etkiler?", [
            {"key": "A", "text": "Yalancı negatif sonuçlara yol açabilir", "isCorrect": True, "explanation": "Ders notunda 'antiseptik kullanımı yalancı negatif sonuçlara yol açabilir' uyarısı açıkça yer almaktadır."},
            {"key": "B", "text": "Kültürde virüs üremesini 100 kat artırır", "isCorrect": False, "explanation": "Virüs standart agarda üremez."},
            {"key": "C", "text": "Sonucu hiçbir şekilde etkilemez", "isCorrect": False, "explanation": "Bakterileri öldürür."},
            {"key": "D", "text": "İdrarı anında altına çevirir", "isCorrect": False, "explanation": "Tıbbi temeli yoktur."}
        ])
    ]
    slides.append(make_slide(81, "İdrar Kültürü Kriterleri ve Koloni Sayımı (CFU/ml)", "İdrar kültürü altın standardı, ≥10⁵ CFU/ml eşiği, suprapubik kuralı ve antiseptik uyarısı", "İdrar Kültürü", s81_narrative, s81_bullets, s81_elements))

    # Slide 82: İdrar Kültüründe Kontaminasyon Göstergeleri
    s82_narrative = (
        "Mikrobiyoloji laboratuvarında bir idrar kültürünün gerçek bir enfeksiyonu mu yoksa perineal/vajinal "
        "cilt florası bulaşını mı yansıttığını ayırt etmek kritik önem taşır.\n\n"
        "- **Polimikrobiyal Üreme:** Kültür plağında **birden fazla farklı morfolojide bakteri** "
        "(3 veya daha fazla tür) üremesi gerçek enfeksiyondan ziyade açık bir **kontaminasyon göstergesidir** "
        "(komplike/kateterli durumlar hariç).\n"
        "- **Skuamöz Epitel Hücreleri:** Mikroskopide idrarda yoğun **skuamöz epitel hücrelerinin** "
        "görülmesi, örneğin distal üretra ve dış genital ciltten döküntü topladığını belgeler.\n"
        "- **Laktobasiller ve Korinebakteriler:** İdrarda normal vajinal flora elemanı olan **laktobasillerin** "
        "saptanması vajinal sekresyonların idrar kabına karıştığının kesin kanıtıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kontaminasyon göstergeleri: 1) Birden fazla farklı morfolojide bakteri varlığı, 2) Skuamöz epitel hücre varlığı, 3) Laktobasil varlığı (vajinal sekresyon karışımı)!"
    )
    s82_bullets = [
        "Birden fazla farklı morfolojide bakteri üremesi kontaminasyonu düşündürür.",
        "İdrar mikroskopisinde skuamöz epitel hücre varlığı cilt temasını gösterir.",
        "Laktobasil varlığı idrara vajinal sekresyon karıştığının kanıtıdır."
    ]
    s82_elements = [
        make_cloze("İdrar kültüründe vajinal sekresyon karışımını ve kontaminasyonu kanıtlayan mikroorganizma laktobasil varlığıdır.", "laktobasil", "Vajen florasının koruyucu basili"),
        make_table("Kültürde Kontaminasyon Kriterleri", ["Laboratuvar Bulgusu", "Biyolojik Kaynak", "Klinik Karar"], [
            {"cells": [{"text": "Çoklu Bakteri Morfolojisi", "isMasked": False}, {"text": "Perine ve cilt kommensalleri", "isMasked": True, "hint": "birden fazla bakteri türü"}, {"text": "Kontaminasyon şüphesi → Kültür tekrarı"}]},
            {"cells": [{"text": "Skuamöz Epitel Hücreleri", "isMasked": False}, {"text": "Dış genital cilt ve introitus", "isMasked": False}, {"text": "Örneğin kötü alındığının göstergesi", "isMasked": True, "hint": "cilt döküntüsü karışması"}]},
            {"cells": [{"text": "Laktobasil İzolasyonu", "isMasked": False}, {"text": "Normal vajina florası", "isMasked": False}, {"text": "Vajinal akıntı kontaminasyonu kanıtı", "isMasked": False}]}
        ]),
        make_chain("Kontaminasyon Ayıklama Zinciri", [
            "1. İnceleme: Kültür plağında 3 farklı renkte koloni görülür.",
            "2. Sediment Bakısı: Mikroskopta bol skuamöz epitel ve laktobasiller izlenir.",
            "3. Raporlama: Laboratuvar 'Örnek kontamine kabul edildi' notu düşer.",
            "4. Tekrar: Hastaya hijyenik orta akım tekniği anlatılarak taze sabah örneği istenir."
        ]),
        make_recall("İdrar kültüründe örneğin kontamine olduğunu gösteren üç temel laboratuvar bulgusu nedir?", "1) Birden fazla farklı morfolojide bakteri üremesi, 2) Skuamöz epitel hücre varlığı, 3) Laktobasil varlığıdır (vajinal sekresyon karışımı)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kontaminasyon Göstergeleri", [
            {"text": "Birden fazla farklı morfolojide bakteri üremesi kontaminasyon göstergesidir.", "isLie": False, "explanation": "Doğru. Monomikrobiyal olmalıdır."},
            {"text": "Skuamöz epitel hücre varlığı dış genital bulaşı gösterir.", "isLie": False, "explanation": "Doğru. Kötü örnek alımıdır."},
            {"text": "İdrarda laktobasil üremesi böbreklerin çürüdüğünü ve acil nakil gerektiğini kanıtlar.", "isLie": True, "explanation": "Tuzak! Laktobasil normal vajen florasıdır; idrara vajinal akıntı karıştığını (kontaminasyonu) gösterir."},
            {"text": "Laktobasil varlığı vajinal sekresyon karışımına işaret eder.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("İdrar kültürü ve mikroskopisinde aşağıdakilerden hangisinin saptanması örneğin KONTAMİNE olduğunu gösteren bulgulardan biridir?", [
            {"key": "A", "text": "Skuamöz epitel hücreleri ve laktobasil varlığı", "isCorrect": True, "explanation": "Ders notunda kontaminasyon göstergeleri: birden fazla bakteri morfolojisi, skuamöz epitel hücreleri ve laktobasil varlığı olarak sayılmıştır."},
            {"key": "B", "text": "Saf monomikrobiyal 10⁵ E. coli üremesi", "isCorrect": False, "explanation": "Gerçek enfeksiyonu gösterir."},
            {"key": "C", "text": "Lökosit silendirlerinin görülmesi", "isCorrect": False, "explanation": "Böbrek hasarını gösterir."},
            {"key": "D", "text": "Suprapubik aspirasyonda tek basil üremesi", "isCorrect": False, "explanation": "Altın standart enfeksiyon kanıtıdır."}
        ])
    ]
    slides.append(make_slide(82, "İdrar Kültüründe Kontaminasyon Göstergeleri", "Kontaminasyon kriterleri, çoklu bakteri morfolojisi, skuamöz epitel ve laktobasiller", "İdrar Kültürü", s82_narrative, s82_bullets, s82_elements))

    # Slide 83: İdrar Kültürü Endikasyonları ve Ek Tetkikler
    s83_narrative = (
        "Her basit sistit atağında idrar kültürü almak maliyet-etkin değildir; ancak komplike risk "
        "taşıyan veya tedavi başarısızlığı ihtimali yüksek hastalarda kültür zorunludur.\n\n"
        "- **Kültür Alınması Zorunlu Durumlar:** Diabetes Mellitus hastaları, hamile kadınlar (gebeler), "
        "tüm akut pyelonefrit şüphesi olanlar, çocukluk çağı enfeksiyonları, erkek hastalar, komplike "
        "ÜSE ve tekrarlayan ÜSE (ör. tekrarlayan sistit) vakalarıdır.\n"
        "- **Akut Pyelonefritte Ek Tetkikler:** Sistemik bakteriyemi ve sepsis riskini izlemek amacıyla "
        "**tam kan sayımı (hemogram / lökositoz) ve CRP** istenir.\n"
        "- **Erkek ve CYBH'de Ek Tetkikler:** Akut prostatit şüphesinde **Total PSA**; cinsel aktif riskli "
        "hastalarda VDRL, RPR, TPHA, Anti-HIV ve hepatit belirteçleri taranmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> Diyabet, gebelik, pyelonefrit, çocuklar ve tekrarlayan ÜSE olgularında ampirik tedaviye başlanmadan önce mutlaka idrar kültürü alınmalıdır."
    )
    s83_bullets = [
        "Kültür endikasyonları: DM, gebelik, pyelonefrit, çocuklar, komplike ve tekrarlayan ÜSE.",
        "Akut pyelonefritte hemogram (lökositoz) ve CRP rutin istenir.",
        "Akut prostatitte Total PSA; şüpheli olgularda CYBH paneli (VDRL, RPR, HIV) taranır."
    ]
    s83_elements = [
        make_cloze("Akut pyelonefritli hastada sistemik enflamatuar yanıtı değerlendirmek için hemogram ve CRP istenir.", "CRP", "C-reaktif protein akut faz belirteci"),
        make_table("Kültür Endikasyonları ve Ek Tetkik Paneli", ["Klinik Durum", "Gereken Laboratuvar Testi", "Tanısal Amacı"], [
            {"cells": [{"text": "Diyabet, Gebelik, Çocuklar", "isMasked": False}, {"text": "İdrar kültürü ve antibiyogram", "isMasked": True, "hint": "bakteri üretimi ve duyarlılık"}, {"text": "Dirençli üropatojenin saptanması"}]},
            {"cells": [{"text": "Akut Pyelonefrit", "isMasked": False}, {"text": "Kültür + Hemogram + CRP", "isMasked": False}, {"text": "Sistemik tutulum ve sepsisin taranması", "isMasked": True, "hint": "kandaki iltihap düzeyi"}]},
            {"cells": [{"text": "Akut Prostatit", "isMasked": False}, {"text": "Total PSA ve idrar analizi", "isMasked": False}, {"text": "Prostatik doku enflamasyonu değerlendirmesi", "isMasked": False}]}
        ]),
        make_chain("Pyelonefrit Laboratuvar İstem Zinciri", [
            "1. Klinik: Yüksek ateş ve böğür ağrısı saptanır.",
            "2. İdrar Kültürü: Antibiyotik verilmeden önce idrar kültürü ve antibiyogram alınır.",
            "3. Sistemik Belirteçler: Kanda lökositoz için hemogram ve CRP istenir.",
            "4. Tedavi Başlangıcı: Tetkikler alındıktan hemen sonra ampirik parenteral tedaviye geçilir."
        ]),
        make_recall("Hangi hasta gruplarında ÜSE geliştiğinde mutlaka idrar kültürü alınmalıdır?", "Diyabetik hastalar, gebeler, pyelonefrit olguları, çocuklar, komplike ÜSE ve tekrarlayan ÜSE vakalarında mutlaka kültür alınmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kültür Endikasyonları", [
            {"text": "Diyabet, hamilelik ve pyelonefritte idrar kültürü alınmalıdır.", "isLie": False, "explanation": "Doğru. Kesin endikasyonlardır."},
            {"text": "Akut pyelonefritte hemogram ve CRP tetkiki istenir.", "isLie": False, "explanation": "Doğru. Sistemik yanıttır."},
            {"text": "Gebelere kültür alınması yasaktır çünkü kültür tüpleri anneye radyasyon yayar.", "isLie": True, "explanation": "Tuzak! Kültür bir laboratuvar ekimidir, radyasyon içermez ve gebelerde kültür ZORUNLUDUR."},
            {"text": "Tekrarlayan ÜSE ve çocuklarda idrar kültürü endikedir.", "isLie": False, "explanation": "Doğru. Odak ve direnç saptanır."}
        ]),
        make_quiz("Aşağıdaki klinik tablolardan hangisinde ampirik antibiyotik başlamadan önce İDRAR KÜLTÜRÜ alınması ZORUNLU DEĞİLDİR?", [
            {"key": "A", "text": "Sağlıklı, 20 yaşında, gebe olmayan kadında ilk kez gelişen basit sistit", "isCorrect": True, "explanation": "Sağlıklı genç kadında ilk basit komplike olmayan sistitte kültür şartı aranmaz, doğrudan ampirik tedavi başlanabilir. Gebelerde, diyabetiklerde, pyelonefritte ve çocuklarda ise kültür şarttır."},
            {"key": "B", "text": "Gebe kadında idrar yolu enfeksiyonu şüphesi", "isCorrect": False, "explanation": "Kültür zorunludur."},
            {"key": "C", "text": "Akut pyelonefrit tablosu", "isCorrect": False, "explanation": "Kültür zorunludur."},
            {"key": "D", "text": "Diabetes Mellitus hastasında ÜSE", "isCorrect": False, "explanation": "Kültür zorunludur."}
        ])
    ]
    slides.append(make_slide(83, "İdrar Kültürü Endikasyonları ve Ek Tetkikler", "Kültür endikasyonları (gebe, DM, çocuk, pyelonefrit), hemogram, CRP ve PSA", "İdrar Kültürü", s83_narrative, s83_bullets, s83_elements))

    # Slide 84: Radyolojik Görüntüleme Prensipleri: Rutinde Gereksizdir!
    s84_narrative = (
        "Klinik pratikte yapılan en büyük kaynak israflarından biri, basit sistit veya komplike olmayan "
        "pyelonefrit vakalarında gereksiz radyolojik tetkik istenmesidir.\n\n"
        "- **Rutin Görüntüleme Kuralı:** Üriner sistem enfeksiyonlarının **çoğunda görüntüleme çalışmalarına "
        "KESİNLİKLE GEREK YOKTUR**; hastaların çoğunda sadece klinik ve laboratuvar bulgular doğru "
        "tanı ve tedavi için tamamen yeterlidir.\n"
        "- **Radyolojik İnceleme Gerektiren Durumlar:** Sepsis ve septik şok tablosu; nefrolitiazis "
        "(taş) şüphesi; cerrahi işlem gerektiren amfizematöz obstrüksiyonlar; renal veya perirenal "
        "abse şüphesi; rekürren enfeksiyonlar ve **tedavinin 72. saatinde ateşi düşmeyen pyelonefritler**.\n"
        "- **Seçenekler:** DÜSG taş opasitelerini; USG hidronefroz ve abseleri; Kontrastsız/Kontrastlı "
        "BT ise obstrüksiyon, darlık ve gaz oluşumunu mükemmel gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Üriner sistem enfeksiyonlarının çoğunda görüntüleme tetkiklerine gerek yoktur; radyoloji sadece sepsis, taş, abse, amfizem ve tedaviye yanıtsızlıkta istenir."
    )
    s84_bullets = [
        "ÜSE'lerin çoğunda görüntüleme çalışmalarına GEREK YOKTUR.",
        "Klinik ve laboratuvar bulgular hastaların çoğunda tanı ve tedaviye yeterlidir.",
        "Radyoloji: Sepsis, nefrolitiazis, abse, amfizem ve yanıtsız olgularda istenir."
    ]
    s84_elements = [
        make_cloze("Üriner sistem enfeksiyonlarının çoğunda radyolojik görüntüleme çalışmalarına gerek yoktur.", "gerek yoktur", "Rutin radyoloji istememe ilkesi"),
        make_table("Radyolojik Yöntemlerin Tanısal Katkıları", ["Yöntem", "Görüntülenen Lezyon", "Endike Olduğu Durum"], [
            {"cells": [{"text": "Direkt Üriner Sistem Grafisi (DÜSG)", "isMasked": False}, {"text": "Opak kalkül (taş), kitle, parankimal gaz", "isMasked": True, "hint": "radyoopak taşlar ve gaz"}, {"text": "Nefrolitiazis ve amfizem taraması"}]},
            {"cells": [{"text": "Ultrasonografi (USG)", "isMasked": False}, {"text": "Hidronefroz, taş, abse, amfizem", "isMasked": False}, {"text": "Tıkanıklık ve koleksiyonun hızlı tespiti", "isMasked": True, "hint": "böbrek genişlemesi ve püy arayışı"}]},
            {"cells": [{"text": "Bilgisayarlı Tomografi (BT)", "isMasked": False}, {"text": "Obstrüksiyon, gaz, abse, yapısal anomali", "isMasked": False}, {"text": "En duyarlı ve kesin anatomik haritalama", "isMasked": False}]}
        ]),
        make_chain("Radyolojik Endikasyon Zinciri", [
            "1. Basit Sistit: Hasta yanma ile gelir → Görüntüleme İSTENMEZ.",
            "2. Komplike Seyir: Hastada şok veya 72 saat düşmeyen ateş gelişir.",
            "3. Acil USG: Hidronefroz veya perirenal koleksiyon aranır.",
            "4. Kesin BT: Gaz, taş veya abse netleştirilerek cerrahi drenaj planlanır."
        ]),
        make_recall("Üriner sistem enfeksiyonlarında radyolojik görüntüleme ne zaman gereklidir?", "Rutin vakalarda gerek yoktur; yalnızca sepsis/septik şok, nefrolitiazis (taş), cerrahi gerektiren abse/amfizem, rekürren enfeksiyonlar ve tedaviye dirençli pyelonefritte gereklidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Radyolojik Görüntüleme", [
            {"text": "Üriner sistem enfeksiyonlarının çoğunda görüntüleme çalışmalarına gerek yoktur.", "isLie": False, "explanation": "Doğru. Klinik ve laboratuvar yeterlidir."},
            {"text": "Sepsis, abse ve nefrolitiazis durumlarında radyoloji istenir.", "isLie": False, "explanation": "Doğru. Kesin endikasyonlardır."},
            {"text": "Her basit idrar yanmasında hastaya mutlaka 50 kez tüm vücut tomografisi çekilmelidir.", "isLie": True, "explanation": "Tuzak! Komplike olmayan vakalarda görüntüleme kesinlikle önerilmez; gereksiz radyasyon ve maliyettir."},
            {"text": "Ultrasonografi hidronefroz ve böbrek absesini saptamada çok faydalıdır.", "isLie": False, "explanation": "Doğru. Radyasyonsuz ilk tercihtir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarında radyolojik görüntüleme tetkikleri ile ilgili aşağıdaki ilkelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Vakaların çoğunda görüntülemeye gerek yoktur; sadece sepsis, taş, abse ve amfizem gibi durumlarda istenir", "isCorrect": True, "explanation": "Ders notunda 'Üriner sistem enfeksiyonlarının çoğunda görüntüleme çalışmalarına gerek yoktur' ifadesi ve spesifik endikasyonlar listelenmiştir."},
            {"key": "B", "text": "Tüm sistitli hastalara acil kontrastlı akciğer tomografisi çekilmelidir", "isCorrect": False, "explanation": "Gereksizdir."},
            {"key": "C", "text": "Radyoloji sadece tırnak mantarında kullanılır", "isCorrect": False, "explanation": "İlişkisizdir."},
            {"key": "D", "text": "Abse şüphesinde radyoloji kesinlikle yasaktır", "isCorrect": False, "explanation": "Absede görüntüleme şarttır."}
        ])
    ]
    slides.append(make_slide(84, "Radyolojik Görüntüleme Prensipleri: Rutinde Gereksizdir!", "Radyolojinin rutinde gereksizliği, DÜSG, USG, BT endikasyonları (sepsis, abse, taş)", "Görüntüleme", s84_narrative, s84_bullets, s84_elements))

    # Slide 85: Tedavi İlkeleri ve %20 Direnç Kuralı
    s85_narrative = (
        "Üriner sistem enfeksiyonlarında tedaviye başlama kararı ve antibiyotik seçimi, mikrobiyolojik "
        "kültür sonucunu beklemeden ampirik olarak verilir.\n\n"
        "- **Ampirik Başlangıç İlkesi:** Akut semptomları olan bir hastada **kültür sonucu beklenmez, "
        "tedavi hemen ampirik olarak başlanır** (piyüri/nitrit pozitifse tedavi edilir; negatifse İYE yoktur).\n"
        "- **%20 Direnç Eşiği Kuralı:** Bir toplumda veya bölgede, belirli bir üropatojenin (özellikle "
        "E. coli) bir antibiyotiğe karşı **direnç oranı %20'nin üzerindeyse, o antibiyotik ampirik "
        "tedavide ASLA birinci tercih olarak kullanılmamalıdır** (ör. yüksek TMP-SMX direnci olan bölgeler).\n"
        "- **Tedavi Kararını Etkileyenler:** İlacın böbrek ve mesanede ulaştığı konsantrasyon, dışkı ve "
        "vajen florasına ekolojik yan hasar etkisi, yan etki profili ve maliyettir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kültür şartı aranmaz, tedavi ampirik başlanır; ancak toplumda bir antibiyotiğe %20'nin üzerinde direnç varsa o ilaç ampirik tedavide KULLANILMAMALIDIR!"
    )
    s85_bullets = [
        "Kültür sonucu beklenmeden tedaviye hemen ampirik olarak başlanır.",
        "Toplumdaki direnç oranı %20'nin üzerindeyse o antibiyotik ampirik seçilemez.",
        "İlacın üriner konsantrasyonu ve vajinal floraya yan etkisi seçimde kritiktir."
    ]
    s85_elements = [
        make_cloze("Toplumda üropatojen direnci %20'nin üzerinde olan antibiyotikler ampirik tedavide kullanılmamalıdır.", "%20'nin üzerinde", "Yüzde yirmilik direnç barajı"),
        make_table("Ampirik Tedavi Karar Parametreleri", ["Kriter / Kural", "Standart Uygulama", "Gerekçe"], [
            {"cells": [{"text": "Kültür Bekleme", "isMasked": False}, {"text": "Kültür sonucu beklenmez, ampirik başlanır", "isMasked": True, "hint": "sonuç çıkmadan başlama"}, {"text": "Semptomların hızla giderilmesi ve komplikasyonun önlenmesi"}]},
            {"cells": [{"text": "Direnç Eşiği", "isMasked": False}, {"text": "Toplumda direnç >%20 ise seçilmez", "isMasked": True, "hint": "yüzde yirmi barajı"}, {"text": "Ampirik tedavi başarısızlığı riskini önleme"}]},
            {"cells": [{"text": "Floraya Yan Hasar", "isMasked": False}, {"text": "Vajinal ve bağırsak florasını koruma", "isMasked": False}, {"text": "Dirençli bakterilerin ve C. difficile'nin seçilmesini engelleme", "isMasked": False}]}
        ]),
        make_chain("Ampirik Tedavi Başlama Zinciri", [
            "1. Tanı: Dizüri ve pollaküri olan hastada dipstikte lökosit esteraz pozitifleşir.",
            "2. Hızlı Karar: Kültür 48 saat süreceği için beklemeden ampirik ilaç seçilir.",
            "3. Direnç Kontrolü: Bölgesel direnci %20'nin altında olan güvenli ajan belirlenir.",
            "4. Tedavi Başlangıcı: Hasta ilk doz antibiyotiğini derhal alarak rahatlar."
        ]),
        make_recall("Bir bölgede ampirik sistit tedavisinde bir antibiyotiğin kullanılmaması için gereken direnç eşiği nedir?", "Toplumdaki direnç oranının %20'nin üzerinde olmasıdır (>%20 direnç kuralı)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: %20 Direnç Kuralı", [
            {"text": "Kültür şartı aranmaz, tedaviye hemen ampirik başlanır.", "isLie": False, "explanation": "Doğru. Semptomatik hastada beklenmez."},
            {"text": "Toplumda %20'nin üzerinde direnç varsa o antibiyotik ampirik kullanılmamalıdır.", "isLie": False, "explanation": "Doğru. Temel kılavuz kuralıdır."},
            {"text": "Bir antibiyotiğe %99 direnç olsa bile dünyadaki en iyi ampirik ilaçtır.", "isLie": True, "explanation": "Tuzak! Direnç %20'yi aştığında o ilaç ampirik seçenek olmaktan çıkarılır."},
            {"text": "İlacın mesane ve böbrekteki konsantrasyonu tedavi başarısında etkilidir.", "isLie": False, "explanation": "Doğru. Doku penetrasyonu önemlidir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarının ampirik tedavisinde bir antibiyotiğin birinci basamakta tercih EDİLMEMESİ için toplumdaki direnç eşiği ne olmalıdır?", [
            {"key": "A", "text": "Toplumda %20'nin üzerinde direnç bulunması", "isCorrect": True, "explanation": "Ders notunda 'toplumda %20'nin üzerinde direnç varsa o antibiyotiğin ampirik tedavide kullanımından kaçınılmalıdır' kuralı açıkça belirtilmiştir."},
            {"key": "B", "text": "Toplumda %0,01 direnç bulunması", "isCorrect": False, "explanation": "Bu güvenli bir ilaçtır."},
            {"key": "C", "text": "Sadece 1 hastada alerji görülmesi", "isCorrect": False, "explanation": "Toplum direnç eşiği değildir."},
            {"key": "D", "text": "İlacın renginin beyaz olması", "isCorrect": False, "explanation": "Tıbbi kriter değildir."}
        ])
    ]
    slides.append(make_slide(85, "Tedavi İlkeleri ve %20 Direnç Kuralı", "Ampirik tedavi başlangıcı, kültür şartı aranmaması ve %20 direnç eşiği kuralı", "Tedavi İlkeleri", s85_narrative, s85_bullets, s85_elements))

    # Slide 86: Kadınlarda Akut Komplike Olmayan Sistit Tedavi Rejimleri
    s86_narrative = (
        "Ateş ve böğür ağrısı bulunmayan, oral tedavi alabilen kadınlarda akut sistit, kısa süreli "
        "ve üriner sisteme özgü konsantrasyonu yüksek antibiyotiklerle tedavi edilir.\n\n"
        "- **Standart Kısa Rejimler:**\n"
        "  - **Fosfomisin Trometamol:** **3 gram tek doz oral saşe** (pratiktir; ancak erken faz pyelonefrit "
        "şüphesinde doku penetrasyonu yetersiz olduğundan kullanılmamalıdır).\n"
        "  - **TMP-SMX:** **2x160/800 mg dozunda 3 gün** (yerel E. coli direnci <%20 olan bölgelerde).\n"
        "  - **Pivmesillinam:** 800 mg/gün dozunda **5 gün süreyle** verilebilir.\n"
        "- **Kesin Yasak (Ampisilin):** Yüksek direnç (%40-60) nedeniyle **ampisilin veya amoksisilin "
        "tek başına KESİNLİKLE kullanılmamalıdır**.\n\n"
        "> [!IMPORTANT]\n"
        "> Akut sistitte Fosfomisin 3 g tek doz, TMP-SMX 3 gün kullanılır; ampisilin/amoksisilin yüksek direnç nedeniyle tek başına asla tercih edilmez."
    )
    s86_bullets = [
        "Fosfomisin trometamol 3 gram tek doz saşe uygulanır.",
        "TMP-SMX (2x160/800 mg) 3 gün süreyle verilir (direnç <%20 ise).",
        "Ampisilin veya amoksisilin yüksek direnç nedeniyle tek başına KULLANILMAMALIDIR."
    ]
    s86_elements = [
        make_cloze("Kadınlarda akut komplike olmayan sistitte en pratik oral tedavi seçeneği 3 gram tek doz Fosfomisin kullanımıdır.", "Fosfomisin", "Tek saşe şeklinde alınan hücre duvarı inhibitörü"),
        make_table("Akut Komplike Olmayan Sistit Rejimleri", ["Antibiyotik Ajanı", "Doz ve Süre", "Önemli Klinik Not"], [
            {"cells": [{"text": "Fosfomisin Trometamol", "isMasked": False}, {"text": "3 g tek doz oral", "isMasked": True, "hint": "tek saşe doz"}, {"text": "Pyelonefrit şüphesinde yetersizdir, kullanılmaz"}]},
            {"cells": [{"text": "TMP-SMX", "isMasked": False}, {"text": "2x160/800 mg, 3 gün", "isMasked": True, "hint": "üç günlük çift güç tablet"}, {"text": "Lokal direnç <%20 ise ilk tercihlerdendir"}]},
            {"cells": [{"text": "Ampisilin / Amoksisilin", "isMasked": False}, {"text": "TEK BAŞINA KULLANILMAZ", "isMasked": False}, {"text": "Yüksek direnç (%40-60) nedeniyle kontrendikedir", "isMasked": True, "hint": "küresel direnç nedeniyle yasak"}]}
        ]),
        make_chain("Sistit Reçeteleme Algoritması", [
            "1. Doğrulama: Ateş yok, böğür ağrısı yok → Komplike olmayan sistit.",
            "2. Hızlı Seçim: Hasta uyumu için Fosfomisin 3 g tek doz saşe veya TMP-SMX 3 gün verilir.",
            "3. Kontrendikasyon: Ampisilin tek başına kesinlikle reçete edilmez.",
            "4. Yanıtsızlık Kontrolü: 3 günde ateş çıkarsa pyelonefrit açısından revize edilir."
        ]),
        make_recall("Kadınlarda komplike olmayan akut sistit tedavisinde Fosfomisin ve TMP-SMX'in standart kullanım süreleri nedir?", "Fosfomisin 3 gram TEK DOZ; TMP-SMX ise 3 GÜN süreyle kullanılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sistit Tedavisi", [
            {"text": "Fosfomisin komplike olmayan sistitte 3 gram tek doz olarak kullanılır.", "isLie": False, "explanation": "Doğru. Standart dozdur."},
            {"text": "TMP-SMX sistitte 3 gün süreyle verilebilir.", "isLie": False, "explanation": "Doğru. 3 günlük rejimdir."},
            {"text": "Ampisilin tek başına sistit için dünyadaki en kusursuz ve dirençsiz mucize ilaçtır.", "isLie": True, "explanation": "Tuzak! Ampisilin ve amoksisilin %40-60'ı aşan yüksek direnç nedeniyle sistitte TEK BAŞINA KULLANILMAMALIDIR."},
            {"text": "Fosfomisin pyelonefrit şüphesi olan hastalarda kullanılmamalıdır.", "isLie": False, "explanation": "Doğru. Doku penetrasyonu düşüktür."}
        ]),
        make_quiz("Kadınlarda akut komplike olmayan sistit tedavisinde yüksek direnç oranları nedeniyle TEK BAŞINA KULLANILMAMASI gereken antibiyotik hangisidir?", [
            {"key": "A", "text": "Ampisilin veya amoksisilin", "isCorrect": True, "explanation": "Ders notunda 'ampisilin ya da amoksisilin tek başına kullanılmamalıdır' uyarısı açıkça vurgulanmıştır."},
            {"key": "B", "text": "Fosfomisin 3 g tek doz", "isCorrect": False, "explanation": "Önerilen standart rejimdir."},
            {"key": "C", "text": "TMP-SMX (direnç <%20 ise)", "isCorrect": False, "explanation": "Önerilen rejimdir."},
            {"key": "D", "text": "Pivmesillinam 5 gün", "isCorrect": False, "explanation": "Önerilen rejimdir."}
        ])
    ]
    slides.append(make_slide(86, "Kadınlarda Akut Komplike Olmayan Sistit Tedavi Rejimleri", "Fosfomisin 3 g tek doz, TMP-SMX 3 gün ve ampisilin tek başına yasağı", "Tedavi İlkeleri", s86_narrative, s86_bullets, s86_elements))

    # Slide 87: Komplike Sistit Tedavisi ve Gebeler: 7 Gün Kuralı
    s87_narrative = (
        "Altta yatan risk faktörü bulunan komplike sistit olgularında, 3 günlük kısa süreli tedaviler "
        "yetersiz kalarak hızla relaps veya pyelonefrite dönüşür.\n\n"
        "- **7 Gün Tedavi Kuralı:** Gebeler, yaşlı hastalar, diyabetik hastalar, diyafram kullananlar, "
        "yakın zamanda antibiyotik kullananlar ve üriner sistemde anatomik/fonksiyonel anomalisi olanlarda "
        "**tedavi süresi KESİNTİSİZ 7 GÜNDÜR**.\n"
        "- **Gebelerde İlaç Güvenliği:** Gebelikte kinolonlar (kıkırdak hasarı) ve TMP-SMX (teratojenite/kernikterus) "
        "kontrendikedir. Bu nedenle **gebelerde mutlaka beta-laktam grubu bir antibiyotik (veya güvenli sefalosporin)** seçilmelidir.\n"
        "- **Uyumsuzluk Riski:** Komplike sistitte 7 günlük süre tamamlanmadan ilacın kesilmesi derin doku "
        "invazyonunu tetikler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Komplike sistitte (gebe, DM, yaşlı, anomali) tedavi süresi 7 GÜNDÜR; gebelerde yan etkiler nedeniyle beta-laktam antibiyotikler tercih edilir."
    )
    s87_bullets = [
        "Komplike sistitte (gebe, diyabetik, yaşlı, anomali) tedavi süresi 7 GÜNDÜR.",
        "Gebelerde fetal yan etkiler nedeniyle beta-laktam grubu antibiyotikler seçilir.",
        "Kısa süreli 3 günlük tedaviler komplike sistitte kesinlikle uygulanmaz."
    ]
    s87_elements = [
        make_cloze("Gebe veya diyabetik hastalarda komplike sistit tedavisi için önerilen antibiyotik süresi 7 gündür.", "7 gündür", "Yedi günlük komplike tedavi periyodu"),
        make_table("Komplike Sistit Tedavi Protokolü", ["Hasta Grubu", "Önerilen Tedavi Süresi", "İlaç Tercihi İlkesi"], [
            {"cells": [{"text": "Gebeler", "isMasked": False}, {"text": "7 gün", "isMasked": True, "hint": "bir haftalık süre"}, {"text": "Beta-laktam antibiyotikler (sefalosporin vb.)", "isMasked": True, "hint": "gebelikte güvenli ilaç grubu"}]},
            {"cells": [{"text": "Diyabetik / Yaşlı Hasta", "isMasked": False}, {"text": "7 gün", "isMasked": False}, {"text": "Antibiyograma uygun geniş spektrumlu ajanlar", "isMasked": False}]},
            {"cells": [{"text": "Anatomik Anomali", "isMasked": False}, {"text": "7 gün", "isMasked": False}, {"text": "Doku penetrasyonu sağlayan ajanlar", "isMasked": False}]}
        ]),
        make_chain("Komplike Sistit Tedavi Kararı", [
            "1. Risk Tespiti: Kadın hastanın gebe veya diyabetik olduğu saptanır.",
            "2. Süre Kararı: Basit sistit gibi 3 gün değil, tam 7 günlük rejim planlanır.",
            "3. Güvenli Ajan: Gebe ise florokinolonlar elenir; güvenli beta-laktam seçilir.",
            "4. Takip: 7 gün sonunda semptomların tam gerilediği doğrulanır."
        ]),
        make_recall("Gebe veya diyabetik bir kadında sistit geliştiğinde antibiyotik tedavi süresi kaç gün olmalıdır?", "7 gün olmalıdır (komplike sistitte tedavi süresi 7 gündür)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Komplike Sistit Süresi", [
            {"text": "Gebeler ve diyabetik hastalarda sistit için tedavi süresi 7 gündür.", "isLie": False, "explanation": "Doğru. Standart süredir."},
            {"text": "Gebelerde diğer ilaçların yan etkileri nedeniyle beta laktam grubu seçilmelidir.", "isLie": False, "explanation": "Doğru. En güvenli gruptur."},
            {"text": "Gebe kadınlara sistitte sadece 1 saatlik kinolon hapı verilir ve tedavi biter.", "isLie": True, "explanation": "Tuzak! Gebelerde kinolon kontrendikedir ve komplike sistit süresi 7 gündür."},
            {"text": "Yaşlı hastalarda da komplike sistit tedavisi 7 gün uygulanır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("Gebe bir kadında akut sistit saptandığında antibiyotik tedavi süresi ve seçilecek ilaç grubu hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Tedavi süresi 7 gün — Beta-laktam grubu antibiyotik", "isCorrect": True, "explanation": "Ders notunda gebelerde komplike sistit için sürenin 7 gün olduğu ve beta-laktam grubu antibiyotik seçileceği belirtilmiştir."},
            {"key": "B", "text": "Tedavi süresi 1 gün — Florokinolon grubu", "isCorrect": False, "explanation": "Kinolon gebede kontrendikedir."},
            {"key": "C", "text": "Tedavi süresi 1 ay — Doksisiklin", "isCorrect": False, "explanation": "Tetrasiklin gebede kontrendikedir."},
            {"key": "D", "text": "Hiç ilaç verilmez", "isCorrect": False, "explanation": "Gebelikte tedavi şarttır."}
        ])
    ]
    slides.append(make_slide(87, "Komplike Sistit Tedavisi ve Gebeler: 7 Gün Kuralı", "Komplike sistit (gebe, DM, yaşlı), 7 gün kuralı ve gebelerde beta-laktam seçimi", "Tedavi İlkeleri", s87_narrative, s87_bullets, s87_elements))

    # Slide 88: Akut Pyelonefrit Tedavisi: Süre ve Kinolon vs Diğer Ajanlar
    s88_narrative = (
        "Akut pyelonefrit parankimal bir enfeksiyon olduğu için doku konsantrasyonu yüksek ajanlarla "
        "organize edilen daha uzun süreli parenteral veya oral rejimler gerektirir.\n\n"
        "- **Tedavi Süresi Kuralı:** Tedavi süresi **florokinolonlar seçilecekse 7 gün**, kinolon "
        "dışındaki antibiyotiklerle (sefalosporin, aminopenisilin türevleri vb.) **14 gündür**.\n"
        "- **Ayaktan Tedavi Rejimi:** Bölgesel kinolon direnci <%10 ise oral siprofloksasin (2x500 mg, "
        "7 gün) veya levofloksasin (1x750 mg, 5 gün) verilebilir; alternatif olarak tek doz seftriakson "
        "veya aminoglikozid sonrası oral tedaviye geçilir.\n"
        "- **Hastaneye Yatış ve Parenteral Tedavi:** Yüksek ateş, titreme, kusma, oral alamama ve "
        "konfüzyonu olan şiddetli olgular derhal yatırılır; geniş spektrumlu sefalosporin veya aminoglikozid başlanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Akut pyelonefritte tedavi süresi: Florokinolon ile 7 GÜN; kinolon dışı antibiyotiklerle 14 GÜNDÜR!"
    )
    s88_bullets = [
        "Akut pyelonefritte tedavi süresi kinolonlarla 7 gün, diğer ajanlarla 14 gündür.",
        "Kinolon direnci <%10 ise oral siprofloksasin (7 gün) ayaktan verilebilir.",
        "Kusma, oral alamama ve şiddetli sepsis bulgularında hasta hastaneye yatırılmalıdır."
    ]
    s88_elements = [
        make_cloze("Akut pyelonefritte antibiyotik tedavi süresi kinolon seçilirse 7 gün, diğer antibiyotiklerle 14 gündür.", "14 gündür", "Kinolon dışı ilaçlarla iki haftalık tedavi süresi"),
        make_table("Akut Pyelonefrit Tedavi Süreleri", ["Antibiyotik Grubu", "Standart Tedavi Süresi", "Klinik Özellik"], [
            {"cells": [{"text": "Florokinolonlar (Sipro/Levo)", "isMasked": False}, {"text": "7 gün (Levo ile 5 gün)", "isMasked": True, "hint": "yedi günlük kinolon süresi"}, {"text": "Bölgesel direnç <%10 ise tercih edilir"}]},
            {"cells": [{"text": "Kinolon Dışı Ajanlar", "isMasked": False}, {"text": "14 gün (2 hafta)", "isMasked": True, "hint": "on dört günlük süre"}, {"text": "Sefalosporinler, beta-laktamlar"}]},
            {"cells": [{"text": "Yatış Endikasyonu", "isMasked": False}, {"text": "Kusma, konfüzyon, sepsis, oral alamama", "isMasked": False}, {"text": "Parenteral geniş spektrumlu tedavi zorunlu", "isMasked": False}]}
        ]),
        make_chain("Pyelonefrit Tedavi Akışı", [
            "1. Değerlendirme: Ateş ve KVAH olan hasta oral alabiliyor mu?",
            "2. Oral Alabiliyorsa: Siprofloksasin ile 7 günlük tedavi planlanır.",
            "3. Oral Alamıyorsa / Kusuyorsa: Hastaneye yatırılarak IV seftriakson başlanır.",
            "4. Kinolon Dışı İlaç: Seftriakson/beta-laktam seçilmişse süre 14 güne tamamlanır."
        ]),
        make_recall("Akut komplike olmayan pyelonefrit tedavisinde antibiyotik tedavi süreleri kinolonlar ve kinolon dışı ajanlar için kaçar gündür?", "Florokinolonlar ile 7 gün; florokinolon dışındaki antibiyotikler ile 14 gündür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Pyelonefrit Tedavi Süresi", [
            {"text": "Akut pyelonefritte kinolon seçilirse tedavi süresi 7 gündür.", "isLie": False, "explanation": "Doğru. Yüksek doku penetrasyonu vardır."},
            {"text": "Kinolon dışı antibiyotiklerle pyelonefrit tedavi süresi 14 gündür.", "isLie": False, "explanation": "Doğru. 2 haftalık süredir."},
            {"text": "Akut pyelonefritli hasta kussa ve şoka girse bile asla hastaneye yatırılmaz.", "isLie": True, "explanation": "Tuzak! Kusma, oral alamama ve sepsis bulguları mutlak hastaneye yatış endikasyonudur."},
            {"text": "Bölgesel kinolon direnci %10'un altında ise siprofloksasin oral başlanabilir.", "isLie": False, "explanation": "Doğru. Kılavuz kuralıdır."}
        ]),
        make_quiz("Kadınlarda akut komplike olmayan pyelonefrit tedavisinde kinolon DIŞINDAKİ antibiyotikler seçildiğinde önerilen tedavi süresi kaç gündür?", [
            {"key": "A", "text": "14 gün", "isCorrect": True, "explanation": "Ders notunda 'tedavi süresi kinolonlar seçilecekse 7 gün, kinolon dışındaki antibiyotiklerle 14 gündür' açıkça yer almaktadır."},
            {"key": "B", "text": "3 gün", "isCorrect": False, "explanation": "Sistit süresidir."},
            {"key": "C", "text": "1 gün", "isCorrect": False, "explanation": "Yetersizdir."},
            {"key": "D", "text": "6 ay", "isCorrect": False, "explanation": "Reenfeksiyon profilaksisi süresidir."}
        ])
    ]
    slides.append(make_slide(88, "Akut Pyelonefrit Tedavisi: Süre ve Kinolon vs Diğer Ajanlar", "Kinolon ile 7 gün, kinolon dışı ile 14 gün kuralı, yatış kriterleri ve parenteral rejim", "Tedavi İlkeleri", s88_narrative, s88_bullets, s88_elements))

    # Slide 89: Dokuzuncu Bölüm Özeti: Kültür, Görüntüleme ve Tedavi Kriterleri
    s89_narrative = (
        "İdrar kültürü, radyolojik inceleme ve antibiyotik seçim ilkeleri, ÜSE yönetiminin rasyonel "
        "ve kılavuzlara dayalı temel çerçevesini çizer.\n\n"
        "- **Kültür ve Kontaminasyon:** Semptomatik orta akımda tek patojenin ≥10⁵ CFU/ml üremesi "
        "tanısaldır; suprapubikte tek bakteri dahi yeterlidir. Çoklu bakteri, skuamöz epitel ve "
        "laktobasiller kontaminasyonu belgeler; antiseptik kullanımı yalancı negatiftir.\n"
        "- **Radyoloji Kuralı:** Rutin vakalarda görüntüleme GEREKSİZDİR; sadece sepsis, taş, abse ve "
        "amfizem şüphesinde USG/BT istenir.\n"
        "- **Tedavi Protokolleri:** Tedavi ampirik başlanır (%20 direnç barajı); basit sistitte Fosfomisin "
        "tek doz veya TMP-SMX 3 gün; komplike sistitte 7 gün; pyelonefritte kinolonla 7 gün, kinolon dışıyla 14 gündür.\n\n"
        "> [!IMPORTANT]\n"
        "> Sistit (3 gün / tek doz) → Komplike sistit (7 gün) → Pyelonefrit (7-14 gün) → Komplike ÜSE (en az 14 gün) basamaklı süre kuralıdır."
    )
    s89_bullets = [
        "Kültürde ≥10⁵ eşiği; çoklu bakteri, epitel ve laktobasil kontaminasyondur.",
        "Radyoloji rutinde gereksizdir; ampirik tedavide %20 direnç barajı esastır.",
        "Süreler: Sistit 3 gün/tek doz | Komplike sistit 7 gün | Pyelonefrit 7-14 gün."
    ]
    s89_elements = [
        make_cloze("Üriner enfeksiyonlarda ampirik tedavide toplumda direnç oranı %20'nin üzerinde olan antibiyotiklerden kaçınılmalıdır.", "%20'nin üzerinde", "Yüzde yirmi direnç sınırı"),
        make_table("Bölüm 9 Kardinal Süre Özeti", ["Klinik Tablo", "Antibiyotik Seçeneği", "Standart Tedavi Süresi"], [
            {"cells": [{"text": "Basit Sistit", "isMasked": False}, {"text": "Fosfomisin trometamol", "isMasked": True, "hint": "tek saşe"}, {"text": "3 g tek doz oral"}]},
            {"cells": [{"text": "Komplike Sistit (Gebe/DM)", "isMasked": False}, {"text": "Beta-laktam / Sefalosporin", "isMasked": False}, {"text": "7 gün kesintisiz", "isMasked": True, "hint": "bir haftalık süre"}]},
            {"cells": [{"text": "Akut Pyelonefrit", "isMasked": False}, {"text": "Kinolon dışı antibiyotikler", "isMasked": False}, {"text": "14 gün (2 hafta)", "isMasked": True, "hint": "on dört gün"}]}
        ]),
        make_recall("Basit sistit, komplike sistit ve kinolon dışı pyelonefrit için standart tedavi süreleri sırasıyla kaçar gündür?", "Basit sistit: Tek doz (Fosfomisin) veya 3 gün (TMP-SMX); Komplike sistit: 7 gün; Kinolon dışı pyelonefrit: 14 gündür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 9 Özeti", [
            {"text": "İdrar kültüründe tek bakterinin ≥10⁵ CFU/ml üremesi semptomatik hastada tanısaldır.", "isLie": False, "explanation": "Doğru. Standart kriterdir."},
            {"text": "Radyolojik görüntüleme ÜSE'lerin çoğunda gereksizdir.", "isLie": False, "explanation": "Doğru. Rutinde istenmez."},
            {"text": "Akut pyelonefritte kinolon dışı ilaçlarla tedavi süresi sadece 10 dakikadır.", "isLie": True, "explanation": "Tuzak! Pyelonefritte kinolon dışı ajanlarla tedavi süresi tam 14 gündür (2 haftadır)."},
            {"text": "Komplike sistitte tedavi süresi 7 gündür.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."}
        ]),
        make_quiz("Aşağıdaki klinik tablolardan hangisinde standart antibiyotik tedavi süresi 14 GÜNDÜR?", [
            {"key": "A", "text": "Kinolon dışı antibiyotiklerle tedavi edilen akut komplike olmayan pyelonefrit", "isCorrect": True, "explanation": "Ders notunda kinolon dışı pyelonefrit tedavisinin 14 gün olduğu açıkça belirtilmiştir."},
            {"key": "B", "text": "Fosfomisin ile tedavi edilen basit sistit", "isCorrect": False, "explanation": "Tek dozdur."},
            {"key": "C", "text": "TMP-SMX ile tedavi edilen basit sistit", "isCorrect": False, "explanation": "3 gündür."},
            {"key": "D", "text": "Gebelikteki sistit", "isCorrect": False, "explanation": "7 gündür."}
        ])
    ]
    slides.append(make_slide(89, "Dokuzuncu Bölüm Özeti: Kültür, Görüntüleme ve Tedavi Kriterleri", "Kültür kriterleri, kontaminasyon, rutinde radyoloji yasağı ve basamaklı süreler", "Konsolidasyon", s89_narrative, s89_bullets, s89_elements))

    # Slide 90: [TEKRAR SAYFASI - CHECKPOINT 9] Kültür, Radyoloji ve Tedavi Rejimleri
    s90_narrative = (
        "Bu tekrar sayfasında 9. Bölümde işlenen kültür kriterlerini, kontaminasyon ayırıcı tanısını, "
        "radyolojik ilkeleri ve tedavi rejimlerinin süre kurallarını konsolide ediyoruz.\n\n"
        "- **Kültür ve Kontaminasyon:** Semptomatik orta akımda ≥10⁵ CFU/ml tek patojen aranır. "
        "Çoklu bakteri morfolojisi, skuamöz epitel ve laktobasiller kontaminasyondur. Antiseptik yalancı negatiflik yapar.\n"
        "- **Radyoloji ve %20 Kuralı:** Görüntüleme rutinde GEREKSİZDİR (sepsis, taş, abse hariç). "
        "Toplum direnci >%20 olan antibiyotikler ampirik tedavide seçilemez.\n"
        "- **Süreler Özeti:** Basit sistit = 3 gün (TMP-SMX) veya Tek Doz (Fosfomisin 3 g); Komplike "
        "sistit = 7 gün (gebede beta-laktam); Pyelonefrit = Kinolonla 7 gün, Kinolon dışıyla 14 gün!\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] 1) Kültür = ≥10⁵ CFU/ml! 2) Radyoloji = Rutinde gereksiz! 3) Direnç barajı = >%20 ampirik yasak! 4) Sistit = 3 gün/tek doz! 5) Komplike sistit = 7 gün! 6) Pyelonefrit = 7-14 gün!"
    )
    s90_bullets = [
        "Orta akımda ≥10⁵ CFU/ml üreme tanısaldır; antiseptik yalancı negatiftir.",
        "Görüntüleme rutinde gereksizdir; toplum direnci >%20 ise ampirik seçilemez.",
        "Süreler: Sistit 3 gün/tek doz | Komplike sistit 7 gün | Pyelonefrit 7-14 gün."
    ]
    s90_elements = [
        make_cloze("Kadınlarda komplike olmayan akut sistit tedavisinde Fosfomisin 3 gram tek doz saşe olarak uygulanır.", "tek doz", "Bir defalık saşe dozu"),
        make_table("9. Bölüm Büyük Tekrar Tablosu", ["Tanısal / Tedavi Parametresi", "Standart Tıbbi Kural", "Kritik Mesaj"], [
            {"cells": [{"text": "Kültür Tanısal Eşiği", "isMasked": False}, {"text": "Tek patojenin ≥10⁵ CFU/ml üremesi", "isMasked": True, "hint": "yüz bin koloni tek bakteri"}, {"text": "Suprapubikte herhangi bir sayıda basil yeterli"}]},
            {"cells": [{"text": "Ampirik Direnç Kuralı", "isMasked": False}, {"text": "Toplumda direnç >%20 ise kullanılmaz", "isMasked": True, "hint": "yüzde yirmi sınır"}, {"text": "Tedavi başarısızlığını önleme ilkesi"}]},
            {"cells": [{"text": "Komplike Sistit Süresi", "isMasked": False}, {"text": "7 gün kesintisiz tedavi", "isMasked": False}, {"text": "Gebelerde beta-laktam grubu seçilir", "isMasked": True, "hint": "gebelikte güvenli antibiyotik"}]},
            {"cells": [{"text": "Pyelonefrit Süresi", "isMasked": False}, {"text": "Kinolon 7 gün; Kinolon dışı 14 gün", "isMasked": False}, {"text": "Parankim invazyonunun tam eradikasyonu", "isMasked": False}]}
        ]),
        make_chain("9. Bölüm Entegre Tedavi Karar Akışı", [
            "1. Teşhis: Hasta sistit mi, pyelonefrit mi ayrılır.",
            "2. Basit Sistit: Fosfomisin 3 g tek doz veya TMP-SMX 3 gün verilir.",
            "3. Komplike Sistit (Gebe): Beta-laktam ile tam 7 gün tedavi edilir.",
            "4. Pyelonefrit: Kinolonla 7 gün, kinolon dışı parenteral/oral ajanla 14 gün tedavi edilir."
        ]),
        make_recall("Akut komplike olmayan sistit, komplike sistit ve kinolon dışı pyelonefrit tedavilerinin standart süreleri nedir?", "Komplike olmayan sistit: Tek doz (Fosfomisin) veya 3 gün (TMP-SMX); Komplike sistit: 7 gün; Kinolon dışı pyelonefrit: 14 gündür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 9. Bölüm Konsolidasyonu", [
            {"text": "Semptomatik hastada temiz orta akımda tek bakterinin ≥10⁵ CFU/ml üremesi tanısaldır.", "isLie": False, "explanation": "Doğru. Standart kriterdir."},
            {"text": "Toplumda direnç %20'nin üzerindeyse o antibiyotik ampirik kullanılmaz.", "isLie": False, "explanation": "Doğru. Temel direnç kuralıdır."},
            {"text": "Gebelerde sistit tedavisi sadece 5 dakikadır ve kinolonlar zorunlu ilk tercihtir.", "isLie": True, "explanation": "Tuzak! Gebelerde kinolon kontrendikedir, beta-laktamlar seçilir ve komplike sistit süresi tam 7 gündür."},
            {"text": "Pyelonefritte kinolon dışı antibiyotiklerle tedavi süresi 14 gündür.", "isLie": False, "explanation": "Doğru. Ders notu süresidir."}
        ]),
        make_quiz("9. Bölümün temel kazanımlarına göre aşağıdaki tedavi kurallarından hangisi KESİNLİKLE YANLIŞTIR?", [
            {"key": "A", "text": "Gebelerde komplike sistit tedavisi 1 gündür ve kinolonlar ilk seçenektir", "isCorrect": True, "explanation": "Kesinlikle yanlış! Gebelerde komplike sistit süresi 7 gündür; kinolonlar gebelerde kıkırdak hasarı nedeniyle kontrendikedir, beta-laktamlar seçilir."},
            {"key": "B", "text": "Basit sistitte Fosfomisin trometamol 3 gram tek doz olarak uygulanabilir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Akut pyelonefritte kinolon dışı antibiyotiklerle tedavi süresi 14 gündür", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Toplumda direnci %20'nin üzerinde olan antibiyotikler ampirik tedavide seçilmemelidir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(90, "[TEKRAR SAYFASI - CHECKPOINT 9] Kültür, Radyoloji ve Tedavi Rejimleri", "9. Bölümün kapsamlı pekiştirmesi: kültür eşiği, %20 direnç, sistit, komplike sistit ve pyelonefrit süreleri", "Bölüm Tekrarı", s90_narrative, s90_bullets, s90_elements))

    return slides
