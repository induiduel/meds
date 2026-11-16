"""
Üriner Obstrüksiyonun Fizyopatolojisi (Ders 11) - Bölüm 1 (Slayt 1 - 10)
Konu: Tanım, Sınıflandırma, Etiyolojik Nedenler, Alt Üriner Sistem Obstrüksiyonu ve Glob Vezikale
Checkpoint: Slayt 9 ([TEKRAR SAYFASI - CHECKPOINT 1])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_1_slides():
    raw = [
        # Slayt 1
        {
            "title": "Obstrüktif Üropatinin Tanımı ve Klinik Belirleyicileri",
            "subtitle": "Üriner Akım Engelleri ve Proksimal Hidrostatik Basınç Artışı",
            "badge": "Obstrüksiyon Tanımı",
            "coreContent": {
                "text": "Obstrüktif üropati, idrar üretim yeri olan renal tübüllerden en dış çıkış noktası olan eksternal üretral meatusa kadar üriner traktusun herhangi bir anatomik seviyesinde idrarın serbest antegrad akışını mekanik veya fonksiyonel olarak engelleyen patolojik durumların tümünü kapsar. Obstrüksiyonun temel patofizyolojik sonucu, tıkanıklık noktasının gerisinde (proksimalinde) idrar stazı ve lümen içi hidrostatik basınç artışıdır. Bu basınç artışı retrograd olarak toplayıcı sistemlere, kalikslere ve renal parankime iletilerek tübüler iskemi ve fonksiyonel kayba yol açar. Bir obstrüktif üropati tablosunun hastadaki nihai klinik ağırlığını ve seyrini belirleyen dört kardinal faktör mevcuttur: (1) Obstrüksiyonun anatomik seviyesi, (2) Tıkanıklığın derecesi (tam veya kısmi), (3) Tıkanıklığın süresi ve (4) Tabloya bakteriyel enfeksiyonun eşlik edip etmemesidir.",
                "keyBullets": [
                    {"title": "Geniş Anatomik Yelpaze", "desc": "Renal tübülden eksternal meaya kadar her düzeyde gelişebilir.", "isKey": True},
                    {"title": "Proksimal Staz ve Basınç", "desc": "Tıkanıklığın proksimalinde sıvı göllenmesi ve basınç yükselmesi esastır.", "isKey": True},
                    {"title": "Dört Temel Belirleyici", "desc": "Seviye, derece, süre ve enfeksiyon varlığı klinik tabloyu ve prognozu belirler.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "Obstrüktif üropatide tıkanıklığın hemen proksimalinde idrar stazı ve lümen içi basınç artışı gelişir.",
                    "basınç artışı",
                    "Tıkanıklık gerisindeki mekanik kuvvet değişimini anımsayınız"
                ),
                make_table(
                    ["Klinik Belirleyici Faktör", "Patofizyolojik Etkisi", "Klinik Örnek"],
                    [
                        [("Obstrüksiyonun Seviyesi", False, ""), ("Supravezikal tek böbreği, infravezikal her iki böbreği etkiler", True, "Anatomik lokalizasyon etkisi"), ("Üreter taşı vs Prostat hiperplazisi", False, "")],
                        [("Obstrüksiyonun Derecesi", False, ""), ("Komplet obstrüksiyon hızla anüri ve parankim hasarı yapar", True, "Tam vs kısmi tıkanıklık"), ("Tıkayıcı taş vs üreteral darlık", False, "")],
                        [("Obstrüksiyonun Süresi", False, ""), ("Süre uzadıkça nefron kaybı ve fibrozis geri dönüşümsüzleşir", True, "Zaman faktörü"), ("Akut renal kolik vs kronik hidronefroz", False, "")],
                        [("Enfeksiyon Varlığı", False, ""), ("Basınç altında ürosepsis ve piyonefroz riskini patlatır", True, "Bakteriyel kolonizasyon"), ("Enfekte taş acil drenaj gerektirir", False, "")]
                    ]
                ),
                make_active_recall(
                    "Obstrüktif üropatide klinik tablonun ağırlığını ve hastanın prognozunu belirleyen 4 temel faktör nedir?",
                    "Obstrüksiyonun seviyesi, derecesi, süresi ve enfeksiyon varlığıdır.",
                    "Dört kardinal prognostik etken"
                )
            ],
            "spotPearls": [
                "Obstrüktif üropati tübülden meaya kadar herhangi bir düzeyde olabilir.",
                "Tıkanıklığın proksimalinde STAZ ve BASINÇ ARTIŞI gelişir.",
                "Prognozu belirleyen 4 etken: Seviye, derece, süre ve enfeksiyondur."
            ]
        },

        # Slayt 2
        {
            "title": "Üriner Obstrüksiyonun Sınıflandırma Kriterleri",
            "subtitle": "Etiyoloji, Süre, Derece, Seviye ve Taraf Odaklı Tipoloji",
            "badge": "Sınıflandırma",
            "coreContent": {
                "text": "Üriner sistem obstrüksiyonları, klinik yaklaşımı ve aciliyet derecesini belirlemek amacıyla beş temel kategorik ölçüte göre sınıflandırılır: (1) Etiyolojiye göre: Doğuştan gelen anatomik kusurlar konjenital (örneğin posterior üretral valv, UPJ darlığı), sonradan kazanılanlar edinseldir (taş, BPH, tümör). (2) Süreye göre: Aniden gelişen akut obstrüksiyon (renal kolik tablosu) veya aylar/yıllar içinde sinsi ilerleyen kronik obstrüksiyon. (3) Derecesine göre: İdrar geçişinin tamamen durduğu komplet (tam) veya lümenin kısmen açık kaldığı inkomplet (parsiyel) obstrüksiyon. (4) Anatomik seviyeye göre: Mesane ve distalini ilgilendiren infravezikal (alt üriner sistem) veya üreter ve böbreği ilgilendiren supravezikal (üst üriner sistem). (5) Etkilenen böbrek tarafına göre: Tek bir böbrek ünitesini ilgilendiren unilateral veya her iki böbreği eş zamanlı boğan bilateral obstrüksiyon.",
                "keyBullets": [
                    {"title": "Etiyolojik Ayrım", "desc": "Konjenital (yapısal anomaliler) ve Edinsel (taş, BPH, malignite) nedenler.", "isKey": True},
                    {"title": "Seviye Ayrımı", "desc": "İnfravezikal (mesane çıkımı ve üretra) ve Supravezikal (üreter ve böbrek).", "isKey": True},
                    {"title": "Bilateralite Kuralı", "desc": "İnfravezikal obstrüksiyonlar daima bilateral böbrek etkilenmesine yol açar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "İnfravezikal vs Supravezikal Obstrüksiyon",
                    "İnfravezikal Obstrüksiyon",
                    "Mesane tabanı, prostat veya üretra seviyesindedir; mesane duvarını kalınlaştırır ve daima bilateral üst sistemi etkiler.",
                    "Supravezikal Obstrüksiyon",
                    "Üreter veya renal pelvis seviyesindedir; mesane etkilenmez; çoğunlukla tek taraflı (unilateral) hidronefroz üretir."
                ),
                make_micro_quiz(
                    "Mesane çıkımında veya üretrada yer alan infravezikal bir obstrüksiyonun üst üriner sistem üzerindeki en temel karakteristik yansıması hangisidir?",
                    {
                        "A": "Daima tek taraflı sol böbrek atrofisi yapması",
                        "B": "Daima bilateral (her iki böbreği kapsayan) hidronefroz ve dilatasyona yol açması",
                        "C": "Böbrek fonksiyonlarını hiçbir zaman etkilememesi",
                        "D": "Mesane duvarında incelme ve gevşeme yapması",
                        "E": "Yalnızca kadın hastalarda görülmesi"
                    },
                    "B",
                    {
                        "A": "İnfravezikal obstrüksiyon tek taraflı kalmaz.",
                        "B": "Doğru cevap B'dir: Mesane çıkımı tıkandığında artan intravezikal basınç bilateral vezikoüreteral bileşkeyi bozarak her iki böbreği birden etkiler.",
                        "C": "Tedavi edilmezse bilateral KBY yapar.",
                        "D": "Mesane duvarında hipertrofi ve kalınlaşma yapar.",
                        "E": "Her iki cinsiyette de (özellikle BPH'lı erkeklerde) sıktır."
                    }
                ),
                make_cloze(
                    "Mesane seviyesinin yukarısında, üreter veya renal pelviste yer alan obstrüksiyonlara supravezikal obstrüksiyon adı verilir.",
                    "supravezikal",
                    "Mesane üstü tıkanıklık terimini yazınız"
                )
            ],
            "spotPearls": [
                "İnfravezikal obstrüksiyon = Mesane boynu, prostat ve üretra seviyesi (bilateral etkilenim).",
                "Supravezikal obstrüksiyon = Üreter ve renal pelvis seviyesi (çoğunlukla unilateral etkilenim).",
                "Komplet bilateral obstrüksiyon anüri tablosuyla seyreden mutlak bir ürolojik acildir."
            ]
        },

        # Slayt 3
        {
            "title": "Renal Düzeydeki Obstrüksiyon Nedenleri",
            "subtitle": "Pelvikaliksiyel Bileşke Darlıkları, Kistler, Taşlar ve Tümörler",
            "badge": "Renal Obstrüksiyon",
            "coreContent": {
                "text": "Böbrek ve renal pelvis düzeyindeki obstrüktif patolojiler, idrarın kalikslerden toplanıp üretere aktarıldığı ilk hunide akım direncine yol açar. Nedenler dört ana patolojik grupta incelenir: (1) Konjenital nedenler: En sık konjenital anomali Üreteropelvik Bileşke (UPJ) darlığıdır; intrensek adinamik düz kas segmenti veya alt polü çaprazlayan aberran bir renal arter/ven basısıyla ortaya çıkar. Polikistik böbrek hastalığı ve peripelvik kistler de toplayıcı kanalları basıya uğratabilir. (2) Neoplastik nedenler: Renal Pelvis Transizyonel Hücreli Karsinomu (TCC/Urotelyal karsinom), Renal Hücreli Karsinom (RCC), Wilms tümörü veya multipl miyelomda protein silendir tıkaçları. (3) İnflamatuar nedenler: Renal tüberküloz (kazeöz nekroz striktürleri) ve kist hidatik. (4) Taş ve vasküler nedenler: Pelvisi dolduran geyik boynuzu (staghorn) taşlar, renal arter anevrizması ve analjezik nefropatisinde kopan nekrotik papillaların pelviste tıkanmasıdır.",
                "keyBullets": [
                    {"title": "En Sık Konjenital", "desc": "Üreteropelvik bileşke (UPJ) darlığı ve aberran alt pol damar basısıdır.", "isKey": True},
                    {"title": "Geyik Boynuzu Taşlar", "desc": "Staghorn kalkülleri tüm pelvikaliksiyel sistemi doldurarak tam akım engeli kurar.", "isKey": True},
                    {"title": "Papiller Nekroz Tıkanması", "desc": "Kopan iskemik papilla dokuları pelvis çıkışını tıkayarak akut kolik yapabilir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kategori", "Spesifik Renal Patoloji", "Obstrüksiyon Mekanizması"],
                    [
                        [("Konjenital", False, ""), ("UPJ Darlığı ve Aberran Damar", True, "Pelvis çıkım darlığı"), ("Pelvis çıkışında adinamik dar segment veya dıştan vasküler bası"), ],
                        [("Neoplastik", False, ""), ("Renal Pelvis Urotelyal Karsinomu", True, "İntralüminal tümöral kitle"), ("Pelvis lümenini dolduran vejetan karnabahar benzeri kitle"), ],
                        [("İnflamatuar", False, ""), ("Renal Tüberküloz", True, "Kazeifikasyon sikatrisi"), ("İnfundibulum ve kaliks boyunlarında kazeöz fibrotik darlık"), ],
                        [("Kalkülöz / Diğer", False, ""), ("Staghorn Taş ve Papiller Nekroz", False, ""), ("Pelvis lümenini tıkayan taş kütlesi veya nekrotik doku tıkacı"), ]
                    ]
                ),
                make_micro_quiz(
                    "Çocukluk çağında ve genç erişkinlerde böbrek pelvisi düzeyinde en sık saptanan konjenital obstrüksiyon nedeni hangisidir?",
                    {
                        "A": "Böbrek kist hidatiği",
                        "B": "Üreteropelvik bileşke (UPJ) darlığı",
                        "C": "Multipl miyelom silendir nefropatisi",
                        "D": "Renal ven trombozu",
                        "E": "Retroperitoneal fibrozis"
                    },
                    "B",
                    {
                        "A": "Kist hidatik paraziter nadir nedendir.",
                        "B": "Doğru cevap B'dir: Üreteropelvik bileşke (UPJ) darlığı konjenital üst üriner sistem obstrüksiyonlarının en sık nedenidir.",
                        "C": "Miyelom ileri yaşta görülür.",
                        "D": "Venöz tromboz vaskülerdir.",
                        "E": "Retroperitoneal fibrozis üreter düzeyindedir."
                    }
                ),
                make_cloze(
                    "Böbrek pelvisi düzeyinde konjenital hidronefrozun en yaygın nedeni üreteropelvik bileşke veya UPJ darlığıdır.",
                    "UPJ",
                    "Üreteropelvik bileşke kısaltmasını yazınız"
                )
            ],
            "spotPearls": [
                "Renal düzeyde en sık konjenital obstrüksiyon UPJ (üreteropelvik bileşke) darlığıdır.",
                "Aberran alt pol renal damarları pelvis çıkışına dıştan bası yaparak hidronefroz yapabilir.",
                "Staghorn taşlar ve dökülen nekrotik papillalar pelviste intralüminal tıkanma nedenidir."
            ]
        },

        # Slayt 4
        {
            "title": "Üreteral Obstrüksiyon Nedenleri: İntrensek ve Ekstrensek Patolojiler",
            "subtitle": "İntralüminal Tıkaçlardan Retroperitoneal Kitle ve Fibrozislere",
            "badge": "Üreteral Obstrüksiyon",
            "coreContent": {
                "text": "Üreter yaklaşık 25-30 cm uzunluğunda, ince lümenli retroperitoneal tübüler bir organdır. Üreteral obstrüksiyonlar lümenin içinden (intrensek) veya çevre dokulardan kaynaklanan dış basıyla (ekstrensek) gelişir: (1) İntrensek Nedenler: En sık neden üreter taşlarıdır (kalküller en sık üreteropelvik bileşke, iliak damarları çaprazlama noktası ve üreterovezikal bileşkede takılır). Üreterin primer urotelyal karsinomu, üreterosel, üreter darlıkları, kan pıhtıları ve üreteritis kistika diğer intrensek faktörlerdir. (2) Ekstrensek Bası Nedenleri: Pelvik ve jinekolojik maligniteler (özellikle ileri evre Serviks Kanseri kadınlarda bilateral üreteral obstrüksiyon ve üremik ölümün bir numaralı nedenidir; rektum ve prostat kanserleri), Retroperitoneal Fibrozis (Ormond hastalığı; aort çevresinde üreterleri ortaya çekip boğan fibröz kitle), aort anevrizması, pelvik lipomatozis, lenfosel, retrokaval üreter ve GEBELİKTİR (sağ üreterde belirgin fizyolojik bası).",
                "keyBullets": [
                    {"title": "İntrensek Lider: Taş", "desc": "Üreteral obstrüksiyonun tek başına en sık nedeni lümeni tıkayan taşlardır.", "isKey": True},
                    {"title": "Malign Ekstrensek: Serviks Ca", "desc": "Kadınlarda bilateral üreteral bası ve üremiye yol açan en kritik malignitedir.", "isKey": True},
                    {"title": "Retroperitoneal Fibrozis", "desc": "Ormond hastalığı üreterleri mediyale doğru çekerek dıştan boğar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Obstrüksiyon Türü", "En Karakteristik Patolojiler", "Klinik Özellik"],
                    [
                        [("İntrensek (Lümen İçi)", False, ""), ("Üreter taşları, Urotelyal karsinom, Kan pıhtısı", True, "Lümen içi mekanik tıkaç"), ("Akut renal kolik, hematüri"), ],
                        [("Ekstrensek (Dıştan Bası)", False, ""), ("Serviks ca, Rektum ca, Retroperitoneal kitle", True, "Dıştan bası yapan infiltratif kitle"), ("Sinsi ilerleyen hidronefroz, bilateralite"), ],
                        [("İnflamatuar Ekstrensek", False, ""), ("Retroperitoneal Fibrozis (Ormond hastalığı)", True, "Fibröz bant sıkıştırması"), ("Üreterleri mediyale çeken retroperitoneal plak"), ],
                        [("Fizyolojik Ekstrensek", False, ""), ("Gebelik (Özellikle sağ üreter dilatasyonu)", False, ""), ("Dekstro-rotasyon ve hormonal gevşeme"), ]
                    ]
                ),
                make_micro_quiz(
                    "İleri evre jinekolojik kanserli kadın hastalarda bilateral üreteral obstrüksiyona, hidronefroza ve tedavi edilmezse üremik ölüme en sık yol açan primer pelvik malignite hangisidir?",
                    {
                        "A": "Endometrium kanseri",
                        "B": "Serviks (rahim ağzı) kanseri",
                        "C": "Over karsinomu",
                        "D": "Vajen sarkomu",
                        "E": "Koryokarsinom"
                    },
                    "B",
                    {
                        "A": "Endometrium kanseri daha geç bası yapar.",
                        "B": "Doğru cevap B'dir: İleri evre serviks kanseri parametriyumlara doğrudan yayılarak üreterleri bilateral dıştan infiltre eder ve üremiye yol açar.",
                        "C": "Over kanseri daha çok peritoneal yayılır.",
                        "D": "Vajen sarkomu nadirdir.",
                        "E": "Koryokarsinom hematojen yayılır."
                    }
                ),
                make_cloze(
                    "Retroperitoneal alanda aort çevresinde gelişerek üreterleri mediyale doğru çeken ve obstrüksiyona yol açan idiyopatik fibröz hastalığa retroperitoneal fibrozis veya Ormond hastalığı denir.",
                    "retroperitoneal fibrozis",
                    "Üreteri boğan fibröz hastalık adını yazınız"
                )
            ],
            "spotPearls": [
                "Üreteral intrensek obstrüksiyonun en sık nedeni üreter taşlarıdır.",
                "Kadınlarda bilateral üreteral basının en sık malign nedeni SERVİKS KANSERİDİR.",
                "Retroperitoneal fibrozis (Ormond hastalığı) üreterleri mediyale çeken sinsi bir nedendir."
            ]
        },

        # Slayt 5
        {
            "title": "Mesane Çıkımı ve Üretra Düzeyindeki Obstrüksiyon Nedenleri",
            "subtitle": "İnfravezikal Patolojiler: BPH, Kanserler, Striktürler ve Valvler",
            "badge": "İnfravezikal Nedenler",
            "coreContent": {
                "text": "Mesane çıkımını ve üretrayı ilgilendiren infravezikal obstrüksiyonlar, klinik pratikte en sık karşılaşılan ve tüm üriner sistemi bilateral olarak tehdit eden obstrüktif üropati grubudur. Bu düzeydeki başlıca etiyolojik aktörler: (1) Prostatik Nedenler: Yaşlanan erkeklerde tek başına en yaygın obstrüksiyon nedeni Benign Prostat Hiperplazisidir (BPH; transizyonel zon büyümesiyle prostatik üretrayı komprese eder). Prostat adenokarsinomu (periferik zon kökenli olup ileri evrede üretrayı tutar), akut prostatit ve prostat apsesi diğer nedenlerdir. (2) Üretral Nedenler: Erkek çocuklarda en sık konjenital neden Posterior Üretral Valvdir (PUV). Yetişkinlerde travma, geçirilmiş enfeksiyon veya kateterizasyon sonrası gelişen Üretra Darlıkları (striktür), eksternal mea darlığı, fimozis ve üretral kalküller. (3) Nörolojik Nedenler: Spina bifida, meningomiyelosel, diyabetik nöropati veya spinal kord travmasına bağlı gelişen Detrüsör-Sfinkter Disinerjisi ve nöropatik mesanedir.",
                "keyBullets": [
                    {"title": "Yaşlı Erkekte BPH", "desc": "Erişkin erkekte infravezikal obstrüksiyonun en sık nedeni Benign Prostat Hiperplazisidir.", "isKey": True},
                    {"title": "Erkek Çocukta PUV", "desc": "Erkek çocuklarda en sık ve en yıkıcı konjenital infravezikal neden Posterior Üretral Valvdir.", "isKey": True},
                    {"title": "Fonksiyonel Nedenler", "desc": "Nöropatik mesane ve detrüsör-sfinkter disinerjisi mekanik darlık olmadan obstrüksiyon yapar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kategori", "İnfravezikal Patoloji", "Hedef Popülasyon", "Patofizyolojik Etki"],
                    [
                        [("Benign Prostat", False, ""), ("Benign Prostat Hiperplazisi (BPH)", True, "Transizyonel zon hiperplazisi"), ("50 yaş üstü erkekler", False, ""), ("Prostatik üretranın mekanik kompresyonu")],
                        [("Konjenital Valv", False, ""), ("Posterior Üretral Valv (PUV)", True, "Verumontanum membranöz kapağı"), ("Yenidoğan ve erkek çocuklar", False, ""), ("Üretra içinde tek yönlü valv tıkanıklığı")],
                        [("Edinsel Darlık", False, ""), ("Üretra Darlığı (Striktür)", True, "Spongiofibrozis darlığı"), ("Travma / Kateter öykülü erkek", False, ""), ("Lümende fibrotik halkasal daralma")],
                        [("Nörolojik", False, ""), ("Nöropatik Mesane / Disinerji", False, ""), ("Spinal travma, Spina bifida", False, ""), ("Detrüsör kasılırken sfinkterin gevşeyememesi")]
                    ]
                ),
                make_micro_quiz(
                    "Yeni doğan bir erkek bebekte prenatal ultrasonda bilateral ağır hidronefroz, dev mesane (megasistis) ve dilate posterior üretra ('anahtar deliği' manzarası) saptanıyor. En olası konjenital tanı hangisidir?",
                    {
                        "A": "Üreterosel",
                        "B": "Posterior Üretral Valv (PUV)",
                        "C": "Hipospadias",
                        "D": "Fimozis",
                        "E": "Polikistik böbrek hastalığı"
                    },
                    "B",
                    {
                        "A": "Üreterosel distal üretere aittir.",
                        "B": "Doğru cevap B'dir: Erkek bebekte bilateral hidronefroz ve dilate posterior üretra ile anahtar deliği manzarası veren en sık konjenital patoloji Posterior Üretral Valvdir (PUV).",
                        "C": "Hipospadias mea yerleşim kusurudur, megasistis yapmaz.",
                        "D": "Fimozis sünnet derisi darlığıdır.",
                        "E": "Polikistik böbrek kistik parankimdir, megasistis yapmaz."
                    }
                ),
                make_cloze(
                    "İleri yaş erkek popülasyonunda infravezikal üriner obstrüksiyonun tek başına en yaygın görülen nedeni benign prostat hiperplazisidir.",
                    "benign prostat hiperplazisi",
                    "Sık görülen prostat büyümesi hastalığını yazınız"
                )
            ],
            "spotPearls": [
                "Erişkin erkekte infravezikal tıkanıklığın 1 numaralı nedeni BPH'DIR.",
                "Erkek çocuklarda en sık ve en tehlikeli konjenital infravezikal neden POSTERİOR ÜRETRAL VALVDİR (PUV).",
                "Nöropatik mesane mekanik darlık olmadan fonksiyonel obstrüksiyon yapar."
            ]
        },

        # Slayt 6
        {
            "title": "Yaş ve Cinsiyete Göre Üriner Obstrüksiyon Epidemiyolojisi",
            "subtitle": "Yenidoğan, Çocukluk, Doğurganlık Çağı ve Geriatrik Dağılım",
            "badge": "Epidemiyolojik Dağılım",
            "coreContent": {
                "text": "Üriner obstrüksiyonların etiyolojik spektrumu hastanın yaşına ve cinsiyetine göre belirgin farklılıklar sergiler. (1) Erken çocukluk ve yenidoğan dönemi: Obstrüksiyonların büyük çoğunluğu konjenital anomalilere bağlıdır; erkek bebeklerde tek başına en önemli neden Posterior Üretral Valv (PUV) ve eksternal mea darlığı iken, kız çocuklarında distal üretral stenoz ve ektopik üreterosel öne çıkar. Her iki cinste UPJ darlığı sıktır. (2) Genç ve orta yaş erişkinler (20-50 yaş): Erkek ve kadınlarda nefrolitiazis (üriner sistem taş hastalığı) primer nedendir. Kadınlarda bu yaş grubunda gebelik ve jinekolojik patolojiler (endometriozis, pelvik kitleler) eklenir. (3) İleri yaş (>60 yaş): Erkeklerde Benign Prostat Hiperplazisi (BPH), prostat kanseri ve üretra darlıkları ezici çoğunluğu oluşturur; kadınlarda ise ilerlemiş serviks veya uterus kanserleri ile ağır pelvik organ prolapsusları (sistosel/uterin prolapsus) obstrüksiyon nedenidir.",
                "keyBullets": [
                    {"title": "Erken Yaş Erkek", "desc": "Posterior üretral valv (PUV) ve UPJ darlığı primer konjenital etkenlerdir.", "isKey": True},
                    {"title": "Genç Erişkin", "desc": "Her iki cinste en sık akut obstrüksiyon nedeni üriner sistem taşlarıdır.", "isKey": True},
                    {"title": "İleri Yaş Karşılaştırması", "desc": "Erkekte BPH ve prostat ca; kadında serviks kanseri ve pelvik prolapsus.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Yaş Grubu", "Erkeklerde En Sık Nedenler", "Kadınlarda En Sık Nedenler"],
                    [
                        [("Yenidoğan / Çocukluk", False, ""), ("Posterior üretral valv (PUV), UPJ darlığı", True, "Erkek çocukta PUV lider"), ("Distal üretral darlık, ektopik üreterosel", False, "")],
                        [("Genç Erişkin (20-50)", False, ""), ("Üriner sistem taşları (nefrolitiazis), travma", True, "Taş hastalığı çağı"), ("Üriner taşlar, gebelik basısı, pelvik kitleler", False, "")],
                        [("İleri Yaş (>60 yaş)", False, ""), ("Benign Prostat Hiperplazisi (BPH), Prostat kanseri", True, "Yaşlı erkekte BPH"), ("Serviks kanseri, pelvik organ sarkması (sistosel)", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "İleri yaştaki bir kadın hastada infravezikal üriner obstrüksiyona ve akut/kronik idrar retansiyonuna yol açabilecek en yaygın benign anatomik pelvik patoloji hangisidir?",
                    {
                        "A": "Posterior üretral valv",
                        "B": "Pelvik organ prolapsusu (Ağır sistosel / uterin prolapsus)",
                        "C": "Retrokaval üreter",
                        "D": "Wilms tümörü",
                        "E": "Polikistik böbrek hastalığı"
                    },
                    "B",
                    {
                        "A": "PUV yalnız erkek bebeklerde görülür.",
                        "B": "Doğru cevap B'dir: Yaşlı kadınlarda mesanenin vajinaya doğru fıtıklaşması (sistosel) mesane boynunu bükerek infravezikal obstrüksiyona yol açar.",
                        "C": "Retrokaval üreter üst üriner sistemdir.",
                        "D": "Wilms tümörü çocukluk çağı böbrek tümörüdür.",
                        "E": "Polikistik böbrek infravezikal obstrüksiyon yapmaz."
                    }
                ),
                make_active_recall(
                    "Erkek çocuklarda yenidoğan ve süt çocukluğu döneminde bilateral obstrüktif üropatinin en sık konjenital nedeni nedir?",
                    "Posterior Üretral Valvdir (PUV).",
                    "Erkek çocuk infravezikal konjenital lideri"
                )
            ],
            "spotPearls": [
                "Erkek çocukta: Posterior Üretral Valv (PUV).",
                "Genç erişkinde: Üriner sistem taş hastalığı (her iki cinste).",
                "İleri yaş erkekte: BPH; İleri yaş kadında: Serviks kanseri ve pelvik prolapsus."
            ]
        },

        # Slayt 7
        {
            "title": "Alt Üriner Sistem Obstrüksiyonunun Genel Patofizyolojisi",
            "subtitle": "Üretral Direnç Artışı, İntravezikal Basınç ve Retrograd Etkiler",
            "badge": "İnfravezikal Patofizyoloji",
            "coreContent": {
                "text": "Alt üriner sistem (infravezikal) obstrüksiyonunda primer patofizyolojik olay, mesane çıkımında veya üretrada akıma karşı hidrolik direncin (üretral direnç) artmasıdır. Bu direnci aşabilmek ve idrar boşaltımını sürdürebilmek için mesane detrüsör kası daha yüksek bir intravezikal basınç (normal işeme basıncının 2-4 katı) üretmek zorunda kalır. Artan intravezikal basınç ve lümen gerginliği; mesane, prostat ve üretra dokularında geniş kapsamlı anatomik deformasyonlara yol açar: (1) Üretra düzeyinde: Tıkanıklık proksimalinde üretral distansiyon, duvarda incelme, divertikül oluşumu, zayıflayan alanlarda rüptür, periüretral apse ve fistülleşme. (2) Prostat düzeyinde: Yüksek basıncın intraprostatik kanallara reflüsüyle duktal dilatasyon, kronik prostatit ve epididimoorşit. (3) Mesane düzeyinde: Detrüsör hipertrofisi, trabekülasyon ve divertiküller gelişirken, yüksek basınç vezikoüreteral bileşkeyi tahrip ederek hidroüreteronefroza zemin hazırlar.",
                "keyBullets": [
                    {"title": "Direnç ve Basınç Artışı", "desc": "İnfravezikal direnci aşmak için mesane içi basınç normalin 2-4 katına fırlar.", "isKey": True},
                    {"title": "Üretral Hasar", "desc": "Distansiyon, divertikül, lümen rüptürü ve periüretral apse/fistül riski doğar.", "isKey": True},
                    {"title": "Prostatik Reflü", "desc": "İdrarın prostatik kanallara geri kaçışı tekrarlayan prostatit ve orşit yapar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "İnfravezikal Obstrüksiyonda Doku Hasarı Zinciri",
                    [
                        "1. Üretra veya mesane çıkımında anatomik mekanik engel oluşur",
                        "2. Detrüsör kası idrarı atmak için intravezikal basıncı 2-4 kat artırır",
                        "3. Yüksek basınç intraprostatik kanallara ve divertiküllere doğru geri yansır",
                        "4. Üreterotrigonal kapak mekanizması bozulur; bilateral VUR ve böbrek hasarı başlar"
                    ]
                ),
                make_cloze(
                    "İnfravezikal obstrüksiyonu yenmek amacıyla işeme sırasında mesane içi basınç normal fizyolojik değerin yaklaşık 2-4 katına kadar yükselir.",
                    "2-4 katına",
                    "İntravezikal basınç artış katsayısını anımsayınız"
                ),
                make_active_recall(
                    "Alt üriner sistem obstrüksiyonunda yüksek işeme basıncının prostat dokusu içine geri kaçması hangi tekrarlayan klinik enfeksiyonlara yol açar?",
                    "Kronik prostatit ve retrograd yolla epididimit / epididimoorşite yol açar.",
                    "Prostatik kanal reflüsü enfeksiyonları"
                )
            ],
            "spotPearls": [
                "İnfravezikal obstrüksiyonda mesane içi basınç 2-4 kat artar.",
                "Yüksek basınç üretrada divertikül, rüptür ve periüretral fistüle yol açabilir.",
                "Vezikoüreteral bileşkenin bozulmasıyla bilateral hidroüreteronefroz gelişir."
            ]
        },

        # Slayt 8
        {
            "title": "Akut Alt Üriner Sistem Obstrüksiyonu: Glob Vezikale ve Akut Retansiyon",
            "subtitle": "Ağrılı Mesane Distansiyonu ve Ani İdrar Boşaltamama Tablosu",
            "badge": "Akut Retansiyon",
            "coreContent": {
                "text": "Akut alt üriner sistem obstrüksiyonu, mesane çıkımının veya üretranın aniden tamamen tıkanması sonucu hastanın aşırı idrar yapma isteğine rağmen tek bir damla bile idrar çıkaramaması ile karakterize acil bir klinik tablodur (akut idrar retansiyonu). En sık etiyolojik nedenler: BPH zemininde alkol alımı, soğuğa maruziyet, antikolinerjik/sempatomimetik ilaç kullanımı sonucu gelişen akut pelvik konjesyon, üretra taşı impaksiyonu, üretral travma (straddle yaralanması) ve akut bakteriyel prostatit/prostat apsesidir. Fizik muayenede suprapubik bölgede göbeğe doğru uzanan, son derece hassas, palpasyonla ağrılı, perküsyonla matite veren gergin bir kitle palpe edilir; bu duruma 'Glob Vezikale' adı verilir. Mesane içinde 1000-1500 ml'ye varan idrar birikebilir. Şiddetli suprapubik ağrı, ajitasyon, taşikardi ve hipertansiyon eşlik eder; acil üretral drenaj endikasyonudur.",
                "keyBullets": [
                    {"title": "Karakteristik Tablo", "desc": "Aşırı işeme isteği olmasına karşın hiç idrar yapamama ve şiddetli suprapubik ağrıdır.", "isKey": True},
                    {"title": "Glob Vezikale", "desc": "Suprapubik bölgede palpe edilen gergin, ağrılı, perküsyonla matite veren mesane kitlesidir.", "isKey": True},
                    {"title": "Tetikleyici Faktörler", "desc": "BPH hastasında soğuk, alkol, antikolinerjik/antihistaminik ilaçlar retansiyonu tetikler.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_branching_logic(
                    "68 yaşında BPH tanısı olan bir erkek hasta, şiddetli grip nedeniyle kullandığı psödoefedrin ve klorfeniramin içeren soğuk algınlığı ilacından 6 saat sonra acil servise başvuruyor. Hasta alt karında kıvrandırıcı bir ağrı olduğunu, idrarını hiç yapamadığını söylüyor. Suprapubik bölgede göbeğe kadar uzanan ağrılı gergin mat bir kitle (glob vezikale) saptanıyor. Bu hastada acil servisteki ilk tanısal ve terapötik yaklaşım ne olmalıdır?",
                    [
                        {"text": "Akut üriner retansiyon tanısıyla acilen steril şartlarda 16-18 French Foley üretral kateter takılarak mesane dekompresyonu sağlanmalıdır", "isCorrect": True, "feedback": "Hayat kurtaran acil karar! Glob vezikalede ilk basamak acil tedavi üretral kateterizasyon ile mesanenin rahatlatılmasıdır."},
                        {"text": "Hastaya yüksek doz intravenöz furosemid (Lasix) verilerek idrar çıkışı zorlanmalıdır", "isCorrect": False, "feedback": "Çıkış tıkalıyken diüretik vermek mesaneyi patlatabilir; kontrendikedir."},
                        {"text": "Hasta eve gönderilip sabah üroloji polikliniğine başvurması önerilmelidir", "isCorrect": False, "feedback": "Akut glob vezikale acil boşaltılması gereken dayanılmaz bir tablodur."}
                    ]
                ),
                make_cloze(
                    "Akut komplet infravezikal obstrüksiyonda mesanenin aşırı dolarak suprapubik bölgede gergin, ağrılı bir kitle oluşturması tablosuna glob vezikale denir.",
                    "glob vezikale",
                    "Palpe edilen gergin mesane kitlesi Latince adını yazınız"
                ),
                make_active_recall(
                    "BPH'lı yaşlı bir erkekte akut üriner retansiyonu (glob vezikale) tetikleyen en yaygın iyatrojenik farmakolojik etken grubu nedir?",
                    "Antikolinerjikler, antihistaminikler ve alfa-adrenerjik sempatomimetik içeren soğuk algınlığı ilaçlarıdır.",
                    "Mesane boynunu kasan / detrüsörü felç eden ilaçlar"
                )
            ],
            "spotPearls": [
                "Akut retansiyonda suprapubik gergin ağrılı kitle = GLOB VEZİKALE.",
                "BPH zemininde soğuk algınlığı ilaçları (sempatomimetik/antikolinerjik) retansiyonu tetikler.",
                "Tedavide ilk adım derhal steril üretral kateterizasyon uygulamaktır."
            ]
        },

        # Slayt 9 (CHECKPOINT 1)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Obstrüktif Üropatinin Tanımı, Etiyolojisi ve Sınıflandırılması",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 1",
            "coreContent": {
                "text": "Bu ilk bölümde obstrüktif üropatinin temellerini ve alt üriner sistem obstrüksiyonuna giriş yaptık. Obstrüktif üropati tübülden eksternal meaya kadar her düzeyde idrar akım engelidir; proksimalinde staz ve basınç artışı gelişir. Klinik tabloyu belirleyen 4 kardinal faktör: seviye, derece, süre ve enfeksiyondur. Sınıflandırma: konjenital/edinsel, akut/kronik, komplet/inkomplet, infravezikal/supravezikal ve unilateral/bilateraldir. İnfravezikal tıkanıklıklar daima her iki böbreği birden etkiler. Renal düzeyde en sık konjenital neden UPJ darlığıdır. Üreterde en sık intrensek neden taşlar; en sık malign ekstrensek neden serviks kanseridir (kadınlarda üremiye yol açar). İnfravezikal düzeyde erkek çocukta en sık Posterior Üretral Valv (PUV), yaşlı erkekte ise BPH'dır. Akut infravezikal obstrüksiyonda göbeğe uzanan ağrılı gergin kitle glob vezikaledir ve acil üretral kateterizasyon gerektirir.",
                "keyBullets": [
                    {"title": "Dört Belirleyici", "desc": "Seviye, derece, süre ve enfeksiyon varlığı klinik seyri ve prognozu tayin eder.", "isKey": True},
                    {"title": "Etiyoloji İmzaları", "desc": "Böbrekte UPJ darlığı; üreterde taş ve serviks ca; çocukta PUV; yaşlıda BPH.", "isKey": True},
                    {"title": "Glob Vezikale", "desc": "Akut retansiyonda suprapubik ağrılı gergin mesane kitlesidir; acil kateter gerekir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Anatomik Düzey", "En Karakteristik Patoloji", "Popülasyon / Klinik Özellik"],
                    [
                        [("Böbrek Pelvisi", False, ""), ("UPJ Darlığı ve Aberran Damar", True, "Pelvis çıkış darlığı"), ("Çocukluk çağında konjenital hidronefroz")],
                        [("Üreter (İntrensek)", False, ""), ("Üreter Taşları (Kalküller)", True, "En sık üreteral intrensek"), ("Akut renal kolik, hematüri")],
                        [("Üreter (Ekstrensek)", False, ""), ("İleri Evre Serviks Kanseri", True, "Kadında bilateral bası"), ("Kadınlarda obstrüktif üremi ve ölüm")],
                        [("Üretra (Çocuk)", False, ""), ("Posterior Üretral Valv (PUV)", True, "Erkek bebekte megasistis"), ("Bilateral ağır hidronefroz, anahtar deliği")],
                        [("Mesane Çıkımı (Yaşlı)", False, ""), ("Benign Prostat Hiperplazisi (BPH)", True, "Yaşlı erkekte BPH"), ("Kronik infravezikal obstrüksiyon prototipi")]
                    ]
                ),
                make_cloze(
                    "Kadınlarda parametriyumlara yayılarak bilateral üreteral obstrüksiyona ve üremiye en sık yol açan primer pelvik malignite serviks kanseridir.",
                    "serviks",
                    "Bilateral üreteral obstrüksiyon yapan jinekolojik kanseri anımsayınız"
                ),
                make_active_recall(
                    "İnfravezikal obstrüksiyonların supravezikal obstrüksiyonlara kıyasla böbrek parankimi üzerindeki en önemli sistemik farkı nedir?",
                    "İnfravezikal obstrüksiyonların daima bilateral (her iki böbreği birden) etkileyerek sistemik böbrek yetmezliğine yol açabilmesidir.",
                    "Bilateralite ve sistemik yetmezlik riski"
                )
            ],
            "spotPearls": [
                "Obstrüksiyon proksimalinde daima STAZ ve BASINÇ ARTIŞI olur.",
                "Erkek çocukta PUV, yaşlı erkekte BPH en sık infravezikal nedendir.",
                "Kadınlarda bilateral üreteral obstrüksiyonun en sık malign nedeni serviks kanseridir."
            ]
        },

        # Slayt 10
        {
            "title": "Glob Vezikalede Dekompresyon İlkeleri ve 'Ex Vacuo' Hematüri",
            "subtitle": "Mesanenin Hızlı Boşaltılmasında Mukoza Kanaması ve Hipotansiyon Riski",
            "badge": "Dekompresyon İlkeleri",
            "coreContent": {
                "text": "Akut üriner retansiyon ve glob vezikale tablosunda acil üretral Foley kateterizasyon hayat kurtarıcıdır; ancak aşırı gerilmiş bir mesanenin boşaltılmasında çok kritik bir ürolojik komplikasyon riski mevcuttur. 1000-1500 ml idrarla aşırı distandü olmuş mesanede lümen içi basınç çok yüksektir; bu yüksek basınç mesane duvarındaki konjeste mukozal ve submukozal venöz pleksusları dıştan komprese ederek kanamalarını engeller. Eğer kateter takıldığında tüm bu hacim birdenbire ve kontrolsüzce son damlasına kadar hızla boşaltılırsa, ani basınç düşüşü ve lümende oluşan negatif vakum etkisi nedeniyle gerilmiş submukozal kılcal damarlar yırtılır. Bu tabloya 'hematuria ex vacuo' (ani boşalmaya bağlı mesane kanaması) adı verilir. Ayrıca pelvik venlerdeki ani göllenmeye bağlı geçici hipotansiyon ve bradikardi (vazovagal senkop) gelişebilir. Bu nedenle aşırı distandü mesaneler kademeli ve aralıklı klempleme yöntemiyle boşaltılmalıdır.",
                "keyBullets": [
                    {"title": "Hematuria Ex Vacuo", "desc": "Aşırı gergin mesanenin aniden boşaltılmasıyla oluşan mukozal venöz kanamadır.", "isKey": True},
                    {"title": "Vakum Mekanizması", "desc": "Lümendeki ani basınç düşüşü submukozal konjeste damarları yırtar.", "isKey": True},
                    {"title": "Kademeli Boşaltma", "desc": "Her 500-750 ml'de bir kateter klemplenerek aralıklı dekompresyon uygulanmalıdır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Ani Dekompresyon ve Ex Vacuo Hematüri Zinciri",
                    [
                        "1. Glob vezikalede 1500 ml idrar yüksek intralüminal basınçla mesane venlerini sıkıştırır",
                        "2. Üretral kateter takılarak tüm idrar saniyeler içinde kontrolsüzce hızla boşaltılır",
                        "3. İntravezikal basınç sıfıra düşer; tamponlayıcı mekanik karşı basınç aniden kalkar",
                        "4. Gergin ve konjeste submukozal venler yırtılarak masif makroskopik hematüri (hematuria ex vacuo) gelişir"
                    ]
                ),
                make_cloze(
                    "Aşırı dolu mesanenin kateterle aniden boşaltılması sonucu lümendeki basınç düşüşüyle gelişen mukoza kanamasına hematuria ex vacuo denir.",
                    "ex vacuo",
                    "Boşalmaya bağlı kanama Latince terimini yazınız"
                ),
                make_micro_quiz(
                    "Glob vezikale nedeniyle acil serviste üretral kateter takılan bir hastada 1400 ml idrar hızla boşaltıldıktan hemen sonra idrar torbasının parlak kırmızı kanla dolduğu görülüyor. Bu komplikasyonun gelişim mekanizması hangisidir?",
                    {
                        "A": "Böbrek taşının üreteri delmesi",
                        "B": "Ani basınç düşüşü ve vakum etkisiyle submukozal mesane venlerinin yırtılması (Hematuria ex vacuo)",
                        "C": "Hastada hemofili A hastalığı bulunması",
                        "D": "Prostat kanserinin aniden kemiğe metastaz yapması",
                        "E": "Kateter balonunun böbrek pelvisinde şişirilmesi"
                    },
                    "B",
                    {
                        "A": "Üreter taşının mesane boşalmasıyla ilgisi yoktur.",
                        "B": "Doğru cevap B'dir: Mesanenin ani boşaltılmasıyla tamponlayıcı basıncın kalkması 'hematuria ex vacuo' tablosuna yol açar.",
                        "C": "Hastanın primer sorunu pıhtılaşma defekti değildir.",
                        "D": "Ani metastaz kanama yapmaz.",
                        "E": "Üretral kateter mesanededir."
                    }
                )
            ],
            "spotPearls": [
                "Aşırı gergin mesanenin ani boşaltılması 'HEMATURİA EX VACUO' yapar.",
                "Ani basınç düşüşü konjeste submukozal venleri yırtarak kanatır.",
                "Komplikasyonu önlemek için mesane aralıklı klemplemeyle kademeli boşaltılmalıdır."
            ]
        }
    ]
    for idx, s in enumerate(raw):
        s["id"] = f"k1-11-s{idx+1:02d}"
        if "content" not in s:
            s["content"] = s.get("coreContent", {}).get("text", "")
        if "sourcePdf" not in s:
            s["sourcePdf"] = "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)"
        if "elements" not in s:
            s["elements"] = s.get("interactiveElements", [])
    return raw
