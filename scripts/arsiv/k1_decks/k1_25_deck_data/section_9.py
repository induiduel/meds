# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 9: HIV/AIDS Patogenezi ve Amiloidoz Biyolojisi (Slayt 81 - 90)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # Slayt 81: HIV/AIDS Epidemiyolojisi ve Retrovirüs Yapısı
    slides.append({
        "id": "k1-25-s81",
        "title": "HIV/AIDS Epidemiyolojisi ve Retrovirüs Yapısı",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 81,
        "narrative": (
            "Kazanılmış İmmün Yetmezlik Sendromu (AIDS), İnsan İmmün Yetmezlik Virüsünün (HIV) yol açtığı, "
            "derin hücresel immün yetmezlik, fırsatçı enfeksiyonlar ve sekonder malignitelerle seyreden ölümcül pandemidir: "
            "1. **Viral Morfoloji:** HIV, Retroviridae ailesinin Lentivirüs cinsine ait zarflı bir RNA virüsüdür. "
            "Viral merkezde iki özdeş tek iplikli RNA kopyası ve viral enzimler (Revers Transkriptaz, İntegraz, Proteaz) bulunur. "
            "Bu çekirdek **p24 majör kapsid proteini** ile sarılıdır (kanda p24 antijen tespiti erken tanıda kullanılır). "
            "2. **Zarf Glikoproteinleri (Hedefe Kilitlenme):** "
            "- **gp120 (Yüzeyel Başlık):** Konak hücresi yüzeyindeki CD4 molekülüne ve kemokin koreseptörlerine bağlanan proteindir. "
            "- **gp41 (Transmembran Sap):** gp120 bağlanmasından sonra virüs lipid zarfını konak hücre zarıyla kaynaştıran proteindir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "HIV Viral Proteinleri ve Biyolojik Fonksiyonları",
                ["Viral Protein", "Anatomik Konumu", "Hedef Yapı / Fonksiyon", "Klinik Tanısal Önemi"],
                [
                    ["gp120", "Viral zarf dış glikoproteini", "CD4 molekülü ve CCR5/CXCR4 koreseptörleri", "Hücreye tutunma ve enfeksiyonun başlaması"],
                    ["gp41", "Viral zarf transmembran sapı", "Konak hücre plazma membranı", "Membran füzyonu ve nükleokapsid girişi"],
                    [
                        "p24",
                        "İç silindirik kapsid proteini",
                        {"text": "Viral RNA ve enzimlerin kılıfı", "isMasked": True, "hint": "Erken dönemde kanda ELISA ile saptanan majör viral kapsid antijeni"},
                        "Akut enfeksiyon pencere döneminde serolojik belirteç"
                    ],
                    ["Revers Transkriptaz", "İç enzim", "Viral RNA'dan proviral çift zincir DNA sentezi", "Antiretroviral tedavide primer hedef"]
                ]
            ),
            make_active_recall(
                "İnsan İmmün Yetmezlik Virüsünün (HIV) konak hücre zarıyla virüs zarfının kaynaşmasını (füzyon) sağlayan transmembran glikoproteini hangisidir?",
                "gp41 glikoproteinidir.",
                "Viral füzyondan sorumlu kırk bir kilodaltonluk transmembran protein"
            )
        ]
    })

    # Slayt 82: HIV Yaşam Döngüsü ve Koreseptörler (CCR5 ve CXCR4)
    slides.append({
        "id": "k1-25-s82",
        "title": "HIV Yaşam Döngüsü ve Koreseptörler (CCR5 ve CXCR4)",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 82,
        "narrative": (
            "HIV'in bir hücreyi enfekte edebilmesi için yalnızca CD4 molekülü yetmez; kemokin koreseptörlerine de bağlanmalıdır: "
            "1. **Koreseptörler ve Viral Tropizm:** "
            "- **CCR5 (R5 Virüsleri - Makrofagotrofik):** Mukoza epiteli altındaki makrofajları, dendritik hücreleri ve T hücrelerini enfekte eder. "
            "Cinsel temasla bulaşmada ve **erken enfeksiyon fazında** baskın olan suşlardır. Toplumda homozigot **CCR5-delta32** delesyonu "
            "taşıyan bireyler HIV bulaşmasına karşı doğal olarak dirençlidir. "
            "- **CXCR4 (X4 Virüsleri - T-trofik):** Enfeksiyonun geç döneminde mutasyonla ortaya çıkar; saf T hücrelerini hızla enfekte eder. "
            "2. **Hücre İçi Döngü:** Virüs içeri girdikten sonra Revers Transkriptaz viral RNA'dan proviral DNA üretir. "
            "Viral **İntegraz**, bu DNA'yı konak nükleer kromozomuna kalıcı olarak entegre eder (provirüs). "
            "T hücresi aktive olduğunda NF-kappaB viral transkripsiyonu patlatır; yeni viryonlar tomurcuklanarak kana dökülür."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "HIV Hücre İçi Yaşam Döngüsü",
                [
                    "1. Tutunma ve Füzyon: gp120'nin CD4 ve CCR5/CXCR4'e bağlanması, gp41 ile membran füzyonu",
                    "2. Ters Transkripsiyon: Revers transkriptaz ile tek zincir RNA'dan çift zincir proviral DNA sentezi",
                    "3. Genomik Entegrasyon: Viral integraz enziminin provirüsü insan kromozomuna kalıcı dikmesi",
                    "4. Tomurcuklanma ve Matürasyon: Viral proteaz ile yeni proteinlerin kesilip enfektif viryon saçılması"
                ]
            ),
            make_cloze(
                "HIV'in erken bulaşma fazında makrofajları ve T hücrelerini enfekte etmek için kullandığı primer kemokin koreseptörü CCR5 reseptörüdür.",
                "CCR5",
                "Doğal delta-32 delesyonunda HIV enfeksiyonuna direnç sağlayan koreseptör"
            )
        ]
    })

    # Slayt 83: CD4+ T Hücre Tükenmesi ve İmmün Çöküş Mekanizmaları
    slides.append({
        "id": "k1-25-s83",
        "title": "CD4+ T Hücre Tükenmesi ve İmmün Çöküş Mekanizmaları",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 83,
        "narrative": (
            "HIV enfeksiyonunun nihai sonucu, hücresel bağışıklığın orkestra şefi olan CD4+ T lenfositlerinin yok edilmesidir: "
            "1. **Tükenme Mekanizmaları:** "
            "- **Doğrudan Viral Lizis:** Milyarlarca yeni virüsün hücre zarından tomurcuklanması hücre zar bütünlüğünü bozar. "
            "- **Piropitoz (Seyirci Hücre Ölümü):** Lenf nodundaki enfekte olmamış naif T hücreleri, biriken viral DNA parçalarını algılayarak "
            "inflamazom ve kaspaz-1 aktivasyonuyla iltihaplı hücre intiharına (**piropitoz**) gider (en büyük T hücresi kaybı yoludur). "
            "- **CD8+ CTL Saldırısı:** Sitotoksik T hücreleri viral peptit taşıyan CD4+ hücreleri yabancı bilip öldürür. "
            "2. **Klinik AIDS Eşiği:** Sağlıklı insanda periferik CD4+ T hücresi sayısı 1000-1500 / mikrolitredir. "
            "Yıllar süren kronik fazda sayı yavaşça erir; CD4 sayısı **<200 / mikrolitre** düzeyine indiğinde hücresel bağışıklık tamamen çöker ve "
            "resmi olarak ölümcül **AIDS tablosu** ilan edilir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "HIV Enfeksiyonu Evreleri ve CD4 Sayısı",
                "Kronik Latent Faz",
                "CD4 sayısı 200-500 arasında, minimal semptomlar, lenf nodlarında sürekli replikasyon ve immün denge",
                "İlerlemiş AIDS Evresi",
                "CD4 sayısı <200 altına düşmüş, hücresel immünite tamamen çökmüş, ölümcül fırsatçı enfeksiyonlar ve tümörler"
            ),
            make_micro_quiz(
                "HIV ile enfekte bir hastada hücresel immün yetmezliğin son evresi olan AIDS tanısının konulması için periferik kanda CD4+ T lenfosit sayısının hangi kritik eşik değerin altına inmesi gerekir?",
                {
                    "A": "200 hücre / mikrolitre",
                    "B": "500 hücre / mikrolitre",
                    "C": "800 hücre / mikrolitre",
                    "D": "1000 hücre / mikrolitre",
                    "E": "50 hücre / mikrolitre"
                },
                "A",
                {
                    "A": "Doğrudur; CD4 sayısının 200'ün altına düşmesi AIDS tanım kriteridir ve fırsatçı enfeksiyonları başlatır.",
                    "B": "Yanlış; 500 normal ile latent sınırıdır.",
                    "C": "Yanlış; bu düzeyde bağışıklık korunur.",
                    "D": "Yanlış; normal sağlıklı insan düzeyidir.",
                    "E": "Yanlış; 50 terminal son dönemdir."
                }
            )
        ]
    })

    # Slayt 84: HIV/AIDS Fırsatçı Enfeksiyonları ve Maligniteleri
    slides.append({
        "id": "k1-25-s84",
        "title": "HIV/AIDS Fırsatçı Enfeksiyonları ve Maligniteleri",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 84,
        "narrative": (
            "CD4+ T hücrelerinin çöküşü, normalde sağlıklı bireyde hastalık yapamayan mikroorganizmaların vücudu istila etmesine yol açar: "
            "1. **Fırsatçı Enfeksiyonlar:** "
            "- **Pneumocystis jirovecii Pnömonisi (PCP):** AIDS hastalarında en sık görülen ve ölüme yol açan primer fırsatçı akciğer enfeksiyonudur; "
            "alveollerde köpüksü eksüda ve gümüş boyasıyla fincan tabağı biçimli kistler görülür. "
            "- **Diğer Patojenler:** Candida albicans özofajiti, Cryptococcus neoformans menenjiti, Toxoplasma gondii beyin apseleri (halka şeklinde lezyonlar), "
            "Sitomegalovirüs (CMV) retiniti/koliti ve Mycobacterium avium-intracellulare (MAC) dissemine enfeksiyonu. "
            "2. **AIDS İlişkili Maligniteler:** "
            "- **Kaposi Sarkomu (KS):** **İnsan Herpesvirüs 8 (HHV-8)** ile enfekte endotel hücrelerinin oluşturduğu vasküler iğsi hücreli tümördür. "
            "- **Primer SSS Lenfoması:** **Epstein-Barr Virüsü (EBV)** ile ilişkili yüksek dereceli diffüz büyük B hücreli lenfomadır. "
            "- İnvaziv servikal karsinom (HPV)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "AIDS İlişkili Fırsatçı Ajanlar ve Maligniteler",
                ["Klinik Tablo", "Etyolojik Patojen Ajan", "Karakteristik Patolojik Lezyon", "Hedef Organ"],
                [
                    ["PCP Pnömonisi", "Pneumocystis jirovecii (Mantar)", "Alveollerde köpüksü eksüda, gümüş boyalı kistler", "Akciğerler"],
                    [
                        "Kaposi Sarkomu",
                        "İnsan Herpesvirüs 8 (HHV-8)",
                        {"text": "İğsi hücreler, vasküler yarıklar ve eritrosit ekstravazasyonu", "isMasked": True, "hint": "Deri ve mukozalarda mor-kırmızı nodüller oluşturan vasküler neoplazi"},
                        "Deri, ağız mukozası, GİS"
                    ],
                    ["Primer SSS Lenfoması", "Epstein-Barr Virüsü (EBV)", "Perivasküler atipik B lenfosit infiltratı", "Beyin parankimi"],
                    ["Beyin Apseleri", "Toxoplasma gondii (Protozoon)", "Kontrast tutan çok odaklı halka lezyonları", "Bazal gangliyonlar ve korteks"]
                ]
            ),
            make_active_recall(
                "AIDS hastalarında deride ve iç organlarda mor-kırmızı vasküler nodüller oluşturan Kaposi sarkomunun gelişiminden sorumlu olan onkojenik virüs hangisidir?",
                "İnsan Herpesvirüs 8 (HHV-8 / KSHV) virüsüdür.",
                "Kaposi sarkomu ilişkili sekizinci herpesvirüs ailesi üyesi"
            )
        ]
    })

    # Slayt 85: Amiloidoz Biyolojisi: Yanlış Katlanmış Proteinler ve Beta-Kırmalı Fibriller
    slides.append({
        "id": "k1-25-s85",
        "title": "Amiloidoz Biyolojisi: Yanlış Katlanmış Proteinler ve Beta-Kırmalı Fibriller",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 85,
        "narrative": (
            "Amiloidoz, çözünür normal proteinlerin anormal şekilde katlanarak dokularda çözünmeyen, proteolitik sindirime "
            "dirençli fibriller halinde hücre dışı (ekstraselüler) boşlukta birikmesiyle karakterize hastalıktır: "
            "1. **Beta-Kırmalı Tabaka (Cross-beta-pleated sheet):** Hangi proteinden köken alırsa alsın (hafif zincir, SAA vb.), "
            "tüm amiloid fibrilleri ortak bir üçüncül konformasyona sahiptir: **çapraz beta-kırmalı tabaka**. "
            "Bu katlanma amiloidi proteazlara karşı aşırı dirençli kılar; dokuda kalıcı birikime yol açar. "
            "2. **Elektron Mikroskopisi:** Tüm amiloid birikintileri elektron mikroskopisinde **7.5 ile 10 nm çapında**, "
            "dallanma göstermeyen, düz ve sert protein fibrillerinden oluşur. "
            "3. **Yardımcı Bileşenler:** Fibrillere her zaman Serum Amiloid P (SAP) bileşeni ve proteoglikanlar eşlik eder; "
            "biriken kütle parankim hücrelerini mekanik olarak ezer ve atrofiye uğratır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Amiloid Fibrillerinin Biyofiziksel Özellikleri",
                ["Yapısal Özellik", "Biyofiziksel Karşılığı", "Patolojik Önemi"],
                [
                    ["Tersiyer Konformasyon", "Çapraz beta-kırmalı tabaka (cross-beta sheet)", "Tüm amiloid tiplerinin evrensel ortak iskeleti"],
                    [
                        "Elektron Mikroskopisi",
                        {"text": "7.5 - 10 nm çapında dallanmayan düz fibriller", "isMasked": True, "hint": "Amiloid liflerinin elektron mikroskobundaki kesin nano-ölçüsü"},
                        "Kolajen veya elastik liflerden ayırt ettirici morfoloji"
                    ],
                    ["Proteaz Duyarlılığı", "Lizozomal ve interstisyel enzimlere dirençli", "Doku makrofajlarınca eritilemeyip birikmesi"]
                ]
            ),
            make_active_recall(
                "Tüm amiloid tiplerinin köken aldığı proteinden bağımsız olarak sahip olduğu ve proteolitik parçalanmaya direnç sağlayan evrensel katlanma konformasyonu nedir?",
                "Çapraz beta-kırmalı tabaka (cross-beta-pleated sheet) yapısıdır.",
                "Kongo kırmızısı ile elma yeşili çift kırıcılık veren karakteristik katlanma mimarisi"
            )
        ]
    })

    # Slayt 86: Amiloidozun Boyanma Özellikleri ve Tanısal Altın Standart
    slides.append({
        "id": "k1-25-s86",
        "title": "Amiloidozun Boyanma Özellikleri ve Tanısal Altın Standart",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 86,
        "narrative": (
            "Amiloidozun kesin tanısı doku biyopsisinde spesifik histokimyasal ve optik boyanma özelliklerinin gösterilmesiyle konur: "
            "1. **Işık Mikroskopisinde Rutin H&E:** Standart Hematoksilen-Eozin (H&E) boyamasında amiloid; hücreler arasında, "
            "özellikle kan damarlarının duvarlarında ve bazal membranlarda biriken **amorf, homojen, asellüler, camsı (hiyalin) pembe** "
            "madde olarak izlenir. Kollajen skarla veya hiyalin dejenerasyonla karışabilir. "
            "2. **Kongo Kırmızısı (Congo Red) Boyası:** Amiloid için en güvenilir histokimyasal boyadır. Normal ışık mikroskopisinde "
            "amiloid birikintilerini kiremit kırmızısı / pembemsi-turuncu renge boyar. "
            "3. **Polarize Işık Mikroskopisi (Altın Standart):** Kongo kırmızısı ile boyanmış kesit polarize ışık mikroskobunda "
            "incelendiğinde, beta-kırmalı tabakanın ışığı kırması sonucu son derece karakteristik **parlak elma yeşili çift kırıcılık "
            "(apple-green birefringence)** oluşturur. Bu optik parıltı amiloidoz tanısı için mutlak patognomoniktir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Amiloidozun Mikroskobik Ayrımı",
                "Standart H&E Boyası",
                "Damar duvarlarında amorf, hiyalin, homojen eozinofilik pembe birikinti (Nonspesifik)",
                "Kongo Kırmızısı + Polarize Işık",
                "Beta tabakaların polarize ışığı kırmasıyla ortaya çıkan parlak ELMA YEŞİLİ ÇİFT KIRICILIK (Patognomonik)"
            ),
            make_micro_quiz(
                "Şüpheli bir böbrek biyopsisinde amiloidoz tanısını kesinleştirmek için Kongo kırmızısı ile boyanan doku kesitinin polarize ışık mikroskobunda vermesi gereken patognomonik optik bulgu hangisidir?",
                {
                    "A": "Parlak elma yeşili çift kırıcılık (apple-green birefringence)",
                    "B": "Koyu siyah kömürleşme manzarası",
                    "C": "Koyu mavi nükleer floresans ışıması",
                    "D": "Sarı-kahverengi granüler çökelti",
                    "E": "Tamamen ışıksız mat şeffaf görünüm"
                },
                "A",
                {
                    "A": "Doğrudur; Kongo kırmızısının polarize ışıkta verdiği elma yeşili çift kırıcılık amiloidozun tartışmasız altın standardıdır.",
                    "B": "Yanlış; gümüş boyalarında siyahlaşma görülür.",
                    "C": "Yanlış; bu DAPI nükleer floresanıdır.",
                    "D": "Yanlış; bu hemosiderindir.",
                    "E": "Yanlış; amiloid güçlü çift kırıcılık verir."
                }
            )
        ]
    })

    # Slayt 87: Başlıca Amiloid Proteinleri 1: AL Amiloidozu
    slides.append({
        "id": "k1-25-s87",
        "title": "Başlıca Amiloid Proteinleri 1: AL (İmmünoglobulin Hafif Zincir) Amiloidozu",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 87,
        "narrative": (
            "AL amiloidozu, Batı dünyasında sistemik amiloidoz vakalarının en sık ve klinik seyri en agresif formudur: "
            "1. **Öncül Protein:** Klonal plazma hücreleri tarafından aşırı üretilen **monoklonal immünoglobulin hafif zincirleridir** "
            "(özellikle **lambda - lambda hafif zincirleri**, daha az oranda kappa). "
            "2. **Etyolojik Zemin:** "
            "- Hastaların %15-20'sinde açık **Multipl Miyelom** eşlik eder. "
            "- Geri kalan %80'inde ise kemik iliğinde hafif bir klonal plazma hücresi artışı (monoklonal gamopati) bulunur (Eskiden 'Primer Amiloidoz' olarak adlandırılırdı). "
            "3. **Klinik Organ Tutulumları:** "
            "- **Kalp:** Restriktif kardiyomiyopati, düşük voltajlı EKG ve erken ölümcül kalp yetmezliği/aritmiler. "
            "- **Böbrek:** Ağır nefrotik sendrom ve proteinüri. "
            "- **Dil:** Dil parankiminde amiloid birikimiyle devasa dil (**makroglossi** - AL amiloidozuna çok karakteristiktir). "
            "- **Deri:** Periorbital alanda vasküler amiloid fragilitesine bağlı 'rakun gözü' purpuraları."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "AL Amiloidozunun Klinik ve Patolojik Karakteri",
                ["Özellik", "Patolojik / İmmünolojik Karşılığı", "Klinik Yansıması"],
                [
                    ["Öncül Protein", "Monoklonal immünoglobulin hafif zinciri (özellikle lambda)", "Serum/idrar immünfiksasyon elektroforezinde monoklonal pik"],
                    [
                        "Karakteristik Dil Bulgusu",
                        {"text": "Makroglossi (Dev dil)", "isMasked": True, "hint": "Dil kasları arasına hafif zincir amiloidi çökmesiyle dilin ağza sığmaması"},
                        "Konuşma ve yutma güçlüğü, obstrüktif uyku apnesi"
                    ],
                    ["Kardiyak Tutulum", "Restriktif kardiyomiyopati", "Düşük voltajlı EKG, kalp yetmezliği"],
                    ["Vasküler Kırılganlık", "Kapiller duvar amiloid infiltrasyonu", "Periorbital purpura (rakun gözü manzarası)"]
                ]
            ),
            make_active_recall(
                "Multipl miyelom veya plazma hücresi diskrazisi zemininde klonal monoklonal immünoglobulin hafif zincirlerinin (özellikle lambda) dokularda birikmesiyle oluşan amiloidoz tipi hangisidir?",
                "AL amiloidozudur (Primer amiloidoz).",
                "İmmünoglobulin hafif zincir türevi sistemik amiloid proteini"
            )
        ]
    })

    # Slayt 88: Başlıca Amiloid Proteinleri 2: AA (Serum Amiloid A) Amiloidozu
    slides.append({
        "id": "k1-25-s88",
        "title": "Başlıca Amiloid Proteinleri 2: AA (Serum Amiloid A) Amiloidozu",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 88,
        "narrative": (
            "AA amiloidozu, uzun süreli kronik inflamatuar süreçlerin zemininde gelişen sistemik amiloidoz tablosudur: "
            "1. **Öncül Protein (SAA):** Kronik inflamasyonda makrofaj kaynaklı sitokinler (**IL-6 ve IL-1**) karaciğeri uyararak "
            "bir akut faz reaktanı olan **Serum Amiloid A (SAA)** proteininin sentezini 1000 kata kadar artırır. "
            "Dolaşımdaki SAA, makrofaj proteazlarınca kısmen parçalanarak 8.5 kDa'lık **AA amiloid proteinine** dönüşür ve dokulara çöker. "
            "2. **Etyolojik Hastalıklar:** "
            "- Kronik otoimmün artritler (**Romatoid Artrit**, Ankilozan Spondilit). "
            "- Kronik enfeksiyonlar (**Bronşiektazi**, Kronik Osteomiyelit, Tüberküloz). "
            "- **Ailesel Akdeniz Ateşi (FMF):** MEFV genindeki pirin mutasyonuyla kontrolsüz IL-1 salınımı ve tekrarlayan peritonit atakları; "
            "tedavisiz FMF hastalarında kaçınılmaz olarak AA amiloidozu gelişir. "
            "3. **Hedef Organ:** AA amiloidozu en sık ve en ağır **böbrekleri** tutar; masif nefrotik sendrom ve üremiye yol açar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "AA Amiloidozu Gelişim Yolağı",
                [
                    "1. Kronik İnflamasyon: RA, bronşiektazi veya FMF zemininde aralıksız IL-6 ve IL-1 fırtınası",
                    "2. Karaciğerde SAA Patlaması: Hepatositlerden Serum Amiloid A proteininin kanda bin kat yükselmesi",
                    "3. Mononükleer Proteoliz: Makrofaj enzimlerinin SAA'yı çözünmeyen AA fragmanına çevirmesi",
                    "4. Glomerüler Amiloidoz: Böbrek glomerül mezangiyumuna çökerek masif nefrotik sendrom yapması"
                ]
            ),
            make_cloze(
                "Kronik osteomiyelit, romatoid artrit veya FMF zemininde karaciğerden sentezlenen akut faz proteini SAA'dan köken alan amiloidoz tipi AA amiloidozudur.",
                "AA",
                "Serum amiloid A proteininden üretilen sekonder amiloidoz kısaltması"
            )
        ]
    })

    # Slayt 89: Checkpoint 9
    slides.append({
        "id": "k1-25-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] HIV/AIDS İmmünopatolojisi ve Amiloid Proteini Biyolojisi",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 89,
        "narrative": (
            "Bu dokuzuncu kontrol noktasında, HIV/AIDS patogenezini ve amiloidoz biyolojisini pekiştiriyoruz: "
            "1. **HIV Mimarisi:** gp120 CD4 ve CCR5/CXCR4'e tutunur; gp41 füzyon yapar; p24 kapsid proteinidir. "
            "2. **Tropizm:** Erken bulaşta makrofagotrofik CCR5 (delta-32 koruyucudur); geç dönemde T-trofik CXCR4 kullanılır. "
            "3. **AIDS Eşiği:** CD4 sayısı <200/mikrolitreye düştüğünde fırsatçı enfeksiyonlar (PCP pnömonisi) ve tümörler (HHV-8 Kaposi) başlar. "
            "4. **Amiloid Biyofiziği:** Yanlış katlanmış proteinlerin çapraz beta-kırmalı tabaka konformasyonunda 7.5-10 nm fibriller yapmasıdır. "
            "5. **Tanısal Standart:** Kongo kırmızısı ile boyanan amiloid, polarize ışık mikroskobunda parlak elma yeşili çift kırıcılık verir. "
            "6. **AL vs AA:** AL immünoglobulin monoklonal hafif zinciridir (Miyelom, makroglossi); AA ise kronik inflamasyonda karaciğer SAA'sından türer (FMF, böbrek)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s89-1",
                "HIV'in erken dönemde makrofaj ve T hücrelerine girişte kullandığı ve genetik homozigot delesyonunda virüse karşı bağışıklık sağlayan kemokin koreseptörü nedir?",
                "CCR5 koreseptörüdür.",
                "Delta-32 varyantı doğal direnç oluşturan beta-kemokin reseptör ailesi üyesi",
                "CCR5 ve Direnç"
            ),
            make_flashcard(
                "k1-25-fc-s89-2",
                "Amiloid birikintilerinin Kongo kırmızısı boyası sonrasında polarize ışık mikroskobunda verdiği patognomonik optik kırılma rengi nedir?",
                "Elma yeşili çift kırıcılıktır.",
                "Polarize filtreler altında amiloid beta tabakalarının saçtığı karakteristik zümrüt pırıltısı",
                "Elma Yeşili Çift Kırıcılık"
            ),
            make_flashcard(
                "k1-25-fc-s89-3",
                "Plazma hücresi diskrazileri ve multipl miyelom zemininde monoklonal immünoglobulin hafif zincirlerinin dokularda birikmesiyle oluşan amiloid türü nedir?",
                "AL tipi amiloidozdur.",
                "Hafif zincir lambda veya kappa peptidinden köken alan primer varyant",
                "AL Amiloidozu"
            )
        ],
        "interactiveElements": [
            make_table(
                "HIV ve Amiloidoz Checkpoint Karşılaştırma Matrisi",
                ["Kavram", "Temel Moleküler Bileşen", "Altın Standart Patoloji Bulgusu", "Primer Klinik Sonuç"],
                [
                    ["HIV Hücre Girişi", "gp120 / gp41 ve CD4 + CCR5", "CD4+ T hücre tükenmesi (<200)", "AIDS, fırsatçı enfeksiyonlar"],
                    ["AIDS Tümörleri", "HHV-8 (Kaposi) ve EBV (Lenfoma)", "İğsi hücreli endotel proliferasyonu", "Mor kutanöz nodüller, SSS kitlesi"],
                    [
                        "Amiloidoz Fiziği",
                        "Çapraz beta-kırmalı tabakalar",
                        {"text": "Kongo kırmızısı ile elma yeşili çift kırıcılık", "isMasked": True, "hint": "Polarize ışık mikroskobunda amiloidi tescilleyen renk değişimi"},
                        "Doku hücrelerinin mekanik ezilmesi ve atrofi"
                    ],
                    ["AL Amiloidozu", "Monoklonal hafif zincir (lambda)", "Plazma hücresi diskrazisi, kemik iliği klonu", "Makroglossi, restriktif kardiyomiyopati"],
                    ["AA Amiloidozu", "Serum Amiloid A (SAA)", "Kronik inflamasyon, FMF, romatoid artrit", "Masif nefrotik sendrom, böbrek yetmezliği"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi amiloidozun histopatolojik tanısında polarize ışık mikroskobunda patognomonik elma yeşili çift kırıcılık veren biyofiziksel yapısal özelliktir?",
                {
                    "A": "Proteinlerin çapraz beta-kırmalı tabaka konformasyonunda katlanmış olması",
                    "B": "Yalnızca kalsiyum tuzlarının kristalleşmesi",
                    "C": "Hücre zarındaki fosfolipidlerin çift katmanlı dizilimi",
                    "D": "DNA sarmallarının nükleozom etrafına sarılması",
                    "E": "Hemoglobin molekülünün demir içermesi"
                },
                "A",
                {
                    "A": "Doğrudur; beta-kırmalı tabaka yapısı Kongo kırmızısı boyasını düzenli aralıklarla bağlayarak polarize ışığı elma yeşili kırar.",
                    "B": "Yanlış; kalsiyum bazofilik boyanır ve çift kırıcılık amiloid değildir.",
                    "C": "Yanlış; membran fosfolipidi çift kırıcılık vermez.",
                    "D": "Yanlış; nükleozom kromatin yapısıdır.",
                    "E": "Yanlış; hemoglobin eritrosit içindedir."
                }
            )
        ]
    })

    # Slayt 90: Bölüm Özeti: Diğer Amiloid Tiplerine ve Büyük Senteze Geçiş
    slides.append({
        "id": "k1-25-s90",
        "title": "Bölüm Özeti: Diğer Amiloid Tiplerine ve Büyük Senteze Geçiş",
        "section": "HIV/AIDS ve Amiloidoz Biyolojisi",
        "slideNumber": 90,
        "narrative": (
            "AL ve AA amiloidozun en yaygın sistemik formlarıdır; ancak amiloid protein ailesi çok daha geniştir: "
            "1. **ATTR (Transtiretin):** Tiroksin ve retinol taşıyıcı proteindir. Mutant formu ailesel amiloid polinöropatilerinde; "
            "yabanıl (wild-type) normal formu ise yaşlı bireylerin kalbinde birikerek **senil kardiyak amiloidoz** yapar. "
            "2. **Abeta2m (Beta-2 Mikroglobulin):** Uzun süreli hemodiyaliz hastalarında glomerülden süzülemediği için birikir ve "
            "eklemlerde **karpal tünel sendromu** ve artrit oluşturur. "
            "3. **Abeta Proteini:** Alzheimer hastalığında serebral kortekste amiloid plaklarını ve anjiyopatisini yapar. "
            "4. **Lokalize Endokrin Amiloidler:** Tiroid medüller karsinomunda prokalsitonin amiloidi, Tip 2 DM'de amilin birikimi. "
            "Son bölümümüzde (Bölüm 10) organ amiloidozlarını (böbrek, dalak, kalp), Robbins patoloji spotlarını ve dersin büyük sentezini tamamlayacağız."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Sistemik vs Lokalize Amiloidoz Spektrumu",
                "Sistemik Amiloidozlar (AL, AA)",
                "Dolaşımdan kaynaklanan öncül proteinlerle böbrek, kalp, karaciğer ve dalağın eşzamanlı tutulumu",
                "Lokalize ve Senil Amiloidozlar (Abeta, ATTR, Endokrin)",
                "Tek bir organda sınırlı birikim (Beyinde Alzheimer Abeta'sı, yaşlı kalpte normal Transtiretin, tiroidde kalsitonin)"
            ),
            make_active_recall(
                "Kronik hemodiyaliz hastalarında diyaliz membranından süzülemediği için biriken ve özellikle sinovyada birikerek karpal tünel sendromu yapan amiloid proteini hangisidir?",
                "Beta-2 mikroglobulin amiloididir (Abeta2m).",
                "MHC Sınıf I molekülünün hafif zincirinden köken alan diyaliz ilişkili amiloid"
            )
        ]
    })

    return slides
