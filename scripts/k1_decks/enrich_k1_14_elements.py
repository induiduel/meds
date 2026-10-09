# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını garanti eder.
"""

from scripts.k1_14_deck_data.helpers import (
    make_branching_logic, make_causal_chain, make_table
)

def get_extra_branching():
    """Branching logic (klinik ve saha karar verme) oranını artırmak için hedeflenen slaytlara eklenecek ögeler."""
    return {
        3: make_branching_logic(
            "Bir sınır kenti devlet hastanesi acil servisine yüksek ateş, retroorbital ağrı, trombositopeni ve burun kanaması olan 2 göçmen hasta başvuruyor. Hastaların 3 gün önce Asya'dan geldiği öğreniliyor.",
            "Acil nöbetçi hekimi olarak ilk sistemik epidemiyolojik yaklaşımınız ne olmalıdır?",
            [
                {
                    "text": "Hastaları genel dahiliye servisinde 4 kişilik açık odaya yatırıp rutin tahlil istemek",
                    "outcome": "Ölümcül hata: Olası viral kanamalı ateş veya dang diğer hastalara ve personele bulaşabilir.",
                    "isCorrect": False
                },
                {
                    "text": "Hastaları derhal tek kişilik temas/damlacık izolasyon odasına almak, tam KKE giymek ve İl Sağlık Müdürlüğü Bulaşıcı Hastalıklar Birimine 24 saat içinde bildirim yapmak",
                    "outcome": "Kusursuz epidemiyolojik klinik karar: Nozokomiyal bulaş engellenir ve uluslararası sınır aşan sürveyans tetiklenir.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaları hastaneye almayıp geldikleri ülkeye geri göndermek",
                    "outcome": "Etik dışı ve yasa dışı: Kaçan hastalar şehirde kontrolsüz salgın başlatır.",
                    "isCorrect": False
                }
            ]
        ),
        7: make_branching_logic(
            "Bir üniversite kampüsünde 3 gün içinde 25 öğrencide benzer sarılık, bulantı, koyu renkli idrar ve karın ağrısı tablosu gelişiyor. Hastaların ortak noktasının ana yemekhane olduğu belirleniyor.",
            "Kampüs hekimi ve halk sağlığı timi olarak yemekhane yönetimine karşı ilk adımınız ne olmalıdır?",
            [
                {
                    "text": "Hepatit A şüphesiyle yemekhaneyi derhal geçici olarak kapatmak, tüm aşçı ve çalışanlardan dışkı ve seroloji örnekleri almak ve menüdeki çiğ salataları imha etmek",
                    "outcome": "Mükemmel filyasyon müdahalesi: Fekal-oral bulaş zinciri kırılır ve yeni vakaların çıkması önlenir.",
                    "isCorrect": True
                },
                {
                    "text": "Sadece hasta öğrencilere istirahat raporu verip yemekhanenin faaliyetine dokunmamak",
                    "outcome": "Ağır hata: Bulaş kaynağı aktif kalır ve yüzlerce öğrenci daha enfekte olur.",
                    "isCorrect": False
                },
                {
                    "text": "Yemekhanedeki yemeklere yüksek dozda sirke katılarak servise devam edilmesini istemek",
                    "outcome": "Tıbbi değeri olmayan tehlikeli bir yaklaşımdır.",
                    "isCorrect": False
                }
            ]
        ),
        13: make_branching_logic(
            "Tarım ve Orman Bakanlığı veteriner hekimleri, bir ilçedeki göçmen kuş sulak alanında kitlesel yabani ördek ölümleri tespit ediyor. Numunelerde yüksek patojenik H5N1 kuş gribi virüsü doğrulanıyor.",
            "Tek Sağlık (One Health) protokolü gereğince İl Sağlık Müdürlüğü'nün atacağı ilk proaktif adım ne olmalıdır?",
            [
                {
                    "text": "Kuş ölümleriyle hekimlerin ilgilenmesine gerek olmadığını belirterek beklemek",
                    "outcome": "Körlük: Zoonotik sıçrama gerçekleştiğinde insanlar ölmeye başlar.",
                    "isCorrect": False
                },
                {
                    "text": "Sulak alan çevresindeki 5 km yarıçaptaki tüm tavuk çiftliklerini karantinaya almak, çiftlik çalışanlarını semptom açısından günlük taramaya almak ve profilaktik antiviral stoklarını hazır tutmak",
                    "outcome": "Mükemmel Tek Sağlık iş birliği: İnsana sıçrama riski erken evrede bloke edilir.",
                    "isCorrect": True
                },
                {
                    "text": "İlçedeki tüm su şebekesini 1 ay süreyle tamamen kesmek",
                    "outcome": "Gereksiz ve felç edici bir tedbirdir.",
                    "isCorrect": False
                }
            ]
        ),
        17: make_branching_logic(
            "Acil servise getirilen 28 yaşındaki bir dağcıda yüksek ateş, bilinç bulanıklığı ve ense sertliği saptanıyor. Hastanın 4 gün önce kırsal alanda piknik yaptığı ve vücudundan kene kopardığı öğreniliyor.",
            "Klinisyen olarak ilk tanısal ve terapötik önceliğiniz ne olmalıdır?",
            [
                {
                    "text": "Kenenin önemsiz olduğunu söyleyip hastayı psikiyatriye sevk etmek",
                    "outcome": "Ölümcül hata: Kene kaynaklı ensefalit veya KKKA atlanır.",
                    "isCorrect": False
                },
                {
                    "text": "KKKA ve Kene Kaynaklı Ensefalit (TBE) ön tanılarıyla tam kan, karaciğer enzimleri ve koagülasyon paneli istemek, kanamalı ateş KKE'si giyerek hastayı izole etmek ve destek tedavi başlamak",
                    "outcome": "Doğru klinik refleks: Uyanık klinisyen yaklaşımı hastanın hayatını kurtarır ve personeli korur.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaya hemen canlı virüs aşısı uygulamak",
                    "outcome": "Kontrendike: Akut enfeksiyonda aşı yapılmaz.",
                    "isCorrect": False
                }
            ]
        ),
        23: make_branching_logic(
            "Bir ilçede ilk kez tespit edilen bir solunum yolu virüsü vakası (örneğin MERS-CoV) sonrası filyasyon ekibi görevlendiriliyor. Hastanın temas ettiği 18 kişi tespit ediliyor.",
            "Salgının 'Giriş ve Lokal Yayılım' fazında sınırlama (containment) başarısı için temaslılara ne yapılmalıdır?",
            [
                {
                    "text": "Semptom çıkmasını beklemeden tüm temaslıları evlerinde 14 gün karantinaya almak, günlük semptom/ateş takibi yapmak ve pozitifleşeni anında izole etmek",
                    "outcome": "Kusursuz sınırlama stratejisi: Patojenin üçüncü şahıslara yayılması engellenerek salgın odakta boğulur.",
                    "isCorrect": True
                },
                {
                    "text": "Temaslılara maske verip normal işlerine gitmelerini söylemek",
                    "outcome": "Sınırlama çöker: Amplifikasyon fazı başlar.",
                    "isCorrect": False
                },
                {
                    "text": "Temaslıların tamamına rutin geniş spektrumlu antibiyotik başlamak",
                    "outcome": "Etkisiz: Viral etkene antibiyotik etki etmez ve direnç gelişir.",
                    "isCorrect": False
                }
            ]
        ),
        27: make_branching_logic(
            "Bir metropolde yeni bir influenza varyantı nedeniyle hastanelerin yoğun bakım doluluk oranı %95'e ulaşıyor. Salgın 'Amplifikasyon' fazındadır.",
            "Halk sağlığı kriz komitesinin bu aşamadaki birincil stratejik hedefi ne olmalıdır?",
            [
                {
                    "text": "Hala tek tek filyasyonla her temaslıyı izole etmeye çalışmak",
                    "outcome": "Artık geç kalınmıştır: Kaynaklar tükenir ve sağlık sistemi çöker.",
                    "isCorrect": False
                },
                {
                    "text": "Kontrol ve Etkiyi Azaltma (Mitigation) stratejisine geçerek kitlesel toplanmaları kısıtlamak, triyajı sıkılaştırmak, elektif ameliyatları erteleyip yoğun bakım kapasitesini artırmak",
                    "outcome": "En doğru faz müdahalesi: Salgın eğrisi düzleştirilir (flatten the curve) ve önlenebilir ölümler engellenir.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaneleri tamamen kapatıp hastaların evde beklemesini emretmek",
                    "outcome": "Yıkıcı felaket: Binlerce insan evde hipoksiden hayatını kaybeder.",
                    "isCorrect": False
                }
            ]
        ),
        33: make_branching_logic(
            "Türkiye'de son yerli polio (çocuk felci) vakası 1998'de görülmüş ve 2002'de DSÖ Avrupa Bölgesi ile birlikte 'Polio-Free' (Poliodan Arındırılmış) eliminasyon sertifikası alınmıştır.",
            "Komşu bir ülkede savaş nedeniyle aşılama çöküp polio salgını başladığında, Türkiye'de Sağlık Bakanlığı'nın tutumu ne olmalıdır?",
            [
                {
                    "text": "'Biz zaten elimine ettik' diyerek çocukluk çağı polio aşılamasını tamamen durdurmak",
                    "outcome": "Epidemiyolojik felaket: İthal virüs duyarsızlaşan Türk çocuklarında hızla yeni salgın yapar.",
                    "isCorrect": False
                },
                {
                    "text": "Eliminasyonun bölgesel olduğunu bilerek sınır illerinde ek doz aşılama kampanyaları yapmak, atık su ve AFP (Akut Flask Paralizi) sürveyansını en üst düzeye çıkarmak",
                    "outcome": "Kusursuz eliminasyon koruma refleksi: Dışarıdan gelecek virüs aşılı toplum duvarına çarparak söner.",
                    "isCorrect": True
                },
                {
                    "text": "Yalnızca sınır kapılarını kapatıp aşı takvimini değiştirmemek",
                    "outcome": "Yetersiz: Kaçak geçişler ve inkübasyondaki vakalar aşı açığı olan bölgelerde yayılır.",
                    "isCorrect": False
                }
            ]
        ),
        37: make_branching_logic(
            "Küresel bir patojenin eradikasyonu hedeflenirken araştırma ekibi patojenin doğada kemirgenler ve yaban domuzlarında da asemptomatik taşıyıcılık yaptığını saptıyor.",
            "Bu keşif sonrası küresel eradikasyon hedefi için bilimsel yargınız ne olmalıdır?",
            [
                {
                    "text": "Eradikasyon hedefi aynen sürdürülebilir, hiçbir değişiklik gerekmez",
                    "outcome": "Bilimsel yanılgı: Hayvan rezervuarı olan bir patojeni yeryüzünden silmek imkansızdır.",
                    "isCorrect": False
                },
                {
                    "text": "Doğal hayvan rezervuarı varlığı nedeniyle küresel eradikasyonun biyolojik olarak imkansız olduğu kabul edilmeli; hedef 'bölgesel kontrol ve eliminasyon' olarak revize edilmelidir",
                    "outcome": "Mükemmel epidemiyolojik muhakeme: Patojen doğada hayvanlarda saklandığı sürece küresel eradikasyon sağlanamaz.",
                    "isCorrect": True
                },
                {
                    "text": "Yeryüzündeki tüm kemirgen ve domuzları zehirleyerek öldürmek",
                    "outcome": "Ekolojik intihar ve pratik olarak imkansızdır.",
                    "isCorrect": False
                }
            ]
        ),
        63: make_branching_logic(
            "Bir pandemi hastanesinde KKE tedarik zinciri aksıyor ve N95 maske stoku tükenmek üzere kalıyor. Başhekimlik acil toplantı yapıyor.",
            "Personeli korumak ve hizmeti sürdürmek için en doğru kriz yönetimi adımı hangisidir?",
            [
                {
                    "text": "Hekimlerin maskesiz çalışmasını emretmek",
                    "outcome": "Kabul edilemez mesleki cinayet: Onlarca hekim enfekte olur ve hastane kapanır.",
                    "isCorrect": False
                },
                {
                    "text": "ASOM ve İl Sağlık rezervinden acil KKE sevkiyatı istemek; bu sırada N95 maskeleri sadece entübasyon ve bronkoskopi gibi aerosol üreten işlemlere tahsis edip diğer alanlarda cerrahi maske kullanmak",
                    "outcome": "Mükemmel risk triyajı ve lojistik koordinasyon: Sağlık personeli korunur ve kaynak akılcı yönetilir.",
                    "isCorrect": True
                },
                {
                    "text": "Tüm hastaları sokağa bırakıp hastaneyi kilitlemek",
                    "outcome": "Kaos ve cezai sorumluluk doğurur.",
                    "isCorrect": False
                }
            ]
        ),
        73: make_branching_logic(
            "Bir köyde hayvan kesimi yapan bir kasap ve çırağında kesimden 3 gün sonra ani başlayan titreme, ateş ve burun kanaması gelişiyor. Hastaların kene tutunması öyküsü yok.",
            "Hekim olarak bulaş yolu ve enfeksiyon kaynağı hakkındaki kararınız ne olmalıdır?",
            [
                {
                    "text": "Kene tutunmadığı için KKKA kesinlikle dışlanır, hastalar üşütmüştür",
                    "outcome": "Ölümcül yanılgı: KKKA sadece kene ısırmasıyla değil, viremik hayvanın taze kan ve dokularıyla doğrudan temasla da bulaşır!",
                    "isCorrect": False
                },
                {
                    "text": "Viremik hayvan kanı ve dokusuyla temas yoluyla bulaşan KKKA ön tanısıyla hastaları derhal izole etmek, destek tedaviye başlamak ve kesilen hayvanın sürü temaslılarını incelemek",
                    "outcome": "Kusursuz klinik tanı: KKKA'nın hayvan dokusuyla temasla bulaşabilme gerçeği hayat kurtarır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaları doğrudan psikiyatri kliniğine yönlendirmek",
                    "outcome": "Ağır tıbbi ihmal.",
                    "isCorrect": False
                }
            ]
        ),
        83: make_branching_logic(
            "Bir göçmen kampında 2 çocukta laboratuvar onaylı çiçek benzeri Mpox (Maymun Çiçeği) lezyonları saptanıyor. Elinizde yalnızca 300 doz aşı stoku bulunmaktadır.",
            "Bu sınırlı kaynakla salgını yayılmadan durdurmak için hangi aşılama stratejisini tercih edersiniz?",
            [
                {
                    "text": "300 dozu kamptaki rastgele kişilere çekilişle dağıtmak",
                    "outcome": "Etkisiz: Bulaş zinciri kırılmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Halka Aşılama (Ring Vaccination) uygulayarak hastaların aile bireylerini, yakın temaslılarını ve kamp sağlık görevlilerini öncelikle aşılamak",
                    "outcome": "Mükemmel stratejik halk sağlığı kararı: Virüsün sıçrayacağı temas halkası kapatılarak salgın odakta boğulur.",
                    "isCorrect": True
                },
                {
                    "text": "Aşıların tamamını imha edip herkesi kaderine bırakmak",
                    "outcome": "Mantık dışı.",
                    "isCorrect": False
                }
            ]
        ),
        87: make_branching_logic(
            "Bir ilçede dini ve kültürel gerekçelerle aşı reddi yapan 150 ailenin çocuklarının gittiği özel bir okulda boğmaca ve kızamık vakaları görülmeye başlanıyor.",
            "İlçe Sağlık Müdürü olarak toplum sağlığını korumak için en etkili hukuki ve etik hamleniz ne olmalıdır?",
            [
                {
                    "text": "Okulu hiçbir tedbir almadan açık tutmak",
                    "outcome": "Bebek ölümlerine yol açar.",
                    "isCorrect": False
                },
                {
                    "text": "Umumi Hıfzıssıhha Kanunu gereğince salgın sönümlenene kadar aşısız temaslı öğrencilerin okula devamını geçici olarak kısıtlamak, yerel kanaat önderleriyle ailelere yönelik bilgilendirme ve aşı ikna seansları düzenlemek",
                    "outcome": "Mükemmel denge: Siracusa ilkelerine uygun, orantılı, meşru ve toplum sağlığını koruyan karardır.",
                    "isCorrect": True
                },
                {
                    "text": "Aileleri vatan hainliğiyle suçlayıp hapse attırmak",
                    "outcome": "Hukuka aykırı ve toplumsal direnci artıran felaket hamlesidir.",
                    "isCorrect": False
                }
            ]
        ),
        95: make_branching_logic(
            "Uzak Doğu'da vahşi hayvan pazarından kaynaklanan ve daha önce tıp literatüründe tanımlanmamış yeni bir RNA virüsü 5 günde 20 kişiyi solunum yetmezliğinden öldürüyor. DSÖ alarm durumuna geçiyor.",
            "Bu 'Hastalık X' tablosu karşısında ulusal sağlık otoritesinin ilk 72 saatteki proaktif önlemi ne olmalıdır?",
            [
                {
                    "text": "Virüsün adı bilinmediği için resmi olarak varlığını inkar etmek",
                    "outcome": "Tarihi skandal: Virüs sessizce tüm kıtaya yayılır.",
                    "isCorrect": False
                },
                {
                    "text": "Hastalık X protokolünü aktive etmek; moleküler tanı laboratuvarlarına genomik dizileme talimatı vermek, sınır kapılarında termal ve semptom triyajı başlatmak ve hastanelerde solunum izolasyon yataklarını rezerve etmek",
                    "outcome": "Kusursuz proaktif hazırlık: Bilinmeyen patojene karşı esnek savunma kalkanı dakikalar içinde kurulur.",
                    "isCorrect": True
                },
                {
                    "text": "Halka virüsün zararsız olduğunu söyleyip maske takılmasını yasaklamak",
                    "outcome": "Kitlesel ölümlere davetiye çıkarır.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_chains():
    """Causal chain oranını artırmak için hedeflenen slaytlara eklenecek zincirler."""
    return {
        8: make_causal_chain(
            "Küresel Seyahat ve Patojenin Yayılma Zinciri",
            [
                "1. Yerel Bulaş: Virüs kırsal bir bölgede ilk insanı enfekte eder.",
                "2. Asemptomatik Uçuş: Kuluçka dönemindeki yolcu kıtalararası uçağa biner.",
                "3. Küresel Hub İnişi: 12 saat içinde dünyanın öbür ucundaki metropol havalimanına ulaşır.",
                "4. Çok Odaklı Toplum Bulaşı: Kişi semptomsuzken onlarca temaslıya patojeni aktarır."
            ]
        ),
        18: make_causal_chain(
            "Klinisyenin Uyanıklığıyla Salgını Durdurma Zinciri",
            [
                "1. Klinik Şüphe: Hekim alışılmadık kanamalı ateşi olan hastada endemik olmayan patojenden şüphelenir.",
                "2. İzolasyon Hamlesi: Hasta hemen tek kişilik odaya alınır ve sağlık personeline KKE giydirilir.",
                "3. Erken Sürveyans Bildirimi: İl Sağlık Müdürlüğü ve referans laboratuvar 2 saat içinde uyarılır.",
                "4. Filyasyon ve Sınırlama: Hastanın temaslıları aynı gün karantinaya alınarak salgın başlamadan söndürülür."
            ]
        ),
        28: make_causal_chain(
            "Salgın Eğrisini Düzleştirme (Flatten the Curve) Zinciri",
            [
                "1. Erken Toplumsal Kısıtlama: Okullar, etkinlikler ve kalabalık ortamlar sınırlandırılır.",
                "2. İletim Katsayısının Düşmesi: R0 ve Rt değeri 1'in altına doğru geriletilir.",
                "3. Zirve Vaka Sayısının Yayılması: Günlük hasta akışı sağlık sisteminin taşıma kapasitesinin altında tutulur.",
                "4. Sağlık Sisteminin Ayakta Kalması: Yoğun bakımlar tıkanmaz; hem salgın hem rutin hastalar tedavi edilir."
            ]
        ),
        68: make_causal_chain(
            "Birinci Basamak Filyasyon ve Temas Takip Zinciri",
            [
                "1. Pozitif Bildirim: Laboratuvar onaylı vaka filyasyon ekibinin tabletine düşer.",
                "2. Aile Hekimi/Ebe Teması: Ekip 6 saat içinde hastanın evine giderek klinik durumunu değerlendirir.",
                "3. Temas Haritası Çıkarma: Son 48 saatte temas edilen tüm akraba ve iş arkadaşları listelenir.",
                "4. Karantina ve İlaç Teslimi: Temaslılara evde karantina protokolü tebliğ edilir ve ilaçları elden verilir."
            ]
        ),
        84: make_causal_chain(
            "Halka Aşılama ile Salgın Odağını Söndürme Zinciri",
            [
                "1. Vaka İzolasyonu: İndeks vaka tespit edilir edilmez negatif basınçlı odaya alınır.",
                "2. Birinci Halka Tespiti: Hastayla aynı evde veya odada kalan doğrudan temaslılar belirlenir.",
                "3. Hızlı Aşılama: Birinci halkadaki kişilere temasın ilk 72 saatinde aşı uygulanır.",
                "4. İkinci Halka Kalkanı: Komşular ve çevre haneler aşılanarak virüsün gidebileceği tüm duyarlı kapılar kapatılır."
            ]
        ),
        96: make_causal_chain(
            "Uluslararası Sağlık Tüzüğü (UST/IHR) Küresel Yanıt Zinciri",
            [
                "1. Ulusal Olay Tespiti: Ülkedeki ASOM olağan dışı ölüm kümelenmesini doğrular.",
                "2. 24 Saat İçinde DSÖ Bildirimi: UST Odak Noktası (National Focal Point) DSÖ'ye resmi rapor sunar.",
                "3. PHEIC Değerlendirmesi: DSÖ Genel Direktörü Acil Durum Komitesini toplayarak küresel acil durum ilan eder.",
                "4. GOARN ve Küresel Seferberlik: Sınır kapısı önlemleri, aşı dağıtımı ve uzman desteği dünyaya duyurulur."
            ]
        )
    }

def get_extra_tables():
    """Interactive table oranını artırmak için hedeflenen slaytlara eklenecek tablolar."""
    return {
        14: make_table(
            ["Sektör", "Salgındaki Görevi", "Aksarsa Oluşacak Risk"],
            [
                ["Sağlık Bakanlığı", "Klinik triyaj, filyasyon, sürveyans, aşılama", "Vaka ve ölümlerin patlaması, sistemin çöküşü"],
                ["Tarım ve Orman", "Zoonotik hayvan sürveyansı, çiftlik karantinası", "Hayvandan insana sürekli yeni virüs sıçraması"],
                ["Çevre ve Şehircilik", "Tıbbi atık imhası, su kaynaklarının korunması", "Atıklardan ve derelerden ikinci dalga bulaşı"],
                ["İçişleri ve Yerel Yönetim", "Karantina güvenliği, defin, temiz su temini", "Toplumsal kargaşa, cenaze bulaşları ve susuzluk"]
            ]
        ),
        74: make_table(
            ["Patojen", "Bulaş Rotası", "Kritik Klinik Özellik", "Temel Önleme Hamlesi"],
            [
                ["Vibrio cholerae", "Su (Fekal-oral)", "Pirinç suyu diyare, hızlı şok", "0.5 mg/L klorlama ve ORS"],
                ["Polio Virüs", "Fekal-oral", "Flask paralizi, motor nöron hasarı", "OPV/IPV rutin aşılaması"],
                ["Shigella dysenteriae", "Gıda (Fekal-oral)", "Kanlı-mukuslu diyare, tenesmus", "El hijyeni ve gıda sanitasyonu"],
                ["Kızamık Virüsü", "Solunum (Aerosol)", "Koplik lekesi, makülopapüler döküntü", "%95 KKK aşı duvarı"]
            ]
        )
    }

def enrich_slides(slides):
    """Slayt listesini alır ve eklenen elemanlarla zenginleştirip dengeli olarak geri döndürür."""
    branching_map = get_extra_branching()
    chain_map = get_extra_chains()
    table_map = get_extra_tables()

    for idx, slide in enumerate(slides, start=1):
        if idx in branching_map:
            slide["elements"].append(branching_map[idx])
        if idx in chain_map:
            slide["elements"].append(chain_map[idx])
        if idx in table_map:
            slide["elements"].append(table_map[idx])

    return slides
