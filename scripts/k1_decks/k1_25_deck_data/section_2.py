# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 2: Tip II (Antikor Aracılı) ve Tip III (İmmün Kompleks Aracılı) Hipersensitivite (Slayt 11 - 20)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_2_slides():
    slides = []

    # Slayt 11: Tip II Aşırı Duyarlılık: Tanım ve Üç Temel Efektör Mekanizma
    slides.append({
        "id": "k1-25-s11",
        "title": "Tip II Aşırı Duyarlılık: Tanım ve Üç Temel Efektör Mekanizma",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 11,
        "narrative": (
            "Tip II aşırı duyarlılık reaksiyonları, doğrudan hedef hücre yüzeyinde veya ekstraselüler matriks dokusunda "
            "yerleşik sabit antijenlere bağlanan spesifik antikorlar (özellikle **IgG ve IgM**) tarafından yürütülür: "
            "1. **Antijen Sabitliği Kuralı:** Antijen serbestçe kanda dolaşmaz; bir eritrosit membranı, bazal membran veya hücre "
            "reseptörü gibi sabit bir anatomik yapıdır. "
            "2. **Üç Temel Efektör Yolak:** "
            "- **Mekanizma 1 (Opsonizasyon ve Fagositoz):** Antikorla kaplanan hücrelerin dalak ve karaciğer fagositlerince yutulması veya komplemanla parçalanması. "
            "- **Mekanizma 2 (Kompleman ve Fc Aracılı İnflamasyon):** Dokuya bağlanan antikorların komplemanı aktive ederek nötrofilleri çekmesi ve lokal doku nekrozu yapması. "
            "- **Mekanizma 3 (Hücresel Disfonksiyon):** Antikorun hücre reseptörünü bloke etmesi veya aşırı uyarması sonucu inflamasyon olmaksızın fonksiyonun bozulması."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tip II Hipersensitivite Üç Temel Efektör Mekanizması",
                ["Mekanizma Tipi", "İmmünolojik Yolak", "Histopatolojik Sonuç", "Klinik Prototip Hastalıklar"],
                [
                    ["Opsonizasyon / Fagositoz", "Fc reseptörü ve C3b fagositozu", "Hücre sayısı azalması (sitopeni)", "Otoimmün hemolitik anemi, ITP"],
                    [
                        "Doku İnflamasyonu",
                        "C5a kemotaksisi ve nötrofil aktivasyonu",
                        {"text": "Bazal membran yıkımı ve nekroz", "isMasked": True, "hint": "Lökosit enzimleriyle doku bütünlüğünün parçalanması"},
                        "Goodpasture sendromu, Pemfigus vulgaris"
                    ],
                    ["Reseptör Disfonksiyonu", "Reseptör blokajı veya kontrolsüz uyarım", "İnflamasyonsuz fonksiyonel arıza", "Miyastenia gravis, Graves hastalığı"]
                ]
            ),
            make_active_recall(
                "Tip II aşırı duyarlılık reaksiyonlarında doku ve hücre hasarını başlatan primer antikor sınıfları hangileridir?",
                "IgG ve IgM izotipleridir.",
                "Kompleman bağlayabilen ve Fc reseptörlerince tanınan primer immünoglobulinler"
            )
        ]
    })

    # Slayt 12: Tip II Mekanizma 1: Opsonizasyon, Fagositoz ve Hücre Yıkımı
    slides.append({
        "id": "k1-25-s12",
        "title": "Tip II Mekanizma 1: Opsonizasyon, Fagositoz ve Hücre Yıkımı",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 12,
        "narrative": (
            "Dolaşımdaki kan hücrelerinin yüzey antijenlerine bağlanan antikorlar, bu hücreleri mononükleer fagositik sistemin hedefi yapar: "
            "1. **Opsonizasyon Süreci:** Eritrosit veya trombosit yüzeyine bağlanan IgG'nin Fc kuyruğu, dalak ve karaciğer makrofajlarındaki "
            "**Fc-gama reseptörleri (FcgammaR)** tarafından tanınır. Eşzamanlı aktive olan komplemanın **C3b ve iC3b** fragmanları da "
            "makrofajların C3b reseptörlerine (CR1) kenetlenir. "
            "2. **Ekstravasküler Hemoliz:** Opsonize eritrositler dalak kordonlarından geçerken makrofajlarca fagositozla yutulur (Otoimmün Hemolitik Anemi / AIHA). "
            "Eritrosit membranı kısmen koparıldığında küresel, sert mikrosferositler oluşur. "
            "3. **Diğer Sitopeniler:** Trombosit yüzeyindeki GpIIb/IIIa kompleksine karşı antikorlar İmmün Trombositopenik Purpuraya (ITP), "
            "Rh antijenine karşı maternal antikorlar Yenidoğanın Hemolitik Hastalığına (Eritroblastozis Fetalis) yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Otoimmün Hemolitik Anemi Opsonizasyon Zinciri",
                [
                    "1. Otoantikor Bağlanması: Eritrosit membran Rh veya I antijenine IgG antikorlarının yapışması",
                    "2. Dalak Geçişi: Opsonize eritrositlerin dalak kırmızı pulpa sinüzoidlerine girmesi",
                    "3. Fc ve C3b Tanınması: Makrofaj yüzeyindeki FcgammaR ve CR1 reseptörlerinin pıhtıyı yakalaması",
                    "4. Fagositoz ve Yıkım: Eritrositin yutulması veya sferosite dönüştürülerek parçalanması"
                ]
            ),
            make_cloze(
                "Otoimmün hemolitik anemide eritrositlerin dalak makrofajları tarafından fagositozunu kolaylaştıran temel kompleman opsonini C3b molekülüdür.",
                "C3b",
                "Fagositoz reseptörlerince tanınan üçüncü kompleman opsonin parçası"
            )
        ]
    })

    # Slayt 13: Tip II Mekanizma 2: Kompleman ve Fc Aracılı Doku İnflamasyonu
    slides.append({
        "id": "k1-25-s13",
        "title": "Tip II Mekanizma 2: Kompleman ve Fc Aracılı Doku İnflamasyonu",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 13,
        "narrative": (
            "Antikorlar hücre serbestken değil, bazal membran veya hücreler arası bağlantı gibi sabit doku elemanlarına bağlandığında "
            "lokal inflamatuar yıkım başlar: "
            "1. **Goodpasture Sendromu:** Glomerül ve pulmoner alveol bazal membranındaki **Tip IV kollajenin alfa-3 zincirine** "
            "karşı otoantikorlar gelişir. İmmünofloresan mikroskopide bazal membran boyunca kesintisiz **lineer (çizgisel) IgG birikimi** izlenir. "
            "Kompleman aktivasyonuyla (C5a) nötrofiller toplanır; nekrotizan kresentik glomerülonefrit ve ölümcül akciğer kanaması gelişir. "
            "2. **Pemfigus Vulgaris:** Epidermis keratinositlerini birbirine bağlayan desmozom proteini **desmoglein-3**'e karşı antikorlar "
            "gelişir. Hücreler birbirinden ayrılır (**akantoliz**); intraepidermal suprabazal gevşek büller oluşur. "
            "3. **Akut Romatizmal Ateş:** Streptokok M proteinine karşı antikorların kalp miyozini ile çapraz reaksiyonu (miyokardit)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Tip II İnflamatuar Doku Hasarı Prototip Hastalıkları",
                ["Hastalık Adı", "Hedef Sabit Doku Antijeni", "Histopatolojik / İmmünofloresan Bulgusu", "Klinik Tablo"],
                [
                    [
                        "Goodpasture Sendromu",
                        "Tip IV kollajen alfa-3 zinciri",
                        {"text": "Lineer (çizgisel) IgG ve C3 birikimi", "isMasked": True, "hint": "Bazal membran boyunca pürüzsüz düz bir çizgi halinde floresan ışıma"},
                        "Hemoptizi ve hızlı ilerleyen glomerülonefrit"
                    ],
                    ["Pemfigus Vulgaris", "Desmoglein-3 (desmozomlar)", "İntraepidermal akantoliz, suprabazal bül", "Ağrılı mukozal ve kutanöz erozyonlar"],
                    ["Akut Romatizmal Ateş", "Kalp sarkolemması ve miyozin", "Aschoff cisimcikleri ve Anitschkow hücreleri", "Pankardit, poliartrit, Sydenham koresi"]
                ]
            ),
            make_micro_quiz(
                "Goodpasture sendromu şüphesiyle yapılan böbrek biyopsisinde glomerül bazal membranında immünofloresan mikroskopide beklenen karakteristik antikor boyanma paterni hangisidir?",
                {
                    "A": "Bazal membran boyunca kesintisiz lineer (çizgisel) IgG birikimi",
                    "B": "Mezangiyumda düzensiz granüler kaba birikim",
                    "C": "Subepitelyal aralıkta aralıklı hörgüç (hump) tarzı birikim",
                    "D": "Damar duvarında konsantrik 'soğan zarı' fibrin birikimi",
                    "E": "Tamamen negatif immünofloresan (pauci-immün) görünüm"
                },
                "A",
                {
                    "A": "Doğrudur; Tip IV kollajen bazal membranda homojen dağıldığı için antikorlar lineer (düz çizgisel) birikir.",
                    "B": "Yanlış; granüler birikim Tip III immün kompleks nefritlerine özgüdür.",
                    "C": "Yanlış; subepitelyal hörgüç poststreptokoksik nefritte görülür.",
                    "D": "Yanlış; soğan zarı malign hipertansiyonda görülür.",
                    "E": "Yanlış; pauci-immün vaskülit ANCA ilişkili glomerülonefrittir."
                }
            )
        ]
    })

    # Slayt 14: Tip II Mekanizma 3: Reseptör Aracılı Hücresel Fonksiyon Bozukluğu
    slides.append({
        "id": "k1-25-s14",
        "title": "Tip II Mekanizma 3: Reseptör Aracılı Hücresel Fonksiyon Bozukluğu",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 14,
        "narrative": (
            "Bazı Tip II aşırı duyarlılık reaksiyonlarında antikorlar hücreyi öldürmez veya inflamasyon yapmaz; doğrudan reseptör işlevini değiştirir: "
            "1. **Miyastenia Gravis (Reseptör Blokajı):** İskelet kası motor son plağındaki nikotinik **Asetilkolin reseptörlerine (AChR)** "
            "karşı antikorlar oluşur. Antikorlar reseptörü bloke eder, endositozla içeri çeker ve yıkar. Sinir-kas iletimi kesilir; "
            "gün içinde yorulmakla artan pitozis, diplopi ve proksimal kas güçsüzlüğü gelişir. Hastaların %65'inde timus hiperplazisi, %15'inde timoma vardır. "
            "2. **Graves Hastalığı (Reseptör Stimülasyonu):** Tiroid folikül hücrelerindeki **TSH reseptörlerine** karşı stimülan "
            "antikorlar (TSI) bağlanır. TSH gibi davranarak adenilat siklazı sürekli uyarır; kontrolsüz tiroid hormonu sentezi, "
            "diffüz toksik guatr, taşikardi, ekzoftalmus ve pretibial miksödem tablosu doğar. "
            "3. **Pernisiyöz Anemi:** Mide pariyetal hücrelerine ve intrinsik faktöre (IF) karşı antikorlar B12 emilimini bloke eder."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Reseptör Fonksiyon Değişimi Karşılaştırması",
                "Miyastenia Gravis (İnhibisyon)",
                "ACh reseptörlerine blokan antikor bağlanması, reseptör kaybı ve çizgili kas güçsüzlüğü",
                "Graves Hastalığı (Aktivasyon)",
                "TSH reseptörüne stimülan antikor bağlanması, kontrolsüz tiroid hormon üretimi ve hipertiroidizm"
            ),
            make_active_recall(
                "Miyastenia gravis hastalığında otoantikorların bağlandığı ve sinir-kas kavşağında iletiyi engelleyen hedef postsinaptik membran reseptörü hangisidir?",
                "Asetilkolin reseptörüdür (nikotinik AChR).",
                "Nöromusküler kavşakta motor son plakta yer alan kolinerjik reseptör"
            )
        ]
    })

    # Slayt 15: Tip III Aşırı Duyarlılık: Tanım, İmmün Kompleksler ve Patogenez
    slides.append({
        "id": "k1-25-s15",
        "title": "Tip III Aşırı Duyarlılık: Tanım, İmmün Kompleksler ve Patogenez",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 15,
        "narrative": (
            "Tip III aşırı duyarlılık, dolaşımda serbest halde bulunan çözünür antijenler ile antikorların birleşerek "
            "**antijen-antikor (immün) kompleksleri** oluşturması ve bunların dokulara çökmesiyle karakterizedir: "
            "1. **Antijen-Antikor Dinamikleri:** "
            "- **Büyük Kompleksler (Antikor Fazlalığı):** Karaciğer ve dalaktaki mononükleer fagositlerce hızla temizlenir; zararsızdır. "
            "- **Küçük Kompleksler:** Filtre olmadan idrarla atılır veya çökelmez. "
            "- **Orta Büyüklükteki Kompleksler (Hafif Antijen Fazlalığı):** Dolaşımda uzun süre kalır; mononükleer fagositlerce yakalanamaz "
            "ve yüksek hidrostatik basınç altındaki vasküler filtrasyon yataklarına (renal glomerüller, sinovya, koroid pleksus) çöker. "
            "2. **Çökme Bölgeleri:** Kompleksler damar duvarına mekanik olarak gömülür ve endotel altında hapsolur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İmmün Kompleks Büyüklüğü ve Patolojik Kaderi",
                ["Kompleks Büyüklüğü", "Antijen/Antikor Oranı", "Fagositik Klirens Hızı", "Damar Duvarına Çökme ve Doku Hasarı Riski"],
                [
                    ["Büyük İmmün Kompleksler", "Antikor Fazlalığı / Denge", "Çok Hızlı (Dalak makrofajlarınca yutulur)", "Düşük (Hastalık yapmaz)"],
                    [
                        "Orta Büyüklükteki Kompleksler",
                        "Hafif Antijen Fazlalığı",
                        {"text": "Yetersiz / Kaçar", "isMasked": True, "hint": "Dolaşımda uzun süre kalarak damar duvarına gömülme nedeni"},
                        "En Yüksek (Vaskülit ve nefrit yapar)"
                    ],
                    ["Küçük İmmün Kompleksler", "Aşırı Antijen Fazlalığı", "Düşük", "Düşük (Böbrekten filtre olur, çökmez)"]
                ]
            ),
            make_cloze(
                "Tip III aşırı duyarlılık reaksiyonlarında doku hasarına yol açan ve damar duvarına en kolay çöken kompleksler hafif antijen fazlalığında oluşan orta büyüklükteki komplekslerdir.",
                "orta",
                "Fagositlerce yakalanamayıp endotel altına gömülen immün kompleks boyutu"
            )
        ]
    })

    # Slayt 16: Tip III Patogenez Kaskadı: Kompleman Aktivasyonu ve Fibrinoid Nekroz
    slides.append({
        "id": "k1-25-s16",
        "title": "Tip III Patogenez Kaskadı: Kompleman Aktivasyonu ve Fibrinoid Nekroz",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 16,
        "narrative": (
            "İmmün komplekslerin damar duvarına çökmesiyle başlayan inflamasyon yıkıcı bir vaskülit tablosuna dönüşür: "
            "1. **Kompleman Aktivasyonu:** Damar bazal membranına sıkışan komplekslerin Fc parçaları klasik kompleman yolağını uyarır. "
            "Ortaya çıkan **C3a ve C5a** kemotaktik anafilatoksinleri nötrofilleri hızla bölgeye çeker. "
            "2. **Çaresiz Fagositoz (Frustrated Phagocytosis):** Nötrofiller damar bazal membranına yapışık devasa kompleksleri "
            "içlerine alamazlar; fagositoz başarısız olunca nötrofil lizozomal enzimleri ve reaktif oksijen radikalleri (ROS) damar duvarına kusulur. "
            "3. **Fibrinoid Nekroz:** Damar duvarı nekroza uğrar; dolaşımdan sızan plazma proteinleri, kompleman parçacıkları ve fibrin "
            "damar duvarında parlak pembe, homojen bir kitle halinde çöker. Bu görünüm Tip III vaskülitinin histopatolojik imzası olan **Fibrinoid Nekrozdur**."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Tip III Vaskülit ve Fibrinoid Nekroz Kaskadı",
                [
                    "1. Kompleks Çöküşü: Orta boy immün komplekslerin arteriyol veya glomerül endotel altına yerleşmesi",
                    "2. C5a ve C3a Salınımı: Klasik kompleman fiksasyonu ile güçlü lökosit kemotaksinlerinin üretilmesi",
                    "3. Nötrofil Enzim Kusması: Damar duvarına sıkışan kompleksi yutamayan nötrofillerin proteaz salması",
                    "4. Fibrinoid Nekroz: Damar düz kasının ölmesi ve lümenden sızan fibrinin pembe birikinti oluşturması"
                ]
            ),
            make_active_recall(
                "Tip III hipersensitivite zemininde gelişen akut vaskülit lezyonlarında damar duvarında immün kompleks, kompleman ve fibrin birikimiyle oluşan parlak pembe histopatolojik nekroz türü hangisidir?",
                "Fibrinoid nekrozdur.",
                "Damar duvarında fibrin birikimiyle karakterize parlak eozinofilik nekroz"
            )
        ]
    })

    # Slayt 17: Tip III Sistemik Hastalık Prototipi: Akut Serum Hastalığı
    slides.append({
        "id": "k1-25-s17",
        "title": "Tip III Sistemik Hastalık Prototipi: Akut Serum Hastalığı",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 17,
        "narrative": (
            "Akut serum hastalığı, sistemik Tip III aşırı duyarlılığın klasik deneysel ve klinik modelidir: "
            "1. **Tarihsel ve Güncel Nedenler:** Eskiden difteri tedavisinde at serumu infüzyonundan sonra görülürken, günümüzde "
            "yılan antivenomları veya fare kökenli monoklonal antikor tedavileri (rituksimab vb.) sonrası ortaya çıkar. "
            "2. **Zaman Çizelgesi (7 - 14 Gün):** Yabancı antijen verildikten yaklaşık bir ila iki hafta sonra konak bu antijene "
            "karşı IgG üretir. Kanda antijen ve antikor bir araya gelerek immün kompleksler oluşturur. "
            "3. **Klinik Triad:** Komplekslerin eklemlere, deriye ve böbreklere çökmesiyle **ateş, ürtiker/döküntü, artralji/artrit**, "
            "lenfadenopati ve geçici proteinüri gelişir. "
            "4. **Kompleman Tüketimi:** Damarlarda kompleman tüketildiği için serum **C3 ve C4** düzeyleri geçici olarak belirgin düşer (hipokomplemantemi)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Akut Serum Hastalığının Klinik Evreleri",
                ["Zaman Penceresi", "İmmünolojik Durum", "Kandaki Serbest Antikor / Antijen", "Klinik Belirti"],
                [
                    ["1 - 5. Gün", "Sensitizasyon ve antijen işleme", "Yüksek serbest antijen, sıfır antikor", "Asemptomatik latent dönem"],
                    [
                        "7 - 10. Gün (Kriz)",
                        "Masif immün kompleks oluşumu ve çökme",
                        {"text": "Kompleksler dorukta, serum C3/C4 düşmüş", "isMasked": True, "hint": "Kanda komplemanın tükendiği ve vaskülitin alevlendiği dönem"},
                        "Ateş, ürtiker, poliartralji, proteinüri"
                    ],
                    ["2 - 3. Hafta", "Antijen tükenmesi ve serbest antikor artışı", "Serbest IgG antikorları yüksek, kompleksler temizlenmiş", "Klinik iyileşme ve nefritin gerilemesi"]
                ]
            ),
            make_micro_quiz(
                "Yabancı bir terapötik protein (antivenom) verilmesinden 10 gün sonra ateş, yaygın kaşıntılı döküntü, eklem ağrıları ve proteinüri gelişen bir hastada serum laboratuvarında hangisinin saptanması Tip III serum hastalığını doğrular?",
                {
                    "A": "Serum kompleman (C3 ve C4) düzeylerinde belirgin düşüş",
                    "B": "Serum IgE düzeyinde 1000 kat artış",
                    "C": "Periferik kanda CD8+ T hücrelerinin tamamen sıfırlanması",
                    "D": "Serum kalsiyum düzeyinin masif yükselmesi",
                    "E": "Trombosit sayısının 1 milyonun üzerine çıkması"
                },
                "A",
                {
                    "A": "Doğrudur; immün kompleksler klasik kompleman yolağını masif olarak fikse ettiği için serum C3 ve C4 düzeyleri düşer (hipokomplemantemi).",
                    "B": "Yanlış; IgE Tip I aşırı duyarlılık belirtecidir.",
                    "C": "Yanlış; CD8+ hücreler sıfırlanmaz.",
                    "D": "Yanlış; kalsiyum metabolizması değişmez.",
                    "E": "Yanlış; trombositopeni görülebilir ancak masif trombositoz beklenmez."
                }
            )
        ]
    })

    # Slayt 18: Tip III Lokal Reaksiyon Prototipi: Arthus Reaksiyonu ve Klinik Örnekler
    slides.append({
        "id": "k1-25-s18",
        "title": "Tip III Lokal Reaksiyon: Arthus Reaksiyonu ve Klinik Spektrum",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 18,
        "narrative": (
            "İmmün kompleks hasarı kanda yaygın dolaşmak yerine lokal bir anatomik noktada da tetiklenebilir: "
            "1. **Arthus Reaksiyonu (Lokal Tip III):** Kanda önceden yüksek düzeyde IgG antikoru bulunan bir bireye "
            "antijenin intrakutan (deri içine) enjekte edilmesiyle gelişir. Antijen dermisteki kapillerlerden sızan "
            "antikorlarla lokal olarak birleşir. Birkaç saat içinde enjeksiyon yerinde lokal vaskülit, tromboz, ödem ve ağır doku nekrozu gelişir. "
            "2. **Klinik Tip III Hastalık Spektrumu:** "
            "- **Sistemik Lupus Eritematozus (SLE):** Çekirdek antijenlerine (DNA/histon) karşı oluşan komplekslerin glomerüllere çökmesiyle lupus nefriti. "
            "- **Poststreptokoksik Glomerülonefrit (PSGN):** Streptokok antijen-antikor komplekslerinin glomerül bazal membranında "
            "çökmesiyle kaba **granüler (hump / hörgüç)** birikimler. "
            "- **Poliarteritis Nodoza (PAN):** Hepatit B antijen komplekslerine bağlı orta çaplı arter vasküliti."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Tip II vs Tip III İmmünofloresan Boyanma Paternleri",
                "Tip II Glomerülonefrit (Goodpasture)",
                "Bazal membranın homojen sabit antijenine bağlanan antikorların oluşturduğu pürüzsüz düz LİNEER patern",
                "Tip III Glomerülonefrit (SLE / PSGN)",
                "Dolaşımdan düzensiz öbekler halinde çöken komplekslerin oluşturduğu benekli GRANÜLER patern"
            ),
            make_active_recall(
                "İmmünofloresan mikroskopide Goodpasture sendromundaki düz çizgisel lineer boyanmanın aksine, Tip III glomerülonefritlerde izlenen kesintili benekli boyanma paternine ne ad verilir?",
                "Granüler boyanma paterni denir.",
                "Dolaşan komplekslerin rastgele damar duvarına oturmasıyla oluşan kum tanesi manzarası"
            )
        ]
    })

    # Slayt 19: Checkpoint 2
    slides.append({
        "id": "k1-25-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 19,
        "narrative": (
            "Bu ikinci kontrol noktasında, Tip II ve Tip III hipersensitivite ayrımını ve patolojilerini pekiştiriyoruz: "
            "1. **Tip II Temeli:** Hedef hücre veya bazal membrandaki sabit antijene bağlanan IgG/IgM'dir. "
            "2. **Tip II Formları:** Opsonizasyonla hemoliz (AIHA), komplemanla inflamasyon (Goodpasture, Pemfigus) ve "
            "reseptör disfonksiyonu (Miyastenia'da blokaj, Graves'te stimülasyon). "
            "3. **Tip III Temeli:** Dolaşımda çözünür antijen ile IgG/IgM'nin birleşerek damar duvarına çökmesidir. "
            "4. **Kompleks Boyutu:** En tehlikelisi hafif antijen fazlalığında oluşan orta büyüklükteki komplekslerdir. "
            "5. **Fibrinoid Nekroz:** Tip III vaskülitinde nötrofillerin lizozom kusması sonucu gelişen karakteristik pembe lezyondur. "
            "6. **İmmünofloresan Ayrımı:** Tip II Goodpasture'de düz LİNEER, Tip III nefritlerde (SLE/PSGN) kesintili GRANÜLER boyanma izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s19-1",
                "İmmünofloresan mikroskopide Tip II Goodpasture nefritinde lineer boyanma izlenirken, Tip III glomerülonefritlerde izlenen karakteristik benekli boyanma kalıbı nedir?",
                "Granüler birikim paternidir.",
                "Dolaşan pıhtı kümelerinin bazal zarda kesintili çökelti manzarası",
                "Granüler vs Lineer Patern"
            ),
            make_flashcard(
                "k1-25-fc-s19-2",
                "Tip II aşırı duyarlılık zemininde gelişen Goodpasture sendromunda otoantikorların yöneldiği primer bazal membran bileşeni nedir?",
                "Tip IV kolajen alfa-3 zinciridir.",
                "Glomerül ve alveol bazal matriksinde yer alan dördüncü tip bağ dokusu alt birimi",
                "Goodpasture Antijeni"
            ),
            make_flashcard(
                "k1-25-fc-s19-3",
                "Tip III hipersensitivite reaksiyonlarında nötrofilik proteazların damar duvarını eritmesi ve fibrin birikmesiyle oluşan histopatolojik lezyon nedir?",
                "Fibrinoid nekroz lezyonudur.",
                "Arteriyol duvarında plazma proteinlerinin meydana getirdiği homojen pembe erime tabakası",
                "Fibrinoid Nekroz"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tip II vs Tip III Ayırıcı Tanı Özeti",
                ["Özellik", "Tip II Hipersensitivite", "Tip III Hipersensitivite"],
                [
                    ["Antijenin Durumu", "Sabit doku / hücre yüzey antijeni", "Kanda çözünür dolaşan antijen"],
                    ["Kompleks Oluşum Yeri", "Doğrudan doku üzerinde yerinde (in situ)", "Dolaşımda kanda birleşir ve sonra çöker"],
                    [
                        "Glomerül Floresan Paterni",
                        "Lineer (düz çizgisel)",
                        {"text": "Granüler (kaba benekli)", "isMasked": True, "hint": "SLE ve poststreptokoksik nefritte görülen kesintili desen"}
                    ],
                    ["Damar Duvarı Lezyonu", "Genellikle vaskülit yapmaz (bazal membran lizisi)", "Klasik Fibrinoid Nekroz ve lökositoklastik vaskülit"],
                    ["Klinik Örnekler", "AIHA, Goodpasture, Pemfigus, Graves", "Akut serum hastalığı, Arthus, SLE nefriti, PSGN"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki hastalıklardan hangisi Tip II aşırı duyarlılık DEĞİL, Tip III immün kompleks aracılı aşırı duyarlılık mekanizmasıyla gelişir?",
                {
                    "A": "Sistemik Lupus Eritematozus glomerülonefriti (Lupus nefriti)",
                    "B": "Otoimmün Hemolitik Anemi",
                    "C": "Goodpasture Sendromu",
                    "D": "Miyastenia Gravis",
                    "E": "Pemfigus Vulgaris"
                },
                "A",
                {
                    "A": "Doğrudur; SLE nefriti DNA-antiDNA immün komplekslerinin glomerüllere çökmesiyle gelişen klasik Tip III tablosudur.",
                    "B": "Yanlış; eritrosit opsonizasyonu Tip II mekanizmasıdır.",
                    "C": "Yanlış; Tip IV kollajene karşı lineer antikor Tip II mekanizmasıdır.",
                    "D": "Yanlış; ACh reseptör blokajı Tip II mekanizmasıdır.",
                    "E": "Yanlış; desmogleine karşı antikor Tip II mekanizmasıdır."
                }
            )
        ]
    })

    # Slayt 20: Bölüm Özeti: Hümoral Hasardan T Hücre Aracılı Tip IV Hipersensitiviteye Geçiş
    slides.append({
        "id": "k1-25-s20",
        "title": "Bölüm Özeti: Hümoral Hasardan T Hücre Aracılı Tip IV Hipersensitiviteye Geçiş",
        "section": "Tip II ve Tip III Aşırı Duyarlılık Mekanizmaları",
        "slideNumber": 20,
        "narrative": (
            "İlk üç aşırı duyarlılık tipinin ortak paydası antikorların (IgE, IgG, IgM) efektör molekül olarak işlev görmesidir: "
            "1. **Antikor Sınırı:** Tip I, II ve III reaksiyonlarında antikorlar hedefi tanır, komplemanı çağırır veya mast hücresini degranüle eder. "
            "2. **Hücresel Dünyaya Geçiş:** Ancak bağışıklık sisteminin en güçlü doku yıkım mekanizmalarından biri doğrudan T lenfositleri "
            "tarafından yürütülür; buna **Tip IV (Hücresel / Gecikmiş Tip) Aşırı Duyarlılık** adı verilir. "
            "3. **T Hücre Çift Kollu Gücü:** Tip IV'te CD4+ T hücreleri sitokin salgılayarak makrofajları aktive eder (Gecikmiş Tip Aşırı Duyarlılık - DTH) "
            "veya CD8+ sitotoksik T hücreleri hedef hücreleri doğrudan delerek öldürür (perforin/granzim). "
            "Bölüm 3'te tüberkülin testinden granülomlara ve kontakt dermatite kadar Tip IV patolojisini inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "İmmün Yanıt Efektör Ayrımı",
                "Hümoral Hipersensitivite (Tip I, II, III)",
                "B hücresi kökenli antikorlar (IgE/IgG/IgM), kompleman aktivasyonu ve erken mikrovasküler yıkım",
                "Hücresel Hipersensitivite (Tip IV)",
                "T lenfositleri (CD4+ Th1/Th17 ve CD8+ CTL), makrofaj aktivasyonu, granülomlar ve geç doku nekrozu"
            ),
            make_active_recall(
                "Coombs ve Gell sınıflamasında gelişmesi 24 ile 48 saat süren ve antikorlar yerine doğrudan antijene duyarlı T lenfositleriyle yürütülen tek hipersensitivite tipi hangisidir?",
                "Tip IV (Gecikmiş Tip / Hücresel) aşırı duyarlılıktır.",
                "T lenfosit aracılı hücresel immünite tipi"
            )
        ]
    })

    return slides
