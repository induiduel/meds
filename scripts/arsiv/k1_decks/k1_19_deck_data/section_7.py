# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-19-s61",
        "title": "5α-Redüktaz 2 Eksikliği: Genetik Temel ve SRD5A2 Geni",
        "content": "46,XY CGB vakalarının en çarpıcı biyolojik ve klinik modellerinden biri **5α-Redüktaz 2 eksikliğidir** (Sınav Spotu):\n\n- **Genetik ve Kalıtım:**\n  - Hastalık kromozom 2p23 bölgesinde yer alan **SRD5A2** genindeki mutasyonlara bağlıdır.\n  - Kalıtım paterni **otozomal resesiftir** (akraba evliliklerinin sık olduğu topluluklarda ve izole coğrafi izolatörlerde sıktır; örn. Dominik Cumhuriyeti, Türkiye, Papua Yeni Gine).\n  - Literatürde en sık tanımlanan kurucu mutasyonlardan biri **p.L55Q** (lösin 55 glutamin) missense mutasyonudur.\n- **İzoenzim Farkı:**\n  - 5α-redüktaz tip 1 (SRD5A1) deride ve karaciğerde bulunur, pubertede aktifleşir.\n  - Fetal dış genital dokularda ve prostatta çalışan asıl enzim **5α-redüktaz tip 2 (SRD5A2)** dir; fetal maskülinizasyon için bu izoenzim zorunludur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["İzoenzim", "Kodlayan Gen", "Doku Dağılımı", "CGB ile İlişkisi"],
                [
                    ["5α-Redüktaz Tip 2", "SRD5A2 (2p23)", "Fetal genital tüberkül, skrotal deri, prostat", "Mutasyonunda 46,XY CGB gelişir (Klasik hastalık)"],
                    ["5α-Redüktaz Tip 1", "SRD5A1 (5p15)", "Karaciğer, pubertal deri, yağ bezleri", "Pubertede aktifleşerek virilizasyona katkı sağlar"]
                ]
            ),
            make_cloze(
                "Fetal dış genital dokularda testosteronu dihidrotestosterona dönüştüren ve mutasyonunda 46,XY CGB gelişen enzim 5α-redüktaz tip 2 enzimidir.",
                "5α-redüktaz tip 2",
                "SRD5A2 geni tarafından kodlanan ve fetal maskülinizasyonu sağlayan izoenzim"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-19-s62",
        "title": "Biyokimyasal Tablo: Testosteron/DHT Oranında Aşırı Artış",
        "content": "5α-redüktaz eksikliğinin laboratuvar tanısı, enzimin substratı ile ürünü arasındaki oransal dengesizliğe dayanır (Sınav Spotu):\n\n- **Enzimatik Blokaj:** Testis Leydig hücreleri normal veya yüksek düzeyde **Testosteron** üretir. Ancak hedef dokularda testosteronun DHT'ye dönüşümü bloke olmuştur.\n- **Serum Hormon Profili:**\n  - Serum Testosteron (T) düzeyi: **Normal veya Yüksek**\n  - Serum Dihidrotestosteron (DHT) düzeyi: **Belirgin şekilde Düşük**\n  - Serum Östrojen düzeyi: Normal veya hafif yüksek (aromatizasyonla)\n  - **Testosteron / DHT Oranı:** Normal bireylerde bu oran 10-20 arasındayken, 5α-redüktaz eksikliğinde **>30 (sıklıkla 40-60'ın üzerinde)** bulunur.\n- **hCG Stimülasyon Testi:** Prepübertal çocuklarda bazal hormonlar düşük olabileceğinden hCG uygulanarak Leydig hücreleri uyarılır; stimülasyon sonrası T/DHT oranının 30'un üzerine fırlaması tanı koydurucudur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Normal Erkek Hormon Profili vs 5α-Redüktaz Eksikliği",
                "Normal Erkek Hormon Profili",
                "Testosteron normal, DHT normal; T/DHT oranı 10-20 arasındadır; dış genitalya tam maskülinizedir.",
                "5α-Redüktaz Eksikliği (SRD5A2)",
                "Testosteron normal/yüksek, DHT çok düşüktür; T/DHT oranı >30'dur; dış genitalya yetersiz maskülinizedir."
            ),
            make_quiz(
                "Kuşkulu genitalya ile incelenen 46,XY bir bebekte hCG uyarımı sonrasında aşağıdaki hormonal tablolardan hangisinin saptanması 5α-redüktaz 2 eksikliğini en güçlü şekilde destekler?",
                [
                    {"key": "A", "text": "Yüksek testosteron, belirgin düşük DHT ve T/DHT oranının >35 olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: 5α-redüktaz eksikliğinde testosteron DHT'ye çevrilemediği için testosteron yüksek/normal, DHT çok düşük kalır ve T/DHT oranı >30-35'in üzerine çıkar."},
                    {"key": "B", "text": "Düşük testosteron, yüksek DHT ve T/DHT oranının <5 olması", "isCorrect": False, "explanation": "Bu durumda enzim hiperaktiftir, eksiklik olamaz."},
                    {"key": "C", "text": "Testosteron ve DHT'nin her ikisinin de sıfır olması", "isCorrect": False, "explanation": "Bu tablo StAR veya 17α-hidroksilaz gibi erken steroidogenez blokajlarında görülür."},
                    {"key": "D", "text": "Aşırı yüksek 17-OH progesteron ve düşük testosteron", "isCorrect": False, "explanation": "Bu durum 21-hidroksilaz eksikliği tablosudur."}
                ]
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-19-s63",
        "title": "Doğumdaki Fenotip: Kriptorşidizm, Psödovajina ve Kuşkulu Genitalya",
        "content": "Doğum anında 5α-redüktaz 2 eksikliği olan bir bebeğin dış muayenesi son derece yanıltıcı olabilir (Sınav Spotu):\n\n- **Kuşkulu Dış Genitalya:**\n  - Fetal dönemde DHT olmadığı için labioskrotal kabartılar kaynaşamaz; ayrık kalarak labia benzeri bir görünüm oluşturur.\n  - Ürogenital kıvrımlar kapanamaz; üretral açıklık fallusun tabanında, perineal bölgede kalır (**perineoskrotal hipospadias**).\n  - Fallus çok küçüktür; klitoromegali izlenimi verir (**mikrofallus**).\n  - Altta kör bir cep şeklinde sonlanan **psödovajina** (kısa vajinal poş) bulunabilir.\n- **Gonadların Durumu:**\n  - Testisler genellikle karın içinde veya inguinal kanaldadır (**kriptorşidizm**); bazen labia benzeri kabartıların içinde palpe edilebilir.\n- **Cinsiyet Tayini Yanılgısı:**\n  - Doğumda bu bebeklerin büyük çoğunluğu **kız zannedilir ve kız cinsiyetinde nüfusa kaydettirilerek** kız çocuğu gibi büyütülür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Anatomik Bölge", "Doğumdaki Muayene Bulgusu", "Embriyolojik Neden"],
                [
                    ["Fallus", "Mikrofallus (klitoromegaliye benzer)", "Genital tüberkülün DHT eksikliğinde uzayamaması"],
                    ["Üretra", "Perineoskrotal hipospadias", "Ürogenital kıvrımların ventralde birleşememesi"],
                    ["Skrotal Bölge", "Bifid skrotum / Labia benzeri yapı", "Labioskrotal kabartıların orta hatta füzyon olamaması"],
                    ["Vajen Girişi", "Kör sonlanan psödovajina", "Ürogenital sinüsün erkeksi kapanmayı tamamlayamaması"]
                ]
            ),
            make_cloze(
                "5α-redüktaz 2 eksikliği ile doğan 46,XY bebekler dış genitalyanın yetersiz maskülinizasyonu ve psödovajina varlığı nedeniyle genellikle doğumda kız olarak yetiştirilir.",
                "kız olarak yetiştirilir",
                "Bebeğin doğum anındaki dış genital görünümüne bağlı toplumsal cinsiyet yönlendirmesi"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-19-s64",
        "title": "İç Genital Yapılar: Normal Wolff Türevleri ve Müller Yokluğu",
        "content": "5α-redüktaz eksikliğini diğer CGB tablolarından ayıran en temel özellik iç genital kanalların anatomisidir (Sınav Spotu):\n\n- **Müller Kanalları Yoktur:**\n  - Testis Sertoli hücreleri embriyolojik 7. haftadan itibaren normal şekilde **AMH (MIS)** üretmiştir.\n  - Bu nedenle uterus, fallop tüpleri ve vajinanın üst 1/3 kısmı **kesinlikle bulunmaz** (uterus agenezisi).\n- **Wolff Kanalları Tam Gelişmiştir:**\n  - Wolff kanallarının gelişimi DHT'ye değil, doğrudan Leydig hücrelerinden salgılanan **yüksek lokal konsantrasyondaki Testosterona** bağımlıdır.\n  - Bu sayede hastada **epididim, vas deferens, seminal vezikül ve duktus ejakulyatorius** kusursuz olarak gelişmiştir.\n- **Kritik Ayrım:** Bu hastalarda içte erkek kanalları (Wolff) tamdır, Müller kanalları yoktur; sorun yalnızca DHT bağımlı dış genital dokulardadır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "İç Genital Yapı vs Dış Genital Yapı (5α-Redüktaz)",
                "İç Genital Kanallar (Testosteron ve AMH)",
                "AMH nedeniyle uterus ve tüp yoktur; Testosteron sayesinde epididim ve vas deferens tamamen gelişmiştir.",
                "Dış Genital Organlar (DHT Bağımlı)",
                "DHT olmadığı için penis küçüktür, üretra altta açılır, skrotum bifiddir; görünüm kuşkulu veya dişidir."
            ),
            make_quiz(
                "5α-redüktaz 2 eksikliği olan 46,XY bir hastada iç genital organların durumu ile ilgili ifadelerden hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "AMH üretimi normal olduğu için uterus yoktur, lokal testosteron sayesinde vas deferens ve epididim mevcuttur", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sertoli hücreleri normal AMH üreterek uterusu yok eder; Leydig hücreleri de testosteron üreterek Wolff türevlerini (vas deferens, epididim) tam olarak geliştirir."},
                    {"key": "B", "text": "Uterus ve fallop tüpleri normal gelişmiştir", "isCorrect": False, "explanation": "AMH varlığında uterus ve tüpler geriler, bulunamaz."},
                    {"key": "C", "text": "Vas deferens ve seminal veziküller tamamen ageneziktir", "isCorrect": False, "explanation": "Wolff kanalı testosteron ile geliştiği için vas deferens mevcuttur."},
                    {"key": "D", "text": "Bilateral overler ve uterus mevcuttur", "isCorrect": False, "explanation": "Hastada testis vardır, over yoktur."}
                ]
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-19-s65",
        "title": "Pubertede Dramatik Virilizasyon: Testosteron Patlaması",
        "content": "5α-redüktaz eksikliğinin tıptaki en ünlü dönüm noktası puberte döneminde yaşanan fizyolojik dönüşümdür (Sınav Spotu):\n\n- **Pubertal Testosteron Patlaması:**\n  - Puberteye giren bireyde hipotalamo-hipofizer aks aktive olur ve LH uyarısıyla testislerden muazzam miktarda **testosteron salgılanır**.\n  - Ayrıca pubertede karaciğer ve derideki **5α-redüktaz tip 1 (SRD5A1)** izoenzimi devreye girerek dolaşıma bir miktar DHT sağlar.\n- **Erkekleşme (Virilizasyon) Bulguları:**\n  - Klitoris zannedilen fallus hızla büyüyerek **işlevsel bir penise** dönüşür.\n  - Kas kütlesi belirgin artar, omuzlar genişler, ses kalınlaşır (larinks büyümesi).\n  - İntraabdominal veya inguinal testisler skrotal torbalara doğru iniş yapar (**desensus testis**).\n  - Yüzde ve vücutta erkek tipi kıllanma başlar.\n- **Eksik Kalan Özellikler:**\n  - Fetal dönemde DHT eksikliği nedeniyle prostat bezi gelişmemiştir (prostat rudimentary kalır).\n  - Erkek tipi androgenetik saç dökülmesi (kellik) ve şiddetli akne görülmez (çünkü saç folikülleri DHT'ye bağımlıdır).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Pubertede Erkekleşme Mekanizması",
                [
                    "1. LH Artışı: Hipofizden salgılanan yüksek LH testis Leydig hücrelerini uyarır.",
                    "2. Aşırı Testosteron: Kanda testosteron yetişkin erkek düzeylerinin bile üzerine çıkar.",
                    "3. Tip 1 Enzim Desteği: Periferik dokularda 5α-redüktaz tip 1 kısmi DHT katkısı sağlar.",
                    "4. Fallik Büyüme: Mikrofallus uzayarak penise dönüşür ve ereksiyon kabiliyeti kazanır.",
                    "5. Maskülinizasyon: Ses kalınlaşır, kas kütlesi artar ve testisler inişini tamamlar."
                ]
            ),
            make_cloze(
                "5α-redüktaz 2 eksikliği olan bireylerde pubertede aşırı artan testosteron ve devreye giren tip 1 enzim sayesinde fallik büyüme ve maskülinizasyon gerçekleşir.",
                "maskülinizasyon",
                "Puberte döneminde ses kalınlaşması, kas gelişimi ve penis büyümesi ile giden erkekleşme süreci"
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-19-s66",
        "title": "Sosyal ve Psikoseksüel Dönüşüm: Kızdan Erkeğe Cinsiyet Rolü",
        "content": "5α-redüktaz eksikliği, tıp antropolojisi ve biyopsikososyal psikiyatri açısından eşsiz bir fenomendir (Sınav Spotu):\n\n- **Guevedoces Fenomeni:** Dominik Cumhuriyeti'nde bu bireylere halk arasında '12 yaşında penis çıkanlar' anlamında *Guevedoces* veya *machihembras* adı verilmiştir.\n- **Beyin Maskülinizasyonu:** Fetal dönemde ve pubertede beynin cinsel kimlik merkezleri (hipotalamik çekirdekler) testosteronun kendisi ve östrojene aromatizasyonu ile maskülinize olur (beyin için DHT zorunlu değildir).\n- **Cinsiyet Rolü Değişimi:**\n  - Doğumdan puberteye kadar kız çocuğu olarak yetiştirilen bu bireylerin **%60-80'i pubertede kendiliğinden erkek cinsel kimliğini benimser**.\n  - Toplumda kadın rolünden erkek rolüne geçerler, isimlerini değiştirirler ve kadınlara cinsel ilgi duyarlar.\n- **Psikososyal Yaklaşım:** Bu dönüşüm, erken dönemde cerrahi cinsiyet atama operasyonlarının neden geri dönülemez zararlar verebileceğinin en somut tıbbi kanıtıdır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Çocukluk Sosyal Rolü vs Puberte Cinsiyet Kimliği",
                "Çocukluk Evresi (0-12 Yaş)",
                "Dış genitalya kız zannedildiği için kız kıyafetleri ve kız sosyal kimliği ile büyütülür.",
                "Puberte Evresi (12+ Yaş)",
                "Biyolojik virilizasyon ve beyin maskülinizasyonu ile bireylerin %60-80'i erkek kimliğine geçer."
            ),
            make_quiz(
                "Kız çocuğu olarak büyütülen 13 yaşındaki bir hastada menstrüasyon görülmemesi, klitorisin penise dönüşmesi, ses kalınlaşması ve kas gelişimi saptanıyor. Bireyin kendisini erkek olarak hissettiği öğreniliyor. En olası tanı hangisidir?",
                [
                    {"key": "A", "text": "5α-Redüktaz 2 Eksikliği", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kız yetiştirilen bir çocukta pubertede dramatik penis büyümesi, ses kalınlaşması ve erkek kimliğine geçiş klasik 5α-redüktaz 2 eksikliği tablosudur."},
                    {"key": "B", "text": "Komplet Androjen Duyarsızlık Sendromu", "isCorrect": False, "explanation": "CAIS'te reseptör olmadığı için pubertede virilizasyon olmaz, meme gelişir."},
                    {"key": "C", "text": "Turner Sendromu", "isCorrect": False, "explanation": "Turner sendromunda virilizasyon ve penis gelişimi görülmez."},
                    {"key": "D", "text": "Swyer Sendromu", "isCorrect": False, "explanation": "Swyer sendromunda gonad streak'tir, testosteron patlaması olmaz."}
                ]
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-19-s67",
        "title": "Tanısal Yöntemler: hCG Testi ve SRD5A2 Moleküler Genetiği",
        "content": "Kuşkulu genitalya veya virilizasyon ile başvuran hastada tanı algoritması basamak basamak ilerler (Sınav Spotu):\n\n- **1. Sitogenetik Analiz:**\n  - İlk adımda karyotipin **46,XY** olduğu konfirme edilir (FISH/karyotip).\n- **2. Pelvik Ultrasonografi:**\n  - Müller yapılarının (uterus ve tüpler) bulunmadığı, testislerin inguinal/skrotal yerleşimli olduğu gösterilir.\n- **3. hCG Uyarım Testi ve Hormon Düzeyleri:**\n  - Bazal ve hCG uyarısı sonrası Testosteron ve DHT ölçülür.\n  - Testosteron/DHT oranının **30'un üzerinde olması** 5α-redüktaz eksikliği lehine kuvvetli biyokimyasal kanıttır.\n- **4. İdrar Steroid Profil Analizi (GC-MS):**\n  - İdrarda 5α-tetrahidrokortizol (5α-THF) / 5β-THF oranının belirgin düşük olması tanıyı pekiştirir.\n- **5. Moleküler Genetik Doğrulama:**\n  - **SRD5A2 geninin dizi analizi (sekanslama)** ile homozigot veya compound heterozigot patojenik varyant saptanarak kesin tanı konur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "5α-Redüktaz Eksikliği Tanı Basamakları",
                [
                    "1. Karyotip: 46,XY genetik cinsiyeti doğrulanır.",
                    "2. Görüntüleme: Pelvik USG ile uterusun olmadığı, testislerin varlığı saptanır.",
                    "3. hCG Stimülasyonu: Testosteron/DHT oranının >30 olduğu biyokimyasal olarak gösterilir.",
                    "4. İdrar Steroid Profili: GC-MS ile 5α ve 5β metabolit dengesizliği kanıtlanır.",
                    "5. DNA Sekanslama: SRD5A2 genindeki mutasyon moleküler olarak gösterilir."
                ]
            ),
            make_cloze(
                "5α-redüktaz eksikliği tanısında kesin moleküler tanı SRD5A2 geninin DNA dizi analizi ile mutasyonun gösterilmesiyle konulur.",
                "SRD5A2",
                "2p23 bölgesinde yer alan 5α-redüktaz tip 2 enzimi kodlayıcı gen"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-19-s68",
        "title": "Tedavi ve Yönetim: DHT Jelleri, Cerrahi Onarımlar ve Destek",
        "content": "5α-redüktaz eksikliğinde klinik yaklaşım multidisipliner bir kurul tarafından yürütülmelidir (Sınav Spotu):\n\n- **Cinsiyet Yönelimi ve Kimlik:**\n  - Bireylerin çoğunluğu pubertede erkek kimliğini seçtiği için günümüzde erken çocuklukta geri dönüşsüz kadınlaştırma cerrahilerinden kesinlikle kaçınılmaktadır.\n  - Cinsiyet rolü kararı ailenin, psikoloğun ve çocuğun katılımıyla verilmelidir.\n- **Medikal Tedavi (Erkek Yönünde Büyütülenlerde):**\n  - Fallus boyutunu büyütmek için erken çocuklukta veya prepübertal dönemde **topikal Dihidrotestosteron (DHT) jelleri** kullanılır; bu tedavi penil dokuyu büyütür ve hipospadias cerrahisini kolaylaştırır.\n- **Cerrahi Tedavi:**\n  - Kriptorşidizm için orşiopeksi yapılır (testislerin skrotuma indirilmesi).\n  - Üretra açıklığı için kordi düzeltmesi ve üretra rekonstrüksiyonu (hipospadias onarımı) uygulanır.\n- **Fertilite Potansiyeli:**\n  - Testis dokusu spermatogenez yapabilir; semen hacmi ve prostat salgısı yetersiz olsa dahi **TESE ve intrasitoplazmik sperm enjeksiyonu (ICSI)** ile biyolojik çocuk sahibi olabilirler.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Klinik Problem", "Tedavi Yaklaşımı", "Hedef"],
                [
                    ["Mikrofallus", "Topikal transdermal DHT jeli", "Fallus boyunu uzatmak ve dokuyu olgunlaştırmak"],
                    ["Hipospadias ve Kordi", "Üretroplasti ve kordi eksizyonu", "Normal idrar akışı ve cinsel fonksiyon"],
                    ["İnmemiş Testis", "Orşiopeksi ameliyatı", "Malignite riskini azaltmak ve spermogenezi korumak"],
                    ["İnfertilite", "TESE + ICSI (Tüp bebek)", "Biyolojik babalık şansını sağlamak"]
                ]
            ),
            make_quiz(
                "5α-redüktaz 2 eksikliği tanısı konan ve erkek cinsiyetinde büyütülmesine karar verilen küçük bir çocukta mikrofallusu büyütmek amacıyla kullanılan en spesifik medikal tedavi hangisidir?",
                [
                    {"key": "A", "text": "Topikal Dihidrotestosteron (DHT) jel uygulaması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hastada testosterondan DHT yapılamadığı için doğrudan DHT preparatlarının (jel) lokal uygulanması fallik dokuyu büyüterek cerrahiye hazırlar."},
                    {"key": "B", "text": "Yüksek doz östrojen tedavisi", "isCorrect": False, "explanation": "Östrojen erkek yönünde büyütülen çocukta feminizasyon yapar."},
                    {"key": "C", "text": "Deksametazon tedavisi", "isCorrect": False, "explanation": "Deksametazon KAH tedavisidir, 5α-redüktazda yeri yoktur."},
                    {"key": "D", "text": "Spironolakton", "isCorrect": False, "explanation": "Spironolakton antiandrojenik ilaçtır, tabloyu kötüleştirir."}
                ]
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-19-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] 5-Alfa Redüktaz 2 Eksikliği ve Virilizasyon",
        "content": "Bu checkpointte 5α-redüktaz 2 eksikliğinin temel özelliklerini özetliyoruz:\n\n- **Gen ve Kalıtım:** SRD5A2 geni (2p23), otozomal resesif kalıtım, sık kurucu mutasyon p.L55Q.\n- **Biyokimya:** Testosteron normal/yüksek, DHT çok düşük; **Testosteron/DHT oranı >30-35'tir**.\n- **İç Genitalya:** AMH normal olduğu için **uterus ve tubalar yoktur**; lokal testosteron sayesinde **vas deferens, epididim ve seminal veziküller mevcuttur**.\n- **Dış Genitalya (Doğumda):** Mikrofallus, perineoskrotal hipospadias, bifid skrotum ve psödovajina vardır; sıklıkla kız olarak yetiştirilir.\n- **Puberte Virilizasyonu:** Aşırı testosteron patlaması ve Tip 1 enzim katkısıyla ses kalınlaşır, penis büyür, kaslar gelişir ve testisler iner.\n- **Kimlik Değişimi:** Bireylerin %60-80'i pubertede erkek cinsiyet kimliğini benimser.\n- **Tedavi:** Mikrofallus için **topikal DHT jeli**, orşiopeksi ve hipospadias onarımı uygulanır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Özellik", "5α-Redüktaz 2 Eksikliğindeki Durum", "Önemli Klinik Not"],
                [
                    ["Karyotip", "46,XY", "Genetik olarak erkektir"],
                    ["İç Organlar", "Uterus yok, vas deferens var", "Müller gerilemiş, Wolff tam gelişmiştir"],
                    ["T / DHT Oranı", "Aşırı yüksek (>30)", "hCG uyarısı ile teyit edilir"],
                    ["Puberte Seyri", "Güçlü virilizasyon (erkekleşme)", "Kız yetiştirilen çocuk erkek kimliğine döner"],
                    ["Prostat / Kellik", "Prostat hipoplastik, kellik görülmez", "DHT bağımlı dokular rudimenter kalır"]
                ]
            ),
            make_chain(
                "5α-Redüktaz Özet Akış Şeması",
                [
                    "1. Genetik Kusur: SRD5A2 resesif mutasyonu ile tip 2 enzim yokluğu.",
                    "2. Fetal Dönem: Yetersiz DHT ile kuşkulu genitalya ve kız yetiştirilme.",
                    "3. Korunan Yapı: Normal AMH ve testosteron ile erkek iç kanalları mevcut.",
                    "4. Puberte Patlaması: Yüksek testosteron ile dramatik erkekleşme süreci.",
                    "5. Tedavi: Topikal DHT, rekonstrüksiyon ve psikolojik destek."
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-19-s70",
        "title": "Bölüm Özeti: Enzim Eksikliğinden Androjen Duyarsızlık Sendromuna Geçiş",
        "content": "Bölüm 7 boyunca 5α-redüktaz eksikliğinin biyokimyasını, iç-dış kanal ayrımını ve pubertedeki dramatik dönüşümünü inceledik:\n\n- **Özet:** 5α-redüktaz eksikliğinde androjen üretimi ve reseptör yanıtı vardır; eksik olan tek şey periferik dönüşümdür (DHT).\n- **Sonraki Bölüm (Bölüm 8):** Hem testosteronun hem de DHT'nin bolca üretildiği ancak hedef hücre reseptörlerinin tamamen duyarsız olduğu **Androjen Duyarsızlık Sendromunu (ADS / CAIS / PAIS / Testiküler Feminizasyon) ve kör vajen tablosunu** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "5α-redüktaz 2 eksikliğinde iç genital muayenede uterusun bulunmamasının biyolojik nedeni nedir?",
                "Sertoli hücrelerinin normal AMH salgılaması",
                "Müller kanallarını gerileten fetal hormonun varlığı"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi 5α-redüktaz eksikliği olan bir bireyde puberte sonrasında BEKLENMEYEN bir bulgudur?",
                [
                    {"key": "A", "text": "Erkek tipi saç dökülmesi (androgenetik alopesi)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Androgenetik saç dökülmesi doğrudan DHT hormonuna bağımlıdır; 5α-redüktaz eksikliği olan erkeklerde kellik görülmez."},
                    {"key": "B", "text": "Ses kalınlaşması", "isCorrect": False, "explanation": "Ses kalınlaşması testosterona bağımlıdır ve pubertede gerçekleşir."},
                    {"key": "C", "text": "Kas kütlesinde artış", "isCorrect": False, "explanation": "Kas gelişimi testosteron tarafından sağlanır."},
                    {"key": "D", "text": "Fallus boyutunda büyüme", "isCorrect": False, "explanation": "Yüksek testosteron fallusu büyütür."}
                ]
            )
        ]
    })

    return slides
