# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)
İnteraktif Eleman Zenginleştirme ve %8 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 (hedef %10-20) oranına ulaşmasını sağlar.
"""

from scripts.k1_16_deck_data.helpers import (
    make_branching_logic, make_active_recall
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar verme) oranını artırmak için eklenecek ögeler."""
    return {
        2: make_branching_logic(
            "Acil servise aşırı kusma ve ishal nedeniyle getirilen 40 yaşındaki dehidrate hastada toplam vücut sıvısının ve kompartmanlarının durumu değerlendiriliyor.",
            "Bu hastada sıvı kaybının ilk nereden karşılandığı ve kompartmanlar arası geçiş hekim tarafından nasıl yorumlanmalıdır?",
            [
                {
                    "text": "Sıvı kaybı doğrudan ve sadece hücrelerin içinden gerçekleşir, damar içi plazma hacmi hiç etkilenmez.",
                    "outcome": "Hatalı fizyoloji: Sıvı öncelikle ekstrasellüler alandan (intravasküler ve interstisyel) kaybedilir.",
                    "isCorrect": False
                },
                {
                    "text": "Kayıp öncelikle ekstrasellüler kompartmandan (plazma ve doku aralığı) olur; hacim düşüşü kompanse edilemezse ozmotik denge bozulup hücre içinden dışarıya su çekilmeye başlar.",
                    "outcome": "Kusursuz hemodinamik yaklaşım: Kompartmanlar arası Starling ve ozmotik su geçişi doğru kavranmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Toplam vücut suyunun %90'ı plazmada olduğu için hasta ilk dakikada tüm suyunu tüketmiştir.",
                    "outcome": "Bilim dışı oranlar ve hatalı bilgi.",
                    "isCorrect": False
                }
            ]
        ),
        5: make_branching_logic(
            "Göğüs travması geçiren bir hastanın torasik duktusu (duktus torasikus) rüptüre oluyor ve sol plevral boşlukta süt benzeri beyaz bir sıvı toplanıyor.",
            "Göğüs cerrahisi ekibi bu sıvının doğası ve lenfatik drenajla ilişkisi hakkında hangi kararı vermelidir?",
            [
                {
                    "text": "Bu pürülan bir bakteriyel absedir, hemen yüksek doz intravenöz antibiyotik başlanmalıdır.",
                    "outcome": "Hatalı tanı: Süt rengi sıvı şilomikron zengini lenf sıvısıdır (şilotorks), püy değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Bu sıvı duktus torasikus yaralanmasına bağlı lenf kaçağıdır (şilotoraks); diyetle yağ kısıtlanmalı, tüp torakostomi uygulanmalı ve gerekirse duktus cerrahi olarak bağlanmalıdır.",
                    "outcome": "Kusursuz klinik karar: Lenfatik sistemin ana gövdesi duktus torasikus rüptürü ve şilotoraks doğru yönetilir.",
                    "isCorrect": True
                },
                {
                    "text": "Hiçbir müdahaleye gerek yoktur, süt kıvamındaki lenf sıvısı akciğer dokusunu besler.",
                    "outcome": "Ölümcül kompresyon atelektazisine yol açacak ihmal.",
                    "isCorrect": False
                }
            ]
        ),
        8: make_branching_logic(
            "Nefes darlığı ile başvuran 55 yaşındaki hastanın plevra ponksiyonunda 1000 ml berrak sarı sıvı aspire ediliyor. Sıvı proteini 1.2 g/dL ve dansitesi 1.010 ölçülüyor.",
            "Sıvının analizini değerlendiren klinisyenin tanısal ve etiyolojik yaklaşımı ne olmalıdır?",
            [
                {
                    "text": "Sıvı yüksek proteinli bir eksudadır, tüberküloz plöriti veya akciğer kanseri aranmalıdır.",
                    "outcome": "Hatalı analiz: Protein <3.0 ve dansite <1.012 transudanın kesin göstergesidir.",
                    "isCorrect": False
                },
                {
                    "text": "Sıvı tipik bir hemodinamik transudadır; damar geçirgenlik artışı yoktur, öncelikle konjestif kalp yetmezliği, siroz veya nefrotik sendrom gibi hidrostatik/onkotik nedenler araştırılmalıdır.",
                    "outcome": "Kusursuz patolojik muhakeme: Transuda kriterleri ve etiyolojik köken eksiksiz eşleştirilmiştir.",
                    "isCorrect": True
                },
                {
                    "text": "Sıvı doğrudan mide suyudur, diyafram yırtılmıştır.",
                    "outcome": "Gerçek dışı iddia.",
                    "isCorrect": False
                }
            ]
        ),
        12: make_branching_logic(
            "Yarı maraton koşan 28 yaşındaki bir atlette yarış sırasında quadriceps kaslarında belirgin ısı artışı, kızarıklık ve doku gerginliği gözleniyor.",
            "Spor hekimliği stajyerinin bu vasküler tablonun mekanizması hakkındaki en doğru patofizyolojik yorumu ne olmalıdır?",
            [
                {
                    "text": "Bacakta venöz kan akımı tamamen durmuştur ve pasif bir konjesyon gelişmiştir.",
                    "outcome": "Hatalı yorum: Koşan kasta venöz drenaj aksamaz, arteriyel giriş patlaması olur.",
                    "isCorrect": False
                },
                {
                    "text": "Artan kas metabolitleri (NO, adenozin, laktat) arteriyolleri aktif olarak genişletmiş, kapiller debiyi katlayarak fizyolojik bir aktif hiperemi tablosu oluşturmuştur.",
                    "outcome": "Mükemmel fizyoloji ve patoloji sentezi: Egzersiz kasındaki aktif hiperemi doğru açıklanmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Kas dokusu nekroze olmuş ve kazeifiye olmuştur.",
                    "outcome": "Tüberküloz nekrozu ile ilgisiz bir durum.",
                    "isCorrect": False
                }
            ]
        ),
        15: make_branching_logic(
            "Sol bacağında aniden tek taraflı ağrılı şişlik, gerginlik ve hafif morarma gelişen 60 yaşındaki bir hastada derin ven trombozu (DVT) saptanıyor.",
            "Acil nöbetçi hekiminin bu tablonun hemodinamik karakteri ve acil komplikasyonu hakkındaki kararı ne olmalıdır?",
            [
                {
                    "text": "Bu durum aktif bir hiperemidir, bacağa sıcak kompres uygulanarak hasta yürütülmelidir.",
                    "outcome": "Ölümcül hata: Sıcak kompres ve yürütmek pıhtıyı kopararak fatal pulmoner emboli yapar.",
                    "isCorrect": False
                },
                {
                    "text": "Bu tablo lokal venöz drenaj bozukluğuna bağlı pasif bir konjesyondur; hasta yatak istirahatine alınmalı, bacak eleve edilmeli ve masif pulmoner emboli riskine karşı acil antikoagülan başlanmalıdır.",
                    "outcome": "Kusursuz klinik ve patolojik karar: Venöz konjesyon doğası ve pulmoner emboli koruması doğru uygulanır.",
                    "isCorrect": True
                },
                {
                    "text": "Ödem sadece böbrek yetmezliğinden kaynaklanmaktadır, diyalize alınmalıdır.",
                    "outcome": "Asimetrik tek bacak ödeminde renal yetmezlik primer neden değildir.",
                    "isCorrect": False
                }
            ]
        ),
        18: make_branching_logic(
            "Kronik venöz yetmezliği olan 70 yaşındaki hastanın ayak bileği medial malleol çevresinde koyu kahverengi-pas rengi geniş lekeler ve bacakta ödem saptanıyor.",
            "Deri biyopsisinde izlenen bu renk değişiminin hücresel kaynağı hakkında patoloğun raporu ne olmalıdır?",
            [
                {
                    "text": "Ciltte melanositlerin malign proliferasyonu sonucu yaygın melanom gelişmiştir.",
                    "outcome": "Hatalı onkolojik tanı: Konjestif staz lekesi melanom değildir.",
                    "isCorrect": False
                },
                {
                    "text": "Yüksek venöz hidrostatik basınçla rüptüre olan kapillerlerden sızan eritrositlerin doku makrofajlarınca fagositozu sonucu yoğun hemosiderin pigmenti birikmiştir (staz dermatiti).",
                    "outcome": "Kusursuz patoloji analizi: Kronik konjesyonda kapiller rüptürü ve hemosiderin depolanması doğru tanımlanmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Deriye dışarıdan bulaşan endüstriyel boya maddesidir.",
                    "outcome": "Bilimsel olmayan yorum.",
                    "isCorrect": False
                }
            ]
        ),
        22: make_branching_logic(
            "Akut miyokard enfarktüsü geçiren 65 yaşındaki hasta aniden şiddetli nefes darlığı, ortopne ve ağzından pembe köpüklü balgam çıkarma şikayetiyle fenalaşıyor.",
            "Kardiyoloji yoğun bakım ekibinin bu acil tablonun patolojisi hakkındaki en doğru değerlendirmesi hangisidir?",
            [
                {
                    "text": "Hastada akciğer kanseri bronşu tıkamıştır, acil bronkoskopi yapılmalıdır.",
                    "outcome": "Hatalı yönelim: Akut pembe köpük sol kalp yetmezliğine bağlı akut akciğer ödemidir.",
                    "isCorrect": False
                },
                {
                    "text": "Sol ventrikül pompasının çökmesiyle pulmoner venöz hidrostatik basınç aniden fırlamış, alveoller köpüklü transuda ve mikro-kanama sıvısıyla dolmuştur (akut kardiyojenik akciğer ödemi).",
                    "outcome": "Kusursuz patolojik muhakeme: Sol kalp yetmezliği ve akut akciğer ödemi mekanizması tam kavranmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastanın midesi delinmiş ve asit akciğere kaçmıştır.",
                    "outcome": "Anatomik ve klinik olarak uyumsuz iddia.",
                    "isCorrect": False
                }
            ]
        ),
        24: make_branching_logic(
            "Kronik sol kalp yetmezliği olan bir hastanın balgam yaymasında sitopatoloji uzmanı sitoplazmasında altın-kahverengi granüller bulunan çok sayıda iri mononükleer hücre görüyor. Prusya mavisi boyası pozitif reaksiyon veriyor.",
            "Asistan hekime bu hücrelerin kimliği ve anlamı hakkında verilecek en doğru bilgi hangisidir?",
            [
                {
                    "text": "Bu hücreler malign adenokarsinom hücreleridir, hasta acilen kemoterapiye verilmelidir.",
                    "outcome": "Vahim tanı hatası: Prusya mavisi pozitif hücreler malignite değil hemosiderindir.",
                    "isCorrect": False
                },
                {
                    "text": "Bu hücreler alveol içine sızan eritrositleri yutmuş 'kalp yetmezliği hücreleri'dir (hemosiderin yüklü makrofajlar / siderofajlar) ve kronik pulmoner konjesyonun kanıtıdır.",
                    "outcome": "Kusursuz sitopatolojik teşhis: Kalp yetmezliği hücreleri ve siderofaj kimliği tam olarak açıklanmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Bu hücreler akciğer surfaktanını üreten Tip II pnömositlerdir, kalp yetmezliğiyle ilişkisizdir.",
                    "outcome": "Tip II pnömositler hemosiderin depolamaz.",
                    "isCorrect": False
                }
            ]
        ),
        26: make_branching_logic(
            "Otopsi yapılan 72 yaşındaki kronik konjestif kalp yetmezliği hastasının karaciğer kesitinde lobül merkezlerinin kırmızı-kahverengi çökük, periportal alanların ise açık sarımsı renkte olduğu alacalı 'muskat karaciğeri' manzarası izleniyor.",
            "Patoloji asistanının bu alacalı görünümün zonal biyolojisi hakkındaki en doğru çıkarımı ne olmalıdır?",
            [
                {
                    "text": "Tüm karaciğer eşit derecede etkilenmiştir, renk farkı ışıktan kaynaklanmaktadır.",
                    "outcome": "Hatalı patoloji yorumu: Lobül zonlarının oksijenlenme farkı belirleyicidir.",
                    "isCorrect": False
                },
                {
                    "text": "Lobül merkezi (Zon 3) hipoksiye en duyarlı bölge olduğu için konjesyon ve hepatosit nekrozuyla kırmızı çökerken; arteriyole yakın periportal Zon 1 canlı kalarak yağlanma (steatoz) gösterir.",
                    "outcome": "Mükemmel patolojik muhakeme: Rappaport asinüs Zon 3 nekrozu ve Zon 1 steatozu muskat görünümünü açıklar.",
                    "isCorrect": True
                },
                {
                    "text": "Sarı alanlar safra kanalı kanseridir, kırmızı alanlar ise tamamen normal dokudur.",
                    "outcome": "Kanserle ilişkisiz klasik konjestif hepatik lezyon.",
                    "isCorrect": False
                }
            ]
        ),
        28: make_branching_logic(
            "Yıllardır konstriktif perikardit ve ağır sağ kalp yetmezliği olan hastada karaciğer biyopsisinde sentrosantral fibröz köprüler ve yaygın nodüler sertleşme saptanıyor. Viral ve otoimmün paneller negatiftir.",
            "Klinik patoloji konseyinde bu karaciğer tablosunun kesin tanısı ne olarak konulmalıdır?",
            [
                {
                    "text": "Primer sklerozan kolanjit",
                    "outcome": "Yanlış tanı: Safra yolları tutulumu ve soğan zarı fibrozisi yoktur.",
                    "isCorrect": False
                },
                {
                    "text": "Kardiyak siroz (kardiyak skleroz)",
                    "outcome": "Kusursuz teşhis: Kronik sağ kalp yetmezliğine ikincil gelişen sentrilobüler kaynaklı siroz tablosu doğru konulmuştur.",
                    "isCorrect": True
                },
                {
                    "text": "Wilson hastalığı",
                    "outcome": "Wilson bakır birikim hastalığıdır, kardiyak yetmezlikle doğrudan ilişkisizdir.",
                    "isCorrect": False
                }
            ]
        ),
        33: make_branching_logic(
            "Ortopedi servisinde kalça protezi ameliyatı sonrası 5. gününde sağ bacağı belirgin şişen ve homans bulgusu pozitif olan hastada Doppler USG ile femoral vende akut DVT kanıtlanıyor.",
            "Bu hastada ödemin yayılmasını ve fatal komplikasyonu önlemek için izlenecek en doğru strateji nedir?",
            [
                {
                    "text": "Ödemli bacağa sert masaj yaparak pıhtının dağılmasını sağlamak",
                    "outcome": "Ölümcül hata: Masaj trombüsü koparıp fatal pulmoner emboli yaratır.",
                    "isCorrect": False
                },
                {
                    "text": "Hastayı hemen mobilize etmemek, düşük molekül ağırlıklı heparin (antikoagülasyon) başlamak ve venöz dönüşü rahatlatıcı tedbirler almak",
                    "outcome": "Kusursuz klinik yaklaşım: Trombüs büyümesi durdurulur ve pulmoner emboli engellenir.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaya yüksek doz su içirip hiçbir ilaç vermemek",
                    "outcome": "Trombüsü tedavi etmeyen tehlikeli yaklaşım.",
                    "isCorrect": False
                }
            ]
        ),
        35: make_branching_logic(
            "Konjestif kalp yetmezliği olan bir hastada kardiyak debi düşüşüne yanıt olarak böbreklerin aşırı renin salgıladığı ve aldosteronun sodyum tuttuğu saptanıyor.",
            "Kardiyoloğun bu hastaya ACE inhibitörü (kaptopril vb.) ve aldosteron antagonisti (spironolakton) reçete etmesinin temel patofizyolojik amacı nedir?",
            [
                {
                    "text": "Hastanın idrar yapmasını tamamen durdurup suyu damarda tutmak",
                    "outcome": "Tam tersi: Amaç sodyum ve su atılımını sağlamaktır.",
                    "isCorrect": False
                },
                {
                    "text": "RAAS kaskadını bloke ederek böbreğin sodyum ve su tutmasını engellemek, venöz aşırı yüklenmeyi (preload) azaltarak ödem kısır döngüsünü kırmak",
                    "outcome": "Kusursuz farmakolojik ve patolojik mantık: Sekonder hiperaldosteronizmin kısır döngüsü hedeflenir.",
                    "isCorrect": True
                },
                {
                    "text": "Kalp kasını doğrudan uyarıp kasılma hızını 200'e çıkarmak",
                    "outcome": "ACE inhibitörleri pozitif inotrop veya taşikardik ajan değildir.",
                    "isCorrect": False
                }
            ]
        ),
        38: make_branching_logic(
            "Yatağa bağımlı serebrovasküler inme hastasını vizitte muayene eden intörn hekim 'Hastanın ayak bileklerinde ödem yok, o yüzden kalp yetmezliği bulunmuyor' diyor.",
            "Kıdemli uzman hekimin intörne yerçekimi ve bağımlı ödem hakkında vereceği en doğru eğitim uyarısı ne olmalıdır?",
            [
                {
                    "text": "'Haklısın, kalp yetmezliği ödemi daima sadece ayak bileklerinde görülür.'",
                    "outcome": "Hatalı klinik değerlendirme: Yatan hastada sıvı sakruma çöker.",
                    "isCorrect": False
                },
                {
                    "text": "'Yanılıyorsun; yerçekimi sıvıyı en altta kalan bölgeye çeker. Yatan hastada bacaklar ince kalabilir ancak sıvı presakral bölgede ve uyluk arkasında göllenir; mutlaka presakral gode aranmalıdır.'",
                    "outcome": "Mükemmel klinik muayene eğitimi: Bağımlı (dependent) ödemin pozisyona göre yer değiştirmesi tam kavranır.",
                    "isCorrect": True
                },
                {
                    "text": "'Ödem sadece kafatasında aranmalıdır.'",
                    "outcome": "Anlamsız ve bilim dışı iddia.",
                    "isCorrect": False
                }
            ]
        ),
        43: make_branching_logic(
            "Dört yaşında bir çocukta sabahları belirginleşen göz kapağı şişliği (periorbital ödem) ve idrar tahlilinde 4+ proteinüri (>4 g/gün) saptanıyor. Tansiyon ve böbrek fonksiyonları normaldir.",
            "Pediatri uzmanının bu sendromun patolojisi ve ilk basamak tedavisi hakkındaki kararı ne olmalıdır?",
            [
                {
                    "text": "Bu akut bir piyelonefrittir, hemen 3 hafta antibiyotik verilmelidir.",
                    "outcome": "Hatalı teşhis: Ağır proteinüri ve periorbital ödem enfeksiyon değil nefrotik sendromdur.",
                    "isCorrect": False
                },
                {
                    "text": "Tablo Minimal Lezyon Hastalığına bağlı Nefrotik Sendromdur; podosit ayak silinmesi masif albümin kaçağına yol açmıştır; ilk tercih sistemik kortikosteroid tedavisidir.",
                    "outcome": "Kusursuz pediatrik nefroloji yaklaşımı: Minimal lezyon nefrotik sendromu ve steroid duyarlılığı doğru yönetilir.",
                    "isCorrect": True
                },
                {
                    "text": "Çocuğa bol tuzlu su içirilmelidir.",
                    "outcome": "Ödemi anasarkaya çevirecek ölümcül hata.",
                    "isCorrect": False
                }
            ]
        ),
        46: make_branching_logic(
            "Karaciğer sirozu zemininde gergin masif asiti olan ve nefes almakta zorlanan 58 yaşındaki hastaya acil serviste 6 litre terapötik parasentez (karından sıvı boşaltılması) yapılıyor.",
            "Gastroenteroloji ekibinin parasentez sırasında hastaya intravenöz albümin infüzyonu vermesinin temel fizyolojik nedeni nedir?",
            [
                {
                    "text": "Albüminin karındaki delikten dışarı akmasını sağlamak",
                    "outcome": "Mantıksız ve hatalı yorum.",
                    "isCorrect": False
                },
                {
                    "text": "Karın içi basıncın aniden düşmesiyle splanknik damarlarda kan göllenmesini ve intravasküler plazma hacminin çökerek parazentez sonrası dolaşım disfonksiyonu (şok ve böbrek yetmezliği) gelişmesini önlemek",
                    "outcome": "Kusursuz hemodinamik yönetim: Sirozda onkotik basınç desteği ve dolaşım çöküşü önlenir.",
                    "isCorrect": True
                },
                {
                    "text": "Hastada iştah açmak",
                    "outcome": "Albümin iştah açıcı değildir.",
                    "isCorrect": False
                }
            ]
        ),
        48: make_branching_logic(
            "Serum albümini 1.6 g/dL olan nefrotik sendromlu bir hastaya kontrolsüz biçimde yüksek doz intravenöz furosemid (güçlü kıvrım diüretik) veriliyor.",
            "Bu hastada ödem gerilerken aynı zamanda kreatinin düzeyinin hızla yükselmesi ve tansiyonun 70/40 mmHg'ye düşmesi nasıl açıklanır?",
            [
                {
                    "text": "Diüretik böbrekleri parçalamıştır.",
                    "outcome": "Yetersiz ve popüler açıklama.",
                    "isCorrect": False
                },
                {
                    "text": "Hipoalbüminemide damar içi efektif hacim zaten kritik düşüktür; agresif diürezle kalan damar içi sıvı da atılınca hasta prerenal azotemiye ve hipovolemik şoka girmiştir.",
                    "outcome": "Mükemmel patofizyolojik muhakeme: Hipoalbüminemide damar içi susuzluk paradoksu doğru anlaşılmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Hasta gizlice zehirli mantar yemiştir.",
                    "outcome": "Klinik bağlamla ilgisiz iddia.",
                    "isCorrect": False
                }
            ]
        ),
        52: make_branching_logic(
            "Güneydoğu Asya seyahatinden dönen 35 yaşındaki bir hastada sağ bacakta ve skrotumda devasa boyutlara ulaşan, derisi kalınlaşmış ve çatlaklı bir şişlik (fil hastalığı) saptanıyor.",
            "Enfeksiyon hastalıkları uzmanının etiyoloji ve patogenez hakkındaki en doğru açıklaması hangisidir?",
            [
                {
                    "text": "Bu durum basit bir mantar enfeksiyonudur, topikal krem yeterlidir.",
                    "outcome": "Yetersiz tanı: Masif elefantiyazis yüzeyel mantarla açıklanamaz.",
                    "isCorrect": False
                },
                {
                    "text": "Wuchereria bancrofti parazitlerinin inguinal lenf nodlarında oluşturduğu kronik lenfanjit ve fibröz obliterasyona bağlı obstrüktif masif lenfödemdir (filaryazis).",
                    "outcome": "Kusursuz parazitoloji ve patoloji teşhisi: Filaryazis ve elefantiyazis patogenezi tam olarak kavranmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Bacak kemiklerinde primer osteosarkom gelişmiştir.",
                    "outcome": "Tümör dokusu ile paraziter lenfödem tamamen farklıdır.",
                    "isCorrect": False
                }
            ]
        ),
        54: make_branching_logic(
            "Sağ meme kanseri nedeniyle modifiye radikal mastektomi ve aksiller lenf nodu diseksiyonu geçiren, ardından radyoterapi alan 50 yaşındaki bir kadının sağ kolunda kalıcı lenfödem gelişiyor.",
            "Cerrahi onkoloji polikliniğinde hastaya bu koldan kan alınmaması, tansiyon ölçülmemesi ve kesiklerden kaçınılması uyarısının temel nedeni nedir?",
            [
                {
                    "text": "Koldan kan alınırsa tüm kanserin anında geri nüksetmesi",
                    "outcome": "Bilimsel olmayan gerekçe.",
                    "isCorrect": False
                },
                {
                    "text": "Lenfatik drenajı bozulmuş ve protein göllenen bu kolun lokal immün savunmasının zayıf olması; en ufak yara veya ponksiyondan şiddetli bakteriyel lenfanjit/selülit gelişebilmesi",
                    "outcome": "Kusursuz cerrahi ve immünolojik yaklaşım: Lenfödemli dokunun enfeksiyona aşırı yatkınlığı doğru yönetilir.",
                    "isCorrect": True
                },
                {
                    "text": "Kolun hemen amputasyon gerektirmesi",
                    "outcome": "Hatalı ve gereksiz radikal yaklaşım.",
                    "isCorrect": False
                }
            ]
        ),
        57: make_branching_logic(
            "Boğaz enfeksiyonundan 2 hafta sonra idrar rengi çay gibi olan (hematüri), tansiyonu 160/100 mmHg'ye fırlayan ve yüzünde ödem gelişen 12 yaşındaki çocukta akut poststreptokokal glomerülonefrit saptanıyor.",
            "Bu hastada ödemin tedavisinde ilk ve en kritik hemodinamik basamak ne olmalıdır?",
            [
                {
                    "text": "Hemen 5 litre serum fizyolojik (tuzlu su) takarak tansiyonu daha da artırmak",
                    "outcome": "Ölümcül akciğer ödemine ve hipertansif ensefalopatiye sokacak vahim hata.",
                    "isCorrect": False
                },
                {
                    "text": "Böbrekler primer sodyum ve su atamadığı için kesin tuz ve su kısıtlaması uygulamak, diüretik ve antihipertansif ile aşırı hacim yükünü boşaltmak",
                    "outcome": "Kusursuz nefrolojik yönetim: Glomerüler primer tuz tutulumunun hipervolemik doğası doğru çözülür.",
                    "isCorrect": True
                },
                {
                    "text": "Hastanın böbreklerini acilen ameliyatla almak",
                    "outcome": "Akut nefritte nefrektomi endikasyonu yoktur.",
                    "isCorrect": False
                }
            ]
        ),
        64: make_branching_logic(
            "Ağır gram negatif pnömoni ve sepsis tablosundaki bir hastada kapiller hidrostatik basınç normal olduğu halde akciğer grafisinde yaygın bilateral infiltrasyon ve ağır hipoksi (ARDS) gelişiyor.",
            "Yoğun bakım hekiminin bu akciğer ödeminin niteliği hakkındaki patofizyolojik kararı ne olmalıdır?",
            [
                {
                    "text": "Bu ödem kalp yetmezliğine bağlı tipik bir transudadır, sadece su birikmiştir.",
                    "outcome": "Hatalı ayrım: ARDS'de endotel hasarı ve proteinöz eksuda vardır.",
                    "isCorrect": False
                },
                {
                    "text": "Sepsis mediyatörlerinin alveolokapiller membranı parçalaması sonucu gelişen artmış vasküler geçirgenlik ödemidir (eksuda); alveoller protein, fibrin ve nötrofil doludur.",
                    "outcome": "Kusursuz patolojik analiz: Non-kardiyojenik akciğer ödemi ve ARDS eksuda mekanizması doğru tanımlanmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Akciğerlere dışarıdan hava yerine saf helyum gazı kaçmıştır.",
                    "outcome": "Gerçek dışı iddia.",
                    "isCorrect": False
                }
            ]
        ),
        66: make_branching_logic(
            "Kafa travması geçiren ve beyin tomografisinde sulkusları tamamen silinmiş, girusları basıklaşmış ve ventrikülleri daralmış ağır beyin ödemi saptanan hastada kafa içi basınç (KİBA) fırlıyor.",
            "Nöroşirürji ekibinin foramen magnumdan tonsiller herniasyonu önlemek için uygulayacağı acil medikal ajan tercihi ne olmalıdır?",
            [
                {
                    "text": "Hastaya damardan saf hipotonik su vermek",
                    "outcome": "Ölümcül hata: Hipotonik sıvı beyin hücrelerine dolarak ödemi anında patlatır ve herniasyonla öldürür.",
                    "isCorrect": False
                },
                {
                    "text": "İntravenöz Mannitol veya Hipertonik Salin vererek plazma ozmolaritesini artırmak; böylece ödem sıvısını beyin parankiminden damar içine ozmotik olarak çekmek",
                    "outcome": "Kusursuz nöroşirürjikal karar: Ozmotik diüretiklerle beyin parankimindeki ödem çekilir ve hayat kurtarılır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastanın kafasını tamamen aşağı sarkıtmak",
                    "outcome": "Venöz drenajı bozarak KİBA'yı daha da artırır.",
                    "isCorrect": False
                }
            ]
        ),
        74: make_branching_logic(
            "Yalnız yaşayan, hiç taze sebze-meyve tüketmeyen ve alkol bağımlısı olan 65 yaşındaki hastada diş etlerinde kabarma-kanama ve bacak kıl folikülleri çevresinde noktasal peteşiler saptanıyor. Trombosit sayısı ve PT/aPTT tamamen normaldir.",
            "Klinik patoloji ekibinin bu kanama diyatezinin moleküler mekanizması hakkındaki en doğru tanısı nedir?",
            [
                {
                    "text": "Ağır Hemofili B tablosudur, acil Faktör IX verilmelidir.",
                    "outcome": "Hatalı tanı: Faktör testleri ve trombosit normaldir.",
                    "isCorrect": False
                },
                {
                    "text": "C vitamini eksikliğidir (Skorbüt); prokollajen hidroksilasyonu aksadığı için damar duvarı aşırı kırılganlaşmış ve perivasküler kanamalar oluşmuştur; oral C vitaminiyle hızla düzelir.",
                    "outcome": "Kusursuz klinik patoloji teşhisi: Skorbüt ve vasküler frajilite mekanizması tam kavranmıştır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastada akut miyeloid lösemi vardır.",
                    "outcome": "Lösemide kemik iliği çöküşü ve trombositopeni beklenir.",
                    "isCorrect": False
                }
            ]
        ),
        76: make_branching_logic(
            "Koroner arter stent öyküsü nedeniyle günde 100 mg Aspirin kullanan bir hastaya elektif fıtık cerrahisi planlanıyor.",
            "Cerrahi ekibinin cerrahi sırasında masif kanamayı önlemek için operasyon zamanlaması hakkındaki en doğru kararı ne olmalıdır?",
            [
                {
                    "text": "Aspirin trombositleri sadece 1 saat etkiler, ameliyat sabahı ilacı alıp hemen ameliyata girebilir.",
                    "outcome": "Ölümcül cerrahi kanama riski: Aspirin COX-1'i geri dönüşümsüz bloke eder.",
                    "isCorrect": False
                },
                {
                    "text": "Aspirin trombosit siklooksijenazını geri dönüşümsüz inhibe eder; yeni ve fonksiyonel trombositlerin üretilebilmesi için cerrahiden 7-10 gün önce ilaç kesilmelidir.",
                    "outcome": "Kusursuz cerrahi ve hematolojik karar: Trombosit ömrü (7-10 gün) ve geri dönüşümsüz inhibisyon doğru uygulanır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaya ameliyat masasında 10 ünite taze eritrosit takıp Aspirini 10 katına çıkarmak",
                    "outcome": "Tıbbi olarak hatalı ve tehlikeli yaklaşım.",
                    "isCorrect": False
                }
            ]
        ),
        95: make_branching_logic(
            "Halsizlik şikayetiyle başvuran 60 yaşındaki bir erkekte hemoglobin 7.5 g/dL, MCV 70 fL (mikrositer) ve serum ferritini aşırı düşük (demir eksikliği anemisi) saptanıyor. Travma öyküsü yoktur.",
            "Bu hastada iç hematom yerine gizli kronik dış kanama şüphesini ön planda tutan hekimin bir sonraki en kritik adımı ne olmalıdır?",
            [
                {
                    "text": "Sadece kas içi hematom aramak için bacak MR'ı çekmek ve hastayı evine göndermek",
                    "outcome": "Hatalı yaklaşım: İç hematom demir eksikliği anemisi yapmaz.",
                    "isCorrect": False
                },
                {
                    "text": "Demir kaybı yalnızca vücut dışına kanamayla mümkün olduğundan; gizli bir gastrointestinal kanamayı (kolon kanseri veya peptik ülser) dışlamak için acilen üst ve alt endoskopi (kolonoskopi) planlamak",
                    "outcome": "Kusursuz klinik karar: Demir eksikliği anemisinin dış kanama kaynağı araştırılır ve hayat kurtarılır.",
                    "isCorrect": True
                },
                {
                    "text": "Hastaya sadece demir hapı verip kanama odağını hiç araştırmamak",
                    "outcome": "Altta yatan olası bir kolon kanserinin atlanmasına yol açacak ihmal.",
                    "isCorrect": False
                }
            ]
        )
    }

def get_extra_recalls():
    """Active recall oranını artırmak için eklenecek soru-cevaplar."""
    return {
        1: make_active_recall(
            "Toplam vücut suyunun yaklaşık üçte ikisini (2/3) barındıran temel sıvı kompartmanı hangisidir?",
            "İntrasellüler kompartman (hücre içi sıvı)",
            "Hücrelerin içindeki sitoplazmik sıvı alanı"
        ),
        4: make_active_recall(
            "Mikrosirkülasyonda kılcal damarın venüler ucunda dokudaki sıvının damara geri emilimini sağlayan majör kuvvet nedir?",
            "Plazma kolloid ozmotik (onkotik) basıncı",
            "Plazma proteinlerinin yarattığı çekim gücü"
        ),
        7: make_active_recall(
            "Tüm deri altı dokularında aşırı yaygın şişlik ile birlikte vücut seröz boşluklarında sıvı toplanmasıyla karakterize genel ağır ödeme ne ad verilir?",
            "Anasarka",
            "Ağır yaygın sistemik masif ödem tablosu"
        ),
        13: make_active_recall(
            "Akut enflamasyon alanında arteriyollerin genişlemesi sonucu dokunun parlak kırmızı renk alması ve ısınması hangi hemodinamik süreçtir?",
            "Aktif hiperemi (enflamatuvar hiperemi)",
            "Arteriyel akım artışına bağlı kırmızı-sıcak doku tablosu"
        ),
        17: make_active_recall(
            "Kronik venöz konjesyon zemininde dokuda gelişen süreğen perfüzyon yetersizliği ve oksijensizlik hangi kalıcı dokusal değişikliğe yol açar?",
            "Parankim hücresi atrofisi/nekrozu ve sekonder fibrozis",
            "Hücre kaybı ve bağ dokusu artışı"
        ),
        23: make_active_recall(
            "Kronik sol kalp yetmezliğinde akciğerin alveol septalarında fibrozis ve hemosiderin birikimi sonucu sertleşip pas rengi almasına ne ad verilir?",
            "Kahverengi endürasyon (Brown induration)",
            "Akciğerin kronik konjestif sertleşme ve renk terimi"
        ),
        27: make_active_recall(
            "Karaciğer asinüsünde venöz konjesyon ve sistemik şok hipoksisine karşı en duyarlı olan ve ilk nekroza giden lobül bölgesi neresidir?",
            "Asinüs Zon 3 (sentrilobüler bölge)",
            "Santral ven komşuluğundaki en duyarlı asinüs zonu"
        ),
        32: make_active_recall(
            "Uzun süreli immobilizasyon veya cerrahi sonrası tek bir bacakta derin ven trombozuna bağlı ödem gelişmesinde primer rol oynayan Starling kuvveti nedir?",
            "Artmış lokal kapiller hidrostatik basınç",
            "Venöz akımın tıkanmasıyla geriye tepen itici damar içi basınç"
        ),
        36: make_active_recall(
            "Kalp yetmezliğinde böbrek hipoperfüzyonunun tetiklediği ve böbrek tübüllerinden sodyum ve suyun tutulmasına yol açan sürrenal hormon artışı tablosuna ne ad verilir?",
            "Sekonder hiperaldosteronizm",
            "Renin aracılığıyla uyarılmış aşırı aldosteron tablosu"
        ),
        42: make_active_recall(
            "Plazma kolloid ozmotik basıncının yaklaşık yüzde 80'ini tek başına sağlayan ve eksikliğinde yaygın ödem gelişen temel plazma proteini nedir?",
            "Albümin",
            "Karaciğerde üretilen majör plazma proteini"
        ),
        47: make_active_recall(
            "Çocuklarda kalorisi yeterli ancak proteini tamamen eksik beslenme sonucu karaciğerde albümin üretilememesiyle gelişen ödemli malnütrisyon hastalığı nedir?",
            "Kwashiorkor",
            "Protein eksikliğine bağlı ödemli beslenme bozukluğu"
        ),
        53: make_active_recall(
            "Meme kanseri karsinom hücrelerinin derialtı subdermal lenfatik kanalları infiltre edip tıkaması sonucu meme cildinde oluşan karakteristik pürtüklü görünüme ne ad verilir?",
            "Peau d'orange (Portakal kabuğu görünümü)",
            "Meme derisinde lenfödemik pürtüklenme tablosu"
        ),
        58: make_active_recall(
            "Enflamasyonda endotel hücre aralıklarının açılması sonucu dokuya sızan, yüksek proteinli (>3 g/dL) ve lökosit zengini sıvıya ne ad verilir?",
            "Eksuda",
            "Enflamatuvar geçirgenlik artışına bağlı ödem sıvısı"
        ),
        63: make_active_recall(
            "Sol ventrikül yetmezliğine bağlı akut akciğer ödeminde kesit yüzeyinden ve bronş lümeninden fışkıran sıvının hava ile çalkalanmış karakteristik fiziksel görünümü nedir?",
            "Köpüklü pembe sıvı (seröz transuda)",
            "Hava ile seröz sıvının karışması sonucu oluşan görünüm"
        ),
        73: make_active_recall(
            "Minimal travmayla veya kendiliğinden anormal kanamaya yatkınlık yaratan hastalıklar grubuna verilen genel tıbbi isim nedir?",
            "Hemorajik diyatez",
            "Kanama eğilimi şemsiye terimi"
        ),
        83: make_active_recall(
            "Deri muayenesinde 3-5 mm çapında lezyonların palpabl (parmakla kabarıklık hissedilen) olması öncelikle hangi patolojik süreci kanıtlar?",
            "Lökositoklastik vaskülit (damar duvarı enflamasyonu)",
            "Damar duvarında yangı ve nekrozla seyreden durum"
        )
    }

def enrich_slides(slides):
    """Slaytları branching logic ve active recall ile zenginleştirip %8 kuralını sağlar."""
    extra_branching = get_extra_branching()
    extra_recalls = get_extra_recalls()

    for idx, slide in enumerate(slides, start=1):
        if idx in extra_branching:
            slide["elements"].append(extra_branching[idx])
        if idx in extra_recalls:
            slide["elements"].append(extra_recalls[idx])

    return slides
