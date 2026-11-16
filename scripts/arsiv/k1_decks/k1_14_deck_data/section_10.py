# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-14-s91",
        "title": "Uluslararası Sağlık Tüzüğü (UST / IHR 2005) ve Hukuki Çerçeve",
        "content": "Küreselleşen dünyada hiçbir ülke sınırlarını biyolojik patojenlere karşı tek başına kapatamaz; uluslararası hukuk kuralları şarttır:\n\n- **UST / IHR 2005 Tanımı (Sınav Spotu):** Dünya Sağlık Örgütü üyesi 196 ülkeyi yasal olarak bağlayan, uluslararası hastalık yayılımını önlemek, kontrol etmek ve kamu sağlığı yanıtı vermek için hazırlanmış **küresel bağlayıcı sağlık antlaşmasıdır**.\n- **Temel Felsefe:** Uluslararası trafiğe ve ticarete **gereksiz ve orantısız müdahalelerden kaçınırken**, halk sağlığı güvenliğini en üst düzeyde korumaktır.\n- **Ülkelerin Yükümlülükleri:**\n  - Olağan dışı halk sağlığı olaylarını 24 saat içinde DSÖ'ye bildirmek.\n  - Havalimanı, liman ve kara sınır kapılarında asgari sürveyans ve karantina altyapısını kurmak.\n  - Biyolojik, kimyasal ve nükleer tehditleri erken yakalayacak ulusal çekirdek kapasiteleri (core capacities) geliştirmek.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Eski Karantina Kanunları vs Uluslararası Sağlık Tüzüğü (IHR 2005)",
                "Eski Klasik Yaklaşım (Pasif Sınır Kapatma)",
                "Sadece belirli 3-4 hastalığı (kolera, veba, sarı humma) sayar; keyfi sınır kapatmalarla küresel ticareti felç ederdi.",
                "IHR 2005 (Dinamik ve Küresel Güvenlik)",
                "Patojenin adına bakmaksızın tüm biyolojik, kimyasal ve nükleer acil durumları kapsar; orantılı ve kanıta dayalı önlem şart koşar."
            ),
            make_cloze(
                "DSÖ üyesi ülkeleri yasal olarak bağlayan ve sınır aşan sağlık tehditlerini düzenleyen belge Uluslararası Sağlık Tüzüğüdür.",
                "Tüzüğüdür",
                "IHR 2005 belgesinin Türkçe adı"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-14-s92",
        "title": "Uluslararası Öneme Sahip Halk Sağlığı Acil Durumu (PHEIC)",
        "content": "DSÖ Genel Direktörü tarafından ilan edilen en üst düzey küresel alarm seviyesi **PHEIC** (Public Health Emergency of International Concern) olarak adlandırılır:\n\n- **PHEIC Tanımı (Sınav Spotu):** Hastalığın uluslararası yayılımı yoluyla diğer devletler için bir halk sağlığı riski oluşturduğu ve **koordine edilmiş küresel bir yanıt gerektiren olağanüstü olaydır**.\n- **Karar Algoritması (UST Ek 2):** Bir olayın PHEIC olup olmadığı 4 soruyla test edilir:\n  1. Halk sağlığı etkisi **ciddi** mi?\n  2. Durum **olağan dışı veya beklenmedik** mi?\n  3. **Uluslararası yayılma riski** belirgin mi?\n  4. Uluslararası **seyahat veya ticaret kısıtlaması riski** var mı?\n- **Tarihi PHEIC İlanları:** 2009 H1N1 Pandemisi, 2014 Çocuk Felci, 2014 Batı Afrika Ebola, 2016 Zika Virüsü, 2020 COVID-19 ve 2022-2024 Mpox (Maymun Çiçeği).",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["PHEIC Kriteri", "Açıklama", "Karar Etkisi"],
                [
                    ["1. Ciddi Etki", "Yüksek vaka ölüm hızı veya sağlık sistemini aşma", "En az 2 'Evet' varsa DSÖ'ye 24 saatte bildirim şarttır"],
                    ["2. Olağan Dışı / Beklenmedik", "Daha önce görülmemiş yeni mutant patojen", "Küresel alarm zillerini çalar"],
                    ["3. Uluslararası Yayılma Riski", "Havalimanları veya sınır aşan yoğun hareketlilik", "Diğer ülkelerin hazırlık moduna geçmesini gerektirir"],
                    ["4. Ticaret/Seyahat Kısıtlaması", "Sınırların kapatılması veya uçuş iptalleri riski", "Ekonomik ve diplomatik koordinasyon gerektirir"]
                ]
            ),
            make_quiz(
                "Dünya Sağlık Örgütü tarafından uluslararası yayılma riski taşıyan ve küresel koordineli yanıt gerektiren olağanüstü durumlar için kullanılan en üst düzey alarm kavramı hangisidir?",
                [
                    {"key": "A", "text": "PHEIC (Uluslararası Öneme Sahip Halk Sağlığı Acil Durumu)", "isCorrect": True, "explanation": "Doğru cevap A'dır: PHEIC, IHR 2005 kapsamında DSÖ'nün ilan ettiği en üst düzey resmi küresel acil durum statüsüdür."},
                    {"key": "B", "text": "Endemik stabil faz", "isCorrect": False, "explanation": "Endemik olağan ve yerleşik durumu ifade eder."},
                    {"key": "C", "text": "Klinik remisyon dönemi", "isCorrect": False, "explanation": "Remisyon hastanın iyileşme evresidir."},
                    {"key": "D", "text": "Rutin sağlık denetimi", "isCorrect": False, "explanation": "Acil durum statüsü değildir."}
                ]
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-14-s93",
        "title": "İzolasyon vs Karantina: Hukuki, Tıbbi ve Epidemiyolojik Ayrım",
        "content": "Tıp ve halk sağlığı terminolojisinde en sık birbirine karıştırılan iki kavram izolasyon ve karantinadır. Hekimler bu ayrımı kesin olarak bilmelidir:\n\n- **İzolasyon (Yalıtım - Sınav Spotu):**\n  - **Kime Uygulanır:** Bulaşıcı hastalığı **kanıtlanmış (testi pozitif) veya semptom gösteren HASTA kişilere** uygulanır.\n  - **Amaç:** Patojen saçan enfekte kişinin sağlıklı bireylerle temasını keserek bulaş zincirini durdurmaktır. Hastane odasında veya evde tek bir odada yapılır.\n- **Karantina (Sınav Spotu):**\n  - **Kime Uygulanır:** Bulaşıcı bir hastalık etkenine **maruz kalmış (temaslı), ancak henüz HASTALANMAMIŞ ve SEMPTOMSUZ (sağlıklı görünen) kişilere** uygulanır.\n  - **Amaç:** Kişi kuluçka (inkübasyon) süresinde olabilir; semptomlar çıktığında veya kuluçka süresi bitene kadar toplum içine çıkmasını kısıtlamaktır.\n  - **Süre:** Hastalığın bilinen **maksimum kuluçka süresi** kadardır (örneğin COVID-19 için 10-14 gün, Ebola için 21 gün).",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "İzolasyon (Hasta Kişi) vs Karantina (Sağlıklı Temaslı)",
                "İzolasyon (Hasta / Pozitif Birey)",
                "Hastalık tanısı almış veya semptomlu kişilerin bulaştırıcılık dönemi boyunca ayrılmasıdır.",
                "Karantina (Semptomsuz / Şüpheli Temaslı)",
                "Hastayla temas etmiş sağlıklı görünen kişilerin maksimum kuluçka süresince hareketinin sınırlandırılmasıdır."
            ),
            make_cloze(
                "Bulaşıcı hastalığa maruz kaldığından şüphelenilen ancak henüz semptom göstermeyen sağlıklı kişilere karantina uygulanır.",
                "karantina",
                "Semptomsuz temaslıların hareket kısıtlaması terimi"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-14-s94",
        "title": "Salgınlarda Biyoetik: Bireysel Özgürlükler vs Toplum Yararı (Siracusa İlkeleri)",
        "content": "Salgın yönetimi tıp ile insan haklarının en sert çarpıştığı biyoetik alanıdır:\n\n- **Etik İkilem:** Bir bireyin seyahat etme, çalışma veya toplanma özgürlüğü; toplumun hayatta kalma ve sağlıklı yaşama hakkıyla çatıştığında ne yapılmalıdır?\n- **Siracusa İlkeleri (BM İnsan Hakları Standardı - Sınav Spotu):** Salgın döneminde bireysel özgürlükleri kısıtlayan tedbirlerin hukuki ve etik olabilmesi için 5 şartı sağlaması zorunludur:\n  1. **Kanunilik:** Kısıtlama keyfi değil, açık bir kanuna dayanmalıdır.\n  2. **Meşru Amaç:** Amaç yalnızca halk sağlığını korumak olmalıdır; siyasi baskı aracı olamaz.\n  3. **Zorunluluk:** Başka hiçbir alternatifle hedefe ulaşılamıyor olmalıdır.\n  4. **Orantılılık:** Kısıtlama tehdidin büyüklüğüyle orantılı olmalı; en az kısıtlayıcı yol seçilmelidir.\n  5. **Ayrımcılık Yasağı:** Belirli bir ırk, din veya sosyal gruba karşı ayrımcı uygulanamaz.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Salgın dönemlerinde kamu otoritesinin bireysel özgürlükleri (karantina, seyahat yasağı) sınırlandırırken uymak zorunda olduğu uluslararası etik ve hukuki ilkeler hangisidir?",
                [
                    {"key": "A", "text": "Nürnberg Kodları", "isCorrect": False, "explanation": "Nürnberg kodları insan üzerindeki tıbbi deneylerle ilgilidir."},
                    {"key": "B", "text": "Siracusa İlkeleri (Kanunilik, meşru amaç, zorunluluk, orantılılık ve ayrımcılık yasağı)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Siracusa İlkeleri, kamu sağlığı acillerinde temel insan haklarının hangi şartlarda sınırlandırılabileceğini belirleyen evrensel biyoetik kılavuzdur."},
                    {"key": "C", "text": "Helsinki Bildirgesi", "isCorrect": False, "explanation": "Helsinki bildirgesi klinik araştırmaların etik kurallarını belirler."},
                    {"key": "D", "text": "Cenevre Sözleşmesi", "isCorrect": False, "explanation": "Cenevre sözleşmesi savaş hukuku ve esir haklarıyla ilgilidir."}
                ]
            ),
            make_recall(
                "Salgında karantina uygularken devlete düşen karşılıklı sorumluluk (reciprocity) ilkesi neyi gerektirir?",
                "Kişinin hareket özgürlüğü kısıtlanıyorsa; devlet o kişinin gıda, temiz su, ilaç, psikolojik destek ve gelir kaybını telafi etmekle etik olarak yükümlüdür."
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-14-s95",
        "title": "Geleceğin Tehdidi: 'Hastalık X' (Disease X) ve Bilinmeyene Hazırlık",
        "content": "DSÖ'nün öncelikli patojenler listesinde Ebola, Zika veya SARS'ın yanında çok özel ve gizemli bir başlık yer alır:\n\n- **Hastalık X Tanımı (Sınav Spotu):** İnsanlarda henüz bilinmeyen, şu anda hayvan rezervuarlarında sessizce bekleyen, ancak gelecekte ciddi bir küresel pandemiye yol açma potansiyeli taşıyan **varsayımsal/öngörülen bilinmeyen bir patojendir**.\n- **Felsefi ve Stratejik Amaç:** Salgın hazırlıklarının sadece bilinen virüslere (örneğin gribe) odaklanmasını engellemek; 'bilinmeyene karşı' esnek aşı platformları, hızlı genomik dizileme ve çok amaçlı yoğun bakım kapasiteleri inşa etmektir.\n- **COVID-19 Örneği:** SARS-CoV-2 ortaya çıktığında tıp dünyası için tam bir 'Hastalık X' örneğiydi; hazırlıklı olan ülkeler moleküler tanı ve mRNA teknolojileriyle hızla adapte olabildi.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Reaktif Yaklaşım vs 'Hastalık X' Proaktif Yaklaşımı",
                "Reaktif Yaklaşım (Geleneksel)",
                "Sadece geçmişte salgın yapmış virüslere karşı ilaç depolar; yeni bir virüs çıktığında aylar boyu çaresizce bekler.",
                "Hastalık X Proaktif Yaklaşımı (Modern Hazırlık)",
                "Patojen-bağımsız platformlar (mRNA, geniş spektrumlu antiviraller, yapay zeka sürveyansı) kurarak herhangi bir yeni virüse 100 günde yanıt üretir."
            ),
            make_cloze(
                "DSÖ'nün gelecekte bilinmeyen bir patojenin yol açabileceği varsayımsal küresel salgını temsil etmek için kullandığı kavrama Hastalık X denir.",
                "X",
                "Bilinmeyen gelecekteki patojeni simgeleyen harf"
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-14-s96",
        "title": "Erken Uyarı ve Küresel Yanıt Ağları (GOARN ve Entegre Sürveyans)",
        "content": "Hiçbir ülke küresel bir patojeni tek başına durduramaz; uluslararası bilimsel ve operasyonel dayanışma şarttır:\n\n- **GOARN (Global Outbreak Alert and Response Network - Sınav Spotu):** Dünya Sağlık Örgütü koordinasyonunda çalışan, 250'den fazla teknik kurum, üniversite ve laboratuvarı barındıran **Küresel Salgın Uyarı ve Yanıt Ağıdır**.\n  - Bir ülkede salgın patlak verdiğinde ve yerel kapasite aşıldığında; GOARN uzman epidemiyologları, saha laboratuvarlarını ve lojistiği 48 saat içinde o ülkeye sevk eder.\n- **Dijital ve Açık Kaynak Sürveyans (EIOS):** Yapay zeka ve internet tarama botları (ProMED, EIOS), dünyadaki tüm dillerdeki yerel haberleri, sosyal medya paylaşımlarını ve hastane yoğunluklarını tarayarak resmi bildirimden günler önce salgın ipuçlarını yakalar.\n- **Genomik Sürveyans:** Viral mutasyonların küresel veri tabanlarına (GISAID) eş zamanlı yüklenmesi varyantların anlık izlenmesini sağlar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Küresel Salgın İhbar ve Müdahale Döngüsü",
                [
                    "1. Erken Uyarı Tespiti: EIOS veya yerel hekim olağan dışı zatürre kümelenmesini sisteme girer.",
                    "2. UST / IHR Bildirimi: Ülke 24 saat içinde DSÖ Bölge Ofisi'ne resmi durumu raporlar.",
                    "3. PHEIC Değerlendirmesi: Acil Durum Komitesi toplanarak küresel halk sağlığı aciliyetini inceler.",
                    "4. GOARN Seferberliği: Uluslararası uzman ekipler ve seyyar laboratuvarlar sahaya indirilir.",
                    "5. Sınır Aşan Önlemler: Tüm havalimanlarında ve sınırlarda standart tarama protokolleri başlar."
                ]
            ),
            make_quiz(
                "Dünya Sağlık Örgütü çatısı altında teknik kurumları ve uzmanları bir araya getirerek salgın bölgelerine acil epidemiyolojik saha desteği sağlayan küresel ağ hangisidir?",
                [
                    {"key": "A", "text": "GOARN (Küresel Salgın Uyarı ve Yanıt Ağı)", "isCorrect": True, "explanation": "Doğru cevap A'dır: GOARN (Global Outbreak Alert and Response Network), salgın anında sahaya uzman ve laboratuvar sevk eden operasyonel ağdır."},
                    {"key": "B", "text": "NATO Savunma Konseyi", "isCorrect": False, "explanation": "Askeri bir ittifaktır."},
                    {"key": "C", "text": "Uluslararası Para Fonu (IMF)", "isCorrect": False, "explanation": "Finansal bir kuruluştur."},
                    {"key": "D", "text": "Küresel Patent Ofisi", "isCorrect": False, "explanation": "Fikri mülkiyet kurumudur."}
                ]
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-14-s97",
        "title": "Salgın Sonrası İnceleme: After-Action Review (AAR) ve Sistematik İyileşme",
        "content": "Salgın kontrol altına alındığında veya bittiğinde süreç tamamlanmış sayılmaz; en kritik öğrenme aşaması başlar:\n\n- **After-Action Review (AAR - Eylem Sonrası Değerlendirme):** Salgın yanıtına katılan tüm kurumların (sağlık, emniyet, yerel yönetim, sivil toplum) bir araya gelerek yanıtın güçlü ve zayıf yönlerini açık yüreklilikle analiz ettiği yapılandırılmış niteliksel bir incelemedir.\n- **Dört Temel AAR Sorusu (Sınav Spotu):**\n  1. Ne yapılması **planlanmıştı**?\n  2. Gerçekte ne **yaşandı**?\n  3. Planlanan ile gerçekleşen arasındaki **farklar neden kaynaklandı**?\n  4. Bir sonraki salgında aynı hataları yapmamak için **neyi değiştirmeliyiz**?\n- **Suçlama Değil Öğrenme:** AAR bir mahkeme veya günah keçisi arama süreci değildir; sistemik aksaklıkları tespit edip mevzuatı ve stokları güncelleme mekanizmasıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["AAR Analiz Alanı", "Salgında Yaşanan Sık Hata", "Alınan Yapısal Karar"],
                [
                    ["KKE Tedariği", "İlk iki haftada tulum ve N95 maske tükenmesi", "Stratejik 3 aylık ulusal KKE rezervi oluşturulması"],
                    ["Risk İletişimi", "Çelişkili açıklamalar yüzünden panik", "Tek sözcülü resmi basın merkezi kurulması"],
                    ["Laboratuvar Kapasitesi", "Test sonuçlarının 4 güne sarkması", "Ülke genelinde 81 ilde PCR altyapısının standardize edilmesi"]
                ]
            ),
            make_cloze(
                "Salgın yanıtı bittikten sonra güçlü ve zayıf yönleri sistemik olarak analiz etmek için yapılan değerlendirmeye eylem sonrası inceleme denir.",
                "sonrası",
                "After-Action Review teriminin Türkçe karşılığı"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-14-s98",
        "title": "Tıp Hekiminin Salgın Yönetimindeki Liderlik Rolü ve Mesleki Yemin",
        "content": "Geleceğin hekimleri olarak tıp öğrencileri, salgın anında sadece reçete yazan bir teknisyen değil, toplumun en güvenilir lideridir:\n\n- **Klinisyenin Eşsiz Gücü (Sınav Spotu):** Bir salgını laboratuvarlar veya algoritmalar değil; olağan dışı bir semptomu fark eden **uyanık ve şüpheci bir ilk basamak hekimi** başlatır veya durdurur.\n- **Liderlik ve Sakinlik:** Toplum panik içindeyken hekimin sergileyeceği rasyonel, bilimsel ve şefkatli duruş kitlesel histeriyi engeller.\n- **Etik Sadakat:** Hastanın kimliğine, inancına veya sosyal statüsüne bakılmaksızın eşit bakım vermek, hekimlik andının salgınlardaki en asil sınavıdır.\n- **Mesleki Dayanışma:** Hekimler, hemşirelerden temizlik personeline kadar tüm sağlık çalışanlarıyla tek bir zincirin halkaları gibi kenetlenmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Sadece Bireysel Reçete Yazan Hekim vs Toplum Sağlığı Lideri Hekim",
                "Bireysel Reçeteci Yaklaşım",
                "Hastayı muayene edip ilacını verir; vakanın nereden geldiğini, temaslılarını ve salgın potansiyelini sorgulamaz.",
                "Toplum Sağlığı Lideri Yaklaşım",
                "Vakanın epidemiyolojik bağlantısını görür, filyasyonu başlatır, toplumu bilgilendirir ve salgını büyümeden söndürür."
            ),
            make_recall(
                "Bir tıp hekiminin salgın yönetimindeki en büyük halk sağlığı sorumluluğu nedir?",
                "Klinik tanı koyduğu anda olayın epidemiyolojik boyutunu düşünmek, sürveyans bildirimini gecikmeksizin yapmak ve topluma kanıta dayalı doğru bilgiyle rehberlik etmektir."
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-14-s99",
        "title": "Çok Sektörlü Salgın Simülasyonu: Küresel Patojen Krizinde Stratejik Karar Akışı",
        "content": "Uluslararası bir liman kentinde acil servis hekimi olarak nöbettesiniz. Bir yük gemisinden indirilen 3 denizcide yüksek ateş, hemoptizi ve solunum yetmezliği saptanıyor:\n\n- **1. Adım (Klinik Şüphe):** Hastalar derhal negatif basınçlı izolasyona alınıyor; KKE ile müdahale ediliyor ve İl Sağlık Müdürlüğü ASOM'a acil sürveyans bildirimi yapılıyor.\n- **2. Adım (Filyasyon ve Sınır Kontrolü):** Gemideki diğer 25 mürettebat kabinlerinde **karantinaya** alınıyor (maksimum kuluçka süresince temaslı takibi).\n- **3. Adım (Laboratuvar ve Küresel İletişim):** Numuneler referans laboratuvara gönderiliyor; patojenin yeni bir mutant solunum virüsü olduğu saptanıyor. Durum 24 saat içinde UST/IHR kapsamında DSÖ'ye bildiriliyor.\n- **4. Adım (Risk İletişimi):** Sosyal medyada 'limandan şehre veba yayıldı' yalanları çıkmadan önce Sağlık Bakanlığı basın toplantısıyla doğru bilgiyi paylaşıyor; dedikoduların önü kesiliyor.\n- **Sonuç:** Çok sektörlü koordinasyon ve erken müdahale ile yerel yayılım başlamadan salgın sınırlanıyor.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Stratejik Kriz Yönetimi: Liman Kenti Salgın Simülasyonu",
                "Liman işletmesi geminin kargosunun milyonlarca dolar değerinde olduğunu, geminin hemen boşaltılması gerektiğini belirterek karantinayı kırmak istiyor. Hekim ve liman sağlık denetçisi olarak tavrınız ne olmalıdır?",
                [
                    {
                        "text": "Ticaretin aksamaması için mürettebatın maske takarak kargoyu boşaltmasına izin vermek",
                        "outcome": "Ölümcül hata: Mürettebat liman işçilerini enfekte eder ve şehirde kitlesel solunum salgını patlar.",
                        "isCorrect": False
                    },
                    {
                        "text": "UST / IHR 2005 ve ulusal mevzuat yetkisini kullanarak gemiyi izole etmek, kargo operasyonunu temas olmaksızın uzaktan robotik/güvenli protokollerle planlamak ve mürettebatın karantinasını tavizsiz sürdürmek",
                        "outcome": "Mükemmel halk sağlığı kararı: Hem biyolojik güvenlik sağlanır, hem orantılılık ilkesiyle kriz yönetilir.",
                        "isCorrect": True
                    },
                    {
                        "text": "Korkup nöbeti terk etmek ve basına gizli belgeleri sızdırmak",
                        "outcome": "Mesleki ve hukuki suç.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu simülasyonda denizcilerin hasta olanlarının hastaneye yatırılması ile semptomsuz olanlarının gemide tutulması arasındaki temel kavramsal fark nedir?",
                [
                    {"key": "A", "text": "Hasta olanlara izolasyon, semptomsuz temaslılara karantina uygulanmıştır", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hasta/pozitif kişilere izolasyon; semptomsuz ancak temaslı kişilere kuluçka süresince karantina uygulanır."},
                    {"key": "B", "text": "Her ikisi de sadece kitlesel aşılamadır", "isCorrect": False, "explanation": "Aşılama değil hareket kısıtlamasıdır."},
                    {"key": "C", "text": "Hasta olanlara karantina, temaslılara izolasyon denir", "isCorrect": False, "explanation": "Kavramlar ters verilmiştir."},
                    {"key": "D", "text": "Bu uygulamaların halk sağlığında hiçbir farkı yoktur", "isCorrect": False, "explanation": "Tıbbi ve hukuki olarak tamamen farklıdır."}
                ]
            )
        ]
    })

    # Slide 100 - CHECKPOINT 10 / BÜTÜNCÜL ÖZET
    slides.append({
        "id": "k1-14-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri Bütüncül Özeti",
        "content": "Bu son checkpointte Ders 14'ün tüm temel halk sağlığı ve epidemiyoloji ilkelerini birleştiriyoruz:\n\n- **1. Salgın Tehditleri:** 1970'ten beri 1500+ yeni patojen; ortaya çıkanların %70'i zoonotik (Tek Sağlık).\n- **2. Hazırlık ve Tanı:** İyi sürveyans, sağlıklı çevre, bilimsel yatırım; tanı ilk klinisyenle başlar!\n- **3. Epidemik Fazlar:** Giriş -> Lokal yayılım -> Amplifikasyon -> Azalma. Sınırlama ilk vakada başlar.\n- **4. Eliminasyon vs Eradikasyon:** Eliminasyon bölgesel sıfırlanmadır (aşı sürer); eradikasyon küresel kalıcı yok oluştur (yalnızca Çiçek).\n- **5. Yanıtın 4 Bileşeni:** Kurumlar arası koordinasyon (ASOM), sağlık enformasyonu (sürveyans: kişi-zaman-yer, müdahale: süreç/çıktı), risk iletişimi, sağlık müdahaleleri.\n- **6. Toplum ve İletişim:** Buyurgan dil bitti, önce güven; infodemiye karşı konuş, dinle, dedikoduyu engelle.\n- **7. Sağlık İşgücü ve Klinik Bakım:** Sağlık işgücünü korumak esastır; destekleyici bakımla Ebola'da ölüm %75'ten %33'e indi!\n- **8. Bulaş Yolları:** Vektör (Chikungunya, sarı humma, sıtma), Kene (KKKA), Fekal-oral (Kolera, polio), Solunum (Kızamık), Kemirgen (Veba), Güvenli ve Onurlu Defin.\n- **9. Aşı ve Matematik:** $H = 1 - 1/R_0$; halka aşılama çiçeği bitirdi; soğuk zincir (+2°C/+8°C).\n- **10. Hukuk ve Etik:** IHR 2005, PHEIC alarmı, İzolasyon (hasta) vs Karantina (temaslı), Hastalık X hazırlığı.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Ders Bölümü", "Anahtar Kavram ve Eşik", "Hayati Halk Sağlığı Kuralı"],
                [
                    ["Fazlar ve Sınırlama", "Erken tanı / İlk vaka", "Sınırlama ilk vaka tespit edildiği anda başlar"],
                    ["Eliminasyon / Eradikasyon", "Bölgesel vs Küresel yok oluş", "Eradikasyon yalnız Çiçek hastalığında başarılmıştır"],
                    ["Salgın Yanıtı (ASOM)", "4 Temel Bileşen", "Koordinasyon, enformasyon, risk iletişimi, müdahaleler"],
                    ["Destekleyici Bakım", "Ebola 2014 (%75 -> %33)", "Spesifik ilaç olmasa dahi kaliteli bakım hayat kurtarır"],
                    ["Aşı Matematiği", "H = 1 - 1/R0, Halka Aşılama", "Kızamık için ≥%95 bağışıklık şarttır; soğuk zincir +2°C/+8°C"],
                    ["Hukuk ve Terminoloji", "İzolasyon vs Karantina", "İzolasyon hastaya, karantina kuluçka süresince temaslıya"]
                ]
            ),
            make_chain(
                "Salgın Kontrol ve Korunmanın 5 Büyük İlkesi",
                [
                    "1. Tek Sağlık ve Klinisyen Uyanıklığı: Hayvan-insan dengesini gözet, ilk vaka şüphesinde erken tanı alarmını çal.",
                    "2. Anında Sınırlama ve ASOM: İlk vakayla birlikte filyasyonu başlat, kurumlar arası koordinasyonu tek çatı altında topla.",
                    "3. Çift Enformasyon ve Güven: Sürveyans ile süreç göstergelerini izle, halkı dinleyerek infodemiyi engelle.",
                    "4. Sağlıkçı Koruması ve WASH: KKE ile personeli koru, agresif destek bakım ve su-vektör mücadelesi ver.",
                    "5. Aşı Kalkanı ve Küresel Hukuk: Halka aşılama ve soğuk zincirle sürü bağışıklığı kur, UST/IHR ile dünyaya entegre ol."
                ]
            )
        ]
    })

    return slides
