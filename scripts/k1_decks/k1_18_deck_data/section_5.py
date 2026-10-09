# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-18-s41",
        "title": "Su ile Bulaşan Salgın Hastalıklar: Kolera ve Tifo Tarihçesi",
        "content": "Temiz içme ve kullanma suyuna erişim, insan sağlığını ve beklenen yaşam süresini en çok artıran halk sağlığı unsurudur (Sınav Spotu):\n\n- **Tifo (Salmonella Typhi):**\n  - Yaklaşık 2500 yıldır bilinmektedir; antik çağlardan beri kirli kuyu ve nehir sularıyla ilişkisinden şüphelenilmiştir.\n  - Barsak perforasyonu ve yüksek ateşle seyreden tifo, kanalizasyon sularının içme suyuna karışmasıyla kitlesel salgınlar yapmıştır.\n- **Kolera (Vibrio cholerae):**\n  - Ganj deltasından çıkarak 19. yüzyılda buharlı gemiler ve ticaret yollarıyla 7 büyük küresel pandemi oluşturmuştur.\n  - 'Pirinç suyu' benzeri masif sulu ishal ve kusmayla hastayı saatler içinde ağır dehidratasyon ve hipovolemik şoktan öldürür.\n- **Kritik Halk Sağlığı Gerçeği:** Su şebekelerinin arıtılması ve klorlanması, modern tıptaki tüm antibiyotiklerin toplamından daha fazla insanın hayatını kurtarmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Kolera vs Tifo Salgınları",
                "Kolera (Akut Dehidratasyon)",
                "Saatler içinde litrelerce pirinç suyu ishal yapar; tedavi edilmezse aynı gün hipovolemik şoktan öldürür.",
                "Tifo (Subakut Sistemik Enfeksiyon)",
                "Kademeli artan merdiven ateşi, bradikardi, barsak ülserleri ve kanamaları ile haftalarca sürer."
            ),
            make_quiz(
                "İnsanlık tarihinde su kaynaklarının kirlenmesiyle kitlesel salgınlar yapan, saatler içinde masif sıvı kaybı ve hipovolemik şokla öldüren 19. yüzyılın en korkutucu salgını hangisidir?",
                [
                    {"key": "A", "text": "Kolera", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kolera pirinç suyu ishaliyle saatler içinde ölümcül sıvı kaybı yapan su kaynaklı pandemidir."},
                    {"key": "B", "text": "Çiçek hastalığı", "isCorrect": False, "explanation": "Solunum damlacıkları ve temasla bulaşır."},
                    {"key": "C", "text": "Kuduz", "isCorrect": False, "explanation": "Hayvan ısırığıyla bulaşır."},
                    {"key": "D", "text": "Skorbüt", "isCorrect": False, "explanation": "C vitamini eksikliği beslenme hastalığıdır."}
                ]
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-18-s42",
        "title": "Miazma Teorisi vs Germ Kuramı: Salgınlar Havadan mı Sudan mı?",
        "content": "19. yüzyılın ortalarında tıp dünyası iki büyük düşünce ekolü arasında şiddetli bir çatışma yaşıyordu (Sınav Spotu):\n\n- **Miazma Kuramı (Egemen Görüş):**\n  - Hastalıkların bataklıklardan, çürüyen çöplerden ve lağımlardan yükselen kötü kokulu, zehirli buharlardan (**miazma**) kaynaklandığına inanılıyordu.\n  - Bu inanç nedeniyle tıp otoriteleri salgın anında pencereleri kapatmayı, tütsüler yakmayı ve koku gidericiler kullanmayı öneriyordu; suyun rolü tamamen reddediliyordu.\n- **Su Yoluyla Bulaş Kuramı:**\n  - Hastalığın havadan değil, hastaların dışkısıyla kirlenen içme sularının yutulmasıyla sindirim kanalından giren görünmez bir zehir/etkenle yayıldığı görüşüydü.\n- **Tarihi Kırılma:** John Snow, bakterinin kendisi (Vibrio cholerae) mikroskopta izole edilmeden 30 yıl önce su yolunu matematiksel ve mekânsal olarak kanıtlayacaktır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Görüş / Kuram", "Savunulan Bulaş Mekanizması", "Önerilen Korunma Yöntemi"],
                [
                    ["Miazma Teorisi (Geleneksel)", "Kokuşmuş pis havayı solumak (zehirli gazlar)", "Pencereleri kapatmak, tütsü yakmak, havalandırma"],
                    ["Su / Germ Kuramı (John Snow)", "Dışkı bulaşmış içme suyunu ağızdan tüketmek", "Su kaynaklarını arıtmak, tulumba kollarını sökmek"]
                ]
            ),
            make_cloze(
                "19. yüzyıla kadar salgın hastalıkların çürüyen organik maddelerden çıkan pis kokulu zehirli gazlardan kaynaklandığını savunan inanışa miazma teorisi denirdi.",
                "miazma",
                "Kötü ve zehirli hava anlamına gelen antik salgın kuramı"
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-18-s43",
        "title": "John Snow ve 1854 Londra Broad Street Kolera Salgını",
        "content": "İngiliz hekim ve anestezi uzmanı John Snow (1813-1858), 1854 yılında Londra'nın Soho bölgesinde patlak veren kolera salgınında tarihin akışını değiştirdi (Sınav Spotu):\n\n- **Soho / Broad Street Salgını:**\n  - Ağustos 1854'te Broad Street civarında aniden yüzlerce insan koleraya yakalandı ve birkaç gün içinde 500'den fazla insan öldü.\n- **Nokta Haritası (Dot Map) Yöntemi:**\n  - John Snow sokak sokak, kapı kapı dolaşarak her kolera ölümünün gerçekleştiği evi bir Londra haritası üzerinde **noktalarla işaretledi**.\n  - Ölümlerin **Broad Street üzerindeki sokak su pompasının (tulumbasının)** etrafında yoğunlaştığını görsel olarak ortaya koydu.\n- **Uç Örneklerin İncelenmesi:**\n  - Tulumbaya çok yakın olan bir bira fabrikasındaki (brewery) işçilerden hiçbirinin kolera olmadığını gördü; çünkü işçiler su yerine bira içiyorlardı.\n  - Uzakta oturan ancak Broad Street'in suyunun tadını sevdiği için oradan su getirten bir kadının koleradan öldüğünü saptadı.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "John Snow'un Saha Araştırması Basamakları",
                [
                    "1. Vaka Tespiti: Soho mahallesindeki tüm kolera ölümleri tek tek listelenir.",
                    "2. Mekansal Haritalama: Londra haritası üzerine her ölüm bir çubuk veya nokta olarak çizilir.",
                    "3. Merkez Çekim Noktası: Ölümlerin Broad Street su pompası çevresinde kümelendiği belirlenir.",
                    "4. Negatif ve Pozitif Kontroller: Bira fabrikası çalışanları ile uzaktan su getirtenlerin analizi hipotezi doğrular."
                ]
            ),
            make_cloze(
                "John Snow'un 1854 Londra kolera salgınında ölümleri harita üzerinde işaretleyerek salgının kaynağı olduğunu kanıtladığı su tulumbası Broad Street caddesindedir.",
                "Broad Street",
                "Modern epidemiyolojinin doğduğu Londra caddesi ve su pompası"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-18-s44",
        "title": "Broad Street Tulumba Kolunun Sökülmesi: İlk Saha Epidemiyolojisi Müdahalesi",
        "content": "John Snow elde ettiği epidemiyolojik kanıtlarla yerel yetkilileri eyleme geçmeye ikna etmiştir (Sınav Spotu):\n\n- **Tarihi Müdahale (7 Eylül 1854):**\n  - Snow, St. James bölgesi idare meclisine giderek ölümlerin Broad Street pompasından kaynaklandığını haritasıyla sundu.\n  - Meclis ikna oldu ve pompanın **çalışma kolu (handle) yerinden söküldü**.\n  - İnsanların o tulumbadan su alması engellenir engellenmez bölgedeki yeni kolera vakaları bıçak gibi kesildi.\n- **Kirlenmenin Nedeni:**\n  - Daha sonra yapılan kazıda, pompanın hemen yanındaki bir fosseptik çukurunun tuğlalarının çatladığı ve koleralı bir bebeğin bezlerinin yıkandığı lağım suyunun içme suyu kuyusuna sızdığı ortaya çıktı.\n- **Halk Sağlığı Dersi:** Etken mikrop henüz laboratuvarda tanımlanmamış olsa bile, **epidemiyolojik gözlem ve bulaş yolunu kesme müdahalesiyle** bir salgın tamamen durdurulabilir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Müdahale Öncesi vs Tulumba Kolu Söküldükten Sonra",
                "Müdahale Öncesi (Salgın Zirvesi)",
                "Günde onlarca insan kusma ve ishalden ölüyor, mahalleli panik içinde kaçıyordu.",
                "Müdahale Sonrası (Kol Söküldü)",
                "Halkın kuyu suyunu içmesi engellendi; yeni vaka sayısı hızla sıfıra indi ve salgın sona erdi."
            ),
            make_quiz(
                "1854 Londra kolera salgınında John Snow'un yerel konseyi ikna ederek gerçekleştirdiği ve salgını anında durduran tarihi halk sağlığı müdahalesi nedir?",
                [
                    {"key": "A", "text": "Broad Street su pompasının kolunu söktürerek su alımını durdurmak", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tulumba kolunun sökülmesi saha epidemiyolojisinin ilk ve en ünlü müdahalesidir."},
                    {"key": "B", "text": "Tüm Soho mahallesini ateşe vermek", "isCorrect": False, "explanation": "Orta Çağ veba uygulamasıdır."},
                    {"key": "C", "text": "Hastalara antibiyotik dağıtmak", "isCorrect": False, "explanation": "O dönemde antibiyotik henüz keşfedilmemişti."},
                    {"key": "D", "text": "Tüm Londra halkına kolera aşısı yapmak", "isCorrect": False, "explanation": "Kolera aşısı henüz yoktu."}
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-18-s45",
        "title": "John Snow'un Mirası: 'Çevre Sağlığı ve Epidemiyolojinin Babası'",
        "content": "John Snow'un Broad Street araştırması ve Thames Nehri su şirketleri karşılaştırması modern epidemiyolojinin kurucu metodolojisidir (Sınav Spotu):\n\n- **Büyük Doğal Deney (Grand Experiment):**\n  - Londra'da iki rakip su şirketi vardı: Southwark and Vauxhall Şirketi (suyu kanalizasyonun karıştığı kirli Thames'ten alıyordu) ve Lambeth Şirketi (suyu nehrin yukarısındaki temiz alandan alıyordu).\n  - Snow, aynı sokakta oturan komşulardan kirli su şirketine abone olanlarda kolera ölüm oranının temiz su şirketine abone olanlara göre **katbekat yüksek olduğunu** gösterdi.\n- **Unvanları:**\n  - Robert Koch kolera vibrionunu 1883'te (Snow'un ölümünden 25 yıl sonra) izole etti.\n  - Bu nedenle John Snow, tıp literatüründe haklı olarak **'Modern Epidemiyolojinin ve Çevre Sağlığı Biliminin Başlatıcısı / Babası'** olarak kabul edilir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Su Şirketi", "Su Alma Noktası", "Kolera Ölüm Oranı"],
                [
                    ["Southwark and Vauxhall", "Kanalizasyon karışan kirli nehir bölgesi", "Aşırı yüksek ölüm oranı (10.000 evde ~315 ölüm)"],
                    ["Lambeth Şirketi", "Kanalizasyon öncesi temiz nehir membaı", "Düşük ölüm oranı (10.000 evde ~37 ölüm)"]
                ]
            ),
            make_cloze(
                "1854 Broad Street kolera salgını araştırmasıyla mikroorganizma henüz bulunmadan önce suyun önemini kanıtlayan John Snow çevre sağlığı biliminin başlatıcısı kabul edilir.",
                "çevre sağlığı",
                "John Snow'un kurucusu sayıldığı halk sağlığı alt disiplini"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-18-s46",
        "title": "Edwin Chadwick ve İngiltere'de Büyük Sanitasyon Raporu (1842)",
        "content": "İngiltere'de Sanayi Devrimi'nin getirdiği sefalet ve salgınlara karşı kamusal sağlık reformunu başlatan avukat ve bürokrat Edwin Chadwick'tir (Sınav Spotu):\n\n- **1842 Sanitasyon Raporu (The Sanitary Report):**\n  - 'Büyük Britanya Emekçi Nüfusun Sıhhi Koşulları Üzerine Rapor' adıyla yayınlandı.\n  - Yoksulluk ile hastalık arasındaki doğrudan nedensellik ilişkisini istatistiklerle ortaya koydu.\n  - İşçi sınıfının ortalama yaşam süresinin pis su, çöp yığınları ve kötü havalandırma nedeniyle 20 yaşın altında olduğunu belgeledi.\n- **Halk Sağlığı Yasası (Public Health Act - 1848):**\n  - Raporun etkisiyle dünyadaki ilk kapsamlı halk sağlığı yasası çıkarıldı.\n  - Merkezi Sağlık Kurulu kuruldu; kentlerde temiz içme suyu şebekeleri, kapalı kanalizasyon boruları ve çöp toplama sistemleri yasal zorunluluk haline getirildi.\n- **Sanitasyon Devrimi:** Bu altyapı adımları ölüm oranlarını dramatik biçimde düşürdü.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Chadwick Öncesi Vahşi Sanayi vs 1848 Sağlık Yasası",
                "Chadwick Öncesi (Açık Lağımlar)",
                "Sokaklarda çöp ve dışkı yığınları, işçilerin 18-20 yaşında tifodan ölmesi.",
                "1848 Yasası Sonrası (Sanitasyon Devrimi)",
                "Kapalı kanalizasyon boruları, temiz şehir şebeke suyu ve devlet denetimli halk sağlığı kurulları."
            ),
            make_quiz(
                "1842 yılında yayınladığı raporla İngiltere'de yoksulluk ve pisliğin salgınlara yol açtığını kanıtlayarak 1848'de ilk 'Halk Sağlığı Yasası'nın çıkmasını sağlayan reformcu kimdir?",
                [
                    {"key": "A", "text": "Edwin Chadwick", "isCorrect": True, "explanation": "Doğru cevap A'dır: Edwin Chadwick 1842 sanitasyon raporuyla modern çevre sağlığı ve altyapı yasalarını başlatmıştır."},
                    {"key": "B", "text": "John Snow", "isCorrect": False, "explanation": "Snow 1854'te Broad Street salgınını çözmüştür."},
                    {"key": "C", "text": "James Lind", "isCorrect": False, "explanation": "Skorbüt araştırmacısıdır."},
                    {"key": "D", "text": "Nusret Fişek", "isCorrect": False, "explanation": "Türkiye'de sosyalleştirmeyi kurmuştur."}
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-18-s47",
        "title": "Sıtma Tarihçesi: Bataklıklardan (Mal'aria) Anofel Sivrisineğine",
        "content": "Sıtma (Malaria), insanlık tarihini en derinden şekillendiren ve imparatorlukların yıkılışına neden olan paraziter bir hastalıktır (Sınav Spotu):\n\n- **İsmin Kökeni:**\n  - İtalyanca **'mal'aria' (kötü hava)** kelimesinden gelir; Roma döneminden beri bataklıklardan yükselen zehirli kokuların sıtmaya yol açtığına inanılmıştır.\n- **Columella (MS 100):**\n  - Romalı tarım yazarı Columella, bataklıkların zehirli gaz değil, 'gözle görülemeyen küçük hayvanlar' ürettiğini ve bunların insanı sokarak hastalığı bulaştırdığını ilk sezen yazardır.\n- **Tedavi Edilen İlk Bulaşıcı Hastalık:**\n  - Sıtma, etkeni (Plazmodium) ve bulaş yolu (sivrisinek) **henüz hiç bilinmezken tedavisi keşfedilen tarihteki ilk hastalıktır**!\n  - Güney Amerika'da yerli kabileler tarafından kullanılan **Kına-kına (Cinchona) ağacı kabuğu** 17. yüzyılda Avrupa'ya getirilmiş ve içindeki **kinin** alkaloidi sayesinde sıtma nöbetleri mucizevi biçimde tedavi edilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Sıtma Anlayışının Tarihsel Gelişimi",
                [
                    "1. Mal'aria (Kötü Hava): Bataklık kokularının hastalığa yol açtığı inancı.",
                    "2. Kına-Kına Ağacı (Kinin): Etkeni bilinmeden kinin ile tedavi edilen ilk enfeksiyon olması.",
                    "3. Laveran'ın Keşfi (1880): Alyuvarlarda Plazmodium parazitinin görülmesi.",
                    "4. Ross ve Anofel (1897): Vektörün sivrisinek olduğunun ispatı ve bataklık kurutma mücadelesi."
                ]
            ),
            make_cloze(
                "Sıtma hastalığının tedavisi için 17. yüzyılda Peru'dan Avrupa'ya getirilen ve etken bilinmeden tedavi sağlayan ağaç kabuğu kına-kına ağacıdır.",
                "kına-kına",
                "Kinin alkaloidinin elde edildiği Cinchona ağacı kabuğunun Türkçe adı"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-18-s48",
        "title": "Sıtmanın Çözümü: Laveran (1880) ve Ronald Ross (1897)",
        "content": "Sıtmanın biyolojik zincirinin çözülmesi parazitoloji ve tıbbi entomolojinin doğuşunu sağlamıştır (Sınav Spotu):\n\n- **Alphonse Laveran (1880 - Cezayir):**\n  - Fransız askeri cerrahı Laveran, sıtmalı bir askerin taze kanında alyuvarlar içinde kamçılanan ve hareket eden parazitleri gördü.\n  - Sıtmanın bir bakteri değil, tek hücreli bir protozoon (**Plasmodium**) olduğunu kanıtladı (1907 Nobel Tıp Ödülü).\n- **Ronald Ross (1897 - Hindistan):**\n  - İngiliz hekim Ronald Ross, sıtma parazitinin insandan insana **Anofel cinsi dişi sivrisineklerin** midesi ve tükürük bezleri aracılığıyla taşındığını kanıtladı (1902 Nobel Tıp Ödülü).\n- **Halk Sağlığı Stratejisi:**\n  - Vektörün anofel olduğunun anlaşılmasıyla sıtma mücadelesi bataklıkların kurutulması, durgun sulara gazyağı dökülmesi ve insektisit (DDT) uygulamalarına odaklanmış ve milyonlarca hayat kurtarılmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Bilim İnsanı", "Yıl", "Tarihi Keşif", "Ödül"],
                [
                    ["Alphonse Laveran", "1880", "Alyuvarlarda sıtma etkeni Plasmodium'un keşfi", "1907 Nobel Fizyoloji ve Tıp Ödülü"],
                    ["Ronald Ross", "1897", "Sıtmanın Anofel sivrisineği ile bulaştığının ispatı", "1902 Nobel Fizyoloji ve Tıp Ödülü"]
                ]
            ),
            make_quiz(
                "1880 yılında Cezayir'de sıtmalı hastaların alyuvarları içinde hareket eden Plasmodium parazitini mikroskopta ilk kez gözlemleyen Fransız hekim kimdir?",
                [
                    {"key": "A", "text": "Alphonse Laveran", "isCorrect": True, "explanation": "Doğru cevap A'dır: Laveran 1880'de sıtma etkeni Plasmodium'u keşfetmiş ve 1907'de Nobel almıştır."},
                    {"key": "B", "text": "Ronald Ross", "isCorrect": False, "explanation": "Ross sivrisinek vektörünü bulmuştur."},
                    {"key": "C", "text": "Robert Koch", "isCorrect": False, "explanation": "Tüberküloz basilini bulmuştur."},
                    {"key": "D", "text": "Louis Pasteur", "isCorrect": False, "explanation": "Kuduz aşısını bulmuştur."}
                ]
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-18-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] John Snow, Çevre Sağlığı ve Epidemiyoloji",
        "content": "Bu checkpointte su, çevre sağlığı, epidemiyoloji ve sıtmanın tarihçesini özetliyoruz:\n\n- **Kolera ve Tifo:** Su ile bulaşan en büyük iki ölümcül salgın hastalıktır. Su arıtımı ve klorlama devasa hayat kurtarmıştır.\n- **Miazma vs Su:** Miazma zehirli gaz inancıydı; John Snow salgının kirli içme suyundan kaynaklandığını kanıtladı.\n- **John Snow (1854):** Londra Broad Street salgınında ölümleri haritaladı; tulumba kolunu söktürerek salgını durdurdu; **çevre sağlığı ve modern epidemiyolojinin babasıdır**.\n- **Edwin Chadwick (1842):** Sanitasyon raporuyla yoksulluk-salgın ilişkisini gösterdi; 1848'de ilk Halk Sağlığı Yasası'nı çıkarttı.\n- **Sıtma:** Etkeni bilinmeden tedavi edilen ilk hastalıktır (Kına-kına ağacı kabuğu / kinin).\n- **Laveran (1880) & Ross (1897):** Laveran alyuvarda Plasmodium'u, Ross Anofel sivrisinek vektörünü bularak sıtma zincirini çözdü.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Öncü İsim", "Olay / Yıl", "Halk Sağlığı Mirası"],
                [
                    ["John Snow", "1854 (Broad Street)", "Çevre sağlığının başlatıcısı, haritalama, tulumba kolu müdahalesi"],
                    ["Edwin Chadwick", "1842-1848", "Sanitasyon raporu ve tarihin ilk Halk Sağlığı Yasası"],
                    ["Kına-kına Kabuğu", "17. Yüzyıl", "Etken bilinmeden kinin ile tedavi edilen ilk bulaşıcı hastalık"],
                    ["Alphonse Laveran", "1880", "Alyuvar içinde Plasmodium parazitinin keşfi"],
                    ["Ronald Ross", "1897", "Anofel cinsi dişi sivrisinek vektörünün ispatı"]
                ]
            ),
            make_chain(
                "Çevre Sağlığı ve Epidemiyolojinin Evrimi",
                [
                    "1. Chadwick Raporu: Şehirlerde kapalı kanalizasyon ve temiz su zorunluluğu.",
                    "2. John Snow Haritası: Broad Street tulumba kolunun sökülmesiyle ilk saha epidemiyolojisi.",
                    "3. Su Şirketleri Analizi: Doğal deneyle kirli su tüketenlerde ölüm fazlalığının tescili.",
                    "4. Sıtma ve Vektör Mücadelesi: Bataklıkların kurutulmasıyla çevresel kontrolün başarısı."
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-18-s50",
        "title": "Bölüm Özeti: Çevre Sağlığından Beslenme ve Meslek Hastalıklarına Geçiş",
        "content": "Bölüm 5 boyunca içme suyunun, sanitasyonun, John Snow'un metodolojisinin ve çevre sağlığının zaferini inceledik:\n\n- **Özet:** Kolera ve tifo suyun temizlenmesiyle durduruldu; miazma yerini bilimsel çevre sağlığına bıraktı.\n- **Sonraki Bölüm (Bölüm 6):** Denizcilerin korkulu rüyası olan **Skorbüt hastalığını (C vitamini eksikliği), Kommodor Anson'un trajik seferini, James Lind'in tarihteki ilk kontrollü klinik deneyini (limon ve portakal) ve Bernardino Ramazzini ile Meslek Hastalıklarının doğuşunu** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "1854 Londra Broad Street kolera salgınında ölümleri harita üzerinde işaretleyerek çevre sağlığı bilimini başlatan İngiliz hekim kimdir?",
                "John Snow",
                "Epidemiyolojinin ve çevre sağlığının babası kabul edilen anestezi uzmanı"
            ),
            make_quiz(
                "Etkeni ve bulaşma yolu henüz hiçbir mikroskopla bilinmiyorken Güney Amerika yerlilerinin kullandığı kına-kına ağacı kabuğuyla (kinin) tedavi edilen ilk enfeksiyon hastalığı hangisidir?",
                [
                    {"key": "A", "text": "Sıtma (Malaria)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sıtma etkeni ve sivrisinek bilinmeden kininle tedavi edilen ilk bulaşıcı hastalıktır."},
                    {"key": "B", "text": "Frengi (Sifilis)", "isCorrect": False, "explanation": "Penisilinle tedavi edilmiştir."},
                    {"key": "C", "text": "Çiçek", "isCorrect": False, "explanation": "Aşıyla önlenmiştir."},
                    {"key": "D", "text": "Tüberküloz", "isCorrect": False, "explanation": "Streptomisinle tedavi edilmiştir."}
                ]
            )
        ]
    })

    return slides
