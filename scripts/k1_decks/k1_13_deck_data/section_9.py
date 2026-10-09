# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-13-s81",
        "title": "Biyopsi Alımı ve Patolojiye Gönderim İlkeleri",
        "content": "Granülomatöz ve kronik enflamatuar lezyonlarda patoloğun kesin etiyolojik tanıya ulaşabilmesi, cerrah veya hekimin biyopsiyi doğru almasına ve göndermesine bağlıdır:\n\n- **Temsili Doku (Lezyon Sınırı):** Sadece santral nekroz alanından biyopsi alınırsa mikroskopta yalnızca hücresel döküntü (ölü doku) görülür ve tanı konulamaz. Biyopsi mutlaka nekroz ile sağlam dokunun kesiştiği **aktif granülom çeperini (canlı epiteloid sınır)** içermelidir.\n- **Doku Fiksasyonu:** Işık mikroskopisi için doku derhal **%10'luk tamponlu nötral formalin** solüsyonuna konmalıdır (doku hacminin en az 10-20 katı hacimde formalin).\n- **Mikrobiyolojiye Ayrı Parça:** Tüberküloz ve mantar şüphesinde dokunun bir kısmı kesinlikle formaline konmadan, **steril serum fizyolojik içinde taze olarak mikrobiyoloji laboratuvarına (kültür ve PCR için)** gönderilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Nekroz Merkezi Biyopsisi vs Aktif Çeper Biyopsisi",
                "Yalnızca Santral Nekroz Biyopsisi",
                "Mikroskopta sadece amorf hücre enkazı görülür; granülom mimarisi ve dev hücreler seçilemez.",
                "Aktif Çeperi İçeren Biyopsi",
                "Epiteloid histiositler, dev hücreler, lenfosit mantosu ve nekroz ilişkisi eksiksiz incelenir."
            ),
            make_cloze(
                "Granülomatöz lezyon biyopsilerinde ışık mikroskobik inceleme için standart doku tespit solüsyonu yüzde onluk tamponlu nötral formalindir.",
                "nötral formalin",
                "Standart patoloji fiksatif solüsyonu"
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-13-s82",
        "title": "H&E Boyasında Epiteloid Hücre, Dev Hücre ve Nekroz",
        "content": "Rutin patolojide kullanılan temel boya Hematoksilen & Eozin (H&E)'dir. H&E boyasında granülomun üç temel bileşeni şu şekilde ayırt edilir:\n\n1. **Hematoksilen (Bazik Boya):** Nükleik asitleri (DNA/RNA) boyar. Lenfosit çekirdeklerini koyu mavi/mor boyayarak perivasküler alanda yoğun koyu halkalar şeklinde gösterir.\n2. **Eozin (Asidik Boya):** Sitoplazmik proteinleri boyar. Epiteloid histiositlerin zengin sitoplazmasını ve Langhans dev hücrelerini **canlı pembe (eozinofilik)** boyar.\n3. **Kazeöz Nekroz:** Hücre çekirdekleri parçalandığı için bazofili (mavi boyanma) kaybolur; geride kalan nükleus artıkları hafif mor noktalı granüller şeklinde parlar ve zemin tamamen **amorf pembe** bir enkaz olarak izlenir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Doku Bileşeni", "H&E Boyanma Karakteri", "Işık Mikroskobu Görünümü"],
                [
                    [
                        {"text": "Lenfosit Çekirdekleri", "isMasked": False, "hint": ""},
                        {"text": "Koyu bazofilik (Hematoksilen)", "isMasked": False, "hint": ""},
                        {"text": "Koyu mor, yuvarlak hiperkromatik odaklar", "isMasked": True, "hint": "Hematoksilenin mavi-mor nükleer rengi"}
                    ],
                    [
                        {"text": "Epiteloid Histiosit Sitoplazması", "isMasked": False, "hint": ""},
                        {"text": "Canlı eozinofilik (Eozin)", "isMasked": True, "hint": "Eozinin pembe sitoplazma rengi"},
                        {"text": "Geniş, soluk pembe sinsityal kordonlar", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kazeifikasyon Nekrozu", "isMasked": True, "hint": "Hücre konturları silinmiş nekroz"},
                        {"text": "Amorf granüler eozinofilik", "isMasked": False, "hint": ""},
                        {"text": "Hücresiz, pembe enkaz alanı", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Standart H&E boyasında nükleusları koyu mavi-mor renge boyayan bazik boya maddesi hangisidir?",
                "Hematoksilendir.",
                "Rutin patolojinin çekirdek boyası"
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-13-s83",
        "title": "Asit-Fast Boyama: Ehrlich-Ziehl-Neelsen ve Kinyoun",
        "content": "Kazeöz nekrozlu bir granülomda Mycobacterium tuberculosis veya Mycobacterium leprae varlığını kanıtlamak için Asit-Fast (Aside Dirençli) boyama protokolleri uygulanır:\n\n- **Ehrlich-Ziehl-Neelsen (EZN) Tekniği (Sıcak Yöntem):**\n  1. Kesit üzerine primer boya olan **Karbol Fuksin** damlatılır ve buhar çıkana kadar alttan alevle ısıtılır (ısı mikolik asit lipidlerini gevşetir).\n  2. Kesit **asit-alkol (%3 HCl + %95 Etanol)** solüsyonu ile yıkanır. Mikobakteriler boyayı bırakmaz, diğer tüm hücreler solar.\n  3. Zıt boya olarak **Metilen Mavisi** uygulanır.\n  4. Sonuç: Mavi zemin üzerinde ince, uzun, kıvrık **parlak kırmızı basiller**.\n- **Kinyoun Yöntemi (Soğuk Yöntem):** Karbol fuksin konsantrasyonu artırılarak ısıtma yapılmadan uygulanan modifiye tekniktir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Ehrlich-Ziehl-Neelsen (EZN) Boyama Aşamaları",
                [
                    "1. Karbol Fuksin ve Isıtma: Boya dokuya damlatılıp ısıtılarak mikolik asit bariyeri aşılır.",
                    "2. Asit-Alkol Dekolorizasyonu: Asitli alkol uygulanır; zayıf hücreler solar, basil boyayı tutar.",
                    "3. Metilen Mavisi Zıt Boyama: Arka plan dokusu ve nötrofiller maviye boyanır.",
                    "4. Mikroskobik Teşhis: Mavi zemin üzerinde parlak kırmızı tüberküloz basilleri taranır."
                ]
            ),
            make_quiz(
                "Ehrlich-Ziehl-Neelsen boyamasında mikobakterilerin asit-alkol solüsyonu ile rengini kaybetmeyip kırmızı kalmasını sağlayan hücre duvarı biyokimyasal bileşeni nedir?",
                [
                    {"key": "A", "text": "Mikolik asit ve kompleks mumsu lipidler", "explanation": "A seçeneği DOĞRUDUR: Mikolik asit karbol fuksini sıkıca bağlar ve asit-alkolde solmasını engeller."},
                    {"key": "B", "text": "Peptidoglikan tabakasının kalınlığı", "explanation": "B seçeneği yanlıştır: Gram pozitifliğin temelidir, asit direncini açıklamaz."},
                    {"key": "C", "text": "Kapsül polisakkaritleri", "explanation": "C seçeneği yanlıştır: Kapsül boyaları çini mürekkebi ile gösterilir."},
                    {"key": "D", "text": "Teykoik asit", "explanation": "D seçeneği yanlıştır: Stafilokok duvar bileşenidir."},
                    {"key": "E", "text": "Endotoksin lipopolisakkariti", "explanation": "E seçeneği yanlıştır: Gram negatif dış membran yapısıdır."}
                ],
                "A"
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-13-s84",
        "title": "Mantar ve Karbonhidrat Boyaları: GMS ve PAS",
        "content": "Kazeifiye granülomlarda tüberküloz dışlandıktan sonra ikinci büyük şüpheli mantarlardır. Mantar tanısında iki klasik histokimyasal boya vazgeçilmezdir:\n\n1. **Gomori Metenamin Gümüş (GMS - Grocott):**\n   - Mantar hücre duvarındaki glikoproteini kromik asit ile okside eder; açığa çıkan aldehit grupları gümüş iyonlarını metalik gümüşe indirger.\n   - **Sonuç (Sınav Spotu):** Mantar hücre duvarı, hifleri ve sporları açık yeşil zemin üzerinde **kömür siyahı (keskin siyah)** renkte parlar.\n2. **Periyodik Asit Schiff (PAS):**\n   - Periyodik asit glikol gruplarını aldehite çevirir; Schiff reaktifi ile **parlak macenta kırmızısı (pembe-eflatun)** boyanma elde edilir.\n   - Mantar sporlarını ve bazal membranları çok net gösterir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "GMS Gümüşleme vs PAS Boyası Karşılaştırması",
                "Gomori Metenamin Gümüş (GMS)",
                "Mantar duvarını kömür siyahı boyar; açık yeşil fonda mantar taraması için en yüksek kontrastı verir.",
                "Periyodik Asit Schiff (PAS)",
                "Mantar duvarını parlak macenta pembesi boyar; bazal membran ve mukus eşliğini de gösterir."
            ),
            make_cloze(
                "Mantar enfeksiyonu şüpheli granülom kesitlerinde mantar duvarını kömür siyahı renge boyayan gümüşleme yöntemine Grocott metenamin gümüş boyası denir.",
                "metenamin gümüş",
                "GMS boyasının açılımındaki kimyasal ad"
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-13-s85",
        "title": "Sifiliz ve Treponema Tespiti: Warthin-Starry Gümüşleme",
        "content": "Tersiyer sifiliz gomlarında veya primer şankr lezyonlarında etken spiroket olan **Treponema pallidum** son derece ince ve helezonik yapılıdır:\n\n- **Işık Mikroskobu Yetersizliği:** Treponema pallidum standart H&E boyasında ışık kırılma indeksi dokuya çok yakın olduğu için ASLA görülemez.\n- **Warthin-Starry Gümüş Boyası (Sınav Spotu):** Kesite gümüş nitrat uygulanır; spiroketlerin ince tirbüşon şeklindeki helezonik gövdeleri gümüşle kaplanarak sarı-kahverengi zemin üzerinde **kıvrık siyah iplikçikler** halinde görünür hale getirilir.\n- **Alternatif Yöntem:** Taze lezyon sıvısında **Karanlık Saha Mikroskopisi** ile spiroketlerin tirbüşon gibi dönme hareketleri canlı olarak izlenebilir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Sifiliz gom lezyonunda veya primer şankrda Treponema pallidum spiroketlerini dokuda siyah helezonik iplikçikler olarak gösteren klasik gümüşleme boyası hangisidir?",
                [
                    {"key": "A", "text": "Warthin-Starry gümüş boyası", "explanation": "A seçeneği DOĞRUDUR: Warthin-Starry ve Levaditi gümüş boyaları Treponema pallidum ve Bartonella henselae tespiti için kullanılır."},
                    {"key": "B", "text": "Prusya mavisi", "explanation": "B seçeneği yanlıştır: Demir pigmenti boyasıdır."},
                    {"key": "C", "text": "Kongo kırmızısı", "explanation": "C seçeneği yanlıştır: Amiloid boyasıdır."},
                    {"key": "D", "text": "Trikrom Masson", "explanation": "D seçeneği yanlıştır: Bağ doku kollajen boyasıdır."},
                    {"key": "E", "text": "Sudan siyahı", "explanation": "E seçeneği yanlıştır: Nötral lipid boyasıdır."}
                ],
                "A"
            ),
            make_recall(
                "Treponema pallidum spiroketlerinin biyopsi kesiti gerektirmeden eksüda sıvısında tirbüşon hareketleriyle canlı incelenmesini sağlayan optik mikroskopi tekniği nedir?",
                "Karanlık saha mikroskopisidir (dark-field microscopy).",
                "Spiroket hareketini gösteren canlı mikroskopi yöntemi"
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-13-s86",
        "title": "Bağ Dokusu ve Fibrozis Boyaları: Masson Trikrom ve EVG",
        "content": "Kronik enflamasyonun evrelenmesinde ve dokudaki fibrozis miktarının ölçülmesinde özel bağ dokusu boyaları kullanılır:\n\n1. **Masson Trikrom Boyası (Sınav Spotu):**\n   - Karaciğer biyopsilerinde (kronik hepatit/siroz) fibrozis evrelemesinde altın standarttır.\n   - **Hücresel Parankim ve Kas:** Kırmızı renge boyanır.\n   - **Kollajen Lifleri (Fibrozis):** Parlak **Mavi** (veya yeşil) renge boyanır.\n   - **Çekirdekler:** Siyah/koyu kahverengi boyanır.\n2. **Elastik Van Gieson (EVG) / Verhoeff:**\n   - Damar elastik liflerini **siyah** boyar; dev hücreli temporal arteritte lamina elastica internanın parçalanıp koptuğunu kanıtlamada kullanılır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Standart H&E vs Masson Trikrom Karşılaştırması",
                "Standart H&E",
                "Kollajen pembe, kas pembe, sitoplazma pembe görünür; erken fibrozisi seçmek güçtür.",
                "Masson Trikrom",
                "Kollajeni parlak mavi, kas ve parankimi kırmızı boyayarak fibrozis miktarını kusursuz gösterir."
            ),
            make_cloze(
                "Karaciğer biyopsisinde siroz ve fibrozis evrelemesinde kollajen liflerini parlak mavi renge boyayan özel boya Masson trikrom boyasıdır.",
                "Masson trikrom",
                "Üçlü bağ doku ve fibrozis boyası"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-13-s87",
        "title": "İmmünohistokimya (İHK) Belirteçleri: Hücrelerin Kimlik Kartları",
        "content": "Işık mikroskobunda birbirine benzeyen mononükleer hücrelerin kesin türünü tayin etmek için yüzey ve sitoplazmik antijenlere özgül monoklonal antikorlar (İHK) kullanılır:\n\n- **Makrofaj ve Epiteloid Hücre Belirteçleri:**\n  - **CD68:** Lizozomal glikoproteindir; tüm monosit ve makrofaj soyunda kuvvetli pozitiftir.\n  - **CD163:** Özellikle alternatif aktive (M2) makrofajlarda yüksek oranda eksprese edilen temizleyici (scavenger) reseptördür.\n- **Lenfosit Belirteçleri:**\n  - **CD3:** Tüm **T lenfositlerinin** pan-T belirtecidir.\n  - **CD4 ve CD8:** Yardımcı ve sitotoksik T alt gruplarını ayırır.\n  - **CD20:** Tüm **B lenfositlerinin** pan-B belirtecidir.\n  - **CD138:** **Plazma hücrelerinin** kesin immünohistokimyasal kimlik kartıdır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İHK Belirteci (Antijen)", "Pozitif Boyanan Hücre Tipi", "Klinik / Patolojik Kullanımı"],
                [
                    [
                        {"text": "CD68 ve CD163", "isMasked": False, "hint": ""},
                        {"text": "Makrofajlar ve epiteloid histiositler", "isMasked": True, "hint": "Granülomun temel hücresel kökeni"},
                        {"text": "Granülom ve histiositik infiltratın doğrulanması", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "CD3", "isMasked": True, "hint": "Pan-T lenfosit belirteci"},
                        {"text": "Tüm T Lenfositleri", "isMasked": False, "hint": ""},
                        {"text": "T-hücre infiltrasyonunun ve manto zonunun gösterilmesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "CD138", "isMasked": False, "hint": ""},
                        {"text": "Plazma hücreleri", "isMasked": True, "hint": "Saat kadranı çekirdekli antikor hücresi"},
                        {"text": "Sifiliz, plazmositom ve kronik endometrit tanısı", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Granülomatöz bir lezyonda epiteloid histiositlerin ve dev hücrelerin mononükleer fagosit kökenini kanıtlayan en yaygın pan-makrofaj İHK belirteci nedir?",
                "CD68'dir (ayrıca CD163).",
                "Makrofajların klasik Cluster of Differentiation numarası"
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-13-s88",
        "title": "Moleküler Patoloji ve PCR: Doku DNA Tanısı",
        "content": "Histopatolojik boyalarla etkenin gösterilemediği (paucibacillary tüberküloz, lepra, atipik mikobakteriler) olgularda moleküler patoloji devreye girer:\n\n- **Formalinle Fikse Parafine Gömülü (FFPE) Bloktan PCR:** Arşivdeki parafin bloktan kesilen mikrotom kesitlerinden mikrobiyal DNA izole edilir.\n- **Tüberküloz PCR (IS6110 Dizisi):** M. tuberculosis genomunda çok sayıda kopyası bulunan IS6110 insersiyon sekansı hedeflenerek tek bir basil DNA'sı dahi amplifiye edilebilir.\n- **İlaç Direnci Mutasyonları:** Moleküler testlerle dokudaki basilin rifampisin (rpoB geni mutasyonu) ve izoniazid (katG / inhA mutasyonları) direnci saatler içinde saptanır.\n- **Kültür ile Karşılaştırma:** Kültür 4-6 hafta sürerken PCR sonuçları 24 saatte çıkar; hasta derhal doğru tedaviye başlanabilir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Histokimyasal Boya (EZN) vs Moleküler PCR",
                "Histokimyasal Boya (EZN)",
                "Kesitte mm3'te en az 10.000 basil gerektirir; duyarlılığı düşüktür (%30-50).",
                "Moleküler Polimeraz Zincir Reaksiyonu (PCR)",
                "Doku kesitinde birkaç basil DNA'sını dahi saptar; duyarlılığı ve özgüllüğü olağanüstü yüksektir."
            ),
            make_cloze(
                "Parafin blok doku kesitlerinden tüberküloz basil DNA'sının çoğaltılarak saptanmasında en sık hedeflenen genomik dizi IS6110 insersiyon sekansıdır.",
                "IS6110",
                "Tüberküloz PCR testinin hedef dizi adı"
            )
        ]
    })

    # Slide 89
    slides.append({
        "id": "k1-13-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Histopatolojik Yöntemler, Özel Boyalar ve Tanı Algoritmaları",
        "content": "Bu kontrol noktasında granülomatöz ve kronik enflamasyon patolojisinde kullanılan histokimyasal, immünohistokimyasal ve moleküler yöntemleri özetliyoruz:\n\n- **H&E:** Epiteloid hücre (pembe sitoplazma), lenfosit (koyu mor çekirdek), kazeöz nekroz (amorf pembe enkaz).\n- **Asit-Fast (EZN/Kinyoun):** Mikolik asit tutulumu → mavi zemin üzerinde parlak kırmızı mikobakteri basilleri.\n- **GMS / PAS:** Mantar hücre duvarı polisakkaritleri → GMS ile kömür siyahı, PAS ile parlak macenta pembesi.\n- **Warthin-Starry:** Gümüşleme ile Treponema pallidum (sifiliz) ve Bartonella (kedi tırmığı) spiroket/basilleri siyah görünür.\n- **Masson Trikrom:** Fibrozis ve kollajen parlak mavi boyanır.\n- **İHK Belirteçleri:** CD68 (makrofaj), CD3 (T hücresi), CD20 (B hücresi), CD138 (plazma hücresi).\n- **PCR:** Parafin bloktan IS6110 hedefli hızlı tüberküloz DNA tespiti.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Karaciğer biyopsisinde kronik hepatite bağlı fibrozis ve parankim mimari bozukluğunu değerlendirmede kollajeni maviye boyayan altın standart boya hangisidir?",
                [
                    {"key": "A", "text": "Masson trikrom boyası", "explanation": "A seçeneği DOĞRUDUR: Masson trikrom kollajen liflerini mavi boyayarak fibrozisi gösterir."},
                    {"key": "B", "text": "Ziehl-Neelsen boyası", "explanation": "B seçeneği yanlıştır: Tüberküloz asit boyasıdır."},
                    {"key": "C", "text": "Metenamin gümüş boyası", "explanation": "C seçeneği yanlıştır: Mantar boyasıdır."},
                    {"key": "D", "text": "Prusya mavisi", "explanation": "D seçeneği yanlıştır: Hemosiderin demirini gösterir."},
                    {"key": "E", "text": "Toluidin mavisi", "explanation": "E seçeneği yanlıştır: Mast hücresi metakromazi boyasıdır."}
                ],
                "A"
            ),
            make_cloze(
                "İmmünohistokimyasal boyamada T lenfositleri pan-T belirteci olan CD3 ile, B lenfositleri pan-B belirteci olan CD20 ile ayırt edilir.",
                "CD20",
                "B lenfositlerinin majör Cluster of Differentiation numarası"
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-13-s90",
        "title": "Granülomatöz Lenfadenopati Ayırıcı Tanı Ağacı",
        "content": "Klinikte lenf düğümü biyopsisinde granülom saptandığında patolog ve hekim şu tanısal karar ağacını izler:\n\n1. **Adım 1: Nekroz Var mı?**\n   - **Nekroz YOK (Non-kazeöz):** Öncelikle **Sarkoidoz** (çıplak granülomlar, hiler LAP), Berilyozis, Crohn hastalığı veya yabancı cisim düşünülür.\n   - **Nekroz VAR:** Adım 2'ye geçilir.\n2. **Adım 2: Nekrozun Niteliği Nedir?**\n   - **Kazeöz (Amorf Pembe) Nekroz:** Öncelikle **Tüberküloz** ve mantarlar (Histoplazmoz) düşünülür; EZN ve GMS boyanır.\n   - **Süpüratif (Nötrofilik) Nekroz:** Öncelikle **Kedi Tırmığı Hastalığı** (stellat granülom, Bartonella), Tularemi veya Lenfogranüloma Venereum (LGV) düşünülür; Warthin-Starry ve seroloji istenir.\n3. **Adım 3: Polarize Işık:** Tüm olgularda yabancı cisim ve sütür ekarte edilir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Boyunda ağrısız lenfadenopati nedeniyle çıkarılan lenf düğümünün histopatolojik incelemesinde epiteloid histiositlerden oluşan granülomlar izleniyor. Granülom merkezlerinde hiçbir nekroz alanı görülmüyor ve lenfosit mantosu oldukça zayıf (çıplak granülom).",
                "Bu hastada ilk olarak düşünülmesi gereken ve akciğer grafisiyle taranması gereken öncelikli hastalık hangisidir?",
                [
                    {
                        "text": "Sarkoidozdur (Bilateral hiler lenfadenopati taranmalıdır).",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Non-kazeöz çıplak granülomların en sık nedeni sarkoidozdur; bilateral hiler LAP tipiktir."
                    },
                    {
                        "text": "Primer akciğer tüberkülozudur.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Tüberküloz kural olarak amorf kazeifikasyon nekrozu içerir."
                    },
                    {
                        "text": "Kedi tırmığı hastalığıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Kedi tırmığı merkezinde yoğun nötrofilik püy içeren süpüratif granülom yapar."
                    }
                ]
            ),
            make_recall(
                "Lenf düğümü granülomatöz lezyonunda merkezde kazeöz nekroz yerine nötrofilik mikroapse ve nükleer debris varlığı ilk olarak hangi enfeksiyonu düşündürmelidir?",
                "Kedi tırmığı hastalığıdır (Bartonella henselae / stellat süpüratif granülom).",
                "Nötrofilli yıldızsı granülomun primer etkeni"
            )
        ]
    })

    return slides
