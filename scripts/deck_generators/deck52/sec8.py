# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec8():
    slides = []

    # Slide 71: Akut Sistit Ampirik Tedavisi: TMP-SXT ve Direnç Eşiği
    s71_narrative = (
        "Lokalize alt üriner sistem enfeksiyonu olan akut sistitte akılcı antibiyotik seçimi, "
        "toplumdaki yerel direnç oranları dikkate alınarak yapılmalıdır.\n\n"
        "- **İlk Tercih Rejim:** Akut sistitte ilk tercih ajanlar arasında **Trimetoprim-sulfametoksazol "
        "(TMP-SXT) 2x160/800 mg doz ile 5 gün** yer alır.\n"
        "- **Direnç Eşik Kuralı:** TMP-SXT'nin ampirik ilk tercih olarak güvenle kullanılabilmesi için "
        "o bölgedeki **lokal direnç oranının <%20 olması** şarttır.\n"
        "- **Klinik Başarısızlık Eşiği:** Eğer toplumdaki E. coli kökenli TMP-SXT direnci %20'yi aşıyorsa, "
        "bu ajanın ampirik olarak başlanması yüksek tedavi başarısızlığı riski taşır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Akut sistitte ilk tercih: Trimetoprim-sulfametoksazol (TMP-SXT) 2x160/800 mg doz ile 5 gündür (lokal direnç <%20 ise)."
    )
    s71_bullets = [
        "İlk tercih: Trimetoprim-sulfametoksazol (TMP-SXT) 2x160/800 mg doz ile 5 gün.",
        "Kullanım koşulu: Lokal direnç oranının <%20 olması şarttır.",
        "Yerel direnç %20'nin üzerindeyse ampirik ilk seçenek olarak önerilmez."
    ]
    s71_elements = [
        make_cloze("Akut sistitte ilk tercih trimetoprim-sulfametoksazol (TMP-SXT) 2x160/800 mg doz ile 5 gündür (lokal direnç <%20 ise).", "2x160/800 mg doz ile 5 gün", "TMP-SXT'nin standart sistit tedavi dozu ve süresi"),
        make_table("TMP-SXT Sistit Tedavi Protokolü", ["Parametre", "Standart Uygulama Kriteri", "Klinik Gerekçe"], [
            {"cells": [{"text": "Doz ve Süre", "isMasked": False}, {"text": "2x160/800 mg oral, 5 gün", "isMasked": True, "hint": "günde iki kez beş günlük kür"}, {"text": "Yeterli doku ve idrar konsantrasyonu"}]},
            {"cells": [{"text": "Direnç Sınırı", "isMasked": False}, {"text": "Lokal direnç <%20 olmalıdır", "isMasked": True, "hint": "yüzde yirmiden az direnç"}, {"text": "Tedavi başarısızlığını önleme"}]}
        ]),
        make_chain("TMP-SXT Tedavi Karar Zinciri", [
            "1. Klinik Tanı: Akut komplike olmayan sistit tablosu.",
            "2. Direnç Kontrolü: Bölgesel TMP-SXT direncinin <%20 olduğunun doğrulanması.",
            "3. Reçete: TMP-SXT 2x160/800 mg oral başlanması.",
            "4. Süre: Tedavinin tam 5 günde tamamlanması."
        ]),
        make_recall("Akut sistitte TMP-SXT'nin dozu, tedavi süresi ve kullanılabilmesi için gereken lokal direnç eşiği nedir?", "2x160/800 mg doz ile 5 gündür; lokal direncin <%20 olması şarttır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: TMP-SXT Sistit", [
            {"text": "TMP-SXT 2x160/800 mg doz ile 5 gün kullanılır.", "isLie": False, "explanation": "Doğru. Ders notu protokolüdür."},
            {"text": "Lokal direnç <%20 ise ilk tercih ajanlar arasındadır.", "isLie": False, "explanation": "Doğru. Direnç eşiğidir."},
            {"text": "Lokal direnç %99 olsa bile TMP-SXT her zaman tek ve zorunlu ilk seçenektir.", "isLie": True, "explanation": "Tuzak! TMP-SXT ancak lokal direnç <%20 olduğunda ampirik ilk tercih olarak önerilir."},
            {"text": "TMP-SXT oral yoldan kullanılan bir kombinasyondur.", "isLie": False, "explanation": "Doğru. Tablet formudur."}
        ]),
        make_quiz("Akut sistit ampirik tedavisinde TMP-SXT'nin standart dozu, kullanım süresi ve lokal direnç eşiği aşağıdakilerden hangisinde DOĞRU verilmiştir?", [
            {"key": "A", "text": "TMP-SXT 2x160/800 mg doz ile 5 gün (lokal direnç <%20 ise)", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Trimetoprim-sulfametoksazol (TMP-SXT) 2x160/800 mg doz ile 5 gün (lokal direnç <%20 ise)' denmektedir."},
            {"key": "B", "text": "TMP-SXT 1x100 mg 1 gün (lokal direnç >%80 ise)", "isCorrect": False, "explanation": "Doz, süre ve direnç kriteri yanlıştır."},
            {"key": "C", "text": "TMP-SXT 4x2000 mg 30 gün", "isCorrect": False, "explanation": "Aşırı toksik ve yanlış dozdur."},
            {"key": "D", "text": "TMP-SXT sistitte asla kullanılamaz, tamamen yasaktır", "isCorrect": False, "explanation": "Direnç düşükse ilk tercihtir."}
        ])
    ]
    slides.append(make_slide(71, "Akut Sistit Tedavisi: TMP-SXT ve Direnç Eşiği", "TMP-SXT 2x160/800 mg 5 gün rejimi ve %20 yerel direnç sınırı", "Sistit Tedavisi", s71_narrative, s71_bullets, s71_elements))

    # Slide 72: Florokinolonlar: Yan Etki ve Artan Direnç Uyarısı
    s72_narrative = (
        "Florokinolon grubu antibiyotikler (siprofloksasin, levofloksasin), geçmişte sistitte yaygın "
        "kullanılmış olsa da günümüzde ciddi güvenlik uyarıları nedeniyle geri plana çekilmiştir.\n\n"
        "- **Kullanım Kısıtlaması:** Florokinolonlar (yan etki ve artan direnç oranları nedeniyle) sistitte "
        "**yalnızca diğer yaygın ajanların kullanılamadığı durumlarda** kullanılabilir.\n"
        "- **Kollateral Hasar ve Yan Etkiler:** Tendinit, tendon rüptürü, QT uzaması, periferik nöropati "
        "ve santral sinir sistemi toksisitesi gibi kalıcı olabilen ciddi yan etki profiline sahiptirler.\n"
        "- **Direnç Baskısı:** Basit bir sistitte florokinolon kullanımı, hastanede ve toplumda "
        "kinolona dirençli suşların patlamasına yol açar; bu nedenle basit sistitte ampirik ilk tercih olamazlar.\n\n"
        "> [!WARNING] Florokinolonlar (yan etki ve artan direnç oranları nedeniyle) sistitte yalnızca diğer yaygın ajanların kullanılamadığı durumlarda kullanılabilir!"
    )
    s72_bullets = [
        "Florokinolonlar sistitte yalnızca diğer yaygın ajanlar kullanılamıyorsa tercih edilir.",
        "Ciddi yan etki profili (tendinit, nöropati vb.) nedeniyle ilk seçenek olmaktan çıkarılmıştır.",
        "Hızla artan küresel ve ulusal direnç oranları florokinolon kullanımını kısıtlar."
    ]
    s72_elements = [
        make_cloze("Florokinolonlar sistitte yan etki ve artan direnç oranları nedeniyle yalnızca diğer yaygın ajanların kullanılamadığı durumlarda kullanılabilir.", "yalnızca diğer yaygın ajanların kullanılamadığı durumlarda", "Florokinolonların sistitteki kısıtlı kullanım endikasyonu"),
        make_table("Florokinolonların Sistitteki Konumu", ["Antibiyotik Grubu", "Kullanım Kuralı", "Kısıtlama Gerekçeleri"], [
            {"cells": [{"text": "Florokinolonlar (Siprofloksasin vb.)", "isMasked": False}, {"text": "Yalnızca diğer ajanlar kullanılamıyorsa", "isMasked": True, "hint": "son çare rezerv kullanım"}, {"text": "Ciddi yan etkiler ve artan direnç oranları", "isMasked": True, "hint": "toksisite ve direnç baskısı"}]}
        ]),
        make_chain("Florokinolon Kısıtlama Mantığı", [
            "1. Basit Sistit Başvurusu: Komplike olmayan alt üriner enfeksiyon.",
            "2. Ajan Taraması: TMP-SXT, nitrofurantoin veya fosfomisinin değerlendirilmesi.",
            "3. Diğer Ajanların Kontrendikasyonu: Hiçbir standart ajanın verilememesi.",
            "4. Rezerve Kullanım: Ancak bu istisna halinde florokinolon başlanması."
        ]),
        make_recall("Ders notuna göre florokinolonlar sistitte hangi şart altında kullanılabilir ve gerekçesi nedir?", "Yan etki ve artan direnç oranları nedeniyle, yalnızca diğer yaygın ajanların kullanılamadığı durumlarda kullanılabilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Florokinolonlar", [
            {"text": "Florokinolonlar sistitte yalnızca diğer yaygın ajanların kullanılamadığı durumlarda tercih edilir.", "isLie": False, "explanation": "Doğru. Ders notu kısıtlamasıdır."},
            {"text": "Yan etki ve artan direnç oranları florokinolonların kısıtlanma nedenidir.", "isLie": False, "explanation": "Doğru. İki temel gerekçedir."},
            {"text": "Her basit sistit hastasına ilk saniyede mutlaka en yüksek doz florokinolon başlanmalıdır.", "isLie": True, "explanation": "Tuzak! Florokinolonlar basit sistitte ilk tercih değildir; yan etki ve direnç nedeniyle saklanır."},
            {"text": "Florokinolon direnci toplumda yükselmektedir.", "isLie": False, "explanation": "Doğru. Direnç oranı yüksektir."}
        ]),
        make_quiz("Akut sistitte florokinolon grubu antibiyotiklerin kullanım endikasyonu aşağıdakilerden hangisinde doğru ifade edilmiştir?", [
            {"key": "A", "text": "Yalnızca diğer yaygın ajanların kullanılamadığı durumlarda (yan etki ve artan direnç oranları nedeniyle)", "isCorrect": True, "explanation": "Ders notunda 'Florokinolonlar (yan etki ve artan direnç oranları!!!) sistitte yalnızca diğer yaygın ajanların kullanılamadığı durumlarda kullanılabilir' denmektedir."},
            {"key": "B", "text": "Her hastada istisnasız ilk ve zorunlu ampirik tercih olarak", "isCorrect": False, "explanation": "İlk tercih değildir."},
            {"key": "C", "text": "Sadece idrar kültürü tamamen steril olan sağlıklı kişilerde", "isCorrect": False, "explanation": "Enfeksiyon yokken antibiyotik verilmez."},
            {"key": "D", "text": "Yalnızca vitamin takviyesi amacıyla", "isCorrect": False, "explanation": "Antibiyotiktir, vitamin değildir."}
        ])
    ]
    slides.append(make_slide(72, "Florokinolonlar: Yan Etki ve Direnç Uyarısı", "Florokinolonların kısıtlı endikasyonu, toksisite riskleri ve direnç uyarısı", "Sistit Tedavisi", s72_narrative, s72_bullets, s72_elements))

    # Slide 73: Akut Sistitte Tedavi Süresi (Kadın ve Erkek)
    s73_narrative = (
        "Akut sistit tedavisinde antibiyotik süresi, enfeksiyonun anatomik lokalizasyonuna ve hastanın "
        "cinsiyetine göre belirlenir.\n\n"
        "- **Genel Süre:** Komplike olmayan kadın sistitinde tedavi süresi **genellikle 3 ila 5 gün** arasındadır.\n"
        "- **Erkek Hastalarda Süre:** Erkek hastalar için sistemik belirti yoksa tedavi süresi **5-7 gündür**.\n"
        "- **Süre Uzamasının Nedeni:** Erkeklerde sistit nadir olduğundan ve prostat dokusunun subklinik "
        "tutulum riski bulunduğundan, bakteriyel eradikasyonu garantiye almak için süre daha uzundur.\n\n"
        "> [!IMPORTANT]\n"
        "> Tedavi süresi: Genellikle 3 ila 5 gün arasındadır; erkek hastalar için sistemik belirti yoksa 5-7 gündür."
    )
    s73_bullets = [
        "Genel tedavi süresi: Genellikle 3 ila 5 gün arasındadır.",
        "Erkek hastalarda (sistemik belirti yoksa) süre: 5-7 gündür.",
        "Gereksiz uzun süreli antibiyotik tedavileri flora hasarı yaratır; kısa kürler yeterlidir."
    ]
    s73_elements = [
        make_cloze("Akut sistitte tedavi süresi genellikle 3 ila 5 gün arasındadır (erkek hastalar için sistemik belirti yoksa 5-7 gün).", "3 ila 5 gün", "Akut sistitteki genel standart tedavi süresi"),
        make_table("Cinsiyete Göre Sistit Tedavi Süreleri", ["Hasta Grubu", "Klinik Tablo", "Önerilen Tedavi Süresi"], [
            {"cells": [{"text": "Kadın Hastalar (Genel)", "isMasked": False}, {"text": "Komplike olmayan akut sistit", "isMasked": False}, {"text": "3 ila 5 gün", "isMasked": True, "hint": "üç ila beş günlük kür"}]},
            {"cells": [{"text": "Erkek Hastalar", "isMasked": False}, {"text": "Sistemik belirti yoksa", "isMasked": True, "hint": "ateşsiz lokalize tablo"}, {"text": "5-7 gün", "isMasked": True, "hint": "beş ila yedi gün"}]}
        ]),
        make_chain("Tedavi Süresi Karar Algoritması", [
            "1. Sistit Tanısı: Lokal alt üriner sistem semptomları.",
            "2. Cinsiyet Değerlendirmesi: Kadın vs erkek ayrımı.",
            "3. Sistemik Belirti Kontrolü: Ateş/KVAH olmaması.",
            "4. Süre Tayini: Kadında 3-5 gün, erkekte 5-7 gün antibiyotik."
        ]),
        make_recall("Akut sistitte genel tedavi süresi kaç gündür ve erkek hastalarda (sistemik belirti yoksa) kaç gün uygulanır?", "Genellikle 3 ila 5 gün arasındadır; erkek hastalar için sistemik belirti yoksa 5-7 gündür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tedavi Süresi", [
            {"text": "Sistit tedavi süresi genellikle 3 ila 5 gün arasındadır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Erkek hastalarda sistemik belirti yoksa süre 5-7 gündür.", "isLie": False, "explanation": "Doğru. Erkekteki süredir."},
            {"text": "Basit sistitte tedavi en az 10 yıl boyunca kesintisiz her gün damardan verilmelidir.", "isLie": True, "explanation": "Tuzak! Sistit kısa süreli (3-5 gün; erkekte 5-7 gün) tedavi edilir."},
            {"text": "Kısa süreli tedaviler yan etki riskini azaltır.", "isLie": False, "explanation": "Doğru. Uyum ve güvenliği artırır."}
        ]),
        make_quiz("Akut sistitte genel tedavi süresi ve erkek hastalarda sistemik belirti yoksa önerilen tedavi süresi aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Genellikle 3 ila 5 gün; erkek hastalar için sistemik belirti yoksa 5-7 gün", "isCorrect": True, "explanation": "Ders notunda 'Tedavi süresi: genellikle 3 ila 5 gün arasındadır (erkek hastalar için sistemik belirti yoksa 5-7 gün)' denmektedir."},
            {"key": "B", "text": "Genellikle 1 saat; erkekte 2 saat", "isCorrect": False, "explanation": "Saatlik tedavi olmaz."},
            {"key": "C", "text": "Genellikle 6 ay; erkekte 2 yıl", "isCorrect": False, "explanation": "Çok aşırı sürelerdir."},
            {"key": "D", "text": "Süreye bakılmaksızın sadece tek bir bardak su içilir", "isCorrect": False, "explanation": "Tedavi protokolü değildir."}
        ])
    ]
    slides.append(make_slide(73, "Akut Sistitte Tedavi Süresi: Kadın ve Erkek", "Genellikle 3-5 gün; erkekte sistemik belirti yoksa 5-7 gün tedavi süresi", "Sistit Tedavisi", s73_narrative, s73_bullets, s73_elements))

    # Slide 74: Aminopenisilinler: Yüksek E. coli Direnci ve Uygunsuzluk
    s74_narrative = (
        "Antibiyotik çağının başlangıcında sistitte yaygın kullanılan klasik aminopenisilinler "
        "(ampisilin, amoksisilin), günümüzde üriner enfeksiyon ampirik tedavisinde tamamen terk edilmiştir.\n\n"
        "- **Direnç Uyarısı:** **Aminopenisilinler dünya çapında yüksek E. coli direnci nedeniyle "
        "ampirik tedaviye uygun değildir**.\n"
        "- **Direnç Oranları:** Ülkemizde ve dünyada E. coli suşlarında ampisilin direnci %60'ları "
        "aşmış durumdadır; bu denli yüksek direnç oranı ampirik başarı şansını ortadan kaldırır.\n"
        "- **Klinik İlke:** Kültür sonucu çıkmadan önce hiçbir sistit hastasına tek başına ampisilin "
        "veya amoksisilin başlanmamalıdır.\n\n"
        "> [!WARNING] Aminopenisilinler dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildir!"
    )
    s74_bullets = [
        "Aminopenisilinler dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildir.",
        "Ampisilin direnci toplum kökenli suşlarda dahi %60'ın üzerindedir.",
        "Kültürde duyarlılık kanıtlanmadıkça ampirik sistit tedavisinde asla seçilmemelidir."
    ]
    s74_elements = [
        make_cloze("Aminopenisilinler dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildir.", "ampirik tedaviye uygun değildir", "Aminopenisilinlerin yüksek direnç nedeniyle sistitteki durumu"),
        make_table("Aminopenisilinlerin Sistitteki Durumu", ["İlaç Grubu", "Direnç Durumu", "Klinik Karar"], [
            {"cells": [{"text": "Aminopenisilinler (Ampisilin, Amoksisilin)", "isMasked": False}, {"text": "Dünya çapında yüksek E. coli direnci", "isMasked": True, "hint": "küresel yüksek direnç"}, {"text": "Ampirik tedaviye UYGUN DEĞİLDİR", "isMasked": True, "hint": "kullanılmaması kuralı"}]}
        ]),
        make_chain("Aminopenisilinlerin Dışlanma Mantığı", [
            "1. Tarihsel Kullanım: Yoğun ve kontrolsüz aminopenisilin tüketimi.",
            "2. Beta-laktamaz Gelişimi: E. coli suşlarında plazmid kaynaklı direnç.",
            "3. Direnç Zirvesi: Direnç oranlarının %60'ın üzerine tırmanması.",
            "4. Dışlanma: Rehberlerin aminopenisilinleri ampirik tedaviden çıkarması."
        ]),
        make_recall("Aminopenisilinlerin akut sistit ampirik tedavisinde önerilmeme gerekçesi nedir?", "Dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildirler."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Aminopenisilinler", [
            {"text": "Aminopenisilinler dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Ampisilin ve amoksisilin aminopenisilin grubundadır.", "isLie": False, "explanation": "Doğru. Farmakolojik sınıftır."},
            {"text": "Aminopenisilinlere karşı dünyadaki tüm bakteriler %100 duyarlıdır ve asla direnç gelişmez.", "isLie": True, "explanation": "Tuzak! Dünya çapında çok yüksek E. coli direnci mevcuttur."},
            {"text": "Yüksek direnç tedavinin başarısızlıkla sonuçlanmasına yol açar.", "isLie": False, "explanation": "Doğru. Ameliyat veya nüks riski doğurur."}
        ]),
        make_quiz("Aminopenisilinlerin (ampisilin, amoksisilin) akut sistit ampirik tedavisindeki konumu aşağıdakilerden hangisinde doğru açıklanmıştır?", [
            {"key": "A", "text": "Dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildir", "isCorrect": True, "explanation": "Ders notunda aynen 'Aminopenisilinler dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviye uygun değildir' denmektedir."},
            {"key": "B", "text": "Dünyadaki en etkili ilk tercih mucize ilaçtır", "isCorrect": False, "explanation": "Direnç nedeniyle uygun değildir."},
            {"key": "C", "text": "Yalnızca böbrek taşı eritmek için kullanılır", "isCorrect": False, "explanation": "Taş eritici değildir."},
            {"key": "D", "text": "Sadece mantar enfeksiyonlarında kullanılır", "isCorrect": False, "explanation": "Antibakteriyeldir, antifungallere girmez."}
        ])
    ]
    slides.append(make_slide(74, "Aminopenisilinler: Yüksek Direnç ve Uygunsuzluk", "Dünya çapında yüksek E. coli direnci nedeniyle ampirik tedaviden çıkarılmaları", "Sistit Tedavisi", s74_narrative, s74_bullets, s74_elements))

    # Slide 75: Ekolojik Yan Hasar: Oral Sefalosporinler ve İnhibitörlü Penisilinler
    s75_narrative = (
        "Klinisyenlerin basit sistit tedavisinde sıklıkla reçete ettiği amoksisilin-klavulanat veya "
        "oral sefalosporinler (sefiksim, sefuroksim aksetil), mikrobiyom üzerinde ağır bir tahribat yaratır.\n\n"
        "- **Önerilmeme Nedeni:** Beta-laktamaz inhibitörlü aminopenisilinler ve oral sefalosporinler "
        "**ekolojik yan hasar nedeniyle** ampirik tedavide önerilmez.\n"
        "- **Çoklu Direnç Seçilimi:** Bu ajanların kullanımı, bağırsak florasında **Genişlemiş Spektrumlu "
        "Beta-Laktamaz (GSBL) üreten çoklu dirençli bakterilerin seçilmesine** yol açar.\n"
        "- **Süperenfeksiyon:** Ayrıca normal anaerobik bağırsak florasını baskılayarak **Clostridioides "
        "difficile enfeksiyonlarına** ve gelecekteki enfeksiyonlar için daha dirençli patojenlerin üremesine zemin hazırlar.\n\n"
        "> [!WARNING] Beta-laktamaz inhibitörlü aminopenisilinler ve oral sefalosporinler EKOLOJİK YAN HASAR (GSBL seçilimi ve C. difficile riski) nedeniyle ampirik sistitte önerilmez!"
    )
    s75_bullets = [
        "İnhibitörlü aminopenisilinler ve oral sefalosporinler ekolojik yan hasar nedeniyle önerilmez.",
        "GSBL üreten çoklu dirençli bakterilerin seçilmesine neden olurlar.",
        "Clostridioides difficile enfeksiyonlarına ve gelecekteki dirençli enfeksiyonlara zemin hazırlarlar."
    ]
    s75_elements = [
        make_cloze("Oral sefalosporinler ekolojik yan hasar yaratarak Genişlemiş Spektrumlu Beta-Laktamaz (GSBL) üreten çoklu dirençli bakterilerin seçilmesine zemin hazırlar.", "Genişlemiş Spektrumlu Beta-Laktamaz (GSBL)", "Dirençli enzim üreten çoklu dirençli bakteri tipi"),
        make_table("Ekolojik Yan Hasarın Mekanizmaları", ["Antibiyotik Grubu", "Hedef Dışı Olumsuz Etki", "Klinik Tehlike"], [
            {"cells": [{"text": "Beta-laktamaz inhibitörlü aminopenisilinler", "isMasked": False}, {"text": "Ekolojik yan hasar", "isMasked": True, "hint": "flora tahribatı"}, {"text": "GSBL seçilimi ve C. difficile"}]},
            {"cells": [{"text": "Oral Sefalosporinler", "isMasked": False}, {"text": "Geniş flora baskısı", "isMasked": False}, {"text": "Gelecekteki inatçı dirençli enfeksiyonlar", "isMasked": True, "hint": "tedavisi zor yeni ataklar"}]}
        ]),
        make_chain("Ekolojik Yan Hasar Gelişimi", [
            "1. Basit Sistit Reçetesi: Oral sefalosporin veya ko-amoksilav verilmesi.",
            "2. Flora Katliamı: Bağırsak florasındaki duyarlı bakterilerin ölmesi.",
            "3. Dirençli Seçilim: GSBL üreten suşların ortamda baskın hale gelmesi.",
            "4. Süperenfeksiyon: C. difficile koliti veya dirençli ÜSE atağı gelişimi."
        ]),
        make_recall("Beta-laktamaz inhibitörlü aminopenisilinler ve oral sefalosporinlerin sistit ampirik tedavisinde önerilmeme gerekçesi nedir?", "Ekolojik yan hasar nedeniyle önerilmezler; GSBL üreten çoklu dirençli bakterilerin seçilmesine ve C. difficile enfeksiyonlarına zemin hazırlarlar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ekolojik Yan Hasar", [
            {"text": "Oral sefalosporinler ekolojik yan hasar nedeniyle ampirik sistitte önerilmez.", "isLie": False, "explanation": "Doğru. Ders notundaki kesin uyarıdır."},
            {"text": "Bu ajanların kullanımı GSBL üreten bakterilerin seçilmesine zemin hazırlar.", "isLie": False, "explanation": "Doğru. Dirençli bakteri seçer."},
            {"text": "Oral sefalosporinler Clostridioides difficile enfeksiyonlarına yol açabilir.", "isLie": False, "explanation": "Doğru. C. difficile riskidir."},
            {"text": "Oral sefalosporin almak bağırsak florasını cennete çevirip tüm mikropları ölümsüzleştirir.", "isLie": True, "explanation": "Tuzak! Ekolojik yan hasar yapar, florayı bozar ve tehlikeli dirençli bakterileri seçer."}
        ]),
        make_quiz("Akut sistit ampirik tedavisinde beta-laktamaz inhibitörlü aminopenisilinlerin ve oral sefalosporinlerin önerilmeme gerekçesi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Ekolojik yan hasar nedeniyle (GSBL üreten çoklu dirençli bakterilerin seçilmesi ve C. difficile enfeksiyonlarına yol açması)", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Genişlemiş Spektrumlu Beta-Laktamaz (GSBL) üreten çoklu dirençli bakterilerin seçilmesine, Clostridioides difficile enfeksiyonlarına zemin hazırlar' denmektedir."},
            {"key": "B", "text": "İlaçların tadının acı olması", "isCorrect": False, "explanation": "Tat tıbbi gerekçe değildir."},
            {"key": "C", "text": "Hastada saç dökülmesi yapması", "isCorrect": False, "explanation": "Gerekçe bu değildir."},
            {"key": "D", "text": "Yalnızca böbrekleri dondurması", "isCorrect": False, "explanation": "Tıbbi olarak anlamsızdır."}
        ])
    ]
    slides.append(make_slide(75, "Ekolojik Yan Hasar: GSBL ve C. difficile Tehdidi", "Oral sefalosporinlerin ve ko-amoksilavın GSBL seçilimi ve floraya zararları", "Sistit Tedavisi", s75_narrative, s75_bullets, s75_elements))

    # Slide 76: Özel Durum: Gebelikte Sistit Tedavisi ve TMP-SXT Kısıtlaması
    s76_narrative = (
        "Gebelikte üriner enfeksiyon yönetimi, fetal organogenez ve teratojenite riskleri nedeniyle "
        "ilaç seçiminde azami dikkat gerektirir.\n\n"
        "- **Gebelikte Uygun Ajanlar:** Gebelikte sistit tedavisinde genel olarak uygun kabul edilen "
        "antibiyotikler **penisilinler, sefalosporinler, fosfomisin ve nitrofurantoin**dir.\n"
        "- **TMP-SXT Kısıtlaması:** **TMP-SXT; G6PD eksikliğinde, ilk trimesterde ve son trimesterde "
        "önerilmez**.\n"
        "- **Fetal Riskler:** TMP ilk trimesterde folik asit metabolizmasını bozarak nöral tüp defektlerine; "
        "sulfametoksazol ise son trimesterde bilirubini albüminden ayırarak kernikterus riskine yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Gebelikte uygun ajanlar: Penisilinler, sefalosporinler, fosfomisin, nitrofurantoin. TMP-SXT ise G6PD eksikliğinde, ilk ve son trimesterde ÖNERİLMEZ!"
    )
    s76_bullets = [
        "Gebelikte uygun ajanlar: Penisilinler, sefalosporinler, fosfomisin, nitrofurantoin.",
        "TMP-SXT: G6PD eksikliğinde, ilk trimesterde ve son trimesterde önerilmez.",
        "İlk trimesterde teratojenite (folat antagonizmi), son trimesterde kernikterus riski vardır."
    ]
    s76_elements = [
        make_cloze("Gebelikte TMP-SXT kullanımı G6PD eksikliğinde, ilk ve son trimesterde önerilmez.", "G6PD eksikliğinde, ilk ve son trimesterde", "TMP-SXT'nin gebelikte kontrendike/uygunsuz olduğu üç durum"),
        make_table("Gebelikte Sistit İlaç Seçimi", ["Antibiyotik", "Gebelikteki Güvenlik Durumu", "Önemli Kısıtlama / Risk"], [
            {"cells": [{"text": "Penisilinler, Sefalosporinler, Fosfomisin", "isMasked": False}, {"text": "Genel olarak uygun", "isMasked": True, "hint": "güvenle verilebilenler"}, {"text": "Standart gebelik rejimleri"}]},
            {"cells": [{"text": "Nitrofurantoin", "isMasked": False}, {"text": "Uygun (son haftalar hariç)", "isMasked": False}, {"text": "Term döneminde hemoliz riski", "isMasked": True, "hint": "doğuma yakın hemolitik anemi"}]},
            {"cells": [{"text": "TMP-SXT", "isMasked": False}, {"text": "ÖNERİLMEZ", "isMasked": True, "hint": "kısıtlı / sakıncalı"}, {"text": "G6PD eksikliği, ilk ve son trimester"}]}
        ]),
        make_chain("Gebelikte Antibiyotik Karar Akışı", [
            "1. Gebelik Tespiti: Hastanın gebe olduğunun doğrulanması.",
            "2. Trimester Kontrolü: 1. mi, 2. mi yoksa 3. trimester mi?",
            "3. Güvenli Ajan Seçimi: Penisilin, sefalosporin veya fosfomisin tercihi.",
            "4. TMP-SXT'den Kaçınma: İlk ve son trimesterde kesinlikle reçete etmeme."
        ]),
        make_recall("Gebelikte genel olarak uygun sistit ajanları nelerdir ve TMP-SXT hangi durumlarda önerilmez?", "Penisilinler, sefalosporinler, fosfomisin ve nitrofurantoin uygundur; TMP-SXT ise G6PD eksikliğinde, ilk ve son trimesterde önerilmez."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Gebelikte Tedavi", [
            {"text": "Penisilinler ve sefalosporinler gebelikte sistit için uygundur.", "isLie": False, "explanation": "Doğru. Güvenli ajanlardır."},
            {"text": "Fosfomisin gebelikte sistit tedavisinde kullanılabilir.", "isLie": False, "explanation": "Doğru. Genel olarak uygundur."},
            {"text": "TMP-SXT gebeliğin 1. gününden son gününe kadar her gebeye zorunlu olarak verilmelidir.", "isLie": True, "explanation": "Tuzak! TMP-SXT ilk ve son trimesterde ile G6PD eksikliğinde önerilmez."},
            {"text": "G6PD eksikliğinde TMP-SXT hemolitik anemi riski yaratır.", "isLie": False, "explanation": "Doğru. Kontrendikedir."}
        ]),
        make_quiz("Gebelikte akut sistit tedavisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Penisilinler, sefalosporinler, fosfomisin ve nitrofurantoin uygundur; TMP-SXT ilk ve son trimesterde önerilmez", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Gebelik: genel olarak uygun: penisilinler, sefalosporinler, fosfomisin, nitrofurantoin; TMP-SXT (G6PD eksikliğinde, ilk ve son trimesterde önerilmez)' denmektedir."},
            {"key": "B", "text": "Gebelere hiçbir antibiyotik verilemez, enfeksiyon kendi haline bırakılır", "isCorrect": False, "explanation": "Gebelikte ÜSE mutlaka tedavi edilmelidir."},
            {"key": "C", "text": "TMP-SXT gebelikte en güvenli tek antibiyotiktir", "isCorrect": False, "explanation": "İlk ve son trimesterde önerilmez."},
            {"key": "D", "text": "Sefalosporinler gebelikte kesin kontrendikedir", "isCorrect": False, "explanation": "Sefalosporinler uygundur."}
        ])
    ]
    slides.append(make_slide(76, "Gebelikte Sistit Tedavisi ve İlaç Kısıtlamaları", "Gebelikte güvenli ajanlar ve TMP-SXT'nin trimester/G6PD kısıtlamaları", "Özel Gruplarda Tedavi", s76_narrative, s76_bullets, s76_elements))

    # Slide 77: Böbrek Yetmezliğinde Sistit: Nefrotoksisite ve Nitrofurantoin
    s77_narrative = (
        "Böbrek fonksiyon bozukluğu olan hastalarda sistit tedavisi planlanırken, antibiyotiklerin "
        "nefrotoksisite potansiyeli ve idrardaki terapötik konsantrasyonları belirleyicidir.\n\n"
        "- **Kombinasyon Nefrotoksisitesi:** Böbrek yetmezliğinde **loop diüretik + sefalosporin "
        "kombinasyonu belirgin nefrotoksiktir**; bu ikilinin birlikte kullanımından kaçınılmalıdır.\n"
        "- **Nitrofurantoin Kontrendikasyonu:** **Nitrofurantoin eGFR <30 mL/dk/1,73 m² düzeyinde "
        "kontrendikedir**.\n"
        "- **Nedeni ve Tehlikesi:** Düşük glomerüler filtrasyonda nitrofurantoin renal tübüllerden "
        "idrara yeterince atılamaz (terapötik etki kaybolur) ve serumda birikerek toksik periferik nöropatiye yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Böbrek yetmezliğinde: Loop diüretik + sefalosporin nefrotoksiktir; Nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir!"
    )
    s77_bullets = [
        "Loop diüretik + sefalosporin kombinasyonu nefrotoksiktir.",
        "Nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir.",
        "Düşük GFR'de idrar konsantrasyonu düşerken sistemik nörotoksisite riski artar."
    ]
    s77_elements = [
        make_cloze("Böbrek yetmezliğinde nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir.", "eGFR <30 mL/dk/1,73 m²'de", "Nitrofurantoinin kesin kontrendike olduğu glomerüler filtrasyon eşiği"),
        make_table("Böbrek Yetmezliğinde Toksisite Kuralları", ["İlaç / Kombinasyon", "Etkileşim / Kısıtlama", "Klinik Risk"], [
            {"cells": [{"text": "Loop Diüretik + Sefalosporin", "isMasked": False}, {"text": "Nefrotoksik etkileşim", "isMasked": True, "hint": "böbreğe toksik sinerji"}, {"text": "Akut böbrek hasarı"}]},
            {"cells": [{"text": "Nitrofurantoin", "isMasked": False}, {"text": "eGFR <30 mL/dk'da KONTRENDİKE", "isMasked": True, "hint": "otuzun altında yasak"}, {"text": "Etkisizlik ve periferik nöropati", "isMasked": False}]}
        ]),
        make_chain("Nitrofurantoin Toksisite Mekanizması", [
            "1. Düşük GFR: Hastanın eGFR düzeyinin <30 mL/dk olması.",
            "2. Filtrasyon Engeli: İlacın glomerülden idrara geçememesi.",
            "3. İdrarda Başarısızlık: İdrar konsantrasyonunun antibakteriyel eşiğin altında kalması.",
            "4. Sistemik Birikim: Kanda birikerek ağır periferik nöropati yapması."
        ]),
        make_recall("Böbrek yetmezliğinde nitrofurantoin hangi eGFR düzeyinde kontrendikedir ve hangi kombinasyon nefrotoksiktir?", "eGFR <30 mL/dk/1,73 m² düzeyinde kontrendikedir; loop diüretik + sefalosporin kombinasyonu nefrotoksiktir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Böbrek Yetmezliği", [
            {"text": "Loop diüretik + sefalosporin kombinasyonu nefrotoksiktir.", "isLie": False, "explanation": "Doğru. Ders notu uyarısıdır."},
            {"text": "Nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir.", "isLie": False, "explanation": "Doğru. Kesin kontrendikasyondur."},
            {"text": "eGFR sıfır olan diyaliz hastalarına sınırsız nitrofurantoin verilmesi böbrekleri yeniden üretir.", "isLie": True, "explanation": "Tuzak! eGFR <30'da nitrofurantoin kontrendikedir; nörotoksisite yapar."},
            {"text": "Düşük GFR'de nitrofurantoin idrara geçemez.", "isLie": False, "explanation": "Doğru. Terapötik etki oluşamaz."}
        ]),
        make_quiz("Böbrek yetmezliği olan bir hastada akut sistit tedavisi planlanırken nitrofurantoin kullanımı ile ilgili aşağıdaki kurallardan hangisi DOĞRUDUR?", [
            {"key": "A", "text": "eGFR <30 mL/dk/1,73 m² düzeyinde kontrendikedir", "isCorrect": True, "explanation": "Ders notunda açıkça 'nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir' denmektedir."},
            {"key": "B", "text": "Her eGFR düzeyinde en güvenli tek antibiyotiktir", "isCorrect": False, "explanation": "eGFR <30'da kontrendikedir."},
            {"key": "C", "text": "Yalnızca böbrek nakli yapılan hastalarda serbesttir", "isCorrect": False, "explanation": "Kural GFR'ye bağlıdır."},
            {"key": "D", "text": "eGFR >90 olduğunda kesinlikle yasaktır", "isCorrect": False, "explanation": "Normal GFR'de kullanılabilir."}
        ])
    ]
    slides.append(make_slide(77, "Böbrek Yetmezliğinde Sistit: Toksisite ve Nitrofurantoin", "Loop diüretik+sefalosporin nefrotoksisitesi ve nitrofurantoin kontrendikasyon sınırı", "Özel Gruplarda Tedavi", s77_narrative, s77_bullets, s77_elements))

    # Slide 78: Erkekte Sistit: Nadirlik ve Tedavi (Pivmesilinam ve Nitrofurantoin)
    s78_narrative = (
        "Erkek anatomisinde üretra uzunluğu ve prostatik savunma nedeniyle lokalize alt üriner "
        "sistem enfeksiyonu (akut sistit) son derece nadir bir klinik tablodur.\n\n"
        "- **Klinik Nadirlik:** Lokalize üriner sistem enfeksiyonu **erkekte nadirdir**.\n"
        "- **Önerilen İki Ajan:** Genç erkekte prostat tutulumu dışlanmışsa ampirik olarak **pivmesilinam "
        "ve nitrofurantoin** önerilir.\n"
        "- **Prostatik Ayrım:** Eğer hastada prostat tutulumu (prostatit) şüphesi varsa bu ajanlar "
        "prostat dokusuna yeterince nüfuz edemez; bu nedenle pivmesilinam ve nitrofurantoin yalnızca "
        "prostat tutulumu dışlanmış yüzeyel sistit olgularında uygundur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Erkekte sistit nadirdir; genç erkekte prostat tutulumu dışlanmışsa ampirik olarak pivmesilinam ve nitrofurantoin önerilir."
    )
    s78_bullets = [
        "Lokalize ÜSE (sistit) erkekte nadirdir.",
        "Genç erkekte önerilen iki ajan: Pivmesilinam ve nitrofurantoin.",
        "Bu iki ajanın seçimi için prostat tutulumunun mutlaka dışlanmış olması gerekir."
    ]
    s78_elements = [
        make_cloze("Genç erkekte prostat tutulumu dışlandığında sistit tedavisinde pivmesilinam ve nitrofurantoin önerilir.", "pivmesilinam ve nitrofurantoin", "Erkekte sistit için önerilen iki spesifik antibiyotik"),
        make_table("Erkekte Sistit Tedavi Özellikleri", ["Klinik Özellik", "Tanımlayıcı Kural", "Gerekçe"], [
            {"cells": [{"text": "Sıklık", "isMasked": False}, {"text": "Erkekte sistit NADİRDİR", "isMasked": True, "hint": "seyrek görülen tablo"}, {"text": "Uzun üretra ve prostat sıvısı korur"}]},
            {"cells": [{"text": "Önerilen Ajanlar", "isMasked": False}, {"text": "Pivmesilinam ve nitrofurantoin", "isMasked": True, "hint": "iki spesifik ilaç"}, {"text": "Prostat tutulumu dışlanmışsa etkilidir"}]}
        ]),
        make_chain("Erkekte Sistit Karar Zinciri", [
            "1. Semptom Başvurusu: Erkek hastada dizüri ve pollaküri.",
            "2. Prostat Muayenesi: Dijital rektal muayene ile prostatitin dışlanması.",
            "3. İlaç Seçimi: Pivmesilinam veya nitrofurantoin başlanması.",
            "4. Tedavi Süresi: Sistemik belirti yoksa 5-7 gün sürdürülmesi."
        ]),
        make_recall("Ders notuna göre genç erkekte prostat tutulumu dışlanmışsa sistitte önerilen iki ajan nedir?", "Pivmesilinam ve nitrofurantoindir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erkekte Sistit", [
            {"text": "Lokalize ÜSE erkekte nadirdir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Genç erkekte pivmesilinam ve nitrofurantoin önerilir.", "isLie": False, "explanation": "Doğru. Önerilen iki ajandır."},
            {"text": "Erkekte sistit görüldüğünde prostat tutulumu araştırılmasına gerek yoktur.", "isLie": True, "explanation": "Tuzak! Erkekte prostat tutulumu mutlaka dışlanmalıdır."},
            {"text": "Erkekte sistit tedavisi sistemik belirti yoksa 5-7 gün sürer.", "isLie": False, "explanation": "Doğru. Süre kuralıdır."}
        ]),
        make_quiz("Lokalize üriner sistem enfeksiyonu saptanan ve prostat tutulumu dışlanmış genç bir erkek hastada sistit tedavisi için ders notunda önerilen ajanlar aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Pivmesilinam ve nitrofurantoin", "isCorrect": True, "explanation": "Ders notunda harfiyen 'genç erkekte pivmesilinam ve nitrofurantoin önerilir (prostat tutulumu dışlanmışsa)' denmektedir."},
            {"key": "B", "text": "Yalnızca intravenöz vankomisin", "isCorrect": False, "explanation": "Basit sistitte vankomisin verilmez."},
            {"key": "C", "text": "Ampisilin tek doz", "isCorrect": False, "explanation": "Aminopenisilinler direnç nedeniyle uygun değildir."},
            {"key": "D", "text": "Karbapenem 21 gün", "isCorrect": False, "explanation": "Aşırı ve gereksiz tedavidir."}
        ])
    ]
    slides.append(make_slide(78, "Erkekte Sistit: Pivmesilinam ve Nitrofurantoin", "Erkekte sistitin nadirliği, prostatit ayırımı ve pivmesilinam/nitrofurantoin kullanımı", "Özel Gruplarda Tedavi", s78_narrative, s78_bullets, s78_elements))

    # Slide 79: Sekizinci Bölüm Özeti: Sistit Tedavi Yaklaşımları
    s79_narrative = (
        "Akut sistit tedavisi; direnç eşikleri, ekolojik yan hasar riskleri, tedavi süreleri ve "
        "özel hasta gruplarının kuralları ile sekizinci bölümün temelini oluşturur.\n\n"
        "- **İlk Tercih ve Kısıtlar:** TMP-SXT 2x160/800 mg 5 gün (direnç <%20 ise); florokinolonlar "
        "yalnızca diğerleri kullanılamıyorsa; süre kadında 3-5 gün, erkekte 5-7 gündür.\n"
        "- **Uygunsuz ve Zararlı:** Aminopenisilinler yüksek E. coli direnci nedeniyle uygun değildir; "
        "ko-amoksilav ve sefalosporinler GSBL ve C. difficile yan hasarı nedeniyle önerilmez.\n"
        "- **Özel Gruplar:** Gebede penisilin/sefalosporin/fosfomisin/nitrofurantoin uygun, TMP-SXT "
        "1. ve son trimesterde önerilmez; nitrofurantoin eGFR <30'da kontrendikedir; erkekte pivmesilinam ve nitrofurantoin esastır.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] TMP-SXT <%20 dirençte 5 gün ilk tercihtir; aminopenisilinler dirençli, sefalosporinler yan hasarlıdır; gebede TMP-SXT kısıtlıdır; nitrofurantoin eGFR <30'da kontrendikedir; erkekte pivmesilinam/nitrofurantoin verilir."
    )
    s79_bullets = [
        "TMP-SXT 2x160/800 mg 5 gün (lokal direnç <%20 ise ilk tercih).",
        "Florokinolonlar kısıtlıdır; süre kadında 3-5 gün, erkekte 5-7 gündür.",
        "Aminopenisilinler direnç nedeniyle, sefalosporinler ekolojik yan hasar nedeniyle önerilmez.",
        "Gebede TMP-SXT ilk/son trimesterde önerilmez; nitrofurantoin eGFR <30'da kontrendikedir; erkekte pivmesilinam/nitrofurantoin."
    ]
    s79_elements = [
        make_cloze("Akut sistitte TMP-SXT lokal direnç <%20 ise 5 gün verilirken nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir.", "eGFR <30 mL/dk/1,73 m²'de", "Nitrofurantoinin böbrek yetmezliği sınırı"),
        make_table("8. Bölüm Sistit Tedavi Matrisi", ["İlaç / Grup", "Kullanım Durumu", "Klinik Şart / Uyarı"], [
            {"cells": [{"text": "TMP-SXT", "isMasked": False}, {"text": "İlk tercih (5 gün)", "isMasked": True, "hint": "standart rejim"}, {"text": "Lokal direnç <%20 olmalıdır"}]},
            {"cells": [{"text": "Aminopenisilinler", "isMasked": False}, {"text": "Ampirik UYGUN DEĞİL", "isMasked": False}, {"text": "Yüksek küresel E. coli direnci", "isMasked": True, "hint": "aşırı direnç oranı"}]},
            {"cells": [{"text": "Oral Sefalosporinler", "isMasked": False}, {"text": "Ampirik ÖNERİLMEZ", "isMasked": True, "hint": "tavsiye edilmeyen grup"}, {"text": "GSBL seçilimi ve C. difficile"}]},
            {"cells": [{"text": "Nitrofurantoin", "isMasked": False}, {"text": "Etkili sistit ajanı", "isMasked": False}, {"text": "eGFR <30'da KONTRENDİKE", "isMasked": True, "hint": "otuzun altında yasak"}]}
        ]),
        make_chain("Sistit Reçeteleme Algoritması", [
            "1. Direnç Değerlendirmesi: Yerel direnç <%20 ise TMP-SXT 5 gün.",
            "2. Yan Hasardan Kaçınma: Oral sefalosporin ve ko-amoksilavdan uzak durma.",
            "3. Gebelik/Böbrek Kontrolü: Gebede trimester ve eGFR <30 sınırına dikkat.",
            "4. Erkek Sistiti: Prostatit dışlanmışsa pivmesilinam/nitrofurantoin."
        ]),
        make_recall("Sekizinci bölümün temel ilaç ilkeleri olarak TMP-SXT direnç sınırı, sefalosporinlerin yan hasarı ve nitrofurantoin kontrendikasyon sınırı nedir?", "TMP-SXT direnç sınırı <%20; sefalosporinler GSBL ve C. difficile ekolojik hasarı yapar; nitrofurantoin ise eGFR <30 mL/dk/1,73 m²'de kontrendikedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 8 Özeti", [
            {"text": "TMP-SXT 2x160/800 mg 5 gün kullanılır (direnç <%20 ise).", "isLie": False, "explanation": "Doğru. İlk tercih rejimdir."},
            {"text": "Aminopenisilinler yüksek E. coli direnci nedeniyle ampirik uygun değildir.", "isLie": False, "explanation": "Doğru. Uygunsuz gruptur."},
            {"text": "Nitrofurantoin eGFR <30 olduğunda dozu 100 kat artırılarak güvenle verilir.", "isLie": True, "explanation": "Tuzak! Nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kesinlikle kontrendikedir."},
            {"text": "Erkekte prostat dışlanmışsa pivmesilinam ve nitrofurantoin önerilir.", "isLie": False, "explanation": "Doğru. Erkek sistit ajanlarıdır."}
        ]),
        make_quiz("Sekizinci bölümde işlenen sistit tedavi yaklaşımları değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Oral sefalosporinler ve ko-amoksilav ekolojik yan hasar yapmadıkları için ampirik sistitte ilk tercihtir", "isCorrect": True, "explanation": "Yanlış! Oral sefalosporinler ve ko-amoksilav ekolojik yan hasar (GSBL seçilimi ve C. difficile) nedeniyle ampirik sistitte önerilmez."},
            {"key": "B", "text": "TMP-SXT 2x160/800 mg 5 gün lokal direnç <%20 ise ilk tercihtir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Nitrofurantoin eGFR <30 mL/dk/1,73 m² düzeyinde kontrendikedir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Genç erkekte prostat tutulumu dışlandığında pivmesilinam ve nitrofurantoin önerilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(79, "Sekizinci Bölüm Özeti: Sistit Tedavi Yaklaşımları", "Sistit rejimi, florokinolon uyarısı, ekolojik yan hasar ve özel grupların özeti", "Bölüm Özeti", s79_narrative, s79_bullets, s79_elements))

    # Slide 80: [TEKRAR SAYFASI - CHECKPOINT 8] Akut Sistit Tedavisi ve Özel Gruplar
    s80_narrative = (
        "Bu tekrar sayfasında 8. Bölümde işlenen akut sistit tedavi rejimlerini, florokinolon uyarısını, "
        "ekolojik yan hasarı ve gebelik/böbrek/erkek özel gruplarını pekiştiriyoruz.\n\n"
        "- **İlk Tercih ve Süre:** TMP-SXT **2x160/800 mg 5 gün** (lokal direnç **<%20** ise); "
        "süre kadında **3-5 gün**, erkekte **5-7 gün**; florokinolonlar yalnızca diğerleri yoksa.\n"
        "- **Önerilmeyenler:** Aminopenisilinler (yüksek direnç); ko-amoksilav ve oral sefalosporinler "
        "(**ekolojik yan hasar: GSBL seçilimi ve C. difficile**).\n"
        "- **Özel Gruplar:** Gebede penisilin/sefalosporin/fosfomisin/nitrofurantoin uygun, **TMP-SXT "
        "G6PD, 1. ve son trimesterde önerilmez**; **nitrofurantoin eGFR <30'da kontrendike**; erkekte **pivmesilinam ve nitrofurantoin**.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 8] TMP-SXT 2x160/800 mg 5 gün (<%20 direnç); sefalosporinler GSBL/C. difficile yan hasarı yapar; gebede TMP-SXT ilk/son trimesterde yasak; nitrofurantoin eGFR <30'da kontrendike; erkekte pivmesilinam/nitrofurantoin."
    )
    s80_bullets = [
        "TMP-SXT 2x160/800 mg 5 gün (lokal direnç <%20 ise ilk tercih).",
        "Florokinolonlar kısıtlıdır; süre kadında 3-5 gün, erkekte 5-7 gün.",
        "Oral sefalosporinler ve ko-amoksilav ekolojik yan hasar (GSBL, C. diff) nedeniyle önerilmez.",
        "Gebede TMP-SXT ilk/son trimesterde önerilmez; nitrofurantoin eGFR <30'da kontrendikedir; erkekte pivmesilinam/nitrofurantoin."
    ]
    s80_elements = [
        make_cloze("Akut sistitte TMP-SXT dozu 2x160/800 mg 5 gün olup nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir.", "2x160/800 mg 5 gün", "TMP-SXT'nin standart sistit rejimi"),
        make_table("8. Bölüm Büyük Tekrar Tablosu", ["Tedavi / Grup", "Kriter / Doz / Sınır", "Temel Klinik Mesaj"], [
            {"cells": [{"text": "TMP-SXT Rejimi", "isMasked": False}, {"text": "2x160/800 mg 5 gün (direnç <%20)", "isMasked": True, "hint": "ilk tercih sistit kürü"}, {"text": "Lokal dirence bağımlı ilk seçenek"}]},
            {"cells": [{"text": "Ekolojik Yan Hasar", "isMasked": False}, {"text": "Oral sefalosporin ve ko-amoksilav", "isMasked": False}, {"text": "GSBL seçilimi ve C. difficile", "isMasked": True, "hint": "mikrobiyom yıkım tehlikesi"}]},
            {"cells": [{"text": "Gebelik Kısıtlaması", "isMasked": False}, {"text": "TMP-SXT ilk ve son trimesterde önerilmez", "isMasked": True, "hint": "gebelikteki TMP-SXT yasağı"}, {"text": "Teratojenite ve kernikterus riski"}]},
            {"cells": [{"text": "Böbrek Yetmezliği", "isMasked": False}, {"text": "Nitrofurantoin eGFR <30'da kontrendike", "isMasked": False}, {"text": "Nörotoksisite ve etkisizlik", "isMasked": True, "hint": "periferik sinir hasarı riski"}]},
            {"cells": [{"text": "Erkekte Sistit", "isMasked": False}, {"text": "Pivmesilinam ve nitrofurantoin", "isMasked": True, "hint": "erkek sistit iki ajanı"}, {"text": "Prostat tutulumu dışlanmışsa"}]}
        ]),
        make_chain("8. Bölüm Konsolidasyon Zinciri", [
            "1. İlk Basamak: TMP-SXT 2x160/800 mg 5 gün (direnç <%20 ise).",
            "2. Yan Hasar Uyarısı: Sefalosporinlerin GSBL ve C. difficile riski.",
            "3. Güvenlik Sınırları: Gebede TMP-SXT kısıtı ve eGFR <30'da nitrofurantoin yasağı.",
            "4. Erkek Yönetimi: Prostatit dışlandığında pivmesilinam/nitrofurantoin."
        ]),
        make_recall("Checkpoint 8: TMP-SXT'nin dozu ve süresi, sefalosporinlerin yan hasarı, gebede TMP-SXT kısıtlaması ve nitrofurantoinin kontrendikasyon eşiği nedir?", "TMP-SXT 2x160/800 mg 5 gün (<%20 direnç); sefalosporinler GSBL ve C. diff yan hasarı yapar; TMP-SXT gebede 1. ve son trimesterde önerilmez; nitrofurantoin eGFR <30'da kontrendikedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 8 Konsolidasyonu", [
            {"text": "TMP-SXT 2x160/800 mg doz ile 5 gün uygulanır (direnç <%20 ise).", "isLie": False, "explanation": "Doğru. 8. bölümün ilk kuralıdır."},
            {"text": "Oral sefalosporinler GSBL ve C. difficile riski nedeniyle ampirik önerilmez.", "isLie": False, "explanation": "Doğru. Ekolojik yan hasardır."},
            {"text": "Gebelikte TMP-SXT ilk ve son trimesterde en güvenli birinci seçenek ilaçtır.", "isLie": True, "explanation": "Tuzak! TMP-SXT gebelikte ilk ve son trimesterde ve G6PD eksikliğinde önerilmez."},
            {"text": "Nitrofurantoin eGFR <30 mL/dk/1,73 m²'de kontrendikedir.", "isLie": False, "explanation": "Doğru. Kesin kontrendikasyondur."}
        ]),
        make_quiz("8. Bölümün tamamı (Akut Sistit Tedavisi ve Özel Gruplar) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Nitrofurantoin diyaliz hastalarında ve eGFR <10 olduğunda sınırsızca verilebilen tek güvenli ilaçtır", "isCorrect": True, "explanation": "Yanlış! Nitrofurantoin eGFR <30 mL/dk/1,73 m² düzeyinde kesinlikle kontrendikedir."},
            {"key": "B", "text": "TMP-SXT 2x160/800 mg doz ile 5 gün uygulanır (lokal direnç <%20 ise)", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Oral sefalosporinler ve ko-amoksilav ekolojik yan hasar nedeniyle ampirik sistitte önerilmez", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Genç erkekte prostat tutulumu dışlandığında pivmesilinam ve nitrofurantoin önerilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(80, "[TEKRAR SAYFASI - CHECKPOINT 8] Akut Sistit Tedavisi ve Özel Gruplar", "8. Bölümün kapsamlı pekiştirmesi: sistit tedavisi, yan hasar, gebelik, böbrek yetmezliği ve erkek", "Bölüm Tekrarı", s80_narrative, s80_bullets, s80_elements))

    return slides
