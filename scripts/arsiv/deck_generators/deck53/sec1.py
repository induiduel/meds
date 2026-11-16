# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec1():
    slides = []

    # Slide 1: Menstrüel Siklusun Biyolojik Anlamı ve Tanımı
    s1_narrative = (
        "Dişi üreme sisteminde her ay ortalama bir yumurta olgunlaşarak döllenmeye hazırlanır "
        "ve uterus iç tabakası olası bir gebelik için yapısal olarak kalınlaşır.\n\n"
        "- **Döngüsel Yenilenme:** Döllenme gerçekleşmediğinde, döllenmemiş yumurta hücresi ile "
        "gebelik için hazırlanmış olan endometrial fonksiyonel tabaka yıkılarak dışarı atılır.\n"
        "- **Süre ve Periyodisite:** Yaklaşık 28 gün süren bu biyolojik evreye **menstrual siklus** "
        "(menstrüel döngü) adı verilir.\n"
        "- **Fonksiyonel Tabaka Atılımı:** Her dört haftada bir meydana gelen siklik vajinal kanamalar, "
        "endometriumun yüzeyel fonksiyonel tabakasının dökülmesi ile karakterizedir.\n\n"
        "> [!NOTE]\n"
        "> Menstrüel siklus, overlerdeki foliküler gelişim ile uterus iç tabakasındaki dokusal yenilenmenin senkronize döngüsüdür."
    )
    s1_bullets = [
        "Dişi üreme sisteminde ortalama ayda bir yumurta olgunlaşır ve döllenmeye hazırlanır.",
        "Döllenme olmazsa döllenmemiş yumurta ve hazırlanan endometrium yıkılarak dışarı atılır.",
        "Yaklaşık 28 gün süren bu evre menstrual siklustur; yüzeyel fonksiyonel tabaka atılır."
    ]
    s1_elements = [
        make_cloze("Yaklaşık 28 gün süren bu biyolojik evreye menstrual siklus adı verilir.", "menstrual siklus", "Dişi üreme döngüsünün tıbbi adı"),
        make_table("Menstrüel Siklusun Temel Nitelikleri", ["Özellik", "Fizyolojik Değer", "Klinik Anlamı"], [
            {"cells": [{"text": "Ortalama Döngü Süresi", "isMasked": False}, {"text": "Yaklaşık 28 gün", "isMasked": True, "hint": "aylık döngü periyodu"}, {"text": "Fizyolojik ritmik periyot"}]},
            {"cells": [{"text": "Dökülen Doku", "isMasked": False}, {"text": "Yüzeyel fonksiyonel tabaka", "isMasked": False}, {"text": "Gebeliksiz siklusun kanamayla sonlanması", "isMasked": True, "hint": "uterus iç örtüsünün atılması"}]}
        ]),
        make_chain("Siklusun Temel Döngü Basamakları", [
            "1. Hazırlık: Overde yumurta olgunlaşırken endometrium kalınlaşır.",
            "2. Döllenme Yokluğu: Gebelik oluşmadığında hormonal destek aniden çekilir.",
            "3. Dokusal Yıkım: Fonksiyonel tabaka iskemik nekroza uğrar.",
            "4. Dökülme: Döllenmemiş yumurta ve kanayan doku vajinadan atılır."
        ]),
        make_recall("Menstrüel siklusta her dört haftada bir gerçekleşen kanamanın dokusal kaynağı nedir?", "Endometriumun yüzeyel fonksiyonel tabakasının (stratum functionale) dökülmesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Menstrüel Siklus Tanımı", [
            {"text": "Menstrüel döngü ortalama 28 gün süren fizyolojik bir süreçtir.", "isLie": False, "explanation": "Doğru. Klasik fizyolojik süre 28 gündür."},
            {"text": "Döllenme gerçekleşmediğinde hazırlanan fonksiyonel tabaka yıkılarak dışarı atılır.", "isLie": False, "explanation": "Doğru. Siklusun temel amacı gebeliğe hazırlıktır."},
            {"text": "Menstrüel kanama sırasında endometriumun tüm myometrium tabakası tamamen dökülür.", "isLie": True, "explanation": "Tuzak! Dökülen tabaka sadece endometriumun yüzeyel fonksiyonel tabakasıdır; myometrium kas tabakasıdır ve dökülmez."},
            {"text": "Her ay ortalama bir yumurta hücresi olgunlaşarak döllenmeye hazırlanır.", "isLie": False, "explanation": "Doğru. Monofoliküler gelişim esastır."}
        ]),
        make_quiz("Menstrüel siklus sırasında her dört haftada bir gerçekleşen kanamanın kaynağı olan doku tabakası hangisidir?", [
            {"key": "A", "text": "Endometriumun yüzeyel fonksiyonel tabakası", "isCorrect": True, "explanation": "Menstrüel kanama fonksiyonel tabakanın dökülmesiyle meydana gelir."},
            {"key": "B", "text": "Myometriumun orta sirküler kas lifleri", "isCorrect": False, "explanation": "Myometrium kas tabakasıdır, kanamayla dökülmez."},
            {"key": "C", "text": "Perimetriumun seroza zarı", "isCorrect": False, "explanation": "Perimetrium en dış örtüdür."},
            {"key": "D", "text": "Endometriumun çoğalmayı sağlayan derin bazal tabakası", "isCorrect": False, "explanation": "Bazal tabaka dökülmez, rejenerasyonu sağlar."}
        ])
    ]
    slides.append(make_slide(1, "Menstrüel Siklusun Biyolojik Anlamı ve Tanımı", "Dişi üreme döngüsü, fonksiyonel tabakanın hazırlanışı ve menstrüel atılım", "Fizyoloji ve Anatomi", s1_narrative, s1_bullets, s1_elements))

    # Slide 2: Hormonal Kontrol Ekseni: Hipotalamus, Hipofiz ve Over
    s2_narrative = (
        "Menstrüel siklus boyunca endometriumdaki yapısal değişimler ve fonksiyonel tabakanın "
        "yeniden oluşumu over hormonlarının sıkı denetimi altındadır.\n\n"
        "- **Hormonal Hiyerarşi:** Overlerin tüm endokrin işlevleri hipotalamus ve hipofiz bezi "
        "tarafından hiyerarşik bir eksenle kontrol edilir.\n"
        "- **Hipotalamik Düzenleyici:** Hipotalamustan pulsatil biçimde salgılanan primer hormon **GnRH**'tır "
        "(Gonadotropin Releasing Hormone).\n"
        "- **Hipofiz Ön Lob Hormonları:** GnRH uyarısıyla adenohipofizden salgılanan gonadotropinler **FSH ve LH**'tır.\n"
        "- **Ovaryum Yanıtı:** Hipofiz gonadotropinlerinin denetiminde overlerden salgılanan steroid hormonlar "
        "ise **östrojen ve progesteron**dur.\n\n"
        "> [!IMPORTANT]\n"
        "> [HORMONAL EKSEN] Hipotalamus (GnRH) → Hipofiz (FSH, LH) → Ovaryum (Östrojen, Progesteron) ekseni menstrüel döngünün ana motorudur."
    )
    s2_bullets = [
        "Endometrium değişimleri overden salgılanan östrojen ve progesteron etkisi altındadır.",
        "Over fonksiyonları hipotalamus ve hipofiz hormonları tarafından kontrol edilir.",
        "Hipotalamus hormonu GnRH; hipofiz hormonları FSH ve LH; over hormonları östrojen ve progesterondur."
    ]
    s2_elements = [
        make_cloze("Hipotalamusun hormonu GnRH; hipofiz hormonları FSH ve LH; ovaryum hormonları östrojen ve progesterondur.", "östrojen ve progesterondur", "Overden salgılanan steroid hormonlar"),
        make_table("Hipotalamo-Hipofizer-Ovaryal Eksen", ["Organ / Doku", "Salgılanan Primer Hormon", "Hedef Organ"], [
            {"cells": [{"text": "Hipotalamus", "isMasked": False}, {"text": "GnRH", "isMasked": True, "hint": "gonadotropin salgılatıcı hormon"}, {"text": "Hipofiz ön lobu"}]},
            {"cells": [{"text": "Hipofiz Bezi", "isMasked": False}, {"text": "FSH ve LH", "isMasked": False}, {"text": "Ovaryum folikül ve luteal hücreleri", "isMasked": True, "hint": "yumurtalık dokusu"}]},
            {"cells": [{"text": "Ovaryum", "isMasked": False}, {"text": "Östrojen ve Progesteron", "isMasked": False}, {"text": "Uterus endometriumu ve hedef dokular"}]}
        ]),
        make_chain("Endokrin Kontrol İletim Zinciri", [
            "1. Hipotalamus: GnRH salgılayarak portal dolaşıma verir.",
            "2. Hipofiz: GnRH uyarısıyla FSH ve LH gonadotropinlerini üretir.",
            "3. Ovaryum: Gonadotropinlerin etkisiyle östrojen ve progesteron sentezler.",
            "4. Endometrium: Steroid hormonların etkisiyle proliferasyon ve sekretuar farklılaşma gösterir."
        ]),
        make_recall("Hipofiz denetiminde overden salgılanarak endometriumu yöneten iki primer hormon hangisidir?", "Östrojen ve progesterondur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hormonal Kontrol Ekseni", [
            {"text": "Hipotalamusun kontrol hormonu GnRH'tır.", "isLie": False, "explanation": "Doğru. GnRH hipotalamustan salgılanır."},
            {"text": "Hipofiz ön lobundan salgılanan gonadotropinler FSH ve LH'tır.", "isLie": False, "explanation": "Doğru. Gonadotropik hormonlardır."},
            {"text": "Östrojen ve progesteron doğrudan hipotalamus nöronları tarafından üretilip kana verilir.", "isLie": True, "explanation": "Tuzak! Östrojen ve progesteron over hormonlarıdır; hipotalamusun hormonu GnRH'tır."},
            {"text": "Endometriumdaki yapısal değişimler over hormonlarının etkisi altındadır.", "isLie": False, "explanation": "Doğru. Hedef doku endometriumdur."}
        ]),
        make_quiz("Menstrüel siklusun hormonal düzenlenmesinde hipotalamus, hipofiz ve ovaryum hormon eşleşmelerinden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Hipotalamus: GnRH | Hipofiz: FSH ve LH | Ovaryum: Östrojen ve Progesteron", "isCorrect": True, "explanation": "Ders notunda hiyerarşik hormonal kontrol bu şekilde açıkça tanımlanmıştır."},
            {"key": "B", "text": "Hipotalamus: Östrojen | Hipofiz: GnRH | Ovaryum: FSH ve LH", "isCorrect": False, "explanation": "Östrojen overden, GnRH hipotalamustan salgılanır."},
            {"key": "C", "text": "Hipotalamus: Progesteron | Hipofiz: Oksitosin | Ovaryum: GnRH", "isCorrect": False, "explanation": "Hormon kaynakları tamamen yanlıştır."},
            {"key": "D", "text": "Hipotalamus: LH | Hipofiz: Progesteron | Ovaryum: GnRH", "isCorrect": False, "explanation": "LH hipofiz hormonudur."}
        ])
    ]
    slides.append(make_slide(2, "Hormonal Kontrol Ekseni: Hipotalamus, Hipofiz ve Over", "GnRH, gonadotropinler ve over hormonlarının hiyerarşik endokrin kontrolü", "Endokrinoloji", s2_narrative, s2_bullets, s2_elements))

    # Slide 3: Menarş, Menopoz ve Siklus Süre Dinamikleri
    s3_narrative = (
        "Menstrüel siklus kadının yaşam döngüsünde belirli bir biyolojik pencerede aktif kalır.\n\n"
        "- **Başlangıç ve Sonlanma:** Menstruasyon kanamaları ortalama 12 yaşında **menarş** ile başlar "
        "ve fertil dönemin sonunda menopoz ile tamamen sona erer.\n"
        "- **Regülasyon Süreci:** Menstrüel sikluslar menarşı takiben hemen düzenli hale gelmez; tam "
        "olarak regüle olması **5-7 yıl** kadar bir zaman alabilir.\n"
        "- **Normal Aralık:** Menstrüel siklus süresi kadından kadına değişebilmekle birlikte ortalama "
        "28 gündür; tıbbi olarak **21-35 gün arası normal kabul edilir**.\n"
        "- **Fizyolojik Değişkenlik:** Menarştan sonraki adolesan ve menopozdan önceki perimenopozal "
        "dönemlerde anovulatuar sikluslar nedeniyle döngü sürelerinde fizyolojik dalgalanmalar izlenir.\n\n"
        "> [!NOTE]\n"
        "> Menstrüel siklus uzunluğunun 21 günden kısa (polimenore) veya 35 günden uzun (oligomenore) olması patolojik kabul edilir."
    )
    s3_bullets = [
        "Kanamalar ortalama 12 yaşta menarş ile başlar, menopoz ile sona erer.",
        "Siklusların tam regüle olması menarştan sonra 5-7 yıl sürer.",
        "Siklus süresi ortalama 28 gündür; 21-35 gün arası normal kabul edilir."
    ]
    s3_elements = [
        make_cloze("Menstrüel siklus süresi ortalama 28 gündür; 21-35 gün arası normal kabul edilir.", "21-35 gün", "Normal siklus uzunluğu sınırları"),
        make_table("Menstrüel Yaşam Dönemleri ve Siklus Süreleri", ["Parametre", "Sayısal Değer / Süre", "Klinik Özellik"], [
            {"cells": [{"text": "Ortalama Menarş Yaşı", "isMasked": False}, {"text": "Ortalama 12 yaş", "isMasked": True, "hint": "ilk adet görme yaşı"}, {"text": "Üreme çağının başlangıcı"}]},
            {"cells": [{"text": "Siklus Regülasyon Süresi", "isMasked": False}, {"text": "5-7 yıl", "isMasked": False}, {"text": "Aks olgunlaşması gereklidir", "isMasked": True, "hint": "menarş sonrası düzenlenme süresi"}]},
            {"cells": [{"text": "Normal Siklus Aralığı", "isMasked": False}, {"text": "21-35 gün", "isMasked": False}, {"text": "Fizyolojik kabul edilen sınırlar"}]}
        ]),
        make_chain("Üreme Çağı Zaman Çizelgesi", [
            "1. Menarş: Ortalama 12 yaşında ilk menstrüel kanama başlar.",
            "2. Regülasyon: Sonraki 5-7 yıl boyunca anovulatuar döngüler azalır ve aks olgunlaşır.",
            "3. Erişkin Dönem (20-30'lu yaşlar): 21-35 gün aralığında düzenli ovulatuar sikluslar seyreder.",
            "4. Perimenopoz ve Menopoz: Anovulatuar dalgalanmalar artar ve menopozla döngü biter."
        ]),
        make_recall("Fizyolojik olarak normal kabul edilen menstrüel siklus süresi hangi gün aralığıdır?", "21-35 gün arası normal kabul edilir (ortalama 28 gün)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Siklus Süreleri ve Menarş", [
            {"text": "Menstrüel kanamalar menarş ile başlar ve menopozla sona erer.", "isLie": False, "explanation": "Doğru. Kadının reprodüktif penceresidir."},
            {"text": "Menstrüel sikluslar menarşı takiben 5-7 yıl sonra tam olarak regüle olur.", "isLie": False, "explanation": "Doğru. HPA eksen olgunlaşması zaman alır."},
            {"text": "Menstrüel siklus süresi 45 ile 60 gün arasında olduğunda kesinlikle normal kabul edilir.", "isLie": True, "explanation": "Tuzak! Fizyolojik normal aralık 21-35 gündür; 35 günü aşan durumlar oligomenoredir."},
            {"text": "Diyet, yoğun egzersiz ve emosyonel stres siklus sürelerinde geçici değişiklik yapabilir.", "isLie": False, "explanation": "Doğru. Hipotalamik aks strese duyarlıdır."}
        ]),
        make_quiz("Tıbbi olarak normal bir menstrüel siklusun süresi hangi aralıkta kabul edilir?", [
            {"key": "A", "text": "21-35 gün arası", "isCorrect": True, "explanation": "Ders notunda ortalama 28 gün olup 21-35 gün arasının normal kabul edildiği belirtilmiştir."},
            {"key": "B", "text": "10-15 gün arası", "isCorrect": False, "explanation": "Çok kısadır, patolojiktir."},
            {"key": "C", "text": "40-60 gün arası", "isCorrect": False, "explanation": "Oligomenoredir."},
            {"key": "D", "text": "7-10 gün arası", "isCorrect": False, "explanation": "Fizyolojik olamaz."}
        ])
    ]
    slides.append(make_slide(3, "Menarş, Menopoz ve Siklus Süre Dinamikleri", "Menarş yaşı, 5-7 yıllık regülasyon süreci ve 21-35 günlük fizyolojik sınır", "Epidemiyoloji ve Klinik", s3_narrative, s3_bullets, s3_elements))

    # Slide 4: Siklus Başlangıcı ve Menstrüel Faz (İlk 4 Gün)
    s4_narrative = (
        "Menstrüel siklusun zamansal başlangıç noktası, menstrüel kanamanın ilk günü olarak tanımlanır.\n\n"
        "- **Başlangıç Kriteri:** Kanamanın başladığı birinci gün, hem klinik hesaplamalarda hem de "
        "biyolojik olarak yeni bir menstrüel döngünün 1. günüdür.\n"
        "- **Menstrüel Faz:** Menstrüel kanamanın devam ettiği **ilk 4 gün menstrüel fazdır**.\n"
        "- **Hormonal Durum:** Bu evrede korpus luteumun gerilemesi nedeniyle östrojen ve progesteron "
        "düzeyleri bazal seviyelere inmiştir.\n"
        "- **Negatif Feedback Kalkışı:** Dolaşımdaki steroidlerin düşmesi hipofiz üzerindeki baskıyı "
        "kaldırarak yeni bir foliküler kohortun uyarılması için FSH salınımını tetikler.\n\n"
        "> [!NOTE]\n"
        "> Kanamanın ilk günü siklusun 1. günüdür ve ilk 4 gün menstrüel faz olarak adlandırılır."
    )
    s4_bullets = [
        "Siklus menstrüel kanama ile başlar; kanamanın 1. günü siklusun başlangıcıdır.",
        "Menstrüel kanamanın olduğu ilk 4 gün menstrüel fazdır.",
        "Östrojen ve progesteron düzeyleri bu evrede taban değerlerdedir."
    ]
    s4_elements = [
        make_cloze("Siklus menstrüel kanama ile başlar; menstrüel kanamanın olduğu ilk 4 gün menstrüel fazdır.", "ilk 4 gün", "Menstrüel fazın gün aralığı"),
        make_table("Menstrüel Faz Özellikleri", ["Parametre", "Durum", "Fizyolojik Sonuç"], [
            {"cells": [{"text": "Siklus Günü", "isMasked": False}, {"text": "1 ile 4. günler arası", "isMasked": True, "hint": "ilk dört günlük periyot"}, {"text": "Menstrüel faz"}]},
            {"cells": [{"text": "Steroid Hormon Düzeyi", "isMasked": False}, {"text": "Östrojen ve progesteron dip seviyede", "isMasked": False}, {"text": "FSH üzerindeki negatif feedback kalkar", "isMasked": True, "hint": "hipofiz baskılanmasının kalkması"}]}
        ]),
        make_chain("Yeni Döngünün Başlangıç Zinciri", [
            "1. Kanama: Kanamanın ilk günü yeni menstrüel siklusun 1. günü olarak kaydedilir.",
            "2. Menstrüel Faz: İlk 4 gün boyunca fonksiyonel tabaka dökülür.",
            "3. Hormon Düşüşü: Östrojen ve progesteron konsantrasyonları en düşük seviyededir.",
            "4. FSH Salınımı: Hipofiz negatif feedbackten kurtularak folikül uyarısını başlatır."
        ]),
        make_recall("Menstrüel siklusun ilk 4 gününe verilen fizyolojik isim nedir?", "Menstrüel fazdır (kanamanın ilk 4 günü)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Menstrüel Faz", [
            {"text": "Menstrüel kanamanın ilk günü yeni bir menstrüel döngünün birinci günüdür.", "isLie": False, "explanation": "Doğru. Siklus kanama ile başlar."},
            {"text": "Menstrüel kanamanın olduğu ilk 4 gün menstrüel faz olarak kabul edilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Menstrüel fazda progesteron hormonu plazmada en yüksek zirve seviyesindedir.", "isLie": True, "explanation": "Tuzak! Menstrüel fazda progesteron ve östrojen en düşük dip seviyededir; progesteron luteal faz ortasında pik yapar."},
            {"text": "Steroidlerin düşmesi hipofizden yeni folikül gelişimi için uyarı doğurur.", "isLie": False, "explanation": "Doğru. Negatif feedback kalkar."}
        ]),
        make_quiz("Menstrüel siklusta menstrüel faz kaçıncı günleri kapsar ve hormon seviyeleri nasıldır?", [
            {"key": "A", "text": "İlk 4 gündür; östrojen ve progesteron seviyeleri düşüktür", "isCorrect": True, "explanation": "Ders notunda ilk 4 günün menstrüel faz olduğu ve steroidlerin düşük seyrettiği belirtilmiştir."},
            {"key": "B", "text": "14-28. günlerdir; progesteron pik yapmıştır", "isCorrect": False, "explanation": "Bu luteal fazdır."},
            {"key": "C", "text": "11-12. günlerdir; östrojen pik seviyesindedir", "isCorrect": False, "explanation": "Bu preovulatuar dönemdir."},
            {"key": "D", "text": "Yalnızca 28. gündür; HCG salgısı maksimumdur", "isCorrect": False, "explanation": "HCG gebelikte salgılanır."}
        ])
    ]
    slides.append(make_slide(4, "Siklus Başlangıcı ve Menstrüel Faz (İlk 4 Gün)", "Kanamanın 1. günü, ilk 4 günlük menstrüel faz ve bazal hormon düzeyleri", "Fizyoloji", s4_narrative, s4_bullets, s4_elements))

    # Slide 5: FSH'ın Temel İşlevleri ve Foliküler Uyarım
    s5_narrative = (
        "Folikül Stimüle Edici Hormon (FSH), adenohipofizden salgılanarak ovaryumdaki foliküler "
        "gelişimi başlatan ve yöneten primer gonadotropindir.\n\n"
        "- **Folikül Gelişimi ve Oogenez:** FSH, ovaryumda primordial foliküllerin uyarılmasını, "
        "büyümesini, olgunlaşmasını ve oogenezin ilerlemesini sağlar.\n"
        "- **Östrojen Uyarımı:** Büyüyen folikülün granüloza hücrelerini stimüle ederek folikülden "
        "**östrojen salgılanmasını uyarır**.\n"
        "- **GnRH İlişkisi:** Hipotalamik GnRH gonadotropin salınımını tetikler; ancak FSH, LH'a göre "
        "daha çok **bağımsız (otonom) dinamiklerle** salgılanma eğilimi gösterir.\n"
        "- **Siklus Ortası Değişimi:** Siklus ortasında FSH seviyelerinde hafif bir düşme izlense de, "
        "folikül büyümesi ve östrojen üretimi kesintisiz devam eder.\n\n"
        "> [!NOTE]\n"
        "> FSH folikül olgunlaşmasını sağlar ve folikülden östrojen sentezini aktive eder."
    )
    s5_bullets = [
        "Ovaryumda folikül gelişmesini, olgunlaşmasını ve oogenezi sağlar.",
        "Gelişen folikülden östrojen salgılanmasını uyarır.",
        "GnRH etkisiyle salgılansa da LH'a kıyasla daha bağımsız bir salınım dinamiğine sahiptir."
    ]
    s5_elements = [
        make_cloze("FSH ovaryumda folikül gelişimini sağlar ve folikülden östrojen salgılanmasını uyarır.", "östrojen salgılanmasını", "FSH'ın uyardığı over hormonu"),
        make_table("FSH Hormonunun Biyolojik Etkileri", ["Hedef Doku", "FSH Etkisi", "Sonuç"], [
            {"cells": [{"text": "Ovaryum Folikülü", "isMasked": False}, {"text": "Folikül gelişimi ve olgunlaşma", "isMasked": True, "hint": "yumurta olgunlaşması"}, {"text": "Oogenezin ilerlemesi"}]},
            {"cells": [{"text": "Granüloza Hücreleri", "isMasked": False}, {"text": "Aromataz aktivasyonu ve uyarım", "isMasked": False}, {"text": "Östrojen salgılanması", "isMasked": True, "hint": "dişilik hormonu üretimi"}]}
        ]),
        make_chain("FSH Etki Mekanizması", [
            "1. Hipofiz Salınımı: FSH kana salınarak dolaşıma geçer.",
            "2. Reseptör Bağlanması: Overdeki granüloza hücre reseptörlerine bağlanır.",
            "3. Folikül Büyümesi: Folikül kılıfı kalınlaşır ve antrum sıvısı birikir.",
            "4. Östrojen Artışı: Folikülden artan miktarda östrojen sentezlenir."
        ]),
        make_recall("FSH'ın ovaryum üzerindeki iki temel fizyolojik görevi nedir?", "Foliküllerin olgunlaşmasını sağlamak ve folikülden östrojen salgılanmasını uyarmaktır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: FSH Fonksiyonları", [
            {"text": "FSH overde folikül gelişimini ve oogenezi uyarır.", "isLie": False, "explanation": "Doğru. Temel görevidir."},
            {"text": "FSH foliküllerden östrojen sentezini aktive eder.", "isLie": False, "explanation": "Doğru. Granüloza hücrelerini uyarır."},
            {"text": "FSH ovulasyon anında folikülü bizzat yırtarak korpus luteuma dönüştüren tek hormondur.", "isLie": True, "explanation": "Tuzak! Folikülün yırtılmasını ve korpus luteuma dönüşmesini sağlayan hormon LH'tır (Luteinizan Hormon)."},
            {"text": "Siklus ortasında FSH seviyesinde hafif bir düşüş gözlenebilir.", "isLie": False, "explanation": "Doğru. Ders notunda belirtilen fizyolojik dalgalanmadır."}
        ]),
        make_quiz("Folikül gelişimini sağlayan ve folikülden östrojen salgılanmasını uyaran hipofiz ön lob hormonu hangisidir?", [
            {"key": "A", "text": "FSH (Folikül Stimüle Edici Hormon)", "isCorrect": True, "explanation": "Ders notunda folikül gelişimini ve östrojen salgısını uyaran hormonun FSH olduğu açıkça belirtilmiştir."},
            {"key": "B", "text": "Progesteron", "isCorrect": False, "explanation": "Overden salgılanır."},
            {"key": "C", "text": "Prolaktin", "isCorrect": False, "explanation": "Süt üretimi ile ilgilidir."},
            {"key": "D", "text": "HCG", "isCorrect": False, "explanation": "Trofoblastik dokudan salgılanır."}
        ])
    ]
    slides.append(make_slide(5, "FSH'ın Temel İşlevleri ve Foliküler Uyarım", "Folikül büyümesi, oogenez ve östrojen salınımının FSH ile uyarılması", "Endokrinoloji", s5_narrative, s5_bullets, s5_elements))

    # Slide 6: Östrojen Dinamikleri ve 11-12. Gün Piki
    s6_narrative = (
        "Östrojen, menstrüel siklusun ilk yarısına (foliküler faza) damgasını vuran ana steroid hormondur.\n\n"
        "- **Siklus Başı Seviyesi:** Siklus başında östrojen düzeyi oldukça düşüktür; menstrüasyon "
        "ile birlikte taban değerlerde seyreder.\n"
        "- **Paralel Artış:** FSH uyarısıyla seçilen dominant folikülün büyümesine tam paralel olarak "
        "kandaki östrojen seviyesi giderek tırmanır.\n"
        "- **Zirve Zamanı:** Östrojen salgısı hızla artarak **siklusun 11-12. gününde pik yapar**.\n"
        "- **Endometrial Etki:** Bu yükselen östrojen, endometrium hücrelerinde mitoz bölünmeyi hızlandırarak "
        "dokunun kalınlaşmasını ve uterusa bol kan damarı gelmesini sağlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Östrojen konsantrasyonu siklusun 11-12. gününde zirveye (pike) ulaşır ve mitozla endometriumu kalınlaştırır."
    )
    s6_bullets = [
        "Siklus başında östrojen düzeyi düşüktür, folikül büyümesine paralel artar.",
        "Östrojen konsantrasyonu siklusun 11-12. gününde pik yapar.",
        "Mitozu hızlandırarak endometriumu kalınlaştırır ve vaskülarizasyonu artırır."
    ]
    s6_elements = [
        make_cloze("Östrojen düzeyi folikül büyümesine paralel olarak artar ve siklusun 11-12. gününde pik yapar.", "11-12. gününde", "Östrojenin pik yaptığı günler"),
        make_table("Östrojen Hormonunun Siklus Eğrisi", ["Dönem", "Östrojen Düzeyi", "Endometrial Morfoloji"], [
            {"cells": [{"text": "Siklus Başı (1-4. gün)", "isMasked": False}, {"text": "Düşük (bazal seviye)", "isMasked": True, "hint": "taban hormon düzeyi"}, {"text": "Menstrüel dökülme ve ince bazal tabaka"}]},
            {"cells": [{"text": "Preovulatuar (11-12. gün)", "isMasked": False}, {"text": "Pik düzeyi (maksimum)", "isMasked": False}, {"text": "Yoğun mitoz, bez çoğalması, 2-3 mm kalınlık", "isMasked": True, "hint": "proliferatif faz kalınlaşması"}]}
        ]),
        make_chain("Östrojen Salınım ve Etki Kademeleri", [
            "1. Folikül Uyarımı: FSH etkisiyle granüloza hücrelerinde aromataz aktive olur.",
            "2. Kademeli Artış: Folikül büyüdükçe kana verilen östrojen miktarı katlanır.",
            "3. 11-12. Gün Piki: Östrojen konsantrasyonu en yüksek preovulatuar seviyesine ulaşır.",
            "4. Uterin Yanıt: Endometrial bezlerde ve stromada aktif mitoz ile doku kalınlaşır."
        ]),
        make_recall("Östrojen menstrüel siklusun kaçıncı gününde pik seviyesine ulaşır?", "Siklusun 11-12. gününde pik yapar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Östrojen Piki", [
            {"text": "Östrojen siklus başında düşük olup folikül büyümesine paralel artar.", "isLie": False, "explanation": "Doğru. Foliküler faz dinamiğidir."},
            {"text": "Östrojen siklusun 11-12. gününde en yüksek pik seviyesine ulaşır.", "isLie": False, "explanation": "Doğru. Ders notundaki net gündür."},
            {"text": "Östrojen endometriumda mitozu durdurarak dokunun hızla dökülmesini sağlar.", "isLie": True, "explanation": "Tuzak! Östrojen mitozu hızlandırarak endometriumu kalınlaştırır ve damarlanmasını artırır; dokuyu döken değil çoğaltan hormondur."},
            {"text": "Östrojen pikinden sonra hipofiz üzerinde pozitif feedback etkisi oluşur.", "isLie": False, "explanation": "Doğru. LH pikini tetikleyen mekanizmadır."}
        ]),
        make_quiz("Menstrüel siklusta folikülden salgılanan östrojen hormonu kaçıncı günde pik yapar?", [
            {"key": "A", "text": "Siklusun 11-12. gününde", "isCorrect": True, "explanation": "Ders notunda östrojenin folikül büyümesine paralel artarak 11-12. günde pik yaptığı vurgulanmıştır."},
            {"key": "B", "text": "Siklusun 1. gününde", "isCorrect": False, "explanation": "1. günde dip seviyededir."},
            {"key": "C", "text": "Siklusun 28. gününde", "isCorrect": False, "explanation": "Menstruasyondan önce düşer."},
            {"key": "D", "text": "Luteal fazın tam ortasında (21. günde)", "isCorrect": False, "explanation": "21. günde pik yapan progesterondur."}
        ])
    ]
    slides.append(make_slide(6, "Östrojen Dinamikleri ve 11-12. Gün Piki", "Foliküler büyüme, 11-12. gün östrojen piki ve endometrial mitozun uyarılması", "Endokrinoloji", s6_narrative, s6_bullets, s6_elements))

    # Slide 7: LH Piki ve 36 Saat Kuralı
    s7_narrative = (
        "Preovulatuar dönemde östrojenin ulaştığı yüksek tepe düzeyi, hipotalamo-hipofizer eksende "
        "paradoksal bir pozitif feedback mekanizmasını devreye sokar.\n\n"
        "- **Pozitif Feedback:** Östrojen pikinin belirli bir süre yüksek kalması hipofizden masif "
        "bir LH salınım patlamasına yol açar.\n"
        "- **36 Saat Kuralı:** Östrojen pik yaptıktan tam **36 saat sonra LH pikine neden olur**.\n"
        "- **Ovulasyon Tetikleyicisi:** LH pikinin gerçekleşmesi folikül duvarındaki proteolitik "
        "enzimleri aktive ederek folikülün yırtılmasını ve ovulasyonu (14. gün) sağlar.\n"
        "- **Luteinizasyon Başlatıcı:** LH aynı zamanda yırtılan folikülün luteinize olarak korpus "
        "luteum haline gelmesini ve yoğun progesteron salgılamasını yönetir.\n\n"
        "> [!IMPORTANT]\n"
        "> [KRİTİK ZAMANLAMA] Östrojen pikinden 36 saat sonra LH piki oluşur; LH piki ovulasyonun mutlak tetikleyicisidir."
    )
    s7_bullets = [
        "Östrojen pik yaptıktan 36 saat sonra LH pikine neden olur.",
        "LH piki olgun folikülün yırtılmasını (ovulasyonu) gerçekleştirir.",
        "Yırtılan folikülün korpus luteuma dönüşmesini ve progesteron salgısını sağlar."
    ]
    s7_elements = [
        make_cloze("Östrojen pik yaptıktan 36 saat sonra LH pikine neden olur.", "36 saat sonra", "İki tepe noktası arasındaki süre"),
        make_table("Östrojen ve LH Pikleri Zaman İlişkisi", ["Hormon", "Pik Zamanı", "Biyolojik Sonucu"], [
            {"cells": [{"text": "Östrojen", "isMasked": False}, {"text": "Siklusun 11-12. günü", "isMasked": False}, {"text": "Hipofiz üzerinde pozitif feedback uyarımı", "isMasked": True, "hint": "LH salınımını tetikleyen sinyal"}]},
            {"cells": [{"text": "LH (Luteinizan Hormon)", "isMasked": False}, {"text": "Östrojen pikinden 36 saat sonra", "isMasked": True, "hint": "otuz altı saatlik gecikme"}, {"text": "Folikül rüptürü ve ovulasyon (14. gün)"}]}
        ]),
        make_chain("LH Piki ve Ovulasyon Tetikleme Zinciri", [
            "1. Östrojen Zirvesi: 11-12. günde östrojen piki oluşur.",
            "2. Pozitif Feedback: Hipofiz ön lobundan ani ve masif LH salgılanır.",
            "3. 36 Saat Sonrası: LH konsantrasyonu kendi pik tepe noktasına ulaşır.",
            "4. Rüptür ve Dönüşüm: Folikül yırtılarak oosit atılır, folikül korpus luteuma dönüşür."
        ]),
        make_recall("Östrojen pik yaptıktan kaç saat sonra LH pikine neden olur?", "36 saat sonra LH pikine neden olur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: LH Piki ve Zamanlama", [
            {"text": "Östrojen piki oluştuktan 36 saat sonra LH pikine neden olur.", "isLie": False, "explanation": "Doğru. Klasik 36 saat kuralıdır."},
            {"text": "LH piki folikülün yırtılmasını ve ovulasyonu sağlar.", "isLie": False, "explanation": "Doğru. Ovulasyonun ana tetikleyicisidir."},
            {"text": "LH piki östrojen pikinden tam 20 gün önce gerçekleşir.", "isLie": True, "explanation": "Tuzak! LH piki östrojen pikinden 36 saat SONRA meydana gelir."},
            {"text": "Yırtılan folikül LH etkisiyle korpus luteum haline gelir.", "isLie": False, "explanation": "Doğru. Korpus luteum oluşumunu LH sağlar."}
        ]),
        make_quiz("Siklusta östrojen piki oluştuktan kaç saat sonra LH piki meydana gelir?", [
            {"key": "A", "text": "36 saat sonra", "isCorrect": True, "explanation": "Ders notunda açıkça 'östrojen pik yaptıktan 36 saat sonra LH pikine neden olur' denmektedir."},
            {"key": "B", "text": "2 saat sonra", "isCorrect": False, "explanation": "Süre çok yetersizdir."},
            {"key": "C", "text": "7 gün sonra", "isCorrect": False, "explanation": "Bu kadar uzun gecikme olmaz."},
            {"key": "D", "text": "12 saat önce", "isCorrect": False, "explanation": "LH östrojen pikini izler, öncesinde pik yapmaz."}
        ])
    ]
    slides.append(make_slide(7, "LH Piki ve 36 Saat Kuralı", "Pozitif feedback, 36 saat sonra gelişen LH piki ve ovulasyon mekanizması", "Endokrinoloji", s7_narrative, s7_bullets, s7_elements))

    # Slide 8: Progesteron Hormonunun Dinamikleri ve Pik Zamanı
    s8_narrative = (
        "Progesteron, ovulasyon sonrasında dişi vücudunu olası bir gebeliğe hazırlayan temel luteal hormondur.\n\n"
        "- **İlk Yarıda Yokluk:** Progesteron hormonu menstrüel siklusun ilk yarısında (foliküler faz) "
        "kanda pratik olarak **salgılanmaz**.\n"
        "- **Korpus Luteum Kaynağı:** Ovulasyondan (14. gün) sonra meydana gelen korpus luteum progesteron "
        "salgılamaya başlar.\n"
        "- **Zirve Zamanı:** Progesteron plazma konsantrasyonu hızla yükselerek **en yüksek seviyeye luteal "
        "faz ortasında (yaklaşık 21. gün)** ulaşır.\n"
        "- **Uterin Hazırlık:** Endometriumda bezlerin kıvrıntılı uzamasını, subnükleer vakuol oluşumunu "
        "ve embriyonun tutunması için uterusun süngerimsi hale gelmesini sağlar; myometrium kasılmasını baskılar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Progesteron siklusun ilk yarısında salgılanmaz; ovulasyon sonrası korpus luteumdan salgılanarak luteal faz ortasında zirve yapar."
    )
    s8_bullets = [
        "Siklusun ilk yarısında salgılanmaz; ovulasyondan sonra korpus luteumdan salgılanır.",
        "En yüksek seviyesine luteal faz ortasında (yaklaşık 21. günde) ulaşır.",
        "Embriyonun tutunması için uterusu hazırlar ve myometrium kasılmasını önler."
    ]
    s8_elements = [
        make_cloze("Progesteron siklusun ilk yarısında salgılanmaz ve en yüksek seviyeye luteal faz ortasında ulaşır.", "luteal faz ortasında", "Progesteronun pik yaptığı zaman"),
        make_table("Progesteron Hormonu Salınım Profili", ["Siklus Dönemi", "Progesteron Durumu", "Endometrial Cevap"], [
            {"cells": [{"text": "Siklusun İlk Yarısı (1-14. gün)", "isMasked": False}, {"text": "Salgılanmaz (yok denecek kadar az)", "isMasked": True, "hint": "foliküler fazda salgılanmama"}, {"text": "Sadece östrojenik proliferasyon"}]},
            {"cells": [{"text": "Luteal Faz Ortası (~21. gün)", "isMasked": False}, {"text": "En yüksek seviye (Pik)", "isMasked": False}, {"text": "Sekretuar transformasyon, vakuolizasyon, implantasyon hazırlığı", "isMasked": True, "hint": "sekretuar faz olgunlaşması"}]}
        ]),
        make_chain("Progesteron Salınım Aşamaları", [
            "1. Ovulasyon: 14. günde folikül yırtılır.",
            "2. Korpus Luteum: Granüloza ve teka hücreleri luteinize olur.",
            "3. Sekresyon Başlangıcı: Korpus luteumdan bol progesteron salgılanır.",
            "4. Luteal Faz Ortası Piki: Yaklaşık 21. günde zirve yaparak endometriumu sekresyona hazırlar."
        ]),
        make_recall("Progesteron hormonu menstrüel siklusta en yüksek seviyesine ne zaman ulaşır?", "Luteal faz ortasında (yaklaşık 21. günde) ulaşır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Progesteron Dinamiği", [
            {"text": "Progesteron siklusun ilk yarısında salgılanmaz.", "isLie": False, "explanation": "Doğru. Foliküler fazda overden progesteron salgısı yoktur."},
            {"text": "Progesteron en yüksek seviyesine luteal faz ortasında ulaşır.", "isLie": False, "explanation": "Doğru. Korpus luteumun en aktif evresidir."},
            {"text": "Progesteron uterus düz kas kasılmasını şiddetle artırarak erken düşüklere yol açar.", "isLie": True, "explanation": "Tuzak! Progesteron uterus kas kasılmasını önleyerek gebeliğin sürmesini sağlar; azalması düşüğe neden olabilir."},
            {"text": "Korpus luteum çok miktarda progesteron, daha az miktarda östrojen salgılar.", "isLie": False, "explanation": "Doğru. Luteal fazın endokrin profilidir."}
        ]),
        make_quiz("Menstrüel siklusta progesteron hormonunun salınım dinamiği ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Siklusun ilk yarısında salgılanmaz; en yüksek seviyeye luteal faz ortasında ulaşır", "isCorrect": True, "explanation": "Ders notunda açıkça belirtilmiştir: ilk yarıda salgılanmaz, ovulasyon sonrası korpus luteumdan salgılanıp luteal faz ortasında pik yapar."},
            {"key": "B", "text": "Siklusun 1. gününde pik yapar ve ovulasyonda tamamen sıfırlanır", "isCorrect": False, "explanation": "1. günde salgılanmaz."},
            {"key": "C", "text": "Östrojen ile aynı anda 11-12. günde pik yapar", "isCorrect": False, "explanation": "11-12. günde östrojen pik yapar, progesteron yoktur."},
            {"key": "D", "text": "Yalnızca hipofiz ön lobundan salgılanır", "isCorrect": False, "explanation": "Korpus luteumdan salgılanır."}
        ])
    ]
    slides.append(make_slide(8, "Progesteron Hormonunun Dinamikleri ve Pik Zamanı", "İlk yarıda yokluk, korpus luteum salgısı ve luteal faz ortasında pik seviye", "Endokrinoloji", s8_narrative, s8_bullets, s8_elements))

    # Slide 9: HCG ve Gebeliğin 5. Ayına Kadar Progesteron Desteği
    s9_narrative = (
        "Döllenme ve gebelik gerçekleştiğinde, korpus luteumun siklus sonundaki fizyolojik dejenerasyonu "
        "trofoblastik sinyallerle engellenir.\n\n"
        "- **Trofoblastik Hormon:** Gelişen blastokist ve trofoblastik dokudan **HCG** (Human Chorionic "
        "Gonadotropin) salgılanır.\n"
        "- **Korpus Luteumun Korunması:** HCG, LH benzeri etki göstererek korpus luteumun gerilemesini "
        "(luteolizisi) önler ve canlı kalmasını sağlar.\n"
        "- **5. Ay Sınırı:** HCG etkisiyle korpus luteum bozulmadığı için **gebeliğin 5. ayına kadar "
        "progesteron salgılamaya devam eder**.\n"
        "- **Plasental Devir:** Gebeliğin ileri dönemlerinde progesteron sentezini korpus luteumdan "
        "plasenta devralır.\n"
        "- **Gebelik Testleri:** HCG'nin kanda ve idrarda saptanması gebeliğin kesin biyokimyasal kanıtıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Korpus luteum HCG sayesinde gebeliğin 5. ayına kadar progesteron üretir; ileri dönemde görevi plasenta devralır."
    )
    s9_bullets = [
        "HCG korpus luteumun bozulmasını engeller ve östrojen-progesteron salgısını sürdürür.",
        "Korpus luteum HCG sayesinde gebeliğin 5. ayına kadar progesteron salgılar.",
        "Gebeliğin ileri dönemlerinde progesteron üretimi plasenta tarafından devralınır."
    ]
    s9_elements = [
        make_cloze("HCG'nin etkisiyle korpus luteum bozulmadığı için gebeliğin 5. ayına kadar progesteron salgılamaya devam eder.", "gebeliğin 5. ayına kadar", "Korpus luteumun progesteron salgılama süresi"),
        make_table("HCG ve Luteal Destek Evreleri", ["Dönem", "Progesteron Kaynağı", "Hormonal Düzenleyici"], [
            {"cells": [{"text": "Gebelik 0 - 5. Ay", "isMasked": False}, {"text": "Korpus luteum", "isMasked": True, "hint": "gebelik sarı cismi"}, {"text": "Trofoblast kaynaklı HCG"}]},
            {"cells": [{"text": "Gebelik 5. Ay ve Sonrası", "isMasked": False}, {"text": "Plasenta dokusu", "isMasked": False}, {"text": "Fetoplasental otonom sentez", "isMasked": True, "hint": "plasentanın devralması"}]}
        ]),
        make_chain("Gebelik Endokrin Devir Teslim Zinciri", [
            "1. İmplantasyon: Trofoblastlar HCG üretmeye başlar.",
            "2. Luteolizis Engeli: HCG korpus luteumun gerilemesini durdurur.",
            "3. 5. Aya Kadar Salgı: Korpus luteum yüksek progesteron üreterek düşüğü önler.",
            "4. Plasental Dönem: 5. aydan itibaren progesteron sentezini plasenta devralır."
        ]),
        make_recall("Gebelikte korpus luteum HCG desteği ile kaçıncı aya kadar progesteron salgılamaya devam eder?", "Gebeliğin 5. ayına kadar devam eder (sonrasında plasenta devralır)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HCG ve Korpus Luteum", [
            {"text": "HCG korpus luteumun bozulmasını engelleyerek progesteronu yüksek tutar.", "isLie": False, "explanation": "Doğru. Düşüğü önleyen mekanizmadır."},
            {"text": "HCG etkisiyle korpus luteum gebeliğin 5. ayına kadar progesteron salgılar.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Gebelikte progesteron sentezini ilk günden doğuma kadar yalnızca over stroması yapar, plasenta asla progesteron üretemez.", "isLie": True, "explanation": "Tuzak! Gebeliğin 5. ayından sonra progesteron sentezini plasenta devralır."},
            {"text": "HCG'nin kanda varlığı gebelik testlerinde belirteç olarak kullanılır.", "isLie": False, "explanation": "Doğru. Rutin test temelidir."}
        ]),
        make_quiz("Gebelikte korpus luteumun bozulmasını engelleyen ve gebeliğin 5. ayına kadar progesteron salgısını sürdüren hormon hangisidir?", [
            {"key": "A", "text": "HCG (Human Chorionic Gonadotropin)", "isCorrect": True, "explanation": "Ders notunda HCG'nin korpus luteumu koruyarak gebeliğin 5. ayına kadar progesteron salgılattığı açıkça belirtilmiştir."},
            {"key": "B", "text": "Oksitosin", "isCorrect": False, "explanation": "Doğum kasılmalarını uyarır."},
            {"key": "C", "text": "Prolaktin", "isCorrect": False, "explanation": "Laktasyonla ilgilidir."},
            {"key": "D", "text": "GnRH", "isCorrect": False, "explanation": "Hipotalamus hormonudur."}
        ])
    ]
    slides.append(make_slide(9, "HCG ve Gebeliğin 5. Ayına Kadar Progesteron Desteği", "Trofoblastik HCG, korpus luteumun korunması ve 5. aya kadar progesteron salgısı", "Endokrinoloji", s9_narrative, s9_bullets, s9_elements))

    # Slide 10: [TEKRAR SAYFASI - CHECKPOINT 1] Menstrual Siklus ve Hormonal Düzenleme
    s10_narrative = (
        "Bu tekrar sayfasında 1. Bölümde işlenen menstrüel döngü dinamiklerini, eksen hormonlarını, "
        "östrojen ve LH pik sürelerini ve progesteron salınım kurallarını konsolide ediyoruz.\n\n"
        "- **Eksen ve Süre:** Hipotalamus GnRH, hipofiz FSH ve LH, overler östrojen ve progesteron üretir; "
        "normal siklus süresi 21-35 gündür ve ilk 4 gün menstrüel fazdır.\n"
        "- **Östrojen ve LH Pikleri:** Östrojen dominant folikülden salgılanarak 11-12. günde pik yapar; "
        "bu pikten tam 36 saat sonra LH piki oluşarak ovulasyonu tetikler.\n"
        "- **Progesteron ve Gebelik:** Progesteron siklusun ilk yarısında salgılanmaz; luteal faz ortasında "
        "zirveye ulaşır ve gebelikte HCG desteği ile 5. aya kadar korpus luteumdan salgılanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] 21-35 gün normal siklus; 11-12. gün östrojen piki; 36 saat sonra LH piki; luteal faz ortasında progesteron piki; gebelikte 5. aya kadar HCG ile korpus luteum desteği."
    )
    s10_bullets = [
        "Normal siklus süresi 21-35 gün; ilk 4 gün menstrüel fazdır.",
        "Östrojen 11-12. günde pik yapar; 36 saat sonra LH piki gerçekleşir.",
        "Progesteron ilk yarıda yoktur, luteal faz ortasında pik yapar; gebelikte 5. aya kadar korpus luteumdan salgılanır."
    ]
    s10_elements = [
        make_cloze("Östrojen siklusun 11-12. gününde pik yapar ve östrojen pikinden 36 saat sonra LH piki gerçekleşir.", "36 saat sonra", "LH pikinin östrojen pikini izleme süresi"),
        make_table("1. Bölüm Büyük Hormon Tekrar Tablosu", ["Hormon", "Pik / Tepe Zamanı", "Temel Görev / Etki"], [
            {"cells": [{"text": "Östrojen", "isMasked": False}, {"text": "Siklusun 11-12. günü", "isMasked": True, "hint": "on bir ve on ikinci günler"}, {"text": "Endometrium mitozu ve LH pozitif feedbacki"}]},
            {"cells": [{"text": "LH", "isMasked": False}, {"text": "Östrojen pikinden 36 saat sonra", "isMasked": False}, {"text": "Folikül rüptürü (ovulasyon) ve luteinizasyon", "isMasked": True, "hint": "yumurtlama tetikleyicisi"}]},
            {"cells": [{"text": "Progesteron", "isMasked": False}, {"text": "Luteal faz ortası (~21. gün)", "isMasked": True, "hint": "luteal periyot ortası"}, {"text": "Sekretuar hazırlık, kas kasılmasını önleme"}]},
            {"cells": [{"text": "HCG", "isMasked": False}, {"text": "Gebelikte salgılanır", "isMasked": False}, {"text": "Korpus luteumu 5. aya kadar koruma", "isMasked": True, "hint": "beşinci aya kadar destek"}]}
        ]),
        make_chain("Hormonal Sıralama Özeti", [
            "1. Menstrüel Faz (1-4. gün): Östrojen ve progesteron dip seviyededir.",
            "2. Foliküler Proliferasyon: FSH folikülü büyütür, östrojen tırmanır.",
            "3. Östrojen Piki (11-12. gün): Zirveye ulaşarak LH'a pozitif feedback gönderir.",
            "4. LH Piki (36 saat sonra): Masif pik yaparak ovulasyonu sağlar.",
            "5. Progesteron Piki (Luteal Faz Ortası): Korpus luteumdan sekresyonu zirveye taşır."
        ]),
        make_recall("1. Bölümün temel hormon pik süreleri: Östrojen hangi gün, LH östrojen pikinden ne kadar sonra, progesteron hangi fazda pik yapar?", "Östrojen 11-12. günde, LH östrojen pikinden 36 saat sonra, progesteron ise luteal faz ortasında pik yapar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 1. Bölüm Konsolidasyonu", [
            {"text": "Menstrüel siklus süresi 21-35 gün arası normal kabul edilir.", "isLie": False, "explanation": "Doğru. Fizyolojik sınırlardır."},
            {"text": "Östrojen 11-12. günde pik yapar, 36 saat sonra LH pikine neden olur.", "isLie": False, "explanation": "Doğru. İki hormonun kritik zaman ilişkisidir."},
            {"text": "Progesteron siklusun 1. gününde en yüksek düzeydedir ve folikül büyümesini sağlar.", "isLie": True, "explanation": "Tuzak! Progesteron siklusun ilk yarısında salgılanmaz; luteal faz ortasında korpus luteumdan salgılanarak pik yapar."},
            {"text": "Gebelikte HCG etkisiyle korpus luteum 5. aya kadar progesteron salgılamaya devam eder.", "isLie": False, "explanation": "Doğru. 5. aydan sonra plasenta devralır."}
        ]),
        make_quiz("Menstrüel siklusun hormonal düzenlenmesi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Progesteron hormonu siklusun ilk 4 gününde pik yaparak menstrüasyonu durdurur", "isCorrect": True, "explanation": "Yanlış! Progesteron siklusun ilk yarısında salgılanmaz, menstrüel fazda dip seviyededir ve luteal faz ortasında pik yapar."},
            {"key": "B", "text": "Menstrüel kanamanın olduğu ilk 4 gün menstrüel fazdır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Östrojen pik yaptıktan 36 saat sonra LH pikine neden olur", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "HCG sayesinde korpus luteum gebeliğin 5. ayına kadar progesteron salgılamaya devam eder", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(10, "[TEKRAR SAYFASI - CHECKPOINT 1] Menstrual Siklus ve Hormonal Düzenleme", "1. Bölümün konsolidasyonu: GnRH, gonadotropinler, 11-12. gün östrojen piki, 36 saat kuralı ve luteal faz", "Bölüm Tekrarı", s10_narrative, s10_bullets, s10_elements))

    return slides
