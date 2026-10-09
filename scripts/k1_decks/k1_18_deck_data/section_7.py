# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-18-s61",
        "title": "Sosyal Hekimliğin Doğuşu: Hastalıkların Sosyoekonomik Belirleyicileri",
        "content": "19. yüzyılın sonlarına doğru tıpta mikrobiyolojik devrim yaşanırken, hekimler mikropların tek başına hastalık yapmaya yetmediğini fark etmeye başladılar (Sınav Spotu):\n\n- **Sosyal Belirleyiciler Gerçeği:**\n  - Tüberküloz basili zengin bir malikanede oturan bir soyluyu da, havasız bir fabrikada çalışan bir tekstil işçisini de enfekte edebilirdi.\n  - Ancak işçi yoksulluk, kötü beslenme, aşırı çalışma ve nemli barınma koşulları nedeniyle ölürken, soylu kişi hastalığı hafifçe atlatıyordu.\n- **Biyomedikal Modelin Sınırları:**\n  - Sadece mikrobu öldürmeye çalışan biyomedikal model yetersizdi; mikrobu besleyen **sosyal, ekonomik, kültürel ve çevresel eşitsizliklerin** ortadan kaldırılması gerekiyordu.\n- **Sosyal Hekimlik Disiplini:** Hekimliğin yalnızca bir biyoloji alanı değil, toplumun sosyoekonomik yapısıyla iç içe geçmiş kamusal bir bilim olduğu anlayışı doğdu.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Yalnızca Biyomedikal Model vs Sosyal Hekimlik Modeli",
                "Yalnızca Biyomedikal Model",
                "Hastalığı sadece mikrop, hücre veya molekülden ibaret görür; hastanın gelirini, evini ve işini hesaba katmaz.",
                "Sosyal Hekimlik Modeli",
                "Hastalığı üreten asıl zeminin yoksulluk, adaletsizlik ve olumsuz yaşam koşulları olduğunu kabul eder."
            ),
            make_quiz(
                "Hastalıkların oluşumunda ve seyrinde biyolojik etkenlerin yanı sıra gelir düzeyi, barınma, beslenme ve sosyal adaletin rolünü inceleyen tıp yaklaşımına ne ad verilir?",
                [
                    {"key": "A", "text": "Sosyal hekimlik", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sosyal hekimlik, sağlığın sosyoekonomik belirleyicilerini merkeze alan yaklaşımdır."},
                    {"key": "B", "text": "Adli tıp", "isCorrect": False, "explanation": "Yasal ve hukuki otopsi tıp alanıdır."},
                    {"key": "C", "text": "Spor hekimliği", "isCorrect": False, "explanation": "Sporcuların sağlığıyla ilgilenir."},
                    {"key": "D", "text": "Estetik tıp", "isCorrect": False, "explanation": "Kozmetik cerrahi ve dermatolojidir."}
                ]
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-18-s62",
        "title": "Alfred Grotjahn (1869-1931) ve Sosyal Patoloji Kuramı",
        "content": "Alman hekim Alfred Grotjahn, sosyal hekimliğin akademik ve bilimsel temellerini atan kurucu teorisyendir (Sınav Spotu):\n\n- **Sosyal Patoloji (Soziale Pathologie - 1912):**\n  - Grotjahn, Berlin Üniversitesi'nde sosyal hekimlik kürsüsünü kuran ilk profesördür.\n  - 'Sosyal Patoloji' adlı başyapıtında hastalıkların toplum içindeki dağılımını sosyoekonomik faktörlerle açıkladı.\n- **Temel Tezi:**\n  - *'Hekimlik ve halk sağlığı hizmetleri yalnızca zengin ve seçkin bir zümre için bir lüks değil, tüm halk kitleleri için anayasal bir haktır; kamu bu hizmetleri ücretsiz ve nitelikli olarak sağlamakla yükümlüdür.'*\n- **Riskli Gruplar Kavramı:** Küçük çocuklar, gebe ve lohusa anneler, okul çocukları, ağır sanayi işçileri ve kimsesizlerin bulaşıcı hastalıklardan öncelikle korunmasını savunmuştur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Grotjahn'ın Sosyal Patoloji Yaklaşımı",
                [
                    "1. Sosyal Sınıf Analizi: Hastalıkların zengin ve yoksul mahallelerdeki sıklığı kıyaslanır.",
                    "2. Riskli Grupların Tespiti: Çocuklar, gebeler ve işçiler öncelikli koruma alanı ilan edilir.",
                    "3. Kamusal Görev: Sağlık hizmetinin devlet tarafından tüm kitlelere hak olarak sunulması savunulur.",
                    "4. Sosyal Hijyen Yasaları: Sosyal sigortalar ve koruyucu hekimlik politikaları yasalaşır."
                ]
            ),
            make_cloze(
                "Sağlık hizmetlerinin yalnızca seçkinler için değil tüm halk için bir hak olduğunu savunan ve Sosyal Patoloji kitabını yazan Alman tıp profesörü Alfred Grotjahn'dır.",
                "Alfred Grotjahn",
                "Sosyal hekimliğin ve sosyal patolojinin kurucusu kabul edilen Alman hekim"
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-18-s63",
        "title": "Grotjahn'ın Sosyal Hekimlik İlkeleri: 'Önemli Hastalık' Ölçütleri",
        "content": "Alfred Grotjahn'ın formüle ettiği sosyal hekimlik ilkeleri günümüzde halk sağlığının temel yasalarıdır (Sınav Spotu):\n\n- **1. İlke (Önemli Hastalık Ölçütü):**\n  - Bir toplumda kaynakların hangi hastalıklara ayrılacağını belirleyen altın kuraldır:\n  - **'En önemli hastalıklar; en çok öldüren, en sık görülen ve en çok sakat bırakan hastalıklardır.'**\n  - Nadir görülen ilginç hastalıklar yerine, halkı kitleler halinde sakat bırakan ve öldüren hastalıklara öncelik verilmelidir.\n- **2. İlke (Sosyal Koşullanma):**\n  - Sağlık düzeyini belirleyen biyolojik ve fizik çevre etmenlerini koşullayan ve yöneten asıl güç **sosyal ve ekonomik etkenlerdir**.\n- **3. İlke (Toplumsal Sorumluluk):**\n  - Bir kişinin hastalığı yalnızca o bireyin kişisel meselesi değildir; ailesinden başlayarak **tüm toplumun ortak sorunudur**.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Grotjahn'ın Sosyal Hekimlik İlkesi", "İçerik ve Anlamı", "Halk Sağlığı Planlamasına Etkisi"],
                [
                    ["1. Önemli Hastalık İlkesi", "En çok öldüren, en sık görülen ve en çok sakat bırakan hastalık önemlidir", "Bütçe ve sağlık personeli öncelikli sorunlara tahsis edilir"],
                    ["2. Sosyoekonomik Belirleyicilik", "Biyolojik çevreyi sosyal ve ekonomik koşullar şekillendirir", "Yoksullukla mücadele edilmeden sağlık düzelemez"],
                    ["3. Toplumsal Bütünlük", "Bir bireyin hastalığı tüm toplumun sorunudur", "Bulaşıcı hastalıklarda karantina ve toplumsal koruma esastır"]
                ]
            ),
            make_quiz(
                "Alfred Grotjahn'ın sosyal hekimlik ilkelerine göre bir hastalığın halk sağlığı planlamasında 'en önemli hastalık' sayılmasının üç temel ölçütü hangisidir?",
                [
                    {"key": "A", "text": "En çok öldüren, en sık görülen ve en çok sakat bırakan hastalık olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Grotjahn'ın klasik kuralına göre en sık görülen, en çok sakat bırakan ve en çok öldüren hastalık en önemlidir."},
                    {"key": "B", "text": "En pahalı ilaçlarla tedavi edilebilen ve nadir görülen hastalık olması", "isCorrect": False, "explanation": "Nadir hastalıklar halk sağlığı önceliği değildir."},
                    {"key": "C", "text": "Yalnızca krallarda ve zengin soylularda ortaya çıkması", "isCorrect": False, "explanation": "Sosyal hekimliğin tam zıddıdır."},
                    {"key": "D", "text": "Yalnızca cerrahi ameliyatla düzeltilebilmesi", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-18-s64",
        "title": "Rudolf Virchow: 'Tıp Bir Sosyal Bilimdir, Politika Geniş Kapsamlı Tıptır'",
        "content": "Modern hücresel patolojinin kurucusu olan büyük hekim Rudolf Virchow (1821-1902), aynı zamanda radikal bir sosyal hekimlik savunucusuydu (Sınav Spotu):\n\n- **1848 Yukarı Silezya Tifüs Salgını Araştırması:**\n  - Prusya hükümeti 27 yaşındaki genç patolog Virchow'u Silezya'daki yoksul dokuma işçileri arasındaki tifüs salgınını incelemeye gönderdi.\n- **Tarihi Rapor:**\n  - Virchow raporunda salgının nedeninin yalnızca tifüs basili değil; yoksulluk, açlık, cehalet, ezilmişlik ve adaletsizlik olduğunu yazdı.\n  - Tedavi olarak ilaç değil; **'Tam demokrasi, eğitim, köylüye toprak, adil vergi sistemi ve özgürlük'** önerdi!\n- **Tarihe Geçen Sözü:**\n  - *'Tıp bir sosyal bilimdir ve politika geniş kapsamlı tıptan başka bir şey değildir.' (Die Medizin ist eine soziale Wissenschaft, und die Politik ist weiter nichts als Medizin im Großen.)*",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Virchow'un Hücresel Patolojisi vs Sosyal Tıbbı",
                "Hücresel Patoloji (Omnis cellula e cellula)",
                "Tüm hastalıkların hücre hasarından kaynaklandığını kanıtlayan biyolojik devrim.",
                "Sosyal Hekimlik (Politika Geniş Kapsamlı Tıptır)",
                "Hücreyi hasta eden asıl gücün adaletsiz toplumsal ve siyasal düzen olduğunu savunan sosyal felsefe."
            ),
            make_cloze(
                "Yukarı Silezya tifüs salgınından sonra 'Tıp bir sosyal bilimdir ve politika geniş kapsamlı tıptan başka bir şey değildir' diyen ünlü hekim Rudolf Virchow'dur.",
                "Rudolf Virchow",
                "Hücresel patolojinin ve sosyal tıbbın büyük Alman kurucusu"
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-18-s65",
        "title": "20. Yüzyılda İnsan Hakları ve Sağlıkta Fırsat Eşitliği",
        "content": "20. yüzyılda tıp felsefesine ve halk sağlığına yapılan en büyük entelektüel katkı 'İnsan Hakları ve Eşitlik' kavramlarının kabulüdür (Sınav Spotu):\n\n- **Lüks Olmaktan Çıkan Sağlık:**\n  - Sağlık geçmişte parası olanın satın alabildiği bireysel bir ayrıcalıkken; 20. yüzyılda doğuştan kazanılan temel bir **insan hakkı** olarak tescillenmiştir.\n- **Sağlıkta Fırsat Eşitliği (Equity in Health):**\n  - Günümüz halk sağlığının en temel sloganı: **'Sağlığın korunması ve hastalıkların iyileştirilmesinde fırsat eşitliğidir.'**\n  - Coğrafi, ekonomik, etnik veya cinsiyet ayrımı olmaksızın her yurttaşın aynı kalitede sağlık hizmetine engelsizce ulaşabilmesi hedeflenir.\n- **İnsan Hakları Evrensel Beyannamesi (Madde 25 - 1948):**\n  - 'Herkesin kendisinin ve ailesinin sağlığı ve refahı için beslenme, giyim, konut ve tıbbi bakım hakkı vardır.'",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Sağlık Hakkının Evrenselleşme Süreci",
                [
                    "1. Ayrıcalık Dönemi: Sağlık hizmeti yalnızca soylu ve varlıklı sınıflara aittir.",
                    "2. Sosyal Sigortalar: 19. yüzyıl sonu Almanya'da işçi sınıfına ilk sağlık güvenceleri başlar.",
                    "3. İnsan Hakları Evrensel Bildirisi (1948): Tıbbi bakımın tüm insanların doğal hakkı olduğu ilan edilir.",
                    "4. Fırsat Eşitliği: Her bireye ihtiyacı olduğu anda ve ihtiyacı kadar eşit sağlık hizmeti sunulması ilkesi oturur."
                ]
            ),
            make_quiz(
                "20. yüzyılda halk sağlığı düşüncesine yapılan en büyük kavramsal katkı ve günümüz çağdaş halk sağlığının ana sloganı hangisidir?",
                [
                    {"key": "A", "text": "Sağlığın korunması ve hastalıkların iyileştirilmesinde fırsat eşitliği", "isCorrect": True, "explanation": "Doğru cevap A'dır: 20. yüzyılın en büyük katkısı insan hakları ve sağlıkta fırsat eşitliği ilkesinin evrenselleşmesidir."},
                    {"key": "B", "text": "Yalnızca vergi ödeyenlerin hastanelerden faydalanması", "isCorrect": False, "explanation": "Eşitlik ilkesine tamamen aykırıdır."},
                    {"key": "C", "text": "Tüm hastanelerin özel şirketlere devredilmesi", "isCorrect": False, "explanation": "Halk sağlığı felsefesiyle bağdaşmaz."},
                    {"key": "D", "text": "Bulaşıcı hastalıklarda devletin hiçbir müdahalede bulunmaması", "isCorrect": False, "explanation": "İhmaldir."}
                ]
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-18-s66",
        "title": "İkinci Dünya Savaşı Sonrası Yoksulluk ve Yunanistan Deneyimi",
        "content": "İkinci Dünya Savaşı sonrasında yaşanan trajik deneyimler halk sağlığı anlayışının şekillenmesinde dönüm noktası olmuştur (Sınav Spotu):\n\n- **Savaş Sonrası Yıkım ve Yoksulluk:**\n  - II. Dünya Savaşı Avrupa'yı harabeye çevirmiş, açlık, tifüs, tüberküloz ve çocuk ölümleri tavan yapmıştır.\n- **Tarihi 'Yunanistan Deneyimi':**\n  - Savaş sonrası uluslararası yardım kuruluşları Yunanistan'daki ağır beslenme bozukluğu (malnütrisyon) çeken bebek ve çocukları lüks hastanelere yatırdı.\n  - Çocuklar modern tıbbın tüm imkanlarıyla tedavi edildi, kilo aldı ve tamamen iyileşerek taburcu edildi.\n  - Ancak ailelerinin yanına dönen çocuklar **birkaç ay sonra aynı hastalık ve açlıkla yeniden hastaneye düştüler**!\n- **Çıkarılan Büyük Ders:**\n  - Hastalıkların asıl kök nedeni **yaşadıkları ortam, topluluk, aile ve yoksulluktur**.\n  - Bireyi hastanede iyileştirmek yetmez; **ortamı, aileyi ve toplumu iyileştiren koruyucu halk sağlığı hizmetleri** kurulmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Hastanede Bireysel Tedavi vs Toplumsal Çevre İyileştirmesi",
                "Yalnızca Hastanede Tedavi (Yunanistan Hatası)",
                "Çocuk hastanede iyileştirilir ancak yoksul ve sağlıksız evine dönünce hemen yeniden hastalanır.",
                "Toplumsal Halk Sağlığı Çözümü",
                "Ailenin beslenmesi, temiz su ve barınma koşulları düzeltilerek hastalığın tekrarı kökten önlenir."
            ),
            make_cloze(
                "II. Dünya Savaşı sonrasında hastanede iyileştirilen çocukların evlerine dönünce yeniden hastalanmasıyla asıl nedenin aile ve çevre koşulları olduğunu gösteren tarihi olay Yunanistan deneyimidir.",
                "Yunanistan deneyimi",
                "Hastanede iyileştirmenin yetmediğini kanıtlayan savaş sonrası tarihi sağlık tecrübesi"
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-18-s67",
        "title": "Dünya Sağlık Örgütü'nün (DSÖ - WHO) Kuruluşu (1948) ve Sağlık Tanımı",
        "content": "Birleşmiş Milletler bünyesinde küresel sağlık koordinasyonunu sağlamak amacıyla 7 Nisan 1948 tarihinde Dünya Sağlık Örgütü (WHO) kurulmuştur (Sınav Spotu):\n\n- **Dünya Sağlık Günü:** DSÖ Anayasası'nın yürürlüğe girdiği **7 Nisan** her yıl tüm dünyada 'Dünya Sağlık Günü' olarak kutlanır.\n- **DSÖ'nün Devrimsel Sağlık Tanımı:**\n  - 'Sağlık; yalnızca hastalık veya sakatlığın olmayışı değil;\n  - **BEDENEN, RUHEN VE SOSYAL YÖNDEN TAM BİR İYİLİK HALİDİR.**'\n- **Tanımın Önemi:**\n  1. Sağlığı negatif bir kavram olmaktan (hastalığın yokluğu) çıkarıp pozitif bir 'tam iyilik hali' olarak tanımlamıştır.\n  2. Biyolojik sağlığın yanına **ruhsal ve sosyal boyutları** eşit ağırlıkta yerleştirmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Sağlığın Üç Temel Boyutu (DSÖ)", "Kapsadığı İyilik Hali", "Örnek Gösterge"],
                [
                    ["1. Bedensel (Fiziksel) Boyut", "Organların ve sistemlerin biyolojik ve anatomik kusursuz işleyişi", "Hastalık, enfeksiyon veya sakatlık olmaması"],
                    ["2. Ruhsal (Mental) Boyut", "Bireyin kendisiyle ve çevresiyle barışık, stresle başa çıkabilen ruh hali", "Depresyon, anksiyete ve psikotik bozukluk olmaması"],
                    ["3. Sosyal Boyut", "Bireyin toplum içinde üretken, ilişkileri sağlıklı ve güvencede olması", "Toplumsal dayanışma, adil gelir ve sosyal güvence"]
                ]
            ),
            make_quiz(
                "Dünya Sağlık Örgütü'nün (DSÖ) 1948 Anayasası'nda yer alan evrensel tanımına göre sağlık ne demektir?",
                [
                    {"key": "A", "text": "Yalnızca hastalık veya sakatlığın olmayışı değil, bedenen, ruhen ve sosyal yönden tam bir iyilik halidir", "isCorrect": True, "explanation": "Doğru cevap A'dır: DSÖ sağlığı fiziksel, ruhsal ve sosyal tam bir iyilik hali olarak tanımlamıştır."},
                    {"key": "B", "text": "Kişinin hiçbir ilaç kullanmadan çalışabilme gücüdür", "isCorrect": False, "explanation": "Eksik ve dar bir tanımdır."},
                    {"key": "C", "text": "Hastanede yatış gerektiren bir enfeksiyonun bulunmamasıdır", "isCorrect": False, "explanation": "Yalnızca biyomedikal kısıtlı bakıştır."},
                    {"key": "D", "text": "Kan basıncı ve kan şekerinin normal sınırlarda olmasıdır", "isCorrect": False, "explanation": "Yalnızca fizyolojik laboratuvar parametresidir."}
                ]
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-18-s68",
        "title": "Kentucky Üniversitesi ve Toplum Hekimliği (Deuschle) Modeli",
        "content": "Geleneksel halk sağlığı kürsüleri tıp fakültelerinde genellikle sadece teorik dersler verirken, 1960'larda tıp eğitimini doğrudan toplum içine sokan yeni bir model doğdu (Sınav Spotu):\n\n- **Kurt W. Deuschle ve Kentucky Modeli:**\n  - 'Toplum Hekimliği' (Community Medicine) terimi ve eğitim modeli ilk kez ABD'de **Kentucky Üniversitesi Tıp Fakültesi'nde** Kurt W. Deuschle ve arkadaşları tarafından kuruldu.\n- **Modelin İlkeleri:**\n  1. Tıp öğrencileri hastane duvarlarının dışına çıkarılır; toplumun içine, köylere, yoksul mahallelere götürülür.\n  2. Hekimlik bir **sağlık ekibi** (hekim, hemşire, ebe, sağlık memuru, sosyal hizmet uzmanı) ile birlikte yürütülür.\n  3. Toplumun öncelikli sağlık sorunları epidemiyolojik yöntemlerle sahada bizzat tespit edilir.\n  4. Koruyucu ve tedavi edici hizmetler toplum içinde bir arada (entegre) sunulur.\n- **Türkiye'ye Etkisi:** Bu model, Prof. Dr. Nusret Fişek tarafından Hacettepe Toplum Hekimliği Enstitüsü'ne ve Türk sağlık reformuna ilham kaynağı olmuştur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Kentucky Toplum Hekimliği Eğitim Aşamaları",
                [
                    "1. Saha İntörnlüğü: Hekim adayları hastaneden çıkarılıp kırsal sağlık ocaklarına yerleştirilir.",
                    "2. Ekip Çalışması: Hekim ebe ve hemşireyle birlikte bir sağlık ekibi lideri olarak çalışır.",
                    "3. Bölge Taraması: Hane halkı tespit fişleriyle tüm toplumun riskleri haritalanır.",
                    "4. Entegre Hizmet: Aşı, gebe takibi ve poliklinik muayenesi aynı çatı altında verilir."
                ]
            ),
            make_cloze(
                "Sağlık ekibiyle toplum içinde koruyucu ve tedavi edici hekimliği birleştiren toplum hekimliği modeli ilk kez Kentucky Üniversitesi'nde Kurt Deuschle tarafından kurulmuştur.",
                "Kentucky Üniversitesi",
                "Toplum hekimliği kavramının ilk doğduğu Amerikan üniversitesi"
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-18-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Sosyal Hekimlik ve Küresel Sağlık Örgütlenmesi",
        "content": "Bu checkpointte sosyal hekimliğin kuruluşunu ve DSÖ'nün ilkelerini özetliyoruz:\n\n- **Sosyal Hekimlik:** Hastalıkların arkasındaki asıl gücün sosyoekonomik adaletsizlikler olduğunu savunur.\n- **Alfred Grotjahn (1912):** Sosyal patolojinin kurucusudur; sağlık hizmetinin kamu güvencesinde bir hak olduğunu belirtmiştir.\n- **Grotjahn Kuralı:** 'En önemli hastalıklar en çok öldüren, en sık görülen ve en çok sakat bırakan hastalıklardır.'\n- **Rudolf Virchow:** 'Tıp bir sosyal bilimdir ve politika geniş kapsamlı tıptan başka bir şey değildir.'\n- **Yunanistan Deneyimi:** Çocukları hastanede iyileştirmenin yetmediğini, aileyi ve çevreyi düzeltmek gerektiğini kanıtlamıştır.\n- **DSÖ (1948):** 7 Nisan'da kuruldu; sağlığı 'bedenen, ruhen ve sosyal yönden tam bir iyilik hali' olarak tanımladı.\n- **Kentucky Modeli (Deuschle):** Tıp eğitimini toplumun içine taşıyan ekip tabanlı toplum hekimliğidir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Öncü / Kurum", "Yıl", "Tarihsel İlke ve Katkı"],
                [
                    ["Alfred Grotjahn", "1912", "Sosyal patoloji; en önemli hastalık en çok öldüren, sakatlayan, sık görülendir"],
                    ["Rudolf Virchow", "1848", "Tıp bir sosyal bilimdir; politika geniş kapsamlı tıptır"],
                    ["Yunanistan Deneyimi", "1945+", "Kök nedenin hastane değil aile ve çevre ortamı olduğunun ispatı"],
                    ["DSÖ (WHO)", "1948", "Bedenen, ruhen ve sosyal yönden tam bir iyilik hali tanımı (7 Nisan)"],
                    ["Kentucky Üniversitesi", "1960'lar", "Toplum hekimliği ve sağlık ekibi eğitim modeli (K.W. Deuschle)"]
                ]
            ),
            make_chain(
                "Sosyal Hekimliğin Gelişim Aşamaları",
                [
                    "1. Virchow ve Silezya: Tifüsün reçetesinin demokrasi ve adalet olduğunun tespiti.",
                    "2. Grotjahn İlkeleri: Önemli hastalık ve risk gruplarına öncelik verilmesi kuralı.",
                    "3. DSÖ'nün Doğuşu: Sağlığın fiziksel, ruhsal ve sosyal tam iyilik olarak tanımlanması.",
                    "4. Kentucky Toplum Hekimliği: Hekimin toplum içine girip sağlık ekibi kurması."
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-18-s70",
        "title": "Bölüm Özeti: Dünya Deneyiminden Türkiye'nin Sağlık Reformuna Geçiş",
        "content": "Bölüm 7 boyunca sosyal hekimliğin, DSÖ'nün evrensel sağlık tanımının ve toplum hekimliği felsefesinin temellerini inceledik:\n\n- **Özet:** Sağlık insan hakkıdır, fırsat eşitliği esastır ve hekimlik toplumsal çevreyi düzeltmeden başarıya ulaşamaz.\n- **Sonraki Bölüm (Bölüm 8):** Bu evrensel ilkeleri Türkiye'ye taşıyan **Prof. Dr. Nusret Fişek'i, 224 Sayılı Sağlık Hizmetlerinin Sosyalleştirilmesi Kanunu'nu (1961), Sağlık Ocakları modelini ve Nüfus Planlaması devrimini** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "Grotjahn'ın sosyal hekimlik kuralına göre sağlık kaynaklarının planlanmasında bir hastalığın en önemli hastalık sayılmasının üç kriteri nelerdir?",
                "En çok öldüren, en sık görülen ve en çok sakat bırakan hastalık olması",
                "Grotjahn'ın önemli hastalık formülü"
            ),
            make_quiz(
                "Dünya Sağlık Örgütü Anayasası'nın yürürlüğe girdiği ve her yıl tüm dünyada 'Dünya Sağlık Günü' olarak kutlanan tarih hangisidir?",
                [
                    {"key": "A", "text": "7 Nisan", "isCorrect": True, "explanation": "Doğru cevap A'dır: DSÖ 7 Nisan 1948'de kurulmuş olup her yıl 7 Nisan Dünya Sağlık Günü olarak kutlanır."},
                    {"key": "B", "text": "14 Mart", "isCorrect": False, "explanation": "Türkiye'de Tıp Bayramı'dır."},
                    {"key": "C", "text": "1 Aralık", "isCorrect": False, "explanation": "Dünya AIDS Günü'dür."},
                    {"key": "D", "text": "24 Mart", "isCorrect": False, "explanation": "Dünya Tüberküloz Günü'dür."}
                ]
            )
        ]
    })

    return slides
