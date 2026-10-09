# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-14-s61",
        "title": "Tıbbi Tedaviler ve Aşıların Salgınlardaki Yeri",
        "content": "Salgın hastalıkların kontrolünde 20. yüzyılın en büyük halk sağlığı devrimleri aşılar ve antibiyotikler olmuştur:\n\n- **Tarihi Kalkan:** Aşılar ve antibiyotikler, geçmişte insanlığı kırıp geçiren veba, kolera, tifo, çiçek, çocuk felci ve difteri gibi devasa salgınların büyük bir kısmını durdurmuştur.\n- **Kombine DTP Aşısı (Sınav Spotu):** DSÖ verilerine göre difteri-tetanoz-boğmaca (DTP) kombine aşısı günümüzde küresel olarak **çocukların %86'sını** bu ölümcül bakteriyel hastalıklardan korumaktadır.\n- **Toplum Düzeyinde Etki:** Kitlesel aşılama, duyarlı konak havuzunu kurutarak patojenin toplumda dolaşımını imkansız hale getirir ve aşılanamayan bebekleri/bağışıklığı baskılanmış bireyleri de dolaylı olarak korur (sürü bağışıklığı).",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Dünya Sağlık Örgütü (DSÖ) verilerine göre kombine difteri-tetanoz-boğmaca (DTP) aşısı küresel olarak çocukların yaklaşık yüzde kaçını korumaktadır?",
                [
                    {"key": "A", "text": "%25", "isCorrect": False, "explanation": "%25 çok düşüktür; rutin çocukluk çağı aşı kapsayıcılığı küresel düzeyde çok daha yüksektir."},
                    {"key": "B", "text": "%50", "isCorrect": False, "explanation": "%50 küresel ortalamanın oldukça altındadır."},
                    {"key": "C", "text": "%86", "isCorrect": True, "explanation": "Doğru cevap C'dir: Ders notundaki spot bilgiye göre DTP kombine aşısı küresel olarak çocukların yaklaşık %86'sını korumaktadır."},
                    {"key": "D", "text": "%100", "isCorrect": False, "explanation": "Hiçbir aşı küresel olarak %100 kapsayıcılığa henüz ulaşamamıştır; savaş bölgeleri ve yoksul ülkelerde aşıya erişim açığı vardır."}
                ]
            ),
            make_cloze(
                "DSÖ verilerine göre difteri-tetanoz-boğmaca aşısı dünyadaki çocukların yaklaşık yüzde 86'sını korumaktadır.",
                "86",
                "DTP aşısının küresel çocuk koruma yüzdesi"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-14-s62",
        "title": "Antiviraller, Monoklonal Antikorlar ve İlaç Eşitsizliği",
        "content": "20. yüzyılın son çeyreği ve 21. yüzyıl, enfeksiyon tedavisinde moleküler biyolojinin zirveye ulaştığı bir dönem olmuştur:\n\n- **Antiviral Devrim:** Özellikle 1980'lerden sonra HIV/AIDS pandemisinde geliştirilen kombine antiretroviral tedaviler (HAART), ölümcül bir virüsü kronik yönetilebilir bir hastalığa dönüştürmüştür.\n- **Monoklonal Antikorlar (mAbs):** SARS-CoV-2 ve Ebola için laboratuvarda üretilen yüksek afiniteli nötralizan antikorlar klinik yanıtı hızlandırmıştır.\n- **Kitlesel Erişim ve Maliyet Engeli (Sınav Spotu):** Monoklonal antikorlar ve yeni nesil antiviraller **aşırı pahalıdır** ve üretim kapasiteleri kısıtlıdır. Bu nedenle yoksul ülkelerde veya milyonlarca insanı etkileyen salgınlarda **kitlesel halk sağlığı uygulaması için uygun ve erişilebilir değildirler**.\n- **Halk Sağlığı Dersi:** Pahalı butik tedaviler yerine herkese eşit ulaşabilen aşılar, hijyen ve destekleyici bakım daima önceliklidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Monoklonal Antikorlar vs Kitlesel Halk Sağlığı Araçları",
                "Monoklonal Antikorlar (Pahalı ve Butik)",
                "Bireysel düzeyde virüsü hızla nötralize eder; ancak binlerce dolarlık maliyeti nedeniyle kitlelere ulaştırılamaz.",
                "Kitlesel Halk Sağlığı Araçları (Aşı ve Destek)",
                "Düşük maliyetlidir, tüm topluma milyonlarca doz uygulanabilir ve salgının belini kırar."
            ),
            make_recall(
                "Monoklonal antikorlar gibi modern moleküler tedaviler neden büyük salgınların kontrolünde tek başına yeterli olamaz?",
                "Çünkü aşırı yüksek maliyetleri, karmaşık soğuk zincir/infüzyon gereksinimleri ve sınırlı küresel üretim kapasiteleri nedeniyle kitlesel kullanıma uygun değillerdir."
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-14-s63",
        "title": "Sağlık İşgücünün Korunması: En Değerli ve Yenilenemez Kaynak",
        "content": "Bir salgında en gelişmiş ilaçlar, en modern hastane binaları ve binlerce solunum cihazı olsa bile, onları uygulayacak hekim ve hemşire yoksa hiçbir şey ifade etmez:\n\n- **Sağlık Personelinin Vazgeçilmezliği (Sınav Spotu):** Tüm tedaviler ancak **kalifiye, sağlıklı, eğitimli ve özverili sağlık personeli** uygulandığında hayat kurtarır.\n- **Tükenme ve Enfeksiyon Riski:** Sağlık çalışanları patojenle en yüksek viral/bakteriyel yük altında doğrudan temas eden gruptur. Korunmayan bir sağlık personeli hem hastalanıp sistemi felç eder, hem de süper-bulaştırıcı haline gelerek hastaneyi bulaş yuvasına çevirir.\n- **Yenilenemez Kaynak:** Yeni bir yoğun bakım hekimi veya enfeksiyon hemşiresi yetiştirmek en az 5-10 yıl sürer; salgın anında sağlık işgücünün kaybı telafi edilemez bir felakettir.\n- **Koruma Şartı:** Sağlık işgücünün fiziksel, zihinsel ve enfeksiyon açısından korunması, salgın yanıtının sürdürülebilmesi için 1 numaralı önceliktir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Salgın yönetiminde 'sağlık işgücünün korunmasının' birincil derecede hayati olmasının temel nedeni hangisidir?",
                [
                    {"key": "A", "text": "Sağlık çalışanlarının hastane yönetim kurulu toplantılarını düzenlemesi", "isCorrect": False, "explanation": "İdari toplantılar krizdeki temel neden değildir."},
                    {"key": "B", "text": "Tüm tıbbi tedavilerin ancak kalifiye ve özverili personel uyguladığında yarar sağlaması ve işgücünün hızla yenilenememesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Ders notunda açıkça vurgulandığı gibi, tedaviler ancak kalifiye sağlık personeli varsa yararlıdır ve sağlık işgücünün korunması yanıtın sürdürülmesi için elzemdir."},
                    {"key": "C", "text": "Sağlık çalışanlarının hiç ilaç kullanmadan bağışık kabul edilmesi", "isCorrect": False, "explanation": "Sağlık personeli de normal insanlar gibi enfeksiyona son derece açıktır."},
                    {"key": "D", "text": "Hastanelerdeki cihazların kendi kendini otomatik tamir edebilmesi", "isCorrect": False, "explanation": "Cihazlar hekim olmadan hayat kurtaramaz."}
                ]
            ),
            make_cloze(
                "Tüm tıbbi tedaviler ancak kalifiye ve özverili sağlık personeli uygulandığında yararlıdır.",
                "personeli",
                "Tıbbi müdahaleyi hayata geçiren vazgeçilmez aktör"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-14-s64",
        "title": "Kişisel Koruyucu Ekipman (KKE) ve Enfeksiyon Önleme-Kontrol (IPC)",
        "content": "Sağlık çalışanlarını ve hastaları korumanın temel teknik omurgası **Enfeksiyon Önleme ve Kontrol (IPC - Infection Prevention and Control)** ve **Kişisel Koruyucu Ekipman (KKE)** standartlarıdır:\n\n- **Bulaş Yoluna Uygun KKE Seçimi:**\n  - **Damlacık:** Cerrahi maske, göz koruyucu (siperlik/gözlük), önlük, eldiven.\n  - **Hava Yolu (Aerosol):** N95 / FFP2 / FFP3 maskeler, negatif basınçlı izolasyon odaları.\n  - **Temas / Vücut Sıvısı (Ebola, KKKA):** Sıvı geçirmez tulum, çift eldiven, çizme koruyucu, tam yüz koruması.\n- **Kritik Süreç: Donning ve Doffing:**\n  - **Donning (Giyme):** Sırasıyla ve dikkatle giyilir.\n  - **Doffing (Çıkarma - En Riskli Aşama):** Sağlık çalışanlarının en sık enfekte olduğu an KKE'yi çıkarma anıdır! Dış yüzey kontamine olduğu için çıkarma işlemi ayna karşısında veya bir gözlemci eşliğinde, her katmanda el dezenfeksiyonu yapılarak adım adım yürütülmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "KKE Çıkarma (Doffing) Sırasında Kontaminasyonu Önleme",
                [
                    "1. Risk Bilinci: KKE'nin dış yüzeyinin yoğun patojenle kaplı olduğu kabul edilir.",
                    "2. En Kirli Katmanın Çıkarılması: Dış eldivenler ters yüz edilerek çıkarılır ve el hijyeni sağlanır.",
                    "3. Önlük/Tulum Çıkarılması: Boyun bağları çözülür, öne dokunmadan içten dışa yuvarlanarak çıkarılır.",
                    "4. Gözlük ve Maske Çıkarılması: Önden asla tutulmaz; arkadaki lastiklerden tutularak atılır.",
                    "5. Son El Hijyeni: Alkol bazlı dezenfektanla eller en az 20 saniye ovalanır."
                ]
            ),
            make_table(
                ["İzolasyon Türü", "Gereken Temel KKE", "Hastanede Oda Koşulu"],
                [
                    ["Standart Önlemler", "El hijyeni, duruma göre eldiven ve önlük", "Standart hasta odası"],
                    ["Damlacık İzolasyonu", "Cerrahi maske, göz koruması (1-2 metre mesafe)", "Tek kişilik oda veya kohortlama"],
                    ["Hava Yolu İzolasyonu", "N95/FFP2 maske, sızdırmaz tulum", "Negatif basınçlı oda (saatte 12 hava değişimi)"],
                    ["Kanamalı Ateş (Ebola/KKKA)", "Sıvı geçirmez tulum, çift eldiven, tam siperlik, çizme", "Yüksek düzey izolasyon ünitesi, çift kapılı giriş"]
                ]
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-14-s65",
        "title": "Destekleyici Tedavinin Hayat Kurtarıcı Gücü",
        "content": "Modern tıpta sıkça düşülen bir yanılgı, bir virüse karşı spesifik antiviral yoksa tıbbın çaresiz kaldığı inancıdır. Bu inanç tamamen yanlıştır:\n\n- **Spesifik Tedavi Olmasa Bile (Sınav Spotu):** Bir patojene karşı geliştirilmiş doğrudan bir aşı veya mucizevi bir antiviral ilaç olmasa dahi, **yeterli ve kaliteli klinik destekleyici yöntemler binlerce hayat kurtarır**.\n- **Destekleyici Bakımın Bileşenleri:**\n  - **Sıvı ve Elektrolit Dengesi:** Ağır diyare ve kusmayla kaybedilen sıvının (oral rehidrasyon veya IV ringer laktat) yerine konması hipovolemik şoku ve böbrek yetmezliğini önler.\n  - **Oksijen Desteği ve Solunum Yönetimi:** Hipokseminin erken fark edilip oksijen, yüksek akışlı nazal kanül veya mekanik ventilasyonla düzeltilmesi.\n  - **Asit-Baz Dengesi ve Glukoz Kontrolü:** Metabolik asidozun ve hipogliseminin düzeltilmesi.\n  - **İkincil Bakteriyel Enfeksiyonların Tedavisi:** Virüsle zayıflayan akciğerde süperenfeksiyonu hedefleyen rasyonel antibiyotikler.\n- **Sonuç:** Vücuda bağışıklık sistemi virüsü temizleyene kadar zaman kazandırılır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Sadece 'Mucize İlaç' Beklentisi vs Kaliteli Destekleyici Bakım",
                "Spesifik İlaç Beklentisi (Pasif)",
                "İlaç yoksa hastanın öleceği varsayılır; hasta susuzluk, hipoksi ve şoktan kaybedilir.",
                "Kaliteli Destekleyici Bakım (Aktif Mücadele)",
                "Sıvı, elektrolit, oksijen ve beslenme desteğiyle organ yetmezlikleri önlenir; hastaların büyük kısmı iyileşir."
            ),
            make_cloze(
                "Spesifik bir antiviral ilaç bulunmasa bile yeterli klinik destekleyici yöntemler ve sıvı-elektrolit yönetimi hayat kurtarır.",
                "destekleyici",
                "Semptomları ve organ fonksiyonlarını ayakta tutan tedavi türü"
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-14-s66",
        "title": "Tarihi Kanıt: 2014 Ebola Salgınında Ölüm Oranının %75'ten %33'e Düşmesi",
        "content": "Destekleyici bakımın olağanüstü gücünü kanıtlayan tıp tarihinin en çarpıcı örneği Batı Afrika Ebola salgınıdır:\n\n- **2014 Batı Afrika Ebola Gerçeği (Sınav Sorusu):** 2014 yılında Gine, Liberya ve Sierra Leone'de patlak veren Ebola salgınında onaylanmış hiçbir antiviral ilaç veya aşı bulunmuyordu.\n- **İlk Tablo:** Sahada sağlık altyapısının çöktüğü ilk haftalarda vaka ölüm oranı (CFR) **yaklaşık %75** civarındaydı; hastalar ağır kusma, kanama ve diyareye bağlı dehidratasyondan ölüyordu.\n- **Destekleyici Bakım Devrimi:** Sağlık çalışanlarının korunması sağlandıktan sonra hastalara yoğun agresif intravenöz sıvı, elektrolit replasmanı, kan basıncı kontrolü ve beslenme desteği sağlandı.\n- **Çarpıcı Sonuç:** Tek bir spesifik antiviral ilaç dahi verilmeden, sadece **daha iyi destekleyici bakım sayesinde ölüm oranı %75'ten yaklaşık %33'e geriledi!**\n- **Halk Sağlığı Dersi:** Temel klinik bakım ve hekimlik sanatı, en ölümcül patojenin dahi yıkımını yarıdan fazla azaltabilir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "2014 Batı Afrika Ebola salgınında spesifik bir ilaç olmamasına rağmen daha iyi destekleyici bakım ile ölüm oranı yaklaşık hangi seviyeden hangi seviyeye düşürülmüştür?",
                [
                    {"key": "A", "text": "%100'den %90'a", "isCorrect": False, "explanation": "Ölüm oranı %100 değildi ve %90 başarı sayılmaz."},
                    {"key": "B", "text": "%75'ten %33'e", "isCorrect": True, "explanation": "Doğru cevap B'dir: Ders notunda açıkça vurgulandığı üzere, 2014 Batı Afrika Ebola salgınında daha iyi destekleyici bakımla ölüm oranı yaklaşık %75'ten %33'e düşürülmüştür."},
                    {"key": "C", "text": "%50'den %48'e", "isCorrect": False, "explanation": "Fark bu kadar küçük değildir."},
                    {"key": "D", "text": "%20'den %1'e", "isCorrect": False, "explanation": "Ebola ölüm hızı %20 gibi düşük bir seviyede başlamamıştır."}
                ]
            ),
            make_recall(
                "2014 Ebola salgınında ölüm oranının %75'ten %33'e düşmesi tıp öğrencilerine hangi temel ilkeyi öğretir?",
                "Spesifik bir antiviral veya antibiyotik olmasa dahi, agresif sıvı-elektrolit ve klinik destekleyici bakımın hastaların hayatını kurtarmada devasa bir güç olduğunu gösterir."
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-14-s67",
        "title": "Triyaj, İzolasyon Odaları ve Nozokomiyal Bulaşın Önlenmesi",
        "content": "Salgınlarda hastaneler birer şifa merkezi olabileceği gibi, tedbir alınmazsa salgının en büyük bulaş yuvasına (amplifikasyon merkezi) dönüşebilir:\n\n- **Nozokomiyal Bulaş Riski:** Bekleme salonlarında öksüren bir hastanın diğer kronik hastaları veya refakatçileri enfekte etmesi.\n- **Girişte Triyaj (Kapı Önü Ayrımı):**\n  - Hastane ana kapısında tüm hastalar ateş ve solunum semptomları açısından sorgulanır.\n  - Şüpheli hastalar derhal cerrahi maske takılarak ayrı bir 'izolasyon/triyaj polikliniğine' yönlendirilir.\n- **Hastane İçi Kohortlama:** Pozitif hastalar ayrı bir serviste veya binada (kohort) toplanır; bu servise giriş çıkışlar sınırlandırılır.\n- **Personel Ayrımı:** Salgın servisinde çalışan hekim ve hemşirelerin temiz servislerde (onkoloji, yenidoğan) nöbet tutması kesinlikle yasaklanır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Hastane Alanı", "Uygulanan Önlem", "Amacı"],
                [
                    ["Ana Giriş / Kapı", "Termal kamera, semptom sorgulama, maske dağıtımı", "Şüpheli vakaları temiz bekleme salonlarına girmeden yakalamak"],
                    ["Triyaj Alanı", "Fiziksel mesafe (en az 1.5 m), hızlı antijen testi", "Acil hastaları bulaştırıcılık durumuna göre ayırmak"],
                    ["İzolasyon Servisi", "Negatif basınç, sıkı KKE, ziyaretçi yasağı", "Patojenin hastane havalandırmasına ve koridorlara yayılmasını kesmek"]
                ]
            ),
            make_cloze(
                "Hastanelerde şüpheli vakaların ana giriş kapısında semptomlarına göre ayrılmasına ve yönlendirilmesine triyaj denir.",
                "triyaj",
                "Hastaları öncelik ve bulaş riskine göre tasnif etme süreci"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-14-s68",
        "title": "Toplum Sağlığı Çalışanları, Ebeler, Hemşireler ve Gönüllülerin Rolü",
        "content": "Salgın mücadelesi yalnızca büyük üniversite hastanelerindeki yoğun bakım ünitelerinde değil, esas olarak mahallelerde ve evlerde kazanılır:\n\n- **Her Düzeyde Fark Yaratan Sağlık Ordusu (Sınav Spotu):** Toplum sağlığı çalışanları, ebeler, hemşireler, aile hekimleri ve gönüllüler salgın yönetiminin en ön cephesindedir.\n- **Ev Ziyaretleri ve Filyasyon:** Ebeler ve toplum sağlığı çalışanları ev ev dolaşarak temaslıları tarar, karantinadaki hastaların ateşini ölçer ve ilaçlarını teslim eder.\n- **Güven Köprüsü:** Yerel halk hastanedeki yabancı bir profesörden ziyade kendi mahallesindeki ebe veya hemşireye güvenir; aşı iknasında bu çalışanlar kilit rol oynar.\n- **Gönüllülerin Seferberliği:** Kızılay ve sivil toplum gönüllüleri karantinadaki yaşlıların gıda ve sıcak yemek ihtiyaçlarını karşılayarak evde kalmalarını mümkün kılar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Üçüncü Basamak Hastane Odaklı vs Birinci Basamak Toplum Odaklı Yanıt",
                "Sadece 3. Basamak Odaklı (Geç Müdahale)",
                "Hastalar ancak organ yetmezliği geliştiğinde yoğun bakıma gelir; sistem hızla kilitlenir.",
                "1. Basamak ve Toplum Sağlığı Odaklı (Erken ve Yaygın)",
                "Ebeler, hemşireler ve filyasyon ekipleri vakaları evinde tespit eder, yayılımı keser ve hastaneleri korur."
            ),
            make_quiz(
                "Salgın yönetiminde birinci basamak sağlık çalışanlarının (ebe, hemşire, toplum sağlığı çalışanı) en kritik gücü nedir?",
                [
                    {"key": "A", "text": "Toplumla doğrudan temas kurarak güven köprüsü oluşturmaları, filyasyonu ve erken tespiti sahada yürütmeleri", "isCorrect": True, "explanation": "Doğru cevap A'dır: Ders notunda vurgulandığı gibi, toplum sağlığı çalışanları, ebeler ve hemşireler her düzeyde fark yaratır ve yerel güveni temsil eder."},
                    {"key": "B", "text": "Hastanelerde kalp nakli ameliyatlarını tek başlarına yapmaları", "isCorrect": False, "explanation": "Kalp nakli cerrahi bir uzmanlık alanıdır."},
                    {"key": "C", "text": "İlaç fiyatlarını uluslararası borsada belirlemeleri", "isCorrect": False, "explanation": "İlaç fiyatları ekonomi bakanlıkları ve firmalarla ilgilidir."},
                    {"key": "D", "text": "Salgın döneminde tüm sağlık ocaklarını kapatıp tatile çıkmaları", "isCorrect": False, "explanation": "Birinci basamak salgının en aktif çalışan kalesidir."}
                ]
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-14-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Sağlık İşgücünün Korunması ve Klinik Yönetim",
        "content": "Bu checkpointte klinik yönetim prensiplerini ve sağlık işgücünün korunmasının hayati önemini pekiştiriyoruz:\n\n- **Aşıların Gücü:** DTP kombine aşısı dünyadaki çocukların %86'sını korumaktadır.\n- **İlaç Eşitsizliği:** Monoklonal antikorlar ve yeni antiviraller aşırı pahalıdır; kitlesel halk sağlığı uygulaması için uygun değildir.\n- **Sağlık İşgücünün Korunması:** Tedaviler ancak kalifiye ve özverili personel uyguladığında yararlıdır; sağlık çalışanlarının korunması yanıtın sürdürülmesi için zorunludur.\n- **KKE ve Doffing:** En yüksek enfeksiyon riski ekipmanı çıkarma (doffing) aşamasındadır; adım adım protokol uygulanmalıdır.\n- **Destekleyici Tedavi:** Spesifik ilaç olmasa bile sıvı-elektrolit ve klinik bakım hayat kurtarır.\n- **Ebola 2014 Kanıtı:** İyi destekleyici bakımla ölüm oranı %75'ten %33'e düşürülmüştür.\n- **Birinci Basamak:** Ebe, hemşire ve toplum sağlığı çalışanları sahadaki güvenin ve filyasyonun omurgasıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Klinik Salgın Yönetimi ve Personel Güvenliği Zinciri",
                [
                    "1. Giriş Triyajı: Şüpheli hastalar ana kapıda ayrılır ve damlacık/temas izolasyonuna alınır.",
                    "2. KKE Güvenliği: Sağlık personeli tam koruyucu donanımla hastaya yaklaşır, doffingte hata yapılmaz.",
                    "3. Agresif Destekleyici Bakım: Sıvı-elektrolit, oksijen ve beslenme desteği hızla başlanır.",
                    "4. Nozokomiyal Önleme: Kohortlama ve servis izolasyonuyla hastane içi bulaş sıfırlanır."
                ]
            ),
            make_table(
                ["Klinik Parametre", "Salgındaki Karşılığı", "Halk Sağlığı Hedefi"],
                [
                    ["DTP Aşısı Kapsayıcılığı", "Küresel çocukların %86'sı korunur", "Toplum bağışıklığı ve çocuk ölümlerini önleme"],
                    ["Ebola 2014 Destek Bakımı", "Ölüm oranı %75'ten %33'e geriledi", "Spesifik ilaç yokluğunda dahi hayat kurtarma"],
                    ["Doffing Eğitimi", "KKE'yi kontamine olmadan çıkarma", "Sağlık personelinin enfekte olmasını engelleme"]
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-14-s70",
        "title": "Mini Vaka: Kırım-Kongo Kanamalı Ateşi (KKKA) Kliniğinde Personel Korunması",
        "content": "İç Anadolu'da kırsal bir devlet hastanesi acil servisine vücudundan kene çıkaran, burun kanaması, yüksek ateş ve trombositopenisi (PLT: 18.000/uL) olan 48 yaşında bir çiftçi getiriliyor:\n\n- **Acil Hekimi Yaklaşımı:**\n  - Hekim şüpheli KKKA tanısıyla hastayı derhal tek kişilik yüksek izolasyon odasına alıyor.\n  - Hastaya kan alma veya damar yolu açma işlemi sırasında çift eldiven, sıvı geçirmez tulum, koruyucu gözlük ve N95 maske takılıyor.\n  - Personel iğne batması riskine karşı kesici-delici alet kutusunu yatak başına getiriyor.\n- **Klinik Tedavi:** Hastaya derhal taze donmuş plazma, trombosit süspansiyonu, agresif IV hidrasyon ve destekleyici bakım başlanıyor.\n- **Sonuç:** Doğru KKE ve doffing kuralları sayesinde tek bir sağlık çalışanına dahi bulaş olmadan, hasta 10 günlük destekleyici tedaviyle tamamen iyileşerek taburcu ediliyor.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Klinik Karar: KKKA Şüpheli Hastada İğne Batması Riski",
                "KKKA şüpheli kanamalı hastadan kan alırken çömez bir stajyer hekimin eldivensiz yaklaştığını ve aceleyle iğne kapağını iki eliyle kapatmaya (recapping) çalıştığını gördünüz. İlk hamleniz ne olmalıdır?",
                [
                    {
                        "text": "Ses çıkarmayıp işlemi bitirmesini beklemek",
                        "outcome": "Hayati tehlike: İğne batmasıyla virüs doğrudan kana geçer ve sağlık çalışanı ölümcül KKKA tablosuna girer.",
                        "isCorrect": False
                    },
                    {
                        "text": "Hemen müdahale ederek iğne kapağını kapatmasını durdurmak, stajyeri uyararak KKE giydirmek ve iğneyi tek elle veya doğrudan atık kutusuna atmasını sağlamak",
                        "outcome": "Mükemmel enfeksiyon kontrolü: İğne batması önlenir, sağlık işgücü korunur ve hastane içi ölümcül kaza engellenir.",
                        "isCorrect": True
                    },
                    {
                        "text": "Stajyeri hemen hastaneden kovmak ve tutanak tutmak",
                        "outcome": "Yetersiz ve geç müdahale: Önemli olan kazayı o saniye fiziksel olarak önlemektir.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada KKKA şüpheli hastanın bakımında sağlık çalışanlarının enfekte olmasını engelleyen en kritik uygulama hangisidir?",
                [
                    {"key": "A", "text": "Sıvı geçirmez KKE kullanımı, güvenli doffing ve iğne batmalarının önlenmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kanamalı ateşlerde virüs vücut sıvılarıyla ve kanla bulaşır; sıvı geçirmez KKE ve kesici alet güvenliği personeli korur."},
                    {"key": "B", "text": "Hastaya yüksek doz aspirin verilmesi", "isCorrect": False, "explanation": "Aspirin trombositleri inhibe eder ve kanamayı artırarak öldürür."},
                    {"key": "C", "text": "Hastanın açık bahçede bekletilmesi", "isCorrect": False, "explanation": "İzolasyon odasında takip gerekir."},
                    {"key": "D", "text": "Tüm hastane çalışanlarının aynı gün istifa etmesi", "isCorrect": False, "explanation": "Mantık dışıdır."}
                ]
            )
        ]
    })

    return slides
