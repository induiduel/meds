# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-14-s31",
        "title": "Eliminasyon (Bölgesel Yok Etme) Tanımı ve Kriterleri",
        "content": "Bulaşıcı hastalıklarla mücadelede 'eliminasyon' ve 'eradikasyon' kavramları halk sağlığının en temel iki ayrı başarı basamağıdır:\n\n- **Eliminasyon Tanımı (Sınav Spotu):** Bir enfeksiyon hastalığının, kasıtlı ve planlı halk sağlığı önlemleri (aşılama, vektör kontrolü) sonucunda **tanımlı belirli bir coğrafi bölgede (ülke veya kıta çapında)** insidansının sıfıra indirilmesi ve **artık büyük bir halk sağlığı sorunu olmaktan çıkarılmasıdır**.\n- **Kritik Kural:** Patojen dünyanın başka bölgelerinde varlığını sürdürmektedir! Bu nedenle eliminasyona ulaşmış bir ülkede **sürveyans ve aşılama/kontrol önlemleri KESİNTİSİZ SÜRDÜRÜLMELİDİR**.\n- **Risk:** Önlemler bırakılırsa dışarıdan gelen (ithal/imported) tek bir vaka duyarlı nüfusta yeniden salgın başlatabilir.\n- **Örnek:** Türkiye'de ve Amerika kıtasında yerli kızamık ve çocuk felcinin elimine edilmiş olması.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Eliminasyon vs Eradikasyon Kapsam Farkı",
                "Eliminasyon (Bölgesel Başarı)",
                "Belirli bir coğrafyada (ör. bir ülkede) vakaların sıfırlanmasıdır; dış tehdit sürdüğü için aşı bırakılamaz.",
                "Eradikasyon (Küresel Zafer)",
                "Patojenin tüm dünyada yeryüzünden tamamen silinmesidir; artık aşı ve kontrol önlemlerine gerek kalmaz."
            ),
            make_cloze(
                "Bir hastalığın belirli bir coğrafi bölgede halk sağlığı sorunu olmaktan çıkarılmasına eliminasyon denir ve kontrol önlemleri sürdürülmelidir.",
                "eliminasyon",
                "Bölgesel vaka sıfırlanması terimi"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-14-s32",
        "title": "Eradikasyon (Küresel Yok Oluş) Tanımı ve Şartları",
        "content": "Eradikasyon, halk sağlığı biliminin ulaşabileceği en üst, en kutsal ve nihai zirvedir:\n\n- **Eradikasyon Tanımı (Sınav Spotu):** Bir patojenin yol açtığı enfeksiyonun görülme sıklığının **dünya çapında kalıcı olarak sıfıra indirilmesidir**.\n- **Kalıcı Zafer:** Eradikasyon sağlandığında patojen doğada tamamen yok olmuştur. Bu nedenle, artık **hiçbir ülkede sürveyans, karantina veya rutin aşılama yapılmasına GEREK KALMAZ!**\n- **Olağanüstü Güçlük:** Eradikasyon insanlık tarihinde başarılması en zor halk sağlığı hedefidir ve bugüne kadar insan hekimliğinde **yalnızca tek bir hastalık için** başarılabilmiştir: **Çiçek Hastalığı (Smallpox)**.\n- **Veteriner Başarısı:** Hayvan hekimliğinde ise sığır vebası (Rinderpest) 2011 yılında eradike edilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Özellik", "Eliminasyon (Bölgesel)", "Eradikasyon (Küresel)"],
                [
                    [
                        {"text": "Coğrafi Kapsam", "isMasked": False, "hint": ""},
                        {"text": "Tanımlı bir bölge veya ülke ile sınırlı", "isMasked": False, "hint": ""},
                        {"text": "Tüm dünya gezegeni çapında küresel", "isMasked": True, "hint": "Gezegen genelindeki etki"}
                    ],
                    [
                        {"text": "Kontrol Önlemleri (Aşı)", "isMasked": False, "hint": ""},
                        {"text": "Yeniden girişi önlemek için zorunlu sürdürülür", "isMasked": True, "hint": "Aşının bırakılamaması kuralı"},
                        {"text": "Artık aşı ve müdahaleye gerek kalmaz (bırakılır)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Başarı Örneği", "isMasked": False, "hint": ""},
                        {"text": "Türkiye'de Polio ve Maternal Tetanoz", "isMasked": False, "hint": ""},
                        {"text": "Çiçek Hastalığı (Variola - 1980)", "isMasked": True, "hint": "Dünyadan silinen tek insan hastalığı"}
                    ]
                ]
            ),
            make_recall(
                "Bir bulaşıcı hastalığın dünya çapında görülme sıklığının kalıcı olarak sıfırlanmasına ve artık rutin aşılamaya gerek kalmamasına ne ad verilir?",
                "Eradikasyondur (küresel kökünün kurutulması).",
                "Dünya çapında yok oluş terimi"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-14-s33",
        "title": "Bir Patojenin Eradike Edilebilirliğini Belirleyen Biyolojik Şartlar",
        "content": "Her bulaşıcı hastalık eradike edilemez. Bir patojenin dünyadan silinebilmesi için doğanın çok katı biyolojik şartları sağlaması gerekir:\n\n1. **Tek Rezervuarın İnsan Olması (Zorunlu Şart):** Patojenin hiçbir hayvan rezervuarı ve çevresel odağı (toprak, su) bulunmamalıdır. Eğer virüs kuşlarda, yarasalarda veya kemirgenlerde yaşıyorsa insanda sıfırlansa bile hayvandan tekrar bulaşır!\n2. **Asemptomatik Taşıyıcılığın Olmaması:** Hastalanan her bireyin belirgin klinik bulgu vermesi gerekir; gizli taşıyıcılar sürveyanstan kaçar.\n3. **Etkin, Güvenli ve Tek Dozluk/Kolay Bir Aşının Varlığı:** Yaşam boyu kalıcı bağışıklık sağlayan, soğuk zincire dayanıklı bir aşı şarttır.\n4. **Mevsimsel Değil Sabit Antijenik Yapı:** İnfluenza gibi sürekli mutasyonla antijen değiştirmemelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Eradike Edilebilir Patojen vs Edilemez Patojen",
                "Eradike Edilebilir (Ör. Çiçek Virüsü, Polio)",
                "Yalnızca insanda yaşar; hayvan rezervuarı yoktur; etkin aşı kalıcı koruma sağlar.",
                "Eradike Edilemez (Ör. İnfluenza, Kuduz, Tetanoz)",
                "Hayvan rezervuarları geniştir; toprakta spor oluşturur veya sürekli antijenik mutasyon geçirir."
            ),
            make_quiz(
                "Aşağıdakilerden hangisi bir bulaşıcı hastalığın küresel olarak eradike edilebilmesi için gereken zorunlu biyolojik kriterlerden biri DEĞİLDİR?",
                [
                    {"key": "A", "text": "Patojenin geniş bir vahşi hayvan rezervuar havuzuna sahip olması", "explanation": "A seçeneği DOĞRUDUR (aranan yanlıştır): Hayvan rezervuarı olan hastalıklar eradike edilemez; yalnızca insan konağı olanlar eradike edilebilir."},
                    {"key": "B", "text": "Hastalığın tek doğal rezervuarının insan olması", "explanation": "B seçeneği zorunlu temel şarttır."},
                    {"key": "C", "text": "Etkin, güvenli ve uzun süreli bağışıklık sağlayan bir aşının bulunması", "explanation": "C seçeneği zorunlu temel şarttır."},
                    {"key": "D", "text": "Vakaların klinik olarak kolayca tanınabilmesi (belirgin semptomlar)", "explanation": "D seçeneği sürveyans için temel şarttır."},
                    {"key": "E", "text": "Kronik asemptomatik taşıyıcılık durumunun bulunmaması", "explanation": "E seçeneği bulaşın gizlenmemesi için temel şarttır."}
                ],
                "A"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-14-s34",
        "title": "Tarihin En Büyük Zaferi: Çiçek Hastalığının Eradikasyonu (1980)",
        "content": "Çiçek hastalığı (Variola virüsü), insanlık tarihi boyunca yüz milyonlarca insanın yüzünü körleştiren, sakat bırakan ve öldüren en acımasız veba idi:\n\n- **Biyolojik Avantajlar:** Çiçek virüsünün hiçbir hayvan rezervuarı yoktu; taşıyıcılık yoktu (her vaka belirgin püstüller dökerdi) ve Edward Jenner'ın geliştirdiği aşı ömür boyu koruyordu.\n- **Stratejik Deha (Halka Aşılama - Ring Vaccination):** Tüm dünya nüfusunu aşılamak yerine, vaka çıkan köyün etrafındaki temaslı çemberi (halka) aşılandı; virüs kaçacak insan bulamadı.\n- **Son Vaka ve Resmi İlan (Sınav Spotu):** Dünyadaki son doğal vaka 1977'de Somali'de (Ali Maow Maalin) görüldü. 1980 yılında Dünya Sağlık Asamblesi **çiçek hastalığının dünya üzerinden tamamen silindiğini (eradike edildiğini)** resmen ilan etti.\n- **Sonuç:** O tarihten bu yana çiçek aşısı yapılmamaktadır!",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Çiçek Hastalığının Eradikasyon Zafer Adımları",
                [
                    "1. Jenner'ın Aşısı: İnek çiçeği virüsüyle güvenli ve kalıcı bağışıklık sağlayan aşı geliştirildi.",
                    "2. DSÖ Küresel Seferi (1967): Tüm ülkeleri kapsayan koordineli sürveyans ağı kuruldu.",
                    "3. Halka Aşılama Stratejisi: Vaka görülen odakların çevresindeki tüm temaslılar kordonla aşılandı.",
                    "4. 1980 Resmi Eradikasyon İlanı: Doğada son vaka sıfırlandı; aşı uygulaması tüm dünyada sonlandırıldı."
                ]
            ),
            make_cloze(
                "İnsanlık tarihinde küresel olarak başarıyla eradike edilen ve 1980 yılında dünya üzerinden silindiği ilan edilen tek hastalık çiçek hastalığıdır.",
                "çiçek hastalığı",
                "Variola virüsünün yol açtığı eradike edilmiş hastalık"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-14-s35",
        "title": "Eradikasyonun Eşiğindeki Hastalıklar: Polio ve Gine Solucanı",
        "content": "Günümüzde insanlık iki hastalığı daha çiçek hastalığı gibi yeryüzünden silmenin eşiğine gelmiştir:\n\n1. **Poliomiyelit (Çocuk Felci):**\n   - Küresel Polio Eradikasyon Girişimi (1988'den beri) sayesinde vakalar %99.9 oranında azaltıldı.\n   - Tip 2 ve Tip 3 vahşi poliovirüsler tamamen eradike edildi. Günümüzde Tip 1 vahşi virüs yalnızca savaş ve güvensizlik altındaki **Afganistan ve Pakistan'da** sınırlı ceplerde kalmıştır.\n2. **Drakunkuliyazis (Gine Solucanı):**\n   - Kirli su içilmesiyle bulaşan parazitik bir nematoddur.\n   - Aşısı veya ilacı yoktur; yalnızca su filtreleri ve su kaynaklarının korunmasıyla vakalar yılda 3.5 milyondan **15'in altına indirilmiştir**; tarihin aşı olmadan eradike edilen ilk hastalığı olmaya adaydır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Polio (Çocuk Felci) vs Gine Solucanı Eradikasyon Yöntemi",
                "Poliomiyelit Eradikasyonu",
                "Canlı oral (Sabin) ve inaktif (Salk) aşılarla yürütülen küresel kitlesel bağışıklama başarısıdır.",
                "Gine Solucanı (Drakunkuliyazis)",
                "Aşısı ve ilacı yoktur; yalnızca naylon su filtreleri ve su hijyeni eğitimiyle sıfırlanmaktadır."
            ),
            make_recall(
                "Günümüzde vahşi suşu yalnızca Afganistan ve Pakistan'da sınırlı kalan ve küresel eradikasyonunun eşiğine gelinen enteroviral felç hastalığı nedir?",
                "Poliomiyelittir (Çocuk Felci / Vahşi Poliovirüs Tip 1).",
                "Aşıyla eradike edilmek üzere olan çocukluk felci hastalığı"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-14-s36",
        "title": "Neden Her Patojen Eradike Edilemez? Biyolojik Engeller",
        "content": "Modern tıbbın olağanüstü gücüne rağmen birçok ölümcül patojeni dünyadan silmek biyolojik doğaları gereği imkansızdır:\n\n- **Geniş Hayvan Rezervuarı:** Kuduz virüsü yarasalar ve etoburlarda; İnfluenza su kuşları ve domuzlarda; Sarı humma orman maymunlarında sürekli döngü halindedir. İnsanlardaki tüm vakaları sıfırlasanız bile hayvandan insana sıçrama her an tekrar başlar.\n- **Çevresel Rezervuar:** Tetanoz basili (**Clostridium tetani**) ve şarbon basili toprakta onlarca yıl canlı kalan sporlar oluşturur; dünyadaki tüm toprakları sterilize etmek imkansızdır!\n- **Antijenik Değişkenlik:** HIV ve Hepatit C gibi virüsler vücut içinde bile dakikalar içinde mutasyon geçirerek bağışıklıktan kaçar; etkin aşı geliştirilemez.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Hastalık", "Eradike Edilememe Nedeni", "Uygulanabilir Halk Sağlığı Hedefi"],
                [
                    [
                        {"text": "Tetanoz", "isMasked": False, "hint": ""},
                        {"text": "Toprakta spor oluşturması (çevresel rezervuar)", "isMasked": True, "hint": "Topraktaki spor varlığı"},
                        {"text": "Maternal ve neonatal eliminasyon / bireysel aşı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kuduz", "isMasked": True, "hint": "Yarasa ve tilki kaynaklı ölümcül ensefalit"},
                        {"text": "Yarasa, tilki, kurt gibi yaban hayvan rezervuarları", "isMasked": False, "hint": ""},
                        {"text": "Köpek aşılaması ve temas sonrası profilaksi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "İnfluenza (Grip)", "isMasked": False, "hint": ""},
                        {"text": "Sürekli antijenik sapma/kırılma ve göçmen kuş rezervuarı", "isMasked": True, "hint": "Sürekli mutasyon ve kuş rezervuarı"},
                        {"text": "Yıllık mevsimsel aşı ve sürveyans kontrolü", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Tetanoz hastalığının dünyadan asla eradike edilememesinin ve yalnızca bireysel aşılamayla korunulabilmesinin temel biyolojik gerekçesi nedir?",
                "Clostridium tetani sporlarının toprakta doğal çevresel rezervuara sahip olmasıdır.",
                "Topraktaki spor varlığı gerekçesi"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-14-s37",
        "title": "Kızamık ve Kızamıkçık Eliminasyonu: Aşı Karşıtlığı Tehdidi",
        "content": "Kızamık (Measles), temel üreme katsayısı (R0 = 12-18) en yüksek olan, havadan son derece kolay bulaşan bir virüstür:\n\n- **Yüksek Sürü Bağışıklığı Eşiği:** Kızamık bulaşını durdurabilmek için toplumun **en az %95'inin iki doz aşı ile bağışık olması şarttır!**\n- **Aşı Karşıtlığı ve Tereddüt:** Bilim dışı iddialar ve dezenformasyon nedeniyle aşılama oranları %90'ın altına düştüğünde, eliminasyona ulaşmış gelişmiş ülkelerde dahi kızamık salgınları hortlamaktadır (Avrupa ve ABD salgınları).\n- **Subakut Sklerozan Panensefalit (SSPE):** Kızamık geçiren çocuklarda yıllar sonra ortaya çıkan, beyinde ilerleyici demans ve ölümle sonuçlanan korkunç bir komplikasyondur; tek koruyucu aşıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "%95 Aşılama Kapsayıcılığı vs %85'e Düşüş",
                "%95 ve Üzeri Aşılama",
                "Sürü bağışıklığı duvarı tamdır; dışarıdan vaka gelse bile salgın başlamaz; eliminasyon korunur.",
                "%85'e Gerileyen Aşılama (Aşı Tereddütü)",
                "Duyarlı cepler birikir; tek bir kızamıklı hasta kreş ve okullarda yüzlerce çocuğu enfekte eder."
            ),
            make_cloze(
                "Kızamık hastalığının toplumda yayılmasını engellemek ve eliminasyonu korumak için gereken asgari aşı kapsayıcılık oranı yüzde doksan beştir.",
                "yüzde doksan beş",
                "Kızamık için gereken minimum sürü bağışıklığı yüzdesi"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-14-s38",
        "title": "Eliminasyon Sonrası Aşama: Sürveyans Neden Asla Bırakılamaz?",
        "content": "Halk sağlığı yöneticilerinin en sık düştüğü ölümcül tuzak, bir hastalığı elimine ettikten sonra rehavete kapılıp bütçe ve sürveyansı kesmeleridir:\n\n- **İthal Vaka Tehdidi (Importation):** Bir ülke kendi sınırları içinde polio veya kızamığı sıfırlamış olsa bile, komşu ülkede veya dünyanın başka bir ucunda hastalık devam ediyorsa risk sıfırlanmamıştır.\n- **Aşılamayı Bırakmanın Bedeli:** Aşılamayı durdurursanız doğan her yeni bebek 'duyarlı' olarak büyür. 10 yıl sonra toplumun %20'si savunmasız kalır. Dışarıdan uçakla gelen tek bir vaka felaketi tetikler.\n- **Sürveyans Nöbeti:** Akut flask paralizi (AFP) sürveyansı polio için, döküntülü hastalık sürveyansı kızamık için eliminasyon sonrasında da harfiyen sürdürülmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Bir ülkede çocuk felci (polio) vakaları 20 yıldır hiç görülmemektedir (bölgesel eliminasyon sağlanmıştır). Sağlık Bakanlığı bütçe komisyonunda bir yetkili 'Hastalık bitti, artık polio aşı bütçesini kesip aşılamayı durduralım' önerisinde bulunuyor.",
                "Bir halk sağlığı uzmanı olarak bu öneriye karşı verilecek en doğru epidemiyolojik yanıt nedir?",
                [
                    {
                        "text": "Kesinlikle reddedilmelidir; küresel eradikasyon sağlanmadığı sürece dışarıdan virüs girişi riski vardır ve aşılama durdurulursa doğan yeni nesiller savunmasız kalarak salgın patlar.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Eliminasyon bölgeseldir; dünya genelinde virüs yok edilmeden (eradikasyon olmadan) aşı asla bırakılamaz."
                    },
                    {
                        "text": "Öneri kabul edilmeli ve aşı derhal takvimden çıkarılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Aşısız bir nesil büyür ve ithal bir vaka kitlesel felce yol açar."
                    },
                    {
                        "text": "Yalnızca yurt dışına çıkacak yetişkinlere aşı yapılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Çocukluk çağı temel bağışıklaması durdurulamaz."
                    }
                ]
            ),
            make_recall(
                "Bir ülkede çocuk felci eliminasyonunun sürdüğünü kanıtlamak için 15 yaş altı ani gelişen gevşek felçli her çocuğun incelendiği zorunlu sürveyans protokolüne ne ad verilir?",
                "Akut Flask Paralizi (AFP) sürveyansıdır.",
                "Polio sürveyansının altın standart göstergesi"
            )
        ]
    })

    # Slide 39
    slides.append({
        "id": "k1-14-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Eliminasyon vs Eradikasyon ve Başarılı Örnekler",
        "content": "Bu kontrol noktasında bulaşıcı hastalıklarla mücadelenin en üst hedefleri olan eliminasyon ve eradikasyon dinamiklerini pekiştiriyoruz:\n\n- **Eliminasyon:** Belirli bir coğrafi bölgede vakaların sıfırlanması; dış tehdit sürdüğü için aşılama ve kontrol önlemleri zorunlu olarak devam eder.\n- **Eradikasyon:** Patojenin tüm dünyadan kalıcı olarak silinmesi; doğada virüs kalmadığı için aşı ve kontrol önlemleri sonlandırılır.\n- **Tarihin Tek Örneği:** Çiçek hastalığı (Variola, 1980'de eradike edildi; halka aşılama yöntemiyle başarıldı).\n- **Eradikasyon Şartları:** Tek rezervuar insan olmalı, hayvan/toprak rezervuarı olmamalı, asemptomatik taşıyıcılık bulunmamalı, etkin koruyucu aşı olmalı.\n- **Eradike Edilemeyenler:** Kuduz (hayvan rezervuarı), tetanoz (toprak sporu), grip (sürekli mutasyon/kuşlar).\n- **Eşiğindekiler:** Polio (çocuk felci) ve Gine solucanı (Drakunkuliyazis).",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Eliminasyon ve eradikasyon kavramları arasındaki en temel stratejik fark aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Eliminasyonda bölgesel vaka sıfırlanır ancak aşı sürdürülür; eradikasyonda ise küresel yok oluş sağlandığı için aşılamaya gerek kalmaz", "explanation": "A seçeneği DOĞRUDUR: Eliminasyonda aşı devam eder, eradikasyonda aşı sonlandırılır."},
                    {"key": "B", "text": "Eliminasyon tüm dünyada, eradikasyon tek bir köyde geçerlidir", "explanation": "B seçeneği yanlıştır: Coğrafi kapsam tam tersidir."},
                    {"key": "C", "text": "Eliminasyon yalnızca hayvan hastalıklarında, eradikasyon insanlarda kullanılır", "explanation": "C seçeneği yanlıştır: Her iki kavram da insanlar için kullanılır."},
                    {"key": "D", "text": "Eradikasyon sağlandıktan sonra karantina önlemleri iki katına çıkarılır", "explanation": "D seçeneği yanlıştır: Patojen kalmadığı için karantina gereksizdir."},
                    {"key": "E", "text": "Eliminasyon aşıyla, eradikasyon yalnızca antibiyotikle başarılır", "explanation": "E seçeneği yanlıştır: Eradikasyon aşı ve halk sağlığı müdahaleleriyle sağlanır."}
                ],
                "A"
            ),
            make_cloze(
                "Dünya Sağlık Örgütü tarafından 1980 yılında dünya üzerinden tamamen eradike edildiği resmen ilan edilen tek insan hastalığı çiçek hastalığıdır.",
                "çiçek hastalığı",
                "Eradike edilmiş tek insan enfeksiyonu"
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-14-s40",
        "title": "Yok Edilme (Extinction) Kavramı: Laboratuvar Stoklarının da İmhası",
        "content": "Eradikasyonun da ötesinde teorik ve pratik bir son aşama mevcuttur:\n\n- **Extinction (Yok Edilme / Neslinin Tüketilmesi):** Patojenin doğada canlı vaka yapmamasının yanı sıra, dünya üzerindeki tüm araştırma merkezleri ve biyolojik silah **laboratuvarlarındaki dondurulmuş suşlarının da tamamen imha edilmesidir**.\n- **Çiçek Virüsü İkilemi:** Çiçek hastalığı 1980'de doğadan silinmiştir (eradike edilmiştir) ancak henüz 'extinct' değildir!\n- **Kalan İki Stok:** Çiçek virüsünün bilinen son resmi örnekleri yüksek güvenlikli (BSL-4) iki merkezde muhafaza edilmektedir:\n  1. CDC (Atlanta, ABD)\n  2. VECTOR Enstitüsü (Koltsovo, Rusya)\n- **Biyoterörizm Riski:** Bu stokların imha edilip edilmemesi küresel tıp politikasında yıllardır süregelen büyük bir etik ve güvenlik tartışmasıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Eradikasyon vs Extinction (Yok Edilme)",
                "Eradikasyon (Çiçek Hastalığı 1980)",
                "Doğada hiçbir canlı vaka kalmamıştır; ancak laboratuvar dondurucularında suşlar saklanır.",
                "Extinction (Tam Yok Edilme)",
                "Laboratuvar stokları dahil virüsün yeryüzündeki son genetik kopyası da tamamen imha edilir."
            ),
            make_recall(
                "Bir patojenin doğadaki vakalarının sıfırlanmasının ötesinde, dünyadaki tüm araştırma laboratuvarlarındaki canlı suşlarının da yok edilmesine ne ad verilir?",
                "Yok edilmedir (extinction / neslinin tamamen tüketilmesi).",
                "Biyolojik olarak tüm kopyaların silinmesi"
            )
        ]
    })

    return slides
