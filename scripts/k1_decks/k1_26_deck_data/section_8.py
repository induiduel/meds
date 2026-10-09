# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 8: Yeme Bozuklukları, Obezite ve Enerji Homeostazı (Slayt 71-80)
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

def get_section_8_slides():
    slides = []

    # Slayt 71: Yeme Bozuklukları Spektrumu
    slides.append({
        "id": "k1-26-s71",
        "title": "Yeme Bozuklukları Spektrumu: Anoreksiya ve Bulimia",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 71,
        "narrative": (
            "Yeme bozuklukları, çarpık beden algısı ve kilo alma korkusu ile karakterize, "
            "psikiyatrik temelli ancak ölümcül somatik ve metabolik komplikasyonlar doğuran hastalıklardır: "
            "1. **Anoreksiya Nervoza:** "
            "- Bireyin gerçek dışı şişmanlık hezeyanı ile **kendine zorunlu açlık uygulaması** ve aşırı kilo kaybetmesidir. "
            "- Genellikle mükemmeliyetçi genç kızlarda ve adölesanlarda başlar. Vücut kitle indeksi sıklıkla <17.5 kg/m²'dir. "
            "2. **Bulimia Nervoza:** "
            "- Tekrarlayan kontrolsüz aşırı tıkınırcasına yeme nöbetleri (binge eating), peşinden gelen suçlulukla "
            "kilo almayı önlemek için **kendini zorla kusturma**, laksatif veya diüretik kötüye kullanımıdır. "
            "- Bulimikler genellikle normal kiloda veya hafif kiloludur; bu nedenle anoreksiyadan daha gizli seyreder. "
            "3. **Mortalite:** Anoreksiya nervoza, tüm psikiyatrik hastalıklar arasında **en yüksek ölüm oranına sahip bozukluktur** "
            "(ölümlerin yarısı kardiyak arrest/aritmi, diğer yarısı intihardır)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Anoreksiya Nervoza ve Bulimia Nervoza Karşılaştırması",
                ["Klinik Özellik", "Anoreksiya Nervoza", "Bulimia Nervoza"],
                [
                    ["Beden Kitle İndeksi (VKİ)", "Aşırı düşük (<17.5 kg/m²), kaşektik", "Genellikle normal veya hafif kilolu"],
                    ["Yeme Davranışı", "Kendini aç bırakma, katı kalori kısıtlaması", "Tıkınırcasına aşırı yeme + arınma (kusma)"],
                    [
                        "Kardinal Endokrin Bulgusu",
                        {"text": "GnRH baskılanmasına bağlı sekonder amenore", "isMasked": True, "hint": "Aşırı zayıflık ve leptin düşüklüğü sonucu menstrüel döngünün kesilmesi"},
                        "Düzensiz adetler, amenore nadir"
                    ],
                    ["Kusma Komplikasyonu", "Nadir (Kısıtlayıcı tipte)", "Diş minesi erozyonu, parotis şişmesi, Mallory-Weiss"]
                ]
            ),
            make_active_recall(
                "Tıkınırcasına aşırı yeme ataklarının ardından parmakla kendini kusturma davranışı sergileyen ve diş hekimine başvurduğunda lingual diş minelerinde yaygın asit erozyonu saptanan genç hastada tanı nedir?",
                "Bulimia nervozadır.",
                "Mide asidinin ağız içine reflüsüyle diş minesini eritmesi tablosu"
            )
        ]
    })

    # Slayt 72: Anoreksiya Nervoza Patolojisi ve Endokrin Çöküş
    slides.append({
        "id": "k1-26-s72",
        "title": "Anoreksiya Nervoza Patolojisi ve Endokrin Çöküş",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 72,
        "narrative": (
            "Anoreksiya nervoza, vücuttaki enerji depolarının tükenmesiyle hipotalamik kontrol merkezlerinin tamamen kilitlendiği tablodur: "
            "1. **Hipotalamik-Hipofizer Aksın Çöküşü (Amenore):** "
            "- Adipoz doku eridiğinde leptin hormonu sıfırlanır; hipotalamustan **GnRH salınımı durur**. "
            "- Hipofizden LH ve FSH salgılanamaz; overlerde folikül gelişimi ve östrojen üretimi durur. "
            "- **Sekonder Amenore:** Anoreksiyanın kardinal tanısal belirtisidir (menstrüasyon tamamen kesilir). "
            "2. **Tiroid ve Isı Regülasyonu:** "
            "- T3 ve T4 hormon düzeyleri düşer; bazal metabolizma hızı düşürülür. "
            "- Şiddetli **soğuk intoleransı**, bradikardi, hipotansiyon ve vücutta ince tüylenme (**lanugo kılları**) gelişir. "
            "3. **Kemik Kaybı (Osteoporoz):** "
            "- Ağır östrojen eksikliği ve kortizol yüksekliği nedeniyle genç yaşta **şiddetli osteopeni ve osteoporoz** gelişir; "
            "omurga ve kalça kırıkları riski fırlar. "
            "4. **Kardiyak Ölüm:** Elektrolit dengesizliği (hipokalemi) ve miyokard atrofisi sonucu letal ventriküler aritmiler (QT uzaması)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Anoreksiyada Hipotalamik Kapanma ve Amenore Basamakları",
                [
                    "1. Şiddetli Açlık: Vücut yağ dokusunun erimesi ve plazma leptin düzeyinin dip yapması",
                    "2. GnRH Baskılanması: Hipotalamusun pulsatil GnRH nörosekresyonunu tamamen durdurması",
                    "3. Gonadotropin Çöküşü: Hipofiz ön lobundan LH ve FSH salgısının sıfırlanması",
                    "4. Hipoöstrojenizm: Overlerin hormon üretememesi ve endometrium proliferasyonunun durması",
                    "5. Sekonder Amenore: Menstrüel siklusun kesilmesi ve kemik dansitesinin hızla erimesi"
                ]
            ),
            make_cloze(
                "Anoreksiya nervozada adipoz doku kaybı sonucu hipotalamusta GnRH salınımının durması genç kadınlarda sekonder amenore tablosuna yol açar.",
                "sekonder amenore",
                "Daha önce adet gören bir kadında menstrüel kanamanın aylar boyunca kesilmesi"
            )
        ]
    })

    # Slayt 73: Bulimia Nervoza ve Kusma Komplikasyonları
    slides.append({
        "id": "k1-26-s73",
        "title": "Bulimia Nervoza ve Kusma Komplikasyonları",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 73,
        "narrative": (
            "Bulimia nervozanın morbidite ve mortalitesi, tekrarlayan kusma ve laksatif kötüye kullanımının yarattığı metabolik travmadır: "
            "1. **Hipokalemi ve Kardiyak Aritmi (En Letal Tehlike):** "
            "- Kusma ile mide asidi ($HCl$) ve kalsiyum/potasyum kaybedilir; sekonder hiperaldosteronizm ile böbrekten de $K^+$ atılır. "
            "- **Şiddetli Hipokalemi ($K^+ < 3.0 mEq/L$):** Kardiyak elektriksel repolarizasyonu bozar; QT mesafesini uzatır, "
            "Torsades de Pointes ve **ölümcül ventriküler fibrilasyona** yol açar. Bulimiklerin en sık ani ölüm nedenidir! "
            "2. **Metabolik Alkaloz:** Mide asidinin ($H^+$ ve $Cl^-$) kaybı sonucu hipokloremik metabolik alkaloz gelişir. "
            "3. **Mekanik Gastrointestinal Travmalar:** "
            "- **Mallory-Weiss Yırtığı:** Şiddetli öğürme sonucu gastroözofageal bileşkede mukozal longitudinal yırtılma ve masif hematemez. "
            "- **Boerhaave Sendromu:** Özofagusun tam kat rüptürü ve mediastinit (yüksek oranda ölümcül). "
            "- Kronik tükürük bezi uyarısıyla bilateral parotis bezinde ağrısız büyüme (siyaloenozis)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tekrarlayan Kusmanın Patolojik ve Anatomik İmzaları",
                ["Hedef Organ / Parametre", "Patolojik Bulgusu", "Tetikleyici Mekanizma"],
                [
                    ["Serum Potasyumu", "Ağır hipokalemi ve letal aritmi", "Mide asidi kaybı ve renal potasyum atılımı"],
                    ["Gastroözofageal Bileşke", "Mallory-Weiss mukozal laserasyonu", "Şiddetli öğürme ve intralüminal basınç artışı"],
                    [
                        "Dişlerin Lingual Yüzü",
                        {"text": "Perimolizis (diş minesi kimyasal erozyonu)", "isMasked": True, "hint": "Kusma sırasında hidroklorik asidin ön kesici dişlerin arka yüzeyini eritmesi"},
                        "Mide hidroklorik asit (HCl) reflüsü"
                    ],
                    ["Tükürük Bezleri", "Bilateral parotidomegali (parotis şişmesi)", "Kronik asit irritasyonuna bağlı bez hipertrofisi"],
                    ["El Sırtı Derisi", "Russell belirtisi (eklem üzeri nasır)", "Kusmayı başlatmak için parmak sokarken dişlerin sürtünmesi"]
                ]
            ),
            make_active_recall(
                "Bulimia nervozada parmakla boğazı uyararak kusma refleksi oluşturma alışkanlığına bağlı olarak el sırtı metakarpofalangeal eklem derisinde oluşan nasırlaşma lezyonuna ne ad verilir?",
                "Russell belirtisidir (Russell sign).",
                "Kusma indüksiyonu sırasında dişlerin el sırtını travmatize etmesiyle oluşan kutanöz lezyon"
            )
        ]
    })

    # Slayt 74: Obezite Epidemiyolojisi ve Viseral Yağ
    slides.append({
        "id": "k1-26-s74",
        "title": "Obezite Epidemiyolojisi ve Viseral Yağlanmanın Önemi",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 74,
        "narrative": (
            "Obezite, vücutta sağlık için risk oluşturacak düzeyde aşırı veya anormal yağ birikimidir: "
            "1. **Beden Kitle İndeksi (VKİ / BMI):** Ağırlığın boyun karesine bölünmesiyle hesaplanır ($kg/m^2$): "
            "- 18.5 - 24.9: Normal "
            "- 25.0 - 29.9: Fazla kilolu (Overweight) "
            "- **≥ 30.0: Obez** "
            "- **≥ 40.0: Morbid Obez**. "
            "2. **Yağın Dağılımı ve Viseral Yağ (Kritik Patolojik İlke):** "
            "- Obezitede morbiditeyi belirleyen toplam kilo değil, **yağın nerede toplandığıdır**! "
            "- **Deri Altı (Subkütan) Yağlanma (Armut Tipi):** Gluteal ve uyluk bölgesinde birikir; metabolik riski düşüktür. "
            "- **Viseral (Abdominal / Karın İçi) Yağlanma (Elma Tipi):** Omentum ve mezenter çevresinde, iç organlar etrafında birikir. "
            "Bel çevresi ölçümüyle saptanır (Erkekte >102 cm, Kadında >88 cm risk eşiğidir). "
            "- Viseral adipositler lipolitik olarak aşırı aktiftir; portal dolaşıma doğrudan serbest yağ asitleri (FFA) pompalar, "
            "karaciğeri yağlandırır ve **insülin direnci ile metabolik sendromu** ateşler!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Subkütan (Armut) vs Viseral (Elma) Yağlanma Zıtlığı",
                "Subkütan Yağlanma (Gluteofemoral / Armut)",
                "Deri altında toplanır; portal dolaşıma dökülmez; insülin direnci ve metabolik sendrom riski düşüktür",
                "Viseral Yağlanma (Abdominal / Elma)",
                "Omentum ve mezenterde toplanır; portal vene serbest yağ asidi boşaltır; diyabet, hipertansiyon ve aterosklerozu fırlatır"
            ),
            make_micro_quiz(
                "Metabolik sendrom, tip 2 diyabet ve aterosklerotik kardiyovasküler hastalık riski açısından vücuttaki toplam yağ miktarından çok daha belirleyici olan ve portal dolaşıma serbest yağ asitleri pompalayan yağ dağılım bölgesi hangisidir?",
                {
                    "A": "Viseral (abdominal / omental) yağ dokusu",
                    "B": "Gluteal deri altı yağ dokusu",
                    "C": "Ayak tabanı yağ yastıkçıkları",
                    "D": "Orbita içi retrobulber yağ dokusu",
                    "E": "Diz eklemi Hoffa yağ yastığı"
                },
                "A",
                {
                    "A": "Doğrudur; viseral yağ metabolik olarak çok aktiftir ve portal dolaşım yoluyla doğrudan karaciğeri insülin direncine sokar.",
                    "B": "Yanlış; gluteal yağ armut tipidir, metabolik riski düşüktür.",
                    "C": "Yanlış; mekanik destek yağıdır.",
                    "D": "Yanlış; retrobulber yağ metabolik risk oluşturmaz.",
                    "E": "Yanlış; eklem içi koruyucu yağdır."
                }
            )
        ]
    })

    # Slayt 75: Enerji Dengesi ve Hipotalamik Regülasyon
    slides.append({
        "id": "k1-26-s75",
        "title": "Enerji Dengesi ve Hipotalamik Regülasyon",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 75,
        "narrative": (
            "Vücut ağırlığı, enerji alımı ile harcanması arasındaki karmaşık nöroendokrin döngüyle (**lipostat sistemi**) sabit tutulur: "
            "1. **Merkezi Kontrol Üssü: Hipotalamus Arkuat Çekirdeği:** "
            "- Arkuat çekirdekte birbirine zıt çalışan iki ana nöron grubu yer alır: "
            "2. **POMC / CART Nöronları (Anoreksijenik / İştah Kapatıcı Yolak):** "
            "- Pro-opiomelanokortin (POMC) ve kokain-amfetamin düzenleyici transkript (CART) üretirler. "
            "- Alfa-MSH salgılayarak 2. sıra nöronlardaki **Melanokortin 4 Reseptörünü (MC4R)** uyarırlar. "
            "- **Sonuç:** İştahı kapatır (tokluk hissi) ve sempatik tonusu artırarak **enerji harcamasını hızlandırır**. "
            "MC4R mutasyonları monogenik insan obezitesinin en sık nedenidir! "
            "3. **NPY / AgRP Nöronları (Oreksijenik / İştah Açıcı Yolak):** "
            "- Nöropeptid Y (NPY) ve Agouti-related peptide (AgRP) üretirler. "
            "- MC4R'ı bloke eder ve paraventriküler çekirdeği uyararak **açlık hissi doğurur, iştahı patlatır** ve enerji harcamasını kısar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Hipotalamik Arkuat Çekirdeğin İki Zıt Nöron Grubu",
                ["Nöron Popülasyonu", "Salgılanan Mediyatörler", "Hedef Reseptör ve Net Fizyolojik Etki"],
                [
                    ["POMC / CART Nöronları", "alfa-MSH ve CART", "MC4R aktivasyonu: İştahı baskılar, metabolizmayı hızlandırır (Tokluk)"],
                    [
                        "NPY / AgRP Nöronları",
                        "Nöropeptid Y ve AgRP",
                        {"text": "MC4R inhibisyonu: İştahı açar, enerji tasarrufu sağlar (Açlık)", "isMasked": True, "hint": "Gıda alımını çılgınca artıran oreksijenik hipotalamik nöron grubu"}
                    ]
                ]
            ),
            make_active_recall(
                "İnsanlarda erken başlangıçlı monogenik şiddetli obezitenin en sık nedeni olan ve hipotalamusta tokluk sinyalini ileten melanokortin reseptörü hangisidir?",
                "Melanokortin 4 Reseptörüdür (MC4R).",
                "POMC nöronlarından salınan alfa-MSH ile uyarılan iştah frenleyici reseptör"
            )
        ]
    })

    # Slayt 76: Yağ Dokusu Hormonları 1: Leptin ve Leptin Direnci
    slides.append({
        "id": "k1-26-s76",
        "title": "Yağ Dokusu Hormonları 1: Leptin ve Leptin Direnci",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 76,
        "narrative": (
            "Yağ dokusu pasif bir trigliserid deposu değil, vücudun en büyük aktif endokrin organlarından biridir: "
            "1. **Leptin (Lipostatın Bekçisi):** "
            "- 16 kDa ağırlığında bir proteindir; neredeyse tamamen beyaz adipositler tarafından sentezlenir. "
            "- Dolaşımdaki leptin düzeyi, vücuttaki **toplam yağ kütlesiyle doğrudan doğru orantılıdır**. "
            "2. **Etki Mekanizması:** "
            "- Kan-beyin bariyerini geçerek hipotalamus arkuat çekirdeğindeki leptin reseptörlerine (Ob-R) bağlanır. "
            "- İştah kapatıcı **POMC/CART nöronlarını uyarır**; iştah açıcı **NPY/AgRP nöronlarını baskılar**. "
            "- Beyne 'Depolar dolu, yemek yemeyi durdur ve enerji harca!' mesajı iletir. "
            "3. **Obezitede Leptin Paradoksu ve Leptin Direnci:** "
            "- İnsan obezitesi (çok nadir konjenital leptin mutasyonları hariç) leptin eksikliğinden kaynaklanmaz! "
            "- Tam aksine obez bireylerin kanında **leptin düzeyleri tavan yapmıştır**. "
            "- Ancak hipotalamik reseptör taşıma mekanizmalarında ve hücre içi sinyal yolaklarında (SOCS3 artışı) **leptin direnci** gelişmiştir. "
            "Beyin yüksek leptini 'göremez'; kendini açlıkta sanarak iştahı açık tutmaya devam eder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Normal vs Obez Bireyde Leptin Sinyalizasyonu",
                "Normal Birey (Duyarlı Hipotalamus)",
                "Yağ deposu artınca leptin yükselir; hipotalamus tokluk hisseder, gıda alımı durur ve kilo dengelenir",
                "Obez Birey (Leptin Direnci)",
                "Kanda devasa leptin fazlalığı vardır; ancak reseptör direnci nedeniyle beyin sinyali algılayamaz ve iştahı kapatamaz"
            ),
            make_cloze(
                "Obez bireylerde yağ kütlesinin artışına paralel olarak kanda leptin düzeyi çok yüksek olduğu halde tokluk hissinin oluşamaması tablosuna leptin direnci adı verilir.",
                "leptin direnci",
                "Hipotalamustaki doygunluk almacının yüksek hormon düzeyine karşı duyarsızlaşması fenomeni"
            )
        ]
    })

    # Slayt 77: Yağ Dokusu Hormonları 2: Adiponektin
    slides.append({
        "id": "k1-26-s77",
        "title": "Yağ Dokusu Hormonları 2: Adiponektin",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 77,
        "narrative": (
            "Adiponektin, adipositler tarafından üretilen 'mucizevi koruyucu adipokin' olarak tanımlanır: "
            "1. **Fizyolojik Görevleri (Metabolik Koruyucu):** "
            "- İskelet kası ve karaciğerdeki AdipoR1 ve AdipoR2 reseptörlerine bağlanarak **AMPK (AMP-aktive protein kinaz)** yolağını uyarır. "
            "- Karaciğerde glukoneogenezi baskılar, glukoz kullanımını ve yağ asidi beta-oksidasyonunu hızlandırır. "
            "- **İnsülin Duyarlılığını Artırır:** Dokuların insüline yanıtını mükemmelleştirir (anti-diyabetik etki). "
            "- **Anti-aterojenik ve Anti-enflamatuar Etki:** Endotelde monosit adezyonunu engeller, düz kas proliferasyonunu durdurur. "
            "2. **Adiponektin Paradoksu (Obezitede Çöküş):** "
            "- Leptin, rezistin ve sitokinler (TNF-alfa, IL-6) obezitede artarken; **adiponektin yağ kütlesi arttıkça PARADOKSAL OLARAK AZALIR!** "
            "- Obez bireylerde adiponektin düzeyleri taban yapar. "
            "- Adiponektin korumasından mahrum kalan organizmada **ağır insülin direnci, endotel disfonksiyonu ve ateroskleroz** hızla patlak verir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Leptin ve Adiponektin Zıtlığı Matrisi",
                ["Karakteristik Özellik", "Leptin", "Adiponektin"],
                [
                    ["Obezitedeki Kan Düzeyi", "YÜKSEK (Aşırı artar)", "DÜŞÜK (Paradoksal olarak çöker)"],
                    ["Primer Hedef Organ", "Hipotalamus arkuat çekirdeği", "İskelet kası, karaciğer ve endotel"],
                    ["Metabolik Fonksiyon", "İştahı kapatmak (Lipostat)", "İnsülin duyarlılığı ve yağ asidi oksidasyonu artırmak"],
                    [
                        "Klinik Önemi",
                        "Obezitede leptin direnci vardır",
                        {"text": "Eksikliği insülin direnci ve diyabete zemin hazırlar", "isMasked": True, "hint": "Koruyucu hormonun düşmesiyle glukoz intoleransı ve aterosklerozun patlaması"}
                    ]
                ]
            ),
            make_active_recall(
                "Yağ dokusu tarafından sentezlenen diğer tüm hormon ve sitokinlerin aksine, obezite ve viseral yağ kütlesi arttıkça plazma konsantrasyonu paradoksal olarak AZALAN koruyucu adipokin nedir?",
                "Adiponektindir.",
                "AMPK enzimini uyararak insülin duyarlılığı sağlayan koruyucu yağ hormonu"
            )
        ]
    })

    # Slayt 78: Obezitenin Metabolik Komplikasyonları
    slides.append({
        "id": "k1-26-s78",
        "title": "Obezitenin Metabolik Komplikasyonları: NAFLD ve Ateroskleroz",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 78,
        "narrative": (
            "Obezite, tüm organ sistemlerinde geri dönüşümsüz yapısal ve metabolik hasarlara yol açar: "
            "1. **Tip 2 Diyabet:** Artmış serbest yağ asitleri (FFA) ve TNF-alfa, insülin reseptör substratlarını (IRS-1) "
            "serin rezidülerinden fosforilleyerek insülin sinyalini kilitler; pankreas beta hücreleri tükenir ve açık diyabet gelişir. "
            "2. **Metabolik Sendrom Triadı:** Abdominal obezite + Hipertansiyon + Aterojenik dislipidemi (Yüksek trigliserid, düşük HDL). "
            "3. **Alkolsüz Yağlı Karaciğer Hastalığı (NAFLD / NASH):** "
            "- Obezite günümüzde kronik karaciğer hastalığının bir numaralı nedenidir. "
            "- Basit steatoz -> **Non-Alkolik Steatohepatit (NASH)** -> Siroz -> Hepatoselüler karsinom (HCC) zinciri. "
            "4. **Kardiyovasküler:** Sol ventrikül hipertrofisi, koroner ateroskleroz, inme ve kalp yetmezliği. "
            "5. **Diğer Komplikasyonlar:** Safra kesesinde kolesterol aşırı doygunluğuyla **kolelitiyazis (safra taşları)**; "
            "eklemlere binen mekanik yükle **osteoartrit**; obstrüktif uyku apnesi (Pickwick sendromu)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Obeziteden Non-Alkolik Steatohepatite (NASH) Giden Yolak",
                [
                    "1. Viseral Lipoliz: Karın içi yağ dokusundan portal vene aşırı serbest yağ asidi (FFA) boşalması",
                    "2. Hepatik Steatoz: Karaciğer hepatositlerinde trigliserid birikmesiyle basit yağlanma oluşması",
                    "3. Lipid Peroksidasyonu: Aşırı yağ asitlerinin mitokondride serbest radikaller ve oksidatif stres üretmesi",
                    "4. Steatohepatit (NASH): Hepatosit balonlaşması, nekroz ve Mallory-Denk benzeri cisimcikler",
                    "5. İlerleyici Siroz: Stellat hücrelerin kollajen depolamasıyla geri dönüşsüz mikronodüler siroz"
                ]
            ),
            make_cloze(
                "Obez bireylerde karaciğerde basit yağlanmanın hepatosit hasarı, inflamasyon ve Mallory-Denk cisimcikleriyle ilerlemiş inflamatuar formuna non-alkolik steatohepatit adı verilir.",
                "non-alkolik steatohepatit",
                "Alkol kullanımı olmaksızın gelişen fibrozis ve siroza ilerleyebilen yağlı karaciğer iltihabı"
            )
        ]
    })

    # Slayt 79: Checkpoint 8
    slides.append({
        "id": "k1-26-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Yeme Bozuklukları ve Obezite Biyolojisi",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 79,
        "narrative": (
            "Sekizinci kontrol noktamızda yeme bozukluklarını ve obezite patolojisini özetliyoruz: "
            "1. **Anoreksiya Nervoza:** Kendini aç bırakma, aşırı kilo kaybı (<17.5 VKİ); GnRH baskılanmasıyla sekonder amenore; osteoporoz. "
            "2. **Bulimia Nervoza:** Tıkınırcasına yeme ve kusma; hipokalemiye bağlı ölümcül ventriküler aritmi; diş erozyonu ve Russell belirtisi. "
            "3. **Viseral Yağ:** Portal dolaşıma FFA pompalar; insülin direnci ve metabolik sendromun ana kaynağıdır (elma tipi obezite). "
            "4. **Hipotalamik Merkez:** POMC/CART tokluk hissi verir (MC4R aktivasyonu); NPY/AgRP açlık hissi doğurur. "
            "5. **Leptin:** Yağ dokusundan salınır, tokluk verir; obezlerde kanda çok yüksektir ancak leptin direnci nedeniyle işlevsizdir. "
            "6. **Adiponektin:** İnsülin duyarlılığını artırır ve yağ yakar; obezitede paradoksal olarak düşer!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-26-fc-s79-1",
                "Anoreksiya nervozada GnRH salınımının durması ve gonadotropinlerin düşmesi sonucu genç kadınlarda ortaya çıkan kardinal endokrin bulgu nedir?",
                "Sekonder amenoredir (adet görememe).",
                "Hipotalamik aks baskılanmasıyla menstrüel siklusun kesilmesi",
                "Anoreksiya"
            ),
            make_flashcard(
                "k1-26-fc-s79-2",
                "Adipoz dokudan salgılanarak hipotalamusta iştahı baskılayan ancak obez bireylerde reseptör düzeyinde direnç geliştiği için kanda çok yüksek bulunan hormon nedir?",
                "Leptin hormonudur.",
                "Yağ kütlesi arttıkça yükselen ve tokluk hissi oluşturan lipostat habercisi",
                "Leptin"
            ),
            make_flashcard(
                "k1-26-fc-s79-3",
                "Yağ dokusu tarafından salgılanan, insülin duyarlılığını artıran ve yağ oksidasyonunu hızlandıran ancak obezlerde diğer yağ hormonlarının aksine paradoksal olarak azalan hormon nedir?",
                "Adiponektin hormonudur.",
                "Karaciğer ve kaslarda glukoz kullanımını artıran koruyucu yağ dokusu peptidi",
                "Adiponektin"
            )
        ],
        "interactiveElements": [
            make_table(
                "Yeme Bozuklukları ve Obezite Checkpoint Matrisi",
                ["Durum / Hormon", "Primer Patofizyolojik Değişim", "Kritik Klinik / Laboratuvar Belirteç", "Majör Mortalite Riski"],
                [
                    ["Anoreksiya Nervoza", "Gıdayı reddetme, hipotalamik aks çöküşü", "Sekonder amenore, lanugo, osteoporoz", "Aritmi ve intihar"],
                    ["Bulimia Nervoza", "Aşırı yeme nöbeti ve kendini kusturma", "Hipokalemi, diş erozyonu, parotidomegali", "Letal kardiyak aritmi"],
                    [
                        "Leptin",
                        "Yağ dokusundan salınan tokluk hormonu",
                        {"text": "Obezitede kanda çok yüksek fakat reseptörde dirençli", "isMasked": True, "hint": "Hormon düzeyinin artmasına rağmen hipotalamusun doygunluk algılayamaması"},
                        "Durdurulamayan aşırı kalori alımı"
                    ],
                    ["Adiponektin", "AMPK aktivatörü koruyucu adipokin", "Obezitede paradoksal olarak dip yapar", "İnsülin direnci ve diyabet"]
                ]
            ),
            make_micro_quiz(
                "Bulimia nervoza tanılı bir hastada kendini kusturma davranışı sonrasında serum biyokimyasında saptanan ve ventriküler taşikardi/fibrilasyon gibi ölümcül aritmileri tetikleyen en tehlikeli elektrolit bozukluğu nedir?",
                {
                    "A": "Ağır hipokalemi (serum potasyum düşüklüğü)",
                    "B": "Aşırı hiperkalsemi",
                    "C": "Hiperpotasemi",
                    "D": "Hipofosfatemi",
                    "E": "Hipernatremi"
                },
                "A",
                {
                    "A": "Doğrudur; mide içeriğiyle asit ve potasyum kaybı ağır hipokalemiye yol açar ve QT uzamasıyla ölümcül aritmiler yapar.",
                    "B": "Yanlış; hiperkalsemi kusmayla gelişmez.",
                    "C": "Yanlış; potasyum yükselmez, tam aksine düşer.",
                    "D": "Yanlış; primer tehlike potasyum kaybıdır.",
                    "E": "Yanlış; dehidratasyona rağmen ana aritmi sebebi hipokalemidir."
                }
            )
        ]
    })

    # Slayt 80: Obezite ve Kanser İlişkisi
    slides.append({
        "id": "k1-26-s80",
        "title": "Obezite ve Kanser İlişkisi: Moleküler Mekanizmalar",
        "section": "Yeme Bozuklukları ve Obezite",
        "slideNumber": 80,
        "narrative": (
            "Sigaradan sonra önlenebilir kanser ölümlerinin dünyadaki en büyük ikinci nedeni obezitedir: "
            "1. **Hiperinsülinemi ve IGF-1 Ekseni:** "
            "- İnsülin direnci nedeniyle pankreas kanda devasa insülin biriktirir (kompansatuar hiperinsülinemi). "
            "- Yüksek insülin karaciğerde **IGF-1 (İnsülin Benzeri Büyüme Faktörü-1)** sentezini artırır; IGF-bağlayıcı proteinleri (IGFBP) baskılar. "
            "- Serbest IGF-1, tümör hücrelerindeki IGF-1R reseptörlerine bağlanarak **RAS/MAPK ve PI3K/AKT yolaklarını** ateşler; "
            "hücre proliferasyonunu hızlandırır ve apoptozu engeller. "
            "2. **Adipoz Aromataz ve Östrojen Patlaması (Kadın Kanserleri):** "
            "- Yağ dokusu **Aromataz** enzimini yoğun olarak içerir. "
            "- Adrenal androjenler yağ dokusunda **östron ve östradiole** dönüştürülür. "
            "- Menopoz sonrası kadınlarda karşılanmamış aşırı östrojen seviyesi **Endometrium Karsinomu riskini 5-6 kat**, "
            "hormon reseptör pozitif **Meme Kanseri** riskini ise 2 kat artırır! "
            "3. **Diğer Obezite Kanserleri:** Kolorektal karsinom, özofagus adenokarsinomu (reflü zemininde), böbrek (RCC) ve safra kesesi kanseri."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Genetik, Pediatrik ve Çevresel Patoloji (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Obezitede Karsinojenez Mekanizmaları ve Hedef Organlar",
                ["Moleküler Mekanizma", "Biyolojik Süreç", "İlişkili Kanser Türleri"],
                [
                    ["Hiperinsülinemi ve IGF-1 Artışı", "PI3K/AKT yolağı ile mitoz uyarımı ve apoptoz blokajı", "Kolorektal karsinom, prostat kanseri"],
                    [
                        "Adipoz Aromataz Aktivitesi",
                        "Androjenlerin östrojene çevrilmesi ve karşılanmamış östrojen",
                        {"text": "Endometrium karsinomu ve postmenopozal meme kanseri", "isMasked": True, "hint": "Yağ dokusunda östrojen sentezi artışıyla tetiklenen kadın genital organ kanserleri"}
                    ],
                    ["Kronik Düşük Düzeyli İnflamasyon", "Makrofaj kaynaklı TNF-alfa ve IL-6 karsinojenez uyarımı", "Hepatoselüler karsinom, özofagus adenokarsinomu"]
                ]
            ),
            make_active_recall(
                "Menopoz sonrası obez kadınlarda yağ dokusundaki aromataz enziminin androjenleri östrojene çevirmesi sonucu en dramatik şekilde (5-6 kat) insidansı artan jinekolojik malignite hangisidir?",
                "Endometrium karsinomudur (rahim kanseri).",
                "Karşılanmamış kronik östrojen uyarısıyla gelişen uterus mukozası kanseri"
            )
        ]
    })

    return slides
