# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 1: Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler (Slayt 1 - 10)
Checkpoint 1: Slayt 9
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # Slayt 1: Bebek Beslenmesinin Halk Sağlığı Açısından Önemi ve Yaşamın İlk 1000 Günü
    slides.append({
        "id": "k1-22-s01",
        "title": "Bebek Beslenmesinin Halk Sağlığı Açısından Önemi ve Yaşamın İlk 1000 Günü",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 1,
        "narrative": (
            "Bebeklik dönemi, insan yaşamında büyüme ve nörogelişimin en hızlı gerçekleştiği evredir. "
            "Gebelikte fetüsün anne karnına düşmesinden çocuğun 2 yaşını tamamlamasına kadar geçen yaklaşık "
            "**1000 günlük süre (İlk 1000 Gün)**, insan metabolizmasının, bağışıklık sisteminin ve beyin mimarisinin "
            "programlandığı en kritik penceredir. "
            "Bu dönemdeki beslenme yetersizlikleri veya hataları, ileriki yaşlarda bodurluk, düşük bilişsel kapasite, "
            "okul başarısızlığı ve erişkin dönemde tip 2 diyabet, hipertansiyon ve obezite gibi kronik metabolik hastalıklara "
            "zemin hazırlar. "
            "Halk sağlığı açısından bebek beslenmesine yapılan her yatırım, hem çocuk ölümlerini dramatik biçimde azaltır "
            "hem de toplumun genel refahını ve ekonomik üretkenliğini doğrudan yükseltir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne karnından 2 yaşın sonuna kadar süren ve metabolik programlamanın temelini oluşturan kritik döneme ilk 1000 gün denir.",
                "ilk 1000 gün",
                "Gebelikte başlayan ve ikinci yaş bittiğinde tamamlanan zaman dilimi"
            ),
            make_causal_chain(
                "İlk 1000 Gün Beslenmesinin Metabolik Programlama Zinciri",
                [
                    "1. Erken Beslenme: Fetal ve erken bebeklik döneminde anne sütüyle ideal makro besin sağlanır.",
                    "2. Epigenetik Düzenleme: DNA metilasyonu ve metabolik enzim genleri fizyolojik ayarlanır.",
                    "3. Sağlıklı Matürasyon: Beyin dokusu, adipsit hacmi ve pankreas beta hücreleri orantılı olgunlaşır.",
                    "4. Uzun Dönem Koruma: Erişkin çağda obezite, insülin direnci ve ateroskleroz gelişimi önlenir."
                ]
            ),
            make_active_recall(
                "Yaşamın ilk 1000 günündeki yetersiz beslenmenin yetişkinlik dönemindeki en tehlikeli kronik metabolik sonuçları nelerdir?",
                "Obezite, Tip 2 Diabetes Mellitus, esansiyel hipertansiyon ve koroner arter hastalığı gibi kardiyovasküler patolojilerdir.",
                "Metabolik sendrom ve kronik damar hastalıkları riskleri"
            )
        ]
    })

    # Slayt 2: Dünyada Çocuk Beslenmesi Göstergeleri: Bodurluk, Çelimsizlik ve Obezite
    slides.append({
        "id": "k1-22-s02",
        "title": "Dünyada Çocuk Beslenmesi Göstergeleri: Bodurluk, Çelimsizlik ve Obezite",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 2,
        "narrative": (
            "Dünya Sağlık Örgütü (DSÖ) verilerine göre küresel çapta beş yaş altı çocuk popülasyonunda "
            "beslenme bozuklukları halen en büyük morbidite nedenlerindendir. "
            "Epidemiyolojik çalışmalarda üç temel yetersiz ve dengesiz beslenme göstergesi izlenir: "
            "1. **Bodurluk (Stunting - Yaşa Göre Kısa Boy):** Kronik ve uzun süreli yetersiz beslenmenin, tekrarlayan enfeksiyonların "
            "ve sosyoekonomik yoksunluğun kesin göstergesidir; dünyada yaklaşık **150 milyon çocuk** bu durumdadır. "
            "2. **Çelimsizlik / Zayıflık (Wasting - Boya Göre Düşük Kilo):** Akut ve şiddetli açlığın, ani kalori yoksunluğunun veya "
            "ağır ishal/pnömoni atağının göstergesidir; dünyada yaklaşık **43 milyon çocuk** akut ölüm riskiyle karşı karşıyadır. "
            "3. **Aşırı Kilo ve Şişmanlık (Overweight):** Dünyada yaklaşık **36 milyon çocuk** yanlış formül mama veya şekerli besinlerle "
            "erken çocukluk obezitesine sürüklenmektedir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Kronik yetersiz beslenme ve sık enfeksiyonlar sonucu yaşa göre boyun yetersiz kalmasına bodurluk veya stunting adı verilir.",
                "bodurluk",
                "Uzun erimli besin eksikliğine bağlı boy güdükleşmesi"
            ),
            make_table(
                "Küresel Çocuk Beslenmesi Epidemiyolojik Göstergeleri",
                ["Beslenme Göstergesi", "Antropometrik Ölçüt", "Yansıttığı Patoloji", "Dünya Genelinde Vaka Sayısı"],
                [
                    ["Bodurluk (Stunting)", "Yaşa göre kısa boy", "Kronik yetersiz beslenme ve yoksulluk", "~150 milyon çocuk"],
                    [
                        "Çelimsizlik (Wasting)",
                        "Boya göre düşük ağırlık",
                        {"text": "Akut açlık ve ağır enfeksiyon kaybı", "isMasked": True, "hint": "Ani gelişen kalori ve sıvı yıkımı tablosu"},
                        "~43 milyon çocuk"
                    ],
                    ["Aşırı Kilo (Overweight)", "Yaşa ve boya göre yüksek kilo", "Dengesiz aşırı kalori ve erken obezite", "~36 milyon çocuk"]
                ]
            ),
            make_micro_quiz(
                "Beş yaş altı çocuk beslenmesi göstergeleri ile ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?",
                {
                    "A": "Bodurluk (Stunting) - Yaşa göre boyun persentilin çok altında kalması",
                    "B": "Çelimsizlik (Wasting) - Boya göre ağırlığın akut şekilde yetersiz olması",
                    "C": "Bodurluk - Akut bir haftalık ishal atağının anlık sonucu",
                    "D": "Çelimsizlik - Akut açlık ve yüksek ölüm riski taşıyan şiddetli tablo",
                    "E": "Aşırı Kilo - Erken dönemde uygunsuz beslenme sonucu 36 milyon çocuğu etkileyen yük"
                },
                "C",
                "Doğru cevap C'dir: Bodurluk (stunting) bir haftalık akut ishal atağıyla oluşamaz; aylar ve yıllar süren kronik yetersiz beslenmenin ve sosyoekonomik geri kalmışlığın kümülatif sonucudur. Akut kilo kayıpları ise çelimsizlik (wasting) oluşturur."
            )
        ]
    })

    # Slayt 3: Çocuk Ölümleri ve Yetersiz Beslenme İlişkisi: DSÖ ve UNICEF Verileri
    slides.append({
        "id": "k1-22-s03",
        "title": "Çocuk Ölümleri ve Yetersiz Beslenme İlişkisi: DSÖ ve UNICEF Verileri",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 3,
        "narrative": (
            "Dünya Sağlık Örgütü (DSÖ) ve UNICEF'in küresel mortalite analizleri, çocuk sağlığında sarsıcı bir gerçeği belgeler: "
            "Dünyadaki tüm 5 yaş altı çocuk ölümlerinin **yaklaşık yarısı (%45-50'si) doğrudan veya dolaylı olarak yetersiz beslenmeyle ilişkilidir**! "
            "Beslenme yetersizliği olan çocukta timus atrofisi, lenfopeni, epitel bütünlüğünün bozulması ve fagositoz yetmezliği gelişir; "
            "bu nedenle normal bir çocukta hafif geçen pnömoni veya ishal atağı, malnütrisyonlu çocukta süratle fatal seyreder. "
            "**En Ucuz ve En Etkili Hayat Kurtarıcı Müdahale:** "
            "Tüm bebeklerin ilk 6 ay sadece anne sütüyle beslenmesi ve 2 yaşına kadar emzirmenin sürdürülmesi durumunda, "
            "dünya genelinde her yıl **400.000'den fazla 5 yaş altı çocuk ölümünün önüne geçilebileceği** hesaplanmaktadır. "
            "Buna rağmen dünyada ilk 6 ay sadece anne sütü alabilen bebek oranı henüz %44-47 düzeyindedir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Dünya genelinde 5 yaş altı çocuk ölümlerinin yaklaşık yarısı doğrudan veya dolaylı olarak yetersiz beslenme ile bağlantılıdır.",
                "yetersiz beslenme",
                "Pediatrik mortaliteyi tetikleyen besin ve kalori kıtlığı tablosu"
            ),
            make_before_after(
                "Yetersiz Beslenme ve Optimal Anne Sütü Mortalite Kıyası",
                "Yetersiz Beslenme Etkisi",
                "Dünyadaki 5 yaş altı çocuk ölümlerinin %50'sine zemin hazırlar; basit enfeksiyonları ölümcül sepsis ve pnömoniye çevirir.",
                "Optimal Emzirme Koruyuculuğu",
                "İlk 6 ay tek başına anne sütü ve 2 yıl emzirme ile yılda 400.000'den fazla çocuğun hayatı kurtarılabilir.",
                "Çocuk ölümlerini tetikleyen malnütrisyon ile hayat kurtarıcı emzirmenin halk sağlığı gücü"
            ),
            make_active_recall(
                "DSÖ ve UNICEF verilerine göre ilk 6 ay yalnız anne sütü ve 2 yaşına kadar emzirme ile yılda kaç çocuk ölümü önlenebilir?",
                "Yılda yaklaşık 400.000 (dört yüz bin) beş yaş altı çocuk ölümü önlenebilir.",
                "Yüz binlerle ifade edilen yıllık önlenebilir çocuk ölümü sayısı"
            )
        ]
    })

    # Slayt 4: Bebek Ölüm Hızı (BÖH): Tanımı, Hesaplama Formülü ve Anlamı
    slides.append({
        "id": "k1-22-s04",
        "title": "Bebek Ölüm Hızı (BÖH): Tanımı, Hesaplama Formülü ve Anlamı",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 4,
        "narrative": (
            "Halk sağlığında bir ülkenin veya bölgenin gelişmişlik düzeyini, anne-çocuk sağlığı hizmetlerinin kalitesini, "
            "beslenme durumunu ve çevre sağlığını en duyarlı yansıtan altın standart gösterge **Bebek Ölüm Hızıdır (BÖH)**. "
            "**Matematiksel Formülü:** "
            "BÖH = (Bir takvim yılında 1 yaşını doldurmadan ölen bebek sayısı / Aynı yıldaki canlı doğum sayısı) × 1000. "
            "BÖH binde (‰) olarak ifade edilir. "
            "Bir yaşından küçük bebekler enfeksiyonlara, beslenme hatalarına, hijyen yetersizliklerine ve bakım ihmaline "
            "karşı biyolojik olarak en hassas gruptur. "
            "Gelişmiş ülkelerde BÖH binde 2 ila 4 düzeyindeyken, az gelişmiş ülkelerde binde 50 ila 80'in üzerindedir. "
            "Anne sütünün yaygınlaştırılması ve doğru bebek beslenmesi politikaları, BÖH'ü düşürmenin bir numaralı aracıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bir yılda bir yaşını doldurmadan ölen bebek sayısının canlı doğum sayısına bölünüp 1000 ile çarpılmasına bebek ölüm hızı denir.",
                "bebek ölüm hızı",
                "Toplum gelişmişliğini ölçen binde bazlı pediatrik gösterge"
            ),
            make_causal_chain(
                "Bebek Beslenmesinin Bebek Ölüm Hızını (BÖH) Düşürme Mekanizması",
                [
                    "1. Erken Emzirme: Doğumdan hemen sonra kolostrum alan bebekte mukozal sIgA kalkanı kurulur.",
                    "2. Enfeksiyon Bariyeri: Bebek ishal ve pnömoni gibi ölümcül enfeksiyonlardan korunur.",
                    "3. Optimal Büyüme: Boy ve kilo artışı persentil eğrisine paralel ilerler; malnütrisyon engellenir.",
                    "4. Mortalite Düşüşü: 0-1 yaş arası ölümler geriler ve toplumun BÖH göstergesi belirgin düşer."
                ]
            ),
            make_micro_quiz(
                "Bebek Ölüm Hızı (BÖH) hesaplaması ve epidemiyolojik anlamı ile ilgili hangisi doğrudur?",
                {
                    "A": "Paydada o yıldaki toplam kadın nüfusu, payda ise ölen 5 yaş altı çocuk sayısı yer alır",
                    "B": "Yalnızca hastanede doğan ve ilk 28 günde ölen bebekleri kapsar",
                    "C": "Bir takvim yılında 1 yaşını doldurmadan ölen bebeklerin o yıldaki canlı doğumlara oranının 1000 ile çarpımıdır",
                    "D": "Toplumun sosyoekonomik refahıyla hiçbir ilişkisi olmayan tesadüfi bir orandır",
                    "E": "Sonuç yüzdelik (%) olarak hesaplanır ve binde çarpanı kullanılmaz"
                },
                "C",
                "Doğru cevap C'dir: BÖH formülü gereği payda 1 yaşını bitirmeden ölen bebekler, paydada aynı yıldaki toplam canlı doğum sayısı yer alır ve binde (1000 ile) çarpılır. Gelişmişliğin en hassas aynasıdır."
            )
        ]
    })

    # Slayt 5: Türkiye'de Bebek Beslenmesi Durumu: TNSA Verileri
    slides.append({
        "id": "k1-22-s05",
        "title": "Türkiye'de Bebek Beslenmesi Durumu: TNSA Verileri",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 5,
        "narrative": (
            "Türkiye Nüfus ve Sağlık Araştırması (TNSA) verileri, ülkemizde bebek beslenmesi uygulamalarında "
            "hem sevindirici gelişmelerin hem de acil müdahale gerektiren aksaklıkların bir arada olduğunu ortaya koymaktadır. "
            "**TNSA Öne Çıkan Beslenme Bulguları:** "
            "- **Erken Emzirme:** İki yaş altı çocukların **%71'i doğumdan sonraki ilk 1 saat içinde emzirmeye başlatılmıştır**. "
            "Erken emzirme oranı kentsel bölgelerde (%73), kırsal bölgelere (%67) göre daha yüksektir ve annenin eğitim düzeyi arttıkça yükselmektedir. "
            "- **Sadece Anne Sütü (Exclusive):** 6 aydan küçük bebeklerin **yalnızca %41'i sadece anne sütü** alabilmektedir. "
            "Daha da kritik olan bulgu: Sadece anne sütü alan bebeklerde bu uygulamanın **ortanca süresi yalnızca 1.8 aydır**! "
            "Anneler sütlerinin yetmediği endişesiyle veya kültürel baskılarla bebeklerine erken dönemde su, çay veya formül mama başlamaktadır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de TNSA verilerine göre 6 aydan küçük bebeklerin sadece anne sütü alma ortanca süresi 1,8 aydır.",
                "1,8 aydır",
                "İki aydan daha kısa süren Türkiye ortanca emzirme süresi"
            ),
            make_table(
                "Türkiye Nüfus ve Sağlık Araştırması (TNSA) Temel Emzirme İstatistikleri",
                ["Beslenme Göstergesi / Parametre", "TNSA Türkiye Değeri", "Halk Sağlığı Hedefi / Yorumu"],
                [
                    ["İlk 1 saatte emzirmeye başlama oranı", "%71 (Kırsal %67, Kent %73)", "Her doğumda ilk 30-60 dakikada emzirme hedeflenir"],
                    [
                        "6 aydan küçüklerde sadece anne sütü oranı",
                        {"text": "%41", "isMasked": True, "hint": "Yarıdan daha az olan Türkiye yalnız anne sütü yüzdesi"},
                        "İlk 6 ayda %100 sadece anne sütü hedeflenir"
                    ],
                    ["Sadece anne sütü alma ortanca süresi", "1.8 ay", "Erken ek gıda ve su başlama hatalarını yansıtır"],
                    ["0-23 aylık bebeklerde biberon kullanım oranı", "%53", "Biberon meme başı şaşkınlığı ve enfeksiyon yapar"]
                ]
            ),
            make_active_recall(
                "Türkiye'de TNSA verilerine göre çocukların ilk 1 saatte emzirilme oranı kentsel ve kırsal bölgelerde nasıldır?",
                "Kentsel bölgelerde %73, kırsal bölgelerde %67'dir; genel Türkiye ortalaması ise %71'dir ve annenin eğitim seviyesi arttıkça yükselir.",
                "Kent ve kır arasındaki emzirme yüzdesi farkı"
            )
        ]
    })

    # Slayt 6: Prelakteal Beslenme Tehlikesi: Anne Sütünden Önce Verilen Sıvılar
    slides.append({
        "id": "k1-22-s06",
        "title": "Prelakteal Beslenme Tehlikesi: Anne Sütünden Önce Verilen Sıvılar",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 6,
        "narrative": (
            "**Prelakteal beslenme**, yenidoğan bebeğe doğumdan sonra anne memesine tutulup anne sütü verilmeden ÖNCE "
            "herhangi bir sıvı veya gıdanın (şekerli su, zemzem suyu, çay, formül mama, inek sütü veya bal) verilmesidir. "
            "TNSA verilerine göre Türkiye'de çocukların **%42'si prelakteal besin almaktadır**; bu oran halk sağlığı açısından vahim bir tehdittir! "
            "**Prelakteal Beslenmenin Yarattığı Ağır Riskler:** "
            "1. **Emme Refleksinin Körelmesi:** Şekerli su veya biberon alan bebek tokluk hisseder, memeyi güçlü emmez ve anne sütü uyarımı gecikir. "
            "2. **Kolostrumun Ziyan Edilmesi:** İlk saatlerdeki altın değerindeki immünolojik aşı (kolostrum) bebek tarafından alınamaz. "
            "3. **Enfeksiyon Riski:** Steril olmayan sular ve biberonlar steril bebek bağırsağına patojen bakterileri eker. "
            "4. **Alerji Duyarlılaşması:** İnek sütü bazlı mamalar yabancı protein alerjilerini (inek sütü alerjisi) tetikler."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğana ilk anne sütü verilmeden önce şekerli su veya mama verilmesi uygulamasına prelakteal beslenme adı verilir.",
                "prelakteal beslenme",
                "Emzirme başlatılmadan önce dışarıdan sıvı verilmesi adeti"
            ),
            make_before_after(
                "Prelakteal Sıvı Verme ile Doğrudan Memeye Tutma Kıyaslaması",
                "Prelakteal Sıvı Verme (Hatalı)",
                "Bebek tokluk hissiyle memeyi reddeder, kolostrum ziyan olur, patojen bakteri bulaşır ve süt üretimi baskılanır.",
                "Doğrudan Memeye Tutma (Doğru)",
                "Bebek ilk 30-60 dakikada emer; oksitosin ve prolaktin salınarak süt iner, bağışıklık kalkanı kurulur.",
                "Yenidoğanda zararlı erken sıvı verme ile hayat kurtarıcı erken emzirmenin zıt sonuçları"
            ),
            make_micro_quiz(
                "Prelakteal beslenme (anne sütünden önce başka sıvı/besin verilmesi) ile ilgili aşağıdakilerden hangisi yanlıştır?",
                {
                    "A": "Bebeğin tokluk hissetmesine ve anneyi istekle emmemesine yol açar",
                    "B": "Türkiye'de çocukların yaklaşık %42'sinde görülmektedir",
                    "C": "Kolostrumun içerdiği koruyucu antikorların alınmasını geciktirir",
                    "D": "Yenidoğanın steril bağırsak mukozasında alerjen ve enfeksiyon riskini artırır",
                    "E": "Süt yapımını hızlandıran ve bebeğin kilo kaybını tamamen önleyen faydalı bir uygulamadır"
                },
                "E",
                "Doğru cevap E'dir: Prelakteal beslenme kesinlikle faydalı değildir; aksine meme uyarımını durdurarak anne sütünün inmesini geciktirir, enfeksiyon ve alerji riskini katlar. Tıbben kesinlikle yasaklanması gereken bir gelenektir."
            )
        ]
    })

    # Slayt 7: Yalnız Anne Sütü Alma Dinamikleri ve Biberon Kullanım Sorunu
    slides.append({
        "id": "k1-22-s07",
        "title": "Yalnız Anne Sütü Alma Dinamikleri ve Biberon Kullanım Sorunu",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 7,
        "narrative": (
            "Dünya Sağlık Örgütü ve Sağlık Bakanlığı, bebeklerin **ilk 6 ay boyunca SADECE anne sütü (Exclusive Breastfeeding)** "
            "almasını şart koşar. 'Sadece anne sütü', bebeğe anne sütü dışında su, çay, meyve suyu dahil hiçbir ek sıvı veya katı "
            "gıda verilmemesi anlamına gelir (yalnızca hekimin önerdiği vitamin ve mineral damlaları hariçtir). "
            "Ülkemizde 0-23 aylık bebeklerin **%53'ünde biberon kullanıldığı** tespit edilmiştir. "
            "**Biberon Kullanımının 3 Temel Sakıncası:** "
            "1. **Meme Başı Şaşkınlığı (Nipple Confusion):** Biberondan süt akıtmak için bebeğin çaba harcaması gerekmez; "
            "memeyi emmek ise dil, damak ve çene kaslarının koordineli negatif basınç oluşturmasını gerektirir. "
            "Biberona alışan bebek anne memesini yorucu bularak reddeder. "
            "2. **Ağız ve Çene Bozuklukları:** Biberon ve yalancı emzikler damak kubbesini derinleştirir ve diş oklüzyonunu bozar. "
            "3. **Enfeksiyon Yuvası:** Biberon emzikleri mikroorganizmaların biyofilm oluşturması için mükemmel ortamlardır; "
            "yetersiz sterilizasyon ölümcül gastroenterit salgınlarına yol açar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Biberondan zahmetsiz süt akışına alışan bebeğin anne memesini kavramayı reddetmesi durumuna meme başı şaşkınlığı denir.",
                "meme başı şaşkınlığı",
                "Yapay emzik kullanımı sonucu göğsü kavramayı terk etme hali"
            ),
            make_causal_chain(
                "Biberon Kullanımının Anne Sütünü Sonlandırma Kaskadı",
                [
                    "1. Biberon Verilmesi: Anne sütü veya mama kauçuk/silikon emzikle sunulur.",
                    "2. Kolay Akış: Bebek efor sarf etmeden yerçekimiyle gelen süte alışır.",
                    "3. Memeyi Reddetme: Anne memesindeki vakum emeği bebeğe zor gelir; bebek ağlayarak memeden kaçar.",
                    "4. Uyarım Kaybı: Meme boşaltılamayınca prolaktin ve oksitosin salınımı durur; süt kesilir."
                ]
            ),
            make_branching_logic(
                "Doğumdan sonra 2. haftada olan bir anne, bebeğine su vermek için biberon aldığını belirtiyor. Aile hekiminin anneye vermesi gereken en doğru kanıta dayalı tıbbi yaklaşım hangisidir?",
                [
                    {
                        "text": "İlk 6 ay anne sütü alan bebeğin su dahil hiçbir ek sıvıya ihtiyacı yoktur; biberon meme başı şaşkınlığı yaparak emzirmeyi bitirebileceğinden biberon kesinlikle kullanılmamalıdır.",
                        "isCorrect": True,
                        "explanation": "Doğru. Anne sütünün %87'si sudur ve en sıcak çöl ikliminde bile bebeğin tüm sıvı ihtiyacını eksiksiz karşılar. Biberon kullanımı ise memeyi bırakmanın en sık nedenidir."
                    },
                    {
                        "text": "Bebekler yazın susar, bu nedenle her emzirme sonrası bir biberon kaynatılmış ılık su verilmelidir.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Anne sütü alan bebeğe su verilmesi mide hacmini doldurarak süt alımını azaltır ve hiponatremi riski yaratır."
                    },
                    {
                        "text": "Biberon çene kaslarını daha çok geliştirdiği için günde en az iki kez biberonla besleme yapılmalıdır.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Biberon çene kaslarını tembelleştirir ve maloklüzyon yapar; anne memesi çene gelişimini doğal destekler."
                    }
                ]
            )
        ]
    })

    # Slayt 8: Bebek Beslenmesinin Temel Amaçları: Büyüme, Gelişme ve Bağlanma
    slides.append({
        "id": "k1-22-s08",
        "title": "Bebek Beslenmesinin Temel Amaçları: Büyüme, Gelişme ve Bağlanma",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 8,
        "narrative": (
            "Bebek beslenmesi yalnızca biyolojik kalori ve gram hesabı yapılan mekanik bir süreç değildir; "
            "pediatrik tıp ve halk sağlığı açısından dört temel stratejik hedefi kapsar: "
            "1. **Büyüme ve Gelişmeyi Desteklemek:** Hücresel hiperplazi ve hipertrofi için gerekli aminoasit, "
            "esansiyel yağ asidi ve mikro besinleri sunarak gelecekteki erişkin sağlığını garantiye almak. "
            "2. **Anne-Bebek Bağlanmasını (Bonding) Güçlendirmek:** Emzirme sırasında salgılanan maternal oksitosin hormonu "
            "ve kurulan göz-ten teması, bebeğin temel güven duygusunun ve duygusal zekasının temel taşını oluşturur. "
            "3. **Yeme Becerilerini ve Oral Motor Koordinasyonu Geliştirmek:** Zamanı geldiğinde yeni lezzet ve kıvamlarla "
            "tanışarak çiğneme, yutma ve dil koordinasyonunu geliştirmek. "
            "4. **Besinlere Karşı Pozitif Tutum Geliştirmek:** Zorlamadan, sevgi dolu ve bebeğin tokluk ipuçlarına saygılı "
            "bir beslenme ortamı sağlayarak ömür boyu sürecek sağlıklı yeme alışkanlığı kazandırmak."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Emzirme sırasında kurulan ten ve göz teması oksitosin salınımını tetikleyerek anne-bebek bağlanmasını güçlendirir.",
                "oksitosin salınımını",
                "Bağlanma ve süt fışkırtma refleksini yöneten nörohormon yanıtı"
            ),
            make_table(
                "Bebek Beslenmesinin Bütüncül Boyutları ve Beklenen Kazanımlar",
                ["Beslenme Boyutu", "Sağlanan Fizyolojik / Psikolojik Mekanizma", "Uzun Dönemli Klinik Kazanım"],
                [
                    ["Biyolojik Büyüme", "Yeterli kalori, esansiyel yağ asitleri ve mikro besin sunumu", "Persentil eğrisinde ideal boy ve kilo artışı"],
                    [
                        "Duygusal Bağlanma",
                        {"text": "Ten tene temas ve maternal oksitosin uyarımı", "isMasked": True, "hint": "Sevgi ve güven hormonunun cilt dokunuşuyla aktivasyonu"},
                        "Güvenli bağlanma ve azalmış çocukluk kaygısı"
                    ],
                    ["Oral-Motor Gelişim", "Meme emme ve ardından püre/parmak gıda çiğneme koordinasyonu", "Düzgün diş gelişimi ve net konuşma artikülasyonu"],
                    ["Davranışsal Tutum", "Bebeğin tokluk sinyallerine saygılı duyarlı besleme", "Erişkin dönemde yeme bozukluklarından korunma"]
                ]
            ),
            make_active_recall(
                "Bebek beslenmesinin salt kalori alımının ötesinde anne-bebek ilişkisine en büyük psikososyal katkısı nedir?",
                "Ten tene temas ve oksitosin salınımı aracılığıyla güvenli anne-bebek bağlanmasını (attachment/bonding) sağlaması ve bebeğin temel güven duygusunu inşa etmesidir.",
                "Güvenli bağlanma ve duygusal gelişim katkısı"
            )
        ]
    })

    # Slayt 9: [TEKRAR SAYFASI - CHECKPOINT 1] Bebek Beslenmesinde Epidemiyoloji ve Göstergeler
    slides.append({
        "id": "k1-22-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Bebek Beslenmesinde Epidemiyoloji ve Göstergeler",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 9,
        "narrative": (
            "Bu birinci checkpoint sayfasında, bebek beslenmesinin küresel ve ulusal halk sağlığı boyutunu "
            "özetleyen temel kavramları pekiştiriyoruz: "
            "1. **İlk 1000 Gün:** Gebelikten 2 yaşın sonuna kadar süren metabolik ve nörolojik programlama penceresidir. "
            "2. **Bodurluk (Stunting):** Yaşa göre kısa boy olup kronik yetersiz beslenmenin ve yoksulluğun aynasıdır (~150 milyon çocuk). "
            "3. **Çelimsizlik (Wasting):** Boya göre düşük ağırlık olup akut açlığı ve ölümcül enfeksiyon kaybını simgeler (~43 milyon çocuk). "
            "4. **Bebek Ölüm Hızı (BÖH):** Bir yıldaki 1 yaş altı ölümlerin canlı doğumlara oranının binde çarpanıdır; toplumun en hassas sağlık aynasıdır. "
            "5. **TNSA ve Prelakteal Beslenme:** Türkiye'de ilk 1 saatte emzirme %71 iken, %42 prelakteal besin alma ve %53 biberon kullanımı emzirmeyi tehdit eden kritik tablolardır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "k1-22-fc-01",
                "Bir toplumda belirli bir yılda 1 yaşını doldurmadan ölen bebek sayısının aynı yıldaki canlı doğum sayısına bölünüp 1000 ile çarpılmasıyla hesaplanan temel halk sağlığı göstergesi nedir?",
                "Bebek Ölüm Hızı (BÖH)",
                "Toplumun sosyoekonomik refahını ve sağlık hizmet kalitesini yansıtan binde oran",
                "Epidemiyoloji"
            ),
            make_flashcard(
                "k1-22-fc-02",
                "Çocuklarda kronik yetersiz beslenmenin göstergesi olan ve yaşa göre boyun standart persentilin altında kalması durumuna ne ad verilir?",
                "Bodurluk (Stunting)",
                "Gelişme geriliği sonucu kalıcı boy kısalığı tablosu",
                "Epidemiyoloji"
            ),
            make_flashcard(
                "k1-22-fc-03",
                "Bebeğe doğumdan sonra anne sütü verilmeden önce şekerli su, formül mama veya bal gibi besinlerin verilmesi uygulamasına ne denir?",
                "Prelakteal beslenme",
                "İlk emzirme öncesi yabancı sıvı verme riski",
                "Epidemiyoloji"
            )
        ]
    })

    # Slayt 10: Bölüm Özeti: Epidemiyolojik Göstergelerden Bebek Fizyolojisine Geçiş
    slides.append({
        "id": "k1-22-s10",
        "title": "Bölüm Özeti: Epidemiyolojik Göstergelerden Bebek Fizyolojisine Geçiş",
        "section": "Bebek Beslenmesinin Önemi, Küresel ve Ulusal Göstergeler",
        "slideNumber": 10,
        "narrative": (
            "Bebek beslenmesinin epidemiyolojik çerçevesini kavradıktan sonra, bu gereksinimlerin altında yatan "
            "anatomik ve fizyolojik temelleri incelemek gerekir. "
            "Bebek neden ilk aylarda sadece sıvı anne sütü tolere edebilir? "
            "Neden katı gıdalar veya inek sütü 6 aydan önce verildiğinde böbrek yetmezliği, dehidratasyon ve alerji gelişir? "
            "Bu soruların yanıtı, yenidoğan ve süt çocuğunun sindirim sistemi, böbrek konsantrasyon kapasitesi ve "
            "vücut bileşiminin hızla değişen dinamiklerinde yatmaktadır. "
            "İkinci bölümümüzde, bebeklikteki ağırlık ve boy artış dönüm noktaları, mide kapasitesinin 10 ml'den 250 ml'ye evrilmesi, "
            "enzimatik olgunlaşma ve renal immadürite ilkeleri derinlemesine ele alınacaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bebek beslenmesi stratejilerini belirleyen en temel biyolojik faktör sindirim kanalı ve böbrek fonksiyonlarının immatür olmasıdır.",
                "immatür olmasıdır",
                "Organ sistemlerinin henüz tam olgunlaşmamış bulunması durumu"
            ),
            make_causal_chain(
                "Epidemiyolojiden Organ Fizyolojisine Geçiş Mantığı",
                [
                    "1. Yüksek İhtiyaç: Hızlı büyüme ve kütle katlanması yüksek kalori ve sıvı gerektirir.",
                    "2. Kısıtlı Kapasite: Mide hacmi küçük, sindirim enzimleri ve böbrek fonksiyonu immatürdür.",
                    "3. Mükemmel Uyum: Anne sütü düşük renal solüt yükü ve ideal ozmolariteyle bu açığı kapatır.",
                    "4. Yanlış Besin Riski: Erken verilen inek sütü veya katı gıdalar immatür organları iflasa sürükler."
                ]
            ),
            make_active_recall(
                "Bebek beslenmesinde yetişkin tipi besinlerin erken dönemde tolere edilememesinin iki temel organ sistemi nedeni nedir?",
                "Sindirim sisteminin (gastrik asit, pepsin ve pankreatik enzimler) ve böbrek fonksiyonlarının (düşük glomerüler filtrasyon ve düşük konsantrasyon kapasitesi) immatür olmasıdır.",
                "GİS enzim ve böbrek konsantrasyon yetersizliği"
            )
        ]
    })

    return slides
