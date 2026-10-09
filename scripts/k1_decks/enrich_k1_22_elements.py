# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_22_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik karar verme, bebek besleme ikilemleri, emzirme ve weaning yönetimi) ögeleri."""
    return {
        2: make_branching_logic(
            "Toplum sağlığı merkezinde çalışan bir hekim, bölgesindeki 5 yaş altı çocuklarda bodurluk (stunting) oranının %25 olduğunu saptıyor. Belediye başkanı bu sorunu çözmek için okul çağındaki çocuklara süt dağıtmayı öneriyor.",
            "Halk sağlığı ilkelerine göre bu bodurluk tablosunu kalıcı olarak önlemek için en kritik biyolojik pencere hangisidir?",
            [
                {
                    "text": "İlk 1000 Gün (Gebeliğin başlangıcından 2 yaşın sonuna kadar olan süre)",
                    "isCorrect": True,
                    "feedback": "Mükemmel Halk Sağlığı Kararı: Bodurluk kronik yetersiz beslenmenin sonucudur ve geri döndürülemez nörobilişsel/boy kayıplarını önlemek için müdahale gebelikten 2 yaş sonuna kadar olan ilk 1000 günde yapılmalıdır."
                },
                {
                    "text": "İlkokul Çağı (7-11 yaş arası)",
                    "isCorrect": False,
                    "feedback": "Hatalı: Okul çağında kemik epifizleri ve nöronal sinapslar büyük oranda oturmuştur; ilk 1000 gündeki bodurluk hasarı okul çağında telafi edilemez."
                },
                {
                    "text": "Ergenlik Dönemi (12-18 yaş arası)",
                    "isCorrect": False,
                    "feedback": "Hatalı: Ergenlik büyüme atağı sağlasa da ilk 1000 gündeki bilişsel gerilik ve boy potansiyeli kaybı düzeltilemez."
                }
            ]
        ),
        5: make_branching_logic(
            "Birinci basamak sağlık ocağında bir hekim, bir mahallede bebek ölüm hızının (BÖH) binde 45 olduğunu tespit ediyor. Bölgede kanalizasyon altyapısı yetersiz ve formül mama kullanımı yaygın.",
            "Bu bölgede bebek ölümlerini en hızlı ve en etkili şekilde düşürmek için atılması gereken birinci basamak önlem hangisidir?",
            [
                {
                    "text": "Tüm annelere temiz içme suyu güvencesiyle birlikte ilk 6 ay sadece anne sütü verilmesini ve emzirmenin korunmasını zorunlu eğitim ve izlemle yaygınlaştırmak",
                    "isCorrect": True,
                    "feedback": "Doğru Halk Sağlığı Müdahalesi: Kötü sanitasyon koşullarında formül mama hazırlamak ölümcül ishale yol açar; tek başına anne sütü enfeksiyon ilişkili ölümleri %80'e varan oranda engeller."
                },
                {
                    "text": "Tüm bebeklere doğar doğmaz geniş spektrumlu profilaktik antibiyotik başlamak",
                    "isCorrect": False,
                    "feedback": "Hatalı ve Tehlikeli: Profilaktik antibiyotik dirençli mikropları ve nekrotizan enterokoliti patlatır; koruma temiz anne sütüyle sağlanır."
                },
                {
                    "text": "Bölgeye ücretsiz biberon ve kaynatılmış inek sütü dağıtmak",
                    "isCorrect": False,
                    "feedback": "Hatalı: 1 yaş altı inek sütü mikrokanama ve anemi yapar; biberon ölümcül gastroenterite davetiye çıkarır."
                }
            ]
        ),
        11: make_branching_logic(
            "Doğum ağırlığı 3200 gram olan bir term bebek, 5. gün poliklinik kontrolüne getiriliyor. Tartıda bebeğin ağırlığı 3000 gram (%6.25 kayıp) ölçülüyor. Bebek aktif emiyor, hidrasyonu iyi.",
            "Bu kilo kaybı karşısında hekimin sergilemesi gereken en uygun pediatrik tutum hangisidir?",
            [
                {
                    "text": "Bu kaybın fizyolojik tartı kaybı olduğunu aileye açıklamak, anneye emzirmeye aynı sıklıkta devam etmesini söylemek ve 10-14. günde doğum ağırlığına ulaşacağını belirtmek",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik Değerlendirme: İlk günlerde hücre dışı sıvının atılmasıyla %7-10'a kadar kilo kaybı tamamen fizyolojiktir; bebek 10-14. günlerde doğum kilosunu yakalar."
                },
                {
                    "text": "Sütün yetmediğine karar verip bebeğe derhal günde 6 kez formül mama takviyesi başlamak",
                    "isCorrect": False,
                    "feedback": "Hatalı: Gereksiz mama takviyesi anne memesinin uyarılmasını azaltarak laktasyonu söndürür."
                },
                {
                    "text": "Bebeği dehidratasyon şüphesiyle acil yenidoğan yoğun bakım ünitesine yatırmak",
                    "isCorrect": False,
                    "feedback": "Hatalı: %6 kilo kaybı stabildir, acil yatış endikasyonu değildir."
                }
            ]
        ),
        15: make_branching_logic(
            "Doğumdan sonraki 2. günde olan bir anne, göğüslerinden yalnızca birkaç damla sarımsı koyu sıvı geldiğini, bebeğin doymadığını ve açlıktan ağladığını belirterek eczaneden hazır mama alıp vermek istediğini söylüyor.",
            "Hekim olarak anneye verilecek en doğru fizyolojik ve bilimsel yanıt hangisidir?",
            [
                {
                    "text": "Bu sıvının kolostrum olduğunu, 2 günlük bebeğin midesinin yalnızca bir kiraz/ceviz büyüklüğünde (10-20 ml) olduğunu ve bu birkaç damlanın hem doyurmaya hem de enfeksiyonlardan korumaya fazlasıyla yettiğini anlatmak",
                    "isCorrect": True,
                    "feedback": "Klinik Yaklaşım Kusursuz: Yenidoğan mide kapasitesi ilk günlerde 10-20 ml'dir; kolostrumun az hacmi minik mide için tam tasarlanmıştır, mama kesinlikle gerekmez."
                },
                {
                    "text": "Haklı olduğunu, sütünün henüz gelmediğini onaylayarak biberonla 60 ml formül mama vermesini söylemek",
                    "isCorrect": False,
                    "feedback": "Hatalı ve Zararlı: 60 ml mama minik mideyi aşırı gerer, kusmaya yol açar ve anne memesini bıraktırır."
                },
                {
                    "text": "Bebeğin susuz kalmaması için emzirme aralarında şekerli serum suyu içirmesini önermek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Şekerli su verilmesi yasaktır; hiponatremi ve enfeksiyon riski yaratır."
                }
            ]
        ),
        22: make_branching_logic(
            "Sezaryen doğum sonrası genel anestezi alan bir annenin ailesi, annenin narkozdan henüz tam uyanmadığını belirterek bebeğe ilk kaka çıkana kadar hazır mama vermeyi teklif ediyor.",
            "Doğum salonu hekimi olarak bebeğin beslenmesiyle ilgili verilecek en doğru talimat hangisidir?",
            [
                {
                    "text": "Bebeğe mama verilmemeli; anne uyanır uyanmaz ilk 30-60 dakikada ten tene temasla memeye tutulmalı ve ilk besin mutlaka kolostrum olmalıdır",
                    "isCorrect": True,
                    "feedback": "Doğru Karar: Sezaryen sonrasında da öncelik ilk 1 saatte kolostrumla buluşmaktır; mama verilmesi prelakteal beslenme hatasıdır."
                },
                {
                    "text": "Anne tam olarak ayağa kalkana kadar bebeğin 24 saat aç bekletilmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Uzun süreli açlık hipoglisemi ve hipotermi riskini artırır."
                },
                {
                    "text": "İlk besin olarak biberonla kaynatılmış papatya çayı içirilmesi",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bitki çayları yenidoğanda toksik reaksiyonlara ve nöbetlere yol açabilir."
                }
            ]
        ),
        26: make_branching_logic(
            "Polikliniğe getirilen 3 haftalık bebeğin annesi, 'sütüm yetmiyor' endişesiyle başvuruyor. Muayenede bebeğin günde 6-8 kez açık renkli bol idrar yaptığı, günde 3 kez altın sarısı pürtüklü kaka yaptığı ve haftalık 220 gram tartı aldığı saptanıyor.",
            "Bu hekimin vereceği en doğru klinik geri bildirim hangisidir?",
            [
                {
                    "text": "Günde 6'dan fazla ıslak bez ve haftalık >150-200 gram tartı artışının anne sütünün mükemmel yettiğinin nesnel kanıtı olduğunu belirterek anneyi rahatlatmak ve emzirmeye devam ettirmek",
                    "isCorrect": True,
                    "feedback": "Klinik Yargı Tam İsabet: Süt yeterliliğinin altın standart göstergesi tartı artışı ve günde en az 6 kez açık renkli idrardır; anne endişesi subjektiftir."
                },
                {
                    "text": "Annenin memesini sağdırarak çıkan mililitreye göre sütün yetersiz olduğunu tescilleyip mama eklemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Pompayla sağılan miktar bebeğin emiş gücünü yansıtmaz; gereksiz mama başlatır."
                },
                {
                    "text": "Bebeğin midesini genişletmek için akşamları pirinç unlu mama başlamak",
                    "isCorrect": False,
                    "feedback": "Hatalı: 3 haftalık bebeğe pirinç unu verilmesi aspirasyon ve sindirim felci yapar."
                }
            ]
        ),
        33: make_branching_logic(
            "Doğumdan sonraki ilk haftada olan bir anne, bebeğin memeyi her emişinde alt karnında ağrılı kasılmalar ve adet sancısı benzeri kramplar hissettiğini söyleyerek korkuyla başvuruyor.",
            "Bu durumun fizyopatolojik mekanizması ve anneye verilecek bilgi hangisidir?",
            [
                {
                    "text": "Emme uyarısıyla salgılanan oksitosin hormonunun aynı zamanda uterus kasını da sıkarak doğum sonu kanamayı önlediğini ve rahmi hızla küçülttüğünü belirterek bunun son derece sağlıklı bir fizyolojik süreç olduğunu açıklamak",
                    "isCorrect": True,
                    "feedback": "Doğru Endokrinolojik Yaklaşım: Oksitosin hem miyoepitelyal hücreleri sıkarak sütü fışkırtır hem de miyometriyumu kasarak hemostaz ve uterus involüsyonu sağlar."
                },
                {
                    "text": "Rahimde enfeksiyon (endometrit) geliştiğini söyleyerek emzirmeyi acilen durdurmak",
                    "isCorrect": False,
                    "feedback": "Hatalı: Ateş ve kötü kokulu akıntı yoksa bu kramp oksitosine bağlı normal involüsyon sancısıdır."
                },
                {
                    "text": "Kasılmaların bebeğin sütü sindiremediğinin işareti olduğunu söyleyip mamaya geçmek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Uterus krampları anne hormonlarıyla ilgilidir, bebeğin sindirimiyle ilgisi yoktur."
                }
            ]
        ),
        36: make_branching_logic(
            "Çok stresli bir doğum süreci geçiren ve kayınvalidesiyle tartışan bir annenin, sütü gelmesine rağmen bebeğe memeyi verdiğinde sütün akmadığını fark ediliyor. Anne 'sütüm bitti' diye ağlıyor.",
            "Bu vakada süt akımının durmasının nörohumoral mekanizması ve ilk yapılması gereken nedir?",
            [
                {
                    "text": "Aşırı stres ve sempatik aktivitenin (adrenalin/noradrenalin) oksitosin refleksini geçici olarak bloke ettiğini bilmek; anneyi sakin, loş ve destekleyici bir ortama alarak tensel temasla oksitosin akışını yeniden tetiklemek",
                    "isCorrect": True,
                    "feedback": "Mükemmel Psikofizyolojik Yönetim: Oksitosin stresi sevmez; prolaktin sütü üretmiştir ancak sempatik vazokonstrüksiyon süt inme refleksini engeller; huzurlu ortam sütü derhal akıtır."
                },
                {
                    "text": "Sütün geri dönüşümsüz olarak bittiğini kabul edip bebeğe ömür boyu formül mama yazmak",
                    "isCorrect": False,
                    "feedback": "Hatalı: Süt bitmemiştir, sadece akış geçici bloke olmuştur."
                },
                {
                    "text": "Anneye acil prolaktin artırıcı ilaçlar yüklemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Sorun süt yapımı (prolaktin) değil, süt akıtımı (oksitosin) blokajıdır."
                }
            ]
        ),
        44: make_branching_logic(
            "Viral gastroenterit salgını olan bir kreşte çalışan emziren bir anne, kendisinde sulu ishal ve hafif ateş başladığını belirterek 'bebeğime mikrop geçmesin diye emzirmeyi bırakayım mı?' diye soruyor.",
            "Hekimin bu anneye vermesi gereken en kritik halk sağlığı ve immünoloji tavsiyesi hangisidir?",
            [
                {
                    "text": "Emzirmeye kesinlikle ve daha sık aralıklarla devam etmelidir; çünkü annenin bağışıklık sistemi virüse karşı spesifik sekretuvar IgA üretip sütle bebeğe aktararak onu hastalanmaktan korur",
                    "isCorrect": True,
                    "feedback": "Doğru İmmünolojik Karar: Enteromammarik yolak sayesinde anne bağırsağındaki lenfositler memeye göç eder ve bebeğe o virüse özel antikor zırhı sunar; emzirmeyi kesmek bebeği savunmasız bırakır."
                },
                {
                    "text": "İshal tamamen düzelene kadar 10 gün boyunca sütünü sağıp lavaboya dökmesini söylemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Anne sütü değerlidir, lavaboya dökülmez ve bebeğin en güçlü ilacıdır."
                },
                {
                    "text": "Anneye antibiyotik verip bebeğe pastörize inek sütü başlamak",
                    "isCorrect": False,
                    "feedback": "Hatalı: Viral ishalde antibiyotik etkisizdir, 1 yaş altı inek sütü kesin yasaktır."
                }
            ]
        ),
        53: make_branching_logic(
            "Emziren bir anne bebeğinin 10 günlük olduğunu, emzirirken ilk gelen sütün sulu ve renksiz olduğunu, sonlara doğru sütün beyaz ve kremamsı olduğunu fark ettiğini söylüyor. İlk gelen sulu sütü bebeğe içirmeyip sağarak attığını belirtiyor.",
            "Bu annenin uygulamasına yönelik hekimin açıklaması ne olmalıdır?",
            [
                {
                    "text": "Ön sütün laktoz ve su zengini olup susuzluğu giderdiğini, son sütün ise yağ zengini olup tokluk sağladığını; her iki sütün de bebeğin dengeli beslenmesi için zorunlu olduğunu anlatıp sağarak atmayı derhal yasaklamak",
                    "isCorrect": True,
                    "feedback": "Doğru Beslenme İlkesi: Ön süt susuzluğu giderir ve beyin gelişimini destekler, son süt kalori ve tokluk verir. Memenin tek taraflı tam boşaltılması her iki fraksiyonun alınmasını sağlar."
                },
                {
                    "text": "Ön sütün sadece su olduğunu onaylayarak atmaya devam etmesini ve yalnızca son sütü emzirmesini önermek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Ön süt atılırsa bebek susuz kalır ve laktozun beyin gelişimindeki faydasından mahrum olur."
                },
                {
                    "text": "Ön sütün gaz yaptığını belirterek içine karbonat katmasını tavsiye etmek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Anne sütüne hiçbir yabancı madde katılamaz."
                }
            ]
        ),
        57: make_branching_logic(
            "Aile hekimliği birimine başvuran bir anne adayı, doğumdan sonra bebeğini emzirmek istemediğini, formül mamanın daha modern olduğunu ve emzirmenin kendisini yıpratacağını söylüyor.",
            "Hekimin anneyi ikna ederken vurgulayabileceği emzirmenin ANNEYE sağladığı uzun vadeli onkolojik fayda hangisidir?",
            [
                {
                    "text": "Emzirmenin meme ve over (yumurtalık) kanseri riskini belirgin oranda azalttığını, kümülatif emzirilen her 12 ayın meme kanseri riskini %4.3 düşürdüğünü anlatmak",
                    "isCorrect": True,
                    "feedback": "Kanıta Dayalı Onkolojik Bilgi: Emzirme meme epitelinin terminal diferansiyasyonunu sağlar ve ovulatuar siklusları baskılayarak hem over hem meme kanserine karşı güçlü koruma kalkanı sunar."
                },
                {
                    "text": "Emzirmenin annenin boyunu uzattığını ve saç dökülmesini tamamen durdurduğunu söylemek",
                    "isCorrect": False,
                    "feedback": "Tıbben asılsızdır; emzirme boy uzatmaz."
                },
                {
                    "text": "Emzirmeyen tüm kadınlarda kesinlikle diyabet gelişeceğini söyleyerek korkutmak",
                    "isCorrect": False,
                    "feedback": "Hatalı iletişim; risk azalır ancak kesin hastalık tehdidi etik dışıdır."
                }
            ]
        ),
        63: make_branching_logic(
            "Bir eczacı, formül mama hazırlarken kutunun üzerinde 'Taurin ilaveli' yazdığını görüyor ve bir hekime inek sütü bazlı mamalara neden ekstra taurin katıldığını soruyor.",
            "Bu pediatrik biyokimyasal sorunun doğru bilimsel cevabı hangisidir?",
            [
                {
                    "text": "İnek sütünde taurin çok azdır ve yenidoğanda sistationaz enzimi immatür olduğundan taurin sentezlenemez; retina ve beyin gelişimi için mamalara eklenmesi zorunludur",
                    "isCorrect": True,
                    "feedback": "Doğru Biyokimyasal Gerekçe: Anne sütünde serbest taurin inek sütünün 30-40 katıdır; endojen sentez immatür olduğundan formül mamalar taurin ile zenginleştirilmek zorundadır."
                },
                {
                    "text": "Taurinin mamanın raf ömrünü 5 yıl uzatan bir koruyucu kimyasal olması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Taurin koruyucu katkı maddesi değil, retina ve santral sinir sistemi için şartlı esansiyel amino asittir."
                },
                {
                    "text": "Taurinin inek sütündeki laktozu tamamen parçalayarak şekeri sıfırlaması",
                    "isCorrect": False,
                    "feedback": "Hatalı: Taurin amino asittir, laktaz enzimi değildir."
                }
            ]
        ),
        72: make_branching_logic(
            "Yeni doğum yapmış bir lohusa, bebeği her emzirdiğinde meme uçlarında kanamalı çatlaklar oluştuğunu söylüyor. Gözlemde bebeğin yalnızca meme ucunu ağzına aldığı, areolayı kavramadığı ve çenesinin memeden uzakta olduğu görülüyor.",
            "Bu annenin meme başı çatlağını iyileştirecek ve tekrarlamasını önleyecek en etkili girişim hangisidir?",
            [
                {
                    "text": "Bebeğin ağzını geniş açtırarak areolanın alt kısmını tamamen ağza almasını ve alt dudağın dışa kıvrılarak kavramasını sağlamak",
                    "isCorrect": True,
                    "feedback": "Doğru Mekanik Çözüm: Meme başı çatlakları mekanik sürtünme ve ezilmeden kaynaklanır; areola kavranınca meme ucu bebeğin yumuşak damağında güvende kalır ve acı anında biter."
                },
                {
                    "text": "Meme ucuna her emzirmeden önce alkol ve antibiyotikli merhem sürüp silmeden emzirtmek",
                    "isCorrect": False,
                    "feedback": "Hatalı ve Tehlikeli: Alkol cildi çatlatır, antibiyotik bebek tarafından yutulmamalıdır."
                },
                {
                    "text": "Emzirmeye 2 hafta ara verip bebeği biberonla beslemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Biberon meme başı şaşkınlığı yapar ve anne sütünü keser."
                }
            ]
        ),
        76: make_branching_logic(
            "Çalışan bir anne sabah 08:00'de sağdığı anne sütünü oda sıcaklığında (24 °C) unuttuğunu, saat 10:30'da fark ettiğini söylüyor. 'Bu süt bozulmuş mudur, bebeğe verebilir miyim?' diye danışıyor.",
            "Anne sütü saklama kılavuzlarına göre bu soruya verilecek en doğru yanıt hangisidir?",
            [
                {
                    "text": "Anne sütü temiz koşullarda sağıldıysa oda ısısında 3 saat güvenle bekleyebilir; 2.5 saat geçtiği için bu süt bebeğe güvenle içirilebilir",
                    "isCorrect": True,
                    "feedback": "Kurala Uygun Yanıt: 3-3-3 kuralına göre oda ısısında (22-26 °C) sağılmış süt 3 saat bozulmadan dayanır; 2.5 saatlik süt güvenlidir."
                },
                {
                    "text": "Oda ısısında kalan süt 15 dakikada zehire dönüşür, derhal dökülmelidir",
                    "isCorrect": False,
                    "feedback": "Hatalı: Anne sütündeki lizozim ve laktoferrin bakteriyel üremeyi saatlerce engeller."
                },
                {
                    "text": "Sütü tencerede kaynattıktan sonra buzdolabına kaldırmasını söylemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Kaynatma antikorları denatüre eder; oda ısısındaki süte kaynatma uygulanmaz."
                }
            ]
        ),
        83: make_branching_logic(
            "3.5 aylık bir bebeğin annesi, komşusunun tavsiyesiyle bebeğin daha çabuk büyümesi ve gece deliksiz uyuması için akşamları pirinç unlu muhallebi vermeye başladığını söylüyor.",
            "Pediatrist olarak bu uygulamaya karşı aileye açıklanması gereken en temel tıbbi sakınca hangisidir?",
            [
                {
                    "text": "4 aydan önce bağırsak bariyerinin açık olması nedeniyle gıda alerjilerinin tetiklenmesi, amilaz yetersizliği ve ekstrüzyon refleksi nedeniyle boğulma riski",
                    "isCorrect": True,
                    "feedback": "Eksiksiz Pediatrik Bilgi: 6 aydan (en erken 17 haftadan) önce katı besin verilmesi hem aspirasyona hem de immünolojik alerji fırtınasına yol açar."
                },
                {
                    "text": "Pirinç ununun bebeğin kemiklerini eriterek boyunu kısaltması",
                    "isCorrect": False,
                    "feedback": "Tıbben anlamsızdır; kemik erimesi yapmaz."
                },
                {
                    "text": "Muhallebinin bebeğin dişlerinin dökülmesine yol açması",
                    "isCorrect": False,
                    "feedback": "Hatalı: 3.5 aylık bebekte henüz süt dişleri sürmemiştir."
                }
            ]
        ),
        88: make_branching_logic(
            "10 aylık bir bebeğe ailesi öksürüğü geçsin diye bir kaşık kestane balı yedirmiştir. Bebek 1 gün sonra emememe, ağlarken ses çıkaramama, başını tutamama ve kabızlık şikayetiyle acile getiriliyor.",
            "Bu klinik tabloda hekimin acilen şüphelenmesi gereken tablo ve yapması gereken nedir?",
            [
                {
                    "text": "İnfantil Botulizm: Clostridium botulinum spor toksininin nöromüsküler kavşakta asetilkolini bloke etmesi; acil yoğun bakım ve Botulizm İmmünglobulin tedavisi",
                    "isCorrect": True,
                    "feedback": "Hayati Doğru Teşhis: 1 yaş altı bal tüketimi infantil botulizmin başlıca sebebidir; kabızlık ve flask paralizi klasik bulgudur."
                },
                {
                    "text": "Basit boğaz enfeksiyonu: antibiyotik şurup yazıp eve göndermek",
                    "isCorrect": False,
                    "feedback": "Ölümcül Hata: Hasta hipotoniktir ve solunum arrestine girebilir, acil yatış gerekir."
                },
                {
                    "text": "Laktoz intoleransı: süt ürünlerini kesmesini söylemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Bal yedikten sonra gelişen flask paralizinin laktozla ilgisi yoktur."
                }
            ]
        ),
        92: make_branching_logic(
            "Ağır yoksulluk bölgesinde yaşayan 9 aylık bir bebek muayene ediliyor. Cilt altı yağ dokusu tamamen erimiş, kasları atrofiye uğramış, kaburgaları sayılıyor ve yüzü 80 yaşında bir ihtiyar görünümünde. Ancak bacaklarında ve göz kapaklarında ödem saptanmıyor.",
            "Bu hastadaki protein-enerji malnütrisyonu tipi ve ödem olmamasının biyolojik açıklaması nedir?",
            [
                {
                    "text": "Marasmus: Ağır genel kalori açlığı mevcuttur; karaciğer albümin sentezini bir dereceye kadar koruyabildiği için onkotik basınç çökmemiştir ve ödem yoktur",
                    "isCorrect": True,
                    "feedback": "Klinik Ayırıcı Tanı Kusursuz: Marasmusta kalori açlığı vardır, doku erir ama ödem görülmez; ödem Kvaşiorkor'un kardinal bulgusudur."
                },
                {
                    "text": "Kvaşiorkor: Saf karbonhidrat fazlalığına bağlı gelişen tablo",
                    "isCorrect": False,
                    "feedback": "Hatalı: Kvaşiorkor'da gode bırakan yaygın ödem ve karaciğer büyümesi zorunludur."
                },
                {
                    "text": "D Vitamini İntoksikasyonu",
                    "isCorrect": False,
                    "feedback": "Hatalı: İntoksikasyon kaşeksi ve faun yüzü yapmaz."
                }
            ]
        ),
        94: make_branching_logic(
            "Ağır akut malnütrisyon (SAM) nedeniyle hastaneye yatırılan aşırı zayıf bir çocuğa nöbetçi asistan hemen bol şekerli yüksek kalorili mama ve intravenöz demir infüzyonu başlatmak istiyor.",
            "Kıdemli pediatristin bu uygulamayı derhal durdurmasının ve F-75 formülüne geçmesinin hayati gerekçesi nedir?",
            [
                {
                    "text": "Hızlı karbonhidrat yüklemesinin ölümcül Hipofosfatemi (Refeeding Sendromu) ve kardiyak arreste; erken serbest demirin ise sepsis patlamasına yol açma riski",
                    "isCorrect": True,
                    "feedback": "Hayat Kurtaran Tıbbi Müdahale: Malnütrisyonda ani besleme insülin patlamasıyla fosfatı hücreye çeker ve kalbi durdurur; demir ise serbest radikal ve sepsis yapar."
                },
                {
                    "text": "Mamaların pahalı olması ve hastane bütçesini aşması",
                    "isCorrect": False,
                    "feedback": "Tıbbi gerekçe değildir; sebep biyokimyasal refeeding sendromu riskidir."
                },
                {
                    "text": "Çocuğun şekere alışıp normal yemekleri reddetme ihtimali",
                    "isCorrect": False,
                    "feedback": "Yetersiz ve önemsiz gerekçe; acil tehdit kardiyak arrest ve ölümcül sepsistir."
                }
            ]
        ),
        96: make_branching_logic(
            "7 aylık bebeğine Bebek Öncülüğünde Beslenme (BLW) uygulayan bir anne, bebeğin haşlanmış brokoliyi ağzına götürdüğünde birden sesli olarak öksürdüğünü, yüzünün kızardığını ve hafifçe öğürerek parçayı ağzından dışarı attığını söylüyor. Anne paniğe kapılarak bir daha katı gıda vermekten korktuğunu belirtiyor.",
            "Hekimin bu anneye gagging (öğürme) ile choking (boğulma) ayrımını anlatırken yapacağı en doğru açıklama hangisidir?",
            [
                {
                    "text": "Sesli öksürme ve öğürmenin (gagging) hava yolunun açık olduğunu gösteren koruyucu bir refleks olduğunu; ölümcül boğulmanın (choking) ise sessiz, morarmayla seyrettiğini ve sakin kalıp bebeğin dik oturmasına izin vermesi gerektiğini anlatmak",
                    "isCorrect": True,
                    "feedback": "Mükemmel Danışmanlık: Öğürme dili ve yutma refleksini eğiten koruyucu bir mekanizmadır; ses varsa hava yolu açıktır, müdahale edilmez."
                },
                {
                    "text": "Bebeğin ölümden döndüğünü ve acilen tüm besinleri mikserde un haline getirip biberonla vermesini söylemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Anneye gereksiz anksiyete yükler ve çiğneme eğitimini baltalar."
                },
                {
                    "text": "Öğüren her bebeğe derhal parmakla boğazına müdahale edip sırtına sertçe vurmasını tembihlemek",
                    "isCorrect": False,
                    "feedback": "Tehlikeli Hata: Körlemesine parmak sokmak güvenli parçayı trakeaya itip gerçek boğulmaya sebep olabilir."
                }
            ]
        ),
        97: make_branching_logic(
            "18 aylık bir çocuk annesi tarafından iştahsızlık, halsizlik ve toprak yeme (pika) şikayetiyle getiriliyor. Hikayede çocuğun yemek yemediği için annesinin günde yaklaşık 1.5 litre inek sütü içirdiği öğreniliyor. Hemoglobin 6.8 g/dl, MCV 62 fl bulunuyor.",
            "Bu tablonun tanı ve tedavisiyle ilgili en doğru klinik yönetim hangisidir?",
            [
                {
                    "text": "Tanı Süt Anemisidir (Ağır Demir Eksikliği): Günlük inek sütü maksimum 400-500 ml ile sınırlandırılmalı, demir tedavisi başlanmalı ve aile sofrasından et/sebze takviyesi yapılmalıdır",
                    "isCorrect": True,
                    "feedback": "Doğru Klinik Yönetim: Günde 1.5 litre inek sütü kalsiyum yarışmasıyla demir emilimini felç eder ve tokluk yaparak et tüketimini engeller; süt kısıtlanmadan anemi düzelmez."
                },
                {
                    "text": "Süt miktarını günde 2.5 litreye çıkararak kalori desteği sağlamak",
                    "isCorrect": False,
                    "feedback": "Ölümcül Hata: Anemiyi ve iştahsızlığı daha da derinleştirir."
                },
                {
                    "text": "İnek sütünü kesip yerine hazır meyve suyu ve gazlı içecekler vermek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Şekerli içecekler besleyici değildir, anemiyi düzeltmez."
                }
            ]
        ),
        99: make_branching_logic(
            "Sağlık ocağına aşıya gelen 4 aylık sağlıklı bir term bebeğin annesi, 'Bebeğimin hiçbir şikayeti yok, kan tahlili de temiz çıktı, neden her gün demir damlası vermek zorundayım?' diye soruyor.",
            "Sağlık Bakanlığı 'Demir Gibi Türkiye' projesi kapsamında hekimin vereceği kanıta dayalı profilaksi cevabı hangisidir?",
            [
                {
                    "text": "Term doğan bebeklerde anne karnında biriken karaciğer demir depolarının 4-6. aylarda fizyolojik olarak tükendiğini, anemi klinik olarak oturmadan önce profilaktik koruma sağlamak için tahlil beklenmeksizin başlandığını açıklamak",
                    "isCorrect": True,
                    "feedback": "Kusursuz Halk Sağlığı Bilinci: Profilaksi hastalık çıkmadan önce önlemektir; fetal depolar 4. ayda erir, bu yüzden rutin profilaktik demir başlanır."
                },
                {
                    "text": "Haklı olduğunu söyleyip kan tahlili bozulana kadar ilacı vermemesini önermek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Demir eksikliği kan tahlilinde anemi yapmadan önce beyin gelişimini bozar; beklemek yanlıştır."
                },
                {
                    "text": "Demir damlası yerine her gün bebeğe bir çay kaşığı pekmez içirmesini söylemek",
                    "isCorrect": False,
                    "feedback": "Hatalı: Pekmezdeki demir biyoyararlanımı düşüktür ve bebek böbreği için yüksek şeker yükü taşır."
                }
            ]
        )
    }

def get_extra_sliders():
    """Before/after slider (fizyolojik ve biyokimyasal karşılaştırma) ögeleri."""
    return {
        7: make_before_after(
            "Emzirme ile Biberonla Beslemenin Ağız ve Çene Gelişimine Etkisi",
            "Biberonla Besleme",
            "Bebek pasif emiş yapar; yapay kauçuk uç çene kemiğini daraltır, damak kubbesini yükseltir ve ileride diş çapraşıklığı (maloklüzyon) ile horlamaya zemin hazırlar.",
            "Anne Memesinden Emzirme",
            "Bebek areolayı kavrayıp dil ve masseter kaslarıyla güçlü peristaltik dalga üretir; çene arkı genişler, diş dizilimi düzgün gelişir ve konuşma kasları güçlenir.",
            "Ağız-diş sağlığı ve kraniyofasiyal anatomi karşılaştırması"
        ),
        17: make_before_after(
            "Mide Boşalma Dinamikleri: Anne Sütü vs Formül Mama",
            "Formül Mama Alımı",
            "Midede kaba ve sert pıhtılar oluşturur; gastrik boşalma üç buçuk-dört saati bulur, reflü ve kolik ağrılarına yol açar.",
            "Anne Sütü Alımı",
            "Yüksek whey oranı sayesinde yumuşak ve ince mikropıhtılar oluşturur; mide fizyolojik olarak doksan dakikada tamamen boşalır.",
            "Gastrik motilite ve boşalma süreleri karşılaştırması"
        ),
        25: make_before_after(
            "Laktasyon Evreleri: Kolostrum vs Olgun Süt",
            "Kolostrum (İlk 5 Gün)",
            "Protein, sIgA, çinko ve A vitamininden zengin, düşük yağ ve laktozlu, yoğun sarı renkli doğal aşı kıvamındadır.",
            "Olgun Süt (15. Günden Sonra)",
            "Yağ ve laktoz konsantrasyonu artmış, protein oranı dengelenmiş, bebeğin hızlı kilo alımını ve enerjisini sağlayan dengeli besindir.",
            "Sütün evreler arası biyokimyasal dönüşümü"
        ),
        35: make_before_after(
            "Meme İçi Düzenleme: Boş Meme vs Dolu Meme Hormon Yanıtı",
            "Dolu ve Gergin Meme",
            "Alveollerde süt birikir; Geri Bildirimli Laktasyon İnhibitörü (FIL) proteini birikerek alveolar hücrelere süt üretimini durdurma sinyali gönderir.",
            "Sık Emzirilen Boş Meme",
            "Meme tamamen boşaltıldığında FIL baskısı kalkar; prolaktin reseptörleri duyarlılaşır ve epitelyal hücreler hızla yeni süt sentezlemeye başlar.",
            "FIL mekanizması ve süt yapım hızı kontrolü"
        ),
        43: make_before_after(
            "Bağırsak Mikrobiyotası: Anne Sütü vs Mama ile Beslenen Bebek",
            "Formül Mama ile Beslenme",
            "Bağırsak pH'sı daha alkalidir; E. coli, Clostridium ve Bacteroides türleri florada baskın hale gelerek enfeksiyon riskini artırır.",
            "Anne Sütü ile Beslenme",
            "Laktoz ve oligosakkaritler (HMO) sayesinde bağırsak asidiktir; koruyucu Bifidobacterium ve Lactobacillus türleri floranın yüzde doksanını oluşturur.",
            "Bağırsak lümen florası ve pH dengesi karşılaştırması"
        ),
        55: make_before_after(
            "Prematüre Anne Sütü vs Term Anne Sütü Bileşimi",
            "Term Doğum Anne Sütü",
            "Matür organ sistemlerine uygun olarak standart protein (1 g/100 ml), dengeli sodyum ve yüksek laktoz içerir.",
            "Prematüre Doğum Anne Sütü",
            "Erken doğan bebeğin hızlı büyümesini desteklemek için belirgin yüksek protein, yüksek sodyum/klor ve daha düşük laktoz içerir.",
            "Gestasyonel yaşa göre sütün özelleşmiş tasarımı"
        ),
        65: make_before_after(
            "Mineral Yükü ve Böbrek: Anne Sütü vs İnek Sütü",
            "İnek Sütü Tüketimi",
            "Aşırı fosfor (6 kat) ve kalsiyum yükler; Ca/P oranı 1.2:1'dir; böbrekten atılamayan fosfor kanda kalsiyumu çöktürerek hipokalsemik tetani yapar.",
            "Anne Sütü Tüketimi",
            "Düşük mineral yükü ve ideal 2:1 Ca/P oranı içerir; böbrekleri yormadan kemik mineralizasyonunu mükemmel destekler.",
            "Mineral homeostazı ve renal tolerans karşılaştırması"
        ),
        75: make_before_after(
            "Emme Mekaniği: Anne Memesi vs Biberon Kauçuk Ucu",
            "Biberonla Emme Mekaniği",
            "Süt delikten kendiliğinden akar; bebek sadece diş etleriyle ucu sıkarak pasif emer, dilini geri çeker ve tembelleşir.",
            "Anne Memesinden Emme Mekaniği",
            "Bebek areolayı vakumlar, dilini areolanın altına serip damağıyla peristaltik dalga hareketi yaparak aktif süt sağar.",
            "Meme başı şaşkınlığının biomekanik arka planı"
        ),
        85: make_before_after(
            "Ek Gıdada Kıvam: Sulu Çorbalar vs Enerji Yoğun Püreler",
            "Sulu Süzme Çorbalar",
            "Yüzde doksanı sudur; bebeğin minik midesini sahte bir toklukla doldurur, kalori ve demir açığı yaratarak büyümeyi duraklatır.",
            "Çatalla Ezilmiş Zengin Püreler",
            "Az hacimde yüksek enerji, protein ve demir barındırır; mideyi suyla işgal etmeden gerçek besin gereksinimini karşılar.",
            "Besin dansitesi ve mide hacmi optimizasyonu"
        ),
        93: make_before_after(
            "Malnütrisyonda Ödem Durumu: Marasmus vs Kvaşiorkor",
            "Marasmus Tablosu",
            "Genel kalori açlığına bağlı tüm dokular erimiştir; albümin kısmen korunduğu için ödem kesinlikle bulunmaz.",
            "Kvaşiorkor Tablosu",
            "Saf protein yokluğuna bağlı karaciğer albümin yapamaz; onkotik basınç çöker ve tüm vücutta godet bırakan ödem gelişir.",
            "Onkotik basınç ve klinik ödem ayırıcı tanısı"
        ),
        95: make_before_after(
            "D Vitamini Düzeyi: Profilaksi Alan vs Almayan Bebek",
            "D Vitamini Almayan Bebek",
            "Güneş görmeyen ve profilaksi verilmeyen bebekte kalsiyum kemiğe çökelemez; kraniyotabes, raşitik tespih ve O-bacak gelişir.",
            "400 IU/Gün D Vitamini Alan Bebek",
            "Bağırsaktan kalsiyum ve fosfor emilimi tam gerçekleşir; kafatası kemikleri ve uzun kemikler sağlam ve düzgün mineralize olur.",
            "Raşitizm patolojisi ile profilaktik korunma tablosu"
        ),
        98: make_before_after(
            "İkinci Yaşta Beslenme: Anne Sütü Alan vs Almayan Çocuk",
            "Sütten Erken Kesilen Çocuk",
            "Enfeksiyon anında katı gıdayı reddedince hızla dehidratasyona ve akut kilo kaybına girer; hastane yatış riski artar.",
            "2 Yaşına Kadar Emzirilen Çocuk",
            "Gastroenterit veya pnömoni olsa bile memeyi emerek sıvı ve antikor desteğini sürdürür; hidrasyonu ve büyümesi korunur.",
            "Yaşamın 2. yılında laktasyonun koruyucu gücü"
        )
    }

def apply_enrichment(slides):
    """Slayt listesine ek interaktif ögeleri entegre eder."""
    extra_branching = get_extra_branching()
    extra_sliders = get_extra_sliders()

    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        if "elements" in slide:
            elements = slide["elements"]
        else:
            elements = slide.setdefault("interactiveElements", [])

        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_sliders:
            elements.append(extra_sliders[slide_num])

    return slides
