# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 4: Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem (Slayt 31 - 40)
Checkpoint 4: Slayt 39
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # Slayt 31: Sağlık Bakanlığı 4 Kademeli Gebe İzlem Takvimi ve Aralıkları
    slides.append({
        "id": "k1-23-s31",
        "title": "Sağlık Bakanlığı 4 Kademeli Gebe İzlem Takvimi ve Aralıkları",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 31,
        "narrative": (
            "Sağlık Bakanlığı Doğum Öncesi Bakım Yönetim Rehberi'ne göre, herhangi bir komplikasyonu bulunmayan "
            "tüm sağlıklı gebelerin aile hekimliği birimlerinde **en az 4 kez** periyodik izlemden geçmesi zorunludur. "
            "Bu 4 izlemin haftalık dağılımı maternal ve fetal fizyolojinin en kritik dönüm noktalarına göre standardize edilmiştir: "
            "1. **1. İzlem:** Gebeliğin **0-14. haftaları arasında** (ideal olarak ilk trimesterde, ilk geciken adetten hemen sonra). "
            "2. **2. İzlem:** Gebeliğin **18-24. haftaları arasında** (ikinci trimester fetal büyüme ve organogenez kontrolü). "
            "3. **3. İzlem:** Gebeliğin **28-32. haftaları arasında** (üçüncü trimester başı, preeklampsi ve erken doğum takibi). "
            "4. **4. İzlem:** Gebeliğin **36-38. haftaları arasında** (terme yaklaşırken doğum şekli ve acil eylem planlaması). "
            "Bu haftalar dışında gebe her şüpheli durumda hekime başvurabilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlık Bakanlığı gebe izlem takvimine göre birinci izlem 0-14. haftalarda, ikinci izlem ise 18-24. haftalarda yapılır.",
                "18-24. haftalarda",
                "İkinci trimester fetal büyüme ve FKS izlem aralığı"
            ),
            make_table(
                "Sağlık Bakanlığı 4 Aşamalı Gebe İzlem Takvimi",
                ["İzlem Sırası", "Önerilen Gebelik Haftası", "Trimester Karşılığı", "Temel Klinik Odak"],
                [
                    ["1. İzlem", "0 - 14. Hafta", "1. Trimester", "Ayrıntılı öykü, bazal tansiyon, kan grubu, HBsAg ve idrar"],
                    [
                        "2. İzlem",
                        {"text": "18 - 24. Hafta", "isMasked": True, "hint": "İkinci trimester organogenez ve FKS kontrolü"},
                        "2. Trimester",
                        "Fetal kalp sesi, indirekt Coombs, fundus yüksekliği"
                    ],
                    ["3. İzlem", "28 - 32. Hafta", "3. Trimester Başı", "Preeklampsi kontrolü, doğum yeri planlama ve emzirme eğitimi"],
                    ["4. İzlem", "36 - 38. Hafta", "Term Öncesi", "Leopold manevraları, prezantasyon ve doğum eylemi hazırlığı"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı Doğum Öncesi Bakım Yönetim Rehberi'ne göre 'İkinci Gebe İzlemi' hangi gebelik haftaları arasında yapılmalıdır?",
                {
                    "A": "0 - 8. hafta",
                    "B": "10 - 14. hafta",
                    "C": "18 - 24. hafta",
                    "D": "28 - 32. hafta",
                    "E": "38 - 40. hafta"
                },
                "C",
                {
                    "A": "Yanlıştır; Erken birinci izlem evresidir.",
                    "B": "Yanlıştır; 1. izlemin sonudur.",
                    "C": "Doğrudur; 2. gebe izlemi 18-24. haftalar arasında gerçekleştirilir.",
                    "D": "Yanlıştır; 3. izlem aralığıdır.",
                    "E": "Yanlıştır; Term doğum anıdır."
                }
            )
        ]
    })

    # Slayt 32: 1. Gebe İzlemi (0-14. Hafta): Ayrıntılı Öykü ve Risk Tespiti
    slides.append({
        "id": "k1-23-s32",
        "title": "1. Gebe İzlemi (0-14. Hafta): Ayrıntılı Öykü ve Risk Tespiti",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 32,
        "narrative": (
            "1. Gebe İzlemi, tüm gebelik sürecinin temel taşıdır ve hekimin gebeye **en az 30 dakika** zaman ayırmasını gerektirir. "
            "Bu vizitin en kritik bileşeni **kapsamlı tıbbi öykü (anamnez)** ve **Risk Değerlendirme Formu'nun** eksiksiz doldurulmasıdır: "
            "1. **Kişisel ve Sosyal Bilgiler:** Yaş (<18 veya >35 risk), akraba evliliği, eğitim düzeyi, ekonomik durum, çalışma şartları. "
            "2. **Tıbbi ve Cerrahi Öykü:** Diyabet, esansiyel hipertansiyon, böbrek yetmezliği, kalp hastalığı, tüberküloz, "
            "kullanılan düzenli ilaçlar (teratojenik ajanlar), geçirilmiş pelvik ameliyatlar. "
            "3. **Obstetrik Öykü:** Önceki gebelik sayısı (gravida), doğum sayısı (parite), yaşayan çocuk, düşük (abortus), "
            "kürtaj, ölü doğum, sezaryen öyküsü, önceki gebeliklerde preeklampsi veya postpartum kanama hikayesi. "
            "4. **Mevcut Gebelik:** Son adet tarihi (SAT), gebelik planlı mı, vajinal kanama veya şiddetli bulantı-kusma var mı."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Birinci gebe izleminde hekimin hastaya en az otuz dakika zaman ayırarak ayrıntılı öykü alması ve risk değerlendirmesi yapması gerekir.",
                "en az otuz dakika",
                "İlk vizitte kapsamlı anamnez için gereken minimum muayene süresi"
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı 1. Gebe İzlemi protokolünde ayrıntılı öykü alınırken hekimin sorgulaması gereken öncelikli obstetrik risk faktörleri arasında hangisi yer almaz?",
                {
                    "A": "Önceki gebeliklerde geçirilmiş preeklampsi veya eklampsi öyküsü",
                    "B": "Daha önce ölü doğum veya tekrarlayan düşük öyküsü",
                    "C": "Gebenin önceki doğumlarında masif postpartum kanama geçmişi",
                    "D": "Gebenin çocukluk çağında suçiçeği aşısı olup olmadığı yerine saç boyatma sıklığı",
                    "E": "Önceki doğumun sezaryenle yapılmış olması ve aradan geçen süre"
                },
                "D",
                {
                    "A": "Sorgulanır; Tekrarlama riski çok yüksektir.",
                    "B": "Sorgulanır; Trombofili veya genetik anomali riski taşır.",
                    "C": "Sorgulanır; Atoni tekrarlayabilir.",
                    "D": "Tıbbi Önceliği Yoktur; Saç boyatma tıbbi obstetrik risk formu parametresi değildir.",
                    "E": "Sorgulanır; Uterus rüptürü ve plasenta invazyon anomalisi riskini belirler."
                }
            ),
            make_active_recall(
                "1. Gebe İzleminde gebelik haftasının ve tahmini doğum tarihinin doğru hesaplanabilmesi için hastadan öğrenilmesi gereken temel tarih nedir?",
                "Son Adet Tarihinin (SAT) ilk günüdür.",
                "Gestasyonel yaş hesaplamasının başlangıç takvimi"
            )
        ]
    })

    # Slayt 33: 1. İzlem Fizik Muayenesi: Boy, Kilo, Bazal Kan Basıncı ve Pelvis
    slides.append({
        "id": "k1-23-s33",
        "title": "1. İzlem Fizik Muayenesi: Boy, Kilo, Bazal Kan Basıncı ve Pelvis",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 33,
        "narrative": (
            "1. Gebe İzleminde yapılan fizik muayene, tüm gebelik boyunca kullanılacak **'bazal referans değerleri'** belirler: "
            "1. **Boy ve Kilo Ölçümü:** Gebelik öncesi Beden Kitle İndeksi (BKİ) hesaplanır. "
            "Boyun 150 cm'nin altında olması dar pelvis ve distosi (zor doğum) açısından risk faktörüdür. "
            "BKİ'ye göre gebelik boyunca alınması gereken ideal kilo belirlenir. "
            "2. **Bazal Kan Basıncı:** Mutlaka doğru manşonla ve dinlenmişken ölçülür. "
            "İlk trimesterde tansiyonun normal veya düşük olması beklenir (progesteronun vazodilatör etkisi). "
            "İlk vizitte ölçülen bazal tansiyon, 20. haftadan sonra gelişebilecek preeklampsinin tanısında referanstır. "
            "3. **Sistemik Muayene:** Kalp oskültasyonu (üfürüm varlığı), solunum sesleri, tiroid bezi, meme muayenesi. "
            "4. **Anemi ve Ödem:** Konjonktiva ve tırnak yatağı solukluğu; pretibial ödem kontrolü."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "İlk gebe izleminde ölçülen bazal kan basıncı gebeliğin ilerleyen haftalarında preeklampsi gelişimini ayırt etmede referans oluşturur.",
                "preeklampsi gelişimini",
                "20. haftadan sonra tansiyon yükselmesiyle beliren toksemi tablosu"
            ),
            make_before_after(
                "Kan Basıncı Değerlendirmesi: Normal Gebelik vs Preeklampsi Başlangıcı",
                "Fizyolojik İlk Trimester",
                "Progesteronun düz kas gevşetici etkisiyle periferik vasküler direnç düşer; tansiyon hafif azalır (ör. 100/60 mmHg).",
                "Preeklamptik Değişim (20. Hafta Sonrası)",
                "Plasental iskemiye bağlı sistemik vazokonstrüksiyon gelişir; kan basıncı 140/90 mmHg üzerine fırlar ve proteinüri eklenir.",
                "Gebelikte tansiyon dinamiklerinin karşılaştırılması"
            ),
            make_active_recall(
                "Gebe muayenesinde boy ölçümünün kaç santimetrenin altında olması kemik pelvis darlığı ve mekanik doğum engeli açısından yüksek risk göstergesidir?",
                "Boyun 150 cm'nin altında olması dar pelvis riski taşır.",
                "Kısa boy ve mekanik distosi risk sınırı"
            )
        ]
    })

    # Slayt 34: 1. İzlem Laboratuvar Testleri: İdrar, Kan Grubu, Hb-Hct ve HBsAg
    slides.append({
        "id": "k1-23-s34",
        "title": "1. İzlem Laboratuvar Testleri: İdrar, Kan Grubu, Hb-Hct ve HBsAg",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 34,
        "narrative": (
            "1. Gebe İzleminde yapılması Sağlık Bakanlığı tarafından zorunlu kılınan **dört temel laboratuvar incelemesi** vardır: "
            "1. **Tam İdrar Tahlili (ve İdrar Kültürü):** Asemptomatik bakteriüri taraması hayati önem taşır; gebelikte tedavi edilmeyen "
            "bakteriüri %30-40 oranında akut piyelonefrite ve erken doğuma döner. Ayrıca bazal proteinüri olup olmadığı kontrol edilir. "
            "2. **Kan Grubu ve Rh Faktörü:** Anne ve babanın Rh uygunsuzluğu (Anne Rh-, Baba Rh+) riski ilk vizitte belgelenmelidir. "
            "3. **Hemoglobin ve Hematokrit (Hb-Hct):** Anemi taraması yapılır. Gebelikte Hb < 11 g/dl anemi kabul edilir; "
            "Hb < 7 g/dl ise acil sevk gerektiren ağır anemidir. "
            "4. **HBsAg (Hepatit B Yüzey Antijeni):** Perinatal Hepatit B geçişini önlemek için her gebeye taranır. "
            "HBsAg pozitif anneden doğan bebeğe doğumdan sonraki ilk 12 saatte Hepatit B aşısıyla beraber **Hepatit B İmmünglobulini (HBIG)** yapılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Birinci izlemde her gebeye rutin HBsAg taranarak pozitif annelerin bebeklerine doğumda hepatit B aşısı ve immünglobulin uygulanır.",
                "hepatit B aşısı ve immünglobulin",
                "Vertikal hepatit bulaşını engelleyen kombine koruyucu tedavi"
            ),
            make_table(
                "1. Gebe İzleminde Zorunlu Laboratuvar Taramaları ve Amaçları",
                ["Laboratuvar Testi", "Taranan Patoloji", "Pozitiflik Durumunda Yapılacak Acil Müdahale"],
                [
                    ["Tam İdrar / Kültür", "Asemptomatik Bakteriüri ve Proteinüri", "Gebelikte güvenli antibiyotik tedavisi ve piyelonefrit önleme"],
                    [
                        "Kan Grubu ve Rh Faktörü",
                        "Rh Uyuşmazlığı (Anne Rh-, Baba Rh+)",
                        {"text": "İndirekt Coombs testi planlaması", "isMasked": True, "hint": "Eritrosit antikorlarını saptayan laboratuvar testi"}
                    ],
                    ["Tam Kan Sayımı (Hb-Hct)", "Gebelikte Anemi (Hb < 11 g/dl)", "Demir tedavisi veya derin anemide (Hb<7) sevk"],
                    ["HBsAg Taraması", "Maternal Hepatit B Taşıyıcılığı", "Doğumda bebeğe ilk 12 saatte aşı + HBIG koruması"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı 1. Gebe İzlemi protokolüne göre her gebeye rutin olarak yapılması gereken tarama testleri arasında hangisi YER ALMAZ?",
                {
                    "A": "Tam idrar tahlili (proteinüri ve bakteriüri kontrolü)",
                    "B": "Kan grubu ve Rh faktörü tayini",
                    "C": "Hepatit B yüzey antijeni (HBsAg) testi",
                    "D": "Hemoglobin ve hematokrit ölçümü",
                    "E": "Tüm gebelere rutin lomber ponksiyon ile beyin omurilik sıvısı incelemesi"
                },
                "E",
                {
                    "A": "Rutin testtir; Piyelonefriti önler.",
                    "B": "Rutin testtir; İzoimmünizasyon için şarttır.",
                    "C": "Rutin testtir; Perinatal bulaşı önler.",
                    "D": "Rutin testtir; Anemi tespitidir.",
                    "E": "Kesinlikle Rutin Değildir; Lomber ponksiyon invaziv nörolojik girişimdir, rutin izlemde yeri yoktur."
                }
            )
        ]
    })

    # Slayt 35: Fetal Kalp Sesleri (FKS): Yöntemler, Eşikler ve Normal Hız (120-160)
    slides.append({
        "id": "k1-23-s35",
        "title": "Fetal Kalp Sesleri (FKS): Yöntemler, Eşikler ve Normal Hız (120-160)",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 35,
        "narrative": (
            "Fetal Kalp Seslerinin (FKS) duyulması, intrauterin fetal canlılığın en dolaysız ve sevindirici kanıtıdır. "
            "FKS dinleme yöntemleri ve klinik eşikleri şunlardır: "
            "1. **El Doppleri (Ultrasonik Akım Cihazı):** Gebeliğin **10-12. haftalarından itibaren** fetal kalp atımları net olarak duyulabilir. "
            "2. **Fetoskop / Pinard Steteskopu:** Akustik dinleme konisiyle FKS ancak gebeliğin **16-20. haftalarından itibaren** duyulabilir "
            "(anne karın duvarı kalınlığına göre değişir). "
            "3. **Normal FKS Hızı:** Dakikada **120 - 160 vuru / dakikadır** (erişkin kalp hızının yaklaşık iki katı). "
            "FKS'nin dakikada 120'nin altında olması (fetal bradikardi) veya 160'ın üzerinde olması (fetal taşikardi) "
            "akut fetal distres, asidoz veya hipoksi tehlikesini gösterir; acil obstetrik sevk endikasyonudur. "
            "Uygun haftada FKS'nin hiç duyulamaması intrauterin fetal eksitus (ölüm) alarmıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Normal bir gebelikte fetal kalp seslerinin fizyolojik hızı dakikada 120 ile 160 vuru arasındadır.",
                "120 ile 160",
                "İntrauterin fetal kardiyak atım hızı normal referans aralığı"
            ),
            make_table(
                "Fetal Kalp Seslerinin Dinlenme Araçları ve Zaman Eşikleri",
                ["Dinleme Aracı / Yöntem", "Duyulabildiği En Erken Gebelik Haftası", "Çalışma Prensibi"],
                [
                    [
                        "El Doppleri (Doppler USG)",
                        {"text": "10 - 12. Hafta", "isMasked": True, "hint": "Birinci trimester sonunda elektronik ses yakalama eşiği"},
                        "Ultrasonik dalgaların eritrosit hareketine çarpıp yansıması"
                    ],
                    ["Pinard Steteskopu (Fetoskop)", "16 - 20. Hafta", "Doğrudan akustik ses iletimi"],
                    ["Fizyolojik FKS Aralığı", "120 - 160 atım/dk", "Normal sinüs ritmi ve fetal iyilik hali"]
                ]
            ),
            make_micro_quiz(
                "Birinci basamak sağlık biriminde gebe izlemi yapan bir hekim, el Doppleri cihazı ile en erken kaçıncı gebelik haftasından itibaren fetal kalp seslerini (FKS) duyabilir?",
                {
                    "A": "2 - 4. hafta",
                    "B": "6 - 8. hafta",
                    "C": "10 - 12. hafta",
                    "D": "24 - 28. hafta",
                    "E": "36 - 38. hafta"
                },
                "C",
                {
                    "A": "Yanlıştır; Henüz kalp tüpü yeni oluşmaktadır, el Doppleri duyamaz.",
                    "B": "Yanlıştır; Transvajinal USG görüntüler ama el Doppleri dışarıdan duyamaz.",
                    "C": "Doğrudur; El Doppleri ile 10-12. haftalarda FKS duyulabilir.",
                    "D": "Yanlıştır; Çok geçtir.",
                    "E": "Yanlıştır; Doğuma yakın zamandır."
                }
            )
        ]
    })

    # Slayt 36: 2. Gebe İzlemi (18-24. Hafta): Uterus Fundus Yüksekliği ve İzlem
    slides.append({
        "id": "k1-23-s36",
        "title": "2. Gebe İzlemi (18-24. Hafta): Uterus Fundus Yüksekliği ve İzlem",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 36,
        "narrative": (
            "2. Gebe İzlemi **18-24. haftalar arasında** gerçekleştirilir. "
            "Bu dönem fetal büyümenin hızlandığı, organ sistemlerinin ayrıntılı değerlendirildiği evredir: "
            "1. **Anamnez Güncellemesi:** İlk izlemden bu yana şikayet oldu mu? Fetal hareketler hissedilmeye başlandı mı? "
            "(Primiparlarda ~20. haftada, multiparlarda ~16-18. haftada hissedilir). "
            "2. **Fizik Muayene:** Ağırlık artışı, kan basıncı, pretibial ödem ve anemi muayenesi tekrarlanır. "
            "FKS el doppleri veya fetoskopla sayılarak ritmi kontrol edilir (120-160/dk). "
            "3. **Fundus-Pubis Yüksekliği (FPY) Ölçümü:** Simfizis pubis üst kenarından uterus fundusunun en tepe noktasına mezura ile "
            "mesafe ölçülür. 20-34. haftalar arasında **FPY santimetre cinsinden kabaca gebelik haftasına eşittir (±2 cm tolerans)**. "
            "Ölçümün gebelik haftasından **±4 cm ve daha fazla farklı olması** (büyük veya küçük) acil sevk gerektirir "
            "(çoğul gebelik, polihidramnios, fetal makrozomi veya intrauterin gelişme geriliği şüphesi)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Uterus fundus yüksekliğinin beklenen gebelik haftasından artı eksi dört santimetreden fazla farklı olması acil sevk endikasyonudur.",
                "artı eksi dört santimetreden fazla",
                "İntrauterin büyüme sapmasını gösteren mezura sevk eşiği"
            ),
            make_table(
                "Gebelik Haftalarına Göre Uterus Fundus Yüksekliği Anatomik Kılavuzu",
                ["Gebelik Haftası", "Uterus Fundusunun Anatomik Seviyesi", "Klinik Özellik"],
                [
                    ["12. Hafta", "Simfizis pubis hizasında (pelvisten yeni çıkar)", "Bimanuel muayenede hissedilir"],
                    ["16. Hafta", "Simfizis pubis ile göbek çukuru arasında", "Karından palpasyonla rahatça hissedilir"],
                    [
                        "20. Hafta",
                        {"text": "Tam göbek çukuru (Umblikus) hizasında", "isMasked": True, "hint": "Yarı yarıya gestasyonel dönüm noktası seviyesi"},
                        "Fundus yüksekliği yaklaşık 20 cm'dir"
                    ],
                    ["36. Hafta", "Ksifoid çıkıntı (Sternum alt ucu) hizasında", "Maksimum anatomik tepe noktası"],
                    ["40. Hafta", "Bebeğin başı pelvise inince hafifçe aşağı geriler", "Doğum kanalına angajman belirtisi"]
                ]
            ),
            make_active_recall(
                "Normal tekil bir gebelikte 20. gebelik haftasında uterus fundusunun karın muayenesinde tam olarak hangi anatomik kılavuz noktada bulunması beklenir?",
                "Tam göbek çukuru (umblikus) hizasında bulunması beklenir.",
                "Orta hat anatomik göbek hizası"
            )
        ]
    })

    # Slayt 37: İndirekt Coombs Testi ve Rh Uyuşmazlığı Yönetimi
    slides.append({
        "id": "k1-23-s37",
        "title": "İndirekt Coombs Testi ve Rh Uyuşmazlığı Yönetimi",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 37,
        "narrative": (
            "Rh uygunsuzluğu (Anne Rh Negatif, Baba Rh Pozitif olduğunda) fetal eritrositlerin anne kanına geçerek "
            "anne immün sistemini duyarlılaştırması (izoimmünizasyon) ve sonraki gebeliklerde ölümcül **Eritroblastozis Fetalis** tablosu yaratmasıdır: "
            "1. **İndirekt Coombs Testi (İCT):** Annenin serumunda anti-D antikorlarının varlığını araştırır. "
            "Rh uygunsuzluğu olan gebelerde İCT **ilk izlemde ve mutlaka 2. izlemde (18-24. haftalarda)** tekrarlanır. "
            "2. **İCT Negatifse (Duyarlanma Yoksa):** Koruma protokolü uygulanır: "
            "- Gebeliğin **28. haftasında profilaktik tek doz Anti-D İmmünglobulin (Rhogam)** enjeksiyonu yapılır. "
            "- Doğumdan sonra bebeğin kan grubuna bakılır; bebek Rh(+) ise doğumdan sonraki **ilk 72 saat içinde** "
            "anneye tekrar tam doz Anti-D immünglobulin uygulanarak gelecekteki gebelikler güvenceye alınır. "
            "3. **İCT Pozitifse:** Anne zaten duyarlanmıştır; Anti-D verilmesinin faydası yoktur, perinatoloji merkezine sevk edilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Rh uyuşmazlığı olan gebelerde indirekt Coombs testi negatif ise 28. haftada profilaktik anti-D immünglobulin uygulanır.",
                "anti-D immünglobulin",
                "Maternal antikor oluşumunu engelleyen koruyucu pasif immünizasyon"
            ),
            make_causal_chain(
                "Rh İzoimmünizasyonunu Önleme Protokolü",
                [
                    "1. Risk Tespiti: Anne Rh(-), Baba Rh(+) olarak 1. izlemde kaydedilir.",
                    "2. Antikor Taraması: 2. izlemde İndirekt Coombs testi yapılır; negatif olduğu doğrulanır.",
                    "3. Antenatal Profilaksi: 28. gebelik haftasında anneye profilaktik Anti-D İmmünglobulin enjekte edilir.",
                    "4. Postpartum Güvence: Bebek Rh(+) doğarsa ilk 72 saatte ikinci doz Anti-D yapılarak bağışıklama tamamlanır."
                ]
            ),
            make_micro_quiz(
                "Rh uygunsuzluğu bulunan (Anne Rh-, Baba Rh+) ve İndirekt Coombs testi negatif olan bir gebeye Sağlık Bakanlığı protokollerine göre profilaktik Anti-D İmmünglobulin kaçıncı gebelik haftasında yapılmalıdır?",
                {
                    "A": "8. gebelik haftasında",
                    "B": "14. gebelik haftasında",
                    "C": "28. gebelik haftasında",
                    "D": "38. gebelik haftasında",
                    "E": "Yalnızca bebek doğduktan 1 ay sonra"
                },
                "C",
                {
                    "A": "Yanlıştır; Kanama/kürtaj olmadıkça erkendir.",
                    "B": "Yanlıştır; Rutin haftası değildir.",
                    "C": "Doğrudur; İzoimmünizasyon profilaksisi rutin olarak 28. haftada uygulanır.",
                    "D": "Yanlıştır; Geç kalınmış olur.",
                    "E": "Yanlıştır; Doğum sonrası 72 saat içinde yapılır, 1 ay sonra etkisizdir."
                }
            )
        ]
    })

    # Slayt 38: Gestasyonel Diyabet Taraması: 24-28. Hafta Glukoz Tolerans Testi
    slides.append({
        "id": "k1-23-s38",
        "title": "Gestasyonel Diyabet Taraması: 24-28. Hafta Glukoz Tolerans Testi",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 38,
        "narrative": (
            "Gestasyonel Diabetes Mellitus (GDM); ilk kez gebelikte başlayan veya tanınan karbonhidrat intoleransıdır. "
            "Plasentadan salgılanan **İnsan Plasental Laktojeni (hPL)**, progesteron ve kortizol 24. haftadan sonra "
            "annede güçlü bir periferik insülin direnci yaratır. Anne pankreası bu direnci kıramazsa maternal hiperglisemi gelişir. "
            "Fazla glukoz plasentayı geçer; fetal hiperinsülinizm sonucu **Makrozomi (iri bebek >4000 g)**, omuz distosisi, "
            "organomegali, doğum sonrası ölümcül neonatal hipoglisemi ve solunum sıkıntısı (RDS) tablosu patlak verir. "
            "Bu nedenle Sağlık Bakanlığı kılavuzuna göre önceden diyabeti olmayan tüm gebelere **24-28. haftalar arasında "
            "Oral Glukoz Tolerans Testi (OGTT)** yapılması kesinlikle önerilir (tek aşamalı 75g veya iki aşamalı 50g/100g testi)."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Gestasyonel diyabet taraması için oral glukoz tolerans testi gebeliğin yirmi dört ile yirmi sekizinci haftaları arasında yapılır.",
                "yirmi dört ile yirmi sekizinci haftaları",
                "İnsülin direncinin zirveye çıktığı gestasyonel tarama penceresi"
            ),
            make_causal_chain(
                "Tedavi Edilmemiş Gestasyonel Diyabetin Fetal Risk Zinciri",
                [
                    "1. Maternal Hiperglisemi: Annenin kanda yükselen şekeri serbestçe plasentayı aşarak fetüse geçer.",
                    "2. Fetal Hiperinsülinizm: Fetüsün pankreası uyarılır ve bolca insülin (anabolik büyüme hormonu) salgılar.",
                    "3. Fetal Makrozomi: Fetal dokular aşırı büyür; omuz genişler, doğumda omuz takılması ve brakial pleksus felci riski doğar.",
                    "4. Neonatal Hipoglisemi: Doğumda göbek kordonu kesilince glukoz akışı durur ama kanda insülin yüksek kalır; bebek hipoglisemik nöbete girer."
                ]
            ),
            make_active_recall(
                "Gebelikte 24. haftadan sonra fizyolojik insülin direncini tetikleyen en temel plasental hormon hangisidir?",
                "İnsan Plasental Laktojeni (hPL / Human Placental Lactogen) hormonudur.",
                "Plasentadan salınan insülin antagonisti hormon"
            )
        ]
    })

    # Slayt 39: [TEKRAR SAYFASI - CHECKPOINT 4] 1. ve 2. Gebe İzlem Standartları
    slides.append({
        "id": "k1-23-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] 1. ve 2. Gebe İzlem Standartları",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 39,
        "narrative": (
            "Bu dördüncü checkpoint sayfasında, Sağlık Bakanlığı'nın ilk iki gebe izlem standartlarını özetliyoruz: "
            "1. **Takvim:** 1. izlem 0-14. hafta; 2. izlem 18-24. hafta; 3. izlem 28-32. hafta; 4. izlem 36-38. haftada yapılır. "
            "2. **1. İzlem İçeriği:** En az 30 dk öykü, risk formu, boy, kilo (BKİ), bazal kan basıncı, idrar tahlili, kan grubu, Hb-Hct ve HBsAg taraması. "
            "3. **FKS Eşikleri:** El Doppleri ile 10-12. haftada; Pinard steteskopla 16-20. haftada duyulur. Normal hızı 120-160 vuru/dakikadır. "
            "4. **Fundus Yüksekliği:** 20. haftada göbek hizasındadır. Beklenenden ±4 cm ve fazla fark acil sevk gerektirir. "
            "5. **İndirekt Coombs:** Rh uygunsuzluğunda 2. izlemde bakılır; negatifse 28. haftada profilaktik Anti-D uygulanır. "
            "6. **Glukoz Taraması:** 24-28. haftalarda OGTT ile gestasyonel diyabet araştırılır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s39-1",
                "Sağlık Bakanlığı kılavuzuna göre bir gebenin İkinci Gebe İzlemi hangi gebelik haftaları arasında gerçekleştirilmelidir?",
                "Gebeliğin on sekizinci ile yirmi dördüncü haftaları arasında gerçekleştirilmelidir.",
                "İkinci trimesterin orta dönemine denk gelen kontrol aralığı",
                "Gebe İzlem Takvimi"
            ),
            make_flashcard(
                "k1-23-fc-s39-2",
                "İntrauterin fetal canlılığı gösteren normal Fetal Kalp Seslerinin (FKS) dakikadaki atım hızı referans aralığı nedir?",
                "Dakikada yüz yirmi ile yüz altmış atım arasındadır (120-160/dk).",
                "Normal kardiyak vuru limitleri",
                "Fetal Fizyoloji"
            ),
            make_flashcard(
                "k1-23-fc-s39-3",
                "Gestasyonel diyabet taraması için Oral Glukoz Tolerans Testi (OGTT) hangi gebelik haftaları arasında yapılmalıdır?",
                "Gebeliğin yirmi dördüncü ile yirmi sekizinci haftaları arasında yapılmalıdır.",
                "İnsülin direncinin belirdiği gestasyonel tarama penceresi",
                "Laboratuvar Taramaları"
            )
        ],
        "interactiveElements": [
            make_table(
                "1. ve 2. Gebe İzlemi Karşılaştırmalı Özet Tablosu",
                ["Klinik Parametre", "1. İzlem (0-14. Hafta)", "2. İzlem (18-24. Hafta)"],
                [
                    ["Öykü Süresi / Kapsam", "Ayrıntılı ilk anamnez (~30 dk)", "Öyküdeki değişikliklerin takibi (~20 dk)"],
                    [
                        "FKS Dinleme Yöntemi",
                        "El Doppleri ile (10-12. haftadan sonra)",
                        {"text": "El Doppleri veya Pinard steteskopu", "isMasked": True, "hint": "Akustik ve elektronik dinleme cihazları"}
                    ],
                    ["Zorunlu Kan Testleri", "Kan grubu, Hb-Hct, HBsAg", "İndirekt Coombs (Rh uygunsuzluğunda)"],
                    ["Metabolik Tarama", "Açlık kan şekeri (diyabet şüphesi varsa)", "24-28. haftada OGTT planlaması"],
                    ["Uterus Muayenesi", "Bimanuel pelvik muayene", "Mezura ile fundus yüksekliği ölçümü"]
                ]
            )
        ]
    })

    # Slayt 40: Bölüm Özeti: İlk İki İzlemden 3. ve 4. Gebe İzlemine Geçiş
    slides.append({
        "id": "k1-23-s40",
        "title": "Bölüm Özeti: İlk İki İzlemden 3. ve 4. Gebe İzlemine Geçiş",
        "section": "Sağlık Bakanlığı Gebe İzlem Protokolü: 1. ve 2. İzlem",
        "slideNumber": 40,
        "narrative": (
            "1. ve 2. Gebe İzlemleri, gebeliğin temellerinin atıldığı, bazal parametrelerin (kan basıncı, idrar, Hb, HBsAg, kan grubu) "
            "belirlendiği ve fetal kalp seslerinin doğrulanarak gestasyonel diyabet ile Rh izoimmünizasyonunun taranmaya başlandığı evredir. "
            "Bu iki vizit zamanında ve eksiksiz yapıldığında gebelik komplikasyonlarının yarısından fazlası henüz başlangıç aşamasında önlenir. "
            "Ancak gebelik ilerledikçe riskler değişir: 28. haftadan sonra preeklampsi fırtınası, erken doğum tehdidi, "
            "fetal pozisyon anomalileri ve doğum eyleminin yönetimi ön plana çıkar. "
            "Beşinci bölümümüzde, **'3. İzlem (28-32. Hafta), 4. İzlem (36-38. Hafta), Leopold Manevraları, "
            "Pelvik Muayene, İkili/Üçlü Tarama Testleri ve Tetanoz Aşılama Takvimi'** ele alınacaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Birinci basamakta gebe izlemi yapan hekimin 18-24. haftalarda yapılan 2. izlemde kaçırmaması gereken en kritik iki laboratuvar planlaması nedir?",
                "Rh uyuşmazlığında İndirekt Coombs testi yapılması ve 24-28. haftalarda OGTT şeker yükleme testinin planlanmasıdır.",
                "Rh antikoru ve diyabet taraması planı"
            ),
            make_branching_logic(
                "22 haftalık bir gebe 2. izlem için polikliniğe geliyor. Yapılan mezura ölçümünde uterus fundus yüksekliği 28 cm ölçülüyor (gebelik haftasından 6 cm büyük).",
                "Hekim olarak bu hastaya yönelik atılması gereken en doğru klinik adım hangisidir?",
                [
                    {
                        "text": "Fundus yüksekliğinin beklenen haftadan ±4 cm'den fazla büyük olması nedeniyle çoğul gebelik, polihidramnios veya makrozomi şüphesiyle hastayı kadın doğum uzmanına / ultrasona sevk etmek",
                        "isCorrect": True,
                        "feedback": "Mükemmel Klinik Yargı: ±4 cm kuralı aşılmıştır; FPY 6 cm büyüktür ve altta yatan çoğul gebelik veya amniyon sıvısı fazlalığı için acil ileri inceleme şarttır."
                    },
                    {
                        "text": "Bunun çok normal olduğunu, bebeğin sadece biraz gürbüz olacağını söyleyip 36. haftada kontrole çağırmak",
                        "isCorrect": False,
                        "feedback": "Hatalı ve Tehlikeli: 6 cm'lik fark patolojiktir, polihidramnios veya anomali atlanabilir."
                    },
                    {
                        "text": "Hastaya acilen diyetisyene gidip ekmeği kesmesini tembihleyerek eve göndermek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Sorun kilo değil, intrauterin hacim artışıdır; ultrason gereklidir."
                    }
                ]
            )
        ]
    })

    return slides
