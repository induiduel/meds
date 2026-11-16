# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec7():
    slides = []

    # Slide 61: Endometrial Hiperplazi Tanımı ve Rölatif Östrojen Fazlalığı
    s61_narrative = (
        "Endometrial hiperplazi, glandüler ve stromal elemanların kontrolsüz biçimde çoğaldığı preneoplastik bir süreçtir.\n\n"
        "- **Hormonal Tetikleyici:** Progesteron seviyesine göre **rölatif östrojen fazlalığı** "
        "belirgin olarak veya uzun süre endometriumu etkilerse gelişir.\n"
        "- **Biyolojik Sonuç:** Karşılanmamış bu uyarım endometriumda preneoplastik olabilecek "
        "**abartılı proliferasyon (hiperplazi)** meydana getirir.\n"
        "- **Doku Dönüşümü:** Gland/stroma oranı belirgin şekilde artar; bezler yoğunlaşır, "
        "lümenler genişler ve stroma miktarı orantısal olarak azalır.\n"
        "- **Eşik Değer:** Her aşırı östrojen seviyesi potansiyel olarak endometrial hiperplaziye yol açabilir.\n\n"
        "> [!NOTE]\n"
        "> Progesteron seviyesine göre rölatif östrojen fazlalığı uzun süre endometriumu etkilerse preneoplastik abartılı proliferasyon (hiperplazi) gelişir."
    )
    s61_bullets = [
        "Progesteron seviyesine göre rölatif östrojen fazlalığına bağlı gelişir.",
        "Uzun süreli etki endometriumda preneoplastik abartılı proliferasyon (hiperplazi) yapar.",
        "Her aşırı östrojen seviyesi endometrial hiperplaziye neden olabilir."
    ]
    s61_elements = [
        make_cloze("Progesteron seviyesine göre rölatif östrojen fazlalığı uzun süre endometriumu etkilerse abartılı proliferasyon (hiperplazi) meydana gelir.", "rölatif östrojen fazlalığı", "Hiperplaziyi tetikleyen hormonal durum"),
        make_table("Endometrial Hiperplazi Temel Patogenezi", ["Bileşen", "Durum", "Biyolojik Etki"], [
            {"cells": [{"text": "Östrojen Düzeyi", "isMasked": False}, {"text": "Rölatif veya mutlak fazlalık", "isMasked": True, "hint": "yüksek östrojen etkisi"}, {"text": "Aşırı mitotik uyarım"}]},
            {"cells": [{"text": "Progesteron Düzeyi", "isMasked": False}, {"text": "Yetersiz veya tamamen yok", "isMasked": False}, {"text": "Frenleyici ve dökücü etkinin kalkması", "isMasked": True, "hint": "durdurucu hormon eksikliği"}]},
            {"cells": [{"text": "Doku Yanıtı", "isMasked": False}, {"text": "Preneoplastik abartılı proliferasyon", "isMasked": False}, {"text": "Endometrial hiperplazi tablosu"}]}
        ]),
        make_chain("Hiperplazi Gelişim Basamakları", [
            "1. Hormon Dengesizliği: Progesterona kıyasla rölatif östrojen fazlalığı oluşur.",
            "2. Sürekli Proliferasyon: Bez epiteli kesintisiz mitoz bölünmeye girer.",
            "3. Bez Yoğunlaşması: Stroma azalırken bezlerin hacmi ve sayısı katlanır.",
            "4. Hiperplazi Tablosu: Preneoplastik abartılı doku büyümesi şekillenir."
        ]),
        make_recall("Endometrial hiperplazinin ortaya çıkmasına neden olan temel hormonal dengesizlik nedir?", "Progesteron seviyesine göre rölatif östrojen fazlalığının uzun süre endometriumu etkilemesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hiperplazi Tanımı", [
            {"text": "Endometrial hiperplazi rölatif östrojen fazlalığı sonucu gelişir.", "isLie": False, "explanation": "Doğru. Temel nedendir."},
            {"text": "Uzun süreli etki preneoplastik abartılı proliferasyon meydana getirir.", "isLie": False, "explanation": "Doğru. Tanımıdır."},
            {"text": "Endometrial hiperplazi sadece östrojen sıfırlandığında ve progesteron tavan yaptığında görülür.", "isLie": True, "explanation": "Tuzak! Hiperplazi tam tersine rölatif ÖSTROJEN FAZLALIĞI ve progesteron yetersizliği durumunda gelişir."},
            {"text": "Her aşırı östrojen seviyesi endometrial hiperplaziye neden olabilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Endometriumda preneoplastik abartılı proliferasyona (hiperplazi) yol açan primer hormonal mekanizma hangisidir?", [
            {"key": "A", "text": "Progesteron seviyesine göre rölatif östrojen fazlalığı", "isCorrect": True, "explanation": "Ders notunda açıkça: 'progesteron seviyesine göre rölatif östrojen fazlalığı belirgin olarak veya uzun süre endometriumu etkilerse hiperplazi meydana gelir' denmektedir."},
            {"key": "B", "text": "Aşırı insülin eksikliği ve kan şekeri düşüklüğü", "isCorrect": False, "explanation": "Metabolik durumdur."},
            {"key": "C", "text": "Sadece prolaktin hormonu fazlalığı", "isCorrect": False, "explanation": "Laktasyonla ilgilidir."},
            {"key": "D", "text": "Kalsiyum emiliminin tamamen durması", "isCorrect": False, "explanation": "Kemik metabolizmasıdır."}
        ])
    ]
    slides.append(make_slide(61, "Endometrial Hiperplazi Tanımı ve Rölatif Östrojen Fazlalığı", "Karşılanmamış proliferasyon, rölatif östrojen fazlalığı ve preneoplastik abartılı büyüme", "Patofizyoloji", s61_narrative, s61_bullets, s61_elements))

    # Slide 62: Yapısal ve Sitolojik Sınıflama (Basit/Kompleks, Atipisiz/Atipili)
    s62_narrative = (
        "Endometrial hiperplazi sınıflaması, lezyonun yapısal mimarisi ve hücre çekirdeğindeki atipi durumuna göre iki basamaklı olarak yapılır.\n\n"
        "- **Sınıflama Ekseni:** Yapısal değişiklikler ve sitolojik atipi göz önüne alınarak sınıflanır: "
        "**yapısal olarak basit-kompleks, sitolojik olarak atipisiz-atipili** olarak ayrılır.\n"
        "- **Yapısal Boyut (Basit vs Kompleks):** Basit hiperplazide bezler kistik dilate fakat aralarında "
        "stroma mevcuttur; kompleks hiperplazide bezler ileri derecede kalabalıklaşmış, sırt sırta vermiş "
        "ve aradaki stroma belirgin azalmıştır.\n"
        "- **Sitolojik Boyut (Atipisiz vs Atipili):** Atipisiz grupta nükleuslar normal polaritesini korur; "
        "atipili hiperplazide nükleer yuvarlaklaşma, pleomorfizm, kaba kromatin ve belirgin nükleol izlenir.\n"
        "- **Kademeli İlerleme:** Aşırı östrojen seviyesi ve süresine bağlı olarak basitten komplekse "
        "ve atipisizden atipiliye uzanan bir spektrum mevcuttur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endometrial hiperplazi sınıflaması: yapısal olarak basit-kompleks; sitolojik olarak atipisiz-atipili olarak sınıflandırılır."
    )
    s62_bullets = [
        "Sınıflama: yapısal olarak basit-kompleks, sitolojik olarak atipisiz-atipili şeklindedir.",
        "Aşırı östrojen seviyesi ve süresine bağlı olarak basitten komplekse, atipisizden atipiliye uzanır.",
        "Yapısal mimari gland kalabalığını, sitolojik atipi ise malignite potansiyelini belirler."
    ]
    s62_elements = [
        make_cloze("Endometrial hiperplazi yapısal olarak basit-kompleks, sitolojik olarak atipisiz-atipili olarak sınıflandırılır.", "basit-kompleks", "Hiperplazinin yapısal mimari sınıflaması"),
        make_table("Endometrial Hiperplazi Sınıflama Matrisi", ["Sınıflama Ekseni", "Kategoriler", "Değerlendirilen Parametre"], [
            {"cells": [{"text": "Yapısal (Mimari)", "isMasked": False}, {"text": "Basit - Kompleks", "isMasked": True, "hint": "mimari iki kategori"}, {"text": "Gland/stroma oranı, bez kalabalığı ve sırt sırta verme"}]},
            {"cells": [{"text": "Sitolojik (Nükleer)", "isMasked": False}, {"text": "Atipisiz - Atipili", "isMasked": False}, {"text": "Nükleer pleomorfizm, polarite kaybı, nükleol", "isMasked": True, "hint": "hücre çekirdeği atipisi"}]}
        ]),
        make_chain("Hiperplazi İlerleme Spektrumu", [
            "1. Basit Atipisiz: Kistik genişlemiş bezler, bol stroma, normal nükleus.",
            "2. Kompleks Atipisiz: Sırt sırta bezler, azalmış stroma, normal nükleus.",
            "3. Basit Atipili: Kistik bezler, sitolojik nükleer atipi.",
            "4. Kompleks Atipili: Yoğun bez kalabalığı ve belirgin sitolojik atipi (en yüksek risk)."
        ]),
        make_recall("Endometrial hiperplazi yapısal ve sitolojik olarak hangi kategorilere ayrılarak sınıflandırılır?", "Yapısal olarak basit-kompleks; sitolojik olarak atipisiz-atipili olarak sınıflandırılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hiperplazi Sınıflaması", [
            {"text": "Yapısal olarak basit-kompleks olarak sınıflandırılır.", "isLie": False, "explanation": "Doğru. Mimari sınıflamadır."},
            {"text": "Sitolojik olarak atipisiz-atipili olarak sınıflandırılır.", "isLie": False, "explanation": "Doğru. Nükleer sınıflamadır."},
            {"text": "Endometrial hiperplazi sadece Grade 1-2-3-4-5 kemik iliği nekrozu olarak sınıflandırılır.", "isLie": True, "explanation": "Tuzak! Endometrial hiperplazi yapısal olarak basit-kompleks, sitolojik olarak atipisiz-atipili olarak sınıflandırılır."},
            {"text": "Aşırı östrojen seviyesi ve süresine bağlı basitten komplekse ilerleme olabilir.", "isLie": False, "explanation": "Doğru. Spektrum kuralıdır."}
        ]),
        make_quiz("Endometrial hiperplazinin yapısal ve sitolojik sınıflaması aşağıdakilerden hangisinde eksiksiz verilmiştir?", [
            {"key": "A", "text": "Yapısal olarak basit-kompleks; sitolojik olarak atipisiz-atipili", "isCorrect": True, "explanation": "Ders notunda kelimesi kelimesine: 'yapısal olarak basit-kompleks, sitolojik olarak atipisiz-atipili olarak sınıflandırılır' denmektedir."},
            {"key": "B", "text": "Yapısal olarak malign; sitolojik olarak metastatik", "isCorrect": False, "explanation": "Hiperplazi sınıflaması değildir."},
            {"key": "C", "text": "Yalnızca akut ve kronik olarak", "isCorrect": False, "explanation": "Enflamasyon sınıflamasıdır."},
            {"key": "D", "text": "Granülomatöz ve kazeifiye olarak", "isCorrect": False, "explanation": "Tüberküloz sınıflamasıdır."}
        ])
    ]
    slides.append(make_slide(62, "Yapısal ve Sitolojik Sınıflama (Basit/Kompleks, Atipisiz/Atipili)", "Mimari eksende basit-kompleks, nükleer eksende atipisiz-atipili sınıflama mimarisi", "Patoloji", s62_narrative, s62_bullets, s62_elements))

    # Slide 63: Otonom Proliferasyon ve Karsinoma Uzanım
    s63_narrative = (
        "Endometrial hiperplazi, zaman içinde hormonal kontrolden çıkarak klonal bir neoplaziye dönüşebilir.\n\n"
        "- **Hormon Bağımlılığı Kaybı:** Başlangıçta östrojenin varlığına bağımlı olan hiperplastik "
        "hücreler, edindikleri somatik mutasyonlar (örneğin PTEN inaktivasyonu) sonucu otonomi kazanır.\n"
        "- **Bağımsız Büyüme:** Zamanla hiperplazi, **östrojen varlığına gereksinim duymaksızın "
        "bağımsız olarak prolifere olmaya devam eder**.\n"
        "- **Karsinoma Uzanım:** Bu otonom hücresel klonlar çevre stromayı istila etme yeteneği "
        "kazanarak **karsinoma uzanabilir** (invaziv endometrioid adenokarsinom).\n"
        "- **Klinik Önem:** Hiperplazinin takipsiz bırakılması, hastanın geri dönüşümsüz bir karsinoma "
        "adım atmasına neden olabilir; özellikle atipili olgularda progestin tedavisi veya histerektomi şarttır.\n\n"
        "> [!NOTE]\n"
        "> Zamanla hiperplazi östrojen varlığına gereksinim duymaksızın bağımsız olarak prolifere olmaya devam eder ve karsinoma uzanabilir."
    )
    s63_bullets = [
        "Zamanla hiperplazi östrojen gereksinimi duymadan bağımsız prolifere olmaya başlar.",
        "Hormondan bağımsız hale gelen bu hücreler karsinoma uzanabilir.",
        "Somatik mutasyonların birikmesi klonal neoplastik dönüşümü tetikler."
    ]
    s63_elements = [
        make_cloze("Zamanla hiperplazi, östrojen varlığına gereksinim duymaksızın bağımsız olarak prolifere olmaya devam eder ve karsinoma uzanabilir.", "bağımsız olarak prolifere", "Hiperplazinin östrojensiz büyüme hali"),
        make_table("Hormon Bağımlılığından Otonomiye Geçiş", ["Evre", "Hormon Durumu", "Onkolojik Durum"], [
            {"cells": [{"text": "Erken Hiperplazi", "isMasked": False}, {"text": "Östrojen bağımlı", "isMasked": True, "hint": "hormon uyarısı şart"}, {"text": "Progestinle gerileyebilir"}]},
            {"cells": [{"text": "Geç / Otonom Hiperplazi", "isMasked": False}, {"text": "Östrojenden bağımsız prolifere olur", "isMasked": False}, {"text": "Karsinoma uzanabilir", "isMasked": True, "hint": "kanserleşme potansiyeli"}]}
        ]),
        make_chain("Otonom Karsinogenez Basamakları", [
            "1. Hormonal Başlangıç: Östrojen uyarısıyla hiperplazi başlar.",
            "2. Genetik Hasar: Hücrelerde PTEN ve diğer mutasyonlar birikir.",
            "3. Otonomlaşma: Hücreler östrojene ihtiyaç duymadan kendi kendine bölünür.",
            "4. İnvaziv Karsinom: Myometrial invazyon ve adenokarsinom tablosu oturur."
        ]),
        make_recall("Endometrial hiperplazinin zaman içinde hormonal kontrolden çıkarak karsinoma uzanmasındaki temel biyolojik değişim nedir?", "Östrojen varlığına gereksinim duymaksızın bağımsız olarak prolifere olmaya devam etmesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Otonom Proliferasyon", [
            {"text": "Hiperplazi zamanla östrojen gereksinimi olmadan bağımsız prolifere olabilir.", "isLie": False, "explanation": "Doğru. Otonomlaşmadır."},
            {"text": "Bu otonom proliferasyon karsinoma uzanabilir.", "isLie": False, "explanation": "Doğru. Neoplastik ilerlemedir."},
            {"text": "Hiperplastik hücreler zamanla tamamen yok olarak kendi kendine buharlaşır ve asla kanser olamaz.", "isLie": True, "explanation": "Tuzak! Hiperplazi tedavi edilmezse bağımsız çoğalmaya devam ederek karsinoma uzanabilir."},
            {"text": "Hücreler zamanla östrojen varlığına gereksinim duymayabilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."}
        ]),
        make_quiz("Endometrial hiperplazinin neoplastik transformasyonunda izlenen kritik süreç hangisidir?", [
            {"key": "A", "text": "Zamanla östrojen gereksinimi duymaksızın bağımsız prolifere olması ve karsinoma uzanabilmesi", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'zamanla hiperplazi, östrojen varlığına gereksinim duymaksızın bağımsız olarak prolifere olmaya devam eder ve karsinoma uzanabilir' denmektedir."},
            {"key": "B", "text": "Sadece tiroid bezine göç edip guatr yapması", "isCorrect": False, "explanation": "İlgisizdir."},
            {"key": "C", "text": "Hücrelerin kemik iliğinde pıhtılaşma faktörüne dönüşmesi", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."},
            {"key": "D", "text": "Hiperplazinin tümör baskılayıcı bir aşıya dönüşmesi", "isCorrect": False, "explanation": "Kanser öncülüdür."}
        ])
    ]
    slides.append(make_slide(63, "Otonom Proliferasyon ve Karsinoma Uzanım", "Östrojen bağımsızlığı, klonal otonom çoğalma ve karsinoma ilerleme mekanizması", "Onkoloji", s63_narrative, s63_bullets, s63_elements))

    # Slide 64: Karsinom Riski: Basit vs Atipili Hiperplazi (%20 Risk)
    s64_narrative = (
        "Endometrial hiperplazide tedavi ve takip stratejisini belirleyen en kritik unsur, sitolojik atipinin varlığıdır.\n\n"
        "- **Riski Belirleyen Faktör:** Karsinom gelişim riski, hiperplastik değişikliklerin şiddetine "
        "ve en çok **hücresel atipiye (sitolojik atipi)** bağlıdır.\n"
        "- **Basit Hiperplazide Risk:** Hücresel atipinin bulunmadığı **basit hiperplazide kanser "
        "gelişim riski kayda değer değildir (ihmal edilebilir düzeydedir)**.\n"
        "- **Atipili Hiperplazide Risk:** Buna karşılık sitolojik atipinin eşlik ettiği **atipili "
        "hiperplazide yaklaşık %20 oranında karsinom gelişim riski** bulunmaktadır.\n"
        "- **Gizli Karsinom Tehlikesi:** Hatta atipili hiperplazi nedeniyle histerektomi yapılan hastaların "
        "yaklaşık üçte birinde eşzamanlı gizli (senkron) invaziv endometrioid adenokarsinom saptanmaktadır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Basit hiperplazide kanser riski kayda değer değilken; atipili hiperplazide karsinom gelişim riski %20'dir."
    )
    s64_bullets = [
        "Karsinom riski hiperplastik değişikliklerin şiddetine ve hücresel atipiye bağlıdır.",
        "Basit hiperplazide kanser riski kayda değer değildir.",
        "Atipili hiperplazide %20 oranında karsinom gelişim riski bulunmaktadır."
    ]
    s64_elements = [
        make_cloze("Basit hiperplazide kanser riski kayda değer değilken atipili hiperplazide %20 oranında karsinom gelişim riski bulunmaktadır.", "%20 oranında", "Atipili hiperplazide karsinom gelişim riski"),
        make_table("Hiperplazi Tiplerine Göre Karsinom Riski", ["Hiperplazi Tipi", "Hücresel Atipi", "Karsinom Gelişim Riski"], [
            {"cells": [{"text": "Basit Hiperplazi (Atipisiz)", "isMasked": False}, {"text": "Yok", "isMasked": False}, {"text": "Kayda değer değil (ihmal edilebilir)", "isMasked": True, "hint": "önemsiz risk düzeyi"}]},
            {"cells": [{"text": "Atipili Hiperplazi", "isMasked": False}, {"text": "Belirgin sitolojik nükleer atipi var", "isMasked": True, "hint": "çekirdek anomalisi"}, {"text": "%20 oranında karsinom riski", "isMasked": True, "hint": "yüzde yirmi risk"}]}
        ]),
        make_chain("Risk Değerlendirme Algoritması", [
            "1. Biyopsi: Hiperplazi saptanan materyal yüksek büyütmede taranır.",
            "2. Atipi Analizi: Nükleer yuvarlaklaşma, nükleol ve polarite kaybı aranır.",
            "3. Atipi Yoksa: Basit atipisiz hiperplazi denir, risk kayda değer değildir.",
            "4. Atipi Varsa: Atipili hiperplazi teşhis edilir; %20 kanser riski nedeniyle cerrahi/yakın takip planlanır."
        ]),
        make_recall("Basit hiperplazide ve atipili hiperplazide karsinom gelişim riski oranları nasıldır?", "Basit hiperplazide kanser riski kayda değer değilken; atipili hiperplazide karsinom gelişim riski %20'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hiperplazi Karsinom Riski", [
            {"text": "Karsinom gelişim riski hücresel atipiye bağlıdır.", "isLie": False, "explanation": "Doğru. En kritik parametredir."},
            {"text": "Basit hiperplazide kanser riski kayda değer değildir.", "isLie": False, "explanation": "Doğru. İhmal edilebilir düzeydedir."},
            {"text": "Atipili hiperplazide karsinom riski tamamen sıfırdır, asla kanser gelişmez.", "isLie": True, "explanation": "Tuzak! Atipili hiperplazide karsinom gelişim riski tam %20'dir; en yüksek riskli gruptur."},
            {"text": "Atipili hiperplazide %20 oranında karsinom gelişim riski bulunmaktadır.", "isLie": False, "explanation": "Doğru. Ders notu oranıdır."}
        ]),
        make_quiz("Endometrial hiperplazide kanser gelişim riski basit ve atipili tipler için aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Basit hiperplazide risk kayda değer değilken; atipili hiperplazide risk %20'dir", "isCorrect": True, "explanation": "Ders notunda ve kutu uyarısında açıkça: 'basit hiperplazide kanser riski kayda değer değilken, atipili hiperplazide %20 oranında karsinom gelişim riski bulunmaktadır' denmektedir."},
            {"key": "B", "text": "Basit hiperplazide %100; atipili hiperplazide %0", "isCorrect": False, "explanation": "Tamamen ters ve yanlıştır."},
            {"key": "C", "text": "Her iki tipte de risk kesin olarak %99.9'dur", "isCorrect": False, "explanation": "Basit hiperplazide risk önemsizdir."},
            {"key": "D", "text": "Atipili hiperplazide risk sadece milyonda birdir", "isCorrect": False, "explanation": "Risk %20 gibi çok yüksek bir orandır."}
        ])
    ]
    slides.append(make_slide(64, "Karsinom Riski: Basit vs Atipili Hiperplazi (%20 Risk)", "Hücresel atipinin önemi, basit hiperplazide ihmal edilebilir risk ve atipili hiperplazide %20 karsinom riski", "Onkoloji ve Patoloji", s64_narrative, s64_bullets, s64_elements))

    # Slide 65: Menopozal Ovulasyon Yetmezliği ve Uzamış Steroidler
    s65_narrative = (
        "Endometrial hiperplazi tablosunu tetikleyen etiyolojik nedenlerin başında perimenopozal "
        "ovulasyon yetmezliği ve iatrojenik hormon uygulamaları gelir.\n\n"
        "- **Menopozal Ovulasyon Yetmezliği:** Menopoz geçiş döneminde izlenen ovulasyon yetmezliği, "
        "korpus luteum oluşumunu engelleyerek endometriumu karşılanmamış östrojene maruz bırakır.\n"
        "- **İatrojenik Östrojen Uygulaması:** Projestin ile dengelenmeyen uzamış ekzojen östrojen "
        "steroid uygulanması hiperplazinin en sık hekime bağlı (iatrojenik) nedenidir.\n"
        "- **Doku Cevabı:** Sürekli uyarım bezlerde kistik dilatasyona ve hücresel stratifikasyona yol açar.\n"
        "- **Dengelenme Zorunluluğu:** Ekzojen steroid tedavilerinde projestin kombinasyonu yapılmadığı "
        "taktirde hiperplazi kaçınılmaz hale gelir.\n\n"
        "> [!NOTE]\n"
        "> Hiperplazi nedenleri: menapozda ovulasyon yetmezliği ve projestin ile dengelenmeyen uzamış östrojen steroid uygulamasıdır."
    )
    s65_bullets = [
        "Menapoz döneminde izlenen ovulasyon yetmezliği hiperplaziye zemin hazırlar.",
        "Projestin ile dengelenmeyen uzamış östrojen steroid uygulaması önemli bir nedendir.",
        "Her iki durumda da progesteronsuz kalan endometriumda kontrolsüz çoğalma izlenir."
    ]
    s65_elements = [
        make_cloze("Menapoz döneminde izlenen ovulasyon yetmezliği ve projestin ile dengelenmeyen uzamış östrojen uygulaması hiperplazi nedenidir.", "ovulasyon yetmezliği", "Menopozda progesteronsuzluğa yol açan durum"),
        make_table("Hormonal Yetmezlik ve İatrojenik Nedenler", ["Etiyolojik Faktör", "Patofizyolojik Kusur", "Endometrial Sonuç"], [
            {"cells": [{"text": "Perimenopozal Anovulasyon", "isMasked": False}, {"text": "Ovulasyon yetmezliği, progesteron yokluğu", "isMasked": True, "hint": "yumurtlama olmaması"}, {"text": "Endojen östrojenle hiperplazi"}]},
            {"cells": [{"text": "Ekzojen Hormon Tedavisi", "isMasked": False}, {"text": "Projestinsiz tek başına östrojen alımı", "isMasked": False}, {"text": "İatrojenik hiperplazi ve karsinom riski", "isMasked": True, "hint": "ilaç kaynaklı doku uyarımı"}]}
        ]),
        make_chain("Ovulasyon Yetmezliği Hiperplazi Zinciri", [
            "1. Folikül Yaşlanması: Ovulasyon gerçekleşemez (ovulasyon yetmezliği).",
            "2. Progesteron Sıfırlanması: Luteal doku oluşmadığı için dengeleyici hormon salınamaz.",
            "3. Sürekli Östrojen: Granüloza veya periferik kaynaklı östrojen endometriumu aralıksız uyarır.",
            "4. Hiperplazi: Dokuda kontrolsüz bez çoğalması başlar."
        ]),
        make_recall("Endometrial hiperplaziye neden olabilen temel hormonal durumlardan ikisi nedir?", "Menopoz döneminde izlenen ovulasyon yetmezliği ve projestin ile dengelenmeyen uzamış östrojen steroid uygulanmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hiperplazi Etyolojisi", [
            {"text": "Menapoz döneminde izlenen ovulasyon yetmezliği hiperplazi nedenlerindendir.", "isLie": False, "explanation": "Doğru. Anovulatuar zemindir."},
            {"text": "Projestin ile dengelenmeyen uzamış östrojen steroid uygulanması hiperplazi yapabilir.", "isLie": False, "explanation": "Doğru. Ekzojen faktördür."},
            {"text": "Projestin eklenmesi hiperplazi riskini 1000 kat artırarak derhal rahim yırtılması yapar.", "isLie": True, "explanation": "Tuzak! Projestin koruyucudur; hiperplaziye neden olan durum projestin ile DENGELENMEYEN östrojendir."},
            {"text": "Her aşırı östrojen seviyesi endometrial hiperplaziye yol açabilir.", "isLie": False, "explanation": "Doğru. Temel ilkedir."}
        ]),
        make_quiz("Endometrial hiperplaziye yol açabilen etiyolojik durumlar arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Menapoz döneminde ovulasyon yetmezliği ve projestin ile dengelenmeyen östrojen uygulaması", "isCorrect": True, "explanation": "Ders notunda hiperplaziye neden olabilen durumlar arasında ilk sırada sayılmıştır."},
            {"key": "B", "text": "Yalnızca aşırı C vitamini tüketimi", "isCorrect": False, "explanation": "Vitaminlerin hiperplazi ile bağı yoktur."},
            {"key": "C", "text": "Böbrek taşlarının idrar kanalını tıkaması", "isCorrect": False, "explanation": "Ürolojik obstrüksiyondur."},
            {"key": "D", "text": "Kulak zarının delinmesi", "isCorrect": False, "explanation": "KBB patolojisidir."}
        ])
    ]
    slides.append(make_slide(65, "Menopozal Ovulasyon Yetmezliği ve Uzamış Steroidler", "Menopozal ovulasyon yetmezliği, dengelenmemiş ekzojen östrojen ve kontrolsüz proliferasyon", "Patofizyoloji", s65_narrative, s65_bullets, s65_elements))

    # Slide 66: Ovaryal Nedenler: Polikistik Over (PCOS) ve Kortikal Hiperplazi
    s66_narrative = (
        "Endometrial hiperplazinin endojen kaynakları arasında overin hormonal lezyonları çok önemli bir yer tutar.\n\n"
        "- **Polikistik Overler (PCOS):** Östrojen üreten **polikistik overler**, reprodüktif çağdaki genç kadınlarda "
        "endometrial hiperplazinin en sık endojen nedenidir.\n"
        "- **PCOS Mekanizması:** Kronik anovulasyon nedeniyle progesteron sentezlenemezken, çok sayıdaki "
        "kistik folikülden ve periferik aromatizasyondan sürekli östrojen salınır.\n"
        "- **Kortikal Stromal Hiperplazi:** Postmenopozal kadınlarda over korteksindeki stromanın "
        "hiperplazisi (**kortikal stromal hiperplazi**), androjen ve östrojen öncülleri sentezleyerek endometriumu uyarır.\n"
        "- **Uzun Süreli Maruziyet:** Bu durumlar genç yaşta bile atipili hiperplazi ve hatta endometrioid "
        "adenokarsinom gelişimine zemin hazırlayabilir.\n\n"
        "> [!NOTE]\n"
        "> Östrojen üreten polikistik overler ve kortikal stromal hiperplazi endometrial hiperplaziye neden olabilen önemli over lezyonlarıdır."
    )
    s66_bullets = [
        "Östrojen üreten polikistik overler (PCOS) hiperplaziye yol açabilir.",
        "Overin kortikal stromal hiperplazisi steroid öncülleri üreterek hiperplazi yapabilir.",
        "Her iki durumda da kronik karşılanmamış östrojen maruziyeti esastır."
    ]
    s66_elements = [
        make_cloze("Endometrial hiperplaziye neden olabilen durumlar arasında östrojen üreten polikistik overler ve kortikal stromal hiperplazi yer alır.", "polikistik overler", "PCOS olgularındaki kistik over lezyonu"),
        make_table("Ovaryal Hiperöstrojenik Durumlar", ["Ovaryal Lezyon", "Hasta Profili", "Hormonal Kusur"], [
            {"cells": [{"text": "Polikistik Over (PCOS)", "isMasked": False}, {"text": "Genç reprodüktif çağ", "isMasked": True, "hint": "üreme çağı kadını"}, {"text": "Kronik anovulasyon + sürekli östrojen"}]},
            {"cells": [{"text": "Kortikal Stromal Hiperplazi", "isMasked": False}, {"text": "İleri yaş / postmenopoz", "isMasked": False}, {"text": "Stromal steroidogenez artışı", "isMasked": True, "hint": "over korteksi kaynaklı hormon"}]}
        ]),
        make_chain("PCOS ve Hiperplazi Patogenezi", [
            "1. LH/FSH Dengesizliği: Folikül gelişimi durur, çok sayıda kist oluşur.",
            "2. Kronik Anovulasyon: Ovulasyon olmadığı için progesteron üretilemez.",
            "3. Sürekli Östrojen Desteği: Kistlerden sürekli östrojen üretilir.",
            "4. Endometrial Hiperplazi: Uterus mukozası kalınlaşarak hiperplaziye dönüşür."
        ]),
        make_recall("Endometrial hiperplaziye zemin hazırlayan iki önemli benign ovaryal patoloji nedir?", "Östrojen üreten polikistik overler (PCOS) ve kortikal stromal hiperplazidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: PCOS ve Kortikal Hiperplazi", [
            {"text": "Östrojen üreten polikistik overler hiperplaziye neden olabilir.", "isLie": False, "explanation": "Doğru. Endojen nedendir."},
            {"text": "Kortikal stromal hiperplazi hiperplaziye neden olabilen over lezyonlarındandır.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Polikistik over sendromunda overler tamamen östrojen üretimini durdurur ve endometrium kağıt gibi kurur.", "isLie": True, "explanation": "Tuzak! PCOS'ta sürekli östrojen üretimi ve kronik anovulasyon vardır; bu da endometrial hiperplaziye yol açar."},
            {"text": "Kronik anovulasyon progesteron eksikliğine yol açar.", "isLie": False, "explanation": "Doğru. Temel fizyopatolojidir."}
        ]),
        make_quiz("Genç kadınlarda kronik anovulasyon ve östrojen üretimi ile endometrial hiperplaziye yol açabilen over lezyonu hangisidir?", [
            {"key": "A", "text": "Östrojen üreten polikistik overler (PCOS)", "isCorrect": True, "explanation": "Ders notunda hiperplazi nedenleri arasında: 'östrojen üreten polikistik overler gibi over lezyonları; kortikal stromal hiperplazi' açıkça belirtilmiştir."},
            {"key": "B", "text": "Akut apandisit flegmonu", "isCorrect": False, "explanation": "Gastrointestinal tablodur."},
            {"key": "C", "text": "Overin pür kalsiyum taşı", "isCorrect": False, "explanation": "Tıbbi antite değildir."},
            {"key": "D", "text": "Saf testosteron salgılayan sertoli hücre tümörü", "isCorrect": False, "explanation": "Maskülinizasyon yapar, hiperöstrojenizm yapmaz."}
        ])
    ]
    slides.append(make_slide(66, "Ovaryal Nedenler: Polikistik Over (PCOS) ve Kortikal Hiperplazi", "PCOS zemininde anovulasyon, kortikal stromal hiperplazi ve kronik endojen östrojen", "Patofizyoloji", s66_narrative, s66_bullets, s66_elements))

    # Slide 67: Overin Granüloza-Teka Hücreli Tümörleri
    s67_narrative = (
        "Endometrial hiperplazinin neoplastik ovaryal kaynakları arasında seks kord-stromal tümörler ilk sırada gelir.\n\n"
        "- **Fonksiyonel Tümör:** **Overin granüloza-teka hücreli tümörü**, yüksek miktarlarda östrojen "
        "sentezleyen en prototipik fonksiyonel ovaryal neoplazidir.\n"
        "- **Endometrial Uyarım:** Tümör hücrelerinin otonom ve aşırı östrojen üretimi, endometriumda "
        "şiddetli ve kesintisiz bir proliferatif dalga yaratır.\n"
        "- **Hiperplazi ve Kanser Birlikteliği:** Granüloza-teka hücreli tümörü olan kadınların büyük "
        "bölümünde endometrial hiperplazi, yaklaşık %5-10'unda ise eşzamanlı endometrioid adenokarsinom saptanır.\n"
        "- **Her Yaşta Tehdit:** Postmenopozal kanama ile başvuran veya prepubertal dönemde yalancı "
        "erken ergenlik (pseudopuberte prekoks) gösteren olgularda mutlaka granüloza hücreli tümör araştırılmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Overin granüloza-teka hücreli tümörü östrojen salgılayarak endometrial hiperplazi ve adenokarsinoma yol açabilen önemli bir over tümörüdür."
    )
    s67_bullets = [
        "Overin granüloza-teka hücreli tümörü östrojen salgılayan fonksiyonel bir tümördür.",
        "Endometriumda hiperplazi ve endometrioid karsinom gelişimini tetikler.",
        "Postmenopozal kanama veya erken puberte tablosuyla prezente olabilir."
    ]
    s67_elements = [
        make_cloze("Endometrial hiperplaziye neden olabilen over tümörlerinin başında overin granüloza-teka hücreli tümörü gelir.", "granüloza-teka hücreli tümörü", "Östrojen salgılayan over tümörü"),
        make_table("Granüloza-Teka Tümörü ve Endometrium Etkileşimi", ["Parametre", "Tümör Özelliği", "Endometrial Yansıması"], [
            {"cells": [{"text": "Tümör Grubu", "isMasked": False}, {"text": "Seks kord-stromal tümör", "isMasked": False}, {"text": "Ovaryal kitle"}]},
            {"cells": [{"text": "Salgılanan Hormon", "isMasked": False}, {"text": "Yoğun östrojen salgısı", "isMasked": True, "hint": "dişilik hormonu fazlalığı"}, {"text": "Uterin hiperplazi ve kanama", "isMasked": True, "hint": "endometrium kalınlaşması"}]},
            {"cells": [{"text": "Klinik Görünüm", "isMasked": False}, {"text": "Postmenopozal kanama / erken puberte", "isMasked": False}, {"text": "Senkron hiperplazi / adenokarsinom"}]}
        ]),
        make_chain("Granüloza Tümörü Etki Zinciri", [
            "1. Over Neoplazisi: Overde granüloza-teka hücreli tümör gelişir.",
            "2. Otonom Östrojen Sentezi: Tümör kanda östrojen seviyesini aşırı yükseltir.",
            "3. Uterin Hedef: Yüksek östrojen endometriumu sürekli proliferasyona zorlar.",
            "4. Patoloji: Endometrial hiperplazi ve endometrioid kanser ortaya çıkar."
        ]),
        make_recall("Östrojen salgılayarak endometrial hiperplaziye ve adenokarsinoma zemin hazırlayan primer ovaryum tümörü hangisidir?", "Overin granüloza-teka hücreli tümörüdür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Granüloza-Teka Tümörü", [
            {"text": "Overin granüloza-teka hücreli tümörü hiperplaziye neden olabilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Bu tümör östrojen salgılayarak endometriumu uyarır.", "isLie": False, "explanation": "Doğru. Fonksiyonel niteliğidir."},
            {"text": "Granüloza-teka tümörü sadece erkek prostatında görülen benign bir kıkırdaktır.", "isLie": True, "explanation": "Tuzak! Granüloza-teka tümörü bir OVER tümörüdür ve östrojen salgılar."},
            {"text": "Postmenopozal kadınlarda kanamaya yol açabilir.", "isLie": False, "explanation": "Doğru. Klinik belirtisidir."}
        ]),
        make_quiz("Aşağıdaki over lezyonlarından hangisi östrojen üreterek endometrial hiperplazi gelişimine neden olur?", [
            {"key": "A", "text": "Overin granüloza-teka hücreli tümörü", "isCorrect": True, "explanation": "Ders notunda hiperplaziye neden olan durumlar arasında açıkça: 'overin granüloza-teka hücreli tümörü' belirtilmiştir."},
            {"key": "B", "text": "Dermoid kist (matür kistik teratom)", "isCorrect": False, "explanation": "Genellikle hormon üretmez."},
            {"key": "C", "text": "Fibrom (Meigs sendromu)", "isCorrect": False, "explanation": "Hormonal olarak inaktiftir."},
            {"key": "D", "text": "Basit folikül kisti yırtılması", "isCorrect": False, "explanation": "Kalıcı hiperöstrojenizm yapmaz."}
        ])
    ]
    slides.append(make_slide(67, "Overin Granüloza-Teka Hücreli Tümörleri", "Fonksiyonel seks kord tümörü, otonom östrojen sentezi ve endometrial hiperplazi/karsinom tetiklenmesi", "Onkoloji", s67_narrative, s67_bullets, s67_elements))

    # Slide 68: Obezite, Aromataz ve Periferik Östrojen Sentezi
    s68_narrative = (
        "Modern çağda endometrial hiperplazi ve Tip 1 endometrium kanserinin en yaygın nedeni obezitedir.\n\n"
        "- **Adipöz Doku ve Steroidler:** **Adipöz dokular östrojen için gerekli steroid öncüllerini "
        "içerdiği için obezite önemli bir risk faktörüdür**.\n"
        "- **Aromataz Aktivitesi:** Yağ dokusundaki stromal hücreler yüksek konsantrasyonda **aromataz "
        "enzimi** içerir; bu enzim adrenal kaynaklı androstenodionu östrona (E1) dönüştürür.\n"
        "- **Progesteronsuz Fazlalık:** Periferik yağ dokusunda sentezlenen bu östrojen, over döngüsünden "
        "bağımsız olduğu için progesteron tarafından dengelenemez (karşılanmamış hiperöstrojenizm).\n"
        "- **Vücut Kitle İndeksi:** Vücut ağırlığı arttıkça aromataz kapasitesi katlanır; bu durum "
        "özellikle postmenopozal obez kadınlarda hiperplazi ve karsinom riskini dramatik şekilde yükseltir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Adipöz dokular östrojen için gerekli steroid öncüllerini içerdiği ve aromataz taşıdığı için obezite önemli bir risk faktörüdür."
    )
    s68_bullets = [
        "Adipöz dokular östrojen için gerekli steroid öncüllerini içerir.",
        "Obezite endometrial hiperplazi için önemli bir bağımsız risk faktörüdür.",
        "Yağ dokusundaki aromataz enzimi androjenleri progesteronsuz östrojene dönüştürür."
    ]
    s68_elements = [
        make_cloze("Adipöz dokular östrojen için gerekli steroid öncüllerini içerdiği için obezite önemli bir risk faktörüdür.", "steroid öncüllerini", "Yağ dokusunda östrojen sentezi için bulunan moleküller"),
        make_table("Obezite ve Endometrial Risk Mekanizması", ["Aşama", "Biyokimyasal Olay", "Sonuç"], [
            {"cells": [{"text": "Yağ Dokusu Hacmi", "isMasked": False}, {"text": "Adipöz doku kitlesinde artış", "isMasked": True, "hint": "kilo fazlalığı"}, {"text": "Yüksek aromataz enzim rezervi"}]},
            {"cells": [{"text": "Periferik Dönüşüm", "isMasked": False}, {"text": "Androjenlerin östrojene çevrilmesi", "isMasked": False}, {"text": "Karşılanmamış kronik östrojen artışı", "isMasked": True, "hint": "progesteronsuz östrojen"}]},
            {"cells": [{"text": "Endometrial Etki", "isMasked": False}, {"text": "Sürekli glandüler stimülasyon", "isMasked": False}, {"text": "Hiperplazi ve endometrioid kanser"}]}
        ]),
        make_chain("Obeziteden Karsinoma Uzanan Yol", [
            "1. Adipöz Artışı: Yağ dokusu steroid öncüllerini depolar.",
            "2. Aromataz Çevrimi: Androjenler östrona (östrojen) dönüştürülür.",
            "3. Progesteron Dengesi Yok: Karşılanmamış periferik östrojen kana verilir.",
            "4. Endometrial Hiperplazi: Endometrium kalınlaşır ve neoplazi riski katlanır."
        ]),
        make_recall("Obezite neden endometrial hiperplazi ve kanser açısından çok önemli bir risk faktörüdür?", "Adipöz dokular östrojen için gerekli steroid öncüllerini içerdiği ve aromataz enzimiyle androjenleri östrojene dönüştürdüğü içindir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Obezite ve Östrojen", [
            {"text": "Adipöz dokular östrojen için gerekli steroid öncüllerini içerir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Obezite endometrial hiperplazi için önemli bir risk faktörüdür.", "isLie": False, "explanation": "Doğru. Kanıtlanmış risk faktörüdür."},
            {"text": "Obezite kadınlarda östrojen üretimini tamamen sıfırlar ve endometriumu kanserden mutlak korur.", "isLie": True, "explanation": "Tuzak! Obezite östrojen üretimini ARTIRIR; adipöz dokudaki aromataz nedeniyle hiperplazi ve kanser riskini belirgin şekilde yükseltir."},
            {"text": "Yağ dokusunda aromataz enzimiyle periferik östrojen sentezlenir.", "isLie": False, "explanation": "Doğru. Biyokimyasal mekanizmadır."}
        ]),
        make_quiz("Obezitenin endometrial hiperplazi ve karsinom gelişiminde önemli bir risk faktörü olmasının temel nedeni nedir?", [
            {"key": "A", "text": "Adipöz dokuların östrojen için gerekli steroid öncüllerini içermesi ve aromataz aktivitesi", "isCorrect": True, "explanation": "Ders notunda açıkça: 'adipöz dokular östrojen için gerekli steroid öncüllerini içerdiği için obezite önemli bir risk faktörüdür' denmektedir."},
            {"key": "B", "text": "Yağ dokusunun sadece tiroid hormonu depolaması", "isCorrect": False, "explanation": "Tiroid ile ilgisizdir."},
            {"key": "C", "text": "Obezitenin tüm genleri anında mutasyona uğratıp parçalaması", "isCorrect": False, "explanation": "Mekanizma hormonaldir."},
            {"key": "D", "text": "Uterus kaslarının yağlanarak tamamen erimesi", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."}
        ])
    ]
    slides.append(make_slide(68, "Obezite, Aromataz ve Periferik Östrojen Sentezi", "Adipöz doku öncülleri, aromataz enzimi, karşılanmamış periferik östrojen ve hiperplazi riski", "Patofizyoloji", s68_narrative, s68_bullets, s68_elements))

    # Slide 69: Endometrial Hiperplazide Ayırıcı Tanı ve Biyopsi Prensipleri
    s69_narrative = (
        "Endometrial hiperplazi tanısı, histopatolojik örneklemenin dikkatli incelenmesini ve ayırıcı tanı basamaklarının titizlikle uygulanmasını gerektirir.\n\n"
        "- **Biyopsi Endikasyonları:** Anormal uterin kanaması olan 45 yaş üstü tüm kadınlarda, "
        "35 yaş üstü yüksek riskli (obez, PCOS) hastalarda veya postmenopozal kanamalarda endometrial biyopsi şarttır.\n"
        "- **Ayırıcı Tanı Spektrumu:** Patolog biyopsi kesitinde hiperplaziyi; **düzensiz proliferatif "
        "endometrium, endometrial polip, kistik atrofi ve iyi diferansiye endometrioid adenokarsinom** "
        "ile kesin olarak ayırt etmelidir.\n"
        "- **Karsinom Sınırı (İnvazyon Kriterleri):** Kompleks atipili hiperplaziyi iyi diferansiye "
        "adenokarsinomdan ayıran en kritik bulgular; kribriform yapılar, konfluent glandlar ve stromal invazyondur.\n"
        "- **Tedavi Kararı:** Atipisiz hiperplazilerde progestin tedavisi yeterli olurken; atipili "
        "hiperplazide %20 kanser riski nedeniyle histerektomi öncelikli cerrahi seçenektir.\n\n"
        "> [!NOTE]\n"
        "> Hiperplazi; düzensiz proliferatif endometrium, polip ve adenokarsinom ile ayırt edilmelidir; atipili hiperplazide cerrahi düşünülmelidir."
    )
    s69_bullets = [
        "AUK ile başvuran riskli hastalarda endometrial biyopsi tanı için esastır.",
        "Ayırıcı tanı: düzensiz proliferatif endometrium, polip, kistik atrofi ve adenokarsinom.",
        "Atipili hiperplazide karsinom riski (%20) nedeniyle cerrahi eksizyon (histerektomi) ön plandadır."
    ]
    s69_elements = [
        make_cloze("Endometrial hiperplazinin ayırıcı tanısında düzensiz proliferatif endometrium, endometrial polip ve endometrioid adenokarsinom yer alır.", "endometrioid adenokarsinom", "Hiperplaziden ayırt edilmesi gereken malign tümör"),
        make_table("Hiperplazinin Ayırıcı Tanı Spektrumu", ["Antite", "Gland/Stroma Oranı", "Atipi / İnvazyon"], [
            {"cells": [{"text": "Düzensiz Proliferatif", "isMasked": False}, {"text": "Nispeten normal", "isMasked": True, "hint": "korunmuş stroma"}, {"text": "Atipi yok, invazyon yok"}]},
            {"cells": [{"text": "Basit Hiperplazi", "isMasked": False}, {"text": "Hafif-orta artmış (kistik bezler)", "isMasked": False}, {"text": "Atipisiz, invazyon yok"}]},
            {"cells": [{"text": "Atipili Hiperplazi", "isMasked": False}, {"text": "Belirgin artmış (sırt sırta)", "isMasked": False}, {"text": "Nükleer atipi var, invazyon yok", "isMasked": True, "hint": "hücresel atipi mevcudiyeti"}]},
            {"cells": [{"text": "Adenokarsinom", "isMasked": False}, {"text": "Stroma yok denecek kadar az", "isMasked": False}, {"text": "Stromal invazyon, kribriform patern"}]}
        ]),
        make_chain("Klinik Yönetim Algoritması", [
            "1. Endometrial Örnekleme: Pipelle veya küretajla doku alınır.",
            "2. Atipi Ayrımı: Patolog sitolojik nükleer atipiyi doğrular.",
            "3. Basit Atipisiz: Tıbbi progestin tedavisi uygulanır.",
            "4. Kompleks Atipili: %20 kanser riski nedeniyle histerektomi değerlendirilir."
        ]),
        make_recall("Endometrial hiperplazinin histopatolojik ayırıcı tanısında yer alan lezyonlar hangileridir?", "Düzensiz proliferatif endometrium, endometrial polip, kistik atrofi ve iyi diferansiye endometrioid adenokarsinomdur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Hiperplazi Ayırıcı Tanısı", [
            {"text": "Hiperplazi düzensiz proliferatif endometrium ile ayırt edilmelidir.", "isLie": False, "explanation": "Doğru. Bez-stroma oranıyla ayrılır."},
            {"text": "Endometrial polip ayırıcı tanıda yer alır.", "isLie": False, "explanation": "Doğru. Fibröz stroma ve kalın damarlarla ayrılır."},
            {"text": "Atipili hiperplazi saptandığında hiçbir tedavi yapılmaz ve hasta ömür boyu evine gönderilir.", "isLie": True, "explanation": "Tuzak! Atipili hiperplazide %20 karsinom riski vardır; progestin veya histerektomi ile agresif tedavi planlanır."},
            {"text": "İyi diferansiye adenokarsinomdan stromal invazyon kriterleri ile ayrılır.", "isLie": False, "explanation": "Doğru. Kanser ayrım kriteridir."}
        ]),
        make_quiz("Endometrial hiperplazi tanısında patoloğun en kritik ayırıcı tanıları arasında aşağıdakilerden hangisi yer alır?", [
            {"key": "A", "text": "Düzensiz proliferatif endometrium, endometrial polip ve iyi diferansiye adenokarsinom", "isCorrect": True, "explanation": "Ders notunda hiperplazinin düzensiz proliferasyon, polip ve karsinom ile ayırıcı tanısı açıkça vurgulanmıştır."},
            {"key": "B", "text": "Yalnızca karaciğer sirozu", "isCorrect": False, "explanation": "Karaciğer hastalığıdır."},
            {"key": "C", "text": "Beyin kanaması", "isCorrect": False, "explanation": "Nörolojik tablodur."},
            {"key": "D", "text": "Deri skuamöz hücreli karsinomu", "isCorrect": False, "explanation": "Cilt lezyonudur."}
        ])
    ]
    slides.append(make_slide(69, "Endometrial Hiperplazide Ayırıcı Tanı ve Biyopsi Prensipleri", "Düzensiz proliferasyon, polip ve karsinom ayrımı, invazyon kriterleri ve klinik yönetim", "Klinik Patoloji", s69_narrative, s69_bullets, s69_elements))

    # Slide 70: [TEKRAR SAYFASI - CHECKPOINT 7] Endometrial Hiperplazi Sınıflaması ve Karsinom Riski
    s70_narrative = (
        "Bu tekrar sayfasında 7. Bölüm boyunca işlediğimiz endometrial hiperplazi patogenezini, "
        "basit/kompleks ve atipisiz/atipili sınıflamasını, %20 kanser riskini ve PCOS/granüloza/obezite etiyolojilerini konsolide ediyoruz.\n\n"
        "- **Hormonal Neden:** Progesterona göre rölatif östrojen fazlalığı; zamanla östrojenden bağımsız "
        "otonom proliferasyona ve karsinoma uzanabilir.\n"
        "- **Sınıflama:** Yapısal olarak basit-kompleks; sitolojik olarak atipisiz-atipili.\n"
        "- **Karsinom Riski:** Basit hiperplazide kanser riski kayda değer değilken; atipili hiperplazide "
        "karsinom gelişim riski %20'dir.\n"
        "- **Etiyolojik Durumlar:** Menopozal ovulasyon yetmezliği; dengelenmemiş uzamış ekzojen östrojen; "
        "östrojen üreten polikistik overler (PCOS); kortikal stromal hiperplazi; overin granüloza-teka "
        "hücreli tümörü; steroid öncülleri ve aromataz içeren obezite.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Rölatif östrojen fazlalığı; Basit/Kompleks ve Atipisiz/Atipili; Basit hiperplazide risk ihmal edilebilir, Atipili hiperplazide risk %20; PCOS, granüloza tümörü ve obezite."
    )
    s70_bullets = [
        "Rölatif östrojen fazlalığı hiperplazi yapar; zamanla hormondan bağımsız karsinoma uzanabilir.",
        "Sınıflama: yapısal basit-kompleks, sitolojik atipisiz-atipili; atipili hiperplazide kanser riski %20'dir.",
        "Nedenler: anovulasyon, projestinsiz östrojen, PCOS, kortikal hiperplazi, granüloza tümörü, obezite."
    ]
    s70_elements = [
        make_cloze("Basit hiperplazide kanser riski kayda değer değilken atipili hiperplazide karsinom riski %20 olup obezite önemli bir risk faktörüdür.", "%20", "Atipili hiperplazideki kanser riski yüzdesi"),
        make_table("7. Bölüm Büyük Hiperplazi Konsolidasyon Tablosu", ["Hiperplazi Tipi / Risk", "Histopatolojik Nitelik", "Karsinom Riski / Etiyoloji"], [
            {"cells": [{"text": "Basit Hiperplazi", "isMasked": False}, {"text": "Kistik bezler, korunmuş stroma, atipisiz", "isMasked": True, "hint": "atipisiz basit bezler"}, {"text": "Risk kayda değer değil"}]},
            {"cells": [{"text": "Atipili Hiperplazi", "isMasked": False}, {"text": "Sitolojik nükleer atipi, polarite kaybı", "isMasked": False}, {"text": "%20 karsinom gelişim riski", "isMasked": True, "hint": "yüzde yirmi risk"}]},
            {"cells": [{"text": "Ovaryal Tümör", "isMasked": False}, {"text": "Granüloza-teka hücreli tümör", "isMasked": True, "hint": "östrojenik over tümörü"}, {"text": "Aşırı östrojen salgısı"}]},
            {"cells": [{"text": "Obezite Zemin", "isMasked": False}, {"text": "Adipöz dokuda aromataz enzimi", "isMasked": False}, {"text": "Steroid öncüllerinden östrojen sentezi"}]}
        ]),
        make_chain("Bölüm 7 Süreç Konsolidasyonu", [
            "1. Tetikleyiciler: PCOS, menopozal anovulasyon, granüloza tümörü veya obezite östrojen üretir.",
            "2. Abartılı Proliferasyon: Progesteronsuz östrojen endometrial hiperplazi başlatır.",
            "3. Sınıflama: Yapısal (basit/kompleks) ve sitolojik (atipisiz/atipili) sınıflanır.",
            "4. Kanser Eşiği: Atipisiz grupta risk yokken, atipili hiperplazide risk %20'ye fırlar."
        ]),
        make_recall("7. Bölümün altın bilgileri: Atipili hiperplazide karsinom riski nedir ve hiperplazi yapan 3 önemli etiyolojik faktör hangileridir?", "Atipili hiperplazide karsinom riski %20'dir; etiyolojik faktörler ise PCOS, overin granüloza-teka tümörü ve obezitedir (adipöz aromataz)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 7. Bölüm Konsolidasyonu", [
            {"text": "Basit hiperplazide kanser riski kayda değer değildir.", "isLie": False, "explanation": "Doğru. İhmal edilebilir."},
            {"text": "Atipili hiperplazide %20 oranında karsinom gelişim riski bulunmaktadır.", "isLie": False, "explanation": "Doğru. Kritik onkolojik risk."},
            {"text": "Overin granüloza-teka hücreli tümörü endometrial hiperplaziyi %100 iyileştiren koruyucu bir vitamindir.", "isLie": True, "explanation": "Tuzak! Granüloza-teka hücreli tümör östrojen salgılayarak endometrial hiperplazi ve karsinom gelişimine yol açan neoplastik bir nedendir."},
            {"text": "Adipöz dokular östrojen öncüllerini içerdiği için obezite önemli bir risk faktörüdür.", "isLie": False, "explanation": "Doğru. Metabolik risk faktörüdür."}
        ]),
        make_quiz("Endometrial hiperplazinin karsinom riski ve etiyolojik nedenleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Atipili hiperplazide karsinom riski %20'dir; PCOS, granüloza tümörü ve obezite etiyolojide yer alır", "isCorrect": True, "explanation": "Ders notunun tüm temel verilerini eksiksiz ve doğru olarak özetleyen seçenektir."},
            {"key": "B", "text": "Basit hiperplazide kanser riski %95 iken atipili hiperplazide sıfırdır", "isCorrect": False, "explanation": "Tam tersidir."},
            {"key": "C", "text": "Obezite östrojen üretimini tamamen durdurarak hiperplaziyi önler", "isCorrect": False, "explanation": "Obezite riski artırır."},
            {"key": "D", "text": "Hiperplazi sadece erkeklerde izlenen benign bir testis lezyonudur", "isCorrect": False, "explanation": "Endometrium lezyonudur."}
        ])
    ]
    slides.append(make_slide(70, "[TEKRAR SAYFASI - CHECKPOINT 7] Endometrial Hiperplazi Sınıflaması ve Karsinom Riski", "7. Bölümün konsolidasyonu: basit/kompleks, atipisiz/atipili, %20 karsinom riski, PCOS, granüloza tümörü ve obezite", "Bölüm Tekrarı", s70_narrative, s70_bullets, s70_elements))

    return slides
