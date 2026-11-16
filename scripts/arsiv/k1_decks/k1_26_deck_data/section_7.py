# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 7: Beslenme Bozuklukları ve Protein-Enerji Malnütrisyonu (Slayt 61-70)
"""

from .helpers import (
    make_cloze,
    make_micro_quiz,
    make_table,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_section_7_slides():
    slides = []

    # Slayt 61: Beslenme Patolojisine Giriş
    slides.append({
        "id": "k1-26-s61",
        "title": "Beslenme Patolojisine Giriş: Primer vs Sekonder Malnütrisyon",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 61,
        "narrative": (
            "Beslenme bozuklukları, vücudun hücresel işlevleri ve doku bütünlüğünü sürdürebilmek için gereken enerji, "
            "protein, vitamin ve mineralleri yeterli düzeyde alamaması veya kullanamamasıdır: "
            "1. **Primer Malnütrisyon:** "
            "- Diyette temel besin maddelerinin (kalori, protein, vitaminler) mutlak eksikliğidir. "
            "- Yoksulluk, kıtlık, bilgisizlik, afetler veya ihmal sonucu gelişir. "
            "2. **Sekonder (Koşullu) Malnütrisyon:** "
            "- Diyette besin maddeleri yeterli olduğu halde; emilim bozukluğu (malabsorpsiyon, Çölyak, Crohn), "
            "aşırı katabolik kayıp (şiddetli yanıklar, cerrahi travma), kullanım bozukluğu veya depolama yetersizliği sonucu gelişir. "
            "3. **Kanser Kaşeksisi:** "
            "- Malign tümörlü hastalarda görülen özel bir sekonder malnütrisyon formudur. "
            "- Tümör ve konak makrofajlarından salgılanan sitokinler (**TNF-alfa - eski adıyla Kaşektin, IL-6, Proteoliz İndükleyici Faktör - PIF**) "
            "iştahı tamamen kapatır, yağ dokusunu ve iskelet kasını agresif şekilde eritir; zorla beslenmeyle bile geri çevrilemez."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Primer ve Sekonder Malnütrisyon Ayrımı",
                ["Malnütrisyon Tipi", "Temel Etyolojik Mekanizma", "Klinik Prototip"],
                [
                    ["Primer Malnütrisyon", "Diyette kalori ve proteinin mutlak yokluğu", "Gelişmekte olan ülkelerde kıtlık, Marasmus, Kwashiorkor"],
                    ["Sekonder Malnütrisyon", "Kronik ishal, emilim bozukluğu, aşırı kayıp", "Çölyak hastalığı, kistik fibrozis malabsorpsiyonu, kısa bağırsak"],
                    [
                        "Kanser Kaşeksisi",
                        {"text": "TNF-alfa (Kaşektin) ve PIF aracılı aşırı katabolizma", "isMasked": True, "hint": "Tümör hastalarında yağ ve iskelet kasını eriten pro-enflamatuar sitokin fırtınası"},
                        "İleri evre pankreas, mide ve akciğer karsinomları"
                    ]
                ]
            ),
            make_active_recall(
                "Kanser hastalarında aşırı kas ve yağ kaybına yol açarak geri dönüşsüz kilo kaybı ve anoreksiya yapan ve tarihsel olarak 'kaşektin' adıyla da bilinen majör sitokin hangisidir?",
                "TNF-alfa sitokinidir (Tümör Nekroz Faktörü alfa).",
                "Makrofajlardan salınan ve lipid metabolizmasını yıkan pro-enflamatuar aracı"
            )
        ]
    })

    # Slayt 62: Şiddetli Akut Malnütrisyon (SAM) ve Kriterler
    slides.append({
        "id": "k1-26-s62",
        "title": "Şiddetli Akut Malnütrisyon (SAM) ve Kriterler",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 62,
        "narrative": (
            "Dünya Sağlık Örgütü (DSÖ), çocuklarda mortalitesi en yüksek olan yetersiz beslenme tablosunu "
            "**Şiddetli Akut Malnütrisyon (SAM - Severe Acute Malnutrition)** olarak tanımlamıştır: "
            "1. **Antropometrik Tanı Kriterleri (3 Ana Kriterden Herhangi Biri):** "
            "- **Boya Göre Ağırlık Z-Skoru:** DSÖ büyüme standartlarına göre medyanın **-3 Standart Sapmanın (-3 SD) altında** olması. "
            "- **Orta Üst Kol Çevresi (MUAC):** 6-59 aylık çocuklarda kol çevresinin **<115 mm (11.5 cm)** ölçülmesi (kırmızı bölge). "
            "- **Nutrisyonel Ödem:** İki taraflı simetrik gode bırakan ayak ve bacak ödeminin saptanması (doğrudan SAM tanısı koydurur!). "
            "2. **Hücresel İki Protein Bölmesi:** "
            "- İnsan vücudundaki proteinler ikiye ayrılır: "
            "  * **Somatik Bölme:** İskelet kası proteinleridir (kol çevresi ve kreatinin atılımıyla ölçülür). "
            "  * **Viseral Bölme:** Karaciğer tarafından üretilen plazma proteinleridir (serum **albümin ve transferrin** ile ölçülür)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Somatik vs Viseral Protein Bölmeleri",
                "Somatik Protein Bölmesi",
                "İskelet kaslarında yer alır; marasmusta şiddetle yıkılarak enerjiye çevrilir; kol çevresiyle ölçülür",
                "Viseral Protein Bölmesi",
                "Karaciğer ve iç organ proteinleridir (albümin, transferrin); kwashiorkorda çöker ve hipoalbüminemik ödem yapar"
            ),
            make_cloze(
                "Şiddetli akut malnütrisyon tanısında 6-59 aylık çocuklarda orta üst kol çevresinin yüz on beş milimetre altında ölçülmesi kırmızı bayrak kriteridir.",
                "yüz on beş milimetre",
                "Basit mezura ile çocuğun kol kalınlığında şiddetli kas kaybını saptayan eşik ölçü"
            )
        ]
    })

    # Slayt 63: Marasmus Etyopatogenezi ve Somatik Yıkım
    slides.append({
        "id": "k1-26-s63",
        "title": "Marasmus Etyopatogenezi ve Somatik Yıkım",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 63,
        "narrative": (
            "Marasmus, Yunanca 'kuruma / tükenme' anlamına gelir; diyetle **hem kalori hem de proteinin eşit derecede mutlak eksikliğidir**: "
            "1. **Patofizyolojik Uyarlanma:** "
            "- Vücut hayatta kalabilmek için katabolik moda geçer; kortizol düzeyi yükselir, insülin seviyesi tabana vurur. "
            "- Hayati iç organları beslemek için **somatik protein bölmesi (iskelet kasları)** acımasızca proteolize uğratılır. "
            "- Kaslardan salınan aminoasitler karaciğere taşınarak glukoneogenezde yakıt olarak kullanılır. "
            "2. **Deri Altı Yağ Dokusunun Tükenmesi:** "
            "- Lipoliz tetiklenir; deri altındaki tüm nötral yağ depoları hızla eritilir. "
            "3. **Viseral Bölmenin Göreceli Korunması:** "
            "- Marasmus hastasında karaciğer viseral protein sentezini (albümin) korumak için elinden geleni yapar. "
            "- Bu nedenle serum albümin düzeyi normal veya normale yakındır; **ÖDEM GÖRÜLMEZ**!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Marasmusta Somatik Yıkım ve Katabolik Uyum Zinciri",
                [
                    "1. Mutlak Kalori Yokluğu: Diyetle alınan karbonhidrat, yağ ve proteinin tamamen tükenmesi",
                    "2. İnsülin Düşüşü: Hipoglisemiyi önlemek için insülinin sıfırlanıp kortizolün fırlaması",
                    "3. Kas Proteolizi: İskelet kaslarının (somatik bölme) aminoasit eldesi için acımasızca eritilmesi",
                    "4. Subkütan Lipoliz: Deri altı yağ yastıklarının erimesi ve hastanın iskelet görünümü alması",
                    "5. Albümin Korunumu: Karaciğerin viseral sentezi sürdürmesi ve ödem oluşmaksızın zayıflık"
                ]
            ),
            make_active_recall(
                "Marasmus hastası bir çocukta şiddetli kas ve yağ dokusu kaybına rağmen kwashiorkordan farklı olarak yaygın anazarka ödemin gelişmemesinin temel biyokimyasal nedeni nedir?",
                "Viseral protein bölmesinin (serum albümin düzeyinin) görece korunmuş olmasıdır.",
                "Karaciğerin aminoasitleri kullanarak albümin sentezini normal sınırlarda tutabilmesi"
            )
        ]
    })

    # Slayt 64: Marasmus Morfolojisi ve Kliniği
    slides.append({
        "id": "k1-26-s64",
        "title": "Marasmus Morfolojisi ve Kliniği",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 64,
        "narrative": (
            "Marasmuslu bir çocuk, tükenmiş bir canlı iskeleti andıran son derece dramatik morfolojik bulgular sergiler: "
            "1. **Büyüme-Gelişme Duraklaması:** Çocuğun kilosu yaşına göre standart medyanın **%60'ının altına** inmiştir. "
            "2. **Aşırı Kas ve Yağ Kaybı:** "
            "- Kollar ve bacaklar ipince kalmıştır ('zayıf çomak' bacaklar). "
            "- Gluteal yağ yastıkları tamamen eridiği için kalça cildi sarkar ('torba pantolon' görünümü). "
            "3. **'Yaşlı Adam / Maymun Yüzü' Manzarası:** "
            "- Yanaklardaki emme yağ yastıkçıkları (Bichat yağ dokusu) vücudun en son eriyen yağıdır; "
            "marasmusta bu yağ da eriyince yanaklar içeri çöker, elmacık kemikleri fırlar ve çocuk **küçük bir yaşlı adam veya maymun yüzü** görünümü alır. "
            "4. **Vital Bulgular:** Hipotermi, bradikardi, hipotansiyon; metabolizma hızı düşürülmüştür. "
            "5. **Deri ve Saç:** Deri kuru, gevşek ve kırışıktır; saçlar zayıftır ancak kwashiorkordaki gibi dökülme ve renk kaybı belirgin değildir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Marasmusun Karakteristik Fiziksel Muayene İmzaları",
                ["Anatomik Bölge", "Klinik Görünüm", "Altta Yatan Morfolojik Kayıp"],
                [
                    ["Yüz (Fasies)", "Yaşlı adam / maymun yüzü görünümü", "Bichat bukkal emme yağ yastıklarının erimesi"],
                    ["Ekstremiteler", "Çomak bacaklar, sarkan deri", "İskelet kası liflerinde ağır atrofi"],
                    [
                        "Gluteal Bölge",
                        {"text": "Torba pantolon (baggy pants) manzarası", "isMasked": True, "hint": "Gluteal yağ dokusunun tamamen yok olmasıyla sarkan bol deri kıvrımı"},
                        "Deri altı adipoz dokunun sıfırlanması"
                    ],
                    ["Batın ve Karın", "Çökük veya düz karın (ÖDEM YOKTUR)", "Asit veya hepatomegali bulunmaması"]
                ]
            ),
            make_micro_quiz(
                "Ağır beslenme yetersizliği olan 10 aylık bir bebeğin muayenesinde boy ve kilonun -3 SD altında olduğu, kol ve bacak kaslarının tamamen eridiği, yanak yağlarının kaybolmasıyla 'yaşlı adam yüzü' görünümünün oluştuğu ancak bacaklarda hiçbir ödem saptanmadığı izlenmiştir. Tanı nedir?",
                {
                    "A": "Marasmus",
                    "B": "Kwashiorkor",
                    "C": "Kistik Fibrozis",
                    "D": "Konjenital Hipotiroidi (Kretinizm)",
                    "E": "Down Sendromu"
                },
                "A",
                {
                    "A": "Doğrudur; saf kalori eksikliği, somatik kas erimesi, yaşlı adam yüzü ve ödemin olmaması marasmusun klasik tablosudur.",
                    "B": "Yanlış; kwashiorkorda yaygın ödem ve şiş karın vardır.",
                    "C": "Yanlış; KF akciğer ve ter testiyle belirir.",
                    "D": "Yanlış; kretinizmde kaba yüz ve miksödem vardır.",
                    "E": "Yanlış; Down sendromu genetik trizomidir."
                }
            )
        ]
    })

    # Slayt 65: Kwashiorkor Etyopatogenezi ve Viseral Yıkım
    slides.append({
        "id": "k1-26-s65",
        "title": "Kwashiorkor Etyopatogenezi ve Viseral Yıkım",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 65,
        "narrative": (
            "Kwashiorkor, Afrika dilinde 'ikinci bebek doğduğunda birincinin yakalandığı hastalık' anlamına gelir: "
            "1. **Klasik Sosyal Senaryo:** "
            "- Yeni bir bebek doğunca anne sütünden aniden kesilen ilk çocuk, neredeyse sadece karbonhidrattan zengin "
            "(nişasta, pirinç lapası, manyok kökü) ancak **proteinden tamamen yoksun** bir diyetle beslenir. "
            "- Kalori nispeten yeterli veya hafif azdır; ancak **protein alımı neredeyse sıfırdır**. "
            "2. **Hipoalbüminemi ve Anazarka Ödem:** "
            "- Karaciğer aminoasit bulamadığı için albümin sentezleyemez; serum albümini dibe vurur (**<2.5 g/dL**). "
            "- Plazma onkotik basıncı çöker; damar içindeki sıvı interstisyel boşluğa kaçar. "
            "- Sonuç: Ayaklarda, bacaklarda, yüzde ve karında masif **nutrisyonel ödem (asit)** gelişir. "
            "3. **Karaciğer Yağlanması (Steatoz):** "
            "- Karaciğerde serbest yağ asitlerinden trigliserid sentezlenir; ancak trigliseridleri VLDL halinde kana verecek "
            "**apolipoproteinler sentezlenemez**! "
            "- Trigliseridler hepatositlerde hapsolur; karaciğer devasa boyuta ulaşır (**masif hepatomegali**)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Kwashiorkorda Hipoalbüminemi ve Yağlı Karaciğer Basamakları",
                [
                    "1. Protein Yokluğu: Diyetin sadece nişasta/karbonhidrattan oluşması, aminoasit girişinin durması",
                    "2. Hepatik Sentez Çöküşü: Karaciğerin viseral proteinleri (albümin ve apolipoprotein B) üretememesi",
                    "3. Onkotik Basınç Kaybı: Hipoalbüminemi sonucu intravasküler sıvının dokulara sızıp anazarka ödem yapması",
                    "4. Trigliserid Tuzağı: Sentezlenen lipidlerin apolipoproteinsiz VLDL yapamayıp karaciğerde birikmesi",
                    "5. Masif Yağlı Karaciğer: Hepatositlerin trigliseridle dolması ve belirgin hepatomegali gelişimi"
                ]
            ),
            make_before_after(
                "Marasmus vs Kwashiorkor Biyokimyasal Zıtlığı",
                "Marasmus (Kalori ve Protein Yok)",
                "Somatik iskelet kası erir; albümin normaldir; karaciğer yağlanması ve ödem görülmez",
                "Kwashiorkor (Yalnızca Protein Yok)",
                "Viseral proteinler çöker; ağır hipoalbüminemi vardır; anazarka ödem ve masif hepatik steatoz kaçınılmazdır"
            )
        ]
    })

    # Slayt 66: Kwashiorkor Morfolojisi: Ödem, Deri ve Bayrak Saç
    slides.append({
        "id": "k1-26-s66",
        "title": "Kwashiorkor Morfolojisi: Ödem, Deri ve Bayrak Saç",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 66,
        "narrative": (
            "Kwashiorkorlu bir çocuk, marasmusun aksine şiş ve aldatıcı bir tokluk görüntüsü verir: "
            "1. **Nutrisyonel Ödem ve Şiş Karın (Karakteristik Görünüm):** "
            "- Ayak sırtından başlayıp uyluklara, genital bölgeye ve göz kapaklarına kadar uzanan yumuşak, gode bırakan ödem. "
            "- Karında asit ve devasa yağlı karaciğer (hepatomegali) nedeniyle batın ileriye doğru çıkıktır (şiş karın). "
            "Bu durum çocuğun 'kilosunun iyi olduğu' yanılsamasını yaratarak aileleri aldatabilir! "
            "2. **Deri Bulguları (Boya Soyulması Manzarası - Flaky Paint Dermatosis):** "
            "- Deride alacalı hiperkeratoz, hiperpigmente ve hipopigmente yamalar oluşur. "
            "- Deri kurur, çatlar ve kurumuş boyanın pul pul dökülmesi gibi dökülür; derin erozyonlar ve sekonder enfeksiyonlar gelişir. "
            "3. **Saç Bulguları ve 'Bayrak İşareti' (Flag Sign):** "
            "- Saçlar incelir, kurur, kıvrımını kaybeder ve kolayca kökünden çekilip dökülür. "
            "- Çocuğun beslenemediği protein yokluğu dönemlerinde saç rengi açılır (kızıl/sarımsı şerit); iyi beslendiği "
            "dönemlerde ise koyulaşır. Saç teli boyunca **ardışık açık ve koyu renkli bantlar oluşur (**Bayrak İşareti**). "
            "4. **Apatik Davranış:** Çocuk aşırı derecede halsiz, uyuşuk, çevreye ilgisiz (apati) ve beslenmeyi reddeder haldedir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kwashiorkorun Klinik Triadı ve Patognomonik Belirteçleri",
                ["Klinik Belirteç", "Görsel / Morfolojik Özellik", "Altta Yatan Patofizyoloji"],
                [
                    ["Yaygın Nutrisyonel Ödem", "Gode bırakan periferik ödem ve asit", "Ağır hipoalbüminemiye bağlı onkotik basınç çöküşü"],
                    [
                        "Deri Lezyonları",
                        "Soyulmuş boya manzarası (Flaky paint dermatosis)",
                        {"text": "Dermal atrofi, hiperkeratoz ve mozaik pullanma", "isMasked": True, "hint": "Eski kurumuş boyanın duvardan dökülmesine benzeyen pullu deri döküntüsü"}
                    ],
                    ["Saç Anomalisi", "Bayrak işareti (Flag sign)", "Dönemsel protein alımına bağlı saçta açık/koyu renkli şeritler"],
                    ["Batın Muayenesi", "Şişkin karın ve belirgin hepatomegali", "Apolipoprotein yokluğuna bağlı masif hepatik steatoz"],
                    ["Davranış", "Aşırı letarji, çevreye ilgisizlik ve apati", "Nörotransmitter sentez yetersizliği ve serebral enerji açığı"]
                ]
            ),
            make_active_recall(
                "Kwashiorkorlu çocukların saç tellerinde protein eksikliği dönemlerinde melanin sentezinin durup saçın sararması, protein aldığı dönemlerde ise koyulaşmasıyla oluşan açık-koyu bantlı saç bulgusuna ne ad verilir?",
                "Bayrak işaretidir (flag sign).",
                "Saçta çizgili renk değişimini bayrak şeritlerine benzeten klasik pediatrik işaret"
            )
        ]
    })

    # Slayt 67: Marasmus ile Kwashiorkor'un Karşılaştırmalı Tablosu
    slides.append({
        "id": "k1-26-s67",
        "title": "Marasmus ile Kwashiorkor'un Karşılaştırmalı Tablosu",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 67,
        "narrative": (
            "Tıp fakültesi kurullarında ve pediatri sınavlarında en sık sorulan iki malnütrisyon tablosunun kesin zıtlıkları: "
            "1. **Eksiklik Türü:** Marasmusta hem kalori hem protein eşit derecede yoktur; Kwashiorkorda protein eksikliği kaloriye göre çok daha derindir. "
            "2. **Etkilenen Protein Bölmesi:** Marasmusta somatik bölme (kaslar) tükenir, viseral (albümin) korunur. "
            "Kwashiorkorda ise viseral bölme çöker, albümin taban yapar. "
            "3. **Ödem:** Marasmusta kesinlikle **yoktur**; Kwashiorkorun **olmazsa olmaz kardinal bulgusudur**. "
            "4. **Karaciğer:** Marasmusta normaldir; Kwashiorkorda apolipoprotein yapılamadığı için **masif yağlı karaciğer ve hepatomegali** vardır. "
            "5. **Deri altı Yağı:** Marasmusta tamamen erir; Kwashiorkorda ödemin altında yağ dokusu kısmen korunmuştur. "
            "6. **Görünüm:** Marasmus 'küçük yaşlı adam / maymun yüzü'; Kwashiorkor ise 'ödemli, şiş karınlı, dökülen derili çocuktur'."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Marasmus ve Kwashiorkor Ayırıcı Tanı Matrisi",
                ["Özellik / Parametre", "Marasmus", "Kwashiorkor"],
                [
                    ["Primer Eksiklik", "Kalori ve protein (Eşit eksik)", "Yalnızca protein (Karbonhidrat var)"],
                    ["Ödem Varlığı", "YOKTUR", "VARDIR (Kardinal bulgu)"],
                    ["Serum Albümin Düzeyi", "Normal veya hafif düşük", "Çok ağır derecede düşük (<2.5 g/dL)"],
                    [
                        "Karaciğer Morfolojisi",
                        "Normal boyut ve histoloji",
                        {"text": "Masif hepatomegali ve ağır yağlanma (steatoz)", "isMasked": True, "hint": "Apolipoprotein sentezlenememesi sonucu karaciğerde trigliserid hapsolması"}
                    ],
                    ["Somatik Kas Yıkımı", "Çok şiddetli (Çomak bacaklar)", "Hafif - orta düzeyde"],
                    ["Deri ve Saç Bulgusu", "Hafif kuruluk, yaşlı adam yüzü", "Flaky paint döküntü, bayrak işareti saç"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki klinik ve laboratuvar bulgularından hangisi bir malnütrisyon olgusunda marasmustan ziyade kesin olarak KWASHİORKOR tablosunu destekler?",
                {
                    "A": "Bilateral alt ekstremitelerde gode bırakan ödem ve masif hepatomegali varlığı",
                    "B": "Deri altı yağ dokusunun tamamen tükenmesi ve yanakların içeri çökmesi",
                    "C": "Serum albümin konsantrasyonunun tamamen normal sınırlarda saptanması",
                    "D": "Vücutta hiçbir ödem veya asit sıvısının bulunmaması",
                    "E": "Karaciğer boyutlarının ve fonksiyon testlerinin tamamen normal olması"
                },
                "A",
                {
                    "A": "Doğrudur; hipoalbüminemik ödem ve apolipoprotein yetersizliğine bağlı yağlı karaciğer kwashiorkorun mutlak belirteçleridir.",
                    "B": "Yanlış; bu marasmusun yaşlı adam yüzüdür.",
                    "C": "Yanlış; marasmusta albümin korunur, kwashiorkorda çöker.",
                    "D": "Yanlış; ödem olmaması marasmustur.",
                    "E": "Yanlış; kwashiorkorda karaciğer masif büyür."
                }
            )
        ]
    })

    # Slayt 68: Malnütrisyon Zemininde İmmün Yetmezlik
    slides.append({
        "id": "k1-26-s68",
        "title": "Malnütrisyon Zemininde İmmün Yetmezlik",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 68,
        "narrative": (
            "Şiddetli akut malnütrisyonu olan çocukların ölüm nedeni doğrudan açlık değil, **ikincil immün yetmezlik zemininde gelişen ağır enfeksiyonlardır**: "
            "1. **Hücresel Bağışıklığın Çöküşü (T Hücre Kusuru):** "
            "- Malnütrisyonda en ağır darbeyi T lenfositleri alır. "
            "- **Timus Atrofisi:** Timus bezi hızla küçülür, lenfositlerini kaybeder (besinsel timektomi). "
            "- Periferik kanda CD4+ T hücre sayısı dramatik düşer; gecikmiş tip aşırı duyarlılık (PPD cilt testi) tamamen kaybolur (**anerji**). "
            "2. **Mukozal Bariyer Yıkımı:** "
            "- Bağırsak epitel hücreleri hızla çoğalamaz; villus atrofisi gelişir. "
            "- Salgısal IgA (sIgA) üretimi durur; bağırsak florasındaki bakteriler kana sızarak **gram negatif sepsise** yol açar. "
            "3. **Fırsatçı ve Ağır Enfeksiyonlar:** "
            "- Bu çocuklar basit bir kızamık veya gastroenterit atağında bile hayatını kaybeder. "
            "- Gram negatif basiller, *Pneumocystis jirovecii*, tüberküloz ve yaygın pamukçuk (Kandida) ölümcül seyreder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Malnütrisyonda İmmün Çöküş ve Letal Enfeksiyon Zinciri",
                [
                    "1. Aminoasit Açlığı: Lenfoid organlarda protein sentezi ve hücre bölünmesinin durması",
                    "2. Timik İnvolüsyon: Timusun atrofiye uğrayarak T lenfosit üretimini durdurması",
                    "3. Hücresel Anerji: Dolaşımdaki T hücrelerinin felç olması ve fagositoz aktivitesinin çökmesi",
                    "4. Mukozal Translokasyon: İntestinal villus atrofisiyle bağırsak bakterilerinin kana karışması",
                    "5. Septik Şok: Gram negatif bakteriyemi ve fırsatçı patojenlerle fatal sepsis"
                ]
            ),
            make_cloze(
                "Şiddetli akut malnütrisyonlu çocuklarda T lenfosit üretiminin durmasına ve hücresel bağışıklığın çökmesine yol açan lenfoid organ büzüşmesine timik atrofi denir.",
                "timik atrofi",
                "Protein eksikliğinde göğüs kafesi içindeki primer T hücresi eğitim organının küçülüp körelmesi"
            )
        ]
    })

    # Slayt 69: Checkpoint 7
    slides.append({
        "id": "k1-26-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Protein-Enerji Malnütrisyonu (Marasmus vs Kwashiorkor)",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 69,
        "narrative": (
            "Yedinci kontrol noktamızda beslenme yetersizliği patolojisini ve iki büyük klinik sendromu pekiştiriyoruz: "
            "1. **Bölmeler:** Somatik bölme iskelet kasıdır; viseral bölme karaciğerin ürettiği albümindir. "
            "2. **Marasmus:** Kalori ve protein eşit yok; kaslar ve yağlar erir; albümin normaldir; yaşlı adam yüzü; ÖDEM YOKTUR. "
            "3. **Kwashiorkor:** Protein yok, karbonhidrat var; viseral bölme çöker, albümin <2.5 g/dL; yaygın nutrisyonel ödem ve asit. "
            "4. **Yağlı Karaciğer:** Kwashiorkorda apolipoprotein yapılamaz; trigliseridler karaciğerde kalır ve masif hepatomegali gelişir. "
            "5. **Deri ve Saç:** Kwashiorkorda flaky paint döküntüsü ve açık/koyu çizgili bayrak işareti (flag sign) saç görülür. "
            "6. **İmmünite:** Timus atrofisi ve T hücre çöküşü; çocuklar enfeksiyon ve gram negatif sepsis ile kaybedilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s09-1".replace("09", "69"),
                "Kalori ve protein eksikliğinin eşit derecede ağır olduğu, somatik iskelet kası ve deri altı yağ dokusunun tamamen tükendiği ancak ödemin görülmediği malnütrisyon formu nedir?",
                "Marasmus tablosudur.",
                "Somatik protein bölmesinin tükenmesiyle yaşlı adam yüzü görünümü veren saf açlık durumu",
                "Marasmus"
            ),
            make_flashcard(
                "k1-26-fc-s69-2",
                "Kalorinin nispeten korunduğu ancak protein alımının çok yetersiz olduğu, hipoalbüminemiye bağlı yaygın ödem ve karaciğer yağlanmasıyla seyreden malnütrisyon tablosu nedir?",
                "Kwashiorkor hastalığıdır.",
                "Erken sütten kesilen çocuklarda viseral protein çöküşü ve batında şişlik ile beliren durum",
                "Kwashiorkor"
            ),
            make_flashcard(
                "k1-26-fc-s69-3",
                "Kwashiorkor hastası çocukların saçlarında yetersiz beslenme dönemlerinde renk kaybı ve düzelme dönemlerinde koyulaşma ile ortaya çıkan karakteristik saç çizgilenmesine ne ad verilir?",
                "Bayrak işaretidir (flag sign).",
                "Saç tellerinde ardışık açık ve koyu bantların oluşturduğu morfolojik görüntü",
                "Kwashiorkor Bulguları"
            )
        ],
        "interactiveElements": [
            make_table(
                "Marasmus ve Kwashiorkor Checkpoint Karşılaştırması",
                ["Klinik Özellik", "Marasmus", "Kwashiorkor", "Tanısal Ayrım Püf Noktası"],
                [
                    ["Kardinal Belirteç", "Aşırı zayıflık, yaşlı adam yüzü", "Yaygın ödem, asit, hepatomegali", "Ödem varsa doğrudan Kwashiorkor"],
                    ["Albümin Düzeyi", "Korunmuş / Normal", "Ağır düşük (<2.5 g/dL)", "Viseral protein sentez yetersizliği"],
                    [
                        "Deri ve Saç",
                        "Kuru ve gevşek deri",
                        {"text": "Soyulmuş boya dermatiti ve bayrak işareti saç", "isMasked": True, "hint": "Protein yokluğunda saçta melanin sentezinin dalgalanmasıyla oluşan bantlar"},
                        "Dönemsel beslenme izleri"
                    ],
                    ["Hepatik Yağlanma", "Görülmez", "Belirgin (Masif steatoz)", "Apolipoprotein yokluğuna bağlı VLDL salgı yetmezliği"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi kwashiorkor hastalığında karaciğerde masif yağlanma (steatoz) ve belirgin hepatomegali gelişmesinin doğrudan biyokimyasal nedenidir?",
                {
                    "A": "Protein eksikliği nedeniyle trigliseridleri kanda taşıyacak apolipoproteinlerin sentezlenememesi",
                    "B": "Diyette aşırı miktarda doymuş hayvansal kolesterol alınması",
                    "C": "Safra kanallarının parazitlerle mekanik olarak tıkanması",
                    "D": "Karaciğerde glikojen depolarının aşırı şişmesi",
                    "E": "Hepatit B virüsünün karaciğeri istila etmesi"
                },
                "A",
                {
                    "A": "Doğrudur; protein yokluğunda apolipoprotein üretilemez, VLDL yapılamaz ve üretilen trigliseridler karaciğerden çıkamayıp hapsolur.",
                    "B": "Yanlış; çocuk proteinden yoksundur, hayvansal gıda alamaz.",
                    "C": "Yanlış; safra tıkanıklığı kolestaz yapar, steatoz yapmaz.",
                    "D": "Yanlış; glikojen birikimi değil, yağ birikimidir.",
                    "E": "Yanlış; viral hepatit değildir."
                }
            )
        ]
    })

    # Slayt 70: Erken Çocuklukta Malnütrisyon ve Beyin Gelişimi
    slides.append({
        "id": "k1-26-s70",
        "title": "Erken Çocuklukta Malnütrisyon ve Beyin Gelişimi",
        "section": "Beslenme Bozuklukları ve Malnütrisyon",
        "slideNumber": 70,
        "narrative": (
            "İnsan beyninin büyüme atağı intrauterin son trimesterde başlar ve yaşamın ilk iki yılında tamamlanır: "
            "1. **Kritik Gelişim Penceresi:** "
            "- İlk 2 yılda nöronal göç, dentritik dallanma, sinaptogenez ve oligodendrosit kaynaklı **aksonal miyelinizasyon** tavan yapar. "
            "2. **Malnütrisyonun Nöropatolojisi:** "
            "- İlk 1-2 yılda yaşanan ağır protein ve kalori eksikliği, beyin ağırlığında azalmaya (**mikrosefali**) ve "
            "serebral korteks hacminde küçülmeye yol açar. "
            "- Nöron sayısı azalır, sinaps yoğunluğu düşer ve miyelinizasyon kalıcı olarak aksar. "
            "3. **Geri Dönüşsüz Nörokognitif Hasar:** "
            "- İlerleyen yıllarda çocuk iyi beslense ve boy-kilosu düzelse bile, ilk iki yıldaki beyin gelişimi duraklaması "
            "tam olarak telafi edilemez! "
            "- Bu çocuklarda kalıcı IQ kayıpları, öğrenme güçlüğü, soyut düşünme becerisinde gerilik ve "
            "okul terk oranlarında belirgin artış saptanır. Bu nedenle erken çocuklukta malnütrisyonla mücadele ulusal bir beka konusudur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Erken Çocukluk Malnütrisyonunun Beyne Kısa ve Uzun Dönem Etkisi",
                "Akut Dönem (İlk 2 Yaş)",
                "Serebral hipoplazi, nöronal sinaps sayısında azalma ve oligodendrosit miyelinizasyonunun duraklaması",
                "Uzun Dönem (Erişkinlik)",
                "Beslenme düzeltilse dahi telafi edilemeyen kalıcı IQ düşüklüğü, bilişsel gerilik ve motor beceri kayıpları"
            ),
            make_active_recall(
                "Yaşamın ilk iki yılında geçirilen şiddetli akut protein-enerji malnütrisyonunun ileride çocuk iyi beslense dahi tam olarak düzeltilemeyen en ağır geri dönüşümsüz kalıcı komplikasyonu nedir?",
                "Kalıcı nörokognitif kayıplar ve zihinsel gelişim geriliğidir.",
                "Sinaptogenez ve miyelinizasyon penceresinin kaçırılması sonucu oluşan zeka düşüşü"
            )
        ]
    })

    return slides
