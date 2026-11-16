# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-11-s91",
        "title": "Etiyolojiye Yönelik Tedaviler: BPH Cerrahileri",
        "content": "Alt üriner sistem obstrüksiyonunun en sık edinsel nedeni olan Benign Prostat Hiperplazisinde (BPH) medikal tedaviye (alfa-blokerler, 5-alfa redüktaz inhibitörleri) yanıtsız veya komplikasyon gelişmiş olgularda cerrahi çıkım dekompresyonu uygulanır. Güncel cerrahi yaklaşımlar:\n\n- **Transüretral Prostat Rezeksiyonu (TUR-P):** 30-80 gram arası prostatlarda altın standart endoskopik yöntemdir. Elektrokoter halkasıyla adenom dokusu parça parça kazınarak üretra lümeni genişletilir.\n- **Lazer Enükleasyon (HoLEP / ThuLEP):** Özellikle 80 gramdan büyük dev prostatlarda prostatik cerrahi kapsül boyunca adenomun lazerle tek parça halinde mesaneye soyulup morselatörle kıyılarak çıkarılmasıdır; açık ameliyat başarısını minimal invaziv yolla sunar.\n- **Açık / Robotik Suprapubik Prostatektomi:** Çok büyük adenomlarda veya eşlik eden dev mesane taşı/divertikülü varlığında tercih edilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "BPH Cerrahi Yöntemleri Karşılaştırması",
                "Transüretral Rezeksiyon (TUR-P)",
                "Orta büyüklükteki prostatlarda endoskopik elektrokoter ile dokunun kazınarak açılmasıdır.",
                "Lazer Enükleasyon (HoLEP)",
                "Büyük prostatlarda adenomun kapsülden anatomik olarak lazerle soyulup çıkarılmasıdır."
            ),
            make_cloze(
                "Benign prostat hiperplazisinde orta büyüklükteki bezler için klasik altın standart cerrahi yöntem transüretral prostat rezeksiyonudur.",
                "prostat rezeksiyonudur",
                "TUR-P kısaltmasının açılımı olan endoskopik girişim"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-11-s92",
        "title": "Üreter Darlıklarında Rekonstrüksiyon: Anderson-Hynes Pyeloplasti",
        "content": "Böbrek düzeyindeki en sık konjenital supravezikal obstrüksiyon olan Üreteropelvik Bileşke (UPJ) Darlığında cerrahi altın standart **Anderson-Hynes Açık veya Laparoskopik/Robotik Dezmember (Ayrık) Pyeloplasti** ameliyatıdır. Bu rekonstrüksiyonun temel cerrahi adımları şunlardır:\n\n1. **Diseksiyon:** Pelvis ve üreter proksimali çevre yapışıklıklardan ve bası yapan aberran alt pol damarlarından serbestleştirilir.\n2. **Dezmember Rezeksiyon:** Fonksiyon görmeyen, fibrotik, disorganize düz kas demetleri içeren dar UPJ segmenti tamamen kesilerek çıkarılır; aşırı genişlemiş renal pelvisten redüksiyon (hacim küçültme) yapılır.\n3. **Transpozisyon:** Eğer bası yapan aberran renal damar varsa üreter bu damarın arkasından öne taşınır.\n4. **Spatülasyon ve Anastomoz:** Sağlıklı üreter lateralden spatüle edilerek (genişletilerek) huni şeklindeki renal pelvise geniş, gerilimsiz ve su geçirmez şekilde yeniden dikilir (anastomoze edilir).",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Anderson-Hynes Pyeloplasti Aşamaları",
                [
                    "1. Mobilizasyon: Pelvis ve aberran alt pol damarının çevre dokulardan ayrılması",
                    "2. Eksizyon: Fibrotik dar UPJ bileşkesinin kesilerek çıkarılması",
                    "3. Pelvik Redüksiyon: Aşırı genişlemiş pelvisten doku çıkarılarak hunileştirilmesi",
                    "4. Spatüle Anastomoz: Üreterin genişletilip pelvise gerilimsiz yeniden dikilmesi"
                ]
            ),
            make_recall(
                "Üreteropelvik bileşke (UPJ) darlığının kesin anatomik onarımında uygulanan altın standart cerrahi rekonstrüksiyon tekniği hangisidir?",
                "Anderson-Hynes (dezmember) pyeloplastidir.",
                "Eponymli ayrık pelvik rekonstrüksiyon ameliyatı"
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-11-s93",
        "title": "Pediatrik Acil Tedavi: Posterior Üretral Valv Endoskopik Ablasyonu",
        "content": "Erkek bebeklerde en sık görülen ve bilateral ağır obstrüksiyonla renal yetmezliğe yol açan Posterior Üretral Valv (PUV) tedavisinde zamanlama nefronların kurtarılması için kritiktir. Antenatal USG'de bilateral hidronefroz ve anahtar deliği mesane ile tanınan veya doğumdan sonra anüri/damla damla işeme ile saptanan bebeklerde ilk adım acil transüretral küçük lümenli beslenme tüpü ile mesane dekompresyonudur. Bebek stabilize edildikten, elektrolit dengesi ve kreatinin düşüşü sağlandıktan sonra kesin tedavi uygulanır: Pediatrik sistoüretroskop ile girilerek verumontanumun hemen distalindeki obstrüktif mukozal valv yaprakçıkları saat 12, 5 ve 7 hizalarından **endoskopik valv ablasyonu (elektrofulgurasyon veya lazer)** ile kesilir. Böylece üretra lümeni açılır ve mesane içi yüksek basınç kalıcı olarak düşürülür.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Posterior üretral valvli erkek infantlarda kesin tedavi yöntemi transüretral endoskopik valv ablasyonu işlemidir.",
                "endoskopik valv ablasyonu",
                "Mukozal perdeyi kamera altında yakarak açma işlemi"
            ),
            make_quiz(
                "Yenidoğan erkek bebekte bilateral hidronefroz ve böbrek yetmezliğine neden olan posterior üretral valvin kesin cerrahi tedavisi hangisidir?",
                [
                    {"key": "A", "text": "Endoskopik transüretral valv ablasyonu (fulgurasyonu)", "explanation": "A seçeneği DOĞRUDUR: Valv yaprakçıkları sistoskopik olarak kesilerek lümen açılır."},
                    {"key": "B", "text": "Radikal sistektomi ve barsaktan yapay mesane yapılması", "explanation": "B seçeneği yanlıştır: Bebeklerde mesane çıkarılmaz, valv kesilir."},
                    {"key": "C", "text": "Ömür boyu diyalize bağlanıp cerrahiden kaçınılması", "explanation": "C seçeneği yanlıştır: Valv açılırsa nefronlar kurtulur."},
                    {"key": "D", "text": "Yalnızca oral idrar söktürücü ilaçlarla takip", "explanation": "D seçeneği yanlıştır: Mekanik perde ilaçla erimez."},
                    {"key": "E", "text": "Her iki böbreğin cerrahi olarak dondurulması", "explanation": "E seçeneği anlamsızdır."}
                ],
                "A"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-11-s94",
        "title": "Ürolitiyazis Tedavi Modaliteleri: ESWL, URS/RIRC ve PCNL",
        "content": "Üriner sistem taşlarına bağlı akut veya kronik obstrüksiyonlarda taşın boyutuna, lokalizasyonuna ve sertliğine göre modern endoürolojik yöntemler seçilir:\n\n1. **Vücut Dışı Şok Dalga Litotripsi (ESWL):** 20 mm altındaki böbrek ve üst üreter taşlarında vücut dışından odaklanan ses dalgalarıyla taşı kırarak kum halinde dökülmesini hedefler.\n2. **Semirijit ve Fleksibl Üreterorenoskopi (URS / RIRC):** İdrar kanalından doğal yolla girilerek üreter veya böbrek içindeki taşa ulaşılır; Holmium veya Thulium lazer enerjisiyle taş 'tozlaştırma (dusting)' tekniğiyle tamamen eritilir veya basket ile parçaları toplanır.\n3. **Perkütan Nefrolitotomi (PCNL):** 20 mm'den büyük geyik boynuzu (staghorn) veya multipl kaliks taşlarında böğürden 1 cm'lik kesiyle böbreğe girilip taşlar doğrudan kırılarak dışarı alınır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Taş Tedavi Modalitesi", "Uygulama Tekniği", "İdeal Taş Tipi ve Boyutu"],
                [
                    [
                        {"text": "ESWL", "isMasked": False, "hint": ""},
                        {"text": "Vücut dışı şok dalgaları ile kırma", "isMasked": True, "hint": "Kesi olmaksızın ses dalgası ile kırma"},
                        {"text": "< 20 mm, dansitesi düşük böbrek taşları", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Retrograd İntrarenal Cerrahi (RIRC)", "isMasked": False, "hint": ""},
                        {"text": "Fleksibl üreteroskop ve Holmium lazer", "isMasked": True, "hint": "Doğal idrar yolundan bükülebilir aletle lazerleme"},
                        {"text": "Üreter taşları ve 10-20 mm kaliks taşları", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Perkütan Nefrolitotomi (PCNL)", "isMasked": False, "hint": ""},
                        {"text": "Sırttan böbreğe perkütan nefroskopik giriş", "isMasked": True, "hint": "1 cm kesiyle kalikse doğrudan kanal açılması"},
                        {"text": "> 20 mm dev staghorn veya kompleks taşlar", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "20 mm'den büyük kompleks veya staghorn böbrek taşlarında sırt bölgesinden perkütan kanal oluşturularak uygulanan cerrahi yöntem nedir?",
                "Perkütan nefrolitotomidir (PCNL).",
                "Böbrek taşının ciltten girilerek çıkarılması ameliyatı"
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-11-s95",
        "title": "Retroperitoneal Fibrozis (Ormond Hastalığı) Tedavi İlkeleri",
        "content": "Retroperitoneal Fibrozis (RPF / Ormond Hastalığı), abdominal aorta ve iliak damarları saran kronik inflamatuar ve sklerotik bir bağ dokusu plağının üreterleri bilateral olarak içe doğru çekip (medyale deviasyon) sıkıştırmasıyla karakterizedir. Olguların önemli bir kısmı IgG4-ilişkili sistemik hastalık spektrumundadır. Tedavi stratejisi:\n\n- **Akut Drenaj:** Üremi varlığında önce bilateral JJ stent veya perkütan nefrostomi yerleştirilir.\n- **Medikal İmmünsüpresif Tedavi:** Erken aktif inflamatuar evrede sistemik **kortikosteroidler (prednizolon)** ve tamoksifen veya azatioprin/mikofenolat mofetil plağın gerilemesini sağlar.\n- **Cerrahi Üreterolizis:** Medikal tedaviye yanıtsız veya olgunlaşmış fibrozis olgularında laparoskopik veya açık yöntemle üreterler sklerotik plağın içinden serbestleştirilir (üreterolizis). Fibrozisin üreterleri tekrar sarmasını engellemek için vaskülarize büyük omentum üreterlerin etrafına sarılır (omentoplasti / omental wrapping).",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Retroperitoneal Fibrozis Tedavi Aşamaları",
                [
                    "1. Acil Drenaj: Bilateral üreteral stentleme ile böbreklerin rahatlatılması",
                    "2. İmmünsüpresif Protokol: Yüksek doz steroid ve tamoksifen ile plağın baskılanması",
                    "3. Cerrahi Üreterolizis: Dirençli olgularda üreterin fibrotik skardan diseke edilmesi",
                    "4. Omentoplasti: Nüksü önlemek için canlı omentumun üreter etrafına sarılması"
                ]
            ),
            make_recall(
                "Retroperitoneal fibrozis cerrahisinde serbestleştirilen üreterlerin nüks skar dokusuyla tekrar sarılmasını önlemek için etrafına sarılan vasküler doku nedir?",
                "Büyük omentumdur (omentoplasti).",
                "Karın içi koruyucu yağlı önlük dokusu"
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-11-s96",
        "title": "Gebelikte Obstrüksiyonun Konservatif ve İnvaziv Yönetimi",
        "content": "Gebelikte saptanan hidroüreteronefrozun büyük çoğunluğu (%80-90 sağ tarafta) progesteron ve büyüyen uterusun basısına bağlı benign fizyolojik bir süreçtir. Bu nedenle gebelerde asemptomatik dilatasyon tek başına cerrahi girişim endikasyonu değildir. Hastaya **sol yan yatış pozisyonu (lateral dekübit)** önerilir; bu pozisyonda gravür uterus sağ üreter üzerinden sola doğru yer değiştirerek mekanik basıyı rahatlatır ve bol hidrasyon sağlanır. Ancak şu komplikasyonlar geliştiğinde girişim zorunludur:\n\n1. Medikal tedaviye yanıtsız şiddetli dirençli renal kolik ağrısı,\n2. Eşlik eden ateşli üriner sistem enfeksiyonu (piyelonefrit / sepsis riski),\n3. Progresif böbrek fonksiyon bozukluğu.\n\nBu durumlarda ultrasonografi eşliğinde (radyasyonsuz) lokal anesteziyle **Double-J stent** veya **perkütan nefrostomi** takılarak gebelik güvenle miada ulaştırılır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "28 haftalık gebe kadın, sağ yan ağrısı ve USG'de sağda belirgin hidronefroz ile başvuruyor. Hastanın ateşi yok, lökositi normal, böbrek fonksiyonları tamamen fizyolojik sınırlarda.",
                "Bu aşamada hastaya önerilmesi gereken en uygun ilk basamak yaklaşım hangisidir?",
                [
                    {
                        "text": "Sol yan yatış pozisyonu ve konservatif hidrasyon takibi; enfeksiyon veya fonksiyon bozukluğu gelişmedikçe invaziv girişimden kaçınılması.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Fizyolojik gebelik hidronefrozu konservatif izlenir; sol yan yatış uterusun sağ üretere basısını azaltır."
                    },
                    {
                        "text": "Acil genel anestezi altında sağ böbreğe açık piyeloplasti yapılması.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Fizyolojik dilatasyonda gereksiz açık cerrahi fetal ve maternal mortaliteyi artırır."
                    },
                    {
                        "text": "Bebeğin derhal sezaryenle doğurtulması.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. 28 haftada prematürite riski vardır; basit hidronefroz doğum endikasyonu değildir."
                    }
                ]
            ),
            make_cloze(
                "Gebelikte sağ üreter basısını mekanik olarak rahatlatmak için hastaya sol yan yatıs pozisyonu önerilir.",
                "sol yan yatıs",
                "Uterusun basısını hafifleten lateral dekübit pozisyonu"
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-11-s97",
        "title": "Malign Ekstrensek Obstrüksiyonlarda Palyatif Drenaj ve Yaşam Kalitesi",
        "content": "İleri evre pelvik ve retroperitoneal malignitelerde (özellikle lokal ileri serviks kanseri, prostat kanseri, rektum karsinomu ve retroperitoneal lenfomalar) tümörün üreterleri dışarıdan sarması ve infiltre etmesi sonucu bilateral obstrüktif üropati ve akut/kronik böbrek yetmezliği tablosu gelişir. Bu onkolojik hastalarda üremik komayı önlemek ve hastanın hayat kurtarıcı sistemik kemoterapi/radyoterapi alabilmesini sağlamak amacıyla palyatif idrar drenajı zorunludur. Drenaj seçenekleri:\n\n- **Ekstra-Sert / Metalik Üreteral Stentler:** Dışarıdan tümör basısının yüksek olduğu durumlarda klasik polimer stentler kolayca ezilebilir; bu nedenle güçlendirilmiş veya hafızalı metalik stentler lümeni açık tutmada daha başarılıdır.\n- **Bilateral Perkütan Nefrostomi:** Retrograd stent geçirilemeyen olgularda kalıcı nefrostomi kateterleri hayat kurtarır. Ancak kateter bakım güçlüğü ve yaşam kalitesi hasta ve ailesiyle multidisipliner olarak tartışılarak karar verilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Malign Obstrüksiyonda Drenaj Yolları Karşılaştırması",
                "Metalik Üreteral Stentler",
                "Tümörün dış kompresyonuna dirençlidir, vücut içinde kaldığından torbasız yaşam konforu sunar.",
                "Perkütan Nefrostomi",
                "Stent takılamayan ileri tümörlerde hayat kurtarır fakat dış torba bakımı ve enfeksiyon riski taşır."
            ),
            make_recall(
                "İleri evre serviks veya pelvik kanserlerin üreteri dışarıdan sıkıştırdığı olgularda klasik stentlerin ezilmesini önleyen özel stent tipi hangisidir?",
                "Metalik veya takviyeli üreteral stentlerdir.",
                "Eksternal basıya dirençli metalik lümenli stentler"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-11-s98",
        "title": "Kronik Obstrüktif Nefropati Takibi ve KBY Profilaksisi",
        "content": "Obstrüksiyon cerrahi olarak açıldıktan sonra hastanın takibi bitmez; aksine kronik nefrolojik izlem süreci başlar. Obstrüktif süreç boyunca kaybedilen nefronlar yenilenemez; geriye kalan nefronlar hiperfiltrasyon hasarına ve glomerüloskleroza adaydır. Uzun dönem izlemde dört temel sütun yönetilmelidir:\n\n1. **Kan Basıncı Kontrolü:** Kalan nefronların korunması için kan basıncı 130/80 mmHg altında tutulmalıdır. Proteinüri varlığında düşük doz ACE inhibitörleri veya ARB'ler glomerül içi basıncı düşürür (ancak bilateral kritik darlıkta akut GFR düşüşüne dikkat edilmelidir).\n2. **Tuz ve Su Dengesi:** Kronik tübüler hasara bağlı tuz kaybettiren nefropatisi olanlarda aşırı tuz kısıtlaması hipovolemiye yol açabilir; hastanın elektrolit profili kişiselleştirilmelidir.\n3. **Asidoz Tedavisi:** Kronik metabolik asidoz kemik erimesini ve kas yıkımını hızlandırdığından oral sodyum bikarbonat replasmanı yapılır.\n4. **Nefrotoksik İlaçlardan Kaçınma:** NSAİİ'ler, aminoglikozidler ve gereksiz kontrast maddeler kesinlikle yasaklanmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Uzun Dönem Takip Parametresi", "Hedef ve Yönetim", "Önlenen Komplikasyon"],
                [
                    [
                        {"text": "Kan Basıncı", "isMasked": False, "hint": ""},
                        {"text": "< 130/80 mmHg (Antihipertansif tedavi)", "isMasked": True, "hint": "Hedef arteriyel kan basıncı düzeyi"},
                        {"text": "Glomerüler hiperfiltrasyon ve skleroz", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Serum Bikarbonatı", "isMasked": False, "hint": ""},
                        {"text": "> 22 mEq/L (Oral NaHCO3 desteği)", "isMasked": True, "hint": "Hedef plazma alkali rezervi"},
                        {"text": "Metabolik asidoz, osteomalazi ve kas erimesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Nefrotoksik İlaç Maruziyeti", "isMasked": False, "hint": ""},
                        {"text": "NSAİİ ve nefrotoksik ajanlardan tam kaçınma", "isMasked": True, "hint": "Böbreğe toksik ilaç kısıtlaması"},
                        {"text": "Geri dönüşümsüz akut KBY alevlenmesi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Kronik obstrüktif nefropatili hastaların uzun dönem izleminde kalan nefronları korumak için NSAİİ kullanımından kesinlikle kaçınılmalıdır.",
                "NSAİİ",
                "COX inhibitörü non-steroid ağrı kesici ilaç grubu"
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-11-s99",
        "title": "Çok Disiplinli Klinik Yaklaşım: Üroloji, Nefroloji ve Radyoloji Entegrasyonu",
        "content": "Obstrüktif üropatinin başarılı yönetimi tek bir branşın sınırlarını aşan, üçlü bir klinik koordinasyon gerektirir:\n\n- **Radyoloji / Girişimsel Radyoloji:** USG, Helikal Taş BT ve MRÜ ile obstrüksiyonun varlığını, lokalizasyonunu ve nedenini saniyeler içinde netleştirir. Cerrahiye uygun olmayan kritik veya septik olgularda acil perkütan nefrostomi (PNS) takarak böbreğin kurtarılmasında ilk köprüyü kurar.\n- **Üroloji:** Cerrahi, laparoskopik, robotik ve endoskopik yöntemlerle (TUR-P, HoLEP, URS, RIRC, PCNL, Pyeloplasti, Valv ablasyonu) tıkanıklığı kalıcı olarak ortadan kaldırır ve üriner traktusun antegrad akış geometrisini yeniden inşa eder.\n- **Nefroloji:** Obstrüksiyon öncesi ve sonrası akut böbrek hasarı, postobstrüktif diürezin sıvı-elektrolit resüsitasyonu, kalıcı tübüler asidoz ve konsantrasyon defektlerinin uzun dönem medikal takibini üstlenir.\n\nBu üç disiplinin uyumu nefron kaybını sıfırlayan en kritik organizasyondur.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Multidisipliner Obstrüksiyon Yönetim Zinciri",
                [
                    "1. Radyolojik Triyaj: USG ve Taş BT ile seviye ve hidronefrozun netleştirilmesi",
                    "2. Girişimsel/Ürolojik Dekompresyon: Acil kateter veya nefrostomi ile basıncın kırılması",
                    "3. Nefrolojik İzlem: Postobstrüktif diürez ve elektrolit imbalansının yönetimi",
                    "4. Kesin Cerrahi Onarım: Taş, BPH veya darlığın kalıcı endoürolojik rekonstrüksiyonu"
                ]
            ),
            make_recall(
                "Obstrüktif nefropatide postobstrüktif diürezin sıvı-elektrolit dengesini ve uzun dönem tübüler fonksiyon bozukluklarını yöneten uzmanlık dalı hangisidir?",
                "Nefrolojidir (veya Pediatrik Nefroloji).",
                "Böbrek iç hastalıkları tıbbi uzmanlık dalı"
            )
        ]
    })

    # Slide 100 (CHECKPOINT 10 - FINAL ENTEGRASYON)
    slides.append({
        "id": "k1-11-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Üriner Obstrüksiyonun Bütüncül Özeti ve Final Entegrasyonu",
        "content": "Üriner Obstrüksiyonun Fizyopatolojisi dersinin 100 slaytlık tam entegrasyonu ve tüm kardinal sınav noktaları:\n\n1. **Tanım ve Seviye:** Tübülden meaya her düzeyde gelişebilir; proksimalinde staz ve basınç artar. Çocukta en sık PUV, erişkinde taş, yaşlıda BPH'dır.\n2. **Evreler:** İnfravezikalde kompanzasyon (PVR=0) → irritasyon (LUTS, PVR<50) → dekompansasyon (PVR>500, taşma inkontinansı, VUR).\n3. **Mesane Duvarı:** Tip III kollajen artışı kompliyansı yok eder; trabekülasyon, selül, sakkül ve divertikül oluşur.\n4. **Üst Sistem İlk Yanıt:** Kaliks forniksleri küntleşir, papilla düzleşir. 7. günde kollektör nekrozu başlar.\n5. **Koruyucu Reflüler:** En sık pyelointerstisyeldir; lenfatik ve pyelovenöz geri akım basıncı düşürür. Enfeksiyonda pyelovenöz yol sepsise yol açar.\n6. **Hemodinami ve İyileşme Sınırı:** Erken PGE2/NO vazodilatasyonu, geç TXA2/AngII vazokonstriksiyonu. Köpekte 2 hafta %46, 4 hafta %35, 6 hafta %0 dönüş.\n7. **Tübüler Defekt ve Spot:** ADH direnci, hipostenüri, poliüri ve asidifikasyon bozulur; ancak **üriner dilüsyon yeteneği ETKİLENMEZ**.\n8. **Acil ve POD:** Anüri ve piyonefroz acil drenajdır. Bilateral tıkanıklık açılınca solüt diürezi (POD) gelişir; çıkanın %50-70'i replase edilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Üriner obstrüksiyonun fizyopatolojisine dair aşağıdaki ifadelerden hangisi BÜTÜNCÜL OLARAK YANLIŞTIR?",
                [
                    {"key": "A", "text": "Obstrüksiyon giderildikten sonra konsantrasyon kapasitesi çökse dahi üriner dilüsyon yeteneği etkilenmez.", "explanation": "A seçeneği doğrudur: Ders notunun en temel kardinal kuralıdır."},
                    {"key": "B", "text": "Üst üriner sistem obstrüksiyonunda hidrostatik basınç artışından ilk etkilenen yer kalikslerdir.", "explanation": "B seçeneği doğrudur: Forniks küntleşmesi ve papilla düzleşmesi ilk bulgudur."},
                    {"key": "C", "text": "Deneysel çalışmalara göre 6 haftalık tam üreter obstrüksiyonu sonrası dekompresyonla GFR tamamen normale döner.", "explanation": "C seçeneği BÜTÜNCÜL OLARAK YANLIŞTIR: 6 haftalık tam tıkanıklık sonrası geri dönen hiçbir fonksiyon kalmaz (%0 GFR)."},
                    {"key": "D", "text": "Postobstrüktif diürezde iatrojenik poliüriyi önlemek için IV sıvı replasmanı çıkanın %50-70'i oranında tutulmalıdır.", "explanation": "D seçeneği doğrudur: Fazla sıvı vermek sonsuz diürez döngüsü yaratır."},
                    {"key": "E", "text": "İnfravezikal obstrüksiyonun kompanzasyon evresinde postmiksiyonel rezidüel idrar kalmaz.", "explanation": "E seçeneği doğrudur: Detrüsör hipertrofisi erken dönemde tam boşalmayı sağlar."}
                ],
                "C"
            ),
            make_cloze(
                "Tam üreter obstrüksiyonunda altıncı haftadan sonra toplayıcı sistem acılsa dahi geri dönen hiçbir filtrasyon fonksiyonu kalmaz.",
                "hiçbir filtrasyon fonksiyonu",
                "Tam kayıp ve sıfırlanma durumunu simgeleyen kavram"
            )
        ]
    })

    return slides
