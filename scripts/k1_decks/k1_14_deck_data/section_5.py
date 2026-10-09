# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-14-s41",
        "title": "Kapsamlı Salgın Yanıtının Dört Temel Bileşeni",
        "content": "Salgınlar, tek bir hekimin, tek bir hastanenin veya tek bir sağlık biriminin kendi başına yönetebileceği standart klinik durumlar değildir. Çok paydaşlı, karmaşık ve olağanüstü olaylardır:\n\n- **Sistemik Karmaşıklık:** Salgın ortaya çıktığında rutin sağlık hizmetleri hızla yetersiz kalır; fazladan bütçe, insan gücü, lojistik ve sektörler arası iş birliği gerekir.\n- **DSÖ ve Halk Sağlığına Göre 4 Temel Özellik (Sınav Spotu):**\n  1. **Kurumlar Arası Koordinasyon:** Tüm aktörlerin tek elden, senkronize ve tek komuta merkeziyle çalışması.\n  2. **Tam ve Eksiksiz Sağlık Enformasyonu:** Hem sürveyans (kişi-zaman-yer) hem de müdahale süreç verilerinin toplanması.\n  3. **Risk İletişimi (Riski Doğru ve Tam Aktarma):** Toplumla güven temelli çift yönlü iletişim ve infodemiyle mücadele.\n  4. **Tam ve Eksiksiz Sağlık Müdahaleleri:** Tanı, tedavi, filyasyon, aşı, KKE ve defin süreçlerinin eksiksiz yürütülmesi.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Bileşen", "Temel Görev ve Kapsam", "Başarısızlık Riski"],
                [
                    ["1. Koordinasyon", "Acil Operasyon Merkezi (ASOM), ortak eylem planı, tek komuta", "Yetki karmaşası, kaynak israfı, çatışan kararlar"],
                    ["2. Sağlık Enformasyonu", "Sürveyans (kişi-zaman-yer) + Müdahale göstergeleri (süreç/çıktı)", "Kör uçuş; salgının nerede yayıldığını bilememe"],
                    ["3. Risk İletişimi", "Şeffaf bilgilendirme, dinleme, dedikodu engelleme, infodemi yönetimi", "Panik, aşı reddi, toplumsal direniş ve güvensizlik"],
                    ["4. Sağlık Müdahaleleri", "Klinik bakım, filyasyon, temaslı takibi, aşı, IPC, defin", "Sağlık sisteminin çökmesi, kontrolsüz ölüm artışı"]
                ]
            ),
            make_cloze(
                "Kapsamlı bir salgın yanıtında koordinasyon, sağlık enformasyonu, risk iletişimi ve sağlık müdahaleleri olmak üzere dört temel bileşen bulunur.",
                "dört",
                "Temel salgın yanıt bileşeni adedi"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-14-s42",
        "title": "Bileşen 1: Kurumlar Arası Koordinasyon ve Liderlik",
        "content": "Salgın yanıtının ilk ve en kritik omurgası **kurumlar arası güçlü koordinasyondur**:\n\n- **İstisnai Bir Olay Olarak Salgın:** Salgın anında rutin bürokratik mekanizmalar çok yavaş kalır. Fazladan finansman, binlerce ek personel, güvenlik güçleri, yerel yönetimler (belediyeler), ulaştırma, gıda tedariki ve uluslararası kuruluşlar aynı anda sürece dahil olur.\n- **Tek Komuta ve Yetki:** Kararların tek bir merkezden, çelişki üretmeden ve hızla alınabilmesi için çok sektörlü liderlik yapısı kurulmalıdır.\n- **Sektörler Arası Entegrasyon:** Sağlık Bakanlığı, İçişleri, Milli Eğitim, Tarım ve Orman Bakanlığı ile sivil toplum kuruluşları arasında kesintisiz bilgi ve kaynak paylaşımı sağlanmalıdır.\n- **Temel Tehlike:** Koordinasyonun olmadığı durumlarda farklı kurumlar birbiriyle çelişen kararlar alır (örneğin biri okulları kapatırken diğeri kitlesel sınav düzenler) ve halkın güveni sarsılır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Salgın yanıtında 'kurumlar arası koordinasyonun' en temel varlık nedeni aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Yalnızca sağlık personeline fazladan maaş ödemesi yapılmasını sağlamak", "isCorrect": False, "explanation": "Koordinasyon idari maaş ödemesi için değil, devasa çok sektörlü salgın yanıtının tek elden yönetilmesi içindir."},
                    {"key": "B", "text": "Salgının fazladan insan, finansal kaynak ve çok sektörlü ortaklık gerektiren istisnai bir olay olması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Salgın olağanüstü bir durumdur; tek bir kurumun bütçesi ve personeli yetmez, bu yüzden çok sektörlü koordinasyon şarttır."},
                    {"key": "C", "text": "Hastalığın patogenezindeki hücresel mutasyonları laboratuvarda tek başına engellemek", "isCorrect": False, "explanation": "Mutasyonları engellemek laboratuvar ve virolojik süreçtir, idari koordinasyonun doğrudan amacı değildir."},
                    {"key": "D", "text": "Hastanelerin tüm rutin ameliyatlarını süresiz olarak durdurmak", "isCorrect": False, "explanation": "Rutin sağlık hizmetlerinin tamamen kapatılması değil, akılcı triyaj ve kaynak yönetimi hedeflenir."}
                ]
            ),
            make_recall(
                "Salgın yönetiminde kurumlar arası koordinasyon sağlanamazsa ne tür krizler ortaya çıkar?",
                "Yetki karmaşası, çelişkili kamuoyu açıklamaları, kaynakların mükerrer veya yanlış kullanımı, lojistik tıkanıklıklar ve toplumda derin güven kaybı oluşur."
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-14-s43",
        "title": "Acil Operasyon Merkezi (ASOM / EOC) ve Fiziksel Altyapı",
        "content": "Kurumlar arası koordinasyonun somutlaştığı kalbi **Acil Sağlık Operasyon Merkezi (ASOM / Public Health Emergency Operations Centre - PHEOC)** adı verilen özel fiziksel ve teknolojik merkezdir:\n\n- **Özel Fiziksel Alan (Sınav Spotu):** Tüm paydaş liderlerinin, epidemiyologların, lojistikçilerin ve iletişim uzmanlarının 7/24 kesintisiz birlikte çalışabileceği, güvenli ve donanımlı fiziksel bir merkez gereklidir.\n- **Teknolojik Altyapı:** Kesintisiz enerji kaynakları (jeneratör), uydu interneti, haritalama ekranları (CBS/GIS), güvenli telsiz ve veri sunucuları.\n- **Operasyonel Dokümantasyon Araçları:**\n  - Güncel **irtibat listeleri** (tüm kilit paydaşların doğrudan iletişim kanalları).\n  - **Toplantı izleme ve görev dağıtım sistemi** (her sabah yapılan brifing kararlarının takibi).\n- **Önemi:** ASOM, sahadan gelen ham verilerin hızla stratejik kararlara ve sahadaki eylemlere dönüştürüldüğü komuta güvertesidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Klasik Bürokratik Yönetim vs Acil Operasyon Merkezi (ASOM)",
                "Klasik Bürokrasi (Rutin Dönem)",
                "Resmi yazışmalar günlerce sürer, hiyerarşik onaylar beklenir, departmanlar birbirinin verisini gerçek zamanlı göremez.",
                "ASOM / PHEOC (Salgın Modu)",
                "Tüm paydaşlar aynı masada veya canlı dashboard başında toplanır; anlık veriyle saatler içinde karar alıp uygular."
            ),
            make_cloze(
                "Salgın koordinasyonunun etkin yürütülebilmesi için paydaşların toplandığı özel fiziksel alana acil operasyon merkezi denir.",
                "operasyon",
                "EOC/ASOM yapısındaki kilit kelime"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-14-s44",
        "title": "Ortak Eylem Planı, Görev Dağılımı ve Paydaş İletişimi",
        "content": "Acil operasyon merkezinin elindeki en kritik kılavuz **Ortak Eylem Planı (Incident Action Plan)** ve paydaş iletişim araçlarıdır:\n\n- **Düzenli Güncellenen Ortak Eylem Planı (Sınav Spotu):** Hangi müdahalenin ne zaman, hangi kaynakla yapılacağını ve her paydaşın rol ve sorumluluklarını açıkça tanımlayan yaşayan bir belgedir. Salgının gidişatına göre dinamik olarak revize edilir.\n- **Rol ve Sorumluluk Matrisi:** Kim filyasyon yapacak, kim güvenliği sağlayacak, kim laboratuvar kitini dağıtacak, kim basına konuşacak açıkça belirlenir.\n- **Paydaşlar Arası İletişim Araçları:**\n  - Acil telefon ve telsiz ağları.\n  - **Gösterge Tabloları (Dashboard):** Yatak doluluk oranları, KKE stokları, günlük vaka sayıları canlı izlenir.\n  - **Coğrafi Haritalar (GIS):** Kümelenmelerin (cluster) mekansal dağılımı haritalandırılır.\n  - **Hizmet ve Kaynak Dizinleri:** Hangi hastanede kaç solunum cihazı veya izolasyon odası olduğunu gösteren veri tabanları.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Salgın Eylem Planı ve Komuta Döngüsü",
                [
                    "1. Veri Toplama: Sahadaki filyasyon ekipleri ve hastanelerden anlık vaka ve kapasite verileri ASOM'a akar.",
                    "2. Analiz ve Haritalama: Epidemiyoloji uzmanları cluster haritalarını ve bulaş katsayısını günceller.",
                    "3. Eylem Planı Revizyonu: Darboğazlar (ör. reaktif eksikliği) belirlenir ve ortak eylem planı güncellenir.",
                    "4. Görev Dağılımı: İlgili paydaşlara (belediye, lojistik, laboratuvar) net yazılı direktifler iletilir.",
                    "5. Saha Denetimi: Kararların sahada uygulanma oranı süreç göstergeleriyle takip edilir."
                ]
            ),
            make_quiz(
                "Salgın koordinasyonunda kullanılan 'Ortak Eylem Planı' ile ilgili hangisi doğrudur?",
                [
                    {"key": "A", "text": "Salgın başında bir kez yazılır ve salgın bitene kadar asla değiştirilemez", "isCorrect": False, "explanation": "Ortak eylem planı sabit değil; salgının evrelerine ve dinamiklerine göre düzenli güncellenen canlı bir belgedir."},
                    {"key": "B", "text": "Müdahaleleri, paydaş rol ve sorumluluklarını tanımlayan ve düzenli güncellenen belgedir", "isCorrect": True, "explanation": "Doğru cevap B'dir: Ortak eylem planı her kurumun ne yapacağını belirleyen ve düzenli revize edilen temel operasyonel dokümandır."},
                    {"key": "C", "text": "Yalnızca hastane başhekimlerinin okumasına izin verilen gizli bir bütçe cetvelidir", "isCorrect": False, "explanation": "Tüm sektör ve paydaşların rollerini ve sorumluluklarını koordine eden operasyonel bir eylem rehberidir."},
                    {"key": "D", "text": "Sadece salgın tamamen bittikten sonra geçmişi değerlendirmek için yazılan rapordur", "isCorrect": False, "explanation": "Geçmişi değerlendirme raporu değil, kriz anında uygulanan aktif yol haritasıdır."}
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-14-s45",
        "title": "Bileşen 2: Sağlık Enformasyonu ve İki Temel Bilgi Türü",
        "content": "Doğru karar alabilmek, müdahale etkisini ölçmek ve kaynakları hedefe yönlendirebilmek için sağlam enformasyon şarttır. Enformasyon yoksa salgın yönetimi karanlıkta araç kullanmaya benzer:\n\n- **Sağlık Enformasyonunun Amacı:** Epidemiyolojik eğilimleri izlemek, yüksek riskli grupları belirlemek, sağlık sisteminin kapasite sınırlarını kestirmek ve kararların kanıta dayalı olmasını sağlamaktır.\n- **Salgında Gereken İki Temel Bilgi Türü (Sınav Sorusu):**\n  1. **Sürveyans Bilgisi:** Hastalığın yayılımını gösteren doğrudan epidemiyolojik veriler (Kişi, Zaman ve Yere göre vaka ve ölüm sayıları).\n  2. **Müdahale Bilgisi:** Sahada yürütülen eylemlerin kapsamı, verimliliği ve etkisini ölçen göstergeler (Süreç ve Çıktı göstergeleri).\n- **Bütünleşik Yaklaşım:** Sadece vaka sayısını bilmek yetmez; kaç temaslıya ulaşıldığını, kaç test yapıldığını ve kaç yatağın boş olduğunu da bilmek zorunludur.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Salgın Karar Vericisi: İki Bilgi Türünün Dengesi",
                "Bir ilde günlük vaka sayıları 100'den 500'e fırladı. Önünüzde iki rapor var: Biri sadece vaka sayıları (sürveyans), diğeri temaslı tarama ve laboratuvar hızı (müdahale bilgisi). Hangi yaklaşımı benimsersiniz?",
                [
                    {
                        "text": "Sadece vaka sayısına bakıp hemen sokağa çıkma yasağı ilan etmek",
                        "outcome": "Hatalı yaklaşım: Laboratuvar ve filyasyon kapasitesini bilmeden alınan panik kararları ekonomik ve sosyal yıkıma yol açar.",
                        "isCorrect": False
                    },
                    {
                        "text": "Sürveyans bilgisiyle (yer-zaman-kişi) müdahale bilgisini (test gecikmesi, filyasyon oranı) birleştirerek darboğazı çözmek",
                        "outcome": "Mükemmel halk sağlığı kararı: Bilgiler birleştirildiğinde artışın tek bir fabrikadaki kümelenmeden kaynaklandığı ve filyasyonun orada yoğunlaştırılması gerektiği görülür.",
                        "isCorrect": True
                    },
                    {
                        "text": "Verileri gizleyerek halkın panik yapmasını engellemeye çalışmak",
                        "outcome": "Felaket senaryosu: Veri gizleme infodemiyi patlatır ve salgın kontrol edilemez hale gelir.",
                        "isCorrect": False
                    }
                ]
            ),
            make_cloze(
                "Salgın yönetiminde gereken iki temel bilgi türü sürveyans bilgisi ile müdahale bilgisidir.",
                "müdahale",
                "Yapılan eylemlerin kapsam ve etkisini ölçen bilgi türü"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-14-s46",
        "title": "Sürveyans Bilgisi: Kişi, Zaman ve Yer Analitiği",
        "content": "Epidemiyolojinin kutsal sacayağı **Kişi, Zaman ve Yer (Person, Time, Place)** analizi, sürveyans bilgisinin özünü oluşturur:\n\n- **1. Kişi (Person) Değişkenleri:**\n  - Yaş, cinsiyet, meslek, gebelik durumu, altta yatan kronik hastalıklar (diyabet, immün yetmezlik).\n  - Hangi yaş grubunun daha duyarlı olduğunu veya kimlerin asemptomatik taşıyıcı olduğunu ortaya koyar.\n- **2. Zaman (Time) Değişkenleri:**\n  - Semptom başlangıç tarihi, tanı tarihi, hastaneye yatış ve taburculuk/ölüm tarihleri.\n  - Bu verilerle **Epidemik Eğri (Epi curve)** çizilir; salgının tek kaynaklı mı (point source) yoksa insandan insana yayılan (propagated) mı olduğu anlaşılır.\n- **3. Yer (Place) Değişkenleri:**\n  - İkametgah adresi, çalışma yeri, okul, seyahat geçmişi, hastane koğuşu.\n  - Mekansal kümelenmeleri ve bulaş odaklarını saptayarak coğrafi sınırlama sağlar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Epidemiyolojik Boyut", "İncelenen Temel Parametreler", "Sağladığı Kritik Karar"],
                [
                    ["Kişi (Person)", "Yaş, cinsiyet, meslek, aşı durumu, ek hastalıklar", "Öncelikli aşılanacak ve korunacak risk grubunu belirleme"],
                    ["Zaman (Time)", "Hastalık başlangıç günleri, kuluçka süresi eğrisi", "Salgının fazını, yayılma hızını ve tedbirlerin etkisini izleme"],
                    ["Yer (Place)", "İlçe, mahalle, iş yeri, okul, coğrafi koordinatlar", "Filyasyonu odaklama, lokal karantina veya sanitasyon uygulama"]
                ]
            ),
            make_quiz(
                "Epidemiyolojide sürveyans verilerinin sınıflandırıldığı üç temel parametre hangi seçenekte eksiksiz verilmiştir?",
                [
                    {"key": "A", "text": "Hekim, hemşire ve hastane binası", "isCorrect": False, "explanation": "Bunlar sağlık sistemi kaynaklarıdır, epidemiyolojik sürveyans değişkenleri değildir."},
                    {"key": "B", "text": "Kişi, zaman ve yer", "isCorrect": True, "explanation": "Doğru cevap B'dir: Sürveyans verisi daima kişi (kim), zaman (ne zaman) ve yer (nerede) ekseninde analiz edilir."},
                    {"key": "C", "text": "Maliyet, fatura ve sigorta kapsamı", "isCorrect": False, "explanation": "Bunlar sağlık ekonomisi terimleridir."},
                    {"key": "D", "text": "Genotip, sekans ve primer tasarımı", "isCorrect": False, "explanation": "Bunlar moleküler biyoloji analizleridir."}
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-14-s47",
        "title": "Müdahale Bilgisi: Süreç ve Çıktı Göstergeleri",
        "content": "Salgında yalnızca kaç kişinin hastalandığını saymak eylemleri yönetmeye yetmez; yapılan müdahalelerin sahada işleyip işlemediğini ölçen **Müdahale Bilgisine** ihtiyaç vardır:\n\n- **Süreç Göstergeleri (Process Indicators):** Müdahale adımlarının hedeflenen hız ve kalitede yapılıp yapılmadığını ölçer:\n  - Şüpheli vakanın bildirilmesi ile numunenin laboratuvara ulaşması arasındaki süre (ör. < 24 saat).\n  - Test sonucunun çıkma süresi (turnaround time).\n  - Temaslıların kaç saat içinde tespit edilip izolasyona alındığı (filyasyon süresi).\n  - Sağlık çalışanlarının KKE temin oranı ve el hijyeni uyumu.\n- **Çıktı ve Etki Göstergeleri (Outcome Indicators):**\n  - Hedef nüfusta aşılama kapsayıcılığı yüzdesi (ör. %85 üzeri).\n  - Vaka ölüm hızı (CFR) değişimi.\n  - İkincil atak hızındaki düşüş oranı.\n- **Yönetimsel Önemi:** Süreç göstergelerindeki aksama erken fark edilirse, vaka sayıları patlamadan operasyonel hata düzeltilir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Süreç Göstergesi vs Çıktı Göstergesi",
                "Süreç Göstergesi (Operasyonel Hız)",
                "Temaslıların ilk 24 saatte aranma oranı, testlerin sonuçlanma süresi gibi operasyonel kalite adımlarıdır.",
                "Çıktı/Sonuç Göstergesi (Epidemiyolojik Etki)",
                "Aşılama kapsayıcılığı yüzdesi, vaka ölüm hızı (CFR) ve morbiditedeki net azalma gibi nihai sonuçlardır."
            ),
            make_cloze(
                "Müdahalelerin kapsamını ve operasyonel kalitesini izlemek için süreç ve çıktı göstergeleri kullanılır.",
                "göstergeleri",
                "Performans ve etki ölçüm kriterleri"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-14-s48",
        "title": "Sağlık Müdahalelerinin Üç Temel Amacı",
        "content": "Kapsamlı bir salgın yanıtında yürütülen tüm sağlık müdahaleleri nihai olarak 3 temel hedefe odaklanır (Sınav Spotu):\n\n- **1. Bulaşmayı Azaltmak (Amacın Özü):**\n  - Enfeksiyon zincirini kırmak, yeni ikincil vakaların ortaya çıkmasını engellemek ve R0/Rt değerini 1'in altına düşürmek.\n  - Yöntemler: İzolasyon, karantina, maske, el hijyeni, fiziksel mesafe, filyasyon.\n- **2. Ağır Morbidite ve Mortaliteyi Azaltmak:**\n  - Hastalanan kişilerin hayatını kurtarmak, yoğun bakım ihtiyacını ve kalıcı sakatlıkları en aza indirmek.\n  - Yöntemler: Erken tanı, etkili triyaj, doğru destekleyici tedavi, oksijen desteği, antiviraller ve antibiyotikler.\n- **3. Sağlık Sistemleri ile Politik ve Sosyoekonomik Etkiyi Azaltmak:**\n  - Hastanelerin ve yoğun bakımların tıkanmasını önlemek; rutin sağlık hizmetlerinin (kanser, kalp cerrahisi, doğum) aksamasını engellemek.\n  - Toplumun ekonomik çöküşünü, gıda arzı kesintilerini ve politik istikrarsızlığı sınırlandırmak.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Halk sağlığı ilkelerine göre salgın döneminde uygulanan tam sağlık müdahalelerinin üç temel amacı hangi seçenekte doğru özetlenmiştir?",
                [
                    {"key": "A", "text": "Yalnızca ilaç fabrikalarının kârını artırmak, ithalatı kesmek ve sınırları kapatmak", "isCorrect": False, "explanation": "İlaç kârı veya ithalat ticari kavramlardır; halk sağlığının tıbbi amaçları arasında yer almaz."},
                    {"key": "B", "text": "Bulaşmayı azaltmak, ağır morbidite ve mortaliteyi azaltmak, sağlık sistemleri ve toplum üzerindeki etkiyi azaltmak", "isCorrect": True, "explanation": "Doğru cevap B'dir: Ders notunda vurgulanan üç ana hedef: (a) bulaşmayı, (b) ağır morbidite/mortaliteyi, (c) sağlık sistemleri ve sektörler üzerindeki etkiyi azaltmaktır."},
                    {"key": "C", "text": "Tüm nüfusu zorunlu olarak hastanelere yatırmak ve taburculukları yasaklamak", "isCorrect": False, "explanation": "Tüm nüfusu hastaneye yatırmak sistemi dakikalar içinde çökertir."},
                    {"key": "D", "text": "Laboratuvar testlerini durdurarak vaka sayısını sıfır göstermek", "isCorrect": False, "explanation": "Testleri durdurmak epidemiyolojik körlüktür."}
                ]
            ),
            make_recall(
                "Salgın müdahalelerinde 'sağlık sistemleri üzerindeki etkiyi azaltmak' neden kritik bir hedeftir?",
                "Çünkü sağlık sistemi aşırı yüklenirse sadece salgın hastaları değil; kalp krizi, travma, inme veya doğum gibi acil rutin hastalar da bakım alamayarak hayatını kaybeder."
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-14-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Kapsamlı Salgın Yanıtının Dört Temel Bileşeni",
        "content": "Bu checkpointte salgın yönetim mekanizmasının kurumsal bileşenlerini ve bilgi akışını pekiştiriyoruz:\n\n- **Dört Temel Bileşen:** Kurumlar arası koordinasyon, tam sağlık enformasyonu, doğru risk iletişimi ve tam sağlık müdahaleleri.\n- **Acil Operasyon Merkezi (ASOM / EOC):** Kararların tek elden alındığı özel fiziksel ve teknolojik komuta merkezi.\n- **Ortak Eylem Planı:** Paydaşların görev, yetki ve sorumluluklarını tanımlayan, dinamik olarak güncellenen ana kılavuz.\n- **İki Enformasyon Türü:** Sürveyans bilgisi (kişi-zaman-yer) ve Müdahale bilgisi (süreç ve çıktı göstergeleri).\n- **Müdahale Amaçları:** (1) Bulaşmayı azaltmak, (2) Ağır morbidite/mortaliteyi azaltmak, (3) Sağlık sistemleri ve toplum üzerindeki hasarı en aza indirmek.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Salgın Yanıtının 4 Bileşeninin Entegrasyonu",
                [
                    "1. Koordinasyon (ASOM): Tüm kurumlar fiziksel merkezde ortak komuta altında birleşir.",
                    "2. Enformasyon (Sürveyans ve Müdahale): Sahadan gelen kişi-zaman-yer ve süreç verileri analiz edilir.",
                    "3. Sağlık Müdahaleleri: Triyaj, klinik bakım, filyasyon ve temaslı takibi sahaya yayılır.",
                    "4. Risk İletişimi: Alınan kararlar ve korunma önlemleri şeffaf biçimde topluma aktarılır."
                ]
            ),
            make_table(
                ["Kavram", "Tanım ve Kilit Özellik", "Salgındaki Hayati Rolü"],
                [
                    ["ASOM / EOC", "Özel donanımlı fiziksel kriz komuta merkezi", "Farklı kurumların aynı masada anlık karar almasını sağlar"],
                    ["Sürveyans Bilgisi", "Kişi, zaman ve yer dağılımı", "Patojenin kimleri ve hangi coğrafyayı vurduğunu gösterir"],
                    ["Müdahale Bilgisi", "Süreç (filyasyon hızı) ve çıktı (aşılama oranı) verisi", "Operasyonel darboğazları ve müdahalenin başarısını ölçer"]
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-14-s50",
        "title": "Mini Vaka: İl Sağlık Müdürlüğünde Salgın Yanıtı ve ASOM Yönetimi",
        "content": "Güneydoğu Anadolu bölgesindeki 1 milyon nüfuslu bir ilde, aniden yüksek ateş, kusma ve kanamalı diyare ile başvuran 45 vaka tespit ediliyor. İl Sağlık Müdürü salgın yanıtını başlatıyor:\n\n- **İlk Karar:** İl Sağlık Müdürlüğü bünyesinde derhal **Acil Sağlık Operasyon Merkezi (ASOM)** aktive ediliyor. Emniyet, Belediye Su ve Kanalizasyon İdaresi, İl Tarım Müdürlüğü ve Kızılay temsilcileri masaya çağrılıyor.\n- **Sürveyans Analizi:** Vakaların tamamının aynı ilçede ve aynı ana su isale hattı çevresinde yaşadığı (Yer), yaş ortalamasının 18-45 olduğu (Kişi) ve vakaların son 48 saatte patladığı (Zaman) saptanıyor.\n- **Müdahale Bilgisi:** Test sonuçlarının çıkış süresinin 36 saate uzadığı (süreç aksaması) görülüyor ve hemen ek PCR cihazı talep ediliyor.\n- **Hedef:** Su şebekesi klorlaması artırılarak bulaş kesiliyor, hastanelerde sıvı-elektrolit ve antibiyotik triyajı kurularak mortalite sıfırda tutuluyor.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Klinik Karar: İl Sağlık Müdürü Olarak Kritik Öncelik",
                "ASOM masasında Belediye Başkanı su şebekesinde arıza olmadığını iddia ederken, hastanelerden her saat 10 yeni ağır vaka bildiriliyor. İlk operasyonel adımınız ne olmalıdır?",
                [
                    {
                        "text": "Belediyeyle tartışmaya girmeyip sadece hastanedeki doktorların fazla mesai yapmasını emretmek",
                        "outcome": "Hatalı yaklaşım: Kaynak (şebeke suyu) kapatılmazsa hastanelere binlerce yeni vaka gelir ve sistem çöker.",
                        "isCorrect": False
                    },
                    {
                        "text": "ASOM yetkisiyle ilgili bölgeye derhal süperklorlama yaptırmak, tankerle temiz içme suyu sağlamak ve halka suyu kaynatma uyarısı yayınlamak",
                        "outcome": "Mükemmel epidemiyolojik müdahale: Bulaş kaynağı hemen kesilir, morbidite sınırlandırılır ve kurumlar arası koordinasyon işletilir.",
                        "isCorrect": True
                    },
                    {
                        "text": "Salgın haberini basından gizleyip tüm tahlilleri Ankara'ya göndermek",
                        "outcome": "Tehlikeli ve etik dışı: Zaman kaybı ölümleri artırır ve infodemi patlar.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada İl Sağlık Müdürlüğü'nün ASOM çatısı altında Belediye Su İdaresi ve İl Tarım'ı sürece dahil etmesi salgın yanıtının hangi temel özelliğine örnektir?",
                [
                    {"key": "A", "text": "Kurumlar arası koordinasyon", "isCorrect": True, "explanation": "Doğru cevap A'dır: Farklı kamu kurumlarının (sağlık, belediye, tarım) ortak masa etrafında birlikte çalışması 'kurumlar arası koordinasyon' ilkesinin birebir uygulamasıdır."},
                    {"key": "B", "text": "Biyokimyasal mutasyon analizi", "isCorrect": False, "explanation": "Bu laboratuvar analizidir."},
                    {"key": "C", "text": "Küresel eradikasyon sertifikasyonu", "isCorrect": False, "explanation": "Eradikasyon dünya çapında yok olmadır, yerel operasyonel koordinasyonla ilgisi yoktur."},
                    {"key": "D", "text": "Yalnızca klinik palyatif bakım", "isCorrect": False, "explanation": "Palyatif bakım terminal dönem hastaları içindir."}
                ]
            )
        ]
    })

    return slides
