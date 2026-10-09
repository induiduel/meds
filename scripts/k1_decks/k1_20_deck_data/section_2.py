# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-20-s11",
        "title": "Trombosit Morfolojisi: Megakaryosit Kökeni ve Çekirdeksiz Yapı",
        "content": "Primer hemostazın ana hücresel elemanı olan trombositler (plateletler), klasik hücre tanımına uymayan özelleşmiş sitoplazmik parçacıklardır (Sınav Spotu):\n\n- **Hücresel Köken:** Kemik iliğindeki dev poliploid hücreler olan **megakaryositlerin** sitoplazmik uzantılarından (proplateletler) parçalanarak kana salınırlar.\n- **Çekirdeksiz Yapı:** Trombositlerin çekirdeği (nükleusu) yoktur; bu nedenle genomik DNA transkripsiyonu yapamazlar. Ancak megakaryositten devraldıkları mRNA'lar, zengin organeller, sitoskeleton ve granüller içerirler.\n- **Sayı ve Yaşam Süresi:**\n  - Normal kanda mikrolitrede **150.000 ila 450.000** arasında bulunurlar.\n  - Dolaşımdaki ortalama yaşam süreleri **7 ila 10 gündür**.\n  - Yaşlanan veya hasarlanan trombositler dalak ve karaciğerdeki makrofajlar tarafından fagositozla dolaşımdan temizlenir.\n- **İnaktif Durum:** İstirahat halindeki trombositler bikonveks disk (oval disk) şeklindedir ve endotelle etkileşime girmezler.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Parametre", "Normal Değer / Özellik", "Klinik / Biyolojik Anlamı"],
                [
                    ["Köken Hücre", "Kemik iliği Megakaryositi", "Trombopoietin (TPO) hormonu ile uyarılır"],
                    ["Çekirdek", "Yoktur (Enükleer)", "Protein sentezi kısıtlıdır, DNA içermez"],
                    ["Referans Aralık", "150.000 - 450.000 / µL", "<150.000 trombositopeni, >450.000 trombositoz"],
                    ["Yaşam Süresi", "7 - 10 gün", "Aspirinin antitrombositik etkisi trombosit ömrü boyuncadır"]
                ]
            ),
            make_cloze(
                "Kemik iliğindeki megakaryositlerden tomurcuklanarak dolaşıma verilen trombositlerin ortalama yaşam süresi yedi ila on gündür.",
                "yedi ila on",
                "Trombositlerin periferik kanda dolaştığı ortalama gün süresi"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-20-s12",
        "title": "Membran Fosfolipidleri ve Fosfatidilserin Flip-Flop Mekanizması",
        "content": "Trombosit plazma membranı yalnızca hücreyi sınırlayan bir zar değil, koagülasyon kaskadının montaj platformudur (Sınav Spotu):\n\n- **İstirahat Membran Asimetrisi:**\n  - İnaktif bir trombositte yüksüz fosfolipidler (fosfatidilkolin ve sfingomiyelin) dış tabakada yer alır.\n  - Negatif yüklü fosfolipidler olan **Fosfatidilserin (PS)** ve fosfatidiletanolamin ise enerji harcanarak (flipaz enzimiyle) **iç tabakada (sitoplazmik yüzde)** gizli tutulur.\n- **Aktivasyon ve Flip-Flop:**\n  - Trombosit kollajen veya trombinle uyarıldığında hücre içi Ca2+ patlaması yaşanır; skramblaz enzimi aktive olurken flipaz durdurulur.\n  - Negatif yüklü **fosfatidilserin hızla dış membran yüzeyine döner (flip-flop hareketi)**.\n- **Pıhtılaşma Katalizörü:** Dış yüzeye çıkan negatif yüklü fosfatidilserin başlıkları, kalsiyum (Ca2+) iyonları aracılığıyla **K vitaminine bağımlı pıhtılaşma faktörlerinin (Faktör II, VII, IX, X)** bağlanması için elektrostatik bir platform sağlar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Fosfatidilserin Dışa Dönüş Mekanizması",
                [
                    "1. Dinlenme Hali: Negatif yüklü fosfatidilserin iç yaprakta tutulur.",
                    "2. Trombosit Uyarımı: Trombin ve kollajen hücre içi kalsiyumu artırır.",
                    "3. Skramblaz Aktivasyonu: Membran fosfolipid asimetrisi hızla bozulur.",
                    "4. Fosfatidilserin Dışa Dönüşü: Negatif yükler dış plazma yüzeyine serilir.",
                    "5. Faktör Bağlanması: Kalsiyum aracılığıyla koagülasyon enzimleri zara kenetlenir."
                ]
            ),
            make_quiz(
                "Aktive olmuş trombosit zarında iç tabakadan dış tabakaya geçerek koagülasyon kaskadı enzimlerinin kalsiyum ile bağlanacağı negatif yüklü yüzeyi oluşturan membran fosfolipidi hangisidir?",
                [
                    {"key": "A", "text": "Fosfatidilserin (PS)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Fosfatidilserin aktivasyon sırasında dış yüzeye dönerek K vitamini bağımlı faktörler için katalitik negatif zemin sağlar."},
                    {"key": "B", "text": "Fosfatidilkolin", "isCorrect": False, "explanation": "Fosfatidilkolin yüksüzdür ve normalde dış zarda bulunur."},
                    {"key": "C", "text": "Sfingomiyelin", "isCorrect": False, "explanation": "Sfingomiyelin pıhtılaşma kompleksi bağlamaz."},
                    {"key": "D", "text": "Kolesterol", "isCorrect": False, "explanation": "Kolesterol zar akışkanlığını düzenler, negatif pıhtılaşma platformu değildir."}
                ]
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-20-s13",
        "title": "Alfa (α) Granülleri: Protein Depoları ve P-Selektin",
        "content": "Trombosit sitoplazması, hemostaz ve doku onarımında görevli iki farklı granül tipiyle doludur; en bol bulunanı **Alfa (α) granülleridir** (Sınav Spotu):\n\n- **Sayısal Yoğunluk:** Her trombositte yaklaşık 50 ila 80 adet alfa granülü bulunur.\n- **Protein Zenginliği:** Alfa granülleri büyük protein moleküllerini depolar:\n  1. **Koagülasyon ve Yapışma Proteinleri:** **Fibrinojen**, **von Willebrand Faktörü (vWF)**, **Faktör V**, Faktör XI, protein S ve fibronektin.\n  2. **Yara İyileşmesi ve Büyüme Faktörleri:** **PDGF (Trombosit kaynaklı büyüme faktörü)**, **TGF-β** ve FGF (fibroblast ve düz kas proliferasyonunu uyarırlar).\n- **Membran İmzası: P-Selektin (CD62P):**\n  - Dinlenme halindeki trombositte P-selektin alfa granülünün iç zarındadır.\n  - Degranülasyon (ekzositoz) anında granül zarı dış hücre zarıyla kaynaşır ve **P-selektin trombosit dış yüzeyine çıkar**.\n  - Bu durum trombosit aktivasyonunun akım sitometrisindeki en güvenilir belirtecidir; ayrıca lökositlerin trombosite yapışmasını sağlar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Alfa Granül İçeriği", "Biyolojik Fonksiyonu", "Patofizyolojik Önemi"],
                [
                    ["Fibrinojen ve vWF", "Adezyon ve agregasyon köprüleri kurma", "Trombosit tıkacının mekanik bütünlüğü"],
                    ["Faktör V", "Protrombinaz kompleksinin kofaktörü", "Lokal trombin üretimini katlama"],
                    ["PDGF ve TGF-β", "Yara iyileşmesi ve bağ dokusu uyarımı", "Aterosklerozda düz kas hücresi proliferasyonu"],
                    ["P-Selektin (CD62P)", "Lökosit bağlama ve adezyon", "İnflamasyon ile tromboz arasındaki köprü"]
                ]
            ),
            make_cloze(
                "Trombosit aktivasyonu sırasında alfa granüllerinin zarı dış zara kaynaşarak P-selektin adezyon molekülünü trombosit dış yüzeyine aktarır.",
                "P-selektin",
                "Alfa granül membranında bulunan ve aktivasyonda dış yüze çıkan adezyon molekülü"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-20-s14",
        "title": "Yoğun (Delta) Granülleri: Küçük Moleküller ve ADP Motoru",
        "content": "Alfa granüllerine göre sayıca daha az (trombosit başına 4-8 adet) ancak elektron mikroskobunda çok koyu görünen granüller **Yoğun (Delta - δ) Granüllerdir** (Sınav Spotu):\n\n- **İçerik:** Yoğun granüller protein değil, yüksek konsantrasyonda iyon ve küçük aktif moleküller depolar:\n  1. **Adenozin Difosfat (ADP):** Trombosit aktivasyonunun ve toplanmasının (rekruitment) en güçlü amplifikatörüdür.\n  2. **Adenozin Trifosfat (ATP):** Enerji ve pürinerjik sinyal kaynağıdır.\n  3. **İyonize Kalsiyum (Ca2+):** Koagülasyon faktörlerinin zara bağlanması ve hücre içi kasılma için zorunludur.\n  4. **Serotonin (5-HT):** Vazokonstriksiyonu güçlendirir (trombositler serotonini plazmadan geri alır, kendisi sentezlemez).\n  5. **Epinefrin:** Trombosit adrenerjik reseptörlerini uyarır.\n- **Klinik Bozukluk:** Yoğun granül eksikliği (Storage Pool Disease / Gri Trombosit Sendromu veya Hermansky-Pudlak), ADP yetersizliği nedeniyle primer hemostaz kanamalarına yol açar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Alfa Granülleri vs Yoğun (Delta) Granülleri",
                "Alfa Granülleri (Protein Zengin)",
                "Fibrinojen, vWF, Faktör V, PDGF, TGF-β ve zarında P-selektin içerir; büyüktür.",
                "Yoğun Granülleri (Küçük Molekül Zengin)",
                "ADP, ATP, Kalsiyum (Ca2+), Serotonin ve Epinefrin içerir; elektron-yoğundur."
            ),
            make_quiz(
                "Aşağıdakilerden hangisi trombositlerin yoğun (delta) granüllerinde yüksek konsantrasyonda bulunan moleküllerden biridir?",
                [
                    {"key": "A", "text": "Adenozin difosfat (ADP) ve Kalsiyum (Ca2+)", "isCorrect": True, "explanation": "Doğru cevap A'dır: ADP, ATP, kalsiyum ve serotonin yoğun (delta) granüllerin karakteristik içeriğidir."},
                    {"key": "B", "text": "von Willebrand Faktörü (vWF)", "isCorrect": False, "explanation": "vWF alfa granüllerinde bulunur."},
                    {"key": "C", "text": "Fibrinojen", "isCorrect": False, "explanation": "Fibrinojen alfa granüllerindedir."},
                    {"key": "D", "text": "Trombosit Kaynaklı Büyüme Faktörü (PDGF)", "isCorrect": False, "explanation": "PDGF alfa granüllerindedir."}
                ]
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-20-s15",
        "title": "Trombosit Adezyonu: vWF, Subendotelyal Kollajen ve GpIb",
        "content": "Akut bir damar kesisi olduğunda hızla akan kanın yarattığı yüksek kayma gerilimi (shear stress) altında trombositlerin duvara tutunması özel bir moleküler köprü gerektirir (Sınav Spotu):\n\n- **Yüksek Kayma Gerilimi Problemi:** Arteriyel dolaşımda kan çok hızlı akar; trombositlerin doğrudan kollajene tutunması mekanik olarak imkansızdır.\n- **von Willebrand Faktörü (vWF):**\n  - Endotel hücrelerindeki Weibel-Palade cisimciklerinden ve megakaryositlerden salgılanan devasa bir multimerik glikoproteindir.\n  - Damar hasarında açığa çıkan subendotelyal tip I ve tip III kollajene sıkıca bağlanır.\n  - Kan akımının çekme kuvvetiyle vWF multimeri açılarak trombosit bağlama bölgelerini (A1 domeni) görünür hale getirir.\n- **GpIb-IX-V Reseptör Kompleksi:** Trombosit yüzeyindeki **GpIb** reseptörü açılmış olan vWF'ye kilitlenir.\n- **Sonuç:** Trombosit yüksek hızdaki kan akımında duvara 'fren yaptırılarak' yapıştırılır (**adezyon**).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Trombosit Adezyonunun Moleküler Akışı",
                [
                    "1. Endotel Hasarı: Subendotelyal kollajen kan akımına maruz kalır.",
                    "2. vWF Bağlanması: Plazma ve endotel kökenli vWF kollajene tutunur.",
                    "3. Şekil Açılması: Kayma gerilimiyle vWF multimeri uzayarak A1 bölgesini açar.",
                    "4. GpIb Kilitlenmesi: Trombosit zarı GpIb reseptörüyle vWF'ye bağlanır.",
                    "5. Trombosit Tutunması: Trombosit endotel yüzeyinde yuvarlanmayı bırakıp sabitlenir."
                ]
            ),
            make_cloze(
                "Yüksek kayma gerilimi altında trombositlerin subendotelyal kollajene yapışabilmesi için trombosit GpIb reseptörü ile kollajen arasında von Willebrand faktörü köprü kurar.",
                "von Willebrand faktörü",
                "Subendotelyal matrikse bağlanan ve GpIb reseptörünü tutan devasa multimerik adezyon proteini"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-20-s16",
        "title": "von Willebrand Hastalığı vs Bernard-Soulier Sendromu",
        "content": "Trombosit adezyon köprüsünün iki temel ayağındaki genetik kusurlar iki klasik kanama diyatezi oluşturur (Sınav Spotu):\n\n- **von Willebrand Hastalığı (vWH):**\n  - İnsanlarda en sık görülen kalıtsal kanama bozukluğudur (toplumda yaklaşık %1).\n  - **Köprü molekülü olan vWF'nin** miktar veya fonksiyon eksikliğidir; en sık otozomal dominant (Tip 1 ve Tip 2) kalıtılır.\n  - Ayrıca vWF kanda **Faktör VIII'i taşıyıp stabilize ettiği için**, vWH hastalarında sekonder olarak Faktör VIII düzeyi de düşebilir ve aPTT uzayabilir.\n- **Bernard-Soulier Sendromu:**\n  - Trombosit yüzeyindeki **Glikoprotein Ib-IX-V (GpIb)** reseptör kompleksinin otozomal resesif genetik eksikliğidir.\n  - Kanda vWF normaldir ancak trombosit yüzeyinde reseptör olmadığı için vWF'ye bağlanamaz.\n  - Periferik yaymada **dev trombositler (makrotrombositopeni)** ve trombositopeni tipiktir.\n- **Ortak Özellik:** Her iki hastalıkta da ristocetin ile trombosit agregasyonu uyarılmaz (Ristocetin kofaktör testi bozuktur).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "von Willebrand Hastalığı vs Bernard-Soulier Sendromu",
                "von Willebrand Hastalığı (En Sık)",
                "vWF proteini eksiktir veya kusurludur; Faktör VIII taşıyıcılığı da bozulabilir; otozomal dominanttır.",
                "Bernard-Soulier Sendromu (Nadir)",
                "Trombosit GpIb reseptörü eksiktir; vWF normaldir; kanda dev trombositler görülür; otozomal resesiftir."
            ),
            make_quiz(
                "Kanamaya meyilli bir hastada trombosit sayısı hafif düşük, periferik yaymada belirgin derecede dev trombositler izleniyor ve trombosit yüzeyinde GpIb reseptörünün eksik olduğu saptanıyor. En olası tanı hangisidir?",
                [
                    {"key": "A", "text": "Bernard-Soulier Sendromu", "isCorrect": True, "explanation": "Doğru cevap A'dır: Bernard-Soulier sendromu GpIb reseptör eksikliği ve dev trombositlerle karakterizedir."},
                    {"key": "B", "text": "Glanzmann Trombastenisi", "isCorrect": False, "explanation": "Glanzmann sendromunda GpIIb/IIIa reseptörü eksiktir, trombosit boyutları normaldir."},
                    {"key": "C", "text": "Hemofili A", "isCorrect": False, "explanation": "Hemofili A Faktör VIII eksikliğidir, trombosit reseptörleri normaldir."},
                    {"key": "D", "text": "İmmün Trombositopenik Purpura (ITP)", "isCorrect": False, "explanation": "ITP akkiz bir otoimmün yıkımdır, konjenital GpIb yokluğu yapmaz."}
                ]
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-20-s17",
        "title": "Trombosit Agregasyonu: GpIIb/IIIa ve Fibrinojen Köprüsü",
        "content": "Trombositler damar duvarına yapışıp aktive olduktan sonra birbirlerine tutunarak kitleyi büyütürler; bu olaya **agregasyon** denir (Sınav Spotu):\n\n- **Konformasyonel Değişim (Inside-Out Sinyalizasyon):**\n  - Dinlenme halindeki trombositte GpIIb/IIIa (integrain αIIbβ3) reseptörü inaktif konformasyondadır ve ligand bağlayamaz.\n  - ADP, trombin veya TxA2 ile aktive olan trombositte hücre içinden gelen sinyallerle GpIIb/IIIa dışa doğru açılarak aktif formuna döner.\n- **Fibrinojen ile Çift Taraflı Köprüleşme:**\n  - Fibrinojen simetrik dimerik bir plazma proteinidir; her iki ucunda da GpIIb/IIIa bağlama bölgeleri (RGD sekansı) taşır.\n  - Bir fibrinojen molekülü iki farklı trombositin GpIIb/IIIa reseptörüne aynı anda tutunarak aralarında sağlam bir moleküler köprü kurar.\n- **Geri Dönüşümlüden Geri Dönüşümsüze:**\n  - İlk agregasyon gevşek ve geri dönüşümlüdür.\n  - Ancak ortamda trombin oluştuğunda pıhtı kasılması ve fibrin çökmesi ile agregasyon **kalıcı ve geri dönüşümsüz** hale gelir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Trombosit Agregasyon Süreci",
                [
                    "1. Trombosit Aktivasyonu: ADP ve trombin trombosit reseptörlerini uyarır.",
                    "2. İntegrain Açılması: GpIIb/IIIa reseptörü konformasyonel olarak aktifleşir.",
                    "3. Fibrinojen Yakalama: Dimerik fibrinojen komşu trombosit reseptörlerine bağlanır.",
                    "4. Primer Kümelenme: Yüzlerce trombosit birbirine kenetlenerek tıkaç oluşturur.",
                    "5. Fibrinle Kilitlenme: Trombin devreye girerek agregasyonu geri dönüşümsüz kılar."
                ]
            ),
            make_cloze(
                "Trombositlerin birbirine bağlanarak agregasyon oluşturmasında iki komşu trombositin GpIIb/IIIa reseptörleri arasında köprü vazifesi gören plazma proteini fibrinojen proteinidir.",
                "fibrinojen",
                "GpIIb/IIIa reseptörleri arasında çift taraflı köprü kuran dimerik plazma proteini"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-20-s18",
        "title": "Glanzmann Trombastenisi ve Trombosit Aktivasyon İndükleyicileri",
        "content": "Agregasyon mekanizmasının genetik veya farmakolojik bozuklukları klinikte büyük öneme sahiptir (Sınav Spotu):\n\n- **Glanzmann Trombastenisi:**\n  - Trombosit yüzeyindeki **Glikoprotein IIb/IIIa (GpIIb/IIIa)** kompleksinin otozomal resesif kalıtsal eksikliği veya disfonksiyonudur.\n  - Trombosit adezyonu ve şekil değiştirmesi tamamen normaldir ancak **trombositler birbirine bağlanamaz (agregasyon sıfırdır)**.\n  - Şiddetli mukokutanöz kanamalar, epistaksis ve menoraji görülür; periferik yaymada trombositler kümelenemez, tek tek saçılmış durur.\n- **Üç Temel Aktivasyon İndükleyicisi ve Farmakoloji:**\n  1. **Trombin:** Trombosit yüzeyindeki **PAR-1 ve PAR-4 (Protease-Activated Receptors)** reseptörlerini parçalayarak en güçlü aktivasyonu yapar.\n  2. **ADP:** Yoğun granüllerden salgılanır; **P2Y1 ve P2Y12** reseptörlerine bağlanır (**Klopidogrel, Tikagrelor** P2Y12'yi bloke eder).\n  3. **Tromboksan A2 (TxA2):** Siklooksijenaz-1 (COX-1) ile sentezlenir; güçlü vazokonstriktör ve agregasyon yapıcıdır (**Aspirin** COX-1'i kalıcı inhibe eder).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İndükleyici / Reseptör", "Etki Mekanizması", "Hedef Alan İlaç / Patoloji"],
                [
                    ["GpIIb/IIIa Kompleksi", "Fibrinojen köprüleriyle agregasyon", "Eksikliğinde Glanzmann; blokörler: Abkiksımab, Tirofiban"],
                    ["P2Y12 Reseptörü", "ADP bağlanmasıyla Gi aktivasyonu", "Blokörler: Klopidogrel, Prasugrel, Tikagrelor"],
                    ["COX-1 / TxA2", "Arakidonik asitten TxA2 sentezi", "Kalıcı asetilasyonla inhibe eden: Asetilsalisilik asit (Aspirin)"],
                    ["PAR-1 Reseptörü", "Trombin ile proteolitik aktivasyon", "PAR-1 antagonisti: Vorapaksar"]
                ]
            ),
            make_quiz(
                "Trombosit sayısı ve morfolojisi tamamen normal olan ancak GpIIb/IIIa kompleksi genetik olarak eksik olduğu için trombositleri birbirine bağlanamayan ve agregasyon yapamayan bir hastada tanı hangisidir?",
                [
                    {"key": "A", "text": "Glanzmann Trombastenisi", "isCorrect": True, "explanation": "Doğru cevap A'dır: GpIIb/IIIa eksikliği sonucu trombosit agregasyonunun bozulduğu klasik hastalık Glanzmann trombastenisidir."},
                    {"key": "B", "text": "Bernard-Soulier Sendromu", "isCorrect": False, "explanation": "Bernard-Soulier sendromunda GpIb eksiktir ve dev trombositler vardır."},
                    {"key": "C", "text": "Hemofili B", "isCorrect": False, "explanation": "Hemofili B Faktör IX eksikliğidir."},
                    {"key": "D", "text": "von Willebrand Hastalığı", "isCorrect": False, "explanation": "vWH'de plazma vWF düzeyi düşüktür."},
                ]
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-20-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Trombosit Biyolojisi ve Fonksiyonel Bozukluklar",
        "content": "Bu checkpointte trombositlerin iç yapısını, granüllerini ve kalıtsal hastalıklarını özetliyoruz:\n\n- **Megakaryosit Kökeni:** Trombositler çekirdeksizdir; yaşam süreleri **7-10 gündür**.\n- **Fosfatidilserin Flip-Flop:** Aktivasyonla iç zardan dış zara dönerek **K vitamini bağımlı koagülasyon faktörleri (II, VII, IX, X)** için negatif katalitik zemin hazırlar.\n- **Alfa Granülleri (Protein):** Fibrinojen, vWF, Faktör V, PDGF, TGF-β ve zarda **P-selektin** taşır.\n- **Yoğun (Delta) Granülleri (Küçük Molekül):** **ADP**, ATP, iyonize **Kalsiyum (Ca2+)**, Serotonin ve Epinefrin içerir.\n- **Adezyon Kusurları:**\n  - vWF eksikliği $\\to$ **von Willebrand Hastalığı** (en sık kalıtsal kanama bozukluğu),\n  - GpIb reseptör eksikliği $\\to$ **Bernard-Soulier Sendromu** (dev trombositler).\n- **Agregasyon Kusuru:** GpIIb/IIIa reseptör eksikliği $\\to$ **Glanzmann Trombastenisi** (fibrinojen köprüsü kurulamaz).\n- **İlaç Hedefleri:** Aspirin **COX-1 / TxA2**'yi, Klopidogrel **P2Y12 (ADP)** reseptörünü, Abkiksımab **GpIIb/IIIa**'yı bloke eder.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hastalık / Kusur", "Eksik Molekül", "Bozulan Basamak", "Ayırt Edici Özellik"],
                [
                    ["von Willebrand Hst.", "vWF multimeri", "Adezyon (tutunma)", "En sık kanama hastalığı; Faktör VIII taşıyıcısı"],
                    ["Bernard-Soulier", "GpIb-IX-V reseptörü", "Adezyon (tutunma)", "Kanda dev trombositler (makrotrombositopeni)"],
                    ["Glanzmann Trombasteni", "GpIIb/IIIa reseptörü", "Agregasyon (kümelenme)", "Fibrinojen bağlanamaz, normal boyutlu trombositler"],
                    ["Storage Pool Disease", "Yoğun granüller", "Sekresyon / aktivasyon", "ADP ve kalsiyum depoları boş"]
                ]
            ),
            make_chain(
                "Trombosit Aktivasyonunun Büyük Akışı",
                [
                    "1. Adezyon: vWF ve GpIb ile hasarlı duvara yapışma gerçekleşir.",
                    "2. Şekil Değişimi: Dikenli küreye dönüşüp fosfatidilserini dışa çevirir.",
                    "3. Sekresyon: Alfa granüllerinden proteinler, yoğun granüllerden ADP dökülür.",
                    "4. Agregasyon: GpIIb/IIIa konformasyonu açılır ve fibrinojen köprüleri kurulur."
                ]
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-20-s20",
        "title": "Bölüm Özeti: Trombositten Koagülasyon Kaskadına ve Trombine Geçiş",
        "content": "Bölüm 2 boyunca trombositlerin morfolojisini, granül içeriklerini, adezyon ve agregasyon mekanizmalarını inceledik:\n\n- **Özet:** Trombositler primer tıkacı kurar ve negatif yüklü fosfatidilserin zarlarıyla plazma faktörlerinin toplanma alanını oluşturur.\n- **Sonraki Bölüm (Bölüm 3):** Trombosit tıkacını kalıcı fibrin zırhıyla kaplayan **koagülasyon kaskadını, ekstrinsik ve intrinsik yolları, PT ve aPTT laboratuvar testlerini ve kaskadın orkestra şefi olan Trombini** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Trombosit agregasyonunda görev yapan GpIIb/IIIa reseptörünün konjenital eksikliği sonucu gelişen kanama bozukluğunun adı nedir?",
                "Glanzmann Trombastenisi",
                "Fibrinojen köprülerinin kurulamadığı otozomal resesif fonksiyonel trombosit hastalığı"
            ),
            make_quiz(
                "Klopidogrel ve tikagrelor gibi yaygın kullanılan antiplatelet ilaçlar trombosit yüzeyindeki hangi reseptörü bloke ederek etki gösterir?",
                [
                    {"key": "A", "text": "P2Y12 (ADP reseptörü)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Klopidogrel ve tikagrelor ADP'nin bağlandığı P2Y12 reseptörünü antagonize ederek agregasyonu engeller."},
                    {"key": "B", "text": "Glikoprotein Ib", "isCorrect": False, "explanation": "GpIb vWF reseptörüdür."},
                    {"key": "C", "text": "PAR-1 reseptörü", "isCorrect": False, "explanation": "PAR-1 trombin reseptörüdür."},
                    {"key": "D", "text": "Trombomodulin", "isCorrect": False, "explanation": "Trombomodulin endotel antikoagülan reseptörüdür."}
                ]
            )
        ]
    })

    return slides
