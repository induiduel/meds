# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 5: Sistemik Lupus Eritematozus (SLE): Etyopatogenez, Otoantikorlar ve Organ Patolojisi (Slayt 41 - 50)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_5_slides():
    slides = []

    # Slayt 41: Sistemik Lupus Eritematozus: Tanım, Epidemiyoloji ve Genetik Zemin
    slides.append({
        "id": "k1-25-s41",
        "title": "Sistemik Lupus Eritematozus: Tanım, Epidemiyoloji ve Genetik Zemin",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 41,
        "narrative": (
            "Sistemik Lupus Eritematozus (SLE), poliklonal B hücresi hiperaktivitesi, antinükleer otoantikorlar (ANA) "
            "ve yaygın immün kompleks vaskülitiyle karakterize prototip sistemik otoimmün hastalıktır: "
            "1. **Epidemiyolojik Karakter:** En sık doğurganlık çağındaki genç kadınlarda görülür (Kadın / Erkek oranı **9:1**). "
            "Afrika ve Asya kökenlilerde daha sık ve ağır seyreder. Klinik tablo alevlenmeler (relaps) ve yatışmalarla (remisyon) ilerler. "
            "2. **Genetik Yatkınlık:** "
            "- **HLA Allelleri:** HLA-DR2 ve HLA-DR3 taşıyıcılarında göreceli risk 2-3 kat artmıştır. "
            "- **Kompleman Eksiklikleri:** Erken klasik yolak kompleman proteinleri olan **C1q, C2 veya C4** kalıtsal eksikliğinde "
            "hastalarda %90'a varan oranda lupus gelişir. Çünkü bu moleküller apoptotik hücre enkazlarının kandan temizlenmesinden sorumludur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "SLE Etyopatogenezinde Genetik ve İmmün Faktörler",
                ["Faktör Kategorisi", "Moleküler / Genetik Bileşen", "Bozulan İmmünolojik Fonksiyon", "Klinik Yansıması"],
                [
                    ["Kompleman Genleri", "C1q, C2, C4 eksikliği", "Apoptotik hücrelerin fagositlerce temizlenememesi", "Nükleer antijen birikimi"],
                    [
                        "Doku Uygunluk Grubu",
                        "HLA-DR2 ve HLA-DR3",
                        {"text": "Otoantijenlerin T hücrelerine aşırı sunumu", "isMasked": True, "hint": "SLE gelişiminde en güçlü genetik yatkınlığı oluşturan HLA allelleri"},
                        "Antinükleer antikor fırtınası"
                    ],
                    ["Cinsiyet Hormonları", "Östrojen hakimiyeti", "B lenfosit hiperaktivitesi ve apoptoz direnci", "Genç kadınlarda 9 kat sıklık"]
                ]
            ),
            make_active_recall(
                "Genetik olarak C1q, C2 veya C4 eksikliği olan bireylerde apoptotik hücre enkazlarının temizlenememesi sonucu en sık gelişen otoimmün hastalık hangisidir?",
                "Sistemik Lupus Eritematozustur (SLE).",
                "Kelebek döküntüsü ve multiorgan nefritiyle seyreden sistemik otoimmün sendrom"
            )
        ]
    })

    # Slayt 42: SLE Patogenezi: Apoptotik Debris ve Tip I İnterferon İmzası
    slides.append({
        "id": "k1-25-s42",
        "title": "SLE Patogenezi: Apoptotik Debris ve Tip I İnterferon İmzası",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 42,
        "narrative": (
            "SLE patogenezinin merkezinde, temizlenemeyen hücre çekirdeklerinin doğuştan bağışıklık sistemini uyarması yer alır: "
            "1. **UV Işığı ve Apoptoz:** Güneş ışığı (ultraviyole radyasyon) keratinositlerde DNA hasarı ve masif apoptoz tetikler. "
            "Apoptotik veziküllerdeki nükleer antijenler (DNA, RNA, histonlar) yüzeye çıkar. "
            "2. **TLR-7 ve TLR-9 Aktivasyonu:** Nükleer antijenleri içeren immün kompleksler, plazmasitoid dendritik hücrelerin "
            "endozomlarındaki **TLR-7 (RNA bağlar)** ve **TLR-9 (DNA bağlar)** reseptörlerine kenetlenir. "
            "3. **Tip I İnterferon (IFN-alfa) İmzası:** Plazmasitoid dendritik hücreler devasa miktarda **Tip I İnterferon (IFN-alfa)** salgılar. "
            "IFN-alfa, B lenfositlerini kontrolsüz uyararak daha fazla antinükleer antikor üretmelerini sağlar; böylece otoantikor kaskadı sonsuz bir döngüye girer."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "SLE Tip I İnterferon Kaskadı",
                [
                    "1. UV Hasarı ve Apoptoz: Güneş ışığıyla keratinosit apoptozu ve serbest nükleer partikül saçılması",
                    "2. İmmün Kompleks Girişi: DNA/RNA içeren pıhtıların dendritik hücre endozomuna alınması",
                    "3. TLR-7 / TLR-9 Uyarımı: Endozomal reseptörlerin nükleik asitleri algılayıp uyarılması",
                    "4. Masif IFN-alfa Üretimi: 'İnterferon imzası' ile B lenfosit poliklonal aktivasyonunun alevlenmesi"
                ]
            ),
            make_cloze(
                "SLE patogenezinde plazmasitoid dendritik hücrelerin TLR-7 ve TLR-9 aktivasyonuyla masif salgıladığı ve interferon imzasını oluşturan sitokin IFN-alfa molekülüdür.",
                "IFN-alfa",
                "Tip I interferon ailesinin en güçlü B hücresi aktive edici üyesi"
            )
        ]
    })

    # Slayt 43: SLE Otoantikor Profili ve Klinik Anlamları
    slides.append({
        "id": "k1-25-s43",
        "title": "SLE Otoantikor Profili ve Klinik Anlamları",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 43,
        "narrative": (
            "SLE'de üretilen otoantikorların her birinin tanısal duyarlılığı ve organ tutulum korelasyonu farklıdır: "
            "1. **Antinükleer Antikorlar (ANA):** Hastaların **%95-98'inde pozitiftir**. Taramada ilk adımdır ve duyarlılığı en yüksek "
            "testtir; ancak sağlıklı bireylerde veya diğer romatolojik hastalıklarda da pozitifleşebildiğinden spesifik değildir (ANA negatifse SLE dışlanır). "
            "2. **Anti-dsDNA (Çift Sarmallı DNA):** SLE için oldukça spesifiktir (%70 sıklık). Titresi **lupus nefriti** varlığı ve "
            "hastalık alevlenmesi ile doğrudan paralel seyreder. "
            "3. **Anti-Smith (Anti-Sm):** Çekirdek ribonükleoproteinlerine karşıdır. SLE için **en spesifik** antikordur (%99 spesifisite); "
            "fakat hastaların yalnızca %25'inde saptanır (düşük duyarlılık). "
            "4. **Anti-Ro (SSA) ve Anti-La (SSB):** Subakut kutanöz lupus, neonatal lupus ve bebekte **konjenital kalp bloğu** ile ilişkilidir. "
            "5. **Anti-Histon Antikorları:** İlaca bağlı lupusta (prokainamid, hidralazin, izoniazid) **>%95 pozitiftir**."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "SLE Otoantikor Spektrumu ve Klinik Özellikleri",
                ["Otoantikor Tipi", "Duyarlılık / Spesifisite", "Klinik Patolojik Korelasyon"],
                [
                    ["ANA (İndirekt İmmünofloresan)", "%98 Duyarlı / Düşük Spesifisite", "Negatifse SLE tanısını dışlar (tarama testi)"],
                    [
                        "Anti-dsDNA",
                        "Yüksek Spesifisite (%70)",
                        {"text": "Lupus nefriti ve hastalık alevlenmesi", "isMasked": True, "hint": "Böbrek tutulumunun ciddiyetini ve relapsı takip eden antikor"}
                    ],
                    ["Anti-Smith (Anti-Sm)", "%99 Spesifik / %25 Duyarlı", "SLE tanısını kesinleştiren en spesifik belirteç"],
                    ["Anti-Histon", "%95 Pozitif (İlaca Bağlı)", "Hidralazin, prokainamid kullanımına bağlı lupus"],
                    ["Anti-Ro (SSA) / Anti-La (SSB)", "%30 - 40 Pozitif", "Neonatal lupus, konjenital kalp bloğu, Sjögren"]
                ]
            ),
            make_active_recall(
                "Sistemik Lupus Eritematozus için duyarlılığı düşük (%25) olmasına rağmen tanısal spesifisitesi yaklaşık yüzde doksan dokuz olan en spesifik otoantikor hangisidir?",
                "Anti-Smith (Anti-Sm) antikorudur.",
                "Çekirdek ribonükleoprotein çekirdek kompleksine karşı gelişen spesifik antikor"
            )
        ]
    })

    # Slayt 44: Antifosfolipid Antikorları ve Antifosfolipid Sendromu
    slides.append({
        "id": "k1-25-s44",
        "title": "Antifosfolipid Antikorları ve Antifosfolipid Sendromu (APS)",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 44,
        "narrative": (
            "SLE hastalarının yaklaşık üçte birinde fosfolipid-protein komplekslerine karşı antikorlar saptanır: "
            "1. **Antikor Türleri:** Lupus antikoagülanı, anti-kardiolipin antikorları ve anti-beta2-glikoprotein I antikorlarıdır. "
            "2. **Laboratuvar Paradoksu:** Bu antikorlar laboratuvar tüpünde fosfolipidleri bağlayarak koagülasyon testlerini "
            "(özellikle aktive parsiyel tromboplastin zamanı / **aPTT**) yapay olarak **uzatır** (antikoagülan gibi görünür). "
            "Ancak canlı vücudunda (in vivo) tam aksine endoteli aktive edip trombositi uyararak **masif trombozlara** yol açar! "
            "3. **Antifosfolipid Sendromu (APS) Kliniği:** Tekrarlayan arteriyel ve venöz trombozlar (DVT, inme), trombositopeni ve "
            "plasental enfarktüslere bağlı **tekrarlayan fetal kayıplar (düşükler)** gelişir. "
            "4. **Yalancı Sifiliz Pozitifliği:** Kardiolipin sifiliz testinde (VDRL/RPR) antijen olarak kullanıldığından bu hastalarda yalancı pozitiflik verir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Antifosfolipid Antikorlarının İkili Yüzü",
                "İn Vitro (Tüp İçinde Laboratuvar)",
                "Koagülasyon testlerinde fosfolipidi bağlayarak aPTT süresini yapay olarak uzatır",
                "İn Vivo (Canlı Vücudunda Klinik)",
                "Trombosit ve endoteli tetikleyerek masif venöz/arteriyel tromboz ve tekrarlayan gebelik kayıpları yapar"
            ),
            make_micro_quiz(
                "SLE tanılı genç bir kadın hastada aPTT süresinin uzamış olmasına rağmen bacakta derin ven trombozu (DVT) ve 3 kez tekrarlayan spontan düşük öyküsü saptanıyor. Bu klinik paradokstan sorumlu otoantikor grubu hangisidir?",
                {
                    "A": "Antifosfolipid antikorları (Lupus antikoagülanı)",
                    "B": "Anti-sentromer antikorları",
                    "C": "Anti-Jo-1 antikorları",
                    "D": "Anti-Scl-70 antikorları",
                    "E": "Anti-mitokondriyal antikorlar (AMA)"
                },
                "A",
                {
                    "A": "Doğrudur; antifosfolipid antikorları in vitro aPTT uzatırken in vivo tromboz ve gebelik kayıpları yapan paradoksal etkiye sahiptir.",
                    "B": "Yanlış; anti-sentromer CREST sendromuna özgüdür.",
                    "C": "Yanlış; anti-Jo-1 dermatomiyozit belirtecidir.",
                    "D": "Yanlış; anti-Scl-70 diffüz skleroderma belirtecidir.",
                    "E": "Yanlış; AMA primer biliyer kolanjit belirtecidir."
                }
            )
        ]
    })

    # Slayt 45: Lupus Nefriti: ISN/RPS Sınıflaması I'den VI'ya
    slides.append({
        "id": "k1-25-s45",
        "title": "Lupus Nefriti: ISN/RPS Sınıflaması I'den VI'ya",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 45,
        "narrative": (
            "Lupus hastalarında morbidite ve mortaliteyi belirleyen en kritik organ tutulumu böbrektir (Lupus Nefriti): "
            "Uluslararası Nefroloji Derneği (ISN/RPS) sınıflamasına göre böbrek tutulumu altı sınıfta incelenir: "
            "1. **Sınıf I (Minimal Mezangiyal):** Işık mikroskopisi normaldir; mezangiyumda immün birikim vardır. "
            "2. **Sınıf II (Mezangiyal Proliferatif):** Mezangiyal hücre artışı ve matriks genişlemesi izlenir. "
            "3. **Sınıf III (Fokal Lupus Nefriti):** Glomerüllerin **<%50'sinde** segmental veya global endokapiller proliferasyon vardır. "
            "4. **Sınıf IV (Diffüz Proliferatif Nefrit - DPN):** **En sık görülen (%40-50) ve en ağır sınıftır**. "
            "Glomerüllerin **>%50'si** tutulmuştur; masif proliferasyon, kresentler ve böbrek yetmezliği tablosu gelişir. "
            "5. **Sınıf V (Membranöz Nefrit):** Glomerül bazal membranında diffüz kalınlaşma ve masif nefrotik sendrom izlenir. "
            "6. **Sınıf VI (İlerlemiş Sklerozan):** Glomerüllerin >%90'ı skleroza uğramıştır; son dönem böbrek yetmezliğidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Lupus Nefriti ISN/RPS Histopatolojik Sınıflaması",
                ["Sınıf Numarası", "Sınıf Adı", "Glomerül Tutulum Oranı", "Temel Histopatolojik / Klinik Özellik"],
                [
                    ["Sınıf I", "Minimal Mezangiyal", "Çok az / Mezangiyal", "Işık mikroskopisi normal, mikroskopik hematüri"],
                    ["Sınıf II", "Mezangiyal Proliferatif", "Mezangiyum odaklı", "Mezangiyal matriks artışı, hafif proteinüri"],
                    ["Sınıf III", "Fokal Lupus Nefriti", "Glomerüllerin <%50'si", "Segmental endokapiller nekroz ve proliferasyon"],
                    [
                        "Sınıf IV",
                        "Diffüz Proliferatif (DPN)",
                        {"text": "Glomerüllerin >%50'si", "isMasked": True, "hint": "En yaygın, en ağır ve tel halkası lezyonlarının görüldüğü sınıf"},
                        "En sık ve en ağır sınıf; hipertansiyon, azotemi"
                    ],
                    ["Sınıf V", "Membranöz Nefrit", "Diffüz bazal membran", "Masif nefrotik sendrom, spike-dome manzarası"],
                    ["Sınıf VI", "İlerlemiş Sklerozan", "Glomerüllerin >%90'ı", "Kalıcı glomerüloskleroz, son dönem yetmezlik"]
                ]
            ),
            make_active_recall(
                "Sistemik Lupus Eritematozus hastalarında yapılan böbrek biyopsilerinde en sık karşılaşılan ve prognozu en kötü olan diffüz proliferatif lupus nefriti hangi sınıftır?",
                "Sınıf IV (Diffüz Proliferatif Lupus Nefriti) sınıfıdır.",
                "Glomerüllerin yüzde ellisinden fazlasını tutan dördüncü evre nefrit"
            )
        ]
    })

    # Slayt 46: Lupus Nefritinde Tel Halkası ve Full-House Paterni
    slides.append({
        "id": "k1-25-s46",
        "title": "Lupus Nefritinde Tel Halkası ve Full-House Paterni",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 46,
        "narrative": (
            "Lupus nefritinin (özellikle Sınıf IV DPN) histopatolojik incelemesinde iki altın standart bulgu saptanır: "
            "1. **Işık Mikroskopisinde Tel Halkası (Wire Loop) Lezyonu:** "
            "Endotel hücreleri ile glomerül bazal membranı arasına (subendotelyal alana) devasa immün kompleks kitleleri çöker. "
            "Bu durum kapiller duvarların aşırı derecede sert, kalın ve kıvrımlı görünmesine yol açar; ışık mikroskopisinde "
            "adeta sert bir bükülmüş tel görünümü verdiğinden **wire loop (tel halkası) lezyonu** olarak adlandırılır. "
            "2. **İmmünofloresanda Tam Ev (Full-House) Paterni:** "
            "Diğer böbrek hastalıklarında izole tek bir immünoglobulin (örneğin IgA nefropatisinde yalnız IgA) çökerken, "
            "lupus nefritinde **tüm immünoglobulin sınıfları (IgG, IgA, IgM)** ve **tüm kompleman bileşenleri (C3, C1q)** "
            "birlikte pozitif boyanır. Bu çoklu pozitiflik tablosuna **Full-House (Tam Ev) Floresan Paterni** denir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Lupus Nefriti İmmünofloresan ve Mikroskopi Damgaları",
                ["Patolojik Yöntem", "Karakteristik Patolojik Terim", "Lezyonun Anatomik Yeri", "Tanısal Önemi"],
                [
                    [
                        "Işık Mikroskopisi",
                        "Wire loop (Tel halkası)",
                        {"text": "Subendotelyal immün kompleks birikimi", "isMasked": True, "hint": "Endotel ile bazal membran arasına masif pıhtı çökmesi"},
                        "Sınıf IV DPN için son derece karakteristiktir"
                    ],
                    ["İmmünofloresan", "Full-House (Tam Ev) paterni", "Mezangiyum ve kapiller duvarlar", "IgG, IgA, IgM, C3, C1q eşzamanlı pozitifliği"],
                    ["Elektron Mikroskopisi", "Parmak izi (fingerprint) birikimler", "Subendotelyal ve mezangiyal elektron-yoğun alan", "Kriyoimmünoglobulin kristalizasyonu"]
                ]
            ),
            make_active_recall(
                "Lupus nefriti immünofloresan mikroskopisinde IgG, IgA, IgM, C3 ve C1q moleküllerinin hepsinin birden eşzamanlı pozitif boyanması fenomenine ne ad verilir?",
                "Full-House (Tam Ev) floresan paterni denir.",
                "Tüm immünoglobulin ve kompleman sınıflarının bir arada glomerüle oturduğu floresan tablosu"
            )
        ]
    })

    # Slayt 47: Deri Patolojisi: Kelebek Raş, Diskoid Lezyon ve Lupus Band Testi
    slides.append({
        "id": "k1-25-s47",
        "title": "Deri Patolojisi: Kelebek Raş, Diskoid Lezyon ve Lupus Band Testi",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 47,
        "narrative": (
            "Deri tutulumu SLE hastalarının %80'inden fazlasında görülür ve klinik tanıda kritik öneme sahiptir: "
            "1. **Malar (Kelebek) Raş:** Yüzde her iki yanak ve burun köprüsünü kaplayan, güneş temasıyla alevlenen, "
            "karakteristik olarak **nazolabiyal olukları koruyan** kırmızı kabarıklıktır. "
            "2. **Kronik Diskoid Lupus:** Skar bırakan, foliküler tıkaçlar, skuam, hiperpigmentasyon halkası ve santral atrofiyle seyreden plaklardır. "
            "3. **Histopatoloji (Likenoid İnterfaz Dermatiti):** Epidermis bazal tabakasında hidropik dejenerasyon ve vakuolizasyon, "
            "dermal-epidermal bileşkede lenfosit infiltrasyonu ve dermal ödem izlenir. "
            "4. **Lupus Band Testi:** Deri biyopsisinde immünofloresan yöntemiyle dermo-epidermal bileşke boyunca **kesintisiz granüler "
            "IgG ve kompleman (C3) birikim bandının** gösterilmesidir. Sistemik SLE'de bu bant hem lezyonlu deride hem de **güneş görmeyen "
            "sağlam deride** pozitiftir; diskoid lupusta ise yalnız lezyonlu deride pozitiftir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Lupus Band Testi: Sistemik SLE vs Diskoid Lupus Ayrımı",
                "Sistemik Lupus Eritematozus (SLE)",
                "Dermo-epidermal bileşkedeki granüler immünoglobulin bandı HEM lezyonlu deride HEM sağlam deride pozitiftir",
                "Diskoid Lupus Eritematozus (Kutanöz)",
                "İmmünoglobulin bandı YALNIZCA lezyonlu deride pozitiftir; güneş görmeyen sağlam deride daima negatiftir"
            ),
            make_micro_quiz(
                "Deri biyopsisinde dermo-epidermal bileşkede immünofloresanla granüler IgG ve C3 birikiminin gösterildiği 'Lupus Band Testi'nin güneş görmeyen sağlam deride de pozitif olması hangisini gösterir?",
                {
                    "A": "Hastalığın sistemik tutulumlu (SLE) olduğunu",
                    "B": "Yalnızca lokalize diskoid lupus olduğunu",
                    "C": "Primer histiyositoz X hastalığını",
                    "D": "Aktinik keratoz zemininde skuamöz karsinomu",
                    "E": "Dermatitis herpetiformis hastalığını"
                },
                "A",
                {
                    "A": "Doğrudur; sağlam deride lupus bandının pozitif olması sistemik vasküler immün kompleks dolaşımını (SLE) kanıtlar.",
                    "B": "Yanlış; diskoid lupusta sağlam deride negatif çıkar.",
                    "C": "Yanlış; histiyositoz CD1a pozitif neoplazidir.",
                    "D": "Yanlış; karsinom immün kompleks hastalığı değildir.",
                    "E": "Yanlış; dermatitis herpetiformiste dermal papillalarda IgA birikir."
                }
            )
        ]
    })

    # Slayt 48: Kardiyovasküler Tutulum: Libman-Sacks Endokarditi ve Perikardit
    slides.append({
        "id": "k1-25-s48",
        "title": "Kardiyovasküler Tutulum: Libman-Sacks Endokarditi ve Perikardit",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 48,
        "narrative": (
            "Lupus kardiyovasküler sistemin tüm katmanlarını (perikard, miyokard ve endokard) tutabilir: "
            "1. **Perikardit (En Sık Kardiyak Tutulum):** Hastaların yaklaşık %50'sinde perikardiyal efüzyon ve seröfibrinöz "
            "perikardit gelişir; retrosternal plöritik göğüs ağrısı yapar. "
            "2. **Libman-Sacks Endokarditi (Nonbakteriyel Verrukoz Endokardit):** "
            "- **Vejetasyon Özelliği:** 1 ile 4 mm boyutlarında, steril, verrüköz, pembe-gri renkli pıhtı kümeleridir. "
            "- **Eşsiz Anatomik Yerleşim:** İnfektif endokardit vejetasyonları yalnızca akım yüzeyinde otururken; "
            "Libman-Sacks vejetasyonları kapak yaprakçıklarının **HER İKİ YÜZÜNDE (hem inflow hem outflow yüzeyinde)**, "
            "korda tendinealarda ve hatta mural endokard üzerinde yerleşir. "
            "- **Histopatoloji:** Fibrinoid nekroz, organize trombüs ve hematoksilin cisimcikleri içerir; bakteri barındırmaz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Kardiyak Endokardit Tiplerinin Ayırıcı Tanı Tablosu",
                ["Endokardit Tipi", "Vejetasyonun Anatomik Oturumu", "Bakteri İçeriği", "Klinik Zemin"],
                [
                    ["İnfektif Endokardit", "Kapakların sadece akım yüzeyinde (inflow)", "CANLI BAKTERİ İÇERİR (Süpüratif)", "S. aureus / Streptokok bakteriyemisi"],
                    [
                        "Libman-Sacks Endokarditi",
                        "Kapakların her iki yüzünde ve kordalarda",
                        {"text": "STERİL (Bakteri içermez)", "isMasked": True, "hint": "Kültürde üremeyen immün kompleks kökenli verrüköz pıhtı"},
                        "Sistemik Lupus Eritematozus ve APS"
                    ],
                    ["Nonbakteriyel Trombotik (NBTE)", "Kapanma hattında pürüzsüz nodüller", "STERİL (Fibrin ve trombosit)", "Müsinöz adenokarsinom (Marantik)"]
                ]
            ),
            make_active_recall(
                "Sistemik Lupus Eritematozus hastalarında kalp kapak yaprakçıklarının her iki yüzünde yerleşen steril verrüköz vejetasyonlara verilen ad nedir?",
                "Libman-Sacks endokarditidir (Nonbakteriyel verrukoz endokardit).",
                "Lupus kapak tutulumuna özgü steril vejetasyon sendromu"
            )
        ]
    })

    # Slayt 49: Checkpoint 5
    slides.append({
        "id": "k1-25-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Sistemik Lupus Eritematozus ve Lupus Nefriti",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 49,
        "narrative": (
            "Bu beşinci kontrol noktasında, Sistemik Lupus Eritematozus patolojisini ve tanısal damgalarını özetliyoruz: "
            "1. **Etyoloji:** Genç kadınlarda (9:1), HLA-DR2/DR3 ve C1q/C2/C4 eksikliğinde apoptotik enkazın temizlenememesi. "
            "2. **Patogenez:** UV hasarı, TLR-7/TLR-9 aktivasyonu ve plazmasitoid dendritik hücrelerden masif Tip I IFN (IFN-alfa). "
            "3. **Otoantikorlar:** ANA en duyarlı (%98, tarama); Anti-dsDNA nefrit ve aktiviteyle korele; Anti-Sm en spesifik (%99); "
            "Anti-histon ilaca bağlı lupusta; Antifosfolipid tromboz ve tekrarlayan düşük yapar. "
            "4. **Lupus Nefriti:** En sık ve ağır sınıf IV Diffüz Proliferatif Nefrittir (DPN); mikroskopide tel halkası (wire loop), "
            "immünofloresanda tüm antikor ve komplemanların yandığı Full-House paterni görülür. "
            "5. **Deri ve Kalp:** Kelebek raş, lupus band testi; kalpte her iki kapak yüzünde steril Libman-Sacks endokarditi izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s49-1",
                "Sistemik Lupus Eritematozus tanısında hastaların yüzde doksan sekizinde pozitif çıkan ve taramada kullanılan en duyarlı otoantikor hangisidir?",
                "Antinükleer antikorlardır (ANA).",
                "Negatif saptandığında SLE tanısını ekarte ettiren birinci basamak tarama belirteci",
                "ANA Duyarlılığı"
            ),
            make_flashcard(
                "k1-25-fc-s49-2",
                "Lupus nefritinde immün komplekslerin subendotelyal alana masif çökmesiyle kapiller duvarların aşırı kalınlaşması manzarasına ne ad verilir?",
                "Tel halkası (wire loop) lezyonu denir.",
                "Bükülmüş sert metal tel benzeri eozinofilik kılcal damar genişlemesi",
                "Wire Loop Lezyonu"
            ),
            make_flashcard(
                "k1-25-fc-s49-3",
                "SLE hastalarında mitral kapak yaprakçıklarının her iki yüzünde ve kordalarda yerleşen steril verrüköz vejetasyonlara ne ad verilir?",
                "Libman-Sacks endokarditi denir.",
                "Bakteriyel enfeksiyon olmaksızın gelişen immün kompleks kökenli kardiyak kapak tutulumu",
                "Libman-Sacks Endokarditi"
            )
        ],
        "interactiveElements": [
            make_table(
                "SLE Checkpoint Büyük Özet Tablosu",
                ["Organ / Sistem", "Karakteristik Patolojik Lezyon", "Mikroskobik / İmmünolojik Belirteç", "Klinik Yansıması"],
                [
                    ["Böbrek (Nefrit)", "Sınıf IV Diffüz Proliferatif Nefrit", "Wire loop lezyonları, Full-House IF", "Hematüri, proteinüri, azotemi"],
                    ["Kalp", "Libman-Sacks endokarditi", "Her iki kapak yüzünde steril vejetasyon", "Üfürüm, perikardit ağrısı"],
                    [
                        "Deri",
                        "Malar kelebek raş ve diskoid lezyon",
                        {"text": "Lupus band testi (sağlam deride bile pozitif)", "isMasked": True, "hint": "Dermo-epidermal bileşkedeki granüler immünoglobulin birikimi"},
                        "Güneşle artan fotosensitif eritem"
                    ],
                    ["Damar Sistemi", "Fosfolipid trombozu (APS)", "Antifosfolipid antikorları, uzamış aPTT", "Tekrarlayan düşükler ve DVT"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki otoantikorlardan hangisinin titre yüksekliği Sistemik Lupus Eritematozus hastalarında aktif glomerülonefrit varlığı ve hastalık alevlenmesi ile en yakın korelasyonu gösterir?",
                {
                    "A": "Anti-dsDNA (Çift sarmallı DNA)",
                    "B": "Anti-Sentromer antikoru",
                    "C": "Anti-Scl-70 antikoru",
                    "D": "Anti-Histon antikoru",
                    "E": "Anti-Jo-1 antikoru"
                },
                "A",
                {
                    "A": "Doğrudur; Anti-dsDNA titresi lupus nefriti varlığı ve hastalık aktivitesiyle doğrudan paralel seyreder.",
                    "B": "Yanlış; anti-sentromer CREST sendromuna özgüdür.",
                    "C": "Yanlış; anti-Scl-70 diffüz sklerodermaya özgüdür.",
                    "D": "Yanlış; anti-histon ilaca bağlı lupusta pozitiftir fakat nefrit aktivitesini yansıtmaz.",
                    "E": "Yanlış; anti-Jo-1 dermatomiyozit antikorudur."
                }
            )
        ]
    })

    # Slayt 50: Bölüm Özeti: SLE'den Sjögren ve Sistemik Skleroz Patolojisine Geçiş
    slides.append({
        "id": "k1-25-s50",
        "title": "Bölüm Özeti: SLE'den Sjögren ve Sistemik Skleroz Patolojisine Geçiş",
        "section": "Sistemik Lupus Eritematozus (SLE) Patolojisi",
        "slideNumber": 50,
        "narrative": (
            "SLE sistemik otoimmünitenin nükleer antikor prototipidir; ancak diğer bağ dokusu hastalıkları farklı "
            "organ sistemlerini ve farklı immünolojik yolakları hedefler: "
            "1. **Sjögren Sendromu:** Bağışıklık sistemi doğrudan gözyaşı ve tükürük bezlerini hedef alarak yoğun lenfositik "
            "infiltrasyonla bezleri kurutur (ağız ve göz kuruluğu - kserostomi ve keratokonjonktivit sikka). "
            "Otoantikorları Anti-Ro (SSA) ve Anti-La'dır (SSB); bu hastalarda **B hücreli lenfoma riski 40 kat artmıştır**. "
            "2. **Sistemik Skleroz (Skleroderma):** Vasküler endotel hasarı ve kontrolsüz fibroblast aktivasyonuyla tüm deride ve "
            "iç organlarda taş gibi sert kollajen birikimi (fibrozis) gelişir. "
            "Bölüm 6'da Sjögren sendromunu, Sistemik Sklerozu (Diffüz vs CREST) ve inflamatuvar miyopatileri inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Sistemik Romatolojik Spektrum",
                "Sistemik Lupus Eritematozus",
                "Nükleer antijenlere karşı otoantikorlar, immün kompleks vasküliti ve yaygın nekroz",
                "Sjögren ve Sistemik Skleroz",
                "Eksokrin bezlerin lenfositik harabiyeti (Sjögren) veya masif fibroblast aktivasyonuyla yaygın fibrozis (Skleroderma)"
            ),
            make_active_recall(
                "Gözyaşı ve tükürük bezlerinin lenfositik yıkımı sonucu göz ve ağız kuruluğuyla seyreden ve B hücreli MALT lenfoma riskini 40 kat artıran otoimmün hastalık hangisidir?",
                "Sjögren sendromudur.",
                "Kserostomi ve keratokonjonktivit sikka ile karakterize otoimmün ekzokrinopati"
            )
        ]
    })

    return slides
