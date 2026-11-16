# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-19-s41",
        "title": "Chicago Konsensüsü (2006): Terminoloji Devrimi ve CGB Tanımı",
        "content": "2006 yılında Chicago'da toplanan uluslararası konsensüs (LWPES/ESPE), cinsiyet anomalilerine yaklaşımda devrim yaratmıştır (Sınav Spotu):\n\n- **Tanım:** Cinsiyet Gelişim Bozuklukları (CGB / DSD - Disorders of Sex Development), kromozomal, gonadal veya anatomik cinsiyetin atipik olduğu doğumsal durumları tanımlar.\n- **Terminoloji Değişikliğinin Nedenleri:**\n  - Eski 'hermafrodit', 'psödohermafrodit' ve 'interseks' gibi terimler aileler ve hastalar için aşağılayıcı ve damgalayıcı (stigmatize edici) bulunmuştur.\n  - Ayrıca eski sınıflama moleküler genetik etiyolojiyi yansıtmaktan uzaktı.\n- **Yeni Prensipler:** Sınıflama artık doğrudan **genetik karyotip** ve altta yatan moleküler mekanizma (gonadal disgenezi, hormon sentez veya etki defekti) temelinde yapılır.\n- **Görülme Sıklığı:** Kuşkulu genitalya ve belirgin CGB tabloları canlı doğumların yaklaşık 1/4500 ila 1/5000'inde görülür; izole hafif varyantlarla bu oran %1'e yaklaşır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Eski Terminoloji vs Yeni CGB Terminolojisi",
                "Eski Terminoloji (Pre-2006)",
                "İnterseks, hermafroditizm, erkek/dişi psödohermafrodit gibi kafa karıştırıcı ve damgalayıcı terimler kullanılırdı.",
                "Yeni CGB Terminolojisi (Chicago 2006)",
                "Karyotip tabanlı: 46,XX CGB, 46,XY CGB ve Seks Kromozom CGB şeklinde bilimsel ve saygın sınıflama getirildi."
            ),
            make_cloze(
                "2006 Chicago Konsensüsü ile eski interseks ve hermafrodit terimleri yerine karyotip tabanlı Cinsiyet Gelişim Bozuklukları sınıflaması kabul edilmiştir.",
                "Cinsiyet Gelişim Bozuklukları",
                "DSD kısaltmasıyla bilinen ve genetik temele dayanan modern tıbbi sınıflama terimi"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-19-s42",
        "title": "Üç Ana Grup: Seks Kromozom CGB, 46,XY CGB ve 46,XX CGB",
        "content": "Chicago Konsensüsü tüm durumları karyotip temelli 3 ana grupta toplamıştır (Sınav Spotu):\n\n- **1. Seks Kromozomu CGB:**\n  - Seks kromozomlarında sayısal anöploidi veya mozaisizm vardır.\n  - Örnekler: **47,XXY (Klinefelter Sendromu)**, **45,X (Turner Sendromu)**, **45,X/46,XY Miks Gonadal Disgenezi**, 47,XYY, 47,XXX.\n- **2. 46,XY CGB (Eski Erkek Psödohermafroditizm):**\n  - Karyotip 46,XY'dir; testis disgenezisi, androjen sentez kusurları (**5α-redüktaz 2 eksikliği**) veya androjen direnci (**Androjen Duyarsızlık Sendromu - CAIS/PAIS**) nedeniyle yetersiz maskülinizasyon vardır.\n- **3. 46,XX CGB (Eski Dişi Psödohermafroditizm):**\n  - Karyotip 46,XX'dir; over dokusu mevcuttur ancak aşırı fetal androjen maruziyeti (**Konjenital Adrenal Hiperplazi - KAH**) nedeniyle dış genitalya virilize olmuştur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["CGB Ana Grubu", "Karyotip Özelliği", "En Sık / Tipik Klinik Örnekler"],
                [
                    ["Seks Kromozomu CGB", "Sayısal veya mozaik seks anöploidisi", "Klinefelter (47,XXY), Turner (45,X), Miks gonadal disgenezi (45,X/46,XY)"],
                    ["46,XY CGB", "46,XY karyotipi (Yetersiz virilizasyon)", "Androjen duyarsızlık sendromu (AR), 5α-redüktaz eksikliği (SRD5A2)"],
                    ["46,XX CGB", "46,XX karyotipi (Aşırı virilizasyon)", "Konjenital adrenal hiperplazi (CYP21A2 mutasyonu)"]
                ]
            ),
            make_quiz(
                "2006 Chicago Konsensüs sınıflamasına göre aşağıdakilerden hangisi '46,XY CGB' kategorisinde yer alır?",
                [
                    {"key": "A", "text": "Androjen Duyarsızlık Sendromu (ADS)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Androjen duyarsızlık sendromu (CAIS/PAIS), 46,XY genetik yapısına sahip bir bireyde androjen reseptör defektine bağlı 46,XY CGB tablosudur."},
                    {"key": "B", "text": "Konjenital Adrenal Hiperplazi (21-hidroksilaz eksikliği)", "isCorrect": False, "explanation": "KAH en sık 46,XX CGB nedenidir."},
                    {"key": "C", "text": "Turner Sendromu (45,X)", "isCorrect": False, "explanation": "Turner seks kromozomu anöploidi CGB'sidir."},
                    {"key": "D", "text": "Klinefelter Sendromu (47,XXY)", "isCorrect": False, "explanation": "Klinefelter seks kromozomu anöploidi CGB'sidir."}
                ]
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-19-s43",
        "title": "Eski vs Yeni Terminoloji: Hermafroditizmden CGB'ye Geçiş",
        "content": "Tıbbi literatürde ve eski soru bankalarında yer alan terimlerin modern karşılıkları net olarak bilinmelidir (Sınav Spotu):\n\n- **Gerçek Hermafroditizm $\\to$ Ovotestiküler CGB:**\n  - Aynı bireyde hem overyan (oosit/folikül) hem de testiküler (seminifer tübül) dokunun bir arada bulunması durumudur.\n- **Erkek Psödohermafroditizm $\\to$ 46,XY CGB:**\n  - Gonad testistir, karyotip 46,XY'dir ancak dış genitalya tam maskülinize olamamış; dişi veya ambigustur.\n- **Dişi Psödohermafroditizm $\\to$ 46,XX CGB:**\n  - Gonad overdir, Müller kanalları mevcuttur, karyotip 46,XX'dir ancak dış genitalya aşırı androjenle virilize olmuştur.\n- **Testiküler Feminizasyon $\\to$ Komplet Androjen Duyarsızlık Sendromu (CAIS):**\n  - Reseptör yokluğuna bağlı 46,XY dişi fenotip tablosudur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Eski Damgalayıcı Terim", "Modern Tıbbi Terim (2006 Sonrası)", "Temel Gonadal ve Genetik Özellik"],
                [
                    ["Gerçek Hermafrodit", "Ovotestiküler CGB", "Hem over hem testis dokusu birlikte mevcuttur"],
                    ["Erkek Psödohermafrodit", "46,XY CGB (Yetersiz virilizasyon)", "Testis var, karyotip XY; dış genital dişi/ambigus"],
                    ["Dişi Psödohermafrodit", "46,XX CGB (Virilize dişi)", "Over var, karyotip XX; dış genital virilize"],
                    ["Testiküler Feminizasyon", "Komplet Androjen Duyarsızlığı (CAIS)", "Testis var, AR reseptörü yanıtsız, dış fenotip tam kadın"]
                ]
            ),
            make_cloze(
                "Eski sınıflamadaki 'gerçek hermafroditizm' teriminin modern tıptaki tam karşılığı ovotestiküler CGB olarak tanımlanır.",
                "ovotestiküler CGB",
                "Aynı bireyde hem folikül hem seminifer tübül bulunması tablosunun modern adı"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-19-s44",
        "title": "Ovotestiküler CGB: Histopatoloji ve Klinik",
        "content": "Eski adıyla 'gerçek hermafroditizm' olan bu nadir tabloda gonadal histoloji esastır (Sınav Spotu):\n\n- **Histolojik Tanı Şartı:** Tanı koyabilmek için biyopside aynı bireyde hem **seminifer tübüller (testis dokusu)** hem de **primordial/antral foliküller (over dokusu)** kesin olarak gösterilmelidir.\n- **Gonadal Dağılım Tipleri:**\n  - En sık (%70): Tek bir gonadda her iki dokunun birleşik bulunması (**Ovotestis**).\n  - İkinci sıklıkta: Bir tarafta normal over, diğer tarafta testis bulunması.\n  - Nadiren: Bilateral ovotestis.\n- **Karyotip Dağılımı:** Vakaların yaklaşık **%60-70'i 46,XX karyotiplidir** (çoğunda SRY saptanamaz; SOX9/RSPO1 delesyon/mutasyonları sorumlu tutulur); %10-15'i 46,XY ve %15-20'si 46,XX/46,XY kimerizmidir.\n- **İç ve Dış Genitalya:** Genellikle asimetriktir; ovotestisin veya testisin bulunduğu tarafta Wolff kanalı gelişirken, overin bulunduğu tarafta Müller kanalı korunur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_quiz(
                "Aynı bireyin gonadal biyopsisinde hem oosit içeren foliküllerin hem de seminifer tübüllerin bir arada saptanması durumunda konulacak en doğru modern tanı hangisidir?",
                [
                    {"key": "A", "text": "Ovotestiküler CGB", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hem over hem testis dokusunun histolojik olarak gösterilmesi ovotestiküler CGB (eski gerçek hermafroditizm) tanısını koydurur."},
                    {"key": "B", "text": "Swyer Sendromu", "isCorrect": False, "explanation": "Swyer sendromunda streak gonad vardır, folikül veya tübül gelişemez."},
                    {"key": "C", "text": "Klinefelter Sendromu", "isCorrect": False, "explanation": "Klinefelter'de over dokusu bulunmaz."},
                    {"key": "D", "text": "Konjenital Adrenal Hiperplazi", "isCorrect": False, "explanation": "KAH'ta testis dokusu bulunmaz, overler normaldir."}
                ]
            ),
            make_recall(
                "Ovotestiküler CGB (gerçek hermafroditizm) vakalarında en sık (%60-70) saptanan kromozomal karyotip hangisidir?",
                "46,XX",
                "Çoğunda SRY negatif olan dişi karyotipi"
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-19-s45",
        "title": "Erkek Psödohermafroditizm vs Dişi Psödohermafroditizm",
        "content": "Psödohermafroditizm kavramı, gonadın türü ile dış genitalyanın yönü arasındaki tezatı ifade eder (Sınav Spotu):\n\n- **46,XY CGB (Erkek Psödohermafroditizm):**\n  - Bireyde **yalnızca testis dokusu** vardır; over dokusu kesinlikle yoktur.\n  - Ancak fetal dönemde ya yeterli testosteron/DHT sentezlenememiştir ya da hedef hücre reseptörleri androjene yanıtsızdır.\n  - Sonuçta dış genitalya dişi görünümünde kalır veya ambigus (kuşkulu) olur.\n  - En sık nedenler: 5α-redüktaz 2 eksikliği, Androjen duyarsızlık sendromu (CAIS/PAIS) ve 17β-HSD defekti.\n- **46,XX CGB (Dişi Psödohermafroditizm):**\n  - Bireyde **yalnızca over dokusu** vardır; testis dokusu yoktur.\n  - Müller yapıları (uterus, tubalar) normal gelişmiştir.\n  - Ancak aşırı androjen maruziyeti nedeniyle genital tüberkül ve katlantılar virilize olmuştur (klitoromegali, labial füzyon).\n  - En sık neden: **Konjenital Adrenal Hiperplazi (CYP21A2 eksikliği)**.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "46,XY CGB (Erkek Psödo) vs 46,XX CGB (Dişi Psödo)",
                "46,XY CGB (Gonad: Testis)",
                "Karyotip 46,XY; testis mevcut, over yok; yetersiz androjen etkisiyle dış genitalya kız/ambigustur.",
                "46,XX CGB (Gonad: Over)",
                "Karyotip 46,XX; over ve uterus mevcut; aşırı androjen etkisiyle dış genitalya erkeksi virilize olmuştur."
            ),
            make_cloze(
                "Yalnızca testis dokusu taşıyan ancak yetersiz androjen etkisi nedeniyle dış genitalyası virilize olamayan 46,XY bireyler 46,XY CGB grubunu oluşturur.",
                "46,XY CGB",
                "Eski adıyla erkek psödohermafroditizm olan klinik kategori"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-19-s46",
        "title": "Prader Evrelemesi (Evre 0 - Evre 5): Dış Genital Maskülinizasyon Derecesi",
        "content": "Özellikle KAH ve virilize 46,XX olgularında dış genitalyanın maskülinizasyon şiddetini nesnel olarak derecelendirmek için **Prader Evrelemesi** kullanılır (Sınav Spotu):\n\n- **Evre 0:** Tamamen normal dişi dış genitalyası (virilizasyon yok).\n- **Evre 1:** Yalnızca hafif klitoris büyümesi (klitoromegali); labial füzyon yoktur, üretral ve vajinal orifisler tamamen ayrıdır.\n- **Evre 2:** Belirgin klitoromegali; labioskrotal katlantılarda hafif posterior füzyon başlar; ürogenital açıklık daralır.\n- **Evre 3:** İleri derecede büyümüş klitoris (fallus görünümü); belirgin labial füzyon; üretral ve vajinal orifislerin birleştiği tek bir ortak **ürogenital sinüs** açıklığı vardır.\n- **Evre 4:** Penise çok benzeyen fallus; fallus tabanına açılan perineoskrotal hipospadias; skrotum görünümünde tam füzyone dudaklar.\n- **Evre 5:** Tamamen normal erkek dış genitalyası; penil üretra glans ucuna açılır; içi boş skrotum (kriptorşidizm zannedilir).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Prader Evresi", "Klitoris / Fallus Durumu", "Labioskrotal Füzyon", "Üretral / Vajinal Açıklık"],
                [
                    ["Evre 0", "Normal dişi klitoris", "Yok (Açık labia majörler)", "Ayrı üretra ve vajen"],
                    ["Evre 1", "Hafif klitoromegali", "Yok", "Ayrı üretra ve vajen"],
                    ["Evre 2", "Belirgin klitoromegali", "Hafif posterior füzyon", "Giriş daralmış"],
                    ["Evre 3", "Mikrofallus benzeri klitoris", "İleri labial füzyon", "Tek ortak ürogenital sinüs orifisi"],
                    ["Evre 4", "Penis görünümlü fallus", "Skrotal füzyon", "Perineoskrotal hipospadias"],
                    ["Evre 5", "Normal erkek penis boyutu", "Tam skrotum", "Glans ucunda normal orifis (Erkek fenotipi)"]
                ]
            ),
            make_quiz(
                "Konjenital adrenal hiperplazi tanısı alan 46,XX bir yenidoğanın muayenesinde belirgin klitoromegali, labioskrotal füzyon ve üretral-vajinal açıklıkların tek bir ortak ürogenital sinüse açıldığı görülüyor. Prader evresi kaçtır?",
                [
                    {"key": "A", "text": "Prader Evre 3", "isCorrect": True, "explanation": "Doğru cevap A'dır: Büyümüş klitoris, labioskrotal füzyon ve ortak tek bir ürogenital sinüs varlığı klasik Prader Evre 3 tablosudur."},
                    {"key": "B", "text": "Prader Evre 1", "isCorrect": False, "explanation": "Evre 1'de sadece hafif klitoromegali vardır, labial füzyon yoktur."},
                    {"key": "C", "text": "Evre 5", "isCorrect": False, "explanation": "Evre 5'te tam erkek dış genitalyası oluşmuştur, orifis glanstadır."},
                    {"key": "D", "text": "Evre 0", "isCorrect": False, "explanation": "Evre 0 normal dişidir."}
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-19-s47",
        "title": "İzole Dış Genital Anomaliler: Hipospadias ve Kriptorşidizm",
        "content": "Kuşkulu genitalya olmaksızın sık karşılaşılan izole anatomik varyantlar da CGB spektrumunda değerlendirilmelidir (Sınav Spotu):\n\n- **Hipospadias:**\n  - Eksternal üretral orifisin penisin ventral (alt) yüzünde sonlanmasıdır.\n  - Embriyolojik Neden: Ürogenital kıvrımların orta hatta kapanmasındaki aksaklıktır (DHT yetersizliği veya reseptör defekti).\n  - Sınıflama: Glanüler, koronal, penil ve perineoskrotal hipospadias.\n  - **Kritik Kural:** Ağır (proksimal) hipospadias veya beraberinde inmemiş testis saptanan her olgu tam bir **CGB protokolü ile araştırılmalıdır**.\n- **Kriptorşidizm (İnmemiş Testis):**\n  - Testislerin skrotuma inemeyip batın içi, kasık kanalı veya dış halkada kalmasıdır.\n  - Prematürelerde %30, term bebeklerde %3 oranında görülür.\n  - Komplikasyonlar: Testis torsiyonu, subfertilite/infertilite ve **malignite (seminom/testis kanseri) riskinde 4-10 kat artış**.\n  - Tedavi: 6-12. aylara kadar kendiliğinden inmezse cerrahi orşiopeksi yapılır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Hipospadias Gelişim ve Kapanma Kusuru",
                [
                    "1. DHT Sinyali: Fetal dönemde androjen düzeyi penil üretrayı kapatmaya başlar.",
                    "2. Ventral Kapanma: Ürogenital kıvrımlar proksimalden distale doğru kaynaşır.",
                    "3. Kapanma Duraklaması: Androjenik uyarım yetersiz kalırsa füzyon yarım kalır.",
                    "4. Anatomik Defekt: Üretra meatüsü glans yerine ventral peniste açılır.",
                    "5. Klinik İnceleme: Beraberinde kordi (eğrilik) ve prepisyum fazlalığı eşlik eder."
                ]
            ),
            make_cloze(
                "Eksternal üretral ağzın penisin ventral alt yüzüne açılması durumuna hipospadias adı verilir ve ürogenital kıvrımların kapanma defektinden kaynaklanır.",
                "hipospadias",
                "Erkek çocuklarda en sık cerrahi gerektiren ventral üretra açıklığı anomalisi"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-19-s48",
        "title": "Mikrofallus ve Etiyolojik Nedenleri: Hipogonadizm Ayrımı",
        "content": "Yenidoğan döneminde fallus boyutunun doğru ölçülmesi CGB tanısında hayati bir basamaktır (Sınav Spotu):\n\n- **Tanım:** Term bir erkek bebekte gerilmiş penis boyunun (SPL - Stretched Penile Length) **2.5 cm'nin (ortalamanın -2.5 SD altı)** altında olmasıdır.\n- **Etiyolojik Sınıflama:**\n  - **1. Hipogonadotropik Hipogonadizm (Santral):**\n    - Hipotalamus (GnRH yetersizliği - Kallmann Sendromu) veya hipofiz ön lobu (LH/FSH yetmezliği, panhipopituitarizm).\n    - İkinci ve üçüncü trimesterde fetal testisin testosteron üretememesine bağlı fallik büyüme duraksar.\n  - **2. Hipergonadotropik Hipogonadizm (Primer Testiküler):**\n    - Testis disgenezisi veya Leydig hücre hipoplazisi (LHCGR mutasyonu).\n    - Testis testosteron yapamaz, LH yüksek bulunur.\n  - **3. Hedef Doku Yanıtsızlığı:**\n    - 5α-redüktaz eksikliği veya parsiyel androjen duyarsızlığı (PAIS).\n- **Acil Uyarı:** Mikrofallus ile birlikte hipoglisemi varsa **panhipopituitarizm (ACTH + GH eksikliği)** neonatal bir acildir!",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Santral Hipogonadotropik vs Primer Hipergonadotropik Mikrofallus",
                "Santral Hipogonadotropik (Hipofiz)",
                "LH ve FSH düşüktür; GnRH veya hipofiz hormon eksikliği vardır; mikrofallusa hipoglisemi eşlik edebilir.",
                "Primer Hipergonadotropik (Testis)",
                "LH ve FSH yüksektir; testis Leydig hücreleri haraptır veya reseptör defektlidir; periferik androjen azdır."
            ),
            make_quiz(
                "Yenidoğan bir erkek bebekte mikrofallus ile birlikte ağır hipoglisemi ve mikropenis saptanması durumunda öncelikle dışlanması gereken hayati endokrin acil hangisidir?",
                [
                    {"key": "A", "text": "Konjenital Panhipopituitarizm (ACTH ve GH eksikliği)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Mikrofallus ile neonatal hipogliseminin birlikteliği hayatı tehdit eden panhipopituitarizmi (kortizol ve büyüme hormonu yokluğu) düşündürür."},
                    {"key": "B", "text": "İzole Turner Sendromu", "isCorrect": False, "explanation": "Turner sendromu 45,X kızlarda görülür."},
                    {"key": "C", "text": "Basit fimozis", "isCorrect": False, "explanation": "Fimozis sünnet derisi darlığıdır, hipoglisemi ve mikrofallus yapmaz."},
                    {"key": "D", "text": "Sertoli hücre tümörü", "isCorrect": False, "explanation": "Yenidoğanda tümör nadirdir ve hipoglisemi mikrofallus tablosu oluşturmaz."}
                ]
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-19-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] CGB Sınıflaması ve Prader Evrelemesi",
        "content": "Bu checkpointte modern CGB sınıflamasını ve klinik evrelemeyi özetliyoruz:\n\n- **Chicago Konsensüsü (2006):** Aşağılayıcı terimler yerine genetik tabanlı 3 grup kabul edildi: Seks Kromozom CGB, 46,XY CGB ve 46,XX CGB.\n- **Ovotestiküler CGB (Gerçek Hermafrodit):** Aynı bireyde hem folikül hem seminifer tübül bulunmasıdır; %70'i ovotestistir ve en sık **46,XX karyotiplidir**.\n- **46,XY CGB (Erkek Psödo):** Testis vardır, over yoktur; testosteron/DHT yetersizliği veya reseptör direnci nedeniyle yetersiz maskülinizasyon görülür.\n- **46,XX CGB (Dişi Psödo):** Over ve uterus vardır; en sık neden **Konjenital Adrenal Hiperplazidir (CYP21A2)**.\n- **Prader Evrelemesi (0-5):** Evre 0 normal dişi, Evre 3 ortak tek ürogenital sinüs, Evre 5 tam erkek dış görünüşüdür.\n- **Hipospadias:** Ürogenital kıvrımların ventralde kapanamamasıdır; proksimal tipler CGB araştırması gerektirir.\n- **Mikrofallus:** Term bebekte gerilmiş boyun 2.5 cm altında olmasıdır; hipoglisemi eşlik ederse santral hipopituitarizm aranmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Klinik Durum", "Karyotip", "Gonad", "Dış Genitalya Özelliği"],
                [
                    ["Ovotestiküler CGB", "%60-70 46,XX", "Hem over hem testis (ovotestis)", "Değişken, sıklıkla asimetrik ve kuşkulu"],
                    ["46,XY CGB", "46,XY", "Testisler mevcut", "Dişi veya ambigus (yetersiz virilizasyon)"],
                    ["46,XX CGB", "46,XX", "Overler mevcut", "Virilize / erkekleşmiş (aşırı androjen)"],
                    ["Prader Evre 3", "En sık 46,XX (KAH)", "Normal overler", "Büyümüş klitoris + tek ürogenital sinüs"]
                ]
            ),
            make_chain(
                "CGB Terminolojik Yaklaşım Özeti",
                [
                    "1. Genetik Belirleme: Karyotip analizi ile kromozomal zemin saptanır.",
                    "2. Gonadal Değerlendirme: Palpabl gonad varlığı ve USG ile iç organlar taranır.",
                    "3. Fenotipik Skorlama: Prader cetveli ile virilizasyon şiddeti kaydedilir.",
                    "4. Etiyolojik Ayrım: Androjen fazlalığı mı yoksa androjen direnci mi olduğu belirlenir."
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-19-s50",
        "title": "Bölüm Özeti: Sınıflamadan Seks Kromozomu Sayısal Anomalilerine Geçiş",
        "content": "Bölüm 5 boyunca Chicago konsensüsünü, Prader evrelemesini, ovotestiküler CGB'yi ve mikrofallus yaklaşımını inceledik:\n\n- **Özet:** CGB'de temel hedef genetik ve hormonal nedeni saptayarak erken tıbbi ve psikososyal yönetim planı oluşturmaktır.\n- **Sonraki Bölüm (Bölüm 6):** CGB sınıflamasının ilk grubu olan **Seks Kromozomu Sayısal Bozukluklarını (47,XXY Klinefelter, 45,X Turner, 47,XYY, 47,XXX ve 45,X/46,XY Miks Gonadal Disgenezi)** detaylarıyla inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "Hem testis hem de over dokusunun histolojik olarak aynı bireyde gösterildiği CGB tablosuna ne ad verilir?",
                "Ovotestiküler CGB",
                "Eski adı gerçek hermafroditizm olan durum"
            ),
            make_quiz(
                "Prader sınıflamasına göre büyümüş klitoris ile birlikte vajina ve üretranın birleşerek tek bir orifisle dışarı açıldığı ortak ürogenital sinüs tablosu hangi evredir?",
                [
                    {"key": "A", "text": "Prader Evre 3", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tek ortak ürogenital sinüs açıklığı Prader Evre 3'ün temel belirleyicisidir."},
                    {"key": "B", "text": "Prader Evre 1", "isCorrect": False, "explanation": "Evre 1'de orifisler tamamen ayrıdır."},
                    {"key": "C", "text": "Prader Evre 2", "isCorrect": False, "explanation": "Evre 2'de giriş dardır ancak orifisler henüz tek sinüs halinde birleşmemiştir."},
                    {"key": "D", "text": "Prader Evre 4", "isCorrect": False, "explanation": "Evre 4'te perineoskrotal hipospadiaslı fallus vardır."}
                ]
            )
        ]
    })

    return slides
