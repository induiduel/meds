# -*- coding: utf-8 -*-
"""Part 1: Slides 1 to 12 for Kronik ve Granülomatöz Enflamasyon Deck."""

slides_part1 = [
    # SLIDE 1
    {
        "slideNumber": 1,
        "title": "Kronik Enflamasyonun Tanımı ve Patolojik Triadı",
        "subtitle": "Aktif Enflamasyon, Doku Yıkımı ve Onarım Süreçlerinin Eşzamanlı Birlikteliği",
        "content": (
            "Değerli meslektaşlarım, patoloji kürsüsünün en temel ve klinik açıdan en belirleyici konularından biri olan "
            "kronik enflamasyona adım atıyoruz. Akut enflamasyon dakikalar ya da günler içinde başlayıp nötrofil hakimiyeti "
            "ve eksüdayla seyrederken, kronik enflamasyon haftalar, aylar ve hatta yıllar boyu devam edebilen uzamış bir süreçtir. "
            "Ancak kronik enflamasyonu sadece takvimdeki süresiyle tanımlamak patolojik açıdan son derece yetersizdir. "
            "Kronik enflamasyonun asıl alametifarikası; aktif doku hasarı, devam eden hücresel enflamatuvar yanıt ve eşzamanlı "
            "olarak yürütülen doku onarım girişimlerinin (anjiyogenez ve fibrozis) aynı doku yatağında bir arada bulunmasıdır.\n\n"
            "Akut enflamasyonun bildiğimiz klasik sonlanımları vardır: Etken tamamen temizlenir ve doku rezolüsyon ile eski mimarisine "
            "kavuşur; ya da doku çatısı çöktüğünde organizasyon ile basit bir skar dokusu kalır. Kronik enflamasyonda ise uyarının "
            "inatçı olması nedeniyle çözünme (rezolüsyon) asla gerçekleşemez. Örneğin bir peptik ülser kraterine mikroskop altında "
            "baktığınızda, en yüzeyde nekrotik hücresel döküntüler ve aktif lökosit infiltrasyonu görürken, hemen altında granülasyon "
            "dokusu ve daha derinde yoğun kollajen birikiminden ibaret fibröz bir skar dokusuyla karşılaşırsınız. İşte bu manzara, "
            "hasar ve tamirin eşzamanlı sürdüğünün en somut kanıtıdır.\n\n"
            "Süreç iki temel patogenetik yolla başlayabilir: İlki, çözülememiş ve etkenin eradike edilemediği bir akut enflamasyonun "
            "tedricen kronikleşmesidir. İkincisi ve klinikte çok daha sık gördüğümüz form ise, önceden hiçbir akut enflamatuvar fırtına "
            "olmadan, sinsi ve asemptomatik olarak başlayan primer kronik tablodur. Romatoid artrit, ateroskleroz ve tüberküloz gibi "
            "hastalıklar genellikle bu sessiz başlangıçla doku parankimini adım adım tahrip ederler."
        ),
        "synthesisNarrative": (
            "Kronik enflamasyon, haftalarca veya aylarca süren ve aktif enflamasyon, parankimal doku yıkımı ile onarım "
            "girişimlerinin (anjiyogenez ve fibrozis) aynı odakta eşzamanlı seyrettiği patolojik bir süreçtir."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Kronik enflamasyon yalnızca süresiyle değil, histopatolojik triadı ile tanımlanır: Mononükleer hücre infiltrasyonu, kalıcı doku hasarı ve eşzamanlı süren onarım girişimleri (anjiyogenez ve fibrozis).",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Akut enflamasyondan farklı olarak kronik enflamasyon sahasında doku yıkımı ile birlikte eşzamanlı olarak anjiyogenez (yeni damar oluşumu) ve fibrozis (kollajen sentezi) görülmesi patognomonik bir özelliktir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Akut enflamasyondan farklı olarak nötrofil ve ödem yerine mononükleer hücreler hakimdir.",
            "Doku yıkımı ile birlikte aynı odakta granülasyon dokusu ve fibrozis eşzamanlı ilerler.",
            "Primer kronik formlar belirgin bir akut faz olmadan sinsi bir başlangıç sergiler."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-001",
            "question": "Kronik enflamasyonun histopatolojik özellikleri ile ilgili aşağıdaki ifadelerden hangisi temel tanısal triadı en doğru şekilde özetler?",
            "options": [
                "A) Yoğun nötrofilik infiltrasyon, masif seröz ödem ve tam epitel rejenerasyonu",
                "B) Mononükleer hücre infiltrasyonu, aktif doku hasarı ve eşzamanlı anjiyogenez/fibrozis",
                "C) Yalnızca fibröz skar dokusu gelişimi ve enflamatuvar hücrelerin tamamen kaybolması",
                "D) Vasküler permeabilite artışına bağlı fibrinöz eksüda ve vasküler tromboz",
                "E) Eozinofil lökosit hakimiyeti, mast hücre degranülasyonu ve mukoid dejenerasyon"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Kronik enflamasyonun histopatolojik triadı: Mononükleer lökosit (makrofaj, lenfosit, plazma hücresi) infiltrasyonu, inatçı etkene bağlı doku yıkımı ve eşzamanlı doku onarımı girişimleridir (anjiyogenez ve fibroblastik aktivite/fibrozis). Nötrofil ve yaygın seröz ödem akut enflamasyona özgüdür."
        }
    },

    # SLIDE 2
    {
        "slideNumber": 2,
        "title": "Akut ve Kronik Enflamasyonun Karşılaştırmalı Patolojisi",
        "subtitle": "Vasküler Yanıttan Mononükleer İstilaya: Hücresel ve Dinamik Farklılıklar",
        "content": (
            "Amfide sıkça sorduğumuz klasik bir patoloji sorusuyla devam edelim: Bir doku kesitine baktığımızda gördüğümüz "
            "tablonun akut mu yoksa kronik mi olduğunu nasıl ayırt ederiz? Bu ayrım sadece morfolojik bir egzersiz değil, hastanın "
            "tedavisini ve prognozunu belirleyen temel klinik ayrımdır. Akut enflamasyon dakikalar içinde tetiklenen vazodilatasyon, "
            "kapiller geçirgenlik artışı ve protein zengini eksüdanın interstisyuma geçişiyle (ödem) karakterizedir. Buradaki hücresel "
            "öncü kuvvet, dolaşımdan ilk 6-24 saatte hızla göç eden ve yarı ömrü 1-2 günle sınırlı olan polimorfonükleer lökosittir (nötrofil).\n\n"
            "Buna karşılık kronik enflamasyonda hemodinamik vasküler geçirgenlik krizi geride kalmıştır. Dokuda sıvı ödeminden ziyade "
            "yoğun mononükleer hücre göçü ve proliferasyonu izlenir. Bu infiltratın ana aktörleri makrofajlar, T ve B lenfositleri ile "
            "plazma hücreleridir. Akut enflamasyonun temel amacı patojeni dakikalar içinde fagositoz ve nötrofilik enzimlerle yok edip "
            "sahayı temizlemek iken; kronik enflamasyon, konak bağışıklığının kolayca alt edemediği uyarana karşı kurduğu organize bir "
            "direniş ve sınırlandırma cephesidir.\n\n"
            "En dramatik fark ise doku parankiminin akıbetinde gizlidir. Akut enflamasyonda parankimal hücrelerin bazal membranı sağlam "
            "kaldığı sürece organ eski haline dönebilir (tam rezolüsyon). Kronik enflamasyonda ise sitokinler ve proteolitik enzimler "
            "dokunun ana çatısını yıkar. Parankim hücreleri kaybolur; yerini körü körüne çoğalan yeni kapiller damarlar (anjiyogenez) "
            "ve fibroblastların sentezlediği ekstraselüler matriks doldurur. Sonuç organ disfonksiyonu ve kalıcı fibrotik deformasyondur."
        ),
        "synthesisNarrative": (
            "Akut enflamasyon vazodilatasyon, ödem ve nötrofil hakimiyetiyle başlayıp tam iyileşmeyle sonlanabilirken; "
            "kronik enflamasyon mononükleer infiltrat, kalıcı parankimal doku yıkımı ve organ fibrozisiyle karakterizedir."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Akut enflamasyonda primer lökosit yanıtı nötrofiller iken, kronik enflamasyonda mononükleer fagositik sistem elemanları (makrofajlar, lenfositler ve plazma hücreleri) baskındır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Kronik enflamasyon zemininde parankim kaybının yerini fibröz bağ dokusunun alması (fibrozis) geri dönüşsüz fonksiyon kaybına ve organ sertleşmesine yol açar.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Akut süreç dakikalar-günler sürerken, kronik süreç haftalar, aylar veya yıllar boyu devam eder.",
            "Akut tablonun vasküler yanıtı sıvı eksüdasyonu iken, kronik tablonun yanıtı anjiyogenezdir.",
            "Kronik enflamasyonda rezolüsyon yerine destrüksiyon ve bağ dokusu organizasyonu gerçekleşir."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-002",
            "question": "Aşağıdakilerden hangisi kronik enflamasyonu akut enflamasyondan ayıran temel histopatolojik özelliklerden biridir?",
            "options": [
                "A) Erken dönemde vasküler permeabilite artışına bağlı zengin seröz eksüda birikimi",
                "B) Lezyon odağında predominant hücre olarak nötrofil lökositlerin bulunması",
                "C) Doku parankim hasarı ile birlikte eşzamanlı anjiyogenez ve kollajen birikiminin izlenmesi",
                "D) Doku bazal membranlarının tamamen korunarak lezyonun iz bırakmadan iyileşmesi",
                "E) Yalnızca vazoaktif aminlerin (histamin, serotonin) lokal salınımıyla sınırlı olması"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Kronik enflamasyonda akut süreçten farklı olarak doku yıkımı ile birlikte anjiyogenez ve kollajen birikimi (fibrozis) eşzamanlı olarak gerçekleşir. Nötrofil hakimiyeti, erken sıvı eksüdasyonu ve tam rezolüsyon akut enflamasyonun tipik bulgularıdır."
        }
    },

    # SLIDE 3
    {
        "slideNumber": 3,
        "title": "Kronik Enflamasyonun Etiyolojik Sınıflandırması",
        "subtitle": "Kalıcı Enfeksiyonlar, İmmün Aracılı Bozukluklar ve Toksik Maddelere Maruziyet",
        "content": (
            "Kronik enflamasyonu başlatan ve canlı dokuda aylarca devam ettiren etkenleri üç ana patogenetik grupta inceliyoruz. "
            "Bu ayrım klinisyenin etiyolojik tanıya ulaşmasında pusula görevi görür. Birinci grup, vücudun fagositoz mekanizmalarına "
            "direnen inatçı mikroorganizma enfeksiyonlarıdır. Bunların prototipi Mycobacterium tuberculosis, Treponema pallidum "
            "(sifilis etkeni) ve belirli mantar/parazit türleridir. Bu patojenler hücre duvarlarındaki özel lipidler veya konak savunmasını "
            "aldatan proteinler sayesinde fagozom-lizozom füzyonunu engeller ve kronik gecikmiş tip aşırı duyarlılık yanıtını kışkırtır.\n\n"
            "İkinci büyük grup, immün aracılı enflamatuvar hastalıklardır. Burada immün sistem hedef şaşırmıştır veya regülasyonunu "
            "kaybetmiştir. Otoimmün hastalıklarda (Romatoid Artrit, Sistemik Lupus Eritematozus, İnflamatuar Barsak Hastalıkları) "
            "vücut kendi dokularındaki otoantijenleri yabancı algılar ve sürekli bir antijenik uyarı döngüsü oluşur. Otoantijenler "
            "ortamdan temizlenemeyeceği için enflamasyon kendiliğinden sönmez, kronik doku destrüksiyonu ve sakatlayıcı fibrozisle "
            "seyreder. Benzer şekilde bronşiyal astım gibi alerjik hastalıklarda da zararsız çevresel antijenlere karşı kronik "
            "eozinofilik ve mononükleer yanıt sürdürülür.\n\n"
            "Üçüncü grup ise parçalanamayan toksik maddelere uzun süreli maruziyettir. Bu maddeler eksojen veya endojen kaynaklı olabilir. "
            "Eksojen partiküllerin klasik örneği solunan kristalize silika (silikozis) ve asbest lifleridir (asbestozis). Fagosite "
            "edilemeyen bu partiküller makrofaj lizozomlarını patlatarak kronik enflamatuvar kaskadı tetikler. Endojen toksik maddelerin "
            "en yaygın örneği ise arter intima tabakasında biriken ve kristalleşen kolesterol esterleridir; bu tablo aterosklerozun "
            "temelindeki kronik enflamatuvar damar duvarı yıkımını yönetir."
        ),
        "synthesisNarrative": (
            "Kronik enflamasyon başlıca üç grupta incelenir: İnatçı mikrobiyal enfeksiyonlar (tüberküloz, mantarlar), "
            "immün aracılı hastalıklar (otoimmünite, alerjiler) ve parçalanamayan eksojen/endojen toksik partiküller (silika, kolesterol kristalleri)."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Otoimmün hastalıklarda (Romatoid Artrit, SLE) otoantijenler yok edilemediğinden, immün sistem kalıcı bir pozitif geri besleme döngüsüne girer ve primer kronik enflamasyon ortaya çıkar.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Endojen toksik madde maruziyetine bağlı gelişen ve arteryel duvarda mononükleer hücre birikimiyle seyreden en önemli kronik enflamasyon modeli aterosklerozdur (kolesterol birikimi).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Fagositoza dirençli intrasellüler patojenler kronik T hücre aracılı yanıtı başlatır.",
            "Eksojen etkenler (silika, asbest) makrofajlarca parçalanamadığı için fibrozisi uyarır.",
            "Alerjik hastalıklar (astım) zararsız çevresel ajanlara karşı kronik hipersensitivite oluşturur."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-003",
            "question": "Kronik enflamasyonun etiyolojisi düşünüldüğünde, aşağıdakilerden hangisi 'endojen toksik partikül birikimine bağlı gelişen kronik enflamasyon' sürecine en uygun örnektir?",
            "options": [
                "A) Taş ocağı işçisinde kristalize silika partiküllerinin solunmasıyla gelişen silikozis",
                "B) Mycobacterium tuberculosis basillerinin fagozom-lizozom füzyonunu engellemesi",
                "C) Arteryel intima tabakasında kolesterol kristalleri birikimiyle karakterize ateroskleroz",
                "D) Tip 1 diyabette pankreas adacık beta hücrelerine karşı gelişen otoimmün insülit",
                "E) Bronşiyal duvarda polen maruziyetiyle tetiklenen Th2 yanıtı ve mukus hipersekresyonu"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Ateroskleroz, arteryel intimatabakasında biriken endojen lipidlerin (özellikle okside LDL ve kolesterol kristalleri) makrofajlarca fagosite edilmesi ve inflamatuar yanıtı uyarmasıyla gelişen endojen toksik kronik enflamasyon modelidir. Silikozis eksojen toksik partiküldür; tüberküloz inatçı mikrobiyal etkendir; insülit ve astım immün aracılı tablolardır."
        }
    },

    # SLIDE 4
    {
        "slideNumber": 4,
        "title": "Mononükleer Fagositik Sistem ve Makrofaj Biyogenezi",
        "subtitle": "Kemik İliği Öncüllerinden Dolaşımdaki Monosite: Dokusal İstilaya Giriş",
        "content": (
            "Kronik enflamasyonun hücresel sahnesine baktığımızda, tartışmasız en merkezi oyuncu ve adeta orkestra şefi "
            "makrofajdır. Makrofajlar tek başlarına bağımsız hücreler değil; eskiden retiküloendotelyal sistem olarak adlandırılan, "
            "günümüzde ise 'Mononükleer Fagositik Sistem' (MFS) çatısı altında toplanan hücre ailesinin kıdemli üyeleridir. "
            "Bu sistem kemik iliğindeki hematopoetik kök hücrelerin monoblast ve promiyelosit aşamalarından geçerek kana monosit "
            "olarak verilmesiyle başlar.\n\n"
            "Dolaşımdaki kanda bulunan monositler 10-15 mikrometre çapında, tipik olarak böbrek veya fasulye şeklinde girintili "
            "nükleusları ve soluk bazofilik, ince granüllü sitoplazmaları olan hücrelerdir. Monositlerin kandaki yarı ömrü yaklaşık "
            "bir gündür. Ancak enflamatuvar bir uyaran ortaya çıktığında, endotel üzerindeki adezyon molekülleri (selektinler ve integrinler) "
            "ile kemokinlerin (özellikle MCP-1/CCL2) kılavuzluğunda damar dışına çıkarak doku aralığına ekstravaze olurlar. Dokuya geçen "
            "monosit, hacmini büyüterek, lizozom sayısını katlayarak ve zengin mikrobisidal enzim donanımına kavuşarak doku makrofajına "
            "(histiyosit) dönüşür.\n\n"
            "Enflamasyon başladıktan sonraki 48 saat içinde nötrofillerin ömrü tükenirken, doku makrofajları sahaya tamamen hakim olur. "
            "Makrofajların dokudaki ömrü nötrofiller gibi saatlerle değil; haftalar, aylar ve hatta yıllarla ölçülür. Üstelik bu hücreler "
            "yalnızca dolaşımdan göç eden monositlerle yenilenmez; yangı sahasında yerel olarak prolifere olma (mitoz bölünme) yeteneğine "
            "de sahiptirler. Bu uzun ömür ve yerel çoğalma kabiliyeti, kronik enflamasyonun neden bu kadar inatçı ve kendi kendini "
            "besleyen bir yapıya büründüğünü açıkça ortaya koyar."
        ),
        "synthesisNarrative": (
            "Mononükleer fagositik sistem, kemik iliğinde üretilip kana geçen monositlerin dokulara göç ederek uzun ömürlü "
            "makrofajlara dönüşmesiyle oluşur; enflamasyonun 48. saatinden itibaren baskın hücre haline gelirler."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Enflamasyon sahasında ilk 24 saatte nötrofiller hakimken, 48 saatten itibaren monosit kaynaklı makrofajlar baskın hücre popülasyonu haline gelir ve haftalarca dokuda kalabilir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Monositlerin kandan dokuya kemotaktik göçünde en kritik rolü oynayan kemokin Monosit Kemoatraktan Protein-1 (MCP-1 / CCL2)'dir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Dolaşımdaki monositler böbrek/fasulye çekirdekli olup kanda yaklaşık 24 saat kalır.",
            "Dokudaki makrofajlar yerel olarak çoğalma (proliferasyon) yeteneğine sahiptir.",
            "Mononükleer fagositik sistem konak savunmasının fagositoz ve antijen sunum merkezidir."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-004",
            "question": "Mononükleer fagositik sistem ve monosit-makrofaj göçü ile ilgili aşağıdaki ifadelerden hangisi BİYOLOJİK OLARAK DOĞRUDUR?",
            "options": [
                "A) Monositler kanda haftalarca kalarak doğrudan kan dolaşımında fagosite edilmiş materyali sindirir",
                "B) Dokuya göç eden makrofajlar mitoz bölünme yeteneğini tamamen kaybetmiş terminal hücrelerdir",
                "C) Enflamatuvar odakta 48. saatten itibaren makrofajlar nötrofillerin yerini alarak baskın lökosit olur",
                "D) Monositlerin endotelden dokuya geçişinde integrinler ve adezyon molekülleri rol oynamaz",
                "E) Makrofajların dokudaki yaşam süresi nötrofillerde olduğu gibi 6 ila 12 saat arasında sınırlıdır"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Akut enflamatuar yanıtta ilk 6-24 saatte nötrofiller baskınken, 24-48 saat sonrasında monositler dokuya göç eder ve 48. saatten itibaren uzun ömürlü makrofajlar dominant popülasyon haline gelir. Makrofajlar dokuda aylarca yaşayabilir ve yerel olarak çoğalabilirler."
        }
    },

    # SLIDE 5
    {
        "slideNumber": 5,
        "title": "Dokularda Yerleşik Makrofaj Popülasyonları",
        "subtitle": "Kupffer, Alveolar, Mikroglia, Sinüs Histiyositleri ve Osteoklastların Mimari Rolü",
        "content": (
            "Mononükleer fagositik sistemin çok önemli ve sınavlarda sıkça sorgulanan bir boyutu, enflamasyon yokken bile "
            "sağlıklı dokularda karakol görevi yapan 'yerleşik doku makrofajları' (rezidan histiyositler) varlığıdır. "
            "Modern immünobiyoloji bize göstermiştir ki, dokulardaki yerleşik makrofajların önemli bir kısmı erişkin kemik iliğinden "
            "değil, embriyogenez sırasında vitellüs kesesi (yolk sac) ve fetal karaciğerdeki öncüllerden köken alarak dokulara yerleşir. "
            "Bu hücreler bulundukları mikroçevreye kusursuz şekilde adapte olmuş, özgül morfoloji ve fonksiyon kazanmış hücrelerdir.\n\n"
            "Karaciğer sinüzoidlerinin lümenine bakan yüzeyinde yerleşen makrofajlara 'Kupffer hücreleri' denir; portal dolaşımla "
            "bağırsaktan gelen mikrobiyal antijenleri ve yaşlanmış eritrositleri süzerek sistemik dolaşıma geçmesini engellerler. "
            "Akciğer alveol lümenlerinde ve interstisyumunda 'Alveolar makrofajlar' solunumla alınan toz, partikül ve mikropları "
            "temizler (kalp yetmezliğinde hemosiderin yüklü hemosiderofajlara dönüşürler). Santral sinir sisteminde yer alan mezankimal "
            "kökenli 'Mikroglia' hücreleri, nöronal artıkların fagositozundan ve nöroinflamasyondan sorumludur.\n\n"
            "Dalak kırmızı pulpasında ve lenf nodu medullasında bulunan 'Sinüs histiyositleri', lenf ve kan akımındaki yabancı "
            "antijenleri yakalarken; kemik dokusunda çok çekirdekli dev hücre formuna evrilen 'Osteoklastlar' kemik rezorpsiyonunu "
            "yönetir. Derideki epidermiste antijen sunucu makrofaj benzeri 'Langerhans hücreleri' bulunur. Bu yerleşik bekçiler, "
            "dokuda bir hasar veya istila algıladıkları anda ilk alarmı vererek dolaşımdaki lökositleri bölgeye çağıran sitokinleri "
            "üretirler ve kronik enflamasyonun fitilini ateşlerler."
        ),
        "synthesisNarrative": (
            "Dokularda yerleşik makrofajlar (karaciğerde Kupffer, akciğerde alveolar makrofaj, beyinde mikroglia, kemikte osteoklast) "
            "embriyonik öncüllerden dokulara yerleşmiş olup organa özgü savunma ve homeostazı yönetirler."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Dokulardaki yerleşik makrofajların (Kupffer, mikroglia) önemli bir kısmı fetal yaşamda vitellüs kesesi ve fetal karaciğerden köken alır ve doku içinde kendi kendini yenileyebilir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Santral sinir sisteminde mononükleer fagositik sistemin temsilcisi olan ve doku hasarında fagositik aktivite gösteren hücre mikroglia hücresidir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Karaciğer Kupffer hücreleri portal venden gelen toksin ve antijenleri süzmede kritik rol oynar.",
            "Alveolar makrofajlar solunum havasındaki yabancı partikülleri fagositozla elimine eder.",
            "Osteoklastlar monosit-makrofaj serisinden köken alan kemik erimesinden sorumlu dev hücrelerdir."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-005",
            "question": "Mononükleer fagositik sistem elemanları ve bulundukları doku eşleştirmelerinden hangisi YANLIŞTIR?",
            "options": [
                "A) Karaciğer — Kupffer hücresi",
                "B) Akciğer — Alveolar makrofaj",
                "C) Santral Sinir Sistemi — Mikroglia",
                "D) Kemik Dokusu — Osteoklast",
                "E) Epidermis — Melanosit"
            ],
            "correctAnswer": 4,
            "explanation": "E seçeneği yanlıştır. Epidermisteki mononükleer fagosit/antijen sunucu hücre Langerhans hücresidir. Melanositler ise nöral krest kökenli melanin pigmenti üreten hücrelerdir; fagositik sisteme dahil değillerdir. A, B, C ve D eşleştirmeleri doğru doku makrofajlarıdır."
        }
    },

    # SLIDE 6
    {
        "slideNumber": 6,
        "title": "Makrofaj Aktivasyonunda M1 (Klasik) Yolak",
        "subtitle": "Mikrobisidal Saldırı, iNOS, Reaktif Oksijen Türleri ve Proinflamatuar Fırtına",
        "content": (
            "Dokuya ulaşan ya da dokuda bulunan bir makrofaj uyarılmadığı sürece dinlenme fazındadır. Ancak mikroçevreden "
            "gelen sinyaller makrofajın kaderini ve işlevsel kimliğini belirler. Patolojide makrofaj aktivasyonunu iki zıt uç "
            "üzerinde modelleriz: Klasik aktivasyon (M1) ve Alternatif aktivasyon (M2). Bu iki kutup, immün sistemin 'savaş' mı "
            "yoksa 'barış ve yeniden inşa' mı ilan edeceğini belirler. İlk olarak savaşçı fenotip olan M1 yolağını derinlemesine inceleyelim.\n\n"
            "M1 aktivasyonu temelde iki güçlü uyaran tarafından tetiklenir: Birincisi, mikrobiyal endotoksinler (özellikle gram-negatif "
            "bakteri lipopolisakkariti - LPS) ve patojenlerin hücre duvar bileşenleridir; bunlar makrofaj yüzeyindeki Toll-Benzeri Reseptörleri "
            "(TLR'ler) bağlar. İkincisi ve en güçlü endojen kışkırtıcı ise aktive antijene-özgül T lenfositlerinden (özellikle Th1 hücreleri "
            "ve Natural Killer hücreleri) salgılanan İnterferon-gama (IFN-γ) sitokinidir. Bu iki sinyal makrofaj içinde NF-κB ve STAT1 "
            "transkripsiyon faktörlerini aktive eder.\n\n"
            "Klasik olarak aktive olan M1 makrofajının metabolik motoru tamamen mikrobisidal saldırıya kilitlenir. Hücrede İndüklenebilir "
            "Nitrik Oksit Sentaz (iNOS) enzimi eksprese edilir; iNOS L-arjinin aminoasidini kullanarak masif miktarda Nitrik Oksit (NO) üretir. "
            "Eşzamanlı olarak fagositik NADPH oksidaz enzimi aktive edilerek Reaktif Oksijen Türleri (ROS) ve lizozomal proteolitik enzimler "
            "salınır. NO ile süperoksitin birleşmesiyle ölümcül bir radikal olan peroksinitrit meydana gelir. Ayrıca M1 makrofajları "
            "yoğun miktarda TNF-alfa, IL-1, IL-6 ve IL-12 salgılayarak yangıyı alevlendirir. Patojenleri yok eden bu cephane, maalesef "
            "çevre konak dokusunda da ağır kollateral hasar ve nekroz yaratır."
        ),
        "synthesisNarrative": (
            "M1 (klasik) makrofaj aktivasyonu LPS/TLR ligandları ve IFN-γ ile tetiklenir; iNOS üzerinden NO, NADPH oksidaz ile "
            "ROS ve lizozomal enzimler üreterek mikropları öldürürken doku hasarını ve enflamasyonu körükler."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Klasik M1 aktivasyonunu sağlayan en güçlü immün sitokin Th1 lenfosit kaynaklı IFN-γ'dır. Enzim belirteci indüklenebilir nitrik oksit sentaz (iNOS)'tır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: M1 makrofajları mikrobisidal aktiviteyi NO, ROS ve lizozomal enzimlerle yürütür; çevreye IL-1, TNF ve IL-12 salarak yangıyı amplifiye ederler.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "M1 aktivasyonunun tetiği LPS (TLR uyarısı) ve Th1 kaynaklı IFN-γ'dır.",
            "L-arjinin iNOS aracılığıyla sitotoksik nitrik okside (NO) dönüştürülür.",
            "M1 fenotipi mikrop öldürmede üstün, ancak konak doku yıkımında baş sorumludur."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-006",
            "question": "Klasik yolakla aktive olmuş (M1) bir makrofajın mikrobisidal yanıtı ve biyolojik özellikleri ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Primer tetikleyici sitokin: IL-4 / Anahtar enzim: Arjinaz-1",
                "B) Primer tetikleyici sitokin: IFN-γ / Anahtar enzim: İndüklenebilir nitrik oksit sentaz (iNOS)",
                "C) Primer tetikleyici sitokin: IL-13 / Salınan mediyatör: TGF-beta",
                "D) Temel hücresel fonksiyon: Fibroblast proliferasyonu ve kollajen sentezi",
                "E) Salgılanan sitokin profili: IL-10 ve çözünür IL-1 reseptör antagonisti"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Klasik aktive M1 makrofajları Th1 hücre kaynaklı IFN-γ ve mikrobiyal LPS ile uyarılır. Karakteristik enzimi iNOS'tur ve L-arjininden NO üreterek mikrobisidal etki gösterir. IL-4/IL-13, Arjinaz-1, TGF-beta ve fibrozis ise alternatif M2 aktivasyonunun özellikleridir."
        }
    },

    # SLIDE 7
    {
        "slideNumber": 7,
        "title": "Makrofaj Aktivasyonunda M2 (Alternatif) Yolak",
        "subtitle": "IL-4/IL-13 Sinyali, Arjinaz, Doku Onarımı, Anjiyogenez ve Fibrozis Kaskadı",
        "content": (
            "Enflamasyonun yıkıcı fırtınası dindikten sonra veya ortama paraziter antijenler ile alerjik sitokinler hakim "
            "olduğunda sahneye makrofajın ikinci yüzü çıkar: Alternatif aktivasyon yolağı (M2). M2 makrofajlar yangıyı söndüren, "
            "doku enkazını temizleyen ve harabe haline gelmiş organ mimarisini tamir eden 'rekonstrüksiyon mühendisleridir'. "
            "Bu hücreler, doku hasarının ardından başlayan yara iyileşmesi ve rejenerasyon basamaklarının temel orkestratörleridir.\n\n"
            "M2 aktivasyonu IFN-γ veya endotoksinlerle tetiklenmez. Aksine bu yolak, Th2 lenfositleri, mast hücreleri ve eozinofiller "
            "tarafından salgılanan İnterlökin-4 (IL-4) ve İnterlökin-13 (IL-13) sitokinleri ile indüklenir. Bu sitokinler makrofajda "
            "STAT6 transkripsiyon yolağını aktive ederek bambaşka bir gen ekspresyon profilini devreye sokar. M1 hücresinin aksine "
            "M2 makrofajında iNOS aktivitesi baskılanmıştır; bunun yerine 'Arjinaz-1' enzimi aşırı eksprese edilir. Arjinaz enzimi "
            "L-arjinini NO yerine L-ornitin ve üreye dönüştürür. Ornitin ise prolin aminoasidine çevrilerek kollajen sentezinin "
            "ve hücre proliferasyonunu sağlayan poliaminlerin temel yapıtaşını oluşturur.\n\n"
            "M2 makrofajlarının cephanesinde mikrobisidal toksinler değil, güçlü büyüme faktörleri yer alır. Başta Dönüştürücü Büyüme Faktörü "
            "Beta (TGF-β) olmak üzere, Trombosit Kaynaklı Büyüme Faktörü (PDGF) ve Fibroblast Büyüme Faktörü (FGF) salgılarlar. "
            "Bu faktörler fibroblastları bölgeye çekip uyararak yoğun kollajen sentezletir (fibrogenez) ve endotel hücrelerini çoğaltarak "
            "yeni kılcal damarlar tomurcuklandırır (anjiyogenez). Ayrıca IL-10 ve TGF-β salgılayarak enflamatuvar yanıtı aktif olarak baskılarlar. "
            "Ancak M2 yanıtı kontrolsüz uzarsa organları taşlaştıran patolojik fibrozis (örneğin karaciğer sirozu, idiyopatik pulmoner fibrozis) "
            "gelişir; bu nedenle M2 aktivitesi iki ucu keskin bir kılıç gibidir."
        ),
        "synthesisNarrative": (
            "M2 (alternatif) makrofaj aktivasyonu Th2 kaynaklı IL-4 ve IL-13 ile uyarılır; arjinaz aktivasyonu ile kollajen prekürsörleri "
            "üretir, TGF-β, PDGF ve FGF salarak anjiyogenez, yara iyileşmesi ve fibrozisi teşvik eder."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: M2 makrofajları IL-4 ve IL-13 sitokinleri ile indüklenir. Mikrobisidal kapasiteleri düşüktür; temel görevleri enflamasyonu IL-10 ile baskılamak ve TGF-β ile fibrozis/onarım sağlamaktır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: M2 makrofajlarında L-arjinini kollajen prekürsörü olan prolini oluşturmak üzere ornitine çeviren ve fibrozisi destekleyen temel enzim Arjinaz-1'dir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "M2 indükleyicileri IL-4 ve IL-13 sitokinleridir (Th2 ve eozinofil kaynaklı).",
            "Salgılanan TGF-β ve PDGF fibroblastları uyararak kollajen birikimini ve skarı yönetir.",
            "Aşırı ve kontrolsüz M2 yanıtı organ fibrozisi ve sirozun moleküler motorudur."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-007",
            "question": "Alternatif yolakla aktive olmuş (M2) makrofajların biyolojik fonksiyonları ve salgıladıkları mediyatörlerle ilgili aşağıdakilerden hangisi YANLIŞTIR?",
            "options": [
                "A) IL-4 ve IL-13 sitokinlerinin reseptörlerine bağlanmasıyla aktive olurlar",
                "B) L-arjinin metabolizmasında arjinaz enzimini kullanarak ornitin ve prolin üretimini artırırlar",
                "C) Masif miktarda nitrik oksit (NO) ve reaktif oksijen ürünleri (ROS) sentezleyerek doku nekrozuna yol açarlar",
                "D) Salgıladıkları TGF-β ve PDGF aracılığıyla fibroblast kemotaksisi ve kollajen sentezini uyarırlar",
                "E) IL-10 ve TGF-β salgılayarak anti-enflamatuvar ve immünsüpresif etki gösterirler"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği yanlıştır. Masif NO ve ROS üreterek mikrobisidal etki ve doku hasarı oluşturan hücre M1 makrofajıdır. Alternatif aktive M2 makrofajlarının mikrobisidal toksin üretimi baskılanmıştır; odak noktaları anti-enflamatuvar etki, anjiyogenez ve doku onarımı/fibrozisdir."
        }
    },

    # SLIDE 8
    {
        "slideNumber": 8,
        "title": "M1 ve M2 Fenotipik Spektrumu ve Plastisite",
        "subtitle": "Kronik Doku Hasarı, Çözünme ve Skar Gelişimi Arasındaki Hassas Moleküler Denge",
        "content": (
            "Ders kitaplarında pedagojik netlik sağlamak amacıyla M1 ve M2 makrofajları iki ayrı hücre tipi gibi "
            "anlatsak da, gerçek insan patolojisinde bu iki kutup siyah ve beyaz gibi birbirinden kesin çizgilerle ayrılmaz. "
            "Makrofajlar son derece yüksek fenotipik plastisiteye (esnekliğe) sahip hücrelerdir. Bir makrofaj mikroçevredeki sitokin "
            "havuzunun değişmesiyle M1 durumundan M2 durumuna veya tam tersi yönde M2'den M1'e transdiferansiye olabilir. "
            "Ayrıca in vivo doku kesitlerinde her iki fenotipin özelliklerini melez olarak taşıyan ara hücre popülasyonları sıklıkla mevcuttur.\n\n"
            "Normal fizyolojik bir iyileşme sürecinde mükemmel bir zamansal orkestrasyon izlenir: İlk günlerde dokuda M1 makrofajları "
            "hakimdir; patojenler yok edilir, nekrotik hücre artıkları fagositozla ortamdan uzaklaştırılır. İşlem tamamlandığında, apoptotik "
            "nötrofillerin makrofajlarca yutulması (efferositoz) makrofaj içinde anti-enflamatuvar bir şalteri açar. Hücre fenotipini "
            "M2 yönüne çevirir; TGF-β ve IL-10 üretimi tavan yapar, granülasyon dokusu oluşturulur ve defekt nedbe ile kapatılır.\n\n"
            "Patolojik kronik enflamasyonda ise bu hassas denge tam anlamıyla çökmüştür. Eğer M1 fazı inatçı bir mikroorganizma "
            "(tüberküloz) veya otoantijen nedeniyle kapanmazsa, durmaksızın devam eden doku nekrozu, kavitasyon ve parankim kaybı yaşanır. "
            "Aksine, eğer etken tam temizlenmeden aşırı bir M2 polarizasyonu başlarsa veya M2 yanıtı durdurulamazsa; karaciğerde siroz, "
            "akciğerde idiyopatik pulmoner fibrozis, böbrekte glomerüloskleroz ve konstriktif perikardit gibi organı işlevsiz taşlaşmış "
            "bir kitleye çeviren patolojik fibrozis tabloları meydana gelir."
        ),
        "synthesisNarrative": (
            "M1 ve M2 fenotipleri mutlak sabit durumlar olmayıp mikroçevreye göre değişebilen dinamik bir spektrum oluşturur; "
            "dengenin M1 tarafında kalması kalıcı doku destrüksiyonuna, kontrolsüz M2 tarafına kayması ise organ fibrozisine yol açar."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Apoptotik lökositlerin makrofajlarca temizlenmesi (efferositoz), makrofajın M1 fenotipinden doku tamir edici M2 fenotipine geçişini sağlayan fizyolojik sinyaldir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Kronik enflamasyon seyrinde doku hasarını M1 makrofaj ürünleri (NO, ROS, proteazlar) yaparken, gelişen parankimal fibrozis ve sirozdan M2 kaynaklı büyüme faktörleri (özellikle TGF-β) sorumludur.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Makrofajlar çevre sitokin sinyallerine göre M1 ve M2 arasında geçiş yapabilir (plastisite).",
            "Efferositoz akut yangının sonlanıp onarım fazına geçişindeki en kilit biyolojik eşiktir.",
            "Organ yetmezliğiyle biten fibrotik hastalıkların temelinde kontrolsüz M2/TGF-β aktivitesi yatar."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-008",
            "question": "Makrofaj plastisitesi ve M1/M2 denge bozuklukları dikkate alındığında, aşırı ve kontrolsüz M2 aktivasyonunun en olası patolojik sonucu aşağıdakilerden hangisidir?",
            "options": [
                "A) Akut kazeöz nekroz ve dokuda kavitasyon oluşumu",
                "B) Lökopeni ve sistemik septik şok tablosu",
                "C) Doku parankiminin yerini yoğun ekstraselüler matriksin alması ve organ fibrozisi",
                "D) Damar duvarında endotel hücrelerinin apoptozu ve masif iç kanama",
                "E) Nötrofillerin aşırı göçüyle karakterize fulminan süpüratif apse formasyonu"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Alternatif (M2) makrofaj aktivasyonunun kontrolsüz ve uzamış olması, aşırı miktarda TGF-β, PDGF ve FGF üretimine yol açarak fibroblastları ve miyofibroblastları uyarır; bu durum parankim kaybı ve organ fibrozisi (örneğin siroz veya akciğer fibrozisi) ile sonuçlanır. Doku erimesi ve kavitasyon M1 hasarıdır."
        }
    },

    # SLIDE 9
    {
        "slideNumber": 9,
        "title": "T Lenfosit Alt Tipleri ve Polarizasyon",
        "subtitle": "Th1, Th2 ve Th17 Hücrelerinin Sitokin İmzaları ve Enflamatuar Yanıtı Şekillendirmesi",
        "content": (
            "Kronik enflamasyonda makrofajlar kas gücünü ve yürütmeyi temsil ederken, T lenfositleri stratejik kararları "
            "alan ve süreci yönlendiren kurmay heyetidir. Hücresel bağışıklığın merkezinde yer alan naif CD4+ T yardımcı (Th) "
            "hücreleri, antijen sunucu hücrelerle karşılaştıktan sonra ortamdaki sitokin sinyallerine bağlı olarak üç ana fonksiyonel "
            "alt tipe farklılaşırlar (polarizasyon): Th1, Th2 ve Th17. Bu üç hücre alt grubu, salgıladıkları özgül sitokinler "
            "aracılığıyla kronik enflamasyonun tipini ve şiddetini belirler.\n\n"
            "Th1 hücreleri hücre içi mikroorganizmalara (bakteriler, virüsler, parazitler) karşı gelişen savunmanın baş aktörüdür. "
            "İl-12 etkisiyle farklılaşırlar ve temel sitokinleri İnterferon-gama (IFN-γ)'dır. IFN-γ doğrudan klasik M1 makrofaj "
            "aktivasyonunu tetikler, fagositozu güçlendirir ve gecikmiş tip aşırı duyarlılık reaksiyonunu (Tip IV) yönetir. Otoimmün "
            "hastalıkların çoğunda (örneğin tip 1 diyabet, multipl skleroz) doku hasarından sorumludurlar.\n\n"
            "Th2 hücreleri helmintik parazit enfeksiyonları ve alerjik hastalıklarda (astım, egzama) başrolü oynar. IL-4 etkisiyle "
            "farklılaşırlar ve IL-4, IL-5 ile IL-13 salgılarlar. IL-4 B lenfositlerinden IgE sentezini indükler; IL-5 eozinofillerin "
            "kemik iliğinden çıkışını ve aktivasyonunu sağlar; IL-4 ve IL-13 ise M2 makrofaj polarizasyonunu ve mukus sekresyonunu "
            "tetikler. Th17 hücreleri ise IL-6 ve TGF-β varlığında gelişir, IL-17 ve IL-22 salgılarlar. IL-17 diğer hücrelerden "
            "kemokin salınımını tetikleyerek yangı sahasına yoğun nötrofil ve monosit akını sağlar; psöriasis, ankilozan spondilit ve "
            "inflamatuar barsak hastalıklarının patogenezinde kritik öneme sahiptir."
        ),
        "synthesisNarrative": (
            "CD4+ T yardımcı hücreleri üçe ayrılır: Th1 (IFN-γ ile M1 makrofaj aktivasyonu), Th2 (IL-4, IL-5, IL-13 ile alerji, "
            "eozinofil ve M2 aktivasyonu) ve Th17 (IL-17 ile nötrofil/monosit toplanması ve otoimmün hasar)."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Th1 hücreleri IFN-γ salarak M1 makrofajlarını uyarırken; Th2 hücreleri IL-4, IL-5 ve IL-13 salarak eozinofilleri ve alternatif (M2) makrofajları aktive eder.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Eozinofillerin proliferasyonunu, dokuya göçünü ve aktivasyonunu spesifik olarak uyaran anahtar Th2 sitokini İnterlökin-5 (IL-5)'tir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Th1 fenotipi hücre içi patojenler ve Tip IV aşırı duyarlılıkla özdeşleşmiştir.",
            "Th2 sitokinleri (IL-4/IL-13) IgE sentezini ve doku onarım/fibrozis yolunu tetikler.",
            "Th17 lenfositleri IL-17 salgısıyla nötrofilik infiltrasyonu kronik zemine davet eder."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-009",
            "question": "CD4+ T yardımcı lenfosit alt grupları, salgıladıkları anahtar sitokinler ve fonksiyonları ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Th1 hücresi — IL-5 salgılar — Eozinofil lökositlerin aktivasyonunu sağlar",
                "B) Th2 hücresi — IFN-γ salgılar — Klasik (M1) makrofaj aktivasyonunu uyarır",
                "C) Th17 hücresi — IL-17 salgılar — Kemokinler aracılığıyla nötrofil ve monosit toplanmasını uyarır",
                "D) Th1 hücresi — IL-4 salgılar — B lenfositlerinden IgE sentezini indükler",
                "E) Th2 hücresi — IL-12 salgılar — Doğal katil (NK) hücre sitotoksisitesini artırır"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Th17 lenfositleri IL-17 salgılayarak endotel ve epitelden kemokin üretimini indükler, böylece bölgeye yoğun nötrofil ve monosit toplanmasını sağlarlar. Th1 IFN-γ salar (M1 aktivasyonu), Th2 ise IL-4, IL-5 (eozinofil) ve IL-13 salgılar."
        }
    },

    # SLIDE 10
    {
        "slideNumber": 10,
        "title": "Makrofaj-Lenfosit İki Yönlü Kısır Döngüsü",
        "subtitle": "Antijen Sunumu, IFN-γ Sinyalizasyonu ve Kronisitenin İmmünolojik Devridaimi",
        "content": (
            "Kronik enflamasyonun aylarca hatta yıllarca kendi kendine nasıl devam edebildiğini anlamak için, "
            "patolojinin en zarif ve tehlikeli mekanizmalarından biri olan 'Makrofaj-Lenfosit İki Yönlü Etkileşim Döngüsü'nü "
            "kavramak şarttır. Bu etkileşim adeta yangına sürekli odun atan bir pozitif geri besleme (feedback) makinesidir. "
            "İmmün sistem bu döngü sayesinde başlangıçtaki küçük bir antijenik uyarıyı devasa bir hücresel savunma cephesine dönüştürür.\n\n"
            "Döngü şu şekilde işler: Dokuda bir yabancı antijen veya inatçı mikroorganizma ile karşılaşan makrofaj, bu ajanı fagosite eder. "
            "Antijeni lizozomlarında işledikten sonra, hücre yüzeyindeki Majör Histokompatibilite Kompleksi Sınıf II (MHC-II) molekülleri "
            "üzerinde CD4+ T lenfositlerine sunar. Eşzamanlı olarak makrofaj, T hücresine ko-stimülatuvar moleküller (B7/CD80-CD86) sağlar "
            "ve ortama güçlü bir sitokin olan İnterlökin-12 (IL-12) salgılar. IL-12, antijeni tanıyan naif T hücresinin hızla aktive "
            "olup Th1 fenotipine farklılaşmasını ve klonal olarak çoğalmasını emreder.\n\n"
            "Aktivasyonunu tamamlayan Th1 lenfositi ise borçlu kalmaz; derhal bol miktarda İnterferon-gama (IFN-γ) sentezleyip "
            "dokudaki makrofajların üzerine döker. IFN-γ, makrofajların klasik M1 yolunu aktive eden en kudretli sitokindir. "
            "IFN-γ uyarısını alan makrofaj daha fazla lizozomal enzim üretir, fagositoz gücünü artırır, TNF ve IL-1 salar, çevreye "
            "daha fazla kemokin yayarak kandan yeni monositleri çağırır ve T hücresine daha fazla antijen sunar. Böylece her iki hücre "
            "birbirini sürekli uyararak yangının sönmesine izin vermez. Eğer bu döngü regülatuar T hücreleri veya immünsüpresif "
            "mekanizmalarla kırılmazsa, doku nekrozu ve ardından kaçınılmaz organ fibrozisi gelişir."
        ),
        "synthesisNarrative": (
            "Makrofajlar T hücrelerine antijen sunup IL-12 salarak onları Th1'e dönüştürür; aktive Th1 hücreleri ise IFN-γ "
            "salgılayarak makrofajları yeniden uyarır. Bu iki yönlü pozitif döngü kronik enflamasyonun inatçı yakıtıdır."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Makrofajlarca salgılanan IL-12 naif T hücrelerini Th1 yönünde polarize eder; aktive Th1 hücreleri ise IFN-γ salarak makrofajları tekrar aktive eder (pozitif feedback döngüsü).",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Kronik enflamasyon odağında makrofaj ile T lenfositi arasındaki çift yönlü moleküler köprüde makrofajdan T hücresine IL-12, T hücresinden makrofaja IFN-γ sinyali iletilir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Makrofajlar MHC-II ve ko-stimülatörlerle T lenfositlerine profesyonel antijen sunar.",
            "IL-12 ve IFN-γ kronik yangının kendi kendini besleyen eksenini oluşturur.",
            "Bu kısır döngü granülomatöz enflamasyonun da hücresel ve moleküler omurgasıdır."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-010",
            "question": "Kronik enflamasyonda makrofaj ve T lenfositler arasında kurulan iki yönlü etkileşim döngüsüyle ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Makrofajlar T lenfositlerine IL-4 salgılayarak Th1 farklılaşmasını engeller",
                "B) T lenfositleri makrofajları aktive etmek için öncelikle IL-10 ve IL-13 sitokinlerini kullanır",
                "C) Makrofajlar antijen sunumuyla birlikte IL-12 salgılar; aktive Th1 hücreleri ise IFN-γ üreterek makrofajları uyarır",
                "D) Bu döngü negatif geri besleme niteliğinde olup enflamasyonun birkaç günde kendiliğinden sönmesini sağlar",
                "E) Döngü yalnızca B lenfositlerinin plazma hücresine dönüşmesiyle tetiklenir ve T hücrelerine bağımlı değildir"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Makrofajlar antijen sunumu yapıp IL-12 salgılayarak naif T lenfositlerini Th1 hücrelerine dönüştürür. Aktive Th1 lenfositleri ise IFN-γ salgılayarak makrofajları klasik yoldan (M1) kuvvetle aktive eder. Bu pozitif feedback döngüsü kronik yangının devamını sağlar."
        }
    },

    # SLIDE 11
    {
        "slideNumber": 11,
        "title": "Plazma Hücreleri ve B Lenfosit İnfiltrasyonu",
        "subtitle": "Saat Kadranı Kromatini, Russell Cisimcikleri ve Tersiyer Lenfoid Yapılar",
        "content": (
            "Kronik enflamatuvar eksüdanın en karakteristik ve tanısal hücrelerinden bir diğeri plazma hücreleridir. "
            "Plazma hücreleri, antijenik uyarım sonucu T lenfositlerinin desteğiyle terminal olarak farklılaşmış antikor fabrikası "
            "B lenfositleridir. Bir doku kesitinde yoğun plazma hücresi infiltrasyonu görmek, patoloğa sürecin tartışmasız kronik "
            "olduğunu ve lokal bir hümoral immün yanıtın yürütüldüğünü fısıldar.\n\n"
            "Mikroskop altında plazma hücresi morfolojisi son derece tipiktir: Eksantrik (hücrenin bir kenarına itilmiş) yuvarlak "
            "bir nükleusu vardır. Nükleus içindeki heterokromatin adeta bir araba tekerleğinin parmaklıkları veya klasik bir duvar "
            "saatinin rakamları gibi nükleer zar boyunca radyal olarak kümelenmiştir; bu görünüme 'saat kadranı' (clock-face) ya da "
            "'araba tekerleği' (cartwheel) kromatini denir. Sitoplazması, masif immünglobulin sentezleyen yoğun granüllü endoplazmik "
            "retikulum (GER) içeriğinden ötürü koyu amfofilik-bazofilik boyanır. Nükleusun hemen yanında ise iyi gelişmiş Golgi aygıtına "
            "karşılık gelen soluk, perinükleer bir halo (berrak alan) dikkat çeker.\n\n"
            "Bazen antikor sentezi o kadar aşırı ve hızlı olur ki, immünglobulinler GER sisternalarında birikerek eozinofilik, homojen, "
            "yuvarlak globüler inklüzyonlar oluşturur; bunlara 'Russell cisimcikleri' adı verilir (eğer benzer inklüzyonlar nükleusta "
            "izlenirse 'Dutcher cisimcikleri' denir). Romatoid artrit sinovyumu veya Hashimoto tiroiditi gibi ileri derecede uzamış "
            "kronik enflamasyon alanlarında, toplanan B ve T lenfositleri ile plazma hücreleri öylesine organize olurlar ki lenf nodu "
            "benzeri foliküller ve germinal merkezler kurarlar. Dokuda sonradan kazanılan bu organize mimariye 'Tersiyer Lenfoid Organlar' "
            "(lenfoid neogenezis) adı verilir."
        ),
        "synthesisNarrative": (
            "Plazma hücreleri eksantrik 'saat kadranı' nükleusu, perinükleer halosu ve Russell cisimcikleriyle tanınan antikor üreten "
            "B hücre türevleridir; kronik süreçte dokuda tersiyer lenfoid foliküller oluşturabilirler."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Plazma hücrelerinde GER sisternalarında biriken immünglobulin birikintilerine 'Russell cisimciği', nükleus içine taşan inklüzyonlara ise 'Dutcher cisimciği' adı verilir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Işık mikroskobunda eksantrik yerleşimli nükleusunda 'araba tekerleği / saat kadranı' kromatin paterni ve perinükleer soluk Golgi halosu gösteren hücre plazma hücresidir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Plazma hücreleri lokal antikor (immünglobulin) sentezinden sorumlu B hücreleridir.",
            "Saat kadranı kromatini heterokromatini nükleer zar boyunca radyal diziliminden doğar.",
            "Tersiyer lenfoid organlar (lenfoid folikül oluşumu) uzamış kronik yangının bir sonucudur."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-011",
            "question": "Kronik enflamasyonlu bir doku biyopsisinde; eksantrik yerleşimli 'araba tekerleği' kromatinli nükleusu, perinükleer soluk zonu ve sitoplazmasında immünglobulin birikimine bağlı eozinofilik Russell cisimcikleri bulunan hücre aşağıdakilerden hangisidir?",
            "options": [
                "A) Epiteloid histiyosit",
                "B) Plazma hücresi",
                "C) Mast hücresi",
                "D) Eozinofil lökosit",
                "E) Fibroblast"
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Eksantrik yerleşimli araba tekerleği/saat kadranı nükleusu, perinükleer açık renkli Golgi halosu ve aşırı immünglobulin birikimine bağlı Russell cisimcikleri plazma hücresinin karakteristik histomorfolojik özellikleridir."
        }
    },

    # SLIDE 12
    {
        "slideNumber": 12,
        "title": "Eozinofiller ve Kronik Enflamasyon",
        "subtitle": "Eotaksin Kemotaksisi, Major Basic Protein (MBP) ve Paraziter/Alerjik Doku Yıkımı",
        "content": (
            "Genellikle akut alerjik reaksiyonların hücresi olarak bilinse de, eozinofiller belirli kronik enflamasyon "
            "tiplerinde başrolü oynayan kritik lökositlerdir. Özellikle helmint tipi paraziter enfeksiyonlarda, kronik bronşiyal "
            "astımda, alerjik rinitte, atopik dermatitte ve eozinofilik özofajit/gastroenterit tablolarında doku infiltrasyonunun "
            "hakim hücresi eozinofillerdir.\n\n"
            "Eozinofillerin yangı sahasına toplanması çok spesifik bir kemokin ve sitokin ağıyla yönetilir. Th2 hücrelerinden salgılanan "
            "IL-5, kemik iliğinde eozinofil üretimini ve kana salınışını dramatik olarak artırırken; dokulardan salgılanan ve CC kemokin "
            "ailesine mensup olan 'Eotaksin' (özellikle CCL11), eozinofillerin endotelden dokuya transmigrasyonunu kusursuz bir hassasiyetle "
            "sağlar. Mikroskop altında eozinofiller tipik olarak iki loblu (gözlük şeklinde) nükleusları ve eozin boyasıyla parlak "
            "kırmızı-pembe boyanan iri sitoplazmik granülleri ile hemen göze çarparlar.\n\n"
            "Bu parlak granüller aslında öldürücü bir biyokimyasal cephaneliktir. Granüllerin kristaloid santralinde 'Major Basic Protein' "
            "(MBP) yer alır; MBP helmintlerin kütikulasını delerek paraziti felç eder ve öldürür. Ancak aynı zamanda konak epitel hücreleri "
            "için de son derece sitotoksiktir; kronik astımda bronş epitelinin dökülmesinden ve doku hasarından sorumludur. Granüllerde "
            "ayrıca Eozinofil Katyonik Protein (ECP), Eozinofil Peroksidaz (EPO) ve nörotoksin bulunur. İlginç bir şekilde eozinofiller, "
            "mast hücrelerinden salınan histamini yıkan 'Histaminaz' ve lökotrienleri parçalayan 'Arilsülfataz' enzimlerine de sahiptir; "
            "bu sayede alerjik reaksiyonun erken fazını sınırlamaya çalışırken, kronik fazda kendi granül proteinleriyle dokuyu harap ederler."
        ),
        "synthesisNarrative": (
            "Eozinofiller IgE aracılı alerjilerde ve paraziter enfeksiyonlarda IL-5 ve eotaksin ile dokuya çekilir; "
            "Major Basic Protein (MBP) parazitleri öldürürken aynı zamanda konak epitelinde ağır kronik doku hasarı meydana getirir."
        ),
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "🔴 ÖNEMLİ: Eozinofillerin granüllerinde bulunan Major Basic Protein (MBP), helmintlere karşı parazitisidal etki gösterirken, kronik astımda bronş epitelinde belirgin lizis ve doku yıkımına yol açar.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "🔵 ÇIKMIŞ SORU: Eozinofil lökositlerin dokuya spesifik kemotaksisini sağlayan kemokin Eotaksin (CCL11); üretimini ve olgunlaşmasını uyaran temel sitokin ise IL-5'tir.",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Bilobe (iki parçalı) nükleus ve parlak pembe/kırmızı granüller tanı koydurucudur.",
            "MBP, ECP ve EPO helmint parazitleri öldürmede özelleşmiş katyonik proteinlerdir.",
            "Eozinofiller histaminaz enzimi ile mast hücre mediyatörlerini inaktive edebilir."
        ],
        "practiceQuestion": {
            "id": "prac-kronik-012",
            "question": "Helmint enfeksiyonu veya kronik alerjik enflamasyon alanında bol miktarda bulunan, parazit kütikulasını zedeleyen fakat konak epitelinde de nekroza yol açan Major Basic Protein (MBP) içeren hücre aşağıdakilerden hangisidir?",
            "options": [
                "A) Nötrofil lökosit",
                "B) Bazofil lökosit",
                "C) Eozinofil lökosit",
                "D) Epiteloid histiyosit",
                "E) Plazma hücresi"
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği doğrudur. Eozinofil lökositlerin spesifik granüllerinde yüksek konsantrasyonda bulunan Major Basic Protein (MBP), parazitlere karşı toksik olan ancak kronik enflamasyonda (örneğin bronşiyal astımda) epitel hasarına yol açan temel katyonik proteindir."
        }
    }
]
