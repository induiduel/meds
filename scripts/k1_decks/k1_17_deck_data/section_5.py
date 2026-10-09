# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-17-s41",
        "title": "Chlamydia trachomatis Yaşam Döngüsü: İki Fazlı Hücresel Biyoloji",
        "content": "Chlamydia trachomatis, kendi başına ATP sentezleyemeyen ve bu nedenle konak hücre içinde yaşamak zorunda olan bir zorunlu intrasellüler bakteridir (Sınav Spotu):\n\n- **İki Ayrı Morfolojik Form:**\n  1. **Elementer Cisim (Elementary Body - EB):**\n     - Küçük (~0.3 μm), metabolik olarak inaktif, yoğun disülfit bağlarıyla çevrili dayanıklı formdur.\n     - **Bulaşıcı (İnfeksiyöz) Formdur:** Hücre dışı ortamda yaşayabilir ve hedef konak hücreye (kolumnar epitel) tutunarak fagositozu tetikler.\n  2. **Retiküler Cisim (Reticulate Body - RB):**\n     - Hücre içine girdikten sonra vakuol (inklüzyon) içinde metabolik olarak aktif, büyük (~1 μm) forma dönüşür.\n     - **Çoğalan (Replikatif) Formdur:** Konağın ATP'sini kullanarak ikiye bölünerek çoğalır; ardından tekrar EB'lere dönüşür.\n- **Hücre Lizisi:** İntrasellüler inklüzyon patlayınca yüzlerce yeni EB çevre dokuya ve mukozaya yayılarak enfeksiyonu yayar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Elementer Cisim (EB) vs Retiküler Cisim (RB)",
                "Elementer Cisim (EB)",
                "Küçük, metabolik olarak inaktif, hücre dışına dayanıklı ve bulaşıcı (infeksiyöz) formdur.",
                "Retiküler Cisim (RB)",
                "Büyük, metabolik olarak aktif, konak ATP'sini kullanan ve hücre içinde çoğalan (replikatif) formdur."
            ),
            make_cloze(
                "Chlamydia trachomatis'in konak hücreler arasında aktarılabilen küçük, dayanıklı ve bulaşıcı formuna elementer cisim denir.",
                "elementer cisim",
                "Klamidyanın infeksiyöz hücre dışı formu"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-17-s42",
        "title": "Chlamydia trachomatis Serovarları: Trahomdan Ürogenital Hastalığa",
        "content": "Klamidyanın majör dış membran proteini (MOMP) antijenik yapısına göre 15'ten fazla serovarı tanımlanmıştır (Sınav Spotu):\n\n- **1. Serovar A, B, Ba ve C (Trahom Grubu):**\n  - Cinsel yolla değil; el-göz teması ve sineklerle bulaşır.\n  - Kronik granülomatöz keratokonjonktivit yaparak dünyada **önlenebilir körlüğün en sık enfeksiyöz nedenidir**.\n- **2. Serovar D - K (Klasik Ürogenital Grup - Kurulun Odağı):**\n  - Cinsel temasla bulaşır.\n  - Erkeklerde nongonokokal üretrit (NGU) ve epididimit; kadınlarda mukopürülan servisit, üretral sendrom, endometrit, salpenjit ve pelvik inflamatuvar hastalık (PİH) yapar.\n  - Doğum sırasında yenidoğana geçerek inklüzyonlu konjonktivit ve pnömoni oluşturur.\n- **3. Serovar L1, L2 ve L3 (Lenfogranüloma Venereum - LGV):**\n  - Lenfotropik serovarlardır; sistemik ve derin lenfatik invazyonla genital ülser ve süpüratif lenfadenit (bubon) tablosu yapar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Serovar Grubu", "Bulaş Yolu", "Primer Hedef Doku", "Karakteristik Klinik Tablo"],
                [
                    ["Serovar A - C", "El-göz teması, sinekler", "Konjonktiva epiteli", "Trahom (kronik keratit, körlük)"],
                    ["Serovar D - K", "Cinsel temas, doğum kanalı", "Ürogenital kolumnar epitel", "Nongonokokal üretrit, servisit, PİH, neonatal pnömoni"],
                    ["Serovar L1 - L3", "Cinsel temas", "Bölgesel lenfatik doku", "Lenfogranüloma venereum (LGV, oluk belirtisi, bubon)"]
                ]
            ),
            make_quiz(
                "Cinsel yolla bulaşan klamidya enfeksiyonlarında nongonokokal üretrit, mukopürülan servisit ve yenidoğan konjonktivitinden sorumlu serovar grubu hangisidir?",
                [
                    {"key": "A", "text": "Serovar A, B, C", "isCorrect": False, "explanation": "A-C körlük yapan trahom serovarlarıdır."},
                    {"key": "B", "text": "Serovar D - K", "isCorrect": True, "explanation": "Doğru cevap B'dir: Ürogenital klamidya enfeksiyonları ve neonatal bulaş D-K serovarlarıyla gerçekleşir."},
                    {"key": "C", "text": "Serovar L1 - L3", "isCorrect": False, "explanation": "L1-L3 Lenfogranüloma venereum (LGV) etkenidir."},
                    {"key": "D", "text": "Yalnızca Serovar M", "isCorrect": False, "explanation": "Serovar M bu sınıflamada yoktur."}
                ]
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-17-s43",
        "title": "Lenfogranüloma Venereum (LGV): Serovar L1-L3 ve Bubonlar",
        "content": "Lenfogranüloma venereum (LGV), lenfatik damarları ve düğümleri infiltre eden agresif bir klamidya varyantıdır (Sınav Spotu):\n\n- **Etken Serovarlar:** Chlamydia trachomatis **L1, L2, L2b ve L3** serovarlarıdır.\n- **Üç Evreli Klinik Seyir:**\n  1. **Primer Evre:** Cinsel temastan günler sonra genital bölgede küçük, ağrısız, hızla iyileşen geçici bir papül veya herpetiform erozyon/ülser belirir; hasta sıklıkla fark etmez.\n  2. **Sekonder Evre (Akut Lenfadenit / Bubon):** Primer lezyondan 2-6 hafta sonra tek veya iki taraflı **inguinal lenf düğümleri masif şekilde büyür, ağrılı ve fluktuan hale gelir (bubon)**; cilde fistülize olarak püy akıtabilir.\n  - **Oluk Belirtisi (Groove Sign):** İnguinal ligamanın üstündeki ve altındaki lenf nodları büyüyerek ligaman boyunca bir çöküntü oluşturur (oluk belirtisi patognomoniktir).\n  3. **Tersiyer Evre:** Kronik lenfatik obstrüksiyon sonucu genital elefantiyazis ve rektal darlıklar (proktokolit).\n- **LGV Tedavisi:** Standart klamidyadan daha uzun sürer: **Doksisiklin 2x100 mg oral, tam 21 gün**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["LGV Evresi", "Zaman Aralığı", "Morfolojik Lezyon", "Klinik Özellik"],
                [
                    ["Primer Evre", "Temastan 3 - 30 gün sonra", "Küçük ağrısız papül veya sığ erozyon", "Hızla kendiliğinden kaybolur"],
                    ["Sekonder Evre", "2 - 6 hafta sonra", "Ağrılı süpüratif inguinal bubonlar ve oluk belirtisi", "Fistülizasyon ve sistemik ateş"],
                    ["Tersiyer Evre", "Aylar - yıllar sonra", "Lenfatik skar, striktür ve genital elefantiyazis", "Rektal darlık, kronik fistüller"]
                ]
            ),
            make_cloze(
                "Chlamydia trachomatis L1-L3 serovarlarının yol açtığı ve inguinal lenf düğümlerinde oluk belirtisiyle süpüratif bubonlar yapan hastalığa lenfogranüloma venereum denir.",
                "lenfogranüloma venereum",
                "Klamidyanın lenfotropik sistemik hastalığının tıbbi adı"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-17-s44",
        "title": "Ürogenital Klamidya Tedavisi: Azitromisin vs Doksisiklin",
        "content": "Chlamydia trachomatis D-K ürogenital enfeksiyonlarının tedavisinde iki majör antibiyotik seçeneği kılavuzlarda yer alır (Sınav Spotu):\n\n- **1. Azitromisin (Makrolid Grubu - Birinci Tercih):**\n  - **Doz:** **Azitromisin 1 g oral TEK DOZ** (2 adet 500 mg tablet hekim gözetiminde yutturulur).\n  - **Avantajı:** Tek doz doğrudan gözlemle tedavi (DOT) hasta uyum sorununu tamamen ortadan kaldırır.\n  - Etki Mekanizması: Bakteriyel ribozomun 50S alt birimine bağlanarak protein sentezini inhibe eder; uzun doku yarı ömrü sayesinde tek dozla günlerce etkili konsantrasyon sağlar.\n- **2. Doksisiklin (Tetrasiklin Grubu - Eşit Etkinlik):**\n  - **Doz:** **Doksisiklin 2x100 mg oral, 7 gün**.\n  - Etki Mekanizması: 30S ribozomal alt birime bağlanır.\n  - Dezavantajı: 7 gün boyunca günde 2 kez aksatmadan içilmesi gerekir; hasta uyumu aksarsa tedavi başarısız olabilir.\n- **Alternatif Rejimler:** Levofloksasin 1x500 mg oral 7 gün veya Ofloksasin 2x300 mg 7 gün (diğer kinolonlar klamidyaya etkisizdir!).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Azitromisin 1 g Tek Doz vs Doksisiklin 7 Gün Rejimi",
                "Azitromisin 1 g Oral Tek Doz",
                "Tek seferde alınır, hasta uyumu %100'dür; klinikte doğrudan gözetimle içirilebilir.",
                "Doksisiklin 2x100 mg (7 Gün)",
                "7 gün boyunca sabah-akşam alınmalıdır; rektal klamidyada biraz daha üstündür ancak uyum aksayabilir."
            ),
            make_quiz(
                "Nongonokokal üretrit saptanan ve Chlamydia trachomatis pozitif çıkan genç bir erkek hastada tek dozla kesin kür sağlayan birinci basamak tedavi hangisidir?",
                [
                    {"key": "A", "text": "Azitromisin 1 g oral, tek doz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Klamidya ürogenital enfeksiyonunda tek doz Azitromisin 1 gram oral standart kür rejimidir."},
                    {"key": "B", "text": "Penisilin V oral, 10 gün", "isCorrect": False, "explanation": "Klamidya hücre içi bakteridir, hücre duvarı yapısı penisiline yanıtsızdır."},
                    {"key": "C", "text": "Metronidazol 500 mg tek doz", "isCorrect": False, "explanation": "Metronidazol parazit ve anaeroplara etkilidir."},
                    {"key": "D", "text": "Siprofloksasin 250 mg tek doz", "isCorrect": False, "explanation": "Siprofloksasin klamidyaya karşı klinik olarak yetersizdir."}
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-17-s45",
        "title": "Gebelikte Klamidya Tedavisi ve Doksisiklin Kontrendikasyonu",
        "content": "Gebelikte klamidya enfeksiyonunun tedavisi hem fetal güvenlik hem de yenidoğanın korunması açısından katı kurallara bağlıdır (Sınav Spotu):\n\n- **Doksisiklinin Kesin Kontrendikasyonu:**\n  - Tetrasiklin grubu ilaçlar (doksisiklin) kalsiyum şelasyonu yapar.\n  - Fetal kemik büyümesini durdurur ve diş minesi matriksine çökerek **bebekte kalıcı sarı-kahverengi diş renklenmesine ve kemik displazisine** yol açar.\n  - Bu nedenle **gebelikte ve emziren annelerde doksisiklin KESİNLİKLE YASAKTIR (KONTRENDİKEDİR)**.\n- **Gebelikte Birinci Basamak Güvenli Tedavi:**\n  - **Azitromisin 1 g oral tek doz** gebelikte birinci basamak güvenli seçenektir (FDA Kategori B).\n- **Gebelikte Alternatif Rejimler:**\n  - Amoksisilin 3x500 mg oral, 7 gün.\n  - Eritromisin baz 4x500 mg oral, 7 gün.\n- **Kür Kontrolü:** Gebelerde nüks ve vertikal geçiş riskini dışlamak için tedaviden **3-4 hafta sonra kontrol NAAT testi** yapılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Hasta Grubu", "Birinci Tercih İlaç", "Alternatif Seçenekler", "Kesin Kontrendike İlaç"],
                [
                    ["Gebe Olmayan Erişkin", "Azitromisin 1 g tek doz VEYA Doksisiklin 7 gün", "Levofloksasin 1x500 mg 7 gün", "Yok"],
                    ["Gebe Kadın", "Azitromisin 1 g oral tek doz", "Amoksisilin 7 gün, Eritromisin 7 gün", "Doksisiklin (Tetrasiklinler), Kinolonlar"]
                ]
            ),
            make_quiz(
                "Gebeliğinin 24. haftasında Chlamydia trachomatis servisiti saptanan bir kadında fetusta kemik gelişim bozukluğu ve kalıcı diş renklenmesi riski nedeniyle KESİNLİKLE verilmemesi gereken antibiyotik hangisidir?",
                [
                    {"key": "A", "text": "Doksisiklin (Tetrasiklin grubu)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Doksisiklin gebelikte diş minesi hipoplazisi ve kemik gelişim geriliği yaptığı için mutlak kontrendikedir."},
                    {"key": "B", "text": "Azitromisin", "isCorrect": False, "explanation": "Azitromisin gebede birinci seçenektir."},
                    {"key": "C", "text": "Amoksisilin", "isCorrect": False, "explanation": "Amoksisilin gebelikte güvenli alternatiftir."},
                    {"key": "D", "text": "Eritromisin", "isCorrect": False, "explanation": "Eritromisin baz gebede kullanılabilir."}
                ]
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-17-s46",
        "title": "Yenidoğanda Klamidya Komplikasyonları: Konjonktivit ve Pnömoni",
        "content": "Klamidya ile enfekte anneden normal vajinal doğumla doğan bebeklerin yaklaşık %50-70'i mikroorganizmayı kapar:\n\n- **1. İnklüzyonlu Neonatal Konjonktivit (Oftalmiya Neonatorum):**\n  - Doğumdan **5 ila 14 gün sonra** başlar (Gonokok konjonktiviti ilk 2-5 günde hızla başlarken, klamidya daha geç başlar).\n  - Göz kapaklarında ödem, kemozis ve bol mukopürülan çapaklanma izlenir.\n  - Lokal damlalar yetersizdir; nazofarengeal rezervuarı kurutmak ve pnömoniyi engellemek için **sistemik oral eritromisin veya azitromisin şurup** verilmelidir.\n- **2. Bebeklik Klamidya Pnömonisi (İnterstisyel Pnömoni - Sınav Spotu):**\n  - Doğumdan **4 ila 12 hafta sonra** sinsice gelişir.\n  - Karakteristik Öksürük: Ateşsiz seyreden, kesik kesik, makinalı tüfek gibi ardışık **'stakkato öksürük' (staccato cough)** tablosudur.\n  - Akciğer grafisinde bilateral yaygın interstisyel infiltrasyon izlenir; kanda belirgin eozinofili eşlik eder.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Gonokokal Neonatal Konjonktivit vs Klamidyal Neonatal Konjonktivit",
                "Gonokokal Konjonktivit",
                "Doğumdan sonraki 2-5. günlerde hiperakut başlar; bol fışkırıcı püy ve kornea perforasyonu riski taşır.",
                "Klamidyal Konjonktivit",
                "Doğumdan sonraki 5-14. günlerde daha subakut başlar; mukopürülandır ve pnömoniye ilerleyebilir."
            ),
            make_cloze(
                "Klamidya ile enfekte anneden doğan bebekte doğumdan 1-3 ay sonra gelişen ve ateşsiz stakkato öksürükle seyreden tablo klamidya pnömonisi tablosudur.",
                "klamidya pnömonisi",
                "Bebekte stakkato öksürük yapan atipik akciğer enfeksiyonu"
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-17-s47",
        "title": "Mycoplasma genitalium Biyolojisi ve İnatçı Üretrit Sorunu",
        "content": "Mycoplasma genitalium, cinsel tıpta son yılların en çok konuşulan dirençli nongonokokal üretrit etkenidir:\n\n- **Biyolojik Özellik:** Doğada serbest yaşayabilen en küçük genomlu bakterilerden biridir. **Hücre duvarı (peptidoglikan tabakası) tamamen YOKTUR**.\n  - Bu hücresel özellik nedeniyle hücre duvar sentezini hedefleyen hiçbir beta-laktam antibiyotik (penisilinler, sefalosporinler) veya vankomisin mikoplazmalara karşı **zerre kadar etki gösteremez (doğal intrinsik direnç)**.\n- **Klinik Tablo:**\n  - Chlamydia trachomatis negatif nongonokokal üretritlerin %15-25'inden sorumludur.\n  - Kadınlarda servisit, endometrit ve pelvik inflamatuvar hastalık (PİH) yapar.\n- **Tanı Güçlüğü:** Kültürde üremesi aylar sürer; bu nedenle pratik klinik tanısı yalnızca **NAAT (PCR)** ile konabilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Mycoplasma genitalium Direnç ve Tedavi Çıkmazı",
                [
                    "1. Hücre Duvarı Yokluğu: Beta-laktamlar (penisilin/sefalosporin) tamamen etkisizdir.",
                    "2. Doksisiklin Yanıtsızlığı: Standart 7 günlük doksisiklin kürü klamidyayı temizlerken M. genitalium'u temizleyemez.",
                    "3. Makrolid Direnci Patlaması: 23S rRNA mutasyonları ile Azitromisin direnci %50'yi aşmıştır.",
                    "4. Dirençli Nüks Üretrit: Hasta standart tedavilere rağmen süregelen akıntıyla hekime döner."
                ]
            ),
            make_cloze(
                "Mycoplasma genitalium bakterisinin hücre duvarı bulunmadığı için penisilin ve sefalosporin grubu antibiyotiklere karşı doğal direnç gösterir.",
                "hücre duvarı",
                "Bakteriye şekil veren ve beta-laktamların hedefi olan yapı"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-17-s48",
        "title": "Mycoplasma genitalium Direnç Yönetimi ve Moksifloksasin",
        "content": "Mycoplasma genitalium enfeksiyonlarında körlemesine azitromisin kullanımı global bir direnç krizine yol açmıştır:\n\n- **Makrolid Direnç Oranları:** Birçok ülkede M. genitalium suşlarında 23S rRNA mutasyonlarına bağlı azitromisin direnci %50-80 seviyelerine ulaşmıştır.\n- **Doksisiklinin Rolü:** Doksisiklin bakteriyi tek başına tam eradike edemez (kür oranı <%30); ancak bakteri yükünü belirgin biçimde düşürür.\n- **Güncel İki Basamaklı Tedavi Kılavuzu (Sınav Spotu):**\n  1. **İlk Adım (Bakteriyel Yük Azaltma):** Doksisiklin 2x100 mg oral, 7 gün verilir.\n  2. **İkinci Adım (Direnç Durumuna Göre Eradikasyon):**\n     - Eğer makrolid direnci saptanmamışsa: Azitromisin (ilk gün 1 g, ardından 3 gün 500 mg).\n     - Eğer makrolid direnci varsa veya direnç testi yapılamıyorsa: **Moksifloksasin 1x400 mg oral, 7 gün** (solunum kinolonu olan moksifloksasin topoizomeraz IV mutasyonunu aşarak %90'ın üzerinde kür sağlar).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Standart Doksisiklin Rejimi vs Moksifloksasin Rejimi",
                "Doksisiklin Tek Başına",
                "Klamidyayı temizler fakat Mycoplasma genitalium'da kür oranı düşüktür; tedavi başarısızlığı sıktır.",
                "Doksisiklin + Moksifloksasin",
                "Bakteri yükü düşürüldükten sonra moksifloksasin eklenerek makrolid dirençli suşlar tamamen eradike edilir."
            ),
            make_quiz(
                "Doksisiklin ve azitromisin tedavisine rağmen üretral akıntısı nükseden ve Mycoplasma genitalium saptanan dirençli bir olguda ikinci basamakta tercih edilen florokinolon hangisidir?",
                [
                    {"key": "A", "text": "Moksifloksasin (1x400 mg, 7 gün)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Makrolid dirençli Mycoplasma genitalium olgularında etkin kür sağlayan ajan moksifloksasindir."},
                    {"key": "B", "text": "Siprofloksasin", "isCorrect": False, "explanation": "Siprofloksasin M. genitalium'a etkisizdir."},
                    {"key": "C", "text": "Metronidazol", "isCorrect": False, "explanation": "Metronidazol bakteriyel mikoplazmaya etkisizdir."},
                    {"key": "D", "text": "Vankomisin", "isCorrect": False, "explanation": "Vankomisin hücre duvarına etki eder, mikoplazmada duvar yoktur."}
                ]
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-17-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Klamidya ve Mikoplazma Tedavileri",
        "content": "Bu checkpointte Chlamydia trachomatis ve Mycoplasma genitalium biyolojisini ve farmakoterapisini özetliyoruz:\n\n- **Yaşam Döngüsü:** Elementer cisim (EB) hücre dışı infeksiyöz form; Retiküler cisim (RB) hücre içi çoğalan formdur.\n- **Serovarlar:** A-C trahom (körlük); D-K ürogenital enfeksiyonlar (üretrit, servisit, PİH, neonatal pnömoni); L1-L3 lenfogranüloma venereum (ağrısız papül, oluk belirtisi, süpüratif bubonlar).\n- **Standart Tedavi:** Azitromisin 1 g oral tek doz VEYA Doksisiklin 2x100 mg 7 gün.\n- **Gebelikte Kural:** Doksisiklin fetusta diş ve kemik hasarı nedeniyle KESİNLİKLE KONTRENDİKEDİR; gebede Azitromisin 1 g tek doz verilir.\n- **Bebek Komplikasyonları:** Doğumdan 5-14 gün sonra konjonktivit; 4-12 hafta sonra ateşsiz stakkato öksürüklü pnömoni.\n- **Mycoplasma genitalium:** Hücre duvarı yoktur; beta-laktamlar etkisizdir; makrolid direnci yüksektir; dirençli olguda Moksifloksasin (7 gün) verilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Enfeksiyon Tipi", "Hedef Patojen", "Birinci Tercih İlaç", "Önemli Kural / Uyarı"],
                [
                    ["Ürogenital Klamidya", "C. trachomatis (D-K)", "Azitromisin 1 g tek doz (veya Doksisiklin 7 gün)", "Hasta uyumunda tek doz avantajı"],
                    ["Gebelikte Klamidya", "C. trachomatis", "Azitromisin 1 g oral tek doz", "Doksisiklin kesin kontrendikedir!"],
                    ["Lenfogranüloma Venereum", "C. trachomatis (L1-L3)", "Doksisiklin 2x100 mg, tam 21 gün", "Uzun süreli tedavi gerektirir"],
                    ["Dirençli Mikoplazma", "Mycoplasma genitalium", "Doksisiklin ardından Moksifloksasin 7 gün", "Makrolid direncini kırma rejimi"]
                ]
            ),
            make_chain(
                "Klamidya ve Mikoplazma Tedavi Algoritması",
                [
                    "1. NGU Şüphesi: Mukoid akıntı ve dizürili hastada NAAT ile etken aranır.",
                    "2. Klamidya Pozitifliği: Azitromisin 1 g tek doz veya Doksisiklin 7 gün başlanır.",
                    "3. Gebe Hasta Ayrımı: Doksisiklin yasaklanır, mutlaka Azitromisin verilir.",
                    "4. Tedavi Yanıtsızlığı: M. genitalium direnci düşünülüp Moksiflosasin başlanır."
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-17-s50",
        "title": "Bölüm Özeti: Klamidyadan Gonokok Direnç Yönetimine Geçiş",
        "content": "Bölüm 5 boyunca klamidya serovarlarını, hücre içi döngüsünü ve mikoplazma direncini inceledik:\n\n- **Kritik İlke:** Gebelikte klamidya tedavisinde doksisiklin yasağı ve azitromisin tercihi en temel kurul spotudur.\n- **Sonraki Bölüm:** Bir sonraki bölümde global antibiyotik direncinin simgesi haline gelen **Neisseria gonorrhoeae enfeksiyonunu, penisilin/kinolon direnç mekanizmalarını ve güncel ikili tedavi rejimlerini** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Chlamydia trachomatis ile enfekte anneden doğan bir bebekte 4-12 haftalıkken ateşsiz gelişen ve kesik kesik nöbetlerle seyreden karakteristik öksürük tipi nedir?",
                "Stakkato öksürük (Staccato cough)",
                "Bebeklik klamidya pnömonisinin tipik öksürük paterni"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi Lenfogranüloma venereum (LGV) tedavisinde önerilen standart ilaç ve tedavi süresidir?",
                [
                    {"key": "A", "text": "Doksisiklin 2x100 mg oral, tam 21 gün", "isCorrect": True, "explanation": "Doğru cevap A'dır: LGV lenfatik tutulumlu derin bir enfeksiyon olduğundan Doksisiklin tedavisi 21 gün sürdürülmelidir."},
                    {"key": "B", "text": "Azitromisin 250 mg tek doz", "isCorrect": False, "explanation": "Doz yetersizdir."},
                    {"key": "C", "text": "Metronidazol 2 g tek doz", "isCorrect": False, "explanation": "Metronidazol klamidyaya etkisizdir."},
                    {"key": "D", "text": "Penisilin G intramusküler tek doz", "isCorrect": False, "explanation": "Penisilin LGV tedavisinde kullanılmaz."}
                ]
            )
        ]
    })

    return slides
