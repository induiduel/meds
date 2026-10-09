# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-17-s71",
        "title": "Genital Ülser Sendromuna Giriş: Ağrılı vs Ağrısız Algoritması",
        "content": "Genital bölgede açık yara (ülser veya erozyon) ile başvuran hastada etiyolojik ayrımın ilk ve en kritik basamağı ağrı varlığıdır (Sınav Spotu):\n\n- **Ağrılı Genital Ülserler (Şiddetli Yanma ve Hassasiyet):**\n  1. **Şankroid (Ulkus Molle - Haemophilus ducreyi):** Genellikle tek veya birkaç adet, derin, tabanı sarı pürülan cerahatli, sınırları düzensiz ve **aşırı derecede ağrılı ülser**.\n  2. **Genital Herpes (HSV-1 ve HSV-2):** Kırmızı zemin üzerinde grup yapmış veziküllerin patlamasıyla oluşan, yüzeysel, çoklu ve **son derece ağrılı sığ ülserler**.\n- **Ağrısız Genital Ülserler (Ağrı ve Hassasiyet Yok):**\n  1. **Primer Sifilis (Sert Şankr / Ulkus Durum - Treponema pallidum):** Tipik olarak tek, yuvarlak, sınırları belirgin, kenarları ve tabanı sert (endüre), yüzeyi temiz ve **tamamen ağrısız lezyon**.\n  2. **Lenfogranüloma Venereum (LGV):** Erken dönemdeki geçici küçük ağrısız papül/ülser.\n  3. **Granüloma İnguinale (Donovanozis):** Ağrısız, temasla kolay kanayan granülasyon dokulu yaygın ülserler.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Ağrılı Ülser (Şankroid/Herpes) vs Ağrısız Ülser (Sifilis)",
                "Ağrılı Genital Ülser",
                "Şankroid (H. ducreyi) ve Genital Herpes (HSV); hasta şiddetli ağrı ve yanmadan yakınır; şankroidde cerahat vardır.",
                "Ağrısız Genital Ülser",
                "Primer Sifilis (T. pallidum); sert tabanlı, temiz yüzeylidir; hastada ağrı veya hassasiyet kesinlikle yoktur."
            ),
            make_quiz(
                "Genital muayenesinde ağrısız, sert tabanlı, temiz yüzeyli tek bir ülser saptanan hastada öncelikle hangi patojen araştırılmalıdır?",
                [
                    {"key": "A", "text": "Treponema pallidum (Primer Sifilis)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Ağrısız, sert endüre tabanlı ve temiz yüzeyli şankr Treponema pallidum'un (sifilis) klasik lezyonudur."},
                    {"key": "B", "text": "Haemophilus ducreyi", "isCorrect": False, "explanation": "Şankroid ülseri yumuşak ve çok ağrılıdır."},
                    {"key": "C", "text": "Herpes Simpleks Virüsü", "isCorrect": False, "explanation": "Herpes vezikül ve ülserleri şiddetli ağrılıdır."},
                    {"key": "D", "text": "Candida albicans", "isCorrect": False, "explanation": "Candida ülser yapmaz, kaşıntılı plak yapar."}
                ]
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-17-s72",
        "title": "Şankroid (Ulkus Molle / Yumuşak Şankr): Haemophilus ducreyi",
        "content": "Şankroid, özellikle gelişmekte olan tropikal ülkelerde sık görülen akut enfeksiyöz bir genital ülser hastalığıdır (Sınav Spotu):\n\n- **Etken Patojen:** **Haemophilus ducreyi** adı verilen, küçük, fakültatif anaerop, pleomorfik gram negatif bir kokobasildir.\n- **İnokülasyon ve Patogenez:**\n  - Cinsel temas sırasında deride oluşan mikroskobik çatlaklardan girer.\n  - Sitotoksinler (sitolethal distending toxin - CDT) salgılayarak keratinosit ve fibroblast ölümüne yol açar.\n  - 4-7 günlük kısa bir kuluçka süresinden sonra inokülasyon yerinde çevresi eritemli hassas bir papül belirir.\n  - Papül hızla püstüle döner ve 24-48 saat içinde patlayarak derin, nekrotik bir ülsere dönüşür.\n- **HIV Bulaşını Kolaylaştırma:** Şankroid ülserleri yoğun lenfosit ve makrofaj içerdiği için HIV virüsünün girişini ve kan dolaşımına geçişini 5 ila 10 kat kolaylaştırır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Şankroid Ülserinin Gelişim Aşamaları",
                [
                    "1. Mukozal Giriş: Cinsel temasla Haemophilus ducreyi mikroskobik çatlaklardan girer.",
                    "2. Papül ve Püstül: 3-5 gün içinde eritemli hassas bir papül, ardından püstül oluşur.",
                    "3. Doku Nekrozu ve Patlama: Püstül çatlar ve derin, sarı tabanlı bir yara açılır.",
                    "4. Ağrılı Yumuşak Şankr: Tabanı cerahatli, son derece ağrılı şankroid ülseri oturur."
                ]
            ),
            make_cloze(
                "Genital bölgede yumuşak tabanlı, pürülan akıntılı ve son derece ağrılı şankroid lezyonunun etkeni Haemophilus ducreyi bakterisidir.",
                "Haemophilus ducreyi",
                "Şankroid ülserinin gram negatif etkeni"
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-17-s73",
        "title": "Şankroid Morfolojisi: Pürülan Taban ve Süpüratif Bubo",
        "content": "Şankroid ülseri fizik muayenede kendine has dramatik bulgular sergiler (Sınav Spotu):\n\n- **1. Ülser Morfolojisi (Ulkus Molle - Yumuşak Şankr):**\n  - Boyutları 1 mm'den 2 cm'ye kadar değişebilir.\n  - **Ağrılıdır:** En hafif dokunmada bile hasta şiddetli acı duyar.\n  - **Yumuşaktır:** Sifilizin sert kıkırdaksı tabanının aksine dokunulduğunda tabanı yumuşacıktır (bu yüzden 'yumuşak şankr' denir).\n  - **Pürülan / Nekrotik Taban:** Ülser tabanı gri-sarı renkli, kötü kokulu cerahatli eksuda ile kaplıdır; kazındığında kolayca kanar.\n  - **Düzensiz Sınırlar:** Ülser kenarları dik veya oyukludur (undermined borders).\n- **2. Süpüratif İnguinal Lenfadenit (Bubon - Olguların %50'si):**\n  - Ülserden 1-2 hafta sonra kasık lenf düğümleri (çoğunlukla tek taraflı) aşırı büyür.\n  - Ağrılı, kızarık ve fluktuasyon veren dev bir kitleye (**bubon**) dönüşür; tedavi edilmezse cildi eriterek dışarıya bol püy akıtır (fistülizasyon).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Şankroid Ülseri Tabanı vs Sifiliz Ülseri Tabanı",
                "Şankroid (Yumuşak Şankr)",
                "Tabanı yumuşaktır; sarı-gri pürülan cerahatle doludur; son derece ağrılıdır; tek taraflı süpüratif bubo yapar.",
                "Sifiliz (Sert Şankr)",
                "Tabanı kıkırdak gibi serttir (endüre); yüzeyi tertemiz ve parlaktır; tamamen ağrısızdır; bilateral ağrısız sert LAP yapar."
            ),
            make_quiz(
                "Şankroidli bir hastada kasık lenf düğümlerinin tek taraflı olarak aşırı büyümesi, kızarması, fluktuasyon vermesi ve cilde açılarak cerahat akıtması tablosuna ne ad verilir?",
                [
                    {"key": "A", "text": "Bubon (Süpüratif lenfadenit)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Şankroid ve LGV'de kasık lenf nodlarının eriyip cilde fistülize olan cerahatli kitlelerine bubo denir."},
                    {"key": "B", "text": "Kondiloma lata", "isCorrect": False, "explanation": "Sekonder sifiliz lezyonudur."},
                    {"key": "C", "text": "Eritema nodozum", "isCorrect": False, "explanation": "Tibia önünde septal pannikülittir."},
                    {"key": "D", "text": "Gom", "isCorrect": False, "explanation": "Tersiyer sifiliz nekrozudur."}
                ]
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-17-s74",
        "title": "Şankroid Tanısı: 'Balık Sürüsü' / 'Tren Yolu' Manzarası",
        "content": "Haemophilus ducreyi'nin mikroskobik morfolojisi tıp literatürünün en ünlü sınav sorularındandır (Sınav Spotu):\n\n- **Gram ve Giemsa Boyama Görünümü:**\n  - Ülser tabanından veya aspire edilen bubon püyünden hazırlanan yaymada bakteriler birbirine paralel dizilimler gösterir.\n  - Bu dizilim mikroskop altında karakteristik olarak **'balık sürüsü' (school of fish) veya 'tren yolu / demiryolu rayı' (railroad track)** manzarası olarak tanımlanır.\n- **Kültür Şartları:**\n  - Özel zenginleştirilmiş besiyerleri (GC agara hemoglobin ve fetal dana serumu veya Mueller-Hinton agar) ve vankomisin gerektirir.\n  - Bakteri çok zor ürer (duyarlılık <%75); bu nedenle kesin tanı kültürle konulsa da klinik pratikte kültür negatifliği şankroidi dışlamaz.\n- **Olası Şankroid Klinik Tanı Kriterleri (CDC):**\n  1. Bir veya daha fazla ağrılı genital ülser.\n  2. Sifiliz testlerinin (karanlık saha mikroskopisi veya seroloji) negatif olması.\n  3. HSV testlerinin (PCR veya kültür) negatif olması.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Gram Yaymasında Balık Sürüsü vs Kültür İzolasyonu",
                "Mikroskopik Yayma (Gram/Giemsa)",
                "Bakteriler birbirine paralel dizilerek 'balık sürüsü' veya 'tren yolu' benzeri zincirler oluşturur.",
                "Seçici Kültür",
                "H. ducreyi üretilmesi zor bir bakteridir; kesin tanı koysa da klinik tanı sıklıkla dışlama kriterleriyle konur."
            ),
            make_cloze(
                "Haemophilus ducreyi'nin Gram boyamasında hücrelerin birbirine paralel dizilmesiyle oluşan karakteristik mikroskobik görünüme balık sürüsü manzarası denir.",
                "balık sürüsü",
                "H. ducreyi'nin sınav klasiği morfolojik dizilim terimi"
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-17-s75",
        "title": "Şankroid Tedavi Protokolleri: Azitromisin ve Seftriakson",
        "content": "Şankroid etkeni Haemophilus ducreyi uygun antibiyotiklerle hızlı bir iyileşme gösterir (Sınav Spotu):\n\n- **Birinci Basamak Tedavi Protokolleri (CDC ve Kılavuzlar):**\n  1. **Azitromisin 1 g oral TEK DOZ** (En pratik ve hasta uyumu mükemmel seçenek).\n  2. **Seftriakson 250 mg İM TEK DOZ** (Eşit etkinlikte intramusküler seçenek).\n- **Alternatif Rejimler:**\n  - Siprofloksasin 2x500 mg oral, 3 gün (gebelikte ve emzirenlerde KONTRENDİKEDİR).\n  - Eritromisin baz 3x500 mg oral, 7 gün.\n- **Klinik İyileşme Seyri:**\n  - Tedavi başlandıktan 3 ila 7 gün sonra ağrı belirgin biçimde azalır ve ülser tabanı temizlenmeye başlar.\n  - Büyük ülserlerin tamamen epitelize olması 2 haftayı bulabilir.\n- **Fluktuan Bubonların Yönetimi:**\n  - İçi cerahat dolu fluktuan bubonlar cerrahi olarak kesilip açılmaz (insizyon kalıcı fistül ve yara açar); **kalın uçlu bir iğneyle aspire edilmelidir**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["İlaç Adı", "Dozaj ve Uygulama Yolu", "Kür Süresi", "Önemli Avantaj"],
                [
                    ["Azitromisin (Birinci Tercih)", "1 g oral", "Tek doz", "Doğrudan gözetimli tek doz tedavi üstünlüğü"],
                    ["Seftriakson (Birinci Tercih)", "250 mg İM", "Tek doz", "Enjeksiyonla uyum garantisi"],
                    ["Siprofloksasin (Alternatif)", "2x500 mg oral", "3 gün", "Gebelerde ve çocuklarda kesinlikle kullanılmaz"],
                    ["Eritromisin (Alternatif)", "3x500 mg oral", "7 gün", "Gastrointestinal yan etkileri daha sıktır"]
                ]
            ),
            make_quiz(
                "Haemophilus ducreyi'ye bağlı şankroid (yumuşak şankr) tanısı konan bir hastada tek dozla kesin kür sağlayan oral birinci basamak tedavi hangisidir?",
                [
                    {"key": "A", "text": "Azitromisin 1 g oral, tek doz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Şankroid tedavisinde tek doz Azitromisin 1 g oral veya Seftriakson 250 mg İM birinci tercihtir."},
                    {"key": "B", "text": "Flukonazol 150 mg tek doz", "isCorrect": False, "explanation": "Flukonazol mantar ilacıdır."},
                    {"key": "C", "text": "Asiklovir 5x200 mg, 10 gün", "isCorrect": False, "explanation": "Asiklovir herpes ilacıdır."},
                    {"key": "D", "text": "Metronidazol 2 g tek doz", "isCorrect": False, "explanation": "Metronidazol H. ducreyi'ye etkisizdir."}
                ]
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-17-s76",
        "title": "Primer Sifilis (Ulkus Durum / Sert Şankr): Treponema pallidum",
        "content": "Sifilis (frengi), spiroket grubu bir bakteri olan Treponema pallidum tarafından oluşturulan sistemik bir hastalıktır:\n\n- **İnkübasyon Süresi:** Cinsel temastan sonra ortalama **2 ila 3 hafta (10 ila 90 gün)** içinde lezyon belirir.\n- **Primer Evre - Sert Şankr (Ulkus Durum - Sınav Spotu):**\n  - Giriş yerinde (glans penis, vulva, serviks, anüs veya ağız) tek bir papül başlar ve ülsere döner.\n  - **Tamamen Ağrısızdır:** Ülser hastaya hiçbir acı, kaşıntı veya rahatsızlık vermez (bu yüzden servikste veya rektumdaysa hasta hiç fark etmez).\n  - **Sert Tabanlıdır (Endüre):** Parmaklar arasında tutulduğunda deri altında kıkırdak veya düğme varmış gibi sert hissedilir.\n  - **Temiz Tabanlıdır:** Ülser tabanında cerahat yoktur; parlak, pembe-kırmızı, temiz ve seröz sıvı sızdıran bir yüzeyi vardır; spiroketlerden kaynar.\n- **Bölgesel Lenfadenopati:** Ağrısız, sert, lastik kıvamında, hareketli bilateral lenf nodları (asla şankroid gibi erimez ve cerahat akıtmaz).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Sifiliz Sert Şankrı vs Şankroid Yumuşak Şankrı",
                "Primer Sifilis (Sert Şankr)",
                "Tamamen ağrısızdır; tabanı düğme gibi serttir; yüzeyi temiz ve parlaktır; ağrısız sert lenf nodları eşlik eder.",
                "Şankroid (Yumuşak Şankr)",
                "Son derece ağrılıdır; tabanı yumuşaktır; sarı cerahatle kaplıdır; süpüratif fluktuan bubon yapar."
            ),
            make_cloze(
                "Treponema pallidum'un primer evresinde genital bölgede oluşan ağrısız, sert endüre tabanlı ve temiz yüzeyli ülsere sert şankr denir.",
                "sert şankr",
                "Primer sifilisin karakteristik ağrısız ülseri"
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-17-s77",
        "title": "Şankroid ve Sifilis Karşılaştırmalı Tablosu",
        "content": "Kurul sınavlarında genital ülserlerin ayırıcı tanısı klinikte en sık sorulan soru formatlarından biridir (Sınav Spotu):\n\n- **Ağrı Parametresi:** Şankroid ve Genital Herpes şiddetli ağrılıdır; Sifilis ise kesinlikle ağrısızdır.\n- **Ülser Tabanı:** Şankroid yumuşak ve pürülanken; Sifilis sert (endüre) ve temizdir.\n- **Lezyon Sayısı:** Sifilis genellikle tek bir şankr ile seyrederken; şankroidde otoinokülasyonla çoklu ülserler sık görülür.\n- **Lenf Bezi Tutulumu:**\n  - Şankroidde tek taraflı, son derece ağrılı, kızarık ve cerahat toplayıp cilde açılan **süpüratif bubo** gelişir.\n  - Sifiliste iki taraflı, ağrısız, sert, paket yapmayan 'lastik kıvamında' lenfadenopati gelişir; asla cerahat akıtmaz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Özellik", "Şankroid (Yumuşak Şankr)", "Primer Sifilis (Sert Şankr)"],
                [
                    ["Etken Patojen", "Haemophilus ducreyi (bakteri)", "Treponema pallidum (spiroket)"],
                    ["Ağrı Durumu", "Şiddetli derecede ağrılı ve hassas", "Tamamen ağrısız"],
                    ["Ülser Tabanı", "Yumuşak, gri-sarı pürülan cerahatli", "Sert (kıkırdaksı endürasyon), temiz ve parlak"],
                    ["Lezyon Kenarları", "Düzensiz, oyuklu (undermined)", "Düzenli, belirgin, sınırlı"],
                    ["Lenfadenopati", "Tek taraflı, ağrılı, süpüratif fluktuan bubon", "Bilateral, ağrısız, sert, lastik kıvamında LAP"],
                    ["Kür Tedavisi", "Azitromisin 1 g oral tek doz", "Benzatin Penisilin G 2.4 milyon ünite İM"]
                ]
            ),
            make_quiz(
                "Aşağıdaki özelliklerden hangisi şankroid ülserini primer sifilis şankrından kesin olarak ayıran bir bulgudur?",
                [
                    {"key": "A", "text": "Şankroidin ağrılı ve tabanının pürülan cerahatli olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Şankroid şiddetli ağrılı ve sarı cerahatli tabanlıdır; sifilis ise tamamen ağrısız ve temizdir."},
                    {"key": "B", "text": "Şankroidin kıkırdak gibi taş sertliğinde olması", "isCorrect": False, "explanation": "Sert taban sifilize özgüdür."},
                    {"key": "C", "text": "Sifiliste kasık lenf bezlerinin patlayıp püy akıtması", "isCorrect": False, "explanation": "Püy akıtan bubon şankroide aittir."},
                    {"key": "D", "text": "Şankroidin virüslerden kaynaklanması", "isCorrect": False, "explanation": "Her ikisi de bakteriyeldir."}
                ]
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-17-s78",
        "title": "Sifilis Tanı Yöntemleri ve Benzatin Penisilin G Tedavisi",
        "content": "Treponema pallidum cansız yapay besiyerlerinde üretilemez; tanısı mikroskopi ve serolojiye dayanır (Sınav Spotu):\n\n- **1. Karanlık Saha Mikroskopisi (Dark-field):**\n  - Taze şankr lezyonundan sızan seröz sıvı karanlık saha mikroskobunda incelenir.\n  - Siyah zemin üzerinde kendi ekseni etrafında tirbüşon gibi dönen parlak spiroketlerin görülmesi anında kesin tanıdır.\n- **2. Serolojik Testler:**\n  - **Nontreponemal Testler (VDRL ve RPR):** Tarama ve tedavi takibinde kullanılır; kardiyolipin antijenine karşı antikorları ölçer; antikor titresi tedaviyle düşer.\n  - **Treponemal Testler (TPHA, FTA-ABS):** Doğrulama testleridir; treponema spesifik antijenleri saptar; ömür boyu pozitif kalabilir.\n- **Sifilis Tedavisi (Altın Standart İlaç):**\n  - Treponema pallidum penisiline karşı bugüne kadar tek bir direnç vakası bile geliştirememiştir.\n  - **Erken Sifilis (Primer, Sekonder, Erken Latent):** **Benzatin Penisilin G 2.4 milyon ünite İM TEK DOZ**.\n  - **Penisilin Alerjisinde:** Doksisiklin 2x100 mg oral, 14 gün.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Test Türü", "Örnek Testler", "Klinik Kullanım Amacı", "Tedavi Sonrası Seyri"],
                [
                    ["Nontreponemal Testler", "VDRL, RPR", "Tarama ve tedavi yanıtı takibi", "Başarılı tedaviyle titre 4 kat düşer ve negatifleşir"],
                    ["Treponemal Testler", "TPHA, FTA-ABS, TP-PA", "Tanı doğrulama", "Genellikle ömür boyu pozitif kalır (takipte kullanılmaz)"]
                ]
            ),
            make_quiz(
                "Primer sifilis (sert şankr) tanısı konan bir hastada rehberlerin önerdiği standart birinci basamak kür tedavisi hangisidir?",
                [
                    {"key": "A", "text": "Benzatin Penisilin G 2.4 milyon ünite İM, tek doz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Erken sifilisin standart tedavisi Benzatin Penisilin G 2.4 milyon İM tek dozdur."},
                    {"key": "B", "text": "Siprofloksasin 500 mg tek doz", "isCorrect": False, "explanation": "Siprofloksasin sifilize etkisizdir."},
                    {"key": "C", "text": "Metronidazol 2 g tek doz", "isCorrect": False, "explanation": "Metronidazol spirokete etkisizdir."},
                    {"key": "D", "text": "Asiklovir 400 mg oral", "isCorrect": False, "explanation": "Asiklovir antiviraldir."}
                ]
            )
        ]
    })

    # Slide 79 - CHECKPOINT 8
    slides.append({
        "id": "k1-17-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Genital Ülserler ve Şankroid Tedavisi",
        "content": "Bu checkpointte genital ülser sendromunu, şankroid ve sifilis ayrımını özetliyoruz:\n\n- **Ağrılı vs Ağrısız:** Şankroid ve herpes şiddetli ağrılıdır; primer sifilis şankrı tamamen ağrısızdır.\n- **Şankroid (Haemophilus ducreyi):** Küçük eritemli papül $\\to$ püstül $\\to$ yumuşak, sarı pürülan tabanlı, çok ağrılı derin ülser; %50 olguda tek taraflı süpüratif fluktuan bubon.\n- **Şankroid Mikroskopisi:** Gram/Giemsa yaymasında paralel dizilimli 'balık sürüsü' veya 'tren yolu' kokobasilleri.\n- **Şankroid Tedavisi:** Azitromisin 1 g oral tek doz VEYA Seftriakson 250 mg İM tek doz. Fluktuan bubonlar kesilmez, iğneyle aspire edilir.\n- **Primer Sifilis (Treponema pallidum):** Sert endüre tabanlı, temiz pembe yüzeyli, ağrısız ülser; bilateral ağrısız sert LAP. Tanı karanlık saha ve VDRL/TPHA. Tedavi: Benzatin Penisilin G 2.4 milyon ünite İM tek doz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Hastalık", "Etken", "Ülser Karakteri", "Lenfadenopati", "Birinci Tercih İlaç"],
                [
                    ["Şankroid (Ulkus Molle)", "Haemophilus ducreyi", "Ağrılı, yumuşak, sarı pürülan taban", "Tek taraflı cerahatli bubo", "Azitromisin 1 g tek doz / Seftriakson 250 mg"],
                    ["Primer Sifilis (Ulkus Durum)", "Treponema pallidum", "Ağrısız, sert kıkırdaksı taban, temiz yüzey", "Bilateral ağrısız sert LAP", "Benzatin Penisilin G 2.4 M İM tek doz"]
                ]
            ),
            make_chain(
                "Genital Ülser Hızlı Karar Basamakları",
                [
                    "1. Ağrı Değerlendirmesi: Ağrılı ise Şankroid veya Herpes; ağrısız ise Sifilis.",
                    "2. Taban Muayenesi: Pürülan cerahatli ise Şankroid; sert ve temiz ise Sifilis.",
                    "3. Şankroid Tedavisi: Azitromisin 1 g oral veya Seftriakson 250 mg İM tek doz.",
                    "4. Sifilis Tedavisi: Benzatin Penisilin G 2.4 M İM tek doz enjeksiyon."
                ]
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-17-s80",
        "title": "Bölüm Özeti: Bakteriyel Ülserlerden Viral Lezyonlara Geçiş",
        "content": "Bölüm 8 boyunca bakteriyel genital ülserleri, şankroidin ağrılı cerahatli tablosunu ve primer sifilisin sert şankrını tamamladık:\n\n- **Kritik İlke:** Genital ülserler HIV bulaş riskini kat kat artırır; ülserli her hastada HIV taraması yapılmalıdır.\n- **Sonraki Bölüm:** Bir sonraki bölümde en sık görülen viral genital lezyonları — **Genital Herpesi (HSV) ve Anogenital Siğilleri (Kondiloma akuminata / HPV) ve tedavilerini** — inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Haemophilus ducreyi'nin yayma preparatında mikroskop altında oluşturduğu karakteristik paralel dizilime verilen isim nedir?",
                "Balık sürüsü (veya tren yolu) manzarası",
                "School of fish görünümü"
            ),
            make_quiz(
                "Şankroid enfeksiyonunda kasıkta gelişen ve cilde açılarak fistülize olma riski taşıyan içi cerahat dolu fluktuan bir bubon saptandığında cerrahi yaklaşım ne olmalıdır?",
                [
                    {"key": "A", "text": "Neşterle genişçe kesilip açık bırakılmalıdır", "isCorrect": False, "explanation": "İnsizyon ve drenaj kalıcı fistül ve ülser yapar, yasaktır."},
                    {"key": "B", "text": "İnsizyon yapılmamalı, kalın uçlu bir iğne ve enjektörle steril biçimde aspire edilmelidir", "isCorrect": True, "explanation": "Doğru cevap B'dir: Bubonlar kesilmez; iğne aspirasyonu ile boşaltılarak fistülleşme önlenir."},
                    {"key": "C", "text": "Bubon üzerine tuz basılmalıdır", "isCorrect": False, "explanation": "Zararlı ve acı verici halk uygulamasıdır."},
                    {"key": "D", "text": "Hasta acilen böbrek nakline alınmalıdır", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    return slides
