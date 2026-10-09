# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
Bölüm 8: Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi (Slayt 71 - 80)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # Slayt 71: Bebek ve Çocuk İzleminin Amaçları ve Koruyucu Stratejiler
    slides.append({
        "id": "k1-23-s71",
        "title": "Bebek ve Çocuk İzleminin Amaçları ve Koruyucu Stratejiler",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 71,
        "narrative": (
            "Bebek ve çocuk izlemleri, sağlam çocuk takibinin ve birinci basamak koruyucu hekimliğinin merkezidir: "
            "1. **Doğuştan Anomali ve Patolojilerin Tespiti:** Doğumsal kalp hastalıkları, inmemiş testis, "
            "yarık damak-dudak, kalça çıkığı ve metabolik hastalıkların kalıcı sekel bırakmadan erken saptanması. "
            "2. **Bebeklik ve Çocukluk Patolojilerine Yönelik Önlem:** Demir eksikliği anemisi, D vitamini yetersizliği (raşitizm), "
            "malnütrisyon veya obezitenin önlenmesi. "
            "3. **Rutin Aşılar:** Genişletilmiş Bağışıklama Programı (GBP) kapsamında aşıların eksiksiz uygulanması. "
            "4. **Büyüme ve Gelişmenin İzlenmesi:** Fiziksel büyüme (persentil eğrileri) ve nöromotor gelişim basamaklarının periyodik izlenmesi, "
            "beslenmenin düzenlenmesi ve anne sütünün teşvik edilmesi, annenin bebek bakımında eğitilerek desteklenmesi."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Bebek ve çocuk izlemlerinin en önemli koruyucu basamaklarından biri Genişletilmiş Bağışıklama Programı çerçevesinde rutin aşıların uygulanmasıdır.",
                "rutin aşıların",
                "Çocukluk çağı enfeksiyonlarından koruyan bağışıklama müdahaleleri"
            ),
            make_table(
                "Bebek ve Çocuk İzlemlerinin Temel Hedef Alanları",
                ["Hedef Alan", "Klinik Amaç", "Kritik Müdahale"],
                [
                    ["Konjenital Patolojiler", "Doğumsal anomali erken tespiti", "Fizik muayene, kalça USG, kırmızı refle testi"],
                    [
                        "Nütrisyonel Koruma",
                        {"text": "Raşitizm ve demir eksikliği profilaksisi", "isMasked": True, "hint": "Mikrobesin destekleri ve anemi önleme"},
                        "D vitamini ve profilaktik demir damlası"
                    ],
                    ["Bağışıklama", "Enfeksiyon hastalıklarını önleme", "GBP takvimine uygun rutin aşılar"],
                    ["Nörogelişimsel Takip", "Gelişimsel gerilik tespiti", "İlkel refleksler, kaba-ince motor basamaklar"]
                ]
            ),
            make_active_recall(
                "Bebek izleminde hekimin büyüme parametreleri dışında çocuğun fonksiyonel olgunlaşmasını izlemek için değerlendirdiği parametre grubuna ne ad verilir?",
                "Nöromotor ve psikososyal gelişim basamakları adı verilir.",
                "Fonksiyonel olgunlaşma ve kaba-ince motor basamaklar"
            )
        ]
    })

    # Slayt 72: Pediatrik Yaş Dönemleri ve Sağlık Riskleri
    slides.append({
        "id": "k1-23-s72",
        "title": "Pediatrik Yaş Dönemleri ve Karşılaşılan Sağlık Riskleri",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 72,
        "narrative": (
            "Çocukluk çağı, fizyolojik ve gelişimsel özelliklerine göre standart üç temel döneme ayrılır: "
            "1. **Neonatal (Yenidoğan) Dönem:** Doğumdan sonraki **ilk 4 haftayı (0 - 28 gün)** kapsar. "
            "Prematürite, doğum asfiksisi, neonatal sarılık, konjenital anomaliler ve sepsis en kritik mortalite riskleridir. "
            "2. **Bebeklik Dönemi:** Doğumdan **1 yaşın sonuna kadar (0 - 12 ay)** olan evredir. "
            "Enfeksiyonlar (pnömoni, ishal), beslenme yetersizlikleri, aşı aksamaları ve büyüme geriliği ön plandadır. "
            "3. **Okul Öncesi Çocukluk Dönemi:** **1 yaşından 6 yaşın sonuna kadar** olan süreci kapsar. "
            "Ev kazaları, zehirlenmeler, bulaşıcı döküntülü hastalıklar, parazitozlar, davranış ve konuşma sorunları sıklaşır. "
            "Çevre koşulları, sosyoekonomik düzey ve sağlık kuruluşunu kullanmada gecikme tüm dönemlerde ortak risk faktörleridir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Çocukluk yaş dönemlerinden neonatal dönem doğumdan sonraki ilk 4 haftayı kapsayan evredir.",
                "ilk 4 haftayı",
                "Yenidoğan evresinin gün ve hafta cinsinden süresi"
            ),
            make_table(
                "Pediatrik Yaş Dönemleri ve Klinik Risk Matrisi",
                ["Dönem Adı", "Kapsadığı Yaş Süresi", "En Yaygın Sağlık Riski", "İzlem Önceliği"],
                [
                    [
                        "Neonatal Dönem",
                        {"text": "İlk 4 hafta (0-28 gün)", "isMasked": True, "hint": "Doğum sonrası ilk bir aylık evre"},
                        "Asfiksi, sepsis, sarılık, GKD",
                        "Topuk kanı, kalça USG, işitme testi"
                    ],
                    ["Bebeklik Dönemi", "1 yaşa kadar (0-12 ay)", "Pnömoni, ishal, büyüme geriliği", "Anne sütü, ek gıda, rutin GBP aşıları"],
                    ["Okul Öncesi Dönem", "6 yaşa kadar (1-5 yaş)", "Ev kazaları, davranış sorunları, anemi", "Yıllık izlemler, diş muayenesi, gelişim testi"]
                ]
            ),
            make_micro_quiz(
                "Halk sağlığı ve pediatri sınıflamasına göre doğumdan sonraki ilk 28 günlük (4 haftalık) süreci tanımlayan yaş dönemi hangisidir?",
                {
                    "A": "Neonatal (Yenidoğan) Dönem",
                    "B": "Postneonatal Dönem",
                    "C": "Okul Öncesi Dönem",
                    "D": "Adölesan Dönem",
                    "E": "Toddler Dönemi"
                },
                "A",
                {
                    "A": "Neonatal dönem doğumdan sonraki ilk 28 günü (4 haftayı) kapsar.",
                    "B": "Postneonatal dönem 29. günden 1 yaşın sonuna kadar olan süredir.",
                    "C": "Okul öncesi dönem 1-6 yaş arasını ifade eder.",
                    "D": "Adölesan dönem 10-19 yaş aralığıdır.",
                    "E": "Toddler dönemi 1-3 yaş arası oyun çocuğu dönemidir."
                }
            )
        ]
    })

    # Slayt 73: Sağlık Bakanlığı Bebek İzlem Takvimi (0-1 Yaş)
    slides.append({
        "id": "k1-23-s73",
        "title": "Sağlık Bakanlığı Bebek İzlem Takvimi (0 - 1 Yaş)",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 73,
        "narrative": (
            "Sağlık Bakanlığı Çocuk ve Ergen Sağlığı Dairesi bebek izlem protokolü gereğince: "
            "1. **İlk İki İzlem:** Doğumun gerçekleştiği hastanede yapılır (1. izlem doğumda, 2. izlem taburcu olurken). "
            "2. **3. İzlem (İlk Hafta Kontrolü):** Doğumdan sonraki **ilk hafta içinde (tercihen 3. - 5. günlerde)** aile hekimi tarafından yapılır. "
            "Topuk kanı kontrolü, tartı kaybı (fizyolojik tartı kaybı <%10 olmalı) ve sarılık değerlendirilir. "
            "3. **Sonraki Bebek İzlemleri:** "
            "- **15. Gün İzlemi:** D vitamini profilaksisi (günde 400 IU) başlanır. "
            "- **1. Ay İzlemi:** Hepatit B 2. dozu, baş çevresi ve fiziksel büyüme değerlendirilir. "
            "- **2. Ay İzlemi:** KPA, KKK hazırlığı, 5'li karma aşı (DaBT-İPA-Hib) ve BCG aşısı uygulanır. "
            "- **3. Ay İzlemi:** Rutin gelişimsel muayene. "
            "- **4. Ay İzlemi:** Profilaktik demir desteği (1 mg/kg/gün) başlanır. "
            "- **6. Ay İzlemi:** Ek gıdaya geçiş danışmanlığı, OPA ve Hepatit B 3. dozu. "
            "- **9. Ay İzlemi:** Kaba motor gelişim ve anemi tespiti."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlık Bakanlığı bebek izlem takvimine göre birinci ve ikinci izlem doğumun yapıldığı sağlık kuruluşunda hastanede gerçekleştirilir.",
                "hastanede",
                "Yenidoğanın ilk iki izleminin yapıldığı resmi mekan"
            ),
            make_causal_chain(
                "Yenidoğan İlk Hafta İzlemi Patoloji Tespit Zinciri",
                [
                    "1. Doğum: Yenidoğanın doğum salonunda APGAR ve ilk muayenesinin tamamlanması",
                    "2. Taburculuk: Hastaneden ayrılmadan önce işitme testi ve ilk topuk kanının alınması",
                    "3. 3-5. Gün ASM Başvurusu: Aile hekiminde 3. izlem için tartı kontrolü ve sarılık taraması yapılması",
                    "4. Profilaksi Başlangıcı: 15. günde D vitamini desteği ile raşitizm gelişiminin önlenmesi"
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı Bebek İzlem Protokolü'ne göre bebeğin ilk iki izlemi nerede gerçekleştirilir?",
                {
                    "A": "Hastanede (doğumun gerçekleştiği kurumda)",
                    "B": "Toplum Sağlığı Merkezinde",
                    "C": "Yalnızca ev ziyaretinde",
                    "D": "Kreş ve gündüz bakımevinde",
                    "E": "İl Sağlık Müdürlüğü TSM laboratuvarında"
                },
                "A",
                {
                    "A": "Bebek izlemlerinin 1. ve 2. basamağı doğumun gerçekleştiği hastanede uygulanır.",
                    "B": "TSM doğrudan bireysel izlem birincil yeri değildir.",
                    "C": "Ev ziyareti lohusa/bebek risk durumlarında destekleyicidir.",
                    "D": "Bebeklikte kreş izlemi yoktur.",
                    "E": "Laboratuvar muayene yeri değildir."
                }
            )
        ]
    })

    # Slayt 74: Sağlık Bakanlığı Çocuk İzlem Takvimi (1 - 5 Yaş)
    slides.append({
        "id": "k1-23-s74",
        "title": "Sağlık Bakanlığı Çocuk İzlem Takvimi (1 - 5 Yaş)",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 74,
        "narrative": (
            "1 yaşını dolduran çocuklarda bebeklik izlemleri tamamlanarak çocuk izlem protokolüne geçilir: "
            "1. **İzlem Sıklığı:** Sağlık Bakanlığı takvimine göre 1 yaşından 5 yaşına kadar **toplam 7 izlem** yapılır. "
            "2. **İzlem Yaşları:** "
            "- **1 Yaş (12. Ay):** KKK, KPA pekiştirme ve suçiçeği aşıları, büyüme eğrileri, diş muayenesi. "
            "- **1.5 Yaş (18. Ay):** DaBT-İPA-Hib pekiştirme dozu, OPA, Hepatit A 1. dozu, otizm taraması (M-CHAT formu). "
            "- **2 Yaş (24. Ay):** Hepatit A 2. dozu, boy/kilo persentilleri, tuvalet eğitimi danışmanlığı. "
            "- **2.5 Yaş (30. Ay):** Nöromotor gelişim, konuşma ve kelime dağarcığı değerlendirmesi. "
            "- **3 Yaş (36. Ay):** Görme keskinliği taraması (Lea sembolleri veya E eşeli), kan basıncı ölçümü. "
            "- **4 Yaş (48. Ay):** Sosyal uyum, kaba-ince motor beceriler, işitme taraması. "
            "- **5 Yaş (60. Ay):** Okul olgunluğu değerlendirmesi, tam fizik muayene."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlık Bakanlığı takvimine göre bir yaş sonrası çocukluk döneminde bir, bir buçuk, iki, iki buçuk, üç, dört ve beş yaşlarında olmak üzere toplam 7 izlem yapılır.",
                "toplam 7 izlem",
                "1-5 yaş arasındaki standart çocuk kontrol sayısı"
            ),
            make_table(
                "Sağlık Bakanlığı 1-5 Yaş Çocuk İzlem Takvimi",
                ["İzlem Sırası", "Hedef Yaş", "Kritik Tarama / Aşı Müdahalesi"],
                [
                    ["1. Çocuk İzlemi", "12. Ay (1 Yaş)", "KKK, Suçiçeği aşıları ve tam büyüme persentili"],
                    ["2. Çocuk İzlemi", "18. Ay (1.5 Yaş)", "Hepatit A 1. doz ve M-CHAT otizm taraması"],
                    ["3. Çocuk İzlemi", "24. Ay (2 Yaş)", "Hepatit A 2. doz ve 20 süt dişi kontrolü"],
                    [
                        "4. Çocuk İzlemi",
                        {"text": "30. Ay (2.5 Yaş)", "isMasked": True, "hint": "İki buçuk yaş nörogelişim kontrolü"},
                        "Konuşma gelişimi ve iki kelimeli cümle takibi"
                    ],
                    ["5. Çocuk İzlemi", "36. Ay (3 Yaş)", "Görme taraması ve rutin tansiyon ölçümü"],
                    ["6. Çocuk İzlemi", "48. Ay (4 Yaş)", "İnce motor beceri ve sosyal uyum kontrolü"],
                    ["7. Çocuk İzlemi", "60. Ay (5 Yaş)", "Okul öncesi tam sistemik muayene"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı Çocuk İzlem Protokolü'ne göre 1 yaş ile 5 yaş (dahil) arasındaki süreçte bir çocuk için toplam kaç rutin izlem planlanmıştır?",
                {
                    "A": "7 izlem",
                    "B": "3 izlem",
                    "C": "5 izlem",
                    "D": "10 izlem",
                    "E": "12 izlem"
                },
                "A",
                {
                    "A": "1, 1.5, 2, 2.5, 3, 4 ve 5 yaşlarında olmak üzere toplam 7 izlem yapılır.",
                    "B": "3 izlem yetersizdir.",
                    "C": "5 izlem ara basamakları (1.5 ve 2.5 yaş) içermez.",
                    "D": "10 izlem bebeklik dönemi sıklığına benzerdir.",
                    "E": "12 izlem yetişkin aralığı değildir."
                }
            )
        ]
    })

    # Slayt 75: Yenidoğan İlk Ziyaret Muayenesi Kapsamı
    slides.append({
        "id": "k1-23-s75",
        "title": "Yenidoğan İlk Ziyaret Muayenesinin Kapsamı ve Organ Bulguları",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 75,
        "narrative": (
            "Doğum sonrası ilk ASM ziyaretinde bebeğin baştan ayağa ayrıntılı fizik muayenesi yapılır: "
            "1. **Deri:** Sarılık (ilk 24 saatte sarılık patolojiktir!), siyanoz, pletora, eritema toksikum, mongol lekeleri. "
            "2. **Fontaneller ve Baş:** Ön ve arka fontanel açıklığı, sefal hematom, kaput suksadeneum, kraniyosinostoz. "
            "3. **Gözler:** Subkonjonktival kanama, pürülan konjonktivit (klamidya/gonokok), katarakt taraması için **kırmızı refle testi**. "
            "4. **Ağız:** Yarık dudak ve damak muayenesi, pamukçuk (moniliazis), Epstein incileri. "
            "5. **Boyun:** Tortikollis (sternokleidomastoid hematomu), kistik higroma, klavikula kırığı palpasyonu. "
            "6. **Göbek:** Omfalit (kızarıklık, kötü koku, akıntı), göbek granülomu, umbilikal herni, kordonda 2 arter 1 ven varlığı. "
            "7. **Genital Organlar:** Erkekte inmemiş testis (kriptorşidizm), hidrosel, hipospadias; kızda yalancı menstrüasyon; ambigius genitalya."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan fizik muayenesinde konjenital katarakt ve retinoblastom gibi patolojileri ekarte etmek için oftalmoskopla kırmızı refle testi yapılır.",
                "kırmızı refle testi",
                "Göz tabanından pupilla yoluyla yansıyan ışık muayenesi"
            ),
            make_table(
                "Yenidoğan İlk Muayenesi Organ ve Alarm Bulguları Matrisi",
                ["Muayene Alanı", "Normal/Benign Bulgu", "Kritik Alarm Bulgusu"],
                [
                    ["Deri Rengi", "Mongol lekesi, hafif eritem", "İlk 24 saatte sarılık, santral siyanoz"],
                    [
                        "Kafa ve Fontaneller",
                        "Kaput suksadeneum (ödem)",
                        {"text": "Erken sütür kapanması (kraniyosinostoz) veya bombe fontanel", "isMasked": True, "hint": "KİBAS ve kafa deformitesi alarmı"}
                    ],
                    ["Göbek Kordonu", "Kuru, temiz kordon kütüğü", "Omfalit (eritem, pürülan akıntı, kötü koku)"],
                    ["Genital Sistem", "Geçici fizyolojik hidrosel", "İki taraflı palpe edilemeyen inmemiş testis"]
                ]
            ),
            make_active_recall(
                "Yenidoğanda doğum travmasına bağlı sternokleidomastoid kası içine kanama sonucu gelişen ve başın bir tarafa eğik durmasına yol açan klinik tablo nedir?",
                "Konjenital musküler tortikollis tablosudur.",
                "Sternokleidomastoid kas hematomu ve boyun eğriliği"
            )
        ]
    })

    # Slayt 76: Yenidoğan İlkel Refleksleri ve Nörolojik Değerlendirme
    slides.append({
        "id": "k1-23-s76",
        "title": "Yenidoğan İlkel Refleksleri ve Nörolojik Değerlendirme",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 76,
        "narrative": (
            "Yenidoğanın santral sinir sistemi ve periferik sinir bütünlüğü ilkel reflekslerle değerlendirilir: "
            "1. **Moro Refleksi:** Ani ses veya başın hafifçe geriye düşürülmesiyle bebeğin kollarını açması (abdüksiyon/ekstansiyon) "
            "ve ardından sarılma hareketi (addüksiyon/fleksiyon) yapmasıdır. 3-4. ayda kaybolur. "
            "**Asimetrik Moro:** Klavikula kırığı, brakiyal pleksus felci (Erb-Duchenne) veya tek taraflı beyin lezyonunu gösterir! "
            "2. **Yakalama (Grasp) Refleksi:** Avuç içine veya ayak tabanına dokunulduğunda parmakların sıkıca kapanmasıdır (palmar 3-4 ay, plantar 9-12 ay). "
            "3. **Emme ve Arama (Rooting) Refleksi:** Yanağa dokunulduğunda başın o yöne dönmesi ve memeyi aramasıdır; beslenmenin temelidir. "
            "4. **Asimetrik Tonik Boyun Refleksi (Eskrimci Duruşu):** Baş bir yöne çevrildiğinde o taraftaki ekstremitelerde ekstansiyon, "
            "karşı tarafta fleksiyon izlenir. "
            "5. **Adımlama ve Yakalama Refleksleri:** Dik tutulup ayak tabanı masaya değdirildiğinde yürüme adımları atmasıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan muayenesinde asimetrik Moro refleksi saptanması klavikula kırığı veya brakiyal pleksus hasarı olasılığını gösterir.",
                "asimetrik Moro",
                "Tek taraflı kol sıçrama ve kucaklama bozukluğu"
            ),
            make_table(
                "Yenidoğan İlkel Refleksleri ve Normal Kaybolma Zamanları",
                ["İlkel Refleks", "Uyarılma Şekli", "Normal Yanıt", "Fizyolojik Kaybolma"],
                [
                    [
                        "Moro Refleksi",
                        "Ani baş düşmesi veya gürültü",
                        "Kollarda simetrik açılma ve sarılma",
                        {"text": "3 - 4. ayda kaybolur", "isMasked": True, "hint": "Dördüncü ay civarı istemli harekete geçiş"}
                    ],
                    ["Palmar Yakalama", "Avuç içine parmak sokulması", "Parmakların güçlü kapanması", "3 - 4. ayda kaybolur"],
                    ["Arama (Rooting)", "Yanak köşesine temas", "Başın temas yönüne dönmesi", "3 - 4. ayda kaybolur"],
                    ["Plantar Yakalama", "Ayak tabanına bası", "Ayak parmaklarının fleksiyonu", "9 - 12. ayda kaybolur"]
                ]
            ),
            make_micro_quiz(
                "Zor bir doğum sonrası muayene edilen term yenidoğanda sağ kolun gövde yanında gevşek durduğu ve Moro refleksi sırasında sağ kolda hareket izlenmediği (asimetrik yanıt) görülmüştür. En olası ön tanı hangisidir?",
                {
                    "A": "Brakiyal pleksus zedelenmesi veya klavikula kırığı",
                    "B": "Konjenital kalça displazisi",
                    "C": "Fizyolojik hiperbilirubinemi",
                    "D": "Epstein incisi varlığı",
                    "E": "Umbilikal granülom"
                },
                "A",
                {
                    "A": "Asimetrik Moro refleksi en sık brakiyal pleksus yaralanması veya klavikula fraktürüne işaret eder.",
                    "B": "Kalça displazisi alt ekstremite testleriyle (Ortolani/Barlow) saptanır.",
                    "C": "Sarılık kolda asimetrik kuvvetsizlik yapmaz.",
                    "D": "Epstein incisi damakta benign kisttir.",
                    "E": "Umbilikal granülom göbek kordonu lezyonudur."
                }
            )
        ]
    })

    # Slayt 77: Gelişimsel Kalça Displazisi (GKD) Taraması
    slides.append({
        "id": "k1-23-s77",
        "title": "Gelişimsel Kalça Displazisi (GKD): Klinik Testler ve Tarama",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 77,
        "narrative": (
            "Gelişimsel Kalça Displazisi (GKD), erken teşhis edilmezse kalıcı yürüme bozukluğu ve sakatlığa yol açan kritik bir patolojidir: "
            "1. **Risk Faktörleri:** Kız cinsiyet (kadınlarda 6 kat sık), makat doğum prezantasyonu, "
            "pozitif aile öyküsü, oligohidramnios ve kundaklama (kalçayı ekstansiyon ve addüksiyona zorlayan en tehlikeli geleneksel uygulama!). "
            "2. **Fizik Muayene Testleri:** "
            "- **Ortolani Manevrası:** Çıkık olan femur başını asetabuluma geri sokma (redüksiyon) testidir. Kalça 90 derece fleksiyondayken abdüksiyona getirilirken ele hissedilen 'klik/klunk' sesi pozitiftir. "
            "- **Barlow Manevrası:** Asetabulumdaki gevşek femur başını dışarı çıkarma (dislokasyon) testidir. Addüksiyonda arkaya itilerek disloke edilir. "
            "- **Pili Asimetrisi ve Galeazzi Belirtisi:** Uyluk kıvrımlarının asimetrisi ve diz yükseklik farkı. "
            "3. **Altın Standart Tarama:** Sağlık Bakanlığı protokolüne göre tüm bebeklere **4. - 6. haftalarda Kalça Ultrasonografisi (USG)** yapılır. "
            "6 aydan önce kemikleşme tamamlanmadığından direkt grafi yerine USG kullanılır (Graf yöntemi)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gelişimsel kalça displazisinde disloke olmuş femur başının kalça abdüksiyona getirilirken asetabulum içine girmesi Ortolani manevrası ile test edilir.",
                "Ortolani manevrası",
                "Çıkık kalçayı redükte eden ve klik hissi veren klinik manevra"
            ),
            make_table(
                "Gelişimsel Kalça Displazisi Klinik Test ve Tanı Protokolü",
                ["Klinik Yöntem", "Uygulama Tekniği", "Pozitif Bulgusu", "Tanısal Değeri"],
                [
                    ["Ortolani Testi", "Fleksiyondaki uyluğu abdüksiyona alma", "Femur başının asetabuluma oturma 'klunk' hissi", "Çıkık kalçanın redüksiyonu"],
                    [
                        "Barlow Testi",
                        "Uyluğu addüksiyona alıp arkaya itme",
                        {"text": "Femur başının asetabulumdan dışarı kayması", "isMasked": True, "hint": "Labil/gevşek kalçanın disloke edilmesi"},
                        "Kalça instabilitesini saptama"
                    ],
                    ["Pili Asimetrisi", "Uyluk iç yüz kıvrımlarını karşılaştırma", "Kıvrım sayısı ve seviyesinde uyumsuzluk", "Şüphe uyandırıcı yardımcı bulgu"],
                    ["Kalça USG (Graf)", "4-6. haftalarda dinamik ultrasonografi", "Alfa açısı <60 derece (displazi)", "0-6 ay arası altın standart"]
                ]
            ),
            make_micro_quiz(
                "Gelişimsel Kalça Displazisi (GKD) açısından ülkemizde tüm bebeklere birinci basamak sağlık kuruluşlarında tarama amacıyla önerilen en uygun görüntüleme yöntemi ve zamanı hangisidir?",
                {
                    "A": "4 - 6. haftalarda Kalça Ultrasonografisi",
                    "B": "Doğumun ilk 24 saatinde Manyetik Rezonans (MR)",
                    "C": "1. haftada direkt Pelvis Grafisi",
                    "D": "12. ayda Bilgisayarlı Tomografi (BT)",
                    "E": "5. yaşta Kemik Sintigrafisi"
                },
                "A",
                {
                    "A": "İlk 6 ayda femur başı kıkırdak yapıda olduğundan 4-6. haftalarda Kalça USG altın standart taramadır.",
                    "B": "MR pahalıdır ve rutin taramada yeri yoktur.",
                    "C": "İlk aylarda kıkırdak femur başı röntgende görünmez.",
                    "D": "BT yüksek radyasyon içerir, taramada kullanılmaz.",
                    "E": "Sintigrafi GKD tarama yöntemi değildir."
                }
            )
        ]
    })

    # Slayt 78: Yenidoğan Taramaları: Topuk Kanı ve İşitme/Görme Programları
    slides.append({
        "id": "k1-23-s78",
        "title": "Ulusal Yenidoğan Tarama Programları: Topuk Kanı ve Duyusal Taramalar",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 78,
        "narrative": (
            "Sağlık Bakanlığı Ulusal Yenidoğan Tarama Programı, semptomsuz evrede tanı koyarak ağır zeka geriliğini ve ölümleri önler: "
            "1. **Topuk Kanı Taraması (Guthrie Kartı):** Bebek anne sütü veya mama ile beslenmeye başladıktan sonra (en az 48 saat beslenme sonrası) "
            "özel filtre kağıdına topuktan kılcal kan damlatılır. Taranan 6 hastalık şunlardır: "
            "- **Fenilketonüri (FKÜ):** Fenilalanin hidroksilaz eksikliği; tedavi edilmezse derin mental retardasyon yapar. "
            "- **Konjenital Hipotiroidi (KH):** TSH ölçümü yapılır; kretinizmi önler, erken L-tiroksin başlanır. "
            "- **Biyotinidaz Eksikliği:** Enzim aktivitesi taranır; saç dökülmesi, konvülsiyon ve işitme kaybını önler. "
            "- **Kistik Fibrozis (KF):** İmmünreaktif Tripsinojen (IRT) seviyesi taranır. "
            "- **Konjenital Adrenal Hiperplazi (KAH):** 17-OH-progesteron taranır; tuz kaybı krizini önler. "
            "- **Spinal Muskuler Atrofi (SMA):** SMN1 gen delesyonu taranır; erken gen tedavisini sağlar. "
            "2. **İşitme Taraması:** Taburcu olmadan önce OAE (Otoakustik Emisyon) veya BERA (ABR) ile taranır. "
            "3. **Görme Taraması:** Oftalmoskop ile Kırmızı Refle testi yapılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan topuk kanı taramasında fenilketonüri tanısının doğru konabilmesi için kan örneğinin bebek en az 48 saat beslendikten sonra alınması gerekir.",
                "en az 48 saat beslendikten sonra",
                "Metabolitin kanda yükselebilmesi için gereken minimum enteral beslenme süresi"
            ),
            make_table(
                "Ulusal Yenidoğan Topuk Kanı Tarama Paneli ve Önlenen Klinik Tablo",
                ["Hastalık Adı", "Tarama Biyobelirteci", "Önlenen Kritik Klinik Tablo"],
                [
                    ["Fenilketonüri (FKÜ)", "Kanda fenilalanin düzeyi", "Ağır ve geri dönüşsüz zeka geriliği (mental retardasyon)"],
                    [
                        "Konjenital Hipotiroidi",
                        {"text": "Serum TSH seviyesi", "isMasked": True, "hint": "Tiroid stimülan hormon yüksekliği"},
                        "Kretinizm, cücelik ve nörogelişimsel gerilik"
                    ],
                    ["Biyotinidaz Eksikliği", "Biyotinidaz enzim aktivitesi", "Nörolojik nöbetler, koma ve saç dökülmesi"],
                    ["Kistik Fibrozis", "İmmünreaktif tripsinojen (IRT)", "Mekonyum ileusu, kronik akciğer hasarı, malnütrisyon"],
                    ["Konjenital Adrenal Hiperplazi", "17-alfa-OH-progesteron", "Akut adrenal kriz, tuz kaybı ve neonatal şok"],
                    ["SMA", "SMN1 gen delesyon analizi", "Progresif spinal motor nöron kaybı ve respiratuar yetmezlik"]
                ]
            ),
            make_micro_quiz(
                "Yenidoğan topuk kanı taramasında fenilketonüri testinin yalancı negatif çıkmasını önlemek için en önemli uygulama kuralı hangisidir?",
                {
                    "A": "Bebeğin en az 48 saat protein içeren besinle (anne sütü/mama) beslenmiş olması",
                    "B": "Kan örneğinin yalnızca kord kanından alınması",
                    "C": "Örneğin doğumun ilk 10 dakikasında alınması",
                    "D": "Bebeğe test öncesi K vitamini verilmemiş olması",
                    "E": "Örneğin sadece santral venöz kateterden çekilmesi"
                },
                "A",
                {
                    "A": "Fenilalanin proteinle alındığından bebeğin en az 48 saat enteral beslenmiş olması şarttır.",
                    "B": "Kord kanı FKÜ taraması için uygun değildir.",
                    "C": "İlk 10 dakikada kanda fenilalanin birikmez, test yalancı negatif çıkar.",
                    "D": "K vitamini FKÜ sonucunu etkilemez.",
                    "E": "Tarama topuktan kılcal kanla özel filtre kağıdına damlatılarak yapılır."
                }
            )
        ]
    })

    # Slayt 79: [TEKRAR SAYFASI - CHECKPOINT 8] Bebek ve Çocuk İzlem Protokolü ve Yenidoğan Muayenesi
    slides.append({
        "id": "k1-23-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Bebek ve Çocuk İzlem Protokolü ve Yenidoğan Muayenesi",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 79,
        "narrative": (
            "Bu sekizinci checkpoint sayfasında, bebek ve çocuk izlem ilkelerini ve tarama algoritmalarını pekiştiriyoruz: "
            "1. **Yaş Dönemleri:** Neonatal dönem ilk 4 hafta (0-28 gün), Bebeklik 0-12 ay, Okul öncesi 1-6 yaştır. "
            "2. **Bebek İzlem Takvimi:** 1. ve 2. izlem hastanede, 3. izlem ilk hafta içinde ASM'de yapılır (ardından 15. gün, 1, 2, 3, 4, 6, 9. aylar). "
            "3. **Çocuk İzlem Takvimi:** 1 yaşından sonra 1, 1.5, 2, 2.5, 3, 4 ve 5 yaşlarında olmak üzere TOPLAM 7 İZLEM yapılır. "
            "4. **İlkel Refleksler:** Moro, yakalama, rooting 3-4. aylarda geriler. Asimetrik Moro klavikula kırığı veya brakiyal pleksus hasarı alarmıdır. "
            "5. **Gelişimsel Kalça Displazisi:** Ortolani (redüksiyon) ve Barlow (dislokasyon) testleri yapılır; 4-6. haftada Kalça USG altın standarttır. "
            "6. **Topuk Kanı (Guthrie):** En az 48 saatlik beslenme sonrası alınır; FKÜ, Konjenital Hipotiroidi, Biyotinidaz, Kistik Fibrozis, KAH ve SMA taranır. "
            "7. **Duyusal Taramalar:** OAE/BERA ile işitme, Kırmızı Refle testi ile konjenital katarakt taranır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s79-1",
                "Sağlık Bakanlığı protokolüne göre 1-5 yaş arası çocukluk döneminde planlanan toplam periyodik izlem sayısı kaçtır?",
                "Tam yedi kez sağlık kontrolü gerçekleştirilir.",
                "İlk çocukluk ve okul öncesi senelerindeki rutin vizit adedi",
                "Çocuk İzlem Takvimi"
            ),
            make_flashcard(
                "k1-23-fc-s79-2",
                "Gelişimsel kalça displazisinde femurun asetabulum içine redükte edilerek klik sesinin alındığı muayene manevrası hangisidir?",
                "Ortolani manevrasıdır.",
                "Kalçanın abdüksiyona ve öne doğru nazikçe itilmesi testi",
                "Yenidoğan Kalça Taraması"
            ),
            make_flashcard(
                "k1-23-fc-s79-3",
                "Sağlık Bakanlığı yenidoğan topuk kanı (Guthrie kartı) ulusal tarama programında taranan hastalıklardan biri hangisidir?",
                "Fenilketonüri metabolik bozukluğudur.",
                "Zeka geriliğini önlemek için doğumdan sonra beslenme başlanınca bakılan enzim eksikliği",
                "Ulusal Yenidoğan Taramaları"
            )
        ],
        "interactiveElements": [
            make_table(
                "Bebek ve Çocuk İzleminde Kritik Yaş Dönemleri ve Müdahaleler",
                ["Yaş Evresi", "Zaman Aralığı", "Rutin İzlem Sayısı", "Kritik Koruyucu Müdahale"],
                [
                    ["Neonatal Dönem", "0 - 28 Gün", "3 izlem (Doğum, Taburculuk, İlk Hafta)", "Topuk kanı, işitme testi, sarılık kontrolü"],
                    ["Süt Çocukluğu", "1 - 12 Ay", "6 izlem (15. gün, 1, 2, 3, 4, 6, 9. ay)", "Kalça USG, D vitamini, demir, GBP aşıları"],
                    ["Oyun ve Okul Öncesi", "1 - 5 Yaş", "Toplam 7 izlem (1, 1.5, 2, 2.5, 3, 4, 5 yaş)", "Otizm taraması, görme taraması, diş gelişimi"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı çocuk izlem takvimine göre 18. ay (1.5 yaş) izleminde ulusal protokol gereğince nöropsikiyatrik gelişim açısından mutlaka uygulanması gereken tarama anketi hangisidir?",
                {
                    "A": "M-CHAT (Otizm Erken Tarama Formu)",
                    "B": "Mini Mental Durum Muayenesi (MMSE)",
                    "C": "Beck Depresyon Ölçeği",
                    "D": "APGAR Skorlama Çizelgesi",
                    "E": "Glasgow Koma Skalası (GKS)"
                },
                "A",
                {
                    "A": "M-CHAT formu 18-24. aylarda yaygın gelişimsel bozukluk ve otizm erken teşhisi için rutin uygulanır.",
                    "B": "MMSE yaşlılarda demans taramasıdır.",
                    "C": "Beck depresyon ölçeği ergen/erişkin psikiyatri testidir.",
                    "D": "APGAR doğumun ilk dakikalarında kullanılır.",
                    "E": "Glasgow bilinci kapalı travma hastalarında kullanılır."
                }
            )
        ]
    })

    # Slayt 80: Bölüm Özeti: Muayene İlkelerinden Fiziksel Büyüme Parametrelerine Geçiş
    slides.append({
        "id": "k1-23-s80",
        "title": "Bölüm Özeti: Muayene İlkelerinden Fiziksel Büyüme Parametrelerine Geçiş",
        "section": "Bebek ve Çocuk İzleminin Temel İlkeleri ve İzlem Takvimi",
        "slideNumber": 80,
        "narrative": (
            "Bebek ve çocuk izlem protokolünün sekizinci bölümünü tamamlarken klinik hekimlik kazanımlarını özetliyoruz: "
            "1. **Bütüncül İzlem Yaklaşımı:** Çocuk hekimliği yalnızca hastalıkları tedavi etmek değil, büyüme-gelişmeyi takip ederek patolojileri önlemektir. "
            "2. **Zamanlama Hayatidir:** Topuk kanının 48 saatlik beslenme sonrası alınması yalancı negatifliği önler; kalça USG'sinin 4-6. haftalarda yapılması "
            "cerrahiye gerek kalmadan basit bandajla (Pavlik bandajı) tedavi şansı sunar. "
            "3. **Reflekslerin Kayboluşu Nörolojik Olgunlaşmadır:** Moro ve yakalama reflekslerinin 4. aydan sonra devam etmesi serebral palsi gibi "
            "üst motor nöron patolojilerini düşündürür. "
            "4. **Sonraki Bölüme Köprü:** Bir sonraki bölümde çocuğun fiziksel büyüme göstergeleri olan kilo alma hızı, boy uzaması, "
            "baş ve göğüs çevresi dinamikleri ile fontanel ve diş gelişimini inceleyeceğiz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan döneminde görülen Moro refleksinin dördüncü aydan sonra kaybolmayıp devam etmesi serebral palsi gibi nörolojik patolojilerin alarm bulgusudur.",
                "serebral palsi",
                "İlkel refleksin kalıcı olmasına yol açan üst motor nöron beyin hasarı tablosu"
            ),
            make_active_recall(
                "Yenidoğan muayenesinde kalça instabilitesi saptanan bir bebekte 4-6. haftada USG ile GKD tanısı konduğunda erken dönemde cerrahisiz uygulanan en yaygın ortopedik cihaz nedir?",
                "Pavlik bandajı (dinamik fleksiyon-abdüksiyon ortezi) uygulanır.",
                "Kalçayı fleksiyonda ve açık tutan dinamik askı cihazı"
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi bebek ve çocuk izlemlerinde birinci basamak hekiminin acil sevk etmesini gerektiren kırmızı bayrak (alarm) bulgularından biri değildir?",
                {
                    "A": "İlk 24 saat içinde belirginleşen cilt sarılığı",
                    "B": "Yenidoğanda doğumdan 3 gün sonra görülen hafif fizyolojik kilo kaybı (%5)",
                    "C": "Moro refleksinin tek kolda hiç alınamaması (asimetri)",
                    "D": "Dizler bükülüyken diz yüksekliklerinin belirgin farklı olması (Galeazzi pozitifliği)",
                    "E": "Ön fontanelin dışa doğru belirgin şekilde kabarması ve bombeleşmesi"
                },
                "B",
                {
                    "A": "İlk 24 saatteki sarılık patolojiktir, acil tetkik gerekir.",
                    "B": "Yenidoğanda ilk günlerde %5-10'a kadar tartı kaybı tamamen fizyolojiktir, alarm bulgusu değildir.",
                    "C": "Asimetrik Moro brakiyal pleksus hasarı veya klavikula kırığı belirtisidir.",
                    "D": "Galeazzi pozitifliği tek taraflı kalça çıkığı göstergesidir.",
                    "E": "Bombe fontanel menenjit veya KİBAS acil alarmıdır."
                }
            )
        ]
    })

    return slides
