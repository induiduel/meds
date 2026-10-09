# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)
Bölüm 9: Trombüsün Akıbeti ve Klinik Yansımaları (Slayt 81 - 90)
Checkpoint 9: Slayt 89
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # Slayt 81: Trombüsün 4 Olası Akıbeti
    slides.append({
        "id": "k1-20-s81",
        "title": "Trombüsün Akıbeti: Dört Temel Patofizyolojik Sonuç",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 81,
        "narrative": (
            "Damar veya kalp lümeninde bir trombüs meydana geldiğinde, dokunun sağkalımı ve hastanın "
            "klinik seyri trombüsün akıbetine (kaderine) bağlıdır. Robbins ve standart patoloji referanslarına göre "
            "bir trombüsün karşılaşabileceği **4 temel sonuç** tanımlanmıştır: "
            "1. **Propagasyon (Büyüme/İlerleme):** Trombüs daha fazla trombosit ve fibrin toplayarak lümen boyunca uzanır ve kritik damar dallarını tıkar. "
            "2. **Embolizasyon (Koparak Taşınma):** Trombüsün bir kısmı veya tamamı damar duvarından ayrılarak kan akımıyla uzak vasküler yataklara sürüklenir. "
            "3. **Dissolüsyon (Eritilme/Lizis):** Endojen fibrinolitik sistemin hızlı aktivasyonuyla pıhtı tamamen eritilir ve damar lümeni açılır. "
            "4. **Organizasyon ve Rekanalizasyon:** Trombüs içine endotel, fibroblast ve düz kas hücreleri göç ederek bağ dokusu oluşturur ve lümende yeni kılcal damar kanalcıkları açılır. "
            "Bu dört mekanizma arasındaki dinamik yarış, enfarktüs ve ölüm ile tam iyileşme arasındaki sınır çizgisini belirler."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Trombüsün akıbetinde pıhtının endojen fibrinolitik yolakla tamamen temizlenip lümenin açılması olayına dissolüsyon adı verilir.",
                "dissolüsyon",
                "Pıhtının fibrinoliz ile tamamen eritilmesi terimi"
            ),
            make_table(
                ["Trombüs Akıbeti", "Hücresel / Biyokimyasal Mekanizma", "Klinik Yansıması"],
                [
                    ["Propagasyon", "Lümende ardışık trombosit ve fibrin birikimi", "Oklüzyonun ilerlemesi ve yaygın iskemi"],
                    ["Embolizasyon", "Frajil pıhtı parçalarının akımla kopması", "Pulmoner emboli veya iskemik inme"],
                    [
                        "Dissolüsyon",
                        {"text": "t-PA ve plazmin aracılı fibrin yıkımı", "isMasked": True, "hint": "Endojen fibrinolitik sistem enzimleri"},
                        "Damar açıklığının tam restorasyonu"
                    ],
                    ["Organizasyon", "Fibroblast ve endotel göçüyle kapiller kanallar", "Parsiyel lümen akımı veya fibröz kordon"]
                ]
            ),
            make_micro_quiz(
                "Trombüsün akıbetinde tanımlanan 4 temel patolojik süreç hangisinde eksiksiz verilmiştir?",
                {
                    "A": "Adezyon, Agregasyon, Salınım, Hemostaz",
                    "B": "Propagasyon, Embolizasyon, Dissolüsyon, Organizasyon/Rekanalizasyon",
                    "C": "Vazokonstriksiyon, Plak rüptürü, Anevrizma, Aterom",
                    "D": "Kalsifikasyon, Apoptoz, Nekroz, Metaplazi",
                    "E": "Hemostaz, Kemotaksis, Fagositoz, Skar"
                },
                "B",
                {
                    "A": "A seçeneği primer ve sekonder hemostaz basamaklarıdır, trombüsün akıbeti değildir.",
                    "B": "B seçeneği doğrudur: Robbins patolojisine göre trombüsün 4 akıbeti propagasyon, embolizasyon, dissolüsyon ve organizasyon/rekanalizasyondur.",
                    "C": "C seçeneği ateroskleroz ve vasküler yanıtlardır.",
                    "D": "D seçeneği genel hücresel hasar terimleridir.",
                    "E": "E seçeneği yara iyileşmesi ve inflamasyon aşamalarıdır."
                }
            )
        ]
    })

    # Slayt 82: 1. Propagasyon
    slides.append({
        "id": "k1-20-s82",
        "title": "Propagasyon: Trombüsün Lümen Boyunca İlerlemesi",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 82,
        "narrative": (
            "Propagasyon, bir trombüsün başlangıç odak noktasından itibaren lümen içinde kalbe doğru "
            "uzanması, kalınlaşması ve damar ağacının kritik yan dallarını sırayla bloke etmesi sürecidir. "
            "Pıhtının yüzeyindeki trombin aktivitesi devam ettiği sürece çevre kandan dolaşan fibrinojen molekülleri "
            "fibrine çevrilir ve yeni trombositler kitleye dahil olur. "
            "Örneğin baldır derin venlerinde (vena tibialis posterior) başlayan küçük bir venöz trombüs, "
            "staz ve hiperkoagülabilite devam ettiğinde yukarıya doğru proksimale ilerleyerek vena poplitea, "
            "vena femoralis ve hatta vena iliaca communis'e kadar uzanabilir. "
            "Trombüs ne kadar proksimale ilerlerse, hem venöz obstrüksiyon o denli şiddetlenir hem de kopabilecek "
            "pıhtı kitlesinin hacmi büyüyerek masif fatal pulmoner emboli riski katlanarak artar. "
            "Arteriyel sistemde propagasyon ise kollateral akım sağlayan yan dalları kapatarak doku enfarktüsünün sınırlarını dramatik biçimde genişletir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Venöz sistemde baldır venlerinden başlayarak vena femoralis ve iliak venlere kadar ilerleyen pıhtı büyümesine propagasyon denir.",
                "propagasyon",
                "Trombüsün lümen boyunca ardışık birikimle büyümesi ve uzanması"
            ),
            make_causal_chain(
                "Venöz Trombüs Propagasyon Zinciri",
                [
                    "1. Baldır Ven Tutulumu: Vena tibialis posteriorda fokal stazla mikrotrombüs başlar.",
                    "2. Proksimal Büyüme: Trombin aktivasyonuyla pıhtı popliteal vene doğru kalbe antegrat uzanır.",
                    "3. Femoral Yayılım: Vena femoralise ulaşan trombüs lümenin büyük kısmını doldurur.",
                    "4. Kollateral Blokajı: Drenaj yolları kapandıkça alt ekstremitede masif ödem ve venöz staz derinleşir.",
                    "5. Geniş Trombotik Yük: Kopmaya hazır dev bir serbest kuyruk oluşarak pulmoner emboli zeminini hazırlar."
                ]
            ),
            make_micro_quiz(
                "Trombüs propagasyonunun klinik önemi ile ilgili hangisi en doğrudur?",
                {
                    "A": "Propagasyon daima distaldeki en uç kapillerlere doğru ilerler.",
                    "B": "Proksimale uzandıkça kopma riski olan embolus hacmi ve mortalite artar.",
                    "C": "Propagasyon gösteren trombüsler t-PA tedavisine daha duyarlı hale gelir.",
                    "D": "Propagasyon süreci sadece arterlerde görülür, venöz sistemde oluşmaz.",
                    "E": "Propagasyon damar endotelini koruyarak inflamasyonu sınırlar."
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; trombüsler distal uçlara değil kalbe doğru ilerler.",
                    "B": "B seçeneği doğrudur: Proksimale (femoral/iliak) uzayan trombüslerde hem oklüzyon derinleşir hem de kopabilecek embolus kitlesi masif pulmoner emboliye yol açacak kadar büyür.",
                    "C": "C seçeneği yanlıştır; taze pıhtıya göre trombotik yük arttıkça lizis zorlaşır.",
                    "D": "D seçeneği yanlıştır; venöz sistemde derin venlerde propagasyon son derece yaygındır.",
                    "E": "E seçeneği yanlıştır; endoteli korumaz, tam aksine endotel hasarını ve inflamasyonu genişletir."
                }
            )
        ]
    })

    # Slayt 83: 2. Embolizasyon
    slides.append({
        "id": "k1-20-s83",
        "title": "Embolizasyon: Trombüsten Kopan Parçaların Göçü",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 83,
        "narrative": (
            "Embolizasyon, trombüsün damar duvarına yapışık tabanından ayrılarak veya serbest kuyruğunun koparak "
            "kan dolaşımıyla ilk oluştuğu anatomik bölgeden çok uzak vasküler ağlara sürüklenmesidir. "
            "Taşınan bu kitleye **embolus** adı verilir. "
            "Venöz trombüslerin (özellikle alt ekstremite derin ven trombozunun) en önemli ve ölümcül komplikasyonu "
            "**Pulmoner Embolizm (PE)** tablosudur. Alt ekstremite venlerinden kopan pıhtı; inferior vena kava, "
            "sağ atriyum ve sağ ventrikülden geçerek ana pulmoner arteri veya lober dallarını tıkar. "
            "Büyük bir embolus ana pulmoner bifurkasyona oturursa buna **Semer Emboli (Saddle Embolus)** denir ve ani kardiyak arrest/ölümle sonuçlanır. "
            "Buna karşılık kardiyak mural trombüslerden (sol ventrikül, sol atriyum) veya aort anevrizmalarından kopan emboluslar "
            "**sistemik arteriyel embolizm** oluşturur; en sık beyin (inme), böbrek, dalak ve bacak arterlerini tıkayarak enfarktüslere yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Alt ekstremite derin venlerinden kopan bir embolus pulmoner arter bifürkasyonuna oturursa semer emboli olarak adlandırılır.",
                "semer emboli",
                "Ana pulmoner arter çatallanmasını tıkayan ölümcül dev pıhtı"
            ),
            make_before_after(
                "Venöz Embolizm ile Sistemik Arteriyel Embolizm Ayrımı",
                "Venöz Embolizm (DVT Kökenli)",
                [
                    "Kaynak: Alt ekstremite derin venleri (femoral, popliteal)",
                    "Dolaşım güzergahı: İnferior vena kava -> Sağ kalp odacıkları",
                    "Hedef organ: Pulmoner arter yatağı (Pulmoner Emboli)",
                    "Klinik tablo: Ani dispne, plöritik göğüs ağrısı, hipoksi, sağ kalp yetmezliği"
                ],
                "Arteriyel Embolizm (Kardiyak/Aort Kökenli)",
                [
                    "Kaynak: Sol kalp mural trombüsü veya aterosklerotik aort",
                    "Dolaşım güzergahı: Aort -> Sistemik arteriyel dallar",
                    "Hedef organ: Beyin, alt ekstremite arterleri, böbrek, mezenter",
                    "Klinik tablo: İskemik inme, bacakta akut soğukluk/ağrı, böbrek enfarktüsü"
                ]
            ),
            make_active_recall(
                "Atriyal fibrilasyonu olan bir hastada sol atriyal apendiksteki trombüsten kopan embolus hangi organlara gidip enfarktüs oluşturur?",
                "Sistemik dolaşıma geçer; en sık beyin (inme), alt ekstremiteler (gangren), böbrek ve mezenter arterlerine gider.",
                "Sol kalp embolusunun hedef vasküler yatakları"
            )
        ]
    })

    # Slayt 84: 3. Dissolüsyon (Eritilme)
    slides.append({
        "id": "k1-20-s84",
        "title": "Dissolüsyon: Fibrinolitik Yolak ve Pıhtı Yaşlanması",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 84,
        "narrative": (
            "Dissolüsyon, yeni oluşmuş bir trombüsün organizmanın endojen fibrinolitik savunma mekanizmalarıyla "
            "tamamen eritilerek damar lümeninin yeniden açılmasıdır. "
            "Trombüs oluştuktan hemen sonra endotelden salınan doku plazminojen aktivatörü (t-PA), "
            "fibrine bağlı plazminojeni aktif plazmine dönüştürür. Plazmin fibrin ağlarını keserek çözünür D-Dimer ve FDP fragmanlarına yıkar. "
            "Ancak dissolüsyon sürecinde **zaman faktörü** hayati bir kuraldır: "
            "Trombüs yaşlandıkça aktive Faktör XIIIa (FXIIIa) aracılığıyla fibrin lifleri arasında yoğun kovalent çapraz bağlar kurulur "
            "ve trombositler büzülerek pıhtıyı kompakt ve sert hale getirir. "
            "Bu nedenle saatler veya günler geçmiş eski (organize olmaya başlamış) trombüsler endojen plazmine ve dışarıdan verilen "
            "trombolitik ilaçlara (t-PA, alteplaz) karşı belirgin direnç kazanır. "
            "Akut miyokard enfarktüsü veya iskemik inmede trombolitik tedavinin ilk birkaç saat içinde ('altın saatler') uygulanmasının temel patolojik gerekçesi budur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Trombüsün yaşlanmasıyla fibrin lifleri arasında kovalent bağ kurarak pıhtıyı lizise dirençli kılan enzim Faktör XIIIa enzimidir.",
                "Faktör XIIIa",
                "Fibrini çapraz bağlayan transglutaminaz koagülasyon faktörü"
            ),
            make_causal_chain(
                "Pıhtı Yaşlanması ve Lizis Direnci Mekanizması",
                [
                    "1. Taze Trombüs: Gevşek fibrin ağları t-PA ve plazmin ile kolayca degrade edilir.",
                    "2. FXIIIa Aktivasyonu: Fibrin monomerleri arasında kovalent glutamil-lisil çapraz bağları örülür.",
                    "3. Pıhtı Retraksiyonu: Trombosit aktin-miyozin kasılmasıyla pıhtı suyunu kaybeder ve sıkılaşır.",
                    "4. Fibroblast İnfiltrasyonu: Endotel ve bağ dokusu elemanları pıhtı iskeletine invaze olur.",
                    "5. Trombolitik Direnç: Eski pıhtı t-PA ile eritilemez hale gelir ve organizasyon sürecine girer."
                ]
            ),
            make_micro_quiz(
                "Eski (yaşlanmış) bir trombüsün taze bir trombüse kıyasla t-PA ve trombolitik ilaçlara dirençli olmasının temel nedeni hangisidir?",
                {
                    "A": "Eski pıhtıda trombosit sayısının 10 katına çıkması",
                    "B": "Faktör XIIIa ile fibrin çapraz bağlanması ve fibröz organizasyonun başlamış olması",
                    "C": "Eritrositlerin tamamen parçalanarak hemoglobin salması",
                    "D": "Damar endotelinin aşırı miktarda t-PA sentezlemeye başlaması",
                    "E": "Pıhtı lümeninde laminer akımın kendiliğinden restore olması"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; trombosit sayısı pıhtı yaşlandıkça artmaz.",
                    "B": "B seçeneği doğrudur: Faktör XIIIa kovalent çapraz bağları ve bağ dokusu organizasyonu eski pıhtıyı enzimatik sindirime karşı son derece dirençli kılar.",
                    "C": "C seçeneği lizis direncini açıklayan mekanizma değildir.",
                    "D": "D seçeneği t-PA sentezi artarsa pıhtı erir, direnç gelişmez.",
                    "E": "E seçeneği direncin sebebi değil, pıhtı kalkarsa oluşabilecek bir sonuçtur."
                }
            )
        ]
    })

    # Slayt 85: 4. Organizasyon ve Rekanalizasyon
    slides.append({
        "id": "k1-20-s85",
        "title": "Organizasyon ve Rekanalizasyon: Damar İçi Restorasyon",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 85,
        "narrative": (
            "Dissolüsyona uğramayan ve embolize olmayan eski trombüsler, damar duvarından gelen inflamatuar ve onarıcı "
            "yanıt sonucunda **organizasyon ve rekanalizasyon** sürecine girer. "
            "Organizasyon, trombüsün tabanından itibaren endotel hücreleri, düz kas hücreleri ve fibroblastların "
            "pıhtı kitlesi içine göç etmesi (granülasyon dokusu benzeri infiltrasyon) ve kollajen birikimiyle pıhtının fibröz bir kütleye dönüşmesidir. "
            "Zamanla bu fibröz kütle damar duvarının bir parçası (subendotelyal intimal kalınlaşma) haline gelir. "
            "Rekanalizasyon ise, trombüsün içine urgan gibi uzanan kapiller endotel hücrelerinin tübüler boşluklar oluşturması ve "
            "bu boşlukların birleşerek pıhtının bir ucundan diğer ucuna uzanan yeni mikrovasküler kanallar açmasıdır. "
            "Bu yeni kanallar sayesinde damar lümeninde kısmi de olsa kan akımı yeniden başlar. "
            "Bazen organize trombüsler distrofik kalsifikasyona uğrayarak radyoopak taş benzeri sert yapılar (**flebolit**) oluşturabilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Organize trombüs kütlesi içinde endotel hücrelerinin yeni tübüler kanallar açarak parsiyel kan akımını sağlamasına rekanalizasyon denir.",
                "rekanalizasyon",
                "Pıhtı içinden yeni lümen kanalcıklarının açılması süreci"
            ),
            make_table(
                ["Süreç Basamağı", "Hücresel Aktörler", "Morfolojik Görünüm"],
                [
                    ["Erken Organizasyon (1-3 gün)", "Monosit / Makrofajlar ve Endotel", "Pıhtı tabanında kapiller tomurcuklanma"],
                    [
                        "İleri Organizasyon (1-2 hafta)",
                        {"text": "Fibroblastlar ve Düz Kas Hücreleri", "isMasked": True, "hint": "Kollajen ve matriks sentezleyen onarım hücreleri"},
                        "Trombüsün fibröz bağ dokusuna dönüşmesi"
                    ],
                    ["Rekanalizasyon", "Anastomoz yapan yeni Endotel tüpleri", "Trombüs içinden geçen kan dolu mikrokanallar"],
                    ["Geç Evre / Kalsifikasyon", "Kalsiyum hidroksiapatit birikimi", "Damar içinde kalsifiye flebolit nodülleri"]
                ]
            ),
            make_active_recall(
                "Kronik oklüziv venöz trombüs zemininde distrofik kalsifikasyon ile taşlaşmış intralüminal nodüllere ne ad verilir?",
                "Flebolit (ven taşı) adı verilir.",
                "Ven lümeninde kalsifiye organize trombüs kalıntısı"
            )
        ]
    })

    # Slayt 86: Derin Ven Trombozu (DVT)
    slides.append({
        "id": "k1-20-s86",
        "title": "Derin Ven Trombozu (DVT): Patogenez ve Klinik Belirtiler",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 86,
        "narrative": (
            "Derin Ven Trombozu (DVT), alt ekstremitenin derin venöz sisteminde (özellikle vena poplitea, "
            "femoral ven ve iliak venlerde) ortaya çıkan ve klinikte en sık karşılaşılan tromboz tablosudur. "
            "Olguların yaklaşık %50'si başlangıçta tamamen asemptomatiktir; çünkü alt ekstremitenin yüzeyel ve kollateral "
            "venöz yolları tıkanan derin venin drenajını geçici olarak kompanse edebilir. "
            "Semptomatik olgularda ise klasik belirtiler; tek taraflı bacakta şişlik (ödem), eritem, lokal ısı artışı, "
            "baldırda dolgunluk ve derin palpasyonla ağrıdır. "
            "Ayak bileğinin ani pasif dorsifleksiyonu ile baldırda şiddetli ağrı uyarılmasına **Homans belirtisi** denir; "
            "ancak bu belirti hem duyarlılığı hem de özgüllüğü düşük bir fizik muayene bulgusudur. "
            "DVT'nin en kritik klinik tehlikesi, semptomların hafifliğine rağmen pıhtının proksimale (femoral/iliak) uzanarak "
            "ansızın kopması ve fatal pulmoner emboli meydana getirmesidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Ayak bileğinin pasif dorsifleksiyonu ile baldırda ağrı tetiklenmesi klasik fizik muayenede Homans belirtisi olarak tanımlanır.",
                "Homans belirtisi",
                "DVT tanısında sorgulanan geleneksel baldır ağrısı işareti"
            ),
            make_before_after(
                "Baldır DVT ile Proksimal (Femoral/İliak) DVT Karşılaştırması",
                "Baldır DVT (Distal Yerleşim)",
                [
                    "Yerleşim: Vena tibialis posterior ve vena peronea",
                    "Klinik seyir: Çoğunlukla asemptomatik veya hafif lokal ağrı",
                    "Pulmoner emboli riski: Düşük (%10-15); kendiliğinden lizis sıktır",
                    "Tedavi yaklaşımı: Yakın takip veya kısa süreli antikoagülasyon"
                ],
                "Proksimal DVT (Popliteal / Femoral / İliak)",
                [
                    "Yerleşim: Vena poplitea, vena femoralis ve vena iliaca",
                    "Klinik seyir: Masif tek taraflı bacak ödemi ve belirgin ağrı",
                    "Pulmoner emboli riski: Çok yüksek (%50'ye varan oranlar)",
                    "Tedavi yaklaşımı: Acil ve tam doz sistemik antikoagülasyon"
                ]
            ),
            make_micro_quiz(
                "Alt ekstremite derin ven trombozu (DVT) kliniği ve patolojisi ile ilgili hangisi yanlıştır?",
                {
                    "A": "Olguların yaklaşık yarısı başlangıçta tamamen sessiz (asemptomatik) seyredebilir.",
                    "B": "Proksimal femoral ve iliak ven trombüslerinde pulmoner emboli riski çok yüksektir.",
                    "C": "Tek taraflı bacak ödemi, ısı artışı ve baldır hassasiyeti tipik klinik bulgulardır.",
                    "D": "Homans belirtisi DVT için %100 özgül ve altın standart tanı yöntemidir.",
                    "E": "Trombüsün en yaygın başlangıç yeri venöz kapak cepleridir."
                },
                "D",
                {
                    "A": "A seçeneği doğrudur; kollateraller nedeniyle %50 vaka sessizdir.",
                    "B": "B seçeneği doğrudur; proksimal trombüsler yüksek oranda pulmoner emboli yapar.",
                    "C": "C seçeneği doğrudur; venöz oklüzyonun tipik lokal staz bulgularıdır.",
                    "D": "D seçeneği yanlıştır: Homans belirtisi özgüllüğü ve duyarlılığı oldukça düşük bir bulgudur; kesin tanı Kompresyon Doppler Ultrasonografi ile konur.",
                    "E": "E seçeneği doğrudur; kapak ceplerindeki staz ve düşük oksijenasyon endoteli aktive eder."
                }
            )
        ]
    })

    # Slayt 87: Arteriyel Tromboz Sonuçları
    slides.append({
        "id": "k1-20-s87",
        "title": "Arteriyel Trombozun Klinik Tabloları: İskemi ve Enfarktüs",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 87,
        "narrative": (
            "Arteriyel sistem yüksek basınçlı ve terminal organlara oksijen taşıyan bir otoyol olduğundan, "
            "arteriyel bir trombüsün gelişimi hemen daima beslenen parankimde akut oksijensizlik (iskemi) "
            "ve geri dönüşümsüz hücre ölümü (koagülasyon veya likefaksiyon nekrozu/enfarktüs) ile sonuçlanır. "
            "En sık görülen klinik felaketler şunlardır: "
            "1. **Miyokard Enfarktüsü (MI):** Koroner arter aterom plağının yırtılması üzerine oturan trombüs, miyokard dokusunu dakikalar içinde nekroza götürür. "
            "2. **İskemik İnme (Serebrovasküler Olay):** Karotis bifurkasyonu veya orta serebral arterdeki trombotik tıkanma, beyinde likefaksiyon (sıvılaşma) nekrozu oluşturur. "
            "3. **Akut Mezenterik İskemi:** Süperior mezenterik arter trombozu, ince bağırsaklarda masif hemorajik gangrene ve septik şoka neden olur. "
            "4. **Akut Ekstremite İskemisi:** Femoral/popliteal arter oklüzyonu; 6P tablosu (Pain/Ağrı, Pallor/Solukluk, Pulselessness/Nabızsızlık, "
            "Paresthesia/Uyuşma, Paralysis/Felç, Poikilothermia/Soğukluk) ile seyreder ve acil revaskülarizasyon yapılmazsa ekstremite gangrenine yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Arteriyel tromboza bağlı akut ekstremite iskemisinde solukluk, nabızsızlık ve ağrının eşlik ettiği klasik sendrom 6P tablosu olarak adlandırılır.",
                "6P tablosu",
                "Akut periferik arter tıkanıklığının 6 İngilizce P harfiyle anılan belirtileri"
            ),
            make_table(
                ["Etkilenen Arter Yatağı", "Oluşan Patolojik Lezyon", "Temel Nekroz Tipi"],
                [
                    ["Koroner Arterler", "Akut Miyokard Enfarktüsü (Kalp krizi)", "Koagülasyon nekrozu"],
                    [
                        "Serebral Arterler",
                        {"text": "İskemik İnme / Serebral Enfarktüs", "isMasked": True, "hint": "Beyin parankiminde sıvılaşma ile seyreden felç"},
                        "Likefaksiyon (Sıvılaşma) nekrozu"
                    ],
                    ["Süperior Mezenterik Arter", "Mezenterik Enfarktüs / Bağırsak Gangreni", "Hemorajik gangrenöz nekroz"],
                    ["Femoral / Popliteal Arter", "Akut Bacak İskemisi ve Kuru Gangren", "Koagülasyon nekrozu"]
                ]
            ),
            make_micro_quiz(
                "Serebral arteriyel tromboz sonucunda gelişen beyin dokusu enfarktüsünde izlenen karakteristik patolojik nekroz tipi hangisidir?",
                {
                    "A": "Koagülasyon nekrozu",
                    "B": "Likefaksiyon (sıvılaşma) nekrozu",
                    "C": "Kazeifikasyon nekrozu",
                    "D": "Fibrinoid nekroz",
                    "E": "Enzimik yağ nekrozu"
                },
                "B",
                {
                    "A": "A seçeneği kalp ve böbrek gibi organ enfarktüslerinde görülür.",
                    "B": "B seçeneği doğrudur: Santral sinir sisteminde hidrolitik enzimlerin yoğunluğu ve miyelin içeriği nedeniyle iskemik hasar likefaksiyon (sıvılaşma) nekrozu ile sonuçlanır.",
                    "C": "C seçeneği tüberküloz enfeksiyonuna özgüdür.",
                    "D": "D seçeneği malign hipertansiyon ve vaskülitlerde damar duvarında izlenir.",
                    "E": "E seçeneği akut pankreatit tablosuna özgüdür."
                }
            )
        ]
    })

    # Slayt 88: Kronik Venöz Yetmezlik ve Post-Trombotik Sendrom
    slides.append({
        "id": "k1-20-s88",
        "title": "Kronik Venöz Yetmezlik ve Post-Trombotik Sendrom (PTS)",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 88,
        "narrative": (
            "DVT geçiren hastaların yaklaşık %30-50'sinde, akut tromboz tablosu düzelse bile aylar veya yıllar sonra "
            "**Post-Trombotik Sendrom (PTS)** adı verilen kronik bir sekonder hastalık tablosu gelişir. "
            "Bu durumun altta yatan temel patofizyolojik nedeni, derin ven lümenindeki organize olan trombüsün "
            "venöz kapak yaprakçıklarını tahrip etmesi ve fibrotik skar ile kapakların kapanamaz (inkompetan) hale gelmesidir. "
            "Kapak fonksiyonunu kaybeden venlerde yerçekimi etkisiyle hidrostatik basınç dramatik şekilde yükselir (venöz hipertansiyon). "
            "Yüksek venöz basınç kapiller yatağa iletilerek eritrositlerin interstisyuma sızmasına (diyapedez) yol açar. "
            "Dokuya sızan eritrositlerin parçalanmasıyla açığa çıkan hemosiderin pigmenti deride kalıcı kahverengi pigmentasyona "
            "(staz dermatiti) neden olur. "
            "Doku oksijenasyonunun bozulması ve kronik inflamasyon, mediyal malleol üzerinde iyileşmesi son derece güç olan "
            "kronik venöz staz ülserlerinin açılmasıyla sonlanır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "DVT sonrası kapak tahribatı ve kronik venöz hipertansiyon sonucu gelişen tabloya post-trombotik sendrom denir.",
                "post-trombotik sendrom",
                "Geçirilmiş DVT zemininde oluşan kronik sekellerin klinik sendrom adı"
            ),
            make_causal_chain(
                "Post-Trombotik Sendrom ve Ülser Patogenezi",
                [
                    "1. Kapak Hasarı: Derin vende organize olan trombüs valvülleri skatrisize eder.",
                    "2. Venöz Hipertansiyon: Valvüler inkompetans yerçekimiyle venöz staz basıncını artırır.",
                    "3. Hemosiderin Sızıntısı: Yüksek basınçla dokuya kaçan eritrositler parçalanarak hemosiderin bırakır.",
                    "4. Staz Dermatiti: Deri sertleşir (lipodermatoskleroz) ve kahverengi pigmentasyon oluşur.",
                    "5. Venöz Staz Ülseri: Mikrodolaşım iskemisi mediyal malleol çevresinde kronik açık yaralara yol açar."
                ]
            ),
            make_active_recall(
                "Post-trombotik sendromda deride görülen karakteristik kahverengi pigmentasyon hangi pigmentin dokuda birikmesinden kaynaklanır?",
                "Ekstravaze olan eritrositlerin yıkımıyla oluşan hemosiderin pigmentidir.",
                "Staz dermatitinde kahverengi rengi veren demir içerikli pigment"
            )
        ]
    })

    # Slayt 89: [TEKRAR SAYFASI - CHECKPOINT 9]
    slides.append({
        "id": "k1-20-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Trombüsün Akıbeti ve Klinik Yansımaları",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 89,
        "narrative": (
            "Bu checkpoint sayfasında trombüsün 4 temel akıbetini (propagasyon, embolizasyon, dissolüsyon, "
            "organizasyon/rekanalizasyon), pıhtı yaşlanmasında lizis direncinin biyokimyasal temelini ve "
            "derin ven trombozunun uzun dönemli komplikasyonu olan post-trombotik sendromu "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-20-cp9-1",
                "Trombüsün 4 temel akıbeti (kaderi) nelerdir?",
                "1. Propagasyon (lümen boyunca büyüme), 2. Embolizasyon (koparak uzak yatağa taşınma), 3. Dissolüsyon (fibrinoliz ile tam eritilme), 4. Organizasyon ve rekanalizasyon (bağ dokusu oluşumu ve yeni lümen kanalcıkları).",
                "Robbins'te tanımlanan 4 patofizyolojik akıbet",
                "Trombüsün Akıbeti"
            ),
            make_flashcard(
                "fc-k1-20-cp9-2",
                "Eski (organize) bir trombüsün taze bir trombüse göre t-PA ve trombolitiklere dirençli olmasının temel nedeni nedir?",
                "Faktör XIIIa aracılığıyla kurulan yoğun kovalent fibrin çapraz bağları, trombosit retraksiyonu ve fibroblastik/kollajen infiltrasyonudur.",
                "Kovalent çapraz bağlar ve organizasyon yapısı",
                "Fibrinolitik Direnç"
            ),
            make_flashcard(
                "fc-k1-20-cp9-3",
                "Geçirilmiş DVT zemininde gelişen post-trombotik sendromun temel patofizyolojik tetikleyicisi nedir?",
                "Trombüs organizasyonu sırasında venöz kapakçıkların tahrip olması sonucu gelişen kronik valvüler inkompetans ve derin venöz hipertansiyondur.",
                "Valvüler hasar ve venöz basınç artışı",
                "Venöz Patoloji"
            )
        ]
    })

    # Slayt 90: Bölüm Özeti ve Tedaviye Geçiş
    slides.append({
        "id": "k1-20-s90",
        "title": "Trombüsün Akıbeti Özeti: Patolojiden Farmakoterapiye Köprü",
        "section": "Trombüsün Akıbeti ve Klinik Yansımaları",
        "slideNumber": 90,
        "narrative": (
            "Özetle; bir trombüs oluştuktan sonra damar içinde durağan kalmaz. Eğer fibrinolitik sistem erken evrede "
            "etkin çalışırsa pıhtı dissolüsyon ile iz bırakmadan temizlenir. "
            "Ancak Faktör XIIIa kovalent bağları oluştuktan sonra pıhtı yaşlanır, sertleşir ve organizasyon sürecine girer; "
            "endotelial tomurcuklanma ile rekanalize olsa dahi kapaklar tahrip olarak post-trombotik sendroma zemin hazırlar. "
            "Pıhtı kalbe doğru ilerlerse (propagasyon) oklüzyon genişler; parçalanıp koparsa (embolizasyon) venöz sistemden "
            "akciğere (PE), arteriyel/kardiyak sistemden beyne (inme) ve ekstremitelere felaket taşır. "
            "Bu yıkıcı klinik sonuçların önüne geçebilmek için modern tıpta patofizyolojik mekanizmalara doğrudan hedeflenmiş "
            "antiplatelet, antikoagülan ve trombolitik farmakolojik tedaviler geliştirilmiştir. "
            "Son bölümümüzde bu tedavi stratejilerini, profilaksi ilkelerini ve tanı algoritmalarını inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Trombüsün damar duvarından koparak kan akımıyla taşınması sonucunda gelişen klinik felaket tablosuna tromboembolizm adı verilir.",
                "tromboembolizm",
                "Tromboz ve embolizasyonun ortak patolojik klinik terimi"
            ),
            make_table(
                ["Patolojik Süreç", "Zaman Penceresi", "Tıbbi Müdahale Amacı"],
                [
                    ["Akut Dissolüsyon", "İlk saatler (altın pencere)", "Trombolitik ajanlarla (t-PA) damar açıklığını kurtarma"],
                    [
                        "Propagasyonun Durdurulması",
                        {"text": "Akut ve subakut evre", "isMasked": True, "hint": "Pıhtılaşma kaskadını bloke eden antikoagülan ilaçlar"},
                        "Heparin ve oral antikoagülanlarla yeni fibrin yapımını engelleme"
                    ],
                    ["Kronik Rekanalizasyon", "Haftalar ve aylar", "Kompresyon çorapları ile post-trombotik sendromu önleme"]
                ]
            ),
            make_micro_quiz(
                "Trombüsün akıbeti ve klinik yansımalarıyla ilgili hangisi doğru bir patofizyolojik yorumdur?",
                {
                    "A": "Faktör XIIIa çapraz bağları trombüsün plazmin ile eritilmesini belirgin şekilde hızlandırır.",
                    "B": "Venöz trombüslerden kopan emboluslar serebral arterlere ulaşarak ilk olarak inmeye neden olur.",
                    "C": "Rekanalizasyon sürecinde organize trombüs içinde yeni tübüler endotelial kanallar oluşur.",
                    "D": "DVT olgularının tümü ilk günden itibaren şiddetli bacak ağrısı ve dev ödemle belirti verir.",
                    "E": "Propagasyon süreci trombüsün hacmini küçülterek emboli riskini ortadan kaldırır."
                },
                "C",
                {
                    "A": "A seçeneği yanlıştır; FXIIIa çapraz bağları pıhtıyı lizise dirençli kılar.",
                    "B": "B seçeneği yanlıştır; venöz emboluslar intrakardiyak şant yoksa önce akciğere gider.",
                    "C": "C seçeneği doğrudur: Rekanalizasyon sırasında organize bağ dokusu içinde kapiller kanallar açılarak kısmi kan akımı restore edilir.",
                    "D": "D seçeneği yanlıştır; vakaların yaklaşık %50'si kollateraller sayesinde asemptomatiktir.",
                    "E": "E seçeneği yanlıştır; propagasyon pıhtı hacmini büyütür ve riski artırır."
                }
            )
        ]
    })

    return slides
