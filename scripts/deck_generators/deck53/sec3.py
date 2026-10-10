# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec3():
    slides = []

    # Slide 21: Endometriumun Temel Histolojik Yapısı
    s21_narrative = (
        "Endometrium, uterus kavitesini döşeyen ve siklik hormonal uyarılara son derece duyarlı olan mukoza tabakasıdır.\n\n"
        "- **Epitel ve Bezler:** Endometrium, yüzey epiteli ile basit tübüler bezler içeren bir **lamina propria**dan oluşur.\n"
        "- **Hücre Tipi:** Bezleri ve lümen yüzeyini döşeyen epitel hücreleri **basit prizmatik (kolumnar)** karakterdedir.\n"
        "- **Lamina Propria:** Lamina proprianın bağ dokusu stroma olarak adlandırılır ve **fibroblastlardan oldukça zengindir**.\n"
        "- **Siklik Değişim:** Lamina proprianın selüler stroması içinde yer alan bezlerin şekilleri, "
        "çapları ve büyüklükleri **ovaryal siklusa bağlı olarak sürekli değişir**.\n\n"
        "> [!NOTE]\n"
        "> Endometrium basit prizmatik epitel, basit tübüler bezler ve fibroblasttan zengin lamina propriadan oluşur; bezlerin şekli siklusa göre değişir."
    )
    s21_bullets = [
        "Endometrium: epitel ile basit tübüler bezler içeren lamina propriadan oluşur.",
        "Epitel hücreleri basit prizmatiktir; lamina propria bağ dokusu fibroblastlardan zengindir.",
        "Selüler stroma içindeki bezlerin şekil ve büyüklükleri ovaryal siklusa bağlı olarak değişir."
    ]
    s21_elements = [
        make_cloze("Endometrium epitel hücreleri basit prizmatiktir ve lamina proprianın bağ dokusu fibroblastlardan zengindir.", "basit prizmatiktir", "Endometrium epitel hücre tipi"),
        make_table("Endometrium Histolojik Katmanları", ["Bileşen", "Hücresel Özellik", "Fonksiyonel Nitelik"], [
            {"cells": [{"text": "Yüzey ve Bez Epiteli", "isMasked": False}, {"text": "Basit prizmatik epitel", "isMasked": True, "hint": "tek katlı silindirik hücreler"}, {"text": "Sekresyon ve proliferasyon"}]},
            {"cells": [{"text": "Lamina Propria (Stroma)", "isMasked": False}, {"text": "Fibroblastlardan zengin bağ dokusu", "isMasked": False}, {"text": "Hormonlara duyarlı selüler matriks", "isMasked": True, "hint": "destek doku çatısı"}]},
            {"cells": [{"text": "Endometrial Bezler", "isMasked": False}, {"text": "Basit tübüler bezler", "isMasked": False}, {"text": "Ovaryal siklusa göre şekil değiştirir"}]}
        ]),
        make_chain("Endometrial Histolojik Katmanlaşma", [
            "1. Lümen Teması: Tek katlı basit prizmatik yüzey epiteli.",
            "2. Glandüler Yapı: Stromaya doğru uzanan basit tübüler bezler.",
            "3. Stroma Desteği: Fibroblastlardan zengin yoğun lamina propria.",
            "4. Siklik Değişim: Ovaryal hormonların etkisiyle bez şekillerinin yeniden modellenmesi."
        ]),
        make_recall("Endometriumu döşeyen epitel hücre tipi nedir ve lamina propria hangi hücrelerden zengindir?", "Epitel hücreleri basit prizmatiktir; lamina propria bağ dokusu fibroblastlardan zengindir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endometrium Histolojisi", [
            {"text": "Endometrium basit tübüler bezler içeren lamina propriadan oluşur.", "isLie": False, "explanation": "Doğru. Temel histolojik yapıdır."},
            {"text": "Endometrium epitel hücreleri basit prizmatiktir.", "isLie": False, "explanation": "Doğru. Hücre tipidir."},
            {"text": "Endometriumu döşeyen epitel keratinize çok katlı yassı epiteldir ve hiçbir bez içermez.", "isLie": True, "explanation": "Tuzak! Endometrium epitel hücreleri basit prizmatiktir ve basit tübüler bezler içerir; keratinize çok katlı epitel epidermiste bulunur."},
            {"text": "Bezlerin şekilleri ve büyüklükleri ovaryal siklusa bağlı olarak değişir.", "isLie": False, "explanation": "Doğru. Hormon duyarlılığıdır."}
        ]),
        make_quiz("Endometriumun normal histolojik yapısı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Epitel hücreleri basit prizmatiktir ve lamina propria fibroblastlardan zengindir", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'epitel hücreleri basit prizmatiktir; lamina proprianın bağ dokusu fibroblastlardan zengindir' denmektedir."},
            {"key": "B", "text": "Hiyalin kıkırdak ve osteositlerden oluşan avasküler bir kemik zarıdır", "isCorrect": False, "explanation": "Kemik dokusuyla ilgisi yoktur."},
            {"key": "C", "text": "Bezlerin şekil ve çapları tüm yaşam boyu hiç değişmeden sabit kalır", "isCorrect": False, "explanation": "Ovaryal siklusa göre sürekli değişir."},
            {"key": "D", "text": "Sadece çizgili iskelet kas liflerinden oluşur", "isCorrect": False, "explanation": "Endometrium müköz bir zardır, kas değildir."}
        ])
    ]
    slides.append(make_slide(21, "Endometriumun Temel Histolojik Yapısı", "Basit prizmatik epitel, basit tübüler bezler, lamina propria ve siklik bez değişimleri", "Histoloji", s21_narrative, s21_bullets, s21_elements))

    # Slide 22: Endometriumun İki Tabakası: Fonksiyonel vs Bazal Tabaka
    s22_narrative = (
        "Endometrium dikey eksende histolojik ve fizyolojik olarak iki temel tabakaya ayrılır.\n\n"
        "- **Fonksiyonel Tabaka (Stratum Functionale):** Lümen yüzeyine bakan yüzeyel tabakadır; "
        "her menstrüel siklus karşısında **menstruasyonla dökülen kısımdır**.\n"
        "- **Hormonal Duyarlılık:** Fonksiyonel tabaka östrojen ve progesteron dalgalanmalarına "
        "tam yanıt vererek proliferasyon, sekresyon ve iskemik dökülme evrelerini yaşar.\n"
        "- **Bazal Tabaka (Stratum Basale):** Myometriuma komşu derin tabakadır; menstrüel dökülmeden "
        "etkilenmez ve **menstruasyon sonu hemen çoğalarak yenilenmeyi sağlayan kısımdır**.\n"
        "- **Kök Hücre Rezervi:** Bazal tabakadaki bezlerin derin uçlarında yer alan kök hücreler, "
        "menstruasyon biter bitmez yüzeye doğru göç ederek yeni fonksiyonel tabakayı inşa eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Menstruasyonla dökülen tabaka fonksiyonel tabakadır; menstruasyon sonunda hızla çoğalarak dokuyu yenileyen tabaka ise bazal tabakadır."
    )
    s22_bullets = [
        "Endometrium iki tabakadan oluşur: fonksiyonel tabaka ve bazal tabaka.",
        "Fonksiyonel tabaka her menstrüel siklusta menstruasyonla dökülen kısımdır.",
        "Bazal tabaka dökülmez; menstruasyon sonu hemen çoğalarak yenilenmeyi sağlar."
    ]
    s22_elements = [
        make_cloze("Endometrium iki tabakadan oluşur: menstruasyonla dökülen fonksiyonel tabaka ile yenilenen kısmı olan bazal tabaka.", "fonksiyonel tabaka", "Menstruasyonla dökülen yüzeyel tabaka"),
        make_table("Endometrium Tabakalarının Karşılaştırması", ["Özellik", "Fonksiyonel Tabaka", "Bazal Tabaka"], [
            {"cells": [{"text": "Siklik Kanamada Durum", "isMasked": False}, {"text": "Menstruasyonla tamamen dökülür", "isMasked": True, "hint": "kanamayla atılan kısım"}, {"text": "Dökülmez, korunur"}]},
            {"cells": [{"text": "Rejenerasyon Görevi", "isMasked": False}, {"text": "Her ay yeniden inşa edilir", "isMasked": False}, {"text": "Çoğalarak fonksiyonel tabakayı yeniler", "isMasked": True, "hint": "rejenerasyonu sağlayan kaynak"}]},
            {"cells": [{"text": "Vasküler Beslenme", "isMasked": False}, {"text": "Spazma uğrayan spiral arterler", "isMasked": False}, {"text": "Sabit düz bazal arterler"}]}
        ]),
        make_chain("Endometrial Yenilenme Döngüsü", [
            "1. Menstruasyon Fazı: Fonksiyonel tabaka iskemik nekrozla dökülür.",
            "2. Bazal Korunma: Bazal tabaka hasarsız olarak yerinde kalır.",
            "3. Hücresel Göç: Bazal bez uçlarındaki hücreler mitozla çoğalır.",
            "4. Re-epitelizasyon: Yüzeye göç eden hücreler yeni fonksiyonel tabakayı oluşturur."
        ]),
        make_recall("Endometriumun menstruasyonla dökülen ve menstruasyon sonu yenilenmeyi sağlayan iki tabakası hangileridir?", "Menstruasyonla dökülen fonksiyonel tabaka (stratum functionale), çoğalarak yenilenmeyi sağlayan ise bazal tabakadır (stratum basale)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Fonksiyonel ve Bazal Tabaka", [
            {"text": "Fonksiyonel tabaka her menstrüel siklusta menstruasyonla dökülür.", "isLie": False, "explanation": "Doğru. Dökülen tabakadır."},
            {"text": "Bazal tabaka menstruasyon sonu hemen çoğalarak endometriumun yenilenmesini sağlar.", "isLie": False, "explanation": "Doğru. Kök hücre kaynağıdır."},
            {"text": "Menstruasyon sırasında bazal tabaka dökülürken fonksiyonel tabaka ömür boyu sabit kalır.", "isLie": True, "explanation": "Tuzak! Tam tersidir: fonksiyonel tabaka dökülür, bazal tabaka dökülmeyip yenilenmeyi sağlar."},
            {"text": "Endometrium histolojik olarak iki ana tabakadan oluşur.", "isLie": False, "explanation": "Doğru. Anatomik sınıflandırmadır."}
        ]),
        make_quiz("Menstrüel siklus sırasında dökülen tabaka ile bu dökülmenin ardından hızla çoğalarak endometriumu yenileyen tabaka hangisidir?", [
            {"key": "A", "text": "Dökülen: Fonksiyonel tabaka | Yenilenmeyi sağlayan: Bazal tabaka", "isCorrect": True, "explanation": "Ders notunda açıkça: 'menstruasyonla dökülen fonksiyonel tabaka ile menstruasyon sonu hemen çoğalarak yenilenen bazal tabaka' tanımlanmıştır."},
            {"key": "B", "text": "Dökülen: Bazal tabaka | Yenilenmeyi sağlayan: Myometrium", "isCorrect": False, "explanation": "Bazal tabaka dökülmez."},
            {"key": "C", "text": "Dökülen: Perimetrium | Yenilenmeyi sağlayan: Tuba uterina", "isCorrect": False, "explanation": "Perimetrium dış zardır."},
            {"key": "D", "text": "Dökülen: Myometrium | Yenilenmeyi sağlayan: Seröz zar", "isCorrect": False, "explanation": "Myometrium dökülmez."}
        ])
    ]
    slides.append(make_slide(22, "Endometriumun İki Tabakası: Fonksiyonel vs Bazal Tabaka", "Fonksiyonel tabakanın dökülmesi, bazal tabakanın korunması ve yenilenme mekanizması", "Histoloji", s22_narrative, s22_bullets, s22_elements))

    # Slide 23: Myometriumun Histolojik Mimarisi ve Kas Tabakaları
    s23_narrative = (
        "Myometrium, uterus duvarının en kalın tabakası olup doğum eylemi ve mekanik stabiliteden sorumlu düz kas kütlesidir.\n\n"
        "- **Doku Yapısı:** Bağ dokusu ile birbirinden ayrılmış yoğun düz kas liflerinin oluşturduğu, "
        "uterusun **en kalın tabakasıdır**.\n"
        "- **Yüzeyel ve Derin Kas Tabakası:** Myometriumun en yüzeyel (seroza altı) ve en derin (endometrium "
        "altı) kısımlarında kas lifleri **uterusun uzun eksenine paralel (longitudinal)** yerleşim gösterir.\n"
        "- **Orta Tabaka (Stratum Vasculare):** Orta kısımlarında geniş kan damarları içeren **oblik ve "
        "sirküler kas lifleri** bulunur; bu lifler kontraksiyon sırasında damarları boğarak hemostaz sağlar.\n"
        "- **Dış Örtü:** En dış tabakada ise peritonla kaplı bölgelerde **seroza** (bağ dokusu ve mezotelyum), "
        "retroperitoneal komşuluklarda ise **adventisya** (bağ dokusu) bulunur.\n\n"
        "> [!NOTE]\n"
        "> Myometrium en kalın tabakadır; yüzeyel ve derinde longitudinal kaslar, ortada geniş kan damarları içeren oblik-sirküler lifler bulunur."
    )
    s23_bullets = [
        "Myometrium düz kas liflerinin oluşturduğu uterusun en kalın tabakasıdır.",
        "En yüzeyel ve en derin kısımlarda kas lifleri uterusun uzun eksenine paraleldir.",
        "Orta kısımlarında geniş kan damarları içeren oblik-sirküler lifler yer alır; en dışta seroza veya adventisya vardır."
    ]
    s23_elements = [
        make_cloze("Myometriumun orta kısımlarında geniş kan damarları içeren oblik-sirküler kas lifleri vardır.", "oblik-sirküler kas lifleri", "Orta tabakadaki kas lifi yönelimi"),
        make_table("Myometrium Tabaka Mimarisi", ["Tabaka Bölgesi", "Kas Lifi Yönelimi", "İçerik Özelliği"], [
            {"cells": [{"text": "En Yüzeyel ve En Derin", "isMasked": False}, {"text": "Uzun eksene paralel (longitudinal)", "isMasked": True, "hint": "paralel yönelim"}, {"text": "Mekanik güç ve aksiyal direnç"}]},
            {"cells": [{"text": "Orta Kısım", "isMasked": False}, {"text": "Oblik-sirküler kas lifleri", "isMasked": False}, {"text": "Geniş kan damarları içerir", "isMasked": True, "hint": "vasküler zenginlik"}]},
            {"cells": [{"text": "En Dış Örtü", "isMasked": False}, {"text": "Seroza ya da adventisya", "isMasked": False}, {"text": "Mezotelyum ve bağ dokusu"}]}
        ]),
        make_chain("Uterus Duvar Katmanlaşması", [
            "1. Endometrium: Basit prizmatik epitel ve tübüler bezler.",
            "2. İç Myometrium: Uterus uzun eksenine paralel longitudinal düz kaslar.",
            "3. Orta Myometrium: Geniş kan damarları içeren oblik-sirküler kas demetleri.",
            "4. Dış Katman: Dış longitudinal kaslar ve en dışta seroza / adventisya."
        ]),
        make_recall("Myometriumun orta kısımlarında yer alan kas liflerinin yönelimi ve vasküler içeriği nasıldır?", "Orta kısımlarında geniş kan damarları içeren oblik-sirküler kas lifleri bulunur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Myometrium Yapısı", [
            {"text": "Myometrium uterusun en kalın tabakasıdır.", "isLie": False, "explanation": "Doğru. Duvarın ana kütlesidir."},
            {"text": "Yüzeyel ve en derin kısımlarda kas lifleri uterusun uzun eksenine paraleldir.", "isLie": False, "explanation": "Doğru. Longitudinal dizilimdir."},
            {"text": "Myometriumun hiçbir yerinde kan damarı bulunmaz ve orta tabaka tamamen kıkırdaktır.", "isLie": True, "explanation": "Tuzak! Myometriumun orta kısımlarında geniş kan damarları içeren oblik-sirküler kas lifleri yer alır."},
            {"text": "Uterusun en dışında ya seroza ya da adventisya bulunur.", "isLie": False, "explanation": "Doğru. Dış anatomik örtüdür."}
        ]),
        make_quiz("Myometriumun kas lifi organizasyonu ve vasküler yapısı ile ilgili hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Yüzeyel ve derinde uzun eksene paralel; orta kısımlarında geniş kan damarları içeren oblik-sirküler lifler bulunur", "isCorrect": True, "explanation": "Ders notunda myometrium kas tabakaları aynen bu anatomik detayla anlatılmıştır."},
            {"key": "B", "text": "Myometrium düz kastan değil, sadece kemik dokusundan oluşur", "isCorrect": False, "explanation": "Düz kas dokusudur."},
            {"key": "C", "text": "Tüm kas lifleri tek yönde transvers uzanır, damar içermez", "isCorrect": False, "explanation": "Farklı tabakalarda farklı yönelimler vardır."},
            {"key": "D", "text": "Uterusun en ince tabakasıdır, kalınlığı 0.1 mm'dir", "isCorrect": False, "explanation": "En kalın tabakadır."}
        ])
    ]
    slides.append(make_slide(23, "Myometriumun Histolojik Mimarisi ve Kas Tabakaları", "Düz kas organizasyonu, longitudinal lifler, damarlı oblik-sirküler tabaka ve seroza", "Histoloji", s23_narrative, s23_bullets, s23_elements))

    # Slide 24: Proliferatif (Foliküler) Faz (5-14. Günler)
    s24_narrative = (
        "Proliferatif faz, menstrüel dökülmenin tamamlanmasıyla başlayıp ovulasyona kadar devam eden dokusal rekonstrüksiyon evresidir.\n\n"
        "- **Zaman Aralığı:** Menstrüel siklusun **5 ile 14. günleri arasıdır**; overdeki foliküler faza tam karşılık gelir.\n"
        "- **Hormonal İtici Güç:** Overden artarak salgılanan östrojenin mitojenik etkisi altındadır.\n"
        "- **Hücresel Proliferasyon:** Bezler ve yüzey epitel hızla yenilenir; lamina propria stroması "
        "ve bezleri döşeyen epitel hücreleri **aktif mitozlarla çoğalır**.\n"
        "- **Ulaşılan Kalınlık:** Bezler başlangıçta dar, düz ve tübülerdir; bu fazın sonunda **endometrium "
        "2-3 mm kalınlığa** ulaşır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Proliferatif faz 5-14. günleri kapsar; aktif mitozlarla bez ve stroma çoğalır; faz sonunda endometrium 2-3 mm kalınlığa ulaşır."
    )
    s24_bullets = [
        "Proliferatif faz 5 ile 14. günler arasıdır; östrojen etkisiyle bezler ve yüzey epiteli yenilenir.",
        "Lamina propria ve epitel hücreleri aktif mitozlarla çoğalır.",
        "Bu fazın sonunda endometrium 2-3 mm kalınlığa ulaşır."
    ]
    s24_elements = [
        make_cloze("Proliferatif faz 5 ile 14. günler arasıdır ve bu faz sonunda endometrium 2-3 mm kalınlığa ulaşır.", "2-3 mm", "Proliferatif faz sonu endometrium kalınlığı"),
        make_table("Proliferatif Faz Morfolojik Kriterleri", ["Özellik", "Proliferatif Faz Durumu", "Klinik Önem"], [
            {"cells": [{"text": "Siklus Günleri", "isMasked": False}, {"text": "5 - 14. günler", "isMasked": True, "hint": "beş ila on dördüncü günler"}, {"text": "Foliküler faza eşlik eder"}]},
            {"cells": [{"text": "Mitoz Aktivitesi", "isMasked": False}, {"text": "Aktif mitozlar boldur", "isMasked": False}, {"text": "Hızlı doku büyümesi", "isMasked": True, "hint": "hücre bölünme hızı"}]},
            {"cells": [{"text": "Endometrium Kalınlığı", "isMasked": False}, {"text": "2-3 mm", "isMasked": False}, {"text": "Östrojenle ulaşılan ara kalınlık"}]}
        ]),
        make_chain("Proliferatif Büyüme Basamakları", [
            "1. Başlangıç (5. gün): Bazal tabaka hücreleri yüzeyi örter.",
            "2. Östrojen Uyarımı: Granüloza kaynaklı östrojen stroma ve epitele bağlanır.",
            "3. Aktif Mitoz: Lamina propria ve bez epitelinde yoğun mitotik figürler izlenir.",
            "4. 2-3 mm Kalınlık: 14. günde düz tübüler bezlerle endometrium 2-3 mm'ye ulaşır."
        ]),
        make_recall("Proliferatif faz hangi günler arasındadır ve faz sonunda endometrium kaç mm kalınlığa ulaşır?", "5 ile 14. günler arasındadır; faz sonunda endometrium 2-3 mm kalınlığa ulaşır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Proliferatif Faz", [
            {"text": "Proliferatif faz 5 ile 14. günler arasındadır.", "isLie": False, "explanation": "Doğru. Siklus günleridir."},
            {"text": "Epitel ve stroma hücreleri aktif mitozlarla çoğalır.", "isLie": False, "explanation": "Doğru. Proliferasyonun esası mitozdur."},
            {"text": "Proliferatif faz sonunda endometrium kalınlığı 25-30 mm'ye ulaşır.", "isLie": True, "explanation": "Tuzak! Proliferatif faz sonunda endometrium 2-3 mm kalınlığa ulaşır; 25-30 mm devasa patolojiktir."},
            {"text": "Bezler ve yüzey epiteli bu evrede hızla yenilenir.", "isLie": False, "explanation": "Doğru. Rejenerasyon dönemidir."}
        ]),
        make_quiz("Menstrüel siklusta proliferatif fazın gün aralığı ve faz sonunda ulaştığı endometrium kalınlığı hangisidir?", [
            {"key": "A", "text": "5-14. günler arasıdır ve endometrium 2-3 mm kalınlığa ulaşır", "isCorrect": True, "explanation": "Ders notunda açıkça: 'proliferatif faz 5 ile 14. günler arasıdır; bu faz sonunda endometrium 2-3 mm kalınlığa ulaşır' denmektedir."},
            {"key": "B", "text": "1-4. günler arasıdır ve kalınlık 10 mm'dir", "isCorrect": False, "explanation": "1-4. günler menstrüel fazdır."},
            {"key": "C", "text": "14-28. günler arasıdır ve kalınlık 50 mm'dir", "isCorrect": False, "explanation": "Bu sekretuar fazdır."},
            {"key": "D", "text": "Sadece 28. gündür ve kalınlık sıfırdır", "isCorrect": False, "explanation": "Tanıma aykırıdır."}
        ])
    ]
    slides.append(make_slide(24, "Proliferatif (Foliküler) Faz (5-14. Günler)", "5-14. günler arası, aktif mitozlar, dokusal yenilenme ve 2-3 mm kalınlık", "Histoloji", s24_narrative, s24_bullets, s24_elements))

    # Slide 25: Sekretuar Faz Başlangıcı ve Subnükleer Vakuolizasyon
    s25_narrative = (
        "Sekretuar (luteal) faz, ovulasyonun hemen ardından korpus luteumun faaliyete geçmesiyle başlar.\n\n"
        "- **Hormonal Değişim:** Proliferatif fazdaki östrojen baskınlığının yerini korpus luteumdan "
        "salgılanan **progesteron hakimiyeti** alır.\n"
        "- **Erken Histolojik Belirteç:** Sekretuar faza geçişin en erken, en güvenilir ve patognomonik "
        "morfolojik bulgusu, bez epitel hücrelerinde **subnükleer vakuolizasyon** oluşmasıdır.\n"
        "- **Glikojen Depolanması:** Nükleusun altında biriken bu vakuoller glikojenden zengin salgı öncülleridir.\n"
        "- **Mitozun Durması:** Progesteronun antiproliferatif etkisiyle mitotik aktivite hızla baskılanır; "
        "stromada ödem gelişir ve **mitoz nadir** hale gelir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Sekretuar fazın erken dönem histolojik kanıtı glandüler epitelde subnükleer vakuolizasyon oluşmasıdır; progesteron etkisiyle mitoz durur."
    )
    s25_bullets = [
        "Sekretuar faz ovulasyondan sonra başlar; korpus luteum progesteronunun etkisi altındadır.",
        "En erken histolojik bulgu bez epitelinde subnükleer vakuolizasyon oluşmasıdır.",
        "Stromada ödem gelişir, hücrelerde mitoz nadir hale gelir."
    ]
    s25_elements = [
        make_cloze("Sekretuar fazda bezler kıvrıntılı hal alır, uzamaya başlar ve subnükleer vakuolizasyon oluşur.", "subnükleer vakuolizasyon", "Sekretuar faz erken histolojik belirteci"),
        make_table("Sekretuar Faza Geçiş Bulguları", ["Histolojik Parametre", "Gözlenen Değişim", "Tanısal Değeri"], [
            {"cells": [{"text": "Bez Epiteli", "isMasked": False}, {"text": "Subnükleer vakuolizasyon", "isMasked": True, "hint": "çekirdek altı boşluklar"}, {"text": "Ovulasyonun kesin histolojik kanıtı"}]},
            {"cells": [{"text": "Stroma", "isMasked": False}, {"text": "Belirgin ödem gelişimi", "isMasked": False}, {"text": "Doku gevşemesi ve süngerimsi yapı", "isMasked": True, "hint": "sıvı birikimi"}]},
            {"cells": [{"text": "Mitotik Aktivite", "isMasked": False}, {"text": "Mitoz nadirdir (baskılanır)", "isMasked": False}, {"text": "Proliferasyonun sona ermesi"}]}
        ]),
        make_chain("Sekretuar Transformasyon Zinciri", [
            "1. Ovulasyon: 14. günde korpus luteum progesteron salgılamaya başlar.",
            "2. Progesteron Yanıtı: Bez epitelinde glikojen sentezi uyarılır.",
            "3. Subnükleer Vakuol: Glikojen nükleusun tabanında vakuol şeklinde birikir (16-17. gün).",
            "4. Stromal Ödem ve Mitoz Durması: Stromada sıvı toplanır, mitoz neredeyse kaybolur."
        ]),
        make_recall("Sekretuar fazın başlangıcında bez epitelinde görülen ve ovulasyonun kanıtı olan karakteristik erken histolojik bulgu nedir?", "Subnükleer vakuolizasyondur (bez epitelinde çekirdek altında vakuol oluşumu)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Subnükleer Vakuolizasyon", [
            {"text": "Sekretuar faz korpus luteumdan salgılanan progesteronun etkisi altındadır.", "isLie": False, "explanation": "Doğru. Ana hormondur."},
            {"text": "Bez epiteli hücrelerinde subnükleer vakuolizasyon oluşur.", "isLie": False, "explanation": "Doğru. Erken sekretuar bulgudur."},
            {"text": "Sekretuar fazda mitotik bölünmeler rekor kırarak proliferatif fazın 50 katına çıkar.", "isLie": True, "explanation": "Tuzak! Sekretuar fazda progesteron mitozu baskılar; stromada ödem oluşur ve mitoz nadirdir."},
            {"text": "Bezler uzamaya ve kıvrıntılı hal almaya başlar.", "isLie": False, "explanation": "Doğru. Morfolojik değişimdir."}
        ]),
        make_quiz("Sekretuar fazın erken döneminde endometrial bez epitelinde izlenen karakteristik histopatolojik bulgu hangisidir?", [
            {"key": "A", "text": "Subnükleer vakuolizasyon oluşumu ve mitozun nadirleşmesi", "isCorrect": True, "explanation": "Ders notunda erken sekretuar faz bulgusu olarak: 'bezler kıvrıntılı hal alır, uzamaya başlar, subnükleer vakuolizasyon oluşur; mitoz nadirdir' denmektedir."},
            {"key": "B", "text": "Masif skuamöz kornifikasyon ve keratin incileri", "isCorrect": False, "explanation": "Karsinom veya metaplazi bulgusudur."},
            {"key": "C", "text": "Aşırı mitotik patlama ve bezlerin tamamen kaybolması", "isCorrect": False, "explanation": "Mitoz durur."},
            {"key": "D", "text": "Tüm damarların kalsifiye olup taşlaşması", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."}
        ])
    ]
    slides.append(make_slide(25, "Sekretuar Faz Başlangıcı ve Subnükleer Vakuolizasyon", "Progesteron hakimiyeti, subnükleer vakuoller, stromal ödem ve mitozda azalma", "Histopatoloji", s25_narrative, s25_bullets, s25_elements))

    # Slide 26: İlerlemiş Sekretuar Faz, Spiral Arterler ve 5 mm Kalınlık
    s26_narrative = (
        "Sekretuar faz ilerledikçe endometrium glandüler mimari ve vasküler dallanma açısından zirve olgunluğuna ulaşır.\n\n"
        "- **Bezlerin Morfolojisi:** Faz ilerledikçe bezler daha da uzar, ileri derecede kıvrılır "
        "(testere dişi görünümü) ve epitel kolumnar (prizmatik) hal alır; lümen glikojenden zengin sekresyonla dolar.\n"
        "- **Spiral Arterlerin Uzaması:** Lamina propriadaki **spiral arterler uzayıp kıvrılarak "
        "endometriumun en yüzeyel kısımlarına kadar uzanır**.\n"
        "- **Pre-desidual Dönüşüm:** Fazın sonuna doğru spiral arterlerin etrafındaki stromal fibroblastlar "
        "sitoplazma kazanarak pre-desidual hücrelere farklılaşır.\n"
        "- **Maksimum Kalınlık:** Bu yoğun vaskülarizasyon ve bez hipertrofisi sonucunda **bu faz "
        "sonunda endometrium 5 mm kalınlığa** ulaşır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Spiral arterler uzayıp kıvrılarak yüzeye kadar uzanır; sekretuar faz sonunda endometrium tam 5 mm kalınlığa ulaşır."
    )
    s26_bullets = [
        "Faz ilerledikçe bezler uzar, kıvrılır, lümen sekresyonla dolar ve epitel kolumnar hal alır.",
        "Spiral arterler uzayıp kıvrılarak yüzeyel kısımlara kadar uzanır.",
        "Bu faz sonunda endometrium 5 mm kalınlığa ulaşır."
    ]
    s26_elements = [
        make_cloze("Spiral arterler uzayıp kıvrılarak yüzeyel kısımlara kadar uzanır ve bu faz sonunda endometrium 5 mm kalınlığa ulaşır.", "5 mm", "Sekretuar faz sonu endometrium kalınlığı"),
        make_table("Geç Sekretuar Fazın Ayırıcı Bulguları", ["Yapısal Unsur", "Morfolojik Özellik", "Fonksiyonel Amacı"], [
            {"cells": [{"text": "Endometrial Bezler", "isMasked": False}, {"text": "Uzar, kıvrılır, lümeni sekresyonla dolar", "isMasked": True, "hint": "kıvrıntılı bezler"}, {"text": "Embriyo için besin deposu"}]},
            {"cells": [{"text": "Spiral Arterler", "isMasked": False}, {"text": "Kıvrılarak yüzeyel tabakaya uzanır", "isMasked": False}, {"text": "Fonksiyonel tabakanın beslenmesi", "isMasked": True, "hint": "yüzeye kadar kan desteği"}]},
            {"cells": [{"text": "Toplam Kalınlık", "isMasked": False}, {"text": "5 mm", "isMasked": False}, {"text": "Maksimum endometrial kalınlık"}]}
        ]),
        make_chain("Geç Sekretuar Olgunlaşma Aşamaları", [
            "1. Bez Kıvrımlanması: Bezler ileri derecede kıvrılarak testere dişi halini alır.",
            "2. Apikal Sekresyon: Subnükleer vakuoller lümene boşaltılarak hücre tepesine geçer.",
            "3. Spiral Arterlerin Tırmanışı: Spiral arterler kıvrıla kıvrıla yüzeye tırmanır.",
            "4. 5 mm Kalınlık Zirvesi: Endometrium 5 mm ile en yüksek kalınlığına ulaşır."
        ]),
        make_recall("Sekretuar faz sonunda endometrium kaç mm kalınlığa ulaşır ve spiral arterlerde ne izlenir?", "Endometrium 5 mm kalınlığa ulaşır; spiral arterler uzayıp kıvrılarak yüzeyel kısımlara kadar uzanır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İlerlemiş Sekretuar Faz", [
            {"text": "Faz ilerledikçe bezler uzar, kıvrılır ve epitel kolumnar hal alır.", "isLie": False, "explanation": "Doğru. Tipik bez gelişimidir."},
            {"text": "Spiral arterler uzayıp kıvrılarak yüzeyel kısımlara kadar uzanır.", "isLie": False, "explanation": "Doğru. Vasküler adaptasyondur."},
            {"text": "Sekretuar faz sonunda endometrium küçülerek 0.1 mm'ye iner ve tüm damarlar yok olur.", "isLie": True, "explanation": "Tuzak! Sekretuar faz sonunda endometrium kalınlaşarak tam 5 mm kalınlığa ulaşır."},
            {"text": "Bez lümenleri glikojenden zengin sekresyonla doludur.", "isLie": False, "explanation": "Doğru. Sekretuar faz özelliğidir."}
        ]),
        make_quiz("Sekretuar fazın ilerleyen döneminde spiral arterlerin durumu ve faz sonunda ulaşılan endometrium kalınlığı hangisidir?", [
            {"key": "A", "text": "Spiral arterler uzayıp kıvrılarak yüzeye uzanır; endometrium 5 mm kalınlığa ulaşır", "isCorrect": True, "explanation": "Ders notunda açıkça: 'spiral arterler uzayıp kıvrılarak yüzeyel kısımlara kadar uzanır; bu faz sonunda endometrium 5 mm kalınlığa ulaşır' denmektedir."},
            {"key": "B", "text": "Spiral arterler tamamen erir; endometrium 1 mm'ye geriler", "isCorrect": False, "explanation": "Damarlar erimez, uzar ve kalınlık 5 mm olur."},
            {"key": "C", "text": "Hiçbir damar gelişmez; kalınlık 100 mm olur", "isCorrect": False, "explanation": "Damarlanma yoğundur ve 5 mm'dir."},
            {"key": "D", "text": "Sadece bazal arterler büyür ve kalınlık 2 mm'de donar", "isCorrect": False, "explanation": "2-3 mm proliferatif faz sonundadır."}
        ])
    ]
    slides.append(make_slide(26, "İlerlemiş Sekretuar Faz, Spiral Arterler ve 5 mm Kalınlık", "Kıvrıntılı bezler, yüzeye uzanan spiral arterler ve 5 mm'lik tepe kalınlık", "Histoloji", s26_narrative, s26_bullets, s26_elements))

    # Slide 27: Menstruasyon Fazı Patogenezi: Spiral Arter Vazokonstriksiyonu
    s27_narrative = (
        "Menstruasyon fazı, ovumun döllenmemesi durumunda korpus luteum desteğinin kesilmesiyle tetiklenen vasküler bir krizdir.\n\n"
        "- **Hormon Çöküşü:** Ovumun döllenmesi ve implantasyonu mümkün olmadığında korpus luteumun "
        "görevi azalır ve **kandaki progesteron ve östrojen düzeyleri hızla düşer**.\n"
        "- **Damar Duvarı Spazmı:** Steroid desteğinin çekilmesi sonucu yüzeye kadar uzanmış olan "
        "**spiral arterlerin duvarları şiddetle kasılır (vazokonstriksiyon)**.\n"
        "- **Kan Akışının Kesilmesi:** Spiral arter spazmı nedeniyle fonksiyonel tabakaya giden "
        "kan akışı tamamen engellenir.\n"
        "- **İskemik Faz:** Perfüzyonun durması, dakikalar ve saatler içinde dokuda hipoksi ve metabolik çöküşü başlatır.\n\n"
        "> [!NOTE]\n"
        "> Döllenme olmazsa korpus luteum geriler, progesteron-östrojen hızla düşer; spiral arterler kasılarak kan akışı engellenir."
    )
    s27_bullets = [
        "Döllenme ve implantasyon olmadığında korpus luteum geriler; östrojen ve progesteron hızla düşer.",
        "Spiral arterlerin duvarları kasılır (vazokonstriksiyon).",
        "Fonksiyonel tabakaya kan akışı engellenerek iskemi süreci başlatılır."
    ]
    s27_elements = [
        make_cloze("Kandaki progesteron ve östrojen düzeyleri hızla düşer; spiral arterlerin duvarları kasılır ve kan akışı engellenir.", "spiral arterlerin duvarları kasılır", "Hormon çekilmesine vasküler yanıt"),
        make_table("Menstrüel Vazokonstriksiyon Mekanizması", ["Aşama", "Fizyolojik Değişim", "Doku Sonucu"], [
            {"cells": [{"text": "Hormon Çekilmesi", "isMasked": False}, {"text": "Östrojen ve progesteron hızla düşer", "isMasked": True, "hint": "luteal desteğin bitişi"}, {"text": "Vasküler tonus kontrolü kaybolur"}]},
            {"cells": [{"text": "Arteriyel Kasılma", "isMasked": False}, {"text": "Spiral arter duvarları şiddetle kasılır", "isMasked": False}, {"text": "Kan akışı engellenir", "isMasked": True, "hint": "kanlanmanın kesilmesi"}]},
            {"cells": [{"text": "Doku Perfüzyonu", "isMasked": False}, {"text": "Fonksiyonel tabaka kansız kalır", "isMasked": False}, {"text": "Akut hipoksi ve iskemi"}]}
        ]),
        make_chain("Vasküler Spazm Zinciri", [
            "1. Döllenme Yokluğu: HCG desteği gelmez ve korpus luteum geriler.",
            "2. Ani Hormon Çöküşü: Plazma östrojen ve progesteronu taban yapar.",
            "3. Spiral Arter Spazmı: Damar düz kasları kasılarak lümeni kapatır.",
            "4. Perfüzyonun Durması: Fonksiyonel tabakaya giden kan akışı tamamen kesilir."
        ]),
        make_recall("Menstruasyon başlangıcında spiral arterlerin kasılmasını ve kan akışının engellenmesini tetikleyen endokrin olay nedir?", "Korpus luteumun görevinin azalmasıyla kandaki progesteron ve östrojen düzeylerinin hızla düşmesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Spiral Arter Spazmı", [
            {"text": "Döllenme olmazsa östrojen ve progesteron düzeyleri hızla düşer.", "isLie": False, "explanation": "Doğru. Hormon çekilmesidir."},
            {"text": "Spiral arterlerin duvarları kasılır ve kan akışı engellenir.", "isLie": False, "explanation": "Doğru. Vazokonstriksiyondur."},
            {"text": "Progesteron seviyesi tavana vurduğunda spiral arterler aniden yırtılarak tüm uterusu patlatır.", "isLie": True, "explanation": "Tuzak! Spiral arter spazmı progesteronun zirve yapmasıyla değil, progesteron ve östrojenin hızla DÜŞMESİ ile tetiklenir."},
            {"text": "Kan akışının kesilmesi fonksiyonel tabakada iskemiye yol açar.", "isLie": False, "explanation": "Doğru. Nekrozun öncüsüdür."}
        ]),
        make_quiz("Menstruasyon fazında kan akışının engellenmesine ve spiral arter duvarlarının kasılmasına neden olan olay nedir?", [
            {"key": "A", "text": "Korpus luteum görevinin azalması ile progesteron ve östrojen düzeylerinin hızla düşmesi", "isCorrect": True, "explanation": "Ders notunda açıkça: 'korpus luteumun görevi azalır ve kandaki progesteron ve östrojen düzeyleri hızla düşer; spiral arterlerin duvarları kasılır, kan akışı engellenir' denmektedir."},
            {"key": "B", "text": "FSH'ın 1 milyon üniteye çıkıp damarları dondurması", "isCorrect": False, "explanation": "Fizyolojik değildir."},
            {"key": "C", "text": "HCG'nin spiral damarları bizzat bağlaması", "isCorrect": False, "explanation": "Gebelikte HCG damarları kasmaz."},
            {"key": "D", "text": "Böbrekten renin salgılanmasının tamamen durması", "isCorrect": False, "explanation": "Uterin döngüyle doğrudan tetikleyici bağı yoktur."}
        ])
    ]
    slides.append(make_slide(27, "Menstruasyon Fazı Patogenezi: Spiral Arter Vazokonstriksiyonu", "Korpus luteum gerilemesi, hormon çekilmesi, spiral arter spazmı ve kan akışının kesilmesi", "Fizyopatoloji", s27_narrative, s27_bullets, s27_elements))

    # Slide 28: İskemi, Nekroz, Damar Yırtılması ve Menstrüel Kanama
    s28_narrative = (
        "Spiral arterlerin kasılmasıyla başlayan doku iskemisi, kaçınılmaz olarak nekroz ve damar yırtılmasıyla sonlanır.\n\n"
        "- **İskemi ve Nekroz:** Kan akışı engellenen spiral arter damar duvarlarında ve fonksiyonel "
        "tabaka dokusunda **iskemi ve nekroz oluşur**.\n"
        "- **Büzüşme ve Yırtılma:** Nekroze olan ve destrükte hale gelen büzüşmüş kan damarları, "
        "kısa süreli reperfüzyon basıncına dayanamayarak **yırtılır ve kanama başlar**.\n"
        "- **Doku Atılımı:** Fonksiyonel tabaka parçaları, lümendeki kan ve döllenmemiş yumurta ile "
        "birlikte menstrüel sıvı halinde dışarı atılır.\n"
        "- **Derin Sınır:** Bu nekrotik yıkım tam olarak fonksiyonel tabaka ile bazal tabaka arasındaki "
        "sınırda durur; bazal tabaka sağlam kalır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Damar duvarlarının ve fonksiyonel tabakanın nekrozu ile iskemi oluşur; büzüşmüş kan damarları yırtılır ve kanama başlar."
    )
    s28_bullets = [
        "Damar duvarlarının ve fonksiyonel tabakanın nekrozu ile iskemi oluşur.",
        "Büzüşmüş kan damarları yırtılır ve kanama başlar.",
        "Yıkım fonksiyonel tabakayla sınırlıdır; bazal tabaka korunur."
    ]
    s28_elements = [
        make_cloze("Daha sonra damar duvarlarının ve fonksiyonel tabakanın nekrozu ile iskemi oluşur; büzüşmüş kan damarları yırtılır ve kanama başlar.", "büzüşmüş kan damarları yırtılır", "Menstrüel kanamayı başlatan vasküler olay"),
        make_table("Nekroz ve Kanama Basamakları", ["Aşama", "Patolojik Süreç", "Klinik Yansıması"], [
            {"cells": [{"text": "İskemik Nekroz", "isMasked": False}, {"text": "Damar duvarları ve fonksiyonel tabaka nekrozu", "isMasked": True, "hint": "doku ölümü"}, {"text": "Dokusal bütünlüğün bozulması"}]},
            {"cells": [{"text": "Vasküler Yırtılma", "isMasked": False}, {"text": "Büzüşmüş kan damarları yırtılır", "isMasked": False}, {"text": "Menstrüel kanamanın başlaması", "isMasked": True, "hint": "vajinal kanama"}]},
            {"cells": [{"text": "Bazal Bütünlük", "isMasked": False}, {"text": "Bazal tabaka canlılığını korur", "isMasked": False}, {"text": "Yenilenme için zemin hazır kalır"}]}
        ]),
        make_chain("Kanamalı Dökülme Zinciri", [
            "1. Vazokonstriksiyon: Spiral damarlar kasılır.",
            "2. Nekroz: Damar duvarı ve fonksiyonel tabakada iskemi gelişir.",
            "3. Damar Yırtılması: Büzüşmüş nekrotik damarlar yırtılır.",
            "4. Kanama ve Atılım: Doku fragmanları kanamayla birlikte dışarı atılır."
        ]),
        make_recall("Menstruasyon fazında iskemik nekrozun ardından kanamayı doğrudan başlatan mikrovasküler olay nedir?", "Büzüşmüş kan damarlarının yırtılmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İskemik Nekroz ve Kanama", [
            {"text": "Damar duvarlarının ve fonksiyonel tabakanın nekrozu ile iskemi oluşur.", "isLie": False, "explanation": "Doğru. Doku nekrozudur."},
            {"text": "Büzüşmüş kan damarları yırtılır ve kanama başlar.", "isLie": False, "explanation": "Doğru. Kanamayı başlatan olaydır."},
            {"text": "Menstrüel kanama sırasında bazal tabaka da tamamen nekroze olup bir daha asla iyileşmez.", "isLie": True, "explanation": "Tuzak! Nekroz fonksiyonel tabaka ile sınırlıdır; bazal tabaka sağlam kalarak yenilenmeyi sağlar."},
            {"text": "Kanama döllenmemiş yumurta ve doku parçalarıyla beraber vajinadan atılır.", "isLie": False, "explanation": "Doğru. Menstrüel atılımdır."}
        ]),
        make_quiz("Menstruasyon fazında fonksiyonel tabaka nekrozunu takiben kanamanın başlamasına yol açan mekanizma nedir?", [
            {"key": "A", "text": "Damar duvarlarının ve fonksiyonel tabakanın nekrozu sonucu büzüşmüş kan damarlarının yırtılması", "isCorrect": True, "explanation": "Ders notunda harfiyen: 'damar duvarlarının ve fonksiyonel tabakanın nekrozu ile iskemi oluşur; büzüşmüş kan damarları yırtılır ve kanama başlar' denmektedir."},
            {"key": "B", "text": "Myometrium kas liflerinin kendiliğinden erimesi", "isCorrect": False, "explanation": "Kas erimez."},
            {"key": "C", "text": "Servikal kanalın tamamen tıkanıp patlaması", "isCorrect": False, "explanation": "Serviks açıktır."},
            {"key": "D", "text": "Endometrium epitelinin kemik dokusuna dönüşmesi", "isCorrect": False, "explanation": "Fizyolojiye aykırıdır."}
        ])
    ]
    slides.append(make_slide(28, "İskemi, Nekroz, Damar Yırtılması ve Menstrüel Kanama", "Fonksiyonel nekroz, büzüşmüş spiral arter yırtılması ve menstrüel kanamanın başlaması", "Fizyopatoloji", s28_narrative, s28_bullets, s28_elements))

    # Slide 29: Menstrual Safha Sonu ve Bazal Rejenerasyon
    s29_narrative = (
        "Menstruasyon fazının sona ermesiyle birlikte uterus hemen kendini onarma ve yeniden inşa sürecine geçer.\n\n"
        "- **Kök Hücre Lokasyonu:** Menstrual safhanın sonunda sağlam kalan **bazal tabakada bulunan "
        "endometrial bezlerin bazal uçlarındaki hücreler** hızla çoğalmaya başlar.\n"
        "- **Yüzeye Göç:** Bu hücreler çıplak kalmış stroma yüzeyine doğru göç ederek yüzey epitelini "
        "yeniden döşer (re-epitelizasyon).\n"
        "- **Proliferatif Faza Geçiş:** Bazal hücrelerin çoğalması ve yüzeye göçleri **proliferasyon "
        "fazını başlatır** ve yeni menstrüel döngü kesintisiz devam eder.\n"
        "- **Hormonal Sinyal:** Bu rejeneratif göç, yeni döngünün başında hipofizden salgılanan FSH'ın "
        "folikülleri uyarması ve östrojen üretmeye başlamasıyla senkronize ilerler.\n\n"
        "> [!NOTE]\n"
        "> Menstrual safhanın sonunda bazal bez uçlarındaki hücrelerin çoğalması ve yüzeye göçü proliferasyon fazını başlatır."
    )
    s29_bullets = [
        "Menstrual safhanın sonunda bazal tabakadaki bezlerin bazal uç hücreleri hızla çoğalır.",
        "Bu hücrelerin yüzeye göçleri yeni yüzey epitelini örter ve proliferasyon fazını başlatır.",
        "Döngü böylece bazal tabaka sayesinde kesintisiz devam eder."
    ]
    s29_elements = [
        make_cloze("Bazal tabakada bulunan endometrial bezlerin bazal uçlarındaki hücrelerin çoğalması ve onların yüzeye göçleri proliferasyon fazını başlatır.", "proliferasyon fazını başlatır", "Bazal göçün başlattığı yeni faz"),
        make_table("Endometrial Rejenerasyon Aşamaları", ["Aşama", "Hücresel Olay", "Sonuç"], [
            {"cells": [{"text": "Bazal Bez Uçları", "isMasked": False}, {"text": "Mitoz ile aktif çoğalma", "isMasked": True, "hint": "hücresel bölünme"}, {"text": "Yeni epitel hücresi rezervi"}]},
            {"cells": [{"text": "Yüzeye Göç", "isMasked": False}, {"text": "Çıplak stroma üzerine yayılma", "isMasked": False}, {"text": "Re-epitelizasyon ve lümen örtüsü", "isMasked": True, "hint": "yüzeyin örtülmesi"}]},
            {"cells": [{"text": "Faz Geçişi", "isMasked": False}, {"text": "Proliferatif faza adım atılması", "isMasked": False}, {"text": "Yeni siklusun büyüme evresi"}]}
        ]),
        make_chain("Yenilenme ve Döngü Sürekliliği Zinciri", [
            "1. Menstrual Dökülme Sonu: Fonksiyonel tabaka tamamen atılır.",
            "2. Bazal Aktivasyon: Bazal tabakadaki bez diplerinde mitoz başlar.",
            "3. Epitelyal Göç: Hücreler yukarı göç ederek yüzeyi hızla kapatır.",
            "4. Proliferatif Faz Başlangıcı: Yeni foliküler östrojen etkisiyle döngü yeniden başlar."
        ]),
        make_recall("Menstrual safhanın sonunda proliferasyon fazını başlatan hücresel olay nedir?", "Bazal tabakada bulunan endometrial bezlerin bazal uçlarındaki hücrelerin çoğalması ve onların yüzeye göçleridir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bazal Tabaka Rejenerasyonu", [
            {"text": "Menstrual safhanın sonunda bazal tabaka bez uçlarındaki hücreler çoğalır.", "isLie": False, "explanation": "Doğru. Rejenerasyon kaynağıdır."},
            {"text": "Hücrelerin yüzeye göçleri proliferasyon fazını başlatır.", "isLie": False, "explanation": "Doğru. Epitel yenilenmesidir."},
            {"text": "Menstrual safha bittiğinde yeni epitel overlerden fallop tüpüyle taşınan yabancı hücrelerce oluşturulur.", "isLie": True, "explanation": "Tuzak! Yeni epitel bizzat bazal tabakadaki bezlerin bazal uç hücrelerinin çoğalarak yüzeye göç etmesiyle oluşturulur."},
            {"text": "Bazal tabaka döngünün sürekliliğini temin eder.", "isLie": False, "explanation": "Doğru. Temel biyolojik görevdir."}
        ]),
        make_quiz("Menstrual safhanın sonunda proliferasyon fazını başlatan ve döngünün devamını sağlayan hücresel kaynak nedir?", [
            {"key": "A", "text": "Bazal tabakada bulunan endometrial bezlerin bazal uçlarındaki hücrelerin çoğalması ve yüzeye göçleri", "isCorrect": True, "explanation": "Ders notunda kelimesi kelimesine: 'bazal tabakada bulunan endometrial bezlerin bazal uçlarındaki hücrelerin çoğalması ve onların yüzeye göçleri proliferasyon fazını başlatır, döngü devam eder' denmektedir."},
            {"key": "B", "text": "Myometrium kas hücrelerinin yağ hücresine dönüşmesi", "isCorrect": False, "explanation": "Böyle bir dönüşüm yoktur."},
            {"key": "C", "text": "Akciğer alveol epitelinin uterusa göç etmesi", "isCorrect": False, "explanation": "Tıbbi olarak imkansızdır."},
            {"key": "D", "text": "Sadece peritoneal mezotelyum hücrelerinin dökülmesi", "isCorrect": False, "explanation": "Rejenerasyon bazal tabakadan olur."}
        ])
    ]
    slides.append(make_slide(29, "Menstrual Safha Sonu ve Bazal Rejenerasyon", "Bazal bez uçlarında mitoz, epitel hücrelerinin yüzeye göçü ve proliferasyon fazının başlaması", "Histoloji", s29_narrative, s29_bullets, s29_elements))

    # Slide 30: [TEKRAR SAYFASI - CHECKPOINT 3] Endometrium Histolojisi ve Faz Değişimleri
    s30_narrative = (
        "Bu tekrar sayfasında 3. Bölümde işlenen endometriumun histolojik yapısını, tabakalarını, "
        "myometrium mimarisini ve fazlar arası kalınlık/damarlanma değişimlerini konsolide ediyoruz.\n\n"
        "- **Histolojik Katmanlar:** Basit prizmatik epitel, basit tübüler bezler ve fibroblasttan zengin stroma; "
        "dökülen fonksiyonel tabaka ve yenilenmeyi sağlayan bazal tabaka.\n"
        "- **Myometrium:** Yüzeyel ve derinde longitudinal paralel lifler; ortada geniş kan damarları "
        "içeren oblik-sirküler kas lifleri; en dışta seroza veya adventisya.\n"
        "- **Fazlar ve Kalınlık:** Proliferatif fazda (5-14. gün) aktif mitoz ve 2-3 mm kalınlık; "
        "sekretuar fazda subnükleer vakuolizasyon, yüzeye uzanan spiral arterler ve 5 mm tepe kalınlık.\n"
        "- **Menstrual Yıkım ve Onarım:** Hormon çekilmesi → spiral arter kasılması → fonksiyonel nekroz → "
        "damar yırtılması ve kanama; bazal bez uçlarının yüzeye göçü ile yeni proliferasyonun başlaması.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM KONSOLİDASYONU] Fonksiyonel (dökülen) vs Bazal (yenileyen); Proliferatif (2-3 mm, mitoz) vs Sekretuar (5 mm, subnükleer vakuol, spiral arterler); İskemi, nekroz, damar yırtılması ve bazal re-epitelizasyon."
    )
    s30_bullets = [
        "Endometrium: fonksiyonel (dökülen) ve bazal (yenileyen) tabakalardan oluşur.",
        "Proliferatif fazda 2-3 mm; sekretuar fazda subnükleer vakuol, yüzeye uzanan spiral arterler ve 5 mm kalınlık izlenir.",
        "Hormon çekilmesiyle spiral arterler kasılır, iskemik nekrozla damarlar yırtılır; bazal tabaka çoğalarak yeni döngüyü başlatır."
    ]
    s30_elements = [
        make_cloze("Proliferatif faz sonunda endometrium 2-3 mm kalınlığa ulaşırken sekretuar faz sonunda 5 mm kalınlığa ulaşır.", "5 mm kalınlığa", "Sekretuar faz sonu tepe kalınlık"),
        make_table("3. Bölüm Büyük Histoloji ve Fazlar Tablosu", ["Faz / Yapı", "Morfolojik Kriter", "Kalınlık / Özellik"], [
            {"cells": [{"text": "Proliferatif Faz (5-14. gün)", "isMasked": False}, {"text": "Aktif mitozlar, bez ve stroma yenilenmesi", "isMasked": True, "hint": "mitotik çoğalma"}, {"text": "2-3 mm kalınlık"}]},
            {"cells": [{"text": "Sekretuar Faz", "isMasked": False}, {"text": "Subnükleer vakuol, kıvrıntılı spiral arterler", "isMasked": False}, {"text": "5 mm kalınlık", "isMasked": True, "hint": "beş milimetre"}]},
            {"cells": [{"text": "Menstruasyon Fazı", "isMasked": False}, {"text": "Spiral arter spazmı, iskemik nekroz, damar yırtılması", "isMasked": True, "hint": "damarsal yırtılma"}, {"text": "Fonksiyonel tabakanın dökülmesi"}]},
            {"cells": [{"text": "Bazal Tabaka", "isMasked": False}, {"text": "Dökülmez, bez dipleri yüzeye göç eder", "isMasked": False}, {"text": "Proliferasyonu yeniden başlatır", "isMasked": True, "hint": "yeni döngü başlangıcı"}]}
        ]),
        make_chain("Endometrial Biyolojik Döngü Özeti", [
            "1. Yenilenme (5-14. gün): Östrojenle bazal tabakadan 2-3 mm kalınlık inşa edilir.",
            "2. Farklılaşma: Progesteronla subnükleer vakuoller oluşur ve kalınlık 5 mm'ye çıkar.",
            "3. İskemik Çöküş: Hormon çekilmesiyle spiral damarlar kasılır, doku nekroze olur.",
            "4. Dökülme ve Başlangıç: Damarlar yırtılıp dökülür; bazal uçlar çoğalarak yeni fazı başlatır."
        ]),
        make_recall("3. Bölümün iki kritik kalınlık ölçütü: Proliferatif faz sonunda ve sekretuar faz sonunda endometrium kalınlığı kaçar mm'dir?", "Proliferatif faz sonunda 2-3 mm, sekretuar faz sonunda ise 5 mm'dir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: 3. Bölüm Konsolidasyonu", [
            {"text": "Proliferatif faz sonunda endometrium 2-3 mm kalınlığa ulaşır.", "isLie": False, "explanation": "Doğru. Proliferatif kalınlıktır."},
            {"text": "Sekretuar faz sonunda endometrium 5 mm kalınlığa ulaşır.", "isLie": False, "explanation": "Doğru. Sekretuar kalınlıktır."},
            {"text": "Menstruasyon fazında fonksiyonel tabaka sapasağlam kalırken tüm bazal tabaka cerrahi olarak dökülür.", "isLie": True, "explanation": "Tuzak! Dökülen tabaka fonksiyonel tabakadır; bazal tabaka dökülmez ve rejenerasyonu sağlar."},
            {"text": "Spiral arterler sekretuar fazda uzayıp kıvrılarak yüzeyel kısımlara kadar uzanır.", "isLie": False, "explanation": "Doğru. Vasküler özelliktir."}
        ]),
        make_quiz("Endometriumun siklik faz değişimleri ve histolojik kalınlıkları ile ilgili hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Proliferatif faz sonunda endometrium 15 mm, sekretuar faz sonunda 1 mm kalınlıktadır", "isCorrect": True, "explanation": "Yanlış! Proliferatif faz sonunda 2-3 mm, sekretuar faz sonunda ise 5 mm kalınlığa ulaşır."},
            {"key": "B", "text": "Sekretuar fazda bez epitelinde subnükleer vakuolizasyon izlenir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Myometriumun orta tabakasında geniş kan damarları içeren oblik-sirküler lifler bulunur", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Menstrual safha sonunda bazal bez uçlarının yüzeye göçü proliferatif fazı başlatır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(30, "[TEKRAR SAYFASI - CHECKPOINT 3] Endometrium Histolojisi ve Faz Değişimleri", "3. Bölümün konsolidasyonu: fonksiyonel/bazal tabaka, myometrium, 2-3 mm ve 5 mm kalınlıklar, nekroz ve rejenerasyon", "Bölüm Tekrarı", s30_narrative, s30_bullets, s30_elements))

    return slides
