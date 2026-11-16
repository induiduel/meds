# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 10: Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez (Slayt 91 - 100)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: 1. Evre: İlerlemeyen (Nonprogresif / Kompanse) Evre
    slides.append({
        "id": "k1-24-s91",
        "title": "1. Evre: İlerlemeyen (Nonprogresif / Kompanse) Evre",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 91,
        "narrative": (
            "Şok tablosu aniden ölümle sonuçlanmaz; patolojik olarak net sınırlarla ayrılan üç dinamik evreden geçer: "
            "1. **Evre Tanımı:** İlerlemeyen (kompanse) evrede, refleks nörohumoral mekanizmalar kardiyak debiyi ve arteriyel "
            "basıncı sürdürmek için derhal devreye girer. "
            "2. **Kompansatuar Mekanizmalar:** "
            "- **Baroreseptör Refleksleri:** Aort kavsi ve karotis sinüs geriminin azalmasıyla sempatik deşarj tetiklenir; taşikardi başlar. "
            "- **Katekolamin Salınımı:** Adrenalin ve noradrenalin salınır; cilt, kas ve visseral organlarda vazokonstriksiyon yapılır. "
            "- **RAAS Aksı:** Renal perfüzyon düşünce renin salınır; anjiyotensin II damarları büzer, aldosteron sodyum ve su tutar. "
            "- **ADH Salınımı:** Hipofiz arka lobundan salınan vazopressin suyu geri emerek intravasküler hacmi korur. "
            "3. **Klinik Görünüm:** Kutanöz vazokonstriksiyonla cilt soğuk ve soluktur, taşikardi vardır, böbrekte sıvı tutulumuyla oligüri "
            "başlar. Ancak koroner ve serebral perfüzyon tam olarak korunur; hasta bilinci açıktır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "İlerlemeyen Evre Kompansasyon Kaskadı",
                [
                    "1. Basınç Düşüşü: Etkin dolaşan kan hacminin azalması ve arteriyel baroreseptör deşarjının tetiklenmesi",
                    "2. Sempatik Deşarj: Taşikardi, periferik arteriyoler vazokonstriksiyon ve ciltte solukluk",
                    "3. RAAS ve ADH Aktivasyonu: Böbreklerden su ve sodyum geri emilimi ile intravasküler hacmin korunması",
                    "4. Selektif Perfüzyon: Kan akımının deri ve böbrekten çekilerek beyin ve koroner dolaşıma yönlendirilmesi"
                ]
            ),
            make_cloze(
                "Şokun ilerlemeyen erken kompanse evresinde böbreklerden su ve tuz tutulumunu sağlayan temel hormonal aks RAAS sistemidir.",
                "RAAS",
                "Renin anjiyotensin aldosteron sisteminin standart medikal kısaltması"
            )
        ]
    })

    # Slayt 92: 2. Evre: İlerleyici (Progresif) Evre
    slides.append({
        "id": "k1-24-s92",
        "title": "2. Evre: İlerleyici (Progresif) Evre: Doku Asidozu ve Göllenme",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 92,
        "narrative": (
            "Altta yatan primer neden hızla düzeltilmediğinde şok ikinci aşama olan ilerleyici (progresif) evreye geçer: "
            "1. **Yaygın Doku Hipoperfüzyonu:** Kompansatuar vazokonstriksiyon uzadıkça periferik dokular ağır hipoksiye maruz kalır. "
            "2. **Laktik Asidoz ve Vazomotor Felç:** Hücreler zorunlu anaerobik glikolize geçer; dokularda laktik asit birikir. "
            "Lokal asidoz ve metabolitler prekapiller arteriyol sfinkterlerini gevşetir; ancak postkapiller venüller dar kalmaya devam eder. "
            "3. **Mikrosirkülasyonda Göllenme (Pooling):** Kan mikrodolaşımda havuzlanır; hidrostatik basınç artışı sıvıyı interstisyuma iter. "
            "Efektif kardiyak venöz dönüş daha da çöker. Endotel hipoksik olarak hasarlanır; mikrovasküler lümende DİK tetiklenir. "
            "4. **Klinik Tablo:** Hastada konfüzyon, derin oligüri, taşipne ve metabolik asidoz tablosu belirginleşir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "İlerlemeyen Evreden İlerleyici Evreye Geçiş",
                "İlerlemeyen Evre (Kompanse)",
                "Etkili vazokonstriksiyon, korunmuş koroner ve serebral perfüzyon, hafif taşikardi ve kompanse laktat",
                "İlerleyici Evre (Progresif)",
                "Prekapiller sfinkter gevşemesi, kapiller göllenme, derin laktik asidoz, endotel hasarı ve konfüzyon"
            ),
            make_micro_quiz(
                "Şokun ilerleyici (progresif) evresinde mikrosirkülasyonda kanın göllenmesine (pooling) ve kapiller kaçağa yol açan primer lokal metabolik değişiklik hangisidir?",
                {
                    "A": "Derin doku hipoksisi sonucu gelişen laktik asidoz ve vazomotor tonus gevşemesi",
                    "B": "Primer respiratuar alkaloz ve serebral vazokonstriksiyon",
                    "C": "Hepatik üre döngüsünün aşırı hızlanması",
                    "D": "Kalsiyum çökelmesine bağlı vasküler taşlaşma",
                    "E": "Trombosit granüllerinden aşırı serotonin salınımı"
                },
                "A",
                {
                    "A": "Doğrudur; laktik asidoz prekapiller sfinkterleri gevşetir, postkapiller direnç sürdüğü için kan mikrodolaşımda göllenir.",
                    "B": "Yanlış; ilerleyici evrede metabolik asidoz hakimdir.",
                    "C": "Yanlış; üre döngüsü duraklar.",
                    "D": "Yanlış; kalsiyum hücre içine girer ancak damar taşlaşması yapmaz.",
                    "E": "Yanlış; serotonin göllenme mekanizması değildir."
                }
            )
        ]
    })

    # Slayt 93: 3. Evre: Geri Dönüşümsüz (İrreversibl) Evre
    slides.append({
        "id": "k1-24-s93",
        "title": "3. Evre: Geri Dönüşümsüz (İrreversibl) Evre ve Hücresel Ölüm",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 93,
        "narrative": (
            "Geri dönüşümsüz (irreversibl) evre, hemodinamik parametreler (kan basıncı ve nabız) tıbbi müdahaleyle düzeltilse dahi "
            "hastanın sağkalımının imkansız hale geldiği hücresel tükenme aşamasıdır: "
            "1. **Yaygın Hücresel Hasar:** Membran lipid peroksidasyonu ve intraselüler kalsiyum yüklenmesiyle lizozom membranları "
            "yırtılır; asit hidrolazlar sitoplazmaya dökülerek otolitik enzim sindirimini başlatır. "
            "2. **Mitokondriyal Çöküş:** ATP rezervleri sıfırlanır; yüksek enerjili fosfat bileşikleri yeniden sentezlenemez. "
            "3. **Bakteriyel Translokasyon ve Toksemi:** İskemik bağırsak mukozası nekroze olur; bağırsak florasındaki bakteriler ve "
            "endotoksinler kana dökülür. İkincil endotoksemik septik şok dalgası eklenir. "
            "4. **Miyokard ve Renal Çöküş:** Miyokard kontraktilitesi tamamen durur, böbrekler tam anüriye girer ve klinik ölüm gerçekleşir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Saatlerdir derin şokta olan, anürik, laktatı >15 mmol/L ve bilateral midriatik bir hastada agresif vazopressör ve sıvı tedavisine rağmen kan basıncı yanıtı alınamıyor.",
                [
                    {
                        "text": "Tablonun şokun irreversibl (geri dönüşümsüz) evresine girdiğini, yaygın hücresel lizozomal erime ve ATP tükenmesi geliştiğini öngörmek",
                        "isCorrect": True,
                        "explanation": "Mükemmel. Hücresel düzeyde enerji sıfırlandığında ve bağırsak translokasyonu ile lizozomal sızıntı başladığında şok irreversibl hale gelir."
                    },
                    {
                        "text": "Hastanın sadece sıvı eksikliği olduğunu düşünerek 10 litre kristalloid yüklemesi yapmak",
                        "isCorrect": False,
                        "explanation": "Hatalı ve anlamsız. İrreversibl evrede hücresel ölüm gerçekleşmiştir; sıvı yüklemesi sadece masif doku ödemine ve pulmoner taşkına yol açar."
                    }
                ]
            ),
            make_cloze(
                "Şokun geri dönüşümsüz evresinde hücresel otolizi başlatan en kritik organel hasarı lizozomal enzimlerin sitoplazmaya sızmasıdır.",
                "lizozomal",
                "Asit hidrolazları içeren ve membran bütünlüğü bozulduğunda hücreyi eriten organel"
            )
        ]
    })

    # Slayt 94: Şokun Otopsi ve Histopatolojik Bulguları
    slides.append({
        "id": "k1-24-s94",
        "title": "Şokun Otopsi ve Histopatolojik Bulguları",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 94,
        "narrative": (
            "Şok nedeniyle kaybedilen bir hastanın otopsisinde tüm organ sistemlerinde yaygın hipoksik ve iskemik morfoloji izlenir: "
            "1. **Böbrekler:** Korteks soluk ve şişkin, medülla koyu konjesyonludur. Mikroskopide proksimal tübüllerde iskemik "
            "akut tübüler nekroz (ATN) ve lümenlerde kahverengi granüler silendirler saptanır. "
            "2. **Akciğerler:** Ağır, ıslak ve koyu kırmızıdır. Mikroskopide diffüz alveoler hasar (DAD), kapiller konjesyon, "
            "interstisyel ödem ve alveol duvarlarında pembe camsı hiyalin membranlar görülür (özellikle septik şokta). "
            "3. **Sürrenal Bezler:** Strese bağlı kortikal lipid tükenmesi (berrak hücrelerin kompakt eozinofilik hücrelere dönüşümü) "
            "veya meningokoksemide iki taraflı masif hemorajik nekroz (Waterhouse-Friderichsen) izlenir. "
            "4. **Kalp:** Subendokardiyal peteşiyal kanamalar, miyositlerde dalgalı lifler ve kontraksiyon band nekrozu mevcuttur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Şokta Organların Otopsi ve Histopatolojik Bulguları",
                ["Hedef Organ", "Makroskopik Otopsi Görünümü", "Mikroskobik Patolojik Lezyon", "Patogenetik Mekanizma"],
                [
                    ["Böbrek", "Soluk şişkin korteks, koyu medülla", "İskemik Akut Tübüler Nekroz (ATN)", "Renal kortikal hipoperfüzyon"],
                    ["Akciğer", "Ağır, koyu kırmızı, hava içermeyen", "Diffüz Alveoler Hasar ve Hiyalin Membran", "Endotel-epitel hasarı ve ödem"],
                    [
                        "Sürrenal Bez",
                        "Lipid tükenmesi veya bilateral hemoraji",
                        {"text": "Kortikal hücre lizisi veya hematom", "isMasked": True, "hint": "Waterhouse-Friderichsen sendromunda izlenen mikroskobik kanama"},
                        "Stres hiperaktivitesi veya DİK mikrotrombozu"
                    ],
                    ["Karaciğer", "Alacalı 'muskat cevizi' manzarası", "Sentrilobüler (Zon 3) hepatosit nekrozu", "Santral ven çevresi hipoksisi"],
                    ["Beyin", "Ödemli, giruslar yassılaşmış", "Kortikal laminer nekroz, Sommer sektörü ölümü", "Yaygın serebral iskemik hasar"]
                ]
            ),
            make_active_recall(
                "Şokta böbrek üstü bezi korteksinde kronik stres uyarımı sonucu lipid yüklü vakuollü berrak hücrelerin eozinofilik kompakt hücrelere dönüşümüne ne ad verilir?",
                "Kortikal lipid tükenmesi (lipid deplesyonu) denir.",
                "Stres karşısında steroid hormon sentezi için kolesterol rezervlerinin harcanması"
            )
        ]
    })

    # Slayt 95: Şok Tipleri Karşılaştırmalı Özeti
    slides.append({
        "id": "k1-24-s95",
        "title": "Şok Tipleri Karşılaştırmalı Özeti: Ayırıcı Tanı Matrisi",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 95,
        "narrative": (
            "Beş temel şok tipinin hemodinamik, klinik ve laboratuvar ayrımı hastanın acil yönetiminde kılavuzdur: "
            "1. **Hipovolemik Şok:** Kan/sıvı kaybı -> Debi düşer, PCWP düşer, SVR kompanse olarak artar. Cilt soğuk ve soluktur. "
            "2. **Kardiyojenik Şok:** Miyokard arızası -> Debi düşer, PCWP belirgin artar, SVR artar. Cilt soğuk, soluk ve akciğer ödemlidir. "
            "3. **Septik Şok (Erken):** Sitokinler ve NO -> Debi artar/korunur, PCWP normal/düşük, SVR dramatik düşer. Cilt sıcak ve pembedir. "
            "4. **Nörojenik Şok:** Sempatik tonus felci -> SVR dramatik düşer, venöz göllenmeyle debi azalır, bradikardi eşlik edebilir. "
            "5. **Anafilaktik Şok:** Mast hücre histamin salınımı -> SVR düşer, kapiller kaçak ve laringeal ödem/bronkospazm ön plandadır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Şok Tipleri Büyük Ayırıcı Tanı Matrisi",
                ["Şok Türü", "Primer Neden", "PCWP", "SVR", "Cilt Durumu"],
                [
                    ["Kardiyojenik", "MI / Pompa yetmezliği", "Yüksek", "Yüksek", "Soğuk, nemli, soluk"],
                    [
                        "Hipovolemik",
                        "Hemoraji / Dehidratasyon",
                        {"text": "Düşük", "isMasked": True, "hint": "Sol ventrikül ön yükünün azalmasıyla kama basıncının yönü"},
                        "Yüksek",
                        "Soğuk, nemli, soluk"
                    ],
                    ["Septik (Erken)", "Bakteriyemi / Sitokinler", "Düşük / Normal", "Belirgin Düşük", "Sıcak, kuru, pembe"],
                    ["Nörojenik", "Spinal kord hasarı", "Düşük", "Belirgin Düşük", "Ilık / Normal"],
                    ["Anafilaktik", "IgE alerjen uyarımı", "Düşük", "Belirgin Düşük", "Ödemli, eritemli, ürtikerli"]
                ]
            ),
            make_micro_quiz(
                "Fizik muayenesinde akciğer bazallerinde belirgin raller duyulan, juguler venöz dolgunluğu olan, kardiyak debisi düşük ve PCWP'si yüksek saptanan bir hastada öncelikli şok tanısı hangisidir?",
                {
                    "A": "Kardiyojenik şok",
                    "B": "Primer hipovolemik şok",
                    "C": "Erken dönem septik şok",
                    "D": "Nörojenik şok",
                    "E": "Anafilaktik şok"
                },
                "A",
                {
                    "A": "Doğrudur; yüksek PCWP, akciğer konjesyonu ve düşük debi kardiyojenik şokun kusursuz tablosudur.",
                    "B": "Yanlış; hipovolemide PCWP düşüktür ve akciğerler temizdir.",
                    "C": "Yanlış; erken septik şokta debi yüksek veya normaldir, SVR düşüktür.",
                    "D": "Yanlış; nörojenik şokta PCWP düşüktür ve sempatik tonus kayıptır.",
                    "E": "Yanlış; anafilakside ürtiker ve bronkospazm ön plandadır."
                }
            )
        ]
    })

    # Slayt 96: Prognoz ve Klinik Sonuçlar
    slides.append({
        "id": "k1-24-s96",
        "title": "Prognoz ve Klinik Sonuçlar: Etyolojiye Göre Sağkalım Dinamikleri",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 96,
        "narrative": (
            "Şok sendromunda prognoz ve sağkalım oranları hastanın yaşına, altta yatan etyolojiye ve müdahale hızına göre değişir: "
            "1. **Hipovolemik Şok:** Genç, önceden sağlıklı bireylerde gelişen hipovolemik şokta erken ve uygun volüm replasmanı "
            "(kristalloid ve kan transfüzyonu) ile sağkalım oranı **%90'ın üzerindedir**. "
            "2. **Kardiyojenik Şok:** Geniş miyokard enfarktüsüne sekonder geliştiğinde mortalite dramatik derecede yüksektir (%50 ile %80). "
            "Hasarlı miyokard dokusu rejenere olamadığı için mekanik destek ve acil revaskülarizasyon gereklidir. "
            "3. **Septik Şok:** Modern antibiyotik ve yoğun bakım organ destek protokollerine rağmen mortalite halen **%20 ile %50** "
            "arasında seyreder; ARDS ve DİK eşlik ettiğinde bu oran %70'in üzerine çıkar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Şok Tiplerinde Sağkalım Karşılaştırması",
                "Hipovolemik Şok Prognozu",
                "Erken agresif sıvı/kan replasmanı ile genç ve sağlıklı hastalarda >%90 sağkalım başarısı",
                "Kardiyojenik ve Septik Şok Prognozu",
                "Miyokard nekrozu ve MODS nedeniyle yoğun bakıma rağmen %50-80 mortalite riski"
            ),
            make_active_recall(
                "Şok kategorileri arasında zamanında ve uygun resüsitasyon yapıldığında en yüksek sağkalım oranına (>%90) sahip olan form hangisidir?",
                "Hipovolemik şok tablosudur.",
                "Eksilen kan ve plazmanın yerine konmasıyla hızla düzelen dolaşım yetmezliği"
            )
        ]
    })

    # Slayt 97: Robbins Patoloji Temelli Spot Bilgiler
    slides.append({
        "id": "k1-24-s97",
        "title": "Robbins Patoloji Temelli Sınav Spotları: Emboli, Enfarktüs ve Şok",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 97,
        "narrative": (
            "Tıp fakültesi kurulları ve uzmanlık sınavları için Robbins Patoloji kaynaklı altın spot bilgiler: "
            "1. **Tromboemboli:** Pulmoner embolilerin >%95'i bacak derin venlerinden (DVT) köken alır; en sık mortal form bifurkasyona oturan **eyer (saddle) embolidir**. "
            "2. **Sistemik Emboli:** Sistemik arteriyel embolilerin %80'i **sol kalp mural trombüslerinden** (sol ventrikül MI veya sol atriyal AF) kaynaklanır. "
            "3. **Yağ Embolisi:** Uzun kemik kırıklarından 1-3 gün sonra gelişir; klasik triadı taşipne/dispne, konfüzyon/nörolojik defisit ve **peteşiyal döküntüdür**. "
            "4. **Amniyon Sıvısı Embolisi:** Mikroskopide anne pulmoner arteriyollerinde **fetal skuamöz epitel hücreleri ve lanugo kılları** görülür; DIC ile seyreder. "
            "5. **Enfarktüsler:** Katı organlarda (kalp, böbrek, dalak) **beyaz (anemik)**; çift dolaşımlı organlarda (akciğer, bağırsak) ve venöz tıkanmada **kırmızı (hemorajik)** olur. "
            "6. **Beyin İstisnası:** Tüm organlarda koagülatif nekroz görülürken beyinde **sıvılaşma (likuefaksiyon) nekrozu** ve astrositer **gliozis skarı** gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Emboli, Enfarktüs ve Şok Sınav Spotları Tablosu",
                ["Klinik Patolojik Konsept", "Altın Standart Patoloji Bulgusu", "En Sık Etyolojik Kaynak"],
                [
                    ["Pulmoner Tromboemboli", "Bifurkasyonda eyer emboli, sağ kalp yetmezliği", "Alt ekstremite derin ven trombozu (DVT)"],
                    ["Sistemik Tromboemboli", "Alt ekstremite arter tıkanması ve gangren", "Sol kalp mural trombüsleri (%80)"],
                    [
                        "Yağ Embolisi Triadı",
                        "Solunum sıkıntısı, nörolojik bulgu ve peteşi",
                        {"text": "Uzun kemik (femur/pelvis) kırıkları", "isMasked": True, "hint": "Kemik iliği yağının dolaşıma karıştığı travmatik durum"},
                    ],
                    ["Amniyon Embolisi", "Fetal skuamöz hücreler ve lanugo kılları", "Doğum sırasında uterin ven yırtılması"],
                    ["Beyin Enfarktüsü", "Sıvılaşma nekrozu ve kistik gliozis", "Karotis veya serebral arter aterotrombozu"],
                    ["Waterhouse-Friderichsen", "Bilateral sürrenal hemorajik nekrozu", "Neisseria meningitidis sepsis tablosu"]
                ]
            ),
            make_active_recall(
                "Amniyon sıvısı embolisi nedeniyle kaybedilen bir annenin otopsisinde akciğer mikrovasküler lümenlerinde saptanan patognomonik fetal yapı nedir?",
                "Fetal skuamöz epitel hücreleri ve lanugo kıllarıdır.",
                "Bebeğin cildinden dökülen pullu hücreler ve ince tüyler"
            )
        ]
    })

    # Slayt 98: Çıkmış Kurul ve TUS Soru Tiplerinin Patolojik Analizi
    slides.append({
        "id": "k1-24-s98",
        "title": "Çıkmış Kurul ve TUS Soru Tiplerinin Patolojik Analizi",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 98,
        "narrative": (
            "Dönem 1 Kurul 1 ve TUS sınavlarında en çok sorgulanan soru kalıplarının mantıksal analizi: "
            "1. **Soru Tipi 1 (Nekroz Eşleştirme):** 'Hangisinde koagülatif nekroz DEĞİL, sıvılaşma nekrozu görülür?' -> Cevap daima **Beyin enfarktüsüdür**. "
            "2. **Soru Tipi 2 (Kırmızı Enfarktüs Kriteri):** 'Hangi organda kırmızı (hemorajik) enfarktüs gelişir?' -> Çift dolaşımlı organlar (**Akciğer ve İnce Bağırsak**) veya venöz torsiyon (**Testis/Over**). "
            "3. **Soru Tipi 3 (Dekompresyon):** 'Vurgun yiyen dalgıçta femurun avasküler nekrozuna yol açan tablo nedir?' -> **Caisson hastalığı (Kronik gaz embolisi)**. "
            "4. **Soru Tipi 4 (Septik Şok Sitokinleri):** 'Endotel hasarı ve DİK başlatan ana sitokinler hangileridir?' -> **TNF-alfa ve IL-1**. "
            "5. **Soru Tipi 5 (Hemodinamik Tablo):** 'Düşük debi, yüksek PCWP, yüksek SVR hangi şoka aittir?' -> **Kardiyojenik şok**."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_micro_quiz(
                "TUS ve kurul sınavlarında sıkça sorulan 'Hangi organ enfarktüsünde koagülatif nekroz yerine daima sıvılaşma (likuefaksiyon) nekrozu gelişir?' sorusunun doğru yanıtı hangisidir?",
                {
                    "A": "Beyin (Serebral parankim)",
                    "B": "Kalp (Miyokard)",
                    "C": "Böbrek korteksi",
                    "D": "Dalak parankimi",
                    "E": "Karaciğer parankimi"
                },
                "A",
                {
                    "A": "Doğrudur; beyin dokusunda yüksek lipid ve hidrolitik enzimler nedeniyle iskemik nekroz daima sıvılaşma nekrozuyla sonlanır.",
                    "B": "Yanlış; miyokard koagülatif nekroza uğrar.",
                    "C": "Yanlış; böbrek koagülatif nekroza uğrar.",
                    "D": "Yanlış; dalak koagülatif nekroza uğrar.",
                    "E": "Yanlış; karaciğer koagülatif nekroza uğrar."
                }
            ),
            make_active_recall(
                "Kronik dekompresyon hastalığında (Caisson hastalığı) azot gazı mikroembolilerinin en sık kalıcı iskemik nekroz (aseptik osteonekroz) oluşturduğu kemik anatomik bölgesi neresidir?",
                "Femur başı ve boynudur (Ayrıca tibia ve humerus başı).",
                "Uyluk kemiğinin kalça eklemine oturan üst epifizi"
            )
        ]
    })

    # Slayt 99: Birinci Basamak ve Acil Hekimliğinde Şok Algoritması
    slides.append({
        "id": "k1-24-s99",
        "title": "Birinci Basamak ve Acil Hekimliğinde Şok Algoritması ve Resüsitasyon",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 99,
        "narrative": (
            "Geleceğin hekimi olarak acil serviste şok şüphesi taşıyan bir hastaya yaklaşım prensipleri: "
            "1. **Tanı Triadı:** Hipotansiyon (sistolik kan basıncı <90 mmHg veya bazalden >40 mmHg düşüş), taşikardi ve doku hipoperfüzyon bulguları "
            "(oligüri, bilinç değişikliği, soğuk/soluk cilt veya laktat >2 mmol/L) varlığında şok tanısı konur. "
            "2. **İlk Adım (Hava Yolu ve Oksijenasyon):** Havayolu güvenliği sağlanmalı, yüksek akımlı oksijen başlanmalı, bilinç kapalıysa entübasyon planlanmalıdır. "
            "3. **Damar Yolu ve Sıvı Resüsitasyonu:** İki adet geniş lümenli periferik damar yolu açılmalıdır. Hipovolemik ve septik şokta 30 ml/kg "
            "hızlı kristalloid sıvı infüzyonu başlanmalıdır; ancak kardiyojenik şok şüphesinde (akciğerde raller ve PCWP artışı) sıvı yüklemesinden kaçınılmalıdır. "
            "4. **Vazopressör Desteği:** Sıvıya yanıtsız hipotansiyonda ilk tercih edilen vazopressör **Noradrenalindir** (alfa-1 ve beta-1 agonist). "
            "Septik şokta ilk bir saat içinde kültürler alınıp ampirik geniş spektrumlu intravenöz antibiyotik başlanmalıdır (Altın Saat Kuralı)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Acil servise getirilen 68 yaşında bir hastada tansiyon 75/40 mmHg, nabız 128/dk, ateş 39.2 C saptanıyor. Cildi sıcak ve pembedir, idrar çıkışı yoktur.",
                [
                    {
                        "text": "Septik şok tanısıyla hızla 30 ml/kg kristalloid sıvı infüzyonu başlamak, kan kültürleri alıp ilk bir saat içinde geniş spektrumlu antibiyotik vermek ve yanıtsızsa noradrenalin eklemek",
                        "isCorrect": True,
                        "explanation": "Mükemmel. 'Sıcak şok' bulgusu taşıyan septik hastada ilk 1 saat içinde sıvı, kültür, ampirik antibiyotik ve gerekirse noradrenalin altın standarttır."
                    },
                    {
                        "text": "Hastaya herhangi bir sıvı veya ilaç vermeden önce 24 saatlik idrar biriktirmesini beklemek",
                        "isCorrect": False,
                        "explanation": "Ölümcül hata! Şok acil resüsitasyon gerektiren dinamik bir krizdir; saatler içinde geri dönüşümsüz MODS ve arrest gelişir."
                    }
                ]
            ),
            make_cloze(
                "Sıvı resüsitasyonuna yanıtsız septik şok tablosunda arteriyoler damar tonusunu düzeltmek için ilk tercih edilen vazopressör ilaç noradrenalindir.",
                "noradrenalindir",
                "Alfa-1 adrenerjik reseptörleri güçlü şekilde uyararak vazokonstriksiyon yapan katekolamin"
            )
        ]
    })

    # Slayt 100: Checkpoint 10
    slides.append({
        "id": "k1-24-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Emboli, Enfarktüs ve Şok Büyük Özeti",
        "section": "Şokun Klinik Evreleri, Morfolojik Özeti ve Büyük Sentez",
        "slideNumber": 100,
        "narrative": (
            "Dersimizin bu nihai kontrol noktasında, 100 slaytlık emboli, enfarktüs ve şok patolojisini büyük sentezle bağlıyoruz: "
            "1. **Emboli Bütünlüğü:** %99 tromboembolidir; DVT kaynaklı venöz emboliler pulmoner dolaşıma giderken, sol kalp mural "
            "trombüsleri sistemik arterleri tıkar. Yağ embolisinde kırık sonrası nefes darlığı, peteşi ve konfüzyon gelişir. "
            "2. **Enfarktüs Bütünlüğü:** Katı uç arterli organlar (kalp, böbrek, dalak) beyaz koagülatif nekroza uğrarken, "
            "çift dolaşımlı organlar (akciğer, bağırsak) ve venöz tıkanmalar kırmızı nekroz yapar; beyinde ise daima sıvılaşma nekrozu gelişir. "
            "3. **Şok Bütünlüğü:** Perfüzyon yetersizliği ve hücresel hipoksidir. Kompanse evrede sempatik/RAAS devrededir; "
            "ilerleyici evrede laktik asidoz ve göllenme başlar; irreversibl evrede hücresel lizozomal erimeyle ölüm kaçınılmazdır. "
            "Septik şokta Gram-pozitif/negatif patojenler, TLR-4, TNF/IL-1 fırtınası, kapiller kaçak ve DİK başroldedir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s100-1",
                "Şokun ilerleyici evresinden geri dönüşümsüz (irreversibl) evresine geçişi belirleyen ve hücresel sindirimi başlatan organel zar hasarı nedir?",
                "Lizozom zarlarının parçalanmasıdır.",
                "Asidik sindirim hidrolazlarının serbest kalarak hücreyi içeriden eritmesi",
                "İrreversibl Faz Organeli"
            ),
            make_flashcard(
                "k1-24-fc-s100-2",
                "Uzun kemik kırıklarından 1-3 gün sonra gelişen; solunum sıkıntısı, nörolojik defisit ve konjonktival peteşiyel döküntüyle seyreden klinik sendrom nedir?",
                "Yağ embolisi sendromudur.",
                "Medüller kavitedeki lipid damlacıklarının mikrosirkülasyona saçılması",
                "Yağ Embolisi Triadı"
            ),
            make_flashcard(
                "k1-24-fc-s100-3",
                "Septik şok resüsitasyonunda sıvı yüklemesine yanıtsız inatçı arteriyel hipotansiyonu düzeltmek amacıyla ilk sırada tercih edilen vazopressör katekolamin hangisidir?",
                "Noradrenalin (Norepinefrin) ilacıdır.",
                "Periferik alfa damar reseptörlerini uyararak sistemik direnci yükselten ajan",
                "İlk Tercih Vazopressör"
            )
        ],
        "interactiveElements": [
            make_table(
                "Ders 24 Büyük Patoloji Özeti Matrisi",
                ["Patolojik Süreç", "Primer Tetikleyici / Etyoloji", "Altın Standart Histopatoloji", "Nihai Klinik Sonuç"],
                [
                    ["Pulmoner Tromboemboli", "Alt ekstremite DVT (%95)", "Bifurkasyonda eyer emboli, pulmoner enfarktüs", "Akut sağ kalp yetmezliği / Ani ölüm"],
                    ["Sistemik Tromboemboli", "Sol kalp mural trombüsü (%80)", "Ekstremite veya organ iskemik enfarktüsü", "Gangren, inme, organ yetmezliği"],
                    ["Miyokard Enfarktüsü", "Koroner aterotrombozu", "Koagülatif nekroz ve kontraksiyon bandları", "Kardiyojenik şok, aritmi, ölüm"],
                    ["Serebral Enfarktüs", "Karotis / Serebral arter tıkanması", "Sıvılaşma nekrozu ve astrositer gliozis", "Kalıcı inme ve nörolojik defisit"],
                    [
                        "Septik Şok ve DİK",
                        "Gram-pozitif/negatif bakteriyemi",
                        {"text": "Yaygın mikrotromboz, DAD ve ATN", "isMasked": True, "hint": "Çoklu organ disfonksiyonunda görülen kombine histopatolojik hasar"},
                        "Refrakter hipotansiyon, MODS ve ölüm"
                    ]
                ]
            ),
            make_micro_quiz(
                "Emboli, enfarktüs ve şok patolojisinin tüm klinik ve patolojik ilkeleri göz önüne alındığında aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                {
                    "A": "Beyin enfarktüsünde daima sıvılaşma nekrozu gelişirken, böbrek enfarktüsünde beyaz koagülatif nekroz izlenir.",
                    "B": "Tüm embolilerin yüzde doksan dokuzu yağ damlacıklarından kaynaklanır.",
                    "C": "Kardiyojenik şokta pulmoner kapiller uç basıncı (PCWP) dramatik şekilde düşer.",
                    "D": "Septik şokun en sık etkeni günümüzde parazitik helmintlerdir.",
                    "E": "Şokun ilerlemeyen evresinde hücresel lizozomlar tamamen patlamış ve irreversibl ölüm gerçekleşmiştir."
                },
                "A",
                {
                    "A": "Doğrudur; beyinde daima sıvılaşma nekrozu, uç arterli solid böbrek dokusunda ise beyaz koagülatif nekroz gelişir.",
                    "B": "Yanlış; embolilerin >%99'u tromboembolidir.",
                    "C": "Yanlış; kardiyojenik şokta PCWP yükselir.",
                    "D": "Yanlış; en sık etken Gram-pozitif bakterilerdir.",
                    "E": "Yanlış; lizozom patlaması irreversibl 3. evrede görülür."
                }
            )
        ]
    })

    return slides
