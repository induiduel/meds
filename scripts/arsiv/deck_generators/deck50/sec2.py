import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec2():
    slides = []

    # Slide 11: Primer Sifiliz: Şankr (Ağrısız Sert Ülser)
    s11_narrative = (
        "Primer sifiliz, enfeksiyonun giriş kapısında Treponema pallidum'un lokal çoğalması sonucu "
        "ortaya çıkan kardinal deri ve mukoza lezyonudur.\n\n"
        "- **Zamanlama ve Başlangıç:** Bakterinin girişinden yaklaşık 3 hafta sonra (inkübasyon bitiminde) "
        "inokülasyon yerinde önce küçük, sert, kırmızımsı bir papül belirir.\n"
        "- **Şankr Morfolojisi:** Bu papül kısa sürede erozyona uğrayarak yuvarlak veya oval, "
        "tabanı sert (endüre), kenarları belirgin ve kalkık, temiz yüzeyli **ağrısız bir ülsere (şankr)** dönüşür.\n"
        "- **Yüksek Bulaştırıcılık:** Şankrın seröz eksüdası milyonlarca canlı ve hareketli spiroket içerir; "
        "bu nedenle lezyon ==son derece yüksek oranda bulaştırıcıdır==.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Primer sifilizin kardinal lezyonu şankrdır (ağrısız, sert tabanlı ülser); bol spiroket içerir ve son derece bulaştırıcıdır."
    )
    s11_bullets = [
        "İnkübasyondan ~3 hafta sonra inokülasyon yerinde şankr gelişir.",
        "Şankr sert tabanlı, temiz yüzeyli ve tamamen ağrısız bir ülserdir.",
        "Bol canlı spiroket içerdiğinden son derece bulaştırıcıdır."
    ]
    s11_elements = [
        make_cloze("Primer sifilizin kardinal lezyonu olan ağrısız ve sert tabanlı ülsere şankr adı verilir.", "şankr", "Primer sifilizin tipik sert ülser lezyonu"),
        make_table("Primer Şankrın Klinik Özellikleri", ["Klinik Özellik", "Morfolojik Karakter", "Sınav Notu"], [
            {"cells": [{"text": "Ağrı Durumu", "isMasked": False}, {"text": "Tamamen ağrısız ve hassasiyetsiz", "isMasked": True, "hint": "acı hissi bulunmayan yara"}, {"text": "Ağrılı şankroidden (H. ducreyi) en temel ayrım"}]},
            {"cells": [{"text": "Ülser Tabanı", "isMasked": False}, {"text": "Sert, kıkırdaksı endürasyon", "isMasked": False}, {"text": "Palpasyonda düğme hissi verir", "isMasked": True, "hint": "sert taban endürasyonu"}]},
            {"cells": [{"text": "Bulaştırıcılık", "isMasked": False}, {"text": "Son derece yüksek bulaştırıcılık", "isMasked": True, "hint": "aktif bulaşma potansiyeli"}, {"text": "Eksüdasında bol canlı spiroket bulunur"}]}
        ]),
        make_chain("Şankr Gelişim Basamakları", [
            "1. İnokülasyon Odağı: Genital mukozada spiroketler çoğalır.",
            "2. Papül Fazı: 3. haftada ağrısız kırmızı bir kabarıklık oluşur.",
            "3. Ülserleşme: Papülün merkezi açılarak temiz tabanlı krater halini alır.",
            "4. Endürasyon: Çevre dokuda lenfoplazmasitik birikimle kıkırdaksı sert taban oturur."
        ]),
        make_recall("Primer sifilizin kardinal lezyonu olan şankrın ağrı durumu ve bulaştırıcılık özelliği nasıldır?", "Şankr tamamen ağrısız bir ülserdir ve bol spiroket içerdiğinden son derece bulaştırıcıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Primer Şankr Özellikleri", [
            {"text": "Şankr primer sifilizin kardinal lezyonudur.", "isLie": False, "explanation": "Doğru. Primer dönemin temel bulgusudur."},
            {"text": "Şankr tipik olarak sert tabanlı ve ağrısızdır.", "isLie": False, "explanation": "Doğru. Ağrısız endüre ülserdir."},
            {"text": "Primer şankr içinde tek bir bakteri bile bulunmayan tamamen bulaşıcısız steril bir yaradır.", "isLie": True, "explanation": "Tuzak! Şankr milyonlarca canlı spiroket içerir ve son derece bulaştırıcıdır."},
            {"text": "Yaklaşık 3 haftalık kuluçka süresinden sonra gelişir.", "isLie": False, "explanation": "Doğru. Tipik gelişim süresidir."}
        ]),
        make_quiz("Primer sifiliz lezyonu olan şankr ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Ağrısız, sert tabanlı bir ülserdir ve son derece bulaştırıcıdır", "isCorrect": True, "explanation": "Şankr ağrısız, sert tabanlı ve yüksek oranda bulaştırıcı bir ülserdir."},
            {"key": "B", "text": "Şiddetli zonklayıcı ağrısı olan pürülan bir apsedir", "isCorrect": False, "explanation": "Ağrısız ve temiz tabanlıdır."},
            {"key": "C", "text": "Hiçbir zaman genital bölgede görülmeyen bir tırnak mantarıdır", "isCorrect": False, "explanation": "Mukokutanöz veneral lezyondur."},
            {"key": "D", "text": "Bulaştırıcılığı kesinlikle sıfırdır", "isCorrect": False, "explanation": "Son derece bulaştırıcıdır."}
        ])
    ]
    slides.append(make_slide(11, "Primer Sifiliz: Şankr (Ağrısız Sert Ülser)", "İnokülasyon odağı, ağrısız endüre ülser morfolojisi, yüksek bulaştırıcılık ve seröz eksüda", "Primer Sifiliz: Şankr", s11_narrative, s11_bullets, s11_elements))

    # Slide 12: Şankr Anatomik Yerleşimleri: Genital ve Ekstragenital
    s12_narrative = (
        "Primer sifiliz şankrı, Treponema pallidum'un konağa ilk temas ettiği ve mikrotravma yoluyla "
        "giriş yaptığı her anatomik lokalizasyonda gelişebilir.\n\n"
        "- **Erkekte Genital Yerleşim:** En sık glans penis, korona sulkusu, prepusyum ve penis gövdesinde yerleşir.\n"
        "- **Kadında Genital Yerleşim:** Labia majora, labia minora, klitoris ve en önemlisi **servikste veya "
        "vajina duvarında** yerleşebilir. Kadında iç genital yerleşim ağrısız olduğundan çoğu zaman fark edilmez "
        "ve tanı gecikir.\n"
        "- **Ekstragenital Yerleşim:** Olguların %5-10'unda dudaklar, dil, farenks mukozası, tonsiller, "
        "meme başı veya anorektal bölgede de tipik ağrısız şankr lezyonları gelişebilir.\n\n"
        "> [!NOTE]\n"
        "> Şankr genital bölgede yerleşebileceği gibi oral ve anorektal ekstragenital temas alanlarında da görülebilir; kadında servikal şankrlar sıklıkla fark edilmez."
    )
    s12_bullets = [
        "Erkekte en sık penis ve korona sulkusunda yerleşir.",
        "Kadında labia, vajen veya servikste yerleşir (fark edilmeyebilir).",
        "Dudak, oral kavite ve anüste ekstragenital şankrlar izlenebilir."
    ]
    s12_elements = [
        make_cloze("Kadınlarda şankr servikste veya vajina duvarında yerleştiğinde ağrısız olması nedeniyle sıklıkla fark edilmez.", "servikste", "İç genital yerleşim nedeniyle gözden kaçabilen anatomik bölge"),
        make_table("Şankrın Anatomik Dağılımı", ["Lokalizasyon Grubu", "En Sık Tutulan Bölgeler", "Klinik Özellik"], [
            {"cells": [{"text": "Erkek Genital", "isMasked": False}, {"text": "Glans penis, prepusyum, şaft", "isMasked": True, "hint": "erkek dış genital yapıları"}, {"text": "Hasta tarafından kolayca fark edilir"}]},
            {"cells": [{"text": "Kadın Genital", "isMasked": False}, {"text": "Labialar, vajen forniksi, serviks", "isMasked": False}, {"text": "Derin yerleşimde asemptomatik kalabilir", "isMasked": True, "hint": "iç genitalde gizli kalma"}]},
            {"cells": [{"text": "Ekstragenital", "isMasked": False}, {"text": "Dudak, dil, tonsil, anorektal", "isMasked": True, "hint": "ağız ve anüs bölgeleri"}, {"text": "Aft veya karsinomla karışabilir"}]}
        ]),
        make_chain("Anatomik Girişten Tanıya", [
            "1. Temas Alanı: Cinsel pratikte bakteri genital, oral veya anal mukozaya değer.",
            "2. Lokal Şankr: Temas eden noktada 3 hafta sonra sert papül ve ülser açılır.",
            "3. Görünürlük Farkı: Erkekte peniste barizken, kadında servikste gizli kalır.",
            "4. Tanı Gecikmesi: Görülmeyen şankrlar doğrudan sekonder evreye ilerler."
        ]),
        make_recall("Kadınlarda primer sifiliz şankrının erkeklere kıyasla daha sık gözden kaçmasının ve fark edilmemesinin anatomik nedeni nedir?", "Şankrın vajina duvarı veya serviks gibi iç genital organlarda yerleşmesi ve ağrısız olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Şankr Yerleşimleri", [
            {"text": "Şankr en sık dış genital organlarda yerleşir.", "isLie": False, "explanation": "Doğru. Tipik cinsel temas alanıdır."},
            {"text": "Kadında servikste yerleştiğinde fark edilmeyebilir.", "isLie": False, "explanation": "Doğru. Ağrısız iç genital lezyonudur."},
            {"text": "Sifiliz şankrı sadece kafa kemiğinin tam tepesinde saçların altında delik açar.", "isLie": True, "explanation": "Tuzak! Şankr cinsel temas mukozasında (genital, oral, anal) yerleşir; kafa kemiğiyle ilgisi yoktur."},
            {"text": "Dudak, dil ve anüste ekstragenital şankrlar görülebilir.", "isLie": False, "explanation": "Doğru. Ekstragenital lezyonlar tanımlanmıştır."}
        ]),
        make_quiz("Primer sifiliz şankrının kadınlarda sıklıkla fark edilmeyip tanının gecikmesine yol açan anatomik yerleşimi neresidir?", [
            {"key": "A", "text": "Serviks ve vajina duvarı", "isCorrect": True, "explanation": "Serviks ve vajinadaki şankrlar ağrısız olduğundan hasta tarafından görülemez."},
            {"key": "B", "text": "Burun ucu", "isCorrect": False, "explanation": "Görünür alandır."},
            {"key": "C", "text": "Alın bölgesi", "isCorrect": False, "explanation": "Göz önündedir."},
            {"key": "D", "text": "El parmak uçları", "isCorrect": False, "explanation": "Kolayca fark edilir."}
        ])
    ]
    slides.append(make_slide(12, "Şankr Anatomik Yerleşimleri: Genital ve Ekstragenital", "Glans penis, labia, servikal gizli şankr, oral/anorektal ekstragenital lezyonlar", "Topografik Tutulum", s12_narrative, s12_bullets, s12_elements))

    # Slide 13: Bölgesel Lenfadenopati (Ağrısız, Sert, Lastik Kıvamında)
    s13_narrative = (
        "Primer sifilizde inokülasyon yerindeki bakteriyel çoğalmayı takiben, spiroketlerin lokal lenfatik "
        "drenaj yollarını istila etmesiyle karakteristik bir lenf bezi tutulumu gelişir.\n\n"
        "- **Zamanlama:** Bölgesel lenfadenopati (LAP), primer şankrın ortaya çıkışından **yaklaşık 1 hafta sonra** belirir.\n"
        "- **LAP Morfolojisi:** Tutulan lenf bezleri büyür; tipik olarak **ağrısız, hassasiyetsiz, sert, "
        "hareketli ve lastik kıvamındadır**.\n"
        "- **Bilateralite ve Süpürasyon Yokluğu:** Genital şankrlarda genellikle bilateral inguinal lenf nodları tutulur; "
        "lenf bezleri birbirine yapışmaz ve bakteri piyojenik olmadığından **kesinlikle süpürasyon (apseleşme/akıntı) yapmaz**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Şankrdan yaklaşık 1 hafta sonra ağrısız, sert, lastik kıvamında bölgesel lenfadenopati gelişir; süpürasyon (apse) görülmez."
    )
    s13_bullets = [
        "Şankrdan ~1 hafta sonra bölgesel lenfadenopati gelişir.",
        "Lenf nodları ağrısız, sert, lastik kıvamında ve hareketlidir.",
        "Lenf bezlerinde süpürasyon (apseleşme/akıntı) kesinlikle olmaz."
    ]
    s13_elements = [
        make_cloze("Primer sifilizde şankrın ortaya çıkışından yaklaşık 1 hafta sonra ağrısız bölgesel lenfadenopati gelişir.", "1 hafta", "Şankr sonrası LAP gelişim süresi"),
        make_table("Primer Sifiliz Lenfadenopati Kriterleri", ["Özellik", "Primer Sifilizde Karakteri", "Ayırıcı Tanı"], [
            {"cells": [{"text": "Ağrı / Hassasiyet", "isMasked": False}, {"text": "Ağrısız ve hassasiyetsiz", "isMasked": True, "hint": "ağrı hissi bulunmaması"}, {"text": "Şankroidde (ağrılı) ayrımda kilit"}]},
            {"cells": [{"text": "Kıvam ve Fluktuasyon", "isMasked": False}, {"text": "Sert, lastik kıvamında, hareketli", "isMasked": False}, {"text": "Apseleşme ve fistülleşme YOKTUR", "isMasked": True, "hint": "süpürasyon yapmayan lenf nodu"}]}
        ]),
        make_chain("Lenfatik Drenaj Zinciri", [
            "1. Şankr Eksüdası: Spiroketler submukozal lenfatik kapillerlere sızar.",
            "2. İnguinal Göç: 1 hafta içinde bakteriler bölgesel inguinal lenf bezlerine akar.",
            "3. Foliküler Hiperplazi: Lenf nodu kapsülü gerilmeden sertleşerek lastik kıvamı alır.",
            "4. Ağrısız Şişlik: Kasıkta ağrısız lenf bezi paketleri palpe edilir."
        ]),
        make_recall("Primer sifilizde lenfadenopati şankrdan ne kadar süre sonra çıkar ve fizik muayenedeki temel özellikleri nelerdir?", "Şankrdan yaklaşık 1 hafta sonra çıkar; ağrısız, sert, lastik kıvamında, hareketlidir ve apseleşmez."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölgesel Lenfadenopati", [
            {"text": "Şankrdan yaklaşık 1 hafta sonra bölgesel LAP gelişir.", "isLie": False, "explanation": "Doğru. Tipik kronolojik aralıktır."},
            {"text": "Lenf bezleri ağrısız ve sert lastik kıvamındadır.", "isLie": False, "explanation": "Doğru. Klasik palpasyon bulgusudur."},
            {"text": "Sifiliz lenf bezleri patlayarak cilde litrelerce pürülan yeşil iltihap akıtır.", "isLie": True, "explanation": "Tuzak! Primer sifiliz LAP'ı kesinlikle süpürasyon (apse) ve akıntı yapmaz; sert ve ağrısız kalır."},
            {"text": "Genital lezyonlarda inguinal lenf nodları tutulur.", "isLie": False, "explanation": "Doğru. Bölgesel drenaj alanıdır."}
        ]),
        make_quiz("Primer sifilize eşlik eden bölgesel lenfadenopatinin (LAP) fizik muayenedeki karakteristik özellikleri hangisidir?", [
            {"key": "A", "text": "Ağrısız, sert, lastik kıvamında ve süpürasyonsuz (apsesiz)", "isCorrect": True, "explanation": "Primer LAP ağrısız, sert, lastik kıvamında ve apsesizdir."},
            {"key": "B", "text": "Aşırı ağrılı, fluktuasyon veren ve deriye fistülleşen apse", "isCorrect": False, "explanation": "Bu şankroid veya LGV bulgusudur."},
            {"key": "C", "text": "Taş sertliğinde kemikleşmiş kalsiyum kisti", "isCorrect": False, "explanation": "Kalsifiye değildir."},
            {"key": "D", "text": "Sadece kulak arkasında tek taraflı dev kitle", "isCorrect": False, "explanation": "Genital lezyonda inguinal tutulum olur."}
        ])
    ]
    slides.append(make_slide(13, "Bölgesel Lenfadenopati (Ağrısız, Sert, Lastik Kıvamında)", "Şankrdan 1 hafta sonra, ağrısız lastik kıvamı, süpürasyon yokluğu ve inguinal tutulum", "Klinik Muayene: Primer LAP", s13_narrative, s13_bullets, s13_elements))

    # Slide 14: Şankrın Doğal Seyri: Spontan İyileşme (Aldatıcı Sakinlik)
    s14_narrative = (
        "Primer sifilizin klinik seyrindeki en aldatıcı ve tanısal yanılgılara yol açan özellik, "
        "şankr lezyonunun hiçbir tedavi uygulanmasa dahi kendiliğinden iyileşmesidir.\n\n"
        "- **Spontan İyileşme Süresi:** Primer şankr, ortaya çıktıktan sonra genellikle **3 ila 6 hafta "
        "(yaklaşık 1 ay) içinde** tedavisiz olarak tamamen epitelize olur ve çoğu zaman iz bırakmadan kaybolur.\n"
        "- **Bölgesel LAP'ın Sebatı:** Şankr iyileştikten sonra kasıktaki ağrısız lenfadenopati haftalarca "
        "veya aylarca daha uzun süre sebat edebilir.\n"
        "- **Büyük Tehlike (Aldatıcı Şifa):** Hastalar yaranın kendi kendine kapanmasını 'hastalığın geçtiği "
        "ve iyileştikleri' şeklinde yorumlar. Oysa bakteri ölmemiş; damarlar yoluyla tüm vücuda yayılarak "
        "sekonder evreyi hazırlamaya başlamıştır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Primer şankr tedavi edilmese dahi yaklaşık 1 ay (3-6 hafta) içinde kendiliğinden iyileşir; bu aldatıcı iyileşme enfeksiyonun bittiği anlamına gelmez."
    )
    s14_bullets = [
        "Şankr tedavisiz kalsa bile ~1 ay (3-6 hafta) içinde kendiliğinden iyileşir.",
        "Bölgesel lenfadenopati şankrdan daha uzun süre sebat edebilir.",
        "Klinik iyileşme şifa değil, sekonder döneme geçiş hazırlığıdır."
    ]
    s14_elements = [
        make_cloze("Primer sifiliz şankrı tedavi edilmese dahi yaklaşık 1 ay içinde spontan olarak kendiliğinden iyileşir.", "1 ay", "Şankrın tedavisiz kendiliğinden kapanma süresi"),
        make_table("Şankrın Doğal Seyri ve Yanılgılar", ["Dönem", "Klinik Görünüm", "Biyolojik Gerçek"], [
            {"cells": [{"text": "1-3. Haftalar", "isMasked": False}, {"text": "Ağrısız endüre aktif ülser", "isMasked": True, "hint": "açıkta duran primer yara"}, {"text": "Yoğun lokal replikasyon ve spiroketemi"}]},
            {"cells": [{"text": "4-6. Haftalar", "isMasked": False}, {"text": "Ülserin tamamen kapanması (skarsız)", "isMasked": False}, {"text": "Aldatıcı şifa; bakteri tüm vücuda dağılmıştır", "isMasked": True, "hint": "iyileşme sanrısı ve sekonder hazırlık"}]}
        ]),
        make_chain("Aldatıcı İyileşme Süreci", [
            "1. Lokal İmmün Yanıt: CD4+ ve CD8+ hücreler şankr tabanında toplanır.",
            "2. Epitelizasyon: Lokal sitokinlerle ülser yüzeyi 1 ay içinde kapanır.",
            "3. Hastanın Yanılgısı: Hasta doktora gitmekten vazgeçer.",
            "4. Sekonder Fırtına: Kanda çoğalan spiroketler birkaç hafta sonra tüm cildi kaplar."
        ]),
        make_recall("Primer sifiliz şankrı tedavi edilmediğinde doğal seyri nasıldır ve bu durum klinik olarak ne anlama gelir?", "Yaklaşık 1 ay (3-6 hafta) içinde kendiliğinden iyileşir; bu durum şifa değil, bakterinin vücuda yayıldığı aldatıcı bir dönemdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Şankrın Doğal Seyri", [
            {"text": "Yaklaşık 1 ay içinde şankr tedavisiz de iyileşir.", "isLie": False, "explanation": "Doğru. Spontan iyileşme tipiktir."},
            {"text": "Bölgesel lenfadenopati daha uzun süre sebat edebilir.", "isLie": False, "explanation": "Doğru. LAP hemen kaybolmaz."},
            {"text": "Şankr kapandığı anda vücuttaki tüm bakteriler buharlaşıp hasta tamamen kurtulur.", "isLie": True, "explanation": "Tuzak! Şankr kapansa bile bakteri tüm organlara yayılmıştır; tedavi edilmezse sekonder sifiliz gelişir."},
            {"text": "Şankrın kendiliğinden geçmesi aldatıcı bir iyileşmedir.", "isLie": False, "explanation": "Doğru. Hastaları yanıltan kritik noktadır."}
        ]),
        make_quiz("Primer sifilizde şankr lezyonunun tedavi edilmediğindeki doğal seyri aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Yaklaşık 1 ay (3-6 hafta) içinde kendiliğinden iyileşir", "isCorrect": True, "explanation": "Şankr tedavisiz kalsa dahi 3-6 hafta içinde spontan iyileşir."},
            {"key": "B", "text": "Ömür boyu hiç durmadan büyüyerek 2 metre çapa ulaşır", "isCorrect": False, "explanation": "Böyle bir büyüme olmaz."},
            {"key": "C", "text": "İkinci gün kangrene dönüşüp bacağı çürütür", "isCorrect": False, "explanation": "Primer şankr selimce kapanır."},
            {"key": "D", "text": "Kemikleşerek boynuz halini alır", "isCorrect": False, "explanation": "Kemikleşmez, epitelize olur."}
        ])
    ]
    slides.append(make_slide(14, "Şankrın Doğal Seyri: Spontan İyileşme (Aldatıcı Sakinlik)", "Tedavisiz kapanma, 1 aylık pencere, LAP sebatı ve aldatıcı klinik iyileşme tuzağı", "Doğal Seyir: Spontan İyileşme", s14_narrative, s14_bullets, s14_elements))

    # Slide 15: Sekonder Sifilize Geçiş: Zamanlama (2-8 Hafta)
    s15_narrative = (
        "Sekonder sifiliz, şankr evresinde kan dolaşımına sızan Treponema pallidum spiroketlerinin "
        "tüm vücuda yayılarak organ ve dokularda yaygın immünolojik-inflamatuvar reaksiyonlar başlattığı dissemine evredir.\n\n"
        "- **Zamanlama:** Sekonder evre bulguları genellikle şankrın ortaya çıkışından **2 ila 8 hafta sonra** "
        "(bazen 24 haftaya kadar gecikebilir) patlak verir.\n"
        "- **Örtüşme (Overlap):** Olguların bir kısmında sekonder döküntüler başladığında primer şankr "
        "henüz tamamen kapanmamış olabilir; iki evre birbiriyle çakışabilir.\n"
        "- **Biyolojik Nitelik:** Sekonder evre bakteriyeminin zirve yaptığı, bağışıklık sistemiyle "
        "spiroketlerin kıyasıya savaştığı sistemik dissemine bir klinik tablodur.\n\n"
        "> [!NOTE]\n"
        "> Sekonder sifiliz şankr oluşumundan 2-8 hafta sonra ortaya çıkar; sistemik spiroketemi ve yaygın doku tutulumunu yansıtır."
    )
    s15_bullets = [
        "Şankr oluşumundan genellikle 2 ila 8 hafta sonra gelişir.",
        "Bazı olgularda ortaya çıkış 24 haftaya kadar uzayabilir.",
        "Primer şankr tamamen kapanmadan sekonder evre başlayabilir."
    ]
    s15_elements = [
        make_cloze("Sekonder sifiliz tablosu primer şankrın çıkışından genellikle 2 ila 8 hafta sonra başlar.", "2 ila 8 hafta", "Sekonder döneme geçiş için gereken süre aralığı"),
        make_table("Sekonder Sifilize Geçiş Zamanlaması", ["Parametre", "Tipik Süre", "Önemli Klinik Not"], [
            {"cells": [{"text": "Tipik Başlangıç", "isMasked": False}, {"text": "Şankrdan 2-8 hafta sonra", "isMasked": True, "hint": "klasik haftalık süre aralığı"}, {"text": "En sık karşılaşılan dissemine başlangıç"}]},
            {"cells": [{"text": "Uç Aralık", "isMasked": False}, {"text": "24 haftaya kadar uzayabilir", "isMasked": False}, {"text": "Aylar sonra gecikmiş prezentasyon", "isMasked": True, "hint": "uzamış kuluçka benzeri geçiş"}]}
        ]),
        make_chain("Sekonder Geçiş Dinamiği", [
            "1. Şankr Evresi: Giriş yerinde primer lezyon mevcuttur.",
            "2. Sessiz Hematojen Yayılım: Spiroketler kanda çoğalır.",
            "3. 2-8. Hafta Eşiği: İmmün kompleksler ve spiroketler kılcal damarları tıkar.",
            "4. Sekonder Patlama: Ciltte yaygın simetrik döküntüler ve sistemik bulgular başlar."
        ]),
        make_recall("Sekonder sifiliz tablosu primer şankr lezyonunun ortaya çıkışından ne kadar süre sonra gelişir?", "Genellikle şankrdan 2 ila 8 hafta sonra (bazen 24 haftaya kadar uzayabilir) gelişir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Sifilize Geçiş", [
            {"text": "Sekonder sifiliz şankrdan 2-8 hafta sonra gelişir.", "isLie": False, "explanation": "Doğru. Tipik kronolojik aralıktır."},
            {"text": "Süre bazen 24 haftaya kadar uzayabilir.", "isLie": False, "explanation": "Doğru. Gecikmiş vakalar olabilir."},
            {"text": "Sekonder sifiliz sadece 90 yıl sonra başlayan ve sadece saçları beyazlatan bir durumdur.", "isLie": True, "explanation": "Tuzak! Şankrdan 2-8 hafta sonra başlar ve yaygın kutanöz-sistemik bir tablodur."},
            {"text": "Şankr henüz iyileşmeden sekonder döküntüler başlayabilir.", "isLie": False, "explanation": "Doğru. Örtüşme (overlap) sık görülür."}
        ]),
        make_quiz("Sekonder sifiliz bulguları primer şankrın ortaya çıkışından ortalama ne kadar süre sonra görülmeye başlar?", [
            {"key": "A", "text": "Genellikle 2 ila 8 hafta sonra", "isCorrect": True, "explanation": "Sekonder evre şankrdan 2-8 hafta sonra ortaya çıkar."},
            {"key": "B", "text": "Tam olarak 50 yıl sonra", "isCorrect": False, "explanation": "Tersiyer dönem bile bu kadar sürmez."},
            {"key": "C", "text": "Temastan 10 saniye sonra", "isCorrect": False, "explanation": "İnkübasyon bile 3 haftadır."},
            {"key": "D", "text": "Hiçbir zaman ortaya çıkmaz", "isCorrect": False, "explanation": "Tedavisiz olgularda ortaya çıkar."}
        ])
    ]
    slides.append(make_slide(15, "Sekonder Sifilize Geçiş: Zamanlama (2-8 Hafta)", "2-8 haftalık pencere, 24 haftaya uzayabilen aralık, şankr ile örtüşme ve dissemine yayılım", "Kronolojik İlerleme", s15_narrative, s15_bullets, s15_elements))

    # Slide 16: Sekonder Sifilizin Tipik Cilt Lezyonları
    s16_narrative = (
        "Sekonder sifiliz, klinik tıpta 'büyük taklitçi' (great imitator) unvanını kazandıran son derece "
        "zengin ve polimorfik cilt döküntüleri ile karakterizedir.\n\n"
        "- **Döküntü Karakteri:** Tipik kutanöz lezyonlar **kaşıntısız, simetrik, bilateral ve yaygındır**. "
        "Kaşıntının bulunmaması sifilitik döküntüyü diğer alerjik veya viral döküntülerden ayıran en kritik klinik ipucudur.\n"
        "- **Morfolojik Yelpaze:** Maküler (roseol sifilitik), makülopapüler, papüler, püstüler veya pullu psoriatik "
        "(sedef benzeri) formlarda izlenebilir; vezikülobüllöz formlar erişkinde görülmez.\n"
        "- **Bulaştırıcılık:** Bu döküntüler canlı spiroketler barındırır; ancak lezyon bütünlüğü bozulmadığı sürece "
        "şankr kadar yüksek bulaştırıcı değildir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Sekonder sifilizin tipik cilt lezyonları kaşıntısız, simetrik, bilateral ve yaygındır; kaşıntı olmaması kilit ayırıcı tanı özelliğidir."
    )
    s16_bullets = [
        "Tipik cilt lezyonları kaşıntısız, simetrik, bilateral ve yaygındır.",
        "Maküler, makülopapüler, püstüler veya psoriatik formlar alabilir.",
        "Kaşıntının bulunmaması alerjik dermatozlardan ayrımda anahtardır."
    ]
    s16_elements = [
        make_cloze("Sekonder sifilizin tipik cilt döküntüleri alerjilerin aksine tamamen kaşıntısız karakterdedir.", "kaşıntısız", "Döküntünün en karakteristik semptomsuz özelliği"),
        make_table("Sekonder Sifiliz Döküntü Özellikleri", ["Klinik Kriter", "Sifilitik Özellik", "Ayırıcı Tanı İpucu"], [
            {"cells": [{"text": "Kaşıntı Hissi", "isMasked": False}, {"text": "Kaşıntısız (pruritus yok)", "isMasked": True, "hint": "kaşınmayan döküntü"}, {"text": "İlaç erüpsiyonu ve uyuzdan ayırır"}]},
            {"cells": [{"text": "Dağılım Patern", "isMasked": False}, {"text": "Simetrik, bilateral ve generalize", "isMasked": False}, {"text": "Gövde ve ekstremiteleri eşit tutar", "isMasked": True, "hint": "iki taraflı dengeli yayılım"}]}
        ]),
        make_chain("Döküntü Patogenez Zinciri", [
            "1. Dermal Emboli: Kanda dolaşan spiroketler kutanöz kapillerlere yerleşir.",
            "2. Perivaskülit: Endoteller şişer ve damar çevresinde plazma hücreleri birikir.",
            "3. Makülopapüler Erüpsiyon: Epidermiste hafif ödem ve hücresel infiltratla lezyon belirir.",
            "4. Kaşıntısız Seyir: Histamin salımı olmadığından hasta kaşıntı hissetmez."
        ]),
        make_recall("Sekonder sifilizin tipik cilt döküntülerinin en karakteristik dört klinik özelliği nedir?", "Kaşıntısız, simetrik, bilateral ve yaygın olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sekonder Cilt Lezyonları", [
            {"text": "Sekonder sifiliz lezyonları kaşıntısızdır.", "isLie": False, "explanation": "Doğru. Kaşıntı tipik olarak bulunmaz."},
            {"text": "Döküntüler simetrik, bilateral ve yaygındır.", "isLie": False, "explanation": "Doğru. Tipik dağılım paternidir."},
            {"text": "Sekonder sifiliz döküntüleri hastayı çılgına çeviren dayanılmaz bir kaşıntı krizidir.", "isLie": True, "explanation": "Tuzak! Sekonder sifiliz döküntüleri kesinlikle KAŞINTISIZDIR; bu ayırıcı tanıdaki en kilit kuraldır."},
            {"text": "Makülopapüler ve psoriatik lezyonlar şeklinde görülebilir.", "isLie": False, "explanation": "Doğru. Çok çeşitli formlarda olabilir."}
        ]),
        make_quiz("Sekonder sifilizde izlenen tipik cilt döküntülerinin en belirgin ayırıcı tanı özelliği aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Kaşıntısız, simetrik ve bilateral olması", "isCorrect": True, "explanation": "Sekonder sifiliz döküntüleri kaşıntısız, simetrik ve bilateraldir."},
            {"key": "B", "text": "Aşırı kaşıntılı ve tek taraflı olması", "isCorrect": False, "explanation": "Kaşıntısız ve iki taraflıdır."},
            {"key": "C", "text": "Yalnızca saç diplerinde kepek yapması", "isCorrect": False, "explanation": "Yaygın gövde ve ekstremite döküntüsüdür."},
            {"key": "D", "text": "Daima içi sarı iltihap dolu dev büllerle seyretmesi", "isCorrect": False, "explanation": "Erişkinde büllöz lezyon görülmez."}
        ])
    ]
    slides.append(make_slide(16, "Sekonder Sifilizin Tipik Cilt Lezyonları", "Kaşıntısız, simetrik, bilateral, makülopapüler erüpsiyonlar ve ayırıcı tanı ilkeleri", "Kutanöz Bulgular", s16_narrative, s16_bullets, s16_elements))

    # Slide 17: El İçi ve Ayak Tabanı Döküntülerinin Önemi
    s17_narrative = (
        "Dermatoloji ve enfeksiyon hastalıkları pratiğinde el içi (avuç içi) ve ayak tabanını tutan "
        "döküntüler son derece sınırlı sayıda hastalıkta görülür ve sifiliz için altın değerinde bir ipucudur.\n\n"
        "- **Avuç İçi ve Taban Tutulumu:** Sekonder sifilizde döküntüler sıklıkla **avuç içlerine (palmar) "
        "ve ayak tabanlarına (plantar)** yerleşir; bakır kırmızısı veya kahverengimsi makülopapüller şeklinde belirir.\n"
        "- **Biett Kolareti:** Papüllerin etrafında ince bir deskuamasyon halkası (Biett kolareti) görülebilir.\n"
        "- **Klinik Alarm Kuralı:** ==El ve ayak tabanı döküntülerinde sifiliz özellikle düşünülmelidir==. "
        "Genç veya orta yaşlı bir hastada avuç içinde kaşıntısız kırmızı-kahverengi lezyonlar görüldüğünde aksi "
        "kanıtlanana kadar sifiliz araştırılmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] El içi ve ayak tabanında döküntü görüldüğünde ilk akla gelmesi gereken hastalık sekonder sifilizdir; bu lokalizasyon patognomonik tanısal ipucudur."
    )
    s17_bullets = [
        "El içi (palmar) ve ayak tabanında (plantar) bakır kırmızısı papüller izlenir.",
        "El ve ayak tabanı tutulumunda sifiliz özellikle düşünülmelidir.",
        "Lezyonlar kaşıntısızdır ve çevresinde soyulma (Biett kolareti) olabilir."
    ]
    s17_elements = [
        make_cloze("Klinik pratikte kaşıntısız el içi ve ayak tabanı döküntülerinde akla ilk gelmesi gereken enfeksiyon sekonder sifilizdir.", "sekonder sifiliz", "Avuç içi ve ayak tabanı döküntüsü yapan klinik evre"),
        make_table("Palmar ve Plantar Tutulum Önemi", ["Lokalizasyon", "Morfolojik Renk / Yapı", "Tanısal Değeri"], [
            {"cells": [{"text": "Avuç İçi (Palmar)", "isMasked": False}, {"text": "Bakır kırmızısı makülopapüller", "isMasked": True, "hint": "kahverengi-kırmızımsı papül"}, {"text": "Aksi kanıtlanana kadar sifiliz şüphesi"}]},
            {"cells": [{"text": "Ayak Tabanı (Plantar)", "isMasked": False}, {"text": "Sert, soyulan keratotik plaklar", "isMasked": False}, {"text": "Nadir döküntü alanıdır, tanı koydurur", "isMasked": True, "hint": "yüksek özgüllüklü lokalizasyon"}]}
        ]),
        make_chain("Palmar Tutulum Tanı Zinciri", [
            "1. Spiroket İstilası: Bakteriler el ve ayak tabanı kapillerlerine oturur.",
            "2. Bakır Rengi Papüller: Avuç içinde kaşıntısız lezyonlar belirir.",
            "3. Hekim Muayenesi: Jinekolog/dermatolog el içindeki lezyonu görür.",
            "4. Seroloji İsteği: VDRL/TPHA istenerek gizli sifiliz derhal yakalanır."
        ]),
        make_recall("Dermatolojik muayenede el içi ve ayak tabanında kaşıntısız döküntü saptanan bir hastada öncelikle hangi hastalık düşünülmelidir?", "Sekonder sifiliz düşünülmelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: El ve Ayak Tabanı Döküntüsü", [
            {"text": "El ve ayak tabanı döküntülerinde sifiliz özellikle düşünülmelidir.", "isLie": False, "explanation": "Doğru. En kritik tanısal ipucudur."},
            {"text": "Lezyonlar bakır kırmızısı renginde ve kaşıntısızdır.", "isLie": False, "explanation": "Doğru. Tipik palmar-plantar morfolojidir."},
            {"text": "Sifiliz mikrobu el içine kesinlikle dokunamaz, el ayası sifilize doğuştan bağışıktır.", "isLie": True, "explanation": "Tuzak! Tam aksine el içi ve ayak tabanı sifilizin en tipik ve en ünlü tutulum yeridir."},
            {"text": "Lezyonların çevresinde ince soyulmalar (Biett kolareti) görülebilir.", "isLie": False, "explanation": "Doğru. Tipik deskuamasyon halkasıdır."}
        ]),
        make_quiz("Genç bir erişkinde avuç içi ve ayak tabanında kaşıntısız, bakır kırmızısı makülopapüler döküntüler saptandığında öncelikle hangisi düşünülmelidir?", [
            {"key": "A", "text": "Sekonder sifiliz", "isCorrect": True, "explanation": "El içi ve ayak tabanı döküntüsü sekonder sifilizin klasik bulgusudur."},
            {"key": "B", "text": "Güneş yanığı", "isCorrect": False, "explanation": "Avuç içi ve taban güneş görmez."},
            {"key": "C", "text": "Basit su çiçeği", "isCorrect": False, "explanation": "Kaşıntılı veziküller yapar."},
            {"key": "D", "text": "Hipertansiyon krizi", "isCorrect": False, "explanation": "Döküntü yapmaz."}
        ])
    ]
    slides.append(make_slide(17, "El İçi ve Ayak Tabanı Döküntülerinin Önemi", "Palmar/plantar erüpsiyon, bakır kırmızısı lezyonlar, Biett kolareti ve kilit alarm bulgusu", "Palmar-Plantar Lezyonlar", s17_narrative, s17_bullets, s17_elements))

    # Slide 18: Kondiloma Lata: Nemli Alanların Bulaştırıcı Plakları
    s18_narrative = (
        "Sekonder sifilizin en dramatik ve bulaştırıcılığı en yüksek mukokutanöz lezyonu "
        "**kondiloma lata (geniş kondilom)** olarak adlandırılan plak benzeri oluşumlardır.\n\n"
        "- **Anatomik Lokalizasyon:** Vücudun sıcak, nemli ve sürtünmeye maruz kalan deri kıvrımlarında; "
        "özellikle **vulva, skrotum, perine, perianal bölge, uyluk iç yüzü ve meme altında** yerleşir.\n"
        "- **Morfolojik Görünüm:** Geniş tabanlı, kabarık, yüzeyi düzleşmiş veya hafif verrüköz, "
        "masere, gri-beyaz veya pembe renkli **nemli plaklar ve nodüller** halindedir.\n"
        "- **Bulaştırıcılık Zirvesi:** HPV'nin yaptığı sivri uçlu siğillerden (kondiloma aküminata) farklı olarak "
        "kondiloma lata düz tepelidir ve ==içerisinde milyonlarca canlı spiroket barındırdığından son derece bulaştırıcıdır==.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Vulva, skrotum ve perine gibi nemli alanlarda gri-beyaz, geniş tabanlı, aşırı bulaştırıcı lezyonlara 'kondiloma lata' denir; sekonder sifiliz bulgusudur."
    )
    s18_bullets = [
        "Vulva, perine, skrotum gibi nemli kıvrımlarda gri-beyaz plaklardır.",
        "Kondiloma lata sekonder sifilizin kardinal lezyonudur.",
        "Bol miktarda spiroket içerir ve son derece yüksek bulaştırıcıdır."
    ]
    s18_elements = [
        make_cloze("Sekonder sifilizde nemli genital kıvrımlarda gelişen gri-beyaz bulaştırıcı plaklara kondiloma lata adı verilir.", "kondiloma lata", "Geniş tabanlı bulaştırıcı sifilitik lezyon"),
        make_table("Kondiloma Lata ve Kondiloma Aküminata Ayrımı", ["Özellik", "Kondiloma Lata (Sifiliz)", "Kondiloma Aküminata (HPV)"], [
            {"cells": [{"text": "Etken Mikroorganizma", "isMasked": False}, {"text": "Treponema pallidum (Bakteri)", "isMasked": True, "hint": "spiral spiroket etkeni"}, {"text": "HPV tip 6 ve 11 (Virüs)"}]},
            {"cells": [{"text": "Morfolojik Şekil", "isMasked": False}, {"text": "Geniş tabanlı, düz tepeli, nemli gri plak", "isMasked": False}, {"text": "Karnabahar benzeri, saplı, sivri siğil", "isMasked": True, "hint": "sivri ekzofitik siğil yapısı"}]},
            {"cells": [{"text": "Bulaştırıcılık", "isMasked": False}, {"text": "Aşırı derecede yüksek canlı spiroket", "isMasked": True, "hint": "yüksek bulaştırıcı bakteri yükü"}, {"text": "Viral temasla bulaşır"}]}
        ]),
        make_chain("Kondiloma Lata Gelişim Yolu", [
            "1. Nemli Alan Yayılımı: Spiroketler sürtünmeli perineal deriye yerleşir.",
            "2. Epidermal Kalınlaşma: Epitelde maserasyon ve akantotik hiperplazi oluşur.",
            "3. Düzleşmiş Plak: Lezyon yüzeyi nemle aşınarak gri-beyaz düz plak halini alır.",
            "4. Masif Eksüda: Yüzeyden sızan seröz sıvı canlı spiroket kaynar ve temasla bulaşır."
        ]),
        make_recall("Kondiloma lata nedir, hangi sifiliz evresinde görülür ve morfolojik özellikleri nelerdir?", "Sekonder sifilizde nemli kıvrım yerlerinde (vulva, perine) görülen gri-beyaz, geniş tabanlı, düz yüzeyli ve son derece bulaştırıcı lezyonlardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kondiloma Lata", [
            {"text": "Kondiloma lata sekonder sifiliz evresinde görülür.", "isLie": False, "explanation": "Doğru. Sekonder dönemin tipik lezyonudur."},
            {"text": "Vulva, skrotum ve perine gibi nemli alanlarda yerleşir.", "isLie": False, "explanation": "Doğru. İntertrijinöz alanları sever."},
            {"text": "Kondiloma lata lezyonları tamamen kısırdır ve dokunan kişiye asla bulaşmaz.", "isLie": True, "explanation": "Tuzak! Kondiloma lata canlı spiroket kaynar ve son derece yüksek oranda bulaştırıcıdır."},
            {"text": "Gri-beyaz, geniş tabanlı plaklar şeklinde izlenir.", "isLie": False, "explanation": "Doğru. Tipik makroskopi bulgusudur."}
        ]),
        make_quiz("Sekonder sifilizde genital ve perineal nemli deri kıvrımlarında gelişen yüksek oranda bulaştırıcı gri-beyaz plaklara ne ad verilir?", [
            {"key": "A", "text": "Kondiloma lata", "isCorrect": True, "explanation": "Sekonder sifilizin bu lezyonuna kondiloma lata denir."},
            {"key": "B", "text": "Bartholin kisti", "isCorrect": False, "explanation": "Benign kistik lezyondur."},
            {"key": "C", "text": "Melanom", "isCorrect": False, "explanation": "Pigmente malignitedir."},
            {"key": "D", "text": "Gartner kisti", "isCorrect": False, "explanation": "Mezonefrik kalıntıdır."}
        ])
    ]
    slides.append(make_slide(18, "Kondiloma Lata: Nemli Alanların Bulaştırıcı Plakları", "İntertrijinöz alanlar, vulva/skrotum/perine, düz tepeli gri-beyaz plaklar ve spiroket zenginliği", "Mukokutanöz Lezyonlar: Kondiloma Lata", s18_narrative, s18_bullets, s18_elements))

    # Slide 19: Mukozal Lezyonlar ve Toksik Alopesi (Kaş Dökülmesi)
    s19_narrative = (
        "Sekonder sifiliz yalnızca deriyi değil, vücuttaki tüm mukozal yüzeyleri ve kıl foliküllerini "
        "de yaygın biçimde etkileyen sistemik bir hastalıktır.\n\n"
        "- **Mukozal Yama (Mucous Patches):** Ağız içi, dil, farenks, larenks ve servikovajinal mukozada "
        "ağrısız, yüzeyi erozyone, çevreleri eritemli **gri-beyaz mukozal yamalar (müköz plaklar)** izlenir. "
        "Bu lezyonlar spiroket dolu olup oral temasla kolayca bulaşır.\n"
        "- **Toksik Alopesi (Güve Yeniği Saç Dökülmesi):** Bakterilerin kıl foliküllerinde oluşturduğu "
        "perivasküler inflamasyon sonucu saçlı deride yama tarzında, düzensiz **güve yeniği benzeri saç dökülmesi** görülür.\n"
        "- **Kaş Dökülmesi:** Saç dökülmesine ek olarak hastaların **kaşlarının dış 1/3'lük kısımlarında dökülme** "
        "saptanması sifiliz için oldukça karakteristik bir fizik muayene bulgusudur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Sekonder sifilizde ağız ve mukozalarda gri-beyaz müköz plaklar; kıl folikülü tutulumuyla güve yeniği tarzında toksik alopesi ve kaş dökülmesi izlenir."
    )
    s19_bullets = [
        "Ağız, farinks ve larinkste gri-beyaz müköz yamalar izlenir.",
        "Kıl folikülü tutulumu güve yeniği tarzı toksik alopesi yapar.",
        "Kaşların dış kısımlarında dökülme tipik klinik bulgudur."
    ]
    s19_elements = [
        make_cloze("Sekonder sifilizde kıl foliküllerinin tutulması sonucu gelişen yama tarzı saç dökülmesine toksik alopesi adı verilir.", "toksik alopesi", "Güve yeniği tarzında gelişen sifilitik saç dökülmesi"),
        make_table("Mukozal ve Folliküler Tutulum Özellikleri", ["Klinik Alan", "Gözlenen Patoloji", "Klinik Özellik"], [
            {"cells": [{"text": "Ağız ve Farinks", "isMasked": False}, {"text": "Gri-beyaz eritemli müköz yamalar", "isMasked": True, "hint": "oral mukoza plakları"}, {"text": "Ağrısızdır fakat son derece bulaştırıcıdır"}]},
            {"cells": [{"text": "Kıl Folikülleri", "isMasked": False}, {"text": "Güve yeniği alopesi ve kaş dökülmesi", "isMasked": False}, {"text": "Tedaviyle tamamen geri dönebilen dökülme", "isMasked": True, "hint": "tedavi sonrası saçın yeniden çıkması"}]}
        ]),
        make_chain("Foliküler Tutulum Zinciri", [
            "1. Foliküler İnflamasyon: Spiroketler kıl köklerindeki kapillere yerleşir.",
            "2. Plazmasitik Kuşatma: Kıl kökü çevresinde perivasküler lenfoplazmasitik kılıf oluşur.",
            "3. Kıl Matriks Hasarı: Kıl büyümesi durur ve telogen faza girer.",
            "4. Toksik Dökülme: Saçta yamalı güve yeniği açılır ve kaşların kenarları dökülür."
        ]),
        make_recall("Sekonder sifilizde saçlı deri ve kaşlarda görülen karakteristik foliküler tutulum bulguları nelerdir?", "Güve yeniği tarzında toksik alopesi ve kaşlarda (özellikle dış kısımlarında) dökülmedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Mukoza ve Alopesi Bulguları", [
            {"text": "Ağız ve farinkste gri-beyaz mukozal lezyonlar görülebilir.", "isLie": False, "explanation": "Doğru. Tipik müköz yamalardır."},
            {"text": "Kıl foliküllerinin tutulumu toksik alopesi ve kaş dökülmesi yapar.", "isLie": False, "explanation": "Doğru. Güve yeniği manzarası oluşturur."},
            {"text": "Sekonder sifilizde saçlar anında uzayarak yerlere kadar dökülmeden ipek olur.", "isLie": True, "explanation": "Tuzak! Saçlar güzelleşmez; perivasküler inflamasyonla dökülerek güve yeniği alopesi yapar."},
            {"text": "Mukozal lezyonlar spiroket içerir ve bulaştırıcıdır.", "isLie": False, "explanation": "Doğru. Müköz plaklar bulaştırıcıdır."}
        ]),
        make_quiz("Sekonder sifilizde kıl foliküllerinin tutulması sonucu ortaya çıkan karakteristik saç ve kaş bulgusu nedir?", [
            {"key": "A", "text": "Güve yeniği tarzında toksik alopesi ve kaşlarda dökülme", "isCorrect": True, "explanation": "Güve yeniği tarzı alopesi ve kaş dökülmesi sekonder sifilize özgüdür."},
            {"key": "B", "text": "Saçların tamamen kızıla dönmesi", "isCorrect": False, "explanation": "Renk değişikliği yapmaz."},
            {"key": "C", "text": "Tüm vücutta aşırı kıllanma (hipertrikoz)", "isCorrect": False, "explanation": "Dökülme yapar, kıllanma yapmaz."},
            {"key": "D", "text": "Sadece diş etinde saç çıkması", "isCorrect": False, "explanation": "Tıbben imkansızdır."}
        ])
    ]
    slides.append(make_slide(19, "Mukozal Lezyonlar ve Toksik Alopesi (Kaş Dökülmesi)", "Müköz yamalar, oral spiroketemi, güve yeniği alopesi ve kaş dökülmesi", "Mukoza ve Adneks Tutulumu", s19_narrative, s19_bullets, s19_elements))

    # Slide 20: [TEKRAR SAYFASI - CHECKPOINT 2] Primer Sifiliz ve Sekonder Kutanöz Bulgular
    s20_narrative = (
        "Bölüm 2'de primer sifilizin sert şankrını, lenfadenopatisini ve sekonder dönemin "
        "kardinal kutanöz bulgularını kapsamlı biçimde konsolide ediyoruz.\n\n"
        "- **Primer Şankr:** ~3 haftalık kuluçka sonrası inokülasyon yerinde gelişen **ağrısız, sert "
        "tabanlı, temiz ülserdir**; bol spiroket içerdiğinden **son derece bulaştırıcıdır**. Kadında servikste "
        "yerleştiğinde ağrısız olduğu için sıklıkla fark edilmez. Tedavi edilmese dahi **yaklaşık 1 ay içinde "
        "kendiliğinden iyileşir (aldatıcı şifa)**.\n"
        "- **Primer LAP:** Şankrdan **1 hafta sonra** gelişen ağrısız, sert, lastik kıvamında lenfadenopatidir; "
        "kesinlikle süpürasyon (apse) yapmaz.\n"
        "- **Sekonder Cilt Bulguları:** Şankrdan **2-8 hafta sonra** patlak verir. Döküntüler **kaşıntısız, "
        "simetrik, bilateral ve yaygındır**. **El içi ve ayak tabanı döküntülerinde sifiliz özellikle düşünülmelidir**.\n"
        "- **Kondiloma Lata ve Alopesi:** Nemli kıvrımlarda gelişen **kondiloma lata** son derece bulaştırıcı "
        "gri-beyaz plaklardır; kıl tutulumuyla **toksik alopesi ve kaş dökülmesi** izlenir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 2 SENTEZİ] Primer şankr ağrısız, sert ve bulaştırıcıdır, 1 ayda kendiliğinden geçer. Sekonder döküntü kaşıntısız ve simetriktir; el-ayak tabanı tutulumu ve nemli alanlardaki kondiloma lata kardinal bulgulardır."
    )
    s20_bullets = [
        "Şankr ağrısız, sert, bulaştırıcıdır; 1 haftada LAP gelişir, 1 ayda kendiliğinden geçer.",
        "Sekonder evre 2-8 haftada başlar; döküntüler kaşıntısız, simetrik ve bilateraldir.",
        "El içi-ayak tabanı tutulumu ve nemli kıvrımlardaki kondiloma lata patognomoniktir.",
        "Kıl kökü tutulumu güve yeniği toksik alopesi ve kaş dökülmesi yapar."
    ]
    s20_elements = [
        make_cloze("Sekonder sifilizde nemli alanlarda gelişen yüksek bulaştırıcı plaklara kondiloma lata adı verilir.", "kondiloma lata", "Bölüm 2 checkpointinde pekiştirilen bulaştırıcı plak"),
        make_table("Bölüm 2 Klinik Bulgular Sentez Tablosu", ["Evre / Lezyon", "Temel Morfolojik Özellik", "Kritik Sınav Notu"], [
            {"cells": [{"text": "Primer Şankr", "isMasked": False}, {"text": "Ağrısız, sert tabanlı, temiz ülser", "isMasked": True, "hint": "ağrısız endüre primer lezyon"}, {"text": "Bulaştırıcıdır, 1 ayda kendiliğinden iyileşir"}]},
            {"cells": [{"text": "Sekonder Cilt Döküntüsü", "isMasked": False}, {"text": "Kaşıntısız, simetrik, el içi ve ayak tabanı", "isMasked": False}, {"text": "Avuç içi döküntüsünde sifiliz düşünülmelidir", "isMasked": True, "hint": "palmar-plantar alarm bulgusu"}]},
            {"cells": [{"text": "Kondiloma Lata", "isMasked": False}, {"text": "Nemli intertrijinöz alanda gri-beyaz plak", "isMasked": True, "hint": "nemli bölge genital plağı"}, {"text": "Bol spiroket içerir, son derece bulaştırıcıdır"}]}
        ]),
        make_chain("Bölüm 2 Süreç Konsolidasyonu", [
            "1. Primer Faz: 3. haftada ağrısız şankr çıkar, 1 hafta sonra ağrısız LAP eklenir.",
            "2. Aldatıcı İyileşme: 1 ayda şankr kapanır fakat spiroketler kana yayılır.",
            "3. Sekonder Patlama: 2-8 hafta sonra el-ayak tabanında kaşıntısız simetrik döküntü belirir.",
            "4. Genital Plaklar: Nemli alanda kondiloma lata oturur ve kaşlar dökülür."
        ]),
        make_recall("Bölüm 2'de öğrendiğimiz: (1) Şankrın ağrı ve bulaşıcılık durumu, (2) Döküntünün kaşıntı durumu ve (3) Nemli alan lezyonu nedir?", "(1) Ağrısız ve son derece bulaştırıcıdır, (2) Kaşıntısızdır, (3) Kondiloma latadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 2 Checkpoint Sentezi", [
            {"text": "Şankr ağrısızdır ve son derece bulaştırıcıdır.", "isLie": False, "explanation": "Doğru. Tipik şankr özelliğidir."},
            {"text": "Şankr tedavisiz de yaklaşık 1 ayda kendiliğinden iyileşir.", "isLie": False, "explanation": "Doğru. Spontan epitelize olur."},
            {"text": "Sekonder sifiliz döküntüleri sadece tek bir parmağın ucunda aşırı kaşıntılı tek bir sivilcedir.", "isLie": True, "explanation": "Tuzak! Döküntüler kaşıntısız, simetrik, bilateral ve yaygındır; el içi ve ayak tabanını tutar."},
            {"text": "Kondiloma lata nemli kıvrımlarda gelişen bulaştırıcı lezyonlardır.", "isLie": False, "explanation": "Doğru. Sekonder dönemin bulaştırıcı plağıdır."}
        ]),
        make_quiz("Bölüm 2'de işlenen primer ve sekonder sifiliz bulguları ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Primer şankr şiddetli ağrı yapar ve kesinlikle bulaştırıcı değildir", "isCorrect": True, "explanation": "Yanlış önerme! Şankr AĞRISIZDIR ve son derece BULAŞTIRICIDIR."},
            {"key": "B", "text": "Şankr tedavisiz kalsa bile yaklaşık 1 ayda kendiliğinden geçer", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Sekonder sifiliz döküntüleri kaşıntısız ve simetriktir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Kondiloma lata nemli genital alanlarda görülen bulaştırıcı plaklardır", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(20, "[TEKRAR SAYFASI - CHECKPOINT 2] Primer Sifiliz ve Sekonder Kutanöz Bulgular", "Bölüm 2 kapsamlı tekrarı: şankr, 1 ayda iyileşme, kaşıntısız döküntü, kondiloma lata ve alopesi", "Bölüm Tekrarı ve Konsolidasyon", s20_narrative, s20_bullets, s20_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec2()
    print(f"Sec2 generated: {len(slides)} slides (Slide 11 to 20)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
