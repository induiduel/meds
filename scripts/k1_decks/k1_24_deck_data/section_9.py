# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 9: Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS) (Slayt 81 - 90)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # Slayt 81: Hücresel Metabolik Çöküş ve Mitokondriyal Disfonksiyon
    slides.append({
        "id": "k1-24-s81",
        "title": "Hücresel Metabolik Çöküş ve Mitokondriyal Disfonksiyon",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 81,
        "narrative": (
            "Septik şokta doku hasarının nihai boyutu, hücrelerin biyokimyasal enerji fabrikası olan mitokondrilerin "
            "işlevsizleşmesiyle ortaya çıkar: "
            "1. **Sitopatik Hipoksi Kavramı:** Dokulara mikrovasküler düzeyde yeterli oksijen ulaştırılsa bile hücreler "
            "bu oksijeni kullanamaz; bu tabloya 'sitopatik veya hücresel hipoksi' denir. "
            "2. **Mitokondriyal Toksisite:** Aşırı üretilen nitrik oksit (NO), peroksinitrit radikalleri ve proinflamatuar sitokinler, "
            "mitokondriyal elektron taşıma zinciri enzim komplekslerini (özellikle Kompleks I ve IV) doğrudan inaktive eder. "
            "3. **Enerji Çöküşü:** Oksidatif fosforilasyon durur; hücresel ATP seviyeleri hızla tükenir. "
            "Membran potansiyelleri kaybolur, mitokondri membran geçirgenlik geçiş gözeneği (MPTP) açılarak sitokrom c sitoplazmaya sızar "
            "ve apoptoz ile hücre nekrozu tetiklenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_cloze(
                "Septik şokta dokularda oksijen bulunmasına rağmen mitokondriyal disfonksiyon nedeniyle oksijenin tüketilememesi durumuna sitopatik hipoksi denir.",
                "sitopatik hipoksi",
                "Hücresel düzeyde oksijen kullanım bozukluğunu tanımlayan patolojik kavram"
            ),
            make_micro_quiz(
                "Septik şokta hücresel ATP üretiminin durmasına ve sitopatik hipoksiye yol açan temel organel disfonksiyonu hangisidir?",
                {
                    "A": "Mitokondriyal oksidatif fosforilasyon çöküşü",
                    "B": "Granüllü endoplazmik retikulum hipertrofisi",
                    "C": "Golgi aygıtında vezikül tomurcuklanması",
                    "D": "Peroksizom enzimlerinin aşırı aktivasyonu",
                    "E": "Lizozomal enzim üretiminin inhibisyonu"
                },
                "A",
                {
                    "A": "Doğrudur; mitokondrilerin sitokin ve NO ile zehirlenmesi elektron taşıma zincirini durdurur ve enerji çöküşü yaratır.",
                    "B": "Yanlış; retikulum hasarlanır ve şişer, hipertrofi olmaz.",
                    "C": "Yanlış; golgi disfonksiyonu primer enerji çöküşü yapmaz.",
                    "D": "Yanlış; peroksizom hasarı şokun primer nedeni değildir.",
                    "E": "Yanlış; lizozom enzimleri serbest kalarak otofaji ve nekroza neden olur."
                }
            )
        ]
    })

    # Slayt 82: Laktik Asidoz Patofizyolojisi ve Klinik Anlamı
    slides.append({
        "id": "k1-24-s82",
        "title": "Laktik Asidoz Patofizyolojisi ve Klinik Anlamı",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 82,
        "narrative": (
            "Laktik asidoz, şok hastasının hücresel perfüzyon yetersizliğini yansıtan en değerli biyokimyasal belirteçtir: "
            "1. **Anaerobik Glikoliz Aktivasyonu:** Oksidatif fosforilasyon durduğunda hücreler zorunlu olarak glikolize yönelir. "
            "Pirüvat, mitokondride asetil-KoA'ya dönüştürülemediği için laktat dehidrogenaz (LDH) enzimiyle laktata çevrilir. "
            "2. **Karaciğer Klirensinin Bozulması:** Normal şartlarda kanda biriken laktat karaciğerde Cori döngüsüyle glukoneogeneze "
            "aktarılır. Ancak septik şokta sentrilobüler karaciğer iskemisi nedeniyle laktat klirensi durur. "
            "3. **Asidozun Vasküler Etkisi:** Kanda biriken laktik asit arteriyel pH'ı düşürür. Asidoz; miyokard kontraktilitesini zayıflatır, "
            "periferik damarların katekolaminlere (adrenalin/noradrenalin) yanıtını köreltir ve vazodilatasyonu derinleştirir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Laktik Asidoz Gelişim ve Kötüleşme Zinciri",
                [
                    "1. Hücresel Hipoksi: Oksijen yetersizliği ve mitokondri hasarı ile aerobik solunumun durması",
                    "2. Pirüvat Birikimi: Glikolizin anaerobik yöne sapması ve LDH ile laktata dönüşüm",
                    "3. Hepatik Klirens Kaybı: Karaciğer perfüzyon bozukluğu nedeniyle Cori döngüsünün durması",
                    "4. Vasküler Yanıtsızlık: Düşük pH'ın miyokard kontraktilitesini ve katekolamin duyarlılığını felç etmesi"
                ]
            ),
            make_cloze(
                "Şokta doku hipoperfüzyonunu ve anaerobik glikoliz artışını gösteren temel serum biyokimyasal parametresi laktat konsantrasyonudur.",
                "laktat",
                "Pirüvatın oksijensiz ortamda indirgendiği metabolik belirteç"
            )
        ]
    })

    # Slayt 83: İnsülin Direnci ve Stres Hiperglisemisi
    slides.append({
        "id": "k1-24-s83",
        "title": "İnsülin Direnci ve Stres Hiperglisemisi",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 83,
        "narrative": (
            "Septik şoktaki metabolik bozuklukların bir diğer yüzü, diyabet öyküsü olmayan hastalarda bile gelişen "
            "derin stres hiperglisemisidir: "
            "1. **Kontr-regülatuvar Hormon Artışı:** Şok stresi hipotalamo-hipofizer-adrenal aksı ve sempatik sistemi aşırı uyarır. "
            "Kanda kortizol, glukagon, büyüme hormonu ve katekolamin düzeyleri tavan yapar; hepatik glikojenoliz ve glukoneogenez hızlanır. "
            "2. **Periferik İnsülin Direnci:** Proinflamatuar sitokinler (özellikle TNF-alfa ve IL-1), kas ve yağ dokusundaki insülin reseptör "
            "substratlarını (IRS-1) serin fosforilasyonu ile inaktive eder. Glukoz taşıyıcısı **GLUT-4**'ün hücre zarına yerleşimi bloke olur. "
            "3. **İmmün Baskılama:** Hiperglisemi, nötrofillerin fagositoz yeteneğini ve mikrobisidal aktivitesini felç eder; "
            "enfeksiyonun kontrol altına alınmasını imkansızlaştırır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Şokta Stres Hiperglisemisinin Hormonal ve Moleküler Mekanizması",
                ["Mekanizma Bileşeni", "Etkilenen Hormon / Molekül", "Hedef Organ / Dokudaki Etki", "Klinik Patolojik Sonuç"],
                [
                    ["Hormonal Aşırı Üretim", "Kortizol, Glukagon, Katekolaminler", "Karaciğerde glikojenoliz ve glukoneogenez", "Masif glukoz üretimi"],
                    [
                        "Reseptör İnhibisyonu",
                        "TNF-alfa ve IL-1 sitokinleri",
                        {"text": "İnsülin reseptörü ve GLUT-4 blokajı", "isMasked": True, "hint": "Çizgili kas ve yağ dokusunda glukoz giriş kapısının engellenmesi"},
                        "Periferik insülin direnci"
                    ],
                    ["İmmün İnhibisyon", "Aşırı Hücre Dışı Glukoz", "Nötrofil fagositoz ve kemotaksisi", "Fagositik işlev yetmezliği"]
                ]
            ),
            make_active_recall(
                "Septik şokta sitokinlerin çizgili kas ve yağ dokusunda insülin uyarılı hücre içine glukoz alımını engelleyen temel taşıyıcı protein hangisidir?",
                "GLUT-4 glukoz taşıyıcısıdır.",
                "İnsülin bağımlı dokularda yer alan dördüncü tip glukoz transporterı"
            )
        ]
    })

    # Slayt 84: Adrenal Yetmezlik ve Waterhouse-Friderichsen Sendromu
    slides.append({
        "id": "k1-24-s84",
        "title": "Adrenal Yetmezlik ve Waterhouse-Friderichsen Sendromu",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 84,
        "narrative": (
            "Septik şok sürecinde böbrek üstü bezleri (sürrenal bezler) çift taraflı hemorajik nekroza uğrayabilir: "
            "1. **Klinik Tanım:** Şiddetli bakteriyemi (özellikle **Neisseria meningitidis / meningokoksemi**, bazen Pseudomonas veya "
            "Streptococcus pneumoniae) zemininde gelişen iki taraflı masif adrenal hemoraji tablosuna **Waterhouse-Friderichsen Sendromu** denir. "
            "2. **Patogenez:** Endotel hasarı ve sistemik DİK mikrosirkülasyonda yaygın fibrin mikrotrombüsleri oluşturur. "
            "Zengin vaskülarize adrenal korteks sinüzoidleri tromboze olur; ardından gelişen enfarktüs masif kanamalı nekrozla sonuçlanır. "
            "3. **Akut Primer Adrenal Kriz:** Adrenal korteks hormonları (kortizol ve aldosteron) sentezlenemez. "
            "Kortizol eksikliği vazomotor tonusun sürdürülmesini engeller; vazopressörlere tamamen yanıtsız derin hipotansiyon ve ölüm gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Adrenal Bezlerin Şoktaki Dönüşümü",
                "Normal / Kompanse Adrenal Yanıt",
                "Lipid yüklü sarı korteks hücreleri, masif kortizol sentezi ve vasküler tonusun idamesi",
                "Waterhouse-Friderichsen Sendromu",
                "Bilateral masif adrenal hemorajik nekroz, lipid tükenmesi ve akut kortikosteroid çöküşü"
            ),
            make_micro_quiz(
                "Özellikle Neisseria meningitidis enfeksiyonu zemininde gelişen, iki taraflı sürrenal bez kanamalı nekrozu ve akut primer adrenal yetmezlikle seyreden tablo hangisidir?",
                {
                    "A": "Waterhouse-Friderichsen Sendromu",
                    "B": "Sheehan Sendromu",
                    "C": "Conn Sendromu",
                    "D": "Cushing Hastalığı",
                    "E": "Schmidt Sendromu"
                },
                "A",
                {
                    "A": "Doğrudur; meningokoksemiye bağlı bilateral adrenal hemoraji ve akut kriz Waterhouse-Friderichsen sendromudur.",
                    "B": "Yanlış; Sheehan doğum sonrası hipofiz iskemik nekrozudur.",
                    "C": "Yanlış; Conn primer hiperaldosteronizmdir.",
                    "D": "Yanlış; Cushing kortizol fazlalığıdır.",
                    "E": "Yanlış; Schmidt otoimmün poliglandüler yetmezliktir."
                }
            )
        ]
    })

    # Slayt 85: Şok Akciğeri: Diffüz Alveoler Hasar (DAD) ve ARDS
    slides.append({
        "id": "k1-24-s85",
        "title": "Şok Akciğeri: Diffüz Alveoler Hasar (DAD) ve ARDS",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 85,
        "narrative": (
            "Şok tablosunda akciğerler hedef organların başında gelir; gelişen klinik patolojik tabloya **Şok Akciğeri** veya "
            "**Akut Respiratuar Distres Sendromu (ARDS)** adı verilir: "
            "1. **Morfolojik Zemin (Diffüz Alveoler Hasar - DAD):** Alveoler kapiller endotel ve Tip I pnömosit hücreleri sitokinler "
            "ve aktive nötrofillerin proteazlarıyla parçalanır. "
            "2. **Hiyalin Membranlar:** Kapillerlerden alveol boşluğuna fibrin ve protein zengin eksüda akar. Bu eksüda nekrotik "
            "epitel artıklarıyla birleşerek alveol duvarlarını pembe camsı tabakalar halinde kaplar (**hiyalin membranlar**). "
            "3. **Surfaktan Kaybı ve Atelektazi:** Tip II pnömositlerin zedelenmesiyle sürfaktan üretimi durur; alveoller kollabe olur. "
            "Oksijen difüzyon bariyeri kalınlaşır; ventilasyon-perfüzyon uyumsuzluğu sonucu mekanik ventilatörle bile düzeltilemeyen "
            "**refrakter hipoksemi** tablosu ortaya çıkar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Şok Akciğeri (ARDS / DAD) Histopatolojik Gelişimi",
                [
                    "1. Nötrofil Sekestrasyonu: Akciğer kapillerlerinde lökositlerin birikmesi ve proteolitik enzim salınımı",
                    "2. Alveolokapiller Bariyer Yıkımı: Endotel ve Tip I pnömosit nekrozu ile masif geçirgenlik artışı",
                    "3. Eksüdasyon ve Hiyalin Membran: Fibrin zengin sıvının alveol içini doldurması ve pembe membran oluşumu",
                    "4. Refrakter Hipoksemi: Alveoler kollaps, sürfaktan kaybı ve oksijen difüzyonunun tamamen tıkanması"
                ]
            ),
            make_cloze(
                "Şok akciğeri (ARDS) histopatolojisinde alveol duvarlarını sıvayan ve fibrin ile nekrotik epitel döküntülerinden oluşan pembe yapılara hiyalin membran denir.",
                "hiyalin membran",
                "Diffüz alveoler hasarın en karakteristik histopatolojik bulgusu"
            )
        ]
    })

    # Slayt 86: Şok Böbreği: İskemik Akut Tübüler Nekroz (ATN)
    slides.append({
        "id": "k1-24-s86",
        "title": "Şok Böbreği: İskemik Akut Tübüler Nekroz (ATN)",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 86,
        "narrative": (
            "Böbrekler kardiyak debinin yaklaşık dörtte birini alan ve hipoperfüzyona son derece duyarlı olan organlardır: "
            "1. **Patoloji Tanımı:** Şokta renal arteriyoler vazokonstriksiyon ve hipotansiyona bağlı gelişen akut tübüler epitel nekrozuna "
            "**Şok Böbreği veya İskemik Akut Tübüler Nekroz (ATN)** denir. "
            "2. **Duyarlı Segmentler:** İskemiye en duyarlı tübül segmentleri metabolik aktivitesi ve oksijen tüketimi en yüksek olan "
            "**proksimal kıvrıntılı tübüller** ile Henle kulpunun çıkan kalın koludur. "
            "3. **Tübüler Tıkanma:** Nekroza uğrayan tübül epitel hücreleri bazal membrandan dökülerek lümende toplanır; Tamm-Horsfall "
            "proteiniyle birleşerek **kahverengi granüler silendirleri** oluşturur. "
            "4. **Klinik Sonuç:** Tübül içi obstrüksiyon ve geri sızıntı sonucu glomerüler filtrasyon durur; hastada oligüri veya anüri ile "
            "hızla yükselen kan üre azotu (BUN) ve kreatinin düzeyleri izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İskemik Akut Tübüler Nekroz (Şok Böbreği) Histopatolojik Özellikleri",
                ["Anatomik Bölge", "İskemiye Duyarlılık Düzeyi", "Tipik Morfolojik Hasar", "Fonksiyonel Bozukluk"],
                [
                    ["Glomerüller", "Düşük / Korunmuş", "Fibrin mikrotrombüsleri (DİK varsa)", "GFR'de hidrostatik düşüş"],
                    [
                        "Proksimal Tübüller",
                        "En Yüksek",
                        {"text": "Fırçamsı kenar kaybı ve epitel nekrozu", "isMasked": True, "hint": "Yüksek metabolik enerjili epitelin lümene dökülmesi"},
                        "Geri emilim kapasitesinin çökmesi"
                    ],
                    ["Henle Kalın Çıkan Kol", "Yüksek", "Segmental epitel soyulması", "Konsantrasyon yeteneğinin kaybı"],
                    ["Toplayıcı Kanallar", "Orta / Pasif", "Kahverengi granüler silendirler", "Lüminal obstrüksiyon ve anüri"]
                ]
            ),
            make_active_recall(
                "Şok böbreğinde dökülen nekrotik epitel hücrelerinin lümende Tamm-Horsfall proteiniyle birleşmesi sonucu idrarda görülen patognomonik silendir hangisidir?",
                "Kahverengi granüler silendirlerdir (Çamur silendirleri).",
                "İskemik ATN idrar mikroskopisinde karakteristik mikroskobik çökelti"
            )
        ]
    })

    # Slayt 87: Karaciğer, Gastrointestinal Sistem ve Beyin Hasarı
    slides.append({
        "id": "k1-24-s87",
        "title": "Karaciğer, Gastrointestinal Sistem ve Beyin Hasarı",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 87,
        "narrative": (
            "Şok sürecinde çoklu organ yetmezliği (MODS) diğer hayati parankimal organları da yıkıma uğratır: "
            "1. **Karaciğer:** Hepatik lobülün periferi portal ven ve hepatik arterle iyi beslenirken, santral ven çevresindeki hepatositler "
            "oksijenden en fakir bölgedir. Şokta santral ven çevresinde **sentrilobüler nekroz** gelişir; serum transaminazları (AST/ALT) "
            "hızla yükselir ve kolestaz izlenir. "
            "2. **Gastrointestinal Sistem:** Mukozal hipoperfüzyon iskemik enteropatiye ve yaygın yüzeysel erezyonlara (stres ülserleri) "
            "yol açar. Bağırsak mukozal bariyeri yıkıldığında lümen içindeki bakteriler ve endotoksinler dolaşıma sızar (bakteriyel translokasyon). "
            "3. **Beyin:** Hipotansiyon uzadığında **hipoksik-iskemik ensefalopati** gelişir. Özellikle serebral korteksin 3., 5. ve 6. tabakalarında "
            "**kortikal laminer nekroz** ve Sommer sektöründe (hipokampus) piramidal hücre ölümü görülür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Şok tablosundaki bir hastada ani karaciğer transaminaz fırlaması (AST/ALT > 3000 U/L), gastrointestinal kanama ve koma tablosu gelişiyor.",
                [
                    {
                        "text": "Sentrilobüler hepatik nekroz, iskemik mukozal stres ülseri ve hipoksik ensefalopatiyi kapsayan MODS tanısıyla yoğun parankimal destek planlanması",
                        "isCorrect": True,
                        "explanation": "Mükemmel. Şok karaciğerde sentrilobüler nekroza, midede stres ülserlerine ve beyinde hipoksik nekroza yol açarak MODS tablosunu derinleştirir."
                    },
                    {
                        "text": "Tabloyu sadece akut viral hepatit B enfeksiyonu olarak yorumlayıp izole antiviral tedavi başlamak",
                        "isCorrect": False,
                        "explanation": "Hatalı ve yetersiz. Şokta gelişen ani transaminaz artışı iskemik hepatite ('şok karaciğeri') bağlıdır ve sistemik resüsitasyon gerektirir."
                    }
                ]
            ),
            make_cloze(
                "Şok karaciğerinde oksijene en uzak olan hepatik lobül bölgesinde gelişen karakteristik nekroza sentrilobüler nekroz denir.",
                "sentrilobüler nekroz",
                "Santral ven çevresindeki Zon 3 hepatositlerinin iskemik ölümü"
            )
        ]
    })

    # Slayt 88: Miyokard Depresyonu ve Kalp Yetmezliği
    slides.append({
        "id": "k1-24-s88",
        "title": "Miyokard Depresyonu ve Kalp Yetmezliği: Şokun Kısır Döngüsü",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 88,
        "narrative": (
            "Erken dönem hiperdinamik septik şokta kardiyak output normal veya yüksek olabilirken, sürecin uzamasıyla miyokard çöker: "
            "1. **Miyokard Deprese Edici Faktörler:** Dolaşımda aşırı miktarda bulunan **TNF-alfa**, **IL-1** ve nitrik oksit, "
            "kardiyomiyositlerin kalsiyum taşıma kanallarını ve aktin-miyozin çapraz köprülerini doğrudan felç eder. "
            "2. **Koroner Hipoperfüzyon:** Sistemik arteriyel diyastolik kan basıncının kritik seviyenin altına inmesi, koroner arterlerin "
            "diyastolik dolumunu bozar. Miyokard dokusu derin iskemiye sürüklenir; subendokardiyal hemorajiler ve miyosit nekrozu gelişir. "
            "3. **Klinik Dönüşüm:** Sol ventrikül ejeksiyon fraksiyonu düşer, kalp debisi çöker. Erken hiperdinamik 'sıcak şok' fazı, "
            "terminal dönemde vazokonstriksiyon, soğuk ve nemli ekstremitelerle seyreden dekompanse 'soğuk şok' tablosuna dönüşür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Septik Şokta Miyokard Fonksiyonu",
                "Erken Faz (Hiperdinamik)",
                "Düşük periferik direnç, taşikardi, artmış kardiyak debi ve kompanse ejeksiyon fraksiyonu",
                "Geç Faz (Miyokard Depresyonu)",
                "Sitokin aracılı kontraktilite felci, subendokardiyal nekroz, düşen debi ve dekompanse arrest"
            ),
            make_micro_quiz(
                "Septik şokun geç döneminde kardiyak outputun çökmesine ve miyokard kontraktilitesinin doğrudan deprese olmasına yol açan temel sitokinler hangileridir?",
                {
                    "A": "TNF-alfa ve İnterlökin-1 (IL-1)",
                    "B": "İnterlökin-4 ve İnterlökin-5",
                    "C": "TGF-beta ve Eritropoietin",
                    "D": "İnterlökin-10 ve IL-37",
                    "E": "G-CSF ve Trombopoietin"
                },
                "A",
                {
                    "A": "Doğrudur; TNF-alfa ve IL-1 miyokardiyal kalsiyum dinamiklerini bozarak doğrudan miyokard depresan faktör olarak işlev görür.",
                    "B": "Yanlış; IL-4 ve 5 eozinofilik ve alerjik yolak sitokinleridir.",
                    "C": "Yanlış; TGF-beta fibrozis sitokinidir.",
                    "D": "Yanlış; bunlar antienflamatuar mediyatörlerdir.",
                    "E": "Yanlış; büyüme faktörleridir."
                }
            )
        ]
    })

    # Slayt 89: Checkpoint 9
    slides.append({
        "id": "k1-24-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Septik Şokun Metabolik ve Organ Düzeyinde Patolojisi (MODS)",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 89,
        "narrative": (
            "Bu dokuzuncu kontrol noktasında, şokun metabolik ve organ düzeyindeki hasar mekanizmalarını pekiştiriyoruz: "
            "1. **Sitopatik Hipoksi:** Mitokondriyal elektron taşıma zinciri felç olur; hücre içi ATP tükenir. "
            "2. **Laktik Asidoz:** Anaerobik glikoliz artar, karaciğer Cori döngüsü durur; kan pH'ı düşer ve miyokard baskılanır. "
            "3. **Stres Hiperglisemisi:** Kontr-regülatuvar hormonlar artar, TNF/IL-1 GLUT-4 kapılarını kapatır ve insülin direnci gelişir. "
            "4. **Waterhouse-Friderichsen:** Meningokoksemide iki taraflı sürrenal hemorajik nekrozu ve akut adrenal kriz tablosudur. "
            "5. **Şok Akciğeri (ARDS):** DAD, hiyalin membranlar, sürfaktan kaybı ve refrakter hipoksemi ile karakterizedir. "
            "6. **Şok Böbreği (ATN):** Proksimal tübül epitel nekrozu, kahverengi granüler silendirler ve oligüri gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-24-fc-s89-1",
                "Meningokoksik sepsis zemininde gelişen bilateral böbrek üstü bezi hemorajik enfarktüsü ve akut primer yetmezlik tablosuna ne ad verilir?",
                "Waterhouse-Friderichsen sendromu denir.",
                "Sürrenal korteks bezlerinin iki taraflı kanamalı doku erimesi tablosu",
                "Waterhouse-Friderichsen Sendromu"
            ),
            make_flashcard(
                "k1-24-fc-s89-2",
                "Şok akciğeri (ARDS) histopatolojisinde alveol yüzeylerini kaplayan pembe protein-fibrin katmanlarına verilen mikroskopik ad nedir?",
                "Hiyalin membran yapılarıdır.",
                "Eksüda ve dökülen epitel artıklarının meydana getirdiği camsı örtü tabakası",
                "Hiyalin Membranlar"
            ),
            make_flashcard(
                "k1-24-fc-s89-3",
                "Şok böbreğinde iskemiye bağlı epitel nekrozunun en ağır görüldüğü proksimal tübüllerde dökülen hücrelerin idrarda oluşturduğu çökelti nedir?",
                "Kahverengi çamur granüllü silendirlerdir.",
                "Lümende Tamm-Horsfall proteiniyle birleşen tübüler debris kümeleri",
                "Kahverengi Granüler Silendirler"
            )
        ],
        "interactiveElements": [
            make_table(
                "Şok Organ Hasarları ve Patolojik Bulguları",
                ["Hedef Organ", "Karakteristik Patolojik Lezyon", "Mikroskobik Anahtar Bulgu", "Klinik Yansıması"],
                [
                    ["Akciğer (ARDS)", "Diffüz Alveoler Hasar (DAD)", "Pembe hiyalin membranlar", "Refrakter hipoksemi"],
                    [
                        "Böbrek (ATN)",
                        "İskemik Akut Tübüler Nekroz",
                        {"text": "Kahverengi granüler silendirler", "isMasked": True, "hint": "Tübül epitel döküntülerinin oluşturduğu mikroskobik lümen tıkacı"},
                        "Oligüri, azotemi, anüri"
                    ],
                    ["Sürrenal Bezler", "Waterhouse-Friderichsen", "Bilateral hemorajik nekroz", "Vazopressöre yanıtsız hipotansiyon"],
                    ["Karaciğer", "Sentrilobüler nekroz", "Zon 3 hepatosit lizisi", "Transaminaz artışı, sarılık"],
                    ["Beyin", "Kortikal laminer nekroz", "Sommer sektörü piramidal hücre ölümü", "Koma, iskemik ensefalopati"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki organ ve şok histopatolojisi eşleştirmelerinden hangisi YANLIŞTIR?",
                {
                    "A": "Akciğer - Diffüz Alveoler Hasar ve hiyalin membranlar",
                    "B": "Böbrek - Proksimal tübül iskemik nekrozu ve granüler silendirler",
                    "C": "Sürrenal bez - Bilateral hemorajik nekroz (Waterhouse-Friderichsen)",
                    "D": "Karaciğer - Portal alanlarda safra kanalı hiperplazisi ve granülomlar",
                    "E": "Beyin - Kortikal laminer nekroz ve hipoksik ensefalopati"
                },
                "D",
                {
                    "A": "Doğrudur; ARDS tablosunda DAD ve hiyalin membranlar görülür.",
                    "B": "Doğrudur; iskemik ATN tablosudur.",
                    "C": "Doğrudur; sürrenal hemoraji gelişir.",
                    "D": "YANLIŞTIR; Şok karaciğerinde portal granülom DEĞİL, santral ven çevresinde SENTRİLOBÜLER NEKROZ görülür.",
                    "E": "Doğrudur; hipoksik iskemik ensefalopati gelişir."
                }
            )
        ]
    })

    # Slayt 90: Bölüm Özeti: Organ Patolojisinden Şokun Evreleri ve Büyük Senteze Geçiş
    slides.append({
        "id": "k1-24-s90",
        "title": "Bölüm Özeti: Organ Patolojisinden Şokun Evreleri ve Büyük Senteze Geçiş",
        "section": "Septik Şokta Metabolik Bozukluklar ve Çoklu Organ Yetmezliği (MODS)",
        "slideNumber": 90,
        "narrative": (
            "Çoklu organ yetmezliği (MODS), şok tablosunun kontrol altına alınamadığında ulaştığı son aşamadır: "
            "1. **Sistemik Yıkım Bütünlüğü:** Hücresel mitokondri disfonksiyonu, laktik asidoz, bilateral sürrenal yetmezlik, "
            "akciğerde ARDS, böbrekte ATN ve karaciğerde sentrilobüler nekroz birbirini besleyen ölümcül bir kısır döngü oluşturur. "
            "2. **Zaman Penceresi:** Şok bir anda irreversibl hale gelmez; belirli dinamik evrelerden geçerek ilerler. "
            "Erken evrede hekimin doğru müdahalesi hastayı hayata döndürürken, geç evrede ölüm kaçınılmazdır. "
            "3. **Son Bölüme Köprü:** Son bölümümüzde (Bölüm 10) şokun klinik evrelerini (ilerlemeyen, ilerleyici ve geri dönüşümsüz evre), "
            "otopsi morfolojisini, Robbins patoloji spotlarını ve acil resüsitasyon prensiplerini inceleyerek desteyi tamamlayacağız."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Emboli, Enfarktüs ve Şok (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Şokun Klinik Seyri ve Dönüm Noktaları",
                "Reversibl Faz (Erken Müdahale Edilebilir)",
                "Kompansatuar vazokonstriksiyon, oligüri, erken laktat artışı ve organ hasarının henüz sınırlandırılabilir olması",
                "İrreversibl Faz (MODS ve Hücresel Ölüm)",
                "ARDS, anürik ATN, koma, adrenal nekroz, miyokard çöküşü ve resüsitasyona yanıtsız ölüm"
            ),
            make_active_recall(
                "Şok hastasında birden fazla organ sisteminin aynı anda fonksiyonel çöküşe uğraması tablosuna verilen genel klinik ad nedir?",
                "Çoklu Organ Yetmezliği Sendromu (MODS).",
                "Multiorgan disfonksiyon sendromunun tıbbi kısaltması"
            )
        ]
    })

    return slides
