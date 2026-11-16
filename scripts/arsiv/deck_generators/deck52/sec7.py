# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec7():
    slides = []

    # Slide 61: Asemptomatik Bakteriüri (ABU) Tanımı
    s61_narrative = (
        "Asemptomatik bakteriüri (ABU), idrarda mikrobiyal üreme saptanmasına rağmen konağın "
        "herhangi bir klinik yakınma sergilemediği özel bir kolonizasyon tablosudur.\n\n"
        "- **Temel Tanım:** Asemptomatik bakteriüri tanımı; **üriner sistem semptomu olmaması, "
        "piyüri bulunabilmesi ve idrar kültüründe ≥10⁵ CFU/mL üropatojen mikroorganizma üremesi**dir.\n"
        "- **Semptomsuzluk:** Hastada dizüri, pollaküri, sıkışma hissi, ateş veya yan ağrısı "
        "gibi hiçbir lokal veya sistemik enfeksiyon belirtisi yer almaz.\n"
        "- **Piyüri Varlığı:** İdrarda lökosit (piyüri) bulunması ABU tanısını dışlamaz; asemptomatik "
        "bireylerin önemli bir kısmında düşük düzeyde piyüri eşlik edebilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Asemptomatik bakteriüri tanımı: Üriner sistem semptomu olmaması, piyüri ve idrar kültüründe ≥10⁵ CFU/mL üropatojen üremesidir."
    )
    s61_bullets = [
        "ABU tanımı: Üriner sistem semptomu olmaması.",
        "İdrar analizinde piyüri eşlik edebilir.",
        "İdrar kültüründe ≥10⁵ CFU/mL üropatojen mikroorganizma üremesi saptanır."
    ]
    s61_elements = [
        make_cloze("Asemptomatik bakteriüri tanımı üriner sistem semptomu olmaması, piyüri ve kültürde ≥10⁵ CFU/mL üropatojen üremesidir.", "≥10⁵ CFU/mL", "Asemptomatik bakteriürideki kantitatif koloni eşik değeri"),
        make_table("Asemptomatik Bakteriüri Tanı Kriterleri", ["Kriter Bileşeni", "Klinik Durum", "Önemi"], [
            {"cells": [{"text": "Klinik Semptomlar", "isMasked": False}, {"text": "Semptom bulunmaz", "isMasked": True, "hint": "şikayetsiz tablo"}, {"text": "Enfeksiyondan ziyade kolonizasyon"}]},
            {"cells": [{"text": "Piyüri Durumu", "isMasked": False}, {"text": "Bulunabilir (+/-)", "isMasked": False}, {"text": "Tanıyı dışlamaz veya tedavi gerektirmez", "isMasked": True, "hint": "tedavi endikasyonu doğurmaz"}]},
            {"cells": [{"text": "Kültür Koloni Sayısı", "isMasked": False}, {"text": "≥10⁵ CFU/mL üreme", "isMasked": True, "hint": "yüz bin koloni eşiği"}, {"text": "Anlamlı bakteriüri kanıtı"}]}
        ]),
        make_chain("ABU Tanı Mantığı", [
            "1. Semptom Sorgusu: Üriner şikayet bulunmadığının teyidi.",
            "2. İdrar Analizi: Piyürinin eşlik edebileceğinin bilinmesi.",
            "3. Kültür Değerlendirmesi: ≥10⁵ CFU/mL üropatojen üremesi saptanması.",
            "4. ABU Teşhisi: Özel endikasyon yoksa tedavi verilmeden izlenmesi."
        ]),
        make_recall("Ders notuna göre asemptomatik bakteriürinin (ABU) tanı kriterleri nelerdir?", "Üriner sistem semptomu olmaması, piyüri bulunabilmesi ve idrar kültüründe ≥10⁵ CFU/mL üropatojen üremesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ABU Tanımı", [
            {"text": "Asemptomatik bakteriüride üriner sistem semptomu bulunmaz.", "isLie": False, "explanation": "Doğru. Temel özelliğidir."},
            {"text": "İdrar kültüründe ≥10⁵ CFU/mL üropatojen üremesi aranır.", "isLie": False, "explanation": "Doğru. Sayısal eşiktir."},
            {"text": "ABU tanısı koymak için hastanın mutlaka 40 derece ateşle yoğun bakımda yatması şarttır.", "isLie": True, "explanation": "Tuzak! Ateş ve semptom varsa tablo ABU değil, semptomatik enfeksiyon veya sepsistir; ABU semptomsuzdur."},
            {"text": "ABU'da idrarda piyüri görülebilir.", "isLie": False, "explanation": "Doğru. Piyüri eşlik edebilir."}
        ]),
        make_quiz("Asemptomatik bakteriürinin (ABU) temel klinik ve mikrobiyolojik tanımı aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Üriner sistem semptomu olmaması, piyüri ve idrar kültüründe ≥10⁵ CFU/mL üropatojen üremesi", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Asemptomatik bakteriüri tanımı: üriner sistem semptomu olmaması; piyüri; idrar kültüründe ≥10⁵ CFU/mL üropatojen mikroorganizma üremesi' denmektedir."},
            {"key": "B", "text": "Ağır yan ağrısı ve idrarda sıfır bakteri bulunması", "isCorrect": False, "explanation": "Bakteriüri olmadan ABU olmaz."},
            {"key": "C", "text": "Yalnızca idrarda kan görülmesi ve kültürün steril olması", "isCorrect": False, "explanation": "Bu hematüridir."},
            {"key": "D", "text": "Her gün 10 litre idrar çıkarma hissi", "isCorrect": False, "explanation": "Poliüridir, ABU tanımı değildir."}
        ])
    ]
    slides.append(make_slide(61, "Asemptomatik Bakteriüri (ABU) Tanımı", "Üriner semptomsuzluk, piyüri ve ≥10⁵ CFU/mL mikrobiyolojik tanı kriteri", "Asemptomatik Bakteriüri", s61_narrative, s61_bullets, s61_elements))

    # Slide 62: Kadınlarda ABU Tanısı: Ardışık İki Kültür Kuralı
    s62_narrative = (
        "Kadın anatomisinde perineal ve periüretral floranın dış idrar yolu ağzına yakınlığı, tek bir "
        "idrar kültüründe saptanan üremenin kontaminasyona bağlı olma olasılığını belirgin biçimde artırır.\n\n"
        "- **Kadınlarda Tanı Kuralı:** Kadınlarda asemptomatik bakteriüri tanısı koyabilmek için "
        "**24-48 saat arayla gönderilen ardışık iki idrar kültüründe** aynı üropatojenin ≥10⁵ CFU/mL üremesi şarttır.\n"
        "- **Yalancı Pozitiflikten Kaçınma:** Tek bir kültürde üreme saptandığında hastaların yaklaşık "
        "%20-40'ında ikinci kültür negatif çıkmaktadır; bu nedenle ardışık iki kültür zorunludur.\n"
        "- **Aynı Etken Kriteri:** İki kültürde de aynı tür mikroorganizmanın izole edilmesi, tablonun "
        "geçici bir genital kontaminasyon değil, gerçek bir mesane kolonizasyonu olduğunu doğrular.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kadınlarda ABU tanısı için: 24-48 saat arayla gönderilen ardışık iki idrar kültüründe aynı etkenin ≥10⁵ CFU/mL üremesi gereklidir."
    )
    s62_bullets = [
        "Kadınlarda ABU: 24-48 saat arayla gönderilen ardışık iki idrar kültürü gereklidir.",
        "Her iki kültürde de aynı üropatojenin ≥10⁵ CFU/mL üremesi aranır.",
        "Ardışık iki kültür kuralı genital flora kontaminasyonunu dışlamak için zorunludur."
    ]
    s62_elements = [
        make_cloze("Kadınlarda ABU tanısı için 24-48 saat arayla gönderilen ardışık iki idrar kültüründe aynı üropatojenin üremesi şarttır.", "24-48 saat arayla", "İki idrar kültürü arasındaki zaman aralığı"),
        make_table("Kadınlarda ABU Doğrulama Protokolü", ["İnceleme Aşaması", "Kültür Zamanlaması", "Beklenen Mikrobiyolojik Sonuç"], [
            {"cells": [{"text": "1. İdrar Kültürü", "isMasked": False}, {"text": "Başlangıç örneği", "isMasked": False}, {"text": "≥10⁵ CFU/mL üropatojen üremesi", "isMasked": True, "hint": "ilk kültür pozitifliği"}]},
            {"cells": [{"text": "2. İdrar Kültürü", "isMasked": False}, {"text": "24-48 saat sonra ardışık örnek", "isMasked": True, "hint": "ikinci teyit kültürü"}, {"text": "Aynı etkenin ≥10⁵ CFU/mL üremesi"}]}
        ]),
        make_chain("Kadında ABU Tanı Zinciri", [
            "1. İlk Kültür: Semptomsuz kadında tesadüfi ≥10⁵ CFU/mL üreme.",
            "2. Bekleme: 24-48 saatlik aranın verilmesi.",
            "3. İkinci Kültür: İkinci idrar örneğinin gönderilmesi.",
            "4. Doğrulama: Aynı bakterinin tekrar ≥10⁵ CFU/mL üremesiyle tanı konması."
        ]),
        make_recall("Kadınlarda asemptomatik bakteriüri tanısı koyabilmek için kaç saat arayla kaç kültür gönderilmelidir?", "24-48 saat arayla gönderilen ardışık iki idrar kültüründe üreme olmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kadında ABU Kuralı", [
            {"text": "Kadınlarda ABU için 24-48 saat arayla ardışık iki kültür istenir.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Her iki kültürde de aynı etkenin ≥10⁵ CFU/mL üremesi aranır.", "isLie": False, "explanation": "Doğru. Doğrulama kriteridir."},
            {"text": "Kadınlarda tek bir damla idrar analiz şeridine değer değmez derhal ABU kesin tanısı konur ve 10 yıl hapis cezası verilir.", "isLie": True, "explanation": "Tuzak! Kadınlarda kontaminasyonu ekarte etmek için 24-48 saat arayla 2 ardışık kültür şarttır."},
            {"text": "İki kültür kuralı perineal kontaminasyonu dışlamayı amaçlar.", "isLie": False, "explanation": "Doğru. Yalancı pozitifliği önler."}
        ]),
        make_quiz("Kadınlarda asemptomatik bakteriüri tanısının kesinleştirilmesi için gereken idrar kültürü protokolü aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "24-48 saat arayla gönderilen ardışık iki idrar kültüründe ≥10⁵ CFU/mL üreme", "isCorrect": True, "explanation": "Ders notunda parantez içinde '(kadınlarda 24-48 saat arayla gönderilen ardışık iki idrar kültüründe)' olarak belirtilmiştir."},
            {"key": "B", "text": "Aynı gün içinde 5 dakika arayla alınan 10 kültür", "isCorrect": False, "explanation": "Protokol bu değildir."},
            {"key": "C", "text": "Sadece 1 kez alınan idrar strip testi", "isCorrect": False, "explanation": "Kültür ile doğrulama şarttır."},
            {"key": "D", "text": "Yılda bir kez gönderilen tek bir kan kültürü", "isCorrect": False, "explanation": "İdrar kültürü gerekir."}
        ])
    ]
    slides.append(make_slide(62, "Kadınlarda ABU: Ardışık İki Kültür Protokolü", "Kadınlarda kontaminasyon riskini dışlayan 24-48 saat aralıklı iki kültür kuralı", "Asemptomatik Bakteriüri", s62_narrative, s62_bullets, s62_elements))

    # Slide 63: Proteus mirabilis ve Enfeksiyon Taşları
    s63_narrative = (
        "Asemptomatik veya semptomatik bakteriüri takiplerinde idrarda sürekli olarak belirli "
        "bir bakterinin üremesi, altta yatan yapısal bir patolojinin göstergesidir.\n\n"
        "- **Kritik Kural:** İdrar kültüründe **üreaz üreten bakteri (ör. Proteus mirabilis) sürekli "
        "ürüyorsa taş oluşumu dışlanmalıdır**.\n"
        "- **Taş Oluşum Mekanizması:** Proteus mirabilis güçlü üreaz aktivitesiyle idrardaki üreyi "
        "parçalayıp idrarı aşırı alkali hale getirerek magnezyum amonyum fosfat (struvit) taşları oluşturur.\n"
        "- **Bakteriyel Sığınak:** Bakteriler oluşan taşın çatlakları ve iç katmanları içine gömülerek "
        "antibiyotiklerden ve immün sistemden korunur; bu nedenle taş cerrahi olarak temizlenmedikçe üreme kesilmez.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Üreaz üreten bakteri (ör. Proteus mirabilis) sürekli ürüyorsa üriner sistemde taş oluşumu mutlaka dışlanmalıdır."
    )
    s63_bullets = [
        "Proteus mirabilis gibi üreaz üreten bakteriler sürekli ürüyorsa taş dışlanmalıdır.",
        "Üreaz idrarı alkalileştirerek struvit (magnezyum amonyum fosfat) taşlarını oluşturur.",
        "Taş varlığı bakteriye sığınak oluşturarak inatçı bakteriüriye neden olur."
    ]
    s63_elements = [
        make_cloze("İdrarda üreaz üreten bakteri (ör. Proteus mirabilis) sürekli ürüyorsa taş oluşumu dışlanmalıdır.", "taş oluşumu", "Proteus'un sürekli üremesinde ekarte edilmesi zorunlu ürolojik patoloji"),
        make_table("Proteus ve Taş Bağıntısı", ["Bakteriyel Özellik", "Biyokimyasal Etki", "Klinik Zorunluluk"], [
            {"cells": [{"text": "Proteus mirabilis", "isMasked": False}, {"text": "Güçlü üreaz üretimi", "isMasked": True, "hint": "üre yıkan enzim"}, {"text": "Sürekli üreme kaynağı"}]},
            {"cells": [{"text": "Alkali İdrar Ortamı", "isMasked": False}, {"text": "Struvit taş presipitasyonu", "isMasked": False}, {"text": "Taş oluşumunun dışlanması", "isMasked": True, "hint": "ürolojik görüntüleme şartı"}]}
        ]),
        make_chain("Proteus ve Taş İkilemi", [
            "1. İdrar Kültürü: Proteus mirabilis'in persistan/sürekli üremesi.",
            "2. Biyokimyasal Şüphe: Üreaz kaynaklı alkali idrar ortamı.",
            "3. Tanısal Karar: Üriner sistem görüntülemesi ile taş araştırılması.",
            "4. Tedavi: Taşın çıkarılması olmadan bakteriürinin kürlenemeyeceğinin bilinmesi."
        ]),
        make_recall("İdrar kültüründe üreaz üreten bir bakteri (ör. Proteus mirabilis) sürekli ürüyorsa hangi patoloji mutlaka dışlanmalıdır?", "Üriner sistem taş oluşumu mutlaka dışlanmalıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Proteus ve Taş", [
            {"text": "Proteus mirabilis üreaz üreten bir bakteridir.", "isLie": False, "explanation": "Doğru. Tipik özelliğidir."},
            {"text": "Üreaz üreten bakteri sürekli ürüyorsa taş oluşumu dışlanmalıdır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Proteus mirabilis üremesi hastada böbrek taşlarının tamamen eridiğini ve yok olduğunu kanıtlar.", "isLie": True, "explanation": "Tuzak! Tam aksine Proteus struvit taşlarının oluşumuna yol açar, taş varlığı dışlanmalıdır."},
            {"text": "Bakteriler taş matrisi içinde antibiyotiklerden saklanabilir.", "isLie": False, "explanation": "Doğru. İnatçı üremenin nedenidir."}
        ]),
        make_quiz("İdrar kültüründe Proteus mirabilis gibi üreaz üreten bir bakterinin sürekli üremesi durumunda aşağıdaki klinik patolojilerden hangisi MUTLAKA dışlanmalıdır?", [
            {"key": "A", "text": "Taş oluşumu", "isCorrect": True, "explanation": "Ders notunda 'Üreaz üreten bakteri (ör. Proteus mirabilis) sürekli ürüyorsa taş oluşumu dışlanmalıdır' denmektedir."},
            {"key": "B", "text": "Akut apandisit", "isCorrect": False, "explanation": "Proteus üreazı ile ilişkili değildir."},
            {"key": "C", "text": "Mide perforasyonu", "isCorrect": False, "explanation": "Üriner patoloji değildir."},
            {"key": "D", "text": "Demir eksikliği anemisi", "isCorrect": False, "explanation": "Hematolojik bir tablodur."}
        ])
    ]
    slides.append(make_slide(63, "Proteus mirabilis ve Taş Oluşumu Riski", "Persistan üreaz pozitif üremede enfeksiyon taşlarının dışlanması zorunluluğu", "Asemptomatik Bakteriüri", s63_narrative, s63_bullets, s63_elements))

    # Slide 64: Erkekte Bakteriüri: Dijital Rektal Muayene ve Prostatit
    s64_narrative = (
        "Erkeklerde anatomik koruma nedeniyle asemptomatik veya semptomatik bakteriüri son derece "
        "nadir bir durumdur ve arkasında her zaman özel bir odak aranmalıdır.\n\n"
        "- **Klinik Muayene:** Erkekte prostat ilişkili hastalığı dışlamak adına mutlaka **dijital "
        "rektal muayene (DRM)** yapılmalıdır.\n"
        "- **Genç Erkekte Nadirlik:** Genç erkekte bakteriüri ve ÜSE **nadirdir**; saptanırsa "
        "**kronik bakteriyel prostatit** düşünülmelidir.\n"
        "- **Prostat Odağı:** Prostat kanalları bakteriler için korunaklı bir rezervuar oluşturur; "
        "prostatit varlığında bakteriler buradan periyodik olarak idrara dökülerek tekrarlayan bakteriüriye yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> Erkekte bakteriüri saptandığında prostatı değerlendirmek için dijital rektal muayene yapılmalıdır; genç erkekte nadirdir, saptanırsa kronik bakteriyel prostatit düşünülmelidir."
    )
    s64_bullets = [
        "Erkekte prostat hastalığını dışlamak adına dijital rektal muayene yapılmalıdır.",
        "Genç erkekte bakteriüri nadirdir; saptanırsa kronik bakteriyel prostatit düşünülür.",
        "Prostat bezi tekrarlayan ve inatçı bakteriürilerin başlıca gizli odağıdır."
    ]
    s64_elements = [
        make_cloze("Erkekte bakteriüri varlığında prostat ilişkili hastalığı dışlamak adına dijital rektal muayene yapılmalıdır.", "dijital rektal muayene", "Prostat bezini parmakla değerlendiren fizik muayene yöntemi"),
        make_table("Erkekte Bakteriüri Değerlendirmesi", ["Hasta Profili", "Klinik Özellik", "Düşünülmesi Gereken Tanı"], [
            {"cells": [{"text": "Genç Erkek", "isMasked": False}, {"text": "Bakteriüri nadirdir", "isMasked": True, "hint": "seyrek görülen durum"}, {"text": "Kronik bakteriyel prostatit"}]},
            {"cells": [{"text": "Fizik Muayene", "isMasked": False}, {"text": "Dijital rektal muayene (DRM)", "isMasked": False}, {"text": "Prostat hassasiyeti ve büyüklüğü", "isMasked": True, "hint": "prostat tutulumunun tespiti"}]}
        ]),
        make_chain("Erkekte Bakteriüri İnceleme Akışı", [
            "1. İdrar Kültürü: Erkek hastada bakteriüri saptanması.",
            "2. Nadirlik Analizi: Genç erkekte bu tablonun nadir olduğunun fark edilmesi.",
            "3. Rektal Muayene: Dijital rektal muayene ile prostatın palpe edilmesi.",
            "4. Tanı: Kronik bakteriyel prostatit odağının teşhis edilmesi."
        ]),
        make_recall("Erkek hastada bakteriüri saptandığında hangi fizik muayene yapılmalıdır ve genç erkekte ne düşünülmelidir?", "Dijital rektal muayene yapılmalıdır; genç erkekte saptanırsa kronik bakteriyel prostatit düşünülmelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erkekte Bakteriüri", [
            {"text": "Erkekte prostat hastalığını dışlamak için dijital rektal muayene yapılmalıdır.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Genç erkekte bakteriüri nadirdir.", "isLie": False, "explanation": "Doğru. %1'in altındadır."},
            {"text": "Genç erkekte bakteriüri görüldüğünde kronik bakteriyel prostatit düşünülmelidir.", "isLie": False, "explanation": "Doğru. Önemli bir odaktır."},
            {"text": "Erkeklerde prostat bezi diye bir organ yoktur, bu nedenle muayene yasaktır.", "isLie": True, "explanation": "Tuzak! Erkekte prostat bezi mevcuttur ve dijital rektal muayene ile değerlendirilmelidir."}
        ]),
        make_quiz("Genç bir erkek hastada idrar kültüründe anlamlı bakteriüri saptanması durumunda ders notuna göre öncelikle hangi tanı düşünülmeli ve hangi muayene yapılmalıdır?", [
            {"key": "A", "text": "Kronik bakteriyel prostatit düşünülmeli; dijital rektal muayene yapılmalıdır", "isCorrect": True, "explanation": "Ders notunda 'Erkekte prostat ilişkili hastalığı dışlamak adına dijital rektal muayene yapılmalıdır; genç erkekte nadirdir, saptanırsa kronik bakteriyel prostatit düşünülmelidir' denmektedir."},
            {"key": "B", "text": "Menenjit düşünülmeli; lomber ponksiyon yapılmalıdır", "isCorrect": False, "explanation": "Üriner sistemle ilgisizdir."},
            {"key": "C", "text": "Osteomiyelit düşünülmeli; kemik sintigrafisi çekilmelidir", "isCorrect": False, "explanation": "Kemik enfeksiyonu değildir."},
            {"key": "D", "text": "Akut glomerülonefrit düşünülmeli; böbrek biyopsisi yapılmalıdır", "isCorrect": False, "explanation": "Öncelikli tanı prostatittir."}
        ])
    ]
    slides.append(make_slide(64, "Erkekte Bakteriüri ve Prostatik Muayene", "Dijital rektal muayenenin rolü ve genç erkekte kronik bakteriyel prostatit", "Asemptomatik Bakteriüri", s64_narrative, s64_bullets, s64_elements))

    # Slide 65: Tekrarlayan ÜSE: Relaps Tanımı ve Mekanizması
    s65_narrative = (
        "Tekrarlayan üriner sistem enfeksiyonları, nüksün zamanlamasına ve izole edilen mikroorganizmaya "
        "bağlı olarak relaps ve reenfeksiyon olmak üzere iki temel kategoriye ayrılır.\n\n"
        "- **Relaps Tanımı:** Tedaviden sonraki **iki hafta içinde (≤2 hafta) aynı mikroorganizmayla** "
        "enfeksiyonun tekrarlanmasıdır.\n"
        "- **Tedavi Başarısızlığı:** Relaps, verilen antibiyotiğin bakteriyi dokudan tamamen eradike "
        "edemediğini ve bakterinin doku derinliklerinde saklanarak yeniden alevlendiğini gösterir.\n"
        "- **İlişkili Patolojiler:** Relaps tabloları tipik olarak **renal tutulum (üst sistem odağı), "
        "üriner sistemde yapısal/fonksiyonel anormallik veya erkekte kronik prostatit** ile ilişkilidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Relaps: Tedaviden sonraki 2 hafta içinde aynı mikroorganizmayla gelişen nükstür; renal tutulum, yapısal anormallik veya kronik prostatitle ilişkilidir."
    )
    s65_bullets = [
        "Relaps: Tedaviden sonraki iki hafta içinde aynı mikroorganizmayla tekrarlamadır.",
        "Renal tutulum, yapısal veya fonksiyonel anormalliklerle ilişkilidir.",
        "Erkek hastalarda kronik prostatit odağını düşündürür."
    ]
    s65_elements = [
        make_cloze("Tedaviden sonraki iki hafta içinde aynı mikroorganizmayla enfeksiyonun tekrarlamasına relaps adı verilir.", "iki hafta içinde", "Relaps tanımı için geçerli kritik zaman sınırı"),
        make_table("Relapsın Klinik ve Patolojik Özellikleri", ["Parametre", "Tanımlayıcı Kriter", "Klinik Yansıması"], [
            {"cells": [{"text": "Zaman Sınırı", "isMasked": False}, {"text": "Tedaviden sonraki ≤2 hafta", "isMasked": True, "hint": "iki haftalık süre"}, {"text": "Erken dönemde nüks"}]},
            {"cells": [{"text": "Mikrobiyolojik Etken", "isMasked": False}, {"text": "Birebir AYNI mikroorganizma", "isMasked": False}, {"text": "Eradikasyon yetersizliği", "isMasked": True, "hint": "mikrobun temizlenememesi"}]},
            {"cells": [{"text": "Altta Yatan Odak", "isMasked": False}, {"text": "Renal tutulum, anormallik, prostatit", "isMasked": True, "hint": "derin doku saklanma odakları"}, {"text": "Yapısal araştırma gereksinimi"}]}
        ]),
        make_chain("Relaps Patofizyolojik Akışı", [
            "1. İlk Enfeksiyon: ÜSE atağının antibiyotik ile tedavi edilmesi.",
            "2. Yetersiz Eradikasyon: Bakterinin parankimde veya prostatta saklanması.",
            "3. 2 Hafta İçinde Alevlenme: Antibiyotik bitiminden sonra hızla çoğalma.",
            "4. Relaps Tanısı: Aynı bakteriyle 2 hafta içinde enfeksiyon nüksü."
        ]),
        make_recall("Tekrarlayan ÜSE'de 'relaps' tanımı süre, etken ve ilişkili durumlar açısından nedir?", "Tedaviden sonraki iki hafta içinde aynı mikroorganizmayla gelişen enfeksiyondur; renal tutulum, yapısal/fonksiyonel anormallik veya kronik prostatit ile ilişkilidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Relaps", [
            {"text": "Relaps tedaviden sonraki iki hafta içinde tekrarlamadır.", "isLie": False, "explanation": "Doğru. Zaman kriteridir."},
            {"text": "Relapsta etken aynı mikroorganizmadır.", "isLie": False, "explanation": "Doğru. Aynı bakteridir."},
            {"text": "Relaps renal tutulum veya kronik prostatit ile ilişkili olabilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Tedaviden 15 yıl sonra farklı bir bakteriyle enfeksiyon gelişmesi kesin relapstır.", "isLie": True, "explanation": "Tuzak! Relaps ≤2 hafta içinde ve aynı mikroorganizmayla olur; bu tablo reenfeksiyondur."}
        ]),
        make_quiz("Tekrarlayan üriner sistem enfeksiyonlarında 'relaps' tanımı ve ilişkili klinik durumlar aşağıdakilerden hangisinde eksiksiz verilmiştir?", [
            {"key": "A", "text": "Tedaviden sonraki iki hafta içinde aynı mikroorganizmayla tekrarlama (renal tutulum, anormallik veya kronik prostatit)", "isCorrect": True, "explanation": "Ders notundaki eksiksiz relaps tanımıdır."},
            {"key": "B", "text": "Tedaviden en az 6 ay sonra farklı bir virüsle enfeksiyon", "isCorrect": False, "explanation": "Bu relaps değildir."},
            {"key": "C", "text": "Yalnızca böbrek taşı düşüren hastalarda görülen hematüri", "isCorrect": False, "explanation": "Relaps tanımı değildir."},
            {"key": "D", "text": "İki hafta içinde tamamen iyileşip bir daha asla hasta olmama", "isCorrect": False, "explanation": "Tam tersine relaps nükstür."}
        ])
    ]
    slides.append(make_slide(65, "Tekrarlayan ÜSE: Relaps Tanımı ve Odakları", "Tedaviden sonraki ≤2 hafta içinde aynı mikroorganizmayla nüks mekanizması", "Tekrarlayan ÜSE", s65_narrative, s65_bullets, s65_elements))

    # Slide 66: Tekrarlayan ÜSE: Reenfeksiyon Tanımı ve Özellikleri
    s66_narrative = (
        "Tekrarlayan üriner enfeksiyonların büyük çoğunluğunu oluşturan reenfeksiyon, tedavi "
        "başarısızlığından ziyade konağın yeni bir kolonizasyon atağına maruz kalmasını ifade eder.\n\n"
        "- **Reenfeksiyon Tanımı:** Tedaviden **en az iki hafta sonra farklı mikroorganizma veya "
        "aynı mikroorganizmanın farklı suşuyla** gelişen yeni enfeksiyondur.\n"
        "- **Kür Kanıtı:** İlk enfeksiyon tamamen iyileşmiş ve idrar steril hale gelmiştir; ancak "
        "perineal floradan mesaneye tırmanan yeni bir suş yeni bir enfeksiyon atağı başlatmıştır.\n"
        "- **Kadın Yatkınlığı:** Reenfeksiyonlar özellikle genç ve cinsel aktif kadınlarda anatomik "
        "yatkınlık ve cinsel aktivite nedeniyle oldukça yaygın gözlenir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Reenfeksiyon: Tedaviden en az iki hafta sonra farklı mikroorganizma veya aynı mikroorganizmanın farklı suşuyla gelişen yeni enfeksiyondur."
    )
    s66_bullets = [
        "Reenfeksiyon: Tedaviden en az iki hafta sonra gelişen yeni enfeksiyondur.",
        "Etken farklı mikroorganizma veya aynı mikroorganizmanın farklı suşudur.",
        "Önceki enfeksiyon kürlenmiştir; dışarıdan yeni bir kolonizasyon söz konusudur."
    ]
    s66_elements = [
        make_cloze("Tedaviden en az iki hafta sonra farklı mikroorganizma veya farklı suşla gelişen enfeksiyona reenfeksiyon adı verilir.", "farklı mikroorganizma", "Yeni atağı oluşturan farklı etken özelliği"),
        make_table("Relaps ve Reenfeksiyon Karşılaştırma Tablosu", ["Özellik", "Relaps", "Reenfeksiyon"], [
            {"cells": [{"text": "Zaman Sınırı", "isMasked": False}, {"text": "Tedaviden sonra ≤2 hafta", "isMasked": True, "hint": "iki hafta içinde"}, {"text": "Tedaviden sonra en az 2 hafta"}]},
            {"cells": [{"text": "Etken Mikroorganizma", "isMasked": False}, {"text": "AYNI mikroorganizma", "isMasked": False}, {"text": "Farklı mikroorganizma veya farklı suş", "isMasked": True, "hint": "yeni ve değişik suş"}]},
            {"cells": [{"text": "Patolojik Mekanizma", "isMasked": False}, {"text": "Doku eradikasyon yetersizliği", "isMasked": True, "hint": "iyileşemeyen derin odak"}, {"text": "Yeni eksojen kolonizasyon atağı"}]}
        ]),
        make_chain("Reenfeksiyon Gelişim Süreci", [
            "1. Başarılı Tedavi: İlk enfeksiyonun antibiyotikle tamamen kürlenmesi.",
            "2. İki Haftalık Aralık: İdrarın steril kaldığı semptomsuz dönem.",
            "3. Yeni Kolonizasyon: Perineden mesaneye farklı bir bakterinin girişi.",
            "4. Reenfeksiyon: En az iki hafta sonra yeni etkenle akut enfeksiyon atağı."
        ]),
        make_recall("Tekrarlayan ÜSE'de 'reenfeksiyon' tanımı süre ve etken özellikleri açısından nedir?", "Tedaviden en az iki hafta sonra farklı mikroorganizma veya aynı mikroorganizmanın farklı suşuyla gelişen yeni enfeksiyondur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Reenfeksiyon", [
            {"text": "Reenfeksiyon tedaviden en az iki hafta sonra gelişir.", "isLie": False, "explanation": "Doğru. Zaman eşiğidir."},
            {"text": "Reenfeksiyonda etken farklı mikroorganizma veya farklı suştur.", "isLie": False, "explanation": "Doğru. Yeni bir mikroptur."},
            {"text": "Reenfeksiyon daima aynı gün içinde aynı bakteriyle gelişen tek bir saniyelik tablodur.", "isLie": True, "explanation": "Tuzak! Aynı bakteriyle erken gelişen relapstır; reenfeksiyon en az 2 hafta sonra ve farklı etkenle olur."},
            {"text": "Reenfeksiyon kadınlarda sık görülen bir tekrarlayan enfeksiyon formudur.", "isLie": False, "explanation": "Doğru. Çok yaygındır."}
        ]),
        make_quiz("Tekrarlayan üriner sistem enfeksiyonlarında 'reenfeksiyon' kavramı aşağıdakilerden hangisinde doğru tanımlanmıştır?", [
            {"key": "A", "text": "Tedaviden en az iki hafta sonra farklı mikroorganizma veya aynı mikroorganizmanın farklı suşuyla gelişen yeni enfeksiyon", "isCorrect": True, "explanation": "Ders notundaki harfiyen reenfeksiyon tanımıdır."},
            {"key": "B", "text": "Tedaviden sonraki 2 gün içinde aynı mikroorganizmayla gelişen enfeksiyon", "isCorrect": False, "explanation": "Bu relapstır."},
            {"key": "C", "text": "Hiçbir zaman bakteri içermeyen psikolojik idrar hissi", "isCorrect": False, "explanation": "Reenfeksiyon gerçek bakteriyel enfeksiyondur."},
            {"key": "D", "text": "Yalnızca böbrek nakli yapılan hastalarda görülen rejeksiyon", "isCorrect": False, "explanation": "Graft rejeksiyonu ile ilgisizdir."}
        ])
    ]
    slides.append(make_slide(66, "Tekrarlayan ÜSE: Reenfeksiyon Tanımı", "Tedaviden ≥2 hafta sonra farklı etken veya farklı suşla yeni enfeksiyon gelişimi", "Tekrarlayan ÜSE", s66_narrative, s66_bullets, s66_elements))

    # Slide 67: Profilaksi Endikasyonu: ≥3 Atak/Yıl ve Kadınlarda Yapısal Durum
    s67_narrative = (
        "Sık tekrarlayan üriner sistem enfeksiyonları hastanın yaşam kalitesini bozar, iş gücü "
        "kaybına yol açar ve sürekli antibiyotik kullanımına bağlı direnç gelişimini tetikler.\n\n"
        "- **Profilaksi Eşiği:** Tekrarlayan ÜSE olgularında **yılda 3 veya daha fazla (≥3 atak/yıl)** "
        "atak geçirilmesi durumunda antimikrobiyal profilaksi düşünülür.\n"
        "- **Alternatif 6 Aylık Eşik:** Benzer şekilde son 6 ayda ≥2 atak geçirilmesi de tekrarlayan "
        "ÜSE sınıflamasına girer ve koruyucu yaklaşım gerektirir.\n"
        "- **Kadınlarda Yapısal Durum:** Kadınlarda tekrarlayan ÜSE **yapısal/fonksiyonel anormallik "
        "olmadan da görülebilir**; yani tamamen normal anatomisi olan kadınlarda da sık nüksler yaşanabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Tekrarlayan ÜSE'de ≥3 atak/yıl durumunda profilaksi düşünülür; kadınlarda yapısal/fonksiyonel anormallik olmadan da görülebilir."
    )
    s67_bullets = [
        "≥3 atak/yıl durumunda antimikrobiyal profilaksi düşünülür.",
        "Kadınlarda yapısal veya fonksiyonel anormallik olmadan da sık görülebilir.",
        "Koruyucu profilaksi hastanın atak sıklığını ve antibiyotik yükünü azaltmayı hedefler."
    ]
    s67_elements = [
        make_cloze("Tekrarlayan ÜSE'de yılda ≥3 atak/yıl saptanması durumunda antimikrobiyal profilaksi düşünülür.", "≥3 atak/yıl", "Profilaksi endikasyonu doğuran yıllık atak sayısı eşiği"),
        make_table("Tekrarlayan ÜSE ve Profilaksi Kriterleri", ["Kriter", "Tanımlayıcı Eşik / Durum", "Klinik Yönetim"], [
            {"cells": [{"text": "Yıllık Atak Sayısı", "isMasked": False}, {"text": "≥3 atak/yıl", "isMasked": True, "hint": "yılda üç veya daha fazla"}, {"text": "Profilaksi düşünülür"}]},
            {"cells": [{"text": "Kadınlarda Anatomi", "isMasked": False}, {"text": "Yapısal/fonksiyonel anormallik OLMADAN da görülür", "isMasked": True, "hint": "anomali şart değildir"}, {"text": "Normal anatomide de nüks olabilir"}]}
        ]),
        make_chain("Profilaksi Karar Basamakları", [
            "1. Atak Sayımı: Hastanın son bir yıldaki kanıtlanmış ÜSE ataklarının sayılması.",
            "2. Eşik Kontrolü: Yılda ≥3 atak (veya 6 ayda ≥2 atak) olduğunun tespiti.",
            "3. Anatomik İnceleme: Kadında anomali olmasa dahi riskin sürdüğünün bilinmesi.",
            "4. Profilaksi Başlanması: Uygun profilaktik antibiyotik stratejisinin seçilmesi."
        ]),
        make_recall("Tekrarlayan ÜSE'de profilaksi düşünülmesi için gereken yıllık atak sayısı nedir ve kadınlarda yapısal anomali şart mıdır?", "≥3 atak/yıl durumunda profilaksi düşünülür; kadınlarda yapısal/fonksiyonel anormallik olmadan da görülebilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Profilaksi Eşiği", [
            {"text": "Tekrarlayan ÜSE'de ≥3 atak/yıl durumunda profilaksi düşünülür.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Kadınlarda yapısal anormallik olmadan da tekrarlayan ÜSE görülebilir.", "isLie": False, "explanation": "Doğru. Anatomi normal olabilir."},
            {"text": "Profilaksi kararı vermek için hastanın yılda en az 5000 kez pyelonefrit geçirmesi şarttır.", "isLie": True, "explanation": "Tuzak! Profilaksi eşiği yılda 3 veya daha fazla (≥3 atak/yıl) ataktır."},
            {"text": "Tekrarlayan enfeksiyonlar hayat kalitesini bozar.", "isLie": False, "explanation": "Doğru. Klinik öneme sahiptir."}
        ]),
        make_quiz("Tekrarlayan üriner sistem enfeksiyonlarında antimikrobiyal profilaksi düşünülmesi için gereken yıllık atak eşiği ve kadınlardaki anatomik özellik aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "≥3 atak/yıl; kadınlarda yapısal/fonksiyonel anormallik olmadan da görülebilir", "isCorrect": True, "explanation": "Ders notunda açıkça '≥3 atak/yıl durumunda profilaksi düşünülür; kadınlarda yapısal/fonksiyonel anormallik olmadan da görülebilir' denmektedir."},
            {"key": "B", "text": "≥100 atak/yıl; sadece böbreği tek olan kadınlarda görülür", "isCorrect": False, "explanation": "Eşikler ve anatomik kural yanlıştır."},
            {"key": "C", "text": "Yılda sadece 1 atak; mutlaka mesane kanseri eşlik etmelidir", "isCorrect": False, "explanation": "Profilaksi eşiği 3 ataktır."},
            {"key": "D", "text": "Hiçbir zaman profilaksi verilmez", "isCorrect": False, "explanation": "Tekrarlayan ÜSE'de profilaksi endikedir."}
        ])
    ]
    slides.append(make_slide(67, "Profilaksi Endikasyonu ve Kadında Yapısal Durum", "≥3 atak/yıl eşiği, profilaksi endikasyonu ve yapısal anormalliksiz nüksler", "Tekrarlayan ÜSE", s67_narrative, s67_bullets, s67_elements))

    # Slide 68: Asemptomatik Bakteriüride Tedavi Yaklaşımı Genel İlkeleri
    s68_narrative = (
        "Asemptomatik bakteriüri saptanan her hastaya antibiyotik verilmesi, modern tıpta "
        "antibiyotik direncinin yayılmasındaki en büyük hatalardan biridir.\n\n"
        "- **Genel İlke:** Asemptomatik bakteriüri, kanıtlanmış çok sınırlı özel durumlar haricinde "
        "**tedavi edilmemelidir**.\n"
        "- **Zararları:** ABU'nun gereksiz tedavisi; çok ilaca dirençli bakterilerin seçilmesine, "
        "Clostridioides difficile kolitine ve ileride daha agresif semptomatik enfeksiyonlara yol açar.\n"
        "- **Ders Notu Kapsamı:** Bu bölümde ABU tanımı (≥10⁵ CFU/mL) ve kadınlardaki iki kültür kuralı "
        "öğrenilmiş olup, spesifik tedavi endikasyonları ilerleyen klinik bölümlerde ele alınacaktır.\n\n"
        "> [!NOTE]\n"
        "> Asemptomatik bakteriüri genel popülasyonda benign bir durumdur; özel endikasyonlar dışındaki hastalarda antibiyotik tedavisi önerilmez."
    )
    s68_bullets = [
        "ABU genel kural olarak tedavi edilmez; gereksiz antibiyotik direnç doğurur.",
        "Tanı kriteri semptomsuz hastada ≥10⁵ CFU/mL üremedir.",
        "Özel tedavi endikasyonları dışındaki hastalarda rutin antibiyotik verilmemelidir."
    ]
    s68_elements = [
        make_cloze("Asemptomatik bakteriüride genel ilke özel endikasyonlar haricinde antibiyotik ile tedavi edilmemesidir.", "tedavi edilmemesidir", "Gereksiz antibiyotik kullanımını engelleyen temel tıp ilkesi"),
        make_table("ABU Tedavi Yaklaşım İlkeleri", ["Klinik Durum", "Yaklaşım", "Gerekçe"], [
            {"cells": [{"text": "Genel Popülasyonda ABU", "isMasked": False}, {"text": "Tedavi ÖNERİLMEZ", "isMasked": True, "hint": "ilaç verilmemesi kuralı"}, {"text": "Direnç ve yan hasarı önleme"}]},
            {"cells": [{"text": "Gereksiz Tedavi Sonucu", "isMasked": False}, {"text": "ÇİD patojen seçilimi ve C. difficile", "isMasked": False}, {"text": "Mikrobiyomun bozulması", "isMasked": True, "hint": "flora hasarı ve süperenfeksiyon"}]}
        ]),
        make_chain("ABU Klinik Değerlendirme Zinciri", [
            "1. İdrar Tahlili ve Kültür: Semptomsuz hastada ≥10⁵ CFU/mL üreme.",
            "2. Semptom Teyidi: Ateş, dizüri veya yan ağrısı olmadığının doğrulanması.",
            "3. Endikasyon Taraması: Gebelik veya ürolojik işlem gibi özel durum var mı?",
            "4. Karar: Özel endikasyon yoksa antibiyotik vermeden izlem."
        ]),
        make_recall("Genel popülasyonda asemptomatik bakteriüriye yaklaşımın temel ilkesi nedir?", "Özel endikasyonlar haricinde tedavi edilmemesi (antibiyotik verilmemesi) esastır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ABU Genel Yaklaşım", [
            {"text": "Genel popülasyonda ABU rutin olarak tedavi edilmez.", "isLie": False, "explanation": "Doğru. Temel enfeksiyon ilkesidir."},
            {"text": "Gereksiz antibiyotik kullanımı dirençli bakterilerin seçilmesine yol açar.", "isLie": False, "explanation": "Doğru. Ekolojik yan hasardır."},
            {"text": "İdrarında semptomsuz bakteri üreyen herkes ömür boyu damardan 10 antibiyotik almalıdır.", "isLie": True, "explanation": "Tuzak! ABU genel popülasyonda zararsızdır ve tedavi edilmez."},
            {"text": "ABU tanısında semptomsuzluk ve ≥10⁵ CFU/mL eşiği esastır.", "isLie": False, "explanation": "Doğru. Tanım kriteridir."}
        ]),
        make_quiz("Asemptomatik bakteriürinin (ABU) genel klinik yönetimi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Özel endikasyonlar haricinde rutin antibiyotik tedavisi verilmemelidir", "isCorrect": True, "explanation": "ABU genel kural olarak tedavi edilmez, direnç gelişimini önlemek için izlenir."},
            {"key": "B", "text": "Her ABU hastası derhal acil ameliyata alınmalıdır", "isCorrect": False, "explanation": "Cerrahi endikasyon değildir."},
            {"key": "C", "text": "ABU saptanan tüm hastalar yoğun bakıma yatırılmalıdır", "isCorrect": False, "explanation": "Yatış endikasyonu değildir."},
            {"key": "D", "text": "Hastalara antibiyotik yerine sadece saf alkol içirilmelidir", "isCorrect": False, "explanation": "Tıbbi tedavi değildir."}
        ])
    ]
    slides.append(make_slide(68, "Asemptomatik Bakteriüride Tedavi İlkeleri", "Gereksiz antibiyotik kullanımından kaçınma ve kolonizasyon yönetimi", "Asemptomatik Bakteriüri", s68_narrative, s68_bullets, s68_elements))

    # Slide 69: Yedinci Bölüm Özeti: ABU ve Tekrarlayan ÜSE
    s69_narrative = (
        "Asemptomatik bakteriüri tanısal kriterleri, relaps ve reenfeksiyon ayrımları ile profilaksi "
        "endikasyonları yedinci bölümün temel klinik kazanımlarını oluşturur.\n\n"
        "- **ABU Tanımı:** Semptom olmaması, piyüri ve **≥10⁵ CFU/mL** üremedir; kadınlarda **24-48 saat "
        "arayla ardışık iki kültürde** aynı etken aranır.\n"
        "- **Taş ve Prostat:** Proteus mirabilis sürekli ürüyorsa **taş oluşumu** dışlanmalı; erkekte "
        "bakteriüri varsa **dijital rektal muayene** yapılmalı ve genç erkekte **kronik prostatit** düşünülmelidir.\n"
        "- **Tekrarlayan ÜSE:** Relaps **≤2 hafta içinde aynı mikroorganizmayla**; reenfeksiyon **≥2 hafta "
        "sonra farklı mikroorganizmayla** gelişir; **≥3 atak/yıl** profilaksi endikasyonudur.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] ABU: ≥10⁵ CFU/mL (kadında 2 kültür); Proteus'ta taş, erkekte prostatit dışlanmalı; Relaps ≤2 hafta aynı etken, Reenfeksiyon ≥2 hafta farklı etken; Profilaksi eşiği ≥3 atak/yıldır."
    )
    s69_bullets = [
        "ABU: Semptomsuz, ≥10⁵ CFU/mL; kadınlarda 24-48 saat arayla 2 kültür.",
        "Proteus mirabilis sürekli ürüyorsa taş oluşumu dışlanmalıdır.",
        "Erkekte dijital rektal muayene; genç erkekte kronik prostatit düşünülür.",
        "Relaps ≤2 hafta (aynı etken); Reenfeksiyon ≥2 hafta (farklı etken); Profilaksi ≥3 atak/yıl."
    ]
    s69_elements = [
        make_cloze("Tekrarlayan ÜSE'de relaps tedaviden sonraki iki hafta içinde aynı mikroorganizmayla gelişirken profilaksi eşiği ≥3 atak/yıl olarak tanımlanır.", "iki hafta içinde", "Relapsın zaman kriteri"),
        make_table("7. Bölüm Büyük Karşılaştırma Matrisi", ["Kavram", "Tanısal Kriter / Zaman", "Klinik Mesaj"], [
            {"cells": [{"text": "Kadında ABU", "isMasked": False}, {"text": "24-48 saat arayla 2 kültürde ≥10⁵ CFU/mL", "isMasked": True, "hint": "iki ardışık kültür"}, {"text": "Kontaminasyon dışlanmalı"}]},
            {"cells": [{"text": "Relaps", "isMasked": False}, {"text": "≤2 hafta içinde AYNI etken", "isMasked": False}, {"text": "Renal tutulum, yapısal anormallik, prostatit", "isMasked": True, "hint": "derin odak ilişkisi"}]},
            {"cells": [{"text": "Reenfeksiyon", "isMasked": False}, {"text": "≥2 hafta sonra FARKLI etken/suş", "isMasked": True, "hint": "farklı bakteriyle yeni atak"}, {"text": "Yeni eksojen kolonizasyon"}]},
            {"cells": [{"text": "Profilaksi Eşiği", "isMasked": False}, {"text": "≥3 atak/yıl", "isMasked": False}, {"text": "Kadında anormallik olmadan da olabilir", "isMasked": True, "hint": "profilaksi endikasyonu"}]}
        ]),
        make_chain("7. Bölüm Karar Algoritması", [
            "1. ABU Tanısı: Kadında 24-48 saat arayla 2 kültürde ≥10⁵ CFU/mL.",
            "2. Odak Taraması: Proteus'ta taş, erkekte DRM ile prostatit araştırma.",
            "3. Nüks Tipi: ≤2 hafta aynı etken (relaps) vs ≥2 hafta farklı (reenfeksiyon).",
            "4. Profilaksi: Yılda ≥3 atak varsa profilaktik tedavi planlama."
        ]),
        make_recall("Yedinci bölümün temel kazanımı olarak relaps ile reenfeksiyon arasındaki iki temel fark nedir?", "Süre farkı (relaps ≤2 hafta, reenfeksiyon ≥2 hafta) ve etken farkıdır (relaps aynı bakteri, reenfeksiyon farklı bakteri veya farklı suş)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 7 Özeti", [
            {"text": "Kadınlarda ABU için 24-48 saat arayla iki kültürde ≥10⁵ CFU/mL üreme aranır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Proteus mirabilis sürekli ürüyorsa taş oluşumu dışlanmalıdır.", "isLie": False, "explanation": "Doğru. Üreaz ve taş bağıntısıdır."},
            {"text": "Relaps ve reenfeksiyon tamamen aynı şeydir, aralarında hiçbir zaman ve etken farkı yoktur.", "isLie": True, "explanation": "Tuzak! Relaps ≤2 hafta içinde aynı etkenle; reenfeksiyon ≥2 hafta sonra farklı etkenle gelişir."},
            {"text": "Tekrarlayan ÜSE'de ≥3 atak/yıl durumunda profilaksi düşünülür.", "isLie": False, "explanation": "Doğru. Profilaksi eşiğidir."}
        ]),
        make_quiz("Yedinci bölümde işlenen ABU ve tekrarlayan ÜSE bilgileri değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Relaps tedavisinden 6 ay sonra tamamen farklı bir mikroorganizmayla gelişen enfeksiyondur", "isCorrect": True, "explanation": "Yanlış! Bu reenfeksiyondur; relaps tedaviden sonraki 2 hafta içinde aynı mikroorganizmayla gelişir."},
            {"key": "B", "text": "Kadınlarda ABU tanısı için 24-48 saat arayla gönderilen ardışık iki kültürde ≥10⁵ CFU/mL üreme gereklidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Üreaz üreten bakteri sürekli ürüyorsa taş oluşumu dışlanmalıdır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Tekrarlayan ÜSE'de ≥3 atak/yıl durumunda profilaksi düşünülür", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(69, "Yedinci Bölüm Özeti: ABU ve Tekrarlayan ÜSE", "ABU kriterleri, Proteus-taş ilişkisi, relaps-reenfeksiyon ve profilaksi özeti", "Bölüm Özeti", s69_narrative, s69_bullets, s69_elements))

    # Slide 70: [TEKRAR SAYFASI - CHECKPOINT 7] Asemptomatik Bakteriüri ve Tekrarlayan ÜSE
    s70_narrative = (
        "Bu tekrar sayfasında 7. Bölümde işlenen ABU tanı kriterlerini, taş/prostatit bağlantılarını, "
        "relaps-reenfeksiyon ayrımlarını ve profilaksi endikasyonunu pekiştiriyoruz.\n\n"
        "- **ABU Tanımı:** Semptomsuzluk, piyüri ve **≥10⁵ CFU/mL** üropatojen üremesidir; kadınlarda "
        "**24-48 saat arayla iki kültür** istenir.\n"
        "- **Özel Odaklar:** Proteus mirabilis sürekli ürüyorsa **taş oluşumu**; erkekte bakteriüride "
        "**dijital rektal muayene** ve genç erkekte **kronik prostatit** araştırılmalıdır.\n"
        "- **Relaps vs Reenfeksiyon:** Relaps **≤2 hafta içinde aynı mikroorganizmayla** (renal/prostatik odak); "
        "Reenfeksiyon **≥2 hafta sonra farklı etkenle**; Profilaksi **≥3 atak/yıl** (kadında anomali olmadan da görülebilir).\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 7] ABU: ≥10⁵ CFU/mL (kadında 24-48 saat arayla 2 kültür); Proteus'ta taş, erkekte prostatit dışlanmalı; Relaps ≤2 hafta aynı etken, Reenfeksiyon ≥2 hafta farklı etken; Profilaksi ≥3 atak/yıldır."
    )
    s70_bullets = [
        "ABU: Semptomsuz, ≥10⁵ CFU/mL; kadında 24-48 saat arayla 2 kültür.",
        "Proteus sürekli ürüyorsa taş; erkekte bakteriüri varsa prostatit dışlanmalıdır.",
        "Relaps: ≤2 hafta içinde aynı mikroorganizmayla.",
        "Reenfeksiyon: ≥2 hafta sonra farklı etken veya suşla.",
        "Profilaksi: ≥3 atak/yıl (kadında yapısal anormallik olmadan da olabilir)."
    ]
    s70_elements = [
        make_cloze("Asemptomatik bakteriüri tanısında kadınlarda 24-48 saat arayla ardışık iki kültürde ≥10⁵ CFU/mL üreme aranırken profilaksi için ≥3 atak/yıl gereklidir.", "≥10⁵ CFU/mL", "ABU mikrobiyolojik tanı eşiği"),
        make_table("7. Bölüm Büyük Tekrar Tablosu", ["Kavram", "Tanı Eşiği / Kriter", "Klinik Özellik"], [
            {"cells": [{"text": "Kadında ABU Kriteri", "isMasked": False}, {"text": "24-48 saat arayla 2 kültürde ≥10⁵ CFU/mL", "isMasked": True, "hint": "iki ardışık kültür eşiği"}, {"text": "Kontaminasyon kontrolü"}]},
            {"cells": [{"text": "Proteus Sürekli Üremesi", "isMasked": False}, {"text": "Taş oluşumu dışlanmalı", "isMasked": False}, {"text": "Üreaz ve struvit taş riski", "isMasked": True, "hint": "enfeksiyon taşı şüphesi"}]},
            {"cells": [{"text": "Relaps Tanımı", "isMasked": False}, {"text": "≤2 hafta içinde AYNI etken", "isMasked": True, "hint": "erken aynı bakteri nüksü"}, {"text": "Renal veya prostatik derin odak"}]},
            {"cells": [{"text": "Reenfeksiyon Tanımı", "isMasked": False}, {"text": "≥2 hafta sonra FARKLI etken", "isMasked": False}, {"text": "Yeni eksojen süperenfeksiyon", "isMasked": True, "hint": "yeni bakteri girişi"}]},
            {"cells": [{"text": "Profilaksi Endikasyonu", "isMasked": False}, {"text": "≥3 atak/yıl", "isMasked": True, "hint": "yıllık nüks eşiği"}, {"text": "Kadında anomalisiz de görülebilir"}]}
        ]),
        make_chain("7. Bölüm Sentez Zinciri", [
            "1. ABU Tanımı: Semptomsuz hastada ≥10⁵ CFU/mL (kadında 2 kültür).",
            "2. Gizli Odak: Proteus'ta taş, erkekte dijital muayene ile prostatit arama.",
            "3. Nüks Analizi: ≤2 hafta aynı (relaps) vs ≥2 hafta farklı (reenfeksiyon).",
            "4. Profilaksi Eşiği: Yılda ≥3 atak durumunda profilaktik tedaviye geçiş."
        ]),
        make_recall("Checkpoint 7: Kadınlarda ABU doğrulama kriteri, relapsın zaman/etken kuralı ve profilaksi eşiği nedir?", "Kadında 24-48 saat arayla 2 kültürde ≥10⁵ CFU/mL; relaps ≤2 hafta içinde aynı mikroorganizmayla; profilaksi eşiği ise ≥3 atak/yıldır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 7 Konsolidasyonu", [
            {"text": "Kadınlarda ABU tanısı için 24-48 saat arayla ardışık iki kültürde ≥10⁵ CFU/mL üreme aranır.", "isLie": False, "explanation": "Doğru. 7. bölümün temel kuralıdır."},
            {"text": "Proteus mirabilis sürekli ürüyorsa taş oluşumu dışlanmalıdır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Tekrarlayan ÜSE'de profilaksi ancak yılda en az 100 atak geçirilirse düşünülür.", "isLie": True, "explanation": "Tuzak! Profilaksi düşünülme eşiği yılda 3 veya daha fazla (≥3 atak/yıl) ataktır."},
            {"text": "Relaps ≤2 hafta içinde aynı etkenle, reenfeksiyon ≥2 hafta sonra farklı etkenle gelişir.", "isLie": False, "explanation": "Doğru. İki tanımın temel farkıdır."}
        ]),
        make_quiz("7. Bölümün tamamı (Asemptomatik Bakteriüri ve Tekrarlayan ÜSE) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Proteus mirabilis sürekli ürüyorsa hastanın hiçbir tetkike ihtiyacı yoktur, bu durum tamamen normaldir", "isCorrect": True, "explanation": "Yanlış! Proteus mirabilis sürekli ürüyorsa taş oluşumu mutlaka dışlanmalıdır."},
            {"key": "B", "text": "Kadınlarda ABU tanısı için 24-48 saat arayla gönderilen iki kültürde ≥10⁵ CFU/mL üreme aranır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Relaps tedaviden sonraki iki hafta içinde aynı mikroorganizmayla tekrarlamadır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Tekrarlayan ÜSE'de ≥3 atak/yıl durumunda profilaksi düşünülür", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(70, "[TEKRAR SAYFASI - CHECKPOINT 7] Asemptomatik Bakteriüri ve Tekrarlayan ÜSE", "7. Bölümün kapsamlı pekiştirmesi: ABU kriterleri, Proteus-taş, relaps/reenfeksiyon ve profilaksi", "Bölüm Tekrarı", s70_narrative, s70_bullets, s70_elements))

    return slides
