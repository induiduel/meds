# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-14-s21",
        "title": "Salgın Sürecinin Dört Epidemik Fazı ve Karşılık Gelen Müdahaleler",
        "content": "Dünya Sağlık Örgütü (DSÖ), bir salgının evrimini ve her evrede uygulanması gereken halk sağlığı müdahalelerini **dört epidemik fazda** modeller:\n\n1. **Faz 1: Giriş / Ortaya Çıkış (Emergence):** Patojenin topluma ilk sızması → **Müdahale: Bekleme ve Öngörü (Anticipation)**.\n2. **Faz 2: Lokal Yayılım (Local Transmission):** İlk vakalar ve sınırlı kümelenmeler → **Müdahale: Erken Teşhis ve Sınırlama (Containment)**.\n3. **Faz 3: Amplifikasyon (Amplification):** Salgının katlanarak büyümesi ve yaygın toplum içi bulaş → **Müdahale: Kontrol ve Etkiyi Azaltma (Mitigation)**.\n4. **Faz 4: Azalma ve Sönümlenme (Decline):** Bağışıklık veya müdahalelerle vakaların düşüşe geçmesi → **Müdahale: Eliminasyon veya Eradikasyon**.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Epidemik Faz", "Fazın Epidemiyolojik Tanımı", "Uygulanacak Temel Müdahale"],
                [
                    [
                        {"text": "1. Giriş / Ortaya Çıkış", "isMasked": False, "hint": ""},
                        {"text": "Patojenin insan popülasyonuna ilk adımı", "isMasked": False, "hint": ""},
                        {"text": "Bekleme ve Öngörü (Anticipation)", "isMasked": True, "hint": "Olası riskleri önceden tahmin etme"}
                    ],
                    [
                        {"text": "2. Lokal Yayılım", "isMasked": False, "hint": ""},
                        {"text": "Sınırlı yerel vaka kümeleri", "isMasked": False, "hint": ""},
                        {"text": "Erken Teşhis ve Sınırlama (Containment)", "isMasked": True, "hint": "İlk vakada başlayan karantina"}
                    ],
                    [
                        {"text": "3. Amplifikasyon", "isMasked": True, "hint": "Salgının patlama evresi"},
                        {"text": "Kontrolsüz yaygın toplum bulaşı", "isMasked": False, "hint": ""},
                        {"text": "Kontrol ve Etkiyi Azaltma (Mitigation)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "4. Azalma", "isMasked": False, "hint": ""},
                        {"text": "Duyarlı havuzunun tükenmesi ve sönümlenme", "isMasked": False, "hint": ""},
                        {"text": "Eliminasyon veya Eradikasyon", "isMasked": True, "hint": "Bölgesel veya küresel yok etme"}
                    ]
                ]
            ),
            make_recall(
                "Salgın sürecinin üçüncü fazı olan ve salgının katlanarak büyüyüp yaygın toplum içi bulaşa dönüştüğü döneme ne ad verilir?",
                "Amplifikasyon fazıdır (büyüme / patlama fazı).",
                "Katlanarak büyüme anlamına gelen epidemik faz adı"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-14-s22",
        "title": "Faz 1: Giriş ve Bekleme / Öngörü Stratejisi",
        "content": "Salgının birinci fazı, patojenin hayvandan insana sıçradığı ya da bir seyahatçi ile ülkeye sızdığı ilk evredir:\n\n- **Öngörülebilirlik Paradoksu:** Yeni bir virüsün tam olarak hangi gün, nerede ve hangi genetik mutasyonla çıkacağını nokta atışı bilmek imkansızdır; ancak **tahmin edilebilir ve öngörülebilir**!\n- **Risk Tahmini (Öngörü):** Bölgedeki yaban hayatı döngüleri, iklim değişiklikleri, göç hareketleri ve mevsimsel koşullar analiz edilerek en olası patojenler ve yayılmayı kolaylaştıracak 'sürücüler' (drivers) önceden modellenir.\n- **Hızlı Araştırma Kapasitesi:** Yeni ve bilinmeyen bir patojen belirdiği anda laboratuvarların patojeni izole edip genom dizilimini 48 saat içinde çıkaracak Ar-Ge altyapısı hazır bekletilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Pasif Bekleyiş vs Aktif Öngörü (Anticipation)",
                "Pasif Bekleyiş",
                "Salgın çıkana kadar hiçbir hazırlık yapılmaz; virüs gelince şaşkınlık ve gecikme yaşanır.",
                "Aktif Öngörü Stratejisi",
                "En olası tehditler ve sürücüler önceden modellenir; tanı kitleri ve protokoller hazır tutulur."
            ),
            make_cloze(
                "Salgın sürecinin birinci fazı olan giriş evresinde uygulanması gereken temel halk sağlığı müdahalesi bekleme ve öngörü stratejisidir.",
                "bekleme ve öngörü",
                "Tehdidi önceden tahmin etme müdahalesi"
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-14-s23",
        "title": "Risk Değerlendirmesi: Salgını Tetikleyen Sürücüler",
        "content": "Bir salgının patlamasında patojenin virulansı kadar, çevresel ve toplumsal **yayılma sürücüleri (drivers)** de belirleyicidir:\n\n1. **Ekolojik Sürücüler:** Kuraklık, seller, orman yangınları veya baraj inşaatları kemirgen ve sivrisinek popülasyonlarını insan yerleşimlerine kaydırır.\n2. **Demografik ve Davranışsal Sürücüler:** Hızlı plansız kentleşme, aşırı kalabalık kamplar, göçmen dalgaları ve yetersiz sanitasyon.\n3. **Sağlık Sistemi Zayıflıkları:** Düşük aşılama oranları, KKE eksikliği, nozokomiyal enfeksiyon kontrolsüzlüğü.\n- **Erken Risk Değerlendirmesi:** Bu sürücüler önceden analiz edilerek 'Hangi mahallede kolera patlayabilir?', 'Hangi sınır kapısından kızamık girebilir?' sorularının yanıtı aranır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Risk Değerlendirmesi ve Sürücü Analiz Basamakları",
                [
                    "1. Tehdit Tanımlama: Çevrede dolaşan potansiyel viral ve bakteriyel ajanların listelenmesi.",
                    "2. Kırılganlık Haritalama: Aşı kapsayıcılığı düşük, altyapısı zayıf bölgelerin tespiti.",
                    "3. Sürücü Değerlendirmesi: İklim, mevsim ve göç dinamiklerinin yayılma riskine etkisinin analizi.",
                    "4. Hazırlık Planının Tetiklenmesi: Riskli bölgelere erken ilaç, tanı kiti ve personel sevkiyatı."
                ]
            ),
            make_recall(
                "Salgınların ortaya çıkışını ve yayılmasını kolaylaştıran ekolojik, demografik ve davranışsal tetikleyici etkenlere genel olarak ne ad verilir?",
                "Yayılma sürücüleridir (epidemic drivers).",
                "Salgını körükleyen itici faktörler"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-14-s24",
        "title": "Faz 2: Lokal Yayılım ve Erken Teşhis",
        "content": "İkinci fazda patojen ilk insan konaklarını enfekte etmiş ve sınırlı bir yerel küme (aile, iş yeri, hastane) içinde bulaşmaya başlamıştır:\n\n- **Kritik Eşik:** Bu faz, büyük bir felaketi önlemek için insanlığın elindeki **en değerli ve son fırsat penceresidir**.\n- **Erken Teşhisin Hayati Önemi:** İlk birkaç vakanın semptomları başladığı anda hızlı tanı testleriyle (PCR, antijen) doğrulanması gerekir.\n- **İndeks Vaka:** Topluma enfeksiyonu ilk getiren veya sağlık otoritesince ilk saptanan vakadır. İndeks vakanın seyahat geçmişi ve temaslıları saniyeler içinde geriye doğru taranmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Lokal Yayılımda Müdahale vs Müdahalesizlik",
                "Hemen Müdahale (Faz 2)",
                "İlk 10 vaka ve temaslıları izole edilir; salgın büyümeden 14 günde tamamen biter.",
                "Müdahalesiz Bırakma",
                "Eksponansiyel çoğalma başlar; 10 vaka 1 ay sonra 10.000 vakaya dönüşür ve amplifikasyona geçer."
            ),
            make_cloze(
                "Bir salgın incelemesinde sağlık otoritesi tarafından ilk tespit edilen veya topluma enfeksiyonu ilk sokan hastaya indeks vaka denir.",
                "indeks vaka",
                "Salgının ilk resmi vakası terimi"
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-14-s25",
        "title": "Sınırlama (Containment) İlkesi: İlk Vakada Başlayan Yangın Söndürme",
        "content": "Salgın kontrolünde zaman en acımasız düşmandır. Bu nedenle sınırlama müdahalesi katı bir kurala tabidir:\n\n- **Temel Prensip (Sınav Spotu):** Sınırlama (containment) müdahalesi **ilk vaka teşhis edildiği anda başlamalıdır!**\n- **Laboratuvarı Beklemeden Harekete Geçme:** Patojenin türü, alt varyantı veya kesin genetik dizilimi henüz tam netleşmemiş olsa dahi, epidemiyolojik klinik şüphe oluştuğu anda izolasyon ve temaslı sınırlaması başlatılmalıdır.\n- **Karantina ve İzolasyon Kordonu:** Enfekte hasta derhal hava/temas izolasyon odasına alınır; lezyon bölgesine giriş-çıkışlar kontrol altına alınır ve yayılma çemberi fiziksel olarak daraltılır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Büyük çaplı bir salgının önlenmesinde hayati olan 'sınırlama' (containment) müdahalesi tam olarak ne zaman başlatılmalıdır?",
                [
                    {"key": "A", "text": "İlk vaka teşhis edildiği anda derhal başlatılmalıdır", "explanation": "A seçeneği DOĞRUDUR: Sınırlama ilk vaka saptandığı anda, patojen tam tanımlanmasa bile gecikmeksizin başlar."},
                    {"key": "B", "text": "Toplumda en az 100 ölüm gerçekleştikten sonra", "explanation": "B seçeneği yanlıştır: Bu aşamada sınırlama fırsatı çoktan kaçmıştır."},
                    {"key": "C", "text": "Hastalığa karşı etkin aşı üretilip piyasaya sürüldüğünde", "explanation": "C seçeneği yanlıştır: Aşı aylarca sürebilir, sınırlama hemen uygulanır."},
                    {"key": "D", "text": "DSÖ küresel pandemi ilan ettikten sonra", "explanation": "D seçeneği yanlıştır: Pandemi faz 3'tür, sınırlama yerel faz 2'dedir."},
                    {"key": "E", "text": "Salgın kendi kendine azalma fazına girdiğinde", "explanation": "E seçeneği yanlıştır: Bu faz 4'tür."}
                ],
                "A"
            ),
            make_cloze(
                "Salgınların büyük çaplı bir epidemiyolojik felakete dönüşmesini engellemek için sınırlama müdahalesi ilk vaka teşhis edildiği anda başlatılmalıdır.",
                "ilk vaka",
                "Sınırlama müdahalesinin başlangıç zamanı"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-14-s26",
        "title": "Filyasyon ve Temaslı Takibi: Bulaş Zincirini Kırma Dedektifliği",
        "content": "Lokal yayılım fazında salgının belini büken en kritik epidemiyolojik saha çalışması **filyasyon (contact tracing)** işlemidir:\n\n- **Filyasyonun Amacı:** İndeks vakanın bulaştırıcı olduğu süre boyunca temas ettiği tüm kişileri tek tek tespit etmek, bulmak ve izole etmektir.\n- **Temaslı Sınıflandırması:**\n  - Yakın Temaslı (Yüksek Risk): Aynı evde yaşayan, maskesiz 1 metreden yakın 15 dakikadan uzun süre geçirenler → Doğrudan karantinaya alınır.\n  - Düşük Riskli Temaslı: Aynı ortamda kısa süreli bulunanlar → Kendi semptomlarını günlük izlemeleri istenir.\n- **Bulaş Zincirinin Kırılması:** Her temaslı kişi kuluçka süresi boyunca toplumdan izole edildiğinde, virüs yeni bir konak bulamaz ve bulaşma zinciri kırılıp söner.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Filyasyon ve Temaslı Yönetim Protokolü",
                [
                    "1. Vaka Mülakatı: Pozitif çıkan hastayla görüşülerek son 14 günlük hareketleri listelenir.",
                    "2. Temaslı Listesi: Hastanın konuştuğu, aynı ortamı paylaştığı tüm kişiler saptanır.",
                    "3. Sahada Ulaşım: Filyasyon ekipleri temaslıları adreslerinde bulup sağlık kontrolü yapar.",
                    "4. Karantina ve Takip: Temaslılar kuluçka süresince evde izole edilir; semptom çıkarsa test edilir."
                ]
            ),
            make_recall(
                "Salgın odağında bulaşıcı hastalık vakasının temas ettiği kişilerin geriye dönük taranması ve bulaş zincirinin kırılması işlemine ne ad verilir?",
                "Filyasyondur (temaslı takibi / contact tracing).",
                "Epidemiyolojik saha temaslı taraması"
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-14-s27",
        "title": "Faz 3: Amplifikasyon ve Kontrolsüz Toplum Bulaşı",
        "content": "Eğer ikinci fazda sınırlama ve filyasyon başarısız olursa veya patojen aşırı bulaşıcıysa salgın **üçüncü faza (amplifikasyona)** geçer:\n\n- **Eksponansiyel Patlama:** Vaka sayıları lineer değil, logaritmik (katlanarak) artar. 1 vaka 3'e, 3 vaka 9'a, 9 vaka 81'e fırlar.\n- **Bulaş Zincirlerinin Kaybı:** Artık vakaların kaynağı (kimin kimden kaptığı) takip edilemez hale gelir; toplum içi yaygın bulaş (**community transmission**) oturur.\n- **Süper-Bulaştırıcı Olaylar (SSE):** Düğünler, ibadethaneler, konserler ve kapalı havalandırmasız binalar tek bir kişinin onlarca kişiyi enfekte ettiği amplifikasyon jeneratörlerine dönüşür.\n- **Sağlık Sistemi Alarmı:** Hastanelere akın başlar; yatak ve personel kapasiteleri dolma noktasına gelir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Lokal Sınırlı Yayılım vs Amplifikasyon Fazı",
                "Lokal Yayılım (Faz 2)",
                "Bulaş zincirleri bellidir; temaslılar tek tek izlenebilir; hastane kapasitesi zorlanmaz.",
                "Amplifikasyon (Faz 3)",
                "Kaynak belirsizdir; toplumda yaygın bulaş oturmuştur; sağlık sistemi aşırı yük altındadır."
            ),
            make_cloze(
                "Salgının amplifikasyon evresinde vakaların kaynağının tek tek izlenemediği genel yayılıma toplum içi yaygın bulaş denir.",
                "toplum içi yaygın bulaş",
                "Zincirlerin koptuğu genel yayılım terimi"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-14-s28",
        "title": "Etkiyi Azaltma (Mitigation): Eğriyi Düzleştirme Sanatı",
        "content": "Amplifikasyon fazına girildiğinde artık tek tek vakaları sıfırlamaya çalışmak (sınırlama) imkansızdır. Müdahale stratejisi **Kontrol ve Etkiyi Azaltma (Mitigation)** moduna geçer:\n\n- **Temel Amaç:** Virüsü tamamen yok etmek değil; yayılma hızını yavaşlatarak hastane başvurularını zamana yaymak ve **sağlık sisteminin çökmesini engellemektir**.\n- **Eğriyi Düzleştirmek (Flattening the Curve):** Günlük vaka sayısını sağlık sisteminin azami kapasite çizgisinin altında tutmaktır.\n- **Uygulanan Önlemler (Farmakolojik Olmayan Müdahaleler - NPI):**\n  - Okulların ve üniversitelerin kapatılması, uzaktan eğitime geçiş.\n  - Toplu etkinliklerin, konserlerin, spor müsabakalarının iptali.\n  - Kamusal alanlarda maske zorunluluğu, sokağa çıkma kısıtlamaları ve seyahat engelleri.\n  - Ağır vakalara yoğun bakım desteği verilerek mortalitenin düşürülmesi.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Sınırlama (Containment) vs Etkiyi Azaltma (Mitigation)",
                "Sınırlama (Faz 2)",
                "Hedef: Patojenin topluma girmesini durdurmak ve bulaşı tamamen sıfırlamaktır.",
                "Etkiyi Azaltma (Faz 3)",
                "Hedef: Bulaşı durduramayacağını kabul edip yayılma hızını yavaşlatmak ve ölümleri azaltmaktır."
            ),
            make_quiz(
                "Salgının yaygın toplum içi bulaş gösterdiği amplifikasyon fazında, sağlık sisteminin kapasitesinin aşılmasını önlemek amacıyla uygulanan 'eğriyi düzleştirme' odaklı stratejiye ne ad verilir?",
                [
                    {"key": "A", "text": "Etkiyi azaltma ve sönümlendirme (Mitigation)", "explanation": "A seçeneği DOĞRUDUR: Mitigation toplum içi yaygın fazda sağlık sistemini korumak için pik dalgayı zamana yayan stratejidir."},
                    {"key": "B", "text": "Öngörü ve bekleme", "explanation": "B seçeneği yanlıştır: Faz 1 giriş stratejisidir."},
                    {"key": "C", "text": "Küresel eradikasyon", "explanation": "C seçeneği yanlıştır: Faz 4 sonrası nihai yok etme hedefidir."},
                    {"key": "D", "text": "Giriş taraması", "explanation": "D seçeneği yanlıştır: Sınır kapısı önlemidir."},
                    {"key": "E", "text": "Deratizasyon", "explanation": "E seçeneği yanlıştır: Kemirgen mücadelesidir."}
                ],
                "A"
            )
        ]
    })

    # Slide 29
    slides.append({
        "id": "k1-14-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Epidemik Fazlar, Sınırlama ve Etkiyi Azaltma",
        "content": "Bu kontrol noktasında salgın fazlarını ve fazlara özgü stratejik müdahaleleri özetliyoruz:\n\n- **Faz 1 (Giriş):** Patojenin topluma sızması → Bekleme ve Öngörü (risk sürücülerinin analizi).\n- **Faz 2 (Lokal Yayılım):** Sınırlı kümelenmeler → Erken Teşhis ve Sınırlama (Containment).\n- **Sınırlama Kuralı:** İlk vaka teşhis edildiği anda başlar; patojen tam tanımlanmasa bile beklenmez.\n- **Filyasyon:** İndeks vakanın temaslılarının taranması ve bulaş zincirinin kırılması.\n- **Faz 3 (Amplifikasyon):** Katlanarak büyüme ve toplum içi yaygın bulaş → Kontrol ve Etkiyi Azaltma (Mitigation).\n- **Eğriyi Düzleştirme:** Farmakolojik olmayan müdahalelerle (NPI) hasta yükünü zamana yayarak yoğun bakımların çökmesini önleme.\n- **Faz 4 (Azalma):** Duyarlı havuzun tükenmesiyle sönümlenme → Eliminasyon / Eradikasyon.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Salgın sürecinin evreleri ve uygulanan halk sağlığı müdahaleleri eşleştirmelerinden hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Faz 2 (Lokal yayılım) -> Erken teşhis ve sınırlama (containment)", "explanation": "A seçeneği DOĞRUDUR: İkinci fazda sınırlama ve erken teşhis uygulanır."},
                    {"key": "B", "text": "Faz 1 (Giriş) -> Kitlesel sokağa çıkma yasakları", "explanation": "B seçeneği yanlıştır: Faz 1'de bekleme ve öngörü vardır."},
                    {"key": "C", "text": "Faz 3 (Amplifikasyon) -> Bekleme ve hiçbir müdahale yapmama", "explanation": "C seçeneği yanlıştır: Faz 3'te en agresif mitigation uygulanır."},
                    {"key": "D", "text": "Faz 4 (Azalma) -> Sınırlama başlatılması", "explanation": "D seçeneği yanlıştır: Sınırlama faz 2'de başlar."},
                    {"key": "E", "text": "Faz 2 (Lokal yayılım) -> Küresel eradikasyon ilanı", "explanation": "E seçeneği yanlıştır: Eradikasyon faz 4 sonrasıdır."}
                ],
                "A"
            ),
            make_cloze(
                "Salgının katlanarak büyüdüğü amplifikasyon döneminde sağlık sisteminin çökmesini engellemek için uygulanan stratejiye etkiyi azaltma denir.",
                "etkiyi azaltma",
                "Mitigation stratejisinin Türkçe karşılığı"
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-14-s30",
        "title": "Faz 4: Azalma ve Sönümlenme Dinamikleri",
        "content": "Her salgın dalgası eninde sonunda bir tepe noktasına (pik) ulaşır ve ardından dördüncü faza, yani **azalma ve sönümlenme evresine** girer:\n\n- **Neden Söner?**\n  1. Toplumdaki duyarlı (enfekte olabilecek) insan havuzunun tükenmesi (hastalığı geçirenlerin antikor kazanması).\n  2. Etkin aşılama ile toplumsal bağışıklık duvarının örülmesi.\n  3. İzolasyon, maske ve kısıtlamaların virüsün yeni insan bulmasını imkansız kılması.\n- **Kritik Yanılgı (Erken Rehavet):** Vaka sayıları düşmeye başladığında önlemler aceleyle terk edilirse, kalan duyarlı popülasyonda virüs yeniden alevlenir ve **ikinci/üçüncü dalgalar** başlar (1918 İspanyol gribindeki ölümcül ikinci dalga gibi).\n- **Hedef:** Bu evrede rehavete kapılmadan sürveyansı sürdürerek hastalığı bölgesel olarak silmek (eliminasyon) veya tamamen yok etmektir (eradikasyon).",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Disiplinli Sönümlendirme vs Erken Rehavet",
                "Disiplinli Sönümlendirme (Faz 4)",
                "Önlemler kademeli gevşetilir, sürveyans sürdürülür; salgın tamamen sıfırlanır.",
                "Erken Rehavet ve Önlemleri Bırakma",
                "Kalan duyarlı bireyler hızla enfekte olur; çok daha yıkıcı ikinci dalga patlak verir."
            ),
            make_recall(
                "Salgın eğrisinin inişe geçtiği dördüncü fazda halkın ve yöneticilerin önlemleri erkenden gevşetmesi sonucu ortaya çıkan yeni vaka patlamasına ne ad verilir?",
                "İkinci dalgadır (second wave / nüks salgın).",
                "Rehavet sonucu patlayan ikincil salgın dalgası"
            )
        ]
    })

    return slides
