# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-14-s11",
        "title": "Bir Sonraki Salgına Hazırlığın Dört Temel Direği",
        "content": "Gelecekteki salgınların felakete dönüşmesini engellemek için Dünya Sağlık Örgütü (DSÖ) hazırlık stratejisini dört ana sütun üzerine kurmuştur:\n\n1. **İyi Bir Sürveyans Sistemi:** Erken uyarı ağları, şüpheli vakaların anında tespiti ve güvenilir laboratuvar doğrulaması.\n2. **Sağlıklı Bir Çevre (Tek Sağlık):** Zoonotik sıçramaları önlemek için yaban hayatı ve tarımsal çevre dengesinin korunması.\n3. **Bilimsel Yatırım ve Araştırma-Geliştirme:** Patojen genom dizileme, hızlı aşı ve antiviral geliştirme platformlarına sürekli finansman.\n4. **Güçlü ve Esnek Sağlık Sistemleri:** Ani hasta akışını absorbe edebilecek eğitimli, korunan işgücü ve adil sağlık finansmanı.\nBu dört unsurdan birinin eksikliği tüm savunma kalkanını çökertir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Reaktif Kriz Yanıtı vs Proaktif Salgın Hazırlığı",
                "Reaktif Yaklaşım (Kriz Patlayınca)",
                "Patojen yayıldıktan sonra panik halinde önlem alınır; maliyet ve can kaybı çok yüksektir.",
                "Proaktif Hazırlık (Dört Direk Modeli)",
                "Sürveyans, çevre, bilimsel yatırım ve güçlü altyapı ile salgın henüz yerelken bastırılır."
            ),
            make_cloze(
                "Salgınlara hazırlığın dört temel direği sürveyans sistemi, sağlıklı çevre, bilimsel yatırım ve güçlü sağlık sistemleridir.",
                "sağlıklı çevre",
                "Zoonotik sıçramaları önleyen ekolojik sütun"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-14-s12",
        "title": "Tek Sağlık (One Health) Yaklaşımı: Bölünemez Sağlık",
        "content": "Tek Sağlık (One Health), insan sağlığının hayvan sağlığı ve paylaştığımız çevre sağlığı ile ayrılmaz bir bütün olduğunu savunan disiplinler arası küresel bir yaklaşımdır:\n\n- **Geleneksel Tıbbın Hatası:** İnsan hekimliği sadece hastaneye gelen insanı tedavi etmeye odaklanmış; hayvan popülasyonlarındaki virüs döngülerini ve ekosistem tahribatını görmezden gelmiştir.\n- **Bütünleşik Çözüm:** Beşeri hekimler, veteriner hekimler, epidemiyologlar, çevre bilimciler ve vahşi yaşam uzmanları aynı masada ortak veri paylaşımı yapmalıdır.\n- **Hedef:** Virüs bir hayvandan insana sıçramadan önce ormanda, çiftlikte veya pazarda tespit edilip kontrol altına alınmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Tek Sağlık (One Health) Entegrasyon Çarkı",
                [
                    "1. Yaban Hayatı İzlemi: Yarasalarda ve kemirgenlerde dolaşan yeni virüslerin taranması.",
                    "2. Veteriner Sürveyansı: Çiftlik hayvanları ve canlı hayvan pazarlarında bulaş riskinin izlenmesi.",
                    "3. Çevresel Koruma: Ormansızlaşma ve ekolojik tahribatın önlenerek türlerin izolasyonu.",
                    "4. Beşeri Erken Uyarı: Zoonotik sıçrama anında klinisyenin vakayı tanıyıp filyasyonu başlatması."
                ]
            ),
            make_recall(
                "İnsan, hayvan ve çevre sağlığının birbiriyle ayrılmaz şekilde bağlantılı olduğunu savunan ve salgınların önlenmesinde esas alınan çok disiplinli yaklaşıma ne ad verilir?",
                "Tek Sağlık (One Health) yaklaşımıdır.",
                "Üçlü sağlık dengesi yaklaşımı"
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-14-s13",
        "title": "Zoonotik Tehditler: Yeni Patojenlerin %70'i Hayvan Kaynaklıdır",
        "content": "Halk sağlığı istatistikleri, modern çağın enfeksiyon tehditleri hakkında çarpıcı ve tartışmasız bir gerçeği ortaya koymaktadır:\n\n- **%70 Kuralı (Sınav Spotu):** İnsanlarda yeni ortaya çıkan (emerging) bulaşıcı hastalıkların **yaklaşık %70'i hayvan kaynaklıdır (zoonozdur)!**\n- **Rezervuarlar:**\n  - Yarasalar: Kuduz, Ebola, Marburg, Nipah, Hendra, SARS ve SARS-CoV-2 rezervuarıdır.\n  - Kemirgenler: Hantavirüs, Veba, Lassa ateşi, Leptospiroz rezervuarıdır.\n  - Kuşlar: Yüksek patojeniteli Avian İnfluenza (Kuş Gribi - H5N1, H7N9) rezervuarıdır.\n- **Kritik Çıkarım:** Yaban hayatı ve hayvan sağlığı kontrol edilmeden insanları salgınlardan korumak biyolojik olarak imkansızdır!",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "İnsan popülasyonunda yeni ortaya çıkan (emerging) enfeksiyon hastalıklarının yaklaşık yüzde kaçı hayvanlardan insanlara sıçrayan zoonotik patojenlerdir?",
                [
                    {"key": "A", "text": "%70", "explanation": "A seçeneği DOĞRUDUR: Yeni insan patojenlerinin yaklaşık %70'i hayvan kaynaklıdır."},
                    {"key": "B", "text": "%10", "explanation": "B seçeneği yanlıştır: Zoonotik oran çok daha yüksektir."},
                    {"key": "C", "text": "%25", "explanation": "C seçeneği yanlıştır: Zoonotik yükün altında kalır."},
                    {"key": "D", "text": "%40", "explanation": "D seçeneği yanlıştır: Gerçek oran yaklaşık %70'tir."},
                    {"key": "E", "text": "%99", "explanation": "E seçeneği yanlıştır: Patojenlerin tümü zoonotik değildir."}
                ],
                "A"
            ),
            make_cloze(
                "Yeni ortaya çıkan insan enfeksiyon hastalıklarının yaklaşık yüzde yetmişi hayvan kaynaklı zoonotik patojenlerden köken almaktadır.",
                "yüzde yetmişi",
                "Zoonotik patojenlerin oransal ağırlığı"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-14-s14",
        "title": "Çevresel Bozulma, Yoğun Hayvancılık ve Islak Pazarlar",
        "content": "Patojenlerin hayvanlardan insanlara sıçramasını (spillover) hızlandıran üç büyük insan yapımı faktör bulunmaktadır:\n\n1. **Ormansızlaşma ve Yaşam Alanı Kaybı:** Tropikal ormanların tarım veya madencilik için yok edilmesi, vahşi hayvanları insan yerleşimlerine yaklaşmaya zorlar (yarasaların meyve bahçelerine gelmesi gibi).\n2. **Endüstriyel Yoğun Hayvancılık:** Binlerce genetik olarak tekdüze hayvanın dar alanlarda tutulması, virüslerin hızla mutasyona uğrayıp virulans kazanması için kusursuz bir kuluçka makinesi (bioreaktör) işlevi görür.\n3. **Canlı Yaban Hayatı Pazarları (Wet Markets):** Farklı türden vahşi ve evcil hayvanların stres altında üst üste kafeslendiği, kan ve dışkıların karıştığı pazarlar türler arası sıçramanın merkez üssüdür.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Doğal Denge vs Ekolojik Bozulmanın Salgın Riski",
                "Bozulmamış Doğal Ekosistem",
                "Virüsler kendi yaban rezervuarları içinde sınırlı kalır; seyreltme etkisiyle insana sıçramaz.",
                "Ekolojik Bozulma ve Canlı Pazarlar",
                "Bariyerler kalkar; vahşi türler insanla doğrudan temas eder; kitlesel sıçramalar tetiklenir."
            ),
            make_recall(
                "Farklı vahşi ve evcil hayvan türlerinin canlı satıldığı, hijyenik olmayan ve türler arası virüs sıçramasını kolaylaştıran geleneksel pazarlara ne ad verilir?",
                "Islak pazarlardır (canlı hayvan pazarları / wet markets).",
                "Zoonotik sıçramanın beşiği olan pazar tipi"
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-14-s15",
        "title": "Sürveyansın Temeli: Tanı İlk Olarak Klinisyenle Başlar",
        "content": "Dünyanın en gelişmiş dijital izleme algoritmaları veya yapay zeka sistemleri dahi tek bir hekimin klinik şüphesinin yerini tutamaz:\n\n- **Altın İlke (Sınav Spotu):** Salgınların erken uyarısında tanı **ilk olarak klinisyenle başlar!**\n- **Klinisyenin Uyanıklığı:** Acil serviste veya poliklinikte çalışan bir hekim, alışılagelmişin dışında seyreden, standart tedaviye yanıt vermeyen veya aynı aileden/bölgeden benzer şikayetlerle gelen hastaları fark ettiğinde alarm zillerini çalmalıdır.\n- **Bildirim Zinciri:** Klinisyen vakayı şüphelendiği anda halk sağlığı otoritesine bildirmelidir. Klinisyenin atladığı veya bildirmeyi unuttuğu bir vaka, haftalar içinde tüm şehri veya ülkeyi saran kontrolsüz bir salgına dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "İlçe devlet hastanesi acil servisinde nöbetçisiniz. Aynı köyden gelen 3 farklı hastada ani başlayan yüksek ateş, şiddetli trombositopeni ve ciltte peteşiyal kanamalar fark ediyorsunuz. Hastalardan biri kene tutunması öyküsü veriyor.",
                "Bir klinisyen olarak halk sağlığı sürveyansı ve salgın kontrolü açısından en öncelikli göreviniz nedir?",
                [
                    {
                        "text": "Olası Kırım-Kongo Kanamalı Ateşi salgını şüphesiyle hastaları derhal izole edip İl Sağlık Müdürlüğü Bulaşıcı Hastalıklar Birimine acil vaka bildirimi yapmaktır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Tanı klinisyenle başlar; kümeleşen şüpheli olguların anında filyasyon için yetkililere bildirilmesi salgını büyümeden durdurur."
                    },
                    {
                        "text": "Hastalara antibiyotik reçete edip 1 hafta sonra kontrole çağırmaktır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Viral kanamalı ateş antibiyotiğe yanıt vermez ve bildirim yapılmazsa toplumda yayılır."
                    },
                    {
                        "text": "Yalnızca hastane başhekimine sözlü bilgi verip başka hiçbir işlem yapmamaktır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Resmi bulaşıcı hastalık bildirim sistemine derhal girilmeli ve acil temaslı taraması başlatılmalıdır."
                    }
                ]
            ),
            make_cloze(
                "Salgın erken uyarı ve sürveyans sistemlerinde yeni veya olağan dışı bir tehdidin ilk fark edilmesi klinisyen ile başlar.",
                "klinisyen",
                "Hastayı ilk gören hekimin mesleki unvanı"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-14-s16",
        "title": "Tanısal Gecikmenin Bedeli: Ebola'da 2 Aylık Körlük",
        "content": "Tarih, erken tanı ve sürveyanstaki en ufak bir aksamanın ne denli büyük bir insani trajediye yol açabileceğinin acı örnekleriyle doludur:\n\n- **Gine Vakası (Aralık 2013):** Salgının ilk vakası (indeks vaka) 2 yaşındaki bir çocuktu. Çocuk ve ardından ailesi hayatını kaybetti.\n- **İki Aylık Tanı Körlüğü (Sınav Spotu):** Bölgedeki yerel sağlık çalışanları ölümleri kolera veya Lassa ateşine bağladı; gerekli numuneler alınıp doğru laboratuvara gönderilemedi.\n- **Sonuç:** Ebola virüsü **tam iki ay boyunca resmi olarak teşhis edilemeden** üç ülkenin sınırlarından serbestçe geçti ve mega-kentlere ulaştı. Zamanında sınırlanamayan salgın 11.000'den fazla can aldı.\n- **Ders:** Şüpheli kümeleşmelerde erken laboratuvar teyidi hayat kurtarır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Erken Teşhis (İlk Gün) vs Gecikmiş Teşhis (2 Ay)",
                "Erken Teşhis ve Sınırlama",
                "İlk birkaç vaka karantinaya alınır; temaslılar taranır; salgın birkaç haftada söndürülür.",
                "2 Aylık Tanı Gecikmesi (Ebola 2014)",
                "Bulaş zincirleri kontrolden çıkar; virüs şehirlere yayılır; on binlerce insan ölür ve ekonomi çöker."
            ),
            make_recall(
                "2014 Batı Afrika Ebola salgınında salgının başlangıcında yerel sağlık sisteminin kaç ay boyunca virüsü teşhis edememesi küresel krize yol açmıştır?",
                "Tam iki ay (yaklaşık 60 gün) boyunca tanı konulamamıştır.",
                "Ebola'nın teşhissiz yayıldığı ay sayısı"
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-14-s17",
        "title": "Sağlık Sistemlerinin Esnekliği (Resilience) ve Kapasite",
        "content": "Salgınlar başladığında sağlık sistemleri daha önce hiç görmedikleri devasa bir stres testine tabi tutulurlar:\n\n- **Sağlık Sistem Esnekliği (Resilience):** Bir sağlık sisteminin şoklara (salgın, deprem, savaş) karşı temel fonksiyonlarını kaybetmeden direnme, uyum sağlama ve kriz anında kapasitesini hızla artırabilme yeteneğidir.\n- **Dalgalanma Kapasitesi (Surge Capacity):** 4 temel bileşenden oluşur (4S kuralı):\n  1. **Staff (İşgücü):** Yedek doktor, hemşire ve sağlık çalışanlarının hızla göreve çağrılması.\n  2. **Stuff (Malzeme):** KKE, ventilatör, oksijen ve ilaç stoklarının hazır olması.\n  3. **Structure (Mekan):** Normal servislerin yoğun bakıma, fuar alanlarının sahra hastanesine dönüştürülmesi.\n  4. **Systems (Sistemler):** Triyaj ve hasta sevk protokollerinin işletilmesi.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Dalgalanma Kapasitesi (4S)", "Açıklama", "Salgındaki Somut Karşılığı"],
                [
                    [
                        {"text": "Staff (İşgücü)", "isMasked": False, "hint": ""},
                        {"text": "Yeterli ve eğitimli sağlık personeli", "isMasked": True, "hint": "Salgını göğüsleyen insan kaynağı"},
                        {"text": "Yedek hekim/hemşire havuzu ve nöbet rotasyonları", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Stuff (Malzeme)", "isMasked": True, "hint": "Tıbbi cihaz ve sarf malzemesi"},
                        {"text": "Kritik tıbbi ekipman ve sarf stoğu", "isMasked": False, "hint": ""},
                        {"text": "KKE, medikal oksijen, mekanik ventilatör, aşı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Structure (Mekan)", "isMasked": False, "hint": ""},
                        {"text": "Fiziksel alan ve izolasyon altyapısı", "isMasked": False, "hint": ""},
                        {"text": "Negatif basınçlı odalar, sahra hastaneleri", "isMasked": True, "hint": "Hastane dışı acil tedavi merkezleri"}
                    ]
                ]
            ),
            make_recall(
                "Sağlık sistemlerinin kriz anında ani hasta akışını göğüslemek için işgücü, mekan, malzeme ve sistemlerini hızla büyütme yeteneğine ne ad verilir?",
                "Dalgalanma kapasitesidir (surge capacity).",
                "Kapasite artırma terimi"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-14-s18",
        "title": "Sağlık Finansmanı ve Acil Kriz Fonları",
        "content": "Salgın başladığında bütçe onayları ve bürokratik ödenek tahsisleri haftalar sürerse mücadele kaybedilir:\n\n- **Önceden Tahsis Edilmiş Acil Fonlar:** Salgın öncesinde hazır tutulan acil durum bütçeleri, kriz çıktığı ilk saatlerde KKE, tanı kiti ve ilaç alımını finanse etmelidir.\n- **Evrensel Sağlık Kapsamı:** Salgın kontrolünün en kritik finansal şartı **hastaların tanı ve tedavisinin tamamen ücretsiz olmasıdır!**\n  - Eğer şüpheli bir hasta hastaneye gittiğinde cebinden para ödemek zorunda kalırsa doktora gitmekten kaçınır.\n  - Teşhis edilemeyen bu hasta topluma karışarak virüsü yüzlerce kişiye bulaştırır.\n- **Yatırımın Geri Dönüşü:** Salgına hazırlık için harcanan 1 dolar, kriz patladığında harcanacak 100 doları ve trilyonlarca dolarlık ekonomik çöküşü önler.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Ücretli Sağlık Hizmeti vs Ücretsiz Salgın Erişimi",
                "Cepten Ödemeli Sistem",
                "Yoksul hastalar test ve tedavi ücreti nedeniyle doktora gitmez; virüs gizlice yayılır.",
                "Evrensel Ücretsiz Erişim",
                "Herkes ilk semptomda çekinmeden başvurur; vakalar erken izole edilir ve salgın durdurulur."
            ),
            make_cloze(
                "Salgın kontrolünde hastaların tanı ve tedaviye ücretsiz erişimi şüpheli vakaların doktora başvurmasını sağlayarak bulaş zincirlerini kırar.",
                "ücretsiz erişimi",
                "Maddi engellerin kaldırılması ilkesi"
            )
        ]
    })

    # Slide 19
    slides.append({
        "id": "k1-14-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Salgına Hazırlık, Tek Sağlık ve Klinisyenin Rolü",
        "content": "Bu kontrol noktasında salgınlara hazırlığın temel taşlarını ve Tek Sağlık yaklaşımını özetliyoruz:\n\n- **Dört Hazırlık Direği:** 1) Sürveyans, 2) Sağlıklı çevre, 3) Bilimsel yatırım, 4) Esnek sağlık sistemi.\n- **Tek Sağlık (One Health):** İnsan, hayvan ve çevre sağlığı bölünmez bir bütündür.\n- **%70 Kuralı:** Yeni insan patojenlerinin yaklaşık %70'i zoonotiktir (hayvan kaynaklı).\n- **Klinisyenin Rolü:** Salgında erken tanı klinisyenle başlar; kümeleşen vakaları fark etmek hekimin sorumluluğudur.\n- **Ebola Dersi:** 2 aylık tanı körlüğü salgını uluslararası krize dönüştürdü.\n- **Esneklik ve Dalgalanma Kapasitesi (4S):** Staff (işgücü), Stuff (malzeme), Structure (mekan), Systems (sistemler).\n- **Finansman:** Ücretsiz tanı ve tedavi salgın kontrolünün mutlak şartıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Salgınlara hazırlık ve erken uyarı sistemlerinde yeni bir salgın tehdidinin ilk olarak fark edilmesini sağlayan ve sürveyansın temel tetikleyicisi olan aktör kimdir?",
                [
                    {"key": "A", "text": "Hastayı ilk değerlendiren klinisyen hekim", "explanation": "A seçeneği DOĞRUDUR: Tanı klinisyenle başlar; klinisyenin şüphesi ve bildirimi sürveyansı harekete geçirir."},
                    {"key": "B", "text": "Havaalanı pasaport polisi", "explanation": "B seçeneği yanlıştır: Tıbbi tanı koyamaz."},
                    {"key": "C", "text": "İlaç fabrikası yöneticisi", "explanation": "C seçeneği yanlıştır: Üretim tarafıdır."},
                    {"key": "D", "text": "Uluslararası turizm acenteleri", "explanation": "D seçeneği yanlıştır: Sağlık aktörü değildir."},
                    {"key": "E", "text": "Sosyal medya fenomenleri", "explanation": "E seçeneği yanlıştır: Genellikle infodemi kaynağıdır."}
                ],
                "A"
            ),
            make_cloze(
                "İnsan, hayvan ve çevre sağlığını tek bir çatı altında birleştiren küresel halk sağlığı yaklaşımı Tek Sağlık yaklaşımıdır.",
                "Tek Sağlık",
                "One Health Türkçe karşılığı"
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-14-s20",
        "title": "Salgınlarda Korku, Panik ve İrrasyonel Kararların Engellenmesi",
        "content": "Salgınlar sadece biyolojik ajanların yayılması değil, aynı zamanda kitlesel korku ve psikolojik travma dalgalarıdır:\n\n- **Korkunun Getirdiği Tehlike:** Panik ve belirsizlik; halkın hastanelere kontrolsüz hücum etmesine, KKE ve ilaç stokçuluğuna, sağlık çalışanlarının darp edilmesine ve yabancılara karşı ırkçılık/damgalamaya (stigmatizasyon) yol açar.\n- **Hatalı Yönetici Kararları:** Yöneticiler korku ve politik baskı altında bilimsel temeli olmayan kararlar alabilirler (etkisiz seyahat yasakları, faydasız sokak dezenfeksiyonları, kanıtlanmamış ilaçların dağıtılması).\n- **Çözüm:** Bilimsel verilere dayalı, şeffaf, açık ve dürüst bir liderlik sergilemektir. Gerçekler halktan gizlenmemeli, belirsizlikler açıkça ifade edilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Panik Odaklı Kriz Yönetimi vs Bilimsel Şeffaf İletişim",
                "Panik ve Gizleme Yaklaşımı",
                "Gerçekler gizlenir; dedikodular yayılır; halk sağlık otoritesine güvenini tamamen kaybeder.",
                "Bilimsel ve Şeffaf Liderlik",
                "Veriler dürüstçe paylaşılır; belirsizlikler açıklanır; toplumla karşılıklı güven inşa edilir."
            ),
            make_recall(
                "Salgın dönemlerinde yöneticilerin ve halkın bilimsel kanıtlara dayanmayan, panik ve önyargıyla aldığı hatalı kararların temel psikolojik tetikleyicisi nedir?",
                "Korku ve bilgi eksikliğidir (şeffaf iletişimin olmaması).",
                "İrrasyonel kararların arkasındaki duygusal durum"
            )
        ]
    })

    return slides
