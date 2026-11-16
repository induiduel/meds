# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-17-s91",
        "title": "Cinsel Partner Tedavisi ve 'Ping-Pong' Enfeksiyonu Önleme İlkeleri",
        "content": "Cinsel yolla bulaşan bir enfeksiyonun başarılı tedavisinde en kritik halka cinsel partnerin eşzamanlı yönetimidir (Sınav Spotu):\n\n- **Ping-Pong Enfeksiyonu Nedir?**\n  - İndeks hastanın antibiyotikle tamamen iyileşmesi, ancak tedavi edilmemiş asemptomatik partnerinden etkeni tekrar alması ve kısır bir enfeksiyon-reenfeksiyon döngüsüne girmesidir.\n- **Son 60 Gün Kuralı:**\n  - Semptomların başlamasından veya laboratuvar tanısından önceki **son 60 gün** içinde hastayla cinsel teması olan tüm partnerler bilgilendirilmeli, klinik muayeneye çağrılmalı ve test sonuçları beklenmeksizin **ampirik olarak tedavi edilmelidir**.\n  - Son temas 60 günden daha eski ise en son cinsel partner tedavi kapsamına alınır.\n- **Hızlandırılmış Partner Terapisi (EPT - Expedited Partner Therapy):**\n  - Partnerin sağlık merkezine başvuramadığı durumlarda hekimin hastaya partneri için de reçete veya ilaç teslim etmesi yöntemidir (özellikle klamidya ve trikomoniyaziste yaygın kullanılır).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Partner Yönetimi ve Ping-Pong Döngüsünü Kırma Basamakları",
                [
                    "1. İndeks Hasta Tanısı: Hastada CYBE tespit edilir ve tam tedavi başlanır.",
                    "2. Partner İletişimi: Son 60 gün içindeki tüm cinsel temaslılar belirlenir.",
                    "3. Eşzamanlı Tedavi: Partnerler semptomsuz olsalar dahi ampirik tedaviye alınır.",
                    "4. Reenfeksiyonun Önlenmesi: Ping-pong bulaşı engellenerek toplum yayılımı kırılır."
                ]
            ),
            make_cloze(
                "CYBE saptanan bir hastada reenfeksiyonu ve ping-pong döngüsünü engellemek için son altmış gün içindeki tüm cinsel partnerler tedavi edilmelidir.",
                "altmış gün",
                "Cinsel temaslıların geriye dönük taranması gereken iki aylık kritik zaman aralığı"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-17-s92",
        "title": "Tedavi Süresince Cinsel Perhiz Kuralı: 7 Gün Cinsel İlişki Yasağı",
        "content": "CYBE tedavisinde ilaç verilmesi kadar hastaya cinsel perhiz kurallarının anlatılması da yaşamsaldır (Sınav Spotu):\n\n- **7 Gün Kesin Cinsel Perhiz Kuralı:**\n  - Tek doz rejim uygulanan hastalar (örn. Klamidya için Azitromisin 1 g, Gonore için Seftriakson 250 mg, Trikomoniyazis için Metronidazol 2 g) ilacı aldıktan sonra **tam 7 gün boyunca hiçbir şekilde cinsel ilişkide bulunmamalıdır**.\n  - Çok günlük tedavi rejimlerinde (örn. Doksisiklin 7 gün, Metronidazol 7 gün) ilaç kürü tamamen bitene kadar cinsel temas kesinlikle yasaktır.\n- **Kuralın Gerekçeleri:**\n  1. İlacın doku konsantrasyonuna ulaşıp mikroorganizmaları tamamen yok etmesi birkaç gün sürer; bu süreçte bulaştırıcılık devam eder.\n  2. Partnerin de eşzamanlı tedavi alması ve onun da 7 günlük süresini doldurması zorunludur.\n  3. İlaç alınır alınmaz girilen ilişkide enfeksiyon partnerler arasında gidip gelerek tedavi başarısızlığına yol açar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Tek Doz İlaç Alımı vs Bulaştırıcılığın Sona Ermesi",
                "İlaç Alındığı Gün (0. Gün)",
                "Hasta ilacı içmiş olsa da genital mukozada canlı mikroorganizma saçılımı devam etmektedir.",
                "7 Günlük Perhiz Sonu (7. Gün)",
                "Doku konsantrasyonu patojeni tamamen temizler; partnerin tedavisiyle birlikte güvenli döneme geçilir."
            ),
            make_quiz(
                "Üretrit tanısıyla tek doz azitromisin 1 g oral tedavi verilen bir hastaya cinsel aktiviteye yeniden ne zaman başlayabileceği konusunda verilmesi gereken en doğru tavsiye hangisidir?",
                [
                    {"key": "A", "text": "İlaç alındıktan sonra ve partnerinin tedavisi tamamlandıktan sonra en az 7 gün cinsel perhiz uygulamalıdır", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hem tek doz ilaçtan sonra hem de partnerin eşzamanlı tedavisi bitene kadar 7 gün cinsel perhiz kuralı mutlaktır."},
                    {"key": "B", "text": "İlacı içtikten 2 saat sonra kondomsuz ilişkiye girebilir", "isCorrect": False, "explanation": "Bulaştırıcılık devam eder, kesinlikle yasaktır."},
                    {"key": "C", "text": "Yalnızca idrar tahlili tamamen temizlenene kadar 1 ay beklenmelidir", "isCorrect": False, "explanation": "Standart perhiz süresi 7 gündür."},
                    {"key": "D", "text": "İlişki serbesttir, sadece sıcak su banyosu yapmalıdır", "isCorrect": False, "explanation": "Tıbbi dayanağı yoktur."}
                ]
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-17-s93",
        "title": "Gebelikte CYBE Tedavisi: Kontrendike İlaçlar ve Fetal Toksisite",
        "content": "Gebelikte meydana gelen CYBE'lerin tedavisinde fetal güvenlilik birincil önceliktir; birçok standart ilaç gebelerde kesinlikle kullanılamaz (Sınav Spotu):\n\n- **1. Tetrasiklinler ve Doksisiklin (KESİNLİKLE KONTRENDİKE):**\n  - Kemik ve diş kalsifikasyon bölgelerinde birikir.\n  - Fetal uzun kemik büyümesini geri dönüşümlü olarak baskılar.\n  - Bebek dişlerinde kalıcı hipoplazi ve **sarı-kahverengi kalıcı renk değişikliğine (diş diskolorasyonu)** neden olur.\n- **2. Florokinolonlar - Siprofloksasin, Ofloksasin, Levofloksasin (KONTRENDİKE):**\n  - Gelişmekte olan fetal eklem ve kıkırdak dokusunda kondrotoksisite ve kalıcı artropati riski taşır.\n- **3. Podofilotoksin ve Podofilin (KESİNLİKLE KONTRENDİKE):**\n  - Güçlü bir antimitotik (mikrotübül zehiri) ajandır; sistemik emilimle fetal anomalilere ve ölüme (teratojenite) yol açabilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["İlaç Grubu", "Kontrendike Olduğu Durum", "Fetal Toksisite / Teratojenik Mekanizma"],
                [
                    ["Doksisiklin / Tetrasiklin", "Gebelik ve Emzirme", "Kemik büyüme geriliği ve dişlerde kalıcı sarı-kahverengi lekelenme"],
                    ["Florokinolonlar (Sipro/Levo)", "Gebelik", "Fetal eklem kıkırdağı hasarı ve kalıcı artropati riski"],
                    ["Podofilotoksin", "Gebelik", "Antimitotik spindle zehirlenmesi, embriyotoksisite ve teratojenite"]
                ]
            ),
            make_quiz(
                "Gebelikte genital enfeksiyon tedavisinde tetrasiklin veya doksisiklin kullanımının kesinlikle yasaklanmasının başlıca fetal toksisite nedeni hangisidir?",
                [
                    {"key": "A", "text": "Fetal kemiklerde birikerek kemik gelişimini baskılaması ve dişlerde kalıcı sarı-kahverengi diskolorasyon yapması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Doksisiklin ve tetrasiklinler kalsiyum ile şelasyon yaparak fetal kemik ve diş tomurcuklarında kalıcı hasara ve lekelenmeye neden olur."},
                    {"key": "B", "text": "Bebekte konjenital sağırlık oluşturması", "isCorrect": False, "explanation": "Aminoglikozitlerin (örn. gentamisin, streptomisin) ototoksisitesidir."},
                    {"key": "C", "text": "Fetal kardiyak kapak kapanma kusuru yapması", "isCorrect": False, "explanation": "Tetrasiklinin klasik etkisi kemik ve diştir."},
                    {"key": "D", "text": "Plasentada kalsiyum birikimini sıfırlayarak düşüğe yol açması", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-17-s94",
        "title": "Gebelikte Güvenli Antibiyotikler ve Alternatif Rejimler",
        "content": "Gebelikte standart rejimlerin yerine güvenli alternatif antibiyotikler seçilmelidir (Sınav Spotu):\n\n- **Klamidya Enfeksiyonu:**\n  - Birinci tercih: **Azitromisin 1 g oral tek doz** (gebelikte son derece güvenlidir).\n  - Alternatif: **Amoksisilin 3 $\\times$ 500 mg oral, 7 gün** VEYA **Eritromisin baz 4 $\\times$ 500 mg, 7 gün**.\n  - Gebelerde doksisiklin verilemez! Tedaviden 3-4 hafta sonra mutlaka **kür kontrolü (NAAT ile test-of-cure)** yapılmalıdır.\n- **Gonore Enfeksiyonu:**\n  - **Seftriakson 250 mg İM tek doz** + **Azitromisin 1 g oral tek doz** (sefalosporinler gebelikte güvenlidir).\n- **Trikomoniyazis:**\n  - **Metronidazol 2 g oral tek doz** (CDC kılavuzuna göre gebeliğin tüm trimesterlerinde güvenle uygulanır).\n- **Sifilis:**\n  - **Benzatin Penisilin G** gebelikte tek kanıtlanmış güvenli ve konjenital sifilisi önleyen ajandır. Penisilin alerjisi varsa hasta desensitize edilerek mutlaka penisilinle tedavi edilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Gebede Klamidya: Doksisiklin (Yasak) vs Azitromisin (Güvenli)",
                "Doksisiklin (Gebe Dışı Standart)",
                "7 günlük standart klamidya ilacıdır; ancak teratojenik kemik/diş toksisitesi nedeniyle gebede KESİNLİKLE YASAKTIR.",
                "Azitromisin (Gebede Birinci Tercih)",
                "Tek doz 1 g oral uygulanır; gebelik kategorisi B'dir ve gebelikte klamidyanın ilk tercih ilacıdır."
            ),
            make_cloze(
                "Gebe bir kadında saptanan Chlamydia trachomatis enfeksiyonunun tedavisinde birinci tercih antibiyotik azitromisin tek doz 1 gramdır.",
                "azitromisin",
                "Doksisiklinin yasak olduğu gebelikte tercih edilen tek doz makrolid"
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-17-s95",
        "title": "Gebelikte Viral CYBE: Genital Herpes, HPV ve Doğum Şekli",
        "content": "Viral enfeksiyonların gebelikte yönetimi, yenidoğana bulaşın ve neonatal komplikasyonların önlenmesine odaklanır (Sınav Spotu):\n\n- **1. Gebelikte Genital Herpes ve Doğum Yönetimi:**\n  - Doğum eylemi başladığında hastanın genital bölgesinde **aktif vezikül/ülser** veya **prodromal semptomlar** varsa, bebeğin vajinal doğum sırasında enfekte sekresyonlarla temasını önlemek için **ACİL SEZARYEN DOĞUM ZORUNLUDUR**.\n  - Doğum anında lezyon veya prodrom yoksa vajinal doğum güvenle yaptırılabilir.\n  - Gebeliğinde herpes öyküsü olan kadınlara rekürrensi ve viral saçılımı önlemek için **36. gebelik haftasından itibaren doğuma kadar Asiklovir süpresyonu** başlanır.\n- **2. Gebelikte Kondiloma Akuminata (HPV):**\n  - Kondilomlar doğum kanalını fiziksel olarak tıkamadığı veya masif kanama riski yaratmadığı sürece sezaryen endikasyonu **DEĞİLDİR**; vajinal doğum yapılabilir.\n  - Tedavide Podofilotoksin yasaktır; hekim tarafından uygulanan **Kriyoterapi** veya **TCA** güvenle kullanılır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Gebelikte Genital Herpes Doğum Karar Algoritması",
                [
                    "1. 36. Hafta Süpresyonu: Rekürrensi önlemek için Asiklovir profilaksisi başlanır.",
                    "2. Doğum Eylemi Muayenesi: Vulva, vajina ve servikste aktif lezyon aranır.",
                    "3. Aktif Lezyon Varlığı: Aktif vezikül veya ülser varsa sezaryen doğum yapılır.",
                    "4. Aktif Lezyon Yokluğu: Genital kanal temiz ise güvenle vajinal doğum gerçekleştirilir."
                ]
            ),
            make_quiz(
                "Miadında doğum eylemi başlayan 39 haftalık gebe bir kadının genital muayenesinde vulvada çok sayıda ağrılı vezikülo-ülseratif lezyon saptanırsa en uygun yaklaşım hangisidir?",
                [
                    {"key": "A", "text": "Neonatal herpes enfeksiyonunu önlemek amacıyla acilen sezaryen ile doğum yaptırılmalıdır", "isCorrect": True, "explanation": "Doğru cevap A'dır: Aktif lezyon varlığında doğum kanalından geçerken bebeğe fatal neonatal herpes bulaşmasını önlemek için sezaryen şarttır."},
                    {"key": "B", "text": "Lezyonların üzerine podofilotoksin sürülüp vajinal doğum beklenmelidir", "isCorrect": False, "explanation": "Podofilotoksin teratojendir ve lezyonu hemen yok etmez."},
                    {"key": "C", "text": "Normal vajinal doğum yaptırılıp bebeğe aşı yapılmalıdır", "isCorrect": False, "explanation": "Vajinal yolla bulaş riski çok yüksektir, aşısı yoktur."},
                    {"key": "D", "text": "Hasta 2 hafta bekletilmelidir", "isCorrect": False, "explanation": "Doğum eylemi başlamıştır, bekletilemez."}
                ]
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-17-s96",
        "title": "Yenidoğanda CYBE Komplikasyonları ve Oftalmiya Neonatorum",
        "content": "Enfekte doğum kanalından geçen yenidoğan bebeklerde ciddi konjenital ve perinatal enfeksiyonlar meydana gelebilir (Sınav Spotu):\n\n- **1. Gonokokal Oftalmiya Neonatorum (Neisseria gonorrhoeae):**\n  - Doğumdan sonraki **ilk 2-5 gün içinde** başlar.\n  - Hiperakut, her iki gözden fışkırır tarzda bol cerahatli pürülan akıntı, şiddetli kemozis ve göz kapağı ödemi ile karakterizedir.\n  - Tedavi edilmezse saatler içinde korneayı eriterek delinme ve kalıcı körlüğe yol açar.\n  - **Rutin Profilaksi:** Tüm yenidoğanlara doğumdan hemen sonra her iki konjonktival keseye **Eritromisin %0.5 oftalmik pomat** sürülür.\n- **2. Klamidyal Oftalmiya Neonatorum (Chlamydia trachomatis):**\n  - Doğumdan **5-14 gün sonra** daha geç ortaya çıkar; mukopürülan akıntı yapar.\n  - Topikal pomatlara yanıtsızdır; klamidyal interstisyel pnömoni riskini de önlemek için **sistemik oral Eritromisin** ile tedavi edilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Özellik", "Gonokokal Konjonktivit", "Klamidyal Konjonktivit"],
                [
                    ["Başlangıç Zamanı", "Erken: Doğumdan sonraki 2-5. günler", "Geç: Doğumdan sonraki 5-14. günler"],
                    ["Klinik Şiddet", "Hiperakut, bol cerahatli püy, kornea körlüğü riski", "Subakut, mukopürülan akıntı"],
                    ["Profilaksiye Yanıt", "Doğumda topikal eritromisin pomat ile önlenir", "Topikal profilaksiye dirençlidir"],
                    ["Tedavi", "Sistemik Seftriakson İM/İV", "Sistemik oral Eritromisin (pnömoni riski)"]
                ]
            ),
            make_quiz(
                "Yenidoğan bir bebekte doğumdan 3 gün sonra gelişen hiperakut, her iki gözden bol cerahatli pürülan akıntı ve kornea perforasyonu riski taşıyan enfeksiyonun en olası etkeni hangisidir?",
                [
                    {"key": "A", "text": "Neisseria gonorrhoeae", "isCorrect": True, "explanation": "Doğru cevap A'dır: İlk 2-5 günde gelişen hiperakut pürülan konjonktivitin (oftalmiya neonatorum) klasik etkeni Neisseria gonorrhoeae'dir."},
                    {"key": "B", "text": "Chlamydia trachomatis", "isCorrect": False, "explanation": "Klamidya daha geç (5-14. günler) ortaya çıkar."},
                    {"key": "C", "text": "Staphylococcus aureus", "isCorrect": False, "explanation": "Gonokok hiperakut körlük yapan ana etkendir."},
                    {"key": "D", "text": "Candida albicans", "isCorrect": False, "explanation": "Pamukçuk yapar, konjonktivit yapmaz."}
                ]
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-17-s97",
        "title": "CYBE Tarama Prensipleri ve HIV / Hepatit B Koinfeksiyonu",
        "content": "Cinsel yolla bulaşan enfeksiyonlar hiçbir zaman izole bir hastalık olarak değerlendirilmemelidir (Sınav Spotu):\n\n- **Sinerjistik HIV Bulaş Riski:**\n  - Genital ülser oluşturan etkenler (HSV-2, Şankroid, Sifilis) mukozal bariyeri yıkar ve CD4+ T lenfositleri bölgeye çeker.\n  - Akıntı yapan enfeksiyonlar (Gonore, Klamidya, Trikomoniyazis) genital mukozada yoğun enflamasyona yol açar.\n  - Bu durum HIV virüsünün hem bulaşma hem de karşı tarafa aktarılma riskini **3 ila 10 kat artırır**.\n- **Bir CYBE Saptandığında Rutin Tarama Paketi:**\n  1. **HIV Antijen/Antikor (4. Kuşak ELISA) Testi** (tanı anında ve 3. ayda kontrol).\n  2. **Sifilis Serolojisi (VDRL/RPR ve TPHA/FTA-ABS)**.\n  3. **Hepatit B ve Hepatit C Göstergeleri (HBsAg, Anti-HBc IgM, Anti-HCV)**.\n- **Primer Korunma:** Hepatit B seronegatif tüm bireylere HBV aşısı, uygun yaş gruplarına HPV aşısı yapılmalı ve bariyer korunma (kondom) mutlak önerilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "İzole CYBE Teşhisi vs Bütüncül Tarama Paketi",
                "Yalnızca Şikayete Yönelik Tedavi",
                "Örn. gonoreyi tedavi edip hastayı göndermek; altta yatan asemptomatik klamidya, sifilis veya HIV'in atlanmasına yol açar.",
                "Bütüncül CYBE Tarama Paketi",
                "Her CYBE hastasında HIV, Sifilis, HBV ve HCV taranır; partnerler eşzamanlı tedavi edilerek zincir kırılır."
            ),
            make_cloze(
                "Genital ülser veya akıntı ile başvuran bir CYBE hastasında mukozal hasar ve enflamasyon nedeniyle HIV bulaş riski belirgin şekilde artar.",
                "HIV",
                "CYBE zemininde bulaşması 3-10 kat kolaylaşan retrovirüs"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-17-s98",
        "title": "Klinik Vaka Entegrasyonu: DSÖ Sendromik Yönetim Algoritması",
        "content": "Laboratuvar olanaklarının kısıtlı olduğu veya sonuçların günlerce gecikeceği durumlarda DSÖ'nün **sendromik yaklaşımı** hayat kurtarır (Sınav Spotu):\n\n- **1. Üretral Akıntı Sendromu:**\n  - Hasta pürülan veya mukoid üretral akıntı ve dizüri ile başvurur.\n  - Beklemeden hem Gonoreyi hem Klamidyayı kapsayan rejim verilir: **Seftriakson 250 mg İM tek doz + Doksisiklin 2 $\\times$ 100 mg oral 7 gün** (veya Azitromisin 1 g tek doz).\n- **2. Vajinal Akıntı Sendromu:**\n  - Spekülum ve mikroskopi imkanı yoksa hem Trikomoniyazis hem de Bakteriyel Vajinozisi kapsamak üzere: **Metronidazol 2 g oral tek doz** (veya 2x500 mg 7 gün) başlanır; riskli ise servisit tedavisi eklenir.\n- **3. Genital Ülser Sendromu:**\n  - Ülser saptanan hastada hem Sifilis hem Şankroid kapsanır: **Benzatin Penisilin G 2.4 M İM tek doz + Azitromisin 1 g tek doz** (veya Seftriakson 250 mg İM).\n  - Vezikül varsa herpes tedavisi rejimine geçilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Sendromik Tablo", "Hedeflenen Ana Patojenler", "Ampirik Kapsayıcı Tedavi Protokolü"],
                [
                    ["Üretral Akıntı", "N. gonorrhoeae + C. trachomatis", "Seftriakson 250 mg İM + Doksisiklin 2x100 mg 7 gün"],
                    ["Vajinal Akıntı", "T. vaginalis + Bakteriyel Vajinozis", "Metronidazol 2 g oral tek doz veya 2x500 mg 7 gün"],
                    ["Genital Ülser", "T. pallidum + H. ducreyi (veya HSV)", "Benzatin Penisilin G 2.4 M İM + Azitromisin 1 g oral"]
                ]
            ),
            make_quiz(
                "Laboratuvar imkanının bulunmadığı kırsal bir sağlık merkezinde üretral akıntı şikayetiyle başvuran genç bir erkek hastaya DSÖ sendromik tedavi protokolüne göre hangi ikili ampirik tedavi derhal başlanmalıdır?",
                [
                    {"key": "A", "text": "Seftriakson 250 mg İM tek doz + Doksisiklin 100 mg oral 2x1 (7 gün)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sendromik yaklaşımda gonore ve klamidya eşzamanlı kapsanmalıdır."},
                    {"key": "B", "text": "Yalnızca parasetamol ve istirahat", "isCorrect": False, "explanation": "Antibiyoterapi şarttır."},
                    {"key": "C", "text": "Metronidazol tek başına", "isCorrect": False, "explanation": "Metronidazol gonore ve klamidyayı etkilemez."},
                    {"key": "D", "text": "Penisilin V oral tablet", "isCorrect": False, "explanation": "Gonore ve klamidyaya etkisizdir."}
                ]
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-17-s99",
        "title": "Farmakolojik Tedavi Karar Ağacı ve Kritik Klinik Tuzaklar",
        "content": "CYBE tedavisinde sık yapılan hatalar ve farmakolojik etkileşim tuzakları (Sınav Spotu):\n\n- **1. Metronidazol ve Alkol Etkileşimi (Disülfiram Benzeri Reaksiyon):**\n  - Metronidazol aldehit dehidrogenaz enzimini bloke eder.\n  - Tedavi sırasında veya ilaç bittikten sonraki **24-48 saat içinde alkol alınırsa** asetaldehit birikir; şiddetli bulantı, kusma, yüzde kızarma, taşikardi ve hipotansiyon gelişir.\n- **2. Gebe Sifilis Hastasında Penisilin Alerjisi:**\n  - Penisilin dışında hiçbir antibiyotik fetal sifilisi güvenle tedavi edemez.\n  - Penisilin alerjisi olan gebe sifilis hastasında alternatif ilaç aranmaz; hasta yoğun bakım şartlarında **oral veya intravenöz penisilin ile desensitize edilerek mutlaka Benzatin Penisilin G verilir**.\n- **3. Gonorede Monoterapi Yanılgısı:**\n  - Sadece seftriakson veya sadece azitromisin vermek hızla antibiyotik direncine yol açar; bu nedenle gonorede ikili tedavi prensibine sadık kalınmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Metronidazol + Alkol Etkileşimi (Disülfiram Reaksiyonu)",
                "Normal Alkol Metabolizması",
                "Alkol dehidrogenaz ile asetaldehite, ardından aldehit dehidrogenaz ile zararsız asetata yıkılır.",
                "Metronidazol Varlığında Blokaj",
                "Aldehit dehidrogenaz bloke olur; kanda asetaldehit birikerek şiddetli kusma, kızarma ve hipotansiyon yapar."
            ),
            make_cloze(
                "Metronidazol kullanan bir hastada aldehit dehidrogenaz inhibisyonu sonucu alkol alındığında şiddetli taşikardi, bulantı ve hipotansiyonla seyreden disülfiram benzeri reaksiyon gelişir.",
                "disülfiram benzeri reaksiyon",
                "Asetaldehit birikimine bağlı akut intolerans tablosu"
            )
        ]
    })

    # Slide 100 - CHECKPOINT 10
    slides.append({
        "id": "k1-17-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] CYBE Klinik Yönetim ve Farmakoterapi Büyük Özeti",
        "content": "Bu son checkpoint ile Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi dersinin tüm temel prensiplerini özetliyoruz:\n\n- **Partner ve Perhiz:** Son 60 gün partnerleri semptomsuz olsa da ampirik tedavi edilir. Tedavi sonrası 7 gün cinsel perhiz zorunludur.\n- **Gebelikte İlaç Güvenliği:** Doksisiklin (diş/kemik lekesi), Kinolonlar (kıkırdak artropatisi) ve Podofilotoksin (teratojen) KONTRENDİKEDİR. Azitromisin, Seftriakson, Amoksisilin ve Metronidazol güvenlidir. Gebe sifilisinde tek seçenek penisilin desensitizasyonudur.\n- **Doğum ve Yenidoğan:** Aktif genital herpes lezyonunda sezaryen zorunludur. Doğumda rutin eritromisin %0.5 göz pomadı ile gonokokal oftalmiya neonatorum önlenir.\n- **Genel Tedavi Şablonu:**\n  - Gonore: Seftriakson 250 mg İM + Azitromisin 1 g oral\n  - Klamidya: Doksisiklin 2x100 mg 7 gün (veya Azitromisin 1 g tek doz)\n  - Trikomoniyazis & BV: Metronidazol 2 g oral tek doz (gebede de aynı)\n  - Sifilis: Benzatin Penisilin G 2.4 M İM tek doz\n  - Şankroid: Azitromisin 1 g veya Seftriakson 250 mg İM\n  - Herpes: Valasiklovir / Asiklovir",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Enfeksiyon Tablosu", "Birinci Tercih İlaç", "Gebelikteki Yaklaşım", "Partner Tedavisi"],
                [
                    ["Gonore", "Seftriakson 250 mg İM + Azitromisin 1 g", "Aynı rejim güvenlidir", "Eşzamanlı ampirik tedavi"],
                    ["Klamidya", "Doksisiklin 2x100 mg 7 gün", "Doksisiklin YASAK; Azitromisin 1 g verilir", "Eşzamanlı ampirik tedavi"],
                    ["Trikomoniyazis", "Metronidazol 2 g oral tek doz", "Metronidazol güvenle verilir", "Eşzamanlı ampirik tedavi"],
                    ["Sifilis", "Benzatin Penisilin G 2.4 M İM", "Tek seçenek; alerjide desensitizasyon", "Seroloji ve ampirik tedavi"]
                ]
            ),
            make_chain(
                "CYBE Farmakoterapötik Başarı Zinciri",
                [
                    "1. Doğru Tanı ve Ampirik Kapsama: Gonore, klamidya veya ülser etkenine yönelik tam rejim.",
                    "2. Partner Tedavisi: Son 60 gündeki partnerlerin eşzamanlı ilaç alması.",
                    "3. 7 Gün Cinsel Perhiz: Reenfeksiyonu ve bulaşı önlemek için tam perhiz uygulanması.",
                    "4. Tarama ve Profilaksi: HIV/HBV/Sifilis taraması ve yenidoğan göz profilaksisi."
                ]
            )
        ]
    })

    return slides
