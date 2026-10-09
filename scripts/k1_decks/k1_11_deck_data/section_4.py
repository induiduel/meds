# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-11-s31",
        "title": "Üst Üriner Sistem (Supravezikal) Obstrüksiyonunun Genel Dinamikleri",
        "content": "Supravezikal obstrüksiyon, üreterovezikal bileşke ile toplayıcı tübüller arasında kalan herhangi bir anatomik noktada idrar transportunun kesintiye uğramasıdır. Renal fonksiyonlara ve klinik seyire etki eden temel parametreler; tıkanıklığın şiddeti (tam veya kısmi), devam süresi, bakteriyel enfeksiyonun varlığı, tek taraflı (unilateral) ya da iki taraflı (bilateral) olması ve tablonun akut veya kronik seyirli olmasıdır. Tıkanıklık seviyesi ne kadar proksimalde (örneğin üreteropelvik bileşkede) yer alırsa, böbrek parankimi hidrostatik basınca o kadar hızlı ve doğrudan maruz kalır. Üst üriner sistemde idrar akımı yalnızca yerçekimiyle değil, kaliks pacemaker hücrelerinden başlayıp üretere yayılan aktif peristaltik kasılma dalgalarıyla sağlanır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Supravezikal obstrüksiyonda tıkanıklık seviyesi üreteropelvik bileskeye ne kadar yakınsa böbrek üzerine etkisi o kadar erken ve fazladır.",
                "üreteropelvik bileskeye",
                "Pelvis ile üreterin birleştiği en proksimal anatomik nokta"
            ),
            make_quiz(
                "Üst üriner sistem obstrüksiyonunda renal parankim hasarının ciddiyetini ve klinik prognozu belirleyen faktörlerden hangisi doğrudan böbrek içi basınç iletim hızını etkiler?",
                [
                    {"key": "A", "text": "Obstrüksiyonun üreteropelvik bileşkeye olan yakınlığı ve seviyesi", "explanation": "A seçeneği doğrudur: Tıkanıklık böbreğe ne kadar yakınsa hidrostatik basınç sönümlenmeden doğrudan kalikslere iletilir."},
                    {"key": "B", "text": "Hastanın kan grubu ve eritrosit sayısı", "explanation": "B seçeneği yanlıştır: Kan grubu obstrüksiyon dinamiğiyle ilişkisizdir."},
                    {"key": "C", "text": "Mesane kapasitesinin büyüklüğü", "explanation": "C seçeneği yanlıştır: Supravezikal obstrüksiyon mesane dolumundan bağımsız gelişebilir."},
                    {"key": "D", "text": "Üretral mea çapı", "explanation": "D seçeneği yanlıştır: Bu infravezikal faktördür."},
                    {"key": "E", "text": "Prostat bezinin stromal ağırlığı", "explanation": "E seçeneği yanlıştır: Üst sistem tıkanıklıklarında primer belirleyici değildir."}
                ],
                "A"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-11-s32",
        "title": "Üreter Kas Mimarisi: Longitudinal ve Sirküler Liflerin Fonksiyonel Rolü",
        "content": "Üreter duvarı histolojik olarak özelleşmiş iki düz kas tabakasına sahiptir ve bu lifler idrarın emniyetli transportunda kritik bir işbölümü yapar:\n\n- **İç Longitudinal Kas Lifleri:** Üreter boyunca uzunlamasına uzanır. Peristaltik dalga sırasında kasılarak idrar bolusunu aşağıya, mesaneye doğru antegrad yönde iletir.\n- **Dış Sirküler Kas Lifleri:** Üreter lümenini halka gibi sarar. Kasılma dalgası geçerken lümeni kapatıcı bir sfinkterik bariyer oluşturur; bu sayede distal üreterde oluşan yüksek basıncın retrograd olarak yukarıya, kalikslere ve böbreğe geri iletilmesini mekanik olarak engeller.\n\nObstrüksiyon durumunda intralüminal basınç üreterin kompanzasyon kapasitesini aştığında bu iki tabaka arasındaki koordinasyon çözülür, kas demetleri birbirinden uzaklaşır ve koruyucu sfinkter mekanizması çöker.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Üreter Kas Tabakalarının Fonksiyonel Ayrımı",
                "Longitudinal Kas Lifleri",
                "İdrar bolusunu aşağıya, mesaneye doğru antegrad yönde iletmekten sorumludur.",
                "Sirküler Kas Lifleri",
                "Lümeni halkasal kapatarak yüksek basıncın böbreğe geri kaçmasını engeller."
            ),
            make_recall(
                "Üreter peristaltizminde üreterdeki yüksek basıncın böbreğe geri iletimini engelleyen kas tabakası hangisidir?",
                "Sirküler kas lifleridir.",
                "Lümeni çevreleyen halkasal düz kas tabakası"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-11-s33",
        "title": "Erken Kaliksiyel Yanıt: Konkavlığın Kaybı, Forniks Küntleşmesi ve Düzleşme",
        "content": "Üst üriner sistemde basınç artışından ilk ve en erken etkilenen anatomik yapılar kalikslerdir. Normal bir böbrekte minör kaliksin medüller papillayı sardığı forniks bölgesi son derece keskin açılı ve derindir; papilla kaliks içine doğru belirgin bir konveksite yapar ve kaliks boşluğu hilal şeklinde konkav görünür. Obstrüksiyon başladığında yükselen intrapelvik hidrostatik basınç papillaya doğru geri bası uygular. Kaliksin konkav görüntüsü hızla kaybolur, fornikslerin keskin açıları silinerek küntleşir. Süreç devam ettikçe renal papillalar ezilip yassılaşır ve kaliks tavanı çukurlaşarak konveks bir kadeh halini alır. Bu morfolojik değişim radyolojide 'kaliks küntleşmesi (clubbing)' olarak adlandırılır ve erken obstrüktif hasarın kardinal bulgusudur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Anatomik Bölge", "Normal Morfoloji", "Obstrüksiyondaki Erken Yanıt"],
                [
                    [
                        {"text": "Minör Kaliks Forniksi", "isMasked": False, "hint": ""},
                        {"text": "Keskin açılı ve derin girinti", "isMasked": True, "hint": "Papilla boynunu saran normal dar açı"},
                        {"text": "Küntleşme ve açı kaybı (clubbing)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Renal Papilla", "isMasked": False, "hint": ""},
                        {"text": "Kaliks içine uzanan konveks tepe", "isMasked": True, "hint": "Toplayıcı kanalların açıldığı kubbe"},
                        {"text": "Ezilme, yassılaşma ve silinme", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kaliks Kavitesi", "isMasked": False, "hint": ""},
                        {"text": "Hilal şeklinde konkav kontur", "isMasked": True, "hint": "Normal boşluk silüeti"},
                        {"text": "Genişlemiş, balonlaşmış konveks kontur", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Supravezikal obstrüksiyonda basınç artışından ilk olarak kaliksler etkilenir; forniksler küntleşir ve papillalar yassılaşır.",
                "kaliksler",
                "İdrarın tübüllerden ilk döküldüğü kadeh biçimli toplayıcı yapı"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-11-s34",
        "title": "Üreter Düz Kasında Hipertrofi, Hiperplazi ve Neksus Hasarı",
        "content": "Obstrüksiyonun ilk haftalarında üreter ve renal pelviste progresif bir lümen dilatasyonu izlenir. Tıkanıklık gerisindeki proksimal üreter ve pelvis, idrar transportunu sürdürebilmek amacıyla daha kuvvetli kasılmalar üretmeye başlar. Bu kompanzatuar yanıt üreter düz kas hücrelerinde hem hacimsel büyüme (hipertrofi) hem de sayısal artış (hiperplazi) ile sonuçlanır. Ancak obstrüksiyon devam ettiğinde düz kas lifleri arasına kollajen ve elastik bağ dokusu sızar. En önemlisi, düz kas hücreleri arasında elektriksel uyarıyı ve senkron peristaltizmi sağlayan oluklu bağlantı (gap junction / neksus) kompleksleri basınç ve gerilim etkisiyle hasara uğrar. Neksus hasarı miyojenik iletiyi tamamen koparır; üreter peristaltik dalgaları koordinasyonunu kaybederek etkisiz, kaotik kasılmalara dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Üreterde Miyojenik İleti Bozukluğu Zinciri",
                [
                    "1. Proksimal Basınç: Toplayıcı sistemde intralüminal basıncın yükselmesi",
                    "2. Aşırı Gerilim: Üreter düz kas liflerinde hipertrofi ve araya bağ dokusu girmesi",
                    "3. Neksus Hasarı: Hücreler arası gap junction bağlantılarının kopması",
                    "4. Aritmik Peristaltizm: Miyojenik iletinin kaybolması ve idrar transportunun durması"
                ]
            ),
            make_recall(
                "Üreter düz kas hücreleri arasında miyojenik elektriksel iletiyi sağlayan ve obstrüksiyonda hasara uğrayarak peristaltizmi bozan bağlantı yapıları hangileridir?",
                "Neksus (gap junction / oluklu bağlantı) yapılarıdır.",
                "Hücreler arası direkt elektriksel köprüler"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-11-s35",
        "title": "Toplayıcı Sistemde 7. Gün Kritik Eşiği: Kollektör Kanal Nekrozu",
        "content": "Deneysel ve klinik çalışmalarda üst üriner sistem obstrüksiyonunun zaman çizelgesinde '7. gün' çok kritik bir patofizyolojik dönüm noktası olarak tanımlanmıştır. Tıkanıklığın ilk 6 gününde toplayıcı tübüllerde basınç artışına bağlı pasif dilatasyon ve hücresel gerilme hakimdir; tübül epiteli henüz morfolojik bütünlüğünü korumaktadır. Ancak obstrüksiyonun 7. gününe ulaşıldığında, aşırı dilate olmuş kollektör kanalların epitel hücrelerinde iskemik hasara bağlı koagülasyon nekrozu ve apoptoz başlar. Bu hücresel ölüm toplayıcı kanallarda fokal incelme, rüptür ve interstisyel alana idrar sızmasına yol açar. Epitel yıkımı aynı zamanda toplayıcı kanal bazal membranını parçalayarak geri dönüşümsüz tübüler atrofi ve interstisyel fibrozis sürecini tetikler.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Tam üreter obstrüksiyonunda toplayıcı sistem kollektör kanallarında hücresel atrofi ve nekrozun başladığı kritik zaman eşiği hangisidir?",
                [
                    {"key": "A", "text": "7. gün", "explanation": "A seçeneği doğrudur: Ders notunda belirtildiği üzere obstrüksiyonun 7. gününde dilate kollektör kanallarda hücresel atrofi ve nekroz başlar."},
                    {"key": "B", "text": "1. saat", "explanation": "B seçeneği yanlıştır: Bu dönemde yalnızca erken vazoaktif hemodinamik yanıtlar izlenir."},
                    {"key": "C", "text": "6. ay", "explanation": "C seçeneği yanlıştır: 6. ayda parankim tamamen fibrotik ve atrofik hale gelmiştir."},
                    {"key": "D", "text": "24. saat", "explanation": "D seçeneği yanlıştır: İlk günde tübüllerde gerilme vardır ancak nekroz 7. günde başlar."},
                    {"key": "E", "text": "2. yıl", "explanation": "E seçeneği yanlıştır: Çok geç bir süredir."}
                ],
                "A"
            ),
            make_cloze(
                "Üst üriner sistem obstrüksiyonunun 7. gününde asırı dilate toplayıcı kanallarda atrofi ve nekroz süreci baslar.",
                "atrofi ve nekroz",
                "Hücresel yıkım ve doku ölümü süreçleri"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-11-s36",
        "title": "Koruyucu Reflü Mekanizmaları - I: Pyelointerstisyel Reflü",
        "content": "Üst üriner sistem obstrüksiyonunda yükselen intrapelvik basıncın glomerüllere ulaşıp filtrasyonu tamamen durdurmasını geciktirmek amacıyla böbrek özelleşmiş 'koruyucu (basınç azaltıcı) reflü sistemleri' devreye sokar. Bu mekanizmaların klinik ve deneysel olarak en sık görüleni pyelointerstisyel reflüdür. İntrapelvik hidrostatik basınç kritik eşiği aştığında minör kaliks forniksleri ve papilla tabanında mikro-yırtıklar oluşur. İdrar bu yırtıklardan toplayıcı sistem dışına sızarak renal sinüsün gevşek bağ dokusuna ve perirenal interstisyel alana geçer. İnterstisyuma geçen bu idrar daha sonra perirenal venöz ve lenfatik damarlar tarafından emilerek sistemik dolaşıma taşınır. Bu güvenlik valfi intrapelvik basıncı geçici olarak düşürerek renal parankimi ani patlama ve masif yırtılmadan korur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "Akut tam üreter taşı tıkanıklığı olan bir hastada pelvik basınç 50 mmHg üzerine çıkıyor ve forniks tabanından interstisyel alana idrar sızıntısı gelişiyor.",
                "Bu olgudaki en sık koruyucu reflü mekanizması ve fizyolojik hedefi nedir?",
                [
                    {
                        "text": "Pyelointerstisyel reflüdür; intrapelvik basıncı düşürerek böbrek fonksiyonundaki bozulmayı geciktirmeyi hedefler.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Pyelointerstisyel reflü en sık koruyucu mekanizmadır; idrar sinüs ve perirenal alana geçerek basıncı tahliye eder."
                    },
                    {
                        "text": "Vezikoüreteral reflüdür; idrarı mesaneden taşırarak sfinkteri korur.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. VUR mesaneden geriye kaçıştır; intrapelvik dekompresyon mekanizması değildir."
                    },
                    {
                        "text": "Pyelokutanöz fistüldür; idrarın ciltten doğrudan dışarı akmasını sağlar.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Spontan kutanöz fistül normal koruyucu bir fizyolojik dekompresyon yolu değildir."
                    }
                ]
            ),
            make_recall(
                "Üst üriner sistem obstrüksiyonunda görülen koruyucu (basınç azaltıcı) reflü mekanizmaları arasında en sık izleneni hangisidir?",
                "Pyelointerstisyel reflüdür.",
                "Forniksten böbrek sinüsüne ve perirenal dokuya idrar kaçışı"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-11-s37",
        "title": "Koruyucu Reflü Mekanizmaları - II: Pyelolenfatik ve Pyelovenöz Geri Akım",
        "content": "Pyelointerstisyel reflünün yanı sıra böbreğin iki önemli vasküler emilim mekanizması daha mevcuttur:\n\n- **Pyelolenfatik Reflü:** Normalde böbrek lenfi hiler ve kapsüler lenfatik kanallarla drene edilir. İstirahat halindeki bir böbrekte lenfatik akım volümü yaklaşık olarak idrar akım volümüne eşittir. Üreter obstrüksiyonu geliştiğinde böbrek lenf akımı dramatik şekilde katlanarak artar; fornikslerden sızan idrar lenfatik damarlarca hızla emilerek duktus torasikusa iletilir. İlginç olarak akut lenfatik obstrüksiyon varlığında natriürez ve diürez oluştuğu gösterilmiştir.\n- **Pyelovenöz Reflü:** Kaliksiyel fornikslerin hemen komşuluğunda yer alan arkuat ve interlobüler venler yüksek intrapelvik basınçla erode olduğunda, idrar doğrudan venöz sisteme boşalır. Bu mekanizma çok etkili bir basınç tahliyesi sağlar ancak enfekte idrar varlığında doğrudan bakteriyemiye yol açma riski taşır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Koruyucu Mekanizma", "Anatomik Yol", "Klinik Özellik ve Risk"],
                [
                    [
                        {"text": "Pyelointerstisyel", "isMasked": False, "hint": ""},
                        {"text": "Forniksten renal sinüs ve perirenal bağ dokusuna", "isMasked": True, "hint": "En sık görülen dekompresyon yolu"},
                        {"text": "En sık mekanizma; perirenal sıvı birikimi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Pyelolenfatik", "isMasked": False, "hint": ""},
                        {"text": "Hiler ve kapsüler lenfatik kanallara geçiş", "isMasked": True, "hint": "Normal volümü idrar akımına eşit olan kanal sistemi"},
                        {"text": "Lenf debisinde masif artış; duktus torasikusa iletim", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Pyelovenöz", "isMasked": False, "hint": ""},
                        {"text": "Forniks komşuluğundaki venöz pleksusa doğrudan geçiş", "isMasked": True, "hint": "Doğrudan kan dolaşımına bağlantı"},
                        {"text": "Hızlı basınç düşüşü sağlar fakat enfeksiyonda sepsis riski doğurur", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Normal böbrekte lenfatik akım volümü yaklasık olarak idrar akımına eşittir ve üreter obstrüksiyonunda belirgin şekilde artış gösterir.",
                "idrar akımına",
                "Dakikadaki üretilen idrar miktarıyla lenf hacmi dengesi"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-11-s38",
        "title": "Forniks Rüptürü, Ürinom Oluşumu ve İntrarenal Reflü",
        "content": "İntrapelvik hidrostatik basınç pelvik duvarın ve forniks dokusunun gerilme direncini aştığında makroskopik 'forniks rüptürü' meydana gelir. Rüptür sonucu idrar retroperitoneal boşluğa fışkırarak perirenal alanda kapsüllü bir idrar koleksiyonu oluşturur; buna ürinom (urinoma) denir. Forniks rüptürü aslında pelvis içi basıncı aniden sıfırlayarak hastanın şiddetli renal kolik ağrısını bir anda bıçak gibi kesebilir; bu durum hekimi yanıltmamalıdır. Diğer taraftan, basınç artışı idrarın toplayıcı kanallara ve Bellini duktuslarına zorla geri girmesine (intrarenal reflü) neden olur. Eğer obstrükte idrar stafilokok, E. coli veya proteus gibi bakterilerle enfekte ise, intrarenal reflü ve pyelovenöz geri akım yoluyla bakteriler dakikalar içinde doğrudan sistemik vasküler alana girer; süratle üroseptik şok tablosu gelişir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Forniks Rüptürü ve Ürosepsis Gelişim Aşamaları",
                [
                    "1. Şiddetli Basınç: İntrapelvik basıncın forniks yırtılma eşiğini aşması",
                    "2. Forniks Rüptürü: Kaliks forniksinde makroskopik yırtılma ve retroperitona idrar sızması",
                    "3. Ağrıda Ani Azalma: Pelvik dekompresyon ile renal koliğin geçici olarak rahatlaması",
                    "4. İntrarenal/Pyelovenöz Giriş: Enfekte idrarın doğrudan dolaşıma karışarak ürosepsis başlatması"
                ]
            ),
            make_recall(
                "Forniks rüptürü sonrası idrarın retroperitoneal alanda birikerek sınırlı bir koleksiyon oluşturmasına ne ad verilir?",
                "Ürinom (urinoma).",
                "Retroperitoneal idrar kisti veya koleksiyonu"
            )
        ]
    })

    # Slide 39 (CHECKPOINT 4)
    slides.append({
        "id": "k1-11-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Üst Üriner Sistem Obstrüksiyonu ve Koruyucu Mekanizmalar",
        "content": "Üst üriner sistem obstrüksiyonunun temel anatomik ve fizyopatolojik ilkeleri:\n\n1. **Kas Mimarisi:** Longitudinal lifler idrarı aşağı iletir; sirküler lifler retrograd basınç geçişini engelleyen bir bariyerdir.\n2. **İlk Hasar:** Basınçtan ilk etkilenen yer kalikslerdir; konkavlık bozulur, forniksler küntleşir (clubbing), papillalar düzleşir.\n3. **Miyojenik Kopuş:** Düz kas hipertrofisi ve neksus (gap junction) hasarı peristaltizmi bozar; 7. günde kollektör kanallarda nekroz ve atrofi başlar.\n4. **Koruyucu Sistemler:** İntrapelvik basıncı düşürerek böbrek fonksiyonunu korumaya çalışan mekanizmalar pyelointerstisyel (en sık), pyelolenfatik ve pyelovenöz reflüdür.\n5. **Risk:** Enfekte obstrüksiyonda intrarenal ve pyelovenöz reflü hızla ürosepsise yol açar; forniks rüptürü perirenal ürinoma neden olur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Supravezikal obstrüksiyonda gelişen koruyucu (basınç azaltıcı) mekanizmalarla ilgili hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "Pyelointerstisyel reflü en sık izlenen koruyucu yoldur.", "explanation": "A seçeneği doğrudur: En sık görülen mekanizmadır."},
                    {"key": "B", "text": "Normalde lenfatik volüm idrar akım volümüne yakındır ve obstrüksiyonda belirgin artar.", "explanation": "B seçeneği doğrudur: Lenfatik drenaj dekompresyona yardımcı olur."},
                    {"key": "C", "text": "Pyelovenöz reflü enfekte olgularda bakterilerin doğrudan vasküler yatağa geçiş riskini taşır.", "explanation": "C seçeneği doğrudur: Venöz sisteme açıldığı için bakteriyemi yapar."},
                    {"key": "D", "text": "Forniks rüptürü intrapelvik basıncı dramatik şekilde artırarak kolik ağrısını dayanılmaz hale getirir.", "explanation": "D seçeneği YANLIŞTIR: Forniks yırtıldığında basınç aniden düşer ve paradoksal olarak hastanın kolik ağrısı aniden rahatlar."},
                    {"key": "E", "text": "Koruyucu mekanizmalar yeterince çalışırsa böbrek fonksiyonundaki bozulma gecikir.", "explanation": "E seçeneği doğrudur: Basıncı düşürerek nefron hasarını geciktirir."}
                ],
                "D"
            ),
            make_cloze(
                "Supravezikal obstrüksiyonda koruyucu reflü mekanizmaları yeterince calısırsa böbrek fonksiyonundaki bozulma gecikir.",
                "bozulma gecikir",
                "Nefron fonksiyon kaybının zamanlamasındaki erteleme"
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-11-s40",
        "title": "Obstrüksiyon Süresi ve Fonksiyonel İyileşme Potansiyeli",
        "content": "Üriner obstrüksiyonda en kritik klinik soru, tıkanıklık giderildikten sonra böbreğin ne kadar fonksiyon geri kazanabileceğidir. Deneysel köpek modellerinde yapılan klasik çalışmalarda:\n\n- **2 Haftalık Tam Obstrüksiyon:** Tıkanıklık açıldığında böbrek GFR'sinin kontrol değerinin **%46'sını** geri kazanabilmektedir.\n- **4 Haftalık Tam Obstrüksiyon:** GFR geri dönüşü kontrol değerinin **%35'i** ile sınırlı kalmaktadır.\n- **6 Haftalık Tam Obstrüksiyon:** Tıkanıklık açılsa bile fonksiyonel olarak **geri dönen hiçbir filtrasyon fonksiyonu kalmamaktadır (%0)**.\n\nİnsan böbreği için kesin bir zaman tablosu çizmek etik olarak mümkün olmasa da, 6 haftalık tam obstrüksiyon sınırının geri dönüşümsüz parankim kaybını simgelediği kabul edilir. Obstrüksiyon ne kadar erken kaldırılırsa, nefron rezervi o kadar yüksek oranda kurtarılır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Obstrüksiyon Süresi (Deneysel)", "Dekompresyon Sonrası Geri Dönen GFR", "Klinik Yorum"],
                [
                    [
                        {"text": "2 Hafta", "isMasked": False, "hint": ""},
                        {"text": "Kontrolün %46'sı", "isMasked": True, "hint": "Yaklaşık yarı yarıya geri kazanım oranı"},
                        {"text": "Belirgin fonksiyonel iyileşme potansiyeli", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "4 Hafta", "isMasked": False, "hint": ""},
                        {"text": "Kontrolün %35'i", "isMasked": True, "hint": "Üçte bir düzeyinde sınırlı geri dönüş"},
                        {"text": "Kısmi iyileşme, belirgin kalıcı nefron kaybı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "6 Hafta", "isMasked": False, "hint": ""},
                        {"text": "Geri dönen fonksiyon yok (%0)", "isMasked": True, "hint": "Tam kayıp ve geri dönüşümsüzlük sınırı"},
                        {"text": "Tam irreversibilite; hidronefrotik atrofi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Deneysel çalışmalara göre tam üreter obstrüksiyonu sonrasında dekompresyon yapılsa dahi geri dönen hiçbir GFR fonksiyonunun kalmadığı kritik süre eşiği nedir?",
                "6 haftadır.",
                "Geri dönüşün sıfırlandığı hafta sayısı"
            )
        ]
    })

    return slides
