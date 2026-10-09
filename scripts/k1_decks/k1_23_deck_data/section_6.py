# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 6: Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi (Slayt 51 - 60)
Checkpoint 6: Slayt 59
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_6_slides():
    slides = []

    # Slayt 51: Gebelikte Kardinal Tehlike İşaretleri: Kanama, Konvülsiyon ve Baş Ağrısı
    slides.append({
        "id": "k1-23-s51",
        "title": "Gebelikte Kardinal Tehlike İşaretleri: Kanama, Konvülsiyon ve Baş Ağrısı",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 51,
        "narrative": (
            "Doğum öncesi bakımın en hayati koruyucu boyutu, gebeye ve ailesine acil servise koşmayı gerektiren "
            "**Kardinal Tehlike İşaretleri'nin** öğretilmesidir. Bu işaretler görüldüğünde randevu günü beklenmez: "
            "1. **Vajinal Kanama:** Gebeliğin hangi haftasında olursa olsun, ister damla ister masif olsun "
            "her türlü vajinal kanama patolojiktir (ilk trimesterde düşük/ektopik gebelik; son trimesterde plasenta previa/dekolman). "
            "2. **Konvülsiyon (Kasılma Nöbeti):** Eklampsi krizidir; beyin ödemi ve anoksiye bağlı gelişir, ölüm riski %10'u aşar. "
            "3. **Şiddetli ve İnatçı Baş Ağrısı:** Basit analjeziklerle geçmeyen, özellikle frontal/oksipital zonklayıcı baş ağrısı; "
            "serebral vazospazm ve yaklaşan eklampsi nöbetinin (impending eclampsia) habercisidir. "
            "Bu üç bulgudan herhangi biri doğrudan acil 112 sevk endikasyonudur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gebelikte basit analjeziklere yanıt vermeyen şiddetli baş ağrısı ve görme bozukluğu yaklaşan eklampsi krizinin habercisidir.",
                "yaklaşan eklampsi",
                "Serebral ödem ve konvülsiyon öncesi toksemik alarm dönemi"
            ),
            make_table(
                "Gebelikte Kardinal Tehlike İşaretleri ve Şüphelenilen Patolojiler",
                ["Tehlike İşareti", "Altta Yatan Muhtemel Acil Patoloji", "Beklenen Maternal-Fetal Risk"],
                [
                    ["Her Türlü Vajinal Kanama", "Düşük, Ektopik Gebelik, Plasenta Previa veya Dekolman", "Hemorajik şok ve fetal asfiksi"],
                    [
                        "Konvülsiyon / Kasılma",
                        {"text": "Eklampsi (Gebelik Toksemisi Krizi)", "isMasked": True, "hint": "Serebral vazospazma bağlı tonik-klonik nöbet tablosu"},
                        "Beyin kanaması, anoksi ve anne-bebek kaybı"
                    ],
                    ["İnatçı Şiddetli Baş Ağrısı", "Serebral ödem ve hipertansif ensefalopati", "Birkaç saat içinde eklampsi nöbetine ilerleme"]
                ]
            ),
            make_active_recall(
                "Gebelikte görülen şiddetli baş ağrısının basit bir gerilim tipi baş ağrısı olmayıp yaklaşan eklampsi krizi olduğunu düşündüren en önemli ek klinik bulgu nedir?",
                "Kan basıncının 140/90 mmHg üzerinde olması, görme bozuklukları (skotom) ve proteinüri eşliğidir.",
                "Hipertansiyon ve görme bulanıklığı eşliği"
            )
        ]
    })

    # Slayt 52: Görme Bozuklukları, Solunum Güçlüğü, Fetus Hareket Kaybı ve Su Gelmesi
    slides.append({
        "id": "k1-23-s52",
        "title": "Görme Bozuklukları, Solunum Güçlüğü, Fetus Hareket Kaybı ve Su Gelmesi",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 52,
        "narrative": (
            "Gebelikte kardinal işaretlerin yanı sıra şu klinik alarmlar da derhal hastane müdahalesi gerektirir: "
            "1. **Görme Bozuklukları:** Bulanık görme, çift görme (diplopi), göz önünde ışık çakmaları veya sinek uçuşması (skotomlar); "
            "retinal arteriyoler spazmın ve serebral iskeminin göstergesidir. "
            "2. **Fetus Hareketlerinin Hissedilmemesi:** 24. haftadan sonra fetus hareketlerinin belirgin azalması veya hiç hissedilmemesi; "
            "akut uteroplasental yetmezlik ve fetal hipoksi işaretidir. Anneye yemek sonrası sol yan yatarak 2 saatte en az 10 hareket sayması öğretilir. "
            "3. **Suyun Gelmesi:** Membran rüptürü; kordon sarkması ve koryoamniyonit alarmıdır. "
            "4. **Yüksek Ateş ve Ciddi Karın Ağrısı:** Akut karın (apandisit, plasenta dekolmanı) veya koryoamniyonit şüphesidir. "
            "5. **Hızlı Kilo Alımı ve Yüzde-Elde Şişme:** Haftada 1 kg'dan fazla ani kilo artışı ve sabahları göz kapaklarında gode bırakan ödem toksemi alarmıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "İleri gebelik haftalarında fetus hareketlerinin hissedilmemesi veya ani azalması akut fetal distres ve hipoksi göstergesidir.",
                "akut fetal distres",
                "İntrauterin oksijen yetersizliği ve asidoz tablosu"
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı Doğum Öncesi Bakım Yönetim Rehberi'ne göre gebelikte derhal sağlık kuruluşuna başvurmayı gerektiren tehlike işaretleri arasında hangisi YER ALMAZ?",
                {
                    "A": "Vajinadan berrak su gelmesi (membran rüptürü)",
                    "B": "Göz önünde şimşek çakması, parlak ışıklar görme veya bulanık görme",
                    "C": "Fetus hareketlerinin aniden durması veya hissedilmemesi",
                    "D": "İlk trimesterde sabahları hafif bulantı hissedilmesi ve krakerle geçmesi",
                    "E": "Yüzde, ellerde ve göz kapaklarında aniden başlayan yaygın gode bırakan şişlik"
                },
                "D",
                {
                    "A": "Tehlike işaretidir; Kordon prolapsusu riski taşır.",
                    "B": "Tehlike işaretidir; Retinal spazm ve preeklampsidir.",
                    "C": "Tehlike işaretidir; Fetal asfiksi şüphesidir.",
                    "D": "Olağan Fizyolojik Yakınmadır; İlk trimester sabah bulantısı beta-hCG'ye bağlı fizyolojik yakınmadır, acil tehlike işareti değildir.",
                    "E": "Tehlike işaretidir; Preeklamptik patolojik ödemdir."
                }
            ),
            make_active_recall(
                "Gebeliğin 28. haftasından sonra bir annenin bebeğinin intrauterin iyilik halini evde test etmesi için yemek sonrası sol yan pozisyonda 2 saat içinde en az kaç fetal hareket hissetmesi beklenir?",
                "2 saat içinde en az 10 fetal hareket hissetmesi beklenir.",
                "Fetal hareket sayımı minimum referans eşiği"
            )
        ]
    })

    # Slayt 53: Birinci Basamaktan Acil Sevk Kriterleri (Hb < 7, Fundus ±4 cm)
    slides.append({
        "id": "k1-23-s53",
        "title": "Birinci Basamaktan Acil Sevk Kriterleri (Hb < 7, Fundus ±4 cm)",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 53,
        "narrative": (
            "Aile hekimliği biriminde gebe izlemi yapan hekim, komplikasyonlu vakaları gecikmeden 2. veya 3. basamağa "
            "sevk etmekle yükümlüdür. Sağlık Bakanlığı'nın **Mutlak Sevk Kriterleri** şunlardır: "
            "1. **Ağır Anemi (Hb < 7 g/dl):** Kalp yetmezliği ve anoksik şok riski nedeniyle acil yatış ve kan transfüzyonu gerektirir. "
            "2. **Fundus-Pubis Yüksekliği (FPY) Sapması:** Ölçülen mezura boyunun gebelik haftasından **±4 cm ve daha fazla farklı olması** "
            "(makrozomi, İUGG, polihidramnios veya oligohidramnios şüphesi). "
            "3. **Fetal Kalp Sesleri Anomalisi:** FKS'nin duyulamaması veya hızının <120 ya da >160 atım/dk olması. "
            "4. **Preeklampsi Bulguları:** Tansiyonun $\\ge 140/90$ mmHg olması veya idrarda proteinüri saptanması. "
            "5. **Dirençli Bakteriüri:** Uygun antibiyotik tedavisine rağmen idrar kültüründe üremenin devam etmesi. "
            "6. **Vajinal Kanama, Lekelenme veya Su Gelmesi** durumlarında gebe asla bekletilmeden sevk edilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Birinci basamak izleminde hemoglobin değerinin yedi gram bölü desilitrenin altına düşmesi acil hastane sevki gerektirir.",
                "yedi gram bölü desilitrenin",
                "Ağır maternal anemi ve kan nakli sevk eşiği"
            ),
            make_table(
                "Sağlık Bakanlığı Birinci Basamak Gebe Acil Sevk Kriterleri Özeti",
                ["Klinik / Laboratuvar Parametre", "Sevk Eşiği / Kritik Değer", "Şüphelenilen Ağır Tablo"],
                [
                    [
                        "Hemoglobin Düzeyi",
                        {"text": "Hb < 7 g/dl", "isMasked": True, "hint": "Ağır anemi ve kalp yetmezliği sınırı"},
                        "Dekompanse anemi ve intrauterin hipoksi"
                    ],
                    ["Uterus Fundus Yüksekliği", "Gebelik haftasından ±4 cm farklı", "Çoğul gebelik, polihidramnios, İUGG"],
                    ["Fetal Kalp Hızı", "< 120 veya > 160 atım/dk", "Akut fetal distres ve asidoz"],
                    ["Kan Basıncı", "Tansiyon ≥ 140/90 mmHg", "Preeklampsi / Gebelik Toksemisi"],
                    ["Asemptomatik Bakteriüri", "Tedaviye rağmen devam etmesi", "Akut piyelonefrit ve sepsis riski"]
                ]
            ),
            make_micro_quiz(
                "Aile sağlığı merkezinde izlenen 30 haftalık bir gebede aşağıdaki bulgulardan hangisinin saptanması durumunda derhal 2. veya 3. basamak sağlık kuruluşuna sevk zorunluluğu YOKTUR?",
                {
                    "A": "Laboratuvarda hemoglobin düzeyinin 6.4 g/dl bulunması",
                    "B": "Mezura ile ölçülen uterus fundus yüksekliğinin 35 cm (haftadan +5 cm büyük) bulunması",
                    "C": "Dinlenen fetal kalp seslerinin dakikada 105 atım (bradikardi) olması",
                    "D": "Gebenin bacaklarında uzun süre ayakta kalmaya bağlı hafif ayak bileği ödemi olması",
                    "E": "Hastanın idrarında dipstick ile ++ proteinüri ve tansiyonun 150/95 mmHg ölçülmesi"
                },
                "D",
                {
                    "A": "Sevk Kriteridir; Hb < 7 g/dl acil sevk gerektirir.",
                    "B": "Sevk Kriteridir; ±4 cm kuralı aşılmıştır (+5 cm).",
                    "C": "Sevk Kriteridir; FKS < 120 fetal distrestir.",
                    "D": "Sevk Kriteri Değildir; Ayakta kalmaya bağlı hafif ayak bileği ödemi fizyolojiktir, istirahatle geçer ve tansiyon normalse sevk gerektirmez.",
                    "E": "Sevk Kriteridir; Klasik preeklampsi tablosudur."
                }
            )
        ]
    })

    # Slayt 54: Gebelikte Fizyolojik Kilo Alımı Dinamikleri (9-13 kg Dağılımı)
    slides.append({
        "id": "k1-23-s54",
        "title": "Gebelikte Fizyolojik Kilo Alımı Dinamikleri (9-13 kg Dağılımı)",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 54,
        "narrative": (
            "Sağlıklı, normal kilolu (BKİ 18.5 - 24.9) bir kadının tekil gebeliği boyunca ortalama **9 - 13 kg (ortalama 11-12 kg)** "
            "kilo alması ideal kabul edilir. Bu kilo artışının zamansal dağılımı şöyledir: "
            "- **İlk 3 Ayda (1. Trimester):** Toplamda yalnızca **yaklaşık 1 kg** (bazı gebelerde bulantı nedeniyle kilo kaybı dahi görülebilir). "
            "- **2. ve 3. Trimesterde:** Ayda yaklaşık **1.5 - 2 kg (haftada ~400-500 gram)** artış fizyolojiktir. "
            "Alınan 12 kg'lık ağırlığın anatomik ve dokusal dağılımı şöyledir: "
            "- **Fetüs:** ~3.5 kg, "
            "- **Memeler:** ~1 kg (alveoler proliferasyon), "
            "- **Plasenta:** ~0.5 - 0.7 kg, "
            "- **Amniyon Sıvısı:** ~1 kg, "
            "- **Uterus Kası:** ~1 kg (miyometriyum hipertrofisi), "
            "- **Artan Kan ve Ekstraselüler Sıvı:** ~1.5 - 2 kg, "
            "- **Maternal Yağ Depoları:** ~3 - 3.5 kg (laktasyon hazırlığı)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Normal kilolu bir kadının gebelik boyunca ortalama dokuz ile on üç kilogram arasında kilo alması beklenir.",
                "dokuz ile on üç",
                "İdeal fizyolojik maternal ağırlık artış aralığı"
            ),
            make_table(
                "Gebelikte Alınan 12 Kilogramın Anatomik ve Biyolojik Dağılımı",
                ["Anatomik Kompartman / Doku", "Ortalama Ağırlık Payı", "Fizyolojik Amacı"],
                [
                    ["Fetüs", "~3.5 kg", "Term yenidoğan büyümesi"],
                    [
                        "Meme Dokusu",
                        {"text": "~1 kg", "isMasked": True, "hint": "Glandüler hiperplazi ile laktasyona hazırlanan meme ağırlığı"},
                        "Doğum sonrası emzirme ve süt üretimi"
                    ],
                    ["Plasenta ve Kordon", "~0.5 - 0.7 kg", "Solunum ve besin değişimi organı"],
                    ["Amniyon Sıvısı", "~1.0 kg", "Fetal koruma ve hareket alanı"],
                    ["Uterus Miyometriyumu", "~1.0 kg", "Fetüsü taşıyan kas hipertrofisi"],
                    ["Kan Hacmi ve Sıvı Artışı", "~1.5 - 2.0 kg", "Uteroplasental perfüzyon ve kanama toleransı"],
                    ["Maternal Yağ Rezervi", "~3.0 - 3.5 kg", "Emzirme dönemi kalori deposu"]
                ]
            ),
            make_active_recall(
                "Gebelikte ilk 3 ayda toplam kilo artışının yalnızca yaklaşık 1 kg olması beklenirken, 2. ve 3. trimesterlerde ayda ortalama kaç kg artış fizyolojiktir?",
                "Ayda ortalama 1.5 - 2 kg (haftada yaklaşık 400-500 gram) artış fizyolojiktir.",
                "İkinci ve üçüncü trimester aylık kilo artış hızı"
            )
        ]
    })

    # Slayt 55: Gebelikte Ödem Nedenleri ve Fizyolojik vs Patolojik Ödem Ayrımı
    slides.append({
        "id": "k1-23-s55",
        "title": "Gebelikte Ödem Nedenleri ve Fizyolojik vs Patolojik Ödem Ayrımı",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 55,
        "narrative": (
            "Ödem, gebelerin %80'inde görülen en yaygın semptomdur; ancak hekim fizyolojik ödem ile patolojik ödemi kesinlikle ayırt etmelidir: "
            "1. **Fizyolojik (Ortostatik) Ödem:** Büyüyen uterusun vena kava inferior ve iliak venlere mekanik basısı sonucu "
            "alt ekstremitelerde venöz göllenme olur. Akşama doğru ayakta kalındığında belirir, gece yatıp ayakları yükseltince tamamen kaybolur. "
            "Yalnızca ayak bileklerindedir; tansiyon ve idrar tahlili tamamen normaldir. "
            "2. **Patolojik Ödem Nedenleri:** "
            "- **Gebelik Toksemisi (Preeklampsi):** Sabahları uyanıldığında göz kapaklarında, yüzde ve yüzüklerin sıkmasına yol açacak şekilde "
            "parmaklarda gode bırakan yaygın ödemdir. "
            "- **Şiddetli Anemi (Hb < 7):** Onkotik basınç düşüşü ve kalp yetmezliği. "
            "- **Kronik Böbrek ve Kalp Hastalıkları:** Proteinüri veya konjestif iflas. "
            "- **Çoğul Gebelik ve Polihidramnios:** Aşırı mekanik kaval bası. "
            "- **Protein Yetersizliği:** Ağır malnütrisyon sonucu hipoalbüminemi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gebelikte sabahları yüzde ve parmaklarda gode bırakan yaygın ödem görülmesi gebelik toksemisinin önemli işaretidir.",
                "gebelik toksemisinin",
                "Hipertansiyon ve proteinüriyle seyreden preeklampsi tablosu"
            ),
            make_before_after(
                "Fizyolojik vs Patolojik Gebelik Ödemi Ayrımı",
                "Fizyolojik Ortostatik Ödem",
                "Akşamları sadece ayak bileğinde belirir; gece istirahatle ve bacakları kaldırmakla tamamen geriler; tansiyon normaldir.",
                "Patolojik Toksemik Ödem",
                "Sabah uyanınca yüzde ve parmaklarda gode bırakır; istirahatle gerilemez, tansiyon yüksekliği ve proteinüri eşlik eder.",
                "Gebelikte ödemin klinik ayırıcı tanısı"
            ),
            make_active_recall(
                "Gebelikte basit fizyolojik ayak bileği ödeminin oluşmasında rol oynayan temel anatomik mekanizma nedir?",
                "Büyüyen uterusun vena kava inferior ve pelvik venlere mekanik bası yaparak bacaklarda hidrostatik basıncı artırmasıdır.",
                "Kaval bası ve venöz göllenme mekanizması"
            )
        ]
    })

    # Slayt 56: Gebelik Toksemisi (Preeklampsi): Triad ve Patofizyoloji
    slides.append({
        "id": "k1-23-s56",
        "title": "Gebelik Toksemisi (Preeklampsi): Triad ve Patofizyoloji",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 56,
        "narrative": (
            "Gebelik Toksemisi (Preeklampsi); gebeliğin **20. haftasından sonra**, daha önce normotansif olan bir kadında "
            "**üçlü kardinal triad** ile karakterize sistemik endotel hastalığıdır: "
            "1. **Hipertansiyon:** En az 4 saat arayla ölçülen sistolik kan basıncının $\\ge 140$ mmHg veya diyastolik kan basıncının $\\ge 90$ mmHg olması. "
            "2. **Proteinüri:** 24 saatlik idrarda $\\ge 300$ mg protein veya dipstick idrar testinde en az $\\ge +1$ pozitiflik. "
            "3. **Ödem:** Yüz ve ellerde belirgin, hızlı kilo alımıyla seyreden patolojik sıvı tutulumu. "
            "**Patofizyoloji:** Plasentanın trofoblastik invazyon kusuru nedeniyle uterin spiral arterler genişleyemez. "
            "Gelişen plasental iskemi anne kanına toksik anti-anjiyogenik faktörler (sFlt-1) salar; "
            "tüm vücutta yaygın endotel hasarı, vazospazm, böbrek glomerülendotelyozisi ve trombosit tüketimi başlar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gebelik toksemisi yirminci haftadan sonra ortaya çıkan hipertansiyon, ödem ve proteinüri triadı ile tanımlanır.",
                "hipertansiyon, ödem ve proteinüri",
                "Preeklampsi tanısını koyduran klasik üçlü klinik tablo"
            ),
            make_causal_chain(
                "Preeklampsi Patofizyolojik Gelişim Zinciri",
                [
                    "1. Bozuk Trofoblastik İnvazyon: Spiral arterler genişleyemez; yüksek dirençli dar lümenler kalır.",
                    "2. Plasental İskemi: Plasentada hipoksi gelişir ve maternal dolaşıma anti-anjiyogenik faktörler salınır.",
                    "3. Sistemik Endotel Hasarı: Nitrik oksit azalır, endotelin artar; tüm damar yataklarında yaygın vazospazm oturur.",
                    "4. Hedef Organ Hasarı: Böbrekte proteinüri, beyinde ödem, karaciğerde iskemi ve kanda hipertansiyon patlar."
                ]
            ),
            make_micro_quiz(
                "Gebelikte 'Preeklampsi (Gebelik Toksemisi)' tanısı koyabilmek için hipertansiyon ve proteinürinin gebeliğin en erken kaçıncı haftasından sonra ortaya çıkmış olması gerekir?",
                {
                    "A": "6. haftadan sonra",
                    "B": "12. haftadan sonra",
                    "C": "20. haftadan sonra",
                    "D": "36. haftadan sonra",
                    "E": "Yalnızca doğum eylemi başladıktan sonra"
                },
                "C",
                {
                    "A": "Yanlıştır; Kronik hipertansiyondur.",
                    "B": "Yanlıştır; 20 haftadan önce preeklampsi tanısı konmaz (mol hidatiform hariç).",
                    "C": "Doğrudur; Preeklampsi kural olarak 20. gebelik haftasından sonra başlar.",
                    "D": "Yanlıştır; Daha erken başlar.",
                    "E": "Yanlıştır; Antenatal dönemde gelişir."
                }
            )
        ]
    })

    # Slayt 57: Eklampsi Tablosu: Konvülsiyonlar, Koma ve Acil Yönetim
    slides.append({
        "id": "k1-23-s57",
        "title": "Eklampsi Tablosu: Konvülsiyonlar, Koma ve Acil Yönetim",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 57,
        "narrative": (
            "Eklampsi; preeklamptik bir gebede altta yatan başka bir nörolojik neden (epilepsi, menenjit, kafa travması vb.) olmaksızın "
            "**jeneralize tonik-klonik konvülsiyonların ve/veya komanın ortaya çıkmasıdır**. "
            "Anne ve fetus için en ölümcül obstetrik tablodur: "
            "1. **Klinik Nöbet Evreleri:** Yüz ve dilde seğirmelerle başlar, ardından tüm vücutta tonik kasılma, "
            "siyanotik solunum durması, klonik çırpınmalar ve derin postiktal koma tablosu gelişir. "
            "2. **Ölüm Nedenleri:** İntraserebral kanama, akut akciğer ödemi, aspirasyon pnömonisi ve kardiyak arresttir. "
            "3. **Acil Tedavi Altın Standardı: MAGNEZYUM SÜLFAT ($MgSO_4$):** "
            "Magnezyum sülfat antikonvülzan ve nöroprotektiftir; santral vazodilatasyon yapar ve nöromüsküler kavşakta asetilkolin salınımını bloke eder. "
            "Nöbeti durdurmak ve tekrarlamasını önlemek için derhal intravenöz uygulanır. "
            "Eklampsinin tek kesin ve radikal tedavisi ise **bebeğin ve plasentanın acilen doğurtulmasıdır**."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Eklampsi nöbetlerinin tedavisinde ve önlenmesinde kullanılan ilk seçenek altın standart ilaç magnezyum sülfattır.",
                "magnezyum sülfattır",
                "Nöromüsküler blokaj ve serebral vazodilatasyon sağlayan antikonvülzan iyon çözeltisi"
            ),
            make_table(
                "Preeklampsi ile Eklampsi Arasındaki Temel Klinik ve Tedavi Farkları",
                ["Klinik Parametre", "Preeklampsi Tablosu", "Eklampsi Tablosu"],
                [
                    ["Kardinal Tanı Kriteri", "Hipertansiyon + Proteinüri + Ödem", "Preeklampsiye eklenen tonik-klonik konvülsiyon/koma"],
                    [
                        "Nörolojik Durum",
                        "Şiddetli baş ağrısı ve görme bulanıklığı",
                        {"text": "Bilinç kaybı ve jeneralize epileptik kasılmalar", "isMasked": True, "hint": "Serebral ödeme bağlı motor deşarj tablosu"}
                    ],
                    ["Maternal Mortalite Riski", "Düşük - Orta", "Aşırı Yüksek (>%10-15)"],
                    ["İlaç Tedavisi", "Antihipertansif + Nöbet profilaksisi", "Acil Magnezyum Sülfat yükleme ve idamesi"],
                    ["Kesin Çözüm", "Yakın takip veya terme göre doğum", "Stabilizasyon sonrası acil doğum"]
                ]
            ),
            make_active_recall(
                "Eklampsi konvülsiyonu geçiren bir gebede magnezyum sülfat tedavisi uygulanırken toksisiteyi izlemek için hekimin yatak başında kontrol edeceği en hassas klinik refleks nedir?",
                "Patella (Derin Tendon) Refleksidir (refleks kaybolursa magnezyum toksisitesi gelişmiştir; antidot Kalsiyum Glukonattır).",
                "Derin tendon refleksi ve kalsiyum antidotu"
            )
        ]
    })

    # Slayt 58: Preeklampsi Risk Faktörleri ve Maternal-Fetal Komplikasyonlar
    slides.append({
        "id": "k1-23-s58",
        "title": "Preeklampsi Risk Faktörleri ve Maternal-Fetal Komplikasyonlar",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 58,
        "narrative": (
            "Preeklampsi gelişme ihtimali yüksek olan kadınlar ilk izlemdeki risk değerlendirme formuyla hemen tanınmalıdır: "
            "1. **En Önemli Risk Faktörleri:** "
            "- **İlk Gebelik (Nulliparite):** Paternal antijenlere ilk maruziyet nedeniyle preeklampsi riski 3-4 kat fazladır. "
            "- **İleri Anne Yaşı (>35 Yaş) veya Çok Genç Yaş (<18 Yaş),** "
            "- **Çoğul Gebelik (İkiz, Üçüz):** Artmış plasental kitle, "
            "- **Polihidramnios,** "
            "- **Önceki Gebelikte Toksemi Hikayesi,** "
            "- **Kronik Hastalıklar:** Kronik böbrek yetmezliği, önceden var olan hipertansiyon, diyabet ve antifosfolipid sendromu. "
            "2. **Ağır Komplikasyonlar:** "
            "- **Maternal:** HELLP Sendromu (Hemoliz, Karaciğer Enzim Yüksekliği, Trombositopeni), Plasenta Dekolmanı, Akut Böbrek İflası. "
            "- **Fetal:** Ağır intrauterin gelişme geriliği (İUGG), oligohidramnios, prematürite ve intrauterin ölüm."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "İlk gebeliğini yaşayan nullipar kadınlarda paternal antijenlere immünolojik yanıtsızlık nedeniyle preeklampsi riski daha yüksektir.",
                "nullipar kadınlarda",
                "Daha önce hiç doğum yapmamış ilk gebe grubu"
            ),
            make_micro_quiz(
                "Aşağıdaki gebe gruplarından hangisinde Gebelik Toksemisi (Preeklampsi) gelişme riski diğerlerine göre belirgin olarak DAHA YÜKSEKTİR?",
                {
                    "A": "Daha önce 2 normal sağlıklı vajinal doğum yapmış 25 yaşındaki kadın",
                    "B": "Kronik hipertansiyonu ve ikiz gebeliği olan 38 yaşındaki ilk gebeliğindeki kadın",
                    "C": "Düzenli spor yapan ve gebeliğe normal kiloda başlayan kadın",
                    "D": "İlk trimesterde hafif sabah bulantısı olan kadın",
                    "E": "İki gebelik arasında 3 yıl süre bırakmış olan kadın"
                },
                "B",
                {
                    "A": "Düşük risklidir; Multiparite koruyucudur.",
                    "B": "En Yüksek Risklidir; İleri yaş (>35), ilk gebelik (nulliparite), çoğul gebelik (ikiz) ve kronik hipertansiyon en ağır preeklampsi risk faktörleridir.",
                    "C": "Düşük risklidir.",
                    "D": "Fizyolojik durumdur, risk değildir.",
                    "E": "İdeal aralıktır."
                }
            ),
            make_active_recall(
                "Preeklampsinin en ölümcül varyantı olan ve mikroanjiyopatik hemolitik anemi, karaciğer yetmezliği ve trombositopeni ile seyreden tablonun tıbbi kısaltması nedir?",
                "HELLP Sendromudur (Hemolysis, Elevated Liver enzymes, Low Platelets).",
                "Karaciğer ve trombosit çöktüren obstetrik akronim"
            )
        ]
    })

    # Slayt 59: [TEKRAR SAYFASI - CHECKPOINT 6] Tehlike İşaretleri, Sevk ve Toksemi
    slides.append({
        "id": "k1-23-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Tehlike İşaretleri, Sevk ve Toksemi",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 59,
        "narrative": (
            "Bu altıncı checkpoint sayfasında, gebelikte tehlike işaretlerini, acil sevk kurallarını ve preeklampsiyi özetliyoruz: "
            "1. **Kardinal Tehlike İşaretleri:** Vajinal kanama (her türlü), konvülsiyon, inatçı şiddetli baş ağrısı ve görme bozuklukları. "
            "2. **Diğer Alarmlar:** Su gelmesi, fetus hareket kaybı, solunum güçlüğü, yüksek ateş ve yüzde-ellerde ani gode bırakan ödem. "
            "3. **Acil Sevk Kriterleri:** Hb < 7 g/dl, fundus yüksekliği beklenenden ±4 cm farklı, FKS <120 veya >160, preeklampsi. "
            "4. **Fizyolojik Kilo:** Toplam 9-13 kg; ilk 3 ayda ~1 kg, sonra ayda 1.5-2 kg. "
            "5. **Preeklampsi Triadı:** 20. haftadan sonra hipertansiyon ($\\\\ge 140/90$), ödem ve proteinüri ($\\\\ge 300$ mg/gün). "
            "6. **Eklampsi:** Preeklampsiye konvülsiyon eklenmesi; ilk seçenek ilaç Magnezyum Sülfattır; kesin tedavi acil doğumdur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s59-1",
                "Gebelikte 20. haftadan sonra ortaya çıkan ve preeklampsi (toksemi) tanısını koyduran üç klasik kardinal bulgu nedir?",
                "Hipertansiyon, patolojik ödem ve idrarda proteinüri saptanmasıdır.",
                "Arteryel basınç artışı, yaygın sıvı birikimi ve albumin kaçağı üçlüsü",
                "Toksemi Tanı Kriterleri"
            ),
            make_flashcard(
                "k1-23-fc-s59-2",
                "Eklampsi tablosunda konvülsiyonların durdurulması ve profilaksisinde ilk seçenek altın standart ilaç hangisidir?",
                "Magnezyum Sülfat ilacıdır.",
                "Nöromüsküler kavşak blokajı yapan iyon infüzyonu",
                "Acil Obstetrik Tedavi"
            ),
            make_flashcard(
                "k1-23-fc-s59-3",
                "Birinci basamakta takip edilen bir gebede hemoglobin değeri kaç g/dl altına düştüğünde acil üst basamağa sevk zorunludur?",
                "Yedi gram bölü desilitrenin altına (Hb < 7 g/dl) düştüğünde sevk zorunludur.",
                "Kritik eritrosit azlığı ve kardiyak dekompansasyonda hastaneye nakil eşiği",
                "Birinci Basamak Sevk Kriterleri"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tehlike İşaretleri ve Toksemi Karar Tablosu",
                ["Klinik Durum / Bulgu", "Acil Tıbbi Anlamı", "Birinci Basamak Hekiminin Eylemi"],
                [
                    ["Vajinal Kanama (Ağrılı/Ağrısız)", "Dekolman veya Previa şüphesi", "Damar yolu aç, dokunma, ambulansla 112 sevki"],
                    [
                        "Tansiyon ≥ 140/90 + Proteinüri",
                        {"text": "Preeklampsi (Gebelik Toksemisi)", "isMasked": True, "hint": "Sistemik endotel vazospazmı hastalığı"},
                        "Acil sevk et, semptom varsa MgSO4 hazırla"
                    ],
                    ["Hb < 7 g/dl", "Dekompanse derin anemi", "Hastaneye transfüzyon için sevk"],
                    ["Fundus Yüksekliği ±4 cm Sapma", "Fetal büyüme anomalisi / Sıvı sapması", "Ultrason incelemesi için kadın doğuma sevk"]
                ]
            )
        ]
    })

    # Slayt 60: Bölüm Özeti: Gebelik Patolojilerinden Lohusalık ve Kadın İzlemlerine Geçiş
    slides.append({
        "id": "k1-23-s60",
        "title": "Bölüm Özeti: Gebelik Patolojilerinden Lohusalık ve Kadın İzlemlerine Geçiş",
        "section": "Gebelikte Tehlike İşaretleri, Acil Sevk Kriterleri ve Toksemi",
        "slideNumber": 60,
        "narrative": (
            "Gebelik döneminin tehlike işaretlerini, toksemi yönetimini ve acil sevk kurallarını kavrayarak "
            "antenatal izlem sürecinin tüm basamaklarını eksiksiz tamamlamış bulunuyoruz. "
            "Ancak bir kadının sağlık riskleri doğumun gerçekleşmesiyle sona ermez! "
            "Doğumdan sonraki ilk 42 günü kapsayan **Lohusalık (Puerperium)** dönemi; kanama, lohusalık sepsisi, "
            "mastit ve postpartum depresyon gibi ölümcül tabloların en sık patlak verdiği hassas bir penceredir. "
            "Ayrıca toplum sağlığının korunması için yalnızca gebe ve lohusalar değil; doğurganlık çağındaki (15-49 yaş) "
            "gebe olmayan tüm kadınların da periyodik izlemi zorunludur. "
            "Yedinci bölümümüzde, **'Lohusa İzleminin Amaçları ve Takvimi (3 İzlem), DSÖ İlk 24 Saat İlkesi, "
            "Postpartum Kanama/Sepsis ve 15-49 Yaş Kadın İzlemi (Yılda 2 Kez)'** konuları ele alınacaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Doğum eylemi bittikten sonra lohusalık döneminde gelişen maternal ölümlerin en sık görülen doğrudan obstetrik nedeni nedir?",
                "Uterus atonisine bağlı erken postpartum kanamadır.",
                "Miyometriyum kasılma yetersizliği ve masif kan kaybı"
            ),
            make_branching_logic(
                "34 haftalık bir gebe aile hekimine gelerek sabah uyandığında göz kapaklarının ve ellerinin çok şiştiğini, gözünün önünde ışıklar çaktığını ve midesinin üzerinde (epigastrik) şiddetli ağrı olduğunu söylüyor. Tansiyonu 160/105 mmHg ölçülüyor.",
                "Bu hastada hekimin acil düşünmesi gereken tablo ve yapması gereken hayat kurtarıcı adım hangisidir?",
                [
                    {
                        "text": "Ağır Preeklampsi / İmpending Eklampsi tablosu: Hasta eklampsi nöbeti ve HELLP sendromu eşiğindedir; acilen damar yolu açılarak Magnezyum Sülfat yüklemesi planlanmalı ve donanımlı 3. basamak merkeze nakledilmelidir",
                        "isCorrect": True,
                        "feedback": "Mükemmel Karar: Epigastrik ağrı karaciğer kapsül gerilmesidir, gözde ışık çakması serebral vazospazmdır; hasta nöbetin eşiğindedir, acil MgSO4 ve sevk şarttır."
                    },
                    {
                        "text": "Mide ağrısı için antiasit şurup verip tansiyonu 3 gün sonra tekrar ölçmek üzere eve göndermek",
                        "isCorrect": False,
                        "feedback": "Ölümcül Hata: Hasta evde eklamptik nöbet geçirebilir ve beyin kanamasıyla kaybedilebilir."
                    },
                    {
                        "text": "Tuzsuz diyet önerip gebeyi sakinleştirmek",
                        "isCorrect": False,
                        "feedback": "Hatalı ve Yetersiz: Preeklampsi acil tıbbi tablodur, diyetle geçiştirilemez."
                    }
                ]
            )
        ]
    })

    return slides
