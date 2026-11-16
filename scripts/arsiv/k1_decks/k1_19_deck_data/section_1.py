# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-19-s01",
        "title": "Fertilizasyon ve Üç Temel Görevi: Genetik Başlangıç",
        "content": "İnsan yaşamının biyolojik başlangıcı, haploid bir sperm ile haploid bir sekonder oositin birleşmesi olan fertilizasyondur (döllenme) (Sınav Spotu):\n\n- **Tanım:** Spermatozoonun oosit sitoplazmasına girmesiyle dişi ve erkek pronükleusları kaynaşır ve diploid (2n=46) tek bir hücre olan **zigot** meydana gelir.\n- **Fertilizasyonun Üç Temel Görevi:**\n  1. **Diploid Kromozom Sayısını Yeniden Kurmak:** Sperm, anneden gelen 23 kromozomluk takıma babanın 23 kromozomunu ekleyerek türe özgü 46 kromozomu tamamlar.\n  2. **Genetik Cinsiyeti Belirlemek:** Oosit her zaman 23,X taşır; cinsiyeti dölleyen spermin X mi (46,XX kız) yoksa Y mi (46,XY erkek) taşıdığı anında belirler.\n  3. **Embriyogenezi Başlatmak:** Oosit içinde metabolik ve hücresel reaksiyonları (kortikal granül reaksiyonu ve kalsiyum dalgalanması) tetikleyerek bölünmeyi (mitotik klivaj) başlatır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Fertilizasyonun 3 Görevi", "Biyolojik Mekanizma", "Genetik Sonuç"],
                [
                    ["1. Genetik Takım", "Haploid (n=23) + Haploid (n=23) kaynaşması", "Diploid (2n=46) kromozom sayısının restorasyonu"],
                    ["2. Cinsiyet Tayini", "X taşıyan veya Y taşıyan sperm girişi", "46,XX (dişi) veya 46,XY (erkek) genetik cinsiyet"],
                    ["3. Aktivasyon", "Kalsiyum salınımı ve oosit 2. mayozunun tamamlanması", "Mitotik bölünmenin ve embriyonik gelişimin başlaması"]
                ]
            ),
            make_quiz(
                "İnsan embriyogenezinde fertilizasyon anında gerçekleşen ve sonraki tüm cinsiyet gelişim basamaklarının temelini oluşturan olay hangisidir?",
                [
                    {"key": "A", "text": "Dölleyen spermin X veya Y taşımasına bağlı olarak genetik cinsiyetin belirlenmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Fertilizasyon genetik cinsiyeti belirleyen temel olaydır (X veya Y kromozomu girişi)."},
                    {"key": "B", "text": "Overlerin hemen östrojen salgılamaya başlaması", "isCorrect": False, "explanation": "Overler fertilizasyonda henüz yoktur, 6. haftadan sonra belirir."},
                    {"key": "C", "text": "Testosteronun dış genitalyayı penise dönüştürmesi", "isCorrect": False, "explanation": "Dış genitalya 9-12. haftalarda farklılaşır."},
                    {"key": "D", "text": "Müller kanallarının rahme dönüşmesi", "isCorrect": False, "explanation": "Kanal gelişimi embriyonik dönemin ilerleyen evrelerindedir."}
                ]
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-19-s02",
        "title": "Zigottan Blastosite Erken Dönem: Morula ve 6. Gün İmplantasyonu",
        "content": "Fertilizasyondan sonra zigot, fallop tüpü boyunca uterus kavitesine doğru ilerlerken hızlı mitotik bölünmelere (klivaj) uğrar (Sınav Spotu):\n\n- **Embriyonik Genom Aktivasyonu:** Konseptustaki zigotik genler **4 ila 8 hücreli aşamada** transkripsiyona başlar (öncesinde maternal mRNA kullanılır).\n- **Morula Aşaması (16 Hücre):** Fertilizasyondan sonraki 3-4. günde dut meyvesine benzeyen 16 hücreli yoğun küreye **morula** denir (kompaksiyon başlar).\n- **Blastosist Aşaması (32-64 Hücre):** Hücreler arasına sıvı dolarak blastosist boşluğu (blastosöl) oluşur; dışta trofoblast (plasentayı yapar), içte embriyoblast (iç hücre kitlesi - embriyoyu yapar) ayrılır.\n- **İmplantasyon (6. Gün):** Blastosist fertilizasyondan sonraki **6. günde** endometriyuma tutunur ve gömülür; trofoblastlardan salgılanan insan koryonik gonadotropini (**hCG**) maternal kanda pozitifleşir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Fertilizasyondan İmplantasyona Erken Gelişim Basamakları",
                [
                    "1. Zigot: Spermin oositi döllemesiyle oluşan tek diploid hücre.",
                    "2. Klivaj: 4-8 hücreli evrede embriyonik genomun aktifleşmesi.",
                    "3. Morula: 16 hücreli dut benzeri sıkılaşmış hücre kümesi (3-4. gün).",
                    "4. Blastosist: İç hücre kitlesi ve trofoblastın ayrıldığı sıvı dolu yapı.",
                    "5. İmplantasyon: 6. günde endometriyuma gömülme ve hCG salgılanması."
                ]
            ),
            make_cloze(
                "Fertilizasyondan sonra oluşan blastosist yapısı gebeliğin altıncı gününde endometriyuma implante olur ve hCG salgılanmaya başlar.",
                "altıncı gününde",
                "Embriyonun rahim duvarına tutunduğu post-konsepsiyonel gün"
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-19-s03",
        "title": "Cinsiyet Farklılaşmasının Dört Düzeyi: Genetikten Sosyal Role",
        "content": "İnsan cinsiyeti tek bir anda oluşup biten bir olgu değildir; embriyolojik yaşamdan erişkinliğe uzanan 4 ardışık düzeyde şekillenir (Sınav Spotu):\n\n- **1. Genetik (Kromozomal) Cinsiyet:**\n  - Fertilizasyon anında kurulur (46,XX veya 46,XY).\n- **2. Gonadal Cinsiyet:**\n  - 6-7. haftalarda genetik komutla bipotansiyel gonadın **testis veya over** yönünde farklılaşmasıdır.\n- **3. Fenotipik (Duktal ve Dış Genital) Cinsiyet:**\n  - Gonadlardan salgılanan hormonların (AMH, Testosteron, DHT) etkisiyle iç genital kanalların (Wolff veya Müller) ve dış genitalyanın gelişmesidir.\n- **4. Psikososyal ve İkincil Cinsiyet:**\n  - Pubertede hormonlarla ikincil seks karakterlerinin (meme, kıllanma, ses) oturması, bireyin kendi hissettiği cinsel kimlik ve toplumun yüklediği toplumsal cinsiyet rolüdür.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Genetik Cinsiyet vs Fenotipik Cinsiyet",
                "Genetik Cinsiyet (Fertilizasyon)",
                "Karyotip düzeyindedir (46,XX veya 46,XY); Y kromozomu üzerindeki SRY geninin varlığına bağlıdır.",
                "Fenotipik Cinsiyet (Embriyogenez & Puberte)",
                "İç kanallar, dış genitalya ve sekonder karakterlerdir; hormonların ve reseptörlerin işlevine bağlıdır."
            ),
            make_quiz(
                "Bireyin kromozomal yapısının 46,XY olmasına rağmen androjen reseptör duyarsızlığı nedeniyle dış görünüşünün kadın olması hangi iki cinsiyet düzeyi arasındaki uyumsuzluğu gösterir?",
                [
                    {"key": "A", "text": "Genetik cinsiyet ile fenotipik cinsiyet arasındaki uyumsuzluk", "isCorrect": True, "explanation": "Doğru cevap A'dır: Genetik olarak 46,XY erkek olmasına rağmen dış genital fenotipin kadın olması genetik-fenotipik cinsiyet ayrışmasıdır."},
                    {"key": "B", "text": "Gonadal cinsiyet ile genetik cinsiyetin tam özdeşliği", "isCorrect": False, "explanation": "Burada tam bir fenotipik tezatlık vardır."},
                    {"key": "C", "text": "Yalnızca yasal kimlik ile doğum tarihi uyumsuzluğu", "isCorrect": False, "explanation": "Hukuki/bürokratik bir konu değildir."},
                    {"key": "D", "text": "Mitotik klivaj hızındaki azalma", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-19-s04",
        "title": "Cinsiyet Kromozomları ve Y Kromozomunun Belirleyici Gücü",
        "content": "Memelilerde ve insanda cinsiyet tayininde temel kural, Y kromozomunun varlığı veya yokluğudur (Sınav Spotu):\n\n- **Genel Genetik Kural:**\n  - Karyotipte **en az bir adet işlevsel Y kromozomu bulunması, embriyonun erkek yönünde farklılaşması için şarttır ve yeterlidir**.\n  - Kaç tane X kromozomu olursa olsun (örn. 47,XXY, 48,XXXY, 49,XXXXY), ortamda Y kromozomu varsa birey gonadal olarak testis geliştirir ve erkek fenotipine yönelir.\n- **Kadın Yönünün Varsayılan Olması:**\n  - Y kromozomu bulunmadığında (örn. 46,XX veya 45,X Turner), embriyo kendiliğinden dişi yönünde gelişir.\n- **Eşitlik İlkesi:** Erkek spermlerinin yarısı X, yarısı Y taşıdığı için döllenmede kız veya erkek olma teorik olasılığı %50'dir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Karyotip", "Y Kromozomu Varlığı", "Gelişen Gonad", "Temel Fenotipik Yön"],
                [
                    ["46,XY", "Var (Normal)", "Testis", "Normal Erkek"],
                    ["46,XX", "Yok (Normal)", "Over", "Normal Kadın"],
                    ["47,XXY (Klinefelter)", "Var (1 adet Y)", "Testis (küçük/disgenetik)", "Erkek Fenotipi"],
                    ["45,X (Turner)", "Yok", "Streak Gonad (Over taslağı)", "Dişi Fenotipi"]
                ]
            ),
            make_cloze(
                "İnsan embriyogenezinde kaç tane X kromozomu bulunursa bulunsun ortamda en az bir Y kromozomu bulunması embriyonun erkek yönünde farklılaşmasını sağlar.",
                "Y kromozomu",
                "Erkek cinsiyeti belirleyen temel seks kromozomu"
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-19-s05",
        "title": "Lyon Hipotezi ve Barr Cisimciği: X Kromozom İnaktivasyonu",
        "content": "Dişilerde iki adet X kromozomu (XX), erkeklerde ise tek bir X kromozomu (XY) bulunması gen dozajı dengesizliği yaratır; bu denge Mary Lyon'un keşfettiği mekanizma ile kurulur (Sınav Spotu):\n\n- **Lyon Hipotezi (X İnaktivasyonu):**\n  - Erken embriyonik dönemde (blastosist aşamasında), dişi hücrelerindeki iki X kromozomundan biri **rastgele (random) ve kalıcı olarak inaktive edilir**.\n  - İnaktive olan X kromozomu heterokromatin haline gelerek büzülür.\n- **Barr Cisimciği (Seks Kromatini):**\n  - İnaktif X kromozomu, interfaz çekirdeğinde nükleer membranın hemen iç yüzünde koyu boyanan bir kitle olarak görülür (**Barr cisimciği**).\n- **Formül Kuralı:** Barr cisimciği sayısı = **(Toplam X Sayısı - 1)**.\n  - Normal kadın (46,XX): 1 Barr cisimciği,\n  - Normal erkek (46,XY): 0 Barr cisimciği,\n  - Turner sendromu (45,X): 0 Barr cisimciği,\n  - Klinefelter sendromu (47,XXY): 1 Barr cisimciği,\n  - Trizomi X (47,XXX): 2 Barr cisimciği.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Karyotip", "Toplam X Sayısı", "Barr Cisimciği Sayısı (X-1)", "Klinik Durum"],
                [
                    ["46,XY", "1", "0", "Normal Erkek"],
                    ["46,XX", "2", "1", "Normal Kadın"],
                    ["45,X", "1", "0", "Turner Sendromu"],
                    ["47,XXY", "2", "1", "Klinefelter Sendromu"],
                    ["47,XXX", "3", "2", "Trizomi X Kadını"]
                ]
            ),
            make_quiz(
                "Ağız mukoza sürüntüsünde yapılan seks kromatini incelemesinde hücre çekirdeklerinde 2 adet Barr cisimciği saptanan bir bireyin seks kromozomu içeriği hangisidir?",
                [
                    {"key": "A", "text": "47,XXX (veya 48,XXXY)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Barr cisimciği formülü (Toplam X - 1)'dir; 2 Barr cisimciği olan bireyde 3 adet X kromozomu bulunur (47,XXX veya 48,XXXY)."},
                    {"key": "B", "text": "46,XY", "isCorrect": False, "explanation": "Erkekte 0 Barr cisimciği vardır."},
                    {"key": "C", "text": "45,X", "isCorrect": False, "explanation": "Turner sendromunda 0 Barr cisimciği vardır."},
                    {"key": "D", "text": "46,XX", "isCorrect": False, "explanation": "Normal kadında 1 Barr cisimciği vardır."}
                ]
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-19-s06",
        "title": "Bipotansiyel Gonad Dönemi (Post-konsepsiyonel 6. Hafta)",
        "content": "Embriyonik gelişimin ilk haftalarında erkek ve dişi embriyolar morfolojik olarak birbirinin tamamen aynısıdır (Sınav Spotu):\n\n- **Bipotansiyel (İndifferan) Evre:**\n  - Fertilizasyondan sonraki **ilk 6 hafta boyunca** gelişen gonad taslağı hem testise hem de overe dönüşme potansiyeline sahiptir (**bipotansiyel gonad**).\n  - Bu dönemde her iki cinste de hem erkek kanal taslağı (**Wolff / Mezonefrik**) hem de dişi kanal taslağı (**Müller / Paramezonefrik**) yan yana bulunur.\n- **Ürogenital Kabartı (Ridge):**\n  - Gonadlar intermediate mezodermden gelişen ürogenital kabartının medial yüzünde belirir.\n- **Kritik Eşik (6. Haftanın Sonu):**\n  - Post-konsepsiyonel 6. haftanın sonuna kadar cinsiyet morfolojik olarak ayırt edilemez; 7. haftadan itibaren genetik komutla ayrışma başlar.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Bipotansiyel Dönem (İlk 6 Hafta) vs Farklılaşma Dönemi (7. Hafta+)",
                "Bipotansiyel Dönem (0-6. Hafta)",
                "Gonad belirsizdir; hem Wolff hem Müller kanalları aynı anda mevcuttur; cinsiyet ayırt edilemez.",
                "Farklılaşma Dönemi (7. Hafta ve Sonrası)",
                "SRY varlığında testis ve Wolff kanalları gelişir; SRY yokluğunda over ve Müller kanalları gelişir."
            ),
            make_cloze(
                "İnsan embriyosunda post-konsepsiyonel altıncı haftanın sonuna kadar gonadlar her iki cinse de dönüşebilen bipotansiyel gonad yapısındadır.",
                "altıncı haftanın",
                "İndifferan gonad döneminin sona erdiği embriyonik hafta"
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-19-s07",
        "title": "Alfred Jost Deneyleri (1947): Testisin Rolü ve Dişi Varsayılanı",
        "content": "Fransız embriyolog Alfred Jost'un 1947 yılında tavşan embriyoları üzerinde yaptığı cerrahi deneyler, genital gelişimin temel kurallarını ortaya koymuştur (Sınav Spotu):\n\n- **Jost'un Tarihi Deneyleri:**\n  - **1. Deney (Erken Gonadektomi):** Hem erkek (XY) hem dişi (XX) embriyoların gonadları farklılaşma başlamadan önce cerrahi olarak çıkarıldığında;\n    - **Sonuç:** Bütün embriyolar (genetik olarak XY olanlar dahil!) **tamamen dişi iç ve dış genital organları** (uterus, vajen, klitoris) geliştirdi!\n  - **2. Deney (Testis Grefti):** Dişi (XX) embriyoya testis dokusu nakledildiğinde;\n    - Nakil yapılan tarafta Müller kanalları eridi ve Wolff kanalları gelişti.\n- **Jost Paradigması:**\n  - Dişi gelişimi **'varsayılan (default)'** yoldur; aktif bir hormonal uyarı gerektirmez.\n  - Erkek gelişimi için ise testisin bizzat varlığı ve salgıladığı **iki ayrı hormon (Testosteron ve AMH)** zorunludur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "Alfred Jost'un 1947 Deney Sonuçları",
                [
                    "1. Erken Gonad Eksizyonu: Embriyonun gonadları 6. haftadan önce çıkarılır.",
                    "2. Hormonsuz Ortam: Testosteron ve AMH salgılanamaz.",
                    "3. Müller Kanalının Korunması: AMH olmadığı için Müller kanalları kendiliğinden uterusa döner.",
                    "4. Dişi Fenotip: Genetik cinsiyet XY olsa bile birey dişi iç ve dış organları geliştirir."
                ]
            ),
            make_quiz(
                "1947 yılında embriyolarda gonadların çıkarılması durumunda genetik erkek (XY) embriyoların da dişi iç ve dış genital organları geliştirdiğini kanıtlayan ünlü Fransız embriyolog kimdir?",
                [
                    {"key": "A", "text": "Alfred Jost", "isCorrect": True, "explanation": "Doğru cevap A'dır: Alfred Jost tavşan deneyleriyle dişi yönün varsayılan olduğunu ve erkek gelişimi için testisin şart olduğunu kanıtlamıştır."},
                    {"key": "B", "text": "Mary Lyon", "isCorrect": False, "explanation": "X inaktivasyonunu bulmuştur."},
                    {"key": "C", "text": "Robert Koch", "isCorrect": False, "explanation": "Bakteriyoloji uzmanıdır."},
                    {"key": "D", "text": "Edward Jenner", "isCorrect": False, "explanation": "Çiçek aşısını bulmuştur."}
                ]
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-19-s08",
        "title": "Primordial Germ Hücrelerinin Göçü: Vitellustan Gonada",
        "content": "Geleceğin sperm ve yumurtalarını oluşturacak olan primordial germ hücreleri (PGH) gonadların içinde doğmaz, dışarıdan göç eder (Sınav Spotu):\n\n- **Köken ve İlk Görülme:**\n  - PGH'ler gebeliğin 3-4. haftasında **vitellus kesesinin (yolk sac) allantois yakınındaki endoderminde** belirir.\n- **Ameboid Göç Yolu:**\n  - 4-6. haftalar arasında PGH'ler ameboid hareketlerle arka bağırsağın mezenterinden geçerek dorsal karın duvarındaki **ürogenital kabartılara (gonadal kabartı)** göç ederler.\n- **Kritik Klinik İlke:**\n  - Eğer primordial germ hücreleri ürogenital kabartıya ulaşamazsa veya göç sırasında ölürse, **gonadlar gelişemez ve germ hücresinden yoksun fibröz 'çizgi gonad' (streak gonad)** tablosu ortaya çıkar.\n  - Göç yolundan sapan başıboş germ hücreleri koksiks veya mediasten gibi yerlerde **teratomlara** yol açabilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Başarılı Germ Hücresi Göçü vs Göç Kusuru",
                "Başarılı Göç (Normal Gonad)",
                "PGH'ler vitellus kesesinden genital kabartıya ulaşır; normal spermatogenez veya oogenez başlar.",
                "Göç Kusuru (Streak Gonad)",
                "PGH'ler kabartıya ulaşamaz; gonad germ hücresinden yoksun fibröz bir bağ dokusu bandı (streak) olarak kalır."
            ),
            make_cloze(
                "Gelecekte sperm ve yumurtaya dönüşecek olan primordial germ hücreleri gebeliğin üçüncü haftasında vitellus kesesi duvarında belirir ve genital kabartıya göç eder.",
                "vitellus kesesi",
                "Primordial germ hücrelerinin ilk ortaya çıktığı embriyonik kese"
            )
        ]
    })

    # Slide 9 - CHECKPOINT 1
    slides.append({
        "id": "k1-19-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Fertilizasyon ve Cinsiyet Farklılaşmasına Giriş",
        "content": "Bu checkpointte fertilizasyonu ve cinsiyet gelişiminin embriyolojik temellerini özetliyoruz:\n\n- **Fertilizasyon:** 3 görevi vardır: Diploid 46 kromozomu tamamlamak, genetik cinsiyeti belirlemek (X veya Y sperm), embriyogenezi başlatmak.\n- **Klivaj ve İmplantasyon:** 4-8 hücrede embriyonik genom açılır; 16 hücrede morula, 32+ hücrede blastosist; **6. günde implantasyon ve hCG salgılanması** başlar.\n- **Cinsiyet Düzeyleri:** Genetik cinsiyet (XX/XY) $\\to$ Gonadal cinsiyet (testis/over) $\\to$ Fenotipik cinsiyet (Wolff/Müller kanalları ve dış genitalya) $\\to$ Sosyal cinsiyet.\n- **Y Kromozomu:** Erkek yönü için en az bir Y şarttır; Y yoksa dişi yönü gelişir.\n- **Lyon Hipotezi:** Kadında bir X inaktive olur ve Barr cisimciği (X-1) oluşur.\n- **Bipotansiyel Gonad:** İlk 6 hafta boyunca gonad her iki cinse de dönüşebilir.\n- **Alfred Jost (1947):** Gonadlar erken çıkarılırsa embriyo dişi gelişir; dişi varsayılandır, erkek gelişimi için testis hormonları (testosteron ve AMH) şarttır.\n- **Primordial Germ Hücreleri:** Vitellus kesesinden 4-6. haftalarda genital kabartıya göç eder.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Embriyolojik Evre", "Zaman Aralığı", "Temel Cinsiyet Gelişim Olayı"],
                [
                    ["Fertilizasyon", "0. Gün", "Genetik cinsiyetin (46,XX veya 46,XY) belirlenmesi"],
                    ["İmplantasyon", "6. Gün", "Blastosistin gömülmesi ve hCG pozitifleşmesi"],
                    ["Germ Hücresi Göçü", "4-6. Hafta", "Vitellus kesesinden genital kabartıya göç"],
                    ["Bipotansiyel Gonad", "İlk 6 Hafta", "Hem Wolff hem Müller kanallarının bir arada bulunması"],
                    ["Gonadal Farklılaşma", "7. Hafta başı", "SRY varlığında testis, yokluğunda over yönünde ayrışma"]
                ]
            ),
            make_chain(
                "Cinsiyet Farklılaşmasının İlk Basamakları",
                [
                    "1. Genetik Belirlenme: Dölleyen sperm X veya Y kromozomunu getirir.",
                    "2. 6. Gün Tutunma: Blastosist implante olur ve gebelik başlar.",
                    "3. Germ Hücresi Göçü: PGH'ler vitellustan genital kabartıya yerleşir.",
                    "4. Bipotansiyel Eşik: 6. haftanın sonuna kadar her iki cinsiyet taslağı korunur.",
                    "5. Hormonal Komuta Geçiş: Jost modeline göre testis varsa erkek, yoksa dişi gelişimi başlar."
                ]
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-19-s10",
        "title": "Bölüm Özeti: Embriyolojiden Gonadal Farklılaşma Genlerine Geçiş",
        "content": "Bölüm 1 boyunca fertilizasyonun görevlerini, erken bölünmeleri, bipotansiyel gonad evresini ve Jost deneylerini inceledik:\n\n- **Özet:** Bipotansiyel gonad 6. haftaya kadar indiferandır; erkek gelişimi için Y kromozomunun aktif sinyali gerekir.\n- **Sonraki Bölüm (Bölüm 2):** Y kromozomu üzerindeki anahtar gen olan **SRY'yi (41. gün piki), otozomal testis faktörü SOX9'u, Kampomelik displaziyi, SF1 ve WT1 genlerini ve testis farklılaşmasının genetik kontrolünü** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "Dişi memeli hücrelerinde inaktive olan X kromozomunun interfaz çekirdeğinde koyu bir kitle olarak görülmesine ne ad verilir?",
                "Barr cisimciği (Seks kromatini)",
                "Mary Lyon'un X inaktivasyon hipotezine bağlı çekirdek kütlesi"
            ),
            make_quiz(
                "İnsan embriyosunda blastosistin endometriyuma implante olduğu ve maternal kanda hCG'nin pozitifleştiği post-konsepsiyonel gün hangisidir?",
                [
                    {"key": "A", "text": "6. gün", "isCorrect": True, "explanation": "Doğru cevap A'dır: Blastosist fertilizasyondan sonraki 6. günde implante olur ve hCG üretimi başlar."},
                    {"key": "B", "text": "1. gün", "isCorrect": False, "explanation": "1. günde tek hücreli zigottur."},
                    {"key": "C", "text": "14. gün", "isCorrect": False, "explanation": "Primitif çizgi evresidir."},
                    {"key": "D", "text": "28. gün", "isCorrect": False, "explanation": "Nöral tüp kapanma evresidir."}
                ]
            )
        ]
    })

    return slides
