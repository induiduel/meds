# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 8: Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları (Slayt 71 - 80)
Checkpoint 8: Slayt 79
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # Slayt 71: Başarılı Emzirmenin İlk Adımı: İlk 30-60 Dakika ve Ten Tene Temas
    slides.append({
        "id": "k1-22-s71",
        "title": "Başarılı Emzirmenin İlk Adımı: İlk 30-60 Dakika ve Ten Tene Temas",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 71,
        "narrative": (
            "Başarılı bir laktasyon sürecinin en kritik penceresi **doğumdan sonraki ilk 30-60 dakikadır**. "
            "Normal spontan doğum veya anestezi sonrası genel durumu uygun sezaryen doğumlarda bebek kurulanır kurulanmaz, "
            "anne çıplak göğsü üzerine yüzükoyun yatırılarak **Ten Tene Temas (Skin-to-Skin Contact)** başlatılmalıdır. "
            "Bu temasın fizyolojik mucizeleri şunlardır: "
            "1. Anne ve bebekte **oksitosin patlaması** yaşanır; anksiyete yatışır, maternal bağlanma mühürlenir ve uterus kasılarak kanama önlenir. "
            "2. Yenidoğanın arama ve emme refleksleri doğum sonrası ilk 1 saatte en canlı haldedir; bebek meme başını kendiliğinden bulup kavrar. "
            "3. Hipotermi riski önlenir; annenin göğüs derisi sıcaklığı bebeğin vücut ısısına göre dinamik termoregülasyon sağlar. "
            "4. Bebek steril gastrointestinal sistemini hastane florasıyla değil, annenin koruyucu cilt mikrobiyotasıyla kolonize eder."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Doğumdan hemen sonra anne ile yenidoğan arasında kurulan ten tene temas oksitosin salgısını zirveye taşır ve ilk emzirmeyi başlatır.",
                "ten tene temas",
                "Çıplak tenlerin buluşmasıyla başlayan termal ve hormonal yakınlaşma"
            ),
            make_causal_chain(
                "Doğum Sonrası Erken Ten Tene Temasın Biyolojik Basamakları",
                [
                    "1. Termal ve Duyusal Uyarı: Yenidoğanın annenin göğsüne yatırılmasıyla cilt reseptörleri aktive olur.",
                    "2. Nöroendokrin Tetiklenme: Hipotalamustan supraoptik ve paraventriküler nükleuslar oksitosin boşaltır.",
                    "3. Miyometriyum ve Miyoeptelyal Yanıt: Uterus kasılarak hemostaz sağlanır; meme kanalları kolostrumu iletir.",
                    "4. Mikrobiyal Zırh: Bebeğin derisi ve mukozası annenin fizyolojik cilt mikroflorasıyla kolonize olur."
                ]
            ),
            make_micro_quiz(
                "Doğumdan hemen sonraki ilk 30-60 dakika içinde anne ile bebek arasında ten tene temasın başlatılmasının temel faydaları arasında hangisi yer almaz?",
                {
                    "A": "Maternal oksitosin salınımını uyararak doğum sonu uterus kanamasını azaltması",
                    "B": "Bebeğin vücut sıcaklığının dengelenmesini sağlayarak hipotermiyi önlemesi",
                    "C": "Bebeğin derisinin patojen hastane mikropları yerine annenin koruyucu florasıyla kolonize olması",
                    "D": "Bebeğe ilk besin olarak şekerli su verilerek hipogliseminin engellenmesi",
                    "E": "Anne-bebek duygusal bağlanmasını güçlendirerek emzirme süresini uzatması"
                },
                "D",
                {
                    "A": "Faydadır; Oksitosin uterusu katarak hemostazı hızlandırır.",
                    "B": "Faydadır; Anne cildi dinamik ısıtıcı görevi görür.",
                    "C": "Faydadır; Anne florası patojen kolonizasyonunu engeller.",
                    "D": "Hatalı Uygulamadır; Şekerli su veya serum verilmesi kesinlikle yasaktır, ilk besin kolostrum olmalıdır.",
                    "E": "Faydadır; Oksitosin maternal bağlanmayı mühürler."
                }
            )
        ]
    })

    # Slayt 72: Doğru Emzirme Tekniği, Pozisyon ve Meme Başı Çatlaklarının Önlenmesi
    slides.append({
        "id": "k1-22-s72",
        "title": "Doğru Emzirme Tekniği, Pozisyon ve Meme Başı Çatlaklarının Önlenmesi",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 72,
        "narrative": (
            "Başarısız emzirmenin ve erken bırakmanın en yaygın sebebi süt yetersizliği değil, **hatalı emzirme tekniğidir**. "
            "Doğru kavramanın (latch-on) altın kuralları şunlardır: "
            "1. **Geniş Açılmış Ağız:** Bebek ağzını esner gibi tam açmalıdır; sadece meme ucu değil, **areolanın (koyu halkanın) büyük kısmı ağza alınmalıdır**. "
            "Özellikle areolanın alt kısmı üst kısmına göre daha fazla ağız içinde olmalıdır. "
            "2. **Balık Ağzı:** Bebeğin **alt dudağı dışa doğru kıvrılmış (eversed)** olmalıdır; çene memeye sıkıca temas etmeli, burun delikleri açık kalmalıdır. "
            "3. **Yanaklar:** Emiş sırasında yanaklar içeri çökmemeli (çukurluk oluşmamalı), tam tersine dolgun ve yuvarlak durmalıdır. "
            "4. **Ağrı ve Çatlak İlkesi:** Emzirme acı vermemelidir! Eğer annenin canı yanıyorsa bebek yalnızca meme ucunu çiğniyor demektir. "
            "Meme başı çatlaklarının bir numaralı sebebi enfeksiyon değil, **hatalı tutuşa bağlı mekanik travmadır**."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Emzirme sırasında bebeğin alt dudağının dışa kıvrılmış olması ve areolanın büyük kısmını kavraması doğru tutuşun göstergesidir.",
                "alt dudağının dışa kıvrılmış",
                "Balık ağzı görünümünü oluşturan dudak pozisyonu"
            ),
            make_table(
                "Doğru Kavrama ile Yanlış Kavramanın Klinik Karşılaştırması",
                ["Kavrama Belirtisi", "Doğru Emzirme Pozisyonu", "Yanlış (Hatalı) Kavrama", "Klinik Yansıması"],
                [
                    ["Areola Tutuşu", "Areolanın çoğu ağızda (alttan geniş)", "Yalnızca meme ucu ağızda", "Meme başı çatlağı ve travma"],
                    [
                        "Dudak ve Çene",
                        {"text": "Alt dudak dışa kıvrık, çene memede", "isMasked": True, "hint": "Ağzın balık dudağı gibi dışa dönük açılması"},
                        "Dudaklar içe bükük, çene uzakta",
                        "Vakum kaybı ve hava yutma (gaz sancısı)"
                    ],
                    ["Yanak Yapısı", "Dolgun ve yuvarlak", "İçeri çökük (çukurlaşmış)", "Yetersiz süt akışı"],
                    ["Maternal His", "Ağrısız, rahat çekilme hissi", "Şiddetli acı ve batma hissi", "Emzirmeden kaçınma ve laktasyon durması"]
                ]
            ),
            make_branching_logic(
                "Doğumdan 4 gün sonra polikliniğe başvuran primipar bir anne, emzirirken meme ucunda dayanılmaz bir acı hissettiğini, "
                "meme uçlarının kızarıp çatladığını ve bu yüzden emzirmeyi bırakmak istediğini ifade ediyor. "
                "Muayenede bebeğin sadece meme ucunu ağzına aldığı, areolayı kavramadığı görülüyor.",
                "Hekim olarak bu annenin sorununu çözmek için atacağınız en öncelikli adım hangisidir?",
                [
                    {
                        "text": "Emzirmeyi derhal kesip formül mamaya geçmek ve meme ucuna kortizonlu krem yazmak",
                        "isCorrect": False,
                        "feedback": "Hatalı: Emzirmeyi kesmek gereksizdir ve laktasyonu sonlandırır. Sorun meme ucu değil, kavrama tekniğidir."
                    },
                    {
                        "text": "Anneye bebeğin ağzını genişçe açtırıp areolayı alttan kavratacak doğru emzirme pozisyonunu bizzat uygulamalı öğretmek",
                        "isCorrect": True,
                        "feedback": "Klinik Yaklaşım Mükemmel: Meme başı çatlaklarının temel sebebi hatalı kavramadır. Areola kavranınca meme ucundaki mekanik basınç sıfırlanır ve çatlak hızla iyileşir."
                    },
                    {
                        "text": "Bebeğe biberonla sağılmış süt verilmesini ve memenin 10 gün dinlendirilmesini önermek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Biberon verilmesi meme başı şaşkınlığına yol açarak bebeğin memeyi tamamen reddetmesine sebep olur."
                    }
                ]
            )
        ]
    })

    # Slayt 73: Bebek Dostu Hastane Girişimi (BDHG): 10 Adımda Başarılı Emzirme
    slides.append({
        "id": "k1-22-s73",
        "title": "Bebek Dostu Hastane Girişimi (BDHG): 10 Adımda Başarılı Emzirme",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 73,
        "narrative": (
            "DSÖ ve UNICEF tarafından 1991 yılında başlatılan ve ülkemizde Sağlık Bakanlığı tarafından titizlikle yürütülen "
            "**Bebek Dostu Hastane Girişimi (BDHG)**, emzirmeyi koruma, özendirme ve desteklemenin küresel rehberidir. "
            "Bu programın temel omurgasını oluşturan **10 Adımda Başarılı Emzirme** kurallarının kilit maddeleri şunlardır: "
            "1. Yazılı bir emzirme politikası oluşturulmalı ve tüm sağlık personeli düzenli eğitilmelidir. "
            "2. Tüm hamile kadınlara emzirmenin yararları ve yönetimi anlatılmalıdır. "
            "3. Doğumdan sonraki ilk yarım saat içinde emzirmeye başlanması için annelere yardım edilmelidir. "
            "4. Tıbbi bir zorunluluk olmadıkça **yenidoğana anne sütü dışında hiçbir yiyecek veya içecek (su, şekerli su, formül mama) verilmemelidir**. "
            "5. Anne ile bebeğin 24 saat aynı odada kalması (**Rooming-in**) sağlanmalıdır. "
            "6. Bebek her istedikçe emzirilmesi (**on-demand feeding**) teşvik edilmelidir. "
            "7. Emzirilen bebeklere **asla yalancı emzik veya biberon verilmemelidir**."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bebek Dostu Hastane Girişimi kapsamında tıbbi bir zorunluluk olmadıkça yenidoğana anne sütü dışında hiçbir sıvı verilmez.",
                "tıbbi bir zorunluluk olmadıkça",
                "Sadece kesin klinik endikasyonda mama verilmesine izin veren istisna kuralı"
            ),
            make_micro_quiz(
                "DSÖ ve UNICEF'in 'Bebek Dostu Hastane Girişimi (BDHG) - 10 Adımda Başarılı Emzirme' ilkelerine göre aşağıdakilerden hangisi doğrudan YASAKLANMIŞ bir uygulamadır?",
                {
                    "A": "Doğumdan sonraki ilk yarım saat içinde emzirmenin başlatılması",
                    "B": "Anne ile bebeğin 24 saat boyunca aynı odada birlikte kalması (rooming-in)",
                    "C": "Ağlayan veya huzursuzlanan bebekleri sakinleştirmek amacıyla yalancı emzik ve biberon verilmesi",
                    "D": "Bebeğin saat kısıtlaması olmaksızın her acıktığında emzirilmesinin teşvik edilmesi",
                    "E": "Tüm sağlık personeline düzenli emzirme eğitimi verilmesi"
                },
                "C",
                {
                    "A": "Kuraldır; İlk 30 dakikada emzirme teşvik edilir.",
                    "B": "Kuraldır; 24 saat oda birlikteliği (rooming-in) esastır.",
                    "C": "Doğrudan Yasaktır; BDHG ilkelerine göre biberon ve yalancı emzik kullanımı kesinlikle yasaklanmıştır.",
                    "D": "Kuraldır; İsteğe bağlı (on-demand) beslenme kuraldır.",
                    "E": "Kuraldır; Personel eğitimi ilk maddedir."
                }
            ),
            make_active_recall(
                "Bebek Dostu Hastane Girişimi ilkelerine göre doğumhanede rutin olarak uygulanan 'bebeğe ilk besin olarak şekerli serum verilmesi' pratiğinin tıbbi açıdan değerlendirmesi nedir?",
                "Kesinlikle yasak ve hatalı bir uygulamadır; tıbbi mutlak endikasyon olmadıkça anne sütü (kolostrum) dışında hiçbir sıvı verilemez.",
                "Gereksiz sıvı kısıtlaması ve kolostrum önceliği"
            )
        ]
    })

    # Slayt 74: Anne-Bebek Birlikteliği (Rooming-in) ve İsteğe Bağlı Emzirme
    slides.append({
        "id": "k1-22-s74",
        "title": "Anne-Bebek Birlikteliği (Rooming-in) ve İsteğe Bağlı Emzirme",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 74,
        "narrative": (
            "Geleneksel hastane düzenlerindeki 'bebek odası' kavramı modern tıpta terk edilmiştir; **Anne-Bebek Birlikteliği (Rooming-in)** esastır. "
            "Bebeğin doğumdan taburculuğa kadar 24 saat annesinin yanında kalması, annenin bebeğin erken açlık işaretlerini "
            "(kıpırdanma, ağzını açma, başını çevirme, elini ağzına götürme) hemen fark etmesini sağlar. "
            "Ağlama geç bir açlık belirtisidir; ağlayan bebeği memeye tutturmak zordur. "
            "Emzirme kesinlikle saatle sınırlandırılmamalı, **İsteğe Bağlı (On-Demand / Cue-based)** olmalıdır. "
            "Yenidoğan günde en az **8-12 kez** emzirilmelidir. "
            "Özellikle **gece emzirmeleri hayati öneme sahiptir**: Prolaktin hormonu sirkadiyen ritim gereği gece pik yapar; "
            "gece emziren annelerin toplam süt üretimi belirgin olarak daha yüksek ve laktasyon süreleri çok daha uzundur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Prolaktin hormonu sirkadiyen ritim gereği gece en yüksek seviyeye ulaştığı için gece emzirmeleri süt üretiminin devamında kritiktir.",
                "gece en yüksek seviyeye",
                "Karanlıkta ve uykuda tepe noktasına çıkan hormonal salınım"
            ),
            make_before_after(
                "Emzirme Rejimi: Saatli Besleme vs İsteğe Bağlı (On-Demand) Besleme",
                "Saatli Besleme (Üç Saatte Bir)",
                "Bebek katı 3 saatlik aralarla beslenir; erken açlık ipuçları kaçırılır, bebek ağlama krizine girer, gece emzirilmeyince prolaktin çöker ve süt hızla azalır.",
                "İsteğe Bağlı (On-Demand) Besleme",
                "Bebek her erken açlık işaretinde ve gece dahil günde sekiz-on iki kez emzirilir; prolaktin reseptörleri maksimum uyarılır ve süt üretimi tavan yapar."
            ),
            make_micro_quiz(
                "Başarılı emzirme sürecinde 'gece emzirmelerinin' aksatılmamasının en temel nöroendokrinolojik gerekçesi nedir?",
                {
                    "A": "Gece saatlerinde oksitosin hormonunun bebeğin idrar çıkışını azaltması",
                    "B": "Süt yapımını sağlayan prolaktin hormonunun gece saatlerinde tepe noktasına (pike) ulaşması",
                    "C": "Anne sütünün gece vakti kalorisinin gündüze göre yarı yarıya düşmesi",
                    "D": "Bebeğin gece sindirim enzimlerinin tamamen durması",
                    "E": "Gece emzirilmezse memede mastit gelişmesinin imkansız hale gelmesi"
                },
                "B",
                {
                    "A": "Yanlıştır; Oksitosin süt fışkırtma hormonudur, antidiüretik regülasyonla ilişkili değildir.",
                    "B": "Doğrudur; Prolaktin gece zirve yapar, bu yüzden gece emzirmesi bol süt yapımının garantisidir.",
                    "C": "Yanlıştır; Anne sütünün kalorisi düşmez, aksine melatonin içeriği artarak uykuya yardımcı olur.",
                    "D": "Yanlıştır; Sindirim enzimleri gece durmaz.",
                    "E": "Yanlıştır; Gece emzirilmezse süt kanalları tıkanır ve mastit riski artar."
                }
            )
        ]
    })

    # Slayt 75: Biberon ve Yalancı Emzik Tehlikesi: Meme Başı Şaşkınlığı
    slides.append({
        "id": "k1-22-s75",
        "title": "Biberon ve Yalancı Emzik Tehlikesi: Meme Başı Şaşkınlığı",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 75,
        "narrative": (
            "Yenidoğan ve küçük süt çocuklarına erken dönemde biberon veya yalancı emzik verilmesi emzirme başarısını sabote eden en büyük tuzaktır. "
            "Bu durum **'Meme Başı Şaşkınlığı' (Nipple Confusion)** tablosuna yol açar. "
            "Bunun anatomik ve fizyolojik mekanizması şöyledir: "
            "1. Anne memesinden süt sağmak aktif kas çalışması gerektirir; bebek dilini areolanın altına yerleştirir, damağıyla peristaltik dalga yapar. "
            "2. Biberon emziğinde ise yapay kauçuk/silikon uçtan süt neredeyse kendiliğinden damlar; bebek sadece diş etleriyle ucu sıkarak pasif emer. "
            "3. Biberonun kolaylığına alışan bebek, anne memesine döndüğünde diliyle memeyi dışarı iter, kavramayı reddeder veya memeyi ısırarak anneyi yaralar. "
            "Ayrıca biberon ve yalancı emzik kullanımı; **erken sütten kesilme, otitis media (orta kulak iltihabı) sıklığında artış "
            "ve diş arkında maloklüzyon (çene yapısı bozukluğu)** risklerini dramatik şekilde artırır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Biberon veya yalancı emzik verilen bebeklerde anne memesini kavramada yaşanan mekanik disfonksiyona meme başı şaşkınlığı denir.",
                "meme başı şaşkınlığı",
                "Yapay kauçuk uç ile fizyolojik meme arasındaki emme karmaşası"
            ),
            make_causal_chain(
                "Meme Başı Şaşkınlığı ve Emzirmeyi Bırakma Zinciri",
                [
                    "1. Yapay Emzik Teması: Bebeğe su, mama veya sakinleştirme amacıyla biberon/emzik verilir.",
                    "2. Kas Belleği Değişimi: Bebek dilini aktif dalgalandırmak yerine biberonun pasif akışına alışır.",
                    "3. Memeyi Reddetme: Anne memesine tutulunca bebek memeyi kavrayamaz, sinirlenir ve ağlayarak iter.",
                    "4. Süt Üretiminin Çökmesi: Meme uyarılmadığı için prolaktin düşer, süt çekilir ve erken ablasyon gerçekleşir."
                ]
            ),
            make_active_recall(
                "Yenidoğan yoğun bakımda yatan veya sağılmış süt verilmesi gereken bir bebeğe meme başı şaşkınlığını önlemek için biberon yerine hangi besleme araçları tercih edilmelidir?",
                "Kaşık, kadeh (beslenme kabı) veya enjektör / damlalık gibi dili ve damağı pasifleştirmeyen araçlar tercih edilmelidir.",
                "Alternatif besleme araçları"
            )
        ]
    })

    # Slayt 76: Sağılmış Anne Sütü Saklama Kuralları: 3 - 3 - 3 Kuralı
    slides.append({
        "id": "k1-22-s76",
        "title": "Sağılmış Anne Sütü Saklama Kuralları: 3 - 3 - 3 Kuralı",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 76,
        "narrative": (
            "Çalışan anneler, prematüre bebek anneleri veya memeyi tam boşaltamayan kadınlar için sütün sağılarak saklanması altın standarttır. "
            "Anne sütü içerdiği güçlü antimikrobiyal faktörler sayesinde inek sütünden çok daha dayanıklıdır. "
            "Klinik uygulamada akılda kalması en kolay ve güvenli kılavuz **'3 - 3 - 3 Kuralı'dır**: "
            "1. **Oda Isısında (22-26 °C):** Temiz koşullarda sağılmış süt oda ısısında güvenle **3 saat** kalabilir (serin ortamda 4-6 saate kadar uzayabilir). "
            "2. **Buzdolabında (+4 °C):** Buzdolabının kapağında değil, iç arka kısımlarında **3 gün** (ideal) ile 5 gün saklanabilir. "
            "3. **Derin Dondurucuda (-18 °C veya altı):** Bağımsız dondurucu bölmesinde **3 ay** boyunca bozulmadan dondurulabilir. "
            "Sütler temiz, BPA içermeyen cam şişelerde veya tek kullanımlık anne sütü saklama poşetlerinde, üzerine tarih ve saat yazılarak depolanmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Sağılmış anne sütü oda ısısında üç saat, buzdolabında üç gün ve derin dondurucuda üç ay saklanabilir.",
                "üç saat, buzdolabında üç gün ve derin dondurucuda üç ay",
                "Laktasyon saklama protokolünün 3-3-3 kuralı"
            ),
            make_table(
                "Sağılmış Anne Sütü Saklama Süreleri ve Koşulları (3-3-3 Protokolü)",
                ["Saklama Ortamı", "Ortam Sıcaklığı", "Maksimum Güvenli Süre", "Dikkat Edilecek Püf Noktası"],
                [
                    [
                        "Oda Sıcaklığı",
                        "22 - 26 °C",
                        {"text": "3 saat", "isMasked": True, "hint": "Oda ısısındaki saatlik dayanma sınırı"},
                        "Güneş ışığından ve kaloriferden uzak"
                    ],
                    ["Buzdolabı Rafı", "+4 °C", "3 gün (maks 5 gün)", "Kapakta değil, en soğuk iç rafta"],
                    ["Derin Dondurucu", "-18 °C", "3 ay", "Tarih etiketli, genleşme payı bırakılarak"]
                ]
            ),
            make_micro_quiz(
                "Çalışan bir annenin sağdığı anne sütünü oda sıcaklığında (yaklaşık 22-24 °C) bebeğine güvenle içirebilmesi için önerilen süre ne kadardır?",
                {
                    "A": "En fazla 15 dakika",
                    "B": "3 saat",
                    "C": "24 saat",
                    "D": "3 gün",
                    "E": "1 hafta"
                },
                "B",
                {
                    "A": "Yanlıştır; 15 dakika çok kısıtlayıcıdır, anne sütünün antibakteriyel koruması vardır.",
                    "B": "Doğrudur; 3-3-3 kuralına göre oda ısısında 3 saat güvenle bekletilebilir.",
                    "C": "Yanlıştır; 24 saat oda ısısında bakteri üremesine yol açar.",
                    "D": "Yanlıştır; 3 gün buzdolabı (+4 °C) raf süresidir.",
                    "E": "Yanlıştır; 1 hafta dondurucu dışı ortamlarda kesin bozulur."
                }
            )
        ]
    })

    # Slayt 77: Sağılmış Sütün Isıtılması, Çözdürülmesi ve Güvenlik Protokolü
    slides.append({
        "id": "k1-22-s77",
        "title": "Sağılmış Sütün Isıtılması, Çözdürülmesi ve Güvenlik Protokolü",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 77,
        "narrative": (
            "Dondurulmuş veya buzdolabında bekletilmiş anne sütünün bebeğe verilmeden önce hazırlanması yüksek titizlik gerektirir: "
            "1. **Çözdürme Aşaması:** Dondurucudan çıkarılan süt bir gece önceden buzdolabı rafına (+4 °C) konularak yavaşça çözdürülmelidir. "
            "Acil durumlarda ılık su dolu bir kaba konularak çözdürülebilir. "
            "2. **Benmari Usulü Ilıtma:** Süt kabı, sıcak su içeren bir kabın içine oturtularak (benmari usulü) vücut sıcaklığına (37 °C) getirilmelidir. "
            "3. **Mikrodalga Fırın ve Doğrudan Ateş YASAĞI:** Anne sütü **asla mikrodalgada ısıtılmamalı ve ocakta kaynatılmamalıdır**. "
            "Mikrodalga sütün homojen ısınmasını engelleyerek 'sıcak noktalar' yaratır ve bebeğin ağzını yakar; "
            "ayrıca aşırı ısı laktoferrin, lizozim ve sekretuvar IgA gibi **tüm koruyucu proteinleri denatüre ederek yok eder**. "
            "4. **Tekrar Dondurma Yasağı:** Çözdürülmüş süt ASLA tekrar dondurulamaz; bebekten arta kalan süt bir sonraki öğüne saklanamaz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütünün mikrodalga fırında ısıtılması koruyucu antikorları ve enzimleri denatüre ettiği ve sıcak noktalarla ağzı yaktığı için kesinlikle yasaktır.",
                "mikrodalga fırında ısıtılması",
                "İmmün proteinleri tahrip eden elektromanyetik ısıtma yöntemi"
            ),
            make_micro_quiz(
                "Dondurulmuş anne sütünün çözdürülmesi ve ısıtılması sürecinde aşağıdakilerden hangisi KESİNLİKLE YAPILMAMALIDIR?",
                {
                    "A": "Dondurucudan çıkan sütün önce buzdolabı rafına alınarak yavaşça çözdürülmesi",
                    "B": "Sütün ılık su banyosu içine (benmari usulü) oturtularak ılıtılması",
                    "C": "Mikrodalga fırında yüksek güçte ısıtılarak hızlıca bebeğe verilmesi",
                    "D": "Isıtılan sütün bilek içine damlatılarak sıcaklığının kontrol edilmesi",
                    "E": "Çözünen sütün tekrar derin dondurucuya atılmaması"
                },
                "C",
                {
                    "A": "Doğru yöntemdir; Kademeli çözdürme proteinleri korur.",
                    "B": "Doğru yöntemdir; Benmari usulü en güvenli ısıtma yoludur.",
                    "C": "Kesinlikle Yasaktır; Mikrodalga koruyucu antikorları parçalar ve bebekte ağız içi yanıklara yol açar.",
                    "D": "Doğru yöntemdir; Termal yanık kontrolüdür.",
                    "E": "Doğru yöntemdir; Çözünen süt asla tekrar dondurulamaz."
                }
            ),
            make_active_recall(
                "Dondurulmuş anne sütü çözdürüldükten sonra bebek tarafından içilmeyip biberonda artan sütün saklanma kuralı nedir?",
                "Artan süt tükürük teması ve mikrobiyal üreme riski nedeniyle atılmalıdır; tekrar ısıtılamaz veya dondurulamaz.",
                "Tükürük teması ve artan sütün akıbeti"
            )
        ]
    })

    # Slayt 78: Emzirmeyi Bozan Durumlar: Mastit Yönetimi ve Kontrendikasyonlar
    slides.append({
        "id": "k1-22-s78",
        "title": "Emzirmeyi Bozan Durumlar: Mastit Yönetimi ve Kontrendikasyonlar",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 78,
        "narrative": (
            "Klinik pratikte anne veya bebeğe ait bazı patolojiler emzirmeyi tehdit eder: "
            "1. **Meme Angorjmanı ve Mastit:** Süt kanallarının tıkanmasıyla memede ağrılı, kızarık ve sıcak kitle oluşur (Staph. aureus mastiti). "
            "**Kritik Kural: Mastitte emzirmeye KESİNLİKLE DEVAM EDİLİR!** Emzirmeyi kesmek stazı artırarak apseye yol açar; "
            "bebek hasta memeyi emerek kanalları boşaltmalıdır, anneye uygun antibiyotik (amoksisilin-klavulanat) başlanır. "
            "2. **Bebeğe Ait Mutlak Kontrendikasyon: Klasik Galaktozemi**. Bebekte galaktoz-1-fosfat üridiltransferaz eksikliği varsa "
            "anne sütündeki laktoz ölümcüldür; derhal laktozsuz soya/özel mamaya geçilir. "
            "3. **Anneye Ait Kontrendikasyonlar:** Aktif tedavi edilmemiş tüberküloz (anne tedavi alana kadar sağılmış süt verilir), "
            "meme cildinde aktif herpetik lezyon (sağlam memeden emzirilir), antimetabolit/kemoterapi ilaçları ve radyoaktif madde kullanımıdır. "
            "Gelişmiş ülkelerde HIV pozitifliği kontrendikedir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne memesinde ağrı, ateş ve kızarıklıkla seyreden mastit tablosunda emzirmeye kesinlikle devam edilmeli ve meme boşaltılmalıdır.",
                "emzirmeye kesinlikle devam edilmeli",
                "Kanal tıkanıklığını ve abseleşmeyi önleyen en kritik klinik kural"
            ),
            make_table(
                "Emzirmeyi Etkileyen Durumlar ve Doğru Klinik Kararlar",
                ["Klinik Durum", "Doğru Klinik Karar", "Hatalı / Tehlikeli Karar", "Gerekçe"],
                [
                    [
                        "Bakteriyel Mastit",
                        {"text": "Emzirmeye ısrarla devam etmek", "isMasked": True, "hint": "Kanal stazını çözmek için süt akışını sürdürme"},
                        "Emzirmeyi derhal kesmek",
                        "Memenin boşaltılması iyileşmeyi hızlandırır, apseyi önler"
                    ],
                    ["Bebekte Galaktozemi", "Anne sütünü derhal kesmek", "Emzirmeye devam etmek", "Karaciğer yetmezliği ve katarakt riski"],
                    ["Memede Aktif HSV", "O memeden emzirmemek", "Lezyonlu memeyi emzirmek", "Bebekte ölümcül neonatal herpes sepsisi"],
                    ["Maternal Kemoterapi", "Emzirmeyi tamamen durdurmak", "Emzirmeye devam etmek", "Sitotoksik ilaçların süte geçişi"]
                ]
            ),
            make_micro_quiz(
                "Doğumdan 3 hafta sonra sağ memesinde şiddetli ağrı, kızarıklık, şişlik ve 38.8 °C ateş ile başvuran bir anneye mastit tanısı konuluyor. Bu vakada en uygun yaklaşım hangisidir?",
                {
                    "A": "Sağ memeden emzirmeyi derhal durdurup bebeğe formül mama başlamak",
                    "B": "Meme ucunu alkolle temizleyip emzirmeye 1 hafta ara vermek",
                    "C": "Uygun sistemik antibiyotik başlarken sağ memeden emzirmeye sık aralıklarla devam etmek",
                    "D": "Mastitli memeden sağılan sütü kaynatarak bebeğe vermek",
                    "E": "Memeyi bandajla sıkıca sararak süt yapımını tamamen baskılamak"
                },
                "C",
                {
                    "A": "Yanlıştır; Emzirmeyi kesmek süt stazını artırır ve apse gelişimini hızlandırır.",
                    "B": "Yanlıştır; Alkol meme derisini kurutur, emzirmeye ara verilmez.",
                    "C": "Doğrudur; Memenin boşaltılması tedavinin en kritik parçasıdır; antibiyotik altında emzirme güvenlidir.",
                    "D": "Yanlıştır; Süt kaynatılmaz, doğrudan emzirilir.",
                    "E": "Yanlıştır; Bandajlamak stazı ve doku hasarını artırır."
                }
            )
        ]
    })

    # Slayt 79: [TEKRAR SAYFASI - CHECKPOINT 8] Emzirme Pratiği ve Süt Saklama Protokolü
    slides.append({
        "id": "k1-22-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Emzirme Pratiği ve Süt Saklama Protokolü",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 79,
        "narrative": (
            "Bu checkpoint sayfasında, başarılı emzirmenin altın kurallarını, süt saklama sürelerini ve klinik kontrendikasyonları özetliyoruz: "
            "1. **İlk Adım:** Doğumdan sonra ilk 30-60 dakikada ten tene temas başlatılmalı ve ilk emzirme gerçekleştirilmelidir. "
            "2. **Doğru Kavrama:** Areolanın büyük kısmı ağızda olmalı, alt dudak dışa kıvrılmalı ve çene memeye değmelidir. "
            "Meme başı çatlağı enfeksiyon değil, hatalı kavramanın mekanik sonucudur. "
            "3. **BDHG ve Rooming-in:** Anne ve bebek 24 saat aynı odada kalmalı; saat kısıtlaması olmaksızın isteğe bağlı (on-demand) beslenmelidir. "
            "Gece emzirmeleri prolaktini zirvede tutar. Yalancı emzik ve biberon meme başı şaşkınlığı yapar. "
            "4. **3-3-3 Kuralı:** Sağılmış anne sütü oda sıcaklığında 3 saat, buzdolabında 3 gün, dondurucuda 3 ay saklanır. "
            "Asla mikrodalgada ısıtılmaz ve kaynatılmaz (benmari usulü ısıtılır). "
            "5. **Mastit:** Emzirmenin kesilme nedeni değildir; aksine meme mutlaka sık emzirilerek boşaltılmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "flashcards": [
            make_flashcard(
                "k1-22-fc-s79-1",
                "Sağılmış anne sütünün '3 - 3 - 3' kuralına göre oda ısısında, buzdolabında ve derin dondurucuda saklanma süreleri sırasıyla nedir?",
                "Oda sıcaklığında 3 saat, buzdolabında 3 gün ve dondurucuda 3 aydır.",
                "Kısa, orta ve uzun vadeli kademeli koruma süreleri",
                "Süt Saklama Protokolü"
            ),
            make_flashcard(
                "k1-22-fc-s79-2",
                "Emziren bir annede bakteriyel mastit geliştiğinde emzirme eylemine yönelik temel klinik yaklaşım ne olmalıdır?",
                "Emzirmeye kesinlikle devam edilmeli ve meme sık aralıklarla emzirilerek boşaltılmalıdır.",
                "Kanal tıkanıklığına karşı laktasyonun sürdürülmesi",
                "Klinik Emzirme Yönetimi"
            ),
            make_flashcard(
                "k1-22-fc-s79-3",
                "Bebekte saptandığında anne sütüyle beslenmenin mutlak olarak yasaklandığı konjenital metabolik bozukluk hangisidir?",
                "Klasik Galaktozemi hastalığıdır.",
                "Laktozun yapı taşı olan şekerin yıkılamadığı enzim eksikliği",
                "Mutlak Kontrendikasyonlar"
            )
        ],
        "interactiveElements": [
            make_table(
                "Başarılı Emzirme Yönetiminde Kritik Doğrular ve Yanlışlar",
                ["Uygulama Alanı", "Doğru Tıbbi Uygulama", "Geleneksel Yanlış Uygulama"],
                [
                    ["İlk Besin", "İlk 30-60 dk içinde kolostrum", "Şekerli su veya serum vermek"],
                    [
                        "Emzirme Sıklığı",
                        {"text": "İsteğe bağlı, gece dahil günde 8-12 kez", "isMasked": True, "hint": "Açlık işaretlerine göre saat kısıtlamasız besleme"},
                        "3 saatte bir katı saatli besleme"
                    ],
                    ["Meme Başı Ağrısı", "Kavrama tekniğini düzeltmek", "Emzirmeye ara verip krem sürmek"],
                    ["Sağılmış Sütü Isıtma", "Benmari usulü ılık suda", "Mikrodalga veya ocakta kaynatma"]
                ]
            )
        ]
    })

    # Slayt 80: Bölüm Özeti: Emzirme Yönetiminden Tamamlayıcı Beslenmeye Geçiş
    slides.append({
        "id": "k1-22-s80",
        "title": "Bölüm Özeti: Emzirme Yönetiminden Tamamlayıcı Beslenmeye Geçiş",
        "section": "Başarılı Emzirme Yönetimi, Teknikler ve Süt Saklama Koşulları",
        "slideNumber": 80,
        "narrative": (
            "Başarılı bir emzirme dönemi doğum anında ten tene temasla başlar; doğru kavrama tekniği, oda birlikteliği (rooming-in), "
            "on-demand besleme ve gece emzirmeleriyle sürdürülür. "
            "Biberon ve emziğin dışlanması meme başı şaşkınlığını ve erken kesilmeyi önlerken, 3-3-3 kuralı çalışan annelerin sütünü korur. "
            "Mastit gibi tablolarda emzirmenin sürdürülmesi hekimin en temel kılavuzluğudur. "
            "İlk 6 ay boyunca tek başına anne sütü bebeğin su dahil tüm gereksinimlerini eksiksiz karşılar. "
            "Ancak 6. aya gelindiğinde bebeğin nöromotor olgunlaşması ve artan besin ihtiyaçları yeni bir dönemi başlatır: "
            "Bir sonraki bölümde, **'Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri, Gelişimsel Eşikler, Yasak Besinler ve 3 Gün Kuralı'** "
            "ayrıntılarıyla incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_active_recall(
                "İlk 6 ay tek başına anne sütü alan bir bebeğin 6. aydan itibaren tamamlayıcı besinlere ihtiyaç duymaya başlamasının iki ana nedeni nedir?",
                "Bebeğin hızla büyüyen vücudunun enerji, demir ve çinko ihtiyacının anne sütünü aşması ve çiğneme reflekslerinin gelişmesidir.",
                "Enerji açığı, tükenen demir depoları ve oral motor gelişim"
            ),
            make_branching_logic(
                "6 aylık bebeği olan bir anne, bebeğinin artık büyüdüğünü ve sütünün yetmediğini düşünerek doğrudan aile sofrasındaki yemeklerden (tuzlu, baharatlı, salçalı) yedirmeye başladığını belirtiyor.",
                "Hekim olarak tamamlayıcı beslenmeye geçişte anneye verilecek en doğru rehberlik hangisidir?",
                [
                    {
                        "text": "Tamamlayıcı beslenmeye tek çeşit, tuzsuz, şekersiz, alerji yapma riski düşük besinlerle (yoğurt, sebze püresi) 3 gün kuralına uyularak ve anne sütüne devam edilerek başlanmalıdır",
                        "isCorrect": True,
                        "feedback": "Mükemmel Klinik Yaklaşım: Tamamlayıcı besinler kademeli, alerji takipli ve tuzsuz/şekersiz başlanmalı, anne sütü ana besin olarak kalmalıdır."
                    },
                    {
                        "text": "Anne sütünü derhal kesip bebeğin tamamen aile sofrası yemekleriyle doymasını sağlamak",
                        "isCorrect": False,
                        "feedback": "Hatalı: 6-12 ayda anne sütü enerjinin en az %50'sini karşılar; anne sütü kesilmez."
                    },
                    {
                        "text": "Bebek 1 yaşına gelene kadar anne sütü dışında hiçbir besin vermemek",
                        "isCorrect": False,
                        "feedback": "Hatalı: 6. aydan sonra ek gıda verilmezse demir eksikliği anemisi, çiğneme tembelliği ve malnütrisyon kaçınılmazdır."
                    }
                ]
            )
        ]
    })

    return slides
