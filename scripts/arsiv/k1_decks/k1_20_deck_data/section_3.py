# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-20-s21",
        "title": "Koagülasyon Kaskadının Genel Prensipleri: Enzim, Substrat ve Kofaktör",
        "content": "Sekonder hemostazı yöneten koagülasyon kaskadı, inaktif proenzimlerin ardışık proteolitik aktivasyonu ile yürütülen muazzam bir biyokimyasal basamaklar dizisidir (Sınav Spotu):\n\n- **Serin Proteaz Mantığı:** Pıhtılaşma faktörlerinin çoğu (Faktör XII, XI, IX, VII, X, Protrombin) aktif bölgelerinde serin amino asidi taşıyan **serin proteazlar** ailesine aittir.\n- **Üçlü Kompleks Kuralı:** Kaskadın her basamağında verimli bir reaksiyon gerçekleşebilmesi için üç temel bileşen bir araya gelmelidir:\n  1. **Aktif Enzim (Proteaz):** Önceki basamakta aktive edilmiş serin proteaz (örn. Faktör IXa veya Xa).\n  2. **İnaktif Substrat:** Parçalanarak aktive edilecek hedef proenzim (örn. Faktör X veya Protrombin).\n  3. **Akseleratör Kofaktör:** Reaksiyon hızını binlerce kat artıran yardımcı protein (örn. Faktör VIIIa veya Faktör Va).\n- **Fosfolipid ve Kalsiyum Gereksinimi:** Bu enzim-substrat-kofaktör üçlüsü serbest plazma sıvısında değil; yalnızca aktive trombositlerin **negatif yüklü fosfatidilserin zarı üzerinde ve iyonize Kalsiyum (Ca2+) köprüleriyle** birleşerek çalışabilir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kompleks Bileşeni", "Örnek (Tenaz Kompleksi)", "Örnek (Protrombinaz Kompleksi)"],
                [
                    ["Aktif Enzim (Proteaz)", "Faktör IXa", "Faktör Xa"],
                    ["Akseleratör Kofaktör", "Faktör VIIIa", "Faktör Va"],
                    ["İnaktif Substrat", "Faktör X (hedef)", "Protrombin / Faktör II (hedef)"],
                    ["Platform ve İyon", "Trombosit Zarı (PS) + Ca2+", "Trombosit Zarı (PS) + Ca2+"]
                ]
            ),
            make_cloze(
                "Koagülasyon kaskadında enzim, substrat ve kofaktörün birleşerek hızlı reaksiyon verebilmesi için aktive trombosit zarı üzerindeki fosfatidilserin ve kalsiyum iyonları zorunludur.",
                "kalsiyum iyonları",
                "Negatif fosfolipid ile faktörlerin Gla domenleri arasında köprü kuran iki değerlikli iyon"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-20-s22",
        "title": "K Vitamini Bağımlı Faktörler ve γ-Karboksiglutamat (Gla) Domenleri",
        "content": "Pıhtılaşma faktörlerinin kalsiyum aracılığıyla trombosit zarına bağlanabilmesi özel bir post-translasyonel modifikasyona bağlıdır (Sınav Spotu):\n\n- **K Vitamini Bağımlı Faktörler:** Karaciğerde sentezlenen **Faktör II (Protrombin), Faktör VII, Faktör IX, Faktör X** ile antikoagülan **Protein C ve Protein S** proteinleri K vitaminine bağımlıdır.\n- **Gama-Glutamil Karboksilaz Enzimi:**\n  - Karaciğer mikrozomlarında bu faktörlerin N-terminal ucundaki glutamat (Glu) kalıntılarına karbondioksit eklenerek **gama-karboksiglutamat (Gla)** oluşturulur.\n  - Bu reaksiyonda K vitamini indirgenmiş hidrokinon formundan inaktif **K vitamini epoksit** formuna yükseltgenir.\n- **Kalsiyum Kıskaçları (Kelasyon):** Gla rezidüleri iki adet eksi yüklü karboksil grubu taşır; bu yapı **iki değerlikli pozitif Ca2+ iyonlarını güçlü bir kıskaç gibi tutar**.\n- **Farmakolojik Hedef (Varfarin / Coumadin):** Varfarin **K vitamini epoksit redüktaz (VKORC1)** enzimini bloke eder; karboksilasyon durur, fonksiyonsuz faktörler (PIVKA) dolaşıma verilir ve kan pıhtılaşamaz.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "K Vitamini Bağımlı Karboksilasyon Mekanizması",
                [
                    "1. Hepatik Sentez: Ribozomlarda Faktör II, VII, IX, X polipeptitleri üretilir.",
                    "2. Karboksilaz Uyarımı: İndirgenmiş K vitamini yardımıyla glutamatlar Gla'ya çevrilir.",
                    "3. Kalsiyum Bağlama Kapasitesi: Çift karboksilli Gla domenleri Ca2+ yakalar.",
                    "4. Membran Tutunması: Ca2+ köprüsüyle negatif trombosit zarına kenetlenme sağlanır.",
                    "5. Varfarin Etkisi: VKORC1 blokajı ile Gla oluşumu engellenip antikoagülasyon yapılır."
                ]
            ),
            make_quiz(
                "Aşağıdaki koagülasyon faktörlerinden hangisinin karaciğerde sentezlendikten sonra fonksiyonel hale gelebilmesi için K vitaminine bağımlı gama-karboksilasyon geçirmesi ZORUNLU DEĞİLDİR?",
                [
                    {"key": "A", "text": "Faktör VIII", "isCorrect": True, "explanation": "Doğru cevap A'dır: Faktör VIII karaciğer sinüzoidal endoteli ve diğer endotellerde üretilir, K vitaminine bağımlı DEĞİLDİR. K vitaminine bağımlı faktörler II, VII, IX, X, Protein C ve Protein S'tir."},
                    {"key": "B", "text": "Faktör II (Protrombin)", "isCorrect": False, "explanation": "Protrombin K vitaminine bağımlıdır."},
                    {"key": "C", "text": "Faktör VII", "isCorrect": False, "explanation": "Faktör VII K vitaminine bağımlıdır."},
                    {"key": "D", "text": "Faktör X", "isCorrect": False, "explanation": "Faktör X K vitaminine bağımlıdır."}
                ]
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-20-s23",
        "title": "İn Vivo Kaskadın Başlatıcısı: Doku Faktörü ve Faktör VIIa",
        "content": "Eski tıp kitaplarında pıhtılaşmanın intrinsik ve ekstrinsik olarak iki bağımsız yolla başladığı öğretilirdi; modern hücresel hemostaz modeli bu anlayışı güncellemiştir (Sınav Spotu):\n\n- **İn Vivo Asıl Başlatıcı:** Yaşayan insan vücudunda normal hemostatik pıhtılaşmayı başlatan tek ve asıl mekanizma **Doku Faktörü (TF) - Faktör VIIa yoludur** (klasik ekstrinsik yol).\n- **Faktör VIIa'nın Hazır Bulunması:** Sağlıklı bireylerde dolaşımdaki Faktör VII'nin yaklaşık %1'i daima aktif **Faktör VIIa** halinde dolaşır ancak doku faktörüyle karşılaşmadığı sürece inaktiftir.\n- **TF-VIIa Kompleksinin Çift Yönlü Aktivasyonu:**\n  - Damar kesilip TF açığa çıktığında TF-VIIa kompleksi kurulur.\n  - Bu kompleks doğrudan **Faktör X'u aktive ederek Xa yapar** (klasik ortak yol).\n  - Ancak aynı zamanda **Faktör IX'u da aktive ederek IXa yapar** (intrinsik yola köprü atar).\n- **Sonuç:** Doku faktörü yolu hem doğrudan ortak yola hem de intrinsik yola sinyal göndererek trombin patlamasını ateşler.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İn Vivo Hemostaz Başlatıcısı vs İn Vitro Test Başlatıcısı",
                "İn Vivo Başlatıcı (Fizyolojik)",
                "Doku Faktörü (TF) + Faktör VIIa kompleksidir; hücre zedelenmesiyle tetiklenir.",
                "İn Vitro Başlatıcı (Tüp Laboratuvarı)",
                "Cam boncuk, kaolin veya silika ile negatif yük temasında Faktör XII aktivasyonudur."
            ),
            make_cloze(
                "Canlı vücudunda in vivo hemostazın asıl başlatıcısı subendotelyal doku faktörü ile dolaşımdaki Faktör VIIa arasında kurulan komplekstir.",
                "Faktör VIIa",
                "Doku faktörünü bağlayarak in vivo koagülasyonu ateşleyen K vitamini bağımlı aktif serin proteaz"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-20-s24",
        "title": "İntrinsik Yol: Faktör XII, XI, IX ve VIII (Tenaz Kompleksi)",
        "content": "Klasik intrinsik yol (temas yolağı), laboratuvar testlerinde ve pıhtılaşmanın amplifikasyon fazında kritik roller üstlenir (Sınav Spotu):\n\n- **Temas Aktivasyonu (Faktör XII / Hageman Faktörü):**\n  - Negatif yüklü yabancı yüzeylerle (laboratuvarda cam/kaolin, in vivo ortamda bakteriyel polifosfatlar, nükleik asitler) temas eden Faktör XII aktif Faktör XIIa'ya dönüşür.\n  - **Kritik Sınav Çıkmışı:** Faktör XII eksikliği olan bireylerde in vitro aPTT aşırı uzar ancak **bu hastalarda klinik kanama görülmez**; çünkü in vivo başlatıcı Faktör XII değil Doku Faktörüdür!\n- **Ardışık Basamaklar:** XIIa $\\to$ Faktör XI'i aktif XIa'ya çevirir $\\to$ XIa kalsiyum varlığında Faktör IX'u aktif IXa'ya çevirir.\n- **İntrinsik Tenaz Kompleksi (Kritik Kavşak):**\n  - Enzim: **Faktör IXa**,\n  - Kofaktör: **Faktör VIIIa**,\n  - Substrat: **Faktör X**,\n  - Zemin: Trombosit zarı ve Kalsiyum (Ca2+).\n  - Bu kompleks Faktör X'u ortak yolun merkezinde devasa hızla aktif Faktör Xa'ya dönüştürür.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "İntrinsik Yol ve Tenaz Kompleksi Akışı",
                [
                    "1. Temas / Trombin Geri Beslemesi: Faktör XI aktifleşerek XIa formuna geçer.",
                    "2. Faktör IX Aktivasyonu: XIa enzimi Faktör IX'u proteolitik olarak açar (IXa).",
                    "3. Kofaktör Desteği: Trombin Faktör VIII'i aktive ederek VIIIa kofaktörünü üretir.",
                    "4. Tenaz Montajı: Trombosit zarında IXa + VIIIa + Ca2+ kompleksi kurulur.",
                    "5. Faktör Xa Üretimi: Tenaz kompleksi Faktör X'u aktif Xa'ya dönüştürür."
                ]
            ),
            make_quiz(
                "Hangi koagülasyon faktörünün konjenital eksikliğinde laboratuvarda aPTT süresi belirgin olarak uzamasına rağmen hastada hiçbir klinik kanama diyatezi görülmez?",
                [
                    {"key": "A", "text": "Faktör XII (Hageman Faktörü)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Faktör XII temas yolağını başlatır ve eksikliğinde aPTT uzar; ancak in vivo hemostaz doku faktörüyle yürüdüğü için FXII eksikliğinde kanama olmaz."},
                    {"key": "B", "text": "Faktör VIII", "isCorrect": False, "explanation": "Faktör VIII eksikliği ağır kanama ile seyreden Hemofili A'dır."},
                    {"key": "C", "text": "Faktör IX", "isCorrect": False, "explanation": "Faktör IX eksikliği Hemofili B'dir ve kanama yapar."},
                    {"key": "D", "text": "Faktör XI", "isCorrect": False, "explanation": "Faktör XI eksikliği Hemofili C'dir ve hafif/orta kanama yapabilir."}
                ]
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-20-s25",
        "title": "Ortak Yol: Faktör Xa, Faktör Va ve Protrombinaz Kompleksi",
        "content": "Hem ekstrinsik hem de intrinsik yolakların birleştiği nokta **Ortak Yolun** başlangıcı olan Faktör X aktivasyonudur (Sınav Spotu):\n\n- **Kavşak Noktası (Faktör X):** Hem TF-VIIa kompleksi hem de IXa-VIIIa (tenaz) kompleksi Faktör X'u parçalayarak aktif **Faktör Xa** enzimine dönüştürür.\n- **Protrombinaz Kompleksi (Kaskadın Zirvesi):**\n  - Enzim (Proteaz): **Faktör Xa**\n  - Kofaktör: **Faktör Va** (Trombin tarafından aktive edilir)\n  - Substrat: **Protrombin (Faktör II)**\n  - Zemin: Aktive trombosit zarı (fosfatidilserin) ve **Ca2+ iyonları**.\n- **Muazzam Katalitik Hız:** Tek başına Faktör Xa protrombini çok yavaş parçalar; ancak Faktör Va ve Ca2+ ile protrombinaz kompleksini kurduğunda reaksiyon hızı **yaklaşık 300.000 kat artar**.\n- **Nihai Ürün:** Protrombin (Faktör II), aktif **Trombine (Faktör IIa)** dönüştürülür.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Protrombinaz Bileşeni", "Molekül", "Görevi"],
                [
                    ["Katalitik Enzim", "Faktör Xa", "Protrombini iki yerinden keserek trombini açığa çıkarma"],
                    ["Akseleratör Kofaktör", "Faktör Va", "Reaksiyon hızını 300.000 kat hızlandırma"],
                    ["Hedef Substrat", "Protrombin (Faktör II)", "Trombin monomerine dönüşecek proenzim"],
                    ["Membran Köprüsü", "Ca2+ ve Fosfatidilserin", "Enzim ve kofaktörü trombosit yüzeyine kenetleme"]
                ]
            ),
            make_cloze(
                "Protrombinaz kompleksinde Faktör Xa'nın reaksiyon hızını yüz binlerce kat artıran ve trombin tarafından aktive edilen kofaktör Faktör Va kofaktörüdür.",
                "Faktör Va",
                "Protrombinaz kompleksinin kofaktörü olan ve Faktör V Leiden'de inaktive edilemeyen protein"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-20-s26",
        "title": "Trombinin Çok Yönlü Fonksiyonları: Kaskadın Orkestra Şefi",
        "content": "Trombin (Faktör IIa), koagülasyon kaskadının en kritik, en güçlü ve çok yönlü düzenleyicisidir (Sınav Spotu):\n\n- **1. Fibrin Oluşumu:** Çözünür fibrinojeni parçalayarak fibrinopeptid A ve B'yi ayırır; çözünmeyen **fibrin monomerlerini** üretir.\n- **2. Pıhtı Stabilizasyonu:** **Faktör XIII'ü aktive ederek (XIIIa)** fibrini kovalent çapraz bağlarla sağlamlaştırır.\n- **3. Pozitif Geri Besleme (Kaskadın Güçlendirilmesi):** Kofaktörler olan **Faktör V** ve **Faktör VIII**'i aktive eder; ayrıca **Faktör XI**'i aktive ederek intrinsik yolu ateşler.\n- **4. Güçlü Trombosit Aktivasyonu:** Trombosit yüzeyindeki **PAR (Protease-Activated Receptor)** reseptörlerini keserek agregasyon, TxA2 salgısı ve degranülasyonu doruğa çıkarır.\n- **5. İnflamasyon ve Hücresel Etkiler:** Endotel ve lökositlerdeki PAR reseptörleri üzerinden P-selektin salgısını, nitrik oksit, kemokin ve adezyon molekülü üretimini uyarır.\n- **6. Paradoksal Antikoagülan Rol:** Sağlam endotelde **trombomoduline** bağlandığında prokoagülan özelliğini kaybeder ve **Protein C'yi aktive ederek** kaskadı durdurur.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Trombinin Çoklu Etki Spektrumu",
                [
                    "1. Fibrinojen Kesimi: Fibrinopeptidleri uzaklaştırıp fibrin ağını örer.",
                    "2. Faktör XIII Aktivasyonu: Fibrini çapraz bağlayarak pıhtıyı sertleştirir.",
                    "3. Kofaktör Amplifikasyonu: Faktör V ve VIII'i aktive ederek kaskadı büyütür.",
                    "4. PAR Uyarımı: Trombosit ve endotel hücrelerini aktive eder.",
                    "5. Trombomodulin Bağlantısı: Sağlam endotelde Protein C'yi açıp kaskadı frenler."
                ]
            ),
            make_quiz(
                "Aşağıdakilerden hangisi koagülasyon kaskadının merkezi enzimi olan Trombinin (Faktör IIa) biyolojik görevlerinden biri DEĞİLDİR?",
                [
                    {"key": "A", "text": "Fibrini doğrudan parçalayarak D-Dimer oluşturmak", "isCorrect": True, "explanation": "Doğru cevap A'dır: Fibrini parçalayan enzim trombin değil, Plazmindir! Trombin fibrini oluşturur ve pıhtılaştırır, fibrini eritmez."},
                    {"key": "B", "text": "Fibrinojeni fibrine dönüştürmek", "isCorrect": False, "explanation": "Trombinin temel görevidir."},
                    {"key": "C", "text": "Faktör XIII'ü aktive etmek", "isCorrect": False, "explanation": "Trombin Faktör XIII'ü aktive eder."},
                    {"key": "D", "text": "PAR reseptörleri aracılığıyla trombositleri aktive etmek", "isCorrect": False, "explanation": "Trombin trombositleri PAR üzerinden uyarır."}
                ]
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-20-s27",
        "title": "Fibrinojenin Fibrine Dönüşümü ve Polimerizasyon",
        "content": "Kanın sıvı halden jel kıvamına geçişinin nihai biyokimyasal basamağı fibrinojenin polimerleşmesidir (Sınav Spotu):\n\n- **Fibrinojenin Yapısı:**\n  - Karaciğerde sentezlenen 340 kDa ağırlığında heksamerik bir plazma glikoproteinidir (ikişer adet Aα, Bβ ve γ zinciri taşır).\n  - Molekül bir merkezi **E domeni** ve iki uçta yer alan **D domenlerinden** oluşan simetrik üç loblu bir çubuk yapısındadır.\n- **Trombinin Proteolitik Kesisi:**\n  - Trombin, fibrinojenin merkezi E domenindeki negatif yüklü **Fibrinopeptid A (FPA)** ve **Fibrinopeptid B (FPB)** parçalarını kesip uzaklaştırır.\n  - Bu kesimle elektrostatik itme kuvveti ortadan kalkar ve molekülün adı **Fibrin Monomeri** olur.\n- **Spontan Polimerizasyon:**\n  - Bir fibrin monomerinin E domeni komşu monomerin D domenine kendiliğinden yapışır (D-E-D uç uca ve yan yana bağlanma).\n  - Çözünmeyen uzun fibrin iplikçikleri ve dallanmış **fibrin jeli ağı** oluşur; içine eritrositleri ve lökositleri hapsederek pıhtıyı kurar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Çözünür Fibrinojen vs Çözünmeyen Fibrin Polimeri",
                "Fibrinojen (Çözünür Plazma Proteini)",
                "Fibrinopeptid A ve B taşır; negatif yükler nedeniyle birbirini iter ve plazmada sıvı halde dolaşır.",
                "Fibrin Polimeri (Çözünmeyen Ağ)",
                "Peptidler trombinle kesilmiştir; D ve E domenleri uç uca kenetlenerek çözünmeyen mekanik jel ağı örer."
            ),
            make_cloze(
                "Trombin enzimi çözünür fibrinojen molekülünden fibrinopeptid A ve B parçalarını keserek çözünmeyen fibrin monomerlerini oluşturur.",
                "fibrin monomerlerini",
                "Fibrinopeptidlerin ayrılmasıyla kendiliğinden polimerleşen temel yapı birimi"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-20-s28",
        "title": "Klinik Laboratuvar Testleri: PT / INR vs aPTT",
        "content": "Klinik uygulamada hastanın pıhtılaşma sistemini taramak için iki temel laboratuvar testi kullanılır (Sınav Spotu):\n\n- **Protrombin Zamanı (PT / INR):**\n  - **Değerlendirdiği Yolak:** **Ekstrinsik ve Ortak Yol** (Faktör VII, X, V, Protrombin / II ve Fibrinojen).\n  - **Test Mekanizması:** Sitratlı plazmaya **Doku Faktörü (tromboplastin)**, fosfolipid ve kalsiyum eklenerek pıhtılaşma süresi ölçülür.\n  - **Kullanım Alanı:** **Varfarin (Coumadin)** tedavisinin takibinde (INR olarak), karaciğer yetmezliğinde ve K vitamini eksikliğinde (Faktör VII'nin yarı ömrü çok kısa olduğundan PT hızla uzar).\n- **Aktive Parsiyel Tromboplastin Zamanı (aPTT):**\n  - **Değerlendirdiği Yolak:** **İntrinsik ve Ortak Yol** (Faktör XII, XI, IX, VIII, X, V, II, Fibrinojen).\n  - **Test Mekanizması:** Sitratlı plazmaya negatif yüklü aktivatör (kaolin, silika), fosfolipid ve kalsiyum eklenir.\n  - **Kullanım Alanı:** **Fraksiyone olmayan heparin** takibinde, **Hemofili A (Faktör VIII)** ve **Hemofili B (Faktör IX)** taramasında.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Laboratuvar Testi", "Taranan Yolak ve Faktörler", "Tetikleyici Madde", "Klinik Takip Alanı"],
                [
                    ["Protrombin Zamanı (PT / INR)", "Ekstrinsik + Ortak Yol (VII, X, V, II, I)", "Doku Faktörü + Ca2+", "Varfarin tedavisi, K vitamini eksikliği, karaciğer yetmezliği"],
                    ["aPTT", "İntrinsik + Ortak Yol (XII, XI, IX, VIII, X, V, II, I)", "Kaolin/Silika + Ca2+", "Heparin tedavisi, Hemofili A/B, Lupus antikoagülanı"]
                ]
            ),
            make_quiz(
                "Varfarin (Coumadin) tedavisi alan bir hastada antikoagülasyon düzeyini ve pıhtılaşma kaskadının ekstrinsik yolunu takip etmek amacıyla kullanılan temel laboratuvar parametresi hangisidir?",
                [
                    {"key": "A", "text": "Protrombin Zamanı (PT / INR)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Varfarin ekstrinsik yolun ana faktörü Faktör VII'yi etkilediği için takibinde PT/INR kullanılır."},
                    {"key": "B", "text": "aPTT", "isCorrect": False, "explanation": "aPTT standart heparin takibinde ve Hemofili taramasında kullanılır."},
                    {"key": "C", "text": "Kanama Zamanı", "isCorrect": False, "explanation": "Kanama zamanı trombosit fonksiyonunu gösterir."},
                    {"key": "D", "text": "D-Dimer", "isCorrect": False, "explanation": "D-Dimer fibrinoliz yıkım ürünüdür."}
                ]
            )
        ]
    })

    # Slide 29 - CHECKPOINT 3
    slides.append({
        "id": "k1-20-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Koagülasyon Kaskadı ve Trombin Fonksiyonları",
        "content": "Bu checkpointte koagülasyon kaskadının mimarisini ve testlerini özetliyoruz:\n\n- **Serin Proteazlar:** Enzim, kofaktör ve substrat trombosit zarı üzerinde Ca2+ ile birleşir.\n- **K Vitamini Bağımlılığı:** Faktör **II, VII, IX, X, Protein C ve Protein S** karaciğerde Gla domenleri kazanır; Ca2+ bağlamak için bu şarttır; Varfarin **VKORC1**'i bloke eder.\n- **İn Vivo Başlatıcı:** **Doku Faktörü (TF) - Faktör VIIa** kompleksidir; hem Faktör X'u hem Faktör IX'u aktive eder.\n- **Tenaz Kompleksi:** Faktör **IXa (enzim) + VIIIa (kofaktör)** $\\to$ Faktör X'u aktive eder.\n- **Protrombinaz Kompleksi:** Faktör **Xa (enzim) + Va (kofaktör)** $\\to$ Protrombini trombine çevirir.\n- **Trombin (IIa):** Fibrinojen $\\to$ Fibrin, Faktör XIII aktivasyonu, PAR ile trombosit aktivasyonu, Faktör V, VIII ve XI amplifikasyonu, endotelde Protein C aktivasyonu.\n- **Testler:** **PT (INR)** ekstrinsik yolu (Faktör VII) ve Varfarini tarar; **aPTT** intrinsik yolu (VIII, IX, XI, XII) ve heparini tarar. Faktör XII eksikliğinde aPTT uzar ancak kanama olmaz.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Test / Kompleks", "İçerik / Özellik", "Sınav İçin Kilit Püf Noktası"],
                [
                    ["Protrombin Zamanı (PT)", "Ekstrinsik yol (VII) + Ortak yol", "Varfarin takibi, K vitamini eksikliğinde ilk uzayan test"],
                    ["aPTT", "İntrinsik yol (XII, XI, IX, VIII) + Ortak", "Standart heparin takibi, Hemofili A ve B taraması"],
                    ["Tenaz Kompleksi", "IXa + VIIIa + Ca2+ + Zar", "Eksikliğinde Hemofili A veya B gelişir"],
                    ["Protrombinaz Kompleksi", "Xa + Va + Ca2+ + Zar", "Protrombini trombine çeviren anahtar motor"]
                ]
            ),
            make_chain(
                "Koagülasyon Kaskadının Özeti",
                [
                    "1. Tetikleme: Doku faktörü Faktör VIIa'yı bağlayarak kaskadı açar.",
                    "2. Tenaz: Faktör IXa ve VIIIa birleşerek Faktör X'u aktive eder.",
                    "3. Protrombinaz: Faktör Xa ve Va protrombini parçalayıp trombini üretir.",
                    "4. Fibrin Ağı: Trombin fibrinojeni kesip çözünmeyen polimere çevirir.",
                    "5. Stabilizasyon: Faktör XIIIa kovalent çapraz bağlarla pıhtıyı kilitler."
                ]
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-20-s30",
        "title": "Bölüm Özeti: Koagülasyondan Doğal Antikoagülan Mekanizmalara Geçiş",
        "content": "Bölüm 3 boyunca koagülasyon kaskadının enzimatik mantığını, trombinin rollerini ve PT/aPTT testlerini inceledik:\n\n- **Özet:** Pıhtılaşma faktörleri trombosit yüzeyinde kalsiyum köprüleriyle birleşerek trombin patlaması yaratır ve fibrin ağını örer.\n- **Sonraki Bölüm (Bölüm 4):** Pıhtı oluştuktan sonra damar lümeninin tamamen tıkanmasını engelleyen ve pıhtıyı sınırlandıran **doğal antikoagülan mekanizmaları (Trombomodulin, Protein C/S, Antitrombin III, TFPI) ve Fibrinolitik sistemi (Plazmin, t-PA, D-Dimer)** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Standart fraksiyone edilmemiş heparin tedavisinin antikoagülan etkinliğini izlemek için kullanılan temel laboratuvar pıhtılaşma testi hangisidir?",
                "aPTT (Aktive Parsiyel Tromboplastin Zamanı)",
                "İntrinsik ve ortak yolu değerlendiren laboratuvar testi"
            ),
            make_quiz(
                "Trombin tarafından aktive edilerek çözünmeyen fibrin polimerleri arasında kovalent glutamil-lisil çapraz bağları kuran faktör hangisidir?",
                [
                    {"key": "A", "text": "Faktör XIIIa", "isCorrect": True, "explanation": "Doğru cevap A'dır: Faktör XIIIa (fibrin stabilize edici faktör) kovalent çapraz bağları kurarak pıhtıyı mekanik olarak sağlamlaştırır."},
                    {"key": "B", "text": "Faktör Va", "isCorrect": False, "explanation": "Faktör Va protrombinaz kofaktörüdür."},
                    {"key": "C", "text": "Faktör VIIIa", "isCorrect": False, "explanation": "Faktör VIIIa tenaz kofaktörüdür."},
                    {"key": "D", "text": "Faktör VIIa", "isCorrect": False, "explanation": "Faktör VIIa doku faktörüyle ekstrinsik yolu başlatır."}
                ]
            )
        ]
    })

    return slides
