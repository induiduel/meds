# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-11-s81",
        "title": "Üriner Obstrüksiyonda Acil Tedavi İlkeleri ve Triyaj",
        "content": "Üriner sistem obstrüksiyonunda tedavi planı obstrüksiyonun anatomik seviyesine, derecesine ve altta yatan etiyolojik nedene göre şekillendirilir. Ancak klinik pratikte iki kardinal durum tartışmasız en yüksek öncelikli **acil tedavi** gerektirir:\n\n1. **Komplet Bilateral Obstrüksiyon veya Soliter Böbrekte Tam Tıkanıklık:** Bu tablolarda idrar üretimi tamamen durur (anüri), saatler içinde fatal hiperkalemi, asidoz ve akciğer ödemi gelişir.\n2. **Enfekte Obstrüksiyon (Piyonefroz / Üroseptik Şok):** Tıkanmış sistemin arkasındaki enfeksiyon dakikalar içinde dolaşıma sızar.\n\nHer iki acil tabloda temel prensip: **'Önce obstrüksiyon ortadan kaldırılır ve toplayıcı sistem acilen drene edilir; etiyolojiye yönelik ayrıntılı araştırmalar ve ileri tedavi planı drenaj sağlandıktan sonraya bırakılır.'**",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Komplet bilateral veya soliter böbrekte anüriye yol açan obstrüksiyonlar acil drenaj ve dekompresyon gerektirir.",
                "acil drenaj",
                "Tıkanıklığı anında tahliye etme süreci"
            ),
            make_quiz(
                "Üriner obstrüksiyonda acil drenaj endikasyonları ve tedavi ilkeleriyle ilgili hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Önce obstrüksiyon dekomprese edilir, etiyolojik inceleme ve kalıcı tedavi sonraya bırakılır.", "explanation": "A seçeneği DOĞRUDUR: Hayati acillerde ilk adım böbreği hızla rahatlatmaktır."},
                    {"key": "B", "text": "Anürik hastada dekompresyondan önce 3 gün boyunca tüm genetik testler tamamlanmalıdır.", "explanation": "B seçeneği yanlıştır: Hasta üremi ve hiperkalemiden kaybedilir."},
                    {"key": "C", "text": "Soliter böbrek tıkanıklığı 2 hafta boyunca konservatif izlenmelidir.", "explanation": "C seçeneği yanlıştır: Soliter böbrek tam tıkanıklığı acil girişim gerektirir."},
                    {"key": "D", "text": "Enfekte obstrüksiyonda kateter takılması kontrendikedir.", "explanation": "D seçeneği yanlıştır: Acil drenaj hayat kurtarır."},
                    {"key": "E", "text": "Bilateral obstrüksiyonda ilk tercih daima genel anestezi altında açık ameliyattır.", "explanation": "E seçeneği yanlıştır: İlk tercih minimal invaziv kateterizasyondur."}
                ],
                "A"
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-11-s82",
        "title": "İnfravezikal Acil Dekompresyon: Foley Kateter ve Sistostomi",
        "content": "Alt üriner sistem düzeyindeki akut tıkanıklıklarda (örneğin BPH'ya bağlı akut glob vezikale tablosunda) ilk tercih edilen girişim **üretral kateterizasyondur (Foley kateter)**. Steril koşullarda lubrike edilerek uygulanan 16-18 French bir Foley sonda mesaneye ulaştırılarak biriken yüzlerce mililitre idrar hızla tahliye edilir. Ancak bazı durumlarda üretral kateterizasyon imkansız veya kontrendikedir:\n\n- **Üretra Darlığı veya Pelvik Travma:** Kateter üretrada takılıyorsa zorlanmamalıdır (üretra yırtılması ve yalancı pasaj riski).\n- **Akut Bakteriyel Prostatit:** Üretral manipülasyon bakteriyemiyi tetikleyebilir.\n\nBu gibi durumlarda ultrasonografi kılavuzluğunda simfizis pubis üzerinden mesane apeksine perkütan trokar ile girilerek **Suprapubik Sistostomi** tüpü yerleştirilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "İnfravezikal Drenaj Yöntemleri Karşılaştırması",
                "Üretral Foley Kateter",
                "İlk tercih; doğal üretral lümenden hızla mesaneye yerleştirilir.",
                "Suprapubik Sistostomi",
                "Üretra darlığı, travması veya sonda takılamayan olgularda simfizis üzerinden takılır."
            ),
            make_recall(
                "Üretra darlığı veya travması nedeniyle Foley sonda takılamayan akut glob vezikaleli hastada mesaneyi boşaltmak için simfizis üzerinden uygulanan acil işlem nedir?",
                "Suprapubik sistostomidir (suprapubic cystostomy).",
                "Karın alt duvarından mesaneye perkütan drenaj takılması"
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-11-s83",
        "title": "Supravezikal Acil Dekompresyon: Perkütan Nefrostomi ve JJ Stent",
        "content": "Üst üriner sistem (üreter ve böbrek) obstrüksiyonlarında acil idrar drenajı iki ana minimal invaziv yöntemle sağlanır:\n\n1. **Perkütan Nefrostomi (PNS):** Hasta yüzüstü yatırılarak lokal anestezi altında, ultrasonografi ve skopi eşliğinde böbreğin alt pol arka kaliksine iğne ile girilir. Seldinger tekniğiyle kılavuz tel üzerinden toplayıcı sisteme bir drenaj kateteri yerleştirilir. Özellikle enfekte hidronefrozda (piyonefroz), ürosepsiste veya alt üriner sistem anatomisinin sistoskopiye izin vermediği durumlarda **en güvenli ve etkili supravezikal drenaj yoludur**.\n2. **Retrograd Üreteral Double-J (JJ) Stent:** Sistoskopi ile mesaneye girilip üreter orifisinden böbrek pelvisine kadar uzanan iki ucu kıvrık (pigtail) bir stent yerleştirilir. Dışarıya sarkan bir torba olmaması konfor sağlar ancak enfekte püy varlığında ince lümeni tıkanabilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Drenaj Yöntemi", "Giriş Yolu ve Teknik", "Öncelikli Endikasyon"],
                [
                    [
                        {"text": "Perkütan Nefrostomi (PNS)", "isMasked": False, "hint": ""},
                        {"text": "Böğürden kalikse perkütan giriş", "isMasked": True, "hint": "Lokal anesteziyle ciltten toplayıcı sisteme iğneyle giriş"},
                        {"text": "Piyonefroz, septik şok, başarısız JJ stent", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Retrograd Double-J Stent", "isMasked": False, "hint": ""},
                        {"text": "Sistoskopik yolla üreter lümeninden yukarı", "isMasked": True, "hint": "Endoskopik antegrad/retrograd iç stentleme"},
                        {"text": "Steril taş tıkanıklıkları, üreteral darlıklar", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Piyonefroz ve üroseptik şok tablosundaki bir hastada üst üriner sistemi hızla drene etmede en güvenli yöntem perkütan nefrostomidir.",
                "perkütan nefrostomidir",
                "Cilt yoluyla doğrudan böbrek kaliksine takılan drenaj tüpü"
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-11-s84",
        "title": "Postobstrüktif Diürez (POD): Tanım ve Risk Faktörleri",
        "content": "Bilateral komplet obstrüksiyon veya soliter böbrekteki tam obstrüksiyon kateter veya cerrahiyle giderildikten hemen sonra saatte 200 ml'den (veya 24 saatte 3-4 litreden) fazla idrar çıkarılması durumuna **Postobstrüktif Diürez (POD)** denir. Tıkanıklık aniden ortadan kalktığında böbrekler adeta bir baraj kapağının açılması gibi masif miktarda su ve elektroliti dışarı pompalamaya başlar. Postobstrüktif diürez gelişimi için majör risk faktörleri şunlardır:\n\n1. Obstrüksiyonun iki taraflı (bilateral) olması veya soliter böbreği etkilemesi,\n2. Tıkanıklık öncesinde hastada masif periferik ödem, kilo artışı ve hipervolemi bulunması,\n3. Serum üre ve kreatinin değerlerinin belirgin derecede yükselmiş (derin azotemi) olması,\n4. Tıkanıklığın uzun sürmüş olmasıdır. Tek taraflı obstrüksiyonların açılmasından sonra sağlam böbrek dengeyi koruduğu için POD görülmez.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Postobstrüktif Diürez Ortaya Çıkış Dinamiği",
                [
                    "1. Ağır Azotemi ve Hipervolemi: Bilateral tıkanıklıkla vücutta masif üre ve su birikmesi",
                    "2. Acil Dekompresyon: Kateter ile idrar yolu direncinin sıfırlanması",
                    "3. Masif Solüt Atılımı: Birikmiş ürenin tübüllere hücum ederek ozmotik diürez başlatması",
                    "4. Yüksek Debili Poliüri: Saatte 200 ml üzerinde kontrolsüz idrar çıkışı"
                ]
            ),
            make_recall(
                "Bilateral veya soliter böbrek obstrüksiyonu açıldıktan sonra ortaya çıkan belirgin poliüri tablosuna ne ad verilir?",
                "Postobstrüktif diürezdir (POD).",
                "Tıkanıklık sonrası aşırı idrar çıkışı fenomeni"
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-11-s85",
        "title": "Postobstrüktif Diürez Fizyopatolojisi: Üre ve Solüt Diürezi",
        "content": "Postobstrüktif diürezin arkasında üç ayrı fizyopatolojik mekanizma birlikte rol oynar:\n\n1. **Ozmotik (Solüt) Diürezi:** Obstrüksiyon süresince kanda aşırı biriken üre, kreatinin ve sodyum dekompresyonla birlikte hızla glomerüllerden filtre edilir. Tübül lümenindeki aşırı yüksek üre konsantrasyonu güçlü bir ozmotik çekim kuvveti oluşturur; suyun tübüllerden geri emilmesini engelleyerek devasa bir ozmotik diürez başlatır.\n2. **Hipervoleminin Giderilmesi:** Vücutta birikmiş olan aşırı ekstraselüler sıvının atılması amacıyla atriyal natriüretik peptit (ANP) salınımı artar; bu da natriürezi uyarır.\n3. **Tübüler ADH Duyarsızlığı:** Daha önce öğrendiğimiz gibi, toplayıcı kanallarda Akuaporin-2 ekspresyonu baskılanmıştır. Medüller hipertonisite de yıkandığı için toplayıcı tübüller lümendeki suyu geri çekemez ve su kontrolsüzce idrara dökülür.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Fizyopatolojik Bileşen", "Temel Moleküler Sebep", "Sonuç"],
                [
                    [
                        {"text": "Ozmotik Solüt Yükü", "isMasked": False, "hint": ""},
                        {"text": "Aşırı filtre edilen ürenin lümende su tutması", "isMasked": True, "hint": "Kanda biriken temel azotlu solütün ozmotik etkisi"},
                        {"text": "Güçlü ozmotik diürez", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Tübüler Yanıtsızlık", "isMasked": False, "hint": ""},
                        {"text": "Toplayıcı kanallarda AQP2 eksikliği ve ADH direnci", "isMasked": True, "hint": "Su kanallarının membrana gidememesi"},
                        {"text": "Suyun geri emilememesi (nefrojenik DI)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Medüller Yıkanma", "isMasked": False, "hint": ""},
                        {"text": "Henle çıkan kolunda gradyent kaybı", "isMasked": True, "hint": "Papilladaki ozmotik konsantrasyonun silinmesi"},
                        {"text": "Konsantrasyon kapasitesinin sıfırlanması", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Postobstrüktif diürezin en önemli solüt bileşeni, kanda birikip filtrasyona uğrayarak ozmotik diürez yapan üre molekülüdür.",
                "üre molekülüdür",
                "Protein yıkımının majör azotlu son ürünü"
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-11-s86",
        "title": "Fizyolojik Solüt Diürezi vs Patolojik Postobstrüktif Diürez",
        "content": "Klinikte postobstrüktif diürez iki farklı seyir gösterir ve bu ayrım hayati önem taşır:\n\n- **Fizyolojik Solüt Diürezi:** Olguların büyük kısmını oluşturur. Vücutta obstrüksiyon boyunca hapsolmuş fazla su, sodyum ve ürenin atılması için organizmanın verdiği son derece sağlıklı ve fizyolojik bir temizlenme tepkisidir. İdrar miktarı birkaç gün içinde üre ve sıvı dengesi sağlandıkça kendiliğinden azalır. Bilinci açık hastada normal susuzluk mekanizması aşırı sıvı kaybını dengeler.\n- **Patolojik Postobstrüktif Diürez:** Nadir fakat ölümcül formdur. Vücuttaki fazla sıvı ve üre tükendiği halde, ağır tübüler hasar ve tam ADH direnci nedeniyle böbrek su ve tuzu tutamaz. Hasta saatte 500-1000 ml idrar çıkarmayı sürdürür; derin hipovolemi, dehidratasyon, hipokalemi, hiponatremi ve hipovolemik şok tablosuna girer. Derhal aktif tıbbi müdahale gerektirir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Fizyolojik ve Patolojik POD Karşılaştırması",
                "Fizyolojik POD (Sık)",
                "Fazla sıvı ve ürenin atılmasıdır, kendini sınırlar; susuzluk mekanizması hastayı korur.",
                "Patolojik POD (Nadir/Tehlikeli)",
                "Tübül hasarı nedeniyle kontrolsüz su ve tuz kaybı sürer; hipovolemik şok ve ölüm riski taşır."
            ),
            make_recall(
                "Bilateral obstrüksiyon açıldıktan sonra vücutta birikmiş aşırı sıvı ve ürenin atılmasını sağlayan ve genellikle kendini sınırlayan normal duruma ne ad verilir?",
                "Fizyolojik postobstrüktif diürez.",
                "Kompansatuar solüt atılım süreci"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-11-s87",
        "title": "Postobstrüktif Diürez Yönetimi: Sıvı Resüsitasyonu ve İzlem",
        "content": "Postobstrüktif diürez izlemindeki en kritik hata tuzağı 'hastanın çıkardığı kadar sıvıyı birebir damardan geri vermektir'. Hastaya çıkardığı idrar kadar (örneğin 100 ml idrara 100 ml IV sıvı) replasman yapılırsa, verilen bu fazla sıvı böbrekler tarafından tekrar atılmaya çalışılır ve hekim kendi eliyle yapay bir 'iatrojenik diürez döngüsü' yaratır. Doğru klinik protokol şudur:\n\n1. Vital bulgular (tansiyon, nabız) ve saatlik idrar debisi yakın takip edilir.\n2. Serum elektrolitleri (sodyum, potasyum, kalsiyum, magnezyum) 4-6 saatte bir kontrol edilir.\n3. Hasta susama hissi varsa ağızdan serbestçe sıvı almalıdır.\n4. İntravenöz sıvı replasmanı gerekiyorsa, hastanın çıkardığı idrar volümünün **%50 ila %70'i oranında** (hipotonik mayi, örneğin %0.45 NaCl) verilerek organizmanın kendi sıvı dengesini kurmasına izin verilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "Bilateral üreter tıkanıklığı açılan bir hastada saatlik idrar miktarı 400 ml olarak ölçülüyor. Nöbetçi asistan hastaya saatte 400 ml IV serum fizyolojik infüzyonu başlatıyor; ancak aradan 24 saat geçmesine rağmen idrar miktarı hiç azalmıyor ve hasta günde 10 litre idrar çıkarmaya devam ediyor.",
                "Bu tablonun uzamasındaki temel klinik hata ve yapılması gereken doğru yaklaşım nedir?",
                [
                    {
                        "text": "Çıkan idrarın birebir replase edilmesi iatrojenik solüt diürezini beslemektedir; IV replasman çıkanın %50-70'ine çekilmeli veya hasta stabilse azaltılmalıdır.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Çıkanın %100'ünü vermek diürezi sonsuz döngüye sokar; replasman %50-70 oranında tutulmalıdır."
                    },
                    {
                        "text": "Verilen sıvı miktarı az gelmiştir, saatlik IV sıvı 1000 ml'ye çıkarılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Sıvıyı artırmak diürez döngüsünü daha da patlatır ve volüm aşırı yüklenmesi yapar."
                    },
                    {
                        "text": "Hastaya derhal yüksek doz furosemid yapılarak idrarı durdurulmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Furosemid diüretiktir, idrarı durdurmaz tam tersine sıvı kaybını ölümcül kılar."
                    }
                ]
            ),
            make_cloze(
                "Postobstrüktif diürez takibinde iatrojenik poliüri döngüsünü kırmak için IV sıvı replasmanı çıkan idrarın yüzde elli ila yetmişi oranında tutulmalıdır.",
                "yüzde elli ila yetmişi",
                "İdrar karşılama yüzdesi aralığı"
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-11-s88",
        "title": "'Ex Vacuo' Hematüri ve Hızlı Dekompresyon Komplikasyonları",
        "content": "Akut komplet infravezikal obstrüksiyonda (glob vezikale) mesane 1 ila 2 litre idrarla aşırı gerilmiş olabilir. Böyle bir hastada Foley kateter takıldığında mesanenin dakikalar içinde tamamen ve birdenbire boşaltılması ciddi komplikasyonlara davetiye çıkarır:\n\n- **Ex Vacuo Hematüri (Vakum Kanaması):** Aşırı gerilmiş olan mesane duvarındaki submukozal venler ve kapillerler yüksek intralüminal basınç altındadır. İdrar aniden boşaltıldığında mesane içi basınç saniyeler içinde sıfıra düşer. Bu ani negatif basınç (vakum etkisi) aşırı gerilmiş ve frajil hale gelmiş submukozal venöz pleksusların ve kapillerlerin yırtılmasına yol açar; mesane lümeni masif kanamayla dolar.\n- **Vazovagal Senkop:** İntraabdominal basıncın aniden düşmesi splanknik alanda kanın göllenmesine ve serebral perfüzyonun geçici azalmasıyla senkopa yol açabilir. Bu nedenle mesane kademeli olarak (örneğin her seferinde 400-500 ml boşaltılıp kateter klemplenerek) dekomprese edilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Hızlı Dekompresyon Riski", "Fizyopatolojik Süreç", "Önleyici Tedbir"],
                [
                    [
                        {"text": "Ex Vacuo Hematüri", "isMasked": False, "hint": ""},
                        {"text": "Ani vakum etkisiyle submukozal kapiller yırtılması", "isMasked": True, "hint": "Basıncın sıfırlanmasıyla oluşan mukozal kanama"},
                        {"text": "Mesaneyi kademeli olarak (400-500 ml'lik porsiyonlarla) boşaltmak", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Vazovagal Hipotansiyon", "isMasked": False, "hint": ""},
                        {"text": "İntraabdominal basınç düşüşüyle venöz göllenme", "isMasked": True, "hint": "Splanknik yatakta kan toplanması"},
                        {"text": "Hastayı yatar pozisyonda tutmak ve yavaş tahliye", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Aşırı dolu bir mesanenin birdenbire hızla boşaltılması sonucu vakum etkisiyle mukozal damarların yırtılmasına bağlı gelişen kanamaya ne ad verilir?",
                "Ex vacuo hematüri (dekompresyon hematürisi).",
                "Boşluk etkisiyle gelişen hematüri terimi"
            )
        ]
    })

    # Slide 89 (CHECKPOINT 9)
    slides.append({
        "id": "k1-11-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Acil Girişimler, Drenaj Yöntemleri ve Postobstrüktif Diürez",
        "content": "Üriner obstrüksiyonda acil drenaj ve postobstrüktif diürezin kilit ilkeleri:\n\n1. **Öncelik:** Bilateral tam obstrüksiyon, soliter böbrek tıkanıklığı ve piyonefroz acil drenaj gerektirir. Önce drenaj sağlanır, etiyolojik tedavi sonraya bırakılır.\n2. **Drenaj Seçimi:** İnfravezikalde Foley (kontrendikasyonda sistostomi); supravezikalde özellikle enfeksiyonda perkütan nefrostomi (PNS) altın standarttır.\n3. **Postobstrüktif Diürez (POD):** Bilateral tıkanıklık açılınca saatte 200 ml üstü poliüri gelişebilir. Üre ozmotik yükü ve toplayıcı kanal ADH direnci ana sebeptir.\n4. **POD Sıvı Kuralı:** Çıkanın %100'ü verilmez! İatrojenik döngüyü önlemek için %50-70 oranında karşılanır.\n5. **Ex Vacuo Hematüri:** Glob vezikale aniden boşaltılırsa vakum etkisiyle kanar; kademeli boşaltılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Postobstrüktif diürez (POD) tablosu ve klinik yönetimiyle ilgili hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "Yalnızca tek taraflı basit üreter taşlarının düşmesinden sonra görülür.", "explanation": "A seçeneği YANLIŞTIR: POD bilateral obstrüksiyon veya soliter böbrek obstrüksiyonu giderildikten sonra görülür; tek taraflıda sağlam böbrek dengelediğinden POD oluşmaz."},
                    {"key": "B", "text": "Birikmiş ürenin başlattığı ozmotik diürez temel mekanizmalardan biridir.", "explanation": "B seçeneği doğrudur: Solüt diürezi esastır."},
                    {"key": "C", "text": "Toplayıcı kanallardaki geçici ADH direnci poliüriye katkı sağlar.", "explanation": "C seçeneği doğrudur: AQP2 eksikliği su kaybını artırır."},
                    {"key": "D", "text": "İntravenöz sıvı replasmanı çıkan idrarın %50-70'i oranında tutulmalıdır.", "explanation": "D seçeneği doğrudur: Fazla sıvı vermek iatrojenik poliüri döngüsü yaratır."},
                    {"key": "E", "text": "Fark edilmezse hasta derin hipovolemi ve elektrolit imbalansına girebilir.", "explanation": "E seçeneği doğrudur: Yakın izlem şarttır."}
                ],
                "A"
            ),
            make_cloze(
                "Glob vezikalede mesanenin aniden bosaltılması vakum etkisiyle ex vacuo hematüriye yol açabilir.",
                "ex vacuo hematüriye",
                "Ani dekompresyon kaynaklı kanama tablosu"
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-11-s90",
        "title": "Erken Elektif Cerrahi Endikasyonları ve Renal Rezervin Korunması",
        "content": "Obstrüktif üropatili bir hastada acil dekompresyon sağlandıktan veya akut tablo yatıştırıldıktan sonra, kalıcı cerrahi müdahale zamanlaması renal fonksiyonların korunması açısından kritik bir karardır. Ders notlarında açıkça vurgulanan **erken cerrahi endikasyonları** şunlardır:\n\n1. **Tekrarlayan Üriner Sistem Enfeksiyonları:** İdrar stazının antibiyotik tedavisine rağmen enfeksiyonu kronikleştirmesi,\n2. **Dirençli ve Tekrarlayan Ağrı / Dizüri:** Hastanın yaşam kalitesini bozan medikal tedaviye yanıtsız semptomlar,\n3. **Ciddi Vezikal Semptomlar ve İdrar Retansiyonu:** Mesane dekompansasyonuna gidiş işaretleri,\n4. **Progresif Renal Hasar Bulguları:** Seri biyokimyasal ve radyolojik testlerde GFR düşüşü, parankim incelmesi veya sintigrafide diferansiyel fonksiyon kaybı saptanmasıdır. Bu bulguların varlığında obstrüksiyon gecikmeksizin cerrahi olarak düzeltilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Erken Cerrahi Karar Algoritması",
                [
                    "1. Klinik İnceleme: Tekrarlayan enfeksiyon ve medikal tedaviye yanıtsız ağrı",
                    "2. Fonksiyonel İzlem: Sintigrafide parankimal diferansiyel fonksiyonda düşüş",
                    "3. Morfolojik Bozulma: USG ve BT'de parankim kalınlığında incelme",
                    "4. Cerrahi Rekonstrüksiyon: Nefron kaybı geri dönüşümsüz olmadan kesin anatomik onarım"
                ]
            ),
            make_recall(
                "Obstrüktif üropatide beklemeden erken cerrahiye geçilmesini gerektiren en kritik laboratuvar ve radyolojik kriter nedir?",
                "Progresif renal hasar bulgularıdır (GFR kaybı, parankim incelmesi).",
                "Böbrek dokusunun eridiğini gösteren nesnel bulgular"
            )
        ]
    })

    return slides
