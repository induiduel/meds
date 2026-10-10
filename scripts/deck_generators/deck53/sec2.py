# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec2():
    slides = []

    # Slide 11: Menstrüel Döngünün Dört Temel Evresi
    s11_narrative = (
        "Menstrüel döngü, ovaryum ve uterus dokularında senkronize yürütülen dört ana evreden oluşur.\n\n"
        "- **Evrelerin Sıralanışı:** Bu dört evre sırasıyla **folikül evresi, ovulasyon evresi, "
        "korpus luteum evresi ve menstruasyon evresi**dir.\n"
        "- **Süre Dağılımları:** Folikül evresi 10-14 gün, ovulasyon 14. günde, korpus luteum evresi "
        "10-14 gün ve menstruasyon evresi 3-5 gün sürer.\n"
        "- **Dinamik Dengelenme:** Bu evrelerin sürelerindeki kontrollü ardışıklık, menstrüel siklusun "
        "toplam 21-35 günlük fizyolojik sınırda kalmasını temin eder.\n"
        "- **Organ Koordinasyonu:** Her evrede overdeki hücresel değişimler ile uterus endometriumundaki "
        "yapısal transformasyon birbiriyle tam bir nedensellik bağı içerisindedir.\n\n"
        "> [!NOTE]\n"
        "> Menstrüel siklus dört birbirini izleyen evreden oluşur: folikül (10-14 gün), ovulasyon (14. gün), korpus luteum (10-14 gün) ve menstruasyon (3-5 gün)."
    )
    s11_bullets = [
        "Menstrüel döngü 4 evreden oluşur: folikül, ovulasyon, korpus luteum ve menstruasyon.",
        "Folikül evresi 10-14 gün, ovulasyon 14. günde, korpus luteum 10-14 gün sürer.",
        "Menstruasyon evresi 3-5 gün sürer ve toplam siklus 21-35 gün aralığındadır."
    ]
    s11_elements = [
        make_cloze("Menstrüel döngü sırasıyla folikül, ovulasyon, korpus luteum ve menstruasyon evresi olmak üzere dört evreden oluşur.", "korpus luteum", "Ovulasyondan sonraki luteal evre"),
        make_table("Menstrüel Döngünün Dört Evresi", ["Evre Adı", "Fizyolojik Süre", "Ana Olay"], [
            {"cells": [{"text": "1. Folikül Evresi", "isMasked": False}, {"text": "10-14 gün", "isMasked": True, "hint": "on ila on dört günlük evre"}, {"text": "FSH ile folikül gelişimi ve östrojen sentezi"}]},
            {"cells": [{"text": "2. Ovulasyon Evresi", "isMasked": False}, {"text": "14. gün", "isMasked": False}, {"text": "LH etkisiyle folikül yırtılması ve oosit salınımı", "isMasked": True, "hint": "yumurtlama günü"}]},
            {"cells": [{"text": "3. Korpus Luteum Evresi", "isMasked": False}, {"text": "10-14 gün", "isMasked": False}, {"text": "Progesteron ve östrojen salgısı"}]},
            {"cells": [{"text": "4. Menstruasyon Evresi", "isMasked": False}, {"text": "3-5 gün", "isMasked": True, "hint": "üç ila beş günlük kanama"}, {"text": "Fonksiyonel tabakanın dökülmesi"}]}
        ]),
        make_chain("Evrelerin Kronolojik Akışı", [
            "1. Menstruasyon: 3-5 gün süren kanamayla eski fonksiyonel tabaka atılır.",
            "2. Folikül Evresi: 10-14 gün boyunca yeni folikül gelişir ve östrojen artar.",
            "3. Ovulasyon: 14. günde LH etkisiyle oosit serbestleşir.",
            "4. Korpus Luteum Evresi: 10-14 gün boyunca progesteron endometriumu olgunlaştırır."
        ]),
        make_recall("Menstrüel döngünün dört evresini ve fizyolojik sürelerini sırasıyla belirtiniz.", "1. Folikül evresi (10-14 gün), 2. Ovulasyon evresi (14. gün), 3. Korpus luteum evresi (10-14 gün), 4. Menstruasyon evresi (3-5 gün)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Siklus Evreleri", [
            {"text": "Folikül evresi ortalama 10-14 gün sürer.", "isLie": False, "explanation": "Doğru. Foliküler faz süresidir."},
            {"text": "Ovulasyon evresi siklusun 14. gününde gerçekleşir.", "isLie": False, "explanation": "Doğru. Tipik ovulasyon zamanıdır."},
            {"text": "Korpus luteum evresi 10-14 gün devam eder.", "isLie": False, "explanation": "Doğru. Luteal faz süresidir."},
            {"text": "Menstruasyon evresi normal şartlarda aralıksız 25-30 gün sürer.", "isLie": True, "explanation": "Tuzak! Menstruasyon evresi 3-5 gün sürer; 25-30 gün süren kanama ağır bir patolojidir."}
        ]),
        make_quiz("Menstrüel döngünün evreleri ve süreleri ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Folikül: 10-14 gün | Ovulasyon: 14. gün | Korpus Luteum: 10-14 gün | Menstruasyon: 3-5 gün", "isCorrect": True, "explanation": "Ders notu tablosundaki resmi evreler ve süreler eksiksiz verilmiştir."},
            {"key": "B", "text": "Folikül: 1 gün | Ovulasyon: 10 gün | Korpus Luteum: 1 gün | Menstruasyon: 20 gün", "isCorrect": False, "explanation": "Süreler tamamen hatalıdır."},
            {"key": "C", "text": "Folikül: 25 gün | Ovulasyon: 1. gün | Korpus Luteum: 30 gün | Menstruasyon: 1 saat", "isCorrect": False, "explanation": "Süreler orantısızdır."},
            {"key": "D", "text": "Folikül: 3 gün | Ovulasyon: 28. gün | Korpus Luteum: 2 gün | Menstruasyon: 14 gün", "isCorrect": False, "explanation": "Fizyolojiye aykırıdır."}
        ])
    ]
    slides.append(make_slide(11, "Menstrüel Döngünün Dört Temel Evresi", "Folikül, ovulasyon, korpus luteum ve menstruasyon evrelerinin genel mimarisi", "Fizyoloji", s11_narrative, s11_bullets, s11_elements))

    # Slide 12: Folikül Evresi (10-14 Gün) Dinamikleri
    s12_narrative = (
        "Folikül evresi, menstrüel döngünün başlangıcından ovulasyona kadar geçen 10-14 günlük "
        "hazırlık ve büyüme periyodudur.\n\n"
        "- **FSH Uyarısı:** Hipofiz ön lobundan salgılanan FSH, overdeki primordial ve primer folikülleri "
        "uyararak bir kohortun büyümesini başlatır.\n"
        "- **Folikül Gelişimi:** Genellikle foliküllerden biri dominant hale gelir, folikül kılıfı "
        "(teka ve granüloza) kalınlaşır ve içi sıvı (antrum) ile dolar.\n"
        "- **Oosit Olgunlaşması:** Folikül içindeki primer oosit mayoz bölünmesine devam ederek döllenme "
        "özelliği kazanacak olgun ikincil oosit yönünde ilerler.\n"
        "- **Östrojen ve Feedback:** Gelişen folikülden bol miktarda östrojen salgılanır; kanda östrojen "
        "arttığında hipofizin FSH salgısı negatif feedback ile azalır.\n\n"
        "> [!NOTE]\n"
        "> Folikül evresinde FSH folikülü büyütür, östrojen salgılanır ve artan östrojen hipofizin FSH salgısını azaltır."
    )
    s12_bullets = [
        "Folikül evresi 10-14 gün sürer; hipofizden salgılanan FSH folikülleri uyarır.",
        "Foliküllerden biri gelişir, folikül kılıfı kalınlaşır ve içi sıvı dolar.",
        "Folikülden östrojen salgılanır; kanda östrojen arttığında hipofizin FSH salgısı azalır."
    ]
    s12_elements = [
        make_cloze("Folikül evresinde kanda östrojen arttığında hipofizin FSH salgısı azalır.", "FSH salgısı azalır", "Östrojenin hipofize negatif feedback etkisi"),
        make_table("Folikül Evresinin Hücresel Dinamikleri", ["Yapı / Hormon", "Gelişme", "Sonuç"], [
            {"cells": [{"text": "FSH Hormonu", "isMasked": False}, {"text": "Folikül hücrelerini stimüle eder", "isMasked": True, "hint": "folikül uyarıcı etki"}, {"text": "Kohort büyümesi başlar"}]},
            {"cells": [{"text": "Folikül Kılıfı", "isMasked": False}, {"text": "Kalınlaşır ve içi sıvı dolar", "isMasked": False}, {"text": "Antral folikül oluşumu", "isMasked": True, "hint": "sıvı dolu boşluk gelişimi"}]},
            {"cells": [{"text": "Östrojen", "isMasked": False}, {"text": "Plazmada giderek yükselir", "isMasked": False}, {"text": "Hipofiz FSH salgısını negatif feedbackle frenler"}]}
        ]),
        make_chain("Foliküler Faz İlerleme Zinciri", [
            "1. FSH Uyarısı: Hipofiz FSH salgılayarak folikül reseptörlerini uyarır.",
            "2. Folikül Seçilimi: Foliküllerden biri gelişip sıvı dolarak olgunlaşır.",
            "3. Östrojen Sentezi: Büyüyen granüloza hücreleri kana yüksek östrojen verir.",
            "4. Negatif Feedback: Artan östrojen hipofizin aşırı FSH salgısını baskılar."
        ]),
        make_recall("Folikül evresinde kanda östrojen konsantrasyonu arttığında hipofiz FSH salgısında ne gözlenir?", "Hipofizin FSH salgısı negatif feedback ile azalır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Folikül Evresi", [
            {"text": "Folikül evresi 10-14 gün sürer.", "isLie": False, "explanation": "Doğru. Tipik süredir."},
            {"text": "FSH folikülleri uyararak folikül kılıfının kalınlaşmasını ve içinin sıvı dolmasını sağlar.", "isLie": False, "explanation": "Doğru. Morfolojik büyümedir."},
            {"text": "Kanda östrojen yükseldikçe hipofizden salgılanan FSH miktarı katlanarak artar.", "isLie": True, "explanation": "Tuzak! Kanda östrojen arttığında negatif feedback ile hipofizin FSH salgısı azalır."},
            {"text": "Yumurta hücresi folikül içinde olgunlaşarak döllenme özelliği kazanır.", "isLie": False, "explanation": "Doğru. Oogenez ilerler."}
        ]),
        make_quiz("Folikül evresinde (10-14 gün) folikülden salgılanan östrojen kanda arttığında hipofiz bezi nasıl yanıt verir?", [
            {"key": "A", "text": "Hipofizin FSH salgısı negatif feedback ile azalır", "isCorrect": True, "explanation": "Ders notunda açıkça: 'kanda östrojen arttığında hipofizin FSH salgısı azalır' denmektedir."},
            {"key": "B", "text": "Hipofiz derhal kalsitonin salgısını durdurur", "isCorrect": False, "explanation": "Kalsitonin tiroid parafoliküler hücrelerinden salgılanır."},
            {"key": "C", "text": "FSH salgısı yüz katına çıkar", "isCorrect": False, "explanation": "FSH artmaz, azalır."},
            {"key": "D", "text": "Hipofiz ön lobu tamamen nekroze olur", "isCorrect": False, "explanation": "Fizyolojik geri bildirimdir, nekroz olmaz."}
        ])
    ]
    slides.append(make_slide(12, "Folikül Evresi (10-14 Gün) Dinamikleri", "FSH uyarısı, antral folikül oluşumu, östrojen artışı ve FSH negatif feedbacki", "Fizyoloji", s12_narrative, s12_bullets, s12_elements))

    # Slide 13: Ovulasyon Evresi (14. Gün) ve LH Rolü
    s13_narrative = (
        "Ovulasyon evresi, olgunlaşmış dişi gametin overden periton boşluğuna atıldığı kritik dönüm noktasıdır.\n\n"
        "- **Tanım:** Folikülün yırtılıp olgunlaşmış ikincil oositin serbest hâle gelmesine **ovulasyon** "
        "(yumurtlama) denir.\n"
        "- **Zamanlama ve Hormon:** Ovulasyon menstrüel döngünün **14. gününde** gerçekleşir ve mutlak "
        "olarak **hipofizden salgılanan LH etkisiyle** yürütülür.\n"
        "- **Fertil Pencere:** Döllenme ve gebeliğin başlama ihtimalinin en yüksek olduğu dönem, "
        "**ovulasyondan sonraki birkaç gündür**.\n"
        "- **Oosit Alımı:** Serbest kalan oosit tubanın fimbria uçları tarafından yakalanarak ampullaya "
        "doğru iletilir ve spermle karşılaşmaya hazır hale gelir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ovulasyon siklusun 14. gününde hipofizden salgılanan LH etkisiyle gerçekleşir; gebelik ihtimali ovulasyondan sonraki birkaç gün en yüksektir."
    )
    s13_bullets = [
        "Folikülün yırtılıp ikincil oositin serbest kalmasına ovulasyon (yumurtlama) denir.",
        "Ovulasyon 14. günde hipofizden salgılanan LH etkisiyle gerçekleşir.",
        "Döllenme ve hamilelik ihtimalinin en fazla olduğu evre ovulasyondan sonraki birkaç gündür."
    ]
    s13_elements = [
        make_cloze("Folikülün yırtılıp ikincil oositin serbest kalması olan ovulasyon hipofizden salgılanan LH etkisiyle gerçekleşir.", "LH etkisiyle", "Ovulasyonu gerçekleştiren hormon"),
        make_table("Ovulasyon Evresi Temel Parametreleri", ["Parametre", "Değer / Mekanizma", "Klinik Yansıması"], [
            {"cells": [{"text": "Gerçekleşme Zamanı", "isMasked": False}, {"text": "Siklusun 14. günü", "isMasked": True, "hint": "on dördüncü gün"}, {"text": "28 günlük siklusun tam ortası"}]},
            {"cells": [{"text": "Primer Hormonal Neden", "isMasked": False}, {"text": "Hipofiz LH piki", "isMasked": False}, {"text": "Folikül rüptürü ve oosit atılımı", "isMasked": True, "hint": "yumurtlama uyarısı"}]},
            {"cells": [{"text": "En Yüksek Fertilite", "isMasked": False}, {"text": "Ovulasyondan sonraki birkaç gün", "isMasked": False}, {"text": "Döllenme ve gebelik ihtimali zirvededir"}]}
        ]),
        make_chain("Ovulasyon Patofizyolojik Akışı", [
            "1. LH Piki: Hipofiz masif LH deşarjı yapar.",
            "2. Enzimatik Sindirim: Folikül apeksindeki kollajenazlar aktive olur.",
            "3. Stigma Rüptürü: Folikül duvarı açılarak ikincil oosit atılır (14. gün).",
            "4. Fertil Pencere: Takip eden birkaç gün içinde ampullada döllenme imkanı en yüksektir."
        ]),
        make_recall("Ovulasyon siklusun kaçıncı gününde ve hangi hipofiz hormonunun etkisiyle gerçekleşir?", "Siklusun 14. gününde, hipofizden salgılanan LH etkisiyle gerçekleşir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ovulasyon Evresi", [
            {"text": "Folikülün yırtılıp olgunlaşmış ikincil oositin serbestleşmesine ovulasyon denir.", "isLie": False, "explanation": "Doğru. Tanımdır."},
            {"text": "Ovulasyon hipofizden salgılanan LH etkisiyle gerçekleşir.", "isLie": False, "explanation": "Doğru. Ana tetikleyicidir."},
            {"text": "Döllenme ve hamilelik ihtimali ovulasyondan sonraki birkaç gün en düşüktür, sıfıra iner.", "isLie": True, "explanation": "Tuzak! Döllenme ve hamileliğin başlama ihtimalinin en FAZLA olduğu evre ovulasyondan sonraki birkaç gündür."},
            {"text": "Ovulasyon tipik olarak menstrüel siklusun 14. gününde izlenir.", "isLie": False, "explanation": "Doğru. Ortalama 28 günlük siklusta 14. gündür."}
        ]),
        make_quiz("Folikülün yırtılarak ikincil oositin serbest kalmasını sağlayan hormon ve gerçekleştiği siklus günü hangisidir?", [
            {"key": "A", "text": "LH etkisiyle, 14. günde gerçekleşir", "isCorrect": True, "explanation": "Ders notunda açıkça: 'ovulasyon hipofizden salgılanan LH etkisiyle gerçekleşir ve 14. gündür' denmektedir."},
            {"key": "B", "text": "FSH etkisiyle, 1. günde gerçekleşir", "isCorrect": False, "explanation": "FSH folikülü büyütür, yırtmaz."},
            {"key": "C", "text": "Östrojen etkisiyle, 28. günde gerçekleşir", "isCorrect": False, "explanation": "28. gün menstrüasyon öncesidir."},
            {"key": "D", "text": "HCG etkisiyle, 5. ayda gerçekleşir", "isCorrect": False, "explanation": "HCG gebelikte etkindir."}
        ])
    ]
    slides.append(make_slide(13, "Ovulasyon Evresi (14. Gün) ve LH Rolü", "Folikül rüptürü, ikincil oosit salınımı, LH etkisi ve yüksek fertilite penceresi", "Fizyoloji", s13_narrative, s13_bullets, s13_elements))

    # Slide 14: Korpus Luteum Evresi (10-14 Gün)
    s14_narrative = (
        "Korpus luteum evresi, ovulasyonu izleyen ve menstrüel siklusun ikinci yarısını kapsayan 10-14 günlük dönemdir.\n\n"
        "- **Sarı Cismin Oluşumu:** Ovulasyonda yırtılan folikül, LH etkisiyle hızla luteinize olarak "
        "lipidden zengin sarı cisme (**korpus luteum**) dönüşür.\n"
        "- **Hormon Salgısı:** Korpus luteum **çok miktarda progesteron, daha az miktarda östrojen** salgılar.\n"
        "- **Kavite Hazırlığı:** Progesteron uterin kaviteyi (döl yatağı) embriyonun olası implantasyonuna "
        "karşı hazırlar; bezlerin salgısını artırır ve stromayı süngerimsi hale getirir.\n"
        "- **Süre Kararlılığı:** Normal sikluslarda korpus luteumun yaşam süresi oldukça sabittir ve "
        "yaklaşık 10-14 gün devam eder.\n\n"
        "> [!NOTE]\n"
        "> Yırtılan folikül LH etkisiyle korpus luteuma dönüşür; çok miktarda progesteron, daha az östrojen salgılar."
    )
    s14_bullets = [
        "Ovulasyonda yırtılan folikül LH etkisiyle korpus luteuma dönüşür.",
        "Korpus luteum evresi 10-14 gün sürer.",
        "Korpus luteum çok miktarda progesteron, daha az miktarda östrojen salgılar."
    ]
    s14_elements = [
        make_cloze("Ovulasyonda yırtılan folikül korpus luteuma dönüşür; çok miktarda progesteron, daha az miktarda östrojen salgılar.", "progesteron", "Korpus luteumun bol ürettiği hormon"),
        make_table("Korpus Luteum Evresi Özellikleri", ["Özellik", "Durum / Süre", "İşlev"], [
            {"cells": [{"text": "Evre Süresi", "isMasked": False}, {"text": "10-14 gün", "isMasked": True, "hint": "on ila on dört gün"}, {"text": "Luteal faz süresi"}]},
            {"cells": [{"text": "Baskın Hormon", "isMasked": False}, {"text": "Çok miktarda progesteron", "isMasked": False}, {"text": "Uterus kavitesini embriyoya hazırlama", "isMasked": True, "hint": "döl yatağını hazırlama"}]},
            {"cells": [{"text": "İkincil Hormon", "isMasked": False}, {"text": "Daha az miktarda östrojen", "isMasked": False}, {"text": "Endometrial desteğin sürdürülmesi"}]}
        ]),
        make_chain("Luteal Transformasyon Basamakları", [
            "1. Folikül Rüptürü: Oosit atıldıktan sonra teka ve granüloza hücreleri çöker.",
            "2. Luteinizasyon: LH etkisiyle hücreler lipid biriktirip korpus luteumu oluşturur.",
            "3. Yüksek Progesteron: Korpus luteumdan yoğun progesteron salınır (10-14 gün).",
            "4. İmplantasyon Hazırlığı: Uterus iç duvarı embriyo için süngerimsi kıvama gelir."
        ]),
        make_recall("Korpus luteumdan salgılanan hormonların orantısal dağılımı nasıldır?", "Çok miktarda progesteron, daha az miktarda östrojen salgılanır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Korpus Luteum Evresi", [
            {"text": "Ovulasyonda yırtılan folikül LH etkisiyle korpus luteuma dönüşür.", "isLie": False, "explanation": "Doğru. Luteinizasyon sürecidir."},
            {"text": "Korpus luteum evresi yaklaşık 10-14 gün sürer.", "isLie": False, "explanation": "Doğru. Tipik luteal süredir."},
            {"text": "Korpus luteum sadece testosteron üretir, asla progesteron salgılayamaz.", "isLie": True, "explanation": "Tuzak! Korpus luteum çok miktarda progesteron ve daha az miktarda östrojen salgılar."},
            {"text": "Progesteron uterin kaviteyi embriyonun yerleşme olasılığına karşı hazırlar.", "isLie": False, "explanation": "Doğru. Temel biyolojik görevidir."}
        ]),
        make_quiz("Korpus luteum evresinde (10-14 gün) over dokusundan salgılanan hormon profili nasıldır?", [
            {"key": "A", "text": "Çok miktarda progesteron, daha az miktarda östrojen salgılanır", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'korpus luteum çok miktarda progesteron, daha az miktarda östrojen salgılar' denmektedir."},
            {"key": "B", "text": "Sadece yüksek miktarda GnRH salgılanır", "isCorrect": False, "explanation": "GnRH hipotalamus hormonudur."},
            {"key": "C", "text": "Yalnızca oksitosin ve vazopressin salgılanır", "isCorrect": False, "explanation": "Nörohipofiz hormonlarıdır."},
            {"key": "D", "text": "Hormon üretimi tamamen durur ve sıfıra iner", "isCorrect": False, "explanation": "Korpus luteum son derece aktif bir endokrin bezdir."}
        ])
    ]
    slides.append(make_slide(14, "Korpus Luteum Evresi (10-14 Gün)", "Luteinizasyon, 10-14 günlük evre, bol progesteron ve az miktarda östrojen salgısı", "Fizyoloji", s14_narrative, s14_bullets, s14_elements))

    # Slide 15: Menstruasyon Evresi (3-5 Gün)
    s15_narrative = (
        "Menstruasyon evresi, döllenme gerçekleşmediğinde siklusun hücresel ve dokusal yıkımla sonlandığı 3-5 günlük periyottur.\n\n"
        "- **Luteolizis:** Yumurta döllenmezse korpus luteumun yapısı hızla bozulur (luteolizis) "
        "ve progesteron-östrojen salgısı aniden düşer.\n"
        "- **Doku Parçalanması:** Hormonal çekilme sonucu uterin kavitenin iç duvarı parçalanır.\n"
        "- **Vajinal Atılım:** Oluşan doku parçaları döllenmemiş yumurta hücresiyle beraber kanamalar "
        "hâlinde vajinadan dışarı atılır.\n"
        "- **Yeni Siklusun Başlangıcı:** Kanamanın ilk günü, biyolojik ve klinik olarak yeni bir "
        "menstrüel döngünün birinci günüdür; kanama 3-5 gün devam eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Döllenme olmazsa progesteron azalır, dokular dökülür; kanamanın ilk günü yeni bir menstrüel döngünün 1. günüdür ve menstruasyon 3-5 gün sürer."
    )
    s15_bullets = [
        "Döllenme olmazsa korpus luteum bozulur ve progesteron salgısı azalır.",
        "Uterin iç duvar parçalanır, dokular ve döllenmemiş yumurta kanamayla vajinadan atılır.",
        "Menstruasyon evresi 3-5 gün sürer; kanamanın ilk günü yeni döngünün 1. günüdür."
    ]
    s15_elements = [
        make_cloze("Yumurta döllenmezse korpus luteum bozulur ve kanamanın ilk günü yeni bir menstrüel döngünün birinci günüdür.", "birinci günüdür", "Kanamanın başladığı günün siklustaki yeri"),
        make_table("Menstruasyon Evresi Dinamikleri", ["Aşama", "Fizyolojik Değişim", "Klinik Yansıması"], [
            {"cells": [{"text": "Korpus Luteum Gerilemesi", "isMasked": False}, {"text": "Progesteron ve östrojen hızla düşer", "isMasked": True, "hint": "hormon çekilmesi"}, {"text": "Hormon desteği kesilir"}]},
            {"cells": [{"text": "Kanamalı Dökülme", "isMasked": False}, {"text": "Fonksiyonel doku parçalanır", "isMasked": False}, {"text": "3-5 gün süren menstrüel kanama", "isMasked": True, "hint": "üç ila beş günlük kanama periyodu"}]},
            {"cells": [{"text": "Döngü Sıfırlanması", "isMasked": False}, {"text": "Kanamanın 1. günü", "isMasked": False}, {"text": "Yeni menstrüel siklusun başlangıcı"}]}
        ]),
        make_chain("Menstrüel Yıkım Zinciri", [
            "1. Döllenme Yokluğu: Gebelik sinyali (HCG) gelmez.",
            "2. Luteal Bozulma: Korpus luteum geriler ve progesteron düşer.",
            "3. Dokusal Nekroz: Fonksiyonel tabaka beslenemez ve parçalanır.",
            "4. Dışarı Atılım: Doku artıkları ve döllenmemiş yumurta kanamayla atılır (3-5 gün)."
        ]),
        make_recall("Menstruasyon evresinin normal süresi kaç gündür ve yeni siklus ne zaman başlar?", "Menstruasyon 3-5 gün sürer; kanamanın ilk günü yeni bir menstrüel döngünün birinci günüdür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Menstruasyon Evresi", [
            {"text": "Yumurta döllenmezse korpus luteumun yapısı bozulur ve progesteron azalır.", "isLie": False, "explanation": "Doğru. Luteolizis mekanizmasıdır."},
            {"text": "Kanamanın ilk günü yeni bir menstrüel döngünün birinci günüdür.", "isLie": False, "explanation": "Doğru. Döngü kanamayla başlar."},
            {"text": "Menstruasyon evresi normal bir kadında en az 20 gün boyunca aralıksız sürer.", "isLie": True, "explanation": "Tuzak! Menstruasyon evresi 3-5 gün sürer."},
            {"text": "Doku parçaları döllenmemiş yumurtayla beraber kanama hâlinde atılır.", "isLie": False, "explanation": "Doğru. Dökülme içeriğidir."}
        ]),
        make_quiz("Menstruasyon evresi süresi ve menstrüel siklus başlangıcı ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Menstruasyon 3-5 gün sürer ve kanamanın ilk günü yeni döngünün 1. günüdür", "isCorrect": True, "explanation": "Ders notunda açıkça: 'menstruasyon evresi 3-5 gündür ve kanamanın ilk günü yeni bir menstrüel döngünün birinci günüdür' denmektedir."},
            {"key": "B", "text": "Menstruasyon 15 gün sürer ve ovulasyon bittiğinde yeni döngü başlar", "isCorrect": False, "explanation": "Süre 3-5 gündür."},
            {"key": "C", "text": "Menstruasyon sadece 1 saat sürer ve doku atılmaz", "isCorrect": False, "explanation": "3-5 gün sürer."},
            {"key": "D", "text": "Yumurta döllendiğinde menstruasyon evresi daha da şiddetlenir", "isCorrect": False, "explanation": "Döllenme olduğunda menstruasyon durur."}
        ])
    ]
    slides.append(make_slide(15, "Menstruasyon Evresi (3-5 Gün)", "Luteolizis, dokusal parçalanma, 3-5 günlük kanama ve yeni siklus başlangıcı", "Fizyoloji", s15_narrative, s15_bullets, s15_elements))

    # Slide 16: Progesteronun Uterin Kaviteye Etkileri
    s16_narrative = (
        "Progesteron, korpus luteum evresinde endometrium dokusunu hücresel ve vasküler olarak tamamen yeniden yapılandırır.\n\n"
        "- **Süngerimsi Yapı:** Progesteronun etkisiyle uterin kavitenin iç duvarı belirgin biçimde "
        "kalınlaşarak **süngerimsi bir yapı** hâlini alır.\n"
        "- **Vasküler Genişleme:** Endometriumdaki kılcal kan damarları genişler ve hiperemik hale gelir.\n"
        "- **Salgı Artışı:** Endometrial bezlerin kıvrıntılı hale gelmesiyle birlikte dokuda **kan ve mukus salgısı artar**.\n"
        "- **İmplantasyon Ortamı:** Bu vasküler ve sekretuar zenginleşme, olası bir zigotun tutunması "
        "ve erken embriyonik beslenmesi için ideal biyokimyasal mikroçevreyi sağlar.\n\n"
        "> [!NOTE]\n"
        "> Progesteron etkisiyle iç duvar kalınlaşarak süngerimsi hal alır; kılcal damarlar genişler, kan ve mukus salgısı artar."
    )
    s16_bullets = [
        "Progesteron etkisiyle uterin kavitenin iç duvarı kalınlaşarak süngerimsi yapı alır.",
        "Kılcal damarlar genişler, kanlanma belirgin artar.",
        "Endometriumda kan ve mukus salgısı artarak embriyo için uygun ortam hazırlanır."
    ]
    s16_elements = [
        make_cloze("Progesteronun etkisiyle uterin kavitenin iç duvarı kalınlaşarak süngerimsi bir yapı hâlini alır.", "süngerimsi bir yapı", "Uterus iç duvarının progesteronla aldığı hal"),
        make_table("Progesteronun Endometrial Etkileri", ["Doku Komponenti", "Progesteron Etkisi", "Fizyolojik Önemi"], [
            {"cells": [{"text": "Uterin İç Duvar", "isMasked": False}, {"text": "Kalınlaşarak süngerimsi yapı alır", "isMasked": True, "hint": "süngerimsi doku dönüşümü"}, {"text": "Yumuşak implantasyon yatağı"}]},
            {"cells": [{"text": "Kılcal Damarlar", "isMasked": False}, {"text": "Belirgin biçimde genişler", "isMasked": False}, {"text": "Trofoblastlara zengin kan akımı", "isMasked": True, "hint": "damarsal beslenme artışı"}]},
            {"cells": [{"text": "Endometrial Bezler", "isMasked": False}, {"text": "Kan ve mukus salgısını artırır", "isMasked": False}, {"text": "Embriyonun beslenmesi"}]}
        ]),
        make_chain("Süngerimsi Transformasyon Akışı", [
            "1. Luteal Progesteron: Korpus luteumdan kana yoğun progesteron verilir.",
            "2. Reseptör Aktivasyonu: Endometrium stroma ve epitelinde progesteron reseptörleri bağlanır.",
            "3. Vasküler Dilatasyon: Kılcal damarlar genişler, perfüzyon katlanır.",
            "4. Mukus ve Glikojen Salgısı: Bezler yoğun mukus salgılayarak kaviteyi süngerimsi yapar."
        ]),
        make_recall("Progesteron etkisiyle uterin kavite iç duvarı nasıl bir yapı kazanır ve salgılarda ne değişir?", "İç duvar kalınlaşarak süngerimsi bir yapı halini alır; kılcal damarlar genişler, kan ve mukus salgısı artar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Progesteronun Uterin Etkisi", [
            {"text": "Progesteron etkisiyle uterin kavitenin iç duvarı süngerimsi bir yapı halini alır.", "isLie": False, "explanation": "Doğru. Karakteristik tanımlamadır."},
            {"text": "Endometriumdaki kılcal damarlar genişler.", "isLie": False, "explanation": "Doğru. Vaskülarizasyon artar."},
            {"text": "Progesteron tüm kılcal damarları tamamen kurutur ve mukus salgısını sıfıra indirir.", "isLie": True, "explanation": "Tuzak! Progesteron kılcal damarları genişletir, kan ve mukus salgısını artırır."},
            {"text": "Süngerimsi yapı embriyonun implantasyonu için ideal bir zemin sunar.", "isLie": False, "explanation": "Doğru. Temel fizyolojik hedeftir."}
        ]),
        make_quiz("Progesteron hormonunun etkisiyle uterin kavitenin iç duvarında ve salgılarında hangi değişiklik meydana gelir?", [
            {"key": "A", "text": "İç duvar kalınlaşarak süngerimsi bir yapı alır; kılcal damarlar genişler, kan ve mukus salgısı artar", "isCorrect": True, "explanation": "Ders notunda progesteron etkisi kelimesi kelimesine bu şekilde açıklanmıştır."},
            {"key": "B", "text": "Endometrium tamamen kurur, atrofiye uğrar ve tüm bezler kaybolur", "isCorrect": False, "explanation": "Atrofi hormon yokluğunda olur."},
            {"key": "C", "text": "Sadece kemik iliğinde eritrosit üretimi durur", "isCorrect": False, "explanation": "Uterus ile ilgisizdir."},
            {"key": "D", "text": "Myometrium kas lifleri yırtılarak masif nekroz oluşturur", "isCorrect": False, "explanation": "Progesteron kas kasılmasını gevşetir, yırtmaz."}
        ])
    ]
    slides.append(make_slide(16, "Progesteronun Uterin Kaviteye Etkileri", "Süngerimsi transformasyon, kılcal damar dilatasyonu, kan ve mukus salgı artışı", "Fizyoloji", s16_narrative, s16_bullets, s16_elements))

    # Slide 17: Siklus Boyunca FSH ve LH Salınım Eğrileri
    s17_narrative = (
        "Hipofiz gonadotropinleri FSH ve LH, menstrüel siklus boyunca birbirini tamamlayan özgül dalgalanma eğrileri çizer.\n\n"
        "- **GnRH Portal Uyarımı:** Hipotalamustan pulsatil salgılanan GnRH portal sistem ile hipofize "
        "ulaşarak özellikle LH'ın salgılanmasını sağlar.\n"
        "- **FSH Otonomisi:** FSH da GnRH etkisiyle salgılansa da daha çok bağımsız olarak salgılanmaktadır.\n"
        "- **Siklus Ortası ve İkinci Yarı:** Siklus ortasında FSH seviyelerinde hafif bir düşme olur; "
        "buna rağmen folikül büyümesi sürer. Siklusun ikinci yarısında FSH değerleri foliküler fazdakine oranla belirgin olarak düşüktür.\n"
        "- **LH Eğrisi:** Foliküler fazdaki LH değerleri FSH'a göre daha düşüktür. Preovulatuar dönemde "
        "artan östrojenin pozitif feedbacki ile LH pik yaparak ovulasyona katkıda bulunur, ardından tekrar bazal düzeylerine iner.\n\n"
        "> [!NOTE]\n"
        "> GnRH özellikle LH salgısını uyarır. Siklusun ikinci yarısında FSH seviyesi foliküler fazdakinden daha düşüktür; LH ise preovulatuar pik sonrası düşer."
    )
    s17_bullets = [
        "GnRH portal sistemle hipofize gelerek özellikle LH salgılanmasını sağlar.",
        "Siklusun ikinci yarısında FSH değerleri foliküler fazdakine oranla daha düşüktür.",
        "LH preovulatuar dönemde pik yaparak ovulasyonu sağlar, sonra foliküler fazdaki değerine düşer."
    ]
    s17_elements = [
        make_cloze("Siklusun ikinci yarısında FSH değerleri foliküler fazdakine oranla daha düşüktür.", "daha düşüktür", "FSH'ın ikinci yarıdaki seviyesi"),
        make_table("FSH ve LH Salınım Eğrileri Karşılaştırması", ["Faz", "FSH Düzeyi", "LH Düzeyi"], [
            {"cells": [{"text": "Foliküler Faz (1-10. gün)", "isMasked": False}, {"text": "Yüksek (folikül kohortunu uyarır)", "isMasked": False}, {"text": "FSH'a göre daha düşük seyreder", "isMasked": True, "hint": "başlangıçta daha düşük LH"}]},
            {"cells": [{"text": "Preovulatuar (13-14. gün)", "isMasked": False}, {"text": "Hafif düşme / küçük pik", "isMasked": False}, {"text": "Masif zirve (LH piki)", "isMasked": True, "hint": "ovulasyonu tetikleyen pik"}]},
            {"cells": [{"text": "Luteal Faz (15-28. gün)", "isMasked": False}, {"text": "Foliküler fazdan daha düşüktür", "isMasked": True, "hint": "luteal dönemde düşük FSH"}, {"text": "Bazal düşük düzeylere iner"}]}
        ]),
        make_chain("Gonadotropin Dalgalanma Zinciri", [
            "1. GnRH İletimi: Portal damarlarla hipofize gelerek gonadotropinleri uyarır.",
            "2. Foliküler Başlangıç: FSH yüksek seyreder, LH nispeten düşüktür.",
            "3. Siklus Ortası Piki: Östrojen pozitif feedbacki ile LH pik yapar.",
            "4. Luteal Faz Düşüşü: Siklusun ikinci yarısında FSH ve LH bazal seviyelere iner."
        ]),
        make_recall("Siklusun ikinci yarısında FSH değerleri foliküler fazdakine kıyasla nasıldır?", "Foliküler fazdakine oranla belirgin olarak daha düşüktür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Gonadotropin Eğrileri", [
            {"text": "GnRH hipofize gelerek gonadotropinlerin, özellikle LH'ın salgılanmasını sağlar.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Siklusun ikinci yarısında FSH değerleri foliküler fazdakine oranla daha düşüktür.", "isLie": False, "explanation": "Doğru. Endokrin profildir."},
            {"text": "LH hormonu luteal faz boyunca sürekli ovulasyon pikindeki maksimum seviyesinde kalır.", "isLie": True, "explanation": "Tuzak! LH piki ovulasyondan sonra hızla foliküler fazdaki bazal değerlerine düşer."},
            {"text": "Foliküler fazdaki LH değerleri genellikle FSH değerlerine göre daha düşük seyreder.", "isLie": False, "explanation": "Doğru. Normal fizyolojidir."}
        ]),
        make_quiz("Menstrüel siklus boyunca gonadotropinlerin salınım seyri ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Siklusun ikinci yarısında FSH değerleri foliküler fazdakine oranla daha düşüktür", "isCorrect": True, "explanation": "Ders notunda açıkça: 'siklusun ikinci yarısında FSH değerleri foliküler fazdakine oranla daha düşüktür' denmektedir."},
            {"key": "B", "text": "LH hiçbir zaman pik yapmaz, siklus boyu dümdüz sıfırdır", "isCorrect": False, "explanation": "LH 14. günde pik yapar."},
            {"key": "C", "text": "FSH sadece menstruasyonun bittiği gün 1 dakika salgılanır", "isCorrect": False, "explanation": "Sürekli salınımı vardır."},
            {"key": "D", "text": "GnRH doğrudan overe gidip folikülleri yırtar", "isCorrect": False, "explanation": "GnRH hipofizi uyarır."}
        ])
    ]
    slides.append(make_slide(17, "Siklus Boyunca FSH ve LH Salınım Eğrileri", "GnRH portal etkisi, siklusun ikinci yarısında düşük FSH ve LH piki dinamikleri", "Endokrinoloji", s17_narrative, s17_bullets, s17_elements))

    # Slide 18: Östrojen ve Progesteronun Siklus Boyunca Çapraz Seyri
    s18_narrative = (
        "Ovaryal steroid hormonlar östrojen ve progesteron, siklus boyunca zıt ve birbirini tamamlayan fazik dinamikler sergiler.\n\n"
        "- **Östrojenin İki Fazlılığı:** Östrojen 11-12. günde birinci pikini yapar; ovulasyonda hafif "
        "bir düşüşün ardından luteal fazda korpus luteumdan salgılanarak **daha küçük ikinci bir tepe** oluşturur.\n"
        "- **Menstruasyon Öncesi Çöküş:** Menstruasyona birkaç gün kala östrojen siklus başı taban düzeylerine hızla iner.\n"
        "- **Progesteronun Tek Fazlılığı:** Progesteron siklusun ilk 14 gününde yok denecek kadar azdır; "
        "ovulasyonla birlikte korpus luteumdan salınarak **luteal faz ortasında tek bir dev tepe** yapar.\n"
        "- **Çekilme Kanaması:** Korpus luteumun gerilemesiyle her iki hormonun eşzamanlı çöküşü "
        "endometriumdaki damarları daraltır ve kanamayı başlatır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Östrojen menstruasyona birkaç gün kala siklus başı düzeylerine iner; progesteron luteal faz ortasında pik yaptıktan sonra hızla düşer."
    )
    s18_bullets = [
        "Östrojen 11-12. gün pikinden sonra menstruasyona birkaç gün kala siklus başı düzeylerine iner.",
        "Progesteron ilk yarıda yoktur, luteal faz ortasında en yüksek seviyeye ulaşır.",
        "Her iki hormonun menstruasyon öncesi ani düşüşü dökülmeyi tetikler."
    ]
    s18_elements = [
        make_cloze("Östrojen düzeyi menstruasyona birkaç gün kala siklus başı düzeylerine iner.", "siklus başı düzeylerine", "Östrojenin menstruasyon öncesi indiği seviye"),
        make_table("Östrojen ve Progesteron Karşılaştırmalı Zaman Çizelgesi", ["Hormon", "İlk Yarı (1-14. gün)", "İkinci Yarı (15-28. gün)"], [
            {"cells": [{"text": "Östrojen", "isMasked": False}, {"text": "Giderek artar, 11-12. gün pik yapar", "isMasked": True, "hint": "preovulatuar pik"}, {"text": "İkincil luteal yükselme ve menstrüasyon öncesi çöküş"}]},
            {"cells": [{"text": "Progesteron", "isMasked": False}, {"text": "Salgılanmaz (yok düzeyinde)", "isMasked": False}, {"text": "Luteal faz ortasında en yüksek seviyeye ulaşır", "isMasked": True, "hint": "luteal faz pik zamanı"}]}
        ]),
        make_chain("Steroid Çöküş ve Kanama Zinciri", [
            "1. Luteal Faz Ortası: Östrojen ve progesteron yüksek seviyede seyreder.",
            "2. Luteolizis Başlangıcı: Korpus luteum fonksiyonunu kaybetmeye başlar.",
            "3. Hormon Çöküşü: Menstruasyona birkaç gün kala östrojen ve progesteron tabana iner.",
            "4. Vasküler Spazm: Çekilme etkisiyle spiral damarlar kasılır ve kanama başlar."
        ]),
        make_recall("Östrojen hormonu menstruasyon başlamadan önceki günlerde nasıl bir seyir izler?", "Menstruasyona birkaç gün kala siklus başı düzeylerine hızla iner."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Steroid Hormon Eğrileri", [
            {"text": "Östrojen 11-12. günde pik yapar.", "isLie": False, "explanation": "Doğru. Foliküler faz zirvesidir."},
            {"text": "Östrojen menstruasyona birkaç gün kala siklus başı düzeylerine iner.", "isLie": False, "explanation": "Doğru. Çekilme dönemidir."},
            {"text": "Progesteron siklusun 1. gününden 28. gününe kadar hiç değişmeyen sabit bir çizgide salgılanır.", "isLie": True, "explanation": "Tuzak! Progesteron ilk yarıda salgılanmaz; luteal faz ortasında pik yapıp ardından hızla düşer."},
            {"text": "Her iki hormonun düşüşü menstrüel dökülmeyi başlatır.", "isLie": False, "explanation": "Doğru. Çekilme kanaması prensibidir."}
        ]),
        make_quiz("Menstrüel siklusta over kaynaklı östrojen ve progesteron hormonlarının seyri ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Östrojen 11-12. günde pik yapar ve menstruasyona birkaç gün kala siklus başı düzeylerine iner", "isCorrect": True, "explanation": "Ders notunda östrojenin 11-12. günde pik yaptığı ve menstruasyona birkaç gün kala başlangıç düzeylerine indiği belirtilmiştir."},
            {"key": "B", "text": "Progesteron siklus başında en yüksek, sonunda en düşüktür", "isCorrect": False, "explanation": "İlk yarıda hiç salgılanmaz."},
            {"key": "C", "text": "Östrojen yalnızca menopozdan sonra pik yapar", "isCorrect": False, "explanation": "Menopozda östrojen düşer."},
            {"key": "D", "text": "Progesteron 11-12. günde LH ile birlikte pik yapar", "isCorrect": False, "explanation": "Progesteron luteal faz ortasında pik yapar."}
        ])
    ]
    slides.append(make_slide(18, "Östrojen ve Progesteronun Siklus Boyunca Çapraz Seyri", "Fazik steroid dinamikleri, menstruasyon öncesi düşüş ve çekilme sinyali", "Endokrinoloji", s18_narrative, s18_bullets, s18_elements))

    # Slide 19: Anovulatuar Sikluslar ve Fizyolojik Değişkenlikler
    s19_narrative = (
        "Menstrüel siklus her zaman saat gibi 28 günde bir kusursuz düzenlilikte çalışmaz.\n\n"
        "- **Yaşa Bağlı Stabilite:** Siklus uzunluğu kadının en fertil olduğu **20-30'lu yaşlarda oldukça düzenli** seyreder.\n"
        "- **Geçiş Dönemleri:** Menarştan sonraki adolesan dönem ile menopozdan önceki perimenopozal "
        "dönemde sikluslar sıklıkla **anovulatuar (yumurtlamasız)** seyreder.\n"
        "- **Süre Değişkenliği:** Anovulatuar sikluslarda korpus luteum oluşmadığı için progesteron "
        "desteği bulunmaz; östrojenin kesintili etkisine bağlı olarak siklus süreleri büyük değişkenlik gösterir.\n"
        "- **Çevresel Faktörler:** Diyet, ağır egzersiz, emosyonel stres, doğum ve düşükler hipotalamik "
        "GnRH salınımını etkileyerek siklus sürelerinde belirgin farklılıklara yol açabilir.\n\n"
        "> [!NOTE]\n"
        "> Menarştan sonra ve menopozdan önce anovulatuar sikluslar sıktır; 20-30'lu yaşlar en düzenli dönemdir."
    )
    s19_bullets = [
        "Siklus uzunluğu 20-30'lu yaşlarda en düzenli seyreder.",
        "Menarştan sonra ve menopozdan önce anovulatuar sikluslara bağlı süre değişkenlikleri sıktır.",
        "Diyet, egzersiz, stres, doğum ve düşükler siklus süresini değiştirebilir."
    ]
    s19_elements = [
        make_cloze("Menarştan sonraki ve menopozdan önceki dönemlerde siklusların anovulatuar olmasına bağlı süreler değişkenlik gösterir.", "anovulatuar", "Yumurtlama olmadan geçen siklus tipi"),
        make_table("Yaşam Evrelerinde Siklus Düzeni", ["Dönem", "Siklus Karakteri", "Temel Neden"], [
            {"cells": [{"text": "Menarş Sonrası (Adolesan)", "isMasked": False}, {"text": "Düzensiz, değişken süreli", "isMasked": True, "hint": "aks olgunlaşmamışlığı"}, {"text": "Anovulatuar sikluslar sıktır (5-7 yıl)"}]},
            {"cells": [{"text": "20-30'lu Yaşlar", "isMasked": False}, {"text": "Düzenli (21-35 gün)", "isMasked": False}, {"text": "Matür ve ovulatuar sikluslar", "isMasked": True, "hint": "olgun üreme çağı"}]},
            {"cells": [{"text": "Perimenopoz", "isMasked": False}, {"text": "Düzensiz, değişken süreli", "isMasked": False}, {"text": "Ovaryal folikül tükenmesi ve anovulasyon"}]}
        ]),
        make_chain("Anovulatuar Değişkenlik Zinciri", [
            "1. HPA Ekseni Olgunlaşmamışlığı / Tüketimi: GnRH pulsatilitesi aksar.",
            "2. Ovulasyon Gerçekleşmez: LH piki oluşamaz ve folikül rüptüre olmaz.",
            "3. Korpus Luteum Yokluğu: Progesteron sentezlenemez.",
            "4. Süre Dalgalanması: Karşılanmamış östrojenle siklus süresi öngörülemez hale gelir."
        ]),
        make_recall("Menstrüel siklus sürelerinin en düzenli seyrettiği yaş grubu hangisidir?", "20-30'lu yaşlardır (menarş sonrası ve menopoz öncesi anovulasyona bağlı düzensizdir)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Siklus Düzenliliği", [
            {"text": "Siklus uzunluğu 20-30'lu yaşlarda oldukça düzenli seyreder.", "isLie": False, "explanation": "Doğru. En stabil dönemdir."},
            {"text": "Menarştan sonraki dönemde anovulatuar sikluslar sık görülür.", "isLie": False, "explanation": "Doğru. İlk 5-7 yıl regülasyon sürer."},
            {"text": "Menopoz öncesi kadınlarda siklus süreleri her zaman kesin olarak tam 28 gündür, hiç değişmez.", "isLie": True, "explanation": "Tuzak! Menopozdan önceki perimenopozal dönemde anovulatuar sikluslara bağlı süreler büyük değişkenlik gösterir."},
            {"text": "Diyet, aşırı egzersiz ve emosyonel stres siklus sürelerini etkileyebilir.", "isLie": False, "explanation": "Doğru. Hipotalamik aks hassastır."}
        ]),
        make_quiz("Menstrüel siklusların menarştan sonra ve menopozdan önce düzensizleşmesinin ve sürelerinin değişmesinin temel nedeni nedir?", [
            {"key": "A", "text": "Siklusların anovulatuar olmasına bağlı hormonal dalgalanmalar", "isCorrect": True, "explanation": "Ders notunda menarştan sonra ve menopozdan önce siklusların anovulatuar olmasına bağlı süre değişkenlikleri açıkça vurgulanmıştır."},
            {"key": "B", "text": "Kalp kapaklarının kalsifiye olması", "isCorrect": False, "explanation": "Genital fizyoloji ile ilgisizdir."},
            {"key": "C", "text": "Uterusun tamamen kaybolması", "isCorrect": False, "explanation": "Uterus mevcuttur."},
            {"key": "D", "text": "HCG'nin erkek cinsiyet geni üretmesi", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."}
        ])
    ]
    slides.append(make_slide(19, "Anovulatuar Sikluslar ve Fizyolojik Değişkenlikler", "20-30 yaş stabilitesi, menarş/menopoz geçişleri ve anovulasyon dinamikleri", "Klinik ve Fizyoloji", s19_narrative, s19_bullets, s19_elements))

    # Slide 20: [TEKRAR SAYFASI - CHECKPOINT 2] Menstrual Döngünün Evreleri ve Siklus Dinamikleri
    s20_narrative = (
        "Bu tekrar sayfasında 2. Bölüm boyunca ele aldığımız menstrüel döngünün dört evresini, "
        "evre sürelerini, folikül-LH-luteal ilişkilerini ve anovulatuar dalgalanmaları konsolide ediyoruz.\n\n"
        "- **Dört Evre ve Süreleri:** Folikül evresi (10-14 gün, FSH ile östrojen), Ovulasyon evresi "
        "(14. gün, LH etkisiyle), Korpus luteum evresi (10-14 gün, bol progesteron ve az östrojen), "
        "Menstruasyon evresi (3-5 gün, dökülme ve yeni siklus başlangıcı).\n"
        "- **Endometrial Yanıt:** Progesteron etkisiyle iç duvar süngerimsi hal alır, damarlar genişler, "
        "mukus salgısı artar; döllenme olmazsa progesteron düşüşüyle doku parçalanır.\n"
        "- **Gonadotropin Eğrileri:** Siklusun ikinci yarısında FSH foliküler fazdan daha düşüktür; "
        "LH preovulatuar pik sonrası düşer; 20-30 yaş arası en düzenli dönemdir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Folikül (10-14 gün) → Ovulasyon (14. gün, LH) → Korpus Luteum (10-14 gün, bol progesteron) → Menstruasyon (3-5 gün, ilk gün = 1. gün). Süngerimsi kavite, genişleyen kılcallar ve anovulatuar geçişler."
    )
    s20_bullets = [
        "Folikül 10-14 gün, Ovulasyon 14. gün (LH), Korpus Luteum 10-14 gün, Menstruasyon 3-5 gün sürer.",
        "Progesteron uterin iç duvarı süngerimsi yapar, kılcal damarları genişletir ve salgıyı artırır.",
        "Kanamanın ilk günü yeni döngünün 1. günüdür; 20-30 yaş arası düzenli, geçiş dönemleri anovulatuardır."
    ]
    s20_elements = [
        make_cloze("Menstrüel döngüde ovulasyon 14. günde LH etkisiyle gerçekleşirken korpus luteum evresi 10-14 gün sürer.", "10-14 gün", "Korpus luteum evresinin süresi"),
        make_table("2. Bölüm Büyük Evreler ve Dinamikler Tablosu", ["Evre", "Süre", "Hormonal Hakimiyet", "Kritik Olay"], [
            {"cells": [{"text": "Folikül Evresi", "isMasked": False}, {"text": "10-14 gün", "isMasked": True, "hint": "on ila on dört gün"}, {"text": "FSH ve yükselen östrojen", "isMasked": False}, {"text": "Antral folikül gelişimi"}]},
            {"cells": [{"text": "Ovulasyon Evresi", "isMasked": False}, {"text": "14. gün", "isMasked": False}, {"text": "Hipofiz LH piki", "isMasked": True, "hint": "lüteinizan hormon tepe noktası"}, {"text": "İkincil oositin serbest kalması"}]},
            {"cells": [{"text": "Korpus Luteum", "isMasked": False}, {"text": "10-14 gün", "isMasked": False}, {"text": "Bol progesteron, az östrojen", "isMasked": True, "hint": "luteal steroid salgısı"}, {"text": "Süngerimsi endometrial dönüşüm"}]},
            {"cells": [{"text": "Menstruasyon", "isMasked": False}, {"text": "3-5 gün", "isMasked": True, "hint": "üç ila beş günlük dökülme"}, {"text": "Östrojen ve progesteron çekilmesi", "isMasked": False}, {"text": "Fonksiyonel tabakanın kanamayla atılması"}]}
        ]),
        make_chain("Bölüm 2 Süreç Konsolidasyonu", [
            "1. Folikül Büyümesi (10-14 gün): FSH etkisiyle folikül kılıfı kalınlaşır, östrojen artar.",
            "2. Ovulasyon (14. gün): LH etkisiyle rüptür olur, en yüksek fertilite başlar.",
            "3. Luteal Faz (10-14 gün): Korpus luteum süngerimsi endometrium oluşturur.",
            "4. Menstruasyon (3-5 gün): Hormon çekilmesiyle parçalanan dokular atılır ve döngü 1. güne sıfırlanır."
        ]),
        make_recall("2. Bölümün dört ana evresini ve sürelerini eksiksiz özetleyiniz.", "Folikül evresi (10-14 gün), Ovulasyon evresi (14. gün), Korpus luteum evresi (10-14 gün), Menstruasyon evresi (3-5 gün)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 2. Bölüm Konsolidasyonu", [
            {"text": "Folikül evresi 10-14 gün, korpus luteum evresi 10-14 gün sürer.", "isLie": False, "explanation": "Doğru. Her iki ana faz 10-14 gündür."},
            {"text": "Ovulasyon 14. günde hipofizden salgılanan LH etkisiyle gerçekleşir.", "isLie": False, "explanation": "Doğru. Klasik 14. gün kuralıdır."},
            {"text": "Menstruasyon evresi 3-5 gün sürer ve kanamanın ilk günü yeni siklusun 1. günüdür.", "isLie": False, "explanation": "Doğru. Siklus başlangıç tanımıdır."},
            {"text": "Progesteron uterus iç duvarını incelterek kılcal damarları tamamen yok eder ve salgıyı keser.", "isLie": True, "explanation": "Tuzak! Progesteron iç duvarı kalınlaştırıp süngerimsi yapar, kılcalları genişletir, kan ve mukus salgısını artırır."}
        ]),
        make_quiz("Menstrüel döngünün evreleri ve süreleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Korpus luteum evresi 45 gün sürer ve sadece androjen salgılar", "isCorrect": True, "explanation": "Yanlış! Korpus luteum evresi 10-14 gün sürer; çok miktarda progesteron, daha az miktarda östrojen salgılar."},
            {"key": "B", "text": "Ovulasyon hipofizden salgılanan LH etkisiyle 14. günde gerçekleşir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Folikül evresi 10-14 gün sürer ve folikülden östrojen salgılanır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Menstruasyon evresi 3-5 gün sürer ve ilk günü yeni siklusun 1. günüdür", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(20, "[TEKRAR SAYFASI - CHECKPOINT 2] Menstrual Döngünün Evreleri ve Siklus Dinamikleri", "2. Bölümün kapsamlı konsolidasyonu: 4 evre süreleri, LH ve ovulasyon, korpus luteum ve süngerimsi endometrium", "Bölüm Tekrarı", s20_narrative, s20_bullets, s20_elements))

    return slides
