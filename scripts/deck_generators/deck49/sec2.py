import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec2():
    slides = []
    
    # Slide 11: Endoservikal Polip: Tanım ve Morfoloji
    s11_narrative = (
        "Endoservikal polip, servikal kanalın mukus salgılayan mukozasından lümene doğru ekzofitik olarak büyüyen, "
        "kadın genital sisteminde oldukça sık karşılaşılan benign bir kitle lezyonudur.\n\n"
        "- **Makroskopik Morfoloji:** Endoservikal kanalda yerleşen küçük, sapsız nodüllerden servikal açıklıktan (eksternal os) "
        "dışarıya doğru sarkan büyük, lobüle polipoid kitlelere kadar değişken boyutlarda izlenebilir.\n"
        "- **Biyolojik Davranış:** Bu lezyonlar kesinlikle selim karakterdedir; neoplastik bir süreç olmayıp ==malign potansiyelleri yoktur==.\n"
        "- **Histolojik Kompozisyon:** Genişlemiş, mukus salgılayan endoservikal glandlar ile bunları çevreleyen ödemli ve vaskülarize "
        "fibröz stromadan meydana gelir; sıklıkla ikincil inflamatuvar infiltrasyon eşlik eder.\n\n"
        "> [!NOTE]\n"
        "> Endoservikal polipler tamamen selim lezyonlardır; serviks kanseri ile doğrudan biyolojik ilişkileri bulunmaz."
    )
    s11_bullets = [
        "Endoservikal kanalda gelişen benign ekzofitik lezyondur.",
        "Malign potansiyeli kesinlikle yoktur.",
        "Fibröz stroma ve mukus salgılayan bezlerden oluşur."
    ]
    s11_elements = [
        make_cloze("Endoservikal polip endoservikal kanal mukozasından lümene sarkan ekzofitik ve benign bir lezyondur.", "benign", "Selim huylu biyolojik davranış özelliği"),
        make_table("Endoservikal Polip Morfolojisi", ["Yapısal Eleman", "Histolojik Özellik", "Klinik Özellik"], [
            {"cells": [{"text": "Endoservikal Bezler", "isMasked": False}, {"text": "Mukus salgılayan genişlemiş kistik yapılar", "isMasked": True, "hint": "salgılayıcı glandüler yapılar"}, {"text": "Kanal içi mukus artışına katkıda bulunur"}]},
            {"cells": [{"text": "Fibröz Stroma", "isMasked": False}, {"text": "Damardan zengin ve ödemli bağ dokusu", "isMasked": False}, {"text": "Travmayla kolayca kanayabilir", "isMasked": True, "hint": "yüzeyel frajilite ve temas kanaması"}]}
        ]),
        make_chain("Endoservikal Polip Oluşum Aşamaları", [
            "1. Mukozal İnflamasyon: Endoservikal kanalda kronik irritasyon veya hormonal uyarı oluşur.",
            "2. Fokal Proliferasyon: Mukozal stroma ve endoservikal bezler fokal hiperplazi gösterir.",
            "3. Ekzofitik Büyüme: Kitle lümene doğru uzanarak saplı veya geniş tabanlı polip halini alır.",
            "4. Dışarı Sarkma: Büyüyen polip servikal açıklıktan vajinaya doğru prolabe olabilir."
        ]),
        make_recall("Endoservikal poliplerin malign transformasyon riski var mıdır?", "Hayır, endoservikal polipler tamamen benign lezyonlardır ve malign potansiyelleri yoktur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endoservikal Polip Özellikleri", [
            {"text": "Endoservikal polipler endoservikal kanalda yerleşen ekzofitik benign kitlelerdir.", "isLie": False, "explanation": "Doğru. Servikal kanal mukozasından gelişen selim lezyonlardır."},
            {"text": "Histolojisinde mukus salgılayan bezler ve fibröz stroma bulunur.", "isLie": False, "explanation": "Doğru. Temel histolojik mimari gland ve stromadan oluşur."},
            {"text": "Endoservikal poliplerin doğrudan invaziv kansere dönüşme malign potansiyeli çok yüksektir.", "isLie": True, "explanation": "Tuzak! Endoservikal polipler tamamen selimdir; malign potansiyelleri yoktur."},
            {"text": "Servikal os dışına sarkarak vajinal spekulum muayenesinde görülebilirler.", "isLie": False, "explanation": "Doğru. Dış ağızdan sarkan polipoid kitleler oluşturabilirler."}
        ]),
        make_quiz("Endoservikal polip ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Malign potansiyeli olmayan benign ekzofitik bir lezyondur", "isCorrect": True, "explanation": "Endoservikal polipler tamamen benign olup malign potansiyel taşımazlar."},
            {"key": "B", "text": "Yalnızca kemoterapi ile gerileyebilen yüksek dereceli neoplazidir", "isCorrect": False, "explanation": "Neoplastik malignite değildir, basit cerrahiyle çıkarılır."},
            {"key": "C", "text": "Sarkomatoz dokudan oluşan ve retroperitona yayılan bir tümördür", "isCorrect": False, "explanation": "Uzak yayılım yapmaz, selim mukozal poliptir."},
            {"key": "D", "text": "Hiçbir zaman endoservikal bez içermeyen sırf lipom dokusudur", "isCorrect": False, "explanation": "Müsin salgılayan endoservikal bezler ve stroma içerir."}
        ])
    ]
    slides.append(make_slide(11, "Endoservikal Polip: Tanım ve Morfoloji", "Kanal içi ekzofitik büyüme, histoloji ve selim biyolojik karakter", "Benign Serviks Lezyonları", s11_narrative, s11_bullets, s11_elements))

    # Slide 12: Endoservikal Polip: Klinik Önemi ve Düzensiz Kanama
    s12_narrative = (
        "Endoservikal polipler biyolojik olarak tamamen iyi huylu olmalarına karşın, oluşturdukları klinik belirtiler "
        "nedeniyle jinekolojik pratikte serviks kanseri ile karışabilen önemli lezyonlardır.\n\n"
        "- **Klinik Belirtiler:** En sık yol açtıkları semptom, yüzeyel erezyon ve ülserasyona bağlı olarak gelişen "
        "**düzensiz vajinal kanama (metroraji)** veya cinsel ilişki sonrası temas kanamasıdır (postkoital kanama).\n"
        "- **Malignite Şüphesi:** Kanama semptomu ileri yaştaki kadınlarda ve postmenopozal dönemde ilk olarak "
        "invaziv serviks veya endometrium karsinomunu akla getirir; bu nedenle klinik şüphe uyandırır.\n"
        "- **İnflamasyon:** Polip yüzeyi vajinal bakteriyel ortama maruz kaldığında ülsere olur ve yoğun nötrofilik infiltrasyon gelişir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Endoservikal polipin klinik önemi maligniteye dönüşmesi değil, kanama yaparak serviks kanseri şüphesi doğurmasıdır."
    )
    s12_bullets = [
        "Yüzeyel ülserasyon düzensiz vajinal kanamaya yol açar.",
        "Postkoital veya intermenstrüel kanama karsinom şüphesi doğurur.",
        "Ayırıcı tanıda histopatolojik doğrulama zorunludur."
    ]
    s12_elements = [
        make_cloze("Endoservikal polipler yüzeyel ülserasyon nedeniyle düzensiz vajinal kanama oluşturarak serviks kanseri şüphesi doğurabilir.", "vajinal kanama", "Polipin yüzey erozyonuna bağlı ortaya çıkan klinik semptom"),
        make_table("Endoservikal Polipte Kanama Mekanizması", ["Aşama", "Fizyopatolojik Süreç", "Klinik Yansıması"], [
            {"cells": [{"text": "Yüzeyel Ülserasyon", "isMasked": False}, {"text": "Polip yüzeyindeki ince epitelin mekanik sürtünmeyle aşınması", "isMasked": True, "hint": "epitelyal bütünlüğün bozulması"}, {"text": "Mikroskobik kılcal damar açığa çıkar"}]},
            {"cells": [{"text": "Temas Kanaması", "isMasked": False}, {"text": "İlişki veya muayene ile frajil damarların kanaması", "isMasked": False}, {"text": "Postkoital kanama ve hekime başvuru", "isMasked": True, "hint": "ilişki sonrası lekelenme semptomu"}]}
        ]),
        make_chain("Endoservikal Polipten Tanıya Gidiş", [
            "1. Vasküler Frajilite: Endoservikal polip stromasındaki damarlar mekanik travmayla açılır.",
            "2. Kanama Belirtisi: Hasta düzensiz lekelenme veya ilişki sonrası kanama şikayetiyle başvurur.",
            "3. Spekulum Muayenesi: Servikal açıklıktan sarkan kırmızı, yumuşak polipoid kitle gözlenir.",
            "4. Biyopsi/Eksizyon: Karsinomu dışlamak amacıyla polip çıkarılarak patolojiye gönderilir."
        ]),
        make_recall("Endoservikal polipin klinikte en çok korkutan ve hekime başvurmayı sağlayan prezentasyonu nedir?", "Yüzeyel ülserasyona bağlı gelişen düzensiz vajinal kanamadır (karsinom taklidi)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endoservikal Polipin Klinik Tablosu", [
            {"text": "Endoservikal polipler yüzey ülserasyonuyla düzensiz kanamaya neden olabilir.", "isLie": False, "explanation": "Doğru. En tipik klinik prezentasyon kanamadır."},
            {"text": "Oluşan kanama klinisyende serviks veya endometrium kanseri şüphesi uyandırabilir.", "isLie": False, "explanation": "Doğru. Kanser ayırıcı tanısında ilk sıralarda araştırılır."},
            {"text": "Endoservikal polipler daima kemik iliğini infiltre ederek pansitopeni yapar.", "isLie": True, "explanation": "Tuzak! Polip lokal selim bir lezyondur, kemik iliği tutulumu veya sitopeni yapmaz."},
            {"text": "İnflamasyon ve vasküler konjesyon polip yüzeyinde frajiliteyi artırır.", "isLie": False, "explanation": "Doğru. Ödemli ve vaskülarize stroma kolayca kanar."}
        ]),
        make_quiz("Endoservikal poliplerin klinik açıdan en büyük önemi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Ülserasyon ve kanama sonucu malign lezyon şüphesi oluşturması", "isCorrect": True, "explanation": "Düzensiz kanama karsinom şüphesi yarattığı için klinikte büyük önem taşır."},
            {"key": "B", "text": "Hastalarda daima bilateral plevral efüzyona yol açması", "isCorrect": False, "explanation": "Akciğer veya plevra ile hiçbir ilgisi yoktur."},
            {"key": "C", "text": "Birkaç hafta içinde anaplastik metastatik tümöre dönüşmesi", "isCorrect": False, "explanation": "Malign potansiyeli yoktur, selim kalır."},
            {"key": "D", "text": "Sadece erkeklerde görülen bir gonadal tümör olması", "isCorrect": False, "explanation": "Serviks kadın genital organıdır."}
        ])
    ]
    slides.append(make_slide(12, "Endoservikal Polip: Klinik Önemi ve Düzensiz Kanama", "Ülserasyon, metroraji, postkoital kanama ve malignite ayırıcı tanısı", "Klinik Ayırıcı Tanı", s12_narrative, s12_bullets, s12_elements))

    # Slide 13: Endoservikal Polip: Tedavi ve Patolojik İnceleme
    s13_narrative = (
        "Endoservikal polip saptanan olgularda yaklaşım hem semptomun giderilmesini hem de kanamanın "
        "gerçek nedeninin kanıtlanmasını amaçlayan cerrahi eksizyondur.\n\n"
        "- **Tedavi Yöntemi:** Standart yaklaşım **polipektomi** (basit cerrahi eksizyon veya polip tabanına küretaj) uygulanmasıdır; "
        "genellikle poliklinik şartlarında anestezi gerektirmeden uygulanabilen küratif bir işlemdir.\n"
        "- **Histolojik Doğrulama Zorunluluğu:** Çıkarılan her polip mutlaka patolojik incelemeye gönderilmelidir; "
        "çünkü serviksin gerçek malign lezyonları (özellikle ekzofitik karsinomlar) bazen polipoid kitle taklidi yapabilir.\n"
        "- **Nüks:** Tamamen çıkarılan poliplerde nüks nadirdir; hastanın kanama semptomu işlem sonrası hızla geriler.\n\n"
        "> [!NOTE]\n"
        "> Basit küretaj veya polipektomi küratiftir; histolojik inceleme maligniteyi kesin olarak dışlamak için şarttır."
    )
    s13_bullets = [
        "Tedavide basit küretaj veya cerrahi eksizyon (polipektomi) küratiftir.",
        "Çıkarılan materyalin histolojik incelemesi maligniteyi dışlamak için zorunludur.",
        "Karsinomlar bazen polipoid büyüme paterni gösterebilir."
    ]
    s13_elements = [
        make_cloze("Endoservikal polip tedavisinde uygulanan basit küretaj veya cerrahi eksizyon işlemi polipektomi olarak adlandırılır.", "polipektomi", "Polipin cerrahi olarak çıkarılması işlemi"),
        make_table("Endoservikal Polip Yönetimi", ["Basamak", "Yapılan İşlem", "Temel Amaç"], [
            {"cells": [{"text": "Cerrahi Girişim", "isMasked": False}, {"text": "Basit forseps ile burkma veya taban küretajı", "isMasked": True, "hint": "polipin tabanından ayrılması"}, {"text": "Lezyonun tamamen vücuttan uzaklaştırılması"}]},
            {"cells": [{"text": "Patoloji İncelemesi", "isMasked": False}, {"text": "Rutin kesit alma ve mikroskobik inceleme", "isMasked": False}, {"text": "Gerçek karsinom varlığını ekarte etmek", "isMasked": True, "hint": "maligniteyi kesin dışlama gereği"}]}
        ]),
        make_chain("Endoservikal Polip Tedavi Süreci", [
            "1. Teşhis: Spekulum muayenesinde eksternal os seviyesinde polip saptanır.",
            "2. Polipektomi: Polip tabanından yakalanarak burulur veya küretajla eksize edilir.",
            "3. Fiksasyon: Örnek formaldehite konularak patoloji laboratuvarına gönderilir.",
            "4. Mikroskopi: Stromal ödem ve bezler doğrulanır, malignite dışlanarak tam kür sağlanır."
        ]),
        make_recall("Endoservikal polip çıkarıldıktan sonra mutlaka patolojiye gönderilmesinin temel nedeni nedir?", "Ekzofitik serviks kanserlerinin polip taklidi yapabilmesi nedeniyle maligniteyi kesin olarak dışlamaktır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Endoservikal Polip Tedavisi", [
            {"text": "Basit küretaj veya eksizyon genellikle polip tedavisinde küratiftir.", "isLie": False, "explanation": "Doğru. Basit polipektomi yeterli tedavidir."},
            {"text": "Çıkarılan lezyonun patolojik incelemesi maligniteyi dışlamak için yapılır.", "isLie": False, "explanation": "Doğru. Ekzofitik kanserleri dışlamak şarttır."},
            {"text": "Her endoservikal polip hastasına acil radikal histerektomi ve pelvik radyoterapi verilmelidir.", "isLie": True, "explanation": "Tuzak! Polip benign bir lezyondur; radikal histerektomi veya radyoterapi gerekmez."},
            {"text": "İşlem sonrası hastanın kanama şikayeti genellikle düzelir.", "isLie": False, "explanation": "Doğru. Kanama odağı ortadan kalktığı için semptom geriler."}
        ]),
        make_quiz("Endoservikal polip tedavisi ve yönetimi ile ilgili aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Basit cerrahi eksizyon küratiftir ve maligniteyi dışlamak için histolojik inceleme şarttır", "isCorrect": True, "explanation": "Polipektomi yeterlidir ve patolojik değerlendirme karsinomu dışlamak için gereklidir."},
            {"key": "B", "text": "Polipler hiçbir zaman cerrahi olarak çıkarılmamalı, ömür boyu beklenmelidir", "isCorrect": False, "explanation": "Kanama yaptığı ve karsinomu ekarte etmek gerektiği için çıkarılır."},
            {"key": "C", "text": "Tek etkili tedavi yöntemi yüksek doz sistemik immünsüpresyondur", "isCorrect": False, "explanation": "İmmünsüpresyonun tedavide yeri yoktur."},
            {"key": "D", "text": "Polip çıkarıldığında doku doğrudan çöpe atılmalı, mikroskopta bakılmamalıdır", "isCorrect": False, "explanation": "Maligniteyi dışlamak için mikroskobik inceleme zorunludur."}
        ])
    ]
    slides.append(make_slide(13, "Endoservikal Polip: Tedavi ve Patolojik İnceleme", "Polipektomi, küretaj, histopatolojik konfirmasyon ve küratif yaklaşım", "Cerrahi ve Patolojik Yönetim", s13_narrative, s13_bullets, s13_elements))

    # Slide 14: Serviks Epitelyal Mimarisi: Ektoserviks ve Endoserviks
    s14_narrative = (
        "Serviks karsinogenezini anlayabilmek için ektoserviks ile endoservikal kanalın normal epitelyal "
        "örtüleri arasındaki histolojik zıtlığın çok iyi bilinmesi gerekir.\n\n"
        "- **Ektoserviks:** Vajinaya komşu olan dış servikal yüzeydir; mekanik travmaya dayanıklı, glikojenden zengin, "
        "**keratinize olmayan çok katlı yassı (skuamöz) epitel** ile döşelidir.\n"
        "- **Endoserviks:** Uterusa doğru uzanan servikal kanaldır; lümene alkalen mukus salgılayan "
        "**tek katlı kolumnar (prizmatik) epitel** tabakası ile kaplıdır ve kleft benzeri dallanan glandüler yapılar içerir.\n"
        "- **Fonksiyonel Ayrım:** Ektoserviks koruyucu mekanik bir bariyer sağlarken, endoserviks vajinal asiditeye karşı mukus tıkacı üreterek "
        "asendan enfeksiyonlara karşı koruma sağlar.\n\n"
        "> [!NOTE]\n"
        "> Ektoserviks çok katlı yassı epitel, endoserviks ise tek katlı mukus salgılayan kolumnar epitel ile karakterizedir."
    )
    s14_bullets = [
        "Ektoserviks çok katlı keratinize olmayan yassı epitel ile döşelidir.",
        "Endoserviks tek katlı mukus salgılayan kolumnar epitel ile örtülüdür.",
        "İki epitelin karşılaşma hattı servikal patolojilerin başlangıç merkezidir."
    ]
    s14_elements = [
        make_cloze("Endoservikal kanal mukozası lümene mukus salgılayan tek katlı kolumnar epitel ile döşelidir.", "kolumnar", "Endoserviksi döşeyen silindirik/prizmatik epitel türü"),
        make_table("Servikal Epitel Kompartmanları Karşılaştırması", ["Anatomik Bölge", "Epitel Tipi", "Temel Görevi"], [
            {"cells": [{"text": "Ektoserviks", "isMasked": False}, {"text": "Çok katlı keratinize olmayan skuamöz epitel", "isMasked": True, "hint": "vajinaya komşu yassı epitel"}, {"text": "Mekanik travma ve sürtünmeye direnç"}]},
            {"cells": [{"text": "Endoserviks", "isMasked": False}, {"text": "Tek katlı mukus salgılayan prizmatik epitel", "isMasked": False}, {"text": "Mukus tıkacı ile mikroorganizma girişini engelleme", "isMasked": True, "hint": "bakteriyel asendan yayılıma bariyer"}]}
        ]),
        make_chain("Servikal Epitel Dağılım Düzeni", [
            "1. Vajinal Devamlılık: Vajina kubbesinden ektoservikse kesintisiz çok katlı yassı epitel uzanır.",
            "2. Kanal Girişi: Eksternal os hizasında skuamöz epitel kolumnar epitel ile karşılaşır.",
            "3. Kanal Döşemesi: Endoserviks boyunca tek katlı müsinöz prizmatik epitel lümeni örter.",
            "4. İnternal Os: Kanal yukarıda endometriyal gland ve stromaya geçiş yapar."
        ]),
        make_recall("Ektoserviks ile endoservikal kanal arasındaki temel histolojik epitel farkı nedir?", "Ektoserviks çok katlı yassı epitel ile, endoserviks ise tek katlı mukus salgılayan kolumnar epitel ile döşelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Serviks Epitel Mimarisi", [
            {"text": "Ektoserviks çok katlı skuamöz epitel ile döşelidir.", "isLie": False, "explanation": "Doğru. Mekanik travmaya dirençli yassı epiteldir."},
            {"text": "Endoserviks tek katlı mukus salgılayan kolumnar epitel ile kaplıdır.", "isLie": False, "explanation": "Doğru. Müsinöz prizmatik hücreler içerir."},
            {"text": "Ektoserviks kemik iliği ve çizgili kas liflerinden oluşan bir glanddır.", "isLie": True, "explanation": "Tuzak! Ektoserviks kas veya ilik değil, çok katlı yassı epitelle döşeli mukozal yüzeydir."},
            {"text": "İki epitel arasındaki sınır skuamo-kolumnar bileşkedir.", "isLie": False, "explanation": "Doğru. Geçiş hattına bu isim verilir."}
        ]),
        make_quiz("Ektoserviksin normal histolojik epitelyal döşemesi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Çok katlı keratinize olmayan yassı (skuamöz) epitel", "isCorrect": True, "explanation": "Ektoserviks çok katlı keratinize olmayan yassı epitel ile örtülüdür."},
            {"key": "B", "text": "Tek katlı silli silindirik epitel", "isCorrect": False, "explanation": "Bu tuba uterinaya özgüdür."},
            {"key": "C", "text": "Değişici epitel (ürotelyum)", "isCorrect": False, "explanation": "Üriner sisteme özgü epiteldir."},
            {"key": "D", "text": "Keratinize çok katlı prizmatik epitel", "isCorrect": False, "explanation": "Ektoserviks yassı epiteldir, prizmatik değildir."}
        ])
    ]
    slides.append(make_slide(14, "Serviks Epitelyal Mimarisi: Ektoserviks ve Endoserviks", "Çok katlı skuamöz epitel, mukus salgılayan kolumnar epitel ve mukozal bariyer", "Serviks Histolojisi", s14_narrative, s14_bullets, s14_elements))

    # Slide 15: Skuamo-Kolumnar Bileşke (SKB) ve Dinamik Konumu
    s15_narrative = (
        "Skuamo-kolumnar bileşke (SKB), ektoserviksin çok katlı yassı epiteli ile endoserviksin tek katlı kolumnar epitelinin "
        "birbirine komşu olduğu keskin histolojik geçiş hattıdır.\n\n"
        "- **Dinamik Bir Sınır:** Bu bileşke sabit anatomik bir çizgi değildir; kadının yaşına, gebelik durumuna ve "
        "kandaki **hormonal düzeylere (özellikle östrojen)** bağlı olarak yaşam boyu yer değiştirir.\n"
        "- **Yenidoğan ve Çocukluk:** Çocukluk çağında bileşke genellikle endoservikal kanalın içindedir veya eksternal os düzeyindedir.\n"
        "- **Hormonal Etki:** Puberte ve üreme çağında artan östrojen etkisiyle serviks hacmi artar ve bu durum bileşkenin "
        "dışarıya, vajinal ortama doğru kaymasına zemin hazırlar.\n\n"
        "> [!NOTE]\n"
        "> Skuamo-kolumnar bileşkenin anatomik konumu sabit olmayıp yaş ve hormonal duruma bağlı olarak sürekli değişir."
    )
    s15_bullets = [
        "SKB, skuamöz epitel ile kolumnar epitelin buluştuğu sınırdır.",
        "Sabit bir hat olmayıp yaş ve hormonal duruma göre dinamik olarak yer değiştirir.",
        "Östrojen uyarısı bileşkenin konumunu belirleyen temel etkendir."
    ]
    s15_elements = [
        make_cloze("Endoservikal ve ektoservikal epitelin birleştiği sınıra skuamo-kolumnar bileşke adı verilir.", "skuamo-kolumnar bileşke", "Yassı ve silindirik epitelin kesişme hattı"),
        make_table("Skuamo-Kolumnar Bileşkenin Yaş Dönemlerine Göre Konumu", ["Dönem", "Bileşkenin Konumu", "Hormonal Durum"], [
            {"cells": [{"text": "Çocukluk / Postmenopoz", "isMasked": False}, {"text": "Endoservikal kanal içine çekilmiş", "isMasked": True, "hint": "kanal içi yerleşim"}, {"text": "Düşük östrojen seviyesi"}]},
            {"cells": [{"text": "Puberte / Üreme Çağı", "isMasked": False}, {"text": "Ektoservikse doğru dışarı kaymış", "isMasked": False}, {"text": "Yüksek östrojen stimülasyonu", "isMasked": True, "hint": "aktif over hormon etkisi"}]}
        ]),
        make_chain("Bileşkenin Dinamik Hareketi", [
            "1. Menarş ve Puberte: Overlerden östrojen salgılanması belirgin şekilde artar.",
            "2. Servikal Hacim Artışı: Servikal doku büyür ve endoservikal mukoza dışarıya doğru sarkar.",
            "3. Bileşke Göçü: Skuamo-kolumnar bileşke eksternal os dışına, ektoservikal alana kayar.",
            "4. Asidik Temas: Açığa çıkan kolumnar epitel vajinal asit pH ile doğrudan temas eder."
        ]),
        make_recall("Skuamo-kolumnar bileşkenin (SKB) serviksteki konumu neden sabit değildir?", "Kadının yaşına ve kandaki östrojen hormonunun seviyesine bağlı olarak serviksin anatomik hacmiyle birlikte yer değiştirir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Skuamo-Kolumnar Bileşke Dinamiği", [
            {"text": "SKB ektoservikal skuamöz ile endoservikal kolumnar epitelin buluştuğu sınırdır.", "isLie": False, "explanation": "Doğru. İki epitelin geçiş hattıdır."},
            {"text": "Bileşkenin konumu yaş ve hormonal duruma bağlı olarak değişkenlik gösterir.", "isLie": False, "explanation": "Doğru. Statik değil dinamiktir."},
            {"text": "SKB anne karnında kemikleşerek ömür boyu kafatasına fikse kalan bir yapıdır.", "isLie": True, "explanation": "Tuzak! SKB servikste yer alan mikroskobik mukozal bir sınırdır, kemikle ilişkisi yoktur."},
            {"text": "Üreme çağında östrojen etkisiyle bileşke vajinaya doğru eversiyona uğrayabilir.", "isLie": False, "explanation": "Doğru. Dışarıya doğru kayma tipiktir."}
        ]),
        make_quiz("Skuamo-kolumnar bileşkenin (SKB) anatomik konumu ile ilgili aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Yaş ve hormonal faktörlere bağlı olarak yaşam boyunca dinamik biçimde yer değiştirir", "isCorrect": True, "explanation": "Östrojen ve yaş bileşkenin kanal içinde veya dışında olmasını belirler."},
            {"key": "B", "text": "Doğumdan ölüme kadar milimetrik olarak tamamen hareketsiz ve sabittir", "isCorrect": False, "explanation": "Dinamiktir, sürekli yer değiştirir."},
            {"key": "C", "text": "Yalnızca menopozdan sonra aniden ortaya çıkan patolojik bir fibröz banttır", "isCorrect": False, "explanation": "Fizyolojik normal bir epitel sınırıdır."},
            {"key": "D", "text": "Sadece erkeklerde mesane boynunda bulunan bir yapıdır", "isCorrect": False, "explanation": "Uterus serviksine özgü bir yapıdır."}
        ])
    ]
    slides.append(make_slide(15, "Skuamo-Kolumnar Bileşke (SKB) ve Dinamik Konumu", "Epitel sınırı, östrojen regülasyonu, yaşa bağlı anatomik kaymalar", "Serviks Morfofizyolojisi", s15_narrative, s15_bullets, s15_elements))

    # Slide 16: Ergenlikte Eversiyon ve Skuamöz Metaplazi
    s16_narrative = (
        "Ergenlik döneminde östrojen seviyesinin yükselmesiyle birlikte endoservikal kanal genişler ve "
        "tek katlı kolumnar epitel dışarıya, ektoservikal alana doğru sarkar; bu duruma **eversiyon (ektropion)** denir.\n\n"
        "- **Vajinal Asidik Ortam:** Vajinanın normal pH'sı (3.8-4.5) asidiktir; oysa tek katlı kolumnar epitel bu asidik "
        "ve mekanik çevreye karşı son derece hassastır.\n"
        "- **Skuamöz Metaplazi:** Kolumnar epitelin altındaki indiferansiye rezerv hücreleri prolifere olarak "
        "kolumnar hücrelerin yerine asite dirençli **çok katlı yassı (skuamöz) epitele** dönüşür; bu koruyucu adaptif sürece skuamöz metaplazi denir.\n"
        "- **Fizyolojik Korunma:** Metaplazi bir kanser değildir; dokuyu asidik çevre travmasından korumayı amaçlayan fizyolojik bir adaptasyondur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ergenlikte eversiyon sonucu açığa çıkan kolumnar epitel, vajinal asiditeye yanıt olarak koruyucu skuamöz metaplaziye uğrar."
    )
    s16_bullets = [
        "Ergenlikte hormonal etkiyle eversiyon (ektropion) gelişir.",
        "Açığa çıkan kolumnar epitel vajinal asit pH ile temas eder.",
        "Rezerv hücrelerin farklılaşmasıyla fizyolojik skuamöz metaplazi gerçekleşir."
    ]
    s16_elements = [
        make_cloze("Ergenlikte endoservikal kolumnar epitelin vajinal ortama kaymasına eversiyon adı verilir.", "eversiyon", "Endoservikal mukozanın dışarıya dönmesi/sarkması"),
        make_table("Eversiyon ve Skuamöz Metaplazi Aşamaları", ["Basamak", "Hücresel Süreç", "Biyolojik Anlam"], [
            {"cells": [{"text": "Eversiyon (Ektropion)", "isMasked": False}, {"text": "Kolumnar epitelin ektoservikse taşması", "isMasked": True, "hint": "mukozanın dışarıya dönmesi"}, {"text": "Hassas bez hücreleri vajinal aside maruz kalır"}]},
            {"cells": [{"text": "Skuamöz Metaplazi", "isMasked": False}, {"text": "Rezerv hücrelerden yassı epitel gelişimi", "isMasked": False}, {"text": "Dirençli çok katlı koruyucu tabaka oluşur", "isMasked": True, "hint": "asite dayanıklı adaptasyon"}]}
        ]),
        make_chain("Eversiyondan Metaplaziye İlerleyiş", [
            "1. Hormonal Yükseliş: Pubertede östrojen uyarısıyla serviks hacmi artar.",
            "2. Dışarı Sarkma (Eversiyon): Tek katlı endoservikal epitel ektoservikal alana kayar.",
            "3. Asit Hasarı: Vajinal asidite kolumnar hücrelerde mikro-erozyon ve hasar yaratır.",
            "4. Rezerv Hücre Yanıtı: Subkolumnar rezerv hücreler bölünerek çok katlı skuamöz metaplazi oluşturur."
        ]),
        make_recall("Ergenlikte eversiyonla dışarı açılan endoservikal epitelde hangi adaptif hücresel dönüşüm gerçekleşir?", "Vajinal asidik ortama karşı koruyucu bir yanıt olarak skuamöz metaplazi gerçekleşir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Eversiyon ve Skuamöz Metaplazi", [
            {"text": "Ergenlikte kolumnar epitelin ektoservikse doğru kaymasına eversiyon denir.", "isLie": False, "explanation": "Doğru. Hormonal büyümeyle dışarı taşmadır."},
            {"text": "Vajinal asidik çevreye karşı koruyucu olarak skuamöz metaplazi gelişir.", "isLie": False, "explanation": "Doğru. Metaplazi koruyucu bir adaptasyondur."},
            {"text": "Skuamöz metaplazi gelişen her kadında 24 saat içinde kemik sarkomu gelişmesi kaçınılmazdır.", "isLie": True, "explanation": "Tuzak! Skuamöz metaplazi fizyolojik ve benign bir adaptasyondur; sarkomla hiçbir ilişkisi yoktur."},
            {"text": "Metaplazi subkolumnar rezerv hücrelerin prolifere olup farklılaşmasıyla oluşur.", "isLie": False, "explanation": "Doğru. Rezerv hücreler kaynak dokudur."}
        ]),
        make_quiz("Ergenlikte eversiyon sonucu açığa çıkan kolumnar epitelde gelişen temel hücresel değişim nedir?", [
            {"key": "A", "text": "Vajinal asidik ortama karşı koruyucu skuamöz metaplazi gelişmesi", "isCorrect": True, "explanation": "Asidik ortama yanıt olarak dirençli yassı epitel (metaplazi) gelişir."},
            {"key": "B", "text": "Hücrelerin kıkırdak dokusuna dönüşerek serviksi tıkaması", "isCorrect": False, "explanation": "Kondroid metaplazi görülmez."},
            {"key": "C", "text": "Tüm epitelin eriyerek tamamen peritona dökülmesi", "isCorrect": False, "explanation": "Epitel erimez, tam aksine çok katlılaşarak kalınlaşır."},
            {"key": "D", "text": "Doğrudan yüksek dereceli anaplastik rabdomiyosarkoma dönüşmesi", "isCorrect": False, "explanation": "Metaplazi selim adaptif bir süreçtir."}
        ])
    ]
    slides.append(make_slide(16, "Ergenlikte Eversiyon ve Skuamöz Metaplazi", "Ektropion, asidik vajinal pH, rezerv hücre aktivasyonu ve adaptif dönüşüm", "Metaplazik Adaptasyon", s16_narrative, s16_bullets, s16_elements))

    # Slide 17: Transformasyon Bölgesi (Zonu): Tanım ve Önemi
    s17_narrative = (
        "Orijinal skuamo-kolumnar bileşke ile yeni oluşan skuamo-kolumnar bileşke arasında kalan ve "
        "skuamöz metaplaziye uğramış epitel içeren alana **Transformasyon Bölgesi (TZ - Zonu)** adı verilir.\n\n"
        "- **Hücresel İçerik:** Bu zon henüz tam matüre olmamış, hızlı bölünme yeteneğinde ve aktif transkripsiyon "
        "yapan genç metaplastik skuamöz hücrelerden meydana gelir.\n"
        "- **Naboth Kistleri:** Skuamöz metaplazi yüzeyi örterken alttaki endoservikal kleftlerin ağzını kapatabilir; "
        "salgılanan mukus birikerek benign **Naboth kistlerini** oluşturur.\n"
        "- **Klinik Muayene:** Kolposkopi ve Pap smear taramalarında görselleştirilmesi ve örneklenmesi zorunlu olan alandır.\n\n"
        "> [!NOTE]\n"
        "> Transformasyon bölgesi, eversiyona uğramış kolumnar epitelin skuamöz metaplazi ile kaplandığı dinamik sahadır."
    )
    s17_bullets = [
        "Orijinal ve yeni SKB arasındaki metaplastik alandır.",
        "Hızla bölünen genç, olgunlaşmamış skuamöz hücreler içerir.",
        "Kleft ağızlarının tıkanmasıyla selim Naboth kistleri gelişebilir."
    ]
    s17_elements = [
        make_cloze("Orijinal SKB ile yeni SKB arasında skuamöz metaplazinin gerçekleştiği sahaya transformasyon bölgesi adı verilir.", "transformasyon bölgesi", "Metaplastik epitelin yerleştiği anatomik zon"),
        make_table("Transformasyon Bölgesi Anatomik Unsurları", ["Yapı", "Histolojik Karakteri", "Önemi"], [
            {"cells": [{"text": "Metaplastik Epitel", "isMasked": False}, {"text": "Hızla çoğalan immatür skuamöz hücreler", "isMasked": True, "hint": "bölünme yeteneği yüksek genç epitel"}, {"text": "Onkojenik ajanlara en açık hücresel hedef"}]},
            {"cells": [{"text": "Naboth Kistleri", "isMasked": False}, {"text": "Mukus retansiyonuna bağlı genişlemiş glandlar", "isMasked": False}, {"text": "Metaplazinin eşlik ettiği tamamen benign kistler", "isMasked": True, "hint": "selim mukozal retansiyon kistleri"}]}
        ]),
        make_chain("Transformasyon Zonu ve Naboth Kisti Oluşumu", [
            "1. Yüzeyel Metaplazi: Transformasyon bölgesinde skuamöz epitel yüzeyi hızla örter.",
            "2. Kanal Tıkanması: Alttaki endoservikal gland kleftlerinin ağızları yassı epitel ile kapanır.",
            "3. Mukus Birikimi: Derindeki glandüler hücreler mukus salgılamaya devam eder.",
            "4. Naboth Kisti: Lümen genişleyerek makroskopik sarı-beyaz renkli selim retansiyon kistleri belirir."
        ]),
        make_recall("Transformasyon bölgesinde endoservikal bez ağızlarının skuamöz metaplazi ile tıkanması sonucu hangi selim yapılar oluşur?", "Naboth retansiyon kistleri oluşur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Transformasyon Bölgesi", [
            {"text": "Transformasyon bölgesi skuamöz metaplazinin gerçekleştiği sahadır.", "isLie": False, "explanation": "Doğru. Metaplazik aktivite bu alandadır."},
            {"text": "Bu alanda olgunlaşmamış genç skuamöz hücreler bulunur.", "isLie": False, "explanation": "Doğru. Proliferatif rezerv hücreler ön plandadır."},
            {"text": "Transformasyon bölgesi sadece kalpte bulunan koroner bir damar ağıdır.", "isLie": True, "explanation": "Tuzak! Transformasyon zonu servikse özgü bir epitel sahasıdır; kalple ilgisi yoktur."},
            {"text": "Gland ağızlarının örtülmesiyle selim Naboth kistleri meydana gelebilir.", "isLie": False, "explanation": "Doğru. Mukus hapsolarak kist oluşturur."}
        ]),
        make_quiz("Transformasyon bölgesi (zonu) ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Eversiyona uğramış alanda immatür skuamöz metaplazinin geliştiği dinamik sahadır", "isCorrect": True, "explanation": "Orijinal ve yeni SKB arasındaki metaplastik sahadır."},
            {"key": "B", "text": "Doğuştan itibaren tamamen kemikleşmiş ve hiçbir hücresi bulunmayan bir alandır", "isCorrect": False, "explanation": "Canlı, dinamik epitel içerir."},
            {"key": "C", "text": "Sadece 80 yaş üzerindeki kadınlarda görülen bir atrofi alanıdır", "isCorrect": False, "explanation": "Üreme çağında ve ergenlikte en aktiftir."},
            {"key": "D", "text": "Hiçbir zaman skuamöz hücre içermeyen sırf çizgili kas demetidir", "isCorrect": False, "explanation": "Epitel sahasıdır, kas lifi değildir."}
        ])
    ]
    slides.append(make_slide(17, "Transformasyon Bölgesi (Zonu): Tanım ve Önemi", "Orijinal ve yeni SKB, metaplastik epitel, Naboth kistleri", "Kritik Servikal Bölge", s17_narrative, s17_bullets, s17_elements))

    # Slide 18: Transformasyon Bölgesi Neden Karsinogenez Merkezidir?
    s18_narrative = (
        "Serviks karsinomlarının ve öncü displastik lezyonlarının neredeyse tamamının transformasyon bölgesinden "
        "kaynaklanması rastlantısal olmayıp dokunun hücresel biyolojisiyle doğrudan ilişkilidir.\n\n"
        "- **Viral Tropizm ve Duyarlılık:** Transformasyon bölgesi, hızla bölünen **olgunlaşmamış (immatür) skuamöz hücrelerden** "
        "oluşur; bu hücreler ==onkojenik HPV enfeksiyonuna en duyarlı alandır==.\n"
        "- **Hücre Döngüsü:** Hücreler bazal membranda sürekli DNA sentezi ve mitoz halindedir; bu aktif ortam virüsün hücre içine "
        "kolayca girmesini ve viral DNA'nın konak mekanizmasını ele geçirmesini kolaylaştırır.\n"
        "- **Karsinom Odak Noktası:** İster skuamöz karsinom ister servikal intraepitelyal neoplazi olsun, patolojik süreç "
        "daima bu metaplastik transformasyon sınırından köken alır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Servikste transformasyon bölgesi olgunlaşmamış skuamöz hücrelerden oluştuğu için onkojenik HPV enfeksiyonuna en duyarlı alandır ve karsinomlar en sık burada gelişir."
    )
    s18_bullets = [
        "Metaplastik olgunlaşmamış hücreler HPV enfeksiyonuna aşırı duyarlıdır.",
        "Aktif DNA sentezi viral genom replikasyonu için uygun zemin sunar.",
        "Serviks kanserleri ve öncü lezyonların neredeyse tamamı burada başlar."
    ]
    s18_elements = [
        make_cloze("Servikste onkojenik HPV enfeksiyonuna en duyarlı ve kanserlerin en sık geliştiği alan transformasyon bölgesi olarak bilinir.", "transformasyon bölgesi", "Neoplazilerin başladığı servikal metaplazi alanı"),
        make_table("Transformasyon Bölgesinin Onkojenik Duyarlılık Faktörleri", ["Biyolojik Özellik", "Hücresel Mekanizma", "Karsinojenik Sonuç"], [
            {"cells": [{"text": "Hücre Matürasyonu", "isMasked": False}, {"text": "Olgunlaşmamış immatür skuamöz hücreler", "isMasked": True, "hint": "tam diferansiye olmamış epitel"}, {"text": "HPV virionlarının kolay tutunması"}]},
            {"cells": [{"text": "Mitotik Aktivite", "isMasked": False}, {"text": "Yüksek oranda hücre döngüsü ve bölünme", "isMasked": False}, {"text": "Viral DNA entegrasyonu için açık kromatin", "isMasked": True, "hint": "genoma entegrasyon kolaylığı"}]}
        ]),
        make_chain("Transformasyon Bölgesinden Neoplaziye Yatkınlık", [
            "1. Metaplastik Odak: Transformasyon bölgesinde genç skuamöz hücreler hızla prolifere olur.",
            "2. Viral Giriş: Mukozal mikrotravmalarla HPV bu çoğalan bazal rezerv hücrelere penetre olur.",
            "3. Entegrasyon: Hızlı çoğalan kromatin yapısı viral genlerin konak DNA'sına girmesine izin verir.",
            "4. Karsinogenez Başlangıcı: Onkoproteinler tetiklenir ve serviks kanserinin temeli bu zonda atılır."
        ]),
        make_recall("Servikste tümörlerin en sık transformasyon bölgesinde gelişmesinin temel nedeni nedir?", "Bu bölgenin hızla bölünen olgunlaşmamış skuamöz hücrelerden oluşması ve onkojenik HPV enfeksiyonuna en duyarlı alan olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Transformasyon Bölgesi ve Karsinogenez", [
            {"text": "Transformasyon bölgesi onkojenik HPV'ye en duyarlı alandır.", "isLie": False, "explanation": "Doğru. İmmatür hücreler enfeksiyona çok yatkındır."},
            {"text": "Servikal tümörler en sık bu metaplastik zondan köken alır.", "isLie": False, "explanation": "Doğru. Karsinomların neredeyse tamamı burada başlar."},
            {"text": "Transformasyon bölgesindeki hücreler virüsleri öldüren zırhlı titanyum tabakası üretir.", "isLie": True, "explanation": "Tuzak! Tam tersine bu bölge virüse en duyarlı ve en savunmasız alandır."},
            {"text": "İmmatür skuamöz hücrelerin varlığı viral penetrasyonu kolaylaştırır.", "isLie": False, "explanation": "Doğru. Hücresel olgunlaşmamışlık duyarlılığı artırır."}
        ]),
        make_quiz("Servikal karsinomların en sık transformasyon bölgesinde gelişmesini açıklayan temel patolojik mekanizma nedir?", [
            {"key": "A", "text": "Bölgenin olgunlaşmamış skuamöz hücrelerden oluşması ve onkojenik HPV'ye en duyarlı alan olması", "isCorrect": True, "explanation": "İmmatür metaplastik hücreler HPV enfeksiyonuna ve transformasyona en açıktır."},
            {"key": "B", "text": "Bu bölgenin sadece kemik iliği kök hücrelerinden meydana gelmesi", "isCorrect": False, "explanation": "Kemik iliği hücresi içermez, epiteldir."},
            {"key": "C", "text": "Bölgede hiçbir zaman hücre bölünmesinin gerçekleşmemesi", "isCorrect": False, "explanation": "Tam tersine hücre bölünmesi son derece hızlıdır."},
            {"key": "D", "text": "Yalnızca retroperitoneal yağ dokusu içermesi", "isCorrect": False, "explanation": "Retroperitonla ilişkisi yoktur."}
        ])
    ]
    slides.append(make_slide(18, "Transformasyon Bölgesi Neden Karsinogenez Merkezidir?", "Viral duyarlılık, immatür skuamöz hücreler, proliferatif zemin ve neoplazi odağı", "Onkolojik Zemin", s18_narrative, s18_bullets, s18_elements))

    # Slide 19: Serviks Neoplazileri Genel Sınıflaması
    s19_narrative = (
        "Serviks neoplazileri, epitelin kaynaklandığı hücre türüne ve hücresel diferansiyasyonuna göre "
        "skuamöz ve glandüler olmak üzere iki ana histolojik grupta incelenir.\n\n"
        "- **Skuamöz Hücreli Neoplaziler:** Olguların ezici çoğunluğunu oluşturur; prekanseröz lezyonları (SIL / CIN) "
        "ve invaziv skuamöz hücreli karsinomu kapsar.\n"
        "- **Glandüler Neoplaziler:** Endoservikal mukus salgılayan kolumnar epitelden gelişir; adenokarsinoma in situ (AIS) "
        "ve invaziv adenokarsinomları içerir.\n"
        "- **Ortak Payda Olarak HPV:** Hem skuamöz karsinomların hem de adenokarsinomların neredeyse tamamı "
        "yüksek riskli onkojenik HPV tipleriyle (özellikle HPV 16 ve 18) doğrudan etiyolojik bağlantıya sahiptir.\n\n"
        "> [!NOTE]\n"
        "> Serviks tümörlerinin büyük çoğunluğu yüksek onkojenik riskli HPV ile ilişkili karsinomlardır."
    )
    s19_bullets = [
        "En sık görülen grup skuamöz neoplazilerdir.",
        "Glandüler neoplaziler endoservikal kolumnar epitelden gelişir.",
        "Her iki grubun da gelişiminde onkojenik HPV temel etkendir."
    ]
    s19_elements = [
        make_cloze("Serviks epitelyal tümörlerinin büyük çoğunluğu onkojenik HPV tipleriyle ilişkili karsinomlardır.", "HPV", "Karsinogenezden sorumlu temel viral etken kısaltması"),
        make_table("Serviks Neoplazileri Temel Sınıflaması", ["Neoplazi Türü", "Köken Aldığı Epitel", "En Önemli Etyolojik Faktör"], [
            {"cells": [{"text": "Skuamöz Neoplaziler", "isMasked": False}, {"text": "Çok katlı yassı / metaplastik epitel", "isMasked": True, "hint": "transformasyon zonu yassı epiteli"}, {"text": "Yüksek riskli HPV (Tip 16, 18)"}]},
            {"cells": [{"text": "Glandüler Neoplaziler", "isMasked": False}, {"text": "Endoservikal mukus salgılayan kolumnar epitel", "isMasked": False}, {"text": "Yüksek riskli HPV (Tip 16, 18)", "isMasked": True, "hint": "viral etyolojik payda"}]}
        ]),
        make_chain("Epitelden Neoplastik Spektruma", [
            "1. Normal Epitel: Ektoserviks skuamöz, endoserviks kolumnar epitel ile örtülüdür.",
            "2. Viral Maruziyet: Yüksek riskli HPV her iki epitel kompartmanına da temas eder.",
            "3. İntraepitelyal Faz: Skuamöz hücrelerde SIL/CIN, glandüler hücrelerde AIS gelişir.",
            "4. İnvaziv Kanser: Bazal membran aşılarak invaziv skuamöz karsinom veya adenokarsinom oluşur."
        ]),
        make_recall("Servikal epitelyal malignitelerin hem skuamöz hem glandüler formlarında ortak olan en kritik etiyolojik ajan nedir?", "Yüksek onkojenik riskli Human Papilloma Virus (HPV) enfeksiyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Serviks Neoplazileri Sınıflaması", [
            {"text": "Servikal neoplaziler skuamöz ve glandüler olmak üzere iki temel grupta incelenir.", "isLie": False, "explanation": "Doğru. Yassı ve bez kaynaklı tümörlerdir."},
            {"text": "Servikal tümörlerin büyük çoğunluğu onkojenik HPV enfeksiyonuyla ilişkilidir.", "isLie": False, "explanation": "Doğru. HPV en temel onkojenik ajandır."},
            {"text": "Serviks kanserleri asla epitelden gelişmez, sadece kemik dokusunun kırılmasıyla oluşur.", "isLie": True, "explanation": "Tuzak! Serviks kanserleri epitel kaynaklı karsinomlardır; kemik kırığı ile ilişkisi yoktur."},
            {"text": "Glandüler neoplaziler endoservikal kolumnar hücrelerden köken alır.", "isLie": False, "explanation": "Doğru. Mukus salgılayan bez epitelinden gelişirler."}
        ]),
        make_quiz("Servikal tümörlerin büyük çoğunluğunun etyopatogenezi ile ilgili aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Hemen hepsi onkojenik HPV enfeksiyonu ile ilişkili karsinomlardır", "isCorrect": True, "explanation": "Serviks karsinomlarının %95'ten fazlası yüksek riskli HPV ile bağlantılıdır."},
            {"key": "B", "text": "Sadece aşırı demir eksikliği anemisi sonucu gelişen selim kistlerdir", "isCorrect": False, "explanation": "Malign epitelyal neoplazidir, anemiyle ilişkili kist değildir."},
            {"key": "C", "text": "Hiçbir zaman servikal epitelle ilişkili olmayan plevra tümörleridir", "isCorrect": False, "explanation": "Serviks kaynaklı jinekolojik tümörlerdir."},
            {"key": "D", "text": "Yalnızca bakteriyel tüberküloz basili tarafından oluşturulurlar", "isCorrect": False, "explanation": "Temel etken viraldir (HPV)."}
        ])
    ]
    slides.append(make_slide(19, "Serviks Neoplazileri Genel Sınıflaması", "Skuamöz karsinomlar, adenokarsinomlar, HPV ilişkisi ve genel spektrum", "Genel Onkolojik Sınıflama", s19_narrative, s19_bullets, s19_elements))

    # Slide 20: [TEKRAR SAYFASI - CHECKPOINT 2] Endoservikal Polip ve Transformasyon Bölgesi
    s20_narrative = (
        "Bu tekrar sayfasında Bölüm 2 boyunca işlediğimiz endoservikal poliplerin biyolojisini, serviks epitel mimarisini "
        "ve karsinogenezin beşiği olan transformasyon bölgesini sentezliyoruz.\n\n"
        "- **Endoservikal Polip Özeti:** Tamamen selim, ekzofitik lezyonlardır; malign potansiyelleri yoktur ancak "
        "yüzeyel ülserasyonla **düzensiz vajinal kanama** yaparak karsinom şüphesi uyandırırlar; polipektomi ile tedavi edilirler.\n"
        "- **Epitel Ayrımı:** Ektoserviks çok katlı yassı epitel; endoserviks tek katlı mukus salgılayan kolumnar epiteldir. "
        "Aralarındaki sınır **skuamo-kolumnar bileşkedir (SKB)** ve yaş ile östrojen durumuna göre hareket eder.\n"
        "- **Eversiyon ve Metaplazi:** Pubertede açığa çıkan kolumnar epitel vajinal asit pH uyarısıyla **skuamöz metaplaziye** uğrar.\n"
        "- **Transformasyon Bölgesi (TZ):** Olgunlaşmamış immatür skuamöz hücrelerden oluşur; **HPV enfeksiyonuna en duyarlı alandır** ve tümörler burada başlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 2 SENTEZİ] Endoservikal polip benign olup kanamayla karsinomu taklit eder; transformasyon bölgesi ise immatür metaplastik hücreleri nedeniyle onkojenik HPV ve karsinom gelişiminin ana merkezidir."
    )
    s20_bullets = [
        "Endoservikal polip malign potansiyelsizdir ancak kanama ile kanseri taklit eder.",
        "SKB dinamiktir; eversiyon sonrası asit temasıyla koruyucu skuamöz metaplazi gelişir.",
        "Transformasyon bölgesi immatür hücreleri nedeniyle HPV'ye en duyarlı neoplazi odağıdır."
    ]
    s20_elements = [
        make_cloze("Servikal tümörlerin en sık kaynaklandığı ve immatür metaplastik hücreler içeren alana transformasyon bölgesi adı verilir.", "transformasyon bölgesi", "Checkpoint 2 sentezinde pekiştirilen karsinogenez alanı"),
        make_table("Bölüm 2 Temel Kazanımları Sentez Tablosu", ["Patolojik Yapı / Bölge", "Biyolojik Doğası", "En Kritik Klinik / Patolojik Önemi"], [
            {"cells": [{"text": "Endoservikal Polip", "isMasked": False}, {"text": "Tamamen benign ekzofitik kitle", "isMasked": True, "hint": "selim mukozal büyüme"}, {"text": "Ülserasyon ve kanamayla kanser şüphesi doğurur"}]},
            {"cells": [{"text": "Transformasyon Zonu", "isMasked": False}, {"text": "İmmatür skuamöz metaplazi alanı", "isMasked": False}, {"text": "HPV'ye en duyarlı alan olup kanserlerin başlangıç yeridir", "isMasked": True, "hint": "karsinogenezin kritik merkezi"}]}
        ]),
        make_chain("Bölüm 2 Mekanizma Konsolidasyonu", [
            "1. Hormonal Etki: Pubertede eversiyon ile kolumnar epitel asidik vajinal ortama açığa çıkar.",
            "2. Adaptif Yanıt: Rezerv hücrelerden gelişen skuamöz metaplazi transformasyon bölgesini kurar.",
            "3. İmmün/Viral Hedef: Bu alandaki hızla çoğalan immatür hücreler HPV tropizmine en duyarlı zemin haline gelir.",
            "4. Klinik Ayırıcı Tanı: Bu zonda karsinom gelişirken; lümendeki benign polipler benzer kanama semptomuyla kliniğe başvurur."
        ]),
        make_recall("Bölüm 2 kapsamında öğrendiğimiz: (1) Malign potansiyeli olmayıp kanama yapan lezyon ve (2) HPV'ye en duyarlı anatomik alan hangileridir?", "(1) Endoservikal polip, (2) Transformasyon bölgesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 2 Checkpoint Sentezi", [
            {"text": "Endoservikal poliplerin malign potansiyeli yoktur, selim lezyonlardır.", "isLie": False, "explanation": "Doğru. Polip kesinlikle benign bir kitle lezyonudur."},
            {"text": "Transformasyon bölgesi olgunlaşmamış skuamöz hücreler içerdiğinden HPV'ye en duyarlı alandır.", "isLie": False, "explanation": "Doğru. Karsinogenezin ana odağı bu alandır."},
            {"text": "Endoservikal polipler çıkarıldıktan sonra mutlaka mikroskopta kanser ekarte edilmelidir.", "isLie": False, "explanation": "Doğru. Ekzofitik karsinomları dışlamak için histoloji şarttır."},
            {"text": "Eversiyon sonucu açığa çıkan kolumnar epitel daima kemik iliğine dönüşerek lösemi yapar.", "isLie": True, "explanation": "Tuzak! Eversiyon lösemi yapmaz; vajinal asit etkisiyle koruyucu skuamöz metaplaziye dönüşür."}
        ]),
        make_quiz("Bölüm 2'de ele alınan konular çerçevesinde aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Endoservikal polip - Yüksek malign potansiyel ve zorunlu kemoterapi", "isCorrect": True, "explanation": "Yanlış eşleştirme! Endoservikal polip benigndir; kemoterapi gerekmez."},
            {"key": "B", "text": "Ektoserviks - Çok katlı keratinize olmayan skuamöz epitel", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "C", "text": "Transformasyon bölgesi - Onkojenik HPV enfeksiyonuna en duyarlı alan", "isCorrect": False, "explanation": "Doğru eşleştirmedir."},
            {"key": "D", "text": "Eversiyon - Pubertede kolumnar epitelin ektoservikse doğru kayması", "isCorrect": False, "explanation": "Doğru eşleştirmedir."}
        ])
    ]
    slides.append(make_slide(20, "[TEKRAR SAYFASI - CHECKPOINT 2] Endoservikal Polip ve Transformasyon Bölgesi", "Bölüm 2 kapsamlı tekrarı: polip biyolojisi, epitel mimarisi ve metaplastik zon", "Bölüm Tekrarı ve Konsolidasyon", s20_narrative, s20_bullets, s20_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec2()
    print(f"Sec2 generated: {len(slides)} slides (Slide 11 to 20)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
