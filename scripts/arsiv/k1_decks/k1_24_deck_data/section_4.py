# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 4: Özel Emboli Tipleri II: Gaz Embolisi, Dekompresyon Hastalığı ve Nadir Emboliler (Slayt 31 - 40)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # Slayt 31: Gaz ve Hava Embolisi Tanımı ve Fiziksel Etkisi
    slides.append({
        "id": "k1-24-s31",
        "title": "Gaz ve Hava Embolisi Tanımı: Fiziksel Dinamikler ve Mekanik Tıkanma",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 31,
        "narrative": (
            "Dolaşım sistemi içinde sıvı kan yerine gaz kabarcıklarının bulunması hemodinamik bir felakete yol açar: "
            "1. **Gaz Embolisi Tanımı:** Atmosferik havanın veya kanda çözünmüş gazların dolaşıma karışarak, "
            "kılcal ve büyük damarlarda lümeni tıkayan gaz kabarcıkları (köpük kütlesi) oluşturmasıdır. "
            "2. **Fiziksel Özellikler:** Gaz kabarcıkları sıkıştırılabilir (kompresibl) niteliktedir; "
            "bu durum kalp odacıklarında veya damarlarda bir piston gibi çalışan kan akımını kesintiye uğratır. "
            "Küçük kabarcıklar birleşerek büyük hava cepleri oluşturur ve kanın ilerlemesini mekanik olarak bloke eder. "
            "3. **Tıkanma Bölgeleri:** "
            "- **Venöz Hava Embolisi:** Venlerden girip sağ kalbe ve pulmoner kapiller yatağa ulaşır. "
            "- **Arteriyel Hava Embolisi:** Akciğer venleri veya sol kalpten girip koroner ve serebral arterleri tıkayarak anında inme ve MI yapar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Dolaşım sistemine giren gaz kabarcıklarının damar lümenini tıkayarak kan akımını durdurması olayına gaz ve hava embolisi adı verilir.",
                "hava embolisi",
                "Damar lümenine atmosferik havanın girmesiyle oluşan emboli türü"
            ),
            make_table(
                "Venöz ve Arteriyel Hava Embolisinin Karşılaştırmalı Özellikleri",
                ["Özellik", "Venöz Hava Embolisi", "Arteriyel Hava Embolisi"],
                [
                    ["Giriş Kapısı", "Boyun venleri, santral venöz kateter, pelvis venleri", "Açık kalp cerrahisi, torasik travma, pulmoner venler"],
                    ["İlk Ulaştığı Yer", "Sağ ventrikül ve pulmoner arterler", "Aorta, serebral ve koroner arterler"],
                    [
                        "Kritik Sonuç",
                        "Sağ ventrikülde hava kilidi ve akut hipoksi",
                        {"text": "İskemik inme ve akut miyokard enfarktüsü", "isMasked": True, "hint": "Beyin ve kalp damarlarının hava kabarcığıyla tıkanması"}
                    ],
                    ["Ölümcül Hacim", "~100 - 150 ml hava", "Çok küçük hacimler (<1-2 ml dahi öldürücü)"]
                ]
            ),
            make_micro_quiz(
                "Dolaşım sistemine giren gaz kabarcıklarının arteriyel dolaşıma ulaşarak doğrudan beyin veya koroner arterleri tıkaması (arteriyel hava embolisi) en sık hangi klinik girişim sırasında gelişir?",
                {
                    "A": "Kardiyopulmoner baypas kullanılan açık kalp cerrahisi veya pulmoner venöz travmalar",
                    "B": "Yüzeysel cilt biyopsisi",
                    "C": "Ayak tırnağı çekimi",
                    "D": "Rutin intramüsküler aşı enjeksiyonu",
                    "E": "Periferik koldan kan gazı alınması"
                },
                "A",
                {
                    "A": "Açık kalp cerrahisinde kardiyopulmoner baypas cihazları veya pulmoner ven yaralanmaları arteriyel sisteme hava kaçırabilir.",
                    "B": "Cilt biyopsisi arteriyel hava embolisi yapmaz.",
                    "C": "Tırnak çekimi kapillerdir.",
                    "D": "Aşı kas içine yapılır, majör hava embolisi yapmaz.",
                    "E": "Kan gazı arterden enjektöre çekilir, içeri hava verilmez."
                }
            )
        ]
    })

    # Slayt 32: İyatrojenik ve Travmatik Hava Embolisi Nedenleri
    slides.append({
        "id": "k1-24-s32",
        "title": "İyatrojenik ve Travmatik Hava Embolisi Nedenleri",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 32,
        "narrative": (
            "Hava embolisi, hastane ortamında çoğu zaman önlenebilir iyatrojenik kazalar veya travmalar sonucu ortaya çıkar: "
            "1. **Santral Venöz Kateter (SVK) Girişimleri:** "
            "Vena jugularis interna veya vena subclavia kateterizasyonu sırasında kateter kapağının açık unutulması, "
            "kateterin çekilmesi anında hastanın derin nefes alması veya hava sızdırması içeri hızla hava emilmesine neden olur. "
            "2. **Baş, Boyun ve Toraks Cerrahisi:** "
            "Baş ve boyun venlerinde yerçekimi ve negatif intratorasik basınç nedeniyle ven içi basınç subatmosferiktir (negatiftir). "
            "Büyük bir boyun veni kesildiğinde dışarı kan akmaz, tam aksine içeriye hızla atmosferik hava emilir! "
            "3. **Laparoskopik Cerrahi:** Abdomen içine $\\text{CO}_2$ gazı verilirken iğnenin yanlışlıkla bir vene girmesi. "
            "4. **Obstetrik Girişimler:** Doğum veya küretaj sırasında genişlemiş myometrial venöz pleksuslardan hava girişi."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Boyun ve toraks cerrahisinde büyük venlerdeki basıncın negatif olması nedeniyle damar kesildiğinde dışarı kanamak yerine içeriye hızla atmosferik hava emilir.",
                "negatif",
                "Atmosfer basıncından düşük olan intratorasik venöz basınç düzeyi"
            ),
            make_table(
                "Hava Embolisi İyatrojenik Nedenleri ve Önleme Stratejileri",
                ["Klinik Durum", "Hava Giriş Mekanizması", "Önleyici Klinik Manevra"],
                [
                    [
                        "Santral Venöz Kateter",
                        "Kateter takılması/çekilmesinde hava girişi",
                        {"text": "Hastaya Trendelenburg ve Valsalva manevrası yaptırmak", "isMasked": True, "hint": "Venöz basıncı artırarak içeri hava kaçmasını önleme"}
                    ],
                    ["Boyun Cerrahisi", "Negatif basınçlı juguler ven kesilmesi", "Damarların derhal klemplenmesi"],
                    ["Laparoskopi", "İğnenin damar içine gaz üflemesi", "Veress iğnesi aspirasyon testi"]
                ]
            ),
            make_micro_quiz(
                "Yoğun bakımda yatan bir hastanın subklavian venöz kateteri çıkarılırken hastanın derin bir nefes alması (içe çekmesi) sonrası aniden dispne, siyanoz ve kollaps gelişmiştir. Bu klinik tablonun fizyopatolojik gerekçesi hangisidir?",
                {
                    "A": "Derin inspirasyonla göğüste negatif basınç oluşarak kateter giriş yerinden ven içine hava emilmesi",
                    "B": "Hastada ani aort diseksiyonu gelişmesi",
                    "C": "Hastanın kan grubunun uyuşmaması",
                    "D": "Kemik iliği yağının vena cavaya akması",
                    "E": "Akut apandisit rüptürü"
                },
                "A",
                {
                    "A": "İnspirasyonda plevral negatif basınç artar ve açık ven deliğinden lümene hava çekilerek hava embolisi oluşur.",
                    "B": "Aort diseksiyonu kateter çekilmesiyle oluşmaz.",
                    "C": "Kan uyuşmazlığı transfüzyonda olur.",
                    "D": "Yağ kemik kırığında olur.",
                    "E": "Apandisit batın patolojisidir."
                }
            )
        ]
    })

    # Slayt 33: Kalpte Hava Kilidi (Air Lock) ve Ölümcül Hacim
    slides.append({
        "id": "k1-24-s33",
        "title": "Kalpte 'Hava Kilidi' (Air Lock) Mekanizması ve Ölümcül Eşik Hacim",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 33,
        "narrative": (
            "Venöz hava embolisinin öldürücü mekanizması sağ ventriküldeki mekanik 'hava kilidi'dir: "
            "1. **Ölümcül Hacim Sınırı:** Venöz dolaşıma aniden giren **>100 ml hava (yaklaşık 100 - 150 ml)** genellikle ölümcüldür. "
            "(Yavaş infüzyonla verilen küçük hava kabarcıkları kanda çözünebilir veya akciğerden atılabilir). "
            "2. **Hava Kilidi (Air Lock) Mekanizması:** "
            "Büyük hacimli hava sağ atriyumdan sağ ventriküle akar. Ventrikül sistolde kasıldığında, "
            "sıkıştırılamayan sıvı kan yerine **sıkışabilen elastik havayı köpürtmeye başlar**; triküspid ve pulmoner kapakların açılma mekanizması bozulur. "
            "Ventrikül içi köpük tıkacı pulmoner arter çıkış yolunu (RVOT) tamamen kapatır. "
            "3. **Klinik ve Tedavi:** Pulmoner kan akımı durur, kardiyak debi anında sıfırlanır, stetoskopla kalpte 'çalkantı / değirmen taşı sesi' (mill-wheel murmur) duyulur. "
            "**Acil Müdahale (Durant Pozisyonu):** Hasta derhal **sol yan pozisyona ve Trendelenburg (baş aşağı)** eğimine alınır; "
            "böylece hafif olan hava sağ ventrikül apeksinde yükselerek çıkış yolunu serbest bırakır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Sağ ventriküle aniden giren yüksek hacimli havanın pulmoner arter çıkış yolunu köpük oluşturarak kapatması tablosuna hava kilidi denir.",
                "hava kilidi",
                "Sağ ventrikülün kan pompalayamayıp köpük tıkacıyla tıkanması mekanizması"
            ),
            make_table(
                "Hava Kilidi Patolojisi ve Acil Yönetim Basamakları",
                ["Patolojik Durum", "Ventriküler Etki", "Acil Kurtarma Müdahalesi"],
                [
                    ["100 ml Üzeri Ani Hava Girişi", "Sağ ventrikülde köpük kitlesi oluşması", "Hava giriş yolunun derhal kapatılması"],
                    [
                        "RVOT Obstrüksiyonu",
                        "Pulmoner kapağın açılamaması",
                        {"text": "Sol yan Trendelenburg pozisyonu (Durant manevrası)", "isMasked": True, "hint": "Havayı sağ ventrikül apeksinde hapsedip çıkışı açan pozisyon"}
                    ],
                    ["Kardiyak Debi Sıfırlanması", "Sol kalbe kan dönüşünün durması", "Santral kateterden havanın enjektörle aspire edilmesi"]
                ]
            ),
            make_micro_quiz(
                "Hava embolisi şüphesiyle aniden kollaps gelişen ve kalbinde değirmen taşı üfürümü (mill-wheel murmur) duyulan bir hastada, havanın pulmoner çıkış yolunu tıkamasını engellemek için derhal verilmesi gereken hayat kurtarıcı pozisyon hangisidir?",
                {
                    "A": "Sol yan dekübit ve Trendelenburg (Baş aşağı) pozisyonu",
                    "B": "Sağ yan dik oturur pozisyon",
                    "C": "Sırtüstü düz yatar (supin) pozisyon",
                    "D": "Yüzüstü (prone) pozisyon",
                    "E": "Fowler (yarı oturur) pozisyon"
                },
                "A",
                {
                    "A": "Sol yan Trendelenburg pozisyonu havayı sağ ventrikül apeksinde tutarak pulmoner kapağın açılmasını sağlar.",
                    "B": "Sağ yan hava çıkış yolunu daha çok tıkar.",
                    "C": "Supin pozisyonda hava pulmoner çıkışta kalır.",
                    "D": "Prone pozisyonda kalp resüsitasyonu yapılamaz.",
                    "E": "Oturur pozisyonda hava yukarı kaçıp çıkış yolunu tıkar."
                }
            )
        ]
    })

    # Slayt 34: Dekompresyon Hastalığı Fizyopatolojisi (Henry Kanunu)
    slides.append({
        "id": "k1-24-s34",
        "title": "Dekompresyon Hastalığı Fizyopatolojisi: Henry Kanunu ve Azot Kabarcıkları",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 34,
        "narrative": (
            "Dalgıçlarda ve derin tünel işçilerinde görülen Dekompresyon Hastalığı (Vurgun), temel bir gaz fiziği yasasına dayanır: "
            "1. **Henry Kanunu:** 'Bir sıvıda çözünen gaz miktarı, o gazın sıvının üzerindeki kısmi basıncıyla doğru orantılıdır.' "
            "2. **Derin Dalışta Basınç Artışı:** Bir dalgıç denizin derinliklerine indikçe (her 10 metrede ortam basıncı 1 atmosfer artar), "
            "soluduğu havadaki **Azot (Nitrojen - $N_2$) gazı** yüksek basınç altında kanda, doku sıvılarında ve özellikle yağ dokusunda çözünür. "
            "(Azot yağda son derece yüksek çözünürlüğe sahiptir). "
            "3. **Hızlı Çıkış (Ani Dekompresyon):** Dalgıç su yüzeyine **aniden ve basamaklı dekompresyon duraklarını yapmadan** hızla çıktığında, "
            "ortam basıncı süratle düşer. "
            "Tıpkı kapağı aniden açılan gazlı içecek şişesinde gazın köpürmesi gibi, kanda ve dokularda çözünmüş olan azot sıvı fazdan çıkarak "
            "milyonlarca mikroskobik **azot gazı kabarcığına** dönüşür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Dekompresyon hastalığında derin dalıştan su yüzeyine hızlı çıkış sırasında basıncın aniden düşmesiyle kanda kabarcık oluşturan gaz azottur.",
                "azottur",
                "Vurgun tablosunda çözünmüş sıvı halden gaz kabarcığına dönüşen inert gaz"
            ),
            make_table(
                "Henry Kanunu ve Dekompresyon Fizikokimyasal Evreleri",
                ["Evre / Durum", "Ortam Basıncı", "Azot Gazının Fiziksel Hali", "Dokudaki Karşılığı"],
                [
                    ["Deniz Yüzeyi", "1 Atmosfer", "Normal fizyolojik çözünürlük", "Doku ve kanda denge halinde"],
                    [
                        "Derin Dalış (Örn. 40 m)",
                        "5 Atmosfer",
                        {"text": "Aşırı miktarda çözünmüş sıvı faz", "isMasked": True, "hint": "Yüksek basınç altında kanda ve yağda depolanan azot"},
                        "Yağ dokusu ve miyelinde yüksek azot birikimi"
                    ],
                    ["Ani Yüzeye Çıkış", "1 Atmosfere ani düşüş", "Sıvıdan kontrolsüz gaz kabarcığına geçiş", "Kanda ve eklemlerde köpürme (Vurgun)"]
                ]
            ),
            make_micro_quiz(
                "Tüplü dalış (scuba) yapan bir sporcunun 35 metre derinlikten panikleyerek su yüzeyine çok hızlı çıkması sonucunda kanda ve dokularda kabarcıklar oluşturarak dekompresyon hastalığına (vurgun) yol açan primer gaz hangisidir?",
                {
                    "A": "Azot (Nitrojen)",
                    "B": "Oksijen",
                    "C": "Karbondioksit",
                    "D": "Helyum",
                    "E": "Karbonmonoksit"
                },
                "A",
                {
                    "A": "Henry kanunu gereğince yüksek basınçta çözünüp ani çıkışta kabarcık oluşturan gaz azottur.",
                    "B": "Oksijen dokularda metabolize edilir, inert gaz gibi kabarcık oluşturmaz.",
                    "C": "Karbondioksit bikarbonat olarak tamponlanır.",
                    "D": "Helyum özel karışımlarda kullanılır, normal dalışta primer azot suçludur.",
                    "E": "Karbonmonoksit toksik zehir gazıdır."
                }
            )
        ]
    })

    # Slayt 35: Akut Dekompresyon Kliniği: Bends ve Chokes
    slides.append({
        "id": "k1-24-s35",
        "title": "Akut Dekompresyon Kliniği: 'The Bends', 'The Chokes' ve SSS Tutulumu",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 35,
        "narrative": (
            "Akut dekompresyon hastalığında gaz kabarcıklarının yerleştiği dokulara özgü klasik semptomlar gelişir: "
            "1. **'The Bends' (Kıvrılma / Bükülme):** "
            "Azot kabarcıkları periartiküler dokularda, eklem kapsüllerinde, tendon ve iskelet kaslarında toplanır. "
            "Özellikle diz, omuz ve dirseklerde dayanılmaz, kıvrandırıcı bir eklem ağrısına yol açar; "
            "hasta ağrıyı hafifletmek için iki büklüm olur ('bends' adı buradan gelir). Olguların %70-80'inde görülür. "
            "2. **'The Chokes' (Boğulma):** "
            "Gaz kabarcıkları pulmoner kapiller yatağa hücum ederek mikrosirkülasyonu tıkar. "
            "Hastada şiddetli substernal göğüs ağrısı, inatçı öksürük krizleri, taşipne, dispne ve pulmoner ödem tablosu patlar. "
            "3. **Santral Sinir Sistemi Tutulumu:** "
            "Spinal kordun beyaz cevherinde (miyelinden zengin lipofilik alan) azot kabarcıkları iskemik nekroza yol açarak "
            "parapleji (bacaklarda felç) ve sfinkter kusurları yapabilir; beyinde koma ve nörolojik defisitler gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Akut dekompresyon hastalığında azot kabarcıklarının eklem kapsülleri ve kaslarda toplanarak dayanılmaz bükücü ağrı yapmasına the bends adı verilir.",
                "the bends",
                "Vurgun yiyen dalgıçta iki büklüm eklem ağrısı tablosu"
            ),
            make_table(
                "Akut Dekompresyon Hastalığı Klinik Formları",
                ["Klinik Tablo", "Tutulan Organ / Doku", "Karakteristik Semptomlar"],
                [
                    ["The Bends", "Diz, omuz, dirsek eklemleri ve kaslar", "Şiddetli kıvrandırıcı eklem ağrısı, pozisyon alma"],
                    [
                        "The Chokes",
                        "Pulmoner kapiller mikrodolaşım",
                        {"text": "Substernal göğüs yanması, öksürük krizi, dispne", "isMasked": True, "hint": "Akciğer damarlarının gazla tıkanması sonucu solunum sıkıntısı"}
                    ],
                    ["Spinal Form", "Spinal kord beyaz cevheri (miyeloid iskemi)", "Paraparezi, parapleji, duyu kaybı"],
                    ["Serebral Form", "Beyin kortikal arteriyolleri", "Görme kaybı, konfüzyon, nöbet, koma"]
                ]
            ),
            make_micro_quiz(
                "Derin dalıştan hızla su yüzeyine çıkan bir dalgıçta 1 saat sonra başlayan ve 'The Chokes' olarak tanımlanan klinik tablonun primer patolojisi hangisidir?",
                {
                    "A": "Pulmoner mikrodolaşımda toplanan azot gazı kabarcıklarının dispne ve öksürüğe yol açması",
                    "B": "Koroner arterde aterom plağı yırtılması",
                    "C": "Mide duvarında perforasyon",
                    "D": "Böbrek taşının üreteri tıkaması",
                    "E": "Safra kesesinde taş koliği"
                },
                "A",
                {
                    "A": "The chokes, azot kabarcıklarının akciğer kapillerlerini tıkamasıyla gelişen substernal ağrı, dispne ve öksürük tablosudur.",
                    "B": "Aterom plağı aterosklerozdur.",
                    "C": "Mide perforasyonu dalışa özgü akut gaz embolisi tablosu değildir.",
                    "D": "Üreter taşı renal koliğe yol açar.",
                    "E": "Safra taşı kolesistittir."
                }
            )
        ]
    })

    # Slayt 36: Kronik Dekompresyon Hastalığı (Caisson Hastalığı)
    slides.append({
        "id": "k1-24-s36",
        "title": "Kronik Dekompresyon Hastalığı: Caisson Hastalığı ve Avasküler Nekroz",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 36,
        "narrative": (
            "Dekompresyonun kronik formu, sürekli su altı tünel ve köprü inşaatlarında çalışan işçilerde (Caisson işçileri) tanımlanmıştır: "
            "1. **Caisson Hastalığı Tanımı:** Tekrarlayan veya yetersiz tedavi edilmiş dekompresyon olayları sonucu "
            "kemik iliğinde ve iskelet sisteminde kalıcı iskemik hasarların birikmesidir. "
            "2. **Aseptik Kemik Nekrozu (Avasküler / İskemik Kemik Nekrozu):** "
            "Kemik iliğindeki zengin yağ dokusu azotu depolar. Tekrarlayan gaz mikroembolileri kemik içi terminal arteriyolleri tıkar. "
            "Beslenemeyen kemik iliğinde ve kemik trabeküllerinde **koagülatif nekroz** gelişir. "
            "3. **En Sık Tutulan Bölgeler:** "
            "- **Femur Başı ve Boynu** "
            "- **Tibia Proksimal Epifizi** "
            "- **Humerus Başı** "
            "4. **Klinik Sonuç:** Subkondral kemik desteği çöker; üzerindeki eklem kıkırdağı kırılır ve "
            "şiddetli sakatlık yaratan sekonder osteoartrit (eklem harabiyeti) tablosuna yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Kronik dekompresyon hastalığı olan Caisson hastalığında tekrarlayan azot embolileri kemik epifizlerinde aseptik kemik nekrozuna yol açar.",
                "aseptik kemik nekrozuna",
                "Kemik başlarında mikrodamar tıkanmasına bağlı gelişen iskemik doku ölümü"
            ),
            make_table(
                "Akut ve Kronik Dekompresyon Hastalığı Karşılaştırması",
                ["Özellik", "Akut Dekompresyon Hastalığı", "Kronik Dekompresyon (Caisson Hastalığı)"],
                [
                    ["Maruziyet", "Tek bir hızlı dalış/yüzeye çıkış atağı", "Aylar/yıllar süren tekrarlayan dekompresyonlar"],
                    ["Temel Lezyon", "Eklemlerde 'bends', akciğerde 'chokes'", "Uzun kemik epifizlerinde avasküler kemik nekrozu"],
                    [
                        "En Sık Bölge",
                        "Diz, omuz, akciğer mikrodolaşımı",
                        {"text": "Femur başı, tibia ve humerus başı", "isMasked": True, "hint": "Aseptik nekrozun en sık görüldüğü kemik eklem bölgeleri"}
                    ],
                    ["Kalıcı Sonuç", "Erken tedaviyle tam kür", "Eklem kıkırdağının çökmesi ve sekonder osteoartrit"]
                ]
            ),
            make_micro_quiz(
                "Yıllardır köprü ayakları su altı inşaatında (keson/caisson işçisi) çalışan 45 yaşındaki bir işçide her iki kalça ekleminde kronik ağrı ve hareket kısıtlılığı gelişmiştir. Manyetik rezonans (MR) görüntülemede bilateral femur başında saptanması beklenen patolojik lezyon hangisidir?",
                {
                    "A": "Aseptik (Avasküler) İskemik Kemik Nekrozu",
                    "B": "Osteosarkom tümör kitlesi",
                    "C": "Piyojenik bakteriyel osteomiyelit",
                    "D": "Romatoid artrit pannus dokusu",
                    "E": "Kemik kisti ve osteomalazi"
                },
                "A",
                {
                    "A": "Caisson hastalığında tekrarlayan gaz embolileri femur başında avasküler (aseptik) nekroz yapar.",
                    "B": "Osteosarkom malign kemik tümörüdür.",
                    "C": "Osteomiyelit bakteriyel iltihaptır.",
                    "D": "Romatoid artrit otoimmün sinovittir.",
                    "E": "Osteomalazi D vitamini eksikliğidir."
                }
            )
        ]
    })

    # Slayt 37: Dekompresyon Hastalığında Acil Tedavi: Hiperbarik Oksijen
    slides.append({
        "id": "k1-24-s37",
        "title": "Dekompresyon Hastalığında Tedavi: Rekompresyon ve Hiperbarik Oksijen",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 37,
        "narrative": (
            "Dekompresyon hastalığı, nedene yönelik fiziksel tedavisi olan nadir emboli tablolarındandır: "
            "1. **Rekompresyon (Yüksek Basınç Odası):** Hastaya yapılacak ilk ve hayat kurtarıcı müdahale "
            "derhal özel bir **Rekompresyon / Basınç Odasına (Hyperbaric Chamber)** alınmasıdır. "
            "2. **Gaz Fizyolojisinin Tersine Çevrilmesi:** "
            "Odada ortam basıncı hızla yükseltilir (hastanın daldığı derinlikteki basınca denk getirilir). "
            "Henry kanunu gereğince, damarları ve dokuları tıkayan **gaz halindeki azot kabarcıkları küçülür ve tekrar kanda sıvı fazda çözünür**; "
            "böylece doku perfüzyonu anında geri döner. "
            "3. **Kademeli Yavaş Dekompresyon:** Basınç odasındaki basınç saatler veya günler boyunca çok yavaş ve basamaklı olarak düşürülür; "
            "bu sırada hastaya **%100 Hiperbarik Oksijen** solutularak doku hipoksisi düzeltilir ve azotun akciğer yoluyla güvenle atılması sağlanır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Dekompresyon hastalığının kesin tedavisi hastanın yüksek basınç odasına alınarak gaz kabarcıklarının yeniden kanda çözünmesini sağlayan rekompresyon tedavisidir.",
                "rekompresyon",
                "Ortam basıncını artırarak gaz kabarcığını eriten fiziksel tedavi yöntemi"
            ),
            make_table(
                "Basınç Odası (Rekompresyon) Tedavisinin Mekanizmaları",
                ["Tedavi Bileşeni", "Fiziksel / Biyolojik Etki", "Klinik İyileşme Sonucu"],
                [
                    ["Yüksek Ortam Basıncı", "Gaz kabarcıklarının hacmini küçültüp eritme", "Tıkalı kılcal damarlarda kan akımının yeniden başlaması"],
                    [
                        "%100 Hiperbarik Oksijen",
                        {"text": "Plazmada çözünmüş oksijen miktarını dramatik artırma", "isMasked": True, "hint": "Eritrositlerden bağımsız plazma oksijenasyonu"},
                        "İskemik doku hipoksisinin hızla gerilemesi"
                    ],
                    ["Kademeli Yavaş Çıkış", "Azotun akciğer alveollerinden atılmasını sağlama", "Yeni kabarcık oluşumunun tamamen engellenmesi"]
                ]
            ),
            make_micro_quiz(
                "Dalış sonrası akut nefes darlığı (the chokes) ve şiddetli eklem ağrıları (the bends) ile acil servise getirilen bir dalgıca uygulanması gereken en acil ve kesin spesifik tedavi yöntemi hangisidir?",
                {
                    "A": "Rekompresyon odasında hiperbarik basınç ve oksijen tedavisi",
                    "B": "Yalnızca intravenöz antibiyotik başlanması",
                    "C": "Acil kemik iliği nakli",
                    "D": "Torasik cerrahi ile akciğer rezeksiyonu",
                    "E": "Tüm eklemlere intraartiküler kortizon enjeksiyonu"
                },
                "A",
                {
                    "A": "Rekompresyon odası azot kabarcıklarını tekrar sıvı fazda çözerek kesin tedavi sağlar.",
                    "B": "Antibiyotik enfeksiyon içindir, gaz kabarcığını eritmez.",
                    "C": "Kemik iliği nakli gerekmez.",
                    "D": "Cerrahi rezeksiyon endike değildir.",
                    "E": "Kortizon gaz kabarcığını yok etmez."
                }
            )
        ]
    })

    # Slayt 38: Diğer Emboli Tipleri: Tümör Embolisi ve Yabancı Cisimler
    slides.append({
        "id": "k1-24-s38",
        "title": "Diğer Emboli Tipleri: Tümör Embolisi ve Yabancı Cisimler",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 38,
        "narrative": (
            "Klinik pratikte karşılaşılan diğer spesifik emboli tipleri şunlardır: "
            "1. **Tümör Embolisi (Hematolojik Metastaz):** "
            "Malign neoplazmlar çevre damar duvarlarını eriterek venöz veya arteriyel lümene girer. "
            "Damar içinde tek tek veya kümeler halinde yüzen tümör hücreleri (tümör embolusları), "
            "trombositler ve fibrinle kaplanarak kendilerini immün sistemden korur. "
            "Uzak organ kapiller yatağına oturduklarında damarı tıkayıp mikro-enfarktüs yapabilir veya "
            "damar dışına çıkarak **metastatik tümör odakları** kurarlar. "
            "2. **Yabancı Cisim Embolisi (İntravenöz Madde Bağımlılığı):** "
            "Damar içi uyuşturucu kullanan bireyler, suda erimeyen katkı maddelerini (talk pudrası, mısır nişastası, selüloz) "
            "damar içine enjekte ederler. "
            "Bu partiküller akciğer kapillerlerine takılarak mikro-embolizasyon yapar; "
            "zamanla yabancı cisim dev hücreleri içeren **granülomatöz vaskülit ve pulmoner hipertansiyona** yol açar. "
            "Kutup mikroskobunda parlayan talk kristalleri (birefringence) patognomoniktir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "İntravenöz madde bağımlılarında enjekte edilen katkı maddelerinin akciğer damarlarını tıkamasıyla gelişen yabancı cisim embolisinde polarize ışık mikroskobunda çift kıran talk kristalleri izlenir.",
                "talk kristalleri",
                "Yabancı cisim granülomunda çift kırınım (birefringence) gösteren kristal partiküller"
            ),
            make_table(
                "Nadir Emboli Tipleri ve Patolojik Karakteristikleri",
                ["Emboli Türü", "Tipik Etyolojik Neden", "Tanısal Histolojik Görünüm"],
                [
                    ["Tümör Embolisi", "Malign epiteliyal karsinomlar", "Damar lümeninde atipik mitotik tümör kümeleri"],
                    [
                        "Talk / Yabancı Cisim Embolisi",
                        "İV ilaç bağımlılığı (enjeksiyon katkısı)",
                        {"text": "Yabancı cisim dev hücreleri içinde parlak kristal partiküller", "isMasked": True, "hint": "Polarize mikroskopta parlayan egzojen cisimler"}
                    ],
                    ["Kolesterol Embolisi", "Komplike aort aterosklerozu", "Damar içinde boşluk bırakan iğsi kolesterol kleftleri"]
                ]
            ),
            make_micro_quiz(
                "İntravenöz eroin bağımlılığı öyküsü olan 35 yaşındaki bir hastanın akciğer biyopsisinde küçük pulmoner arterler çevresinde multinükleer dev hücreler içeren granülomlar ve polarize ışık mikroskobunda çift kırınım (parlama) gösteren partiküller saptanmıştır. Bu tablo hangi emboli türüne işaret eder?",
                {
                    "A": "Yabancı Cisim (Talk) Embolisi",
                    "B": "Amniyon Sıvısı Embolisi",
                    "C": "Gaz Embolisi",
                    "D": "Kemik İliği Embolisi",
                    "E": "Safra Embolisi"
                },
                "A",
                {
                    "A": "İV bağımlılarda talk pudrası yabancı cisim granülomatöz reaksiyonu ve polarize mikroskopta parlama yapar.",
                    "B": "Amniyon sıvısında fetal hücreler vardır.",
                    "C": "Gaz mikroskopta gaz boşluğudur, granülom yapmaz.",
                    "D": "Kemik iliğinde hematopoetik hücreler izlenir.",
                    "E": "Safra travmatik karaciğer hasarında görülür."
                }
            )
        ]
    })

    # Slayt 39: [TEKRAR SAYFASI - CHECKPOINT 4] Gaz Embolisi, Dekompresyon Hastalığı ve Nadir Emboliler
    slides.append({
        "id": "k1-24-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Gaz Embolisi, Dekompresyon Hastalığı ve Nadir Emboliler",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 39,
        "narrative": (
            "Bu dördüncü checkpoint sayfasında, gaz embolisi, dekompresyon hastalığı ve nadir embolileri özetliyoruz: "
            "1. **Hava Embolisi:** Santral venöz kateter veya boyun cerrahisinde negatif venöz basınçla içeri hava emilmesidir. "
            "2. **Hava Kilidi (Air Lock):** >100 ml havanın sağ ventrikülde köpük yaparak pulmoner çıkışı tıkamasıdır; "
            "tedavide hasta SOL YAN TRENDELENBURG (Durant) pozisyonuna alınır. "
            "3. **Dekompresyon Hastalığı (Henry Kanunu):** Derin dalıştan ani yüzeye çıkışta kanda çözünmüş AZOTUN kabarcık oluşturmasıdır. "
            "4. **The Bends:** Eklem ve kaslarda kıvrandırıcı ağrı; **The Chokes:** Pulmoner kapiller tıkanmaya bağlı substernal ağrı ve öksürüktür. "
            "5. **Caisson Hastalığı:** Kronik dekompresyon sonucu femur başı ve tibiada ASEPTİK (AVASKÜLER) KEMİK NEKROZUDUR. "
            "6. **Tedavi:** Rekompresyon (basınç odası) ve %100 hiperbarik oksijendir. "
            "7. **Nadir Emboliler:** Tümör embolisi (metastaz), talk/yabancı cisim embolisi (İV bağımlılarda polarize kristaller)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s39-1",
                "Santral venöz kateter takılması sırasında sağ kalbe aniden giren yüksek hacimli havanın pulmoner çıkış yolunu mekanik olarak kapatması tablosuna ne ad verilir?",
                "Kardiyak hava kilidi (air lock) tablosudur.",
                "Sağ ventrikülde köpüklü gaz birikmesiyle kan akımının durması fenomeni",
                "Hava Kilidi"
            ),
            make_flashcard(
                "k1-24-fc-s39-2",
                "Derin dalıştan su yüzeyine aniden çıkan dalgıçlarda eklem ve kaslarda kıvrandırıcı şiddetli ağrıyla seyreden akut azot kabarcığı tablosuna ne ad verilir?",
                "Bends (kıvrılma) semptomudur.",
                "Basınç düşüşünde nitrojen gazının eklem kavitelerinde kabarcık oluşturması",
                "The Bends"
            ),
            make_flashcard(
                "k1-24-fc-s39-3",
                "Kronik dekompresyon hastalığında (Caisson hastalığı) azot gazı mikroembolilerinin en sık yol açtığı iskemik iskelet patolojisi nedir?",
                "Kemik başlarında aseptik (avasküler) nekrozdur.",
                "Femur ve tibia epifizlerinin beslenememesi sonucu hücresel kalsifiye çöküş",
                "Caisson Hastalığı"
            )
        ],
        "interactiveElements": [
            make_table(
                "Özel Emboli Tipleri ve Tanısal Ayırıcı Özellikleri",
                ["Emboli Türü", "Primer Tetikleyici Olay", "Tanısal İpucu / Patoloji"],
                [
                    ["Venöz Hava Embolisi", "Boyun travması, santral venöz kateter", "Sağ ventrikül hava kilidi, değirmen taşı üfürümü"],
                    ["Akut Dekompresyon", "Derin dalıştan hızlı yüzeye çıkış", "Eklemlerde 'bends', akciğerde 'chokes'"],
                    [
                        "Caisson Hastalığı",
                        "Sürekli su altı tünel çalışması",
                        {"text": "Femur başında aseptik avasküler nekroz", "isMasked": True, "hint": "Kronik azot tıkanmasına bağlı kemik başı ölümü"}
                    ],
                    ["Yabancı Cisim Embolisi", "İV uyuşturucu madde kullanımı", "Polarize mikroskopta çift kıran talk kristalleri"]
                ]
            ),
            make_micro_quiz(
                "Dekompresyon hastalığı (vurgun) ve Caisson hastalığı ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Vurgun tablosunda kabarcık oluşturan primer gaz kanda çözünen azottur",
                    "B": "Caisson hastalığında en sık görülen kronik lezyon femur ve humerus başında aseptik kemik nekrozudur",
                    "C": "'The Chokes' akciğer kapillerlerinin gaz kabarcıklarıyla tıkanması sonucu gelişen dispne ve öksürüktür",
                    "D": "Dekompresyon hastalığının kesin tedavisi hastanın hemen sıcak banyoya sokulmasıdır",
                    "E": "'The Bends' eklem kapsülleri ve tendonlardaki gaz kabarcıklarının yol açtığı şiddetli ağrıdır"
                },
                "D",
                {
                    "A": "Doğrudur; Henry kanunu ile kanda çözünen azot kabarcıklaşır.",
                    "B": "Doğrudur; kronik Caisson hastalığında avasküler nekroz gelişir.",
                    "C": "Doğrudur; chokes pulmoner gaz tutulumudur.",
                    "D": "YANLIŞTIR; Sıcak banyo vazodilatasyon yaparak kabarcık oluşumunu daha da artırabilir! Kesin tedavi REKOMPRESYON (BASINÇ ODASI) tedavisidir.",
                    "E": "Doğrudur; bends iki büklüm eklem ağrısıdır."
                }
            )
        ]
    })

    # Slayt 40: Bölüm Özeti: Emboliden Doku İskemisi ve Enfarktüs Mekanizmalarına Geçiş
    slides.append({
        "id": "k1-24-s40",
        "title": "Bölüm Özeti: Emboliden Doku İskemisi ve Enfarktüs Mekanizmalarına Geçiş",
        "section": "Özel Emboli Tipleri: Gaz Embolisi ve Dekompresyon",
        "slideNumber": 40,
        "narrative": (
            "Dersimizin ilk dört bölümünü oluşturan 'Emboli' ana başlığını tamamlarken klinik hekimlik kazanımlarını özetliyoruz: "
            "1. **Emboli Doku Ölümünün Taşıyıcısıdır:** İster pıhtı, ister yağ, ister amniyon sıvısı, isterse hava kabarcığı olsun; "
            "tüm embolilerin ortak paydası damar lümenini tıkayarak dokunun kanlanmasını durdurmasıdır. "
            "2. **Önleme Tedaviden Kolaydır:** DVT profilaksisi, kateter takılırken dikkat, dalış kurallarına uyum ve kırıkların erken fiksasyonu hayat kurtarır. "
            "3. **Sonraki Bölüme Köprü:** Emboli veya primer tromboz bir arteriyel damarı tıkadığında hedef dokuda ne olur? "
            "Bir sonraki bölümümüzde iskemik hücre ölümünün nihai tablosu olan 'Enfarktüs' konusunu, kırmızı ve beyaz enfarktüs ayrımlarını, "
            "morfolojik dinamikleri ve doku duyarlılıklarını incelemeye başlıyoruz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Arteriyel damar lümeninin tromboz veya emboli ile aniden tıkanması sonucunda hedef dokuda gelişen iskemik koagülatif nekroz alanına enfarktüs denir.",
                "enfarktüs",
                "Kan akımının kesilmesiyle oluşan iskemik doku nekrozu alanı"
            ),
            make_active_recall(
                "Santral venöz kateter takılması sırasında ven içine hava kaçtığı fark edilen bir hastada hava kilidini önlemek için derhal uygulanması gereken mekanik manevra nedir?",
                "Kateterin derhal klemplenmesi ve hastanın sol yan Trendelenburg pozisyonuna alınmasıdır.",
                "Havayı sağ ventrikül apeksinde tutan sol yan baş aşağı pozisyon"
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi bir hastada gelişen embolinin türünün 'Gaz Embolisi' olduğunu düşündüren en spesifik klinik veya otopsi bulgusudur?",
                {
                    "A": "Derin dalıştan hızla çıkan hastada eklem ağrıları (bends) ve akciğerde boğulma hissi (chokes) gelişmesi",
                    "B": "Femur kırığından 2 gün sonra göğüste peteşi çıkması",
                    "C": "Doğum salonunda amniyon sıvısı kaçağı ile masif DİK gelişmesi",
                    "D": "Sol ventrikül MI sonrası bacakta 6P tablosu gelişmesi",
                    "E": "DVT sonrası sağ kalp yetmezliği gelişmesi"
                },
                "A",
                {
                    "A": "Dalış sonrası bends ve chokes tablosu azot gazı kabarcıklarının yol açtığı dekompresyon gaz embolisidir.",
                    "B": "Femur kırığı yağ embolisidir.",
                    "C": "Doğumdaki tablo amniyon sıvısı embolisidir.",
                    "D": "MI sonrası bacak sistemik tromboembolidir.",
                    "E": "DVT sonrası sağ kalp pulmoner tromboembolidir."
                }
            )
        ]
    })

    return slides
