# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)
Bölüm 10: Farmakolojik Tedavi İlkeleri ve Tromboz Büyük Özeti (Slayt 91 - 100)
Checkpoint 10: Slayt 100
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: Antiplatelet Tedaviler
    slides.append({
        "id": "k1-20-s91",
        "title": "Antiplatelet Tedaviler: Trombosit Fonksiyonlarının Blokajı",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 91,
        "narrative": (
            "Arteriyel trombozlar trombositten zengin (beyaz pıhtı) olduğundan, bu patolojilerin önlenmesinde "
            "ve tedavisinde temel farmakolojik dayanak **antiplatelet ilaçlardır**. "
            "Etki mekanizmalarına göre 3 ana grup kullanılır: "
            "1. **Siklooksijenaz (COX) İnhibitörleri (Aspirin):** Trombositlerdeki COX-1 enzimini geri dönüşümsüz olarak "
            "asetilleyip inhibe eder. Trombositler çekirdeksiz olduğu için yeni enzim sentezleyemez; bu nedenle trombositin "
            "tüm yaşam süresi boyunca (7-10 gün) güçlü agregasyon ve vazokonstriksiyon uyarıcısı olan Tromboksan A2 (TxA2) sentezi durur. "
            "2. **P2Y12 Reseptör Blokerleri (Klopidogrel, Prasugrel, Tikagrelor):** Trombosit yüzeyindeki ADP reseptörü olan "
            "P2Y12'yi bloke ederek ADP aracılı aktivasyonu ve GpIIb/IIIa reseptör ekspresyonunu engeller. "
            "3. **GpIIb/IIIa Reseptör Antagonistleri (Absiksimab, Tirofiban, Eptifibatid):** Fibrinojenin bağlandığı son ortak yolak "
            "olan integrin kompleksini doğrudan bloke ederek trombosit agregasyonunu en güçlü şekilde durdurur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Aspirin trombositlerdeki COX-1 enzimini geri dönüşümsüz olarak inhibe ederek Tromboksan A2 sentezini baskılar.",
                "Tromboksan A2",
                "COX-1 aktivitesi sonucu üretilen güçlü trombosit agregasyon medyatörü"
            ),
            make_table(
                ["İlaç Grubu", "Moleküler Hedef", "Klinik Kullanım Endikasyonu"],
                [
                    ["Asetilsalisilik Asit (Aspirin)", "Trombosit COX-1 enzimi (TxA2 blokajı)", "Miyokard enfarktüsü ve inme profilaksisi"],
                    [
                        "P2Y12 Reseptör Blokerleri",
                        {"text": "ADP P2Y12 reseptörü", "isMasked": True, "hint": "Klopidogrel ve tikagrelorun bağlandığı nükleotid reseptörü"},
                        "Akut koroner sendrom ve koroner stent trombozu önleme"
                    ],
                    ["GpIIb/IIIa İnhibitörleri", "Fibrinojen bağlayan integrin kompleksi", "Yüksek riskli perkütan koroner girişimler (PCI)"]
                ]
            ),
            make_micro_quiz(
                "Aspirinin trombositler üzerindeki antiagregan etkisinin trombosit ömrü (7-10 gün) boyunca kalıcı olmasının temel nedeni nedir?",
                {
                    "A": "Aspirinin böbreklerden hiç atılamayıp plazmada birikmesi",
                    "B": "Trombositlerin çekirdeksiz olması ve yeni COX-1 proteini sentezleyememesi",
                    "C": "Aspirinin endotel hücresindeki PGI2 sentezini kalıcı durdurması",
                    "D": "Kemik iliğinde megakaryosit üretimini tamamen felç etmesi",
                    "E": "Trombositlerdeki von Willebrand faktör genini susturması"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; aspirinin plazma yarı ömrü çok kısadır (yaklaşık 20 dakika).",
                    "B": "B seçeneği doğrudur: Trombositler çekirdeksiz olduğu için irreversibl asetillenen COX-1 yerine yenisini üretemez; etki trombositin ömrü boyunca sürer.",
                    "C": "C seçeneği yanlıştır; endotel çekirdekli olduğu için COX-1/COX-2'yi hızla yeniden sentezleyip PGI2 üretimini sürdürür.",
                    "D": "D seçeneği yanlıştır; megakaryosit üretimini durdurmaz.",
                    "E": "E seçeneği yanlıştır; vWF geni megakaryosit ve endoteldedir, aspirin bu geni etkilemez."
                }
            )
        ]
    })

    # Slayt 92: Antikoagülan Tedaviler I (Heparinler)
    slides.append({
        "id": "k1-20-s92",
        "title": "Antikoagülan Tedaviler I: Standart Heparin ve DMAH",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 92,
        "narrative": (
            "Antikoagülan ilaçlar, pıhtılaşma kaskadındaki faktörleri inhibe ederek fibrin ağının oluşumunu "
            "ve trombüs propagasyonunu engeller. Klinikte en köklü parenteral antikoagülan **heparin** ailesidir. "
            "Heparinler etkilerini doğrudan göstermez; plazmanın doğal antikoagülanı olan **Antitrombin III (ATIII)** molekülüne "
            "bağlanarak onun konformasyonunu değiştirir ve inhibitör hızını yaklaşık 1000 kat artırır. "
            "1. **Fraksiyone Olmayan Standart Heparin (UFH):** Uzun polisakkarit zinciri sayesinde hem Antitrombin III'e hem de "
            "Trombine (Faktör IIa) aynı anda bağlanabilen bir köprü oluşturur; böylece hem Trombini hem de Faktör Xa'yı eşit güçte bloke eder (1:1 oran). "
            "Etkisi **aPTT (aktive parsiyel tromboplastin zamanı)** testi ile takip edilir. Aşırı dozunda antidotu **Protamin sülfattır**. "
            "2. **Düşük Molekül Ağırlıklı Heparin (DMAH / Enoksaparin):** Kısa zincirli olduğundan trombin köprüsü kuramaz; "
            "ATIII üzerinden seçici olarak **Faktör Xa**'yı inhibe eder (oran yaklaşık 3:1 veya 4:1). "
            "Biyoyararlanımı yüksek, dozu öngörülebilir ve heparin kaynaklı trombositopeni (HIT) riski UFH'ye göre çok daha düşüktür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Standart heparinin aşırı dozuna bağlı kanamalarda kullanılan spesifik nötralizan antidot protamin sülfat bileşiğidir.",
                "protamin sülfat",
                "Pozitif yüklü heparin antagonist proteini"
            ),
            make_before_after(
                "Standart Heparin (UFH) ile Düşük Molekül Ağırlıklı Heparin (DMAH) Karşılaştırması",
                "Standart Heparin (UFH)",
                [
                    "Hedef faktörler: Eşit güçte Trombin (IIa) ve Faktör Xa inhibisyonu (1:1)",
                    "Laboratuvar takibi: Zorunlu aPTT takibi gerektirir",
                    "Uygulama yolu: Sürekli intravenöz infüzyon veya subkutan",
                    "Spesifik antidot: Protamin sülfat ile %100 tam nötralizasyon"
                ],
                "Düşük Molekül Ağırlıklı Heparin (DMAH)",
                [
                    "Hedef faktörler: Seçici olarak Faktör Xa inhibisyonu baskındır (3:1)",
                    "Laboratuvar takibi: Rutin takip gerekmez (özel durumlarda Anti-Xa düzeyi)",
                    "Uygulama yolu: Günde 1-2 kez sabit doz subkutan enjeksiyon",
                    "Spesifik antidot: Protamin sülfat ile yalnızca parsiyel (%60) nötralizasyon"
                ]
            ),
            make_active_recall(
                "Heparinlerin antikoagülan etkilerini gösterebilmeleri için plazmada mutlaka bulunması gereken kofaktör molekül hangisidir?",
                "Antitrombin III (ATIII) molekülüdür.",
                "Heparinin bağlandığı endojen serin proteaz inhibitörü"
            )
        ]
    })

    # Slayt 93: Antikoagülan Tedaviler II (Varfarin)
    slides.append({
        "id": "k1-20-s93",
        "title": "Antikoagülan Tedaviler II: Varfarin ve K Vitamini Döngüsü",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 93,
        "narrative": (
            "Varfarin (Coumadin), on yıllardır kullanılan klasik oral antikoagülandır. "
            "Karaciğerde **K vitamini epoksit redüktaz kompleksi 1 (VKORC1)** enzimini inhibe ederek "
            "K vitamininin indirgenmiş (aktif) formuna dönüşümünü engeller. "
            "Aktif K vitamini bulunamadığında, **Faktör II (protrombin), VII, IX, X** ve doğal antikoagülanlar olan "
            "**Protein C ve Protein S**'in glutamat kalıntıları gama-karboksillenemez. "
            "Karboksillenmeyen bu faktörler kalsiyum iyonlarına bağlanamadığı için pıhtılaşma reaksiyonlarına katılamaz. "
            "Varfarinin etkisi **PT / INR (Uluslararası Düzeltme Oranı)** ile takip edilir (hedef genellikle 2.0 - 3.0). "
            "**Kritik Patolojik Uyarı:** Varfarin başlandığında yarı ömrü en kısa olan faktör Protein C'dir (yaklaşık 6-8 saat). "
            "Bu nedenle tedavinin ilk 24-48 saatinde pıhtılaşma faktörleri henüz kanda dolaşırken doğal antikoagülan Protein C çöker; "
            "bu geçici hiperkoagülabilite penceresi mikrovasküler trombozlara ve **Varfarin Kaynaklı Deri Nekrozuna** yol açabilir! "
            "Bu felaketi önlemek için varfarin daima heparin köprülemesi ile birlikte başlanır. Aşırı doz antidotu K vitamini ve taze donmuş plazmadır (TDP/PCC)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Varfarin tedavisine başlandığında yarı ömrü en kısa olan Protein C hızla tükenerek geçici protrombotik deri nekrozu riskine yol açar.",
                "Protein C",
                "Varfarin başlandığında ilk tükenen endojen antikoagülan protein"
            ),
            make_causal_chain(
                "Varfarin Kaynaklı Cilt Nekrozu Mekanizması",
                [
                    "1. Varfarin Başlangıcı: Karaciğerde K vitamini döngüsü bloke edilir.",
                    "2. Hızlı Protein C Tükenmesi: Yarı ömrü 6 saat olan Protein C kandan hızla temizlenir.",
                    "3. Geçici Hiperkoagülabilite: Faktör II ve X henüz aktifken antikoagülan fren ortadan kalkar.",
                    "4. Mikrovasküler Tromboz: Meme, uyluk ve kalça deri venüllerinde yaygın mikrotrombüsler oluşur.",
                    "5. Nekroz ve Gangren: Deri perfüzyonu durarak geniş hemorajik cilt nekrozu gelişir."
                ]
            ),
            make_micro_quiz(
                "Varfarin tedavisinin etkinliği ve güvenliği hangi laboratuvar parametresi ile monitörize edilir?",
                {
                    "A": "aPTT (aktive parsiyel tromboplastin zamanı)",
                    "B": "Kanama zamanı (Bleeding time)",
                    "C": "Protrombin Zamanı / INR (International Normalized Ratio)",
                    "D": "Trombin zamanı (TT)",
                    "E": "D-Dimer plazma düzeyi"
                },
                "C",
                {
                    "A": "A seçeneği heparinin takibinde kullanılır.",
                    "B": "B seçeneği trombosit fonksiyonlarını ve vWF'yi tarar.",
                    "C": "C seçeneği doğrudur: Varfarin ekstrinsik yolu (başta Faktör VII) etkilediğinden PT/INR testi ile takip edilir.",
                    "D": "D seçeneği fibrinojenin fibrine dönüşümünü ölçer.",
                    "E": "E seçeneği fibrinoliz göstergesidir, antikoagülasyon takibinde kullanılmaz."
                }
            )
        ]
    })

    # Slayt 94: Antikoagülan Tedaviler III (DOAC'lar)
    slides.append({
        "id": "k1-20-s94",
        "title": "Antikoagülan Tedaviler III: Direkt Oral Antikoagülanlar (DOAC)",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 94,
        "narrative": (
            "Direkt Oral Antikoagülanlar (DOAC / NOAC), son yıllarda varfarinin yerini büyük ölçüde alan yeni nesil moleküllerdir. "
            "Pıhtılaşma faktörlerini kofaktöre ihtiyaç duymadan doğrudan ve seçici olarak inhibe ederler. İki ana sınıfa ayrılırlar: "
            "1. **Direkt Faktör Xa İnhibitörleri:** İsimlerinde 'xa' hecesi bulunan **Rivaroksaban, Apiksaban ve Edoksaban**'dır. "
            "Hem serbest Faktör Xa'yı hem de protrombinaz kompleksi içindeki Xa'yı bloke ederler. Spesifik antidotları modifiye rekombinant protein olan **Andeksanet alfa**'dır. "
            "2. **Direkt Trombin (Faktör IIa) İnhibitörü:** **Dabigatran** eteksilattır. Trombinin aktif bölgesine bağlanarak serbest ve pıhtıya bağlı trombini bloke eder. "
            "Spesifik antidotu monoklonal antikor fragmanı olan **İdarusizumab (Praxbind)**'tır. "
            "DOAC'ların varfarine üstünlükleri: Sabit dozda kullanılabilmeleri, gıda-ilaç etkileşimlerinin çok az olması, "
            "en önemlisi rutin laboratuvar (INR) takibi gerektirmemeleri ve ölümcül intrakraniyal kanama riskini anlamlı oranda azaltmalarıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Direkt trombin inhibitörü dabigatranın hayatı tehdit eden kanamalarında kullanılan spesifik antidot idarusizumab monoklonal antikorudur.",
                "idarusizumab",
                "Dabigatranı bağlayıp nötralize eden spesifik monoklonal Fab fragmanı"
            ),
            make_table(
                ["DOAC İlaç Sınıfı", "Örnek Moleküller", "Doğrudan Moleküler Hedef", "Spesifik Antidot"],
                [
                    ["Direkt Xa İnhibitörleri", "Rivaroksaban, Apiksaban, Edoksaban", "Faktör Xa", "Andeksanet alfa"],
                    ["Direkt Trombin İnhibitörü", "Dabigatran eteksilat", "Trombin (Faktör IIa)", "İdarusizumab"]
                ]
            ),
            make_micro_quiz(
                "Direkt oral antikoagülanların (DOAC) klasik varfarin tedavisine göre en belirgin pratik ve klinik avantajı hangisidir?",
                {
                    "A": "Rutin INR veya pıhtılaşma takibi gerektirmemesi ve intrakraniyal kanama riskinin düşük olması",
                    "B": "Yalnızca intravenöz infüzyonla uygulanabilmesi",
                    "C": "Vücutta hiçbir kanama yan etkisine yol açmaması",
                    "D": "K vitamini eksikliği yaratarak osteoporozu önlemesi",
                    "E": "Trombosit sayısını doğrudan artırarak kanamayı durdurması"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Sabit doz kullanımı, rutin kan takibi ihtiyacının olmaması ve kafa içi kanama riskinin varfarine göre belirgin düşük olması DOAC'ların temel avantajıdır.",
                    "B": "B seçeneği yanlıştır; oral yoldan hap şeklinde kullanılırlar.",
                    "C": "C seçeneği yanlıştır; tüm antikoagülanlar gibi kanama riski taşırlar.",
                    "D": "D seçeneği yanlıştır; DOAC'lar K vitaminini etkilemez.",
                    "E": "E seçeneği yanlıştır; trombosit sayısını artırmazlar."
                }
            )
        ]
    })

    # Slayt 95: Fibrinolitik (Trombolitik) Tedaviler
    slides.append({
        "id": "k1-20-s95",
        "title": "Fibrinolitik Tedaviler: Oluşmuş Pıhtının Acil Eritilmesi",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 95,
        "narrative": (
            "Antiplatelet ve antikoagülan ilaçlar yeni trombüs oluşumunu ve var olanın büyümesini engellerken, "
            "**oluşmuş bir pıhtıyı doğrudan sindirebilen** yegane farmakolojik sınıf **trombolitik (fibrinolitik)** ajanlardır. "
            "Bu moleküller plazminojeni aktif plazmine çevirerek pıhtının fibrin iskeletini parçalar. "
            "Klinikte rekombinant DNA teknolojisiyle üretilen doku plazminojen aktivatörü türevleri kullanılır: "
            "**Alteplaz (rt-PA), Tenekteplaz (TNK-tPA) ve Reteplaz**. "
            "Trombolitiklerin en kritik iki kullanım alanı: Akut ST elevasyonlu miyokard enfarktüsü (STEMI) ve "
            "akut iskemik inmedir (inmede ilk 4.5 saat içinde uygulanmalıdır). "
            "**Mutlak Kontrendikasyonlar:** Pıhtıyı eriten bu agresif tedavi kontrolsüz kanamalara yol açabileceğinden; "
            "aktif iç kanama, geçirilmiş hemorajik inme, son 3 ayda kafa travması/cerrahisi, şüpheli aort diseksiyonu "
            "ve intrakraniyal vasküler malformasyon/neoplazm durumlarında trombolitik tedavi kesinlikle yasaktır!"
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Akut iskemik inmede rekombinant t-PA tedavisi geri dönüşümsüz beyin hasarını ve hemoraji riskini önlemek için ilk 4.5 saat içinde verilmelidir.",
                "ilk 4.5 saat",
                "Akut iskemik inmede intravenöz alteplaz için kabul edilen altın pencere süresi"
            ),
            make_causal_chain(
                "Trombolitik Tedavi ve Reperfüzyon Zinciri",
                [
                    "1. Damar Tıkanıklığı: Koroner arterde fibrin ve trombositten zengin taze oklüziv pıhtı oluşur.",
                    "2. rt-PA Uygulaması: İntravenöz yolla rekombinant doku plazminojen aktivatörü verilir.",
                    "3. Fibrine Bağlanma: t-PA pıhtı içindeki fibrine yüksek affiniteyle tutunur.",
                    "4. Plazmin Patlaması: Fibrine bağlı plazminojen aktif plazmine dönüştürülür.",
                    "5. Fibrinoliz ve Reperfüzyon: Fibrin lifleri kesilerek damar lümeni hızla açılır ve doku kurtarılır."
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki durumlardan hangisi trombolitik (t-PA) tedavisi için bir 'mutlak kontrendikasyon' oluşturur?",
                {
                    "A": "Hafif kontrol altında hipertansiyon (130/85 mmHg)",
                    "B": "Hastanın yaşının 60 olması",
                    "C": "Şüpheli aort diseksiyonu veya geçirilmiş hemorajik inme öyküsü",
                    "D": "Hastada sigara içme öyküsünün bulunması",
                    "E": "Hastanın serum kolesterol düzeyinin yüksek olması"
                },
                "C",
                {
                    "A": "A seçeneği kontrendikasyon değildir (ağır kontrolsüz hipertansiyon >185/110 mmHg rölatiftir).",
                    "B": "B seçeneği kontrendikasyon değildir.",
                    "C": "C seçeneği doğrudur: Aort diseksiyonu ve intrakraniyal kanama öyküsü fatal rüptür ve ölüm riski nedeniyle mutlak kontrendikasyondur.",
                    "D": "D seçeneği ateroskleroz risk faktörüdür, kontrendikasyon değildir.",
                    "E": "E seçeneği kontrendikasyon değildir."
                }
            )
        ]
    })

    # Slayt 96: Tromboprofilaksi İlkeleri
    slides.append({
        "id": "k1-20-s96",
        "title": "Tromboprofilaksi İlkeleri: Virchow Triyadını Kırmak",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 96,
        "narrative": (
            "Hastanede yatan hastalarda, özellikle büyük cerrahi geçirenlerde (örneğin total kalça/diz protezi) "
            "ve yoğun bakımda yatan dahili hastalarda DVT ve pulmoner emboli en önemli önlenebilir ölüm nedenidir. "
            "Tromboprofilaksinin temel mantığı Virchow triyadının elemanlarını (staz ve hiperkoagülabilite) kırmaktır: "
            "1. **Mekanik Profilaksi (Stazı Giderme):** Ameliyat sonrası hastaların mümkün olan en erken dönemde ayağa kaldırılması "
            "(erken mobilizasyon) baldır kas pompasını çalıştırarak stazı önler. "
            "Ayağa kalkamayan yatalak hastalarda kademeli kompresyon çorapları (anti-emboli çorapları) ve "
            "aralıklı pnömatik kompresyon (IPC) cihazları kullanılarak venöz kanın kalbe pompalanması sağlanır. "
            "2. **Farmakolojik Profilaksi (Hiperkoagülabiliteyi Baskılama):** Yüksek ve orta riskli hastalarda kontrendikasyon yoksa "
            "düşük doz subkutan Düşük Molekül Ağırlıklı Heparin (örneğin Enoksaparin 40 mg/gün) uygulanır. "
            "Mekanik ve farmakolojik profilaksinin kombine kullanımı perioperatif tromboemboli riskini %70'ten fazla azaltır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Cerrahi sonrası yatağa bağımlı hastalarda venöz stazı önlemek için bacaklara hava basıncı uygulayan aralıklı pnömatik kompresyon cihazları kullanılır.",
                "pnömatik kompresyon",
                "Mekanik venöz pompa sağlayan kompresyon sistemi türü"
            ),
            make_before_after(
                "Mekanik Profilaksi ile Farmakolojik Profilaksi Karşılaştırması",
                "Mekanik Tromboprofilaksi",
                [
                    "Yöntemler: Kademeli kompresyon çorabı, aralıklı pnömatik kompresyon, erken mobilizasyon",
                    "Hedef mekanizma: Venöz stazı kırmak ve akım hızını artırmak",
                    "Kanama riski: Kesinlikle kanama riski oluşturmaz",
                    "Öncelikli grup: Aktif kanaması olan veya kanama riski çok yüksek cerrahi hastalar"
                ],
                "Farmakolojik Tromboprofilaksi",
                [
                    "Yöntemler: Profilaktik doz DMAH (Enoksaparin), subkutan heparin veya DOAC",
                    "Hedef mekanizma: Pıhtılaşma kaskadını (Faktör Xa/trombin) baskılamak",
                    "Kanama riski: Düşük de olsa sistemik kanama riski taşır",
                    "Öncelikli grup: Kanama riski kabul edilebilir yüksek tromboz riskli hastalar"
                ]
            ),
            make_active_recall(
                "Total kalça protezi ameliyatı geçiren bir hastada en önemli önlenebilir hastane içi ölüm nedeni nedir?",
                "Derin ven trombozuna bağlı gelişen masif Pulmoner Embolizmdir.",
                "Ortopedik cerrahinin en korkulan ölümcül trombotik komplikasyonu"
            )
        ]
    })

    # Slayt 97: Trombozda Biyobelirteçler (D-Dimer)
    slides.append({
        "id": "k1-20-s97",
        "title": "Trombozda Biyobelirteçler: D-Dimer ve Klinik Anlamı",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 97,
        "narrative": (
            "Klinik pratikte tromboz ve tromboembolizm şüphesinde en sık başvurulan biyobelirteç **D-Dimer** testidir. "
            "D-Dimer, Faktör XIIIa tarafından kovalent çapraz bağlarla birbirine bağlanmış polimerize fibrin ağının, "
            "plazmin tarafından parçalanması sonucu ortaya çıkan spesifik bir fibrin yıkım ürünüdür (FDP). "
            "D-Dimer testinin klinikteki en büyük gücü **yüksek negatif prediktif değeridir (%95'in üzerinde)**. "
            "Düşük veya orta klinik olasılıklı bir hastada D-Dimer düzeyi normalse (negatifse), vücutta aktif bir venöz tromboz veya "
            "pulmoner emboli bulunmadığı güvenle söylenebilir ve ileri tetkike gerek kalmadan tanı dışlanabilir. "
            "Ancak D-Dimer testinin **özgüllüğü (spesifisitesi) oldukça düşüktür!** "
            "Çünkü pıhtılaşma ve fibrinolizin aktive olduğu her durumda; ileri yaş, gebelik, cerrahi girişimler, "
            "travma, enfeksiyonlar, sepsis ve malignitelerde de D-Dimer düzeyi yüksek çıkabilir. "
            "Bu nedenle tek başına D-Dimer yüksekliği tromboz tanısı koydurmaz, sadece ileri görüntülemeyi gerektirir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "D-Dimer testi yüksek negatif prediktif değeri sayesinde tromboz şüphesi olan hastalarda tanıyı dışlamak amacıyla kullanılır.",
                "negatif prediktif değeri",
                "Testin normal çıkması durumunda hastalığın olmadığını gösteren istatistiksel parametre"
            ),
            make_table(
                ["D-Dimer Test Durumu", "Klinik Yorumu", "Yapılması Gereken Eylem"],
                [
                    ["D-Dimer Negatif (Normal)", "Aktif tromboz veya PE ihtimali yok denecek kadar azdır", "Tanı güvenle dışlanır, görüntülemeye gerek yoktur"],
                    [
                        "D-Dimer Pozitif (Yüksek)",
                        {"text": "Tromboz olabilir veya non-spesifik enflamasyon mevcuttur", "isMasked": True, "hint": "Spesifisitenin düşük olmasının sonucu"},
                        "Ultrasonografi veya BT Anjiyo ile kesin doğrulama yapılır"
                    ]
                ]
            ),
            make_micro_quiz(
                "Acil servise bacak ağrısıyla başvuran düşük klinik riskli bir hastada D-Dimer testinin negatif (normal sınırlarda) bulunması ne anlama gelir?",
                {
                    "A": "Hastada kesinlikle masif derin ven trombozu vardır, acil cerrahi gerekir.",
                    "B": "DVT ve pulmoner emboli tanısı güvenle dışlanabilir, ileri görüntülemeye gerek yoktur.",
                    "C": "Hastada kemik iliği yetmezliği geliştiğini gösterir.",
                    "D": "D-Dimer testinin hiçbir klinik değeri olmadığından doğrudan anjiyografi yapılmalıdır.",
                    "E": "Hastaya derhal yüksek doz trombolitik tedavi başlanmalıdır."
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; test negatifken tromboz tanısı konulamaz.",
                    "B": "B seçeneği doğrudur: D-Dimer testinin negatif prediktif değeri çok yüksektir; negatif sonuç DVT/PE olasılığını dışlar.",
                    "C": "C seçeneği yanlıştır; kemik iliğiyle doğrudan ilişkili bir belirteç değildir.",
                    "D": "D seçeneği yanlıştır; dışlama amaçlı en değerli testtir.",
                    "E": "E seçeneği yanlıştır; negatif hastaya trombolitik verilmez."
                }
            )
        ]
    })

    # Slayt 98: Tanı Algoritmaları ve Görüntüleme Altın Standartları
    slides.append({
        "id": "k1-20-s98",
        "title": "Tanı Algoritmaları: Görüntülemenin Altın Standartları",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 98,
        "narrative": (
            "Tromboz şüphesinde klinik skorlama (örneğin DVT ve PE için Wells skoru) ve D-Dimer sonrasında "
            "kesin tanı görüntüleme yöntemleriyle doğrulanır. Modern tıpta kabul edilen altın standartlar şunlardır: "
            "1. **Derin Ven Trombozu (DVT):** Altın standart non-invaziv yöntem **Kompresyon Doppler Ultrasonografidir**. "
            "Normal bir ven prob ile hafifçe bastırıldığında lümeni tamamen kollabe olur (basılarak kapanır). "
            "Eğer ven lümeninde bir trombüs varsa damar lümeni **kollabe olmaz (basılamaz ven)** ve Doppler incelemesinde akım kaybı saptanır. "
            "2. **Pulmoner Tromboembolizm (PE):** Altın standart tanı yöntemi **Bilgisayarlı Tomografi Pulmoner Anjiyografidir (BTPA)**. "
            "Pulmoner arter dalları içindeki pıhtıyı dolum defekti şeklinde doğrudan ve net olarak gösterir. "
            "3. **Koroner Tromboz (STEMI):** Altın standart girişimsel yöntem **Acil Koroner Anjiyografidir (KAG)**; "
            "tıkanıklık saptandığı anda primer perkütan koroner girişimle (balon/stent) damar açılır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Kompresyon ultrasonografisinde ven prob baskısıyla kollabe olmuyorsa lümende oklüziv trombüs varlığı kanıtlanır.",
                "kollabe olmuyorsa",
                "DVT tanısında prob basısı ile ven lümeninin kapanmama durumu"
            ),
            make_table(
                ["Klinik Tromboz Tablosu", "Altın Standart Tanı Yöntemi", "Patolojik Radyolojik Bulgu"],
                [
                    ["Derin Ven Trombozu (DVT)", "Kompresyon Doppler Ultrasonografi", "Prob basısına dirençli basılamayan ven lümeni"],
                    [
                        "Pulmoner Emboli (PE)",
                        {"text": "BT Pulmoner Anjiyografi (BTPA)", "isMasked": True, "hint": "Kontrastlı tomografik damar görüntülemesi"},
                        "Pulmoner arter lümeninde intralüminal dolum defekti"
                    ],
                    ["Akut Koroner Tromboz", "Konvansiyonel Koroner Anjiyografi", "Epikardiyal koroner arterde tam lümen oklüzyonu"]
                ]
            ),
            make_branching_logic(
                "Nefes darlığı ve göğüs ağrısı ile acile getirilen 58 yaşındaki hastada Wells skoru yüksek bulunmuş ve Bilgisayarlı Tomografi Pulmoner Anjiyografi çekilmiştir. Sol ana pulmoner arterde kontrast tutmayan dolum defekti saptanmıştır.",
                "Bu hastanın kesin patolojik tanısı ve derhal başlanması gereken tedavi yaklaşımı nedir?",
                [
                    {
                        "key": "A",
                        "text": "Akut Pulmoner Emboli tanısıdır; hemodinami stabilse derhal tam doz antikoagülan tedavi başlanmalıdır.",
                        "isCorrect": True,
                        "explanation": "Doğru karar: BTPA'da dolum defekti pulmoner emboli için kesin altın standart tanı kriteridir; acil antikoagülasyon hayat kurtarır."
                    },
                    {
                        "key": "B",
                        "text": "Aort anevrizması rüptürüdür; hasta acil açık kalp ameliyatına alınmalıdır.",
                        "isCorrect": False,
                        "explanation": "Yanlış karar: Dolum defekti pulmoner arterdedir, aortta değildir."
                    },
                    {
                        "key": "C",
                        "text": "Yalnızca mekanik varis çorabı giydirilmeli ve hasta taburcu edilmelidir.",
                        "isCorrect": False,
                        "explanation": "Yanlış karar: Pulmoner emboli mortalitesi yüksek bir tablodur, mekanik çorap tek başına tedavi olamaz."
                    },
                    {
                        "key": "D",
                        "text": "Pnömotoraks gelişmiştir, acil göğüs tüpü takılmalıdır.",
                        "isCorrect": False,
                        "explanation": "Yanlış karar: Plevral hava kaçağı değil vasküler dolum defekti mevcuttur."
                    }
                ]
            )
        ]
    })

    # Slayt 99: Tromboz Araştırmalarında Gelecek Perspektifleri
    slides.append({
        "id": "k1-20-s99",
        "title": "Tromboz Araştırmalarında Gelecek: FXIa İnhibitörleri ve Nanotıp",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 99,
        "narrative": (
            "Geleneksel tüm antikoagülanların en büyük ortak dezavantajı, hemostaz ile tromboz arasındaki "
            "ortak enzimleri (Faktör Xa ve trombin) bloke ettikleri için tedavi dozlarında dahi kanama riski yaratmalarıdır. "
            "Bu paradoksu çözmek amacıyla geliştirilen yeni nesil stratejiler **kontakt aktivasyon yolağı (intrinsik yolak)** "
            "üzerine yoğunlaşmıştır. Özellikle **Faktör XIa (FXIa) ve Faktör XIIa inhibitörleri** klinik faz çalışmalarında büyük heyecan yaratmaktadır. "
            "FXI eksikliği olan bireylerde ciddi spontan kanama görülmezken, bu bireylerin tromboza karşı belirgin şekilde dirençli olduğu saptanmıştır. "
            "Dolayısıyla FXIa blokajı, 'kanama yapmayan ideal antikoagülan' hayalini gerçeğe dönüştürmeye en yakın adaydır. "
            "Ayrıca nanotıp alanında, pıhtı yüzeyindeki aktif trombositleri veya fibrin liflerini tanıyan "
            "biyomimetik nanorobotlar ve nanopartiküller sayesinde, trombolitik ilaçların sadece trombüs içine lokalize olarak "
            "salınması ve sistemik kanama riskinin sıfıra indirilmesi hedeflenmektedir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Geleceğin antikoagülan tedavilerinde hemostazı bozmadan trombozu önlemeyi hedefleyen yeni ilaçlar Faktör XIa enzimini hedeflemektedir.",
                "Faktör XIa",
                "İntrinsik yolağın kanama riski oluşturmayan hedeflenen faktörü"
            ),
            make_table(
                ["Yeni Tedavi Stratejisi", "Hedeflenen Yolak / Teknoloji", "Geleneksel Tedaviye Üstünlüğü"],
                [
                    ["Faktör XIa İnhibitörleri", "Kontakt yolak / FXI inhibisyonu", "Hemostatik pıhtıyı bozmadan patolojik trombozu engelleme"],
                    [
                        "Nanopartikül Tromboliz",
                        {"text": "Hedefe yönelik lokalize t-PA salınımı", "isMasked": True, "hint": "İlacı sadece pıhtı içine boşaltan nanoteknoloji"},
                        "Sistemik fatal kanama komplikasyonlarını ortadan kaldırma"
                    ],
                    ["RNA İnterferans (siRNA)", "Karaciğerde faktör transkripsiyon susturması", "Yılda birkaç enjeksiyonla uzun süreli profilaksi"]
                ]
            ),
            make_active_recall(
                "Hemostazı bozmadan trombozu önleme potansiyeli taşıdığı için yeni nesil araştırmaların odak noktası olan pıhtılaşma faktörü hangisidir?",
                "Faktör XIa (ve Faktör XIIa) faktörüdür.",
                "Kontakt aktivasyon kaskadının kanama riski düşük faktörü"
            )
        ]
    })

    # Slayt 100: [TEKRAR SAYFASI - CHECKPOINT 10]
    slides.append({
        "id": "k1-20-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Tromboz Patofizyolojisi Büyük Özeti",
        "section": "Tedavi İlkeleri ve Büyük Özet",
        "slideNumber": 100,
        "narrative": (
            "Tebrikler! Kurul 1 Ders 20 Tromboz Patofizyolojisi destesini başarıyla tamamladınız. "
            "Bu son checkpoint sayfasında hemostaz ile tromboz arasındaki hassas dengeyi, "
            "Virchow triyadının üçayağını, antitrombotik tedavi ilkelerini ve altın standart tanı yöntemlerini "
            "3 adet kapsamlı aktif hatırlama kartı üzerinden pekiştirerek dersi nihayete erdiriyoruz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-20-cp10-1",
                "Virchow triyadının 3 temel bileşeni nelerdir ve arteriyel ile venöz trombozda hangileri ön plandadır?",
                "1. Endotel hasarı (arteriyel trombozda 1 numaralı faktör), 2. Anormal kan akımı (türbülans arterde, staz vende baskın), 3. Hiperkoagülabilite (venöz trombozda baskın bileşen).",
                "Virchow'un üç ayağı ve vasküler yatak ayrımı",
                "Tromboz Büyük Özeti"
            ),
            make_flashcard(
                "fc-k1-20-cp10-2",
                "Antiplatelet, antikoagülan ve trombolitik ilaçların patofizyolojik etki mekanizması farkı nedir?",
                "Antiplateletler trombosit adezyon ve agregasyonunu engeller (arteriyel pıhtıda anahtar). Antikoagülanlar pıhtılaşma faktörlerini baskılayarak yeni fibrin ağını durdurur. Trombolitikler ise oluşmuş pıhtının fibrin iskeletini plazminle doğrudan eritir.",
                "Trombosit, fibrin kaskadı ve pıhtı lizisi farkı",
                "Farmakoterapi İlkeleri"
            ),
            make_flashcard(
                "fc-k1-20-cp10-3",
                "DVT ve Pulmoner Tromboemboli tanısında D-Dimer'in ve altın standart görüntüleme yöntemlerinin yeri nedir?",
                "D-Dimer yüksek negatif prediktif değeriyle hastalığı dışlamada kullanılır. Kesin tanı için DVT'de Kompresyon Doppler Ultrasonografi (kollabe olmayan ven), Pulmoner Embolide ise BT Pulmoner Anjiyografi (dolum defekti) altın standarttır.",
                "Dışlama biyobelirteci ve altın standart radyoloji",
                "Tanı Algoritmaları"
            )
        ]
    })

    return slides
