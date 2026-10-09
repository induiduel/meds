# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 9: Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler (Slayt 81 - 90)
Checkpoint 9: Slayt 89
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # Slayt 81: Tamamlayıcı Beslenme Tanımı ve Temel Felsefesi
    slides.append({
        "id": "k1-22-s81",
        "title": "Tamamlayıcı Beslenme Tanımı ve Temel Felsefesi",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 81,
        "narrative": (
            "Tamamlayıcı beslenme (eski adıyla ek gıdalar), **bebeğin 6. ayını (180 gününü) doldurduğu andan itibaren**, "
            "tek başına anne sütünün bebeğin artan enerji ve besin ögesi ihtiyaçlarını karşılamaya yetmediği dönemde "
            "anne sütüne ek olarak diğer katı, yarı-katı ve sıvı gıdaların diyete eklenmesi sürecidir. "
            "Burada en kritik kavramsal ilke şudur: **Tamamlayıcı besinler anne sütünün YERİNİ ALMAZ, onu TAMAMLAR**. "
            "6-12 ay arasında anne sütü bebeğin ana besini olmaya devam eder; günlük kalori ihtiyacının yaklaşık **%50'sini** karşılar. "
            "12-24 ay arasında ise günlük kalorinin yaklaşık **üçte birini (%30-35)** sağlamayı sürdürür. "
            "Bu süreçte amaç bebeği aniden sütten kesmek değil, çiğneme reflekslerini eğiterek onu kademeli olarak aile sofrasına hazırlamaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Tamamlayıcı beslenme döneminde ek gıdalar anne sütünün yerine geçmez, onu tamamlar ve 6-12 ayda kalorinin yaklaşık yüzde ellisi anne sütünden gelir.",
                "yüzde ellisi",
                "Altıncı ve on ikinci aylar arasında anne sütünün sağladığı enerji payı"
            ),
            make_table(
                "Farklı Yaş Gruplarında Anne Sütü ve Tamamlayıcı Besin Enerji Dağılımı",
                ["Bebek Yaş Dönemi", "Anne Sütü Enerji Payı", "Tamamlayıcı Besin Payı", "Temel Beslenme Amacı"],
                [
                    ["İlk 6 Ay (0 - 180 Gün)", "%100 (Tek Başına)", "%0 (Sıfır)", "Mükemmel büyüme ve enfeksiyon kalkanı"],
                    [
                        "6 - 12 Ay Arası",
                        {"text": "Yaklaşık %50", "isMasked": True, "hint": "Yarı yarıya dengeli enerji ortaklığı"},
                        "Yaklaşık %50",
                        "Enerji açığını kapatma ve tat alışkanlığı"
                    ],
                    ["12 - 24 Ay Arası", "Yaklaşık %30 - 35", "Yaklaşık %65 - 70", "Aile sofrasına tam entegrasyon"]
                ]
            ),
            make_micro_quiz(
                "Tamamlayıcı beslenme döneminde anne sütünün rolü ile ilgili aşağıdakilerden hangisi bilimsel olarak doğrudur?",
                {
                    "A": "6. ay biter bitmez anne sütü tamamen kesilmeli ve katı gıdaya geçilmelidir",
                    "B": "6-12 ay arasında anne sütü çocuğun enerji ihtiyacının yaklaşık yarısını (%50) karşılamaya devam eder",
                    "C": "Tamamlayıcı besinlere başlandığında anne sütündeki immünglobulinler tamamen kaybolur",
                    "D": "1 yaşından sonra anne sütü vermek bebeğin gelişimini durdurur",
                    "E": "Tamamlayıcı besinler anne sütünden önce verilmeli, bebek ancak doymazsa memeye tutulmalıdır"
                },
                "B",
                {
                    "A": "Yanlıştır; Anne sütü 2 yaşına kadar sürdürülmelidir.",
                    "B": "Doğrudur; 6-12 ayda enerjinin %50'si, 12-24 ayda %30-35'i anne sütünden sağlanır.",
                    "C": "Yanlıştır; İmmünolojik koruma 2 yaş boyunca devam eder.",
                    "D": "Yanlıştır; 1 yaşından sonra da kaliteli protein ve mikro besin kaynağıdır.",
                    "E": "Yanlıştır; Öncelik anne sütüdür, tamamlayıcı gıdalar destekleyicidir."
                }
            )
        ]
    })

    # Slayt 82: Neden Tam 6. Ay?: Enerji Açığı ve Tükenen Demir Depoları
    slides.append({
        "id": "k1-22-s82",
        "title": "Neden Tam 6. Ay?: Enerji Açığı ve Tükenen Demir Depoları",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 82,
        "narrative": (
            "DSÖ ve tıp kılavuzlarının tamamlayıcı beslenmeye başlama zamanı olarak kesinlikle **'180. günü (6. ayı)'** belirlemesinin "
            "iki temel fizyolojik ve metabolik gerekçesi vardır: "
            "1. **Enerji Açığı (Energy Gap):** Term doğan sağlıklı bir bebeğin günlük enerji ihtiyacı 6. aydan sonra yaklaşık 600-700 kcal'ye yükselir. "
            "Bir annenin günde ürettiği ortalama 700-800 ml süt ise ancak 450-500 kcal sağlayabilir. "
            "Ortaya çıkan yaklaşık **200 kcal'lik enerji açığı** ancak kaliteli tamamlayıcı besinlerle kapatılabilir. "
            "2. **Tükenen Fetal Demir ve Çinko Depoları:** Yenidoğan bebek intrauterin hayatta karaciğerinde depoladığı demir ile doğar. "
            "Bu fetal demir rezervi term bebekte tam **4-6 ayda tükenir**. "
            "Anne sütünün demir emilimi mükemmel olsa da toplam demir miktarı düşüktür; bu yüzden 6. aydan itibaren demir ve çinko zengini "
            "gıdalar başlanmazsa ağır mikrositer anemi ve büyüme duraklaması kaçınılmaz hale gelir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğanın doğumda karaciğerinde depoladığı fetal demir rezervi term doğan bebeklerde dördüncü altıncı aylarda tükenir.",
                "dördüncü altıncı aylarda",
                "Karaciğerdeki konjenital demir depolarının boşalma zamanı"
            ),
            make_causal_chain(
                "6. Ayda Tamamlayıcı Beslenme İhtiyacının Metabolik Zinciri",
                [
                    "1. Büyüme İvmesi: 6. ayda bebeğin doğum ağırlığı iki katına çıkar, metabolik enerji ihtiyacı sıçrama yapar.",
                    "2. Anne Sütü Kapasitesi: Anne sütü tek başına günlük kalori ve protein ihtiyacını karşılayamaz hale gelir.",
                    "3. Fetal Depo Tükenişi: Karaciğerde depolanan intrauterin demir ve çinko 6. ay civarında tamamen boşalır.",
                    "4. Ek Besin Zorunluluğu: Enerji açığını kapatmak ve anemiyi önlemek için katı/yarı-katı besinler devreye girer."
                ]
            ),
            make_active_recall(
                "Tamamlayıcı besinlere geçiş zamanlamasının belirlenmesinde rol oynayan 'enerji açığı' kavramı neyi ifade eder?",
                "6. aydan sonra bebeğin günlük metabolik enerji ihtiyacının anne sütünün sağlayabileceği kaloriyi (~200 kcal) aşması durumudur.",
                "Anne sütünün sağladığı kalori ile bebeğin gereksinimi arasındaki fark"
            )
        ]
    })

    # Slayt 83: Neden 6. Aydan Önce Başlanmaz?: İmmün ve Nöromotor Eşikler
    slides.append({
        "id": "k1-22-s83",
        "title": "Neden 6. Aydan Önce Başlanmaz?: İmmün ve Nöromotor Eşikler",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 83,
        "narrative": (
            "Tamamlayıcı besinlere 6. aydan (veya tıbbi özel durumlar dışında en erken 17. haftadan) önce başlanması son derece tehlikelidir: "
            "1. **Ekstrüzyon (Dili Dışarı İtme) Refleksi:** İlk 4-5 ayda bebeğin ağzına katı bir nesne değdiğinde dilini refleks olarak dışarı iter; "
            "bu koruyucu refleks bebek katı gıdaları yutamasın ve aspire etmesin diye programlanmıştır; 5-6. ayda kaybolur. "
            "2. **Baş ve Gövde Kontrolü:** Bebek 6. aydan önce desteksiz veya mama sandalyesinde dik oturamaz; yatarak katı gıda verilmesi aspirasyon boğulmasına yol açar. "
            "3. **Gastrointestinal İmmatürite:** Bağırsak mukozasında tight-junction bağlantıları gevşektir ve 'açık bağırsak' (open gut) tablosu vardır; "
            "erken verilen yabancı proteinler doğrudan kana geçerek **ağır gıda alerjilerini ve atopiyi** tetikler. "
            "Ayrıca pankreatik amilaz ve safra tuzu salgısı ilk 4-6 ayda karmaşık nişastaları sindirmeye yetersizdir. "
            "4. **Böbrek Yükü:** İmmatür glomerüller ek besinlerin yüksek solüt yükünü tolere edemez."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İlk aylarda kaşıkla verilen katı besinlerin ağız dışına itilmesini sağlayan ve 5-6. ayda kaybolan koruyucu reflekse ekstrüzyon refleksi denir.",
                "ekstrüzyon refleksi",
                "Aspirasyonu önleyen dili dışarı itme yanıtı"
            ),
            make_before_after(
                "Bağırsak Geçirgenliği: 4 Aydan Önce vs 6. Ay Sonrası",
                "4 Aydan Önce (Açık Bağırsak)",
                "İnterenterosit tight junctionlar henüz olgunlaşmamıştır; yabancı antijenik gıda proteinleri mukozayı aşarak kana geçer ve ağır atopik alerjileri tetikler.",
                "6. Ay Sonrası (Matür Mukozal Bariyer)",
                "Bağırsak epitel bağlantıları kapanmış, sIgA zırhı güçlenmiş ve enzimler olgunlaşmıştır; alerjen proteinlerin kontrolsüz geçişi bloke edilir."
            ),
            make_micro_quiz(
                "Süt çocuklarında tamamlayıcı besinlere 4. aydan önce çok erken başlanmasının yaratabileceği klinik riskler arasında hangisi YER ALMAZ?",
                {
                    "A": "Ekstrüzyon refleksi nedeniyle besinin soluk borusuna kaçarak aspirasyon pnömonisi yapması",
                    "B": "Gevşek mukozal bariyerden geçen yabancı proteinler nedeniyle gıda alerjisi gelişimi",
                    "C": "Anne sütü alımının azalmasına bağlı büyüme-gelişme geriliği ve enfeksiyon artışı",
                    "D": "Pankreatik amilaz yetersizliği nedeniyle hazımsızlık ve ozmotik ishal tablosu",
                    "E": "Bağırsak epitelinin hızla yaşlanarak kalsiyum emiliminin tamamen durması"
                },
                "E",
                {
                    "A": "Yer alır; Dili dışarı itme refleksi aspirasyona yol açar.",
                    "B": "Yer alır; Mukozal bariyer immatürdür, alerji tetiklenir.",
                    "C": "Yer alır; Erken ek gıda anne sütünün yerini alır.",
                    "D": "Yer alır; Amilaz enzimi ilk aylarda yetersizdir.",
                    "E": "Tıbbi olarak anlamsızdır; Bağırsak epiteli yaşlanmaz, kalsiyum emilimi durmaz."
                }
            )
        ]
    })

    # Slayt 84: Geç Başlamanın (8. Aydan Sonra) Tehlikeleri: Oral Motor Disfonksiyon
    slides.append({
        "id": "k1-22-s84",
        "title": "Geç Başlamanın (8. Aydan Sonra) Tehlikeleri: Oral Motor Disfonksiyon",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 84,
        "narrative": (
            "Tamamlayıcı beslenmeye erken başlamak kadar, **8. aydan sonraya gecikmek de ağır klinik patolojilere yol açar**. "
            "Bebek gelişiminde 6-9. aylar arasında çiğneme, dili damağa bastırarak lokmayı arkaya itme ve yutma kaslarının nöromotor **'kritik öğrenme penceresi'** vardır. "
            "Eğer bu kritik pencere kaçırılırsa: "
            "1. **Oral Motor Disfonksiyon ve Pütürlü Gıda Reddi:** Bebek sadece sıvı emmeyi bilir; katı veya pütürlü bir parça ağzına geldiğinde "
            "öğürür, kusar ve gıdayı panikle dışarı püskürtür. Bu durum yıllarca sürebilecek yeme bozukluklarının temelini atar. "
            "2. **Ağır Malnütrisyon:** 8. aydan sonra tek başına anne sütü bebeğin enerji gereksinimini karşılayamadığından boy kısalığı ve bodurluk (stunting) gelişir. "
            "3. **Derin Demir Eksikliği Anemisi:** Boşalan demir depoları takviye edilmediği için nörobilişsel gelişimi geri dönülmez biçimde bozan anemi oturur. "
            "4. **Çinko Eksikliği:** İmmün yetmezlik, kronik ishal ve büyüme duraklaması tablosu yerleşir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Tamamlayıcı besinlere sekizinci aydan sonra geç başlanması çiğneme kaslarının kritik penceresini kaçırarak pütürlü gıda reddine yol açar.",
                "pütürlü gıda reddine",
                "Öğürme ve katı lokmayı tükürmeyle seyreden oral motor yeme bozukluğu"
            ),
            make_causal_chain(
                "Tamamlayıcı Beslenmeye Geç Başlamanın Patofizyolojik Seyri",
                [
                    "1. Kritik Nöromotor Pencerenin Kaçırılması: 6-9 aylık dönemde çiğneme refleksleri eğitilmez.",
                    "2. Çiğneme Becerisi Eksikliği: Dil ve masseter kasları pütürlü dokuları ezmeyi öğrenemez.",
                    "3. Öğürme ve Besin Reddi: Ağza gelen yarı-katı lokmalar öğürme refleksiyle kusulur ve besin reddi başlar.",
                    "4. Ağır Anemi ve Bodurluk: Kalori, demir ve çinko açığı kronikleşerek protein-enerji malnütrisyonuna dönüşür."
                ]
            ),
            make_active_recall(
                "Tamamlayıcı beslenmeye başlama zamanının nöromotor açıdan 6-9. aylarda olmasını zorunlu kılan gelişimsel kavram nedir?",
                "Çiğneme, pütürlü dokuları ezme ve yutma koordinasyonunun kazanıldığı kritik öğrenme penceresidir.",
                "Oral motor çiğneme becerisinin kritik penceresi"
            )
        ]
    })

    # Slayt 85: Tamamlayıcı Besinlerin İdeal Nitelikleri ve Kıvam Evrimi
    slides.append({
        "id": "k1-22-s85",
        "title": "Tamamlayıcı Besinlerin İdeal Nitelikleri ve Kıvam Evrimi",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 85,
        "narrative": (
            "Bebeğe sunulan tamamlayıcı besinlerin biyolojik ve fiziksel özellikleri titizlikle planlanmalıdır: "
            "1. **Enerji Yoğunluğu (Dansitesi):** Besinler sulu çorbalar şeklinde olmamalıdır! Fazla su bebeğin minik midesini doldurarak erkenden doygunluk hissi yaratır. "
            "Besinler kaşıkta akmayacak kıvamda, az hacimde yüksek kalori ve demir barındırmalıdır. "
            "2. **Kıvam Evrimi (Doku Aşamaları):** "
            "- **6. Ay:** Pürüzsüz püre veya muhallebi kıvamı (çatalla ezilmiş). "
            "- **7-8. Ay:** Hafif pütürlü püreler ve ezilmiş sebzeler; parmak gıdaların (haşlanmış havuç, muz dilimi) tanıtılması. "
            "- **9-11. Ay:** Küçük lokmalar halinde doğranmış, çiğnenebilen yumuşak aile yemekleri. "
            "- **12. Ay ve Sonrası:** Baharatsız ve az tuzlu aile sofrası yemekleri. "
            "3. **Temizlik ve Güvenlik:** Taze hazırlanmalı, oda ısısında bekletilmemeli, çiğ besinler bol suyla yıkanmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Tamamlayıcı besinler sulu çorba şeklinde değil, minik mideyi suyla doldurmayacak yüksek enerji dansitesine sahip püre kıvamında olmalıdır.",
                "yüksek enerji dansitesine",
                "Birim hacimde zengin kalori ve besin yoğunluğu"
            ),
            make_table(
                "Aylara Göre Tamamlayıcı Besin Kıvamı ve Besleme Becerisi Evrimi",
                ["Bebek Yaşı", "Önerilen Gıda Kıvamı / Dokusu", "Bebeğin Gelişimsel Becerisi", "Örnek Besin"],
                [
                    ["6. Ay", "Pürüzsüz püre / Ezme", "Diliyle damağına bastırarak yutma", "Çatalla ezilmiş kabak veya yoğurt"],
                    [
                        "7 - 8. Ay",
                        {"text": "Pütürlü püre ve parmak gıdalar", "isMasked": True, "hint": "Çiğnemeyi öğreten hafif parçacıklı kıvam"},
                        "Dil yan hareketleri ve damağa ezme",
                        "Haşlanmış yumuşak havuç çubuğu"
                    ],
                    ["9 - 11. Ay", "İnce kıyılmış / Doğranmış gıda", "Parmaklarıyla tutup ağza götürme", "Kıyılmış köfte veya yumuşak meyve"],
                    ["12. Ay+", "Aile sofrası yemekleri", "Kendi kaşığını ve bardağını kullanma", "Tuzsuz tencere yemekleri"]
                ]
            ),
            make_active_recall(
                "Süt çocuklarında tamamlayıcı beslenme döneminde 'sulu kemik suyu veya süzme sebze çorbası' verilmesinin en temel sakıncası nedir?",
                "Enerji ve besin dansitesinin çok düşük olması, bebeğin midesini suyla doldurarak kalori ve demir açığı yaratmasıdır.",
                "Düşük kalori dansitesi ve mide hacmini suyla işgal etme"
            )
        ]
    })

    # Slayt 86: İlk Başlanacak Besinler ve Doğru Besin Sıralaması
    slides.append({
        "id": "k1-22-s86",
        "title": "İlk Başlanacak Besinler ve Doğru Besin Sıralaması",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 86,
        "narrative": (
            "6. ayını dolduran bir bebekte tamamlayıcı beslenmeye hangi gıdalarla başlanacağı kültürel alışkanlıklara göre değişse de tıbbi ilkeler sabittir: "
            "1. **Ev Yapımı Doğal Yoğurt:** Sindirimi kolay, kalsiyum ve probiyotik zengini, alerjenitesi süte göre düşüktür; ilk tercihtir. "
            "2. **Mevsim Sebze Püreleri:** Kabak, havuç, tatlı patates, balkabağı gibi gaz yapmayan, az lifli ve tatlımsı sebzeler buharda pişirilip "
            "çatalla ezilerek zeytinyağı ilavesiyle verilir. Sebzelerin meyveden önce başlanması sebze tadına alışması için önerilir. "
            "3. **Glutensiz Tahıllar:** Pirinç unu veya yulaf ezmesi su veya sağılmış anne sütüyle pişirilerek kaşık maması yapılabilir. "
            "4. **Mevsim Meyve Püreleri:** Elma, şeftali, armut gibi asitsiz meyveler cam rendede rendelenerek başlanır. "
            "5. **Hayvansal Protein ve Demir Kaynağı (7. Aydan İtibaren):** İyice pişmiş yumurta sarısı (sekizde bir ile başlanarak) ve "
            "iki kez çekilmiş dana/kuzu kıyması sebze pürelerine katılarak demir desteği sağlanır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Tamamlayıcı beslenmeye başlarken bebekte sebze tadı kabulünü artırmak için sebze pürelerinin meyve pürelerinden önce tanıtılması önerilir.",
                "sebze pürelerinin meyve pürelerinden önce",
                "Tatlı meyve şekeri bağımlılığını önleyen giriş sırası"
            ),
            make_micro_quiz(
                "6. ayını yeni tamamlamış bir bebeğe ilk tamamlayıcı besin olarak başlanacak gıdalar ve hazırlanışları konusunda hangisi doğrudur?",
                {
                    "A": "Meyveler blenderda tamamen sıvı hale getirilip biberonla verilmelidir",
                    "B": "İlk sebze olarak bakla ve çiğ domates tercih edilmelidir",
                    "C": "Yoğurt, buharda pişirilip çatalla ezilmiş sebze püreleri ve asitsiz meyveler kaşıkla verilmelidir",
                    "D": "Pürelerin lezzetini artırmak için içine bal ve tuz ilave edilmelidir",
                    "E": "Tüm besinler aynı gün karıştırılarak bebeğe tek seferde sunulmalıdır"
                },
                "C",
                {
                    "A": "Yanlıştır; Blender çiğneme refleksini bozar, çatalla ezilmeli ve kaşıkla verilmelidir.",
                    "B": "Yanlıştır; Bakla favizm riski nedeniyle, domates asiditesiyle ilk başta önerilmez.",
                    "C": "Doğrudur; Ev yoğurdu, çatalla ezilmiş sebze ve meyveler kaşıkla başlanır.",
                    "D": "Yanlıştır; Bal ve tuz ilk 1 yıl kesinlikle yasaktır.",
                    "E": "Yanlıştır; Alerji takibi için besinler tek tek tanıtılmalıdır."
                }
            ),
            make_active_recall(
                "Bebeklere sebze püreleri hazırlanırken besinlerin blender yerine çatalla ezilmesinin gelişimsel gerekçesi nedir?",
                "Bebeğin dil ve damak hareketleriyle pütürleri hissetmesini sağlamak ve çiğneme refleksini geliştirmektir.",
                "Blender homojenliği yerine pütürlü doku eğitimi"
            )
        ]
    })

    # Slayt 87: 3 Gün Kuralı ve Alerji - İntolerans Takip Protokolü
    slides.append({
        "id": "k1-22-s87",
        "title": "3 Gün Kuralı ve Alerji - İntolerans Takip Protokolü",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 87,
        "narrative": (
            "Tamamlayıcı beslenmede her yeni besin bir **antijenik sınavdır**. "
            "Gıda alerjilerini, intoleransları veya gastrointestinal reaksiyonları doğru tespit edebilmek için altın standart **'3 Gün Kuralı'dır**: "
            "1. **Tek Besin İlkesi:** Her seferinde sadece tek bir yeni gıda tanıtılır; asla birden fazla yeni gıda aynı gün başlanmaz. "
            "2. **3 Gün Bekleme Süresi:** Yeni besin sabah veya öğle öğününde, 1-2 çay kaşığı gibi küçük bir miktarla başlanır. "
            "Takip eden 3 gün boyunca miktar kademeli artırılırken başka HİÇBİR yeni besin diyete eklenmez (daha önce tolere edilen gıdalar verilebilir). "
            "3. **Klinik Alarm Bulguları:** Bu 3 gün boyunca bebek şu reaksiyonlar açısından yakından izlenir: "
            "- Cilt: Ağız çevresinde kızarıklık, ürtiker (kurdeşen), egzama alevlenmesi. "
            "- GİS: Fışkırır tarzda kusma, müköz veya kanlı ishal, şiddetli gaz sancısı. "
            "- Solunum: Hırıltı, burun tıkanıklığı, öksürük. "
            "Reaksiyon görülürse o besin derhal kesilir ve hekime danışılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yeni başlanan her besinin tek tek tanıtılması ve olası alerjik reaksiyonları gözlemlemek için en az üç gün beklenmesi kuralına üç gün kuralı denir.",
                "üç gün kuralı",
                "Besin intoleransı ve alerji takibinin zamansal altın standardı"
            ),
            make_causal_chain(
                "3 Gün Kuralı Uygulama Basamakları",
                [
                    "1. Tekil Tanıtım: Bebeğe sabah saatlerinde 1 tatlı kaşığı yeni gıda (ör. havuç püresi) kaşıkla tattırılır.",
                    "2. Gözlem ve Tolerans: Gün boyu cilt döküntüsü, kusma veya mukuslu dışkılama olup olmadığı izlenir.",
                    "3. Üç Gün İzolasyonu: Üç gün boyunca başka hiçbir yeni besin denenmez; tolere edilirse miktar artırılır.",
                    "4. Güvenli Liste: Reaksiyon vermeyen besin 'güvenli besinler' listesine eklenir ve bir sonraki yeni besine geçilir."
                ]
            ),
            make_micro_quiz(
                "Tamamlayıcı beslenmeye yeni başlayan bir bebeğin annesine '3 Gün Kuralı' anlatılırken aşağıdakilerden hangisi söylenmelidir?",
                {
                    "A": "Üç yeni sebzeyi aynı anda çorba yapıp üç gün boyunca içirmelidir",
                    "B": "Yeni besini akşam yatmadan hemen önce karnı tokken vermelidir",
                    "C": "Her seferinde sadece tek bir yeni besin başlamalı, az miktarla başlayıp 3 gün boyunca alerji bulgularını gözlemlemelidir",
                    "D": "Bebek yeni besini reddederse burnunu sıkarak zorla yutturmalıdır",
                    "E": "Üç gün kuralı sadece et ve tavuk gibi hayvansal gıdalar için geçerlidir"
                },
                "C",
                {
                    "A": "Yanlıştır; Birden fazla besin başlanırsa alerjinin hangisinden kaynaklandığı anlaşılamaz.",
                    "B": "Yanlıştır; Reaksiyonu gündüz gözlemlemek için sabah veya öğle verilmelidir.",
                    "C": "Doğrudur; Tek besin, küçük porsiyon ve 3 günlük alerji takibi esastır.",
                    "D": "Yanlıştır; Asla zorla besleme yapılmamalıdır.",
                    "E": "Yanlıştır; Sebze, meyve, tahıl dahil tüm gıdalara uygulanır."
                }
            )
        ]
    })

    # Slayt 88: 1 Yaşına Kadar Kesinlikle Yasak Besinler (Kritik Tablo)
    slides.append({
        "id": "k1-22-s88",
        "title": "1 Yaşına Kadar Kesinlikle Yasak Besinler (Kritik Tablo)",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 88,
        "narrative": (
            "Süt çocukluğu döneminde bebeğin immatür organ sistemlerini korumak için **ilk 1 yaşta kesinlikle yasaklanmış gıdalar** vardır: "
            "1. **Bal:** *Clostridium botulinum* sporları içerebilir. Bebek mide asidi ve florası sporları yok edemez; sporlar kolonda açılarak nörotoksin üretir. "
            "Bebekte hipotonik felç, solunum arresti ve ölüme yol açan **'İnfantil Botulizm' (Floppy Baby Sendromu)** tablosunu tetikler. "
            "2. **Tam İnek Sütü:** Bağırsakta mikrokanama, anemi ve 308 mOsm/L aşırı böbrek yükü nedeniyle yasaktır. "
            "3. **Sofra Tuzu ve Rafine Şeker:** Tuz immatür böbreği tüketir ve hipertansiyona yatkınlık yaratır; şeker bağımlılık ve obezite yapar. "
            "4. **Bakla:** Glukoz-6-fosfat dehidrogenaz (G6PD) enzim eksikliği olan bebeklerde ölümcül akut hemolitik krizi (**Favizm**) tetikler. "
            "5. **Çiğ Yumurta Akı:** Yüksek alerjenite taşır; 1 yaşından sonra başlanır (yumurta sarısı 7. ayda verilebilir). "
            "6. **Sert Kabuklu Kuruyemişler (Fındık, Fıstık):** Tane olarak verilmesi ölümcül trakeal yabancı cisim aspirasyonuna yol açar (ancak ezme/un halinde verilebilir)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bir yaşından küçük bebeklere bal verilmesi Clostridium botulinum sporlarına bağlı ölümcül infantil botulizm tablosuna yol açtığı için kesinlikle yasaktır.",
                "infantil botulizm",
                "Bal tüketimiyle tetiklenen gevşek bebek ve solunum felci tablosu"
            ),
            make_table(
                "1 Yaşından Önce Kesinlikle Yasak Olan Besinler ve Klinik Riskleri",
                ["Yasak Besin", "Tehlike Mekanizması / Toksin", "Neden Olduğu Ağır Klinik Tablo"],
                [
                    [
                        "Doğal Bal",
                        "Clostridium botulinum sporları",
                        {"text": "İnfantil botulizm (Gevşek felç)", "isMasked": True, "hint": "Nörotoksine bağlı hipotonik bebek tablosu"}
                    ],
                    ["Tam İnek Sütü", "Beta-laktoglobulin ve yüksek solüt", "GİS mikrokanama, anemi ve böbrek yükü"],
                    ["Bakla (Fava)", "Vicineden oluşan divicin maddesi", "Favizm (Akut hemolitik anemi krizi)"],
                    ["Sofra Tuzu", "Yüksek sodyum konsantrasyonu", "İmmatür böbrekte glomerüler zorlanma"],
                    ["Tane Kuruyemiş", "Sert küresel fiziksel yapı", "Trakeobronşiyal yabancı cisim aspirasyonu"]
                ]
            ),
            make_branching_logic(
                "8 aylık bir bebeğin büyükannesi, bebeğin öksürüğünü yumuşatmak ve balgamını söktürmek amacıyla bir tatlı kaşığı çam balı içirmiştir. "
                "24 saat sonra bebekte emmede zayıflık, kabızlık, boynunu tutamama, göz kapaklarında düşme (ptozis) ve genel kas gevşekliği saptanıyor.",
                "Bu vakada acil düşünülmesi gereken klinik tanı ve etiyolojik mekanizma hangisidir?",
                [
                    {
                        "text": "İnfantil Botulizm: Bal içindeki Clostridium botulinum sporlarının kolonda toksin salgılaması",
                        "isCorrect": True,
                        "feedback": "Doğru Klinik Teşhis: 1 yaş altı bal tüketimi İnfantil Botulizmin klasik nedenidir; asetilkolin salınımı bloke olur ve gevşek paralizi gelişir."
                    },
                    {
                        "text": "Akut Bakla Zehirlenmesi (Favizm)",
                        "isCorrect": False,
                        "feedback": "Hatalı: Favizm bakla alımıyla tetiklenen hemolitik krizdir; bal infantil botulizme yol açar."
                    },
                    {
                        "text": "İnek Sütü Alerjisi Proktokoliti",
                        "isCorrect": False,
                        "feedback": "Hatalı: Proktokolit kanlı dışkılama yapar, hipotonik felç yapmaz."
                    }
                ]
            )
        ]
    })

    # Slayt 89: [TEKRAR SAYFASI - CHECKPOINT 9] Tamamlayıcı Beslenme Zamanlaması ve İlkeleri
    slides.append({
        "id": "k1-22-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Tamamlayıcı Beslenme Zamanlaması ve İlkeleri",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 89,
        "narrative": (
            "Bu checkpoint sayfasında, tamamlayıcı beslenmenin zamanlama biyolojisini, püre kıvamını ve yasak besinleri mühürlüyoruz: "
            "1. **Başlama Eşiği:** Tam 6. ayda (180. günde) başlanır. Anne sütü kesilmez; 6-12 ayda enerjinin %50'si anne sütünden gelir. "
            "2. **Başlama Gerekçesi:** ~200 kcal enerji açığı ve 4-6. ayda tükenen fetal demir ve çinko rezervlerinin kapatılmasıdır. "
            "3. **Erken Başlama Tehlikesi:** Ekstrüzyon refleksi aspirasyon yapar; açık bağırsak alerjiye yol açar; amilaz yetersizdir. "
            "4. **Geç Başlama Tehlikesi:** 8. aydan sonra çiğnemenin kritik nöromotor penceresi kaçar ve pütürlü gıda reddi yerleşir. "
            "5. **3 Gün Kuralı:** Her yeni besin tek tek tanıtılır; alerji için 3 gün beklenir. "
            "6. **Yasak Besinler:** Bal (botulizm), inek sütü (mikrokanama/anemi), sofra tuzu, şeker, bakla (favizm) 1 yaşına kadar kesinlikle yasaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "flashcards": [
            make_flashcard(
                "k1-22-fc-s89-1",
                "Term doğan sağlıklı bebeklerde intrauterin depolanan fetal demir rezervi yaklaşık kaçıncı aylarda tükenir?",
                "Yaklaşık dördüncü ile altıncı aylarda tükenir.",
                "Ek gıda başlama eşiğine denk gelen hepatik rezerv boşalma aralığı",
                "Depo Biyokimyası"
            ),
            make_flashcard(
                "k1-22-fc-s89-2",
                "Bir yaşından küçük bebeklere bal verilmesinin kesinlikle yasak olmasının altında yatan mikrobiyolojik patoloji nedir?",
                "Clostridium botulinum sporlarının gastrointestinal kanalda toksin üreterek infantil botulizme yol açmasıdır.",
                "Gevşek bebek tablosu yaratan anaerobik mikrobiyal felç zehiri",
                "Toksikoloji ve Güvenlik"
            ),
            make_flashcard(
                "k1-22-fc-s89-3",
                "Glukoz-6-fosfat dehidrogenaz (G6PD) enzim eksikliği olan süt çocuklarında favizme bağlı akut hemolizi tetikleyen yasak bakliyat hangisidir?",
                "Bakla bakliyatıdır.",
                "Akdeniz anemisi krizini tetikleyen taze fasulye benzeri yeşil tohum",
                "Metabolik Kontrendikasyonlar"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tamamlayıcı Beslenmede Kritik Zamanlama ve Uygulama Tablosu",
                ["Beslenme Evresi", "Doğru Uygulama Zamanı", "Klinik Gerekçe / Tehlike"],
                [
                    ["İlk 6 Ay (0-180 Gün)", "Yalnızca anne sütü", "Mukozal zırh ve enfeksiyon koruması"],
                    [
                        "Ek Gıdaya Başlama",
                        {"text": "Tam 180. gün (6. ay)", "isMasked": True, "hint": "Enerji açığının ve demir ihtiyacının başladığı dönüm noktası"},
                        "Demir depolarının tükenmesi ve enerji açığı"
                    ],
                    ["Pütürlüye Geçiş", "7 - 8. ay arası", "Çiğneme kritik penceresini kaçırmama"],
                    ["Bal ve İnek Sütü", "1 yaşından sonra", "İnfantil botulizm ve mikrokanama önleme"]
                ]
            )
        ]
    })

    # Slayt 90: Bölüm Özeti: Tamamlayıcı Beslenmeden Malnütrisyon ve Büyük Özete Geçiş
    slides.append({
        "id": "k1-22-s90",
        "title": "Bölüm Özeti: Tamamlayıcı Beslenmeden Malnütrisyon ve Büyük Özete Geçiş",
        "section": "Tamamlayıcı (Ek) Beslenmeye Geçiş İlkeleri ve Gelişimsel Eşikler",
        "slideNumber": 90,
        "narrative": (
            "Tamamlayıcı beslenme, anne sütünün koruyucu şemsiyesi altında bebeğin metabolik, immünolojik ve oral motor olgunlaşmasını sağlayan köprüdür. "
            "6. ayda başlayan bu süreç; enerji açığını kapatırken demir ve çinko depolarını tazeler. "
            "Ekstrüzyon refleksinin gerilemesi, çatalla ezilmiş püreler, 3 gün kuralı ve 1 yaş yasakları (bal, inek sütü, tuz, bakla) "
            "çocuğun sağlıklı erişkin beslenme temellerini kurar. "
            "Ancak beslenmenin yetersiz kaldığı, tamamlayıcı gıdaların hijyensiz veya kaloriden yoksun olduğu durumlarda "
            "çocuk hızla yıkıcı bir patolojik girdaba sürüklenir: "
            "Son bölümümüzde, bebek beslenmesinin klinik zirvesi olan **'Çocukluk Çağı Malnütrisyonu (Marasmus, Kvaşiorkor), "
            "Mikro Besin Eksiklikleri, BLW Yöntemi ve Büyük Kurs Özeti'** konularını ele alarak dersimizi tamamlayacağız."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_active_recall(
                "Tamamlayıcı beslenmeye geçiş sürecinde annelere verilecek en temel üç pediatrik kural nedir?",
                "Tam 6. ayda başlanması, besinlerin çatalla ezilerek 3 gün kuralıyla tanıtılması ve 1 yaşına kadar bal ile inek sütünün kesin yasak olmasıdır.",
                "Zamanlama, püre kıvamı ve yasak gıdalar"
            ),
            make_branching_logic(
                "Sağlık ocağına getirilen 7 aylık bir bebeğin annesi, bebeğe her gün pirinç ununu tam inek sütü ve bol bal ile pişirip biberonla içirdiğini belirtiyor.",
                "Bu beslenme modelindeki en ölümcül tıbbi hatalar ve hekimin acil müdahalesi ne olmalıdır?",
                [
                    {
                        "text": "Bal (infantil botulizm riski) ve inek sütü (bağırsak kanaması ve böbrek yükü) derhal kesilmeli, biberon yerine kaşıkla çatalla ezilmiş sebze/yoğurt pürelerine ve anne sütüne geçilmelidir",
                        "isCorrect": True,
                        "feedback": "Mükemmel Müdahale: Bal ölümcül botulizm riski taşır, inek sütü 1 yaşından önce yasaktır; besin kaşıkla verilmelidir."
                    },
                    {
                        "text": "Biberon deliğini genişletip karışıma biraz tuz ve zeytinyağı eklemesini önermek",
                        "isCorrect": False,
                        "feedback": "Hatalı ve Tehlikeli: Tuz böbrekleri iflas ettirir, bal ve inek sütü tehlikesi devam eder."
                    },
                    {
                        "text": "Bal miktarını azaltıp pirinç unu yerine buğday nişastası kullanmasını söylemek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Balın azı da ölümcüldür, inek sütü tehlikesi çözülmemiştir."
                    }
                ]
            )
        ]
    })

    return slides
