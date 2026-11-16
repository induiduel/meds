# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec5():
    slides = []

    # Slide 41: Normal Menstruasyon Kriterleri ve AUK Tanımı
    s41_narrative = (
        "Kadın üreme sağlığının değerlendirilmesinde normal menstrüel kanamanın kesin tıbbi kriterlerini bilmek esastır.\n\n"
        "- **Normal Menstruasyon:** Ovulatuar bir siklusla beraber, sekretuar dönemden sonra olan "
        "ve **beş günü aşmayan kanama** olarak tanımlanır.\n"
        "- **Anormal Uterin Kanama (AUK):** Bu fizyolojik kriterlerin (süre, miktar, periyot) dışındaki "
        "herhangi bir vajinal/uterin kanama **anormal uterin kanama** olarak adlandırılır.\n"
        "- **Organik Lezyonlar:** AUK vakalarında en sık saptanan organik lezyonlar; submuköz leiomyom, "
        "endometrit, endometrial polip, endometriozis ve endometrial karsinomdur.\n"
        "- **Klinik Yaklaşım:** Anormal kanama ile başvuran bir hastada ilk amaç hayatı tehdit eden "
        "karsinom veya gebelik komplikasyonlarını hızla dışlamaktır.\n\n"
        "> [!IMPORTANT]\n"
        "> [TANIM] Normal menstruasyon: ovulatuar siklusla beraber, sekretuar dönemden sonra olan ve 5 günü aşmayan kanamadır; bunun dışındakiler AUK'tur."
    )
    s41_bullets = [
        "Normal menstruasyon: ovulatuar siklusla, sekretuar dönemden sonra olan ve 5 günü aşmayan kanamadır.",
        "Bu kriterlerin dışındaki kanamalar anormal uterin kanama (AUK) olarak adlandırılır.",
        "AUK leiomyom, endometrit, polip, endometriozis veya karsinom sonucu görülebilir."
    ]
    s41_elements = [
        make_cloze("Normal menstruasyon, ovulatuar siklusla beraber, sekretuar dönemden sonra olan beş günü aşmayan kanama olarak tanımlanır.", "beş günü aşmayan", "Normal adet kanaması üst süre sınırı"),
        make_table("Normal Menstruasyon vs AUK Kriterleri", ["Özellik", "Normal Menstruasyon", "Anormal Uterin Kanama (AUK)"], [
            {"cells": [{"text": "Siklus Karakteri", "isMasked": False}, {"text": "Ovulatuar, düzenli (21-35 gün)", "isMasked": False}, {"text": "Düzensiz, anovulatuar veya organik lezyonlu", "isMasked": True, "hint": "anormal siklus yapısı"}]},
            {"cells": [{"text": "Kanama Süresi", "isMasked": False}, {"text": "5 günü aşmayan kanama", "isMasked": True, "hint": "en çok beş gün"}, {"text": ">5 gün veya lekelenme tarzı"}]},
            {"cells": [{"text": "Öncül Faz", "isMasked": False}, {"text": "Sekretuar dönem sonrası", "isMasked": False}, {"text": "Yetersiz fazlar veya kontrolsüz dökülme"}]}
        ]),
        make_chain("Kanama Sınıflama Algoritması", [
            "1. Anamnez: Kanama günü, miktarı ve sıklığı sorgulanır.",
            "2. Normal Kriter Testi: Kanama 5 günü aşıyor mu, siklus ovulatuar mı incelenir.",
            "3. AUK Tanısı: 5 günü aşan veya sekretuar faz dışı kanamaya AUK denir.",
            "4. Etiyoloji Ayrımı: Organik lezyon mu yoksa disfonksiyonel mi olduğu araştırılır."
        ]),
        make_recall("Tıbbi olarak 'normal menstruasyon' tanımının içerdiği üç temel kriter nedir?", "1) Ovulatuar siklusla beraber olması, 2) Sekretuar dönemden sonra gerçekleşmesi, 3) Beş günü aşmayan kanama olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Normal Menstruasyon ve AUK", [
            {"text": "Normal menstruasyon beş günü aşmayan kanama olarak tanımlanır.", "isLie": False, "explanation": "Doğru. Klasik tanımdır."},
            {"text": "Normal kanama ovulatuar siklusla beraber ve sekretuar dönemden sonra olur.", "isLie": False, "explanation": "Doğru. Fizyolojik kriterdir."},
            {"text": "Aralıksız 30 gün süren kanama her kadında kesinlikle normal menstruasyon kabul edilir.", "isLie": True, "explanation": "Tuzak! Normal menstruasyon beş günü aşmayan kanamadır; 30 gün süren kanama açıkça anormal uterin kanamadır."},
            {"text": "Endometrial polip ve karsinom anormal uterin kanama yapabilen organik nedenlerdir.", "isLie": False, "explanation": "Doğru. Organik etiyolojidir."}
        ]),
        make_quiz("Tıbbi olarak normal menstruasyonun tanımı aşağıdakilerden hangisinde eksiksiz verilmiştir?", [
            {"key": "A", "text": "Ovulatuar siklusla beraber, sekretuar dönemden sonra olan beş günü aşmayan kanama", "isCorrect": True, "explanation": "Ders notunda harfiyen bu üç kriterli resmi tanım yer almaktadır."},
            {"key": "B", "text": "Anovulatuar dönemde rastgele başlayan ve en az 1 ay süren kanama", "isCorrect": False, "explanation": "Bu AUK'tur."},
            {"key": "C", "text": "Yalnızca menopozdan sonra yılda bir görülen kanama", "isCorrect": False, "explanation": "Postmenopozal kanamadır, patolojiktir."},
            {"key": "D", "text": "Her gün aralıksız az miktarda lekelenme olması", "isCorrect": False, "explanation": "Metrorajidir."}
        ])
    ]
    slides.append(make_slide(41, "Normal Menstruasyon Kriterleri ve AUK Tanımı", "Ovulatuar siklus, sekretuar zemin, 5 gün kuralı ve AUK genel kavramı", "Jinekoloji ve Patoloji", s41_narrative, s41_bullets, s41_elements))

    # Slide 42: Organik vs Disfonksiyonel Uterin Kanama (DUK)
    s42_narrative = (
        "Anormal uterin kanamalar altta yatan nedene göre organik ve disfonksiyonel olmak üzere iki ana kategoriye ayrılır.\n\n"
        "- **Organik Nedenler:** Anatomik, histolojik veya sistemik belirgin bir patolojiye bağlı "
        "kanamalardır; submuköz miyom, endometrial polip, endometrit, hiperplazi ve karsinom gibi lezyonları içerir.\n"
        "- **Disfonksiyonel Uterin Kanama (DUK):** Uterusta hiçbir **organik bir nedene bağlanamayan "
        "kanamalara disfonksiyonel uterin kanama** adı verilir.\n"
        "- **DUK Sınıflaması:** DUK olguları mekanizma olarak **ovulasyonla birlikte olan ve "
        "ovulasyonsuz (anovulatuar) olan kanamalar** olmak üzere ikiye ayrılır.\n"
        "- **Dışlama Tanısı:** DUK tanısı ancak tüm organik tümöral, enfeksiyöz ve gebelik nedenleri "
        "kesin olarak dışlandıktan sonra konulabilir.\n\n"
        "> [!NOTE]\n"
        "> Organik bir nedene bağlanamayan kanamalara disfonksiyonel uterin kanama denir; ovulasyonlu ve ovulasyonsuz olarak ikiye ayrılır."
    )
    s42_bullets = [
        "Organik nedene bağlanamayan anormal kanamalara disfonksiyonel uterin kanama (DUK) denir.",
        "DUK iki kategoriye ayrılır: ovulasyonla birlikte olan ve ovulasyonsuz (anovulatuar) kanamalar.",
        "Organik nedenler leiomyom, polip, endometrit, hiperplazi ve karsinomu kapsar."
    ]
    s42_elements = [
        make_cloze("Organik bir nedene bağlanamayan kanamalara disfonksiyonel uterin kanama denir.", "disfonksiyonel uterin kanama", "Organik nedeni olmayan kanama tipi"),
        make_table("Organik vs Disfonksiyonel Kanama Ayrımı", ["Özellik", "Organik Kanama", "Disfonksiyonel Kanama (DUK)"], [
            {"cells": [{"text": "Altta Yatan Lezyon", "isMasked": False}, {"text": "Polip, miyom, karsinom, endometrit", "isMasked": True, "hint": "somut anatomik lezyon"}, {"text": "Organik lezyon saptanamaz"}]},
            {"cells": [{"text": "Temel Mekanizma", "isMasked": False}, {"text": "Yapısal doku yıkımı / vasküler patoloji", "isMasked": False}, {"text": "Hormonal eksen ve feedback aksaklığı", "isMasked": True, "hint": "endokrin dengesizlik"}]},
            {"cells": [{"text": "Alt Tipleri", "isMasked": False}, {"text": "Tümöral, enfektif, gebelik", "isMasked": False}, {"text": "Ovulasyonlu vs Anovulatuar"}]}
        ]),
        make_chain("DUK Tanısal Ayrım Zinciri", [
            "1. Kanama Şikayeti: Hasta anormal kanamayla başvurur.",
            "2. Biyopsi ve Görüntüleme: Miyom, polip, hiperplazi ve kanser taranır.",
            "3. Organik Yokluk: Tüm anatomik lezyonlar ekarte edilir.",
            "4. DUK Sınıflaması: Kanama ovulasyonlu mu yoksa anovulatuar mı belirlenir."
        ]),
        make_recall("Organik bir nedene bağlanamayan anormal uterin kanamalara ne ad verilir ve iki alt tipi nedir?", "Disfonksiyonel uterin kanama (DUK) denir; ovulasyonla birlikte olan ve ovulasyonsuz (anovulatuar) kanamalar olarak ikiye ayrılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: DUK Tanımı", [
            {"text": "Organik bir nedene bağlanamayan kanamalara disfonksiyonel uterin kanama denir.", "isLie": False, "explanation": "Doğru. DUK tanımıdır."},
            {"text": "DUK ovulasyonlu ve ovulasyonsuz olarak ikiye ayrılır.", "isLie": False, "explanation": "Doğru. İki alt kategorisidir."},
            {"text": "Uterusunda dev bir karsinom kitlesi saptanan hastanın kanaması kesinlikle disfonksiyonel uterin kanamadır.", "isLie": True, "explanation": "Tuzak! Karsinom saptandığında bu organik bir kanamadır; DUK organik neden bulunamadığında konur."},
            {"text": "Submuköz leiomyom organik bir kanama nedenidir.", "isLie": False, "explanation": "Doğru. Yapısal bir tümördür."}
        ]),
        make_quiz("Organik bir patolojiye bağlanamayan anormal kanamalara ne ad verilir ve hangi kategorilere ayrılır?", [
            {"key": "A", "text": "Disfonksiyonel uterin kanama; ovulasyonla birlikte olan ve ovulasyonsuz olarak ikiye ayrılır", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'organik bir nedene bağlanamayan kanamalara disfonksiyonel uterin kanama denir; ovulasyonla birlikte olan ve ovulasyonsuz olmak üzere iki kategoriye ayrılır' denmektedir."},
            {"key": "B", "text": "Organik polipozis; iyi huylu ve kötü huylu olarak ikiye ayrılır", "isCorrect": False, "explanation": "Polip organik bir nedendir."},
            {"key": "C", "text": "Sekonder hematom; sadece erkeklerde görülür", "isCorrect": False, "explanation": "Uterin kanamadır."},
            {"key": "D", "text": "Hemofilik menstrüasyon; sadece pıhtılaşma faktör yokluğunda olur", "isCorrect": False, "explanation": "DUK tanımı değildir."}
        ])
    ]
    slides.append(make_slide(42, "Organik vs Disfonksiyonel Uterin Kanama (DUK)", "Organik lezyonlar, DUK tanımı, ovulasyonlu ve ovulasyonsuz disfonksiyonel kanamalar", "Klinik ve Patoloji", s42_narrative, s42_bullets, s42_elements))

    # Slide 43: DUK Mekanizmaları: Ovulatuar vs Anovulatuar Kanama
    s43_narrative = (
        "Disfonksiyonel uterin kanamalarda kanamanın mekanizması ovulasyonun var olup olmamasına göre tamamen farklı patofizyolojik temellere dayanır.\n\n"
        "- **Ovulatuar Grupta Mekanizma:** Ovulasyonun korunduğu disfonksiyonel kanamalarda temel sorun "
        "faz yetersizlikleridir; **yetersiz proliferatif faz veya yetersiz sekretuar faz (luteal faz yetmezliği)** "
        "nedeni ile kanama meydana gelmektedir.\n"
        "- **Luteal Yetersizlik:** Progesteron desteğinin erken kesilmesi veya yetersiz kalması endometriumun "
        "zamansız dökülmesine yol açar.\n"
        "- **Anovulatuar Grupta Mekanizma:** Anovulatuar sikluslarla beraber olan kanamanın nedeni ise "
        "**uzun süreli düzensiz östrojen stimülasyonu** sonucu oluşan dokusal kırılmalardır.\n"
        "- **Karşılanmamış Kırılma Kanaması:** Ovulasyon olmayınca korpus luteum oluşmaz; sürekli östrojenle "
        "aşırı kalınlaşan ve damarları yetersiz kalan doku parçalı ve düzensiz dökülür.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ovulatuar DUK: yetersiz proliferatif veya yetersiz sekretuar faza bağlıdır; Anovulatuar DUK: uzun süreli düzensiz östrojen stimülasyonuna bağlıdır."
    )
    s43_bullets = [
        "Ovulatuar grupta kanama: yetersiz proliferatif faz veya yetersiz sekretuar faz nedeniyledir.",
        "Anovulatuar grupta kanama nedeni: uzun süreli düzensiz östrojen stimülasyonudur.",
        "Anovulasyonda progesteron yokluğuna bağlı östrojen çekilme/kırılma kanaması gelişir."
    ]
    s43_elements = [
        make_cloze("Anovulatuar sikluslarla beraber olan kanamanın nedeni uzun süreli düzensiz östrojen stimülasyonu sonucu ile oluşan değişikliklerdir.", "uzun süreli düzensiz östrojen stimülasyonu", "Anovulatuar kanamanın temel nedeni"),
        make_table("Ovulatuar vs Anovulatuar DUK Mekanizmaları", ["DUK Kategorisi", "Temel Patofizyolojik Neden", "Hormonal Arka Plan"], [
            {"cells": [{"text": "Ovulatuar DUK", "isMasked": False}, {"text": "Yetersiz proliferatif veya yetersiz sekretuar faz", "isMasked": True, "hint": "faz yetersizlikleri"}, {"text": "Luteal faz yetmezliği, progesteron dengesizliği"}]},
            {"cells": [{"text": "Anovulatuar DUK", "isMasked": False}, {"text": "Uzun süreli düzensiz östrojen stimülasyonu", "isMasked": False}, {"text": "Progesteron yokluğu, östrojenik kırılma", "isMasked": True, "hint": "karşılanmamış östrojen"}]}
        ]),
        make_chain("Anovulatuar DUK Oluşum Zinciri", [
            "1. Anovulasyon: Folikül olgunlaşır fakat LH piki oluşmaz ve çatlamaz.",
            "2. Progesteronsuzluk: Korpus luteum gelişmediği için progesteron sıfırdır.",
            "3. Sürekli Östrojen Uyarısı: Uzun süreli düzensiz östrojen endometriumu büyütür.",
            "4. Düzensiz Dökülme: Vasküler destek yetersiz kalınca lekelenme ve ağır kanamalar başlar."
        ]),
        make_recall("Ovulatuar DUK ile anovulatuar DUK'un temel patofizyolojik nedenleri nelerdir?", "Ovulatuar grupta: yetersiz proliferatif veya yetersiz sekretuar faz; Anovulatuar grupta: uzun süreli düzensiz östrojen stimülasyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: DUK Mekanizmaları", [
            {"text": "Ovulatuar grupta kanama yetersiz proliferatif veya sekretuar faz nedeniyle olabilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Anovulatuar kanamanın nedeni uzun süreli düzensiz östrojen stimülasyonudur.", "isLie": False, "explanation": "Doğru. Temel mekanizmadır."},
            {"text": "Anovulatuar sikluslarda kanamanın tek nedeni kanda progesteronun 100 kat artmasıdır.", "isLie": True, "explanation": "Tuzak! Anovulatuar sikluslarda korpus luteum oluşmadığı için progesteron salgılanamaz; neden uzun süreli düzensiz östrojen stimülasyonudur."},
            {"text": "Disfonksiyonel kanamalarda etiyoloji kadınların yaşına da bağlıdır.", "isLie": False, "explanation": "Doğru. Yaş kritik faktördür."}
        ]),
        make_quiz("Disfonksiyonel uterin kanamalarda ovulatuar ve anovulatuar kanama nedenleri hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Ovulatuar: yetersiz proliferatif/sekretuar faz | Anovulatuar: uzun süreli düzensiz östrojen stimülasyonu", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'ovulatuar grupta kanama yetersiz proliferatif veya sekretuar faz nedeni ile olabilmektedir; anovulatuar sikluslarla beraber olan kanamanın nedeni ise uzun süreli düzensiz östrojen stimülasyonudur' denmektedir."},
            {"key": "B", "text": "Ovulatuar: tiroidit | Anovulatuar: aşırı kalsiyum birikimi", "isCorrect": False, "explanation": "Tıbbi olarak yanlıştır."},
            {"key": "C", "text": "Her ikisinde de tek neden overlerin cerrahi olarak alınmış olmasıdır", "isCorrect": False, "explanation": "Overler mevcuttur."},
            {"key": "D", "text": "Ovulatuar: sürekli progesteron fazlalığı | Anovulatuar: GnRH tümörü", "isCorrect": False, "explanation": "Mekanizmalar ters ve hatalıdır."}
        ])
    ]
    slides.append(make_slide(43, "DUK Mekanizmaları: Ovulatuar vs Anovulatuar Kanama", "Yetersiz fazlar, luteal yetmezlik, uzun süreli östrojen stimülasyonu ve dokusal dökülme", "Fizyopatoloji", s43_narrative, s43_bullets, s43_elements))

    # Slide 44: Menoraji ve Metroraji Tanımları
    s44_narrative = (
        "Menstrüasyon işlevlerindeki bozuklukların doğru terminoloji ile tanımlanması klinik patolojide büyük önem taşır.\n\n"
        "- **Menoraji Tanımı:** Düzenli aralıklarla olmakla beraber adet kanamasının **aşırı miktarda "
        "olup uzun sürmesi** tablosudur (hipermenore ile birlikte anılır).\n"
        "- **Klinik Nedenleri:** Menoraji sıklıkla intramural/submuköz leiomyomlar, adenomyozis veya "
        "koagülopatiler zemininde gelişir.\n"
        "- **Metroraji Tanımı:** Normal düzende görülen adet kanaması tamamen bitmiş olmasına rağmen, "
        "**adet kanamasının bitişinden birkaç gün sonra yeniden hafif lekelenme tarzında kanama olması** durumudur.\n"
        "- **Ayırıcı Tanı:** Metroraji organik bir endometrial polip, servikal lezyon, karsinom veya "
        "ani hormonal kırılmaların habercisi olabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Menoraji: düzenli fakat aşırı ve uzun kanamadır; Metroraji: adet bittikten birkaç gün sonra yeniden hafif lekelenme tarzı kanama olmasıdır."
    )
    s44_bullets = [
        "Menoraji: düzenli olmakla beraber adet kanamasının aşırı miktarda olup uzun sürmesidir.",
        "Metroraji: adet bittikten birkaç gün sonra yeniden hafif lekelenme tarzı kanama olmasıdır.",
        "Menoraji sıklıkla miyom/adenomyozisle, metroraji polip/karsinomla ilişkili olabilir."
    ]
    s44_elements = [
        make_cloze("Normal düzende görülen adet bittikten birkaç gün sonra yeniden hafif lekelenme tarzında kanama olmasına metroraji denir.", "metroraji", "Adet bitimi sonrası lekelenme kanaması"),
        make_table("Menoraji vs Metroraji Karşılaştırması", ["Terim", "Kanama Karakteri ve Zamanlaması", "Sıklıkla Eşlik Eden Durum"], [
            {"cells": [{"text": "Menoraji", "isMasked": False}, {"text": "Düzenli fakat aşırı miktarda ve uzun süren kanama", "isMasked": True, "hint": "yoğun ve uzun süreli adet"}, {"text": "Leiomyom, adenomyozis, pıhtılaşma bozukluğu"}]},
            {"cells": [{"text": "Metroraji", "isMasked": False}, {"text": "Adet bitiminden birkaç gün sonra hafif lekelenme", "isMasked": False}, {"text": "Endometrial polip, karsinom, servikal lezyon", "isMasked": True, "hint": "ara kanama / organik lezyon"}]}
        ]),
        make_chain("Kanama Bozukluğu Ayırımı", [
            "1. Zamanlama Tespiti: Kanama periyodik adetle mi çakışıyor, ara dönemde mi?",
            "2. Miktar Değerlendirmesi: Adet aşırı miktarda ve uzun mu sürüyor (Menoraji)?",
            "3. Bitiş Sonrası Lekelenme: Adet bittikten sonra ara lekelenme mi var (Metroraji)?",
            "4. Hedefli Biyopsi: Metrorajide polip ve karsinom ekarte edilir."
        ]),
        make_recall("Menoraji ile metroraji arasındaki temel tanısal fark nedir?", "Menoraji: düzenli fakat aşırı miktarda ve uzun süren kanamadır; Metroraji: adet kanaması bittikten birkaç gün sonra yeniden hafif lekelenme tarzında kanama olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Menoraji ve Metroraji", [
            {"text": "Menoraji adet kanamasının aşırı miktarda olup uzun sürmesidir.", "isLie": False, "explanation": "Doğru. Menoraji tanımıdır."},
            {"text": "Metroraji adet bittikten birkaç gün sonra yeniden hafif lekelenme tarzı kanamadır.", "isLie": False, "explanation": "Doğru. Metroraji tanımıdır."},
            {"text": "Menoraji sadece menopozdaki kadınlarda yılda bir damla lekelenme olması durumudur.", "isLie": True, "explanation": "Tuzak! Bu postmenopozal kanamadır; menoraji düzenli siklusta aşırı ve uzun kanamadır."},
            {"text": "Metroraji varlığında organik lezyonlar akla getirilmelidir.", "isLie": False, "explanation": "Doğru. Klinik prensiptir."}
        ]),
        make_quiz("Adet kanamasının bitişinden birkaç gün sonra yeniden hafif lekelenme tarzında kanama olması tablosuna ne ad verilir?", [
            {"key": "A", "text": "Metroraji", "isCorrect": True, "explanation": "Ders notu tablosunda kelimesi kelimesine: 'metroraji: normal düzende görülen adet kanaması bitmiş olmasına rağmen, adet kanamasının bitişinden birkaç gün sonra yeniden hafif lekelenme tarzında kanama olması' denmektedir."},
            {"key": "B", "text": "Menoraji", "isCorrect": False, "explanation": "Menoraji aşırı ve uzun kanamadır."},
            {"key": "C", "text": "Oligomenore", "isCorrect": False, "explanation": "Seyrek adet görmedir."},
            {"key": "D", "text": "Hipomenore", "isCorrect": False, "explanation": "Miktarı az olan kanamadır."}
        ])
    ]
    slides.append(make_slide(44, "Menoraji ve Metroraji Tanımları", "Aşırı/uzun süren düzenli kanama (menoraji) ve adet sonu lekelenme tarzı kanama (metroraji)", "Klinik Terminoloji", s44_narrative, s44_bullets, s44_elements))

    # Slide 45: Oligomenore, Polimenore ve Hipomenore
    s45_narrative = (
        "Menstrüel döngü periyodunun ve akış miktarının anormallikleri özgül tıbbi terimlerle sınıflandırılır.\n\n"
        "- **Oligomenore:** Menstrüel siklus aralığının **genellikle 35 günü geçen seyrek adet görme "
        "durumu** olarak tanımlanır.\n"
        "- **PCOS İlişkisi:** Oligomenore en sık polikistik over sendromu (PCOS) ve kronik anovulasyon zemininde izlenir.\n"
        "- **Polimenore:** Adet kanamalarının **21 gün veya daha sık aralıklarla ortaya çıkması** durumudur.\n"
        "- **Hipomenore:** Adet sikluslarının düzenli aralıklarla devam etmesine karşın, kanama miktarının "
        "**belirgin biçimde az olması** tablosudur.\n"
        "- **Diğer Tipler:** Siklus ortasında görülen intermenstrüel kanamalara **ovulatuar kanama**, "
        "menopozdan sonra görülen her türlü kanamaya ise **postmenapozal kanama** denir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Oligomenore: >35 günü geçen seyrek adet; Polimenore: 21 gün veya daha sık adet; Hipomenore: düzenli fakat miktarı az olan kanamadır."
    )
    s45_bullets = [
        "Oligomenore: genellikle 35 günü geçen seyrek adet görme durumudur.",
        "Polimenore: 21 gün veya daha sık adet görme durumudur.",
        "Hipomenore: düzenli ancak miktarı az olan kanamadır; ovulatuar kanama ise intermenstrüeldir."
    ]
    s45_elements = [
        make_cloze("Genellikle 35 günü geçen seyrek adet görme durumuna oligomenore denir.", "oligomenore", "Otuz beş günü geçen seyrek adet terimi"),
        make_table("Menstrüasyon Frekans ve Miktar Bozuklukları", ["Terim", "Kriter / Aralık", "Fizyopatolojik Anlam"], [
            {"cells": [{"text": "Oligomenore", "isMasked": False}, {"text": ">35 günü geçen seyrek adet", "isMasked": True, "hint": "otuz beş günden uzun aralık"}, {"text": "Seyrek ovulasyon, PCOS, anovulasyon"}]},
            {"cells": [{"text": "Polimenore", "isMasked": False}, {"text": "21 gün veya daha sık adet", "isMasked": False}, {"text": "Kısalmış siklus, luteal yetmezlik", "isMasked": True, "hint": "yirmi bir günden sık döngü"}]},
            {"cells": [{"text": "Hipomenore", "isMasked": False}, {"text": "Düzenli fakat miktarı az kanama", "isMasked": False}, {"text": "Endometrial hipoplazi veya yapışıklık"}]}
        ]),
        make_chain("Siklus Periyodu Tanı Akışı", [
            "1. Döngü Gün Sayımı: İki adet başlangıcı arasındaki süre hesaplanır.",
            "2. 35 Gün Üstü: Süre >35 gün ise Oligomenore tanısı konur.",
            "3. 21 Gün Altı: Süre ≤21 gün ise Polimenore tanısı konur.",
            "4. Miktar Azlığı: Aralık normalken akım çok az ise Hipomenore belirlenir."
        ]),
        make_recall("Oligomenore ve polimenore terimlerinin gün sınırları nelerdir?", "Oligomenore: genellikle 35 günü geçen seyrek adet; Polimenore: 21 gün veya daha sık adet görme durumudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Siklus Periyot Bozuklukları", [
            {"text": "Oligomenore genellikle 35 günü geçen seyrek adet görme durumudur.", "isLie": False, "explanation": "Doğru. Tanımdır."},
            {"text": "Polimenore 21 gün veya daha sık adet görme durumudur.", "isLie": False, "explanation": "Doğru. Tanımdır."},
            {"text": "Hipomenore her gün en az 5 litre kan kaybedilen aşırı kanamadır.", "isLie": True, "explanation": "Tuzak! Hipomenore düzenli ancak miktarı AZ olan kanamadır; aşırı kanama menorajidir."},
            {"text": "Ovulatuar kanama intermenstrüel kanama olarak da adlandırılır.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Genellikle 35 günü geçen seyrek adet görme durumuna verilen tıbbi isim hangisidir?", [
            {"key": "A", "text": "Oligomenore", "isCorrect": True, "explanation": "Ders notu tablosunda: 'oligomenore: genellikle 35 günü geçen seyrek adet görme durumu' olarak tanımlanmıştır."},
            {"key": "B", "text": "Polimenore", "isCorrect": False, "explanation": "Polimenore 21 gün veya daha sık görmedir."},
            {"key": "C", "text": "Hipomenore", "isCorrect": False, "explanation": "Hipomenore miktarın az olmasıdır."},
            {"key": "D", "text": "Menoraji", "isCorrect": False, "explanation": "Menoraji aşırı miktarda uzun kanamadır."}
        ])
    ]
    slides.append(make_slide(45, "Oligomenore, Polimenore ve Hipomenore", ">35 gün (oligomenore), <21 gün (polimenore), az miktar (hipomenore) ve intermenstrüel kanamalar", "Klinik Terminoloji", s45_narrative, s45_bullets, s45_elements))

    # Slide 46: Yaşa Göre AUK Nedenleri: Prepuberte ve Adolesan Dönem
    s46_narrative = (
        "Anormal uterin kanamaların olası etiyolojisi kadınların bulunduğu yaş dönemine sıkı sıkıya bağımlıdır.\n\n"
        "- **Prepuberte Dönemi:** Puberte öncesi bir kız çocuğunda vajinal/uterin kanama kesinlikle "
        "patolojiktir; **en önemli neden puberte prekoks** (erken ergenlik) tablosudur.\n"
        "- **Prepuberte Ayırıcı Tanı:** Puberte prekoks dışında yabancı cisim, travma veya genital "
        "sarkomlar (botryoid rabdomyosarkom) akla getirilmelidir.\n"
        "- **Adolesan Dönem:** Menarştan sonraki ergenlik çağında anormal kanamanın **en sık ve "
        "kardinal nedeni anovulatuar siklus**tur.\n"
        "- **Eksenel Olgunlaşma:** Hipotalamo-hipofizer-ovaryal eksenin menarşı takiben 5-7 yıl boyunca "
        "tam olgunlaşamaması, ovulasyonun aksamasına ve karşılanmamış östrojenle düzensiz dökülmelere yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Prepubertede AUK nedeni: puberte prekoks; Adolesan dönemde AUK nedeni: anovulatuar siklustur."
    )
    s46_bullets = [
        "Prepuberte döneminde anormal uterin kanama nedeni: puberte prekoks.",
        "Adolesan dönemde anormal uterin kanama nedeni: anovulatuar siklus.",
        "Adolesanda hipotalamik eksenin olgunlaşmamışlığı anovulatuar kanamaları tetikler."
    ]
    s46_elements = [
        make_cloze("Prepuberte döneminde AUK nedeni puberte prekoks iken adolesan dönemde anovulatuar siklustur.", "anovulatuar siklus", "Adolesan dönemde AUK'un temel nedeni"),
        make_table("Genç Yaş Gruplarında AUK Nedenleri", ["Yaşam Dönemi", "En Önemli Neden", "Fizyopatolojik Zemin"], [
            {"cells": [{"text": "Prepuberte (Çocukluk)", "isMasked": False}, {"text": "Puberte prekoks", "isMasked": True, "hint": "erken ergenlik tablosu"}, {"text": "Erken hormonal aks aktivasyonu"}]},
            {"cells": [{"text": "Adolesan (Ergenlik)", "isMasked": False}, {"text": "Anovulatuar siklus", "isMasked": False}, {"text": "HPA ekseninin henüz regüle olmaması (5-7 yıl)", "isMasked": True, "hint": "aks olgunlaşma yetersizliği"}]}
        ]),
        make_chain("Ergenlik Çağı Kanama Mekanizması", [
            "1. Menarş Başlangıcı: Ortalama 12 yaşında ilk adet görülür.",
            "2. Olgunlaşmamış Aks: GnRH pulsatilitesi henüz düzenli LH piki oluşturamaz.",
            "3. Anovulasyon: Folikül çatlasa bile korpus luteum oluşamaz.",
            "4. Adolesan AUK: Karşılanmamış östrojenle düzensiz, bazen aşırı kanama izlenir."
        ]),
        make_recall("Prepuberte ve adolesan dönemlerde anormal uterin kanamanın en sık nedenleri nelerdir?", "Prepuberte döneminde puberte prekoks; Adolesan döneminde ise anovulatuar siklustur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Prepuberte ve Adolesan AUK", [
            {"text": "Prepuberte döneminde AUK nedeni puberte prekokstur.", "isLie": False, "explanation": "Doğru. Ders notu tablosu verisidir."},
            {"text": "Adolesan dönemde anormal kanama nedeni anovulatuar siklustur.", "isLie": False, "explanation": "Doğru. En sık nedendir."},
            {"text": "Adolesan dönemde anormal kanamanın tek nedeni kesinlikle metastatik akciğer karsinomudur.", "isLie": True, "explanation": "Tuzak! Adolesanda primer neden anovulatuar siklustur; karsinom bu yaşta son derece nadirdir."},
            {"text": "Adolesan dönemde siklusların tam regüle olması 5-7 yıl sürebilir.", "isLie": False, "explanation": "Doğru. Bilinen fizyolojidir."}
        ]),
        make_quiz("Adolesan dönemdeki genç bir kızda anormal uterin kanamanın en sık görülen nedeni aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Anovulatuar siklus", "isCorrect": True, "explanation": "Ders notu tablosunda: 'Adolesan dönemi AUK nedeni: anovulatuar siklus' olarak net şekilde belirtilmiştir."},
            {"key": "B", "text": "Puberte prekoks", "isCorrect": False, "explanation": "Prepuberte nedenidir."},
            {"key": "C", "text": "Endometrial atrofi", "isCorrect": False, "explanation": "Postmenopoz nedenidir."},
            {"key": "D", "text": "Senil vajinit", "isCorrect": False, "explanation": "İleri yaş nedenidir."}
        ])
    ]
    slides.append(make_slide(46, "Yaşa Göre AUK Nedenleri: Prepuberte ve Adolesan Dönem", "Prepubertede puberte prekoks, adolesanda aks olgunlaşmamışlığı ve anovulatuar sikluslar", "Klinik Patoloji", s46_narrative, s46_bullets, s46_elements))

    # Slide 47: Reprodüktif Yaşlarda AUK Nedenleri
    s47_narrative = (
        "Doğurganlık çağındaki (reprodüktif) kadınlarda anormal uterin kanama yelpazesi son derece geniş ve çeşitlidir.\n\n"
        "- **Gebelik Komplikasyonları:** Reprodüktif çağda AUK ile başvuran her hastada ilk olarak "
        "**gebelik komplikasyonları (düşük / abortus, trofoblastik hastalık, ektopik gebelik)** dışlanmalıdır.\n"
        "- **Organik Nedenler:** Uterusun yapısal lezyonları; **leiomyom, adenomyozis, endometrial polip, "
        "endometrial hiperplazi ve karsinom**dur.\n"
        "- **Anovulatuar Siklus:** Polikistik over sendromu veya strese bağlı anovulatuar kanamalar bu yaş grubunda da görülebilir.\n"
        "- **Ovaryal Disfonksiyon:** Korpus luteumun yetersiz hormon salgıladığı **luteal faz yetmezliği** "
        "(ovaryal disfonksiyonel kanama) ara kanamalara yol açabilir.\n\n"
        "> [!NOTE]\n"
        "> Reprodüktif yaşta AUK: gebelik komplikasyonları (düşük, ektopik, trofoblastik), organik nedenler (miyom, adenomyozis, polip, karsinom), anovulasyon ve luteal yetmezliktir."
    )
    s47_bullets = [
        "Gebelik komplikasyonları: düşük (abortus), trofoblastik hastalık, ektopik gebelik.",
        "Organik nedenler: leiomyom, adenomyozis, polip, endometrial hiperplazi, karsinom.",
        "Anovulatuar siklus ve ovaryal disfonksiyonel kanama (luteal faz yetmezliği) sık görülür."
    ]
    s47_elements = [
        make_cloze("Reprodüktif yaşta AUK nedenleri arasında gebelik komplikasyonları, organik lezyonlar ve anovulatuar siklus yer alır.", "gebelik komplikasyonları", "Üreme çağında ilk dışlanması gereken durum"),
        make_table("Reprodüktif Çağ AUK Etyoloji Yelpazesi", ["Kategori", "Özgül Klinik Durumlar", "Tanı Yöntemi"], [
            {"cells": [{"text": "Gebelik Komplikasyonları", "isMasked": False}, {"text": "Düşük, ektopik gebelik, trofoblastik hastalık", "isMasked": True, "hint": "gebelik kaynaklı aciller"}, {"text": "Serum beta-HCG ve ultrason"}]},
            {"cells": [{"text": "Organik Lezyonlar", "isMasked": False}, {"text": "Leiomyom, adenomyozis, polip, hiperplazi, karsinom", "isMasked": False}, {"text": "Biyopsi, histeroskopi, patoloji", "isMasked": True, "hint": "dokusal tanı"}]},
            {"cells": [{"text": "Endokrin / Fonksiyonel", "isMasked": False}, {"text": "Anovulatuar siklus, luteal faz yetmezliği", "isMasked": False}, {"text": "Hormon profili ve siklus takibi"}]}
        ]),
        make_chain("Reprodüktif AUK Ayırıcı Tanı Zinciri", [
            "1. HCG Testi: Gebelik komplikasyonu (düşük, ektopik) ekarte edilir.",
            "2. Anatomik Görüntüleme: Ultrasonla leiomyom, polip ve adenomyozis taranır.",
            "3. Endometrial Biyopsi: Hiperplazi ve karsinom histolojik olarak dışlanır.",
            "4. Fonksiyonel İnceleme: Anovulasyon ve luteal faz yetmezliği yönetilir."
        ]),
        make_recall("Reprodüktif yaşlardaki bir kadında AUK etiyolojisinde yer alan başlıca gruplar nelerdir?", "1) Gebelik komplikasyonları (düşük, trofoblastik hastalık, ektopik gebelik), 2) Organik nedenler (leiomyom, adenomyozis, polip, hiperplazi, karsinom), 3) Anovulatuar siklus ve luteal faz yetmezliğidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Reprodüktif Çağ AUK", [
            {"text": "Gebelik komplikasyonları reprodüktif çağda AUK nedenleri arasındadır.", "isLie": False, "explanation": "Doğru. Düşük ve ektopik gebelik sıktır."},
            {"text": "Leiomyom, adenomyozis ve endometrial polip organik nedenlerdir.", "isLie": False, "explanation": "Doğru. Yapısal lezyonlardır."},
            {"text": "Reprodüktif çağdaki kadınlarda gebelik testi yapılması tıbben yasaktır ve asla gebelik düşünülmez.", "isLie": True, "explanation": "Tuzak! Reprodüktif yaşta kanama ile gelen her kadında gebelik komplikasyonları ilk akla gelmesi gereken durumdur."},
            {"text": "Ovaryal disfonksiyonel kanama (luteal faz yetmezliği) görülebilir.", "isLie": False, "explanation": "Doğru. Endokrin nedendir."}
        ]),
        make_quiz("Reprodüktif yaşlardaki kadınlarda anormal uterin kanama (AUK) etiyolojisinde aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Gebelik komplikasyonları, leiomyom, polip, adenomyozis ve anovulatuar siklus", "isCorrect": True, "explanation": "Ders notu tablosunda reprodüktif yaş nedenleri tam olarak bu bileşenleri içermektedir."},
            {"key": "B", "text": "Yalnızca prostat hiperplazisi", "isCorrect": False, "explanation": "Erkek hastalığıdır."},
            {"key": "C", "text": "Sadece puberte prekoks", "isCorrect": False, "explanation": "Prepuberte nedenidir."},
            {"key": "D", "text": "Hiçbir neden bulunamaz, tamamen hayalidir", "isCorrect": False, "explanation": "Organik ve fonksiyonel nedenler vardır."}
        ])
    ]
    slides.append(make_slide(47, "Reprodüktif Yaşlarda AUK Nedenleri", "Gebelik komplikasyonları (düşük, ektopik), miyom, adenomyozis, polip ve luteal yetmezlik", "Klinik Patoloji", s47_narrative, s47_bullets, s47_elements))

    # Slide 48: Perimenopozal Dönemde AUK ve Düzensiz Dökülme
    s48_narrative = (
        "Menopoz geçişi (perimenopoz), over rezervinin tükendiği ve hormonal dalgalanmaların zirve yaptığı kırılgan bir dönemdir.\n\n"
        "- **Hormonal Dalgalanma:** Perimenopozal dönemde foliküler kohort azaldığı için ovulasyon "
        "sıklığı düşer ve sikluslar çoğunlukla **anovulatuar** seyreder.\n"
        "- **Düzensiz Dökülme:** Ovulasyon olmaksızın uzayan östrojenik uyarım, fonksiyonel tabakanın "
        "eşzamanlı değil, parçalı ve **düzensiz dökülmesine (irregular shedding)** yol açar.\n"
        "- **Organik Lezyon Artışı:** Yaşın ilerlemesiyle birlikte **organik lezyonlar (endometrial "
        "karsinom, hiperplazi, endometrial polip)** belirgin biçimde sıklaşır.\n"
        "- **Klinik Yaklaşım:** Perimenopozal bir kadında kanama düzensizliği basit bir anovulasyon "
        "olarak geçiştirilmemeli, mutlaka biyopsi ile hiperplazi ve karsinom ekarte edilmelidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Perimenopozda AUK nedenleri: anovulatuar siklus, düzensiz dökülme ve organik lezyonlardır (karsinom, hiperplazi, polip)."
    )
    s48_bullets = [
        "Perimenopozda AUK: anovulatuar siklus ve düzensiz dökülme sıktır.",
        "Organik lezyonlar sıklaşır: endometrial karsinom, hiperplazi, polip.",
        "Hormonal dalgalanma zemininde malignite riski mutlaka dışlanmalıdır."
    ]
    s48_elements = [
        make_cloze("Perimenopoz döneminde AUK nedenleri anovulatuar siklus, düzensiz dökülme ve organik lezyonlardır.", "düzensiz dökülme", "Perimenopozda izlenen karakteristik dökülme paterni"),
        make_table("Perimenopozal AUK Patolojileri", ["Neden Grubu", "Özgül Durum", "Klinik Önemi"], [
            {"cells": [{"text": "Fonksiyonel Bozukluk", "isMasked": False}, {"text": "Anovulatuar siklus ve düzensiz dökülme", "isMasked": True, "hint": "düzensiz adet kanamaları"}, {"text": "Geçiş dönemi hormonal kaosu"}]},
            {"cells": [{"text": "Premalign Lezyon", "isMasked": False}, {"text": "Endometrial hiperplazi", "isMasked": False}, {"text": "Karsinoma ilerleme riski", "isMasked": True, "hint": "kanser öncülü yapı"}]},
            {"cells": [{"text": "Malign ve Benign Organik", "isMasked": False}, {"text": "Karsinom ve endometrial polip", "isMasked": False}, {"text": "Biyopsi ile kesin tanı zorunluluğu"}]}
        ]),
        make_chain("Perimenopozal Kanama Patogenezi", [
            "1. Folikül Azalması: Over rezervi kritik seviyeye iner.",
            "2. Anovulatuar Döngüler: Korpus luteum oluşamaz, progesteron üretilemez.",
            "3. Düzensiz Dökülme: Endometrium kontrolsüz kanar ve ara kanamalar başlar.",
            "4. Neoplastik Zemin: Karşılanmamış östrojen hiperplazi ve karsinom riskini tetikler."
        ]),
        make_recall("Perimenopozal dönemde anormal uterin kanamaya yol açan temel nedenler nelerdir?", "Anovulatuar siklus, düzensiz dökülme ve organik lezyonlardır (karsinom, hiperplazi, polip)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Perimenopozal AUK", [
            {"text": "Perimenopozda anovulatuar siklus ve düzensiz dökülme AUK nedenidir.", "isLie": False, "explanation": "Doğru. Geçiş dönemi karakteristiğidir."},
            {"text": "Karsinom, hiperplazi ve polip perimenopozda organik kanama nedenleridir.", "isLie": False, "explanation": "Doğru. Ders notu tablosu verisidir."},
            {"text": "Perimenopozal dönemdeki tüm kanamalar sadece puberte prekoks nedeniyledir.", "isLie": True, "explanation": "Tuzak! Puberte prekoks çocukluk çağındadır; perimenopozda anovulasyon, hiperplazi ve karsinom ön plandadır."},
            {"text": "Perimenopozal kanamalarda biyopsi ile malignite dışlanmalıdır.", "isLie": False, "explanation": "Doğru. Hayati prensiptir."}
        ]),
        make_quiz("Perimenopozal dönemdeki bir kadında anormal uterin kanama (AUK) nedenleri arasında hangisi yer alır?", [
            {"key": "A", "text": "Anovulatuar siklus, düzensiz dökülme, karsinom, hiperplazi ve polip", "isCorrect": True, "explanation": "Ders notu tablosunda perimenopoz nedenleri eksiksiz bu şekildedir."},
            {"key": "B", "text": "Yalnızca akut apandisit perforasyonu", "isCorrect": False, "explanation": "Batın içi cerrahi tablodur."},
            {"key": "C", "text": "Puberte prekoks ve botryoid rabdomyosarkom", "isCorrect": False, "explanation": "Çocukluk çağı lezyonlarıdır."},
            {"key": "D", "text": "Kemik iliğinde megakaryosit patlaması", "isCorrect": False, "explanation": "Hematolojik ilgisiz tablodur."}
        ])
    ]
    slides.append(make_slide(48, "Perimenopozal Dönemde AUK ve Düzensiz Dökülme", "Perimenopozal anovulasyon, düzensiz dökülme, polip, hiperplazi ve karsinom riskleri", "Klinik Patoloji", s48_narrative, s48_bullets, s48_elements))

    # Slide 49: Postmenapozal Kanamalar ve Endometrial Atrofi
    s49_narrative = (
        "Postmenopozal dönemde görülen herhangi bir uterin kanama, aksi kanıtlanana kadar malignite şüphesi taşır.\n\n"
        "- **Klinik Alarm:** Menopoz tamamlandıktan sonra kanama olması fizyolojik değildir; **postmenapozal "
        "kanama mutlaka araştırılmalıdır**.\n"
        "- **Organik Nedenler:** Bu dönemde AUK'un başlıca organik nedenleri **karsinom, hiperplazi "
        "ve endometrial polip**tir.\n"
        "- **En Sık Benign Neden:** Karsinom en çok korkulan tanı olmakla birlikte, postmenopozal "
        "kanamaların pratikte en sık rastlanan benign nedeni **endometrial atrofi**dir.\n"
        "- **Atrofi Mekanizması:** Östrojenin tamamen çekilmesiyle incelen ve kırılganlaşan atrofik "
        "endometrium yüzeyindeki yüzeyel kılcal damarlar kolayca çatlayarak lekelenme tarzı kanama yapar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Postmenopozda AUK nedenleri: organik lezyonlar (karsinom, hiperplazi, polip) ve endometrial atrofidir."
    )
    s49_bullets = [
        "Postmenapozal dönemde kanama malignite şüphesi taşır ve araştırılmalıdır.",
        "Organik nedenler: endometrial karsinom, hiperplazi ve polip.",
        "Benign en sık neden: östrojen yokluğuna bağlı gelişen endometrial atrofidir."
    ]
    s49_elements = [
        make_cloze("Postmenapoz döneminde AUK nedenleri organik lezyonlar (karsinom, hiperplazi, polip) ve endometrial atrofidir.", "endometrial atrofi", "Postmenopozda sık görülen benign kanama nedeni"),
        make_table("Postmenopozal Kanama Etyolojisi", ["Patolojik Durum", "Biyolojik Doğası", "Klinik Önemi"], [
            {"cells": [{"text": "Endometrium Karsinomu", "isMasked": False}, {"text": "Malign neoplazi", "isMasked": True, "hint": "kötü huylu tümör"}, {"text": "Mutlak ekarte edilmelidir"}]},
            {"cells": [{"text": "Endometrial Atrofi", "isMasked": False}, {"text": "İncelmiş, kırılgan atrofik mukoza", "isMasked": False}, {"text": "En sık benign kanama nedeni", "isMasked": True, "hint": "iyi huylu en sık sebep"}]},
            {"cells": [{"text": "Hiperplazi ve Polip", "isMasked": False}, {"text": "Preneoplastik veya benign lezyonlar", "isMasked": False}, {"text": "Tedavi ve takip gerektirir"}]}
        ]),
        make_chain("Postmenopozal Kanama Yönetimi", [
            "1. Başvuru: Postmenopozal hasta vajinal kanama ile gelir.",
            "2. Acil Yaklaşım: Karsinom riski nedeniyle derhal endometrial örnekleme yapılır.",
            "3. Biyopsi Sonucu: Olguların bir kısmında karsinom veya hiperplazi saptanır.",
            "4. Atrofi Tanısı: Belirgin bir tümör yoksa kırılgan endometrial atrofi doğrulanır."
        ]),
        make_recall("Postmenapozal dönemde anormal uterin kanamaya yol açan temel etiyolojik nedenler nelerdir?", "Organik lezyonlar (karsinom, hiperplazi, polip) ve endometrial atrofidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Postmenopozal Kanamalar", [
            {"text": "Postmenopozda organik lezyonlar (karsinom, hiperplazi, polip) kanama nedenidir.", "isLie": False, "explanation": "Doğru. Ders notu verisidir."},
            {"text": "Endometrial atrofi postmenopozal kanama nedenleri arasında yer alır.", "isLie": False, "explanation": "Doğru. En sık benign nedendir."},
            {"text": "Postmenopozal kanama tamamen normaldir, asla doktora gitmeye ve biyopsi almaya gerek yoktur.", "isLie": True, "explanation": "Tuzak! Postmenopozal kanama aksi kanıtlanana kadar karsinom şüphesi taşır ve mutlak biyopsi gerektirir."},
            {"text": "Östrojen çekilmesiyle atrofik damarlar kolayca çatlayabilir.", "isLie": False, "explanation": "Doğru. Atrofi kanama mekanizmasıdır."}
        ]),
        make_quiz("Postmenapozal dönemde anormal uterin kanama (AUK) ile başvuran bir kadında etiyolojide aşağıdakilerden hangileri aranmalıdır?", [
            {"key": "A", "text": "Organik lezyonlar (karsinom, hiperplazi, polip) ve endometrial atrofi", "isCorrect": True, "explanation": "Ders notu tablosunda postmenopoz nedenleri tam olarak: 'organik lezyonlar (karsinom, hiperplazi, polip), endometrial atrofi' olarak verilmiştir."},
            {"key": "B", "text": "Yalnızca puberte prekoks", "isCorrect": False, "explanation": "Çocukluk dönemi nedenidir."},
            {"key": "C", "text": "Sadece ektopik gebelik", "isCorrect": False, "explanation": "Postmenopozda gebelik görülmez."},
            {"key": "D", "text": "Menarş başlangıcı", "isCorrect": False, "explanation": "Menarş ilk adettir, menopoz sonrasıyla ilgisi yoktur."}
        ])
    ]
    slides.append(make_slide(49, "Postmenapozal Kanamalar ve Endometrial Atrofi", "Postmenopozal kanama alarmı, karsinom riski, polipler ve benign endometrial atrofi", "Klinik Patoloji", s49_narrative, s49_bullets, s49_elements))

    # Slide 50: [TEKRAR SAYFASI - CHECKPOINT 5] Anormal Uterin Kanamalar ve Menstrüasyon Bozuklukları
    s50_narrative = (
        "Bu tekrar sayfasında 5. Bölüm boyunca ele aldığımız normal menstruasyon kriterlerini, "
        "DUK mekanizmalarını, terminolojik tanımları ve yaşa göre AUK nedenlerini konsolide ediyoruz.\n\n"
        "- **Normal vs AUK:** Normal menstruasyon: ovulatuar siklusla, sekretuar dönemden sonra olan "
        "ve 5 günü aşmayan kanamadır; bunun dışındakiler AUK'tur.\n"
        "- **DUK:** Organik neden olmaksızın olan kanamalardır; ovulatuar (yetersiz fazlar) ve anovulatuar "
        "(uzun süreli düzensiz östrojen) olarak ikiye ayrılır.\n"
        "- **Terminoloji:** Menoraji (düzenli fakat aşırı ve uzun), Metroraji (adet bitiminden sonra "
        "lekelenme), Oligomenore (>35 gün), Polimenore (≤21 gün), Hipomenore (az miktar).\n"
        "- **Yaşa Göre Dağılım:** Prepubertede puberte prekoks; Adolesanda anovulatuar siklus; Reprodüktifte "
        "gebelik komplikasyonları ve organik lezyonlar; Perimenopozda düzensiz dökülme ve hiperplazi/karsinom; "
        "Postmenopozda karsinom, hiperplazi, polip ve endometrial atrofi.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] 5 günü aşmayan kanama normaldir; Menoraji vs Metroraji; Oligo (>35 gün) vs Poli (<21 gün); Prepuberte: prekoks, Adolesan: anovulasyon, Postmenopoz: karsinom ve atrofi."
    )
    s50_bullets = [
        "Normal menstruasyon: 5 günü aşmayan ovulatuar sekretuar kanamadır.",
        "Menoraji: aşırı/uzun; Metroraji: adet sonu lekelenme; Oligomenore: >35 gün; Polimenore: <21 gün.",
        "Prepuberte: puberte prekoks; Adolesan: anovulasyon; Postmenopoz: karsinom, hiperplazi, polip, atrofi."
    ]
    s50_elements = [
        make_cloze("Oligomenore genellikle 35 günü geçen seyrek adet iken polimenore 21 gün veya daha sık adet görme durumudur.", "polimenore", "Yirmi bir günden sık adet görme terimi"),
        make_table("5. Bölüm Büyük Yaş ve Terminoloji Tablosu", ["Yaşam Dönemi / Terim", "Tanısal Kriter / Neden", "Klinik Özellik"], [
            {"cells": [{"text": "Prepuberte", "isMasked": False}, {"text": "Puberte prekoks", "isMasked": True, "hint": "erken ergenlik"}, {"text": "Çocukluk çağı kanaması"}]},
            {"cells": [{"text": "Adolesan", "isMasked": False}, {"text": "Anovulatuar siklus", "isMasked": False}, {"text": "Aks olgunlaşma süreci", "isMasked": True, "hint": "ergenlik yumurtlama aksaklığı"}]},
            {"cells": [{"text": "Postmenapoz", "isMasked": False}, {"text": "Karsinom, hiperplazi, polip, atrofi", "isMasked": True, "hint": "karsinom ve atrofi"}, {"text": "Malignite dışlanması zorunlu"}]},
            {"cells": [{"text": "Menoraji vs Metroraji", "isMasked": False}, {"text": "Menoraji: aşırı/uzun | Metroraji: ara lekelenme", "isMasked": False}, {"text": "Miktar ve zamanlama ayrımı"}]}
        ]),
        make_chain("Bölüm 5 Süreç Konsolidasyonu", [
            "1. Kriter Kontrolü: Kanama 5 günü aşıyor mu (AUK)?",
            "2. Terim Eşleme: Kanama aşırı mı (Menoraji), lekelenme mi (Metroraji), seyrek mi (Oligomenore)?",
            "3. Yaş Odaklı Yaklaşım: Hasta adolesan mı (anovulasyon), postmenopozal mi (karsinom/atrofi)?",
            "4. DUK Ayrımı: Organik lezyon yoksa ovulatuar vs anovulatuar DUK belirlenir."
        ]),
        make_recall("5. Bölümün altın bilgileri: Oligomenore gün eşiği nedir, adolesan AUK nedeni nedir ve postmenopozal kanama nedenleri nelerdir?", "Oligomenore >35 gün; adolesan nedeni anovulatuar siklus; postmenopozal nedenler ise karsinom, hiperplazi, polip ve endometrial atrofidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 5. Bölüm Konsolidasyonu", [
            {"text": "Normal menstruasyon 5 günü aşmayan kanama olarak tanımlanır.", "isLie": False, "explanation": "Doğru. Tanım kriteridir."},
            {"text": "Oligomenore genellikle 35 günü geçen seyrek adettir.", "isLie": False, "explanation": "Doğru. Gün eşiğidir."},
            {"text": "Adolesan dönemdeki kanamaların tek nedeni kesinlikle endometrial karsinomdur ve anovulasyon asla görülmez.", "isLie": True, "explanation": "Tuzak! Adolesanda primer neden anovulatuar siklustur; karsinom ise ileri yaş (postmenopoz) hastalığıdır."},
            {"text": "Postmenopozal dönemde karsinom, hiperplazi, polip ve endometrial atrofi kanama nedenleridir.", "isLie": False, "explanation": "Doğru. Tablo verisidir."}
        ]),
        make_quiz("Anormal uterin kanamalar ve menstrüasyon bozuklukları ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Polimenore 35 günden uzun süren adet aralığıdır ve adolesanda sadece karsinom görülür", "isCorrect": True, "explanation": "Yanlış! Polimenore 21 gün veya daha sık görmedir (>35 gün oligomenoredir); adolesanda ise primer neden anovulatuar siklustur."},
            {"key": "B", "text": "Normal menstruasyon ovulatuar siklusla sekretuar dönemden sonra olan ve 5 günü aşmayan kanamadır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Metroraji adet bitiminden birkaç gün sonra hafif lekelenme tarzı kanamadır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Postmenapozal dönemde AUK nedenleri karsinom, hiperplazi, polip ve endometrial atrofidir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(50, "[TEKRAR SAYFASI - CHECKPOINT 5] Anormal Uterin Kanamalar ve Menstrüasyon Bozuklukları", "5. Bölümün konsolidasyonu: 5 gün kuralı, menoraji/metroraji, oligo/polimenore ve yaşa göre prepuberte/adolesan/postmenopoz AUK nedenleri", "Bölüm Tekrarı", s50_narrative, s50_bullets, s50_elements))

    return slides
