# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-17-s21",
        "title": "Üretral Akıntı Sendromuna Giriş: Klinik Bulgular ve Başvuru",
        "content": "Üretral akıntı (üretrit), üretranın mukozal enflamasyonudur ve erkeklerde cinsel yolla bulaşan enfeksiyonların en sık klinik tablosudur:\n\n- **Kardinal Yakınmalar:**\n  - **Üretral Akıntı:** Penil meatustan spontan veya penisi sıvazlayınca gelen pürülan, mukoid veya seröz akıntı.\n  - **Dizüri:** İdrar yaparken özellikle üretranın ucunda bıçak saplanır gibi şiddetli yanma ve sızlama hissi.\n  - **Üretral İrritasyon ve Kaşıntı:** Meatus çevresinde kaşıntı, karıncalanma ve eritem (meatal inflamasyon).\n- **Temel Klinik Ayrım:** Üretritler mikrobiyolojik ve klinik açıdan iki büyük kategoriye ayrılır (Sınav Spotu):\n  1. **Gonokokal Üretrit:** Neisseria gonorrhoeae tarafından oluşturulan tablo.\n  2. **Nongonokokal Üretrit (NGU):** Gonokok dışındaki patojenler (başta Chlamydia trachomatis olmak üzere Mycoplasma genitalium vb.) tarafından oluşturulan tablo.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Gonokokal Üretrit vs Nongonokokal Üretrit Başlangıcı",
                "Gonokokal Üretrit",
                "Kısa inkübasyon (2-7 gün); ani başlar; bol, koyu kıvamlı sarı-yeşil pürülan akıntı ve şiddetli dizüri görülür.",
                "Nongonokokal Üretrit (NGU)",
                "Daha uzun inkübasyon (1-3 hafta); sinsi başlar; az miktarda berrak, mukoid veya seröz akıntı görülür."
            ),
            make_cloze(
                "Erkeklerde idrar yaparken üretrada şiddetli yanma ve penil akıntıyla seyreden üretral mukoza iltihabına üretrit denir.",
                "üretrit",
                "Üretra mukozasının enflamatuvar enfeksiyonu"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-17-s22",
        "title": "Gonokokal Üretrit: Neisseria gonorrhoeae ve Akut Pürülan Tablo",
        "content": "Gonokokal üretrit (halk arasında bel soğukluğu), Neisseria gonorrhoeae'nin ürogenital kolumnar epitele invazyonuyla ortaya çıkar:\n\n- **İnkübasyon Süresi:** Cinsel temastan sonra son derece kısadır; genellikle **2 ila 7 gün (ortalama 3-5 gün)** içinde semptomlar patlar.\n- **Karakteristik Akıntı:**\n  - Bol miktarda, kıvamlı, opak ve **sarı-yeşil pürülan (cerahatli)** bir akıntıdır; iç çamaşırını kirletir ve penisi sıkmaya gerek kalmadan meatustan kendiliğinden damlar.\n- **Yoğun Dizüri:** İdrar yaparken hasta adeta 'cam kırıkları dökülüyormuş gibi' şiddetli bir yanmadan yakınır.\n- **Erkekte Yüksek Semptom Oranı:** Enfekte erkeklerin **%90'ından fazlası** belirgin semptom gösterir; asemptomatik taşıyıcılık erkekte yalnızca yaklaşık %10'dur; bu sayede erkekler hızla sağlık merkezine başvurur.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Gonokokal Üretrit Gelişim Aşamaları",
                [
                    "1. Bakteriyel Kolonizasyon: Pilus ve Opa proteinleri ile anterior üretra epiteline tutunur.",
                    "2. İntrasellüler İnvazyon: Endotel altına girerek LOS toksinleriyle akut yangı başlatır.",
                    "3. Masif Nötrofil Akını: Binlerce nötrofil lümene dökülerek pürülan cerahat oluşturur.",
                    "4. Şiddetli Akut Tablo: 2-5 gün içinde bol sarı-yeşil akıntı ve şiddetli dizüri başlar."
                ]
            ),
            make_quiz(
                "Şüpheli cinsel ilişkiden 3 gün sonra penil meatustan bol miktarda sarı-yeşil pürülan cerahatli akıntı ve şiddetli dizüri ile başvuran genç bir erkekte öncelikle hangi etken düşünülmelidir?",
                [
                    {"key": "A", "text": "Neisseria gonorrhoeae", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kısa inkübasyon süresi (2-7 gün) ve bol sarı-yeşil pürülan cerahat gonokokal üretritin tipik tablosudur."},
                    {"key": "B", "text": "Treponema pallidum", "isCorrect": False, "explanation": "Treponema sert şankr yapar, pürülan üretrit yapmaz."},
                    {"key": "C", "text": "Candida albicans", "isCorrect": False, "explanation": "Kandida erkeklerde pürülan üretrit yapmaz, balanit yapabilir."},
                    {"key": "D", "text": "HPV Tip 6", "isCorrect": False, "explanation": "HPV siğil yapar, üretral pürülan akıntı yapmaz."}
                ]
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-17-s23",
        "title": "Nongonokokal Üretrit (NGU): Klamidya ve Mikoplazma Rolü",
        "content": "Nongonokokal üretrit (NGU), Neisseria gonorrhoeae dışındaki mikroorganizmaların yol açtığı üretrit tablosudur:\n\n- **Etiyolojik Dağılım:**\n  - **Chlamydia trachomatis (D-K Serovarları):** NGU olgularının %30-50'sinden sorumlu olan **en sık etkendir**.\n  - **Mycoplasma genitalium:** Olguların %15-25'inden sorumludur; makrolid direnci yüksek olduğu için tedavi başarısızlıklarının baş failidir.\n  - **Ureaplasma urealyticum:** Daha az sıklıkla NGU etkenidir.\n  - **Trichomonas vaginalis:** Nadir fakat önemli bir nongonokokal üretrit nedenidir.\n- **Klinik Profil:**\n  - İnkübasyon süresi daha uzundur: **1 ila 3 hafta** (bazen haftalarca fark edilmez).\n  - Akıntı pürülan değil; **az miktarda, sulu, müköz veya seröz (şeffaf/beyazımsı)** niteliktedir; çoğunlukla yalnızca sabah ilk idrardan önce penisi sıvazlayınca fark edilir.\n  - Erkeklerin yaklaşık %50'si asemptomatiktir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["NGU Etkeni", "Sıklık Oranı", "Hücresel Özellik", "Klinik Özellik"],
                [
                    ["Chlamydia trachomatis", "%30 - 50 (En sık)", "Zorunlu hücre içi bakteri", "Hafif dizüri, sabah sıvazlamada gelen mukoid akıntı"],
                    ["Mycoplasma genitalium", "%15 - 25", "Hücre duvarsız mikoplazma", "Dirençli, nükseden, doksisikline yanıtsız üretrit"],
                    ["Ureaplasma urealyticum", "%5 - 10", "Üreaz pozitif mikoplazma", "Hafif seyirli nongonokokal akıntı"],
                    ["Trichomonas vaginalis", "%2 - 5", "Kamçılı protozoon", "Köpüksü üretral irritasyon, partnerde vajinit"]
                ]
            ),
            make_cloze(
                "Nongonokokal üretritlerin en sık bakteriyel etkeni olan zorunlu hücre içi mikroorganizma Chlamydia trachomatis bakterisidir.",
                "Chlamydia trachomatis",
                "NGU'nun bir numaralı bakteriyel nedeni"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-17-s24",
        "title": "Gonokokal vs Nongonokokal Üretrit Karşılaştırmalı Tablosu",
        "content": "Klinik muayene ve anamnez iki üretrit tablosunu birbirinden ayrıştırmada hekime güçlü ipuçları sağlar (Sınav Spotu):\n\n- **İnkübasyon:** Gonore 2-7 günde hızla belirirken; klamidya 1-3 haftada sinsi ortaya çıkar.\n- **Akıntı Miktarı ve Niteliği:** Gonorede bol, sarı-yeşil, kıvamlı pürülan cerahat; NGU'da az, müköz, sulu veya berrak seröz akıntı izlenir.\n- **Dizüri Şiddeti:** Gonorede şiddetli, dayanılmaz yanma; NGU'da hafif batma, kaşıntı ve karıncalanma hissi vardır.\n- **Ko-enfeksiyon Birlikteliği (Kritik İlke):** Gonore tanısı alan hastaların **yaklaşık üçte birinde (%20-40) aynı anda klamidya enfeksiyonu da bulunur**. Bu nedenle yalnızca gonore tedavisi verilirse hasta birkaç gün sonra klamidyaya bağlı NGU ile geri döner (postgonokoksik üretrit); güncel kılavuzlar bu yüzden **ikili kombine tedavi** önerir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Özellik", "Gonokokal Üretrit (Gonore)", "Nongonokokal Üretrit (NGU)"],
                [
                    ["Etken", "Neisseria gonorrhoeae", "Chlamydia trachomatis, M. genitalium"],
                    ["İnkübasyon Süresi", "2 - 7 gün (kısa ve ani)", "1 - 3 hafta (uzun ve sinsi)"],
                    ["Akıntı Tipi", "Bol, koyu kıvamlı sarı-yeşil pürülan", "Az miktarda, müköz, sulu, beyazımsı"],
                    ["Dizüri Şiddeti", "Çok şiddetli ve keskin", "Hafif-orta derecede yanma ve kaşıntı"],
                    ["Gram Boyama", "Nötrofil içi Gram (-) diplokoklar", "Lökosit var, diplokok izlenmez"]
                ]
            ),
            make_quiz(
                "Gonore tanısı konan bir hastaya yalnızca gonokoka etkili tedavi verildiğinde günler sonra hafif mukoid akıntıyla geri gelmesine yol açan ve ko-enfeksiyon sıklığı yüksek olan etken hangisidir?",
                [
                    {"key": "A", "text": "Chlamydia trachomatis", "isCorrect": True, "explanation": "Doğru cevap A'dır: Gonore hastalarında %20-40 klamidya birlikteliği vardır; tedavi edilmezse postgonokoksik üretrit gelişir."},
                    {"key": "B", "text": "Pseudomonas aeruginosa", "isCorrect": False, "explanation": "Pseudomonas tipik CYBE ko-enfeksiyonu değildir."},
                    {"key": "C", "text": "Bacillus subtilis", "isCorrect": False, "explanation": "Patojen değildir."},
                    {"key": "D", "text": "Clostridium difficile", "isCorrect": False, "explanation": "Antibiyotik ishali etkenidir, üretritle ilişkisizdir."}
                ]
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-17-s25",
        "title": "Gram Boyamanın Rolü: Nötrofil İçi Gram (-) Diplokoklar",
        "content": "Üretral akıntının Gram boyaması erkek hastada dakikalar içinde kesin yönlendirme sağlayan altın değerinde hızlı bir testtir (Sınav Spotu):\n\n- **Testin Uygulanması:** Penil meatustan alınan bir damla akıntı lam üzerine yayılır, ısı ile tespit edilip standart Gram boyama yapılır.\n- **Patognomonik Gonore Bulgusu:**\n  - Polimorfonükleer lökositlerin (nötrofillerin) **sitoplazması içinde** çiftler halinde kümelenmiş **kahve çekirdeği veya böbrek şeklinde Gram negatif (pembe-kırmızı) diplokokların** görülmesi.\n  - Erkek semptomatik üretritte bu bulgunun duyarlılığı >%95, özgüllüğü >%99'dur; anında gonore tanısı koydurur.\n- **Nongonokokal Üretrit Bulgusu:**\n  - Mikroskopta büyük büyütme alanında (1000x immersion) **>5 adet nötrofil** saptanır, ancak nötrofil içinde veya dışında hiçbir diplokok görülmez.\n  - Bu tablo nongonokokal üretriti (NGU) kanıtlar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Gonokokal Gram Boyama vs NGU Gram Boyama",
                "Gonokokal Gram Boyama",
                "Nötrofillerin sitoplazmasında çiftler halinde böbrek biçimli Gram (-) pembe diplokoklar (intrasellüler gonokok).",
                "Nongonokokal Gram Boyama (NGU)",
                "Bol miktarda nötrofil lökosit vardır, ancak sitoplazmada veya alanda hiçbir diplokok izlenmez."
            ),
            make_cloze(
                "Erkek üretral akıntısının Gram boyamasında nötrofillerin sitoplazması içinde izlenen böbrek şekilli pembe mikroorganizmalara Gram negatif diplokok denir.",
                "Gram negatif diplokok",
                "Gonokokun karakteristik mikroskopik boyanma şekli"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-17-s26",
        "title": "İlk Damla İdrar (First-Catch Urine) ve NAAT Testi",
        "content": "Üretradan sürüntü almak ağrılı olduğu için modern tanı kılavuzları non-invaziv ilk idrar örneğini önermektedir:\n\n- **İlk Damla İdrar (First-Catch Urine - Sınav Spotu):**\n  - Hastanın en az 1-2 saat idrar yapmamış olması şarttır.\n  - İdrarın orta akımı değil; üretrayı yıkayarak gelen **ilk 10-20 mililitrelik kısmı** toplanır.\n  - Bu ilk hacim üretra epitelinde dökülmüş enfekte hücreleri ve lökositleri en yüksek konsantrasyonda barındırır.\n- **Lökosit Esteraz Testi:** İdrar çubuğunda (dipstick) pozitif lökosit esteraz veya santrifüj mikroskopisinde >10 lökosit/büyütme alanı üretriti doğrular.\n- **NAAT ile Çift Teşhis:** Bu ilk idrar örneğinden tek bir PCR/NAAT paneliyle hem Neisseria gonorrhoeae hem de Chlamydia trachomatis DNA'sı eş zamanlı olarak %99 doğrulukla saptanır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Örnek Alma Yöntemi", "Doğru Uygulama Şekli", "Hatalı Uygulama", "Tanısal Başarı"],
                [
                    ["İlk Damla İdrar (First-Catch)", "En az 2 saat idrar yapmadan, ilk 10-20 ml hacim", "Orta akım idrarı toplamak (bakteri seyreltilir)", "NAAT için mükemmel duyarlılık"],
                    ["Üretral Sürüntü", "İnce eküvyonla üretra içine 2-4 cm girip çevirmek", "Sadece meatus yüzeyine değdirmek", "Gram boyama ve kültür için standart"]
                ]
            ),
            make_quiz(
                "Erkek hastada üretrit şüphesiyle NAAT testi için idrar örneği toplanırken dikkat edilmesi gereken en kritik kural nedir?",
                [
                    {"key": "A", "text": "İdrarın son damlalarının toplanması", "isCorrect": False, "explanation": "Son damlalar mesane tabanını temsil eder."},
                    {"key": "B", "text": "Hastanın en az 1-2 saat idrar yapmamış olması ve üretrayı yıkayan ilk 10-20 ml'lik kısmın (ilk damla) alınması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Üretra epitelindeki patojen ve lökositler ilk 10-20 ml idrarda yoğunlaşır."},
                    {"key": "C", "text": "İdrar yapmadan önce bol su içilip üretranın temizlenmesi", "isCorrect": False, "explanation": "Üretrayı yıkamak patojen konsantrasyonunu düşürür."},
                    {"key": "D", "text": "İdrara aseton damlatılması", "isCorrect": False, "explanation": "Aseton testi bozar."}
                ]
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-17-s27",
        "title": "Tedavi Edilmemiş Üretritin Komplikasyonları: Epididimit ve Darlık",
        "content": "Üretrit zamanında veya yeterli dozda tedavi edilmezse enfeksiyon asendan yolla yayılır ve kalıcı hasar bırakır:\n\n- **1. Akut Epididimit ve Epididimoorşit:**\n  - Patojen duktus deferens boyunca geriye doğru tırmanarak epididime ve testise ulaşır.\n  - Genç cinsel aktif erkeklerde (<35 yaş) akut epididimitin en sık nedenleri **C. trachomatis ve N. gonorrhoeae**'dir.\n  - Skrotumda tek taraflı şiddetli ağrı, şişlik, kızarıklık ve ateş gelişir; skrotum yukarı kaldırıldığında ağrının azalması (Prehn bulgusu pozitifliği) torsiyondan ayırt etmede yardımcıdır.\n- **2. Üretral Striktür (Darlık - Sınav Spotu):**\n  - Özellikle gonokokal üretritin kronikleştiği olgularda üretra submukozasında yoğun fibrozis ve skar dokusu gelişir; üretra lümeni daralır (üretral darlık), idrar akımı zayıflar ve kalıcı cerrahi dilatasyon gerektirir.\n- **3. Kronik Prostatit ve İnfertilite:** Sperm kalitesinin bozulması ve duktus tıkanıklığı kısırlığa yol açabilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Akut Üretrit Aşaması vs Tedavi Edilmemiş Kronik Darlık",
                "Akut Üretrit Aşaması",
                "Enflamasyon yüzeyeldir; uygun antibiyotikle tamamen iyileşir ve kalıcı anatomik sekel bırakmaz.",
                "Kronikleşmiş Üretral Darlık",
                "Submukozal fibrotik skar üretra lümenini daraltır; idrar yapma güçlüğü ve cerrahi dilatasyon gerektirir."
            ),
            make_cloze(
                "35 yaş altı genç cinsel aktif erkeklerde akut epididimit tablosuna en sık yol açan iki CYBE etkeni gonokok ve klamidya bakterileridir.",
                "klamidya",
                "Genç erkeklerde epididimitin majör bakteriyel etkeni"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-17-s28",
        "title": "Disemine Gonokokal Enfeksiyon (DGI): Artrit ve Dermatit Triadı",
        "content": "Tedavi edilmemiş asemptomatik veya lokalize gonore hastalarının yaklaşık %0.5-3'ünde bakteri kana karışarak sistemik yayılım gösterir (Disemine Gonokoksemi - DGI):\n\n- **Patogenez:** Serum bakterisidal aktivitesine dirençli gonokok suşları (özellikle kompleman C5-C9 eksikliği olan bireylerde) kana karışır.\n- **Klasik Artrit-Dermatit Sendromu Triadı (Sınav Spotu):**\n  1. **Göçücü Poliartralji / Poliartrit:** El bileği, diz, ayak bileği gibi büyük eklemleri sırayla tutan göçücü eklem ağrısı.\n  2. **Tenosinovit:** Özellikle el ve ayak sırtındaki tendon kılıflarında ağrılı şişlik ve kızarıklık.\n  3. **Karakteristik Deri Döküntüsü:** Ekstremitelerin distalinde az sayıda (genellikle 5-30 adet), ortası nekrotik veya püstüler, tabanı eritemli papülo-püstüler lezyonlar.\n- **Pürülan Septik Artrit:** İlerleyen evrede tek bir büyük eklemde (en sık diz) masif pürülan sıvı toplanmasıyla monoartrit gelişir; eklem sıvısı aspirasyonu ve acil İV Seftriakson gerekir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["DGI Klinik Komponenti", "Tutulan Anatomik Yapı", "Fizik Muayene Bulgusu"],
                [
                    ["Tenosinovit", "El ve ayak fleksör/ekstensör tendonları", "Tendon boyunca ağrı, şişlik ve hareket kısıtlılığı"],
                    ["Dermatit Lezyonları", "El ve ayak parmak uçları, ekstremiteler", "Ortası grimsi nekrotik papül ve püstüller (az sayıda)"],
                    ["Göçücü Artrit / Monoartrit", "Diz, el bileği, dirsek eklemleri", "Sıcak, şiş, hareketle aşırı ağrılı septik eklem"],
                    ["Sistemik Belirtiler", "Tüm vücut (bakteriyemi)", "Ateş, titreme, halsizlik, lökositoz"]
                ]
            ),
            make_quiz(
                "Ateş, el bileğinde tenosinovit, göçücü eklem ağrıları ve parmaklarında ortası nekrotik püstüllerle başvuran 24 yaşındaki cinsel aktif bir kadında öncelikle hangi disemine enfeksiyon düşünülmelidir?",
                [
                    {"key": "A", "text": "Disemine Gonokokal Enfeksiyon (DGI)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tenosinovit, göçücü artralji ve nekrotik deri püstülleri triadı disemine gonokokin klasik tablosudur."},
                    {"key": "B", "text": "Romatoid Artrit atağı", "isCorrect": False, "explanation": "RA simetrik küçük eklem tutar, nekrotik püstül yapmaz."},
                    {"key": "C", "text": "Gut artriti", "isCorrect": False, "explanation": "Gut 1. metatarsofalangeal eklemde monoartrittir."},
                    {"key": "D", "text": "Akut apandisit", "isCorrect": False, "explanation": "Sağ alt kadran ağrısıdır, tenosinovit yapmaz."}
                ]
            )
        ]
    })

    # Slide 29 - CHECKPOINT 3
    slides.append({
        "id": "k1-17-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Üretrit Sendromu ve Ayrımı",
        "content": "Bu checkpointte üretrit tiplerini, Gram boyama kriterlerini ve sistemik komplikasyonları pekiştiriyoruz:\n\n- **Gonokokal Üretrit:** N. gonorrhoeae; 2-7 gün inkübasyon; bol sarı-yeşil pürülan akıntı; şiddetli dizüri; erkekte %90 semptomatik.\n- **Nongonokokal Üretrit (NGU):** En sık Chlamydia trachomatis (D-K), Mycoplasma genitalium; 1-3 hafta inkübasyon; az miktarda mukoid akıntı.\n- **Gram Boyama Altın Değeri:** Nötrofil içinde böbrek biçimli Gram (-) diplokoklar görülmesi gonore için tanı koydurucudur.\n- **İlk Damla İdrar:** En az 1-2 saatlik tutulmuş idrarın ilk 10-20 ml'lik kısmı toplanarak NAAT çalışılır.\n- **Komplikasyonlar:** 35 yaş altı erkekte akut epididimit; kronikleşen gonorede üretral striktür (darlık); DGI'de tenosinovit, dermatit ve göçücü poliartrit triadı.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Kriter", "Gonokokal Üretrit", "Nongonokokal Üretrit (NGU)"],
                [
                    ["Primer Patojen", "Neisseria gonorrhoeae", "Chlamydia trachomatis, M. genitalium"],
                    ["İnkübasyon", "2 - 7 gün (kısa)", "1 - 3 hafta (uzun)"],
                    ["Akıntı Özelliği", "Bol pürülan sarı-yeşil cerahat", "Az miktarda şeffaf/beyazımsı mukoid"],
                    ["Gram Yayması", "İntrasellüler Gram (-) diplokoklar", "Sadece nötrofiller (>5/alan)"],
                    ["Kombine Tedavi Gerekçesi", "%20-40 klamidya ko-enfeksiyonu riski", "Mikoplazma ve gonore birlikteliği"]
                ]
            ),
            make_chain(
                "Üretrit Tanı ve Komplikasyon Akış Şeması",
                [
                    "1. Semptom: Penil akıntı ve dizüri ile başvuru.",
                    "2. Hızlı Gram Boyama: İntrasellüler diplokok varsa gonore; yoksa NGU.",
                    "3. İlk Damla İdrarda NAAT: Moleküler doğrulama ve ko-enfeksiyon tespiti.",
                    "4. Tedavi Edilmezse Risk: Akut epididimit veya üretral darlık gelişimi."
                ]
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-17-s30",
        "title": "Bölüm Özeti: Üretrit Sendromundan Trikomoniyazis Tedavisine Geçiş",
        "content": "Bölüm 3 boyunca gonokokal ve nongonokokal üretrit tablolarını, Gram boyamanın gücünü ve disemine gonokoksemiyi tamamladık:\n\n- **Önemli Kural:** Üretrit tablosuyla gelen her hastada gonore ve klamidya birlikte düşünülmeli ve tedavi ortak planlanmalıdır.\n- **Sonraki Bölüm:** Bir sonraki bölümde protozoal bir CYBE olan **Trichomonas vaginalis enfeksiyonunu**, çilek serviks manzarasını ve **tek doz Metronidazol tedavisinin inceliklerini** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Genç cinsel aktif bir erkekte akut tek taraflı skrotal ağrı ve şişlikle seyreden epididimitin en sık iki CYBE bakteriyel etkeni hangileridir?",
                "Chlamydia trachomatis ve Neisseria gonorrhoeae",
                "35 yaş altı genç erkekte epididimitin iki majör etkeni"
            ),
            make_quiz(
                "Disemine gonokokal enfeksiyonun (DGI) klasik kliniğini oluşturan üçlü semptom kompleksi (triad) aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Tenosinovit, dermatit (nekrotik püstüller) ve göçücü poliartrit", "isCorrect": True, "explanation": "Doğru cevap A'dır: DGI'nin klasik triadı tenosinovit, nekrotik deri püstülleri ve göçücü poliartralji/artrittir."},
                    {"key": "B", "text": "Sarılık, asit ve splenomegali", "isCorrect": False, "explanation": "Siroz tablosudur."},
                    {"key": "C", "text": "Hipertansiyon, bradikardi ve solunum düzensizliği", "isCorrect": False, "explanation": "Cushing triadı / KİBA bulgusudur."},
                    {"key": "D", "text": "Öksürük, hemoptizi ve kilo kaybı", "isCorrect": False, "explanation": "Akciğer tüberkülozu veya karsinom bulgusudur."}
                ]
            )
        ]
    })

    return slides
