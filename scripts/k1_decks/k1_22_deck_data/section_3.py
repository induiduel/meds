# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 3: Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri (Slayt 21 - 30)
Checkpoint 3: Slayt 29
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # Slayt 21: Enerji Gereksinimi ve Büyüme Eğrileri
    slides.append({
        "id": "k1-22-s21",
        "title": "Enerji Gereksinimi ve Büyüme Eğrileri",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 21,
        "narrative": (
            "Süt çocukluğu döneminde günlük enerji harcaması üç temel bileşenden oluşur: "
            "1. **Bazal Metabolizma:** Toplam enerjinin yaklaşık %50'si organların yaşamsal fonksiyonları için harcanır. "
            "2. **Büyüme ve Doku Sentezi:** İlk aylarda toplam kalorinin %25-30'u yeni doku inşası için depolanır. "
            "3. **Fiziksel Aktivite ve Besinlerin Termik Etkisi:** Kalan %20-25'lik dilimi kapsar. "
            "Anne sütü bu gereksinimi mükemmel karşılar; ortalama **30 ml anne sütü 20 kalori (100 ml süt ~67 kcal)** sağlar. "
            "Bebeğin aldığı enerjinin yeterli olup olmadığını anlamanın klinik olarak **en güvenilir ve altın standart yöntemi**, "
            "standart persentil büyüme eğrilerinde boy ve tartı artışının düzenli takip edilmesidir. "
            "Eğride duraklama veya persentil kaybı enerji yetersizliğinin ilk göstergesidir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütü her 30 mililitresinde 20 kalori sağlayarak bebeğin ilk 6 aydaki tüm enerji ihtiyacını eksiksiz karşılar.",
                "20 kalori",
                "Bir ons anne sütünün ürettiği net termal enerji"
            ),
            make_table(
                "Bebeklikte Yaşa Göre Günlük Enerji Gereksinimi",
                ["Yaşam Dönemi", "Ortalama Enerji İhtiyacı (kcal/kg/gün)", "Enerjinin Temel Harcanma Yeri"],
                [
                    ["0 - 3 Ay", "110 - 120 kcal/kg", "Hızlı büyüme ve doku depolaması (%30)"],
                    [
                        "4 - 6 Ay",
                        {"text": "100 - 110 kcal/kg", "isMasked": True, "hint": "Yarım yaş civarındaki kilogram başı kalori bandı"},
                        "Dengeli büyüme ve bazal metabolizma"
                    ],
                    ["7 - 12 Ay", "95 - 100 kcal/kg", "Artan motor aktivite ve emekleme enerjisi"],
                    ["Erişkin Birey", "30 - 35 kcal/kg", "Yalnızca idame ve günlük fiziksel hareket"]
                ]
            ),
            make_micro_quiz(
                "Anne sütünün enerji içeriği ve bebek metabolizması ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "30 ml anne sütü yaklaşık 20 kalori enerji sağlar",
                    "B": "100 ml anne sütünün kalori değeri yaklaşık 67 kilokaloridir",
                    "C": "İlk aylarda alınan kalorinin yaklaşık %30'u büyüme ve yeni doku sentezine harcanır",
                    "D": "Bebeğin enerji yeterliliğinin en güvenilir göstergesi büyüme eğrilerindeki persentil izlemidir",
                    "E": "Bebeklerin kilogram başına kalori ihtiyacı yetişkinlerin yaklaşık üçte biri kadardır"
                },
                "E",
                "Doğru cevap E'dir: Bebeklerin kilogram başına enerji ihtiyacı (100-120 kcal/kg) yetişkinlerin (30-35 kcal/kg) yaklaşık 3 kat fazlasıdır; üçte biri değil! A, B, C ve D seçenekleri tamamen doğrudur."
            )
        ]
    })

    # Slayt 22: Protein İhtiyacı ve Aşırı Protein Yükünün Riskleri
    slides.append({
        "id": "k1-22-s22",
        "title": "Protein İhtiyacı ve Aşırı Protein Yükünün Riskleri",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 22,
        "narrative": (
            "Proteinler büyüme, enzimler ve antikor sentezi için vazgeçilmezdir. "
            "Bebeklikte kilogram başına protein gereksinimi erişkinden (0.8 g/kg) oldukça yüksektir ve **ortalama 1.6 g/kg/gün** civarındadır. "
            "Anne sütü ilk 6 ay boyunca bebeğin tüm protein ve aminoasit gereksinimini %100 oranında karşılar. "
            "6. aydan sonra artan ihtiyaç yoğurt, yumurta sarısı, kıyma, tavuk ve baklagillerle desteklenir. "
            "**Pediatrik Uyarı: Fazla Protein Faydalı Değildir!** "
            "Bebeğe erken dönemde aşırı protein (örneğin inek sütü veya yüksek proteinli mamalar) verilmesi: "
            "1. İntrasellüler suyun böbreğe çekilmesine ve dehidratasyona, "
            "2. Üre ve amonyak birikimiyle metabolik asidoza, "
            "3. İleriki çocukluk ve erişkinlik döneminde **obezite riskinin katlanmasına** (Erken Protein Hipotezi) yol açar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Süt çocuğunda hızlı doku sentezi nedeniyle kilogram başına protein ihtiyacı yaklaşık 1,6 g/kg düzeyindedir.",
                "1,6 g/kg",
                "Bebeklikte kilogram başına gereken gram protein miktarı"
            ),
            make_before_after(
                "İdeal Protein Alımı ile Aşırı Protein Yüklemesi Kıyası",
                "İdeal Düzey (Anne Sütü)",
                "Enerjinin %6-7'si proteinden gelir; büyüme mükemmeldir, böbreğe binen üre yükü minimaldir.",
                "Aşırı Protein Yükü (İnek Sütü)",
                "Enerjinin %20'si proteindir; azot yükü böbreği yorar, metabolik asidoz ve çocukluk obezitesini tetikler.",
                "Fizyolojik büyüme sağlayan dengeli protein ile böbreği tüketen aşırı proteinin farkı"
            ),
            make_active_recall(
                "Erken dönemde bebeklere yüksek proteinli besinler veya inek sütü verilmesinin uzun dönemli metabolik riski nedir?",
                "İGF-1 eksenini aşırı uyararak adipsit hiperplazisine yol açması ve çocukluk/erişkinlik döneminde obezite riskini belirgin artırmasıdır (Erken Protein Hipotezi).",
                "Erken protein hipotezi ve obezite bağlantısı"
            )
        ]
    })

    # Slayt 23: Yağ Gereksinimi ve Esansiyel Yağ Asitleri (Linoleik Asit)
    slides.append({
        "id": "k1-22-s23",
        "title": "Yağ Gereksinimi ve Esansiyel Yağ Asitleri (Linoleik Asit)",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 23,
        "narrative": (
            "Yağlar bebek beslenmesinde birincil kalori kaynağıdır; anne sütündeki toplam enerjinin **yaklaşık %50'si yağlardan** gelir. "
            "Her 100 kalori için 3.8 ila 6 gram yağ bulunmalıdır; bebeklerde asla düşük yağlı veya yağsız diyet uygulanmaz! "
            "**Linoleik Asit (Omega-6) Elzemdir:** "
            "Linoleik asit vücutta sentezlenemeyen esansiyel bir çoklu doymamış yağ asididir. "
            "Anne sütü enerjisinin **en az %5'i linoleik asitten** oluşur. "
            "Eksikliğinde bebekte büyüme duraklar, kuru pullanan deri lezyonları (dermatit) ve saç dökülmesi gelişir. "
            "Ayrıca anne sütündeki **DHA (Dokosaheksaenoik asit)** ve **ARA (Arakidonik asit)**, "
            "beyin serebral korteksinin gelişimi, miyelinizasyon ve retina fotoreseptör olgunlaşması için kritiktir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Büyüme ve cilt bütünlüğü için elzem olan linoleik asit anne sütü enerjisinin yüzde beşini oluşturur.",
                "yüzde beşini",
                "Omega-6 yağ asidinin anne sütü enerjisindeki asgari payı"
            ),
            make_causal_chain(
                "Esansiyel Yağ Asitlerinin Nörolojik Gelişim Zinciri",
                [
                    "1. Yağ Alımı: Anne sütünden zengin linoleik asit, alfa-linolenik asit ve DHA emilir.",
                    "2. Hücre Zarı Entegrasyonu: Çoklu doymamış yağlar nöron membranlarına kovalent katılır.",
                    "3. Miyelinizasyon: Aksonlar etrafında miyelin kılıf izolasyonu süratle tamamlanır.",
                    "4. Fonksiyonel Kazanım: Bebekte yüksek görme keskinliği ve ileri bilişsel test skorları elde edilir."
                ]
            ),
            make_active_recall(
                "Bebek beslenmesinde linoleik asit eksikliğinde klinik olarak hangi iki majör patoloji ortaya çıkar?",
                "Büyüme duraklaması ve ciltte kuruluk, pullanma ve egzamatöz dermatit lezyonları gelişir.",
                "Büyüme geriliği ve kutanöz lezyon tablosu"
            )
        ]
    })

    # Slayt 24: Karbonhidrat Dengesi: Laktoz ve Galaktozun Biyolojik Rolü
    slides.append({
        "id": "k1-22-s24",
        "title": "Karbonhidrat Dengesi: Laktoz ve Galaktozun Biyolojik Rolü",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 24,
        "narrative": (
            "Karbonhidratlar bebek enerjisinin %30 ila %60'ını oluşturur. "
            "Anne sütünün majör karbonhidratı bir disakkarit olan **Laktozdur (Süt Şekeri)**. "
            "Anne sütündeki laktoz konsantrasyonu (7 g/100 ml), inek sütündekinden (4.8 g/100 ml) çok daha yüksektir. "
            "**Laktozun 3 Hayati Fonksiyonu:** "
            "1. **Beyin Gelişimi:** İnce bağırsaktaki laktaz enzimi laktozu glikoz ve **galaktoza** parçalar. "
            "Galaktoz, santral sinir sistemindeki serebrozidlerin ve gangliozidlerin (beyin ak maddesi) ana yapıtaşıdır. "
            "2. **Mikrobiyota Desteği:** Sindirilmeyen laktoz kolona geçer; yararlı *Lactobacillus bifidus* bakterilerini "
            "besleyerek laktik asit üretir, kolon pH'sını asitleştirir ve patojen bakterileri öldürür. "
            "3. **Kalsiyum Emilimi:** Asidik ortam kalsiyum, magnezyum ve demirin çözünürlüğünü ve emilimini artırır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Laktozun parçalanmasıyla açığa çıkan galaktoz santral sinir sisteminde serebrozid sentezi için temel yapıtaşıdır.",
                "serebrozid sentezi",
                "Beyin ak maddesinde glikolipid kılıf üretimi süreci"
            ),
            make_table(
                "Anne Sütü Karbonhidratının Fizyolojik Etkileri",
                ["Karbonhidrat Fraksiyonu", "Metabolik Ürünü / Hedefi", "Biyolojik Fonksiyonu"],
                [
                    ["Glukoz", "Doğrudan hücresel enerji", "Eritrosit ve nöronların anlık kalori yakıtı"],
                    [
                        "Galaktoz",
                        {"text": "Serebrozid ve gangliozid", "isMasked": True, "hint": "Beyin miyelin ak maddesi lipitleri"},
                        "Beyin dokusu ve sinir miyelinizasyonunun inşası"
                    ],
                    ["Kolon Laktozu", "Laktik asit fermantasyonu", "Asidik pH ile patojenlerin baskılanması"],
                    ["Oligosakkaritler (HMO)", "Bifidobakteri stimülasyonu", "Prebiyotik koruma ve enfeksiyon bariyeri"]
                ]
            ),
            make_micro_quiz(
                "Anne sütündeki laktozun yüksek olmasının bebek fizyolojisine sağladığı avantajlarla ilgili hangisi yanlıştır?",
                {
                    "A": "Açığa çıkan galaktoz beyin serebrozidlerinin sentezinde kullanılır",
                    "B": "Kolonda fermantasyona uğrayarak ortamı asitleştirir ve patojen üremesini engeller",
                    "C": "Kalsiyum ve demir gibi minerallerin bağırsaktan biyoyararlanımını artırır",
                    "D": "Bebeklerin büyük çoğunluğunda doğuştan laktaz eksikliği olduğundan laktoz tehlikelidir",
                    "E": "Tüm memeliler arasında beyni en gelişmiş canlı olan insanın sütünde laktoz en yüksek düzeydedir"
                },
                "D",
                "Doğru cevap D'dir: Term bebeklerde laktaz enzimi doğumda tam aktiftir ve bebeklerin çok azında konjenital intolerans görülür; laktoz bebek için hayati bir beyin ve bağırsak besinidir. Diğer seçenekler tamamen doğrudur."
            )
        ]
    })

    # Slayt 25: Sıvı ve Su Gereksinimi: 1.5 ml/kal Kuralı ve Dehidratasyon
    slides.append({
        "id": "k1-22-s25",
        "title": "Sıvı ve Su Gereksinimi: 1.5 ml/kal Kuralı ve Dehidratasyon",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 25,
        "narrative": (
            "Bebekler yüksek metabolik hızları, geniş vücut yüzey alanları ve immatür böbrekleri nedeniyle "
            "yetişkinlere kıyasla kilogram başına muazzam miktarda sıvıya ihtiyaç duyarlar. "
            "**Sıvı İhtiyacı Formülü:** "
            "Pediatride temel kural: **Her 1 kalori için 1.5 ml sıvı** alınmasıdır (1.5 ml/kcal/gün). "
            "- 3. ayda: **140 - 160 ml/kg/gün**, "
            "- 6. ayda: **130 - 155 ml/kg/gün** sıvı gerekir. "
            "**Hayati Klinik Gerçek:** "
            "İlk 6 ay sadece anne sütü alan bir bebeğe, hava sıcaklığı 40 dereceye çıksa bile **KESİNLİKLE SU VERİLMEZ**! "
            "Çünkü anne sütünün %87-88'i saf, steril ve ideal mineral dengeli sudur. "
            "Bebeğe su verilmesi mide hacmini doldurarak süt emmesini engeller, malnütrisyon ve hiponatremi yapar. "
            "Ancak kusma veya ishal gibi patolojik durumlarda dehidratasyon ve elektrolit kaybı yakından izlenmelidir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bebeklerin günlük sıvı gereksinimi alınan her bir kalori başına 1,5 ml su olarak hesaplanır.",
                "1,5 ml su",
                "Kalori başına düşen mililitre sıvı gereksinim katsayısı"
            ),
            make_table(
                "Süt Çocuğunun Yaşa Göre Sıvı İhtiyacı Skalası",
                ["Bebek Yaşı", "Günlük Sıvı Gereksinimi (ml/kg)", "En İdeal Sıvı Kaynağı"],
                [
                    [
                        "3. Ay",
                        {"text": "140 - 160 ml/kg/gün", "isMasked": True, "hint": "Üçüncü ayın kilogram başı sıvı hacmi"},
                        "Sadece Anne Sütü (Ek suya gerek yoktur)"
                    ],
                    ["6. Ay", "130 - 155 ml/kg/gün", "Sadece Anne Sütü (veya tamamlayıcı başlangıcı)"],
                    ["1 Yaş", "100 - 120 ml/kg/gün", "Anne sütü ve aile sofrası sıvıları"],
                    ["Erişkin", "30 - 40 ml/kg/gün", "İçme suyu ve içecekler"]
                ]
            ),
            make_micro_quiz(
                "Anne sütü alan 2 aylık bir bebeğe yaz aylarında su verilmesi ile ilgili en doğru tıbbi tavsiye hangisidir?",
                {
                    "A": "Hava sıcak olduğu için her emzirmeden sonra 50 ml kaynatılmış su verilmelidir",
                    "B": "Anne sütünün %87'si su olduğundan en sıcak havalarda bile bebeğe ek su verilmemelidir",
                    "C": "Su verilmezse bebekte böbrek taşı oluşur",
                    "D": "Su yerine taze sıkılmış portakal suyu verilmelidir",
                    "E": "Günde en az yarım litre su biberonla verilmelidir"
                },
                "B",
                "Doğru cevap B'dir: Anne sütünün %87'si sudur ve böbreğin konsantrasyon kapasitesini hiç zorlamadan tüm sıvı ihtiyacını karşılar. Dışarıdan su verilmesi tokluk hissiyle anne sütü alımını azaltır ve hiponatremi riski yaratır."
            )
        ]
    })

    # Slayt 26: Kalsiyum ve Fosfor Dengesi: İskelet Mineralizasyonu ve Hipokalsemi
    slides.append({
        "id": "k1-22-s26",
        "title": "Kalsiyum ve Fosfor Dengesi: İskelet Mineralizasyonu ve Hipokalsemi",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 26,
        "narrative": (
            "Hızlı iskelet büyümesi muazzam miktarda kalsiyum ve fosfor gerektirir: "
            "- **Anne Sütünde Kalsiyum Biyoyararlanımı:** "
            "Anne sütündeki kalsiyum miktarı (30 mg/100 ml), inek sütündekinden (120 mg/100 ml) rakamsal olarak 4 kat daha azdır. "
            "Fakat anne sütündeki kalsiyumun **üçte ikisi (%60-70'i) bebek tarafından hızla emilir ve vücutta birikir**! "
            "İnek sütündeki kalsiyumun ise ancak %20-30'u emilebilir. "
            "- **İdeal Ca / P Oranı (2 : 1):** "
            "Anne sütünde kalsiyum / fosfor oranı 2:1'dir; bu oran kemik mineralizasyonu için doğadaki en kusursuz orandır. "
            "- **İnek Sütünde Aşırı Fosfor ve Hipokalsemik Tetani:** "
            "İnek sütünde fosfor 6 kat fazladır. Yenidoğana inek sütü verilirse kanda fosfor yükselir (hiperfosfatemi); "
            "immatür paratiroid bezi bunu dengeleyemez ve kanda iyonize kalsiyum aniden çökerek **Yenidoğanın Hipokalsemik Tetanisine (konvülsiyon ve laringospazm)** yol açar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki kalsiyum fosfor oranı ikiye bir olup kemik mineralizasyonu için en kusursuz fizyolojik dengedir.",
                "ikiye bir",
                "Anne sütündeki Ca ve P atomlarının ideal oran katsayısı"
            ),
            make_before_after(
                "Anne Sütü ile İnek Sütü Kalsiyum/Fosfor Metabolizması Kıyası",
                "Anne Sütü Ca/P Dengesi (2:1)",
                "Kalsiyumun 2/3'ü emilir; fosfor dengelidir, paratiroidi yormaz, iskelet hızla mineralize olur.",
                "İnek Sütü Ca/P Dengesizliği (1.2:1)",
                "Fosfor 6 kat fazladır; kanda fosfor birikir, kalsiyum çöker ve yenidoğanda hipokalsemik tetani nöbeti yapar.",
                "Yüksek biyoyararlanımlı fizyolojik mineralizasyon ile hiperfosfatemik tetani riski ayrımı"
            ),
            make_active_recall(
                "Yenidoğana inek sütü verildiğinde gelişebilen 'Neonatal Hipokalsemik Tetani' tablosunun biyokimyasal mekanizması nedir?",
                "İnek sütündeki 6 kat fazla fosforun kanda hiperfosfatemi yaratması ve kalsiyumu bağlayarak iyonize kalsiyum düzeyini tehlikeli biçimde düşürmesidir.",
                "Aşırı fosfor yükü ve hipokalsemi mekanizması"
            )
        ]
    })

    # Slayt 27: Demir Metabolizması: Depoların Tükenmesi ve Biyoyararlanım
    slides.append({
        "id": "k1-22-s27",
        "title": "Demir Metabolizması: Depoların Tükenmesi ve Biyoyararlanım",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 27,
        "narrative": (
            "Demir, hemoglobin sentezi ve beyinde miyelinizasyon ile nörotransmitter enzimleri için elzemdir: "
            "- **Fetal Depolar:** Term doğan sağlıklı bir bebek, anneden plasenta yoluyla aldığı demir depolarıyla doğar. "
            "Bu depolar doğum ağırlığı iki katına çıkana kadar, yani **yaklaşık 4 ila 6 ay boyunca** bebeğe tam yeterlidir. "
            "Prematüre veya düşük doğum ağırlıklı bebeklerde ise bu depolar çok daha küçük olduğundan 2. ayda tükenir. "
            "- **Eşsiz Biyoyararlanım:** "
            "Anne sütündeki demir konsantrasyonu düşüktür (0.5 mg/L), ancak **emilimi olağanüstü yüksektir (%50 - 60)**! "
            "Buna karşılık inek sütü veya formül mamalardaki demirin ancak **%10'u** emilebilir. "
            "- **Kritik Kural:** "
            "Bebeğe anne sütüyle birlikte meyve püresi veya sebze verildiğinde, fitatlar ve lifler demiri bağlar ve "
            "anne sütü demirinin emilimi aniden %10'a düşer! "
            "Bu nedenle 4-6. aydan sonra demir depoları tükenir ve ek besinlerle demir desteği şart hale gelir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütündeki demirin biyoyararlanımı yüzde elli ila altmış gibi olağanüstü yüksek bir orandadır.",
                "yüzde elli ila altmış",
                "Anne sütü demirinin bağırsaktan biyoyararlanım fraksiyonu aralığı"
            ),
            make_table(
                "Farklı Süt Türlerinde Demir Emilim Biyoyararlanımı",
                ["Süt / Besin Türü", "Demir Konsantrasyonu", "Bağırsaktan Emilim Oranı (%)", "Biyoyararlanım Mekanizması"],
                [
                    [
                        "Anne Sütü (Tek Başına)",
                        "0.5 mg/L (Düşük)",
                        {"text": "%50 - 60", "isMasked": True, "hint": "Anne sütündeki eşsiz yüksek demir emilim oranı"},
                        "Laktoferrin, C vitamini ve asidik laktoz ile maksimum emilim"
                    ],
                    ["İnek Sütü", "0.5 mg/L (Düşük)", "%10", "Kazein ve fosfat demiri bağlar; bağırsakta mikrokanama yapar"],
                    ["Demir Destekli Mama", "12 mg/L (Çok Yüksek)", "%4 - 10", "Düşük biyoyararlanımı telafi etmek için aşırı doz konur"],
                    ["Anne Sütü + Ek Gıda", "Değişken", "%10 - 15", "Ek gıdalardaki fitat ve lifler anne sütü demirini bloke eder"]
                ]
            ),
            make_micro_quiz(
                "Term doğan sağlıklı bir bebekte doğumda var olan karaciğer demir depoları ne zamana kadar yeterlidir?",
                {
                    "A": "Doğumdan sonraki ilk 10 gün içinde biter",
                    "B": "Doğum ağırlığı iki katına çıkana kadar (yaklaşık 4-6 ay)",
                    "C": "İki yaşına kadar hiçbir ek demir gerekmez",
                    "D": "Demir depoları ancak 5 yaşında tükenir",
                    "E": "Doğum anında hiçbir bebekte demir deposu bulunmaz"
                },
                "B",
                "Doğru cevap B'dir: Term bebek fetal dönemde biriktirdiği demir rezerviyle doğar ve bu rezerv doğum ağırlığı 2 katına çıkana kadar (ortalama 4-6 ay) ihtiyacı karşılar; 4-6. aydan sonra depolar biter ve profilaksi/ek gıda gerekir."
            )
        ]
    })

    # Slayt 28: Çinko ve Flor Gereksinimleri
    slides.append({
        "id": "k1-22-s28",
        "title": "Çinko ve Flor Gereksinimleri",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 28,
        "narrative": (
            "Eser elementler hücresel büyüme ve organogenezde anahtar kofaktörlerdir: "
            "- **Çinko (Zinc):** "
            "Yenidoğan bebeğin vücudunda **hiç çinko deposu yoktur**! "
            "Buna rağmen anne sütü alan bebeklerde ilk yıl çinko eksikliği görülmez; çünkü anne sütündeki çinko, "
            "düşük molekül ağırlıklı ligandlara bağlıdır ve mamalardakinden kat kat daha iyi emilir. "
            "Ancak sıkı vejetaryen/vegan beslenen annelerin sütünde çinko düşük olabilir. "
            "Çinko eksikliğinde büyüme duraklar, immün yetmezlik, kronik ishal ve periorifisiyel dermatit (akrodermatitis enteropatika benzeri) gelişir. "
            "- **Flor (Fluoride):** "
            "Flor diş minesi kristallerine (floroapatit) katılarak diş çürüklerini önler. "
            "Anne sütünde flor konsantrasyonu düşüktür; dişler çıkmaya başladıktan sonra (yaklaşık 6. aydan itibaren) "
            "içme suyunun flor içeriğine göre uygun flor profilaksisi değerlendirilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan bebeğin vücudunda çinko deposu bulunmamasına rağmen anne sütündeki yüksek emilim ilk yıl ihtiyacı karşılar.",
                "çinko deposu",
                "Yenidoğanda rezervi bulunmayan esansiyel eser element stoku"
            ),
            make_before_after(
                "Çinko ve Flor Elementlerinin Bebekteki Dinamikleri",
                "Çinko Metabolizması",
                "Vücutta deposu yoktur; anne sütünden yüksek biyoyararlanımla emilir; büyüme ve bağışıklık için zorunludur.",
                "Flor Metabolizması",
                "Anne sütünde düşüktür; dişlerin çıkmasıyla birlikte diş minesini çürüklerden korumak için önem kazanır.",
                "Deposu olmayan hücresel büyüme kofaktörü ile diş minesini sertleştiren mineral ayrımı"
            ),
            make_active_recall(
                "Yenidoğanda vücut deposu bulunmayan ancak anne sütündeki yüksek emilim sayesinde eksikliği ilk 6 ayda nadir görülen eser element hangisidir?",
                "Çinko (Zinc) elementidir; büyüme, immünite ve epitel bütünlüğü için kilit rol oynar.",
                "Vücutta rezervi olmayan temel büyüme minerali"
            )
        ]
    })

    # Slayt 29: [TEKRAR SAYFASI - CHECKPOINT 3] Bebeğin Besin Ögesi ve Sıvı İhtiyaçları
    slides.append({
        "id": "k1-22-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Bebeğin Besin Ögesi ve Sıvı İhtiyaçları",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 29,
        "narrative": (
            "Bu üçüncü checkpoint sayfasında, bebeğin makro ve mikro besin ögesi gereksinimlerinin "
            "en kritik noktalarını kilitliyoruz: "
            "1. **Enerji:** 30 ml anne sütü 20 kalori (100 ml ~67 kcal) sağlar; persentil takibi yeterliliğin aynasıdır. "
            "2. **Protein:** 1.6 g/kg gerekir; aşırı protein böbreğe azot yükü bindirir ve ileride obezite yapar. "
            "3. **Linoleik Asit:** Anne sütü enerjisinin %5'i olmalıdır; büyüme ve cilt bariyeri için elzemdir. "
            "4. **Laktoz ve Galaktoz:** Beyin serebrozidlerinin sentezi ve asidik kolon florası için majör kaynaktır. "
            "5. **Sıvı:** 1.5 ml/kcal kuralı geçerlidir; anne sütünün %87'si su olduğundan ilk 6 ay ek su verilmez. "
            "6. **Mineraller:** Ca/P oranı 2:1'dir; demir depoları 4-6 ayda biter; yenidoğanda çinko deposu yoktur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "k1-22-fc-07",
                "Anne sütünün sağladığı ortalama enerji miktarı 30 mililitrede kaç kaloridir ve 100 mililitrede kaça denk gelir?",
                "30 ml'de 20 kalori (100 ml'de yaklaşık 67 kcal)",
                "Standart bebek sütünün bir ons hacmindeki termal enerji değeri",
                "Besin Ögeleri"
            ),
            make_flashcard(
                "k1-22-fc-08",
                "Bebekte büyüme ve cilt bütünlüğü için elzem olan ve anne sütü enerjisinin yaklaşık %5'ini oluşturan esansiyel yağ asidi hangisidir?",
                "Linoleik asit (Omega-6)",
                "Deri bariyeri ve hücre zarı için zorunlu doymamış lipid",
                "Besin Ögeleri"
            ),
            make_flashcard(
                "k1-22-fc-09",
                "Zamanında doğan (term) sağlıklı bir bebeğin karaciğer demir depoları dışarıdan ek demir almadan yaklaşık kaçıncı aya kadar yeterlidir?",
                "Yaklaşık 4 - 6. aya kadar",
                "Doğum tartısı iki katına çıkana dek tükenmeyen mineral stoğu süresi",
                "Besin Ögeleri"
            )
        ]
    })

    # Slayt 30: Bölüm Özeti: Besin Ögelerinden Vitaminler ve Yasaklı Gıdalara Geçiş
    slides.append({
        "id": "k1-22-s30",
        "title": "Bölüm Özeti: Besin Ögelerinden Vitaminler ve Yasaklı Gıdalara Geçiş",
        "section": "Bebeğin Makro ve Mikro Besin Ögesi Gereksinimleri",
        "slideNumber": 30,
        "narrative": (
            "Makro besinler (protein, yağ, karbonhidrat) ve temel mineraller bebeğin iskelet ve kas yapısını kurarken, "
            "vitaminler hücresel biyokimyasal reaksiyonların katalizörleridir. "
            "Anne sütü neredeyse tüm vitaminleri içerse de, iki hayati istisna vardır: "
            "Birincisi, anne sütünde D vitamini yetersizdir; dışarıdan profilaksi verilmezse raşitizm kaçınılmazdır. "
            "İkincisi, yenidoğan bağırsağında K vitamini üreten flora henüz yoktur; doğumda K vitamini yapılmazsa ölümcül beyin kanaması gelişir. "
            "Ayrıca bazı gıdalar (bal, keçi sütü, inek sütü) bebek metabolizması için ölümcül riskler taşır. "
            "Dördüncü bölümümüzde, profilaktik D ve K vitamini protokolleri, B12 eksikliği, keçi sütü anemisi ve bebek botulizmi incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yeterli beslenen annenin sütü D vitamini dışındaki tüm vitamin gereksinimini karşıladığından her bebeğe D vitamini desteği zorunludur.",
                "D vitamini",
                "Anne sütünde fizyolojik olarak yetersiz olan kalsiferol bileşiği"
            ),
            make_causal_chain(
                "Vitamin Eksikliklerinin Önlenmesi Mantığı",
                [
                    "1. Doğum Anı: Steril bağırsak K vitamini sentezleyemez; hemorajiyi önlemek için 1 mg IM K1 yapılır.",
                    "2. İlk Haftalar: Anne sütünde D vitamini düşüktür; raşitizmi önlemek için 400 IU/gün D vitamini başlanır.",
                    "3. 4-6. Aylar: Fetal demir depoları tükenir; anemi gelişimini önlemek için profilaktik demir verilir.",
                    "4. Yasak Besinler: 1 yaşından önce bal (botulizm) ve inek sütü (mikrokanama) kesinlikle yasaklanır."
                ]
            ),
            make_active_recall(
                "Anne sütüyle beslenen term bir bebeğe doğumdan itibaren mutlaka dışarıdan takviye edilmesi gereken tek vitamin hangisidir?",
                "D Vitaminidir; anne sütündeki konsantrasyonu yetersiz olduğundan doğumdan itibaren günlük 400 IU D vitamini damlası verilmelidir.",
                "Günlük 400 IU damla şeklinde verilen raşitizm önleyici takviye"
            )
        ]
    })

    return slides
